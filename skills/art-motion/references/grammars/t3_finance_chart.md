# Financial Data Charts (The Economist / FT / Bloomberg data graphics)

> Adapted from huashu-art-motion (MIT, (c) 2026 alchaincyf) - references/动画语法/t3_finance_chart.md

Build the axes, grow the data, then annotate exactly one thing. One colour carries the hero and everything else goes grey. Values stay honest (bars from zero, unit and source on the chart): animation decides how a number appears, never what it is.

Evoke the grammar; never copy the channel's characters, branding or footage.

## Use it / avoid it

Use it for:
- Growth in revenue, profit or users; price trends; market-share rankings (bar chart race); regional comparisons (shaded maps); an inflection around an event. Best when the copy has specific numbers, dates or comparisons ("8.7x in five years", "since March 2023").
- Segments that must be credible, which viewers will screenshot and check.
- Ads: proof and performance claims, only when the brief supplies the numbers and their source. Never invent, round up or "illustrate" numbers in an ad. No numbers in the brief means no chart.

Avoid it for:
- A single number: use a big counting number instead (keynote UI or kinetic type grammar).
- Data you can't source or don't trust: make no chart at all.
- Mechanisms: use the 3b1b grammar.

## Before you start

1. **Write each chart's one point.** The title is that conclusion and the annotation marks only it. If you can't write the sentence, make no chart; use one big number or another grammar.
2. **Numbers reconcile.** A multiple in the title must be computable from the chart (show a / b in the annotation); the same number in two shots must match. "Rose to 8.7x" and "rose by 8.7x" are different claims.
3. **Data grows on its word.** Each bar or group grows when the copy names it. Don't show the title at 0 s and then grow everything at once.
4. **Hold after landing** for >= 0.5 s (15 f), with no constant slow push. To look at a detail, slow-push ~1 s (30 f) when the copy names it (Heer & Robertson: ~1 s per step, ease in-out). Only the single most critical number gets a 0.28 s (8 f) quick push, or a zoom-through into that point.
5. **At most 3 charts with the same layout in a row.** Rule + title + chart three times reads as flipping through a report; break it with a push-in, a slammed big number, or a cut to real product footage.
6. **Keep the chart in the film's world.** Its background belongs to the same family as the neighbouring shots: a dark film gets a dark chart, and a white report page only belongs in a paper or web-page film. Better still, draw the chart onto an object in the scene (a phone screen, a sheet of paper, a board). A white chart with a fixed title bar cut into a night scene "breaks from the film".

## Composition

| Item | Value | Source |
|---|---|---|
| Background | white `#FFFFFF` (Economist web charts) or FT salmon `#FFF1E5`; dark variant `#0E1116` with light text and cyan hero bars | (official) Economist 2017 style guide; FT o-colors |
| Layout | thin top rule (8 px) + small top-left tag (96 x 22) + bold title (the one-sentence conclusion) + subtitle (metric, unit) + source at bottom left | (official) Economist |
| Palette | red `#E3120B`, blue `#006BA2`, cyan `#3EBCD2`, green `#379A8B`, yellow `#EBB434`, grey `#758D99`, black `#0C0C0C` | (official) Economist |
| Emphasis | one colour for the hero, the rest light grey (demo: the last bar stays blue, the others go to `#C6D2D8`) | (official) Datawrapper |
| Grid | horizontal lines only, thin grey (demo 1.5 px at 13% opacity); only the zero baseline is solid black (3 px); y tick labels at the right end, sitting above their lines | (official) Economist |
| Type | The original uses Econ Sans Condensed. Use `RobotoCondensed` for numbers (demo), or the brand's condensed face. Title 700; subtitle and axes 400; axis text smallest; source smallest and lightest (75% black) | (official) / (demo) |
| Up/down colours | mainland China A-shares: red up, green down. Hong Kong and the West: green up, red down. State the convention on the chart when it could be misread; colour-blind safe: blue/orange plus up/down triangles | (official) Jiang et al. 2014; Bloomberg terminal |
| Strokes | main data line 5 px, moving average 4 px, callout leader 2 px | (demo) |
| Shapes | rectangle bars, polyline with end dot, candle body + wick, small dot + leader callouts | |

Brand mapping: the hero colour is the brand primary (if it is red or green, keep it clear of up/down meaning). Colour the rule and tag with the brand accent, not Economist red: the thin rule + tag layout is the grammar, while the red-and-Econ-Sans identity belongs to the Economist. Keep the grey for everything secondary.

