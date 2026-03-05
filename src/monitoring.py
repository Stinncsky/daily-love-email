"""Monitoring и 日志模块 for daily romance mail system.

Provides: log_execution, get_stats, health_check, send_alert
"""

from __future__ import annotations

import json
import os
import logging
import datetime
from pathlib import Path
from typing import Any, Dict, Optional

# Paths for logs
LOG_DIR = Path("logs")
LOG_FILE = LOG_DIR / "execution.log"

_logger = logging.getLogger("monitoring")
if not _logger.handlers:
    _logger.setLevel(logging.INFO)
    _sh = logging.StreamHandler()
    _fmt = logging.Formatter("%(levelname)s:%(name)s:%(message)s")
    _sh.setFormatter(_fmt)
    _logger.addHandler(_sh)


def _ensure_log_dir() -> None:
    try:
        LOG_DIR.mkdir(parents=True, exist_ok=True)
    except Exception as e:
        _logger.error("Failed ensuring log directory: %s", e)


def _parse_ts(ts: Optional[str]) -> Optional[datetime.datetime]:
    if not ts:
        return None
    try:
        if ts.endswith("Z"):
            ts = ts[:-1] + "+00:00"
        return datetime.datetime.fromisoformat(ts)
    except Exception:
        return None


def log_execution(context: Optional[Dict[str, Any]]) -> None:
    """Record execution result as a JSON line in logs/execution.log.

    Context can contain arbitrary data. The function determines status, duration
    and error from the context when available.
    """
    _ensure_log_dir()
    if context is None:
        context = {}

    # Derive status and error
    status = context.get("status") if isinstance(context, dict) else None
    error = None
    duration = None

    if isinstance(context, dict):
        if not status:
            status = "success"
        if "error" in context:
            error = context.get("error")
        # Try to infer duration from explicit value or timestamps
        if "duration" in context:
            duration = context.get("duration")
        if "start" in context and "end" in context:
            start = context.get("start")
            end = context.get("end")
            if isinstance(start, (int, float)) and isinstance(end, (int, float)):
                duration = float(end) - float(start)
        if error is not None:
            status = "failure" if not str(error) or str(error) == "" else status
    else:
        status = status or "unknown"

    # If there is an error, mark as failure
    if error is not None:
        status = "failure"

    timestamp = datetime.datetime.utcnow().isoformat(timespec="seconds") + "Z"

    log_entry = {
        "timestamp": timestamp,
        "status": status,
        "duration": duration,
        "error": error,
        "context": context,
    }

    try:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(json.dumps(log_entry, ensure_ascii=False) + "\n")
    except Exception as e:
        _logger.error("Failed writing monitoring log: %s", e)

    # Also emit a simple log line for immediate visibility
    _logger.info("execution logged: status=%s duration=%s error=%s", status, duration, error)


def get_stats(days: int = 30) -> Dict[str, Any]:
    """Return execution statistics for the last N days.

    Returns a dict: { total, successes, failures, success_rate }.
    """
    _ensure_log_dir()
    cutoff = datetime.datetime.utcnow() - datetime.timedelta(days=days)
    total = 0
    successes = 0
    failures = 0

    if not LOG_FILE.exists():
        return {"total": 0, "successes": 0, "failures": 0, "success_rate": 0.0}

    try:
        with open(LOG_FILE, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    entry = json.loads(line)
                except Exception:
                    continue
                ts = _parse_ts(entry.get("timestamp"))
                if ts is None or ts < cutoff:
                    continue
                total += 1
                if entry.get("status") == "success":
                    successes += 1
                else:
                    failures += 1
    except Exception as e:
        _logger.error("Failed reading monitoring logs: %s", e)
        return {"total": 0, "successes": 0, "failures": 0, "success_rate": 0.0}

    if total > 0:
        rate = successes / total
    else:
        rate = 0.0
    return {"total": total, "successes": successes, "failures": failures, "success_rate": round(rate, 4)}


def health_check() -> Dict[str, Any]:
    """Perform a lightweight health check for monitoring setup."""
    issues = []
    ok = True
    # Check log directory and file writability
    try:
        LOG_DIR.mkdir(parents=True, exist_ok=True)
        if not LOG_FILE.exists():
            # best-effort create and remove a tiny file to ensure writability
            try:
                LOG_FILE.touch()
                LOG_FILE.unlink()
            except Exception as e:
                issues.append(f"Cannot create log file: {e}")
                ok = False
        else:
            if not os.access(LOG_DIR, os.W_OK):
                issues.append("Logs directory is not writable")
                ok = False
    except Exception as e:
        issues.append(f"Log directory check failed: {e}")
        ok = False

    # Check availability of stdlib modules (json, datetime)
    try:
        import json as _json  # noqa: F401
        import datetime as _dt  # noqa: F401
    except Exception as e:
        issues.append(f"stdlib modules missing: {e}")
        ok = False

    return {
        "healthy": ok,
        "issues": issues,
        "details": {
            "log_dir": str(LOG_DIR),
            "log_file": str(LOG_FILE),
        },
    }


def send_alert(message: str) -> bool:
    """Send a simple alert email if SMTP is configured via environment vars.

    Required env vars (optional):
      - ALERT_SMTP_HOST
      - ALERT_SMTP_PORT (default 25)
      - ALERT_SMTP_USER
      - ALERT_SMTP_PASSWORD
      - ALERT_RECIPIENTS (comma-separated emails)
    """
    host = os.environ.get("ALERT_SMTP_HOST")
    port = int(os.environ.get("ALERT_SMTP_PORT", "25"))
    user = os.environ.get("ALERT_SMTP_USER")
    password = os.environ.get("ALERT_SMTP_PASSWORD")
    recipients = os.environ.get("ALERT_RECIPIENTS", "")

    if not host or not recipients:
        _logger.warning("Alerting not configured (host or recipients missing). Skipping.")
        return False

    to_addrs = [r.strip() for r in recipients.split(",") if r.strip()]
    if not to_addrs:
        _logger.warning("Alert recipients list is empty. Skipping.")
        return False

    from email.message import EmailMessage
    import smtplib

    msg = EmailMessage()
    msg["Subject"] = "Monitoring Alert"
    msg["From"] = user if user else "monitor@example.com"
    msg["To"] = ", ".join(to_addrs)
    msg.set_content(message)

    try:
        with smtplib.SMTP(host, port, timeout=10) as server:
            server.ehlo()
            if port == 587:
                server.starttls()
            if user and password:
                server.login(user, password)
            server.send_message(msg)
        _logger.info("Alert email sent to %s", to_addrs)
        return True
    except Exception as e:
        _logger.error("Failed to send alert: %s", e)
        return False
