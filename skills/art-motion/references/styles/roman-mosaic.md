# Roman Floor Mosaic (Pompeii, AD 79)

> Adapted from huashu-art-motion (MIT, (c) 2026 alchaincyf) - references/风格配方/04_roman.md

Layer: material (works on any subject; narrow use) - Upstream quality: ★★★ - Known weakness: faces lose detail at small scale.

## Look
- Everything is small stone tesserae in grey mortar. Stones are not on a grid: rows follow every contour (*andamento*), so outlines are ringed by parallel rows and backgrounds fill in staggered courses. Each stone is slightly irregular, bevel-lit from the upper left, with its own color jitter.
- Every figure and object sits in a 44-50 px white halo whose stones also follow the contour; this is what makes figures pop. Dark outlines 8-10 px (about two stones) so they form rows. Black-and-white wave-scroll borders.
- Palette: wall `#e4ddcd`, halo `#f5f1e8`, outline `#46322a`, mortar `rgb(112,103,92)` +-8; frame red `#a8322a`, dark red `#7c221d`, gold `#d0a23c`; inset landscape: mountain faces `#7c84b8` / `#4e5796` / `#2f3672`, sky `#9ec0d8` -> `#d3e3e4`, slopes `#6f9341` / `#92b254`, ground `#cba344`, cypress `#2b5a2f`, lava `#d64a22` / `#f2952c`; figures: white robe `#efe7d5` with red bands, gold hair `#dcaa42` / `#9c6c1c`, lips `#a8282a`; orange animal `#dc8530` / back `#c06a24` / stripes `#9c4818` / white `#f7f2e8` / eye `#e9c22c`.

## Build it in Remotion
px at 1920 wide; scale with the canvas. Core idea: **compute the stone layout once; each frame only recolors stones** from a flat underpainting. Stones stay put; color flows through them.
1. **Layout (once, in `useMemo`; upstream ~200 ms)**
   - Structure map: render the flat underpainting (static parts + figures at rest) at half resolution; mark edges where the neighbor RGB difference sum > 34, plus region-class boundaries.
   - Distance field from those edges (exact Euclidean transform, two 1-D passes, ~20 ms at half res).
   - Contour rows: candidates where `|d - (k + 0.5)*s| < 1.5` for k below the class's row count; walk them along 8-neighbors preferring the previous direction (smoothed 0.6/0.4), drop a stone every >= s px, oriented along the distance-field tangent; a spatial hash keeps stones >= 0.8x mean size apart.
   - Fill holes with a staggered brick grid per class (row jitter +-5%, column +-9%, min spacing 0.86), gated *only* by min spacing.
   - Borders: per side, 11 rows of 7.6 px stones in local coordinates, widths 0.86-1.14; corners 11x11 squares.
   - Stone size / contour rows / color jitter: wall 12 px / 1 then courses / +-8% (7% darkened 12%); halo 11 / 9 / +-5%; bodies and objects 10 / all / +-5%; faces 5-6 / all / +-4%; hair 8 / all; inset picture 9 / 2 / +-6%; lettering 7 / all; floor band 13 / 1 / +-6.5%. Plus +-7 additive grey jitter; 9% of stones warm (+12,+4,-8), 7% cool (-6,0,+9).
