# Painting in code: frame first, then paint it

> Adapted from huashu-art-motion (MIT, (c) 2026 alchaincyf) - references/03-一帧先行四条路线.md, references/04-纯代码绘制.md, references/10-角色.md, references/角色精细度.md, references/07-正面经验.md (painting practices)

Design one frame that already works as a still, then paint it in code, then make it move (motion: `living-paintings.md`). Split the work by what each source does best: code is strong at rules (stroke fields, geometry, camera, timing, physics, determinism) and weak at people and faces; the brand's real images are the truth about product, logo and people.

Pixel values are at 1920 wide (the upstream frames were 1920x1080); scale them with your canvas. 1080x1920 has the same pixel count as 1920x1080, so per-frame costs carry over.

## 1. Frame first

Before any motion, design one keyframe:

- Decide the subject, where it sits, where the eye lands, and where the camera will go.
- Consider three distinct compositions (say: product close and central / product small in a wide painted world / product as one object in a still life) and pick the strongest.
- Block it in as flat shapes and check it with `preview_frames` before painting. Then paint. Then animate.
- Put the frame's positions in one `LAYOUT` constant (hero, product, horizon, focal points, text block). Every layer and every scene reads from it; nothing re-lays itself out. A cut-out placed by its frame coordinates lines up in one pass.
- Matching a reference (a brand key visual)? Measure it rather than guess: read positions off a 20 px grid. Upstream, hand-guessed coordinates produced the wrong figure; measured ones read right in one round.
- Text that moves or changes (headline, price, counter, year) never goes into a painted layer. Keep it live on top. Paint only static decorative lettering into the scene.

Where each layer comes from (there is no frame-generation pipeline):

| Route | Painted by | Moved by | Choose when |
|---|---|---|---|
| A. Pure code | canvas / SVG renderers | code: curves, particles, boil | stylised worlds; many styles (swap the renderer, swap the style); exact control of every element and of beat timing |
| B. Real assets + code | the brand's photos, product shots, cut-outs (`remove_background`) | code: position, arcs, squash, physics, effects | photographic fidelity; anything with people |
| C. Mixed | painted backdrop in code; real product/people via `<Img>` | one code timeline | the default for a styled ad: texture from code, truth from real assets |

## 2. The layer stack

Default order for oil- and print-like styles:

1. **Block-in.** Large areas (sky, wall, floor, window view) as flat colours or gradients, at the right place and value. This layer decides the composition; no style yet.
2. **Style renderer.** Repaint the whole frame in the style's mark (flow-field strokes, dabs, tiles, halftone, pixels), sampling colour from the block-in. The renderer is what makes it read as that kind of painting.
3. **Small objects on their own layer.** Cups, vases, leaves, table legs pushed through the big-area renderer shatter into mush. Paint them separately with finer parameters, texturing only onto themselves (`source-atop` on their own layer).
4. **Hero.** The product or a real person: composited, given the style's material treatment (section 9), finished with a crisp edge. The eye lands here; it must read instantly.
5. **Moving highlights.** The style's motif loops (`living-paintings.md`). Continuous motion runs on continuous time; only hand-drawn line art boils at 8-12 fps.

Exceptions: **ink wash** runs backwards (the paper is the base, ink only adds, large areas stay empty; never fill first). **Pattern styles** (polka dot, geometric poster) are flat fills with a pattern scattered on top; the pattern is the renderer. **Chiaroscuro** paints the lit version first, then multiplies a light map over it.

Evidence: sunflowers and table legs were shredded by large strokes until they got their own layer; a "lit version / dark version, clipped by light shapes" build later generalised the same split.

## 3. Remotion toolkit

| Need | Use |
|---|---|
| hundreds to thousands of strokes or dabs, per-pixel work, pixel art | `<canvas>` repainted in a `useEffect` keyed on `frame` |
| clean shapes, drawn-on lines, patterns | SVG `<path>`, `<pattern>`; `evolvePath`, `getLength`, `getPointAtLength` from `@remotion/paths` |
| wobbly hand-made edges, paper, heat haze | SVG `feTurbulence` into `feDisplacementMap` (scale 2-6) |
| ink bleed, glow, soft light | `feGaussianBlur`, CSS `filter: blur()`, canvas `ctx.filter = "blur(4px)"` on a cached layer |
| grading, duotone, desaturation | `feColorMatrix`, CSS `filter` |
| paper, grain, light over everything | an overlay with `mixBlendMode: "multiply"` (paper, shadow), `"soft-light"` (grain), `"screen"` (light) |
| reveals, wipes, cut-paper edges | CSS `clipPath` (polygon/circle driven by frame), `maskImage` |
| flow fields, organic drift | `noise2D` / `noise3D` from `@remotion/noise`, time as the third axis |
| jitter, scatter, boil | `random(seed)` from `remotion`; the seed includes the index (and the step, for boil) |
| stepped, limited animation | `const f = Math.floor(frame / 3) * 3` |

