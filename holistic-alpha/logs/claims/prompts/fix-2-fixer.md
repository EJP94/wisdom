You work in the repo /home/user/wisdom, the Holistic Alpha knowledge vault. This is step A of the topic notes pilot (topic instructions v2 draft, 2026-10-30): each Recap is split into claims, saved in a registry. Run Python as `python3 -I`. Don't read the transcripts, other Recaps, topic notes or other branches. Don't commit or push.

Registry folder: `holistic-alpha/claims`. Recaps: the files of `holistic-alpha/recaps/` whose names start with 001 to 008, 537, 549, 556, 565, 663 and 675.

**Your job: fix the claims from a second round of findings.**

Read first: `holistic-alpha/topic-instructions.md` sections 3 and 9.1, and section 15 of `holistic-alpha/recap-instructions.md` (how to judge a finding). Findings: `holistic-alpha/logs/claims/review/fix-2.json`. Each finding has a `block` and a `reviewer`.
- Block 001-008: a blind full review. Some findings may already be fixed in the registry (003-19, 007-10) or were rejected before (006-09: "In this view" is the Recap's own hedge for the host's view). Check the current file before acting
- Block 537-675: a focused check for hedges, numbers and sources lost in a split. Some are judgment calls: a hedge or source that covers only one sentence of a bullet stays with that sentence

For each finding: check it against the Recap (`cat -n "<file>"`) and the claims file. If it is right, fix `holistic-alpha/claims/<id>.jsonl` (verdict `fixed`). If it is wrong, leave the file (verdict `rejected`) and say why in one line.
- Keep the `id` of every existing row. A new row goes in its place, without `id`, and `fill` gives it one. Delete a row only when the Recap doesn't hold it
- A label bullet (section 3.1) keeps one claim with its own words and topic `none`
- After editing a file, run `python3 -I tools/claims.py fill <id>`

Append every finding, one JSON object per line, to the log of its block, `holistic-alpha/logs/claims/findings/001-008.jsonl` or `holistic-alpha/logs/claims/findings/537-675.jsonl`. Never overwrite them:
{"date": "2026-10-30", "instructions": "v2-draft", "block": "001-008", "reviewer": "sonnet blind", "id": "001", "severity": "S3", "kind": "format", "line": 23, "claim": "001-14", "verdict": "fixed", "note": "<what changed, or why rejected>"}

Then run `python3 -I tools/claims.py check 001 002 003 004 005 006 007 008 537 549 556 565 663 675` and fix every ERROR, and `python3 -I tools/claims.py proposed`.

End with: fixed and rejected counts per block and severity, at most 6 lines.
