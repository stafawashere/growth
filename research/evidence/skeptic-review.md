---
title: Skeptic Review of the AP Calculus BC Research Library
research_date: 2026-09-19
status: draft
purpose: Adversarial audit of the registries and Markdown views for fabrication, over-claiming, broken diagnostics, and coverage gaps, with a ranked fix list.
---

# Skeptic Review of the AP Calculus BC Research Library

This file records an independent check of the library against the cached documents. It fixes nothing. Sampling is deterministic: `../../tools/audit_sample.py`, seed 2027.

## Method [verified]

`tools/audit_sample.py` draws the sample with `random.Random(2027)` over ID-sorted pools, so the same records are drawn on any rerun. FRQ records are drawn round robin across years so every administration in the corpus is represented. Each sampled record was checked against the page named in its own `doc_id` and `doc_page`, and against its `sg_doc_id` and `sg_page` where one exists. Judgements are match, partial, or mismatch. Partial means the claim is supported but is either broader than the cited page, or rests on an inference the record does not label as one.

Two mechanical checks were run over the whole tree rather than over the sample. First, every page cited inside prose (`earns`, `does_not_earn`, `scoring_behaviors`, `discriminating_probe`, and similar fields) was resolved against `cache/text/`. Second, every quoted span longer than 25 words in `research/` and in the registries was tested for a twelve word verbatim window inside the cache.

## Part 1: fabrication audit [verified]

No invented citation was found. Every page cited anywhere in the registries, including the pages named inside prose fields, resolves to a file under `cache/text/`. Zero citations point at a page the corpus does not hold. That is the strongest single result of this audit.

| Group | Sampled | Match | Partial | Mismatch |
|---|---|---|---|---|
| FRQ records | 25 | 19 | 5 | 1 |
| Skills, CED page against topic and LO mapping | 15 | 13 | 2 | 0 |
| Scoring point types, three rubric instances each | 10 | 7 | 3 | 0 |
| Chief Reader errors, the 99 synthesis block | 10 | 9 | 0 | 1 |
| MCQ correct_option against the key page | 10 | 8 | 2 | 0 |
| Total | 70 | 58 | 10 | 2 |

### FRQ records [verified]

| ID | Verdict | Reason |
|---|---|---|
| BC-FRQ-2012-Q6-A | match | Five behaviours reproduce the five point labels on samples-12-q6:1 in order. |
| BC-FRQ-2012-Q6-B | match | Two point labels and the third-term error bound match the page. |
| BC-FRQ-2012-Q6-C | match | Point split for three terms and general term matches. |
| BC-FRQ-2013-Q3-B | match | Average rate point and MVT conclusion point match samples-13-q3:1. |
| BC-FRQ-2013-Q4-D | match | Two points for the composite derivative plus one for the value matches. |
| BC-FRQ-2014-Q1-C | partial | Content matches, but `calculator` is `calculator` while the cited page carries no calculator statement; the status is inferred from the three-decimal answer and is tagged `verified`. |
| BC-FRQ-2014-Q3-C | match | Quotient rule two points plus value matches; the `point_type_gap` note is honest. |
| BC-FRQ-2015-Q1-A | partial | Integrand and answer points match; calculator status again not stated on the cited page. |
| BC-FRQ-2015-Q6-C | match | One point for the exponential series and two for the polynomial matches. |
| BC-FRQ-2018-Q6-A | partial | Description matches frq-18:7, but `points` is 0, `scoring_behaviors` is empty, and `sg_doc_id` is null because no 2018 scoring guideline is in the corpus. |
| BC-FRQ-2018-Q6-B | partial | Same placeholder condition. |
| BC-FRQ-2019-Q1-C | partial | Points two to four match sg-19:2 and samples-19-q1:10, but the first entry of `scoring_behaviors` is a note about the rubric numbering convention, not a behaviour. |
| BC-FRQ-2019-Q3-C | match | Three points match sg-19:4 despite the same numbering note. |
| BC-FRQ-2021-Q4-A | match | Single point with reason matches sg-21:15, and the ninth-point note about the global FTC point is correct. |
| BC-FRQ-2021-Q4-C | match | Both points and the linkage-error rule match sg-21:16 exactly. |
| BC-FRQ-2022-Q3-B | match | Both points, the one-of-two special case, and the rejected reasoning list match sg-22:11. |
| BC-FRQ-2022-Q6-B | match | Second-term rule, degree-five exclusion, and the equality refusal match sg-22:21. |
| BC-FRQ-2023-Q1-C | match | Average value formula point and answer point match sg-23:3. |
| BC-FRQ-2023-Q2-B | match | Speed equation point, first-solution point, and parenthesis special case match sg-23:6. |
| BC-FRQ-2024-Q3-A | match | Single solution-curve point matches sg-24:9; the note that the text layer drops the scoring prose is accurate. |
| BC-FRQ-2024-Q4-B | match | FTC point and answer-with-reason point match sg-24:13. |
| BC-FRQ-2025-Q2-B | match | P2, P3, and the statement that limits and the one-half factor are assessed in P4 match sg-25:7 word for word in substance. |
| BC-FRQ-2025-Q6-B | match | P6 and P7 match sg-25:26. |
| BC-FRQ-2026-Q3-A | match | All three behaviours match the Part A notes on sg-26:11. |
| BC-FRQ-2026-Q3-D | mismatch | The special case is described as separating "with the shifted quantity in the wrong position". sg-26:13 describes a sign error, a separation of the form A dH over H plus 20, not a repositioning. The eligibility consequence quoted is correct; the description of the trigger is not. |

