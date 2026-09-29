---
title: Unit 5 attack map, Analytical Applications of Differentiation
research_date: 2026-09-29
status: draft
purpose: The map every designer of the 15 BC-UNIT-05 concept lessons reads first, giving the concept order along the prerequisite edges, the exam shapes the unit feeds and their justification points, the cross-concept recognition features and confusable set, the recurring traps, the time budgets and the delivery mode each concept's orientation and key ideas take under TEMPLATE.md's selection rules.
---

# Unit 5 attack map, Analytical Applications of Differentiation

Every fact below comes from the library snapshot (`app.content.loader.load_snapshot`), data/prereq_edges.csv, data/errors.json, data/misconceptions.json, data/scoring_points.json or the research files, cited by id, page or heading. Claims with no such source are tagged [inferred] with what would settle them. The per-concept lesson designs follow docs/lessons/TEMPLATE.md and the finished example docs/lessons/unit-02/LSN-CON-02013.md.

## 1. Concept order along the prerequisite edges

The order is a topological sort of the 15 BC-CON ids of BC-UNIT-05, where concept A is a parent of concept B when a `hard_prerequisite` edge in data/prereq_edges.csv runs from a skill of A to a skill of B, ties broken by id. Every intra-unit edge runs from a lower id to a higher one, so the order equals id order. "Unit parents" are Unit 5 concepts; "outside parents" are concepts or topics in other units reached by `hard_prerequisite` edges; "BC-PRQ parents" are the `supporting` edges from prerequisite records.

| # | Concept | Name | Skills | Unit parents | Outside parents (hard) | BC-PRQ parents (supporting) |
|---|---|---|---|---|---|---|
| 1 | BC-CON-05001 | Mean Value Theorem as an existence result | BC-SKL-05001 to 05006 | none | BC-CON-02008 (via BC-SKL-02019), BC-CON-04002 (via BC-SKL-04004), BC-TOP-0102 | BC-PRQ-05001, 05004, 05008, BC-PRQ-06005 |
| 2 | BC-CON-05002 | Extreme Value Theorem as an existence result | BC-SKL-05007 to 05009 | none | BC-CON-01014 (via BC-SKL-01046), BC-TOP-0102 | BC-PRQ-05004 |
| 3 | BC-CON-05003 | Critical points and the local versus global distinction | BC-SKL-05010 to 05013 | none | BC-CON-02009 (via BC-SKL-02021), BC-CON-02010 (via BC-SKL-02025), BC-CON-04002 (via BC-SKL-04001) | BC-PRQ-05001, 05003, 05006 |
| 4 | BC-CON-05004 | Monotonicity read from the sign of the first derivative | BC-SKL-05014 to 05018 | none | BC-CON-02010 (via BC-SKL-02027), BC-CON-04002 (via BC-SKL-04001) | BC-PRQ-05001, 05002, 05003, 05006 |
| 5 | BC-CON-05005 | First derivative test for relative extrema | BC-SKL-05019 to 05023 | BC-CON-05003, BC-CON-05004 | none | none |
| 6 | BC-CON-05006 | Candidates test for absolute extrema on a closed interval | BC-SKL-05024 to 05029 | BC-CON-05003, BC-CON-05004 | none | BC-PRQ-05004, BC-PRQ-06005 |
| 7 | BC-CON-05007 | Concavity as the monotonicity of the first derivative | BC-SKL-05030, 05031 | BC-CON-05004 | BC-CON-03009 (via BC-SKL-03030), BC-TOP-0205 | BC-PRQ-05001, 05002, 05006 |
| 8 | BC-CON-05008 | Point of inflection as a change of concavity | BC-SKL-05032 to 05035 | BC-CON-05007 | BC-CON-03009 (via BC-SKL-03030) | BC-PRQ-05001, 05003 |
| 9 | BC-CON-05009 | Second derivative test at a critical point | BC-SKL-05036, 05037, 05039 | BC-CON-05003, 05005, 05007 | none | none |
| 10 | BC-CON-05010 | A sole relative extremum as an absolute extremum | BC-SKL-05038 | BC-CON-05005, 05009 | none | none |
| 11 | BC-CON-05011 | Graph of a function reconstructed from its derivative graphs | BC-SKL-05040 to 05044 | BC-CON-05004, 05007, 05008 | BC-CON-02013 (via BC-SKL-02037) | BC-PRQ-05006 |
| 12 | BC-CON-05012 | Simultaneous reading of a function and its first two derivatives | BC-SKL-05045 to 05048 | BC-CON-05004, 05007, 05011 | none | BC-PRQ-06005 |
| 13 | BC-CON-05013 | Optimisation model with an objective and a constraint | BC-SKL-05049 to 05053 | BC-CON-05003, 05006, 05010 | BC-CON-04007 (via BC-SKL-04017) | BC-PRQ-05003, 05005 |
| 14 | BC-CON-05014 | Interpretation of an optimal value in context | BC-SKL-05054 to 05057 | BC-CON-05006, 05013 | none | none |
| 15 | BC-CON-05015 | Critical points and behaviour of an implicit relation | BC-SKL-05058 to 05063 | BC-CON-05009 | BC-CON-03004 (via BC-SKL-03014), BC-CON-03005 (via BC-SKL-03012), BC-TOP-0301 | BC-PRQ-05001, BC-PRQ-05007 |

