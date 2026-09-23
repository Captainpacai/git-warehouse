# campus-resume-mailer

用个人邮箱 SMTP（默认 163）**一对一**发送简历 PDF：限速、可预览、写发送日志、自动跳过已成功地址。

> 仅供本人求职投递使用。请遵守邮箱服务商政策与当地反垃圾邮件规范，勿骚扰收件人。

## Features

- Python 标准库，无第三方依赖
- `.env` 配置 SMTP / 主题 / 正文 / 简历路径
- `--dry-run` / `--to` / `--to-self` / `--limit`
- `sent_log.csv` 去重
- 可选公司表标注日志中的企业名
- Cursor Skill：`.cursor/skills/campus-resume-mailer/`

## Quick start

```bash
git clone <your-repo-url>
cd campus-resume-mailer   # or this folder name

cp .env.example .env
cp emails.example.txt emails.txt
# optional:
cp companies.example.csv companies.csv

# put your resume at assets/resume.pdf (or set RESUME_PATH)
python send_resume.py --dry-run
python send_resume.py --to you@example.com
python send_resume.py --limit 5
```

Edit `.env`:

| Key | Meaning |
|-----|---------|
| `SMTP_HOST` / `SMTP_PORT` | e.g. `smtp.163.com` / `465` |
| `SMTP_USER` | your mailbox |
| `SMTP_AUTH_CODE` | provider auth code (not login password) |
| `RESUME_PATH` | path to PDF |
| `SUBJECT` / `BODY` | message |
| `SEND_INTERVAL` | seconds between sends |
| `DAILY_LIMIT` | max recipients per run (`0` = unlimited) |

## Suggested daily volume

| Stage | / day |
|-------|------:|
| First days | 15–25 |
| Stable | 25–40 |

## Project layout

```text
send_resume.py              # main script
.env.example                # config template
emails.example.txt          # sample roster
companies.example.csv       # sample company map
assets/.gitkeep
.cursor/skills/campus-resume-mailer/
LICENSE
CONTRIBUTING.md
```

Local-only (gitignored): `.env`, `emails.txt`, `companies.csv`, `招聘汇总.*`, `sent_log.csv`, `assets/*.pdf`

## Cursor Skill

Project skill path:

`.cursor/skills/campus-resume-mailer/SKILL.md`

Ask the agent to follow **campus-resume-mailer** when configuring or batch-sending resumes.

## License

MIT — see [LICENSE](LICENSE).
