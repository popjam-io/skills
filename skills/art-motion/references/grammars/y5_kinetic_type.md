# Kinetic Typography (Saul Bass title sequences, lyric kinetic-type videos)

> Adapted from huashu-art-motion (MIT, (c) 2026 alchaincyf) - references/动画语法/y5_kinetic_type.md

Words are the actors: each key word slams in on an accent, the main word is big enough to read in one glance, supporting lines rise out of a slot, there is only ever one focus, and the camera and background keep moving while landed type stays still.

Evoke the grammar; never copy the channel's characters, branding or footage.

Lineage: Saul Bass's North by Northwest titles (1959) are usually cited as the first large-scale kinetic type in a feature; post-2008 After Effects lyric videos made it the standard for openers, lists, quotes and number reveals.

## Use it / avoid it

Use it for:
- Openers and chapter cards for lists ("3 reasons", "4 steps"): the information is structure (how many, which one, from what to what), not imagery.
- Quotes, slogans, one-line conclusions: reading them sticks better than hearing them.
- Number reveals: one number per shot, the number is the hero.
- Copy with a clear stressed word ("not more code - *intent*").
- Ads: hooks, offer and price reveals, benefit lists, the claim before the CTA. This is the most ad-ready grammar in the set.

Avoid it for:
- Stories and emotional arcs: no faces, little empathy.
- Long explanations as full-screen text: viewers read, stop listening, and still can't keep up. More than 30-60 s of pure kinetic type is tiring; use it for the opener, chapter cards and the conclusion.
- Lists of more than 5 items: use a static infographic instead.

## Before you start

1. Confirm type should be the hero (lists, slogans, numbers, chapter cards). If the whole piece would be type, switch grammar or put a visual page (product image, screenshot, chat bubble, UI card) after every 2 type pages.
2. Count words. Main word: 1-2 words, ideally <= 10 characters. Sub-line: <= ~6 words / ~35 characters. (Upstream limits are <= 4 and <= 14 CJK characters; the English figures are adapted.) Only one thing enters at a time. Too long: split onto another page; never shrink type to cram it in.
3. Same page layout at most 3 times in a row. "Big word + sub-line + top-left label" four times is a slideshow; break it with a number slam, an evidence object, or a dive into a colour block.
4. Write every landing as a beat number (or a word in the music/VO). A landing that is neither on the grid nor on a word gets deleted or moved onto one.
5. Landed type does not move. Energy comes from beat pulses, page changes and evidence objects; the main word never floats or "breathes".

## Composition

- **Layout:** one main word per screen, left-aligned in the left 1/3-1/2 (or mirrored right); sub-line tight below it; an "evidence object" on the other side (product shot, screenshot, chat bubble, checklist, card). Small label in a top corner ("STEP 01") and a progress rail. Margins >= 130 px at 1080 px short side (~12%), and everything inside the platform safe zone. Vertical 1080x1920: stack the main word above the evidence object.
- **Type ladder (demo, 1080p):** main 340 px Black (900) : sub 96 px Heavy (800) : label 40 px Bold (700), tracking +6 px = 3.4 : 1 : 0.4. As a share of the short side: ~31% / ~9% / ~3.7%. Main:sub at least 3:1. The main word must read in 0.3 s - hence 1-2 words.
- **Fit to width** (no text measuring available): size = min(ladder size, boxWidth / (chars x avgAdvance)), with avgAdvance ~0.72 em for heavy grotesk caps (Inter 900, Archivo Black), ~0.6 em mixed case, ~0.45-0.5 em condensed caps (Anton, Oswald), ~0.4 em Bebas Neue (heuristic: leave 10% slack, check the frame preview). For long words in vertical, prefer a condensed display face over shrinking.
- **Colour:** one full-screen background per chapter; a new chapter = a new background (colour is the chapter number). Demo palette:

  | Page | Background | Main word | Accent |
  |---|---|---|---|
  | Title | yellow `#FFD23F` | ink `#111111` | white numeral in a coral `#FF5A36` circle |
  | 01 | coral `#FF5A36` | white | yellow marker `#FFD23F` |
  | 02 | navy `#14213D` | yellow | yellow marker, blue bubble `#3A86FF` |
  | 03 | off-white `#F4EFE6` | ink | coral underline, green tick `#2BB673` |

  4 backgrounds + ink + white; only one accent at a time. Brand mapping: rotate 2-4 brand colours as page backgrounds, ink or white type with >= 4.5:1 contrast, one accent for marker, underline and numbers.
