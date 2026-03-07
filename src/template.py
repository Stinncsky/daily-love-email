import os
import re
from pathlib import Path
from typing import Dict, Any, Optional
from jinja2 import Environment, FileSystemLoader, select_autoescape

from background import (
    get_background_style,
    get_card_background_style,
    get_icon_url,
    convert_to_jsdelivr,
)


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


def convert_all_to_jsdelivr(text: str) -> str:
    """Scan the text for raw.githubusercontent.com URLs and convert them to jsDelivr CDN URLs."""
    pattern = re.compile(r"https?://raw\.githubusercontent\.com[^\s'\"]+")
    def _repl(m: re.Match) -> str:
        return convert_to_jsdelivr(m.group(0))
    return pattern.sub(_repl, text)


def render_email_template(
    days_together: int,
    months_together: int,
    years_together: int,
    quote: Dict[str, Any],
    weather: Optional[Dict[str, Any]],
    next_anniversary: Optional[Dict[str, Any]],
    today: str,
) -> str:
    """
    Render the daily love email HTML template.
    
    Args:
        days_together: Total days spent together
        months_together: Total months spent together
        years_together: Total years spent together
        quote: Dict with 'content' and 'category' keys
        weather: Dict with 'temperature', 'condition', 'humidity', 'wind_speed' or None
        next_anniversary: Dict with 'name' and 'days_until' or None
        today: Today's date as a formatted string
        
    Returns:
        Rendered HTML string ready for email
    """
    env = get_template_env()
    template = env.get_template("email_new.html")
    
    context = {
        "days_together": days_together,
        "months_together": months_together,
        "years_together": years_together,
        "quote": quote,
        "weather": weather,
        "next_anniversary": next_anniversary,
        "today": today,
    }
    
    content = template.render(**context)
    # Convert any raw.githubusercontent.com image URLs to jsDelivr CDN URLs
    content = convert_all_to_jsdelivr(content)
    return content


def render_email_with_data(data: Dict[str, Any]) -> str:
    """
    Render email using a data dictionary.
    
    Convenience function that extracts values from a dict
    and calls render_email_template.
    
    Expected data structure:
    {
        'days_together': int,
        'months_together': int,
        'years_together': int,
        'quote': {'content': str, 'category': str},
        'weather': {'temperature': float, 'condition': str, ...} or None,
        'next_anniversary': {'name': str, 'days_until': int} or None,
        'today': str,
    }
    """
    return render_email_template(
        days_together=data["days_together"],
        months_together=data["months_together"],
        years_together=data["years_together"],
        quote=data["quote"],
        weather=data.get("weather"),
        next_anniversary=data.get("next_anniversary"),
        today=data["today"],
    )


def render_email(context: dict) -> str:
    """
    Render email template with main.py compatible interface.

    This is a wrapper that adapts main.py's context format to
    render_email_template_new's expected format (the new romantic template).

    Args:
        context: Dict from main.py with keys: days_together, quote, weather,
                 anniversary, date, config, sender_name, recipient_name, recipient_city

    Returns:
        Rendered HTML string
    """
    import datetime

    days = context.get("days_together", 0)
    months = context.get("months_together", 0)
    years = context.get("years_together", 0)

    config = context.get("config", {})
    app_config = config.get("app", {})

    template_name = app_config.get("template", "email_new")
    background_type = app_config.get("background_type", "gradient")
    background_image = app_config.get("background_image", "romantic")

    card_bg_type = app_config.get("card_background_type", "solid")
    card_bg_value = app_config.get("card_background_value", "rgba(255, 255, 255, 0.6)")

    # Check if we should use URL instead of base64 (default: True)
    use_url = os.environ.get("USE_IMAGE_URL", "true").lower() in ("true", "1", "yes")

    # Generate card background style if possible
    try:
        card_background_style = get_card_background_style(card_bg_type, card_bg_value, use_url=use_url)
    except Exception:
        card_background_style = "rgba(255, 255, 255, 0.6)"

    # Get background style
    try:
        background_style = get_background_style(background_type, background_image, use_url=use_url)
    except Exception:
        background_style = "linear-gradient(180deg, #FAD4E4 0%, #FDF6F0 50%, #FFF8F5 100%)"

    # Get icon URL
    icon_url = app_config.get("icon_url")
    if not icon_url:
        try:
            icon_url = get_icon_url("romantic-icon")
        except Exception:
            icon_url = None

    return render_email_template_new(
        recipient_name=context.get("recipient_name", ""),
        sender_name=context.get("sender_name", ""),
        recipient_city=context.get("recipient_city", ""),
        days_together=days,
        months_together=months,
        years_together=years,
        quote=context.get("quote", {"content": "", "category": ""}),
        weather=context.get("weather"),
        today=context.get("date", datetime.date.today().isoformat()),
        template_name=template_name,
        background_style=background_style,
        card_background_style=card_background_style,
        card_background_type=card_bg_type,
        icon_url=icon_url,
    )


def render_email_template_new(
    recipient_name: str,
    sender_name: str,
    recipient_city: str,
    days_together: int,
    months_together: int,
    years_together: int,
    quote: dict,
    weather: Optional[Dict[str, Any]],
    today: str,
    template_name: str = "email_new",
    background_style: str = "linear-gradient(180deg, #FAD4E4 0%, #FDF6F0 50%, #FFF8F5 100%)",
    card_background_style: Optional[str] = None,
    card_background_type: str = "solid",
    icon_url: Optional[str] = None,
) -> str:
    """Render the new romantic style email template."""
    env = get_template_env()
    template = env.get_template(f"{template_name}.html")

    # Convert icon URL to jsDelivr if it's from raw.githubusercontent.com
    if icon_url and "raw.githubusercontent.com" in icon_url:
        icon_url = convert_to_jsdelivr(icon_url)

    context = {
        "recipient_name": recipient_name,
        "sender_name": sender_name,
        "recipient_city": recipient_city,
        "days_together": days_together,
        "months_together": months_together,
        "years_together": years_together,
        "quote": quote,
        "weather": weather,
        "today": today,
        "background_style": background_style,
        "card_background_style": card_background_style,
        "card_background_type": card_background_type,
        "icon_base64": icon_url if icon_url else "",
    }

    html = template.render(**context)
    
    # Convert any remaining raw.githubusercontent.com URLs to jsDelivr
    html = convert_all_to_jsdelivr(html)
    
    return html
