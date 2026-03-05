#!/usr/bin/env python3
"""
Daily Love Email - Main Script

This script orchestrates the daily love email workflow:
1. Load configuration
2. Calculate days together
3. Get weather
4. Select random quote
5. Find next anniversary
6. Render email template
7. Send email
"""

import os
import sys
import argparse
import logging
from datetime import date

# Wave 2 modules (best-effort imports; provide fallbacks if unavailable)
try:
    from config import load_config  # type: ignore
except Exception:
    load_config = None  # fallback below

try:
    from calculator import calculate_days_together  # type: ignore
except Exception:
    calculate_days_together = None

try:
    from anniversary import get_next_anniversary  # type: ignore
except Exception:
    get_next_anniversary = None

try:
    from weather import get_weather  # type: ignore
except Exception:
    get_weather = None

try:
    from quotes import get_random_quote  # type: ignore
except Exception:
    get_random_quote = None

try:
    from template import render_email  # type: ignore
except Exception:
    render_email = None

try:
    from email_sender import send_email  # type: ignore
except Exception:
    send_email = None

LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)
log = logging.getLogger("daily-love-email")
NOTEPAD_PATH = os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")), ".sisyphus/notepads/daily-love-email/learnings.md")


def ensure_notepad_dir():
    dirpath = os.path.dirname(NOTEPAD_PATH)
    os.makedirs(dirpath, exist_ok=True)


def append_learning_log(entry: str):
    try:
        ensure_notepad_dir()
        with open(NOTEPAD_PATH, "a", encoding="utf-8") as f:
            f.write(entry + "\n")
    except Exception as e:
        log.debug("Failed to write to learnings notepad: %s", e)

def load_config_safe():
    """Load config from config.yaml via load_config(), or fall back to env vars."""
    cfg = {}
    # Preferred: load from config.yaml / environment via the project API
    if callable(load_config):
        try:
            cfg = load_config()
        except Exception as e:
            log.warning("load_config() failed: %s", e)
            cfg = {}
    # Fallback: environment-based config
    if not cfg:
        cfg = {
            "to_email": os.environ.get("TO_EMAIL"),
            "from_email": os.environ.get("FROM_EMAIL"),
            "smtp_server": os.environ.get("SMTP_SERVER"),
            "smtp_port": int(os.environ.get("SMTP_PORT", "587")) if os.environ.get("SMTP_PORT") else 587,
            "smtp_user": os.environ.get("SMTP_USER"),
            "smtp_password": os.environ.get("SMTP_PASSWORD"),
            "location": os.environ.get("LOCATION", "") ,
            "sender_name": os.environ.get("SENDER_NAME", "Daily Love"),
            "subject": os.environ.get("EMAIL_SUBJECT", "Daily Love Email"),
            "start_date": os.environ.get("START_DATE"),
        }
    return cfg


def safe_call(func, *args, **kwargs):
    """Call a function if available, else return None."""
    if not callable(func):
        return None
    try:
        return func(*args, **kwargs)
    except TypeError:
        # Fallback: call with no args, in case the signature is different
        try:
            return func()
        except Exception as e:
            log.error("Function call failed: %s", e)
            return None
    except Exception as e:
        log.error("Function call failed: %s", e)
        return None


def build_context(cfg, days, weather, quote, anniversary):
    return {
        "config": cfg,
        "days_together": days,
        "weather": weather,
        "quote": quote,
        "anniversary": anniversary,
        "date": date.today().isoformat(),
    }


def main():
    parser = argparse.ArgumentParser(description="Daily Love Email Orchestrator")
    parser.add_argument("--dry-run", dest="dry_run", action="store_true", help="Test without sending email")
    parser.add_argument("--test-email", dest="test_email", default=None, help="Override recipient email for testing")
    args = parser.parse_args()

    dry_run = bool(args.dry_run)
    test_email = args.test_email

    
    cfg = load_config_safe()
    if not cfg:
        log.error("Configuration is empty. Aborting.")
        return 1

    
    days = safe_call(calculate_days_together, cfg.get("start_date"), date.today())
    weather = safe_call(get_weather, cfg.get("location", ""))
    quote = safe_call(get_random_quote)
    anniversary = safe_call(get_next_anniversary, cfg)

    
    context = build_context(cfg, days, weather, quote, anniversary)
    body = render_email(context) if callable(render_email) else ""

    
    recipient = test_email or cfg.get("to_email")
    subject = cfg.get("subject", "Daily Love Email")

    if not recipient:
        log.error("No recipient email configured (TO_EMAIL). Aborting.")
        return 1

    if dry_run:
        log.info("Dry-run: email would be sent to %s with subject '%s'", recipient, subject)
    else:
        if callable(send_email):
            sent = safe_call(send_email, cfg, subject, body, to=recipient)
            if sent is None:
                sent = safe_call(send_email, recipient, subject, body)
            if sent is False:
                log.error("Email sending failed.")
        else:
            log.warning("send_email() not available; skipping actual send in this environment.")

    log.info("Workflow completed. dry_run=%s, recipient=%s", dry_run, recipient)
    try:
        summary_line = (
            f"{date.today().isoformat()} | dry_run={dry_run} | to={recipient} | "
            f"days={days} | weather={weather} | quote={quote} | anniversary={anniversary}"
        )
        append_learning_log(summary_line)
    except Exception as e:
        log.debug("Skipping learnings append due to error: %s", e)
    return 0


if __name__ == "__main__":
    try:
        code = main()
        sys.exit(code)
    except Exception as e:
        log.exception("Unhandled exception in main: %s", e)
        sys.exit(1)
