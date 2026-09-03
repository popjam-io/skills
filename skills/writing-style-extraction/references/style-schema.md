# Per-Sample Extraction Schema

Use this schema for every text analyzed in Phase 3. Fill every field; use `"none"` / `"n/a"` explicitly rather than omitting — omissions are indistinguishable from oversights during synthesis.

Quote in the source language, verbatim, emoji and punctuation included. Counts and lengths are the script's job (`stats.json`) — don't re-estimate them. Your unique contribution is *pattern and intent*: what kind of hook this is, what the structure does, how the offer is framed, what the brand never says.

```json
{
  "id": "corpus id",
  "channel": "social | long_form | ads | web",
  "language": "tr | en | sv | ... ; 'mixed (tr body, en CTA)' when code-switching",
  "content_type": "promo | launch | educational | community | testimonial | seasonal | recruitment | other",
  "hook_type": "question | number | quote | statement | emoji | bold-claim | pain-point | story | none",
  "hook_verbatim": "the first sentence or line, verbatim",
  "structure": ["hook", "context", "proof", "offer", "cta", "hashtags"],
  "sentence_style": "short-punchy | medium | long-flowing | fragments | mixed; note list/bullet/line-break habits",
  "person": "first-singular | first-plural | second | third | mixed; who speaks and who is addressed",
  "formality": "casual | conversational | neutral | formal; name the marker (tú/usted, sen/siz, du/ni, slang, contractions, honorifics)",
  "emoji_usage": {"level": "none | accent | heavy", "which": ["🔥", "✨"], "position": "leading | inline | trailing | as-bullets"},
  "hashtags": {"count": 0, "verbatim": ["#..."], "position": "inline | trailing block | none"},
  "cta_verbatim": "...",
  "cta_type": "shop | sign-up | learn-more | link-in-bio | engage (comment/tag/share) | contact | download | none",
  "offer_framing": "percentage | absolute | starting-price | threshold | bundle | free-trial | coupon-code | none",
  "urgency_device": "verbatim phrase or none",
  "recurring_phrases": ["taglines, product names, verbal tics or constructions that look like brand vocabulary"],
  "sign_off": "verbatim closing line, signature or brand hashtag, or none",
  "taboo_or_absent": ["things conspicuously never used: emoji, exclamation marks, discounts, 'we', English loanwords, competitor names, superlatives..."],
  "engagement": {"likes": 0, "comments": 0, "shares": 0},
  "rule_breaks": "anything that deviates from the channel's apparent system: guest author, co-brand, crisis notice, other language",
  "confidence_notes": "anything you were unsure about"
}
```

`engagement` is `"unknown"` when the corpus carries no metrics; never guess it.

## Why these fields

A generation pipeline doesn't consume adjectives — it consumes reproducible decisions, and every field maps to one:

- `channel`, `language`, `content_type` are the split keys Phase 4 re-tallies on. Without them a 45%-overall pattern can't be resolved into "90% in ads" or "always in Turkish, never in English", and a living system flattens into a false average.
- `hook_type` + `hook_verbatim`: the hook is the single highest-leverage line in social and ads. The type is what gets tallied; the verbatim line is what goes into the prompt block as the example a model imitates. The script classifies hooks by surface form (question/number/quote/statement/emoji); you add the intent forms it can't see (bold-claim, pain-point, story).
- `structure` as an *ordered list* is the writing equivalent of reading order in a layout: it's what lets a pipeline reproduce the shape (hook → proof → offer → CTA) rather than just the tone.
- `sentence_style`, `person`, `formality`: the three choices that most decide whether copy "sounds like us" — and the three that generic models default away from (they drift to medium sentences, first-plural, neutral-polite). Formality needs its *marker* because the same brand can be casual in Swedish and formal in Turkish.
- `emoji_usage.which` and `hashtags.verbatim` matter more than the counts: a brand doesn't "use emoji", it uses *these four*, in *this* position. Same for hashtags — a fixed trailing block of brand tags is a rule; scattered topical tags are a variation.
- `cta_verbatim` + `cta_type` and `offer_framing` + `urgency_device` are split out because they differ by channel more than any other dimension (an ad says "Shop now, 30% off today only"; a blog says "Read the full guide"), and because offer mechanics are what performance data correlates with.
- `recurring_phrases` and `sign_off` are the brand vocabulary. They're the fastest way for a reader to recognise the brand and the easiest thing for a pipeline to get right once listed verbatim.
- `taboo_or_absent` is negative space. "Never uses exclamation marks", "never mentions price", "never says 'we'" are rules a pipeline needs spelled out, and they only surface if every reader records what is missing, not just what is present.
- `rule_breaks` is how Phase 4 discovers sub-systems (guest posts, a co-brand, the English-language ads) instead of diluting the core rules with them.
- `engagement` joins performance to pattern. Keep it raw; tiering happens in Phase 4 with the caveats stated.
