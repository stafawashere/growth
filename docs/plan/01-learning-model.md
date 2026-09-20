---
title: Learning Model
research_date: 2026-09-19
status: draft
purpose: The pedagogical specification for the adaptive AP Calculus BC tutor. One section per product mechanic, each with its evidence, its parameters and their sources, the library records it consumes, the engine rule that implements it, and the metric that tells us whether it worked.
---

# Learning Model

This file states what the product does to a student's mind and why. The computational half is [02-adaptive-engine.md](02-adaptive-engine.md), which implements the rules named here under the labels D2 (mastery model), D3 (selection policy) and D4 (feedback and diagnosis). Feedback rendering sits in [03-diagnosis-and-feedback.md](03-diagnosis-and-feedback.md), item generation in [04-item-generation.md](04-item-generation.md), assessment shapes in [05-assessment-modes.md](05-assessment-modes.md), metrics in [10-quality-and-evaluation.md](10-quality-and-evaluation.md). Every parameter marked tunable is carried forward in [12-open-questions.md](12-open-questions.md). Scope and non-goals are in [00-executive-summary.md](00-executive-summary.md).

The thesis: the scarcest resource is the student's minutes, spent in this priority order, mastery-gated practice at the outer fringe of the prerequisite graph, interleaved and spaced retrieval scheduled to the exam date, worked examples faded adaptively per skill, and criterion-shaped rehearsal at a low fixed cadence. The expectation is d = 0.4 to 0.7 against a standardized criterion, not two sigma.

Tags are taken from the evidence ledgers. [verified] means a primary source or abstract carried the number, [single-source] one secondary page, [inferred] an extrapolation to this product that nothing published supports. Exam counts and timings are stated only by reference to [research/exam/exam-structure.md](../../research/exam/exam-structure.md).

## Interleaving

### Evidence

- Rohrer, Dedrick, Hartwig and Cheung 2020, J Educ Psych 112(1). 787 students, 54 classes, randomized. Delayed test one month later: 61 percent interleaved against 38 percent blocked, d = 0.83, CI [0.68, 0.97]. [verified] http://uweb.cas.usf.edu/~drohrer/pdfs/Rohrer_et_al_2020JEdPsych.pdf
- Rohrer, Dedrick and Stershic 2015, J Educ Psych 107(3). 80 against 64 percent at one day, 74 against 42 percent at one month. [single-source] http://uweb.cas.usf.edu/~drohrer/pdfs/Rohrer_et_al_2015JEdPsych.pdf
- Rohrer, Dedrick and Burgess 2014, Psychon Bull Rev 21. 72 against 38 percent, d = 1.05. [single-source] https://link.springer.com/article/10.3758/s13423-014-0588-3
- Brunmair and Richter 2019, Psych Bulletin. 59 studies, 238 effect sizes, overall g = 0.42, largest for mathematics, near zero or negative for expository texts. [verified] https://pubmed.ncbi.nlm.nih.gov/31556629/

Brunmair and Richter is the contradicting work and it does not contradict the application: interleaving pays when the problem is discriminating among confusable strategies, which is the defining BC failure mode.

### The mechanic

After a unit's first blocked, example-heavy pass, every subsequent set is interleaved. No more than two consecutive items share a primary skill, and each block of ten draws from at least four skills spanning at least two units once two units are open. Antiderivative technique and series convergence tests get a named method-selection drill where the student sees only the expression and must name the method before executing it.

### Parameters

| Parameter | Value | Source | Tag |
|---|---|---|---|
| Planning effect size | d = 0.83 classroom math RCT | Rohrer et al 2020 | [verified] |
| Cross-material effect | g = 0.42 | Brunmair and Richter 2019 | [verified] |
| Max consecutive same-skill items | 2 | no published value | [inferred], tunable |
| Distinct skills per block of ten | at least 4 | no published value | [inferred], tunable |
| Distinct units per block of ten | at least 2 once 2 units open | no published value | [inferred], tunable |
| Translation share of a set | at least 20 percent | no published value | [inferred], tunable |
| Random-within-fringe exploration | deferred, 0 until P7 reports | Pelanek and Gervet feedback-loop warnings | [inferred], tunable |

Exploration is not pedagogical. A policy that only serves what it believes is near target trains on its own beliefs, and it is listed here because it costs student minutes. Per R4 the dedicated exploration share is deferred: selection in P1 and P2 chooses uniformly at random inside the fringe, which supplies the same coverage without a separate budget, and `EXPLORE_SHARE` may be turned on only if the P7 simulation shows the weighted score beating the two-term score.

The interleaving constraints above are hard set constraints and are not affected by that deferral. Per R4 the deferred quantities are the weighted score terms, never the constraints: the maximum consecutive same-skill count, the skills and units per block, and the 20 percent translation floor all stay enforced on every assembled set in P1 and P2.

### Library IDs used

Computed over `data/archetypes.json` (BC-QA) and `data/skills.json` (BC-SKL), reading each candidate's `skills` array, first entry as primary skill, and the skill's `unit`. A conforming block might run BC-QA-06001 (Riemann sum from a table, primary skill BC-SKL-06005, unit 6), then a unit 3 archetype, then unit 10. The method-selection drill strips the stem using `typical_wording` and `expected_solution_path`. Translation share is measured against `representations` and the 14 BC-REP records in `data/taxonomies.json`, for example BC-REP-03 paired with BC-REP-01.

### Engine rule

D3, the interleaving constraints in [02-adaptive-engine.md](02-adaptive-engine.md) "Item selection algorithm", applied to every non-diagnostic set as a filter after candidate scoring so a high-scoring candidate cannot trade it away, and enforced on the assembled set in "Session assembly". Diagnostic mode is exempt because its job is measurement.

### Measurement in the product

Each attempt logs `(chose right method, executed correctly)` separately, the first derived from whether the opening step matches the archetype's `expected_solution_path` family. A positive result is method-selection accuracy rising on unseen mixed sets with execution accuracy flat. Execution rising alone means the student got faster at procedures they could already choose.

## Spaced retrieval scheduled to the exam date

### Evidence

- Cepeda, Vul, Rohrer, Wixted and Pashler 2008, Psych Science 19(11). Over 1350 participants; optimal inter-study gap about 20 percent of the retention interval at delays of weeks, falling to 5 to 10 percent at one year. [verified] https://laplab.ucsd.edu/articles/Cepeda%20et%20al%202008_psychsci.pdf
- Cepeda et al 2006, Psych Bulletin 132(3). 254 studies, over 14,000 participants, a 9 percent absolute recall advantage for spaced over massed. [single-source] https://pubmed.ncbi.nlm.nih.gov/16719566/
- Rohrer and Taylor 2006, Appl Cogn Psych 20. Spacing math practice across two sessions gave 74 against 49 percent at four weeks; within-session overlearning gave no durable benefit. [single-source] https://onlinelibrary.wiley.com/doi/10.1002/acp.1266
- Distributed practice in applied classroom research, d = 0.54, CI [0.31, 0.77]. [single-source] https://www.ncbi.nlm.nih.gov/pmc/articles/PMC12189222/

The benefit is robust, the optimal gap is not. The 2008 ridgeline is one study on trivia facts and the mathematics result is one small study, so the band carries unknown error bars for calculus.

### The mechanic

The retention interval is fixed by the exam date, Monday 10 May 2027 per [research/exam/exam-structure.md](../../research/exam/exam-structure.md) [single-source]. Every mastered skill carries an FSRS stability and retrievability and is due when retrievability falls below the phase's desired retention, which rises as the exam approaches and shortens gaps without a hand-written schedule. Per R3 the decay model is scheduling only: FSRS retrievability decides when a skill is due and supplies the retention condition read at mastery declaration, and it carries no penalty term inside the strength estimate, because the same quantity used twice would be counted twice. The `lambda` decay penalty is set to 0 until the arm 6 ablation in [10-quality-and-evaluation.md](10-quality-and-evaluation.md) reports. Overlearning inside a session is refused: once demonstrated that day, further repetitions of the same skill neither count toward mastery nor get scheduled.

