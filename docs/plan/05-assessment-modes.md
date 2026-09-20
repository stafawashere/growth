---
title: Assessment Modes
research_date: 2026-09-19
status: draft
purpose: The five assessment shapes the product serves, what each one measures, what it logs, which of them are allowed to move the mastery model, how free-response work is captured and graded, and what the product is willing to say about an AP score.
---

# Assessment Modes

This file specifies the shapes in which the student is assessed. The pedagogy behind them is in [01-learning-model.md](01-learning-model.md); the engine rules named here as D2 (mastery model), D3 (selection policy) and D4 (feedback and diagnosis) are implemented in [02-adaptive-engine.md](02-adaptive-engine.md). Grading prompts and diagnosis output live in [03-diagnosis-and-feedback.md](03-diagnosis-and-feedback.md), item generation and key verification in [04-item-generation.md](04-item-generation.md), screen design in [08-design-brief.md](08-design-brief.md), metrics in [10-quality-and-evaluation.md](10-quality-and-evaluation.md), and delivery order in [11-phased-delivery.md](11-phased-delivery.md), where assessment modes are phase P5.

Every exam count and timing below is taken from [research/exam/exam-structure.md](../../research/exam/exam-structure.md), which is the only file in the library permitted to state them. The numbers are restated here for readability and they come from that file, not from this one. Section I has 42 multiple-choice questions, split into Part A with 29 questions in 62 minutes with no calculator at 35 percent of the exam weight and Part B with 13 questions in 38 minutes with a calculator required at 15 percent. Section II has 6 free-response questions in 90 minutes, split into Part A with 2 questions in 30 minutes with a calculator required and Part B with 4 questions in 60 minutes with no calculator. Each free-response question carries 9 points, for 54 free-response points. Total testing time is 3 hours 10 minutes and the two sections carry 50 percent each. The administration is hybrid digital: multiple choice is answered in Bluebook, free-response prompts are viewed in Bluebook, and free-response answers are handwritten in paper booklets returned to the AP Program for scoring [single-source] https://apcentral.collegeboard.org/exam-administration-ordering-scores/administering-exams/digital-ap-exams/exam-modes and the hybrid arrangement is stated by College Board as continuing into 2027 [single-source] https://apcentral.collegeboard.org/exam-administration-ordering-scores/administering-exams/digital-ap-exams/hybrid-digital Per R20 both tags follow [research/exam/exam-structure.md](../../research/exam/exam-structure.md), which heads its digital delivery section [single-source]; track 3 found corroboration but the library file has not been updated, and the plan follows the library.

The organising decision across all five modes is that diagnosis and rehearsal are separate activities. Untimed and generously timed work feeds the mastery model, timed work does not. Under speeded conditions examinees receive lower ability estimates than under unspeeded conditions, and rapid guessing as time runs out is a documented behaviour [single-source] https://pubmed.ncbi.nlm.nih.gov/31551639/ . Mixing the two lets a pacing problem masquerade as a knowledge gap, which then routes the student to remediation they do not need.

## Micro-session

Purpose. This is where learning happens and it is the default use of the product. Its learning impact is the sum of the mechanics in [01-learning-model.md](01-learning-model.md): spaced retrieval, interleaving, mastery-gated fringe work and adaptive fading. It is the only mode whose job is to change what the student knows rather than to measure it or to rehearse a format.

Cadence. The session is available whenever the student opens the product and its length is a forecast of the assembled queue, about 45 minutes, never a schedule and never a quota. It ends when the four assembly blocks in [02-adaptive-engine.md](02-adaptive-engine.md) "Session assembly" are empty rather than on a timer. The forecast is computed from per-archetype median attempt time and is output of the engine, not input to it.

Response formats. Per R10 the micro-session serves multiple choice and MathLive short answers only, both graded deterministically, and per-point free-response grading does not run here. Criterion writing is still rehearsed: a micro-session may attach a one-sentence justification prompt, which the tutor role responds to as feedback and which carries no credit and moves no mastery state. Per-point free-response grading runs only inside unit checks, part drills, mocks and the six-week checkpoint, where the printing, capture, read-back and grading cost buys a measurement rather than a daily ritual.

