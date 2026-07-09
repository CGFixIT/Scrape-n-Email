# Scrape-n-Email

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![CI](https://github.com/CGFixIT/Scrape-n-Email/actions/workflows/ci.yml/badge.svg)](https://github.com/CGFixIT/Scrape-n-Email/actions/workflows/ci.yml)

Small Python automation that scrapes RealClearPolitics headlines and Atlanta Craigslist sysadmin/networking jobs, writes digest files, and emails them through Gmail SMTP.

The repo now uses a `src/` package layout, offline tests, linting, type checking, and a small CI matrix. It is still intentionally small and dependency-light.

## What It Does

Default daily flow:

1. Scrape RealClearPolitics headlines.
2. Scrape Atlanta Craigslist job listings.
3. Write digest artifacts.
4. Email the digests as attachments.

Generated runtime files:

- `RCPheadlines.txt`
- `jobs.txt`
- `RCPlinks.csv`

There is also a standalone Drudge parser in `src/scrape_n_email/scrapers/drudge.py`, but it is not part of the default daily pipeline.

## Current Layout

- `src/scrape_n_email/cli.py` - main CLI entrypoint and orchestration.
- `src/scrape_n_email/config.py` - env-driven config dataclass and validation.
- `src/scrape_n_email/csv.py` - CSV initialization, append helpers, and spreadsheet-formula escaping.
- `src/scrape_n_email/mailer.py` - Gmail SMTP sending and logging.
- `src/scrape_n_email/scrapers/base.py` - shared HTTP session, headers, and retry loop.
- `src/scrape_n_email/scrapers/rcp.py` - RealClearPolitics scrape + parse flow.
- `src/scrape_n_email/scrapers/clist.py` - Craigslist scrape + parse flow.
- `src/scrape_n_email/scrapers/drudge.py` - standalone Drudge scrape + parse flow.
- `tests/unit/` - parser, config, CSV, mailer, CLI, and retry-path coverage.
- `tests/integration/` - offline pipeline coverage.
- `main.py` - compatibility shim for older scheduled invocations.
- `pyproject.toml` - packaging, dependencies, ruff, mypy, and pytest config.
- `Dockerfile` - single-run container image.
- `AGENTS.md`, `.codex/`, `.claude/`, `commands/` - repo-local AI agent guidance and command wiring.

## Requirements

- Python 3.10+
- Runtime dependencies are declared in `pyproject.toml` and mirrored in `requirements.txt`

## Setup

Runtime install:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Contributor/dev install:

```bash
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

Required for live email sends:

- `EMAIL_USER` - Gmail address used to send mail
- `EMAIL_PASS` - Gmail app password

Optional:

- `EMAIL_RECIPIENT` - defaults to `EMAIL_USER`
- `SMTP_HOST` - defaults to `smtp.gmail.com`
- `SMTP_PORT` - defaults to `587`
- `MAX_RCP_ITEMS`
- `MAX_CLIST_ITEMS`
- `MAX_DRUDGE_ITEMS`
- `RCP_URL`
- `CLIST_URL`
- `DRUDGE_URL`

Never commit real credentials or `.env` files.

## Running It

Preferred:

```bash
python -m scrape_n_email
```

Scrape only, skip SMTP:

```bash
python -m scrape_n_email --skip-email
```

Legacy compatibility path:

```bash
python main.py
```

Windows scheduled task example:

```cmd
schtasks /Create /SC DAILY /TN "ScrapeNEmail" /TR "C:\path\to\python.exe -m scrape_n_email" /ST 07:00
```

## Validation

CI is the source of truth. Local validation commands:

```bash
ruff check src/ tests/
ruff format --check src/ tests/
mypy src/scrape_n_email
pytest tests/ --cov=scrape_n_email --cov-report=term-missing --cov-fail-under=80
```

Useful narrow checks:

```bash
pytest tests/unit/test_scrapers.py -q
pytest tests/integration/test_pipeline.py -q
```

All tests are intended to run offline. Do not rely on live websites or real SMTP in ordinary validation.

## Docker

Build:

```bash
docker build -t scrape-n-email .
```

Run:

```bash
docker run --rm \
  -e EMAIL_USER=you@gmail.com \
  -e EMAIL_PASS=app-password \
  -v $(pwd)/output:/data \
  scrape-n-email
```

The container writes output files under `/data`.

## Agent Setup

Repo-local agent guidance lives here:

- `AGENTS.md` - shared project rules for coding agents
- `.codex/` - Codex routines, skills, and checklists
- `commands/` - runnable Codex slash commands
- `.claude/` and `CLAUDE.md` - Claude Code mirrors

If you are updating agent scaffolding, keep Claude and Codex mirrors aligned and prefer adding only missing pieces over inventing new workflow.

## Known Caveats

- Live scraping can break when RealClearPolitics, Craigslist, or Drudge changes HTML.
- The right fix is usually a small parser selector update plus an offline test refresh.
- `RCPlinks.csv` is append-oriented by design and will grow over time.
- Gmail requires an app password, not the account password.
- Generated output files are runtime artifacts and should not be committed.

## License

MIT. See [LICENSE.md](LICENSE.md).
