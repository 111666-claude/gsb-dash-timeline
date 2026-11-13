import argparse
import json

from .core import expand_timeline


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--sample", default="live")
    args = parser.parse_args()
    if args.sample == "live":
        spec = {"timescale": 90000, "presentation_time_offset": 9000, "period_start_ms": 5000, "period_end_ms": 14000, "segments": [{"t": 9000, "d": 180000, "r": 2}, {"d": 135000, "r": -1}]}
    elif args.sample == "splice":
        spec = {"timescale": 1000, "period_start_ms": 12000, "segments": [{"t": 1000, "d": 1500}, {"d": 1500, "r": 1}]}
    else:
        raise SystemExit("unknown sample")
    print(json.dumps(expand_timeline(spec), separators=(",", ":")))


if __name__ == "__main__":
    main()