Canvas layer skeleton: cached static layer, seeded strokes computed once, full repaint per frame.

```tsx
import React, { useEffect, useMemo, useRef } from "react";
import { random, useCurrentFrame } from "remotion";
import { noise3D } from "@remotion/noise";
const W = 960, H = 540; // half res; CSS scales it to the full frame
const SKY = ["#1b2a4a", "#24406e", "#3d6aa2", "#7fa6c9", "#e8d27a"];
export const PaintedSky: React.FC = () => {
  const frame = useCurrentFrame();
  const ref = useRef<HTMLCanvasElement>(null);
  const base = useMemo(() => { // static block-in: painted once per mount
    const c = new OffscreenCanvas(W, H), g = c.getContext("2d");
    if (g) { const gr = g.createLinearGradient(0, 0, 0, H); gr.addColorStop(0, "#1b2a4a"); gr.addColorStop(1, "#7fa6c9"); g.fillStyle = gr; g.fillRect(0, 0, W, H); }
    return c;
  }, []);
  const strokes = useMemo(() => Array.from({ length: 1200 }, (_, i) => ({ // seeded, fixed forever
    x: random(`x${i}`) * W, y: random(`y${i}`) * H, color: SKY[Math.floor(random(`c${i}`) * SKY.length)] ?? "#3d6aa2",
  })), []);
  useEffect(() => {
    const g = ref.current?.getContext("2d");
    if (!g) return;
    g.setTransform(1, 0, 0, 1, 0, 0); g.globalAlpha = 1; g.globalCompositeOperation = "source-over";
    g.drawImage(base, 0, 0); // full repaint: the canvas still holds the last frame
    g.lineWidth = 6; g.lineCap = "round";
    for (const s of strokes) { // positions fixed; the direction field drifts with time
      const a = noise3D("sky", s.x / 240, s.y / 240, frame / 120) * Math.PI;
      g.strokeStyle = s.color; g.beginPath(); g.moveTo(s.x, s.y);
      g.lineTo(s.x + Math.cos(a) * 16, s.y + Math.sin(a) * 16); g.stroke();
    }
  }, [frame, base, strokes]);
  return <canvas ref={ref} width={W} height={H} style={{ width: "100%", height: "100%" }} />;
};
```

Canvas rules:

- Repaint fully every frame. Reset transform, alpha and composite mode first, and set every state you use. Leftover state (lineJoin, alpha, filter) makes a frame reached by scrubbing differ from the same frame reached by playing.
- Never accumulate across frames ("don't clear, let the trails build up"). Remotion renders frames out of order and in parallel tabs. Draw a trail as the last N positions computed from `frame`.
- Precompute everything that doesn't change (stroke positions, colours, lengths, tile layout) in `useMemo`; per frame vary only angle, alpha, offset.
- Composite brand photos as `<Img>` layers between canvases rather than `drawImage`-ing them into a canvas (load timing, CORS). If you must, gate the draw on the image's load with `delayRender`.
- Pixel art: a canvas at 1/8 size (`width={135} height={240}` for 1080x1920) with `style={{ width: "100%", height: "100%", imageRendering: "pixelated" }}`, and `g.imageSmoothingEnabled = false` before any `drawImage`.

Drawn-on line with a hand-made boil (SVG):

