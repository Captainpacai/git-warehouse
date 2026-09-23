# Security Policy

## Secrets

Never publish:

- `.env` / SMTP authorization codes
- Personal resumes under `assets/`
- Real `emails.txt` or company contact CSVs

If a secret was pushed by mistake: revoke the mailbox authorization code immediately, then remove it from git history before the next force-push (only on branches you control).

## Responsible use

This tool is for personal job applications. Do not use it to spam, scrape, or harass recipients.