- **Shapes:** type is the biggest shape. Support shapes only: rounded rects (card r 26, bubble r 30, keycap r 22), circles (number badges), skewed colour blocks (marker, slope 0.18 = `skewX(-10deg)`). Background dot grid: 64 px spacing, 6-10% opacity. No outlined or drop-shadowed type; the only shadow is an offset shadow under cards at 8-18% opacity.
- **Fonts:** the brand font if it has heavy weights; otherwise Inter 900/800/700, Archivo Black or Anton via `@remotion/google-fonts`. Code cards in a loaded mono (`JetBrainsMono`, `RobotoMono`), never a system font such as Menlo.

## Motion

Easing in Remotion:
- expoOut `Easing.out(Easing.exp)`, expoIn `Easing.in(Easing.exp)`, expoInOut `Easing.inOut(Easing.exp)`.
- backOut `Easing.out(Easing.back(s))`: s 2.3-2.6 gives 17-20% overshoot.
- Damped spring in seconds: `springHz(t, freq, decay) = 1 - exp(-decay*t) * cos(2*pi*freq*t)` (Dan Ebberts' inertial bounce, default freq 3 / decay 5).

Entrances, chosen by importance:

| Element | Move | Curve and timing |
|---|---|---|
| Main word | **Slam:** scale 1.7 -> 1, opacity 0 -> 1 in the first 0.06 s (2 f) | `springHz(t, 2.2, 10)`: dips ~8-9% below 1, settled in ~0.35-0.4 s (11-12 f) |
| First word of a title | Slam + rotate -8deg -> 0 | same |
| Sub-line, label | **Rise from a slot:** clipped below the baseline, translateY +1.2 line heights -> 0 | expoOut 0.30-0.35 s (9-11 f) |
| Number, icon, bubble, keycap | **Pop:** scale 0 -> 1 | backOut, 17-20% overshoot, 0.30-0.42 s (9-13 f) |
| Card | **Slide** from +700 px (side) or +260 px (below), rotation 3.4deg -> 0 | expoOut 0.40 s (12 f) |
| Typing | Truncate by character | 26 chars/s (13 chars in 0.5 s); cursor blinks at 2 Hz |
| Instant UI (autocomplete, notification) | Appears in 0 frames, because it is instant in reality; a keycap press squashes 14% and rebounds with `e^(-18t)` | - |
| Marker / underline | Brushes left -> right | expoOut 0.30 s (9 f), 1-3 eighth notes after the word lands |
| Key-word emphasis | Scale to 1.35x on the emphasis beat and pin; the marker scales with it | `springHz(t, 2.5, 9)`, on the same beat as its paired action (tap, tick) |
| Giant chapter number | 900 px, 5-13% opacity, bottom-right; lands 1.35 -> 1, then drifts diagonally 14/10 px/s | `springHz(t, 2, 8)` |
| Check mark | Stroke drawn by arc length; box 1 -> 1.25 -> 1 | 0.22 s (7 f); strike-through 0.08 s (2-3 f) later |

**Exits** are faster than entrances and accelerate: expoIn 0.18 s (5-6 f), stagger 0.03 s (1 f), scale to 0.6, drop 60 px, fade. Attention has left before the exit starts. On a page's last beat, everything exits except the one shape the camera will dive into.

**Stagger:** words in a line one eighth note apart (0.25 s at 120 BPM, 7-8 f); groups of small items (three ticks) the same.

**Ambient motion** (type is still; these move):
- Camera drift: two sines, amplitude 5 px, periods ~7 s and ~2.7 s; rotation within +-0.5deg.
- Beat pulse: on every quarter beat the whole frame scales up 1.2% and decays with `e^(-25t)` (~0.12 s, 4 f), so the picture "breathes" with the kick.
- Dot grid pans diagonally at 36 px/s.
- Last beat: camera pulls back 6% (expoOut 0.5 s, 15 f) = "closing".

**Density (measured):** two lyric kinetic-type videos had only 10.3% and 21.2% fully static adjacent frames (a storytime-style cartoon: 71%). Big visual events came every 0.66 / 0.83 s, about one per beat (105 / 99 BPM). The demo used one per eighth note (0.25 s): fine for an opener or a 3 s ad hook; longer pieces drop to one per beat.

**Practitioner frame counts (School of Motion):** small words slide in over 4 frames; a main word is thrown in over 6 frames plus a 2-frame overshoot back; camera push 6 frames plus a 2-frame pull-back. The camera moves slightly late, "as if pushed by the sound". Falls accelerate (no ease-out), and on impact the whole comp scales up and returns to 100%.

### Beat grid and holds

- **Pick a pulse even without music.** Use the music bed's BPM if there is one; otherwise choose one. 120 BPM = 15 f per beat at 30 fps; eighths are 7.5 f, so compute `Math.round(n * 7.5)` from the page start instead of adding 7 or 8 (no drift).
- **Demo structure (demo):** 120 BPM, 4 bars + 1 beat (8.5 s), one shot per bar. Inside each shot: beat 1 main-word slam (+ giant number), beat 1.5 evidence object, beat 2 sub-line, beat 3 evidence action, beat 3.5 key-word emphasis + marker, beat 4 breath or exit. Beat 16 (8.0 s) is the closing hit, then a 0.5 s hold. Every shot reuses the same beat slots and only swaps side and content; from the second shot on, viewers know where the next hit lands. That predictability is the rhythm.
- Main words land on the downbeat (beat 1 of the bar); small elements land on eighth notes.
- **Reading time:** >= 13 characters per second for English on-screen text (SSW guideline). The main word (1-2 words) holds >= 0.5 s (15 f) after settling; a sub-line holds >= chars / 13 s and never under 1.0 s (30 f). If it doesn't fit, cut words; don't speed up.
- **Sync with VO or lyrics:** main word = stressed word. Picture may lead by at most 1 frame and never lag (EBU R37: sound may lead by <= 40 ms or lag by <= 60 ms; late picture is noticed more).
- **Ads:** the first 3 s hook may be denser than the grid; afterwards return to it. End on a still frame: hold the final claim or CTA (upstream: >= 0.5 s after the closing hit; a CTA usually wants longer).

## Camera and transitions

Camera baseline: in kinetic type the quick push (punch) is a main move and follows beats and accents, with no cap on the count (the usual "accents in <= 1/3 of shots" rule does not apply). Landed type never moves relative to its page.

Transitions:
1. **Fill zoom (dive into a shape):** the camera dives into a shape on the outgoing page (the coral circle behind "3"); its colour is the next page's background. First 55% of the duration: expoIn zoom up to 30x around the shape's centre. Last 45%: the new page settles from 1.25 -> 1 with expoOut. Demo 0.45 s (13-14 f).
2. **Bands:** three skewed colour bands (demo: yellow -> white -> navy) sweep left -> right in relay, staggered 12%; the last band is the new background colour and reveals the new page behind it. 0.5 s (15 f), expoInOut.
3. **Push:** old and new slide together like one long canvas. 0.35 s (10-11 f), expoInOut: `slide({direction: "from-right"})` with `linearTiming({durationInFrames: 11, easing: Easing.inOut(Easing.exp)})`.
4. **Mask wipe:** a shape (circle, bar, the letters themselves) grows as a mask over the new page: `iris()` / `wipe()` from `@remotion/transitions`, or an animated `clipPath`.
5. **Type as transition:** a letter from the old page scales up into the full-screen colour block, or a word flung off-screen drags the old page with it.

**Reveal on the beat (the most valuable trick):** a transition's first frame is not the accent; the frame where the new page appears is. Start the transition at `beat - revealPoint x duration`. Reveal points: fill zoom p = 0.55 (0.45 s, so it starts ~0.25 s before the beat); bands p ~0.6 (0.5 s, starts 0.30 s before); push with expoInOut reads as "arrived" at 90% displacement, p ~0.58, not p = 1 (the demo's first pass used p = 1 and landed 8 frames at 60 fps early). In a `TransitionSeries` the incoming scene's frame 0 is the transition start, so shift its internal beat map by the same offset.

