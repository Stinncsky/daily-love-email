#!/usr/bin/env python3
"""
将 AMap_adcode_citycode.xlsx 转换为 JSON 格式
输出: data/city_codes.json
"""

import json
import sys
from pathlib import Path


def convert_excel_to_json():
    """将 Excel 转换为 JSON 格式"""
    try:
        import pandas as pd
    except ImportError:
        print("错误: 需要 pandas 来转换 Excel 文件")
        print("请运行: pip install pandas openpyxl")
        sys.exit(1)

    # 查找 Excel 文件
    excel_paths = [
        Path("AMap_adcode_citycode.xlsx"),
        Path(__file__).parent.parent / "AMap_adcode_citycode.xlsx",
    ]

    excel_path = None
    for path in excel_paths:
        if path.exists():
            excel_path = path
            break

    if not excel_path:
        print("错误: 找不到 AMap_adcode_citycode.xlsx 文件")
        sys.exit(1)

    print(f"读取 Excel 文件: {excel_path}")

    # 读取 Excel
    df = pd.read_excel(excel_path, header=0)

    # 确保至少有两列
    if len(df.columns) < 2:
        print("错误: Excel 文件列数不足")
        sys.exit(1)

    # 重命名列
    df.columns = ["name", "adcode"] + [f"col_{i}" for i in range(2, len(df.columns))]

    # 清理数据
    df = df.dropna(subset=["name", "adcode"])

    # 转换为列表
    cities = []
    for _, row in df.iterrows():
        try:
            name = str(row["name"]).strip()
            adcode = str(int(row["adcode"])).zfill(6)

            # 只保留 6 位数字的 adcode
            if len(adcode) != 6 or not adcode.isdigit():
                continue

            cities.append({"name": name, "adcode": adcode})
        except (ValueError, TypeError):
            continue

    print(f"共转换 {len(cities)} 个城市")

    # 输出 JSON
    data_dir = Path(__file__).parent.parent / "data"
    data_dir.mkdir(exist_ok=True)

    output_path = data_dir / "city_codes.json"

    # 写入 JSON 文件
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(cities, f, ensure_ascii=False, indent=2)

    print(f"已保存到: {output_path}")

    # 同时生成一个压缩版本（无缩进）供程序使用
    output_path_min = data_dir / "city_codes.min.json"
    with open(output_path_min, "w", encoding="utf-8") as f:
        json.dump(cities, f, ensure_ascii=False, separators=(",", ":"))

    print(f"已保存压缩版本: {output_path_min}")


if __name__ == "__main__":
    convert_excel_to_json()
