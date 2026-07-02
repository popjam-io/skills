# Persona panel generation (Phase 3)

Read this when audiences exist in `audiences/` and you need the synthetic consumer panel
that will react to ads in the simulation phase. Each audience gets its own panel (default
10 personas), persisted one file per persona to `personas/<aud-slug>/<persona-slug>.json`.
Panel quality is simulation quality: a sycophantic panel praises every concept and the
leaderboard learns nothing, which is why the bias-correction block below is the single most
important prompt in this skill.

## Reuse the panel before regenerating

In POPJAM, personas (like their audiences) are org-owned and shared across campaigns — the
same panel reacts to many campaigns so scores are comparable over time. Replicate that:
before generating, check `personas/<aud-slug>/` in this campaign directory and in sibling
campaigns for the same brand. If a panel already exists for a reused audience, use it as-is
and note the reuse in `log.md`. If you must add or replace personas in an existing panel,
record the roster change — engagement scores from before and after the change are no longer
directly comparable, and `leaderboard.md` should say so (see
[audiences.md](audiences.md), comparability caveats).

## Panel size and batching

Default is 10 personas per audience (POPJAM's request default); anywhere in 5–15 is
reasonable, 50 is the hard cap. Generate the whole panel in **one batched generation per
audience**, never one persona at a time — the bias-correction rules calibrate the *set*
(rule 6 explicitly operates over the collection), and personas generated in isolation
converge on ten copies of the same agreeable optimist.

If the user wants a panel larger than 10, generate in batches of at most 10, and feed each
subsequent batch a compact summary of the personas already generated so set-level
calibration still spans the full panel — one line each, e.g.
`Marta Kowalska, 52, warehouse supervisor, Łódź — skeptic, low digital literacy, price-first`.
Tell the later batch explicitly which niches are already covered and which the set still
lacks (skeptics, low-income, rural, older cohorts are the usual gaps).

Across audiences, panels are independent. For the default 2-audience run, generate them
sequentially. For tournament runs (3–5 audiences) or large panels, orchestrate per-audience
generation with the Workflow tool using the script templates in the skill's `workflows/`
directory.

## Ground in public data before inventing distributions

POPJAM feeds deep-research output into persona generation; the file-based analogue is a
quick grounding pass. Before generating a panel, run one or two searches (WebSearch, or the
perplexity MCP if connected) on the segment's real-world shape:

- actual age/income distribution for the named occupations in the named locations,
- platform and device usage for the age band (who is actually on TikTok vs Facebook),
- adoption, skepticism, or churn patterns for the product category.

Anchor the panel's distributions on what you find instead of inventing them — invented
distributions drift toward the idealized defaults the bias block exists to kill. Note the
key stats and sources in `log.md` so a future regeneration can reuse them.

## The generation prompt

Adapted from POPJAM's persona agent:

```
You generate realistic user personas for marketing simulations.
Each persona must strictly match the given target segment (demographics, gender,
interests, etc.).
Include details like name, age, location, occupation, interests, income level,
personality traits, behavioural traits and a brief background bio.
Make sure the info is diverse and realistic, reflecting the target segment's
characteristics while bringing some unique sauce.
Make sure the behavioral attributes mirror a realistic sample of the target segment
in the real world, for the specified locations.
```

Provide as context: the full audience JSON (this is the target segment), `brief.md`, the
relevant parts of `research.md` plus your grounding findings, and `brand.json`. Then apply
the bias-correction block below, and close with the task: "Create {N} personas that fit the
target segment provided." If the brief specifies a campaign language (BCP 47), write all
persona text exclusively in that language.

## Bias correction — the quality core

Apply this block verbatim in every panel generation. It is why POPJAM panels behave like a
population sample instead of a focus group of enthusiastic early adopters.

Adapted from POPJAM's persona agent:

```
# Bias Correction — LLM-generated personas skew positive, progressive, and idealized.
Actively counteract:

**1. Kill the positivity bias.** 60-70% of personas carry realistic struggles,
contradictions, and negative traits: financial constraints, time pressure, tech
frustration, procrastination, poor follow-through. Never a set of uniformly successful,
"passionate"/"dedicated" people. Include conflicting values (e.g. environmentally
concerned but convenience-driven).

**2. Balance worldviews.** Represent the full ideological spectrum in realistic
proportions — traditional, conservative, and economically-motivated viewpoints alongside
progressive ones, and (most commonly) the politically disinterested. Never presume
everyone cares about sustainability or social causes; many prioritize convenience, cost,
family security, and stability, and some are skeptical of corporate
social-responsibility claims.

**3. Match real demographics.** Distributions should mirror the actual population of the
target segment and locations — including limited education, rural backgrounds, lower
socioeconomic status, low digital literacy, and mainstream/lowbrow tastes (reality TV,
pop music, blockbusters). Not an aspirational cross-section.

**4. Model cognitive reality.** Emotional rather than rational decisions, limited
attention, cognitive biases, gaps between stated preferences and actual behavior,
unstable or changing preferences. Specify the current life circumstances (time, budget,
family, work stress) that constrain each persona's behavior.

**5. Anti-sycophancy.** The set must include skeptics: people who would give negative
feedback, prefer a competitor or their existing solution for legitimate reasons, distrust
new technology, or have real privacy/security/complexity concerns and no motivation to
change. Genuine adoption barriers go beyond price.

**6. Calibrate the set.** Each persona must add a genuinely different perspective;
collectively they span socioeconomic, educational, geographic, and attitudinal spectrums
with optimists and pessimists balanced — no demographic or psychographic group
overrepresented.

**7. Ethics.** Realism without harmful stereotypes: respectful representation and
individual dignity across all groups.

When in doubt: realism over idealism, complexity over simplification, diversity over
homogeneity, skepticism over enthusiasm, practical concerns over aspirational goals.
```

## The 12 behavioral floats — anchor them in the archetype

Every persona carries 12 behavioral floats, each 0.0–1.0 (names exact; definitions in
[data-models.md](data-models.md)): `price_sensitivity`, `brand_loyalty`, `novelty_seeking`,
`environmental_consciousness`, `design_appreciation`, `tech_savviness`,
`social_influence_sensitivity`, `risk_aversion`, `convenience_preference`,
`value_orientation`, `emotional_engagement`, `pragmatism`.

These are not flavor text: the deterministic scorer (`scripts/score.py`) applies
persona-trait adjustments to every reaction's engagement score, so wrong floats produce
wrong leaderboards. Anchor them in the audience's 16-trait archetype — a high-`risk`,
high-`discovery` archetype skews the panel toward high `novelty_seeking` and low
`risk_aversion`; a high-`quality`/`order` archetype skews toward high `pragmatism`,
`value_orientation`, and `design_appreciation`. Two rules:

- The **panel mean** should reflect the archetype, but **individual values must spread**
  (roughly ±0.2–0.3 around the mean). Ten personas with identical floats are one persona
  simulated ten times.
- Floats must cohere with the bio. A persona "juggling two jobs to make rent" cannot have
  `price_sensitivity: 0.2`; a self-described skeptic (bias rule 5) needs the floats to back
  it up (high `risk_aversion`, low `novelty_seeking`, or high `brand_loyalty` toward the
  incumbent).

## Deterministic post-processing (outside the prompt)

POPJAM enforces these with output validators and code, not prompt hope. Run them as checks
after generation, before writing files:

1. **Age gate.** If the audience has both `age_min` and `age_max`, every persona's age must
   fall within the range. Regenerate offenders — POPJAM's retry message is literally "Age of
   persona {id} ({age}) is not within the target age range."
2. **Generation tags.** Append the deterministic tag to each persona's `segment_tags` by
   age, then dedupe: age ≤12 → `gen_alpha`; ≤28 → `gen_z`; ≤44 → `gen_y`; ≤60 → `gen_x`;
   ≤79 → `gen_boomer` (80+ gets no generation tag). Compute this yourself — never ask the
   model to.
3. **Audience link.** Set each persona's audience reference to the `aud-slug` yourself
   (POPJAM force-overwrites `audience_id` server-side because models fill it unreliably).
4. **Gender values.** Exactly `MALE`, `FEMALE`, `NON_BINARY`, or `OTHER`.

## Optional avatars

Avatars are cosmetic — useful when presenting the panel to the user, never worth blocking
the pipeline. POPJAM picks DiceBear OpenPeeps avatars in a separate cheap batched call and
falls back to a deterministic random avatar seeded by the persona's name, so looks stay
stable across regenerations. If you add them, store a descriptor object
(`{face, head, skinColor, accessories}`, shape in [data-models.md](data-models.md)) chosen
with the avatar agent's logic:

- `skinColor` → the persona's ethnicity, nationality and location.
- `head` → gender, age and cultural context (e.g. `hijab` / `turban` where fitting, the
  gray styles for older people, `noHair*` / `shaved*` for balding).
- `face` → personality and mood. Prefer natural, realistic expressions and avoid the
  novelty faces (`monster`, `cyclops`, `angryWithFang`) unless the persona is cartoonish.
- `accessories` → leave empty unless a trait clearly calls for eyewear.

The simplest rendering is the seed URL:
`https://api.dicebear.com/9.x/open-peeps/svg?seed=<persona name>` — on any doubt, just use
that and move on.

## Persist and log

Write one file per persona to `personas/<aud-slug>/<persona-slug>.json` (slug from the
persona's name). Full field list — demographics, bio, the 12 floats, `segment_tags`,
optional avatar — is in [data-models.md](data-models.md). Append to `log.md`: which panel
was created or reused, its size, the grounding sources used, and who the designated
skeptics are (naming them keeps you honest when reading simulation results later).

## Interviewing a persona

Beyond batch simulation, personas are useful for ad-hoc qualitative probing — "ask the
skeptics why they'd scroll past this". POPJAM has a dedicated roleplay agent for this;
replicate its stance when the user wants to talk to a persona:

- Assume the persona and reply as them, speaking in first person. You are aware of the
  brand and product being discussed and respond from the persona's perspective — floats
  and bio constrain the answers (a `tech_savviness: 0.2` persona doesn't praise the app's
  API).
- Bring the persona's history: ads they've seen, reactions they've given, questions they've
  answered (read them from `simulations/*/reactions.json`). Use this memory naturally in
  conversation — don't dump it all at once.
- When an ad being discussed has real media in `creatives/<concept-id>/`, actually look at
  the visual before commenting on it — not just the headline and copy.

Log notable interview takeaways in `log.md`; they often seed the next variant round.

## Panel quality checklist (audit the set, not each persona)

Before accepting a panel, verify the collection against the bias rules it was generated
under:

- [ ] 60–70% of personas carry real struggles, contradictions, or negative traits — count
      them, don't eyeball.
- [ ] At least 2–3 genuine skeptics who prefer a competitor or the status quo for
      legitimate reasons.
- [ ] Worldview spread includes traditional/conservative/economically-motivated views and a
      politically disinterested majority — not ten sustainability enthusiasts.
- [ ] Demographics match your grounding search (education, income, digital literacy,
      mainstream tastes), not an aspirational cross-section.
- [ ] Every persona adds a perspective the others don't — if two would react identically to
      every ad, one is dead weight.
- [ ] Floats spread around the archetype-implied mean and cohere with each bio.
- [ ] All ages inside the audience range; generation tags stamped and deduped.

When a check fails, regenerate the specific offending personas and cite the violated bias
rule in the regeneration request — targeted correction beats regenerating a whole panel
that was mostly fine.
