# Safe Zones & Creative Specs — Paid Social / Display (2025–2026)

Verified 2026-08-11 against official sources where noted:
Meta Ads Guide (facebook.com/business/ads-guide — live pages fetched directly), Google Ads Help
(support.google.com), TikTok Business Help Center (ads.tiktok.com/help). Items that could not be
confirmed on an official page are marked **unverified — community consensus**.

> **Important change vs. older guides:** Meta's widely-circulated Stories safe zone of
> "250 px top / 340 px bottom" (14% / 20%) is **outdated**. Meta's current official guidance,
> confirmed directly on the live Instagram Stories ads spec page, is **top ~14% / bottom ~35% /
> sides ~6%** — one unified safe zone for Stories and Reels. Design to the stricter 35% bottom.

---

## 1. Quick-reference master table

| Canvas | Placement | Keep clear (safe zone) | Pixel values on that canvas | Source |
|---|---|---|---|---|
| 1080×1920 (9:16) | Meta Stories + Reels (FB & IG) | Top 14%, bottom 35%, sides 6% | Top **269 px**, bottom **672 px**, sides **65 px** each | Meta Ads Guide (official, verified) |
| 1440×2560 (9:16) | Meta Stories + Reels — Meta's recommended render size | Same percentages | Top **358 px**, bottom **896 px**, sides **86 px** each | Meta Ads Guide (official, verified) |
| 1080×1920 (9:16) | TikTok In-Feed | Varies by caption length; use TikTok's downloadable templates | Top **~130 px**, bottom **~484 px**, left **~44 px**, right **~140 px** | TikTok Help (official = templates); px figures derived from templates — community consensus |
| 1080×1080 (1:1) | Meta feed (FB/IG) | No platform UI overlays the image — safe zone not required | Keep ~60–80 px internal padding as craft margin (rule of thumb, not a platform spec) | Meta Ads Guide (official) + community consensus |
| 1200×628 (1.91:1) | Meta feed link ads / right column; Google Demand Gen & Display | No UI overlay; risk is **cropping**, not overlay | Keep logo/text inside center ~80% (≈120 px in from left/right, ≈60 px top/bottom) — rule of thumb | Google Ads Help (sizes official); margin rule — community consensus |

---

## 2. Format 1 — 1080×1080 (1:1 square) · Instagram/Facebook feed

### Official spec status (Meta Ads Guide, verified 2026-08)
- **Meta's recommended feed asset is now 4:5, not 1:1.** Both the Facebook Feed and Instagram
  Feed image ad pages currently recommend **4:5 at 1440×1800 px** (JPG/PNG, max 30 MB).
- 1:1 is still **fully supported**: Instagram Feed supports ratios from 4:5 up to 1.91:1
  (tolerance ±1%), minimum width 500 px (IG) / 600 px (FB). A 1:1 image renders **uncropped and
  without letterboxing** in FB/IG feed — it simply occupies less vertical screen than 4:5.
- Text specs (IG feed): primary text ≤125 characters recommended, headline ≤40, max 30 hashtags.
  FB feed: primary text 50–150 characters, headline ~27.

### How feed UI interacts with the image
- In feed, Meta's UI sits **outside** the creative: page name + "Sponsored" above, primary text
  above the image, CTA bar and like/comment/share row below. **Nothing overlays a 1:1 or 4:5
  feed image**, so no mandatory safe zone exists inside the canvas.
- Practical craft margin: keep logos/text ≥60–80 px from the edges anyway — corners are slightly
  rounded in-app and some surfaces scale the image marginally. *(unverified — community consensus)*

### Cropping / reuse risks for 1:1
- **Instagram profile grid** now crops previews to **3:4** (organic surface; ads unaffected, but
  relevant if the same asset is posted organically). *(widely reported platform change;
  not on an ads-spec page — community consensus)*