### Parameters

| Parameter | Value | Source | Tag |
|---|---|---|---|
| Gap as fraction of remaining interval | 10 to 20 percent | Cepeda et al 2008 | [verified] band, [inferred] choice |
| Maximum gap | 60 days | chosen for at least three exposures before May 2027 | [inferred], tunable |
| Minimum first gap | 1 day | Roediger and Karpicke's null at 5 minutes | [inferred] from a [verified] result |
| Desired retention before 15 March 2027 | 0.90 | decisions memo D3 | [inferred], tunable |
| Desired retention from 15 March 2027 | 0.95 | decisions memo D3 | [inferred], tunable |
| FSRS parameters | the 34 srs-benchmark defaults | decisions memo D2 | [verified] |
| Same-day repeats counting to mastery | none | Rohrer and Taylor | [inferred] |

The 15 March switch is a product decision, late enough that shorter gaps do not consume the spring and early enough to cover the final eight weeks.

### Library IDs used

Scheduling state is per BC-SKL record, for example BC-SKL-06017. The queue is materialised as archetypes, so the scheduler asks `data/archetypes.json` which BC-QA covers the most due skills. Propagated credit walks `data/prereq_edges.csv`, using only `hard_prerequisite` and `supporting` edges. Unit exam weight for tie-breaking comes from [research/exam/exam-blueprint.md](../../research/exam/exam-blueprint.md), where BC-UNIT-10 carries 15 to 20 percent and BC-UNIT-03 carries 5 to 10 percent [verified].

### Engine rule

D3, the due-date rules in [02-adaptive-engine.md](02-adaptive-engine.md) "Decay" and review-mode selection with repetition compression in "Item selection algorithm". Compression is why the queue is built from archetypes: one BC-QA loading four skills plus their one-hop hard ancestors retires several due reviews at once, which is the only lever keeping daily load bounded as the graph fills.

### Measurement in the product

Per-skill review history with first-attempt accuracy at each gap, a fitted forgetting curve per unit, and predicted recall on exam day. A positive result is predicted exam-day recall rising while daily review load stays flat, the signature of stability growing rather than the queue lengthening.

## Practice testing over restudy

### Evidence

- Adesope, Trevisan and Sundararajan 2017, RER 87(3). 272 effects from 188 experiments, weighted mean g = 0.51 against restudy and 0.93 against filler; multiple choice g = 0.70, short answer g = 0.48. [verified] https://journals.sagepub.com/doi/abs/10.3102/0034654316689306
- Roediger and Karpicke 2006, Psych Science 17(3). At one week 61 percent tested against 40 percent restudied, with no advantage at five minutes. [verified] https://journals.sagepub.com/doi/10.1111/j.1467-9280.2006.01693.x
- Dunlosky et al 2013, PSPI 14(1). Practice testing and distributed practice are the only two of ten techniques rated high utility. [verified] https://journals.sagepub.com/doi/10.1177/1529100612453266
- Rowland 2014. Mean g = 0.50 across 159 effect sizes, 81 percent favouring retrieval, stronger with complex content and with feedback. [verified] https://pubmed.ncbi.nlm.nih.gov/25150680/
- van Gog and Sweller 2015 argue the effect vanishes as element interactivity rises [single-source] https://link.springer.com/article/10.1007/s10648-015-9310-x ; Karpicke and Aue 2015 reply that element interactivity is undefined and the null studies used immediate massed retrieval [verified] https://learninglab.psych.purdue.edu/downloads/2015/2015_Karpicke_Aue_EDPR.pdf

### The mechanic

Sessions are attempted-problem time, not reading time. Generation is the default response format despite Adesope's larger multiple-choice effect, because Section II is generation on paper and a format advantage measured on verbal recall does not outrank criterion alignment. The van Gog dispute is resolved by sequencing rather than by picking a side: a skill is not eligible for unsupported retrieval until it has produced one unaided correct attempt. Before that, examples; after it, retrieval, and restudy only on failure.

### Parameters

| Parameter | Value | Source | Tag |
|---|---|---|---|
| Session time on attempted problems | at least 70 percent | no published value | [inferred], tunable |
| Session time on reading solutions | at most 30 percent | no published value | [inferred], tunable |
| Unaided successes before retrieval eligibility, `RETRIEVAL_ENTRY` | 1 | track 1 contradiction resolution | [inferred], tunable, A/B candidate against 3 |
| Minimum delay before a retrieval counts | 1 calendar day | Roediger and Karpicke five-minute null | [inferred] from a [verified] result |
| MCQ credit weight | 0.75 | 3PL guessing floor of 0.25 for the four options | [inferred], tunable |

Per R8, `RETRIEVAL_ENTRY` and the mastery rule are two different quantities that read alike. `RETRIEVAL_ENTRY = 1` is the number of credited successes at stage `unsupported` a skill needs before it may enter the interleaved review pool. Mastery separately needs 3 credited unaided successes among its six conditions, set out in the mastery gating section below. The A/B in [10-quality-and-evaluation.md](10-quality-and-evaluation.md) tests `RETRIEVAL_ENTRY` at 1 against 3 and does not test the mastery rule.

### Library IDs used

Response format is set by the archetype's `point_types` and `scoring_pattern`. An archetype carrying BC-PT records, for example BC-QA-06001 with BC-PT-99018, BC-PT-99019, BC-PT-99022, BC-PT-99026 and BC-PT-99007, is served as generated free response with per-point grading. The 56 active archetypes with no `point_types` cannot be point-graded and are served as multiple choice or single-answer until that gap closes, tracked in [12-open-questions.md](12-open-questions.md). Distractors come from `common_distractors`, each traceable to a named BC-ERR path in `data/errors.json`.

### Engine rule

D2, credit assignment in [02-adaptive-engine.md](02-adaptive-engine.md) "Update rules", which holds the 0.75 multiple-choice weight and the `RETRIEVAL_ENTRY` boundary, and D3 in "Item selection algorithm", which refuses to schedule unsupported retrieval for a skill still at stage `example` or `completion`.

Per R2, partial credit is asymmetric by design. A `partial_procedural`, `partial_conceptual` or `partial_unspecified` observation contributes 0 to the success count and 0.5 to the failure count, so a partial state never raises strength, and the engine carries that as an invariant. `notation_only` still contributes 0.25 to the success count because the mathematics was demonstrated. Without the invariant a student who half-solves every item climbs monotonically, which is the one way partial credit can reward not finishing.

### Measurement in the product

First-attempt correctness per item with its retention interval, plus the within-student A/B on `RETRIEVAL_ENTRY`: half of each unit's skills enter the interleaved review pool after one credited unaided success at stage `unsupported` and half after three, compared on a delayed checkpoint at two to four weeks. This is one of the few comparisons a single student can power over eight months.

## Mastery gating

### Evidence

- Kulik, Kulik and Bangert-Drowns 1990, RER 60(2). About d = 0.61 for weaker students and d = 0.4 for stronger, with an earlier precollege estimate near 0.52. [single-source] https://journals.sagepub.com/doi/10.3102/00346543060002265
- Kulik and Fletcher 2016, RER 86(1). Intelligent tutoring raised scores by a median of 0.66 SD, much larger on locally developed tests than on standardized tests. [verified] https://journals.sagepub.com/doi/abs/10.3102/0034654315581420
- Bloom 1984, Educational Researcher 13(6). Tutoring with mastery learning placed the average student about two SD above the conventional mean. [verified] https://journals.sagepub.com/doi/10.3102/0013189X013006004
- Replication critiques land closer to d = 0.4 to 0.8, citing small samples and locally built outcome measures. [single-source] https://nintil.com/bloom-sigma/ and https://www.educationnext.org/two-sigma-tutoring-separating-science-fiction-from-science-fact/

