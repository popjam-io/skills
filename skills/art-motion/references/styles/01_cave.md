# Cave Painting (Upper Paleolithic, c. 40,000 BC)

> Adapted from huashu-art-motion (MIT, (c) 2026 alchaincyf) - references/风格配方/01_cave.md

Layer: era specimen (best for homage, journeys, era-hopping) - Upstream quality: ★★★ - Known weakness: human figures are too smooth and cartoonish to read as truly primitive.

## Look
- Pigment sits *in* a lumpy ochre rock wall lit softly from the upper left; every color is dirtied by the rock's shadows and grain.
- Marks: a solid charcoal line with a sprayed, dotted fuzzy edge, then an opaque flat fill. Animals in strict profile: legs are charcoal lines only, bodies are filled silhouettes with a darker ~22 px band along the back for modelling. Negative hand stencils (pigment sprayed around a hand). People are red-ochre silhouettes with a profile head and one almond eye (white, black pupil, one lash); that single eye carries the "person" read.
- Light: flickering firelight, warm center, heavy vignette, drifting embers.
- Palette: wall `#ce925a` / `#6e4426` / red patches `#b6643a`; charcoal `#21150d`; red ochre `#9c3520` (dark `#74261a`); yellow ochre `#c9772f`, `#cf8f2c` (strands `#6e3c0e`); hide `#b06a2c`, spots `#4e2610`; chalk white `#f0dfbf`; bison `#8c3d22` (head `#76301a`); horse `#cf8236`; hand stencil `#8e2a1a`, spray `#f6e2bc`; ember `#ffe082`. Titles in a hand script (e.g. Kalam 700 via @remotion/google-fonts) in `#9b2a18`, painted into the pigment layer so they take the rock texture.

## Build it in Remotion
px at 1920 wide; scale with the canvas. One `<canvas>`, baked layers plus a light per-frame pass.
1. **Rock relief (bake once in `useMemo`)**. Height field at half resolution (960x540, coordinates in full-res px): `h = fbm(x*0.0022, 4 oct) + 0.16*fbm(x*0.011, 3 oct) + 0.03*noise(x*0.05)` with `noise2D` from @remotion/noise. Normals by finite difference x52, light L = (-0.55, -0.62, 0.56), `shade = clamp(0.5 + (dot(N,L) - 0.56)*0.9)`. Blend the three wall colors with two low-frequency fbm fields, multiply by `0.72 + 0.55*shade`, write ImageData, upscale with smoothing. Add two grain layers (dark: density 0.22, alpha 0.32; light: 0.10, 0.28), ~10 random-walk cracks (turn +-0.45 rad per step, steps 14-40 px, 12% branch chance; a dark line over a light line offset +1.6 px reads as incised), a radial vignette (r 260 -> 1180, edge alpha 0.8) and a static warm center glow ('lighter', alpha 0.36). A few hundred ms once; never per frame.
2. **Pigment layer (offscreen; redraw only what moves)**. Every shape gets three passes: stroke with a *fuzz* pattern (sparse charcoal dots, width 2*lw + 7), stroke with an *ink* pattern (charcoal with 7% random holes plus larger holes where noise > 0.58, width 2*lw), then a flat fill covering the inner half. Painter's order handles overlaps. Then `source-atop` one baked "rock in pigment" texture over the whole layer: rock shadow -> black at alpha `(0.5 - v)*0.6`, highlights -> warm white at `(v - 0.5)*0.2`, grain, low-frequency damp patches up to ~0.27. One full-screen composite per frame.
3. **Charcoal boil without moving geometry**: two seeded 256 px tiles via `createPattern`; every 1/9 s shift them.
   ```tsx
   import { random } from "remotion";

   // fuzz = g.createPattern(fuzzTile, "repeat"); call before stroking with it each frame.
   export const boilPattern = (fuzz: CanvasPattern, frame: number, fps: number) => {
     const step = Math.floor((frame * 9) / fps);
     fuzz.setTransform(new DOMMatrix().translate(random(`fx-${step}`) * 256, random(`fy-${step}`) * 256));
   };
   ```
4. **Hand stencils (bake)**: on a 320 px canvas spray Gaussian dots (sigma 46*s, 3200 dots, alpha 0.15-0.6; plus sigma 28*s, 1400 dots), `destination-out` a solid hand mask, fill the mask at alpha 0.3 with `#f6e2bc`.
5. **Firelight (per frame)**: radial gradient whose center wanders +-60/+-36 px on `noise2D`, intensity `0.14 + 0.11*noise(9.5t) + 0.04*sin(23t) + 0.03*sin(37t)`, composited `'overlay'` at alpha intensity*2.6, plus an outer vignette breathing in counter-phase.
6. **Embers**: ~49 particles (two side clusters of 20, 9 central) rising from the bottom to ~11% from the top over a 5.5 s life; core r 2.6-5.4, halo 3.6x at alpha 0.32, flicker `0.3 + 0.7*|sin(6t + 1.9i)|`, fade `sin(q*pi)`, 'lighter'. Start phase from `random`, position a pure function of frame.
Per frame: one figure redraw, one composite, gradients, particles: well under 30 ms.

## Make it move
- **Main - galloping animals**: two leg poses (extended / gathered) swapped every 3.5 frames (`Math.floor(frame * 2 / 7) % 2`, ~8.6 Hz), head +-0.12 rad about the neck, body bob 9 px vertical and +-3 px horizontal; pair animals in anti-phase. Give any subject the same two-pose stepping instead of smooth tweening.
- **Loop 1 - fire, embers, glowing hands**: each stencil gets a warm radial (r 105, 'lighter') at alpha `0.2*clamp(0.5 + 0.9*noise(7t + 3.7k))` on its own phase.
- **Loop 2 - small character beats**: a head lift on a `sin(pi*q)` envelope (-0.16 rad), ear twitch +-0.06 rad; steam or smoke as three charcoal lines `x0 + sin(13q - 11t + 1.3j)*6`, 58 px tall.
- Motion comes from local actions. Fire pushed beyond +-0.16 intensity / +-90 px reads as camera shake.

## Signature transition
Upstream uses this style as the opener, so it has no entry transition. A natural opener: start black and ramp firelight intensity and pigment-layer alpha over ~0.5 s (15 frames) as if a torch is lit, embers first. Leaving the cave is defined by the next style's card.

## Pitfalls
- Relief mid-frequency too strong (0.35, normals x60) turns the wall into camouflage or dunes, and figures look like they wear camo. Keep 0.16 and x52.
- Never `multiply` pigment onto the wall: chalk white disappears. Opaque fills, dirtied by the `source-atop` texture.
- Fire in `'lighter'` washes blond hair and hide to pink-white; `'overlay'` keeps ochre saturation.
- Hand mask: fill palm and fingers separately. One combined Path2D filled once lets nonzero winding cancel where opposite-wound subpaths overlap, leaving gaps.
- Hair on a tilting head: make lower strands follow the head rotation less and less, or the whole mass swings.
- Weakness (figures too smooth): downsample each outline to 12-16 points and add larger hand-drawn jitter; keep limbs stick-like.
- The relief is static and fire only changes brightness. For rock that seems to shift under the flame, bake two shade maps with different light directions and crossfade them by the fire noise (one extra full-screen draw).
