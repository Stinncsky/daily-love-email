# 文档修复计划

## 问题描述
用户发现两个文档的配置说明存在问题：
1. 没有明确区分**本地使用**和**GitHub Actions**两种配置方式
2. GitHub Actions 的配置内容不完整

## 需要修复的文件

### 1. .github/secrets_template.md

**当前问题**：
- 只说明了 GitHub Actions 配置，没有对比本地配置
- Secrets 列表不完整（缺少纪念日、城市等）
- 没有说明如何手动触发测试
- 没有定时任务配置说明

**修复内容**：
- 添加"配置方式对比"表格，明确区分本地和 Actions
- 完整的 Secrets 列表（核心配置 + 个性化配置 + 可选配置）
- 详细的 QQ 邮箱授权码获取步骤
- 详细的 OpenWeatherMap API Key 获取步骤
- 手动触发测试的方法
- 定时发送时间修改说明（含常用 cron 表达式）
- 故障排查指南

### 2. README.md

**当前问题**：
- "安装与配置"章节混乱，混合了两种方式
- 让用户困惑：到底该改 config.yaml 还是 Secrets？

**修复内容**：
- 重新组织"安装与配置"章节，分为两个独立的方案：
  - 方案 A：本地使用（config.yaml）
  - 方案 B：GitHub Actions（Secrets）
- 明确说明两种方式的区别和选择建议
- 删除过时的".env 文件"配置说明（项目已改用 config.yaml）

## 执行步骤

### Step 1: 重写 secrets_template.md
- 创建新的配置指南结构
- 包含完整的 Secrets 列表和说明
- 添加测试和故障排查章节

### Step 2: 重写 README.md 的配置章节
- 将"安装与配置"分为两个独立方案
- 方案 A：本地运行（使用 config.yaml）
- 方案 B：GitHub Actions（使用 Secrets）
- 让用户根据使用场景选择

### Step 3: 提交更改
- 提交信息：docs: 重构配置文档，明确区分本地和 Actions 配置方式

## 文件变更

- `.github/secrets_template.md` - 完全重写
- `README.md` - 重写"安装与配置"章节

## 验证标准

- [ ] secrets_template.md 包含完整的 Secrets 列表
- [ ] secrets_template.md 说明如何手动触发测试
- [ ] secrets_template.md 包含定时任务修改方法
- [ ] README.md 明确区分本地和 Actions 两种方案
- [ ] 用户能清晰知道该选择哪种配置方式
