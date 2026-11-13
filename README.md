# dash-timeline

展开游戏视频 MPEG-DASH 的 SegmentTimeline，供点播跳转和直播追赶使用，只用 Python 标准库。

## 口径

- timescale、presentation time offset、Period 起点和显式时间共同决定展示时间。
- `r=-1` 要扩展到下一段显式起点或 Period 结束，不能制造无限段。
- 跨 Period 时保留绝对展示时间；相邻段的边界按时间基换算后保持一致。
- 返回 `scanned`，工作量随 Timeline 条目数增长，不逐段回扫前面的条目。

## 不变量

- 段编号连续，时长为正。
- 同一 Period 内段起点单调不减。
- presentation time offset 只影响展示时间，不改变媒体时间基。

## 输出契约

CLI 输出 JSON：`segments` 含 `number`、`start_ms`、`duration_ms`、`end_ms`；另有 `scanned`。
