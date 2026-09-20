---
title: Quality and Evaluation
research_date: 2026-09-19
status: draft
purpose: The test strategy, model-output evaluation sets, learning-outcome metrics, offline engine simulation, A/B readiness, release gates and the generated-item error rate gate for the adaptive AP Calculus BC tutor.
---

# Quality and Evaluation

This document says how the app is checked. It covers deterministic software tests, evaluation of model output where there is no deterministic answer, measurement of whether the student is actually learning, and the gates that a phase in [11-phased-delivery.md](11-phased-delivery.md) must pass before it is called done.

Two framing constraints run through all of it.

The first is that the outcome that matters is a standardized test. Kulik and Fletcher found intelligent tutoring systems raised test scores by a median of 0.66 standard deviations but that the effect was much larger on locally developed tests than on standardized ones [verified, https://journals.sagepub.com/doi/abs/10.3102/0034654315581420]. A tutor that only moves its own internal scores has demonstrated nothing. Every internal metric below is therefore paired with a measurement against released AP material on a fixed cadence.

The second is that there is one student. Most of the experimental designs a product team would reach for are unpowered here. What a single student over eight months can support is per-item randomisation within that student, a long series of repeated measures, and offline simulation against synthetic students. What it cannot support is any between-subject comparison, any claim about effect size, and any calibration of item difficulty from response data, which Pelanek puts at a floor of at least 100 students [verified, https://www.fi.muni.cz/~xpelanek/publications/CAE-elo.pdf].

Evidence tags follow `research/README.md`. [verified], [single-source] and [inferred] carry the same meanings as in the track ledgers.

## Test strategy

### Unit tests

Unit tests cover the engine in [02-adaptive-engine.md](02-adaptive-engine.md) and the deterministic checkers in [04-item-generation.md](04-item-generation.md).

Engine coverage is the credit assignment table across all eight `mastery_state` values, the `m_k` formula, the FSRS-7 stability and difficulty updates against the published default parameter vector [verified, https://github.com/open-spaced-repetition/srs-benchmark], the retrievability curve, prerequisite propagation weights and hop limits, fringe computation, the mastery declaration and un-mastery rules, and the fading ladder transitions.

Checker coverage is SymPy equivalence, numeric evaluation to three decimal places, bounds matching, units presence, and the distractor checks: each distractor unequal to the key both symbolically and numerically, distractors pairwise distinct, and each distractor traceable to a named BC-ERR path.

Fixture discipline: engine unit tests run against small hand-built graphs, not against `data/`, so a library edit cannot turn an engine test red for the wrong reason. The real registries are exercised by integration tests instead.

### Integration tests

The content loader is tested against the real `data/` directory on every run. It must load 541 active BC-SKL, 170 BC-CON, 77 BC-PRQ, 1226 prerequisite edges, 139 active BC-QA in 77 families, 395 BC-QV, 76 BC-PT, 390 active BC-ERR, 213 active BC-MIS, 711 BC-SIG and the 14 BC-REP, 17 BC-DF and 29 BC-CV taxonomies, and it must refuse to start on a cycle or a dangling id. The counts are asserted exactly, so a registry change that alters them fails the build and forces a deliberate update rather than a silent drift.

The generation to verification to grading pipeline is tested end to end on frozen fixtures: a fixed archetype, a fixed parameter draw, a recorded model response, and an expected point vector. Provider calls are replayed from recorded transcripts so the pipeline test is deterministic and free; live-provider tests are a separate, manually triggered suite.

The diagnostician is tested against a fixture set built from BC-SIG records: given an observation matching a signal's `observation` text, the diagnosis must return that signal's `mastery_state` for the named skill. This is the one place the 711 signals act as ground truth for a model output, and it is only approximate, because a signal describes an observation rather than a response.

### End-to-end tests

One e2e path per phase, driven through the real frontend: passkey login, a session served from the real content snapshot with a recorded provider, an item answered, feedback shown, mastery state visibly changed on the progress screen. The e2e suite is deliberately thin. It exists to catch wiring failures, not logic failures, and every logic assertion belongs one layer down where it is cheap.

### Contract tests for the content loader

Every registry file is validated against its schema in `schemas/` at load time and again in CI: `skills.schema.json`, `archetypes.schema.json`, `diagnostic_signals.schema.json`, `errors.schema.json`, `misconceptions.schema.json`, `scoring_points.schema.json`, `taxonomies.schema.json`, `curriculum.schema.json`, `frq_records.schema.json`, `mcq_records.schema.json`, `sources.schema.json`. Schema validation is necessary and not sufficient, so three referential checks run alongside it: every `archetypes.skills` id resolves to an active BC-SKL, every BC-SIG `skill` and `archetype` resolves, and every BC-ERR `possible_misconceptions` entry resolves to an active BC-MIS.

The third of those was challenged, because `repo-facts.md` carries two lines that cannot both be true, one reading "errors with misconception links 0" and the other "errors with possible_misconceptions 388". Recomputed from `data/errors.json` on 2026-09-19: of 390 active BC-ERR records, 388 carry a non-empty `possible_misconceptions` list (fix 27). The 388 figure used across the plan is the correct one, the zero line in `repo-facts.md` is wrong, and the contract test stands as written. Two active errors carry no misconception link, which is an expected state rather than a failure and is asserted as one.

Two known library gaps are asserted as expected states rather than as failures, so that closing them is visible. 56 active archetypes have no `point_types`, which means their free-response variants cannot be point-graded, and 36 have no `official_examples`, which means their difficulty priors rest on BC-DF counts alone. The contract test asserts those counts and the app refuses to serve an FRQ-shaped item from an archetype in the first list. Both gaps are carried in [12-open-questions.md](12-open-questions.md).

### Property-based tests for the engine invariants

All 23 invariants in [02-adaptive-engine.md](02-adaptive-engine.md) are implemented as property tests with generated inputs rather than as example tests. The generators draw random mastery states over the real 541-skill graph, random observation sequences, and random clock advances.

The invariants that carry the most weight are the monotonicity trio (correct answers never lower `m_k`, failures never raise it, and no `partial_*` observation raises it), of which the first two are the direct analogue of the BKT degeneracy condition where violating `P(G) + P(S) < 1` inverts the update so correct answers reduce estimated mastery [verified, https://files.eric.ed.gov/fulltext/EJ1115329.pdf], and the third of which closes the partial-credit ratchet described in [02-adaptive-engine.md](02-adaptive-engine.md) (R2); the propagation invariant that fractional implicit credit can never on its own declare mastery; and the interleaving window invariant, which is the only mechanical guarantee that the strongest single mechanic in the plan actually happens on every session [verified, Rohrer et al 2020, d = 0.83, 95 percent CI 0.68 to 0.97, http://uweb.cas.usf.edu/~drohrer/pdfs/Rohrer_et_al_2020JEdPsych.pdf].

Each property test runs at least 1,000 generated cases in CI and the seed of any failure is recorded as a permanent regression case.

## Model-output evals

Nothing below has a deterministic answer, so each eval is an agreement measurement against a hand-built golden set, and each golden set is authored by the operator. No official College Board response, stem, figure or rubric text is ever copied into a golden set or served by the app. College Board defines commercial use to include test-prep settings [verified], so released items are treated as structure only, and anchor quotes stay under the 25-word limit enforced by `qa/07_quotes.py`.

### Golden set 1: generated items per archetype family

77 archetype families, one hand-verified generated item per family, extended to 139 items covering every active BC-QA as [11-phased-delivery.md](11-phased-delivery.md) phase P4 completes generation. Each golden item is produced by the generator, solved independently by the operator, and frozen with its key, its worked solution tagged to point types, its distractor error paths, and its parameter draw.

The eval replays generation against the frozen parameter draw and asserts the key is mathematically equivalent to the golden key under SymPy, the solution path matches the archetype's `expected_solution_path` step for step, every distractor maps to the BC-ERR path recorded on the golden item, and the calculator boundary holds, meaning a `no_calculator` item is closed-form solvable.

Agreement metrics: exact match on the key, and per-point-type exact match on the tagged solution steps. Kappa is not reported here because the comparison is against a single fixed reference rather than a second rater.

### Golden set 2: operator-authored FRQ-style responses

The grader is the highest-risk model role in the product and the published evidence says so plainly. A 2026 study of LLMs grading a mathematics exam against a rubric reports, on N = 28 student submissions, question-level Pearson correlations with human graders of 0.19 to 0.56, exact agreement at most 0.22, best mean absolute error 1.87 points and best RMSE 2.53 at the question level, and total-score exact agreement near zero for almost all conditions [single-source, https://arxiv.org/html/2607.01247]. Rubric prompt engineering moves the number but not into a different regime: CARO reports overall averages of accuracy 0.51 with kappa 0.22 for naive prompting, 0.70 with 0.47 for a GradeOpt baseline, and 0.78 with 0.56 for CARO itself [single-source, https://arxiv.org/pdf/2603.00451]. Kappa 0.56 is moderate agreement, not human equivalence. No published figure exists for LLM agreement with AP Readers on the AP nine-point scale.

The golden set is therefore built to be adversarial rather than representative. The operator authors responses in the shape of AP free responses, never copying an official student response, covering for each targeted BC-PT: a fully correct response, a response that earns the point with unconventional but valid work, a response that fails the point narrowly, a response that is mathematically right with a notation failure, and a response that is wrong earlier but eligible for later points under the AP eligibility-after-error convention. That last category is the one no cited study covers and the one AP rubrics are defined by [single-source, track 3].

Target: 5 responses on each of at least 30 BC-PT ids in phase P3, extended toward all 76 as archetypes gain `point_types`. Both numbers are [inferred] (N4). No source gives a golden-set size for rubric grading, and 5 by 30 is the smallest set that covers the five adversarial response categories above on enough point types for a per-point-type kappa to mean anything. What would settle it is the width of the kappa confidence interval at the first measurement: if the interval at 5 responses per point type is too wide to distinguish the CARO-reported 0.56 from the GradeOpt-reported 0.47, the set grows before the threshold is set.

Agreement metrics, reported per point type and in aggregate:

- Exact match per point, the share of points where the grader's earned or not-earned decision equals the operator's.
- Cohen's kappa per point type, which corrects exact match for the base rate, because a point type that is earned 90 percent of the time can score 0.9 exact match while agreeing at chance.
- Mean absolute error on the question total out of 9, comparable with the 1.87 figure above.
- Escalation rate, the share of points where the three-sample protocol in [03-diagnosis-and-feedback.md](03-diagnosis-and-feedback.md) disagreed and the point went to the review queue. A rising escalation rate is a healthy signal, not a failure, because the design intent is that no single call is ever the final scorer of a free-response point.

The release gate is on kappa and on escalation behaviour rather than on exact match alone, and the threshold is set after the first measurement rather than in advance, because no prior figure exists for this rubric structure.

### Golden set 3: transcription read-back test images

Transcription is where handwriting errors concentrate. The 2026 AIED study grading photographed handwritten university STEM work reports that in the best model roughly 87 percent of remaining errors were transcription failures rather than rubric misapplication, with poor image quality, hallucinated content and mishandling of mathematically equivalent expressions as the named failure modes [single-source, https://arxiv.org/abs/2605.19043].

The golden set is a fixed collection of operator-written pages photographed under controlled variation: good light, low light, slight blur, angled capture, crossed-out work, work in the margin, and a page containing each of the visual forms BC calculus needs that generic OCR is least tested on, namely limit notation, sigma and series notation, parametric and polar forms, integral bounds, and primes against superscripts. Mathpix and MyScript accuracy on this specific visual vocabulary is untested in any source found [single-source, track 3], which is exactly why this set exists.

Metrics: character-level and expression-level exact match of the read-back against the operator's transcript, plus the rate at which a wrong read-back would have changed a point decision, which is the number that actually matters. The image quality gate in [05-assessment-modes.md](05-assessment-modes.md) is tuned against the low-light and blur subsets.

A rubric point lost to a misread exponent is the single most trust-destroying failure this product can have, which is why the read-back is shown to the student for confirmation before any point is graded rather than folded invisibly into the grading call.

### Leniency calibration against published per-question means

The grader can be accurate on individual points and still be systematically generous or harsh. The check is against the only published external anchor available: per-question free-response means from `research/exam/scoring-system.md` [verified, BC-SRC-stats-23, BC-SRC-stats-24, BC-SRC-stats-25].

| Question | 2023 mean (SD) | 2024 mean (SD) | 2025 mean (SD) |
|---|---|---|---|
| 1 | 5.26 (2.24) | 6.45 (2.25) | 5.22 (2.49) |
| 2 | 5.20 (3.06) | 5.56 (2.98) | 3.09 (2.35) |
| 3 | 3.74 (2.69) | 5.57 (2.78) | 6.27 (2.27) |
| 4 | 4.03 (2.13) | 5.84 (2.78) | 5.46 (2.23) |
| 5 | 4.71 (2.86) | 5.92 (2.78) | 5.21 (2.91) |
| 6 | 4.21 (2.97) | 3.38 (2.56) | 4.32 (2.98) |

Every mean and every standard deviation in that table was checked cell by cell against the table in `research/exam/scoring-system.md` on 2026-09-19 and matches it exactly (fix 28). The library file is the owner; this table is a restatement of it and moves only when it moves.

Implied section totals are 27.15 of 54 in 2023, 32.72 in 2024 and 29.57 in 2025 [verified, same source]. The 2025 Chief Reader report goes further and prints a mean for each of the nine individual scoring points on each question, separately for AB and BC, for example BC1 point 5 at 0.84 and BC1 point 8 at 0.18 against an overall BC1 mean of 5.22 [verified, BC-SRC-crabbc-25 p.2]. Per-point means exist only for 2025 [verified].

The calibration procedure: take the app's grader, run it over the golden-set responses whose intended score the operator has fixed, and compare the distribution of point-earn rates against the 2025 per-point means for the corresponding point positions. A grader whose point-earn rate sits far above the published mean on the hardest points, such as BC1 point 8 at 0.18, is lenient on exactly the points that discriminate.

This comparison is an anchor and not a ground truth, and the reasons must be stated. The population means come from students who are not this student. The point positions in the published tables are positions on specific 2025 questions, not BC-PT ids, so the mapping from a published point mean to a library point type is a judgement, not a lookup. The comparison can detect a large systematic leniency bias and cannot certify calibration. It is reported as a direction and a magnitude, never as a pass or fail on its own.

### Never redistributing official responses

No golden set contains an official student response, an official stem, an official figure or official rubric text. The library's own rule holds: no question stems, no figures, no full rubric text, and anchor quotes capped at 25 words and checked by `qa/07_quotes.py`. Official material enters the evals only as structure, meaning archetype invariants, point-type definitions and published aggregate statistics.

## Learning-outcome metrics

Each metric is defined, sourced to a log, and given a stated positive result. Every one of these is a within-student time series, so the read is on trend and on the 6-week external checkpoint, never on a single session.

**Mastery growth per study hour.** Definition: count of skills newly meeting all six mastery conditions in [02-adaptive-engine.md](02-adaptive-engine.md), divided by logged active item time in hours, over a rolling 14-day window. Logging source: `skills_state.mastered_at` and `attempts` timing. Positive result: a stable or rising rate in the first three months and a deliberate fall later, because late skills are deeper in the graph and carry more prerequisites. A rate that rises monotonically to the exam is a warning that the mastery rule has loosened, not that learning has accelerated.

**Retention at 7 and 30 days.** Definition: first-attempt accuracy on due reviews, segmented by the elapsed interval since the previous credited success, bucketed at 5 to 9 days and 25 to 35 days. Logging source: `attempts` joined to the previous credited observation on the same skill. Positive result: accuracy in each bucket at or above the desired retention that scheduled it, so 0.90 before 2027-03-15 and 0.95 after. Systematic undershoot means the FSRS defaults do not transfer to procedural mathematics, which is the single largest unvalidated assumption in the engine [inferred from absence of any benchmark on mathematical problem solving, track 2].

**Mock-exam trajectory.** Definition: total free-response points out of 54 and multiple-choice correct out of 42 on each full mock, plotted over time against the published per-question means above. Logging source: mock sessions in `sessions` with mode `rehearsal`. Positive result: an upward trajectory that crosses the published section mean and keeps rising. No composite score and no predicted 1 to 5 is reported, because the raw-score-to-composite mapping is not published for any year [verified, `research/exam/scoring-system.md`] and the 2027 form is new. A band with stated assumptions and an uncertainty of at least one full score point is the most that may be shown, per [05-assessment-modes.md](05-assessment-modes.md).

**Calibration error.** Two numbers. Brier score: mean squared difference between the confidence rating mapped to a probability and the realised binary outcome, over all items carrying a rating. Confidence minus accuracy: mean mapped confidence minus proportion correct, which gives the sign of the bias that Brier hides. Logging source: the confidence field on `attempts`. Positive result: Brier falling and confidence minus accuracy converging toward zero from above, since overconfidence is the expected starting direction and overconfident learners stop studying prematurely and retain less [verified, Dunlosky and Rawson 2012, https://www.sciencedirect.com/science/article/pii/S0959475211000685]. This is the cheapest high-value metric in the system because it needs no control condition.

**Method-selection versus execution accuracy.** Definition: every attempt scored on two axes, whether the student chose the right method and whether the chosen method was executed correctly, recoverable from the point vector and the diagnosed BC-ERR. Logging source: `gradings` and `diagnoses`. Positive result: method-selection accuracy rising on unseen interleaved sets with execution accuracy roughly flat, which is the specific signature the interleaving literature predicts [verified, the intervention shape, Rohrer et al 2020]. Interleaving helps when the problem is choosing a strategy among confusable alternatives, so antiderivative technique choice and series convergence test choice are the two places this metric should move first.

**Error-type recurrence.** Definition: for each BC-ERR diagnosed at least twice, the rate at which it reappears on subsequent items loading the same skill, measured over the 30 days after the first diagnosis. Logging source: `diagnoses`. Positive result: a falling recurrence rate for named error types, which is a sharper success criterion than rising overall accuracy because it says the diagnosis did something. The registry supports this directly: 390 active BC-ERR records, 388 with `possible_misconceptions` filled, each separated from the 213 BC-MIS records they may be caused by, because the same error can come from several causes.

**Adherence versus effort.** Definition: adherence is the share of scheduled due queues completed on their due day; effort is median items per session and median time per item. Logging source: `sessions`. Positive result: adherence holding above a level the student sets, with effort flat. The failure signature is explicit and must be alarmed on: adherence holding while items per session falls, which is streak-preserving behaviour with a token session. The streak unit is a completed due queue precisely so this cannot be gamed, and no engine state rewards volume of easy items.

**Free-response participation and read-back abandonment (R11, fix 6).** Definition: two numbers. Free-response items attempted per week, counting any item whose format is free response and whose capture or MathLive entry was started, over a rolling 7-day window. Read-back abandonment rate, the share of paper captures where the image passed the quality gate and the read-back was rendered but the confirm step in [05-assessment-modes.md](05-assessment-modes.md) was never pressed. Logging source: `attempts` for the format and start event, and the capture and confirm events on the transcription path. Positive result: weekly free-response attempts holding at or above a non-zero floor with abandonment flat or falling.

This metric exists because the per-FRQ ritual is expensive for the student, being print, handwrite, photograph, pass a quality gate, read the read-back, confirm it, then wait while the grading calls resolve, and nothing else in this document would notice the student quietly avoiding it. The adherence metric would stay green while mode composition drifted toward multiple choice and MathLive short answers, since those need no paper. A falling free-response rate with flat adherence is the signature to alarm on. P3's exit criteria require a non-zero floor on weekly attempts during the P3 trial and require the abandonment rate to be measured and published rather than assumed small.

**The external checkpoint.** Every 6 weeks, progress is reported against released AP material rather than internal item scores [verified as the design requirement, Kulik and Fletcher 2016]. This is the only metric with authority to contradict all the others.

## Offline simulation of the engine against synthetic students

The engine cannot be tuned on one real student, because the sample is one and the feedback loop between policy and data is exactly the bias the literature warns about. Simulation is how the policy is compared before it touches the student.

**The world.** Synthetic students carry a hidden true state over the real 541-skill graph loaded from `data/`, not a toy graph, so the simulation inherits the genuine 602 hard and 622 supporting edges, the genuine 139 archetypes with their 3 to 6 skill loads, and the genuine 31 independently assessable skills. Each synthetic student has a per-skill latent competence, a per-skill learning rate drawn from a band, and a forgetting process.

**Forgetting.** The simulator's forgetting curve is deliberately not FSRS. Using the engine's own decay model as the world model would make the decay term unfalsifiable. The simulator uses an exponential decay with a per-skill half-life that grows with successful retrievals, which is the shared assumption across SM-2, Leitner, half-life regression and FSRS [verified, the shared assumption, track 2], and a second arm uses a power-law curve. Both arms are run so that policy conclusions that depend on the curve shape are visible as such.

**Slip and guess.** Observation is noisy. Slip is the probability of failing an item whose skills are all truly mastered; guess is the probability of succeeding without them. For multiple-choice items guess is floored at 0.25 for four options, matching the option count and floor the engine assumes in [02-adaptive-engine.md](02-adaptive-engine.md) (C2, fix 14). The earlier 0.2 at five options was inherited from a stale assumption in [01-learning-model.md](01-learning-model.md) and would have biased every policy comparison here, because a simulator that under-credits guessing makes any policy look better at discriminating than it is. The bounds follow the empirical-degeneracy convention that both slip and guess stay below 0.5 [verified, Baker, Corbett and Aleven as reported in https://files.eric.ed.gov/fulltext/EJ1115329.pdf]. Sweeps run at slip in 0.05, 0.10, 0.20 and guess at the format floor. The three slip values are [inferred] (N5): only the 0.5 ceiling is sourced, and 0.05, 0.10 and 0.20 are a low, middle and high bracket chosen to span that range. What would settle them is the observed first-attempt failure rate on items whose skills are all declared mastered, which is a direct empirical estimate of slip and becomes available once a few hundred such attempts exist.

**Policy comparison.** Arms compared on identical student populations and identical seeds:

1. The two-term learning-mode score shipped in P1 and P2, which is due coverage within the fringe with uniform random tie-breaking (R4).
2. Random selection within the outer fringe, the control arm.
3. The deferred five-term score from [02-adaptive-engine.md](02-adaptive-engine.md), with `W_LEARN`, `W_COV`, `W_WEIGHT`, `W_REP` and `EXPLORE_SHARE` turned on.
4. Two-term selection with no interleaving constraints.
5. Two-term selection with no prerequisite propagation.
6. Two-term selection with the FSRS decay term turned on, so `lambda = 2.0` against the shipped `lambda = 0` (R3).
7. Pure compensatory item prediction instead of the conjunctive and compensatory split.
8. Difficulty targets at 0.6, 0.7, 0.8 and 0.9 to bracket `TARGET_LEARN` in its fading-stage-filter role.

Arms 1, 2 and 3 are the three-way comparison that decides the shape of the selection function: five-term against two-term against random (R4). Arm 6 is the ablation that decides whether the decay term returns, and it is now stated in the direction the decision runs, since `lambda = 0` is what ships and the burden is on the term to earn its way back in (R3).

Outcome measures per arm: true skills mastered per item served, true skills mastered per simulated minute, retention of the true state at simulated day 7 and day 30, and measurement bias, meaning the mean signed difference between the engine's `sigmoid(m_k)` and the hidden true competence.

**Feedback-loop bias check.** Adaptive selection breaks naive difficulty estimation, which Pelanek demonstrates by simulation and Gervet et al flag as a general hazard of learning from self-selected data [verified, https://www.fi.muni.cz/~xpelanek/publications/CAE-elo.pdf and https://files.eric.ed.gov/fulltext/EJ1273917.pdf]. The check compares measurement bias on the adaptive arm against the random-selection control arm on the same students. If the adaptive arm's bias is materially worse, the exploration share needed to close the gap becomes a finding rather than a guess, and it is set from that result when the five-term score is turned on.

Under the two-term score there is no separate exploration arm in production, because `EXPLORE_SHARE` is 0 and selection is already uniform random within the tied set, so the live policy and the control differ in exactly one term (R4). The live counterpart to the simulated control returns with the five-term score.

**Acceptance thresholds.** Set as relative comparisons, because absolute numbers from a simulator whose world model is invented would be false precision.

- The two-term policy reaches a given level of true mastery in no more items than the random-fringe control, on at least 90 percent of simulated students. Failing this means selection on due coverage is worse than picking at random from the fringe.
- The five-term score is turned on only if it beats the **two-term** score on true skills mastered per item served, on at least 90 percent of simulated students (R4). Beating the random control is not sufficient and never was: the two-term score already beats random, so a five-term score that only clears the random bar has bought four inferred weights for nothing. This is the acceptance bar referred to in [02-adaptive-engine.md](02-adaptive-engine.md)'s deferred subsection, and the same bar governs `EXPLORE_SHARE`, which returns only with the score it exists to correct.
- `lambda` returns to 2.0 only if arm 6 beats arm 1 on true mastery per item or on retention of the true state at day 30 (R3). Arm 6 is the gate; absent a result from it, `lambda` stays 0.
- Removing interleaving does not improve true retention at day 30. If it does, the constraint is costing learning and the interleaving literature does not transfer as assumed.
- Measurement bias on the adaptive arm is within 0.05 of the control arm's bias in absolute value.
- No arm produces a state in which a skill is declared mastered while its hidden true competence is below the slip-adjusted equivalent, at a rate above 5 percent of declarations. The 5 percent is [inferred] (N6): it is the only numeric acceptance threshold in this section and no source gives a tolerable false-mastery rate. What would settle it is the observed un-mastery rate after declaration on the real student, since a false-mastery rate in the simulator that is far below the un-mastery rate in life means the simulator is the optimistic one and the threshold is not binding.

All of them are relative and none certifies the engine. The simulator's world model is invented, so it can falsify a policy choice and cannot validate one. That limit is stated on the dashboard next to the numbers.

## A/B readiness

**Per-item randomisation within one student.** The only design available. Each experiment assigns a treatment at the item or skill level with a seeded RNG, records the assignment on the attempt, and compares delayed accuracy at a later checkpoint. Assignment is stratified by unit and by the engine's predicted success probability so that the arms are balanced on difficulty, which matters more here than in a large trial because the sample is small enough for chance imbalance to dominate.

**Which experiments from [01-learning-model.md](01-learning-model.md) are powered for a single student.** Powered means enough within-student item pairs accrue over eight months for a difference of a plausible size to be visible, not that a p-value will be computed. Nothing here supports an effect-size claim.

| Experiment | Randomisation unit | Powered | Why |
|---|---|---|---|
| Elaborated feedback versus verification-only | item | yes | every corrected item is an observation, hundreds accrue, and the comparison is a clean within-student A/B over a few months [verified as the design, track 1] |
| `RETRIEVAL_ENTRY` 1 versus 3 unaided successes before a skill joins the block 3 mixed-review pool | skill | yes | 541 skills give a large enough pool to split, and the outcome is delayed accuracy on each skill. This experiment varies `RETRIEVAL_ENTRY` only. It does not touch the six-condition mastery rule, which keeps its 3 credited unaided successes in both arms (R8, fix 12) |
| Self-explanation prompt present versus absent on worked examples | skill | marginal | prompts attach only at `example` and `completion` stages, so the eligible pool shrinks as skills advance |
| Representation-translation share above versus below the floor | session | no | the unit is a session, giving on the order of 200 observations total, and session-level confounds are uncontrolled |
| Productive-failure opener versus direct instruction | concept | no | at most 5 or 6 conceptual targets qualify, so the pool is single digits |
| Desired retention 0.90 versus 0.95 | skill | no | the manipulation changes schedule density, which changes exposure count, so the arms are not comparable on the outcome |

**Switch design.** Every experiment is a named flag in a single experiments table with a state in `off`, `on`, `randomised`, a seed, a start date, and an assignment function. Default is `off`. Turning a flag to `randomised` begins assignment for items served after that instant and never reassigns a unit that already has an assignment, so a skill assigned to the 3-success arm stays there for the life of the experiment. Assignments and outcomes are queryable without joining to provider logs, so the analysis does not depend on anything that may be purged under the retention policy in [09-security-and-privacy.md](09-security-and-privacy.md).

No experiment may change the mastery rule, a gate, a threshold or a tolerance as its treatment. Gates may be strengthened, never loosened, and an experiment is not a licence to loosen one.

## Release gates per phase

Each phase in [11-phased-delivery.md](11-phased-delivery.md) ships as one pull request and does not ship until its gate passes. The standing gate on every phase: all unit, integration, contract and property tests green, and every applicable engine invariant from [02-adaptive-engine.md](02-adaptive-engine.md) passing at 1,000 generated cases. Invariant 6, that no `partial_*` observation may increase `m_k`, is named explicitly in the standing gate (fix 2, R2), because it is the one invariant that a later change to `gamma` or `rho` could silently break from outside the credit table, and the credit weights are tunable.

**P1, teaches from day one.** Content loader passes contract tests against the real `data/`. Engine invariants 1 through 11, 18, 20, 21 and 22 pass, using the numbering in 02-adaptive-engine.md, where 21 is the co_requisite and BC-TOP inertness property. A session on Unit 2 skills completes end to end and mastery states visibly change. The key error rate is measured on a 100-item audited sample and the threshold is set from that measurement, as described below.

Invariant 17 and Golden set 1 were listed here and are removed (R31). Invariant 17 is the rehearsal-mode property, and rehearsal and every timed mode arrive in P5, so it is gated there. Golden set 1 is defined below as items produced by the generator, and the generator arrives in P4, so it is gated there. Neither could be evaluated in P1, and a gate that cannot be evaluated is not a gate.

Three further P1 gates:

- **Cold-start `p_A` distribution (fix 1, R1).** `p_A_knowledge` is computed for all 139 archetypes at the cold-start state, under the centred `beta_k` prior and the conjunctive product, and the distribution is published with its 10th, 50th and 90th percentiles. If the 90th percentile is below 0.3, P1 does not merge: the 0.35 coefficient and `TARGET_LEARN` are recalibrated together first. This gate catches the failure mode where every candidate's predicted success probability collapses toward zero and any difficulty-targeting term stops discriminating.
- **Items are hand-authored (R9).** P1 publishes 130 operator-authored items, 10 per P1 archetype, each with a MathJSON key checked by SymPy. The generator, the independent re-solve and the item review queue are not in P1; they arrive in P4. The 100-item audit stands unchanged, with the operator solving each item without seeing the key.
- **SymPy settle rate published (R9).** The share of BC-relevant expression pairs SymPy can settle is measured on the 40-pair `answers_equiv` fixture and published as a number with its denominator. Unanimity as the P4 publication rule is conditional on that rate, because at a low settle rate unanimity routes a large fraction of items to a one-person review queue and the fringe fails closed behind it.

**P2, diagnostic and whole-graph selection.** Invariants 12 through 16, 19 and 23 pass. 1,000 simulated diagnostics respect the 30-item cap, the 10-item floor, the one held-out extra problem and full 10-unit coverage. The offline simulation's first acceptance threshold, that the two-term policy beats the random-fringe control on at least 90 percent of simulated students, passes.

**P3, FRQ capture and per-point grading.** Golden set 2 exists at 5 responses on at least 30 BC-PT ids, with kappa and exact match per point type reported and the escalation threshold set. Golden set 3 exists and the read-back gate is tuned against its low-light and blur subsets. The share of grading errors attributable to transcription is measured on golden set 3 and compared against the 87 percent figure from the AIED study [single-source, https://arxiv.org/abs/2605.19043]. Leniency calibration against the published per-question means is run and its direction and magnitude reported. Free-response attempts per week hold above a non-zero floor for the duration of the P3 trial, and the read-back abandonment rate is measured and published (R11).

**P4, generation for all 139 archetypes.** Golden set 1 exists for every archetype family shipped in Units 1 to 3, which is where it enters (R31). Key error rate on a fresh 100-item audited sample is at or below the threshold set in P1. The duplicate gate is validated on a labelled sample rather than trusted at its declared thresholds of MinHash Jaccard 0.8 over 5-grams and embedding cosine 0.85 [single-source]. Monte Carlo family checks over a few hundred parameter draws pass for every archetype. No archetype lacking `point_types` serves an FRQ-shaped item.

**P5, assessment modes.** Invariant 17 passes on a full timed part drill, meaning no mastery state moves. This is where invariant 17 enters, and it is not gated before here (R31). Mock-exam trajectory begins logging. The score band displays an uncertainty of at least one full score point and no composite prediction.

**P6, provider layer.** Prompt template golden tests pass for every role. Fallback chains are exercised with simulated provider failures and no role silently degrades to a provider it may not use, in particular the offline fallback is never routable as a grading peer and the tutor role is never routable to a non-streaming adapter.

**P7, evaluation harness.** Every offline simulation acceptance threshold passes, including the three-way comparison of the five-term, two-term and random arms, whose result decides whether the five-term score and `EXPLORE_SHARE` are turned on, and the arm 6 ablation, whose result decides whether `lambda` returns. The metrics dashboard renders all nine learning-outcome metrics from real logged data. At least one A/B switch has run in `randomised` state long enough to produce a readable time series. The 6-week released-material checkpoint flow has run at least once end to end.

**P8, design and multi-user readiness.** WCAG 2.2 AA contrast ratios of 4.5:1 and 3:1 verified on both themes. Data export and purge tested against the retention policy. Item-side Elo recalibration path exists but stays disabled below 100 learners, per the calibration plan in [02-adaptive-engine.md](02-adaptive-engine.md).

## Key error rate gate for generated items

A key error is a generated item whose stated correct answer is wrong, whose worked solution contains a mathematical error, or whose distractor set contains an option that is in fact correct. It is the most damaging defect this product can ship, because it teaches the student something false and destroys trust in every other judgement the app makes.

**The audit.** A stratified sample of 100 generated items that have already passed the full verification pipeline in [04-item-generation.md](04-item-generation.md), meaning independent re-solve by a second model that never saw the key, SymPy equivalence, numeric evaluation at several points, Monte Carlo over the parameter family, distractor checks and the calculator-boundary check. The sample is stratified by unit so that no unit contributes more than 15 items, and by calculator status in proportion to the archetype population of 75 `no_calculator`, 37 `either` and 27 `calculator`. The operator solves each item by hand, without seeing the key, and records the verdict. In P1 the sample is drawn from the 130 hand-authored items instead, which pass the SymPy equivalence, numeric and distractor checks but not the generator or the independent re-solve, since neither exists before P4 (R9). The audit procedure and the threshold rule are identical in both cases; only the population changes, and the P1 rate is therefore a floor for what the generated pipeline must match rather than an estimate of it.

**The measurement.** Reported as key error rate with a Wilson interval, plus a breakdown by unit, by calculator status, and by whether the archetype has `official_examples`, since the 36 archetypes without them are the ones whose invariant structure is least anchored.

**The threshold.** Set after the first measurement in P1 and not before. There is no published base rate for this kind of pipeline on this kind of content, and inventing a number now would be a guess dressed as a gate. What is fixed in advance is the rule for setting it: the threshold is the observed P1 rate or the operator's tolerance, whichever is lower, and it may only move downward afterwards. Gates may be strengthened, never loosened.

**What happens on a failure.** An audit above the threshold blocks the release of generated content for the affected stratum, not the whole bank. Every item in the failing stratum is quarantined, the failure mode is traced to a stage of the verification pipeline, and a regression fixture is added at that stage. Since publication requires unanimous agreement and disagreements go to the review queue rather than being averaged, a raised error rate should show up first as a raised escalation rate, and an audit failure with a flat escalation rate means the verifier is agreeing with the generator for a shared reason, which is the worst case and is investigated as such.

**Re-audit cadence.** Every phase that changes generation, every generator prompt version change, and every 500 newly published items, whichever comes first.
