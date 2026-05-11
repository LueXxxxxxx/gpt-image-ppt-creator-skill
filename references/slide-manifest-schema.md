# 幻灯片 Manifest 结构

当需要保存结构化大纲时，使用 `outline.json`。

```json
{
  "title": "PPT 标题",
  "language": "zh-CN",
  "aspect_ratio": "16:9",
  "selected_roles": ["cover", "agenda", "content", "closing"],
  "numbering_style": "01 02 03",
  "content_title_mode": "topic-only",
  "slides": [
    {
      "number": 1,
      "role": "cover",
      "module": "",
      "main_title": "主标题",
      "subtitle": "可选副标题",
      "body": ["短要点"],
      "conclusion": "可选结论",
      "visual_intent": "描述这一页完整 PPT 图像的视觉构图",
      "density": "low",
      "highlight": false
    }
  ]
}
```

必须包含的 deck 字段：`title`、`slides`。

建议包含的 deck 字段：`language`、`aspect_ratio`、`selected_roles`、`numbering_style`、`content_title_mode`。

每页必须包含的字段：`number`、`role`、`main_title`、`visual_intent`。

`number` 只是内部排序、续跑和文件命名用的元数据，不代表页面中必须显示页码。封面页和尾页默认不得显示 `number` 或由它推导出的 `01`、`1` 等数字。

允许的 `role`：

- `cover`
- `agenda`
- `transition`
- `content`
- `summary`
- `closing`

推荐的 `density`：

- `cover`：`low`
- `agenda`：`medium-low`
- `transition`：`very-low`
- `content`：`high`
- `summary`：`medium`
- `closing`：`very-low`

纯图像 PPT 中，文字越多越容易出现小字和错字。生成最终图片前，应尽量压缩文字。

目录页默认不高亮任何单个目录项。只有用户或大纲明确标注某一项为重点、核心、主线或优先关注时，才在该目录项对应的数据中使用 `"highlight": true`，并在 prompt 中说明强调原因。

当 `selected_roles` 包含 `transition` 时，每个非空内容模块都应有对应的 `transition` 页。过渡页的 `module` 或 `main_title` 应与对应内容模块一致，例如内容模块为 `05 后期制作与发布优化` 时，应存在一页：

```json
{
  "role": "transition",
  "module": "05 后期制作与发布优化",
  "main_title": "05 后期制作与发布优化",
  "density": "very-low"
}
```

生成阶段应把第一张 `transition` 页作为过渡页母版。后续 `transition` 页只替换编号、标题、背景图像和少量装饰元素，不改变标题区布局、编号样式、标题字体和主视觉结构。

内容页标题层级有两种允许模式：

- 默认模式：`content_title_mode: "topic-only"`，`main_title` 使用不带模块序号的具体内容标题。
- 用户要求时的替代模式：`content_title_mode: "module-plus-topic"`，`main_title` 使用模块序号和模块标题，`subtitle` 使用具体内容标题。

当 `selected_roles` 包含 `transition` 且内容页的 `main_title` 与 `module` 完全相同时，该内容页必须提供非空 `subtitle` 或等价字段作为具体内容标题。否则通常表示这一页缺少内容主题，或把过渡页和内容页杂糅在一起。

生成大纲时默认写入 `"content_title_mode": "topic-only"`。只有用户明确要求内容页统一显示模块序号和模块标题时，才写入 `"module-plus-topic"`。

如需拆分，应拆为：

- 一页 `transition`：`main_title` 为模块标题。
- 一页 `content`：`main_title` 为该模块下的具体内容标题。
