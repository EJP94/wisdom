#!/usr/bin/env python3
"""build_episodes.py - build a clean episodes.csv for the Holistic Alpha Recaps.

Python 3 standard library only. Run it isolated:

    python3 -I build_episodes.py --inventory INVENTARIO.csv --transcripts DIR/ --out episodes.csv
                                 [--report report.md] [--pairs pairs.tsv] [--no-replays]

Inputs are read-only. It writes one row per transcript file, plus one row per unavailable episode.

What it fixes or adds, compared with INVENTARIO.csv:
  - titles broken by unescaped inner quotes (243, 261, 464, 467, 484, 588, 764, 782) are rebuilt
  - a row that lists two files (404 and 404b1) becomes two rows
  - every file gets a unique id: 001 ... 816, 404b1, especial-2024-08-28 ...
  - missing dates (the 18 "manual" rows) are estimated from the neighbours and flagged
  - a suggested type: solo, interview, group, challenge, qa, guided, compilation, promo
  - guest, series and part when the title or a known list says so
  - body word count and audio minutes
  - replays: earlier episodes whose text is mostly contained in this one (175 replays five)

The type, guest and series columns are suggestions. The writer confirms them from the transcript.
"""
import argparse
import csv
import datetime as dt
import json
import os
import re
import sys
import zlib
from collections import Counter, defaultdict

VERSION = "0.1 (2026-10-28)"

COLUMNS = ["id", "episode", "title", "date", "date_estimated", "type", "guest", "series", "part",
           "words", "minutes", "replays", "stem", "recap", "status", "flags"]

# Guests found by reading the openings of all 809 transcripts on 2026-10-28.
# Titles name most of them. 566 and 577 do not, so they are listed here.
KNOWN_GUESTS = {
    "235": "Dennis Morolda",
    "528": "Charles Martin",
    "530": "Edrei McCabe",
    "532": "Scott Palmer",
    "537": "Dustin Desheles",
    "549": "Charles Martin",
    "550": "Charles Martin",
    "552": "Charles Martin",
    "553": "Charles Martin",
    "565": "Scott Palmer; Rick; Corey",
    "566": "Scott Palmer",
    "570": "Charles Martin",
    "577": "Scott Palmer",
}
GUEST_TITLE = re.compile(r"(?:Community Convos? #?\d* ?-? ?|Chats with |Convo with |\bwith )"
                         r"(Charles|Dennis Morolda|Edrei McCabe|Scott Palmer|Dustin Desheles)\b", re.I)

SERIES_ALIASES = {
    "building better sexual stamina": "Building Better Stamina",
    "21 day habit challenge": "21D Habit Challenge",
    "12 traits of the unstoppable man": "12 Traits of the Unstoppable Man",
}
TS = re.compile(r"^\[[0-9:]+\]\s?", re.M)


def parse_inventory(path):
    """Split each line by hand: the file has unescaped quotes and a ';' inside one title."""
    raw = open(path, encoding="utf-8-sig", newline="").read()
    lines = [l for l in raw.splitlines() if l.strip()]
    rows = []
    for lineno, line in enumerate(lines[1:], start=2):
        ep, estado, fecha, rest = line.split(";", 3)
        if '";"' in rest:
            t, a = rest.rsplit('";"', 1)
            title = t[1:] if t.startswith('"') else t
            archivo = a[:-1] if a.endswith('"') else a
        else:
            title, archivo = (rest.split(";", 1) + [""])[:2]
            title, archivo = title.strip('"'), archivo.strip('"')
        title = title.replace('""', '"')
        naive = next(csv.reader([line], delimiter=";"))
        fixed = len(naive) == 5 and naive[3] != title
        rows.append({"episodio": ep.strip(), "estado": estado.strip(), "fecha": fecha.strip(),
                     "titulo": title.strip(), "archivo": archivo.strip(), "title_fixed": fixed,
                     "line": lineno})
    return rows


