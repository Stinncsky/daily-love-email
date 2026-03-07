"""Background image utilities for email templates."""

import base64
import os
from pathlib import Path


def get_github_raw_url(image_path: str) -> str:
    """
    Convert a local image path to GitHub raw URL.

    Uses GITHUB_REPO_URL environment variable to construct the URL.
    Defaults to Stinncsky/daily-love-email repository if not set.
    Example: https://raw.githubusercontent.com/Stinncsky/daily-love-email/main/assets/images/backgrounds/romantic.png
    """
    DEFAULT_REPO_URL = "https://github.com/Stinncsky/daily-love-email"
    repo_url = os.environ.get("GITHUB_REPO_URL", DEFAULT_REPO_URL)
    branch = os.environ.get("GITHUB_BRANCH", "main")
    
    # Convert github.com URL to raw.githubusercontent.com
    raw_url = repo_url.replace("github.com", "raw.githubusercontent.com")
    if raw_url.endswith("/"):
        raw_url = raw_url[:-1]
    
    # Ensure path starts with /
    if not image_path.startswith("/"):
        image_path = "/" + image_path
    
    return f"{raw_url}/{branch}{image_path}"


def get_background_base64(image_name: str) -> str:
    """Read a PNG image and return it as a base64-encoded data URL."""
    image_path = Path("assets/images/backgrounds") / f"{image_name}.png"

    if not image_path.exists():
        raise FileNotFoundError(f"Image not found: {image_path}")

    with open(image_path, "rb") as f:
        encoded = base64.b64encode(f.read()).decode("ascii")

    return f"data:image/png;base64,{encoded}"


def get_background_url(image_name: str) -> str:
    """Get background image URL (GitHub raw URL preferred, fallback to base64)."""
    try:
        return get_github_raw_url(f"assets/images/backgrounds/{image_name}.png")
    except ValueError:
        # Fallback to base64 if GITHUB_REPO_URL not set
        return get_background_base64(image_name)


def get_icon_url(icon_name: str = "romantic-icon") -> str:
    """Get icon image URL (GitHub raw URL preferred, fallback to base64)."""
    try:
        return get_github_raw_url(f"assets/images/{icon_name}.png")
    except ValueError:
        # Fallback to base64
        icon_path = Path(__file__).parent.parent / "assets" / "images" / f"{icon_name}.png"
        if not icon_path.exists():
            raise FileNotFoundError(f"Icon not found: {icon_path}")
        with open(icon_path, "rb") as f:
            encoded = base64.b64encode(f.read()).decode("ascii")
        return f"data:image/png;base64,{encoded}"


def get_background_style(background_type: str, image_name: str, use_url: bool = True) -> str:
    """
    Get CSS background style based on type.
    
    Args:
        background_type: 'gradient', 'base64_image', or 'url_image'
        image_name: Name of the image (for image types)
        use_url: If True, use GitHub raw URL instead of base64
    """
    if background_type == "gradient":
        return "linear-gradient(180deg, #FAD4E4 0%, #FDF6F0 50%, #FFF8F5 100%)"
    elif background_type in ("base64_image", "image"):
        if use_url:
            try:
                url = get_background_url(image_name)
                return f"url({url})"
            except Exception:
                # Fallback to base64
                base64_data = get_background_base64(image_name)
                return f"url({base64_data})"
        else:
            base64_data = get_background_base64(image_name)
            return f"url({base64_data})"
    elif background_type == "url":
        # Direct URL provided
        return f"url({image_name})"
    else:
        raise ValueError(f"Invalid background_type: {background_type}")


def get_card_background_style(background_type: str, value: str, for_vml: bool = False, use_url: bool = True) -> str:
    """
    Get CSS background style for card container.

    Args:
        background_type: Type of background - 'solid', 'gradient', 'image', or 'url'
        value: Background value - color code, gradient CSS, image name, or URL
        for_vml: When True, format the background for VML (Outlook), returning a
                 bare URL/data string without the url() wrapper. Defaults to False
                 for CSS-compatible output.
        use_url: If True, use GitHub raw URL instead of base64 for images

    Returns:
        CSS background value string

    Examples:
        >>> get_card_background_style("solid", "#FFE4E1")
        '#FFE4E1'
        >>> get_card_background_style("gradient", "linear-gradient(135deg, #FFE4E1 0%, #FFF0F5 100%)")
        'linear-gradient(135deg, #FFE4E1 0%, #FFF0F5 100%)'
        >>> get_card_background_style("image", "card_bg")
        'url(https://raw.githubusercontent.com/...)' or 'url(data:image/png;base64,...)'
        >>> get_card_background_style("url", "https://example.com/bg.png")
        'url(https://example.com/bg.png)'
    """
    if background_type == "solid":
        # Solid color - return as-is (supports #RGB, #RGBA, rgb(), rgba())
        return value
    elif background_type == "gradient":
        # Gradient - return the full gradient CSS
        return value
    elif background_type == "url":
        # Direct URL provided (external image)
        if for_vml:
            return value
        return f"url({value})"
    elif background_type == "image":
        # Image - use URL if configured, otherwise base64
        if use_url:
            try:
                image_url = get_github_raw_url(f"assets/images/backgrounds/{value}.png")
                if for_vml:
                    return image_url
                return f"url({image_url})"
            except ValueError:
                # GITHUB_REPO_URL not set, fallback to base64
                pass
        
        # Fallback to base64
        base64_data = get_background_base64(value)
        if for_vml:
            # Outlook/VML requires a bare data URL, not wrapped in url()
            return base64_data
        return f"url({base64_data})"
    else:
        raise ValueError(f"Invalid card background_type: {background_type}. "
                        f"Must be one of: solid, gradient, image, url")


def convert_to_jsdelivr(raw_url: str) -> str:
    """
    Convert raw.githubusercontent.com URL to jsDelivr CDN URL for better China access.
    
    Example:
        https://raw.githubusercontent.com/username/repo/main/assets/images/bg.png
        -> https://cdn.jsdelivr.net/gh/username/repo@main/assets/images/bg.png
    """
    if "raw.githubusercontent.com" not in raw_url:
        return raw_url
    
    # Extract parts from raw URL
    # Format: https://raw.githubusercontent.com/{user}/{repo}/{branch}/path
    parts = raw_url.replace("https://raw.githubusercontent.com/", "").split("/")
    if len(parts) < 4:
        return raw_url
    
    user, repo, branch = parts[0], parts[1], parts[2]
    path = "/".join(parts[3:])
    
    return f"https://cdn.jsdelivr.net/gh/{user}/{repo}@{branch}/{path}"
