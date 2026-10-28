#!/usr/bin/env python3
"""plan_blocks.py - plan the next /recaps run: which episodes, in which blocks and chains.

Python 3 standard library only. Run it isolated, from the repo root:

    python3 -I tools/plan_blocks.py --episodes holistic-alpha/episodes.csv --recaps holistic-alpha/recaps/
        [--ids 801-813 537 404b1 especial-2024-12-25 | --all] [--mode write|review|audit] [--overwrite]
        [--order newest|oldest] [--chains 1] [--budget 1100000] [--max-block 8] [--max-words 30000]
        [--alone-over 12000] [--qa-every 25] [--tokens-per-word 20] [--block-tokens 60000]
        [--out-dir test-folder] [--out plan.json]

It reads episodes.csv and writes (or prints) the JSON args of the recap-writeups workflow:
repo, date, python, mode, overwrite, outDir, header, chains (each chain a list of blocks), qa, estimate.

- write mode skips episodes without a transcript, and episodes that already have a Recap
  unless --overwrite. review and audit modes take only episodes that already have a Recap.
- A block holds up to --max-block episodes and --max-words transcript words. An episode longer
  than --alone-over words gets a block of its own.
- Each block names its spot-check episodes: every interview and group. Otherwise the longest
  episode, except in every third block, where a fixed hash picks another one, so shorter
  episodes get checked too.
- --budget stops adding blocks once the estimate would pass it. One 5-hour window of the Pro
  plan was about 1.2M tokens in the One Piece runs.
- The estimate per block is --block-tokens + words x --tokens-per-word, plus a spot-check of
  25,000 + 2 x words per spot episode, plus 5% for escalations. review mode counts 60% of the
  block cost (no writer) and audit mode 30% (reviewer only, no spot-check). These defaults come
  from the One Piece runs. Replace them with the calibration run's numbers.
- qa lists the Recaps Esteban reads by hand: one in --qa-every, plus the first of each
  non-solo type in the run.
Exit code: 0, or 1 when nothing is left to plan.
"""
import argparse
import csv
import datetime
import io
import json
import os
import re
import sys
import zlib

VERSION = "0.1 (2026-10-28)"
PRO_WINDOW = 1_200_000
RISKY = ("interview", "group")
MODE_SHARE = {"write": 1.0, "review": 0.6, "audit": 0.3}


def parse_ids(tokens):
    """'801-813', '537', '404b1', 'especial-2024-12-25' (comma or space separated)."""
    exact, ranges = set(), []
    for t in tokens:
        for part in t.split(","):
            part = part.strip()
            if not part:
                continue
            m = re.fullmatch(r"(\d+)-(\d+)", part)
            if m:
                a, b = int(m.group(1)), int(m.group(2))
                ranges.append((min(a, b), max(a, b)))
            elif part.isdigit():
                ranges.append((int(part), int(part)))
            else:
                exact.add(part)
    return exact, ranges


def wanted(row, exact, ranges):
    if row["id"] in exact:
        return True
    ep = (row.get("episode") or "").strip()
    return ep.isdigit() and any(a <= int(ep) <= b for a, b in ranges)


def words(row):
    try:
        return int(row.get("words") or 0)
    except ValueError:
        return 0


def csv_line(fields, values):
    buf = io.StringIO()
    csv.writer(buf, lineterminator="").writerow([values.get(f, "") for f in fields])
    return buf.getvalue()


def spot_ids(block, index):
    risky = [r["id"] for r in block if r.get("type") in RISKY]
    if risky:
        return risky
    longest = max(block, key=words)
    others = [r for r in block if r is not longest]
    if index % 3 == 2 and others:
        key = ",".join(r["id"] for r in block).encode("utf-8")
        return [others[zlib.crc32(key) % len(others)]["id"]]
    return [longest["id"]]


