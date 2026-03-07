"""
城市编码模块 - 将城市名称转换为高德地图 adcode
使用 JSON 数据文件，无需 pandas 依赖
"""

import json
import logging
from functools import lru_cache
from pathlib import Path
from typing import Dict, List, Optional, Tuple

# 配置模块日志
logger = logging.getLogger(__name__)


# 内置常用城市 fallback 数据（当 JSON 文件无法读取时使用）
FALLBACK_CITY_CODES: Dict[str, str] = {
    "北京市": "110000",
    "北京": "110000",
    "上海市": "310000",
    "上海": "310000",
    "广州市": "440100",
    "广州": "440100",
    "深圳市": "440300",
    "深圳": "440300",
    "杭州市": "330100",
    "杭州": "330100",
    "南京市": "320100",
    "南京": "320100",
    "成都市": "510100",
    "成都": "510100",
    "武汉市": "420100",
    "武汉": "420100",
    "西安市": "610100",
    "西安": "610100",
    "重庆市": "500000",
    "重庆": "500000",
    "天津市": "120000",
    "天津": "120000",
    "苏州市": "320500",
    "苏州": "320500",
    "郑州市": "410100",
    "郑州": "410100",
    "长沙市": "430100",
    "长沙": "430100",
    "沈阳市": "210100",
    "沈阳": "210100",
    "青岛市": "370200",
    "青岛": "370200",
    "宁波市": "330200",
    "宁波": "330200",
    "东莞市": "441900",
    "东莞": "441900",
    "佛山市": "440600",
    "佛山": "440600",
    "石家庄市": "130100",
    "石家庄": "130100",
    "太原市": "140100",
    "太原": "140100",
    "济南市": "370100",
    "济南": "370100",
    "哈尔滨市": "230100",
    "哈尔滨": "230100",
    "长春市": "220100",
    "长春": "220100",
    "大连市": "210200",
    "大连": "210200",
    "厦门市": "350200",
    "厦门": "350200",
    "福州市": "350100",
    "福州": "350100",
    "昆明市": "530100",
    "昆明": "530100",
    "合肥市": "340100",
    "合肥": "340100",
    "南昌市": "360100",
    "南昌": "360100",
    "贵阳市": "520100",
    "贵阳": "520100",
    "南宁市": "450100",
    "南宁": "450100",
    "海口市": "460100",
    "海口": "460100",
    "兰州市": "620100",
    "兰州": "620100",
    "银川市": "640100",
    "银川": "640100",
    "西宁市": "630100",
    "西宁": "630100",
    "乌鲁木齐市": "650100",
    "乌鲁木齐": "650100",
    "拉萨市": "540100",
    "拉萨": "540100",
    "呼和浩特市": "150100",
    "呼和浩特": "150100",
}


def _normalize_city_name(name: str) -> str:
    """标准化城市名称（去除空格，统一大小写）"""
    return name.strip().replace(" ", "")


def _get_short_name(full_name: str) -> str:
    """获取城市短名称（去除'市'、'省'、'自治区'后缀）"""
    suffixes = ["市", "省", "自治区", "特别行政区", "地区", "盟", "自治州"]
    short = full_name
    for suffix in suffixes:
        if short.endswith(suffix):
            short = short[: -len(suffix)]
            break
    return short


def _get_json_paths() -> List[Path]:
    """获取可能的 JSON 文件路径列表"""
    return [
        # 当前工作目录下的 data
        Path("data") / "city_codes.json",
        # 相对于 src 目录的 data
        Path(__file__).parent.parent / "data" / "city_codes.json",
        # 相对于本文件的 data
        Path(__file__).parent / ".." / "data" / "city_codes.json",
    ]


