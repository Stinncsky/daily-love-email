# Fix Critical Issues - 学习笔记

## 2026-03-06 初始化

### 项目结构
- Python 每日恋爱邮件项目
- 关键文件: src/main.py, src/weather.py, src/background.py
- 模板: templates/email_new.html

### 发现的问题

#### Task 1: dry_run 环境变量
- 位置: src/main.py:168
- 当前: `dry_run = bool(args.dry_run)` 只检查 CLI 参数
- 修复: 需要同时检查 `DRY_RUN` 环境变量

#### Task 2: 温度 0°C 处理
- 位置: src/weather.py:69, 71
- 当前: `temp_min = main.get("temp_min") or temperature`
- 问题: Python 中 `0 or temperature` 会返回 temperature
- 修复: 使用 `is not None` 检查

#### Task 3: Outlook VML 兼容性
- 位置: templates/email_new.html:47, src/background.py:59
- 问题: `card_background_style` 返回 `url(data:...)` 格式
- VML `<v:fill src="">` 需要裸 URL，不能有 url() 包装
- 修复方案: 在 background.py 提供裸 URL 版本

#### Task 4: 日志键名
- 位置: src/main.py:206
- 当前: `log.error("No recipient email configured (TO_EMAIL).")`
- 修复: 改为更准确的描述

#### Task 5: 时区
- 位置: src/weather.py:34
- 当前: `datetime.now().date()` 使用服务器时区
- 建议: 简化处理 - 在文档中说明服务器时区应与目标城市时区一致

### 依赖关系
- Wave 1 (Task 1-3) 可并行
- Wave 2 (Task 4-5) 可并行
- Task 6 验证必须在所有修复后执行
