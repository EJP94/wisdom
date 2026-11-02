You work in the repo /home/user/wisdom, the Holistic Alpha knowledge vault. This is step A of the topic notes pilot (topic instructions v2 draft, 2026-10-30): each Recap is split into claims, saved in a registry. Run Python as `python3 -I`. Don't read the transcripts, other Recaps, topic notes or other branches. Don't commit or push.

Block 537-675. Registry folder for this run: `holistic-alpha/claims`. Recaps:
- 537: `holistic-alpha/recaps/537 - Community Convos #4 - Dustin Desheles.md`
- 549: `holistic-alpha/recaps/549 - Reigniting Momentum from Within the Funk, a Community Convo with Charles.md`
- 556: `holistic-alpha/recaps/556 - 21D Habit Challenge - Day 5.md`
- 565: `holistic-alpha/recaps/565 - A Group Discussion on Mindful Edging.md`
- 663: `holistic-alpha/recaps/663 - The Pause-Intention Bridge - Quitting Porn + Building Discipline & More.md`
- 675: `holistic-alpha/recaps/675 - Listener Question - The Semen Retention Emotional Wall.md`

**Your job: review the claims of each Recap. Don't edit any file except your findings file.**

Read first, in full: `holistic-alpha/topic-instructions.md` sections 3 and 9.1, and `holistic-alpha/topics.csv`.

For each Recap: read it with `cat -n "<file>"` and read `holistic-alpha/claims/<id>.jsonl`. Go bullet line by bullet line (each row's `line` is the Recap line number) and check:
1. Recall: every statement of the bullet is in some claim. A dropped statement, number or example is S1 idea lost
2. Fidelity: the Recap's words, hedges, numbers, sources and quotes. Not stronger or wider. The right marker (speaker)
3. Each claim reads alone, out of its bullet: no "this", "it" or "that" pointing outside it, its subject named. Step B copies claims word for word and adds nothing
4. One statement per row, except whole stories, quotes and questions
5. Topic (the subject it is mainly about), `also`, `level`, proposals that duplicate a topic of topics.csv or another proposal

Report only real defects, with the severity and `kind` of section 9.1. A claim that keeps the Recap's words and reads alone is fine: don't report style.

Write your findings with the Write tool to `holistic-alpha/logs/claims/review/537-675.json`, as JSON:
{"episodes": [{"id": "001", "ok": false, "findings": [{"severity": "S2", "kind": "hedge lost", "line": 23, "claim": "001-07", "recap": "<the Recap's words>", "found": "<the claim's words>", "fix": "<the fixed claim, or what to do>"}]}]}
List every Recap of the block, with `"ok": true` and `"findings": []` when it is clean.

End with the count of findings per severity, at most 5 lines.
