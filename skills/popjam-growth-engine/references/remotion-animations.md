# Animation creatives: programmatic Remotion videos

Read this when a concept's `format` is `ANIMATION` — a motion-graphics ad built as React/Remotion
code and rendered locally with `npx remotion render`, instead of a model-generated video. This is
POPJAM's animategen path adapted to Claude Code: you write the composition, you run the render,
and the output MP4 lands in the campaign dir. Image/video generation lives in
[higgsfield-media.md](higgsfield-media.md); the concept JSON shape lives in
[data-models.md](data-models.md).

## Why animation instead of generated video

Pick `ANIMATION` when the message is text-forward — offers, price points, feature lists, stat
reveals, punchy hook/benefit/CTA sequences — or when the brand's logo must appear exactly right.
Generated video redraws logos (~70% unfaithful in POPJAM's measurements); an animation composites
the **real logo file** as an `<Img>` layer, so fidelity is guaranteed by construction and
`media.logo_ok` is true without a visual check. Pick `VIDEO`/`SHORT` instead when the concept
needs humans, live footage, voiceover, or camera realism. Animations are also deterministic and
cheap to iterate: a variant is a two-file edit and a re-render, not a new generation spend.

## Where things live

```
creatives/<concept-id>/animation/
  package.json          # remotion + @remotion/cli + react (nothing else)
  tsconfig.json
  src/index.tsx         # registerRoot + <Composition> — single source of truth
  src/MainScene.tsx     # root scene component
  public/               # REAL brand assets, served via staticFile()
  out/<concept-id>.mp4  # rendered output
```

The concept's `media` block points at `out/<concept-id>.mp4` after a successful render.

## Step 1 — the spec comes first (frame math)

The concept's `media_description` (always English) is the animation brief. For `ANIMATION` it
must be a frame-accurate spec, not vibes — if the concept-drafting phase left it loose, upgrade
it before writing any code, because every timing bug you'll hit later is a spec bug. Plan the
frame budget and text sizing FIRST; never compress dwell below the minimums.

Adapted from POPJAM's adgen agent (ANIMATION media brief spec, 30fps):

```
Write media_description as a frame-accurate motion-graphics spec in plain language —
NO React/Remotion/CSS code. Required structure:
1. Global spec — total duration in seconds AND frames (default 15s = 450f at 30fps);
   aspect ratio matched to platform (see the aspect map below); background; exact-hex
   palette; font roles with px sizes.
2. Scene-by-scene frame ranges.
3. Element-level specs: exact on-screen text (choreograph the ad's headline/body/CTA —
   don't invent copy), relative position (never raw pixels), px size + % screen height,
   hex color, entrance/dwell/exit frame counts with animation verb + easing intent.
4. A frame-math line proving scene durations − transition overlaps = total.

Frame budget: 5s = 150f → 2 scenes MAX; 10s = 300f → 3 scenes; 15s = 450f → 4 scenes;
one message per scene.
Text dwell: ≤3 words → ≥60f; 4-8 words → ≥90f; 9-12 words → ≥120f; never more than
12 words on screen at once.
Entrances 20-30f ease-out; exits 15-20f ease-in; entrance+exit ≤25% of an element's
screen time. Cross-fade/slide/wipe transitions run 15-20f with scene OVERLAP
(total = Σ scenes − Σ transitions); a hard cut adds a 30-45f background-only pause.
The final logo/CTA reveal dwells 60-90f.
Worked 15s example: scenes 95f + 125f + 125f + 150f − 3×15f overlap = 450f. ✓
```

Motion vocabulary (maps 1:1 to Remotion primitives): fade, slide (direction + px), scale,
spring pop (reserve for the CTA), typewriter/word-by-word (short text only). Easing intent:
"ease-out entrances, ease-in exits, gentle ease-in-out for premium/calm brands, springy with
slight overshoot for energetic ones". Stagger related elements 3-8f; ONE dominant motion at
a time.

Typography at 1080x1920: headlines 96-128px or 8-10% of screen height; body minimum 48-64px;
bold 600-700 below 64px; line-height 150%; letter spacing 0% @16px, −2% @48px, −4% @96px;
≤30-40 chars/line; text block ≤70% of width, 2-3 lines; contrast ≥4.5:1 (put a scrim over
imagery).

## Platform aspect map and safe zones

Match the canvas to the concept's `platform` (enum values from [data-models.md](data-models.md)):

| Placement | Aspect | Canvas | Safe zone (px from edge: top / bottom / sides) |
|---|---|---|---|
| TIKTOK | 9:16 | 1080x1920 | 130 / 250 / 60 |
| INSTAGRAM Reels & Stories | 9:16 | 1080x1920 | 200 / 250 / 50 |
| YOUTUBE Shorts | 9:16 | 1080x1920 | 200 / 400 / 100 |
| FACEBOOK / INSTAGRAM feed | 1:1 | 1080x1080 | center 80% safe |
| YOUTUBE | 16:9 | 1920x1080 | center 90% title-safe |

Default is 9:16. All text and logos rest within the center 80% regardless of placement, and the
CTA sits above the bottom clear zone — platform UI (captions, buttons, progress bars) covers
everything outside it.

## Step 2 — scaffold the project

Invoke the installed `remotion-best-practices` skill (Skill tool) before writing composition
code — POPJAM injects the same skill into animategen, and it carries the current Remotion API
guidance (sequences, springs, transitions) this file deliberately doesn't duplicate.

Minimal `package.json` (then `npm install` inside `animation/`):

```json
{
  "name": "<concept-id>-animation",
  "private": true,
  "dependencies": {
    "@remotion/cli": "^4",
    "react": "^19",
    "react-dom": "^19",
    "remotion": "^4"
  }
}
```

`src/index.tsx` holds `registerRoot` + `<Composition>`, and the `<Composition>` is the single
source of truth: duration, fps, width, height, and every piece of ad data are read from it and
its `defaultProps` — never hardcoded inside scene components, never passed as render flags:

```tsx
import React from "react";
import { registerRoot, Composition } from "remotion";
import { MainScene } from "./MainScene";

const Root: React.FC = () => (
  <Composition
    id="Main"
    component={MainScene}
    durationInFrames={450}
    fps={30}
    width={1080}
    height={1920}
    defaultProps={{
      headline: "Stop guessing your macros",
      body: "One scoop. 27 nutrients. Zero math.",
      cta: "Try it for 30 days",
      logoSrc: "logo.png",
      productSrc: "product.png",
      colors: { bg: "#0B0B0F", accent: "#E3FF66", text: "#FFFFFF" }
    }}
  />
);

registerRoot(Root);
```

Type the root scene component `React.FC<Record<string, unknown>>` and cast props inside — a
typed props interface on the root breaks `<Composition>`'s prop plumbing. Use the concept's
actual headline/body/CTA in `defaultProps` (choreograph existing copy, never placeholders), and
remember viewers see only finished ad content — never render technical metadata into the frame.

Coding rules (from POPJAM's animategen file-writing contract):

- Always use `extrapolateLeft: "clamp"` and `extrapolateRight: "clamp"` with `interpolate()`,
  because unclamped values fly off-screen the frame after an animation "ends".
- Use `spring()` for organic motion (the CTA pop).
- Inline styles only; no CSS files, no styled-components.
- Constants at the top of each file: `COLORS` / `TEXT` / `TIMING` / `LAYOUT`.
- Components are pure functions of the current frame — same frame in, same pixels out.

## Step 3 — real assets via staticFile (the logo-fidelity win)

Copy the downloaded brand logo and product images (from the research phase, or from
`creatives/<concept-id>/`) into `animation/public/`, then composite them with
`<Img src={staticFile("logo.png")} />`. Render the ACTUAL asset — NEVER redraw the logo as
styled text, and never approximate it with a font, because a fabricated logo fails the same
fidelity bar generated video fails. Transparent PNGs composite cleanly here (unlike image
models, which mangle alpha), so prefer the transparent logo variant over a boxed one, and pick
the variant whose theme matches your background (light logo on dark bg, dark on light).

Prefer local files in `public/` over remote URLs. If a remote URL must stay in the source,
preflight it — the render fails on any unreachable image:

```bash
curl -sI -o /dev/null -w "%{http_code}\n" "<url>"
```

Anything that isn't `200` — including `403`/`401`/`451` bot-walls that still load in a browser —
gets removed or downloaded into `public/` and replaced with `staticFile()`.

## Step 4 — pre-render lint

POPJAM lints source before burning a render; do the same, because each failed render wastes a
full tsc + bundle + Chromium cycle. Adapted from POPJAM's animategen agent (render-breaking
pitfalls — the pipeline runs `tsc --noEmit` → `eslint` → render, and any failure fails the job):

```
1. Import or declare every identifier you use — TS2304 is the most common failure.
2. Google fonts: module names are PascalCase with NO underscores — `PlayfairDisplay`,
   `OpenSans`, `SpaceGrotesk`, never `Playfair_Display`/`Open_Sans`/`Space_Grotesk`
   (underscore spellings fail TS2307 every time). If unsure a family exists, use a
   system font stack. `loadFont()` takes the style string FIRST:
   `loadFont("normal", { weights: ["400", "700"], subsets: ["latin"] })` — an options
   object as the first argument fails TS2345.
3. Transforms: only `scale`, `translate`, and `rotate` exist as standalone style props.
   `skewY`, `scaleX`, `rotateX`, etc. are NOT CSS properties (TS2353/TS2561) — put them
   inside ONE `transform` string, and never specify `transform` twice (TS2783).
   Interpolated transform strings like transform: `translateY(${y}px)` are fine.
4. No IIFEs in JSX — `{(() => {...})()}` fails eslint. Lift the logic into a `const`
   above the `return`.
5. Remotion hooks (`useCurrentFrame`/`useVideoConfig`) only at the top of components —
   module scope or plain helpers crash the render at runtime.
6. ASCII only in code — smart quotes/em-dashes break the parser. Display text with non-ASCII
   characters belongs in defaultProps strings, not code literals.
7. Deterministic render: no top-level throws, no render-time fetches, no Math.random() or
   Date.now(). Bake all data into <Composition defaultProps>.
8. `<Composition>` `width`/`height`/`fps`/`durationInFrames` are literal integers —
   never constants or expressions (tooling parses them statically).
```

Quick sweep before rendering:

```bash
grep -rn 'google-fonts/[A-Za-z0-9]*_' src/   # rule 2: underscore font modules (always broken)
grep -rn 'loadFont({' src/                   # rule 2: options object passed as first arg
grep -rnE '(skew[XY]?|scale[XYZ]|rotate[XYZ]|translate[XYZ]) ?:' src/ # rule 3: fake standalone props
grep -rn '{(() =>' src/                      # rule 4: IIFE inside JSX — extract to a component
grep -rhoE 'https?://[^"'\''` )]+' src/ | sort -u   # feed each into the curl -I preflight
```

## Step 5 — render locally

```bash
cd creatives/<concept-id>/animation
npx remotion render src/index.tsx Main out/<concept-id>.mp4
```

Duration, fps, and dimensions come from `<Composition>` — pass no `--frames`, `--fps`, or size
flags, so the render can never disagree with the spec. Success is terminal: render once per code
state and don't re-render unchanged sources. On failure, read the error (it's a tsc/eslint line
reference or a missing asset), fix only the broken file — the rest of the tree is known-good —
and render again.

Verify the output before accepting it: pull stills at each scene's midpoint and the final CTA
frame (`npx remotion still src/index.tsx Main check.png --frame=<n>`) and check text sits inside
the safe zones, dwell feels right, and the logo is the real asset. `npx remotion studio
src/index.tsx` gives a scrubbable preview when a timing issue needs eyeballing.

## Step 6 — record the result

Update the concept's `media` block (shape in [data-models.md](data-models.md)): `path` to the
rendered MP4, `aspect_ratio` (e.g. `"9:16"`), `model: "remotion"`, `kind: "video"` (MediaKind
has no "animation" literal — the rendered MP4 is a video; `model: "remotion"` carries the how),
`logo_ok: true` (real file composited). Append a `log.md` line noting the render and any spec
deviations. Simulation shows personas the actual file — never point `media` at an unrendered or
stale MP4.

## Iterating: committed vs staging discipline

POPJAM keeps two copies per animation — `committed_files` (last successfully rendered baseline)
and `source_files` (staging). Locally one directory plays both roles, so hold the line by
convention: the tree as of the last successful render is your baseline; edits on top of it are
staging until a render succeeds; the concept's `media` block only ever advances on success. If
the campaign dir is git-tracked, commit after each successful render so the baseline is
recoverable.

When iterating, edit — don't rewrite. Touch 1-2 files per change, and never rewrite
`src/index.tsx` unless you're changing the composition's dimensions, fps, or duration. For a
variant (`con-hustle-01-v2` with `og_id`), copy the parent's `animation/` dir into the variant's
creatives dir, apply the variant's `reasoning` as a minimal diff, re-render, and update the
variant's own `media` block.

Renders are CPU-bound, not credit-bound: run a handful of concepts sequentially. Only reach for
the Workflow tool (script templates in the skill's `workflows/` dir) when a large batch of
animations must render alongside other pipeline fan-out.
