# 每日浪漫邮件自动发送系统 - MVP版本

## TL;DR

> **项目目标**: 每天自动发送一封包含恋爱天数、天气预报、情话和纪念日倒计时的浪漫邮件给对象
> 
> **技术方案**: Python + GitHub Actions Cron + QQ邮箱SMTP
> 
> **核心功能**:
> - 📅 计算并显示"我们在一起多少天"
> - 🌤️ 获取并显示目标城市天气预报
> - 💌 每日随机情话/土味情话
> - 🎉 显示距离下次纪念日还有多少天
> 
> **成本**: 完全免费（GitHub Actions免费额度足够）
> 
> **预计工期**: 2-3小时完成MVP

---

## Context

### 原始需求
用户希望创建一个自动化系统，每天给对象发送一封邮件，核心内容是"我们在一起多少天"，并附加其他浪漫元素。

### 需求访谈结果
**已确认的功能需求**:
- 发送时间: 每天早上8:00
- 邮件服务商: QQ邮箱SMTP
- 基础内容: 恋爱天数计算
- 附加内容: 天气预报、每日情话、纪念日倒计时、星座运势（V2）

**技术决策**:
- 首选方案: Python + GitHub Actions（零成本、最简单）
- 天气API: OpenWeatherMap 或 和风天气
- 情话来源: 本地JSON数据库（预设200+条）
- V2版本AI方案: 本地Qwen2.5-7B + DeepSeek API（混合方案）

**参考项目**:
- horoscope-email: GitHub Actions Cron定时发送星座运势
- Daily-Quote-Email-Automation: 每日名言/情话定时发送
- Daily-Weather-Email-Automation: 天气API集成

### 技术架构

```
GitHub Actions (每天早上8点触发)
    ↓
Python脚本执行
    ├── 计算恋爱天数 (datetime模块)
    ├── 获取天气预报 (Weather API)
    ├── 选择随机情话 (本地JSON)
    ├── 计算纪念日倒计时 (datetime模块)
    ↓
生成HTML邮件内容
    ↓
通过QQ邮箱SMTP发送
```

---

## Work Objectives

### 核心目标
构建一个完全自动化的每日浪漫邮件系统，每天早上8点自动发送包含恋爱天数、天气预报、情话和纪念日提醒的HTML邮件，无需人工干预，零服务器成本运行。

### 具体交付物
1. **项目代码**: 完整的Python项目结构和源代码
2. **配置文件**: config.yaml配置文件模板（含说明）
3. **GitHub Actions配置**: `.github/workflows/daily-email.yml`
4. **情话数据库**: `data/quotes.json`（200+条土味情话）
5. **邮件模板**: `templates/email.html`（精美HTML邮件模板）
6. **部署文档**: README.md（配置步骤、使用说明）

### 定义完成标准 (Definition of Done)
- [ ] 每天早8点GitHub Actions自动触发
- [ ] 成功发送包含恋爱天数的HTML邮件
- [ ] 成功获取并显示天气预报
- [ ] 成功随机显示一条情话
- [ ] 成功计算并显示纪念日倒计时
- [ ] 邮件格式美观、移动端适配良好

### 必须包含 (Must Have)
- 恋爱天数自动计算
- 天气预报API集成
- 本地情话数据库
- 纪念日倒计时
- HTML邮件模板
- GitHub Actions自动定时任务
- 完整的配置文档

### 必须不包含 (Guardrails)
- 不处理星座运势（V2版本功能）
- 不处理AI内容生成（V2版本功能）
- 不使用外部数据库存储（保持简单）
- 不实现用户认证系统（单用户使用）
- 不添加复杂的多人支持

---

## Verification Strategy

> **ZERO HUMAN INTERVENTION** — ALL verification is agent-executed. No exceptions.

### Test Decision
- **Infrastructure exists**: NO（新项目）
- **Automated tests**: Tests-after（实现后添加基础测试）
- **Framework**: Python unittest（轻量级）
- **Coverage target**: 核心功能路径覆盖

### QA Policy
Every task MUST include agent-executed QA scenarios.
Evidence saved to `.sisyphus/evidence/task-{N}-{scenario-slug}.{ext}`.

