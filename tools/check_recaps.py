#!/usr/bin/env python3
"""check_recaps.py - free, deterministic checker for Holistic Alpha Recaps.

Python 3 standard library only. Run it isolated:

    python3 -I check_recaps.py --recaps DIR/ --transcripts DIR/ [--episodes episodes.csv | --inventory INVENTARIO.csv]
                               [--out report.md] [--json report.json] [--only 001 537 ...] [--strict]

It never edits a Recap. For each Recap it reports:
  ERROR  the format contract is broken (frontmatter, TL;DR, attribution line, body lines,
         host's name in the body, links, uncorrected "Alpha Mail")
  WARN   a likely content slip worth a look: a quote that is not verbatim, a number that is
         not in the transcript, a noun the writer may have added ("stranger", "coach", "beginners",
         "studies"...), a length ratio out of band, an over-long TL;DR, too much bold,
         a frontmatter field that disagrees with episodes.csv
  LOOK   attention points for the AI reviewer (candidates, not errors): transcript passages with an
         advice, quantity or experience hedge whose closest bullet carries no hedge of that kind,
         a number far from its source passage, an absolute word ("only", "every", "nobody"...) with
         no word of its kind near its source, and, with --omissions, transcript stretches that share
         almost no words with the Recap (possible omissions)
Recipe v1 and v2 are both accepted. A Recap with "recipe: v2" in its frontmatter also gets the
v2 checks: id, type from the closed list, words, one-sentence TL;DR of at most 50 words.
  INFO   counts: words, ratio, bullets, quotes, numbers
Exit code: 0, or 1 with --strict when any ERROR was found.
"""
import argparse
import csv
import difflib
import json
import os
import re
import sys
from collections import Counter, defaultdict

VERSION = "0.4 (2026-10-28)"

# ---------------------------------------------------------------- text helpers
STOP = set("""a about above after again against all also am an and any are aren as at be because been before being
below between both but by can cannot could did do does doing don down during each few for from further get gets
getting go goes going gonna got had has have having he her here hers herself him himself his how i if in into is it
its itself just know kind let like ll lot make makes me more most much my myself no nor not now of off on once one
only or other our ours ourselves out over own really right same say says see she should so some something such
than that the their theirs them themselves then there these they thing things think this those through to too
um uh under until up us very want wanna was way we well were what when where which while who whom why will with
would yeah you your yours yourself yourselves re ve s t d m guys man okay ok actually basically gonna go""".split())

# an absolute in the Recap counts as supported when its source passage has any word of its class
ABSOLUTE_SUPPORT = {
    "only": r"only|solely|nothing but|no other|alone",
    "all": r"all|every|everything|everyone|everybody|whole|entire|each|always",
    "every": r"every|all|each|whole|entire|always|everyone|everybody|everything",
    "everyone": r"everyone|everybody|every|all|anybody|anyone",
    "everybody": r"everyone|everybody|every|all|anybody|anyone",
    "always": r"always|every time|any time|never|constantly|no matter|ever",
    "never": r"never|not ever|no one|nobody|always|not even|impossible",
    "nobody": r"nobody|no one|not one|none|never|not a single",
    "none": r"none|nothing|no one|nobody|not one|never|zero",
    "must": r"must|have to|got to|gotta|need to|needs to",
    "guarantee": r"guarantee|guaranteed|promise",
}
ABSOLUTES = list(ABSOLUTE_SUPPORT)
# nouns the writer must not add; flagged when the transcript never uses the exact word
WATCH_NOUNS = ["stranger", "strangers", "beginner", "beginners", "coach", "coaches", "expert", "experts",
               "doctor", "doctors", "member", "members", "client", "clients", "research", "researchers",
               "scientist", "scientists", "science", "study", "studies", "proven", "proof", "evidence",
               "majority"]
