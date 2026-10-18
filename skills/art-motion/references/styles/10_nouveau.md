# Art Nouveau Poster (Mucha style, 1896)

> Adapted from huashu-art-motion (MIT, (c) 2026 alchaincyf) - references/风格配方/10_nouveau.md

Layer: era specimen (best for homage, journeys, era-hopping) - Upstream quality: ★★★ - Known weakness: secondary characters keep stiff, generic poses.

Evoke the technique; never copy a specific work or character.

## Look
- Whiplash curves whose line weight swells and tapers; heavy outer contours with thin inner lines; halo discs and rosettes behind heads; flowing hair in S-locks ending in spirals; flat pastel lithograph color with mottled print grain.
- Gold-ruled frame, dot-lattice ground, leaded stained glass, mosaic band, title banner.
- Palette: background `#b9cba0` -> `#cfd3a6` -> `#ecc9a2`; dots `rgba(120,140,100,.38)`; banner `#8fac80`; line `#4e3320`; gold `#c9a24a` / `#9c7a2e`; cream `#f6eedb`; skin `#f6dcc4`; hair `#e8bf55` / light `#f6dc8a` / dark `#b9862a`; dress `#f4ecda`; pink scarf `#e6aaa5` / fold `#d48e8c`; poppy `#d9706a` / `#b4504b`, center `#3f6a4a` with gold dots; lily `#f7f2e6`; ironwork `#3d7763`; halos pink `#ebb8b2`, teal `#5f9a8a`, red `#b8473a`; animal `#e39a4c` / `#fbf3e3` / stripes `#c0672c`, eye `#e6c040`.

## Build it in Remotion
px at 1920 wide; scale with the canvas. Upstream ~29 ms/frame.
1. **Background (bake)**: three-stop vertical gradient; dot lattice (ring r 10 + dot r 2.6, rows 54 px, columns 62 px, odd rows offset 31); lithograph mottling from a 240x135 fbm image upscaled at alpha 0.5; mosaic band of 20x24 tiles cycling 9 colors by `(k*7 + (k>>2)) % 9`; title in a classical display face (e.g. Marcellus 76 px, letter spacing 12) with a 7 px dark stroke under a cream fill; gold frame 6 px between two 2 px dark rules.
2. **Variable-width ribbon** for every whiplash line (stems, leaves, iron legs, banner scrolls, hair, steam): densify control points with Catmull-Rom (4-10 per segment), offset each point +-w(q)/2 along its normal, fill the closed polygon (canvas or an SVG `<path>`). Swell `w(q) = wmax*sin(pi*q)` tapers both ends; spiral terminals shrink the radius linearly to 15%. `getPointAtLength` / `getTangentAtLength` from @remotion/paths give points and normals.
3. **Thick-outside, thin-inside contour**: draw characters with 2 px inner lines into one layer, then draw dark `#4e3320` silhouettes of that layer underneath at offsets (-1.5, -1.5), (3.5, 4.5) and (2, 2.5): a 1.5 px rim plus a 4-5 px weighted lower-right edge. Canvas: tint a copy with `source-in`, 3 extra drawImage calls. DOM/SVG: `filter: 'drop-shadow(-1.5px -1.5px 0 #4e3320) drop-shadow(3.5px 4.5px 0 #4e3320) drop-shadow(2px 2.5px 0 #4e3320)'` on the character group.
4. **Grain**: warm brown specks, density 0.05, alpha 0.14, on top.

## Make it move
- **Main - sun rising in the window**: ~288 px/s upward (9.6 px/frame) with -20 px/s drift; hills drawn after the sun occlude it. 14 lead lines radiate from the sun (r 92 -> 420), turning 0.225 rad/s with +-0.04 sway; because they follow the sun, every glass division shifts - the most visible motion. Stained-glass border chips (14x14 every 17 px along the arch, tangent-rotated, 6 colors).
- **Loop 1 - turning halos**: subject halo R 172 with 18 studs at +0.9 rad/s and an inner 32-petal rosette at -0.63 rad/s; a smaller halo R 106 with 8 petals at -1.1 rad/s and a dashed gold ring (`strokeDashoffset` advancing).
- **Loop 2 - flowers, hair, steam**: flower heads `13*sin(7.5t + phi) + 5*sin(3.1t + 2phi)` px, moving only the stem's upper control point, leaves 0.3x, left and right clumps in opposite phase. Hair: an outer mass edge rippling `9*sin(6t + y*0.035)`, plus ~9 locks as 12-point S-curves `sin(7.4q + phi - 7t)*(6 + 20q)` (a wave travelling down), ending in 1.2-turn spirals, width 14-18 -> 2.5, cream highlight core + dark gold edge, following the head less toward the tips. Steam: 3 cream ribbons (26 / 20 / 14 wide, 1.8 px brown edge) waving `sin(4q + phi - 6t)*(18 + 70q)`, spreading x(1 + 2.6q), 34 px spiral tips.

## Signature transition
A gold-rimmed organic shape grows from the subject's head and swallows the frame. `R = (0.7*easeOut(p) + 0.3p)*2300`, radius per angle `R*(1 + 0.22 sin(3a + 0.7) + 0.12 sin(5a + 2.1) + 0.06 sin(9a + 3p))`, y squashed 0.92, 120 points; the new shot shows inside; rim stroked 14 px `#6b4a24` then 8 px `#d9b25a`. Upstream 0.24 s (~7 frames); 0.5 s in an ad. Remotion: a custom presentation with `clipPath: path('M...Z')` on the entering child and an SVG rim overlay.

## Pitfalls
- Outlines drawn in a final line pass cut hidden parts (a far sleeve) through the body; draw lines inside the character layer in part order, then apply the contour trick.
- Hair as a few 34 px ribbons looks like sausages; a mass plus fine S-locks (<= 18 px) with spiral ends reads as nouveau.
- Steam rising straight up crosses the face when a cup is at the lips; lean it away as the cup rises (`lean = -90 - 160*cup` px).
- Weakness (stiff poses, stock lettering): give secondary characters a reclining, flowing contour drawn with the same ribbons, and draw custom rounded letterforms instead of a stock font.