The shrinkage on standardized tests is the most important caution in this document, because the outcome that matters here is a standardized test.

### The mechanic

Progression is gated on per-skill evidence, never on time, coverage, or the student's own declaration. A skill is mastered when the model probability clears threshold at current retrievability and the evidence conditions hold. Mastery is revocable: if probability falls below the lower threshold or an unaided attempt fails, it flips off. The remediation loop is always open, so the ladder drops rather than the item repeating.

Per R7 one counter pair decides stage changes and nothing else does. Two consecutive credited successes at a stage advance it and two consecutive credited failures drop it. Un-mastery, meaning a credited failure at stage `unsupported` or the model probability falling below the lower threshold, flips `mastered` to false and does not itself move the stage; the counter moves it. The phrase "two failed mastery attempts" used in earlier drafts of this document is the same counter restated, not a third trigger.

Per R2 a partial state never raises strength. Half-solving contributes to the failure count only, so it can delay mastery and can never produce it.

### Parameters

| Parameter | Value | Source | Tag |
|---|---|---|---|
| Planning expectation, standardized criterion | d = 0.4 to 0.7 | Kulik et al 1990; Kulik and Fletcher 2016 | [single-source] for the Kulik et al 1990 half, [verified] for Kulik and Fletcher 2016 |
| Mastery threshold | sigma(m_k) at least 0.90 at current R | decisions memo D2 | [inferred], tunable |
| Un-mastery threshold | sigma(m_k) below 0.75 | decisions memo D2 | [inferred], tunable |
| Credited unaided successes | 3 at stage unsupported | Kulik structure plus Cepeda spacing | [inferred], tunable |
| Distinct archetypes | 2 | decisions memo D2 | [inferred], tunable |
| Distinct calendar days | 3, spanning at least 7 days | decisions memo D2 | [inferred], tunable |
| Same-day repeats | do not count | sleep and spacing literature | [inferred] |
| Failures before ladder drop | 2 consecutive credited, the same counter the fading section uses | decisions memo D2, R7 | [inferred], tunable |

Every mastery condition above is inferred. They are an operational definition of a construct the literature leaves loose and are the first parameters to revisit once eight weeks of data exist.

### Library IDs used

State is stored per BC-SKL record, for example BC-SKL-06017, whose `adaptive.mastered_if` states in prose what a mastered performance looks like. The diagnostician must choose a `mastery_state` from the enum used by `data/diagnostic_signals.json`, ideally by matching a BC-SIG record such as BC-SIG-06001, whose state is `partial_unspecified` and whose `distinguish_by` names the probe separating an arithmetic slip from a conceptual gap. The outer fringe is computed from `hard_prerequisite` edges in `data/prereq_edges.csv` against the 77 BC-PRQ records, assumed mastered until a gap is diagnosed. Only 31 of 541 active skills carry `independently_assessable: true`, which is why most mastery evidence accumulates from multi-skill archetypes.

### Engine rule

D2, mastery declaration and un-mastery in [02-adaptive-engine.md](02-adaptive-engine.md) "Update rules", plus the fringe restriction in "Prerequisite gating and the outer fringe", which refuses any archetype whose primary skill has unmastered hard prerequisites outside diagnostic mode. The state a skill holds before its first credited observation is set in "Cold-start diagnostic design" per R1, so an unobserved skill of median difficulty starts at probability 0.5 rather than near zero.

### Measurement in the product

Mastery growth per study hour, reported beside a six-week checkpoint against released AP material and never alone. A positive result is both rising together. Internal mastery climbing while the checkpoint stays flat is the Kulik and Fletcher failure and triggers a review of the thresholds.

## Adaptive worked-example fading

### Evidence

- Salden, Aleven, Schwonke and Renkl, Instructional Science. Adaptive fading keyed to a per-skill mastery estimate beat both fixed fading and pure problem solving in a geometry tutor. [single-source] http://www.cee.uma.pt/ron/Salden%20et%20al.%20-%20The%20Expertise%20Reversal%20Effect%20and%20Worked%20Examples.pdf
- Renkl, Atkinson, Maier and Staley 2002. Backward fading, last step removed first, beat an abrupt switch from examples to problems. [single-source] https://link.springer.com/article/10.1023/B:TRUC.0000021815.74806.f6
- Kalyuga, Ayres, Chandler and Sweller 2003, Educ Psychologist 38(1). Expertise reversal: support that helps novices becomes redundant and then harmful. [single-source] https://www.tandfonline.com/doi/abs/10.1207/S15326985EP3801_4
- A recent review notes earlier worked-example effects may have been overestimated, with anticipated effects around Cohen's f = 0.25, roughly eta squared 0.06. [single-source] https://www.tandfonline.com/doi/full/10.1080/01443410.2023.2273762

Robust in direction, thin in parameters. No source names a switching threshold, and Salden's answer is to fade on a running per-skill estimate rather than on a fixed schedule.

### The mechanic

Each skill carries a stage in `{example, completion, unsupported}`. Stage `example` is a fully worked solution with one structured self-explanation prompt; `completion` blanks the last step and fades backwards one step per success; `unsupported` is a plain problem, and once a skill reaches it the example is never shown unprompted again, which is the expertise-reversal guard. Stage `example` is skipped when all hard prerequisites are mastered and the confidence-corrected first attempt succeeds, because that is exactly Kalyuga's harmful case.

### Parameters

| Parameter | Value | Source | Tag |
|---|---|---|---|
| Successes to advance a stage | 2 consecutive credited | no published value | [inferred], tunable |
| Failures to drop a stage | 2 consecutive credited | no published value | [inferred], tunable |
| Fading direction | backward | Renkl et al 2002 | [single-source] |
| Trigger | running per-skill estimate, not a schedule | Salden et al | [single-source] |
| Example-stage skip | hard prerequisites mastered and first attempt correct above guess confidence | decisions memo D2 | [inferred], tunable |
| Expertise-reversal probe | occasional withholding at stage completion | no published value | [inferred], tunable |

### Library IDs used

The example is built from the archetype's `expected_solution_path` with each step tagged to a BC-PT type, so the completion blank falls on a real scoring point rather than an arbitrary line. For BC-QA-06001 the blanked step is BC-PT-99018, BC-PT-99019 or BC-PT-99026 depending on where the evidence is thinnest. The skip condition reads `hard_prerequisite` edges and the BC-PRQ records.

### Engine rule

D2, the fading ladder in [02-adaptive-engine.md](02-adaptive-engine.md) "Update rules", holding the advance, drop and skip conditions, with the single counter pair of R7 as the only writer of `fading_stage`. D3 consumes the stage as a filter in "Item selection algorithm", because an item at stage `example` is not a retrieval opportunity and must not be scheduled as one. Per R4 the stage is also where the 0.8 success target now lives: a candidate whose predicted success is below 0.5 is served at stage `example` or `completion` and one above 0.9 at stage `unsupported`, which makes the target a fading filter rather than a score term.

### Measurement in the product

Stage logged on every attempt. The reversal warning sign is accuracy or latency worsening with support present, tested cheaply by occasionally withholding the example at stage `completion`. A positive result is the median attempts to reach `unsupported` falling across units without a rise in un-mastery events.

## Feedback timing and elaboration

### Evidence

