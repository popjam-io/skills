# Pointillism (Georges Seurat, Neo-Impressionism, 1884)

> Adapted from huashu-art-motion (MIT, (c) 2026 alchaincyf) - references/风格配方/29_seurat.md

Layer: material (works on any subject) - Upstream quality: ★★ - Known weakness: too static, and the dot grid reads as regular.

## Look
Optical mixing: equal dots of a fixed pure palette placed side by side so the eye blends them. Colour pairs approximate every tone, complementary dots sprinkle through, value edges glow (white dots on the light side, deep blue on the dark), and a dotted deep-blue border frames the picture. Calm and luminous. Not Impressionist dabs: dots are equal and the palette fixed.
- 14 saturated: #1a2058 #2a3a9a #3f6fd0 #6aaee6 #1f6a52 #2f9a5a #a8c83a #f2cf3a #f08a2a #e0432a #c0306a #7a4aa8 #f8f4e8 #e8b48a
- 7 tints (mixed with white): #f6e49a #f6c48a #cfe08a #b0cff0 #f2b8c8 #c99a4a #9a7ac8

## Build it in Remotion
Canvas; px at 1920 wide, scale with the canvas.
1. Paint a flat base (subject included) offscreen; read it with getImageData. Under the dots draw the base again with `filter = 'blur(4px) saturate(.85) brightness(1.06)'` as the ground between dots.
2. Hex grid of equal dots: pitch 10, row height 8.66, r 4.5, static jitter +-1.2 px (~24k dots at 1920x1080). Precompute positions once; batch dots into 21 Path2Ds, one fill per colour.
3. Dot colour: jitter the sampled target per dot (dj in +-20: R + dj, G + 0.8dj, B - 0.6dj). For each palette pair (i, j), project the target onto Pj -> Pi for weight w, clamped [.2, .8]; error = weighted squared distance (R .9, G 1.2, B .8) of the mix from the target + 0.004 * |Pi - Pj|^2 (stops black + white making grey). Best pair wins; the dot takes Pi if hash(dot) < w, else Pj. Cache by 15-bit colour (content-independent, safe to keep).
4. 8% of dots swap to the complement (blue<->orange, green<->red-violet, yellow<->violet ...). Irradiation: if luminance differs by > 45 from the pixel (+14, +6) away, 45% of those dots go white on the bright side, deep blue on the dark side.
5. Border: 28 px deep-blue band, dotted too (orange complements appear in it).
6. Cost: heavy. Render the dot layer only per 6 fps step (`Math.floor(frame / 5)`) and blit between steps; stamp pre-rendered dot sprites instead of arcs; pitch 12-14 on 1080-wide verticals. Composite the real logo and text un-dotted on top - dots destroy legibility.

## Make it move
- Trembling light: each step, 7% of dots switch to their pair colour. 4 fps / 3% was judged "basically a still" (adjacent-frame mean difference 0.1-0.2); 6 fps / 7% reached 0.45.
- Shimmer zones (water, sky) re-roll their hash each step.
- One clear main action plus a looping motif: a butterfly circling (x offset sin(2.6t) * 120, wings |sin(20t)|), boats drifting 40 px/s, a smoke plume.
- Beyond upstream (the weakness): breathe dot radius 4.5 +- 0.6 in a slow wave across the grid; swap the hex grid for a jittered or Poisson-disc layout.

## Signature transition
Crystallize into dots, 0.34 s (10 frames): dots grow over the old shot as it fades to paper, change colour in a diagonal wave with a 1.35x hop, then the new shot develops beneath and the dots retract. Recipe: ../transitions.md (pointill).

## Pitfalls
- Preferring single pure colours cut a wall gradient into vertical bands; continuous ratios still banded at pair switches. The per-dot target jitter (step 3) fixes both.
- Without the 7 tints a light wall broke into white, skin and stray blue dots - snow noise.
- Static by default; budget motion deliberately.
