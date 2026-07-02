# Phase 6 — Simulation: the synthetic panel reacts

Read this when a concept (and, for visual formats, its generated creative) is ready to be
tested against the persona panel. This phase produces `simulations/<concept-id>/reactions.json`
and `simulations/<concept-id>/insight.json`, which drive the leaderboard and the variant loop.
File shapes: see [data-models.md](data-models.md).

## The two-stage design — and why you must keep it

POPJAM strictly separates simulation into two passes, and its validators hard-reset any score
an LLM sets during the first pass. Replicate that discipline:

- **Stage 1 (reaction)** — creative role-play at normal temperature: each persona produces an
  engagement label, sentiment, feedback, and keywords. **No numbers.**
- **Stage 2 (scoring)** — a cold, temperature-zero-mindset rubric pass that assigns 6 integer
  dimensions (0–10) per persona, seeing only the content and the qualitative *labels* — not
  the feedback prose.

The separation exists because mixing them causes narrative-driven score inflation: when the
same pass writes an enthusiastic first-person reaction and its scores, the story drags the
numbers up (and vice versa — pre-assigned numbers flatten the prose). Keeping scoring in a
separate pass with a simpler output also makes it far more reliable. So: never write dimension
scores while role-playing, and never rewrite feedback while scoring. The final
`engagement_score` (0–100) is computed by `scripts/score.py`, never by you.

## Preconditions (the awaiting-media guard)

Before simulating, check the concept JSON in `concepts/<concept-id>.json`:

- If the concept's `format` is visual (`IMAGE`/`VIDEO`/`SHORT`/`ANIMATION`) and
  `media.path`/`media.url` is missing or the file doesn't exist under `creatives/<concept-id>/`,
  **refuse to simulate**. POPJAM hard-fails this (`is_awaiting_media`) because vision-based
  judging is mandatory — personas reacting to a text description of an imaginary image produce
  worthless data. Send the concept back to [higgsfield-media.md](higgsfield-media.md) and log
  the refusal in `log.md`.
- Text-only formats (e.g. a plain search ad or email) simulate without media.

Inputs: the concept JSON, the personas for the concept's audience
(`personas/<aud-slug>/*.json`), and the creative asset(s).

## Stage 1 — reaction role-play

Run the panel in batches of **at most 10 personas per pass** — coverage degrades beyond that
(personas get skipped or blur together). For 1–2 batches, just run them sequentially yourself.
For larger panels or multiple concepts × audiences, orchestrate with the Workflow tool using
the script templates in the skill's `workflows/` dir, fanning out one subagent per batch and
one lane per audience.

### Judging visual creatives: look at the actual asset

When the concept has image or video media, the persona reacts to **what they see**, not to the
copy fields:

- **Read the actual image file** from `creatives/<concept-id>/` before writing any reaction.
- **Hide the text blocks**: do not paste `headline`/`body` into the reaction prompt for
  image/video concepts — the copy is baked into or paired with the asset, and showing it
  separately lets personas "react" to text they never saw on screen.
- For **video**, extract 2–3 representative frames (`ffmpeg -i <file> -vf fps=1/3 frame_%02d.png`
  into the scratchpad) and Read those, noting duration and any motion described in the prompt.

For text-only formats, include the text blocks (headline, body, call_to_action) in the prompt.

### Reaction prompt

Adapted from POPJAM's reaction agent — use this as the working instruction for each batch,
filling the `{{...}}` slots:

