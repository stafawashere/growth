---
title: Question standards for multiple-choice and short-answer calculus items
research_date: 2026-09-29
status: draft
purpose: How strong item banks write and validate multiple-choice and short-answer items, what the released AP items in the local cache show about the exam's own item style, and a checklist of machine-checkable standards for the item build stage.
---

# Question standards for multiple-choice and short-answer calculus items

Web sources were read on 2026-09-29. For the psychometric literature only abstracts, publisher pages and search summaries were reachable, so each claim taken from a paper is marked as confirmed by that summary or as recalled and not re-read. Released AP structure was measured from the cache without reproducing any stem, figure or rubric text. Exam counts and timings are not restated here and live in `research/exam/exam-structure.md`. Bank figures below were computed on 2026-09-29 over all 3,316 records under `content/items_*`.

## What a Growth item record carries [verified]

Source: 25 records read (5 each from `content/items_gen_unit02`, `items_gen_unit06`, `items_gen_unit09`, `items_unit06_agent`, `items_p1_agent`, taking every Nth file) and a scan of all 3,316.

A record holds `id`, `archetype_id`, `format` (`mcq` 3,261, `short_answer` 55), `stem` (text plus `command_verb` on generated items only), `answer_key` (form `symbolic` 1,707, `statement` 1,131 or `numeric` 478, with MathJSON or a label, and `decimals` and `units` on numeric keys), an ordered `worked_solution` of steps with `rule_named`, exactly four `options`, `calculator_status`, `representation` (one BC-REP id), `skills`, `difficulty_settings` (BC-DF factor and setting), `parameter_draw`, optional `figure` (465 records: table 200, function graph 196, region 36, slope field 21, polar curve 12), and on generated items `predicted_success_probability` and `provenance`.

Each option carries `id`, `is_key`, `error_path` (null on the key, a BC-ERR id on every distractor), and `value` for expression or numeric keys or `label` for statement keys. Generated items add `derivation` and `mechanism` on each distractor. The 786 agent-drafted items lack `command_verb`, `mechanism`, `derivation` and a predicted probability, and carry `drafted_by` and `authored_on` instead. All 55 `short_answer` records still carry four options, so the short-answer format is a presentation choice over the same record.

Bank shape measured today. Key letter: A 826, B 842, C 827, D 821. Calculator status: 615 calculator (18.5 percent), 2,701 no calculator. Stem length: median 45 words, 90th percentile 77, maximum 137 (generated median 47, agent median 38). Distinct stems after masking every number: 2,266 of 3,316.

## 1. Stem clarity and one construct per item [single-source]

Sources: Haladyna, Downing and Rodriguez 2002, Applied Measurement in Education 15(3), 309 to 333, https://www.tandfonline.com/doi/abs/10.1207/S15324818AME1503_5 and https://eric.ed.gov/?id=EJ660246, accessed 2026-09-29; NBME item-writing guide as mirrored at https://health.uconn.edu/faculty-development/wp-content/uploads/sites/69/2017/06/constructing_written_test_questions.pdf, accessed 2026-09-29.

The 2002 taxonomy has 31 guidelines, validated against 27 textbooks and 27 studies published since 1990 (confirmed by the ERIC record). From memory, and not re-read, the stem guidelines are these: each item tests one important content point, the stem states the whole question so that a knowledgeable student could answer before reading the options, wording is direct with no irrelevant material, negative wording is avoided or highlighted, and words repeated across options move into the stem. The NBME guide, per a search summary, adds that options should match in length, detail and complexity, and that grammatical or pattern cues are flaws.

For calculus this gives four working rules. The stem names the object and the ask in one sentence ("find the value of", "which interval"). Given data that is not needed is allowed only when it is the planned lure for a named error path, as in the generated inflow items that state a starting amount the answer must not use. A stem must not bundle a computation with a separate verdict, which is what the bank's statement items do (compute a second derivative and state concavity, ITM-GEN-09002-20). That pairing is defensible on the AP exam because a justification is the construct, but it puts two constructs in one item, so a wrong option cannot be traced to one failure. And `command_verb` should be present on every record, since 786 lack it.

## 2. Distractors from named error paths [single-source]

