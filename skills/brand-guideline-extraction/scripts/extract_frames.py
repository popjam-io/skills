#!/usr/bin/env python3
"""Extract representative frames from videos for vision analysis.

Pulls 3 frames per video (10%, 50%, 90% of duration): hook, layout hold, endcard.
Requires ffmpeg/ffprobe on PATH.

Usage:
    python extract_frames.py <input_dir> -o <output_dir> [--pcts 10 50 90]
"""
import argparse
import re
import subprocess
import sys
from pathlib import Path

VIDEO_EXTS = {".mp4", ".mov", ".webm", ".mkv", ".avi", ".m4v"}


def duration_of(path: Path) -> float:
    try:
        out = subprocess.run(
            ["ffprobe", "-v", "error", "-show_entries", "format=duration",
             "-of", "csv=p=0", str(path)],
            capture_output=True, text=True, timeout=30,
        ).stdout.strip()
        return float(out)
    except Exception:
        return 2.0  # fallback: short clip assumption


def safe_name(path: Path, root: Path) -> str:
    rel = str(path.relative_to(root).with_suffix(""))
    return re.sub(r"[^\w.+-]+", "_", rel).strip("_")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("input_dir")
    ap.add_argument("-o", "--output-dir", required=True)
    ap.add_argument("--pcts", nargs="*", type=int, default=[10, 50, 90])
    args = ap.parse_args()

    root, out = Path(args.input_dir), Path(args.output_dir)
    out.mkdir(parents=True, exist_ok=True)

    videos = [p for p in root.rglob("*") if p.suffix.lower() in VIDEO_EXTS]
    if not videos:
        print("No videos found.")
        return

    ok = fail = 0
    for v in videos:
        dur = duration_of(v)
        base = safe_name(v, root)
        for pct in args.pcts:
            t = max(0.1, dur * pct / 100.0)
            dest = out / f"{base}__{pct}.jpg"
            if dest.exists():
                continue
            r = subprocess.run(
                ["ffmpeg", "-loglevel", "error", "-ss", f"{t:.2f}", "-i", str(v),
                 "-frames:v", "1", "-q:v", "4", str(dest), "-y"],
                capture_output=True, timeout=60, stdin=subprocess.DEVNULL,
            )
            if r.returncode == 0 and dest.exists():
                ok += 1
            else:
                fail += 1
                print(f"  FAILED: {v.name} @{pct}%", file=sys.stderr)
    print(f"Extracted {ok} frames from {len(videos)} videos ({fail} failures) -> {out}")


if __name__ == "__main__":
    main()
