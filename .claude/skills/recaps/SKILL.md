---
name: recaps
description: Turn Holistic Alpha transcripts into Recaps in the wisdom repo, end to end - rebuild episodes.csv, plan the blocks, run the recap-writeups workflow (Opus writer, Sonnet reviewer, Opus fixer, Opus spot-check, all at xhigh effort), check and report. Use when the user says /recaps <range>, "process episodes X-Y", "the next batch" or "the new episode".
---

# /recaps <range>

Calibrated on 2026-10-28 (see Calibration).
Without a workflow tool, as in a claude.ai cloud session, run section 3 by hand: one agent per step and block, with the prompts, model and effort that `recap-writeups.js` sets.
Reply to the user in Spanish. Recaps, logs and the instructions stay in English.
What a Recap must be is in the Recap instructions, `holistic-alpha/recap-instructions.md`. This skill only runs the pipeline.

## 0. Scope
- Parse the range: `801-813`, `537`, `404b1`, `especial-2024-12-25`, `next` (the next run, in order), `all`.
- The user decides which episodes get processed. Don't widen the range.
- Cost matters. The scripts are free, agents use the plan. When the plan's estimate is over one 5-hour window (about 50 cu, the unit of `tools/usage_report.py`), give the estimate and ask once before launching.
- Run every command from the repo root. Python is standard library only: `python3 -I` (on Windows, `py -3 -I`).

## 1. Episodes table (free)
Only when a transcript was added or `holistic-alpha/INVENTARIO.csv` changed:
```
python3 -I tools/build_episodes.py --inventory holistic-alpha/INVENTARIO.csv --transcripts holistic-alpha/transcripts/ --out holistic-alpha/episodes.csv --report holistic-alpha/logs/episodes-report.md
```
- Read the report's totals. Look at the new rows: type, guest, series, date.
- A wrong guess (a guest, a series, a type) is fixed in the script (`KNOWN_GUESTS` and its rules), never by hand in the CSV.

## 2. Plan (free)
```
python3 -I tools/plan_blocks.py --episodes holistic-alpha/episodes.csv --recaps holistic-alpha/recaps/ --ids <range> --budget 45 --out holistic-alpha/logs/plan-<date>.json
```
- It skips episodes without a transcript, and episodes that already have a Recap. `--overwrite` only when the user asks.
- Blocks: up to 8 episodes and 30,000 transcript words. An episode over 12,000 words goes alone.
- Each block names its spot-check episodes. The plan also lists the QA sample (`qa`) and estimates the cost.
- One 5-hour window: `--budget 45 --chains 1`, about 2 blocks of 8 episodes. Keep about 5 cu for the run's own orchestration.
- Episodes are independent, so `--chains 2` to `4` run blocks in parallel. They finish sooner but spend the window just as fast: on 2026-10-28, 11 agents in parallel and the main session spent a whole window in about 30 minutes.
- Default order: newest first.

## 3. Write, review, fix, spot-check (AI)
Run the saved workflow **`recap-writeups`**, with the plan JSON as its args, unchanged.
Every step runs at **xhigh** effort, set in the workflow. The calibration ran at xhigh, so its quality and cost hold only at xhigh. By hand, pass `effort: "xhigh"` to each agent: without it, an agent takes the effort of the session that launches it.
In each block:
1. An Opus writer reads each transcript once, writes its Recap under the instructions and runs `check_recaps.py`.
2. A Sonnet reviewer follows the checklist of the instructions (checker items, recall walk, fidelity, format) and returns findings with a severity.
3. An Opus fixer checks each finding against the transcript, fixes the real ones and logs every finding in `holistic-alpha/logs/findings/<block>.jsonl`.
4. An Opus spot-check reviews the block's riskiest episode again: every interview and group, otherwise the longest, and every third block another one. One S1 or two S2 escalate the block to a full Opus review and a fix.

Options, only when needed:
- `mode: "review"`: review, fix and spot-check existing Recaps (after a change to the instructions, or a block that came back `reviewed: false`).
- `mode: "audit"`: findings only, no edits (calibration).
- `reviewerModel`: `sonnet`, from the calibration.
- `writerEffort` (writer and fixer), `reviewerEffort`, `spotEffort`: `xhigh`, from the calibration. Change one only after rerunning the calibration at the new level.