## Motion

- **Staging:** layout 0-0.5 s -> gridlines draw left to right one by one (lag 0.12, quintOut) -> x labels fade in rising, in order -> data -> emphasis colour change -> annotation. Each stage takes ~0.5-1.3 s (15-39 f). Heer & Robertson 2007: stage complex changes, ease in-out, ~1 s per step. Axes before data is an industry convention without empirical backing, but viewers see the ruler before the quantity.
- **Bars:** grow from the zero baseline with quintOut `Easing.out(Easing.poly(5))`, staggered (lag 0.22, 1.3 s / 39 f in total). Value labels ride the bar top and count in sync. Never bounce.
- **Line:** draw by x (time), not by arc length. Time flows evenly, so steep stretches draw fast and read as a surge. A 9 px head dot and a tabular price label follow the head; area gradient 14% -> 0 opacity. Demo: 1.5 s (45 f) with smooth easing (`6t^5 - 15t^4 + 10t^3`), so the last price "lands" on the dot. D3's 5000 ms linear suits standalone charts; in video use 1.5-2 s.
- **Annotation:** fires as the head passes the event. The dot pops (spring d 0.45 s, bounce 0.25; see the SwiftUI-style spring in the keynote UI grammar) with one pulse ring; 0.12 s (4 f) later the leader draws; 0.3 s (9 f) later the text fades in. One annotation per shot.
- **Candles:** one by one (lag 0.06, over 0.2-1.3 s); each body grows from open to close, then the wick unfolds; volume bars in sync. The top-right price follows the newest candle, coloured by its change from the start of the range.
- **Numbers:** count up with easeOutExpo (CountUp.js default is 2 s; in video 0.9-1.3 s / 27-39 f). Tabular figures.
- **Bar chart race** (not in the demo; D3 reference): 250 ms per keyframe, 10 interpolated frames between keyframes, 12 bars visible; a position swap takes ~0.5 s. Stagger rank changes so the bars don't all jump at once.

Lags are LaggedStart ratios: item i runs over `[i*r, i*r + 1]` of a total `1 + (n-1)*r`.

## Camera and transitions

Camera baseline: once the chart has grown, the camera holds. It moves only when the copy names a data point: a slow push of ~1 s, or a 0.7 s (21 f) move to the next group. A quick push of 0.28 s is reserved for the one or two most critical numbers in the film. During zoom transitions keep redrawing vectors (scale the SVG, never a bitmap). The demo's constant 1 -> 1.03 push is outdated.

Transitions:
1. **Slide push:** the new panel pushes in from the right while the old one exits left, led by a brand-colour vertical bar at the seam. 0.5 s (15 f), `Easing.bezier(0.7, 0, 0.2, 1)`. The new panel builds its layout while sliding (rule grows, title rises).
2. **Push into a detail:** the camera pushes 6x around the latest data point, and the new view (e.g. the last 20 daily candles) dissolves in from 0.6x scale with its subject (the latest candle) aligned to the push point. Without a circular opening, never start the new view tiny: it reads as a small floating card.
3. **Morph between charts:** same data, new encoding (bar -> dot -> line). Move into place first, then change shape (Heer & Robertson: scatter -> bar slides horizontally, then morphs; stacked -> grouped changes width, then drops). Never morph between different metrics: revenue bars turning into a price line implies the same unit.
4. **Axis rescale:** when the range changes, change the ticks first (old fade out, new fade in), then move the data.
5. **Hard cut, layout fixed:** the frame, rule and title stay put and only the content changes. This is the most common move in Economist videos.

Timing:
- One chart holds 2.5-6 s (75-180 f); the demo's 2.8 / 2.7 / 2.5 s is compressed (in real use, one chart per one or two sentences). Narrative arc: establisher -> initiator -> peak -> release (Amini et al. 2015, from 50 professional data videos).
- A number lands exactly when it is said or shown: fix the landing frame first, then back-compute the start. The annotation pops as the line head passes the event.
- Copy: the title is the conclusion ("Revenue rose to nearly 9x in five years": "rose to", not "rose by", because 8.7x the original is an increase of 7.7x). The subtitle gives the metric and unit ("Annual revenue, $bn"). A multiple must be computable from the chart (107.9 / 12.4 = 8.70). A non-zero axis is stated in the subtitle ("y-axis does not start at 0"). The source is one line at bottom left.

