# 邮件 Bug 修复计划

## 问题总结

根据用户收到的测试邮件截图，发现以下问题：
1. "我们在一起"显示为 **"None"**
2. 显示 **"0 年 0 个月"**
3. **缺少天气信息**
4. **缺少纪念日信息**

## Root Cause 分析

### Bug 1: 恋爱天数显示"None"
**位置**: `src/main.py` 第148行
**问题**: 给 `calculate_days_together` 传递了两个参数，但函数只接受一个参数

```python
# 当前错误代码 (第148行)
days = safe_call(calculate_days_together, cfg.get("start_date"), date.today())

# 问题分析
# calculate_days_together 函数签名: def calculate_days_together(start_date: str) -> Tuple[int, int, int]
# 它只接受 start_date 一个参数，date.today() 是多余的
# 这会导致 TypeError，被 safe_call 捕获后返回 None
```

### Bug 2: 年月日没有正确传递
**位置**: `src/main.py` 第148行 + `src/template.py`
**问题**: 
- `calculate_days_together` 返回 `(days, months, years)` 元组
- 但代码只用一个变量 `days` 接收
- 模板期望 `days_together`, `months_together`, `years_together` 三个独立变量

### Bug 3: 天气信息缺失
**位置**: `src/main.py` 第149行 + `src/weather.py`
**问题**:
1. `main.py` 使用 `cfg.get("location")`，但 config.yaml 中是 `weather.city`
2. `weather.py` 查找 `OPENWEATHER_API_KEY` 环境变量，但 GitHub Secrets 设置的是 `WEATHER_API_KEY`

```python
# 当前错误代码 (第149行)
weather = safe_call(get_weather, cfg.get("location", ""))

# config.yaml 结构是:
# weather:
#   city: "Beijing"
#   api_key: "xxx"

# 应该使用 cfg.get("weather", {}).get("city")
```

### Bug 4: 纪念日信息缺失
**位置**: `src/main.py` 第151行
**问题**: 把整个 `cfg` 传给 `get_next_anniversary`，但函数期望 `anniversaries` 列表

```python
# 当前错误代码 (第151行)
anniversary = safe_call(get_next_anniversary, cfg)

# get_next_anniversary 函数签名: def get_next_anniversary(anniversaries: List[Dict])
# 应该传递 cfg.get("anniversaries", [])
```

### Bug 5: build_context 没有传递年月日
**位置**: `src/main.py` 第121-129行
**问题**: `build_context` 只接收 `days` 一个参数，但需要解构为 `days`, `months`, `years`

### Bug 6: render_email 的数据适配问题
**位置**: `src/template.py` 第89-117行
**问题**: `render_email` 函数中的近似计算逻辑不正确（days // 30 和 days // 365 太粗糙）

### Bug 7: config.yaml 嵌套结构未适配 ❗**新增**
**位置**: `src/main.py` 多处
**问题**: 代码使用扁平化的键名，但 `config.yaml` 使用嵌套结构

| 代码使用的键 | config.yaml 实际路径 |
|-------------|---------------------|
| `cfg.get("start_date")` | `cfg.get("love", {}).get("start_date")` |
| `cfg.get("to_email")` | `cfg.get("email", {}).get("recipient")` |
| `cfg.get("from_email")` | `cfg.get("email", {}).get("sender")` |
| `cfg.get("location")` | `cfg.get("weather", {}).get("city")` |
| `cfg.get("smtp_password")` | `cfg.get("email", {}).get("password")` |
| `cfg.get("smtp_server")` | `cfg.get("email", {}).get("smtp_server")` |
| `cfg.get("smtp_port")` | `cfg.get("email", {}).get("smtp_port")` |

**决策**: 保持 `config.yaml` 的嵌套结构（语义清晰、易于维护），修改代码去正确读取它。

---

## 修复方案

### 修复 1: main.py - 修正 calculate_days_together 调用

**文件**: `src/main.py`  
**行**: 148

**修改前**:
```python
days = safe_call(calculate_days_together, cfg.get("start_date"), date.today())
```

**修改后**:
```python
# calculate_days_together 返回 (days, months, years) 元组
calc_result = safe_call(calculate_days_together, cfg.get("start_date"))
if calc_result and isinstance(calc_result, tuple) and len(calc_result) == 3:
    days, months, years = calc_result
else:
    days, months, years = 0, 0, 0
```

---

### 修复 2: main.py - 修正天气调用

**文件**: `src/main.py`  
**行**: 149

