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
production, ordered by how often they happen. Avoid all of them. Several are
additionally enforced by a pre-render lint (`popjam.utils.render_lint`) that
raises `ModelRetry` before a render is attempted — treat a lint message as a hard
fix-it, not a suggestion.

---

## 1. Never interpolate into a `transform` string (most common runtime crash)

Remotion parses CSS transforms and chokes on interpolated `transform` template
strings — most often `rotate`. This passes `tsc` and `eslint` but **crashes at
render time** ("invalid rotate value" / `parseStringInterpolationComponent`).

❌ WRONG — crashes the render:

```tsx
style={{ transform: `rotate(${-knobRotation + 30}deg)` }}
style={{ transform: `scale(${s}) translateY(${y}px)` }}
```

✅ CORRECT — use individual CSS transform properties:

```tsx
style={{ rotate: `${-knobRotation + 30}deg` }}
style={{ scale: s, translate: `0px ${y}px` }}
```

When you must combine transforms, set each property separately (`rotate`,
`scale`, `translate`) rather than composing one `transform` string. Always feed
`interpolate()` numbers, then attach the unit:

```tsx
const deg = interpolate(frame, [0, 30], [0, 90], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
return <div style={{ rotate: `${deg}deg` }} />;
```

*(Enforced by the pre-render lint.)*

---

## 2. Declare or import every identifier (TS2304 "Cannot find name")

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

## 3. Google Font imports must use the exact, installed module (TS2307)

`import { loadFont } from "@remotion/google-fonts/<Family>"` only resolves for
font families that actually exist as modules **in this renderer** (underscores
for spaces, exact casing, e.g. `Roboto`, `Montserrat`, `Inter`, `Poppins`).
Guessing a family name that isn't installed fails with
`Cannot find module '@remotion/google-fonts/<Family>'`.

> ⚠️ **`Space_Grotesk` does NOT resolve in our renderer.** It was every single
> `TS2307 Cannot find module` failure over the last 14 days. Do not import it.
> The pre-render lint blocks it. (If a different family also starts failing
> TS2307, treat it the same way and fall back to the system stack below.)

Safe approach:

- Stick to confirmed-working families: `Inter`, `Roboto`, `Montserrat`,
  `Poppins`, `Open_Sans`, `Lato`, `Oswald`, `Playfair_Display`.
- If unsure a family is available, **use a system font stack instead** — never
  risk a missing module:

```tsx
const fontFamily = "'Inter', system-ui, -apple-system, Helvetica, Arial, sans-serif";
```

For correct `loadFont()` usage (weights, subsets), see the `remotion-best-practices`
skill's google-fonts guidance. *(Broken-family imports are caught by the
pre-render lint.)*

---

## 4. Use valid CSS value types (TS2322 "Type not assignable")

React's `CSSProperties` types are strict. The recurring failure is
`fontWeight`. When you `loadFont()` a google font, its typed weight union only
contains the weights that font actually ships (commonly `"400" | "500" | "600" |
"700"`), so requesting a heavier weight as a quoted string fails with e.g.
`Type '"800"' is not assignable to type '"400" | "500" | "600" | "700"'`.

❌ `fontWeight: "800"` / `fontWeight: "900"` (weight the loaded font doesn't ship)
✅ `fontWeight: "700"` (an available weight) — or `fontWeight: "bold"` /
   `fontWeight: 800` (number) — or request the weight explicitly:
   `loadFont("normal", { weights: ["400", "800"] })`.

The pre-render lint blocks quoted `"800"`/`"900"`. Same idea for other typed
props: pass numbers where numbers are expected, and only use string literals the
type allows.

---

## 5. Don't add unknown style properties (TS2353)

`Object literal may only specify known properties` means you put a non-CSS key
(or a typo) inside a `style` object, or extra keys on a typed component prop.
Keep `style` objects to real, camelCased CSS properties only.

---

## 6. ASCII only in code (TS1127 "Invalid character")

Smart quotes (`“ ” ‘ ’`), non-breaking spaces, em-dashes pasted into code, and
other non-ASCII characters in source break the TypeScript parser. Use plain
ASCII `"` and `'` in code. (Unicode is fine **inside** rendered string values
like ad copy, just not in the code syntax itself.)

---

## 7. Make render deterministic — avoid "Output file not found after render"

A render that produces no output file usually means the composition threw or
hung at render time. Guard against it:

- **No top-level throws or side effects.** Code at module top level (outside the
  component) runs during bundling — a throw there aborts the whole render.
- **Bake all data into `<Composition defaultProps>`.** Do not fetch at render
  time; the renderer has no app network/auth context. Asset URLs must be public
  HTTPS and already verified (`check_image`).
- **Pure functions of `frame`.** No `Date.now()`, `Math.random()` without a
  seed, timers, or DOM measurement that can vary — non-determinism causes
  intermittent render failures.
- **Guard array/object access.** `.map()` over data baked into props; never
  index into something that can be `undefined` at frame 0.

---

## 8. The `eslint` stage fails the render too — no IIFEs in JSX

`eslint` is a **hard stage** in the pipeline, not advisory: an eslint *error*
fails the whole render exactly like a `tsc` error. Two rules recur in production
(Logfire, 14d) and are 100% avoidable.

**`@eslint-react/unsupported-syntax` — no immediately-invoked function
expressions (IIFEs) in JSX.** Wrapping inline logic in a self-calling function
inside JSX is rejected ("IIFEs will not be optimized by React Compiler"). The
pre-render lint blocks this.

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

**`no-useless-assignment` — don't compute a value you never read.** A variable
that is assigned but not used in any later statement fails eslint. This usually
means a particle/wave/timeline calculation whose result you forgot to render, or
a value you recompute inline instead of using the variable.

❌ `const x = p.x + amp; return <div style={{ left: p.x }} />;` (`x` unused)
✅ Either use the variable (`left: x`) or delete the assignment.

---

## Pre-render self-check (run through this before `render_animation`)

1. No interpolated `transform` strings — used `rotate`/`scale`/`translate` props.
2. Every identifier is imported or declared (no stray `colors`, `interpolate`…).
3. Every `@remotion/google-fonts/*` import is a real family (never `Space_Grotesk`), else system stack.
4. `fontWeight` is an available weight / number, not `"800"`/`"900"`.
5. `style` objects contain only real camelCased CSS keys.
6. Code is ASCII-only (smart quotes live only inside rendered strings).
7. No top-level throws; all data baked into `defaultProps`; render is pure.
8. No IIFEs in JSX — lift inline logic into a `const`/helper above `return`;
   every variable you compute is actually read (no `no-useless-assignment`).