Two patterns cut across the group. 66 of 249 FRQ records carry the same sentence about how that year numbers its rubric points as the first element of `scoring_behaviors`; it belongs in `notes`. And 22 records, all of 2018, carry `points` 0 with empty `point_types` and `scoring_behaviors`, so the corpus total of 548 rubric points understates the real total by one whole administration. The records say so in `notes` and are tagged `single-source`, which is honest, but any aggregate computed over the `points` field is silently wrong.

### Skills [verified]

| ID | Verdict | Reason |
|---|---|---|
| BC-SKL-01014 | match | ced:40 carries LIM-1.C.3 on scale hiding behaviour, under topic 1.3. |
| BC-SKL-02011 | match | ced:61 carries CHA-2.B.4 on multiple representations. |
| BC-SKL-02014 | match | ced:62 carries CHA-2.D.1; sg-25:11 and sg-24:2 show the table difference quotient scored. |
| BC-SKL-02043 | match | ced:69 carries FUN-3.B.3 on rewriting with identities. |
| BC-SKL-04036 | partial | `sources` is `sg-23:14` only. That page shows L'Hospital scored, but no CED page is cited, so the mapping to BC-LO-LIM-4A and BC-EK-LIM-4A2 has no cited support while the record is tagged `verified`. |
| BC-SKL-04037 | match | ced:93 carries LIM-4.A.2. |
| BC-SKL-05002 | match | ced:99 carries FUN-1.B.1; sg-23:3 shows the continuity-from-differentiability requirement scored. |
| BC-SKL-06035 | match | ced:124 carries FUN-6.B.2 and FUN-6.B.3. |
| BC-SKL-06047 | match | ced:126 carries FUN-6.D.1. |
| BC-SKL-07008 | match | ced:138 carries FUN-7.B.1. |
| BC-SKL-07027 | match | ced:142 carries FUN-7.D.2; sg-23:12 shows the solve-for-M point. |
| BC-SKL-07034 | partial | ced:144 supports FUN-7.F.2 exactly, but the record also maps to BC-LO-FUN-7G, which is about determining solutions in context, not about writing the model. The second LO is over-mapping. |
| BC-SKL-08043 | match | ced:160 carries CHA-5.C.1. |
| BC-SKL-08050 | match | ced:162 carries CHA-5.C.3. |
| BC-SKL-10008 | match | ced:187 carries LIM-7.A.4 with the BC-only marker, consistent with `scope`. |
| All 15, as a group | note, not a verdict | Every one is tagged `verified`. A CED page verifies that the essential knowledge exists; it does not verify that this particular atomic decomposition is the right one. The tag is doing two jobs. |

CED coverage itself is complete. Scraping every essential knowledge and learning objective code from ced:34 through ced:200 yields 189 essential knowledge codes and 81 learning objective codes, and `curriculum.json` holds 190 and 81. Nothing in the framework is missing.

### Scoring point types [verified]