**修改前**:
```python
weather = safe_call(get_weather, cfg.get("location", ""))
```

**修改后**:
```python
# 从 cfg 中获取天气配置
weather_cfg = cfg.get("weather", {})
city = weather_cfg.get("city") or cfg.get("location", "")
api_key = weather_cfg.get("api_key")
weather = safe_call(get_weather, city, api_key) if city else None
```

---

### 修复 3: main.py - 修正纪念日调用

**文件**: `src/main.py`  
**行**: 151

**修改前**:
```python
anniversary = safe_call(get_next_anniversary, cfg)
```

**修改后**:
```python
# 传递 anniversaries 列表，而不是整个 cfg
anniversaries_list = cfg.get("anniversaries", [])
anniversary = safe_call(get_next_anniversary, anniversaries_list) if anniversaries_list else None
```

---

### 修复 4: main.py - 修改 build_context 函数

**文件**: `src/main.py`  
**行**: 121-129

**修改前**:
```python
def build_context(cfg, days, weather, quote, anniversary):
    return {
        "config": cfg,
        "days_together": days,
        "weather": weather,
        "quote": quote,
        "anniversary": anniversary,
        "date": date.today().isoformat(),
    }
```

**修改后**:
```python
def build_context(cfg, days, months, years, weather, quote, anniversary):
    return {
        "config": cfg,
        "days_together": days,
        "months_together": months,
        "years_together": years,
        "weather": weather,
        "quote": quote,
        "anniversary": anniversary,
        "date": date.today().isoformat(),
    }
```

---

### 修复 5: main.py - 更新函数调用

**文件**: `src/main.py`  
**行**: 154

**修改前**:
```python
context = build_context(cfg, days, weather, quote, anniversary)
```

**修改后**:
```python
context = build_context(cfg, days, months, years, weather, quote, anniversary)
```

---

### 修复 6: template.py - 改进 render_email 函数

**文件**: `src/template.py`  
**行**: 89-117

**修改前**:
```python
def render_email(context: dict) -> str:
    """
    Render email template with main.py compatible interface.
    
    This is a wrapper that adapts main.py's context format to 
    render_email_with_data's expected format.
    
    Args:
        context: Dict from main.py with keys: days_together, quote, weather, 
                 anniversary, date, config
                 
    Returns:
        Rendered HTML string
    """
    import datetime
    
    days = context.get("days_together", 0)
    
    # Build data dict for render_email_with_data
    data = {
        "days_together": days,
        "months_together": days // 30 if days else 0,
        "years_together": days // 365 if days else 0,
        "quote": context.get("quote", {"content": "", "category": ""}),
        "weather": context.get("weather"),
        "next_anniversary": context.get("anniversary"),
        "today": context.get("date", datetime.date.today().isoformat()),
    }
    
    return render_email_with_data(data)
```

**修改后**:
```python
def render_email(context: dict) -> str:
    """
    Render email template with main.py compatible interface.
    
    This is a wrapper that adapts main.py's context format to 
    render_email_with_data's expected format.
    
    Args:
        context: Dict from main.py with keys: days_together, months_together, 
                 years_together, quote, weather, anniversary, date, config
                 
    Returns:
        Rendered HTML string
    """
    import datetime
    
    # 直接使用 context 中的值，不再重新计算
    days = context.get("days_together", 0)
    months = context.get("months_together", 0)
    years = context.get("years_together", 0)
    
    # Build data dict for render_email_with_data
    data = {
        "days_together": days,
        "months_together": months,
        "years_together": years,
        "quote": context.get("quote", {"content": "", "category": ""}),
        "weather": context.get("weather"),
        "next_anniversary": context.get("anniversary"),
        "today": context.get("date", datetime.date.today().isoformat()),
    }
    
    return render_email_with_data(data)
```

---

### 修复 7: weather.py - 支持 WEATHER_API_KEY

**文件**: `src/weather.py`  
**行**: 16

**修改前**:
```python
key = api_key or os.environ.get("OPENWEATHER_API_KEY")
```

**修改后**:
```python
key = api_key or os.environ.get("WEATHER_API_KEY") or os.environ.get("OPENWEATHER_API_KEY")
```

---

### 修复 8: email.html - 修正天气字段名

**文件**: `templates/email.html`  
**行**: 144

**问题**: 模板使用 `weather.temp`，但 weather.py 返回的是 `temperature`

**修改前**:
```html
<span class="weather-value" style="font-size: 28px; font-weight: 700; display: block;">{{ weather.temp }}°C</span>
```

