---
title: Clean-slate design, a lesson app for every AP Calculus BC skill
research_date: 2026-09-29
status: draft
purpose: If the lesson app were built from nothing today for every skill on the BC exam, the content model, the lesson anatomy minute by minute, the interaction design, the feedback loop on wrong answers, the adaptation, the visual system and the engineering, each decided and each tied to the evidence in this directory.
---

# Clean-slate design

Written by claude-fable-5-1 on 2026-09-29 on the operator's delegation. Every decision below is a decision, not an option list, and each names the file and section in `docs/pedagogy/` that supports it. Where the evidence is thin the tag says so and the decision is the cheapest reversible one. The constraints a clean slate still inherits are the project's: no mastery credit for reading, no praise, no schedules, no prediction of exam outcomes, facts from the library only, and an exam with a published rubric as the criterion.

## The unit and the goal [inferred]

The unit of instruction is the concept, one lesson per BC-CON record, because the exam tests skills that share a concept's definition and notation and because a skill-level lesson would restate its siblings (plan 15 "What a lesson is"). Math Academy's knowledge point, a worked example plus two to three problems, is the closest product unit (products/math-academy.md, Lesson anatomy), and a Growth concept lesson is three to four such points in a fixed order.

The goal of one lesson is that the student's first graded attempt on the concept succeeds at the completion stage more often and sooner than it would without the lesson, measured as attempts to reach the unsupported stage and as delayed accuracy at the six-week checkpoint (plan 15 Telemetry). A lesson never measures itself by its own checks.

## Content model [inferred]

One authored body per concept, sections typed and ordered, every sentence sourced, every step a CAS-checked expression, every check item-shaped so the item grader grades it. That is the current model and it stays. The clean slate adds four things and removes none.

| Addition | What it is | Evidence |
|---|---|---|
| `prediction` section | One question on the concept's core claim, posed on worked example 1's own numbers, with 2 to 4 options or a numeric key, and a one-sentence resolution the key idea screen shows beside the student's choice | learning-science.md 13 (Richland 2009, Pan and Sana 2021), 9 (Sinha and Kapur g = 0.36); products: Brilliant, AoPS, Desmos, 3Blue1Brown (synthesis rank 2) |
| `contrast` on the first strategy block | Two short stems side by side: one that is this concept, one near miss that is not, and the feature that separates them | learning-science.md 14 (Alfieri 2013, Schwartz and Bransford 1998), 2 (Rohrer 2020); products: Desmos card sorts, Khan strategy lessons (synthesis rank 4) |
| `fade_from` on worked example 2 | The step index from which the example is withheld; the student produces the answer from the shown steps before the rest reveals | learning-science.md 1 (Renkl 2002 backward fading, Barbieri 2023 g = 0.48); products: Brilliant "scaffolding falls away", Math Academy (synthesis rank 1) |
| `fix_prompt` on an error block | When the wrong and right steps differ as expressions, the student writes the right step before it is shown | learning-science.md 9 (Durkin and Rittle-Johnson 2012, Adams 2014); products: Khan "find the error" (synthesis rank 3) |

Two more fields make the rest checkable: `no_figure_reason`, a sentence a lesson must carry when it has no drawn block (synthesis rank 6), and a served-text rule that no record id or page citation reaches the student (the reader strips them today; the checker refuses them tomorrow).

The prompts (prediction, fix, fade) are not checks. The three checks stay completion, isomorph and multiple choice, and `LESSON_CHECKS_MAX` stays 3 (rulings-for-operator.md C1). A prompt's answer is stored in the same response table as a check's, uncredited, so telemetry can read it.

## Lesson anatomy, minute by minute [inferred]

The full form, for a student whose predicted knowledge is below `STAGE_LOW`. Minutes are the reading time at 150 words per minute plus a per-interaction allowance; the authored forecast is the words at 150 per minute as today, and the measured forecast replaces it after five completions (plan 15). The total stays under the 6-minute cap because the extended key ideas are the first thing a designer trims.