Sources: Gierl, Bulut, Guo and Zhang 2017, Review of Educational Research 87(6), 1082 to 1116, https://journals.sagepub.com/doi/10.3102/0034654317726529; Gierl, Lai and Turner 2012, Medical Education 46, 757 to 765, https://asmepublications.onlinelibrary.wiley.com/doi/abs/10.1111/j.1365-2923.2012.04289.x; distractor functioning summaries at https://pmc.ncbi.nlm.nih.gov/articles/PMC2713226/ and https://pmc.ncbi.nlm.nih.gov/articles/PMC5395288/, all accessed 2026-09-29; `research/question-analysis/distractor-taxonomy.md`; `research/scoring/chief-reader-findings.md`.

Template-based automatic item generation builds a cognitive model, then an item model with variable slots, then many items (Gierl, Lai and Turner, confirmed). The 2017 review covers developing, analysing and using distractors and the optimal number and order of options (confirmed). Growth already follows the strongest version of this idea, since every distractor is generated from a BC-ERR record rather than from a plausible wrong number.

Functioning is defined in the literature as chosen by at least 5 percent of examinees and negatively correlated with total score, so a distractor chosen by under 5 percent is non-functioning (confirmed by search summaries). One summary reports that 38 percent of distractors in Haladyna and Downing's data fell under 5 percent, and another that only 52.2 percent of 1,542 distractors functioned. These come from classroom and medical tests with many examinees, and Growth cannot measure functioning per item (section 8), so it must instead lint the structure that produces non-functioning options.

The distractor taxonomy records no official rationale for any option in the three released sets, so all 318 option-to-mechanism links there are inferred. The Chief Reader reports document errors per free-response question, not per multiple-choice option, and give means only, so the error catalogue is evidence about what students write, and the mapping from that error to an option value remains the item writer's inference.

Two defects appear in the bank. Distractors that share one error path: 997 of 3,316 records (30.1 percent) have two distractors on the same BC-ERR id and 146 have all three, concentrated in agent items (464 of 786, 59.0 percent, against 533 of 2,530 generated). Two options from one path usually differ by an arithmetic slip, and a student who holds that error sees two nearly equal choices. Second, type mismatch: in the sampled items, a value question offers a function of x as a distractor (ITM-AGT-02002-09) and an exact-value question offers an expression containing the free variable t (ITM-AGT-06012-04). These are almost never chosen, which is the non-functioning case.

Rules on the two composite options, from the NBME summary and the 2002 taxonomy as recalled: avoid "all of the above", and use "none of the above" sparingly. A search summary reports that 80 percent of reviewed sources advise against "all of the above" and 75 percent against "none of the above". The bank has zero such options (measured), so the standard is already met and only needs a lint to keep it so.

## 3. Option-set checks [inferred]

Sources: 2002 taxonomy and NBME summaries as in section 1, Gierl et al. 2017 on ordering; released sets in `cache/text/practice-exam-2012/page-NNN.ocr.txt`, `cache/text/ced/page-NNN.ocr.txt`, `cache/text/sample-questions/page-NNN.ocr.txt`; bank scan.

The published guidance (recalled) is to keep options homogeneous in length and grammar, to order numeric options logically, and to place the key roughly evenly. Measured against that:

| Check | Released AP sets | Growth bank |
|---|---|---|
| Key position balance | CED sample A 6, B 5, C 6, D 5. Standalone sample A 6, B 7, C 6, D 5. 2012 exam A 7, B 9, C 13, D 6, E 10 (`research/question-analysis/mcq-analysis.md`) | A 826, B 842, C 827, D 821, balanced |
| Numeric options in sorted order | 10 of 11 all-number option sets ascending (5 of 5 in the 2012 exam, 5 of 6 in the four-option sets), 1 descending | 34 ascending, 29 descending, 735 unsorted of 798 all-number sets (92.1 percent unsorted) |
| Key is the middle value | not testable at n of 11 | key is the second or third smallest in 530 of 798 (66.4 percent) against 50 percent expected for a random key |
| Statement key is the longest option, ties included | not measured | 461 of 1,131 (40.8 percent) against about 25 percent expected |
| Composite options | none seen in the released sets | 0 |
| Key negation as a distractor | not measured | 0 of 1,131 statement items with an option that differs from the key only by "not" |

The middle-value cue is real in the bank. Distractors built by perturbing the key land on both sides of it, so the key drifts to the middle. Sorting numeric options ascending, as the exam does, removes the position information from the value order and lets the shuffled key letter carry no cue. The longest-option cue is milder because 936 of 1,131 statement items open every option with the same word, but at 40.8 percent it is above chance and comes from the key being the fully justified sentence while distractors drop a clause.

