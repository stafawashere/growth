---
title: Diagnosis and Feedback
research_date: 2026-09-19
status: draft
purpose: How an attempt becomes a graded point vector, a probability-weighted diagnosis, engine credit, and feedback the student sees, with every parameter sourced or marked inferred.
---

# Diagnosis and Feedback

This document specifies the path from a submitted attempt to a changed mastery state and a feedback screen. It is the contract between the item the student saw, the registries in `data/`, the engine described in plan document 02, and the teaching thesis in plan document 01. Decisions D4 (feedback and diagnosis), D2 (mastery model and credit assignment), and D6 (assessment modes) in the decisions memo bind everything below; where this document adds a parameter that the memo did not fix, it says so and the parameter belongs in plan document 12 as a tunable.

Every number below carries its source URL and an evidence tag. A claim with no source is written as unknown rather than guessed. Anchor quotes from official material are capped at 25 words, consistent with the library rule in `research/README.md`.

## Pipeline overview

The pipeline has five stages, and the separation between them is the point. Grading decides what the rubric says. Diagnosis decides what the response reveals. Credit assignment decides what the model believes. Feedback decides what the student is told. Scheduling decides when the item comes back. Collapsing any two of these produces a system that cannot be audited when it is wrong, and the published agreement figures for rubric grading say it will be wrong often enough to matter (question-level exact agreement at most 0.22 on one small study, https://arxiv.org/html/2607.01247 [single-source]; best quadratic weighted kappa 0.56 on the strongest prompt-optimisation result, https://arxiv.org/pdf/2603.00451 [single-source]).

```
  student attempt
        |
        v
  [0] capture gate
      paper photo -> image quality check -> transcription -> rendered read-back
      typed MathLive -> MathJSON
      MCQ -> option id
        |
        | student confirms or corrects the read-back  (D6)
        v
  [1] GRADER  (one structured call per BC-PT, plus deterministic pre-checks)
      SymPy equivalence / numeric to three decimals / bounds / units
        -> mechanical points decided deterministically
      model judges justification, interpretation, notation points
        2 samples at temperature 0 + 1 strictness-varied sample
        -> GraderOutput: per point earned | not_earned | uncertain
        |
        | any disagreement -> review_queue, point shown provisional
        v
  [2] DIAGNOSTICIAN  (one call per attempt on a recurring BC-ERR path; see below)
      input: point vector + confirmed work + archetype + skills + item metadata
      matches observed behaviour against data/errors.json (BC-ERR)
        -> observed_errors[]
      expands each error through possible_misconceptions (BC-MIS)
        and non_conceptual_causes
        -> candidate_misconceptions[] with probabilities, never one at 1.0
      walks data/prereq_edges.csv over hard_prerequisite edges
        -> prerequisite_gaps[] with depth
      selects a mastery_state per skill, preferring a matched BC-SIG
        -> per_skill_mastery_state[]
        |
        v
  [3] ENGINE CREDIT  (deterministic, no model call)
      mastery_state -> c_k / f_k credit per D2
      FSRS grade -> stability and retrievability update
      prerequisite propagation over hard and supporting edges
      MCQ success discounted by the guessing floor
        |
        v
  [4] FEEDBACK AND SCHEDULING
      timing by fading stage and item shape (D4)
      elaborated feedback: rule violated + scoring consequence
      representation of the item first, then at most one translation
      one-line student error note
      requeue at 1 to 2 days; hypercorrection routing to 1 day
      discriminating probe written to pending_probes when the top two
        hypotheses are within 0.2, drained by 02's selection functions
```

Stage 0 exists because transcription, not rubric reasoning, is where the errors concentrate: in the 2026 AIED study of photographed handwritten STEM work, roughly 87 percent of the best model's remaining errors were transcription failures rather than rubric misapplication (https://arxiv.org/abs/2605.19043 [single-source]). A point lost to a misread exponent is the failure most likely to make a student stop trusting the app, so the read-back is shown and confirmed before any grading call is spent. That also follows D6, which makes paper the default free-response capture mode because the exam booklet is handwritten, boxed, unlined, and part-addressed (https://apcentral.collegeboard.org/media/pdf/ap-hybrid-digital-exams-free-response-booklets-overview.pdf [verified]).

Stage 1 and stage 2 are separate model calls with separate schemas because they answer different questions and fail differently. The literature does not settle whether folding transcription into grading is better than splitting it (the AIED study folded them and reported high rubric-item accuracy, https://arxiv.org/abs/2605.19043 [single-source]; track 3 also records that separate extraction-then-evaluate prompts let a model distinguish fully correct solutions from those needing human review). This plan splits them anyway, on the learning-impact argument that the student must be able to see which stage produced a wrong statement about their work, and on the auditability argument that a per-point trail can be disputed while a single number cannot.

Alternative rejected: a single call that reads the image, scores all nine points, and writes the feedback. It is cheaper by roughly a factor of the number of points per question and simpler to build. It is rejected because the one study that measures whole-exam behaviour reports best mean absolute error of 8.00 points at the whole-exam level and total-score exact agreement near zero for almost all conditions (https://arxiv.org/html/2607.01247 [single-source]), and because that study also documents operational failures that a monolithic call inherits: one model hit token and session limits requiring continuation, and another did not reliably handle the full dataset in one run (same URL [single-source]).

## Grading against point types

### Where per-point grading runs

Per-point grading runs only inside unit checks, part drills, mocks and the six-week checkpoint (R10). The daily micro-session serves multiple choice and MathLive short answers, both graded deterministically by the checks below, plus at most one short justification prompt. That justification prompt is read by the tutor role and answered as feedback only: it earns no point, it produces no BC-PT decision, and it writes nothing to `c_k` or `f_k`.

The reason is the cadence cost rather than the grading quality. Each per-point judged item costs printing, handwriting, a photograph, an image quality gate, a read-back confirmation and then a wait while the per-point calls resolve, and the resulting points are provisional often enough that the published agreement figures below cannot carry a daily ritual. Criterion practice at the checkpoint cadence keeps the exam-shaped writing that plan document 01 requires without spending that ritual every day.

### The unit of grading is one BC-PT call

`data/scoring_points.json` holds 76 point types (BC-PT), each carrying `earns`, `does_not_earn`, `requires_previous_work`, `setup_alone_earns`, `simplification_required`, `units_required`, `interpretation_required`, `justification_required`, `hypotheses_required`, `notation_requirements`, `precision_rules`, `dependency_on_other_points`, and `eligibility_after_error`. That record shape is a step-level rubric, and step-level supervision is the mechanism with the strongest published support for mathematical work: the PRM800K release contains 800,000 step-level labels over 75,000 solutions to 12,000 MATH problems, each step labelled positive, neutral, or negative, and process supervision outperformed outcome supervision (https://arxiv.org/abs/2305.20050 [verified], dataset at https://github.com/openai/prm800k [verified]).

So grading is one structured call per point type present on the item, not one call per question. A call receives the confirmed student work, the item's worked solution skeleton, the archetype id, and the full BC-PT record for exactly one point. It returns one decision.

Learning impact first: a per-point decision is a thing the student can argue with, and the elaborated feedback that Shute concludes beats verification-only feedback (https://journals.sagepub.com/doi/10.3102/0034654307313795 [verified]) needs a named rule and a named consequence, which a whole-question score does not supply. Cost second: on a nine-point question this is nine calls rather than one, mitigated by prompt caching and batching as described in plan document 04 and by the deterministic pre-checks below removing most points from the model path. Convenience last: it is more plumbing. Alternative rejected: one call per question with a JSON array of nine decisions, which saves the calls but merges nine decision surfaces into one context where a single early misreading contaminates the rest.

### Deterministic pre-checks decide the mechanical points

Before any model call, a deterministic checker runs against the confirmed work and the item's verified key. Four checks are in scope.

1. Symbolic equivalence with SymPy, for points whose `earns` text names an expression, an integrand, an antiderivative, or an equation. BC-PT-99002 (integrand only, limits assessed elsewhere) and BC-PT-99003 (antiderivative) are the clearest cases, and both records state their own tolerance: BC-PT-99003 earns with or without the constant of integration, per sg-25:14.
2. Numeric comparison to three decimal places, for reported-value points. The 2025 scoring guidelines general scoring notes state that decimal approximations should be accurate to three places after the decimal point (https://apcentral.collegeboard.org/media/pdf/ap25-sg-calculus-bc.pdf [verified]). That precision rule is checked against every reported value the item asks for. The same notes cap the penalty separately: within each individual free-response question at most one point is not earned for inappropriate rounding (same URL [verified]). The cap is therefore enforced per question and not per part, because the published language scopes it to the individual free-response question (R21).
3. Bounds match, for definite-integral points. BC-PT-99001 requires limits matching the requested interval, and the same record carries the eligibility rule that a definite integral with incorrect bounds earns neither that point nor the answer point (sg-22:18).
4. Units present and dimensionally correct, for BC-PT-99006 and its relatives. That record earns for correct units whether or not they are attached to a value, and does not earn when only units appear with no numerical approximation (sg-24:2, sg-22:13).

A point whose BC-PT record answers `no` to `justification_required`, `interpretation_required`, and `hypotheses_required`, and whose `earns` text is fully expressible as one of the four checks, is decided by the checker and never reaches a model. The model decides the rest: justification points, interpretation points, and notation points, which are the ones that require reading an argument rather than comparing an object.

This partition is the single highest-leverage design choice in the grader, because it removes from the unreliable path exactly the points the unreliable path is worst at pricing. Track 3's recommendation states it directly: anchor the ambiguous points with a deterministic check and use the model only where a student's argument must be read. Cost is a secondary gain, since a SymPy call is free relative to a frontier model call. The one caveat carries forward from track 3: SymPy equivalence is undecidable in general and returns unevaluated results on some expressions, so the fraction of BC-relevant expressions it can actually settle is unknown until measured, and an unsettled check falls through to the model path rather than defaulting to earned or not earned.

### What the model call sees, and why

Every judged point call is built from the BC-PT record fields, in this order.

- `earns` becomes the positive criterion, verbatim.
- `does_not_earn` becomes the negative criterion, verbatim. Including it is not decoration: the one study that isolates the leniency dial found that a strict baseline prompt "sometimes applied harsh point deductions" and that a liberal policy improved mean absolute error for every model tested (https://arxiv.org/html/2607.01247 [single-source]), which means strictness is a prompt-level parameter the app sets deliberately. Giving the model both sides of the boundary, in the rubric's own words, is how the boundary stops being the model's invention.
- `eligibility_after_error` becomes an explicit instruction about what earlier mistakes do and do not forfeit. This is the field with no published precedent: track 3 records that no source reports how LLM graders handle eligibility-after-error rules, which is a defining feature of AP rubrics and a plausible new failure mode. The mitigation is in the failure modes section below.
- `notation_requirements` becomes the notation clause, which is what makes a notation-only diagnosis possible downstream. BC-PT-99001's record accepts a missing differential for that point while restricting later eligibility (sg-23:8), and a grader that does not carry that sentence will either over-penalise or silently ignore it.
- `requires_previous_work`, `setup_alone_earns`, `simplification_required`, and `dependency_on_other_points` become the dependency preamble, so a point that the rubric makes conditional on an earlier point is not judged in isolation.

### Sampling, agreement, and escalation

Each judged point is sampled three times: two samples at temperature 0 with the standard prompt, and one sample with a strictness-varied prompt that states the stricter reading of `does_not_earn`. Agreement across all three publishes the decision. Any disagreement sets `decision` to `uncertain`, writes the point to `review_queue`, and shows it to the student as provisional.

Two samples at temperature 0 are not redundant, because structured decoding and server-side nondeterminism can still diverge; if they agree and the strictness-varied sample disagrees, that tells the app the rubric boundary is where the decision is fragile. Self-consistency, sampling several reasoning chains and taking the majority, produced large gains on arithmetic reasoning (GSM8K +17.9 percent, SVAMP +11.0, AQuA +12.2 over plain chain of thought, https://arxiv.org/pdf/2203.11171 [verified]), but those gains were measured on answer production, not on rubric judgement. Track 3's instruction is to treat majority voting here as a disagreement detector rather than an accuracy booster [inferred in track 3], and this plan adopts that reading: disagreement escalates, it never averages.

Alternative rejected: five samples with majority voting and no escalation. It would publish a decision on every point and remove the provisional state, which is more pleasant for the student. It is rejected on learning impact, because a confidently wrong point produces feedback that names the wrong violated rule, and the student then practises against a fiction. Cost is also against it, at five calls per judged point rather than three.

The evidence that makes escalation non-optional sits in two places. The 2026 rubric-grading study reports, on N = 28 student submissions, question-level Pearson correlations with human graders of 0.19 to 0.56, exact agreement at most 0.22, best mean absolute error 1.87 points and best RMSE 2.53 at question level (https://arxiv.org/html/2607.01247 [single-source]). The same study shows calibration and ranking diverging: the model-policy pair with the highest total-score correlation, 0.58, had the worst point calibration at 12.66 mean absolute error (same URL [single-source]). Separately, the strongest rubric prompt-optimisation result reports naive prompting at accuracy 0.51 and kappa 0.22, GradeOpt at 0.70 and 0.47, and CARO at 0.78 and 0.56, with individual tasks moving from kappa 0.28 to 0.57 and 0.31 to 0.46 (https://arxiv.org/pdf/2603.00451 [single-source]). Kappa 0.56 is moderate agreement. Neither study grades AP Calculus, and no published figure exists for LLM agreement with AP Readers on the nine-point scale, so the app must measure its own agreement against operator-graded golden responses as specified in plan document 10.

### Provisional display

A point with `decision` of `uncertain` renders as provisional: the student sees the point, the rule text it was judged against, the evidence quote taken from their own work, and a statement that the app could not decide it. The point is excluded from the score shown and excluded from engine credit until resolved. A one-click dispute path is available on every point, provisional or not, and a disputed point goes to the same review queue.

This is the honest surface of the agreement numbers above. The app is not licensed by any published result to score a nine-point AP rubric autonomously at a standard a student should trust, and saying so on the screen costs less than being caught.

### MCQ grading

Multiple-choice grading is deterministic: the selected option id is compared to the key. No model call is made. The selected distractor is passed to the diagnostician as an observation, because `common_distractors` on the archetype and the mechanism categories in `research/question-analysis/distractor-taxonomy.md` make the chosen option a diagnostic signal rather than a bare wrong answer. The taxonomy is explicit that no official rationale exists for any option in any of the three source documents, and that across 91 records and 318 option entries, 287 carry `inferred` and 31 carry `uncertain` with none `verified`, so a distractor-derived hypothesis enters the diagnosis with a lower prior than one derived from a rubric point.

## Mapping errors to candidate misconceptions

### Why the output is a distribution

`research/misconceptions/error-to-concept-map.md` states the relation plainly: the possible-misconceptions column is many to many in both directions, one error can sit under several misconceptions and one misconception can surface as several errors. `research/misconceptions/diagnostic-signals.md` closes with a section named "One error is not a diagnosis". Of 390 active BC-ERR records, 388 carry `possible_misconceptions` and all 390 carry `non_conceptual_causes` (counts computed 2026-09-19 from `data/` [verified, data/]), so every error in the corpus ships with a competing non-conceptual explanation such as time pressure, an arithmetic slip, or a misread of a table row.

So the diagnostician never emits a single cause with probability 1.0. It emits a ranked, probability-weighted list of BC-MIS candidates plus a list of non-conceptual causes, and the sum over the candidate misconceptions is strictly less than 1 with the remainder assigned to the non-conceptual explanation. D4 fixes this shape and this document does not vary it.

### Inputs the diagnostician uses

For each observed error the diagnostician reads:

- `errors.observed_behavior`, matched against the confirmed student work. This is the match key, not the error name.
- `errors.possible_misconceptions`, which supplies the candidate BC-MIS set.
- `errors.non_conceptual_causes`, which supplies the competing explanations, for example BC-ERR-01001 carrying "misread of an open circle; time pressure; copying the wrong row of a table".
- `errors.scoring_consequence`, which is what the feedback names as the cost, and which is often the sharper statement. BC-ERR-02001's consequence cites the rubric directly: the answer point requires both a difference and a quotient using values from the table, so a difference alone does not earn it (sg-25:11).
- `errors.discriminating_probe`, the follow-up item that separates this error from its neighbours.

For each candidate misconception it reads:

- `misconceptions.rival_misconceptions`, which names the competitors that produce a similar page. 210 of the active BC-MIS records carry rivals, and 213 carry a probe. The earlier 233 and 236 figures counted retired records.
- `misconceptions.discriminating_probe`, the question that separates the leading hypothesis from its rival. BC-MIS-99001's probe is a judgement about speed at an instant where velocity and acceleration are both negative, with the reason required.
- `misconceptions.causal_prerequisites`, which names the prerequisite or skill whose absence would produce the same surface behaviour. BC-MIS-99001 lists BC-PRQ-04005, BC-SKL-04007, BC-SKL-04008. The record's own `notes` field marks `causal_prerequisites` as [inferred], derived from the skills that list the misconception and from their prerequisites, with no source naming a causal relation directly, so a prerequisite-gap hypothesis raised through this field inherits that tag.
- `misconceptions.severity`, which is a prioritisation input for feedback ordering, not a probability.

### How probabilities are formed

The probability attached to each candidate BC-MIS is built from three multiplicative terms and then normalised against a reserved non-conceptual mass. All weights below are [inferred]; no source in any track supplies them, and they belong in plan document 12 as tunables.

1. **Skill prior.** Each skill loaded by the item carries a `misconceptions` list (482 of 541 active skills carry one). A candidate that appears on the misconception list of the skill the item's rubric point actually loads starts at a higher prior than one reached only through a second-hop skill. Starting values: 0.5 for a misconception listed on the primary skill of the failed point, 0.25 for one listed on a secondary skill of the item, 0.1 otherwise [inferred].
2. **Signal match.** If a BC-SIG record matches the observation, its `consistent_with` list names the skills and records the observation supports, and its `distinguish_by` text names the follow-up. A candidate named in a matched signal's `consistent_with` multiplies by 2.0; a candidate that the matched signal's `distinguish_by` text is designed to rule out multiplies by 0.5 [inferred]. The library holds 711 BC-SIG records, distributed across mastery states as partial_procedural 204, partial_conceptual 189, partial_unspecified 174, not_mastered 53, notation_only 50, prerequisite_gap 34, mastered 5, not_attempted 2 (computed 2026-09-19 from `data/diagnostic_signals.json` [verified, the registry]). Those counts matter downstream: `mastered` has only 5 signals, so a mastered state will usually be assigned from the engine's own criteria rather than from a matched signal.
3. **Confidence rating.** The student's pre-feedback 3-point confidence rating (guess, unsure, confident) is collected before any feedback is shown, per D4 and the calibration evidence in track 1 (Dunlosky and Rawson 2012, greater monitoring accuracy associated with higher retention, https://www.sciencedirect.com/science/article/pii/S0959475211000685 [verified]). A high-confidence error multiplies conceptual candidates by 1.5 and non-conceptual mass by 0.5; a "guess" rating does the reverse [inferred]. The reasoning is that a student who was confident and wrong is more likely to hold a belief than to have slipped, which is also why the corrected item routes to hypercorrection scheduling below.

The reserved non-conceptual mass starts at 0.3 and is raised to 0.5 when the error record's `non_conceptual_causes` list includes an explanation the item's own conditions make plausible, for example "time pressure" on an item served in a timed rehearsal block [inferred]. Timed sessions never update mastery state at all (D6, speededness contaminates ability estimates, https://pubmed.ncbi.nlm.nih.gov/31551639/ [single-source]), but their errors still feed the diagnostician for feedback, so this adjustment keeps the feedback honest about what a clock explains.

After multiplication the candidate weights are normalised to sum to one minus the non-conceptual mass. Nothing about this is calibrated; it is a ranking device with a stated shape, and plan document 10 specifies measuring error-type recurrence after diagnosis as the outcome that tells whether the ranking is doing work.

### Rival handling and the probe trigger

When the top two candidates are within 0.2 of each other in probability, the diagnostician sets `recommended_probe` to the archetype that exposes the leading candidate, taken from `misconceptions.exposing_archetypes`. The engine does not read that field directly. `recommended_probe` is written to the `pending_probes` queue on the user, and plan document 02's three selection functions (Item selection algorithm, in learning, review and diagnostic mode alike) drain that queue before running their own scoring, so a pending probe is served ahead of anything the score would have chosen (R6). The queue holds at most 3 entries and expires entries older than 7 days [inferred]. When the top two are rivals of each other (each appears in the other's `rival_misconceptions`), the probe is chosen from `misconceptions.discriminating_probe` text rather than from the exposing archetype, because the probe text is written specifically to separate them. The 0.2 threshold is fixed by D4 and is [inferred] there.

Alternative rejected: always probe. It would resolve more hypotheses, and it costs the student an item per diagnosis. Rejected on learning impact per minute, since the item it displaces would have been a scheduled retrieval, and track 1 ranks spaced retrieval above diagnosis-refinement work (Adesope et al 2017, weighted mean g = 0.51 versus restudy across 272 independent effects from 188 experiments, https://journals.sagepub.com/doi/abs/10.3102/0034654316689306 [verified]).

### A new error the library has not seen

If the confirmed work contains a behaviour that matches no active BC-ERR record above the match threshold, the diagnostician emits an entry in `observed_errors[]` with `error_id` null and `candidate` filled with a proposed record: a one-sentence `observed_behavior` written in the corpus's own voice, the skills the item loaded, the archetype, a proposed `scoring_consequence` taken from the BC-PT record whose point was lost, and a proposed `non_conceptual_causes` list. It carries `evidence_tag: "inferred"` and no `possible_misconceptions`, because linking a new error to a misconception is a library judgement and not a runtime one.

That candidate is written to the app's own `review_queue` and, on operator approval, exported as a staging file for the research library under `data/staging/`, to be merged by `tools/merge_staging.py` in the normal phase order and to receive a minted BC-ERR id from the appropriate two-digit unit block. It never gets an id at runtime. This keeps the app a consumer of the registries and the library the only minting authority, which is what the project's non-negotiable rules require. The app may use the candidate for feedback in the meantime, naming the scoring consequence but not naming a misconception it has not established.

## Prerequisite-gap tracing

### The walk

`data/prereq_edges.csv` holds 1226 edges over the skill and prerequisite graph: 602 `hard_prerequisite`, 622 `supporting`, 2 `co_requisite`, and 0 cycles (computed 2026-09-19 from `data/prereq_edges.csv` [verified, the file]). Tracing runs over the `hard_prerequisite` subgraph only. Supporting edges are not traced for gap hypotheses, because their semantics are weaker and treating all 1226 edges alike propagates false evidence (track 2's stated failure mode for knowledge-space methods [inferred there]).

The procedure, run per skill that the failed point loaded:

```
trace_gaps(failed_skills, observed_errors, candidate_misconceptions):
    frontier = failed_skills
    depth    = 0
    gaps     = {}

    while frontier and depth < 3:
        depth   += 1
        parents  = hard_prerequisite_parents(frontier)      # prereq_edges.csv
        for p in parents:
            score = 0.0

            # the skill's own gap description
            if text_match(skill(child_of p).adaptive.prerequisite_gap_if,
                          observed_work):
                score += 0.5

            # a candidate misconception names p causally
            if p in union(m.causal_prerequisites
                          for m in candidate_misconceptions):
                score += 0.3 * probability(m)

            # a matched signal carries mastery_state prerequisite_gap
            if matched_signal.mastery_state == "prerequisite_gap" \
               and p in matched_signal.consistent_with:
                score += 0.4

            # the model's own state for p
            score *= (1 - sigma(m_p))          # engine strength, plan doc 02

            gaps[p] = max(gaps.get(p, 0), score / depth)

        frontier = parents

    return sorted(gaps, by score desc)          # each with (id, depth, score)
```

Depth is capped at 3 hops. Track 2's propagation weights stop at 2 hops for credit (0.3 at one hop, 0.09 at two, per D2 [inferred]); the trace goes one hop further because a hypothesis is cheaper than credit, and the `/ depth` divisor keeps a three-hop ancestor from outranking a direct parent. The cap and the divisor are [inferred]. So are the three score increments inside the pseudocode above: the 0.5 on a `prerequisite_gap_if` text match, the 0.3 coefficient on a causal-prerequisite hypothesis, and the 0.4 on a matched `prerequisite_gap` signal are each [inferred], no source in any track supplies them, and all three belong in plan document 12 as tunables.

The gap-description term is the field written for this purpose. `skills.adaptive.prerequisite_gap_if` is prose describing what a prerequisite-driven failure looks like for that specific skill. For the skill shown in the sample record, the text names notation reading as the underlying break, cites BC-PRQ-06005, and gives the tell as the function and its derivative being used interchangeably in the sentence. That is a matchable description, and it is authored per skill rather than inferred by the model at runtime.

The causal-prerequisite term uses `misconceptions.causal_prerequisites`, weighted by the misconception's own probability so a weak hypothesis cannot promote a prerequisite on its own. As noted above, that field is tagged [inferred] in the records themselves, and a gap raised only through that term carries that tag into the output.

The signal term uses the 34 BC-SIG records whose `mastery_state` is `prerequisite_gap`. These are the strongest evidence available, because a signal is an authored observation-to-state mapping rather than a runtime inference. BC-SIG-03005, for example, records a response that stops at a correct differentiated equation without collecting the dy/dx terms, states `prerequisite_gap`, names BC-PRQ-03002, and gives the separating follow-up as presenting an already-differentiated equation and asking only for the algebra.

The engine-state term multiplies by the model's own disbelief in the prerequisite. A prerequisite the engine already scores as strong is a poor gap hypothesis, and a BC-PRQ prerequisite is assumed mastered until a diagnosed gap says otherwise, per D3.

### Output and consequences

The result is a ranked list, each entry carrying `prerequisite_id`, `depth`, and `probability`. Two things follow.

First, credit. Per D2, a diagnosed `prerequisite_gap` credits nothing to the target skill, charges 1.0 failure to the named prerequisite, and charges 0.3 of a failure to that prerequisite's hard dependants at one hop [inferred]. This is the credit-assignment rule that makes the diagnosis worth producing: a student who fails a chain-rule item because of an algebra gap should not lose chain-rule credit, and the engine cannot know that without the diagnosis.

Second, scheduling. When the top two hypotheses across the whole diagnosis, whether two misconceptions, two prerequisites, or one of each, are within 0.2 of each other, the discriminating probe of the leading hypothesis is written to the `pending_probes` queue, which 02's selection functions drain before scoring (R6, D4). A probe that resolves a prerequisite question is preferred over one that resolves a misconception question at equal probability, because a prerequisite gap blocks the fringe in plan document 02's selection policy and a misconception does not [inferred].

## Mastery-state assignment

Every diagnosis names exactly one mastery state per skill the item loaded, drawn from the enum used across the library and the engine: `mastered`, `partial_procedural`, `partial_conceptual`, `partial_unspecified`, `prerequisite_gap`, `notation_only`, `not_mastered`, `not_attempted`.

Assignment prefers a matched BC-SIG. A signal record carries `observation`, `mastery_state`, `consistent_with`, `distinguish_by`, `skill`, and `archetype`, so a signal match supplies the state, the supporting records, and the follow-up in one object, and it is authored evidence rather than a runtime judgement. When a signal matches, its `mastery_state` is used and its id is carried in `per_skill_mastery_state[].signal_id`.

When no signal matches, the state is assigned by rule, in this order:

1. `not_attempted` if the skill's points show no work at all. Nothing is credited (D2).
2. `prerequisite_gap` if the skill appears in `trace_gaps` output above the probe threshold and its own points failed. Credit goes to the named prerequisite, not to this skill.
3. `notation_only` if every point the skill loads failed on a `notation_requirements` clause and no other clause. This is a real and separate category in the corpus: 50 BC-SIG records carry it, and BC-PT-99001's notation clause (differential may be omitted, sg-22:2 accepts dx written for dt, sg-23:8 treats a missing differential as recoverable) is exactly the kind of failure that would otherwise be mislabelled as not mastered. Credit is 0.25 of a success (D2).
4. `partial_procedural` if the method chosen was correct and the execution failed, for example BC-SIG-01003, where the factorisation and cancellation are correct and the substitution value is wrong.
5. `partial_conceptual` if the execution was clean and the object produced was the wrong one, for example BC-SIG-04004, where the differentiation performed is correct and produces a quantity other than the one requested.
6. `partial_unspecified` when the response is partly right and the split between 4 and 5 cannot be made from the evidence. 174 signals carry this state, so it is not a failure of the taxonomy to use it.
7. `not_mastered` if every point the skill loads failed and no rule above applies.
8. `mastered` only when every point the skill loads earned. Note that `mastered` here is a per-attempt state, not the engine's `mastered` flag; the flag is declared only by the D2 criteria (sigma(m_k) >= 0.9, at least 3 credited unaided successes at stage unsupported, on at least 2 distinct archetypes, on at least 3 distinct calendar days spanning at least 7 days). The diagnostician can never declare a skill mastered; it can only contribute an observation toward the declaration.

Credit for the three partial states is asymmetric, per R2: `partial_procedural`, `partial_conceptual` and `partial_unspecified` each credit 0 to `c_k` and 0.5 to `f_k`, so no partial observation can raise `m_k`. That is an engine invariant in plan document 02's Update rules, not a convention this document may vary. `notation_only` keeps 0.25 to `c_k` because the mathematics was demonstrated and only the notation failed. The FSRS grade mapping is unchanged by R2.

### When the diagnostician is called at all, corrected 2026-09-20

The diagnostician runs on an incorrect attempt whose BC-ERR path has been seen before for this student, not on every incorrect attempt. On a first occurrence it does not run, and the attempt takes the rule-based assignment below.

The reason is this document's own rule rather than cost. All three parts of elaborated feedback are available without a model call: the rule violated comes from the BC-PT record or from the violated `expected_solution_path` step, the scoring consequence comes from `errors.scoring_consequence` or the BC-PT `does_not_earn` text, and what the correct response would have shown comes from the item's stored worked solution. What the diagnostician adds is a fourth thing, a probability-weighted ranking over candidate misconceptions, and this document already forbids surfacing that as an assertion, permitting it only as the discriminating probe. One observation does not separate a slip from a misconception, so on a first occurrence there is nothing to rank and a hypothesis drawn from it would be exactly the over-claim the Content section warns against. On a recurrence there is.

The cost consequence follows rather than leading: at an `[inferred]` recurrence share of 0.35 the role runs 564 times over the cycle rather than 1,610, and costs $8.21 rather than $20.51 (`14-token-economy.md`). What would overturn the trigger rule: `11-phased-delivery.md`'s diagnostician exit floor, two ranked hypotheses on at least 80 percent of diagnosed errors, together with the error-type recurrence rate measured with and without a first-occurrence diagnosis. If diagnosing the first occurrence measurably lowers recurrence, the trigger goes back to every incorrect attempt.

### Rule-based mastery_state assignment when the diagnostician does not run

P1 wires no diagnostician, a first occurrence of an error path does not call it, and any later phase can lose it to a provider outage or a budget cap. The rule below assigns a mastery state per loaded skill without any model call, and it is what P1 uses for every attempt. It is [inferred] in full (R12); no source supplies it and it belongs in plan document 12 as a tunable rule.

1. A correct answer at the served stage yields `mastered` for every skill the archetype loads. An MCQ success is credited at 0.75 before it reaches `c_k`, per the four-option guessing floor of 0.25.
2. An incorrect MCQ answer whose chosen distractor carries a BC-ERR path, meaning the selected entry of `items.options` has a non-null `error_path` (R26), yields `not_mastered` for the skills listed on that BC-ERR record, and `not_attempted` for every other skill the archetype loads.
3. An incorrect answer with no error path yields `not_mastered` for the archetype's first listed skill and `not_attempted` for the rest.
4. A MathLive answer that SymPy judges equivalent to the key but mis-notated yields `notation_only` for all loaded skills.

Nothing in this ladder produces `prerequisite_gap`, `partial_procedural`, `partial_conceptual` or `partial_unspecified`, because those four states are diagnostic judgements and a deterministic checker cannot make them. A phase running on this rule therefore never charges a prerequisite instead of a target skill, which is the specific capability the diagnostician buys back when it is wired.

The separation of procedural from conceptual partial states is the part of the enum that pays for itself, because it decides which remediation the engine schedules. Track 1's ranking of mechanics puts adaptive backward fading at rank 5 with the rule that stage advances on 2 consecutive correct and drops on 2 consecutive incorrect (Salden et al adaptive fading, http://www.cee.uma.pt/ron/Salden%20et%20al.%20-%20The%20Expertise%20Reversal%20Effect%20and%20Worked%20Examples.pdf [single-source]). Per R7 one counter pair owns every stage change: 2 consecutive credited successes at a stage advance it and 2 consecutive credited failures drop it, and nothing else moves `fading_stage`. So a procedural partial does not drop the stage by itself; it counts as a credited failure toward that counter, and the stage drops on the second consecutive one. A conceptual partial routes to the misconception's `remediation_target` instead, and un-mastery flips the `mastered` flag without touching the stage. `skills.adaptive.remediation_target` names that target per skill, and in the sample record it distinguishes the conceptual failure target from the case where the mathematics is right and only the sentence is short.

Counts to keep in view: 541 active skills carry a signals list, but only 31 skills are independently assessable by a single archetype, and typical archetypes load 3 to 6 skills (computed 2026-09-19 from `data/` [verified, data/]). So most attempts produce several per-skill states from one response, and the credit each receives is fractional in the sense that it is a per-skill judgement of a joint performance. Plan document 02 owns what happens to those numbers; this document owns only their assignment.

## Feedback policy

### Timing

Timing is set by the fading stage and the item shape, per D4.

- Stage `example` and stage `completion`: immediate step-level verification. The student finds out at each step whether the step is right. This is the acquisition phase and the intelligent-tutoring literature and Kulik and Kulik's field studies favour immediate correction there (https://journals.sagepub.com/doi/10.3102/00346543058001079 [single-source]).
- Stage `unsupported` and every exam-shaped item: no feedback of any kind until the whole item is submitted. Bangert-Drowns et al found that feedback helps only when it supplies correct-answer information the learner cannot already anticipate, and that pre-search availability can drive the effect to zero or negative (https://journals.sagepub.com/doi/10.3102/00346543061002213 [single-source]). Showing a correctness cue mid-item on an exam-shaped task destroys the retrieval attempt that is the point of the item.

Shute's conclusion is that the timing literature is inconsistent, with immediate feedback suiting procedural skill acquisition and delayed feedback suiting transfer (https://journals.sagepub.com/doi/10.3102/0034654307313795 [verified]), which is why this policy splits by phase rather than picking a side. Track 1's resolution, tagged [inferred] there, is that the delayed-feedback advantage largely dissolves once the immediate condition is also followed by a later retrieval, and the requeue rule below supplies that later retrieval in both branches.

### Content

Feedback on a lost point is elaborated, never verification-only, and it contains three things in this order.

1. **The rule violated**, in the BC-PT record's own language. Not "you were marked down" but the earning condition the response did not meet. Feedback names a BC-PT only when the item's archetype lists one (R14). 56 active archetypes carry no `point_types` at all, so for those the feedback names the step of `expected_solution_path` that the response violated, together with the BC-ERR path the diagnostician matched, and names no point type. Those archetypes are served only as multiple choice or short answer until the library fills `point_types`, which is why naming a step rather than a point loses nothing on them.
2. **The scoring consequence**, taken from `errors.scoring_consequence` where an error matched and from the BC-PT `does_not_earn` text otherwise. The corpus writes these in exam terms already, for example that a definite integral with incorrect bounds earns neither the integral point nor the answer point (sg-22:18), or that the continuity point requires the reason and a bare statement does not earn it (sg-25:12).
3. **What the correct response would have shown**, at the level of the step, not the whole solution.

**Who composes the string in P1 (R35).** The three parts above are selected deterministically, and the sentence that carries them is written by the tutor role. The application picks the violated `expected_solution_path` step, the `observed_behavior` and `scoring_consequence` fields of the option's BC-ERR record, and the item's stored worked solution, and passes exactly those into `prompts/feedback/elaborated_v1.md`. The tutor sees no other content, and it never receives the final answer before the student has submitted. So the selection is deterministic and the wording is model-written, which is the reading that makes the P1 wiring and the "feedback wording only" restriction on the tutor role the same statement rather than two.

Elaborated over verification-only is Shute's finding (https://journals.sagepub.com/doi/10.3102/0034654307313795 [verified]) supported by Bangert-Drowns et al (https://journals.sagepub.com/doi/10.3102/00346543061002213 [single-source]). Hattie and Timperley report an average feedback effect around d = 0.79 across syntheses while arguing the effect is highly variable and that feedback directed at the self does not help (https://journals.sagepub.com/doi/10.3102/003465430298487 [single-source]), which is the reason feedback here names the work and never the student.

Feedback never names a misconception as established. It may name the leading hypothesis as a question, in the form of the discriminating probe, because the probe is the thing that would settle it. An app that tells a student "you believe acceleration alone determines speeding up" when the diagnosis stands at probability 0.45 is asserting more than it knows.

### Representation and the one-translation rule

Feedback is shown first in the representation of the item itself, using the item's BC-REP code. When the leading candidate misconception's `exposing_archetypes` use a different representation, one translation is added and only one. Never more than two representations appear on a feedback screen.

The cap comes from cognitive load: the spatial contiguity and split-attention meta-analysis reports overall g = 0.63 favouring integrated over split presentation across 58 independent comparisons, n = 2426 (https://link.springer.com/article/10.1007/s10648-018-9435-9 [verified]), and the redundancy effect size is unknown. The translation is kept because the exam tests translation between the 14 representation types (BC-REP-01 to BC-REP-14) directly, and because Ainsworth holds that the benefit of multiple representations depends on whether the learner can translate between them, with unsupported multi-representation displays capable of hurting (https://nschwartz.yourweb.csuchico.edu/Ainsworth_2006_Learning-and-Instruction.pdf [verified]).

Every figure in a feedback screen carries its labels and the relevant algebraic step inside the figure, not in a caption, and no feedback screen requires scrolling between a figure and the text that refers to it. That is the same g = 0.63 result applied to layout.

### The student's one-line error note

Before the corrected item is requeued, the student writes one line saying why their attempt failed. It is free text, it is stored on the attempt, and it is the only free text the app stores about the student beyond their own work (D10).

The argument for asking is Nielsen on spaced repetition for mathematics: most of the value is in constructing the card rather than reviewing it (https://cognitivemedium.com/srs-mathematics [single-source]; a personal essay carrying no study, no n and no effect size, and no track ledger elevates it, per R20), so an app that auto-generates a review card from a diagnosed error is doing the low-value half. Structured self-explanation is the nearest measured mechanic, at g = 0.55 across 69 effect sizes from 64 reports (https://link.springer.com/article/10.1007/s10648-018-9434-x [verified]), and track 1 restricts such prompts to worked examples and corrected errors because math studies find they cost practice volume, which is why the note is asked here and not after correct answers.

### Requeue, hypercorrection, and the probe

Every item that received corrective feedback re-enters the queue at a 1 to 2 day gap (D4). The floor of one day comes from Cepeda et al 2008's optimal inter-study gap of about 20 percent of the retention interval for delays of a few weeks (https://journals.sagepub.com/doi/abs/10.1111/j.1467-9280.2008.02209.x [verified]) and from Roediger and Karpicke's demonstration that the testing advantage appears at a one-week delay and not at five minutes, 61 percent versus 40 percent (https://journals.sagepub.com/doi/10.1111/j.1467-9280.2006.01693.x [verified]).

An error made at high confidence sets a hypercorrection flag and the next due date to 1 day rather than 2. High-confidence errors are the most persistent and the most correctable once corrected (Butterfield and Metcalfe, https://www.columbia.edu/cu/psychology/metcalfe/PDFs/ButterfieldMetcalfe2001.pdf [single-source]); the effect size was not retrieved and is unknown. The 3-point scale and the 1 day gap are [inferred] per track 1.

A scheduled discriminating probe is not requeued at a gap. It goes to the `pending_probes` queue, and because every selection function in 02's Item selection algorithm drains that queue before its own scoring, the probe is served as the next item rather than at a delay (R6). Its purpose is to resolve a live ambiguity in the diagnosis, and a two-day delay lets the engine act on an unresolved distribution in the meantime. In 02's Session assembly the pending probe is served first in the fringe learning block.

### The tutor during practice

A guardrailed tutor is available beside a practice item and it never produces the final answer. The evidence is the Bastani field experiment over nearly 1,000 Turkish high-school mathematics students: during AI-assisted practice the plain chat condition outperformed control by 48 percent and the guardrailed tutor condition by 127 percent, but on the unassisted exam afterwards the plain-chat group scored 17 percent worse than control while the guardrailed tutor group was statistically indistinguishable from control (https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4895486 and https://pubmed.ncbi.nlm.nih.gov/40560616/ [single-source, the SSRN page returned 403 and the numbers come from the search-result summary]).

Guardrails are therefore a floor and not an upside: the best available outcome from in-practice assistance is parity. The tutor restates the prompt, names the representation, asks what the student has tried, and offers the next question the student could ask themselves. It does not evaluate in-progress work on an unsupported or exam-shaped item, because that is mid-item feedback, which the timing rule forbids. The tutor has no tools (D10) and its output is rendered as text or KaTeX and never treated as instructions.

Alternative rejected: a free chat box beside every item, which is the industry default and the cheapest thing to build. Rejected on the 17 percent number.

### What the student sees for a provisional grade

A provisional point renders with three elements: the point's rule text, the evidence quote the grader took from the student's own work, and a plain statement that the app could not decide the point and has sent it for review. It is excluded from the displayed score and from engine credit.

The dispute path is one control on every point. Pressing it writes the point to `review_queue` with the student's reason attached, marks the point provisional if it was not already, and reverses any engine credit the point produced. Reversal matters: a point credited and then disputed has already moved `c_k` or `f_k`, and leaving that in place means a grading error becomes a permanent distortion of the mastery state. The reversal is an explicit inverse of the credit operation recorded on the attempt, which is why every credit write records the attempt and point that produced it.

Score display never shows a predicted AP score as a number anywhere in feedback. The two inputs required, the section weighting and the composite-to-1-to-5 cut points, are both unpublished: College Board states the section totals "are combined to form a composite score" and that composites are translated to the 5-point scale, with no weights, no composite maximum, and no conversion table (https://apstudents.collegeboard.org/help-center/how-are-ap-exams-scored [verified]). Plan document 05 owns the score-band rules.

## JSON schemas

Both schemas are the structured-output contracts for their model calls. Anthropic structured outputs support objects, arrays, enums, anyOf, allOf and string formats, and do not support recursive schemas, minimum and maximum, or minLength and maxLength (https://platform.claude.com/docs/en/build-with-claude/structured-outputs [verified]), so neither schema below uses those keywords and both are validated in the backend after the call rather than relying on the provider for range checks.

### GraderOutput

One object per judged or checked point. A question produces an array of these.

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "GraderOutput",
  "type": "object",
  "required": ["attempt_id", "item_id", "points"],
  "properties": {
    "attempt_id": { "type": "string" },
    "item_id": { "type": "string" },
    "prompt_version": { "type": "string" },
    "points": {
      "type": "array",
      "items": {
        "type": "object",
        "required": [
          "point_type_id", "decision", "rule_cited",
          "deterministic_check_result", "samples_agree", "confidence"
        ],
        "properties": {
          "point_type_id": {
            "type": "string",
            "description": "BC-PT id from data/scoring_points.json"
          },
          "decision": {
            "enum": ["earned", "not_earned", "uncertain"]
          },
          "evidence_quote": {
            "type": "string",
            "description": "Verbatim span from the student's confirmed work that the decision rests on. Empty when the decision is not_earned for absence."
          },
          "rule_cited": {
            "type": "string",
            "description": "The clause of the BC-PT record applied, quoted from earns, does_not_earn, notation_requirements, precision_rules or eligibility_after_error."
          },
          "rule_field": {
            "enum": [
              "earns", "does_not_earn", "notation_requirements",
              "precision_rules", "eligibility_after_error",
              "dependency_on_other_points"
            ]
          },
          "deterministic_check_result": {
            "type": "object",
            "required": ["ran", "outcome"],
            "properties": {
              "ran": { "type": "boolean" },
              "check": {
                "enum": ["sympy_equivalence", "numeric_three_decimals",
                         "bounds_match", "units_present", "none"]
              },
              "outcome": {
                "enum": ["pass", "fail", "unsettled", "not_applicable"]
              },
              "detail": {
                "type": "string",
                "description": "Machine detail, for example the SymPy simplify result or the numeric difference."
              }
            }
          },
          "samples_agree": {
            "type": "object",
            "required": ["temp0_a", "temp0_b", "strict", "agree"],
            "properties": {
              "temp0_a": { "enum": ["earned", "not_earned"] },
              "temp0_b": { "enum": ["earned", "not_earned"] },
              "strict":  { "enum": ["earned", "not_earned"] },
              "agree":   { "type": "boolean" }
            }
          },
          "confidence": {
            "type": "number",
            "description": "0 to 1. Set to 1.0 when a deterministic check settled the point; set from sample agreement otherwise."
          },
          "eligibility_note": {
            "type": "string",
            "description": "Which earlier error, if any, the eligibility_after_error clause was applied to."
          },
          "provisional": { "type": "boolean" },
          "escalated_to_review": { "type": "boolean" }
        }
      }
    },
    "rounding_penalty_applied": {
      "type": "boolean",
      "description": "At most one per question, per the published general scoring note."
    }
  }
}
```

### DiagnosticianOutput

One object per attempt.

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "DiagnosticianOutput",
  "type": "object",
  "required": [
    "attempt_id", "item_id", "archetype_id",
    "observed_errors", "candidate_misconceptions",
    "non_conceptual_causes", "prerequisite_gaps",
    "per_skill_mastery_state", "feedback_plan"
  ],
  "properties": {
    "attempt_id": { "type": "string" },
    "item_id": { "type": "string" },
    "archetype_id": { "type": "string" },
    "prompt_version": { "type": "string" },

    "observed_errors": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["evidence", "matched"],
        "properties": {
          "error_id": {
            "type": "string",
            "description": "BC-ERR id, or absent when matched is false."
          },
          "matched": { "type": "boolean" },
          "candidate": {
            "type": "object",
            "description": "Proposed new error record when matched is false. Never receives an id at runtime.",
            "properties": {
              "observed_behavior": { "type": "string" },
              "skills": { "type": "array", "items": { "type": "string" } },
              "archetypes": { "type": "array", "items": { "type": "string" } },
              "scoring_consequence": { "type": "string" },
              "non_conceptual_causes": {
                "type": "array", "items": { "type": "string" }
              },
              "evidence_tag": { "enum": ["inferred"] }
            }
          },
          "evidence": {
            "type": "string",
            "description": "Verbatim span from the student's confirmed work."
          },
          "points_lost": {
            "type": "array",
            "items": { "type": "string", "description": "BC-PT ids" }
          }
        }
      }
    },

    "candidate_misconceptions": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["misconception_id", "probability", "basis"],
        "properties": {
          "misconception_id": { "type": "string" },
          "probability": { "type": "number" },
          "rival_of": {
            "type": "array",
            "items": { "type": "string" },
            "description": "BC-MIS ids from this record's rival_misconceptions that are also live candidates."
          },
          "basis": {
            "type": "array",
            "items": {
              "enum": ["skill_prior", "signal_match",
                       "confidence_rating", "error_link"]
            }
          },
          "signal_id": { "type": "string" },
          "severity": { "enum": ["low", "medium", "high", "unknown"] },
          "evidence_tag": {
            "enum": ["verified", "single-source", "inferred", "uncertain"]
          }
        }
      }
    },

    "non_conceptual_causes": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["cause", "probability"],
        "properties": {
          "cause": {
            "type": "string",
            "description": "Taken from errors.non_conceptual_causes where an error matched."
          },
          "probability": { "type": "number" }
        }
      }
    },

    "prerequisite_gaps": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["prerequisite_id", "depth", "probability"],
        "properties": {
          "prerequisite_id": {
            "type": "string",
            "description": "BC-PRQ or BC-SKL id reached over hard_prerequisite edges."
          },
          "depth": { "type": "integer" },
          "probability": { "type": "number" },
          "basis": {
            "type": "array",
            "items": {
              "enum": ["prerequisite_gap_if", "causal_prerequisites",
                       "signal_prerequisite_gap", "engine_state"]
            }
          },
          "blocks_skill": { "type": "string" }
        }
      }
    },

    "per_skill_mastery_state": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["skill_id", "mastery_state"],
        "properties": {
          "skill_id": { "type": "string" },
          "mastery_state": {
            "enum": ["mastered", "partial_procedural", "partial_conceptual",
                     "partial_unspecified", "prerequisite_gap",
                     "notation_only", "not_mastered", "not_attempted"]
          },
          "signal_id": {
            "type": "string",
            "description": "BC-SIG id when the state came from a matched signal. Absent when assigned by rule."
          },
          "assigned_by": { "enum": ["signal", "rule"] },
          "points_considered": {
            "type": "array", "items": { "type": "string" }
          }
        }
      }
    },

    "recommended_probe": {
      "type": "object",
      "description": "Written by the backend to the user's pending_probes queue, which plan document 02's selection functions drain before scoring. Never read from this object directly by the engine. The queue holds at most 3 entries and expires entries older than 7 days.",
      "properties": {
        "archetype_id": { "type": "string" },
        "reason": {
          "enum": ["top_two_within_0.2", "rival_pair",
                   "prerequisite_ambiguous", "none"]
        },
        "separates": {
          "type": "array",
          "items": { "type": "string" },
          "description": "The two hypothesis ids the probe is meant to separate."
        }
      }
    },

    "feedback_plan": {
      "type": "object",
      "required": ["representation", "rule_named", "scoring_consequence"],
      "properties": {
        "representation": {
          "type": "string",
          "description": "BC-REP id of the item, shown first."
        },
        "translation_representation": {
          "type": "string",
          "description": "BC-REP id of the single added translation, or absent. Never more than one."
        },
        "rule_named": {
          "type": "string",
          "description": "The BC-PT clause the feedback names."
        },
        "scoring_consequence": {
          "type": "string",
          "description": "From errors.scoring_consequence or the BC-PT does_not_earn text."
        },
        "ask_error_note": { "type": "boolean" },
        "requeue_gap_days": { "type": "integer" },
        "hypercorrection": { "type": "boolean" }
      }
    }
  }
}
```

## Failure modes and mitigations

**Leniency drift.** The one study that isolates it ran a strict baseline prompt against a liberal policy added after the baseline "sometimes applied harsh point deductions", and liberal prompting improved mean absolute error for every model tested (https://arxiv.org/html/2607.01247 [single-source]). Strictness is therefore a parameter the app sets, not a property the model has. Mitigations: the strictness-varied third sample makes drift visible as disagreement rather than as a silent shift; the prompt template is versioned in the repo with golden tests (D8); and the grader's per-point earn rate is compared against the published per-point means the 2025 Chief Reader report carries, which gives a population-level sanity check (track 3's recommendation). The comparison is a sanity check and not a calibration target, because the app's student population is one person.

**Hallucinated steps.** Named as a failure mode in the 2026 AIED handwriting study alongside poor image quality and mishandling of mathematically equivalent expressions (https://arxiv.org/abs/2605.19043 [single-source]). Mitigation: `evidence_quote` is required on every judged point and must be a verbatim span of the confirmed work. A quote that does not appear in the confirmed text fails a backend string check and the point escalates to review rather than publishing. Mathematically equivalent expressions are handled by the SymPy pre-check rather than by the model wherever the point type allows it, which is the direct answer to the third named failure.

**Transcription errors.** Roughly 87 percent of the best model's residual errors in that study were transcription rather than rubric misapplication (same URL [single-source]), and the FERMAT benchmark found several models scored better when the handwritten image was replaced with printed text, which isolates handwriting perception as a distinct bottleneck separate from math reasoning (2,200 handwritten solutions from 609 curated problems, best error-correction rate Gemini-1.5-Pro at 77 percent, https://arxiv.org/abs/2501.07244 and https://aclanthology.org/2025.acl-long.720/ [verified]). Mitigations: the image quality gate before any grading call; the rendered read-back the student confirms or corrects before a point is graded (D6); and a rule that a transcription correction by the student invalidates any grading already run on that attempt. The 77 percent figure is error correction on injected errors in grades 7 to 12 content, not partial-credit scoring on calculus, and is not used as a grading accuracy estimate.

**Eligibility-after-error rules.** Track 3 records that no source reports how LLM graders handle these, and that they are a defining feature of AP rubrics and a plausible new failure mode. The corpus makes them concrete: sg-24:4 states that if the limits of integration are incorrect the response does not earn the answer point, and that a response containing any linkage error can earn at most two of the three points in the part; sg-23:17 allows an antiderivative of the right form with a wrong constant to earn its point while blocking the answer point; sg-25:3 treats incorrect or unclear communication between the integral and the answer as scratch work, so bad linkage does not cost that point. Mitigations: eligibility is evaluated in the backend as a pass over the point vector after all per-point calls return, not inside any single call, so a model never has to hold nine interacting conditions at once; the pass is deterministic code driven by the `eligibility_after_error` and `dependency_on_other_points` fields; and `eligibility_note` records which earlier error was applied, so the student can see the chain. Whether per-point calls compound errors across nine decisions or contain them is untested in any source, so the golden-set measurement in plan document 10 is the only evidence the project will have.

**Long-context failures.** The same 2026 study documents one model hitting token and session limits requiring continuation and another not reliably handling the full dataset in one run (https://arxiv.org/html/2607.01247 [single-source]). Mitigations: never send more than one question's work to one call; persist each point result as it returns so a failure loses one point and not a section; batch by question for the batch API path, which gives 50 percent off both input and output with most batches finishing under an hour and all expiring at 24 hours (https://platform.claude.com/docs/en/build-with-claude/batch-processing [verified]); and cap image payloads against the documented vision limits of 10 MB per image on the Claude API and 32 MB per request (https://platform.claude.com/docs/en/build-with-claude/vision [verified]).

**Confidently wrong keys and confidently wrong diagnoses.** No source reports a confident-wrong rate for frontier models on AP-Calculus-level problems specifically; the AIME figures collated in track 3 describe a much harder distribution and imply nothing about a per-item error rate on a bank of generated BC items (track 3 [inferred]). For grading, the mitigation is the escalation rule. For diagnosis, the mitigation is that the output is a distribution with a reserved non-conceptual mass and a probe trigger, and that feedback never asserts a misconception.

**Over-diagnosis of a timed attempt.** Speeded conditions produce lower ability estimates than unspeeded conditions and rapid guessing at the end of a part is a documented behaviour (https://pubmed.ncbi.nlm.nih.gov/31551639/ [single-source]). Mitigation: timed sessions update pacing metrics only and never mastery state (D6), while their errors still feed the diagnostician for feedback, and the non-conceptual mass is raised on those attempts.

## Traceability to 01 and 02

Each policy below names the mechanic in plan document 01 or the engine rule in plan document 02 that it exists to serve.

| Policy in this document | Serves |
| --- | --- |
| Per-point grading against BC-PT records | 01 mechanic 6, elaborated feedback naming the rule violated; the rule cannot be named without a per-point decision |
| Per-point grading restricted to unit checks, part drills, mocks and the six-week checkpoint | 02 Session assembly, which owns block composition and the minute forecast a daily per-point ritual would break |
| Deterministic pre-checks with SymPy and the three-decimal rule | 01's criterion-alignment requirement that practice be scored the way the exam is scored; 02 Update rules, whose credit must not be driven by an unreliable signal |
| Two temperature-0 samples plus one strictness-varied sample, disagreement escalates | 02 Update rules, which must not consume a grading decision the app cannot stand behind |
| Provisional display and the dispute path with credit reversal | 02 Update rules and their mastery-state integrity: a reversed grade must reverse its credit |
| MCQ deterministic grading, distractor passed as an observation | 02 Update rules and their MCQ guessing correction, which discounts a correct MCQ response before crediting |
| Probability-weighted candidate misconceptions, never one certain cause | 01's error-registry mechanic, which requires the error and the misconception hypothesis to be separate linked records |
| Non-conceptual causes with reserved mass | 01's measurement criterion of a falling recurrence rate for a named error type, which is meaningless if slips are recorded as beliefs |
| Prerequisite-gap tracing over hard_prerequisite edges | 02 Prerequisite gating and the outer fringe, and its rule that an archetype is never served when its primary skill's hard prerequisites are unmastered outside 02 Cold-start diagnostic design |
| Mastery-state enum with a preferred BC-SIG match | 02 Update rules and their credit table, which maps each state to a c_k and f_k split and to an FSRS grade |
| Rule-based assignment when the diagnostician does not run | 02 Update rules, which need a state per loaded skill in P1 where no diagnostician runs, on a first occurrence of an error path, and whenever the role is unavailable |
| `notation_only` as a distinct state | 02 Update rules and their credit of 0.25 of a success, which exists so a notation habit does not read as a missing skill |
| Immediate step-level feedback in stages example and completion | 01 mechanic 5, adaptive backward fading; 02 Update rules, whose single counter pair advances a stage on 2 consecutive credited successes and drops it on 2 consecutive credited failures |
| Feedback withheld until submission on unsupported and exam-shaped items | 01 mechanic 3, practice testing as generation, which a mid-item cue destroys |
| Requeue at 1 to 2 days | 01 mechanic 2, the spaced retrieval queue; 02 Decay, whose FSRS stability update needs a scheduled next review |
| Hypercorrection routing to 1 day | 01 mechanic 7, confidence rating with high-confidence errors requeued first; 02 Decay and the `hypercorrection_due` date it reads |
| One-line student error note before requeue | 01 mechanic 8, structured self-explanation restricted to examples and corrected errors |
| Representation first, then one translation, labels inside figures | 01 mechanic 9, split-attention-free figure design; 02 Item selection algorithm and its 20 percent translation floor |
| Guardrailed tutor that never gives the final answer | 01's teaching thesis, which removes the chat box beside an unsolved problem |
| Discriminating probe written to `pending_probes` when the top two are within 0.2 | 02 Item selection algorithm, whose three selection functions drain the queue before scoring; 02 Session assembly, which serves a pending probe first in the fringe learning block |
| Diagnosed prerequisite gap charges the prerequisite, not the target skill | 02 Update rules and their prerequisite propagation; 02 Prerequisite gating and the outer fringe, which the charged prerequisite reopens |
