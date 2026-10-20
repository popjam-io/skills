# High Renaissance Sfumato (Leonardo, c. 1503)

> Adapted from huashu-art-motion (MIT, (c) 2026 alchaincyf) - references/风格配方/06_renaissance.md

Layer: era specimen (best for homage, journeys, era-hopping) - Upstream quality: ★★ - Known weakness: secondary characters look cartoonish and the whole shot feels static.

## Look
- Sfumato: smoky soft edges, no outlines, volume from gradients, features legible.
- Warm dark interior; an arched window onto aerial perspective (mountains bluer and paler with distance, a silver river); a perspective tiled floor lit only in a pool of window light; a dusty light shaft.
- Old-varnish surface: yellow glaze, canvas weave, faint brush texture, craquelure.
- Palette: wall `#43321f` -> `#22180e`; tiles `#a88c64` / `#5c2418`; far mountains `#9fb4b8` -> `#7d9294`; red drapery folds lit `rgba(200,70,60,.3)`, shadowed `rgba(40,0,0,.45)`; velvet sleeve sheen `rgba(170,200,140,.45)`.

## Build it in Remotion
px at 1920 wide; scale with the canvas. Upstream 16-37 ms/frame.
1. **Static room (bake)**: draw it, then copy it into the cache with `ctx.filter = 'blur(1.3px)'` for whole-scene sfumato. Floor by true projection `y = 420 + f*h/Z`, `x = 960 + f*X/Z` (f = 1029, h = 5.75, Z from 16 stepping 1.4 per row), then a soft-light pool and darkened surroundings. Landscape: 3 fbm mountain silhouettes, river width 3 -> 16 px as it nears.
2. **Characters (per frame, bounding box only)**: draw into an offscreen layer, composite twice: blurred 1.6 px fully opaque, then the sharp layer at alpha 0.82. No outlines; face lit from the left with eye-socket shadow. DOM alternative: two stacked copies, the lower with `filter: blur(1.6px)`.
3. **Overlay (bake, one drawImage per frame)**: vignette (alpha 0.3 at 0.55 radius, 0.8 at edge), yellow glaze alpha 0.07, canvas weave every 3 px, 9000 random-direction brush marks (alpha 0.022-0.028, width 5-10), craquelure (random-walk crack network, alpha 0.32) plus a white copy offset 1 px at alpha 0.16 `'lighter'` for lifted varnish edges (`filter: 'brightness(0) invert(1)'`).
4. **Light shaft**: a wedge baked with `blur(28px)`, composited `'screen'` per frame.

## Make it move
- **Main - a crafted object crossing the distance**: upstream flies a bat-winged ornithopter (Leonardo's design) past the window over ~1.35 s, path ~790 px, bob and pitch +-0.07 rad. Wingbeat `up = 0.5 + 0.5*sin(t*12 + phase)`, tips -118 to +24 px; far wing 0.78 scale, darker, phase +0.5. Wing = spar + 6 ribs + scalloped membrane.
- **Loop 1 - landscape and light**: 24 glints drift downstream and twinkle; 14 birds (scale 1-1.8); cloud shadows cross the valley; shaft brightness `0.75 +- 0.35` as clouds pass the sun; 70 dust motes rise and twinkle.
- **Loop 2 - character micro-motion**: head tilt +-0.16 rad, eyes easing shut and open, tail swing x2.2, visible breathing, hair tips +-11 px.

## Signature transition
Light bursting from the window. The new shot fades in with ease-out over p 0.05-0.5; a radial glow (r 520 at the window: `rgba(255,246,210,.85)` -> `rgba(255,220,140,.35)` at 0.35 -> 0) at intensity `sin(pi*p^0.6)`, `'lighter'`; 34 thin rays (half-angle 0.006-0.016 rad, 2400 px long) rotating 0.35 rad over the transition, `rgba(255,214,120, glow*(0.25-0.7))`. Upstream 0.4 s (12 frames). DOM-friendly: a fade presentation plus an SVG overlay of ray polygons with `mixBlendMode: 'plus-lighter'`.

## Pitfalls
- 26,000 brush marks at alpha 0.05 following noise turned the wall into Van Gogh swirls; 9000, alpha 0.025, random directions stays classical.
- Inner-edge darkening on a pale body (26 px, alpha 0.45) looks like a glass dome; use 14 px at 0.22 and blend colors with radial gradients.
- A bright, contrasty floor reads as vector art; darken outside the light pool.
- Too much blur on the subject (2.6 px, sharp layer 0.38) with a crisp window behind inverts depth; keep the subject the sharpest thing.
- Flat paper-plane wings were unrecognisable; ribs and membrane make it read.
- Weakness (static, cartoonish): run secondary characters through the same sfumato and gradient modelling, and keep many small background motions going.
