import base64
from pathlib import Path
from typing import Dict, Any, Optional
from jinja2 import Environment, FileSystemLoader, select_autoescape

from background import get_background_style


def get_icon_base64(icon_name: str = "romantic-icon") -> str:
    """Read an icon image and return it as a base64-encoded data URL."""
    icon_path = Path(__file__).parent.parent / "assets" / "images" / f"{icon_name}.png"

    if not icon_path.exists():
        raise FileNotFoundError(f"Icon not found: {icon_path}")

    with open(icon_path, "rb") as f:
        encoded = base64.b64encode(f.read()).decode("ascii")

    return f"data:image/png;base64,{encoded}"


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
    
    return template.render(**context)


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
    from background import get_card_background_style

    days = context.get("days_together", 0)
    months = context.get("months_together", 0)
    years = context.get("years_together", 0)

    # 从配置读取模板和背景设置
    config = context.get("config", {})
    app_config = config.get("app", {})

    template_name = app_config.get("template", "email_new")
    background_type = app_config.get("background_type", "gradient")
    background_image = app_config.get("background_image", "romantic")

    card_bg_type = app_config.get("card_background_type", "solid")
    card_bg_value = app_config.get("card_background_value", "rgba(255, 255, 255, 0.6)")

    # Generate card background style if possible
    try:
        card_background_style = get_card_background_style(card_bg_type, card_bg_value)
    except Exception:
        # Fallback to a sensible default if styling generation fails
        card_background_style = "rgba(255, 255, 255, 0.6)"

    # 获取背景样式
    try:
        background_style = get_background_style(background_type, background_image)
    except Exception:
        background_style = "linear-gradient(180deg, #FAD4E4 0%, #FDF6F0 50%, #FFF8F5 100%)"

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
) -> str:
    """渲染新的浪漫风格邮件模板."""
    env = get_template_env()
    template = env.get_template(f"{template_name}.html")

    # 获取图标 base64 数据
    try:
        icon_base64 = get_icon_base64("romantic-icon")
    except Exception:
        icon_base64 = ""

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
        "icon_base64": icon_base64,
    }

    return template.render(**context)
