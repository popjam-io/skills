# Silver-age comic (Jack Kirby era, four-colour print, 1966)

> Adapted from huashu-art-motion (MIT, (c) 2026 alchaincyf) - references/风格配方/27_kirby.md

Layer: era specimen (best for homage, journeys, era-hopping) - Upstream quality: ★★ - Known weakness: reads like clean Lichtenstein pop; missing Kirby's blocky hands, extreme foreshortening and muscular tension.

Evoke the technique; never copy a specific work or character (no existing heroes, logos or panels).

## Look
Cheap four-colour offset print: cream paper #f4ecd6, flat fills with Ben-Day dots, a colour plate slightly off the black plate, 6 px ink outlines, heavy "spotted blacks" with feathered hatching on the shadow side, "krackle" (black dot clusters meaning cosmic energy), blocky extruded sound-effect lettering on starbursts, panels and caption boxes.
- Palette: ink #141212, cyan #2a9fd8, blue #1f3f9e, magenta #e0287a, red #e3262d, yellow #ffd62a, orange #f6921e / #d2541c, skin #fbd9b8, pale wall #cfe7f2, deep blue #2b3f9c, space #121a52, energy #ffe14a / #ff8a2a, purple #b04ac8.

## Build it in Remotion
Same geometry rendered twice, in SVG (px at 1920 wide; scale with the canvas):
1. Colour plate: paper, flat fills, dot `<pattern>`s - light grounds cyan dots pitch 9 r 2.7 at 15 deg; dark grounds purple pitch 9 r 3.2 at 75 deg; skin red pitch 7 r 1.5 at 75 deg. Shift the whole plate (4, 3) px = misregistration; never the ink.
2. Ink plate on white with `mixBlendMode: 'multiply'`. Per part, back to front: white fill -> shadow -> 6 px black stroke; later white fills hide earlier lines, so only visible lines remain.
3. Spotted blacks + feathering, with L = (-0.86, -0.5) pointing at the light: crescent = shape minus a copy shifted by L * d1; hatch band = shape minus a copy shifted by L * d2, filled with lines parallel to L (spacing 9, width 2.6). d1/d2: big garments 16/34, torso 14/30, sleeves 10/22, hair 12/26, animal body 16/34, tabletops 10/18.

```tsx
import React from 'react';
const L = {x: -0.86, y: -0.5}; // unit vector toward the light
export const KirbyShade: React.FC<{id: string; d: string; d1: number; d2: number}> = ({id, d, d1, d2}) => (
  <>
    <defs>
      <pattern id={`${id}-h`} width={9} height={9} patternUnits="userSpaceOnUse"
        patternTransform={`rotate(${(Math.atan2(L.y, L.x) * 180) / Math.PI})`}>
        <rect width={9} height={2.6} fill="#141212" />
      </pattern>
      {[d1, d2].map((s) => (
        <mask id={`${id}-${s}`} key={s}>
          <path d={d} fill="white" />
          <path d={d} fill="black" transform={`translate(${L.x * s} ${L.y * s})`} />
        </mask>
      ))}
    </defs>
    <path d={d} fill={`url(#${id}-h)`} mask={`url(#${id}-${d2})`} />
    <path d={d} fill="#141212" mask={`url(#${id}-${d1})`} />
  </>
);
```
Static parts render once; only krackle, speed lines and lettering change - cheap.

## Make it move
Comic elements step at 12 fps: `Math.floor(frame * 12 / 30)`.
- Krackle: 16-26 black circles per cluster at distance R * rnd^0.7, radius R * (0.05 + 0.2 * (1 - dist/R)) * rnd (bigger near the centre), pulsing with sin(18t + i), reseeded every step. Six clusters ride an S-shaped energy stream at (k/6 + 0.42t) mod 1 (orange band, yellow core, zigzag ink edges). Small rising clusters = steam or sparkle.
- Speed lines: v = |sin(min(1, t/0.9) * pi)|; 9 black lines trailing the mover, length 70-180 * v, jittered each step, plus two motion arcs.
- Sound-effect word: pops at 0.52 s with `Easing.out(Easing.back(1.7))`; Bangers (`@remotion/google-fonts/Bangers`) ~108 px; 7 black copies offset (0.8d, d) for the blocky extrusion; top 46 px of the red face clipped to yellow; 26-point yellow starburst behind; +-3 px jitter. Build extrusion and two-tone face as separate layers.
- Inset panel: close-up of the product or a reaction on magenta with yellow dots, 44 focus wedges re-dealt each step, krackle around the hero; yellow caption boxes (black frame, offset black shadow) carry the copy.

## Signature transition
Comic panels slam in, 0.42 s (13 frames): magenta dots creep over the old shot while the new shot lands panel by panel, each scaling 1.18 -> 1 with outBack behind thick black gutters. Recipe: ../transitions.md (comicPanels).

## Pitfalls
- A full-size sound-effect word covered faces; keep big lettering in empty space at ~0.82 scale, never over product or logo.
- A big black ellipse on an animal's dark side read as markings; spotted blacks are narrow crescents hugging the edge.
- Rings around a body: draw the back half first and the front half last.
- Beyond clean pop (the weakness): squared, blocky fingers; extreme foreshortening (hands or product toward camera at 1.5-2x); diagonal poses; crescents on muscle groups; krackle wherever energy appears.
