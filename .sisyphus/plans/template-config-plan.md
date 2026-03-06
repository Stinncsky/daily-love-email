# 工作计划：配置选择模板 + Base64背景图 + 天数计算

## TL;DR

> **快速摘要**: 为每日恋爱邮件项目添加模板配置选择功能、Base64 背景图方案，并修复天数计算逻辑，使其只计算天数。
> 
> **核心变更**:
> - 添加 `app.template` 配置项支持多模板切换
> - 添加 `app.background_type` 和 `app.background_image` 配置支持 CSS 渐变和 Base64 图片背景
> - 简化 `calculate_days_together()` 只返回天数，移除年月计算
> - 更新模板渲染逻辑注入背景图数据
> - 添加 TDD 测试覆盖
> 
> **交付文件**:
> - `src/calculator.py` - 简化的天数计算
> - `src/template.py` - 支持模板选择和背景图
> - `src/background.py` - Base64 背景图工具（新增）
> - `config.yaml` - 更新配置示例
> - `tests/test_calculator.py` - 天数计算测试
> - `tests/test_background.py` - 背景图工具测试
> - `templates/email_new.html` - 更新背景图变量
> 
> **预计工作量**: 中等 (Medium)  
> **并行执行**: YES - 3 Waves  
> **关键路径**: T1(TDD测试) → T2(计算器简化) → T5(模板更新) → F1-F3(最终验证)

---

## Context

### 原始需求
用户希望为每日恋爱邮件项目：
1. 添加配置选择模板的功能
2. 改成 base64 添加背景图的方案
3. 修复天数计算问题（新模板只显示天数，统一计算方式）

### 当前状态
- **模板系统**: 使用 Jinja2，`email_new.html` 当前只显示天数
- **背景图**: 当前使用 CSS 渐变，文档建议可以改为 Base64 图片
- **天数计算**: `calculate_days_together()` 返回 `(days, months, years)` 三元组
- **配置系统**: YAML + 环境变量覆盖，现有 `app.timezone` 配置

### 需求确认
- ✅ **模板配置**: `app.template` = 'email_new' 或其他模板名
- ✅ **背景图配置**: `app.background_type` = 'gradient' | 'base64_image'
- ✅ **天数计算**: 只计算天数，返回 `int` 而非元组
- ✅ **测试策略**: TDD，先写测试后实现，目标覆盖率 80%+

---

## Work Objectives

### Core Objective
为每日恋爱邮件项目添加灵活的模板选择和背景图配置，同时简化天数计算逻辑，使其与新模板保持一致。

### Concrete Deliverables
1. 更新 `config.yaml` 添加 `app.template`, `app.background_type`, `app.background_image` 配置项
2. 简化 `src/calculator.py` 的 `calculate_days_together()` 只返回天数
3. 新增 `src/background.py` 模块提供 Base64 图片转换功能
4. 更新 `src/template.py` 支持根据配置选择模板和注入背景图数据
5. 更新 `templates/email_new.html` 使用背景图变量
6. 编写 TDD 测试覆盖新功能

### Definition of Done
- [ ] `python src/main.py --dry-run` 能正常渲染邮件
- [ ] 切换 `app.template` 配置可以使用不同模板
- [ ] 切换 `app.background_type` 配置可以在 CSS 渐变和 Base64 图片间切换
- [ ] `pytest tests/` 所有测试通过，覆盖率 ≥80%
- [ ] 代码风格检查通过

### Must Have
- [ ] 模板配置通过 config.yaml 的 `app.template` 设置
- [ ] 背景图类型通过 `app.background_type` 选择（gradient/base64_image）
- [ ] Base64 图片背景支持 `assets/images/backgrounds/` 下的图片
- [ ] 天数计算只返回天数，移除年月计算
- [ ] TDD 测试覆盖所有新功能

### Must NOT Have (Guardrails)
- 不要修改现有 `email.html` 模板（保持向后兼容）
- 不要移除现有的 CSS 渐变背景支持（保持默认行为）
- 不要破坏现有 config.yaml 的其他配置项
- 不要在测试中引入外部依赖（mock 天气 API、邮件发送）

