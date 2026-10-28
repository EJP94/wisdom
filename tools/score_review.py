#!/usr/bin/env python3
"""score_review.py - score a reviewer against an answer key of known findings.

Python 3 standard library only. Run it isolated, from the repo root:

    python3 -I tools/score_review.py --key holistic-alpha/golden/answer-key.jsonl --review review.json
        [--ids 127 275 537 663 813] [--window 90] [--loose] [--out report.md]

The key is JSONL, one known finding per line: {"id", "ts", "severity", "kind", "transcript", "recap"}.
The review can be any of:
  - the result of the recap-writeups workflow in audit mode ({"results": [{"review": [...]}]})
  - one reviewer output ({"episodes": [{"id", "ok", "findings": [...]}]}) or a list of those entries
  - JSONL of findings that carry an "id" (for example holistic-alpha/logs/findings/*.jsonl)
A review finding matches a key finding of the same episode when their [mm:ss] are at most --window
seconds apart and their quoted words share a word of 5 letters or more (--loose drops that second
test). Each finding matches at most once, closest first. Format findings are counted apart.
It prints recall by severity, the key findings the reviewer missed, and the review findings that are
not in the key: each of those is either a new real finding or a false alarm, so check them by hand.
"""
import argparse
import json
import re
import sys
from collections import Counter

VERSION = "0.1 (2026-10-28)"


def seconds(ts):
    m = re.match(r"^\[?(\d+):(\d{2})(?::(\d{2}))?\]?$", (ts or "").strip())
    if not m:
        return None
    a, b, c = m.groups()
    return int(a) * 3600 + int(b) * 60 + int(c) if c else int(a) * 60 + int(b)


def words(f):
    text = " ".join(str(f.get(k, "")) for k in ("transcript", "recap"))
    return {w for w in re.findall(r"[a-z']+", text.lower()) if len(w) >= 5}


def load_key(path):
    with open(path, encoding="utf-8") as fh:
        return [json.loads(l) for l in fh if l.strip()]


def load_review(path):
    with open(path, encoding="utf-8") as fh:
        text = fh.read()
    try:
        data = json.loads(text)
    except json.JSONDecodeError:
        return [json.loads(l) for l in text.splitlines() if l.strip()]
    entries = []
    if isinstance(data, dict) and "results" in data:
        for r in data["results"]:
            entries += r.get("review") or []
    elif isinstance(data, dict) and "episodes" in data:
        entries = data["episodes"]
    elif isinstance(data, list):
        entries = data
    out = []
    for e in entries:
        if "findings" in e:
            out += [dict(f, id=e["id"]) for f in e.get("findings") or []]
        elif "id" in e:
            out.append(e)
    return out


def match(key, review, window, loose):
    pairs = []
    for i, k in enumerate(key):
        for j, r in enumerate(review):
            if str(k["id"]) != str(r.get("id")):
                continue
            if k.get("kind") == "format" or r.get("kind") == "format":
                if k.get("kind") == r.get("kind") == "format":
                    pairs.append((0, i, j))
                continue
            tk, tr = seconds(k.get("ts")), seconds(r.get("ts"))
            if tk is None or tr is None or abs(tk - tr) > window:
                continue
            if not loose and not (words(k) & words(r)):
                continue
            pairs.append((abs(tk - tr), i, j))
    used_k, used_r, matched = set(), set(), []
    for d, i, j in sorted(pairs):
        if i in used_k or j in used_r:
            continue
        used_k.add(i)
        used_r.add(j)
        matched.append((i, j))
    return matched, used_k, used_r


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--key", required=True)
    ap.add_argument("--review", required=True)
    ap.add_argument("--ids", nargs="*", help="only these episodes (default: every episode the review covers)")
    ap.add_argument("--window", type=int, default=90)
    ap.add_argument("--loose", action="store_true")
    ap.add_argument("--out")
    a = ap.parse_args(argv)

    review = load_review(a.review)
    ids = set(a.ids) if a.ids else {str(r.get("id")) for r in review}
    key = [k for k in load_key(a.key) if str(k["id"]) in ids]
    review = [r for r in review if str(r.get("id")) in ids]
    matched, used_k, used_r = match(key, review, a.window, a.loose)

    out = [f"# Reviewer score - score_review.py {VERSION}", "",
           f"Episodes: {' '.join(sorted(ids))}. Key findings: {len(key)}. Review findings: {len(review)}.", "",
           "| severity in the key | found | total | recall |", "|---|---|---|---|"]
    for sev in ("S1", "S2", "S3"):
        tot = [i for i, k in enumerate(key) if k["severity"] == sev]
        if tot:
            got = sum(1 for i in tot if i in used_k)
            out.append(f"| {sev} | {got} | {len(tot)} | {got / len(tot):.0%} |")
    if key:
        out.append(f"| all | {len(used_k)} | {len(key)} | {len(used_k) / len(key):.0%} |")

    per_ep = Counter()
    for i in used_k:
        per_ep[str(key[i]["id"])] += 1
    out += ["", "Found per episode: " + ", ".join(
        f"{e} {per_ep[e]}/{sum(1 for k in key if str(k['id']) == e)}" for e in sorted(ids))]

    missed = [k for i, k in enumerate(key) if i not in used_k]
    out += ["", f"## Missed key findings ({len(missed)})", ""]
    out += [f"- {k['id']} [{k.get('ts') or '-'}] {k['severity']} {k.get('kind', '')}: {k.get('transcript', '')[:110]}"
            for k in sorted(missed, key=lambda k: (k['severity'], str(k['id']), seconds(k.get('ts')) or 0))]

    extra = [r for j, r in enumerate(review) if j not in used_r]
    fmt = [r for r in extra if r.get("kind") == "format"]
    extra = [r for r in extra if r.get("kind") != "format"]
    out += ["", f"## Review findings not in the key ({len(extra)}, plus {len(fmt)} format): check each by hand", ""]
    out += [f"- {r.get('id')} [{r.get('ts') or '-'}] {r.get('severity', '?')} {r.get('kind', '')}: "
            f"{str(r.get('transcript', ''))[:110]}"
            for r in sorted(extra, key=lambda r: (str(r.get('severity')), str(r.get('id')), seconds(r.get('ts')) or 0))]
    by_sev = Counter(r.get("severity", "?") for r in extra)
    out += ["", "Not in the key, by severity: " + (", ".join(f"{s} {n}" for s, n in sorted(by_sev.items())) or "none")]
    report = "\n".join(out) + "\n"
    if a.out:
        with open(a.out, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(report)
    else:
        sys.stdout.write(report)
    s2 = [i for i, k in enumerate(key) if k["severity"] == "S2"]
    print(f"score_review: S2 {sum(1 for i in s2 if i in used_k)}/{len(s2)}, all {len(used_k)}/{len(key)}, "
          f"not in key {len(extra)}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