```tsx
import { evolvePath } from "@remotion/paths";
import { Easing, interpolate, useCurrentFrame, useVideoConfig } from "remotion";

export const BoilingLine: React.FC<{ d: string; id: string }> = ({ d, id }) => {
  const frame = useCurrentFrame();
  const { width, height } = useVideoConfig();
  const step = Math.floor(frame / 4); // reseed every 4 frames = ~8 fps boil at 30 fps
  const progress = interpolate(frame, [0, 24], [0, 1], {
    extrapolateRight: "clamp",
    easing: Easing.out(Easing.cubic),
  });
  const draw = evolvePath(progress, d);
  return (
    <svg width={width} height={height} viewBox={`0 0 ${width} ${height}`}>
      <filter id={`boil-${id}`}>
        <feTurbulence type="turbulence" baseFrequency="0.02" numOctaves={2} seed={step} result="n" />
        <feDisplacementMap in="SourceGraphic" in2="n" scale={4} />
      </filter>
      <path d={d} fill="none" stroke="#1d1d1d" strokeWidth={5} strokeLinecap="round"
        filter={`url(#boil-${id})`} strokeDasharray={draw.strokeDasharray} strokeDashoffset={draw.strokeDashoffset} />
    </svg>
  );
};
```

SVG filter `id`s are document-global: suffix them per instance when a component appears more than once.

## 4. Renderer cookbook

| Renderer | Suits | Key moves |
|---|---|---|
| Flow-field strokes | expressive oil, swirling post-impressionist skies | Direction field written per region (walls vertical, floor along the perspective, sky around vortices); colour from region palettes (section 5); a darker edge on each stroke makes it thick. |
| Long curved strokes + row warp | expressionist, flowing | Each stroke follows the field for 20-30 steps; then shift every row by a sine (margin >= the largest shift, or gaps show at the edges). |
| Dabs | impressionist | Short ellipses shifted warm/cool around the block-in colour, uneven sizes. This is not pointillism. |
| Optical-mix dots | pointillism | Pure palette in fixed proportions, equal dot size, complementary dots, light bleeding across the light/shadow edge. |
| Tiles | mosaic, stained glass | Layout computed once; colour flows through the tiles each frame. Tiles follow contours (iso-lines of a distance field) and are 8-28% larger than half their spacing so neighbours cut clean grout lines. |
| Plate offset + pattern | woodblock, screen print | Fill offset (3, 2) px from the key line; patterns as `createPattern` or SVG `<pattern>`; horizontal brushed gradation. |
| Facets | cubist, low-poly | Translucent gradient planes stacked for depth; triangles left unclipped so contours turn straight-edged. |
| Halftone | pop, old print, photo-in-newsprint | 45 degree grid. A small tile through `createPattern` / `<pattern>` is about 10x faster than drawing each dot. Photo halftone: dot radius from luminance, all dots batched into one path, one `fill()`. |
| Pixel | pixel art, retro games | Paint at 1/8 size (240x135 for 1920x1080), nearest-neighbour upscale; at most 14 colours; a 1 px dark outline on each part. |
| Shaded plastic | early CGI, toy, metal | One shading recipe for everything: base colour + radial dark edge + ambient bounce + hard specular; floor reflection = mirrored copy. |
| Gold leaf | gilding, icons, ornament | Brushed noise with y frequency 20x the x frequency; an embossed dark line with a light line 1 px off; highlights only inside a "goldness" mask. |
| Soft blend | classical oil | A lightly blurred full layer under a translucent sharp layer; craquelure, canvas weave, vignette and yellow varnish as overlays. |
| Variable-width path | art nouveau, calligraphic line, linocut | Offset both sides of a centreline by a width profile into a polygon; a dark, offset copy of the silhouette underneath gives thick-outside/thin-inside lines. |
| Grain stipple | contemporary flat illustration | Dots inside shapes, density a function of position; fully static, so cache it. |
| Brush + ink bleed | ink wash, calligraphy | Pressure in and out at stroke ends; dry brush by sampling at equal arc length; blur for the bleed; paper first, ink only adds. |
| Watercolour wash | watercolour, painted anime backgrounds | Translucent overlapping washes with tide-line edges whose alpha fades as they spread. |
| Light/dark clip + sheared shadows | hard-sunlight realism, surreal | Paint a lit and a dark version, clip by light shapes; long shadows by a shear transform. |
| Light-map multiply | chiaroscuro, night, candlelight | Paint the lit version, then a light-map layer (window light + radial candle glow) with `mixBlendMode: "multiply"`. |
| Cel shadow bands | anime | A shape minus a translated copy of itself = a hard shadow band; a lit rim on the light side. |
| VHS post | vaporwave, retro video | SVG filter: split channels with `feColorMatrix`, `feOffset` red and blue by +-3 px, recombine with `feBlend mode="screen"`; scanlines as a `repeating-linear-gradient` overlay; one drifting tracking-noise band. |
| Stepped time | rubber-hose cartoon, shadow puppet, stop-motion | 10-12 fps steps (`Math.floor(frame / 3)` at 30 fps) are half the style, not lag. |

## 5. Painting practices that proved out

**Region palettes beat colour jitter.** Evidence: the first swirling-stroke pass used only colour jitter and read as "noise in one blue"; giving each region (sky, water, hills, wall, floor) its own 7-8 colour group produced the style, and another build reused it unchanged. Use: in any stroke or dab style, assign colour groups per region, draw each stroke's colour from its group, then mix 30-45% of the block-in colour back in to keep the values.

**The medium's physical process is the renderer.** Evidence: plate offset (3, 2) px + horizontal brushed gradation reads as woodblock; "layout once, colour flows through the tiles" is how a real mosaic would animate; brushed noise with y frequency 20x gave metal on the first try and was reused as-is elsewhere. Use: before writing a renderer, ask how that kind of picture is physically made, and write that process.

**Make small things bigger than instinct says.** Evidence: wave crests drawn 22-50 px did not read; 44-74 px did. Small motifs needed 1.35-1.45x scaling before they read. Use: ads are watched at phone size, so check readability on the `preview_frames` contact sheet, not at full size.

**Letter in the style's material, as paths.** Evidence: modular block lettering on a 5x7 grid, neon-tube letters, and mosaic letters with uniform thick strokes (each stroke at least 2 tiles or pixels wide; thin fonts break apart in coarse styles) all read as part of the painting. Fonts missing a glyph silently fall back to a system font, and a reviewer caught stylised letters that spelled a different word. Use: signs, labels and titles inside the painting as paths; check that the word still reads as intended. The real headline, price and CTA stay a crisp live font.

## 6. Compositing gotchas

- `source-in` per pattern element clears the previous ones (a whole patterned robe vanished). Paint all patterns onto one scratch canvas, then `source-in` once with the silhouette.
- `destination-out` on the main canvas punches transparent holes that show whatever is behind (black in the final video). Cut holes in an offscreen canvas, then `drawImage` it.
- Paper or grain over a figure with `source-atop` washes it out with the paper colour. Clip the texture to the silhouette on a scratch canvas (`destination-in`), then `multiply` it back. DOM equivalent: a masked overlay (section 9).
- `putImageData` ignores transform, clip and alpha: write into an offscreen canvas, then `drawImage`. Contexts you read pixels from: `getContext("2d", { willReadFrequently: true })`.
- Hand-drawn glyphs: two sub-paths with opposite winding in one path cancel under nonzero fill and leave holes. Fill each part separately.
- A final outline pass over stacked parts draws hidden contours through the parts in front. Draw fill + line per part, back to front, or clip the line pass by the parts in front.
- Translucent overlapping cut-paper or shadow-puppet pieces go dark where they overlap: tune stacking order and alpha per material.
- A moving region must use the same parameters as its surroundings (tile size, stroke density, line width); otherwise it shows as a patch the moment it stops.

## 7. Performance

The in-app live preview plays in real time, so keep per-frame work under ~30 ms at 1080p (one frame at 30 fps is 33 ms). Upstream timings: styles with a cached base drew in 2.5-5 ms, most in 5-40 ms, and the heaviest (three full-frame stroke passes) took 110-117 ms, which would stutter in preview.

- Cache static layers once (`useMemo` into an `OffscreenCanvas`) and `drawImage` them; per frame, draw only what moves.
- Fewer, larger strokes. At phone size, bold marks read as painted; ten thousand thin ones only cost time.
- Batch: one path and one `stroke()`/`fill()` per colour, not per mark; halftone via a pattern tile.
- Lower internal resolution, then scale: half resolution (960x540 or 540x960) is invisible for painterly layers. Keep text, logo and product at full resolution in the DOM above.
- Step motion at 8-12 fps where the style allows, and key the effect on the stepped frame (`[step]`) so in-between frames skip the redraw. Safe only when the drawing depends on nothing but `step`.
- Per-pixel loops (`getImageData`) only at low resolution, or once into the cache.
- Full-frame `feTurbulence` and large blurs are expensive in Chromium: put them on cached or small layers, and step any animated seed.
- If preview playback stutters, halve the resolution or the stroke count before anything else.

## 8. Determinism

- All randomness goes through `random(seed)` with descriptive seeds (`` `dab-${i}` ``; for boil, `` `dab-${i}-${step}` ``). Never `Math.random`, `Date.now`, `performance.now` or timers.
- The same frame must render identically every time: Remotion renders out of order, in parallel tabs, and the preview scrubs. Anything that depends on the previous frame flickers in the final render.
- `noise3D(seed, x, y, frame * k)` is a pure function of its inputs; use it for anything that drifts. Canvas `ctx.filter = "blur(...)"` is deterministic in Chromium.
- Text drawn into a canvas needs its font first: load it with `loadFont` from `@remotion/google-fonts/<Family>`, set a `fontsReady` flag when `waitUntilDone()` resolves and include it in the effect's deps, or the first frame of each render tab paints the fallback. Load the subsets your copy needs (`latin-ext` for Turkish, Estonian, Swedish diacritics); missing glyphs fall back silently.

## 9. People, faces, mascots and the product

A crude character is worse than none. One round-headed, dot-eyed figure and the viewer's first thought is "AI made this"; the rest of the ad pays for it. Upstream, code-drawn figures were the weakest element across 36 styles, while figures from real or model-made imagery held up.

Never draw these in generic code shapes:

- cartoon people (round head, dot eyes, blush, no neck, rounded-rectangle body), and stick figures acting out the story;
- white-shell robots (round white shell, blue visor, antenna, hovering or jetting);
- things with faces (smiling coins, frowning ions, balls with eyes, emoji batteries);
- the brand's mascot, redrawn. Use the brand's own mascot artwork via `<Img>`.

Pick one route per ad:

| Route | When | How |
|---|---|---|
| Real people | the brand has lifestyle, UGC or model photos | a full-bleed photo (the scene is the content; don't matte it), or a `remove_background` cut-out composited into the painted world |
| Hands, backs, silhouettes | the story needs a person, no fitting photo exists | paint only hands (holding, pointing, pocketing the product), backs, silhouettes, over-the-shoulder views, in the scene's style; no face in frame |
| No person | the product can carry the story | the object is the hero and acts through shape, motion, scale and contrast, never a face |

Make objects act without faces: through shape and motion (cold particles huddle and move slowly, warm ones spread and race; a charge bar shrinks one cell at a time in a cold wind); through scale (palm-sized to filling the frame); through contrast (two copies side by side, one frozen, one normal); through real material (a real cross-section, real frost texture, a real screenshot).

Painted hands and silhouettes: fill them black and they should still read as what they are doing; fingers or glove shapes must read as a hand, and the object sits in the hand, not beside it; same line, colour and palette as the background.

Real assets in a painted world:

- Product and logo are composited with `<Img>` at their exact URLs. Never redraw them, never repaint them into the canvas.
- Give them a light style treatment so they belong. A sticker on someone else's painting is the most common failure: upstream, figures that went through the style's renderer blended best, and flat, untreated ones were the weakest part of their segments. Light means grain at low opacity, a white paper-cut edge with a soft drop shadow, a gentle grade toward the scene palette. The product stays recognisable and the logo and on-pack text stay legible: never distort, recolour, halftone, mirror or stroke over a logo or packaging text.
- Cut-outs of people may take more of the style (grain, edge, grade, a stroke texture at low opacity), but faces stay natural.
- Place cut-outs by a base or foot anchor at `LAYOUT` coordinates, and give the same subject the same treatment in every shot.
- Several real photos of one subject (angles, poses) stepped at 8-9 fps read as limited animation (upstream frame libraries cycled 8 drawings at 9 fps, no tweening); anchor every photo at the same base point.

Light treatment for a cut-out (CSS edge and grade, grain masked to the cut-out's alpha):

```tsx
import { Img } from "remotion";