- **API/Backend**: Use Bash (curl) - Send requests, assert status + response fields
- **Script/Logic**: Use Bash (python) - Run script, validate output
- **Integration**: Use Bash - Full workflow validation

---

## Execution Strategy

### Parallel Execution Waves

**Wave 1 - 项目初始化与配置（全部可并行）**:
```
├── Task 1: 创建项目结构 [quick]
├── Task 2: 配置GitHub Actions工作流 [quick]
├── Task 3: 创建配置文件模板 [quick]
└── Task 4: 创建情话数据库 [quick]
```

**Wave 2 - 核心功能开发（依赖Wave 1）**:
```
├── Task 5: 实现恋爱天数计算 [quick]
├── Task 6: 实现纪念日倒计时 [quick]
├── Task 7: 集成天气API [quick]
└── Task 8: 实现随机情话选择 [quick]
```

**Wave 3 - 邮件生成与发送（依赖Wave 2）**:
```
├── Task 9: 创建HTML邮件模板 [visual-engineering]
├── Task 10: 实现邮件发送功能 [quick]
└── Task 11: 整合主脚本 [quick]
```

**Wave 4 - 测试与部署（依赖Wave 3）**:
```
├── Task 12: 编写测试用例 [quick]
├── Task 13: 配置GitHub Secrets [quick]
└── Task 14: 端到端测试验证 [unspecified-high]
```

**Wave FINAL - 文档与交付（全部可并行）**:
```
├── Task F1: 编写README文档 [writing]
└── Task F2: 代码质量检查 [quick]
```

### Dependency Matrix

| Task | Dependencies | Blocks |
|------|-------------|--------|
| T1-4 | None | T5-8 |
| T5-8 | T1-4 | T9-11 |
| T9-11 | T5-8 | T12-14 |
| T12-14 | T9-11 | F1-F2 |
| F1-F2 | T12-14 | - |

### Agent Dispatch Summary

- **Wave 1**: **4 tasks** → all `quick` agents
- **Wave 2**: **4 tasks** → all `quick` agents
- **Wave 3**: **3 tasks** → T9 `visual-engineering`, T10-11 `quick`
- **Wave 4**: **3 tasks** → T12-13 `quick`, T14 `unspecified-high`
- **FINAL**: **2 tasks** → F1 `writing`, F2 `quick`

---

## TODOs

### Wave 1 - 项目初始化与配置

- [ ] 1. 创建项目基础结构

  **What to do**:
  - 创建项目目录结构：`src/`, `data/`, `templates/`, `.github/workflows/`
  - 创建 `requirements.txt`，添加依赖：requests, pyyaml, jinja2
  - 创建 `.gitignore`，排除敏感配置文件
  - 创建 `config.yaml.example` 模板文件

  **Must NOT do**:
  - 不要添加V2版本的功能代码（AI、星座等）
  - 不要提交真实的配置文件（含密码）

  **Recommended Agent Profile**:
  - **Category**: `quick`
    - Reason: 基础项目结构搭建，标准化任务
  - **Skills**: []
    - 无需特殊技能，基础Python项目结构

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 1 (with Tasks 2, 3, 4)
  - **Blocks**: Tasks 5-8
  - **Blocked By**: None

  **References**:
  - `.github/workflows/` - GitHub Actions配置目录
  - `config.yaml` - 主配置文件格式参考其他Python项目

  **Acceptance Criteria**:
  - [ ] 目录结构完整
  - [ ] requirements.txt包含所有依赖
  - [ ] .gitignore正确配置

  **QA Scenarios**:
  ```
  Scenario: 验证项目结构
    Tool: Bash
    Steps:
      1. ls -la
      2. cat requirements.txt
    Expected: 目录结构正确，依赖文件存在
    Evidence: .sisyphus/evidence/task-1-structure.txt
  ```

  **Commit**: YES
  - Message: `feat: init project structure`
  - Files: `requirements.txt, .gitignore, config.yaml.example`

---

