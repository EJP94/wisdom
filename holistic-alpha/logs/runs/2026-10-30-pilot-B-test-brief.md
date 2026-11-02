# Brief: test step B on semen-retention, before stage 2

Approved by Esteban on 2026-10-30 at 23:04 UTC. Branch `claude/topic-notes-two-steps`, never merged until he approves. Talk to him in Spanish.

Read first: `STATUS.md`, `holistic-alpha/logs/runs/2026-10-30-pilot-stages-0-1.md`, and `holistic-alpha/topic-instructions.md` (v2 draft) sections 4 and 9.2.

## Why

Step A has claims for 14 Recaps (001-008, 537-675). Before spending 50-55 cu on step A for the other 43 Recaps, check that step B merges claims across episodes. If it doesn't, the format of A changes and stage 2 would be redone.

## The run

Topic `semen-retention`: 72 claims from 6 episodes in the registry today, plus pointers from other topics. Estimate: 2-4 cu.

1. `python3 -I tools/topic_note.py claims semen-retention` gives the writer its input
2. **Writer, Opus, effort xhigh:** writes `holistic-alpha/topics/sex-energy/semen-retention.layout` (sections 4.2 to 4.4), runs `render` and `verify`, fixes the layout until `verify` passes
3. **Reviewer, Sonnet, effort xhigh:** reads the claims and the rendered note, writes findings to a JSON file. Doesn't edit
4. **Fixer, Opus, effort xhigh:** edits the layout, renders, verifies, logs findings in `holistic-alpha/logs/topics/findings/<run>.jsonl`

Give each agent a short prompt that points at a brief file, and keep the briefs in `holistic-alpha/logs/topics/prompts/`. Orchestrate from a short session: in stages 0 and 1, orchestration from a long session cost 15 of 46 cu.

## Criteria, fixed before running

- `verify` passes with no ERROR
- Count the merges: lines with claims from 2 or more episodes. **If there are 3 or fewer, stop and diagnose before stage 2**: is it the topic, the claims' wording, or the rules of 4.3?
- The reviewer looks for false merges (claims of different strength or scope on one line), missed merges, Later view (marked `later`, in date order, nothing dropped) and the pointers of `## In other notes`

## The report

Write `holistic-alpha/logs/runs/<date>-pilot-B-test.md`, in English, with:
- Cost: writer, reviewer, fixer, orchestration. Cost per topic and per claim
- Lines, merges, nested lines, later views, misplaced claims, pointers. The `verify` output
- Reviewer findings by severity and kind, with verdicts
- A comparison with the v1 note: `git show claude/topic-notes-v1-test:holistic-alpha/topics/sex-energy/semen-retention.md` (v1 had 0 merges in 24 Recaps)
- **A projection of the whole vault's cost**: Recaps, step A and step B for the 809 episodes. Then which of these lowers it most, with numbers:
  - review by sample instead of every Recap
  - orchestration from short sessions
  - the Recap writer also writes the claims, so step A needs no second reading

Numbers to start from, measured on 2026-10-28 and 2026-10-30:
- A Recap: about 2.5 cu with the spot-check (1.9 without). 57 of 809 done
- Step A with Opus, one pass of write, review and fix: about 0.06 cu per Recap bullet. The writer alone: about 0.035. The 57 Recaps average 20.6 bullets
- Orchestration: 15 of 46 cu in stages 0 and 1, from a long session
- Step B: this run gives the first number

Then commit to the branch with the report and `STATUS.md` updated, push, and tell Esteban the result: merges, cost, and whether stage 2 can start.

## Already settled

- Opus writes step A. It beat Sonnet in a blind review
- **Merging two topics**, for example `+discipline` into `every-day`, is only a change of slug that a script makes: `python3 -I tools/claims.py merge +discipline every-day`. It needs no agent and no new reading. Tested on a copy of the registry on 2026-10-30: 38 claims and 9 pointers moved, 47 rows changed only in `topic`, `also`, `name` and `area`, `check` OK on all 14. The note of the merged topic is then rendered again from its layout, and step B places the incoming claims. The topic list is decided after stage 2, with all the proposals in front of Esteban
- Later view labels and markers are format, written by the script