What the student sees. One item at a time, one next action per screen. Support is whatever the skill's fading stage supplies: a fully worked example with one self-explanation prompt, a completion problem with the last step blanked, or a plain problem. A three-point confidence rating is collected after the student commits and before any feedback. Feedback is immediate and step-level at the supported stages and withheld until submission at the unsupported stage, then elaborated with the rule violated and the scoring consequence named. There is no calculator affordance unless the item's archetype allows one, and no chat box beside an unsolved problem.

What is logged. Per attempt: item id, archetype, variant, response format, fading stage, confidence, latency, the response, the deterministic grading result, the text of any justification prompt answer with its tutor feedback and an explicit no-credit marker, the diagnostician's output, and the resulting per-skill mastery states.

What updates the engine. Everything. D2 takes credit assignment and the FSRS update, D3 takes the next due dates and the fringe recomputation, D4 takes the diagnosis and schedules any discriminating probe.

Library IDs. Candidates are drawn from the 139 active BC-QA records in `data/archetypes.json` and their 395 BC-QV variants, filtered to the outer fringe computed over the `hard_prerequisite` edges in `data/prereq_edges.csv`. Diagnosis resolves to BC-SIG records in `data/diagnostic_signals.json`, for example BC-SIG-06001, and to BC-ERR and BC-MIS records for the feedback text.

Alternative rejected. A fixed daily problem set by unit, which is simpler to build and to explain. It was rejected because it cannot honour the spacing schedule, cannot enforce the interleaving constraints once several units are open, and cannot avoid serving items whose prerequisites are not in place, which is the condition under which a desirable difficulty stops being desirable.

## Unit check

Purpose. To close a unit honestly. The micro-session accumulates evidence skill by skill and can leave a unit with several skills whose evidence is thin because no archetype happened to load them. The unit check sweeps those, and because it is untimed its results are clean enough to move the model.

Cadence. Once when a unit's fringe-adjacent skills are all at or near mastery, and again on any unit whose six-week checkpoint performance falls below its internal mastery state.

What the student sees. Eight to twelve items spanning every fringe-adjacent skill of the unit, untimed, with feedback withheld until the whole check is submitted so the student cannot use one item's feedback to answer the next. After submission, a per-item breakdown and a per-skill summary of what moved.

What is logged. The same attempt record as a micro-session, plus a check-level record naming the unit, the skill coverage achieved, and which skills the check could not reach.

What updates the engine. Everything, as in a micro-session. This is the point of running it untimed.

Library IDs. Coverage is computed from the `unit` field on BC-SKL records and the `skills` array on candidate BC-QA records. Because only 31 of 541 active skills carry `independently_assessable: true`, most skills are reached only inside multi-skill archetypes, and the check is assembled as a set-cover over the unit's skills rather than one item per skill. Skills the cover cannot reach are recorded rather than silently skipped, which is the honest handling of a known library limit and is tracked in [12-open-questions.md](12-open-questions.md).

Alternative rejected. A timed unit quiz, which would look more like the exam and would have been cheaper because it reuses the timed-drill machinery. It was rejected because the unit check is the product's main untimed measurement instrument, and adding a timer would contaminate the one place where the mastery model gets a clean broad read of a unit.

## Timed section drill

Purpose. Pacing and stamina on the exact shape the exam uses. Speededness transfers poorly between tasks even when they are similar [single-source] https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7181559/ , so the rehearsal target is the specific part shape rather than generic timed practice. A 62-minute 29-question no-calculator block is the thing to practise because that is what the benefit appears to be specific to.

Cadence. One part drill every two to three weeks between full mocks, rising in the final eight weeks. No source establishes an optimal cadence for a three-hour-ten-minute exam, so this is [inferred] and tunable.

