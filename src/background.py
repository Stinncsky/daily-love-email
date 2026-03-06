"""Background image utilities for email templates."""

import base64
from pathlib import Path


def get_background_base64(image_name: str) -> str:
    """Read a PNG image and return it as a base64-encoded data URL."""
    image_path = Path("assets/images/backgrounds") / f"{image_name}.png"

    if not image_path.exists():
        raise FileNotFoundError(f"Image not found: {image_path}")

    with open(image_path, "rb") as f:
        encoded = base64.b64encode(f.read()).decode("ascii")

    return f"data:image/png;base64,{encoded}"


def get_background_style(background_type: str, image_name: str) -> str:
    """Get CSS background style based on type."""
    if background_type == "gradient":
        return "linear-gradient(180deg, #FAD4E4 0%, #FDF6F0 50%, #FFF8F5 100%)"
    elif background_type == "base64_image":
        base64_data = get_background_base64(image_name)
        return f"url({base64_data})"
    else:
        raise ValueError(f"Invalid background_type: {background_type}")


def get_card_background_style(background_type: str, value: str, for_vml: bool = False) -> str:
    """
    Get CSS background style for card container.

    Args:
        background_type: Type of background - 'solid', 'gradient', or 'image'
        value: Background value - color code, gradient CSS, or image name
        for_vml: When True, format the background for VML (Outlook), returning a
                 bare URL/data string without the url() wrapper. Defaults to False
                 for CSS-compatible output.

    Returns:
        CSS background value string

    Examples:
        >>> get_card_background_style("solid", "#FFE4E1")
        '#FFE4E1'
        >>> get_card_background_style("gradient", "linear-gradient(135deg, #FFE4E1 0%, #FFF0F5 100%)")
        'linear-gradient(135deg, #FFE4E1 0%, #FFF0F5 100%)'
        >>> get_card_background_style("image", "card_bg")
        'url(data:image/png;base64,...)'
        >>> get_card_background_style("image", "card_bg", for_vml=True)
        'data:image/png;base64,...'  # bare URL for VML (Outlook)
    """
    if background_type == "solid":
        # Solid color - return as-is (supports #RGB, #RGBA, rgb(), rgba())
        return value
    elif background_type == "gradient":
        # Gradient - return the full gradient CSS
        return value
    elif background_type == "image":
        # Image - convert to base64 data URL
        base64_data = get_background_base64(value)
        if for_vml:
            # Outlook/VML requires a bare data URL, not wrapped in url()
            return base64_data
        return f"url({base64_data})"
    else:
        raise ValueError(f"Invalid card background_type: {background_type}. "
                        f"Must be one of: solid, gradient, image")