- [ ] 2. 配置GitHub Actions定时工作流

  **What to do**:
  - 创建 `.github/workflows/daily-email.yml`
  - 配置Cron定时：每天早上8点运行（`0 0 * * *` UTC时间对应北京时间8点）
  - 配置Python环境：Python 3.10
  - 配置环境变量读取（从GitHub Secrets）
  - 配置执行步骤：安装依赖 → 运行主脚本

  **Must NOT do**:
  - 不要硬编码敏感信息（邮箱密码等）
  - 不要设置过于频繁的触发（避免超出免费额度）

  **Recommended Agent Profile**:
  - **Category**: `quick`
    - Reason: GitHub Actions配置是标准任务
  - **Skills**: []
    - 参考 horoscope-email 项目的工作流配置

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 1 (with Tasks 1, 3, 4)
  - **Blocks**: Task 14 (端到端测试需要工作流)
  - **Blocked By**: None

  **References**:
  - horoscope-email项目的 `.github/workflows/main.yml` 作为参考
  - GitHub Actions Cron语法文档

  **Acceptance Criteria**:
  - [ ] 工作流文件语法正确
  - [ ] Cron表达式设置正确（早8点）
  - [ ] 环境变量配置正确

  **QA Scenarios**:
  ```
  Scenario: 验证工作流语法
    Tool: Bash
    Steps:
      1. cat .github/workflows/daily-email.yml
      2. 检查cron表达式格式
    Expected: 语法正确，无YAML错误
    Evidence: .sisyphus/evidence/task-2-workflow.yml
  ```

  **Commit**: YES
  - Message: `ci: add GitHub Actions workflow`
  - Files: `.github/workflows/daily-email.yml`

---

- [ ] 3. 创建配置文件和数据模板

  **What to do**:
  - 创建 `config.yaml.example` 配置文件模板，包含：
    - 邮件配置（发件人、收件人、SMTP服务器）
    - 恋爱起始日期
    - 纪念日列表
    - 目标城市（用于天气）
    - 其他配置项
  - 创建 `src/config.py` 配置读取模块
  - 使用PyYAML解析配置文件

  **Must NOT do**:
  - 不要在代码中提交真实配置值
  - 配置文件必须包含所有必需字段的说明

  **Recommended Agent Profile**:
  - **Category**: `quick`
    - Reason: 配置管理是标准化任务
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 1 (with Tasks 1, 2, 4)
  - **Blocks**: Tasks 5-11 (所有功能都依赖配置)
  - **Blocked By**: None

  **References**:
  - Python PyYAML库官方文档
  - 配置文件最佳实践（环境变量覆盖）

  **Acceptance Criteria**:
  - [ ] config.yaml.example包含所有必需字段
  - [ ] config.py能正确读取配置文件
  - [ ] 支持环境变量覆盖配置

  **QA Scenarios**:
  ```
  Scenario: 测试配置读取
    Tool: Bash (python)
    Steps:
      1. python -c "from src.config import load_config; print(load_config('config.yaml.example'))"
    Expected: 成功读取配置，无错误
    Evidence: .sisyphus/evidence/task-3-config.txt
  ```

  **Commit**: YES
  - Message: `feat: add configuration system`
  - Files: `config.yaml.example, src/config.py`

---

- [ ] 4. 创建情话数据库

  **What to do**:
  - 创建 `data/quotes.json` 文件
  - 包含至少200条土味情话/浪漫情话
  - 按分类组织：甜蜜型、搞笑型、文艺型等
  - 每条情话包含：内容、分类、标签

  **Must NOT do**:
  - 不要使用可能冒犯的内容
  - 不要包含敏感或不当内容

  **Recommended Agent Profile**:
  - **Category**: `quick`
    - Reason: 数据准备任务
  - **Skills**: []
    - 需要收集情话内容，可以从网上整理

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 1 (with Tasks 1, 2, 3)
  - **Blocks**: Task 8 (随机情话选择)
  - **Blocked By**: None

  **References**:
  - 土味情话大全（网络资源）
  - 经典情话语录

  **Acceptance Criteria**:
  - [ ] 至少200条情话
  - [ ] JSON格式正确
  - [ ] 包含多种风格分类

  **QA Scenarios**:
  ```
  Scenario: 验证情话数据库
    Tool: Bash (python)
    Steps:
      1. python -c "import json; data=json.load(open('data/quotes.json')); print(f'Total: {len(data)}')"
    Expected: 返回情话数量 >= 200
    Evidence: .sisyphus/evidence/task-4-quotes.json
  ```

  **Commit**: YES
  - Message: `feat: add love quotes database`
  - Files: `data/quotes.json`

