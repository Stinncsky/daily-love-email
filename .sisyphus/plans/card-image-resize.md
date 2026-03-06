# 工作计划：卡片背景图片自适应容器大小

## TL;DR

> **快速摘要**: 修改卡片背景图片，使其能够自适应容器大小（使用 CSS background-size: cover）
> 
> **交付文件**:
> - `src/background.py` - 修改返回完整的背景样式（包含 background-size）
> - `templates/email_new.html` - 为卡片容器添加 background-size 属性
> - `config.yaml.example` - 添加图片自适应配置示例
> 
> **预计工作量**: 小 (Small)
> **并行执行**: NO - 单任务

---

## Context

### 原始需求
用户希望卡片背景图片能够自适应容器大小，即图片能够填满整个卡片区域。

### 当前状态
- 卡片背景已经支持图片类型（通过 base64 编码）
- 但图片没有设置 background-size，可能无法完全覆盖卡片
- 需要添加 `background-size: cover` 让图片自适应

### 技术方案
- 对于**纯色和渐变**背景：不需要 background-size
- 对于**图片背景**：需要添加 `background-size: cover` 和 `background-position: center`

---

## Work Objectives

### Core Objective
让图片类型的卡片背景能够自适应容器大小，完整覆盖卡片区域。

### Concrete Deliverables
1. 修改 `src/background.py` - 当类型为 image 时，返回包含 background-size 的完整样式
2. 修改 `templates/email_new.html` - 为图片背景添加 background-size 属性
3. 更新 `config.yaml.example` - 添加图片自适应的注释说明

### Definition of Done
- [ ] 图片背景能够完全覆盖卡片容器
- [ ] 图片保持原始比例（不拉伸变形）
- [ ] 纯色/渐变背景不受影响

---

## Execution Strategy

### Task Sequence
```
Task 1: 修改 background.py - 支持返回 background-size
    ↓
Task 2: 修改 email_new.html - 添加 background-size 样式
    ↓
Task 3: 更新 config.yaml.example - 添加注释说明
    ↓
Task 4: 测试验证 - 验证图片自适应效果
```

---

## TODOs

- [ ] **1. 修改 src/background.py**

  **What to do**:
  - 修改 `get_card_background_style` 函数
  - 当 `background_type == "image"` 时，返回完整的 CSS 样式字符串：
    - 包含 `background-image: url(...)`
    - 包含 `background-size: cover`
    - 包含 `background-position: center`
    - 包含 `background-repeat: no-repeat`
  - 保持纯色和渐变类型返回原来的值
  
  **References**:
  - `src/background.py:31-62` - 当前 `get_card_background_style` 实现
  
  **Acceptance Criteria**:
  - [ ] Image 类型返回完整的 CSS 背景样式（包含 size/position/repeat）
  - [ ] Solid 和 gradient 类型保持原样（只返回颜色值）
  - [ ] 函数签名保持不变，向后兼容

- [ ] **2. 修改 templates/email_new.html**

  **What to do**:
  - 修改第 38 行主容器的样式
  - 当背景是图片时，需要分别设置 background-image 和 background-size 等属性
  - 方案：使用条件判断，如果 card_background_type 是 image，则使用完整的样式字符串
  
  **References**:
  - `templates/email_new.html:38` - 主容器样式
  
  **Acceptance Criteria**:
  - [ ] 图片背景能够完整覆盖卡片容器
  - [ ] 纯色/渐变背景正常工作
  - [ ] 邮件在常见客户端正常显示

- [ ] **3. 更新 config.yaml.example**

  **What to do**:
  - 在图片背景配置示例旁边添加注释
  - 说明图片会自动自适应容器大小（cover 模式）
  
  **Acceptance Criteria**:
  - [ ] 注释说明图片会自动填满卡片
  - [ ] 用户了解不需要额外配置

- [ ] **4. 测试验证**

  **What to do**:
  - 准备一张测试图片（放到 assets/images/backgrounds/）
  - 配置图片背景，生成邮件
  - 验证图片是否正确覆盖整个卡片
  
  **QA Scenarios**:
  ```
  Scenario: 测试图片背景自适应
    Tool: Bash
    Steps:
      1. 准备一张 800x600 的图片到 assets/images/backgrounds/test_card.png
      2. 配置 card_background_type: image
      3. 配置 card_background_value: "test_card"
      4. 运行 python scripts/generate_email.py
      5. 用浏览器打开生成的 HTML
    Expected Result: 
      - 图片覆盖整个卡片区域
      - 图片保持比例，没有拉伸变形
      - 卡片内容（文字等）正常显示在图片上方
    Evidence: 截图保存到 .sisyphus/evidence/
  
  Scenario: 测试纯色背景不受影响
    Tool: Bash
    Steps:
      1. 配置 card_background_type: solid
      2. 配置 card_background_value: "#FFE4E1"
      3. 运行 python scripts/generate_email.py
    Expected Result: 卡片背景为纯色，没有 background-size 相关样式
  
  Scenario: 测试渐变背景不受影响
    Tool: Bash
    Steps:
      1. 配置 card_background_type: gradient
      2. 配置 card_background_value: "linear-gradient(135deg, #FFE4E1 0%, #FFF0F5 100%)"
      3. 运行 python scripts/generate_email.py
    Expected Result: 卡片背景为渐变，没有 background-size 相关样式
  ```

---

## Implementation Notes

### CSS 属性说明
- `background-size: cover` - 保持图片比例，填满容器，可能裁剪边缘
- `background-position: center` - 图片居中显示
- `background-repeat: no-repeat` - 不重复平铺

### 邮件客户端兼容性
- 现代邮件客户端（Apple Mail、iOS Mail、Outlook for Mac）支持良好
- Gmail Web 支持 background-size
- Outlook for Windows 支持有限，但会回退到默认背景

### 实现方案选择

**方案 A：修改 HTML 模板（推荐）**
- 在模板中添加 style 属性，根据类型条件渲染
- 保持 Python 代码简洁
- 模板逻辑清晰

**方案 B：修改 background.py**
- 让 `get_card_background_style` 返回对象或元组
- 需要同步修改 template.py 和 HTML

采用**方案 A**，在 HTML 模板中处理条件渲染。

---

## Success Criteria

### Verification Commands
```bash
# 1. 生成邮件预览（图片背景）
python scripts/generate_email.py

# 2. 检查 HTML 中的样式
# 对于图片背景，应该包含 background-size: cover
grep -o 'background-size' output/email_*.html

# 3. 验证纯色/渐变背景没有多余样式
grep -v 'background-size' output/email_*.html | head -5
```

### Final Checklist
- [ ] 图片背景覆盖整个卡片容器
- [ ] 纯色背景正常工作（无 background-size）
- [ ] 渐变背景正常工作（无 background-size）
- [ ] 卡片内容可读性良好（backdrop-filter 保持）
