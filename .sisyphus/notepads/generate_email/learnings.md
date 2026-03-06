# Learnings from generate_email task
- 使用 src.config.load_config 优先，以保持配置加载的一致性。
- 兜底使用 PyYAML safe_load，避免在缺少自定义加载器时无法读取 YAML 配置。
- 数据生成采用确定性策略：恋爱天数、天气、情话等，通过日期和城市名的种子实现重复性测试。
- 优先调用 src.template 的渲染能力；若不可用，则回退到简易 HTML 模板，确保稳定产出。
- 命令行接口设计为便于测试：--config/-c、--output/-o、--open，输出文件名包含时间戳，便于测试对比。
- 生成路径输出为 output/email_YYYYMMDD_HHMMSS.html，便于回溯和自动化验证。