- If no 9:16 asset is supplied, Advantage+ placements may auto-place the 1:1 into Stories/Reels
  (centered band with generated/blurred background, caption below) or auto-crop toward 4:5 in
  feed. Always supply the 9:16 separately rather than letting Meta adapt the square.
  *(behavior documented in Meta Advantage+ creative materials; exact rendering varies —
  community consensus)*

### Designer rule
Build feed creative on a **4:5 (1440×1800) master** and derive the 1:1 center crop from it,
not the other way round. Keep price tags, product and logo inside the shared center square so
both crops work.

---

## 3. Format 2 — 1080×1920 (9:16) · Stories & Reels (FB + IG)

### Official Meta safe zone (verified directly on Meta Ads Guide, 2026-08)
Meta's Instagram Stories ads page states: avoid placing key creative elements in
**~14% of the top**, **~35% of the bottom**, and **~6% of each side** of the asset.
Recommended render size on that page: **9:16 at 1440×2560 px** (MP4/MOV/GIF, ≤4 GB,
H.264 + AAC stereo ≥128 kbps, 1 s–60 min).

The same 14% / 35% / 6% figures apply to Facebook Stories, Facebook Reels and Instagram Reels —
Meta now publishes one unified vertical safe zone. (Stories page verified directly; Reels pages
consistently quoted with identical numbers by multiple 2026 spec trackers — treat as official.)

### Converted to pixels

| Canvas | Top clear | Bottom clear | Each side clear | Resulting "live" area |
|---|---|---|---|---|
| 1080×1920 | 269 px (14%) | 672 px (35%) | 65 px (6%) | **950 × 979 px** centered band, from y=269 to y=1248 |
| 1440×2560 | 358 px | 896 px | 86 px | 1268 × 1306 px band, from y=358 to y=1664 |

### What the UI covers
- **Top 14%:** profile photo, account name, "Sponsored" label, (Stories) progress bar.
- **Bottom 35%:** CTA button, primary text/caption, audio attribution, like/comment/share
  engagement stack. This is why the bottom zone is much deeper than the old 20% figure.
- **Right side (Reels):** the action rail (like/comment/share/save icons) hugs the right edge in
  roughly the **lower half** of the frame. Meta's official margin is only the 6% (65 px) side
  strip; in practice the icon stack intrudes about **110–140 px** into the right edge across the
  bottom ~40% of the frame — keep prices/CTAs out of that corner entirely.
  *(6% = official; the 110–140 px rail depth = unverified — community consensus)*

### Legacy numbers (do not use)
Top 250 px / bottom 340 px (14% / 20%) was Meta's pre-2025 Stories-only guidance. It still
circulates in older templates. The current bottom zone is **almost twice as deep** — creatives
built to the old 340 px line will have CTAs covered in Reels.

### Designer rule
On the 1080×1920 canvas, treat **x: 65–1015, y: 269–1248** as the only area where headline,
price , logo and CTA may live. Background/ambient imagery may bleed
full-frame. Put the logo in the top of the live band (below y=269), never in the bottom third.
Design once for Reels; anything that clears the Reels zone also clears Stories.

---

## 4. Format 3 — 1200×628 (1.91:1 landscape) · FB link ads / Google Demand Gen / Display

### Meta (Facebook link ads / right column)
- 1.91:1 remains **supported** in FB/IG feed (IG feed supported ratio range extends to 191:100 —
  verified on Meta Ads Guide), but Meta's recommendation for feed is now 4:5. Use 1.91:1 where
  it is native: **right column**, search results, and as the link-preview style asset.
- No platform UI overlays the 1.91:1 image; headline/description/CTA render below or beside it.
- Cropping risk: in Advantage+ / multi-placement delivery, a lone 1.91:1 asset can be
  auto-cropped toward 1:1 for feed surfaces — the outer ~25% of each horizontal side is what
  gets sacrificed. Supply 1:1 and 4:5 alongside it. *(unverified — community consensus)*

