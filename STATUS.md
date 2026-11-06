# Status

Updated 2026-11-06. Read this first. Update it in the commit of any run that changes what is done or what comes next.

## Where we are: Holistic Alpha

- Transcripts: 809 of 809
- Recaps: 82 of 809. Recap instructions v2
  - 001-034, all from 2019
  - 19 episodes from 2019-2026, restored from commit `dd2aaa6`: 079 088 127 150 175 252 275 350 404b1 537 549 556 565 663 675 720 812 813 815. The pilots among them (127 275 537 663 813) had a review against the v2 checklist on 2026-10-30
  - 4 new on 2026-10-30: 289 303 721 731
  - 25 new for cold, 2026-11-02 to 2026-11-06: 080 090 092 105 114 121 140 174 185 191 195 212 240 285 296 355 391 422 458 540 550 569 571 676 711
- Topics: rules v2 (`holistic-alpha/topic-instructions.md`), adopted on 2026-11-02 (PR #10). `holistic-alpha/topics.csv` lists 50 rows, topics and parked ones, `tools/claims.py` and `tools/topic_note.py` run the two steps. All 82 Recaps have claims: 3,958 claims from 1,756 bullets
  - **First complete note: cold** (`holistic-alpha/topics/mind/cold.md`), 252 claims from 27 episodes, 46 groups with 2+ episodes holding 208 claims. Every episode its keywords find has a Recap and claims. Report: `holistic-alpha/logs/runs/2026-11-06-cold.md`
  - The pilot's note, semen-retention, is not complete: most of its episodes have no Recap yet
  - The two-step pilot ran from 2026-10-30 to 2026-11-01. Its reports are `holistic-alpha/logs/runs/2026-10-30-pilot-stages-0-1.md` and the three `2026-11-01-pilot-*.md`. It projected the whole vault at 3,600-4,200 cu with Sonnet writing step B
- Views and pieces: none yet

## Next

The two-step pilot is over and the v2 topic instructions are adopted (PR #10, merged 2026-11-02). Each step runs only when Esteban asks for it, with its cost in front of him first.

1. **Esteban reads the cold note**, and the QA Recaps 240 and 550. If the note groups too little, it is rebuilt with Opus as the writer (about 5 cu)
2. Two registry fixes the cold review found, about 1 cu, for Esteban to decide:
   - The cock looking smaller after cold has two homes: 711-25 in `+body-relationship`, 571-22 and 711-34 in `cold`
   - Winter claims of 140 are split: 140-56, 140-06 and 140-07 in `discomfort`, 140-49 and 140-55 in `cold`
3. **Esteban's proposal of 2026-11-06:** other models write, Claude orchestrates, reviews and fixes. Writers were about 52 of the 100 agent cu of the cold run. First a test: Gemini and DeepSeek write 8 episodes that already have reviewed Recaps, Sonnet reviews blind, and their S1 and S2 are compared with Opus. About 5-8 cu of Claude. The other models run on Esteban's PC
4. Second topic, root muscle and Kegels: keywords match 108 episodes and 13 have a Recap. With the current process, about 430 cu (95 Recaps at 2.3, step A at 1.4 per Recap, step B about 10, orchestration about 20%). It tests changes of view, since 721 asks "Are Kegels Critical or Counterproductive?"
5. Every ~100 new Recaps, propose which topics or proposals overlap and which to merge (Esteban, 2026-11-02). 25 of 100 since then

The cost unit (cu) is defined in `tools/usage_report.py`. One 5-hour window holds about 50 cu. The week of 2026-10-30 to 2026-11-06 ran out after about 300 cu, a rough sum of that week's runs. A Recap cost 2.3 cu in the cold run, review, spot-check and one escalation included.

## Decisions

Made by Esteban between 2026-10-26 and 2026-11-02. Change them only when he asks.

- **Recaps are the source of everything above them.** The vault replaces the transcripts: every idea said in an episode ends up in it
- **Six fixed areas:** mind, sex-energy, hormones, training, fuel, relationships. The first five are Steven's own split in 001, 002 and 029. Relationships was added because partner and family come up often and grow in later years
- **A topic is born at 3 episodes.** An earlier pilot gave 19 "concepts" from 10 episodes, which would be about 1,500 for 809. The 34 Recaps gave 25 topics. The guess for 809 is 60-100
- **One topic at a time.** Before pieces are made on a topic, all its episodes get a Recap. Pieces use only complete notes, so they miss nothing other episodes say
- **Every Recap and every note gets a full review** (2026-11-01). No review by sample. Step A: Opus writes. Step B: Sonnet writes, Opus fixes
- **Topic list (2026-11-02):** when in doubt, two topics. Merging later is a free slug change (`claims.py merge`), splitting costs an agent. `erections` stays apart from `morning-wood`. No big review of the list now: every ~100 new Recaps, a proposal of overlaps
- **No fact-checking in the vault.** Esteban fact-checks each piece himself before he publishes it
- **Credit is settled.** Steven allows reproducing and monetizing his material. Credit to him and to every source goes at the end of each piece. Don't reopen it
- **Views kept for now:** pensum, manual by problem, transformation program, idea graph. Ten others were discussed and left out, such as a glossary, a story bank and an FAQ

## Content plan

- Pieces are in English. YouTube first, then TikTok, Instagram, X and a blog
- Each piece picks its own explicitness: general, sexual-health or explicit. A topic's level in `topics.csv` is only the most its lines reach
- The 34 Recaps lean to the body. Almost half of the 809 titles are about sex, 8 in 10 in 2025-2026. Porn has 32 titles, mostly from 2021, and 310 transcripts name it

## Later

More vaults, one per subject: Kabbalah, mysticism, esotericism, occultism, astrology. None started.

The full proposal behind the topics layer, in Spanish: https://claude.ai/artifact/ANVDiPUACY8yKnKrz7gGqJ
