# 资源存放指南

本指南说明如何管理每日爱情邮件项目的图片、模板等资源文件。

---

## 目录结构

```
auto-email/
├── assets/                 # 静态资源目录
│   ├── images/            # 图片资源
│   │   ├── background_1.png    # 主背景图（当前使用）
│   │   └── backgrounds/        # 可选：多种主题背景
│   │       ├── romantic.png
│   │       ├── minimal.png
│   │       └── festive.png
│   └── fonts/             # 可选：自定义字体
│       └── chinese/
├── templates/             # 邮件模板目录
│   ├── email.html         # 原始模板（保留）
│   ├── email_new.html     # 新浪漫风格模板（当前使用）
│   └── themes/            # 可选：多主题模板
│       ├── romantic.html
│       ├── modern.html
│       └── minimal.html
└── docs/                  # 文档目录
    └── assets-guide.md    # 本文件
```

---

## 背景图存放规范

### 当前方案：CSS渐变（推荐）

由于邮件客户端的兼容性限制，**推荐使用CSS渐变**代替图片背景。

**优点：**
- ✅ 无需外部资源，邮件发送后不会失效
- ✅ 文件体积小，加载速度快
- ✅ 所有邮件客户端都支持
- ✅ 易于修改颜色和样式

**当前使用的渐变：**
```css
background: linear-gradient(180deg, #FAD4E4 0%, #FDF6F0 50%, #FFF8F5 100%);
```

### 如需使用图片背景

如果你仍然想使用图片作为背景（例如你提供的玫瑰花背景），有以下几种方案：

#### 方案1：Base64编码内嵌（兼容性最好）

将图片转换为Base64编码，直接嵌入HTML：

```python
import base64

# 读取图片并转换为Base64
with open('assets/images/background_1.png', 'rb') as f:
    img_data = base64.b64encode(f.read()).decode('utf-8')

# 在HTML中使用
background_url = f"data:image/png;base64,{img_data}"
```

