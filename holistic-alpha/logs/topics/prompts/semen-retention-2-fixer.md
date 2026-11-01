You work in the repo /home/user/wisdom, the Holistic Alpha knowledge vault. This is the second test of step B of the topic notes pilot (topic instructions v2 draft): a topic's claims become a note. Run Python as `python3 -I`. Don't read the transcripts, the Recaps, other topic notes or other branches. Don't read any other `semen-retention` layout or note, here or in `holistic-alpha/logs/`. Don't commit or push.

Topic: `semen-retention`, area `sex-energy`.

**Your job: fix the layout from the reviewer's findings.**

Read first: `holistic-alpha/topic-instructions.md` sections 4 and 9.2, and section 15 of `holistic-alpha/recap-instructions.md` (how to judge a finding). Findings: `holistic-alpha/logs/topics/review/semen-retention-2-x.json`. Claims: `python3 -I tools/topic_note.py claims semen-retention` (and `--pointers` for the pointer claims).

For each finding, check it against the claims and the layout `holistic-alpha/topics/sex-energy/semen-retention.layout`. If it is right, edit the layout (verdict `fixed`). If it is wrong, leave it (verdict `rejected`) and say why in one line. A `misplaced` or `pointer` finding that is right is fixed in the registry, not by you: verdict `registry`, and touch no claims file.

Then run `python3 -I tools/topic_note.py render semen-retention` and `python3 -I tools/topic_note.py verify semen-retention`, and fix the layout until `verify` prints OK.

Log every finding, one JSON object per line, in `holistic-alpha/logs/topics/findings/semen-retention-2.jsonl`:
{"date": "2026-11-01", "instructions": "v2-draft", "topic": "semen-retention", "reviewer": "sonnet", "severity": "S2", "kind": "merge widened", "ids": ["006-12", "675-08"], "verdict": "fixed", "note": "<what changed, or why rejected>"}

Touch nothing outside `holistic-alpha/topics/sex-energy/` and that findings file.

End with: the `verify` output line, and fixed, rejected and registry counts per severity, at most 5 lines.