## 4. Cognitive-level mix [single-source]

Sources: `research/exam/exam-blueprint.md` citing `cache/text/ced/page-205.txt` and `cache/text/ced/page-206.txt`; `research/question-analysis/mcq-analysis.md`.

The CED weights Section I as follows: Practice 1 Implementing Mathematical Processes 50 to 70 percent, Practice 2 Connecting Representations 15 to 30, Practice 3 Justification 10 to 20, Practice 4 Communication and Notation not assessed in multiple choice. The CED also says both exams carry a roughly equal mix of procedural and conceptual tasks (`cache/text/ced/page-206.txt`).

Among the 22 CED sample items that carry a skill code, 10 are Practice 1, 5 are Practice 2 and 7 are Practice 3, with no Practice 4. That is one sample, and Practice 3 lands above its band, so the sample should not be treated as a weighting. No cached Chief Reader report uses Bloom levels (searched `cr-22`, `cr-23`, `cr-24`, `crabbc-25`, `ced` on 2026-09-29, no hit). The reports give a mean out of 9 per question and per-point means only in 2025, so the exam's own cognitive tagging is the practice skills and the procedural or conceptual split, not Bloom. A Bloom-style label would be Growth's own construct and should be marked so.

For the bank, three levels can be assigned from fields already present. Procedural is a symbolic or numeric key with no `justify`, `explain` or `interpret` verb. Conceptual is a `statement` key that asks for a theorem, condition or relation. Interpretive is a contextual representation (BC-REP-05, 353 records) whose stem asks for meaning or units. Of `command_verb` values present, `find` is 1,664, `determine` 249, `justify` 132, `approximate` 98, `interpret` 88, so the bank leans procedural, and the 786 records without a verb cannot be classed. All 154 items whose verb is `justify` or `explain` use the statement key form, so justification is always a choice among sentences, never a produced argument.

## 5. Calculator and no-calculator balance [single-source]

Sources: `research/exam/exam-structure.md` (the only file that states counts), `research/question-analysis/calculator-vs-noncalculator.md`, and the plan 04 rejection rule 8.

Which parts allow a calculator, and how many items and minutes each has, is in `research/exam/exam-structure.md`. The two calculator parts are a minority of Section I by item count, and the Growth bank is 18.5 percent calculator (615 of 3,316), so the shares can be compared directly from that file when the build stage sets a target. The released sets show the same lean: no-calculator 15 of 22, 16 of 24 and 28 of 45.

A calculator item must require the calculator for a step no closed form gives (a definite integral of a non-elementary function, a numeric root, a speed or derivative value at a decimal input), state the answer to three decimal places (the scoring note cited in plan 04), and in a short-answer or free-response frame ask for the setup beside the result (`research/question-analysis/calculator-vs-noncalculator.md`). A no-calculator item must be closed-form solvable by hand. 528 of 615 calculator items say "decimal" in the stem, so 87 do not state the precision. 48 of 440 calculator items with a numeric key store fewer than three decimals (for example 5.7 for 5.700), which matters if the renderer prints the stored value, because the key would then read differently from its three-decimal siblings.

Several calculator distractors in the sampled items use a degree-mode error path, which is a calculator-specific error the exam's Chief Reader reports also list as a radian-mode reminder (`research/scoring/chief-reader-findings.md`, 2022 question 1 advice).

## 6. Representation variety [inferred]

Sources: `research/question-analysis/mcq-analysis.md` (representation table, 91 records), `research/exam/exam-blueprint.md`, `cache/text/ced/page-205.txt`.

Practice 2, Connecting Representations, is weighted 15 to 30 percent of Section I, and the CED names analytical, graphical, tabular and verbal representations. Across the 91 released records, counted per record with a graph, table, slope field or geometric diagram: CED sample 7 of 22, standalone sample 8 of 24, 2012 exam 10 of 45, total 25 of 91 (27.5 percent). Symbolic only: 4, 5 and 14, total 23 of 91 (25.3 percent). A record carries more than one representation tag in 28 of 91. Verbal is tagged on only 3 of 91, and many items are contextual instead.

Growth bank representation: symbolic 1,330 (40.1 percent), contextual 353, series 352, table 268, polar 232, differential equation 226, graph 208, vector 128, verbal 72, parametric 64, geometric 36, calculator-generated 26, slope field 21. 465 records (14.0 percent) carry a figure, against 27.5 percent of released items with a visual. The gap is one to close for graphs and tables, since a figure is what makes Practice 2 items possible.

