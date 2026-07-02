# Audience synthesis (Phase 2)

Read this when the campaign directory has `brand.json`, `brief.md`, and `research.md` on disk
and you need to decide WHO the ads target. This phase turns those three inputs into 2–5
distinct audience segments, each persisted to `audiences/<aud-slug>.json`. Audiences are the
pivot of the whole pipeline — personas are generated per audience, strategy angles map per
audience, and the leaderboard ultimately compares results per audience — so a vague or
overlapping segment poisons everything downstream.

## Inputs: brand and positioning, never the product list

Load `brand.json`, `brief.md`, and `research.md` in full. Do **not** load `products.json`
into the segmentation context. POPJAM hard-codes this exclusion:

> Ground targets in the brand and its catalog (name/positioning) — not the individual
> products. Catalogs can hold thousands of products, so loading the full list into the
> prompt is neither feasible nor useful.

Segmentation happens at the level of who the brand serves — price point, category,
positioning — not individual SKUs. If the brief spotlights specific hero products, that
context is already in `brief.md`; the working set comes back into play in the strategy and
concept phases.

## How many segments to generate

| Run type | Segments | When |
|---|---|---|
| Default | 2 | Standard campaign — enough to compare, cheap to simulate |
| Tournament | 3–5 | User asked for a broad sweep or the brief spans clearly different markets |

Never generate more than 5 in one pass (POPJAM clamps requests to 1–5). More segments means
proportionally more personas, concepts, and simulations — each extra audience roughly doubles
the downstream work — so default to 2 unless the user explicitly wants tournament mode.

## Reuse before you regenerate

In POPJAM, audiences are org-owned and reusable: many campaigns link to the same audience so
different campaigns can be simulated against the same panel and compared apples-to-apples.
Replicate that here: before generating, check `audiences/` in this campaign directory and in
sibling campaign directories for the same brand (`growth/<brand-slug>*/audiences/`). If an
existing segment fits the brief, copy or reference it instead of regenerating — you keep its
persona panel too (see [personas.md](personas.md)), which is what makes cross-campaign
comparison meaningful. Record the reuse decision in `log.md`.

## The synthesis prompt

Generate all N segments in one pass, not one at a time — the set is calibrated together, and
the distinctness rule below operates over the whole set.

Adapted from POPJAM's target agent:

```
You define precise target audience segments for marketing campaigns.
Given the campaign brief and website/research content, create detailed targeting
parameters that align with the product/service and campaign goals.

Analyze the brief and research content to determine:
- A description of the target audience for the product/service
- Appropriate age ranges for the target audience
- Relevant genders (if applicable to the product/service)
- Geographic locations where the product/service is available or most relevant
- Occupations that would be interested in or benefit from the offering
- Income levels that match the product's price point and positioning
- Interests and hobbies that align with the product/service
- Personality traits that would be attracted to the brand/offering
- The needs of the target audience in context of the product/service
- A full archetype profile that encapsulates the target audience's characteristics
  and motivation

# Rules
- Each target should be distinct and focused on different audience segments if multiple
  targets are requested.
- Ensure all targeting parameters are realistic and aligned with the product/service
  positioning.
- Consider the product's price point, complexity, and intended use cases when defining
  target demographics.
- Be specific with locations (include cities/countries where relevant), occupations,
  and interests.
- Be specific and realistic - avoid overly broad targeting that would include
  irrelevant audiences.

# Task
Define {N} NEW target segment(s) based on the given data.
If existing audiences are provided, ensure the new segments are distinct and
non-overlapping — target different demographics, psychographics, or use cases.
```

If the brief specifies a campaign language (IETF BCP 47 code), write all audience text
exclusively in that language — POPJAM enforces this as a hard requirement. If the user gave
extra steering (e.g. "skew toward B2B buyers"), honor it as an additional requirement.

## Non-overlap: the dedup mechanic

POPJAM keeps segments distinct not by hoping the model remembers, but by injecting a summary
of every already-existing audience into the request alongside the "distinct and
non-overlapping" demand. Replicate it exactly:

1. For each existing audience (already in this campaign, or reused from a sibling), build a
   compact summary with exactly these fields: `{title, description, needs, interests,
   occupations}`.
2. Include the summaries in the generation request under an `<existing_targets>` block,
   before the task line:

   ```xml
   <existing_targets>
     <target>
       <title>Fitness-focused parents</title>
       <description>Parents 30-45 in suburban US metros balancing family life with...</description>
       <needs>time-efficient workouts; guilt-free self-care; ...</needs>
       <interests>home fitness, meal prep, parenting podcasts</interests>
       <occupations>teachers, nurses, mid-level office workers</occupations>
     </target>
   </existing_targets>
   ```