- Shute 2008, RER 78(1). Timing findings are inconsistent; immediate feedback suits procedural acquisition and error correction, and specific elaborated feedback beats verification-only. [verified] https://journals.sagepub.com/doi/10.3102/0034654307313795
- Bangert-Drowns, Kulik, Kulik and Morgan 1991, RER 61(2). Feedback helps only when it supplies correct-answer information the learner could not anticipate; feedback available before commitment can produce near-zero or negative effects. [single-source] https://journals.sagepub.com/doi/10.3102/00346543061002213
- Hattie and Timperley 2007, RER 77(1). Average around d = 0.79 across syntheses, highly variable; task, process and self-regulation feedback help, feedback aimed at the self does not. [single-source] https://journals.sagepub.com/doi/10.3102/003465430298487
- Kulik and Kulik 1988, RER 58(1). Field studies favoured immediate feedback, laboratory list-learning favoured delayed. Pooled effect size unknown. [single-source] https://journals.sagepub.com/doi/10.3102/00346543058001079

The timing contradiction is unresolved in the literature. The product's position, that the delayed advantage is largely spacing in disguise so an immediate correction plus a scheduled re-encounter gets both, is [inferred] and is not a claim any fetched source makes.

### The mechanic

Step-level immediate verification at stages `example` and `completion`. Nothing until submission at stage `unsupported` and on every exam-shaped item, then elaborated feedback naming the rule violated and the scoring consequence rather than only the answer. The answer is never visible before commitment. Every corrected item re-enters the queue at a short gap, which turns the correction into a spaced exposure.

### Parameters

| Parameter | Value | Source | Tag |
|---|---|---|---|
| Stages example and completion | immediate, step level | Shute 2008 | [verified] direction |
| Stage unsupported and exam-shaped items | withheld until submission | Shute 2008; Bangert-Drowns et al 1991 | [verified] direction, [inferred] boundary |
| Requeue gap after correction | 1 to 2 days | Cepeda et al 2008 lower bound | [inferred] value |
| Feedback content | names violated rule and scoring consequence | Shute 2008 | [verified] |
| Representations per feedback screen | at most 2 | split-attention literature | [inferred], tunable |

### Library IDs used

The elaborated text is assembled from records rather than written free-hand. The violated rule is the failed BC-PT type, for example BC-PT-99018 for a malformed Riemann sum. The consequence is the `scoring_consequence` field on the matched BC-ERR record, which all 390 active errors carry. The candidate explanation comes from `possible_misconceptions`, resolving to BC-MIS records, present on 388 of 390 errors. Feedback renders first in the item's own representation and at most once more in a translated BC-REP pair implied by the leading misconception's `exposing_archetypes`.

### Engine rule

D4, feedback timing and the elaborated-feedback contract in [03-diagnosis-and-feedback.md](03-diagnosis-and-feedback.md), plus the requeue rule that hands the corrected item back to D3 with a forced short due date, read by [02-adaptive-engine.md](02-adaptive-engine.md) "Decay" and served by the due-review block in "Session assembly".

### Measurement in the product

Next-encounter accuracy for elaborated against verification-only feedback, randomized per item, listed as an A/B switch in [10-quality-and-evaluation.md](10-quality-and-evaluation.md). A positive result is higher next-encounter accuracy in the elaborated arm at matched retention interval.

## Confidence rating and hypercorrection routing

### Evidence

- Dunlosky and Rawson 2012, Learning and Instruction 22(4). Greater monitoring accuracy was associated with higher retention; overconfident learners stopped studying prematurely, and Study 1 manipulated accuracy experimentally. [verified] https://www.sciencedirect.com/science/article/pii/S0959475211000685
- Butterfield and Metcalfe 2001, hypercorrection. High-confidence errors are the most persistent and the most correctable once corrected. Effect size unknown. [single-source] https://www.columbia.edu/cu/psychology/metcalfe/PDFs/ButterfieldMetcalfe2001.pdf
- Nelson and Dunlosky 1991. Delayed judgments of learning are substantially more accurate than immediate ones. [single-source] https://journals.sagepub.com/doi/10.1111/j.1467-9280.1991.tb00147.x

### The mechanic

A three-point rating, guess, unsure, confident, collected before feedback on every item. It costs about three seconds and buys two things. A high-confidence error sets a hypercorrection flag pulling the next due date to one day. And confidence enters the model as a grade modifier, so a success at high confidence and below the archetype's median time grades Easy while any other correct answer grades Good, which stops a slow uncertain answer buying the same stability as a fluent one.

### Parameters

| Parameter | Value | Source | Tag |
|---|---|---|---|
| Scale | 3 points | no published value | [inferred], tunable |
| Collection point | after commit, before feedback | Bangert-Drowns commit-first logic | [inferred] |
| Hypercorrection requeue gap | 1 day | priority from hypercorrection literature, value unsourced | [inferred], tunable |
| Grade Easy condition | mastered, high confidence, time below archetype median | decisions memo D2 | [inferred], tunable |
| Time cost | about 3 seconds per item | track 1 ranking table | [inferred] |

### Library IDs used

Confidence is stored on the attempt and consumed by the diagnostician alongside the graded point vector. It matters for BC-SIG matching: BC-SIG-06001, correct Riemann sum products with an arithmetic slip in the total, is a far more plausible reading at high confidence than at a guess, because a guess with right structure and wrong total is as consistent with not knowing as with slipping. The `non_conceptual_causes` field on the BC-ERR record carries the other half of that discrimination.

### Engine rule

D2, confidence weighting and the FSRS grade mapping in [02-adaptive-engine.md](02-adaptive-engine.md) "Update rules", and D4, which requires the diagnostician to receive confidence as an input rather than inferring it from latency.

### Measurement in the product

Mean confidence minus proportion correct, plotted monthly, plus a Brier score. This is the cheapest high-value metric in the system because it needs no control condition. A positive result is the gap narrowing toward zero from above, the overconfidence direction that predicts premature stopping. Narrowing from below is underconfidence, a different problem, addressed by showing the student their own hit rate.

## Structured self-explanation

### Evidence

- Bisra, Liu, Nesbit, Salimi and Winne 2018, Educ Psych Review 30(3). 69 effect sizes from 64 reports, roughly 6000 participants, weighted mean g = 0.55. [verified] https://link.springer.com/article/10.1007/s10648-018-9434-x
- Chi, Bassok, Lewis, Reimann and Glaser 1989, Cognitive Science 13(2). Students who spontaneously explained worked examples solved more later problems. [single-source] https://onlinelibrary.wiley.com/doi/10.1207/s15516709cog1302_1
- Rittle-Johnson on self-explanation in mathematics: benefits are conditional and sometimes bought at a time cost relative to solving more problems. [single-source] https://link.springer.com/article/10.1007/s10648-017-9436-0

The boundary matters more than the headline. In mathematics prompts help conceptual outcomes while costing practice volume, and open prompts underperform structured ones.

### The mechanic

Exactly one structured prompt, "which rule justifies step k, and why does it apply here", on each worked example and each corrected error. Nothing else. No prompt on a routine correct answer at stage `unsupported`, because those minutes buy another problem. The written answer is scored against the AP justification form, which makes the prompt double as Section II criterion practice.

### Parameters

| Parameter | Value | Source | Tag |
|---|---|---|---|
| Effect size assumed | g = 0.55 | Bisra et al 2018 | [verified] |
| Prompts per worked example | exactly 1 | structured over open prompts | [verified] direction, [inferred] count |
| Prompts on routine correct answers | none | math time-cost caveat | [inferred] |
| Prompt form | name the rule, say why it applies | Bisra et al 2018 | [verified] |

### Library IDs used

The targeted step is chosen by BC-PT type, preferring justification-bearing types such as BC-PT-99010 (justification by sign analysis of a derivative), BC-PT-99011 (candidates test) and BC-PT-99017 (Mean Value Theorem or Rolle conclusion) over mechanical types, because naming the rule is the whole content of those steps. Expected answers are checked against `research/scoring/justification-requirements.md` and the 29 BC-CV command-verb records in `data/taxonomies.json`. On a corrected error the prompt targets the step where the matched BC-ERR `observed_behavior` occurred.