## Build it in Remotion

Layers, bottom to top:
1. **Page background:** solid chapter colour, oversized ~6% beyond the frame so drift, pulse and pull-back never expose an edge (the reviewed demo had 0 frames showing black at any edge).
2. **Dot grid:** a `radial-gradient` background, `backgroundSize: "64px 64px"`, `backgroundPosition` driven by the frame.
3. **Giant chapter number.**
4. **Camera wrapper** `<AbsoluteFill style={{transform}}>`: drift + beat pulse + closing pull-back.
5. **Page content:** main word, sub-line, label, evidence object. Product photos, screenshots and the logo go in via `<Img>`; never redraw them.
6. **Persistent overlay outside the camera and the transitions:** progress rail, logo. Drive it from the global frame only. In the demo's first pass the rail lived inside each page and jumped with the push; change its colour on the reveal frame.

```tsx
import { AbsoluteFill, Easing, interpolate, useCurrentFrame, useVideoConfig } from "remotion";

const BEAT = 15; // 120 BPM at 30 fps
const b = (n: number) => Math.round(n * BEAT); // beat index (0, 0.5, 1...) -> frame
const clamp = { extrapolateLeft: "clamp", extrapolateRight: "clamp" } as const;
const springHz = (t: number, freq: number, decay: number) =>
  t <= 0 ? 0 : 1 - Math.exp(-decay * t) * Math.cos(2 * Math.PI * freq * t);

export const Page = ({ word, sub }: { word: string; sub: string }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const t = frame / fps;
  const slam = interpolate(springHz((frame - b(0)) / fps, 2.2, 10), [0, 1], [1.7, 1]);
  const shown = interpolate(frame - b(0), [0, 2], [0, 1], clamp);
  const rise = interpolate(frame, [b(1), b(1) + 10], [120, 0], { ...clamp, easing: Easing.out(Easing.exp) });
  const pulse = 1 + 0.012 * Math.exp(-25 * ((frame % BEAT) / fps)); // quarter-beat breath
  const dx = 5 * Math.sin((2 * Math.PI * t) / 7);
  const dy = 5 * Math.sin((2 * Math.PI * t) / 2.7);
  return (
    <AbsoluteFill style={{ transform: `translate(${dx}px, ${dy}px) scale(${pulse})`, padding: 130 }}>
      <div style={{ fontSize: 340, fontWeight: 900, whiteSpace: "nowrap", opacity: shown,
        transform: `scale(${slam})`, transformOrigin: "0% 85%" }}>{word}</div>
      <div style={{ overflow: "hidden" }}>
        <div style={{ fontSize: 96, fontWeight: 800, transform: `translateY(${rise}%)` }}>{sub}</div>
      </div>
    </AbsoluteFill>
  );
};
```

