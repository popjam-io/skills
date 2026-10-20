# Mechanism Visualisation (3Blue1Brown / manim)

> Adapted from huashu-art-motion (MIT, (c) 2026 alchaincyf) - references/动画语法/t1_3b1b.md

Only the thing being explained sits on a black screen, smooth morphs (Transform) turn one concept directly into the next, colour is the concept's name, and the piece almost never cuts.

Evoke the grammar; never copy the channel's characters, branding or footage.

## Use it / avoid it

Use it for:
- How a mechanism turns, step by step, into something else: a network's forward pass, attention, matrix transforms, gradient descent, probability, an algorithm. Best when the copy is made of action sentences ("flatten the image into a column", "multiply each pixel by a weight"): one sentence = one Transform.
- Letting viewers "see the maths": formula symbols map one-to-one onto objects (`W` is blue in the formula, and so are the edges).
- Ads: a product's "how it works" beat (how matching, personalisation, a filter or a sensor works), when there is a real object that can transform.

Avoid it for:
- Launches, emotional or brand pieces: black and thin lines are cold and slow.
- Real data trends (use the finance chart grammar).
- Opinions, stories, slogans: nothing to morph, so it turns into decoration.
- Fast edits: the native rhythm is 1-3 s per animation plus a 1 s hold, so 3 shots in 8 s is the ceiling. In a 15-30 s ad, give it one 8-15 s segment.

## Before you start

1. For each shot, write "what becomes what" (grid -> circle, one curve -> another, pixels -> neurons). If you can't write that sentence, don't use this grammar.
2. The first frame is the object. Axes, grid or curve come first; the title and formula come after. Never open on a title being written at 0 s.
3. Count the text on screen: at most 2 points at once. Before a third arrives, the earlier ones become a figure or leave. Bullets written one by one are a slide deck on black.
4. Write the colour table first: one colour per concept, formula symbols the same colour as their objects, <= 4 semantic colours in the whole piece.
5. Holds are still: no constant slow push, breathing or floating. The camera moves only to look at the next object, then stops.

## Composition

| Item | Value | Source |
|---|---|---|
| Background | Pure black `#000000`. The "dark navy `#0E1525`" quoted online comes from marketing blogs, not the original | (official) 3b1b `custom_config.yml` |
| Saturation | manim colour constants, then the whole frame at 1.5x saturation; raw values look washed out | (official) 3b1b's exports apply 1.5x saturation |
| Colours | BLUE_C `#58C4DD`, RED_C `#FC6255`, YELLOW `#FFFF00` (3b1b's pure yellow, not Community Edition's `#F7D96F`), TEAL_C `#5CD0B3`, GREEN_C `#83C167`, GREY_A-E `#DDDDDD` `#BBBBBB` `#888888` `#444444` `#222222` | (official) manim `default_config.yml` |
| Colour coding | One colour = one concept, for the whole piece. Demo: yellow = activation/signal, blue = positive weight, red = negative weight; `a` yellow, `W`/`w` blue in formulas | (official) 3b1b neural-net episode code |
| Strokes | default 4 px at 1080p; axes and network edges 2 px; grid main lines 2 px, subdivisions 1 px at 25% opacity | (official) manimlib |
| Unit | frame height = 8 units, so 1 unit = 135 px at a 1080 px short side | (official) |
| Nodes | white 2 px stroke; fill opacity = activation; radius 0.15 u (~20 px); spacing 0.25 u within a layer; at most 16 drawn per layer, the rest as a vertical ellipsis + brace | (official) |
| Edges | circumference to circumference; width `3 * (abs(w)/max)^3` (demo `0.6 + 3.2 * abs(w)^3` px); positive blue, negative red; opacity 0.7-0.85 | (official) / (demo) |
| Type | Formulas in Computer Modern (CMU Serif), which is not loadable here: use `STIXTwoText` from `@remotion/google-fonts` (italic for variables, upright for words like softmax), or Georgia as a fallback. Labels in the same serif. Demo sizes: title 58 px, formula 64 px | (official) / (demo) |
| Layout | One subject per screen, centred or symmetric. Title/formula pinned in the top 1/8 (y ~110-150 at 1080p) and never moved by the camera. Landscape: text left, figure right. Vertical: figure on top, text below | |
| Shapes | Circles, grids, lines, braces, arrows. Almost no glow: the "glow" is saturated thin lines on pure black, not bloom. Emphasis = Indicate (tint yellow, scale up), never a halo | (inferred from the originals) |