Skill ranges are consecutive ids except where listed; BC-SKL-05038 belongs to BC-CON-05010, not BC-CON-05009.

Supporting edges from other skills (not ordering): BC-SKL-01059 to 05031, BC-SKL-01067 to 05001, BC-SKL-04030 to 05046, BC-SKL-06021 to 05010, BC-SKL-06025 to 05033, BC-SKL-06026 to 05028, BC-TOP-0115 to 05011, BC-TOP-0402 to 05049.

BC-PRQ names: BC-PRQ-05001 solving equations and inequalities to locate where an expression is zero or undefined; 05002 sign analysis of a factored expression across a number line; 05003 domain of a function; 05004 interval notation and the open versus closed distinction; 05005 area, perimeter, volume and similar figure relations; 05006 reading features of a graph; 05007 solving a system of a defining relation and a derived equation; 05008 average rate of change as a difference quotient; 06005 reading function notation, composition and evaluation.

Longest intra-unit chain: BC-CON-05004 to 05005 to 05009 to 05010 to 05013 to 05014, which is why the two optimisation concepts come last in the fringe.

## 2. Exam question types the unit feeds

Exam parts and budgets from research/exam/exam-structure.md#Section and part layout: Section I Part A, 29 MCQ in 62 minutes, no calculator, 2.14 minutes per question; Part B, 13 MCQ in 38 minutes, calculator required, 2.92; Section II, 2 calculator questions in 30 minutes and 4 no-calculator in 60, 15.0 minutes per question, each worth 9 points (research/exam/exam-structure.md#Free-response point totals). An archetype with `calculator_status` either can sit in either part of its section.

Fourteen archetypes load a Unit 5 skill, in nine families. Point types and official examples are the archetype record's `point_types` and `official_examples`; "none" means the field is empty (a library gap, section 7). Shapes and scoring patterns are from research/question-analysis/question-archetypes.md, under the family and archetype heading named.

| Family | Archetype | Shape | Exam part | Point types | BC-FRQ official examples |
|---|---|---|---|---|---|
| mean-value-theorem | BC-QA-05001 MVT existence justification | FRQ part, 2 points | Section II, A or B (either) | BC-PT-99021, BC-PT-99017 | BC-FRQ-2013-Q3-B, 2021-Q4-D, 2023-Q1-B, 2018-Q4-B (also BC-MCQ-CED-013, BC-MCQ-SAMPLE-014) |
| mean-value-theorem | BC-QA-05002 solving for c | FRQ part or MCQ | Section I A or B; Section II | none | none |
| evt-existence | BC-QA-05010 EVT existence claim | MCQ or short FRQ part | Section I Part A; Section II Part B (no_calculator) | none | none |
| critical-points | BC-QA-05014 every critical point, including where f prime fails to exist | MCQ-shaped list | Section I Part A (no_calculator) | BC-PT-99013 | none |
| monotonicity-analysis | BC-QA-05008 intervals of increase or decrease with reason | FRQ part or MCQ | either | BC-PT-99005, 99063, 99010 | BC-FRQ-2022-Q3-C, 2024-Q1-D (also BC-MCQ-SAMPLE-012, BC-MCQ-PE2012-030) |
| extremum-classification | BC-QA-05003 relative extremum from f prime | FRQ part, 1 point | either | BC-PT-99012, 99013 | BC-FRQ-2013-Q4-A, 2015-Q4-C, 2015-Q5-B, 2023-Q4-A |
| extremum-classification | BC-QA-05007 critical point of a function given indirectly | FRQ part, 2 or 3 points | Section II Part B (no_calculator) | BC-PT-99013, 99005, 99004, 99014, 99012 | BC-FRQ-2021-Q3-B, 2015-Q5-C, 2024-Q3-B, 2026-Q2-C |
| extremum-classification | BC-QA-05013 second derivative test | FRQ part or MCQ | either | none | none |
| absolute-extremum-candidates | BC-QA-05006 candidates test with global justification | FRQ part, 3 points | either | BC-PT-99013, 99004, 99011, 99005 | BC-FRQ-2013-Q4-B, 2022-Q3-D, 2023-Q4-D, 2025-Q1-D, 2025-Q4-D, 2026-Q4-D |
| concavity-analysis | BC-QA-05004 intervals of concavity with reason | FRQ part, 2 points | either | BC-PT-99062, 99063 | BC-FRQ-2013-Q4-C, 2014-Q3-B, 2023-Q4-B, 2026-Q4-C, 2018-Q3-C (also BC-MCQ-PE2012-037) |
| concavity-analysis | BC-QA-05005 points of inflection with reason tied to the graph | FRQ part, 2 points | Section II Part B (no_calculator) | BC-PT-99060, 99061 | BC-FRQ-2022-Q3-B, 2025-Q4-B, 2026-Q4-B, 2018-Q3-D (also BC-MCQ-CED-014, BC-MCQ-PE2012-034) |
| function-derivative-graph-relationship | BC-QA-05009 graphs of f, f prime, f double prime | MCQ, or FRQ feature question | either | none | none (MCQ: BC-MCQ-SAMPLE-011, BC-MCQ-PE2012-029, 033, 041, 045) |
| optimisation | BC-QA-05011 applied optimisation | multipart FRQ or MCQ with reduced objective | either | none | none |
| implicit-differentiation | BC-QA-05012 critical points and second derivative of an implicit relation | FRQ part, 2 or 3 points | Section II Part B (no_calculator) | none | none |