- **Marker:** a skewed block behind the word, `scaleX` from 0 with `transformOrigin: "left"`. Never the same colour as the text: on the navy page with yellow type, a yellow marker erased the main word. Pick another accent, or render the covered letters in the page colour.
- **Fill zoom:** scale the outgoing page around the shape centre with log-space zoom, `z = Math.pow(30, expoIn(p / 0.55))`; at p = 0.55 the shape's colour fills the frame; then render the new page at `scale(interpolate(p, [0.55, 1], [1.25, 1]))` with expoOut.
- **Bands:** three skewed full-height rectangles translating across, offset 12% of the duration each; clip the new page to the area behind the last band's trailing edge.
- **Check mark:** `evolvePath(p, d)` from `@remotion/paths` gives `strokeDasharray`/`strokeDashoffset`.
- **Main word:** `whiteSpace: "nowrap"` plus the fit-to-width heuristic, so a long word never wraps unexpectedly.

## Pitfalls

1. **All words the same size, moving together.** No hierarchy means no focus. Main:sub >= 3:1, one element entering at a time, everything else still.
2. **Type keeps floating.** Text being read must not move. Ambient motion belongs to the camera drift, beat pulse and dot grid; the slam pins after ~0.35 s.
3. **Animation off the beat, or the accent on a transition's first frame.** Align the reveal frame and write every landing as a beat number. Each off-grid landing loosens the whole piece.
4. **Sub-line held too short** (0.6-0.9 s in the demo review). Bring it in a beat earlier and cut it to fewer words, for 1.0-1.5 s of readable time.
5. **Collisions.** A sub-line came within 14 px of an evidence panel. Shorten it, right-align it, keep > 180 px between them.
6. **Not kinetic enough.** Tiny step numbers and highlights without scale read as slides. Add the giant background number and the 1.35x key-word emphasis.
7. **No ending.** Add a closing hit on the last downbeat (camera pulls back 6% plus a 3.5% punch). Completed items turn green, not grey, and the layout doesn't leave dead space at the bottom.
8. **Overflow in vertical.** Long words and numbers ran off-frame in upstream tests. Everything that can overflow needs a fallback: shrink, then wrap, then make room. Check a frame with the longest real copy.
