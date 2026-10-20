# Keynote UI and Gradient Motion (Apple-style launches; Linear, Stripe and OpenAI launch films)

> Adapted from huashu-art-motion (MIT, (c) 2026 alchaincyf) - references/动画语法/t2_keynote_ui.md

One thing per screen: the product itself (screenshot, screen recording, physical product) is the hero, nouns and numbers land the moment they come up, type is tight, and springs don't bounce or barely do. Mesh-gradient backgrounds, frosted-glass cards, gradient text, centred blur-in and decorative floating are optional wrapping; use them sparingly.

Evoke the grammar; never copy the channel's characters, branding or footage. No Apple/Linear/Stripe/OpenAI logos, UIs, SF Pro or signature gradients: the brand's own product is the hero.

## Use it / avoid it

Use it for:
- Product and feature launches, version updates, "three new features", price and spec reveals, brand openers, "what is this product" segments. Best when the copy is noun + number ("Plover 2", "320 ms latency", "1M tokens"): one sentence per screen, the noun rises in as it comes up, the number lands as it is said. Product ads are this grammar's natural home.
- Explaining a UI screenshot: full-bleed, pushed in to the part being discussed. Glass cards and 3D tilts are optional wrapping.

Avoid it for:
- Mechanisms (glass and gradients carry no logic: use the 3b1b grammar) and data trends (finance chart grammar).
- Serious incidents and bad news: this language carries a "good news" mood.
- Content with no hero to enlarge (only empty gradient remains), and non-launch topics. Don't use the dark launch stage as a generic template.

## Before you start

