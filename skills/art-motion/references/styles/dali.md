# Dali surrealism (melting time, 1931)

> Adapted from huashu-art-motion (MIT, (c) 2026 alchaincyf) - references/风格配方/23_dali.md

Layer: era specimen (best for homage, journeys, era-hopping) - Upstream quality: ★★ - Known weakness: figures look like vector illustration.

Evoke the technique; never copy a specific work or character.

## Look
Smooth academic modelling with no outlines, a low-horizon desert, deep blue sky melting to pale yellow, impossibly long shadows, rigid objects gone soft, small uncanny motifs. Sky #22407c -> #5f88bd -> #e9dcae; sea #8aa6b8 -> #4f6f86; rocks #e8c27a / #9a6a34; ground #d2ad70 -> #7a5129; walls #f4ead2 -> #cdbf9f; gold #f0d27c / #9a7426; dial #f6efd6.

## Build it in Remotion
px at 1920 wide; scale with the canvas.
- Layers: sky/sea/ground (static) -> shadows (per frame) -> walls -> furniture -> soft objects -> subjects. Shadows sit under walls and furniture, so the background can't be one cached image.
- Volume without lines: linear-gradient fill plus an inner shadow (a blurred dark stroke of the outline inside the shape's own clip; SVG clipPath + feGaussianBlur). No contours anywhere.
- Long shadows: each silhouette in black through matrix(1, 0, -kx, ky, kx*yg, yg*(1 - ky)), yg its ground line (x' = x + kx(yg - y), y' = yg - ky(yg - y)): shadows lie back and right from a low front-left sun. One group, opacity .55 and blur 1.5px on the group (overlaps don't darken), clipped to the ground. kx = 0.85 + 0.6*easeInOut(t/1.2): shadows visibly lengthen.
- Melt map softMap(u, v, sag) for any flat disc (clock, coin, label, screen): v <= fold lies flat (y squashed to 0.28-0.32); v > fold hangs: X = cx + u*(1 - flare*q), Y = ... + d*(0.62 + 0.3*sag) + central Gaussian droop + sine ripple. Rim, face, ticks, hands (sampled into soft polylines) and crease highlight share the map. flare -0.12 (spreads like cloth, round lower edge), drip 0.18-0.4. ~64 samples per ring into SVG paths - cheap.

## Make it move
- Melting (main action): sag 0.1 -> 1.4 over ~1.2 s (0.35 -> 1.0 didn't read); hands turning 4.5-6.5 rad/s; vary size and fold per object (R 72, 88, 64; fold -34 leaves most hanging).
- Shadows lengthening.
- A long-legged creature crossing the horizon at 70 px/s: four thin legs stepping PI/2 apart, knees at 0.52 of leg height, body bobbing 14 Hz.
- 9 ants circling a small object on ellipses; soft parts sag (tip y + q^2*34).

## Signature transition
Melt: the new shot pours down like paint. Lower edge = falling line lerp(-160, H + 40, e) + 26 round-headed drips (profile (1 - u^2)^0.3, width 10-32, length 60-280px, staggered 0-0.25, each growing over half the transition) + 24*sin(x*.005 + 1). The old shot sags in 4px columns (sag = edge*0.22*e). The edge gets an inner dark band rgba(40,20,10,.35) 9px blurred 3px and a highlight rgba(255,250,232,.7) 3px, 5px above. 0.36 s (11 frames). Custom presentation (see flat-illustration.md): polygon clip sampled every 8px, edge strokes in an overlay SVG; for DOM shots swap the column sag for a slight scaleY/translateY.

## Pitfalls
- Shadows cast toward the viewer get cut by the frame; cast them back.
- flare > 0 with a big drip makes an ice-cream cone.
- Blurred inner shadows are costly; bake static volumes.
- Dark text vanished on the deep-blue sky: cream text, dark drop shadow.
- Weakness: add finer highlights and warm ground bounce in figures' shadow sides.
