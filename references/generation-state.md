# 生成状态

使用 `generation-state.json` 记录长 PPT 逐页生成进度，方便中断后自动续跑。

```json
{
  "deck_title": "PPT 标题",
  "total_slides": 12,
  "slides_dir": "slides",
  "completed": [1, 2, 3],
  "failed": [],
  "next_slide": 4,
  "last_updated": "2026-05-07T10:00:00+08:00"
}
```

续跑规则：

- 续跑前检查图片目录。
- 已存在且非空的 `slide-###.png` 视为已完成。
- 从第一张缺失图片开始继续生成。
- 每生成成功一页后立刻更新状态文件。
- 如果用户没有发出新指令，生成中断后自动继续剩余页面。