---

### Wave 2 - 核心功能开发

- [ ] 5. 实现恋爱天数计算模块

  **What to do**:
  - 创建 `src/calculator.py` 模块
  - 实现 `calculate_days_together(start_date)` 函数
  - 输入: 恋爱起始日期 (YYYY-MM-DD格式)
  - 输出: 在一起的天数、月数、年数
  - 处理时区和日期边界情况

  **Must NOT do**:
  - 不要硬编码日期，必须从配置文件读取
  - 不要忽略闰年和时区问题

  **Recommended Agent Profile**:
  - **Category**: `quick`
    - Reason: 日期计算是标准任务
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 2 (with Tasks 6, 7, 8)
  - **Blocks**: Task 11 (主脚本需要此功能)
  - **Blocked By**: Task 3 (配置系统)

  **References**:
  - Python datetime模块官方文档
  - dateutil库处理时区和日期计算

  **Acceptance Criteria**:
  - [ ] 正确计算天数
  - [ ] 处理边界情况（起始日期为未来日期）
  - [ ] 单元测试通过

  **QA Scenarios**:
  ```
  Scenario: 测试恋爱天数计算
    Tool: Bash (python)
    Steps:
      1. python -c "from src.calculator import calculate_days_together; print(calculate_days_together('2023-01-01'))"
    Expected: 返回正确的天数
    Evidence: .sisyphus/evidence/task-5-calculator.txt
  ```

  **Commit**: YES
  - Message: `feat: add days together calculator`
  - Files: `src/calculator.py, tests/test_calculator.py`

---

- [ ] 6. 实现纪念日倒计时模块

  **What to do**:
  - 创建 `src/anniversary.py` 模块
  - 实现 `get_next_anniversary(anniversaries)` 函数
  - 输入: 纪念日列表（日期、名称、类型）
  - 输出: 距离最近的纪念日还有多少天
  - 支持多种纪念日类型：恋爱纪念日、生日、第一次约会等

  **Must NOT do**:
  - 不要只支持单个纪念日
  - 不要忽略重复性纪念日（每年一次）

  **Recommended Agent Profile**:
  - **Category**: `quick`
    - Reason: 日期计算逻辑
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 2 (with Tasks 5, 7, 8)
  - **Blocks**: Task 11
  - **Blocked By**: Task 3

  **Acceptance Criteria**:
  - [ ] 正确计算最近的纪念日
  - [ ] 支持重复性纪念日
  - [ ] 单元测试通过

  **QA Scenarios**:
  ```
  Scenario: 测试纪念日倒计时
    Tool: Bash (python)
    Steps:
      1. python -c "from src.anniversary import get_next_anniversary; print(get_next_anniversary([{'date': '2024-12-25', 'name': '圣诞节'}]))"
    Expected: 返回正确的倒计时天数
    Evidence: .sisyphus/evidence/task-6-anniversary.txt
  ```

  **Commit**: YES
  - Message: `feat: add anniversary countdown`
  - Files: `src/anniversary.py, tests/test_anniversary.py`

---

- [ ] 7. 集成天气API

  **What to do**:
  - 创建 `src/weather.py` 模块
  - 实现 `get_weather(city)` 函数
  - 集成OpenWeatherMap API（免费版）
  - 返回：温度、天气状况、湿度、风速
  - 处理API错误和超时

  **Must NOT do**:
  - 不要硬编码API密钥
  - 不要忽略API错误处理

  **Recommended Agent Profile**:
  - **Category**: `quick`
    - Reason: API集成任务
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 2 (with Tasks 5, 6, 8)
  - **Blocks**: Task 11
  - **Blocked By**: Task 3

  **References**:
  - OpenWeatherMap API文档
  - requests库HTTP请求最佳实践

  **Acceptance Criteria**:
  - [ ] 成功获取天气数据
  - [ ] 正确处理API错误
  - [ ] 返回格式化的天气信息

  **QA Scenarios**:
  ```
  Scenario: 测试天气API
    Tool: Bash (python)
    Steps:
      1. python -c "from src.weather import get_weather; print(get_weather('Beijing'))"
    Expected: 返回天气数据
    Evidence: .sisyphus/evidence/task-7-weather.txt
  ```

  **Commit**: YES
  - Message: `feat: add weather API integration`
  - Files: `src/weather.py, tests/test_weather.py`

