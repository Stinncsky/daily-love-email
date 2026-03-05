# GitHub Secrets 配置模板

项目背景：每日浪漫邮件自动发送系统，使用 GitHub Actions + Python + QQ 邮箱 SMTP。请按照本模板在仓库的 Settings 里配置隐私密钥（Secrets）。

## Secrets 列表
- EMAIL_SENDER: 发件人邮箱
- EMAIL_PASSWORD: 邮箱授权码（不是登录密码）
- EMAIL_RECIPIENT: 收件人邮箱
- WEATHER_API_KEY: OpenWeatherMap API 密钥
- SMTP_SERVER: SMTP服务器（可选，默认 smtp.qq.com）
- SMTP_PORT: SMTP端口（可选，默认 465）

## 配置步骤
- 打开 GitHub 仓库 → Settings → Secrets and variables → Actions
- 点击 "New repository secret"
- 依次添加下列 Secrets：EMAIL_SENDER、EMAIL_PASSWORD、EMAIL_RECIPIENT、WEATHER_API_KEY、SMTP_SERVER、SMTP_PORT
- 如未设置 SMTP_SERVER/SMTP_PORT，建议在工作流中提供默认值，或在 Secrets 中添加默认值

## QQ邮箱授权码获取说明
- 登录 QQ 邮箱网页版
- 设置 → 账户 → 开启 SMTP 服务
- 获取授权码（16位字符串）
- 强调：使用授权码而非登录密码

## OpenWeatherMap API Key 获取
- 访问 openweathermap.org
- 注册免费账户
- 获取 API Key

## 示例配置
### YAML 示例
```yaml
EMAIL_SENDER: "your_email@example.com"
EMAIL_PASSWORD: "your_authorization_code"
EMAIL_RECIPIENT: "recipient@example.com"
WEATHER_API_KEY: "your_openweathermap_api_key"
SMTP_SERVER: "smtp.qq.com"  # optional
SMTP_PORT: 465            # optional
```

### JSON 示例
```json
{
  "EMAIL_SENDER": "your_email@example.com",
  "EMAIL_PASSWORD": "your_authorization_code",
  "EMAIL_RECIPIENT": "recipient@example.com",
  "WEATHER_API_KEY": "your_openweathermap_api_key",
  "SMTP_SERVER": "smtp.qq.com",
  "SMTP_PORT": 465
}
```

> 注意：以上示例中的值均为占位符，请在 GitHub UI 的 Secrets 中配置实际的密钥和邮箱信息。

## MUST NOT DO
- 请勿在文档中放置真实的密钥或密码
- 不要把包含敏感信息的词汇作为文件名

## CONTEXT
### Project Context
- 项目：每日浪漫邮件自动发送系统，使用 GitHub Actions + Python + QQ邮箱SMTP。
- 相关文件：.github/workflows/daily-email.yml、config.yaml.example
