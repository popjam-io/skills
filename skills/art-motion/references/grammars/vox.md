# Collage evidence desk (Vox tradition)

> Adapted from huashu-art-motion (MIT, (c) 2026 alchaincyf) - references/动画语法/y2_vox.md

Lay the argument out on a desk of real material (clippings, photos, documents, screenshots) and move the camera like a reporter's eye across it; lines, circles and highlighter strokes appear in stepped beats, and the credibility comes from "these things were really placed here".

Evoke the grammar; never copy the channel's characters, branding or footage.

## Use it / avoid it

Use it for:
- Real proof the brand actually has: press quotes, review and rating screenshots, documents, real customer or founder photos, maps, dates. "How did this happen", "who said what, when".
- Copy that argues like a journalist: quote, evidence, cause and effect. When the copy says "look at this line" or "note this number", the picture highlights exactly that.
- Any beat where the viewer needs to see the source with their own eyes.

Avoid it for:
- Pure concepts with nothing real to paste: it becomes a fake archive (use kurzgesagt or 3blue1brown).
- Derivations and steps (use whiteboard).
- Heavy character acting: paper cut-outs only move in steps.
- Never fabricate evidence (invented press clippings, reviews, receipts, screenshots). Only paste material the brand supplied or that is verifiably real; without it, pick another grammar.

## Before you start

1. Real material is the main image. Screenshots, quotes and photos fill or nearly fill the frame, and the camera pushes in to the line being read. The desk is the world the camera travels through, not a background for small pictures. Check: more than 2 consecutive shots where the material is under 60% of the frame width is a "picture frame layout".
2. Rotate the reveal moves. List them per beat: already there at the cut, push in, pan to the next item, highlighter sweep, red string, stamp, peel off. Never use the same reveal sequence more than 3 times (one long film slid in 36 of its 37 labels; by the middle the audience could predict every move).
3. Text that must be read goes on the top layer and is drawn last, regardless of which paper it belongs to. Photos, clips and later cards covering words is this grammar's most common recurring bug.
4. Compute camera targets from what must be read now (frame the target plus margin), never hand-typed coordinates; push half-visible neighbour labels out of frame.
5. After every new card on an accumulating desk, read all on-screen words in reading order. Adjacent cards can join into a wrong sentence; remove a card or write the qualifier out in full.
6. Perform each event once. An action shown in the wide view must not replay in the close-up, or it reads as "it happened again".

## Composition

- Three-colour system (measured): near-black #171716; paper white #E0DCDA to #EEEDED; one red in two tones, bright #B65255 for lines and dark #93403C for fills; highlighter yellow #DACF08 (darker and more olive than the channel's logo yellow #FFF200, which rarely appears in large areas). Old map paper #E4DCCF, parchment #CFB195. No pure white, no pure black.
- Demo values: desk #E4DDCF with a static paper texture (fibres plus low-frequency mottling); clue red #B8433F (slightly brighter than measured, for readability); highlighter rgba(218,207,8,0.9) with multiply blending; a large black card #1B1B1A lying on the desk with desk visible around its edges.
- Brand mapping (inferred): the brand's strongest single hue may replace the clue red; keep the rest paper and near-black. Add at most one more accent.
- Materials: archival photos in greyscale 45-degree halftone with a white border and two translucent tape strips; clippings with torn edges, yellowed, serif headlines; labels as black bars with bold white text ("2012 - Google"); ruled index cards. The brand's own product photos and logo stay in faithful colour: no halftone, no torn edges over them.
- Paper texture is static: still segments measure a frame difference of 0.0-0.1. Per-frame grain belongs to a different film-look style, not this one.
- Shadows are weak (barely visible at 360p, measured). Demo: blur 10, offset (3, 6), alpha 0.28.
- Deliberately imperfect: the channel's art director describes a too-perfect look as reading like an ad rather than editorial work (official). For an ad that wants credibility, that is the point.
- People: real photos cut out as stickers with a white edge and a soft shadow.
- Fonts: names and places in small serif, white, under photos; labels in a heavy sans; numbers in a condensed display face. Load them with @remotion/google-fonts (system fonts are not portable).

## Motion

Two frame rates (the core of the grammar, measured):
- The camera moves smoothly (24 fps in the source; render it continuously).
- Elements (map fills growing, red lines drawing, typing, hand-drawn circles, pop-ins) step at 12 fps, "on twos": 52% of motion frames in one film show the move-stop-move fingerprint. Quantize element time to 1/12 s counted from the element's own start (snippet below).

