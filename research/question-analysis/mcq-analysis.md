---
title: AP Calculus BC Multiple-Choice Question Analysis
research_date: 2026-09-19
status: draft
purpose: What College Board states publicly about how multiple-choice questions are built and tagged, the inventory of public official sample multiple-choice material, and the distribution of the indexed questions by unit, practice skill, representation, and archetype.
---

# AP Calculus BC Multiple-Choice Question Analysis

This file is a view over the 91 records in `../../data/mcq_records.json`. Section and timing facts live in [exam-structure.md](../exam/exam-structure.md) and weighting facts in [exam-blueprint.md](../exam/exam-blueprint.md); neither is restated here. The per-question table is in [official-sample-question-index.md](../official-material/official-sample-question-index.md) and the mechanism catalogue is in [distractor-taxonomy.md](distractor-taxonomy.md).

## What College Board states about multiple-choice construction [verified]

The course and exam description sets out, on `ced:205`, what the multiple-choice section draws on. It names the function families the section uses, listing algebraic, exponential, logarithmic, trigonometric, and general types, and it names the representation types, listing analytical, graphical, tabular, and verbal. It states that Mathematical Practices 1, 2, and 3 are assessed in the multiple-choice section and that Practice 4 is not assessed there, with a published weighting band for each of the three. It also publishes a unit-by-unit weighting band for the multiple-choice section on `ced:204`, given separately for AB and for BC.

The sample question framing on `ced:208` states that the sample questions illustrate the relationship between the course framework and the exams and serve as examples of the types of questions that appear on them. It states that a table after the questions shows which skill, learning objective, and unit each question relates to, and that the same table provides the answers to the multiple-choice questions. That table, on `ced:221`, is the tagging that this library reads: one practice skill code such as BC-MPS-1E, one learning objective code, and one unit number per question, alongside the answer letter. No rationale, no explanation of any option, and no difficulty statistic accompany any of it.

The older standalone sample set carries a different tagging scheme. Its introduction on `sample-questions:4` states that each question is accompanied by a table of the main learning objectives, essential knowledge statements, and Mathematical Practices for AP Calculus that the question addresses, that an answer key is provided for the multiple-choice questions, and that where several are listed the primary one is listed first. It also states that the information is intended to aid in identifying the focus of the question and that objectives, statements, and practices other than those listed may also partially apply.

## Inventory of public official multiple-choice sources [verified]

Three cached documents carry official multiple-choice material with answer keys. Together they supply the 91 indexed questions.

| Source | Document | Indexed questions | No calculator | Calculator | Options per question | Official tags |
|---|---|---|---|---|---|---|
| BC-SRC-ced | Course and exam description, sample questions section, `ced:208` to `ced:221` | 22 | 15 | 7 | 4 | practice skill, learning objective, unit |
| BC-SRC-sample-questions | Standalone sample questions, originally published in the fall 2014 curriculum framework | 24 | 16 | 8 | 4 | learning objectives, essential knowledge, mathematical practices of the 2014 framework |
| BC-SRC-practice-exam-2012 | 2012 released BC practice exam, Section I | 45 | 28 | 17 | 5 | none |

Across all three, 59 of 91 are on a part where a graphing calculator is not permitted and 32 are on a part where one is required or permitted. The 2012 exam is the only source with five options; both current-framework sources use four. The course and exam description set is split into a part answered by both AB and BC candidates, indexed here as scope `shared`, and a part answered only by BC candidates, indexed as `BC_only`; the standalone set is split the same way into an AB set of 16 and a BC set of 8. Every record in the 2012 set is scoped `BC_only` because the document is the BC exam, although several of its items cover content shared with AB.

## Distribution by unit [inferred]

Each record carries the topic or topics the question exercises; the unit below is the unit of the first topic listed. Denominator is 91.