**修改后**:
```html
<span class="weather-value" style="font-size: 28px; font-weight: 700; display: block;">{{ weather.temperature }}°C</span>
```

---

## 完整的修改后 main.py 关键部分

```python
def main():
    parser = argparse.ArgumentParser(description="Daily Love Email Orchestrator")
    parser.add_argument("--dry-run", dest="dry_run", action="store_true", help="Test without sending email")
    parser.add_argument("--test-email", dest="test_email", default=None, help="Override recipient email for testing")
    args = parser.parse_args()

    dry_run = bool(args.dry_run)
    test_email = args.test_email

    cfg = load_config_safe()
    if not cfg:
        log.error("Configuration is empty. Aborting.")
        return 1

    # Bug 1 & 2 修复: 正确处理 calculate_days_together 返回值
    calc_result = safe_call(calculate_days_together, cfg.get("start_date"))
    if calc_result and isinstance(calc_result, tuple) and len(calc_result) == 3:
        days, months, years = calc_result
    else:
        days, months, years = 0, 0, 0

    # Bug 3 修复: 正确获取天气配置
    weather_cfg = cfg.get("weather", {})
    city = weather_cfg.get("city") or cfg.get("location", "")
    api_key = weather_cfg.get("api_key")
    weather = safe_call(get_weather, city, api_key) if city else None

    quote = safe_call(get_random_quote)

    # Bug 4 修复: 正确传递 anniversaries 列表
    anniversaries_list = cfg.get("anniversaries", [])
    anniversary = safe_call(get_next_anniversary, anniversaries_list) if anniversaries_list else None

    # Bug 5 修复: 传递 months 和 years 到 context
    context = build_context(cfg, days, months, years, weather, quote, anniversary)
    body = render_email(context) if callable(render_email) else ""

    recipient = test_email or cfg.get("to_email")
    subject = cfg.get("subject", "Daily Love Email")

    if not recipient:
        log.error("No recipient email configured (TO_EMAIL). Aborting.")
        return 1

    if dry_run:
        log.info("Dry-run: email would be sent to %s with subject '%s'", recipient, subject)
        # 在干运行模式下打印邮件内容预览
        print("\n" + "="*60)
        print("邮件内容预览:")
        print("="*60)
        print(f"恋爱天数: {days} 天 ({years} 年 {months} 个月)")
        print(f"天气: {weather}")
        print(f"语录: {quote}")
        print(f"纪念日: {anniversary}")
        print("="*60 + "\n")
    else:
        if callable(send_email):
            sent = safe_call(send_email, cfg, subject, body, to=recipient)
            if sent is None:
                sent = safe_call(send_email, recipient, subject, body)
            if sent is False:
                log.error("Email sending failed.")
        else:
            log.warning("send_email() not available; skipping actual send in this environment.")

    log.info("Workflow completed. dry_run=%s, recipient=%s", dry_run, recipient)
    try:
        summary_line = (
            f"{date.today().isoformat()} | dry_run={dry_run} | to={recipient} | "
            f"days={days} | weather={weather} | quote={quote} | anniversary={anniversary}"
        )
        append_learning_log(summary_line)
    except Exception as e:
        log.debug("Skipping learnings append due to error: %s", e)
    return 0
```

---

## 测试步骤

1. 保存所有修改
2. 运行干运行模式测试:
   ```bash
   python src/main.py --dry-run
   ```
3. 检查输出中是否正确显示:
   - 恋爱天数（数字而不是 None）
   - 年月
   - 天气信息
   - 纪念日信息
4. 发送测试邮件:
   ```bash
   python src/main.py --test-email your_email@example.com
   ```

---

## 提交注意事项

**不要提交 `config.yaml`**（包含敏感信息）

```bash
# 确保 config.yaml 在 .gitignore 中
echo "config.yaml" >> .gitignore

# 提交修复
git add src/main.py src/template.py src/weather.py templates/email.html
git commit -m "fix: 修复邮件内容显示问题

- 修正 calculate_days_together 参数传递错误
- 正确解构返回的 (days, months, years) 元组
- 修正天气配置路径和 API key 环境变量名
- 修正纪念日传参，传递列表而非整个配置
- 修正模板中天气字段名 temp -> temperature
- 增强干运行模式输出，方便调试"
```

---

## 预计修复时间

- 修改代码: 10分钟
- 本地测试: 5分钟
- 提交: 2分钟
- **总计: ~17分钟**

