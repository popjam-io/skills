#!/usr/bin/env python3
"""Safe-zone validator for ad creatives.

Checks an image against platform keep-clear zones (Meta Stories/Reels, TikTok
In-Feed, Google/landscape crop margins) and optionally renders an overlay proof
(red = danger zones, green outline = live area).

Two checking modes:
  1. Heuristic (default): detects "content" as saturated-or-dark foreground and
     reports its bounding box vs the live area. Fast, zero-config, but cannot
     distinguish deliberate full-bleed background art from critical elements —
     treat a heuristic FAIL as "look at the overlay", not as final truth.
  2. Exact (--boxes): pass the bounding boxes of critical elements (text, logo,
     price, CTA); each box is checked precisely. Use this in generation
     pipelines where element positions are known.

Zones are stored as fractions of the canvas, so any resolution works.

Usage:
    python check_safe_zones.py IMAGE [--platform meta|tiktok|union|auto]
                               [--boxes "x1,y1,x2,y2;x1,y1,x2,y2;..."]
                               [--overlay OUT.png] [--json] [--quiet]

Exit codes: 0 = pass, 1 = violations found, 2 = usage/input error.

Requires Pillow (pip install pillow).
"""
import argparse
import json
import sys

from PIL import Image, ImageDraw

# Keep-clear zones as fractions of (width, height): top, bottom, left, right.
# Sources: Meta Ads Guide (official, 2025-26: 14% top / 35% bottom / 6% sides,
# unified Stories+Reels); TikTok figures derived from TikTok's own safe-zone
# templates for 1080x1920 (130 / 484 / 44 / 140 px) — community consensus.
VERTICAL_ZONES = {
    "meta": {"top": 0.14, "bottom": 0.35, "left": 0.06, "right": 0.06},
    "tiktok": {"top": 130 / 1920, "bottom": 484 / 1920, "left": 44 / 1080, "right": 140 / 1080},
}
VERTICAL_ZONES["union"] = {
    k: max(VERTICAL_ZONES["meta"][k], VERTICAL_ZONES["tiktok"][k])
    for k in ("top", "bottom", "left", "right")
}

# Overlay-free formats: advisory craft margins only (fractions of canvas).
ADVISORY_MARGINS = {
    "square": {"top": 70 / 1080, "bottom": 70 / 1080, "left": 70 / 1080, "right": 70 / 1080},
    "portrait_4_5": {"top": 90 / 1800, "bottom": 90 / 1800, "left": 90 / 1440, "right": 90 / 1440},
    "landscape": {"top": 60 / 628, "bottom": 60 / 628, "left": 120 / 1200, "right": 120 / 1200},
}


def classify_format(w, h):
    r = w / h
    if r <= 0.65:
        return "vertical_9_16"
    if r <= 0.9:
        return "portrait_4_5"
    if r <= 1.1:
        return "square"
    return "landscape"


def zones_for(fmt, platform):
    if fmt == "vertical_9_16":
        return VERTICAL_ZONES[platform if platform != "auto" else "union"], False
    return ADVISORY_MARGINS[fmt], True


def live_area(w, h, z):
    return (round(w * z["left"]), round(h * z["top"]),
            round(w * (1 - z["right"])), round(h * (1 - z["bottom"])))


def detect_content_bbox(img, sat_thresh=60, dark_thresh=90, row_frac=0.04):
    """Bounding box of saturated-or-dark foreground, in original pixels."""
    small = img.convert("RGB").resize((min(img.width, 216), min(img.height, 384)))
    sw, sh = small.size
    px = small.load()
    fg_rows, fg_cols = [0] * sh, [0] * sw
    for y in range(sh):
        for x in range(sw):
            r, g, b = px[x, y]
            mx, mn = max(r, g, b), min(r, g, b)
            if (mx - mn) > sat_thresh or mx < dark_thresh:
                fg_rows[y] += 1
                fg_cols[x] += 1
    rows = [y for y in range(sh) if fg_rows[y] >= sw * row_frac]
    cols = [x for x in range(sw) if fg_cols[x] >= sh * row_frac]
    if not rows or not cols:
        return None
    fx, fy = img.width / sw, img.height / sh
    return (round(cols[0] * fx), round(rows[0] * fy),
            round((cols[-1] + 1) * fx), round((rows[-1] + 1) * fy))


