import os
import requests
from typing import Dict, Optional, Any

def get_weather(city: str, api_key: Optional[str] = None) -> Optional[Dict[str, Any]]:
    """
    Get weather data for a city from OpenWeatherMap.
    
    Returns a dict with:
      - temperature (float): current temperature in Celsius
      - temp_min (float): minimum temperature for the day
      - temp_max (float): maximum temperature for the day
      - condition (str): weather description
      - humidity (int): humidity percentage
      - wind_speed (float): wind speed in m/s
    Returns None if any error occurs or required data is missing.
    """
    key = api_key or os.environ.get("WEATHER_API_KEY") or os.environ.get("OPENWEATHER_API_KEY")
    if not key:
        return None
    
    try:
        forecast_url = "https://api.openweathermap.org/data/2.5/forecast"
        forecast_params = {"q": city, "appid": key, "units": "metric"}
        forecast_resp = requests.get(forecast_url, params=forecast_params, timeout=10)
        
        temp_min = None
        temp_max = None
        
        if forecast_resp.status_code == 200:
            forecast_data = forecast_resp.json()
            forecast_list = forecast_data.get("list", [])
            from datetime import datetime, timezone
            today = datetime.now(timezone.utc).date()
            today_temps = []
            
            for forecast in forecast_list:
                dt_txt = forecast.get("dt_txt", "")
                forecast_time = datetime.strptime(dt_txt, "%Y-%m-%d %H:%M:%S")
                if forecast_time.date() == today:
                    main_data = forecast.get("main", {})
                    if "temp" in main_data:
                        today_temps.append(main_data["temp"])
            
            if today_temps:
                temp_min = min(today_temps)
                temp_max = max(today_temps)
        
        url = "https://api.openweathermap.org/data/2.5/weather"
        params = {"q": city, "appid": key, "units": "metric"}
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
        
        if temp_min is None:
            temp_min = main.get("temp_min") if main.get("temp_min") is not None else temperature
        if temp_max is None:
            temp_max = main.get("temp_max") if main.get("temp_max") is not None else temperature
        
        if temperature is None or humidity is None or wind_speed is None or condition is None:
            return None
        
        return {
            "temperature": temperature,
            "temp_min": temp_min,
            "temp_max": temp_max,
            "condition": condition,
            "humidity": humidity,
            "wind_speed": wind_speed,
        }
    except Exception:
        return None
