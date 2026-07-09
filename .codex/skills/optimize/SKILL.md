---
name: optimize
description: Tighten a Scrape-n-Email hotspot or piece of bloat with a small, measurable improvement. Prefer deletion, reuse, and stdlib over new abstractions. Use for known parser, CSV, SMTP, HTTP-session, or test-suite hotspots.
---

# Optimize

Read `AGENTS.md` and `CLAUDE.md` first.

Optimize this Scrape-n-Email change or hotspot. Keep scope tight.

## Fill In

- Goal:
- Current behavior:
- Bottleneck or bloat:
- Constraints:
- Tests:

## Bias

- Prefer deletion over addition.
- Prefer stdlib and existing helpers over new dependencies.
- Prefer one measurable improvement over a sweep of stylistic edits.
- Reuse the shared HTTP session instead of opening a new `requests.Session()` per call.
- Batch CSV writes through `scrape_n_email.csv` instead of reopening `RCPlinks.csv` per row.
- Do not trade clarity for micro-gains in cold code paths.

## State Explicitly

- What changed and why.
- What was not changed and why.
- How the improvement was measured, even if the number is rough.

## Verify Before Declaring Done

```bash
ruff check src/ tests/
ruff format --check src/ tests/
mypy src/scrape_n_email
pytest tests/ --cov=scrape_n_email --cov-report=term-missing --cov-fail-under=80
```
