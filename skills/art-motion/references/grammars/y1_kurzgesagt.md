# Flat scale-travel explainer (Kurzgesagt tradition)

> Adapted from huashu-art-motion (MIT, (c) 2026 alchaincyf) - references/动画语法/y1_kurzgesagt.md

Turn an abstract claim into one concrete object inside a glowing, infinitely zoomable flat world; the camera travels between scales, the ambient layer keeps moving softly, and the subject changes only on copy beats, then holds.

Evoke the grammar; never copy the channel's characters, branding or footage.

## Use it / avoid it

Use it for:
- "What's inside" and scale: ingredient to product, one pixel to the whole app, one user to the network, "zoom in and you find...". The scale dive is the signature move.
- Mechanisms and systems made of invisible processes (signals, energy, data, flavour) drawn as glowing particles and connections.
- A calm, curious, "serious but cute" tone. Source pace: ~168 words/min narration, ~2 sentences per hard-cut shot (measured). In a silent ad: one copy line per visual state.

Avoid it for:
- Real people, real events, testimonials, press: flat cartoon dilutes credibility (use y2_vox).
- Step-by-step reasoning (use y3_whiteboard).
- Thin build budgets. The look depends on something moving in every frame (the studio reports 1200+ hours per film (official)); a cut-corner version reads as a cheap slide deck. In an ad, build 1-3 rich scenes rather than many thin ones.

## Before you start

1. Write the visual metaphor first: what object is this claim? (cell, gear, pipe, city, droplet; in ads often the product, its key ingredient or component.) If a line has no object, do not fall back to a glowing ball with label pills.
2. The upstream demo's orange planet with satellite nodes is one drawing, not the grammar's signature. Choose the centre object's shape and colour from the subject. When a real product photo exists, clip it into the centre object (circle or rounded mask around an `<Img>`) and put the name in a pill below.
3. Every copy beat gets at least one state change (pop, morph, dive, pull-out). Count the beats: two consecutive beats with no change means you add an event, never floating or a slow push.
4. The subject holds once it lands. Only the ambient layer (twinkling stars, drifting particles, far clouds) keeps moving; no breathing or bobbing on the subject or labels.
5. Pause before a dive: hold the target at least 0.3 s (9 f) and light it up so the viewer knows which one we enter. Zoom on a log scale.

## Composition

