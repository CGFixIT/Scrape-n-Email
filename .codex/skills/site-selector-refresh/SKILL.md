---
name: site-selector-refresh
description: Repair a scraper when RealClearPolitics, Craigslist, or Drudge changes HTML. Use for selector drift, fallback logic updates, and the matching offline test refresh.
---

# Site Selector Refresh

Read `AGENTS.md` first, then the target scraper in `src/scrape_n_email/scrapers/` and the matching coverage in `tests/unit/test_scrapers.py`.

Use this skill when a source site changed markup and the parser needs a tight refresh.

## Target Files

- `src/scrape_n_email/scrapers/rcp.py`
- `src/scrape_n_email/scrapers/clist.py`
- `src/scrape_n_email/scrapers/drudge.py`
- `tests/unit/test_scrapers.py`

## Bias

- Prefer a small selector-order or fallback tweak over a rewrite.
- Change the shared parse function, not just one caller.
- Keep parser logic pure and offline-testable.
- Use `BeautifulSoup` patterns already in the repo before adding helpers.
- Preserve output shape unless the task explicitly changes it.

## Workflow

1. Identify which parser failed and why.
2. Update the minimum selector or fallback logic needed.
3. Add or update the smallest representative HTML snippet/assertion in `tests/unit/test_scrapers.py`.
4. If live HTML was captured manually, reduce it to the minimum fixture needed for the regression.
5. Do not add live-network tests.

## Verify Before Declaring Done

```bash
ruff check src/ tests/
ruff format --check src/ tests/
pytest tests/unit/test_scrapers.py -q
```
