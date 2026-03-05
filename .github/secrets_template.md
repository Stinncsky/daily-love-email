# GitHub Actions 配置指南

本项目支持两种运行方式：本地运行和 GitHub Actions 自动运行。本文档详细介绍 GitHub Actions 模式的完整配置流程。

## 配置方式对比

在开始配置前，先了解两种方式的区别：

| 对比项 | 本地运行 | GitHub Actions |
|--------|----------|----------------|
| 配置文件 | config.yaml | GitHub Secrets |
| 运行环境 | 你自己的电脑 | GitHub 服务器 |
| 触发方式 | 手动执行命令 | 定时自动执行 |
| 首次配置 | 较复杂 | 较简单 |
| 持续运行 | 需要保持电脑开机 | 完全自动化 |
| 敏感信息 | 存在本地电脑 | 存储在 GitHub |

对于长期自动运行，推荐使用 GitHub Actions 方式，无需维护电脑开机。

## 完整 Secrets 列表

### 核心配置（必须配置）

| Secret 名称 | 说明 | 示例 |
|-------------|------|------|
| EMAIL_SENDER | 发件人 QQ 邮箱地址 | `123456789@qq.com` |
| EMAIL_PASSWORD | QQ 邮箱授权码（16位字符串，不是登录密码） | `abcd1234efgh5678` |
| EMAIL_RECIPIENT | 收件人邮箱地址 | `partner@example.com` |
| WEATHER_API_KEY | OpenWeatherMap API 密钥 | `a1b2c3d4e5f6g7h8i9j0` |

### 个性化配置（必须配置）

| Secret 名称 | 说明 | 示例 |
|-------------|------|------|
| LOVE_START_DATE | 恋爱起始日期，格式为 YYYY-MM-DD | `2023-01-01` |
| CITY | 目标城市名称（英文） | `Beijing` 或 `Shanghai` |

### 可选配置（可使用默认值）

| Secret 名称 | 说明 | 默认值 | 示例 |
|-------------|------|--------|------|
| SMTP_SERVER | SMTP 服务器地址 | smtp.qq.com | `smtp.qq.com` |
| SMTP_PORT | SMTP 端口号 | 465 | `465` |
| SENDER_NAME | 发件人显示名称 | 空（使用邮箱） | `亲爱的老公` |

## 配置步骤

### 第一步：进入仓库设置

1. 打开你的 GitHub 仓库页面
2. 点击右上角的 "Settings" 按钮
3. 在左侧菜单中找到 "Secrets and variables"，点击 "Actions"
4. 点击页面上的 "New repository secret" 按钮

### 第二步：添加 Secrets

按照下表依次添加所需的 Secrets：

| Secret 名称 | 值示例 | 注意事项 |
|-------------|--------|----------|
| EMAIL_SENDER | `your_qq@qq.com` | 必须是 QQ 邮箱 |
| EMAIL_PASSWORD | `abcd1234efgh5678` | 见下文获取授权码 |
| EMAIL_RECIPIENT | `partner@email.com` | 收件人邮箱 |
| WEATHER_API_KEY | `xxxxxxxxxxxxxxxx` | 见下文获取 API Key |
| LOVE_START_DATE | `2023-01-01` | 格式必须为 YYYY-MM-DD |
| CITY | `Beijing` | 使用英文城市名 |

添加完成后，Secrets 列表应类似如下：

```
✅ EMAIL_SENDER
✅ EMAIL_PASSWORD  
✅ EMAIL_RECIPIENT
✅ WEATHER_API_KEY
✅ LOVE_START_DATE
✅ CITY
```

## QQ 邮箱授权码获取

QQ 邮箱必须使用授权码而非登录密码进行 SMTP 发送。获取步骤如下：

### 第一步：登录 QQ 邮箱

1. 打开 https://mail.qq.com
2. 使用你的 QQ 号和密码登录

### 第二步：进入账户设置

1. 点击右上角的 "设置" 按钮（齿轮图标）
2. 在弹出的菜单中选择 "账户"
3. 在账户页面，向下滚动找到 "POP3/IMAP/SMTP/Exchange/CardDAV/CalDAV服务" 部分

### 第三步：开启 SMTP 服务

1. 找到 "IMAP/SMTP 服务" 项
2. 点击右侧的 "开启" 链接
3. 按照提示发送短信进行验证（发送指定内容到指定号码）
4. 验证成功后，页面会显示一个 16 位的授权码

### ⚠️ 重要提醒

- 授权码 **只会显示一次**，请立即复制保存
- 如果忘记保存，需要重新开启服务获取新授权码
- 授权码不是你的 QQ 登录密码
- 每次重新开启服务可能会生成新的授权码