What the student sees. One part at its published shape, taken from [research/exam/exam-structure.md](../../research/exam/exam-structure.md): Section I Part A as 29 questions in 62 minutes with no calculator, Section I Part B as 13 questions in 38 minutes with a calculator, Section II Part A as 2 questions in 30 minutes with a calculator, Section II Part B as 4 questions in 60 minutes with no calculator. Section I numbering runs continuously across the Part A to Part B boundary, because the CED describes Part B as the final 13 questions of Section I rather than as a fresh numbering [verified, via research/exam/exam-structure.md].

The Bluebook tool set is reproduced rather than approximated, because a student who has rehearsed with a different tool set has rehearsed a different strategy. College Board documents a testing timer that can be hidden until a five-minute alert, a Desmos calculator on certain AP exams, a reference sheet, highlights and notes, mark for review, a line reader, an option eliminator, a question menu showing skipped and flagged questions, and zoom [verified] https://bluebook.collegeboard.org/students/tools . The drill provides the hideable timer with the five-minute alert, highlight and notes on the stem, mark for review, the option eliminator on multiple choice, the question menu, and zoom. The Desmos-equivalent panel appears only on calculator parts. The line reader is provided as an accessibility affordance in [08-design-brief.md](08-design-brief.md) rather than as a fidelity feature.

The reference sheet is treated as absent. Bluebook's tools page states generically that a reference sheet with commonly used formulas appears on all tests with math questions, but that page is written for the SAT suite as well as AP and names no Calculus exam, and neither [research/exam/exam-structure.md](../../research/exam/exam-structure.md) nor [research/exam/calculator-policy.md](../../research/exam/calculator-policy.md) nor the CED nor the scoring guidelines mentions one [uncertain]. Building on the assumption that no sheet is supplied is the conservative direction: if a sheet does exist, the student is over-prepared rather than under-prepared.

What is logged. Per question: response, correctness, time on question, revisits, whether it was marked for review, whether the option eliminator was used, and the position of the question within the part. Per part: total time used, time remaining at completion, and the per-question time series.

What updates the engine. Pacing metrics only. Mastery state does not move. The graded errors do reach D4, so the student gets diagnosis and elaborated feedback, and any item corrected here re-enters the queue at the usual short gap. That is the single path from a timed session back into the learning loop, and it deliberately carries feedback without carrying ability evidence. A timed mock that returns only a score leaves most of the available benefit unclaimed, since feedback is among the moderators that strengthen the testing effect [verified] https://pubmed.ncbi.nlm.nih.gov/25150680/

Library IDs. Items are generated from BC-QA records filtered on `calculator_status`, which partitions the 139 active archetypes into 75 `no_calculator`, 27 `calculator` and 37 `either`. A no-calculator part draws only from `no_calculator` and `either`; a calculator part draws only from `calculator` and `either`. Unit representation across the drill is weighted by the BC-UNIT weights in [research/exam/exam-blueprint.md](../../research/exam/exam-blueprint.md).

Alternative rejected. A generic timed quiz of arbitrary length with a single global timer, which is far cheaper because one timer serves every mode. It was rejected because every fidelity cue College Board documents is attached to a part boundary: calculator availability, the on-screen direction, the printed booklet header, and the timer itself. A drill that blurs the boundary rehearses a test that does not exist.

## Full-length mock exam in the 2027 format

Purpose. Stamina across 3 hours 10 minutes, the section and part transitions, and a single comparable measurement point against published distributions. Nothing else in the product exercises the transition from a 62-minute no-calculator block into a 38-minute calculator block, and that transition is where calculator-mode errors concentrate.

Cadence. Every four to six weeks, more often in the final eight weeks. [inferred], tunable; no source gives an evidence-based mock cadence for AP exams, and the distributed-practice literature argues against massing them.

What the student sees. The four parts in order with their published counts and timings, the calculator control present only on the two calculator-required parts, the Bluebook tool set as above, and paper booklet pages for Section II. Between parts, a fixed break screen rather than a free pause, so the shape of the break is rehearsed too.

