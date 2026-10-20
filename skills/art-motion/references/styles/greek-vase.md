# Attic Black-Figure Pottery (Archaic Greece, c. 530 BC)

> Adapted from huashu-art-motion (MIT, (c) 2026 alchaincyf) - references/风格配方/03_greek.md

Layer: era specimen (best for homage, journeys, era-hopping) - Upstream quality: ★★★ - Known weakness: hems and drapery silhouettes come out too thick.

## Look
Three ingredients, all required; together they read "Greek vase" without any texture:
- **Black-glaze silhouette**: figures and objects filled warm near-black `#1b120d`, no outline; form comes from silhouette against clay.
- **Incision**: 1.5-2 px clay-orange `#e8904c` lines scratched through the black for folds, features and wherever black overlaps black.
- **Added color**: purple-red `#8a2a37` bands (hair bands, cuffs, hems, collars, cushions) and small white dots `#f6ead6` (r ~2, spaced 11-17 px).
- Clay `#dc6a2f`, lighter panel `#e8803f`, reserved clay for whites `#f3cfa4`, gold accents `#f2bd48`, orange `#f2913f` for incised animal stripes.
- Profile heads with a straight brow-nose line and a frontal almond eye. Registers: meander (Greek key), lotus-bud chain with rays, vine with grape triangles, dotted frames. Hand-painted Greek lettering with uneven heights.

## Build it in Remotion
px at 1920 wide; scale with the canvas.
1. **Clay ground (bake once)**: at 480x270 compute `fbm(x*0.016, 4 oct)` mottling +-30 plus horizontal throwing bands `noise(x*0.006, y*0.85)` +-9, then upscale (low-frequency content survives; 16x cheaper). Add ~560 faint horizontal hairlines (length 150-1050, alpha 0.03-0.08, dark and light), 420 dark + 120 light specks, two grain layers with *different* seeds, ~5 cracks (9 px segments, +-2 px jitter, a 1 px light edge offset below for depth), a warm radial lift (0.16), and a radial vignette (380 -> 1180, edge `rgba(30,6,0,.62)`) over everything.
2. **Static black-figure layer (bake)**: frame (18 px black + white dot string at 11.6 px pitch + thin inner line), furniture, vessels from symmetric profile point lists smoothed into paths. SVG suits this well: black fills with incision strokes clipped to them (`clipPath`).
3. **Lettering**: your own stroke tables (1-3 polylines per letter in a unit cell) rather than a font: cap height 30, stroke 3.4, per-letter height x(0.9-1.06), baseline +-6%, vertex jitter +-0.7 px, omicron as a small circle at 0.25 height.
4. **Scrolling bands**: pre-render one strip (width + 2 periods) per band and offset it by `offset mod period` each frame; in SVG/DOM use a repeating pattern with `backgroundPosition` driven by frame (nearly free). Meander: period 60 px, 7 px lines, unit polyline `[[4,46],[4,0],[50,0],[50,34],[18,34],[18,14],[36,14],[36,22]]` + baseline. Lotus buds: 38 px units with alternating purple fills, so the true period is 76 px.
5. **Figures**: fill black, then incise inside a clip. Separate black-on-black overlaps by clipping to (body union head) and stroking the overlapping limb's outline in the incision color. Fine colored detail (hair): a 6 px dark under-stroke, then 2.5 px color (2 px vanishes at thumbnail size). Secondary animals use the same method: black silhouette, a ~26 px purple saddle along the back, incised stripes placed at equal arc length along the back contour pointing toward the body center (`getPointAtLength` / `getTangentAtLength` from @remotion/paths), white added color for chest and muzzle, incised almond eye; blink = one down-curving incision.
Cheap overall (upstream ~8 ms/frame): only bands, motifs and the subject redraw.

## Make it move
- **Main - the subject's gesture**: e.g. lifting a wide, shallow kylix to the lips (tilt <= 5 deg, hand under the foot, purple rim line), steam as three thin black wavy lines with phase `t*9`.
- **Loop 1 - bands scroll in opposite directions**: top drifts left 48 px/s, bottom right 30 px/s, each with one extra eased period jump on a beat (`offset = 48t + 60*easeInOut(beatWindow)`).
- **Loop 2 - vase motifs**: a lyre swinging from its nail `0.09*sin(2*pi*t/0.8 + 0.5)` (+-5 deg, ~17 px at the sound box); dolphins swimming +-9 px along their heading with +-0.12 rad, period 0.85 s (~26 frames), phases 1.3 apart; a ship bobbing +-4 px and rocking +-0.025 rad, period 0.9 s; an 8-petal rosette (black petals, incised dividers, purple heart) turning 1.6 rad/s, alternating direction.

## Signature transition
Vase turn: the old shot rotates away like the face of a turning drum while the new one comes round from the right. `e = easeInOut(p)`, angle `e*pi/2`; each face drawn as ~48 vertical slices that shrink toward the far edge (k = 0.18*sin(angle)) and darken by alpha `0.55*sin(angle)` as they turn away, over `#0d0a08`. Upstream 0.32 s (~10 frames); 0.5-0.7 s in an ad. Remotion: a custom presentation with CSS 3D (`perspective` on the container; entering child `rotateY(90deg -> 0)` with origin left, exiting child `rotateY(0 -> -90deg)` with origin right, a black overlay for shading); the stock `flip` presentation is a cheaper approximation.

## Pitfalls
- A bright cartoon animal beside black-figure people breaks the style at once: every character goes through silhouette + incision + added color.
- Heads scaled up from a generic rig get a helmet-like skull; keep the back of the head and hair close to the face.
- A cup at the mouth merges hand, cup and face into one black blob: incise the arm against the head, shrink the cup (half-width ~32 px), keep the purple rim line, and pose the forearm upright in front of the chest so nose, lips and chin stay exposed.
- Scrolling a periodic band by exactly one period looks identical, so stills and sampled frames read as static. Keep a constant drift.
- Wrap patterned strips at their *true* period (76 px for alternating-color buds), or colors jump.
- Grain layers made with the same seed are identical.
- Weakness (thick hems): taper the hem silhouette and let the purple band and white dots carry the edge instead of mass.
