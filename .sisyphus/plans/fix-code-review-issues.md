# 代码审查问题修复计划

## TL;DR

> **目标**: 修复代码审查中发现的 3 个 Critical、6 个 Major 和 4 个 Minor 问题
> 
> **交付物**: 修复后的代码、新增测试、更新的文档
> 
> **预计工作量**: 中等（6-8 个任务波次）
> 
> **关键路径**: Workflow修复 → 天数计算修复 → 测试验证 → 邮件兼容性修复

---

## Context

### 审查来源
双模型代码审查（Codex + Gemini）发现的问题，涉及：
- **后端逻辑**: Python代码质量、错误处理、测试覆盖
- **前端模板**: 邮件HTML可访问性、CSS兼容性
- **CI/CD**: GitHub Actions配置

### 问题统计
| 级别 | 数量 | 状态 |
|-----|------|------|
| 🔴 Critical | 3 | 必须修复 |
| 🟠 Major | 6 | 强烈建议修复 |
| 🟡 Minor | 4 | 建议修复 |

---

## Work Objectives

### 核心目标
修复所有 Critical 问题，确保代码可合并且生产环境稳定运行。

### 具体交付物
1. 修复后的 `src/main.py`（天数计算、异常处理）
2. 修复后的 `.github/workflows/daily-email.yml`（缩进）
3. 修复后的邮件模板（无障碍属性、CSS兼容性）
4. 增强的测试覆盖
5. 清理后的代码（未使用导入等）

### 定义完成标准
- [ ] 所有 Critical 问题已修复并验证
- [ ] 原有测试通过 + 新增测试通过
- [ ] GitHub Actions workflow 语法验证通过
- [ ] 邮件模板在主流客户端正常显示

### 必须完成 (Must Have)
- 天数计算回归修复
- Workflow YAML 缩进修复
- 表格无障碍属性添加

### 必须不做 (Must NOT Have)
- 不引入新功能
- 不改变原有业务逻辑（仅修复bug）
- 不重构未涉及模块

---

## Verification Strategy

### 测试策略
- **单元测试**: 修复后运行 `pytest tests/`
- **集成测试**: 端到端 dry-run 测试
- **YAML验证**: `actionlint` 或 GitHub 语法检查
- **邮件兼容性**: 多客户端预览测试

### QA策略
每个修复任务包含 Agent-Executed QA Scenarios
- 代码修复 → 运行测试 → 验证输出
- 模板修复 → 生成预览 → 浏览器验证
- Workflow修复 → YAML语法检查

---

## Execution Strategy

### 并行执行波次

```
Wave 1 (Critical - 立即开始):
├── Task 1: 修复 Workflow YAML 缩进 [quick]
├── Task 2: 修复天数计算回归 [quick]
└── Task 3: 修复 calculator 异常类型 [quick]

Wave 2 (Critical - 依赖Wave 1):
├── Task 4: 修复邮件模板无障碍属性 [visual-engineering]
└── Task 5: 修复 ANNIVERSARIES 类型解析 [quick]

Wave 3 (Major - 可并行):
├── Task 6: 增强天气解析容错性 [unspecified-high]
├── Task 7: 修复邮件 CSS 兼容性 [visual-engineering]
└── Task 8: 添加 Outlook VML 后备 [visual-engineering]

Wave 4 (测试和清理):
├── Task 9: 增强测试覆盖 [deep]
└── Task 10: 修复 Minor 问题 [quick]

Wave FINAL (验证):
├── Task F1: 全量测试验证
└── Task F2: 代码质量检查
```

### 依赖矩阵
- Task 2 → Task 9 (测试需要修复后的代码)
- Task 4 → Task 7 (CSS修复依赖模板结构)
- Task 3 → Task 9

---

## TODOs

### Wave 1: Critical 修复