What is logged. Everything the part drills log, plus section-level and exam-level totals, the per-question free-response point vector, and the time of day the mock was taken.

What updates the engine. Pacing metrics, the score-positioning display, and D4 feedback. Mastery state does not move.

Library IDs. Free-response questions are assembled to match the shape of the published corpus: `data/frq_records.json` holds 249 parts across 2012 to 2026 with 227 carrying point totals, and the mock's six questions are built from BC-QA records whose `point_types` produce a 9-point structure. The 56 active archetypes carrying no `point_types`, listed in the repository facts memo, cannot appear as free-response questions until that gap is filled, which currently constrains which units can be represented in Section II of a mock. Multiple-choice distractors come from `common_distractors` on the archetype, each generated from a named BC-ERR path.

Alternative rejected. Using a released full exam as the mock, which would be maximally faithful and free. It was rejected on copyright grounds: College Board's permission instructions define commercial use to include test-prep settings, and the noncommercial classroom carve-out requires pages copied exactly, distributed as stand-alone documents and not incorporated into another interface, every condition of which an app violates by construction [verified] https://privacy.collegeboard.org/copyright-trademark/request-instructions . Released material is worked by reference at the six-week checkpoint described in [01-learning-model.md](01-learning-model.md), never served inside the product.

## Calculator-part handling

The calculator is not a setting the student toggles. It is a property of the part, and the control is removed rather than discouraged on the two no-calculator parts. College Board states that for Calculus, Desmos calculators will only be available in the calculator-required parts, and that only the Bluebook built-in Desmos counts rather than the web or app version [verified] https://apstudents.collegeboard.org/exam-policies-guidelines/calculator-policies . The paper booklet carries the same information from the other side: no-calculator pages carry a large header reading that no calculator is allowed, and students see the corresponding direction in Bluebook [verified] https://apcentral.collegeboard.org/media/pdf/ap-hybrid-digital-exams-free-response-booklets-overview.pdf

The product provides a Desmos-equivalent graphing panel on calculator parts only. Whether the Bluebook Desmos satisfies all four CED capabilities in the form the CED states them is unresolved, and [research/exam/calculator-policy.md](../../research/exam/calculator-policy.md) records it as unresolved [uncertain]. The four required capabilities are plotting a function in an arbitrary window, finding zeros, numerically calculating a derivative, and numerically calculating a definite integral, sourced to CED p.8 [verified, via research/exam/calculator-policy.md]. The panel supplies all four, which is the conservative direction, and the open question is recorded in [12-open-questions.md](12-open-questions.md).

Three rules ride on the calculator parts and each is enforced in grading rather than only mentioned in help text.

Radian mode. The 2025 Question 1 stem carries a parenthetical instruction that the calculator should be in radian mode [single-source] https://apcentral.collegeboard.org/media/pdf/ap25-sg-calculus-bc.pdf . An app whose panel has no mode setting silently drops that cue and trains a student who never thinks about it. The product therefore carries the note on calculator items whose archetype involves trigonometric evaluation, and the panel exposes an explicit mode indicator so the habit of checking it is rehearsed.

Setup shown. When a result is obtained using one of the four capabilities, the response must show the setup that leads to the solution along with the result [verified, via research/exam/calculator-policy.md]. This is carried in the stem, not only in the rubric: the 2025 Question 1 Part A prompt ends by telling the student to show the setup for their calculations, and the rubric splits the two points into an average value formula point and an answer point [verified] https://apcentral.collegeboard.org/media/pdf/ap25-sg-calculus-bc.pdf . The product carries `setup_required` as a first-class field on every calculator-part item and grades the setup point independently of the answer point, using BC-PT types such as BC-PT-99001 (definite integral expression with correct limits), BC-PT-99020 (average value formula) and BC-PT-99005 (answer with supporting work or setup shown).

