#!/usr/bin/env python3
"""topic_note.py - step B of the topic notes: list a topic's claims, render its note, verify it
(topic instructions v2 draft).

Python 3 standard library only. Run it isolated, from the repo root:

    python3 -I tools/topic_note.py claims <slug> [--pointers] [--dir DIR]
    python3 -I tools/topic_note.py render <slug> [--dir DIR]
    python3 -I tools/topic_note.py verify <slug> [--dir DIR]

- claims: every claim of the topic, oldest first, for the writer of step B. --pointers lists instead
  the claims of other topics that name it in also, for the reviewer
- render: reads holistic-alpha/topics/<area>/<slug>.layout and the registry, writes <slug>.md.
  Each line's text is the text of its first claim, word for word
- verify: checks the rendered note against the registry and the layout. Exit code 1 on any ERROR

Layout format (one item per line):
    in short: <at most 60 words>
    ## <section title>
    - <id> [<id> ...]          a line; the first id gives the text
      - <id> ...               nested under the line above (2 spaces per level)
      - later <id> ...         a change of view, rendered as **Later view (YEAR):**
    misplaced: <id> [<id> ...] claims that are not about the topic, left out of the note
"""

import argparse
import csv
import json
import re
import sys
from collections import Counter
from pathlib import Path

VERSION = "0.3 (2026-11-01)"
ROOT = Path(__file__).resolve().parent.parent
HA = ROOT / "holistic-alpha"
REGISTRY = HA / "claims"
LEVELS = ["general", "sexual-health", "explicit"]
ITALIC = ("*Ideas from Holistic Alpha, as told by host Steven Mathis and, where marked, his guests and "
          "listeners. Numbers in parentheses are episodes. Sources he credits are named where they appear. "
          "Not fact-checked.*")
OTHER = "In other notes"