1. **This set reads as an AI template faster than any other.** Mesh background + glass card + gradient text + centred blur-in + floating cards, all five together, is recognised instantly. First ask: is there a real product screenshot, recording or photo? If yes, make it the full-frame hero and push to the part being discussed; drop the mesh and the glass. At most two of the five wrappers per film.
2. **Screenshots big:** width >= 80% of the frame (vertical >= 90%), contain-fit (never crop through key UI), padded with a darkened, blurred copy of the same image. Push in only when the copy points at a part unreadable at full view: default slow push ~0.9 s (27 f); quick push 0.28 s (8 f) only for a reveal or a comparison result. One or two pushes per screenshot; after pushing in, pull back to the whole or pan to the next part. A small card floating on a big gradient is a "dead background".
3. **Count layouts.** Write down each screen's layout (title, three cards, big number, screenshot). The same layout twice in a row: change it (screenshot push, number slam, before/after). Title -> three feature cards -> big number on a loop is a flip-through deck.
4. **Hold after landing.** No floating cards, no constant slow push to fill pauses; the next move happens on the next noun or number. A number about the screenshot (two timings compared, the page's result): pull back to the whole screenshot, darken it, slam the number on top. Don't cut to a gradient page for it.
5. **Colours follow the product.** Background and accent come from the brand. No default purple-blue-cyan mesh unless the brand itself is blue/purple. No dark launch stage for bad news, serious events or non-launch topics.

## Composition

| Item | Value | Source |
|---|---|---|
| Background | near-black: demo `#050508`; Apple `#000000` / `#161617` / `#1d1d1f`; Linear `#08090a` (elevated `#0f1011` / `#141516`, body text `#f7f8f8`, border `#ffffff14`) | (measured) site CSS |
| Mesh (optional) | 4 radial gradients blended with `screen`, very soft, plus 3.5% static grain against banding. Reference hues (Stripe family): purple `rgb(150,90,238)`, blue `rgb(56,104,255)`, cyan `rgb(120,214,255)`, a touch of warm red `rgb(255,96,84)`; Stripe 2021: `#a960ee #ff333d #90e0ff #ffcb57`. A 38% black radial vignette at the centre gives white text contrast. In ads, take the hues from the brand palette | (measured) |
| Mesh motion (optional) | each blob drifts 90-260 px with a 9.5-13 s period; avoid ~5 s periods (sustained ~0.2 Hz oscillation) | (official) Apple HIG Motion |
| Glass card (optional) | backdrop blurred 40 px (Apple nav: `saturate(180%) blur(20px)`; NN/g: more blur reads better) + 7.5% white fill + 14% white gradient band at the top + 1.5 px gradient border (bright top-left, dark bottom-right) + large shadow (blur 70-80, y +30-40, alpha 0.5) | (measured) apple.com CSS; NN/g |
| Corners | cards 36 px; concentric: inner radius = outer - padding (36 - 14 = 22) | (official) WWDC25 |
| Type | Inter (the closest open font to SF Pro; Linear uses it). Titles weight 600; large type tracked -0.02 to -0.03 em (Apple 96 px -0.015 em, Linear 64 px -0.022 em, OpenAI 64 px -0.03 em) | (measured) |
| Text hierarchy | primary `#f5f5f7`, secondary `rgba(235,235,245,.6)`, eyebrow `#a7a7b4` with +6 px tracking. Optional product-name gradient white -> pale violet -> pale cyan (with a mesh, it reads as template) | (measured) Apple site |
| Layout | one focus per screen; screenshot >= 80% of the width; three equal cards (480 px wide, 52 px gap at 1920 px) only for feature lists without screenshots; big numbers >= 55% of the frame width | (demo) |
| Shapes | rounded rects, capsules, thin-line icons (round caps, uniform stroke) | |

## Motion

- **Springs (the main tool), SwiftUI-style duration + bounce:** mass 1, stiffness `(2*pi/d)^2`, damping `4*pi*(1 - bounce)/d`, so the damping ratio = 1 - bounce. Default bounce 0 (most general). 0.15 is crisp and barely bounces (demo card entrance d = 0.75 s, bubble d = 0.5 s). 0.3 bounces visibly; above 0.4 is exaggerated for UI. SwiftUI's .smooth / .snappy / .bouncy are all d = 0.5 (bounce 0 / 0.15 / 0.3).
- **Curves:** apple.com nav 0.32 s `Easing.bezier(0.4, 0, 0.6, 1)`; text rise CSS ease `Easing.bezier(0.25, 0.1, 0.25, 1)`; Linear ease-out-quad `Easing.bezier(0.25, 0.46, 0.45, 0.94)` at 0.16 s; Stripe: under 500 ms with `Easing.bezier(0.2, 1, 0.2, 1)`.
- **Text entrance** (centred blur-in is optional; every screen rising out of blur is template): blur 18-26 px -> 0, rise 16-40 px -> 0, opacity -> 1 over 0.7-1.0 s (21-30 f). Eyebrow -> product name -> subtitle, staggered 0.2-0.4 s (6-12 f).
- **Card entrance:** from 170 px below, rotateY +-0.55 rad (~31 deg, side cards facing outward), scale 0.9, spring into place; three cards 0.1 s (3 f) apart. Perspective 1800 px (Stripe uses 600, Linear 1000).
- **Screenshot cards:** a new full-bleed screenshot hard-cuts in with a light 0.17 s (5 f) slam; consecutive full-bleed screenshots pan across at the same zoom in 0.30 s (9 f).
- **Slam** for a number or big type: 0.17 s (5 f), scale 1.55 -> 0.94 -> 1.0. Then hold for as long as the copy needs.
- **Counting:** starts 0.25 s (8 f) after the card settles and runs 0.9 s (27 f) with easeOutExpo (`Easing.out(Easing.exp)`, the CountUp.js default), so the last digit settles slowly. Count a number once: when a card expands to full screen, keep "1M"; never recount from 0. Tabular figures, so digits don't jitter.
- **Sheen:** a -20 deg band 110-140 px wide sweeps across in 0.8-0.9 s (24-27 f), clipped to the glyphs on text, additive on cards. For a row of cards, compute progress from each card's screen x so it reads as one light.

## Camera and transitions

Camera baseline: the screenshot is full-bleed and still. When the copy reaches a part that's hard to read, slow-push there in ~0.9 s; move to the next part in 0.7 s (21 f); quick push 0.28 s only for a reveal or a two-number comparison. Push at least 18% closer and at most 2.6x; the framed region ends up ~42% of the frame. One or two pushes per screenshot, then pull back or pan: never push-push-push. The demo's 7 px card float and constant 1 -> 1.045 push are outdated.

Transitions:
1. **Blur push:** the old scene scales to 0.92, blurs 24 px and fades; the new one comes from 1.06 with blur to 1.0, sharp. 0.55 s (16-17 f), CSS ease. Underneath, keep a 1.08x, 30 px-blurred copy of the old scene so the shrinking frame never shows black edges.
2. **Shared-element expand:** the chosen card scales to 1.06 while the others recede and dim to 45%. It then expands from its screen rect to the full frame, corner radius 38 -> 0, spring d = 0.55, bounce 0. The new scene is opaque inside the card from the first frame, scaled to the card's size; cards are translucent, so any crossfade shows two layers of text. Stop any float before expanding.
3. **Match cut:** the same object in the same position across shots (product name -> card title position).
4. **Mask wipe / sheen cut:** swap the scene behind a passing light band.
5. **Refraction instead of fade** (the Liquid Glass idea): exits change blur or refraction strength rather than just opacity.

Timing:
- Stage keynote screens run 5-8 s (Jobs's 2007 iPhone launch: 70 s over 9 screens, ~7.8 s each) (measured); product quick cuts 1.5-3 s (45-90 f); the demo used 2.6 / 3.0 / 2.4 s.
- One thing per screen: a noun, a number or a card. After a dense stretch, give one empty screen to breathe.
- Sync: text starts rising 0.2-0.3 s before its noun is said or shown (the rise takes ~0.7 s to sharpen). A number lands on its word: count start = landing time - count duration. Three cards enter on "first, second, third". Without voice, sync to the copy beats.
- Copy limits (adapted from CJK counts): title <= ~3-4 words or a product name; subtitle one sentence of <= ~8 words; card = 1-2 word title + one line + one big number + unit (one size smaller, one grey step lighter).

## Build it in Remotion

Layers, bottom to top:
1. **Stage:** the brand's near-black, or the screenshot as backdrop: `<Img>` with `objectFit: "cover"`, `filter: "blur(40px) brightness(0.5)"`, scaled 1.1 so the blurred edges stay off-frame.
2. **Camera wrapper:** `<AbsoluteFill style={{transform, transformOrigin: "0 0"}}>` holding the contain-fit screenshot `<Img>` and any highlight box with its dim mask (a `box-shadow: 0 0 0 9999px rgba(0,0,0,.5)` on the box works).
3. **Type:** eyebrow, title, subtitle, number. Outside the camera unless pinned to the UI.
4. **Logo** `<Img>` overlay, static; never redrawn.

```tsx
import { spring } from "remotion";

// SwiftUI-style spring: duration d (s) and bounce (0 = critically damped)
export const appleSpring = (frame: number, fps: number, d: number, bounce = 0) =>
  spring({ frame, fps, config: { mass: 1, stiffness: (2 * Math.PI / d) ** 2, damping: (4 * Math.PI * (1 - bounce)) / d } });

type Cam = { z: number; cx: number; cy: number }; // world point (cx, cy) at frame centre
// Frame a region r = [x, y, w, h] (0..1 of the image box at boxX, boxY, boxW, boxH)
export const camFor = (r: number[], box: number[], W: number, H: number, fill = 0.42): Cam => {
  const share = Math.max((r[2] * box[2]) / W, (r[3] * box[3]) / H);
  const z = Math.min(2.6, Math.max(1.18, fill / share));
  return { z, cx: box[0] + (r[0] + r[2] / 2) * box[2], cy: box[1] + (r[1] + r[3] / 2) * box[3] };
};
// Blend two cameras (p already eased); zoom in log space so speed feels constant
export const camAt = (p: number, a: Cam, b: Cam): Cam => ({
  z: Math.exp(Math.log(a.z) + (Math.log(b.z) - Math.log(a.z)) * p),
  cx: a.cx + (b.cx - a.cx) * p,
  cy: a.cy + (b.cy - a.cy) * p,
});
export const camStyle = (c: Cam, W: number, H: number) => ({
  transformOrigin: "0 0",
  transform: `translate(${W / 2 - c.cx * c.z}px, ${H / 2 - c.cy * c.z}px) scale(${c.z})`,
});
```
The resting camera is `{z: 1, cx: W / 2, cy: H / 2}`. Clamp cx/cy near the image edges so the frame stays on the padded backdrop.

- **Count-up without measuring text:** wrap the number in a `position: relative` span with `fontVariantNumeric: "tabular-nums"`; render the final formatted value inside it with `visibility: "hidden"` to reserve the width, and the counting value absolutely positioned on top, right-aligned. The unit never gets squeezed.
- **Blur-in:** `p` eased with `Easing.bezier(0.25, 0.1, 0.25, 1)` over 24 f; style `filter: blur((1-p)*22 px)`, `translateY((1-p)*28 px)`, `opacity: p`.
- **Glass:** prefer a clipped, blurred copy over CSS `backdrop-filter`. Inside the card (`overflow: "hidden"`, radius 36), render the same background offset by -cardX / -cardY with `filter: "blur(40px) saturate(1.8)"`, then the white fill, top band and gradient border (a 1.5 px-padded wrapper with a gradient background). It is deterministic, and you control the edges.
- **Mesh:** 4 absolutely positioned `radial-gradient` divs with `mixBlendMode: "screen"`, centres driven by sines of the frame. Soft gradients need no extra blur. Grain: an SVG `feTurbulence` with a fixed `seed`, static, at 3.5% opacity.
- **Blurring a full-frame layer fades its borders** to transparent or dark: oversize the layer (scale 1.08-1.1) or put an unblurred copy underneath.
- **3D cards:** the parent gets `perspective: "1800px"`; each card `transform: translateY(..) rotateY(..rad) scale(..)` driven by `appleSpring`.
- **Transitions:** a custom `TransitionPresentation` for the blur push (branch on `presentationDirection` "exiting" / "entering" with `presentationProgress`), or two overlapping `<Sequence>`s.

## Pitfalls

1. **Glass with nothing behind it.** Frosted glass only blurs what's behind it; on a flat dark stage it is a grey rectangle. If you use glass, put colour and variation behind it and sample at the card's position.
2. **Springs too bouncy, too much moving.** Bounce defaults to 0, entrances 0.15-0.3 at most; above 0.4 looks cheap immediately. Move one group at a time.
3. **Untracked large type, muddy mesh.** Track -0.015 to -0.03 em above 64 px. Each blob keeps its hue in its own region (screen blend); never average colours into grey-purple mud.
4. **Black edges during transitions** (demo review): keep the 1.08x blurred old scene underneath.
5. **Double text on card expand, then a recount from 0.** The new scene is opaque inside the card from frame 0; keep the same figure and wording throughout ("1M tokens", not "1M" on the card and "1,000,000" full-screen).
6. **Counter jumping** (999,023 -> 1,000,000 in one frame) with the unit squeezed: count once, reserve the final value's width, use tabular figures.
7. **End card too short or outside the safe area** (demo: 0.4 s at the frame edge). Let it rise over 1.2-1.8 s (36-54 f), hold >= 0.6 s, and keep it inside the platform safe zone.