Two cautions. Released items with a graph mostly hide the key behind a figure, so tagging for a graph in the stem and requiring the figure in the record are separate checks. And figure-bound options such as candidate graphs cannot be produced by the current text options, which matches the 28 undetermined option entries in the distractor taxonomy.

## 7. Free-response justification habits in daily items [single-source]

Sources: `research/scoring/justification-requirements.md`, `research/scoring/command-verbs.md`, `research/question-analysis/calculator-vs-noncalculator.md`.

The scoring files record that "justify" requires a reason tied to the object the prompt names, theorem hypotheses checked, global against local arguments stated, and sign analysis shown, and that units and the setup accompany a calculator answer. A daily item can rehearse one of those without per-point grading by making the justification the thing chosen or ordered rather than free text. The bank does this: 154 justify or explain items pick among sentences whose distractors are one error path each (the converse of a theorem, a missing hypothesis, a wrong object).

Three habits can be carried into daily items cheaply. Give one theorem-hypothesis item per theorem in which the missing hypothesis is the only wrong element. Give interpret-with-units items whose options differ only in the unit or the quantity named, so a wrong choice names the misreading. For calculator items, keep the "show the setup" clause as a second question after the numeric answer (choose the integral that was entered) so the setup rule is rehearsed and still auto-graded. Free-text setup can stay in the FRQ path. This is a design suggestion from the scoring files and has no direct evidence on retention, which the learning-science file covers.

## 8. Difficulty estimation from response data and a-priori factors [uncertain]

Sources: https://www.rasch.org/rmt/rmt74m.htm and https://journals.sagepub.com/doi/10.1177/25152459251314798 (Schroeders and Gnambs 2025, sample-size planning for IRT), accessed 2026-09-29; `research/question-analysis/difficulty-factors.md`; `research/scoring/chief-reader-findings.md`.

Classical statistics are the proportion correct (p-value) per item and the point-biserial between item score and rest-of-test score. Both need many examinees per item. Summaries of the IRT sample-size literature say a Rasch or one-parameter model can be calibrated with roughly 100 to 200 examinees, and two- or three-parameter models need 200 to 500 or more (search summary, not re-read in full). The published guidance therefore assumes hundreds of responders per item.

The College Board's own reporting is coarse. The Chief Reader reports give a mean score out of 9 per free-response question, and per-point means only in 2025 (`research/scoring/chief-reader-findings.md`). The released multiple-choice sets publish no p-values or option frequencies (`research/question-analysis/mcq-analysis.md`). There is no external calibration for any released multiple-choice item.

For Growth, a bank of 3,316 items and one student is a bank with about one response per item at most. It cannot estimate per-item p-values, point-biserials, per-item IRT parameters or distractor functioning. What it can estimate is pooled. The student's ability, with the a-priori difficulty as a prior. The pooled effect of each difficulty dial setting, since `predicted_success_probability` takes only about eight distinct values (0.0573 to 0.5866, 2,530 records). The pooled selection rate of each BC-ERR path across all items that use it, which is the measurement the diagnostic already needs. The stored predicted probability is a dial output, not response data, so it should not be reported as measured difficulty. The a-priori factors in `research/question-analysis/difficulty-factors.md` (concepts combined, prerequisite depth, representation, algebraic burden, justification demand) are the available levers, and 11 are tagged verified and 6 inferred there.

## 9. Key verification [single-source]

Sources: `docs/plan/04-item-generation.md` (Independent key verification, Rejection rules); `app/items/ingest.py`, `app/items/distractor_paths.py`, `tools/key_recheck.py`, `tools/check_items.py`; https://gradientscience.org/gsm8k-platinum/ and https://arxiv.org/pdf/2502.03461, accessed 2026-09-29; BUILD-LEDGER.md (key audit).

What the pipeline does per plan 04: a blind independent re-solve by a different model, SymPy equivalence, numeric probes at several points, a Monte Carlo family check on the parameter spec, a calculator-boundary assertion, unanimity to publish, and a hand-audited key error rate gate. `tools/check_items.py` runs only a subset (section 12): key against the worked solution symbolically and numerically, distractors against the key and each other, and error-path resolution. It is not an independent re-solve, since the solution it compares against was produced with the key. `tools/key_recheck.py` is the blind check, computing the answer from the stem alone.