Three decimals with a one-point cap. Per R21 the general scoring note is stated in two sentences rather than as one continuous span. On precision, decimal approximations should be accurate to three places after the decimal point, and either rounding or truncation is accepted [verified] https://apcentral.collegeboard.org/media/pdf/ap25-sg-calculus-bc.pdf . The penalty is capped: at most one point per free-response question is lost to inappropriate rounding, from the same source. The cap is per question, not per part, and the grader implements it that way: the rounding check runs on every point in a question, and if more than one point would fail on rounding alone, only the first such failure is applied and the rest are awarded. Answers need not be simplified, so the symbolic equivalence check must accept unsimplified forms, which is why the mechanical points are decided by SymPy equivalence rather than by string comparison.

## Free-response capture and grading

Purpose. The exam's free-response section is handwritten on paper. The booklet is question-addressed and part-addressed, with printed regions such as an instruction to answer Question 1 Parts A and B on a given page, it is unlined for Calculus, it is written in pencil or black or dark blue ink, students are told not to write outside the box, and erased or crossed-out work is not scored [verified] https://apcentral.collegeboard.org/media/pdf/ap-hybrid-digital-exams-free-response-booklets-overview.pdf . An app that accepts typed math as its primary mode trains a workflow that does not exist on exam day.

Cadence. Per R10, whenever a point-bearing free-response item is served, which is inside unit checks, part drills, mocks and the six-week checkpoint, and nowhere else. Micro-sessions do not serve point-bearing free-response items, so the capture, read-back and per-point grading path never runs in the daily loop. The reason is cost against value: the ritual below costs printing, handwriting, photographing, a quality gate, a read-back and a wait, and its result is provisional, which is worth paying at a measurement point and not worth paying daily.

What the student sees, in order.

First, a printable booklet-shaped answer page: boxed, unlined, addressed by question and part, with a calculator-status header matching the part. Second, the capture step, a photo of the completed page. Third, an image quality gate that runs before any grading call is spent, checking blur, crop, contrast and page-marker detection. Poor image quality is a named failure mode in two of the applied studies, so capture failure is budgeted as a routine event rather than an exception [single-source] https://arxiv.org/abs/2605.19043 . Fourth, a transcription read-back: what the system read, rendered as math, which the student confirms or corrects before any point is graded. Fifth, per-point grading and elaborated feedback.

The read-back is the most important step in this file. In a 2026 AIED study grading photographed handwritten university STEM work against instructor rubrics, roughly 87 percent of the best model's remaining errors were transcription failures rather than rubric misapplication [single-source] https://arxiv.org/abs/2605.19043 . The FERMAT benchmark, covering over 2,200 handwritten math solutions from 609 curated problems, found several models scored better when the handwritten image was replaced with printed text, which isolates handwriting perception as a distinct bottleneck from mathematical reasoning [verified] https://arxiv.org/abs/2501.07244 . A rubric point lost to a misread exponent is the most trust-destroying failure this product can produce, and the read-back is what prevents it.

Typed input is the secondary mode. MathLive with MathJSON export is used for numeric answer boxes, short answers, multiple-choice-adjacent input and accessibility. MathJSON rather than a LaTeX display string is what the verifier consumes, because it maps cleanly onto a symbolic check [verified] https://mathlive.io/mathfield/ . MathQuill was not considered, since its public repository is now published as an archive, which is a maintenance signal against new work [single-source] https://github.com/desmosinc/mathquill-archive

Grading structure. One structured call per BC-PT scoring point, not one call per question. Deterministic pre-checks decide the mechanical points first: SymPy equivalence for closed-form answers, numeric comparison to three decimals, bounds matching, and presence of units. The model decides only justification, interpretation and notation points. Each judged point is sampled twice at temperature 0 and once under a strictness-varied prompt, and disagreement escalates to the review queue rather than being averaged, because that is precisely the population where the literature says the model is unreliable.

