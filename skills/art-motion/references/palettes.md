# Palettes: one piece, one palette

> Adapted from huashu-art-motion (MIT, (c) 2026 alchaincyf) - references/色板.md

Pick one palette before planning and write it on the shot list's Palette line (see `directing.md`). Keep it in one `const P = {...}` object and reference every colour through it. Lightness and opacity may vary; no new hues.

## Off-limits: the blue-purple default

Blue-purple gradient grounds, deep-purple starfields, neon cyan-violet glow, purple frosted glass. These are the colours AI animation falls into by default and viewers read them as "made by AI"; the author called them AI slop.

The rule: a colour is blue-purple when its hue is 225-300 deg and saturation >= 0.30. A frame where 30% or more is blue-purple counts as a blue-purple frame; more than 30% of such frames in a piece = AI look, failed. The only exception is a subject that demands it (the brand's own colour, a brief naming cyberpunk purple or a Starry Night tribute); say why in a code comment.

Flat navy (hue ~210 deg, `navy` below) is allowed: a deliberate single ground, no gradient, no glow.

## Eight ready palettes

Roles: `bg` ground, `surface` card / paper / panel, `ink` main text, `sub` secondary text and fine lines, `accent` main accent, `accent2` second accent.

| Name | Suits | bg | surface | ink | sub | accent | accent2 |
|---|---|---|---|---|---|---|---|
| `paper` | culture, history, books, explaining an idea | #F3EDE2 | #FBF8F2 | #1B1A17 | #6B655B | #C8402F | #2F5D62 |
| `poster` | opinion, conflict, one line hammered home | #FFD23F | #FFF6D6 | #111111 | #4A4433 | #FF5A36 | #14213D |
| `ink` | tech, night, serious topics | #121417 | #1E2226 | #F2EFE8 | #A39E93 | #F2B33D | #5FB3A1 |
| `navy` | products, data, phones and devices (flat, never gradient) | #0D1B2A | #16293D | #EEF3F6 | #8FA3B3 | #5CC8E0 | #F2A93B |
| `bauhaus` | design, structure, geometry, process | #EFE9DD | #FFFFFF | #111111 | #555555 | #D62828 | #1D4E89 |
| `snow` | winter, health, cleaning, lab | #E9EEF0 | #FFFFFF | #1F2A30 | #5E6B72 | #D9482B | #3E7C8C |
| `wood` | home, kitchen, handmade, everyday life | #EDE3D1 | #F7F1E6 | #2B2622 | #7A6E62 | #C4552D | #3F5B4B |
| `chalk` | classroom, derivations, formulas | #23302B | #2E3D37 | #F1EFE6 | #A9B3AA | #F4D35E | #E87D5A |

## Rolling your own

- 3-6 colours: a ground, a surface, a main ink, a secondary ink, one or two accents. Within a shot the accent points at one thing only.
- Decide the ground first: light (paper, snow, wood) or dark (ink, navy, chalk). Never jump between light and dark during the piece.
- Keep the blue-purple zone out of grounds and large areas.
- No gradient grounds, no neon outer glow. For depth use paper texture, grain (`@remotion/noise`) or two flat value layers.
- With real material (screenshots, photos), take one or two accents from the material; the ground still comes from the palette.

## Brand palettes

Map brand colours into the roles; keep the style's value structure:

- **Roles**: main brand colour -> `accent` (exact hex), second -> `accent2`; `bg` and `surface` from the brand's neutrals or the style's palette tinted slightly towards the brand hue; `ink` = the brand's text colour or a high-contrast near-black / near-white.
- **Value structure**: on a light-ground style (paper, wood) a saturated brand colour stays an accent or a block, not the full-frame ground. It becomes the ground only in a colour-field style (`poster`) or when the brand is known for that field.
- **Blue-purple brands**: the brand colour wins, but flat: as an accent or a flat block, no gradient, no glow; say so in a code comment.
- **Never recolour the real logo.** Embed the supplied file with `<Img>` exactly as given: no tint, filter, blend mode or grain over it. Choose the logo variant (light or dark) that suits the ground; if contrast is still poor, put it on a `surface` plate. Product photos are not graded to the palette either; the palette makes room for them.

## Self-check

Line up one preview frame per shot. Is the ground in the same lightness band throughout? Only one or two accents? Does any shot suddenly show another film's colours (a white bar chart, a purple starfield, a neon border)? Redraw that shot in the palette.
