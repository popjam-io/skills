# Storytime character comedy (TheOdd1sOut / Jaiden Animations / Domics tradition)

> Adapted from huashu-art-motion (MIT, (c) 2026 alchaincyf) - references/动画语法/y4_storytime.md

The story is the star and the picture is its reaction meme: a simple character snaps between a few poses in ~0.1 s and freezes, and jokes land by cutting to a reaction close-up and going silent for that beat.

Evoke the grammar; never copy the channel's characters, branding or footage.

This grammar needs a character. Use the brand's character or mascot art: one transparent image per pose (rest, talk, point, shrug, type, stiff, react, back; optional `<pose>_open` mouth-open variants), feet at the bottom centre of each image, at least rest or talk. Without character art, do not improvise a code-drawn bean person as the protagonist: the upstream author judged code-drawn little people and robots an instant "AI look" and disabled them. Keep the rhythm instead (snap and hold, screen insert, smash to the punchline, jump-in) with the product, a phone screen, hands or objects as the protagonist, or pick kinetic-type or vox.

## Use it / avoid it

Use it for:
- First-person stories, mishaps, "the first time I...": a script with build-up and a punchline that can breathe.
- When the audience comes for "this person": a recurring avatar recognised by its silhouette (often just its haircut) more than by drawing skill.
- Ads (inferred): relatable-problem skits (problem, failed attempt, the product saves it), customer or founder stories, comedy hooks. One character, 5-6 poses and three mouths can carry a whole piece.

Avoid it for:
- Dense tutorials or data: viewers watch the character waiting for the joke and forget the numbers (use kinetic-type or finance-chart).
- Copy with no "I" (industry news, product comparisons): the character has no stance to perform, only a talking sticker.
- Copy that is not funny and has no pause: the style amplifies the script, it cannot rescue it.

## Before you start

1. Confirm the character assets exist (see above); otherwise switch approach now.
2. Write the shot list as one copy line = one shot. Mark the punchline and the silent reaction beat after it (0.8-1.5 s, 24-45 f).
3. Choose the 2-4 transitions you will use (cut, smash, whip, jump-in, over-the-shoulder) and place every cut in a breath between lines, never mid-sentence.
4. Build each location once as a world canvas larger than the widest framing plus any drift, so wide, medium and close shots are camera crops of the same room.
5. List the words that must be seen in the picture (screen text, key numbers). Everything else lives in captions or speech bubbles.

## Composition

Framing:
- Medium shot (waist up, head 25-35% of frame height) is the default. The character sits off-centre; the other side holds what they are talking about (computer, other person, the product).
- The background only says where: a wall, a desk, a window, 3-5 large colour blocks. A white or flat-colour ground also works.
- Reaction shots remove the environment: the face fills the frame (head radius ~1/3 of frame height) on a flat colour with a vignette.
- Punchlines often go the other way: cut to an extreme wide where the character is tiny; helplessness is the joke.

Palette roles (demo values):
- Skin near-white #FFE2CC (one tradition uses pure white, another warm white).
- Character line #1B1B1F, the darkest value in the frame.
- Wall / desk / floor #DCE9EC / #E2C29B / #E8DCC8: low saturation, high value; the background is always "lighter" than the character.
- Background line #5B6470 at 3 px, lighter and less than half as thick as the character line.
- Reaction void #3D405B with a radial vignette: cool and dark, pushing all attention to the face.
- Mouth / tongue / blush #6E2430 / #F07B7B / rgba(255,140,120,0.35): the only saturated colour inside the mouth, so lip movement reads.
- Brand mapping (inferred): brand colours go on props, the product and the reaction void, not on walls. Logo and product are `<Img>`.

Line weight: character line = head radius x 0.05 (min 4 px): medium R=165 gives 8 px, close-up R=360 gives 12 px, wide R=95 gives 6 px. The character line scales with the camera; the background line stays 3 px. "Character line >= 2x background line" is why the character always pops. With raster character art, check its outline is clearly heavier than the background's.

Character design reference (for briefing art, not for drawing in code): all round and blunt; head a slightly flattened circle (1.0R x 0.93R), bean body (1.0R x 1.2R), total height 3.2R; tube arms with round ends, no elbows or fingers, hands as circles; no right angles except props. Expression lives mostly in the eyebrows (raised = surprise, inner ends up = hurt, flat = deadpan). Mouths: smile arc, flat line, wavy (worry), half open, open. Pupils 0.075R with a highlight; "dead-fish eyes" shrink to 0.035R without highlight.

## Motion

Source measurements (frame differencing on two reference episodes):

