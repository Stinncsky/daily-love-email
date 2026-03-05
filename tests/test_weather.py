import unittest
from unittest.mock import patch, Mock
from src.weather import get_weather

class TestWeather(unittest.TestCase):
    @patch("src.weather.requests.get")
    def test_get_weather_success(self, mock_get):
        mock_resp = Mock()
        mock_resp.status_code = 200
        mock_resp.json.return_value = {
            "main": {"temp": 22.5, "humidity": 60},
            "weather": [{"description": "clear sky"}],
            "wind": {"speed": 4.2}
        }
        mock_get.return_value = mock_resp

        result = get_weather("Beijing", api_key="test")
        self.assertEqual(result, {
            "temperature": 22.5,
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

if __name__ == "__main__":
    unittest.main()
