# Shadow puppetry (Chinese piying, traditional folk theatre)

> Adapted from huashu-art-motion (MIT, (c) 2026 alchaincyf) - references/风格配方/34_shadowpuppet.md

Layer: era specimen (best for homage, journeys, era-hopping) - Upstream quality: ★★★ - Known weakness: overlapping pieces multiply to near-black, and it is heavy per frame (every piece multiplied separately).

## Look
Translucent dyed leather with carved openwork, riveted joints and thin rods, pressed on a cloth screen lit from behind by an oil lamp whose warm radial glow breathes. Light through leather multiplies with the screen, so overlaps darken. Stepped motion (10 fps), stiff joints, loose wrists. White is never painted - it is cut out. Strong for Lunar New Year, Mid-Autumn and heritage campaigns.
- Leather: red #c0352a, green #2f7d4c, amber #d99a2e, yellow #e2bd4a, blue #2c5a8a, orange #d9782a; edge #3a160a.
- Screen: radial #fff6d6 -> #f2d7a0 -> #cf9a58 -> #7a4a20.

## Build it in Remotion
Px at 1920 wide; scale with the canvas.
- Screen: radial gradient + a screen-blended wick hotspot (radius 260 + 40fl) + a static 3 px cloth weave (two crossed `repeating-linear-gradient`s at low alpha). Flame fl = 0.5 * noise2D('fl', 3ts, 0) + 0.3 * noise2D('fl2', 9ts, 0), ts stepped at 15 fps; the light centre drifts +-26 / +-18 px.
- A piece (SVG): fill -> carve the pattern out via a `<mask>` (white shape, black pattern) -> keep a same-colour leather rim 2 x edge wide (white rim stroke in the mask, clipped to the shape) so carving never breaks the outline -> 2.6 px #3a160a edge.
- Carving `<pattern>`s: fish-roe dots (spacing 14-22, r 3-3.5), five-petal ellipse flowers (36-46), small Archimedean cloud spirals (line 3.4, spacing 24-40), lattice (26-32), carved lines (width 3-7).
- White = cut out: white chest, muzzle, paws, collars become openings with only a leather rim; stripes become carved lines. Graceful faces are "empty": carve the face out, keep the profile line, add a long upswept eye line with lower lid and dot, a willow-leaf brow, a dot of lip. Holds for every silhouette or openwork style.
- Stamping: per puppet, a ghost copy first (alpha .28, blur 6, offset (7, 5) - leather not flush with the cloth), then the puppet; both `mixBlendMode: 'multiply'`.
- Rods: 5 px dark brown, blur 1.2, multiply, from neck, wrist and head to the bottom edge. Wooden frame around the screen.
- Cost: per-piece blur and multiply made upstream slow. One ghost per puppet (not per piece), cache static props, and since motion steps at 10 fps, key canvas redraws on `Math.floor(frame / 3)`.
- Real product/logo: an image on the screen or the wooden frame; don't multiply a logo into the cloth if that kills its colours.

## Make it move
At 10 fps unless noted.
- Figure sways +-0.012 rad around its base; head turns +-0.06 rad on the neck rivet.
- Loose wrist: dangle = 0.35 * sin(11ts) * (1 - 0.6 * lift); a held object swings with the hand.
- Secondary puppet nods 0.1 * sin(6ts) + 0.05; tails and streamers as 4-link hinge chains, each link rotating 0.3 * sin(7ts - 0.9i) + 0.38 relative to the last, so the tip whips late. Bead strands swing.
- A butterfly on a rod flips its wings by scaleX at 12 fps; lamp flicker makes the whole screen breathe.

## Signature transition
The lamp lights up, 0.4 s (12 frames): the old shot darkens like a lamp going out, then the new screen glows open from the lamp in a soft radial reveal with flame jitter and a warm flare. Recipe: ../transitions.md (lampGlow).

## Pitfalls
- A table leg over a skirt multiplied red x green into a black trapezoid. Dark overlaps are authentic - keep them off faces and the product.
- A solid orange leg covered a white chest; white parts must be openings.
- Rods crossing the subject are a mess; rods run down and outward, never across another figure.
