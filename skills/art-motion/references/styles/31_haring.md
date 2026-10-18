# Pop graffiti line (Keith Haring, 1982)

> Adapted from huashu-art-motion (MIT, (c) 2026 alchaincyf) - references/风格配方/31_haring.md

Layer: era specimen (best for homage, journeys, era-hopping) - Upstream quality: ★★★ - Known weakness: the realistic main character was not Haring enough; subjects must be reduced to the same thick-line icon language.

Evoke the technique; never copy a specific work or character (invent your own icons, not his recurring figures).

## Look
Solid ground colours; everything is one uniform round-cap black marker line plus flat fill; featureless figures; short straight "action lines" radiating around anything that moves; dancing figures; the whole world bouncing to a beat.
- Palette: yellow #ffd51c, green #16a54a, red #e8262b, blue #1f62d6, pink #ff6fb0, orange #ff8a1c, white, ink #111111, skin #ffd9b8.
- Line 13 px, round caps and joins (px at 1920 wide; scale with the canvas); a 14 px horizon line.

## Build it in Remotion
SVG; very cheap.
- Every shape: `stroke="#111111" strokeWidth={13} strokeLinecap="round" strokeLinejoin="round"` + flat fill. No thin lines anywhere.
- Dancing figure: 7 capsule limbs + round head. Stroke all parts at 26 px first, then fill all parts unstroked: one merged silhouette, no internal lines. 4 keypoint poses (origin at the feet), hard-cut at 8 fps, no interpolation: `POSES[(Math.floor(frame * 8 / 30) + phase) % 4]`. Short motion arcs beside the hands.
- Action lines: n short lines (length 22-34, width 7-9) on an ellipse around the object, angles re-dealt at 8 fps via `random(`rays-${id}-${Math.floor(frame * 8 / 30)}`)`.
- Beat: bounce = |sin(t * BPM / 60 * pi)|^0.6 (128 BPM upstream; use the ad's music). Subject dy = -12 * bounce, secondary elements half a beat later. Furniture squashes around its base (scaleY 1 - 0.07(1 - b), scaleX 1 + 0.05(1 - b)); small objects hop 26 px; frames rock +-0.025 rad; jump ticks under feet change length with the beat.
- Product: keep the real cut-out image, add a 13 px black sticker outline (`feMorphology` dilate on SourceAlpha, filled #111, under the image) and action lines. Never redraw the logo as marker art.

## Make it move
- Main action on the beat (product hop, reveal, dance).
- Three wall dancers (red / blue / pink, phase-shifted, one mirrored).
- A red heart beating at 1 + 0.15 * bounce, with its own action lines.
- A radiating icon of your own whose 14 rays alternate 66 / 40 px at 8 fps; a two-frame crawl or wave cycle.

## Signature transition
Dancing-figure reveal, 0.32 s (10 frames): a V-armed figure grows from the focal point (scale 0.15 * 320^easeInOut(p)) with the new shot inside its 30 px black-outlined body; 16 action lines jump at 8 fps. Recipe: ../transitions.md (radiant).

## Pitfalls
- Capsule limbs with reversed end caps leave holes at joints under thick strokes; use round caps and overlapping joint circles.
- Window bars and frames go under the figure.
- Thin hair lines break the uniform line and poke through the face when the head tilts; remove them.
- Realistic people never read as Haring (the weakness): reduce characters to icon figures (at most an eye dot and a lip mark) and keep realism only in the composited product image.
