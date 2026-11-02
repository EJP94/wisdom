# Run 2026-11-01: topic notes pilot, test of step B on semen-retention

Approved by Esteban on 2026-10-30 (brief: `2026-10-30-pilot-B-test-brief.md`). Branch `claude/topic-notes-two-steps`, never merged until he approves.

**Result: 0 merged lines. The stop line was 3, so stage 2 waits and this report diagnoses.** `verify` passes. Step B groups across episodes by nesting instead: 7 of 44 top-level lines gather claims from 2 or more episodes.

## The run

- Input: 72 claims from 6 episodes (002, 006, 537, 549, 565, 675), plus 23 pointer claims
- Writer, Opus: 71 lines, 1 merge (002-33 with 006-23), 26 nested, 3 later views
- Reviewer, Sonnet: 0 S1, 2 S2, 1 S3. No missed merge, no In short, misplaced or pointer finding
- Fixer, Opus: all 3 fixed, 0 rejected

| finding | severity | kind | fix |
|---|---|---|---|
| 002-33 "no matter how" with 006-23 "especially alone" | S2 | merge widened | 006-23 nested under 002-33. The only merge is gone |
| 675-23 changes 006-26 "absolutely don't ejaculate" | S2 | view change hidden | `later 675-23` under 006-26 |
| 565-32, 565-33 (a guest's "not a pass-fail test") in Releasing | S3 | wrong section | moved to What it is and is not |

Final `verify`: `semen-retention: OK. 72 claims, 72 lines, 0 merged, 28 nested, 4 later views, 0 misplaced`. Note: `holistic-alpha/topics/sex-energy/semen-retention.md`, layout beside it. Findings with verdicts: `logs/topics/findings/semen-retention.jsonl`. Briefs: `logs/topics/prompts/`.

The 7 groups across episodes:
- 002-33 > 006-23, 675-22 (too much ejaculation drains you)
- 002-34 > 006-14, 006-15, 006-39, later 675-21 (ejaculating alone)
- 006-26 > 006-27, later 675-23 (> 675-16, 675-17), later 675-26 (edge, don't ejaculate)
- 002-38 > 006-30, 002-40 > 006-66, 006-46, 006-42 > 549-66, 006-43 > later 549-63

## Cost

| | cu |
|---|---|
| Writer, Opus | 2.40 |
| Reviewer, Sonnet | 0.91 |
| Fixer, Opus | 0.95 |
| Orchestration on 2026-11-01 | about 5 |
| Preparation on 2026-10-30: brief, `claims.py merge` | 6.03 |

- **Agents: 4.26 cu, 0.059 cu per claim. The writer alone: 0.033 cu per claim.** Estimate was 2-4 cu for the whole run
- The run with orchestration: about 9 cu. With the preparation: about 15 cu
- The writer spent 44k output tokens, mostly reasoning, on a 72-line layout

## Diagnosis: why 0 merges

Esteban's question: the topic, the claims' wording, or the rules of 4.3?

1. **The rules and the wording together, first.** Step A keeps each Recap's hedges and scope, and 4.3 merges only claims with the same strength and scope. Two episodes rarely say a thing with the same hedge. 002-34 "avoid it ever if at all possible, or very, very infrequently" and 006-14 "has to go" say the same thing at two strengths, so they nest. Under these rules a repeat across episodes becomes a nested line, almost never a merged one
2. **The topic sample, second.** Of the 6 episodes, only 002 and 006 cover the same ground. 675 holds 34 of the 72 claims, on one question (the emotional wall) that no other episode touches. 537, 549 and 565 mention retention in passing. 18 of the 57 Recaps match semen-retention by keywords, and only 6 have claims yet
3. **Not the writer.** The reviewer found no missed merge, and the writer's one merge was false

So more episodes alone will probably not bring merges as defined. They will bring more nested lines under the same parents. What a merge means needs Esteban's call before stage 2.

## Comparison with v1

| | v1 (001-024) | v2 (14 Recaps) |
|---|---|---|
| Episodes | 5, by its frontmatter | 6 (002 006 537 549 565 675) |
| Lines | 14 | 72 |
| Merged lines | 0 | 0 |
| Lines that group 2+ episodes | 0 | 7 groups, 23 claims |
| Later views | 0 | 4 |
| Words, 002 / 006 | 150 / 224 | 152 / 493 |

- v1 copied whole bullets. v2 splits them into claims, so the same 002 content takes 7 lines instead of 3, with the same words
- 006 has twice the words in v2: step A filed 21 of its claims under semen-retention, where v1 kept 6 bullets

## Two script outputs fixed during the run

- Pointers to a proposed topic had a link to a note that doesn't exist, against "wikilinks only to other topic notes". Now `- See habits, a proposed topic (549)`, without a link (`topic_note.py` 0.3, section 4.5)
- The reviewer needs the pointer claims: `topic_note.py claims <slug> --pointers` lists them
- Not changed: the note's explicitness is sexual-health while `topics.csv` says explicit. Section 7 sets a topic's level from its claims, so it is raised only when claims reach higher, never lowered

## Points the writer found unclear

- 4.4: when a change of view spreads over many claims (675-20, 675-23, 675-29, 675-31 contradict 2019), does each need `later`? The writer marked one per older line
- 4.4: does `later` cover a guest who disagrees with the host? 565-32 and 565-33 stay unmarked
- 4.3: a claim that repeats another and adds a hedged clause (675-22): held back and nested

## Projection: the whole vault

Base numbers:
- 809 episodes, 57 Recaps done. A Recap costs about 2.5 cu with the spot-check, 1.9 without
- Bullets: 6.9 per 1,000 transcript words in the 57 Recaps, so about 15,000 for the 809. The earlier guess of 22 per Recap gives 17,800
- Claims: 2.05 per bullet, so 31,000-37,000. 3% go to `none`
- Step A, one pass of write, review and fix: 0.06 cu per bullet. The writer alone: 0.035
- Step B, one pass: 0.059 cu per claim. The writer alone: 0.033. One topic measured: bigger topics may cost more per claim
- Orchestration: 9.2 of 31.5 cu of agents in stage 1, about 30%. More in small runs

| | cu |
|---|---|
| Recaps, 752 to go | 1,880 |
| Step A | 900-1,070 |
| Step B | 1,830-2,180 |
| Orchestration, 30% of A and B | 820-980 |
| **Total** | **5,400-6,100**, about 110-120 windows of 50 cu |

**Step B costs about twice step A.** Per claim it costs about what A costs per bullet, and there are twice as many claims as bullets.

Which option lowers it most:

| option | saves | cost to quality |
|---|---|---|
| **Review by sample**, 1 Recap and 1 topic in 5 | about 1,000 cu (A 320, B 700) | about 80% of S2 errors stay. A had 15 S2 in 604 claims, B 2 in 72 |
| **Orchestration from short sessions** or a workflow, 30% down to 5-10% | 600-800 cu | none |
| **The Recap writer writes the claims** | 300-500 cu: A's second reading of the Recap (about 57% of A's writer cost), and part of its review if the Recap reviewer checks the claims | only for the 752 Recaps to go. A longer task for the writer of the canonical layer |

- In cu, review by sample lowers it most. It is also the only option that lowers quality
- Orchestration is second, with no cost to quality, and combines with the other two
- All three together: about 2,000 cu less, so about 3,700-4,100 cu

## What Esteban decides next

1. What counts as a merge. The rules as written give merges near zero and nest repeats instead
2. Whether to test B again on semen-retention with its other 12 Recapped episodes (345 bullets: about 21 cu for step A, which stage 2 needs anyway, and 5-8 cu for B), or go to stage 2, or change 4.3 first
3. Which cost options to adopt

## Files

- Note and layout: `holistic-alpha/topics/sex-energy/semen-retention.{md,layout}`
- Review: `logs/topics/review/semen-retention.json`. Findings: `logs/topics/findings/semen-retention.jsonl`
- Briefs: `logs/topics/prompts/semen-retention-{writer,reviewer,fixer}.md`
