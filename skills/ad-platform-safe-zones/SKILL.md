---
name: ad-platform-safe-zones
description: >-
  Current (2025–26, source-verified) safe-zone and canvas specs for ad creatives on Meta
  (FB/IG Feed, Stories, Reels), TikTok, and Google (Demand Gen, Responsive Display, Gmail),
  plus a bundled validator that checks finished images and renders overlay proofs. Use this
  whenever you generate, compose, resize, audit, or export ANY ad or social media creative —
  story/reels ads, feed images, banners, thumbnails, 9:16 / 4:5 / 1:1 / 1.91:1 canvases —
  even if the user never says "safe zone": platform UI covers large parts of the canvas and
  widely-known numbers are outdated (Meta's 9:16 bottom clear zone is now 35%, not the old
  20%/340px). Also use it when the user asks "will this get cropped/covered?", "what sizes
  do I need?", or wants an export set for a paid campaign.
---

# Ad Platform Safe Zones

Platform UI (profile chips, captions, CTA bars, action rails) is drawn ON TOP of ad creatives, and multi-placement delivery auto-crops assets. A creative that ignores this ships with its price, CTA, or logo hidden. This skill gives the current keep-clear numbers, the export-set logic, and a validator script — use them instead of remembered figures, because the most widely circulated numbers (Meta "250px top / 340px bottom") are obsolete: **Meta's current official 9:16 zone is top 14%, bottom 35%, sides 6%**.

## The numbers that matter (quick reference)

All pixel values below are for the stated canvas; the zones are percentages, so scale them for other resolutions.

| Canvas | Placement | Keep clear of text/logo/CTA | Live area |
|---|---|---|---|
| 1080×1920 (9:16) | Meta Stories + Reels (unified zone) | top 269 px (14%), bottom 672 px (35%), sides 65 px (6%) | x 65–1015, y 269–1248 |
| 1080×1920 (9:16) | TikTok In-Feed (template-derived) | top ~130, bottom ~484, left ~44, right ~140 px | x 44–940, y 130–1436 |
| 1080×1920 (9:16) | **Meta ∪ TikTok one-master** | strictest of each edge | **x 65–940, y 269–1248** |
| 1440×1800 (4:5) | Meta feed (current recommended feed ratio) | no UI overlay — ~80–100 px craft margin; keep critical elements in center square (1440×1440) so a 1:1 crop survives | — |
| 1080×1080 (1:1) | Feed/carousel/Marketplace/Google 1:1 | no UI overlay — ~60–80 px craft margin | — |
| 1200×628 (1.91:1) | FB link/right column; Google Demand Gen & Display | overlay-free; risk is AUTO-CROP toward 1:1 — keep content ≥120 px from left/right, ≥60 px from top/bottom | center ~80% |

Background art may bleed full-frame everywhere — only *readable/critical* elements (text, prices, logos, CTAs, product-critical details) must stay in the live area.

## Workflow A — generating or composing a creative

1. **Pick the canvas from the placement list**, not from habit. Meta feed's recommended master is now 4:5 (1440×1800), with 1:1 as a center-crop derivative. Vertical placements get a true 9:16 master — never let the platform auto-adapt a square into Stories/Reels.
2. **Lay out critical elements inside the live area** for every platform the asset will run on. For a 9:16 running Meta + TikTok that means x 65–940, y 269–1248. Put the logo near the top of the live band, price/CTA in the middle band, never in the bottom third — the bottom 35% will sit under caption + CTA + engagement UI.
3. **Validate before delivering.** Run the bundled checker on the finished file:
   ```bash
   python scripts/check_safe_zones.py OUT.png --platform union --overlay proof.png
   ```
   It auto-detects the format, reports violations with pixel numbers, and writes an overlay proof (red = danger zones, green = live area) you can view or send to the user. If the automatic content detection misfires (e.g., a deliberately full-bleed colorful background), pass explicit element boxes: `--boxes "x1,y1,x2,y2;..."` — those are checked exactly.
4. **Fix violations by moving elements, not by shrinking the whole design.** The design language usually allows sliding the content stack; scaling everything down wastes the live area and reads timid.

## Workflow B — auditing an existing creative

Run the checker first (it gives measured pixel extents), then read the overlay proof yourself to separate real violations (text/logo in a danger zone) from benign background bleed — the heuristic cannot tell those apart. Report: which elements sit in which zone, by how many px, and the minimal move that fixes each. Cite the current zone numbers so the user knows why older templates (built to 340 px bottoms) now fail.

## Workflow C — building a campaign export set

Ship every ratio natively so Advantage+/auto-placement never crops:

- **Meta:** 4:5 1440×1800 (feed) + 1:1 1440×1440 (Explore/Marketplace/carousel) + 9:16 1440×2560 or 1080×1920 (Stories/Reels) + 1.91:1 1200×628 (right column/link previews).
- **Google Demand Gen:** 1.91:1 1200×628 (min 600×314) + 1:1 1200×1200 + 4:5 960×1200 + 9:16 1080×1920; **logo 1200×1200 (min 128×128, ≤150 KB)** with the mark centered at ~60% width — Gmail masks the logo to a circle, cropping ~21% of the square.
- **Google Responsive Display:** 1.91:1 1200×628 + 1:1 1200×1200; logos 1:1 1200×1200 and 4:1 1200×300.
- Never bake letterbox bars or fake platform UI into an asset — Meta down-ranks or rejects simulated-UI creatives, and baked bars break auto-placement.

## Bundled resources

- `scripts/check_safe_zones.py` — validator + overlay renderer (Pillow only). `--json` for machine-readable output; exits non-zero on violations so it can gate a pipeline. Run with `--help` for all options.
- `references/safe-zones.md` — the full research: per-platform sections, exact spec tables, what each UI element covers, which figures are official vs community-consensus, and source URLs. Read it when the user asks about a placement not in the table above (in-stream video, profile-grid cropping, YouTube Shorts), disputes a number, or needs citations.

## Facts that prevent the most common mistakes

- Meta unified Stories and Reels into ONE zone: top 14% / bottom 35% / sides 6%. Anything built to the old 20% bottom line will have its lower third covered in Reels delivery.
- The Reels right-side action rail intrudes ~110–140 px in the lower half — keep prices/CTAs out of the bottom-right corner even inside the official side margin.
- TikTok's bottom zone (~25%) is *shallower* than Meta's, but its right rail (~140 px) is *deeper* than Meta's 6% — a one-master 9:16 must satisfy the union.
- 1:1 and 4:5 feed images get NO overlay — don't waste canvas on huge empty margins there; the risk profile is cropping (profile grid is 3:4, organic only), not UI.
- Verify in-platform before launch: Meta Ads Manager's safe-zone overlay and TikTok's downloadable templates are the ground truth for edge cases.
