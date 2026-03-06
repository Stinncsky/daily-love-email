# 重新设计邮件UI工作计划

## 目标

根据用户提供的设计参考图和背景图，重新设计每日爱情邮件的UI界面，采用粉色浪漫风格的卡片式布局。

---

## 当前状态

**项目技术栈：**
- Python 3.10+
- Jinja2 模板引擎
- SMTP 邮件发送
- GitHub Actions 自动部署

**现有模板位置：**
- `templates/email.html` - 当前邮件模板
- `src/template.py` - 模板渲染逻辑

**已有资源：**
- `background_1.png` - 粉色浪漫风格背景图

---

## 设计方案

### 参考图片设计分析

从参考图可以看出，新UI设计特点：
1. **整体风格**：粉色浪漫风格，带有玫瑰花装饰边框
2. **顶部**：心形+月桂叶装饰图案
3. **主体布局**：
   - 问候语："亲爱的 {{ recipient_name }}"
   - 日期显示
   - 恋爱天数卡片："我们已经相爱了 [大数字] 天"
   - 天气信息卡片：位置图标 + 城市 + 温度
   - 情话卡片：带引号装饰的引用样式
   - 底部分隔线 + 心形装饰
   - 署名："爱你的 {{ sender_name }}" + 日期

### 资源存放规划

```
auto-email/
├── assets/                    # 静态资源目录
│   ├── images/               # 图片资源
│   │   ├── background_1.png  # 主背景图（已移动）
│   │   ├── heart_icon.png    # 心形图标（如需要）
│   │   └── flowers/          # 花卉装饰（可选）
│   └── fonts/                # 自定义字体（可选）
├── templates/                # 邮件模板
│   ├── email.html           # 当前模板（保留备份）
│   └── email_v2.html        # 新模板（新建）
└── src/                     # 源代码
    └── template.py          # 模板渲染逻辑（更新）
```

**资源存放规则：**
- `assets/images/` - 所有图片资源
- 背景图命名：`background_{编号}.png`
- 图标命名：`{name}_icon.png`
- 如需支持多主题，使用子目录：`assets/images/themes/{theme_name}/`

---

## TODOs

### Wave 1: 资源整理与基础设置

- [ ] 1. 创建资源目录结构
  **What to do:**
  - 创建 `assets/images/` 目录
  - 将 `background_1.png` 移动到 `assets/images/`
  - 创建 `.gitignore` 规则（如有大文件）

  **Must NOT do:**
  - 不要删除原始背景图文件
  - 不要修改图片内容

  **Recommended Agent Profile:**
  - **Category**: `quick`
  - **Skills**: []

  **Parallelization:**
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 1 (with Task 2)
  - **Blocks**: Task 3
  - **Blocked By**: None

  **References:**
  - `background_1.png` - 背景图文件
  - 当前目录结构

  **Acceptance Criteria:**
  - [ ] `assets/images/` 目录存在
  - [ ] `background_1.png` 已移动到 `assets/images/`
  - [ ] 目录结构符合规划

  **QA Scenarios:**
  ```
  Scenario: 验证目录结构
    Tool: Bash
    Preconditions: 当前在项目根目录
    Steps:
      1. 运行 `ls -la assets/images/`
    Expected Result: 显示 background_1.png 文件
    Evidence: .sisyphus/evidence/task-1-directory-structure.txt
  ```

  **Commit**: YES
  - Message: `chore(assets): reorganize image assets into assets/images directory`
  - Files: `assets/images/background_1.png` (新增), 原位置删除

---

### Wave 2: 模板设计与实现

- [ ] 2. 备份现有模板
  **What to do:**
  - 将 `templates/email.html` 复制为 `templates/email_backup.html`
  - 保留原始模板作为备份

  **Must NOT do:**
  - 不要直接修改 `email.html`

  **Recommended Agent Profile:**
  - **Category**: `quick`
  - **Skills**: []

  **Parallelization:**
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 1 (with Task 1)
  - **Blocks**: Task 3
  - **Blocked By**: None

  **Acceptance Criteria:**
  - [ ] `templates/email_backup.html` 存在
  - [ ] 内容与原始模板一致

  **QA Scenarios:**
  ```
  Scenario: 验证备份文件
    Tool: Bash
    Preconditions: 无
    Steps:
      1. 运行 `diff templates/email.html templates/email_backup.html`
    Expected Result: 无差异输出
    Evidence: .sisyphus/evidence/task-2-backup-verified.txt
  ```

  **Commit**: YES
  - Message: `chore(templates): backup current email template`
  - Files: `templates/email_backup.html`

