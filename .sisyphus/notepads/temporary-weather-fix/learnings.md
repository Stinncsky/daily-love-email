已完成：修复 weather.py 中温度回退逻辑的 bug。
- 变更要点：将原本使用 "main.get(\"temp_min\") or temperature" 的逻辑，改为显式判断是否为 None，以正确保留 0 值。
- 影响范围：src/weather.py 第68-72行，涉及 temp_min 与 temp_max 的默认赋值。
- 验证要点：当输入数据为 {"temp_min": 0, "temp_max": 5} 时，输出应为 "0° / 5°"，而不是回退到温度值。
- 风险与 Notes：无其他行为更改，保持函数签名与返回值类型不变。
