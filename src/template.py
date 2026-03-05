from pathlib import Path
from typing import Dict, Any, Optional
from jinja2 import Environment, FileSystemLoader, select_autoescape


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
    template = env.get_template("email.html")
    
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
    render_email_with_data's expected format.
    
    Args:
        context: Dict from main.py with keys: days_together, quote, weather, 
                 anniversary, date, config
                 
    Returns:
        Rendered HTML string
    """
    import datetime
    
    # 直接使用 context 中的值，不再重新计算
    days = context.get("days_together", 0)
    months = context.get("months_together", 0)
    years = context.get("years_together", 0)
    
    # Build data dict for render_email_with_data
    data = {
        "days_together": days,
        "months_together": months,
        "years_together": years,
        "quote": context.get("quote", {"content": "", "category": ""}),
        "weather": context.get("weather"),
        "next_anniversary": context.get("anniversary"),
        "today": context.get("date", datetime.date.today().isoformat()),
        "sender_name": context.get("sender_name", ""),
        "recipient_name": context.get("recipient_name", ""),
    }
    
    return render_email_with_data(data)
