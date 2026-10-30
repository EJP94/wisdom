#!/usr/bin/env python3
"""claims.py - step A of the topic notes: the claims registry (topic instructions v2 draft).

Python 3 standard library only. Run it isolated, from the repo root:

    python3 -I tools/claims.py fill <id> [<id> ...] [--dir DIR]
    python3 -I tools/claims.py check <id> [<id> ...] [--dir DIR]
    python3 -I tools/claims.py proposed [--dir DIR]
    python3 -I tools/claims.py stats [--dir DIR] [--out FILE]
    python3 -I tools/claims.py compare DIR_A DIR_B <id> [<id> ...] [--out FILE]

The registry is holistic-alpha/claims/<id>.jsonl, one row per claim, in Recap order. <id> is the
episode id of episodes.csv. --dir points at another folder with the same layout (the pilot keeps a
second writer's claims under logs/ to compare).

- fill: adds id (<episode>-<n>), ep and date to rows that lack them. Never changes an id it gave
- check: validates rows against topics.csv, episodes.csv and the Recap. Every bullet line of the
  Recap must have a claim. Exit code 1 on any ERROR
- proposed: writes _proposed.csv in the folder: subjects proposed with a +slug topic, their episodes
- stats: claims per Recap and per topic, births, explicitness to raise. Markdown
- compare: two writers' claims of the same Recaps, bullet by bullet. Markdown
"""

import argparse
import csv
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

VERSION = "0.2 (2026-10-30)"
ROOT = Path(__file__).resolve().parent.parent
HA = ROOT / "holistic-alpha"
REGISTRY = HA / "claims"
AREAS = {"mind", "sex-energy", "hormones", "training", "fuel", "relationships"}
LEVELS = ["general", "sexual-health", "explicit"]
MARKER = re.compile(r"^(?:Story|Host story|Guest(?: story| advice| question)?(?: \([^)]+\))?"
                    r"|Listener question|Listener story|Quote|Guided practice)?$")
FIELDS = ["id", "ep", "date", "line", "topic", "also", "section", "marker", "level", "claim", "name", "area"]
WRITER_FIELDS = {"line", "topic", "also", "section", "marker", "level", "claim"}
POINTING = re.compile(r"^(?:This|It|That|These|Those|They|He|She)\b")


def load_episodes():
    with open(HA / "episodes.csv", newline="", encoding="utf-8") as f:
        return {r["id"]: r for r in csv.DictReader(f)}


def load_topics():
    with open(HA / "topics.csv", newline="", encoding="utf-8") as f:
        return {r["slug"]: r for r in csv.DictReader(f)}


def read_rows(path):
    rows = []
    with open(path, encoding="utf-8") as f:
        for n, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            try:
                rows.append(json.loads(line))
            except json.JSONDecodeError as e:
                sys.exit(f"{path}:{n}: not JSON ({e})")
    return rows


def write_rows(path, rows):
    with open(path, "w", encoding="utf-8") as f:
        for r in rows:
            ordered = {k: r[k] for k in FIELDS if k in r}
            ordered.update({k: v for k, v in r.items() if k not in ordered})
            f.write(json.dumps(ordered, ensure_ascii=False) + "\n")


def bullet_lines(recap_path):
    """Line numbers (from 1, frontmatter included) of every bullet line, nested ones included."""
    lines = recap_path.read_text(encoding="utf-8").splitlines()
    start = 0
    if lines and lines[0].strip() == "---":
        for i in range(1, len(lines)):
            if lines[i].strip() == "---":
                start = i + 1
                break
    return {i + 1: lines[i] for i in range(start, len(lines)) if re.match(r"^\s*- ", lines[i])}


def rel(path):
    p = Path(path).resolve()
    return p.relative_to(ROOT) if p.is_relative_to(ROOT) else p


def registry_files(folder):
    return sorted(p for p in Path(folder).glob("*.jsonl"))


def all_rows(folder):
    out = []
    for p in registry_files(folder):
        out.extend(read_rows(p))
    return out


def cmd_fill(args, episodes):
    for ep in args.ids:
        if ep not in episodes:
            sys.exit(f"{ep}: not an id of episodes.csv")
        path = Path(args.dir) / f"{ep}.jsonl"
        rows = read_rows(path)
        used = [int(r["id"].rsplit("-", 1)[1]) for r in rows if r.get("id")]
        nxt = max(used, default=0) + 1
        for r in rows:
            if not r.get("id"):
                r["id"] = f"{ep}-{nxt:02d}"
                nxt += 1
            r["ep"] = ep
            r["date"] = episodes[ep]["date"]
        write_rows(path, rows)
        print(f"{ep}: {len(rows)} claims")