The scores are shown as provisional with a visible confidence and a one-click dispute path, and the product does not claim autonomous grading. The published numbers do not support that claim: one 2026 study of LLMs grading a mathematics exam against a rubric reports question-level correlations with human graders of 0.19 to 0.56, exact agreement at most 0.22, best mean absolute error 1.87 points at question level, and total-score exact agreement near zero for almost all conditions, on N = 28 submissions [single-source] https://arxiv.org/html/2607.01247 . Confusion-aware rubric optimization reaches accuracy 0.78 and kappa 0.56 against 0.51 and 0.22 for naive prompting, and 0.56 is moderate agreement, not human equivalence [single-source] https://arxiv.org/pdf/2603.00451 . The same body of work shows strictness is a prompt-level dial with a measurable effect, since a liberal policy prompt improved mean absolute error for every model tested, which is why the strictness prompt is a deliberately set and calibrated parameter rather than a default.

What is logged. The image, the transcription, the student's read-back corrections, the per-point decisions with their sampling agreement, the deterministic pre-check results, and the diagnosis. Images are deletable and are purged on the retention schedule in [09-security-and-privacy.md](09-security-and-privacy.md).

Two of these fields feed learning-outcome metric 9 in [10-quality-and-evaluation.md](10-quality-and-evaluation.md), added by R11: free-response items attempted per week, and the read-back abandonment rate, meaning captures started where the confirm step was never pressed. The second exists because the ritual's predictable failure is avoidance rather than error, and nothing else in the metric set would see it.

What updates the engine. In a unit check, everything. In a part drill, a mock or the six-week checkpoint, D4 only.

Library IDs. Grading runs against the 76 BC-PT records in `data/scoring_points.json`, with `earns`, `does_not_earn`, `eligibility_after_error` and notation requirements read per point. For BC-QA-06001 that is BC-PT-99018, BC-PT-99019, BC-PT-99022, BC-PT-99026 and BC-PT-99007. Diagnosis maps the observed work onto BC-ERR records in `data/errors.json` and their `possible_misconceptions`, present on 388 of 390, and onto BC-SIG records for the per-skill mastery state.

Alternative rejected. A stylus canvas with commercial digital-ink recognition, using Mathpix or MyScript. It was rejected on all three criteria. On learning impact it trains a gesture that does not occur on the exam, where the artefact is paper. On cost it is the only path requiring a commercial contract with undisclosed pricing, since MyScript publishes no tiers, whereas Mathpix image OCR lists at 0.002 USD per image [verified] https://mathpix.com/pricing/api . On convenience it adds a hardware requirement. A second alternative, folding transcription and rubric evaluation into a single model call as the 2026 AIED study did, was rejected for the read-back reason above: a single call gives the student nothing to correct before a point is lost. Both designs are defensible in the literature and it does not settle which wins, so the product chose the one whose failure mode is visible to the student.

## Pacing metrics and rapid-guessing detection

Pacing is reported as its own metric and never folded into a score. The published part boundaries give a concrete exam-derived target rather than an invented one: 62 minutes for 29 questions, 38 for 13, 30 for 2, and 60 for 4, all from [research/exam/exam-structure.md](../../research/exam/exam-structure.md). The implied per-question budgets follow directly from those pairs and are computed rather than stated here, so that a change to the structure file propagates instead of being duplicated.

| Metric | Definition | Source of the target | Tag |
|---|---|---|---|
| Per-question time | Seconds from item render to submission, excluding revisits | derived from part shape | [verified] shape, [inferred] budget split |
| Part time used | Seconds consumed against the part's published limit | research/exam/exam-structure.md | [verified] |
| Time remaining at completion | Seconds left when the last question was answered | research/exam/exam-structure.md | [verified] |
| Rapid-guessing flag | An item answered faster than a per-archetype threshold, clustered in the final minutes of a part | rapid guessing is documented behaviour | [single-source] |
| Rapid-guessing rate | Flagged items as a share of the part | no published threshold | [inferred], tunable |
| Revisit rate | Share of items returned to after first submission | no published value | [inferred] |

