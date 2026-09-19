---
title: Claims and Confidence Register
research_date: 2026-09-19
status: draft
purpose: The register of claims a downstream system would rely on, each carrying the evidence tag its source file already assigns, with the source ids behind it, where it is used, and what would change it.
---

# Claims and Confidence Register

This file records claims, not facts. Facts live in `../../data/` and the Markdown views over them. Every row below repeats the tag its source file assigns and never raises it. Exam counts and timings are not restated here; they are in [../exam/exam-structure.md](../exam/exam-structure.md).

## How to read the tags [verified]

Source: [../README.md](../README.md), evidence tags section.

The four tags are defined in the library README. What each one means operationally for a consumer of this library:

`[verified]` means the claim was read out of a primary College Board document held in this project's cache, with the document id and page recorded. A consumer may treat it as the published position of College Board as of 2026-09-19. It does not mean the claim was checked against a second independent publisher, because for most of this material no second publisher exists.

`[single-source]` means one source stands behind the claim, or the only source is secondary. Two distinct situations carry this tag. The first is a live College Board web page with no cached PDF corroboration, as for the exam date and the calculator model list. The second is a cached PDF that yields only one instance of a pattern, as for the point-type families with a single rubric instance. A consumer should carry the claim with an explicit provenance note and should not build a gate on it alone.

`[inferred]` means the claim is a research conclusion drawn from official material rather than a statement lifted from it. Every graph property, every unit-level count derived by a tool, and every prerequisite edge written by a unit agent carries this tag. A consumer may use it for structure and ordering, and should not present it as a College Board statement.

`[uncertain]` means the question could not be settled from the cache. Each one is also logged in [unresolved-questions.md](unresolved-questions.md). A consumer should treat the field as absent rather than as false.

Two mechanical rules hold. `qa/04_tags.py` fails the build if a registry record carries no valid tag, if a record tagged `verified` or `single-source` carries no sources, or if a Markdown H2 carries neither a tag nor an ID. The same check rejects any Chief Reader citation to a report that is not present in `cache/manifest.json` with status `ok`.

## Tag statistics per registry [verified]

Source: `../../tools/tag_stats.py`, run against `../../data/` on 2026-09-19.

Counts are records per `evidence_tag` per collection. The `other` column counts records whose tag is outside the four permitted values and is zero everywhere, which is what `qa/04_tags.py` enforces.

| file | collection | verified | single-source | inferred | uncertain | other | total |
|---|---|---|---|---|---|---|---|
| archetypes.json | archetypes | 84 | 4 | 46 | 0 | 0 | 134 |
| archetypes.json | variants | 81 | 1 | 312 | 0 | 0 | 394 |
| curriculum.json | essential_knowledge | 188 | 2 | 0 | 0 | 0 | 190 |
| curriculum.json | learning_objectives | 81 | 0 | 0 | 0 | 0 | 81 |
| curriculum.json | practice_skills | 23 | 0 | 0 | 0 | 0 | 23 |
| curriculum.json | practices | 4 | 0 | 0 | 0 | 0 | 4 |
| curriculum.json | topics | 111 | 0 | 0 | 0 | 0 | 111 |
| curriculum.json | units | 10 | 0 | 0 | 0 | 0 | 10 |
| diagnostic_signals.json | signals | 128 | 7 | 104 | 0 | 0 | 239 |
| errors.json | errors | 226 | 10 | 188 | 0 | 0 | 424 |
| frq_records.json | records | 226 | 22 | 1 | 0 | 0 | 249 |
| mcq_records.json | records | 91 | 0 | 0 | 0 | 0 | 91 |
| misconceptions.json | misconceptions | 101 | 5 | 130 | 0 | 0 | 236 |
| scoring_points.json | point_types | 61 | 8 | 0 | 0 | 0 | 69 |
| skills.json | concepts | 170 | 0 | 0 | 0 | 0 | 170 |
| skills.json | prerequisites | 0 | 0 | 77 | 0 | 0 | 77 |
| skills.json | skills | 538 | 3 | 0 | 0 | 0 | 541 |
| sources.json | sources | 107 | 1 | 0 | 0 | 0 | 108 |
| taxonomies.json | command_verbs | 22 | 7 | 0 | 0 | 0 | 29 |
| taxonomies.json | difficulty_factors | 11 | 0 | 6 | 0 | 0 | 17 |
| taxonomies.json | representations | 5 | 0 | 9 | 0 | 0 | 14 |
| prereq_edges.csv | edges | 33 | 0 | 912 | 0 | 0 | 945 |
| ALL | all collections | 2301 | 70 | 1785 | 0 | 0 | 4156 |

