---
name: recaps
description: Turn Holistic Alpha transcripts into Recaps in the wisdom repo, end to end - rebuild episodes.csv, plan the blocks, run the recap-writeups workflow (Opus writer, Sonnet reviewer, Opus fixer, Opus spot-check), check and report. Use when the user says /recaps <range>, "process episodes X-Y", "the next batch" or "the new episode".
---

# /recaps <range>

DRAFT of 2026-10-28, not run yet. The first run is the calibration below.
Reply to the user in Spanish. Recaps, logs and the recipe stay in English.
What a Recap must be is in `holistic-alpha/recap-recipe.md`. This skill only runs the pipeline.

## 0. Scope
- Parse the range: `801-813`, `537`, `404b1`, `especial-2024-12-25`, `next` (the next run, in order), `all`.
- The user decides which episodes get processed. Don't widen the range.
- Cost matters. The scripts are free, agents use the plan. When the plan's estimate is over one 5-hour window (about 1.2M tokens on Pro), give the estimate and ask once before launching.
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
python3 -I tools/plan_blocks.py --episodes holistic-alpha/episodes.csv --recaps holistic-alpha/recaps/ --ids <range> --budget 1100000 --out holistic-alpha/logs/plan-<date>.json
```
- It skips episodes without a transcript, and episodes that already have a Recap. `--overwrite` only when the user asks.
- Blocks: up to 8 episodes and 30,000 transcript words. An episode over 12,000 words goes alone.
- Each block names its spot-check episodes. The plan also lists the QA sample (`qa`) and estimates the tokens.
- Pro plan: `--budget 1100000 --chains 1`, about 2 blocks per 5-hour window. Max plan: a larger budget and `--chains 2` to `4`. Episodes are independent, so chains can run in parallel.
- Default order: newest first.

## 3. Write, review, fix, spot-check (AI)
Run the saved workflow **`recap-writeups`**, with the plan JSON as its args, unchanged. In each block:
1. An Opus writer reads each transcript once, writes its Recap under the recipe and runs `check_recaps.py`.
2. A Sonnet reviewer follows the recipe's checklist (checker items, recall walk, fidelity, format) and returns findings with a severity.
3. An Opus fixer checks each finding against the transcript, fixes the real ones and logs every finding in `holistic-alpha/logs/findings/<block>.jsonl`.
4. An Opus spot-check reviews the block's riskiest episode again: every interview and group, otherwise the longest, and every third block another one. One S1 or two S2 escalate the block to a full Opus review and a fix.

Options, only when needed:
- `mode: "review"`: review, fix and spot-check existing Recaps (after a recipe change, or a block that came back `reviewed: false`).
- `mode: "audit"`: findings only, no edits (calibration).
- `reviewerModel`: set by the calibration.

## 4. After the run (free)
1. Run the checker on the run's ids. Expect no ERROR:
   `python3 -I tools/check_recaps.py --recaps holistic-alpha/recaps/ --transcripts holistic-alpha/transcripts/ --episodes holistic-alpha/episodes.csv --only <ids> --no-look --out holistic-alpha/logs/checker/run-<date>.md`
2. Blocks with `reviewed: false`: rerun them with `mode: "review"`.
3. Read the run's findings logs. Count them by severity and kind, and note what the spot-checks still found.
4. Offer one commit per run, for example `recaps 816-801 (recipe v2)`. Commit only when the user says yes.

## 5. Report (in Spanish)
- Recaps written, skipped and pending.
- First review: S1, S2 and S3 found, fixed and rejected.
- Spot-checks: S1 and S2 still found. Blocks escalated.
- The checker result.
- The QA list for Esteban: the plan's `qa` ids, plus the spot-checked episodes of every escalated block, as links to the Recaps. He reads each Recap alone and flags anything that sounds wrong, odd or missing. Check each flag against the transcript and log it with `"reviewer": "esteban"`.
- Approximate tokens, against the plan's estimate.
- Anything pending.

## Calibration (once, before the first production run)
1. **Score the reviewer.** Copy the original pilot Recaps (recipe v1) to `holistic-alpha/golden/pilots-v1/`. The answer key `holistic-alpha/golden/answer-key.jsonl` lists their 71 known findings (15 S2, 56 S3) from the October 2026 audit.
   - Plan: `plan_blocks.py ... --ids 001-005 127 275 537 663 813 --mode audit --recaps holistic-alpha/golden/pilots-v1/ --out-dir holistic-alpha/golden/pilots-v1`.
   - Run the workflow twice, with `reviewerModel: "sonnet"` and `"opus"`. Save each result to `holistic-alpha/logs/calibration/`.
   - Score each: `python3 -I tools/score_review.py --key holistic-alpha/golden/answer-key.jsonl --review <result.json>`. Check its "not in the key" list by hand: some are real findings the audit missed.
   - Sonnet finds 12 or more of the 15 S2: keep Sonnet. 8 to 11: Opus reviews interviews, groups and episodes over 8,000 words. Under 8: Opus reviews everything.
2. **Golden set.** One Opus agent applies the answer key's findings to copies of the pilots in `holistic-alpha/golden/recaps/`, following the fixer rules, and migrates them to recipe v2. Copy them to `holistic-alpha/recaps/` as the production Recaps of those 10 episodes.
3. **Calibration run.** One run in write mode on 14 episodes of every type: `--ids 079 088 150 175 252 350 404b1 549 556 565 675 720 812 815 --order oldest`, about 1.3M tokens.
   - Measure tokens and minutes per block. Put the numbers into `plan_blocks.py` (`--tokens-per-word`, `--block-tokens`).
   - Esteban reads 079, 175, 252, 565 and 675. Once fixed, they join the golden set.

## Recipe changes
- Every change gets a changelog line in the recipe and a new `recipe:` value (v2.1).
- Before a production run under a new recipe, rerun the golden set into a test folder (`--out-dir holistic-alpha/golden/rerun-<date> --overwrite`) and compare it with `holistic-alpha/golden/recaps/`.
- Existing Recaps: a format change goes through a script or `mode: "review"`, never a full rewrite. A content rule goes through `mode: "review"` on the Recaps it touches (find them with the findings logs or a search). `overwrite: true` only for an S1-class problem that is widespread.
