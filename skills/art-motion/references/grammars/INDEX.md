# Animation grammars for ads: index

> Adapted from huashu-art-motion (MIT, (c) 2026 alchaincyf) - references/09-视频动画语法.md

Eight animation grammars studied from YouTube explainer, tech, AI and finance channels, translated into Remotion for short ads. A grammar is a complete way of drawing a piece: palette, shape language, motion, camera and transitions. Each card holds the measured parameters and pitfalls of one grammar; this page helps you pick one and lists the rules that hold across all of them.

Each card is an evocation of a studied tradition. Never copy a channel's characters, branding or footage.

## 1. The eight grammars

| Grammar | What it is | Use it when | Avoid when |
|---|---|---|---|
| [kurzgesagt](kurzgesagt.md) | An abstract idea drawn as one concrete object in a glowing, zoomable flat world; the camera travels between scales. | "What's inside", scale, a mechanism or ingredient, "zoom in and you find..." | Real people or proof, step-by-step reasoning, no budget for rich scenes |
| [vox](vox.md) | The argument laid out on a desk of real material; a reporter's camera, stepped red lines and highlighter. | Real proof: press, reviews, screenshots, documents, real photos, "look at this line / number" | Nothing real to paste (it becomes a fake archive), derivations, character acting |
| [whiteboard](whiteboard.md) | Say a line, write a line on one big board; the camera follows; a final pull-out shows the whole argument. | A reasoning chain, "why X fails and Y works", problem to cause to fix, "how it works in 3 steps" | Precise data, complex spatial motion, emotional intensity |
| [storytime](storytime.md) | A simple character snaps between poses in 0.1 s and freezes; jokes land on a silent reaction close-up. | A first-person story, mishap or relatable skit with a punchline, and character art exists | Data or tutorials, copy with no "I", unfunny copy, no character assets |
| [kinetic-type](kinetic-type.md) | Words are the actors: keywords slam in on accents, the main word reads at a glance, one focus at a time. | Lists, "3 reasons", a slogan, a hook with a number, offer and CTA cards, silent ads where text carries the message | Emotional storytelling (no face), long dense explanation, lists over 5 items |
| [3blue1brown](3blue1brown.md) | Only the thing being discussed, on black; one concept transforms into the next; colour names the concept; almost no cuts. | A process turning into its result: before to after, input to output, a formula or algorithm | Launches, emotional or brand pieces, real data trends, opinion or story copy |
| [keynote-ui](keynote-ui.md) | One thing per screen; the real screenshot or product is the hero, pushed in; nouns and numbers land when read. | Product or feature launch, app UI, specs, pricing, tutorial steps | Mechanisms (3blue1brown), trends (finance-chart), bad news or serious topics, nothing worth magnifying |
| [finance-chart](finance-chart.md) | Axes first, then data grows, then one annotation; numbers stay honest. | Growth, comparison, share, turning points: numbers people will screenshot and check | A single number (use a big number), unreliable or unsourced data, mechanisms |

Timing in the source films (long-form; see section 2 for ads):