- [x] **1. 修复 Workflow YAML 缩进错误**

  **What to do**:
  - 修复 `.github/workflows/daily-email.yml` 第51行缩进
  - 将 `DRY_RUN`, `CARD_BACKGROUND_TYPE`, `CARD_BACKGROUND_VALUE` 正确缩进到 `env:` 下
  
  **Current (错误)**:
  ```yaml
            CITY: ${{ secrets.CITY }}
            ANNIVERSARIES: ${{ secrets.ANNIVERSARIES }}
    DRY_RUN: ${{ github.event.inputs.dry_run }}
    CARD_BACKGROUND_TYPE: ${{ secrets.CARD_BACKGROUND_TYPE }}
  ```
  
  **Expected (正确)**:
  ```yaml
            CITY: ${{ secrets.CITY }}
            ANNIVERSARIES: ${{ secrets.ANNIVERSARIES }}
            DRY_RUN: ${{ github.event.inputs.dry_run }}
            CARD_BACKGROUND_TYPE: ${{ secrets.CARD_BACKGROUND_TYPE }}
  ```

  **Must NOT do**:
  - 不改变其他 workflow 配置
  - 不添加新功能

  **Recommended Agent Profile**:
  - **Category**: `quick`
  - **Skills**: 无需特殊技能

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 1
  - **Blocked By**: None
  - **Blocks**: None

  **Acceptance Criteria**:
  - [ ] YAML 语法检查通过（无缩进错误）
  - [ ] `actionlint` 或类似工具验证通过
  - [ ] GitHub Actions 编辑器无错误提示

  **QA Scenario**:
  ```
  Scenario: Workflow YAML语法正确
    Tool: Bash
    Steps:
      1. 运行 yamllint 或 actionlint
      2. 验证无 syntax error
    Expected Result: 返回 exit code 0，无错误输出
    Evidence: .sisyphus/evidence/task-1-yaml-valid.txt
  ```

  **Commit**: YES
  - Message: `fix(ci): correct workflow env indentation`
  - Files: `.github/workflows/daily-email.yml`

---

- [x] **2. 修复天数计算回归问题**

  **What to do**:
  - `src/calculator.py` 的 `calculate_days_together` 返回 `int`（天数）
  - 但 `src/main.py` 第179-183行仍按 tuple 解包 `days, months, years`
  - 需要统一返回格式或修改调用方式

  **Current (错误)**:
  ```python
  # src/main.py:179-183
  days, months, years = calculate_days_together(love_start_date)
  # 但 calculator.py 返回的是 int（仅days）
  ```

  **Fix Options**:
  - Option A: 修改 calculator.py 返回 tuple `(days, months, years)`
  - Option B: 修改 main.py 只接收 days，自行计算 months/years
  - **推荐 Option A**（更完整）

  **Must NOT do**:
  - 不改变计算逻辑，只修复返回格式
  - 不修改日期计算算法

  **Recommended Agent Profile**:
  - **Category**: `quick`
  - **Skills**: `python-patterns`

  **Parallelization**:
  - **Can Run In Parallel**: YES (Wave 1)
  - **Blocked By**: None
  - **Blocks**: Task 9 (测试覆盖)

  **References**:
  - `src/calculator.py:4` - 函数定义
  - `src/main.py:179-183` - 调用点

  **Acceptance Criteria**:
  - [ ] `calculate_days_together` 返回 `(days, months, years)` tuple
  - [ ] main.py 解包正确
  - [ ] 测试 `test_calculator.py` 通过
  - [ ] 集成测试验证实际计算结果正确

  **QA Scenario**:
  ```
  Scenario: 天数计算返回正确tuple
    Tool: Bash (python)
    Steps:
      1. python -c "from src.calculator import calculate_days_together; print(calculate_days_together('2020-01-01'))"
      2. 验证返回值为 (days, months, years) 格式
    Expected Result: 返回3个整数的tuple，如 (1850, 60, 5)
    Evidence: .sisyphus/evidence/task-2-calculator.txt
  ```

  **Commit**: YES
  - Message: `fix(calculator): return tuple with days/months/years`
  - Files: `src/calculator.py`, `src/main.py`
  - Pre-commit: `python -m pytest tests/test_calculator.py -v`