WATCH_ABSOLUTE = ["everyone", "everybody", "nobody", "anyone", "anybody", "always", "never"]
# type-specific hedge check: (kind, transcript pattern, Recap words that keep that kind of hedge)
HEDGE_KINDS = [
    ("advice", re.compile(r"\b(I(?:'d| would) (?:suggest|recommend|encourage)|you (?:may|might) (?:want|need) to|"
                          r"you probably (?:want|don't want) to|maybe you (?:want|could|need)|"
                          r"you could (?:try|start)|one option is)\b", re.I),
     re.compile(r"\b(may|might|maybe|suggest|suggests|suggested|recommend|recommended|could|consider|"
                r"option|ideally|can|try)\b", re.I)),
    ("quantity", re.compile(r"\b((?:some|a lot of|lots of|a few|a couple of|many|most|so many|a number of|"
                            r"plenty of|the vast majority of|a large number of) (?:of the |of you |of us )?"
                            r"(?:guys|men|people|clients|dudes|you guys|of you|of us))\b", re.I),
     re.compile(r"\b(some|many|a lot|lots|a few|a couple|several|most|plenty|majority|large number|often|"
                r"for some|certain)\b", re.I)),
    ("experience", re.compile(r"\b(for me|in my experience|my experience has been|I've found|my view is|"
                              r"my belief is|one of my (?:very )?favou?rite|every time I can remember|"
                              r"as far as I know|I don't think I've ever|I can't recall)\b", re.I),
     re.compile(r"\b(Story|personally|favorite|seem|seems|seemed|view|as far as|in (?:his|one's) experience|"
                r"for some|probably|may|might|can remember|recall|known)\b", re.I)),
]
CTA = re.compile(r"(holisticalpha\.com|holistic alpha\.com|show notes|text message|shoot me a text|"
                 r"on instagram|on telegram|on facebook|subscribe|join (?:us in |us |)(?:the )?(?:inner circle|brotherhood)|"
                 r"book a (?:free )?call|view my calendar|801|bell icon|follow button|leave a comment|"
                 r"rate and review|share this)", re.I)
MESSENGER = re.compile(r"\b(he|she|steven|stephen|the host)\s+(says|said|thinks|believes|describes|explains|"
                       r"argues|recommends|suggests|notes|claims|feels|admits|insists|shares|tells)\b", re.I)
TYPES = ("solo", "interview", "group", "qa", "guided", "challenge", "compilation", "promo")
MARKERS = ("Story:", "Guest story:", "Guest:", "Guest advice:", "Guest question:", "Host story:",
           "Listener question:", "Listener story:", "Caller:", "Quote:", "Guided practice:")


def norm_tokens(s):
    s = s.lower().replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"')
    s = s.replace("'", "")
    return re.findall(r"[a-z0-9]+(?:\.[0-9]+)?", s)


def stem(w):
    for suf in ("ingly", "edly", "ings", "ing", "ies", "ied", "es", "ed", "s", "e"):
        if w.endswith(suf) and len(w) - len(suf) >= 4:
            return w[: -len(suf)]
    return w


def content_words(tokens):
    return [stem(t) for t in tokens if len(t) >= 4 and t not in STOP and not t.isdigit()]


def strip_md(s):
    s = re.sub(r"\*\*([^*]+)\*\*", r"\1", s)
    s = re.sub(r"\*([^*]+)\*", r"\1", s)
    return s


# ---------------------------------------------------------------- numbers
UNITS = {"zero": 0, "one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6, "seven": 7, "eight": 8,
         "nine": 9, "ten": 10, "eleven": 11, "twelve": 12, "thirteen": 13, "fourteen": 14, "fifteen": 15,
         "sixteen": 16, "seventeen": 17, "eighteen": 18, "nineteen": 19}
TENS = {"twenty": 20, "thirty": 30, "forty": 40, "fifty": 50, "sixty": 60, "seventy": 70, "eighty": 80,
        "ninety": 90}
SCALES = {"hundred": 100, "thousand": 1000, "million": 1000000}
ORD = {"first": 1, "second": 2, "third": 3, "fourth": 4, "fifth": 5, "sixth": 6, "seventh": 7, "eighth": 8,
       "ninth": 9, "tenth": 10}