---

## Verification Strategy

> **ZERO HUMAN INTERVENTION** — ALL verification is agent-executed. No exceptions.

### Test Decision
- **Infrastructure exists**: YES (pytest)
- **Automated tests**: TDD (先写测试，后实现)
- **Framework**: pytest
- **TDD 工作流**: RED (写失败测试) → GREEN (实现通过) → REFACTOR (重构)

### QA Policy
Every task MUST include agent-executed QA scenarios.
Evidence saved to `.sisyphus/evidence/task-{N}-{scenario-slug}.{ext}`.

- **单元测试**: 使用 pytest
- **集成测试**: 运行 `python src/main.py --dry-run`
- **代码质量**: 运行 `pytest --cov=src tests/`

---

## Execution Strategy

### Parallel Execution Waves

```
Wave 1 (TDD 测试先行):
├── Task 1: 编写 calculator 测试 [quick]
└── Task 2: 编写 background 工具测试 [quick]

Wave 2 (核心实现 - MAX PARALLEL):
├── Task 3: 简化 calculator 只返回天数 [quick]
├── Task 4: 创建 background.py Base64 工具 [unspecified-high]
└── Task 5: 更新 config.yaml 配置示例 [quick]

Wave 3 (模板集成):
├── Task 6: 更新 template.py 支持模板选择和背景图 [deep]
└── Task 7: 更新 email_new.html 模板使用背景图变量 [visual-engineering]

Wave FINAL (最终验证 - 并行):
├── Task F1: 运行全部测试并验证覆盖率 [deep]
├── Task F2: 干运行测试验证功能 [unspecified-high]
└── Task F3: 代码质量检查 [quick]

Critical Path: T1 → T3, T2 → T4 → T6 → F1-F3
Parallel Speedup: ~50% faster than sequential
Max Concurrent: 3 (Wave 2)
```

### Dependency Matrix

| Task | Blocks | Blocked By |
|------|--------|-----------|
| T1 (calculator测试) | T3 | — |
| T2 (background测试) | T4 | — |
| T3 (calculator实现) | T6 | T1 |
| T4 (background实现) | T6 | T2 |
| T5 (config更新) | — | — |
| T6 (template更新) | F1-F3 | T3, T4 |
| T7 (模板更新) | F1-F3 | T6 |
| F1-F3 (验证) | — | T6, T7 |

---

## TODOs

- [x] **1. TDD: 编写 calculator 简化测试**

  **What to do**:
  - 在 `tests/test_calculator.py` 中编写测试，验证 `calculate_days_together()` 只返回 `int` 类型的天数
  - 测试正常日期计算（start_date 在过去）
  - 测试边界情况：start_date 是今天（应该返回 0）
  - 测试异常情况：start_date 在未来（应该抛出 ValueError）
  - 测试异常情况：无效日期格式（应该抛出 ValueError）
  - 使用 `pytest.raises` 验证异常
  - 运行测试确认全部失败（RED 阶段）

  **Must NOT do**:
  - 不要修改 `src/calculator.py`（这是 TDD，先写测试）
  - 不要测试年月计算（将被移除）
  - 不要引入外部依赖（mock 所有外部调用）

  **Recommended Agent Profile**:
  - **Category**: `quick`
    - Reason: 编写测试是标准任务，不需要复杂推理
  - **Skills**: [`python-testing`]
    - `python-testing`: 需要使用 pytest 编写单元测试

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 1 (with T2)
  - **Blocks**: T3
  - **Blocked By**: None (can start immediately)

  **References**:
  - `src/calculator.py:calculate_days_together` - 当前实现（将修改）
  - `tests/` - 测试目录结构（参考现有测试）
  - Python `pytest.raises` - 异常测试语法
  - Python `datetime` 模块 - 日期处理

  **Acceptance Criteria**:
  - [ ] 测试文件 `tests/test_calculator.py` 存在
  - [ ] 运行 `pytest tests/test_calculator.py -v` 显示所有测试失败（预期）
  - [ ] 测试覆盖：正常计算、边界情况、异常处理
  - [ ] 使用 `freezegun` 或 `monkeypatch` 固定测试日期（避免日期漂移）

  **QA Scenarios**:

  ```
  Scenario: 正常日期计算测试
    Tool: Bash
    Preconditions: 测试文件已编写
    Steps:
      1. 运行: pytest tests/test_calculator.py -v
    Expected Result: 所有测试失败（因为实现还未更新），但测试逻辑正确
    Evidence: .sisyphus/evidence/task-1-calculator-tests.png

  Scenario: 测试覆盖率检查
    Tool: Bash
    Steps:
      1. 运行: pytest tests/test_calculator.py --cov=src.calculator --cov-report=term
    Expected Result: 覆盖率 0%（实现未修改），但测试已覆盖所有场景
    Evidence: .sisyphus/evidence/task-1-coverage.txt
  ```

  **Commit**: YES
  - Message: `test(calculator): add tests for simplified days calculation`
  - Files: `tests/test_calculator.py`
  - Pre-commit: `pytest tests/test_calculator.py` (expect failures)