The rapid-guessing threshold is per archetype rather than global, set from the archetype's own observed latency distribution once enough attempts exist and from its `difficulty_factors` count before that. A global threshold would flag fast correct answers on easy archetypes and miss slow guessing on hard ones. The flag is surfaced to the student, because switching from problem solving to fast near-random responding as time runs out is a real and correctable behaviour, and it is surfaced as a pacing observation rather than as a criticism.

Flagged items are excluded from the pacing averages they would otherwise distort, and they are excluded from D4 diagnosis as well, because diagnosing a misconception from a guess produces a confident wrong story about the student's mind.

## What feeds the mastery model and what does not

| Mode | Updates D2 mastery state | Updates D3 scheduling | Feeds D4 diagnosis and feedback | Feeds pacing metrics |
|---|---|---|---|---|
| Micro-session | yes | yes | yes | no |
| Unit check | yes | yes | yes | no |
| Timed part drill | no | corrected items only | yes | yes |
| Full mock | no | corrected items only | yes | yes |
| Six-week released-material checkpoint | no | no | yes | yes |

The rule has one rationale and it is worth stating once rather than in each row. Speededness biases the measurement, so an ability estimate taken under a timer is an estimate of a partly different construct [single-source] https://pubmed.ncbi.nlm.nih.gov/31551639/ . Letting it into D2 would mean a student who knows the material but paces badly gets routed back through remediation for skills they hold, which costs the scarcest resource the product has. The corrected-items exception exists because an error the student has now been shown and corrected is a learning event regardless of the conditions that produced it, and requeueing it at a short gap converts the correction into a spaced exposure. The checkpoint updates nothing at all, because an instrument that trains the model it measures stops being an instrument.

## AP score estimate

The product does not show a predicted AP score as a number. The two inputs required to compute one are both unpublished. College Board states that the free-response and multiple-choice results are weighted and combined into a composite and that the composite is translated to the 1 to 5 scale, with no weights, no composite maximum and no conversion table on any of its scoring pages [verified] https://apstudents.collegeboard.org/help-center/how-are-ap-exams-scored , and [research/exam/scoring-system.md](../../research/exam/scoring-system.md) records the same absence against the CED. Cut scores are not published for any year in the corpus, and standard setting is moving to Evidence-Based Standard Setting, which places cut points from data linking AP performance to college-student performance rather than from a fixed curve [single-source] https://allaccess.collegeboard.org/2025-ap-exams-scoring-standards-and-security-new-digital-era . On top of that, the 2027 form carries the revised Section I counts, so no published distribution corresponds to the structure the product simulates.

What the product does show is a band, labelled an estimate, with its assumptions on the same screen rather than in a footnote. The assumptions are stated in the product's own words as: section weighting assumed equal at the published 50 percent each [verified, via research/exam/exam-structure.md]; cut points unpublished and therefore estimated; multiple-choice scoring as the count of correct answers with no guessing penalty [single-source, via research/exam/scoring-system.md]; uncertainty at least one full score point; and the 2027 form new, so no prior year's distribution matches its structure.

```
# Inputs
mcq_correct        : integer, 0 to 42
frq_points         : integer, 0 to 54, sum of per-question 9-point vectors
section_weight     : 0.50 each, from research/exam/exam-structure.md  [verified]
cut_points         : unknown, not published                            [verified absence]

# Composite on a 0 to 1 scale, weighting the two sections equally
mcq_share  = mcq_correct / 42
frq_share  = frq_points  / 54
composite  = 0.50 * mcq_share + 0.50 * frq_share

# The band is NOT a cut-point lookup. It is a comparison to published outcomes.
# Position the composite against the three published BC distributions, then
# widen by the stated uncertainty of at least one full score point.
band_centre = position_against_published_distribution(composite, years = [2023, 2024, 2025])
band        = (band_centre - 1, band_centre + 1)   # at least one score point either side

# Refuse to emit a point estimate. band_centre is internal and is never displayed (R24).
display(band, assumptions = [equal_section_weight, cut_points_unknown,
                             no_guessing_penalty, form_revised_for_2027])
```