Three shapes are visible. Collections transcribed directly from the CED are wholly `verified`. Collections that decompose CED content into machine units, meaning the prerequisite edges and the archetype variants, are dominated by `inferred`. Collections read out of rubrics and Chief Reader reports are mixed, with `single-source` marking the families and behaviours that appear once in the corpus. No record in any collection carries `uncertain`; uncertainty is carried by Markdown sections and by [unresolved-questions.md](unresolved-questions.md), not by records.

## Register of claims [verified]

Tags in the Tag column are the tags the cited file already assigns. Source ids follow the citation form used by the cited file, so `ced p.199` is the cached CED at printed page 199 and `sg-25:3` is the cached 2025 scoring guidelines at page 3.

### Exam format for May 2027

| Claim | Tag | Source ids or pages | Where it is used | What would change it |
|---|---|---|---|---|
| The exam has two sections, multiple choice then free response, each split into two parts that differ in calculator status | verified | ced p.198 (PDF p.203); BC-SRC-web-bc-exam | [../exam/exam-structure.md](../exam/exam-structure.md); every part-scoped record | A later CED edition restructuring the sections |
| May 2027 is the first administration under the revised multiple-choice structure | verified | ced p.198; BC-SRC-web-bc-exam; BC-SRC-web-exam-dates | [../exam/historical-changes.md](../exam/historical-changes.md) | A further clarifications document before May 2027 |
| The Fall 2026 clarifications changed the question count and the timing of both multiple-choice parts | verified | ced-clarifications-2026 p.2 | [../exam/historical-changes.md](../exam/historical-changes.md) | A superseding clarifications document |
| The clarifications state no change to Section II, to section weightings, or to unit or practice weightings | verified | ced-clarifications-2026 p.2 | [../exam/exam-blueprint.md](../exam/exam-blueprint.md) | A later document that does state such a change |
| Section II is numbered from the first question onward with the calculator-required questions first | verified | ced p.200; sg-25:2 | [../exam/exam-structure.md](../exam/exam-structure.md); frq records | A scoring guideline that orders the sections differently |
| Every free-response question carries the same point total, stated once in exam-structure.md | verified | stats-23 p.1; stats-24 p.1; stats-25 p.1; sg-25:2 | [../exam/exam-structure.md](../exam/exam-structure.md); [../scoring/point-taxonomy.md](../scoring/point-taxonomy.md) | A scoring statistics file publishing an unequal maximum |
| The free-response section weightings published by the CED follow the question split rather than a published point weighting | uncertain | BC-SRC-web-bc-exam; ced p.198 | [../exam/exam-structure.md](../exam/exam-structure.md) Unresolved | A College Board statement of raw point weights |
| The 2027 administration is scheduled for Monday, May 10, 2027, Session 1 | single-source | BC-SRC-web-exam-dates | [../exam/exam-structure.md](../exam/exam-structure.md); [../exam/historical-changes.md](../exam/historical-changes.md) | A cached PDF calendar, or a College Board schedule revision |
| Whether the May 2026 administration used the prior or the revised multiple-choice counts is not established | uncertain | ced-clarifications-2026 p.2 | [../exam/historical-changes.md](../exam/historical-changes.md); [unresolved-questions.md](unresolved-questions.md) | A 2026 exam instructions document or a 2026 statistics file |

### Delivery and calculator

| Claim | Tag | Source ids or pages | Where it is used | What would change it |
|---|---|---|---|---|
| The exam is administered in a hybrid digital format, with multiple choice answered in Bluebook and free-response answers handwritten in paper booklets | single-source | BC-SRC-web-bc-students | [../exam/exam-structure.md](../exam/exam-structure.md); [../exam/historical-changes.md](../exam/historical-changes.md) | A cached College Board PDF describing delivery, or a move to fully digital free response |
| A graphing calculator for the exam is expected to have four built-in capabilities: plotting in an arbitrary window, solving numerically, numeric differentiation, numeric definite integration | verified | ced p.8 (PDF p.13) | [../exam/calculator-policy.md](../exam/calculator-policy.md); calculator relevance fields on skill records | A CED revision to the capability list |
| A free-response result obtained from one of the four capabilities must show the setup together with the result | verified | ced p.8; sg-25:3 | [../exam/calculator-policy.md](../exam/calculator-policy.md); BC-PT-99005 | A CED revision to the answer-recording rule |
| Use of calculator features outside the four capabilities requires the mathematical steps that produced the result | verified | ced p.8 | [../exam/calculator-policy.md](../exam/calculator-policy.md) | A CED revision to the same paragraph |
| A student may bring up to two handheld graphing calculators | single-source | BC-SRC-web-calc-policy | [../exam/calculator-policy.md](../exam/calculator-policy.md) | A change to the published calculator policy page |
| Bluebook includes a built-in Desmos graphing calculator whose availability follows the part boundaries exactly | single-source | BC-SRC-web-calc-policy; BC-SRC-web-bc-students | [../exam/calculator-policy.md](../exam/calculator-policy.md) | A policy change to in-application tool availability |
| Whether the built-in Desmos satisfies all four CED capabilities, and how it counts against the two-handheld allowance, is not established | uncertain | BC-SRC-web-calc-policy | [../exam/calculator-policy.md](../exam/calculator-policy.md); [unresolved-questions.md](unresolved-questions.md) | A College Board statement on the in-application tool |
| A reported decimal approximation must be accurate to three places after the decimal point, and may be rounded or truncated | verified | sg-25:2; sg-25:3 | [../scoring/scoring-patterns.md](../scoring/scoring-patterns.md); precision fields on point types | A change to the general scoring notes |
| Within a free-response question at most one point is not earned for inappropriate rounding | verified | sg-25:2; sg-26:2 | [../exam/calculator-policy.md](../exam/calculator-policy.md); [../scoring/scoring-patterns.md](../scoring/scoring-patterns.md) | A change to the general scoring notes |