| ID | Verdict | Reason |
|---|---|---|
| BC-PT-99002 | partial | sg-25:7 P3 matches. `does_not_earn` adds "an integrand presented with no integral sign", which sg-25:7 implies by saying the point is earned for a definite integral, but never states. Inference presented as verified. |
| BC-PT-99011 | match | Candidates test instances resolve to sg-25:5, sg-25:19, sg-23:15. |
| BC-PT-99012 | match | sg-26:8 states in terms that a Candidates Test is not sufficient justification for that point; sg-24:10 and sg-23:13 support the classification framing. |
| BC-PT-99014 | match | sg-24:8 and sg-26:11 both label a point for considering the sign of a derivative. |
| BC-PT-99041 | match | sg-25:22, sg-26:22, and sg-23:20 all withhold the point for an equality claim. |
| BC-PT-99042 | partial | The rubric instances resolve, but `earns` cites sg-22:21 inline while `sources` lists sg-22:20 and not sg-22:21, so the cited evidence is not in the record's own source list. |
| BC-PT-99052 | match | sg-23:5 and sg-22:7 award one point per acceleration component. |
| BC-PT-99058 | match | sg-26:19 and sg-22:18 support the volume integrand form and the pi rule. |
| BC-PT-99060 | partial | `does_not_earn` says any extra declared value inside the open interval forfeits both points. sg-26:15 carves an explicit exception for a response that also declares the interval endpoints, and sg-25:17 excludes consideration of the endpoints from scoring. The rule as written is broader than either page. |
| BC-PT-99064 | match | sg-25:18 states unlabeled values earn neither point. |

### Chief Reader errors [verified]

| ID | Verdict | Reason |
|---|---|---|
| BC-ERR-99001 | match | cr-22:11 records a vague shift-of-graph argument in part (c). |
| BC-ERR-99006 | match | cr-22:2 records responses failing to include the differential dt. |
| BC-ERR-99007 | match | cr-22:21 records responses treating infinity as a number. |
| BC-ERR-99012 | match | cr-22:11 records the wrong-direction f(0) as the most common error. |
| BC-ERR-99013 | match | cr-22:14 records the missing product rule and the r equals 2h assumption. |
| BC-ERR-99021 | match | cr-22:8 states the setup must accompany the answer in a calculator-active part. |
| BC-ERR-99026 | match | cr-24:32 records the wrong initial value, the wrong derivative value, and the third Euler step. |
| BC-ERR-99030 | mismatch | The instance summary says responses concluded the temperature was changing at an increasing rate. cr-24:4 says responses concluded it was changing at a decreasing rate, and the increasing-rate statement is the model correct answer. The record inverts the reported error into the right answer. |
| BC-ERR-99032 | match | cr-22:3 records the malformed integral forms and the reversed and wrong limits. |
| BC-ERR-99036 | match | cr-22:21 records the power rule applied to the exponential position function. |

Every one of the 424 error records has `description` unset. The content lives in `observed_behavior`, which is fine, but the field is dead weight in the schema and invites a reader to think a description is missing.

### MCQ records [verified]

All ten sampled `correct_option` values match the key page. Two records outside the sample fail, and are recorded below because the sample exposed the defect in the page they share.

| ID | Key page | Key letter | Record | Verdict |
|---|---|---|---|---|
| BC-MCQ-CED-002 | ced:221 | B | B | match |
| BC-MCQ-CED-011 | ced:221 | C | C | match |
| BC-MCQ-CED-014 | ced:221 | D | D | match |
| BC-MCQ-PE2012-002 | practice-exam-2012:72 | A | A | match |
| BC-MCQ-PE2012-020 | practice-exam-2012:72 | C | C | match |
| BC-MCQ-PE2012-023 | practice-exam-2012:72 | A | A | match |
| BC-MCQ-PE2012-030 (number 77) | practice-exam-2012:72 | B | B | match |
| BC-MCQ-PE2012-038 (number 85) | practice-exam-2012:72 | B | B | match |
| BC-MCQ-SAMPLE-014 | sample-questions:26 | C | C | match |
| BC-MCQ-SAMPLE-017 (number 1, BC set) | sample-questions:42 | C | C | match |

