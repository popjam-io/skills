---
name: brand-guideline-extraction
description: Reverse-engineer a comprehensive brand style guide from a corpus of existing design assets (social posts, ad creatives, banners, decks, videos). Produces a structured guideline document plus a reusable "style prompt block" for on-brand AI image generation. Use this whenever the user wants brand guidelines, a style guide, design-language or "look and feel" analysis, brand DNA extraction, visual identity documentation, or wants AI-generated images to match an existing brand — even if they just say "analyze our creatives" or "make generations on-brand" and point at a folder of images.
license: MIT
metadata:
  author: POPJAM (https://popjam.io)
---

# Brand Guideline Extraction

Reverse-engineer a brand's visual and verbal DNA from existing design assets, and codify it so a human designer or a generative pipeline can reproduce the look and feel.

The core insight: a brand guideline extracted from N assets is only as good as (a) how representative the corpus is, and (b) how rigorously you separate *rules* (what the brand always does) from *variations* (what it sometimes does) and *exceptions* (one-offs). The whole workflow is built around that separation.

Work through five phases in order. Phases 2's subagent fan-out is the expensive step; everything else is cheap.

## Phase 1 — Asset inventory

Locate the assets. Usually the user provides a folder; if they name external sources (Meta Ad Library, a website, social profiles) gather what's accessible first, but never block on missing sources — work with what exists and note coverage gaps in the final document.

Build `work/inventory.json`, one entry per asset:

```json
{"file": "path", "kind": "image|video|source_file", "width": 1080, "height": 1920,
 "format_class": "square|portrait|story|landscape", "content_type": "best guess: product-ad|announcement|seasonal|job-ad|...",
 "campaign_hint": "from filename/folder", "date_hint": "from filename if present"}
```

Folder names and filenames are metadata — Turkish, German, or any-language campaign names, dimensions in filenames ("1080x1920px"), dates, and platform markers ("META", "Google", "Pmax") all go into the inventory. Keep assets from different pipelines (e.g., Meta vs. Google vs. organic) distinguishable: they sometimes follow different sub-systems, and mixing them silently muddies the frequency analysis.

- **Videos:** extract 3 frames each (10%/50%/90%) with `scripts/extract_frames.py` — the 10% frame shows the hook, 50% the layout system, 90% the endcard/CTA convention.
- **Design source files** (.psd/.ai/.aep/.fig): don't skip them — run `strings file.psd | grep -iE "font|typeface" | sort -u` (and similar) to recover *actual font names*, which vision analysis can only approximate. Also record their layer/file naming if informative.
- **Corpus size:** 30–60 assets is the sweet spot. Under ~15, tell the user the guideline will be provisional and which content types are missing. Over ~80, sample proportionally across content types and dates rather than analyzing everything.

## Phase 2 — Visual analysis

Two passes, programmatic first, because AI color estimates are approximate and you want ground truth to anchor against.

**2a. Programmatic palette extraction.** Run `scripts/extract_palette.py <asset_dir> -o work/palette.json`. It quantizes every image, clusters recurring colors across the corpus, and reports which hexes appear in what share of assets. Colors recurring across many images are brand colors; colors appearing once are content. This output is the authority on hex values — the vision pass is the authority on *how* colors are used.

**2b. Vision extraction via subagents.** Fan out parallel subagents (vision-capable model required), 8–15 images per agent, grouped by category/campaign so each agent sees coherent sub-systems. Each agent must actually VIEW every image with the Read tool — never let an agent infer design from filenames; that defeats the entire purpose. Give each agent the extraction schema from `references/extraction-schema.md` and have it write one JSON entry per asset to its own output file.

Tell each agent explicitly:
- estimate hexes but defer to the programmatic palette for final values
- describe typography by characteristics (weight, case, geometry, mood) and name a closest match only as a hypothesis, unless Phase 1 recovered real font names
- record the *content hierarchy as a reading order* (e.g., badge → headline → product → price → CTA), not just a list of elements
- note per-asset anything that looks like a deliberate rule-break (seasonal overrides, co-branded pieces)

**2c. Copy/tone capture.** While viewing, agents transcribe visible copy (headlines, CTAs, badges, legal lines) verbatim into the JSON. Tone of voice is extracted from this corpus in Phase 3 — for service brands especially, voice is a first-class design element.

## Phase 3 — Pattern synthesis

Aggregate all agent JSON outputs and build a frequency matrix (a small Python script over the JSONL beats eyeballing). For every dimension — primary color, headline treatment, alignment, layout grid, badge devices, icon style, CTA phrasing, density, white space — tally the distribution and classify:

- **≥70% of assets** → core brand rule. Codify it as a rule.
- **30–70%** → contextual variation. Find the context: split the corpus by `content_type`, `campaign_hint`, and `format_class` and re-tally. A value that's 40% overall but 95% within "seasonal" assets is a *sub-system rule*, not noise. Document each sub-system explicitly (e.g., "category color-coding: blue = X, gold = Y").
- **<30%** → exception. List it as observed-but-not-a-rule; never codify.

Reconcile the vision palette against the programmatic palette here: keep hexes that both passes agree recur, and resolve disagreements in favor of the programmatic pass.

If performance data exists (e.g., ad metrics from an ads MCP or a file the user provides), join it to assets now and note which patterns correlate with performance tiers — a guideline that says "this layout converts 5x better" is far more useful to a generation pipeline than one that only says "this layout exists". But keep correlation claims honest: ad-level attribution, small samples, and audience confounds all apply.

## Phase 4 — Guideline drafting

Write the guideline document following `references/guideline-template.md` (9 sections: foundation, logo, color, typography, layout, graphic elements, imagery, tone of voice, do's & don'ts). Read the template before writing — it encodes the section-level expectations, including the rule/variation/exception labeling.

Things that separate a usable guideline from a pretty one:
- Every rule cites evidence: "(observed in 31/38 assets)" or names example files. Unverifiable rules get challenged by designers and ignored by pipelines.
- Specifics over adjectives: "headline: extra-bold rounded sans, all-caps, ~2.5x body size, tight tracking" beats "bold modern typography".
- Sub-systems get their own subsections with their trigger condition ("when the asset is seasonal/co-branded/category X, the following overrides apply...").
- The do/don't section uses real filenames from the corpus as the do's, and describes the don'ts as violations of specific numbered rules.

## Phase 5 — Validation & generation handoff

**5a. Style prompt block.** Distill the guideline into a compact reusable prompt block (template at the end of `references/guideline-template.md`) — colors with hexes, typography traits, layout formula, imagery treatment, tone, per-format dimensions. One block per sub-system if sub-systems exist. This is the artifact a generation pipeline actually consumes; treat it as a deliverable equal to the document.

Every hex that appears in a style prompt block must be programmatically confirmed, not vision-estimated — generation pipelines reproduce these values literally, so an eyeballed badge yellow propagates into every future asset. Corpus-level clustering often misses small accents (badges, price pills); for those, crop the element region and pixel-sample it (a few lines of Pillow). If a color genuinely can't be confirmed, mark it `(estimate)` inside the block.

**5b. Consistency scoring (when generated samples exist or can be made).** Run any generated/recreated asset back through the Phase 2 extraction schema and diff the JSON against the corpus norms. Divergences are either generation errors or — equally likely — ambiguous/missing rules in the guideline. Feed the latter back into the document.

**5c. Coverage statement.** End the document with what the corpus did NOT contain (platforms, content types, formats) so future users know which rules are extrapolations.

## Deliverables

Save to the user's workspace folder: the guideline document (markdown unless the user asks for docx/pdf), the style prompt block(s), and a `data/` subfolder with `inventory.json`, `palette.json`, and the per-asset extraction JSONs. Intermediate scratch goes in `work/`, not the deliverable folder.
