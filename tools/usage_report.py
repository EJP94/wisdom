#!/usr/bin/env python3
"""usage_report.py - measure what a /recaps run cost, from Claude Code's own session logs.

Python 3 standard library only. Run it isolated:

    python3 -I tools/usage_report.py <session.jsonl or folder> [...] [--since 2026-10-28T12:00] [--until ...]

Claude Code keeps one JSONL log per session in ~/.claude/projects/<repo>/, and one per subagent in
<session id>/subagents/. Pass files or folders. It prints one row per log, then the total.

The unit is the cost unit (cu): API list-price weights, so Opus and Sonnet add up on one scale.
1 cu = 200,000 fresh Opus input tokens. Weights per million tokens:

    model    input  cache write (1 h)  cache read  output
    opus       5          10              0.5        25
    sonnet     3           6              0.3        15
    haiku      1           2              0.1         5

The plan's 5-hour limit is not published in tokens. On 2026-10-28 one window held 46 cu without
hitting the limit, and another hit it at 57 cu. plan_blocks.py uses 50 cu per window.
Exit code: 0, or 1 when no usage was found.
"""
import argparse
import json
import os
import sys

WEIGHTS = {"opus": (5, 10, 0.5, 25), "sonnet": (3, 6, 0.3, 15), "haiku": (1, 2, 0.1, 5)}


def family(model):
    for k in WEIGHTS:
        if k in (model or ""):
            return k
    return None


def read_log(path, since, until):
    seen, row = set(), {"calls": 0, "in": 0, "cw": 0, "cr": 0, "out": 0, "cu": 0.0, "models": set(),
                        "first": "", "last": "", "task": ""}
    with open(path, encoding="utf-8", errors="replace") as fh:
        for line in fh:
            try:
                d = json.loads(line)
            except ValueError:
                continue
            m = d.get("message") or {}
            if not row["task"] and d.get("type") == "user" and isinstance(m.get("content"), str):
                row["task"] = " ".join(m["content"].split())[:60]
            ts = d.get("timestamp", "")
            fam = family(m.get("model"))
            if d.get("type") != "assistant" or not fam or m.get("id") in seen or not (since <= ts < until):
                continue
            seen.add(m.get("id"))
            u = m.get("usage") or {}
            got = [u.get("input_tokens", 0), u.get("cache_creation_input_tokens", 0),
                   u.get("cache_read_input_tokens", 0), u.get("output_tokens", 0)]
            for k, v in zip(("in", "cw", "cr", "out"), got):
                row[k] += v
            row["cu"] += sum(v * w for v, w in zip(got, WEIGHTS[fam])) / 1e6
            row["calls"] += 1
            row["models"].add(fam)
            row["first"] = row["first"] or ts
            row["last"] = ts
    return row


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("paths", nargs="+")
    ap.add_argument("--since", default="", help="ISO time, UTC, e.g. 2026-10-28T12:00")
    ap.add_argument("--until", default="9")
    a = ap.parse_args(argv)

    files = []
    for p in a.paths:
        if os.path.isdir(p):
            files += [os.path.join(p, f) for f in os.listdir(p) if f.endswith(".jsonl")]
        else:
            files.append(p)
    rows = [(f, read_log(f, a.since, a.until)) for f in files]
    rows = sorted((r for r in rows if r[1]["calls"]), key=lambda r: r[1]["first"])
    if not rows:
        print("usage_report: no usage found", file=sys.stderr)
        return 1

    print("start (UTC)\tend\tmodel\tcalls\tinput\tcache write\tcache read\toutput\tcu\ttask")
    for f, r in rows:
        print(f"{r['first'][5:16]}\t{r['last'][11:16]}\t{'+'.join(sorted(r['models']))}\t{r['calls']}\t"
              f"{r['in']:,}\t{r['cw']:,}\t{r['cr']:,}\t{r['out']:,}\t{r['cu']:.2f}\t{r['task'] or os.path.basename(f)}")
    total = sum(r["cu"] for _, r in rows)
    print(f"total: {total:.2f} cu in {len(rows)} logs (~{total / 50:.2f} five-hour windows at 50 cu)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