On ced:221 the answer letter for question 4 is absent from both the `.txt` and the `.raw.txt` layer, and a stray `B` sits inside the row for question 6. BC-MCQ-CED-004 records `B` and BC-MCQ-CED-006 records `C`, both tagged `verified` with no note. The reading is the most plausible reconstruction of a reflowed table, but it is a reconstruction, and neither record says so. Calculator status for the CED questions is properly supported: ced:208 states calculators are not permitted and ced:212 states one is required, and the sampled records agree with the part they sit in.

## Part 2: diagnostic sanity [verified]

### Errors and their causes [verified]

Structurally the requirement holds: every one of the 424 errors has at least two possible causes, because every error carries at least one entry in `non_conceptual_causes`. The conceptual side is thin. 376 errors carry exactly one entry in `possible_misconceptions` and 16 carry none, so only 48 errors present competing conceptual hypotheses at all.

| ID | Misconceptions | Non-conceptual causes | Rivals present | Verdict |
|---|---|---|---|---|
| BC-ERR-01007 | 1 | 1 | no, only through BC-MIS-01005 rivals | thin |
| BC-ERR-02008 | 1 | 2 | no | thin |
| BC-ERR-02023 | 1 | 1 | no | thin |
| BC-ERR-05047 | 1 | 3, boilerplate | no | thin |
| BC-ERR-06027 | 1 | 2 | no | thin |
| BC-ERR-07025 | 1 | 3, boilerplate | no | thin |
| BC-ERR-09034 | 1 | 1 | no | thin |
| BC-ERR-99020 | 2 | 5, specific | yes, the two are declared rivals of each other | adequate |

Where two or more misconceptions are listed, they do rival each other: across all 48 such errors, none fails that test. The problem is the other 376. A diagnostic engine reading one of those records sees a single conceptual explanation and a generic fallback, which is not enough to discriminate.

`non_conceptual_causes` is partly boilerplate. The exact triple "arithmetic slip, misread of the question or the figure, time pressure" appears on 105 of 424 errors, and "arithmetic slip, time pressure" on a further 22. 223 distinct lists cover 424 records.

### Misconception probes [verified]

All eight sampled probes name a concrete task and a discriminating outcome. This is the strongest part of the library.

| ID | Probe specific enough to act on | Note |
|---|---|---|
| BC-MIS-01004 | yes | Asks about behaviour between adjacent table rows. |
| BC-MIS-02002 | yes | Asks where the increment leaves the denominator and why. |
| BC-MIS-02009 | yes | Asks for a squared term from the definition, compared with the rule. |
| BC-MIS-05018 | yes | Asks how the candidate compares with the far endpoint. |
| BC-MIS-06006 | yes | Asks for a sketch of a decreasing concave up curve. |
| BC-MIS-06021 | yes | Names both integrands to compare. |
| BC-MIS-08017 | yes | Names the two radii to substitute. |
| BC-MIS-10009 | yes | Names both exponents to test. |

Three of 236 misconceptions have no rival listed. One naming collision is worth resolving: BC-MIS-06006 and BC-MIS-05020 carry the identical name "Concavity and monotonicity are the same property" in two different unit blocks.

### Adaptive blocks [verified]

This is the weakest area found. Ten of ten sampled skills carry generic text, and the pattern is measurable rather than impressionistic. Replacing every `BC-` identifier with a placeholder and counting distinct sentence skeletons across all 541 skills gives:

| Field | Distinct skeletons | Skills | Largest single skeleton |
|---|---|---|---|
| mastered_if | 19 | 541 | 139 |
| partially_mastered_if | 14 | 541 | 139 |
| prerequisite_gap_if | 6 | 541 | 273 |

Every sampled `mastered_if` reduces to "produces a correct and completely communicated response to <archetype> across at least two representations, with no error from <error ids>". Nothing in it is specific to the skill. There is no mention of the three-decimal reporting rule for the calculator skills, no mention of endpoint testing for BC-SKL-10008, no mention of the differential for the integral-setup skills, even though the scoring point types record exactly those requirements. 28 skills go further and say "no error from the errors recorded for this topic" with no identifiers at all, and 60 say "consistent with the prerequisites recorded for this skill" in `prerequisite_gap_if`, which names nothing.

`remediation_target` is similarly defaulted. BC-PRQ-06005, "Reading function notation, composition, and evaluation", is the remediation target for 87 skills, including 40 or more Unit 1 skills whose own `prerequisite_gap_if` cites it. 134 skills point at a remediation target in a different unit block.

## Part 3: completion test [verified]

