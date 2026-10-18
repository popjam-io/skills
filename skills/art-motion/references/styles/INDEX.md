# Style index (35 styles)

> Adapted from huashu-art-motion (MIT, (c) 2026 alchaincyf) - references/风格配方/INDEX.md

**Read this first.** The upstream sample films for these styles all shared one room composition, because they were made for an art-history speedrun: the style changes, the scene stays. That room is NOT the composition for these styles. Design a fresh composition for each subject and format. From a card, take the renderer, the mark-making, the colour logic and the motif motion; leave behind any layout, furniture or characters it mentions.

Pick from the tables below, then open the card. Upstream quality is how well the style was executed, not how hard the style is:
- ★★★ recognizable at a glance and usable as is
- ★★ recognizable, with clear weaknesses
- ★ needs a redo

The known weakness is the first thing to beat the next time you use that style. Ids run 01-36; there is no 07.

Two layers:
- **Material layer**: mark-making, material, light and colour treatment that can be laid over any subject (product, data, story). "Narrow use" marks styles that only fit specific messages.
- **Era specimens**: the samples lean hard on the era's or artist's motifs, so they suit speedruns, journeys through time and homage. Moving one to a new subject means re-extracting its visual language and composition; the samples' limits are not the artist's limits. When unsure, treat a style as material layer (Hopper's hard-edged light patches, for example, are a lighting treatment that transfers anywhere).

For living artists, studios and actively managed estates (Kusama, Haring, Picasso, Matisse, Dali, Hopper, Lichtenstein, Warhol, Kirby, Ghibli, Shinkai): evoke the technique; never copy a specific work or character.

## Material layer - works on any subject

| File | Style | Core technique | How it moves | Signature transition | Upstream quality | Known weakness |
|---|---|---|---|---|---|---|
| [09_postimp](09_postimp.md) | Van Gogh (Post-Impressionism) | Flow-field strokes in three passes (walls long vertical, floor in perspective, rest along the field) + regional palettes + outlines; props on their own layer; outlines re-added where strokes erase them | Starry swirls, lamp halos ringing outward, flame-like swaying field, a swirling secondary character | Starry swirl pulls the new shot in | ★★★ (benchmark) | Heaviest per-frame cost of all styles |
| [08_impressionism](08_impressionism.md) | Impressionism | Short pastel strokes from regional palettes at fixed positions; finer strokes in the distance | Light flecks drift and flicker, poppies sway, clouds move, ribbons flutter | Coloured dabs paint the new shot on | ★★ | Faces and hands get shattered by strokes |
| [29_seurat](29_seurat.md) | Seurat pointillism | Optical mixing: 21-colour pure palette mixed in pairs by ratio, complementary dots, equal dots | Light irradiation, breathing dots | Picture crystallizes into dots | ★★ | Too static; grid too regular |
| [25_ghibli](25_ghibli.md) | Ghibli-style watercolour (background + overall-language study) | Watercolour washes (transparent glazes, water-mark edges), cel crescent shadows | Curtain billows, grass sways in sheets, dappled leaf light | Wet-paper bleed | ★★ | Characters weaker than backgrounds |
| [17_ink](17_ink.md) | Chinese ink wash (xieyi) | Brush-tip strokes with flying-white, ink bleed by spreading blur, empty space, seal stamp | Opening strokes write themselves, ink blooms spread, small creatures twitch | Old shot washes to paper, ink blots bloom with the new shot inside | ★★ | Figures not loose enough (review 6/10) |
| [13_pop](13_pop.md) | Lichtenstein-style pop | Ben-Day dot patterns, heavy black outline | Warhol-style four-panel colour swaps, thought dots blink, a character wiggles, sound-effect balloon shakes | Lightning bolt + halftoning | ★★★ | - |
| [14_8bit](14_8bit.md) | 8-bit pixel art | 240x135 per-pixel canvas, 14-colour palette, 1 px black border per part | Tail wag, HUD heart blink, question block pops a coin (stepped 15-30 fps) | Pixel blocks grow, then shrink | ★★★ | Layout collision: a character's head overlapped scenery |
| [26_vaporwave](26_vaporwave.md) | Vaporwave / cyber-neon | Two-colour neon glow, perspective grid, VHS channel-split post, neon lettering drawn as paths | Striped sun drifts, grid rolls forward, sign flickers, tracking band rolls | VHS tear + vertical roll | ★★★ | Internal part seams glow too |
| [35_shinkai](35_shinkai.md) | Shinkai-style anime light | Cumulonimbus, god rays, hard cel shadow bands, flare and bloom | Light particles drift, clouds move | Diagonal light sweep | ★★ | Interior background not dense enough |
| [32_rembrandt](32_rembrandt.md) | Rembrandt chiaroscuro | Whole-frame light map multiplied; window light + candle | Dust in the light shaft, cloud shadows dim the window light | Darkness closes, a light shaft reveals the new shot | ★ | Flat figure (review 5/10); most urgent redo |
| [11_cubism](11_cubism.md) | Analytic Cubism | Translucent gradient planes stacked into space, facet cutter (unclipped triangles), double-view face | Lettering hops and swaps, window facets slide, newspaper trembles | Geometric shards misalign and reassemble | ★★ | Too bright; not enough dark-brown mass |
| [30_matisse](30_matisse.md) | Matisse cut-outs | Irregular scissor edges, pinned-paper shadow, saturated flat colour | Paper pieces flutter, fronds sway | A cobalt sheet of pinned cut-outs sweeps across | ★★★ | Gouache texture a bit heavy |
| [16_2026](16_2026.md) | Contemporary flat illustration | Grain-stipple density function, unoutlined colour blocks | Character acting beats (jump, slam, shatter, gasp, sign-off) with damped secondary motion | Three-colour concentric ring iris | ★★★ | - |
| [22_constructivism](22_constructivism.md) | Russian Constructivism (narrow use) | Greyscale photo halftone (variable dots at 45 deg), red wedge and black circle, block lettering drawn as paths | Slogan stamps in letter by letter, then wave-hops | A red wedge stabs across, type bars chase it | ★★★ | Missing the megaphone-shaped text cone |
| [12_bauhaus](12_bauhaus.md) | Bauhaus (narrow use) | Pure geometric composition, mannequin figures with joint discs | Pointer rods swing sharply, grid cells swap primaries, a character bats a ball | Red/yellow/blue geometry spins and scales up | ★★★ | A character's head drifted off its skeleton anchor |
| [04_roman](04_roman.md) | Pompeii mosaic (narrow use) | Distance field lays tesserae along contours, weighted L-infinity Voronoi grout, layout computed once with colour flowing through it per frame | Wave border flows clockwise, volcano smokes and sparks | Tesserae flip over, spreading from a focal point | ★★★ | Little facial detail at small scale |
| [15_raytrace](15_raytrace.md) | Early ray-traced CGI (narrow use) | Uniform plastic shading, per-pixel checkerboard reflections, chrome-sphere environment map | Purple ring spins, lens flare, glowing green eyes | Green wireframe, then a scanline render | ★★ | Legs like straight columns; face reads as a mask |

## Era specimens - homage, journeys, era-hopping

| File | Style | Core technique | How it moves | Signature transition | Upstream quality | Known weakness |
|---|---|---|---|---|---|---|
| [01_cave](01_cave.md) | Cave painting | Noise-relief rock wall + charcoal-dot rough edges + ochre soaked into the rock | Animals run by alternating two poses, firelight flickers, embers | (an opener; no entry transition) | ★★★ | Human figures too cartoony, not primitive enough |
| [02_egypt](02_egypt.md) | Egyptian tomb painting | Profile head with frontal eye, flat fills with fine outlines, 24 hand-drawn hieroglyphs | Scarab rolls the sun, sun rays end in opening and closing hands, hieroglyphs rewrite stroke by stroke | Masonry blocks set in, left to right | ★★★ | Holding arm stiff at the elbow |
| [03_greek](03_greek.md) | Attic black-figure pottery | Black silhouettes + clay-colour incised lines + purple-red bands with white dots | Meander band scrolls backward, ship rocks and dolphins leap, lyre sways | Vase turns like a cylinder to a new face | ★★★ | Skirt too thick |
| [05_gothic](05_gothic.md) | Gothic illuminated manuscript | Per-pixel gold leaf (brushed + embossed, 1 px offset highlight lines), gold-chroma highlight mask | Diagonal glint sweeps the gold, vines sway, snail crawls, mouse runs | Parchment page turn | ★★★ | Blond hair read as a hood |
| [06_renaissance](06_renaissance.md) | Renaissance sfumato | Lightly blurred full layer + high-opacity sharp layer, craquelure, canvas weave, yellow varnish | A flying-machine sketch flies past, glints on a river, floating dust | Divine rays burst from a window | ★★ | Secondary character too cartoony; overall too static |
| [10_nouveau](10_nouveau.md) | Mucha-style Art Nouveau | Variable-width paths (thick outside, thin inside), offset silhouette underlay | Sun rises, halo turns, flowers sway, S-curved steam, waving hair | Gold-edged organic shape grows | ★★★ | Secondary character's pose stiff |
| [18_klimt](18_klimt.md) | Klimt golden phase | Gold leaf (as gothic), spiral and eye ornaments, realistic face on a flat gold robe | Eye motifs on the robe blink in turn, gold flakes drift | Gold leaf tiles spiral out from the head | ★★★ | Hand on the table not connected to the sleeve |
| [19_munch](19_munch.md) | Munch Expressionism | Long curved flow strokes (20-30 steps along a field), whole world warped by per-row sine | The whole picture writhes, the blood-red sky flows | Scream-coloured bands press down from the top | ★★ | Wall once read as Van Gogh |
| [20_dunhuang](20_dunhuang.md) | Dunhuang murals | Earth-red ground with mineral pigments, flaking (background only), desaturated fading | Flying-figure ribbons stream, ceiling petals fall, lamp flames | Ribbons sweep across, the old mural flakes and falls | ★★ | Flying figures crude |
| [21_kusama](21_kusama.md) | Kusama polka dots | Hand-drawn irregular circles, hex grid tiled at its true period | Dots swell and shrink ring by ring from a focal point, pumpkin, infinity-mirror room | Dots grow, each clipping the new shot | ★★★ | Figure same colour as the wall, held only by its outline |
| [23_dali](23_dali.md) | Dali Surrealism | Soft-watch deformation, long shadows by shear transform | Clocks drip, long-legged elephants walk, ants circle a watch, shadows lengthen | New shot drips down with round-headed drops | ★★ | Figures look like vector illustration |
| [24_hopper](24_hopper.md) | Hopper American realism | Two lighting versions (lit and dark) clipped by light patches, hard-edged sun patches | Sun patch slowly crosses the face, a wall shadow mirrors the action | Hard-edged sunlight sweeps in | ★★★ | Secondary character stayed in shadow throughout |
| [27_kirby](27_kirby.md) | Silver-age comic (Jack Kirby era) | Four-colour halftone, misregistered plates, spotted blacks with feathered hatching, krackle energy dots | Sound-effect lettering, inset close-up panel, energy dots | Comic panels slam in | ★★ | Reads more like Lichtenstein; lacks Kirby perspective and blocky hands |
| [28_monet](28_monet.md) | Monet water lilies and footbridge | Short-stroke water reflections, light trembling on water | Lilies drift, willow reflections sway, ripples spread | Water ripples spread | ★★ | Pond on a wall above a wooden floor: awkward space |
| [31_haring](31_haring.md) | Keith Haring | Thick uniform black line, radiating action lines | Figures dance in 8 fps hard cuts, everything bounces to the BPM | A dancing figure grows with the new shot in its body | ★★★ | Main character not Haring enough |
| [33_rubberhose](33_rubberhose.md) | 1930s rubber-hose cartoon | Pie-cut eyes, noodle arms, white gloves, 12 fps stepping, film scratches and flicker | Everything bounces on the beat | Old-film iris out and in | ★★★ | Most of the motion is film noise |
| [34_shadowpuppet](34_shadowpuppet.md) | Chinese shadow puppetry | Translucent carved leather, rivet joints, 10 fps stepping, oil lamp behind the screen | Rod-driven stiff joints, loose wrists | The lamp lights up behind the screen | ★★★ | Overlaps multiply to black; heavy per frame |
| [36_picasso_blue](36_picasso_blue.md) | Picasso Blue Period | Blue monochrome, wide strokes, thick Prussian-blue contour, elongated bodies | Slow breathing | Colour drains to blue, then a wide brush sweeps | ★★ | Forms not melancholic enough |

## Quality and the next step

- Of these 35: ★★★ 20, ★★ 14, ★ 1.
- The most common weakness is characters and subjects not passing through the same renderer as the background. A background that goes through the style's renderer reads as that style; a character drawn as flat vector fills on a skeleton looks pasted on. The next quality step is to push characters through the same renderer, or reshape their forms in the style: Rembrandt, Picasso Blue, ink, Ghibli, Dali and Kirby first.
- Transitions between styles: [../transitions.md](../transitions.md).

## Pick a style for an ad

- **Product or brand as the subject: use the material layer.** Clean modern default: 16_2026. Loud retail and sale energy: 13_pop, 22_constructivism, 31_haring (beat-driven). Retro tech, gaming, youth: 26_vaporwave, 14_8bit, 15_raytrace. Premium and moody reveals: 32_rembrandt (redo the figure), 30_matisse (fashion, design). Warm lifestyle and outdoors: 25_ghibli, 35_shinkai, 08_impressionism, 29_seurat. Craft and artisan: 09_postimp, 17_ink. Design and architecture: 12_bauhaus, 11_cubism.
- **Themed homage: use era specimens.** Cultural moments (Lunar New Year, Mid-Autumn: 20_dunhuang, 34_shadowpuppet), heritage and anniversary stories (33_rubberhose, 27_kirby, 02, 03, 05), "through the ages" journeys that hop eras with each style's signature transition, and art-world nods (18_klimt for jewellery and luxury, 10_nouveau for beauty and fragrance, 23_dali for surreal claims, 24_hopper for quiet urban moods). Recompose every time; the cards' motifs are examples, not the brief.
- **The brand's real logo and product images are composited in, never re-painted.** Stroke fields, dots, halftone, scissor edges, VHS splits and mono passes make logos and packshots illegible or wrong. Run the renderer on the world around them, then integrate the real asset with the style's light, cast shadow, rim light, sticker outline or paper shadow. Keep headline, price and CTA above any post-processing layer and inside the platform safe zones.
- Monochrome styles (33_rubberhose, 36_picasso_blue) cannot show brand colours; put the true-colour logo on an end card.
- Cost: stroke-field and dot renderers (08, 09, 28, 29, 32) and layered multiply styles (34) are the heaviest in live preview; cache static layers and step the animation. Flat and line styles (13, 16, 30, 31) are the lightest.
