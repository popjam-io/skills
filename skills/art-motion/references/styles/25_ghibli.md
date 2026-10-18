# Ghibli-style painted backgrounds (watercolour washes + two-tone cel, Studio Ghibli family)

> Adapted from huashu-art-motion (MIT, (c) 2026 alchaincyf) - references/风格配方/25_ghibli.md

Layer: material (works on any subject) - Upstream quality: ★★ - Known weakness: characters weaker than the background (flat vector next to painted rooms).

Evoke the technique; never copy a specific work or character.

## Look
Bright, airy spaces in transparent watercolour glazes with pigment-pooled edges and soft colour blooms; opaque white for frames, cloth and clouds; characters in two-tone cel (base plus a crescent of shade on the far side) with warm brown lines; everything nudged by wind. Wall #fbf3e0 near the light -> #dcc49a in corners; blooms warm yellow, pink, blue-grey, pale green; line #4a3428 softened to #6a4a38.

## Build it in Remotion
The watercolour background is static: build it once (useMemo) as a memoized SVG group or a cached canvas and animate only small layers above. Upstream's first frame was very slow to build it - keep layer counts modest; half resolution suits soft washes. px at 1920 wide; scale with the canvas.
- deform (midpoint displacement), deterministic:

```tsx
import {random} from 'remotion';
type Pt = [number, number];
export const deform = (pts: Pt[], rounds: number, amp: number, seed: string): Pt[] => {
  let out = pts;
  for (let r = 0; r < rounds; r++, amp *= 0.6) {
    const next: Pt[] = [];
    out.forEach((a, i) => {
      const b = out[(i + 1) % out.length];
      const len = Math.hypot(b[0] - a[0], b[1] - a[1]) || 1;
      const g = random(`${seed}-${r}-${i}-0`) + random(`${seed}-${r}-${i}-1`) + random(`${seed}-${r}-${i}-2`) - 1.5;
      const k = g * amp * Math.min(1, len / 80); // push the midpoint along the edge normal
      next.push(a, [(a[0] + b[0]) / 2 - ((b[1] - a[1]) / len) * k, (a[1] + b[1]) / 2 + ((b[0] - a[0]) / len) * k]);
    });
    out = next;
  }
  return out;
};
```

- wash(shape, colour, {layers, alpha, amp, edge}): base = deform 3 rounds; each layer deforms 2 more and is filled with multiply at low alpha (a transparent glaze) plus a 1.6px same-colour stroke at alpha `edge`; strokes pile up across layers into the pooled water-mark edge. In SVG: one `<path>` per layer with fillOpacity, strokeOpacity and `mixBlendMode: 'multiply'`.
- Settings: big wall layers 5, alpha .4, amp 12; colour blooms layers 3, alpha .045, amp 40; planks layers 3, alpha .5, amp 3, edge .14; opaque whites (frames, cloth, clouds) normal blend at .9-.95.
- Wall: radial gradient wash + 28 heavily deformed blooms in alternating hues + dark blooms in two corners; wainscot and floor washed board by board with varied hue; paper grain multiplied at .3 over all.
- Clouds: 16 opaque white puffs with wash edges and a blue-grey gradient on their underside (clipped / source-atop), cached as sprites. Trees as sprites rocking +-0.025 rad about the root.
- Cel: fill the shape in the shade colour, then inside the shape's clip fill the same shape shifted toward the light by (-dx, -dy) in the base colour - only a far-side crescent of shade remains. 2.4px warm line.
- Painted characters: clip a texture group (paper grain alpha .8 + 40 blooms alpha .1, amp 16) to the character silhouette and multiply it over the cel character.

## Make it move
- Curtains billowing (main action): two gauze panels, hem offset q^2*(60 + 150*gust), gust = 0.55 + 0.45*sin(5.4t + phase), plus a sin(7t + 6q) ripple; 3 translucent wash layers with fixed seeds so edges don't boil.
- Wind over grass: 360 blades, wind = 0.5 + 0.5*sin(3.1t - 0.018x); the phase travels along x, so each gust visibly sweeps the slope.
- Dappled light: 34 warm radial spots on the wall (`mix-blend-mode: screen`), drifting with noise2D, brightness sin(5t + 1.7i).
- Clouds 22-30 px/s; canopy sway; flowers nodding; hair streaming in the wind (7 smoothed points); ribbons and cloth hems fluttering.

## Signature transition
Bleed on wet paper: five blooms open in sequence (starts 0, .14, .24, .30, .34; radius 1400px x 1, .75, .6, .6, .55; each grows over 66% of the transition) with noisy edges R*(1 + 0.28*noise + 0.05*sin(9a + i)); inside them the new shot. While young, each carries a dark pigment rim (multiply rgba(150,110,70,.6*(1 - q/0.55)^2), 5px, blur 1.2) and a pale washed halo outside (rgba(255,250,236,.6*(1 - q)), 70px, blur 18), both fading as it grows. 0.38 s (11 frames). Custom presentation (see 16_2026.md): `clipPath: path(...)` of the blob union (90 noise2D samples each), rims in an overlay SVG.

## Pitfalls
- Blooms at .07 x 4 layers with grain at .5 looked like mouldy parchment; these rooms are bright - .045 x 3 and a lighter gradient.
- Two rectangular washes left a hard seam; darker zones must be large deformed polygons (amp 60), never rectangles.
- Curtains at 3.2 Hz with 90 + 70 billow didn't read as moving; 5.4 Hz and 60 + 150 did.
- Old bloom rims crossing the new image: fade rims as blooms grow.
- Weakness: characters still flat - add painted hair-highlight blocks; run curtain shadows through the floor's light patches.
- No nods to specific films or characters (not even a signature bow or a prop easter egg).

## Unvalidated: overall visual language
Upstream later began researching the wider studio language - readable character silhouettes and acting; characters and environment agreeing in perspective, light direction, contact shadows and colour; everyday actions with weight and the right order of using things; environmental motion with a physical cause (wind, gravity, contact); lived-in, functional spaces - plus a separate street-workshop study. None of it is validated across scenes; treat it as hypotheses. Forests, girls, cats and slow pacing are not required, the washes are an optional material, and multiplying paper grain over a flat character does not finish it.
