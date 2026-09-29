---
title: Unit 1 attack map, Limits and Continuity
research_date: 2026-09-29
status: draft
purpose: The map every designer of the 19 BC-UNIT-01 concept lessons reads before designing, giving the concept order along the prerequisite edges, the exam shapes the unit feeds, the cross-concept recognition features, the recurring traps, the time budgets and the delivery mode each concept's blocks take under the TEMPLATE.md selection rules.
---

# Unit 1 attack map, Limits and Continuity

BC-UNIT-01 covers CED pages 38 to 53, sixteen topics BC-TOP-0101 to BC-TOP-0116 (CED 1.1 to 1.16), 19 concepts BC-CON-01001 to BC-CON-01019 and 68 skills BC-SKL-01001 to BC-SKL-01068 (research/units/unit-01-limits-continuity.md#Unit 1, Limits and Continuity; ced:38, ced:53). Every count and list below is computed from the content snapshot (`load_snapshot(DEFAULT_CONTENT_ROOT)`), data/prereq_edges.csv, data/errors.json and data/misconceptions.json on 2026-09-29. The epsilon delta definition of a limit is excluded from assessment and no skill records it (ced:39; research/units/unit-01-limits-continuity.md#Unresolved).

## 1. Concept order along the prerequisite edges

Order: a topological sort of the 19 concepts, where concept A is a parent of concept B when a `hard_prerequisite` edge in data/prereq_edges.csv runs from a skill of A to a skill of B; ties are broken by the smaller id among the concepts whose parents are all placed. Supporting edges between this unit's concepts are listed but do not order. Every BC-PRQ parent reaches this unit through a `supporting` edge; no BC-PRQ edge into Unit 1 is `hard_prerequisite`. No other unit's skill is a parent of a Unit 1 skill (research/units/unit-01-limits-continuity.md#What Unit 1 depends on).

| # | Concept | Name | Skills | Hard parent concepts | Supporting parents |
|---|---|---|---|---|---|
| 1 | BC-CON-01001 | Instantaneous rate of change as a limit of average rates | BC-SKL-01001, 01002, 01003, 01004 | none | BC-PRQ-06005 |
| 2 | BC-CON-01002 | The limit of a function at a point | BC-SKL-01006, 01008 | none | BC-PRQ-06005 |
| 3 | BC-CON-01003 | Limit notation and its reading | BC-SKL-01005, 01007 | none | BC-PRQ-06005 |
| 4 | BC-CON-01006 | Estimation of a limit from a graph or a table | BC-SKL-01009, 01014, 01015, 01017 | none | BC-PRQ-06005 |
| 5 | BC-CON-01004 | One sided limits and two sided existence | BC-SKL-01010, 01016, 01023 | BC-CON-01006 | BC-PRQ-01003, BC-PRQ-06005 |
| 6 | BC-CON-01005 | Ways a limit can fail to exist | BC-SKL-01011, 01012, 01013 | BC-CON-01004 | BC-PRQ-01003, 01005, 01006, 01009 |
| 7 | BC-CON-01007 | Limit theorems for combinations of functions | BC-SKL-01018, 01019, 01020, 01021, 01022 | BC-CON-01006 | BC-PRQ-01008, BC-PRQ-06005 |
| 8 | BC-CON-01008 | Indeterminate form handled by rewriting | BC-SKL-01024, 01025, 01026, 01027, 01028 | none | BC-PRQ-01001, 01002, 01005, 01007 |
| 9 | BC-CON-01009 | Selection of a procedure for a limit | BC-SKL-01029, 01030, 01031 | BC-CON-01007, BC-CON-01008 | BC-PRQ-01001, 01008 |
| 10 | BC-CON-01010 | The squeeze theorem | BC-SKL-01032, 01033, 01034, 01035 | BC-CON-01009 | BC-PRQ-01005, 01010 |
| 11 | BC-CON-01011 | Connecting graphical, numerical, analytical, and verbal limit statements | BC-SKL-01036, 01037, 01038 | BC-CON-01006 | BC-CON-01002; BC-PRQ-01003, BC-PRQ-06005 |
| 12 | BC-CON-01012 | Classification of discontinuities | BC-SKL-01039, 01040, 01041, 01042 | BC-CON-01006, BC-CON-01008 | BC-PRQ-01001, 01003, 01006, 01008, 01009 |
| 13 | BC-CON-01013 | Continuity at a point as three conditions | BC-SKL-01043, 01044, 01045 | BC-CON-01004, BC-CON-01006 | BC-PRQ-01003, BC-PRQ-06005 |
| 14 | BC-CON-01014 | Continuity on an interval | BC-SKL-01046, 01047, 01048, 01049 | BC-CON-01013 | BC-PRQ-01003, 01008, 01010 |
| 15 | BC-CON-01015 | Removing a discontinuity and matching a piecewise function | BC-SKL-01050, 01051, 01052, 01053 | BC-CON-01012, BC-CON-01013 | BC-PRQ-01001, 01003 |
| 16 | BC-CON-01016 | Infinite limits and vertical asymptotes | BC-SKL-01054, 01055, 01056, 01057 | BC-CON-01006, 01007, 01008, 01012 | BC-CON-01012; BC-PRQ-01001, 01009 |
| 17 | BC-CON-01017 | Limits at infinity and horizontal asymptotes | BC-SKL-01058, 01059, 01060, 01061, 01063 | BC-CON-01008, BC-CON-01016 | BC-PRQ-01004, BC-PRQ-06005 |
| 18 | BC-CON-01018 | Relative magnitude of growth compared by limits | BC-SKL-01062 | BC-CON-01008 | BC-PRQ-01004 |
| 19 | BC-CON-01019 | The Intermediate Value Theorem | BC-SKL-01064, 01065, 01066, 01067, 01068 | BC-CON-01013, BC-CON-01014 | BC-PRQ-01008, 01010 |

Skill ids after the first in a cell drop the `BC-SKL-` prefix; the same holds for BC-PRQ and BC-CON lists. Five concepts are roots (BC-CON-01001, 01002, 01003, 01006, 01008). BC-CON-01006 sits fourth although its topic is 1.3 and 1.4, because four concepts hang from it. BC-CON-01008 is a root although its topic is 1.6: no hard edge enters its skills from BC-CON-01007. The deepest chain is BC-CON-01006, 01004, 01013, 01014, 01019.

## 2. Exam question types the unit feeds

Budgets per question come from research/exam/exam-structure.md#Section and part layout: Section I Part A, 29 questions in 62 minutes, no calculator, 2.14 minutes each; Section I Part B, 13 in 38, calculator required, 2.92 each; Section II, 2 questions in 30 minutes (Part A, calculator) and 4 in 60 (Part B, no calculator), 15.0 each, 9 points per question (research/exam/exam-structure.md#Free-response point totals). Shape is MCQ when `multipart_structure` says "a single multiple choice item", FRQ part when it says "one part of a multipart free response question", and both when it names both. Fifteen archetypes load a Unit 1 skill, one per family, all primary in Unit 1.

| Archetype | Family | Shape (`multipart_structure`) | Calculator status | Exam part | Point types | Official examples |
|---|---|---|---|---|---|---|
| BC-QA-01001 | limit-from-graph | MCQ or FRQ part | no_calculator | I-A; II-B | none recorded | BC-MCQ-CED-011 |
| BC-QA-01002 | limit-from-table | MCQ | either | I-A or I-B | none recorded | none |
| BC-QA-01003 | limit-by-theorems | MCQ | no_calculator | I-A; II-B through its FRQ example | BC-PT-99004 | BC-FRQ-2019-Q3-D (1 point, sg-19:4) |
| BC-QA-01004 | limit-algebraic-rewrite | MCQ or FRQ part | no_calculator | I-A; II-B | none recorded | BC-MCQ-CED-001, BC-MCQ-SAMPLE-002 |
| BC-QA-01005 | squeeze-theorem | FRQ part or MCQ | no_calculator | I-A; II-B | none recorded | none |
| BC-QA-01006 | continuity-at-a-point | FRQ part or MCQ | no_calculator | I-A; II-B | none recorded | BC-MCQ-PE2012-036 |
| BC-QA-01007 | discontinuity-classification | MCQ | no_calculator | I-A | none recorded | none |
| BC-QA-01008 | parameter-for-continuity | MCQ or FRQ part | no_calculator | I-A; II-B | none recorded | none |
| BC-QA-01009 | infinite-limit-asymptote | MCQ | no_calculator | I-A | none recorded | none |
| BC-QA-01010 | end-behaviour-limit | FRQ part | either | II-A or II-B; its FRQ example is II-A | BC-PT-99054, BC-PT-99004 | BC-FRQ-2025-Q1-C (2 points, calculator, sg-25:4), BC-MCQ-PE2012-021 |
| BC-QA-01011 | ivt-existence | FRQ part | no_calculator | II-B; one example is II-A | BC-PT-99015, BC-PT-99016 | BC-FRQ-2014-Q4-B, BC-FRQ-2022-Q4-B (sg-22:14), BC-FRQ-2025-Q3-B (sg-25:12), BC-FRQ-2026-Q1-D (calculator, sg-26:5), 2 points each |
| BC-QA-01012 | derivative-definition-limit | FRQ part | either | II-A or II-B | none recorded | none |
| BC-QA-01013 | representation-consistency | MCQ | no_calculator | I-A | none recorded | none |
| BC-QA-01014 | procedure-selection | MCQ | no_calculator | I-A | none recorded | none |
| BC-QA-01015 | continuity-interval | MCQ | no_calculator | I-A | none recorded | none |

Point types, from data/scoring_points.json: BC-PT-99004 earns the correct value on its own with no supporting work required (sg-25:3, sg-26:4). BC-PT-99054 earns the requested limit written symbolically as the variable tends to infinity, for the function or its derivative (sg-25:4), and is not earned by a limit set up with the variable tending to zero or by arithmetic with infinity. BC-PT-99015 earns an explicit statement that the function is continuous because it is differentiable (sg-25:12, sg-26:5, sg-22:14); a bare continuity statement does not earn it. BC-PT-99016 earns the target shown strictly between two function values, a continuity statement and a yes (sg-25:12, sg-26:5); "yes, IVT" alone does not earn it.

Of the 15 archetypes, 12 carry no `point_types`, so under plan 15 (The scoring checklist, `what_a_reader_scores`) their lessons carry no scoring section. The unit's FRQ grounding is thin: continuity and limit work appears inside larger questions rather than as questions of their own, and only BC-QA-01010 and BC-QA-01011 are verified against a rubric (research/units/unit-01-limits-continuity.md#Archetype summary). Unit 1 skills also appear as secondary skills on FRQ parts of other units' archetypes: BC-SKL-01060 on BC-FRQ-2019-Q2-D (BC-QA-09012), BC-SKL-01058 on BC-FRQ-2023-Q5-B and BC-FRQ-2026-Q5-D (BC-QA-06011) (research/units/unit-01-limits-continuity.md#Official evidence index [verified]).

## 3. Cross-concept patterns

### Which concepts the stems combine

Computed by mapping each archetype's `skills` list to the concepts that hold those skills.

| Archetype | Concepts loaded | Combination the stem makes |
|---|---|---|
| BC-QA-01001 | BC-CON-01002, 01004, 01005, 01006 | one graph, several breaks: value against limit, one sided against two sided, the failure mode |
| BC-QA-01006 | BC-CON-01013, 01012, 01004 | piecewise boundary: one sided limits from branches, then the three conditions |
| BC-QA-01007 | BC-CON-01012, 01016 | removable break against vertical asymptote at a zero of the denominator |
| BC-QA-01009 | BC-CON-01016, 01012 | asymptote located after a cancelling factor is removed |
| BC-QA-01010 | BC-CON-01017, 01018 | end behaviour limit and growth comparison |
| BC-QA-01013 | BC-CON-01011, 01003, 01002, 01006 | notation read against a graph, a table and words |
| BC-QA-01014 | BC-CON-01009, 01007 | form under substitution decides between substitution and rewriting |
| BC-QA-01002, 01003, 01004, 01005, 01008, 01011, 01012, 01015 | one concept each (01006, 01007, 01008, 01010, 01015, 01019, 01001, 01014) | single concept archetypes |

Topic sections record further pairings: an average rate with an existence argument in a later part (1.1), graph reading with classification at the same input (1.3, BC-QA-01007), theorems with a piecewise boundary (1.5), an indeterminate quotient at a piecewise boundary or inside a continuity question (1.6), a determinate substitution, an indeterminate quotient and a limit at infinity in one item (1.7), continuity with a parameter in the same part (1.11, BC-QA-01008), interval continuity as the hypothesis for the IVT (1.12, BC-QA-01011), a removable break and an asymptote in one expression (1.14) (research/units/unit-01-limits-continuity.md, the Assessment behaviour subsection of each topic section).

### Recognition features between neighbouring concepts

Each row names the feature of the stem that separates two neighbours, from the archetype `difficulty_variables`, `asked_to_produce` and `expected_solution_path`, and from the topic sections.

| Neighbours | Feature that separates them | Source |
|---|---|---|
| Limit exists (BC-CON-01002, 01004) against continuity (BC-CON-01013) | the stem asks for a limit, which is the approached value; continuity also asks for the function value and a comparison, three conditions | BC-QA-01006 `asked_to_produce`; BC-SKL-01043; research/units/unit-01-limits-continuity.md#1.11 Defining Continuity at a Point |
| One sided (BC-CON-01004) against two sided (BC-CON-01002) | notation carries a superscript sign or the stem names a side; a two sided answer needs both sides read and compared | BC-QA-01001 `expected_solution_path`; BC-SKL-01007 |
| Squeeze (BC-CON-01010) against direct substitution (BC-CON-01007) | a bounded oscillating factor with no limit of its own multiplies a vanishing factor, so the product theorem has no factor limit to use | BC-SKL-01035; BC-QA-01005 `common_givens` |
| Indeterminate form (BC-CON-01008) against a defined value (BC-CON-01007, 01009) | substitution gives zero over zero; a nonzero over zero is not indeterminate and points to BC-CON-01016; a defined value settles the limit (BC-SKL-01031) | BC-QA-01014 `expected_solution_path`; BC-SKL-01028 |
| Removable (BC-CON-01012, 01015) against vertical asymptote (BC-CON-01016) | whether a factor of the denominator cancels | BC-QA-01007 and BC-QA-01009 `difficulty_variables`; BC-SKL-01057 |
| Infinite limit (BC-CON-01016) against limit at infinity (BC-CON-01017) | where the infinity symbol sits: in the value or under the arrow | BC-MIS-01018 discriminating probe |
| Amount against rate at infinity (BC-CON-01017) | which function the stem names for the end behaviour | BC-QA-01010 `difficulty_variables`; BC-MIS-01014; sg-25:4 |
| IVT hypotheses (BC-CON-01019) against continuity on an interval (BC-CON-01014) | an existence question in an open interval with a target value; continuity must be derived (from differentiability in every FRQ example) before the straddle is used | BC-QA-01011 `difficulty_variables`; sg-25:12 |
| Table estimate (BC-CON-01006) against a settled limit | whether the table is deliberately inconclusive or tabulates one side only | BC-QA-01002 `difficulty_variables`; BC-MIS-01004 |

### First written line per method

`expected_solution_path[0]` of each archetype record, which plan 15 (Recognition cues and the first step, the `strategy` section) names as the first written step.

| Archetype | First written line |
|---|---|
| BC-QA-01001 | locate the named input on the horizontal axis |
| BC-QA-01002 | identify the rows approaching from the left |
| BC-QA-01003 | record the supplied limits |
| BC-QA-01004 | substitute and observe the indeterminate form, presenting the numerator and denominator limits separately, since a limit written equal to zero over zero does not earn the form point (sg-23:14) |
| BC-QA-01005 | bound the oscillating factor between fixed values |
| BC-QA-01006 | evaluate the function at the named input |
| BC-QA-01007 | locate the inputs where the function is undefined or the rule changes |
| BC-QA-01008 | evaluate the one sided limit from each branch at the boundary |
| BC-QA-01009 | factor numerator and denominator |
| BC-QA-01010 | identify the function whose end behaviour is requested, then write the limit expression as the variable increases without bound |
| BC-QA-01011 | state that the function is continuous and give the reason |
| BC-QA-01012 | compute the average rate over each interval |
| BC-QA-01013 | read the limit behaviour from the supplied representation |
| BC-QA-01014 | substitute the target input into each expression |
| BC-QA-01015 | identify every input at which the expression is undefined |

## 4. Recurring traps

### Errors across several concepts

BC-ERR records whose `skills` fall in two or more Unit 1 concepts, with the `scoring_consequence` text of the record.

| Error | Concepts | Scoring consequence (record text) | Linked misconceptions |
|---|---|---|---|
| BC-ERR-01001 Function value reported as the limit | 01002, 01006, 01007, 01013 | The reading point is lost, and in a continuity part the comparison of limit with value collapses. | BC-MIS-01001, 01003 |
| BC-ERR-01002 One sided value reported as the two sided limit | 01004, 01005, 01006, 01011 | The value point is lost because the correct response is that the limit does not exist. | BC-MIS-01002, 01001 |
| BC-ERR-01003 Nonexistence claimed because the function is undefined at the point | 01002, 01006, 01009, 01012, 01015 | Both the value point and any justification point are lost. | BC-MIS-01001, 01009 |
| BC-ERR-01004 Oscillation reported as a limit value | 01005, 01006 | The value point is lost because no limit exists. | BC-MIS-01004, 01003 |
| BC-ERR-01006 Quotient limit theorem applied with a zero denominator limit | 01007, 01009 | The value point is lost and any justification naming the theorem is incorrect. | BC-MIS-01005, 01006 |
| BC-ERR-01008 Indeterminate form read as the answer zero | 01008, 01009 | The value point is lost and the rewriting step is absent. | BC-MIS-01006, 01005 |
| BC-ERR-01009 Indeterminate form read as nonexistence | 01008, 01009 | The value point and the rewriting point are lost. | BC-MIS-01006, 01005 |
| BC-ERR-01015 Continuity claimed from matching one sided limits alone | 01012, 01013, 01015 | The justification point is lost, and a parameter solved this way can be wrong when the defined value differs. | BC-MIS-01009, 01001 |
| BC-ERR-01016 Definition restated in place of a reason | 01013, 01019 | The justification point is lost; a scoring guideline requires the reason rather than the assertion (sg-25:12). | BC-MIS-01010, 01009 |
| BC-ERR-01017 Wrong branch evaluated at a boundary | 01004, 01012, 01013, 01015 | The one sided limit is wrong and every point depending on it is lost. | BC-MIS-01009, 01019 |
| BC-ERR-01018 Cancelling factor reported as a vertical asymptote | 01012, 01016 | The location point is lost and the classification is wrong. | BC-MIS-01011, 01012 |
| BC-ERR-01019 Two sided infinite limit written where the sides differ in sign | 01009, 01016 | The behaviour point is lost because the notation asserts behaviour the function does not have. | BC-MIS-01012, 01011 |
| BC-ERR-01020 Infinite limit reported as an existing real limit | 01005, 01009, 01011, 01012, 01016 | A point requiring a statement about existence is lost. | BC-MIS-01012, BC-MIS-99008 |
| BC-ERR-01021 Infinity substituted as a number | 01009, 01011, 01017 | Arithmetic performed with the infinity symbol is treated as scratch work and does not earn the value point (sg-25:4). | BC-MIS-99008, BC-MIS-01018 |
| BC-ERR-01023 End behaviour decided by the leading coefficients without comparing degrees | 01009, 01017 | The value point is lost. | BC-MIS-99008, BC-MIS-01005 |
| BC-ERR-01033 Limit at infinity confused with an infinite limit | 01011, 01017 | The conversion point is lost. | BC-MIS-01018, 01012 |
| BC-ERR-99008 Hypotheses of a theorem not verified before its conclusion is used | 01010, 01019 | The condition point is not earned; in several years this was the point earned by the smallest proportion of responses on the question. | BC-MIS-99009, BC-MIS-01015 |

Most of these consequences name a point on archetypes whose records carry no `point_types`; the consequence is the record's statement and stays in the error block, but a lesson on such an archetype names no point in a scoring section (plan 15, The scoring checklist).

### Misconceptions across several concepts

BC-MIS records whose `skills` or `concepts` fall in two or more Unit 1 concepts, with severity from the record.

| Misconception | Concepts | Severity |
|---|---|---|
| BC-MIS-01001 The limit at a point is the value of the function there | 01002, 01006, 01013 | high |
| BC-MIS-01002 A limit exists whenever the function approaches something on one side | 01004, 01005, 01006 | high |
| BC-MIS-01004 A table settles the behaviour of a function | 01005, 01006 | medium |
| BC-MIS-01006 An indeterminate form is a value | 01008, 01009 | high |
| BC-MIS-01009 Continuity is a single condition | 01013, 01015 | high |
| BC-MIS-01010 Restating a definition counts as a justification | 01010, 01013, 01019 | high |
| BC-MIS-01011 Every input missing from the domain is an asymptote | 01012, 01016 | high |
| BC-MIS-01012 Unbounded behaviour is the same on both sides | 01005, 01016 | high |
| BC-MIS-01014 The end behaviour of a quantity and of its rate are interchangeable | 01017, 01018 | high |
| BC-MIS-01018 All limit notation with an infinity symbol means the same thing | 01003, 01011, 01016, 01017 | medium |

### Point losses research/scoring names for this unit's shapes

- research/scoring/common-point-losses.md#Justification points [verified]: hypotheses of the Mean Value Theorem, the Intermediate Value Theorem or L'Hospital's Rule not verified, BC-ERR-99008 (cr-23:4, cr-23:16, crabbc-25:12). Applies to BC-QA-01011 and, by the record's skills, to BC-QA-01005.
- research/scoring/common-point-losses.md#Notation points [verified]: limit notation introduced then dropped, or arithmetic written with the infinity symbol, BC-ERR-99007 (cr-23:16, cr-23:31). Applies to BC-QA-01010 and to every limit written inside a larger FRQ part.
- research/scoring/common-point-losses.md#Notation points [verified]: vague referent in a justification, BC-ERR-99001. Applies to the continuity and IVT reasons [inferred: no Unit 1 record links BC-ERR-99001; settled by a scoring guideline page rejecting a vague referent in a continuity or IVT reason].
- research/scoring/justification-requirements.md#Theorem hypotheses [verified]: the hypothesis point is earned only by deriving continuity (sg-25:12, sg-26:5, sg-22:14); the conclusion point needs the straddle, continuity and a yes; naming the theorem is optional but must be correct.
- research/scoring/justification-requirements.md#Justify, give a reason, and give reasons [verified]: a "justify" part needs an argument, a "give a reason" part one targeted sentence (sg-25:5, sg-25:17). This governs how long the continuity reason in BC-QA-01006 and 01007 is [inferred: neither archetype has an FRQ example that settles which verb it carries].

## 5. Time budgets per archetype shape

Plan 15 (Fluency, measured and never credited) sets the budget: Part A figure for a no_calculator MCQ shape, Part B for a calculator one, and the part's share of 15 minutes for a free response part, taken here as points over 9 times 15.0. Steps written are the `expected_solution_path` entries; steps a fluent solver leaves unwritten are marked [inferred] with what would settle them.

| Archetype | Shape and budget | Steps a fluent solver writes | Steps held mentally [inferred] |
|---|---|---|---|
| BC-QA-01001 | MCQ, 2.14 min | none on an MCQ; on an FRQ part the two one sided values and the comparison | locating the input, reading each side |
| BC-QA-01002 | MCQ, 2.14 (I-A) or 2.92 (I-B); `either` has no plan 15 rule [inferred: settled by a plan 15 rule for `either`] | none on an MCQ | row grouping by side |
| BC-QA-01003 | MCQ 2.14; FRQ part 1 point of 9, 1.67 min | the combination with supplied limits substituted; denominator condition on a quotient | recording supplied limits |
| BC-QA-01004 | MCQ 2.14; FRQ part share not recorded (no `point_types`) | the separate numerator and denominator limits (sg-23:14), the rewritten form, the value | the factor or conjugate search |
| BC-QA-01005 | FRQ part or MCQ 2.14; three points named in `scoring_pattern`, no FRQ example | bounding inequality, both bound limits, conclusion | the direction of the inequality after multiplying |
| BC-QA-01006 | FRQ part or MCQ 2.14 | value, both one sided limits, comparison, the failed condition named | none: each step is a named output |
| BC-QA-01007 | MCQ 2.14 | none on an MCQ | factoring, one sided limits |
| BC-QA-01008 | MCQ 2.14 or FRQ part | the matching equation at each boundary, the solution | branch evaluation |
| BC-QA-01009 | MCQ 2.14 | none on an MCQ | factoring, sign on each side |
| BC-QA-01010 | FRQ part, 2 points of 9, 3.33 min (BC-FRQ-2025-Q1-C) | the limit expression with the variable tending to infinity, the value (sg-25:4) | the degree comparison |
| BC-QA-01011 | FRQ part, 2 points of 9, 3.33 min (every example) | continuity from differentiability, the straddling inequality, yes (sg-25:12, sg-26:5) | none: every step carries a point |
| BC-QA-01012 | FRQ part, no `point_types`; two points named in `scoring_pattern`, 3.33 min [inferred: no FRQ example] | each average rate with its quotient, the value approached | the sequence of values |
| BC-QA-01013 | MCQ 2.14 | none | the neutral statement of the behaviour |
| BC-QA-01014 | MCQ 2.14 | none | substitution and classification |
| BC-QA-01015 | MCQ 2.14 | none | the excluded inputs |

## 6. Delivery map

Rules are TEMPLATE.md Delivery selection rules 1 to 5, applied in order. Rule 1 makes every worked example and error block `step_reveal` in all 19 lessons, so the table covers the orientation and key ideas. The figure-bearing codes in rule 3 are BC-REP-02, 07, 08, 12, 13 and 14; in this unit only BC-REP-02 occurs on skills. Every non-text choice is [inferred] by the template's own statement, settled by the modality A/B in the build plan.

| Concept | Orientation | Key ideas | Rule and triggering field |
|---|---|---|---|
| BC-CON-01001 | table | motion: a secant closing on the tangent as the interval shrinks; model on the example: average rates at shrinking h | rule 2, a limit process named by BC-SKL-01003 and BC-SKL-01004 ("over shrinking intervals"); rule 4 for BC-REP-03 on BC-SKL-01001, 01004 |
| BC-CON-01002 | figure | motion: a graph zooming toward the input, an open circle at one height and a filled point at another | rule 2, a limit being taken; rule 3, BC-REP-02 on BC-SKL-01008 |
| BC-CON-01003 | text | text | rule 5: BC-SKL-01005 and 01007 carry BC-REP-01 and 04 only |
| BC-CON-01006 | figure | motion: a table of values filling in from both sides toward the input, with model on the example; figure for the scale that hides behaviour | rule 2, a limit process; rule 3, BC-REP-02 on BC-SKL-01009, 01014; rule 4, BC-REP-03 on BC-SKL-01015, 01017 |
| BC-CON-01004 | figure | interactive: a piecewise function with a movable point approaching the boundary from either side, the question being whether the two one sided values agree | rule 3, BC-REP-02 on BC-SKL-01010, 01023, promoted because BC-QA-01001 and BC-QA-01006 `difficulty_variables` vary "whether the one sided limits agree" and the stem asks for a reading |
| BC-CON-01005 | figure | figure for jump and unbounded; motion for oscillation as the window narrows | rule 3, BC-REP-02 on BC-SKL-01011, 01012, 01013; rule 2 for the narrowing window |
| BC-CON-01007 | table | table of supplied limits; text for the denominator condition | rule 4, BC-REP-03 on BC-SKL-01018, 01019, 01020; rule 5 |
| BC-CON-01008 | text | text; the rewriting lives in step_reveal examples | rule 5: BC-SKL-01024 to 01028 carry BC-REP-01 and 04 only |
| BC-CON-01009 | text | text | rule 5: BC-REP-01 and 04 only; the method choice across BC-CON-01007, 01008, 01016, 01017 belongs to a decision lesson (`contrast`) if confusable_sets returns it |
| BC-CON-01010 | figure | motion: two bounding curves pinching toward the input with the trapped curve between | rule 2, a limit being taken; rule 3, BC-REP-02 on BC-SKL-01033, 01035 |
| BC-CON-01011 | figure | figure with a table beside it (2 representations, the cap) | rule 3, BC-REP-02 on BC-SKL-01036, 01038; rule 4, BC-REP-03 on BC-SKL-01036 |
| BC-CON-01012 | figure | figure: removable, jump and asymptote side by side | rule 3, BC-REP-02 on BC-SKL-01039, 01040, 01041; not promoted, since BC-QA-01007 `difficulty_variables` name no varying quantity |
| BC-CON-01013 | figure | interactive: a piecewise graph whose boundary value can be moved, the question being which of the three conditions fails | rule 3, BC-REP-02 on BC-SKL-01044, promoted because BC-QA-01006 `difficulty_variables` vary "whether the function value is defined at the boundary" and "whether the one sided limits agree" |
| BC-CON-01014 | text | text | rule 5: BC-SKL-01046 to 01049 carry BC-REP-01 and 04 only |
| BC-CON-01015 | figure | interactive: one slider on the unknown constant moving one branch until the ends meet | rule 3, BC-REP-02 on BC-SKL-01050, 01053, promoted because BC-QA-01008 `common_givens` name "a piecewise rule with one or two unknown constants" |
| BC-CON-01016 | figure | motion: the input approaching the zero of the denominator from each side, outputs growing without bound with opposite or equal signs | rule 2, a limit being taken; rule 3, BC-REP-02 on BC-SKL-01056, 01057 |
| BC-CON-01017 | figure | motion: the window widening as the variable grows without bound, the curve settling on the horizontal asymptote | rule 2; rule 3, BC-REP-02 on BC-SKL-01059, 01063 |
| BC-CON-01018 | text | model on the example: the ratio of two functions at growing inputs; key idea text | rule 2 names a computed sequence as the idea; BC-SKL-01062 carries BC-REP-01 only, so no figure exists for motion [inferred] |
| BC-CON-01019 | table | table: the straddling pair picked from tabulated values | rule 4, BC-REP-03 on BC-SKL-01065, 01066, 01068; BC-REP-02 sits on BC-QA-01011 only, not on a skill, so rule 3 does not fire |

Where motion and interactive fit, and where they do not: motion is reserved for the limit processes the template names (a secant closing, a table approaching, a window zooming toward a point or out toward infinity, bounds pinching). Interactive fits where a record names a quantity that varies and the stem asks for a reading: the one sided agreement at a boundary (BC-CON-01004), the failed continuity condition (BC-CON-01013) and the matching constant (BC-CON-01015). An epsilon delta tolerance band reading has no triggering record, because the definition is excluded from assessment (ced:39), so no lesson builds it. Notation, procedure choice, interval continuity and algebraic rewriting (BC-CON-01003, 01008, 01009, 01014) are text, because their skills carry only BC-REP-01 and BC-REP-04.

## 7. Library gaps

- 12 of the 15 archetypes carry no `point_types`, so their lessons carry no scoring section.
- `common_givens` is empty on BC-QA-01006, 01007, 01009 and 01014, so their strategy blocks carry `evidence_tag: inferred` (plan 15, Recognition cues).
- `calculator_status` disagrees with official examples: BC-QA-01001 is no_calculator but BC-MCQ-CED-011 is calculator; BC-QA-01006 is no_calculator but BC-MCQ-PE2012-036 is calculator; BC-QA-01011 is no_calculator but BC-FRQ-2026-Q1-D is calculator (research/units/unit-01-limits-continuity.md#Official evidence index [verified]).
- research/units/unit-01-limits-continuity.md#Archetype summary names 2025 Q2(C) for BC-QA-01010, while the record BC-FRQ-2025-Q1-C cites frq-25:3 and sg-25:4.
- research/question-analysis/question-archetypes.md#BC-QA-01011 Existence of a solution argued from the Intermediate Value Theorem says "Scoring point types. none recorded", while the snapshot record lists BC-PT-99015 and BC-PT-99016; that entry also records no common givens or produced objects, which the snapshot record now holds.
- BC-CON-01011 lists no misconceptions.
- `confusable_with` is filled on 67 Unit 1 skills (tools/derive_confusable.py; plan 15 text predates it) but every Unit 1 component crosses a unit or falls outside the size bounds, so the unit has no derived set and Section 3 reads its neighbour pairs from the records.
- No BC-PRQ edge into Unit 1 is `hard_prerequisite`, so prerequisite gaps never block the fringe in this unit.
- Plan 15 gives no budget rule for `calculator_status: either` (BC-QA-01002, 01010, 01012).

## 8. Sources

Library ids: BC-UNIT-01; BC-TOP-0101 to BC-TOP-0116; BC-CON-01001 to BC-CON-01019; BC-SKL-01001 to BC-SKL-01068; BC-PRQ-01001, 01002, 01003, 01004, 01005, 01006, 01007, 01008, 01009, 01010, BC-PRQ-06005; BC-QA-01001 to BC-QA-01015, BC-QA-06011, BC-QA-09012; BC-PT-99004, BC-PT-99015, BC-PT-99016, BC-PT-99054; BC-ERR-01001, 01002, 01003, 01004, 01006, 01008, 01009, 01015, 01016, 01017, 01018, 01019, 01020, 01021, 01023, 01033, BC-ERR-99001, 99007, 99008; BC-MIS-01001 to BC-MIS-01019, BC-MIS-99008, BC-MIS-99009; BC-REP-01 to BC-REP-05, BC-REP-09; BC-DF-01 to BC-DF-17 as listed on the archetypes; BC-FRQ-2014-Q4-B, BC-FRQ-2019-Q2-D, BC-FRQ-2019-Q3-D, BC-FRQ-2022-Q4-B, BC-FRQ-2023-Q5-B, BC-FRQ-2025-Q1-C, BC-FRQ-2025-Q3-B, BC-FRQ-2026-Q1-D, BC-FRQ-2026-Q5-D; BC-MCQ-CED-001, BC-MCQ-CED-011, BC-MCQ-SAMPLE-002, BC-MCQ-PE2012-021, BC-MCQ-PE2012-036.

Pages: ced:38, ced:39, ced:44, ced:46, ced:53; sg-19:4; sg-22:14; sg-23:14; sg-25:3, sg-25:4, sg-25:5, sg-25:12, sg-25:17; sg-26:4, sg-26:5; cr-23:4, cr-23:16, cr-23:31; crabbc-25:12.

Research headings: research/units/unit-01-limits-continuity.md#Unit 1, Limits and Continuity, #What Unit 1 depends on, #Archetype summary, #Misconception summary, #Unresolved, #Official evidence index [verified], and the Representations and Assessment behaviour subsections of #1.1 to #1.16; research/exam/exam-structure.md#Section and part layout, #Free-response point totals; research/scoring/common-point-losses.md#Justification points [verified], #Notation points [verified]; research/scoring/justification-requirements.md#Theorem hypotheses [verified], #Justify, give a reason, and give reasons [verified]; research/question-analysis/question-archetypes.md#BC-QA-01011 Existence of a solution argued from the Intermediate Value Theorem and the BC-QA-01001 to BC-QA-01015 entries; docs/lessons/TEMPLATE.md Delivery; docs/plan/15-lessons.md#What a lesson is, and its granularity [inferred], #Methods, thought process and scoring habits [inferred], #Pacing to the exam date [inferred].

Data files: data/prereq_edges.csv, data/errors.json, data/misconceptions.json, data/scoring_points.json, data/taxonomies.json, data/frq_records.json, data/mcq_records.json.
