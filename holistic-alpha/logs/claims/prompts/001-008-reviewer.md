You work in the repo /home/user/wisdom, the Holistic Alpha knowledge vault. This is step A of the topic notes pilot (topic instructions v2 draft, 2026-10-30): each Recap is split into claims, saved in a registry. Run Python as `python3 -I`. Don't read the transcripts, other Recaps, topic notes or other branches. Don't commit or push.

Block 001-008. Registry folder for this run: `holistic-alpha/claims`. Recaps:
- 001: `holistic-alpha/recaps/001 - The War Against Resistance.md`
- 002: `holistic-alpha/recaps/002 - Keys to Solid Hormones - How to 80-20 Your Testosterone.md`
- 003: `holistic-alpha/recaps/003 - Every. Single. Day....Becomes Who You ARE.md`
- 004: `holistic-alpha/recaps/004 - Willpower - Kick Resistance in the Nuts with Cold Showers.md`
- 005: `holistic-alpha/recaps/005 - Build Strength Quickly with Total Daily Volume.md`
- 006: `holistic-alpha/recaps/006 - Harnessing & Building Your Sex Energy.md`
- 007: `holistic-alpha/recaps/007 - Push vs. Pull... The Importance of Balance in our Lives AND Our Body.md`
- 008: `holistic-alpha/recaps/008 - Intermittent Fasting — How the Eating Window Can Fuel Your Life.md`

**Your job: review the claims of each Recap. Don't edit any file except your findings file.**

Read first, in full: `holistic-alpha/topic-instructions.md` sections 3 and 9.1, and `holistic-alpha/topics.csv`.

For each Recap: read it with `cat -n "<file>"` and read `holistic-alpha/claims/<id>.jsonl`. Go bullet line by bullet line (each row's `line` is the Recap line number) and check:
1. Recall: every statement of the bullet is in some claim. A dropped statement, number or example is S1 idea lost
2. Fidelity: the Recap's words, hedges, numbers, sources and quotes. Not stronger or wider. The right marker (speaker)
3. Each claim reads alone, out of its bullet: no "this", "it" or "that" pointing outside it, its subject named. Step B copies claims word for word and adds nothing
4. One statement per row, except whole stories, quotes and questions
5. Topic (the subject it is mainly about), `also`, `level`, proposals that duplicate a topic of topics.csv or another proposal

Report only real defects, with the severity and `kind` of section 9.1. A claim that keeps the Recap's words and reads alone is fine: don't report style.

Write your findings with the Write tool to `holistic-alpha/logs/claims/review/001-008.json`, as JSON:
{"episodes": [{"id": "001", "ok": false, "findings": [{"severity": "S2", "kind": "hedge lost", "line": 23, "claim": "001-07", "recap": "<the Recap's words>", "found": "<the claim's words>", "fix": "<the fixed claim, or what to do>"}]}]}
List every Recap of the block, with `"ok": true` and `"findings": []` when it is clean.

End with the count of findings per severity, at most 5 lines.
