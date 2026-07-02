# Workflow template: audience-tournament

Use this for the "which segment do we scale?" question — running the strategy loop over
3-5 audience segments in parallel to find the highest-leverage one. It parallelizes the
*cheap, text-only* stages (personas → angles → concepts → text-level simulation). Media
generation and vision-based simulation stay in the main conversation afterwards, where you
control Higgsfield spend and only pay for the segments that survived round 1.

Precondition: research phase done (brand.json, products.json, research.md, brief.md exist)
and audience JSONs written (one per segment). Personas may or may not exist yet.

```js
export const meta = {
  name: 'audience-tournament',
  description: 'Full text-loop per audience segment: personas, angles, concepts, panel simulation',
  phases: [
    { title: 'Panel', detail: 'personas per segment (skipped where they exist)' },
    { title: 'Strategy', detail: 'angles/hooks + concepts per segment' },
    { title: 'Simulate', detail: 'role-play + cold scoring per segment' },
  ],
}

// args: {
//   skillDir, campaignDir,
//   audiences: [{ slug, path, personasDir, personaCount,   // personaCount 0 => generate 10
//                 platform, nConcepts }],                  // nConcepts default 2
// }

const CONCEPTS_SCHEMA = { type: 'object', required: ['conceptIds'], properties: {
  conceptIds: { type: 'array', items: { type: 'string' } } } }
const SIM_SCHEMA = { type: 'object', required: ['summaries'], properties: {
  summaries: { type: 'array', items: { type: 'object',
    required: ['conceptId', 'reactionsPath'], properties: {
      conceptId: { type: 'string' }, reactionsPath: { type: 'string' } } } } }

const results = await pipeline(args.audiences,
  a => agent(
    `Campaign dir: ${args.campaignDir}. Audience: read ${a.path}. ` +
    (a.personaCount > 0
      ? `Personas already exist in ${a.personasDir} — verify they load and return "ok".`
      : `Generate the persona panel (10 personas) for this audience following ` +
        `${args.skillDir}/references/personas.md — the bias-correction rules are the quality core. ` +
        `Write each persona JSON into ${a.personasDir} per ` +
        `${args.skillDir}/references/data-models.md. Return "ok".`),
    { label: `panel:${a.slug}`, phase: 'Panel' }),
  (_, a) => agent(
    `Campaign dir: ${args.campaignDir} (read brand.json, products.json, research.md, brief.md). ` +
    `Audience: ${a.path}. Following ${args.skillDir}/references/strategy.md: (1) write the ` +
    `angle/hook map to strategy/${a.slug}-angles.json; (2) generate ${a.nConcepts ?? 2} contrasting ` +
    `TEXT-format concepts for platform ${a.platform} (different angles, not variations of one), ` +
    `written to concepts/ with ids con-${a.slug}-01... per data-models.md. Ground every claim — ` +
    `never invent statistics, prices, or social proof. Return the concept ids.`,
    { label: `strategy:${a.slug}`, phase: 'Strategy', schema: CONCEPTS_SCHEMA }),
  (c, a) => agent(
    `Campaign dir: ${args.campaignDir}. Simulate concepts ${JSON.stringify(c.conceptIds)} against ` +
    `ALL personas in ${a.personasDir}, following ${args.skillDir}/references/simulation.md stages 1 ` +
    `and 2 exactly (role-play first, cold-score second; batches of <=10). Write merged ` +
    `simulations/<concept-id>/reactions.json per data-models.md (engagement_score null — do NOT ` +
    `compute scores yourself), then run: python ${args.skillDir}/scripts/score.py score --reactions ` +
    `<file> --personas ${a.personasDir} --platform ${a.platform} --subject-type AD ; and ... aggregate ` +
    `--out simulations/<concept-id>/insight.json ; then fill the insight narrative fields. ` +
    `Return per-concept reactionsPath.`,
    { label: `simulate:${a.slug}`, phase: 'Simulate', schema: SIM_SCHEMA }),
)
return { segments: results.filter(Boolean) }
```

## After the workflow returns

1. Read every `insight.json`; build `leaderboard.md` per
   [iteration.md](../references/iteration.md) (bands, per-persona heat notes, drift caveats).
2. Apply the tournament rules: kill segments whose best concept lands `<40`; shortlist the
   top 1-2 segments; log the decision in `log.md`.
3. Only now spend media credits: upgrade the shortlist's winning concepts to IMAGE via
   [higgsfield-media.md](../references/higgsfield-media.md), re-simulate vision-based, and
   run the variant loop on the results.

Adaptation points: swap platform per segment when testing placement fit; raise `nConcepts`
to 3 when angles diverge strongly; cap total concepts (segments × concepts) around 12 per
round — beyond that, reaction quality drops faster than coverage gains.