---

- [x] **3. 修复 calculator 异常类型错误**

  **What to do**:
  - `src/calculator.py:15-18` 异常分支触发 `AttributeError`
  - 应抛出 `ValueError` 而非 `AttributeError`
  - 检查异常处理逻辑

  **Current (问题)**:
  ```python
  # 当 date_str 格式错误时，可能触发 AttributeError
  # 应该明确抛出 ValueError
  ```

  **Must NOT do**:
  - 不改变正常流程逻辑
  - 不修改成功路径

  **Recommended Agent Profile**:
  - **Category**: `quick`
  - **Skills**: `python-patterns`

  **Parallelization**:
  - **Can Run In Parallel**: YES (Wave 1)

  **Acceptance Criteria**:
  - [ ] 输入非法日期时抛出 `ValueError`
  - [ ] 不抛出 `AttributeError`
  - [ ] 错误消息清晰明确

  **QA Scenario**:
  ```
  Scenario: 非法日期输入抛出ValueError
    Tool: Bash (python)
    Steps:
      1. python -c "from src.calculator import calculate_days_together; calculate_days_together('invalid-date')"
    Expected Result: 抛出 ValueError，不是 AttributeError
    Evidence: .sisyphus/evidence/task-3-exception.txt
  ```

  **Commit**: YES (可与 Task 2 合并)
  - Message: `fix(calculator): correct exception type for invalid input`
  - Files: `src/calculator.py`

---

### Wave 2: Critical 模板修复

- [x] **4. 修复邮件模板无障碍属性**

  **What to do**:
  - 为 `templates/email.html` 和 `email_new.html` 中的所有布局 `<table>` 添加 `role="presentation"`
  - 修复装饰性图片的 `alt` 属性（`alt="♥"` → `alt=""`）

  **Implementation**:
  ```html
  <!-- Before -->
  <table border="0" cellpadding="0" cellspacing="0">
  
  <!-- After -->
  <table role="presentation" border="0" cellpadding="0" cellspacing="0">
  ```

  **Must NOT do**:
  - 不改变视觉设计
  - 不修改表格结构
  - 只添加属性

  **Recommended Agent Profile**:
  - **Category**: `visual-engineering`
  - **Skills**: `ui-ux-pro-max`

  **Parallelization**:
  - **Can Run In Parallel**: YES (Wave 2)
  - **Blocked By**: None
  - **Blocks**: Task 7 (CSS修复依赖模板)

  **Acceptance Criteria**:
  - [ ] 所有布局表格都有 `role="presentation"`
  - [ ] 装饰性图片 `alt=""`
  - [ ] 模板渲染正常

  **QA Scenario**:
  ```
  Scenario: 模板包含无障碍属性
    Tool: Grep
    Steps:
      1. grep -n 'role="presentation"' templates/email.html templates/email_new.html | wc -l
      2. 统计表格总数
    Expected Result: 布局表格100%包含role属性
    Evidence: .sisyphus/evidence/task-4-a11y.txt
  ```

  **Commit**: YES
  - Message: `fix(template): add accessibility attributes to email templates`
  - Files: `templates/email.html`, `templates/email_new.html`

---

