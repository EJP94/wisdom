export const meta = {
  name: 'recap-writeups',
  description: 'Write, review and fix Holistic Alpha episode Recaps in blocks: an Opus writer, a Sonnet reviewer and an Opus fixer per block, then an Opus spot-check that escalates the block when it still finds serious slips',
  whenToUse: 'After tools/plan_blocks.py has written the run plan. args: that plan JSON { repo, date, python, mode, overwrite, outDir, header, chains: [[{ label, ids, spot, rows }]] }, plus optional writerModel, reviewerModel, spotModel, spotCheck, escalateS2',
  phases: [
    { title: 'Write', detail: 'one writer reads each transcript once, writes its Recap under the recipe and runs check_recaps.py', model: 'opus' },
    { title: 'Review', detail: 'one reviewer checks the block with the recipe checklist: checker items, recall walk, fidelity, format', model: 'sonnet' },
    { title: 'Fix', detail: 'one agent verifies the findings, fixes the real ones and logs every finding', model: 'opus' },
    { title: 'Spot-check', detail: 'a second reviewer checks the riskiest episodes of the block after the fix, and escalates to a full review when it finds an S1 or two S2', model: 'opus' },
  ],
}

// 2026-10-28. Adapted from the One Piece chapter-writeups workflow. The calibration ran its steps by
// hand, one agent per step (no workflow tool in the cloud session). The workflow itself has not run
// yet. Episodes are independent, so chains can run in parallel.
//
// Modes:
//   write   (default) write -> review -> fix -> spot-check. Skips episodes that have a Recap unless overwrite.
//   review  review -> fix -> spot-check on existing Recaps (after a recipe change, or to finish an unreviewed block).
//   audit   review only, no edits; returns every finding (calibration: score it with tools/score_review.py).
// args (from tools/plan_blocks.py, which reads episodes.csv: this script cannot read files):
//   repo          absolute path of the wisdom repo
//   date          run date, for the findings log
//   python        "python3", or "py -3" on Windows
//   chains        array of chains; each chain is an array of blocks { label, ids, spot, rows }
//   header        episodes.csv header line; each block's rows are its episodes' CSV lines
//   overwrite     true = rewrite existing Recaps from scratch (after a recipe change). Default false.
//   outDir        optional test folder for the Recaps, relative to the repo. Absent = holistic-alpha/recaps.
//   writerModel 'opus', reviewerModel 'sonnet', spotModel 'opus'. Sonnet won the reviewer calibration.
//   spotCheck     default true (ignored in audit mode)
//   escalateS2    S2 findings in the spot-check that trigger a full Opus review of the block. Default 2.
const A = args || {}
if (!A.repo) throw new Error('args.repo is required: pass the JSON written by tools/plan_blocks.py')
const chains = A.chains || []
if (!chains.length) throw new Error('args.chains is required')
const mode = A.mode || 'write'
if (!['write', 'review', 'audit'].includes(mode)) throw new Error(`unknown mode ${mode}`)
const writerModel = A.writerModel || 'opus'
const reviewerModel = A.reviewerModel || 'sonnet'
const spotModel = A.spotModel || 'opus'
const spotCheck = A.spotCheck !== false && mode !== 'audit'
const escalateS2 = A.escalateS2 || 2
const PY = A.python || 'python3'
const DATE = A.date || new Date().toISOString().slice(0, 10)
const RECAPS = A.outDir || 'holistic-alpha/recaps'

const list = ids => ids.join(', ')
const SOURCES = `Repo root: \`${A.repo}\`. Run every command from there. The rules are in \`holistic-alpha/recap-recipe.md\`. Each transcript is \`holistic-alpha/transcripts/<stem>.txt\` and each Recap is \`${RECAPS}/<stem>.md\`, where <stem> is the \`stem\` column of the episode's row in \`holistic-alpha/episodes.csv\`. Never edit a transcript, \`episodes.csv\` or the recipe.`
const rowsOf = (b, ids) => {
  const keep = b.rows.filter(r => ids.some(id => r.startsWith(id + ',')))
  return `Their rows from \`holistic-alpha/episodes.csv\`:\n${A.header}\n${keep.join('\n')}`
}
const check = (ids, tag) => `\`${PY} -I tools/check_recaps.py --recaps "${RECAPS}/" --transcripts holistic-alpha/transcripts/ --episodes holistic-alpha/episodes.csv --only ${ids.join(' ')} --out holistic-alpha/logs/checker/${tag}.md\``
const overwrite = A.overwrite
  ? 'Some of these episodes may already have a Recap written under older rules. Do NOT edit it: rewrite it from scratch under the current recipe, overwriting the file.'
  : 'If an episode already has a Recap, skip it and say so in your reply.'

