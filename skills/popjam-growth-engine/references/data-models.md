# Data Models — the campaign file contract

Read this when you need the exact shape of any file in the campaign directory: brand.json, products.json, audience/persona JSONs, concept JSONs, reactions.json, insight.json, or question/answer JSONs. This is the single schema source for the whole skill — every other reference links here instead of redefining shapes. Field descriptions marked verbatim come straight from POPJAM's backend models, where they double as prompt engineering (PydanticAI feeds them to the LLM as JSON-schema descriptions), so reuse them word-for-word when you author these fields. JSON examples below use `//` comments for annotation; the files you write must be plain valid JSON without comments.

## LLM-visible vs system-filled fields

POPJAM hides system fields from agents via `SkipJsonSchema` and marks them "NEVER fill this field" — the model literally cannot author ids, timestamps, or computed scores. Mirror that split:

- **You author (LLM-visible):** all copy, descriptions, demographic arrays, trait floats, scoring dimensions (0–10), engagement/sentiment labels, feedback, narrative insight fields.
- **The system fills (never you):** `id` slugs are assigned mechanically when you create the file (kebab-case, sequential — `con-hustle-01`, not invented per-field), `created_at` timestamps come from the clock, `engagement_score` on reactions and every calculated field on insights/summaries come from `scripts/score.py`, and `media.url|path` comes from the Higgsfield download step. If you catch yourself "estimating" an engagement_score, stop — that number is deterministic math, not judgment.

## Enums

Values must match exactly (uppercase, no aliases).

| Enum | Values |
|---|---|
| `Platform` | `FACEBOOK, INSTAGRAM, GOOGLE, YOUTUBE, LINKEDIN, TWITTER, TIKTOK, REDDIT` |
| `Format` | `TEXT, IMAGE, VIDEO, SHORT, POST, MESSAGE, ANIMATION` |
| `SubjectType` | `AD, POST, BLOG, EMAIL, PRESENTATION` |
| `Gender` | `MALE, FEMALE, NON_BINARY, OTHER` |
| `MediaKind` | `"image", "video", "slides"` (lowercase literals, used only in the concept `media` block) |

Format rules, from POPJAM's Content model:

- **Visual set:** `is_visual` = format ∈ {`IMAGE`, `VIDEO`, `SHORT`, `ANIMATION`}. Visual formats route through media generation; non-visual formats must never be dispatched to it.
- **Forced formats per subject type:** `AD` uses the full enum (`TEXT`/`IMAGE`/`VIDEO`/`SHORT`/`ANIMATION`); `POST` and `BLOG` are always `IMAGE`; `EMAIL` and `PRESENTATION` are always `TEXT`.
- **Aspect ratios** (image): `"1:1" | "2:3" | "3:2" | "3:4" | "4:3" | "4:5" | "5:4" | "9:16" | "16:9" | "21:9"`.
- **Media model literals** (recorded in `media.model` for provenance): image `"gpt" | "gemini" | "gemini-pro"` (POPJAM default `gemini-pro`), video `"veo3" | "sora-2" | "sora-2-pro"` (default `veo3`), animation `"remotion"`. When generating via Higgsfield MCP instead, record the actual Higgsfield model id string — see [higgsfield-media.md](higgsfield-media.md).

## brand.json — the style contract

One per campaign directory. Every downstream prompt (copy, media, simulation) reads tone/typography/colors/language from here, so fill it before anything else.