def check_file(ep, folder, episodes, topics, proposals):
    errors, warns = [], []
    path = Path(folder) / f"{ep}.jsonl"
    if ep not in episodes:
        return [f"not an id of episodes.csv"], warns, 0
    if not path.exists():
        return [f"no file {path}"], warns, 0
    rows = read_rows(path)
    recap = HA / "recaps" / episodes[ep]["recap"]
    bullets = bullet_lines(recap)
    seen_ids, covered = set(), set()
    for k, r in enumerate(rows, 1):
        where = f"row {k}" + (f" ({r['id']})" if r.get("id") else "")
        missing = WRITER_FIELDS - r.keys()
        if missing:
            errors.append(f"{where}: missing {', '.join(sorted(missing))}")
            continue
        if not r.get("id"):
            errors.append(f"{where}: no id, run fill")
        elif r["id"] in seen_ids:
            errors.append(f"{where}: id used twice")
        elif not r["id"].startswith(ep + "-"):
            errors.append(f"{where}: id does not start with {ep}-")
        seen_ids.add(r.get("id"))
        if r.get("ep") != ep or r.get("date") != episodes[ep]["date"]:
            errors.append(f"{where}: ep or date wrong, run fill")
        if r["line"] not in bullets:
            errors.append(f"{where}: line {r['line']} is not a bullet line of the Recap")
        covered.add(r["line"])
        t = r["topic"]
        if t.startswith("+"):
            slug = t[1:]
            if not r.get("name") or r.get("area") not in AREAS | {"?"}:
                errors.append(f"{where}: {t} needs a name and an area")
            else:
                proposals[slug].append((ep, r["name"], r["area"]))
        elif t != "none" and t not in topics:
            errors.append(f"{where}: unknown topic {t}")
        if not isinstance(r["also"], list):
            errors.append(f"{where}: also must be a list")
        else:
            for a in r["also"]:
                if a == t:
                    errors.append(f"{where}: also repeats the topic {a}")
                elif not (a in topics or a.startswith("+")):
                    errors.append(f"{where}: unknown topic {a} in also")
        if not MARKER.match(r["marker"]):
            errors.append(f"{where}: unknown marker {r['marker']!r}")
        if r["level"] not in LEVELS:
            errors.append(f"{where}: level must be one of {', '.join(LEVELS)}")
        if not r["claim"].strip():
            errors.append(f"{where}: empty claim")
        elif POINTING.match(r["claim"]):
            warns.append(f"{where}: starts with a pointing word, may not read alone: {r['claim'][:60]}")
        if not r["section"].strip() and t != "none":
            warns.append(f"{where}: no section")
    for n in sorted(set(bullets) - covered):
        errors.append(f"line {n} has no claim: {bullets[n].strip()[:70]}")
    return errors, warns, len(rows)


def cmd_check(args, episodes, topics):
    proposals = defaultdict(list)
    bad = 0
    for ep in args.ids:
        errors, warns, n = check_file(ep, args.dir, episodes, topics, proposals)
        status = "ERROR" if errors else ("WARN" if warns else "OK")
        print(f"{ep}: {status}, {n} claims")
        for e in errors:
            print(f"  ERROR {e}")
        for w in warns:
            print(f"  WARN {w}")
        bad += bool(errors)
    for slug, uses in sorted(proposals.items()):
        names = {(n, a) for _, n, a in uses}
        if len(names) > 1:
            print(f"ERROR +{slug} has different names or areas: {sorted(names)}")
            bad += 1
    sys.exit(1 if bad else 0)


def proposal_table(rows, topics):
    by = defaultdict(lambda: {"eps": set(), "claims": 0, "name": "", "area": "", "example": ""})
    for r in rows:
        if r["topic"].startswith("+"):
            p = by[r["topic"][1:]]
            p["eps"].add(r["ep"])
            p["claims"] += 1
            p["name"] = p["name"] or r.get("name", "")
            p["area"] = p["area"] or r.get("area", "")
            p["example"] = p["example"] or r["claim"]
    return {s: p for s, p in by.items() if s not in topics}


def cmd_proposed(args, topics):
    table = proposal_table(all_rows(args.dir), topics)
    out = Path(args.dir) / "_proposed.csv"
    with open(out, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["slug", "name", "area", "episodes", "claims", "ids", "example"])
        for slug, p in sorted(table.items()):
            w.writerow([slug, p["name"], p["area"], len(p["eps"]), p["claims"], " ".join(sorted(p["eps"])), p["example"]])
    print(f"{out}: {len(table)} proposed subjects")


