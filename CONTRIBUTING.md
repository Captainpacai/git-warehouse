# Contributing

Thanks for contributing.

## Rules

1. Do not commit secrets: `.env`, auth codes, resumes, or real HR contact lists.
2. Keep the sender stdlib-only unless there is a strong reason otherwise.
3. Prefer small PRs: one fix or feature per PR.
4. Update `.env.example` and README when adding config knobs.
5. Match existing code style in `send_resume.py`.

## Dev check

```bash
cp .env.example .env
cp emails.example.txt emails.txt
python send_resume.py --dry-run
```

## Skill changes

If you change the agent workflow, update:

- `.cursor/skills/campus-resume-mailer/SKILL.md`
- `.cursor/skills/campus-resume-mailer/reference.md`