def numbers_in(text, spelled=True):
    """Return the set of numeric values that appear in text, as floats."""
    vals = set()
    t = text.lower().replace(",", "")
    t = t.replace("–", " - ").replace("—", " - ")
    for m in re.finditer(r"(?<![a-z0-9.])(\d+(?:\.\d+)?)(?:st|nd|rd|th|s)?(?![0-9])", t):
        try:
            vals.add(float(m.group(1)))
        except ValueError:
            pass
    if spelled:
        words = re.findall(r"[a-z]+|\d+(?:\.\d+)?", t)
        i = 0
        while i < len(words):
            w = words[i]
            if w in UNITS or w in TENS or w in ORD or (w in ("a", "an") and i + 1 < len(words) and words[i + 1] in SCALES):
                total, cur, j = 0, 0, i
                if w in ORD:
                    # "a second", "one second", "per second" are time, not the ordinal 2
                    if not (w == "second" and i > 0 and words[i - 1] in ("a", "one", "per", "each", "every")):
                        vals.add(float(ORD[w]))
                    i += 1
                    continue
                last = None
                while j < len(words):
                    x = words[j]
                    if x in UNITS and last in ("unit", "teen"):
                        break
                    if x in UNITS:
                        if last == "tens" and UNITS[x] >= 10:
                            break
                        cur += UNITS[x]
                        last = "teen" if UNITS[x] >= 10 else "unit"
                    elif x in TENS:
                        if last in ("unit", "teen", "tens"):
                            break
                        cur += TENS[x]
                        last = "tens"
                    elif x in ("a", "an") and j + 1 < len(words) and words[j + 1] in SCALES:
                        cur += 1
                    elif x in SCALES:
                        last = "scale"
                        cur = max(cur, 1) * SCALES[x]
                        if SCALES[x] >= 1000:
                            total += cur
                            cur = 0
                    elif x == "and" and j + 1 < len(words) and (words[j + 1] in UNITS or words[j + 1] in TENS):
                        pass
                    else:
                        break
                    vals.add(float(total + cur))
                    j += 1
                value = total + cur
                # "seven and a half", "nine and a half"
                if j + 2 < len(words) and words[j] == "and" and words[j + 1] == "a" and words[j + 2] == "half":
                    vals.add(value + 0.5)
                vals.add(float(value))
                i = max(j, i + 1)
                continue
            i += 1
    return vals


def recap_numbers(text):
    """Numbers the Recap states, as (shown, value) pairs. Digits only, plus spelled numbers above ten."""
    out = []
    t = text.replace("–", " - ").replace("—", " - ")
    for m in re.finditer(r"(?<![A-Za-z0-9.])(\d{1,3}(?:,\d{3})+|\d+(?:\.\d+)?)(?:st|nd|rd|th)?(?![0-9])", t):
        shown = m.group(1)
        out.append((shown, float(shown.replace(",", ""))))
    for w in re.findall(r"\b[a-zA-Z]+\b", t):
        lw = w.lower()
        if lw in TENS or lw in ("hundred", "thousand", "dozen") or (lw in UNITS and UNITS[lw] > 10):
            v = TENS.get(lw) or UNITS.get(lw) or {"hundred": 100, "thousand": 1000, "dozen": 12}[lw]
            out.append((w, float(v)))
    return out


# ---------------------------------------------------------------- loading
def load_transcript(path):
    chunks = []
    with open(path, encoding="utf-8") as fh:
        for line in fh:
            line = line.rstrip("\n")
            m = re.match(r"^\[(\d+(?::\d+){1,2})\]\s?(.*)$", line)
            if m:
                chunks.append([m.group(1), m.group(2)])
            elif line.strip() and chunks:
                chunks[-1][1] += " " + line.strip()
    return chunks


def parse_frontmatter(lines):
    fm, order, end = {}, [], None
    if not lines or lines[0].strip() != "---":
        return fm, order, 0, False
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            end = i
            break
        m = re.match(r"^([A-Za-z_][A-Za-z0-9_]*):\s*(.*)$", lines[i])
        if m:
            key, val = m.group(1), m.group(2).strip()
            if val.startswith('"'):
                mm = re.match(r'^"((?:[^"\\]|\\.)*)"', val)
                val = mm.group(1).replace('\\"', '"') if mm else val
            else:
                val = re.sub(r"\s+#.*$", "", val).strip()
            fm[key] = val
            order.append(key)
    if end is None:
        return fm, order, 0, False
    return fm, order, end + 1, True


def load_inventory(path):
    """episodes.csv (comma) or INVENTARIO.csv (semicolon, UTF-8 BOM). Returns {id: row}."""
    if not path or not os.path.exists(path):
        return {}
    with open(path, encoding="utf-8-sig", newline="") as fh:
        sample = fh.read(4096)
        fh.seek(0)
        delim = ";" if sample.count(";") > sample.count(",") else ","
        rows = list(csv.DictReader(fh, delimiter=delim))
    out = {}
    for r in rows:
        if "episodio" in r:  # INVENTARIO.csv
            files = (r.get("archivo") or "").split(" / ")
            for f in files:
                stem = f.strip()[:-4] if f.strip().lower().endswith(".mp3") else f.strip()
                if stem:
                    out[stem] = {"id": stem.split(" - ")[0], "date": r.get("fecha", ""),
                                 "title": r.get("titulo", ""), "stem": stem}
        else:  # episodes.csv
            out[r.get("stem") or r.get("file", "")] = r
    return out


