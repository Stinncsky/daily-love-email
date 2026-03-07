#!/usr/bin/env python3
"""
Generate email HTML preview by aggregating data from existing modules.
Usage:
  python scripts/generate_email.py -c config.yaml -o ./output --open
"""
import argparse
import os
import sys
from datetime import datetime, date
from pathlib import Path
import webbrowser

# Ensure src is on Python path to import existing modules
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, ".."))
SRC_DIR = os.path.join(ROOT_DIR, "src")
if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

from config import load_config
from calculator import calculate_days_together
from quotes import get_random_quote
from weather import get_weather
from anniversary import get_next_anniversary
from template import render_email

def load_and_prepare_context(config_path: str):
    cfg = load_config(config_path)
    if not isinstance(cfg, dict):
        cfg = {}

    email_cfg = cfg.get("email", {})
    weather_cfg = cfg.get("weather", {})
    love_cfg = cfg.get("love", {})
    anniversaries = cfg.get("anniversaries", [])
    app_cfg = cfg.get("app", {})

    start_date = love_cfg.get("start_date")
    # Calculate months/years using existing calculator, but ensure days_together is derived directly
    calc_result = calculate_days_together(start_date) if start_date else None
    if isinstance(calc_result, tuple) and len(calc_result) == 3:
        _, months_together, years_together = calc_result
        # Calculate total days for display consistently using date difference
        sd = datetime.strptime(start_date, "%Y-%m-%d").date()
        days_together = (date.today() - sd).days
    else:
        days_together = 0
        months_together, years_together = 0, 0

    quote = get_random_quote()

    city = weather_cfg.get("city")
    api_key = weather_cfg.get("api_key")
    weather = get_weather(city, api_key) if city else None

    anniversary = get_next_anniversary(anniversaries) if isinstance(anniversaries, list) else None

    context = {
        "config": cfg,
        "days_together": days_together,
        "months_together": months_together,
        "years_together": years_together,
        "weather": weather,
        "quote": quote,
        "anniversary": anniversary,
        "date": date.today().isoformat(),
        "sender_name": email_cfg.get("sender_name", ""),
        "recipient_name": email_cfg.get("recipient_name", ""),
        "recipient_city": weather_cfg.get("city", ""),
        "template": app_cfg.get("template", ""),
        "background_type": app_cfg.get("background_type", ""),
        "background_image": app_cfg.get("background_image", ""),
        "card_background_type": cfg.get("app", {}).get("card_background_type", "image"),
        "card_background_value": cfg.get("app", {}).get("card_background_value", "romantic"),
    }
    print("DEBUG CONTEXT card_background_type=", context.get("card_background_type"), "card_background_value=", context.get("card_background_value"))
    return cfg, context

def main():
    parser = argparse.ArgumentParser(description="Generate email HTML preview using existing modules.")
    parser.add_argument("-c", "--config", default="config.yaml", help="配置文件路径（默认：config.yaml）")
    parser.add_argument("-o", "--output", default="output", help="输出目录（默认：output）")
    parser.add_argument("--open", action="store_true", help="生成后在浏览器中打开")
    args = parser.parse_args()

    cfg, context = load_and_prepare_context(args.config)

    out_dir = args.output
    Path(out_dir).mkdir(parents=True, exist_ok=True)

    html = render_email(context)
    if html is None:
        print("ERROR: render_email returned None")
        sys.exit(2)

    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"email_{ts}.html"
    output_path = os.path.join(out_dir, filename)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"配置加载完成: {args.config}")
    # Verification print: ensure card background context keys exist and have values
    print("VERIFICATION: card_background_type present=", context.get("card_background_type") is not None,
          ", value=", context.get("card_background_type"),
          "; card_background_value present=", context.get("card_background_value") is not None,
          ", value=", context.get("card_background_value"))
    days = context.get("days_together", 0)
    print(f"恋爱天数: {days} 天")
    print(f"使用的模板: {context.get('template','')}，背景类型: {context.get('background_type','')}，背景图: {context.get('background_image','')}")
    print(f"生成的 HTML 文件: {output_path}")

    if args.open:
        try:
            webbrowser.open(f"file://{os.path.abspath(output_path)}")
        except Exception as e:
            print(f"WARNING: Failed to open browser: {e}")

if __name__ == "__main__":
    main()