- [ ] 3. 创建新邮件模板 v2
  **What to do:**
  - 基于参考图设计创建新模板 `templates/email_v2.html`
  - 实现粉色浪漫风格
  - 使用背景图作为卡片背景
  - 包含以下元素：
    - 顶部心形装饰
    - 收件人名称
    - 日期
    - 恋爱天数（大数字突出显示）
    - 天气信息（简化版：城市+温度+天气状况）
    - 每日情话（引用样式）
    - 底部署名和日期
    - 底部分隔线+心形装饰
  - 使用 table 布局确保邮件客户端兼容性
  - 添加响应式样式

  **Must NOT do:**
  - 不要使用 CSS Grid/Flexbox（邮件客户端支持差）
  - 不要引入外部字体（可能加载失败）
  - 不要省略内联样式（会被邮件客户端过滤）

  **Recommended Agent Profile:**
  - **Category**: `visual-engineering`
  - **Skills**: []

  **Parallelization:**
  - **Can Run In Parallel**: NO
  - **Parallel Group**: Wave 2
  - **Blocks**: Task 4, Task 5
  - **Blocked By**: Task 1, Task 2

  **References:**
  - `assets/images/background_1.png` - 背景图
  - `templates/email_backup.html` - 参考原始模板结构
  - 参考图设计（粉色浪漫风格，卡片式布局）

  **Acceptance Criteria:**
  - [ ] `templates/email_v2.html` 文件创建成功
  - [ ] 模板包含所有必要变量：recipient_name, sender_name, today, days_together, weather, quote
  - [ ] 使用背景图作为卡片背景（通过 base64 内嵌或外部URL）
  - [ ] 使用 table 布局确保邮件客户端兼容性
  - [ ] 包含响应式媒体查询
  - [ ] 模板验证通过（无HTML语法错误）

  **QA Scenarios:**
  ```
  Scenario: 验证模板渲染
    Tool: Bash (Python)
    Preconditions: 已安装 Python 和依赖
    Steps:
      1. 运行测试脚本加载模板
      2. 检查所有变量占位符
    Expected Result: 模板无语法错误，所有变量可渲染
    Evidence: .sisyphus/evidence/task-3-template-render.txt

  Scenario: 验证HTML结构
    Tool: Bash
    Preconditions: 无
    Steps:
      1. 运行 `python -c "from src.template import get_template_env; env = get_template_env(); t = env.get_template('email_v2.html')"`
    Expected Result: 无异常抛出
    Evidence: .sisyphus/evidence/task-3-html-valid.txt
  ```

  **Commit**: YES
  - Message: `feat(templates): create new romantic email template v2`
  - Files: `templates/email_v2.html`

- [ ] 4. 更新模板渲染逻辑
  **What to do:**
  - 更新 `src/template.py` 支持新模板
  - 添加新函数 `render_email_v2()`
  - 保持向后兼容（`render_email()` 仍可调用旧模板）
  - 更新模板变量传递逻辑
  - 支持新的设计元素（recipient_name, sender_name）

  **Must NOT do:**
  - 不要删除或修改现有 `render_email()` 函数（保持向后兼容）
  - 不要修改默认行为（除非显式切换到 v2）

  **Recommended Agent Profile:**
  - **Category**: `quick`
  - **Skills**: ["python-patterns"]

  **Parallelization:**
  - **Can Run In Parallel**: NO
  - **Parallel Group**: Wave 2
  - **Blocks**: Task 5
  - **Blocked By**: Task 3

  **References:**
  - `src/template.py` - 模板渲染逻辑
  - `templates/email_v2.html` - 新模板
  - `src/main.py` - 调用方式（了解现有接口）

  **Acceptance Criteria:**
  - [ ] `render_email_v2()` 函数添加成功
  - [ ] 函数接受所有必要参数
  - [ ] 现有 `render_email()` 函数未受影响
  - [ ] 新函数可成功渲染模板

  **QA Scenarios:**
  ```
  Scenario: 测试新渲染函数
    Tool: Bash (Python REPL)
    Preconditions: Python 环境就绪
    Steps:
      1. 运行 `python -c "from src.template import render_email_v2; html = render_email_v2(...)"`
    Expected Result: 成功返回 HTML 字符串
    Evidence: .sisyphus/evidence/task-4-render-test.txt

  Scenario: 验证向后兼容
    Tool: Bash (Python REPL)
    Preconditions: 无
    Steps:
      1. 运行 `python -c "from src.template import render_email; ..."`
    Expected Result: 原始函数仍可正常工作
    Evidence: .sisyphus/evidence/task-4-backward-compat.txt
  ```

  **Commit**: YES
  - Message: `feat(template): add render_email_v2() for new template`
  - Files: `src/template.py`

