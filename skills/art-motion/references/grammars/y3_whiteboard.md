# Whiteboard explainer (RSA Animate tradition)

> Adapted from huashu-art-motion (MIT, (c) 2026 alchaincyf) - references/动画语法/y3_whiteboard.md

Say a line, write a line: a marker writes and draws on one large whiteboard as the argument unfolds, the camera follows the argument across the board, and a final pull-out reveals the whole argument as one picture.

Evoke the grammar; never copy the channel's characters, branding or footage.

Pick one sub-grammar and never mix them:
- Big-board type (RSA Animate): one huge board, the camera moves across it (5.3 moves/min, measured). This card follows it.
- Sheet type (Minute Physics): one sheet per shot, hard cuts between sheets (8.1/min), static camera. Notes on it appear under transitions.

## Use it / avoid it

Use it for:
- Arguments: cause-and-effect chains, a point of view, a short history, problem to cause to fix. Concepts with relationships that can be mapped in space; the RSA illustrator describes the method as laying information out in space so its relationships become visible (official).
- One short reasoning chain: the sheet type.
- Ads (inferred): "why X fails and Y works", "how it works in 3 steps", B2B explainers. Without voiceover the handwriting itself is the copy, so keep each written phrase short.

Avoid it for:
- Precise data charts (hand-drawn error is large; use t3_finance_chart).
- Complex motion or spatial relations (a whiteboard has no depth).
- Emotional intensity (monochrome line art is weak there).
- Expecting better comprehension: a 2016 study (Turkay) found no learning advantage over other formats. Its value is attention and a sense of company (secondary).

## Before you start

1. "Draws little, writes a lot" is a storyboard problem: decide each block's drawn object or joke before its text. Handwritten lines stay within one line. If a block is only text, it is a slide; give it a drawing (for ads the written text is the copy, so this check is about drawings, not about duplicating a voiceover).
2. Rotate block templates. The same structure ("year, object, orange label" or "bullet dot, one line, one icon") at most 3 times; then switch to a comparison (two side-by-side drawings), a flow (arrow chain), a magnified detail, or one large drawing.
3. Never hand-type camera coordinates: compute the frame from the block's stroke bounding box plus margin, and push half-cut old writing out of frame.
4. Fix line meanings from the first stroke: solid = happened, dashed = planned, dotted = a leader across blocks. Things on the board are either erased or stay; they never fade.
5. Check every object's silhouette for accidental rude shapes. Tall objects with a round head, flared sides and a round base are the usual offenders: give them a pointed top or flat base.

## Composition

- Palette (RSA, measured): board white #FBFBFB; line black #0A0503; one accent, orange: text #EB701F, fills #F3742D, hatched light-orange areas about #E9A67C. Orange is ~22% of all ink pixels and appears only on keywords and hatched fills.
- Sheet type (measured): pinkish off-white paper #E7DBE1 with coloured-pencil light yellow #EDE6A2 and light blue #B5CBE8.
- Demo: #FBFBFB, #0A0503, accent #EF7226, fills as a 22%-opacity orange wash.
- Brand mapping (inferred): the brand's primary colour becomes the single accent if it is saturated and readable on white; keep black line and white board. Logo and product appear as `<Img>` pinned to the board (they can be revealed, never redrawn).
- Line weight (measured on 1080p landscape): strokes ~0.6-0.7% of frame height (6-7 px), hatching ~0.3%, title letter height ~5.5% of frame height (~60 px). The sheet type uses thicker lines (~0.8%). Demo 6.5 px. On vertical and square canvases scale from the 1080 px short side (inferred).
- Layout: RSA plans the final full picture first and draws toward it (official). Each frame-full holds 3-6 text/drawing groups, filled, then left behind. A smooth move shifts only ~0.23 frame widths, so old and new areas overlap ~75% and the viewer always sees the edge of the previous block (measured). The closing full view is a long horizontal scroll; for 9:16 ads a tall vertical scroll is the natural equivalent (inferred).
- Lettering: hand-printed capitals in comic style. Use a hand-lettered Google Font via @remotion/google-fonts (for example Patrick Hand for body, Permanent Marker for titles).
- The hand: a real right hand holding a black marker enters from the bottom-right, forearm angled down-right, covering 15-25% of the frame; it leaves entirely when not drawing. On screen RSA 49%, sheet type 40% of the time (measured). A code-drawn cartoon hand read as fake in the upstream review. Use a supplied photographic hand cut-out if one exists; otherwise show only the marker tip leading the line, or no hand at all (inferred).

