You work in the repo /home/user/wisdom, the Holistic Alpha knowledge vault. This is the second test of step B of the topic notes pilot (topic instructions v2 draft): a topic's claims become a note. Run Python as `python3 -I`. Don't read the transcripts, the Recaps, other topic notes or other branches. Don't read any other `semen-retention` layout or note: not in `holistic-alpha/topics/`, not in another folder of `holistic-alpha/logs/topics/`. Don't commit or push.

Topic: `semen-retention`, area `sex-energy`. 218 claims from 13 episodes (002, 006, 011, 027, 029, 034, 088, 127, 537, 549, 565, 675, 731), plus 70 pointer claims from other topics.

Your folder, NOTES, and your letter, X, are named in the message that sent you here. The note to review is `NOTES/sex-energy/semen-retention.md`, its layout `NOTES/sex-energy/semen-retention.layout`.

**Your job: review the note. Don't edit any file except your findings file.**

Read first, in full: `holistic-alpha/topic-instructions.md` sections 4, 7 and 9.2. Then:
- The claims: `python3 -I tools/topic_note.py claims semen-retention`
- The pointers, claims of other topics that name this one in `also`: `python3 -I tools/topic_note.py claims semen-retention --pointers`
- The layout and the rendered note. Each line of the note ends with its claim ids in a comment
- `python3 -I tools/topic_note.py verify semen-retention --notes NOTES` checks text, coverage and markers, and counts groups. Don't report what it checks

Check, line by line:
1. **False merges**: ids on one line that don't make the same claim with the same strength and scope. Compare every merged id's text with the line's first claim: a hedge ("seems", "probably", "for him"), a number, a condition or a scope ("with a partner", "for beginners") that differs is a false merge
2. **Missed merges and missed groups**: claims on separate lines, from different episodes, that make the same claim. Same strength and scope: a missed merge. Another strength or scope, not nested under one line: a missed group
3. **Later view**: a claim of the host that changes or contradicts an older one is nested under it with `later`, newer after older, and the older line is kept. One Later view for each older line that changes. A guest who disagrees is nested with his marker, not a Later view
4. **Nesting and sections**: a nested line is the same claim with another strength or scope, or a detail of its parent. Sections group lines by question
5. **In short**: never stronger or wider than the claims
6. **Misplaced and pointers**: a claim in `misplaced` that is about this topic, or one on a line that is not. A pointer whose claim is mainly about semen retention (its home topic is wrong in the registry)

Report only real defects, with the severity and `kind` of section 9.2. A missed group is kind `merge missed`, S3. Don't report style.

Write your findings with the Write tool to `holistic-alpha/logs/topics/review/semen-retention-2-X.json` (X in lower case), as JSON:
{"topic": "semen-retention", "folder": "NOTES", "merged_lines_checked": <n>, "groups_checked": <n>, "findings": [{"severity": "S2", "kind": "merge widened", "ids": ["006-12", "675-08"], "found": "<what is wrong, quoting the claims>", "fix": "<the change to the layout>"}]}

End with the count of findings per severity and kind, at most 5 lines.