### Weightings

| Claim | Tag | Source ids or pages | Where it is used | What would change it |
|---|---|---|---|---|
| Unit weightings are published for the multiple-choice section only, and no unit weighting is published for the free-response section | verified | ced p.199 (PDF p.204) | [../exam/exam-blueprint.md](../exam/exam-blueprint.md); unit records | A CED that publishes free-response unit weightings |
| Each BC unit weighting is a range, so the table constrains rather than fixes the composition of a form | verified | ced p.199 | [../exam/exam-blueprint.md](../exam/exam-blueprint.md); [../curriculum/curriculum-map.md](../curriculum/curriculum-map.md) | A CED that publishes point weights per unit |
| Units 9 and 10 are marked BC ONLY, so AB is assessed over eight units and BC over ten | verified | ced p.199 | [../exam/exam-blueprint.md](../exam/exam-blueprint.md); scope fields on topic records | A CED that moves content across the AB boundary |
| BC-MP-4 and all five of its skills are not assessed in the multiple-choice section | verified | ced p.200 | [../exam/exam-blueprint.md](../exam/exam-blueprint.md); [../exam/mathematical-practices.md](../exam/mathematical-practices.md) | A CED revision to the practice weighting table |
| All four practices are assessed in the free-response section | single-source | ced p.201 (PDF p.206) | [../exam/exam-blueprint.md](../exam/exam-blueprint.md) | A CED revision, or a clean extraction of the same table |
| The free-response practice percentages are paired to practices by list order in the cached extraction, not by an intact table row | single-source | ced p.201 | [../exam/exam-blueprint.md](../exam/exam-blueprint.md); [../curriculum/curriculum-map.md](../curriculum/curriculum-map.md) | Reading the rendered PDF table instead of the text layer |
| Section I and Section II each carry half the exam weight | verified | ced p.198 | [../exam/exam-structure.md](../exam/exam-structure.md) | A CED revision to the exam overview |
| The AB and BC exams share three free-response questions, printed on both forms and scored against one rubric | verified | ced p.201; sg-25:2 | [../exam/exam-blueprint.md](../exam/exam-blueprint.md); scope on frq records | A scoring guideline with a different shared-question count |
| The AB subscore covers the portion of the BC exam that carries AB content, characterised on one web page as roughly 60 percent | single-source | BC-SRC-web-ab-subscore; ced p.201 | [../exam/exam-blueprint.md](../exam/exam-blueprint.md) | A College Board publication of the subscore composition |
| The Course at a Glance PDF prints weightings that no longer match the CED exam overview and is excluded as a source | single-source | BC-SRC-web-bc-course | [../exam/historical-changes.md](../exam/historical-changes.md) | College Board reissuing the Course at a Glance against the current CED |

### Scoring conventions

