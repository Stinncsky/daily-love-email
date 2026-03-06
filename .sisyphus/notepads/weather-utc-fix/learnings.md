# Weather UTC fix - Learnings
- Updated src/weather.py to use UTC time for date calculations to avoid server timezone drift when querying OpenWeatherMap data (which is timestamped in UTC).
- Change summary:
  - Import timezone from datetime
  - Use datetime.now(timezone.utc).date() instead of datetime.now().date()
- Verification approach:
  - Ensure no syntax errors and that the code reads UTC date regardless of server TZ
  - Run existing weather-related tests to confirm no regressions
