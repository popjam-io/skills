# Anime light and sky (Makoto Shinkai style, contemporary Japanese animation, 2016)

> Adapted from huashu-art-motion (MIT, (c) 2026 alchaincyf) - references/风格配方/35_shinkai.md

Layer: material (works on any subject) - Upstream quality: ★★ - Known weakness: the interior background was not dense enough; this look lives on hyper-detailed backgrounds.

Evoke the technique; never copy a specific work or character.

## Look
Photo-detailed backgrounds under towering cumulonimbus, god rays, lens flare, bloom, warm/cool split toning; cel characters with one hard shadow band and a thin lit rim; window light patches on floor and wall; droplets on glass, sheer curtains, power lines, contrails, birds, dust. A living still: little moves, everything breathes.
- Character colours (base / shadow): skin #ffe8dc / #f2b6a8, blond #f8d681 / #d8a050, white shirt #fbfbfe / #b9c3dc, navy #2c3a66 / #1b2446; line #6a4632, 2.2 px.

## Build it in Remotion
Px at 1920 wide; scale with the canvas. Order: detailed interior (cached) -> sky, clouds, wires, roofs, contrail, birds -> droplets -> curtain -> window light patches (curtain shadow moving inside) -> plants -> cel characters -> steam -> god rays + dust -> flare -> bloom -> soft-light split toning.
- Cel shading (SVG masks, as in 27_kirby): shadow = shape minus a copy shifted (lx, ly) * sd; rim = shape minus a copy shifted -(lx, ly) * rw. Window light lx = -1, ly = -0.55 (shadows lower right); sd 22-30 big parts, 10 face, 8 small; rw 3-9. Per part fill -> shadow -> rim -> line, so occlusion comes out right. Backlit subject: lx 0.5, ly 1, plus an additive warm rim rgba(255,220,160,.55) along the top.
- Hair "angel ring": a 9 px arc rgba(255,250,226,.85). Eyes: iris gradient #1f3f7a -> #3f7fd0 -> #9fd4ff, two highlights, 3.4 px upper lid with one corner lash.
- Cumulonimbus (~80 puffs): blue-grey silhouettes (gradient #b7c6e6 -> #8297c6); per puff a white radial ball of 0.82r offset toward the sun by (+0.22r, -0.3r); the group drawn once with `feGaussianBlur` 3 and once sharp at opacity .55 on top.
- Lens flare (sun inside the glass): core r130; 10 spikes (90 / 170 long) turning 0.25 rad/s; an 840 x 4 streak at alpha .35; 5 hexagon ghosts (`@remotion/shapes` Polygon) on the sun -> centre line at 0.45 / 0.75 / 1.25 / 1.6 / 2.0, alpha .04-.12.
- God rays: 3 wedges blurred 18 px (cached), `mixBlendMode: 'screen'`, alpha 0.75 + 0.25 * sin(3.4t); 60 twinkling dust motes.
- Bloom: on canvas, draw the frame at 480 x 270, blur 6, brightness 1.1, screen it back at alpha .28; in DOM, duplicate only bright layers (sky, sun, rays) with `blur(24px) brightness(1.1)`, screen, opacity .28.
- Split toning: soft-light overlay, warm highlights, cool shadows.
- The real product gets the same rim light and a cast shadow along (lx, ly) so it belongs.

## Make it move
- Puffs breathe 0.05 * sin(1.3t) in radius; the bank drifts 10 px/s.
- A contrail extends; birds flap; a droplet slides down the glass leaving a trail; curtain and its wall shadow sway; leaves and hair stir; flare spikes turn; rays pulse; dust drifts.
- One main character or product action; the rest stays subtle (~3% of the frame moving upstream).

## Signature transition
Diagonal light sweep, 0.38 s (11 frames): a slanted boundary sweeps left to right with warm, white and cyan light bands riding it, plus streak, particles and hexagon ghosts. Recipe: ../transitions.md (flareSweep).

## Pitfalls
- A sun on the window-frame corner spilled flare onto the wall like a lamp; keep the sun inside the glass, flare radius <= 130.
- One radial gradient per puff plus a lit arc made soap bubbles; use silhouette + offset ball + blurred/sharp layers.
- An 1800 px streak looked like a bug; keep ~840 px near the sun at alpha .35.
- Solid-circle droplets read as bubbles in the sky; draw the lower rim arc, a .22-alpha body, one highlight dot.
- One runtime error in a big scene component can blank the shot; check preview frames show the scene.
- Density (the weakness): layer perspective clutter (shelves, cables, posters with invented shapes, plants), or go outdoors where sky and light do the work.
