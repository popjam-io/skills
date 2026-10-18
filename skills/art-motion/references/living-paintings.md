# Living paintings: make the painting move

> Adapted from huashu-art-motion (MIT, (c) 2026 alchaincyf) - references/02-机制.md, references/05-节奏与配乐.md, references/07-正面经验.md, references/11-长卷穿越片.md

A styled ad is not a run of still images with transitions between them. Every shot is a painting that stays alive the whole time it is on screen; cutting between stills is a slideshow, however good the stills are. How to paint the frame itself: `painting-in-code.md`.

Durations are given in seconds and in frames at 30 fps. Pixel values are at 1920 wide; scale them with your canvas.

## 1. One shot = one main action + motif loops

- **Main action:** one continuous action by the hero (a hand lifts the cup, the bottle turns to camera, the sneaker lands). Eased, on continuous time.
- **Motif loops:** about two (up to four) small loops taken from the style's own visual vocabulary, not generic sparkles. Upstream examples: cave-painting animals running by alternating two poses (the multi-leg drawing convention, animated); a scarab rolling a sun disc; a meander border scrolling; a volcano smoking; gold leaf glinting; a night sky swirling; geometric clock hands ticking; a pop four-panel grid swapping colours.
- **Picking motifs:** list the style's three most recognisable formal elements (a material, a mark, a motif, a medium glitch) and give each a way to move.
- **Motion goes where the eye goes:** on the hero, the product, the layout's focal point. Motion in a corner nobody looks at is wasted.
- **Short holds need faster motion:** holds of 0.25-1.4 s (8-42 frames) still showed visible action upstream. Under 0.5 s (15 frames), step the motion at 15-30 fps so it reads within the window.

Evidence: a motion heatmap of the reference film showed 2.5-34% of each segment's area moving, even in holds under a second; before measuring, the author had assumed each segment was a still. Code segments built this way measured 1.6-14% moving, with no jumps. The first code pass measured 2.8-9.9% where the reference had 6.2-17.3%: first passes come out too still, so add motifs.

Scope: this governs art-style frames, where the painting must stay alive. In text-led, explainer or UI shots, motion belongs to events and stillness is fine (section 6).

Check with `preview_frames`: request frames about 0.45 s (14 frames) apart inside a hold, and not within ~0.35 s (11 frames) after a cut, where the beat punch moves everything. If only the hero changed, add motif loops. Sample several frames through a shot, not only its first and last: one upstream shot changed 33% start-to-end yet sat still on 14 of 48 frame pairs.

## 2. Motion craft for painted frames

- **Drift the field, don't reshuffle the strokes.** Keep stroke positions fixed and let the direction field change continuously (`noise3D(seed, x / k, y / k, frame / 120)`) so strokes sway like flames. Evidence: reseeding every stroke at 8 fps gave a frame difference of 18-20, bigger than a transition, and read as "the painting flickers"; fixed positions with a drifting field gave 0 jumps and 9% moving area.
- **Boil is for line art only.** Hand-drawn outlines may reseed every 3-4 frames (10 / 7.5 fps) for a hand-made shiver. Full-frame fills and strokes never boil.
- **Stepped time is a style.** 10-12 fps steps for rubber-hose cartoons, shadow puppets, stop-motion and cut paper (`Math.floor(frame / 3) * 3`) are half the look, not lag. Keep the camera and the product's main action smooth unless the whole piece is stepped.
- **Scroll a pattern by its true period.** Wrap with `% period`, where period is the pattern's real repeat (a hex polka-dot grid repeats every two rows, not every row). Evidence: wrapping by dot spacing made the whole dress jump on the wrap frame, at 2.7x the normal frame difference.
- **The camera is a function of global time; transitions only composite.** Paint a world larger than the frame and move a viewport over it; never zoom a rendered bitmap. A push transition keeps the outgoing shot's own camera pushing. To fly through a round object, scale to at least 1100 / radius (px at 1920 wide) or the last frame jumps. Evidence: a 60x zoom journey stayed sharp because it was redrawn in vector at every scale; transitions that were pure camera moves had 0 jumps.
- **Moving regions share their surroundings' parameters** (stroke density, tile size); different parameters show as a patch the moment the motion stops.

## 3. Style swap: same scene, the style changes

The mechanism behind "art-history speedrun" films: one scene repainted through a run of styles. The upstream example is a room with a window, a cat and a girl holding a cup, carried through 16 eras of art history; it illustrates the mechanism only, so don't reuse its layout. Use style swap when the idea is change against a constant: one product through many worlds, a city over 100 years, a person from 18 to 80, a brand's look through the decades. Don't use it for explainers, stories or single-style pieces; design those compositions from the topic.

