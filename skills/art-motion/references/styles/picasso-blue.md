# Blue Period (Pablo Picasso, 1901-1904)

> Adapted from huashu-art-motion (MIT, (c) 2026 alchaincyf) - references/风格配方/36_picasso_blue.md

Layer: era specimen (best for homage, journeys, era-hopping) - Upstream quality: ★★ - Known weakness: forms not melancholic enough.

Evoke the technique; never copy a specific work or character.

## Look
Strict blue monochrome, broad dry low-contrast strokes softened by blur, faint dry-brush filaments, a firm Prussian-blue contour that never wobbles, elongated figures with long fingers, shawls, downcast heads, slow breathing. Quiet, nocturnal, melancholy.
- Palette: #132240 / #1d3866 / #2d5a94 / #6b8fb6 / #b6c8d8, blue-grey #3b6878; contour #0c1830.
- Separate materials by value only: mid #4f719a, dark #273f66, light #b6c8d8. Blond = brightest blue-grey #cbd8e0 over skin #90a9be (one step brighter than skin reads as blond).

## Build it in Remotion
Px at 1920 wide; scale with the canvas.
1. Blue flat base (walls, floor, a night sea and moon through an opening).
2. Wide dry strokes (canvas, cached): walls cell 34, length 110, width 34, jitter 4, near-vertical +-0.5 * noise2D at frequency 0.003, palette mix 0.8; floor the same, horizontal. Then blur 7 px at alpha .8, then ~900 dry-brush filaments (alpha .07, length 30-90).
3. Frames and furniture on their own layer after the strokes, with their own small strokes; never cut holes in the stroke layer.
4. Static Prussian-blue environment contour.
5. Elongate figures: `transform: 'scale(0.84, 1.12)'` with `transformOrigin` at the feet (secondary subject 0.82 x 1.14), applied to everything of the figure - fill, strokes, contour - or the outline slips off. Small strokes + a cool light gradient, a 5 px #0c1830 contour, shawl folds rgba(20,40,80,.6) 4 px. Long fingers: thin 22 x 4.5 ellipses around a held object.
6. Canvas texture and a cool vignette last. Cheap once cached; only the figure and a few motifs animate.
7. Brand colour cannot exist here: keep the real logo on an end card outside the blue pass, or (only if the brand allows) map it to blue by luminance with `feColorMatrix`, fully legible.

## Make it move
Slow everything down.
- Breathing: sin(1.8t) * 0.026 scale (about 2x the amplitude, 0.45x the frequency of a normal idle).
- The main action takes 1.25 s where a normal one takes 0.9 s; steam rises at half speed.
- Background: waves slide sideways, faster nearer the viewer (20 + 0.25 * (y - 400) px/s); 14 moonlight glints flicker; one pale cloud crosses the moon.

## Signature transition
Drain to blue, then a wide dry brush, 0.42 s (13 frames): the old shot loses its colour to blue, then 6 broad brush bands sweep left to right revealing the new shot, bristle streaks trailing each head. Recipe: ../transitions.md (blueBrush).

## Pitfalls
- Ochre accents broke the monochrome; stay all blue, separate by value.
- Cell 16 / length 40 / width 14 vertical wall strokes read as rain or a blanket - Impressionism. Go wide, long, low-contrast, then blur.
- Dense wide round-capped strokes look like rows of heads; the blur hides it, square or tapered ends fix it.
- A rectangle masked out of the strokes for a table left a flat patch on the floor; furniture is its own layer.
- Not melancholic enough (the weakness): elongate further, droop heads and shoulders, lower the gaze, bring hands toward the face, slow every motion.
