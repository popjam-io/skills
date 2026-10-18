# Egyptian Tomb Painting (New Kingdom, Amarna period, c. 1350 BC)

> Adapted from huashu-art-motion (MIT, (c) 2026 alchaincyf) - references/风格配方/02_egypt.md

Layer: era specimen (best for homage, journeys, era-hopping) - Upstream quality: ★★★ - Known weakness: raised arms (e.g. holding a cup) read stiff at the elbow.

## Look
- No perspective, flat opaque fills, clean even outlines 2.2-2.8 px in dark brown `#2a1810`. Lines never boil: the period feel comes from conventions, palette and pattern density, not brushwork.
- Conventions: profile head with a *frontal* eye (white almond, black pupil touching the upper lid, kohl line trailing ~18 px, long brow); frontal shoulders (wide trapezoid) on a profile body; a seated cat as a compact Bastet silhouette with the forelegs inside the outline.
- Hieroglyph columns between red register lines, layered friezes, a border of colored blocks with cream separators and black seams, a sun disc whose rays end in small hands.
- Linen is translucent white over skin with fine fanned pleats; broad collars of concentric colored bands with drop pendants; wigs of vertical braids with herringbone ticks.
- Palette: wall `#eadcb8`, mottled `#d8c597`; border red `#b8322a`, blue `#2a58a8`, yellow `#e2b13a`, green `#2e8a55`, separators `#f2ead6`, seams `#231a14`; gold `#e0ab38` / `#a8741c` / `#f3d27a`; deep blue band `#1c2236`; register line `#9a2b22`; sun disc `#c8372b`, rays `#c23a2a`, hands `#b4452c`; skin `#e6b282`; Bastet cat `#e08a3c`, stripes `#b45a1c`, white `#f6efe0`, eye `#e8cf4a`; scarab lapis `#2c56b0` + turquoise `#3fa6a0`.

## Build it in Remotion
px at 1920 wide; scale with the canvas. Mostly vector, so SVG works as well as canvas.
1. **Static layer (cache once)**: wall, glyph columns, furniture, friezes, color-block borders - an offscreen canvas baked in `useMemo`, or a memoized SVG subtree.
2. **Hieroglyphs**: ~24 glyph types (ankh, sun disc, bread, reed, owl, falcon, heron, horned viper, eye of Horus, cartouche, scarab, seated man, leg, arm, basket, house, three strokes, feather, djed, shen ring, jar, lotus, nfr, mouth, water ripple), each 10-20 strokes in a ~50 px box, stroke 3.1 px, round caps; author them as SVG path strings. Lay columns out once with seeded `random`: scale = column width/78 x (1.0-1.14), gaps 6-11 px; no identical neighbors, max 3 of one glyph per column, scarab and water down-weighted 60%. Store positions so animated glyphs can be redrawn per frame; keep at least 6 water glyphs.
3. **Figures**: draw conventional figures yourself rather than reusing a generic rig. Linen = skin fill, then white at alpha 0.9; ~27 bezier pleats fanning from the waist (1.3 px, `rgba(120,96,70,.5)`) clipped to the garment; chest pleats every 9 px. Collar: 5 concentric half-ellipses (blue/red/green/gold/blue, rx 50 -> 88, ry 24 -> 55) + 18 red/blue drops. Wig: clip to the wig outline, 15 braids each = 11.5 px dark-gold line + 8.5 px gold line + alternating diagonal ticks every 8 px, staggered ends. Bastet cat: one silhouette, white chest split into forelegs by two lines, tall pointed ears, frontal almond eye with slit pupil, collar clipped to body-union-head (`Path2D.addPath`) so the head outline cannot poke through the neck.
4. **Wall surface**: a baked mottled texture `multiply`-ed over the whole frame, plus grain and ~6 random-walk hairline cracks drawn *in that surface layer* so they cross figures like real plaster ageing. Bake at mount; lazy generation costs ~170 ms on the first frame.
Per-frame work is small (upstream mean ~10 ms).

## Make it move
- **Main - one slow repeated gesture**: upstream raises the cup to the lips, then loops every 0.6 s (18 frames): `cup = 1 - 0.46*(1 - cos(2*pi*u))/2`, head tilting up to ~0.2 rad while at the lips. Large local actions (arm + head) carry most of the visible motion.
- **Loop 1 - inscriptions write themselves**: every 0.12 s (~3.6 frames) pick 6 glyphs from a seeded shuffled list; erase each by redrawing the wall over its box, then stroke it in by dash progress (`setLineDash([p*95, 999])` per subpath, or `evolvePath(p, d)` from @remotion/paths) so strokes appear in order; fills appear after p > 0.55; stroke color settles from bright gold `#f6c846` to its own color with a ~10 px gold glow. 0.36 s (~11 frames) per glyph, ~18 writing at once.
- **Loop 2 - pulsing sun**: hands at the ray tips open and close with period 0.4-0.45 s (12-14 frames); ray length +-9% as a wave along the fan (phase -0.55 per ray), width 2.2 -> 3.8 px, hands scale 0.9-1.2, finger spread 0.03-0.45 rad, tips jitter +-3 px. Glow and bright ring *outside* the disc, then redraw the red disc on top.
- Extras: a scarab rolling a sun ball along a frieze at 642 px/s (21.4 px/frame), wrapping; ball rotation = x/r; legs alternate two poses every 2 frames. Water-glyph zigzags phase-step at 12 fps, 4 steps per cycle. A secondary animal's tail `2.1*tail + 0.25*sin(9.5t)`; an ear flick every ~0.38 s lasting 0.1 s (0.32-0.38 rad about the ear base).

## Signature transition
Blocks laid in like masonry (the index describes strips dropping and bouncing). Split the incoming shot into a 240x180 grid, 45% of cells split into 120x90 quarters. Block start = (center x / width)*0.62 + random*0.3, so it fills left to right with scatter; each block lands over 28% of the transition from offset dx +-30, dy -30..-80 px, rotation +-0.06 rad, scale 1.08 -> 1 with `Easing.back` overshoot, shadow `rgba(30,15,5,.55)` blur 18 -> 0, offsetY 10 -> 0. Upstream 0.42 s (~13 frames); 0.6-0.8 s reads better in an ad. Canvas shots: draw both shots offscreen and composite blocks with `drawImage` sub-rects. DOM shots: a custom `TransitionPresentation` rendering ~16-24 tile copies of the entering child (`clipPath: inset(...)` + transform each); keep the count low, every copy re-renders the shot.

## Pitfalls
- Unconstrained glyph layout fills the wall with scarabs like a sticker sheet; enforce the column rules.
- Beaded wigs read as "gold caviar"; long braids with diagonal ticks read as plaits. Separate white columns for a seated cat's forelegs read as bowling pins.
- Thin-line motifs (rays, water glyphs) barely register as motion in a small preview; treat them as garnish.
- A translucent orange pulse over the red disc turns it orange at peak.
- Clamp ray-hand positions inside their frame or lengthening rays clip them in half.
- Parts that stick out of a figure's box (tall ears, crowns) collide with nearby frames; check those clearances separately.
- Weakness (stiff elbow): support the cup from below (hand under the foot), pivot from the front shoulder, and solve 2-bone IK (upper arm 140 px, forearm 160 px) with the elbow hanging in front of the chest.
