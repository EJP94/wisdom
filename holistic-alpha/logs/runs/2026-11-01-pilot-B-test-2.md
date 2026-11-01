# Run 2026-11-01: topic notes pilot, second test of step B on semen-retention

Approved by Esteban on 2026-11-01 at 14:09 UTC (brief: `2026-11-01-pilot-B-test-2-brief.md`). Pushed to the branch `claude/project-thread-urm8wp`, which sits on top of `claude/topic-notes-two-steps`. Never merged until he approves.

**Result: 22 groups with 2 or more episodes, holding 119 of 218 claims. `verify` passes.** Still 0 merged lines: every group is built by nesting, as Esteban decided. The whole run cost about 34 cu, against 45-55 estimated.

## Step A: 12 Recaps

Opus wrote, Sonnet reviewed, Opus fixed, all at effort xhigh. The reviewer also checked "lost in split".

| block | bullets | claims | writer | reviewer | fixer | cu | cu per bullet | cu per Recap |
|---|---|---|---|---|---|---|---|---|
| 011 016 027 029 034 088 | 150 | 387 | 5.56 | 2.11 | 1.39 | 9.06 | 0.060 | 1.51 |
| 127 150 175 275 731 813 | 195 | 382 | 4.46 | 1.71 | 0.83 | 7.00 | 0.036 | 1.17 |
| **total** | 345 | 769 | 10.02 | 3.82 | 2.22 | **16.06** | **0.047** | 1.34 |

- Estimate was about 21 cu. Stage 1 measured 0.06 cu per bullet
- 2.23 claims per bullet, against 2.05 in stage 1. The registry now holds 1,373 claims from 640 bullets of 26 Recaps, 2.15 per bullet
- `check` on all 26 ids: 0 ERROR, 0 WARN. Stats: `logs/claims/stats-2026-11-01.md`

**Findings: 0 S1, 8 S2, 1 S3. 8 fixed, 1 rejected.**

| claim | severity | kind | verdict |
|---|---|---|---|
| 011-22 | S2 | not standalone | fixed |
| 127-11 | S2 | not standalone | fixed |
| 275-38 | S2 | not standalone | fixed: "being out of balance is a common mistake" |
| 034-47 | S2 | lost in split | fixed: "Probably" put back |
| 731-39, 731-40 | S2 | lost in split | fixed: "and maybe for a good period" put back |
| 016-14 | S2 | lost in split | rejected: the source covers the claim after the colon, which 016-13 carries |
| 034-41 | S2 | claim strengthened | fixed: "on a super regular basis" put back |
| 011-29 | S3 | not split | fixed: split into 011-29 and 011-32 |

For the sample decision:
- 7 confirmed S2 in 769 claims, 0.9 per 100. Stage 1 had 15 in 604, 2.5 per 100
- No idea lost and no wrong speaker in either stage. Every S2 is a hedge or a referent, and step B copies it word for word into the note
- 3 of the 7 are "lost in split", which the reviewer checked in the same pass this time. In stage 1 it took a second round

## Step B: Opus and Sonnet on the same 218 claims

Input: 218 claims from 13 episodes (002 006 011 027 029 034 088 127 537 549 565 675 731), plus 70 pointer claims. 150, 175, 275 and 813 match the topic by keywords but filed no claim under it.

The blind key: x = Opus, y = Sonnet. One Sonnet reviewer per folder, at effort xhigh, with a brief that names no model.

| | Opus, xhigh | Sonnet, medium |
|---|---|---|
| Writer | 4.68 cu, 0.021 per claim | **0.84 cu, 0.004 per claim** |
| Blind review | 1.83 cu | 1.62 cu |
| Lines | 218 (61 top-level) | 218 (83 top-level) |
| Groups with 2+ episodes | 24, 118 claims | 24, 97 claims |
| Merged | 0 | 0 |
| Nested | 157 | 135 |
| Later views | 5 | 4 |
| Misplaced | 0 | 0 |
| Review: S1 | 0 | 0 |
| Review: S2 | **0** | **2** view change hidden |
| Review: S3 | 6: 4 merge missed, 1 wrong nesting, 1 misplaced | 7: 3 merge missed, 1 wrong section, 1 wrong nesting, 1 misplaced, 1 pointer |