### Engine rule

D4, self-explanation prompt placement, inside the feedback contract rather than in selection, because the prompt is a property of the feedback screen and not of the item.

### Measurement in the product

Delayed accuracy on skills whose examples carried prompts against matched skills without, randomized at skill level, plus justification scores reported as FRQ readiness. A positive result is a rise in justification-point earning on unit checks, which is the transfer the prompt is meant to produce.

## Split-attention-free presentation

### Evidence

- Schroeder and Cenkci 2018, Educ Psych Review. 58 independent comparisons, n = 2426, overall g = 0.63 favouring integrated over split presentation. [verified] https://link.springer.com/article/10.1007/s10648-018-9435-9
- Sweller's cognitive load theory: intrinsic load is set by element interactivity, extraneous load by presentation. [single-source] https://link.springer.com/article/10.1007/s10648-019-09465-5
- The redundancy effect: the same content in two simultaneous forms can hurt relative to one. Effect size unknown. [single-source] https://en.wikipedia.org/wiki/Split_attention_effect

### The mechanic

Every graph, slope field, table and diagram carries its labels and the relevant algebraic step inside the figure. No caption-only labels, no layout requiring scrolling between a figure and its question, no audio duplicating on-screen text, one new idea per screen. The prerequisite gate belongs to this mechanic as well as to mastery gating, because intrinsic load cannot be designed away, only reduced by prior schema: no series convergence work until limit evaluation is at mastery.

### Parameters

| Parameter | Value | Source | Tag |
|---|---|---|---|
| Effect size assumed | g = 0.63 | Schroeder and Cenkci 2018 | [verified] |
| Caption-only labels | none permitted | Schroeder and Cenkci 2018 | [verified] direction |
| Scroll between figure and stem | zero | integration principle | [inferred] |
| Simultaneous duplicate channels | none | redundancy effect | [single-source] |
| New ideas per screen | 1 | element interactivity | [inferred], tunable |

This is a build cost and consumes no student minutes, which is why it ranks high on impact per minute despite being a presentation rule.

### Library IDs used

Figures are declarative specifications from the generator in [04-item-generation.md](04-item-generation.md), driven by the archetype's `representations`. The figure-bearing representations BC-REP-02 (graphical), BC-REP-03 (numerical table), BC-REP-07 (slope field) and BC-REP-08 (geometric diagram) are what this rule binds. BC-DF-03 (unusual representation) signals that a figure is doing construct-relevant work and must not be simplified away; BC-DF-11 (unfamiliar surface presentation) is presentation difficulty that is not construct-relevant and must never be added on purpose.

### Engine rule

None. This is a rendering contract enforced in [08-design-brief.md](08-design-brief.md) and checked by the verifier in [04-item-generation.md](04-item-generation.md), which rejects a figure specification whose labels sit outside the figure.

### Measurement in the product

Time to first keystroke and abandoned-attempt rate on items differing only in presentation. Load shows up as slower starts and more abandonment at identical mathematical content. A positive result is no difference in time to first keystroke between a figure-bearing and a symbolic item at matched difficulty factors.

## Productive-failure openers for conceptual targets

### Evidence

- Sinha and Kapur 2021, RER 91(5). 53 studies, 166 comparisons, Hedges g = 0.36, CI [0.20, 0.51] favouring problem solving before instruction. [verified] https://journals.sagepub.com/doi/10.3102/00346543211019105
- Loibl, Roll and Rummel 2017, Educ Psych Review. The benefit requires activating prior knowledge, generating contrasting solutions, and explicitly comparing the canonical solution against the learner's attempt; without the comparison the effect disappears. [single-source] https://link.springer.com/article/10.1007/s10648-016-9379-x
- Kapur: the advantage appears on conceptual and transfer measures, not on procedural fluency. [single-source] https://boldscience.org/wp-content/uploads/2025/04/Productive-Failure.pdf

### The mechanic

A conceptual target opens with one short generation task on a problem whose method the student lacks, then places their attempt beside the canonical method with the gap named. The comparison step is obligatory. The mechanic is capped hard: once per conceptual target, never for a computational skill, because teaching partial fractions this way spends fifteen minutes buying an effect the literature locates elsewhere.

### Parameters

| Parameter | Value | Source | Tag |
|---|---|---|---|
| Effect size assumed | g = 0.36, CI [0.20, 0.51] | Sinha and Kapur 2021 | [verified] |
| Opener duration | 10 to 15 minutes | no published value | [inferred], tunable |
| Frequency | once per conceptual target | no published value | [inferred] |
| Conceptual targets | limits, derivative definition, accumulation, series convergence, polar and parametric area | decisions memo D3 | [inferred] |
| Comparison step | mandatory | Loibl, Roll and Rummel 2017 | [single-source] |
| Use on computational skills | none | Kapur's conceptual-only boundary | [single-source] |

### Library IDs used

Targets map to BC-CON concept records and their opening units, BC-UNIT-01 for limits, BC-UNIT-02 for the derivative definition, BC-UNIT-06 for accumulation, BC-UNIT-09 for polar and parametric area, BC-UNIT-10 for series convergence. The opener's item is drawn from an archetype whose `difficulty_factors` include BC-DF-13 (reversed reasoning direction) or BC-DF-15 (unsignposted procedure selection), the factors that make an item a generation task rather than an execution task. Gap naming uses the reachable BC-MIS records, in particular `rival_misconceptions`, present on 210 of 213 active BC-MIS records, which is exactly the contrasting-solutions structure Loibl requires. The earlier 233 and 236 figures counted retired records.

### Engine rule

D3, [02-adaptive-engine.md](02-adaptive-engine.md) "Session assembly", which per R5 owns the opener. The cap is carried as a per-concept flag `concept_opener_done`, stored on the concept's first skill and consumed by the fringe-learning block the first time any skill of a flagged concept enters the fringe. It does not enter D2: a failed generation attempt at an opener is expected and must not be credited as a failure against the target skill, which would push the fringe backwards for doing the right thing.

### Measurement in the product

Concept-probe accuracy for that target, on a fixed item set never used for practice, against targets introduced without an opener. With five targets this will not be powered within one student, so it is reported descriptively and the mechanic is retained on the meta-analysis rather than on local evidence. That is stated plainly in [10-quality-and-evaluation.md](10-quality-and-evaluation.md).

## Representation translation drills

### Evidence

- Ainsworth 2006, Learning and Instruction 16(3). Multiple representations complement, constrain interpretation and construct understanding, and the benefit depends on the learner's ability to translate; unsupported multi-representation displays can hurt. [verified] https://nschwartz.yourweb.csuchico.edu/Ainsworth_2006_Learning-and-Instruction.pdf
- The Rule of Four is embedded in the AP framework's multiple-representations practice. [single-source] https://teachingcalculus.com/2016/10/11/mpac-4-multiple-representations/
- Reform calculus texts present multiple representations far more often than they require translation between them. [single-source] https://files.eric.ed.gov/fulltext/ED557199.pdf

No meta-analytic effect size for multiple representations in calculus was retrieved; it is unknown. This mechanic earns its place on criterion alignment, not on learning science, and the document says so rather than dressing a curriculum convention as an effect.

### The mechanic

Given one representation, produce or select another. Given a graph of f, sketch f prime. Given a table, estimate a rate. Given a symbolic form, describe the behaviour in words. At least a fifth of scheduled practice is translation rather than compute-the-answer, and the mix is measured against released free-response sections rather than assumed.

### Parameters

