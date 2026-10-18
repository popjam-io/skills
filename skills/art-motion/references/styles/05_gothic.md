# Gothic Illuminated Manuscript (c. 1290)

> Adapted from huashu-art-motion (MIT, (c) 2026 alchaincyf) - references/风格配方/05_gothic.md

Layer: era specimen (best for homage, journeys, era-hopping) - Upstream quality: ★★★ - Known weakness: blond hair reads as a hood.

## Look
- Burnished gold ground tooled with a diamond lattice; gables, pinnacles, pointed arches, stained glass; blackletter columns with vermilion first words; marginal drolleries (snail, knight, mouse).
- Gold reads as metal through fine horizontal burnish grain plus moving highlights. Flat-colored figures with dark outlines, tooled halos, robes with gold pinstripes. Animals act like drolleries: human-like face, side-eye, raised brows.
- Palette: parchment `#ecdfc2`; gold low `#9c6a1a`, gold `#d9a63a`, gold high `#f8de86`; red robe, blue cloak with gold edge; ivy leaves rotating blue / red / gold.

## Build it in Remotion
px at 1920 wide; scale with the canvas. Upstream 11-22 ms/frame.
1. **Static page (bake once)**: parchment, gold, tooling, architecture, window, text, margins.
2. **Gold leaf (per pixel, baked)**: `f = 0.52 + 0.42*fbm(x*0.0035) + 0.5*noise(x*0.004, y*0.09) + top-left light + grain +-0.05`, interpolated across gold low / mid / high. y frequency >= 20x x frequency gives horizontal brushed metal. Lattice: spacing 46 px, diagonals x+y and x-y, each drawn twice (dark, then light offset 1.2 px) so it looks tooled; 4 light/dark dots per diamond center. Faint leaf seams every 118x125 px.
3. **Gold mask (derived, baked)**: alpha = `clamp((r-b-70)/50) * clamp((g-b-30)/40) * clamp((r-140)/40)` over the baked page. Parchment (r-b = 42) and pinks (high b) drop out; every gold element is selected without redrawing shapes.
4. **Moving highlight (per frame)**: a diagonal gradient band (slope 0.45, "/" direction) on a ~920 px scratch canvas, `destination-in` the gold mask, composited `'lighter'` at alpha 0.85. DOM alternative: a gradient div with `mixBlendMode: 'plus-lighter'` and `maskImage` set to the mask's data URL (export once). Four-point star sparkles at fixed points light up while `|u - sweepX| < 70`.
5. **Text**: blackletter (UnifrakturMaguntia via @remotion/google-fonts) at 44 px; at 50 px a line overflowed the page.
6. **Figures**: draw parts yourself, in order, so cloak and halo sit between layers: halo (offset (16, -22) from the head, r 114, red ring + 36 punched dots) -> long wavy hair -> robe (gold pinstripes every 20 px, gold hem) -> cloak anchored at nape and back, gold edge -> head -> gold chalice.

## Make it move
- **Main - gold highlight sweep** at constant speed (~1300 px/s upstream; slower in ads), timed to cross the subject mid-shot.
- **Loop 1 - ivy vines**: two stems of ~120 points displaced `5*sin(t*2.1 + i*0.09)`; every 3-5 points a three-lobed leaf (scale 1.05-1.45) or a gold ball with 3 tendrils; leaves swing `0.42*sin(t*3.1 + k*1.7)` about their stem point.
- **Loop 2 - glass and drolleries**: 40 glass points light a white radial glow while `sin(t*5 + h*40) > 0.6`; a snail creeps 62 px/s with waving antennae; a mouse dashes ~360 px in ~1 s; a secondary character dangles something by a string like a pendulum `0.32*sin(t*5.5)`.

## Signature transition
Parchment page turn: a 260 px curl band moves right to left, `x = lerp(W + band, -1.4*band, easeInOut(p))`. Old page left of the curl; the curl shows parchment `#e9dcc0`, the old image mirrored at alpha 0.18 (show-through) and cylinder shading (`rgba(60,40,20,.45)` -> `rgba(255,248,230,.25)` at 0.18 -> `rgba(120,90,50,.12)` at 0.55 -> `rgba(40,25,10,.55)`); a 90 px shadow falls on the new page. Upstream 0.32 s (~10 frames); 0.6-0.8 s in an ad. Remotion: custom presentation; exiting child `clipPath: inset(0 ${W - x}px 0 0)`, curl and shadow as gradient divs (the mirrored show-through is optional: it re-renders the old shot).

## Pitfalls
- An in-out eased highlight left the gold before reaching the subject; use constant speed.
- Leaf scale 0.85 looked sparse.
- Weakness (hair as a hood): the hair mass framing the face reads as one cowl. Break the silhouette into locks, show the hairline and forehead, and separate hair from halo with an outline or a contrasting halo color.
