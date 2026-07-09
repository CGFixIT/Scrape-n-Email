# Contributing to Scrape-n-Email

This repo is still a small personal automation tool, not a generic scraping platform. Keep changes tight, readable, and easy to verify.

## Prerequisites

- Python 3.10+
- Git

## Setup

```bash
git clone https://github.com/CGFixIT/Scrape-n-Email.git
cd Scrape-n-Email
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -e ".[dev]"
```

## Environment Variables

For live email runs:

- `EMAIL_USER`
- `EMAIL_PASS`
- optional `EMAIL_RECIPIENT`

Never commit secrets, `.env` files, or machine-specific scheduler paths.

## Project Shape

- `src/scrape_n_email/` contains the real package.
- `tests/unit/` contains most focused coverage.
- `tests/integration/test_pipeline.py` covers the offline end-to-end path.
- `main.py` is a compatibility shim, not the preferred entrypoint.

## Running the App

Preferred:

```bash
python -m scrape_n_email
```

Offline-friendly scrape-only path:

```bash
python -m scrape_n_email --skip-email
```

## Validation

Run the full local gate before opening a PR for behavior changes:

```bash
ruff check src/ tests/
ruff format --check src/ tests/
mypy src/scrape_n_email
pytest tests/ --cov=scrape_n_email --cov-report=term-missing --cov-fail-under=80
```

Narrow checks are fine while iterating, but do not stop there for behavior changes:

```bash
pytest tests/unit/test_scrapers.py -q
pytest tests/integration/test_pipeline.py -q
```

## Contribution Rules

- Keep parser functions pure where practical so they stay easy to test offline.
- Reuse `scrape_n_email.scrapers.base.get()` for HTTP behavior.
- Reuse `scrape_n_email.csv` helpers for CSV writes.
- Do not remove spreadsheet-formula escaping.
- Use `logging`, not `print()`, in library code.
- Do not add new dependencies for convenience.
- Do not add live-network or real-SMTP tests to normal CI.

## What To Include In A PR

1. A small, clearly scoped change.
2. Updated tests when parser, config, CSV, CLI, or mailer behavior changed.
3. The validation commands you actually ran.
4. Any manual verification notes, clearly labeled as manual.

## Good Changes

- Parser fixes for source HTML drift.
- Better offline coverage for edge cases.
- Small reliability improvements in config, retry, CSV, or mailer logic.
- Documentation fixes that match the actual repo behavior.

## Bad Changes

- Turning this into a broad scraping framework.
- Introducing new dependencies without a real payoff.
- Committing generated outputs, credentials, or local scratch files.
- Shipping parser changes without updating the matching tests.

## Agent Files

If you touch repo-local AI scaffolding, keep these aligned:

- `AGENTS.md`
- `.codex/`
- `commands/`
- `.claude/`
- `CLAUDE.md`

Codex command files belong in `commands/*.toml`. Reusable Codex skill entrypoints belong in `.codex/skills/`.

## Reporting Issues

Useful bug reports include:

- Python version
- OS
- exact error text
- repro steps
- for scraper bugs, a small HTML snippet or clear description of the site change

## License

By contributing, you agree that your contributions are licensed under the MIT License used by this repository.
