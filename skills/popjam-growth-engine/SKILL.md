---
name: popjam-growth-engine
description: >-
  Run POPJAM's full ad-creation pipeline end to end: research a brand and its products from a
  single website URL, discover and rank target audience segments, synthesize a bias-corrected
  synthetic persona panel (an AI user-research panel), strategize ad angles and hooks per
  audience and platform, generate real ad creatives (images/video via Higgsfield MCP, Remotion
  animations), simulate every persona's reaction with deterministic engagement scoring, and
  iterate variants until the highest-leverage audience + creative combination emerges. Use this
  whenever the user wants ads, ad creatives, marketing campaigns, campaign strategy, audience
  research, target segments, customer personas, ad testing/validation, or creative iteration
  for a brand, product, or website — "make ads for X", "who is my target audience", "test this
  ad concept", "which segment should we scale", "build me a persona panel" — even if they never
  mention POPJAM, and even if they only give you a URL.
---

# POPJAM Growth Engine

Turn one website URL into tested ad creatives with evidence about *who* converts and *why*.
This skill re-implements POPJAM's production pipeline as agent instructions: the same data
contracts, the same prompts that carry quality, the same deterministic scoring — but running
entirely in this session, persisting to files instead of a database.

The loop: **research → audiences → personas → strategy → media → simulate → iterate**. Each
phase has a reference file with the distilled production logic; read it when you enter the
phase, not before. Phases build on files, so a run can stop anywhere and resume later.

## Campaign state (the contract everything shares)

All state lives in one campaign directory — default `growth/<brand-slug>/` under the project
root, created at start (ask only if a plausible dir already exists elsewhere):

```
growth/<slug>/
├── brand.json  products.json  research.md  brief.md      # phase 1
├── audiences/<aud-slug>.json                             # phase 2
├── personas/<aud-slug>/<persona-slug>.json               # phase 3
├── strategy/<aud-slug>-angles.json                       # phase 4
├── concepts/<concept-id>.json                            # phase 4 (variants: -v2 + og_id)
├── creatives/<concept-id>/                               # phase 5 (real assets only)
├── simulations/<concept-id>/reactions.json, insight.json # phase 6
├── leaderboard.md                                        # regenerated after each sim round
└── log.md                                                # append-only decision journal
```

Every JSON shape is defined once in [references/data-models.md](references/data-models.md) —
read it in full before writing any state file, and keep enum values byte-exact (they feed the
scoring script). If the campaign dir already has files, read `log.md` + the newest state first
and continue from where the last run stopped instead of regenerating.

## Phase map

| Phase | Read | Produces |
|---|---|---|
| 1. Research | [research.md](references/research.md) | brand.json, products.json, research.md, brief.md |
| 2. Audiences | [audiences.md](references/audiences.md) | audiences/*.json (2 default, 3-5 tournament) |
| 3. Personas | [personas.md](references/personas.md) | personas/<aud>/*.json (10/audience default) |
| 4. Strategy | [strategy.md](references/strategy.md) | strategy/*-angles.json, concepts/*.json |
| 5. Media | [higgsfield-media.md](references/higgsfield-media.md) or [remotion-animations.md](references/remotion-animations.md) | creatives/*, concept media blocks |
| 6. Simulate | [simulation.md](references/simulation.md) | simulations/*, leaderboard.md |
| 7. Iterate | [iteration.md](references/iteration.md) | variant concepts, updated leaderboard, log.md verdicts |

Users rarely ask for "phase 4" — they ask for outcomes. Map the ask to an entry point: "make
ads for URL" → run everything; "who's my audience" → stop after phase 3 and report; "test
this ad" → build minimal state (brand + one audience + panel) and jump to 6; "make this ad
better" → 6 then 7. When starting from a URL, ask up front (one message) only what research
can't infer: campaign goal, target market/language if ambiguous, platform preferences, and
whether media spend is okay this session. Then stop asking and run.

## Cross-cutting invariants (these are what make it POPJAM and not vibes)

1. **Grounding is a hard rule.** Never invent statistics, user counts, awards, social proof,
   prices, discounts, or operational promises not present in researched inputs. POPJAM's own
   evals hard-fail this; treat it the same in every phase.
2. **The LLM never computes engagement scores.** Personas rate six 0-10 dimensions; only
   `scripts/score.py` turns them into 0-100 scores and aggregates insights. If you catch
   yourself writing an engagement_score by hand, stop and run the script.
3. **Simulation is two-stage** — in-character role-play first (labels + feedback, no
   numbers), cold rubric scoring second. Collapsing them inflates scores.
4. **Visual concepts are never simulated without their media.** Judge the actual image (Read
   the file), not the media_description. Text-format concepts simulate on copy alone.
5. **Comparability**: variants re-simulate against the *same* persona panel; note it in the
   insight when the panel or model changed (drift), because those scores aren't comparable.
6. **Honest media or no media.** Real generations via Higgsfield MCP (discover via ToolSearch),
   real renders via Remotion. If the tooling is missing, say so and deliver strategy +
   simulation on text concepts — never describe an asset as generated when it wasn't.
7. **Money has gates.** Preflight generation cost (`get_cost:true`), announce the batch plan
   once per phase, default text-first: media credits go to concepts that survived a
   simulation round, not to exploration.
8. **Language split**: ad copy in the brand's language (BCP-47 from brand.json);
   `media_description` and all media prompts always in English.
9. **Leave a trail.** Append every phase decision and verdict to `log.md` — the next session
   (or the next person) starts warm.

## Scale and orchestration

Fan out with the Workflow tool when the work is parallel and sizable; stay inline when small:

- Persona reactions beyond ~2 concepts × 10 personas → adapt
  [workflows/simulate-panel.md](workflows/simulate-panel.md).
- Trying 3-5 audience segments end-to-end ("find my best segment") → adapt
  [workflows/audience-tournament.md](workflows/audience-tournament.md): parallel text-only
  loops, then media only for surviving segments.
- Research fan-out (many competitor pages) → parallel Explore/general agents are fine; no
  template needed.

Batch personas ≤10 per simulation pass (larger batches degrade per-persona fidelity). Keep
total concepts per round ≤12.

One hard rule about *how* to fan out: use the Workflow tool or run inline/sequentially —
never spawn self-managed background subagents or arm monitors and stop to wait for them.
In eval runs, every stall came from an agent ending its turn waiting on background children
that couldn't wake it; inline execution and Workflow-orchestrated fan-outs finished unaided.

## Deliverable

End every run with a summary the user can act on: leaderboard (concepts × audiences with
scores and bands), the winning segment + angle and *why* (cite persona feedback themes and
dimension averages), real creative files for the winners, and the recommended next test. The
evidence lives in the campaign dir; the summary makes it legible.
