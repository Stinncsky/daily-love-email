# 修复 main.py 环境变量名称

## 问题描述
GitHub Actions 运行失败，错误信息：
```
ERROR - No recipient email configured (TO_EMAIL). Aborting.
```

## 根本原因
`main.py` 中读取的环境变量名称和 GitHub Actions 中设置的不匹配：

| GitHub Actions 设置 (新) | main.py 读取 (旧) | 结果 |
|--------------------------|-------------------|------|
| `EMAIL_RECIPIENT` | `TO_EMAIL` | ❌ 不匹配 |
| `EMAIL_SENDER` | `FROM_EMAIL` | ❌ 不匹配 |
| `EMAIL_PASSWORD` | `SMTP_PASSWORD` | ❌ 不匹配 |
| `LOVE_START_DATE` | `START_DATE` | ❌ 不匹配 |
| `CITY` | `LOCATION` | ❌ 不匹配 |

## 修复方案

修改 `src/main.py` 第 88-99 行，将环境变量名从旧的改为新的：

```python
# 修改前（旧变量名）
cfg = {
    "to_email": os.environ.get("TO_EMAIL"),
    "from_email": os.environ.get("FROM_EMAIL"),
    "smtp_password": os.environ.get("SMTP_PASSWORD"),
    "location": os.environ.get("LOCATION", ""),
    "start_date": os.environ.get("START_DATE"),
}

# 修改后（新变量名）
cfg = {
    "to_email": os.environ.get("EMAIL_RECIPIENT"),
    "from_email": os.environ.get("EMAIL_SENDER"),
    "smtp_password": os.environ.get("EMAIL_PASSWORD"),
    "location": os.environ.get("CITY", ""),
    "start_date": os.environ.get("LOVE_START_DATE"),
}
```

## 完整修改内容

需要修改 `load_config_safe()` 函数中的环境变量读取部分：

1. `TO_EMAIL` → `EMAIL_RECIPIENT`
2. `FROM_EMAIL` → `EMAIL_SENDER`
3. `SMTP_PASSWORD` → `EMAIL_PASSWORD`
4. `LOCATION` → `CITY`
5. `START_DATE` → `LOVE_START_DATE`
6. `SMTP_SERVER` 默认值改为 `"smtp.qq.com"`
7. `SMTP_PORT` 默认值改为 `465`

## 执行步骤

1. 读取 `src/main.py` 文件
2. 找到 `load_config_safe()` 函数（第76-100行）
3. 修改环境变量名称
4. 提交并推送到 GitHub

## 验证标准

- [ ] 修改后的 main.py 使用新的环境变量名
- [ ] GitHub Actions 能够正确读取 Secrets
- [ ] 手动触发测试能够正常运行
