# Brief: second test of step B on semen-retention, with 12 more Recaps

Approved by Esteban on 2026-11-01 at 14:09 UTC. Branch `claude/topic-notes-two-steps`, never merged until he approves. Talk to him in Spanish, in short lines.

Read first: `STATUS.md`, `holistic-alpha/logs/runs/2026-10-30-pilot-stages-0-1.md`, `holistic-alpha/logs/runs/2026-11-01-pilot-B-test.md`, and `holistic-alpha/topic-instructions.md` (v2 draft) sections 3, 4 and 9.

## Esteban's decisions, 2026-11-01

1. Nesting counts as grouping. 4.3 stays strict: a merged line never takes the most cautious text for both claims. **The measure is now "groups with 2 or more episodes"**, not merged lines. Done: `topic_note.py` 0.4 counts them, and a top-level line shows its group's episodes, `(002 · also 006, 675)`
2. Step A on the 12 Recaps of semen-retention that have no claims, with Opus and full review, as in stage 1
3. Step B twice on the 18 episodes: Opus at effort xhigh, as in the first test, and Sonnet at effort medium. Compare cost, groups, Later views and review findings. B writes only ids and `verify` checks them, so it is where most can be saved
4. Coordination from a short session: this one
5. The writer's doubts, now in 4.3 and 4.4: one Later view for each older line that changes. A guest who disagrees is nested with his Guest marker, never a Later view. A claim that repeats another and adds a hedge is nested
6. Review by sample is decided later, from this test's errors. Step A keeps full review for now. Step B may lower it sooner

## The run, in this order

**1. Step A, block 1: 011 016 027 029 034 088** (150 bullets, mostly 2019)
- Writer Opus, reviewer Sonnet, fixer Opus, all at effort xhigh. One agent at a time
- Copy the briefs `holistic-alpha/logs/claims/prompts/537-675-{writer,reviewer,fixer}.md` to `011-088-*.md` and change only the block: ids, Recap paths (from `holistic-alpha/episodes.csv`), file names. The reviewer also checks "lost in split" (9.1)
- Registry `holistic-alpha/claims`. Review `logs/claims/review/011-088.json`, findings `logs/claims/findings/011-088.jsonl`

**2. Step A, block 2: 127 150 175 275 731 813** (195 bullets), the same way, after block 1: proposals are read in series (3.4)

**3. After step A**
- `python3 -I tools/claims.py check <all 26 ids>` with 0 ERROR, then `proposed`, then `stats --out holistic-alpha/logs/claims/stats-2026-11-01.md`
- A proposal that reaches 3 episodes enters `topics.csv` in this run's commit (3.4). A topic whose claims reach a higher level is raised (7)

**4. Step B, two writers, one after the other**
- Opus, effort xhigh: writes a new `holistic-alpha/topics/sex-energy/semen-retention.layout` from the claims alone, replacing the first test's layout (git keeps it)
- Sonnet, effort medium: writes `holistic-alpha/logs/topics/sonnet/sex-energy/semen-retention.layout`, with `--notes holistic-alpha/logs/topics/sonnet` on `render` and `verify`
- One brief for both, `logs/topics/prompts/semen-retention-2-writer.md`, from `semen-retention-writer.md`: say the layout folder, drop "This test exists to see whether step B merges", ask for groups across episodes where claims are the same claim at another strength or scope, never to reach a number. Neither writer reads the old layout or the other one

**5. Blind review**
- Copy the two layouts to `holistic-alpha/logs/topics/blind/x/sex-energy/` and `.../blind/y/sex-energy/`, in an order you choose at random, and render each with `--notes`. Write the key in the report only after both reviews
- One Sonnet reviewer per folder, effort xhigh, one brief that names no model: `semen-retention-2-reviewer.md`, from `semen-retention-reviewer.md`, with `--notes` and a check for missed groups. Reviews: `logs/topics/review/semen-retention-2-x.json` and `-y.json`

**6. Fixer, Opus, effort xhigh,** on the Opus layout only, the note of record, from its review. Findings `logs/topics/findings/semen-retention-2.jsonl`. Sonnet's layout is kept to compare. `verify` OK at the end

**7. Report** `holistic-alpha/logs/runs/<date>-pilot-B-test-2.md`, in English:
- Step A: cost per Recap and per bullet, findings by severity and kind with verdicts. They feed the sample decision
- Step B: one table, Opus and Sonnet: cost, lines, groups with 2+ episodes and their claims, merged, nested, Later views, misplaced, findings by severity and kind. The `verify` lines
- Topics born and levels raised
- The vault projection of the first report, with the new numbers
- Cost of orchestration in this session

Then update `STATUS.md`, commit on the branch, push, and tell Esteban: groups, cost, Opus or Sonnet for B, and what he decides next.

## Cost

- Step A: about 21 cu (150 bullets at 0.050, 195 at 0.069, as measured in stage 1)
- Step B: 18-28 cu. Semen-retention will hold about 220-320 claims, three to four times the first test. Opus writer 0.033 cu per claim, two blind reviews, one fixer, Sonnet writer cheaper
- Orchestration: about 5 cu
- **Total: 45-55 cu, about one window.** If the running total passes 60 cu, stop and report

## Don't

- Don't run step A on the other 31 Recaps (stage 2) or on any episode not listed here
- Don't edit Recaps, `recap-instructions.md`, `episodes.csv` or `topic-episodes.csv`. Don't merge to main
- Keep this session short: one Agent call per step, with a short prompt that points at its brief file. Read only each agent's final report. Measure cost with `python3 -I tools/usage_report.py` on the subagent logs in `~/.claude/projects/-home-user-wisdom/<session id>/subagents/`
