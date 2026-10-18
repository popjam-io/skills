# Hopper American realism (1942, hard sunlight blocks)

> Adapted from huashu-art-motion (MIT, (c) 2026 alchaincyf) - references/风格配方/24_hopper.md

Layer: era specimen (best for homage, journeys, era-hopping); its hard light blocks also transfer as a material-layer lighting treatment - Upstream quality: ★★★ - Known weakness: a secondary character sat in shadow all shot, too dark.

Evoke the technique; never copy a specific work or character.

## Look
Quiet rooms cut by flat, hard-edged blocks of low sun; cool green shadow against warm yellow light; flat walls; city windows with blinds at uneven heights. Shadow wall #5d8679, wainscot #4b6d63, floor #5b3d2b; lit wall #efcf8f, wainscot #d8ad68, floor #c98b52; red dress #7a2c2a / #cc4a3c; blond hair #a8893f / #f3d67e; brick #b4553a.

## Build it in Remotion
Dual-version clip: render the scene twice - `<Room lit={false} />`, then `<AbsoluteFill style={{clipPath}}><Room lit /></AbsoluteFill>` with the light as `clip-path: path(...)` (a subpath per patch). Hard edges by construction, the light slides as a whole; cheap DOM/SVG. Figures likewise, with their own clip.
- Geometry (px at 1920 wide; scale with the canvas), dx = 30 - 95*easeInOut(t/1.25): wall patch (1420+dx,250) (1920,470) (1920,730) (1420+dx,730); a floor patch below it spreading lower right; for figures a band with left edge (1345+dx, 0) -> (1185+dx, 1080), taking the face from half-shadow to lit. Mullion shadows: a 24px vertical bar and a diagonal parallel to the patch top.
- Cast shadow on the lit wall: inside the patch, the shadow version clipped to the subject's silhouette offset (+150, +18).
- Texture: vertical noise (feTurbulence baseFrequency "0.06 0.006") at soft-light .2 - barely there.
- Opposite windows: 10px hard shadow on their right, blinds at 0.25-0.7.

## Make it move
- The light drifts (main action): ~95px over 1.2 s upstream; in longer shots keep it slow and let the edge cross the face or product as the reveal.
- Barber pole stripes climbing 60 px/s; blind cord sin(4.2t)*0.07 rad; 26 dust motes only inside the light; steam.

## Signature transition
Sun shaft: a hard slanted light block (slant 260px) sweeps in from the left with the new shot inside under a warm screen tint rgba(255,214,140,.45) fading over the last 40%; outside, the old shot sinks into shadow (multiply rgba(70,120,110, up to .7)); a 34px mullion shadow 420px behind the edge; bright edge rgba(255,236,190,.8) 6px. Ease 0.4*easeOut + 0.6*easeInOut. 0.34 s (10 frames). Custom presentation (see 16_2026.md): polygon clip, tint/shade divs with mix-blend-mode screen / multiply.

## Pitfalls
- Horizontal noise at .35 made walls look like watery marble.
- Silhouette and hair carry age: updo and long dress read adult; loose hair and a hairband read teenage.
- White in shadow must stay white (#dcd6c8); #c4bdac read grey.
- Weakness: give secondary characters a small patch of light.