- Sonnet's two S2: 731-43 "some feel no change after release" is not a Later view of 006-21 "the reset button". 675-26 is not one of 006-26 "absolutely don't ejaculate". Opus had marked both. They have no verdicts, since only the Opus layout had a fixer
- Sonnet's first `verify` caught two ids placed twice (088-19, 088-60). The script did its job
- Both reviewers found the same two missed groups in both layouts: 002-39 with 029-50, and 029-52 with 006-43 and 002-37. Both writers missed them

**The fixer, Opus, on the Opus layout: 1.89 cu. 4 S3 fixed, 2 rejected.**
- Fixed: 549-63 is nested under 549-64 and is no longer a Later view. 675-21 joins 731-56 and 731-57 as `later` under 002-34. The 731-51 group goes under 027-19. The 029-52 group goes under 002-37
- Rejected: 002-39 stays in "How often to ejaculate", where it heads the frequency lines and their Later view 731-34. 731-25 stays here: it is about swearing off porn, masturbation and orgasm (NoFap), and the registry already gives it `also porn`

The `verify` lines:
- Opus, first: `semen-retention: OK. 218 claims, 218 lines, 24 groups with 2+ episodes (118 claims), 0 merged, 157 nested, 5 later views, 0 misplaced`
- **Opus, after the fixer, the note of record:** `semen-retention: OK. 218 claims, 218 lines, 22 groups with 2+ episodes (119 claims), 0 merged, 160 nested, 4 later views, 0 misplaced`
- Sonnet: `semen-retention: OK. 218 claims, 218 lines, 24 groups with 2+ episodes (97 claims), 0 merged, 135 nested, 4 later views, 0 misplaced`

The fixer joined groups, so their count fell from 24 to 22 while the claims in them rose to 119.

**Against the first test**: 72 claims from 6 episodes gave 7 groups with 23 claims. Now 218 from 13 give 22 groups with 119. The share of claims in a group went from 32% to 55%.

**Cost per claim fell with a bigger topic.** One Opus pass, writer, review and fixer: 8.40 cu, 0.039 per claim, against 0.059 in the first test. The writer alone: 0.021, against 0.033.

The note: 294 lines, 6,600 words.

**B: Opus or Sonnet.** Sonnet writes for a fifth of the cost and groups less: 97 claims in groups against 118, and two hidden changes of view. B cannot lose an idea: `verify` checks every claim is on one line, word for word. Its errors are in grouping and Later views, and the review catches them. So:
- Sonnet writer with full review and the Opus fixer: about 0.020 cu per claim. The fixer's cost on a Sonnet layout is not measured: it has more findings to fix
- Opus writer with review by sample, 1 topic in 5: about 0.025 cu per claim
- Opus with full review, as now: 0.039 cu per claim

## Unclear rules the writers named

Step A:
- When a claim is `explicit`: both writers drew the line at steps done during stimulation. "Step by step" in section 7 is vague for one-line instructions
- How far a hedge reaches past a colon or a semicolon (027 l.27, 029 l.57). Writers carry it within the sentence
- A bullet that is a label with content (029 l.42, 034 l.35 "To start practicing:"). Section 3.1 covers only pure labels
- 275-13 takes the names "root squeeze" and "root push" from its nested bullets. Section 3.2 allows words from the bullet, its parent or the bullet before. The reviewer found it correct
- **Orgasm without ejaculation**: the block 1 writer filed 034 under `semen-retention`, like 002 and 006. The block 2 writer proposed `+orgasm` for 275. The same subject now has two homes

Step B:
- Opus: one Later view per group or per nested line? It gave one per group, under its top line
- Opus: a claim can serve as the Later view of one older line only, since each claim appears once
- Opus: whether host answers nest under a listener question. It kept questions as top lines
- Sonnet: whether a Later view needs a contradiction, or a softening is enough
- Sonnet: whether a nested line can hold nested lines. It avoided it, which pushed lines to the top level