**注意事项：**
- 图片文件不宜过大（建议 < 50KB）
- 使用 [tinypng.com](https://tinypng.com) 等工具压缩图片
- 将图片调整为合适的尺寸（建议宽度 600px）

#### 方案2：外部图片链接

```html
<style>
.email-container {
    background-image: url('https://your-cdn.com/background_1.png');
}
</style>
```

**缺点：**
- 部分邮件客户端会屏蔽外部图片
- 需要图片托管服务
- 图片可能失效

---

## 添加新的背景图

### 步骤1：准备图片

1. **格式**：PNG（保留透明度）或 JPG（无透明）
2. **尺寸**：建议宽度 600px，高度自适应
3. **压缩**：使用 [tinypng.com](https://tinypng.com) 压缩
4. **命名**：使用语义化命名，如 `romantic-pink.png`

### 步骤2：存放图片

```bash
# 将图片放入 assets/images/backgrounds/ 目录
cp your-background.png assets/images/backgrounds/
```

### 步骤3：在模板中使用

**CSS渐变方式（推荐）：**
```html
<body style="background: linear-gradient(180deg, #YOUR_COLOR1 0%, #YOUR_COLOR2 100%);">
```

**Base64内嵌方式：**
```html
<!-- 在模板顶部添加Python代码获取Base64 -->
{% set bg_base64 = get_background_base64('romantic-pink.png') %}

<body style="background-image: url('data:image/png;base64,{{ bg_base64 }}');">
```

---

## 模板文件管理

### 当前模板

- `templates/email.html` - 原始模板（保留备份）
- `templates/email_new.html` - 新浪漫风格模板（当前使用）

### 添加新模板

1. **创建模板文件**：`templates/email_[theme].html`
2. **添加渲染函数**：在 `src/template.py` 中添加对应的渲染函数
3. **测试模板**：确保渲染正常，邮件客户端显示正确

### 切换邮件模板

在 `src/main.py` 中修改模板调用：

```python
# 使用原始模板
# html_content = render_email_template(...)

# 使用新模板
html_content = render_email_template_new(
    recipient_name=config.get('recipient_name', '亲爱的'),
    sender_name=config.get('sender_name', '爱你的'),
    recipient_city=config.get('city', '北京'),
    days_together=days,
    months_together=months,
    years_together=years,
    quote=quote,
    weather=weather,
    today=today,
)
```

---

## 图片优化工具推荐

### 在线工具

1. **[TinyPNG](https://tinypng.com)**
   - 智能PNG和JPEG压缩
   - 支持批量处理
   - 免费使用（最多20张/次）

2. **[Squoosh](https://squoosh.app)**
   - Google开发的图片压缩工具
   - 支持多种格式和压缩算法
   - 实时对比压缩前后效果

3. **[ImageOptim](https://imageoptim.com/online)**
   - 简单易用的在线压缩工具
   - 支持PNG、JPEG、GIF

### 本地工具

1. **ImageMagick**（命令行）
   ```bash
   # 调整尺寸
   convert input.png -resize 600x output.png
   
   # 压缩
   convert input.png -quality 85 output.jpg
   ```

2. **PNGGauntlet**（Windows GUI）
   - 免费的PNG优化工具
   - 支持批量处理

---

## 邮件客户端兼容性

### 支持的特性

- ✅ CSS内联样式
- ✅ Base64编码图片
- ✅ 基本HTML标签（div, p, span, table）
- ✅ CSS渐变背景（现代客户端）
- ✅ 简单CSS属性（color, font-size, background-color）

### 需谨慎使用的特性

- ⚠️ CSS Grid/Flexbox（部分客户端不支持）
- ⚠️ 外部CSS文件（不支持）
- ⚠️ 外部图片链接（可能被拦截）
- ⚠️ JavaScript（不支持）
- ⚠️ CSS滤镜（backdrop-filter 等）

### 推荐做法

1. **使用 Table 布局**作为主要布局方式
2. **内联样式**所有CSS
3. **测试**在多个邮件客户端（QQ邮箱、Gmail、Outlook）
4. **提供备选方案**（纯文本版本）

---

## 常见问题

### Q: 背景图片为什么不显示？

**A:** 可能原因：
1. 邮件客户端屏蔽了外部图片
2. 图片链接失效
3. 图片文件过大被拦截

**解决方案：**
- 使用CSS渐变代替图片
- 使用Base64编码内嵌图片
- 优化图片大小（< 50KB）

### Q: 如何更换邮件主题颜色？

**A:** 编辑 `templates/email_new.html`，修改CSS中的颜色值：

```css
/* 主背景渐变 */
background: linear-gradient(180deg, #FAD4E4 0%, #FDF6F0 50%, #FFF8F5 100%);

/* 恋爱天数卡片 */
background: linear-gradient(135deg, #F4C2C2 0%, #E8B4B8 100%);

/* 天气卡片 */
background: linear-gradient(135deg, #A8D8EA 0%, #B8E6F0 100%);
```

### Q: 可以添加自定义字体吗？

**A:** 不推荐。邮件客户端对自定义字体支持很差。

**替代方案：**
- 使用系统默认中文字体栈：
  ```css
  font-family: -apple-system, BlinkMacSystemFont, 'PingFang SC', 'Hiragino Sans GB', 'Microsoft YaHei', sans-serif;
  ```
- 使用图片代替特殊字体文字

---

## 文件命名规范

### 图片文件

```
{主题}-{描述}.{格式}

示例：
- romantic-pink.png
- minimal-white.jpg
- festive-red.png
```

### 模板文件

```
email_{主题}.html

示例：
- email_romantic.html
- email_modern.html
- email_minimal.html
```

---

## 维护建议

1. **定期备份**重要资源文件
2. **版本控制**所有变更（使用Git）
3. **测试**每次修改后在真实邮件客户端查看
4. **文档**记录每次样式变更
5. **优化**定期压缩图片，保持小体积

---

## 相关文件

- 模板文件：`templates/email_new.html`
- 渲染模块：`src/template.py`
- 主程序：`src/main.py`
- 背景图片：`assets/images/background_1.png`

---

如有问题，请参考项目 README.md 或提交 Issue。
