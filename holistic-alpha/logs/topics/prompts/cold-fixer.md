You work in the repo /home/user/wisdom, the Holistic Alpha knowledge vault. This is step B of the topic notes (topic instructions v2, adopted 2026-11-02), for the first production topic: a topic's claims become a note. Run Python as `python3 -I`. Don't read the transcripts, the Recaps, other topic notes or other branches. Don't commit or push.

Topic: `cold`, "Cold exposure", area `mind`. Every episode the keywords find for it has a Recap and claims, so this note is complete. The layout is `holistic-alpha/topics/mind/cold.layout`, the note `holistic-alpha/topics/mind/cold.md`.

**Your job: fix the layout from the reviewer's findings.**

Read first: `holistic-alpha/topic-instructions.md` sections 4 and 9.2, and section 15 of `holistic-alpha/recap-instructions.md` (how to judge a finding). Findings: `holistic-alpha/logs/topics/review/cold.json`. Claims: `python3 -I tools/topic_note.py claims cold` (and `--pointers` for the pointer claims).

For each finding, check it against the claims and the layout `holistic-alpha/topics/mind/cold.layout`. If it is right, edit the layout (verdict `fixed`). If it is wrong, leave it (verdict `rejected`) and say why in one line. A `misplaced` or `pointer` finding that is right is fixed in the registry, not by you: verdict `registry`, and touch no claims file.

Then run `python3 -I tools/topic_note.py render cold` and `python3 -I tools/topic_note.py verify cold`, and fix the layout until `verify` prints OK.

Log every finding, one JSON object per line, in `holistic-alpha/logs/topics/findings/cold.jsonl`:
{"date": "<today, YYYY-MM-DD>", "instructions": "v2", "topic": "cold", "reviewer": "sonnet", "severity": "S2", "kind": "merge widened", "ids": ["004-12", "090-08"], "verdict": "fixed", "note": "<what changed, or why rejected>"}

Touch nothing outside `holistic-alpha/topics/mind/` and that findings file.

End with: the `verify` output line, and fixed, rejected and registry counts per severity, at most 5 lines.
