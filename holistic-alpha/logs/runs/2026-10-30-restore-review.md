# Run 2026-10-30: restore 19 Recaps and review the pilots

Steps 1 and 2 of the topic test set plan, approved by Esteban on 2026-10-30.

## Step 1: restore

- 19 Recaps (instructions v2) restored from commit `dd2aaa6`: 079 088 127 150 175 252 275 350 404b1 537 549 556 565 663 675 720 812 813 815
- Findings logs restored with them: `findings/079-556.jsonl`, `findings/175.jsonl`, `findings/565-815.jsonl`
- Checker (`checker/restore-2026-10-30.md`): 0 ERROR, 5 WARN for length (556 565 675 720 812, 36-40%)
- Cost: 0 cu, a script copy

## Step 2: review of the 5 pilots

The pilots 127 275 537 663 813 were written before the v2 checklist was final.
They got a review against it, no rewrite.

- Plan: `plan-2026-10-30-review.json`, mode `review`, no spot-check, 2 blocks (127-663 and 813)
- Sonnet reviewed, Opus fixed, effort xhigh
- Findings: 33. 4 S2 and 29 S3, no S1. Fixed 31, rejected 2
  - `findings/127-663.jsonl`: 3 S2 and 20 S3 fixed, 1 S3 rejected
  - `findings/813.jsonl`: 1 S2 and 7 S3 fixed, 1 S3 rejected
- Checker after the fix (`checker/review-2026-10-30.md`): 0 ERROR, 0 WARN
- Cost: 6.27 cu. Estimate was 4.0 cu
