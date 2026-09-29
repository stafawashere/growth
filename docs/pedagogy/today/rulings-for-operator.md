---
title: Rulings for the operator, Today redesign
research_date: 2026-09-29
status: in_progress
purpose: Every technique the Today research found in a top product that a project rule forbids, with the rule and the reasoning, and every loosening or product decision the redesign needs but only the operator may make.
---

# Rulings for the operator

Nothing here was adopted. Each entry names the technique, where it was seen, the rule it hits, and the reading the orchestrator took. The operator rules; until then the default stands.

## Techniques rejected under the ground rules [inferred]

| Id | Technique | Seen in | Rule it hits | Reasoning |
|---|---|---|---|---|
| R1 | Daily XP or minute target (20 to 40 XP a day) | Math Academy, Brilliant (15 minutes a day) | Today is never a quota or a target; no study advice | A target changes the stop rule from "the blocks are empty" to "the number is reached"; science.md 13 puts completion-contingent rewards at d = -0.36 |
| R2 | Streaks and streak freezes | Duolingo, Brilliant, IXL, Math Academy accountability | no streak beyond the queue-bound one plan 01 allows; no praise copy | Engagement evidence only, no learning evidence; the queue-bound streak in plan 01 already exists and is not displayed by the redesign |
| R3 | Leagues and leaderboards | Math Academy, Duolingo | one student; no praise; no comparison | Hanus and Fox 2015 found lower motivation and lower exam scores under badges and leaderboards |
| R4 | Keys, energy or hearts that limit a day's practice | Brilliant (2 keys a day), Duolingo | the session ends when the blocks are empty | A cap set by a product, not by need |
| R5 | A score that falls on a wrong answer | IXL SmartScore Challenge Zone, ALEKS, DeltaMath Back to Zero, Alcumus un-pass | no score shown to the student; only deterministic grading feeds the model | A visible penalty is a target in reverse; the model's `f_k` already carries the evidence without a number on screen |
| R6 | A visible gate timer (12 hours before the next mastery challenge) | Khan Academy | never a timer | The spacing it enforces is the engine's, on retrievability, and needs no clock on screen |
| R7 | A required-correct count shown as a goal (5 correct to complete) | DeltaMath, IXL (reach 80) | never a target shown to the student | The mastery rule is the engine's, not the student's task |
| R8 | A predicted level, rating or score | IXL grade level, Alcumus rating, Brilliant level | no prediction talk; plan 05 shows a band with its assumptions only | Unpublished cut points and a new 2027 form |
| R9 | Dropping an item from the queue by choice | Anki suspend, Karpicke's self-control condition | the queue is set by the engine | Karpicke 2009 and Kornell and Bjork 2008 found dropping harms retention |
| R10 | Announcing the review topic before the item | Math Academy review tasks, Growth's own focus card for the mixed block | none directly; interleaving is the mechanic | Matuschak's warning that a labelled review defeats the method choice; the redesign hides skill names on the mixed block only |
| R11 | A per-item difficulty target at learning time (85 percent rule, 80 percent quizzes) | Math Academy, Alcumus, IXL, Duolingo Birdbrain | plan 02 R4: two-term until the simulator shows five-term wins; gates are strengthened, never loosened | Wilson et al disclaim the generalisation; five-term lost; a candidate arm is run for the record |

## Loosenings and decisions that need the operator [uncertain]

| Id | Decision | Default taken | What would settle it |
|---|---|---|---|
| C1 | Block 1's cap of 5 items or 5 minutes hides the rest of the due queue (synthesis.md rank 6). The clean-slate design raises it to the whole due queue up to 12 forecast minutes | Not changed in production; the simulator arms keep the cap so the comparison is paired on the shipped shape; Today keeps showing the whole due count | A simulator arm with the wider cap on delayed mastery and retention, then the operator's ruling, since it changes plan 02's block caps |
| C2 | The review eligibility floor `p_A >= 0.5` leaves due skills uncovered when no eligible archetype reaches them (3.9 of 5.5 per due session on the 60-day measurement) | Not changed; the gap analysis reports the causes | A ruling on lowering the floor for sole-reach candidates, since it is a threshold |
| C3 | An uncredited "try the step again" after elaborated feedback (clean-slate design, wrong-answer loop) | Not built in Stage D unless the design stage keeps it; it writes no observation, so no gate moves | Whether an uncredited retry counts as mid-item feedback under plan 03's timing rule |
| C4 | The requeued corrected item returns as a sibling instance rather than the identical item | Not built; the requeue lane is by item id | Whether the review screen's promise "the one you corrected comes back" must hold literally |
| C5 | The pace verdict on the exam countdown reads as a target or a prediction | Left as it is | Whether "pace" is prediction talk under the project rule |
| C6 | Letting the student choose which block to start with (ALEKS carousel, Math Academy dashboard) | Not offered; one next action per screen | A within-student A/B on completion, if the operator wants the autonomy support |
| C7 | A statement-keyed item's key label is verified only by identity (question-standards.md 12) | Left; flagged in the audit | Whether a second reader should judge every statement key, which is human time |
