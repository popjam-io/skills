#!/usr/bin/env python3
"""Programmatic writing-style statistics across a text corpus.

Per sample: length, structure, emoji/hashtag/mention/link counts, question and
exclamation rates, first- and second-person rates, CTA presence, caps rate,
reading grade and hook type. Per channel: sample count, the mean of every
numeric field, CTA rate and hook distribution. These numbers are the ground
truth the voice guideline cites; the LLM reading pass owns intent (why a hook
works, how the offer is framed), never the counts.

Pure standard library, Python 3.10+. Pronoun, CTA and function-word lists cover
en / tr / es / sv / et; any other (or undetected) language falls back to the
union of all lists.

Usage:
    python text_stats.py <corpus_dir|corpus.jsonl> -o stats.json [--language xx]

Input formats:
    - a directory of .txt / .md files, one text per file; the channel is the
      first subfolder name when it is one of social / long_form / ads / web,
      else "unknown"
    - a JSONL file with one {"text", "channel", "language"?, "engagement"?,
      "id"?, "date"?} object per line

Definitions (one line each, so the guideline can cite them):
    chars                    characters in the trimmed text
    words                    whitespace tokens containing a letter or digit
                             (links, hashtags and mentions included)
    sentences                prose sentences: after removing links, hashtags,
                             mentions and emoji, segments ending in . ! ? ... or
                             a line break that still contain a letter or digit
    paragraphs               blocks separated by blank lines
    avg_sentence_words       prose words / sentences
    avg_paragraph_sentences  sentences / paragraphs
    question_rate            share of sentences ending in ? (¿ opener counts)
    exclamation_rate         share of sentences ending in ! (¡ opener counts)
    first_person_rate        first-person pronoun tokens / prose words
    second_person_rate       second-person pronoun tokens / prose words
    cta_present              a CTA phrase, or a sentence-initial imperative CTA
                             verb, inside the last two prose sentences
    caps_word_rate           all-caps alphabetic tokens (>= 2 letters) / prose words
    reading_grade            Flesch-Kincaid grade on the prose, syllables counted
                             as vowel groups, clamped at 0
    starts_with_hook         first line's form: emoji | quote | question | number
                             | statement (checked in that order)

Known limits, stated so the guideline can say so: Turkish and Estonian mark
person mostly with suffixes, so *_person_rate is a floor there; reading_grade
is an English-calibrated formula that runs high on agglutinative languages, so
compare it within a language, never across; number words ("five ways")
classify as "statement"; sentence splitting is punctuation- and newline-based,
so abbreviations over-split slightly and an emoji used as a separator does not
end a sentence.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path
from typing import Any

CHANNELS = ("social", "long_form", "ads", "web")
HOOK_TYPES = ("question", "number", "quote", "statement", "emoji")
LANGUAGES = ("en", "tr", "es", "sv", "et")

# Per-sample field names, in output order. This list is the contract.
FIELDS = (
    "chars",
    "words",
    "sentences",
    "paragraphs",
    "avg_sentence_words",
    "avg_paragraph_sentences",
    "emoji_count",
    "hashtag_count",
    "mention_count",
    "link_count",
    "question_rate",
    "exclamation_rate",
    "first_person_rate",
    "second_person_rate",
    "cta_present",
    "caps_word_rate",
    "reading_grade",
    "starts_with_hook",
)
NUMERIC_FIELDS = tuple(f for f in FIELDS if f not in ("cta_present", "starts_with_hook"))

# --------------------------------------------------------------------------- #
# Regexes
# --------------------------------------------------------------------------- #

def _char_class(*items: int | tuple[int, int]) -> str:
    """Regex character class from code points / (lo, hi) ranges, so the source stays ASCII."""
    parts = [chr(i) if isinstance(i, int) else f"{chr(i[0])}-{chr(i[1])}" for i in items]
    return "[" + "".join(parts) + "]"


_EMOJI_BASE = _char_class(
    (0x1F000, 0x1FAFF),  # emoticons, pictographs, transport, supplemental symbols
    (0x2600, 0x27BF),  # misc symbols + dingbats (sun, sparkles, check mark, heart, arrow)
    (0x2300, 0x23FF),  # misc technical (watch, alarm clock, fast-forward)
    (0x2B00, 0x2BFF),  # star, up/down arrows, black square
    0x203C, 0x2049, (0x2194, 0x2199), 0x21A9, 0x21AA, 0x25B6, 0x25C0, (0x25FB, 0x25FE),
    0x2934, 0x2935, 0x3030, 0x303D, 0x3297, 0x3299,
)
_EMOJI_MOD = _char_class(0xFE0F, (0x1F3FB, 0x1F3FF)) + "*"  # variation selector + skin-tone modifiers
_ZWJ = chr(0x200D)
EMOJI_RE = re.compile(
    _char_class((0x1F1E6, 0x1F1FF)) + "{2}"  # flag pairs
    + "|[0-9#*]" + chr(0xFE0F) + "?" + chr(0x20E3)  # keycaps
    + f"|{_EMOJI_BASE}{_EMOJI_MOD}(?:{_ZWJ}{_EMOJI_BASE}{_EMOJI_MOD})*"  # ZWJ sequences
)
HASHTAG_RE = re.compile(r"(?<![\w#])#(\w*[^\W\d_]\w*)")  # needs a letter: "#1" is a number
MENTION_RE = re.compile(r"(?<![\w.])@\w(?:[\w.]*\w)?")  # not emails (preceded by a word char)
LINK_RE = re.compile(
    r"https?://\S+|www\.\S+"
    r"|(?<![\w@.])[\w-]+(?:\.[\w-]+)*\.(?:com|net|org|io|co|ai|app|dev|shop|store|me|ly|link|eu"
    r"|tr|se|ee|es|uk|de|fi|no|dk)(?:/\S*)?(?!\w)",
    re.IGNORECASE,
)
TOKEN_RE = re.compile(r"\S+")
WORD_RE = re.compile(r"[^\W\d_]+(?:'[^\W\d_]+)*")  # alphabetic tokens incl. contractions
VOWEL_GROUP_RE = re.compile(r"[aeiouyáàâäãåæéèêëíìîïóòôöõøúùûüýÿıœ]+")
_SENT_RE = re.compile(r"\S.*?(?:[.!?…]+[\"”’)»]*(?=\s|$)|$)")
_TERMINAL_RE = re.compile(r"([.!?…]+)[\"”’)»]*$")
_LEADING_NONWORD_RE = re.compile(r"^[\W_]+")
_QUOTE_OPENERS = "\"“«„‘'"
_MARKDOWN_LEAD_RE = re.compile(r"^(?:[#>*\-]+\s*)+")  # markdown heading / bullet / quote markers
_LINE_LEAD_RE = re.compile(r"^(?:[#>]+\s*|[-*•–—]\s+|\d{1,3}[.)]\s+)+")  # + numbered-list markers ("1. ")

# --------------------------------------------------------------------------- #
# Multilingual word lists (lowercase; Turkish dotless-i handled by _lower)
# --------------------------------------------------------------------------- #

FIRST_PERSON = {
    "en": "i me my mine myself we us our ours ourselves i'm i've i'll i'd we're we've we'll we'd".split(),
    "tr": "ben beni bana bende benden benim benimle biz bizi bize bizde bizden bizim bizimle bizler kendim kendimiz".split(),
    "es": "yo me mí mi mis mío mía míos mías conmigo nosotros nosotras nos nuestro nuestra nuestros nuestras".split(),
    "sv": "jag mig min mitt mina vi oss vår vårt våra".split(),
    "et": "ma mina mind mul mulle minu mu minust minuga me meie meid meil meile meist meiega".split(),
}
SECOND_PERSON = {
    "en": "you your yours yourself yourselves you're you've you'll you'd".split(),
    "tr": "sen seni sana sende senden senin seninle siz sizi size sizde sizden sizin sizinle sizler kendin kendiniz".split(),
    "es": "tú tu tus te ti tuyo tuya tuyos tuyas contigo usted ustedes vosotros vosotras os vuestro vuestra vuestros vuestras".split(),
    "sv": "du dig din ditt dina ni er ert era".split(),
    "et": "sa sina sind sul sulle sinu su sinust sinuga te teie teid teil teile teist teiega".split(),
}

# CTA phrases are matched anywhere inside the last two prose sentences; CTA
# starters are single imperative verbs matched only at the start of one of them.
CTA_PHRASES = {
    "en": [
        "shop now", "buy now", "order now", "sign up", "learn more", "get started", "try it free",
        "try for free", "start free", "free trial", "book now", "book a demo", "get yours", "click the link",
        "link in bio", "link in the bio", "tap the link", "swipe up", "see more", "read more", "find out more",
        "get in touch", "contact us", "grab yours", "save your spot", "dm us", "comment below", "tag a friend",
        "tag someone", "follow us", "don't miss", "check out", "watch now", "apply now", "start now",
        "start today", "get the app", "pre-order", "add to cart", "join us", "visit us",
    ],
    "tr": [
        "hemen al", "şimdi al", "satın al", "satın alın", "sipariş ver", "sipariş verin", "hemen sipariş",
        "kaydol", "kaydolun", "hemen kaydol", "başvur", "başvurun", "hemen başvur", "tıkla", "tıklayın",
        "linke tıkla", "biyografideki link", "profildeki link", "bio'daki link", "incele", "inceleyin",
        "hemen incele", "keşfet", "keşfedin", "hemen keşfet", "bize ulaşın", "bize ulaş", "bizi takip",
        "takip et", "takip edin", "etiketle", "etiketleyin", "kaçırma", "kaçırmayın", "hemen başla",
        "ücretsiz dene", "hemen dene", "deneyin", "randevu al", "hemen indir", "indir", "indirin", "abone ol",
        "katıl", "katılın", "göz at", "göz atın", "detaylar için", "daha fazlası için", "yorumlara yaz",
        "yorumlarda", "dm at", "dm'den", "mesaj at", "ziyaret et", "ziyaret edin",
    ],
    "es": [
        "compra ahora", "compra ya", "cómpralo", "pide ahora", "pídelo", "reserva ahora", "reserva ya",
        "regístrate", "inscríbete", "suscríbete", "descubre", "descúbrelo", "descarga", "descárgala",
        "descárgalo", "prueba gratis", "pruébalo", "empieza ahora", "empieza hoy", "comienza ahora",
        "más información", "más info", "saber más", "conoce más", "haz clic", "haz click", "link en la bio",
        "link en bio", "enlace en la bio", "enlace en bio", "síguenos", "contáctanos", "escríbenos",
        "no te lo pierdas", "etiqueta a", "comenta", "comparte", "únete", "visítanos", "consigue",
        "aprovecha", "llámanos", "solicita",
    ],
    "sv": [
        "köp nu", "köp här", "beställ nu", "beställ här", "boka nu", "boka här", "boka din", "boka ditt",
        "läs mer", "upptäck", "prova gratis", "testa gratis", "börja nu", "kom igång", "registrera dig",
        "anmäl dig", "ladda ner", "ladda ned", "följ oss", "kontakta oss", "hör av dig", "klicka här",
        "klicka på länken", "länk i bio", "länken i bion", "länk i bion", "missa inte", "tagga en vän",
        "tagga någon", "kommentera", "dela", "gå med", "besök", "ta del av", "prenumerera", "skaffa",
        "se mer", "läs hela",
    ],
    "et": [
        "osta nüüd", "osta kohe", "telli nüüd", "telli kohe", "broneeri", "loe lähemalt", "loe edasi",
        "loe rohkem", "vaata lähemalt", "vaata lisaks", "avasta", "proovi tasuta", "alusta kohe",
        "alusta tasuta", "registreeru", "liitu", "laadi alla", "lae alla", "jälgi meid", "võta ühendust",
        "kirjuta meile", "kliki", "klõpsa", "vajuta lingile", "link bios", "link profiilis", "ära jäta",
        "ära maga maha", "märgi sõber", "märgi keegi", "kommenteeri", "jaga", "külasta", "tutvu",
        "kasuta ära", "haara", "hangi", "uuri lähemalt", "leia rohkem",
    ],
}
CTA_STARTERS = {
    "en": "shop buy order book reserve register subscribe download join apply claim grab visit discover explore "
    "upgrade unlock dm comment tag share follow contact call preorder try start".split(),
    "tr": "kaydol kaydolun başvur başvurun tıkla tıklayın incele inceleyin keşfet keşfedin indir indirin katıl "
    "katılın başla başlayın dene deneyin etiketle etiketleyin paylaş paylaşın".split(),
    "es": "compra pide reserva regístrate suscríbete descubre descarga prueba empieza comienza visita únete "
    "comparte comenta etiqueta consigue aprovecha solicita".split(),
    "sv": "köp beställ boka upptäck prova testa börja registrera anmäl ladda följ kontakta klicka kommentera dela "
    "besök prenumerera skaffa tagga".split(),
    "et": "osta telli broneeri avasta proovi alusta registreeru liitu laadi lae jälgi kliki klõpsa kommenteeri "
    "jaga külasta tutvu uuri hangi haara vaata loe".split(),
}

# Distinctive function words for cheap language detection (ambiguous ones removed:
# "en", "de", "on", "her", "sen", "mu" all collide across these languages).
FUNCTION_WORDS = {
    "en": "the and you your for with this that our are is to of it we now get from at be have".split(),
    "tr": "ve bir bu için ile çok daha mi mı şimdi hemen yeni ne siz biz gibi kadar olan".split(),
    "es": "el la los las del que y un una con para por es tu tus más ahora nuestro nuestra como lo".split(),
    "sv": "och att det är för med du din ditt dina vi på som ett till av nu här inte våra vår kan har".split(),
    "et": "ja et mis meie sinu sina oma või kui nüüd ka ei siin kõik meil sul uus veel ning selle iga sa".split(),
}


def _union(lists: dict[str, list[str]]) -> set[str]:
    return {w for words in lists.values() for w in words}


def _lower(text: str, lang: str | None) -> str:
    """Lowercase with Turkish dotted/dotless i handled (str.lower turns İ into i + U+0307)."""
    text = text.replace("İ", "i").replace("’", "'")
    if lang == "tr":
        text = text.replace("I", "ı")
    return text.lower()


# --------------------------------------------------------------------------- #
# Primitives
# --------------------------------------------------------------------------- #


def normalize(text: str) -> str:
    return text.replace("\r\n", "\n").replace("\r", "\n").strip()


def prose_text(text: str) -> str:
    """Text with links, hashtags, mentions, emoji and line-leading list/heading markers removed (lines kept)."""
    text = LINK_RE.sub(" ", text)
    text = HASHTAG_RE.sub(" ", text)
    text = MENTION_RE.sub(" ", text)
    text = EMOJI_RE.sub(" ", text)
    lines = (_LINE_LEAD_RE.sub("", line.strip()) for line in text.split("\n"))
    return "\n".join(re.sub(r"[ \t]+", " ", line).strip() for line in lines)


def split_paragraphs(text: str) -> list[str]:
    return [p for p in re.split(r"\n\s*\n", text.strip()) if p.strip()]


def split_sentences(text: str) -> list[str]:
    """Sentences per line; a line break always ends a sentence. Drops segments without a letter/digit."""
    out: list[str] = []
    for line in text.split("\n"):
        for m in _SENT_RE.finditer(line):
            s = m.group(0).strip()
            if s and re.search(r"\w", s):
                out.append(s)
    return out


def count_words(text: str) -> int:
    return sum(1 for t in TOKEN_RE.findall(text) if re.search(r"\w", t))


def count_emoji(text: str) -> int:
    return len(EMOJI_RE.findall(text))


def count_syllables(word: str) -> int:
    return max(1, len(VOWEL_GROUP_RE.findall(word.lower())))


def _terminal(sentence: str) -> str:
    m = _TERMINAL_RE.search(sentence)
    return m.group(1) if m else ""


def is_question(sentence: str) -> bool:
    return "?" in _terminal(sentence) or sentence.startswith("¿")


def is_exclamation(sentence: str) -> bool:
    return "!" in _terminal(sentence) or sentence.startswith("¡")


def detect_language(text: str) -> str:
    """Function-word vote across en/tr/es/sv/et; 'unknown' on no hits or a tie."""
    tokens = WORD_RE.findall(_lower(text, None))
    if not tokens:
        return "unknown"
    scores = {lang: sum(1 for t in tokens if t in words) for lang, words in FUNCTION_WORDS.items()}
    best = max(scores.values())
    if best == 0:
        return "unknown"
    winners = [lang for lang, s in scores.items() if s == best]
    return winners[0] if len(winners) == 1 else "unknown"


def person_rates(prose: str, lang: str | None) -> tuple[float, float]:
    """(first_person_rate, second_person_rate) over prose words; lists per language, union when unknown."""
    tokens = WORD_RE.findall(_lower(prose, lang))
    n_words = count_words(prose)
    if not n_words:
        return 0.0, 0.0
    first = set(FIRST_PERSON[lang]) if lang in FIRST_PERSON else _union(FIRST_PERSON)
    second = set(SECOND_PERSON[lang]) if lang in SECOND_PERSON else _union(SECOND_PERSON)
    return (
        round(sum(1 for t in tokens if t in first) / n_words, 3),
        round(sum(1 for t in tokens if t in second) / n_words, 3),
    )


def has_cta(sentences: list[str], lang: str | None) -> bool:
    """CTA phrase anywhere in, or imperative CTA verb opening, one of the last two prose sentences.

    English CTAs leak into every market's copy, so the English list is always active on top of the
    detected language's list; an unknown language uses the union of all lists.
    """
    tail = sentences[-2:]
    if not tail:
        return False
    if lang in CTA_PHRASES:
        phrases = set(CTA_PHRASES[lang]) | set(CTA_PHRASES["en"])
        starters = set(CTA_STARTERS[lang]) | set(CTA_STARTERS["en"])
    else:
        phrases, starters = _union(CTA_PHRASES), _union(CTA_STARTERS)
    joined = " ".join(_lower(s, lang) for s in tail)
    for phrase in phrases:
        if re.search(rf"(?<!\w){re.escape(phrase)}(?!\w)", joined):
            return True
    for s in tail:
        m = WORD_RE.match(_LEADING_NONWORD_RE.sub("", _lower(s, lang)))
        if m and m.group(0) in starters:
            return True
    return False


def caps_word_rate(prose: str) -> float:
    n_words = count_words(prose)
    if not n_words:
        return 0.0
    caps = sum(1 for t in WORD_RE.findall(prose) if len(t) >= 2 and t.isupper())
    return round(caps / n_words, 3)


def reading_grade(prose: str, sentences: list[str]) -> float:
    """Flesch-Kincaid grade with vowel-group syllables; 0 when there is no prose; clamped at 0."""
    words = WORD_RE.findall(prose)
    if not words or not sentences:
        return 0.0
    syllables = sum(count_syllables(w) for w in words)
    grade = 0.39 * (len(words) / len(sentences)) + 11.8 * (syllables / len(words)) - 15.59
    return round(max(0.0, grade), 1)


def classify_hook(text: str) -> str:
    """Form of the opener: emoji | quote | question | number | statement, checked in that order."""
    t = text.strip()
    if not t:
        return "statement"
    first_line = _MARKDOWN_LEAD_RE.sub("", t.split("\n", 1)[0].strip())  # drop "# ", "- ", "> "
    if EMOJI_RE.match(first_line):
        return "emoji"
    m = _SENT_RE.search(first_line)
    first = (m.group(0) if m else first_line).strip()
    if not first:
        return "statement"
    if first[0] in _QUOTE_OPENERS:
        return "quote"
    if is_question(first):
        return "question"
    if re.match(r"[\W_]*\d", first):
        return "number"
    return "statement"


# --------------------------------------------------------------------------- #
# Per-sample stats and aggregates
# --------------------------------------------------------------------------- #


def compute_sample_stats(text: str, language: str | None = None) -> dict[str, Any]:
    """All FIELDS for one text. `language` picks the pronoun/CTA lists; None → union of lists."""
    text = normalize(text)
    prose = prose_text(text)
    sentences = split_sentences(prose)
    paragraphs = split_paragraphs(text)
    n_words = count_words(text)
    n_prose_words = count_words(prose)
    n_sent = len(sentences)
    n_para = len(paragraphs)
    first_rate, second_rate = person_rates(prose, language)
    return {
        "chars": len(text),
        "words": n_words,
        "sentences": n_sent,
        "paragraphs": n_para,
        "avg_sentence_words": round(n_prose_words / n_sent, 2) if n_sent else 0.0,
        "avg_paragraph_sentences": round(n_sent / n_para, 2) if n_para else 0.0,
        "emoji_count": count_emoji(text),
        "hashtag_count": len(HASHTAG_RE.findall(text)),
        "mention_count": len(MENTION_RE.findall(text)),
        "link_count": len(LINK_RE.findall(text)),
        "question_rate": round(sum(1 for s in sentences if is_question(s)) / n_sent, 3) if n_sent else 0.0,
        "exclamation_rate": round(sum(1 for s in sentences if is_exclamation(s)) / n_sent, 3) if n_sent else 0.0,
        "first_person_rate": first_rate,
        "second_person_rate": second_rate,
        "cta_present": has_cta(sentences, language),
        "caps_word_rate": caps_word_rate(prose),
        "reading_grade": reading_grade(prose, sentences),
        "starts_with_hook": classify_hook(text),
    }


def aggregate_stats(stats_list: list[dict[str, Any]], languages: list[str] | None = None) -> dict[str, Any]:
    """sample_count, mean_<numeric field>, cta_rate, hook_distribution (+ language_distribution if given)."""
    n = len(stats_list)
    agg: dict[str, Any] = {"sample_count": n}
    for field in NUMERIC_FIELDS:
        agg[f"mean_{field}"] = round(sum(float(s[field]) for s in stats_list) / n, 3) if n else 0.0
    agg["cta_rate"] = round(sum(1 for s in stats_list if s["cta_present"]) / n, 3) if n else 0.0
    hooks = Counter(s["starts_with_hook"] for s in stats_list)
    agg["hook_distribution"] = {h: hooks.get(h, 0) for h in HOOK_TYPES}
    if languages is not None:
        agg["language_distribution"] = dict(sorted(Counter(languages).items()))
    return agg


# --------------------------------------------------------------------------- #
# Corpus loading and CLI
# --------------------------------------------------------------------------- #


def load_corpus(path: Path, default_language: str | None = None) -> list[dict[str, Any]]:
    """[{id, channel, text, language?, engagement?, date?}] from a directory or a JSONL file."""
    samples: list[dict[str, Any]] = []
    if path.is_dir():
        for f in sorted(path.rglob("*")):
            if not f.is_file() or f.suffix.lower() not in {".txt", ".md"}:
                continue
            rel = f.relative_to(path)
            channel = rel.parts[0] if len(rel.parts) > 1 and rel.parts[0] in CHANNELS else "unknown"
            samples.append(
                {
                    "id": rel.as_posix(),
                    "channel": channel,
                    "text": f.read_text(encoding="utf-8", errors="replace"),
                    "language": default_language,
                }
            )
        return samples
    for i, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        line = line.strip()
        if not line:
            continue
        obj = json.loads(line)
        samples.append(
            {
                "id": str(obj.get("id") or f"line-{i}"),
                "channel": str(obj.get("channel") or "unknown"),
                "text": str(obj.get("text") or ""),
                "language": obj.get("language") or default_language,
                "engagement": obj.get("engagement"),
                "date": obj.get("date"),
            }
        )
    return samples


def analyze_corpus(samples: list[dict[str, Any]]) -> dict[str, Any]:
    records: list[dict[str, Any]] = []
    for s in samples:
        text = normalize(s.get("text") or "")
        if not text:
            print(f"  skip {s.get('id')}: empty text", file=sys.stderr)
            continue
        given = s.get("language")
        language = given or detect_language(text)
        record: dict[str, Any] = {
            "id": s["id"],
            "channel": s["channel"],
            "language": language,
            "language_source": "given" if given else "detected",
        }
        for key in ("date", "engagement"):
            if s.get(key) is not None:
                record[key] = s[key]
        record["stats"] = compute_sample_stats(text, language if language in LANGUAGES else None)
        records.append(record)

    by_channel: dict[str, list[dict[str, Any]]] = {}
    for r in records:
        by_channel.setdefault(r["channel"], []).append(r)
    channel_order = [c for c in CHANNELS if c in by_channel] + sorted(c for c in by_channel if c not in CHANNELS)
    return {
        "sample_count": len(records),
        "channels": {
            c: aggregate_stats([r["stats"] for r in by_channel[c]], [r["language"] for r in by_channel[c]])
            for c in channel_order
        },
        "overall": aggregate_stats([r["stats"] for r in records], [r["language"] for r in records]),
        "samples": records,
    }


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("corpus", help="directory of .txt/.md files, or a JSONL file")
    ap.add_argument("-o", "--output", required=True)
    ap.add_argument("--language", help="default language code for samples that don't carry one (en/tr/es/sv/et)")
    args = ap.parse_args()

    root = Path(args.corpus)
    if not root.exists():
        raise SystemExit(f"Not found: {root}")
    samples = load_corpus(root, args.language)
    if not samples:
        raise SystemExit(f"No texts found under {root}")

    result = {"source": str(root), **analyze_corpus(samples)}
    Path(args.output).write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")

    print(f"Analyzed {result['sample_count']} texts -> {args.output}")
    for channel, agg in result["channels"].items():
        hooks = ", ".join(f"{h} {n}" for h, n in agg["hook_distribution"].items() if n)
        langs = ", ".join(f"{k} {v}" for k, v in agg["language_distribution"].items())
        print(
            f"  {channel:<10} n={agg['sample_count']:<4} chars {agg['mean_chars']:.0f}  words {agg['mean_words']:.0f}  "
            f"emoji {agg['mean_emoji_count']:.1f}  hashtags {agg['mean_hashtag_count']:.1f}  "
            f"2nd-person {agg['mean_second_person_rate']:.2f}  cta {agg['cta_rate']:.0%}  "
            f"grade {agg['mean_reading_grade']:.1f}  hooks [{hooks}]  lang [{langs}]"
        )


if __name__ == "__main__":
    main()
