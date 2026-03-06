# 工作计划：添加主卡片背景自定义功能

## TL;DR

> **快速摘要**: 修改邮件模板，让主内容容器的背景支持自定义（纯色、渐变、图片）
> 
> **交付文件**:
> - `templates/email_new.html` - 修改主容器背景为可配置
> - `src/template.py` - 添加卡片背景样式生成逻辑
> - `src/background.py` - 添加卡片背景支持
> - `config.yaml.example` - 添加卡片背景配置示例
> 
> **预计工作量**: 小 (Small)
> **并行执行**: NO - 单任务

---

## Context

### 原始需求
用户希望修改邮件中**主内容卡片**的背景（当前是半透明白色 `rgba(255, 255, 255, 0.6)`），而不是整个页面的背景。

### 当前状态
- 页面背景 (`body`) 已经支持通过 `background_style` 自定义
- 主内容容器背景是固定的半透明白色
- 需要让主卡片也支持：纯色、渐变、图片背景

---

## Work Objectives

### Core Objective
让邮件主内容容器的背景支持自定义，类型包括纯色、渐变、图片。

### Concrete Deliverables
1. 修改 `templates/email_new.html` - 主容器背景使用变量
2. 修改 `src/template.py` - 添加 `card_background_style` 生成逻辑
3. 修改 `src/background.py` - 支持生成卡片背景样式
4. 修改 `config.yaml.example` - 添加卡片背景配置示例

### Definition of Done
- [ ] 可以通过配置设置主卡片背景为纯色
- [ ] 可以通过配置设置主卡片背景为渐变
- [ ] 可以通过配置设置主卡片背景为图片
- [ ] 运行脚本后生成的 HTML 反映卡片背景变化

---

## Execution Strategy

### Task Sequence
```
Task 1: 修改 background.py 添加卡片背景支持
    ↓
Task 2: 修改 template.py 添加卡片背景样式生成
    ↓
Task 3: 修改 email_new.html 主容器使用变量
    ↓
Task 4: 更新 config.yaml.example 添加配置示例
    ↓
Task 5: 测试验证
```

---

## TODOs

- [x] **1. 修改 src/background.py**

  **What to do**:
  - 修改 `get_background_style` 函数，支持更多背景类型
  - 添加 `get_card_background_style` 函数，专门处理卡片背景
  - 支持类型：
    - `solid`: 纯色，如 `#FFFFFF` 或 `rgba(255,255,255,0.8)`
    - `gradient`: 渐变，如 `linear-gradient(...)`
    - `image`: 图片背景
  
  **References**:
  - `src/background.py:20-28` - 当前 `get_background_style` 实现
  
  **Acceptance Criteria**:
  - [x] 新增 `get_card_background_style(type, value)` 函数
  - [x] 支持返回纯色背景 CSS
  - [x] 支持返回渐变背景 CSS
  - [x] 支持返回图片背景 CSS (base64)

- [x] **2. 修改 src/template.py**

  **What to do**:
  - 在 `render_email` 函数中，读取卡片背景配置
  - 调用 `get_card_background_style` 生成卡片背景样式
  - 将 `card_background_style` 添加到 context 中
  
  **References**:
  - `src/template.py:104-138` - `render_email` 函数
  - `src/template.py:140-170` - `render_email_template_new` 函数
  
  **Acceptance Criteria**:
  - [x] 从配置中读取 `card_background_type` 和 `card_background_value`
  - [x] 生成 `card_background_style` 并加入 context
  - [x] 默认值保持当前样式 `rgba(255, 255, 255, 0.6)`

- [x] **3. 修改 templates/email_new.html**

  **What to do**:
  - 找到主容器（第38行）
  - 将固定背景 `background: rgba(255, 255, 255, 0.6)` 改为使用变量
  - 使用 `{{ card_background_style|default('rgba(255, 255, 255, 0.6)') }}`
  
  **References**:
  - `templates/email_new.html:38` - 主容器样式
  
  **Acceptance Criteria**:
  - [x] 主容器背景使用 `card_background_style` 变量
  - [x] 保持向后兼容（有默认值）

- [x] **4. 更新 config.yaml.example**

  **What to do**:
  - 在 `app` 配置段添加卡片背景配置示例
  - 添加注释说明各种背景类型的用法
  
  **Acceptance Criteria**:
  - [x] 添加 `card_background_type` 配置项
  - [x] 添加 `card_background_value` 配置项
  - [x] 添加注释说明可选值：solid/gradient/image

- [x] **5. 测试验证**

  **What to do**:
  - 运行 `python scripts/generate_email.py` 测试默认样式
  - 修改 config.yaml 测试不同背景类型
  - 验证生成的 HTML 正确反映背景变化
  
  **QA Scenarios**:
  ```
  Scenario: 测试纯色背景
    Tool: Bash
    Steps:
      1. 设置 card_background_type: solid
      2. 设置 card_background_value: "#FFE4E1"
      3. 运行 python scripts/generate_email.py
    Expected Result: 主卡片背景为粉色纯色
    Evidence: 查看生成的 HTML 文件
  
  Scenario: 测试渐变背景
    Tool: Bash
    Steps:
      1. 设置 card_background_type: gradient
      2. 设置 card_background_value: "linear-gradient(135deg, #FFE4E1 0%, #FFF0F5 100%)"
    Expected Result: 主卡片背景为渐变
  
  Scenario: 测试图片背景
    Tool: Bash
    Steps:
      1. 放置图片到 assets/images/backgrounds/
      2. 设置 card_background_type: image
      3. 设置 card_background_value: "card_bg"
    Expected Result: 主卡片背景为图片
  ```

---

## Success Criteria

### Verification Commands
```bash
# 1. 生成邮件预览
python scripts/generate_email.py

# 2. 检查 HTML 中的主容器背景样式
grep -A 5 'class="container"' output/email_*.html

# 3. 验证背景样式正确应用
```

### Final Checklist
- [x] 纯色背景配置正常工作
- [x] 渐变背景配置正常工作
- [x] 图片背景配置正常工作
- [x] 默认样式保持向后兼容
