# 项目学习记录

## 2026-03-06 - HTML邮件可访问性优化

### 今日任务
为邮件模板添加可访问性支持，确保屏幕阅读器用户能更好地理解邮件内容。

### 学到的知识点

#### 1. 邮件模板中 table 标签的可访问性
- **问题**：邮件客户端广泛使用 table 进行布局，但屏幕阅读器会尝试将 table 解析为数据表格
- **解决方案**：为所有布局用的 table 添加 `role="presentation"`
- **效果**：告诉辅助技术这是一个展示性表格，不是数据表格

#### 2. 修改的文件和位置

**templates/email.html**（10 处修改）：
- Line 33: 主容器 table
- Line 38: 邮件内容容器 table
- Line 43: Header section 内嵌 table
- Line 68: 年月显示 table
- Line 87: 分隔线 table
- Line 96: 引用区块 table
- Line 99: 引用内容内嵌 table
- Line 137: 天气区块 table
- Line 140: 天气内容内嵌 table
- Line 165: 纪念日区块 table
- Line 168: 纪念日内容内嵌 table
- Line 190: Footer 内嵌 table
- Line 208: 底部间距 table

**templates/email_new.html**（7 处修改）：
- Line 33: 主容器 table
- Line 39/41: 邮件内容容器 table（条件分支）
- Line 62: 恋爱天数卡片 table
- Line 78: 天气卡片 table
- Line 81: 天气内容内嵌 table
- Line 105: 情话卡片 table
- Line 109: 情话引用内嵌 table
- Line 138: 底部分隔线 table
- Line 159: 底部间距 table

#### 3. 装饰性图片的 alt 属性
- **问题**：分隔线中的 ♥ 符号使用了无意义的 alt 文本
- **解决方案**：将 `alt="♥"` 改为 `alt=""`
- **原理**：装饰性元素应该使用空 alt，让屏幕阅读器跳过

#### 4. 邮件模板可访问性最佳实践
1. 所有布局 table 都要加 `role="presentation"`
2. 图片必须提供有意义的 alt 文本，装饰性的用空字符串
3. 使用语义化 HTML 标签（header、footer、article 等）
4. 确保颜色对比度足够（WCAG AA 标准）
5. 避免仅通过颜色传递信息

#### 5. 为什么邮件模板需要特殊处理
- 邮件客户端对 CSS 支持有限，常用 table 布局
- 不同客户端对 ARIA 属性支持程度不同
- 屏幕阅读器在邮件客户端中的行为可能不同于网页浏览器

### 验证方法
- 使用 NVDA/JAWS 等屏幕阅读器测试
- 使用 WAVE 或 axe 等可访问性检查工具
- 在多种邮件客户端中测试渲染效果

### 参考资源
- [WCAG 2.1 指南](https://www.w3.org/WAI/WCAG21/quickref/)
- [HTML Email Accessibility](https://www.a11yproject.com/posts/accessibility-email/)
- [MDN ARIA: presentation role](https://developer.mozilla.org/en-US/docs/Web/Accessibility/ARIA/Roles/presentation_role)