Published error rates for benchmark math items are the best available comparison. The GSM8K-Platinum work flagged about 5 percent of GSM8K test questions as problematic (search summary of the Gradient Science post: 219 flagged, 110 removed, 99 verified, 10 mislabeled). One secondary summary states that math benchmarks carry up to 5 to 10 percent mistaken labels, which I could not trace to a primary source, so it stays uncertain. No published error rate for LLM-generated AP-level calculus items was found. Growth's own audit ledger records 0 of 100 key errors, with a Wilson 95 percent upper bound of 0.037 (BUILD-LEDGER.md), which cannot exclude a rate under 3.7 percent.

Spot check during this research: for 15 of the 25 sampled items I recomputed the key independently (finite-difference or closed form) and found no key errors. The ten items I could not recompute from the record are figure-bound or statement-form (ITM-GEN-02004-02, ITM-GEN-02005-18, ITM-GEN-02012-07, ITM-GEN-06003-06, ITM-GEN-06014-09, ITM-GEN-09002-20 and ITM-GEN-99005-02 partly, plus items whose figure or table I did not rebuild). Statement keys are checked only by label identity, so a wrong verdict sentence would pass `check_items.py`. Statement items are 34.1 percent of the bank, which is the largest unverified surface.

## 10. What the released AP items show about the exam's own item style [inferred]

Sources: `cache/text/practice-exam-2012/page-005.txt` to `page-050.txt` (stem measurements), `research/question-analysis/mcq-analysis.md`, the CED sample questions on `cache/text/ced/page-208.txt` to `page-221.txt`, `cache/text/sample-questions/`. Structure only.

Option count is four in the two current-framework sets and five in the 2012 exam. Stems are short. In the 2012 exam, 43 of 45 stems could be parsed, and the median stem has about 15 alphabetic tokens (mean 18.8, maximum 69), which undercounts because the text layer drops typeset mathematics. About half open with "Which of the following" (21 of 43), 12 open "What is", and 12 refer to a graph. Ten in eleven numeric option sets are in ascending order. Options that are expressions are parallel in form. Options that are statements are short parallel clauses, not multi-sentence arguments.

Representation: 27.5 percent have a visual, 25.3 percent are symbolic only, and contextual models appear in 10 of 91. Calculator status splits 59 no-calculator against 32 calculator across all 91. Command verbs in multiple choice are few, mostly "find", "which", "what is the value", and there are no justify prompts, consistent with Practice 4 not being assessed in Section I. The CED states that at least two questions per exam use a real-world context (`cache/text/ced/page-206.txt`).

Contrast with the bank: bank stems are longer (median 45 words against about 15 alphabetic tokens, though the two counts are not comparable for math-heavy stems), 34.1 percent are statement items with sentence options against none I could identify in the released sets (not measured exactly), options are unsorted, and 14.0 percent carry a figure against 27.5 percent. The released items are terse and mostly symbolic or numeric, with sorted numeric options.

## 11. Duplicate and near-duplicate control [uncertain]

Sources: Broder 1997 via https://blog.nelhage.com/post/fuzzy-dedup/ and https://arxiv.org/pdf/2501.01046, accessed 2026-09-29; Gierl and Lai item-model definition (section 2); `app/generation/dedupe.py`, `tools/duplicate_sample.py`, plan 04 rejection rules 10 to 12.

MinHash estimates Jaccard similarity between shingle sets and locality-sensitive hashing finds candidate pairs above a threshold. Thresholds in the sources range from 0.4 to 0.8 depending on purpose, so no threshold is defensible without a labelled sample, which is what `tools/duplicate_sample.py` builds. Embedding cosine catches paraphrase but not equal-structure items with different numbers.

Under parameter variation the useful distinction is between duplicates and siblings. Sibling items share one item model, a stem that is identical after every number is masked, and differ only in the draw. In the bank, 2,266 distinct masked stems cover 3,316 records, 505 masked stems are shared by two or more records, and the largest family has 22. Siblings are not duplicates for scoring, but they are for spacing and for evidence, since a student who solves one sibling has learned its procedure and the next tests recall rather than transfer. Recommended definition: exact duplicate is equal masked stem and equal masked option structure with equal draw. Sibling is equal masked stem with a different draw. Near duplicate is a MinHash or cosine hit at the calibrated threshold across different masked stems. Serve siblings at spaced intervals and count them as one exposure to the archetype for mastery purposes. This is a design proposal, not a finding.

