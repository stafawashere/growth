---
title: Unit 2 attack map
research_date: 2026-09-29
status: draft
purpose: The map every designer of a Unit 2 (Differentiation, Definition and Fundamental Properties) concept lesson reads first, giving the concept order along the prerequisite edges, the exam shapes the unit feeds, the cross-concept recognition features and confusable sets, the recurring traps with their scoring consequences, the time budgets, and the delivery mode each concept's orientation and key ideas take under TEMPLATE.md's selection rules.
---

# Unit 2 attack map

BC-UNIT-02 holds 15 concepts, BC-CON-02001 to BC-CON-02015, over ten topics on ced:60 to ced:69 (research/units/unit-02-differentiation-definition-properties.md#Unit 2, Differentiation: Definition and Fundamental Properties). LSN-CON-02013 in this directory is the finished reference design. Every claim below cites a library id, a cached page or a research heading; claims without one carry [inferred] and name what would settle them.

## 1. Concept order along the prerequisite edges

Order: a topological sort over the `hard_prerequisite` rows of data/prereq_edges.csv whose both ends are Unit 2 skills, lifted to concepts, ties broken by id. The sort reaches all 15 concepts, and the result coincides with id order. "Hard parents" are Unit 2 concepts holding a hard parent skill; "other parents" are the out-of-unit parents on the same file (BC-PRQ rows are all `supporting`; BC-SKL-01xxx rows are marked hard or supporting as the file states). No `supporting` edge links two different Unit 2 concepts except BC-CON-02003 to BC-CON-02006.

| # | Concept | Name | Skills | Hard parents (Unit 2) | Other parents |
|---|---|---|---|---|---|
| 1 | BC-CON-02001 | Average rate of change as a difference quotient | BC-SKL-02001, 02002, 02003 | none | BC-SKL-01001 (hard and supporting), BC-PRQ-02001, BC-PRQ-02005 |
| 2 | BC-CON-02002 | Instantaneous rate of change as the limit of a difference quotient | BC-SKL-02004, 02005, 02006, 02007 | BC-CON-02001 | BC-SKL-01001 (hard), BC-SKL-01003 (hard and supporting), BC-SKL-01005, BC-PRQ-02005 |
| 3 | BC-CON-02003 | The derivative as a function defined by a limit | BC-SKL-02008, 02009 | BC-CON-02002 | BC-SKL-01024 (hard and supporting), BC-PRQ-02001, BC-PRQ-02005 |
| 4 | BC-CON-02004 | Derivative notation and its equivalent forms | BC-SKL-02010, 02011 | BC-CON-02002 | BC-SKL-01036, BC-PRQ-02004 |
| 5 | BC-CON-02005 | The derivative at a point as the slope of the tangent line | BC-SKL-02012, 02013 | BC-CON-02002 | BC-PRQ-02003 |
| 6 | BC-CON-02006 | Recognising a limit as a derivative of a known function | BC-SKL-02035 | BC-CON-02002 (supporting: BC-CON-02003) | BC-PRQ-02005 |
| 7 | BC-CON-02007 | Estimation of a derivative from tabular or graphical information | BC-SKL-02014, 02015, 02016, 02017, 02018 | BC-CON-02002, BC-CON-02005 | BC-SKL-01001, 01009, 01016, BC-PRQ-02004 |
| 8 | BC-CON-02008 | Differentiability implies continuity | BC-SKL-02019, 02020, 02024 | none | BC-SKL-01043 (hard and supporting), BC-SKL-01040, 01044, 01065 |
| 9 | BC-CON-02009 | Ways a derivative fails to exist at a point of continuity | BC-SKL-02021, 02022, 02023 | BC-CON-02002, BC-CON-02005 | BC-SKL-01043 (hard), BC-SKL-01010, 01012, 01040, BC-PRQ-02001 |
| 10 | BC-CON-02010 | The power rule | BC-SKL-02025, 02026, 02027 | BC-CON-02003, BC-CON-02004 | BC-PRQ-06002 |
| 11 | BC-CON-02011 | Linearity of differentiation | BC-SKL-02028, 02029, 02030, 02031 | BC-CON-02010 | BC-SKL-01018, BC-PRQ-02004 |
| 12 | BC-CON-02012 | Derivatives of the basic transcendental functions | BC-SKL-02032, 02033, 02034 | BC-CON-02004 | BC-PRQ-01005, BC-PRQ-06002, BC-PRQ-06003 |
| 13 | BC-CON-02013 | The product rule | BC-SKL-02036, 02037, 02038 | BC-CON-02011 | none |
| 14 | BC-CON-02014 | The quotient rule | BC-SKL-02039, 02040, 02041, 02042 | BC-CON-02011, BC-CON-02013 | none |
| 15 | BC-CON-02015 | Derivatives of the remaining trigonometric functions by rewriting | BC-SKL-02043, 02044, 02045, 02046 | BC-CON-02012, BC-CON-02014 | BC-PRQ-02002 |

Two roots inside the unit: BC-CON-02001 and BC-CON-02008. BC-CON-02008 hangs on Unit 1 continuity only (BC-SKL-01043), so a fringe that has Unit 1 continuity reaches it before any rate concept. The fringe order in the table is the tie-break order; the engine reaches any concept whose hard parents are mastered (docs/plan/15-lessons.md#Pacing to the exam date [inferred]). Every edge above carries `evidence_tag` inferred in data/prereq_edges.csv (research/units/unit-02-differentiation-definition-properties.md#Prerequisites under 2.1).

## 2. Exam question types the unit feeds

Part budgets are from research/exam/exam-structure.md#Section and part layout [verified]: Section I Part A (no calculator) 29 questions in 62 minutes, 2.14 minutes each; Part B (calculator) 13 in 38, 2.92 each; Section II 2 questions in 30 minutes and 4 in 60, 15.0 minutes each, each question 9 points (research/exam/exam-structure.md#Free-response point totals). Shapes come from each archetype's `multipart_structure` and `official_examples`. Point type names are from data/scoring_points.json.

| Family | Archetype | Shape and part | Point types | Official examples |
|---|---|---|---|---|
| derivative-definition-limit | BC-QA-02002 Derivative computed from the limit definition | MCQ or one part; no calculator, so I-A (or II-B as a part) | none recorded; `scoring_pattern`: difference quotient inside a limit, simplification, value, drawn from the CED [inferred] | BC-MCQ-SAMPLE-006 |
| derivative-definition-limit | BC-QA-02003 Limit recognised as a derivative of a known function | MCQ, I-A | none recorded | none |
| derivative-definition-limit | BC-QA-02014 Rate at an instant found before the derivative is defined | short answer or MCQ opener, served before the derivative is taught; I-A shape | none recorded; no scoring guideline scores an opener | none |
| differentiability-and-continuity | BC-QA-02004 Continuity deduced from differentiability inside a larger argument | one part of a multipart FRQ, no calculator, II-B | none recorded on the archetype; the FRQ records that use the step score it under BC-PT-99015, BC-PT-99016 (BC-QA-01011 parts) and BC-PT-99021, BC-PT-99017 (BC-QA-05001 parts) | none on the record; research names 2025 Q3(B) and 2023 Q4(c) (sg-25:12, sg-23:14) |
| differentiability-and-continuity | BC-QA-02005 Point of non-differentiability identified on a continuous function | MCQ or one part, I-A | none recorded | BC-MCQ-CED-002, BC-MCQ-SAMPLE-003, BC-MCQ-PE2012-011 |
| rule-manipulation | BC-QA-02006 Derivative of a polynomial or power expression by rule | MCQ, I-A | none recorded | none |
| rule-manipulation | BC-QA-02007 Derivative of an expression built from the basic transcendental functions | MCQ, I-A; FRQ parts in II-B | BC-PT-99023 Chain rule, BC-PT-99004 Answer with or without supporting work, BC-PT-99005 Answer with supporting work or setup shown | BC-FRQ-2013-Q3-D, BC-FRQ-2026-Q4-A |
| rule-manipulation | BC-QA-02008 Derivative of a product or a quotient by rule | MCQ or one part, I-A or II-B | BC-PT-99005, BC-PT-99004, BC-PT-99022 Product rule, BC-PT-99080 Quotient rule applied to a ratio of two functions | BC-FRQ-2019-Q5-A, BC-FRQ-2014-Q3-C |
| rule-manipulation | BC-QA-02010 Derivative of a tangent, cotangent, secant, or cosecant expression | MCQ, I-A | none recorded | none |
| derivative-from-table | BC-QA-02009 Derivative of a product or quotient evaluated from supplied values | MCQ, I-A; one FRQ part in II-B | BC-PT-99022, BC-PT-99069 Value of an accumulation function found from geometry of a graph, BC-PT-99004 | BC-FRQ-2021-Q4-B, BC-MCQ-CED-003 |
| derivative-from-table | BC-QA-04002 Approximating a derivative from a table with units | opening part of a table based FRQ; calculator status either, so II-A or II-B | BC-PT-99005, BC-PT-99008 Interpretation of a derivative value in context with units, BC-PT-99006 Units | BC-FRQ-2021-Q1-A, BC-FRQ-2022-Q4-A, BC-FRQ-2024-Q1-A, BC-FRQ-2025-Q3-A, BC-FRQ-2026-Q1-A |
| tangent-line-approximation | BC-QA-02011 Tangent line written at a point on a curve | one FRQ part, II-B; MCQ in I-A | BC-PT-99005, BC-PT-99004, BC-PT-99082 Slope and equation of a tangent line at a point on a curve | BC-FRQ-2015-Q5-A, BC-MCQ-PE2012-019 |
| notation-translation | BC-QA-02012 Derivative notation read or converted | MCQ, I-A | none recorded | none |
| technology-numerical-result | BC-QA-02013 Derivative at a point produced with technology | one FRQ part, calculator, II-A (Part B 2.92 when MCQ shaped) | none recorded; `scoring_pattern`: setup naming the quantity, value to three decimal places (sg-25:4) | none |
| critical-points | BC-QA-05014 Every critical point found, including inputs where the derivative fails to exist (Unit 5, loads BC-SKL-02022, 02023) | MCQ or short answer, I-A | BC-PT-99013 Considers the derivative set equal to zero | none |

Research frame: no 2023 to 2025 FRQ assesses Unit 2 as its main subject, and ten Unit 2 archetypes have no matching free response part in those years (research/units/unit-02-differentiation-definition-properties.md#Unresolved). BC-QA-02001 is retired and superseded by BC-QA-04002 (research/question-analysis/question-archetypes.md#Retired archetypes and their canonical records). BC-UNIT-02 pairs with BC-UNIT-04 inside FRQs, the derivative rule with the contextual reading of its value (research/question-analysis/frq-analysis.md#How concepts combine inside one question). The generated FRQ and MCQ record lists are under research/units/unit-02-differentiation-definition-properties.md#Official evidence index [verified].

## 3. Cross-concept patterns

### Stems that combine concepts

- BC-QA-02014 loads BC-SKL-02005, 02004, 02006, 02012, 02002: BC-CON-02001, 02002 and 02005 in one stem.
- BC-QA-02002 loads BC-CON-02002 (02006, 02007), BC-CON-02003 (02008, 02009) and BC-CON-02010 (02027).
- BC-QA-02003 loads BC-CON-02006 (02035) with BC-CON-02002 (02005).
- BC-QA-02012 loads BC-CON-02004 with BC-CON-02002 (02004).
- BC-QA-02009 loads BC-CON-02013 (02037), BC-CON-02014 (02041) and BC-CON-02007 (02017).
- BC-QA-02011 loads BC-CON-02005; its `difficulty_variables` include whether the derivative needs a product or quotient rule, and BC-MCQ-PE2012-019 loads BC-SKL-02039 with 02012 and 02013 (BC-CON-02014 with BC-CON-02005).
- BC-QA-04002 loads BC-CON-02001 (02002, 02003) and BC-CON-02007 (02014, 02015, 02016) with Unit 4 skills.
- BC-QA-02004 and BC-QA-02005 split BC-CON-02008 from BC-CON-02009; BC-QA-05014 carries BC-CON-02009 into Unit 5.
- BC-QA-02008 spans BC-CON-02013 and 02014; BC-QA-02010 carries BC-CON-02015, whose `expected_solution_path` applies the quotient rule (BC-CON-02014) after rewriting.

### Recognition features between neighbours, and the first written line

The first written line is each archetype's `expected_solution_path[0]`.

| Pair | Feature that selects | First written line |
|---|---|---|
| Average (BC-CON-02001) against instantaneous (BC-CON-02002) rate | an interval with two endpoints asks for an average; a single instant asks for the limit of averages (BC-SKL-02004) | BC-QA-04002: select the two tabulated values the named interval determines. BC-QA-02014: write the average rate over a short interval starting at the instant |
| Limit definition (BC-CON-02003) against the rules (BC-CON-02010 to 02015) | the stem says "use the definition of the derivative" (BC-QA-02002 `typical_wording`); producing the value by rule loses the quotient and simplification points (BC-ERR-02008) | BC-QA-02002: write the difference quotient for the given rule. BC-QA-02006: rewrite radicals and reciprocals as powers |
| A limit to evaluate (BC-CON-02006) against a limit to simplify (Unit 1) | the numerator is a difference of values of a known function at a shifted and a base input (BC-QA-02003 path) | compare the numerator with a difference of function values |
| Differentiability (BC-CON-02008) against continuity (BC-CON-02009) | a stated differentiability supplies continuity; a stated continuity supplies nothing about the derivative (BC-ERR-02012) | BC-QA-02004: read the differentiability statement from the stem. BC-QA-02005: confirm that the function is continuous at the input |
| Product (BC-CON-02013) against quotient (BC-CON-02014) against constant multiple (BC-CON-02011) | two variable factors multiplied; a variable denominator; a constant factor or a constant denominator, which BC-SKL-02042 rewrites instead of using the quotient rule (BC-ERR-02023) | BC-QA-02008: identify the two factors and their derivatives |
| Expand against apply a rule (BC-CON-02013, BC-SKL-02038) | a product of polynomials may be expanded first (research/units/unit-02-differentiation-definition-properties.md#2.8 The Product Rule, Required mathematical knowledge) | the expanded polynomial, then BC-QA-02006's path [inferred: no archetype records expansion as a first step] |
| Derivative from a table against from a graph (BC-CON-02007) | BC-REP-03 givens (BC-SKL-02014, 02016) against BC-REP-02 givens (BC-SKL-02017) | table: select the two tabulated values (BC-QA-04002). Graph: no archetype isolates BC-SKL-02017, so the first line is the two points read off the tangent [inferred, settled by an archetype record for 02017] |
| Supplied values in a rule (BC-QA-02009) against a table estimate (BC-QA-04002) | four values at one input, two of them derivative values, against one quantity at several inputs | BC-QA-02009: record the four supplied values at the named input |
| Remaining trigonometric functions (BC-CON-02015) against basic ones (BC-CON-02012) | tangent, cotangent, secant or cosecant in the expression | BC-QA-02010: rewrite the function using sine and cosine |

### The three confusable sets

`python3 tools/check_lessons.py --sets` derives them by `app/lessons/confusable.py` from `adaptive.common_confusions` and `rival_misconceptions` (docs/plan/15-lessons.md#Decision lessons for confusable sets). The three Unit 2 sets, printed first, map to the decision lessons in printed order [inferred: the id to set pairing is fixed at authoring, per docs/lessons/BUILD-PLAN.md].

- LSN-DEC-02-01, {BC-SKL-02001, 02002, 02003, 02014, 02015, 02016}: BC-CON-02001 against BC-CON-02007. Selector: whether the interval is named by the stem (an average rate, BC-SKL-02002) or must be chosen to bracket a point for a derivative estimate (BC-SKL-02016; BC-QA-04002 `difficulty_variables`: whether the interval is named or must be chosen, whether the point lies inside the interval or at an end). Both demand a quotient and compound units.
- LSN-DEC-02-02, {BC-SKL-02010, 02011, 02012, 02013, 02017, 02018}: BC-CON-02004, 02005 and 02007. Selector: what the stem asks to produce, an equivalent notation (BC-QA-02012), a tangent line equation (BC-QA-02011), a slope read from a graph (BC-SKL-02017) or a value from technology (BC-QA-02013, calculator part).
- LSN-DEC-02-03, {BC-SKL-02019, 02020, 02021, 02022, 02023, 02024}: BC-CON-02008 against BC-CON-02009. Selector: the direction of the given, differentiability given (conclude continuity, BC-QA-02004) against continuity given with a verdict on the derivative asked (one sided slopes, BC-QA-02005), with a discontinuity concluding non-differentiability (BC-SKL-02024).

Product against quotient against constant multiple is not a derived set [inferred: BC-MIS-02011 and 02012 name each other as rivals, yet no set holds 02036 and 02039; settled by the confusable.py rules or a `confusable_with` entry].

## 4. Recurring traps

Computed from data/errors.json and data/misconceptions.json: records whose `skills` or whose skills' `misconceptions` meet two or more Unit 2 concepts. Scoring consequences are the records' own `scoring_consequence` text.

| Record | Name | Concepts | Scoring consequence |
|---|---|---|---|
| BC-ERR-02001 | Difference reported without the quotient | 02001, 02007 | the answer point requires both a difference and a quotient from the table (sg-25:11) |
| BC-ERR-02003 | Units omitted or given as the units of the quantity | 02001, 02007 | the units point is lost; earned for correct compound units attached or not (sg-25:11) |
| BC-ERR-02005 | Increment set to zero before the common factor is divided out | 02003, 02010 | the simplification point and the value point are both lost |
| BC-ERR-02006 | Limit symbol dropped during the computation | 02002, 02003 | a notation point is lost where the definition itself is assessed |
| BC-ERR-02008 | Derivative produced by rule where the definition was demanded | 02003, 02010 | the difference quotient and simplification points are lost although the value may be right |
| BC-ERR-02012 | Implication run backwards from continuity to differentiability | 02008, 02009 | a justification point is lost |
| BC-ERR-02015 | Exponent reduced without multiplying by it | 02010, 02011 | the derivative point is lost |
| BC-ERR-02016 | Constant term differentiated to itself | 02011, 02012 | the derivative point is lost |
| BC-ERR-02021 | Quotient rule numerator terms reversed | 02014, 02015 | the result point is lost (wrong sign) |
| BC-ERR-02023 | Quotient rule applied where the denominator is constant | 02013, 02014 | no point necessarily lost; the extra algebra invites a further error |
| BC-ERR-02024 | Function value used where a derivative value was required | 02006, 02007, 02013, 02014 | the value point is lost |
| BC-ERR-02026 | Trigonometric quotient differentiated term by term | 02014, 02015 | the rule point and the result point are both lost |
| BC-ERR-02030 | Derivative function confused with its value at a point | 02002, 02003, 02004 | the conversion point is lost |
| BC-MIS-02001 | A rate is a difference (severity high) | 02001, 02007 | via BC-ERR-02001 |
| BC-MIS-02002 | The definition of the derivative is a formality to be written and then abandoned (high) | 02003, 02010 | via BC-ERR-02005, 02008 |
| BC-MIS-02003 | The limit symbol is decoration on the final line (medium) | 02002, 02003, 02004 | via BC-ERR-02006 |
| BC-MIS-02006 | Differentiability and continuity are the same property (high) | 02008, 02009 | via BC-ERR-02012 |
| BC-MIS-02008 | Units are decoration rather than part of the answer (medium) | 02001, 02007 | via BC-ERR-02003 |
| BC-MIS-02009 | The power rule is a move on the exponent alone (high) | 02010, 02011 | via BC-ERR-02015, 02016 |
| BC-MIS-02012 | The quotient rule is symmetric (high) | 02014, 02015 | via BC-ERR-02021 |
| BC-MIS-02015 | Derivative notation is a set of interchangeable labels (medium) | 02004, 02007 | via BC-ERR-02030 |

Misconception severities are from research/units/unit-02-differentiation-definition-properties.md#Misconception summary; BC-MIS-02003 and BC-MIS-02012 meet two concepts through the concept records' `misconceptions` lists. A misconception appears in a lesson only as the "a possible reason" line inside its error block (docs/plan/15-lessons.md#What a lesson is, and its granularity).

Point losses research/scoring names for this unit's shapes:

- Table estimate (BC-QA-04002): a value without the quotient, and units missing, of the quantity, or wrong in numerator or denominator (research/scoring/common-point-losses.md#Units points, BC-ERR-99005; cr-22:14, cr-23:7, cr-24:4, crabbc-25:12).
- Limit definition (BC-QA-02002): limit notation introduced then dropped (research/scoring/common-point-losses.md#Notation points, BC-ERR-99007; cr-23:16, cr-23:31); the guidelines make limit notation a point in its own right only for improper integrals (research/scoring/notation-requirements.md#Limit notation), so the Unit 2 notation point in BC-ERR-02006 rests on the archetype's CED-drawn pattern [inferred, settled by a scoring guideline that scores a definition part].
- Rule shapes (BC-QA-02006 to 02010): simplification is optional but an attempted one must be correct (research/scoring/notation-requirements.md#Simplification; sg-23:16, sg-26:14), and an unrequired simplification that introduces an error loses the answer point (research/scoring/common-point-losses.md#Answer points, BC-ERR-99022).
- Tangent line and derivative values: a general derivative expression equated to a number (research/scoring/common-point-losses.md#Notation points, BC-ERR-99002); loose derivative notation is accepted when intent is clear (research/scoring/notation-requirements.md#Derivative notation; sg-25:7, sg-24:8); a "function equals constant" equation loses the point (research/scoring/notation-requirements.md#The equal sign; sg-22:6, sg-23:6).
- Continuity from differentiability (BC-QA-02004): a response stating only that the function is continuous does not earn the point (sg-25:12, in the archetype's `scoring_pattern`); unverified theorem hypotheses (research/scoring/common-point-losses.md#Justification points, BC-ERR-99008); a vague referent (research/scoring/common-point-losses.md#Notation points, BC-ERR-99001). The theorem need not be named (research/scoring/notation-requirements.md#What notation never costs; sg-25:12).
- Technology value (BC-QA-02013): no setup before a numerical answer (research/scoring/common-point-losses.md#Setup points, BC-ERR-99021), fewer than three decimal places (research/scoring/common-point-losses.md#Answer points, BC-ERR-99019).
- Supplied values with parentheses: omitted parentheses when a given expression replaces a named function (research/scoring/common-point-losses.md#Notation points, BC-ERR-99009).

## 5. Time budgets and what a fluent solver writes

MCQ-shaped `no_calculator` archetypes take the Part A budget, `calculator` ones the Part B budget, and a free response part takes `scoring_pattern`'s share of 15.0 minutes (docs/plan/15-lessons.md#Methods, thought process and scoring habits, Fluency). The share below is points on the FRQ record over 9 times 15.0 minutes [inferred arithmetic from research/exam/exam-structure.md#Free-response point totals].

| Archetype | Budget | Written lines (from `expected_solution_path`) | Read, not written [inferred] |
|---|---|---|---|
| BC-QA-02002 | 2.14 min (I-A) | the difference quotient inside a limit, the simplified quotient with the limit kept, the value | the expansion of the shifted term when it is short |
| BC-QA-02003 | 2.14 | the function and base point named, the derivative value | the comparison of the numerator |
| BC-QA-02014 | 2.14 (opener, unscored) | the difference quotient, its simplified form, the value approached | none |
| BC-QA-02004 | inside a II-B question; the continuity statement is one point of a 2-point part (BC-FRQ-2025-Q3-B), 3.33 min for the part | the sentence "continuous because differentiable", then the theorem step | none: the sentence is the point |
| BC-QA-02005 | 2.14 | the two one sided slopes as two numbers, the verdict with its reason | the continuity check when the graph shows it |
| BC-QA-02006, 02007, 02010 | 2.14 | the rewritten powers or sine and cosine form where needed, the derivative | the rule named per term; in FRQ form BC-FRQ-2013-Q3-D and 2026-Q4-A are 2 points, 3.33 min |
| BC-QA-02008 | 2.14; FRQ parts of 3 points (BC-FRQ-2019-Q5-A, 2014-Q3-C), 5.0 min | the rule line with both derivatives present, the result | the factor identification |
| BC-QA-02009 | 2.14; BC-FRQ-2021-Q4-B, 3 points, 5.0 min | the rule with supplied values in place, the value | the labelling of the four values |
| BC-QA-02011 | 2.14; BC-FRQ-2015-Q5-A, 2 points, 3.33 min | the slope, the point of tangency, the point slope equation | none |
| BC-QA-02012 | 2.14 | the equivalent expression | the function and variable identification |
| BC-QA-02013 | 2.92 (I-B) or a share of a II-A question | the setup naming the derivative computed, the value to three decimals (sg-25:4) | the calculator keystrokes |
| BC-QA-04002 | 2 points, 3.33 min, II-A or II-B | the difference over the difference of inputs, the value, the compound units | the choice of rows |

## 6. Delivery map

Rules from docs/lessons/TEMPLATE.md#Delivery: (1) worked examples and error blocks step_reveal; (2) a key idea describing a process is motion, with model on the example only where a computed sequence of values is the idea; (3) a figure-bearing BC-REP (02, 07, 08, 12, 13, 14) on the skill gives figure, promoted to interactive when the archetype's `common_givens` or `difficulty_variables` name a varying quantity and the stem asks for a reading; (4) BC-REP-03 givens give table; (5) otherwise text. Every non-text choice is [inferred], settled by the modality A/B in docs/lessons/BUILD-PLAN.md. Examples and error blocks are step_reveal under rule 1 in every concept and are not repeated below.

| Concept | Orientation | Key ideas | Trigger field |
|---|---|---|---|
| BC-CON-02001 | text, rule 5 | table, rule 4, for the average rate over a tabulated interval | BC-SKL-02002 `representations` BC-REP-03 |
| BC-CON-02002 | text, rule 5 | motion, rule 2: a secant closing to the tangent as h shrinks; model on the example: difference quotients at shrinking h shown as a table beside the secant figure | key idea text from BC-EK-CHA-2B1 (a limit being taken); productive-failure target, BC-QA-02014 carries BC-DF-15 (TEMPLATE.md model row) |
| BC-CON-02003 | text, rule 5 | text, rule 5: the key idea is the algebra of the difference quotient; a key idea worded as the limit being taken would trigger rule 2 and reuses 02002's motion spec [inferred] | skills BC-SKL-02008, 02009 carry BC-REP-01 only |
| BC-CON-02004 | text, rule 5 | figure, rule 3, and table, rule 4, for the graphical and numerical representations of the derivative | BC-SKL-02011 `representations` BC-REP-02, BC-REP-03 |
| BC-CON-02005 | figure, rule 3 | figure, rule 3: the tangent at the point with its slope labelled; no promotion, BC-QA-02011 names no varying quantity read from the figure | BC-SKL-02012, 02013 `representations` BC-REP-02 |
| BC-CON-02006 | text, rule 5 | text, rule 5 | BC-SKL-02035 BC-REP-01 only |
| BC-CON-02007 | text, rule 5 | table, rule 4, for the estimate from a table; static figure, rule 3, for the estimate from a graph; both are enough, nothing varies | BC-SKL-02014, 02016 BC-REP-03; BC-SKL-02017 BC-REP-02 |
| BC-CON-02008 | text, rule 5 | text, rule 5, for the implication; figure, rule 3, for a discontinuity concluding non-differentiability | BC-SKL-02019 BC-REP-04; BC-SKL-02024 BC-REP-02 |
| BC-CON-02009 | figure, rule 3 | figure, rule 3, for corner, cusp and vertical tangent; motion, rule 2, for one sided secants closing to two different slopes [inferred: the key idea describes a one sided limit being taken] | BC-SKL-02021, 02022, 02023 BC-REP-02; BC-QA-02005 `difficulty_variables` corner against cusp against vertical tangent |
| BC-CON-02010 | text, rule 5 | text, rule 5 | BC-SKL-02025 to 02027 BC-REP-01 only |
| BC-CON-02011 | text, rule 5 | text, rule 5 | BC-REP-01 only |
| BC-CON-02012 | text, rule 5 | text, rule 5 | BC-REP-01 only |
| BC-CON-02013 | text, rule 5 | text, rule 5 (LSN-CON-02013#Delivery) | BC-SKL-02036, 02038 BC-REP-01; the BC-REP-03 of 02037 sits on the example's givens |
| BC-CON-02014 | text, rule 5 | text, rule 5; a supplied-values example renders its givens as a table inside step_reveal | BC-SKL-02039, 02040, 02042 BC-REP-01; BC-SKL-02041 BC-REP-03 on the example |
| BC-CON-02015 | text, rule 5 | text, rule 5 | BC-SKL-02043 to 02046 BC-REP-01, 04 |

Where each non-text mode fits: motion and model belong to BC-CON-02002 (the secant closing and the difference quotient table), with motion also on BC-CON-02009's one sided secants. Static figure or table is enough for BC-CON-02004, 02005, 02007 and 02008, where the stem asks for one reading of a fixed graph or table. No concept in the unit meets rule 3's interactive promotion [inferred: no Unit 2 archetype's `common_givens` or `difficulty_variables` names a varying quantity read as a relationship]. The rule concepts, BC-CON-02010 to 02015, are text and step_reveal only.

## 7. Sources

Library ids: BC-UNIT-02; BC-CON-02001 to BC-CON-02015; BC-SKL-02001 to BC-SKL-02046; BC-SKL-01001, 01003, 01005, 01009, 01010, 01012, 01016, 01018, 01024, 01036, 01040, 01043, 01044, 01065; BC-PRQ-01005, 02001, 02002, 02003, 02004, 02005, 06002, 06003; BC-QA-02001 (retired), 02002 to 02014, 04002, 05014, 01011, 05001; BC-PT-99004, 99005, 99006, 99008, 99013, 99015, 99016, 99017, 99021, 99022, 99023, 99069, 99080, 99082; BC-ERR-02001, 02003, 02005, 02006, 02008, 02012, 02015, 02016, 02021, 02023, 02024, 02026, 02030, 99001, 99002, 99005, 99007, 99008, 99009, 99019, 99021, 99022; BC-MIS-02001, 02002, 02003, 02006, 02008, 02009, 02011, 02012, 02015; BC-REP-01, 02, 03, 04, 05, 09; BC-DF-15; BC-EK-CHA-2B1; BC-FRQ-2013-Q3-D, 2014-Q3-C, 2015-Q5-A, 2019-Q5-A, 2021-Q1-A, 2021-Q4-B, 2022-Q4-A, 2024-Q1-A, 2025-Q3-A, 2025-Q3-B, 2026-Q1-A, 2026-Q4-A; BC-MCQ-CED-002, CED-003, SAMPLE-003, SAMPLE-006, PE2012-011, PE2012-019.

Data files: data/prereq_edges.csv, data/errors.json, data/misconceptions.json, data/scoring_points.json, the snapshot from app.content.loader.load_snapshot, tools/check_lessons.py --sets.

Pages: ced:60, ced:69; sg-22:6, sg-23:6, sg-23:14, sg-23:16, sg-24:2, sg-24:8, sg-25:4, sg-25:7, sg-25:11, sg-25:12, sg-26:14; cr-22:14, cr-23:7, cr-23:16, cr-23:31, cr-24:4, crabbc-25:12.

Research headings:
- research/units/unit-02-differentiation-definition-properties.md#Unit 2, Differentiation: Definition and Fundamental Properties
- research/units/unit-02-differentiation-definition-properties.md#2.1 Defining Average and Instantaneous Rates of Change at a Point
- research/units/unit-02-differentiation-definition-properties.md#2.8 The Product Rule
- research/units/unit-02-differentiation-definition-properties.md#Misconception summary
- research/units/unit-02-differentiation-definition-properties.md#Unresolved
- research/units/unit-02-differentiation-definition-properties.md#Official evidence index [verified]
- research/exam/exam-structure.md#Section and part layout
- research/exam/exam-structure.md#Free-response point totals
- research/scoring/common-point-losses.md#Setup points, #Answer points, #Units points, #Justification points, #Notation points
- research/scoring/notation-requirements.md#Limit notation, #The equal sign, #Derivative notation, #Simplification, #What notation never costs
- research/question-analysis/question-archetypes.md#Retired archetypes and their canonical records, and the entries for BC-QA-02002 to 02014 and 04002
- research/question-analysis/frq-analysis.md#How concepts combine inside one question
- docs/plan/15-lessons.md#What a lesson is, and its granularity; #Methods, thought process and scoring habits; #Decision lessons for confusable sets; #Pacing to the exam date
- docs/lessons/TEMPLATE.md#Delivery; docs/lessons/unit-02/LSN-CON-02013.md#Delivery; docs/lessons/BUILD-PLAN.md

[inferred] claims and what settles them:
- The pairing of LSN-DEC-02-01 to 02-03 with the three printed sets: settled at decision lesson authoring (docs/lessons/BUILD-PLAN.md).
- Product, quotient and constant multiple absent from the derived sets: settled by confusable.py's rules or a `confusable_with` entry.
- Expansion as a first line and the first line for a graph estimate (BC-SKL-02017): settled by archetype records carrying those paths.
- The notation point for a definition part and BC-QA-02002's three-point pattern: settled by a scoring guideline that scores a definition part.
- FRQ part minutes as points over 9 of 15.0, and the read-not-written column: settled by the fluency telemetry in app/progress/fluency.py.
- Every motion, figure, table and model choice, and the absence of interactive: settled by the modality A/B in docs/lessons/BUILD-PLAN.md.

Library gaps: BC-QA-02002, 02003, 02004, 02005, 02006, 02010, 02012, 02013, 02014 carry no `point_types`; BC-QA-02004 lists no `official_examples` although the research names 2025 Q3(B) and 2023 Q4(c); no archetype isolates BC-SKL-02017; `confusable_with` is filled on 45 Unit 2 skills and the three sets come from it; every Unit 2 prerequisite edge is tagged inferred.
