---
name: writing-style-extraction
description: Reverse-engineer a brand's verbal identity — voice, tone, structure, hooks, CTAs, offer framing, emoji/hashtag policy, formality, person, language mix — from a corpus of existing copy (social captions, blog/long-form articles, ad copy, website page copy). Produces a structured voice guideline plus a per-channel "voice prompt block" for on-brand AI copywriting. Use this whenever the user wants brand voice, writing style or tone-of-voice analysis, a voice or style guide, "make copy sound like us", "write like our brand", or asks to analyze their captions, blog posts, ads or website copy — even if they just point at a folder of texts or a post export.
license: MIT
metadata:
  author: POPJAM (https://popjam.io)
---

# Writing Style Extraction

Reverse-engineer a brand's verbal DNA from the copy it already publishes, and codify it so a copywriter or a generation pipeline reproduces *that* voice instead of a generic one.

The core insight mirrors visual guideline extraction: a voice extracted from N texts is only as good as (a) how representative the corpus is across channels, and (b) how rigorously you separate *rules* (what the brand always does) from *variations* (what it does per channel, campaign type or language) and *exceptions* (one-offs). A brand that writes 40-character emoji-led captions and 1,500-word how-to articles has one voice and two systems — averaging them produces a voice nobody wrote. The whole workflow is built around that separation.

Work through five phases in order. Phase 3's extraction fan-out is the expensive step; everything else is cheap.

## Phase 1 — Corpus inventory

Locate the texts. Usually the user provides a folder or an export (CSV/JSON of posts, a crawl, an ad-library dump); if they name sources (Instagram, blog, Meta Ad Library, website) gather what's accessible first, but never block on missing sources — work with what exists and record the gaps in the coverage section.

Build `work/corpus.jsonl`, one line per text unit, tagged by channel:

```json
{"id": "ig-2026-04-12", "channel": "social | long_form | ads | web", "text": "verbatim", "language": "tr",
 "date": "2026-04-12", "engagement": {"likes": 412, "comments": 9}, "source_hint": "instagram | blog/how-to | meta-ad | pricing page"}
```

- **Channel is the primary axis.** Social captions, long-form articles, ad copy and page copy follow different sub-systems even at brands with a strong voice; keep them distinguishable from the start or Phase 4 averages them away.
- Keep text verbatim — no cleanup, no trimming of hashtags or emoji; those are the evidence. Strip only boilerplate that isn't the brand's voice (cookie banners, nav menus, legal footers) and note that you did.
- Dates and engagement are optional but valuable: they let Phase 4 say which patterns are current and which perform.
- **Corpus size:** 40–120 texts with ≥10 per channel is the sweet spot. Under ~8 in a channel, that channel's block is provisional — say so. Over ~150, sample proportionally per channel and date rather than reading everything.

## Phase 2 — Programmatic stats

Run `scripts/text_stats.py work/corpus.jsonl -o work/stats.json` (also accepts a folder of `.txt`/`.md` files in `social/`, `long_form/`, `ads/`, `web/` subfolders). Pure standard library. It is the ground truth for lengths (chars, words, sentences, paragraphs), emoji/hashtag/mention/link counts, question and exclamation rates, first- and second-person rates, CTA presence, hook type, caps rate, reading grade, and the language of each text — per sample and aggregated per channel.

Numbers from this script beat impressions: LLM readers systematically overestimate emoji use and underestimate length variance. Anchor every quantitative claim in the guideline to `stats.json`, and let the reading pass own what the script can't see — *why* a hook works, what the offer framing is, which words are taboo.

## Phase 3 — Per-channel pattern extraction

Fan out subagents by channel (and by language if the corpus is mixed), 15–25 texts per agent, each agent reading every text in full — never let an agent infer style from titles, IDs or the stats file; that defeats the entire purpose. Give each agent the schema from `references/style-schema.md` and have it write one JSON entry per text to its own output file.

Tell each agent explicitly:
- quote hooks, CTAs, sign-offs and recurring phrases **verbatim** in the source language — paraphrases destroy the evidence, and the prompt block needs the real words
- record structure as an *ordered list of parts* (hook → context → proof → offer → CTA → hashtags), not a summary
- record what is conspicuously *absent* (no emoji, no discounts, never "we", never an exclamation mark) — negative space is a rule too
- flag anything that looks like a deliberate departure (guest author, co-branded post, crisis notice, a different language) so Phase 4 can isolate it instead of averaging it in

## Phase 4 — Synthesis

Aggregate the extraction JSON with `stats.json` and tally every dimension per channel and across the corpus (a small Python script over the JSONL beats eyeballing): hook type, structure template, person, formality, CTA type and wording, offer framing, urgency device, emoji and hashtag policy, sentence style, recurring phrases, language mix. Classify:

- **≥70% of texts** → core rule. Codify it.
- **30–70%** → variation. Find the trigger: split by channel, campaign type (launch / promo / educational / community), language or date and re-tally. A hook that is 45% overall but 90% inside ads is an ads rule, not noise. Document every trigger explicitly.
- **<30%** → exception. List as observed-but-not-a-rule; never codify.

Every rule carries an evidence count ("31/38 social captions") or names example IDs — unverifiable rules get challenged by writers and ignored by pipelines. Where engagement exists, note which patterns sit in the top tier, honestly (small samples, format and timing confounds).

Write the guideline following `references/voice-template.md` (10 sections, then the prompt-block template); read it before writing — it encodes the section-level expectations and the rule/variation/exception labeling. Then distill one **voice prompt block per channel**: compact, no prose, verbatim hook and CTA examples. This is what a generation pipeline consumes; treat it as a deliverable equal to the document. Rules and attributes are written in English; verbatim examples keep the source language; the block states which language(s) to write in.

## Phase 5 — Validation

Hold out one corpus text per channel. From the voice prompt block *alone* (no other corpus access) rewrite its brief — same topic, same offer — then run original and rewrite through `text_stats.py` and diff: length, emoji/hashtag counts, person, hook type, CTA presence and reading grade should land inside the channel's observed range. A miss is either a generation slip or, just as often, a missing or ambiguous rule in the block — fix the block, not only the sample. Then read the pair side by side for what stats miss: vocabulary, warmth, taboo words.

## Deliverables

Save to the user's workspace folder: the voice guideline (markdown unless the user asks for docx/pdf), the voice prompt block(s), and a `data/` subfolder with `corpus.jsonl`, `stats.json` and the per-text extraction JSONs. Intermediate scratch goes in `work/`, not the deliverable folder. End the document with coverage: the channels, languages, campaign types and date range the corpus did NOT contain, so future users know which rules are extrapolations.