### Google Demand Gen (official — Google Ads Help, verified 2026-08)
Per "About image assets specifications and ad format guidelines for Demand Gen campaigns":

| Asset | Ratio | Minimum | Recommended | Max file |
|---|---|---|---|---|
| Landscape image | 1.91:1 | **600×314** | **1200×628** | 5 MB |
| Square image | 1:1 | 300×300 | 1200×1200 | 5 MB |
| Portrait image | 4:5 | 480×600 | 960×1200 | 5 MB |
| Vertical image | 9:16 | 600×1067 | 1080×1920 | 5 MB |
| Logo | 1:1 | **128×128** | **1200×1200** | 150 KB |

- Up to 20 image assets per ad.
- **Gmail logo cropping (official):** the logo is masked to a circle in Gmail — ~21.46% of the
  square is cropped (~5.36% at each corner). Keep the logo mark centered with generous padding;
  no text near corners of the logo file.
- For 9:16 images Google refers to its 9:16 video safe-zone standards (i.e., YouTube Shorts UI) —
  same principle as Meta: keep text/logo out of top and bottom bands.

### Google Display — Responsive Display Ads (official, verified 2026-08)
- Landscape image 1.91:1: recommended **1200×628**, minimum **600×314**, max 5120 KB.
- Square image: 1200×1200 rec / 300×300 min.
- Logos: square 1200×1200 rec / 128×128 min; landscape **4:1** logo 1200×300 rec / 512×128 min.
- The current help page contains **no explicit text-overlay percentage rule**. The old
  "text ≤20% of image" figure is retired/absent. Google's standing best practice is minimal or
  no overlaid text because RDA machine-crops images to fit slots. *(the ≤20% figure:
  unverified — community consensus / legacy)*

### Cropping behavior & margins for 1.91:1
- RDA and Demand Gen can render the landscape asset into differently-proportioned slots;
  centered composition survives, edges do not.
- Rule of thumb: keep all text, price and logo inside the **center 80%** of the 1200×628 canvas
  — i.e., ≥120 px in from left/right, ≥60 px from top/bottom — and never rely on edge content.
  *(unverified — community consensus)*

---

## 5. Meta: aspect-ratio coverage per placement (avoid auto-cropping)

Supply this asset set per campaign so no placement is auto-adapted:

