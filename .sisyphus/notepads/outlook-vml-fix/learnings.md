# Outlook VML Compatibility Change: get_card_background_style()

- 修改目标: 在 src/background.py 的 get_card_background_style 函数中新增 for_vml: bool = False 参数，用于输出 Outlook VML 兼容的背景格式。
- 具体实现:
  - 当 background_type 为 image 且 for_vml 为 True 时，返回裸数据 URL（data:image/png;base64,...），不再包裹在 url() 之中。
  - 当 for_vml 为 False（默认值），保持原有行为，返回 url(data:image/png;base64,...)。
- docstring 更新: 增加 for_vml 参数的说明，以及示例展示以体现两种模式的差异。
- 兼容性考虑: 旧的调用方式不需要修改，未传入 for_vml 时默认为 False，向后兼容。
- 验证要点:
  - 调用 get_card_background_style("image", "card_bg") 应返回类似 "url(data:image/png;base64,...)" 的字符串。
  - 调用 get_card_background_style("image", "card_bg", for_vml=True) 应返回类似 "data:image/png;base64,..." 的裸 URL。

后续工作:
- 如需扩展到其他 Outlook 相关的兼容性场景，可在同一函数中增加更多条件分支。
