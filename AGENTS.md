# AGENTS.md

Guidance for Codex and other AI coding agents working in Scrape-n-Email.

Canonical references:

- `README.md` for project overview, runtime modes, scheduler notes, and deployment caveats.
- `CONTRIBUTING.md` for contributor workflow and PR expectations.
- `pyproject.toml` for packaging metadata, dependency ranges, ruff, mypy, and pytest config.
- `.github/workflows/ci.yml` for the exact CI validation contract.
- `CLAUDE.md` for Claude-specific mirrors of the same repo guidance.
- `.codex/README.md` for Codex routines, checklists, skills, and command registration.
- `.codex/skills/` for Codex skill entrypoints.
- `commands/` for repo-local Codex slash commands.
- `.claude/` for Claude Code commands and skill mirrors that should stay aligned with the Codex equivalents.

## Project Overview

Scrape-n-Email is a small Python automation that scrapes RealClearPolitics headlines, Atlanta Craigslist sysadmin/networking jobs, and a standalone Drudge source, writes digest files, and emails attachments through Gmail SMTP. The current repo has been modernized into a `src/` package with offline tests, linting, type checking, and Docker support.

Keep changes small. This is still a personal scheduled automation, not a generic scraping framework.

## Current Repository Layout

- `src/scrape_n_email/` - installable package.
- `src/scrape_n_email/cli.py` - main orchestration entrypoint.
- `src/scrape_n_email/config.py` - env-driven `Config` dataclass.
- `src/scrape_n_email/csv.py` - CSV initialization, append helpers, and formula-injection escaping.
- `src/scrape_n_email/mailer.py` - Gmail SMTP sending with logging and retry handling.
- `src/scrape_n_email/scrapers/base.py` - shared `requests.Session`, headers, and retry loop.
- `src/scrape_n_email/scrapers/rcp.py` - RealClearPolitics scrape and parse flow.
- `src/scrape_n_email/scrapers/clist.py` - Craigslist scrape and parse flow.
- `src/scrape_n_email/scrapers/drudge.py` - standalone Drudge scrape and parse flow.
- `tests/unit/` - parser, CSV, config, mailer, CLI, and retry-path tests.
- `tests/integration/` - end-to-end offline pipeline coverage.
- `main.py` - legacy shim for existing scheduled invocations.
- `Dockerfile` - single-run container image that writes outputs under `/data`.
- `.codex/` - Codex routines, checklists, and skills.
- `.claude/` - Claude Code mirrors of commands and skills.

Generated runtime files: `jobs.txt`, `RCPheadlines.txt`, `DRUDGEheadlines.txt`, `RCPlinks.csv`.

## Tech Stack Detected

- Language/runtime: Python 3.10+.
- Runtime dependencies: `requests`, `beautifulsoup4`, `lxml`.
- Dev tooling: `pytest`, `pytest-cov`, `ruff`, `mypy`, `types-requests`, `python-dotenv`.
- Packaging/build: `pyproject.toml` with Hatchling.
- CI: GitHub Actions in `.github/workflows/ci.yml`.
- Container path: `Dockerfile`.

## Setup Commands

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -e ".[dev]"
```

## Run Commands

Preferred package entrypoint:

```bash
python -m scrape_n_email
python -m scrape_n_email --skip-email
```

Legacy compatibility path:

```bash
python main.py
```

Windows scheduled-run pattern:

```cmd
schtasks /Create /SC DAILY /TN "ScrapeNEmail" /TR "C:\path\to\python.exe -m scrape_n_email" /ST 07:00
```

## Validation Commands

Use the CI-equivalent stack unless the task is docs-only:

```bash
ruff check src/ tests/
ruff format --check src/ tests/
mypy src/scrape_n_email
pytest tests/ --cov=scrape_n_email --cov-report=term-missing --cov-fail-under=80
```

For narrow parser work, run the smallest relevant slice first, then widen if needed:

```bash
pytest tests/unit/test_scrapers.py -q
pytest tests/integration/test_pipeline.py -q
```

## Codex Skills And Commands Map

Codex skills:

- `.codex/skills/ponytail/SKILL.md` - smallest safe diff, stdlib-first, no scope creep.
- `.codex/skills/optimize/SKILL.md` - bounded hotspot cleanup with measurable improvement.
- `.codex/skills/site-selector-refresh/SKILL.md` - repair parser selectors and fixtures when a source site changes HTML.
- `.codex/skills/daily-run-check/SKILL.md` - verify scrape -> file -> email behavior with the narrowest offline checks.

Codex commands:

- `commands/ponytail.toml` - quick invoke for minimal-diff work.
- `commands/optimize.toml` - quick invoke for focused cleanup/perf work.
- `commands/selector-refresh.toml` - quick invoke for source HTML drift fixes.
- `commands/daily-run-check.toml` - quick invoke for pipeline verification.

Claude mirrors:

- `.claude/skills/` and `.claude/commands/` should stay semantically aligned with the Codex versions.

## Safe Development Workflow

1. Read `README.md`, `pyproject.toml`, `.github/workflows/ci.yml`, and this file.
2. Keep the diff tight and repo-specific.
3. If you touch parser logic, update the corresponding offline tests in `tests/unit/test_scrapers.py`.
4. If you touch mail delivery or config validation, keep SMTP mocked and env-driven.
5. If you touch `pyproject.toml`, `.github/workflows/ci.yml`, or package imports, run the full validation stack.
6. Report live-site behavior as unverified unless you actually hit the real site.

## House Rules For Code Changes

- Reuse `scrape_n_email.scrapers.base.get()` and `get_session()` for HTTP.
- Reuse `scrape_n_email.config.Config` for env-derived settings.
- Reuse `scrape_n_email.csv.init_csv()`, `append_row()`, and `append_rows()` for CSV writes.
- Preserve CSV formula-injection escaping.
- Use `logging`, not `print()`, in library code.
- Prefer selector or fallback updates in existing parsers over broad rewrites.
- Keep generated-file contracts stable unless the task explicitly changes them.
- Do not add dependencies for convenience.

## Testing Expectations

- Tests must stay offline for normal CI.
- Parser fixes should come with a representative HTML snippet or updated assertion in `tests/unit/test_scrapers.py`.
- Mailer tests must mock `smtplib.SMTP`.
- Use temp paths or monkeypatches for generated files instead of committed runtime artifacts.
- Keep coverage at or above the CI gate of 80%.

## Security And Secrets Rules

- Never commit Gmail credentials, app passwords, `.env` files, or machine-specific scheduler paths.
- Required env vars for live email:
  - `EMAIL_USER`
  - `EMAIL_PASS`
  - optional `EMAIL_RECIPIENT`
- Optional env vars include `SMTP_HOST`, `SMTP_PORT`, `MAX_RCP_ITEMS`, `MAX_CLIST_ITEMS`, `MAX_DRUDGE_ITEMS`, `RCP_URL`, `CLIST_URL`, and `DRUDGE_URL`.
- Treat scraped site content as untrusted input.
- Do not run live SMTP sends unless the maintainer explicitly asks.

## Known Gotchas

- Live scraping can break when RealClearPolitics, Craigslist, or Drudge changes HTML.
- The fix is usually a small selector/fallback update plus an offline test refresh, not a pipeline rewrite.
- `drudge.py` is still a supported standalone path even though the main daily flow is RCP + Craigslist.
- `main.py` exists for backwards compatibility; the package entrypoint is the preferred path.
- Output files are runtime artifacts and must not be committed.
