# Scrape-n-Email

A small, dependency-light news + jobs scraper that emails its results as attachments. Originally a Python + Windows batch hybrid that depended on a 2009-era `sendEmail.exe` binary; rewritten end-to-end in pure Python with environment-based credentials and proper SMTP-over-TLS.

![Email sample showing Craigslist jobs and RealClearPolitics headlines delivered as attachments](https://cgfixit.com/img/scrapeNemail.png)

![RealClearPolitics headlines exported to CSV, opened in Excel](https://cgfixit.com/img/scrapeNemail2.png)

-----

## What it does

Three scraper modules feed one orchestrator and one mailer:

```
main.py
  ├── rcpScraper.scrape()           → RCPheadlines.txt
  │     └── drudgeScraper.writer()  → RCPlinks.csv  (called per-headline)
  ├── clistScraper.scrape()         → jobs.txt
  └── mailer.send_all()
        ├── Email 1: "Daily News: <date>" → RCPheadlines.txt + RCPlinks.csv
        └── Email 2: "Daily Jobs: <date>" → jobs.txt
```

- `rcpScraper` pulls top headlines from RealClearPolitics and writes a flat `.txt` digest plus a parallel `.csv` (headline + URL columns).
- `clistScraper` pulls Atlanta Craigslist sysadmin job listings into a `.txt` digest.
- `mailer` sends two separate emails via Gmail SMTP — one for news, one for jobs — with the corresponding files attached. Date-stamped subject lines.

> **About the `drudgeScraper` module name:** the project started as a Drudge Report scraper, then pivoted to RCP, and the module was never renamed. The CSV-writing helpers `csvinit()` and `writer()` live there for historical reasons — `rcpScraper.py` calls `drudgeScraper.writer()` per headline to populate `RCPlinks.csv`. On the to-do list to clean up.

-----

## Setup

**Requirements:** Python 3.6+, `requests`, `beautifulsoup4`. Everything else (`smtplib`, `ssl`, `email.message`, `mimetypes`, `csv`) is stdlib.

```bash
pip install requests beautifulsoup4
```

**Credentials** are read from environment variables — nothing is hardcoded in the repo:

|Variable         |Purpose                                                                                                       |
|-----------------|--------------------------------------------------------------------------------------------------------------|
|`EMAIL_USER`     |Gmail address to send from                                                                                    |
|`EMAIL_PASS`     |Gmail [App Password](https://myaccount.google.com/apppasswords) — 16-char token, **not** your regular password|
|`EMAIL_RECIPIENT`|*(Optional)* destination address; defaults to `EMAIL_USER` if unset                                           |

**Running it:**

```bash
# one-off
python main.py

# scheduled (Windows): edit init.bat to point at your folder, then schedule it
schtasks /Create /SC DAILY /TN "ScrapeNEmail" /TR "C:\path\to\init.bat" /ST 07:00
```

-----

## Why the rewrite — security context

The previous version invoked `sendEmail.exe` (v1.56, Brandon Zehm, 2009) through `email.bat`. It worked, but the design had real problems for anything beyond a personal toy:

|Old design                                    |Issue                                                                                                                                         |New design                                                                                                                |
|----------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------|
|Unsigned 2009-era `.exe` shipped in repo      |DLL search-order risk; ~16-year-old binary with no recent security review                                                                     |Removed. Pure stdlib `smtplib`.                                                                                           |
|TLS handled inside the binary’s bundled libs  |No guarantee modern cipher suites / TLS 1.2+ are actually negotiated                                                                          |`ssl.create_default_context()` — uses the OS’s modern trust store and cipher prefs. Explicit `STARTTLS` on port 587.      |
|Credentials hardcoded in `email.bat`          |Anyone with read access to the repo or a backup leaks the password                                                                            |`os.environ.get()` for `EMAIL_USER` / `EMAIL_PASS` — credentials never touch this repo.                                   |
|Plain Gmail password                          |Doesn’t work post-2022 anyway (Gmail killed less-secure-app access); even when it did, this was full-account creds for a single-purpose script|Gmail **App Passwords** — scoped, revocable per-token.                                                                    |
|No error handling                             |Silent failures; the `.bat` exited via `errorlevel` but the Python wrapper didn’t check                                                       |Typed exception handling for `SMTPAuthenticationError`, `SMTPException`, and `OSError`; per-email success/failure logging.|
|Generic `application/octet-stream` attachments|Some clients won’t render `.csv` previews correctly                                                                                           |`mimetypes.guess_type()` per attachment yields correct `text/csv` and `text/plain` MIME parts.                            |

The full migration plan lives in `python_mailer_todo-DONE.txt`.

-----

## Known Issues

- **Scrapers are currently broken.** RCP and Craigslist both changed their page structure (class names / DOM layout) since this was last working. Selectors need updating. The mailer is independent of the scrapers and works correctly — point it at any pair of files and it will deliver them.
- **No `User-Agent` header** on outbound `requests.get()` calls. Sites increasingly fingerprint or 403 the default `python-requests/x.y.z` UA, and may serve different (or no) HTML to it. This may be contributing to the broken-selector symptom above. One-line fix per scraper: pass `headers={"User-Agent": "Mozilla/5.0 ..."}` to `requests.get()`.
- **Inconsistent file modes.** `clistScraper.py` opens `jobs.txt` in append mode (`'a'`) while `rcpScraper.py` uses truncate (`'w+'`) on `RCPheadlines.txt`. `jobs.txt` therefore accumulates indefinitely across runs. Both should use `'w'` for current-run-only output.
- **Craigslist URL construction bug** in `clistScraper.py`: builds `domain + job.attrs['href']` where `domain = "http://craigslist.com/"`. Craigslist hrefs are already absolute, so the result is a mangled `http://craigslist.com/https://atlanta.craigslist.org/...`. Use `job.attrs['href']` directly.
- **`RCPlinks.csv` has no header initialization on the runtime path.** `csvinit()` exists in `drudgeScraper.py` but is only called when that module runs as `__main__`. From the `main.py` entry point, the CSV gets appended to without a header row, and (because it’s opened in `'a'` mode) it accumulates across runs. Either call `csvinit()` from `main.main()` or switch the writer to `'w'` mode and write the header on each run.

-----

## Roadmap

- Update scrapers’ selectors against current RCP / Craigslist HTML; add browser-like User-Agent.
- Optionally migrate the scraping layer from `requests` + `bs4` to `httpx` + `selectolax` for speed and `async` support.
- Add a config file (`config.toml`) for SMTP host / port so the mailer is provider-agnostic — currently Gmail-specific.
- Replace `print()` calls with structured logging (`logging` module + a rotating file handler).

-----

## Closing note

The 3 web scrapers are the modules most prone to bit-rot or link rotover time as websites change — they’re tied to whatever HTML the upstream site happens to be serving today. The architecture itself (scrape → write to flat file → email attachments via STARTTLS SMTP with env-based creds) **is generic and reusable**: swap the BeautifulSoup HTML selectors (or the entire scraper module) for the desired URL to extract from, and the same mailer pipeline will deliver any HTML-extracted dataset to your inbox. it currently does send a .csv too but should silently fail and still send if only .txt files or missing attachment - This is both by design and something to be aware of

-----

*Christopher Grady · [cgfixit.com](https://cgfixit.com) · [github.com/CGFixIT](https://github.com/CGFixIT)*