| Claim | Tag | Source ids or pages | Where it is used | What would change it |
|---|---|---|---|---|
| Multiple choice is machine scored, free response is scored at the AP Reading, and the weighted combination is converted to a composite on a 1 to 5 scale | verified | ced p.3 (PDF p.8) | [../exam/scoring-system.md](../exam/scoring-system.md) | A CED revision to the scoring paragraph |
| The multiple-choice score is the count of correct answers with no deduction for incorrect answers | single-source | BC-SRC-web-score-setting | [../exam/scoring-system.md](../exam/scoring-system.md) | A cached PDF corroboration, or a policy change |
| AP Exams are criterion referenced rather than norm referenced or curved | verified | ced p.3 | [../exam/scoring-system.md](../exam/scoring-system.md) | A CED revision to the score-setting paragraph |
| The raw weight of multiple choice against free response, the composite maximum, and the cut scores are not published anywhere in this corpus | inferred | ced p.3; BC-SRC-web-score-setting | [../exam/scoring-system.md](../exam/scoring-system.md); [unresolved-questions.md](unresolved-questions.md) | College Board publishing a raw-to-composite mapping |
| The same general scoring notes block opens every question in sg-22 through sg-26 | verified | sg-22:2; sg-23:2; sg-24:2; sg-25:2; sg-26:2 | [../scoring/scoring-patterns.md](../scoring/scoring-patterns.md) | A guideline year that drops or rewrites the block |
| Answers, numeric or algebraic, need not be simplified | verified | sg-25:2 | [../scoring/scoring-patterns.md](../scoring/scoring-patterns.md); `simplification_required` on point types | A guideline that requires simplification |
| Some answer points are earned with or without supporting work, and others require the supporting step | verified | sg-25:3; sg-25:7; sg-25:4; sg-25:8 | BC-PT-99004; BC-PT-99005 | A rubric that collapses the two forms |
| Incorrect or unclear communication between a correct integral and a correct answer is treated as scratch work in sg-25 and sg-26 | verified | sg-25:3; sg-26:9 | [../scoring/scoring-patterns.md](../scoring/scoring-patterns.md); BC-PT-99004 | A later guideline restoring a deduction |
| Banking is the rubric's own word for a point that later simplification or rounding errors cannot remove | verified | sg-25:13; sg-25:14; sg-25:21; sg-25:23; sg-26:3; sg-26:11; sg-26:20 | [../scoring/scoring-patterns.md](../scoring/scoring-patterns.md); eligibility fields on point types | A rubric that withdraws banked points |
| Eligibility runs three ways: a point may require an earlier point, may be blocked by a specific error, or may survive the loss of its neighbour | verified | sg-25:12; sg-25:13; sg-25:14; sg-25:25; sg-26:8; sg-26:16; sg-26:22; sg-22:5 | [../scoring/scoring-patterns.md](../scoring/scoring-patterns.md); `dependency` on point types | A rubric that scores points independently throughout |
| The rubric is point by point rather than holistic, with each point carrying its own earning condition | verified | sg-25:2; sg-25:3 | [../exam/scoring-system.md](../exam/scoring-system.md); the whole point taxonomy | A move to holistic scoring |
| Justify, give a reason, and give reasons are three different demands with different point structures | verified | sg-25:5; sg-25:17; sg-26:15; sg-26:17; sg-24:4 | [../scoring/justification-requirements.md](../scoring/justification-requirements.md); BC-PT-99010 | A guideline that treats the verbs alike |
| A local argument does not earn a justification point for a global claim, though the answer point stays available | verified | sg-25:5; sg-25:9; sg-25:19 | [../scoring/justification-requirements.md](../scoring/justification-requirements.md); BC-ERR-99004 | A guideline that accepts a bare derivative test |
| A candidates test justification must evaluate the interior critical point and both endpoints, and an error at any candidate forfeits the point | verified | sg-25:5; sg-25:19; sg-23:15 | [../scoring/justification-requirements.md](../scoring/justification-requirements.md); BC-PT-99011 | A guideline that accepts a partial candidate set |
| An existence hypothesis point is earned by deriving continuity from differentiability, not by asserting continuity | verified | sg-25:12; sg-26:5; sg-22:14 | [../scoring/justification-requirements.md](../scoring/justification-requirements.md); BC-PT-99015 | A guideline that accepts a bare assertion |

### Score distributions

