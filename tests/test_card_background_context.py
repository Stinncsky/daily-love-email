import sys
from pathlib import Path

from scripts.generate_email import load_and_prepare_context


def write_config(tmp_path: Path, content: str) -> str:
    p = tmp_path / "config.yaml"
    p.write_text(content, encoding="utf-8")
    return str(p)


def test_card_background_context_keys(tmp_path: Path):
    config_content = """
email:
  sender: "a@example.com"
  recipient: "b@example.com"
weather:
  city: "Beijing"
  api_key: "testkey"
love:
  start_date: "2020-01-01"
anniversaries: []
app:
  template: "email"
  card_background_type: "image"
  card_background_value: "romantic"
  background_type: "gradient"
  background_image: "romantic"
"""

    config_path = write_config(tmp_path, config_content)
    cfg, context = load_and_prepare_context(config_path)

    assert "card_background_type" in context
    assert "card_background_value" in context
    assert context["card_background_type"] == "image"
    assert context["card_background_value"] == "romantic"