- [x] **5. 修复 ANNIVERSARIES 类型解析**

  **What to do**:
  - `src/config.py:41-43` 环境变量 `ANNIVERSARIES` 被当作字符串而非 list
  - 需要添加 JSON 解析逻辑

  **Implementation**:
  ```python
  # 在 config.py 中
  if isinstance(anniversaries_str, str):
      import json
      try:
          anniversaries = json.loads(anniversaries_str)
      except json.JSONDecodeError:
          anniversaries = []
  ```

  **Must NOT do**:
  - 不改变配置结构
  - 不修改其他配置项

  **Recommended Agent Profile**:
  - **Category**: `quick`
  - **Skills**: `python-patterns`

  **Parallelization**:
  - **Can Run In Parallel**: YES (Wave 2)

  **Acceptance Criteria**:
  - [ ] 环境变量字符串正确解析为 list
  - [ ] JSON 解析错误时优雅降级（空列表）
  - [ ] 原有 dict 配置路径仍工作

  **QA Scenario**:
  ```
  Scenario: ANNIVERSARIES环境变量正确解析
    Tool: Bash (python)
    Steps:
      1. ANNIVERSARIES='[{"name": "test", "date": "01-01"}]' python -c "
         import os
         from src.config import load_config
         os.environ['ANNIVERSARIES'] = '[{\"name\": \"test\", \"date\": \"01-01\"}]'
         config = load_config()
         print(type(config.get('anniversaries')))
         print(config.get('anniversaries'))
         "
    Expected Result: 类型为 list，内容正确解析
    Evidence: .sisyphus/evidence/task-5-config.txt
  ```

  **Commit**: YES
  - Message: `fix(config): parse ANNIVERSARIES env var as JSON list`
  - Files: `src/config.py`

---

### Wave 3: Major 问题修复

- [x] **6. 增强天气解析容错性**

  **What to do**:
  - `src/weather.py:39,84` 对 `dt_txt` 解析缺少单条容错
  - 任意脏数据导致整体返回 `None`
  - 改为"单条失败跳过"模式

  **Implementation**:
  ```python
  # 单条解析失败时跳过，不要全局 except
  for item in forecast_list:
      try:
          dt_txt = item['dt_txt']
          # 解析逻辑
      except (KeyError, ValueError) as e:
          logger.warning(f"Skip invalid forecast item: {e}")
          continue
  ```

  **Must NOT do**:
  - 不修改 API 调用逻辑
  - 不改变正常数据解析

  **Recommended Agent Profile**:
  - **Category**: `unspecified-high`
  - **Skills**: `python-patterns`

  **Parallelization**:
  - **Can Run In Parallel**: YES (Wave 3)

  **Acceptance Criteria**:
  - [ ] 单条脏数据不导致整体失败
  - [ ] 脏数据被记录日志并跳过
  - [ ] 有效数据正常返回

  **QA Scenario**:
  ```
  Scenario: 天气数据容错处理
    Tool: Bash (python)
    Steps:
      1. 创建测试用例包含脏数据
      2. 调用天气解析函数
    Expected Result: 跳过脏数据，返回有效数据
    Evidence: .sisyphus/evidence/task-6-weather.txt
  ```

  **Commit**: YES
  - Message: `fix(weather): add per-item error handling for forecast data`
  - Files: `src/weather.py`
  - Pre-commit: `python -m pytest tests/test_weather.py -v`

---

- [x] **7. 修复邮件 CSS 兼容性问题**

  **What to do**:
  - `email_new.html` 使用 `backdrop-filter` 和 `box-shadow`
  - 主流邮件客户端会剥离这些属性
  - 添加 fallback 样式

  **Implementation**:
  ```css
  /* 添加 fallback 背景色 */
  .glass-card {
      background: rgba(255, 255, 255, 0.9); /* fallback */
      backdrop-filter: blur(10px); /* 现代浏览器 */
      box-shadow: 0 4px 6px rgba(0,0,0,0.1); /* 可能失效 */
  }
  ```

  **Must NOT do**:
  - 不改变视觉效果（现代浏览器）
  - 只添加 fallback

  **Recommended Agent Profile**:
  - **Category**: `visual-engineering`
  - **Skills**: `ui-ux-pro-max`

  **Parallelization**:
  - **Can Run In Parallel**: YES (Wave 3)
  - **Blocked By**: Task 4

  **Acceptance Criteria**:
  - [ ] 有 fallback 背景色
  - [ ] 现代浏览器仍显示毛玻璃效果
  - [ ] 邮件客户端有可读背景

  **QA Scenario**:
  ```
  Scenario: 邮件模板有CSS fallback
    Tool: Grep
    Steps:
      1. 检查 email_new.html 中的 fallback 样式
    Expected Result: 关键样式都有fallback
    Evidence: .sisyphus/evidence/task-7-css-compat.txt
  ```

  **Commit**: YES (可与 Task 8 合并)
  - Message: `fix(template): add CSS fallback for email clients`
  - Files: `templates/email_new.html`

