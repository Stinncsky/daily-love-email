Date: 2026-03-06
- 修复 ANNIVERSARIES 环境变量解析问题
  - 问题：ANNIVERSARIES 通过环境变量传入，原实现将其覆盖为字符串，导致解析失败。
  - 解决：在 _override_env 中对原值为 list/dict 的字段，在检测到环境变量时，尝试将环境变量解析为 JSON，并如若成功，则直接替换为 parsed；若 JSON 解析失败，保留原 YAML 配置，不污染结构。
  - 兼容性：保留 config.yaml 直接路径的解析逻辑，向后兼容。
- 验证计划
 1) 设置环境变量 ANNIVERSARIES='[{"name": "test", "date": "01-01"}]'，调用 load_config，config['anniversaries'] 应为 list。
 2) 设置无效的 JSON 字符串，如 ANNIVERSARIES='not-json'，load_config 应返回原始 YAML 配置中的 list，且不抛错。
 3) 现有 dict 配置路径 config.yaml 的解析未被破坏。
- 结论：实现符合后向兼容，降低未来环境变量覆盖带来的结构性问题。

## Task 7: 修复邮件 CSS 兼容性问题

### 完成时间
2026-03-06

### 问题描述
templates/email_new.html 使用了 CSS 特性 backdrop-filter 和 box-shadow，这些特性在某些邮件客户端（如 Outlook、旧版 Gmail）中不被支持。

### 修复方案
为行内样式添加 fallback：

1. **fallback 背景色**：在不支持 backdrop-filter 的客户端显示不透明背景
   - 图片背景版本：添加 background-color: rgba(255, 255, 255, 0.95)
   - 纯色背景版本：先写 background: rgba(255, 255, 255, 0.95)，再写现代特性

2. **fallback 边框**：在不支持 box-shadow 的客户端显示边框作为替代
   - 添加 border: 1px solid rgba(255, 255, 255, 0.3)

### CSS Fallback 模式
```css
/* 先写 fallback */
background: rgba(255, 255, 255, 0.95);
/* 再写现代特性（支持它的浏览器会覆盖 fallback） */
background: rgba(255, 255, 255, 0.25);
backdrop-filter: blur(20px);

/* 先写 fallback */
border: 1px solid rgba(255, 255, 255, 0.3);
/* 再写现代特性 */
box-shadow: 0 8px 32px rgba(31, 38, 135, 0.15);
```

### 修改位置
- 第50行（图片背景版本容器）
- 第56行（纯色背景版本容器）

### 验证结果
- fallback 背景色已添加：✅
- fallback 边框已添加：✅
- CSS 顺序正确（fallback在前）：✅
- 原有 backdrop-filter 和 box-shadow 保留：✅

## Task 8: 添加 Outlook VML Fallback

### 完成时间
2026-03-06

### 问题描述
templates/email_new.html 的背景图片和渐变效果在 Outlook 中需要使用 VML (Vector Markup Language) 作为 fallback。

### 修复方案
在邮件模板中添加 Outlook VML fallback 代码：

1. **Body 背景 VML fallback** (第32-36行)
   - 使用 `v:background` + `v:fill` 实现渐变背景
   - 匹配原有 CSS 渐变：`#FAD4E4` → `#FFF8F5`，角度 180°

2. **主容器 VML fallback** (第45-55行)
   - 图片背景：使用 `v:rect` + `v:fill` type="tile"
   - 纯色背景：使用 `v:rect` + `fillcolor="#FFFFFF"`

3. **VML 关闭标签** (第172-174行)
   - 正确关闭 `v:textbox` 和 `v:rect`

### VML Fallback 模式
```html
<!--[if mso]>
<v:rect xmlns:v="urn:schemas-microsoft-com:vml" fill="true" stroke="false" style="width:560px;">
  <v:fill type="tile" src="background-image.jpg" />
  <v:textbox inset="0,0,0,0">
<![endif]-->

<!-- HTML 内容 -->

<!--[if mso]>
  </v:textbox>
</v:rect>
<![endif]-->
```

### 技术要点
- 使用 `<!--[if mso]>` 条件注释确保只在 Outlook 中生效
- 使用正确的 VML 命名空间 `xmlns:v="urn:schemas-microsoft-com:vml"`
- 保持原有 HTML/CSS 对其他客户端完全有效
- VML 代码只是外包装，不改变原有内容

### 验证结果
```bash
grep -i "vml\|mso\|v:rect\|v:background" templates/email_new.html
# 共找到 14 处匹配
```
- Body 背景 VML 已添加：✅
- 主容器图片背景 VML 已添加：✅
- 主容器纯色背景 VML 已添加：✅
- VML 关闭标签已添加：✅
- 条件注释正确包裹：✅
