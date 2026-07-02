# Phase 7 — Iteration: variants, learning, and the audience tournament

Read this when you have at least one completed simulation (`simulations/<concept-id>/insight.json`
exists) and you're deciding what to do next: spin improved variants of a concept, feed accumulated
lessons into fresh generation, rebuild the leaderboard, or run the full audience tournament to find
the segment worth scaling. This phase is where the pipeline stops being a generator and becomes an
optimizer — every decision it produces gets appended to `log.md` so the next session starts warm.

## The loop at a glance

```
insight.json ──► variant mode (1–5 variants) ──► regenerate media ──► re-simulate SAME panel
     │                                                                        │
     │                                                                        ▼
     └────► learning mode (fresh concepts, audience memory) ◄──── leaderboard.md (regenerated)
                                                                              │
                                                                              ▼
                                                              kill / iterate / scale decision → log.md
```

## 1. Variant loop mechanics

### Generating variants

There is no separate "variant agent". A variant is the same generation prompt you used in Phase 4
(see [strategy.md](strategy.md) for the full prompt, including the verbatim variant-mode section)
re-run with two extra attachments:

1. **The original creative as source** — its platform, format, headline, body, media_description,
   call_to_action, plus the actual media file from `creatives/<concept-id>/`, framed as a
   `<source_content>` block. POPJAM calls this the Stimulus view of the original.
2. **The insight** — the full contents of `simulations/<concept-id>/insight.json` as an
   `<insights>` block, so the variant task can target the weakest scoring dimensions and implement
   `recommended_actions`.

Generate 1–5 variants per round (POPJAM's flow caps at 5; default to 1–2 — each visual variant
costs a media generation). Keep the wording POPJAM hard-codes into the variant task, because it is
what separates a variant from a lazy paraphrase:

- With insights: create variants "that address the feedback in `<insights>` while preserving its
  strengths. Implement the recommended actions from the insights (not necessarily all of them in a
  single variant)." Split the recommended actions across variants — one fix per variant tells you
  which fix moved the score.
- Without insights (exploratory variants): "explore a new creative direction while preserving its
  core message and strengths. Each variant MUST be meaningfully different from the original — do
  not merely restate it."

Hold platform and format constant unless the insight explicitly indicts them (e.g. brand_fit
feedback says the creative feels non-native to TIKTOK) — changing the creative AND the placement in
one round makes the score delta unattributable.

### Lineage: og_id and reasoning

Every variant is a full concept file with lineage fields. `con-hustle-01` spawns
`concepts/con-hustle-01-v2.json` with `og_id: "con-hustle-01"`; if you later iterate on v2, the
child is `con-hustle-01-v3` with `og_id: "con-hustle-01-v2"` — og_id always points at the immediate
source, so the chain reconstructs the whole lineage. Field shapes: see
[data-models.md](data-models.md).

`reasoning` is mandatory on every variant — POPJAM's validator rejects variants without it. Write
it the way the prompt demands: explain how this variant "differs from and improves on the
original", naming the dimension or feedback theme it targets ("original scored 2.1 on persuasion;
this variant leads with the concrete price instead of the lifestyle claim"). Six rounds from now,
`reasoning` is the only record of what each experiment tested.

Variants inherit the original's `product_ids`, audience, angle, and hook unchanged — they are the
controlled variables of the experiment.

### Regenerating media for visual variants

If the original has media (format IMAGE, VIDEO, SHORT, or ANIMATION), the variant's
`media_description` must "build on the original visual and evolve it — do not start from a blank
slate" (verbatim from POPJAM's variant prompt). Concretely:

- Pass the original asset from `creatives/<concept-id>/` as a **reference image** to the Higgsfield
  generation call (image-to-image), so the variant visibly descends from the original instead of
  rolling a new random composition. Full media procedure: [higgsfield-media.md](higgsfield-media.md).
- Write the new `media_description` (always English) as a delta on the original: what stays, what
  changes, and why the change addresses the insight.
- Download the result to `creatives/<concept-id>-vN/` and fill `media` in the variant JSON,
  including a fresh `logo_ok` check — regeneration re-rolls the logo-fidelity dice.

Never simulate a visual variant whose media doesn't exist yet. POPJAM hard-refuses simulation of
visual content without a media file ("is_awaiting_media") because personas must react to the actual
pixels, not the description. TEXT-format variants skip this step entirely.

