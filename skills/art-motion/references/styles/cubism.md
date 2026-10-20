# Analytic Cubism (Picasso / Braque, 1912)

> Adapted from huashu-art-motion (MIT, (c) 2026 alchaincyf) - references/风格配方/11_cubism.md

Layer: material (works on any subject) - Upstream quality: ★★ - Known weakness: too light overall; not enough large dark-brown planes.

Evoke the technique; never copy a specific work or character.

## Look
- Space built from translucent overlapping planes, each graded light to dark; "passage" lines running through everything; a near-monochrome ochre/grey/brown range.
- Textures: stipple and hatch patches, short Braque-like dashes (a brick-ish grain), combed faux wood grain with knots, cane weave, ruled paper.
- Collage cues: stencil letters with breaks, a newspaper fragment.
- Figures faceted into big planes whose triangles spill past the contour; a frontal eye on a profile, a spiral ear, outlines as straight segments overshooting their ends.
- Palette: paper `#d6c8ac`, off-white `#ece3cf`, ochre `#b8975f`, brown `#6e5538`, dark brown `#3a2c1e`, grey `#a8a395`, blue-grey `#8e9eab`, dark grey `#5a5852`; window `#c9d3da #8fa3b3 #e4e6e2 #6f8597 #b4c1cb #5f7385`; dress `#6a7a8b`, sleeve `#3c4857`, skin `#e2cfae`, hair `#c9a256`; animal `#c8773a` / `#e8dfc9`.

## Build it in Remotion
px at 1920 wide; scale with the canvas. Upstream ~13 ms/frame.
1. **Background (bake)**: `plane(pts, col, alpha)` fills a polygon with a linear gradient from vertex 0 to a random other vertex: stops color mixed 25% toward off-white -> color -> mixed 40% toward dark brown, alpha 0.18-0.7. Stack ~18 large hand-placed planes, a 9-wedge fan radiating from below (alternating light/dark, alpha 0.3) and ~70 random 3-4-gons. Add 4 stipple patches (9 px diamond grid, r 1.6), 4 hatched patches (7 px diagonals), ~9000 dashes 3-8 x 1.5 px (55% off-white at alpha 0.28, 45% dark at 0.16), ~46 thin straight lines across everything (1.3 px, alpha 0.55). Faux wood: lines along the board bending around knots by `14*exp(-(u - k)^2/0.01)`, 4 elliptical rings per knot.
2. **Multi-view window**: cache the view once; draw it into 4 panes, each clipped and offset differently (`dx = 18*sin(9t + 1.7i)` + 10 fps jitter +-3, `dy = 8*cos(7t + i)`), so one view is misregistered across panes; a translucent triangle slides across each pane at 260 px/s.
3. **Stencil word**: a heavy slab face (e.g. Alfa Slab One 104 px) in a small layer, then `destination-out` horizontal and vertical breaks so the planes show through.
4. **Facetizer for figures**: flat-fill the figure offscreen, read its box (`getImageData`), lay a jittered triangle grid (random diagonal per cell), fill each triangle with its centroid color x(0.8 + 0.38 rand) as a light-to-dark gradient from vertex 0 to 2, and draw triangles *unclipped* (skip centroids with alpha < 120). Cells: 58 px for figures, 26 px for small animals, a second 26 px pass for hair limited to hair-colored pixels.
5. **Re-impose structure after faceting**: two skin planes on the face, a blue-grey plane over the front half (alpha 0.82), frontal almond eye, spiral ear, red lips; radial fold wedges on skirts; outline as straight segments each overshooting 10-16 px. Animals: hexagonal head, straight-segment body, diamond eyes.
6. **Embed**: 5 translucent planes (alpha 0.2) over the characters, shifting `8*sin(6t)`, so figures sit inside the space instead of on top of it.

## Make it move
- **Main - letters jump**: at 12 fps (`Math.floor(frame * 12 / 30)`) the stencil word's letters swap order (e.g. a 4-letter word cycling permutations), each letter offset y +-13 px and rotated +-0.11 rad by a per-step hash.
- **Loop 1 - sliding panes**: the window misregistration above plus the sweeping triangles.
- **Loop 2 - trembling collage and boil**: the newspaper fragment trembles at 8 fps (+-0.0125 rad, +-1.5 px) with a corner folding `sin(20t)`; facet vertices jitter +-8% of a cell at 8 fps and 16-35% of triangles shift brightness +-12%.

## Signature transition
Shards: jitter a 9x6 grid into ~108 triangles. Old shards break away (offset +-80 / +-60 px, rotation +-0.25 rad, `qo = easeInOut((p - 0.4r)/0.45)`), new shards settle into place (`qi = easeOut((p - 0.25 - 0.45r)/0.3)`), r = per-shard random; tint old ones dark and new ones light by `0.12*sin(pi*q)`, 2 px edges `rgba(40,30,20,.35)`, over `#cbbfa8`. Upstream 0.24 s (~7 frames). Canvas shots: composite in one canvas. DOM shots: ~20 shards, each a copy of the shot with a `clipPath: polygon(...)` and transform.

## Pitfalls
- Non-determinism on the first frame: reading back a GPU canvas switches it to CPU raster with different antialiasing (centroid colors change), and context state (`lineJoin`, `lineCap`) leaks between frames. Create readback layers with `{ willReadFrequently: true }` and call `ctx.reset()` at the start of each frame instead of `clearRect`. Check by rendering the same frame three times and comparing.
- 34 px cells look like low-poly 3D; 58 px gives cubist planes.
- A circular clip for the hair pass turned half the face gold; filter by color instead.
- Sleeves must be darker than the dress or the arm dissolves into the dress facets.
- Weakness (too light): add more large dark-brown planes (`#3a2c1e`, `#6e5538`) and stronger value contrast; give figures a polyline skeleton (angled shoulders, elbows, knees) before faceting so more than the edges turns cubist.
