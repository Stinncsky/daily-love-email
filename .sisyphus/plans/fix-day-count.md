# 修复计数显示和重新截图

## TL;DR

修复 `scripts/generate_email.py` 中的计数显示问题：当前显示"剩余天数"（5天），应显示"总天数"（1160天）。然后重新生成邮件预览并截图。

---

## Context

### 问题描述
用户反馈计数功能不对，期望显示总天数（如1160天），但当前显示的是剩余天数（5天）。

### 根本原因
`calculate_days_together()` 返回 tuple `(days_remainder, months, years)`：
- 从 2023-01-01 到 2026-03-06 计算为：3年2个月5天
- `days_together` 被赋值为 5（剩余天数）
- 但用户期望显示 1160（总天数）

### 当前代码
```python
calc_result = calculate_days_together(start_date)  # 返回 (5, 2, 3)
days_together, months_together, years_together = calc_result  # days_together = 5
```

### 期望行为
- `days_together` 应显示总天数：1160
- 保留 `months_together` 和 `years_together` 用于其他用途

---

## Work Objectives

1. **修复计数逻辑** - 在 `scripts/generate_email.py` 中计算总天数
2. **重新生成邮件预览** - 运行脚本生成新的 HTML
3. **重新截图** - 使用 Playwright 截图邮件预览
4. **验证修复** - 确认显示为总天数

---

## TODOs

- [ ] 1. 修复 scripts/generate_email.py 计数逻辑

  **What to do**:
  - 修改 `load_and_prepare_context` 函数
  - 在解包 tuple 后，计算总天数（今天 - 起始日期）
  - 将总天数赋值给 `days_together`
  - 保留 `months_together` 和 `years_together`
  
  **Code change**:
  ```python
  calc_result = calculate_days_together(start_date) if start_date else None
  if isinstance(calc_result, tuple) and len(calc_result) == 3:
      _, months_together, years_together = calc_result
      # Calculate total days for display
      from datetime import datetime, date
      sd = datetime.strptime(start_date, "%Y-%m-%d").date()
      days_together = (date.today() - sd).days
  else:
      days_together, months_together, years_together = 0, 0, 0
  ```
  
  **Verification**:
  - 运行 `python scripts/generate_email.py`
  - 确认输出显示：恋爱天数: 1160 天

- [ ] 2. 重新生成邮件预览

  **What to do**:
  - 运行 `python scripts/generate_email.py`
  - 确认生成新的 HTML 文件
  - 文件路径：`output/email_YYYYMMDD_HHMMSS.html`
  
  **Verification**:
  - 检查 output/ 目录下有新的 HTML 文件
  - 文件大小 > 10KB

- [ ] 3. 重新截图

  **What to do**:
  - 使用 Playwright 截图生成的 HTML
  - 保存到 `screenshot.png`
  - 覆盖旧的截图
  
  **Code**:
  ```python
  from playwright.sync_api import sync_playwright
  
  with sync_playwright() as p:
      browser = p.chromium.launch()
      page = browser.new_page(viewport={'width': 800, 'height': 1200})
      page.goto('file:///E:/meishayong/auto-email/output/email_YYYYMMDD_HHMMSS.html')
      page.wait_for_timeout(2000)
      page.screenshot(path='screenshot.png', full_page=True)
      browser.close()
  ```
  
  **Verification**:
  - screenshot.png 文件存在
  - 文件大小 > 100KB
  - 图片显示 1160 天

- [ ] 4. 验证 README.md 引用

  **What to do**:
  - 确认 README.md 中的截图引用正确
  - 截图显示总天数 1160
  
  **Verification**:
  - Read README.md 第19-20行
  - 确认包含 `![每日恋爱邮件预览](screenshot.png)`

---

## Verification Strategy

### Test Commands
```bash
# 1. 修复后运行脚本
python scripts/generate_email.py
# Expected: 显示 "恋爱天数: 1160 天"

# 2. 验证截图存在
ls -la screenshot.png
# Expected: 文件存在，大小 > 100KB

# 3. 查看 HTML 内容确认天数
grep -o "1160" output/email_*.html | head -1
# Expected: 输出 1160
```

### Success Criteria
- [ ] 脚本输出显示 "恋爱天数: 1160 天"
- [ ] 生成的 HTML 文件中包含 "1160"
- [ ] screenshot.png 已更新且显示 1160 天
- [ ] README.md 正确引用截图

---

## Commit Strategy

**Commit Message**: 
```
fix: display total days instead of remainder days

- Fix scripts/generate_email.py to calculate total days
- Update screenshot.png with correct day count
```

**Files to commit**:
- `scripts/generate_email.py`
- `screenshot.png`

---

## Notes

### 日期计算逻辑
- 起始日期：2023-01-01
- 今天：2026-03-06
- 总天数 = (2026-03-06) - (2023-01-01) = 1160 天
- 分解：3年2个月5天（但显示总天数更直观）

### 截图要求
- 宽度：800px
- 高度：自适应（full_page）
- 等待时间：2秒（确保渲染完成）