Thirteen answerable, eleven partially answerable, one not answerable.

| # | Question | Files and fields | Rating | Why |
|---|---|---|---|---|
| 1 | What BC requires students to know | `data/curriculum.json`: `units`, `topics`, `learning_objectives.text`, `essential_knowledge.text`; `research/units/unit-01` through `unit-10` | answerable | 81 learning objectives and 190 essential knowledge statements, matching every code scraped from ced:34 to ced:200. |
| 2 | Prerequisites of every skill | `data/skills.json`: `prerequisites`, `prerequisites` registry; `data/prereq_edges.csv` | answerable | 945 typed edges; only 10 of 541 skills have an empty list. |
| 3 | Which concepts are independently assessable | `data/skills.json`: `concepts`; `data/archetypes.json`: `skills`, `primary_unit` | partially | 170 concepts exist and archetypes attach to them, but no field states independent assessability; it has to be reconstructed from single-skill archetypes. |
| 4 | How each concept is tested | `data/archetypes.json`: `description`, `typical_wording`, `multipart_structure`; `data/frq_records.json`; `data/mcq_records.json` | answerable | 134 archetypes and 340 official question records carry the mapping. |
| 5 | Which archetypes recur | `research/question-analysis/historical-frequency.md`; `data/archetypes.json`: `official_examples` | answerable | Counts with denominators live in the one file allowed to hold them. |
| 6 | How each archetype varies | `data/archetypes.json`: `difficulty_variables`, `safe_variables`, `variants` | answerable | 394 variants across 134 archetypes. |
| 7 | Which concepts appear together | `data/frq_records.json`: `concepts_combined`, `secondary_units`; `research/question-analysis/frq-analysis.md` | answerable | Co-occurrence is recorded per part and summarised per unit pair. |
| 8 | Which skills require a calculator | `data/skills.json`: `calculator_relevance`; `research/exam/calculator-policy.md` | answerable | 38 typically required, 71 optional, 432 none. |
| 9 | Which representations occur | `data/taxonomies.json`: `representations`; `representations` on skills, archetypes, and question records | answerable | 14 representation types, and no skill has an empty list. |
| 10 | What each FRQ point rewards | `data/scoring_points.json`: `earns`, `does_not_earn`; `data/frq_records.json`: `scoring_behaviors`, `point_types` | partially | 69 point types are well evidenced, but 22 2018 records carry no point data at all and 66 records open `scoring_behaviors` with a numbering note. |
| 11 | What wording or justification earns points | `data/scoring_points.json`: `justification_required`, `notation_requirements`; `research/scoring/justification-requirements.md` | answerable | The rubric prose is paraphrased per point type with the pages named. |
| 12 | Which mistakes repeatedly cost points | `data/errors.json`: `instances`, `scoring_consequence`; `research/scoring/common-point-losses.md` | answerable | Errors carry dated instances with document and page. |
| 13 | Which misconception produces a wrong answer | `data/diagnostic_signals.json`: `observation`, `consistent_with`, `distinguish_by` | partially | 239 signals, but 236 of 541 skills have none attached, so coverage is roughly half. |
| 14 | Alternative misconceptions for the same error | `data/errors.json`: `possible_misconceptions`; `data/misconceptions.json`: `rival_misconceptions` | partially | Only 48 of 424 errors list two or more; the rest need a second hop through the rival graph. |
| 15 | Which question type isolates one skill | `data/skills.json`: `adaptive.diagnostic_archetypes`; `data/archetypes.json`: `skills` | answerable | Every skill but one names at least one archetype. |
| 16 | Which earlier concepts to check when a later skill fails | `data/prereq_edges.csv`; `data/skills.json`: `adaptive.remediation_target` | partially | The edge graph is good, but the remediation target defaults to BC-PRQ-06005 for 87 skills, so the per-skill answer is often uninformative. |
| 17 | How each concept appeared historically | `data/frq_records.json`: `year`, `question`, `part`; `research/question-analysis/historical-frequency.md` | partially | 2012 to 2026 are present, but 2018 has no rubric data and 2026 has no Chief Reader report in cache. |
| 18 | Which official questions evidence each archetype | `data/archetypes.json`: `official_examples`, `official_examples_notes`; variants `official_examples` | partially | 36 of 134 archetypes and 221 of 394 variants carry no official example. |
| 19 | What makes variants harder or easier | `data/archetypes.json`: `variants.difficulty_effect`, `difficulty_factors`; `data/taxonomies.json`: `difficulty_factors` | answerable | 17 difficulty factors with evidence, and every variant declares its direction. |
| 20 | What an AI needs to generate a matching question | `data/archetypes.json`: `invariant_structure`, `safe_variables`, `typical_wording`, `expected_solution_path`, `scoring_pattern`, `common_distractors` | answerable | The generation contract is the best specified object in the library. |
| 21 | How to distinguish conceptual from arithmetic failure | `data/diagnostic_signals.json`: `distinguish_by`; `data/errors.json`: `non_conceptual_causes` | partially | `distinguish_by` is concrete, but 105 errors share one boilerplate non-conceptual list. |
| 22 | Mastery versus partial mastery per skill | `data/skills.json`: `adaptive.mastered_if`, `adaptive.partially_mastered_if` | not answerable | 541 skills reduce to 19 and 14 distinct sentence skeletons; no skill-specific criterion is stated anywhere. |
| 23 | Which later concepts become inaccessible if a prerequisite is missing | `data/prereq_edges.csv`; `data/skills.json`: `dependents` | partially | The edge file answers it in aggregate, but 350 of 541 skills carry an empty `dependents` list. |
| 24 | Which statements are official fact versus inference | `evidence_tag` on every record; `research/evidence/claims-and-confidence.md` | partially | The mechanism exists and 912 of 945 prerequisite edges are honestly marked inferred, but 538 of 541 skills are tagged `verified`, which drains the tag of meaning for that registry. |
| 25 | What evidence supports each conclusion | `sources` on every record; `research/evidence/source-registry.md` | partially | Sources resolve to real cached pages, but 75 records cite pages in prose that are absent from their own `sources` array. |