---

- [ ] 8. 实现随机情话选择

  **What to do**:
  - 创建 `src/quotes.py` 模块
  - 实现 `get_random_quote()` 函数
  - 从 `data/quotes.json` 读取情话库
  - 支持按分类筛选（可选参数）
  - 实现随机选择算法，避免连续重复

  **Must NOT do**:
  - 不要每次都选同一条情话
  - 不要忽略文件不存在的情况

  **Recommended Agent Profile**:
  - **Category**: `quick`
    - Reason: 数据读取和随机选择
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 2 (with Tasks 5, 6, 7)
  - **Blocks**: Task 11
  - **Blocked By**: Task 4 (情话数据库)

  **Acceptance Criteria**:
  - [ ] 成功读取情话库
  - [ ] 随机选择不同情话
  - [ ] 支持按分类筛选

  **QA Scenarios**:
  ```
  Scenario: 测试情话选择
    Tool: Bash (python)
    Steps:
      1. python -c "from src.quotes import get_random_quote; print(get_random_quote())"
      2. 重复运行5次，验证返回不同结果
    Expected: 返回不同的随机情话
    Evidence: .sisyphus/evidence/task-8-quotes.txt
  ```

  **Commit**: YES
  - Message: `feat: add random quote selector`
  - Files: `src/quotes.py, tests/test_quotes.py`

---

### Wave 3 - 邮件生成与发送

- [ ] 9. 创建HTML邮件模板

  **What to do**:
  - 创建 `templates/email.html` Jinja2模板
  - 设计精美的邮件布局：
    - 顶部：浪漫标题和日期
    - 主体：恋爱天数大字显示
    - 中部：今日情话
    - 底部：天气预报 + 纪念日提醒
  - 使用内联CSS（邮件客户端兼容）
  - 移动端适配

  **Must NOT do**:
  - 不要使用外部CSS文件（邮件客户端不支持）
  - 不要使用复杂的JavaScript

  **Recommended Agent Profile**:
  - **Category**: `visual-engineering`
    - Reason: 需要设计美观的邮件模板
  - **Skills**: []
    - HTML/CSS邮件模板设计

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 3 (with Tasks 10, 11)
  - **Blocks**: Task 10 (邮件发送需要模板)
  - **Blocked By**: Wave 2完成

  **References**:
  - Jinja2模板语法
  - 邮件模板最佳实践（Campaign Monitor指南）

  **Acceptance Criteria**:
  - [ ] 模板渲染正确
  - [ ] 移动端显示良好
  - [ ] 所有占位符正确替换

  **QA Scenarios**:
  ```
  Scenario: 测试邮件模板渲染
    Tool: Bash (python)
    Steps:
      1. python -c "from src.template import render_email; print(render_email({'days': 100, 'quote': 'test', 'weather': '晴天'}))"
    Expected: 返回完整的HTML字符串
    Evidence: .sisyphus/evidence/task-9-template.html
  ```

  **Commit**: YES
  - Message: `feat: add HTML email template`
  - Files: `templates/email.html, src/template.py`

---

