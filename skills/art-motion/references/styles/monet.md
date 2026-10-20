# Water lilies and footbridge (Claude Monet, Impressionism, 1899)

> Adapted from huashu-art-motion (MIT, (c) 2026 alchaincyf) - references/风格配方/28_monet.md

Layer: era specimen (best for homage, journeys, era-hopping) - Upstream quality: ★★ - Known weakness: the sample hung the pond on a wall above a wooden floor, so the space felt wrong; water needs its own receding plane.

## Look
A pond made of short horizontal dabs: sky reflections, drifting lily pads with pink/white flowers, swaying willow reflections, an arched green footbridge under wisteria. No outlines; shadows are coloured (warm lit side, violet shade), never black.
- Water base: vertical gradient #b9c7e6 -> #8fa6d6 -> #6c84bf -> #5a72a8 plus 4 pale pink-yellow sky reflections.
- Stroke palettes: water #5b6fb5 #7d8fd0 #9db5e0 #6aa0a8 #b7a6d8 #d9c8e8 #8fb8a8 #a6c4e8 #c8b0d8 (mixed .45 with the base); foliage #5f8f4a #7fae5a #3f6f4a #9cc070 #6f9a7a #b4cc78; blossom #f0a0b8 #f7d0dc #fff2f4 #e88aa0; warm ground #c69a6a #b07a5a #d8b08a #9a6a7a #8a7aa8 #e0bc90.

## Build it in Remotion
Canvas; px at 1920 wide, scale with the canvas.
1. Base layer (flat shapes) offscreen: water gradient, 5 willow-reflection bands, ~100 notched-ellipse pads in 10 clumps (rx 38-78, ry 12-21, 40% flowering).
2. Stroke passes sample the base (getImageData) on a fixed cell grid, mix with the region palette, draw a short stroke at the pass angle; no outlines.
   - Water: cell 9, length 34, width 6.5, horizontal (0 +- 0.06 rad), boil 6 fps.
   - Distant foliage: cell 6, length 13, width 4.5, diagonal above, horizontal below, boil 6 fps.
   - Ground: cell 12, length 34, width 8, boil 0. Architecture: cell 6, one vertical and one horizontal pass, boil 0.
3. Cost: full-frame water at cell 9 is ~25k strokes - one of the heaviest styles. Precompute stroke positions, angles and palette picks once (`useMemo`, seeded `random`); cache static passes; re-render water strokes only when `Math.floor(frame / 5)` changes and blit the cache between steps. Still slow: half-resolution strokes scaled up, or a larger cell.
4. Key structures get their own layer: the bridge vanished into the foliage palette until it got a dark backing #24452a in the base, a 20 px #3f8a62 underlay with a #8fdcae highlight, and its own cell-5 pass with a pale blue-green palette. Treat the product the same way - its own layer, the real image, only a light stroke halo around it.
5. Figures: flat fill -> fine strokes clipped to the figure (cell 6, length 12; white garment from #fbf8f2 #e4e0f6 #cfd2ee #f8ecd0 #d8e8f2) -> warm yellow gradient alpha .22 on the lit side, violet alpha .32 in shade -> features only, thin #5a4f8a lines.

## Make it move
- Water glints (the signature): 160 short bright horizontal strokes (#fffbe8 #fdf0d0 #f8e0ec #e8f4ff), brightness clamp(sin(t * (5..11) + phi) * sin(2.3t + i)), jumping +-5 px sideways at 10 fps.
- Lilies drift x + sin(1.3t + phi) * 7 + 6t; willow band edges wobble sin(0.03y - 3.2t + k) * 14.
- 3 ripples: dashed ellipses (ry = rx * 0.22) expanding and fading where something touches the water - a natural spot to land the product.
- Wisteria: 12 strands of 9 shrinking lilac dots, swaying sin(2.4t + 0.9i) * 8; a ribbon flutters.

## Signature transition
Water ripple, 0.34 s (10 frames): the old shot falls into the water (rows shift sideways), the new one opens through rings of horizontal dab-shaped ellipses spreading from a focal point. Recipe: ../transitions.md (ripple).

## Pitfalls
- Boiling the whole frame at 6 fps gave 47% frame difference - pure noise. Boil only the water.
- Wisteria in thick lines read as smooth pills; use dot chains.
- Text on the stroke field is unreadable; give copy a cream halo (blur ~18 px) or a solid card.
- Space (the weakness): lay water as a horizontal plane receding in perspective (strokes shorter and thinner toward the horizon) with the shore or subject standing on it.