## Part 4: language and copyright sweep [verified]

### Overstatement [verified]

109 lines in `research/` match `always`, `never`, `guarantees`, `definitely`, or `certainly`. Most are legitimate. They fall into three classes: quoted CED wording, for example the Intermediate Value Theorem statement in unit-01; misconception names, where the absolute is the point, for example BC-MIS-08023 "The upper curve always gives the outer radius"; and ID-scheme prose about CED codes never being keys. Three lines assert something about the exam that the evidence does not carry.

| File and line | Text | Problem |
|---|---|---|
| question-analysis/mcq-analysis.md:118 | BC-QA-06003 "always supplies the integrand graphically" | A universal claim drawn from a finite indexed sample. It should read as a count with a denominator. |
| question-analysis/frq-analysis.md:42 | "an application of integration is almost always executed as an accumulation" | Hedged but unquantified, in a file that is not permitted to hold frequency claims. |
| scoring/chief-reader-findings.md:56 | "Speed and total distance setups were nearly always correct" | A paraphrase of cr-24:25 that reads as the library's own finding. |

### Study-plan language [verified]

Clean. The only match for study-plan phrasing in `research/` is the disclaimer in README.md stating the library is not a study plan. No schedule, no week, no daily practice instruction appears anywhere.

One adjacent point. 38 error records carry a `teacher_advice` field, and `research/scoring/chief-reader-findings.md` reproduces it in a table column. Every entry is attributed, opening with "The reports advise", so it is a documented fact about the source rather than the library's own instruction. It is still teaching advice in substance and sits at the edge of the no-advice rule.

### Copied stems and long quotes [verified]

217 quoted spans in `research/` and the registries exceed 25 words. 56 of them contain a twelve word window that appears verbatim in the cached text. None is a question stem. All of the confirmed ones are CED essential knowledge statements reproduced in full inside the unit files and inside `curriculum.json`.

| Measure | Count |
|---|---|
| Spans over 25 words tested | 217 |
| Spans with a verbatim twelve word window in cache | 56 |
| `essential_knowledge.text` entries over 25 words | 58 of 190 |
| Longest `essential_knowledge.text` entry | 110 words |

The README states that anchor quotes are at most 25 words and that `qa/07_quotes.py` verifies them. That script reads only the `anchor_quote` field. It never inspects `curriculum.json`, and it never inspects Markdown bodies. So the 25 word cap is stated as a project rule and enforced on one field out of many. Whether reproducing full CED essential knowledge is acceptable is a policy decision, not an audit finding, but the rule as written and the practice as implemented disagree, and the check does not close the gap.

