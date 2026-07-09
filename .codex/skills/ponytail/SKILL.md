---
name: ponytail
description: Propose and apply the smallest, lazily correct change to Scrape-n-Email. Reuse stdlib and existing helpers before adding dependencies or abstractions. Use for focused bug fixes, parser tweaks, mailer adjustments, and any task where scope creep is the main risk.
---

# Ponytail

Read `AGENTS.md` and `CLAUDE.md` first.

Use the lazily correct solution:

- Ask whether the change needs to exist at all.
- Reuse existing helpers first:
  - HTTP: `scrape_n_email.scrapers.base.get()` / `get_session()`.
  - CSV: `scrape_n_email.csv.append_row()`, `append_rows()`, `init_csv()`.
  - Logging: `logging.getLogger("scrape_n_email.<module>")`, never `print()`.
  - Config: `scrape_n_email.config.Config`.
- Avoid new dependencies. Runtime pins are `requests`, `beautifulsoup4`, and `lxml`.
- Avoid broad abstractions. Three explicit lines beat a premature helper.
- Keep the diff as small as possible. Do not reformat adjacent code or rename unrelated symbols.
- Preserve generated-file contracts: `RCPheadlines.txt`, `jobs.txt`, `DRUDGEheadlines.txt`, and `RCPlinks.csv`.

If the task is non-trivial, prefer the smallest working change and mark any deliberate simplification with a `ponytail:` comment.

## Fill In

- Goal:
- Files:
- Constraints:
- Tests:

## Verify Before Declaring Done

```bash
ruff check src/ tests/
ruff format --check src/ tests/
mypy src/scrape_n_email
pytest tests/ -q
```