```jsonc
{
  "name": "Huel",                       // "Name of the brand." (verbatim)
  "url": "https://huel.com",            // "URL of the official brand website homepage."
  "language": "en-GB",                  // "Target locale of the brand. (IETF BCP 47)" — governs ALL user-facing copy
  "tone": "Direct, science-backed, lightly irreverent",  // "Tone of the brand's messaging."
  "typography": "Inter, sans-serif",    // "Typography of the brand (font family, for use in HTML)."
  "colors": ["#0B0B0B", "#F5F0E8", "#00C16A"],  // "Colors of the brand (#hexcode, formatted for use in HTML)."
  "guidelines": "## Voice\n- ...",      // "Brand guidelines in markdown format (voice, style, dos and don'ts, etc.)."
  "logos": [                            // theme = which background the logo is designed for
    { "url": "https://.../logo-dark.svg", "theme": "light" },   // dark logo for light backgrounds
    { "path": "assets/logo-white.png",   "theme": "dark"  },    // downloaded copies use path instead of url
    { "url": "https://.../logomark.svg", "theme": "any"   }     // theme ∈ {"light","dark","any"}, default "any"
  ]
}
```

## products.json — the working set

An array, capped at 50 products, because POPJAM never injects a full catalog into prompts (creative agents cap the working set and keep pinned items). If the catalog is larger, curate the 50 most campaign-relevant and note the cut in log.md.

```jsonc
[
  {
    "id": "prod-black-edition",         // slug, assigned mechanically
    "url": "https://huel.com/products/black-edition",  // "URL of the official website or listing for this product."
    "name": "Huel Black Edition",       // "Name of the product."
    "description": "High-protein, low-carb meal ...",  // "Description of the product."
    "specs": ["40g protein", "0 added sugar"],         // "Specifications of the product."
    "images": ["https://.../black-1.jpg"],  // "URLs of images of the product, make sure to use FULL URLs and not just relative paths."
    "attributes": {                     // optional; from feeds when available — never invent prices
      "price": "34.00", "sale_price": null, "currency": "GBP", "in_stock": true
    }
  }
]
```

## audiences/&lt;aud-slug&gt;.json

One file per audience. All demographic arrays are optional except `needs` — POPJAM makes needs optional at the DB layer, but this skill requires them because the strategy step maps angles onto needs and produces generic output without them.

```jsonc
{
  "id": "aud-fitness-parents",
  "title": "Time-poor fitness parents",     // "Title of the target audience"
  "description": "Parents 30-45 who ...",   // "Freeform description of the target audience"
  "age_min": 30, "age_max": 45,             // "Min/Max age of the personas" (0 < x < 150)
  "genders": ["FEMALE", "MALE"],            // "Gender if relevant/provided" — Gender enum values
  "locations": ["London, UK"],              // "e.g., 'New York, USA', 'Stockholm, Sweden'"
  "occupations": ["Marketing manager"],     // "Jobs or roles of the personas"
  "income_levels": ["medium", "high"],      // "e.g., 'high', 'medium', 'low'"
  "interests": ["home workouts", "meal prep"],  // "Key interests/hobbies (e.g., 'sports', 'technology')"
  "personality_traits": ["organised", "skeptical of fads"],  // "e.g., 'introverted', 'extroverted'"
  "needs": ["fast nutritious meals", "guilt-free convenience"],  // REQUIRED — "Needs of the personas in the given context"
  "archetype": { "elite": 0.2, "societal_competition": 0.5, /* ... all 16, floats 0.0-1.0 */ }
}
```

### The 16-trait archetype

"A buyer archetype with 16 behavioral traits on a 0.0 to 1.0 scale." All 16 are required floats in [0, 1]. Meanings, verbatim:

| Trait | Meaning |
|---|---|
| `elite` | Represents elitism, status, power, superiority, and exclusivity (premium lifestyle). |
| `societal_competition` | Focuses on achievement, performance, energy, and willpower within competitive systems. |
| `authority` | Prioritizes discipline, control, supervision, and societal adjustment. |
| `conformity` | Upholds conformity, manners, tradition, norms, and recognition by others. |
| `social_security` | Reflects social safety, group belonging, support, and emotional shelter. |
| `home` | Represents tradition, homeland, rootedness, and connection to nature and familiarity. |
| `benevolence` | Emphasizes protection, safety, family values, and love. |
| `order` | Values order, structure, logic, functionality, and health. |
| `quality` | Focuses on quality, efficiency, precision, standards, and effectiveness. |
| `individual_order` | Reflects individuality, self-expression, personal values, and simple, light personal structure. |
| `success` | Driven by personal success, reward, recognition, and goal achievement. |
| `fight` | Centers on fighting spirit, strength, ambition, and a winner mentality. |
| `rebellion` | Includes rebellion, protest, revolution, anarchy, and breaking away from norms. |
| `risk` | Focuses on risk-taking, adventure, courage, instinct, curiosity, and thrill-seeking behavior. |
| `autonomy` | Represents independence, dreaminess, fantasy, and emotional openness. |
| `discovery` | Emphasizes freedom, creativity, imagination, visionary thinking, humor, and fun. |

