#!/usr/bin/env python3
"""Send resume PDF to HR emails via personal SMTP (one-to-one, rate-limited)."""

from __future__ import annotations

import argparse
import csv
import smtplib
import sys
import time
from email.header import Header
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formataddr
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DEFAULT_ENV = ROOT / ".env"
DEFAULT_EMAILS = ROOT / "emails.txt"
DEFAULT_SUMMARY_CANDIDATES = (
    ROOT / "companies.csv",
    ROOT / "招聘汇总.csv",
)
DEFAULT_LOG = ROOT / "sent_log.csv"
LOG_FIELDS = ["time", "email", "company", "result", "detail"]
PLACEHOLDER_AUTH = {
    "your_163_authorization_code",
    "your_authorization_code",
    "在这里粘贴163授权码",
}


def _configure_stdio() -> None:
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8")
        except Exception:
            pass


def load_env(path: Path) -> dict[str, str]:
    if not path.is_file():
        raise SystemExit(
            f"Missing {path.name}. Copy .env.example to .env and fill in your 163 settings."
        )
    env: dict[str, str] = {}
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        env[key.strip()] = value.strip().strip('"').strip("'")
    return env


def load_emails(path: Path) -> list[str]:
    if not path.is_file():
        raise SystemExit(f"Missing email list: {path}")
    emails: list[str] = []
    seen: set[str] = set()
    for line in path.read_text(encoding="utf-8").splitlines():
        email = line.strip()
        if not email or email.startswith("#") or "@" not in email:
            continue
        key = email.lower()
        if key in seen:
            continue
        seen.add(key)
        emails.append(email)
    return emails


def load_company_map(path: Path) -> dict[str, str]:
    """Map email -> company from companies.csv / 招聘汇总.csv when present."""
    mapping: dict[str, str] = {}
    if not path.is_file():
        return mapping
    with path.open(encoding="utf-8-sig", newline="") as fp:
        reader = csv.DictReader(fp)
        for row in reader:
            email = (row.get("邮箱") or row.get("email") or "").strip()
            company = (row.get("企业") or row.get("company") or "").strip()
            if not email or "@" not in email or not company:
                continue
            for part in email.replace("／", "/").split("/"):
                part = part.strip()
                if "@" in part:
                    mapping.setdefault(part.lower(), company)
    return mapping


def resolve_summary(explicit: Path | None) -> Path:
    if explicit is not None:
        return explicit
    for candidate in DEFAULT_SUMMARY_CANDIDATES:
        if candidate.is_file():
            return candidate
    return DEFAULT_SUMMARY_CANDIDATES[0]


def load_sent_ok(path: Path) -> set[str]:
    done: set[str] = set()
    if not path.is_file():
        return done
    with path.open(encoding="utf-8-sig", newline="") as fp:
        reader = csv.DictReader(fp)
        for row in reader:
            if (row.get("result") or "").strip().lower() == "ok":
                email = (row.get("email") or "").strip().lower()
                if email:
                    done.add(email)
    return done


def append_log(path: Path, row: dict[str, str]) -> None:
    new_file = not path.is_file()
    with path.open("a", encoding="utf-8-sig", newline="") as fp:
        writer = csv.DictWriter(fp, fieldnames=LOG_FIELDS)
        if new_file:
            writer.writeheader()
        writer.writerow(row)


def build_message(
    sender: str,
    to_email: str,
    subject: str,
    body: str,
    resume_path: Path,
) -> MIMEMultipart:
    msg = MIMEMultipart()
    msg["From"] = formataddr((str(Header("求职投递", "utf-8")), sender))
    msg["To"] = to_email
    msg["Subject"] = Header(subject, "utf-8")
    msg.attach(MIMEText(body, "plain", "utf-8"))

    data = resume_path.read_bytes()
    filename = resume_path.name
    part = MIMEApplication(data, Name=filename)
    part.add_header("Content-Disposition", "attachment", filename=filename)
    msg.attach(part)
    return msg


