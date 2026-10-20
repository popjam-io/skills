# Paper cut-outs (Henri Matisse, late cut-outs, 1947)

> Adapted from huashu-art-motion (MIT, (c) 2026 alchaincyf) - references/风格配方/30_matisse.md

Layer: material (works on any subject) - Upstream quality: ★★★ - Known weakness: the gouache brush-mark overlay is a bit heavy.

Evoke the technique; never copy a specific work or character.

## Look
Saturated gouache-painted paper cut with scissors (faceted, irregular edges), pinned to a wall, each piece casting a small soft shadow. Motifs: fronds with rounded fingers, irregular stars, hearts, birds, falling scraps. Flat colour, no outlines, no gradients.
- Palette: two-blue checkerboard #1d4fb8 / #4f95dc (blocks ~240x236), cobalt, emerald #1f9a5a, black, red, yellow, white, pink.
- Faces from scraps only: black almond eyes, a red triangle mouth, pink circle cheeks.

## Build it in Remotion
SVG; px at 1920 wide, scale with the canvas.
1. Scissor edge: resample each outline every 14-24 px (`getLength` / `getPointAtLength` from @remotion/paths), add seeded jitter +-2-2.5 px, join with straight segments. Generate once in `useMemo`; the edge must not boil.
2. Frond (key motif): tapered stem + 2 x lobes alternating rounded capsule fingers. At u = 0..1 along the stem: angle +-(1.05 - 0.55u) rad, length width * (1 - 0.45u), finger width width * (0.34 - 0.12u). One `<g>` (or one nonzero path) so pieces union and cast one shadow. Never modulate width along a single spine - caterpillars and zigzag lightning.
3. Hand-cut edges on complex shapes or images: static `feTurbulence` (baseFrequency 0.028, numOctaves 2, fixed seed) -> `feDisplacementMap` scale ~18, limited to the subject's box.
4. Pinned-paper shadow: `filter: drop-shadow(5px 6px 4px rgba(10,20,40,.3))` per piece or group.
5. Gouache texture: ~2600 long marks (60-300 px, 6-22 wide, half black half white, alpha .04-.13, tilted -0.25 rad) drawn once on a cached canvas, laid over with `mixBlendMode: 'overlay'`. The weakness: start at alpha .03-.08 or ~1500 marks.
6. Cheap: static paper, transform-only motion.

## Make it move
- Fronds sway like pinned paper around the root: sin(2.8t + phi) * 0.13 rad, curl breathing scaleX 0.93-1.0.
- Seven yellow stars spin and twinkle (scale .82 + .22 * sin(7t + 1.9k)); a red heart beats 1 + .18 * max(0, sin 9t); a figure floats.
- Two white birds flap: scaleY .55 + .45 * cos 13t.
- A pink scrap tumbles down (scaleX = cos 6t), clear of faces, product and copy.
- Steam or scent = two small white paper strips wavering.

## Signature transition
Cut-paper sweep, 0.36 s (11 frames): a wide cobalt sheet with scissor edges, carrying pinned fronds, stars and discs, slides right to left; the new shot is behind it. Recipe: ../transitions.md (cutouts).

## Pitfalls
- The falling scrap first crossed the face; route flight paths around faces, product and text.
- Black text on cobalt was unreadable; set copy on a white cut-paper patch (a natural price tag).
- Real logos and product photos go on top as clean images (a paper shadow is fine); never re-cut them with the scissor edge.
