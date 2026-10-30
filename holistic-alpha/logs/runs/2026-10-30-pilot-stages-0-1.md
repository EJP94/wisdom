# Run 2026-10-30: topic notes pilot, stages 0 and 1 (step A)

The two-step design approved by Esteban on 2026-10-30, plan v2 with his adjustments. Branch `claude/topic-notes-two-steps`, never merged until he approves.
Step A splits each Recap into claims, saved in `holistic-alpha/claims/<id>.jsonl`. Step B, not run yet, builds a note from a topic's claims.

## Stage 0: rules and scripts

- `holistic-alpha/topic-instructions.md` v2, a draft. Version 1 stays the rule on `main`
- `tools/claims.py`: fill, check, proposed, stats, compare
- `tools/topic_note.py`: claims, render, verify. Each line's text is word for word one claim. Tested on 079 and on the kegels claims of the registry
- Added during the run, from Esteban: a hedge, number or source lost in a split (3.2, 9.1), pointers with the link and the ids only (4.5), a blind Opus and Sonnet comparison
- Clarified during the run, from the writers' notes: a label bullet ("How:") gives one claim with its own words and topic `none`; Guest markers can carry a name; a born proposal keeps its `+slug` in the registry
- Cost: 6.15 cu, all orchestration. Estimate was 3-5 cu

## Stage 1: cost

| run | Recaps | bullets | claims | writer | review | fix | total | per Recap | per bullet |
|---|---|---|---|---|---|---|---|---|---|
| Opus 001-008 | 8 | 144 | 295 | 4.14 | 1.61 | 1.47 | 7.22 | 0.90 | 0.050 |
| Opus 537-675 | 6 | 151 | 307 | 6.10 | 2.24 | 2.09 | 10.43 | 1.74 | 0.069 |
| Second round on Opus, Esteban's additions | 14 | 295 | | | 2.64 | 3.46 | 6.10 | | |
| Sonnet 001-008, to compare | 8 | 144 | 302 | 3.73 | 4.02 | | 7.75 | | |

- Second round: the blind review of Opus 001-008 (1.58), a focused check of 537-675 for hedges lost in a split (1.06), and one fixer for both (3.46)
- Sonnet's review: the first review (1.81) and the blind one (2.21). No fixer: its claims are kept only to compare
- Orchestration: 9.2 cu, from a session with a long context
- **Stage 1 total: about 40 cu. Estimate was 13-20 cu.** The blind second round added 6.1 cu, orchestration 9 cu, and 537-675 has twice the bullets per Recap of 001-008
- One pass of step A with Opus (write, review, fix) costs about **0.06 cu per Recap bullet**: 0.9 cu for a 2019 solo Recap, 1.7 cu for a long interview
- For comparison, v1 notes of 001-008 cost 12.24 cu

## Opus or Sonnet as the writer of step A

Same Recaps (001-008), same rules. The blind review ran on two folders, `blind/x` and `blind/y`, with one brief that names no model. The key was read after: x was Opus, y was Sonnet.

| | Opus | Sonnet |
|---|---|---|
| Writer cost | 4.14 cu | 3.73 cu |
| Output tokens | 71k | 111k |
| Claims | 295 | 302 |
| Blind review | 0 S1, 1 S2, 11 S3 | 0 S1, 8 S2, 8 S3 |
| First review | 0 S1, 3 S2, 1 S3 | 0 S1, 8 S2, 6 S3 |

- S2 matters most, because step B copies claims word for word. Sonnet's S2 are mostly claims that don't read alone ("those powerful changes", "The sets") and two hedges lost in a split
- Opus's one blind S2 was rejected by the fixer: "In this view" is the Recap's own hedge
- 8 of Opus's 11 blind S3 are label bullets summarized, a rule added after both writers ran
- The two writers split 21 of 144 bullets into a different number of claims, and gave 20 a different topic: `logs/claims/compare-001-008.md`
- **Verdict: Opus.** Sonnet's writer costs 10% less, because it writes more tokens, and its claims need about three times the fixes

## The registry after stage 1

- 14 Recaps, 295 bullet lines, 604 claims, 2.0 per bullet: `logs/claims/stats-2026-10-30.md`
- `check`: 0 ERROR, 0 WARN on all 14
- Findings on Opus's claims, both rounds: S2 15 fixed, 5 rejected. S3 15 fixed, 37 rejected. 36 of the rejected S3 flagged `+emotions` as a duplicate after it was born during the run
- No S1 in any review

## Topics

- **The 2019 topic list misses later subjects.** In 001-008, 3% of claims went to a proposed subject. In 537-675, 39% did
- Open proposals: discipline (38 claims, 2 episodes), habits (29, 2), setbacks (27, 2), religion (11, 1), shame (11, 2), community (5, 2), balance (5, 1), comparison (2, 1), alpha-male (1, 1)
- Born and added to `topics.csv`: **emotions** (a proposal, 3 episodes: 537 549 675) and **porn** (parked, now 3 episodes)
- Explicitness raised in `topics.csv`, from the claims' levels: fasting and meditation to sexual-health, life-force to explicit
- Biggest topics so far: edging 75 claims, semen-retention 72, strength 39

## Points the writers found unclear

- How far a marker that opens a sentence inside a bullet reaches
- "[speaker unclear]" has no marker, so the writer kept it in the claim text
- A story told over several bullets keeps one topic, even when its lines change subject
- Resolving "this practice" or "it" so a claim reads alone is the riskiest step. Most S2 findings were here

## Projection

- **Stage 2**, the other 43 Recaps (879 bullets: 501 in 26 Recaps from 2019, 378 in 17 later ones): about 50-55 cu with Opus, one review with the new check and one fixer, plus orchestration. More than one window
- **All 809 Recaps**, at about 22 bullets each: about 1,000 cu for step A with full review, about 600 cu with the writer alone. A Recap costs about 2.5 cu, so step A adds 25-40% to it
- Ways to cut: review a sample once the error rate is known, larger blocks, orchestration from a short session

## Files

- Registry: `holistic-alpha/claims/` (14 files and `_proposed.csv`)
- Sonnet's claims: `holistic-alpha/logs/claims/sonnet-001-008/`. Blind copies: `holistic-alpha/logs/claims/blind/`
- Reviews: `holistic-alpha/logs/claims/review/`. Findings with verdicts: `holistic-alpha/logs/claims/findings/`
- Briefs of every agent: `holistic-alpha/logs/claims/prompts/`
