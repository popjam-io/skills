# Per-Asset Extraction Schema

Use this schema for every asset analyzed in Phase 2. Fill every field; use `"none"` / `"n/a"` explicitly rather than omitting — omissions are indistinguishable from oversights during synthesis.

Estimate hex values from what you see, but flag them as estimates; the programmatic palette (`palette.json`) is the final authority on exact values. Your unique contribution is *usage*: which color goes where, and why.

```json
{
  "file": "relative/path.jpg",
  "content_type": "product-ad | announcement | seasonal | coupon | category-collection | job-ad | testimonial | other",
  "campaign_hint": "named program/campaign if identifiable",
  "colors": {
    "background": {"hex_estimate": "#...", "treatment": "solid | gradient | photo | texture"},
    "dominant": ["#...", "#..."],
    "accent": ["#..."],
    "text_colors": {"headline": "#...", "body": "#...", "price_or_emphasis": "#..."},
    "usage_notes": "which color plays which role; combos that repeat"
  },
  "typography": {
    "headline": {"style": "geometry/weight/case description", "case": "all-caps | title | sentence", "name_hypothesis": "closest known font, clearly marked as guess"},
    "body": {"style": "...", "name_hypothesis": "..."},
    "hierarchy_levels": 3,
    "size_ratio_headline_to_body": "~2.5x",
    "alignment": "left | center | mixed",
    "special_treatments": "italics for emphasis words, outlined text, 3D/bubble, etc."
  },
  "layout": {
    "grid": "e.g. two-zone vertical split, card grid, full-bleed hero",
    "reading_order": "ordered list, e.g. badge -> headline -> product -> price -> CTA",
    "focal_point": "what your eye lands on first and why",
    "density": "minimal | moderate | dense (estimate % canvas occupied)",
    "white_space": "generous | moderate | tight",
    "safe_zones": "fixed header/footer bands, legal text placement"
  },
  "graphic_elements": {
    "shapes": "recurring motifs: waves, blobs, pills, polaroid frames...",
    "badges": [{"text": "verbatim", "style": "shape/color", "role": "program | offer | trust | urgency"}],
    "icons_style": "line | filled | none",
    "decorative": "patterns, props, textures"
  },
  "imagery": {
    "product_presentation": "cutout | lifestyle | packshot | podium | none",
    "product_count": 0,
    "human_presence": "none | model | hands | crowd; treatment notes",
    "image_treatment": "full color | overlay | duotone",
    "brand_logos_shown": ["third-party brand logos visible"]
  },
  "brand_elements": {
    "logo": {"variant": "description", "placement": "e.g. top-center header band", "size_relative": "small | medium | dominant"},
    "recurring_partner_badges": "BNPL, payment, warranty marks",
    "app_or_url_reference": "verbatim if present"
  },
  "copy": {
    "headline_verbatim": "...",
    "subhead_verbatim": "...",
    "cta_verbatim": "...",
    "legal_or_fineprint": "...",
    "offer_framing": "percentage | absolute | starting-price | threshold | coupon-code | none",
    "urgency_device": "verbatim phrase or none",
    "language": "tr | en | ...",
    "emoji_usage": "none | moderate | heavy"
  },
  "video_arc": "for video frames only: hook (10%) -> hold (50%) -> endcard (90%) description, else n/a",
  "rule_breaks": "anything that deviates from the corpus's apparent system: seasonal override, co-brand takeover, different pipeline",
  "production_quality": "polished | template | rough",
  "confidence_notes": "anything you were unsure about"
}
```

## Why these fields

`reading_order` (not just element lists) is what a generation pipeline needs to reproduce hierarchy. `offer_framing` and `urgency_device` are split out because offer mechanics often correlate with performance and differ by sub-system. `rule_breaks` is how Phase 3 discovers sub-systems instead of averaging them away. Verbatim copy transcription powers the tone-of-voice section — paraphrases destroy the evidence.
