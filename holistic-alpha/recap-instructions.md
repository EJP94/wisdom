# Recap instructions v2

## Rename (2026-10-28)

This file was called the recipe (`recap-recipe.md`). The frontmatter field `recipe` is now `instructions`, in every Recap and findings log. No rule changed, so the version stays v2.

## Changelog v1 → v2 (2026-10-28)

Every change comes from the audit of the 10 pilot Recaps (`auditoria.md`). Timestamps point to the transcripts.

1. **Attribution line reworded, and sources he cites are named in the bullet.** v1 said "Every idea and story below is Steven Mathis's", which is false when he reads Emerson (079), repeats a saying ("they say that hormones affect everything", 001 [05:29]), uses a term "as some people call it" (002 [08:39]), credits Joe Dispenza (537 [60:42]) or reads a listener's question (675).
2. **Hedges sorted into four kinds, with real failures as examples.** 9 of the 15 serious findings (S2) were a lost hedge, scope or source: "I would suggest" became an order (663 [05:47], 275 [06:40], [22:24], [35:25]), "some of the Kegel apps" became "Kegel apps" (813 [00:00]), "every time I can remember" became "every time" (537 [37:30], the very example v1 gave).
3. **Do not add hedges either.** Two Recaps softened a flat claim ("may be the two most powerful tools", 537 [44:52]; "it seems limitless", 537 [48:24]).
4. **Keep the source of his experience.** "So many guys that I've worked with" became "many men" (663 [11:02]). "I can't recall talking to a guy who..." became "seems almost unheard of" (275 [20:16]).
5. **Quotes defined as one unbroken run of the transcript.** Two quotes were spliced (127 [02:11], 537 [31:42]) and three were altered (127 [11:48], 537 [26:22], [28:25]). The checker now verifies every quote.
6. **A watch list of words the writer must not add.** "Stranger" (127 [01:26], a word v1 itself banned), "coach" (537 [19:09]), "beginners" (004, 005), "often" (813 [14:31]), "every" (537 [22:24]), "nobody" (275 [48:56]).
7. **Output file = transcript file name + `.md`.** v1 said `NNN - <original title>.md`, but titles hold `/`, `:`, `?` and `*` ("80/20", "C*ck"). The pilots already used the transcript's name.
8. **`episodes.csv` replaces `INVENTARIO.csv`.** The inventory has 8 titles broken by quotes, 18 rows without a date, a row with two files (404 and 404b1) and three unnumbered specials. `tools/build_episodes.py` fixes all of that for free.
9. **Frontmatter v2:** `id`, `type`, `words`, `minutes`, `instructions`, plus `series`/`part`, `replays` and `date_estimated` when they apply. The guest gets his full name (537 had only "Dustin"). The script fills every field. No topics or timestamps yet: later views can add them for free or cheaply.
10. **Eight episode types with their own rules:** solo, interview, group, qa, guided, challenge, compilation, promo. 175 replays five earlier episodes (90 to 97% identical text). The 2024-12-25 special is 142 words of promotion. 079 is 141 words. 252 is a guided exercise. 565 has four voices.
11. **New markers:** `**Listener question:**`, `**Listener story:**`, `**Quote:**`, `**Guided practice:**`.
12. **TL;DR: one sentence, at most 45 words.** 537 had 70 words, 275 had 58, and 005 had two sentences.
13. **Tense:** ideas in the present, stories in the past. v1 asked for present tense everywhere, yet every pilot told its stories in the past, which reads better.
14. **A glossary** of mishearings and of his own terms, so the same thing is spelled the same way in 809 Recaps.
15. **The process is part of the instructions:** the writer runs the checker, the reviewer follows a three-pass checklist with a severity scale, and the fixer logs every finding. In the pilot, one review pass reported no missing idea in 127–813. The audit found 14 there, and 15 serious drifts had survived.
16. **No length target** for episodes under 700 words, promos and compilations.