| | Snap-and-hold reference (30 fps, 475 s) | Constant-motion reference (24 fps, 902 s) |
|---|---|---|
| Average shot length | 2.43 s (median 1.87, IQR 1.03-3.07) | 5.73 s (median 3.21, IQR 1.67-6.67) |
| Fully still adjacent frames | 70.7% | 51.2% |
| Still segments | median 0.40 s, p75 0.70 s | median 0.08 s (on-twos pause) |
| Motion segments | median 100 ms (3 f) | median 42 ms (1 f) |

Read: the first is snap (0.1 s), hold (0.4-0.7 s), snap; the second keeps moving on twos (12 drawings/s) with longer shots. An animation supervisor who adapted the first channel into a series described it as pose-to-pose, mostly switching between pictures, and named "too soft, too slow" as the main risk (official). The demo took the snaps from the first and breathing and lip-sync from the second.

Parameters (demo):
- Stepping: character motion stepped (24 fps in the source; on a 30 fps timeline snap pose changes to whole frames or step on twos), camera smooth.
- Pose change: 0.10 s (3 f) with `Easing.out(Easing.exp)` on limb targets; with image poses, a hard swap plus the squash below.
- Squash and settle on every pose change: the body squashes 7% vertically and springs back with volume preserved (scaleX = 1/scaleY), 3.5 Hz, decay 9, settled in ~0.35 s: scaleY = 1 - 0.07 * cos(2 pi 3.5 t) * e^(-9t), origin at the feet.
- Lip-sync: three mouths (closed, half, open), changing at most every 1/12 s. With voiceover, drive it from the audio's normalised loudness envelope (closed below 0.06, half below 0.22, open above). Without voiceover, flap on the 1/12 s grid while a speech bubble is "being said" (about its reading time), closed otherwise. Head dips 0.015R per mouth level while talking.
- Breathing: body scaleY +-1.2%, period 1.6 s. Blinks on a fixed schedule every 2.4-3.6 s, closed 83 ms (2-3 f); a deadpan slow blink is one frame longer. Gaze: pupils shift 0.09R toward what the character points at.
- Opening: the camera settles 1.04x to 1.01x in 0.5 s `Easing.out(Easing.exp)` instead of a frozen first frame.
- Sweat drop slides down the temple along the face in 0.9 s. A "?" pops above the head with 30% overshoot in 0.26 s (8 f), `Easing.out(Easing.back(3.4))`, then wobbles +-3 degrees.
- Entrances: almost none. The character is in place, already talking, on the first frame of the cut. Only props and symbols (?, !, sweat, numbers) pop in, with 15-30% overshoot (`Easing.out(Easing.back(2.2))` to `Easing.out(Easing.back(3.4))`).
- Micro-motion is limited to breathing, blinks and small background things, amplitude <= 1-2%. Turning breathing, nods and background loops off moves the piece toward the pure snap-and-hold reference. A high share of still frames is the style here, not a freeze.

## Camera and transitions

Prefer a locked camera; change framing through hard cuts and jump-ins; save the slam for the punchline. (The demo pushed slowly in every shot, e.g. medium +3.5% over 2.0 s; that is the old way.) Ration pushes, not cuts.

1. Hard cut: the large majority, one line one shot. Framing contrast makes jokes (close-up to an extreme wide of the same room).
2. Smash cut to the reaction close-up: the new image is complete on its first frame and springs from 1.22x back to 1 (3 Hz, decay 11), clamped at >= 1 so no edge ever shows; a 55% white flash over the first 2 frames, plus a low hit if the ad has sound. Use it for "after the outrageous line, look at the face".
3. Whip pan toward what the character is looking at: 0.26 s (8 f) `Easing.inOut(Easing.exp)`, with ~16-sample horizontal motion blur in the middle (and a whoosh). Use it for "I open my laptop -> (the screen)".
4. Jump-in: same angle, hard cut to ~2x closer, background unchanged. Use it for "they repeated it", "they realised", the punchline line. It only works if wide and close are crops of the same world canvas.
5. Over-the-shoulder / POV: cut to what the character sees (screen, phone, the other person) with the back of the head in the foreground. The foreground does not follow camera pushes, so it parallaxes against the screen. Give the back view recognisable features and a cool rim light on the screen side; a pure black silhouette read as "another shadow person". Needs a "back" pose image.

Insert shot (an ad workhorse): cut to the phone or computer screen close-up: the user types the problem, the reply scrolls faster and faster, then a big text or number slams out while a counter stops on its value. In ads the screen shows the product's real UI (inferred).