# ---------------------------------------------------------------- quote matching
class Source:
    def __init__(self, chunks):
        self.chunks = chunks
        self.tokens, self.tok_chunk = [], []
        for ci, (_, text) in enumerate(chunks):
            for t in norm_tokens(text):
                self.tokens.append(t)
                self.tok_chunk.append(ci)
        self.joined = " " + " ".join(self.tokens) + " "
        self.pos = defaultdict(list)
        for i, t in enumerate(self.tokens):
            self.pos[t].append(i)
        self.freq = Counter(self.tokens)
        self.numbers = numbers_in(" ".join(c[1] for c in chunks))
        self.chunk_cw = [set(content_words(norm_tokens(c[1]))) for c in chunks]
        self.chunk_lower = [c[1].lower() for c in chunks]

    def ts(self, ci):
        return self.chunks[ci][0] if 0 <= ci < len(self.chunks) else "?"

    def find_quote(self, quote):
        q = norm_tokens(quote)
        if not q:
            return "empty", 1.0, None
        if (" " + " ".join(q) + " ") in self.joined:
            k = self.joined.index(" " + " ".join(q) + " ")
            ti = self.joined[:k].count(" ")
            return "exact", 1.0, self.tok_chunk[min(ti, len(self.tok_chunk) - 1)]
        # candidate windows anchored on the rarest quote words
        cands = set()
        ranked = sorted({w for w in q if w in self.pos}, key=lambda w: self.freq[w])[:3]
        for w in ranked:
            off = q.index(w)
            for p in self.pos[w][:300]:
                cands.add(max(0, p - off))
        best, best_start = 0.0, None
        n = len(q)
        for s in cands:
            win = self.tokens[max(0, s - 3): s + n + 3]
            sm = difflib.SequenceMatcher(None, q, win, autojunk=False)
            cov = sum(b.size for b in sm.get_matching_blocks()) / n
            if cov > best:
                best, best_start = cov, s
        ci = self.tok_chunk[min(best_start, len(self.tok_chunk) - 1)] if best_start is not None else None
        if best >= 0.85:
            return "near", best, ci
        return "missing", best, ci

    def best_chunks(self, text, k=3, min_score=1):
        cw = set(content_words(norm_tokens(text)))
        if not cw:
            return []
        scored = sorted(((len(cw & c), i) for i, c in enumerate(self.chunk_cw)), reverse=True)
        return [i for sc, i in scored[:k] if sc >= min_score]