## Recommended fixes [verified]

Ranked by severity. Severity is how badly a downstream consumer would be misled.

| Rank | Severity | Fix | File and records |
|---|---|---|---|
| 1 | critical | Correct the inverted Chief Reader finding. The instance summary says responses concluded an increasing rate; cr-24:4 says decreasing, and increasing is the model answer. | `data/errors.json`, BC-ERR-99030, first instance (cr-24, page 4, Q1 part d) |
| 2 | critical | Replace the boilerplate adaptive blocks with skill-specific criteria, or state plainly that they are templates. As they stand, question 22 of the completion test has no answer. Start with the 28 skills whose `mastered_if` names no error and the 60 whose `prerequisite_gap_if` names no prerequisite. | `data/skills.json`, `adaptive.mastered_if`, `adaptive.partially_mastered_if`, `adaptive.prerequisite_gap_if` across all 541 skills |
| 3 | high | Retag the skills registry. 538 of 541 are `verified`, but a CED page evidences the essential knowledge, not the atomic decomposition. `inferred` is the honest tag for the decomposition. Add a note to BC-MCQ-CED-004 and BC-MCQ-CED-006 recording that the key letter is displaced on ced:221 in both text layers, and downgrade those two to `single-source`. | `data/skills.json` all skills; `data/mcq_records.json`, BC-MCQ-CED-004, BC-MCQ-CED-006 |
| 4 | high | Bring inline citations into `sources`, and extend `qa/03_links.py` to check citations that appear in prose fields rather than only ID references. 17 scoring point types, 51 FRQ records, and 7 misconceptions cite a page in prose that their own `sources` array omits, among them BC-PT-99001, BC-PT-99042, BC-FRQ-2019-Q1-C, and BC-MIS-99005. | `data/scoring_points.json`, `data/frq_records.json`, `data/misconceptions.json`, `qa/03_links.py` |
| 5 | high | Separate rubric metadata from rubric behaviour, and mark the 2018 records as excluded from point totals. 66 records open `scoring_behaviors` with a note about that year's numbering convention, and 22 records carry `points` 0 as a placeholder, so the corpus total of 548 is not a real point count. | `data/frq_records.json`, the 66 records carrying the numbering note and BC-FRQ-2018-Q1-A through BC-FRQ-2018-Q6-C |
| 6 | medium | Extend `qa/07_quotes.py` beyond `anchor_quote` to `curriculum.json` text fields and Markdown bodies, or amend the README so the 25 word cap is stated only for the field it governs. 58 essential knowledge entries exceed the cap, the longest at 110 words. | `qa/07_quotes.py`, `research/README.md`, `data/curriculum.json` |
| 7 | medium | Narrow the three overstated claims to counts with denominators. | `research/question-analysis/mcq-analysis.md:118`, `research/question-analysis/frq-analysis.md:42`, `research/scoring/chief-reader-findings.md:56` |
| 8 | medium | Narrow two scoring point rules to what the pages state. BC-PT-99060 drops the endpoint exception that sg-26:15 spells out, and BC-PT-99002 presents an inference about a missing integral sign as verified. | `data/scoring_points.json`, BC-PT-99060, BC-PT-99002 |
| 9 | medium | Add a second conceptual hypothesis to errors that carry only one, or record that the single misconception is the only one the evidence supports. 376 of 424 errors carry exactly one and 16 carry none. Replace the boilerplate cause triple that 105 errors share. | `data/errors.json`, `possible_misconceptions`, `non_conceptual_causes` |
| 10 | low | Diversify the remediation targets. BC-PRQ-06005 serves 87 skills, which makes the field a default rather than a diagnosis. | `data/skills.json`, `adaptive.remediation_target` |
| 11 | low | Fix the local mismatches found in the sample: the BC-FRQ-2026-Q3-D special case describes a sign error as a repositioning; BC-SKL-04036 cites no CED page for its learning objective mapping; BC-SKL-07034 maps to BC-LO-FUN-7G without support; BC-MIS-06006 and BC-MIS-05020 share a name. | `data/frq_records.json`, `data/skills.json`, `data/misconceptions.json` |
| 12 | low | Drop or populate the unused `description` field on all 424 error records. | `data/errors.json` |
