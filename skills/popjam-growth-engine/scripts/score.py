#!/usr/bin/env python3
"""Deterministic engagement scoring + insight aggregation (POPJAM parity).

The LLM never computes engagement_score. It rates six dimensions 0-10 per persona
(attention, relevance, emotional_resonance, persuasion, brand_fit, clarity); this
script turns those into a 0-100 score using POPJAM's exact weight pipeline:
platform base weights -> content-type multiplier (re-normalized) -> persona-trait
adjustments (floor 0.01, re-normalized) -> weighted sum * 10, clamped 0-100.

Usage:
  score.py score     --reactions simulations/<id>/reactions.json \
                     --personas personas/<aud-slug> \
                     [--platform TIKTOK] [--subject-type AD] [--no-persona-adjust]
  score.py aggregate --reactions simulations/<id>/reactions.json \
                     [--out simulations/<id>/insight.json]

`score` fills reaction["engagement_score"] in place (writes the file back).
`aggregate` computes the insight's calculated fields; the LLM fills only the
narrative fields (summary_text, top_feedback_themes, recommended_actions) after.
Platform/subject_type default from the reactions file's own metadata if present.
"""

from __future__ import annotations

import argparse
import json
import statistics
import sys
from pathlib import Path

DIMENSIONS = ["attention", "relevance", "emotional_resonance", "persuasion", "brand_fit", "clarity"]

# Each row sums to 1.0. Methodology: AIDA, System1 Star Rating, Kantar LINK+.
PLATFORM_WEIGHTS = {
    "FACEBOOK":  [0.25, 0.20, 0.20, 0.15, 0.10, 0.10],
    "INSTAGRAM": [0.25, 0.15, 0.25, 0.15, 0.10, 0.10],
    "TIKTOK":    [0.30, 0.15, 0.25, 0.10, 0.10, 0.10],
    "GOOGLE":    [0.10, 0.25, 0.10, 0.20, 0.10, 0.25],
    "YOUTUBE":   [0.25, 0.15, 0.25, 0.15, 0.10, 0.10],
    "LINKEDIN":  [0.15, 0.25, 0.10, 0.20, 0.15, 0.15],
    "TWITTER":   [0.25, 0.20, 0.20, 0.15, 0.10, 0.10],
    "REDDIT":    [0.20, 0.25, 0.15, 0.15, 0.10, 0.15],
}
DEFAULT_WEIGHTS = [0.20, 0.20, 0.20, 0.15, 0.10, 0.15]

# Multipliers on platform weights, then re-normalized back to the original sum.
CONTENT_TYPE_WEIGHTS = {
    "AD":           [1.0, 1.0, 1.0, 1.0, 1.0, 1.0],
    "POST":         [1.0, 1.0, 1.0, 1.0, 1.0, 1.0],
    "BLOG":         [0.7, 1.3, 0.9, 1.0, 1.0, 1.3],
    "EMAIL":        [1.4, 1.1, 0.9, 1.4, 0.8, 1.0],
    "PRESENTATION": [0.8, 1.0, 0.9, 1.0, 1.3, 1.3],
}

# trait -> (dimension, max_adjustment); delta = trait_value * max_adjustment.
# environmental_consciousness intentionally has no adjustment (POPJAM parity).
TRAIT_ADJUSTMENTS = {
    "design_appreciation":          ("brand_fit", 0.30),
    "emotional_engagement":         ("emotional_resonance", 0.30),
    "pragmatism":                   ("clarity", 0.20),
    "price_sensitivity":            ("persuasion", 0.25),
    "social_influence_sensitivity": ("relevance", 0.20),
    "novelty_seeking":              ("attention", 0.20),
    "risk_aversion":                ("persuasion", -0.15),
    "brand_loyalty":                ("brand_fit", 0.20),
    "convenience_preference":       ("clarity", 0.15),
    "value_orientation":            ("persuasion", 0.20),
    "tech_savviness":               ("attention", 0.10),
}

SCORING_FALLBACK = dict(zip(DIMENSIONS, [2, 2, 2, 2, 3, 3]))


def compute_engagement_score(scoring: dict, platform: str | None, subject_type: str | None,
                             traits: dict | None) -> int:
    weights = list(PLATFORM_WEIGHTS.get((platform or "").upper(), DEFAULT_WEIGHTS))

    multipliers = CONTENT_TYPE_WEIGHTS.get((subject_type or "AD").upper())
    if multipliers:
        original_sum = sum(weights)
        weights = [w * m for w, m in zip(weights, multipliers)]
        s = sum(weights)
        if s > 0:
            weights = [w * original_sum / s for w in weights]

    if traits:
        idx = {d: i for i, d in enumerate(DIMENSIONS)}
        for trait, (dim, max_adj) in TRAIT_ADJUSTMENTS.items():
            value = traits.get(trait)
            if isinstance(value, (int, float)):
                weights[idx[dim]] += float(value) * max_adj
        weights = [max(w, 0.01) for w in weights]
        s = sum(weights)
        weights = [w / s for w in weights]

    raw = sum(float(scoring.get(d, 0)) * w for d, w in zip(DIMENSIONS, weights))
    return max(0, min(100, round(raw * 10)))


def load_reactions_doc(path: Path) -> tuple[dict, list[dict]]:
    doc = json.loads(path.read_text())
    if isinstance(doc, list):
        return {"reactions": doc}, doc
    return doc, doc.get("reactions", [])