## 12. Checklist of machine-checkable standards [inferred]

Sources: `tools/check_items.py`, `app/items/ingest.py`, `app/items/distractor_paths.py`, read 2026-09-29. "Covered" means `tools/check_items.py` fails the record today. "Measured" numbers are today's bank scan.

| Standard | Covered by check_items.py | Measured today |
|---|---|---|
| Exactly one option has is_key true | Yes | not needed |
| Every distractor has an error_path that resolves in its archetype's skills | Yes | 0 missing |
| No distractor equals the key symbolically or numerically (value items) | Yes | not needed |
| Distractors pairwise distinct (value items; label text for statement items) | Yes | 0 duplicate |
| Key equals the worked solution's final step symbolically and numerically (value items) | Yes | not needed |
| Statement key label matches the is_key option label | Yes, label identity only | not needed |
| Exactly four options | No | 3,316 of 3,316 |
| Key letter balance per archetype and per bank | No | balanced overall |
| Numeric options sorted ascending | No | 92.1 percent unsorted |
| Key not the median value more than chance | No | 66.4 percent interior |
| Statement key not the longest option more than chance | No | 40.8 percent longest |
| Distractors from distinct error paths (no two share one) | No | 30.1 percent violate |
| Option type homogeneity, no free variable in a value option | No | 2 sampled defects |
| Every distractor carries mechanism and derivation | No | 2,358 lack both |
| Every stem carries command_verb | No | 786 missing |
| Calculator stem states three decimals, stored key keeps three decimals | No | 87 stems, 48 keys |
| No-calculator item needs no numeric root-finding (rule 8) | No | not measured |
| Stem refers only to a figure the record carries (rule 13) | No | not measured |
| No "all of the above" or "none of the above" | No | 0 |
| Stem length cap (for example 90 words) | No | 10 percent over 77 |
| Short-answer stem is not worded as a choice | No, `tools/key_recheck.py` only | 0 |
| Masked-stem family cap and near-duplicate gate | No, `app/generation/dedupe.py` only | largest family 22 |
| Independent blind re-solve of the key | No, `tools/key_recheck.py` only | 0 of 100 audited wrong |
| Statement key verified beyond label identity | No | 1,131 items |

## Findings from the 25 sampled items [verified]

Source: the 25 records named in section 9, read on 2026-09-29. Keys were recomputed by closed form or finite difference for the value items. Defects are structural, not wrong keys.

| Item | Finding |
|---|---|
| ITM-AGT-06010-00 | All three distractors carry BC-ERR-06026, so one error path fills three options |
| ITM-AGT-06013-08 | Three distractors share BC-ERR-99012 |
| ITM-AGT-01008-03 | Three distractors share BC-ERR-01017 |
| ITM-AGT-06012-04 | Two distractors share BC-ERR-06028, and option D contains the free variable t in an exact-value question |
| ITM-AGT-06002-12 | Two distractors share BC-ERR-99028 |
| ITM-AGT-02002-09 | Format is short_answer yet four options are stored, and two options are functions of x for a value question |
| ITM-GEN-06006-08, ITM-GEN-09006-18 | Numeric keys stored as 14.64 and 5.7 while the stem asks for three decimals |
| ITM-AGT items in general | No command_verb, mechanism or derivation fields, so they cannot be linted on those |

## Open questions for the build stage [uncertain]

The sources above do not settle these, and each needs an operator or measurement decision.

Whether the 2027 Section I keeps four options is unknown, as plan 04 already records, so option count should stay a stored per-item value and the lint should read it. The literature on three options (Rodriguez 2005, https://onlinelibrary.wiley.com/doi/10.1111/j.1745-3992.2005.00006.x, confirmed by the abstract summary that three options are generally optimal) applies to timed tests with many items, and does not change the exam's own format, so it argues for fewer distractors per item only if a daily item is meant to be quick.

Whether statement items should stay at a third of the bank is a product question. They rehearse justification cheaply, but they are the least verifiable form and the source of the longest-option cue.

Which threshold separates a sibling from a near duplicate must be set on the labelled sample from `tools/duplicate_sample.py`, not chosen here.

Whether the daily flow should sort numeric options before display or keep the stored order is a rendering decision. The exam sorts them, and the stored order is the generator's.