def load_claims(folder):
    """A born proposal keeps its +slug in the registry: read it as the slug."""
    claims = {}
    for p in sorted(Path(folder).glob("*.jsonl")):
        with open(p, encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    r = json.loads(line)
                    r["topic"] = r["topic"].lstrip("+")
                    r["also"] = [a.lstrip("+") for a in r["also"]]
                    claims[r["id"]] = r
    return claims


def load_topic(slug):
    with open(HA / "topics.csv", newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            if r["slug"] == slug:
                return r
    sys.exit(f"{slug}: not in topics.csv")


def by_date(ids, claims):
    return sorted(ids, key=lambda i: (claims[i]["date"], i))


def episode_ids(ids, claims):
    eps = {}
    for i in ids:
        eps.setdefault(claims[i]["ep"], claims[i]["date"])
    return [e for e, _ in sorted(eps.items(), key=lambda kv: (kv[1], kv[0]))]


def parse_layout(path):
    """Returns (in_short, items, misplaced, errors). items: ('section', title) or ('line', depth, later, ids)."""
    in_short, items, misplaced, errors = "", [], [], []
    for n, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not raw.strip():
            continue
        if raw.startswith("in short:"):
            in_short = raw[len("in short:"):].strip()
        elif raw.startswith("## "):
            items.append(("section", raw[3:].strip()))
        elif raw.startswith("misplaced:"):
            misplaced += raw[len("misplaced:"):].split()
        else:
            m = re.match(r"^( *)- (later )?(\S.*)$", raw)
            if not m or len(m.group(1)) % 2:
                errors.append(f"layout line {n}: can't read {raw!r}")
                continue
            items.append(("line", len(m.group(1)) // 2, bool(m.group(2)), m.group(3).split()))
    return in_short, items, misplaced, errors


def note_path(topic):
    return HA / "topics" / topic["area"] / f"{topic['slug']}.md"


def render_line(depth, later, ids, claims):
    first = claims[ids[0]]
    text = ""
    if later:
        text += f"**Later view ({first['date'][:4]}):** "
    if first["marker"]:
        text += f"**{first['marker']}:** "
    text += first["claim"]
    return f"{'  ' * depth}- {text} ({', '.join(episode_ids(ids, claims))}) <!-- {' '.join(ids)} -->"


def topic_slugs():
    with open(HA / "topics.csv", newline="", encoding="utf-8") as f:
        return {r["slug"] for r in csv.DictReader(f)}


def pointer_text(home, slugs):
    """A link only to a topic of topics.csv: a proposal has no note yet."""
    return f"See [[{home}]]" if home in slugs else f"See {home}, a proposed topic"


def pointer_lines(slug, claims):
    """One line per home topic: the link and the ids, never text."""
    homes, slugs = {}, topic_slugs()
    for i in by_date([i for i, c in claims.items() if slug in c["also"]], claims):
        homes.setdefault(claims[i]["topic"], []).append(i)
    return [f"- {pointer_text(home, slugs)} ({', '.join(episode_ids(ids, claims))}) <!-- {' '.join(ids)} -->"
            for home, ids in sorted(homes.items())]


def cmd_claims(args):
    claims = load_claims(args.dir)
    topic = load_topic(args.slug)
    mine = by_date([i for i, c in claims.items() if c["topic"] == args.slug], claims)
    ptr = [i for i, c in claims.items() if args.slug in c["also"]]
    print(f"# {topic['name']} ({args.slug}): {len(mine)} claims from {len(episode_ids(mine, claims))} episodes, "
          f"{len(ptr)} pointers rendered by the script")
    if args.pointers:
        print("# id | date | home topic | claim")
        for i in by_date(ptr, claims):
            print(f"{i} | {claims[i]['date']} | {claims[i]['topic']} | {claims[i]['claim']}")
        return
    print("# id | date | marker | level | suggested section | claim")
    for i in mine:
        c = claims[i]
        print(f"{i} | {c['date']} | {c['marker'] or '-'} | {c['level']} | {c['section']} | {c['claim']}")


def cmd_render(args):
    claims = load_claims(args.dir)
    topic = load_topic(args.slug)
    layout = note_path(topic).with_suffix(".layout")
    in_short, items, misplaced, errors = parse_layout(layout)
    unknown = [i for it in items if it[0] == "line" for i in it[3] if i not in claims] + [i for i in misplaced if i not in claims]
    if errors or unknown:
        sys.exit("\n".join(errors + [f"unknown id {i}" for i in unknown]))
    used = [i for it in items if it[0] == "line" for i in it[3]]
    eps = episode_ids(used, claims)
    level = max((LEVELS.index(claims[i]["level"]) for i in used), default=0)
    out = ["---", f"topic: {topic['slug']}", f'title: "{topic["name"]}"', f"area: {topic['area']}",
           f"claims: {len(used)}", f"episodes: {len(eps)}", f"explicitness: {LEVELS[level]}",
           "instructions: v2-draft", "section: topic", "---", "",
           f"> **In short** — {in_short}", "", ITALIC]
    for it in items:
        if it[0] == "section":
            out += ["", f"## {it[1]}", ""]
        else:
            out.append(render_line(it[1], it[2], it[3], claims))
    ptr = pointer_lines(args.slug, claims)
    if ptr:
        out += ["", f"## {OTHER}", ""] + ptr
    note_path(topic).write_text("\n".join(out) + "\n", encoding="utf-8")
    print(f"{note_path(topic).relative_to(ROOT)}: {len(used)} claims, {len(eps)} episodes")


def cmd_verify(args):
    claims = load_claims(args.dir)
    topic = load_topic(args.slug)
    path = note_path(topic)
    _, _, misplaced, errors = parse_layout(path.with_suffix(".layout"))
    lines = path.read_text(encoding="utf-8").splitlines()
    end = lines.index("---", 1) if lines and lines[0] == "---" else -1
    section, seen, slugs = "", Counter(), topic_slugs()
    n_lines = merged = nested = later = 0
    for n, raw in enumerate(lines[end + 1:], end + 2):
        if raw.startswith("## "):
            section = raw[3:]
            continue
        m = re.match(r"^( *)- (.*) \(([^()]*)\) <!-- (.+) -->$", raw)
        if not raw.strip() or raw.startswith(">") or raw == ITALIC:
            continue
        if not m:
            errors.append(f"line {n}: not a note line: {raw[:70]}")
            continue
        depth, text, shown, ids = len(m.group(1)) // 2, m.group(2), m.group(3).split(", "), m.group(4).split()
        bad = [i for i in ids if i not in claims]
        if bad:
            errors.append(f"line {n}: unknown ids {bad}")
            continue
        if section == OTHER:
            home = claims[ids[0]]["topic"]
            if text != pointer_text(home, slugs) or any(claims[i]["topic"] != home for i in ids):
                errors.append(f"line {n}: a pointer has only the link to the home topic of its claims")
            if any(args.slug not in claims[i]["also"] for i in ids):
                errors.append(f"line {n}: pointer to a claim that does not name {args.slug} in also")
            if shown != episode_ids(ids, claims):
                errors.append(f"line {n}: episodes shown {shown}, claims say {episode_ids(ids, claims)}")
            continue
        is_later = False
        lm = re.match(r"^\*\*Later view \((\d{4})\):\*\* (.*)$", text)
        if lm:
            is_later, text = True, lm.group(2)
            if lm.group(1) != claims[ids[0]]["date"][:4]:
                errors.append(f"line {n}: Later view year is not the year of {ids[0]}")
        markers = {claims[i]["marker"] for i in ids}
        if len(markers) > 1:
            errors.append(f"line {n}: claims with different markers on one line: {sorted(markers)}")
        mk = claims[ids[0]]["marker"]
        if mk:
            if not text.startswith(f"**{mk}:** "):
                errors.append(f"line {n}: marker {mk!r} missing")
            text = text[len(f"**{mk}:** "):]
        for i in ids:
            if claims[i]["topic"] != args.slug:
                errors.append(f"line {n}: {i} belongs to {claims[i]['topic']}, not {args.slug}")
            seen[i] += 1
        n_lines += 1
        merged += len({claims[i]["ep"] for i in ids}) > 1
        nested += depth > 0
        later += is_later
        if not any(text == claims[i]["claim"] for i in ids):
            errors.append(f"line {n}: text is not word for word one of its claims: {text[:70]}")
        if shown != episode_ids(ids, claims):
            errors.append(f"line {n}: episodes shown {shown}, claims say {episode_ids(ids, claims)}")
    for i in misplaced:
        seen[i] += 1
    mine = {i for i, c in claims.items() if c["topic"] == args.slug}
    for i in sorted(mine - set(seen)):
        errors.append(f"claim {i} is on no line: {claims[i]['claim'][:70]}")
    for i, k in sorted(seen.items()):
        if k > 1:
            errors.append(f"claim {i} appears {k} times")
    print(f"{args.slug}: {'ERROR' if errors else 'OK'}. {len(mine)} claims, {n_lines} lines, {merged} merged, "
          f"{nested} nested, {later} later views, {len(misplaced)} misplaced")
    for e in errors:
        print(f"  ERROR {e}")
    for i in misplaced:
        print(f"  misplaced {i}: {claims[i]['claim'][:70]}")
    sys.exit(1 if errors else 0)


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    for name in ("claims", "render", "verify"):
        p = sub.add_parser(name)
        p.add_argument("slug")
        p.add_argument("--dir", default=str(REGISTRY))
        if name == "claims":
            p.add_argument("--pointers", action="store_true")
    args = ap.parse_args()
    {"claims": cmd_claims, "render": cmd_render, "verify": cmd_verify}[args.cmd](args)


if __name__ == "__main__":
    main()