def cmd_stats(args, episodes, topics):
    files = registry_files(args.dir)
    rows = all_rows(args.dir)
    out = [f"# Claims registry - claims.py {VERSION}", "", f"Folder: `{rel(args.dir)}`", ""]
    out += ["## Per Recap", "", "| episode | bullets | claims | per bullet | none | proposed |", "|---|---|---|---|---|---|"]
    tot_b = tot_c = 0
    for p in files:
        ep = p.stem
        rs = read_rows(p)
        nb = len(bullet_lines(HA / "recaps" / episodes[ep]["recap"]))
        tot_b += nb
        tot_c += len(rs)
        out.append(f"| {ep} | {nb} | {len(rs)} | {len(rs) / nb:.1f} | {sum(r['topic'] == 'none' for r in rs)} "
                   f"| {sum(r['topic'].startswith('+') for r in rs)} |")
    if tot_b:
        out.append(f"| **total** | {tot_b} | {tot_c} | {tot_c / tot_b:.1f} | | |")
    eps_by, claims_by, level_by, ptr_by = defaultdict(set), defaultdict(int), defaultdict(int), defaultdict(int)
    for r in rows:
        if r["topic"].lstrip("+") in topics:
            r["topic"] = r["topic"].lstrip("+")
        eps_by[r["topic"]].add(r["ep"])
        claims_by[r["topic"]] += 1
        level_by[r["topic"]] = max(level_by[r["topic"]], LEVELS.index(r["level"]))
        for a in r["also"]:
            ptr_by[a] += 1
    out += ["", "## Per topic", "", "| topic | status | claims | episodes | pointers in | level | topics.csv |", "|---|---|---|---|---|---|---|"]
    for t in sorted(claims_by, key=lambda t: (-claims_by[t], t)):
        row = topics.get(t.lstrip("+"), {})
        status = row.get("status", "proposed" if t.startswith("+") else "-")
        lvl = LEVELS[level_by[t]]
        csv_lvl = row.get("explicitness", "")
        flag = " **raise**" if csv_lvl and LEVELS.index(lvl) > LEVELS.index(csv_lvl) else ""
        out.append(f"| {t} | {status} | {claims_by[t]} | {len(eps_by[t])} | {ptr_by.get(t.lstrip('+'), 0)} | {lvl}{flag} | {csv_lvl} |")
    born = [t for t in claims_by if len(eps_by[t]) >= 3 and (t.startswith("+") or topics.get(t, {}).get("status") == "parked")]
    out += ["", "## Births", ""]
    out += [f"- {t}: {len(eps_by[t])} episodes" for t in sorted(born)] or ["None"]
    text = "\n".join(out) + "\n"
    if args.out:
        Path(args.out).write_text(text, encoding="utf-8")
    print(text)


def cmd_compare(args, episodes):
    out = [f"# Two writers, same Recaps - claims.py {VERSION}", "",
           f"A: `{args.dir_a}`  ", f"B: `{args.dir_b}`", "",
           "| episode | bullets | claims A | claims B | bullets where counts differ | bullets where topics differ |",
           "|---|---|---|---|---|---|"]
    detail = []
    for ep in args.ids:
        a = read_rows(Path(args.dir_a) / f"{ep}.jsonl")
        b = read_rows(Path(args.dir_b) / f"{ep}.jsonl")
        bullets = bullet_lines(HA / "recaps" / episodes[ep]["recap"])
        ca, cb = defaultdict(list), defaultdict(list)
        for r in a:
            ca[r["line"]].append(r)
        for r in b:
            cb[r["line"]].append(r)
        dc = [n for n in bullets if len(ca[n]) != len(cb[n])]
        dt = [n for n in bullets if {r["topic"] for r in ca[n]} != {r["topic"] for r in cb[n]}]
        out.append(f"| {ep} | {len(bullets)} | {len(a)} | {len(b)} | {len(dc)} | {len(dt)} |")
        for n in sorted(set(dc) | set(dt)):
            detail.append(f"- {ep} line {n}: A {len(ca[n])} {sorted({r['topic'] for r in ca[n]})}, "
                          f"B {len(cb[n])} {sorted({r['topic'] for r in cb[n]})}")
    text = "\n".join(out + ["", "## Bullets that differ", ""] + (detail or ["None"])) + "\n"
    if args.out:
        Path(args.out).write_text(text, encoding="utf-8")
    print(text)


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    for name in ("fill", "check"):
        p = sub.add_parser(name)
        p.add_argument("ids", nargs="+")
        p.add_argument("--dir", default=str(REGISTRY))
    p = sub.add_parser("proposed")
    p.add_argument("--dir", default=str(REGISTRY))
    p = sub.add_parser("stats")
    p.add_argument("--dir", default=str(REGISTRY))
    p.add_argument("--out")
    p = sub.add_parser("compare")
    p.add_argument("dir_a")
    p.add_argument("dir_b")
    p.add_argument("ids", nargs="+")
    p.add_argument("--out")
    args = ap.parse_args()
    episodes, topics = load_episodes(), load_topics()
    if args.cmd == "fill":
        cmd_fill(args, episodes)
    elif args.cmd == "check":
        cmd_check(args, episodes, topics)
    elif args.cmd == "proposed":
        cmd_proposed(args, topics)
    elif args.cmd == "stats":
        cmd_stats(args, episodes, topics)
    else:
        cmd_compare(args, episodes)


if __name__ == "__main__":
    main()
