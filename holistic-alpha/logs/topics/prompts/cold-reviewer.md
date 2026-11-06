You work in the repo /home/user/wisdom, the Holistic Alpha knowledge vault. This is step B of the topic notes (topic instructions v2, adopted 2026-11-02), for the first production topic: a topic's claims become a note. Run Python as `python3 -I`. Don't read the transcripts, the Recaps, other topic notes or other branches. Don't commit or push.

Topic: `cold`, "Cold exposure", area `mind`. Every episode the keywords find for it has a Recap and claims, so this note is complete. The layout is `holistic-alpha/topics/mind/cold.layout`, the note `holistic-alpha/topics/mind/cold.md`.

**Your job: review the note. Don't edit any file except your findings file.**

Read first, in full: `holistic-alpha/topic-instructions.md` sections 4, 7 and 9.2. Then:
- The claims: `python3 -I tools/topic_note.py claims cold`
- The pointers, claims of other topics that name this one in `also`: `python3 -I tools/topic_note.py claims cold --pointers`
- The layout and the rendered note. Each line of the note ends with its claim ids in a comment
- `python3 -I tools/topic_note.py verify cold` checks text, coverage and markers, and counts groups. Don't report what it checks

Check, line by line:
1. **False merges**: ids on one line that don't make the same claim with the same strength and scope. Compare every merged id's text with the line's first claim: a hedge ("seems", "probably", "for him"), a number, a condition or a scope ("in winter", "for beginners") that differs is a false merge
2. **Missed merges and missed groups**: claims on separate lines, from different episodes, that make the same claim. Same strength and scope: a missed merge. Another strength or scope, not nested under one line: a missed group
3. **Later view**: a claim of the host that would change what someone does or believes, if they read only the older claim, is nested under the older line with `later`, newer after older, and the older line is kept. One Later view per group, under its top line. A hedge that leaves the advice as it was is not a Later view. A guest who disagrees is nested with his marker, not a Later view
4. **Nesting and sections**: a nested line is the same claim with another strength or scope, or a detail of its parent. A listener's or guest's question is a top-level line with the host's answers nested under it. Sections group lines by question
5. **In short**: never stronger or wider than the claims
6. **Misplaced and pointers**: a claim in `misplaced` that is about this topic, or one on a line that is not. A pointer whose claim is mainly about cold exposure (its home topic is wrong in the registry)

Report only real defects, with the severity and `kind` of section 9.2. A missed group is kind `merge missed`, S3. Don't report style.

Write your findings with the Write tool to `holistic-alpha/logs/topics/review/cold.json`, as JSON:
{"topic": "cold", "merged_lines_checked": <n>, "groups_checked": <n>, "findings": [{"severity": "S2", "kind": "merge widened", "ids": ["004-12", "090-08"], "found": "<what is wrong, quoting the claims>", "fix": "<the change to the layout>"}]}

End with one line only: the count of findings per severity.
