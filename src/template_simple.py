"""Simplified template renderer for romantic.html - using direct URLs only."""

import os
from pathlib import Path
from typing import Dict, Any, Optional
from jinja2 import Environment, FileSystemLoader, select_autoescape

from background import get_github_raw_url, convert_to_jsdelivr


def get_template_env() -> Environment:
    """Create and configure Jinja2 environment for email templates."""
    template_dir = Path(__file__).parent.parent / "templates"

    env = Environment(
        loader=FileSystemLoader(str(template_dir)),
        autoescape=select_autoescape(['html', 'xml']),
        trim_blocks=True,
        lstrip_blocks=True,
    )

    return env


def get_default_background_url() -> str:
    """Get default background image URL from GitHub repository."""
    try:
        url = get_github_raw_url("assets/images/backgrounds/romantic.png")
        return convert_to_jsdelivr(url)
    except Exception:
        return ""


def get_default_icon_url() -> str:
    """Get default icon URL from GitHub repository."""
    try:
        url = get_github_raw_url("assets/images/romantic-icon.png")
        return convert_to_jsdelivr(url)
    except Exception:
        return ""


def render_romantic_email(context: dict) -> str:
    """
    Render romantic.html template with simplified configuration.

    Only requires these context keys:
    - days_together: int
    - quote: dict with 'content'
    - weather: dict (optional)
    - date: str (today's date)
    - sender_name: str
    - recipient_name: str
    - recipient_city: str

    Uses environment variables for images (optional):
    - BACKGROUND_IMAGE_URL: URL for background image
    - ICON_URL: URL for icon image

    If not set, defaults to GitHub raw URLs from Stinncsky/daily-love-email repo.
    """
    import datetime

    env = get_template_env()
    template = env.get_template("romantic.html")

    # Get image URLs from environment variables or use defaults
    background_url = os.environ.get("BACKGROUND_IMAGE_URL") or get_default_background_url()
    icon_url = os.environ.get("ICON_URL") or get_default_icon_url()

    template_context = {
        "days_together": context.get("days_together", 0),
        "quote": context.get("quote", {"content": ""}),
        "weather": context.get("weather"),
        "today": context.get("date", datetime.date.today().isoformat()),
        "sender_name": context.get("sender_name", ""),
        "recipient_name": context.get("recipient_name", ""),
        "recipient_city": context.get("recipient_city", ""),
        "background_image_url": background_url,
        "icon_url": icon_url,
    }

    return template.render(**template_context)


def render_email(context: dict) -> str:
    """Main entry point - renders romantic.html template."""
    return render_romantic_email(context)
