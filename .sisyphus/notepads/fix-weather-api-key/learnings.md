# Learnings from fix-weather-api-key

- Task: Make weather API key lookup support both WEATHER_API_KEY and OPENWEATHER_API_KEY with WEATHER_API_KEY taking priority.
- Approach: Update src/weather.py line where key is determined from api_key or environment variables.
- Result: Code now checks WEATHER_API_KEY first, then OPENWEATHER_API_KEY as fallback, preserving existing behavior and enabling GitHub Actions' WEATHER_API_KEY secret.
- Verification notes: Local run will use WEATHER_API_KEY if set; if not, it will fall back to OPENWEATHER_API_KEY; if neither, get_weather returns None as before.
- Plan discipline: Append learnings to this file to preserve minimal history of changes for this plan.