const EDGE = ["3px 0", "-3px 0", "0 3px", "0 -3px"].map((o) => `drop-shadow(${o} 0 #fff)`).join(" ")
  + " drop-shadow(0 12px 16px rgba(0,0,0,0.35))";

export const TreatedCutout: React.FC<{ src: string; id: string; seed: number }> = ({ src, id, seed }) => (
  <div style={{ position: "relative", width: "100%" }}>
    <Img src={src} style={{ width: "100%", display: "block", filter: `${EDGE} saturate(0.92) sepia(0.08)` }} />
    <svg style={{ position: "absolute", inset: 0, width: "100%", height: "100%", mixBlendMode: "soft-light", opacity: 0.5,
      maskImage: `url(${src})`, WebkitMaskImage: `url(${src})`, maskSize: "100% 100%", WebkitMaskSize: "100% 100%" }}>
      <filter id={`grain-${id}`}>
        <feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves={2} seed={seed} />
        <feColorMatrix type="saturate" values="0" />
      </filter>
      <rect width="100%" height="100%" filter={`url(#grain-${id})`} />
    </svg>
  </div>
);
// seed={Math.floor(frame / 3)} gives live grain; CSS masks load in CORS mode, so check the grain shows in preview.
```

Self-check with `preview_frames`: line up about six frames that contain people or objects and ask:

1. Does anything read as a default AI character or a white-shell robot? Change route.
2. Does something have a face that shouldn't? Remove it; let motion tell the story.
3. Do hero and background share one visual language? If not, treat the hero, or show only hands.
