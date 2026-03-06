import os
from pathlib import Path
import yaml


def _cast_leaf(val, env_val):
    """将环境变量字符串按照原始值类型进行简单转换后返回。"""
    # 布尔值处理
    if isinstance(val, bool):
        low = str(env_val).lower()
        if low in ("1", "true", "yes", "on"):
            return True
        if low in ("0", "false", "no", "off"):
            return False
        return val
    # 整数处理
    if isinstance(val, int):
        try:
            return int(env_val)
        except Exception:
            return val
    # 浮点数处理
    if isinstance(val, float):
        try:
            return float(env_val)
        except Exception:
            return val
    # 字符串及其他保持原样
    return env_val


def _override_env(config, path_parts=None):
    if path_parts is None:
        path_parts = []
    if isinstance(config, dict):
        for key, value in config.items():
            current_path = path_parts + [str(key)]
            if isinstance(value, dict):
                _override_env(value, current_path)
            else:
                env_key = "_".join([p.upper() for p in current_path])
                if env_key in os.environ:
                    env_val = os.environ[env_key]
                    # 如果原值是列表或字典类型，尝试将环境变量的 JSON 字符串解析为相同类型
                    if isinstance(value, (list, dict)):
                        try:
                            import json
                            parsed = json.loads(env_val)
                            if isinstance(parsed, type(value)):  # 类型必须匹配
                                config[key] = parsed
                            # 无论解析成功还是类型不匹配，都 continue 保留原值
                            continue
                        except Exception:
                            # 解析失败，保留原值
                            continue
                    # 其他情况走原有类型转换逻辑
                    config[key] = _cast_leaf(value, env_val)
    return config


def load_config(config_path: str = "config.yaml"):
    """从配置文件加载配置，并用环境变量覆盖（以大写下划线连接路径）"""
    cfg = {}
    p = Path(config_path)
    if p.exists():
        try:
            with p.open("r", encoding="utf-8") as f:
                data = yaml.safe_load(f) or {}
                if isinstance(data, dict):
                    cfg = data
                else:
                    cfg = {}
        except Exception:
            # 如果配置加载失败，仍应优雅地返回空配置
            cfg = {}
    # 环境变量覆盖，优先级高于文件配置
    cfg = _override_env(cfg)
    return cfg
