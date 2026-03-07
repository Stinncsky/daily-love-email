# 简化版使用说明

这个版本使用 `romantic.html` 模板，配置更加简单直接。

## 快速开始

### 1. 配置图片 URL（环境变量）

在 GitHub Actions 中设置以下 Secrets：

| Secret 名称 | 说明 | 示例 |
|-------------|------|------|
| `BACKGROUND_IMAGE_URL` | 背景图片 URL | `https://cdn.jsdelivr.net/gh/user/repo@main/bg.jpg` |
| `ICON_URL` | 图标图片 URL | `https://cdn.jsdelivr.net/gh/user/repo@main/icon.png` |

**图片建议**：
- 使用 jsDelivr CDN（国内访问快）：`https://cdn.jsdelivr.net/gh/用户名/仓库名@分支/路径`
- 或使用其他图床

### 2. 必需的环境变量

```bash
EMAIL_SENDER=your_qq@qq.com
EMAIL_PASSWORD=your_auth_code
EMAIL_RECIPIENT=partner@example.com
LOVE_START_DATE=2023-01-01
CITY=Beijing
WEATHER_API_KEY=your_api_key
ANNIVERSARIES=[{"name":"恋爱纪念日","date":"01-01"}]
SENDER_NAME=亲爱的
RECIPIENT_NAME=宝贝

# 新增：图片 URL
BACKGROUND_IMAGE_URL=https://cdn.jsdelivr.net/gh/yourname/repo@main/assets/bg.jpg
ICON_URL=https://cdn.jsdelivr.net/gh/yourname/repo@main/assets/icon.png
```

### 3. 本地测试

```bash
# 设置环境变量
export BACKGROUND_IMAGE_URL="https://your-image-url/bg.jpg"
export ICON_URL="https://your-image-url/icon.png"

# 运行
python src/main.py --dry-run
```

### 4. 邮件效果

邮件将包含：
- 背景图片（来自 `BACKGROUND_IMAGE_URL`）
- 顶部图标（来自 `ICON_URL`）
- 恋爱天数统计
- 天气预报
- 每日情话

## 图片托管建议

### 方案 1：GitHub + jsDelivr（推荐）
1. 把图片上传到 GitHub 仓库
2. 获取 raw 链接：`https://raw.githubusercontent.com/用户名/仓库名/分支/路径`
3. 转换为 jsDelivr：`https://cdn.jsdelivr.net/gh/用户名/仓库名@分支/路径`

### 方案 2：使用图床
- 路过图床: `https://imgse.com`
- SM.MS: `https://sm.ms`
- 七牛云、阿里云 OSS 等

## 注意事项

- 背景图建议尺寸：1920x1080 或更大
- 图标建议尺寸：200x200 PNG
- 使用 HTTPS 链接
- 图片 URL 需要能被公开访问
