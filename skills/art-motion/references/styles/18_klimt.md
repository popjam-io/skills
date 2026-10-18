# Klimt golden phase (Vienna Secession, 1907)

> Adapted from huashu-art-motion (MIT, (c) 2026 alchaincyf) - references/风格配方/18_klimt.md

Layer: era specimen (best for homage, journeys, era-hopping) - Upstream quality: ★★★ - Known weakness: a hand resting on a surface did not connect to its sleeve.

## Look
Flat gold-leaf ornament against softly modelled, naturalistic faces and hands - that contrast is the style. Gold ramp [120,78,18] -> [196,148,52] -> [246,216,128] with faint square seams; robes of spirals, eyes, concentric circles, black-white rectangles; flower carpets; black-white checker furniture.

## Build it in Remotion
px at 1920 wide; scale with the canvas.
- Gold leaf (static): f = 0.5 + fbm(x*.004, y*.004)*0.55 + noise(x*.003, y*.08)*0.5 +- 0.05 through the ramp (anisotropic term = burnished streaks); seams every 96px; walls multiplied by an upscaled 480x270 fbm (brown-gold mottling) plus 9000 gold and dark specks. Bake at half res, or SVG feTurbulence (baseFrequency "0.003 0.08") + feComponentTransfer into the ramp.
- Robe: 150 ornaments - concentric circles in red-white-blue, blue-gold-red, purple-white-gold (30%); gold spirals on dark brown rotating up to +-3 rad/s (32%); eye motifs (22%); white dot clusters with a red centre (16%); a hem of 60 tall black-white rectangles outlined in gold. One ornament group clipped once to the robe; 3px dark robe outline.
- Face and hands: radial #fbe8da -> #f0cfb8 -> #d8a88c -> edge #b88068, blurred blush and eye sockets, a 1.2px faint outline only.
- Extras: pointillist birches (2600 autumn ellipse dots, 6 white trunks with black marks); 260 concentric-circle flowers growing 6 -> 20px toward the viewer.

## Make it move
- Light sweep (main action): a 520px band, alpha .24, sheared matrix(1,0,-0.45,1,0,0), additive, uniformly -200 -> 2300px in 1.15 s (~35 frames), drawn behind the subjects.
- Eye motifs blink in turn: closed while sin(2.2t + phase) > 0.86.
- 420 gold specks flash four-point stars while sin(t*speed + phase) > 0.55 (radius s*(0.6 + 1.1a)), rising 26 px/s; 34 flakes flip (scaleX = cos) and fall 150 px/s; flowers nod sin(4.2t + phase)*0.35r.

## Signature transition
Gold leaf: 72px leaves land in spiral order from the subject's head (key = distance*0.78 + angle*0.12 + random*0.08), settling from 1.3x with a small rotation, gradient #a8741e -> moving #fbe6a0 -> #c8962e, embossed with a spiral, eye or circles (rgba(70,40,10,.75), 2.2px); seated leaves fade to reveal the new shot. 0.5 s (15 frames). Custom presentation (see 16_2026.md): entering scene `clipPath: path(...)` of seated tiles, moving tiles as SVG rects.

## Pitfalls
- Canvas source-in per ornament wipes earlier ones; composite all, clip once.
- Sweep at alpha .38 reads as lens flare.
- Intermittent blinks plus a soft sweep left near-identical frames; continuous carriers (flakes, dust, bigger nods) fixed it.
- Big stars read as Christmas decoration; spirals on an animal's face read as a rash - body only, ~46.
- Weakness: build sleeve and hand as one shape where ornament meets anatomy.