Unchanged and working well: one Recap per episode, every idea kept, the message without the messenger, **Story:** markers, the interview markers, quantities, specifics, cutting calls to action, bullets in order of first appearance, at most one bold term per bullet.

---

The vault replaces the transcripts. A **Recap** lets the reader get **every idea** of an episode in one quick read. It compresses the talk. **It never drops an idea.** Reading only the Recap, nobody should think an idea, a practice or a story was missing from the episode.

## 1. Input and output

- Input: one transcript, `holistic-alpha/transcripts/<stem>.txt` (format `[mm:ss] text`, one line per 20–40 seconds, no speaker labels), and its row in `holistic-alpha/episodes.csv`.
- Output: `holistic-alpha/recaps/<stem>.md`, where `<stem>` is the transcript's file name without `.txt`. Never rebuild the name from the title.
- Build the Recap from the transcript, in one pass. Never from another summary: a summary of a summary compounds errors.
- A compilation is the one exception that looks at other episodes: see section 9.

## 2. What counts as an idea

Each of these gets a bullet, or shares one with a closely related idea:
- A claim or belief: what the episode holds to be true
- Advice or a rule: "avoid fragrance", "make it every day"
- A practice: what to do, how, how much, how often
- A number, dose, study, book or person he cites
- A personal story or example
- A framework or definition: "80/20", "resistance", "the three dials"
- Anything else a listener could act on, repeat or disagree with

## 3. What to cut

- The intro, the outro, greetings and the recording day
- Calls to action: book a call, coaching offers, Inner Circle or Brotherhood invitations, Instagram, the phone number, links, "share this", "leave a comment"
- Repetition. When he comes back to an idea, merge it into the bullet where it first appeared, adding only what is new
- Filler, hesitations and false starts
- The closing recap of the episode, unless it adds something new

Keep a call to action only when it is part of an idea or a story ("he joined Inner Circle, the private membership community, and that week changed things"). A promo episode follows section 9.

## 4. Hard rules

### 4.1 Only what the episode says
No outside knowledge, no fact-checking, no interpretation. A critical reading belongs elsewhere, not here.

### 4.2 The message, not the messenger
The whole note is his view, and the line under the TL;DR says so. Write the ideas directly, as statements or instructions, with no "Steven says", "he thinks" or "he describes". His name never appears in the body. His personal stories start with **Story:** and are told without a subject ("a first try at 1,000 push-ups a day"). In interviews, see section 8.

### 4.3 Name the sources he cites
When he credits an idea to someone else, the bullet says so, the way he did. Keep his hedge on the credit.
- A saying: ✗ `"hormones affect everything and everything affects your hormones"` ✓ `As the saying goes, "hormones affect everything and everything affects your hormones", and it holds:` (001 [05:29])
- A term others use: ✗ `life energy, or "qi"` ✓ `life energy, or "qi", as some people call it` (002 [08:39])
- A person: ✓ `"Change your energy, you change your life", a phrasing probably from Joe Dispenza` (537 [60:42])
- A study, doctors, a book, a client, a listener: ✓ `one study`, `doctors talk about it`, `a client`, `a listener asks`
- A reading: use **Quote:** with the author (section 7)

### 4.4 Keep his hedges, in words
Never make a claim stronger than he made it. Without his name, first-person lines turn universal by accident. Watch four kinds of hedge.

**Advice hedges.** Write advice as a plain instruction only when he gave it plainly.

| He said | ✗ Written | ✓ Write |
|---|---|---|
| "I would suggest that you practice pausing before you take any action" (663 [05:47]) | How to practice: pause before any action | Suggested practice: pause before any action |
| "what you may want to do is you may even want to stop stimulating entirely" (275 [35:25]) | at first stop or ease off | at first you may want to stop, or ease off |
| "So what I would suggest is if you're new to this..." (275 [06:40]) | If you're new: stop two or three times | If you're new, a suggestion: stop two or three times |
| "Maybe you need to do a little warm to wash" (004 [02:59]) | A little warm water to wash is fine | Maybe a little warm water to wash |