- [x] **2. TDD: 编写 background 工具测试**

  **What to do**:
  - 在 `tests/test_background.py` 中编写测试，验证 `background.py` 的功能
  - 测试 `get_background_base64(image_name)` 函数：
    - 正常情况：返回有效的 base64 字符串
    - 图片不存在：抛出 FileNotFoundError
  - 测试 `get_background_style(background_type, image_name)` 函数：
    - `background_type='gradient'`：返回 CSS 渐变样式
    - `background_type='base64_image'`：返回 base64 图片样式
  - 使用 `tmp_path` fixture 创建临时测试图片
  - 运行测试确认全部失败（RED 阶段）

  **Must NOT do**:
  - 不要创建 `src/background.py`（这是 TDD，先写测试）
  - 不要依赖真实图片文件（使用临时文件）
  - 不要测试图片渲染效果（只测试函数返回值）

  **Recommended Agent Profile**:
  - **Category**: `quick`
    - Reason: 编写测试是标准任务
  - **Skills**: [`python-testing`]
    - `python-testing`: pytest 测试编写

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 1 (with T1)
  - **Blocks**: T4
  - **Blocked By**: None (can start immediately)

  **References**:
  - `assets/images/backgrounds/` - 背景图片目录结构
  - Python `base64` 模块 - base64 编码
  - Python `pathlib.Path` - 文件路径处理
  - pytest `tmp_path` fixture - 临时文件

  **Acceptance Criteria**:
  - [ ] 测试文件 `tests/test_background.py` 存在
  - [ ] 运行 `pytest tests/test_background.py -v` 显示所有测试失败（预期）
  - [ ] 测试覆盖：`get_background_base64`, `get_background_style`
  - [ ] 使用临时文件测试，不依赖真实图片

  **QA Scenarios**:

  ```
  Scenario: background 工具测试
    Tool: Bash
    Preconditions: 测试文件已编写
    Steps:
      1. 运行: pytest tests/test_background.py -v
    Expected Result: 所有测试失败（因为实现还未创建）
    Evidence: .sisyphus/evidence/task-2-background-tests.png
  ```

  **Commit**: YES
  - Message: `test(background): add tests for background image utilities`
  - Files: `tests/test_background.py`
  - Pre-commit: `pytest tests/test_background.py` (expect failures)

