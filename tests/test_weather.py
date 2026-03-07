"""
天气模块测试 - 高德地图天气API适配器测试
"""

import unittest
from unittest.mock import patch, Mock

from src.weather import get_weather, _parse_wind_power


class TestWindPowerParser(unittest.TestCase):
    """测试风力解析函数"""

    def test_single_level(self):
        """测试单一级别的风力"""
        self.assertEqual(_parse_wind_power("3级"), 4.5)
        self.assertEqual(_parse_wind_power("1级"), 1.5)
        self.assertEqual(_parse_wind_power("10级"), 15.0)

    def test_range_level(self):
        """测试范围级别的风力"""
        self.assertEqual(_parse_wind_power("4-5级"), 6.8)  # (4+5)/2 * 1.5 = 6.75 -> round to 6.8
        self.assertEqual(_parse_wind_power("1-2级"), 2.2)  # (1+2)/2 * 1.5 = 2.25 -> round to 2.2

    def test_special_characters(self):
        """测试特殊字符"""
        self.assertEqual(_parse_wind_power("<3级"), 4.5)
        self.assertEqual(_parse_wind_power(">8级"), 12.0)
        # 测试 ≤ ≥ 符号（高德API实际返回格式）
        self.assertEqual(_parse_wind_power("≤3级"), 4.5)
        self.assertEqual(_parse_wind_power("≥5级"), 7.5)

    def test_empty_and_invalid(self):
        """测试空值和无效值"""
        self.assertEqual(_parse_wind_power(""), 0.0)
        self.assertEqual(_parse_wind_power(None), 0.0)
        self.assertEqual(_parse_wind_power("invalid"), 0.0)


class TestGetWeather(unittest.TestCase):
    """测试获取天气函数"""

    @patch("src.weather._fetch_forecast_weather")
    @patch("src.weather._fetch_live_weather")
    @patch("src.weather.get_adcode")
    def test_get_weather_success(self, mock_get_adcode, mock_live, mock_forecast):
        """测试成功获取天气数据"""
        mock_get_adcode.return_value = "110000"
        mock_live.return_value = {
            "temperature": 22.0,
            "condition": "晴",
            "humidity": 45.0,
            "wind_speed": 4.5,
        }
        mock_forecast.return_value = {
            "temp_min": 18.0,
            "temp_max": 26.0,
        }

        result = get_weather("北京市", api_key="test_key")

        self.assertIsNotNone(result)
        self.assertEqual(result["temperature"], 22.0)
        self.assertEqual(result["temp_min"], 18.0)
        self.assertEqual(result["temp_max"], 26.0)
        self.assertEqual(result["condition"], "晴")
        self.assertEqual(result["humidity"], 45.0)
        self.assertEqual(result["wind_speed"], 4.5)

    @patch("src.weather._fetch_forecast_weather")
    @patch("src.weather._fetch_live_weather")
    @patch("src.weather.get_adcode")
    def test_get_weather_forecast_fallback(self, mock_get_adcode, mock_live, mock_forecast):
        """测试预报API失败时的降级处理"""
        mock_get_adcode.return_value = "110000"
        mock_live.return_value = {
            "temperature": 22.0,
            "condition": "多云",
            "humidity": 50.0,
            "wind_speed": 3.0,
        }
        mock_forecast.return_value = None  # 预报API失败

        result = get_weather("北京", api_key="test_key")

        self.assertIsNotNone(result)
        self.assertEqual(result["temperature"], 22.0)
        self.assertEqual(result["temp_min"], 22.0)  # 使用实时温度作为min
        self.assertEqual(result["temp_max"], 22.0)  # 使用实时温度作为max

    @patch("src.weather.get_adcode")
    def test_get_weather_city_not_found(self, mock_get_adcode):
        """测试城市编码找不到的情况"""
        mock_get_adcode.return_value = None

        result = get_weather("不存在的城市", api_key="test_key")

        self.assertIsNone(result)

    @patch("src.weather._fetch_live_weather")
    @patch("src.weather.get_adcode")
    def test_get_weather_live_api_failure(self, mock_get_adcode, mock_live):
        """测试实况API失败的情况"""
        mock_get_adcode.return_value = "110000"
        mock_live.return_value = None  # 实况API失败

        result = get_weather("北京市", api_key="test_key")

        self.assertIsNone(result)

    def test_get_weather_no_api_key(self):
        """测试没有API Key的情况"""
        result = get_weather("北京市", api_key=None)
        self.assertIsNone(result)