Brand mapping: keep pure black (or the brand's own near-black) as the stage. Give brand colours to concepts only if they read on black. Logo and product images go in via `<Img>`, outside the saturation filter. No blue-purple gradients or deep-purple starfields.

## Motion

- **Easing:** `smooth = 6t^5 - 15t^4 + 10t^3` (3b1b's version: zero velocity and acceleration at both ends; Community Edition uses a sigmoid). Use it for nearly everything. Linear only for Write, constant rotation and the travel of a passing flash. `there_and_back` for Indicate; `rush_into` / `rush_from` for diving in and out.
- **Durations:** default run time 1 s (30 f), hold 1 s. In the 2023-24 source, explicit run times are most often 2 s (481 uses) > 3 s (333) > 1 s (187) > 4 s (145) (measured).
- **LaggedStart:** default lag ratio 0.05; 0.1 is the most used in the source. Item i runs over `[i*r, i*r + 1]` of a total `1 + (n-1)*r`. Demo: 100 pixels -> neurons at 0.01 (1.1 s), 160 edges at 0.006.
- **Write:** linear. Under 15 sub-objects take 1 s, otherwise 2 s; lag between glyphs `min(4/(n+1), 0.2)`. Each glyph draws its outline first, then fills: over the last 60% the fill fades in and the stroke fades out.
- **Transform:** both shapes resampled to the same number of points with aligned start points (both from the upper left, clockwise); each point moves in a straight line (no arc), and the colour interpolates too.
- **Enter / exit:** FadeIn / FadeOut with a 24-40 px shift (rise in, drift up and out). A new layer of nodes fades in from 24 px to the right. Replaced items shrink to a point and merge into the ellipsis.
- **Signal (ShowPassingFlash, time width 2):** duplicate the edge, tint it yellow, width x1.5; the visible window is `[max(0, u-2), min(1, u)]` of its length while u runs 0 -> 3 linearly; stagger input rows by lag 0.04.
- **Counting:** values (0.95) count up together with the fill and never appear before the picture.

## Camera and transitions

Camera baseline: the camera moves on events, never as texture: hold -> push to the next object -> hold. The default push is smooth, ~1 s (30 f), in one go. A quick push (0.28 s / 8 f, 18-32% closer) is only for the moment the conclusion lands, once or twice per segment. Orbit 3D scenes at 0.5-3 deg/s (3b1b default 1 deg/s), and only for spatial relations. Never fill a hold with a constant slow push (the demo's 1 -> 1.025 creep is the outdated approach).

Transitions:
1. **Transform continuity (no cut)**, by far the most used: the last frame of shot N is the first frame of shot N+1, and a morph turns the old object into the new one. Demo: 100 pixel squares become a column of input neurons, and the two shots match pixel for pixel at the handoff.
2. **Zoom through:** the camera zooms exponentially into an object (zoom = Z^e, constant perceived speed); its outline becomes an opening that contains the new scene. Final zoom must be >= (distance from the opening's centre to the farthest frame corner) / r, ~1100 / r when centred at 1080p, or the opening never covers the frame and the last frame jumps. Keep the new scene's subject centred in the opening until ~55% progress, then let it settle. Demo: outline the target node in yellow for 0.3 s ("look at this one"), then push 48x in 0.75 s (22-23 f).
3. **FadeOut + FadeIn, both shifted up**, for a change of topic.
4. **Formula replacement:** each symbol travels to the same symbol's position in the new formula (TransformMatchingTex, 2 s by default in 3b1b's version); unmatched symbols fade out and in.

Timing:
- One animation takes 1-3 s, then ~1 s hold; one concept often runs 8-20 s. The demo's 3 shots in 8 s (2.6 / 2.8 / 2.6 s) are compressed; real use is 2-3x longer.
- One sentence = one animation: it starts on the action verb, settles at the end of the sentence, then holds ~1 s. 3b1b lays out the animations first and records the voice afterwards (official, interview).
- Ask, then show: the question or title is written before the action. One title line plus one note line at most.
- Every movement must have an identifiable explanatory purpose (3b1b FAQ). Delete the rest.

## Build it in Remotion

- **One continuous SVG scene per concept** rather than cut `<Sequence>`s. Transform continuity is easiest when shot N+1 is the same component continuing. If you do split, shot N+1's frame 0 must render exactly shot N's end state, with the same geometry: a true circle handing off to a 48-gon shows a seam.
- **Camera inside the SVG** (a `<g transform>` or a computed `viewBox`), not a CSS scale of a rasterised layer, so a 48x zoom stays crisp. Interpolate zoom in log space: `z = Math.exp(interpolate(p, [0, 1], [Math.log(z0), Math.log(z1)]))`.
- **Morph:** `interpolatePath(p, a, b)` from `@remotion/paths` plus `interpolateColors`. Build both shapes with the same segment count, start point and direction (snippet below).
- **Draw a line or axis:** `evolvePath(p, d)`. **Passing flash:** `getLength(d)`, then `strokeDasharray = (end - start) * L + " " + L` and `strokeDashoffset = -start * L`.
- **Write text:** reveal glyphs left to right with a linear clip, stroke only (`fill` transparent), then cross-fade the fill in and the stroke out over the last 60%.
- **Saturation:** `filter: "saturate(1.5)"` on the diagram layer only (or pre-saturate the hex values), never on brand images.
- **Title/formula layer** outside the camera group.
- **Vertical fallbacks:** when points don't fit, shrink the figure first (50% -> 30% of the height), then the type (not below 0.6x), then scroll the oldest point out.

```tsx
// 3b1b rate functions
export const smooth = (t: number) => t * t * t * (t * (6 * t - 15) + 10);
export const thereAndBack = (t: number) => smooth(t < 0.5 ? 2 * t : 2 - 2 * t);
export const rushInto = (t: number) => 2 * smooth(t / 2);
export const rushFrom = (t: number) => 2 * smooth(t / 2 + 0.5) - 1;
// LaggedStart: progress of item i of n at overall progress p, lag ratio r
export const lagged = (p: number, i: number, n: number, r: number) =>
  Math.min(1, Math.max(0, p * (1 + (n - 1) * r) - i * r));

// Square and circle as 4 cubic segments, both starting upper-left and running clockwise,
// so interpolatePath(p, squareD(...), circleD(...)) morphs without twisting.
const DIAG = [-135, -45, 45, 135].map((a) => (a * Math.PI) / 180);
export const circleD = (cx: number, cy: number, r: number) => {
  const k = (4 / 3) * Math.tan(Math.PI / 8) * r;
  const P = (a: number) => [cx + r * Math.cos(a), cy + r * Math.sin(a)];
  let d = `M ${P(DIAG[0]).join(" ")}`;
  DIAG.forEach((a, i) => {
    const b = DIAG[(i + 1) % 4];
    const [x0, y0] = P(a);
    const [x1, y1] = P(b);
    d += ` C ${x0 - k * Math.sin(a)} ${y0 + k * Math.cos(a)} ${x1 + k * Math.sin(b)} ${y1 - k * Math.cos(b)} ${x1} ${y1}`;
  });
  return `${d} Z`;
};
export const squareD = (cx: number, cy: number, h: number) => {
  const c = [[-h, -h], [h, -h], [h, h], [-h, h]].map(([x, y]) => [cx + x, cy + y]);
  const seg = (p: number[], q: number[]) =>
    ` C ${p[0] + (q[0] - p[0]) / 3} ${p[1] + (q[1] - p[1]) / 3} ${p[0] + ((q[0] - p[0]) * 2) / 3} ${p[1] + ((q[1] - p[1]) * 2) / 3} ${q[0]} ${q[1]}`;
  return `M ${c[0].join(" ")}${c.map((p, i) => seg(p, c[(i + 1) % 4])).join("")} Z`;
};
```

## Pitfalls

1. **Treating glow as the signature.** Bloom plus a dark-blue gradient reads as a "tech slide deck". The original is pure black, saturated thin lines and 1.5x saturation, with almost no glow.
2. **Linear or generic easing, animations fast and many.** The default must be smooth; 1-3 s per animation, then a 1 s hold; each move maps to a verb in the copy.
3. **Colour code drifting, or too many colours.** One colour = one concept, and a formula symbol matches its object. Beyond 3-4 semantic colours viewers lose track.
4. **Diagram logic errors.** The demo's first cut drew an output neuron's weights as a pixel image, but the output layer connects to the hidden layer, not to pixels. Check that whatever you connect really is connected.
5. **No hold on the conclusion.** A value finished counting in the last 0.1 s. Land the result, then hold >= 0.6 s (18 f), and keep the legend on screen to the end.
6. **Pushing in too soon, leaving ghosts.** Highlight the target 0.3 s before the push. Clear the old picture outside the opening completely (between ~45% and 80% of the transition) so no thick edges trail into the new title, and start writing the new title ~0.75 s in.
7. **Too many concepts.** Five concepts in 8 s is too many; in an ad, one mechanism per segment.