## personas/&lt;aud-slug&gt;/&lt;persona-slug&gt;.json

"Represents a simulated person in the target audience." One file per persona; score.py reads the whole directory.

```jsonc
{
  "id": "per-amara-okafor",
  "audience_id": "aud-fitness-parents",     // parent audience slug
  "name": "Amara Okafor",                   // "A fictitious name for the persona"
  "age": 37,                                // must fall within the audience's age_min..age_max
  "gender": "FEMALE",                       // Gender enum
  "location": "London, UK",                 // "e.g., 'New York, USA', 'Stockholm, Sweden'"
  "occupation": "NHS nurse",                // "Job or role"
  "income_level": "medium",                 // "e.g., 'high', 'medium', 'low'"
  "bio": "Amara juggles 12-hour shifts ...",// "A short narrative paragraph summarizing the persona"
  "interests": ["HIIT", "batch cooking"],
  "personality_traits": ["pragmatic", "warm"],
  "segment_tags": ["gen_y", "shift-worker"],  // "Tags linking persona to input segment"
  // ...plus ALL 12 behavioral floats as TOP-LEVEL fields (POPJAM parity — score.py reads them here):
  "price_sensitivity": 0.7, "brand_loyalty": 0.3, "novelty_seeking": 0.4,
  "environmental_consciousness": 0.5, "design_appreciation": 0.4, "tech_savviness": 0.6,
  "social_influence_sensitivity": 0.5, "risk_aversion": 0.6, "convenience_preference": 0.8,
  "value_orientation": 0.8, "emotional_engagement": 0.5, "pragmatism": 0.8
}
```

`segment_tags` includes a generation tag derived from age — POPJAM's exact bands: `gen_alpha` ≤ 12, `gen_z` ≤ 28, `gen_y` ≤ 44, `gen_x` ≤ 60, `gen_boomer` ≤ 79 — plus free-form tags for sub-segments you deliberately seeded (e.g. `shift-worker`, `price-skeptic`).

### The 12 behavioral traits

All required floats 0.0–1.0. These feed score.py's trait-weight adjustments, so anchor them honestly — a panel of all-0.5s produces flat, useless scores. Anchored meanings, verbatim:

| Trait | Meaning |
|---|---|
| `price_sensitivity` | sensitivity to price changes (0.0 = not price-sensitive, 1.0 = extremely price-sensitive) |
| `brand_loyalty` | tendency to stick with preferred brands (0.0 = no brand preference, 1.0 = extremely brand-loyal) |
| `novelty_seeking` | desire for new and novel products (0.0 = avoids new products, 1.0 = craves new experiences) |
| `environmental_consciousness` | concern for sustainability and eco-friendliness (0.0 = not eco-conscious, 1.0 = highly sustainability-focused) |
| `design_appreciation` | value placed on product and packaging design/aesthetics (0.0 = indifferent to design, 1.0 = highly values aesthetics and design) |
| `tech_savviness` | comfort with technology and adoption of new tech (0.0 = tech-averse, 1.0 = extremely tech-savvy) |
| `social_influence_sensitivity` | how peer opinions and social trends affect the persona (0.0 = not influenced by peers, 1.0 = heavily influenced by others) |
| `risk_aversion` | aversion to risk in trying new products (0.0 = risk-seeking, 1.0 = extremely risk-averse) |
| `convenience_preference` | preference for convenience and ease of use (0.0 = willing to sacrifice convenience, 1.0 = values convenience above all) |
| `value_orientation` | focus on getting the best value (0.0 = not value-driven, 1.0 = extremely value-conscious) |
| `emotional_engagement` | degree of emotional or impulsive involvement in purchases (0.0 = purely rational buyer, 1.0 = highly emotion-driven) |
| `pragmatism` | practical vs idealistic decision approach (0.0 = idealistic/impractical, 1.0 = extremely pragmatic and practical) |