## Topics born and levels raised

- **Born: `setbacks`**, "Setbacks and slips", area mind, 4 episodes (088 175 537 549), 33 claims. It enters `topics.csv` at sexual-health, with keywords guessed from its claims: relapse, setback, slip up, off the path, funk, back on track, fresh start. They match 27 episodes. Its rows keep `+setbacks`
- **Raised in `topics.csv`**, from the claims' levels (section 7):
  - To explicit: kegels, morning-wood
  - To sexual-health: every-day, stress, sleep, dopamine, oxytocin
- `topic-episodes.csv` was rebuilt with `tools/topic_episodes.py`. Only the 27 rows of `setbacks` are new
- **Esteban decides:** `+covid` "Covid and lockdowns" (150) fits none of the six areas, so it has area `?`. It has 1 episode and stays parked
- 24 subjects are proposed. The ones at 2 episodes: `+discipline`, `+habits`, `+breathing`, `+shame`, `+alcohol`, `+balance`, `+community`

## The vault projection, with the new numbers

Base numbers:
- 809 episodes, 57 Recaps done. A Recap costs about 2.5 cu with the spot-check
- About 15,000 bullets in the 809, and up to 17,800 by the older guess. Claims at 2.15 per bullet: 32,000-38,000
- Step A, one pass: 0.047-0.060 cu per bullet
- Step B, one Opus pass: 0.039 cu per claim. With the Sonnet writer: about 0.020
- Orchestration: 25% of A and B, as in this run (below)

| | first report | Opus B, full review | Sonnet B, full review |
|---|---|---|---|
| Recaps, 752 to go | 1,880 | 1,880 | 1,880 |
| Step A | 900-1,070 | 700-1,070 | 700-1,070 |
| Step B | 1,830-2,180 | 1,250-1,480 | 640-760 |
| Orchestration | 820-980 | 490-640 | 340-460 |
| **Total** | **5,400-6,100** | **4,300-5,100** | **3,600-4,200** |

In windows of 50 cu: 110-120 before, 86-101 with Opus B, 71-83 with Sonnet B. Review by sample in step A would save about 200-300 more, at the risk of about 0.7 S2 per 100 claims left in.

## Cost of this run

| | cu |
|---|---|
| Step A, 6 agents | 16.06 |
| Step B, 5 agents | 10.86 |
| Orchestration in this session | about 7.5 |
| **Total** | **about 34.5** |

- Estimate: 45-55 cu. Step A came in under (16 against 21) and step B well under (11 against 18-28), since the cost per claim fell
- Orchestration was 28% of the agents' cost. Each agent's report wakes the session, which reads its whole context again. A short session keeps that context small but does not remove the reads: about 0.35 cu per agent

## Files

- Registry: `holistic-alpha/claims/` (12 new files, `_proposed.csv`)
- Step A: briefs `logs/claims/prompts/{011-088,127-813}-*.md`, reviews `logs/claims/review/`, findings `logs/claims/findings/{011-088,127-813}.jsonl`
- The note of record and its layout: `holistic-alpha/topics/sex-energy/semen-retention.{md,layout}`. It replaces the first test's, which git keeps
- Sonnet's layout, kept to compare: `logs/topics/sonnet/sex-energy/`
- Blind copies: `logs/topics/blind/{x,y}/`. Reviews `logs/topics/review/semen-retention-2-{x,y}.json`. Findings `logs/topics/findings/semen-retention-2.jsonl`
- Step B briefs: `logs/topics/prompts/semen-retention-2-{writer,reviewer,fixer}.md`

## What Esteban decides next

1. **Who writes step B:** Sonnet with full review, or Opus. Sonnet halves step B in the projection
2. **Stage 2:** step A on the other 31 Recaps (534 bullets). About 25-32 cu for the agents, 32-40 cu with orchestration, under one window
3. **Review by sample in step A:** this run had 0.9 confirmed S2 per 100 claims and no S1
4. **The area of `+covid`**, and whether orgasm without ejaculation stays in `semen-retention` or becomes its own topic