## 4. After the run (free)
1. Run the checker on the run's ids. Expect no ERROR:
   `python3 -I tools/check_recaps.py --recaps holistic-alpha/recaps/ --transcripts holistic-alpha/transcripts/ --episodes holistic-alpha/episodes.csv --only <ids> --no-look --out holistic-alpha/logs/checker/run-<date>.md`
2. Blocks with `reviewed: false`: rerun them with `mode: "review"`.
3. Measure the cost: `python3 -I tools/usage_report.py <session log folder>/subagents/ --since <run start, UTC>`. Claude Code keeps the logs in `~/.claude/projects/<repo folder>/`. Compare it with the plan's estimate.
4. Read the run's findings logs. Count them by severity and kind, and note what the spot-checks still found.
5. Offer one commit per run, for example `recaps 816-801 (instructions v2)`. Commit only when the user says yes.

## 5. Report (in Spanish)
- Recaps written, skipped and pending.
- First review: S1, S2 and S3 found, fixed and rejected.
- Spot-checks: S1 and S2 still found. Blocks escalated.
- The checker result.
- The QA list for Esteban: the plan's `qa` ids, plus the spot-checked episodes of every escalated block, as links to the Recaps. He reads each Recap alone and flags anything that sounds wrong, odd or missing. Check each flag against the transcript and log it with `"reviewer": "esteban"`.
- Cost in cu, against the plan's estimate.
- Anything pending.

## Calibration (done 2026-10-28)
The results are in `holistic-alpha/logs/calibration/`. Every step ran at xhigh effort. Rerun a step only for new instructions, a new model or a new effort level.
1. **Reviewer.** Sonnet and Opus each reviewed the 10 pilot Recaps (instructions v1, kept in `holistic-alpha/golden/pilots-v1/`) in audit mode, with a blind copy of the instructions (`instructions-blind.md`), because instructions v2 quote 13 of the 15 pilot S2 as examples.
   - Score: `python3 -I tools/score_review.py --key holistic-alpha/golden/answer-key.jsonl --review <result.json>`. Check its "not in the key" list by hand: some are real findings the audit missed. Add them to the key.
   - Result: Sonnet found 19 of the 19 S2 and 54 of the 75 findings, Opus 17 S2 and 56. Sonnet stays the reviewer.
   - Rule for a rerun: Sonnet finds 80% or more of the S2, keep Sonnet. 50 to 80%: Opus reviews interviews, groups and episodes over 8,000 words. Under 50%: Opus reviews everything.
2. **Golden set.** The 10 pilots, fixed with the answer key and migrated to instructions v2, are in `holistic-alpha/golden/recaps/` and, as production Recaps, in `holistic-alpha/recaps/`.
3. **Calibration run.** 14 episodes of every type: `--ids 079 088 150 175 252 350 404b1 549 556 565 675 720 812 815 --order oldest`, in 3 blocks.
   - Cost 33.3 cu: writer 1.1 cu per episode, reviewer 0.4, fixer 0.4, spot-check and its fix 3.4 per spot episode. These are the defaults of `plan_blocks.py`. A block of 8 took about 30 minutes.
   - The first review left work for the spot-checks: 549 had 13 S3, 565 one S2 and 12 S3. No block escalated.
   - The v2 Recaps run longer than the pilots: 32 to 40% of the transcript, against 20 to 28%.
   - Esteban read 079, 175, 252, 565 and 675 and flagged nothing. They joined the golden set, now 15 Recaps.

## Changes to the instructions
- Every change gets a changelog line in the instructions and a new `instructions:` value (v2.1).
- Before a production run under new instructions, rerun the golden set into a test folder (`--out-dir holistic-alpha/golden/rerun-<date> --overwrite`) and compare it with `holistic-alpha/golden/recaps/`.
- Existing Recaps: a format change goes through a script or `mode: "review"`, never a full rewrite. A content rule goes through `mode: "review"` on the Recaps it touches (find them with the findings logs or a search). `overwrite: true` only for an S1-class problem that is widespread.
