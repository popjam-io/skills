# Early ray-traced CGI (early 3D renders, 1993)

> Adapted from huashu-art-motion (MIT, (c) 2026 alchaincyf) - references/风格配方/15_raytrace.md

Layer: material (narrow use) - Upstream quality: ★★ - Known weakness: organic subjects become toys (legs as straight columns, face like a mask).

## Look
Glossy plastic everything under one shading convention; chrome spheres; a reflective perspective checkerboard; pink-purple sunset with wireframe mountains; lens flares. Wall radial #7dbcb9 -> #64a6a6 -> #3f8285 (lit from the window); sky #a24cc4 -> #df62ae -> #f5a08a -> #f8c070.

## Build it in Remotion
Fake it in 2D, or use @remotion/three for real reflections (drei MeshReflectorMaterial, metalness 1 / roughness 0 spheres). 2D, px at 1920 wide; scale with the canvas:
- Plastic per part: base fill; radial gradient at the highlight, radius R: 0 white .55, 0.28 white .06, 0.62 transparent, 1 rgba(10,0,30,.42) (rim = volume); additive bounce stroke rgba(70,150,150,.28), width 0.18R, 0.04R left (wall colour; canvas 'lighter', CSS `plus-lighter`); a hard white ellipse 0.16R x 0.09R at .85 - the 90s-Phong mark.
- Limbs: gradient across (dark .25 -> white .5 band at 22% -> dark .45) plus a white line along 20-75%. Ball joints at shoulders and knees. Smooth polylines first. Markings under the plastic: blur(2px).
- Floor: dy = y - 480, X = (x - 960)/dy, Z = 1/dy, tiles TX 0.27, TZ 0.00029, 2x2 supersampled, 35% fog within 140px of the wall. Bake once, or a CSS checker plane with `perspective` + `rotateX`.
- Reflections: objects mirrored about each one's own ground line, opacity .34, clipped to the floor; opacity on the whole group, since per-part alpha stacks overlaps to opaque.
- Window: mountains under a 28x26 pink wireframe grid, jagged snow caps. Glass table: translucent green ellipse, white outline, a glint sliding 260 px/s.

## Make it move
- 140 spheres on a ring spinning about the vertical at 7 rad/s, tilt 0.35, depth-sorted; dark purple tube stroke first, then each highlight.
- Chrome sphere (104px): per-pixel env map - reflection down -> checker, up -> sky plus a window streak; checker u offset 4.5t so it spins; brighter Fresnel rim. Precompute reflection vectors once.
- Additive flare: 170px glow pulsing +-8% at 23 rad/s, 12 rays turning 1.6 rad/s, a 960px streak, 5 ghosts on the sun-to-centre line sliding sin(5t)*0.03.
- Glints (eyes, LEDs): additive glow r 46 pulsing +-25% at 18 rad/s.
Rates suit a 0.23 s shot; halve or quarter them for longer shots.

## Signature transition
Wireframe -> render: a #02060a frame fades in over the old shot (first 12%) with a rgba(60,255,150,.8) grid floor (horizon at 59% height, 49 radiating lines, 12 rows spaced by k^2) and the new shot's edges in #3cff96 with an 8px glow; from 30% a scanline sweeps down revealing the rendered shot, led by a 6px rgba(200,255,230,.9) bar. Upstream 0.14 s; 12-20 frames in an ad. Custom presentation (see 16_2026.md): entering `clipPath: inset(0 0 X% 0)`; edges by Sobel on your canvas (half res, gradient > 38) or SVG feConvolveMatrix + feColorMatrix on a copy of the entering scene.

## Pitfalls
- Edges come from the new shot's first frame; it must be complete, not blank or fading in.
- Bake full-frame per-pixel work; only the small sphere is per-pixel per frame.
- Weakness: give organic forms tapered, bent cylinders and sculpted face planes.