The `position_against_published_distribution` step is the honest half and it is specified in the next section. The band is never narrowed below two score points wide.

Per R24 the rule is stated as no centre rather than only as no single number. `band_centre` is an intermediate value inside the computation above and it is never displayed, never logged to a student-facing surface and never named in copy. What the student sees is the band with its assumptions, and the per-question comparison against the published means in the next section. A centre shown beside a band would be a predicted score with error bars, which is the thing this section refuses, and its narrowness would be an artefact of the composite rather than evidence about the unpublished cut points.

## Percentile-style positioning against published distributions

Both sides of this comparison are real published numbers, which is what makes it honest where a score prediction is not. The figures below are reproduced from [research/exam/scoring-system.md](../../research/exam/scoring-system.md), sourced there to the College Board distribution PDFs [verified].

The BC score distributions, at the precision published. 2023, N = 135,458, 43.55 percent scoring 5, 78.45 percent scoring 3 or higher, mean 3.75, SD 1.32. 2024, N = 148,191, 47.7 percent scoring 5, 80.9 percent scoring 3 or higher, mean 3.92, SD 1.27. 2025, N = 160,954, 43.9 percent scoring 5, 78.6 percent scoring 3 or higher, mean 3.82, SD 1.30.

The per-question free-response means, out of 9 points on every question in all three years, are the more useful comparison because they are per question rather than per exam. The 2025 means run 5.22, 3.09, 6.27, 5.46, 5.21 and 4.32 across Questions 1 to 6; 2024 runs 6.45, 5.56, 5.57, 5.84, 5.92 and 3.38; 2023 runs 5.26, 5.20, 3.74, 4.03, 4.71 and 4.21. The lowest single-question mean in the window is 3.09 on 2025 Question 2 and the highest is 6.45 on 2024 Question 1. Implied section totals are 27.15 of 54 in 2023, 32.72 in 2024 and 29.57 in 2025.

The product displays the student's per-question free-response mean against these, position by position, and the whole-exam composite against the distribution shape. It does not convert either into a percentile of the national cohort, because that conversion needs the raw-to-composite mapping that is not published.

The strongest comparison available is finer still. The 2025 Chief Reader report prints a mean for each of the nine individual scoring points on each question, separately for AB and BC, for example BC1 point 5 at 0.84 and BC1 point 8 at 0.18 against an overall BC1 mean of 5.22 [verified, via research/exam/scoring-system.md]. Because the product grades per BC-PT point type, it can tell the student that they are missing the specific point types most students also miss, or failing ones most students earn. That is better sourced and more actionable than a predicted 4. Per-point means exist only for 2025 in the cache, and whether College Board continues publishing them is unresolved, so this display degrades gracefully to whole-question means for other years.

Alternative rejected. Fitting a composite-to-score model against third-party reconstructions of past cut points, which is what most test-prep products do and which would let the product print a single number. It was rejected on learning impact first: a fabricated score invites the student to optimise a number that does not measure them, and the failure is silent because nothing in the product can detect that the fit is wrong. It was rejected on correctness second: the boundaries are unpublished, the standard-setting method is changing, and the 2027 form is structurally new, so the fit would be to a form that no longer exists.

## Open items this file depends on

Four uncertainties in the research library affect these modes directly and are carried into [12-open-questions.md](12-open-questions.md). Whether AP Calculus BC receives a Bluebook reference sheet is unresolved and changes what the item bank may assume. Whether the Bluebook Desmos satisfies all four CED capabilities is not stated by any cached source. The 2027 booklet layout under the revised 42-question Section I is an assumption, since full-length 2027 sample booklets were promised for early 2027 and are not yet available. And 56 active archetypes carry no `point_types`, which currently limits which units can supply free-response questions to a mock or a unit check.