## Motion

Writing speed (measured, 9 samples): body text median ~16 characters/s; the opening title at half speed, ~7.5 characters/s, to establish it; narration runs ~13 characters/s, so writing roughly equals speech. In a silent ad, 16 characters/s is also a comfortable read-along pace (inferred).

Drawing speed (measured + inferred): small icons 0.5-1 s (15-30 f), a portrait ~2 s (60 f); RSA adds new ink at a median 0.25% of the frame area per second. Complex illustrations are not drawn on camera: they are pre-drawn and revealed as the camera arrives, or cut in whole while the hand only adds colour. Real productions are sped up: one channel shoots one photo per second and holds each 2 frames (~12x); RSA is inferred at 5-8x.

Demo parameters (compressed for an 8 s piece; slow them in long pieces, keep them for short ads):
- Line speed 2600 world px/s, about 2x RSA. Stroke duration = length / speed, minimum 0.04 s, 0.02 s pen-up gap. Each stroke eases `Easing.inOut(Easing.sin)` (slow start and finish).
- Figures appear with a 0.7 s zigzag reveal: the pen tip zigzags 8 rows across the figure's bounding box and a mask uncovers only where it has passed, the tip always on the leading edge. Text without stroke-order data: each glyph revealed by a 3-row zigzag with the tip following, which reads as writing. (The first attempt, dashing all strokes at once, was judged "the pen does not lead the line".)
- Keywords without the hand: RSA pops some orange keywords in during post, no hand (measured). Demo: 0.3 s `Easing.out(Easing.back(2.2))` (~15% overshoot).

Pen path:
- Gap under 0.25 s between strokes: the tip glides from the last end to the next start along an arc lifted ~30 px, `Easing.inOut(Easing.sin)`.
- Longer gap: the hand leaves to the bottom-right off-screen in 0.35 s `Easing.in(Easing.cubic)`, and returns from the bottom-right 0.3 s before the next stroke with `Easing.out(Easing.cubic)`.

Continuous motion: the life of the genre is the hand always drawing. RSA's drawing activity barely correlates with word density (|r| < 0.07): the hand keeps going through pauses (measured).

## Camera and transitions

