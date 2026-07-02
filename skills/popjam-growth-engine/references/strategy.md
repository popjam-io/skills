# Phase 4 — Ad strategy: angles, hooks, and concepts

Read this when you have audiences and personas on disk and it's time to decide *what the ads
say*. This phase has two steps: first build an **angle/hook map** per audience
(`strategy/<aud-slug>-angles.json`), then generate **concepts** — AdDraft-shaped JSON files in
`concepts/` that the media phase ([higgsfield-media.md](higgsfield-media.md)) and simulation
phase ([simulation.md](simulation.md)) consume. The variant-mode and learning-mode prompt text
also lives here; *when* to invoke them is covered in [iteration.md](iteration.md).

## Inputs and outputs

Read from the campaign dir: `brand.json`, `products.json` (the working set, max 50 — never
pull in more), `research.md`, `brief.md`, `audiences/<aud-slug>.json`, and each audience's
personas. Write: `strategy/<aud-slug>-angles.json`, then `concepts/<concept-id>.json` per
concept. Append every non-obvious decision (angle chosen over what, format choice, platform
pick) to `log.md`. File shapes are defined in [data-models.md](data-models.md).

Concept IDs are slugs derived from the angle: `con-hustle-01`, `con-hustle-02`. Variants
append a version suffix and point home: `con-hustle-01-v2` with `og_id: "con-hustle-01"`.

## Step 1 — The angle/hook map (`strategy/<aud-slug>-angles.json`)

Work one audience at a time. Put yourself in the frame POPJAM uses for this exact job.

Adapted from POPJAM's campaign agent:

```
You are a marketing director tasked with figuring out the right angles and hooks with ad
creatives that speak to our target audience segments.

Write a campaign brief using the provided information.
Keep it strictly about the ad creatives and target audience segments.
DON'T include planning, metrics, budget, or other non-creative aspects.
Do a competitor analysis to build the right strategy before you start writing.
```

You already have the competitor analysis in `research.md` and the brief in `brief.md` — ground
the map in those findings rather than re-deriving them. For each audience produce **3–5
angles**. An angle is a persuasion route, not a tagline; each one needs:

- **A named psychological mechanism** — loss aversion, identity signaling, curiosity gap,
  authority transfer, effort reduction, belonging, status elevation, anchoring, reciprocity.
  Name it explicitly so simulation feedback can be traced back to a mechanism, not just a
  headline. Social-proof mechanisms are only available when the inputs contain *real* proof
  (a genuine review count, a named client) — see the grounding rule below.
- **A tie to the archetype** — cite which trait scores or pains in the audience's archetype
  (see [audiences.md](audiences.md) and [data-models.md](data-models.md)) make this mechanism
  land. An angle that can't name its trait is a guess.
- **Evidence from research** — the finding in `research.md` or `brief.md` that supports it
  (a competitor gap, a converting hook pattern, a market insight). Quote or reference it.
- **2–3 hooks** — the concrete opening line/visual beat that earns the first second. Vary
  hook *type* across the set. Adapted from POPJAM's post agent: craft each hook as "a
  relatable *question*, a surprising *statistic/fact*, a provocative-but-true *bold
  statement*, an in-medias-res *anecdote*, or a short powerful *quote* — always in the
  platform's register."
- **Platform fit notes** — where this angle plays best and why. Use the scoring weights as a
  compass, because the deterministic scorer will reward exactly this alignment: TIKTOK weighs
  attention (.30) and emotional_resonance (.25) heaviest, so raw-hook, feeling-first angles
  belong there; GOOGLE weighs relevance (.25) and clarity (.25), so intent-matching,
  plain-benefit angles; LINKEDIN weighs relevance (.25) and persuasion (.20), so
  evidence-led professional angles. Platform values are exactly: `FACEBOOK`, `INSTAGRAM`,
  `GOOGLE`, `YOUTUBE`, `LINKEDIN`, `TWITTER`, `TIKTOK`, `REDDIT`.