- Pick one era and do not mix: 2025 dark (61-68% dark pixels, median saturation 0.84-0.89) or 2014 light grey-white, low saturation (measured). Switching the whole colour temperature at a section change is part of the grammar (the demo went from night to day).
- Measured 2025 palette, a record and not a palette to copy: ground #05020F / #0E0631 / #25155E; sub-ground #191670, #3826A3, #5F58DB; cyan #32BAEE, #7DD3DC; orange-yellow glowing bodies #F48301, #E07919, #FACC12 with glow core #F9EF93; magenta #BE3A95, #C83C7F; highlights and text #E7DFE1, #F9FCFB.
- The rule to keep: one dark ground + 2-3 saturated accents that contrast each other (orange-yellow against indigo, cyan against magenta) (measured + inferred).
- Do not ship the deep-violet starfield. Blue-purple gradients, deep-purple starfields and neon cyan-violet glow are the most recognisable "AI slop" defaults; avoid them unless the brand palette itself is blue/purple. Use a flat deep ink ground (#121417, surface #1E2226) or flat navy (#0D1B2A, surface #16293D), and map the brand's 2-3 strongest colours into the accent and glow roles. Logo and product stay `<Img>`, never redrawn.
- Shape language: no outlines. Shadows are the same hue one step darker, never grey; highlights are a white ellipse or arc (inferred). Rounded everything, organic blobs, round heads, tube limbs. Every glowing body gets a radial glow: the dark ground exists so glow can read.
- Two-tone facet (demo): inside each shape leave a shadow band bottom-right, offset about (10, 12) px, and a thin highlight edge top-left, about (4, 5) px. Apply it to every part so everything looks drawn by one hand (snippet below).
- Layout: subject on the lower third, sky above for stars and labels.
- Depth: 5-6 parallax layers (demo): starfield d = 0.05, moon 0.12, far hills 0.3, near slope 0.65, subject 1.0, foreground leaves 1.5 (blurred ~7 px and darkened into the ground colour family, not near-black). The films measure 2-5 layers (inferred).
- Typography: labels are a thin white leader line, then text. Label pills: large radius, saturated solid fill, bold sans. Titles: heavy sans, characters rising one by one.

## Motion

Easing (official, from the studio's course):
- Standard action: `Easing.bezier(0.75, 0, 0.25, 1)` (After Effects 75% influence: soft start, fast middle, soft end), 0.83 s (25 f). Snappier variants 0.5 / 0.33 / 0.17 s (15 / 10 / 5 f); pops 0.08-0.17 s (3-5 f).
- Loops and cycles: `Easing.bezier(0.333, 0, 0.667, 1)` (Easy Ease 33.3%).

Pop-in (measured): 90% size by 0.25 s, overshoot to 108% at ~0.33 s (one card reached 114%), back to 100% by ~0.5 s. `spring({frame, fps, config: {mass: 1, stiffness: 150, damping: 15}})` reproduces it (peak 1.087 at frame 10, settled by frame 16); damping 13 gives ~114%. Small labels (demo): 0.5 s with `Easing.out(Easing.back(1.1))` (~4.5% overshoot).

Stagger (official): same-type elements 0.17-0.33 s apart (5-10 f), limbs ~0.06 s (2 f), pause between actions 0.33 s (10 f). Demo values: title characters 45 ms apart, each 0.5 s `Easing.out(Easing.cubic)`; a 144-block mosaic assembling from the edges, staggered by distance from centre 35 ms per cell, each 0.5 s `Easing.out(Easing.back(1.4))`; a network lighting up layer by layer 0.32 s apart, each node popping in 0.35 s.

Ambient vs subject: in 2025 films only 0.3% of the runtime is fully still for 0.5 s (measured), but what moves is the ambient layer and the thing being discussed, not everything. Explainer shots: subject and info land and hold; motion happens on beats. Pure mood shots (opening, a breath between sections) may keep light ambient motion. Demo ambient: 170 stars each with its own phase, twinkling at 1-3.5 rad/s; particles drifting on depths 0.8-1.3; signal pulses looping along connections; grass swaying at 2.1 rad/s. Drive all of it from the frame with `random(seed)` per particle and `noise2D` from @remotion/noise.

Blink (official): close over 0.08 s (~3 f), open over 0.17 s (5 f), irregular intervals; eyes never shrink to zero.

## Camera and transitions

Camera (measured, 2025): about a third of the runtime is zooming, ~10% panning, ~5% rotating, and pull-outs outnumber push-ins. Zooms are scale travel and reveals, never filler.
- Calling out a node: hold, slow push ~0.9 s (27 f), hold; move to the next node in 0.7 s (21 f); only the reveal gets a snap push 0.28 s (8 f) or a slam 0.17 s (5 f). After pushing in, give it back with a pull-out. Never a constant slow push across a shot (the demo's 2.6 s linear push 1.00 to 1.10 is the old way).
- Ambient layers may move freely; push-ins are rationed; dives and pulls use the durations below.

Transitions:
1. Push through, object colour fills the frame, new scene (the standard scale transition). Measured ~1.4 s (42 f), accelerating then decelerating, speed peak mid-way. Demo recipe: log-zoom into the lit node for 0.45 s (14 f) with `Easing.in(Easing.cubic)` until the frame is solid colour; cross-dissolve +-2 f around the midpoint into a same-coloured object of the next scene (keep both highlights on the same side so the cut hides); pull out 1.45 s (44 f) with `Easing.inOut(Easing.cubic)` from 42x to 1x into the new palette. Never `Easing.out(Easing.exp)` on that pull: its first frame jumps from 42x to 15x.
2. Lens dive: the next world shows only inside an opening (lens, window, pore, bottle neck) that grows as the camera pushes in. Demo: 1.0 s (30 f), `Easing.bezier(0.75, 0, 0.25, 1)`, log zoom 1.1 to 60; an accent ring on the opening's edge; the next scene simultaneously rises from 0.42x with `Easing.out(Easing.exp)`. A subject half-cut by the growing circle mid-dive is normal.
3. Fast pull-out reveal: 0.2-2 s, fast start and long tail (measured per-0.2 s zoom ratios 1.074, 1.040, ... 1.0006). Connects micro and macro; a natural ad ending that lands on the product or logo (inferred).
4. Light or flash fill from a light source inside the scene, ~0.5 s (15 f).
5. Sweep wipe: an object or light band sweeping diagonally with speed lines, ~0.4 s (12 f).
6. Duplicate to fill ("so many that..."): copies multiply until they tile the frame, 3-6 s in long-form; shorten for ads.

Hard cuts are rare (~5/min) and land 0-0.2 s before a sentence starts; other changes are designed 0.3-0.6 s transitions every 4.6-6.7 s (measured). Long-form hard-cut shots have a median of 7-9 s (mean 11.5 s), but the visual unit changes every 4.6-6.7 s. The upstream 8 s demo packed 3 shots (~2.7 s each) at about 3x long-form density (demo); a 15 s ad holds roughly 3-5 visual states with one or two dives (inferred).

Labels (measured): the leader line draws, then text types at ~40 characters/s; one label per sentence, held ~3 s, then erased character by character. Without voiceover, hold until it can be read.

## Build it in Remotion

- One world per scene, drawn as SVG/DOM in world coordinates, inside parallax layers that share one camera `{cx, cy, z}` computed purely from `useCurrentFrame()`. Screen-space overlays (logo, CTA, captions) sit outside the world.
- The scene redraws itself at every camera value. Never scale a bitmap of the previous shot (a 20x enlarged raster turns to mosaic). Avoid `will-change: transform` on zoomed layers; a product `<Img>` shown at high zoom needs native resolution at least its on-screen size.
- Log zoom plus anchoring: interpolate `ln z`, and shrink the target's screen offset linearly so it glides to centre instead of swinging out first.
- Cover zoom for an opening of world radius r: z >= (distance from the opening's screen centre to the farthest corner) / r. Centred: 1101/r at 1920x1080 or 1080x1920, 864/r at 1080x1350, 764/r at 1080x1080.
- Lens reveal: render the next scene in an `<AbsoluteFill>` with `clipPath: circle(Rpx at Xpx Ypx)`, where X, Y, R are the opening's screen position and radius (screen = centre + (world - cam) * z); stroke a ring of the same radius above it.
- Hard cuts are adjacent `<Sequence>`s; the +-2 f dissolve can be a `<TransitionSeries>` with `fade()`; dives and pulls are hand-built camera moves (no stock presentation does a log zoom).
- Glow: an SVG `radialGradient` behind each glowing body (core colour to transparent); avoid stacking heavy CSS blur filters on many items.
- Leader lines: `evolvePath` from @remotion/paths, then `text.slice(0, n)` for typing.

```tsx
import {Easing, interpolate} from 'remotion';

type Cam = {cx: number; cy: number; z: number}; // world offset from centre, zoom

export const zoomTo = (frame: number, f0: number, f1: number, from: Cam, t: Cam): Cam => {
  const p = interpolate(frame, [f0, f1], [0, 1], {
    easing: Easing.bezier(0.75, 0, 0.25, 1),
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });
  const z = Math.exp(Math.log(from.z) + (Math.log(t.z) - Math.log(from.z)) * p);
  // Anchor: the target's screen offset shrinks linearly to 0.
  const sx = (t.cx - from.cx) * from.z * (1 - p);
  const sy = (t.cy - from.cy) * from.z * (1 - p);
  return {cx: t.cx - sx / z, cy: t.cy - sy / z, z};
};

// Parallax layer at depth d: offset scales with d, zoom with z^d.
// Use with transformOrigin: '0 0' on a full-size <AbsoluteFill>.
export const layerTransform = (c: Cam, d: number, w: number, h: number) =>
  `translate(${w / 2}px, ${h / 2}px) scale(${Math.pow(c.z, d)}) ` +
  `translate(${-w / 2 - c.cx * d}px, ${-h / 2 - c.cy * d}px)`;
```

Two-tone facet (no outline): shadow band bottom-right, highlight edge top-left.

```tsx
export const Facet: React.FC<{id: string; d: string; base: string; shade: string; light: string}> =
  ({id, d, base, shade, light}) => (
    <g>
      <clipPath id={`${id}-a`}><path d={d} /></clipPath>
      <clipPath id={`${id}-b`}><path d={d} transform="translate(-10 -12)" /></clipPath>
      <g clipPath={`url(#${id}-a)`}>
        <path d={d} fill={shade} />
        <g clipPath={`url(#${id}-b)`}>
          <path d={d} fill={light} />
          <path d={d} fill={base} transform="translate(4 5)" />
        </g>
      </g>
    </g>
  );
```

## Pitfalls

1. Turning "always moving" into everything breathing. What moves is the ambient layer and the thing being discussed. Floating everything or a constant slow push still reads as a slide deck.
2. Linear zoom interpolation (slow then violent; the sense of travel breaks) or enlarging a bitmap instead of redrawing at the new zoom.
3. A bright, busy palette, outlines, or a mid-brightness ground: it slides into children's-book or corporate flat illustration. Shadows one hue-step darker, never grey.
4. Outlined grass and hills read as a kids' illustration: use filled thin triangles, and keep edge highlights one step from the base colour.
5. A near-black foreground blob in a corner reads as dirt: blur it and lift it into the ground's colour family.
6. A title vanishing in one frame: fade it over ~0.55 s with `Easing.inOut(Easing.sin)`.
7. A recurring object changing colour without explanation: introduce the new one with a leader line and label first.
8. A still ending: end on an event (fast pull-out to the full view, or a dive into the next layer, then the product or logo), then hold. No slow push to fill it.
9. Paths crossing other objects (something flying through a character): check trajectories in frame previews.
10. Zero still frames in previews only proves the ambient layer moves; also check that sampled frames do not read as a sequence of slides.