| Grammar | Typical shot | Main easing in Remotion | Main transitions |
|---|---|---|---|
| kurzgesagt | hard-cut shots 7-9 s, visual unit every 4.6-6.7 s | `Easing.bezier(0.75, 0, 0.25, 1)`; loops `Easing.bezier(0.333, 0, 0.667, 1)` | lens dive, colour-fill match cut (log-scale zoom) |
| vox | slow tempo median 3.3 s (a card 3-7 s); fast tempo 1.4-1.8 s | camera `Easing.inOut(Easing.sin)` or long tail `Easing.bezier(0.33, 0, 0.2, 1)`; elements stepped at 12 fps | hard cut, pan along the red string, push into a photo then cut |
| whiteboard | median 6.6 s per block | pans `Easing.inOut(Easing.sin)` 1.2-2.4 s; far jumps 0.8 s whip with motion blur | camera moves on one board, closing pull-out |
| storytime | average 2.43 s (median 1.87 s) | pose swap 0.1 s `Easing.out(Easing.exp)` plus squash-settle; character stepped | cut, smash, whip, jump-in |
| kinetic-type | one bar per shot (~2 s at 120 BPM) | in `Easing.out(Easing.exp)`, slam with `spring`, out `Easing.in(Easing.exp)` and faster | fill-zoom into a colour block, colour bands, push |
| 3blue1brown | one animation 1-3 s + 1 s wait; a concept 8-20 s | smooth `(t) => t * t * t * (t * (6 * t - 15) + 10)`, almost exclusively | transform continuity (no cut), zoom-through, fade-shift |
| keynote-ui | keynote screen 5-8 s; product quick cuts 1.5-3 s | `spring` with bounce 0-0.15; CSS ease `Easing.bezier(0.25, 0.1, 0.25, 1)` | blur push, expanding card |
| finance-chart | one chart 2.5-6 s | `Easing.out(Easing.poly(5))`; lines with smooth | panel slide-push, zoom into a detail, hard cut with a fixed layout |

## 2. Picking a grammar for ad copy

The input is ad copy or a campaign concept, usually without voiceover. Read what each beat of the copy is doing (hook, claim, proof, demo, offer, CTA), not the product category, then pick.

| The copy is... | Pick | Not | Why |
|---|---|---|---|
| Explaining how the product works, what is inside it, one mechanism | 3blue1brown (a transformation, before to after) or kurzgesagt (scale, inside the product, friendlier) | vox (nothing real to paste turns into fake evidence) | Mechanisms read through morphing and scale |
| Leaning on proof: press quotes, reviews, ratings, real screenshots, documents, founder or customer photos | vox | kurzgesagt (flat cartoon dilutes credibility) | The viewer needs to see the source. Never fabricate proof |
| A relatable story, mishap or skit with a punchline | storytime (only with character art) | keynote-ui (launch language carries a good-news mood) | The joke lives in the pause of the reaction shot |
| A list, "3 reasons", a slogan, a hook number, an offer or CTA | kinetic-type | 3blue1brown (nothing to morph) | The information is structure, not imagery |
| The product itself: feature, UI, specs, price, tutorial steps, launch | keynote-ui (screenshot or product photo full-bleed, pushed in; glass cards optional) | 3blue1brown (glass and gradients carry no logic, and vice versa) | One thing per screen; nouns and numbers are the stars |
| Numbers, growth, comparisons, before/after metrics | finance-chart | keynote-ui's big number (only for a single number) | Needs axes and units, and must survive scrutiny |
| A reasoning chain, step by step | whiteboard | full-screen slide swaps | Write a line per beat; the closing pull-out is the payoff |

Two fallbacks:
- Real screenshots or product photos available: keynote-ui (clean, product or tutorial) or vox (argument, evidence). The material is the main image, as full-bleed as possible, always scaled proportionally, never cropping key UI or the product.
- Only one number in the segment: no chart. Count it up big (keynote-ui or kinetic-type) so it lands on the beat where it should be read.