| Claim | Tag | Source ids or pages | Where it is used | What would change it |
|---|---|---|---|---|
| The published BC score distributions for 2023, 2024 and 2025 are reproduced at the precision each file publishes | verified | dist-23 p.1; dist-24 p.1; dist-25 p.1 | [../exam/scoring-system.md](../exam/scoring-system.md) | A restated distribution file |
| The 2023 and 2025 BC figures are reproduced identically in the corresponding Chief Reader reports | verified | cr-23 p.1; crabbc-25 p.1 | [../exam/scoring-system.md](../exam/scoring-system.md) | A discrepancy between the two series |
| The AB subscore distributions for 2023 to 2025 are published separately from the BC distributions | verified | absub-23 p.1; absub-24 p.1; absub-25 p.1 | [../exam/scoring-system.md](../exam/scoring-system.md) | A change in reporting practice |
| The subscore count may differ slightly from the BC count because of exam administration incidents, and the 2025 pair differs by one | verified | absub-25 p.1; dist-25 p.1 | [../exam/scoring-system.md](../exam/scoring-system.md) | A restated file, or a removal of the footnote |
| Per-question free-response means and standard deviations are published for 2023 to 2025 | verified | stats-23 p.1; stats-24 p.1; stats-25 p.1 | [../exam/scoring-system.md](../exam/scoring-system.md); [../scoring/chief-reader-findings.md](../scoring/chief-reader-findings.md) | A year with no statistics file |
| The 2025 Chief Reader report publishes a mean for each individual scoring point, which the 2023 and 2024 reports do not | verified | crabbc-25 p.2; cr-23 p.2; cr-24 p.2 | [../exam/scoring-system.md](../exam/scoring-system.md); [../exam/exam-construction.md](../exam/exam-construction.md) | A later report dropping or restoring point-level means |
| Nothing is published about multiple-choice item difficulty, and no cached source gives a raw-score-to-composite mapping for any year | inferred | ced p.3; BC-SRC-web-score-setting | [../exam/scoring-system.md](../exam/scoring-system.md) | An item-level technical release |

### Corpus coverage

| Claim | Tag | Source ids or pages | Where it is used | What would change it |
|---|---|---|---|---|
| The coverage matrix states ok, archived_only, or not_obtained per document and year, and a not_obtained cell is a statement about this project's fetch attempts | verified | [../official-material/official-question-index.md](../official-material/official-question-index.md); cache/manifest.json | Every document-scoped claim in the library | Re-running `tools/fetch_corpus.py` against new URLs |
| 2023 to 2025 are complete across all seven document types | verified | [../official-material/official-question-index.md](../official-material/official-question-index.md) | [../scoring/point-taxonomy.md](../scoring/point-taxonomy.md); frq records | A withdrawal from AP Central |
| For 2026 the free-response questions and scoring guidelines are live while samples, statistics, distributions and the Chief Reader report are not yet published | verified | [../official-material/official-question-index.md](../official-material/official-question-index.md) | [../scoring/scoring-patterns.md](../scoring/scoring-patterns.md) | College Board publishing the 2026 remainder |
| 2012 to 2017 free-response questions and scoring guidelines were not obtained at any tried URL | uncertain | [unresolved-questions.md](unresolved-questions.md); BC-SRC-web-bc-past | [../official-material/official-question-index.md](../official-material/official-question-index.md) | A new archive snapshot or a different filename pattern |
| The 2018 scoring guidelines were not obtained under five name variants, so 2018 records carry topics but not scoring points | uncertain | [unresolved-questions.md](unresolved-questions.md) | [../official-material/scoring-guideline-index.md](../official-material/scoring-guideline-index.md) | Recovery of sg-18 |
| 2020 is absent from the corpus entirely and no claim about that administration is made | uncertain | [../exam/historical-changes.md](../exam/historical-changes.md) | [../exam/historical-changes.md](../exam/historical-changes.md) | Recovery of any 2020 document |
| The sg-24 scoring-note prose is absent from the PDF text layer, so 2024 point types carry labels and structure but not rubric wording | verified | [unresolved-questions.md](unresolved-questions.md); sg-24 p.4 | [../scoring/point-taxonomy.md](../scoring/point-taxonomy.md) | An OCR pass over sg-24 |
| Chief Reader evidence may cite only reports present in the manifest with status ok, enforced by qa/04_tags.py | verified | [../README.md](../README.md); qa/04_tags.py | Every error record citing a Chief Reader report | A change to the QA rule |

### CED edition

| Claim | Tag | Source ids or pages | Where it is used | What would change it |
|---|---|---|---|---|
| The registry records the CED cover year and the clarifications year as separate fields | verified | data/curriculum.json `ced_edition`; ced p.i (PDF p.2) | [../curriculum/curriculum-map.md](../curriculum/curriculum-map.md) | A new CED edition with its own cover year |
| The cached CED cover says Effective Fall 2020 while its body already carries the Fall 2026 clarified wording and the revised multiple-choice counts | verified | ced p.i; ced p.198; ced-clarifications-2026 p.1 | [unresolved-questions.md](unresolved-questions.md); [../exam/historical-changes.md](../exam/historical-changes.md) | College Board reissuing the CED with a matching cover |
| Two essential knowledge statements were reworded for Fall 2026, in Unit 5 and Unit 7 | verified | ced-clarifications-2026 p.1 | [../exam/historical-changes.md](../exam/historical-changes.md); BC-EK-FUN-1C1; BC-EK-FUN-7B2 | A further clarifications document |
| The pre-2026 wording of those two statements is not recoverable from the cache, so `previous_text` is empty on both records | verified | [unresolved-questions.md](unresolved-questions.md) | BC-EK-FUN-1C1; BC-EK-FUN-7B2 | Recovery of an earlier CED printing |
| The College Board key-changes page returned HTTP 403 on 2026-09-19 and its content was not obtained | uncertain | BC-SRC-web-key-changes | [../exam/historical-changes.md](../exam/historical-changes.md); [unresolved-questions.md](unresolved-questions.md) | A successful fetch of that page |

