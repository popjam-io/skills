# Post-Impressionism (Van Gogh, 1889)

> Adapted from huashu-art-motion (MIT, (c) 2026 alchaincyf) - references/风格配方/09_postimp.md

Layer: material (works on any subject) - Upstream quality: ★★★ (the benchmark other styles copy) - Known weakness: the heaviest renderer, ~120 ms/frame upstream.

## Look
Thick directional strokes that follow a flow field: walls rise vertically like flames, floors run along perspective lines to a vanishing point, skies swirl around vortices, lights sit in concentric halo rings. Every stroke has a dark blue rim, objects have hand-drawn dark blue outlines, and each region mixes a dozen hues. Palettes (mix with the sampled underpainting by the factor given):
- wall `#7f9be6 #5f7fd8 #a7bbf2 #6c6fd2 #8ad0e6 #c3cbf6 #4f6cc8 #9a8fe0` (0.3)
- night sky `#22339a #2f4fb8 #5c86dc #8fb6ee #1b2a78 #3c6bd0` (0.45)
- floor `#c0573c #a8453a #d7774a #8e3b30 #5f8f6a #c96a52 #e08a5c` (0.3)
- wood `#f2c13a #e0a020 #f8d860 #d08a18 #b8c040` (0.15); red `#e04a32 #c63a2a #f06b45 #b83224` (0.4); green `#2f9a5c #4fc27a #1f7a48 #8be09a` (0.35); halo `#fff2a0 #f6d84a #ffe680 #f0c040` (0.3); line `#1c2458`; star `#f6d84a`.

## Build it in Remotion
px at 1920 wide; scale with the canvas. Pipeline: flat underpainting -> flow-field stroke repaint with region palettes -> props layer -> outlines -> characters -> animated highlights.
1. **Three stroke passes**, never one: walls cell 14, len 64, width 8; floor cell 12, len 46, width 8; everything else cell 10, len 22, width 6.5. Each stroke = a rim pass (width + 2.5, color mixed 38-45% toward `rgb(20,25,60)`, alpha 0.8-0.9) then the color pass. Round caps; butt caps for strokes >= 30 px wide (round ones pack into rows of cobblestones).
2. **Direction field**: wall `-pi/2 + 0.26*noise2D(x*0.008 + t*0.5, y*0.008 - t*0.8)`; floor `atan2(y - vpY, x - vpX)`; sky = tangent of the nearest vortex `+ 0.3t`; around lamps, circular.
3. **Props layer**: small objects get their own pass (cell 7, len 14, width 4.5) clipped to their pixels (`source-atop`), or big strokes shatter them.
4. **Outlines**: dark blue 4.5 px, hand-jittered (+-2.2 px every 14 px), boiling at 8 fps (`Math.floor(frame * 8 / 30)`).
5. **Characters**: flat fill, then fine strokes `source-atop` (cell 8, len 16, width 5, no rim), then visible outlines and features. A secondary character can carry spiral strokes and 7 alternating orange rings rotating 0.6 rad/s.
6. **Cost**: stroke positions and colors are fixed (seeded per cell); only angles that depend on `t` change. Bake every region whose field ignores `t` once in `useMemo`; redraw per frame only the sky, halos and characters.
```tsx
import { noise2D } from "@remotion/noise";
import { random } from "remotion";

type Stroke = { x: number; y: number; a: number; l: number; c: string; rim: string };

const mix = (hex: string, to: [number, number, number], t: number) => {
  const n = parseInt(hex.slice(1), 16);
  const ch = [n >> 16, (n >> 8) & 255, n & 255].map((v, i) => Math.round(v + ((to[i] ?? 0) - v) * t));
  return `rgb(${ch.join(",")})`;
};

// Bake once inside useMemo (here: the wall pass, cell 14 / len 64). One stroke per jittered cell, seeded per cell.
export const bakeWall = (w: number, h: number, palette: string[], cell = 14, len = 64): Stroke[] => {
  const out: Stroke[] = [];
  let k = 0;
  for (let y = 0; y < h; y += cell) {
    for (let x = 0; x < w; x += cell, k++) {
      const sx = x + random(`jx-${k}`) * cell, sy = y + random(`jy-${k}`) * cell;
      const c = palette[Math.floor(random(`c-${k}`) * palette.length)] ?? "#7f9be6";
      const a = -Math.PI / 2 + 0.26 * noise2D("wall", sx * 0.008, sy * 0.008); // t-free, so it bakes
      out.push({ x: sx, y: sy, a, l: len * (0.7 + 0.6 * random(`l-${k}`)), c, rim: mix(c, [20, 25, 60], 0.4) });
    }
  }
  return out;
};

// Rim pass (width + 2.5) then colour pass, stroke by stroke. Round caps; butt caps from 30 px wide.
export const paintStrokes = (g: CanvasRenderingContext2D, strokes: Stroke[], width = 8) => {
  g.lineCap = width >= 30 ? "butt" : "round";
  for (const s of strokes) {
    const dx = (Math.cos(s.a) * s.l) / 2, dy = (Math.sin(s.a) * s.l) / 2;
    for (const [color, lw] of [[s.rim, width + 2.5], [s.c, width]] as const) {
      g.strokeStyle = color; g.lineWidth = lw;
      g.beginPath(); g.moveTo(s.x - dx, s.y - dy); g.lineTo(s.x + dx, s.y + dy); g.stroke();
    }
  }
};
```

## Make it move
- **Main - swirling sky**: 4 vortices of 3 spiral ribbons (width 14 / 11 / 8) rotating 0.9-1.5 rad/s in alternating directions; sky strokes follow their tangents plus 0.3 rad/s.
- **Loop 1 - halos and stars**: 3 dashed rings (dash 22/14, width 18, `rgba(255,236,140, 0.28*(1 - ph))`) expanding r 40 -> 150 about every 1.1 s, dash offset -60 px/s, `'lighter'`; stars twinkle `0.75 + 0.35*sin(5t + 1.7k)` with a 1.9x glow.
- **Loop 2 - flame walls**: the `t` term in the wall field sways strokes like flames. It forces a per-frame wall pass: step it at 8 fps and cache each step, or drop the term and bake. Flowers turn +-0.08 rad.

## Signature transition
Vortex swirl: per pixel at half resolution, rotate the sample angle about a center (a window, a lamp) by `twist*f^2`, `f = max(0, 1 - r/1100)`; the old shot twists away (`5e`), the new shot unwinds (`4.2(1 - e)`, extra rotation `-0.9(1 - e)`) inside a growing, wobbling radius (`2.4e`); crossfade the last 15%. `e = easeOut(p)`, upstream 0.28 s (~8 frames). Heavy (~0.5 M px per frame) but short; lighter: rotate and scale the entering shot inside a growing circular `clipPath`.

## Pitfalls
- One parameter set across the frame becomes carpet; split wall, floor and the rest.
- Color jitter alone gives "noise of one blue"; the look comes from region palettes.
- Re-seeding all strokes every 1/8 s reads as strobing; keep strokes fixed, boil only outlines and motif regions.
- Outlines drawn over a filled figure show hidden parts through it; draw only visible outlines, and redraw overlapping accessories (hats) after outlines.
- Weakness (cost): full-frame repaint is ~120 ms. Bake, step and limit per-frame strokes to motif regions as above; half-resolution passes upscaled are acceptable for the sky.
