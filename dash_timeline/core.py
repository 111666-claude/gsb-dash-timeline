from __future__ import annotations

import math


def expand_timeline(spec: dict) -> dict:
    timescale = int(spec.get("timescale", 1) or 1)
    offset = int(spec.get("presentation_time_offset", 0) or 0)
    period_start = int(spec.get("period_start_ms", 0) or 0)
    segments = []
    current = None
    for item in spec.get("segments", []):
        start = int(item.get("t", current if current is not None else 0))
        duration = int(item["d"])
        repeat = int(item.get("r", 0))
        if repeat < 0:
            period_end = spec.get("period_end_ms")
            if period_end is None:
                repeat = 0
            else:
                target = offset + (int(period_end) - period_start) * timescale // 1000
                repeat = max(0, math.ceil((target - start) / duration) - 1)
        for index in range(repeat + 1):
            raw = start + index * duration
            start_ms = period_start + (raw - offset) * 1000 // timescale
            duration_ms = duration * 1000 // timescale
            segments.append({
                "number": len(segments) + 1,
                "start_ms": start_ms,
                "duration_ms": duration_ms,
                "end_ms": start_ms + duration_ms,
            })
        current = start + (repeat + 1) * duration
    return {"segments": segments, "scanned": len(spec.get("segments", []))}
