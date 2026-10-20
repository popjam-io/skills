# Rubber-hose cartoon (American animation, 1930s)

> Adapted from huashu-art-motion (MIT, (c) 2026 alchaincyf) - references/风格配方/33_rubberhose.md

Layer: era specimen (best for homage, journeys, era-hopping) - Upstream quality: ★★★ - Known weakness: most of the measured motion is film noise, not character animation.

## Look
Monochrome on warm paper, animated on twos, everything bouncing to the beat. Big round heads, pie-cut eyes (black pupil with a wedge missing), constant-width noodle arms, white four-finger gloves with flared cuffs, rubbery smooth bodies, a smiling sun, dancing flowers. Old film over it all: gate weave, flicker, scratches, dust, grain, a round-cornered gate with vignette. Good for nostalgic, playful, "since 19XX" spots.

## Build it in Remotion
Px at 1920 wide; scale with the canvas.
- Background (cached): paper-tone wallpaper stripes with diamond dots, floor seams, darkened watercolour corners.
- Time: tq = `Math.floor(frame * 12 / 30) / 12` (on twos) for characters, motifs and the main action; the film layer steps at 24 fps (`Math.floor(frame * 24 / 30)`).
- Beat bounce: bnc(tq, ph) = |sin(pi * (tq / BEAT + ph))|, BEAT = 60/128 s (match the music). Each object hops `amp` px off its own ground contact; landing squash sx = 1 + 0.09k, sy = 1 - 0.09k; airborne stretch ~5%. Offset phases by quarter beats (e.g. 0.5 / 0.25 / 0.75 / 0); accessories 0.05 beat behind their body = follow-through.
- Character kit: head r 82; pie-cut eyes (white eye, black pupil minus a wedge from -1.45 to -0.85 rad, 3 lashes); hose arm = one quadratic Bezier shoulder -> hand at constant width, black outline 10 px wider (stroke twice); glove with 4 fingers, flared cuff, 3 back lines; tails as wavy hoses offset sin(7q - 9tq) * 26q along length q.
- Smooth every body outline (quadratic curves through segment midpoints).
- Mono pass, once, after all characters: wrap the scene in `filter: 'grayscale(1)'` and lay a `mixBlendMode: 'multiply'` #f2e8d2 layer over it.
- Film layer (overlay, seeded per film frame): gate weave +-1.5 / +-2 px; flicker = white alpha .02-.09 then black 0-.06; 3 vertical scratches repositioned at 6 fps (`Math.floor(frame / 5)`) so each lives several frames; 14 dust specks per frame, an occasional hair; cached grain translated +-20 px per frame; rounded gate (radius 60) with vignette.
- Brand colours cannot survive the mono pass; put the real logo on a title or end card outside the filtered wrapper.

## Make it move
- Everything bounces on the beat.
- Sun face: rays rotate 1.6 rad/s, the face nods on the beat. Dancing flowers: stems +-0.35 rad, leaves wave like hands, petals spin. One smoke ring per beat; curtain hems whip on the beat.
- Fix the weakness: give the hero a real action (walk cycle, anticipation-take-recoil, double take, landing squash) and keep the film layer subtle.

## Signature transition
Iris out, iris in, 0.4 s (12 frames): the old shot turns sepia and contrasty as a black iris closes on a focal point; the new shot bursts open from the same point with an overshoot; film flicker throughout. Recipe: ../transitions.md (irisFilm).

## Pitfalls
- Polyline bodies read as cut cardboard; smooth them.
- Desaturate once, at the very end, after the characters; otherwise gloves and props keep warm tints.
- Film noise must not be the main motion (the weakness).
