# Run 2026-11-01: topic notes pilot, stage 2 and Esteban's decisions

Approved by Esteban on 2026-11-01 at 20:13 UTC. Branch `claude/project-thread-urm8wp`, never merged until he approves.

**Result: every one of the 57 Recaps now has its claims. 2,610 claims from 1,174 bullets, `check` with 0 ERROR.** Stage 2 cost about 45 cu, against 32-40 estimated, and Esteban was told mid-run.

## Esteban's decisions, 2026-11-01

1. Step B: Sonnet writes at medium effort, with full review and the Opus fixer. When cold is complete, Esteban reads its note. If it groups too little, it is rebuilt with Opus
2. Stage 2: yes, step A on the 31 Recaps without claims, Opus, full review
3. No review by sample in step A
4. Covid is not an area or a topic. It is context: each claim goes to the topic it talks about
5. Orgasm without ejaculation is its own topic, `orgasm`, area sex-energy, with `also: semen-retention`. The claims of 034 and 275 on it move there
6. The writers' open rules, now in the v2 instructions (below)
7. After stage 2: a proposal to adopt the v2 instructions and bring the branch to main. Then cold as the first production topic

## The rules written into the v2 instructions

- **4.4, Later view:** a later claim is a change of view when it would change what someone does or believes if they read only the older claim. A hedge that leaves the advice as it was nests without `later`. One Later view per group, under the group's top line
- **4.2, nesting:** a nested line can hold nested lines. A listener's or guest's question is a top-level line, and the host's answers nest under it
- **7, explicit:** any instruction of what to do during stimulation, even in one line
- **3.4, rule 7:** a context such as Covid is not a subject
- **9, process:** full review everywhere. Step B: Sonnet writes, Sonnet reviews, Opus fixes

## Registry moves

One Opus agent, 3.44 cu. Every change is logged in `logs/claims/findings/registry-2026-11-01.jsonl` (38 rows).

- **`orgasm`:** 20 claims of 034 and 2 of 275 (the `+orgasm` rows) moved from semen-retention, with `semen-retention` in `also`. 034-39 to 034-42 and 034-44 stay in semen-retention. The agent also added `orgasm` to the `also` of 7 kegels and edging claims of 034 that name it
- **Covid:** the 3 `+covid` claims of 150 fit no topic or proposal. They went to a new proposal, `+freedom` "Freedom and government control", area mind
- **The semen-retention note:** the 20 ids came off its layout. `verify` then gave 198 claims and 16 groups with 2+ episodes, from 22: the orgasm groups left with their claims
- **Left as they are, for Esteban:** claims of 002, 006, 027 and 029 on orgasm without ejaculation are still in semen-retention. The brief named only 034 and 275

## Stage 2: step A on 31 Recaps

Opus wrote, Sonnet reviewed (with "lost in split"), Opus fixed, all at effort xhigh. Four blocks in series.

| block | Recaps | bullets | claims | cu | cu per bullet |
|---|---|---|---|---|---|
| 009-018 | 8 | 122 | 292 | 8.81 | 0.072 |
| 019-025 | 7 | 125 | 260 | 7.63 | 0.061 |
| 026-033 | 6 | 134 | 311 | 8.57 | 0.064 |
| 079-815 | 10 | 153 | 374 | 8.64 | 0.056 |
| **total** | 31 | 534 | 1,237 | **33.65** | **0.063** |

- 2.32 claims per bullet. The registry: 2.22
- The second test measured 0.047 cu per bullet and stage 1 0.06. 0.06 is the number to plan with

