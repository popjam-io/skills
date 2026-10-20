# Impressionism (Monet era, 1874)

> Adapted from huashu-art-motion (MIT, (c) 2026 alchaincyf) - references/风格配方/08_impressionism.md

Layer: material (works on any subject) - Upstream quality: ★★ - Known weakness: strokes break up faces and hands.

## Look
Short broken strokes of high-key color over a light ground, no outlines, colored shadows, dappled sunlight. Each region draws from its own palette: pink-violet walls (`#d8bede` -> `#f0c8cc` -> `#f2c4d4`) under a warm yellow sun glow, cream-yellow sunlit wall, rose-orange-violet floor, sky, grass greens, lilac curtains, blue-violet cloth; strong reds keep their own color. Light ground `#f2e6ee` shows between strokes.

## Build it in Remotion
px at 1920 wide; scale with the canvas.
1. **Flat underpainting** (canvas): gradients and simple shapes; redraw only parts that move.
2. **Stroke repaint**: jittered grid; per cell sample the underpainting (one `getImageData`), pick a color from the region's palette mixed 30-45% with the sampled color (keeps values), draw a round-capped line of length `len*(0.7-1.3)` at the direction-field angle. Two passes: main (cell 11, len 20, width 7, color jitter 26, masked off small detailed areas) and fine (cell 6, len 11, width 4.5, only inside that mask: distant views, small framed pictures, which get horizontal ripple strokes).
3. **Direction field**: walls diagonal up-right (-0.95 rad in sun, -0.55 elsewhere, +-0.55 noise), floor near horizontal, curtains and cloth vertical, foliage radial, sky horizontal.
4. **Keep whites**: if the sample is brighter than (240,236,225) use white, or frames and highlights get repainted.
5. **Characters**: flat fill into their own layer, then a stroke pass `source-atop` (cell 7, len 13); whites drawn from white, lilac and cream. Features as fine lilac lines; no contours.
6. **Determinism and cost**: seed every cell independently, ``random(`imp-${i}-${j}`)``, never one sequential stream. A full pass is ~20k strokes (upstream 69 ms/frame, too heavy for live preview): precompute the stroke list in `useMemo`, bake static strokes once, redraw only moving regions; or render at half resolution and upscale.

## Make it move
- **Main - dappled light**: ~26 sun patches on floor and table; intensity `0.5 + 0.5*sin(t*sp + ph)*sin(t*sp*0.53 + 2*ph)` clamped (irregular), sp 5-11, slow drift +-44 px; each patch is 40 short pale yellow-white strokes re-seeded at 8 fps (`Math.floor(frame * 8 / 30)`), source-over at alpha 0.95.
- **Loop 1 - wind**: flower heads sway `sin(t*3.2 + ph + x*0.02)*(10 + 0.6r)` px (r = head radius), stems fixed; foliage +-8 px `sin(t*1.9)`; clouds 45 px/s; window strokes turn +-0.22 rad with the wind; ribbons flutter.
- **Loop 2 - sparkle**: 60 diagonal bright strokes on the sunlit wall re-seeded at 6 fps; fur or hair glints on the lit side only (`isPointInPath`), `sin(t*7 + h*30)`.

## Signature transition
Strokes paint the new shot in: ~2600 elliptical dabs (angle -0.9 to -0.4 rad, length 34-80, width 10-20), each with a random start; reveal `q = easeOut(p/0.7)`, each dab grows over 0.12; their union clips the new shot. On top, 260 light dabs (`#f6e27a`, `#f2a7c3`, `#b9d9f2`, `#c6e8a8`, `#ffffff`, alpha 0.75) shown with probability `0.8*sin(pi*p)`; crossfade fully after 0.7. Upstream 0.28 s (~8 frames). Canvas: composite both shots in one canvas. DOM: `clipPath: path(...)` of ~300 larger ellipse subpaths on the entering child.

## Pitfalls
- One coarse pass erases small things (figures in a view, a framed picture); use coarse + fine passes.
- Screen-blended sun patches at 0.75 vanish on pink; use source-over at 0.95.
- Any default outline color leaves dark lines around faces; this style has no contours.
- Re-seeding all strokes at 8 fps strobes (frame diff 4.1 avg, peaks 20, vs 0.57 fixed). Keep strokes fixed; boil only motif regions.
- A sequential RNG plus palette skips reshuffles every later stroke when anything sways; skipping masked character cells has the same effect. Hash per cell.
- Weakness (shredded faces and hands): use a 4-5 px cell there, or keep them soft blended color with only a few strokes.