# ---------------------------------------------------------------- the checks
def check_one(recap_path, transcripts_dir, inventory, omissions=False):
    fname = os.path.basename(recap_path)
    stem = fname[:-3]
    res = {"file": fname, "errors": [], "warns": [], "looks": [], "info": {}}
    E, W, L = res["errors"].append, res["warns"].append, res["looks"].append
    text = open(recap_path, encoding="utf-8").read()
    if "\r" in text:
        W("CRLF line endings (use LF)")
    lines = text.replace("\r\n", "\n").split("\n")
    fm, order, body_start, ok = parse_frontmatter(lines)
    if not ok:
        E("frontmatter missing or not closed with ---")
    body = lines[body_start:]

    # --- frontmatter
    v2 = fm.get("recipe", "").lower().startswith("v2")
    required = ["id", "title", "date", "type", "host", "words", "recipe", "source", "section"] if v2 else \
               ["episode", "title", "date", "host", "source", "section"]
    for k in required:
        if k not in fm:
            E(f"frontmatter: missing '{k}'")
    if v2:
        if fm.get("type") and fm["type"] not in TYPES:
            E(f"frontmatter: type '{fm['type']}' is not one of {', '.join(TYPES)}")
        parts = stem.split(" - ")
        want_id = "especial-" + parts[1] if parts[0] == "especial" and len(parts) > 1 else parts[0]
        if fm.get("id") and fm["id"] != want_id:
            E(f"frontmatter: id '{fm['id']}' does not match the file name (expected '{want_id}')")
        if fm.get("type") == "compilation" and not fm.get("replays"):
            W("type is 'compilation' but there is no 'replays' field")
        if fm.get("type") in ("interview", "group") and not fm.get("guest"):
            E(f"type is '{fm['type']}' but there is no 'guest' field")
    if fm.get("section") and fm.get("section") != "recap":
        E(f"frontmatter: section is '{fm.get('section')}', expected 'recap'")
    if fm.get("host") and fm.get("host") != "Steven Mathis":
        E(f"frontmatter: host is '{fm.get('host')}', expected 'Steven Mathis'")
    if fm.get("date") and not re.match(r"^\d{4}-\d{2}-\d{2}$", fm["date"]):
        E(f"frontmatter: date '{fm['date']}' is not YYYY-MM-DD")
    src = fm.get("source", stem + ".txt")
    if src != stem + ".txt":
        E(f"frontmatter: source '{src}' does not match the file name '{stem}.txt'")
    file_id = stem.split(" - ")[0]
    ep = fm.get("episode", "")
    if file_id.isdigit() and ep and ep.isdigit() and int(ep) != int(file_id):
        E(f"frontmatter: episode {ep} does not match the file number {file_id}")
    inv = inventory.get(stem)
    if inventory and not inv:
        W("not found in the episode list (check the file name)")
    if inv:
        if v2 and inv.get("type") and fm.get("type") and inv["type"] != fm["type"]:
            W(f"frontmatter: type '{fm['type']}' differs from the episode list ('{inv['type']}'): confirm it")
        if v2 and inv.get("guest") and fm.get("guest") and inv["guest"] != fm["guest"]:
            W(f"frontmatter: guest '{fm['guest']}' differs from the episode list ('{inv['guest']}')")
        if v2 and inv.get("words") and fm.get("words") and inv["words"] != fm["words"]:
            W(f"frontmatter: words {fm['words']} differs from the episode list ({inv['words']})")
        if inv.get("date") and fm.get("date") and inv["date"] != fm["date"]:
            E(f"frontmatter: date {fm['date']} differs from the episode list ({inv['date']})")
        if not inv.get("date"):
            W("the episode list has no date for this episode")
        if inv.get("title") and fm.get("title") and inv["title"].strip() != fm["title"].strip():
            W(f"frontmatter: title differs from the episode list: '{inv['title']}'")

    # --- transcript
    tpath = os.path.join(transcripts_dir, src)
    if not os.path.exists(tpath):
        E(f"transcript not found: {src}")
        return res
    S = Source(load_transcript(tpath))
    t_words = len(S.tokens)

    # --- body structure
    tldr_idx = [i for i, l in enumerate(body) if l.startswith("> **TL;DR**")]
    attr_idx = [i for i, l in enumerate(body) if l.startswith("*") and not l.startswith("**")
                and re.search(r"Holistic Alpha (episode|special)", l)]
    bullets = [(i, l) for i, l in enumerate(body) if re.match(r"^( {2})*- \S", l)]
    if len(tldr_idx) != 1:
        E(f"expected exactly one '> **TL;DR** —' line, found {len(tldr_idx)}")
    elif not body[tldr_idx[0]].startswith("> **TL;DR** — "):
        E("TL;DR line must start with '> **TL;DR** — ' (em dash)")
    if len(attr_idx) != 1:
        E(f"expected exactly one italic attribution line, found {len(attr_idx)}")
    if bullets and tldr_idx and tldr_idx[0] > bullets[0][0]:
        E("TL;DR comes after the first bullet")
    if bullets and attr_idx and attr_idx[0] > bullets[0][0]:
        E("attribution line comes after the first bullet")
    if not bullets:
        E("no bullets")
    for i, l in enumerate(body):
        if not l.strip() or i in tldr_idx or i in attr_idx or re.match(r"^( {2})*- \S", l):
            continue
        E(f"unexpected line (only bullets after the attribution line): '{l[:60]}'")
    if attr_idx:
        a = body[attr_idx[0]]
        m = re.search(r"episode (\S+?)[,.]", a)
        if m and file_id.isdigit() and m.group(1).isdigit() and int(m.group(1)) != int(file_id):
            E(f"attribution line names episode {m.group(1)}, file is {file_id}")
        if "Not fact-checked" not in a:
            W("attribution line lacks 'Not fact-checked.'")

    bullet_text = [strip_md(l.strip()[2:]) for _, l in bullets]
    tldr = strip_md(body[tldr_idx[0]].split("—", 1)[-1]) if tldr_idx else ""
    body_plain = "\n".join(bullet_text)
    r_words = len(norm_tokens(body_plain))

    # --- name, links, leftovers
    content_lines = [l for i, l in enumerate(body) if i not in attr_idx]
    joined_content = "\n".join(content_lines)
    for m in re.finditer(r"\b(Steven|Stephen|Steve|Mathis)\b", joined_content):
        E(f"host's name in the body: '{m.group(0)}'")
    if re.search(r"Alpha Mail", text):
        E("uncorrected transcription: 'Alpha Mail'")
    if re.search(r"\[\[|\]\(|https?://", joined_content):
        E("link in the body")
    is_interview = bool(fm.get("guest"))
    guest_markers = len(re.findall(r"\*\*Guest[^*]*\*\*", joined_content))
    if is_interview and guest_markers == 0:
        E("guest in frontmatter but no **Guest...** marker in the body")
    if not is_interview and guest_markers:
        E("**Guest** markers but no 'guest' in frontmatter")
    title = fm.get("title", stem)
    etype = (inv or {}).get("type", "")
    if not is_interview and etype in ("interview", "conversation", "group"):
        W(f"the episode list types this episode as '{etype}' but there is no 'guest' field")
    elif not is_interview and not etype and re.search(
            r"(Convos?\b|Chats? with|Group Discussion|Interview|[-,] (?:a )?(?:[Cc]ommunity [Cc]onvo )?[Ww]ith [A-Z][a-z]+$)", title):
        W("title looks like a conversation but there is no 'guest' field")
    if is_interview and attr_idx and fm.get("guest", "").split()[0] not in body[attr_idx[0]]:
        W("attribution line does not name the guest")
    for m in MESSENGER.finditer(joined_content):
        (L if is_interview else W)(f"messenger phrase '{m.group(0)}' (write the idea directly)")

    # --- length
    ratio = r_words / t_words if t_words else 0
    etype2 = fm.get("type", "")
    if t_words < 700 or etype2 in ("promo", "compilation"):
        lo, hi = 0.0, 1.0   # no band: tiny episodes, promos and compilations
    elif is_interview:
        lo, hi = 0.14, 0.30
    else:
        lo, hi = 0.18, 0.36
    if ratio < lo or ratio > hi:
        W(f"length ratio {ratio:.0%} outside {lo:.0%}-{hi:.0%} (Recap {r_words} / transcript {t_words} words)")
    tl_words = len(norm_tokens(tldr))
    tl_limit = 50 if v2 else 55
    if tl_words > tl_limit:
        W(f"TL;DR has {tl_words} words (at most {tl_limit})")
    tl_sentences = len([s for s in re.split(r"(?<=[.!?])\s+(?=[A-Z])", tldr.strip()) if s.strip()])
    if tl_sentences > 1:
        W(f"TL;DR has {tl_sentences} sentences (one expected)")

    # --- bold
    for (_, l), plain in zip(bullets, bullet_text):
        spans = [s for s in re.findall(r"\*\*([^*]+)\*\*", l) if s.strip() not in MARKERS]
        if len(spans) > 1:
            W(f"more than one bold term in a bullet: {spans}")

    # --- quotes
    q_total = q_exact = 0
    all_text_for_quotes = tldr + "\n" + body_plain
    quotes = re.findall(r"\"([^\"\n]{2,400})\"|“([^”\n]{2,400})”", all_text_for_quotes)
    for a, b in quotes:
        q = a or b
        q_total += 1
        kind, score, ci = S.find_quote(q)
        if kind == "exact":
            q_exact += 1
        elif kind == "near":
            W(f"quote not verbatim ({score:.0%} of its words in order) near [{S.ts(ci)}]: \"{q[:90]}\"")
        elif kind != "empty":
            W(f"quote not found in the transcript (best {score:.0%}) : \"{q[:90]}\"")

    # --- numbers
    n_total = n_missing = 0
    reported = set()
    for shown, val in recap_numbers(tldr + "\n" + body_plain):
        n_total += 1
        if val not in S.numbers:
            n_missing += 1
            reported.add(val)
            W(f"number '{shown}' not found in the transcript")

    # --- numbers near their source passage (catches a changed small number such as 'five' for 'two or three')
    for plain in bullet_text:
        vals = numbers_in(plain)
        if not vals:
            continue
        chunks = S.best_chunks(plain, 3, min_score=5)
        region_text = " ".join(S.chunks[c][1] for c0 in chunks for c in (c0 - 1, c0, c0 + 1) if 0 <= c < len(S.chunks))
        near = numbers_in(region_text)
        for v in sorted(vals):
            if v not in S.numbers and v not in reported:
                reported.add(v)
                n_missing += 1
                W(f"number {int(v) if v == int(v) else v} not found in the transcript: \"{plain[:90]}\"")
            elif chunks and v not in (0.0, 1.0) and v in S.numbers and v not in near:
                shown = int(v) if v == int(v) else v
                where = ", ".join(S.ts(c) for c in chunks[:2]) or "?"
                L(f"number {shown} is not near the bullet's source passage [{where}]: \"{plain[:90]}\"")

    # --- absolutes without local support (a word of the same class near the source passage)
    n_abs = 0
    for plain in bullet_text:
        low = plain.lower()
        for a in ABSOLUTES:
            for m in re.finditer(r"\b" + a + r"\b", low):
                chunks = S.best_chunks(plain, 3)
                region = set()
                for c in chunks:
                    region.update([c - 1, c, c + 1])
                pat = re.compile(r"\b(" + ABSOLUTE_SUPPORT[a] + r")\b")
                supported = any(0 <= c < len(S.chunks) and pat.search(S.chunk_lower[c]) for c in region)
                if not supported:
                    n_abs += 1
                    where = ", ".join(S.ts(c) for c in chunks[:2]) or "?"
                    L(f"'{a}' has no word of its kind near its source [{where}]: \"{plain[max(0, m.start() - 40): m.end() + 40]}\"")

    # --- nouns the writer may have added
    t_vocab = set(S.tokens)
    r_vocab = Counter(norm_tokens(tldr + " " + body_plain))
    for wn in WATCH_NOUNS:
        if r_vocab.get(wn) and wn not in t_vocab:
            W(f"'{wn}' is not a word of the transcript (added detail?)")
    for wn in WATCH_ABSOLUTE:
        if r_vocab.get(wn) and wn not in t_vocab:
            L(f"'{wn}' is not a word of the transcript (check the claim is not wider than the source)")

    # --- hedge ledger: hedged transcript sentences whose closest bullet lost that kind of hedge
    n_hedged = 0
    seen = set()
    for ci, (ts, text_) in enumerate(S.chunks):
        if CTA.search(text_):
            continue
        for sent in re.split(r"(?<=[.?!])\s+", text_):
            for kind, tpat, keep in HEDGE_KINDS:
                hm = tpat.search(sent)
                if not hm:
                    continue
                n_hedged += 1
                sent_cw = set(content_words(norm_tokens(sent)))
                if len(sent_cw) < 3:
                    continue
                best, best_i = 0, None
                for bi, bt in enumerate(bullet_text):
                    ov = len(sent_cw & set(content_words(norm_tokens(bt))))
                    if ov > best:
                        best, best_i = ov, bi
                if best >= 3 and best_i is not None and (best_i, kind) not in seen \
                        and not keep.search(bullet_text[best_i]):
                    seen.add((best_i, kind))
                    L(f"[{ts}] {kind} hedge '{hm.group(0)}' -> closest bullet keeps none: "
                      f"\"{bullet_text[best_i][:110]}\"")

    # --- least-covered passages (possible omissions): the lowest 5% of chunks by shared words
    recap_vocab = set(content_words(norm_tokens(tldr + " " + body_plain)))
    n = len(S.chunks)
    intro = re.compile(r"(welcome back|this is the holistic alpha|thanks for listening|thank you for listening|"
                       r"talk to you soon|see you on the next|have an awesome|have a great|appreciate you|"
                       r"thanks for being here|thank you for being here)", re.I)
    scored = []
    for ci in range(1, n - 1):
        cw = S.chunk_cw[ci]
        if len(cw) < 8 or CTA.search(S.chunks[ci][1]) or intro.search(S.chunks[ci][1]):
            continue
        scored.append((len(cw & recap_vocab) / len(cw), ci))
    scored.sort()
    k = max(2, min(8, round(0.05 * n))) if omissions else 0
    for cov, ci in scored[:k]:
        if cov < 0.45:
            L(f"[{S.ts(ci)}] least-covered passage ({cov:.0%} shared words), possible omission: "
              f"\"{S.chunks[ci][1][:120]}...\"")

    res["info"] = {"transcript_words": t_words, "recap_words": r_words, "ratio": round(ratio, 3),
                   "tldr_words": tl_words, "bullets": len(bullets), "quotes": q_total,
                   "quotes_exact": q_exact, "numbers": n_total, "numbers_missing": n_missing,
                   "hedged_passages": n_hedged, "absolutes_unsupported": n_abs, "interview": is_interview,
                   "speaker_unclear": joined_content.count("[speaker unclear]"),
                   "unsure_word": joined_content.count("[?]")}
    return res