| Unit | Course and exam description | Standalone sample set | 2012 practice exam | Total | Share of 91 |
|---|---|---|---|---|---|
| BC-UNIT-01 Limits and Continuity | 2 | 1 | 2 | 5 | 5.5% |
| BC-UNIT-02 Differentiation: Definition and Basic Rules | 2 | 2 | 3 | 7 | 7.7% |
| BC-UNIT-03 Composite, Implicit, and Inverse Functions | 1 | 0 | 2 | 3 | 3.3% |
| BC-UNIT-04 Contextual Applications of Differentiation | 2 | 3 | 2 | 7 | 7.7% |
| BC-UNIT-05 Applying Derivatives to Analyze Functions | 2 | 3 | 6 | 11 | 12.1% |
| BC-UNIT-06 Integration and Accumulation of Change | 4 | 3 | 11 | 18 | 19.8% |
| BC-UNIT-07 Differential Equations | 2 | 3 | 4 | 9 | 9.9% |
| BC-UNIT-08 Applications of Integration | 2 | 3 | 4 | 9 | 9.9% |
| BC-UNIT-09 Parametric, Polar, and Vector-Valued Functions | 2 | 2 | 3 | 7 | 7.7% |
| BC-UNIT-10 Infinite Sequences and Series | 3 | 4 | 8 | 15 | 16.5% |

Units 6 and 10 hold the largest shares at 18 and 15 of 91, and unit 3 the smallest at 3 of 91. This is a property of these three published sets, not a statement about any administered form; the published weighting bands are in [exam-blueprint.md](../exam/exam-blueprint.md).

## Distribution by practice skill [verified]

Only the course and exam description prints a practice skill code, one per question, so the denominator here is 22 and not 91. The remaining 69 records carry an empty `practice_skills` field.

| Practice skill | Count | Share of 22 |
|---|---|---|
| BC-MPS-1D | 1 | 4.5% |
| BC-MPS-1E | 8 | 36.4% |
| BC-MPS-1F | 1 | 4.5% |
| BC-MPS-2B | 1 | 4.5% |
| BC-MPS-2C | 2 | 9.1% |
| BC-MPS-2D | 2 | 9.1% |
| BC-MPS-3D | 6 | 27.3% |
| BC-MPS-3F | 1 | 4.5% |

Grouped by practice, 10 of 22 carry a Practice 1 skill, 5 carry a Practice 2 skill, and 7 carry a Practice 3 skill. Within Practice 1 the tagging concentrates on BC-MPS-1E, and within Practice 3 on BC-MPS-3D. No question in this set carries a Practice 4 skill, which matches the statement on `ced:205` that Practice 4 is not assessed in the multiple-choice section. The 2014 framework tags in the standalone set are mathematical practices of a superseded scheme and are not crosswalked into BC-MPS ids here.

## Representation mix [inferred]

A record may carry more than one representation, so the 91 records carry 119 representation tags in total.

| Representation | Records | Share of 91 |
|---|---|---|
| BC-REP-01 Symbolic (analytical) expression | 36 | 39.6% |
| BC-REP-11 Series | 17 | 18.7% |
| BC-REP-02 Graphical | 14 | 15.4% |
| BC-REP-09 Calculator-generated numerical result | 12 | 13.2% |
| BC-REP-05 Contextual model | 10 | 11.0% |
| BC-REP-06 Differential equation | 9 | 9.9% |
| BC-REP-03 Numerical table | 8 | 8.8% |
| BC-REP-04 Verbal description | 3 | 3.3% |
| BC-REP-12 Parametric equations | 3 | 3.3% |
| BC-REP-13 Polar equation | 3 | 3.3% |
| BC-REP-07 Slope field | 2 | 2.2% |
| BC-REP-08 Geometric diagram | 1 | 1.1% |
| BC-REP-14 Vector-valued function | 1 | 1.1% |

The symbolic representation carries about two questions in five. The four representation types the course and exam description names on `ced:205` map onto BC-REP-01, BC-REP-02, BC-REP-03, and BC-REP-04, which together account for 61 of the 119 tags; the remaining tags record forms that the stem presents but that the published list does not separate, such as a slope field or a series in sigma notation. The catalogue itself is in [representation-types.md](representation-types.md).

## Recurring archetypes [inferred]

The 91 records use 61 distinct archetypes from `../../data/archetypes.json`. Forty of those appear once. The archetypes carrying two or more of the indexed questions are below.

