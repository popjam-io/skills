---
name: remotion-render-pitfalls
description: POPJAM-specific render-breaking mistakes that fail our renderer (tsc, eslint, and Remotion render). Read this BEFORE writing animation source files. First-party supplement to the external remotion-best-practices skill.
license: MIT
metadata:
  author: POPJAM (https://popjam.io)
  tags: remotion, validation, tsc, eslint, render, debugging, reliability, popjam
---

# Render-breaking pitfalls (read before writing code)

> **First-party POPJAM skill.** This is maintained by us and is intentionally
> separate from the externally-maintained `remotion-best-practices` skill so our
> renderer-specific rules survive upstream syncs. Use it together with
> `remotion-best-practices` (general Remotion knowledge) — this skill adds the
> mistakes that specifically fail **POPJAM's** pipeline.

POPJAM renders every animation through a strict pipeline: **`tsc --noEmit` →
`eslint` → Remotion render**. If any stage fails, the whole render fails and the
work is wasted. The mistakes below are the ones that actually break renders in
production, ordered by how often they happen. Avoid all of them.

---

## 1. Declare or import every identifier (TS2304 "Cannot find name")

Every name you reference must be either imported or defined in the same scope.
Recurrent offenders:

- Remotion helpers used without importing them: `interpolate`, `spring`,
  `Easing`, `useCurrentFrame`, `useVideoConfig`, `Sequence`, `AbsoluteFill`,
  `Img`, `staticFile`.
- Constants referenced before/without declaration: `colors`, `COLORS`,
  scene constants like `SCENE_3_WAVEFORM_HEIGHTS`.

✅ Import everything from `remotion` you use, and define every constant you read:

```tsx
import { useCurrentFrame, useVideoConfig, interpolate, spring, Easing, Sequence, AbsoluteFill, Img, staticFile } from "remotion";

const COLORS = { primary: "#1B8EFB", accent: "#14816E" };
```

Before calling `render_animation`, mentally check that no identifier is used
that isn't imported or declared in that file.

---

## 2. Google Font module names are PascalCase with NO underscores (TS2307)

`import { loadFont } from "@remotion/google-fonts/<Family>"` resolves only when
`<Family>` is the family name **concatenated in PascalCase — spaces removed,
never replaced with underscores**:

| Font | ✅ Correct module | ❌ Fails TS2307 |
|---|---|---|
| Playfair Display | `PlayfairDisplay` | `Playfair_Display` |
| Open Sans | `OpenSans` | `Open_Sans` |
| Space Grotesk | `SpaceGrotesk` | `Space_Grotesk` |
| Roboto | `Roboto` | — |

> ⚠️ Underscore spellings (`Playfair_Display`, `Space_Grotesk`) have been the
> single most common `TS2307 Cannot find module` failure in production. There
> is **no** installed module with an underscore in its name.

Safe approach:

- Confirmed-working families: `Inter`, `Roboto`, `Montserrat`, `Poppins`,
  `OpenSans`, `Lato`, `Oswald`, `PlayfairDisplay`, `SpaceGrotesk`.
- If unsure a family is available, **use a web-safe font stack instead** —
  never risk a missing module:

```tsx
const fontFamily = "Arial, Helvetica, system-ui, sans-serif";
```

**A font-family stack may only LEAD with a font that actually exists in the
renderer** (the pre-render lint enforces this). The live preview runs in the
user's browser (macOS/Windows — every local font resolves); the MP4 renders in
a Linux container. A stack whose first family the container lacks shows the
real font in the preview and a silent substitute in the video — the classic
"the render doesn't use the same fonts as the preview" bug. Rules:

- ✅ Lead with the `fontFamily` returned by `loadFont()` (a loaded Google
  font), a **web-safe family** (`Arial`, `Arial Black`, `Georgia`, `Impact`,
  `Times New Roman`, `Trebuchet MS`, `Verdana`, `Comic Sans MS`,
  `Courier New` — installed in the renderer image), or a generic
  (`system-ui`, `sans-serif`).
- ❌ Never lead with a Google family you did NOT load (`"Montserrat,
  sans-serif"` without its `loadFont` import) — import
  `@remotion/google-fonts/Montserrat` instead.
- ❌ Never lead with an Apple/Windows-only family (`Helvetica Neue`,
  `SF Pro`, `Segoe UI`, `Futura`, `Avenir`, `Gill Sans`) — the container
  cannot ever have them.

**`loadFont()` signature (TS2345).** The FIRST argument is the style string;
options come second. Passing the options object first fails `tsc`:

```tsx
// ❌ WRONG — TS2345
const { fontFamily } = loadFont({ weights: ["400", "700"] });

// ✅ CORRECT
const { fontFamily } = loadFont("normal", { weights: ["400", "700"] });
```

**Never pass a `subsets` option (pre-render lint blocks it).** Each requested
subset becomes a `FontFace` clipped to that subset's unicode-range, so
`subsets: ["latin"]` drops every latin-ext glyph — Turkish `Ğ ğ İ Ş ş`,
Estonian `š ž`, Romanian `ă ț`, … render in a FALLBACK font in the final MP4
while the live preview (which always loads every subset) shows the brand font.
Omitting `subsets` loads all subsets the family ships and matches the preview
exactly; keep `weights` to limit download size.

```tsx
// ❌ WRONG — Turkish İ/ğ/ş silently fall back to a different font in the MP4
const { fontFamily } = loadFont("normal", { weights: ["400", "700"], subsets: ["latin"] });

// ✅ CORRECT — all subsets load; glyph coverage matches the live preview
const { fontFamily } = loadFont("normal", { weights: ["400", "700"] });
```

For deeper `loadFont()` guidance (weights), see the
`remotion-best-practices` skill's google-fonts rule — but IGNORE the
`subsets: ["latin"]` in its examples. That skill is synced verbatim from
upstream `remotion-dev/skills` (we cannot patch it), and its examples target
end-user websites where trimming subsets saves page weight. In POPJAM's
server-side renderer the saving is irrelevant and the clipped unicode-range
breaks localized copy — always omit `subsets` here; the pre-render lint
rejects it either way.

---

## 3. ASCII only in code (TS1127 "Invalid character")

Smart quotes (`“ ” ‘ ’`), non-breaking spaces, em-dashes pasted into code, and
other non-ASCII characters in source break the TypeScript parser. Use plain
ASCII `"` and `'` in code. (Unicode is fine **inside** rendered string values
like ad copy, just not in the code syntax itself.)

---

## 4. Make render deterministic — avoid "Output file not found after render"

A render that produces no output file usually means the composition threw or
hung at render time. Guard against it:

- **No top-level throws or side effects.** Code at module top level (outside the
  component) runs during bundling — a throw there aborts the whole render.
- **Bake all data into `<Composition defaultProps>`.** Do not fetch at render
  time; the renderer has no app network/auth context. Asset URLs must be public
  HTTPS and already verified.
- **Pure functions of `frame`.** No `Date.now()`, `Math.random()` without a
  seed, timers, or DOM measurement that can vary — non-determinism causes
  intermittent render failures.
- **Guard array/object access.** `.map()` over data baked into props; never
  index into something that can be `undefined` at frame 0.

---

## 5. The `eslint` stage can fail the render

`eslint` is a **stage** in the pipeline. Most eslint rules are warnings and
do not block the render, but a few categories do:

**IIFEs in JSX** — `@eslint-react/unsupported-syntax` rejects
`{(() => { ... })()}` style IIFEs ("IIFEs will not be optimized by React
Compiler").

❌ WRONG — fails eslint, fails the render:

```tsx
return (
  <AbsoluteFill>
    {(() => {
      const n = Math.floor(frame / 5);
      return <span>{n}</span>;
    })()}
  </AbsoluteFill>
);
```

✅ CORRECT — lift the logic into a `const` above the `return` (or a `.map()` /
small helper component), then reference the result in the markup:

```tsx
const n = Math.floor(frame / 5);
return (
  <AbsoluteFill>
    <span>{n}</span>
  </AbsoluteFill>
);
```

This applies to every IIFE form: `{(() => {...})()}`, `{((x) => ...)(y)}`,
`{(function () {...})()}`. (A module-scope IIFE like
`const config = (() => {...})()` is fine — the rule is JSX-specific.)

**`no-useless-assignment`** — assigning a value you never read trips the rule.
This usually means a particle/wave/timeline calculation whose result you
forgot to render, or a value you recompute inline instead of using the variable.

❌ `const x = p.x + amp; return <div style={{ left: p.x }} />;` (`x` unused)
✅ Either use the variable (`left: x`) or delete the assignment.

> **Note on preview parity.** The frontend live preview lints with
> `eslint-plugin-only-warn` registered globally, so the same rule there is a
> warning and the preview keeps rendering. The renderer's eslint matches this
> behaviour. Warnings (severity 1) are surfaced back to the caller in the
> render result for diagnostics, but they do not fail the render — only
> severity-2 errors do. Treat the warnings as guidance for the *next* render,
> not as a reason to re-render this turn.

---

## 6. Composition prop typing (avoids TS2322 "Type not assignable")

`React.FC` on the root scene component must accept a permissive prop shape
(`Record<string, unknown>`) and cast individual props inside. A typed prop
interface on the root breaks `<Composition>`'s generic-typed `component` prop.
Sub-components may use their own typed props freely.

```tsx
export const MainScene: React.FC<Record<string, unknown>> = (props) => {
    const title = (props.title as string) || '';
};
```

> If you see TS2322 errors pointing at the root component's prop type, this is
> the fix.

---

## 7. Font must cover the content's language — language-specific glyphs and casing

A font that renders Latin English fine can still drop or tofu glyphs for
other languages, and more importantly, **case-folding rules differ per
language**. Picking a font (or applying `.toUpperCase()`/`.toLowerCase()`)
without checking the language produces broken, unprofessional output:

- **Turkish:** uppercase `i` → `İ` (U+0130, dotted capital I), **not** `I`.
  Lowercase `I` → `ı` (U+0131, dotless i), **not** `i`. The characters `İ`/`ı`
  are distinct code points; most Latin fonts omit them or render a generic
  fallback. Also check `ğ ş ç ö ü`.
- **German:** uppercase `ß` → `ẞ` (U+1E9E) or `SS` depending on style; `ä ö ü`.
- **Nordic:** `æ ø å` / `Æ Ø Å`.
- **Vietnamese:** `đ ơ ư` and precomposed diacritics that many Latin fonts lack.
- **Arabic / Hebrew / Cyrillic / CJK:** require fonts with the matching script
  coverage; do not assume a Latin family includes them.

Rules:

1. **Never pass `subsets` to `loadFont()`** — omit the option entirely so
   every subset the family ships is loaded (`latin-ext`, `vietnamese`,
   `cyrillic`, …). Restricting subsets clips glyph coverage to their
   unicode-ranges and is the #1 cause of Turkish/Estonian characters
   rendering in a fallback font in the MP4 while the preview looks correct.
   (The pre-render lint blocks any `subsets:` option.)
2. **Never call `.toUpperCase()` / `.toLowerCase()` blindly** — use a
   language-aware transform (or pass the already-cased string in from the
   agent) so Turkish `i`→`İ` and `I`→`ı` are honored. JS `String.toUpperCase`
   does **not** apply Turkish/Azeri casing rules.
3. **Prefer a known wide-coverage family** (`Inter`, `Noto Sans`, `Roboto`,
   `Open Sans`) over display/narrow fonts when the content has diacritics or
   non-Latin characters. `Oswald`, `Playfair_Display`, etc. frequently lack
   `latin-ext`.
4. When in doubt, **system-ui** has broad coverage; fall back to it rather
   than shipping a font that tofus the copy.

This won't fail `tsc`/`eslint`, but it produces visibly broken renders that
get rejected downstream.

---

## 8. Only `scale` / `translate` / `rotate` exist as standalone style props (TS2353 / TS2561 / TS2783)

CSS has exactly three standalone transform properties: `scale`, `translate`,
and `rotate`. Everything else — `scaleX`, `scaleY`, `skew`, `skewX`, `skewY`,
`rotateX`, `rotateY`, `rotateZ`, `translateX`, `translateY` — is **not** a CSS
property and fails `tsc` when used as a style key ("Object literal may only
specify known properties"). Put those inside a single `transform` string:

```tsx
// ❌ WRONG — TS2353/TS2561: 'skewY' / 'scaleX' do not exist in Properties
style={{ skewY: `${tilt}deg`, scaleX: stretch }}

// ✅ CORRECT — one transform string for anything beyond scale/translate/rotate
style={{ transform: `skewY(${tilt}deg) scaleX(${stretch})` }}

// ✅ ALSO CORRECT — the three real standalone props
style={{ scale: String(s), translate: `0px ${y}px`, rotate: `${r}deg` }}
```

Never set both a standalone prop AND `transform`, and never specify `transform`
twice in one object (TS2783 "'transform' is specified more than once") — merge
every function into a single `transform` string.

---

## 9. Remotion hooks only inside components rendered by the Composition

`useCurrentFrame()` / `useVideoConfig()` are React hooks. Calling them at
module scope, inside a plain helper function, or inside a `.map()` callback
that isn't a component crashes the render at runtime
("useCurrentFrame() can only be called inside a component that was rendered by
Remotion"). `tsc` and `eslint` do NOT catch every case — the render just dies.

```tsx
// ❌ WRONG — module scope
const frame = useCurrentFrame();

// ❌ WRONG — plain helper invoked from JSX
const barHeight = (i: number) => interpolate(useCurrentFrame(), [0, 30], [0, i]);

// ✅ CORRECT — call the hook ONCE at the top of the component, pass the value down
const Scene: React.FC<Record<string, unknown>> = () => {
  const frame = useCurrentFrame();
  const barHeight = (i: number) => interpolate(frame, [0, 30], [0, i]);
  ...
};
```

---

## 10. Inline styles only — no Tailwind / className utilities

Style every element with inline `style={{ ... }}` objects. The server renderer
happens to process Tailwind classes, but the in-app live preview does NOT — a
`className="flex items-center gap-4"` creative looks correct in the final MP4
while the user's live preview shows unstyled content. Inline styles render
identically in both. (Using `className` as a semantic hook is fine; just never
rely on it for styling.)

---

## 11. `<Composition>` numeric props must be literal numbers

`width`, `height`, `fps`, and `durationInFrames` on the `<Composition>` element
must be written as **literal integers** (`durationInFrames={450}`), never
constants or expressions (`durationInFrames={TOTAL_FRAMES}`,
`durationInFrames={15 * 30}`). POPJAM tooling statically parses these values to
drive the frontend live-preview Player and stored metadata — an expression
parses as the default (300 frames / 1080x1920) and the preview plays the wrong
duration even though the MP4 renders fine. Compute the number yourself and
write the result.

---

## Pre-render self-check (run through this before `render_animation`)

1. Every identifier is imported or declared (no stray `colors`, `interpolate`…).
2. Every `@remotion/google-fonts/*` import is PascalCase with NO underscores
   (`PlayfairDisplay`, not `Playfair_Display`) and a real installed family,
   else a web-safe stack (`Arial, Helvetica, system-ui, sans-serif`);
   `loadFont("normal", {...})` — style string first. Every font stack LEADS
   with a loaded Google font, a web-safe family, or a generic — never an
   unloaded/OS-only family.
3. Code is ASCII-only (smart quotes live only inside rendered strings).
4. No top-level throws; all data baked into `defaultProps`; render is pure.
5. No IIFEs in JSX — lift inline logic into a `const`/helper above `return`;
   every variable you compute is actually read (no `no-useless-assignment`).
6. Root scene component is typed `React.FC<Record<string, unknown>>` and casts
   props inside.
7. Font covers the content's language: NO `subsets` option on `loadFont()`
   (all subsets must load — `subsets: ["latin"]` drops Turkish `İ ğ ş`),
   language-aware casing (no blind `.toUpperCase()` for Turkish `İ`/`ı`),
   fallback to a wide-coverage family or `system-ui` if unsure.
8. Transforms: only `scale`/`translate`/`rotate` as standalone style props —
   `skewY`, `scaleX`, etc. go inside ONE `transform` string, never duplicated.
9. `useCurrentFrame()`/`useVideoConfig()` called only at the top of components,
   never module scope or plain helpers.
10. All styling is inline `style={{ ... }}` — no Tailwind/className utilities
    (the live preview doesn't process them; the render does — they'd diverge).
11. `<Composition>` `width`/`height`/`fps`/`durationInFrames` are literal
    integers, not constants or expressions.