## concepts/&lt;concept-id&gt;.json — the AdDraft + extensions

Core fields map 1:1 to POPJAM's `AdDraft` (the LLM output contract for ad generation — note the backend maps `headline` → Content.title). Skill extensions carry what POPJAM's database would otherwise track.

```jsonc
{
  // ---- skill extensions ----
  "id": "con-hustle-01",                    // slug; variants append -v2, -v3 ...
  "audience": "aud-fitness-parents",        // audience slug this concept targets
  "angle": "reclaim-your-lunch-hour",       // from strategy/<aud-slug>-angles.json
  "hook": "You meal-prepped for the kids. Who prepped for you?",
  "product_ids": ["prod-black-edition"],    // must exist in products.json

  // ---- AdDraft core ----
  "subject_type": "AD",                     // SubjectType enum
  "platform": "TIKTOK",                     // Platform enum — "Platform/medium (ad/post)"
  "format": "SHORT",                        // Format enum; drives media generation
  "headline": "Öğle aranı geri al",         // in brand.json language
  "body": "...",                            // main copy, brand language
  "media_description": "Handheld vertical shot of a nurse ...",  // ALWAYS English, regardless of brand language — generation models follow English prompts most reliably
  "call_to_action": "Shop Black Edition",   // "CTA text (ad)"
  "target_url": "https://huel.com/black",   // "CTA URL (ad)"

  // ---- variant semantics (originals keep both null) ----
  "og_id": null,                            // "Original this is a variant of (None ⇒ this is an original)"
  "reasoning": null,                        // "Why this variant differs from its original (variants only)"

  // ---- media block (null until generated; see higgsfield-media.md) ----
  "media": {
    "url": "https://...",                   // remote asset URL, or
    "path": "creatives/con-hustle-01/short.mp4",  // local downloaded copy (prefer both)
    "aspect_ratio": "9:16",                 // from the aspect-ratio literal set
    "model": "veo3",                        // model literal or Higgsfield model id
    "kind": "video",                        // MediaKind: "image" | "video" | "slides"
    "logo_ok": false                        // did the brand logo survive generation intact? (POPJAM measures ~30% fidelity — generation models redraw logos)
  }
}
```

`reasoning` is populated ONLY in variant mode (when improving an existing ad from insights) and stays null for fresh generation — it is the audit trail linking an iteration to the insight that motivated it. A variant is a full standalone concept file (`con-hustle-01-v2.json` with `og_id: "con-hustle-01"`), not a diff.

## simulations/&lt;concept-id&gt;/reactions.json

A wrapper object with file-level metadata (score.py reads `platform`/`subject_type` from it when the CLI flags are omitted) and exactly one reaction per persona in the target audience. "Represents a persona's reaction to a given simulatable subject."

