# UI重新设计工作计划

## 项目概述

根据用户提供的两张参考图，重新设计邮件UI，采用粉色浪漫风格，包含玫瑰花装饰背景。

---

## 设计分析

### 参考图（Image 1）UI元素分析

**整体风格：** 浪漫、温馨、粉色系

**内容区域（从上到下）：**
1. **顶部装饰** - 心形+橄榄枝花环
2. **称呼** - 亲爱的 {{ recipient_name }}
3. **日期** - {{ today }}
4. **恋爱天数卡片** - 粉色渐变背景
   - "我们已经相爱了"
   - 大号数字天数 (如: 1314天)
5. **天气卡片** - 蓝色背景
   - 📍 城市名称 + "今天"
   - 🌡️ 温度 + 天气图标
6. **情话卡片** - 带装饰引号的引用框
   - 双引号装饰
   - {{ quote.content }}
7. **底部分隔** - 横线 + 心形 + 星星
8. **署名** - 爱你的 {{ sender_name }}

### 背景图（Image 2）分析

- **主色调**: 上浅粉(`#FAD4E4`) → 下奶油色(`#FDF6F0`)渐变
- **装饰元素**: 四角粉色玫瑰花、顶部心形花环、底部心形分隔
- **圆角**: 四个角有较大弧度
- **中央区域**: 80%留白，适合放置文字内容

---

## 资源存放规划

### 目录结构

```
auto-email/
├── assets/
│   ├── images/           # 图片资源
│   │   ├── background_1.png    # 背景图
│   │   ├── backgrounds/        # 可选：多种背景
│   │   │   ├── romantic.png
│   │   │   ├── minimal.png
│   │   │   └── festive.png
│   │   └── icons/              # 可选：自定义图标
│   │       ├── heart.png
│   │       └── weather/
│   └── fonts/            # 可选：自定义字体
│       └── chinese/
├── templates/
│   ├── email.html        # 当前模板（保留备份）
│   ├── email_new.html    # 新设计的模板
│   └── themes/           # 可选：多主题模板
│       ├── romantic.html
│       ├── modern.html
│       └── minimal.html
└── src/
    ├── template.py       # 模板渲染模块
    └── email_sender.py   # 邮件发送模块
```

### 资源存放规范

#### 1. 图片资源 (`assets/images/`)
- **背景图**: 直接放在 `assets/images/` 根目录
- **多主题背景**: 使用 `assets/images/backgrounds/` 子目录
- **图标**: 使用 `assets/images/icons/` 子目录

#### 2. 模板文件 (`templates/`)
- **主模板**: 使用语义化命名，如 `email_romantic.html`
- **多主题**: 使用 `templates/themes/` 子目录
- **备份**: 保留旧模板为 `email_legacy.html`

#### 3. 在HTML模板中引用资源

**方法1: Base64编码内嵌（推荐，邮件客户端兼容性好）**
```html
<!-- 将图片转换为Base64后直接嵌入CSS -->
<style>
.email-container {
    background-image: url('data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAA...');
}
</style>
```

**方法2: 使用CDN或外部链接（需要图片托管）**
```html
<style>
.email-container {
    background-image: url('https://your-cdn.com/background_1.png');
}
</style>
```

**方法3: 纯CSS渐变模拟（无图片依赖）**
```html
<style>
.email-container {
    background: linear-gradient(180deg, #FAD4E4 0%, #FDF6F0 100%);
}
</style>
```

---

## 实现方案

### 方案选择

考虑到邮件客户端的兼容性限制，推荐**方案1（Base64内嵌）**，原因：
- ✅ 大多数邮件客户端支持内嵌Base64图片
- ✅ 不需要外部资源托管
- ✅ 邮件发送后图片不会失效
- ⚠️ 文件体积稍大（但背景图可以优化压缩）

### 图片优化建议

在放入邮件前，对背景图进行优化：
1. **压缩**: 使用 tinypng.com 或类似工具压缩
2. **尺寸**: 将图片调整为适合邮件的尺寸（建议宽度600px）
3. **格式**: PNG格式保留透明度，适合复杂背景

---

## 任务清单

### 任务1: 规划资源目录 ✅
**状态**: 已完成