@lru_cache(maxsize=1)
def _load_city_data() -> Tuple[Dict[str, str], Dict[str, str]]:
    """
    加载城市编码数据，返回 (完整名称映射, 短名称映射)
    使用 LRU 缓存避免重复读取文件
    """
    full_name_map: Dict[str, str] = {}
    short_name_map: Dict[str, str] = {}

    # 首先加载 fallback 数据作为基础
    for name, code in FALLBACK_CITY_CODES.items():
        normalized = _normalize_city_name(name)
        if normalized:
            full_name_map[normalized] = code

    # 尝试读取 JSON 文件
    json_loaded = False
    for json_path in _get_json_paths():
        if not json_path.exists():
            continue

        try:
            with open(json_path, "r", encoding="utf-8") as f:
                cities = json.load(f)

            if not isinstance(cities, list):
                logger.warning("Invalid JSON format in %s: expected list", json_path)
                continue

            loaded_count = 0
            for city in cities:
                if not isinstance(city, dict):
                    continue

                name = city.get("name", "").strip()
                adcode = str(city.get("adcode", "")).strip().zfill(6)

                # 验证 adcode 格式
                if len(adcode) != 6 or not adcode.isdigit():
                    continue

                # 完整名称映射（JSON 数据优先级高于 fallback）
                normalized = _normalize_city_name(name)
                if normalized:
                    full_name_map[normalized] = adcode
                    loaded_count += 1

                # 短名称映射
                short_name = _get_short_name(name)
                normalized_short = _normalize_city_name(short_name)
                if normalized_short:
                    short_name_map[normalized_short] = adcode

            if loaded_count > 0:
                logger.info("Loaded %d cities from %s", loaded_count, json_path)
                json_loaded = True
                break  # 成功读取后跳出循环

        except json.JSONDecodeError as e:
            logger.error("Failed to parse JSON file %s: %s", json_path, e)
            continue
        except FileNotFoundError:
            logger.debug("JSON file not found: %s", json_path)
            continue
        except Exception as e:
            logger.error("Unexpected error loading %s: %s", json_path, e)
            continue

    if not json_loaded:
        logger.warning("Could not load JSON data, using fallback city codes only (%d cities)",
                      len(full_name_map))

    return full_name_map, short_name_map


def get_adcode(city_name: str) -> Optional[str]:
    """
    将城市名称转换为高德 adcode (6位数字)

    匹配策略（优先级）：
    1. 精确匹配完整名称（如"北京市"）
    2. 精确匹配短名称（如"北京"）
    3. 自动添加/去除"市"后缀匹配

    Args:
        city_name: 城市名称（如"北京市"、"北京"、"上海"）

    Returns:
        6位数字 adcode 字符串，找不到则返回 None

    Examples:
        >>> get_adcode("北京市")
        "110000"
        >>> get_adcode("北京")
        "110000"
        >>> get_adcode("上海")
        "310000"
    """
    if not city_name or not isinstance(city_name, str):
        return None

    normalized = _normalize_city_name(city_name)
    if not normalized:
        return None

    full_map, short_map = _load_city_data()

    # 1. 精确匹配完整名称
    if normalized in full_map:
        return full_map[normalized]

    # 2. 精确匹配短名称
    if normalized in short_map:
        return short_map[normalized]

    # 3. 尝试添加/去除"市"后缀
    if not normalized.endswith("市"):
        with_suffix = normalized + "市"
        if with_suffix in full_map:
            return full_map[with_suffix]
    else:
        without_suffix = normalized[:-1]
        if without_suffix in short_map:
            return short_map[without_suffix]

    # 4. 尝试添加/去除"省"后缀
    if not normalized.endswith("省"):
        with_suffix = normalized + "省"
        if with_suffix in full_map:
            return full_map[with_suffix]
    else:
        without_suffix = normalized[:-1]
        if without_suffix in short_map:
            return short_map[without_suffix]

    logger.debug("City not found: %s", city_name)
    return None


def search_cities(keyword: str) -> List[Dict[str, str]]:
    """
    根据关键词搜索城市

    Args:
        keyword: 搜索关键词

    Returns:
        匹配的城市列表，每项包含 name 和 adcode
    """
    if not keyword or not isinstance(keyword, str):
        return []

    normalized = _normalize_city_name(keyword)
    full_map, short_map = _load_city_data()

    results = []
    seen_codes = set()

    # 合并两个映射进行搜索
    all_mappings = {**full_map, **short_map}

    for name, adcode in all_mappings.items():
        if normalized in name:
            if adcode not in seen_codes:
                seen_codes.add(adcode)
                results.append({"name": name, "adcode": adcode})

    return results[:10]  # 最多返回10个结果


def clear_cache() -> None:
    """清除城市数据缓存（用于测试或数据更新后）"""
    _load_city_data.cache_clear()