| Parameter | Value | Source | Tag |
|---|---|---|---|
| Translation share of scheduled practice | at least 20 percent | chosen to approximate the released-section mix | [inferred], tunable |
| Representation taxonomy | 14 BC-REP records | data/taxonomies.json | [verified] |
| Connecting Representations, Section I | 15 to 30 percent | research/exam/exam-blueprint.md | [verified] |
| Connecting Representations, Section II | 10 to 20 percent | research/exam/exam-blueprint.md | [single-source] |
| Representations per feedback screen | at most 2 | split-attention rule | [inferred] |

The Section II pairing is single-source because [research/exam/exam-blueprint.md](../../research/exam/exam-blueprint.md) records that the cached extraction separated the practice labels from their percentages, so the pairing is read from list order rather than an intact row. The product should not lean on it without a re-check.

### Library IDs used

Built from BC-REP pairs in `data/taxonomies.json`, the `representations` array on each BC-QA, and the 395 BC-QV variants that already encode surface changes within a family. BC-QA-06001 carries BC-REP-03 and BC-REP-05, so its translation partner is an archetype carrying BC-REP-01 or BC-REP-02 over the same skills. The representation-gap term reads a per-pair accuracy matrix keyed on `(source BC-REP, target BC-REP)`.

### Engine rule

D3, the 20 percent translation floor, enforced in [02-adaptive-engine.md](02-adaptive-engine.md) "Item selection algorithm" as a hard set constraint alongside the interleaving constraints and checked on the assembled set in "Session assembly". Per R4 the floor is a constraint and stays on in P1 and P2. The `w_rep * representation_gap` score term is deferred with the rest of the weighted terms and may be turned on only after the P7 simulation shows the five-term score beating the two-term score on mastery per item. The per-pair accuracy matrix is still recorded meanwhile, because the deferred term needs it to exist before it can be evaluated.

### Measurement in the product

Accuracy by `(source, target)` representation pair, reported as a matrix. Weak cells are the diagnostic output and map directly onto AP item types. A positive result is the weakest cells rising while the strongest stay flat, which is what a gap-driven selection term should produce.

## FRQ justification writing as criterion practice

### Evidence

- 2025 AP Calculus AB/BC Scoring Guidelines, General Scoring Notes. Three provisions matter here and per R21 they are stated separately rather than as one continuous restatement. Answers need not be simplified. On precision, decimal approximations should be accurate to three places after the decimal point. The penalty is capped, so at most one point per free-response question is lost to inappropriate rounding. [verified] https://apcentral.collegeboard.org/media/pdf/ap25-sg-calculus-bc.pdf
- Practitioner analysis of AP justification: complete justification names the theorem or definition, and over-writing a correct justification can forfeit points by introducing a contradictory claim. [single-source] https://transformativetutoring.com/wp-content/uploads/2019/10/AP-Calculus-FRQ-Justifications.pdf and https://apcentral.collegeboard.org/courses/ap-calculus-ab/exam/past-exam-questions
- Justification carries 35 to 60 percent of the Section II practice weight per [research/exam/exam-blueprint.md](../../research/exam/exam-blueprint.md). [single-source]
- Rowland 2014: the testing effect is stronger with complex content, effortful retrieval and feedback, all three favouring full free-response practice with rubric feedback. [verified] https://pubmed.ncbi.nlm.nih.gov/25150680/

### The mechanic

For every free-response item the student writes the justification in the AP form, stating the theorem or definition, that its hypotheses hold, and the conclusion. It is graded per point against the rubric structure, with explicit feedback when an added unsupported sentence contradicts a correct claim. This is the one mechanic with no effect size behind it and it is kept regardless, because it is the criterion task itself.

### Parameters

| Parameter | Value | Source | Tag |
|---|---|---|---|
| Justification structure | theorem or definition, hypotheses hold, conclusion | practitioner analysis and scoring guidelines | [single-source] |
| Over-writing penalty feedback | shown when an added sentence contradicts an earned claim | scoring guidelines behaviour | [single-source] |
| Three-decimal rule | accurate to three places, rounded or truncated | 2025 scoring guidelines | [verified] |
| Rounding penalty cap | at most one point per free-response question | 2025 scoring guidelines | [verified] |
| Points per free-response question | 9 | research/exam/exam-structure.md | [verified] |
| Grading confidence | provisional until agreement; kappa at best 0.56 in published work | track 3 | [single-source] |

### Library IDs used

Grading runs one structured call per BC-PT record, of which the library holds 76. Justification points are the judged half: BC-PT-99010, BC-PT-99011, BC-PT-99012 (classification of a critical point), BC-PT-99015 (differentiable implies continuous), BC-PT-99016 (Intermediate Value Theorem conclusion) and BC-PT-99017. Mechanical points such as BC-PT-99001 (definite integral with correct limits) and BC-PT-99004 (answer with or without supporting work) are decided by SymPy equivalence and numeric comparison before any model call. Command verbs come from the BC-CV records; language requirements from `research/scoring/justification-requirements.md` and `research/scoring/notation-requirements.md`. Of 249 FRQ parts in `data/frq_records.json`, 227 carry point totals and the 2018 parts carry none.

### Engine rule

D4, the grader contract: deterministic pre-checks decide mechanical points, the model decides only justification, interpretation and notation points, each judged point is sampled twice at temperature 0 and once under a strictness-varied prompt, and any disagreement escalates to the review queue and is shown as provisional rather than averaged.

### Measurement in the product

Earning rate per BC-PT against the published 2025 per-point means recorded in [research/exam/scoring-system.md](../../research/exam/scoring-system.md), which prints a mean for each of the nine scoring points on each question. A positive result is the student's earning rate on a point type rising above the published mean. That is better sourced and more actionable than a predicted score, and it is what the product shows instead.

## Implementation intention and queue-bound streak

### Evidence

- Gollwitzer and Sheeran 2006, Adv Exp Soc Psych 38. Implementation intentions had a medium to large effect on goal attainment, d = 0.65 across 94 independent tests and over 8000 participants. [verified] https://www.sciencedirect.com/science/chapter/bookseries/abs/pii/S0065260106380021
- Lally, van Jaarsveld, Potts and Wardle 2010, Eur J Soc Psych 40(6). Median time to 95 percent of asymptotic automaticity was 66 days, range 18 to 254, among the roughly half of participants whose data fit the curve. [verified] https://onlinelibrary.wiley.com/doi/abs/10.1002/ejsp.674
- Deci, Koestner and Ryan 1999, Psych Bulletin. Tangible expected rewards reduced free-choice intrinsic motivation, reported by contingency type: d = -0.40 engagement-contingent, -0.36 completion-contingent and -0.28 performance-contingent, against d = +0.33 for positive verbal feedback. [single-source] https://pubmed.ncbi.nlm.nih.gov/10589297/
- Streak mechanics are reported by Duolingo to lift engagement, for example 14 percent at day-14 retention from a streak wager. Company-reported engagement, not learning outcomes, and critical work frames streaks as loss-aversion pressure. [single-source] https://papers.ssrn.com/sol3/papers.cfm?abstract_id=6846283

This is the weakest section of the evidence base for this use case. Implementation intentions and habit formation were established on simple daily behaviours, not on 45 minutes of calculus.

### The mechanic

At setup the student writes one if-then plan naming a fixed time and place. The streak unit is a completed scheduled review queue, never minutes and never a session of any length, so a token session cannot preserve it and a heavy day cannot be gamed by grinding easy items. The daily requirement is capped at what the spacing schedule demands, and freeze days exist so one missed evening does not become a reason to quit. Nothing awards points for volume.

### Parameters

