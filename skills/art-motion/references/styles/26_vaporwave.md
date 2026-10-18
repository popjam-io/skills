# Vaporwave / cyber-neon (internet aesthetic, c. 2011)

> Adapted from huashu-art-motion (MIT, (c) 2026 alchaincyf) - references/风格配方/26_vaporwave.md

Layer: material (works on any subject) - Upstream quality: ★★★ - Known weakness: neon outlines stroked per part also glow at internal seams (waist, arm joins).

## Look
A night-purple world of neon tubes: striped sunset, magenta perspective grid rolling toward camera, palms, wireframe mountains, retro OS dialogs, a classical bust - all seen through a worn VHS tape (RGB split, tracking band, scanlines, "PLAY" OSD, timecode).
- Palette: magenta #ff4fd8, hot pink #ff2f8f, cyan #3ff6ff, deep purple #12052a / #2a0b4a, sun yellow #ffd84a, orange #ff8a3a.
- Backdrop gradient #0d0322 -> #4a0f6a; magenta radial glow behind the hero, cyan behind signage, a cyan strip along the base line.
- Neon tube = wide coloured glow + 2-3 px near-white core on the same path.

## Build it in Remotion
Sizes px at 1920 wide; scale with the canvas.
1. Scene layer (SVG suffices), then a VHS post layer. Logo, product, price and CTA sit *above* the post so split and tear never touch them.
2. Neon: stroke twice - glow (`feGaussianBlur` stdDeviation 6-10 merged under the source, or canvas `shadowBlur` 10), then the white core. Figure rim: pink clipped to the side facing the light, cyan to the far side.
3. Striped sun: disc graded yellow -> orange -> hot pink; 7 horizontal slits cut by an SVG `<mask>`, slit height 2 + q^2 * 16 px (q = 0..1 down the disc).
4. Grid floor: vanishing point (960, 600); horizontals at y = 600 + 520 / d, d = k + 1 - phase, phase = (1.3t) % 1; radials from the vanishing point; width grows toward camera.
5. Neon words as polylines in unit (u, v) glyph coordinates, 1-3 strokes per glyph: no missing glyphs, per-letter flicker. Headlines only, never the logo.
6. Ad-ready props: an OS dialog (grey body, navy gradient title bar) whose progress fills 3 + 14t cells / 18 + 70t percent; a marble bust silhouette (purple-grey gradient, veins, pink rim light).
7. VHS post:
   - RGB split: SVG filter, three `feColorMatrix` channel isolations -> `feOffset` (R -o, B +o) -> two `feBlend mode="screen"`. o = 3 + 1.5 * sin(7t), +6 when `random(`vhs-${frame}`) < 0.12`.
   - Tracking band: 70 px tall at y = (520t + 200) mod (H + 160); rows inside shift up to +-30 * sin(pi * y / bandHeight) in 6 px steps, plus ~90 white/grey noise lines. DOM route: `feTurbulence` (baseFrequency "0 0.15") limited to the band by its y/height subregion, merged over a 50% grey `feFlood`, into `feDisplacementMap` (scale ~60, xChannelSelector R).
   - Scanlines: 4 px `repeating-linear-gradient`, row 0 black alpha .28, row 2 alpha .12.
   - OSD: `@remotion/google-fonts/PressStart2P` "PLAY" + a path triangle, blinking every 16 frames; date and timecode from frame.
   Cost: the split is three full-frame filter passes; if preview stutters, split only the background, or run the post on a half-resolution canvas.

## Make it move
- One main action (product rises into the sun, the dialog completes).
- Sun slits drift at 0.9 cycles/s; grid rolls 1.3 lines/s; palms sway.
- Sign flicker: a letter is off when `random(`sign-${k}-${frame}`) < 0.07`; one letter also off 22% of the time while frame % 17 < 5. Off = dim purple tube.
- Post: split wobble, band rolling down 520 px/s, OSD blink - every frame differs (~25% upstream), which is right for this look.

## Signature transition
VHS tear + roll, 0.30 s (9 frames): sync loss rolls the frame up with a 40 px black bar, tear bands 6-54 px pull from old or new (new with probability p) shifted +-130 * sin(pi * p), magenta/cyan ghosts at +-14 px, snow lines. Recipe: ../transitions.md (vhs).

## Pitfalls
- Full-width Latin, katakana and the play triangle silently fall back to a system font. Load fonts via @remotion/google-fonts, use half-width text with 7 px letter-spacing, draw special glyphs as paths.
- Seam glow (the weakness): render the figure as one flat group and glow only its alpha edge (`feMorphology` dilate 3 on SourceAlpha, `feComposite operator="out"`, `feFlood`, blur).
- Clothing or product in the skin's hue reads as bare skin under pink light (a pink top failed; lavender #8f7cf6 with white and cyan accents worked).
