You work in the repo /home/user/wisdom, the Holistic Alpha knowledge vault (topic notes pilot, topic instructions v2 draft). Run Python as `python3 -I`. Don't read the transcripts, other Recaps, other branches or the logs of earlier runs. Don't commit or push.

**Your job: move claims to new homes in the registry, as Esteban decided on 2026-11-01, then keep the semen-retention note valid.**

Esteban's decisions:
- Orgasm without ejaculation is its own topic: slug `orgasm`, area sex-energy, now in `holistic-alpha/topics.csv`. Its claims carry `also: semen-retention`. Reassign the claims of 034 and 275 that are about it
- Covid is not an area or a topic. It is context: each claim goes to the topic it talks about (section 3.4, rule 7)

Read first: `holistic-alpha/topic-instructions.md` sections 3, 4.2 and 9.1, and `holistic-alpha/topics.csv`.

1. **034** (`holistic-alpha/recaps/034 - Multiple Orgasms Without Ejaculation.md`, claims `holistic-alpha/claims/034.jsonl`). Read the Recap with `cat -n` and the claims. A claim mainly about orgasm without ejaculation (separating orgasm from ejaculation, multiple or non-ejaculatory orgasms, how to have one, what it feels like) gets topic `orgasm`, and `semen-retention` in `also` (keep its other `also` entries, never `orgasm` in its own `also`). A claim mainly about retention itself stays in `semen-retention`, with `orgasm` in `also` if it touches orgasm
2. **275** (`holistic-alpha/recaps/275 - The Male Sex Muscle - Understanding It, Training It, and Using It.md`). Rows with topic `+orgasm` get topic `orgasm`, lose their `name` and `area` fields, and get `semen-retention` in `also`. Any other 275 claim mainly about orgasm without ejaculation: the same. `also` entries `+orgasm` anywhere in 034 or 275 become `orgasm`
3. **150** (`holistic-alpha/recaps/150 - Dealing with Extended Periods Without Sex.md`). Each row with topic `+covid` gets the topic it talks about: a topic of `topics.csv` or a subject already in `holistic-alpha/claims/_proposed.csv`. Propose a new subject only if none fits. Rows that leave a proposal lose their `name` and `area`, and gain them only for another proposal
4. Change only `topic`, `also`, `name` and `area`. Never a claim's text, id, line, marker, section or level. After editing each file, run `python3 -I tools/claims.py fill <id> --dir holistic-alpha/claims`. Then `python3 -I tools/claims.py check 034 150 275 --dir holistic-alpha/claims` with 0 ERROR, and `python3 -I tools/claims.py proposed --dir holistic-alpha/claims`
5. Log every changed row, one JSON object per line, in `holistic-alpha/logs/claims/findings/registry-2026-11-01.jsonl`:
{"date": "2026-11-01", "instructions": "v2-draft", "change": "orgasm", "claim": "034-12", "from": "semen-retention", "to": "orgasm", "also": ["semen-retention"], "note": "<one line, why>"}
6. **The semen-retention note.** Claims that left `semen-retention` are no longer on its lines: they become pointers, which the script writes. Edit `holistic-alpha/topics/sex-energy/semen-retention.layout` (section 4.2): remove each id that left. When a removed id led a line, the next id on that line leads it. When a line loses all its ids, its nested lines take its place, one level up, and a `later` among them stays under the line it changes. Keep the In short true to the claims that remain. Then run `python3 -I tools/topic_note.py render semen-retention` and `python3 -I tools/topic_note.py verify semen-retention`, and fix the layout until `verify` prints OK. Touch no other layout

Touch nothing outside `holistic-alpha/claims/`, that layout and its note, and the log file.

End with a short report, at most 10 lines: claims moved per change and per episode, where the covid claims went, the final `verify` line, and any claim you were unsure about.
