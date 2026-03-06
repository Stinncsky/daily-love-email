# 工作计划：创建邮件生成测试脚本

## TL;DR

> **快速摘要**: 创建一个 `scripts/generate_email.py` 脚本，根据 `config.yaml` 生成邮件 HTML 预览文件，方便测试和查看效果。
> 
> **交付文件**:
> - `scripts/generate_email.py` - 主脚本文件
> - `output/` 目录 - 生成的 HTML 保存位置
> 
> **预计工作量**: 小 (Small)
> **并行执行**: NO - 单任务

---

## Context

### 原始需求
用户希望创建一个脚本，能够：
1. 根据 `config.yaml` 配置生成邮件 HTML
2. 保存到文件方便查看效果
3. 支持在浏览器中打开预览

### 技术现状
- 已有完整的配置系统 (`src/config.py`)
- 已有邮件渲染逻辑 (`src/template.py`)
- 已有各种数据获取模块（天气、情话、纪念日、天数计算）

---

## Work Objectives

### Core Objective
创建一个独立脚本，复用现有模块生成邮件 HTML 预览。

### Concrete Deliverables
1. 创建 `scripts/generate_email.py` 脚本
2. 脚本支持命令行参数：`--config`, `--output`, `--open`
3. 脚本显示有用的日志信息
4. 测试验证脚本正常工作

### Definition of Done
- [ ] 运行 `python scripts/generate_email.py` 成功生成 HTML 文件
- [ ] 运行 `python scripts/generate_email.py --open` 在浏览器中打开
- [ ] 生成的 HTML 文件包含完整的邮件内容

---

## Execution Strategy

### Task Sequence
```
Task 1: 创建 scripts/generate_email.py 脚本
    ↓
Task 2: 测试脚本功能
    ↓
Task 3: 验证输出
```

---

## TODOs

- [ ] **1. 创建邮件生成脚本**

  **What to do**:
  - 创建 `scripts/generate_email.py` 文件
  - 实现配置加载（复用 `src.config.load_config`）
  - 实现数据收集：
    - 调用 `calculate_days_together()` 计算恋爱天数
    - 调用 `get_random_quote()` 获取情话
    - 调用 `get_weather()` 获取天气（如果有 API key）
    - 调用 `get_next_anniversary()` 获取纪念日
  - 调用 `render_email()` 渲染 HTML
  - 保存到 `output/email_YYYYMMDD_HHMMSS.html`
  - 添加命令行参数解析：
    - `-c, --config`: 配置文件路径（默认：config.yaml）
    - `-o, --output`: 输出目录（默认：output）
    - `--open`: 生成后在浏览器中打开
  - 添加日志输出，显示：
    - 配置加载状态
    - 恋爱天数
    - 使用的模板和背景类型
    - 生成的文件路径

  **Must NOT do**:
  - 不要实际发送邮件
  - 不要修改现有代码文件
  - 不要硬编码配置值

  **Recommended Agent Profile**:
  - **Category**: `quick`
  - **Skills**: [`python-patterns`]

  **Acceptance Criteria**:
  - [ ] 脚本文件 `scripts/generate_email.py` 存在
  - [ ] 脚本可以独立运行
  - [ ] 命令行参数正常工作
  - [ ] 生成的 HTML 文件可以正常打开查看

  **QA Scenarios**:

  ```
  Scenario: 基本功能测试
    Tool: Bash
    Steps:
      1. 运行: python scripts/generate_email.py
    Expected Result: 
      - 显示配置加载信息
      - 显示恋爱天数
      - 显示生成的文件路径
      - output/ 目录存在 HTML 文件
    Evidence: terminal output

  Scenario: 带参数测试
    Tool: Bash
    Steps:
      1. 运行: python scripts/generate_email.py -c config.yaml -o ./test_output
    Expected Result:
      - HTML 保存到 ./test_output/ 目录
      - 文件名格式: email_YYYYMMDD_HHMMSS.html
    Evidence: ls test_output/
  ```

  **Commit**: YES
  - Message: `feat(scripts): add generate_email.py for testing email templates`
  - Files: `scripts/generate_email.py`

- [ ] **2. 测试脚本功能**

  **What to do**:
  - 运行脚本测试基本功能
  - 测试带参数运行
  - 验证生成的 HTML 内容正确

  **QA Scenarios**:
  ```
  Scenario: 验证 HTML 内容
    Tool: Bash
    Steps:
      1. 运行脚本生成 HTML
      2. 检查 HTML 文件内容
    Expected Result:
      - 包含恋爱天数
      - 包含情话内容
      - 背景样式正确（gradient 或 base64）
    Evidence: grep 检查结果
  ```

- [ ] **3. 验证并文档化**

  **What to do**:
  - 更新 README 或添加使用说明
  - 确认脚本可以正常工作

---

## Success Criteria

### Verification Commands
```bash
# 1. 基本测试
python scripts/generate_email.py

# 2. 带参数测试
python scripts/generate_email.py -c config.yaml -o output --open

# 3. 验证输出
ls output/email_*.html
```

### Final Checklist
- [ ] 脚本可以独立运行
- [ ] 命令行参数正常工作
- [ ] 生成的 HTML 可以正常查看
- [ ] 日志信息清晰有用