const KINDS = ['idea missing', 'advice hedge lost', 'scope widened', 'source lost', 'certainty hedge lost', 'hedge added',
  'word added', 'quote spliced', 'quote altered', 'number wrong', 'speaker wrong', 'fact changed', 'format']
const FINDING = {
  type: 'object',
  properties: {
    severity: { type: 'string', enum: ['S1', 'S2', 'S3'] },
    kind: { type: 'string', enum: KINDS },
    ts: { type: 'string', description: 'the transcript line [mm:ss] where the source passage starts, or "" for a format finding' },
    transcript: { type: 'string', description: "the transcript's exact words" },
    recap: { type: 'string', description: "the Recap's words, or \"\" when the idea has no bullet" },
    fix: { type: 'string', description: 'the smallest edit that fixes it' },
  },
  required: ['severity', 'kind', 'ts', 'transcript', 'recap', 'fix'],
}
const REVIEW = {
  type: 'object',
  properties: {
    episodes: {
      type: 'array',
      items: {
        type: 'object',
        properties: {
          id: { type: 'string' },
          ok: { type: 'boolean', description: 'true only when there is no finding' },
          findings: { type: 'array', items: FINDING },
        },
        required: ['id', 'ok', 'findings'],
      },
    },
  },
  required: ['episodes'],
}

const count = (entries, sev) => entries.reduce((n, e) => n + (e.findings || []).filter(f => f.severity === sev).length, 0)
const tally = entries => ({ S1: count(entries, 'S1'), S2: count(entries, 'S2'), S3: count(entries, 'S3') })

function reviewPrompt(b, ids, tag, second) {
  const intro = second
    ? `You are the second reviewer of the Holistic Alpha Recaps of episodes ${list(ids)}. A first reviewer from another model checked them and a fixer corrected what it found. Find what both missed.`
    : `Review the Holistic Alpha Recaps of episodes ${list(ids)} against their transcripts.`
  return `${intro}
${SOURCES}
${rowsOf(b, ids)}
Read the recipe first, then follow its reviewer checklist (section 14) for each episode, in full:
0. Checker items. Run ${check(ids, tag)} and read the report. Verify each WARN and LOOK against the transcript and report the real ones. A LOOK is a candidate, often a false alarm.
1. Recall. Walk the transcript in order, about two minutes at a time, and find the bullet that carries each stretch's ideas. Report every idea with no bullet. In the pilot, one review reported no missing idea in five episodes where an audit later found 14: walk every stretch, don't skim.
2. Fidelity. For each bullet, find its source passage and compare: hedges of all four kinds ("I would suggest" turned into an order, "some of" or "most times" dropped, "guys I've worked with" turned into "many men"), hedges added, the sources he cites, watch-list words, every number, every quote (one unbroken run of the transcript) and, in interviews and groups, who says what, line by line.
3. Format: TL;DR, markers, frontmatter type and guest, the line under the TL;DR.
Use the severity scale and the kinds of section 14. Give each finding the transcript's [mm:ss] and its exact words. Report a finding when you are unsure: the fixer checks each one against the transcript. Don't report style preferences or wording that keeps the meaning. Don't edit any file. Return one entry per episode.`
}

function fixPrompt(b, entries, who, tag) {
  const ids = entries.map(e => e.id)
  return `Fix the Holistic Alpha Recaps of episodes ${list(ids)}.
${SOURCES}
A reviewer (${who}) reported the findings below. Follow the fixer rules of the recipe (section 15): check each finding against the transcript, fix it only if it is real, with the smallest edit that follows the recipe, and reject false alarms. Fix every real S1 and S2, and an S3 when the edit is small. Missing content is real whenever the transcript holds it. If you change a bullet, check that the TL;DR still matches it.
${JSON.stringify(entries, null, 1)}
Log every finding, fixed or rejected, as one JSON line appended to \`holistic-alpha/logs/findings/${b.label}.jsonl\` (create the folder if needed), with "date": "${DATE}", "recipe" from the Recap's frontmatter, "block": "${b.label}", "reviewer": "${who}", "verdict": "fixed" or "rejected", and the other fields of section 15.
Afterwards run ${check(b.ids, tag)} and make sure no ERROR remains. Reply with one line per episode: "<id>: fixed <n>, rejected <n>".`
}