- [ ] **3. 简化 calculator 只返回天数**

  **What to do**:
  - 修改 `src/calculator.py` 的 `calculate_days_together()` 函数
  - 将返回类型从 `Tuple[int, int, int]` 改为 `int`
  - 移除年月计算逻辑，只保留天数计算
  - 简化后的逻辑：
    ```python
    def calculate_days_together(start_date: str) -> int:
        sd = datetime.strptime(start_date, "%Y-%m-%d").date()
        today = datetime.now(tz=tzlocal()).date()
        if sd > today:
            raise ValueError("Start date cannot be in the future")
        return (today - sd).days
    ```
  - 更新函数文档字符串
  - 移除不再需要的 `add_months` 辅助函数（如果没有其他用途）
  - 运行测试确认全部通过（GREEN 阶段）

  **Must NOT do**:
  - 不要修改其他文件（template.py, main.py 在后续任务处理）
  - 不要保留年月计算（即使注释掉也不行）
  - 不要改变错误处理行为（保持 ValueError）

  **Recommended Agent Profile**:
  - **Category**: `quick`
    - Reason: 函数简化是简单重构
  - **Skills**: [`python-patterns`]
    - `python-patterns`: Python 最佳实践

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 2 (with T4, T5)
  - **Blocks**: T6
  - **Blocked By**: T1 (测试先写好)

  **References**:
  - `src/calculator.py:calculate_days_together` - 当前实现
  - `tests/test_calculator.py` - 已编写的测试（T1 的输出）
  - Python `datetime` - 日期计算

  **Acceptance Criteria**:
  - [ ] `calculate_days_together` 返回 `int` 而非元组
  - [ ] 运行 `pytest tests/test_calculator.py -v` 全部通过
  - [ ] 移除 `add_months` 函数（如果没有其他引用）
  - [ ] 更新函数文档字符串

  **QA Scenarios**:

  ```
  Scenario: 计算器测试通过
    Tool: Bash
    Preconditions: T1 已完成，测试已存在
    Steps:
      1. 运行: pytest tests/test_calculator.py -v
    Expected Result: 所有测试通过 (N passed)
    Evidence: .sisyphus/evidence/task-3-calculator-pass.png

  Scenario: 返回类型验证
    Tool: Bash
    Steps:
      1. 运行: python -c "from src.calculator import calculate_days_together; print(type(calculate_days_together('2023-01-01')))"
    Expected Result: 输出 `<class 'int'>`
    Evidence: .sisyphus/evidence/task-3-return-type.txt
  ```

  **Commit**: YES
  - Message: `refactor(calculator): simplify to return days only`
  - Files: `src/calculator.py`
  - Pre-commit: `pytest tests/test_calculator.py` (must pass)

- [ ] **4. 创建 background.py Base64 工具模块**

  **What to do**:
  - 创建 `src/background.py` 文件
  - 实现 `get_background_base64(image_name: str) -> str` 函数：
    - 从 `assets/images/backgrounds/{image_name}.png` 读取图片
    - 转换为 base64 编码字符串
    - 返回 `data:image/png;base64,{encoded}` 格式
    - 图片不存在时抛出 `FileNotFoundError`
  - 实现 `get_background_style(background_type: str, image_name: str) -> str` 函数：
    - `background_type='gradient'`: 返回 CSS 渐变字符串
    - `background_type='base64_image'`: 返回 base64 图片 URL
  - 运行测试确认全部通过（GREEN 阶段）

  **Must NOT do**:
  - 不要修改 template.py（后续任务处理）
  - 不要硬编码图片路径（使用 Path 构建）
  - 不要处理图片格式转换（只支持 PNG）

  **Recommended Agent Profile**:
  - **Category**: `unspecified-high`
    - Reason: 需要处理文件 I/O 和 base64 编码
  - **Skills**: [`python-patterns`]
    - `python-patterns`: Python 文件处理和编码

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 2 (with T3, T5)
  - **Blocks**: T6
  - **Blocked By**: T2 (测试先写好)

  **References**:
  - `tests/test_background.py` - 已编写的测试（T2 的输出）
  - `assets/images/backgrounds/` - 背景图片目录
  - Python `base64` 模块 - base64 编码
  - Python `pathlib.Path` - 文件路径

  **Acceptance Criteria**:
  - [ ] `src/background.py` 文件存在
  - [ ] `get_background_base64` 函数正确返回 base64 字符串
  - [ ] `get_background_style` 函数支持两种背景类型
  - [ ] 运行 `pytest tests/test_background.py -v` 全部通过

  **QA Scenarios**:

  ```
  Scenario: background 测试通过
    Tool: Bash
    Steps:
      1. 运行: pytest tests/test_background.py -v
    Expected Result: 所有测试通过
    Evidence: .sisyphus/evidence/task-4-background-pass.png

  Scenario: base64 输出验证
    Tool: Bash
    Steps:
      1. 运行: python -c "from src.background import get_background_base64; print(get_background_base64('romantic')[:50])"
    Expected Result: 输出以 `data:image/png;base64,` 开头
    Evidence: .sisyphus/evidence/task-4-base64-output.txt
  ```

  **Commit**: YES
  - Message: `feat(background): add base64 background image utilities`
  - Files: `src/background.py`
  - Pre-commit: `pytest tests/test_background.py` (must pass)