2. **Stone shape and mortar - weighted L-infinity Voronoi (once)**: each stone is a rotated square with four independent half-extents `s/2 x (1.08-1.28)` and +-0.06 rad rotation; distance `D = max(|u|/h, |v|/h)` in stone-local coordinates. Rasterize keeping nearest (D1) and second-nearest (D2); a pixel is mortar if `D1 > 1` or `(D2 - D1)*h/2 < g`, `g = clamp(0.1s, 0.75, 1.25)` px. Joints come out ~1.5-2.5 px and neighbors clip each other into chiselled edges. Store an Int32 stone-id map and a Uint8 shade map: bevel within 2.2 px of the edge from outward normal vs light (-0.6, -0.8), +-16%; dome term `-5%*D1^2`; +-3% pixel grain.
3. **Per frame**: redraw the animated parts of the flat underpainting, `getImageData` once, sample each dynamic stone's center (+ its fixed jitter), fill its pixels as `color*shade >> 7` inside precomputed dynamic rectangles (borders, inset picture, subject), `putImageData` into an offscreen canvas, then `drawImage` onto the visible one. Create contexts with `{ willReadFrequently: true }`. Upstream: ~1 M px/frame, 13-21 ms total. To lighten: lay out at half resolution and upscale with `imageSmoothingEnabled = false`, or limit recoloring to the subject's rectangle.
4. **Lettering**: your own monoline block letters (C as an elliptical arc, others as polylines), stroke 14 px, cap height 60 px, so each stroke is ~2 stones wide.

## Make it move
- **Main - border scrolls clockwise**: wave scroll (spiral r 24 -> 5 over 2.25 turns, line 13 px, period 81 px) around all four sides. Bake each side as a "conveyor belt" strip ~26 periods long whose stone layout also repeats every 81 px (11 stones per row, widths normalised to sum to exactly 81 px), so any phase tiles seamlessly; per frame, transform into the side's local frame, clip, `drawImage(strip, -offset)`. The stones travel with the pattern. Phase `15t + 81*easeInOut(beatWindow)`; corners static.
- **Loop 1 - inset scene**: e.g. a volcano: grey cloud band drifting right 55 px/s (period 380 px), 9 smoke puffs (`#3f3c3a` -> `#a29c94`) hugging the sky, 12 sparks as 10 px square stones on parabolas, pulsing lava.
- **Loop 2 - the subject**: moves through recolored stones. A small handheld prop becomes an *emblema* sprite of 4.4 px stones (dark outline stones, body darker on the shadow side, bright rim) composited at the hand's position and angle each frame; steam as two columns of white square stones rising on a sine. Tails swing ~1.6x normal so motion survives 9 px stones; blink = eye stones take the skin color plus one dark line.

## Signature transition
Tiles flip over, spreading outward from the subject. Grid of 18x34 px cells; each cell starts at (distance from origin, y weighted 1.3)*0.75 + random*0.25; a flip lasts 16% of the transition: width scales by `|cos(q*pi)|`, first half shows a dark tile back (`#17110d` slot, `#2a1c14` back), second half the new image. Upstream 0.38 s (~11 frames); ~0.6 s in an ad. Canvas shots: composite per cell with `drawImage` sub-rects. DOM shots: approximate with an expanding radial `mask-image` on the entering child plus a canvas overlay of flipping dark tiles along the front.

## Pitfalls
- Never `putImageData` straight onto the visible canvas: it ignores transforms and clipping (camera moves, transitions).
- Stones smaller than their spacing leave ~40% mortar and look sparse; oversize them 8-28% and let the bisectors cut them. This is the key to the texture.
- Gating fill stones by "far from edges" leaves narrow shapes (a 26 px tail) as bare mortar.
- Dynamic rectangles must contain moving parts plus halo and steam, or edge stones show half-new, half-old color.
- Never give a moving region its own stone size; at rest it reads as a patch. One wall stone size everywhere.
- Pattern motion slower than a stone per frame is quantised away by color-only updates: move the stones with the pattern, or move much more than a stone.
- Smoke rising straight up gets clipped by a nearby frame within ~70 px; drift it sideways.
- Thin-stroked fonts break at 7-9 px stones (E becomes F, A loses its bar). Props under ~3 stones wide do not read; use an emblema sprite.
- Weakness (faces): 5 px face stones; eye white 13x7 with dark 8x7 (~3 dark stones), lips an 8.5x6 red ellipse (~2 stones), 6 px brows, 10 px face outline. Frontal faces with big round eyes read better than profiles. Keep cups and hands off the face, or everything merges into one patch.
