# Creative & media generation via Higgsfield MCP

Read this when a concept with a visual format (IMAGE, VIDEO, SHORT) needs real media —
after strategy is approved, before simulation. ANIMATION-format concepts go through
[remotion-animations.md](remotion-animations.md) instead. Simulation of a visual concept is
refused until its media exists (see [simulation.md](simulation.md)), so this phase gates the loop.

## Discovering the tools

Higgsfield's MCP tool names carry a session hash prefix (`mcp__<hash>__generate_image`), so
discover them with ToolSearch (keyword: `higgsfield`, or `generate_image`, `models_explore`)
— never hardcode names. If nothing matches, the server isn't connected: stop and tell the
user to add it (`claude mcp add --transport http higgsfield https://mcp.higgsfield.ai/mcp`,
or via claude.ai connector settings). **Never fake this phase** — a described-but-not-generated
image poisons every simulation downstream.

The surface you'll actually use:

| Tool | Use |
|---|---|
| `models_explore` | `action:'recommend'` with your goal, `action:'get'` for a model's aspect ratios, durations, media roles. Check before first use of any model. |
| `media_import_url` | Import an HTTPS image/video into Higgsfield storage → `media_id`. **`medias[].value` takes media_ids/job_ids, never raw URLs** — import brand/product refs first. |
| `generate_image` | `params:{model, prompt, aspect_ratio, count 1-4, medias:[{value, role}]}`. |
| `generate_video` | Same shape plus `duration`; video jobs are async — poll rather than serialize. |
| `show_marketing_studio` | Product/webproduct/brand-kit library. `action:'fetch'` with a URL scrapes a product or whole brand kit server-side — a strong accelerator for the research phase. |
| `job_display`, `show_generations` | Re-inspect past generations; job_ids are reusable as `medias[].value` for iteration. |
| `upscale_image`, `remove_background`, `reframe`, `outpaint_image` | Post-processing for placement adaptation. |
| `virality_predictor` | Optional pre-simulation signal on finished video creatives. |
| `balance` / `show_plans_and_credits` | Credit state; pair with `get_cost:true` preflights. |

Model defaults (verify with `models_explore` if in doubt): **`marketing_studio_image`** for
commercial/product ad images (call it "DTC Ads" when talking to the user — never say
`ms_image`); `soul_2` for realistic people/UGC/portraits; `nano_banana_pro` for 4K or
text-heavy/diagram images. Video: **`marketing_studio_video`** for product ads;
`kling3_0_turbo` for fast text-to-video; `seedance_2_0` when identity consistency matters.
If a tool result includes a `recovery_tool`, call it immediately — don't explain or ask first.

## Cost discipline

Generation spends the user's real credits, and POPJAM's own pipeline spends credits *before*
generating (refunds on failure) — treat every call as paid. Preflight batches with
`get_cost:true`, state the plan once per phase ("6 images across 3 concepts, ~N credits"),
then proceed. Default to images for exploration rounds; reserve video for concepts that
survived at least one simulation round. One hero asset per concept per placement — persona
count never multiplies media.

## Authoring media prompts (the imgen discipline)

The concept's `media_description` is the brief — written like a creative director, always in
English even when ad copy is localized. Expand it into the generation prompt with:

1. **Subject & action** — the one thing a viewer must parse in <1s, serving the hook.
2. **Brand context** — exact product name and physical details from products.json, brand
   palette/typography adjectives from brand.json.
3. **Composition** — framing, camera, and negative space reserved for copy overlay (state
   where: "upper third clear for headline").
4. **Style & mood** — matched to the audience segment's aesthetic; a gen-z TikTok segment
   and a LinkedIn B2B segment must not share style words.
5. **Aspect ratio per placement** — 1:1/4:5 feed, 9:16 story/reels/TikTok, 16:9 YouTube.
   Generate per-placement (or `reframe` afterwards); don't crop blind.
6. **Text policy** — models still mangle typography: ≤3 words of on-image text, or generate
   a clean plate and overlay copy in Remotion/HTML.

**References first.** Import the product image and logo from research
(`media_import_url` on each URL, cache the returned media_ids in the concept's media block)
and pass them in `medias` with roles from `models_explore`. A reference-grounded generation
is the difference between "a cold brew can" and *your* cold brew can. For iteration rounds,
pass the original creative's job_id as reference — variant mode builds on the winning visual
instead of rerolling from scratch.

## Logo fidelity — the known failure

Generation models redraw logos — POPJAM measured only ~30% faithful reproduction, and its
judge's rule is: *a redrawn logo — even if it resembles the brand — is a failure.* So:

- Prefer compositing: generate the scene without the logo, overlay the real logo file
  afterwards (Remotion layer or ImageMagick), especially for anything customer-facing.
- If the logo was generated in-image, actually look at the result (Read the image) against
  the real logo file and record `logo_ok: true/false` in the concept's media block. When
  uncertain, treat it as altered.

## Persisting results

Download every accepted asset into `creatives/<concept-id>/` and update the concept JSON's
media block: `{url, path, aspect_ratio, model, kind, job_id, ref_media_ids, logo_ok}`.
Simulation shows personas the actual local file — a dangling URL breaks the loop.