def load_personas(path: Path) -> dict[str, dict]:
    """Map persona id/slug -> behavioral trait dict from a dir of JSONs or one file.

    Canonical shape (POPJAM parity): the 12 floats live as top-level persona fields.
    Older/nested shapes ({"behavioral": {...}} or {"traits": {...}}) are tolerated.
    """
    trait_names = set(TRAIT_ADJUSTMENTS) | {"environmental_consciousness"}
    personas: dict[str, dict] = {}
    files = sorted(path.glob("*.json")) if path.is_dir() else [path]
    for f in files:
        data = json.loads(f.read_text())
        items = data if isinstance(data, list) else [data]
        for p in items:
            traits = {k: v for k, v in p.items()
                      if k in trait_names and isinstance(v, (int, float))}
            if not traits:
                for nested_key in ("behavioral", "behavioral_traits", "traits"):
                    nested = p.get(nested_key)
                    if isinstance(nested, dict):
                        traits = nested
                        break
            for key in (p.get("id"), p.get("slug"), f.stem if len(items) == 1 else None):
                if key:
                    personas[str(key)] = traits
    return personas


def cmd_score(args: argparse.Namespace) -> int:
    path = Path(args.reactions)
    doc, reactions = load_reactions_doc(path)
    if not reactions:
        print(f"error: no reactions found in {path}", file=sys.stderr)
        return 1
    platform = args.platform or doc.get("platform")
    subject_type = args.subject_type or doc.get("subject_type") or "AD"
    personas = {} if args.no_persona_adjust else load_personas(Path(args.personas)) if args.personas else {}

    unmatched = []
    for r in reactions:
        if "persona_id" not in r and "persona" in r:
            r["persona_id"] = r.pop("persona")
        scoring = r.get("scoring")
        if not scoring or any(d not in scoring for d in DIMENSIONS):
            scoring = {**SCORING_FALLBACK, **(scoring or {})}
            r["scoring"] = scoring
            r["scoring_fallback"] = True
        bad = [d for d in DIMENSIONS if not (0 <= float(scoring[d]) <= 10)]
        if bad:
            print(f"error: {r.get('persona_id')} has out-of-range dims {bad}", file=sys.stderr)
            return 1
        traits = personas.get(str(r.get("persona_id", "")))
        if personas and traits is None:
            unmatched.append(str(r.get("persona_id")))
        r["engagement_score"] = compute_engagement_score(scoring, platform, subject_type, traits)

    path.write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n")
    scores = [r["engagement_score"] for r in reactions]
    print(f"scored {len(scores)} reactions (platform={platform or 'default'}, "
          f"subject_type={subject_type}): mean={statistics.fmean(scores):.1f} "
          f"min={min(scores)} max={max(scores)}")
    if unmatched:
        print(f"warning: no persona match for {unmatched} — scored without trait adjustments",
              file=sys.stderr)
    return 0


def cmd_aggregate(args: argparse.Namespace) -> int:
    path = Path(args.reactions)
    doc, reactions = load_reactions_doc(path)
    if not reactions:
        print(f"error: no reactions found in {path}", file=sys.stderr)
        return 1
    missing = [r.get("persona_id") for r in reactions if r.get("engagement_score") is None]
    if missing:
        print(f"error: run `score` first — engagement_score missing for {missing}", file=sys.stderr)
        return 1

    sentiments = [str(r.get("sentiment", "")).lower() for r in reactions]
    counts = {s: sentiments.count(s) for s in ("positive", "neutral", "negative")}
    total = len(reactions)
    top_ratio = max(counts.values()) / total
    consensus = "High" if top_ratio >= 0.7 else "Medium" if top_ratio >= 0.4 else "Low"

    labels = [r.get("engagement") for r in reactions]
    insight = {
        "concept_id": doc.get("concept_id"),
        "total_personas": total,
        "positive": counts["positive"],
        "neutral": counts["neutral"],
        "negative": counts["negative"],
        "engagement_score": round(statistics.fmean(r["engagement_score"] for r in reactions)),
        "dimension_averages": {
            d: round(statistics.fmean(float(r["scoring"][d]) for r in reactions), 4)
            for d in DIMENSIONS
        },
        "label_counts": {lbl: labels.count(lbl) for lbl in ("Will Click", "Might Click", "No Interest")},
        "consensus_level": consensus,
        # Narrative fields — filled by the LLM afterwards, never by this script.
        "summary_text": None,
        "top_feedback_themes": None,
        "recommended_actions": None,
    }
    out = json.dumps(insight, indent=2, ensure_ascii=False) + "\n"
    if args.out:
        Path(args.out).parent.mkdir(parents=True, exist_ok=True)
        Path(args.out).write_text(out)
        print(f"wrote {args.out}: engagement_score={insight['engagement_score']}, "
              f"consensus={consensus}, sentiment +{counts['positive']}/={counts['neutral']}/-{counts['negative']}")
    else:
        print(out)
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="command", required=True)

    p_score = sub.add_parser("score", help="fill engagement_score per reaction in place")
    p_score.add_argument("--reactions", required=True)
    p_score.add_argument("--personas", help="dir (or file) of persona JSONs with behavioral traits")
    p_score.add_argument("--platform", help="Platform enum; default from reactions file metadata")
    p_score.add_argument("--subject-type", help="AD/POST/BLOG/EMAIL/PRESENTATION; default AD")
    p_score.add_argument("--no-persona-adjust", action="store_true")
    p_score.set_defaults(func=cmd_score)

    p_agg = sub.add_parser("aggregate", help="compute insight calculated fields from scored reactions")
    p_agg.add_argument("--reactions", required=True)
    p_agg.add_argument("--out", help="write insight JSON here (else stdout)")
    p_agg.set_defaults(func=cmd_aggregate)

    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
