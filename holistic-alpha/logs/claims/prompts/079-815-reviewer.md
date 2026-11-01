You work in the repo /home/user/wisdom, the Holistic Alpha knowledge vault. This is step A of the topic notes pilot (topic instructions v2 draft, 2026-10-30): each Recap is split into claims, saved in a registry. Run Python as `python3 -I`. Don't read the transcripts, other Recaps, topic notes or other branches. Don't commit or push.

Block 079-815. Registry folder for this run: `holistic-alpha/claims`. Recaps:
- 079: `holistic-alpha/recaps/079 - The Spirit of All Men.md`
- 252: `holistic-alpha/recaps/252 - The Power of Deep Relaxation, Part 2 - A Guided Exercise.md`
- 289: `holistic-alpha/recaps/289 - Starting Conversations, Cold Exposure, and Releasing Emotional Triggers.md`
- 303: `holistic-alpha/recaps/303 - Glycine, and Constructive Conflict in Relationships.md`
- 350: `holistic-alpha/recaps/350 - Cold Power and Recognizing Wins.md`
- 404b1: `holistic-alpha/recaps/404b1 - Building Better Stamina - Part 3 - The Warm Draw.md`
- 720: `holistic-alpha/recaps/720 - Ending the Night; Taking Advantage of a Small Lever That Opens a Big Door.md`
- 721: `holistic-alpha/recaps/721 - Are Kegels Critical or Counterproductive.md`
- 812: `holistic-alpha/recaps/812 - Earning Your Erections.md`
- 815: `holistic-alpha/recaps/815 - I Built You Something - 3 Free Courses, Live Now.md`

**Your job: review the claims of each Recap. Don't edit any file except your findings file.**

Read first, in full: `holistic-alpha/topic-instructions.md` sections 3 and 9.1, and `holistic-alpha/topics.csv`.

For each Recap: read it with `cat -n "<file>"` and read `holistic-alpha/claims/<id>.jsonl`. Go bullet line by bullet line (each row's `line` is the Recap line number) and check:
1. Recall: every statement of the bullet is in some claim. A dropped statement, number or example is S1 idea lost
2. Fidelity: the Recap's words, hedges, numbers, sources and quotes. Not stronger or wider. The right marker (speaker)
3. Each claim reads alone, out of its bullet: no "this", "it" or "that" pointing outside it, its subject named. Step B copies claims word for word and adds nothing
4. One statement per row, except whole stories, quotes and questions
5. Lost in split: a hedge ("probably", "seems", "a strong belief", "personally"), a number or a source that opens a bullet, or its parent bullet, can cover several statements. Every claim split from them must carry it. Check each bullet with more than one claim, and each parent bullet with nested bullets
6. Topic (the subject it is mainly about), `also`, `level`, proposals that duplicate a topic of topics.csv or another proposal

Report only real defects, with the severity and `kind` of section 9.1. A claim that keeps the Recap's words and reads alone is fine: don't report style.

Write your findings with the Write tool to `holistic-alpha/logs/claims/review/079-815.json`, as JSON:
{"episodes": [{"id": "001", "ok": false, "findings": [{"severity": "S2", "kind": "hedge lost", "line": 23, "claim": "001-07", "recap": "<the Recap's words>", "found": "<the claim's words>", "fix": "<the fixed claim, or what to do>"}]}]}
List every Recap of the block, with `"ok": true` and `"findings": []` when it is clean.

End with the count of findings per severity, at most 5 lines.