def body_words(text):
    return len(TS.sub("", text).split())


def shingles(text, k=8, keep=8):
    """Sampled word k-shingles (crc32 % keep == 0), deterministic across runs."""
    w = re.findall(r"[a-z0-9']+", TS.sub("", text).lower())
    out = set()
    for i in range(max(0, len(w) - k + 1)):
        h = zlib.crc32(" ".join(w[i:i + k]).encode())
        if h % keep == 0:
            out.add(h)
    return out


def find_replays(texts, pairs_out=None):
    """texts: {id: text} in episode order. Returns {later_id: [(earlier_id, share_of_earlier)]}
    and {later_id: share of the later episode covered by replayed material}.
    pairs_out: optional path for a TSV of every pair sharing 5%+ of either episode's text."""
    ids = list(texts)
    sh = {i: shingles(texts[i]) for i in ids}
    index = defaultdict(list)
    for i in ids:
        for h in sh[i]:
            index[h].append(i)
    pair = Counter()
    for h, owners in index.items():
        if 1 < len(owners) < 8:
            for a in range(len(owners)):
                for b in range(a + 1, len(owners)):
                    pair[(owners[a], owners[b])] += 1
    order = {i: n for n, i in enumerate(ids)}
    if pairs_out:
        rows = []
        for (a, b), c in pair.items():
            sa, sb = c / max(1, len(sh[a])), c / max(1, len(sh[b]))
            if max(sa, sb) >= 0.05:
                rows.append((max(sa, sb), a, b, sa, sb, c))
        with open(pairs_out, "w", encoding="utf-8") as fh:
            fh.write("max_share\tepisode_a\tepisode_b\tshare_of_a\tshare_of_b\tshared_shingles\n")
            for r in sorted(rows, reverse=True):
                fh.write(f"{r[0]:.2f}\t{r[1]}\t{r[2]}\t{r[3]:.2f}\t{r[4]:.2f}\t{r[5]}\n")
    replays, covered = defaultdict(list), defaultdict(set)
    for (a, b), c in pair.items():
        early, late = (a, b) if order[a] < order[b] else (b, a)
        share = c / max(1, len(sh[early]))
        if share >= 0.6 and len(sh[early]) >= 20:
            replays[late].append((early, round(share, 2)))
            covered[late] |= sh[early] & sh[late]
    cover = {i: len(covered[i]) / max(1, len(sh[i])) for i in covered}
    return replays, cover


def guess_type(eid, title, guest, replay_cover):
    t = title.lower()
    if eid.startswith("especial") or re.search(r"free courses|announcement", t):
        return "promo"
    if replay_cover >= 0.5:
        return "compilation"
    if re.search(r"habit challenge", t):
        return "challenge"
    if re.search(r"group discussion", t) or ";" in guest:
        return "group"
    if guest:
        return "interview"
    if re.search(r"q ?& ?a|\bfaq\b|listener question", t):
        return "qa"
    if re.search(r"\bguided\b", t):
        return "guided"
    return "solo"


def series_part(title):
    m = re.match(r"(.+?)[,]?\s*(?:-\s*)?(?:Part|Pt\.?)\s*(\d+)\b", title, re.I)
    if not m:
        m = re.match(r"(12 Traits of the Unstoppable Man|Community Convos)\s*-?\s*#(\d+)", title, re.I)
    if not m:
        m = re.match(r"(21D Habit Challenge|21 Day Habit Challenge)\s*-?\s*(?:Day\s*([\d]+(?:\s*(?:-|and)\s*\d+)?)"
                     r"|(Update|Wrapup))", title, re.I)
        if m:
            name = m.group(1)
            part = (m.group(2) or m.group(3) or "").lower().replace(" and ", "-").replace(" ", "")
            return SERIES_ALIASES.get(name.lower(), name), part
        return "", ""
    name = m.group(1).strip(" -,")
    return SERIES_ALIASES.get(name.lower(), name), m.group(2)


