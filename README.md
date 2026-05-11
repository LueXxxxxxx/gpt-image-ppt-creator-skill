# GPT Image PPT Creator

[中文](#中文) | [English](#english)

## 中文

GPT Image PPT Creator 是一个用于 Codex 的纯图像 PPT 生成 Skill。它面向“每页 PPT 都是一张完整图片”的工作流，帮助 Codex 从创意或大纲开始，完成页面定位确认、大纲规划、风格确认、逐页图片生成、过渡页母版一致性控制、中断续跑，以及最终 `.pptx` 打包。

### 核心能力

- 在生成大纲前，先确认需要哪些页面定位类型。
- 支持封面页、目录页、过渡页/章节页、内容页、总结页、尾页/结束页。
- 将用户创意或初始大纲整理为结构化 `outline.json`。
- 在正式逐页生成前，先生成风格确认页供用户确认。
- 使用第一张已确认过渡页作为过渡页母版，后续过渡页只替换编号、标题、背景和少量装饰元素。
- 支持长 PPT 生成过程中的中断续跑。
- 将 `slides/` 中的整页图片打包成 PowerPoint 文件。

### 使用方式

在 Codex 中调用该 Skill，并提供主题、创意、简报或已有大纲。例如：

```text
请使用 GPT Image PPT Creator，基于“AI 漫剧创作培训”生成一份纯图像 PPT。先确认页面定位类型，再生成大纲。
```

### 打包 PPT

如需将已生成的图片打包为 PPTX，先安装依赖：

```bash
python -m pip install -r scripts/requirements.txt
```

然后执行：

```bash
python scripts/images_to_pptx.py --images slides --output deck.pptx
```

脚本会将 `slides/` 目录中的图片按文件名排序，并将每张图片铺满一页 16:9 PowerPoint 页面。

### 注意事项

- 本 Skill 默认生成不可编辑的纯图像 PPT。
- `slides/` 是最终打包 PPT 的默认图片来源。
- 不会默认创建 `slides-final/` 或对 GPT Image 生成结果进行本地二次重绘。
- 如果发现某页图片不符合预期，应重新用 GPT Image 生成该页，而不是用本地脚本重画。

## English

GPT Image PPT Creator is a Codex skill for creating image-only PowerPoint decks. It is designed for workflows where every slide is a single full-slide image. The skill guides Codex from an idea or outline through slide-role confirmation, outline planning, visual style confirmation, slide-by-slide image generation, transition-slide master-template consistency, interruption recovery, and final `.pptx` packaging.

### Features

- Confirm required slide roles before drafting the outline.
- Support cover, agenda, transition/section, content, summary, and closing slides.
- Convert a user idea or rough outline into a structured `outline.json`.
- Generate a style confirmation sheet before final slide generation.
- Use the first accepted transition slide as the master template, so later transition slides only change the section number, title, background, and minor decorative elements.
- Resume long generation runs from missing slide images.
- Package full-slide images from `slides/` into a PowerPoint deck.

### Usage

Invoke the skill in Codex and provide a topic, brief, or existing outline. For example:

```text
Use GPT Image PPT Creator to create an image-only PPT about AI manga drama production. First confirm the slide roles, then draft the outline.
```

### PPTX Packaging

Install the packaging dependency when needed:

```bash
python -m pip install -r scripts/requirements.txt
```

Then run:

```bash
python scripts/images_to_pptx.py --images slides --output deck.pptx
```

The script sorts images in `slides/` by filename and places each image full-bleed on one 16:9 PowerPoint slide.

### Notes

- This skill creates non-editable, image-only PowerPoint decks by default.
- `slides/` is the default source directory for final PPTX packaging.
- The workflow does not create `slides-final/` or locally redraw GPT Image outputs by default.
- If a slide image is not acceptable, regenerate that slide with GPT Image instead of redrawing it locally.

## License

MIT