Camera easing (13 measured moves): median 1.29 s (range 0.71-1.96 s), none linear.
- 7 symmetric `Easing.inOut(Easing.sin)`: long "find the next card" moves.
- 6 fast-start, long-tail, close to `Easing.bezier(0.33, 0, 0.2, 1)`: pull-out reveals and following a line.
- Defaults: push 0.6-1.5 s (18-45 f), pull-out ~1 s (30 f), follow a line 1.3-1.8 s (39-54 f). Demo: after the highlighter finishes, push to that line in 1.5 s sine (1.14x to 1.28x); pull-out 0.85 s long-tail.

Entrances (measured):
- Archive photos and clippings are simply there at the cut: no pop, no drop.
- Only when tracking along a timeline does the next card slide in from off-screen, tilted 5-15 degrees, settling flat in ~0.8 s. Demo: 0.55 s `Easing.out(Easing.poly(4))` from 12 degrees to flat, stepped at 12 fps, starting fully off-screen so the first step is still outside the frame.

Lines and pens (measured): red underline 0.5-1 s; red ellipse ~1 s in one stroke, ends open and slightly crossing; highlighter 1.5-3 s per line, sweeping along the words as they are read; typing ~13 characters/s on twos. Demo: circle 0.65 s, highlighter 0.9 s, each red string 0.5 s with 0.15 s stagger, a counter rolling to 10,000,000 in 1.4 s `Easing.out(Easing.cubic)`.

Holds: when the desk stops, it stops (frame difference 0.0-0.1). While a card animates internally (line, highlighter, typing) the camera stays still. When a static image holds long, push in on the part being read at that moment (find the card 0.5-0.9 s, push 1.0-1.5 s, ease in-out; a 0.28 s snap push only for the reveal), or pan to the next item. Never a constant slow drift.

## Camera and transitions

1. Hard cut: the vast majority, cut on punctuation (between copy lines).
2. Pan along the red string (timeline tracking): 1.3-1.8 s long-tail; the next card slides in from the side, tilted, and settles. Demo: a string runs from the highlighted clipping line to a counter label on the wall; the camera follows in 1.1 s with a short directional motion blur (7 samples).
3. Push into a paper or photo, then hard cut to a high-resolution scan of the same image: 1.0-1.4 s, S-curve. Demo: log-zoom into a small wall photo to ~9.6x in 0.6 s sine, hard cut to the large scan (coarser halftone reads as "a clearer copy"). Match the photo's on-screen width on both sides of the cut and repeat the tape at the same spots.
4. Pull out from a single photo to reveal the whole collage: ~1.0 s, fast start, long tail.
5. Map fills growing, routes drawing: 2.5-3.5 s on twos, a solid red dot at the line's head.
6. Hand page flip or paper pull: approximate as paper sliding in along an arc with a changing shadow.

Not this grammar: torn-paper transitions (zero occurrences in 5 sampled films; a template-site cliche), every image popping or dropping in, jittering grain.

Camera discipline: the desk is one world, so pans between items are the main syntax and may repeat; push in only for the line to read, then pull out. When the camera stops on an item it fills 80-90% of the frame; wide desk views belong only to moves and the closing pull-out.

Rhythm (measured, collage segments):
- Slow tempo: median 3.3 s per shot, ~12 cuts/min, a card holds 3-7 s carried by drawing and highlighting inside it.
- Fast tempo: 1.4-1.8 s per shot, 25-33 cuts/min, images nearly static, rhythm from the cuts.
- For ads (inferred): fast tempo by default; slow tempo for the one proof shot that must be read.

Sync: highlighter, typing and line speed lock to the words being read, not to music beats. One documentary maker scripts in two columns so every word has a matching movement (official). The closing black label works as a point-the-title end card, not an opener.

## Build it in Remotion

