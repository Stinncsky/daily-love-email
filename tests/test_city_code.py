"""
城市编码模块测试 - 测试城市名称到 adcode 的映射功能
"""

import unittest
from pathlib import Path
from unittest.mock import patch, mock_open

from src.city_code import (
    get_adcode,
    search_cities,
    clear_cache,
    _normalize_city_name,
    _get_short_name,
    FALLBACK_CITY_CODES,
)


class TestNormalizeCityName(unittest.TestCase):
    """测试城市名称标准化"""

    def test_basic_normalization(self):
        """测试基本标准化"""
        self.assertEqual(_normalize_city_name(" 北京市 "), "北京市")
        self.assertEqual(_normalize_city_name("北京"), "北京")
        self.assertEqual(_normalize_city_name("  上海  "), "上海")

    def test_remove_spaces(self):
        """测试去除中间空格"""
        self.assertEqual(_normalize_city_name("北 京 市"), "北京市")
        self.assertEqual(_normalize_city_name("上 海"), "上海")


class TestGetShortName(unittest.TestCase):
    """测试获取城市短名称"""

    def test_remove_shi_suffix(self):
        """测试去除'市'后缀"""
        self.assertEqual(_get_short_name("北京市"), "北京")
        self.assertEqual(_get_short_name("上海市"), "上海")

    def test_remove_sheng_suffix(self):
        """测试去除'省'后缀"""
        self.assertEqual(_get_short_name("广东省"), "广东")
        self.assertEqual(_get_short_name("江苏省"), "江苏")

    def test_remove_zizhiqu_suffix(self):
        """测试去除'自治区'后缀"""
        # 注意：后缀按顺序匹配，"广西壮族自治区"会先匹配"自治区"变成"广西壮族"
        # 如果需要进一步处理，需要多次调用或使用其他方式
        self.assertEqual(_get_short_name("广西壮族自治区"), "广西壮族")
        self.assertEqual(_get_short_name("内蒙古自治区"), "内蒙古")

    def test_no_suffix(self):
        """测试无后缀的城市名"""
        self.assertEqual(_get_short_name("北京"), "北京")
        self.assertEqual(_get_short_name("香港"), "香港")


class TestGetAdcode(unittest.TestCase):
    """测试获取城市编码"""

    def setUp(self):
        """每个测试前清除缓存"""
        clear_cache()

    def test_fallback_beijing_full(self):
        """测试Fallback数据 - 北京完整名"""
        result = get_adcode("北京市")
        self.assertEqual(result, "110000")

    def test_fallback_beijing_short(self):
        """测试Fallback数据 - 北京短名"""
        result = get_adcode("北京")
        self.assertEqual(result, "110000")

    def test_fallback_shanghai(self):
        """测试Fallback数据 - 上海"""
        result = get_adcode("上海市")
        self.assertEqual(result, "310000")
        result = get_adcode("上海")
        self.assertEqual(result, "310000")

    def test_fallback_guangzhou(self):
        """测试Fallback数据 - 广州"""
        result = get_adcode("广州市")
        self.assertEqual(result, "440100")
        result = get_adcode("广州")
        self.assertEqual(result, "440100")

    def test_add_shi_suffix(self):
        """测试自动添加'市'后缀"""
        # 输入"北京"应该匹配到fallback中的"北京"或"北京市"
        result = get_adcode("北京")
        self.assertEqual(result, "110000")

    def test_remove_shi_suffix(self):
        """测试自动去除'市'后缀"""
        # 如果数据中只有短名，输入完整名应该能匹配
        # fallback中有"北京市"和"北京"，都能匹配到110000
        result = get_adcode("北京市")
        self.assertEqual(result, "110000")

    def test_invalid_city(self):
        """测试无效城市"""
        result = get_adcode("不存在的城市")
        self.assertIsNone(result)

    def test_empty_string(self):
        """测试空字符串"""
        result = get_adcode("")
        self.assertIsNone(result)

    def test_none_input(self):
        """测试None输入"""
        result = get_adcode(None)
        self.assertIsNone(result)

    def test_whitespace_only(self):
        """测试仅空白字符"""
        result = get_adcode("   ")
        self.assertIsNone(result)

    @patch("src.city_code.json.load")
    @patch("builtins.open")
    def test_json_loading(self, mock_open, mock_json_load):
        """测试从 JSON 加载数据"""
        # 模拟 JSON 数据
        mock_json_load.return_value = [
            {"name": "测试市", "adcode": "110100"},
            {"name": "示例市", "adcode": "120100"},
            {"name": "demo区", "adcode": "130101"},
        ]

        clear_cache()
        result = get_adcode("测试市")
        self.assertEqual(result, "110100")

        result = get_adcode("示例")
        self.assertEqual(result, "120100")


class TestSearchCities(unittest.TestCase):
    """测试城市搜索功能"""

    def setUp(self):
        clear_cache()

    def test_search_by_keyword(self):
        """测试关键词搜索"""
        results = search_cities("北京")
        self.assertGreater(len(results), 0)
        # 检查结果中是否包含北京的adcode
        codes = [r["adcode"] for r in results]
        self.assertIn("110000", codes)

    def test_search_empty_keyword(self):
        """测试空关键词搜索"""
        results = search_cities("")
        self.assertEqual(len(results), 0)

    def test_search_none_keyword(self):
        """测试None关键词搜索"""
        results = search_cities(None)
        self.assertEqual(len(results), 0)

    def test_search_limit(self):
        """测试结果数量限制"""
        # 搜索一个常见的字，应该返回最多10个结果
        results = search_cities("市")
        self.assertLessEqual(len(results), 10)


class TestClearCache(unittest.TestCase):
    """测试缓存清除功能"""

    def test_clear_cache(self):
        """测试清除缓存"""
        # 先调用一次以填充缓存
        get_adcode("北京")
        # 清除缓存
        clear_cache()
        # 再次调用应该正常工作
        result = get_adcode("北京")
        self.assertEqual(result, "110000")


class TestFallbackData(unittest.TestCase):
    """测试Fallback数据完整性"""

    def test_fallback_has_major_cities(self):
        """测试Fallback包含主要城市"""
        major_cities = ["北京", "上海", "广州", "深圳", "杭州", "南京"]
        for city in major_cities:
            self.assertIn(city, FALLBACK_CITY_CODES)

    def test_fallback_codes_are_valid(self):
        """测试Fallback中的编码格式正确"""
        for code in FALLBACK_CITY_CODES.values():
            self.assertEqual(len(code), 6)
            self.assertTrue(code.isdigit())


if __name__ == "__main__":
    unittest.main()