### Curriculum counts

| Claim | Tag | Source ids or pages | Where it is used | What would change it |
|---|---|---|---|---|
| The framework holds ten units, all carrying unit records | verified | data/curriculum.json `units`; ced p.199 | [../curriculum/curriculum-map.md](../curriculum/curriculum-map.md) | A CED that adds or merges units |
| The framework holds 111 topic records | verified | data/curriculum.json `topics` | [../curriculum/curriculum-map.md](../curriculum/curriculum-map.md); archetype mapping | A CED that adds or removes topics |
| The framework holds 81 learning objective records and 190 essential knowledge records | verified | data/curriculum.json `learning_objectives`, `essential_knowledge` | [../curriculum/curriculum-map.md](../curriculum/curriculum-map.md); unit files | A CED revision to the framework statements |
| Two essential knowledge records carry single-source rather than verified, reflecting the clarifications document as their only text | single-source | data/curriculum.json; ced-clarifications-2026 p.1 | BC-EK-FUN-1C1; BC-EK-FUN-7B2 | A CED printing that carries the new wording |
| The framework holds four practices and 23 practice skill records | verified | data/curriculum.json `practices`, `practice_skills`; ced p.12 | [../exam/mathematical-practices.md](../exam/mathematical-practices.md) | A CED revision to the skills table |
| The skills registry holds 541 atomic skill records and 170 concept records | verified | data/skills.json | [../curriculum/skill-taxonomy.md](../curriculum/skill-taxonomy.md) | A re-decomposition pass over the units |
| The skills registry holds 77 non-calculus prerequisite records, all tagged inferred | inferred | data/skills.json `prerequisites` | [../curriculum/prerequisite-map.md](../curriculum/prerequisite-map.md); [../misconceptions/prerequisite-failures.md](../misconceptions/prerequisite-failures.md) | A source that publishes prerequisite content |
| Sample multiple-choice questions carry one skill code and one learning objective each, while free-response scoring points may carry more than one | verified | ced p.216 (PDF p.221); ced p.218 (PDF p.223) | [../exam/exam-construction.md](../exam/exam-construction.md); mcq records | A CED that publishes multi-skill MCQ tagging |

### Point taxonomy conventions

| Claim | Tag | Source ids or pages | Where it is used | What would change it |
|---|---|---|---|---|
| The taxonomy holds 69 point-type records, 61 verified and 8 single-source | verified | data/scoring_points.json; `tools/tag_stats.py` | [../scoring/point-taxonomy.md](../scoring/point-taxonomy.md) | A new guideline year adding families |
| A point-type family tagged single-source has one rubric instance, or one document, in the corpus read | single-source | sg-24:16; sg-26:10 | BC-PT-99009; BC-PT-99066 | A second instance in a later guideline |
| Limits of integration are never a point of their own; they are assessed inside the integral point or the answer point | verified | sg-25:7; sg-26:19; sg-22:18 | BC-PT-99001; BC-PT-99002 | A rubric that scores limits separately |
| A constant of integration is not a point of its own and becomes scoreable only when bundled with an initial condition | verified | sg-25:14; sg-26:13 | BC-PT-99003; BC-PT-99031 | A rubric that scores the constant alone |
| From sg-25 onward points are numbered across a whole question, while sg-19 through sg-24 number points inside a part | verified | sg-25:2; sg-24:2; sg-23:2 | Rubric instance citations on every point type | A later guideline reverting the numbering |
| A point type is scoped BC_only when the question carrying it sits under a BC-only header, even where the content itself is shared | verified | sg-26:12 | BC-PT-99028 and siblings | A shared question that carries the same point |

### Chief Reader recurring errors

