---
name: daily-run-check
description: Verify the daily scrape, file-output, and email pipeline after a change. Use for end-to-end offline checks, scheduler-safe behavior, and generated-file contract verification.
---

# Daily Run Check

Read `AGENTS.md` first, then inspect the touched path in `src/scrape_n_email/` and the matching tests.

Use this skill when the goal is to confirm the daily automation still works after a code or site-change fix.

## Bias

- Prefer the narrowest offline validation that covers the touched code.
- Use `python -m scrape_n_email --skip-email` or mocks before anything live.
- Keep generated outputs in temp paths or disposable directories.
- Do not send real SMTP traffic unless the maintainer explicitly asks.

## Common Checks

- CLI flow: `src/scrape_n_email/cli.py`
- Config/env validation: `src/scrape_n_email/config.py`
- Generated files: `src/scrape_n_email/csv.py`, scraper modules
- Email path: `src/scrape_n_email/mailer.py`
- End-to-end coverage: `tests/integration/test_pipeline.py`

## Verify Before Declaring Done

```bash
ruff check src/ tests/
ruff format --check src/ tests/
mypy src/scrape_n_email
pytest tests/integration/test_pipeline.py -q
pytest tests/unit/test_cli.py tests/unit/test_mailer.py -q
```