| Ratio | Size | Used natively by |
|---|---|---|
| **4:5** | 1440×1800 | FB Feed, IG Feed (Meta's current recommended feed ratio — official, verified) |
| **1:1** | 1440×1440 | IG Search/Explore, FB Marketplace, carousels (carousel cards are 1:1), fallback square |
| **9:16** | 1440×2560 (or 1080×1920) | FB/IG Stories, FB/IG Reels, Audience Network native |
| **1.91:1** | 1200×628 | FB right column, link previews, some search surfaces; also reusable for Google |
| 16:9 | 1920×1080 | FB in-stream video (video campaigns only) |

Placement→ratio mapping beyond the feed/Stories pages is compiled from Meta's placements
documentation and current spec trackers; the 4:5 and 9:16 recommendations are verified official,
the per-surface mapping for right column/search/in-stream is **partially unverified — community
consensus** (Meta's "aspect ratios across placements" help article exists but is JS-gated).

Meta explicitly steers advertisers to **taller ratios (4:5, 9:16)**; square-only campaigns leave
screen real estate unused in feed and get adapted (cropped/extended) in vertical placements.

---

## 6. TikTok 9:16 safe zone (brief)

- **Official position (TikTok Business Help Center, verified 2026-08):** TikTok does not publish
  fixed pixel values in the help text. The safe zone "is determined by the dimension, ad caption
  length, and any additional formats used", and TikTok provides **downloadable safe-zone template
  files** (standard LTR + Arabic RTL versions) in the "TikTok Auction In-Feed Ads" help article.
  In-feed spec: 9:16 vertical recommended, ≥540×960 px; advertiser profile image: keep the key
  element within the center 66×66 px of the 98×98 px file.
- **Working numbers for a 1080×1920 canvas** (derived from TikTok's own templates, echoed by all
  major 2025–26 spec guides — **unverified against the current template — community consensus**):
  - Top clear: **~130 px** (tabs/search area)
  - Bottom clear: **~484 px** (caption, music, account name, CTA)
  - Left clear: **~44 px**
  - Right clear: **~140 px** (like/comment/share/profile stack)
  - Live area ≈ **896 × 1306 px**, offset toward the upper-left.
- Note the TikTok bottom zone (~25%) is shallower than Meta's 35%, but the right rail is much
  deeper than Meta's 6%. A creative built to the union of both zones (bottom 35%, right 140 px,
  top 269 px, left 65 px) runs safely on Meta **and** TikTok from one master.

---

## 7. Rules of thumb for designers

1. **One vertical master, strictest zone wins.** Design 9:16 at 1080×1920 with all copy, prices,
   logo, CTA inside **x: 65–940, y: 269–1248** (Meta 14/35/6 ∪ TikTok right rail). That single
   file clears IG/FB Stories, Reels and TikTok.
2. **Feed master is 4:5, square is a crop.** Compose at 1440×1800 with critical elements in the
   center 1440×1440; export 1:1 from the same file.
3. **Never letterbox manually.** Don't bake black/white bars or fake UI into any asset — Meta
   rejects or down-ranks creatives that simulate platform UI, and baked bars break auto-placement.
4. **Logo discipline:** logo in the top of the live band on vertical formats (just below the 14%
   line); on 1.91:1 keep it ≥120 px from edges; deliver a separate 1200×1200 logo file with the
   mark centered at ~60% of canvas width so Gmail's circular mask never clips it.
5. **Bottom third of vertical = background only.** Price bubbles  must sit
   in the middle band — the bottom 672 px will be covered by caption + CTA + engagement UI.
6. **Ship the full ratio set** (4:5, 1:1, 9:16, 1.91:1) on every Meta campaign so Advantage+
   never auto-crops; on Google Demand Gen ship 1.91:1 + 1:1 + 4:5 (+9:16 for Shorts) at the
   recommended sizes above.
7. **Check before launch:** Meta Ads Manager's safe-zone overlay ("Safe Zone Guardrail") on every
   vertical creative; TikTok's downloadable template overlaid in Figma/Photoshop.

---

## 8. Sources

**Official (fetched directly, 2026-08-11):**
- Meta Ads Guide — Instagram Stories ads (9:16, 1440×2560; top 14% / bottom 35% / sides 6%):
  facebook.com/business/ads-guide/video/instagram-story
- Meta Ads Guide — Instagram Feed image ads (4:5, 1440×1800; ratios to 191:100; min width 500):
  facebook.com/business/ads-guide/image/instagram-feed
- Meta Ads Guide — Facebook Feed image ads (4:5, 1440×1800; min width 600):
  facebook.com/business/ads-guide/image/facebook-feed
- Google Ads Help — Demand Gen image asset specs (1.91:1 1200×628/600×314; logo 1200×1200/128×128;
  Gmail circular crop ~21.46%): support.google.com/google-ads/answer/17140672
- Google Ads Help — Responsive display ads asset specs (1.91:1 1200×628/600×314; logos 1:1 and 4:1):
  support.google.com/google-ads/answer/7005917
- TikTok Business Help Center — Auction In-Feed Ads (safe-zone template downloads; ≥540×960 9:16;
  caption-length dependency): ads.tiktok.com/help/article/tiktok-auction-in-feed-ads

**Secondary (cross-checks; used only for community-consensus items):**
- adnabu.com, billo.app, lucidmedia.co.nz, solidlabs.com, adsuploader.com — Meta unified safe
  zone pixel conversions and Reels rail depth
- zeely.ai, adrate.io, recharm.com, houseofmarketers.com — TikTok 130/484/44/140 px template
  figures