- [ ] **5. 更新 config.yaml 配置示例**

  **What to do**:
  - 更新 `config.yaml` 的 `app` 段添加新配置项：
    ```yaml
    app:
      timezone: "Asia/Shanghai"
      template: "email_new"  # 模板名称: email_new, email, 等
      background_type: "gradient"  # 背景类型: gradient | base64_image
      background_image: "romantic"  # 背景图片名: romantic, minimal, festive
    ```
  - 更新 `config.yaml.example`（如果存在）
  - 更新文档说明新配置项的用途
  - 确保新配置项有默认值处理

  **Must NOT do**:
  - 不要修改 config.py 的加载逻辑（现有逻辑已支持）
  - 不要删除现有配置项
  - 不要破坏现有配置文件格式

  **Recommended Agent Profile**:
  - **Category**: `quick`
    - Reason: 配置文件更新是简单任务
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 2 (with T3, T4)
  - **Blocks**: None (配置示例，不影响其他任务)
  - **Blocked By**: None

  **References**:
  - `config.yaml` - 当前配置文件
  - `config.yaml.example` - 配置示例（如果存在）
  - `src/config.py` - 配置加载逻辑

  **Acceptance Criteria**:
  - [ ] `config.yaml` 包含新的 `app.template` 配置
  - [ ] `config.yaml` 包含新的 `app.background_type` 配置
  - [ ] `config.yaml` 包含新的 `app.background_image` 配置
  - [ ] 配置格式正确，YAML 解析无错误

  **QA Scenarios**:

  ```
  Scenario: 配置 YAML 验证
    Tool: Bash
    Steps:
      1. 运行: python -c "import yaml; yaml.safe_load(open('config.yaml'))"
    Expected Result: 无错误，正常执行
    Evidence: .sisyphus/evidence/task-5-config-valid.txt
  ```

  **Commit**: YES
  - Message: `docs(config): add template and background configuration options`
  - Files: `config.yaml`, `config.yaml.example`

- [ ] **6. 更新 template.py 支持模板选择和背景图**

  **What to do**:
  - 修改 `src/template.py`：
    - 导入 `background` 模块
    - 修改 `get_template_env()` 添加自定义过滤器（如需要）
    - 更新 `render_email_template()` 函数签名，添加 `template_name` 参数
    - 更新 `render_email()` 函数：
      - 从 `context['config']` 读取 `template`, `background_type`, `background_image`
      - 调用 `get_background_style()` 获取背景样式
      - 将背景样式注入模板上下文
      - 根据 `template` 配置选择模板文件
  - 修改 `render_email_template_new()` 添加 `background_style` 参数
  - 确保向后兼容（如果配置不存在使用默认值）

  **Must NOT do**:
  - 不要删除现有函数（保持向后兼容）
  - 不要硬编码模板名称（从配置读取）
  - 不要破坏 main.py 的调用方式

  **Recommended Agent Profile**:
  - **Category**: `deep`
    - Reason: 需要理解现有模板系统并正确集成
  - **Skills**: [`python-patterns`]
    - `python-patterns`: Python 模块集成

  **Parallelization**:
  - **Can Run In Parallel**: NO
  - **Blocked By**: T3, T4, T5

  **References**:
  - `src/template.py` - 当前实现
  - `src/background.py` - T4 的输出
  - `src/calculator.py` - T3 的输出（返回类型已改变）
  - `config.yaml` - T5 的输出（新配置项）
  - `src/main.py` - 调用方（了解 context 结构）

  **Acceptance Criteria**:
  - [ ] `render_email()` 能读取 `app.template` 配置
  - [ ] `render_email()` 能读取 `app.background_type` 和 `app.background_image`
  - [ ] 背景样式正确注入模板上下文
  - [ ] 模板根据配置正确选择

  **QA Scenarios**:

  ```
  Scenario: 模板渲染测试
    Tool: Bash
    Preconditions: T3, T4, T5 已完成
    Steps:
      1. 运行: python -c "
        from src.template import render_email;
        ctx = {
          'config': {'app': {'template': 'email_new', 'background_type': 'gradient', 'background_image': 'romantic'}},
          'days_together': 100,
          'quote': {'content': 'Test', 'category': 'test'},
          'weather': None,
          'date': '2024-01-01'
        };
        html = render_email(ctx);
        print('Rendered successfully')
      "
    Expected Result: 输出 "Rendered successfully"
    Evidence: .sisyphus/evidence/task-6-template-render.txt
  ```

  **Commit**: YES
  - Message: `feat(template): support template selection and background image`
  - Files: `src/template.py`