Ad-specific rules (the first three are the upstream's "bottom lines"; slide-deck feel mostly comes from breaking them):
1. The first event is visual: a curve, a screenshot, data growing, a dive, an icon, a screen close-up, a number slam. Never a title card at frame 0.
2. Text events are at most half of all events, and the same kind of event never runs 3 times in a row.
3. On-screen lines stay short: the upstream limit is 14 Chinese characters, roughly 6-8 English words (inferred). Long copy goes to captions or is split across beats.
4. Density: a 3-8 s segment holds 2-5 events. Denser than that, writing is forced to speed up and the camera cannot arrive.
5. One shot held longer than ~8 s reads as a slide: one layout to the end, a growing bullet list, a dead background. Split into shots that change composition, not style.
6. One ad = one palette and at most 2 grammars. A 6-15 s ad usually runs one grammar; 15-30 s may switch once, between segments and never inside one (for example a kinetic-type hook, a keynote-ui product demo, a kinetic-type CTA) (inferred).
7. Without voiceover, reveals align to music beats or to the reading pace of on-screen text. Budget about 3 words per second of hold and at least ~1 s per line (inferred). With a voiceover, align to its words as the cards describe.
8. Source durations come from long-form films. Ads are denser (the upstream 8 s demos already ran 2.5-3x long-form density): cut the number of beats, keep the holds. The hold after a number and after a punchline survive at any length.
9. Brand: map the brand palette into the grammar's colour roles; logo and product are `<Img>`, never redrawn; prefer the brand's real material as the main image.

## 3. Rules common to all grammars

1. **The camera is a function of time; the scene is redrawn for the camera.** Push, pan and dive are the same world rendered under a different camera, so a 60x zoom stays sharp and the outgoing shot keeps moving through a transition. In Remotion: camera values derive from `useCurrentFrame()`, the world is SVG/DOM inside a transformed wrapper, and a bitmap of a previous shot is never scaled up.
2. **Zoom on a log scale, and far enough through openings.** `z = exp(lerp(ln z0, ln z1, p))` multiplies the zoom by the same factor every frame; linear zoom starts slow and ends violently. To pass through an opening of radius r, zoom by at least the distance from its centre to the farthest screen corner divided by r: centred, ~1101/r at 1920x1080 or 1080x1920, 864/r at 1080x1350, 764/r at 1080x1080.
3. **The reveal frame lands on the beat or the word.** Compute transitions backwards: start = beat frame - reveal point x transition length. A number lands when it is meant to be read, so the count starts one count-duration earlier (~0.9 s, 27 f): a number can never land earlier than that from its segment's start. Whiteboard writing starts ~0.5 s after its phrase. With music, beat frame = round(beat index x 60 / BPM x fps).
4. **Structure, then data, then annotation.** Axes first, data grows, annotation last, one annotation per shot. A concept piece states the question before demonstrating; a launch screen goes eyebrow, product name, subtitle.
5. **One focus per screen.** Only one thing enters at a time while the rest hold still; main to secondary text at least 3:1; backgrounds one step lower in saturation, contrast and line weight than the hero.
6. **Enter slow, exit fast, hold after landing.** Entrances 0.3-0.4 s (9-12 f), exits ~0.18 s (5 f). Hold at least 0.5 s (15 f) after a number lands and 0.9 s (27 f) after a punchline; concept animations wait ~1 s after each move.
7. **Move on events; the camera goes in and comes back.** The camera moves only when the eye must go somewhere new: slow push, pan or pull-out, 0.6-1.5 s, ease in-out. Snap push (0.28 s, 8 f, 18-32% closer) and slam (0.17 s, 5 f, scale 1.55 to 0.94 to 1.0) only for reveals, twists and key numbers. After pushing in, pull out or pan away; never three push-ins in a row; fast moves at most a third of shots (kinetic-type and beat-cut segments follow the music; storytime rations pushes, not cuts). The same move in every shot reads as a slide deck, whether a constant slow push or a snap push per shot (a 102 s vertical short with ~48 push-ins was judged "too many, too fast, not smooth"). Numbers and big words slam onto objects in the piece's world (a screen, a price tag, a board), not onto a flat text card, which blind reviewers read as an inserted slide. Ambient layers may move continuously; storytime is ~70% fully still frames.
8. **Two frame rates: smooth camera, stepped elements.** Collage paper, highlighter and typing step at 12 fps under a smooth camera; storytime characters step while the camera stays smooth. All smooth reads as a corporate promo; all stepped jitters. Step from the element's own start (`Math.floor((frame - start) / step) * step`), not the absolute frame, or it appears up to 2 frames early.
9. **Colour is a concept; few accents.** One colour per concept, kept for the whole piece (a symbol and the object it names share a colour); more than 3-4 semantic colours will not be remembered. Collage is black, paper white, one red; whiteboard is black plus one orange.
10. **Transitions at breaths and topic changes, never mid-sentence.** Whips land between lines, reaction shots sit in silence, whiteboard pans mark a new point, collage cuts land on punctuation.
11. **Review logic and numbers, not just looks.** Caught in practice: "up 8.7x" where "up to 8.7x" was meant; a number recounting from zero after expanding to full screen; a label connected to the wrong element; a multiplier that could not be computed from the numbers on screen. In ads every claim and number must match the brand's verified facts.
12. **Real material is the main image, kept as it is.** Screenshots, photos, footage and quotes fill or nearly fill the frame and the camera pushes in to the part being discussed; code only explains, annotates and moves the camera. Scale proportionally and never crop key UI. Animation changes how data appears, never its value; bars start at zero; a non-zero axis is labelled. Upstream labels made-up data "illustrative" in every shot; in ads, do not show made-up data at all.

Further design rules:
- **One palette, six roles:** background, surface, ink, secondary ink, accent, accent2; every other colour is a tint or shade of these. No large gradient backgrounds or neon glow. Blue-purple gradients, deep-violet starfields and neon cyan-violet are the most recognisable "AI slop" defaults; unless the brand palette itself is blue/purple, keep frames that are over 30% blue-violet (hue 225-300 degrees, saturation >= 0.30) under 30% of the runtime (the upstream's rejection threshold). Flat navy (hue ~210) is fine.
- **Safe areas:** keep text, labels and chart annotations inside the platform's safe zone. In vertical video the bottom band is covered by captions and platform UI; the upstream reserved ~490-570 px at the bottom of 1080x1920 for captions alone, and ad placements usually need more (inferred).
- **Text grammars compete with captions:** kinetic-type, whiteboard, 3blue1brown and finance-chart put words on screen; if the ad also burns in captions, move them or drop them for that segment.
- **Charts stay in the piece's world:** same colour family as neighbouring shots (no white report sheet in a dark piece); better still, draw the chart on an object in the scene (a screen, a board, a sheet of paper).
- **Everything that might not fit needs a fallback:** shrink, then wrap, then make room by moving other elements, and only then give up. Layouts tuned on sample copy in landscape broke on real copy and vertical frames.

## 4. Pitfalls

- **A highlight that starts off-screen** was seen 7 frames late: move the camera first so it arrives one frame before the reveal, and limit the zoom so the circle around the highlight stays in frame.
- **The camera leaving a text card mid-typing:** leave only after typing ends plus a 0.5 s hold; if the gap is short, type faster (at most 40 characters/s).
- **Tick labels that lie:** with a 2.5 step, -2.5 / 2.5 / 7.5 printed as -3 / 3 / 8. Take decimals from the tick step.
- **Ticks that do not enclose the data:** a maximum of 130 with a top tick of 100 lets bars poke out. Add one tick step above and below.
- **Thinned category labels** dropped the name of exactly the highlighted bar: the annotated item always keeps its label.
- **A big number parked where the rising line ends:** give it its own band.
- **Sample-tuned layouts break on vertical and real copy:** a review of 33 test pieces found 12 serious faults: points pushed into the caption band, long numbers off-frame, clipped labels, typing overflowing its bubble, a transparent chart invisible over a dark shot, and a highlighter the same colour as its text erasing the word (invert the text under the marker to the background colour).
- **A fade that is really a cut:** per-character animation ignored the parent's opacity, so a 0.55 s fade vanished in one frame. Check fades frame by frame.
- **Ambient motion tied to the absolute frame** changed composition when its segment moved on the timeline. Inside a `<Sequence>`, `useCurrentFrame()` is local; use it unless continuity across segments is intended.
- **Non-deterministic frames:** a reused buffer made the same frame render one colour level apart. Carry no state between frames; randomness only via `random(seed)`.
- **Fonts:** load every face through @remotion/google-fonts; system fonts change on render. Check unusual whitespace in non-Latin copy (a full-width space rendered with zero width and glued words together).
- **Screenshots on vertical:** highlight the half-sentence being read. A ~900 px wide screenshot needs a 2-2.5x push for 16 px web text; split a long highlight into two, one keyword each. Estimated highlight rectangles are often 20-30% off: verify on a frame preview.
