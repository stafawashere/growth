---
title: Unit 6 attack map, Integration and Accumulation of Change
research_date: 2026-09-29
status: draft
purpose: The map every designer of the 20 Unit 6 concept lessons reads first. It fixes the concept order along the prerequisite edges, the exam question types the unit feeds and the points they score, the cross-concept recognition features and the two confusable sets, the recurring traps, the time budgets per archetype shape, and the delivery mode per concept under the TEMPLATE selection rules, all computed from the library or cited to research and cached pages.
---

# Unit 6 attack map, Integration and Accumulation of Change

Scope: BC-UNIT-06, topics BC-TOP-0601 to BC-TOP-0614, CED pages ced:118 to ced:131 (research/units/unit-06-integration-accumulation.md#Unit 6, Integration and Accumulation of Change). Every count below was computed on 2026-09-29 from the content snapshot (`app.content.loader.load_snapshot`), `data/prereq_edges.csv`, `data/errors.json`, `data/misconceptions.json` and `tools/check_lessons.py --sets`. A claim with no library or research source is tagged [inferred] with what would settle it.

Two library facts shape the whole map.

- Plan 15 Q19 (docs/plan/15-lessons.md, Open-questions register) says BC-CON-06001 and BC-CON-06007 list skills whose own `concept` field names another concept. The git history of `data/skills.json` (commit 3a081db and earlier) shows which: BC-CON-06001 listed BC-SKL-06002 and BC-SKL-06003, whose `concept` is BC-CON-06002, and BC-CON-06007 listed BC-SKL-06021, whose `concept` is BC-CON-06008. Following the skill's back-reference, as Q19 rules, puts BC-SKL-06002 and BC-SKL-06003 in LSN-CON-06002 and BC-SKL-06021 in LSN-CON-06008. The current snapshot already agrees: `data/staging/corrections-skills-concept-lists.json` (merged in commit cff11f5) cut the lists to BC-CON-06001 = [BC-SKL-06001, BC-SKL-06004] and BC-CON-06007 = [BC-SKL-06017, BC-SKL-06020], and no Unit 6 concept list now names a skill whose back-reference differs. Q19 can be closed for Unit 6.
- BC-SKL-06046 (recognise an integrand with no closed-form antiderivative) is retired with `superseded_by` BC-SKL-06074 (BUILD-LEDGER.md, stage 15). Its `concept` field still names BC-CON-06014 and its edge to BC-SKL-06074 stays in `data/prereq_edges.csv`; no concept list holds it. Its content (BC-EK-FUN-6C3) is taught in LSN-CON-06020 through BC-SKL-06074.

## 1. Concept order along the prerequisite edges

Computed: a concept is a parent of another when a `hard_prerequisite` edge in `data/prereq_edges.csv` runs from one of its skills to one of the other's skills. Kahn's topological sort over those concept edges, ties broken by id, gives the order below. All 20 concepts are reached, so the concept graph has no cycle. "Hard parents" are Unit 6 concepts; "outside hard" are hard edges from other units or topic stand-ins; "BC-PRQ" are the supporting non-calculus parents (every BC-PRQ edge is `supporting`, [inferred] evidence tag on the edge). Every edge into a Unit 6 skill carries evidence tag inferred.

| # | Concept | Name | Skills (by `concept` back-reference) | Hard parents in Unit 6 | Outside hard parents | BC-PRQ parents |
|---|---|---|---|---|---|---|
| 1 | BC-CON-06001 | Accumulation of change as area under a rate graph | BC-SKL-06001, BC-SKL-06004 | none | BC-SKL-04001 | BC-PRQ-06005, BC-PRQ-06007 |
| 2 | BC-CON-06002 | Sign and units of accumulated change | BC-SKL-06002, BC-SKL-06003 | none | BC-SKL-04001 | BC-PRQ-06005 |
| 3 | BC-CON-06003 | Riemann sum approximation of a definite integral | BC-SKL-06005, 06006, 06007, 06008, 06009 | BC-CON-06001 | none | BC-PRQ-06005, BC-PRQ-06007, BC-PRQ-06012 |
| 4 | BC-CON-06004 | Over and under estimate reasoning for approximations | BC-SKL-06010, 06011 | BC-CON-06003 | none | BC-PRQ-06008 |
| 5 | BC-CON-06005 | Summation notation and the Riemann sum as a sum of products | BC-SKL-06012, 06013 | BC-CON-06003 | none | BC-PRQ-06006 |
| 6 | BC-CON-06006 | Definite integral as the limit of Riemann sums | BC-SKL-06014, 06015, 06016 | BC-CON-06003, BC-CON-06005 | BC-SKL-01006, BC-TOP-0102 | BC-PRQ-06006 |
| 7 | BC-CON-06010 | Definite integral evaluated by geometry | BC-SKL-06028 | BC-CON-06001 | none | BC-PRQ-06007 |
| 8 | BC-CON-06007 | Accumulation function defined by a definite integral | BC-SKL-06017, 06020 | BC-CON-06005, BC-CON-06010 | none | BC-PRQ-06005, BC-PRQ-06007, BC-PRQ-06013 |
| 9 | BC-CON-06008 | Fundamental Theorem of Calculus part one | BC-SKL-06018, 06019, 06021 | BC-CON-06001, BC-CON-06007 | BC-SKL-01046, BC-SKL-03002 | BC-PRQ-06005, BC-PRQ-06013 |
| 10 | BC-CON-06009 | Behaviour of an accumulation function read from the integrand | BC-SKL-06022 to 06027 | BC-CON-06007, BC-CON-06008 | none (supporting: BC-SKL-05020, BC-SKL-05021, BC-SKL-05029, BC-TOP-0506) | BC-PRQ-06007 |
| 11 | BC-CON-06011 | Algebraic properties of the definite integral | BC-SKL-06029 to 06033 | BC-CON-06005 | none (supporting: BC-TOP-0115) | none |
| 12 | BC-CON-06014 | Antiderivative and indefinite integral | BC-SKL-06040 to 06045 | none | BC-SKL-02027, BC-SKL-02032, BC-SKL-02035, BC-SKL-03002 | BC-PRQ-06002, BC-PRQ-06003, BC-PRQ-06004 |
| 13 | BC-CON-06012 | Fundamental Theorem of Calculus part two and net change | BC-SKL-06034, 06035, 06036, 06037, 06039 | BC-CON-06001, BC-CON-06008, BC-CON-06010, BC-CON-06014 | none (supporting: BC-TOP-0115) | BC-PRQ-06002, BC-PRQ-06005 |
| 14 | BC-CON-06013 | Average value of a function | BC-SKL-06038 | BC-CON-06012 | none | none |
| 15 | BC-CON-06015 | Substitution of variables | BC-SKL-06047 to 06052 | none | BC-SKL-03002 | BC-PRQ-06001, BC-PRQ-06003 |
| 16 | BC-CON-06016 | Rearrangement into an equivalent integrable form | BC-SKL-06053 to 06056 | BC-CON-06014, BC-CON-06015 | none | BC-PRQ-06001, BC-PRQ-06002, BC-PRQ-06009, BC-PRQ-06010 |
| 17 | BC-CON-06017 | Integration by parts | BC-SKL-06057 to 06061 | BC-CON-06012, BC-CON-06014 | BC-TOP-0208 | BC-PRQ-06005 |
| 18 | BC-CON-06018 | Linear partial fraction decomposition | BC-SKL-06062 to 06065 | BC-CON-06012, BC-CON-06015 | none | BC-PRQ-06003, BC-PRQ-06011 |
| 19 | BC-CON-06019 | Improper integral and convergence | BC-SKL-06066 to 06070 | BC-CON-06011, BC-CON-06012 | BC-SKL-01054, BC-TOP-0102 | none |
| 20 | BC-CON-06020 | Selecting an antidifferentiation technique | BC-SKL-06071 to 06074 | BC-CON-06015, BC-CON-06016, BC-CON-06017, BC-CON-06018, BC-CON-06019 | BC-SKL-06046 (retired, see above) | BC-PRQ-06001 |

Order notes. BC-CON-06010 precedes BC-CON-06007 because BC-SKL-06028 is a hard parent of BC-SKL-06020, so a designer of LSN-CON-06007 may assume signed area by geometry. BC-CON-06014 sits after the whole accumulation strand only because its id is larger; it has no Unit 6 hard parent and could be reached first by a student with Units 2 and 3 placed. The chain to the technique set is BC-CON-06014 or BC-CON-06015, then BC-CON-06016 to 06019, then BC-CON-06020, which is last because BC-SKL-06071 has hard parents in five concepts.

Plan 15 (docs/plan/15-lessons.md, What a lesson is, and its granularity) records BC-CON-06014 as loaded by no active archetype. The current snapshot has BC-QA-06008, 06009, 06011, 06016, 06018 and 06019 loading its skills (BC-QA-06018 and BC-QA-06019 with a BC-CON-06014 skill first), so LSN-CON-06014 is now insertable. The plan table is stale on this row.

## 2. Exam question types the unit feeds

Budgets from (research/exam/exam-structure.md#Section and part layout): Section I Part A (29 questions, 62 minutes, no calculator) 2.14 minutes per question; Part B (13 questions, 38 minutes, calculator) 2.92; Section II (Part A 2 questions in 30 minutes, calculator; Part B 4 in 60, no calculator) 15.0 per question, 9 points each (research/exam/exam-structure.md#Free-response point totals). Every archetype below records `multipart_structure` "one part of a multipart free response question, or a single multiple choice item" unless stated, so each has both shapes. The FRQ slot facts are from (research/question-analysis/frq-analysis.md#The calculator questions and the no-calculator questions): Q1 is the contextual calculator slot (recovering an accumulated amount from a rate, an average value, an extremum of an accumulation), Q3 to Q6 are no calculator. BC-QA-06007 is retired and superseded by BC-QA-08001, which still loads BC-SKL-06038.

The table lists every active archetype whose `skills` meets a Unit 6 skill, grouped by `family`.

| Family | Archetype | Calculator | MCQ part | FRQ part | Point types | Official BC-FRQ examples |
|---|---|---|---|---|---|---|
| integral-approximation | BC-QA-06001 Riemann sum from a table with over or under estimate reasoning | calculator | I-B | II-A | BC-PT-99018, 99019, 99022, 99026, 99007 | BC-FRQ-2021-Q1-B, 2021-Q1-C, 2022-Q4-C, 2015-Q3-B, 2023-Q1-A, 2024-Q1-B, 2026-Q1-B |
| integral-approximation | BC-QA-06002 Trapezoidal approximation of an accumulated amount from a table | no_calculator | I-A | II-B | BC-PT-99033, 99018, 99019 | BC-FRQ-2014-Q4-C, 2025-Q3-C, 2018-Q4-C |
| integral-approximation | BC-QA-06017 Riemann or trapezoidal sum with equal subintervals, formula or graph | no_calculator | I-A | II-B (two points) | BC-PT-99018, 99019 | none |
| accumulation-function-analysis | BC-QA-06003 Accumulation function analysed from the graph of the integrand | no_calculator | I-A | II-B | BC-PT-99024, 99013, 99011, 99062, 99069 | BC-FRQ-2019-Q3-C, 2021-Q4-A, 2014-Q3-A, 2024-Q4-B, 2018-Q3-A |
| definite-integral-from-graph | BC-QA-06004 Definite integral evaluated from a graph by geometry | no_calculator | I-A | II-B | BC-PT-99069 | BC-FRQ-2024-Q4-A, 2025-Q4-C, 2018-Q3-B |
| accumulation-with-initial-condition | BC-QA-06005 Net change from a rate with an initial condition | either | I-A or I-B | II-A or II-B | BC-PT-99001, 99004, 99069, 99002, 99033, 99003 | BC-FRQ-2019-Q1-A, 2013-Q1-B, 2022-Q3-A, 2015-Q1-A, 2024-Q1-C, 2025-Q3-D, 2026-Q1-C, 2018-Q1-A, 2018-Q2-B |
| rate-in-rate-out | BC-QA-06006 Rate in minus rate out accumulation | calculator | I-B | II-A | BC-PT-99001, 99068 | BC-FRQ-2015-Q1-D, 2018-Q1-B |
| accumulation-total-from-rate | BC-QA-99008 Total amount from a rate with no initial condition and no rate out | calculator | I-B | II-A (opening part, two points) | BC-PT-99001, 99002, 99004 | BC-FRQ-2013-Q1-B, 2015-Q1-A, 2018-Q1-A |
| accumulation-of-density | BC-QA-99009 Density accumulated over a spatial interval | calculator | I-B | II-A | none | BC-FRQ-2018-Q2-B |
| integral-comparison-bound | BC-QA-99010 Accumulation bounded by a comparison function | calculator | I-B | II-A | none | BC-FRQ-2018-Q2-C |
| accumulation-interpretation | BC-QA-06015 Interpreting a definite integral in context with units | either | I-A or I-B | II-A or II-B | none | none |
| average-value | BC-QA-08001 Average value of a function over an interval | calculator | I-B | II-A | BC-PT-99001, 99004, 99020, 99003 | BC-FRQ-2015-Q3-D, 2019-Q1-B, 2019-Q2-B, 2021-Q1-D, 2022-Q1-B |
| ftc-differentiation | BC-QA-06012 Differentiating an accumulation function with a variable upper limit | no_calculator | I-A | II-B | BC-PT-99024, 99004 | BC-FRQ-2024-Q4-C, 2024-Q5-A, 2025-Q4-A |
| integral-properties | BC-QA-06013 Manipulating definite integrals with their properties | no_calculator | I-A | II-B | BC-PT-99005, 99069, 99004 | BC-FRQ-2019-Q3-A, 2019-Q3-B, 2018-Q2-C |
| riemann-limit-to-integral | BC-QA-06014 Converting between a limit of Riemann sums and a definite integral | no_calculator | I-A | none recorded | none | none (MCQ only: BC-MCQ-CED-006, BC-MCQ-SAMPLE-008) |
| antidifferentiation-technique | BC-QA-06008 Antiderivative or definite integral by substitution | no_calculator | I-A | II-B | BC-PT-99002, 99003, 99004 | BC-FRQ-2021-Q3-A, 2026-Q5-A |
| antidifferentiation-technique | BC-QA-06009 Antiderivative by integration by parts | no_calculator | I-A | II-B | BC-PT-99056, 99057, 99004 | BC-FRQ-2023-Q5-C, 2024-Q5-D |
| antidifferentiation-technique | BC-QA-06010 Antiderivative by linear partial fractions | no_calculator | I-A | II-B | BC-PT-99005, 99003, 99004, 99081 | BC-FRQ-2019-Q5-B, 2015-Q5-D |
| antidifferentiation-technique | BC-QA-06018 Inverse trigonometric form, directly or after completing the square | no_calculator | I-A | none (single MCQ or short answer) | none | none |
| antidifferentiation-technique | BC-QA-06019 Antiderivative after splitting or expanding, confirmed by differentiating | no_calculator | I-A | none (single MCQ or short answer) | none | none |
| improper-integral | BC-QA-06011 Improper integral convergence or divergence | no_calculator | I-A | II-B | BC-PT-99053, 99003, 99005, 99004 | BC-FRQ-2019-Q5-C, 2023-Q5-B, 2026-Q5-D |
| procedure-selection | BC-QA-06016 Selecting an antidifferentiation technique from the form of the integrand | no_calculator | I-A | II-B (scored as the applied technique) | none | none |

### The accumulation free-response parts and the points they score

The three accumulation part shapes the unit feeds, and what each point is for, from the archetype `scoring_pattern` and the BC-PT `earns` and `does_not_earn` fields:

- Riemann or trapezoidal sum from a table (BC-QA-06001, BC-QA-06002, BC-QA-06017). Setup point BC-PT-99018, form of the sum: every term shows a value factor and a width factor, at least five of six factors right for three subintervals (sg-25:13, sg-23:2). Answer point BC-PT-99019: the value with the products present; a bare value earns neither point (sg-23:3). A fully correct sum with the wrong endpoint earns one of the two (BC-QA-06001, sg-23:2); a correct left or right sum where a trapezoidal sum was asked earns the form point only, and the average of a correct left and right sum earns both (BC-QA-06002, sg-25:13). Interpretation point BC-PT-99007 when the same part asks what the integral means: quantity, units and interval together (sg-23:2). Readers read an equals sign as an approximation sign for the form point (research/scoring/notation-requirements.md#The equal sign, sg-25:13).
- Net change with an initial condition (BC-QA-06005, BC-QA-06006). Setup point BC-PT-99001, the definite integral with limits matching the requested interval, with or without the differential; initial condition point BC-PT-99033, the known value added to the integral; answer point BC-PT-99004. Presenting only the integral value without the initial amount does not earn BC-PT-99033 (sg-24:3, sg-24:4). With no initial condition the points fall to the integrand (BC-PT-99002), the antiderivative (BC-PT-99003) and the value, and the answer point requires the antiderivative point (sg-25:14). BC-QA-99008 is the two-point opening shape: integral or integrand, then value; the stated initial amount and second rate belong to later parts (samples-13-q1:1, samples-15-q1:1). Units: no BC-PT among these carries `units_required` yes; units are read where the prompt asks for them (research/scoring/common-point-losses.md#Units points) and are not read where it does not (research/scoring/notation-requirements.md#What notation never costs).
- Accumulation function from a graph (BC-QA-06003, BC-QA-06004, BC-QA-06012). Value point BC-PT-99069: g at the input from signed areas, correct sign for reversed limits (sg-25:18, sg-24:12). Derivative point BC-PT-99024: the derivative written as the integrand at the variable (sg-25:16); differencing the integrand at the two limits earns the answer point but not this one. Answer and reason points are separate, the reason tied to the graph of f (sg-25:17); an absolute extremum needs the candidates argument BC-PT-99011 at every critical input and both endpoints (sg-25:19). Any extra declared inflection input costs both points of that part (sg-25:17).

The technique parts score setup and antiderivative separately: integration by parts BC-PT-99056 (u and dv), BC-PT-99057 (uv minus the integral of v du), answer only after both (sg-23:18, sg-24:18); improper integrals BC-PT-99053 for limit notation throughout with no arithmetic with infinity (sg-23:17), then antiderivative and value; substitution loses the answer point when the original limits are applied to an expression in u (sg-23:16, sg-23:17).

## 3. Cross-concept patterns

### Which concepts the stems combine

Computed from the archetypes' `skills` mapped to concepts:

- BC-CON-06012 is loaded by 11 archetypes, more than any other Unit 6 concept: every accumulation and technique shape that ends in a definite integral value reaches BC-SKL-06034 or BC-SKL-06036.
- BC-QA-06001 joins BC-CON-06003, BC-CON-06004 and BC-CON-06012 (sum, error direction, net change); BC-QA-06002 the same three.
- BC-QA-06003 joins BC-CON-06007, BC-CON-06008 and BC-CON-06009 (value of g, g prime, features of g); BC-QA-06004 joins BC-CON-06001, BC-CON-06007 and BC-CON-06010.
- BC-QA-06015 joins BC-CON-06001, BC-CON-06002 and BC-CON-06013 (interpretation, units, average value).
- BC-QA-06008, 06009 and 06011 each join their technique concept with BC-CON-06012 and BC-CON-06014 (the final evaluation and the basic antiderivative).
- BC-QA-06016 joins BC-CON-06014, BC-CON-06016 and BC-CON-06020.
- Across units, BC-UNIT-06 with BC-UNIT-08 is the dominant pairing in the FRQ corpus, and BC-UNIT-05 with BC-UNIT-06 the next, because an extremum of an accumulated quantity needs the candidates argument (research/question-analysis/frq-analysis.md#How concepts combine inside one question).

### Recognition features between neighbouring concepts, and the first written line

| Neighbours | What in the stem selects each | First written line | Source |
|---|---|---|---|
| Left, right, midpoint, trapezoidal sums (BC-CON-06003) | The stem names the sum; left, right and midpoint differ only in the sample point, the trapezoid averages the two endpoint values. The table's inputs fix the widths, which may be unequal. | The subintervals with their widths, then one product per subinterval (BC-QA-06001 `expected_solution_path`); for a trapezoid, each term as average of endpoint values times width (BC-QA-06002) | research/units/unit-06-integration-accumulation.md#6.2 Approximating Areas with Riemann Sums; BC-ERR-06001, BC-ERR-06002 |
| Error direction by monotonicity against by concavity (BC-CON-06004) | Left or right sum: the stem supplies increasing or decreasing. Trapezoidal or midpoint sum: the argument is concavity. | The property named on the given function, then the direction | BC-SKL-06010, BC-SKL-06011; BC-ERR-06007; (research/scoring/common-point-losses.md#Justification points) (BC-ERR-99020) |
| Net change against amount (BC-CON-06012) | "Find the value of the quantity at the later time" with a known value at one time selects the amount: known value plus the integral. "How much accumulated" or "total amount" with no initial condition selects the integral alone. | \(A(b)=A(a)+\int_a^b r(t)\,dt\) (BC-QA-06005); \(\int_a^b r(t)\,dt\) (BC-QA-99008) | BC-QA-06005 `wrong_approaches` (reporting the net change as the amount); BC-QA-99008 `wrong_approaches` (treating the part as a net change question because the stem gives an initial condition) |
| Rate in against rate in minus rate out (BC-CON-06012) | Two rates, one increasing and one decreasing the quantity | The net rate as inflow minus outflow inside one integral, with parentheses around the outflow | BC-QA-06006 |
| Amount against average value (BC-CON-06012, BC-CON-06013) | "Average value" or a factor \(\frac{1}{b-a}\) in the displayed expression | \(\frac{1}{b-a}\int_a^b f(x)\,dx\) (BC-QA-08001) | BC-QA-06015 `difficulty_variables`; BC-ERR-06016, BC-ERR-06030 |
| FTC part one against part two (BC-CON-06008, BC-CON-06012) | A variable in a limit and a request for a derivative selects part one; numerical limits and a request for a value selects part two | Part one: \(g'(x)=f(x)\) stated (BC-QA-06012). Part two: an antiderivative, then \(F(b)-F(a)\) (BC-SKL-06034) | research/units/unit-06-integration-accumulation.md#6.4 The Fundamental Theorem of Calculus and Accumulation Functions; research/units/unit-06-integration-accumulation.md#6.7 The Fundamental Theorem of Calculus and Definite Integrals |
| Upper limit \(x\) against a composite upper limit (BC-CON-06008) | The upper limit is a function of \(x\) | \(\frac{d}{dx}\int_a^{u(x)} f(t)\,dt=f(u(x))\,u'(x)\) | BC-QA-06012 `difficulty_variables`; BC-ERR-06027 |
| Graph of f against graph of g (BC-CON-06007, BC-CON-06009) | The plotted curve is the integrand; features of g are read from the sign and slope of f | g at the inputs as signed areas, then \(g'=f\) (BC-QA-06003) | BC-ERR-06008, BC-ERR-06009 |
| Substitution, parts, partial fractions, rearrangement (BC-CON-06015 to 06018, BC-CON-06020) | A composite with its inner derivative present selects substitution; a product of unlike factors selects parts; numerator degree at least the denominator degree selects long division; a factorable nonrepeating linear denominator selects partial fractions | Substitution: \(u=\), \(du=\) (BC-QA-06008). Parts: \(u=\), \(dv=\), \(du=\), \(v=\) (BC-QA-06009). Partial fractions: the factored denominator (BC-QA-06010). Rearrangement: the divided or completed-square form | research/units/unit-06-integration-accumulation.md#6.14 Selecting Techniques for Antidifferentiation |
| Definite against improper integral (BC-CON-06012, BC-CON-06019) | An infinite limit, or an integrand unbounded in the interval | \(\lim_{b\to\infty}\int_a^b f(x)\,dx\), the offending limit replaced by a variable (BC-QA-06011) | BC-EK-LIM-6A1; research/scoring/notation-requirements.md#Limit notation |
| Limit of sums against definite integral (BC-CON-06005, BC-CON-06006) | A sigma expression inside a limit | The general term split into a value and a width (BC-QA-06014) | BC-EK-LIM-5C2 |

### The two confusable sets

`tools/check_lessons.py --sets` prints ten sets; two are in Unit 6.

- LSN-DEC-06-01: BC-SKL-06017 (write an accumulation function as a definite integral with a variable upper limit) against BC-SKL-06019 (differentiate an accumulation function whose upper limit is a function of \(x\)). Designed in docs/lessons/decisions/LSN-DEC-06-01.md. Selecting feature: the task verb. "Write \(F(x)\)" selects the integral with the starting input in the lower limit and \(x\) alone in the upper limit; "find \(F'(x)\)" selects the integrand at the upper limit times the derivative of that limit. Archetype BC-QA-06012. Errors the wrong method produces: BC-ERR-06027, BC-ERR-06028, BC-ERR-99032. It spans LSN-CON-06007 and LSN-CON-06008, so it is served no earlier than the first item loading the second member after the first is reached (docs/plan/15-lessons.md, Decision lessons for confusable sets).
- LSN-DEC-06-02: BC-SKL-06044 (include the constant of integration and determine it from an initial condition) against BC-SKL-06045 (verify a proposed antiderivative by differentiating it). Both are in BC-CON-06014; both `adaptive.common_confusions` name BC-MIS-06018 (an antiderivative is a single function). Archetypes: BC-SKL-06044 on BC-QA-06009 and BC-QA-06016, BC-SKL-06045 on BC-QA-06016 and BC-QA-06019. Selecting feature [inferred, from the two `adaptive.mastered_if` texts]: a stem that supplies a value of the antiderivative at a point selects solving for \(C\); a stem that supplies a candidate function selects differentiating it and comparing term by term with the integrand, accepting a candidate that differs by a constant. Settled by the LSN-DEC-06-02 design fixing `selecting_feature` over two parameter draws on one archetype. Its errors: BC-ERR-07026 (constant of integration omitted; BC-ERR-06021 is retired) and BC-ERR-06033 (power rule with the wrong divisor).

Technique selection. Plan 15 names BC-QA-06016 as the archetype for the antiderivative technique drill (docs/plan/15-lessons.md, Decision lessons for confusable sets). The derived sets do not hold a technique set for Unit 6: the technique skills (BC-SKL-06047, 06048, 06050, 06051, 06056, 06057, 06058, 06071, 06072) reference one another through `adaptive.common_confusions` and do not appear among the printed sets [inferred: the component likely exceeds `DECISION_SET_MAX` (6); settled by printing the component sizes from `app/lessons/confusable.py`]. The technique contrast is therefore taught inside LSN-CON-06020 from BC-QA-06016: `expected_solution_path` "inspect the integrand for structural markers", then "name the technique the markers select", then "rule out techniques whose preconditions fail"; `wrong_approaches` BC-ERR-06020, BC-ERR-06022, BC-ERR-06026. BC-QA-06016 lacks `point_types`, so LSN-CON-06020 says nothing about points (plan 15, R14).

## 4. Recurring traps

Computed: an active BC-ERR or BC-MIS whose `skills` meet the skills of two or more Unit 6 concepts. Scoring consequences are the record text.

| Record | Concepts | Scoring consequence (record) |
|---|---|---|
| BC-ERR-06022 Factors of a product antidifferentiated separately | 06016, 06017, 06018, 06020 | Neither the u and dv point nor the expression point is earned (sg-23:18, sg-24:18). |
| BC-ERR-06013 Semicircular region given the area of a full circle | 06001, 06007, 06010 | The value point for that integral is lost. |
| BC-ERR-06014 Regions below the axis added as positive area | 06001, 06007, 06010 | The value point is lost, and any later part that imports the value inherits the error. |
| BC-ERR-06019 Constant factor from the differential dropped | 06015, 06018, 06019 | The antiderivative point is lost and the value point with it. |
| BC-ERR-99012 Fundamental Theorem of Calculus misapplied to an accumulation function | 06007, 06011, 06012 | The value or setup point in that part is not earned, and the error usually propagates to later parts that build on the value. |
| BC-ERR-99032 Definite integral expression written in malformed notation | 06006, 06007, 06011 | The expression point is not earned, since the requested object is an integral expression and nothing else is being scored in that part. |
| BC-ERR-06003 Riemann sum reported as a sum of function values | 06003, 06005 | Neither the form point nor the answer point is earned because no products appear. |
| BC-ERR-99028 Riemann or trapezoidal sum setup insufficient or malformed | 06003, 06006 | The setup point requires the sum of the appropriate products to be visible; the answer point follows it. |
| BC-ERR-06018 Original limits of integration kept after a substitution | 06015, 06019 | Not eligible for the answer point even when the numerical value is correct (sg-23:17, sg-23:16). |
| BC-ERR-06020 Substitution attempted when the inner derivative is absent | 06015, 06020 | The setup point for the technique is not earned and the work does not lead to the antiderivative. |
| BC-ERR-06026 Improper rational integrand decomposed without a preliminary division | 06016, 06018 | The decomposition cannot be solved consistently and the antiderivative point is not earned. |
| BC-ERR-06028 Variable of integration substituted in place of the upper limit | 06007, 06008 | The answer point is not earned because the derivative is not expressed in the independent variable. |
| BC-ERR-06029 Interpretation of a definite integral omits the interval or the units | 06001, 06002 | The interpretation point requires both the quantity with units and the interval (sg-23:2). |
| BC-ERR-06030 Average value expression interpreted as a total | 06001, 06013 | The description must say average over the interval (sg-24:3). |
| BC-ERR-06032 Calculator left in degree mode for a trigonometric integrand | 06012, 06013 | The first point the value would earn is not earned; later points stay available (sg-23:4). |
| BC-ERR-06033 Power rule for antiderivatives applied with the wrong divisor | 06014, 06016 | The proposed function does not differentiate to the integrand, so an antiderivative point is not earned. |
| BC-ERR-07026 Constant of integration omitted | 06014, 06015 | At most the first two points are available; the guideline caps the response there. |
| BC-ERR-99034 Reported answer contradicts the response's own work | 06002, 06003 | The answer point is lost although the supporting work would have earned it. |

Misconceptions across two or more concepts (severity from the record): BC-MIS-08019 area formulas recalled without their constant factors (06001, 06007, 06010; medium); BC-MIS-08024 an integral over an interval measures an area (06002, 06007, 06010; high); BC-MIS-05020 concavity and monotonicity are the same property (06004, 06009; high); BC-MIS-06003 Riemann sums are exact (06003, 06004; medium); BC-MIS-06014 average value and accumulated amount are the same quantity (06001, 06013; high); BC-MIS-06017 a composite integrand guarantees that substitution applies (06015, 06020; high); BC-MIS-06022 technique choice follows the surface look of the integrand (06016, 06020; high); BC-MIS-06024 the variable of integration is the independent variable (06007, 06008; medium); BC-MIS-06026 the Fundamental Theorem of Calculus part two needs no hypotheses (06011, 06012; medium); BC-MIS-08009 an interpretation is complete once the quantity is named (06001, 06002; medium). A lesson names these only as the possible-reason line of the error block they are linked to (TEMPLATE, Traps).

Point losses research/scoring names for this unit's shapes:

- (research/scoring/common-point-losses.md#Setup points): bare values instead of products, the wrong sum type or a uniform width on unequal data (BC-ERR-99028; cr-23:4, cr-24:4); no calculator setup before a numerical answer (BC-ERR-99021; cr-23:7, cr-24:4); differential omitted leaving the expression ambiguous (BC-ERR-99006; cr-23:28, cr-24:27); average value setup replaced by a difference quotient (BC-ERR-99015; cr-23:4).
- (research/scoring/common-point-losses.md#Answer points): accumulation function evaluated without the value at the lower limit or with the sign of reversed limits ignored (BC-ERR-99012; cr-23:20, cr-24:14); integration by parts with the wrong sign or pieces (BC-ERR-99025; cr-23:32, cr-24:32); fewer than three decimal places (BC-ERR-99019); unrequired simplification that introduces an error (BC-ERR-99022; cr-24:19).
- (research/scoring/common-point-losses.md#Units points): units missing where asked (BC-ERR-99005; cr-23:7).
- (research/scoring/common-point-losses.md#Interpretation points): interval omitted, key phrases absent from an average value interpretation (BC-ERR-99027; cr-24:3).
- (research/scoring/common-point-losses.md#Justification points): local sign change where a global argument was required (BC-ERR-99004; cr-23:16); reasoning not tied to the given graph (BC-ERR-99023; cr-23:16); over or underestimate without concavity (BC-ERR-99020; cr-23:11, cr-23:12).
- (research/scoring/common-point-losses.md#Notation points): limit notation dropped or arithmetic with infinity (BC-ERR-99007; cr-23:16, cr-23:31); a variable expression equated to a number (BC-ERR-99002; cr-23:19).
- (research/scoring/notation-requirements.md#Simplification): simplification is optional, an attempted one must be correct (sg-23:16). (research/scoring/notation-requirements.md#The differential is normally optional): a bare missing differential is forgiven, but with an initial condition on the wrong side it changes which points remain (sg-23:8).

The four highest severity clusters the unit research ties to scoring guidelines: features of g read off the plotted integrand (sg-25:17), a local argument for a global extremum (sg-25:19), the integral of a rate treated as the amount (sg-24:4), and a substitution that leaves the limits untouched (sg-23:16, sg-23:17) (research/units/unit-06-integration-accumulation.md#Misconception summary). Several concept records still list retired BC-MIS ids; see Library gaps.

## 5. Time budgets per archetype shape

MCQ budgets are the part figures. An FRQ part's budget is its share of the 15.0 minutes by points out of 9, per plan 15 (docs/plan/15-lessons.md, Fluency, measured and never credited); the point counts come from `scoring_pattern`. "Writes" names the steps that carry a point; "held" names steps with no point of their own. Which steps a fluent solver holds in the head is [inferred] from where the points sit; settled by timing data per step once 10's fluency telemetry exists.

| Shape | MCQ budget | FRQ points and budget | A fluent solver writes | Held |
|---|---|---|---|---|
| BC-QA-06001 Riemann sum from a table | I-B 2.92 | 2 (form, value) = 3.33; with interpretation 3 = 5.0 | every product with its width, the total; the interpretation sentence with quantity, units, interval | reading the widths off the table |
| BC-QA-06002 trapezoidal sum | I-A 2.14 | 2 = 3.33 | each term as average of two values times width, the value | the arithmetic of the average |
| BC-QA-06017 sum on equal subintervals | I-A 2.14 | 2 = 3.33 | the width, the sum of products, the value | the list of sample points |
| BC-QA-06003 accumulation from a graph | I-A 2.14 | 2 per part (answer, reason) = 3.33 per part | the signed-area value; \(g'=f\) at the input; each answer with a reason naming f | the region areas when a single piece |
| BC-QA-06004 integral by geometry | I-A 2.14 | 1 = 1.67 | the labelled value | the partition and each area formula |
| BC-QA-06012 FTC part one | I-A 2.14 | 2 (theorem, value) = 3.33 | the derivative written as the integrand at the limit, times the limit's derivative; the value | nothing further |
| BC-QA-06005 net change with initial condition | I-A or I-B | 3 (integral, initial condition, answer) = 5.0 | \(A(b)=A(a)+\int_a^b r\), the value with units | the calculator evaluation |
| BC-QA-06006 rate in minus rate out | I-B 2.92 | integral and initial amount as in BC-QA-06005 [inferred: 3 = 5.0; settled by a rubric for this exact shape] | one integral of inflow minus outflow, plus the initial amount | which rate is which |
| BC-QA-99008 total from a rate | I-B 2.92 | 2 = 3.33 | the integral, the value | the interval read from the wording |
| BC-QA-08001 average value | I-B 2.92 | 2 = 3.33 | the integral with the division, the value to three places | nothing |
| BC-QA-06015 interpretation | I-A or I-B | 1 = 1.67 | one sentence: quantity, units, interval | the units product |
| BC-QA-06008 substitution | I-A 2.14 | antiderivative and value points [point count not in `scoring_pattern`; inferred 3 = 5.0, settled by a rubric] | \(u\), \(du\), the integral in \(u\) with converted limits, the antiderivative, the value | the constant adjustment |
| BC-QA-06009 integration by parts | I-A 2.14 | 3 (u and dv, expression, answer) = 5.0 | \(u, dv, du, v\); \(uv-\int v\,du\); the answer | the remaining basic integral |
| BC-QA-06010 partial fractions | I-A 2.14 | 3 [inferred in the record] = 5.0 | the factored denominator, the constants, the logarithms | clearing denominators |
| BC-QA-06011 improper integral | I-A 2.14 | 3 (limit notation, antiderivative, value) = 5.0 | the limit of the integral carried on every line, the antiderivative, the value or divergence statement | nothing (limit notation is scored throughout) |
| BC-QA-06013 properties | I-A 2.14 | 1 per value [inferred] | the rewritten combination, the value | matching supplied integrals |
| BC-QA-06014 limit of sums | I-A 2.14 | none | the integral with limits | the width and sample point |
| BC-QA-06016, 06018, 06019 technique forms | I-A 2.14 | none recorded (06016 scored as the applied technique) | the first line of the chosen technique | the structural inspection |

## 6. Delivery map

TEMPLATE selection rules (docs/lessons/TEMPLATE.md, Delivery): 1 worked examples and error blocks are `step_reveal`; 2 a key idea describing a process is `motion`, with `model` on the example only where a computed sequence of values is the idea; 3 figure-bearing BC-REP (02, 07, 08, 12, 13, 14) gives `figure`, promoted to `interactive` when `common_givens` or `difficulty_variables` name a varying quantity and the stem asks for a reading; 4 BC-REP-03 givens give `table`; 5 everything else is `text`. The mode table also puts `model` on every productive-failure target. Rule 1 applies to every concept's examples and error blocks and is not repeated below. Every non-text choice is [inferred]; settled by the modality A/B in the build plan (skip rate and time to first credited success by mode).

| Concept | Orientation | Key ideas (BC-EK) and mode | Rule and triggering field |
|---|---|---|---|
| BC-CON-06001 | figure | CHA-4A1 figure (shaded region between a rate graph and the axis); CHA-4A2 figure; example: `model` | rule 3, `representations` BC-REP-02 on BC-SKL-06001 and 06004; `model` because BC-CON-06001 is Unit 6's productive-failure target (`PRODUCTIVE_FAILURE_TARGETS`, app/engine/constants.py) and BC-QA-06004 carries BC-DF-13 |
| BC-CON-06002 | text | CHA-4A3 figure (sign of rate against sign of area); CHA-4A4 text (units product) | rule 3, BC-REP-02 on BC-SKL-06003; rule 5 for BC-SKL-06002 (BC-REP-04, 05) |
| BC-CON-06003 | table | LIM-5A1 and LIM-5A2 table for the tabulated sums, one static figure of the four sample-point choices at one fixed \(n\) | rule 4, BC-REP-03 on BC-SKL-06005, 06006, 06008; rule 3, BC-REP-02 on BC-SKL-06007, 06009 |
| BC-CON-06004 | figure | LIM-5A4 figure (left and right rectangles on a monotone curve; trapezoid and midpoint on a concave curve) | rule 3, BC-REP-02 on BC-SKL-06010, 06011; not promoted, since BC-QA-06001's `difficulty_variables` name a property (monotone table), not a varying quantity |
| BC-CON-06005 | text | LIM-5B2 text | rule 5, BC-REP-01 only on BC-SKL-06012, 06013 |
| BC-CON-06006 | text | LIM-5C1 `motion` (rectangles refining under a curve as \(n\) grows, widths to 0); example: `model` (Riemann sums computed at growing \(n\), shown as a table beside the figure) | rule 2, the EK text "the limit of Riemann sums as the widths of the subintervals approach 0" (ced:120) is a process and the computed sequence is the idea |
| BC-CON-06010 | figure | FUN-6A1 figure (segments and semicircles, below-axis regions marked negative) | rule 3, BC-REP-02 on BC-SKL-06028; not promoted, since BC-QA-06004's `difficulty_variables` are presence flags |
| BC-CON-06007 | text | FUN-5A1 `motion` (the accumulation function traced as the upper limit moves); FUN-5A3 `interactive` (the upper limit dragged along a graph of the integrand with the signed area and the value of g shown; reading: sign of the change in g) | rule 2 for FUN-5A1 ("used to define new functions", a quantity accumulating); rule 3 promoted for BC-SKL-06020 (BC-REP-02), BC-QA-06003 `common_givens` "an accumulation function g with a fixed lower limit" and `difficulty_variables` "whether regions below the axis are involved", with the stem asking for values of g |
| BC-CON-06008 | text | FUN-5A2 figure (integrand graph with the height at the upper limit marked as \(g'(x)\)) | rule 3, BC-REP-02 on BC-SKL-06018; not promoted, since BC-QA-06012's `difficulty_variables` vary a form (limit \(x\) or a function of \(x\)), not a quantity |
| BC-CON-06009 | figure | FUN-5A3 `interactive` (one draggable input on the graph of f; the sign of f and the slope of f reported against g increasing and g concave up) | rule 3 promoted, BC-REP-02 on all six skills; BC-QA-06003 `difficulty_variables` "whether the question asks about g, g prime, or g double prime", stem asks for a reading of the relationship |
| BC-CON-06011 | text | FUN-6A2 table (supplied integral values over adjacent intervals); FUN-6A3 figure (jump discontinuity, integral split at the jump) | rule 4, BC-REP-03 on BC-SKL-06031; rule 3, BC-REP-02 on BC-SKL-06033 |
| BC-CON-06014 | text | FUN-6C1, FUN-6C2 text | rule 5, BC-REP-01 only |
| BC-CON-06012 | text | FUN-6B1 text; FUN-6B2 text; FUN-6B3 table (known value plus accumulated change) | rule 5 for BC-SKL-06034, 06035; rule 4, BC-REP-03 on BC-SKL-06037 |
| BC-CON-06013 | text | FUN-6B3 text | rule 5, BC-REP-01, 05, 09 on BC-SKL-06038 |
| BC-CON-06015 | text | FUN-6D1, FUN-6D2 text | rule 5, BC-REP-01 only |
| BC-CON-06016 | text | FUN-6D3 text | rule 5, BC-REP-01 only |
| BC-CON-06017 | text | FUN-6E1 text | rule 5, BC-REP-01, 04 |
| BC-CON-06018 | text | FUN-6F1 text | rule 5, BC-REP-01 only |
| BC-CON-06019 | text | LIM-6A1 figure (infinite interval and vertical asymptote); LIM-6A2 `motion` (the upper limit \(b\) moving outward with the accumulated area approaching a value or growing) | rule 3, BC-REP-02 on BC-QA-06011 `representations` and the topic's conversion "unbounded graph to a finite value statement"; rule 2, "determined using limits of definite integrals" is a limit being taken |
| BC-CON-06020 | text | FUN-6C2, FUN-6D3, FUN-6C3 text | rule 5, BC-REP-01 on BC-SKL-06071 to 06073; BC-REP-09 on BC-SKL-06074 is not figure-bearing |

Where each mode fits, in summary:

- Motion: rectangles refining under a curve as \(n\) grows (LSN-CON-06006); the accumulation function traced as the upper limit moves (LSN-CON-06007); the improper integral's upper limit moving outward (LSN-CON-06019). Every motion entry carries `reduced_motion` and a static fallback of three frames side by side (TEMPLATE, Delivery).
- Model: Riemann sums computed at growing \(n\) (LSN-CON-06006 example), and the productive-failure example of LSN-CON-06001.
- Interactive: the upper limit dragged along a graph of the integrand with the signed area shown (LSN-CON-06007, FUN-5A3), and one draggable input reading f's sign and slope against g (LSN-CON-06009). One control per screen [inferred, per TEMPLATE].
- Static figure or table is enough: the sample-point choices and tabulated sums (06003), error direction (06004), geometry (06010), the FTC part one height (06008), properties and discontinuities (06011), sign of accumulated change (06002).
- Text and step reveal only: the antidifferentiation techniques and their notation (06005, 06013, 06014, 06015, 06016, 06017, 06018, 06020). Their representations are BC-REP-01 alone, and the content is a sequence of written lines, which `step_reveal` carries.

## Library gaps met

- Concept `misconceptions` lists name retired BC-MIS ids: BC-CON-06001 (BC-MIS-06012, 06013, 06025), BC-CON-06002 (BC-MIS-06025), BC-CON-06004 (BC-MIS-06005, 06006), BC-CON-06007 and BC-CON-06009 (BC-MIS-06007), BC-CON-06009 (BC-MIS-06006, 06009), BC-CON-06010 (BC-MIS-06011, 06012), BC-CON-06012 (BC-MIS-06013), BC-CON-06013 (BC-MIS-06015), BC-CON-06019 (BC-MIS-06020). Their successors per data/ids.json are BC-MIS-08024, 08006, 08009, 07010, 05020, 05011, 01010, 08019, 99006, 99008. Designers take possible reasons from the BC-ERR record's `possible_misconceptions`, which are current.
- BC-CON-06018 lists no misconception.
- BC-QA-06014, 06015, 06016, 06018, 06019, 99009 and 99010 carry no `point_types`, so their lessons carry no scoring section (plan 15, R14). BC-QA-06015's scoring pattern names an interpretation point (sg-23:2) that BC-PT-99007 would fit.
- BC-QA-06010, 06013 and 06014 have no matching part in the 2023 to 2025 free-response questions read for the unit; their scoring patterns are inferred (research/units/unit-06-integration-accumulation.md#Unresolved).
- LSN-DEC-06-01 has no writing-side archetype (its own Sources note); LSN-DEC-06-02's selecting feature is inferred above.
- Plan 15's statement that BC-CON-06014 is loaded by no archetype and its Q19 are both stale against the current snapshot (section 1).

## 7. Sources

- Concepts: BC-CON-06001 to BC-CON-06020. Skills: BC-SKL-06001 to BC-SKL-06074 (BC-SKL-06046 retired, superseded by BC-SKL-06074). Outside parents: BC-SKL-01006, BC-SKL-01046, BC-SKL-01054, BC-SKL-02027, BC-SKL-02032, BC-SKL-02035, BC-SKL-03002, BC-SKL-03021, BC-SKL-04001, BC-SKL-05020, BC-SKL-05021, BC-SKL-05029, BC-TOP-0102, BC-TOP-0115, BC-TOP-0208, BC-TOP-0506.
- BC-PRQ-06001 to BC-PRQ-06013.
- Archetypes: BC-QA-06001, 06002, 06003, 06004, 06005, 06006, 06008, 06009, 06010, 06011, 06012, 06013, 06014, 06015, 06016, 06017, 06018, 06019, BC-QA-08001, BC-QA-99008, BC-QA-99009, BC-QA-99010; BC-QA-06007 retired, superseded by BC-QA-08001.
- Point types: BC-PT-99001, 99002, 99003, 99004, 99005, 99007, 99011, 99013, 99018, 99019, 99020, 99022, 99024, 99026, 99033, 99053, 99056, 99057, 99062, 99068, 99069, 99081.
- Errors: BC-ERR-06001, 06002, 06003, 06007, 06008, 06009, 06013, 06014, 06015, 06016, 06018, 06019, 06020, 06022, 06026, 06027, 06028, 06029, 06030, 06032, 06033, BC-ERR-07026, BC-ERR-99002, 99004, 99005, 99006, 99007, 99012, 99015, 99019, 99020, 99021, 99022, 99023, 99025, 99027, 99028, 99032, 99034.
- Misconceptions: BC-MIS-05020, BC-MIS-06003, 06014, 06017, 06018, 06022, 06024, 06026, BC-MIS-08009, 08019, 08024.
- Difficulty factors: BC-DF-13, BC-DF-15. Representations: BC-REP-01, 02, 03, 04, 05, 09.
- Essential knowledge: BC-EK-CHA-4A1 to 4A4, BC-EK-LIM-5A1 to 5A4, BC-EK-LIM-5B1, 5B2, 5C1, 5C2, BC-EK-FUN-5A1 to 5A3, BC-EK-FUN-6A1 to 6A3, BC-EK-FUN-6B1 to 6B3, BC-EK-FUN-6C1 to 6C3, BC-EK-FUN-6D1 to 6D3, BC-EK-FUN-6E1, BC-EK-FUN-6F1, BC-EK-LIM-6A1, 6A2.
- CED pages: ced:118, ced:119, ced:120, ced:121, ced:122, ced:123, ced:124, ced:125, ced:126, ced:127, ced:128, ced:129, ced:130, ced:131.
- Scoring guidelines: sg-23:2, sg-23:3, sg-23:4, sg-23:8, sg-23:16, sg-23:17, sg-23:18, sg-24:3, sg-24:4, sg-24:12, sg-24:18, sg-25:13, sg-25:14, sg-25:16, sg-25:17, sg-25:18, sg-25:19. Sample responses: samples-13-q1:1, samples-15-q1:1.
- Chief reader reports: cr-23:4, cr-23:7, cr-23:11, cr-23:12, cr-23:16, cr-23:19, cr-23:20, cr-23:28, cr-23:31, cr-23:32, cr-24:3, cr-24:4, cr-24:14, cr-24:19, cr-24:27, cr-24:32.
- Research headings: research/units/unit-06-integration-accumulation.md#Unit 6, Integration and Accumulation of Change; research/units/unit-06-integration-accumulation.md#6.2 Approximating Areas with Riemann Sums; research/units/unit-06-integration-accumulation.md#6.4 The Fundamental Theorem of Calculus and Accumulation Functions; research/units/unit-06-integration-accumulation.md#6.7 The Fundamental Theorem of Calculus and Definite Integrals; research/units/unit-06-integration-accumulation.md#6.14 Selecting Techniques for Antidifferentiation; research/units/unit-06-integration-accumulation.md#Misconception summary; research/units/unit-06-integration-accumulation.md#Unresolved; research/exam/exam-structure.md#Section and part layout; research/exam/exam-structure.md#Free-response point totals; research/question-analysis/frq-analysis.md#The calculator questions and the no-calculator questions; research/question-analysis/frq-analysis.md#How concepts combine inside one question; research/scoring/common-point-losses.md#Setup points; research/scoring/common-point-losses.md#Answer points; research/scoring/common-point-losses.md#Units points; research/scoring/common-point-losses.md#Interpretation points; research/scoring/common-point-losses.md#Justification points; research/scoring/common-point-losses.md#Notation points; research/scoring/notation-requirements.md#The equal sign; research/scoring/notation-requirements.md#Simplification; research/scoring/notation-requirements.md#The differential is normally optional; research/scoring/notation-requirements.md#Limit notation; research/scoring/notation-requirements.md#What notation never costs; archetype entries: (research/question-analysis/question-archetypes.md#BC-QA-06001 Riemann sum from a table with over or under estimate reasoning) and the `###` entries for every archetype in the table of section 2.
- Plan and code: docs/plan/15-lessons.md (What a lesson is, and its granularity; Decision lessons for confusable sets; Fluency, measured and never credited; Open-questions register Q19); docs/lessons/TEMPLATE.md (Delivery); docs/lessons/decisions/LSN-DEC-06-01.md; app/engine/constants.py (`PRODUCTIVE_FAILURE_TARGETS`); data/staging/corrections-skills-concept-lists.json; BUILD-LEDGER.md (stage 14, stage 15).
- [inferred] claims and what settles them: which steps are held in the head (timing per step from 10's fluency telemetry); FRQ point counts for BC-QA-06006, 06008, 06010, 06013 (a scoring guideline for that exact shape); LSN-DEC-06-02's selecting feature (the decision design's parameter draws); why no Unit 6 technique set is derived (component sizes from `app/lessons/confusable.py`); every non-text delivery mode and the one-control rule (the modality A/B).