def estimate_dates(entries):
    """Linear interpolation by episode number between the nearest dated neighbours."""
    dated = sorted((e["_num"], dt.date.fromisoformat(e["date"])) for e in entries
                   if e["_num"] is not None and e["date"])
    for e in entries:
        if e["date"] or e["_num"] is None:
            continue
        lo = [d for d in dated if d[0] < e["_num"]]
        hi = [d for d in dated if d[0] > e["_num"]]
        if lo and hi:
            (n0, d0), (n1, d1) = lo[-1], hi[0]
            frac = (e["_num"] - n0) / (n1 - n0)
            e["date"] = (d0 + dt.timedelta(days=round(frac * (d1 - d0).days))).isoformat()
        elif lo:
            e["date"] = lo[-1][1].isoformat()
        elif hi:
            e["date"] = hi[0][1].isoformat()
        e["date_estimated"] = "yes"


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--inventory", required=True)
    ap.add_argument("--transcripts", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--report")
    ap.add_argument("--pairs", help="optional TSV of every pair of episodes that share 5%%+ of their text")
    ap.add_argument("--no-replays", action="store_true")
    a = ap.parse_args(argv)

    inv = parse_inventory(a.inventory)
    files = {f[:-4] for f in os.listdir(a.transcripts) if f.endswith(".txt")}
    entries, seen = [], set()
    for r in inv:
        archivos = [x.strip() for x in r["archivo"].split(" / ")] if r["archivo"] else [""]
        titulos = [x.strip() for x in r["titulo"].split(" / ")]
        if len(titulos) != len(archivos):
            titulos = [r["titulo"]] * len(archivos)
        for arch, tit in zip(archivos, titulos):
            stem = os.path.splitext(arch)[0] if arch else ""
            num = int(r["episodio"]) if r["episodio"].isdigit() else None
            if stem.startswith("especial"):
                eid = "especial-" + (r["fecha"] or stem.split(" - ")[1])
            elif stem:
                eid = stem.split(" - ")[0]
            else:
                eid = f"{num:03d}" if num is not None else r["episodio"]
            flags = []
            if r["title_fixed"]:
                flags.append("title_fixed")
            if len(archivos) > 1:
                flags.append("shared_inventory_row")
            status = "available" if stem in files else ("unavailable" if not stem else "no_transcript")
            entries.append({"id": eid, "episode": "" if num is None else str(num), "title": tit,
                            "date": r["fecha"], "date_estimated": "", "type": "", "guest": "",
                            "series": "", "part": "", "words": "", "minutes": "", "replays": "",
                            "stem": stem, "recap": (stem + ".md") if stem else "", "status": status,
                            "flags": flags, "_num": num, "_source": r["estado"]})
            seen.add(stem)
    for stem in sorted(files - seen):
        entries.append({"id": stem.split(" - ")[0], "episode": "", "title": stem, "date": "",
                        "date_estimated": "", "type": "", "guest": "", "series": "", "part": "",
                        "words": "", "minutes": "", "replays": "", "stem": stem, "recap": stem + ".md",
                        "status": "available", "flags": ["not_in_inventory"], "_num": None, "_source": ""})

    estimate_dates(entries)

    texts = {}
    for e in entries:
        if e["status"] != "available":
            continue
        txt = open(os.path.join(a.transcripts, e["stem"] + ".txt"), encoding="utf-8").read()
        texts[e["id"]] = txt
        e["words"] = str(body_words(txt))
        jpath = os.path.join(a.transcripts, e["stem"] + ".json")
        if os.path.exists(jpath):
            try:
                d = json.load(open(jpath, encoding="utf-8"))
                e["minutes"] = str(round(float(d.get("duracion_s", 0)) / 60))
            except (ValueError, OSError):
                e["flags"].append("bad_json")
        else:
            # The repo keeps only the .txt: estimate from the last chunk start (within 1 min of the audio length)
            stamps = re.findall(r"^\[(\d+):(\d\d)\]", txt, re.M)
            if stamps:
                m, s = stamps[-1]
                e["minutes"] = str(round((int(m) * 60 + int(s) + 25) / 60))

    replays, cover = ({}, {}) if a.no_replays else find_replays(texts, a.pairs)
    for e in entries:
        eid = e["id"]
        title_guest = GUEST_TITLE.search(e["title"])
        e["guest"] = KNOWN_GUESTS.get(eid, "")
        if not e["guest"] and title_guest:
            e["guest"] = title_guest.group(1)
            e["flags"].append("guest_from_title")
        if eid in replays:
            e["replays"] = " ".join(x for x, _ in sorted(replays[eid]))
        e["type"] = guess_type(eid, e["title"], e["guest"], cover.get(eid, 0.0))
        e["series"], e["part"] = series_part(e["title"])
        if e["words"] and int(e["words"]) < 700:
            e["flags"].append("short")
        if e["date_estimated"]:
            e["flags"].append("date_estimated")
    # two neighbouring episodes whose titles share a prefix of 2+ words ("Master Your Sexual Flame | ...")
    avail = [e for e in entries if e["status"] == "available"]
    prefix = lambda t: (re.split(r" - | \| |: ", t, maxsplit=1) + [""])[0].strip() if re.search(r" - | \| |: ", t) else ""
    for x, y in zip(avail, avail[1:]):
        px = prefix(x["title"])
        if px and len(px.split()) >= 2 and px.lower() == prefix(y["title"]).lower() and not x["series"] and not y["series"]:
            x["series"], x["part"], y["series"], y["part"] = px, "1", px, "2"
            x["flags"].append("series_guess")
            y["flags"].append("series_guess")

    os.makedirs(os.path.dirname(os.path.abspath(a.out)), exist_ok=True)
    with open(a.out, "w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=COLUMNS, extrasaction="ignore")
        w.writeheader()
        for e in entries:
            row = dict(e)
            row["flags"] = " ".join(e["flags"])
            w.writerow(row)

    avail = [e for e in entries if e["status"] == "available"]
    lines = [f"# episodes.csv build report - build_episodes.py {VERSION}", "",
             f"- rows: {len(entries)} ({len(avail)} with a transcript, "
             f"{sum(e['status'] == 'unavailable' for e in entries)} unavailable)",
             f"- words in transcripts: {sum(int(e['words']) for e in avail):,}",
             f"- types: " + ", ".join(f"{k} {v}" for k, v in Counter(e['type'] for e in avail).most_common()),
             f"- titles rebuilt: " + ", ".join(e["id"] for e in entries if "title_fixed" in e["flags"]),
             f"- dates estimated: " + ", ".join(f"{e['id']} ({e['date']})" for e in entries if e["date_estimated"]),
             f"- short (< 700 words): " + ", ".join(e["id"] for e in avail if "short" in e["flags"]),
             f"- replays: " + ("; ".join(f"{k} replays " + ", ".join(f"{x} ({s:.0%})" for x, s in sorted(v))
                                         for k, v in sorted(replays.items())) or "none"),
             f"- series: " + ", ".join(sorted({e['series'] for e in avail if e['series']})),
             f"- guests: " + ", ".join(f"{e['id']} {e['guest']}" for e in avail if e["guest"]), ""]
    by_type = defaultdict(list)
    for e in avail:
        if e["type"] != "solo":
            by_type[e["type"]].append(e["id"])
    lines.append("## Non-solo episodes by suggested type")
    lines.append("")
    for k in sorted(by_type):
        lines.append(f"- {k}: " + ", ".join(by_type[k]))
    report = "\n".join(lines) + "\n"
    if a.report:
        os.makedirs(os.path.dirname(os.path.abspath(a.report)), exist_ok=True)
        with open(a.report, "w", encoding="utf-8") as fh:
            fh.write(report)
    sys.stdout.write(report)
    return 0


if __name__ == "__main__":
    sys.exit(main())
