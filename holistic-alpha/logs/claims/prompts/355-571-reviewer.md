You work in the repo /home/user/wisdom, the Holistic Alpha knowledge vault. This is step A of the topic notes (topic instructions v2, adopted 2026-11-02), in the run for the topic cold: each Recap is split into claims, saved in a registry. Run Python as `python3 -I`. Don't read the transcripts, other Recaps, topic notes or other branches. Don't commit or push.

Block 355-571. Registry folder for this run: `holistic-alpha/claims`. Recaps:
- 355: `holistic-alpha/recaps/355 - What to Do When You're Feeling Unmotivated.md`
- 391: `holistic-alpha/recaps/391 - Awareness and Sexual Empowerment.md`
- 422: `holistic-alpha/recaps/422 - Trickle-Down Habits.md`
- 458: `holistic-alpha/recaps/458 - How Do I Stay On Course.md`
- 540: `holistic-alpha/recaps/540 - NoFap vs. The Holistic Alpha Way + 4 Indispensable Tools to Overcome Porn Addiction.md`
- 550: `holistic-alpha/recaps/550 - 21D Habit Challenge - Day 1 - With Charles.md`
- 569: `holistic-alpha/recaps/569 - Semen Retention - What to Do When This Happens Around 1-2 Weeks.md`
- 571: `holistic-alpha/recaps/571 - Your Relationship With Your Cock.md`

**Your job: review the claims of each Recap. Don't edit any file except your findings file.**

Read first, in full: `holistic-alpha/topic-instructions.md` sections 3 and 9.1, and `holistic-alpha/topics.csv`.

For each Recap: read it with `cat -n "<file>"` and read `holistic-alpha/claims/<id>.jsonl`. Go bullet line by bullet line (each row's `line` is the Recap line number) and check:
1. Recall: every statement of the bullet is in some claim. A dropped statement, number or example is S1 idea lost
2. Fidelity: the Recap's words, hedges, numbers, sources and quotes. Not stronger or wider. The right marker (speaker)
3. Each claim reads alone, out of its bullet: no "this", "it" or "that" pointing outside it, its subject named. Step B copies claims word for word and adds nothing
4. One statement per row, except whole stories, quotes and questions
5. Lost in split: a hedge ("probably", "seems", "a strong belief", "personally"), a number or a source that opens a bullet, or its parent bullet, can cover several statements. Every claim split from them must carry it. Check each bullet with more than one claim, and each parent bullet with nested bullets
6. Topic (the subject it is mainly about), `also`, `level`, proposals that duplicate a topic of topics.csv or another proposal in `holistic-alpha/claims/_proposed.csv`

Report only real defects, with the severity and `kind` of section 9.1. A claim that keeps the Recap's words and reads alone is fine: don't report style.

Write your findings with the Write tool to `holistic-alpha/logs/claims/review/355-571.json`, as JSON:
{"episodes": [{"id": "001", "ok": false, "findings": [{"severity": "S2", "kind": "hedge lost", "line": 23, "claim": "001-07", "recap": "<the Recap's words>", "found": "<the claim's words>", "fix": "<the fixed claim, or what to do>"}]}]}
List every Recap of the block, with `"ok": true` and `"findings": []` when it is clean.

End with one line only: "S1 <n>, S2 <n>, S3 <n>".
