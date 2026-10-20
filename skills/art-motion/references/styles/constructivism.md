# Russian Constructivist poster (Rodchenko, El Lissitzky, 1924)

> Adapted from huashu-art-motion (MIT, (c) 2026 alchaincyf) - references/风格配方/22_constructivism.md

Layer: material (narrow use: posters, slogans, calls to action) - Upstream quality: ★★★ - Known weakness: missing Rodchenko's megaphone-shaped text cone.

Evoke the technique; never copy a specific work.

## Look
Aged paper, red and black only, hard diagonals, a red wedge against a black circle, halftoned photo cut-outs with white cut edges montaged with crisp line drawing, letters built from rectangles. Paper #e9dfc4 (dark #d9c9a4), red #c8231c / #8f1711, black #151311, off-white #f4ecd6, orange #e2741c, gold #e3b03e / #a87a1c.

## Build it in Remotion
Static poster in a cached layer; px at 1920 wide; scale with the canvas.
- Kit: diagonal black bar (-0.5 rad), red square (0.26 rad), 5 rows of black "body text" bars, thin diagonal rules, a red dot, a black vertical bar with stacked letters, a big black circle behind the subject's head (r 215), a slanted red ground (y 905 left -> 856 right of 1080) with a 12px black top edge, black furniture with red edges.
- Halftone(src, cell, colour, gain, angle = PI/4): sample source luminance L on a rotated grid; dot radius cell*gain*sqrt(1 - L), only where alpha > 128; merge all dots into one path, fill once (a face ~3000 dots is cheap). Backdrop photo: cell 7, gain 0.8. Skin: cell 4.6, gain 0.74 from a greyscale gradient (#fafafa lit -> #9c9c9c) over an off-white underlay, then a 7px #fbf7ea outer stroke = the cut-out's white edge; crisp black pen features and hand-reddened lips on top. Clothes: flat cut paper + 3px black line, shadows as halftone dots inside the path.
- Montage: a halftoned greyscale "photo" (sky #5e5e5e -> #e8e8e8, white clouds, factory silhouettes) with a crisp line structure over it (e.g. a hyperboloid lattice tower: five sections, two families of 18 straight lines phased +-1.1 rad, back-facing lines dropped). To halftone a real product photo, draw it to a canvas and getImageData: it must be same-origin (staticFile) or CORS-enabled, or the canvas is tainted.
- Letters on a 5x7 module, each a few rectangles/quads, each part filled separately. Build Latin letters the same way for the brand's copy rather than faking Cyrillic.

## Make it move
- Slogan stamp (main action): letter k lands at 0.045k s, scale 1.5 -> 1 over ~4 frames; then the row wave-jumps -10*max(0, sin(11t - 0.8k)); every 4th letter black, the rest red.
- Red wedge thrusting into the circle: tip moves 70*(0.5 - 0.5*cos(2*PI*1.6t)) px along a 0.34 rad axis.
- Red dashed ring round the circle: dash [46, 22], strokeDashoffset -260t.
- Radio waves: 4 red arcs, r = 18 + ((1.4t + k/4) mod 1)*230, alpha and width fading with phase.
- Flutters: scarf tails sin(9t)*6; steam as three rising black zigzags.

## Signature transition
Red wedge: a #c8231c triangle (520 long, 660 tall) stabs along a -0.32 rad axis from lower left across the frame; the new shot is revealed 420px behind the tip; three black type bars (26/18/34px tall, lagging 0/0.12/0.2) chase it. 0.4 s (12 frames). Custom presentation (see flat-illustration.md): entering scene `clipPath: polygon(...)` in the rotated frame, wedge and bars as SVG polygons.

## Pitfalls
- Overlapping parts of one letter in a single path cancel under nonzero winding ("A" read as "B"); fill parts separately.
- Keep accents inside the letter cell or neighbours cover them; draw slogans above figures (type overlays people) and anchor them by centre so they stay in frame.
- Cheek shadows halftone into a beard: use half the shadow alpha you would for flat paint.
- Weakness: add the megaphone cone - red and black wedge-shaped text radiating from a source (a mouth, a megaphone, the product). A natural CTA device.