- [ ] 10. 实现邮件发送功能

  **What to do**:
  - 创建 `src/email_sender.py` 模块
  - 实现 `send_email(to, subject, html_content)` 函数
  - 使用Python smtplib库
  - 支持QQ邮箱SMTP（SSL加密）
  - 处理发送错误和重试

  **Must NOT do**:
  - 不要硬编码邮箱密码
  - 不要忽略SMTP错误处理

  **Recommended Agent Profile**:
  - **Category**: `quick`
    - Reason: SMTP邮件发送标准实现
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 3 (with Tasks 9, 11)
  - **Blocks**: Task 11, Task 14
  - **Blocked By**: Task 3 (配置系统)

  **References**:
  - Python smtplib文档
  - QQ邮箱SMTP配置指南

  **Acceptance Criteria**:
  - [ ] 成功发送邮件
  - [ ] 正确处理SMTP错误
  - [ ] 支持HTML内容

  **QA Scenarios**:
  ```
  Scenario: 测试邮件发送（使用测试邮箱）
    Tool: Bash (python)
    Steps:
      1. python -c "from src.email_sender import send_email; send_email('test@example.com', 'Test', '<h1>Test</h1>')"
    Expected: 邮件发送成功（或报错信息正确）
    Evidence: .sisyphus/evidence/task-10-email.txt
  ```

  **Commit**: YES
  - Message: `feat: add email sender`
  - Files: `src/email_sender.py, tests/test_email_sender.py`

---

- [ ] 11. 整合主脚本

  **What to do**:
  - 创建 `src/main.py` 主脚本
  - 整合所有模块：
    1. 加载配置
    2. 计算恋爱天数
    3. 获取天气预报
    4. 选择随机情话
    5. 计算纪念日倒计时
    6. 渲染邮件模板
    7. 发送邮件
  - 添加日志记录
  - 添加错误处理和重试机制

  **Must NOT do**:
  - 不要把所有逻辑写在main函数里（保持模块化）
  - 不要忽略异常处理

  **Recommended Agent Profile**:
  - **Category**: `quick`
    - Reason: 模块整合任务
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 3 (with Tasks 9, 10)
  - **Blocks**: Task 14 (端到端测试)
  - **Blocked By**: Wave 2所有任务

  **Acceptance Criteria**:
  - [ ] 主脚本能完整运行
  - [ ] 错误处理完善
  - [ ] 日志记录完整

  **QA Scenarios**:
  ```
  Scenario: 测试主脚本执行
    Tool: Bash
    Steps:
      1. python src/main.py --dry-run
    Expected: 脚本执行成功，输出执行日志
    Evidence: .sisyphus/evidence/task-11-main.txt
  ```

  **Commit**: YES
  - Message: `feat: add main script`
  - Files: `src/main.py`

---

### Wave 4 - 测试与部署

- [ ] 12. 编写单元测试

  **What to do**:
  - 创建 `tests/` 目录
  - 为每个核心模块编写单元测试：
    - test_calculator.py - 测试恋爱天数计算
    - test_anniversary.py - 测试纪念日倒计时
    - test_quotes.py - 测试情话选择
    - test_email_sender.py - 测试邮件发送（mock）
  - 使用Python unittest框架
  - 达到80%+代码覆盖率

  **Must NOT do**:
  - 不要测试外部API（使用mock）
  - 不要测试私有函数

  **Recommended Agent Profile**:
  - **Category**: `quick`
    - Reason: 单元测试编写
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 4 (with Tasks 13, 14)
  - **Blocks**: None
  - **Blocked By**: Wave 3完成

  **Acceptance Criteria**:
  - [ ] 所有单元测试通过
  - [ ] 代码覆盖率 >= 80%

  **QA Scenarios**:
  ```
  Scenario: 运行所有测试
    Tool: Bash
    Steps:
      1. python -m pytest tests/ -v
    Expected: 所有测试通过
    Evidence: .sisyphus/evidence/task-12-tests.txt
  ```

  **Commit**: YES
  - Message: `test: add unit tests`
  - Files: `tests/*.py`

---

- [ ] 13. 配置GitHub Secrets

  **What to do**:
  - 创建 `.github/secrets_template.md` 文档
  - 说明需要配置的Secrets：
    - `EMAIL_SENDER`: 发件人邮箱
    - `EMAIL_PASSWORD`: 邮箱授权码（不是登录密码）
    - `EMAIL_RECIPIENT`: 收件人邮箱
    - `WEATHER_API_KEY`: 天气API密钥
  - 提供配置步骤截图指引

  **Must NOT do**:
  - 不要在代码中提交真实密钥
  - 不要把Secrets文档命名为敏感名称

  **Recommended Agent Profile**:
  - **Category**: `quick`
    - Reason: 文档编写
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 4 (with Tasks 12, 14)
  - **Blocks**: Task 14
  - **Blocked By**: None

  **Acceptance Criteria**:
  - [ ] 文档完整说明所有Secrets
  - [ ] 包含配置步骤截图位置

  **QA Scenarios**:
  ```
  Scenario: 验证文档完整性
    Tool: Bash
    Steps:
      1. cat .github/secrets_template.md
    Expected: 文档包含所有必需的Secrets说明
    Evidence: .sisyphus/evidence/task-13-secrets.md
  ```

  **Commit**: YES
  - Message: `docs: add secrets configuration guide`
  - Files: `.github/secrets_template.md`

