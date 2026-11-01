You work in the repo /home/user/wisdom, the Holistic Alpha knowledge vault. This is a test of step B of the topic notes pilot (topic instructions v2 draft): a topic's claims become a note. Run Python as `python3 -I`. Don't read the transcripts, the Recaps, other topic notes or other branches. Don't commit or push.

Topic: `semen-retention`, area `sex-energy`. 72 claims from 6 episodes (002, 006, 537, 549, 565, 675).

**Your job: review the note. Don't edit any file except your findings file.**

Read first, in full: `holistic-alpha/topic-instructions.md` sections 4, 7 and 9.2. Then:
- The claims: `python3 -I tools/topic_note.py claims semen-retention`
- The pointers, claims of other topics that name this one in `also`: `python3 -I tools/topic_note.py claims semen-retention --pointers`
- The layout: `holistic-alpha/topics/sex-energy/semen-retention.layout`
- The rendered note: `holistic-alpha/topics/sex-energy/semen-retention.md`. Each line ends with its claim ids in a comment
- `python3 -I tools/topic_note.py verify semen-retention` checks text, coverage and markers. Don't report what it checks

Check, line by line:
1. **False merges**: ids on one line that don't make the same claim with the same strength and scope. Compare every merged id's text with the line's first claim: a hedge ("seems", "probably", "for him"), a number, a condition or a scope ("with a partner", "for beginners") that differs is a false merge
2. **Missed merges**: claims on separate lines, from different episodes, that make the same claim with the same strength and scope
3. **Later view**: a claim that changes or contradicts an older one is nested under it with `later`, newer after older, and the older line is kept
4. **Nesting and sections**: a nested line is the same claim with another strength or scope, or a detail of its parent. Sections group lines by question
5. **In short**: never stronger or wider than the claims
6. **Misplaced and pointers**: a claim in `misplaced` that is about this topic, or one on a line that is not. A pointer whose claim is mainly about semen retention (its home topic is wrong in the registry)

Report only real defects, with the severity and `kind` of section 9.2. Don't report style.

Write your findings with the Write tool to `holistic-alpha/logs/topics/review/semen-retention.json`, as JSON:
{"topic": "semen-retention", "merged_lines_checked": <n>, "findings": [{"severity": "S2", "kind": "merge widened", "ids": ["006-12", "675-08"], "found": "<what is wrong, quoting the claims>", "fix": "<the change to the layout>"}]}

End with the count of findings per severity and kind, at most 5 lines.