### The five layers

1. **A fixed scene skeleton.** Element positions barely move between styles (within +-40 px). The eye has anchors, so it can see that the style changed. Write the skeleton once as a `LAYOUT` constant that every style scene reads. Fixed positions also let transitions start from an object in the frame: tiles spreading from the product, a light ring opening from the cup.
2. **Each style is a living painting** (section 1), held 0.25-1.4 s.
3. **The transition is the next style's signature** (below), with a beat punch.
4. **Acceleration on a beat grid** (section 4).
5. **One continuous anchor and a payoff** (below).

For an ad, the product stays put and the world changes: the product is a real `<Img>` at a fixed `LAYOUT` position with a light per-style treatment (`painting-in-code.md` section 9), the world is repainted behind and around it, transitions grow from it, and the last segment lands on the brand's own look with the CTA.

Speedrun-type pieces get "the same subject travelling through styles" for free from one skeleton, one choreography and N renderers: renderers change only how things are drawn, never where they are or how they move. Evidence: one shared figure rig served 36 styles, and two independent builders both noted that position and motion matched across every style change automatically. In any other kind of piece, compose from the topic; the style may even dictate the composition.

### Signature transitions

Build each transition from the incoming style's most recognisable element (material, mark, motif, medium glitch) that can grow "from nothing to full", and grow it out of an object in the frame. Upstream set: stone blocks or a tapestry dropping in; a frieze rolling round like a turning vase; mosaic tiles flipping; a parchment page turning; rays of light; a great wave sweeping across; dabs filling the frame; a sky vortex swirling in; gold-edged organic growth; geometric shards; primary-colour shapes rotating and scaling up; lightning plus halftone; pixelation; wireframe, then a scanline render; concentric colour rings. Derived later from the same rule: a gold-leaf spiral unrolling, colour bands pressing down, ribbons peeling the old painting away, polka dots growing, melting drips, hard-edged sunlight, a wet-paper bleed, a VHS tear.

Evidence: two independent builders called this the most valuable and most transferable rule in the whole method; nine new transitions followed from it directly. Why it works: one move says goodbye to the old style and announces the new one; viewers know who is next within 0.3 s. Never pick a generic transition from a library.

- **Beat punch:** on the first frame of each transition, scale the scene layer to 1.03 and ease back to 1.0 over ~0.33 s (10 frames). Counters, labels and the CTA don't scale. Punch both the outgoing and the incoming layer. Evidence: punching only the incoming layer (not yet visible on the beat frame) left 6 of 15 transitions 0.1-0.17 s late; punching both put every first visible change on the beat, within 2 frames at 60 fps. Any cut on a beat needs a full-frame visible change on that frame.
- **Time by the visible part:** in-out easing hides both ends, so a complex 0.34 s transition reads as about 0.2 s and looks like a plain wipe. Simple shapes: 0.4 s (12 frames). Complex signatures (gold leaf, colour bands, ribbons): 0.48-0.5 s (15 frames).
- **Melt:** the new image flows down in round-headed drips (drip profile `(1 - u * u) ** 0.3`). Dragging the old image down gives spikes, not drips.
- **Opening without a transition:** let the first painting paint itself (strokes write on, print plates land one by one, pixels light up row by row). Evidence: an ink-wash opening writing its strokes over 0.45 s while the ink bled in was approved; frame 0 is no longer blank paper.

### Anchor and payoff

- One element runs continuously through every segment, driven only by global time. Upstream it was a year counter: during a transition both layers show the same rolling number, each in its own era's lettering, and the label hard-cuts at the transition midpoint so the two never overlap. A counter showing years must run chronologically; otherwise use an index or the style's name.
- The hero's main action is continuous on global time too. Evidence: when each segment replayed the action on local time, viewers saw "she raised the cup five times" instead of "one moment, five styles", and two heads showed through a transition; on global time, poses matched across every cut. Only a segment-specific performance uses local time.
- Give the payoff room (the last segment runs long, 9 or more eighths) and perform it fully: anticipation, squash and stretch, follow-through, secondary action. Squash and stretch pivot on the base (feet, bottle bottom); flip facing at the most squashed frame. Upstream: 11 s of "look", then 4 s of "laugh", and the laugh is what makes people share. In an ad, the payoff is the product moment and the CTA.

### Carrying it to another subject