| Parameter | Value | Source | Tag |
|---|---|---|---|
| Effect size for the if-then plan | d = 0.65 | Gollwitzer and Sheeran 2006 | [verified] |
| Setup cost | about 10 minutes, once | track 1 ranking table | [inferred] |
| Streak unit | one completed due queue | track 1 contradiction resolution | [inferred] |
| Freeze days | 1 to 2 per month | no published value | [inferred], tunable |
| Expected time to automaticity | 66 day median, range 18 to 254 | Lally et al 2010 | [verified] |
| High-support period | first 10 weeks | derived from the 66 day median | [inferred], tunable |

The 66 day figure is a median of a wide skewed distribution among half the participants. It sets an expectation and is never shown to the student as a countdown.

### Library IDs used

None. This mechanic touches no registry and reads only the scheduler's due-queue state, itself derived from BC-SKL retrievability. It appears here because it consumes student minutes and omitting it would hide a mechanic that changes behaviour.

### Engine rule

None in the D2 to D4 sense. The streak is defined by the due-review block emptying in [02-adaptive-engine.md](02-adaptive-engine.md) "Session assembly", and must never feed back into D2, because a motivational construct entering the mastery model is how a system starts optimising for adherence instead of learning.

### Measurement in the product

Adherence, meaning queues completed on their due day, tracked separately from effort, meaning median items per session and median time per item. The failure signature is adherence holding while items per session falls. That pattern changes the streak definition, not the student's notifications.

## Session shape and daily target

### Evidence

- Baddeley and Longman 1978, Ergonomics. One hour once a day produced better learning per hour than two hours once a day or twice-daily schedules; the most distributed schedule was most efficient per hour. [single-source] https://www.tandfonline.com/doi/abs/10.1080/00140137808931764
- Surgical skills training: three 75-minute sessions over three weeks beat the same three massed into one day for acquisition and retention. [single-source] https://digitalpromise.org/2019/05/08/ask-the-cognitive-scientist-distributed-practice/
- No meta-analysis establishing an optimal session length for mathematics was retrieved. Unknown.

The distributed-practice literature concerns gaps between sessions, not session length, and studies that appear to speak to length confound the two. No session-length number here is evidence based and the document does not present one as such.

### The mechanic

The session opens with a due-review block, moves to fringe learning, then interleaved mixed review, then calibration and one-line error notes. It ends when all four blocks are empty, not when a timer expires, so the binding constraint is mastery work rather than time served. The block ordering and sizes are an engine rule and are specified in [02-adaptive-engine.md](02-adaptive-engine.md) "Session assembly" per R5; this section supplies the evidence behind them and nothing else.

The minute figure attached to a session is a forecast of the assembled queue and never a schedule. It is computed from per-archetype median attempt time, it is output rather than input, and the product does not set a daily quota, prescribe days of the week or tell the student when to study. The distribution finding that motivates the design is Baddeley and Longman's, that the most distributed schedule was the most efficient per hour [single-source], and it is recorded here as that source's finding rather than as a recommendation to the student.

### Parameters

| Parameter | Value | Source | Tag |
|---|---|---|---|
| Session length forecast | 40 to 60 minutes, 45 as the planning default, forecast only | no source | [inferred], tunable |
| Due-review block | at most 5 items or 5 minutes forecast | decisions memo D3, R5 | [inferred], tunable |
| Fringe learning | 20 to 30 minutes | decisions memo D3 | [inferred], tunable |
| Interleaved mixed review | 10 to 15 minutes | decisions memo D3 | [inferred], tunable |
| Calibration and error notes | 2 to 5 minutes | decisions memo D3 | [inferred], tunable |
| Stop condition | all four blocks empty, not a timer | desirable-difficulties framing, R5 | [inferred] |
| Target first-attempt accuracy | 60 to 85 percent | no study names this band | [inferred], tunable |
| Timed part drill cadence | every 2 to 3 weeks, more often in the final 8 weeks | no source establishes a cadence | [inferred], tunable |
| Full mock cadence | every 4 to 6 weeks, more often in the final 8 weeks | no source establishes a cadence | [inferred], tunable |

Both cadences are owned by [05-assessment-modes.md](05-assessment-modes.md) and restated here per R19; part drills and full mocks are separate instruments on separate cadences and earlier drafts of this document conflated them.

The accuracy band deserves a warning. Its nearest anchor is the desirable-difficulties framing plus common tutoring practice of targeting moderate success. The 0.8 success target sits inside it and per R4 now selects a fading stage rather than weighting a score, the Math Academy figure of about 80 percent that partly motivates it is single-source, and the Wilson and colleagues 85 percent result is described by its own authors as not generalisable.

### Library IDs used

The session builder reads `data/archetypes.json` for candidates and `data/skills.json` for fringe membership, estimating minutes from per-archetype median latency once attempts exist. Before that it falls back to the archetype's `difficulty_factors` count, the same BC-DF-count prior the mastery model uses for beta.

### Engine rule

D3, [02-adaptive-engine.md](02-adaptive-engine.md) "Session assembly", which per R5 owns the four blocks, their ordering, their sizes, the minute forecast and the stop condition that ends a session when all four blocks are empty. The minute forecast is a presentation of that section's output, never an input to it.

### Measurement in the product

Accuracy by minute within session, to find this student's fatigue point. If first-attempt accuracy on comparable items falls materially after minute N, that is the empirical session cap and it outranks any published number. Time of day and self-reported sleep are logged alongside and the resulting correlation is reported as observational, never as a scheduling rule.

## Metacognitive judgments of learning

### Evidence

- Nelson and Dunlosky 1991. Delayed judgments of learning are substantially more accurate than immediate ones. [single-source] https://journals.sagepub.com/doi/10.1111/j.1467-9280.1991.tb00147.x
- Dunlosky and Rawson 2012, Learning and Instruction 22(4). Monitoring accuracy was associated with retention; overconfident learners stopped studying prematurely. [verified] https://www.sciencedirect.com/science/article/pii/S0959475211000685
- Soderstrom and Bjork 2015, Perspect Psych Science 10(2). Systematic dissociations between training performance and learning measured later. [single-source] https://journals.sagepub.com/doi/10.1177/1745691615569000

### The mechanic

Judgments are asked only at the start of a later session, never immediately after studying the item, because immediate judgments are inflated. The student may never declare a skill mastered. What the product shows in place of a session score is predicted exam-day recall and a calibration curve, so the number the student watches tracks learning rather than performance. Soderstrom and Bjork are why this matters: a display reporting in-session fluency rewards exactly the conditions that produce the worst retention.

### Parameters

| Parameter | Value | Source | Tag |
|---|---|---|---|
| Timing | start of a later session only | Nelson and Dunlosky 1991 | [single-source] |
| Scale | matched to the 3-point confidence scale | consistency with the item rating | [inferred] |
| Calibration report cadence | monthly | no published value | [inferred], tunable |
| Primary displayed number | predicted exam-day recall | desirable-difficulties framing | [inferred] |
| Student self-declaration of mastery | not permitted | Dunlosky and Rawson 2012 | [verified] direction |

### Library IDs used

Judgments are collected per BC-SKL record at unit level, prompted with the skill's `name` so the student judges something recognisable rather than an identifier. The comparison is against that skill's model probability at the moment of judgment, which makes the curve a skill-by-skill comparison rather than an aggregate.

### Engine rule

None in D2. Judgments are recorded and displayed but never enter the mastery model, because a self-report the literature says is systematically biased must not move a state that gates progression. D4 consumes them only for the calibration display.

### Measurement in the product

Two curves, the item-level calibration curve (mean confidence minus proportion correct) and the skill-level judgment curve (mean judgment minus model probability). A positive result is both narrowing. A judgment curve staying wide while the confidence curve narrows means the student is calibrated within an item and miscalibrated about a topic, the pattern that produces premature stopping, and it is addressed by showing the skill-level gap directly.