## Build it in Remotion

- **SVG chart** in a fixed viewBox; scales are plain linear functions. Gridlines: `x2` grows with quintOut, staggered.
- **Bars:** `<rect>` with `y = baseline - h * p`; `interpolateColors` for the hero/grey step. Negative values go below the bar, clear of category names.
- **Line by x:** a `clipPath` rect whose width follows the eased x; the head dot sits at the interpolated y for the current x; the area is a `<path>` filled with a vertical `linearGradient`.
- **Numbers:** `fontVariantNumeric: "tabular-nums"`; reserve the final value's width (a hidden copy of the final string underneath).
- **Placement:** full frame on the film's background, or a chart component positioned and perspective-transformed inside a scene object (the phone screen in a product shot).
- **Vertical (1080x1920):** keep the chart, annotation, subtitle and source inside the safe area. In upstream tests the vertical annotation landed exactly on the burned-in caption band.

```tsx
import { Easing } from "remotion";

export const quintOut = Easing.out(Easing.poly(5));
export const lagged = (p: number, i: number, n: number, r: number) =>
  Math.min(1, Math.max(0, p * (1 + (n - 1) * r) - i * r));

// Nice ticks (1, 2, 2.5, 5 x 10^k) that enclose the data; bars always include 0
export const niceTicks = (lo: number, hi: number, target = 5) => {
  const min = Math.min(0, lo);
  const raw = (hi - min) / target;
  const k = Math.pow(10, Math.floor(Math.log10(raw)));
  const step = ([1, 2, 2.5, 5, 10].find((m) => m * k >= raw) ?? 10) * k;
  const decimals = (String(+step.toPrecision(6)).split(".")[1] ?? "").length; // 2.5 -> 1
  const ticks: number[] = [];
  const top = Math.ceil(hi / step) * step; // max 130 -> 150, never 100
  for (let v = Math.floor(min / step) * step; v <= top + step / 2; v += step) ticks.push(+v.toPrecision(12));
  return { ticks, decimals };
};

// Frame where an eased reveal reaches fraction `frac` of the x-range (annotation trigger)
export const hitFrame = (start: number, dur: number, frac: number, ease: (t: number) => number) => {
  let a = 0;
  let b = 1;
  for (let i = 0; i < 24; i++) {
    const m = (a + b) / 2;
    if (ease(m) < frac) a = m;
    else b = m;
  }
  return Math.round(start + dur * b);
};
```
`hitFrame` keeps the callout synced with the line head even when the line's duration changes.

## Pitfalls

1. **Truncated axes.** Bars always start at 0; lines and candles may not, but say so on the chart. A Tufte Lie Factor (effect shown / effect in the data) outside 0.95-1.05 is distortion, and axis-break marks don't undo the exaggeration (Correll et al. 2020).
2. **Too many colours, everything a hero.** One colour tells the story and the rest go grey; say what red and green mean for this audience.
3. **Animation too fancy to read.** No bouncing bars, 3D bars or spinning pies. Stage it, ease in-out, ~1 s per step, and hold >= 0.5 s after numbers land.
4. **Wording that contradicts the maths:** "rose by 9x" when the chart shows 8.7x the original. Check every claim against the plotted numbers.
5. **Numbers that don't reconcile across shots.** In the demo, a monthly line ended at 268 while the daily chart pushed into 286.40. Derive both from the same data.
6. **Ticks that lie or don't enclose the data.** Rounding printed -2.5 / 2.5 / 7.5 as -3 / 3 / 8; a max of 130 with a top tick of 100 let bars poke out. Take decimals from the step and add a step above the data.
7. **Overlaps:**
   - Two big numbers ghosting during a transition: clear the head label within 0.2 s of the push start.
   - Labels sitting on candles, or bars touching a gridline: move labels into empty space and normalise volume bars with a 6 px gap.
   - A big number covering the rising line head: reserve a strip above the plot.
   - Label thinning removing the annotated bar's name: the annotated item always keeps its name.
8. **Too much for the time.** A 2 s daily-candle shot was unreadable until the moving average was removed (candles done by 1.3 s, callout at 1.75 s, then a 0.75 s hold).
9. **Up/down colours clashing with a red brand.** State the convention, or switch to green-up or blue/orange.
10. **Overflow.** Everything that can overflow needs a fallback: shrink, then wrap to two lines, then make room. Test the longest real labels in vertical.