**Quantity and scope hedges.** "One of", "some", "a lot of guys", "most times", "every time I can remember" stay as they are. Never "all", "members" or "nearly every".

| He said | ✗ Written | ✓ Write |
|---|---|---|
| "some of the Kegel apps that you've maybe seen advertised" (813 [00:00]) | Kegel apps advertised on social media suggest | Some Kegel apps advertised on social media suggest |
| "most times in life, it's the awkward questions ... that produce the most growth" (537 [62:37]) | The awkward questions produce the most growth | Most times in life, the awkward questions produce the most growth |
| "Every time I can remember anybody withdrawing" (537 [37:30]) | every time a man withdrew | every withdrawal that comes to mind |

**Experience hedges: keep the source of what he knows.** His coaching, what he heard, what he remembers, his own body. "For me" becomes "personally", and what he did becomes a **Story:**, never general advice.

| He said | ✗ Written | ✓ Write |
|---|---|---|
| "so many guys that I've worked with around the porn thing" (663 [11:02]) | Many men working on porn reach a stage | In coaching, many men working on porn reach a stage |
| "I don't think I can ever recall hearing about or talking to a guy who's out of balance on the push side" (275 [20:16]) | seems almost unheard of | personally, no case of a push-side imbalance comes to mind |
| "Something I've heard from a lot of guys" (813 [23:02]) | Many men get discouraged | A lot of men say they get discouraged |
| "for me, and I think for a lot of people" (004 [06:03]) | probably leave you drained | personally, and probably for a lot of people, they leave you drained |

**Certainty hedges.** "I think" becomes "seems", "may" or "probably". "Sort of", "kind of", "basically", "in essence", "not really", "my view is" stay.

| He said | ✗ Written | ✓ Write |
|---|---|---|
| "have sort of an inverse relationship" (127 [23:09]) | have an inverse relationship | have sort of an inverse relationship |
| "you're not really placing this great need on your body" (127 [29:00]) | that need is never placed | that need is not really placed |
| "there's not really a shortcut" (537 [53:41]) | There is no shortcut | There is not really a shortcut |

**Do not add hedges either.** When he says it flatly, write it flatly. ✗ `may be the two most powerful tools` for "the most powerful possible thing ... it's meditation and it's sexuality" (537 [44:52]).

### 4.5 Add nothing
Use the transcript's own nouns. Do not add a person, a group, a frequency or an absolute he didn't give. These words need his own word behind them, in that passage:
- people and groups: stranger, beginner, coach, expert, doctor, member, client, scientist, the majority
- evidence: research, science, study, studies, proven, proof, evidence
- absolutes and frequencies: only, all, every, everyone, nobody, never, always, often, usually

Examples from the pilots: "this one guy" is not "one coach" (537 [19:09]). "If you have never taken a cold shower" is not "beginners" (004). "The most random questions" is not "every awkward question" (537 [22:24]). "I've been strictly cold showers for two to three years now" has no "then" after the ice baths (004 [05:34]).

### 4.6 Quotes
Quotation marks hold his exact words, or the guest's.
- A quote is one unbroken run of the transcript. You may drop filler ("uh", "um", "you know") and fix a mishearing from the glossary. Nothing else.
- Never join two places with one pair of quotation marks. Use two quotes, or paraphrase without quotation marks.
- Never quote garbled words. Paraphrase them, or add `[?]`.
- ✗ `"I'm stuck in this job, this relationship, this habit, this weight"` (127 [02:11]: he repeats "I'm stuck in this" each time) ✓ `"I'm stuck in this job, I'm stuck in this relationship"` or a paraphrase.
- ✗ his "one pitch" (537 [28:25]: the transcript says "my my one self's pitch") ✓ `his one sales pitch [?]: get coconut oil`.

### 4.7 Keep every specific
Numbers, doses, timings, foods, products, exercises, books, names and studies stay, even when the bullet gets shorter. Write numbers as he gave them. "Four or five days" may become "4–5 days". Never compute a new number he didn't say.

