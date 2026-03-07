#!/usr/bin/env python3
"""
Daily Love Email - Main Script (Simplified)

This script orchestrates the daily love email workflow:
1. Load configuration
2. Calculate days together
3. Get weather
4. Select random quote
5. Find next anniversary
6. Render email template (using romantic.html with direct URLs)
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

# Use simplified template renderer for romantic.html
try:
    from template_simple import render_email  # type: ignore
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
    if callable(load_config):
        try:
            cfg = load_config()
        except Exception as e:
            log.warning("load_config() failed: %s", e)
            cfg = {}
    if not cfg:
        cfg = {
            "email": {
                "recipient": os.environ.get("EMAIL_RECIPIENT"),
                "sender": os.environ.get("EMAIL_SENDER"),
                "password": os.environ.get("EMAIL_PASSWORD"),
                "smtp_server": os.environ.get("SMTP_SERVER", "smtp.qq.com"),
                "smtp_port": int(os.environ.get("SMTP_PORT", "465")) if os.environ.get("SMTP_PORT") else 465,
                "sender_name": os.environ.get("SENDER_NAME", "Daily Love"),
                "recipient_name": os.environ.get("RECIPIENT_NAME", ""),
            },
            "weather": {
                "city": os.environ.get("CITY", ""),
                "api_key": os.environ.get("WEATHER_API_KEY"),
            },
            "love": {
                "start_date": os.environ.get("LOVE_START_DATE"),
            },
            "anniversaries": parse_anniversaries_from_env(),
            "subject": os.environ.get("EMAIL_SUBJECT", "Daily Love Email"),
            "start_date": os.environ.get("LOVE_START_DATE"),
        }
    return cfg


def parse_anniversaries_from_env():
    """Parse anniversaries from environment variable ANNIVERSARIES (JSON format)."""
    import json
    anniversaries_env = os.environ.get("ANNIVERSARIES", "")
    if not anniversaries_env:
        return []
    try:
        anniversaries = json.loads(anniversaries_env)
        if isinstance(anniversaries, list):
            return anniversaries
    except json.JSONDecodeError:
        pass
    return []


def safe_call(func, *args, **kwargs):
    """Call a function if available, else return None.
    - If the function raises a TypeError due to signature mismatch, try calling without args.
    - Do not blanket-catch unrelated exceptions to avoid hiding bugs."""
    if not callable(func):
        return None
    try:
        return func(*args, **kwargs)
    except TypeError:
        # Fallback: attempt to call with no args if signature differs
        try:
            return func()
        except Exception as e:
            log.error("Function call failed: %s", e)
            return None
    # Do not catch all other exceptions to avoid hiding bugs; let them propagate


def build_context(cfg, days, months, years, weather, quote, anniversary):
    email_cfg = cfg.get("email", {})
    weather_cfg = cfg.get("weather", {})
    return {
        "config": cfg,
        "days_together": days,
        "months_together": months,
        "years_together": years,
        "weather": weather,
        "quote": quote,
        "anniversary": anniversary,
        "date": date.today().isoformat(),
        "sender_name": email_cfg.get("sender_name", ""),
        "recipient_name": email_cfg.get("recipient_name", ""),
        "recipient_city": weather_cfg.get("city", ""),
    }


def main():
    parser = argparse.ArgumentParser(description="Daily Love Email Orchestrator")
    parser.add_argument("--dry-run", dest="dry_run", action="store_true", help="Test without sending email")
    parser.add_argument("--test-email", dest="test_email", default=None, help="Override recipient email for testing")
    args = parser.parse_args()

    dry_run = bool(args.dry_run) or os.environ.get("DRY_RUN", "").lower() in ("true", "1", "yes")
    test_email = args.test_email

    
    cfg = load_config_safe()
    if not cfg:
        log.error("Configuration is empty. Aborting.")
        return 1

    
    # Calculate days together
    calc_result = safe_call(calculate_days_together, cfg.get("love", {}).get("start_date"))
    if isinstance(calc_result, tuple) and len(calc_result) == 3:
        days, months, years = calc_result
    else:
        days, months, years = 0, 0, 0

    # Get weather
    weather_cfg = cfg.get("weather", {})
    city = weather_cfg.get("city") or cfg.get("weather", {}).get("city") or cfg.get("location", "")
    api_key = weather_cfg.get("api_key")
    weather = safe_call(get_weather, city, api_key) if city else None

    quote = safe_call(get_random_quote)
    anniversaries_list = cfg.get("anniversaries", [])
    anniversary = safe_call(get_next_anniversary, anniversaries_list) if anniversaries_list else None

    
    # Build context and render email (using romantic.html template)
    context = build_context(cfg, days, months, years, weather, quote, anniversary)
    body = render_email(context) if callable(render_email) else ""

    
    recipient = test_email or cfg.get("email", {}).get("recipient")
    subject = cfg.get("email", {}).get("subject", cfg.get("subject", "Daily Love Email"))

    if not recipient:
        log.error("No recipient email configured. Aborting.")
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
            f"days={days} | months={months} | years={years} | weather={weather} | quote={quote} | anniversary={anniversary}"
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