---

### Wave 3: 测试与验证

- [ ] 5. 干运行测试新模板
  **What to do:**
  - 使用 `main.py --dry-run` 测试新模板渲染
  - 检查生成的 HTML 内容
  - 验证所有样式正确应用
  - 在浏览器中预览效果

  **Must NOT do:**
  - 不要实际发送邮件（除非明确测试发送）

  **Recommended Agent Profile:**
  - **Category**: `unspecified-high`
  - **Skills**: []

  **Parallelization:**
  - **Can Run In Parallel**: NO
  - **Parallel Group**: Wave 3
  - **Blocks**: Task 6
  - **Blocked By**: Task 3, Task 4

  **References:**
  - `src/main.py` - 主程序入口
  - `templates/email_v2.html` - 新模板
    - `src/template.py` - 渲染逻辑

  **Acceptance Criteria:**
  - [ ] 干运行成功执行
  - [ ] 生成的 HTML 可正常显示
  - [ ] 所有变量正确替换
  - [ ] 背景图正确显示

  **QA Scenarios:**
  ```
  Scenario: 干运行测试
    Tool: Bash
    Preconditions: 已配置 config.yaml
    Steps:
      1. 运行 `python src/main.py --dry-run`
    Expected Result: 输出 HTML 内容，无错误
    Evidence: .sisyphus/evidence/task-5-dry-run.html

  Scenario: 浏览器预览
    Tool: Playwright
    Preconditions: HTML 文件已生成
    Steps:
      1. 打开生成的 HTML 文件
      2. 截图预览
    Expected Result: 显示粉色浪漫风格邮件
    Evidence: .sisyphus/evidence/task-5-preview.png
  ```

  **Commit**: NO

- [ ] 6. 创建资源存放文档
  **What to do:**
  - 创建 `assets/README.md` 说明资源存放规范
  - 包含图片命名规范
  - 包含多主题支持说明（可选）
  - 更新主 README 添加资源管理章节

  **Must NOT do:**
  - 不要遗漏重要的存放规则说明

  **Recommended Agent Profile:**
  - **Category**: `writing`
  - **Skills**: []

  **Parallelization:**
  - **Can Run In Parallel**: NO
  - **Parallel Group**: Wave 3
  - **Blocks**: None
  - **Blocked By**: Task 1

  **References:**
  - `README.md` - 现有文档
  - `assets/images/` - 资源目录

  **Acceptance Criteria:**
  - [ ] `assets/README.md` 创建完成
  - [ ] 包含完整的存放规范
  - [ ] 主 README 已更新

  **QA Scenarios:**
  ```
  Scenario: 验证文档完整性
    Tool: Bash
    Preconditions: 无
    Steps:
      1. 运行 `cat assets/README.md`
    Expected Result: 文档包含命名规范、目录结构说明
    Evidence: .sisyphus/evidence/task-6-docs-check.txt
  ```

  **Commit**: YES
  - Message: `docs(assets): add asset management documentation`
  - Files: `assets/README.md`, `README.md`

---

## Final Verification Wave

- [ ] F1. **功能完整测试** — `unspecified-high`
  测试新模板的完整功能：
  - 渲染测试：所有变量正确显示
  - 样式测试：背景图、颜色、字体正确
  - 响应式测试：移动端和桌面端都正常显示
  - 兼容性测试：在主要邮件客户端中预览正常

- [ ] F2. **代码质量检查** — `quick`
  检查代码质量：
  - Python 代码符合 PEP8
  - HTML 结构清晰，无错误
  - 模板语法正确
  - 无冗余代码

