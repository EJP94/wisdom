#!/usr/bin/env python3
"""topic_episodes.py - find each topic's episodes by keyword, and how many are already applied.

Python 3 standard library only. Run it isolated, from the repo root:

    python3 -I tools/topic_episodes.py --topics holistic-alpha/topics.csv
        --transcripts holistic-alpha/transcripts/ --episodes holistic-alpha/episodes.csv
        --recaps holistic-alpha/recaps/ [--applied holistic-alpha/topics/applied.csv]
        [--logs holistic-alpha/logs/topics/] [--only kegels cold]
        [--out holistic-alpha/topic-episodes.csv] [--report report.md] [--stamp holistic-alpha/topics/]

It reads the closed list of topics (topics.csv: slug, area, name, status, explicitness,
min_hits, keywords) and counts each topic's keywords in every transcript. An episode belongs to
a topic when its transcript has at least min_hits matches, or when a run log placed one of its
Recap bullets in that topic. Keywords are one regular expression, case-insensitive, matched on
the transcript text without its [mm:ss] stamps.

- --logs is the folder of run logs (<run>.jsonl, one line per Recap bullet). A line whose path is
  merged, detail, new, born or reapplied adds its episode to its topic. So the lists get exact
  as episodes are applied, and keywords only guess the episodes not applied yet.
- --out writes one row per topic and episode: slug, id, hits, found_by (keywords, log or both),
  date, recap (yes/no), applied (yes/no).
- --report writes (or prints) one line per topic: matched episodes, how many have a Recap,
  how many are applied to the topic notes, and the coverage "applied/matched".
- --applied is the ledger of Recaps already applied to the topic notes (column id). Missing file =
  nothing applied yet.
- --stamp writes coverage and status (partial or complete) into the frontmatter of each topic note
  that exists at <dir>/<area>/<slug>.md. Nothing else in the note changes.

Keyword matching is a cheap first pass: it misses episodes that talk about a topic in other
words, and catches some that only mention it. The topic instructions say how to treat that.
Exit code: 0, or 1 when topics.csv has an error.
"""
import argparse
import csv
import json
import os
import re
import sys

VERSION = "0.2 (2026-10-30)"
HOME_PATHS = ("merged", "detail", "new", "born", "reapplied")
AREAS = ("mind", "sex-energy", "hormones", "training", "fuel", "relationships")
STATUSES = ("topic", "parked")
EXPLICITNESS = ("general", "sexual-health", "explicit")
STAMP = re.compile(r"^\[\d+:\d{2}(?::\d{2})?\]\s*", re.M)


def load_topics(path, only):
    rows, errors, seen = [], [], set()
    with open(path, encoding="utf-8", newline="") as f:
        for n, r in enumerate(csv.DictReader(f), start=2):
            slug = (r.get("slug") or "").strip()
            where = f"{path}:{n} ({slug or 'no slug'})"
            if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", slug):
                errors.append(f"{where}: slug must be lowercase words joined by '-'")
            if slug in seen:
                errors.append(f"{where}: slug repeated")
            seen.add(slug)
            if r.get("area") not in AREAS:
                errors.append(f"{where}: area must be one of {', '.join(AREAS)}")
            if r.get("status") not in STATUSES:
                errors.append(f"{where}: status must be topic or parked")
            if r.get("explicitness") not in EXPLICITNESS:
                errors.append(f"{where}: explicitness must be one of {', '.join(EXPLICITNESS)}")
            try:
                r["min_hits"] = int(r.get("min_hits") or "")
            except ValueError:
                errors.append(f"{where}: min_hits must be a whole number")
            try:
                r["regex"] = re.compile(r.get("keywords") or "", re.I)
            except re.error as e:
                errors.append(f"{where}: keywords is not a valid regular expression ({e})")
            if not (r.get("keywords") or "").strip():
                errors.append(f"{where}: keywords is empty")
            if not only or slug in only:
                rows.append(r)
    return rows, errors


def load_episodes(path):
    with open(path, encoding="utf-8", newline="") as f:
        return [r for r in csv.DictReader(f) if r.get("stem")]


def load_applied(path):
    if not path or not os.path.exists(path):
        return set()
    with open(path, encoding="utf-8", newline="") as f:
        return {r["id"].strip() for r in csv.DictReader(f) if r.get("id")}


