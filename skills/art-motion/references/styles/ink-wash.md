# Chinese freehand ink painting (xieyi; Bada Shanren, Qi Baishi)

> Adapted from huashu-art-motion (MIT, (c) 2026 alchaincyf) - references/风格配方/17_ink.md

Layer: material (works on any subject) - Upstream quality: ★★ - Known weakness: figures not freehand enough (review 6/10) - vector figures with washes, not brushwork.

## Look
Paper is the ground and ink only adds (unlike oil, where paint covers). Calligraphic strokes swelling with pressure and breaking into dry-brush "flying white"; washes bleeding with soft halos; generous empty paper; whites reserved, never painted; one red seal. Ink rgb(16,14,12) in five tones: scorched .9, thick .8, heavy .6, light .35, clear .15. Ochre #c47a3c; indigo #6f8aa0 / #7d97ab; gamboge rgba(226,170,52,.75) (multiply); carmine rgb(190,40,40) for exactly three accents; vermilion sun #d8553f; seal #c4281e.

## Build it in Remotion
Canvas; px at 1920 wide; scale with the canvas. Order: paper (cached) -> washes (hills, sun) -> mist -> static strokes (cached once written) -> plants -> subjects -> steam threads -> seal.
- Paper: #efe6d0, low-frequency noise (scale .0025, amplitude 9), grain 7, 2600 short fibre arcs (half brown alpha .05-.13, half light .12-.27), vignette to .22. Build once.
- Brush: Catmull-Rom densify, resample at 4px equal arc length (else the dry-brush noise frequency varies with stroke length). Pressure prof(q) = smoothstep(0, head, q) * (1 - 0.7*smoothstep(1 - tail, 1, q)) * (0.85 + 0.15*noise). Wet core: ribbon of width w*prof*(1 - 0.85*dry*q^0.8), alpha tone*0.72 (thins as ink runs out). Bristles: continuous polylines offset +-0.475*w*prof, broken where noise2D(seed, k*1.9, i*0.09) < dry*q^1.2*0.95 + 0.05 - the gaps are flying white.
- Settings: frames w 14-18, dry .45-.6; heavy horizontals w 22; drapery w 4-6, dry .3-.4, tone .78; ground line w 5, dry .85, tone .35.
- Washes: shape on a scratch canvas, multiplied on twice - halo blur(halo*(0.4 + grow)) at alpha haloA*grow, then body blur(blur*(1.6 - 0.6*grow)); grow 0 -> 1 bleeds it in from nothing and keeps the halo widening. Halo 12 (alpha .6) figure, 9 (.78) animal, 14 hills. Blur is the cost: wash at 1/2-1/4 res and scale up, or SVG feGaussianBlur + `mix-blend-mode: multiply`.
- Reserved white: cut light areas (muzzle, chest, inner collar) out of the wash with destination-out. Faces: paper fill + 1.8px scorched outline.

## Make it move
- Write-on (main action): reveal_i = smoothstep(d_i, d_i + l_i, progress) in a planned order; upstream took 0.45 s, give it 1-2 s in an ad. Start slightly in (upstream +0.12 s): a blank first frame is a bad cover.
- Bamboo: pale jointed stem swaying sin(2.9t)*0.11 rad, more toward the tip; 5 three-leaf clusters (L 110, w 15) fluttering sin(7t + g)*0.2.
- Mist: 4 paper-coloured ellipses, blur 14, alpha .72, drifting 150-270 px/s over the hills.
- A small bird (two wing strokes, sin(52t) flapping) darting across at 420 px/s.
- Qi Baishi-manner shrimp: 6 pale segments plus one scorched carapace stroke, wave antennae, three-segment claws, body bend sin(7t)*0.12, swimming along a curve.
- Bada's "white eyes": pupils at the top of the eye, an aloof skyward stare.
- Seal: 1.5 -> 1 over ~3 frames, multiplied on; reversed-out brand initials.

## Signature transition
Ink bloom: the old shot washes into paper (grayscale 0 -> 1, brightness 1 -> 1.35, contrast 1 -> 0.7 over the first half); ink blots bleed out in sequence from the brush-down point, each a noise-perturbed circle (radius*(1 + 0.35*noise)) growing to ~1500px*k, the new shot inside; a dark rim rgba(30,26,22,.55*(1 - q)^1.5), ~34px blurred, fades as each blot grows. 0.45 s (14 frames). Custom presentation (see flat-illustration.md): CSS filter on the exiting side, `clipPath: path(...)` of the blot union on the entering side, rims in an overlay SVG; blur at 1/4 res.

## Pitfalls
- Bristles drawn per segment with round caps knot like rope; one continuous butt-capped path per bristle.
- Thousands of bristles per frame are too slow; cache strokes once written.
- Multiply washes are transparent, so lines behind show through subjects; fill the silhouette with paper first, then wash.
- A mover routed through a dense area (bird through bamboo) vanishes; route it over empty paper or mist.
- Weakness: draw figures with the same brush in a few confident broken strokes with reserved white, not closed outlines plus a wash.
