import os
import requests
from typing import Dict, Optional, Any

def get_weather(city: str, api_key: Optional[str] = None) -> Optional[Dict[str, Any]]:
    """
    Get weather data for a city from OpenWeatherMap.
    
    Returns a dict with:
      - temperature (float): current temperature in Celsius
      - condition (str): weather description
      - humidity (int): humidity percentage
      - wind_speed (float): wind speed in m/s
    Returns None if any error occurs or required data is missing.
    """
    key = api_key or os.environ.get("OPENWEATHER_API_KEY")
    if not key:
        return None
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {"q": city, "appid": key, "units": "metric"}
    try:
        resp = requests.get(url, params=params, timeout=10)
        if resp.status_code != 200:
            return None
        data = resp.json()
        main = data.get("main", {})
        wind = data.get("wind", {})
        weather_list = data.get("weather", [])
        if not main or not wind or not weather_list:
            return None
        temperature = main.get("temp")
        humidity = main.get("humidity")
        wind_speed = wind.get("speed")
        condition = weather_list[0].get("description") if isinstance(weather_list, list) and weather_list else None
        if temperature is None or humidity is None or wind_speed is None or condition is None:
            return None
        return {
            "temperature": temperature,
            "condition": condition,
            "humidity": humidity,
            "wind_speed": wind_speed,
        }
    except Exception:
        return None
