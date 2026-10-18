# Dunhuang cave murals (Mogao Caves, High Tang)

> Adapted from huashu-art-motion (MIT, (c) 2026 alchaincyf) - references/风格配方/20_dunhuang.md

Layer: era specimen (best for homage, journeys, era-hopping) - Upstream quality: ★★ - Known weakness: the flying apsara figure is crude.

## Look
Mineral pigments on earth-red plaster; uniform "iron-wire" contours; flying celestials trailing silk ribbons; scrolling-vine borders and triangular valances; centuries of fading, smoke and flaking down to pale plaster. Line #5a2414 (faces #8a3a24); earth red #a5452f / #7a3020; malachite #3f8f6e / #6ab08e; azurite #2f5f8f / #5a86b0; white #ecdfc4; gold #d8b05a; plaster #d8c6a2.

## Build it in Remotion
px at 1920 wide; scale with the canvas. Static layers once (canvas or SVG).
- Ground: noisy earth red, faded rosettes; a scrolling-vine border with a valance (green, white, red, gold beads); lotus-tile floor. Line: uniform 2.6px.
- Tang costume (for a person): red skirt with slanted green stripes every 44px fanning downward; azurite jacket, white crossed collar, high red sash; high bun (two ellipses) with gold pins and flowers; forehead flower, red temple arc (alpha .32), dotted lips, moth brows.
- Silk ribbon: travelling-wave ribbon with a white dashed line and red dots; trailing part x = back + 230q + 64q*sin(4.2q - 5.5t), last 30% curling up; front part drapes over the arm.
- Aging (static): desaturate ~30%, multiply an earth texture at .5; flake where fbm(x*.0032, y*.0032) + 0.12*noise(x*.03, y*.03) > 0.3 down to #d8c6a2, dark edge in the 0.28-0.30 band; 500 random-walk cracks; smoke over the top 380px. Mask faces and main subjects out of the flaking. SVG: feTurbulence (~0.0032) + discrete feComponentTransfer as a mask.

## Make it move
- Flying apsara (main action): reclining, 1.35x, crossing at 300 px/s; three wave ribbons, one arcing from shoulder over head and flung behind (the signature shape); halo, bun, flower tray.
- 30 four-petal flowers spin and flip (scaleX = cos) as they fall; clouds (puffs with tapering tails) drift 40-76 px/s.
- Lamp flame 1 + 0.12*sin(17t) + 0.08*sin(29t) with glow; 10 paint flakes peel off, flip, fall on parabolas.
- Two motions per subject (upstream added a head turn sin(2.6t) and 2.5x breathing).

## Signature transition
Apsara ribbons sweep right to left with the new mural behind the front, x = lerp(W + 260, -300, e) + 110*sin(y*.006 + 5p); chips of the old picture flip and fall there (y += age^2*900); three ribbons ride it - #6ab08e, #a5452f, #5a86b0, 44/38/32px, outlined #5a2414 2.4px, white dashed [4,10] centre line. 0.5 s (15 frames). Custom presentation (see 16_2026.md): polygon clip, SVG ribbons; for DOM shots use plaster-coloured chips.

## Pitfalls
- Ribbons swinging 18-34px and hanging vertical read as a chair rail; >200px sideways and an upturned tail read as silk.
- Flaking noise at .006 = sesame-seed stains; .0032 with a higher threshold = patches.
- A solid green halo reads as a swim ring: .28 translucent fill, thin line.
- The fade muddies saturated colours (#c8843a went brown); pre-boost (#e08a3a).
- Weakness: draw the apsara a real reclining pose, not a stretched icon.