- One desk world, one camera: every item is placed in world coordinates on a large desk inside one transformed wrapper. Shots that share the desk use a camera pan as the transition; a hard cut goes to a new `<Sequence>`.
- Camera targets from bounding boxes: z = min(W / (w * (1 + m)), H / (h * (1 + m))) for item size (w, h) and margin m, centred on the item. Limit the push so the red circle (1.24x the box width, 1.5x its height) stays in frame.
- Text layer: render all readable text in a separate world-space layer above every paper.
- Red string with sag: `M x1 y1 Q mx (max(y1, y2) + sag) x2 y2`, drawn with `evolvePath`, a dot at the head via `getPointAtLength`.
- Hand-drawn circle: ellipse points with a small `noise2D` wobble (fixed seed), start and end overlapping by 10-20 degrees, drawn with `evolvePath` on twos.
- Highlighter: a rect with ragged ends, `mixBlendMode: 'multiply'`, width interpolated across the line, stepped at 12 fps.
- Halftone (archival photos only): `filter: grayscale(1) contrast(1.15)` plus an overlay of a dot pattern (`radial-gradient` background, ~6 px cell, rotated 45 degrees) with multiply blending.
- Torn edge: a `clipPath` polygon with jagged points from `random(seed)`. Paper texture: a static SVG `feTurbulence` with a fixed seed, never frame-dependent.
- Sticker edge on a transparent cut-out `<Img>`: chain `drop-shadow(6px 0 0 #fff) drop-shadow(-6px 0 0 #fff) drop-shadow(0 6px 0 #fff) drop-shadow(0 -6px 0 #fff)` then a soft shadow.
- Motion blur only on the string-follow pan: wrap just that `<Sequence>` in `<CameraMotionBlur samples={7}>` from @remotion/motion-blur (render cost multiplies by the sample count).

```tsx
import {evolvePath, getLength, getPointAtLength} from '@remotion/paths';
import {Easing, interpolate, useCurrentFrame, useVideoConfig} from 'remotion';

// Elements step at 12 fps "on twos", counted from the element's own start.
const useSteppedSeconds = (startSec: number, stepFps = 12) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const local = Math.max(0, frame / fps - startSec);
  return Math.floor(local * stepFps) / stepFps;
};

export const RedString: React.FC<{d: string; start: number; dur: number}> = ({d, start, dur}) => {
  const t = useSteppedSeconds(start);
  const p = interpolate(t, [0, dur], [0, 1], {
    easing: Easing.bezier(0.33, 0, 0.2, 1),
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });
  if (p <= 0) return null;
  const {strokeDasharray, strokeDashoffset} = evolvePath(p, d);
  const head = getPointAtLength(d, getLength(d) * p);
  return (
    <g>
      <path d={d} fill="none" stroke="#B65255" strokeWidth={5} strokeLinecap="round"
        strokeDasharray={strokeDasharray} strokeDashoffset={strokeDashoffset} />
      {head ? <circle cx={head.x} cy={head.y} r={9} fill="#B65255" /> : null}
    </g>
  );
};
```

## Pitfalls

1. Everything moving smoothly at full frame rate looks like a corporate promo; everything stepped makes the camera nauseating. Camera smooth, elements on twos.
2. Template moves posing as this grammar: torn paper, every image bouncing in, flickering grain. The more decorative the entrances, the less editorial it reads.
3. Logo-yellow as a large fill, or too many colours. Black, paper white, one red, plus at most one accent.
4. A highlight box that starts off-screen: viewers saw it 7 frames late. Move the camera first so it arrives one frame before the reveal.
5. The camera leaving a text card before the typing finished: leave only after typing ends plus a 0.5 s (15 f) hold, at the latest 0.4 s before the next item; if the gap is short, speed typing up to 40 characters/s.
6. A dead opening: put the first event within 0.3 s (9 f) (the item already there at the cut, highlighter or string starting immediately) or open with a 0.17 s slam. An opening slow push is not the fix.
7. The highlighter not finished when the ad ends: finish it, then hold at least 0.3 s.
8. Vertical frames: highlight the half-sentence being read, not the whole paragraph. A screenshot ~900 px wide on a vertical desk needs a 2-2.5x push for 16 px web body text to read; a box spanning nearly the full width leaves no room for the circle and blocks the push, so split it into two highlights, one keyword each (measured: 2.4x push, ~50 px text height).
9. Estimated highlight rectangles are often 20-30% off: verify on a frame preview before trusting them.
10. A cut-in sticker appearing half in frame on its first frame: start it fully off-screen so the first stepped position is outside.
11. A hard cut that switches from the desk to a pure black screen breaks the world: lay a large black card on the same desk with the desk visible around it.