class TestFetchLiveWeather(unittest.TestCase):
    """测试实况天气获取"""

    @patch("src.weather.requests.get")
    def test_fetch_live_success(self, mock_get):
        """测试成功获取实况天气"""
        from src.weather import _fetch_live_weather

        mock_resp = Mock()
        mock_resp.status_code = 200
        mock_resp.json.return_value = {
            "status": "1",
            "lives": [
                {
                    "temperature": "22",
                    "weather": "晴",
                    "humidity": "45",
                    "windpower": "3级",
                }
            ],
        }
        mock_get.return_value = mock_resp

        result = _fetch_live_weather("110000", "test_key")

        self.assertIsNotNone(result)
        self.assertEqual(result["temperature"], 22.0)
        self.assertEqual(result["condition"], "晴")
        self.assertEqual(result["humidity"], 45.0)
        self.assertEqual(result["wind_speed"], 4.5)

    @patch("src.weather.requests.get")
    def test_fetch_live_api_error(self, mock_get):
        """测试API返回错误状态"""
        from src.weather import _fetch_live_weather

        mock_resp = Mock()
        mock_resp.status_code = 200
        mock_resp.json.return_value = {"status": "0", "info": "INVALID_KEY"}
        mock_get.return_value = mock_resp

        result = _fetch_live_weather("110000", "test_key")

        self.assertIsNone(result)

    @patch("src.weather.requests.get")
    def test_fetch_live_empty_lives(self, mock_get):
        """测试空lives数组"""
        from src.weather import _fetch_live_weather

        mock_resp = Mock()
        mock_resp.status_code = 200
        mock_resp.json.return_value = {"status": "1", "lives": []}
        mock_get.return_value = mock_resp

        result = _fetch_live_weather("110000", "test_key")

        self.assertIsNone(result)

    @patch("src.weather.requests.get")
    def test_fetch_live_http_error(self, mock_get):
        """测试HTTP请求错误"""
        import requests
        from src.weather import _fetch_live_weather

        mock_get.side_effect = requests.RequestException("Connection timeout")

        result = _fetch_live_weather("110000", "test_key")

        self.assertIsNone(result)


class TestFetchForecastWeather(unittest.TestCase):
    """测试预报天气获取"""

    @patch("src.weather.requests.get")
    def test_fetch_forecast_success(self, mock_get):
        """测试成功获取预报天气"""
        from src.weather import _fetch_forecast_weather

        mock_resp = Mock()
        mock_resp.status_code = 200
        mock_resp.json.return_value = {
            "status": "1",
            "forecasts": [
                {
                    "casts": [
                        {
                            "daytemp": "26",
                            "nighttemp": "18",
                        }
                    ]
                }
            ],
        }
        mock_get.return_value = mock_resp

        result = _fetch_forecast_weather("110000", "test_key")

        self.assertIsNotNone(result)
        self.assertEqual(result["temp_min"], 18.0)
        self.assertEqual(result["temp_max"], 26.0)

    @patch("src.weather.requests.get")
    def test_fetch_forecast_api_error(self, mock_get):
        """测试API返回错误状态"""
        from src.weather import _fetch_forecast_weather

        mock_resp = Mock()
        mock_resp.status_code = 200
        mock_resp.json.return_value = {"status": "0", "info": "INVALID_PARAMS"}
        mock_get.return_value = mock_resp

        result = _fetch_forecast_weather("110000", "test_key")

        self.assertIsNone(result)

    @patch("src.weather.requests.get")
    def test_fetch_forecast_empty_forecasts(self, mock_get):
        """测试空forecasts数组"""
        from src.weather import _fetch_forecast_weather

        mock_resp = Mock()
        mock_resp.status_code = 200
        mock_resp.json.return_value = {"status": "1", "forecasts": []}
        mock_get.return_value = mock_resp

        result = _fetch_forecast_weather("110000", "test_key")

        self.assertIsNone(result)


class TestWeatherIntegration(unittest.TestCase):
    """集成测试 - 模拟完整的高德API响应"""

    @patch("src.weather.requests.get")
    @patch("src.weather.get_adcode")
    def test_full_flow_with_real_response_format(self, mock_get_adcode, mock_get):
        """测试使用真实高德API响应格式的完整流程"""
        mock_get_adcode.return_value = "310000"

        def mock_side_effect(url, **kwargs):
            mock_resp = Mock()
            mock_resp.status_code = 200
            params = kwargs.get("params", {})
            extensions = params.get("extensions", "")

            if extensions == "base":
                # 实况天气响应
                mock_resp.json.return_value = {
                    "status": "1",
                    "count": "1",
                    "info": "OK",
                    "infocode": "10000",
                    "lives": [
                        {
                            "province": "上海",
                            "city": "上海市",
                            "adcode": "310000",
                            "weather": "多云",
                            "temperature": "24",
                            "winddirection": "东南",
                            "windpower": "≤3",
                            "humidity": "65",
                            "reporttime": "2024-01-01 14:30:00",
                        }
                    ],
                }
            else:
                # 预报天气响应
                mock_resp.json.return_value = {
                    "status": "1",
                    "count": "1",
                    "info": "OK",
                    "infocode": "10000",
                    "forecasts": [
                        {
                            "city": "上海市",
                            "adcode": "310000",
                            "province": "上海",
                            "reporttime": "2024-01-01 14:30:00",
                            "casts": [
                                {
                                    "date": "2024-01-01",
                                    "week": "1",
                                    "dayweather": "多云",
                                    "nightweather": "晴",
                                    "daytemp": "26",
                                    "nighttemp": "18",
                                    "daywind": "东南",
                                    "nightwind": "南",
                                    "daypower": "4",
                                    "nightpower": "3",
                                }
                            ],
                        }
                    ],
                }
            return mock_resp

        mock_get.side_effect = mock_side_effect

        result = get_weather("上海", api_key="test_key")

        self.assertIsNotNone(result)
        self.assertEqual(result["temperature"], 24.0)
        self.assertEqual(result["temp_min"], 18.0)
        self.assertEqual(result["temp_max"], 26.0)
        self.assertEqual(result["condition"], "多云")
        self.assertEqual(result["humidity"], 65.0)
        # 验证 wind_speed 被正确解析（≤3级 -> 4.5 m/s）
        self.assertEqual(result["wind_speed"], 4.5)


if __name__ == "__main__":
    unittest.main()