def send_one(
    host: str,
    port: int,
    user: str,
    auth_code: str,
    to_email: str,
    subject: str,
    body: str,
    resume_path: Path,
) -> None:
    msg = build_message(user, to_email, subject, body, resume_path)
    with smtplib.SMTP_SSL(host, port, timeout=60) as smtp:
        smtp.login(user, auth_code)
        smtp.send_message(msg)


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Send resume PDF via SMTP (one-to-one)")
    p.add_argument("--env", type=Path, default=DEFAULT_ENV, help="Path to .env")
    p.add_argument("--emails", type=Path, default=DEFAULT_EMAILS, help="Email list file")
    p.add_argument(
        "--summary",
        type=Path,
        default=None,
        help="Company map CSV (companies.csv or 招聘汇总.csv)",
    )
    p.add_argument("--log", type=Path, default=DEFAULT_LOG, help="sent_log.csv path")
    p.add_argument(
        "--dry-run",
        action="store_true",
        help="Print recipients only; do not connect to SMTP",
    )
    p.add_argument(
        "--to-self",
        action="store_true",
        help="Send only one test email to SMTP_USER",
    )
    p.add_argument(
        "--to",
        metavar="EMAIL",
        help="Send only one test email to this address",
    )
    p.add_argument(
        "--limit",
        type=int,
        default=None,
        help="Override DAILY_LIMIT for this run (0 = no limit)",
    )
    return p.parse_args()


def main() -> int:
    args = parse_args()
    env = load_env(args.env)

    host = env.get("SMTP_HOST", "smtp.163.com").strip() or "smtp.163.com"
    port = int(env.get("SMTP_PORT", "465") or "465")
    subject = env.get("SUBJECT", "").strip() or "应聘-姓名-相关岗位"
    body = env.get("BODY", "").strip() or "您好，附件是我的简历，恳请查阅。"
    interval = int(env.get("SEND_INTERVAL", "40") or "40")
    daily_limit = int(env.get("DAILY_LIMIT", "25") or "25")
    if args.limit is not None:
        daily_limit = args.limit

    resume_raw = env.get("RESUME_PATH", "assets/resume.pdf").strip() or "assets/resume.pdf"
    resume_path = Path(resume_raw)
    if not resume_path.is_absolute():
        resume_path = ROOT / resume_path

    summary_path = resolve_summary(args.summary)
    company_map = load_company_map(summary_path)
    already_ok = load_sent_ok(args.log)

    user = env.get("SMTP_USER", "").strip()
    auth_code = env.get("SMTP_AUTH_CODE", "").strip()

    if args.to and args.to_self:
        raise SystemExit("Use only one of --to / --to-self")

    if args.to:
        queue = [args.to.strip()]
    elif args.to_self:
        if not user:
            raise SystemExit("SMTP_USER is required for --to-self")
        queue = [user]
    else:
        queue = [e for e in load_emails(args.emails) if e.lower() not in already_ok]

    if daily_limit > 0:
        queue = queue[:daily_limit]

    if not queue:
        print("Nothing to send (empty queue or all already logged as ok).")
        return 0

    print(f"Recipients this run: {len(queue)}")
    for i, email in enumerate(queue, 1):
        company = company_map.get(email.lower(), "")
        label = f"{email}" + (f" ({company})" if company else "")
        print(f"  {i}. {label}")

    if args.dry_run:
        print(f"Subject: {subject}")
        print(f"Resume: {resume_path} ({'found' if resume_path.is_file() else 'MISSING'})")
        print("Dry-run only; no email sent.")
        return 0

    if not user or not auth_code:
        raise SystemExit("SMTP_USER and SMTP_AUTH_CODE are required in .env for real sends")
    if "yourname@" in user or auth_code in PLACEHOLDER_AUTH:
        raise SystemExit("Please replace placeholder SMTP_USER / SMTP_AUTH_CODE in .env")
    if not resume_path.is_file():
        raise SystemExit(f"Resume PDF not found: {resume_path}")

    for i, email in enumerate(queue):
        company = company_map.get(email.lower(), "")
        stamp = time.strftime("%Y-%m-%d %H:%M:%S")
        try:
            send_one(host, port, user, auth_code, email, subject, body, resume_path)
            append_log(
                args.log,
                {
                    "time": stamp,
                    "email": email,
                    "company": company,
                    "result": "ok",
                    "detail": "",
                },
            )
            print(f"OK  {email}" + (f" | {company}" if company else ""))
        except Exception as exc:  # noqa: BLE001 — log any SMTP/IO failure per recipient
            detail = str(exc).replace("\n", " ")[:500]
            append_log(
                args.log,
                {
                    "time": stamp,
                    "email": email,
                    "company": company,
                    "result": "fail",
                    "detail": detail,
                },
            )
            print(f"FAIL {email}: {detail}", file=sys.stderr)

        if i < len(queue) - 1 and interval > 0:
            time.sleep(interval)

    print(f"Done. Log: {args.log}")
    return 0


if __name__ == "__main__":
    _configure_stdio()
    raise SystemExit(main())