**Findings: 0 S1, 13 S2, 20 S3. 31 fixed, 2 rejected.**
- S2: 7 not standalone, 4 lost in split, 1 hedge lost, all fixed. 1 source lost rejected (812-07: the Recap credits the data with less than the claim's sentence)
- S3: 10 wrong topic, 7 not split, 3 wrong level. 1 wrong level rejected (018-24: "last longer in bed" names no act)
- **12 confirmed S2 in 1,237 claims, 1.0 per 100.** The second test: 0.9. Stage 1: 2.5

Points the writers found unclear, not yet in the rules:
- A label bullet that also states something ("Personally, the two biggest benefits are:"). Writers carry its hedge into the nested claims
- How far a parent hedge reaches: 026's "some are very new and only on mice" over eight nested bullets. "Only on mice" was lost in 3 and fixed. "Very new" covers only some of them, so it stays once
- General hormone facts: the fixer moved 8 claims of 026 and 028 from testosterone to a new proposal, `+hormone-basics`. 001-18 and 002-43 hold the same kind of claim and stay in testosterone
- Whether a `+slug` in `also` counts toward a birth. It doesn't: only `topic` counts

## Topics born and levels raised

Into `topics.csv` in this run's commit:
- **`orgasm`**, "Orgasm without ejaculation", sex-energy, by Esteban's decision. 23 claims from 3 episodes
- **`habits`**, "Habits and tracking", mind. 5 episodes (014 018 032 549 556)
- **`breathing`**, mind. 4 episodes (275 289 404b1 813)
- **`alcohol`**, fuel. 3 episodes (016 127 303)
- **`cold`**, parked until now, becomes a topic: 4 episodes with claims, 61 claims

Raised, from the claims' levels:
- To explicit: orgasm
- To sexual-health: toxins, recovery, regret, sprints, truth, never-too-late, partner-family, dhea

Keywords for the new topics are guesses from their claims. `habits` matches 193 episodes and `breathing` 103, so both are wide. `topic-episodes.csv` was rebuilt with `tools/topic_episodes.py`: only the rows of the four new topics are new.

**Proposals to watch:** 34 subjects. At 2 episodes: `+discipline`, `+erections` (303, 812), `+hormone-basics`, `+purpose`, `+coffee`, `+shame`, `+balance`, `+community`, `+alpha-male`.

## The semen-retention note

Step B was not run again, so the note is the second test's, minus the orgasm claims. Stage 2 filed 5 more claims under semen-retention (014-21, 019-13 to 019-16). `verify` lists them as on no line until step B places them.

## Cost

| | cu |
|---|---|
| Registry moves | 3.44 |
| Step A, 12 agents | 33.65 |
| Orchestration in this session, since 20:13 | about 8 |
| **Total** | **about 45** |

- Estimate: 32-40 cu. Step A came in at 0.063 cu per bullet instead of 0.047
- Orchestration was about 22% of the agents. This session was long, so each agent's report cost more to read

## Next, with costs

1. **Adopt the v2 instructions and bring the branch to main**, as Esteban asked. Free: one commit that marks v2 as adopted, then a pull request. Esteban merges
2. **Cold, the first production topic.** Keywords match 29 episodes, 25 without a Recap
   - Recaps: 25 × 2.5 = about 63 cu
   - Step A: 25 Recaps at about 1.1-1.4 cu each, 28-35 cu
   - Step B with Sonnet and full review: about 0.020 cu per claim, 4-6 cu
   - Orchestration: 10-15 cu
   - **About 105-120 cu, 2-2.5 windows.** STATUS gave 60-85 before the pilot measured step A
3. Small fixes for Esteban to decide:
   - Move the orgasm claims of 002, 006, 027 and 029 to `orgasm`, about 1 cu
   - Whether `+erections` lives on its own or next to morning-wood

## Files

- Rules: `holistic-alpha/topic-instructions.md` (v2 draft)
- Registry: `holistic-alpha/claims/`, 57 files and `_proposed.csv`
- Briefs: `logs/claims/prompts/{009-018,019-025,026-033,079-815}-*.md`, `registry-2026-11-01-fixer.md`
- Reviews: `logs/claims/review/`. Findings: `logs/claims/findings/`
- Stats: `logs/claims/stats-2026-11-01-stage-2.md`
