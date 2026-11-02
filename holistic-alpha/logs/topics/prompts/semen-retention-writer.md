You work in the repo /home/user/wisdom, the Holistic Alpha knowledge vault. This is a test of step B of the topic notes pilot (topic instructions v2 draft): a topic's claims become a note. Run Python as `python3 -I`. Don't read the transcripts, the Recaps, other topic notes or other branches. Don't commit or push.

Topic: `semen-retention`, area `sex-energy`. 72 claims from 6 episodes (002, 006, 537, 549, 565, 675).

**Your job: write the layout of the note.**

Read first, in full: `STATUS.md`, `holistic-alpha/logs/runs/2026-10-30-pilot-stages-0-1.md`, then `holistic-alpha/topic-instructions.md` sections 2, 4, 7, 8 and 9.2.

1. Run `python3 -I tools/topic_note.py claims semen-retention`. It is your only input
2. Write `holistic-alpha/topics/sex-energy/semen-retention.layout` (section 4.2)
3. Run `python3 -I tools/topic_note.py render semen-retention`, then `python3 -I tools/topic_note.py verify semen-retention`. Fix the layout until `verify` prints OK

What matters most:
- Merge across episodes whenever two claims make the same claim, with the same strength and scope (4.3). This test exists to see whether step B merges: v1 merged nothing. Never merge to reach a number
- A claim of the same subject with another strength or scope, or a detail, goes on a nested line
- A story never merges. Guest, listener and host claims never share a line
- A change of view: nested under the older line, with `later` (4.4). Never drop the older line
- The In short keeps the claims' hedges. It is never stronger than they are
- Every claim exactly once, on a line or in `misplaced`
- Touch nothing outside `holistic-alpha/topics/sex-energy/`

End with a short report, at most 12 lines: the `verify` output line; merges you made and any you held back, and why; later views; misplaced claims; any rule you found unclear or hard to apply.