---

- [x] **8. 添加 Outlook VML 后备方案**

  **What to do**:
  - Windows Outlook 使用 Word 引擎，不支持 CSS `background-image`
  - 为卡片背景添加 VML (Vector Markup Language) 后备

  **Implementation**:
  ```html
  <!--[if mso]>
  <v:rect xmlns:v="urn:schemas-microsoft-com:vml" fill="true" stroke="false" style="width:600px;height:300px;">
  <v:fill type="tile" src="background.png" color="#FFE4E1" />
  <v:textbox inset="0,0,0,0">
  <![endif]-->
  
  <!-- 正常 HTML 内容 -->
  
  <!--[if mso]>
  </v:textbox>
  </v:rect>
  <![endif]-->
  ```

  **Must NOT do**:
  - 不改变现代浏览器显示效果
  - VML 只作为后备

  **Recommended Agent Profile**:
  - **Category**: `visual-engineering`
  - **Skills**: `ui-ux-pro-max`

  **Parallelization**:
  - **Can Run In Parallel**: YES (Wave 3)

  **Acceptance Criteria**:
  - [ ] 包含 VML 条件注释
  - [ ] Outlook 显示背景色/图
  - [ ] 其他客户端正常显示

  **QA Scenario**:
  ```
  Scenario: 模板包含Outlook VML后备
    Tool: Grep
    Steps:
      1. grep -n 'vml\|mso' templates/email_new.html
    Expected Result: 包含VML条件注释
    Evidence: .sisyphus/evidence/task-8-vml.txt
  ```

  **Commit**: YES
  - Message: `feat(template): add VML fallback for Outlook background`
  - Files: `templates/email_new.html`

---

### Wave 4: 测试和清理

- [x] **9. 增强测试覆盖**

  **What to do**:
  - 为以下场景添加测试：
    1. `main + calculator` 接口兼容
    2. `ANNIVERSARIES` 环境变量 JSON 解析
    3. 天气解析容错（脏数据）
    4. Workflow 结构验证（YAML语法）

  **Implementation**:
  ```python
  # tests/test_integration.py
  def test_calculator_returns_tuple():
      result = calculate_days_together('2020-01-01')
      assert isinstance(result, tuple)
      assert len(result) == 3
  
  def test_anniversaries_env_parsing():
      # 测试环境变量解析
      pass
  
  def test_weather_forecast_error_handling():
      # 测试容错
      pass
  ```

  **Must NOT do**:
  - 不测试已实现的功能（避免重复）
  - 专注新增测试

  **Recommended Agent Profile**:
  - **Category**: `deep`
  - **Skills**: `python-testing`, `tdd-workflow`

  **Parallelization**:
  - **Can Run In Parallel**: YES (Wave 4)
  - **Blocked By**: Task 2, 3, 5, 6

  **Acceptance Criteria**:
  - [ ] 新增测试覆盖率 ≥ 80%
  - [ ] 所有测试通过
  - [ ] 集成测试覆盖 dry-run 场景

  **QA Scenario**:
  ```
  Scenario: 测试覆盖率达标
    Tool: Bash
    Steps:
      1. python -m pytest tests/ --cov=src --cov-report=term-missing
    Expected Result: 覆盖率 >= 80%，无失败测试
    Evidence: .sisyphus/evidence/task-9-coverage.txt
  ```

  **Commit**: YES
  - Message: `test: add coverage for calculator, config, and weather`
  - Files: `tests/test_calculator.py`, `tests/test_config.py`, `tests/test_weather.py`

---

