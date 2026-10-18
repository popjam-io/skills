# Directing: camera, rhythm and the six ways it goes wrong

> Adapted from huashu-art-motion (MIT, (c) 2026 alchaincyf) - SKILL.md (sections 你是谁, 导演的要求：镜头怎么用, 最常见的六种做坏方式), references/镜头语言.md, references/镜头表模板.md

You are the director, storyboard artist, key artist, animator and editor of the piece at once, and you draw with code. The bar: a viewer understands what every shot is saying and wants to keep watching; when an art style is used, it is recognisable at a glance and the picture is alive, not images being swapped.

Every number below says when it applies and when to ignore it. The numbers come from measured reference films and from pieces the author approved or rejected. They are starting points, not quotas: if you have a better design, use it.

## 1. Plan first: the shot list

Before writing any scene, write a shot list as a comment at the top of the composition. If you cannot fill a row, that shot is not thought through yet; do not code it.

Lock three lines first:

- **Style**: one sentence naming one way of drawing for the whole piece (e.g. "warm paper illustration, flat fills, fine pencil line, one low afternoon side-light"). Changing location is fine; changing style is not.
- **Palette**: a name from `palettes.md` or 3-6 hex values; no blue-purple.
- **People**: none / hands and backs only / supplied footage or photos. Never code-drawn chibi people, white-shell robots, or coins and balls with faces.

Then one row per shot:

| Column | Write | Not |
|---|---|---|
| time | `0-3`, `3-7.5`; each shot starts where the last ends | |
| object (noun) | something you could point at: a slice of bread, a spore, the hero's hand, the bottle | title, bullet, text, label, caption, card, background, icon; an empty frame, flat colour, black |
| what it does (verb) | the object's own action: drifts in, cracks open, burrows, gets cut | appears, is shown, fades in, reveals one by one |
| camera | hold / slow push / pull back / pan / fast push / smash-in / cut (section 2) | a push on every shot; a uniform slow push on every shot |
| on-screen text | <= ~8 words, may be empty | the whole voiceover line; three bullet lines |
| technique | real material full-frame, code-drawn scene, which grammar | a different grammar every shot |

Optional labels column: at most 3 small labels beside the object per shot, never a row of glowing pills.

Five rules; check each before coding:

1. **Open on a concrete small action tied to the topic**: a hand or an object doing something relevant, not a title and not "Introducing...". End on an action of the same hero or object (it goes into a pocket, the lid closes, a pull back shows the whole); text can be written on the object. In an ad the last ~1.5-2 s carries logo and CTA: land them with the product still in frame, not on a dead centred quote card.
2. **One concrete example carried through**: the same loaf, the same hands, the same product from first frame to last; each shot is about something happening to it. Every shot stays in the locked style.
3. **Shots of 2-6 s** (an occasional 8 s). A 15 s ad has 3-6 shots; a 6 s bumper 2-3.
4. **Text-led shots <= 30%**: a shot is text-led when its object is words, its text runs past ~8 words, or it is kinetic type. Neither the first nor the last shot is text-led, unless the brief is explicitly a kinetic-type ad (then the type is the object).
5. **Adjacent shots change composition, not style**: after a full-frame close-up, pan, switch object or change shot size.

Any number on screen must come from the brief or product data; an illustrative chart says so on screen.

Example (method only; do not reuse the subject or the order). 15 s, 1080x1920, a thermos. Style: warm paper-cut illustration, flat fills, fine pencil line, one low morning side-light. Palette: `wood`. People: hands only.

| time | object | what it does | camera | text | technique |
|---|---|---|---|---|---|
| 0-2.5 | a gloved hand and the bottle | thumb flips the lid, steam curls out | hold | | product photo + code steam |
| 2.5-5.5 | the steam | rises past a frosted bus-stop window | pan up | 6:10 am | code scene |
| 5.5-9 | the bottle in a side pocket | backpack sways through falling snow | pull back | | code scene + product cutout |
| 9-11.5 | the open bottle | steam still thick at dusk | fast push (the one accent) | claim from the brief | product photo |
| 11.5-15 | the hand and a cup | pours; pull back to the bottle on a bench, logo and CTA beside it | pull back | CTA | product + logo `<Img>` |

Why it holds up: one bottle and one pair of hands throughout; opens on an action; the push in is answered by a pull back; holds where the steam moves by itself; one accent, spent on the claim.