## Measurement against released AP material every 6 weeks

### Evidence

- Kulik and Fletcher 2016, RER 86(1). Tutoring effects were much larger on locally developed tests than on standardized tests, median 0.66 overall. [verified] https://journals.sagepub.com/doi/abs/10.3102/0034654315581420
- Published BC score distributions and per-question free-response means for 2023 to 2025 are recorded in [research/exam/scoring-system.md](../../research/exam/scoring-system.md) from the College Board distribution PDFs. [verified]
- Epstein, Calculus Concept Inventory: normalized gains 0.23 (SD 0.04) for traditional lecture against 0.48 (SD 0.14) for interactive engagement. [verified] https://www.ams.org/notices/201308/rnoti-p1018.pdf Psychometric critiques find weak item discrimination. [single-source] https://blogs.ams.org/matheducation/2016/07/25/does-the-calculus-concept-inventory-really-measure-conceptual-understanding-of-calculus/

### The mechanic

Every six weeks the student works released AP free-response material under the published part timings, scored per point, reported beside the internal mastery count and never merged with it. A stable internal concept probe, a fixed item set never used for practice, runs on a slower cadence. The Calculus Concept Inventory is not the criterion, given the psychometric critiques, though its gain figures are cited as context.

### Parameters

| Parameter | Value | Source | Tag |
|---|---|---|---|
| Checkpoint cadence | every 6 weeks | track 1 mastery-learning section | [inferred], tunable |
| Concept probe cadence | every 8 weeks | track 1 calculus-specific section | [inferred], tunable |
| Comparison basis | published 2023 to 2025 per-question means | research/exam/scoring-system.md | [verified] |
| Lowest published question mean in window | 3.09, 2025 Question 2 | research/exam/scoring-system.md | [verified] |
| Highest published question mean in window | 6.45, 2024 Question 1 | research/exam/scoring-system.md | [verified] |
| Points per question | 9 | research/exam/exam-structure.md | [verified] |

### Library IDs used

The checkpoint draws from `data/frq_records.json`, 249 parts across 2012 to 2026, of which 227 carry point totals, each linked to its `point_types` so the checkpoint yields a BC-PT earning vector directly comparable to the 2025 per-point means. Released material is worked, never redistributed: the student sees the official prompt from College Board's published PDFs by reference, and the app stores only the response and the point vector, per [09-security-and-privacy.md](09-security-and-privacy.md).

### Engine rule

None. Checkpoints deliberately do not update D2, for the same reason timed sessions do not: an instrument that also trains the model it measures stops being a measurement. Diagnosed errors do reach D4 so the student gets feedback, which is the one path back into the system.

### Measurement in the product

The checkpoint is the measurement. What is reported is the per-question point vector against the published 2023 to 2025 means and the trajectory over the eight months. The positive result is the student's per-question means rising toward and past the published means on question positions they have covered. The negative result that matters most is internal mastery climbing while the checkpoint stays flat, which is local-test inflation, and the response is to tighten the mastery thresholds rather than change the checkpoint.

## What the evidence does not support

Thin or contested findings the product uses anyway, with the reason. The optimal spacing gap rests on one large trivia study plus one small mathematics study, so the 10 to 20 percent band is a starting point and observed per-item accuracy is allowed to adjust the schedule rather than the published parameter being trusted. Feedback timing is genuinely unresolved, so the product's position that a spaced re-encounter makes the question moot is an inference, not a finding. The worked-example effect has no published switching threshold at all, so every fading parameter here is a guess. Self-explanation carries a real time cost in mathematics, which is why prompts are rationed. Productive failure is g = 0.36 and conceptual only, which is why it is capped at five targets. Multiple representations in calculus has no retrieved effect size and the drill is justified on criterion alignment. Sleep consolidation as a scheduling mechanism failed a preregistered test, so the same-day rule rests on spacing alone and sleep is not sold as the mechanism. Effect sizes for calculus-specific interventions other than the contested Calculus Concept Inventory comparison are unknown. Numbers taken from secondary summaries and tagged single-source throughout include the Cepeda 2006 pooled effect, the Rohrer 2015 percentages, the Hattie and Timperley 0.79, and the Agarwal K-12 proportion. No effect size was retrieved for Kulik and Kulik 1988, for the redundancy effect, or for hypercorrection.

What the product deliberately does not do. There is no chat box beside an unsolved problem: Bastani and colleagues found a plain chat tutor left students 17 percent worse on the unassisted exam while a guardrailed tutor reached parity, so the affordance that feels most like help carries the clearest measured harm. The tutor role exists, is guardrailed, and does not give the final answer during practice. There are no badges, no points for volume, no leaderboards and no confetti; the undermining estimates for tangible expected rewards, d = -0.40 engagement-contingent, -0.36 completion-contingent and -0.28 performance-contingent, plus the streak-gaming failure mode means a volume reward buys engagement at the cost of the behaviour that matters, and with a single student a leaderboard has nothing to rank against. There is no percent-complete bar on the mastery map, because retention decays and a bar that only rises misstates the state of the student's memory; the map fades instead. There are no streak-loss notifications, which are loss-aversion pressure rather than instruction. There is no predicted AP score as a single number, for reasons set out in [05-assessment-modes.md](05-assessment-modes.md). And there is no expectation of two sigma: Bloom's figure is an upper bound from small studies with locally built outcome measures, the replication range is nearer d = 0.4 to 0.8, and this product plans for d = 0.4 to 0.7 and measures itself against released AP material every six weeks to stay honest.

## Time budget

A 45-minute session is the planning default. The table below is a forecast of what the assembled queue is expected to cost and it is never a schedule: it sets no quota, names no days and tells the student nothing about when to work. Every minute has to beat the alternative use of that minute, which is almost always another attempted problem. Every line below is [inferred]; no source gives a session budget for mathematics.

| Block | Minutes | What happens | Why it earns the minutes |
|---|---|---|---|
| Due reviews | 5 | Items covering skills whose retrievability has fallen below desired retention, chosen to retire the most due skills per item | Spacing is the highest-value zero-cost mechanic in the ledger. Repetition compression means one archetype retires several due skills, so five minutes buys more than five minutes of naive review. |
| Fringe learning | 25 | New skills at the outer fringe at their current fading stage, with step-level feedback at stages example and completion | The only place new mastery can be created, and faded examples are slower per item than retrieval, so it takes the largest block. |
| Interleaved mixed review | 12 | A mixed set under the interleaving constraints, a fifth of it representation translation, all at stage unsupported with feedback withheld until submission | Interleaving is d = 0.83 in classroom mathematics and costs nothing extra, being a reordering of work that had to happen. This block also carries the criterion behaviour: unsignposted items, no method cue, no support. |
| Calibration and error notes | 3 | Confidence data closed out, one-line notes on corrected errors, any judgment of learning owed from a previous session | Three minutes buys the cheapest metric in the system, one that needs no control condition and detects the overconfidence that causes premature stopping. |

The blocks total 45 minutes as a forecast only. The session ends when all four blocks are empty. On a light review day it runs short and on a day thick with discriminating probes it runs long, and neither is a failure. A student who finishes in 30 minutes has not cheated the system; the queue was 30 minutes long.

Where the displaced minutes go. A productive-failure opener takes 10 to 15 minutes and replaces the fringe-learning block on the day a conceptual target opens, which happens five times across the course. A timed part drill or full mock replaces the session outright on its own cadence, part drills every two to three weeks and mocks every four to six weeks, more often in the final eight weeks, and updates pacing metrics only. A six-week checkpoint likewise replaces the session and updates nothing in the mastery model. The implementation intention costs about ten minutes once at setup. Everything else here costs either zero student minutes, because it is a reordering or a rendering rule, or about three seconds per item for the confidence rating.