### Justification points and what a reader accepts

From data/scoring_points.json (fields `earns`, `does_not_earn`) and research/scoring/justification-requirements.md:

- BC-PT-99013, considers the derivative equal to zero. Earns: the equation f prime equals zero, discussing a sign change, or the phrase "critical points of" the function. Does not earn: the solved critical value alone (sg-25:5, sg-25:9, sg-26:17, sg-25:19).
- BC-PT-99012, classification by a derivative test. Earns: relative maximum, minimum or neither with first or second derivative analysis; the test need not be named. Does not earn: a candidates test, or an assertion with no sign or second derivative analysis (sg-26:8). For BC-QA-05003 the classification and reason are one point, and "positive before and after" with no "does not change sign" does not earn it (research/question-analysis/question-archetypes.md#BC-QA-05003, sg-23:13).
- BC-PT-99010, sign analysis. Earns: the derivative positive on one side and negative on the other, closed by a global claim on the interval (sg-25:5, sg-25:9). Does not earn: a bare first or second derivative test without the statement that the critical point is the only one (sg-25:5, sg-22:12; research/scoring/justification-requirements.md#Global versus local arguments).
- BC-PT-99011, candidates test. Earns: the function evaluated at every interior critical point and both endpoints, correct to the first decimal (sg-25:5, sg-25:19). Does not earn: a missing endpoint, an evaluation error, or extra x-values (sg-23:15, sg-25:19; research/scoring/justification-requirements.md#The candidates test).
- BC-PT-99014, considers the sign of a derivative. Does not earn: the sign of the function instead of the derivative, or the concavity of the derivative (sg-26:12).
- BC-PT-99017, MVT or Rolle conclusion. Earns: correct average rate, differentiability on the open interval, continuity on the closed interval, and yes (sg-23:3, sg-21:17). Does not earn: an appeal to the Intermediate Value Theorem (sg-23:3). The hypothesis must be derived ("continuous because differentiable"), not asserted (sg-25:12, sg-26:5; research/scoring/justification-requirements.md#Theorem hypotheses).
- BC-PT-99021, average rate of change expression: a difference of outputs over a difference of inputs with values substituted, not a bare template (sg-25:11, sg-26:2).
- BC-PT-99060 and BC-PT-99061, inflection list and reason. The list must be complete with no extra value inside the interval, else both points go (sg-25:17, sg-26:15). The reason must be about the graphed object: the graphed f prime changes from increasing to decreasing, its slope changes sign, or it has a relative extremum. "f changes concavity" or "f double prime changes sign" earns the list but not the reason, and "the function" or "the graph" as subject forfeits it (sg-25:17, sg-26:15, sg-22:11; research/scoring/justification-requirements.md#Reasons tied to the object the prompt names).
- BC-PT-99062 and BC-PT-99063, interval and reason for a compound condition. Both halves must be cited (the derivative positive and decreasing); one half earns the interval point only (sg-26:16, sg-23:14).

BC-QA-05010 (EVT) is scored in research by analogy with the MVT and IVT existence parts (research/question-analysis/question-archetypes.md#BC-QA-05010, family tagged [inferred]); no BC-FRQ example is on the record.

## 3. Cross-concept patterns

### What the stems combine

- Extremum chain: BC-QA-05006 loads BC-SKL-05010 (BC-CON-05003) with 05024 to 05029 (BC-CON-05006); BC-QA-05007 loads 05010, 05020 and 05039 (BC-CON-05003, 05005, 05009); BC-QA-05013 loads 05036 to 05039 (BC-CON-05009 and 05010).
- Graph questions: BC-QA-05009 loads nine skills across BC-CON-05011 and 05012; BC-QA-05005 and 05004 load BC-CON-05007 and 05008 through BC-SKL-05035.
- Optimisation: BC-QA-05011 loads BC-CON-05013 and 05014 and, through the hard edges BC-SKL-05028 to 05053 and 05038 to 05053, rests on the candidates test and the sole extremum rule.
- Across units: BC-UNIT-05 with BC-UNIT-06 is the second pairing in the corpus, because an extremum of an accumulated quantity needs the candidates argument and the integral (research/question-analysis/frq-analysis.md#How concepts combine inside one question). BC-QA-05006 dv "whether candidate values come from a formula or from accumulated area" and BC-QA-05007 givens "an accumulation function built on a plotted integrand" carry that pairing.

### Recognition features between neighbours

| Neighbours | Feature in the stem that selects | Source |
|---|---|---|
| MVT (05001) against Rolle against EVT (05002) | Asked for a point where f prime equals a value, from an average rate: MVT; equal endpoint outputs make the average rate zero, and Rolle is accepted in the same point; asked whether a maximum or minimum value exists on a closed interval: EVT, whose only hypothesis is continuity on the closed interval. IVT in an MVT answer forfeits the conclusion | BC-PT-99017, sg-23:3, BC-SKL-05006, BC-SKL-05007, BC-QA-05010 dv "whether the interval is closed" |
| First derivative test (05005) against second derivative test (05009) against candidates test (05006) | "relative" or "local" at a named input: first or second derivative test, and a candidates test does not earn BC-PT-99012 (sg-26:8); "absolute" on a closed interval: candidates test or global sign argument, and a local test alone does not earn the justification (sg-25:5, sg-25:19); derivative given only as a graph: first derivative test, since the second derivative test needs the slope of that graph discussed (BC-QA-05003 wrong_approaches) | research/scoring/justification-requirements.md#Global versus local arguments, BC-SKL-05039 |
| Relative against absolute extremum (05003, 05010) | The word "absolute" or "on the closed interval" in the prompt; a sole critical point on an interval lets a local test become global with the uniqueness clause | sg-22:12, sg-25:5, BC-SKL-05012, BC-SKL-05038 |
| Inflection (05008) against a zero of f double prime | A candidate is where f double prime is zero or undefined; it is an inflection only if f double prime changes sign; a touching zero is rejected | BC-SKL-05032 to 05034, BC-QA-05005 dv "whether a candidate is a touching zero with no sign change" |
| Graph of f against graph of f prime (05011, 05012) | The axis label or caption names the plotted object; features of f are read from the sign of f prime and from where f prime rises or falls, and the reason is phrased about the plotted object | BC-MIS-05011, sg-25:16, sg-25:17, BC-QA-05005 dv "whether the given object is f, f prime, or an integrand" |
| Positive f prime against increasing f prime (05004 against 05007) | "increasing" asks for the sign of f prime; "concave up" asks whether f prime rises | BC-ERR-05016, BC-MIS-05020, sg-23:14 |

### First written line per method

From each archetype's `expected_solution_path[0]`:

| Archetype | First written step |
|---|---|
| BC-QA-05001 | state that differentiability supplies continuity on the closed interval |
| BC-QA-05002 | compute the average rate of change |
| BC-QA-05010 | check the interval is closed |
| BC-QA-05014 | differentiate the function |
| BC-QA-05008 | find the zeros and undefined points of the derivative |
| BC-QA-05003 | locate the named input on the derivative information |
| BC-QA-05007 | write the derivative from the given relation |
| BC-QA-05013 | confirm the first derivative is zero at the point |
| BC-QA-05006 | consider the derivative equal to zero and solve |
| BC-QA-05004 | identify where the derivative is decreasing |
| BC-QA-05005 | find where the given plot changes from increasing to decreasing or the reverse |
| BC-QA-05009 | find the turning points of each curve |
| BC-QA-05011 | define the variables and write the objective |
| BC-QA-05012 | differentiate the relation implicitly |

For BC-QA-05006 and 05007 the first line is itself a point (BC-PT-99013), so writing f prime of x equals 0 as an equation, not only its solution, is the scored form (sg-25:5).

### The confusable set, LSN-DEC-05-01

`tools/check_lessons.py --sets` returns one Unit 5 set: {BC-SKL-05058, BC-SKL-05059}, horizontal tangent points against vertical tangent points of an implicit relation, both in BC-CON-05015. Both skills name BC-MIS-05031 in `adaptive.common_confusions` ("a relation has critical points only where its derivative is zero", ced:110).

- BC-SKL-05058 is selected when the stem asks for a horizontal tangent (dy/dx equal to zero): the numerator of dy/dx is zero and the denominator is not. Error: BC-ERR-05057, horizontal tangent points found without checking the denominator (ced:110).
- BC-SKL-05059 is selected when the stem asks for a vertical tangent (dy/dx fails to exist): the denominator is zero and the numerator is not. Error: BC-ERR-05058, vertical tangent points reported without a matching point on the relation (ced:110).
- Both finish at BC-SKL-05060, solving the defining relation and the derived condition together; BC-ERR-05059 (one coordinate reported where a point was asked for, ced:110) is shared.

The derived sets hold no set for the first derivative test against the second derivative test against the candidates test, although BC-SKL-05039 is a choice between tests and sg-26:8 and sg-25:19 score the choice. Every skill's `confusable_with` is empty (docs/plan/15-lessons.md#Methods, thought process and scoring habits). Whether a second decision lesson for that trio is warranted is [inferred]; settled by adding `adaptive.common_confusions` links among BC-SKL-05020, 05036, 05026 and rerunning `--sets`.

## 4. Recurring traps

Computed from the skills of each concept (`common_errors`) and the concepts' `misconceptions`; only records reaching two or more Unit 5 concepts are listed. Scoring consequences are the records' `scoring_consequence` fields.

### BC-ERR records

| Record | Name | Concepts | Scoring consequence (record) | Sources |
|---|---|---|---|---|
| BC-ERR-99004 | Local argument offered where a global argument is required | 05003, 05006, 05010, 05013, 05014 | justification point for the absolute extremum not earned; answer point may still be available | cr-22:11, cr-22:4, cr-23:16, crabbc-25:4, crabbc-25:18, crabbc-25:30, sg-25:19, sg-25:5, sg-25:9 |
| BC-ERR-99001 | Vague referent in a justification | 05001, 05004, 05005, 05008 | reasoning or justification point not earned even when the conclusion is correct | cr-22:18, cr-22:14, cr-22:11, cr-23:16, cr-24:11, crabbc-25:16, crabbc-25:18 |
| BC-ERR-99008 | Hypotheses of a theorem not verified before its conclusion is used | 05001, 05002 | condition point not earned | cr-22:14, cr-23:4, cr-23:16, crabbc-25:12, crabbc-25:14, sg-23:3 |
| BC-ERR-05016 | Increase of the derivative confused with positivity of the derivative | 05004, 05007, 05011 | intervals belong to the other question and the reason point is unavailable | sg-23:14 |
| BC-ERR-05024 | Location reported where the value was asked for | 05005, 05006, 05014 | answer point lost; 2023 awarded it only for the minimum value | sg-23:15 |
| BC-ERR-05013 | Critical point with no sign change declared an extremum | 05003, 05005 | single answer with reason point lost | sg-23:13 |
| BC-ERR-05018 | Justification uses an unnamed referent | 05004, 05005 | reason point lost | sg-25:17 |
| BC-ERR-05026 | One or both endpoints omitted from the candidate comparison | 05006, 05014 | justification point lost | sg-23:15, sg-25:19 |

### BC-MIS records

| Record | Name | Concepts | Severity | Observable errors | Sources |
|---|---|---|---|---|---|
| BC-MIS-05001 | Hypotheses are decoration and the conclusion is the theorem | 05001, 05002 | high | BC-ERR-05001, 05002 | sg-23:3 |
| BC-MIS-05004 | An existence theorem locates the point it asserts | 05001, 05002 | medium | BC-ERR-05005, 05008 | ced:99, ced:100 |
| BC-MIS-05007 | A relative extremum is an absolute extremum | 05003, 05006 | high | BC-ERR-05012 | sg-25:19 |
| BC-MIS-05008 | Every critical point is an extremum | 05003, 05005 | high | BC-ERR-05013, 05020 | sg-23:13 |
| BC-MIS-05011 | The plotted curve is the function under discussion | 05004, 05011, 05012 | high | BC-ERR-05015, 05041, 05042, 05046, 06008, 06009 | sg-25:16, sg-25:17 |
| BC-MIS-05013 | Restating the conclusion counts as a reason | 05004, 05005, 05008 | high | BC-ERR-05018, 05035 | sg-25:17 |
| BC-MIS-05015 | The location of an extremum and its value are the same answer | 05005, 05006, 05014 | medium | BC-ERR-05024 | sg-23:15 |
| BC-MIS-05018 | A local test settles a global question | 05006, 05010 | high | BC-ERR-05012, 99004, 05039 | sg-25:19 |
| BC-MIS-05020 | Concavity and monotonicity are the same property | 05007, 05012 | high | BC-ERR-05016, 05031, 05044, 05047, 06007 | sg-23:14, ced:119, ced:122 |

### Point losses research/scoring names for these shapes

- research/scoring/common-point-losses.md#Justification points: hypotheses of the MVT not verified (BC-ERR-99008; cr-23:4, cr-23:16, crabbc-25:12); local sign change where a global argument or complete candidates test was required (BC-ERR-99004; cr-23:16, crabbc-25:4, crabbc-25:18, crabbc-25:30); reasoning not tied to the given graph (BC-ERR-99023; cr-23:16, crabbc-25:17). The same heading records that in 2025 the two lowest-mean points on their questions were justification points (crabbc-25:15, crabbc-25:28).
- research/scoring/common-point-losses.md#Notation points: vague referent such as it, the function, the graph (BC-ERR-99001; cr-23:16, cr-24:11, crabbc-25:16, crabbc-25:18).
- research/scoring/common-point-losses.md#Setup points: no calculator setup shown before a numerical answer (BC-ERR-99021), which applies to the calculator variants of BC-QA-05002 and 05011 (research/units/unit-05-analytical-applications-differentiation.md#5.10 Introduction to Optimization Problems, Assessment behaviour).
- research/scoring/common-point-losses.md#Answer points: fewer than three decimal places (BC-ERR-99019), which applies to calculator-reported optimal values (research/units/unit-05-analytical-applications-differentiation.md#5.11 Solving Optimization Problems, Assessment behaviour); candidate evaluations are held only to the first decimal (sg-25:5, sg-25:9).
- research/scoring/common-point-losses.md#Units points and #Interpretation points: units and the interval omitted from an interpretation (BC-ERR-99005, BC-ERR-99027), which apply to BC-CON-05014.

## 5. Time budgets per archetype shape

The FRQ budget per point is 15.0 minutes over 9 points, 1.67 minutes, applied to the part's point count from its scoring pattern (docs/plan/15-lessons.md#Methods, thought process and scoring habits, Fluency). The steps written are the scored components; steps not scored are listed as skippable only where a record says so.

| Archetype | Shape and budget | Steps a fluent solver writes | Not required on the record |
|---|---|---|---|
| BC-QA-05001 | FRQ 2 points, 3.3 min | average rate as a difference over a difference with values; "continuous because differentiable"; yes, with MVT or Rolle | naming the theorem (sg-21:17) |
| BC-QA-05002 | MCQ 2.14 or 2.92 min; FRQ share | average rate; the equation f prime of c equals it; solved c inside the interval | none recorded |
| BC-QA-05010 | MCQ 2.14 min | closed interval check; continuity statement; conclusion | differentiating (wrong approach, BC-QA-05010) |
| BC-QA-05014 | MCQ 2.14 min | f prime; zeros; inputs where f prime fails to exist within the domain | none recorded |
| BC-QA-05008 | FRQ part share or MCQ | zeros and undefined points of f prime; intervals; reason naming the sign of the named derivative | a drawn sign chart earns nothing (research/scoring/justification-requirements.md#Sign analysis of a derivative) |
| BC-QA-05003 | FRQ 1 point, 1.7 min | classification plus "f prime does not change sign" or "changes from positive to negative" | intervals, though any given must be correct (sg-23:13) |
| BC-QA-05007 | FRQ 2 or 3 points, 3.3 to 5.0 min | sign of the derivative considered; the input; answer with reason | naming the test, restating the critical value (sg-26:8) |
| BC-QA-05013 | FRQ part share or MCQ | f prime zero at the point; sign of f double prime; classification | none recorded |
| BC-QA-05006 | FRQ 3 points, 5.0 min | f prime equals 0 as an equation; every candidate evaluated, both endpoints; the value | candidates eliminated as local maxima or by reference to an earlier part (sg-23:15) |
| BC-QA-05004 | FRQ 2 points, 3.3 min | intervals; reason about f prime rising or falling | endpoints of intervals (sg-23:14) |
| BC-QA-05005 | FRQ 2 points, 3.3 min | complete list; reason about the graphed object | interval endpoints (sg-25:17) |
| BC-QA-05009 | MCQ 2.14 or 2.92 min | turning points of each curve; the assignment | none recorded |
| BC-QA-05011 | multipart FRQ | objective in one variable; domain; critical point; verification; value with units | none recorded |
| BC-QA-05012 | FRQ 2 or 3 points, 3.3 to 5.0 min | implicit differentiation; substitution of dy/dx; value | none recorded |

Point counts per FRQ part are from research/question-analysis/question-archetypes.md, each archetype's Multipart structure. No time target is set; the budget is the exam's (docs/plan/15-lessons.md#Pacing to the exam date).

## 6. Delivery map

Rules are TEMPLATE.md#Delivery selection rules 1 to 5. Figure-bearing representations are BC-REP-02, 07, 08, 12, 13, 14. Worked examples and error blocks are step_reveal by rule 1 in every lesson and are not repeated below. Every non-text choice is [inferred] per TEMPLATE.md; settled by the modality A/B (skip rate and time to first credited success by mode).

| Concept | Orientation | Key ideas | Rule and triggering field |
|---|---|---|---|
| BC-CON-05001 MVT | text | hypotheses and conclusion: text; average rate from a short table: table | rule 5; rule 4 on BC-REP-03 in BC-SKL-05002, 05003, 05006 and BC-QA-05001 common_givens "a short table of values". No skill carries a figure-bearing REP, so no secant figure is triggered |
| BC-CON-05002 EVT | text | continuity on a closed interval: figure (a graph with a break inside the interval) | rule 3 on BC-REP-02 in BC-SKL-05008; not promoted, because BC-QA-05010 difficulty_variables are yes or no features, not a varying quantity |
| BC-CON-05003 critical points | figure | f prime zero and f prime undefined (cusp, corner, vertical tangent): figure; relative against absolute: figure | rule 3 on BC-REP-02 in BC-SKL-05010 to 05013; BC-QA-05014 dv "whether the failure is a cusp, a vertical tangent or a corner" is categorical, so static |
| BC-CON-05004 monotonicity | figure | sign of f prime against rise of f: interactive, one draggable point on the graph of f prime with the question "is f rising here?"; sign chart from a formula: text | rule 3 on BC-REP-02 in BC-SKL-05015, promoted by BC-QA-05008 dv "whether the derivative changes sign at an undefined point" and the stem's reading of intervals; BC-SKL-05014, 05016 carry BC-REP-01, 04 only, rule 5 |
| BC-CON-05005 first derivative test | text | sign change at a critical point: interactive, a point sliding through the named input on a graph of f prime made of segments and arcs, reading the sign each side; "neither" case: figure | rule 3 on BC-REP-02 in BC-SKL-05019 to 05021, promoted by BC-QA-05003 common_givens "a graph of the derivative made of segments and arcs", "a named input" and dv "whether the answer is neither" |
| BC-CON-05006 candidates test | text | candidate list from the graph of f prime: figure; comparison of candidate values: table | rule 3 on BC-REP-02 in BC-SKL-05024, 05025; rule 4 on BC-REP-03 in BC-SKL-05026, 05028 |
| BC-CON-05007 concavity | figure | concavity as f prime rising: interactive, a point sliding along the graph of f prime with the tangent drawn on f, reading whether f prime rises and whether f is concave up | rule 3 on BC-REP-02 in BC-SKL-05031, promoted by BC-QA-05004 common_givens "a graph of the derivative" and dv "whether the question asks for concave up or concave down"; TEMPLATE names concavity against the tangent as an interactive case |
| BC-CON-05008 inflection | text | inflection as a sign change of f double prime: interactive, a sign chart built from a graph of f prime by dragging a point and recording where f prime turns; touching zero of f double prime: figure | rule 3 on BC-REP-02 in BC-SKL-05032 to 05035, promoted by BC-QA-05005 dv "how many points of inflection there are" and "whether a candidate is a touching zero with no sign change" |
| BC-CON-05009 second derivative test | text | test and its inconclusive case: text | rule 5; BC-SKL-05036, 05037, 05039 carry BC-REP-01, 04, 06 only, and BC-SKL-05039's BC-REP-02 serves the choice of test, a text block |
| BC-CON-05010 sole extremum | text | uniqueness clause: text | rule 5; BC-SKL-05038 carries BC-REP-01, 04, 05 |
| BC-CON-05011 reconstruction from derivative graphs | figure | f from f prime: figure; vertical shift ambiguity: interactive, one slider for the added constant with the question "which features stay fixed?" | rule 3 on BC-REP-02 in BC-SKL-05040 to 05044, promoted by BC-QA-05009 dv "whether a known value is supplied to fix the sketch" |
| BC-CON-05012 f, f prime, f double prime together | figure | three stacked graphs with one point sliding along x, the signs of f prime and f double prime read off: interactive; combined sign table and tabulated derivative values: table | rule 3 on BC-REP-02 in BC-SKL-05045, promoted by BC-QA-05009 dv "whether three objects are in play rather than two"; rule 4 on BC-REP-03 in BC-SKL-05047, 05048 |
| BC-CON-05013 optimisation model | text | objective and constraint from a diagram: figure (static, labels inside); domain from context: text | rule 3 on BC-REP-08 in BC-SKL-05049; not promoted, because BC-QA-05011 dv are yes or no features |
| BC-CON-05014 interpretation | text | value, units, input: text | rule 5; BC-SKL-05054 to 05057 carry BC-REP-01, 04, 05 only |
| BC-CON-05015 implicit relation | text | horizontal and vertical tangent points on the curve: figure; second derivative by substitution: text | rule 3 on BC-REP-02 in BC-SKL-05060, 05063; BC-QA-05012 has no varying quantity in its dv; rule 5 for BC-SKL-05061, 05062 |

Where each mode fits:

- Interactive: BC-CON-05004, 05005, 05007, 05008, 05011, 05012. Each is a reading the stem tests of a relationship along x (sign of f prime against f rising, f prime rising against concavity, a sign chart built from a graph of f prime), which is the interactive row of TEMPLATE.md's mode table. One control per screen, keyboard-operable, with a static fallback of the same figure at three marked positions [inferred].
- Static figure is enough: BC-CON-05002, 05003, 05006, 05013, 05015, where the figure shows a fixed feature (a break, a cusp, a candidate list, a geometric diagram, tangent points) and no archetype names a varying quantity.
- Text and step_reveal only: BC-CON-05009, 05010, 05014, and the theorem statements of 05001.
- Motion: none. No key idea in the unit describes a limit or refining process (rule 2).
- Model: none selected by the numbered rules. The mode table lists every productive-failure target (BC-DF-13 and 15 archetypes) as a model case, and BC-DF-13 is on BC-QA-05003, 05009 and 05011; whether any Unit 5 concept is among the five conceptual targets in 01 is [inferred], settled by that list.

## 7. Sources

Library ids: BC-CON-05001 to BC-CON-05015; BC-SKL-05001 to BC-SKL-05063; BC-QA-05001 to BC-QA-05014; BC-PT-99004, 99005, 99010, 99011, 99012, 99013, 99014, 99017, 99021, 99060, 99061, 99062, 99063; BC-ERR-99001, 99004, 99005, 99008, 99019, 99021, 99023, 99027, BC-ERR-05013, 05016, 05018, 05024, 05026, 05057, 05058, 05059, 05060; BC-MIS-05001, 05004, 05007, 05008, 05011, 05013, 05015, 05018, 05020, 05031; BC-PRQ-05001 to 05008, BC-PRQ-06005; BC-DF-01, 02, 03, 04, 05, 06, 07, 08, 09, 11, 12, 13, 14, 17; BC-REP-01 to 09; outside parents BC-CON-01014, 02008, 02009, 02010, 02013, 03004, 03005, 03009, 04002, 04007, BC-TOP-0102, 0205, 0301.

Official examples: BC-FRQ-2013-Q3-B, 2013-Q4-A, 2013-Q4-B, 2013-Q4-C, 2014-Q3-B, 2015-Q4-C, 2015-Q5-B, 2015-Q5-C, 2018-Q3-C, 2018-Q3-D, 2018-Q4-B, 2021-Q3-B, 2021-Q4-D, 2022-Q3-B, 2022-Q3-C, 2022-Q3-D, 2023-Q1-B, 2023-Q4-A, 2023-Q4-B, 2023-Q4-D, 2024-Q1-D, 2024-Q3-B, 2025-Q1-D, 2025-Q4-B, 2025-Q4-D, 2026-Q2-C, 2026-Q4-B, 2026-Q4-C, 2026-Q4-D; BC-MCQ-CED-013, CED-014, SAMPLE-011, SAMPLE-012, SAMPLE-014, PE2012-029, 030, 033, 034, 037, 041, 045.

Pages: ced:99, ced:100, ced:110, ced:119, ced:122; sg-21:17; sg-22:5, sg-22:11, sg-22:12, sg-22:14; sg-23:3, sg-23:13, sg-23:14, sg-23:15; sg-24:10, sg-24:13; sg-25:4, sg-25:5, sg-25:9, sg-25:11, sg-25:12, sg-25:16, sg-25:17, sg-25:19, sg-25:21; sg-26:2, sg-26:5, sg-26:8, sg-26:12, sg-26:15, sg-26:16, sg-26:17; cr-22:4, cr-22:11, cr-22:14, cr-22:18; cr-23:4, cr-23:16; cr-24:11; crabbc-25:4, crabbc-25:12, crabbc-25:14, crabbc-25:15, crabbc-25:16, crabbc-25:17, crabbc-25:18, crabbc-25:28, crabbc-25:30.

Research headings:
- research/exam/exam-structure.md#Section and part layout
- research/exam/exam-structure.md#Free-response point totals
- research/scoring/justification-requirements.md#Justify, give a reason, and give reasons
- research/scoring/justification-requirements.md#Global versus local arguments
- research/scoring/justification-requirements.md#Sign analysis of a derivative
- research/scoring/justification-requirements.md#The candidates test
- research/scoring/justification-requirements.md#Theorem hypotheses
- research/scoring/justification-requirements.md#Reasons tied to the object the prompt names
- research/scoring/common-point-losses.md#Setup points, #Answer points, #Units points, #Interpretation points, #Justification points, #Notation points
- research/question-analysis/question-archetypes.md#Family absolute-extremum-candidates, #Family concavity-analysis, #Family evt-existence, #Family extremum-classification, #Family function-derivative-graph-relationship, #Family implicit-differentiation, #Family mean-value-theorem, #Family monotonicity-analysis, #Family optimisation, and #BC-QA-05014
- research/question-analysis/frq-analysis.md#How concepts combine inside one question
- research/units/unit-05-analytical-applications-differentiation.md, sections 5.1 to 5.12, subsections Representations and Assessment behaviour
- docs/plan/15-lessons.md#Methods, thought process and scoring habits; #Pacing to the exam date
- docs/lessons/TEMPLATE.md#Delivery

Inferred claims and what settles them:
- Every non-text delivery mode: the modality A/B in the build plan.
- One control per screen and three-position static fallback: TEMPLATE.md's [inferred] bound, same A/B.
- Model mode for BC-DF-13 concepts: the list of five productive-failure targets in 01.
- A decision lesson for the first derivative, second derivative and candidates tests: `adaptive.common_confusions` links among BC-SKL-05020, 05036, 05026 and a rerun of `--sets`.

Library gaps met:
- `point_types` empty on BC-QA-05002, 05009, 05010, 05011, 05012, 05013.
- `official_examples` empty on BC-QA-05002, 05010, 05011, 05012, 05013, 05014; BC-QA-05009 lists MCQ only.
- `confusable_with` is filled on 62 Unit 5 skills (tools/derive_confusable.py; plan 15 predates it); the one derived set is LSN-DEC-05-01.
- `calculator_status` null on every Unit 5 skill record (archetype status used instead).
- Hard edges whose parent looks unrelated to the child and may need review [inferred]: BC-SKL-04001 (units of a derivative) to BC-SKL-05012 and 05015; BC-SKL-02037 (product rule from a table or graph) to BC-SKL-05040.
- Families evt-existence, monotonicity-analysis, function-derivative-graph-relationship and optimisation are tagged [inferred] in research/question-analysis/question-archetypes.md.