## 2. Camera: punctuation, not decoration

Before each move, answer three questions:

1. **Where should the viewer look now, and can they read it at this framing?** If yes, do not move. If the picture moves by itself (footage, a line being drawn, a curve growing, water pouring), hold: a camera move fights it. Hold while the viewer reads.
2. **Transition or accent?** Leading the eye, showing a relationship, building mood = transition: slow. Reveal, twist, key number landing, punchline = accent: fast.
3. **What was the previous move?** After a push in, look for a pull back or a pan. The same move three times running and the viewer hears a metronome.

Rules, with the evidence behind them:

- **Readable means still.** Long holds in an explainer are correct, not a freeze.
- **Slow for transitions, fast only for accents.** Slow push leads to the next detail, pan walks between things, pull back shows the whole or closes a section. Fast push, smash-in and whip are for reveals, twists, key numbers and punchlines, countable on one hand per piece.
- **Give and take.** After pushing in, pull back, pan away, or hard-cut to a new shot size; never three push-ins in a row. Evidence: a 102 s vertical explainer (44 shots) had ~48 push-ins, one every 2.1 s, all inward, each 0.28 s for +10-26%; the author: too many zoom-ins, too fast, not smooth at all.
- **Not one beat for the whole piece.** A uniform slow push on every shot drew "it feels like playing a slideshow"; a quick push on every shot drew "too fast, not smooth". Same disease: every shot has the same move. Let the camera follow the emotion: steady while laying things out, faster at turns and the climax. On a music video: camera and transitions monotonous, dry, no variety, no emotion.
- **Not moving is not the cure.** A version with a plain, static background was rejected as giving no reason to watch. Something must always be happening: the object moves, the material itself moves, something new is uncovered, the camera leads the eye. Slow push, pan and pull back are motion; "fast" and "moving" are separate axes.
- **Art-style pictures must stay alive**: per scene one main action plus 2 motif loops, and the camera may drift slowly. Transitions between still paintings were rejected: in the reference each art era lasts ~1 s, yet everything inside the painting flows.

An approved opening mixed a smash-in, a 0.35 s violent pull back into a cutaway panorama and a pan following a paper plane: the mix was the point.

## 3. Move vocabulary

Durations at 30 fps. Measured on 1920x1080 frames: percentages carry over to any canvas; px values are at 1920 wide, scale them with the canvas.

| Move | Use for | Starting numbers | When the number does not apply |
|---|---|---|---|
| Hold | reading; picture moves by itself; silence after a punchline | as long as needed | - |
| Slow push | lead the eye to the next detail; push the mood one step | 0.6-1.5 s (18-45 f), sine in-out; push until the target reads, typically +10-40% | a 2x+ push may take 2 s (60 f); on music, follow the beat |
| Pull back | back to the whole, "where is it", close a section, the ending | 0.8-2 s (24-60 f), fast start, long settling tail | scale journeys (cell to planet) take longer |
| Pan / glide | step from one item to the next on the same wall or table; follow something | 0.5-0.9 s (15-27 f), sine in-out; tracing a line 1.3-1.8 s (39-54 f), long tail | following a moving object: match its speed |
| Fast push | accent: reveal, twist, key number | 0.25-0.35 s (8-10 f), +18-32%, then stop | kinetic type, where it is the main grammar (e.g. 6-frame push + 2-frame pull back) |
| Whip pan | sudden shift of attention ("I open the laptop -> the screen"), comic timing | 0.26-0.30 s (8-9 f), expo in-out, motion blur | - |
| Smash-in | a big word, number, stamp or new image landing | 0.17 s (5 f), scale 1.55 -> 0.94 -> 1.0 | max once per shot; not on every cut |
| Hard cut / jump-in | change shot size without a move: reaction close-up, one size closer | 0 f | - |
| Slow drift | ambience, art-style pictures, lyrical passages, mood shots over 5 s | 1-4% per second | never as the default on every explainer shot: that is the slideshow |

## 4. How often

Accents are bold type: bold everything and nothing stands out.