| Minute | Screen | What the student does | Words | Why here |
|---|---|---|---|---|
| 0:00 | Predict | Reads one question on concrete numbers and commits to an answer; no verdict yet | 30 to 40 | Pretesting primes the rule that follows (learning-science.md 13); the concrete case comes first (learning-science.md 8) |
| 0:30 | What a response shows | Reads the orientation | 60 | The exam's own framing of the concept, before any rule |
| 0:50 | Key idea | Reads the core key idea, sees the prediction resolved against it, and where the idea is a process or a relation, steps a motion figure or moves one control | 120 | The rule arrives as the answer to the prediction; the figure carries its labels inside (learning-science.md 6, g = 0.63) |
| 1:50 | Recognise | Reads the cue, the first line and the rival, then the contrast pair: this stem, that stem, the feature that tells them apart | 80 plus 60 | Discrimination is what the exam pays for (learning-science.md 2, 14) |
| 2:30 | Worked example 1 | Reveals the steps one at a time, each with its cue and its why beside it, then the scoring checklist where one exists | 100 | The worked example effect for novices (learning-science.md 1) |
| 3:30 | Check 1 | Completes the same example with its last step blank, at once | 20 | Immediate practice on the same shape (synthesis rank 1); backward fading's first step |
| 4:00 | Traps, 2 to 4 | For each error: reads the observed behaviour, sees the wrong step, writes the right step, then sees the right step and the scoring consequence | 40 each | Erroneous examples with a fix beat passive pairs (learning-science.md 9) |
| 5:00 | Worked example 2, faded | Reads the steps up to `fade_from`, writes the answer, then sees the withheld steps | 60 | Backward fading before the graded ladder begins (learning-science.md 1) |
| 5:30 | Check 2 | Solves an isomorph unsupported | 20 | Generation before the graded item (learning-science.md 3) |
| 5:50 | Representations, if any, then Check 3 | Reads the representation block, answers the four-option question whose distractors each carry an error path | 60 | The diagnostic link into the error blocks (plan 15) |
| 6:00 | End | Reads "The first problem is next" | 15 | A defined end (plan 08) |

The brief form, for the middle band: Predict, What a response shows, the core key idea, Recognise with the contrast pair, worked example 1, check 1, the first two traps, check 2, end. About 3 minutes and at most 450 words. The high band gets no lesson and a link on the item, as today.

## Interaction design [inferred]

One action per screen, and the action comes before the reveal. A prediction screen holds one committed answer; a key idea screen holds one figure with one control or one frame stepper; a worked example holds one "Next step"; a trap holds one field; a check holds one field or one option group. That is Desmos's "one screen, one verb" and Math Academy's unfurling Continue (products/desmos-classroom.md, products/math-academy.md) under plan 01's one-idea-per-screen rule.

Reveal is gated on commitment where the science says commitment matters: the prediction cannot be skipped by "Next part" without an answer (though "Skip to the problem" always leaves the lesson), a fix prompt shows the right step only after an answer or after the student asks for it by name ("Show the right step"), and a faded example shows its withheld steps after an answer. A worked example's steps are not gated: "Next part" reveals every remaining step before it leaves, so a student who skips forward still saw the solution.

Keyboard first: Tab moves through the one action and the two buttons, Enter submits a check, arrow keys move a control or a frame, and the math field is MathLive with the raw LaTeX inspector beneath it, as every item already has. No timer anywhere in a lesson.

Pacing is shown as "Part n of m" with the part named ("Predict", "Key idea", "Recognise", "Example", "Check", "Trap", "Faded example", "End") and a segmented bar, so the student knows what kind of screen is next. No minutes remaining, because a countdown reads as a schedule.

## The feedback loop on a wrong answer [inferred]

