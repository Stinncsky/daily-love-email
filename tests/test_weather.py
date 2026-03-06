import unittest
from unittest.mock import patch, Mock
from src.weather import get_weather


class TestWeather(unittest.TestCase):
    @patch("src.weather.requests.get")
    def test_get_weather_success(self, mock_get):
        mock_resp = Mock()
        mock_resp.status_code = 200
        mock_resp.json.return_value = {
            "main": {"temp": 22.5, "humidity": 60, "temp_min": 20.5, "temp_max": 24.5},
            "weather": [{"description": "clear sky"}],
            "wind": {"speed": 4.2}
        }
        mock_get.return_value = mock_resp

        result = get_weather("Beijing", api_key="test")
        self.assertEqual(result, {
            "temperature": 22.5,
            "temp_min": 20.5,
            "temp_max": 24.5,
            "condition": "clear sky",
            "humidity": 60,
            "wind_speed": 4.2
        })

    @patch("src.weather.requests.get")
    def test_get_weather_api_error(self, mock_get):
        mock_resp = Mock()
        mock_resp.status_code = 500
        mock_get.return_value = mock_resp
        result = get_weather("Beijing", api_key="test")
        self.assertIsNone(result)

    @patch("src.weather.requests.get")
    def test_get_weather_missing_fields(self, mock_get):
        mock_resp = Mock()
        mock_resp.status_code = 200
        mock_resp.json.return_value = {"main": {"temp": 20}}
        mock_get.return_value = mock_resp
        result = get_weather("Beijing", api_key="test")
        self.assertIsNone(result)


class TestWeatherDirtyData(unittest.TestCase):
    @patch("src.weather.requests.get")
    def test_weather_empty_weather_list(self, mock_get):
        mock_resp = Mock()
        mock_resp.status_code = 200
        mock_resp.json.return_value = {
            "main": {"temp": 22.5, "humidity": 60},
            "weather": [],
            "wind": {"speed": 4.2}
        }
        mock_get.return_value = mock_resp

        result = get_weather("Beijing", api_key="test")
        self.assertIsNone(result)

    @patch("src.weather.requests.get")
    def test_weather_weather_list_not_list(self, mock_get):
        mock_resp = Mock()
        mock_resp.status_code = 200
        mock_resp.json.return_value = {
            "main": {"temp": 22.5, "humidity": 60},
            "weather": {"description": "clear sky"},
            "wind": {"speed": 4.2}
        }
        mock_get.return_value = mock_resp

        result = get_weather("Beijing", api_key="test")
        self.assertIsNone(result)

    @patch("src.weather.requests.get")
    def test_weather_missing_main_key(self, mock_get):
        mock_resp = Mock()
        mock_resp.status_code = 200
        mock_resp.json.return_value = {
            "weather": [{"description": "clear sky"}],
            "wind": {"speed": 4.2}
        }
        mock_get.return_value = mock_resp

        result = get_weather("Beijing", api_key="test")
        self.assertIsNone(result)

    @patch("src.weather.requests.get")
    def test_weather_missing_wind_key(self, mock_get):
        mock_resp = Mock()
        mock_resp.status_code = 200
        mock_resp.json.return_value = {
            "main": {"temp": 22.5, "humidity": 60},
            "weather": [{"description": "clear sky"}]
        }
        mock_get.return_value = mock_resp

        result = get_weather("Beijing", api_key="test")
        self.assertIsNone(result)

    @patch("src.weather.requests.get")
    def test_weather_null_values(self, mock_get):
        mock_resp = Mock()
        mock_resp.status_code = 200
        mock_resp.json.return_value = {
            "main": {"temp": None, "humidity": None},
            "weather": [{"description": None}],
            "wind": {"speed": None}
        }
        mock_get.return_value = mock_resp

        result = get_weather("Beijing", api_key="test")
        self.assertIsNone(result)

    @patch("src.weather.requests.get")
    def test_weather_weather_item_missing_description(self, mock_get):
        mock_resp = Mock()
        mock_resp.status_code = 200
        mock_resp.json.return_value = {
            "main": {"temp": 22.5, "humidity": 60},
            "weather": [{"icon": "01d"}],
            "wind": {"speed": 4.2}
        }
        mock_get.return_value = mock_resp

        result = get_weather("Beijing", api_key="test")
        self.assertIsNone(result)

    @patch("src.weather.requests.get")
    def test_weather_empty_response(self, mock_get):
        mock_resp = Mock()
        mock_resp.status_code = 200
        mock_resp.json.return_value = {}
        mock_get.return_value = mock_resp

        result = get_weather("Beijing", api_key="test")
        self.assertIsNone(result)

    @patch("src.weather.requests.get")
    def test_weather_wind_missing_speed(self, mock_get):
        mock_resp = Mock()
        mock_resp.status_code = 200
        mock_resp.json.return_value = {
            "main": {"temp": 22.5, "humidity": 60},
            "weather": [{"description": "clear sky"}],
            "wind": {"deg": 180}
        }
        mock_get.return_value = mock_resp

        result = get_weather("Beijing", api_key="test")
        self.assertIsNone(result)

    @patch("src.weather.requests.get")
    def test_weather_main_missing_temp(self, mock_get):
        mock_resp = Mock()
        mock_resp.status_code = 200
        mock_resp.json.return_value = {
            "main": {"humidity": 60, "pressure": 1013},
            "weather": [{"description": "clear sky"}],
            "wind": {"speed": 4.2}
        }
        mock_get.return_value = mock_resp

        result = get_weather("Beijing", api_key="test")
        self.assertIsNone(result)

    @patch("src.weather.requests.get")
    def test_weather_main_missing_humidity(self, mock_get):
        mock_resp = Mock()
        mock_resp.status_code = 200
        mock_resp.json.return_value = {
            "main": {"temp": 22.5, "pressure": 1013},
            "weather": [{"description": "clear sky"}],
            "wind": {"speed": 4.2}
        }
        mock_get.return_value = mock_resp

        result = get_weather("Beijing", api_key="test")
        self.assertIsNone(result)

    @patch("src.weather.requests.get")
    def test_weather_with_forecast_fallback(self, mock_get):
        from datetime import datetime, timezone

        def mock_side_effect(url, **kwargs):
            mock_resp = Mock()
            if "forecast" in url:
                mock_resp.status_code = 200
                today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
                mock_resp.json.return_value = {
                    "list": [
                        {
                            "dt_txt": f"{today} 12:00:00",
                            "main": {"temp": 18.0}
                        },
                        {
                            "dt_txt": f"{today} 15:00:00",
                            "main": {"temp": 22.0}
                        }
                    ]
                }
            else:
                mock_resp.status_code = 200
                mock_resp.json.return_value = {
                    "main": {"temp": 20.0, "humidity": 60},
                    "weather": [{"description": "clear sky"}],
                    "wind": {"speed": 4.2}
                }
            return mock_resp

        mock_get.side_effect = mock_side_effect

        result = get_weather("Beijing", api_key="test")
        self.assertIsNotNone(result)
        self.assertEqual(result["temp_min"], 18.0)
        self.assertEqual(result["temp_max"], 22.0)


if __name__ == "__main__":
    unittest.main()