### 4.8 Fix obvious transcription errors
Use the glossary (section 12). If unsure, keep the word and add `[?]`. If unsure who speaks, add `[speaker unclear]`.

### 4.9 Language and tense
English. Ideas, advice and claims in the present tense. Stories in the past tense.

### 4.10 No links
No links, URLs, wikilinks or phone numbers in the body.

## 5. Style

- **One TL;DR line, then bullets**, in the order ideas first appear in the episode.
- The TL;DR is one sentence of at most 45 words, composed last from this Recap's bullets, in their order. It need not name every bullet. It keeps the bullets' hedges.
- When the episode gives its own list ("four areas, three keys each"), keep it as one bullet with nested bullets. Otherwise, flat bullets.
- When a later part of the episode comes back to each item of that list ("how to practice each dial"), merge it into the list item. Place stand-alone ideas by where they first appear.
- Bold the one key term of a bullet only when it names a framework, a practice or a rule the episode is built on. At most one per bullet. Markers don't count.
- One idea, or one tight cluster, per bullet. Direct verbs, explicit names, no filler.
- Nested bullets use two spaces per level.

## 6. Length

No fixed target. A dense episode gets a longer Recap. **When in doubt, keep the idea.** Typical results:
- solo episodes: 25–30% of the transcript's words
- long solo episodes (over 6,000 words): 20–25%
- interviews and groups: about 20%, because they carry more filler
- under 700 words, promos and compilations: no target

The checker warns outside 18–36% (solo) and 14–30% (interviews and groups).

## 7. Markers

A marker opens the bullet, or a sentence inside it, in bold with a colon.

| Marker | Use |
|---|---|
| **Story:** | his own story or example, in a solo episode |
| **Host story:** | his own story, in an episode with a guest |
| **Guest story:** | the guest's story |
| **Guest:** | the guest's view or claim |
| **Guest advice:** | the guest's advice |
| **Guest question:** | a question the guest asks |
| **Listener question:** | a question sent by a listener, paraphrased, without the listener's name or city |
| **Listener story:** | a listener's experience he reads or retells |
| **Quote:** | words of a third party he reads (a book, a poem, a saying), with the author when he names one |
| **Guided practice:** | a guided exercise, with its steps as nested bullets |

Unmarked lines are his view.

## 8. Interviews, groups and listener questions

The transcript has no speaker labels, so read for turn changes: a short "yeah", "absolutely" or "100%" often means the other person is speaking. Questions usually come from the host.
- The line under the TL;DR names the host and the guest, and says how lines are marked (section 11).
- Unmarked lines are the host's view. The guest's lines carry a **Guest** marker. The host's own experiences start with **Host story:**.
- Names stay out of the body. "The host" is fine inside a guest's story, where he is a character.
- Groups: mark every non-host line **Guest:**. Add the first name in brackets only when the transcript names the speaker at that point: `**Guest (Rick):**`. Otherwise add `[speaker unclear]` when it matters.
- Listener questions (type `qa`, or a question inside any episode): give the question as **Listener question:**, then his answer as unmarked bullets.
- A guest's view the host disagrees with stays the guest's. Never merge the two into one unmarked line.

## 9. Episode types

`type` comes pre-filled from `episodes.csv`. Confirm it from the transcript. If the transcript clearly says otherwise, change it and say so in your reply.

| type | What it is | What changes |
|---|---|---|
| solo | he talks alone (most episodes) | nothing |
| interview | one guest | section 8. `guest` holds the full name |
| group | two or more guests | section 8. `guest` lists them, separated by `; ` |
| qa | listener questions answered | **Listener question:** then the answer |
| guided | mostly a guided practice (252) | one **Guided practice:** bullet, steps nested in order, every duration, count and cue kept. Talk before or after gets normal bullets. Don't transcribe the script |
| challenge | a day of a challenge series (550–568) | keep the day, what was done and the results as **Story:** or **Guest story:**, plus any idea |
| compilation | replays earlier episodes (175) | Recap only what is new. Add one bullet: `Replays episodes 037, 097, 099, 117 and 130, whose Recaps hold those ideas`. `replays` lists them |
| promo | an announcement, trailer or offer (the specials, 815) | one bullet saying what is announced, with no link, price, code or phone number, plus any real idea as usual. If it holds no idea, that one bullet is the Recap |

