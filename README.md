# 每日恋爱邮件 Daily Love Email

自动化每日邮件发送脚本，为你的另一半送上温暖的早安祝福。

![Python Version](https://img.shields.io/badge/Python-3.10%2B-blue)
![GitHub Actions](https://img.shields.io/badge/GitHub%20Actions-自动执行-brightgreen)

## 项目介绍

每日恋爱邮件是一个基于 GitHub Actions 的自动化邮件发送项目，每天定时为你的另一半发送一封温暖的邮件，内容包含恋爱天数、天气预报、每日情话和纪念日提醒。

### 功能特性

- **📅 恋爱天数** - 自动计算并显示你们在一起的天数
- **🌤️ 天气预报** - 获取目标城市的实时天气信息
- **💌 每日情话** - 随机推送一条温馨的恋爱语录
- **🎉 纪念日提醒** - 记录并提醒即将到来的重要纪念日

### 截图预览

![每日恋爱邮件预览](screenshot.png)

## 快速开始

### 项目原理

项目使用 GitHub Actions 定时触发 Python 脚本执行，脚本会自动完成以下工作：读取配置文件、计算恋爱天数、获取天气数据、选择每日情话、渲染邮件模板，最后通过 SMTP 协议发送邮件。

### 部署流程概览

整个部署流程非常简单，只需四个步骤：Fork 本仓库、配置 GitHub Secrets、修改配置文件、启用 GitHub Actions。整个过程不需要服务器，不需要付费，完完全全免费使用。

## 安装与配置

本项目支持两种使用方式，请根据你的需求选择合适的方案。

### 使用方式选择

| 对比项 | 方案 A：本地运行 | 方案 B：GitHub Actions |
|--------|-----------------|----------------------|
| 配置文件 | config.yaml | GitHub Secrets |
| 运行环境 | 你自己的电脑 | GitHub 服务器 |
| 触发方式 | 手动执行命令 | 定时自动执行 |
| 适合场景 | 测试、开发调试 | 长期自动运行 |

**建议**：
- 如果你想先测试项目是否正常工作，选择**方案 A**
- 如果你想让邮件每天自动发送，选择**方案 B**

---

### 方案 A：本地运行（适合测试）

如果你想在本地测试项目是否正常工作，可以使用 config.yaml 配置文件。

#### 适用场景

- 首次使用想先测试功能
- 需要在本地开发和调试
- 不想依赖 GitHub

#### 配置步骤

**第一步：准备配置文件**

复制 `config.yaml.example` 文件，重命名为 `config.yaml`：

```bash
cp config.yaml.example config.yaml
```

然后根据你的实际情况修改配置：

```yaml
# 邮件配置
email:
  sender: "your_qq_email@qq.com"
  password: "your_auth_code"
  recipient: "partner@example.com"
  smtp_server: "smtp.qq.com"
  smtp_port: 465

# 恋爱信息
love:
  start_date: "2023-01-01"
  
# 纪念日列表
anniversaries:
  - name: "恋爱纪念日"
    date: "01-01"
  - name: "TA的生日"
    date: "12-25"
    
# 天气配置
weather:
  city: "北京市"                       # 城市名称（中文，如"北京市"、"上海"）
  api_key: "your_amap_api_key"         # 高德地图天气 API Key

# 其他配置
app:
  timezone: "Asia/Shanghai"
```

**第二步：安装依赖**

```bash
pip install -r requirements.txt
```

**第三步：测试运行**

```bash
# 干运行模式，不发送邮件，只显示邮件内容预览
python src/main.py --dry-run

# 发送测试邮件到指定邮箱
python src/main.py --test-email your_test_email@example.com
```

配置项详细说明见「配置文件说明」章节。

---

### 方案 B：GitHub Actions（适合长期使用）

如果想让邮件每天自动发送，使用 GitHub Secrets 配置会更简单，无需维护电脑开机。

#### 适用场景

- 每天自动发送邮件
- 不想一直开着电脑
- 追求完全自动化

#### 配置步骤

**第一步：Fork 仓库**

访问 GitHub 仓库页面，点击右上角的 "Fork" 按钮，将项目复制到你的账户下。

**第二步：配置 GitHub Secrets**

进入你的仓库页面，点击 Settings → Secrets and variables → Actions，点击 "New repository secret" 按钮，添加以下 Secrets：

| Secret 名称 | 说明 | 是否必需 |
|-------------|------|----------|
| EMAIL_SENDER | 发件人 QQ 邮箱 | 必需 |
| EMAIL_PASSWORD | QQ 邮箱授权码 | 必需 |
| EMAIL_RECIPIENT | 收件人邮箱 | 必需 |
| WEATHER_API_KEY | 高德地图天气 API Key | 必需 |
| LOVE_START_DATE | 恋爱起始日期 (YYYY-MM-DD) | 必需 |
| CITY | 目标城市（中文） | 必需 |
| ANNIVERSARIES | 纪念日列表（JSON 格式） | 必需 |
| SENDER_NAME | 发件人显示称呼（可选） | 可选 |
| RECIPIENT_NAME | 收件人显示称呼（可选） | 可选 |

<!-- AUTO-GENERATED: GitHub Secrets -->

详细的授权码和 API Key 获取方法见下文「GitHub Secrets 详细配置」章节。

**第三步：启用 GitHub Actions**

进入仓库的 Actions 页面，点击 "I understand my workflows, go ahead and enable them" 按钮启用 Actions。

**第四步：手动触发测试**

配置完成后，建议先手动触发一次测试：

1. 进入仓库的 "Actions" 页面
2. 找到 "Daily Love Email" 工作流
3. 点击 "Run workflow" → "Run workflow"
4. 等待几秒钟，刷新页面查看运行状态
5. 点击运行记录查看详情，确认无报错

现在每天早上八点就会自动发送邮件了。

> 详细的 Secrets 配置说明、授权码获取方法、常见问题排查，请参阅 [.github/secrets_template.md](./.github/secrets_template.md)。

---

## GitHub Secrets 详细配置

### QQ 邮箱授权码获取步骤

QQ 邮箱需要使用授权码而非登录密码进行 SMTP 发送。获取授权码的步骤如下：

第一步，登录 QQ 邮箱网页版，点击右上角的设置按钮，选择"账户"选项。

第二步，在账户页面找到"POP3/IMAP/SMTP/Exchange/CardDAV/CalDAV服务"部分，点击"开启"IMAP/SMTP 服务。

第三步，按照提示发送短信进行验证，验证成功后页面会显示授权码。请务必保存好这个授权码，它只会显示一次。

### 高德地图 API Key 获取

第一步，访问高德地图开放平台 (https://lbs.amap.com) 并注册一个开发者账户。

第二步，登录后进入「应用管理」→「我的应用」，点击「创建新应用」，填写应用名称和类型。

第三步，在创建的应用下点击「添加 Key」，选择「Web服务」作为服务平台，提交后即可获得 API Key。

高德地图免费版每日提供 5000 次天气 API 调用额度，完全满足每日邮件的需求。

**注意**：新创建的 Key 可能需要几分钟才能生效。

## 配置文件说明

config.yaml 文件包含以下配置项：

### email 配置段

| 字段 | 说明 | 示例 | 必需 |
|------|------|------|------|
| sender | 发件人邮箱地址 | your_email@qq.com | 必需 |
| password | QQ 邮箱授权码 | xxxxxxxx | 必需 |
| recipient | 收件人邮箱地址 | partner@email.com | 必需 |
| smtp_server | SMTP 服务器地址 | smtp.qq.com | 必需 |
| smtp_port | SMTP 端口号 | 465 | 必需 |
| sender_name | 发件人显示称呼（可选） | 你的名字 | 可选 |
| recipient_name | 收件人显示称呼（可选） | 亲爱的 | 可选 |

<!-- AUTO-GENERATED: email config -->

### love 配置段

| 字段 | 说明 | 示例 |
|------|------|------|
| start_date | 恋爱起始日期，格式为 YYYY-MM-DD | 2023-01-01 |

### anniversaries 配置段

这是一个列表，可以添加多个纪念日。每个纪念日包含：

| 字段 | 说明 | 示例 |
|------|------|------|
| name | 纪念日名称 | 恋爱纪念日 |
| date | 纪念日日期，格式为 MM-DD | 01-01 |

### weather 配置段

| 字段 | 说明 | 示例 |
|------|------|------|
| city | 目标城市名称（中文） | 北京市 |
| api_key | 高德地图天气 API Key | xxxxxxxx |

### app 配置段

| 字段 | 说明 | 示例 | 必需 |
|------|------|------|------|
| timezone | 时区设置 | Asia/Shanghai | 必需 |
| template | 邮件模板名称（当前仅支持 romantic） | romantic | 可选 |
| background_type | 背景类型 (gradient / solid / image) | gradient | 可选 |
| background_image | 背景图片主题 (romantic / nature / custom) | romantic | 可选 |
| card_background_type | 卡片背景类型 (image / gradient / solid) | image | 可选 |
| card_background_value | 卡片背景值 (与 background_image 相同) | romantic | 可选 |

**注意**：图片资源默认从 GitHub 仓库 `Stinncsky/daily-love-email` 加载，无需额外配置环境变量即可本地测试。

## 本地开发

如果你想在本地开发和测试项目，请按照以下步骤操作。

### 环境准备

确保你的电脑上安装了 Python 3.10 或更高版本。你可以在终端中运行以下命令检查 Python 版本：

```bash
python --version
```

如果显示的版本号低于 3.10，请前往 Python 官网 下载安装最新版本。

### 安装依赖

克隆你的仓库到本地，进入项目目录，运行以下命令安装依赖：

```bash
pip install -r requirements.txt
```

requirements.txt 文件包含以下依赖：

- requests：用于发送 HTTP 请求获取天气数据
- pyyaml：用于解析配置文件
- jinja2：用于渲染邮件模板

### 配置本地环境

本地运行使用 `config.yaml` 配置文件，详细配置步骤见「方案 A：本地运行」章节。

### 本地测试运行

完成配置后，可以运行以下命令进行本地测试：

```bash
# 干运行模式，不发送邮件，只显示邮件内容
python src/main.py --dry-run

# 发送测试邮件到指定邮箱
python src/main.py --test-email your_test_email@example.com

# 生成邮件 HTML 预览文件（不发送邮件）
python scripts/generate_email.py

# 生成预览并指定配置文件和输出目录
python scripts/generate_email.py -c config.yaml -o ./output

# 生成预览并在浏览器中打开
python scripts/generate_email.py --open
```

`scripts/generate_email.py` 脚本用于生成邮件 HTML 预览文件，方便在浏览器中查看邮件效果。生成的文件保存在 `output/` 目录，文件名格式为 `email_YYYYMMDD_HHMMSS.html`。

## 测试

项目包含完整的单元测试，涵盖核心功能模块。

### 运行单元测试

在项目根目录下运行：

```bash
pytest tests/
```

测试覆盖了以下模块：

- 恋爱天数计算 (test_calculator.py)
- 纪念日处理 (test_anniversary.py)
- 天气获取 (test_weather.py)
- 情话获取 (test_quotes.py)

### 发送测试邮件

使用以下命令发送测试邮件：

```bash
# 发送到配置文件中指定的收件人
python src/main.py

# 发送到指定邮箱
python src/main.py --test-email your_test_email@example.com
```

## FAQ 常见问题

### 邮件发送失败怎么办

邮件发送失败可能有以下几个原因。首先，检查 QQ 邮箱授权码是否正确，授权码只能使用一次，如果遗失需要重新获取。其次，确认 SMTP 端口是否正确，QQ 邮箱使用 465 端口。第三，查看 GitHub Actions 的运行日志，错误信息会详细说明失败原因。

如果问题仍然存在，可以在 GitHub Actions 页面查看详细的运行日志，日志中会包含具体的错误信息和堆栈跟踪，帮助你定位问题。

### 如何修改发送时间

GitHub Actions 的触发时间由 `.github/workflows/daily-email.yml` 文件中的 cron 表达式控制。当前配置为每天早上八点执行：

```yaml
schedule:
  - cron: '0 8 * * *'
```

如果你想修改发送时间，比如改为早上九点，可以将 cron 表达式改为 `0 9 * * *`。关于 cron 表达式的更多用法，可以参考 crontab.guru 网站。

### 如何添加更多纪念日

在 config.yaml 文件的 anniversaries 列表中添加新条目即可：

```yaml
anniversaries:
  - name: "恋爱纪念日"
    date: "01-01"
  - name: "TA的生日"
    date: "12-25"
  - name: "第一次约会"
    date: "05-20"
```

date 字段使用 MM-DD 格式，每年会自动重复。

### 如何更换天气 API

如果你想使用其他天气服务提供商，比如心知天气或和风天气，只需要修改 src/weather.py 文件中的 API 调用逻辑即可。项目使用了模块化设计，更换天气 API 非常方便。你只需要保持 get_weather 函数的返回格式不变即可。

## V2 版本路线图

项目会持续更新，以下是 V2 版本计划开发的功能：

- **星座运势** - 每日推送双方星座的运势预测
- **AI 个性化内容** - 利用 AI 生成更加个性化的情话和内容
- **更多纪念日类型** - 支持阴历日期、倒数计时等
- **邮件模板主题切换** - 支持多套邮件模板
- **多语言支持** - 支持英文邮件
- **更多天气数据** - 增加空气质量、湿度、紫外线指数等
- **情感分析** - 根据天气、日期等因素调整邮件语气

如果你有好的功能建议，欢迎提交 Issue 或 Pull Request。

## 致谢

本项目参考和使用了以下开源项目：

- [requests](https://docs.python-requests.org/) - Python HTTP 库
- [PyYAML](https://pyyaml.org/) - YAML 配置文件解析
- [Jinja2](https://jinja.palletsprojects.com/) - 模板引擎
- [高德地图开放平台](https://lbs.amap.com/) - 天气数据 API

感谢所有开源贡献者的付出。

---

Made with ❤️ for love