| Archetype | Name | Count |
|---|---|---|
| BC-QA-05009 | Relating the graphs of a function and its first two derivatives | 5 |
| BC-QA-06003 | Accumulation function analysed from the graph of the integrand | 4 |
| BC-QA-02005 | Point of non-differentiability identified on a continuous function | 3 |
| BC-QA-04006 | Related rates in a geometric setting | 3 |
| BC-QA-06008 | Antiderivative or definite integral by substitution | 3 |
| BC-QA-10004 | Convergence or divergence established with a named test | 3 |
| BC-QA-01004 | Indeterminate limit resolved by algebraic rewriting | 2 |
| BC-QA-04009 | Limit of an indeterminate form with L'Hospital's rule | 2 |
| BC-QA-05001 | Mean Value Theorem existence justification on an interval | 2 |
| BC-QA-05005 | Points of inflection identified with a reason tied to the given graph | 2 |
| BC-QA-05008 | Intervals of increase or decrease justified by the sign of the derivative | 2 |
| BC-QA-06009 | Antiderivative by integration by parts | 2 |
| BC-QA-06011 | Improper integral convergence or divergence | 2 |
| BC-QA-06014 | Converting between a limit of Riemann sums and a definite integral | 2 |
| BC-QA-08004 | Amount at a later time from an initial amount and a rate | 2 |
| BC-QA-07002 | Slope field matched to or built from a differential equation | 2 |
| BC-QA-07004 | Euler's method over two steps of equal size | 2 |
| BC-QA-07009 | Logistic model interpreted without solving | 2 |
| BC-QA-08001 | Average value of a function over an interval | 2 |
| BC-QA-08003 | Rectilinear motion analysed with definite integrals | 2 |
| BC-QA-09001 | Slope of the tangent to a parametric path at a time | 2 |

The heaviest recurrence, BC-QA-05009, is the family in which one of a function and its derivatives is supplied and a statement about another is asked for. It occurs in all three sources. The second, BC-QA-06003, always supplies the integrand graphically and asks a question about the accumulation function. Both families are multi-representation by construction, which is consistent with the presence of Practice 2 skills in the tagged subset.

## What the answer keys reveal [verified]

Every source prints a bare answer letter and nothing else. No rationale for any option appears in any of the three documents, so `official_rationale_available` is false on all 91 records and no distractor mechanism in this library carries the `verified` tag.

The letter distributions are as follows. Course and exam description, 22 questions over four options: A 6, B 5, C 6, D 5. Standalone sample set, 24 questions over four options: A 6, B 7, C 6, D 5. The 2012 practice exam, 45 questions over five options: A 7, B 9, C 13, D 6, E 10. The first two are close to uniform. The 2012 spread is wider, with C the most frequent at 13 of 45 and D the least at 6 of 45, on a sample too small to support any claim about key placement as a design property.

The answer key in the course and exam description is also the only place in these three documents where a practice skill and a learning objective are attached to a specific multiple-choice question. The key table on `ced:221` prints the same alignment for the sample free-response questions, in that case as lists of skills rather than one skill per question.

## Limits of this analysis [uncertain]

Three constraints bound what the records can support.

The first is extraction quality. The standalone sample set renders its mathematics as images that the text layer drops, so for 18 of its 24 questions no option text survives at all and the description in each record is reconstructed from the surviving prose and the official tags. The course and exam description linearises its mathematics into read-aloud text that is usable for most items but that failed for questions 13, 14, 15, 17, 18, and 19. The 2012 practice exam extracts well, and its figures, being images, are the main loss there.

The second is the absence of rationales. Because no source explains why an option is wrong, every mechanism in `distractor_analysis` is either an inference from the arithmetic or structure of the printed option, tagged `inferred`, or an admission that the option could not be worked, tagged `uncertain`. Of 318 option entries across the 91 records, 205 are `inferred` and 113 are `uncertain`. None is `verified`.

The third is sample composition. The three documents were published for different purposes across three framework generations, one of them predating the 2019 course framework and one predating the 2014 one. Counting them together, as the unit and representation tables above do, mixes those generations. The counts describe this corpus and nothing beyond it.

## Unresolved [uncertain]

Several specific items could not be settled and are logged here and in `../evidence/unresolved-questions.md`.

The option list cached for the 2012 practice exam question 82 does not contain the value that a direct computation of the requested average gives, so the printed options could not be reconciled with the official key letter. Either the extraction lost or altered an option, or the printed option set differs from what the computation suggests. The record carries all four distractors as `not determined`.

For the 2012 practice exam questions 10, 15, 18, 84, and 88, and for course and exam description questions 13, 15, 17, 18, and 19, the stem, the figure, or the option set is not recoverable from the cache, so the correct option is taken from the printed key and no mechanism is asserted.

The standalone sample set uses the 2014 mathematical practices rather than the practice skills of the current framework. Whether a defensible crosswalk exists from those practices to BC-MPS ids has not been established, so none was applied, and the practice skill distribution above therefore rests on 22 questions rather than 46.