**操作**:
- [x] 创建 `assets/images/` 目录
- [x] 将背景图移动到 `assets/images/background_1.png`

---

### 任务2: 创建新邮件模板 ✅
**状态**: 已完成
**完成时间**: 2026-03-05

**操作**:
- [x] 创建 `templates/email_new.html` (164行)
- [x] 实现粉色渐变背景 (#FAD4E4 → #FDF6F0 → #FFF8F5)
- [x] 恋爱天数卡片 - 粉色渐变 (#F4C2C2 → #E8B4B8) + 88px大号数字
- [x] 天气卡片 - 蓝色渐变 (#A8D8EA → #B8E6F0)
- [x] 情话卡片 - 白色半透明背景 + Georgia引号装饰
- [x] 包含所有Jinja2变量: recipient_name, sender_name, today, days_together, recipient_city, weather, quote
- [x] 响应式设计 (600px/480px断点)
- [x] 邮件客户端兼容的table布局

---

### 任务3: 更新模板渲染模块 ✅
**状态**: 已完成
**完成时间**: 2026-03-05

**操作**:
- [x] 在 `src/template.py` 添加 `render_email_template_new()` 函数
- [x] 支持新模板 `email_new.html`
- [x] 保持向后兼容，现有函数未修改
- [x] 支持变量: recipient_name, sender_name, recipient_city, days_together, months_together, years_together, quote, weather, today

---

### 任务4: 测试新模板 ✅
**状态**: 已完成
**完成时间**: 2026-03-05

**测试结果**:
- [x] 模板渲染成功 (9851字符)
- [x] 所有变量正确替换
- [x] 粉色渐变背景显示正常
- [x] 恋爱天数卡片渲染正确
- [x] 天气卡片渲染正确
- [x] 情话卡片引号装饰正常
- [x] 测试输出保存到 `test_output.html`

---

### 任务5: 创建资源存放文档 ✅
**状态**: 已完成
**完成时间**: 2026-03-05

**操作**:
- [x] 创建 `docs/assets-guide.md`
- [x] 包含目录结构说明
- [x] 包含资源添加指南
- [x] 包含图片优化建议
- [x] 包含主题切换说明

---

## 实施建议

### 推荐的实施顺序

```
任务1 (已完成) 
    ↓
任务2: 创建新模板 ← 使用visual-engineering agent
    ↓
任务3: 更新模板模块 ← 使用quick agent
    ↓
任务4: 测试 ← 使用interactive_bash + playwright验证
    ↓
任务5: 文档 ← 使用writing agent
```

### 技术选型建议

| 组件 | 推荐方案 | 备选方案 |
|------|----------|----------|
| 背景图 | Base64内嵌 | CSS渐变模拟 |
| 图标 | Emoji + CSS | 内嵌SVG |
| 字体 | 系统默认字体 | 网络字体（兼容性差）|
| 布局 | Flexbox/Grid | Table布局（老客户端）|

### 邮件客户端兼容性注意事项

**支持良好的特性：**
- ✅ CSS内联样式
- ✅ Base64编码图片
- ✅ 基本HTML标签（div, p, span, table）
- ✅ 简单CSS属性（color, font-size, background-color）

**需谨慎使用的特性：**
- ⚠️ CSS Grid/Flexbox（部分客户端不支持）
- ⚠️ 外部CSS文件（不支持）
- ⚠️ 外部图片链接（可能被拦截）
- ⚠️ JavaScript（不支持）

**建议：**
- 使用 Table 布局作为备选
- 所有样式使用内联 `style` 属性
- 在Outlook、QQ邮箱、Gmail中测试

---

## 相关文件

- 现有模板: `templates/email.html`
- 新模板位置: `templates/email_new.html`
- 背景图片: `assets/images/background_1.png`
- 模板渲染模块: `src/template.py`
- 主程序: `src/main.py`

---

## 备注

1. **背景图处理**: 如果Base64后文件过大（>50KB），建议使用CSS渐变替代
2. **变量命名**: 保持与参考图一致，如 `recipient_name`, `recipient_city`
3. **多主题**: 后续可以考虑实现多主题切换功能
4. **Git提交**: 建议分多次提交，每次完成一个任务