---

- [ ] 14. 端到端测试验证

  **What to do**:
  - 执行完整测试流程：
    1. 本地运行主脚本（dry-run模式）
    2. 验证输出内容正确
    3. 发送测试邮件到测试邮箱
    4. 验证邮件格式和内容
  - 测试边界情况：
    - 起始日期为未来
    - API超时
    - 无效配置

  **Must NOT do**:
  - 不要直接给对象发测试邮件（先用测试邮箱）
  - 不要忽略错误情况测试

  **Recommended Agent Profile**:
  - **Category**: `unspecified-high`
    - Reason: 需要完整验证整个流程
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 4 (with Tasks 12, 13)
  - **Blocks**: Wave FINAL
  - **Blocked By**: Wave 3所有任务

  **Acceptance Criteria**:
  - [ ] 本地测试通过
  - [ ] 测试邮件发送成功
  - [ ] 邮件内容正确

  **QA Scenarios**:
  ```
  Scenario: 端到端测试
    Tool: Bash
    Steps:
      1. python src/main.py --test
      2. 检查测试邮箱收到邮件
    Expected: 邮件收到，内容完整正确
    Evidence: .sisyphus/evidence/task-14-e2e.txt
  ```

  **Commit**: NO（测试过程不产生代码变更）

---

### Wave FINAL - 文档与交付

- [ ] F1. 编写README文档

  **What to do**:
  - 创建完整的README.md：
    - 项目介绍和截图
    - 功能特性列表
    - 快速开始指南
    - 配置说明（config.yaml）
    - GitHub Secrets配置
    - 本地开发指南
    - 常见问题FAQ
    - V2版本路线图

  **Must NOT do**:
  - 不要只写几行简单的说明
  - 不要遗漏配置步骤

  **Recommended Agent Profile**:
  - **Category**: `writing`
    - Reason: 需要编写完整的项目文档
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave FINAL (with Task F2)
  - **Blocks**: None
  - **Blocked By**: Wave 4完成

  **Acceptance Criteria**:
  - [ ] README内容完整
  - [ ] 包含所有配置步骤
  - [ ] 有截图位置标记

  **QA Scenarios**:
  ```
  Scenario: 验证README完整性
    Tool: Bash
    Steps:
      1. cat README.md
    Expected: 文档包含所有必需章节
    Evidence: .sisyphus/evidence/task-f1-readme.md
  ```

  **Commit**: YES
  - Message: `docs: add comprehensive README`
  - Files: `README.md`

---

- [ ] F2. 代码质量检查

  **What to do**:
  - 运行代码格式化（black/isort）
  - 运行静态检查（flake8/pylint）
  - 检查代码注释和文档字符串
  - 确保没有硬编码的敏感信息
  - 检查.gitignore完整性

  **Must NOT do**:
  - 不要提交未格式化的代码
  - 不要忽略lint错误

  **Recommended Agent Profile**:
  - **Category**: `quick`
    - Reason: 代码质量检查是标准任务
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave FINAL (with Task F1)
  - **Blocks**: None
  - **Blocked By**: Wave 4完成

  **Acceptance Criteria**:
  - [ ] 代码格式正确
  - [ ] 无lint错误
  - [ ] 无敏感信息泄露

  **QA Scenarios**:
  ```
  Scenario: 代码质量检查
    Tool: Bash
    Steps:
      1. flake8 src/
      2. black --check src/
    Expected: 无错误或警告
    Evidence: .sisyphus/evidence/task-f2-quality.txt
  ```

  **Commit**: YES
  - Message: `style: format code and fix linting`
  - Files: `src/*.py`

---

## Final Verification Wave