Any type can be part of a series (`series` and `part`). Each part stands alone: don't bring in ideas from other parts.

An episode under 700 words still gets a full Recap. When it is a reading, quote it in full with **Quote:** if it is under about 60 words, then add his own words as bullets. Example, 079:
```
- **Quote:** Ralph Waldo Emerson: "There is one mind common to all individual men. Every man is an inlet to the same and to all of the same."
- There is also one fire common to all men, one indomitable spirit, one unstoppable life force. You are an inlet to its full power
```

## 10. Guided practices inside other episodes

A guided exercise inside a solo episode (521) gets its own **Guided practice:** bullet at the place where it starts, with the steps nested. The talk around it follows the normal rules.

## 11. Format

```
---
id: "663"
episode: 663
title: "The Pause-Intention Bridge: Quitting Porn + Building Discipline & More"
date: 2024-08-04
type: solo
host: Steven Mathis
words: 2486
minutes: 15
instructions: v2
source: "663 - The Pause-Intention Bridge - Quitting Porn + Building Discipline & More.txt"
section: recap
---

> **TL;DR** — <one sentence, at most 45 words, composed last from this Recap's bullets, in their order>

*Ideas and stories from Holistic Alpha episode 663, as told by host Steven Mathis. Sources he credits are named where they appear. Not fact-checked.*

- <idea>
- <idea>
```

Frontmatter rules:
- Copy every value from the episode's row in `episodes.csv`. The script has already fixed titles, dates and ids.
- `id` is a quoted string ("001", "404b1", "especial-2024-12-25"). `episode` is the number, left out for the specials.
- Leave out the keys that don't apply. Optional keys, in this order after `type`:
  - `guest`: full name as in `episodes.csv`, for interview, group, and challenge days with a guest
  - `series` and `part`: multi-part series
  - `replays`: compilations, as a list of quoted ids, so YAML keeps the leading zeros: `["037", "097", "099", "117", "130"]`
  - `date_estimated: true`: when `episodes.csv` marks the date as estimated
- `title` in double quotes. Escape inner double quotes: `"\"I'm Just Getting Older\""`.

The line under the TL;DR, by type:
- Solo and every type without a guest: `*Ideas and stories from Holistic Alpha episode N, as told by host Steven Mathis. Sources he credits are named where they appear. Not fact-checked.*`
- Interview: `*From Holistic Alpha episode N, a conversation between host Steven Mathis and <full name>. Lines marked **Guest** are <first name>'s, unmarked lines are the host's. Not fact-checked.*`
- Group: `*From Holistic Alpha episode N, a conversation between host Steven Mathis and <names>. Lines marked **Guest** are the guests', unmarked lines are the host's. Not fact-checked.*`
- Specials: write `the Holistic Alpha special of YYYY-MM-DD` in place of `Holistic Alpha episode N`.

## 12. Glossary

Mishearings to fix:

| Transcript | Write |
|---|---|
| Stephen, Steve (the host) | Steven (only in the frontmatter and the line under the TL;DR) |
| Alpha Mail | Alpha Male |
| Joe Dispenses | Joe Dispenza |
| Ralph Aldo Emerson | Ralph Waldo Emerson |
| no fat, no fab, nofap | NoFap |
| keegels, keagles, kegel | Kegels, reverse Kegels |
| Wim-hof | Wim Hof |
| Ashwagonda | ashwagandha |
| 8020 | 80/20 |

His terms, spelled this way:
- root muscle, root squeeze, root push, root hold
- cool draw, warm draw, big draw, testicle breathing, microcosmic orbit
- mindful edging, edging session, arousal scale (0–10)
- semen retention, sexual energy, sex energy, sexual transmutation
- resistance (001), total daily volume (005), the pause-intention bridge (663), the three dials (813)
- Inner Circle (private membership community), Brotherhood (free community), Bootcamp (30-day group training)