### Re-simulating for comparability

Re-run the simulation from [simulation.md](simulation.md) against the **same persona panel** the
original faced — same files under `personas/<aud-slug>/`, nobody added or removed. The variant's
score is only meaningful as a delta against the original, and the delta is only clean if the judges
are identical. Then score and aggregate deterministically:

```
python <skill-dir>/scripts/score.py score --reactions simulations/<id>/reactions.json --personas personas/<aud-slug> --platform TIKTOK --subject-type AD
python <skill-dir>/scripts/score.py aggregate --reactions simulations/<id>/reactions.json --out simulations/<id>/insight.json
```

`score` fills `engagement_score` (0–100) per reaction in place using POPJAM's platform weights ×
content-type multipliers × persona-trait adjustments; `aggregate` pre-fills the insight's
calculated fields (sentiment counts, mean engagement_score, dimension_averages, consensus_level).
You fill ONLY the narrative fields afterwards. Use the variant's own platform and subject_type —
they should match the original's if you held them constant.

For 1–2 variants, run generation → media → simulation sequentially. For a full round across
several concepts or audiences, orchestrate with the Workflow tool — script templates live in the
skill's `workflows/` dir — batching persona reactions ≤10 per call as always.

## 2. Learning mode — audience memory for fresh generation

Variants improve one creative; learning mode improves the *next batch* of fresh concepts. When
generating new concepts for an audience that already has simulation history, inject an audience
memory section. Collect up to **5 most recent insights for the same audience AND same
subject_type** (an audience's reaction to ads says little about its reaction to blog posts), digest
each to `{engagement_score, sentiment: {positive, neutral, negative}, resonated:
top_feedback_themes, recommended_actions, summary: summary_text}`, and wrap them as
`<past_simulation_insights>`. Then add, adapted from POPJAM's learning prompt section:

```
# Audience Memory — Lessons from Past Simulations
This audience has reacted to earlier advertising creatives in prior simulations. Use these aggregated lessons to inform the new work: lean into what resonated, avoid recurring failure points, and apply the recommended actions — WHILE still exploring fresh, original angles. Do NOT merely copy past winners; treat this as accumulated taste, not a template.
{past_simulation_insights XML}
```

(Substitute the subject label for other content types: "social media posts", "blog articles",
"marketing emails", "presentation decks".)

Additionally attach real creative images as visual references: rank the collected insights by
engagement_score, take the **top 2 and bottom 1** IMAGE creatives from `creatives/`, and attach
each to the generation prompt with POPJAM's exact labels:

- `High-performing past creative (engagement {score}/100) — emulate what works here:`
- `Low-performing past creative (engagement {score}/100) — avoid these visual patterns:`

The negative example matters as much as the positive ones — it is the only channel through which
"stop doing the thing that keeps failing" reaches the visual side of generation.

Variant mode and learning mode are exclusive per run: a source creative means variant mode;
otherwise, insights (if any) mean learning mode. Never stack both.

## 3. The leaderboard — `leaderboard.md`

Regenerate `leaderboard.md` from scratch after every simulation round — it is derived state, never
hand-edited (decisions go in `log.md` instead). Build it by reading every
`simulations/*/insight.json` plus the concept files for lineage.

**Ranking.** Sort concepts by mean insight `engagement_score` descending; break ties by most
recent simulation first (POPJAM's exact rule: descending engagement, recency tiebreak). Group by
audience so segment comparisons read at a glance.

**Engagement bands** (POPJAM's canonical thresholds — use these words):

| Score | Band |
|---|---|
| ≥ 90 | exceptional |
| ≥ 75 | strong |
| ≥ 60 | good |
| ≥ 40 | average |
| < 40 | poor |

The 3-band traffic light for quick reads: ≥75 high (green), 40–74 medium (yellow), <40 low (red).
Anchor expectations: honest simulations of first-round concepts mostly land 40–74. A 90+ on round
one deserves suspicion (sycophantic panel?) before celebration — check the persona spread.

**Per-concept row.** id (with lineage, e.g. `con-hustle-01-v2 ← con-hustle-01`), audience, angle,
platform, format, band + score, sentiment split (Positive/Neutral/Negative counts), round number,
and score delta vs its og_id parent for variants.

**Persona heat matrix.** Below the ranking, pivot persona × concept per audience: each cell shows
that persona's `engagement_score` and engagement label (`Will Click`, `Might Click`, `No Interest`)
from `reactions.json`; missing cells (persona not simulated) render as `—`. This is the WHO view:
a concept averaging 55 might be a flat 55 across the panel (weak everywhere) or a split of 85s from
the price-sensitive personas and 25s from the rest (a sharp sub-segment signal worth its own
audience). Averages hide this; the matrix is where sub-segments are discovered. If you render an
HTML view, POPJAM's heat intensity is `alpha = 0.18 + (clamp(score, 0, 100) / 100) × 0.67`,
colored green/red/amber by Positive/Negative/Neutral sentiment.

**Drift warnings.** Comparability across rounds is best-effort, so surface it honestly, exactly as
POPJAM badges it:

- *Panel drift* — the persona set in `reactions.json` no longer matches the current files in
  `personas/<aud-slug>/` (count or slugs differ): flag the row "roster has since changed". Old
  scores came from a different jury.
- *Mixed versions* — reactions carry provenance (model, prompt label, date; see
  [data-models.md](data-models.md)); if the concepts being compared have more than one distinct
  model/version, flag "mixed model versions — scores may not be directly comparable". When a
  drifted comparison would drive a kill/scale decision, re-simulate the older concept against the
  current panel first instead of deciding on stale numbers.

## 4. The audience tournament

The end-goal is not the best single ad — it is the **highest-leverage audience segment**: the one
whose scores are high, whose variants trend upward, and whose heat matrix shows a coherent
who-converts story. A mediocre ad in a hungry segment beats a great ad in an indifferent one,
because the segment is what you'll spend real media budget on.

**Running it.** Pick 3–5 audience segments (from Phase 3) and run the full loop per segment:
personas → angles → concepts → media → simulate → insight → one variant round → re-simulate. This
is the largest fan-out in the skill — orchestrate it with the Workflow tool using the template at
`workflows/audience-tournament.md`, which runs segments concurrently and keeps persona batches ≤10.
For a small tournament (2–3 segments, 1–2 concepts each) sequential execution is fine and easier to
debug.

**Decision rules after each round** — record every verdict in `log.md`:

- **Kill** a segment whose *best* concept is still poor (< 40) after one variant round. One round
  of targeted fixes is enough signal: if implementing the insight's recommended actions can't lift
  the ceiling above 40, the problem is segment-message fit, not execution. Don't spend more media
  credits proving it. (Check the heat matrix first — if a sub-cluster of personas scored high,
  spin that cluster off as a new, narrower audience instead of a pure kill.)
- **Iterate** segments in the middle (best concept 40–74, or trending up): run another variant
  round on the top 1–2 concepts, implementing the next recommended actions. Rising deltas
  (v2 > original) are the strongest buy signal — momentum means the insights are diagnosing real,
  fixable problems.
- **Scale** the segment whose concepts hit strong (≥ 75) or whose variant trend is steepest:
  generate fresh concepts with learning mode ON to widen coverage of angles, upgrade the winning
  concept's format (IMAGE → SHORT or VIDEO — see [higgsfield-media.md](higgsfield-media.md)), and
  present it to the user as the recommended segment with the leaderboard as evidence.

**Stopping criteria.** Stop iterating a concept after **2 consecutive rounds without score
improvement** — variant returns diminish fast once the obvious fixes are implemented, and further
rounds mostly reshuffle noise. Retire it (keep the files; they still feed learning mode as
negative/neutral examples) and redirect effort to fresh concepts or a different segment. Stop the
tournament itself when one segment is clearly ahead and stable across two rounds, or when every
surviving segment has plateaued — at that point produce the final recommendation rather than
another round.

## 5. The decision journal — `log.md`

Append (never rewrite) one entry per decision, at minimum: date, action (generated / simulated /
variant round / killed / scaled / retired), the concept and audience ids involved, the score
evidence ("con-hustle-01: 48 → v2: 61, persuasion 2.1 → 5.4"), and one line of why. A future
session should be able to read `log.md` + `leaderboard.md` and resume the tournament without
re-deriving a single decision — which segments are dead and why, which concepts are retired, what
the next planned round was. Write the entry immediately after each decision, not batched at the
end; a crashed session with a warm log loses nothing.