def block_estimate(block, spot, a):
    w = sum(words(r) for r in block)
    base = (a.block_tokens + w * a.tokens_per_word) * MODE_SHARE[a.mode]
    spot_cost = 0 if a.mode == "audit" else sum(25_000 + 2 * words(r) for r in block if r["id"] in spot)
    return int((base + spot_cost) * 1.05)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--episodes", required=True)
    ap.add_argument("--recaps", required=True, help="folder that holds the Recaps (to skip or pick existing ones)")
    ap.add_argument("--ids", nargs="*", default=[])
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--mode", choices=("write", "review", "audit"), default="write")
    ap.add_argument("--overwrite", action="store_true")
    ap.add_argument("--order", choices=("newest", "oldest"), default="newest")
    ap.add_argument("--chains", type=int, default=1)
    ap.add_argument("--budget", type=int, default=0, help="token budget for this run, 0 = no limit")
    ap.add_argument("--max-block", type=int, default=8)
    ap.add_argument("--max-words", type=int, default=30_000)
    ap.add_argument("--alone-over", type=int, default=12_000)
    ap.add_argument("--qa-every", type=int, default=25)
    ap.add_argument("--tokens-per-word", type=float, default=20)
    ap.add_argument("--block-tokens", type=int, default=60_000)
    ap.add_argument("--repo", help="absolute path of the repo (default: the folder above episodes.csv's folder)")
    ap.add_argument("--out-dir", help="test folder for the Recaps, relative to the repo (default: production)")
    ap.add_argument("--out")
    a = ap.parse_args(argv)
    if not (a.all or a.ids):
        ap.error("give --ids or --all")

    with open(a.episodes, encoding="utf-8", newline="") as fh:
        reader = csv.DictReader(fh)
        fields = reader.fieldnames
        rows = list(reader)

    exact, ranges = parse_ids(a.ids)
    have = set(os.listdir(a.recaps)) if os.path.isdir(a.recaps) else set()
    todo, skipped = [], {"no transcript": 0, "has a Recap": 0, "no Recap to review": 0}
    for r in rows:
        if not (a.all or wanted(r, exact, ranges)):
            continue
        if r.get("status") != "available":
            skipped["no transcript"] += 1
        elif a.mode == "write" and r.get("recap") in have and not a.overwrite:
            skipped["has a Recap"] += 1
        elif a.mode != "write" and r.get("recap") not in have:
            skipped["no Recap to review"] += 1
        else:
            todo.append(r)
    found = {r["id"] for r in rows}
    unknown = sorted(exact - found)

    todo.sort(key=lambda r: (r.get("date") or "", r["id"]), reverse=(a.order == "newest"))

    blocks, cur, cur_w = [], [], 0
    for r in todo:
        w = words(r)
        if w > a.alone_over:
            blocks.append([r])
            continue
        if cur and (len(cur) >= a.max_block or cur_w + w > a.max_words):
            blocks.append(cur)
            cur, cur_w = [], 0
        cur.append(r)
        cur_w += w
    if cur:
        blocks.append(cur)

    planned, total = [], 0
    for i, b in enumerate(blocks):
        spot = spot_ids(b, i)
        est = block_estimate(b, spot, a)
        if a.budget and planned and total + est > a.budget:
            break
        total += est
        ids = [r["id"] for r in b]
        planned.append({
            "label": ids[0] if len(ids) == 1 else f"{ids[0]}-{ids[-1]}",
            "ids": ids,
            "spot": spot,
            "types": sorted({r.get("type", "") for r in b}),
            "words": sum(words(r) for r in b),
            "estimate": est,
            "rows": [csv_line(fields, r) for r in b],
        })

    chains = [[] for _ in range(max(1, a.chains))]
    load = [0] * len(chains)
    for blk in planned:
        k = load.index(min(load))
        chains[k].append(blk)
        load[k] += blk["words"]
    chains = [c for c in chains if c]

    in_run = [r for blk in planned for r in todo if r["id"] in blk["ids"]]
    qa, seen_types = [], set()
    for n, r in enumerate(in_run):
        t = r.get("type", "solo")
        if (t != "solo" and t not in seen_types) or (a.qa_every and n % a.qa_every == a.qa_every // 2):
            qa.append(r["id"])
        seen_types.add(t)
    if in_run and not qa:
        qa.append(in_run[len(in_run) // 2]["id"])

    repo = a.repo or os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(a.episodes)), os.pardir))
    plan = {
        "planner": f"plan_blocks.py {VERSION}",
        "date": datetime.date.today().isoformat(),
        "repo": repo.replace("\\", "/"),
        "python": "py -3" if os.name == "nt" else "python3",
        "mode": a.mode,
        "overwrite": bool(a.overwrite),
        "outDir": a.out_dir or None,
        "header": ",".join(fields),
        "chains": chains,
        "qa": qa,
        "estimate": {
            "episodes": len(in_run),
            "blocks": len(planned),
            "words": sum(blk["words"] for blk in planned),
            "spot_episodes": sum(len(blk["spot"]) for blk in planned),
            "tokens": total,
            "pro_windows": round(total / PRO_WINDOW, 1),
            "left_for_later": len(todo) - len(in_run),
        },
    }
    text = json.dumps(plan, indent=1, ensure_ascii=False) + "\n"
    if a.out:
        with open(a.out, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(text)
    else:
        sys.stdout.write(text)

    e = plan["estimate"]
    print(f"plan_blocks: {e['episodes']} episodes in {e['blocks']} blocks and {len(chains)} chain(s), "
          f"{e['words']:,} words, about {e['tokens'] / 1e6:.1f}M tokens (~{e['pro_windows']} Pro windows). "
          f"Left for later: {e['left_for_later']}. Skipped: "
          + ", ".join(f"{k} {v}" for k, v in skipped.items() if v)
          + (f". Unknown ids: {' '.join(unknown)}" if unknown else ""),
          file=sys.stderr)
    return 0 if planned else 1


if __name__ == "__main__":
    sys.exit(main())