1. Smooth pan or zoom across the board (RSA's main move, 41 uses): 1.2-2.4 s (36-72 f), `Easing.inOut(Easing.sin)` (measured peak/mean speed 1.49; a pure sine gives 1.57). Shift ~0.23 frame widths, ~75% overlap. Demo: a 0.9 s diagonal move of ~0.5 widths while zooming to 1.12x, starting while the hand draws an orange connector toward the new area, so the hand leads the camera.
2. Whip pan: fast pan with motion blur, ~0.8 s (24 f), 0.5-1.2 frame widths, to jump to a distant region (RSA 15 uses). Demo: 0.8 s `Easing.inOut(Easing.cubic)` across about one screen, a 9-sample blur only during the whip; smooth moves and the pull-out stay sharp.
3. Pull-out reveal of the whole board (the ending). RSA: grey wash, 0.6 s fast pull-out, ~9 s pan along the scroll, then a pull-out to the full picture; whiteboard tools default to "zoom out at end" (official). Demo: 0.65 s sine pull to 0.45x, hold 0.5 s, while the whole board tints very light grey #EEEEEC over 0.5 s. In ads, land the logo or CTA on the board at the end of the pull (inferred).
4. Cloud or explosion wipe: cartoon smoke fills then clears, ~1 s (RSA once).
5. Hard cut: to a pre-drawn image (RSA, rare); the sheet type's sheet change (its main transition); the sheet type also inverts the whole frame for a "night" beat.

Not in the sampled films: pushing into a frame or thought bubble, page flips.

A new block equals a new point: transitions land on topic changes, not on pauses. On the big board, panning between blocks is the main syntax and may repeat; push in only for what must be read, then pull back.

Rhythm (measured): RSA holds a median 6.6 s between camera moves (IQR 4.0-13.8 s); the sheet type's median shot is 7.1 s. The demo fit 3 blocks into 8 s, ~2.5x real density. A 15 s ad fits roughly 2-4 blocks (inferred).

Sync (core, measured): writing starts 0.2-0.8 s after its phrase begins (median +0.5 s) and finishes within 1 s after the phrase ends: slightly behind, never ahead. Exception: visual setups (a pill bottle, an arrow) are drawn seconds early and wait for their line. The sheet type drops the drawing ~0.3 s after the noun. Tool defaults for reference: hold 0.5 s after a draw, camera move 1 s, 3 s per drawn asset.

## Build it in Remotion

- One board world (a large SVG with all blocks laid out in board coordinates) under one camera wrapper; every "transition" is a camera move on the same board, so nothing on the board ever jumps.
- A stroke timeline: an ordered list of strokes with start and duration computed from path length (snippet). Compute each block's end time and make sure the camera only moves after it (the demo's first version scheduled block 2 to finish at 7.9 s, 2.5 s after the camera had already left).
- Strokes: `evolvePath(progress, d)` gives `strokeDasharray`/`strokeDashoffset`; round caps and joins.
- Hand-drawn feel: densify path points and add a low-frequency `noise2D` offset of 1-2 px with a fixed seed, constant over time.
- Pen tip: `getPointAtLength(d, length * progress)` places the marker; between strokes interpolate along a lifted arc.
- Zigzag reveal for text and figures: an SVG `<mask>` containing a thick polyline zigzag over the glyph or figure box, itself drawn with `evolvePath`; the pen follows the polyline's head.
- Frames around pasted images: fill with the board colour before stroking, so a frame in front hides lines behind it.
- Erase smudges live in screen space (follow the camera's pan, not its zoom), or a 5x push turns them into a grey blob.
- Whip blur: wrap only the whip window in `<CameraMotionBlur samples={9}>` from @remotion/motion-blur.

```tsx
import {evolvePath, getLength} from '@remotion/paths';
import {Easing, interpolate, useCurrentFrame, useVideoConfig} from 'remotion';

type Stroke = {d: string; start: number; dur: number}; // seconds
const SPEED = 1300; // world px/s, about RSA pace (the demo used 2600)

export const timeline = (paths: string[], t0: number): Stroke[] => {
  let t = t0;
  return paths.map((d) => {
    const dur = Math.max(0.04, getLength(d) / SPEED);
    const s = {d, start: t, dur};
    t += dur + 0.02; // pen-up gap
    return s;
  });
};

export const Ink: React.FC<{s: Stroke; color: string; w: number}> = ({s, color, w}) => {
  const t = useCurrentFrame() / useVideoConfig().fps;
  const p = interpolate(t, [s.start, s.start + s.dur], [0, 1], {
    easing: Easing.inOut(Easing.sin),
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });
  if (p <= 0) return null;
  const {strokeDasharray, strokeDashoffset} = evolvePath(p, s.d);
  return (
    <path d={s.d} fill="none" stroke={color} strokeWidth={w} strokeLinecap="round"
      strokeLinejoin="round" strokeDasharray={strokeDasharray} strokeDashoffset={strokeDashoffset} />
  );
};
```

## Pitfalls

1. Filling a block before the line it illustrates, or after it. Writing should match reading speed and trail the phrase by ~0.5 s. Drawing first makes the viewer wait; drawing late turns the picture into a redundant recap. Complex illustrations are pre-drawn and revealed.
2. Cutting to a blank block every time. Smooth moves shift ~0.23 widths with heavy overlap so the viewer always knows where they are on one big picture; whip only for far jumps; always end on the pull-out to the full view.
3. Many colours, thin or perfectly uniform lines, or a hand that never leaves. Black plus one accent, line ~0.65% of frame height; the hand enters only to draw and exits bottom-right; emphasis words may pop in without it.
4. Mixing big-board camera moves with sheet-type hard cuts.
5. The pen not leading the line (several strokes appearing at once): reveal behind a moving tip.
6. A dead zone after a whip: start drawing the next block as the whip ends, with the tip entering while the camera settles.
7. Writing cut by a frame edge: reframe from the stroke bounding box.
8. The grey end wash plus erase marks reading as a dirty wall: keep the wash very light (#EEEEEC) and smudges faint.
9. A full view held only 0.15 s with blocks that look unrelated: lead from block to block with arrows or connectors, start the pull-out earlier, hold the full view at least 0.5 s (15 f).
10. A cartoon hand: use a real hand cut-out, the marker alone, or nothing.