## OpenWeatherMap API Key 获取

### 第一步：注册账户

1. 打开 https://openweathermap.org
2. 点击右上角的 "Sign Up" 按钮
3. 使用邮箱注册一个免费账户

### 第二步：创建 API Key

1. 登录后，点击右上角的用户名，选择 "My API Keys"
2. 点击 "Create API Key" 按钮
3. 输入一个名称（如 "love-email"）并确认

### 第三步：等待生效

- 新创建的 API Key 需要 **10-15 分钟** 才能生效
- 立即使用可能会提示 API Key 无效

### 免费额度说明

- 免费账户每天 **1000 次** API 调用
- 本项目每天调用 1 次，完全足够

## 手动触发测试

配置完成后，建议先手动触发一次测试，验证配置是否正确。

### 操作步骤

1. 进入仓库的 "Actions" 页面
2. 在左侧菜单中找到 "Daily Love Email" 工作流
3. 点击 "Run workflow" 按钮
4. 确认后点击 "Run workflow" 绿色按钮
5. 等待几秒钟，刷新页面查看运行状态
6. 点击最新的运行记录查看详情

### 检查结果

- 运行状态显示 ✅ 绿色勾：表示邮件发送成功
- 运行状态显示 ❌ 红色叉：表示发送失败，点击查看错误信息
- 查看运行日志中的 "send-email" job，确认无报错

## 定时任务修改

### 当前配置

工作流默认配置为每天 **北京时间 00:00（零点）** 执行：

```yaml
schedule:
  - cron: '0 0 * * *'
```

### 常用 cron 表达式

| cron 表达式 | 执行时间 | 说明 |
|-------------|----------|------|
| `0 0 * * *` | 每天 00:00 | 零点（默认） |
| `0 8 * * *` | 每天 08:00 | 早上八点 |
| `0 12 * * *` | 每天 12:00 | 中午十二点 |
| `0 7 * * *` | 每天 07:00 | 早上七点 |
| `0 9 * * 1-5` | 工作日 09:00 | 仅工作日早上九点 |
| `0 20 * * *` | 每天 20:00 | 晚上八点 |

### 修改方法

1. 打开 `.github/workflows/daily-email.yml` 文件
2. 找到 `schedule` 部分的 cron 表达式
3. 修改为 desired 时间对应的 cron 表达式
4. 提交更改

示例，修改为每天早上八点发送：

```yaml
on:
  schedule:
    - cron: '0 0 * * *'  # 北京时间 0:00 = UTC 16:00
  workflow_dispatch:
```

## 故障排查

### 邮件发送失败

#### 错误：Authentication failed

**原因**：授权码错误或已失效

**解决方法**：
1. 登录 QQ 邮箱，重新获取授权码
2. 在 GitHub Secrets 中更新 EMAIL_PASSWORD
3. 重新触发工作流测试

#### 错误：SMTP connect failed

**原因**：SMTP 服务器或端口配置错误

**解决方法**：
1. 确认 SMTP_SERVER 值为 `smtp.qq.com`
2. 确认 SMTP_PORT 值为 `465`
3. 检查 QQ 邮箱是否开启了 IMAP/SMTP 服务

### 天气 API 失败

#### 错误：401 Unauthorized

**原因**：API Key 无效或未生效

**解决方法**：
1. 确认 WEATHER_API_KEY 填写正确
2. 新创建的 API Key 需要等待 10-15 分钟
3. 访问 OpenWeatherMap 检查 API Key 状态

#### 错误：404 City not found

**原因**：城市名称拼写错误

**解决方法**：
1. CITY 必须使用英文城市名
2. 正确示例：`Beijing`、`Shanghai`、`Hangzhou`
3. 错误示例：`北京`、`上海`、`杭州`

### 其他问题

#### 查看运行日志

1. 进入 Actions 页面
2. 点击失败的运行记录
3. 点击 "send-email" job
4. 滚动查看详细的错误信息

#### 常见错误代码

| 错误信息 | 可能原因 |
|----------|----------|
| `smtplib.SMTPAuthenticationError` | 授权码错误 |
| `smtplib.SMTPServerDisconnected` | SMTP 服务未开启 |
| `requests.exceptions.HTTPError 401` | API Key 无效 |
| `requests.exceptions.HTTPError 404` | 城市名称错误 |

## 安全提醒

- **不要** 在任何公开场合分享你的 Secrets
- **不要** 将包含真实值的 Secrets 提交到代码仓库
- **定期** 检查并更新授权码（QQ 邮箱可能会定期失效）
- 如果怀疑泄露，立即在 GitHub Secrets 中更新
- 本地开发时，敏感信息只存在于你的电脑，请妥善保管
