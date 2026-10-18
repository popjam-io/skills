# Bauhaus Poster (Weimar/Dessau, 1923)

> Adapted from huashu-art-motion (MIT, (c) 2026 alchaincyf) - references/风格配方/12_bauhaus.md

Layer: material (works on any subject; narrow use) - Upstream quality: ★★★ - Known weakness: geometric stand-ins drift from where neighbouring shots put the character (~50 px jump at the cut).

Evoke the technique; never copy a specific work or character.

## Look
Pure geometry - circles, squares, triangles, thick bars - in primaries plus black on aged off-white paper; no curved outlines. Lowercase geometric sans set vertically or rotated, a strong diagonal, tubular-steel furniture, a primary-color grid window, figures as jointed mannequins (circle head, trapezoid torso, rod limbs with disc joints). Flat inks with uneven screen-print texture.
Palette: paper `#ebe3cf`, black `#161514`, red `#d3262b`, blue `#2a58b4`, yellow `#efc12f`, light blue `#b9cee0` / `#a6c0da`, grey `#c6c3bb`, cream `#f2ecdf`, orange `#ee8a2a` / `#c25a14`, chrome `#c9c9c6`.

## Build it in Remotion
px at 1920 wide; scale with the canvas. Upstream ~5 ms/frame. SVG fits best (`rect`, `circle`, `polygon`; @remotion/shapes).
1. **Background (bake or static SVG)**: paper + a 320x180 fbm image upscaled at alpha 0.5 for age; a thin diagonal across the page; black and red bars; a vertical lowercase word in a heavy geometric sans (e.g. Poppins 800 at 210 px, rotated -90 deg, scaled to an exact length, read bottom to top); a second word in red; grey squares, ground line, yellow right triangle; tubular-steel chair as one path stroked three times (15 px dark grey, 10 px chrome, 3 px highlight offset 2 px); sparse dark specks (density 0.02, alpha 0.35).
2. **Ink unevenness**: big color shapes get light fbm mottling `source-atop` at alpha 0.55 (bake per shape). Keep any `feTurbulence` in a static, separately cached layer; never inside an animating subtree.
3. **Characters as primitives** anchored to the same rig points the other shots use: head circle r 70 with geometric hair (sector, triangle, bun circle r 34); bar eyes (blink = horizontal bar), red square cheek, short mouth inside the head; blue + black trapezoid torso; skirt as a fan + trapezoid; thick black round-capped rods for limbs, cream disc joints with 5 px black ring and black center.

## Make it move
- **Main - the diagonal bar swings like a clock hand** about its hub: 28 -> 49.5 deg with ease-out over 0.22 s (~7 frames), bar 27 px, a parallel thin line at +30 px and a short red bar at -30 px turning with it.
- **Loop 1 - grid window recolors**: 4x4 cells sized from (inner box - 3 gutters)/4 (upstream 100x101, gutter 9.5); 6 cells swap color on a 13 fps step (`Math.floor(frame * 13 / 30)`), each with its own phase, changing only when `(step + 2*k) % 9 < 6`, so the rhythm is not mechanical. Colors: red, yellow, blue, cream, light blue, grey.
- **Loop 2 - sound arcs and a rolling ball**: 6 concentric arcs beside a red disc, start phase `0.05*sin(9t - 0.7i)`, radius +-3 px, length sweeping 55% -> 100% in 0.4 s. A paw/hand taps (`sin(pi*clamp((t - 0.05)/0.16))`, 36 px), a blue ball (r 31) rolls ~104 px with ease-out over 0.34 s, rotation = distance/radius (a white diameter and dot show the roll), two speed lines behind. Steam: one 2.2 px sine line, 26 cycles over 170 px, travelling -18 rad/s, fading out.

## Signature transition
Primary shapes spin up and open a window. A 340 px blue square, r 150 red circle and yellow triangle, centered on the subject, scale `0.35*30^easeOut(p/0.7)` while rotating `-0.5 + 0.9p` (circle and triangle counter-rotate 0.6x), then sweep off left (-1600 px, ease-in over p 0.4-1); meanwhile a circle `r = 30*40^easeInOut((p - 0.15)/0.7)` at the same center reveals the new shot. Upstream 0.2 s (6 frames); 0.4-0.5 s in an ad. DOM-friendly: `clipPath: circle(${r}px at ${cx}px ${cy}px)` on the entering child plus transformed SVG shapes.

## Pitfalls
- Derive grid cells from the inner box minus gutters; 107 px cells overflowed the frame by 16 px.
- No black in the color rotation: a black cell looks broken and makes the window heavy.
- A mouth bar extending past the head reads as a cigarette.
- Weakness (continuity): anchor every primitive to the shared rig points (head center, neck, hands) so the character does not jump at cuts.