- [x] **10. 修复 Minor 问题**

  **What to do**:
  - [ ] 移除 `src/calculator.py` 未使用的 `tzlocal` 导入
  - [ ] 优化 `src/main.py` `safe_call` 过度兜底问题
  - [ ] 修复 `README.md` cron 描述与 workflow 不一致
  - [ ] 修复装饰性图标 `alt` 属性

  **Must NOT do**:
  - 不改变业务逻辑

  **Recommended Agent Profile**:
  - **Category**: `quick`
  - **Skills**: `python-patterns`

  **Parallelization**:
  - **Can Run In Parallel**: YES (Wave 4)

  **Acceptance Criteria**:
  - [ ] 无未使用导入
  - [ ] README 描述准确
  - [ ] 代码质量检查通过

  **QA Scenario**:
  ```
  Scenario: 代码清理完成
    Tool: Bash
    Steps:
      1. flake8 src/ --select=F401 (检查未使用导入)
      2. grep -n 'cron' README.md
    Expected Result: 无F401错误，README描述准确
    Evidence: .sisyphus/evidence/task-10-cleanup.txt
  ```

  **Commit**: YES
  - Message: `chore: cleanup unused imports and fix docs`
  - Files: `src/calculator.py`, `src/main.py`, `README.md`

---

## Final Verification Wave

- [x] **F1. 全量测试验证**

  **Agent Profile**: `oracle`
  
  **What to do**:
  1. 运行完整测试套件
  2. 验证所有 Critical/Major 问题已修复
  3. 执行端到端 dry-run
  
  **Acceptance Criteria**:
  - [x] `pytest tests/` 全部通过 (65 passed)
  - [x] `python src/main.py --dry-run` 正常工作
  - [x] YAML 语法检查通过
  - [x] 邮件预览生成正常

- [x] **F2. 代码质量检查**

  **Agent Profile**: `unspecified-high`
  
  **What to do**:
  1. 运行 linter (flake8/pylint)
  2. 类型检查 (mypy，如有)
  3. 安全检查 (bandit)
  
  **Acceptance Criteria**:
  - [x] 无 Critical/High 级别问题 (只有风格警告)
  - [x] 代码风格一致

---

## Commit Strategy

```
Wave 1:
  - fix(ci): correct workflow env indentation
  - fix(calculator): return tuple with days/months/years
  - fix(calculator): correct exception type for invalid input

Wave 2:
  - fix(template): add accessibility attributes to email templates
  - fix(config): parse ANNIVERSARIES env var as JSON list

Wave 3:
  - fix(weather): add per-item error handling for forecast data
  - fix(template): add CSS fallback for email clients
  - feat(template): add VML fallback for Outlook background

Wave 4:
  - test: add coverage for calculator, config, and weather
  - chore: cleanup unused imports and fix docs

Final:
  - refactor: final polish based on code review
```

---

## Success Criteria

### 验收检查清单
- [ ] **Critical 问题**: 3/3 修复并验证
- [ ] **Major 问题**: 至少 4/6 修复（建议全部）
- [ ] **Minor 问题**: 至少 2/4 修复
- [ ] **测试**: 全部通过，覆盖率 ≥ 80%
- [ ] **CI/CD**: Workflow YAML 语法正确
- [ ] **文档**: README 和代码注释准确

### 验证命令
```bash
# 1. 测试
python -m pytest tests/ -v

# 2. YAML检查
actionlint .github/workflows/daily-email.yml

# 3. 代码质量
flake8 src/ --max-line-length=100

# 4. 功能验证
python src/main.py --dry-run

# 5. 生成邮件预览
python scripts/generate_email.py
```

---

## Risk Assessment

| 风险 | 可能性 | 影响 | 缓解措施 |
|-----|-------|------|---------|
| 修复引入新问题 | 中 | 中 | 充分测试，小步提交 |
| 邮件兼容性测试不充分 | 高 | 中 | 多客户端预览验证 |
| Workflow修复后仍有问题 | 低 | 高 | YAML语法工具验证 |

---

## Notes

- 所有修复应基于最新代码分支
- 每个任务完成后更新 TODO 状态
- 遇到阻塞问题及时升级
- 保持代码风格一致性
