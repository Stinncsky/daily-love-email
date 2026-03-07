"""
天气模块 - 高德地图天气API适配器
"""

import logging
import os
from typing import Any, Dict, Optional

import requests

# 支持两种导入方式（直接运行和作为包导入）
try:
    from src.city_code import get_adcode
except ImportError:
    from city_code import get_adcode

# 配置模块日志
logger = logging.getLogger(__name__)


def _parse_wind_power(wind_power: str) -> float:
    """
    将高德风力描述转换为风速（m/s）

    高德返回的风力格式如："3级"、"4-5级"
    转换为 m/s：级别 × 1.5（近似值）

    Args:
        wind_power: 高德风力描述（如"3级"）

    Returns:
        风速（m/s）
    """
    if not wind_power or not isinstance(wind_power, str):
        return 0.0

    try:
        # 处理 "4-5级" 格式，取中间值
        if "-" in wind_power:
            parts = wind_power.replace("级", "").split("-")
            if len(parts) == 2:
                level = (int(parts[0]) + int(parts[1])) / 2
            else:
                return 0.0
        else:
            # 处理 "3级" 格式，同时处理 ≤ ≥ 等特殊符号
            level = int(
                wind_power.replace("级", "")
                .replace("<", "")
                .replace(">", "")
                .replace("≤", "")
                .replace("≥", "")
            )

        # 级别 × 1.5 m/s（近似转换）
        return round(level * 1.5, 1)
    except (ValueError, TypeError):
        return 0.0


def _fetch_live_weather(adcode: str, api_key: str) -> Optional[Dict[str, Any]]:
    """
    获取实况天气数据

    Args:
        adcode: 城市 adcode
        api_key: 高德 API Key

    Returns:
        实况天气数据字典，失败返回 None
    """
    url = "https://restapi.amap.com/v3/weather/weatherInfo"
    params = {"key": api_key, "city": adcode, "extensions": "base"}

    try:
        resp = requests.get(url, params=params, timeout=10)
        resp.raise_for_status()
        data = resp.json()

        if data.get("status") != "1" or not data.get("lives"):
            logger.warning("Live weather API error: status=%s, info=%s", data.get("status"), data.get("info"))
            return None

        live = data["lives"][0]
        return {
            "temperature": float(live.get("temperature", 0)),
            "condition": live.get("weather", ""),
            "humidity": float(live.get("humidity", 0)),
            "wind_speed": _parse_wind_power(live.get("windpower", "")),
        }
    except requests.RequestException as e:
        logger.warning("Live weather request failed for adcode=%s: %s", adcode, e)
        return None
    except (KeyError, ValueError, TypeError) as e:
        logger.error("Live weather data parsing failed: %s", e)
        return None


def _fetch_forecast_weather(adcode: str, api_key: str) -> Optional[Dict[str, float]]:
    """
    获取预报天气数据（用于获取最高/最低温度）

    Args:
        adcode: 城市 adcode
        api_key: 高德 API Key

    Returns:
        包含 temp_min 和 temp_max 的字典，失败返回 None
    """
    url = "https://restapi.amap.com/v3/weather/weatherInfo"
    params = {"key": api_key, "city": adcode, "extensions": "all"}

    try:
        resp = requests.get(url, params=params, timeout=10)
        resp.raise_for_status()
        data = resp.json()

        if data.get("status") != "1" or not data.get("forecasts"):
            logger.warning("Forecast API error: status=%s, info=%s", data.get("status"), data.get("info"))
            return None

        forecast = data["forecasts"][0]
        if not forecast.get("casts"):
            logger.warning("Forecast API: no casts data for adcode=%s", adcode)
            return None

        # 获取今天的预报（第一个元素）
        today_cast = forecast["casts"][0]

        return {
            "temp_min": float(today_cast.get("nighttemp", 0)),
            "temp_max": float(today_cast.get("daytemp", 0)),
        }
    except requests.RequestException as e:
        logger.warning("Forecast request failed for adcode=%s: %s", adcode, e)
        return None
    except (KeyError, ValueError, TypeError) as e:
        logger.error("Forecast data parsing failed: %s", e)
        return None


def get_weather(city: str, api_key: Optional[str] = None) -> Optional[Dict[str, Any]]:
    """
    获取城市天气数据（高德地图天气API）

    返回兼容格式的天气数据：
      - temperature (float): 当前温度（摄氏度）
      - temp_min (float): 当日最低温度
      - temp_max (float): 当日最高温度
      - condition (str): 天气描述（中文，如"晴"、"多云"）
      - humidity (float): 湿度百分比
      - wind_speed (float): 风速（m/s）

    降级处理：
      - 预报API失败时，使用实时温度作为 min/max
      - 实况API失败时，返回 None
      - 城市编码找不到时，返回 None

    Args:
        city: 城市名称（中文，如"北京市"、"上海"）
        api_key: 高德地图 API Key，默认从环境变量 AMAP_API_KEY 读取

    Returns:
        天气数据字典，出错时返回 None

    Examples:
        >>> get_weather("北京市", "your_api_key")
        {
            "temperature": 22.0,
            "temp_min": 18.0,
            "temp_max": 26.0,
            "condition": "晴",
            "humidity": 45.0,
            "wind_speed": 4.5
        }
    """
    # 获取 API Key
    key = api_key or os.environ.get("AMAP_API_KEY") or os.environ.get("WEATHER_API_KEY")
    if not key:
        return None

    # 获取城市 adcode
    adcode = get_adcode(city)
    if not adcode:
        logger.warning("City not found: %s", city)
        return None

    # 获取实况天气
    live_data = _fetch_live_weather(adcode, key)
    if not live_data:
        return None

    # 获取预报天气（最高/最低温度）
    forecast_data = _fetch_forecast_weather(adcode, key)

    if forecast_data:
        # 合并数据
        return {
            "temperature": live_data["temperature"],
            "temp_min": forecast_data["temp_min"],
            "temp_max": forecast_data["temp_max"],
            "condition": live_data["condition"],
            "humidity": live_data["humidity"],
            "wind_speed": live_data["wind_speed"],
        }
    else:
        # 降级：使用实时温度作为 min/max
        temp = live_data["temperature"]
        return {
            "temperature": temp,
            "temp_min": temp,
            "temp_max": temp,
            "condition": live_data["condition"],
            "humidity": live_data["humidity"],
            "wind_speed": live_data["wind_speed"],
        }