- [ ] F3. **文档完整性检查** — `deep`
  验证文档完整性：
  - README 已更新
  - 资源存放文档已创建
  - 代码注释完整

---

## 资源存放规范

### 目录结构

```
assets/
├── README.md           # 资源管理说明文档
├── images/            # 图片资源
│   ├── background_1.png    # 主背景图
│   ├── background_2.png    # 备选背景图（可选）
│   ├── icons/             # 图标资源（可选）
│   │   ├── heart.png
│   │   └── flower.png
│   └── themes/           # 多主题支持（可选）
│       ├── romantic/
│       │   └── background.png
│       └── minimalist/
│           └── background.png
└── fonts/             # 自定义字体（可选）
    └── custom-font.ttf
```

### 命名规范

1. **背景图**：`background_{编号}.png`
   - 例：`background_1.png`, `background_2.png`

2. **图标**：`{name}_icon.png` 或 `{name}.png`
   - 例：`heart_icon.png`, `flower.png`

3. **主题资源**：`themes/{theme_name}/{type}/{file}`
   - 例：`themes/romantic/background.png`

### 邮件模板中的资源引用

**方法 1：Base64 内嵌（推荐，最兼容）**
```html
<img src="data:image/png;base64,iVBORw0KGgo..." alt="背景">
```

**方法 2：外部 URL**
```html
<img src="https://your-cdn.com/assets/background_1.png" alt="背景">
```

**方法 3：相对路径（仅部分邮件客户端支持）**
```html
<img src="cid:background_1" alt="背景">
```

---

## 设计要点

### 颜色方案

- **主色调**：#FFB6C1（浅粉色）- 浪漫氛围
- **背景色**：#FFF0F5（薰衣草淡粉）- 柔和背景
- **文字色**：#4A4A4A（深灰）- 确保可读性
- **强调色**：#FF69B4（热粉）- 重点突出

### 字体建议

- **中文**：系统默认中文字体（确保兼容性）
  - 优先：`PingFang SC`, `Microsoft YaHei`, `SimHei`
- **数字**：无衬线字体
  - 使用：`Helvetica Neue`, `Arial`, `sans-serif`

### 布局结构

1. **顶部装饰**：心形+月桂叶图案（可选，可用emoji代替）
2. **问候语**：收件人名称
3. **日期**：今天日期
4. **恋爱天数卡片**：
   - 标题："我们已经相爱了"
   - 大数字：{{ days_together }}
   - 单位："天"
5. **天气卡片**：
   - 位置图标 + {{ recipient_city }}
   - 温度图标 + {{ weather.temp_min }}-{{ weather.temp_max }}°C
   - 天气图标 + {{ weather.condition }}
6. **情话卡片**：
   - 左侧引号装饰
   - 内容：{{ quote.content }}
   - 右侧引号装饰
7. **底部分隔线**：带心形装饰
8. **署名**："爱你的 {{ sender_name }}" + 日期

### 响应式设计

- 最大宽度：600px（邮件标准）
- 移动端：字体缩小，间距调整
- 图片：使用 max-width: 100% 确保自适应

---

## 风险与注意事项

1. **邮件客户端兼容性**
   - 使用 table 布局而非 CSS Grid/Flexbox
   - 使用内联样式而非外部 CSS
   - 测试 Gmail、Outlook、Apple Mail、QQ 邮箱等

2. **图片显示**
   - 某些邮件客户端默认不加载图片
   - 提供 alt 文本作为备用
   - 考虑使用 Base64 内嵌图片

3. **背景图处理**
   - 邮件客户端对背景图支持不一
   - 提供纯色背景作为 fallback
   - 控制图片大小（< 500KB 最佳）

4. **字体兼容性**
   - 使用系统默认字体确保跨平台一致
   - 避免使用自定义网络字体

---

## 成功标准

- ✅ 新模板成功渲染并显示粉色浪漫风格
- ✅ 所有变量（recipient_name, sender_name, days_together, weather, quote）正确显示
- ✅ 背景图正确应用
- ✅ 在主流邮件客户端中正常显示
- ✅ 移动端响应式正常
- ✅ 代码符合规范，通过质量检查
- ✅ 文档完整，资源存放规范明确
