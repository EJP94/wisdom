You work in the repo /home/user/wisdom, the Holistic Alpha knowledge vault (topic instructions v2). Run Python as `python3 -I`. Don't read the transcripts, other Recaps, other branches or the logs of earlier runs. Don't commit or push.

**Your job: move the orgasm claims of 002, 006, 027 and 029 to the topic `orgasm`, as Esteban decided on 2026-11-02, then keep the semen-retention note valid.**

On 2026-11-01 the same move was done for 034 and 275. Orgasm without ejaculation is its own topic: slug `orgasm`, area sex-energy, in `holistic-alpha/topics.csv`. Its claims carry `also: semen-retention`.

Read first: `holistic-alpha/topic-instructions.md` sections 3, 4.2 and 9.1, and `holistic-alpha/topics.csv`.

1. For each of 002, 006, 027 and 029: find the Recap in `holistic-alpha/recaps/` (its file name starts with the id), read it with `cat -n`, and read `holistic-alpha/claims/<id>.jsonl`
2. A claim mainly about orgasm without ejaculation (separating orgasm from ejaculation, multiple or non-ejaculatory orgasms, how to have one, what it feels like) gets topic `orgasm`, and `semen-retention` in `also` (keep its other `also` entries, never `orgasm` in its own `also`). Look at every claim with topic `semen-retention`, and at claims of other topics too
3. A claim mainly about retention itself stays where it is, with `orgasm` added to `also` if it touches orgasm. When in doubt whether a claim is mainly about orgasm or about retention, leave its topic and add `orgasm` to `also`
4. Change only `topic` and `also`. Never a claim's text, id, line, marker, section or level. After editing each file, run `python3 -I tools/claims.py fill <id> --dir holistic-alpha/claims`. Then `python3 -I tools/claims.py check 002 006 027 029 --dir holistic-alpha/claims` with 0 ERROR, and `python3 -I tools/claims.py proposed --dir holistic-alpha/claims`
5. Log every changed row, one JSON object per line, appended to `holistic-alpha/logs/claims/findings/registry-2026-11-02.jsonl`:
{"date": "2026-11-02", "instructions": "v2", "change": "orgasm", "claim": "002-12", "from": "semen-retention", "to": "orgasm", "also": ["semen-retention"], "note": "<one line, why>"}
A row that only gains `orgasm` in `also` logs `"from"` and `"to"` as the same topic
6. **The semen-retention note.** Claims that left `semen-retention` are no longer on its lines: they become pointers, which the script writes. Edit `holistic-alpha/topics/sex-energy/semen-retention.layout` (section 4.2): remove each id that left. When a removed id led a line, the next id on that line leads it. When a line loses all its ids, its nested lines take its place, one level up, and a `later` among them stays under the line it changes. Keep the In short true to the claims that remain. Then run `python3 -I tools/topic_note.py render semen-retention` and `python3 -I tools/topic_note.py verify semen-retention`, and fix the layout until the only ERRORs left are the five claims that were already on no line before you started: 014-21 and 019-13 to 019-16, filed in stage 2. Leave those five off: step B places them later. Touch no other layout

Touch nothing outside `holistic-alpha/claims/`, that layout and its note, and the log file.

End with a short report, at most 8 lines: claims moved per episode, claims that only gained `orgasm` in `also`, the final `verify` line, and any claim you were unsure about.
