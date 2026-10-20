# Pop Art (comic panel + silkscreen grid, 1962)

> Adapted from huashu-art-motion (MIT, (c) 2026 alchaincyf) - references/风格配方/13_pop.md

Layer: material (works on any subject) - Upstream quality: ★★★ - Known weakness: none recorded.

Evoke the technique (Lichtenstein-style comic, Warhol-style silkscreen); never copy a specific work or character.

## Look
Ben-Day dots on 45 deg grids, thick 5 px black outlines, flat primaries, white highlight dashes, black hatching for shadow, caption box, onomatopoeia burst, thought bubble, a four-panel silkscreen grid with swapped color sets and a misregistered black block. Hair as curl masses with black C-arcs.
Palette: black `#141414`, paper `#f3eedb`, blue `#2f5cc8`, yellow `#f7d52c`, red `#d8232a` / `#a8161c`, white `#fbf8ee`, skin `#fae0cc` with dots `#e2483c`, blonde `#f8d62c` / `#d9a514`, orange `#f39a2c` / `#c4561a`; silkscreen grounds `#9ccf3a #e0359a #2fc0b0 #f08a2a`.

## Build it in Remotion
px at 1920 wide; scale with the canvas. Upstream ~6 ms/frame.
1. **Ben-Day dots as a pattern**: a pitch x pitch tile with 4 corner circles + 1 center circle = a 45 deg grid (diagonal spacing pitch/sqrt 2). Walls: pitch 24, r 5.6, blue on white; skin: pitch 13, r 3.3, red on skin; floor: pitch 14, r 2.2, alpha 0.18. Canvas `createPattern` + `fill(path)`, or SVG `<pattern patternUnits="userSpaceOnUse">`; both stay anchored to the screen, so dots never swim with moving characters.
2. **Background (bake)**: 6 px black panel border, flat color bands with 6 px black edges, a yellow caption box with a 5 px border (comic font such as Bangers 46 px), paper grain.
3. **Characters**: one `ink(path, fill)` helper: stroke black 5 px, then fill flat. Highlights are short thick white strokes; shadows are hatching (clip an ellipse, black diagonals 3.5 px wide every 10 px). Union outlines: stroke *all* pieces first (10-11 px black), then fill all of them (thought bubbles from 10 circles, hair from curl blobs).
4. **Comic hair**: a smoothed mass whose back edge bumps `14*sin(2.1i + 4t)`, 7 curl circles (r 30-48) along it, each with a 4.5 px black C-arc and a darker gold arc, a few black S strands, 2 white highlights. Big eyes, 3 thick lashes, enlarged red lips, skin in red dots.

## Make it move
- **Main - silkscreen grid swaps colors**: 4 color sets (ground, face, shadow, accents), `step = Math.floor(frame * 11 / 30)`; panel i uses set `(i + step) % 4`. Any subject works, a product included: same artwork 4 times, black offset block for misregistration, white glare stripes on one panel.
- **Loop 1 - thought-bubble dots** blink in sequence: 6-frame cycle, dot k lit when `(frame - k) % 6 < 2` (r 20, up 6 px), else r 12.
- **Loop 2 - shaking burst**: per-frame hashed jitter +-8 / +-6 px, +-0.03 rad; a white 14-point burst (radii 128/178, randomised) over a yellow inner burst, two lines of red text (82 px, 12 px black stroke, 4 px black drop shadow); 10 black triangular action lines pulsing `0.85 + 0.25*sin(40t + 2i)`.
- Character beats: a 6 Hz wiggle `16*sin(2*pi*6t)` weighted toward one end of the body (`clamp((x0 - x)/140)`) plus lift `0.6*|wig|`, with stripes, tail and three motion arcs following; steam as two black wavy lines jittering at 14 Hz.

## Signature transition
Lightning + halftone. p < 0.35 old shot; 0.35-0.55 old shot halftoned; 0.55-0.75 new shot halftoned; then the halftone fades off. Halftone: sample at 1/16 resolution, over the image washed with `rgba(244,236,216,.55)` draw dots in the sampled color on offset rows, radius `16*0.62*(0.35 + 0.85*(1 - L)) + 1`. A black 34 px + yellow `#ffe02a` 22 px zigzag (9 segments, +-90 px) draws itself top to bottom over p 0.05-0.6, with a 28-point starburst (r 70/105) at its start for the first half. Upstream 0.16 s (~5 frames); 0.4 s in an ad. Canvas: composite both shots in one canvas. DOM: an SVG dot overlay whose radii grow then shrink across the cut, plus the bolt via `evolvePath` from @remotion/paths.

## Pitfalls
- Per-dot halftone via `getImageData` is ~100x slower than a pattern fill and dots swim with the characters.
- When a body crouches, move the head down into it (~100 px) or it floats above.
- Hair as one wavy yellow sheet reads as a cloth; curls with black C-arcs make it comic hair.
