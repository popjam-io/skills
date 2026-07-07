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

## 2. Google Font imports must use the exact, installed module (TS2307)

`import { loadFont } from "@remotion/google-fonts/<Family>"` only resolves for
font families that actually exist as modules **in this renderer** (underscores
for spaces, exact casing, e.g. `Roboto`, `Montserrat`, `Inter`, `Poppins`).
Guessing a family name that isn't installed fails with
`Cannot find module '@remotion/google-fonts/<Family>'`.

> ⚠️ **`Space_Grotesk` does NOT resolve in our renderer.** It has been the
> single most common `TS2307 Cannot find module` failure. Do not import it.
> Fall back to the system stack below.

Safe approach:

- Stick to confirmed-working families: `Inter`, `Roboto`, `Montserrat`,
  `Poppins`, `Open_Sans`, `Lato`, `Oswald`, `Playfair_Display`.
- If unsure a family is available, **use a system font stack instead** — never
  risk a missing module:

```tsx
const fontFamily = "'Inter', system-ui, -apple-system, Helvetica, Arial, sans-serif";
```

For correct `loadFont()` usage (weights, subsets), see the `remotion-best-practices`
skill's google-fonts guidance.

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

1. **Check the content language before choosing the font.** If `loadFont()`
   accepts a `subsets` option, include the matching subset (e.g. `latin-ext`,
   `vietnamese`, `cyrillic`); if unsure, request **all subsets** rather than
   the default `latin` only.
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

## Pre-render self-check (run through this before `render_animation`)

1. Every identifier is imported or declared (no stray `colors`, `interpolate`…).
2. Every `@remotion/google-fonts/*` import is a real family (never
   `Space_Grotesk`), else system stack.
3. Code is ASCII-only (smart quotes live only inside rendered strings).
4. No top-level throws; all data baked into `defaultProps`; render is pure.
5. No IIFEs in JSX — lift inline logic into a `const`/helper above `return`;
   every variable you compute is actually read (no `no-useless-assignment`).
6. Root scene component is typed `React.FC<Record<string, unknown>>` and casts
   props inside.
7. Font covers the content's language: matching `subsets` requested, language-
   aware casing (no blind `.toUpperCase()` for Turkish `İ`/`ı`), fallback to a
   wide-coverage family or `system-ui` if unsure.
