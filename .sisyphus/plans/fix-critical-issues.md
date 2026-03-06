# 修复 Critical 问题 + 时区/日志优化

## TL;DR

修复代码审查中发现的关键问题：
1. **dry_run 失效** - main.py 不读取 DRY_RUN 环境变量
2. **温度 0°C 处理错误** - `or` 逻辑将 0 视为 False
3. **Outlook VML 不兼容** - card_background_style 格式问题
4. **日志文案旧键名** - TO_EMAIL 未更新
5. **时区不匹配** - 使用服务器时区而非目标城市时区

---

## Work Objectives

### 核心目标
修复所有 Critical 问题，确保生产环境稳定运行。

### 具体交付物
- 修复后的 src/main.py
- 修复后的 src/weather.py
- 修复后的 src/background.py（或 template.py）
- 更新后的日志文案

### 必须完成
- [ ] dry_run 环境变量被正确读取
- [ ] 温度 0°C 正确显示为 0 而非 fallback 值
- [ ] Outlook 邮件背景图正常显示
- [ ] 日志使用正确的配置键名
- [ ] 天气数据使用目标城市时区

### 不处理（超出范围）
- Major 问题（forecast 降级、配置健壮性等）
- 其他可选优化（Base64 体积等）

---

## TODOs

### Wave 1: 核心修复（高优先级）

- [ ] 1. Fix dry_run 环境变量读取

  **问题**: 工作流设置 `DRY_RUN` 环境变量，但 main.py 只检查 CLI 参数 `--dry-run`
  
  **修复方案**:
  ```python
  # src/main.py 中修改 dry_run 判断逻辑
  # 当前: 仅从 args 读取
  # 修复: 优先从 args，其次从环境变量
  dry_run = args.dry_run or os.environ.get("DRY_RUN", "").lower() in ("true", "1", "yes")
  ```
  
  **参考位置**: src/main.py:164-168

- [ ] 2. Fix 温度 0°C 处理 bug

  **问题**: `main.get("temp_min") or temperature` 在 temp_min=0 时会错误回退
  
  **修复方案**:
  ```python
  # src/weather.py
  # 修复前:
  # temp_min = main.get("temp_min") or temperature
  # 修复后:
  temp_min = main.get("temp_min") if main.get("temp_min") is not None else temperature
  # 同理处理 temp_max
  ```
  
  **参考位置**: src/weather.py:69, 71

- [ ] 3. Fix Outlook VML 兼容性

  **问题**: `card_background_style` 返回 `url(data:...)` 格式，但 Outlook VML `<v:fill src="">` 需要裸 URL
  
  **修复方案**:
  方案 A - 修改 background.py:
  ```python
  # src/background.py 中 image 类型返回时去掉 url() 包装
  # 或提供两个版本：一个给 CSS 用，一个给 VML 用
  ```
  
  方案 B - 修改模板:
  ```html
  <!-- templates/email_new.html -->
  <!-- 使用过滤器或条件判断处理 url() 包装 -->
  <v:fill type="tile" src="{{ card_background_style|replace('url(', '')|replace(')', '') }}" />
  ```
  
  **参考位置**: templates/email_new.html:47, src/background.py

### Wave 2: 可选优化（中等优先级）

- [ ] 4. Fix 日志文案旧键名

  **问题**: 日志仍使用 `TO_EMAIL`，与新配置结构不一致
  
  **修复方案**:
  ```python
  # src/main.py:206
  # 修复前: "TO_EMAIL": config.get("recipient")
  # 修复后: "recipient": config.get("recipient")
  # 或根据新的嵌套结构: config.get("email", {}).get("recipient")
  ```
  
  **参考位置**: src/main.py:206

- [ ] 5. Fix 时区不匹配

  **问题**: weather.py 使用 `datetime.now().date()`（服务器时区），应使用目标城市时区
  
  **修复方案**:
  ```python
  # src/weather.py
  from datetime import datetime
  import pytz
  
  # 修复前:
  # today = datetime.now().date()
  
  # 修复后:
  city_timezone = pytz.timezone(get_city_timezone(city))  # 需要城市到时的映射
  today = datetime.now(city_timezone).date()
  ```
  
  **替代方案**（更简单）:
  ```python
  # 使用 UTC 时间，或接受当前行为作为已知限制
  # 在文档中说明：服务器时区应与目标城市时区一致
  ```
  
  **参考位置**: src/weather.py:34

### Wave 3: 验证

- [ ] 6. 运行测试验证修复

  **验证项**:
  - [ ] `pytest tests/test_weather.py -v` 通过
  - [ ] 手动测试: 设置 DRY_RUN=true 环境变量，验证不会发送邮件
  - [ ] 手动测试: 模拟 temp_min=0 的天气数据，验证显示 0°C 而非 fallback
  - [ ] 检查日志输出，确认键名正确

---

## Execution Strategy

### 依赖关系
```
Task 1 (dry_run) ──┐
Task 2 (温度) ──────┼──→ Task 6 (验证)
Task 3 (VML) ──────┤
Task 4 (日志) ─────┤
Task 5 (时区) ─────┘
```

### 并行策略
- Wave 1 的任务 1-3 可以并行开发
- Wave 2 的任务 4-5 可以并行开发
- Task 6 必须在所有修复完成后执行

---

## Success Criteria

### 验收标准
1. **dry_run**: 设置环境变量 DRY_RUN=true，运行脚本，确认不发送邮件
2. **温度 0°C**: 构造测试数据 `{"temp_min": 0, "temp_max": 5}`，验证显示 "0° / 5°" 而非 fallback 值
3. **VML**: 在 Outlook 中打开邮件，背景图片正常显示
4. **日志**: 日志输出使用正确的键名，无 TO_EMAIL
5. **时区**: 日志中显示的天气数据日期与目标城市当前日期一致

### 测试命令
```bash
# 运行所有测试
pytest tests/ -v

# 特定测试
pytest tests/test_weather.py -v
pytest tests/test_main.py -v  # 如果有

# 干运行测试
DRY_RUN=true python src/main.py
```

---

## Notes

### 关于时区修复的注意事项
- 完整的城市时区映射较复杂，可考虑使用 `pytz` + 城市坐标
- 简化方案：在 README 中说明服务器时区应与目标城市时区保持一致
- 如果采用简化方案，Task 5 只需更新文档而非代码

### 关于 VML 修复的注意事项
- VML 仅用于旧版 Outlook（Windows 桌面版）
- 修复时需确保不影响现代邮件客户端（使用 CSS 的版本）
- 建议提供两个变量：`card_background_style_css` 和 `card_background_style_vml`
