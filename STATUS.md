# Status

Updated 2026-11-01. Read this first. Update it in the commit of any run that changes what is done or what comes next.

## Where we are: Holistic Alpha

- Transcripts: 809 of 809
- Recaps: 57 of 809. Recap instructions v2
  - 001-034, all from 2019
  - 19 episodes from 2019-2026, restored from commit `dd2aaa6`: 079 088 127 150 175 252 275 350 404b1 537 549 556 565 663 675 720 812 813 815. The pilots among them (127 275 537 663 813) had a review against the v2 checklist on 2026-10-30
  - 4 new on 2026-10-30: 289 303 721 731
- Topics: the rules are written (`holistic-alpha/topic-instructions.md` v1, `holistic-alpha/topics.csv`, `tools/topic_episodes.py`). On main no topic note exists yet. The pilot's first note, semen-retention, is on its branch
  - Keywords tuned on 2026-10-30. `kegels`, now named "Root muscle and Kegels", also finds root muscle, pelvic floor and sex muscle, the words of later years: 64 to 108 episodes. `every-day` lost `today`, which matched almost every intro: 114 to 50 episodes
  - A first test of the notes with v1 on 24 Recaps (001-024) merged nothing: each line copied a whole Recap bullet with several claims, so no two episodes shared a line. It cost 45.8 cu, and the cost per Recap grew with the notes (1.5, 1.9, 2.3 cu). Its notes, logs and costs are on the branch `claude/topic-notes-v1-test`, kept to compare and never merged
- Views and pieces: none yet

## Next

Each step runs only when Esteban asks for it, with its cost in front of him first.

1. Topic notes in two steps, a pilot on the branch `claude/topic-notes-two-steps`, never merged until Esteban approves. Rules: `holistic-alpha/topic-instructions.md` v2 draft there
   - Stages 0 and 1 done on 2026-10-30: step A split 14 Recaps (001-008, 537-675) into 604 claims, with Opus as the writer. Opus beat Sonnet in a blind review. About 46 cu in all, against 16-25 estimated. Report: `holistic-alpha/logs/runs/2026-10-30-pilot-stages-0-1.md`
   - Test of step B on semen-retention done on 2026-11-01: `verify` OK, 72 lines, **0 merged**, 28 nested, 4 later views. 7 lines group claims from 2 or more episodes by nesting. Agents 4.3 cu, 0.059 cu per claim. Report: `holistic-alpha/logs/runs/2026-11-01-pilot-B-test.md`
   - Stopped at the stop line (3 or fewer merges). Cause: 4.3 merges only claims of the same strength and scope, and step A keeps each Recap's hedges, so repeats nest. Also a thin sample: 6 of the 18 Recapped episodes on the topic have claims
   - Esteban decided on 2026-11-01: nesting counts as grouping, 4.3 stays strict, and the measure is groups with 2 or more episodes
   - Second test done on 2026-11-01: step A on 12 more Recaps (769 claims from 345 bullets, 16.1 cu, 0.047 cu per bullet, 7 S2 fixed). Step B on 218 claims from 13 episodes: **22 groups with 2+ episodes, holding 119 claims**, 0 merged, 4 later views. One Opus pass 0.039 cu per claim. The Sonnet writer cost a fifth of Opus and had 2 S2 against 0 in a blind review. About 34.5 cu in all, against 45-55. On the branch `claude/project-thread-urm8wp`, on top of the pilot branch. Report: `holistic-alpha/logs/runs/2026-11-01-pilot-B-test-2.md`
   - Born in that run: `setbacks`. Raised: kegels and morning-wood to explicit, every-day, stress, sleep, dopamine and oxytocin to sexual-health
   - Waiting on Esteban: Opus or Sonnet as the writer of step B, the area of `+covid`, whether orgasm without ejaculation gets its own topic, and stage 2: step A on the other 31 Recaps (534 bullets, 32-40 cu). The topic list is decided after stage 2, with all the proposals
   - Whole vault projected at 4,300-5,100 cu with Opus in step B and 3,600-4,200 with Sonnet, both with full review. It was 5,400-6,100 before this run
2. First complete topic, cold exposure: keywords match 29 episodes and 25 lack a Recap. Recaps plus notes: 60-85 cu, to estimate again after the pilot
3. Second topic, root muscle and Kegels: keywords match 108 episodes and 11 have a Recap. It tests changes of view, since 721 asks "Are Kegels Critical or Counterproductive?"

The cost unit (cu) is defined in `tools/usage_report.py`. One 5-hour window holds about 50 cu. A Recap costs about 2.5 cu with the spot-check: the saved plans give 226 cu for 92 episodes.

## Decisions

Made by Esteban between 2026-10-26 and 2026-10-30. Change them only when he asks.

- **Recaps are the source of everything above them.** The vault replaces the transcripts: every idea said in an episode ends up in it
- **Six fixed areas:** mind, sex-energy, hormones, training, fuel, relationships. The first five are Steven's own split in 001, 002 and 029. Relationships was added because partner and family come up often and grow in later years
- **A topic is born at 3 episodes.** An earlier pilot gave 19 "concepts" from 10 episodes, which would be about 1,500 for 809. The 34 Recaps gave 25 topics. The guess for 809 is 60-100
- **One topic at a time.** Before pieces are made on a topic, all its episodes get a Recap. Pieces use only complete notes, so they miss nothing other episodes say
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