Illustrative shape (authoritative schema in [data-models.md](data-models.md)):

```json
{
  "audience": "aud-fitness-parents",
  "angles": [
    {
      "id": "hustle",
      "name": "20 minutes is a workout",
      "mechanism": "effort reduction — reframes the barrier (no time) as the product's core promise",
      "trait_link": "archetype scores high on time scarcity pain; low novelty-seeking",
      "evidence": "research.md: top 3 competitors all sell 45-60min programs; none own the micro-workout position",
      "hooks": [
        "question: 'When did a workout last fit between school runs?'",
        "bold statement: 'The gym is optional. Twenty minutes isn't.'"
      ],
      "platform_fit": { "TIKTOK": "hook-first demo, 9:16", "GOOGLE": "intent match on 'short home workout'" }
    }
  ]
}
```

Before moving on, check the map covers *different* mechanisms — five variations of one
mechanism is one angle. Log the angles you considered and rejected in `log.md`; rejected
angles are cheap raw material for later variant rounds.

## Step 2 — Concept generation (AdDraft)

Each concept picks one angle + one hook from the map and becomes a full ad. Default to 2–3
concepts per audience for a first round (POPJAM's whole-campaign default is 2 per audience) —
breadth comes from simulation-driven variants, not from a huge first batch. Write each to
`concepts/<concept-id>.json`: the POPJAM AdDraft core fields plus the skill extensions
(`id`, `audience`, `angle`, `hook`, `product_ids`, `media`) — schema in
[data-models.md](data-models.md). `subject_type` is `AD`; the full SubjectType enum is
`AD, POST, BLOG, EMAIL, PRESENTATION`. Ad formats use `TEXT, IMAGE, VIDEO, SHORT, ANIMATION`
(the remaining Format values `POST, MESSAGE` belong to other content types).

Generate in the persona POPJAM uses, with its rules intact.

Adapted from POPJAM's adgen agent:

```
You are an expert ad creative strategist, finding VERY CREATIVE concepts to create HIGH PERFORMING ADS on digital platforms.

# Rules
- Ground every claim in the provided context: NEVER invent statistics, user counts, awards, social proof (e.g. "join thousands of customers"), prices, discounts, or operational promises (e.g. "24-hour quotes", "free trial") that are not explicitly present in the brief, website/research content, brand, or product data. Strong copy persuades with the real facts you were given.
- `media_description` is always in English (ad copy language adjusts to the target audience): specific, visual, and detailed — visual elements, composition, color scheme, messaging, plus the expected aspect ratio and platform format — optimized for CTR and ROI on the target platform.
```

The grounding rule is the single most load-bearing quality rule in this skill, and a **hard
fail** in POPJAM's own evals — an ad with an invented "4.9 stars from 12,000 customers" is
worthless no matter how well it scores. If a claim isn't in `brand.json`, `products.json`,
`research.md`, or `brief.md`, it doesn't go in the ad. Before saving each concept, re-read
headline, body, and call_to_action against those files and strike anything unsupported.
`target_url` follows the same rule: a real URL from brand or product data, never invented.

Leave `media.url` empty at concept time — the media phase fills it after generation
(POPJAM's rule is "Don't EVER fill `media_url` — the media generation service fills it
later"; here the service is you, one phase later).

### Choosing and honoring the format

If the user pinned a format, it is binding — set it on every concept, no substitutions
(POPJAM's validator rejects the whole batch otherwise). If not, decide per concept, adapted
from adgen's format-unspecified branch: "You must decide the best ad format for this campaign
based on the target audience, platform, campaign brief, and product. Choose from: TEXT,
IMAGE, or ANIMATION." Default the first round to `IMAGE` — POPJAM forces
`AdSpec(format=IMAGE)` in whole-campaign runs "so every creative has a media_url for
vision-based simulation" — and reserve VIDEO/SHORT for concepts that survive a simulation
round (see cost discipline in [higgsfield-media.md](higgsfield-media.md)).

Per-format `media_description` guidance, adapted from POPJAM's adgen agent:

- **TEXT** — "DON'T fill `media_description` field since this ad is text only."
- **IMAGE** — "Make sure `media_description` field describes an image in detail like a
  creative director." (Composition, palette, lighting, negative space for copy — the full
  prompt-writing discipline is in [higgsfield-media.md](higgsfield-media.md).)
- **VIDEO** — "Make sure `media_description` field describes a video ad. Keep the script
  SHORT — at natural speaking pace (~2.5 words/sec), an 8s video fits ~18 words of dialogue,
  a 12s video fits ~28 words. Write only a hook, one key benefit, and a CTA. Do NOT write a
  full paragraph of dialogue — it will be cut off before finishing. Focus `media_description`
  on the visual narrative (scene, actions, mood, product placement) with minimal dialogue
  cues."
- **SHORT** — "Make sure `media_description` field describes a short-form UGC-style video ad
  (8-15 seconds). Keep the script VERY SHORT — at natural speaking pace (~2.5 words/sec), 8s
  fits ~18 words, 12s fits ~28 words. Write only a punchy hook + one benefit + CTA. No long
  monologues. Focus `media_description` on the visual scene and authentic feel, not walls of
  dialogue."
- **ANIMATION** — describe a motion-graphics animation as a frame-accurate 30fps Remotion
  brief: global spec (duration in seconds *and* frames, aspect from platform, exact-hex
  palette, font roles), scene-by-scene frame ranges, per-element on-screen text that
  choreographs the ad's own headline/body/CTA copy ("don't invent different copy"),
  entrance/dwell/exit frames with easing, and one line of frame math proving the totals. The
  full spec — scene budgets, dwell minimums, safe zones, typography scale — is in
  [remotion-animations.md](remotion-animations.md); write the brief against it, not from
  memory.

### Platform hard limits

These come from POPJAM's per-platform playbooks and are non-negotiable — a concept violating
them fails before any persona sees it:

| Platform | Hard limit |
|---|---|
| TWITTER | 280 characters max per tweet; thread (1/n) only if it truly can't fit; at most 1–2 hashtags |
| INSTAGRAM | 3–5 highly relevant hashtags near the end, **5 maximum in total**; no clickable links in captions — say "link in bio" |
| REDDIT | No hashtags or @ mentions; not promotional — write as a peer; **affiliation disclosure is mandatory**, never pose as an unaffiliated satisfied customer (astroturfing) |
| TIKTOK | 9:16 vertical media; short punchy caption — a hook line plus 3–5 relevant hashtags |
| GOOGLE | No hashtags; concise copy with a clear action phrase ("Book now") |
| LINKEDIN | 1–3 relevant hashtags; short paragraphs (1–3 sentences), hook in the first 2–3 lines |
| FACEBOOK | 0–2 hashtags; gentle CTA ("Learn more at [link]", not "Buy now") |
| YOUTUBE | 0–3 hashtags; 16:9 visual |

Aspect ratios follow placement: 9:16 for TIKTOK/Reels/Shorts/Stories, 1:1 for Meta feed,
16:9 for YOUTUBE — set `media.aspect_ratio` at concept time so media generation renders
per-placement instead of cropping after.

### Language

Copy language follows the audience (their locale, or the user's explicit choice), pinned by
IETF BCP 47 code. When a language is set, apply POPJAM's language section verbatim, with
`{{language}}` filled in:

```
# Language Requirement
ALL generated content MUST be written exclusively in the language identified by IETF BCP 47 code `{{language}}`. Do NOT use any other language for any part of the output.
```

The one exception is baked into the adgen rule above: **`media_description` is ALWAYS
English**, even when every line of copy is Turkish or Swedish — image/video models are
prompted in English regardless of the ad's market.

### Product linking

Every ad features at least one real product: set `product_ids` to IDs from `products.json`
only. Adapted from POPJAM's product_linker agent: "pick at least one product that the ad copy
actually features. Multiple = bundle creative. Prefer precision over coverage." If the user
pinned products, keep those first in the working set and feature them; never link a product
the copy doesn't actually show or name.

## Variant mode and learning mode (prompt text)

Two prompt sections modify concept generation on later rounds. They are **mutually
exclusive**: a source concept present → variant mode; no source but past insights exist →
learning mode. The mechanics — when to trigger them, how many variants, how insights are
selected — live in [iteration.md](iteration.md); the prompt text is here because it runs
inside this phase's generation prompt, appended after the task line.

Adapted from POPJAM's variant-mode prompt section (fill `{{subject_label}}` with
"advertising creative", `{{variant_n}}` with the count; `{{source_content_xml}}` is the
original concept's platform/format/copy plus media URL and kind; `{{insights_xml}}` is the
full insight JSON when one exists — resolve the `{{#if}}`/`{{#unless}}` branches by whether
you have insights, and the `has_media` branch by whether the original has media):

```
# Variant Mode — Improve Existing Content
You are NOT generating new {{subject_label}} from scratch. You are producing improved VARIANTS of the existing {{subject_label}} below.
{{source_content_xml}}
{{#if insights_xml}}
{{insights_xml}}

# Variant Task
Create {{variant_n}} improved variant(s) of the {{subject_label}} above that address the feedback in <insights> while preserving its strengths. Implement the recommended actions from the insights (not necessarily all of them in a single variant).
{{/if}}{{#unless insights_xml}}

# Variant Task
Create {{variant_n}} fresh variant(s) of the {{subject_label}} above. No audience feedback was supplied, so explore a new creative direction while preserving its core message and strengths. Each variant MUST be meaningfully different from the original — do not merely restate it.
{{/unless}}For EACH variant you MUST set the `reasoning` field, explaining how it differs from and improves on the original.{{#if has_media}}
Because the source has media, your `media_description` MUST build on the original visual and evolve it — do not start from a blank slate.{{/if}}
```

Variants get `og_id` set to the original's concept id and a filled `reasoning` field — both
are required in variant mode and absent otherwise (POPJAM's schema note: `reasoning` is
"populated ONLY in variant mode... stays None for fresh generation").

Adapted from POPJAM's learning-mode prompt section (`{{learning_insights_xml}}` is a digest
of up to 5 recent insights for this audience — per insight: `engagement_score`, sentiment
counts `{positive, neutral, negative}`, `resonated` themes, `recommended_actions`,
`summary` — wrapped in `<past_simulation_insights>`):

```
# Audience Memory — Lessons from Past Simulations
This audience has reacted to earlier {{subject_label}} in prior simulations. Use these aggregated lessons to inform the new work: lean into what resonated, avoid recurring failure points, and apply the recommended actions — WHILE still exploring fresh, original angles. Do NOT merely copy past winners; treat this as accumulated taste, not a template.
{{learning_insights_xml}}
```

That last sentence is the point of learning mode: past winners inform taste, they are not a
template to clone.

## Self-check before handing off

POPJAM validates drafts deterministically; do the same pass on every concept file:

1. Format matches the request when one was pinned; visual formats have `media_description`,
   TEXT has none.
2. Grounding audit: every claim, price, and promise traces to an input file.
3. Platform hard limits respected; `media_description` is English; copy is in the pinned
   language.
4. `product_ids` non-empty and every id exists in `products.json`.
5. Variant concepts have `og_id` + `reasoning`; if the original had media, the new
   `media_description` builds on that visual.

Log the batch in `log.md` (concept ids, angle each one banks on, format/platform rationale).

## Fan-out

For a couple of audiences, run Step 1 then Step 2 sequentially per audience — the shared
context (brand, research, brief) stays warm and quality is easiest to police. When
orchestrating at scale (many audiences, or strategy running alongside persona generation),
use the Workflow tool with the script templates in the skill's `workflows/` dir; POPJAM runs
per-audience work concurrently but bounds all leaf LLM calls at concurrency 6 — stay in that
neighborhood rather than fanning out unbounded.
