You work in the repo /home/user/wisdom, the Holistic Alpha knowledge vault. This is step A of the topic notes pilot (topic instructions v2 draft, 2026-10-30): each Recap is split into claims, saved in a registry. Run Python as `python3 -I`. Don't read the transcripts, other Recaps, topic notes or other branches. Don't commit or push.

Block 537-675. Registry folder for this run: `holistic-alpha/claims`. Recaps:
- 537: `holistic-alpha/recaps/537 - Community Convos #4 - Dustin Desheles.md`
- 549: `holistic-alpha/recaps/549 - Reigniting Momentum from Within the Funk, a Community Convo with Charles.md`
- 556: `holistic-alpha/recaps/556 - 21D Habit Challenge - Day 5.md`
- 565: `holistic-alpha/recaps/565 - A Group Discussion on Mindful Edging.md`
- 663: `holistic-alpha/recaps/663 - The Pause-Intention Bridge - Quitting Porn + Building Discipline & More.md`
- 675: `holistic-alpha/recaps/675 - Listener Question - The Semen Retention Emotional Wall.md`

**Your job: one focused check of the claims of each Recap. Don't edit any file except your findings file.**

Read first: `holistic-alpha/topic-instructions.md` sections 3.2 and 9.1.

The claims were already reviewed for everything else. Check only this: **lost in split.** A hedge ("probably", "seems", "a strong belief", "personally"), a number or a source that opens a bullet, or its parent bullet, can cover several statements. Every claim split from them must carry it. Example, 014: "a strong belief" covers everything said about the prostate, so each of its three claims carries it.

For each Recap: read it with `cat -n "<file>"` and read `holistic-alpha/claims/<id>.jsonl`. For each bullet with more than one claim, and each parent bullet with nested bullets, check that every claim carries the hedges, numbers and sources that cover it.

Write your findings with the Write tool to `holistic-alpha/logs/claims/review/537-675-recheck.json`, as JSON:
{"episodes": [{"id": "537", "ok": false, "findings": [{"severity": "S2", "kind": "lost in split", "line": 23, "claim": "537-07", "recap": "<the Recap's words>", "found": "<the claim's words>", "fix": "<the fixed claim>"}]}]}
List every Recap of the block, with `"ok": true` and `"findings": []` when it is clean.

End with the count of findings, at most 3 lines.