```
You are simulating realistic persona reactions to content creatives.
You are given persona profiles and a content creative to evaluate.
Respond AS IF YOU WERE EACH PERSONA viewing the content.
You MUST provide exactly one reaction for every persona provided. Do not skip any personas.

For each persona, consider their full profile - demographics, interests, occupation, income,
personality traits, AND their behavioral archetype parameters (price_sensitivity, brand_loyalty,
novelty_seeking, environmental_consciousness, design_appreciation, tech_savviness,
social_influence_sensitivity, risk_aversion, convenience_preference, value_orientation,
emotional_engagement, pragmatism).

## QUALITATIVE REACTION ONLY

You are responsible ONLY for the qualitative reaction fields. Engagement scoring dimensions
are handled separately by a dedicated scoring pass - do NOT fill the `scoring` field.

## GUIDELINES

- Be specific about WHY a persona would or wouldn't engage.
- Let each persona's profile naturally drive the reaction - some will love the content, some won't care.
- Consider real-world factors like price sensitivity, existing solutions, skepticism, and content fatigue
  where they genuinely apply to a persona's profile.

# Content Type: {{SUBJECT_TYPE label, e.g. ADVERTISING CREATIVE}}
{{content: text blocks for text formats; for image/video, the viewed media itself — no text blocks}}
{{personas: full profiles incl. all 12 behavioral trait values}}

# Task
You are provided with {{N}} personas. Return exactly {{N}} Reaction objects, one per persona ID.
As each given persona, provide your reaction to this {{subject label}}. Consider your interests,
needs, and personality. {{engagement guidance for the subject type — see table below}}
If media is provided, base your reaction on the actual viewed media content.

## Required fields per Reaction:
- **engagement**: 'Will Click', 'Might Click', or 'No Interest'. These three labels are fixed for
  every content type — interpret them through the engagement question above (e.g. for a social
  post, 'Will Click' means you would actively engage: like, share, comment, or follow).
- **sentiment**: 'Positive', 'Neutral', or 'Negative'.
- **keywords**: Themes important to this persona's decision.
- **feedback**: 1-3 sentences in first person explaining your reaction. Be critical - point out
  negatives, risks, and blind spots. Frame your reaction in terms of the content type: react to a
  social post as organic content in your feed (share/comment/follow), to an email as something in
  your inbox (open/reply/delete), to an ad as an ad.
- **engagement_score**: leave null — scripts/score.py computes it deterministically.
- **scoring**: leave null — the Stage 2 scoring pass owns it.

## Consistency rules:
- Sentiment should be consistent with engagement (e.g., 'Will Click' rarely pairs with 'Negative')
- Let the persona's profile and the content's relevance naturally determine the reaction
```

