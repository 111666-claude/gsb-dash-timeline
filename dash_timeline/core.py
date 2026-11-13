from __future__ import annotations

import math


def expand_timeline(spec: dict) -> dict:
    timescale = int(spec.get("timescale", 1) or 1)
    offset = int(spec.get("presentation_time_offset", 0) or 0)
    period_start = int(spec.get("period_start_ms", 0) or 0)
    items = spec.get("segments", []) or []

    # One reverse pass: nearest explicit t after each entry. r=-1 must stop at
    # the next explicit time even when period_end_ms is absent. Work stays
    # linear in the number of Timeline entries (no per-segment history rescan).
    next_explicit = [None] * len(items)
    pending = None
    for index in range(len(items) - 1, -1, -1):
        next_explicit[index] = pending
        if "t" in items[index] and items[index]["t"] is not None:
            pending = int(items[index]["t"])

    period_end = spec.get("period_end_ms")
    # Media time corresponding to the Period end, in the entry time base.
    period_end_media = None
    if period_end is not None:
        period_end_media = offset + (int(period_end) - period_start) * timescale // 1000

    def to_presentation_ms(media_time: int) -> int:
        # Media time base is untouched by the offset; only presentation time
        # is shifted. Floored division keeps presentation time monotone even
        # for negative (media - offset) values.
        return period_start + (media_time - offset) * 1000 // timescale

    segments = []
    cursor = None
    for index, item in enumerate(items):
        start = int(item["t"]) if item.get("t") is not None else (
            cursor if cursor is not None else 0
        )
        duration = int(item["d"])
        repeat = int(item.get("r", 0) or 0)

        if repeat < 0:
            boundary = next_explicit[index]
            if boundary is not None:
                # Explicit next start: floor so the last repeated segment ends
                # at or before it; any remaining gap is preserved.
                repeat = max(0, (boundary - start) // duration) - 1
            elif period_end_media is not None:
                # Period end: ceil so the final in-progress live segment is not
                # dropped; an entry already at/past the edge yields nothing.
                repeat = math.ceil((period_end_media - start) / duration) - 1
                repeat = max(-1, repeat)
            else:
                # No boundary known: emit just the declared segment, never loop.
                repeat = 0

        for occurrence in range(repeat + 1):
            media_start = start + occurrence * duration
            media_end = media_start + duration
            start_ms = to_presentation_ms(media_start)
            end_ms = to_presentation_ms(media_end)
            segments.append({
                "number": len(segments) + 1,
                "start_ms": start_ms,
                "duration_ms": end_ms - start_ms,
                "end_ms": end_ms,
            })
        cursor = start + (repeat + 1) * duration

    return {"segments": segments, "scanned": len(items)}
