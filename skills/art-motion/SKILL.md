---
name: art-motion
description: Direct and build art-style and explainer-style motion in Remotion with 35 painterly and graphic style cards (Van Gogh flow-field strokes, Monet water light, Seurat dots, ink wash, Klimt gold, Bauhaus, pop-art halftone, pixel art, vaporwave, Art Nouveau, cubism and more), 8 explainer grammars (kinetic typography, Kurzgesagt-style flat, Vox collage, whiteboard, 3Blue1Brown-style morphs, keynote-style product UI, finance charts, storytime), and camera rules against slideshow-style animation. Use it when an animation should look painted or drawn in a named artist's, movement's or era's style ("make it Van Gogh", "pixel art", "make the painting move"); when it launches, reveals or demos a product (an Apple-keynote-style reveal, an app or UI walkthrough, a screen recording), charts real numbers or runs on kinetic text; when it feels like a slideshow, zooms too much or has a dead background; or when moving a style to a new subject. Adapted from huashu-art-motion (MIT).
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

## How to open the references

`load_capability` loads only this page. Every other file opens with `read_file`, and its path starts with
`art-motion/`, for example `read_file("art-motion/references/styles/van-gogh.md")`. Passing a file path to
`load_capability` fails. If a name is unclear, run `find_files` or `list_directory` on `art-motion/references/`.

**When the brief or the user names a style or an explainer look, read its card before you write scene code.** The
cards hold the measured palettes, stroke sizes, timings and known pitfalls. A style recalled from memory loses them.

## Pick what to read

| The brief or the user says | Read |
|---|---|
| A named artist, movement or era, or "make it painterly" | Its style card (list below), then [painting-in-code](references/painting-in-code.md). Unsure which style fits: [the style index](references/styles/INDEX.md) |
| A product launch or reveal (Apple-keynote style), a product demo, an app or UI walkthrough, a screen recording | [keynote-ui](references/grammars/keynote-ui.md) |
| An explainer look, kinetic text, a chart of real numbers | Its grammar card (list below). Unsure which fits: [the grammar index](references/grammars/INDEX.md) |
| That style on a subject its card wasn't built for, or a style not listed | [style-transfer](references/style-transfer.md) |
| "Make the painting move", a journey through worlds or styles, a morph between styles | [living-paintings](references/living-paintings.md) and [transitions](references/transitions.md) |
| "Feels like a slideshow", "too many zooms", "boring", pacing, or a shot list to plan | [directing](references/directing.md) |
| Colour choices, "looks AI-generated", mapping a brand palette | [palettes](references/palettes.md) |

**Style cards**, under `art-motion/references/styles/`:
- Painters: [van-gogh](references/styles/van-gogh.md), [monet](references/styles/monet.md), [impressionism](references/styles/impressionism.md), [seurat](references/styles/seurat.md), [rembrandt](references/styles/rembrandt.md), [renaissance](references/styles/renaissance.md), [klimt](references/styles/klimt.md), [munch](references/styles/munch.md), [matisse](references/styles/matisse.md), [picasso-blue](references/styles/picasso-blue.md), [dali](references/styles/dali.md), [hopper](references/styles/hopper.md), [kusama](references/styles/kusama.md), [haring](references/styles/haring.md)
- Graphic and digital: [flat-illustration](references/styles/flat-illustration.md), [pop-art](references/styles/pop-art.md), [pixel-art](references/styles/pixel-art.md), [vaporwave](references/styles/vaporwave.md), [retro-cgi](references/styles/retro-cgi.md), [bauhaus](references/styles/bauhaus.md), [constructivism](references/styles/constructivism.md), [cubism](references/styles/cubism.md), [art-nouveau](references/styles/art-nouveau.md), [silver-age-comic](references/styles/silver-age-comic.md)
- Animation and film: [ghibli](references/styles/ghibli.md), [shinkai](references/styles/shinkai.md), [rubber-hose](references/styles/rubber-hose.md), [shadow-puppet](references/styles/shadow-puppet.md)
- Ancient and traditional: [cave-painting](references/styles/cave-painting.md), [egyptian-mural](references/styles/egyptian-mural.md), [greek-vase](references/styles/greek-vase.md), [roman-mosaic](references/styles/roman-mosaic.md), [gothic-manuscript](references/styles/gothic-manuscript.md), [dunhuang](references/styles/dunhuang.md), [ink-wash](references/styles/ink-wash.md)

**Grammar cards**, under `art-motion/references/grammars/`: [kinetic-type](references/grammars/kinetic-type.md), [keynote-ui](references/grammars/keynote-ui.md), [finance-chart](references/grammars/finance-chart.md), [kurzgesagt](references/grammars/kurzgesagt.md), [vox](references/grammars/vox.md), [whiteboard](references/grammars/whiteboard.md), [3blue1brown](references/grammars/3blue1brown.md), [storytime](references/grammars/storytime.md)

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
- **Copy stays readable over paint.** Stroke fields, dots, halftone and other
  painted grounds never run behind text. Put every line of copy, small print
  included, on a calm backing (a solid or softly blurred panel in the palette),
  or clear the marks around it. Check the smallest text in every preview.
- **A restyle keeps the message.** When you restyle an existing animation, keep
  every line of copy, product name, label and product image it had. Spread them
  across more beats (kinetic type) instead of cutting them. Cut something only
  when the user asks.
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
  [painting-in-code](references/painting-in-code.md) has the skeleton.
- **Use SVG or CSS when they're enough.** SVG paths, patterns and filters
  (`feTurbulence`, `feDisplacementMap`, `feGaussianBlur`, `feColorMatrix`),
  and CSS `mix-blend-mode`, `clip-path` and `mask-image`, are often lighter
  than canvas.
- **Previewing.** When you have `preview_frames`, sample every shot at two
  moments about 0.5 s apart to confirm the painting actually moves. Then look
  at one frame per shot side by side: any shot that looks like it came from
  another film gets repainted in the shared style.
- **The renderer's rules still apply:** ASCII-only code, every identifier
  imported, inline styles only. Load `remotion-render-pitfalls` too when it is
  offered; `remotion-best-practices` covers Remotion idioms.

## What was left out on purpose

- Upstream's Canvas engine, Python render/QA/delivery scripts, music synthesis,
  voice and image-generation setup. The thresholds those scripts enforced live
  on as design rules in [directing](references/directing.md).
- Demo characters and mascots, and the shared room composition of upstream's
  art-history demo film.
- The style cards upstream marks as unvalidated research (38-55), and its
  franchise-specific cartoon character card.
