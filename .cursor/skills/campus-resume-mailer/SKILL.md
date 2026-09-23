---
name: campus-resume-mailer
description: >-
  Sets up and runs one-to-one campus/job resume email outreach via personal SMTP
  (163/QQ/Gmail), with dry-run, test sends, rate limits, and sent_log dedupe.
  Use when the user wants to batch-send a resume PDF to HR emails, configure
  .env SMTP, parse job-fair markdown into email lists, or operate send_resume.py.
---

# Campus Resume Mailer

Help the user send a resume PDF one-to-one through their own mailbox. Prefer this
repo's `send_resume.py` over writing a new script.

## Non-negotiables

- Never commit `.env`, auth codes, resumes, or real HR contact lists
- Never BCC / mass-blast; always one `To` per message
- Never paste real `SMTP_AUTH_CODE` into chat; edit `.env` locally only
- Default daily cap ~15–25 on day one; interval ≥30–40s (163 is strict)

## Workflow

Copy and track:

```
Progress:
- [ ] SMTP auth code ready (163: 授权密码 / 客户端授权密码)
- [ ] Resume PDF path correct
- [ ] .env filled (HOST/PORT/USER/AUTH/SUBJECT/BODY/RESUME_PATH)
- [ ] emails.txt ready (or companies.csv)
- [ ] dry-run OK
- [ ] test send (--to or --to-self) OK
- [ ] small batch (--limit N)
```

### 1. Configure

```bash
cp .env.example .env
```

Defaults for 163: `SMTP_HOST=smtp.163.com`, `SMTP_PORT=465`.  
QQ Mail: `smtp.qq.com:465`. Gmail: app password + `smtp.gmail.com:465`.

`SMTP_AUTH_CODE` is the provider **authorization code**, not the web login password.

### 2. Roster

- `emails.txt` — one address per line
- Optional `companies.csv` / `招聘汇总.csv` — columns `企业`/`company` + `邮箱`/`email` for log labels
- Companies without email → phone follow-up list only; do not invent addresses

### 3. Commands

```bash
python send_resume.py --dry-run
python send_resume.py --to friend@example.com
python send_resume.py --to-self
python send_resume.py --limit 5
python send_resume.py
```

Successful rows in `sent_log.csv` are skipped on later runs.

### 4. Agent duties

When implementing or debugging:

1. Read `.env.example` and `send_resume.py` before changing behavior
2. Fix `RESUME_PATH` to the real PDF filename under `assets/`
3. If auth fails: confirm IMAP/SMTP enabled + auth code regenerated once
4. Prefer `--to` test address over flooding `emails.txt`
5. After batches, summarize OK/FAIL from terminal or `sent_log.csv`

## Daily volume guidance

| Stage | Suggested / day |
|-------|-----------------|
| First 1–2 days | 15–25 |
| Stable | 25–40 |
| Avoid | 100+ |

## More detail

- Provider setup notes: [reference.md](reference.md)
