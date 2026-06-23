#!/usr/bin/env python3
"""Programmatic brand-palette extraction across an asset corpus.

Per image: downscale, quantize to N colors, record dominant colors with coverage.
Across corpus: cluster similar colors (RGB distance) and report recurrence —
how many images each color cluster appears in. Colors recurring across many
images are brand colors; one-offs are content.

Requires Pillow (pip install pillow --break-system-packages if missing).

Usage:
    python extract_palette.py <asset_dir> -o palette.json [--per-image 6] [--min-share 0.05]
"""
import argparse
import json
from collections import defaultdict
from pathlib import Path

from PIL import Image

IMG_EXTS = {".jpg", ".jpeg", ".png", ".webp", ".bmp", ".gif"}


def dominant_colors(path: Path, n: int, min_share: float):
    img = Image.open(path).convert("RGB")
    img.thumbnail((256, 256))
    q = img.quantize(colors=n, method=Image.Quantize.MEDIANCUT).convert("RGB")
    counts = defaultdict(int)
    for px in q.getdata():
        counts[px] += 1
    total = sum(counts.values())
    out = []
    for rgb, c in sorted(counts.items(), key=lambda kv: -kv[1]):
        share = c / total
        if share >= min_share:
            out.append({"hex": "#{:02X}{:02X}{:02X}".format(*rgb), "share": round(share, 3)})
    return out


def dist(a, b):
    return sum((x - y) ** 2 for x, y in zip(a, b)) ** 0.5


def hex_to_rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def cluster(corpus, threshold=40.0):
    """Greedy clustering of per-image colors across the corpus."""
    clusters = []  # [{rgb_sum, weight, files:set, samples:[hex]}]
    for entry in corpus:
        for col in entry["colors"]:
            rgb = hex_to_rgb(col["hex"])
            for cl in clusters:
                centroid = tuple(s / cl["weight"] for s in cl["rgb_sum"])
                if dist(rgb, centroid) < threshold:
                    cl["rgb_sum"] = tuple(s + r for s, r in zip(cl["rgb_sum"], rgb))
                    cl["weight"] += 1
                    cl["files"].add(entry["file"])
                    cl["samples"].append(col["hex"])
                    break
            else:
                clusters.append({"rgb_sum": rgb, "weight": 1,
                                 "files": {entry["file"]}, "samples": [col["hex"]]})
    return clusters


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("asset_dir")
    ap.add_argument("-o", "--output", required=True)
    ap.add_argument("--per-image", type=int, default=6)
    ap.add_argument("--min-share", type=float, default=0.05)
    args = ap.parse_args()

    root = Path(args.asset_dir)
    files = sorted(p for p in root.rglob("*") if p.suffix.lower() in IMG_EXTS)
    if not files:
        raise SystemExit("No images found under " + str(root))

    corpus = []
    for f in files:
        try:
            corpus.append({"file": str(f.relative_to(root)),
                           "colors": dominant_colors(f, args.per_image, args.min_share)})
        except Exception as e:
            print(f"  skip {f.name}: {e}")

    n_files = len(corpus)
    clusters = cluster(corpus)
    summary = []
    for cl in sorted(clusters, key=lambda c: -len(c["files"])):
        centroid = tuple(round(s / cl["weight"]) for s in cl["rgb_sum"])
        summary.append({
            "hex": "#{:02X}{:02X}{:02X}".format(*centroid),
            "recurrence": round(len(cl["files"]) / n_files, 3),
            "n_images": len(cl["files"]),
            "sample_hexes": cl["samples"][:5],
        })

    result = {"n_images": n_files,
              "corpus_palette": summary[:20],
              "per_image": corpus}
    Path(args.output).write_text(json.dumps(result, indent=2))
    print(f"Analyzed {n_files} images -> {args.output}")
    print("Top recurring colors (likely brand colors at recurrence >= 0.5):")
    for s in summary[:8]:
        print(f"  {s['hex']}  in {s['n_images']}/{n_files} images ({s['recurrence']:.0%})")


if __name__ == "__main__":
    main()