def load_log_homes(folder):
    """{slug: {id, ...}} from the run logs: where each applied Recap bullet found its home."""
    homes = {}
    if not folder or not os.path.isdir(folder):
        return homes
    for name in sorted(os.listdir(folder)):
        if not name.endswith(".jsonl"):
            continue
        with open(os.path.join(folder, name), encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    e = json.loads(line)
                except ValueError:
                    continue
                if e.get("path") in HOME_PATHS and e.get("topic") and e.get("id"):
                    homes.setdefault(e["topic"], set()).add(str(e["id"]))
    return homes


def stamp_note(path, coverage, status):
    with open(path, encoding="utf-8") as f:
        text = f.read()
    m = re.match(r"---\n(.*?)\n---\n", text, re.S)
    if not m:
        return f"{path}: no frontmatter, not stamped"
    head = m.group(1)
    for key, value in (("coverage", f'"{coverage}"'), ("status", status)):
        line = f"{key}: {value}"
        if re.search(rf"^{key}:.*$", head, re.M):
            head = re.sub(rf"^{key}:.*$", line, head, count=1, flags=re.M)
        else:
            head += "\n" + line
    new = f"---\n{head}\n---\n" + text[m.end():]
    if new != text:
        with open(path, "w", encoding="utf-8", newline="\n") as f:
            f.write(new)
    return None


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--topics", required=True)
    ap.add_argument("--transcripts", required=True)
    ap.add_argument("--episodes", required=True)
    ap.add_argument("--recaps", required=True)
    ap.add_argument("--applied")
    ap.add_argument("--logs")
    ap.add_argument("--only", nargs="*", default=[])
    ap.add_argument("--out")
    ap.add_argument("--report")
    ap.add_argument("--stamp")
    a = ap.parse_args()

    topics, errors = load_topics(a.topics, set(a.only))
    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1
    applied = load_applied(a.applied)
    homes = load_log_homes(a.logs)
    episodes = load_episodes(a.episodes)

    matches = {t["slug"]: [] for t in topics}
    for ep in episodes:
        path = os.path.join(a.transcripts, ep["stem"] + ".txt")
        if not os.path.exists(path):
            continue
        with open(path, encoding="utf-8") as f:
            text = STAMP.sub("", f.read())
        has_recap = os.path.exists(os.path.join(a.recaps, ep["stem"] + ".md"))
        for t in topics:
            hits = len(t["regex"].findall(text))
            by_keywords = hits >= t["min_hits"]
            by_log = ep["id"] in homes.get(t["slug"], ())
            if by_keywords or by_log:
                matches[t["slug"]].append({
                    "slug": t["slug"], "id": ep["id"], "hits": hits,
                    "found_by": "both" if by_keywords and by_log else "keywords" if by_keywords else "log",
                    "date": ep.get("date", ""), "recap": "yes" if has_recap else "no",
                    "applied": "yes" if ep["id"] in applied else "no"})

    if a.out:
        with open(a.out, "w", encoding="utf-8", newline="") as f:
            w = csv.DictWriter(f, fieldnames=["slug", "id", "hits", "found_by", "date", "recap", "applied"],
                               lineterminator="\n")
            w.writeheader()
            for t in topics:
                w.writerows(matches[t["slug"]])

    lines = [f"# Topic episodes ({VERSION})", "",
             "| area | topic | status | matched | with Recap | applied | coverage |",
             "| --- | --- | --- | --- | --- | --- | --- |"]
    problems = []
    for t in sorted(topics, key=lambda t: (AREAS.index(t["area"]), t["status"], t["slug"])):
        m = matches[t["slug"]]
        recaps = sum(r["recap"] == "yes" for r in m)
        done = sum(r["applied"] == "yes" for r in m)
        coverage = f"{done}/{len(m)}"
        lines.append(f"| {t['area']} | {t['name']} | {t['status']} | {len(m)} | {recaps} | {done} | {coverage} |")
        if a.stamp and t["status"] == "topic":
            note = os.path.join(a.stamp, t["area"], t["slug"] + ".md")
            if os.path.exists(note):
                status = "complete" if m and done == len(m) else "partial"
                p = stamp_note(note, coverage, status)
                if p:
                    problems.append(p)
    report = "\n".join(lines + [""] + problems) + "\n"
    if a.report:
        with open(a.report, "w", encoding="utf-8", newline="\n") as f:
            f.write(report)
    else:
        sys.stdout.write(report)
    return 0


if __name__ == "__main__":
    sys.exit(main())