A wrong answer on any check or prompt shows three things in this order, in the record's own words: what the response did (the matched error's `observed_behavior`), the right step beside the wrong one (the error block's `right_step` and `wrong_step`), and the scoring consequence (`scoring_consequence`). Then one retry on a short answer, then the worked solution. When no error record matched, the verdict shows the worked solution at once. Every verdict on a check also carries the link into the trap the error belongs to, as today. No score, no praise, no percent (plan 08 Interface writing; rulings R3, R5).

The evidence: information-rich feedback outperforms verification (learning-science.md 11, Wisniewski 2020 d = 0.48), the second try before the answer is what AoPS, ALEKS and DeltaMath converge on (synthesis rank 5), and the right step beside the wrong step is the contrasting-cases mechanism at the moment of the error (learning-science.md 14).

A correct answer reads "Correct" with its glyph and nothing more. The prediction has no wrong answer: the key idea screen states what the student predicted and what the rule gives, without a verdict word, because the prediction's job was activation, not assessment.

## Adaptation [inferred]

What adapts per student stays what plan 15 already decided, because the evidence supports dose and order changes, not explanation changes: the band from predicted knowledge chooses full or brief; a diagnosed error opens the lesson at its trap through `lesson_link`; a prerequisite gap inserts the bridge; refreshers fire on state (T1 to T5), never on a timer (learning-science.md 4). The clean slate adds nothing to that machinery. It records two new signals for the telemetry only: the prediction answer (right or wrong before instruction) and the fix-prompt outcome per error, so the A/B in plan 15 can read whether a wrong prediction predicts a later credited failure on the same concept. Neither signal writes to any mastery state (plan 15 L0).

## Visual system [inferred]

The tokens of `app/design/growth-tokens.json` and plan 08's type table, unchanged: Inter for prose, KaTeX for mathematics one step up, one column of 820 pixels that stops, 16-pixel gutters on a phone, no footer, no gradient, no colour that carries meaning alone. The lesson-specific rules:

- A figure carries its labels inside and sits under the text that refers to it on the same screen; no screen scrolls between a figure and its question (learning-science.md 6).
- Mathematics that a design writes as a decimal renders as a decimal; a value written as an exact fraction renders as a fraction. The renderer must not turn 0.52 into 13/25 (a defect the gap analysis found).
- The wrong step and the right step sit side by side above 600 pixels and stacked below it, each under its label and glyph, so the pair reads in greyscale.
- The prediction's options and the multiple-choice options are bordered rows, chosen row raised, radio drawn, as every item already does.
- Motion is the student's: frames step on a key press, auto-advance only without reduced motion, cross-fade under it (plan 08 Motion rules).

## Engineering [inferred]

Authoring pipeline: a design document per lesson (prose plus one machine record), a design checker that CAS-verifies every step and key and recomputes every cap, a blind re-solve by a separate agent that never sees a key, a block audit against the source, a deterministic transcriber to the record, a record checker with the same rules, ingest at server start that refuses anything not signed off. That is the current pipeline and every product in the set lacks its verification half (synthesis, last section). The clean slate changes only the template and the two checkers to know the four additions, and the transcriber to carry them.

Storage: one JSON record per lesson under version control, ingested into `lessons`, `lesson_verifications`, `lesson_state`, `lesson_events` and `lesson_check_responses`. Prompt answers go to `lesson_check_responses` with the section id as the check id; no new table.

Rendering: the plan function decides the ordered screens per band and reason, the reader renders the plan and nothing else. The plan gains the prediction as the first screen of both bands and moves check 1 to follow example 1. Section views log their delivery mode, and the events route accepts the reader's screen kinds (`check`, `contrast`, `prediction`) as modes, which the gap analysis found it does not today.

Verification: every new rule has a red fixture that fails it and a green record that passes it, and the render harness walks every record in one process, so a lesson that cannot render never ships.

Cost: authoring runs offline on the operator's Claude Code subscription at $0.00 API spend, as plan 14 already prices it; the four additions add words and one re-solve per faded example and per prediction, inside the existing lines.

## What the clean slate does not build [inferred]

No video (rulings R11). No chat (R7). No hints (R8). No streaks, XP, hearts or leagues (R1 to R4). No delayed lesson check, because the graded ladder is the delayed retrieval and carries the credit (synthesis rank 8). No per-student rewriting of explanations, because the evidence supports changing the dose and the order, not the words (plan 15 "What adapts and what is fixed").