Per-subject-type engagement guidance (POPJAM's exact strings):

| SubjectType | Guidance injected into the task |
|---|---|
| AD | Would they click the ad, consider the product, or scroll past? |
| POST | Would they like/share/comment on this post, or scroll past? |
| BLOG | Would they read the full article, bookmark it, or bounce after the intro? |
| EMAIL | Would they open the email, read it, click the CTA, or delete/ignore it? |
| PRESENTATION | Would they stay engaged through the deck, take notes, or zone out? |

If the campaign has a language set, feedback is written exclusively in that IETF BCP 47
language (unlike `media_description`, which is always English).

Validate each batch before saving: exactly one reaction per persona, every persona slug present,
engagement in the three fixed labels, sentiment in {Positive, Neutral, Negative}, feedback
non-empty, `scoring` and `engagement_score` null. If a persona is missing or a label is invalid,
re-run that batch — don't patch reactions in by hand. Write the accumulated reactions to
`simulations/<concept-id>/reactions.json` (shape in [data-models.md](data-models.md)).

## Stage 2 — the cold scoring pass

Run this as a **separate pass** (a fresh subagent via Workflow for large panels, or at minimum a
clean context that does not re-read the feedback prose). Adopt a temperature-zero mindset:
mechanical, rubric-anchored, no storytelling. The pass sees the content (text truncated to
~500 chars per block), each persona's profile with all 12 trait values, and each persona's
`engagement` + `sentiment` labels — nothing else from Stage 1.

Adapted from POPJAM's scoring agent:

```
You are an engagement scoring specialist. You evaluate how specific personas would
engage with a content creative by assigning precise numeric scores across 6
independent dimensions.

You are given:
1. A content creative (ad, post, blog, email, or presentation)
2. A list of personas with their demographic and behavioral profiles
3. Each persona's qualitative labels for the content (engagement decision + sentiment)

Your ONLY job is to assign the 6 scoring dimensions for each reaction. You do NOT
generate feedback, sentiment, or engagement text — those are already provided.

## CONSISTENCY WITH QUALITATIVE REACTION LABELS

Your scores should be consistent with the persona's qualitative labels:
- If a persona has `engagement='No Interest'`, scores should generally skew lower.
- If a persona has `engagement='Will Click'` with positive sentiment, scores should generally skew higher.
- Let the persona's profile and the content's relevance drive per-dimension variation.

## Scoring Dimensions (each integer 0-10)

- **attention** — Scroll-stopping power. Would this persona pause on this content, or scroll right past?
  Visual hook strength, first-impression impact, novelty vs banner blindness.
- **relevance** — Content-persona fit. Does the content speak to this persona's actual needs, life stage, or interests?
  Product category match, lifestyle alignment, timing relevance.
- **emotional_resonance** — Emotional activation intensity. Does this content make this persona feel something?
  Any emotion counts (excitement, nostalgia, frustration, desire, humor, fear). Neutral/flat = low score.
- **persuasion** — Persuasive strength of the value proposition and call-to-action.
  Offer clarity, social proof, urgency, price appeal, credibility, uniqueness vs alternatives.
- **brand_fit** — Platform and audience appropriateness. Does the content look/feel native and trustworthy?
  Production quality, tone, visual style vs platform norms, professionalism.
- **clarity** — Message comprehension speed. How instantly is the point understood?
  Visual hierarchy, text readability, CTA obviousness, information density.
```

Anchor every dimension with these worked examples, framed as "for a {platform} {format}
creative" (lowercased; degrade to platform-only or "this content type" if unset):

```
attention:          0 "No hook at all; static and easy to ignore."
                    3 "Slightly noticeable, but mostly scroll-past."
                    5 "Solid opener that gets a brief pause from average users."
                    7 "Pattern-breaking opener that reliably interrupts scrolling."
                   10 "Exceptional opener with immediate stop-and-look behavior."
relevance:          0 "Feels unrelated to this persona's needs or context."
                    3 "Weak audience fit; only a small overlap with interests."
                    5 "Reasonable fit for a broad segment of this audience."
                    7 "Strong fit to pains, goals, or life-stage context."
                   10 "Near-perfect fit; feels designed exactly for this persona."
emotional_resonance: 0 "Emotionally flat; no meaningful reaction."
                    3 "Minor feeling, but quickly forgotten."
                    5 "Noticeable emotional response, moderate intensity."
                    7 "Strong emotional pull that supports engagement."
                   10 "Very strong emotional activation and memorability."
persuasion:         0 "No convincing reason to act; weak or absent CTA."
                    3 "Some intent to persuade, but doubts dominate."
                    5 "Average persuasive case; might work for some users."
                    7 "Compelling value proposition with credible reasons to act."
                   10 "Exceptional persuasive clarity; action feels obvious."
brand_fit:          0 "Feels off-brand or unnatural for the channel."
                    3 "Partially aligned, but with clear style/tone mismatches."
                    5 "Acceptable quality and tone for this channel."
                    7 "Strongly native feel for the platform and audience."
                   10 "Looks and feels perfectly native and trustworthy."
clarity:            0 "Confusing message; unclear what the user should do."
                    3 "Partly understandable but effortful to parse."
                    5 "Average clarity; main message is understandable."
                    7 "Clear hierarchy and easy-to-grasp next step."
                   10 "Instant comprehension with crystal-clear next action."
```

Write the six integers into each reaction's `scoring` object in `reactions.json`. Every value
must be an integer in [0,10] and every persona covered. If a persona somehow can't be scored
(dropped from a retried batch, corrupt profile), use POPJAM's conservative fallback rather than
guessing — `{attention: 2, relevance: 2, emotional_resonance: 2, persuasion: 2, brand_fit: 3,
clarity: 3}` — and note it in `log.md`.

## Deterministic scoring — run the script, don't do the math

`engagement_score` is deterministic math, not judgment: platform-specific dimension weights
(TikTok leans attention, Google leans relevance+clarity), times content-type multipliers
(email boosts attention+persuasion), adjusted per persona traits (design_appreciation boosts
brand_fit weight, risk_aversion *lowers* persuasion weight), renormalized, dotted with the six
scores, scaled to 0–100. Never let an LLM — including yourself — compute or "estimate" this
number; determinism is what makes scores comparable across concepts and rounds.

```
python <skill-dir>/scripts/score.py score --reactions simulations/<id>/reactions.json --personas personas/<aud-slug> --platform TIKTOK --subject-type AD
```

`--platform` is one of FACEBOOK, INSTAGRAM, TIKTOK, GOOGLE, YOUTUBE, LINKEDIN, TWITTER, REDDIT
(omit for default weights); `--subject-type` is one of AD, POST, BLOG, EMAIL, PRESENTATION.
This fills `engagement_score` (0–100) per reaction in place. Then aggregate:

```
python <skill-dir>/scripts/score.py aggregate --reactions simulations/<id>/reactions.json --out simulations/<id>/insight.json
```

This pre-fills the insight's calculated fields: sentiment counts, mean `engagement_score`,
`dimension_averages`, and `consensus_level` (High if the dominant sentiment covers ≥ 0.7 of
the panel, Medium if ≥ 0.4, else Low).

## Writing the insight narrative

Open the pre-filled `insight.json` and fill **only** the narrative fields: `summary_text`,
`top_feedback_themes`, `recommended_actions`. Preserve every calculated field byte-for-byte —
POPJAM's validator force-restores them after the LLM pass; you enforce the same rule by never
editing them.

Adapted from POPJAM's insight agent:

```
Review the individual reactions by personas to the content and ruminate about their reasoning.
You are provided with pre-calculated metrics (sentiment counts, engagement_score, and per-dimension scoring averages).

## Your tasks

1. Fill `summary_text` with a concise summary that captures all key points from the reactions.
   Reference the scoring dimensions (attention, relevance, emotional_resonance, persuasion,
   brand_fit, clarity) to explain WHY the content performed as it did — averages are on a 0–10
   scale, e.g.: "The content scored well on attention (5.2 avg) due to its bold visuals, but
   struggled with persuasion (1.8 avg) as most personas found the value proposition unclear."
   Do NOT invent or estimate numeric dimension scores that are not in the input.

2. Fill `top_feedback_themes` with commonly mentioned themes from the reactions.

3. Fill `recommended_actions` with confident, specific actions based on the insights.
   The recommended actions should tie back to the weakest scoring dimensions to suggest targeted improvements.

You are provided with a pre-filled insight object — preserve all its calculated fields
(counts, engagement_score, dimension_averages) and fill only the narrative fields.
```

Before writing, identify the weakest and strongest dimensions from `dimension_averages` (POPJAM
renders these as `→ Weakest: {dim} ({value})` / `→ Strongest: {dim} ({value})`) — the weakest
dimension is what the next variant round must attack. If the concept has an image, look at it
again while writing the summary. Then regenerate `leaderboard.md`, append a `log.md` entry, and
hand the insight to the iteration phase (variants implement `recommended_actions` with
`og_id` lineage).

## Optional: research-panel questions

When a strategic question needs answering before (or instead of) a full creative round — "which
of these two hero images?", "what would stop you from buying?" — run the panel as a survey.
QuestionType is one of **OPEN | MULTIPLE_CHOICE | AB_TEST**.

Adapted from POPJAM's questionnaire agent, for designing the questions:

```
You are a user/market research agent that generates questionnaires.

# Rules
- Consider the website content, research and campaign brief to prepare the questionnaire.
- If a target is provided, consider the target's preferences and needs.
- Try to figure out blind spots, preferences, and potential issues with the planned campaign.

# Question types
- Use a mix of question types where appropriate: `OPEN`, `MULTIPLE_CHOICE`, `AB_TEST`.
- For every `MULTIPLE_CHOICE` question you MUST populate `options` with at least 2 distinct,
  mutually exclusive answer choices written as plain text.
- For every `AB_TEST` question you MUST populate `options` with at least 2 variant references.
- For `OPEN` (free-text) questions leave `options` empty (null).
```

Adapted from POPJAM's answer agent, for role-playing the answers (same ≤10-persona batching and
Workflow fan-out as reactions; fan out over questions concurrently when there are several):