3. Keep the demand explicit: new segments must differ in demographics, psychographics, or
   use cases — at least one of the three.

Two segments overlap when the same real person plausibly sits in both. "Urban millennials
who value convenience" and "busy young professionals in cities" are one segment wearing two
titles. After generation, check every pair: name the axis (demographic, psychographic, or
use case) on which they differ. If you can't name one, regenerate the weaker segment with
the stronger one summarized as an existing target.

## Required fields: needs and archetype

The full audience JSON shape lives in [data-models.md](data-models.md). Two fields are
validator-enforced in POPJAM (generation is retried until they exist) — treat them the same
way here:

- **`needs`** — what this audience needs in the context of the product/service. This is the
  raw material for strategy angles; a segment without needs gives the strategy phase nothing
  to hook into.
- **`archetype`** — the 16-trait behavioral profile (`elite`, `societal_competition`,
  `authority`, `conformity`, `social_security`, `home`, `benevolence`, `order`, `quality`,
  `individual_order`, `success`, `fight`, `rebellion`, `risk`, `autonomy`, `discovery`),
  each a float 0.0–1.0. Definitions are in [data-models.md](data-models.md). The archetype
  anchors the persona panel's 12 behavioral floats in Phase 3, so it must express a real
  shape: push 3–5 traits meaningfully high and let others sit low. An archetype of all-0.5s
  says nothing and produces a beige panel.

  Example shapes: a premium performance-fitness segment peaks on `elite`,
  `societal_competition`, `success`, and `fight`; a family-safety product's segment peaks
  on `benevolence`, `home`, and `social_security`; an early-adopter developer-tool segment
  peaks on `discovery`, `autonomy`, `risk`, and `quality`. The peaks should read as a
  one-line motivation story, and different segments in the same campaign should peak on
  different traits — if two archetypes look alike, the segments probably overlap too.

When `genders` is relevant, use exactly: `MALE`, `FEMALE`, `NON_BINARY`, `OTHER`. Leave it
unset when the product isn't gendered — forcing genders onto a gender-neutral product is a
segmentation error, not thoroughness.

## Persist and validate

Write each segment to `audiences/<aud-slug>.json` (slug derived from the title, `aud-`
prefix: "Fitness-focused parents" → `aud-fitness-parents`). Append to `log.md`: date, which
segments were created and why, what each deliberately excludes.

POPJAM validates output deterministically and retries on failure; replicate as a post-write
checklist rather than trusting the generation:

- Exactly N segments came back ("Exactly N targets were requested").
- Every segment has an `archetype` ("All targets must have an `archetype`").
- Every segment has `needs` ("All targets must have `needs`").
- Ages are sane: 0 < age < 150, `age_min` < `age_max` when both set.
- Every pair of segments (including reused ones) differs on a nameable axis.

Fix violations by regenerating the offending segment, not by hand-editing plausible-sounding
values — the point of the retry loop is that the model reconciles the whole record.

## Audience-level success criteria

A segment is judged twice: once at synthesis time, once after simulation.

**At synthesis time**, a good segment is specific (named cities and occupations, not
"global professionals"), realistic for the price point (a €999/month product does not
target students), and carries needs the product can honestly claim to meet.

**After simulation**, audiences compete on the leaderboard. The bundled scorer produces the
comparable numbers (see the simulation phase and `scripts/score.py`); the audience-level
aggregates you'll report in `leaderboard.md` are:

- **Engagement** per audience-campaign pairing: the rounded mean of its persona reactions'
  `engagement_score` (0–100).
- **Sentiment split**: counts of `positive` / `neutral` / `negative` reactions.
- **Ranking**: descending engagement score; break ties by most recent activity.
- **Bands** (POPJAM's exact thresholds): ≥90 `exceptional`, ≥75 `strong`, ≥60 `good`,
  ≥40 `average`, else `poor`. Traffic-light view: ≥75 high, 40–74 medium, <40 low.

Two comparability caveats, because reusable audiences have no versioning: if the persona
roster changed between two campaigns' simulations, or the reactions were produced by
different model versions, flag the affected leaderboard rows ("roster has since changed",
"mixed versions — scores may not be directly comparable") instead of ranking them as if the
numbers were commensurable.

A `poor`-band audience is a finding, not a failure — it tells you where the brand's message
doesn't land. Log it and shift creative budget toward the segments that scored `strong` or
better rather than deleting the evidence.

## Scale note

Audience synthesis itself is always a single generation call, whatever N is. The fan-out
begins in Phase 3: persona panels and concepts per audience are independent, so for
tournament runs (3–5 audiences) orchestrate them with the Workflow tool using the script
templates in the skill's `workflows/` directory; for the default 2-audience run, plain
sequential calls are simpler and fast enough.
