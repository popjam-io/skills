# Voice Guideline Document Template

Structure the deliverable with these sections. Every rule must carry evidence — a frequency ("31/38 social captions") or named corpus IDs — and be labeled **Rule** (≥70% recurrence), **Variation** (30–70%, with its trigger: channel, campaign type, language, date) or **Exception** (<30%, observed only). Rules and attributes are written in English; verbatim examples stay in their source language.

---

# [Brand] Voice & Writing Style — Extracted Guidelines
*Extracted from N texts (social n, long-form n, ads n, web n; languages), [date range if known]. Method: programmatic text stats + structured reading pass + frequency synthesis.*

## 1. Voice Foundation
Who is speaking (a founder, a team, the brand as a character, a narrator) and to whom, as *inferred from the corpus*. The one-line voice summary a new writer could work from. Positioning cues observed in the copy. Keep brief; this is context, not rules.

## 2. Core Attributes
3–5 voice attributes (e.g. "direct", "warm", "expert without jargon"), each with the verbatim lines that suggest it and a counter-line showing what it is *not* ("confident, not boastful: says X, never Y"). Attributes that hold across all channels only; per-channel character goes in section 3.

## 3. Per-Channel Systems
One subsection each for **social**, **long-form**, **ads** and **web** (skip channels with no corpus and say so in section 10). Per channel: the stats fingerprint from `stats.json` (length range, sentence length, emoji/hashtag/question/exclamation rates, person, CTA rate, reading grade), the dominant structure template, and which core attributes are amplified or muted here. This is what prevents the guideline from flattening a living system into a false average.

## 4. Hooks & Openers
Hook-type distribution per channel from `stats.json`, then the *formulas* behind the winning types with 3–5 verbatim examples each ("[number] [noun] you [verb]…", pain-point question, bold claim). Note what never opens a text.

## 5. Structure & Length
The ordered part list per channel (hook → context → proof → offer → CTA → hashtags) with frequency, length norms as ranges (not means alone), paragraph and line-break habits, list/bullet usage, sign-off conventions.

## 6. CTAs & Offer Framing
CTA patterns verbatim, per channel, with type (shop / sign-up / learn-more / link-in-bio / engage / contact). Offer framing conventions (percentage vs absolute vs starting-price vs free-trial vs coupon) and where each appears. Urgency devices verbatim, and whether urgency is used at all.

## 7. Vocabulary
Recurring phrases, taglines and product names verbatim (the brand lexicon). Banned or absent words and constructions (superlatives, discounts, "we", competitor names…). Emoji policy: level, the specific set, position. Hashtag policy: count range, fixed brand tags vs topical tags, position. Capitalisation and punctuation habits (all-caps words, exclamation policy, ellipses, dashes).

## 8. Language & Localisation
Language mix per channel with counts. Formality marker per language (tú/usted, sen/siz, du/ni). Code-switching habits (English CTAs inside local-language copy, English product names). Which language(s) generated copy should be written in, per channel.

## 9. Do's & Don'ts
Do's: 4–8 exemplary corpus texts (IDs + the first line) with one line each on why they're exemplary. Don'ts: violations of numbered rules above, each with a short *rewritten* example showing the violation and the on-brand fix.

## 10. Coverage & Confidence
What the corpus did NOT contain (channels, languages, campaign types, date range); which rules are extrapolations; per-channel sample sizes and any channel marked provisional; engagement caveats if performance was joined.

---

# Voice Prompt Block Template

Produce one block per channel present in the corpus (minimum: the best-covered one). Compact, no prose, consumable by a generation pipeline; every hook and CTA example is verbatim from the corpus:

```
Voice: [Brand] [channel] copy.
Attributes: [3-5 attributes, each with a two-word "not X" guard].
Person/formality: [first-plural | second...]; [casual | formal] ([marker: sen/siz, tú/usted, du/ni]).
Hook: [formula] — e.g. "[verbatim hook]".
Structure: [hook -> context -> proof -> offer -> CTA -> hashtags].
Length: [chars/words range]; sentences [short | medium]; [paragraph / line-break habit].
CTA: "[verbatim pattern 1]" | "[verbatim pattern 2]"; type [shop | link-in-bio | ...].
Offer framing: [percentage | absolute | starting-price | free-trial | none]; urgency: ["verbatim device" | none].
Emoji: [none | accent (set: ...) | heavy]; position [leading | inline | trailing].
Hashtags: [none | n-m trailing: #brandtag + topical].
Language: [write in tr; product names and CTA in en | ...].
Never: [3-5 don'ts, the most important first].
```
