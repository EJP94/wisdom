You work in the repo /home/user/wisdom, the Holistic Alpha knowledge vault. This is step B of the topic notes (topic instructions v2, adopted 2026-11-02), for the first production topic: a topic's claims become a note. Run Python as `python3 -I`. Don't read the transcripts, the Recaps, other topic notes or other branches. Don't commit or push.

Topic: `cold`, "Cold exposure", area `mind`. Every episode the keywords find for it has a Recap and claims, so this note is complete. The layout is `holistic-alpha/topics/mind/cold.layout`, the note `holistic-alpha/topics/mind/cold.md`.

**Your job: write the layout of the note.**

Read first, in full: `holistic-alpha/topic-instructions.md` sections 2, 4, 7, 8 and 9.2.

1. Run `python3 -I tools/topic_note.py claims cold`. It is your only input
2. Write `holistic-alpha/topics/mind/cold.layout` (section 4.2)
3. Run `python3 -I tools/topic_note.py render cold`, then `python3 -I tools/topic_note.py verify cold`. Fix the layout until `verify` prints OK

What matters most:
- Group across episodes. When claims from different episodes make the same claim, put them in one group: on one line when strength and scope are the same (4.3), nested under one line when the strength or scope differs. Never group to reach a number. A group with 2 or more episodes is the measure of this step
- A detail of a line goes on a nested line under it. A nested line can hold nested lines
- A listener's or guest's question is a top-level line, and the host's answers nest under it
- A story never merges. Guest, listener and host claims never share a line. A guest who disagrees is nested with his marker, never a Later view
- A change of view: a later claim that would change what someone does or believes if they read only the older claim. Nest it under the older line with `later`, one Later view per group, under the group's top line (4.4). A hedge or nuance that leaves the advice as it was nests without `later`. Never drop the older line
- The In short keeps the claims' hedges. It is never stronger than they are
- Every claim exactly once, on a line or in `misplaced`
- Touch nothing outside `holistic-alpha/topics/mind/`

End with a short report, at most 12 lines: the `verify` output line; the groups across episodes, and any you held back and why; later views; misplaced claims; any rule you found unclear or hard to apply.