> 4 review agents run in PARALLEL. ALL must APPROVE.

- [ ] FV1. **功能完整性验证** - `oracle`
  - 检查所有Must Have功能已实现
  - 验证所有Guardrails未违反
  - 测试GitHub Actions工作流
  - Output: `Features [N/N] | Guardrails [PASS] | Workflow [PASS] | VERDICT`

- [ ] FV2. **代码质量审查** - `quick`
  - 运行所有单元测试
  - 检查代码覆盖率
  - 验证无硬编码敏感信息
  - Output: `Tests [PASS/FAIL] | Coverage [N%] | Security [PASS] | VERDICT`

- [ ] FV3. **文档完整性检查** - `writing`
  - 验证README完整性
  - 检查配置文档准确性
  - 验证所有链接可用
  - Output: `README [COMPLETE] | Config [ACCURATE] | VERDICT`

- [ ] FV4. **部署就绪检查** - `unspecified-high`
  - 验证GitHub Secrets模板完整
  - 测试本地运行流程
  - 验证邮件发送功能
  - Output: `Secrets [COMPLETE] | Local [WORKING] | Email [SENDING] | VERDICT`

---

## Commit Strategy

### 提交规范
- 使用Conventional Commits格式
- 每个任务一个commit（除非特别说明）
- 提交前运行测试

### 提交示例
```
feat: init project structure
feat: add GitHub Actions workflow
feat: add configuration system
feat: add love quotes database
feat: add days together calculator
...
```

---

## Success Criteria

### 验证命令
```bash
# 1. 运行测试
python -m pytest tests/ -v

# 2. 运行主脚本（dry-run模式）
python src/main.py --dry-run

# 3. 发送测试邮件
python src/main.py --test-email your-test@email.com

# 4. 检查GitHub Actions状态
gh run list --workflow=daily-email.yml
```

### 最终检查清单
- [ ] 所有单元测试通过
- [ ] 代码覆盖率 >= 80%
- [ ] 本地测试邮件发送成功
- [ ] GitHub Actions配置正确
- [ ] README文档完整
- [ ] 无硬编码敏感信息
- [ ] 代码格式正确

### 部署后验证
1. 推送代码到GitHub
2. 配置GitHub Secrets
3. 手动触发一次工作流测试
4. 确认对象收到第一封邮件
5. 等待第二天早上8点自动触发验证

---

## 项目文件结构

```
daily-love-email/
├── .github/
│   ├── workflows/
│   │   └── daily-email.yml      # GitHub Actions工作流
│   └── secrets_template.md       # Secrets配置说明
├── src/
│   ├── __init__.py
│   ├── main.py                   # 主脚本
│   ├── config.py                 # 配置读取
│   ├── calculator.py             # 恋爱天数计算
│   ├── anniversary.py            # 纪念日倒计时
│   ├── weather.py                # 天气API
│   ├── quotes.py                 # 情话选择
│   ├── template.py               # 邮件模板渲染
│   └── email_sender.py           # 邮件发送
├── templates/
│   └── email.html                # HTML邮件模板
├── data/
│   └── quotes.json               # 情话数据库
├── tests/
│   ├── __init__.py
│   ├── test_calculator.py
│   ├── test_anniversary.py
│   ├── test_quotes.py
│   └── test_email_sender.py
├── config.yaml.example           # 配置文件模板
├── requirements.txt              # Python依赖
├── .gitignore                    # Git忽略文件
└── README.md                     # 项目文档
```

---

## V2版本路线图

MVP版本完成后，可以考虑添加以下功能：

### Phase 2 - 星座运势
- [ ] 集成星座运势API或爬虫
- [ ] 根据对方生日自动计算星座
- [ ] 每日运势推送

### Phase 3 - AI个性化
- [ ] 本地模型分析聊天记录（Ollama + Qwen）
- [ ] DeepSeek API生成个性化情书
- [ ] 学习用户说话风格

### Phase 4 - 增强功能
- [ ] 邮件回执确认
- [ ] 每周/每月统计报告
- [ ] 纪念日提前提醒
- [ ] 照片自动插入

---

*计划生成时间: 2025-03-05*
*版本: MVP v1.0*