| Kind of piece | Police it? | How |
|---|---|---|
| Explainer, product demo, data, whiteboard, evidence board | yes | fast push + smash + whip <= 1/3 of shots; no three push-ins in a row; more than ~8 push-ins per minute is too dense. A 15 s ad gets one or two accent moves at most |
| Hook (first ~3 s of a social video) | density is free | may be dense; return to normal pace after |
| Kinetic type, music-cut passages | not the fast-push count | camera follows beats and accents |
| Story, comedy | pushes yes, cuts no | hold + hard-cut jump-ins carry it; few pushes |
| Music video, mood | by emotion | verse slow push or drift, chorus faster, bridge pull back, transition peaks on the beat |
| Art-style tours | not push-ins; police "is the picture alive" | one main action + 2 motif loops per scene; constant slow drift is fine |

Per-grammar baselines:

- **Mechanism (3b1b-style)**: the camera follows the object under discussion: one smooth ~1 s push, still while waiting; fast push only when the conclusion lands.
- **Keynote / UI screenshots**: screenshot full-frame; slow push only to a part unreadable at full view, once or twice per image; then pull back or pan to the next region.
- **Finance / data chart**: hold while the chart grows; ~1 s slow push to a data point; fast push only for the one or two key numbers.
- **Kurzgesagt-style**: the environment layer may move gently all the time; slow push to the named node; dive in and pull out at scale-journey durations.
- **Evidence board (Vox) / whiteboard**: one world canvas; panning between items is the main grammar and may repeat; push in to the line to be read, pull out after.

## 5. Full-frame real material: the commonest trap

With one full-frame photo or clip per shot, the only move left is a push in, and the piece becomes "cut, push, cut, push" (the 102 s explainer above). Instead:

- **Footage that moves: hold.** A push on top of walking people or moving hands reads as shake.
- **One or two pushes per image at most**, and only where a region is unreadable at full view. Pushing on every noun in the copy is a metronome.
- **Vary the entrance**: start close and pull back to reveal; pan in from a side; hard-cut from the last shot's landing point at the same size.
- **Several pieces of material in a row: lay them on one world canvas** (prints on a table) and pan between them; pushes and pans then alternate naturally.
- **A cut does not demand a new push.** Every shot starting at 1.0 and pushing in stacks into one long zoom-in.
- **The board is not shrunken material.** When the camera rests on an item it fills 80-90% of the frame; bare table shows only in transit and in the closing pull back. (In an A/B, the board version cut push-ins from 15 to 8, but photos at rest filled only half the width and too much table showed.)
- **Landscape image on a vertical canvas: crop first.** A whole 16:9 image in 9:16 is a strip with empty bands above and below. Crop to a vertical framing around the part that matters now; keep the whole image for a final pull back. Two independent agents hit this the same day.

## 6. The camera in Remotion

Lay the world out in absolute px inside one wrapper and move only the wrapper. A stop puts world point (x, y) at screen centre at scale z; two equal stops make a hold.

```tsx
import React from 'react';
import {AbsoluteFill, Easing, interpolate, useCurrentFrame, useVideoConfig} from 'remotion';

export const SINE = Easing.bezier(0.37, 0, 0.63, 1); // slow push, pan
export const TAIL = Easing.bezier(0.16, 1, 0.3, 1); // pull back: fast start, long settle
export const SNAP = Easing.bezier(0.5, 0, 0.1, 1); // fast push: quick attack, dead stop
export const WHIP = Easing.bezier(0.87, 0, 0.13, 1); // whip pan
export type Stop = {f: number; x: number; y: number; z: number; ease?: (t: number) => number};

export const Camera: React.FC<{stops: Stop[]; children: React.ReactNode}> = ({stops, children}) => {
  const frame = useCurrentFrame();
  const {width, height} = useVideoConfig();
  let i = 0;
  while (i < stops.length - 2 && frame >= stops[i + 1].f) i++;
  const a = stops[i];
  const b = stops[Math.min(i + 1, stops.length - 1)];
  const t = b.f > a.f ? interpolate(frame, [a.f, b.f], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp', easing: b.ease ?? SINE}) : 0;
  const x = a.x + (b.x - a.x) * t;
  const y = a.y + (b.y - a.y) * t;
  const z = Math.exp(Math.log(a.z) + (Math.log(b.z) - Math.log(a.z)) * t); // log-space zoom
  return (
    <AbsoluteFill style={{transformOrigin: '0 0', transform: `translate(${width / 2}px, ${height / 2}px) scale(${z}) translate(${-x}px, ${-y}px)`}}>
      {children}
    </AbsoluteFill>
  );
};
```