---

## 新增功能: 发送者/收件人称呼配置

### 功能说明

在邮件中添加个性化称呼，让邮件更温馨。例如：
- 发送者称呼: "老公"、"亲爱的"、"宝贝"
- 收件人称呼: "老婆"、"亲爱的"、"小仙女"

### 配置位置

建议在 `config.yaml` 的 `email` 配置段添加：

```yaml
# 邮件配置
email:
  sender: "1767425567@qq.com"
  sender_name: "老公"              # 新增：发送者称呼
  recipient: "stinncsky@gmail.com"
  recipient_name: "老婆"           # 新增：收件人称呼
  password: "..."
  smtp_server: "smtp.qq.com"
  smtp_port: 465
```

### 需要修改的文件

1. **config.yaml.example** - 添加示例配置
2. **main.py** - 读取称呼配置并传递给模板
3. **email.html** - 在邮件中显示称呼

### 实现方案

#### 1. config.yaml.example 添加示例

```yaml
# 邮件配置
email:
  sender: "your_qq_email@qq.com"
  sender_name: "老公"              # 发送者称呼（可选）
  recipient: "partner@example.com"
  recipient_name: "老婆"           # 收件人称呼（可选）
  password: "your_auth_code"
  smtp_server: "smtp.qq.com"
  smtp_port: 465
```

#### 2. main.py 读取并传递称呼

在 `build_context` 函数中添加：

```python
def build_context(cfg, days, months, years, weather, quote, anniversary):
    email_cfg = cfg.get("email", {})
    return {
        "config": cfg,
        "days_together": days,
        "months_together": months,
        "years_together": years,
        "weather": weather,
        "quote": quote,
        "anniversary": anniversary,
        "date": date.today().isoformat(),
        "sender_name": email_cfg.get("sender_name", ""),        # 新增
        "recipient_name": email_cfg.get("recipient_name", ""),  # 新增
    }
```

#### 3. email.html 显示称呼

在邮件头部添加称呼显示（可选，根据需求决定是否显示）：

```html
<!-- 在 Header Section 中添加称呼 -->
<tr>
    <td style="background: linear-gradient(135deg, #FF6B6B 0%, #FF8E8E 100%); border-radius: 16px 16px 0 0; padding: 40px 30px; text-align: center;">
        <table border="0" cellpadding="0" cellspacing="0" width="100%">
            <tr>
                <td style="text-align: center;">
                    {% if sender_name and recipient_name %}
                    <p style="margin: 0 0 10px; color: rgba(255,255,255,0.9); font-size: 14px;">
                        {{ sender_name }} ❤️ {{ recipient_name }}
                    </p>
                    {% endif %}
                    <span style="font-size: 40px; line-height: 1;">💕</span>
                    <h1 class="header-text" style="margin: 15px 0 10px; color: #ffffff; font-size: 26px; font-weight: 600; letter-spacing: 2px;">每日爱情</h1>
                    <p style="margin: 0; color: rgba(255,255,255,0.9); font-size: 14px;">{{ today }}</p>
                </td>
            </tr>
        </table>
    </td>
</tr>
```

#### 4. render_email 函数适配

```python
def render_email(context: dict) -> str:
    import datetime
    
    days = context.get("days_together", 0)
    months = context.get("months_together", 0)
    years = context.get("years_together", 0)
    
    data = {
        "days_together": days,
        "months_together": months,
        "years_together": years,
        "quote": context.get("quote", {"content": "", "category": ""}),
        "weather": context.get("weather"),
        "next_anniversary": context.get("anniversary"),
        "today": context.get("date", datetime.date.today().isoformat()),
        "sender_name": context.get("sender_name", ""),        # 新增
        "recipient_name": context.get("recipient_name", ""),  # 新增
    }
    
    return render_email_with_data(data)
```

### 效果预览

配置了称呼后，邮件头部会显示：
```
老公 ❤️ 老婆

💕
每日爱情
2026-03-06
```

如果没有配置称呼，则保持原样不显示。

### 优先级

这个功能是**增强功能**，不是 Bug 修复。可以：
- **方案A**: 和 Bug 修复一起完成（推荐，因为已经在修改相关代码）
- **方案B**: 先修复 Bug，称呼功能作为后续迭代

建议 **方案A**，因为：
1. 已经在修改 `build_context` 和 `render_email` 函数
2. 改动量很小，增加 5-10 分钟即可完成
3. 一次提交，避免多次 PR