async function runBlock(b) {
  const label = b.label
  if (mode === 'write') {
    await agent(
      `Write the Holistic Alpha Recaps of episodes ${list(b.ids)}, one episode at a time, in this order.
${SOURCES}
${rowsOf(b, b.ids)}
Read the recipe once, in full, and follow it exactly. Its core: every idea kept (compress, never drop one), only what the episode says, the message without the messenger (his name only in the frontmatter and in the line under the TL;DR), every hedge kept in his own words, the sources he cites named, quotes copied as one unbroken run of the transcript.
${overwrite}
For each episode:
1. Take its frontmatter from its row (recipe section 11). Confirm the type from the transcript (section 9).
2. Read the whole transcript once. Write the bullets, then the TL;DR, then the line under it.
3. Run the recipe's self-check (section 13).
Write UTF-8 with LF line endings. Modify no other file.
When the block is done, run ${check(b.ids, label + '-write')}. Fix every ERROR. Read every WARN and LOOK against the transcript and fix the real ones. Run it again until no ERROR remains. Reply with just "done", plus one line for each episode you skipped or whose type you changed.`,
      { label: `write ${label}`, phase: 'Write', model: writerModel })
  }

  const review = await agent(reviewPrompt(b, b.ids, label + '-review', false),
    { label: `review ${label}`, phase: 'Review', model: reviewerModel, schema: REVIEW })
  const entries = (review && review.episodes) || []
  if (!review) {
    log(`block ${label}: review failed, so the Recaps are unreviewed. Rerun this block in review mode.`)
    return { label, ids: b.ids, mode, reviewed: false }
  }
  const first = tally(entries)
  if (mode === 'audit') {
    log(`block ${label}: audit only, ${first.S1} S1, ${first.S2} S2, ${first.S3} S3`)
    return { label, ids: b.ids, mode, reviewed: true, findings: first, review: entries }
  }

  const bad = entries.filter(e => !e.ok && (e.findings || []).length)
  if (bad.length) {
    await agent(fixPrompt(b, bad, reviewerModel, label + '-fix'), { label: `fix ${label}`, phase: 'Fix', model: writerModel })
  }

  let spot = null
  let escalated = false
  if (spotCheck && (b.spot || []).length) {
    const s = await agent(reviewPrompt(b, b.spot, label + '-spot', true),
      { label: `spot ${label}`, phase: 'Spot-check', model: spotModel, schema: REVIEW })
    const sEntries = (s && s.episodes) || []
    spot = { ids: b.spot, ...tally(sEntries) }
    let toFix = sEntries.filter(e => (e.findings || []).length)
    escalated = spot.S1 > 0 || spot.S2 >= escalateS2
    if (escalated) {
      const rest = b.ids.filter(id => !b.spot.includes(id))
      if (rest.length) {
        const x = await agent(reviewPrompt(b, rest, label + '-escalation', true),
          { label: `escalation ${label}`, phase: 'Spot-check', model: spotModel, schema: REVIEW })
        toFix = toFix.concat(((x && x.episodes) || []).filter(e => (e.findings || []).length))
      }
    }
    if (toFix.length) {
      await agent(fixPrompt(b, toFix, escalated ? `${spotModel} escalation` : `${spotModel} spot-check`, label + '-final'),
        { label: `fix ${label} after spot-check`, phase: 'Spot-check', model: writerModel })
    }
  }

  log(`block ${label}: ${entries.length - bad.length} of ${entries.length} OK at first review ` +
    `(${first.S1} S1, ${first.S2} S2, ${first.S3} S3)` +
    (spot ? `, spot-check ${spot.ids.join(' ')}: ${spot.S1} S1, ${spot.S2} S2, ${spot.S3} S3` : '') +
    (escalated ? ', ESCALATED to a full Opus review' : ''))
  return { label, ids: b.ids, mode, reviewed: true, firstPassOk: entries.filter(e => e.ok).map(e => e.id), findings: first, spot, escalated }
}

async function runChain(chain) {
  const out = []
  for (const b of chain) out.push(await runBlock(b))
  return out
}

const results = await parallel(chains.map(c => () => runChain(c)))
return { mode, writerModel, reviewerModel, spotModel, date: DATE, results: results.filter(Boolean).flat() }