```jsonc
{
  "concept_id": "con-hustle-01",
  "platform": "TIKTOK",                 // Platform enum — drives the scorer's weight table
  "subject_type": "AD",                 // SubjectType enum — drives content-type multipliers
  "provenance": { "model": "claude-fable-5", "date": "2026-07-02" },  // scores across models/dates are not comparable
  "reactions": [
  {
    "persona_id": "per-amara-okafor",
    "engagement": "Will Click",         // EXACTLY one of: "Will Click", "Might Click", "No Interest"
    "sentiment": "Positive",            // EXACTLY one of: "Positive", "Neutral", "Negative"
    "feedback": "The lunch-hour framing lands — I never ...",  // "The persona's comment or reasoning", first person, in character
    "keywords": ["convenience", "guilt"],  // "Important keywords extracted from the feedback"
    "scoring": {                        // 6 integer dimensions, each 0-10, filled by you
      "attention": 8, "relevance": 9, "emotional_resonance": 7,
      "persuasion": 6, "brand_fit": 7, "clarity": 9
    },
    "engagement_score": null            // NEVER authored — score.py fills it (0-100)
  }
  ]
}
```

The three engagement labels are fixed for every content type — interpret them through the engagement question (e.g. for a social post, "Will Click" means you would actively engage: like, share, comment, or follow). Sentiment should be consistent with engagement (e.g., "Will Click" rarely pairs with "Negative").

The six scoring dimensions ("Inspired by AIDA, System1 Star Rating, and Kantar LINK+ methodologies"), verbatim:

| Dimension | Meaning |
|---|---|
| `attention` | How likely the ad captures initial attention within 2-3 seconds (scroll-stopping power, visual hook strength) |
| `relevance` | How well the ad content matches the persona's interests, needs, and current life stage |
| `emotional_resonance` | Intensity of emotional response (positive OR negative) the ad evokes in this persona |
| `persuasion` | How compelling the value proposition, social proof, urgency, and call-to-action are for this persona |
| `brand_fit` | How well the ad's style, tone, and production quality match the platform norms and audience expectations |
| `clarity` | How quickly and easily the message, offer, and intended next steps are understood |

After writing reactions, run the deterministic scorer — never compute scores yourself:

```
python <skill-dir>/scripts/score.py score --reactions simulations/<id>/reactions.json --personas personas/<aud-slug> --platform TIKTOK --subject-type AD
```

This fills `engagement_score` (0-100) per reaction in place using POPJAM's platform weights x content-type multipliers x persona-trait adjustments.

## simulations/&lt;concept-id&gt;/insight.json

"Aggregated insight from a batch of reactions." Strict two-phase fill: run the aggregator first, then author ONLY the narrative fields.

```
python <skill-dir>/scripts/score.py aggregate --reactions simulations/<id>/reactions.json --out simulations/<id>/insight.json
```

This pre-fills the insight's calculated fields (sentiment counts, mean engagement_score, dimension_averages, consensus_level). The LLM fills ONLY narrative fields afterwards.

```jsonc
{
  // ---- calculated by score.py aggregate — never edit ----
  "concept_id": "con-hustle-01",
  "total_personas": 10,
  "positive": 6, "neutral": 3, "negative": 1,   // case-insensitive sentiment tally
  "engagement_score": 68,               // "Average engagement score (0-100) across all reactions" = round(mean)
  "dimension_averages": { "attention": 7.2, "relevance": 8.1, /* ... all 6, 4dp */ },
  "label_counts": { "Will Click": 4, "Might Click": 4, "No Interest": 2 },
  "consensus_level": "Medium",          // max(sentiment count)/total: >=0.7 "High", >=0.4 "Medium", else "Low"

  // ---- narrative, authored by you AFTER aggregation ----
  "top_feedback_themes": ["lunch-hour guilt resonates", "price objection from value-driven personas"],  // "Key themes from feedback"
  "recommended_actions": ["Lead with the time-saved claim", "Test a price-anchored variant"],           // "Bullet-point recommendations"
  "summary_text": "6 of 10 personas reacted positively ..."   // "Free-form summary narration of results"
}
```

Ground every theme and recommendation in actual reaction feedback — the insight exists to drive the next variant, and a hallucinated theme poisons the iteration loop.

## questions/&lt;q-slug&gt;/ — panel research

Optional direct-question research against a persona panel. Three files per question: `question.json`, `answers.json`, `summary.json`.