| Claim | Tag | Source ids or pages | Where it is used | What would change it |
|---|---|---|---|---|
| The errors registry holds 424 error records across the four cached Chief Reader reports and the rubrics | verified | data/errors.json; `tools/tag_stats.py` | [../scoring/chief-reader-findings.md](../scoring/chief-reader-findings.md) | A new Chief Reader report |
| BC-ERR-99001, a vague referent in a justification, is documented in 2022, 2023, 2024 and 2025 | verified | cr-22:12; cr-23:17; cr-24:15; crabbc-25:18 | [../misconceptions/error-to-concept-map.md](../misconceptions/error-to-concept-map.md) | A year with no such finding |
| BC-ERR-99002, equating a variable expression with a numerical value, is documented in all four years | verified | cr-22:25; cr-23:20; cr-24:15; crabbc-25:27 | [../scoring/common-point-losses.md](../scoring/common-point-losses.md) | A year with no such finding |
| BC-ERR-99003, deciding speed from the sign of acceleration alone, is documented in all four years | verified | cr-22:21; cr-23:6; cr-24:6; crabbc-25:21 | [../misconceptions/diagnostic-signals.md](../misconceptions/diagnostic-signals.md) | A year with no such finding |
| BC-ERR-99004, a local argument where a global argument is required, is documented in 2022, 2023 and 2025 | verified | cr-22:12; cr-23:15; crabbc-25:18 | [../scoring/justification-requirements.md](../scoring/justification-requirements.md) | A 2024 or later instance changing the year list |
| BC-ERR-99008, using a theorem's conclusion without verifying its hypotheses, is documented in 2022, 2023 and 2025 | verified | cr-22:13; cr-23:2; crabbc-25:11 | BC-PT-99015; BC-PT-99016 | A 2024 instance changing the year list |
| An error record describes an observed behaviour and a misconception record a possible internal cause; they are separate records linked many to many | inferred | [../README.md](../README.md); [../misconceptions/misconception-taxonomy.md](../misconceptions/misconception-taxonomy.md) | Every diagnostic signal record | A merge of the two registries |

### Prerequisite graph properties

| Claim | Tag | Source ids or pages | Where it is used | What would change it |
|---|---|---|---|---|
| The graph holds 945 edges over 541 skill nodes, 77 prerequisite nodes and 25 topic placeholder nodes | inferred | data/prereq_edges.csv; `tools/graph_check.py` | [../curriculum/concept-dependency-graph.md](../curriculum/concept-dependency-graph.md) | New edges, or remapping the placeholders |
| 376 edges are typed hard_prerequisite and 569 supporting | inferred | data/prereq_edges.csv | [../curriculum/prerequisite-map.md](../curriculum/prerequisite-map.md) | A retyping pass over the edges |
| The hard_prerequisite subgraph is acyclic, with `tools/graph_check.py` reporting 0 cycles | inferred | `tools/graph_check.py` | Any traversal or ordering built on the graph | An added edge that closes a cycle |
| Three unit pairs are mutually dependent at unit level while no skill lies on a cycle | inferred | data/prereq_edges.csv | [../curriculum/concept-dependency-graph.md](../curriculum/concept-dependency-graph.md) | A unit-level acyclicity requirement |
| Units 9 and 10 feed no other unit, which is their terminal position in the CED ordering | inferred | data/prereq_edges.csv | [../curriculum/concept-dependency-graph.md](../curriculum/concept-dependency-graph.md) | An edge from either unit into another |
| 912 of the 945 edges are tagged inferred and 33 verified, so the graph is a research artefact rather than a published structure | inferred | `tools/tag_stats.py` | [../curriculum/prerequisite-map.md](../curriculum/prerequisite-map.md) | College Board publishing a prerequisite structure |

### Consolidation decisions

| Claim | Tag | Source ids or pages | Where it is used | What would change it |
|---|---|---|---|---|
| 129 archetypes are active and 5 were retired into a canonical record after cross-unit consolidation | verified | data/archetypes.json; data/ids.json | [../question-analysis/question-archetypes.md](../question-analysis/question-archetypes.md) | A further consolidation pass |
| A retired record keeps its text and carries `status: retired` with `superseded_by`; nothing is deleted | inferred | data/ids.json; [../README.md](../README.md) | [../misconceptions/misconception-taxonomy.md](../misconceptions/misconception-taxonomy.md) | A decision to delete retired records |
| Misconception records retired in the consolidation are listed separately and not repeated in the unit tables | inferred | data/misconceptions.json | [../misconceptions/misconception-taxonomy.md](../misconceptions/misconception-taxonomy.md) | A restoration of the retired records |
| IDs are append-only and minted through `tools/mint_id.py`, with agents writing to `data/staging/` rather than to the registries | inferred | [../README.md](../README.md) | The whole ID scheme | A change to the merge workflow |

## Claims that are inference from historical exams [inferred]

The claims above rest on published documents. A second class of claim rests on counting what past forms did, which is a different kind of evidence and is kept apart here.

Anything of the form "this structure has appeared in the corpus n times out of m" is an observation about the forms this project cached, not a statement by College Board about any administration. The corpus is uneven: 2023 to 2025 are complete, 2018 to 2022 are archive recoveries, and 2012 to 2017 are largely absent, so a count over the corpus is not a count over the exam's history. The library confines every frequency table to `research/question-analysis/historical-frequency.md`, which is the only file permitted to hold them and which is not yet written; until it exists, no frequency table appears anywhere in the library, and the counts implied by the archetype and FRQ records should be read through that file when it lands.

