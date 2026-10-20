# Contemporary flat vector illustration (Dribbble style, 2026)

> Adapted from huashu-art-motion (MIT, (c) 2026 alchaincyf) - references/风格配方/16_2026.md

Layer: material (works on any subject) - Upstream quality: ★★★ - Known weakness: none recorded; its strength is character acting.

## Look
Flat colour blocks, no outlines; form only through a one-step-darker block of the same hue (a diagonal highlight #f08b7d on coral #e8655a; a darker arc on a limb). Grain stippling makes the gradients. Big heads (head 1.2x around the neck). Palette: wall #f6efe2, floor #eedfc7, navy #262a5c, coral #e8655a / #f08b7d / #d1514a, pink #f5cdc6 + dots #e8807b, lavender #e4dbf6 + dots #b9a4ea, yellow #f2b33d, greens #2f8a5d / #22704a / #57b07a, mint #d6ece0, skin #f8d3bd / #eab79f, hair #f4c24f, blush #f39a8d, orange #f0a23c / #d8832a.

## Build it in Remotion
SVG suits flat shapes; canvas for heavy dot counts. px at 1920 wide; scale with the canvas.
- Stipple: ~0.02 candidates per px^2 inside a shape, kept where random(seed + i) < density(x, y); 2px squares sized x0.6-1.4. Density is a function of position, e.g. denser downward: 0.12 + 0.75*clamp((y - cy + 120)/420). Precompute in useMemo; one `<path>` per colour ("M x y h2 v2 h-2 z ...") or a baked canvas.
- Character grain: a static texture (5% dark dots alpha 70/255, 3.5% light dots 90/255) clipped to the characters only (canvas source-atop, or a pattern inside the character clipPath).
- Lamp light cone: ~26000 dots, width 56 -> 150px down 420px, alpha fading with distance, denser at the centre; bake to a 340x420 image and rotate it with the lamp.
- Rigs: 2-bone IK arms (150/140px) blending between target sets; expressions as discrete swaps (closed-eye smile -> dot eyes + small "o" mouth popping on outBack -> big eyes + open mouth -> wink "<").

## Make it move
Upstream acting beats at 30 fps (generalized: a secondary character leaps onto a surface and swats an object off):
- Anticipation 2 frames: sy 1 -> 0.86, sx 1 -> 1.07, head down 8px. Push-off ~2 frames: pivot moves from feet to centre of mass, rot -> -0.75, sy 1.12, 45% blend into the leap pose. Arc 11 frames on a Catmull-Rom path, rot = tangent angle x 0.8, levelling over the last 3 frames; mid-flight sx 1.12 / sy 0.9. Take-off dust: 4 beige puffs expand and fade over 4 frames.
- Landing 3 frames: sy 0.86 -> 0.70, sx 1.18, feet pinned. On the flattest frame snap the facing (scaleX sign) - cleaner than a 2-3 frame paper flip. Settle 4 frames: sy 0.96 -> 1.07 -> 1.0.
- Swat: anticipation 3-4 frames, strike 2, hold 2, recover 4; three short motion lines spread and fade over 6 frames. Lean 0.1 + 0.28*clamp(distance to target).
- Fall ~10 frames: gravity ~7 px/frame^2, rotation -0.12 - 2.3*q^1.3, 6 trailing droplets from past positions, shrinking. Impact: 7 radial lines fade over 4 frames; 2 shards and 9 crumbs on parabolas, each stopping where it lands; a spill widening 140 -> 220 -> 235px (ease-out, ~0.15 s); two grey ripples to 560/460px, gone within ~0.4 s.
- Reaction: 3 tension lines pop above the head (outBack), pale pink -> red in 2 frames, then jitter +-2.5px every frame, head +-2px.
- Secondary motion from each impact frame f0: damped(f) = amp*exp(-(f - f0)/decay)*sin(2*PI*(f - f0)/period). Lamp 0.055 rad, period 13, decay 11 frames; plant sway 0.035 / 11 / 9, plant shake 0.05 / 4.5 / 13.
- Ambient: clouds 15 px/s, a plane 177 px/s with a dashed trail, sun rays 0.35 rad/s, decorative symbols boiling at 4 fps (+-1.5px, +-0.09 rad; seed random() with Math.floor(frame * 4 / 30)).

## Signature transition
Iris: three concentric rings - navy rgb(33,42,81), coral rgb(234,124,107), cream rgb(250,246,235), 137px each - expand linearly from the hero object (~290 px/frame); the innermost circle shows the new shot. Upstream 0.18 s (5-6 frames). Pattern for any custom presentation:

```tsx
import {AbsoluteFill} from 'remotion';
import type {TransitionPresentation, TransitionPresentationComponentProps} from '@remotion/transitions';

type IrisProps = {cx: number; cy: number; maxR: number}; // maxR = distance to farthest corner
const RINGS = ['rgb(33,42,81)', 'rgb(234,124,107)', 'rgb(250,246,235)'];

const Iris = ({children, presentationDirection, presentationProgress: p, passedProps}: TransitionPresentationComponentProps<IrisProps>) => {
  const {cx, cy, maxR} = passedProps;
  const R = 19 + p * (maxR + 411);
  if (presentationDirection === 'exiting') {
    return (
      <AbsoluteFill>
        {children}
        <svg width="100%" height="100%" style={{position: 'absolute', inset: 0}}>
          {RINGS.map((c, i) => <circle key={c} cx={cx} cy={cy} r={Math.max(0, R - i * 137)} fill={c} />)}
        </svg>
      </AbsoluteFill>
    );
  }
  const ri = Math.max(0, R - 411);
  return <AbsoluteFill style={{clipPath: `circle(${ri}px at ${cx}px ${cy}px)`}}>{children}</AbsoluteFill>;
};
export const iris = (props: IrisProps): TransitionPresentation<IrisProps> => ({component: Iris, props});
// <TransitionSeries.Transition presentation={iris({...})} timing={linearTiming({durationInFrames: 6})} />
```

End-card extra: a handwritten sign-off (Caveat 600, tilted -0.03 rad) revealed by a clip edge travelling over ~14 frames, with an underline of 24 segments tapering 3.4 -> 1.4px drawn by the same front.

## Pitfalls
- Aim after the lean: apply the lean, then map the target into local coordinates with the inverse matrix (`DOMMatrix.inverse().transformPoint`). Aiming in unleaned coordinates put the paw ~60px into the table at 0.38 rad.
- Squash about the centre lifts the feet; pivot at the feet (centre of mass only while airborne).
- Precompute stipples; never regenerate per frame.
