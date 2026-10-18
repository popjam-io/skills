# Chiaroscuro (Rembrandt, Dutch Golden Age, 1642)

> Adapted from huashu-art-motion (MIT, (c) 2026 alchaincyf) - references/风格配方/32_rembrandt.md

Layer: material (works on any subject) - Upstream quality: ★ - Known weakness: the figure looked flat (review 5/10); the most urgent redo of all styles.

## Look
Warm darkness (ambient ~13%) broken by one window shaft and a candle. Light pools on the face, chest and hero object; a "separation light" brightens the wall behind the figure's dark side so the silhouette detaches; edges dissolve into shadow. Broad brown brushwork behind, bristle impasto only on lit highlights, craquelure, fine grain, dark vignette, gold-brown varnish. Made for premium, moody product reveals (glass, metal, leather, food).

## Build it in Remotion
Px at 1920 wide; scale with the canvas.
1. Paint the scene in its fully lit colours.
2. Background repainted with broad brown strokes (canvas, cached): cell 18, length 54, width 16, jitter 6, angle -0.9 + 1.6 * noise2D(seed, x * 0.003, y * 0.003), palette mix 0.7; then a 2.2 px blur at 75% over it. Patterned cloth gets its own fine-stroke layer.
3. Figures: flat fill + volume gradients + fine strokes. Lost edges: the figure blurred 2.4 px at full opacity, the sharp figure at alpha .62 on top.
4. Light map multiplied over everything (the core). Base rgb(30,21,13); warm-white radial pools added on top: window shaft (wedge, blur 40, alpha .8-.95), window r330, face r250 alpha .95, chest r230 alpha .55, secondary subject r240 alpha .8, table/product r280 alpha .6, candle r190 + 40fc alpha .6 + .4fc, separation light behind the figure r300 alpha .35. DOM route: an `AbsoluteFill` with that background, `isolation: 'isolate'` and `mixBlendMode: 'multiply'`, holding radial-gradient divs with `mixBlendMode: 'plus-lighter'`. Cheap, and pools can move per frame.
5. Window glass screen-brightened; a cloud shadow crosses it.
6. Impasto (bristle brush) only on lit points - hair highlights, collar, porcelain, pearls, white fur; in ads the product's rim, cap or label edge: one stroke = round(w / 1.3) parallel bristles, luminance +-17 each, ends shortened 0-25%, width 1.4-2.6; a shadow line below at alpha .28; 2 + w/3 bright specks on top. Cached canvas.
7. Finish: craquelure alpha ~.08, grain density 0.05 alpha .12, vignette 0.75, a `soft-light` layer of rgba(200,140,60,.35). Cache textures once.
8. Real product and logo sit inside a lit pool as images; only light, shadow and varnish pass over them, never strokes.

## Make it move
- Flicker fc = 0.5 * noise2D('flk', 2.2t, 0) + 0.25 * noise2D('flk2', 6.5t, 0); pool centres drift +-14 px with noise at 0.9t.
- Cloud = 0.5 + 0.5 * sin(2.2t - 0.6); window light x (1 - 0.35 * cloud), plus a dark blot crossing the glass at 260 px/s.
- 70 dust motes only inside the shaft, each twinkling over 24 frames; the candle flame leans and jumps by noise; steam.
- One slow main action (raise, turn, unveil); light carries the life (~8% of the frame moves).

## Signature transition
Into the dark, out by the light, 0.45 s (14 frames): the old shot sinks into dark brown under a closing vignette, then a soft-edged light shaft spreads from the window and reveals the new shot with a warm glow. Recipe: ../transitions.md (chiaroscuro).

## Pitfalls
- Impasto as shadow offset + main stroke + bright ridge read as white stickers or band-aids; use the bristle brush.
- Copying a rectangle back from the unstroked base pasted unstroked background; props go in their own layer after the strokes.
- Grain at density 0.12 / alpha .22 dirtied faces; 0.05 / .12 is right.
- Grip order: hand, then held object, then thumb - or the hand covers the product.
- Flat figure (the weakness): pass the figure through the same renderer as the background - brushwork on clothes, pools on the face planes, lost edges, impasto on highlights - not vector fills under a light map.
