# Workflow template: simulate-panel

Use this when the reaction matrix is big enough to hurt — more than ~2 concepts × 10
personas — and the Workflow tool is available. For a couple of concepts against a small
panel, just run the two simulation stages inline per [simulation.md](../references/simulation.md);
orchestration overhead isn't worth it.

The script mirrors POPJAM's fan-out: personas in batches of ≤10, each batch through two
*separate* agents (role-play, then cold scoring — separation prevents narrative-driven score
inflation), no barrier between concepts. Deterministic scoring stays OUTSIDE the workflow:
after it returns, you merge batches, run `score.py score` + `aggregate`, and write the
insight narrative yourself.

Adapt the `args` (paths, concept list, batches) and pass the script to the Workflow tool.
Batch personas yourself before invoking: `personaBatches` = arrays of ≤10 persona file paths.

```js
export const meta = {
  name: 'simulate-panel',
  description: 'Persona panel reactions: role-play then cold-score, per concept x batch',
  phases: [
    { title: 'React', detail: 'stage 1 role-play per concept x persona batch' },
    { title: 'Score', detail: 'stage 2 cold rubric scoring per batch' },
  ],
}

// args: {
//   skillDir: '/abs/path/.claude/skills/popjam-growth-engine',
//   campaignDir: '/abs/path/growth/<slug>',
//   concepts: [{ id, path, platform, subjectType, mediaPath }],   // mediaPath null for TEXT
//   personaBatches: [['/abs/persona1.json', ...(<=10)], ...],
// }

const REACTIONS_SCHEMA = {
  type: 'object', required: ['reactions'],
  properties: { reactions: { type: 'array', items: { type: 'object',
    required: ['persona_id', 'engagement', 'sentiment', 'feedback', 'keywords'],
    properties: {
      persona_id: { type: 'string' },
      engagement: { enum: ['Will Click', 'Might Click', 'No Interest'] },
      sentiment: { enum: ['Positive', 'Neutral', 'Negative'] },
      feedback: { type: 'string' },
      keywords: { type: 'array', items: { type: 'string' } },
    } } } },
}

const SCORED_SCHEMA = {
  type: 'object', required: ['scorings'],
  properties: { scorings: { type: 'array', items: { type: 'object',
    required: ['persona_id', 'attention', 'relevance', 'emotional_resonance',
               'persuasion', 'brand_fit', 'clarity'],
    properties: {
      persona_id: { type: 'string' },
      attention: { type: 'integer', minimum: 0, maximum: 10 },
      relevance: { type: 'integer', minimum: 0, maximum: 10 },
      emotional_resonance: { type: 'integer', minimum: 0, maximum: 10 },
      persuasion: { type: 'integer', minimum: 0, maximum: 10 },
      brand_fit: { type: 'integer', minimum: 0, maximum: 10 },
      clarity: { type: 'integer', minimum: 0, maximum: 10 },
    } } } },
}

const pairs = []
for (const c of args.concepts)
  for (let b = 0; b < args.personaBatches.length; b++) pairs.push({ c, b })

const results = await pipeline(pairs,
  p => agent(
    `Stage 1 of a synthetic-panel simulation. Read ${args.skillDir}/references/simulation.md ` +
    `(Stage 1 section) and follow it exactly. Stimulus: read ${p.c.path}` +
    (p.c.mediaPath ? ` and LOOK at the creative by Reading ${p.c.mediaPath} — judge the visual, ` +
      `not the copy fields.` : ` (text-only concept — judge the copy).`) +
    ` Personas: read each of ${JSON.stringify(args.personaBatches[p.b])}. Role-play EVERY persona ` +
    `(exactly one reaction each, persona_id = the persona's id field): engagement label, consistent ` +
    `sentiment, 2-4 sentence in-character feedback, keywords. No scores — that is a later stage. ` +
    `Platform: ${p.c.platform}. Subject type: ${p.c.subjectType}.`,
    { label: `react:${p.c.id}#${p.b}`, phase: 'React', schema: REACTIONS_SCHEMA }),
  (stage1, p) => agent(
    `Stage 2: cold rubric scoring, temperature-zero mindset. Read ${args.skillDir}/references/simulation.md ` +
    `(Stage 2 anchors) and the stimulus at ${p.c.path}. For each reaction below, assign the six ` +
    `0-10 integer dimensions guided by the anchors, consistent with the persona's stated reaction ` +
    `(a 'No Interest'/Negative reaction cannot score 8s). Reactions: ${JSON.stringify(stage1.reactions)}`,
    { label: `score:${p.c.id}#${p.b}`, phase: 'Score', schema: SCORED_SCHEMA })
    .then(s => ({ conceptId: p.c.id, batch: p.b, reactions: stage1.reactions, scorings: s.scorings })),
)
return { batches: results.filter(Boolean) }
```

## After the workflow returns

For each concept, merge its batches into `simulations/<concept-id>/reactions.json`
(reaction + matching scoring by persona_id, `engagement_score: null`), then:

```bash
python <skillDir>/scripts/score.py score --reactions simulations/<id>/reactions.json \
  --personas personas/<aud-slug> --platform <PLATFORM> --subject-type <TYPE>
python <skillDir>/scripts/score.py aggregate --reactions simulations/<id>/reactions.json \
  --out simulations/<id>/insight.json
```

Then fill the insight's narrative fields per [simulation.md](../references/simulation.md) —
preserving every calculated field — and update `leaderboard.md`.

Sanity checks before trusting results: every persona has exactly one reaction per concept;
any `scoring_fallback: true` entries mean a batch under-delivered — re-run that batch rather
than shipping conservative-default scores.
