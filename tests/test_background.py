import base64
import os
import pytest

ASSETS_BASE = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'assets', 'images', 'backgrounds')


def _write_temp_image_to_assets(tmp_image_path: str, image_bytes: bytes):
    """Helper to write temp image to both tmp_path and assets directory."""
    os.makedirs(ASSETS_BASE, exist_ok=True)
    with open(tmp_image_path, 'wb') as f:
        f.write(image_bytes)
    # Also write to assets directory for the function to find
    asset_path = os.path.join(ASSETS_BASE, os.path.basename(tmp_image_path))
    with open(asset_path, 'wb') as f:
        f.write(image_bytes)
    return asset_path


def test_get_background_base64_valid(tmp_path):
    """Test that get_background_base64 returns correct base64 string for valid image."""
    # Create a temp image
    tmp_image_path = tmp_path / "test_image.png"
    image_bytes = b'\x89PNG\r\n\x1a\n'  # Minimal PNG header
    _write_temp_image_to_assets(str(tmp_image_path), image_bytes)

    # Import and test
    from src.background import get_background_base64
    result = get_background_base64("test_image")
    
    assert isinstance(result, str)
    expected = "data:image/png;base64," + base64.b64encode(image_bytes).decode('ascii')
    assert result == expected


def test_get_background_base64_not_found():
    """Test that get_background_base64 raises FileNotFoundError for missing image."""
    from src.background import get_background_base64
    
    with pytest.raises(FileNotFoundError):
        get_background_base64("nonexistent_image_that_does_not_exist")


def test_get_background_style_gradient():
    """Test that get_background_style returns gradient CSS when type is 'gradient'."""
    from src.background import get_background_style
    
    result = get_background_style("gradient", "any_image")
    assert isinstance(result, str)
    assert "linear-gradient" in result


def test_get_background_style_base64_image(tmp_path):
    """Test that get_background_style returns base64 URL when type is 'base64_image'."""
    # Create a temp image
    tmp_image_path = tmp_path / "style_test.png"
    image_bytes = b'\x89PNG\r\n\x1a\n'
    _write_temp_image_to_assets(str(tmp_image_path), image_bytes)

    from src.background import get_background_style
    result = get_background_style("base64_image", "style_test")
    
    assert isinstance(result, str)
    assert "data:image/png;base64," in result


def test_get_background_style_invalid_type():
    """Test that get_background_style raises ValueError for invalid type."""
    from src.background import get_background_style
    
    with pytest.raises(ValueError):
        get_background_style("invalid_type", "test_image")
