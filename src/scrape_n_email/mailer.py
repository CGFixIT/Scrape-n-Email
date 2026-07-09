"""SMTP mailer with retry logic and structured logging."""

from __future__ import annotations

import logging
import smtplib
import ssl
import time
from collections.abc import Sequence
from datetime import date
from email.message import EmailMessage
from pathlib import Path

from scrape_n_email.config import Config

logger = logging.getLogger("scrape_n_email.mailer")

_MAX_RETRIES = 3
_RETRY_DELAY_BASE = 2
_PERMANENT_SMTP_CODES = {535, 530, 534, 538}


def _is_transient_smtp_error(exc: smtplib.SMTPException) -> bool:
    """Return True if the SMTP error is transient."""
    if isinstance(exc, smtplib.SMTPAuthenticationError):
        return False
    return not (hasattr(exc, "smtp_code") and exc.smtp_code in _PERMANENT_SMTP_CODES)


def _attach_file(msg: EmailMessage, filepath: Path | str) -> bool:
    """Attach a file to the email message if it exists."""
    import mimetypes

    path = Path(filepath)
    if not path.is_file():
        logger.warning("Attachment not found, skipping: %s", path)
        return False

    mime_type, _ = mimetypes.guess_type(str(path))
    maintype, subtype = (mime_type or "application/octet-stream").split("/", 1)

    try:
        data = path.read_bytes()
    except OSError as e:
        logger.warning("Could not read attachment '%s': %s", path, e)
        return False

    msg.add_attachment(data, maintype=maintype, subtype=subtype, filename=path.name)
    return True


def send_email(subject: str, body: str, attachments: Sequence[Path | str]) -> bool:
    """Send a single email with retry logic for transient failures."""
    try:
        config = Config.from_env()
        config.validate()
    except ValueError as e:
        logger.error("Configuration error: %s", e)
        return False

    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = config.email_user
    msg["To"] = config.email_recipient
    msg.set_content(body)

    for filepath in attachments:
        _attach_file(msg, filepath)

    context = ssl.create_default_context()

    for attempt in range(1, _MAX_RETRIES + 1):
        try:
            with smtplib.SMTP(config.smtp_host, config.smtp_port, timeout=30) as server:
                server.starttls(context=context)
                server.login(config.email_user, config.email_pass)
                server.send_message(msg)
            logger.info("Sent: %s (attempt %d/%d)", subject, attempt, _MAX_RETRIES)
            return True
        except smtplib.SMTPAuthenticationError:
            logger.error(
                "SMTP authentication failed for '%s'; check EMAIL_USER/EMAIL_PASS",
                subject,
            )
            return False
        except smtplib.SMTPException as e:
            if not _is_transient_smtp_error(e):
                logger.error("Permanent SMTP error sending '%s': %s", subject, e)
                return False
            logger.warning("Transient SMTP error (attempt %d/%d): %s", attempt, _MAX_RETRIES, e)
        except (ConnectionRefusedError, ConnectionResetError, TimeoutError, OSError) as e:
            logger.warning(
                "Network error sending '%s' (attempt %d/%d): %s",
                subject,
                attempt,
                _MAX_RETRIES,
                e,
            )

        if attempt < _MAX_RETRIES:
            delay = _RETRY_DELAY_BASE**attempt
            logger.info("Retrying in %ds...", delay)
            time.sleep(delay)
        else:
            logger.error("All %d retries exhausted for '%s'", _MAX_RETRIES, subject)

    return False


def send_all(script_dir: Path | str | None = None) -> None:
    """Send the daily news and jobs emails."""
    datestamp = date.today().strftime("%m-%d-%Y")
    base = Path(script_dir) if script_dir else Path.cwd()

    logger.info("Sending emails for %s...", datestamp)
    news_ok = send_email(
        subject=f"Daily News: {datestamp}",
        body="Attached is Today's News Spreadsheet AND txt file (RealClearPolitics)",
        attachments=[base / "RCPheadlines.txt", base / "RCPlinks.csv"],
    )
    jobs_ok = send_email(
        subject=f"Daily Jobs: {datestamp}",
        body="Attached is today's Craigslist job listings!",
        attachments=[base / "jobs.txt"],
    )

    if news_ok and jobs_ok:
        logger.info("All emails sent successfully")
    else:
        logger.error("One or more emails failed")
