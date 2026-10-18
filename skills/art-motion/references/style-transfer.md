# Style transfer: learning a style and moving it to a new subject

> Adapted from huashu-art-motion (MIT, (c) 2026 alchaincyf) - references/15-跨场景风格提炼.md, references/08-风格作者规范.md

Read this when an art style must carry a subject it was never shown with (a product, a service, data), when the brief gives only an artist or studio name, when two neighbouring styles must be told apart, or when designing a style the index does not cover. You learn the visual language; the story, scenes and characters still come from the brief.

## Separate four things

- **Style language**: mark-making and material, colour relationships, light, form, spatial organisation. It must stay recognisable when the subject changes.
- **Compositional tendencies**: off-centre weight, grouping, scale contrast. Re-solve them for the new canvas (9:16, 4:5, 1:1, 16:9) and the new event; never fixed coordinates or one layout for every shot.
- **Content and motifs**: the figures, costumes, bridges, boats, gardens and gods of famous works. They do not come along with the style unless this brief needs them.
- **Narrative and action**: who wants what, what resists, how the action changes things. Pace, camera and beat come from the content: a calm style can carry fast action, and limited animation can carry a complex event.

Choosing an artist is not choosing one famous painting as a template.

## Medium layer vs era and subject motifs

- **Medium layer**: how strokes, material, light and colour are handled. It travels to any subject: a product, a chart, a story. Van Gogh's flowing stroke field, Hopper's hard-edged light blocks, Matisse's cut-paper edges, halftone dots, watercolour tide-lines.
- **Era and subject motifs**: the starry sky and cypress, Hopper's diner, the gold robe. They suit tributes and art-history tours. For a new subject, re-extract the language and drop the motifs. When unsure, treat a trait as medium layer and test it.

## Learn from several works, never one

- Look at **at least 3 different works** (or 3 scenes from different official clips), varied in subject, scale or lighting. Consecutive frames, crops of one painting and recolours of the same composition are not independent samples. If your knowledge is thin, say so in a comment; do not pad or claim to have seen what you have not.
- Write a short **style brief** as a comment next to the shot list:
  1. Scope and sources: which works, period and medium (check attribution).
  2. 3-5 observable, stable traits, each with the works that support it and any that contradict it.
  3. Two differences from the nearest neighbour. Renoir, Pissarro and Sisley cannot share one broken-brush filter and call it done.
  4. This piece's subject, event, space and canvas, rebuilt from the brief, not lifted from a reference.
  5. What visual relationships to keep, what content may change, which technical route is still unproven.
- Record **what is in the picture** separately from **how the painter made it**.
- **Colour**: write the main colour relationships and value organisation. Do not claim a hex set is the artist's canonical palette; 3-6 main colours do not mean every pixel is one of them. Texture, mixing, shadows and reflections obey the main relationship. The blue-purple rule in `palettes.md` still applies; exceptions need a subject reason.

## Studios are film-level art direction, not a filter

Ghibli and Pixar do not share one look across their catalogues. Pin a film, director or period first, matched to the brief.

- **Ghibli**: Totoro, Kiki and Spirited Away share hand-painted backgrounds and clear character silhouettes; Kaguya organises line and empty space very differently and does not belong in the same watercolour-background recipe. Transferable research traits: clear silhouettes and key poses against observed, material-rich backgrounds; characters and environment agree in perspective, light direction, contact shadow and colour (not necessarily the same texture); everyday actions with weight, an order of handling objects, and reactions; environmental motion with causes (wind, gravity, contact); spaces that are livable and serve the story. Forests, country houses, girls, cats, brooms, food and towering clouds are not required: a city laundromat works. "Lived-in" does not mean slow.
- **Pixar**: Luca's graphic, painterly look and Soul's realistic New York plus abstract soul world are different ranges. Transferable: form (silhouette and proportion first, surface detail after; big eyes, round faces and shiny plastic are not the definition); material carries story (cloth, skin and metal read differently); light directs narrative focus (not a fixed golden rim light or blue-purple background); performance (pose, weight, gaze, anticipation and follow-through; emotion from cause and effect). Do not give every object a face; never copy existing characters. Distinct from early ray-traced CGI (uniform plastic, chrome balls).

## Designing a style the index does not cover

1. Write the 3-5 most distinctive formal elements (material, stroke, colour, motifs, traces of the medium), from several different works, noting stable traits and exceptions.
2. Give each element **a way to move** that belongs to that picture's world: water trembles, paper flutters, gold glints, print registration shifts, film jitters.
3. Work out **how this image is physically made** (brushed, carved, printed, pasted, inlaid, sprayed, rendered) and write that process as the renderer: SVG paths with `@remotion/paths`, deterministic jitter with `@remotion/noise`, SVG filters, layered flat fills, `@remotion/three` for true volume.
4. **One frame first**: compare it against what you know of the originals; animate only once it is recognisable at a glance.

A style card (as a comment block at the top of the scene file) must contain:

- scope (artist / film / period / medium) and sources;
- 3-5 stable traits, and where they do not hold;
- two differences from the nearest neighbour;
- the pipeline: how the medium is made and how the code rebuilds it, with key parameters and colour values;
- motif animation: one main action plus 2-4 motif loops, and how each moves;
- a signature transition into the style;
- pitfalls and known weak spots;
- what is verified and what is still a hypothesis.

For a new style direction, consider three distinct compositions (not three recolours of one), pick the strongest, say why in a code comment, and note the two runners-up in one line each.

## Rules when drawing in a style

- **Compose for the subject.** The style decides how to compose and light, not where the furniture goes in a sample scene.
- **Everything goes through the same material.** People, animals and props get the style's stroke, grain, paper multiply, ink-bleed edge, halftone or misregistration, or they look like pasted clip art; this was the most common weakness across 36 styles. A Monet-style music video with vector-shape cat and hands was judged not to match Monet. People come from supplied imagery, else hands, backs and silhouettes. The real logo and product images are never restyled: integrate them through light direction, contact shadow, a print or paper frame, or a style-treated surround; at most a light grain shared by the whole frame may pass over a product photo, never over the logo.
- **The picture stays alive**: one main action plus 2-4 motif loops, visible within the shot.
- **No flicker**: never re-seed the whole frame at a low rate; "boil" only line art or motif regions. A deliberate stepped rate is style, not stutter (rubber-hose 12 fps, shadow puppets 10 fps): `const step = fps / 12; const f = Math.floor(frame / step) * step;`. A scrolling pattern's modulo period must equal the pattern's real period, or it jumps.
- **Deterministic**: every random value from `random(seed)`; the same frame always renders the same.
- **Lettering** in the style's material where possible (paths); fonts only when loaded.
- **Ageing stays off the subject**: peeling, stains and scratches only in the background; protect character and product regions (flaking on a figure's back read as holes in the clothes).

## Validate on a new subject

- **Design for this brief first.** Figures, props and background are handled together in form, edge, light and material; restyling only the background is not a style.
- **Stress-test before reusing** a style across ads: a human action, an object-only scene, and a big change of scale or environment. Sample subjects are prompts, not templates.
- **Stills check**: hide the artist's name and signature motifs. Are form, colour and light, stroke and space still recognisable? Side by side with the nearest neighbour, is there a real difference?
- **Motion check**: contact, occlusion, texture that sticks to surfaces rather than swimming, consistent identity, unified material. Good stills do not prove smooth animation; a sound written plan does not prove the picture works.
- **Be honest about status**: a research hypothesis, a one-scene implementation and a cross-scene validated style are different things. One film of a studio passing does not cover the studio.
