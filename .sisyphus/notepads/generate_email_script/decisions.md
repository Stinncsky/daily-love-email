# Decisions
- 采用现有模块进行数据聚合和模板渲染，确保无需修改现有代码。
- CLI 设计：-c/--config 指定配置，-o/--output 指定输出目录，--open 可选打开浏览器。
- 输出文件命名采用 email_YYYYMMDD_HHMMSS.html，确保唯一性。
- 生成流程日志包含：配置加载、恋爱天数、模板与背景信息、输出路径。