Add to this list when a reviewer or fixer finds a new mishearing or term. Move it to its own file when it passes about 50 entries.

## 13. Writer: process and self-check

1. Take the frontmatter from the episode's row in `episodes.csv`.
2. Read the whole transcript once, then write the bullets, then the TL;DR, then the line under it.
3. Self-check:
   1. Does every idea of the transcript appear?
   2. Is every number, dose, study, book, product and exercise kept?
   3. Is anything stated that the episode doesn't say? Any word from the watch list (4.5) without his word behind it?
   4. Is every hedge kept, of the four kinds? Is every source he cites named?
   5. Is every quote one unbroken run of the transcript?
   6. Are repetitions merged into one bullet?
   7. Is his name gone from the body, with stories and speakers marked?
   8. Is the TL;DR one sentence of at most 45 words, written last, in the bullets' order?
4. Run the checker on your files: `python3 -I tools/check_recaps.py --recaps holistic-alpha/recaps/ --transcripts holistic-alpha/transcripts/ --episodes holistic-alpha/episodes.csv --only <ids>`.
5. Fix every ERROR. Read every WARN and LOOK against the transcript and fix the real ones. A LOOK is a candidate, often a false alarm.

## 14. Reviewer: checklist

Review each Recap against its transcript. Don't edit files. Return findings only.

0. **Checker items first.** Verify each WARN and LOOK of the checker report for this episode. Report the real ones.
1. **Recall.** Walk the transcript in order, about two minutes at a time. For each stretch, find the bullet that carries its ideas. Report every idea with no bullet, with its `[mm:ss]` and the transcript's words. Ignore the intro, the outro, calls to action and filler.
2. **Fidelity.** For each bullet, find its source passage and compare:
   - hedges of the four kinds (4.4), lost or added
   - quantities and scope
   - the source he cites, or the source of his experience
   - words from the watch list (4.5)
   - every number, and every quote (4.6)
   - in interviews and groups: who says it, line by line
3. **Format.** TL;DR, markers, frontmatter `type` and `guest`, the line under the TL;DR.

Don't report style preferences, or wording that keeps the meaning.

Return one entry per episode:
```json
{"id": "663", "ok": false, "findings": [
  {"severity": "S2", "kind": "advice hedge lost", "ts": "05:47",
   "transcript": "I would suggest that you practice pausing before you take any action",
   "recap": "How to practice: pause before any action",
   "fix": "Suggested practice: pause before any action"}]}
```

Severity:
- **S1**: wrong speaker. An invented fact, number, quote or story. A meaning reversed. An important idea missing, one a listener would act on.
- **S2**: a claim made stronger or wider. A hedge, quantity or source lost. A spliced quote, or one with changed words. A distinct secondary idea missing.
- **S3**: near-equivalent wording. A small detail or image missing. A minor added label.

`kind` is one of: idea missing, advice hedge lost, scope widened, source lost, certainty hedge lost, hedge added, word added, quote spliced, quote altered, number wrong, speaker wrong, fact changed, format.

## 15. Fixer: rules

1. Check each finding against the transcript. Fix it only if it is real, with the smallest edit that follows these instructions. Reject false alarms and say why.
2. Fix every S1 and S2. Fix an S3 when the edit is small.
3. If you change a bullet, check the TL;DR still matches it.
4. Run the checker again. No ERROR may remain.
5. Append one JSON line per finding, fixed or rejected, to the block's log `holistic-alpha/logs/findings/<block>.jsonl`. One file per block, so parallel runs never write to the same file:
```json
{"date": "2026-11-02", "instructions": "v2", "block": "663-656", "id": "663", "reviewer": "sonnet", "severity": "S2", "kind": "advice hedge lost", "ts": "05:47", "verdict": "fixed", "note": "I would suggest"}
```