| Layer | Art-history original | "A city over 100 years" |
|---|---|---|
| Skeleton | window, table, cat, person | one street corner: lamp post, shop sign, passers-by, skyline |
| Living painting | era motif loops | each decade's vehicles passing, the sign's lettering flickering, things in the sky (kite, plane, drone) |
| Transition | the next era's signature | the next decade's medium: film burn, TV snow, pixels, scanlines |
| Beat | 128 BPM, shrinking segments | same |
| Anchor + payoff | year counter + the cat knocking the cup off the table | year counter + the same pigeon stealing food in every decade |

Don't misread it: the number of styles is not a quota (three works), it is not the mechanism for every topic, and copying a reference pixel for pixel is only a way to learn the mechanism, never the deliverable.

## 4. Rhythm on a beat grid

Fix the BPM grid first; every cut, transition start, beat punch and accent lands on it. Silent ads benefit too: the rhythm is visible, and any music added later snaps to it.

| BPM | Beat | Eighth |
|---|---|---|
| 90 | 0.667 s = 20 frames | 0.333 s = 10 frames |
| 100 | 0.6 s = 18 frames | 0.3 s = 9 frames |
| 120 | 0.5 s = 15 frames | 0.25 s = 7.5 frames |
| 128 | 0.469 s = 14.06 frames | 0.234 s = 7.03 frames |

128 BPM suits speedruns and montage; 90, 100 and 120 give whole-frame beats at 30 fps.

- Write the segment table first, in eighths per segment; the timeline, transitions and any later music come from it, and retiming means editing one array. Compute boundaries from the running total and round once: `Math.round((eighthsSoFar * 60 * 30) / (bpm * 2))`. Rounding each segment's length separately drifts off the grid.
- Accelerate by shortening segments, not by raising the tempo: at a constant 128 BPM the upstream eighths per segment ran 6, then 4 x5, 3 x4, 2 x3, 1 x3, then a final 9+. Transitions shrink with them (0.4 s down to 0.13 s, 12 to 4 frames), and so do counter rolls (0.55 s down to 0.07 s). To get there, list the duration each segment wants, round to eighths, then nudge the list into a regular decreasing pattern.
- The reveal is the accent. If the reveal happens at fraction `r` of a transition lasting `d` frames, start the transition at `beatFrame - r * d` so the reveal, not the start, lands on the beat.
- Payoff hits (impact, fall, splash) land within 3 frames of a beat.
- If the ad has music: hard onsets at segment starts, no crossfades, no whooshes. When music is fitted after the picture, tempo can vary per segment: upstream gave each segment a whole number of beats and nudged its tempo between 86 and 104 BPM, so all 24 world boundaries landed on a bar's downbeat (max error 11.7 ms, mean 3 ms; a single BPM missed by up to 112 ms). Listeners don't hear a +-8% tempo change between segments; they do hear a style change that misses the downbeat.

## 5. Journey through styles (long scroll)

A sibling of style swap. Instead of one scene repainted, a long horizontal strip of worlds joined end to end: each world is a horizontally extended painting, the hero keeps moving one way, and the moment it crosses a boundary its style changes with the world. Upstream ran 24 worlds in 123.7 s; a 3-world demo ran 15.6 s. For a 6-30 s ad, use 3-5 worlds of 2-6 s each.

Ad version: the hero is the product, or a real cut-out person or painted hand carrying it. A bottle slides along a counter that turns from woodcut to watercolour to pixel art and ends in the brand's own world with the CTA.

Fixed constants (1920x1080), kept in one place:

- ground line at y = 760; hero standing height 300; hero at screen x = 720;
- each world 2000-2800 px wide; within 150 px of either end the ground returns to 760 and the horizon sits at 480-560, so neighbours join; in between, bridges and steps come from a `ground(x)` function;
- portrait (1080x1920): keep the proportions (ground at ~70% of the height, hero ~28% of the height), or scroll vertically.

Rules:

- **The camera only moves forward.** Target = hero x - 720 + `lead` (space opened ahead during an interaction; `lead = 0` holds the camera still). Take the running maximum, then smooth it: the result is monotonic and doesn't jolt at stops and starts. Evidence: v1 let the camera ease back after interactions, and 17 of 24 segments rewound 68-256 px. Metrics missed it; viewers saw it at once. Running max plus smoothing gave 0 rewinds.
- **Time events from the segment's interaction start**, never "n seconds into the segment". Evidence: walk speed later went from 330 to 560 px/s and no segment needed retiming.
- **Draw each boundary in the incoming world's signature:** torn paper edge, pixel checkerboard, colour-block divider. This is "the transition is the next style's signature" in long-scroll form.
- **A hero straddling a boundary is drawn twice,** each copy clipped (`clipPath`) to its own world's side and treated in that world's style.
- **The walk cycle runs at a rate proportional to walk speed** (8 drawings or photos per cycle).
- **Worlds are a registry:** an array of `{ id, width, ground, act: { at, dur }, Back, Front, Seam }`, built against fixed constants. Render only the worlds overlapping the viewport, inside one strip translated by `-camera`.
- **Don't add gags nobody asked for.** Upstream had a "souvenirs stacking on the hero's hat" feature, off by default: it fights the scene for attention.

Monotonic, smoothed camera, computed once for all frames:

```tsx
import { useMemo } from "react";

export const useCamera = (heroX: (f: number) => number, lead: (f: number) => number, total: number) =>
  useMemo(() => {
    const raw: number[] = [];
    let max = -Infinity;
    for (let f = 0; f < total; f++) {
      max = Math.max(max, heroX(f) - 720 + lead(f)); // running max: never backs up
      raw.push(max);
    }
    const R = 12, sigma = 6; // Gaussian smoothing in frames; keeps it monotonic
    return raw.map((_, f) => {
      let sum = 0, wsum = 0;
      for (let k = -R; k <= R; k++) {
        const w = Math.exp(-(k * k) / (2 * sigma * sigma));
        sum += (raw[Math.min(total - 1, Math.max(0, f + k))] ?? 0) * w;
        wsum += w;
      }
      return sum / wsum;
    });
  }, [heroX, lead, total]); // define heroX and lead at module level so this memo holds

// const cam = useCamera(heroX, lead, durationInFrames)[frame] ?? 0;
// <AbsoluteFill style={{ transform: `translateX(${-cam}px)` }}>{visibleWorlds}</AbsoluteFill>
```

## 6. Other practices that proved out

**Stillness is not stuck; the same move in every shot is the disease.** Evidence: in one storytime-cartoon style about 70% of adjacent frames are identical, and that is the style (the joke lands on the cut to a silent reaction). An explainer with a uniform 7.5% slow push on all 31 shots felt "like a slideshow"; the approved rework held still, pushed 18-32% in 0.28 s (8 frames), held, panned 0.30 s (9 frames) at the same scale, and slammed in over 0.17 s (5 frames). Still frames rose from 16% to 72% and fast-motion frames from 0.7% to 10%. Several things changed at once, so read this as direction, not proof. A later 102 s piece that pushed in about 48 times, always inward, was "too many, too fast, not smooth". Use: move the camera to where the viewer should look; keep transitional moves gentle (push, pan or pull over 0.6-1.5 s, 18-45 frames); save quick pushes and slams for accents; after pushing in, come back out. Painted frames still stay alive through their motifs while the camera holds.

**One focus per screen: structure, then content, then one highlight.** Evidence: three independent grammars converged on it. Kinetic type: the key word slams in, the rest rises from a mask. Finance charts: axes first, then data, then mark one thing. Maths explainers: one colour per concept, the previous concept morphing into the next, almost no cuts. Use: one hero per moment; build the frame up in that order.

**Check your idea of a style against real examples.** Evidence: a first news-explainer pass used torn-paper transitions, and counting frames in five real examples found none. A cartoon channel measured a mean shot of 2.4 s with about 70% of adjacent frames static, the opposite of "animation must always move". Use: build a style's signature from what that style actually does; impressions are often borrowed from imitators.

**Animation yields to fixed overlays.** Evidence: in a portrait piece, callouts at y ~1460 collided with burned-in captions (y 1400-1520); laying the chart out inside the safe band (y 300-1430) fixed it, and filling the margins with the film's own dark ground removed a brightness jump between shots. In portrait the bottleneck is width: a full-width screenshot crop left body text ~20 px tall, unreadable on a phone; cropping to the key phrase and pushing 2.4x gave ~50 px. Use: platform UI and captions don't move, so lay the animation out inside the platform's safe zone and give each moment one half-sentence-sized focus.

**Frame-perfect is not correct.** Evidence: reviews caught a diagram wired to the wrong layer, "rose 9x" written where "rose to 9x" was meant, and two prices for the same endpoint that disagreed, all in frames that looked flawless. Use: check every claim, price, unit and number in the frames against the brief; never truncate a chart axis without saying so on the chart.
