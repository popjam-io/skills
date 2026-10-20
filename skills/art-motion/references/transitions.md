# Art-style transitions

> Adapted from huashu-art-motion (MIT, (c) 2026 alchaincyf) - references/风格配方/_转场_迁移测试.md

A style transition is the new style's own physical process, not a generic wipe: melting is liquid, Hopper is light, watercolour is water, VHS is tape. Design one in four steps:
1. Ask how this style's picture would physically appear, light up or sweep in.
2. Contaminate the old shot with that process first.
3. Reveal the new shot from the shape of the process.
4. On the beat, add a brief highlight or overshoot.

Durations are upstream's, from a fast style-hopping montage (seconds / frames at 30 fps). In ads treat them as the snappy end: 10-18 frames is typical, up to ~24 for a hero reveal; land the reveal on a music beat. Sizes are px at 1920 wide; scale with the canvas. Signature transitions of styles not listed here are in [styles/INDEX.md](styles/INDEX.md) and their cards.

## In Remotion

- `TransitionSeries.Transition` with `linearTiming({durationInFrames, easing})` and a custom presentation. Its component gets `children`, `presentationDirection` ('exiting' | 'entering'), `presentationProgress` (p, 0..1, same value on both sides) and `passedProps`. The entering scene renders on top; the overlap shortens the series by the transition length.
- Decorations under the new shot (a reveal shape's outline) go in the exiting branch; decorations over everything (light bands, ribbons, brush heads, paper sheets, film dust) go once in the entering branch.
- Tools, cheapest first:
  - CSS per side: `clipPath` (`circle()`, `polygon()`, `path()`), `maskImage` gradients for soft edges (radial, linear, conic; several layers union), `filter` (sepia, grayscale, contrast, blur), overlay divs with `mixBlendMode` (multiply darkens, color drains hue, screen / plus-lighter adds light).
  - SVG `<clipPath>` with many children (dots, tiles, bands, blobs) via `clipPath: 'url(#id)'`. Children union, so nothing cancels into holes (upstream lost shapes clipping with one compound path; use separate children or a white-filled mask). SVG filters: `feTurbulence` -> `feDisplacementMap` for tears, ripples, warps and sags; `feColorMatrix` for channel splits and colour drains.
  - Pixel sampling (a dot taking the colour beneath it, flakes of the old picture): a presentation cannot read the other scene's pixels. Fake it with style-palette colours plus filters on the real scene, or, when both shots are your own canvas renderers, make the transition one component that draws both into offscreen canvases and composites (getImageData ~10 ms per scene at 1080p; acceptable).
- Determinism: `random`, `noise2D`, `useCurrentFrame` only. Cache geometry (tile tables, seeded points), never anything derived from scene content - upstream replayed the first use's pixels when a transition ran twice, and frames render out of order. SVG def ids must be stable plain strings (`bleed-2`); `useId()` output contains colons that break `url(#...)`.
- Cover the frame by p ~0.85-0.9. A final fade that fills leftover gaps reads as a flash frame.

Skeleton (irisFilm):

```tsx
import React from 'react';
import {AbsoluteFill, Easing, random, useCurrentFrame} from 'remotion';
import type {TransitionPresentation, TransitionPresentationComponentProps} from '@remotion/transitions';

type Iris = {cx: number; cy: number; r0: number}; // r0 = distance to the farthest corner
const back = Easing.out(Easing.back(1.7));

const IrisFilm: React.FC<TransitionPresentationComponentProps<Iris>> = ({
  children, presentationDirection, presentationProgress: p, passedProps: {cx, cy, r0},
}) => {
  const step = Math.floor((useCurrentFrame() * 12) / 30); // 12 fps hand wobble
  const entering = presentationDirection === 'entering';
  const q = entering ? Math.max(0, 2 * p - 1) : Math.min(1, 2 * p);
  const r = entering ? r0 * back(q) : r0 * (1 - Easing.in(Easing.quad)(q));
  const pts = Array.from({length: 48}, (_, i) => {
    const a = (i / 48) * 2 * Math.PI;
    const rr = r * (1 + 0.015 * (2 * random(`iris-${step}-${i}`) - 1));
    return `${cx + Math.cos(a) * rr}px ${cy + Math.sin(a) * rr}px`;
  });
  const clipPath = `polygon(${pts.join(',')})`;
  if (entering) return <AbsoluteFill style={{clipPath, opacity: p < 0.5 ? 0 : 1}}>{children}</AbsoluteFill>;
  return (
    <AbsoluteFill style={{background: '#000'}}>
      <AbsoluteFill style={{clipPath, filter: `sepia(${q}) grayscale(${0.7 * q}) contrast(${1 + 0.3 * q})`}}>{children}</AbsoluteFill>
    </AbsoluteFill>
  );
};
export const irisFilm = (props: Iris): TransitionPresentation<Iris> => ({component: IrisFilm, props});
```

## Catalogue

### Light
- **sunShaft** -> hopper, 0.34 s (10 f). Old shot sinks into cool shadow (multiply rgba(70,120,110, 0.7 * min(1, 2p))); a slanted light patch (260 px slant) sweeps its right edge across the frame with the new shot inside, a warm screen layer (0.45 -> 0 over p .6-1), a moving window-bar shadow and a bright leading edge. Remotion: parallelogram `polygon()` clip. Use: daylight, quiet lifestyle.
- **flareSweep** -> shinkai, 0.38 s (11 f). Slanted boundary (slope 0.35) sweeps -500 -> W + 700 (inOut), new shot on the left; three additive bands ride it (520 px warm alpha .55, 160 px white .85, 60 px cyan .6), plus a horizontal streak, 40 light particles, 3 hexagon ghosts. Remotion: polygon clip; bands as rotated gradient divs with `plus-lighter`. Use: uplifting reveals, summer, launches.
- **lampGlow** -> shadow-puppet, 0.4 s (12 f). Old shot dims like a lamp going out (multiply rgba(70,34,12, min(1, 2.2p))); new shot appears in a radial reveal, solid to 0.55R then soft, R = 1500 * inOut over p .12-1 with +-7% flame jitter; warm additive glow sin(pi * p) and a small flame. Remotion: `maskImage: radial-gradient(...)`. Use: festive, evening, heritage.
- **chiaroscuro** -> rembrandt, 0.45 s (14 f). Over p 0-.45 a multiply vignette closes (inner radius 1100 -> 80, outer 1400 -> 700) plus flat rgba(40,26,14) multiply up to .85. Over p .25-.9 (inOut) the new shot appears in a 40 px-soft light wedge from the window point (spread 60 -> 1400) plus a disc growing 40 -> 1500; a blurred warm wedge glow peaks at alpha .35; full fade-in after p .8. Remotion: `maskImage` union of a `conic-gradient` wedge and a `radial-gradient` disc. Use: premium unveil from darkness.

### Liquid and water
- **melt** -> dali, 0.36 s (11 f). Old shot sags in 4 px columns (sag 0.22 * edge * e, stretch 0.3); the new shot fills down to a liquid edge = falling line (-160 -> H + 40, easeInOut) + 26 round-headed drips (width 10-32, length 60-280, profile (1 - u^2)^0.3, own phases) + a sine wave; dark rim (blur 3) and highlight on the surface. Remotion: entering `path()` clip sampled every ~8 px; exiting `feTurbulence` ("0.02 0") -> `feDisplacementMap` on y, scale growing with e. Use: surreal claims, "melts in your mouth".
- **bleed** -> ghibli, 0.38 s (11 f). 5 blooms open in sequence: radius q * 1400 * k, q = easeInOut over (t0, t0 + .66); edge R * (1 + 0.28 * fbm(angle) + 0.05 * sin 9a); a 70 px bright halo blurred 18 leads (water arrives first), new shot inside, a 5 px brown multiply water-mark on the edge; halo and mark fade by (1 - q). Remotion: `<clipPath>` of 5 noise-edged polygons (~96 points, noise2D over angle); halo and mark as blurred strokes of the same paths. Use: soft, natural, handmade, kids.
- **ripple** -> monet, 0.34 s (10 f). Old shot falls into water: 6 px rows shift dx = sin(.045y - 26p) * 46 * sin(pi * min(1, 1.2p)) * (.4 + |y - cy| / H). New shot opens through ~3600 horizontal dab ellipses (40-110 x 9-17) appearing by elliptical distance from the focal point (y weighted 1.9, denominator 1700); 3 pale dashed ring fronts with dashOffset on p; 140 glint lines mid-way; fade-in from p .7 so corners clear by ~.85. Remotion: `<clipPath>` of ellipses (fewer, larger on verticals); exiting `feTurbulence` ("0.002 0.045") -> `feDisplacementMap`. Use: drinks, skincare, calm.

### Paint and paper
- **blueBrush** -> picasso-blue, 0.42 s (13 f). Old shot drains to blue (`mixBlendMode: 'color'` rgba(45,90,148, min(1, 2.2p)) + darkening multiply); 6 broad bands (H/6 + 90 tall, alternate tilt +-18 px) brush left to right, staggered by .07; each head a quadratic curve with 6-7 px sine-wobbled edges, 26 dark/light bristle streaks 80-280 px behind it. Remotion: `<clipPath>` of band polygons; streak overlay. Use: mood shifts.
- **cutouts** -> matisse, 0.36 s (11 f). A 1100 px cobalt sheet with sine-irregular scissor edges sweeps right to left, shadow (14, 10) blur 12, carrying 260 gouache marks, pinned white/yellow fronds (stem + 7 fingers), yellow/pink six-point stars turning with p and red discs, each shadowed; new shot behind its trailing edge. Remotion: overlay `<g>` translated by x(p); polygon clip from the trailing edge. Use: fashion, design, playful launches.
- **goldLeaf** -> klimt, 0.5 s (15 f). 72 px squares in spiral order from a focal point: key = distance * .78 + angle * .12 + random * .08 (normalized), q = (1.32p - key) / .32. Below q .5 a leaf drops from 1.3x with a twist, gold highlight sliding with q, embossed spiral / eye / ring marks; q .5-1 the leaf fades over the new shot. Remotion: `<clipPath>` of tiles with q >= .5 under a leaf overlay that hides the hard edges. Use: jewellery, luxury, gifting.
- **apsara** -> dunhuang, 0.5 s (15 f). Front x = lerp(W + 260, -300, e) + 110 * sin(y * .006 + 5p) sweeps right to left, new shot to its right; 3 ribbons ride it (mineral green, earth red, azurite; widths 44/38/32; travelling wave; white dashed floral line); behind the front, flakes of the old picture flip and fall in parabolas. Remotion: polygon clip; SVG ribbons; flakes in the old palette (cheap) or a few clipped copies of the old scene (costly). Use: East Asian heritage, "old to new".

### Print, dots, panels
- **pointill** -> seurat, 0.34 s (10 f). Pitch 14; dots grow to r 6.4 in the first 30% as the old shot fades to paper; each dot switches colour at .5 * (.6x/W + .4y/H) + .25 * hash + .15 (top-left first) with a 1.35x pop; after p .6 the new shot develops beneath, after .7 dots shrink away. True colours need the canvas route; otherwise use the Seurat palette. Use: craft, "every detail".
- **dotBloom** -> kusama, 0.48 s (14 f). 58 px hex grid; dots grow by distance from the focal point (outBack, up to .74 x spacing, which tiles the frame), each holding the new shot, with a fading white outline. Remotion: `<clipPath>` of circles. Use: pop, fashion.
- **comicPanels** -> silver-age-comic, 0.42 s (13 f). Magenta dots (pitch 12, r 3.4, 75 deg) creep over the old shot at alpha min(1, 2.5p) * .85; the new shot lands in 5 panels (two over three; re-cut for verticals) starting at 0 / .12 / .24 / .34 / .44 of p, each over .32: scale 1.18 - .18 * outBack(q) inside its rect; 14 px black gutters fade after .8. Remotion: one clipped, scaled copy of the entering scene per panel (fine for SVG scenes; for heavy ones clip one copy to the landed panels). Use: feature call-outs, steps, retro hype.

### Distortion and media
- **screamWarp** -> munch, 0.5 s (15 f). Old shot warps row by row (amplitude 70e); a wavy front y = lerp(-180, H + 220, e) + 80 * sin(x * .0055 + 7p) pushes down, new shot above it settling (warp 60(1 - e)); four 26 px bands on the front #b82a1e #e2541c #f08a24 #f4c03a. Remotion: polygon clip, displacement filters, bands as offset strokes. Use: pain-point hooks.
- **vhs** -> vaporwave, 0.30 s (9 f). Bands of random height 6-54 px (re-dealt each frame) show the new shot with probability p, shifted +-130 * sin(pi * p); p .38-.62 sync loss rolls the frame up with a 40 px black bar; magenta/cyan ghosts at +-14 px; 160 snow lines. Remotion: `<clipPath>` of band rects; `feTurbulence` ("0 0.08", seed from frame) -> `feDisplacementMap`; RGB-split filter at 14 px. Use: retro, gaming, glitch drops.
- **irisFilm** -> rubber-hose, 0.4 s (12 f). Old shot goes sepia / grey / contrasty as a black iris closes on a focal point (R0 * (1 - easeIn(q))); the new shot opens from it with outBack; 48-point circle wobbling +-1.5% at 12 fps; add the film flicker, scratches and dust from rubber-hose. See the skeleton. Use: nostalgia, comedic endings.

### Figure
- **radiant** -> haring, 0.32 s (10 f). A V-armed dancing figure grows from the focal point, s = 0.15 * 320^easeInOut(p); 30 px black outline, limbs holding the new shot; 16 action lines jump at 8 fps; fade only after p .82. Earlier curves failed: 0.08 * 40^p stayed under 300 px for 80% of the time then hard-cut; 0.15 * 120^p left gaps that needed a one-frame fade (a flash). Remotion: `<clipPath>` of the figure's capsules and head scaled by s, outline in the exiting branch. Use: music, dance, youth brands.