```jsonc
// question.json
{
  "id": "q-flavor-pref",
  "question_type": "MULTIPLE_CHOICE",   // "OPEN" | "MULTIPLE_CHOICE" | "AB_TEST"
  "text": "Which flavor would you pick first?",   // "The question text"
  "options": ["Chocolate", "Vanilla", "Salted Caramel"]  // "For 'MULTIPLE_CHOICE', holds answer options; for 'AB_TEST', holds image URIs (URLs or file paths) of variants; required for both". null for OPEN.
}
```

```jsonc
// answers.json — one entry per persona
[
  {
    "persona_id": "per-amara-okafor",
    "answer": "Salted caramel — chocolate shakes always taste artificial to me.",  // "The persona's answer to the question"
    "selected_options": [2],            // "Indices of selected options; required for 'MULTIPLE_CHOICE' and 'AB_TEST'" — null for OPEN
    "confidence": 0.8,                  // float 0-1 — "Confidence level in the answer"
    "reasoning": "Bad experiences with ...",   // "The persona's reasoning for their answer"
    "sentiment": "Positive",            // same fixed set: "Positive" | "Neutral" | "Negative"
    "keywords": ["artificial taste"]
  }
]
```

```jsonc
// summary.json — same calculated/narrative split as insight.json
{
  // calculated — tally by hand/script (score.py aggregate handles reactions only, not answers):
  "total_answers": 10,
  "positive_count": 5, "neutral_count": 4, "negative_count": 1,
  "selected_option_counts": [2, 3, 5],  // per-option tallies, aligned to options[]; null for OPEN
  "consensus_level": "Medium",          // ratio = max(sentiment counts)/total: >=0.7 "High", >=0.4 "Medium", else "Low"
  // narrative (you):
  "top_themes": ["flavor authenticity"],       // "Key themes from answers"
  "unique_insights": ["Two personas assumed ..."],  // "Unique takeaways and insights"
  "summary_text": "..."                        // "Narrative summary of the answers"
}
```

## Validation rules the skill self-enforces

POPJAM enforces these with Pydantic validators and output validators; without a backend, you are the validator. Check them at write time, not after a failed downstream step:

1. **Exact-count persona batches.** When a step asks for N personas, produce exactly N — no more as "bonus", no fewer. Fan out in batches of at most 10 (see [simulation.md](simulation.md) and the templates in `workflows/`).
2. **Age within audience range.** Every persona's `age` satisfies the audience's `age_min <= age <= age_max`; gender must come from the audience's `genders` list when one is set.
3. **Trait bounds.** All 16 archetype floats and all 12 persona trait floats are in [0.0, 1.0]; every trait key present, none invented.
4. **Label exactness.** `engagement` ∈ {"Will Click", "Might Click", "No Interest"}, `sentiment` ∈ {"Positive", "Neutral", "Negative"} — exact strings, exact casing. Scoring dimensions are integers 0–10, all six present.
5. **Sentiment consistent with engagement.** "Will Click" rarely pairs with "Negative" and "No Interest" rarely pairs with "Positive"; if a reaction genuinely needs the odd pairing, the feedback text must explain it.
6. **No simulating missing media.** A concept whose `format` is visual (`IMAGE`/`VIDEO`/`SHORT`/`ANIMATION`) with an empty `media` block is awaiting media — refuse to simulate it, because a vision creative judged on text alone yields garbage reactions. This is POPJAM's `is_awaiting_media` gate; it hard-fails there and hard-fails here.
7. **Referential integrity.** `og_id` references an existing concept file; `reasoning` is non-null on variants and null on originals; `product_ids` exist in products.json; every reaction's `persona_id` exists under the audience's persona directory.
8. **System fields stay systematic.** `engagement_score` and every calculated insight/summary field come only from score.py; `media_description` is always English; brand `colors` are `#hex` strings; `language` is a valid BCP-47 tag.

One reaction file per concept, one entry per persona, reactions complete before aggregation — score.py assumes all three.
