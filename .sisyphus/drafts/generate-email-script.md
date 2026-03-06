# 需求草稿：邮件生成脚本

## 用户需求
创建一个根据 config.yaml 生成邮件 HTML 的脚本，方便测试查看效果。

## 功能要求
1. 读取 config.yaml 配置
2. 生成完整的邮件 HTML 内容
3. 保存到 output/ 目录，文件名包含日期时间戳
4. 支持命令行参数：
   - `-c, --config`: 指定配置文件路径
   - `-o, --output`: 指定输出目录
   - `--open`: 生成后在浏览器中打开
5. 显示有用的日志信息

## 技术方案
- 创建 `scripts/generate_email.py`
- 复用现有模块：
  - `src.config.load_config()` - 加载配置
  - `src.calculator.calculate_days_together()` - 计算天数
  - `src.template.render_email()` - 渲染邮件
  - `src.quotes.get_random_quote()` - 获取情话
  - `src.weather.get_weather()` - 获取天气
  - `src.anniversary.get_next_anniversary()` - 获取纪念日

## 使用方法示例
```bash
# 基本用法
python scripts/generate_email.py

# 生成并打开浏览器
python scripts/generate_email.py --open

# 指定配置和输出目录
python scripts/generate_email.py -c myconfig.yaml -o ./emails
```

## 输出示例
```
[INFO] 已加载配置: config.yaml
[INFO] 已构建渲染上下文
       - 恋爱天数: 796 天
       - 收件人: 我滴娘子~
       - 模板: email_new
       - 背景类型: gradient
[INFO] 邮件渲染成功
[SUCCESS] 已生成: output/email_20240306_143052.html
[INFO] 已在浏览器中打开
```