def file_id(name):
    """'001 - Title.md' -> '001', 'especial - 2024-12-25 - Title.md' -> 'especial-2024-12-25'."""
    parts = name.split(" - ")
    return "especial-" + parts[1] if parts[0] == "especial" and len(parts) > 1 else parts[0]


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--recaps", required=True)
    ap.add_argument("--transcripts", required=True)
    ap.add_argument("--episodes", help="episodes.csv (preferred)")
    ap.add_argument("--inventory", help="INVENTARIO.csv (fallback)")
    ap.add_argument("--only", nargs="*", help="episode ids to check, e.g. 001 537 404b1")
    ap.add_argument("--out", help="write a Markdown report here")
    ap.add_argument("--json", help="write a JSON report here")
    ap.add_argument("--no-look", action="store_true", help="omit LOOK lines from the report")
    ap.add_argument("--omissions", action="store_true",
                    help="also list the least-covered transcript passages (weak signal: about 1 in 5 is a real omission)")
    ap.add_argument("--strict", action="store_true", help="exit 1 when any ERROR is found")
    a = ap.parse_args()

    inventory = load_inventory(a.episodes or a.inventory)
    # only episode files: "001 - Title.md", "404b1 - Title.md", "especial - 2024-12-25 - Title.md"
    files = sorted(f for f in os.listdir(a.recaps)
                   if f.endswith(".md") and re.match(r"^(\d{3}[a-z0-9]*|especial - \d{4}-\d{2}-\d{2}) - ", f))
    if a.only:
        files = [f for f in files if file_id(f) in a.only]
    results = [check_one(os.path.join(a.recaps, f), a.transcripts, inventory, a.omissions) for f in files]

    out = [f"# Recap check - {len(results)} file(s) - check_recaps.py {VERSION}", "",
           "| episode | status | errors | warns | looks | transcript | recap | ratio | TL;DR | bullets | quotes ok | numbers missing |",
           "|---|---|---|---|---|---|---|---|---|---|---|---|"]
    n_err = 0
    for r in results:
        i = r["info"]
        status = "ERROR" if r["errors"] else ("WARN" if r["warns"] else "OK")
        n_err += bool(r["errors"])
        out.append(f"| {file_id(r['file'])} | {status} | {len(r['errors'])} | {len(r['warns'])} | "
                   f"{len(r['looks'])} | {i.get('transcript_words', '-')} | {i.get('recap_words', '-')} | "
                   f"{i.get('ratio', 0):.0%} | {i.get('tldr_words', '-')} | {i.get('bullets', '-')} | "
                   f"{i.get('quotes_exact', '-')}/{i.get('quotes', '-')} | {i.get('numbers_missing', '-')} |")
    for r in results:
        out += ["", f"## {r['file'][:-3]}", ""]
        for e in r["errors"]:
            out.append(f"- ERROR {e}")
        for w in r["warns"]:
            out.append(f"- WARN {w}")
        if not a.no_look:
            for l in r["looks"]:
                out.append(f"- LOOK {l}")
        if not (r["errors"] or r["warns"] or (r["looks"] and not a.no_look)):
            out.append("- OK")
    report = "\n".join(out) + "\n"
    if a.out:
        with open(a.out, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(report)
    else:
        sys.stdout.write(report)
    if a.json:
        with open(a.json, "w", encoding="utf-8") as fh:
            json.dump(results, fh, indent=1, ensure_ascii=False)
    totals = Counter("ERROR" if r["errors"] else ("WARN" if r["warns"] else "OK") for r in results)
    print(f"check_recaps: {len(results)} checked - OK {totals['OK']}, WARN {totals['WARN']}, ERROR {totals['ERROR']}",
          file=sys.stderr)
    sys.exit(1 if (a.strict and n_err) else 0)


if __name__ == "__main__":
    main()
