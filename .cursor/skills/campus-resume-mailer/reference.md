# Campus Resume Mailer — Reference

## 163 setup

1. mail.163.com → Settings → POP3/SMTP/IMAP
2. Enable **IMAP/SMTP** (enough for sending; POP3 optional)
3. Open **授权密码管理** → add authorization password → copy once
4. Put the code in `.env` as `SMTP_AUTH_CODE`

The IMAP toggle page does **not** show the code string. Codes appear only when created.

## File roles

| File | Tracked in git? | Role |
|------|-----------------|------|
| `send_resume.py` | yes | Sender |
| `.env.example` | yes | Template |
| `.env` | no | Secrets |
| `emails.txt` | no | Real roster |
| `emails.example.txt` | yes | Sample roster |
| `companies.csv` / `招聘汇总.csv` | no | Optional company map |
| `companies.example.csv` | yes | Sample map |
| `sent_log.csv` | no | Send results |
| `assets/*.pdf` | no | Resume |

## CSV columns

Script accepts either language:

- Company: `企业` or `company`
- Email: `邮箱` or `email`

## Common failures

| Symptom | Likely cause |
|---------|----------------|
| placeholder SMTP_USER | Still editing `.env.example` or unsaved `.env` |
| Resume MISSING | Filename ≠ `RESUME_PATH` |
| Auth / login error | Wrong auth code; regenerate |
| Rate limit | Lower `DAILY_LIMIT`, raise `SEND_INTERVAL` |

## Open-source hygiene

Before pushing to GitHub: ensure real `emails.txt`, summaries, resumes, and `.env` are gitignored and never committed. If they were committed earlier, rewrite history or rotate auth codes.