- [ ] **7. 更新 email_new.html 模板使用背景图变量**

  **What to do**:
  - 修改 `templates/email_new.html`：
    - 将 body 的 `background` 样式从硬编码改为使用 `{{ background_style }}` 变量
    - 原代码：
      ```html
      <body style="... background: linear-gradient(180deg, #FAD4E4 0%, #FDF6F0 50%, #FFF8F5 100%); ...">
      ```
    - 改为：
      ```html
      <body style="... background: {{ background_style }}; ...">
      ```
    - 确保 `background_style` 变量有默认值（兼容旧代码）
  - 如果需要，添加条件判断：
    ```html
    {% if background_style %}
      background: {{ background_style }};
    {% else %}
      background: linear-gradient(...);
    {% endif %}
    ```

  **Must NOT do**:
  - 不要删除 CSS 渐变作为默认选项
  - 不要破坏模板的其他样式
  - 不要修改其他模板文件

  **Recommended Agent Profile**:
  - **Category**: `visual-engineering`
    - Reason: 涉及 HTML/CSS 模板修改
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: NO
  - **Blocked By**: T6

  **References**:
  - `templates/email_new.html` - 当前模板
  - `src/template.py` - T6 的输出（背景样式注入）
  - Jinja2 模板语法

  **Acceptance Criteria**:
  - [ ] `email_new.html` 使用 `{{ background_style }}` 变量
  - [ ] 模板渲染后背景样式正确应用
  - [ ] 没有破坏其他模板元素

  **QA Scenarios**:

  ```
  Scenario: 模板背景变量测试
    Tool: Bash
    Steps:
      1. 运行: python -c "
        from src.template import render_email;
        ctx = {
          'config': {'app': {'template': 'email_new', 'background_type': 'base64_image', 'background_image': 'romantic'}},
          'days_together': 100,
          'quote': {'content': 'Test', 'category': 'test'},
          'weather': None,
          'date': '2024-01-01'
        };
        html = render_email(ctx);
        print('base64' in html or 'data:image' in html)
      "
    Expected Result: 输出 `True`（包含 base64 图片）
    Evidence: .sisyphus/evidence/task-7-template-bg.txt
  ```

  **Commit**: YES
  - Message: `feat(template): use background_style variable in email_new.html`
  - Files: `templates/email_new.html`

---

## Final Verification Wave

- [ ] **F1. 运行全部测试并验证覆盖率**

  **What to do**:
  - 运行 `pytest tests/ -v` 确保所有测试通过
  - 运行 `pytest tests/ --cov=src --cov-report=term` 验证覆盖率 ≥80%
  - 如果覆盖率不足，补充测试
  - 检查是否有遗留的测试失败

  **QA Scenarios**:

  ```
  Scenario: 全部测试通过
    Tool: Bash
    Steps:
      1. 运行: pytest tests/ -v
    Expected Result: 所有测试通过
    Evidence: .sisyphus/evidence/final-all-tests.png

  Scenario: 覆盖率检查
    Tool: Bash
    Steps:
      1. 运行: pytest tests/ --cov=src --cov-report=term --cov-fail-under=80
    Expected Result: 覆盖率 ≥80%，无失败
    Evidence: .sisyphus/evidence/final-coverage.txt
  ```

