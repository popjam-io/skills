---
name: art-motion
description: Direct and build art-style and explainer-style motion in Remotion. Covers 35 painterly and graphic style recipes (Van Gogh flow-field strokes, Monet water light, Seurat pointillism, ink wash, Klimt gold leaf, Bauhaus, pop-art halftone, 8-bit pixel, vaporwave, Art Nouveau, cubism and more) and 8 explainer grammars (kinetic typography, Kurzgesagt-style flat, Vox collage, whiteboard, 3Blue1Brown-style morphs, keynote UI, finance charts, storytime), plus camera rules and checks against slideshow-style animation. Use it when an animation should look painted or drawn in a named artist's, movement's or era's style ("make it Van Gogh", "like a Monet", "Bauhaus", "pixel art", "ink wash", "vaporwave", "make the painting move"), when it should follow an explainer grammar, when it feels like a slideshow or PPT, has too many zooms or a dead background, or when moving a style to a new subject. Adapted from huashu-art-motion (MIT).
license: MIT
metadata:
  author: POPJAM (https://popjam.io)
  adapted-from: https://github.com/alchaincyf/huashu-art-motion (v1.2.0, MIT, (c) 2026 alchaincyf)
  tags: remotion, motion-design, art-styles, painterly, explainer, kinetic-typography, camera, popjam
---

# Art Motion

> Adapted from [huashu-art-motion](https://github.com/alchaincyf/huashu-art-motion)
> by alchaincyf (MIT; see `NOTICE.md`). Upstream renders with its own Canvas
> engine and Python QA scripts. This adaptation keeps the methods, the measured
> numbers and the known pitfalls, rewritten for Remotion. None of the upstream
> engine, scripts or demo assets are included, and nothing here needs a script.

You are the director, storyboard artist, painter, animator and editor of this
piece, and your brush is code. The bar: a viewer understands what every shot
is saying and wants to keep watching. In an art style, the look is recognizable
at a glance, and the painting is alive. It is never still images cutting into
each other.

## Pick what to read

Read only what the task needs. Every path is under this skill's directory.

| The brief or the user says | Read |
|---|---|
| A named artist, movement or era: "Van Gogh", "impressionist", "Bauhaus", "pixel art", "vaporwave", "make it painterly" | `references/styles/INDEX.md`, then the one card that fits, then `references/painting-in-code.md` |
| That style on a subject its card wasn't built for, or a style not in the index | `references/style-transfer.md` |
| "Make the painting move", a journey through several worlds or styles, a morph from one style into another | `references/living-paintings.md` and `references/transitions.md` |
| An explainer feel: kinetic type, Kurzgesagt-style flat, Vox-style collage, whiteboard, 3Blue1Brown-style, keynote UI, finance chart, storytime | `references/grammars/INDEX.md`, then one grammar card |
| "Feels like a slideshow", "too many zooms", "boring", "the camera is off", or a shot list to plan | `references/directing.md` |
| Colour choices, "looks AI-generated", mapping a brand palette | `references/palettes.md` |

## The director's rules (always)

1. **Plan the shots before writing scenes.** Do it in your head or in a code
   comment. For each shot, write down the object on screen (a noun), what it
   does (a verb), the camera move, the on-screen text (about 8 words at most)
   and the technique. Open on a small concrete action tied to the topic, not
   on a title card. Carry one concrete example through the whole piece. Keep
   shots to 2-6 s, so a 15 s ad has 3-6 shots. Text-led shots should be at
   most ~30%. Neighbouring shots change composition, never style.
2. **The camera is punctuation.** If the viewer can already read the frame,
   hold still. Use slow moves to link shots (slow push, pan, pull back). Save
   fast pushes and smash-ins for the accent: the reveal, the key number, the
   punchline. A short ad gets one or two. After pushing in, pull back, pan
   away or cut to a new framing. Never push in three shots in a row, and don't
   give every shot the same move.
3. **The painting stays alive.** Each art-style shot gets one main action plus
   about two looping motifs (stars swirl, light flickers, water ripples), and
   the camera may drift. Still images joined by crossfades are a failure.
4. **Real material leads.** When the brief has product photos, screenshots or
   real numbers, they are the main image. Code explains, labels and moves them.
   Only paint in code what no real material shows.
5. **One look, start to finish.** Use one style and one palette. People,
   animals and props go through the same treatment as the background. A vector
   cat in a Monet world reads as pasted on. A clean, consistent piece that's a
   little plain beats a collage that changes style every shot.
6. **No instant-AI look.** Avoid blue-to-purple gradient grounds,
   deep-purple starfields and neon cyan-violet glow, unless the brand's own
   palette is blue or purple. Don't draw chibi people, white-shell robots or
   coins and balls with faces in code.

## POPJAM rules that override any style

- **The real logo and product images are embedded with `<Img>`, never redrawn.**
  They can sit inside a painted world with a light treatment (shadow, grain, a
  gentle colour grade, a painted frame around them), but they must stay sharp,
  legible and correct. If you need the product cut out, use `remove_background`.
- **Brand palette first.** When the brand defines colours, map them onto the
  style's palette roles (ground, ink or line, accents). Keep the style's value
  structure and mark-making. A brand `visual_style` is still binding for type,
  logo use and never-rules. The art style is how the piece is painted.
- **Learn the language, not the work.** Take mark-making, colour logic, light
  and form. Never reproduce a specific artwork, character, mascot or franchise
  asset. For living artists, studios and actively managed estates, evoke the
  technique. Put an artist's or studio's name on screen only if the brief asks
  for it.
- **Recompose for the canvas.** Upstream numbers are px at 1920 wide (16:9).
  Scale them with the canvas, and design vertical (9:16, 4:5) compositions
  fresh instead of cropping a landscape layout. Keep the brand's copy clear of
  platform safe zones.

## Six ways it goes wrong (check before the first preview and before finishing)

1. **Slideshow.** Fixed headers, bullets fading in one by one, the same camera
   move every shot, ending on a centred quote card. Fix it with one visual
   event per shot, varied camera moves, and an ending on an action by the main
   object.
2. **Copying the demo.** A layout or subject lifted from a reference card's
   example. Learn the method and redesign the composition for this subject.
3. **No concrete object.** An abstract idea shown only as words and icons. If a
   shot has no object doing something, it isn't ready.
4. **Dead background or empty frame.** A big flat or starfield ground that
   never changes while a small centre moves, or any near-blank frame of 0.3 s
   or more mid-piece. Make the subject fill about half the frame or more, and
   change the background with the content.
5. **Painting what real material already shows.** Use the real photo,
   screenshot or footage full-bleed instead.
6. **Instant AI look.** See rule 6 above, plus a collage that switches style
   every shot.

## Remotion ground rules for painted frames

- **Deterministic.** Everything is a pure function of `useCurrentFrame()`.
  Get randomness from `random(seed)` (from `remotion`) and noise from
  `noise2D`/`noise3D` (from `@remotion/noise`). Never use `Math.random`,
  `Date.now` or timers. The same frame must render the same pixels twice.
- **Canvas.** Use a `<canvas ref>` at composition size and draw synchronously
  in a `useEffect` keyed on `frame`. Compute static layers and stroke lists
  once with `useMemo` and redraw only what moves. The live preview plays in
  real time, so keep each frame's drawing work under about 30 ms at 1080p. For
  the hand-drawn "boil", reseed every 3-4 frames (8-10 fps).
  `references/painting-in-code.md` has the skeleton.
- **Use SVG or CSS when they're enough.** SVG paths, patterns and filters
  (`feTurbulence`, `feDisplacementMap`, `feGaussianBlur`, `feColorMatrix`),
  and CSS `mix-blend-mode`, `clip-path` and `mask-image`, are often lighter
  than canvas.
- **Previewing.** When you have `preview_frames`, sample every shot at two
  moments about 0.5 s apart to confirm the painting actually moves. Then look
  at one frame per shot side by side: any shot that looks like it came from
  another film gets repainted in the shared style.
- **The renderer's rules still apply.** `remotion-render-pitfalls` covers
  ASCII-only code, importing every identifier and inline styles only.
  `remotion-best-practices` covers Remotion idioms.

## What was left out on purpose

- Upstream's Canvas engine, Python render/QA/delivery scripts, music synthesis,
  voice and image-generation setup. The thresholds those scripts enforced live
  on as design rules in `references/directing.md`.
- Demo characters and mascots, and the shared room composition of upstream's
  art-history demo film.
- The style cards upstream marks as unvalidated research (38-55), and its
  franchise-specific cartoon character card.
