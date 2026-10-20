# Munch expressionism (The Scream era, 1893)

> Adapted from huashu-art-motion (MIT, (c) 2026 alchaincyf) - references/风格配方/19_munch.md

Layer: era specimen (best for homage, journeys, era-hopping) - Upstream quality: ★★ - Known weakness: the wall once read as Van Gogh.

## Look
Long, thin, translucent strokes (200-300px) along a writhing field over flat underpaint; the whole world sways together; a blood-orange banded sky. Sky #e2541c #f08a24 #f4c03a #c8301e #e8743a #f6a63a #b82a1e; wall #a8401e -> #5a1a14; sickly face shadow rgba(120,150,70,.4) blurred 8px.

## Build it in Remotion
Canvas; px at 1920 wide; scale with the canvas.
- Underpaint each region flat in its colour family so gaps show colour, not black.
- Seeds on a 24px jittered grid (~3600), tagged by region, integrated through a time-varying field. [steps, step px, width, alpha]: sky [32,7,10,.78], water [26,6,9,.78], wall [42,7,13,.5], floor [32,8,12,.55], +0-8 random steps. Stop at the region edge. No outline.
- Fields: sky 0.55*sin(x*.011 + y*.018 - 2.4t); water: tangent round a whirl centre; wall: vertical, +-0.5 rad sine twist; floor: toward the vanishing point.
- Sky colour from a wavy y: y + 22*sin(x*.014 - 2.2t), 28px bands cycling the 7 colours - the bands twist, the sky flows.
- World warp (last pass): copy the offscreen scene in 4px rows shifted 9*sin(y*.012 + 4.2t) + 4*sin(y*.031 - 6t), then 4px columns shifted 6*sin(x*.009 - 3.6t). Everything sways together, far cheaper than wobbly drawing:

```tsx
const warpRows = (ctx: CanvasRenderingContext2D, src: HTMLCanvasElement, t: number, m = 14) => {
  for (let y = 0; y < src.height; y += 4) {
    const dx = 9 * Math.sin(y * 0.012 + 4.2 * t) + 4 * Math.sin(y * 0.031 - 6 * t);
    ctx.drawImage(src, 0, y, src.width, 4, dx - m, y, src.width + 2 * m, 4); // margin m >= max shift
  }
};
```

- Heaviest card here (~100k segments a frame). For preview: 32px seeds, half-res strokes, stroke field recomputed at 10 fps (`Math.floor(frame / 3)`), warp every frame.

## Make it move
- Everything flows (main action); the warp keeps static things alive.
- Hands to cheeks, mouth 7 + 2*sin(9t) px, sway sin(3.2t)*0.12 rad, 9 hair strands sin(9q - 7t). Borrow the gesture; never redraw the famous painting.
- Wavy furniture legs; a secondary character with mouth ajar, caught by the scream.
- Captions through the same warp; IM Fell English worked, a comic hand (Kalam) broke the mood.

## Signature transition
Scream warp: the old shot row-warps with growing amplitude (70e*sin(y*.014 + ph) + 20e*sin(y*.05 - ph)); a wavy front descends (lerp(-180, H + 220, e) + 80*sin(x*.0055 + 7p)); above it the new shot, warp shrinking 60(1 - e); four 26px bands #b82a1e #e2541c #f08a24 #f4c03a ride the front 22px apart; gaps #3a1410. 0.5 s (15 frames). One canvas for both shots, or a custom presentation (see flat-illustration.md) with a polygon clip and SVG bands.

## Pitfalls
- Dark outlines and short strokes = Van Gogh: lengthen (10 -> 26+ steps), widen, lower opacity.
- Unstretched warp strips leave dark edge gaps.
- Draw raised near limbs after the flow strokes so torso strokes don't cross them.