Usage on 1080x1920: `stops={[{f: 0, x: 540, y: 960, z: 1}, {f: 30, x: 540, y: 960, z: 1}, {f: 60, x: 620, y: 880, z: 1.3}, {f: 90, x: 620, y: 880, z: 1.3}, {f: 120, x: 540, y: 960, z: 1, ease: TAIL}]}` = hold 1 s, slow push +30% in 1 s, hold, pull back with a long tail.

- **Zoom in log space** (as above). A linear 1 -> 4 zoom rushes at the start and crawls at the end, because perceived zoom speed is the ratio of change. It matters for journeys of 2x and up; for a +20% push it is harmless.
- **Big scale journeys (beyond ~3x)**: pan to centre the target first, then zoom with x and y fixed (pull-outs: the reverse). Changing position and a large zoom together makes the target swim off-screen mid-move.
- **Smash-in** inside a `<Sequence from={hit}>`: `interpolate(frame, [0, 2, 5], [1.55, 0.94, 1], {extrapolateRight: 'clamp'})` on the landing element.
- **Slow drift**: `z = 1 + 0.02 * (frame / fps)` is 2% per second.
- **Whip**: a sideways stop 8-9 frames later with `WHIP`, wrapped in `<CameraMotionBlur shutterAngle={180} samples={8}>` from `@remotion/motion-blur`, only around the whip (it renders the children once per sample).

## 7. The six ways it goes wrong

Check all six while writing the shot list and again before finishing.

1. **Slideshow / PPT.** Fixed header and page numbers, bullets fading in one by one, the same camera move on every shot (a uniform slow push everywhere, or a quick push everywhere), ending on a centred quote card. Fix: drop the page frame; one visual event per shot; move the camera per section 2, adjacent shots with different moves, push-ins answered; end on an action of the hero or object, text on the object. Thresholds: a piece with near-total absence of in-shot motion has failed (measured: under ~3.5% of frames in fast motion failed, under 6% was a warning; a ~1 s +20% slow push registers about as much motion as a 0.28 s fast push, so do not speed moves up to compensate); a text card as the last shot fails; three push-ins in a row or more than ~8 push-ins per minute is too dense.
2. **Copying the demo.** Compositions, characters or assets from example films, sample code or style samples (including the examples in this skill) end up in the piece. Fix: learn the method only; redesign the composition and objects for this subject.
3. **No concrete object.** Abstract ideas rendered as words and icons. Fix: every shot-list row names a concrete object and its action; a row without one is not ready to build.
4. **Dead background, empty frame.** A large flat or starfield ground that never changes while a small central area moves; or a frame that is all flat colour, black or empty, hero absent. Fix: the subject fills more than half the frame; the background changes with the content; the hero or the product is in every shot; chart grounds share the palette of neighbouring shots. Threshold: no near-blank frame (near-uniform colour, almost no edges) for >= 0.3 s (9 frames) anywhere mid-film.
5. **Drawing in code what real material already shows.** Fix: screenshots, photos, footage and product images go in full-frame (`<Img>`, `<OffthreadVideo>`); code explains, labels and moves the camera. Only segments with truly no material are drawn in code. The brand's logo and product images are always the real files, never redrawn. Evidence: an almost entirely AI-generated tech film drew "it looks bad".
6. **The instant AI look.** Blue-purple gradient grounds, deep-purple starfields, neon cyan-violet glow; a collage that changes style every shot (cartoon person -> dark code screen -> starfield icons -> white bar chart -> web screenshot); code-drawn chibi people and white-shell robots; coins, balls or ions with faces. Fix: lock one style and one palette before planning (`palettes.md`); people only from supplied imagery, otherwise hands, backs and silhouettes. Threshold: blue-purple ground on more than 30% of frames = AI look (rule in `palettes.md`). A clean, unified piece that looks slightly like slides beats a flashy collage.

## 8. Checking with preview frames

- **Stills show composition, not rhythm.** Whether a move is smooth cannot be seen in stills, and you check with `preview_frames`, so compensate: re-read the camera column (count accents, look for three push-ins in a row or the same move three times running; holds and pans exempt), and sample frames every 2-3 frames across each move to confirm the ease and that nothing jumps.
- **One strip per shot**: frames at ~0.5 s and ~2 s into each shot, side by side against the shot list. Any shot that looks lifted from another film gets redrawn in the locked style.
- **Mid-film blanks**: sample around every cut and transition for the 0.3 s blank rule.