- [ ] **F2. 干运行测试验证功能**

  **What to do**:
  - 运行 `python src/main.py --dry-run` 验证邮件渲染正常
  - 检查输出 HTML 是否包含正确的天数
  - 切换 `app.background_type` 配置，验证背景变化
  - 切换 `app.template` 配置，验证模板变化

  **QA Scenarios**:

  ```
  Scenario: 干运行验证
    Tool: Bash
    Preconditions: config.yaml 配置正确
    Steps:
      1. 运行: python src/main.py --dry-run
    Expected Result: 正常输出 HTML，无错误
    Evidence: .sisyphus/evidence/final-dry-run.html
  ```

- [ ] **F3. 代码质量检查**

  **What to do**:
  - 运行 `python -m py_compile src/*.py` 确保语法正确
  - 检查是否有未使用的导入
  - 检查代码风格一致性

  **QA Scenarios**:

  ```
  Scenario: 语法检查
    Tool: Bash
    Steps:
      1. 运行: python -m py_compile src/calculator.py src/background.py src/template.py
    Expected Result: 无错误
    Evidence: .sisyphus/evidence/final-syntax.txt
  ```

---

## Commit Strategy

- **T1**: `test(calculator): add tests for simplified days calculation`
- **T2**: `test(background): add tests for background image utilities`
- **T3**: `refactor(calculator): simplify to return days only`
- **T4**: `feat(background): add base64 background image utilities`
- **T5**: `docs(config): add template and background configuration options`
- **T6**: `feat(template): support template selection and background image`
- **T7**: `feat(template): use background_style variable in email_new.html`
- **F1-F3**: `chore: final verification and cleanup`

---

## Success Criteria

### Verification Commands

```bash
# 1. 运行所有测试
pytest tests/ -v

# 2. 检查覆盖率
pytest tests/ --cov=src --cov-report=term --cov-fail-under=80

# 3. 干运行验证
python src/main.py --dry-run

# 4. 语法检查
python -m py_compile src/calculator.py src/background.py src/template.py
```

### Final Checklist

- [ ] 所有测试通过 (`pytest tests/`)
- [ ] 代码覆盖率 ≥80%
- [ ] 干运行正常 (`python src/main.py --dry-run`)
- [ ] 模板配置工作正常 (`app.template`)
- [ ] 背景图配置工作正常 (`app.background_type`, `app.background_image`)
- [ ] 天数计算只返回整数
- [ ] 无语法错误
- [ ] 代码风格一致

---

## Notes

### 配置文件更新示例

更新后的 `config.yaml`：

```yaml
# 邮件配置
email:
  sender: "your_email@qq.com"
  password: "your_auth_code"
  recipient: "partner@example.com"
  smtp_server: "smtp.qq.com"
  smtp_port: 465
  sender_name: "marshmallow"
  recipient_name: "我滴娘子~"

# 恋爱信息
love:
  start_date: "2023-01-01"

# 纪念日列表
anniversaries:
  - name: "恋爱纪念日"
    date: "01-01"

# 天气配置
weather:
  city: "Beijing"
  api_key: "your_api_key"

# 应用配置
app:
  timezone: "Asia/Shanghai"
  template: "email_new"              # 模板选择: email_new, email
  background_type: "gradient"        # 背景类型: gradient | base64_image
  background_image: "romantic"       # 背景图片: romantic, minimal, festive
```

### 环境变量映射

根据 `src/config.py` 的 `_override_env` 逻辑：
- `APP_TEMPLATE` → `cfg.app.template`
- `APP_BACKGROUND_TYPE` → `cfg.app.background_type`
- `APP_BACKGROUND_IMAGE` → `cfg.app.background_image`