Rhythm and text:
- Shots follow copy lines, not music: one line ~ one shot. The demo's 5 shots averaged 1.75 s (2.0 / 2.4 / 1.2 / 1.65 / 1.5), inside the reference IQR of 1.03-3.07 s, which also suits ads.
- Transitions sit in the breath between lines, and captions change on the same frame as the cut. The demo's first whip landed on a sentence's first two words; the fix: line ends 1.87 s, whip at 2.00 s, lands 2.26 s, next line starts 2.30 s.
- The reaction shot lives in silence: the demo held 1.3 s with no line at all, and that pause is the joke. After the outrageous line, leave 0.8-1.5 s for the face with no new text.
- Hold at least 0.9 s (27 f) after the punchline (a first version left 0.4 s and "the laugh beat was cut off"), then go to the product or CTA (inferred).
- On-screen words only where they must be seen: screen text and key numbers (demo: a big number in a black-weight face at 230 px, #FFCB6B, slammed with ~23% overshoot, `Easing.out(Easing.back(2.85))`). Burned captions: white 50 px with a 10 px black stroke, whole line cut in and out, no animation (animated captions fight the character). In silent ads, bubbles or captions carry the story; keep them static and change them on cuts.
- A number lands on its beat: number slam = hit sound = screen shake (9 Hz, decaying to zero over 0.3 s).

## Build it in Remotion

- One world canvas per location as an SVG/DOM component; each shot is a `<Sequence>` rendering the same `<Room>` under a different camera transform. Size the world bigger than the widest shot plus drift (the demo's first version leaked black edges three times because the world was too small).
- Characters are `<Img>` pose images placed feet at bottom-centre; a sorted pose timeline picks the current pose; the squash runs on time since the last change (snippet). Keys that start a shot get no squash: the character is already in place on the cut.
- Smash: `scale = Math.max(1, 1 + 0.22 * Math.cos(2 * Math.PI * 3 * dt) * Math.exp(-11 * dt))` on the incoming shot, plus a white `<AbsoluteFill>` at opacity 0.55 for the first 2 frames.
- Whip: animate the camera x across the gap and wrap only that window in `<CameraMotionBlur samples={16}>` from @remotion/motion-blur.
- Shake: translateX = A * sin(2 pi 9 t) * max(0, 1 - t / 0.3).
- Speech bubbles: SVG with a tail toward the mouth, popping in with back-out overshoot at the cut.

```tsx
import {Img, useCurrentFrame, useVideoConfig} from 'remotion';

type Key = {at: number; pose: string; squash?: boolean}; // seconds, sorted by at

// Volume-preserving squash on pose change, settles in ~0.35 s.
const settle = (dt: number) => 1 - 0.07 * Math.cos(2 * Math.PI * 3.5 * dt) * Math.exp(-9 * dt);

export const Character: React.FC<{keys: Key[]; poses: Record<string, string>; x: number; y: number; h: number}> =
  ({keys, poses, x, y, h}) => {
    const t = useCurrentFrame() / useVideoConfig().fps;
    const key = [...keys].reverse().find((k) => k.at <= t) ?? keys[0];
    const dt = t - key.at;
    const sy = key.squash !== false && dt >= 0 ? settle(dt) : 1;
    return (
      <Img
        src={poses[key.pose]}
        style={{
          position: 'absolute', left: x, top: y - h, height: h,
          transform: `translateX(-50%) scale(${1 / sy}, ${sy})`,
          transformOrigin: '50% 100%',
        }}
      />
    );
  };
```

## Pitfalls

1. Treating it as full animation with everything moving: soft, no rhythm, exactly "too soft, too slow". Snap in 0.1 s, then really hold.
2. A background as rich as the character: the eye leaves the face and the joke is lost. Background saturation, contrast and line weight one step below the character.
3. No silence for the reaction: going straight to the next line explains the joke away. Hold the face at least 0.8 s, locked, with one or two small details (sweat drop, slow blink, brows dropping); to intensify, jump in ~2x or slam 0.17 s, never a slow push.
4. Black edges: a world canvas too small, a smash spring dipping below 1, or camera drift in a wide shot. Check all four edges in frame previews.
5. Wide and close shots that are not the same room: build one world and crop it.
6. A cut in the middle of a sentence, or a caption that changes later than the cut.
7. Small expression changes (a brow drop, a slow blink) drifting loose from the sound or beat they answer: time each one deliberately to its cue, or it reads as a mistake rather than a reaction.
8. A code-drawn stand-in character: use real character art or drop the character.
9. Adding hand-drawn jitter to the lines: the reference style is uniform vector line; keep it clean.
