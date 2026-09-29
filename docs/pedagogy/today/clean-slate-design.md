---
title: Clean-slate design of the daily practice set
research_date: 2026-09-29
status: draft
purpose: If Today were built from nothing for the May 2027 BC exam, what the selection policy, the session shape, the ordering, the difficulty control, the wrong-answer loop, the review compression, the question standards and the day screen would be, each decision tied to the Stage A evidence.
---

# Clean-slate design of the daily practice set

Every decision below names its evidence in `synthesis.md`, `science.md` or `question-standards.md`. Where the evidence is thin the decision says so and picks the reversible option. Nothing here is a schedule, a quota or a target for the student, and nothing credits mastery except a deterministically graded attempt.

## The unit of scheduling is the observed skill, not the mastered skill [verified]

Every scheduler in the product set spaces from the first success (Anki, HLR, FIRe, ALEKS's knowledge check; science.md 1). The design keeps one memory state per skill from its first credited observation, which Growth already has as FSRS-7 stability and retrievability, and lets the review need of a skill be `1 - R_k` from that moment. Mastery stays a separate, stricter declaration (three unaided successes over seven days on two archetypes), used for gating and for the progress map, never as the entry ticket to review. The two quantities have different jobs: mastery says what the student can build on, retrievability says what is about to be lost.

## The selection policy fires on every choice [inferred]

One priority, evaluated for every candidate archetype on every choice in every block:

```
need(A) = sum over k in reach(A) of (1 - R_k)      reach(A) = A.skills plus their 1-hop gating parents,
                                                    counting only skills with a memory state
```

Block 1 takes the candidates whose reach holds a skill below the desired retention, ordered by `need`, with the hypercorrection lane and the corrected-item requeues ahead of them. Block 2 takes fringe candidates ordered by `need`, so an item that also refreshes a fading parent goes first, with a seeded uniform draw among equals, which keeps the calibration property the plan wants from randomness (science.md 6: adaptive selection biases item estimates). Block 3 takes the retrieval pool ordered by `need`, lowest retrievability first, which is what Anki's ascending-retrievability sort and the forgetting oracle both do. The interleaving window stays a hard constraint on every block. This is candidate 1 of the simulation; it ships only on the simulator bar, otherwise behind a switch.

## Session shape and size [uncertain]

Four blocks, as now, because no session-length evidence exists for mathematics (science.md 12) and the block order (due first, new next, mixed last, notes at the end) is the one order every product with a review model uses. The forecast stays about 45 minutes and is an assembly input only. Two changes to the caps. Block 1's cap is the whole due queue up to a forecast of 12 minutes rather than 5 items or 5 minutes, because Anki's documented harm is a backlog hidden under a review cap and the 60-day measurement shows a mean of 5.5 due skills per due session with 3.9 of them uncovered; what the cap still cannot serve is shown on Today as a count, never as a target. Block 3's floor rises from 10 to 12 minutes when block 1 was empty, so a student with nothing due still retrieves. The session ends when the blocks are empty.

## Ordering and interleaving [verified]

The window rules stay (no more than 2 consecutive same primary skill, 4 skills and 2 units per 10, no family above 3 per 10, 20 percent translations), because Rohrer's d = 0.83 is the largest single effect in the record and the rule is the only mechanical guarantee of it. Inside the window, block 3 prefers a candidate whose primary skill is a named confusion of the previous item's primary skill (`adaptive.common_confusions` on the skill record), because Brunmair and Richter's moderator puts the interleaving gain in mixing similar-looking skills (science.md 3). Blocks are not announced by skill name on Today for the mixed block, since Matuschak's warning about Math Academy is that announcing the topic of a review defeats the method choice the review exists to practise; the review and learning blocks keep their skill lists.

## Difficulty control [uncertain]

No per-item difficulty targeting at learning time. The 85 percent rule is derived for another learner class and disclaims generalisation, the five-term score lost on the simulator, and item-side ratings need 100 learners (science.md 6 and 8). Difficulty is controlled by three things that have evidence: the fading stage (worked example, completion, unsupported) chosen by the stage bands at first contact and by the counter pair afterwards; the variant shift of 0.4 logits inside an archetype; and the guessing-corrected knowledge target of 0.8 used only as the stage filter. A learner-side family rating (an Elo update from first-attempt outcomes) is kept as a simulator candidate and as a display of per-family accuracy on the progress screen, not as a selection term.

## The wrong-answer loop [verified]

On a wrong answer at stage unsupported: the three-part elaborated feedback (rule violated, scoring consequence, correct step), the student's one-line error note, the self-explanation prompt where a BC-ERR was matched, then the item returns through block 1 after 1 to 2 days, or 1 day when the answer was rated confident. All of this is built. Two additions from the product set, both uncredited. First, "Try the step again": after the feedback, the student may re-enter the violated step once, graded deterministically and shown right or not, writing no observation (Alcumus's second try, ALEKS's retry, the lesson framework's one retry; science.md 10 says learning from an error grows when the correct answer is processed with an explanation). Second, the requeued item comes back as a new instance of the same archetype where the bank holds one, not the identical item, because Yeo and Fazio's one-week result favoured new instances for transfer (science.md 2); the identical item returns only when no sibling exists.

## Review compression [single-source]

Block 1 keeps the greedy cover under repetition compression (FIRe, the ALEKS layer curves). Two changes. The cover's reach counts 1-hop parents both ways, as now, and the eligibility floor for a review candidate drops from `p_A >= 0.5` to `p_A >= 0.35` only for candidates that are the sole reach to an uncovered due skill, because the measurement shows most due skills going unserved for want of an eligible archetype; the floor otherwise stays. An uncovered due skill is written to the coverage-gap audit with its reason (no published item, floor, window), so the operator can see which.

## Question standards [inferred]

From `question-standards.md` section 12, every machine-checkable standard becomes a lint in `tools/check_items.py`, strengthening only: exactly four options; every distractor from a distinct BC-ERR path; numeric options sorted or the key not the median more than chance across a bank; the key not the longest statement option more than chance; no free variable in a value option; a calculator item's stem asks for three decimals and its key carries them; a short-answer stem not worded as a choice; every stem carries its command verb; a stem length cap. Items that fail are fixed at the item through the pipeline (check, blind re-solve, distractor path, duplicate), never at the verdict. New items are drafted only where a representation or calculator gap on an archetype is measured.

## The day screen [inferred]

Today shows the forecast in minutes, the three counts (skills due, skills at the frontier, corrected items coming back), the whole due count when the assembled block 1 cannot hold it, the block cards with their intent, and one primary action. It shows no streak, no XP, no daily goal, no score, no pace verdict, and no skill names for the mixed block. The exam date is a fact; the countdown carries no verdict. After the set, the end screen states what was worked and what comes back, and nothing else.

## What this design does not do [uncertain]

It does not fit any parameter, because one learner cannot identify item difficulty or a personal forgetting curve (science.md 6). It does not offer the student a choice of the next item, because the harm of self-scheduling is measured and the benefit is not (science.md 11); a choice of which block to start with is left to the operator's ruling. It does not add a timer, a quota or a target, and it does not loosen the mastery rule to make the due queue fire sooner, because the lever that makes review fire is scheduling from the first observation, which needs no loosening.