```
You are simulating how specific personas would respond to a question.
Respond AS IF YOU WERE EACH PERSONA answering the question.
You MUST provide exactly one answer for every persona provided. Do not skip any personas.

# Persona Consideration
For each persona, consider:
- Their background, age, interests, personality and behavioral traits
- How their life experiences would shape their perspective
- Their communication style and level of detail they'd provide
- Their confidence in their answer based on their knowledge/experience
- The sentiment of their response (positive, neutral, negative)

# Response Guidelines
- Set confidence (0.0-1.0) based on how certain the persona would be
- Use sentiment: 'Positive', 'Neutral', or 'Negative'
- Provide clear reasoning for each response
- Make each response unique to that persona's perspective
```

Per-type mechanics (inject only the relevant block):

- **MULTIPLE_CHOICE** — select the option(s) that best represent each persona's choice, explain
  why over the others, fill `selected_options` with 0-based indices.
- **OPEN** — thoughtful answer in the persona's voice; `selected_options` stays null.
- **AB_TEST** — variants are labeled A, B, C…; **actually Read each image variant** before
  comparing (same rule as creatives — never judge a described image). Compare all variants
  systematically; `selected_options` are 0-based (Variant A = 0); reasoning must name the
  chosen letter ("Selected Variant B because…").

Aggregate deterministically (same shape of math score.py uses): sentiment counts,
`selected_option_counts[i] += 1` per selection, and
`consensus_level = max(positive, neutral, negative) / total` → High ≥ 0.7, Medium ≥ 0.4, else
Low. Then summarize: key points in `summary_text`; always fill `top_themes` and
`unique_insights`; for choice questions analyze the option distribution and why personas chose
as they did (the summary must include `selected_option_counts`); for open questions surface
recurring themes, surprising viewpoints, and consensus vs disagreement. Save under
`questions/<q-slug>/` (question.json, answers.json, summary.json — shapes in
[data-models.md](data-models.md)) and log the decision the answers informed.

## Provenance

Stamp every `reactions.json` and `insight.json` with `provenance: {model, date}` — the model
that role-played/scored and the run date. Scores from different models (or the same model
months apart) are not directly comparable; flag any leaderboard ranking that mixes provenance
so a "winner" isn't just a model-drift artifact. When re-simulating an old concept on a new
model, write a fresh dated run instead of overwriting the old files.