def box_violations(box, live, label):
    x1, y1, x2, y2 = box
    lx1, ly1, lx2, ly2 = live
    out = []
    if y1 < ly1:
        out.append({"box": label, "edge": "top", "px_into_zone": ly1 - y1,
                    "fix": f"move down so top edge >= y={ly1}"})
    if y2 > ly2:
        out.append({"box": label, "edge": "bottom", "px_into_zone": y2 - ly2,
                    "fix": f"move up so bottom edge <= y={ly2}"})
    if x1 < lx1:
        out.append({"box": label, "edge": "left", "px_into_zone": lx1 - x1,
                    "fix": f"move right so left edge >= x={lx1}"})
    if x2 > lx2:
        out.append({"box": label, "edge": "right", "px_into_zone": x2 - lx2,
                    "fix": f"move left so right edge <= x={lx2}"})
    return out


def render_overlay(img, live, out_path):
    base = img.convert("RGBA")
    layer = Image.new("RGBA", base.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    w, h = base.size
    lx1, ly1, lx2, ly2 = live
    red = (230, 30, 30, 90)
    for box in [(0, 0, w, ly1), (0, ly2, w, h), (0, ly1, lx1, ly2), (lx2, ly1, w, ly2)]:
        d.rectangle(box, fill=red)
    d.rectangle(live, outline=(0, 200, 80, 255), width=max(2, w // 300))
    Image.alpha_composite(base, layer).convert("RGB").save(out_path)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("image")
    ap.add_argument("--platform", choices=["meta", "tiktok", "union", "auto"], default="auto",
                    help="Zone set for 9:16 canvases (default: union of Meta+TikTok)")
    ap.add_argument("--boxes", help='Exact element boxes: "x1,y1,x2,y2;..." (skips heuristic)')
    ap.add_argument("--overlay", metavar="OUT.png", help="Write an overlay proof image")
    ap.add_argument("--json", action="store_true", help="Machine-readable output")
    ap.add_argument("--quiet", action="store_true")
    args = ap.parse_args()

    try:
        img = Image.open(args.image)
    except Exception as e:
        print(f"error: cannot open {args.image}: {e}", file=sys.stderr)
        return 2

    w, h = img.size
    fmt = classify_format(w, h)
    zones, advisory = zones_for(fmt, args.platform)
    live = live_area(w, h, zones)

    violations, mode = [], "heuristic"
    if args.boxes:
        mode = "exact"
        try:
            for i, part in enumerate(x for x in args.boxes.split(";") if x.strip()):
                box = tuple(int(v) for v in part.split(","))
                if len(box) != 4:
                    raise ValueError(part)
                violations += box_violations(box, live, f"box{i + 1}")
        except ValueError as e:
            print(f"error: bad --boxes segment: {e}", file=sys.stderr)
            return 2
        content_bbox = None
    else:
        content_bbox = detect_content_bbox(img)
        if content_bbox:
            violations = box_violations(content_bbox, live, "content")

    if args.overlay:
        render_overlay(img, live, args.overlay)

    result = {
        "image": args.image, "size": [w, h], "format": fmt,
        "platform_zones": args.platform if fmt == "vertical_9_16" else "craft-margin (no UI overlay)",
        "advisory_only": advisory, "live_area": list(live), "mode": mode,
        "content_bbox": list(content_bbox) if content_bbox else None,
        "violations": violations,
        "pass": not violations,
    }
    if args.json:
        print(json.dumps(result, indent=1))
    elif not args.quiet:
        kind = "ADVISORY margins (no platform UI overlays this format)" if advisory \
            else f"platform '{args.platform}' keep-clear zones"
        print(f"{args.image}: {w}x{h} [{fmt}] vs {kind}")
        print(f"  live area: x {live[0]}-{live[2]}, y {live[1]}-{live[3]}")
        if content_bbox:
            print(f"  detected content bbox: {content_bbox}  (heuristic — check overlay for false bleed)")
        if violations:
            for v in violations:
                print(f"  VIOLATION [{v['box']}] {v['edge']}: {v['px_into_zone']}px into zone — {v['fix']}")
        else:
            print("  PASS — no critical content in keep-clear zones" if not advisory
                  else "  PASS — inside advisory margins")
        if args.overlay:
            print(f"  overlay proof: {args.overlay}")

    if advisory and violations and mode == "heuristic":
        return 0  # advisory formats: heuristic hits are informational, don't fail pipelines
    return 1 if violations else 0


if __name__ == "__main__":
    sys.exit(main())
