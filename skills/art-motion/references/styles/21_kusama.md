# Kusama infinity dots (1960s to now)

> Adapted from huashu-art-motion (MIT, (c) 2026 alchaincyf) - references/风格配方/21_kusama.md

Layer: era specimen (best for homage, journeys, era-hopping) - Upstream quality: ★★★ - Known weakness: the figure, in the wall's own dots, survived only by its outline.

Evoke the technique; never copy a specific work or character.

## Look
Every surface covered in hand-painted dots pulsing as one organism; red with white dots, yellow with black; infinity-mirror light lattices. Red #d8181e / #a80e14, floor #c0141a -> #e02024, white #fbf6ee, yellow #f6d02a, black #141210, skin #f6dcc8.

## Build it in Remotion
Canvas, or SVG with one `<path>` per colour; not a thousand elements. px at 1920 wide; scale with the canvas.
- Hex grids: rows sp*0.87 apart, odd rows offset sp/2. Wall: r 30 at spacing 104 plus r 10 offset; jitter 25-50%, size x0.75-1.25, aspect 0.85-1.15, random rotation. Floor: 9 rows growing nearer (r 6 -> 28, spacing 46 -> 116), squashed to 0.42.
- One pulse: radius *= 0.82 + 0.28*sin(dist*0.012 - 6t), dist from the subject.
- Crawling patterns: clip to the silhouette, y offset (46t) mod period (13px dots, spacing 52). Period = two row spacings (2*sp*0.87), or the pattern jumps at the wrap.
- Mirror panel: a 13x7x3 lattice of lights (#ff3a4a #ffd43a #3aa8ff #6aff7a #ff7ad0 #ffffff), z cycling toward camera at 0.3/s, focal 150, depth-sorted; hard core + 3.2x additive glow.
- Dotted centrepiece (good on a product): 5 lobes outer to inner, black dot rows largest mid-lobe (9.5px), riding the pulse; breathing 1 +- 0.025*sin(5t) from the base.

## Make it move
- The pulse (main action), patterns crawling down garments, lights flying in, the centrepiece breathing.
- "Self-obliteration" end: red overlay fades in as a 120px hex lattice blooms from the subject to radius 0.47*spacing (~8 frames), holds ~5 frames breathing; ends white dots on red. A strong end-card ground.

## Signature transition
Dot bloom: a hex grid (spacing 58) grows from the subject; q = clamp((1.55p - 1.1d - 0.08k)/0.42) (d normalized distance, k random), radius outBack(q)*0.74*spacing; the union reveals the new shot; growing dots get a cream rim rgba(251,246,238,1 - q) 5px. 0.48 s (14 frames). Custom presentation (see 16_2026.md) clipping to circle subpaths.

## Pitfalls
- Random lights with big glows = bokeh mush; a regular lattice reads as infinite.
- Unbounded growth ends on blank colour; cap the radius, end on the lattice.
- Weakness: give the figure a different ground or value; keep dots off key colour boundaries.
