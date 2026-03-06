Task: 修改 email_new.html 主容器背景变量化

Change:
- 将 templates/email_new.html 中 class="container" 的 table 的 background 值从固定 rgba(255, 255, 255, 0.6) 改为使用变量:
  background: {{ card_background_style|default('rgba(255, 255, 255, 0.6)') }};
- 保持其他样式不变（backdrop-filter、border-radius、box-shadow 等）并确保向后兼容性通过 default 过滤器实现。

Verification:
- 打开模板，确认背景属性为变量表达式，且默认值为 rgba(255, 255, 255, 0.6)。
- 渲染模板时若未提供 card_background_style，则应输出默认颜色值。