Claims in this class, and the form they take:

- The recurring shape of the free-response section, meaning which question positions have carried calculator status and which have carried BC-only headers, is read from sg-25 and sg-26 and is stated as an observation about those documents (sg-25:2, sg-25:6, sg-25:20, sg-26:6).
- Archetype records tagged inferred describe a reasoning structure abstracted from official questions. The abstraction is the inference; the questions behind it are cited per record.
- Variant records are overwhelmingly inferred, 312 of 394, because a variant dimension is a research construct laid over the observed questions rather than something a document names.
- Prerequisite edges are inferred from the CED's content ordering and from what the rubrics require, not from a published prerequisite structure.
- Per-question difficulty read from the published means is an observation about three administrations and is stated with its year attached, never as a property of a question type.

No claim in this class is written in predictive form, and `qa/08_prediction.py` fails the build on the predictive phrasings it knows.

## Contradictions between sources and how each was resolved [verified]

Five conflicts were found between cached sources. Each is recorded with the resolution and the rule the resolution follows.

**The linkage rule, sg-23 against sg-25.** sg-22:3 and sg-23:4 each give one of two points to a response that writes an integral equal to a divided value with incomplete communication, and sg-23:16 withholds the answer point for a comparable shape. sg-25:3 states the opposite, that incorrect or unclear communication between the correct integral and the correct answer is treated as scratch work and is not considered in scoring, and gives worked examples that earn both points. sg-26:9 repeats the sg-25 wording. Resolution: both readings stand for their own years, and the change is recorded as a genuine change in treatment between sg-23 and sg-25 rather than a difference in question type. Point-type records carry the sg-25 and sg-26 rule for current behaviour and cite the earlier documents for the earlier behaviour. Whether this is a policy change or question-specific is logged in [unresolved-questions.md](unresolved-questions.md).

**Course at a Glance against the CED exam overview.** The Course at a Glance PDF distributed from the course page prints weightings that no longer match the CED exam information pages. Resolution: the CED pages win and the Course at a Glance is excluded from this library as a source. The discrepancy is recorded in [../exam/historical-changes.md](../exam/historical-changes.md) so the stale figures are not mistaken for a finding.

**CED cover year against CED body content.** The cached CED cover reads Effective Fall 2020, while the body carries the Fall 2026 clarified wording of two essential knowledge statements and the revised multiple-choice figures. Resolution: the body is treated as current and the cover as stale, because the clarifications document independently states both changes. The registry keeps the two facts apart in `ced_edition`, with `cover_year` 2020 and `clarifications_year` 2026, so neither is asserted over the other.

**Unit 2 name discrepancy.** The unit file recorded a difference between the name in `data/curriculum.json` and the running head on the CED unit pages. Resolution: the unit is named Differentiation: Definition and Fundamental Properties, following the curriculum record, and that name now stands in the registry, the curriculum map, the blueprint, the skill taxonomy and the dependency graph. The note in [../units/unit-02-differentiation-definition-properties.md](../units/unit-02-differentiation-definition-properties.md) now records the two readings as identical, so the discrepancy is closed rather than open.

**The sg-25 page 15 header.** sg-25:15 opens Question 4 under the header Part A (AB or BC) while the same line states that a graphing calculator is not allowed, and sg-25:11 opens Question 3 under Part B (AB or BC) with the same calculator statement. Question 4 sits in the no-calculator part, so the Part A label on page 15 is a typo in the published document. Resolution: the calculator statement and the question number govern, and the part label on that page is disregarded. Records derived from sg-25:15 onward carry the no-calculator part, consistent with [../exam/exam-structure.md](../exam/exam-structure.md) and with sg-25:2.

## Pointers to unresolved questions [uncertain]

Everything this register could not settle is logged in [unresolved-questions.md](unresolved-questions.md), grouped there by corpus availability, extraction quality, CED edition, scoring process, and exam logistics. The rows above tagged `uncertain` each have a counterpart entry in that file, and the file is the place an agent appends to rather than guessing.

Four entries carry the most weight for a downstream system. The scoring process entries mean no composite or cut-score claim can be made at all. The CED edition entries mean the pre-2026 wording of two essential knowledge statements is unrecoverable from this cache. The extraction quality entries mean sg-24 contributes structure but not rubric wording, and that the handwritten sample pages contribute nothing until an OCR pass exists. The corpus availability entries mean any count over years is a count over an uneven corpus.
