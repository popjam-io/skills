# Brand Guideline Document Template

Structure the deliverable with these sections. Every rule must carry evidence — a frequency ("31/38 assets") or named example files. Label each statement as **Rule** (≥70% recurrence), **Variation** (30–70%, with its trigger context), or **Exception** (<30%, observed only).

---

# [Brand] Visual & Verbal Identity — Extracted Guidelines
*Extracted from N assets ([sources]), [date range if known]. Method: programmatic palette extraction + structured vision analysis + frequency synthesis.*

## 1. Brand Foundation
Positioning and personality as *inferred from the corpus* (3–5 adjectives with the evidence that suggests each). Target-audience cues observed in imagery/copy. Keep brief; this section is context, not rules.

## 2. Logo Usage
Variants observed; placement pattern (with frequency); size relative to canvas; clear-space estimate; co-branding behavior. Don'ts only if violations were observed.

## 3. Color System
- Primary / secondary / neutral palettes: hex (from programmatic extraction), role, recurrence.
- Usage rules: which color on which background; text-color pairings; gradient specs if observed (angle, stops).
- Category or sub-system color coding if discovered in Phase 3 — this is often the most valuable finding for multi-category brands.

## 4. Typography System
Primary and secondary typefaces: real names if recovered from source files/CSS, otherwise characteristics + closest-match hypothesis clearly marked. Hierarchy: levels, size ratios, weight/case per level. Alignment rules per context. Special treatments (italic emphasis, outlines, 3D styles) with their trigger contexts. For service brands typography carries the identity — give it proportionally more depth.

## 5. Layout & Composition
The structural template(s): zones, fixed bands, reading-order formula. Density and white-space norms. Aspect-ratio/format specs per platform observed. Margin/padding estimates where consistent.

## 6. Graphic Elements & Visual Language
Recurring shapes/motifs and their meaning. The badge vocabulary: every recurring badge with verbatim text, shape, color, role, and placement. Icon style. Decorative devices and when they appear.

## 7. Imagery & Product Presentation
Cutout vs lifestyle vs podium staging, by context. Product count norms. Human presence rules. Third-party brand-logo usage (trust rows). Treatments never observed (list them — useful negative space).

## 8. Tone of Voice & Copy Rules
Voice attributes with verbatim examples. Offer-framing conventions (percentage vs absolute vs starting-price vs coupon) and where each appears. Headline formulas. CTA patterns verbatim. Urgency devices. Formality, emoji policy, language conventions. Legal/fine-print conventions.

## 9. Sub-Systems & Overrides
One subsection per discovered sub-system (seasonal, co-brand, category, pipeline): the trigger condition + which rules above it overrides. This is what prevents the guideline from flattening a living system into a false average.

## 10. Do's & Don'ts
Do's: 4–8 exemplary corpus files with one line each on why they're exemplary. Don'ts: violations of numbered rules (cite the rule), drawn from observed weak assets or hypotheticals.

## 11. Performance Notes *(only if performance data was joined)*
Which patterns correlate with stronger/weaker performance, with the caveats stated (attribution, confounds, sample size).

## 12. Coverage & Confidence
What the corpus did not contain; which rules are extrapolations; corpus date range and sources.

---

# Style Prompt Block Template

Produce one block per sub-system (minimum: the core system). Compact, no prose, consumable by a generation pipeline:

```
Visual style: [Brand] [sub-system name] identity.
Canvas: [1080x1920 9:16 story | ...].
Colors: background #HEX [treatment]; primary #HEX; accent #HEX; price/emphasis #HEX on #HEX.
Typography: headline [traits, case], body [traits]; hierarchy [ratio]; alignment [rule].
Layout: [zone formula]; reading order: [badge -> headline -> product -> price -> CTA]; density [norm]; fixed elements: [header band, legal line...].
Graphic elements: [badge vocabulary with verbatim text]; [shapes/motifs].
Imagery: [product presentation mode, count, treatment]; [logo row rule].
Copy: headline formula [..]; offer framing [..]; CTA [verbatim pattern]; urgency [verbatim device]; language [..]; emoji [policy].
Never: [the 3-5 most important don'ts].
```
