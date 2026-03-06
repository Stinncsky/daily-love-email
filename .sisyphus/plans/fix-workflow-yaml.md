# 修复 GitHub Actions YAML 语法错误

## 问题描述
GitHub Actions 报错：
```
Invalid workflow file: .github/workflows/daily-email.yml#L29
You have an error in your yaml syntax on line 29
```

## 错误分析

### 错误 1：workflow_dispatch 配置不完整
当前第5行：
```yaml
workflow_dispatch:
```
GitHub Actions 要求 `workflow_dispatch` 要么：
- 有具体的 inputs 配置
- 或者完全省略（但用户需要手动触发功能）

### 错误 2：内嵌 Python 脚本缩进问题
第25-39行的验证脚本：
```yaml
- name: Validate YAML syntax for this workflow
  run: |
    python -m pip install --upgrade pip
    python - <<'PY'
import sys  # 第29行 - 这里缩进有问题
```
`<<'PY'` heredoc 语法在 GitHub Actions YAML 中解析有问题。

## 修复方案

### 方案：简化工作流文件

1. **删除** 内嵌的 Python 验证脚本（没有必要，GitHub 会自动验证）
2. **简化** workflow_dispatch 配置（添加基本的 inputs）
3. **添加** 缺少的环境变量（CITY 等）

## 修复后的工作流结构

```yaml
name: Daily Love Email

on:
  schedule:
    - cron: '0 0 * * *'
  workflow_dispatch:
    inputs:
      dry_run:
        description: '干运行模式（不发送邮件）'
        required: false
        default: 'false'
        type: choice
        options:
          - 'false'
          - 'true'

jobs:
  send-email:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.10'
      - run: python -m pip install --upgrade pip
      - run: pip install -r requirements.txt
      - run: python src/main.py
        env:
          EMAIL_SENDER: ${{ secrets.EMAIL_SENDER }}
          EMAIL_PASSWORD: ${{ secrets.EMAIL_PASSWORD }}
          EMAIL_RECIPIENT: ${{ secrets.EMAIL_RECIPIENT }}
          WEATHER_API_KEY: ${{ secrets.WEATHER_API_KEY }}
          LOVE_START_DATE: ${{ secrets.LOVE_START_DATE }}
          CITY: ${{ secrets.CITY }}
```

## 执行步骤

1. 重写 `.github/workflows/daily-email.yml`
2. 删除有问题的 Python 验证脚本
3. 添加完整的 workflow_dispatch 配置
4. 添加缺少的 CITY 环境变量
5. 提交并推送到 GitHub

## 验证标准

- [ ] YAML 文件在 GitHub 上不再报语法错误
- [ ] 可以看到 "Run workflow" 按钮
- [ ] 手动触发可以正常工作
