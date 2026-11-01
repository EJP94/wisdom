You work in the repo /home/user/wisdom, the Holistic Alpha knowledge vault. This is the second test of step B of the topic notes pilot (topic instructions v2 draft): a topic's claims become a note. Run Python as `python3 -I`. Don't read the transcripts, the Recaps, other topic notes or other branches. Don't read any other `semen-retention` layout or note, here or in `holistic-alpha/logs/`. Don't commit or push.

Topic: `semen-retention`, area `sex-energy`. 218 claims from 13 episodes (002, 006, 011, 027, 029, 034, 088, 127, 537, 549, 565, 675, 731), plus 70 pointer claims from other topics.

Your notes folder, NOTES, is named in the message that sent you here. Your layout is `NOTES/sex-energy/semen-retention.layout`.

**Your job: write the layout of the note.**

Read first, in full: `STATUS.md`, `holistic-alpha/logs/runs/2026-10-30-pilot-stages-0-1.md`, then `holistic-alpha/topic-instructions.md` sections 2, 4, 7, 8 and 9.2.

1. Run `python3 -I tools/topic_note.py claims semen-retention`. It is your only input
2. Write `NOTES/sex-energy/semen-retention.layout` (section 4.2)
3. Run `python3 -I tools/topic_note.py render semen-retention --notes NOTES`, then `python3 -I tools/topic_note.py verify semen-retention --notes NOTES`. Fix the layout until `verify` prints OK

What matters most:
- Group across episodes. When claims from different episodes make the same claim, put them in one group: on one line when strength and scope are the same (4.3), nested under one line when the strength or scope differs. Never group to reach a number
- A detail of a line goes on a nested line under it
- A story never merges. Guest, listener and host claims never share a line. A guest who disagrees is nested with his marker, never a Later view
- A change of view: nested under the older line, with `later` (4.4). One Later view for each older line that changes. Never drop the older line
- The In short keeps the claims' hedges. It is never stronger than they are
- Every claim exactly once, on a line or in `misplaced`
- Touch nothing outside `NOTES/sex-energy/`

End with a short report, at most 12 lines: the `verify` output line; the groups across episodes, and any you held back and why; later views; misplaced claims; any rule you found unclear or hard to apply.
