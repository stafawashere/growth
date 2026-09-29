---
title: Unit 8 attack map, Applications of Integration
research_date: 2026-09-29
status: draft
purpose: The map every designer of the 21 Unit 8 concept lessons reads first. It fixes the concept order along the prerequisite edges, the exam question types the unit feeds and the points they score, the cross-concept recognition features and the unit's confusable set, the recurring traps, the time budgets per archetype shape, and the delivery mode per concept under the TEMPLATE selection rules, all computed from the library or cited to research and cached pages.
---

# Unit 8 attack map, Applications of Integration

Scope: BC-UNIT-08, topics BC-TOP-0801 to BC-TOP-0813, CED pages ced:152 to ced:164 (research/units/unit-08-applications-integration.md#Unit 8, Applications of Integration). The CED page numbers are the PDF page index; the printed pages run 147 to 159 (research/units/unit-08-applications-integration.md#Unresolved). Every count below was computed on 2026-09-29 from the content snapshot (`app.content.loader.load_snapshot`), `data/prereq_edges.csv`, `data/errors.json`, `data/misconceptions.json` and `tools/check_lessons.py --sets`. A claim with no library or research source is tagged [inferred] with what would settle it.

Library facts that shape the whole map.

- Every one of the 59 Unit 8 skills (BC-SKL-08001 to BC-SKL-08059) is active, and every concept's `skills` list agrees with the skills' own `concept` back-reference. No skill is unlisted. Plan 15 Q19 has nothing to resolve in this unit.
- Four Unit 8 archetypes are retired and superseded: BC-QA-08004 by BC-QA-06005, BC-QA-08005 by BC-QA-06006, BC-QA-08007 by BC-QA-06015, and BC-QA-06007 by BC-QA-08001. The research file's archetype summary still lists the retired ids (research/units/unit-08-applications-integration.md#Archetype summary); a designer uses the successors.
- No Unit 8 concept is in `PRODUCTIVE_FAILURE_TARGETS` (app/engine/constants.py), although BC-QA-08008 carries BC-DF-13 and BC-QA-99008 carries BC-DF-15. See section 6.

## 1. Concept order along the prerequisite edges

Computed: a concept is a parent of another when a `hard_prerequisite` edge in `data/prereq_edges.csv` runs from one of its skills to one of the other's skills. Kahn's topological sort over those concept edges, ties broken by id, gives the order below. All 21 concepts are reached, so the concept graph has no cycle and no skill-level fallback is needed. "Hard parents in Unit 8" are Unit 8 concepts; "outside hard" are hard edges from other units' skills; "outside supporting" are supporting edges from skills or topic stand-ins; "BC-PRQ" are the non-calculus parents, every one a `supporting` edge with evidence tag inferred.

| # | Concept | Name | Skills | Hard parents in Unit 8 | Outside hard parents | Outside supporting | BC-PRQ parents |
|---|---|---|---|---|---|---|---|
| 1 | BC-CON-08001 | Average value of a function over an interval | BC-SKL-08001, 08002, 08003 | none | BC-SKL-06028, 06034, 06038 | none | BC-PRQ-06005, 06007, 08006 |
| 2 | BC-CON-08002 | Average value contrasted with average rate of change | BC-SKL-08004, 08005 | BC-CON-08001 | BC-SKL-06001, 06036 | none | BC-PRQ-06005 |
| 3 | BC-CON-08003 | Displacement as the definite integral of velocity | BC-SKL-08006 | none | BC-SKL-06036 | none | BC-PRQ-06005 |
| 4 | BC-CON-08004 | Total distance as the definite integral of speed | BC-SKL-08007, 08008, 08011 | BC-CON-08003 | BC-SKL-06031 | BC-TOP-0402 | BC-PRQ-06005, 08001, 08003 |
| 5 | BC-CON-08005 | Position and velocity recovered from an initial value | BC-SKL-08009, 08010 | BC-CON-08003 | BC-SKL-06037, 06039 | none | BC-PRQ-06005 |
| 6 | BC-CON-08006 | Amount at a time from an initial amount and a rate | BC-SKL-08012, 08016, 08017 | none | BC-SKL-06034, 06036, 06037 | none | BC-PRQ-06005, 08006 |
| 7 | BC-CON-08007 | Net rate as rate in minus rate out | BC-SKL-08013 | none | BC-SKL-06039 | none | BC-PRQ-06005 |
| 8 | BC-CON-08008 | Extreme value of an accumulated amount from the sign of the net rate | BC-SKL-08014 | BC-CON-08006, BC-CON-08007 | BC-SKL-05020, 05026, 05028 | none | BC-PRQ-08001 |
| 9 | BC-CON-08009 | Meaning of a definite integral in context | BC-SKL-08015 | none | BC-SKL-06036 | none | BC-PRQ-06005 |
| 10 | BC-CON-08011 | Limits of integration from the boundary of the region | BC-SKL-08020, 08021 | none | BC-SKL-05010 | none | BC-PRQ-08001, 08006 |
| 11 | BC-CON-08010 | Area between two curves integrated in x | BC-SKL-08018, 08019, 08022 | BC-CON-08011 | BC-SKL-05014, 06028, 06034 | BC-SKL-06050 | BC-PRQ-06002, 06005 |
| 12 | BC-CON-08012 | Area between two curves integrated in y | BC-SKL-08023, 08024, 08025, 08026 | BC-CON-08010 | BC-SKL-03015 | none | BC-PRQ-06005, 08002 |
| 13 | BC-CON-08013 | Region split where the boundary curves cross | BC-SKL-08027, 08028, 08029, 08030 | BC-CON-08010, BC-CON-08011 | none | none | BC-PRQ-06005, 08001, 08003 |
| 14 | BC-CON-08015 | Cross sectional dimension read from the region | BC-SKL-08031 | BC-CON-08010 | none | none | BC-PRQ-08004 |
| 15 | BC-CON-08014 | Volume as the integral of a cross sectional area | BC-SKL-08032, 08033, 08034, 08035 | BC-CON-08012, BC-CON-08015 | BC-SKL-06034 | BC-SKL-06047 | BC-PRQ-06002, 08002, 08004 |
| 16 | BC-CON-08016 | Cross sectional area from the shape of the slice | BC-SKL-08036, 08037, 08038, 08039 | BC-CON-08015 | BC-SKL-06034 | none | BC-PRQ-06002, 06007, 08005 |
| 17 | BC-CON-08017 | Disc method for a solid of revolution | BC-SKL-08040, 08041, 08042, 08043 | BC-CON-08012, BC-CON-08015 | BC-SKL-06034 | none | BC-PRQ-06002, 08002, 08004 |
| 18 | BC-CON-08018 | Radius measured from a line other than an axis | BC-SKL-08044, 08045, 08046, 08047 | BC-CON-08012, BC-CON-08017 | none | none | BC-PRQ-08002, 08004 |
| 19 | BC-CON-08019 | Washer method for a region held away from the axis | BC-SKL-08048, 08049, 08050, 08051 | BC-CON-08010, BC-CON-08012, BC-CON-08017 | none | none | BC-PRQ-06002, 08002, 08004 |
| 20 | BC-CON-08020 | Washer radii measured from a line other than an axis | BC-SKL-08052, 08053, 08054, 08055 | BC-CON-08018, BC-CON-08019 | none | none | BC-PRQ-08002, 08004 |
| 21 | BC-CON-08021 | Arc length of a curve given by a function | BC-SKL-08056, 08057, 08058, 08059 | none | BC-SKL-02021, 06034, 06057 | BC-SKL-03002, 06034, 06047 | BC-PRQ-06005, 06007, 08006, 08007 |

Order notes.

- Seven concepts have no Unit 8 hard parent: BC-CON-08001, 08003, 08006, 08007, 08009, 08011 and 08021. They open the four strands: average value (08001, 08002), motion (08003 to 08005), applied accumulation (08006 to 08009), and the region strand (08011 onward). BC-CON-08021 has no Unit 8 parent and sits last only because its id is largest.
- BC-CON-08011 precedes BC-CON-08010 because BC-SKL-08020 or 08021 is a hard parent of the area setup, so a designer of LSN-CON-08010 may assume the limits are already found from the intersections.
- BC-CON-08015 precedes BC-CON-08014 because the cross sectional dimension (BC-SKL-08031) is a hard parent of the volume setups; BC-CON-08015 in turn needs only BC-CON-08010.
- The revolution chain is BC-CON-08017, then 08018 and 08019, then 08020. Every volume concept has BC-CON-08012 (area in y) as a hard parent, so the slicing variable is placed before any volume lesson.
- BC-CON-08008 is the only concept with hard parents in Unit 5 (BC-SKL-05020, 05026, 05028): the candidates test and the sign argument (research/units/unit-08-applications-integration.md#What Unit 8 depends on).

## 2. Exam question types the unit feeds

Budgets from (research/exam/exam-structure.md#Section and part layout): Section I Part A (29 questions, 62 minutes, no calculator) 2.14 minutes per question; Part B (13 questions, 38 minutes, calculator) 2.92; Section II (Part A 2 questions in 30 minutes, calculator; Part B 4 in 60, no calculator) 15.0 per question, 9 points each (research/exam/exam-structure.md#Free-response point totals). Slot facts from (research/question-analysis/frq-analysis.md#The calculator questions and the no-calculator questions): Q1 is the contextual calculator slot, recovering an accumulated amount from a rate, an average value, an extremum of an accumulation, and its primary unit is BC-UNIT-08 in 20 of 44 records; Q3 to Q6 are no calculator. Arc length is a BC-only element inside BC-UNIT-08 (research/question-analysis/frq-analysis.md#Shared AB and BC questions against BC-only questions).

The table lists every active archetype whose `skills` meets a Unit 8 skill, grouped by `family`. "Either" archetypes appear in both calculator parts.

| Family | Archetype | Calculator | MCQ part | FRQ part | Point types | Official examples (record) |
|---|---|---|---|---|---|---|
| average-value | BC-QA-08001 Average value of a function over an interval | calculator | I-B | II-A | BC-PT-99001, 99004, 99020, 99003 | BC-FRQ-2015-Q3-D, 2019-Q1-B, 2019-Q2-B, 2021-Q1-D, 2022-Q1-B; BC-MCQ-PE2012-035, BC-MCQ-SAMPLE-009 |
| average-rate-of-change | BC-QA-99007 Average rate of change reported on its own with units | calculator | I-B | II-A (opening part, one point) | BC-PT-99021, 99006, 99004 | BC-FRQ-2014-Q1-A |
| mean-value-theorem | BC-QA-08002 Instantaneous rate set equal to an average rate of change | calculator | I-B | II-A | BC-PT-99021, 99020, 99004, 99005 | BC-FRQ-2014-Q1-A, 2014-Q1-C, 2025-Q1-B |
| motion-by-accumulation | BC-QA-08003 Rectilinear motion analysed with definite integrals | either | I-A or I-B | II-A or II-B (two or three parts) | none | none (MCQ: BC-MCQ-SAMPLE-016, BC-MCQ-PE2012-042) |
| accumulation-with-initial-condition | BC-QA-06005 Net change from a rate with an initial condition | either | I-A or I-B | II-A or II-B | BC-PT-99001, 99004, 99069, 99002, 99033, 99003 | BC-FRQ-2019-Q1-A, 2013-Q1-B, 2022-Q3-A, 2015-Q1-A, 2024-Q1-C, 2025-Q3-D, 2026-Q1-C, 2018-Q1-A, 2018-Q2-B |
| rate-in-rate-out | BC-QA-06006 Rate in minus rate out accumulation | calculator | I-B | II-A | BC-PT-99001, 99068 | BC-FRQ-2015-Q1-D, 2018-Q1-B |
| accumulation-total-from-rate | BC-QA-99008 Total amount from a rate with no initial condition and no rate out | calculator | I-B | II-A (opening part, two points) | BC-PT-99001, 99002, 99004 | BC-FRQ-2013-Q1-B, 2015-Q1-A, 2018-Q1-A |
| accumulation-of-density | BC-QA-99009 Density accumulated over a spatial interval | calculator | I-B | II-A | none | BC-FRQ-2018-Q2-B |
| accumulation-extremum | BC-QA-08006 Time at which an accumulated amount is maximal | calculator | I-B | II-A (closing part) | BC-PT-99013, 99004, 99010, 99011, 99064 | BC-FRQ-2019-Q1-C, 2013-Q1-D, 2022-Q1-D, 2015-Q1-C, 2018-Q1-D |
| accumulation-interpretation | BC-QA-06015 Interpreting a definite integral in context with units | either | I-A or I-B | II-A or II-B | none | none |
| area-between-curves | BC-QA-08008 Area of a region between two curves in x | either | I-A or I-B | II-B opening part, or II-A | BC-PT-99059, 99003, 99004, 99001 | BC-FRQ-2014-Q5-A, 2022-Q5-A, 2023-Q5-A |
| area-between-curves | BC-QA-08009 Area of a region integrated with respect to y | either | I-A or I-B | II-A or II-B | none | none (MCQ: BC-MCQ-CED-010) |
| area-between-curves | BC-QA-08010 Area of a region whose boundary curves cross | either | I-A or I-B | II-A or II-B | none | none |
| cross-sectional-volume | BC-QA-08011 Volume of a solid with known cross sections | either | I-A or I-B | II-A or II-B | BC-PT-99001, 99056, 99057, 99004 | BC-FRQ-2022-Q5-B; BC-MCQ-PE2012-040 |
| revolution-volume | BC-QA-08012 Volume of a solid of revolution by the disc method | either | I-A or I-B | II-A or II-B | BC-PT-99058, 99001, 99003, 99004, 99053 | BC-FRQ-2021-Q3-C, 2022-Q5-C, 2026-Q5-B |
| revolution-volume | BC-QA-08013 Volume of a solid of revolution by the washer method | either | I-A or I-B | II-A or II-B | BC-PT-99058, 99001 | BC-FRQ-2014-Q5-B |
| arc-length | BC-QA-08014 Arc length of a curve given by a function | either | I-A or I-B | II-B (BC-only), or a calculator setup and value part | BC-PT-99022, 99051, 99004, 99009, 99001 | BC-FRQ-2014-Q5-C, 2024-Q5-B, 2026-Q5-C; BC-MCQ-PE2012-004 |

### The free-response parts Unit 8 feeds and the points they score

From the archetype `scoring_pattern`, the BC-PT names, and the generated evidence index (research/units/unit-08-applications-integration.md#Official evidence index). No Unit 8 BC-PT carries `units_required` yes except BC-PT-99006 (Units); elsewhere units are read only where the prompt asks for them (research/scoring/notation-requirements.md#What notation never costs).

- Area (BC-QA-08008, 08009, 08010). Integrand point BC-PT-99059 (area integrand for a region between curves), antiderivative point BC-PT-99003, answer point BC-PT-99004: three points in 2023 (sg-23:16, sg-23:17). The limits are scored inside the integrand or setup point; BC-FRQ-2022-Q5-A scores the definite integral with its limits (BC-PT-99001) and the value. A reversed difference asserted equal to the positive area loses the answer point (sg-23:16, sg-23:17). The split region and area in y scoring patterns are inferred from 2023 (research/units/unit-08-applications-integration.md#Unresolved).
- Volume (BC-QA-08011, 08012, 08013). Setup point: BC-PT-99058 (volume integrand form) for pi with the squared radius or squared radii and the limits, or BC-PT-99001 for a cross section integral; answer point BC-PT-99004. The constant pi is part of the revolution integrand; its omission costs the answer point (BC-ERR-08037). The record's official parts add points from the integration technique the integrand needs: BC-FRQ-2022-Q5-B adds integration by parts (BC-PT-99056, 99057), BC-FRQ-2022-Q5-C adds limit notation for an improper volume (BC-PT-99053) and the antiderivative (BC-PT-99003), BC-FRQ-2021-Q3-C adds the antiderivative. BC-FRQ-2014-Q5-B, the washer part, is 3 points on BC-PT-99058 and 99001. No 2023 to 2025 BC free response part asked for a volume, so these patterns are inferred (research/units/unit-08-applications-integration.md#Unresolved).
- Particle motion by integration (BC-QA-08003, with BC-QA-06005 for a position value). Total distance: a setup point for the integral of speed and an answer point for the decimal (sg-24:6, planar analogue). Position value: a point for the definite integral (BC-PT-99001), a point for using the initial condition (BC-PT-99033) and the answer (BC-PT-99004) (sg-24:7). BC-QA-08003 carries no `point_types`, and its rectilinear pattern is transported from the planar parts of Unit 9 (research/units/unit-08-applications-integration.md#Unresolved).
- Average value (BC-QA-08001). Two points: the integral together with evidence of division by the interval length (BC-PT-99020 or BC-PT-99001), and the value to three decimal places (BC-PT-99004). In 2025 unclear communication between integral and answer was treated as scratch work and both points were awarded (sg-25:3); a 2023 response with the same unlinked chain earned one of two (sg-23:4). BC-FRQ-2015-Q3-D, no calculator, adds the antiderivative point (BC-PT-99003). Units only where asked (BC-QA-99007 for the contrast shape: one point for the answer with units, samples-14-q1:1).
- Amount from a rate (BC-QA-06005, 06006, 99008). Integral point BC-PT-99001 with limits matching the requested interval, initial condition point BC-PT-99033, answer point BC-PT-99004; the integral value presented without the initial amount does not earn BC-PT-99033 (sg-24:3, sg-24:4). With no initial condition the points fall to integrand (BC-PT-99002), antiderivative (BC-PT-99003) and value, and the answer point requires the antiderivative point (sg-25:14).
- Maximum of an accumulated amount (BC-QA-08006). Three points: the derivative considered equal to zero (BC-PT-99013), a global justification (BC-PT-99011 candidates test, or BC-PT-99010 sign analysis), and the answer (BC-PT-99004); a first or second derivative test presented alone does not earn the justification point but leaves the answer available (sg-25:5).
- Arc length (BC-QA-08014). Identifying a supplied integral as arc length: two points, one for naming the arc length of the function and one for naming the interval (sg-24:16, BC-PT-99009 twice on BC-FRQ-2024-Q5-B). A numerical or setup part: the arc length integrand BC-PT-99051 (or BC-PT-99001 for the integral with limits) and the answer; BC-FRQ-2014-Q5-C adds the derivative by the product rule (BC-PT-99022).

## 3. Cross-concept patterns

### Which concepts the stems combine

Computed from the archetypes' `skills` mapped to concepts:

- BC-QA-08003 joins BC-CON-08003, 08004 and 08005 (displacement, distance, position from an initial value).
- BC-QA-06005 joins BC-CON-08005 and 08006; BC-QA-06006 joins 08006 and 08007; BC-QA-08006 joins 08006 and 08008. The Q1 contextual question chains these: total from a rate, then an amount with the initial condition, then the time of maximum (BC-FRQ-2013-Q1-B, C, D; BC-FRQ-2015-Q1-A to D).
- BC-QA-08001, 08002 and 99007 each join BC-CON-08001 and 08002; BC-QA-06015 and 99009 join 08002 with 08009 or 08006.
- BC-QA-08008 joins BC-CON-08010 and 08011. BC-QA-08011 joins 08014, 08015 and 08016. BC-QA-08012 joins 08017 and 08018. BC-QA-08013 joins 08019 and 08020.
- The region question in the no calculator slot opens with an area part and follows with volumes on the same region: BC-FRQ-2014-Q5-A, B, C (area, washer, arc length) and BC-FRQ-2022-Q5-A, B, C (area, cross sections, disc) (BC-QA-08011 `multipart_structure`: "often opens with an area part on the same region").
- Across units, BC-UNIT-06 with BC-UNIT-08 is the dominant pairing in the FRQ corpus, and BC-UNIT-08 with BC-UNIT-09 covers parametric and polar parts that are area or length computations underneath (research/question-analysis/frq-analysis.md#How concepts combine inside one question). Every volume part also loads a Unit 6 technique skill in the record (BC-SKL-06057 on 2022-Q5-B, BC-SKL-06066 on 2022-Q5-C, BC-SKL-06055 on 2021-Q3-C).

### Recognition features between neighbouring concepts, and the first written line

| Neighbours | What in the stem selects each | First written line | Source |
|---|---|---|---|
| Area in x against area in y (BC-CON-08010, 08012) | Integrate in y when the curves are given as functions of y, or when the region in x would need two integrals because the left and right boundaries each stay one curve | Area in x: \(\int_a^b (\text{upper}-\text{lower})\,dx\). Area in y: both boundaries rewritten as \(x=g(y)\), then \(\int_c^d (\text{right}-\text{left})\,dy\) with limits as y values | BC-QA-08009 `difficulty_variables` and `expected_solution_path`; BC-SKL-08026; BC-ERR-08023, BC-ERR-08024 |
| One region against a split region (BC-CON-08010, 08013) | The curves cross inside the interval, so the upper curve changes | Every intersection solved and ordered, then one integral per piece with the order of subtraction fixed, or \(\int_a^b \lvert f(x)-g(x)\rvert\,dx\) when a calculator is allowed | BC-QA-08010 `expected_solution_path`, `wrong_approaches`; BC-ERR-08026, BC-ERR-08027 |
| Limits from the region against a given interval (BC-CON-08011) | The region is bounded by an intersection rather than a vertical line | The equation \(f(x)=g(x)\) solved, by hand or on the calculator with the values stored | BC-QA-08008 `difficulty_variables`; BC-ERR-08019 |
| Cross section against disc against washer (BC-CON-08014, 08017, 08019) | "Cross sections perpendicular to the axis are squares, rectangles, triangles, semicircles" selects a cross section; "revolved about" with the region touching the axis selects a disc; "revolved about" with the region held away from the axis selects a washer | Cross section: the side as the distance between the curves, then the shape's area formula. Disc: the radius as a distance to the axis. Washer: which curve is farther from the axis, then both radii | BC-QA-08011, 08012, 08013 `expected_solution_path`; BC-ERR-99011; BC-MIS-08015 |
| Shape of the slice (BC-CON-08016) | The named shape decides the role of the distance: side, leg, hypotenuse, or diameter | The area of one slice written with its constant factor, for a semicircle with the radius as half the distance | BC-QA-08011 `difficulty_variables`; BC-ERR-06013, BC-ERR-08033, BC-ERR-08034 |
| Axis of revolution a coordinate axis against another line (BC-CON-08017, 08018; 08019, 08020) | The stem names a line \(y=k\) or \(x=h\) | The radius as a distance: \(k-f(x)\) or \(f(x)-k\), whichever is nonnegative; the limits left where the region puts them | BC-QA-08012 `wrong_approaches`; BC-ERR-08038, BC-ERR-08039; BC-MIS-08021, BC-MIS-08022 |
| Washer about a line above against below the region (BC-CON-08020) | The axis lies above or beside the region, which can exchange which curve gives the outer radius | "The curve farther from the axis gives \(R\)" stated before the integral | BC-QA-08013 `difficulty_variables`; BC-ERR-08040; BC-MIS-08023 |
| Displacement against distance (BC-CON-08003, 08004) | "Displacement" or "change in position" selects \(\int v\); "total distance traveled" selects \(\int \lvert v\rvert\), split where \(v\) changes sign when done by hand | \(\int_a^b v(t)\,dt\) against \(\int_a^b \lvert v(t)\rvert\,dt\) | BC-QA-08003 `expected_solution_path`, `wrong_approaches`; BC-ERR-99010, BC-ERR-08010 |
| Change in position against position (BC-CON-08003, 08005) | A stated position at one time and a request for the position at another | \(x(b)=x(a)+\int_a^b v(t)\,dt\) | BC-QA-08003 `scoring_pattern` (sg-24:7); BC-ERR-08011 |
| Net change against amount (BC-CON-08006, 08009) | "How much at time t" with a known amount selects known amount plus the integral; "how much entered", "total" or "net change" with no initial condition selects the integral alone | \(A(b)=A(a)+\int_a^b r(t)\,dt\) (BC-QA-06005); \(\int_a^b r(t)\,dt\) (BC-QA-99008) | BC-QA-06005, BC-QA-99008 `wrong_approaches`; BC-ERR-08012; BC-MIS-08006 |
| One rate against rate in minus rate out (BC-CON-08006, 08007) | Two rates, one increasing and one decreasing the quantity | The net rate as inflow minus outflow in one integral, the outflow in parentheses | BC-QA-06006; BC-ERR-08013, BC-ERR-99009 |
| Amount against its maximum (BC-CON-08006, 08008) | "At what time is the amount greatest" | \(A'(t)=\) net rate \(=0\), then the candidates table with both endpoints | BC-QA-08006; BC-ERR-08016, BC-ERR-99004 |
| Average value against average rate of change (BC-CON-08001, 08002) | "Average value of f" selects \(\frac{1}{b-a}\int_a^b f\); "average rate of change of f" selects \(\frac{f(b)-f(a)}{b-a}\). Units: the function's units against a rate's units | \(\frac{1}{b-a}\int_a^b f(x)\,dx\) (BC-QA-08001) against \(\frac{f(b)-f(a)}{b-a}\) (BC-QA-99007) | BC-QA-08001 and BC-QA-99007 `wrong_approaches`; BC-ERR-99015; BC-MIS-08002 |
| Arc length of a function against a parametric curve (BC-CON-08021, BC-TOP-0903) | \(y=f(x)\) on an x interval selects \(\int_a^b\sqrt{1+(f'(x))^2}\,dx\); \(x(t),y(t)\) on a t interval selects the integral of \(\sqrt{(x')^2+(y')^2}\,dt\), the same shape as the speed integral for planar total distance | \(f'(x)\) written, then the radical with the square and the added one | BC-EK-CHA-6A1 (ced:164), BC-EK-CHA-6B1 (ced:173); research/units/unit-08-applications-integration.md#What depends on Unit 8; BC-ERR-08041, BC-ERR-08042 |
| Arc length against area (BC-CON-08021) | A supplied integral with a radical of one plus a squared derivative is a length, not an area | "The length of the graph of f from x = a to x = b" | BC-QA-08014 `wrong_approaches`; BC-ERR-08043, BC-ERR-08044; BC-MIS-08024 |

### The confusable set

`tools/check_lessons.py --sets` prints ten sets; one is in Unit 8.

- LSN-DEC-08-01: BC-SKL-08006 (compute displacement as the definite integral of velocity), BC-SKL-08008 (split a time interval at the sign changes of velocity), BC-SKL-08011 (select displacement or total distance from the wording of a prompt). All three sit on BC-QA-08003, and all three `adaptive.common_confusions` name BC-MIS-08004 (distance travelled and net change in position treated as one quantity). What selects each member, from the `adaptive.mastered_if` texts: BC-SKL-08011 is the classification from the wording alone, displacement or net change in position against total distance travelled; BC-SKL-08006 is selected by displacement, integral of velocity itself with no absolute value and the sign kept; BC-SKL-08008 is selected by total distance when the integral is done by hand and velocity has an interior zero with a sign change: solve \(v=0\), cut the interval, integrate each piece and sum the absolute values. The feature that separates the stems over two parameter draws is the task word (displacement or total distance) with velocity changing sign inside the interval (BC-QA-08003 `difficulty_variables`, first two entries). Errors the wrong method produces: BC-ERR-99010, BC-ERR-08010, BC-ERR-08009. The set spans LSN-CON-08003 and LSN-CON-08004, so it is served no earlier than the first item loading a second member after the first is reached (docs/plan/15-lessons.md, Decision lessons for confusable sets). BC-QA-08003 has no `point_types`, so the decision lesson names no points (plan 15, R14).

Other contrasts in the table above (average value against average rate, disc against washer against cross section, x against y) are not derived sets; their skills' `confusable_with` lists are wide (for example BC-SKL-08035 names six volume skills) [inferred: the components exceed `DECISION_SET_MAX` (6); settled by printing component sizes from `app/lessons/confusable.py`]. Those contrasts are taught inside the concept lessons' `strategy` blocks.

## 4. Recurring traps

Computed: an active BC-ERR or BC-MIS whose `skills` meet the skills of two or more Unit 8 concepts. Scoring consequences are the record text.

| Record | Concepts | Scoring consequence (record) |
|---|---|---|
| BC-ERR-99019 Decimal presentation error or premature rounding | 08001, 08006, 08011, 08014, 08017, 08021 | The answer point is not earned; the report notes this recurs across several parts of the same response. |
| BC-ERR-08023 Integrand written in one variable with the differential of another | 08012, 08014, 08017, 08019, 08020 | The setup point is lost because the expression does not define a number. |
| BC-ERR-99011 Integrand chosen from the wrong area or volume family | 08010, 08014, 08015, 08017 | The integrand point is not earned; where the form point is separate, an eligible form may still earn it. |
| BC-ERR-08030 Square of a difference used where a difference of squares is needed | 08014, 08016, 08019, 08020 | The setup point is lost, and the value is wrong by the cross term. |
| BC-ERR-99005 Units omitted or built incorrectly | 08002, 08006, 08009 | The units point is not earned; it is scored separately from the value. |
| BC-ERR-99006 Differential omitted from an integral expression | 08006, 08010, 08012 | The setup point is not earned when the resulting expression is ambiguous; in some parts later points in that part are also lost. |
| BC-ERR-08020 Difference of the boundary functions taken in the wrong order | 08010, 08012, 08013 | The integrand point may survive, since either order earned it in 2023, but a negative value reported as an area loses the answer point (sg-23:16, sg-23:17). |
| BC-ERR-08024 Limits given as values of the variable not being integrated | 08012, 08017, 08019 | The setup point is lost and the value is wrong. |
| BC-ERR-99009 Parentheses lost when a given expression is substituted into an integrand | 08007, 08010 | The integrand point is lost; the answer point may survive if a correct calculator value is also reported. |
| BC-ERR-99010 Displacement reported where total distance was asked | 08003, 08004 | The setup point for total distance is not earned; the numerical answer point follows the setup. |
| BC-ERR-99021 Calculator setup not shown before a numerical answer | 08001, 08021 | The setup point is not earned, and an unsupported answer generally receives no credit in a multi point part. |
| BC-ERR-08011 Initial value not added to the accumulated change | 08005, 08006 | The initial condition point is lost and the answer point falls with it (sg-24:7). |
| BC-ERR-08019 Limits of integration taken from the wrong inputs | 08011, 08021 | The answer point is lost, and in 2023 incorrect limits also made a response ineligible for the final area point (sg-23:16). |
| BC-ERR-08037 Factor of pi omitted from a solid of revolution integrand | 08017, 08019 | The answer point is lost. |
| BC-ERR-08038 Radius measured from a coordinate axis when the axis of revolution is elsewhere | 08018, 08020 | The setup point is lost. |
| BC-ERR-08040 Outer and inner radii of a washer exchanged | 08019, 08020 | A negative volume is reported and the answer point is lost. |
| BC-ERR-08045 Numerical length or volume reported with no integral shown | 08014, 08021 | The setup point is lost. |

Misconceptions across two or more concepts (severity from the record): BC-MIS-08006 the integral of a rate is the amount of the quantity (08005, 08006; high); BC-MIS-08009 an interpretation is complete once the quantity is named (08002, 08009; medium); BC-MIS-08011 the order of subtraction in an area integrand does not matter (08010, 08012, 08013; medium); BC-MIS-08013 the differential can be changed without changing the integrand (08012, 08014; high); BC-MIS-08016 the cross sectional dimension is a function value (08014, 08015; high); BC-MIS-08021 the radius is the function value whatever the axis of revolution is (08018, 08020; high); BC-MIS-08023 the upper curve always gives the outer radius (08019, 08020; medium); BC-MIS-09008 a calculator result stands without its expression (08001, 08021; medium). A lesson names these only as the possible-reason line of the error block they are linked to (TEMPLATE, Traps).

Point losses research/scoring names for this unit's shapes:

- (research/scoring/common-point-losses.md#Setup points): no calculator setup before a numerical answer (BC-ERR-99021; cr-23:7, cr-24:4, cr-24:28, crabbc-25:30); differential omitted leaving the expression ambiguous (BC-ERR-99006; cr-23:28, cr-24:27, crabbc-25:23); integrand from the wrong area or volume family, including a squared difference for an area and a missing constant on a revolution (BC-ERR-99011; cr-23:31, cr-24:23, crabbc-25:7, crabbc-25:8); average value setup replaced by a difference quotient (BC-ERR-99015; cr-23:4, crabbc-25:3); displacement setup given where total distance was asked (BC-ERR-99010; cr-23:8, cr-24:8).
- (research/scoring/common-point-losses.md#Answer points): fewer than three digits after the decimal or an intermediate value rounded before reuse (BC-ERR-99019; cr-23:27, cr-24:10, cr-24:26, crabbc-25:8, crabbc-25:30); unrequired simplification that introduces an error (BC-ERR-99022; cr-24:19, crabbc-25:26, crabbc-25:35).
- (research/scoring/common-point-losses.md#Units points): units missing where asked, or a ratio of units built wrongly (BC-ERR-99005; cr-22:14, cr-23:7, cr-24:4, crabbc-25:12).
- (research/scoring/common-point-losses.md#Interpretation points): an arc length named without its interval (BC-ERR-99027; cr-24:32); key phrases absent from an average value interpretation (BC-ERR-99027; cr-24:3); a true statement that does not answer the question (BC-ERR-99027, BC-ERR-99030; cr-24:4).
- (research/scoring/common-point-losses.md#Justification points): a local sign change where a global argument or a complete candidates test was required (BC-ERR-99004; cr-23:16, crabbc-25:4, crabbc-25:18, crabbc-25:30).
- (research/scoring/common-point-losses.md#Notation points): a variable expression equated to a number (BC-ERR-99002; cr-23:19, cr-24:8, cr-24:27, crabbc-25:25); parentheses omitted when a given expression replaces a named function (BC-ERR-99009; cr-23:30, cr-24:23, crabbc-25:7).
- (research/scoring/common-point-losses.md#Precision and presentation points): decimal presentation error carried through several parts (BC-ERR-99019; cr-24:26, crabbc-25:30).
- (research/scoring/notation-requirements.md#The equal sign): an area sentence that equates an integral to a negated value loses the answer point (sg-23:16); an average value chain with unclear communication kept both points in 2025 (sg-25:3). (research/scoring/notation-requirements.md#The differential is normally optional): the phrase "with or without the differential" covers an average value integral, an arc length integral and a volume integral (sg-26:9, sg-26:19). (research/scoring/notation-requirements.md#Simplification): simplification is optional, an attempted one must be correct (sg-23:16).

The four highest severity clusters the unit research ties to scoring guidelines: averaging function values confused with averaging the rate of change (sg-25:4), the integral of a rate reported as the amount itself (sg-24:4, sg-24:7), a local argument offered for a global maximum (sg-25:5), and a definite integral read as an area whatever its integrand (sg-24:16) (research/units/unit-08-applications-integration.md#Misconception summary).

## 5. Time budgets per archetype shape

MCQ budgets are the part figures. An FRQ part's budget is its share of the 15.0 minutes by points out of 9, per plan 15 (docs/plan/15-lessons.md, Fluency, measured and never credited); point counts come from `scoring_pattern` or from the official record's point list in the evidence index. "Writes" names the steps that carry a point; "held" names steps with no point of their own. Which steps a fluent solver holds in the head is [inferred] from where the points sit; settled by timing data per step once 10's fluency telemetry exists.

| Shape | MCQ budget | FRQ points and budget | A fluent solver writes | Held |
|---|---|---|---|---|
| BC-QA-08001 average value | I-B 2.92 | 2 = 3.33 (3 = 5.0 with an antiderivative, BC-FRQ-2015-Q3-D) | \(\frac{1}{b-a}\int_a^b f(x)\,dx\), the value to three places | the interval length |
| BC-QA-99007 average rate of change | I-B 2.92 | 1 = 1.67 | the difference quotient, the value with units | the endpoint evaluations |
| BC-QA-08002 rate equal to average rate | I-B 2.92 | 2 = 3.33 | the average rate of change, the equation \(f'(c)=\) that value, the input | the calculator solve |
| BC-QA-08003 motion by integration | I-A 2.14 or I-B 2.92 | distance 2 = 3.33; position 3 = 5.0 | \(\int \lvert v\rvert\) or the split pieces, the value; \(x(b)=x(a)+\int v\), the value | the sign chart of \(v\) on a calculator part |
| BC-QA-06005 amount with initial condition | I-A 2.14 or I-B 2.92 | 3 = 5.0 | \(A(b)=A(a)+\int_a^b r\), the value with units | the calculator evaluation |
| BC-QA-06006 rate in minus rate out | I-B 2.92 | 2 on the records (BC-FRQ-2015-Q1-D) = 3.33 | one integral of inflow minus outflow, plus the initial amount | which rate is which |
| BC-QA-99008 total from a rate | I-B 2.92 | 2 = 3.33 | the integral, the value | the interval read from the wording |
| BC-QA-08006 time of maximum | I-B 2.92 | 3 = 5.0 (4 = 6.67 on BC-FRQ-2022-Q1-D) | \(A'(t)=0\) solved, the candidates table with both endpoints, the time | the amount at each candidate typed into the calculator |
| BC-QA-06015 interpretation | I-A 2.14 or I-B 2.92 | 1 = 1.67 | one sentence: quantity, units, interval | the units product |
| BC-QA-08008 area in x | I-A 2.14 or I-B 2.92 | 3 = 5.0 (2 on BC-FRQ-2022-Q5-A = 3.33) | the integral of upper minus lower with limits, the antiderivative, the value | which curve is upper, the intersection solve on a calculator part |
| BC-QA-08009 area in y | I-A 2.14 or I-B 2.92 | 2 [inferred from sg-23:16] = 3.33 | both boundaries as \(x=g(y)\), the integral in \(dy\) with y limits, the value | which curve is right |
| BC-QA-08010 split region | I-A 2.14 or I-B 2.92 | 2 [inferred from sg-23:16] = 3.33 | every intersection, one integral per piece or the absolute value integral, the value | the sign of the difference on each piece |
| BC-QA-08011 cross sections | I-A 2.14 or I-B 2.92 | 2 = 3.33 (4 = 6.67 on BC-FRQ-2022-Q5-B, with integration by parts) | the slice area in terms of the distance, the integral with limits, the value | the role of the distance in the shape |
| BC-QA-08012 disc | I-A 2.14 or I-B 2.92 | 2 = 3.33 (4 = 6.67 on BC-FRQ-2021-Q3-C) | \(\pi\int (\text{radius})^2\), the limits, the value | the radius as a distance |
| BC-QA-08013 washer | I-A 2.14 or I-B 2.92 | 3 on BC-FRQ-2014-Q5-B = 5.0 | \(\pi\int (R^2-r^2)\) with limits, the value | which curve is outer |
| BC-QA-08014 arc length | I-A 2.14 or I-B 2.92 | 2 = 3.33 (3 = 5.0 on BC-FRQ-2014-Q5-C) | \(\int_a^b\sqrt{1+(f'(x))^2}\,dx\), the value; or "the length of the graph of f on [a, b]" | the derivative when simple |
| BC-QA-99009 density | I-B 2.92 | none recorded [inferred 2 = 3.33, settled by a scoring guideline for 2018 Q2] | the integral of density times the constant area, the rounded value | the rounding rule |

## 6. Delivery map

TEMPLATE selection rules (docs/lessons/TEMPLATE.md, Delivery): 1 worked examples and error blocks are `step_reveal`; 2 a key idea describing a process is `motion`, with `model` on the example only where a computed sequence of values is the idea; 3 figure-bearing BC-REP (02, 07, 08, 12, 13, 14) gives `figure`, promoted to `interactive` when `common_givens` or `difficulty_variables` name a varying quantity and the stem asks for a reading; 4 BC-REP-03 givens give `table`; 5 everything else is `text`. The figure row also admits a topic Representations paragraph naming a graphical conversion. Rule 1 applies to every concept's examples and error blocks and is not repeated. Every non-text choice is [inferred]; settled by the modality A/B in the build plan (skip rate and time to first credited success by mode). The rule 2 readings for volumes (a region revolved, slices stacked along the axis) are a reading of the EK text, not its literal wording [inferred; settled by the TEMPLATE owner ruling whether "a solid swept" and "slices accumulating" are processes under rule 2].

`model` is assigned nowhere. The mode table puts `model` on every productive-failure target, and no Unit 8 concept is in `PRODUCTIVE_FAILURE_TARGETS`, though BC-QA-08008 carries BC-DF-13 and BC-QA-99008 carries BC-DF-15; see Library gaps.

| Concept | Orientation | Key ideas (BC-EK) and mode | Rule and triggering field |
|---|---|---|---|
| BC-CON-08001 | figure | CHA-4B1 figure (graph of f over [a, b] with the rectangle of height equal to the average value and the same area, labels inside) | rule 3, `representations` BC-REP-02 and BC-REP-08 on BC-SKL-08002; not promoted, BC-QA-08001 `difficulty_variables` vary a form ("formula versus graph presentation") |
| BC-CON-08002 | text | CHA-4B1 text (the two quotients side by side, units named) | rule 5, BC-REP-04, 01, 05 on BC-SKL-08004, 08005 |
| BC-CON-08003 | figure | CHA-4C1 figure (velocity graph with signed areas above and below the axis) | rule 3 through the topic Representations paragraph, "velocity graph to signed and unsigned area" (research/units/unit-08-applications-integration.md#8.2 Connecting Position, Velocity, and Acceleration of Functions Using Integrals); BC-SKL-08006 itself is BC-REP-01, 05 |
| BC-CON-08004 | figure | CHA-4C1 figure (the same velocity graph with the negative piece reflected, the zero of v marked as the split) | rule 3, BC-REP-02 on BC-SKL-08008; not promoted, BC-QA-08003 `difficulty_variables` are presence flags ("whether velocity changes sign") |
| BC-CON-08005 | text | CHA-4C1 text | rule 5, BC-REP-01, 05 on BC-SKL-08009, 08010 |
| BC-CON-08006 | text | CHA-4D1 `motion` (the amount traced as the upper time moves, starting from the initial amount); CHA-4E1 text | rule 2, "an accumulation of a rate of change" (ced:154) is a quantity accumulating; rule 5 for the rest, BC-REP-05, 01, 09 |
| BC-CON-08007 | text | CHA-4D2, CHA-4E1 text | rule 5, BC-REP-05, 01 on BC-SKL-08013 |
| BC-CON-08008 | text | CHA-4D1 text (candidates table) | rule 5, BC-REP-05, 09 on BC-SKL-08014 |
| BC-CON-08009 | text | CHA-4D1, CHA-4D2 text | rule 5, BC-REP-04, 05 on BC-SKL-08015; the topic's tabulated rate (BC-REP-03) sits on BC-QA-06001, not on this concept's skill |
| BC-CON-08011 | figure | CHA-5A1 figure (region with its intersection points marked and the limits read from them) | rule 3, BC-REP-02 on BC-SKL-08021 |
| BC-CON-08010 | figure | CHA-5A1 figure (region shaded, each bounding curve labelled, one vertical representative rectangle from lower to upper curve) | rule 3, BC-REP-02 on BC-SKL-08018, 08019; not promoted, BC-QA-08008 `difficulty_variables` are presence flags |
| BC-CON-08012 | figure | CHA-5A2 figure (the same region with a horizontal rectangle from left to right curve, y limits on the axis) | rule 3, BC-REP-02 on BC-SKL-08024, 08025, BC-REP-08 on BC-SKL-08026; not promoted |
| BC-CON-08013 | figure | CHA-5A3 `interactive` (a vertical rectangle dragged across a region whose curves cross; reading: which curve is on top at the dragged input, and where the difference changes sign) | rule 3 promoted, BC-REP-02 on BC-SKL-08027, 08028; BC-QA-08010 `difficulty_variables` "the number of interior crossings", and the stem asks which curve is greater on each piece |
| BC-CON-08015 | figure | CHA-5B1 figure (one slice drawn across the base region with both endpoints on the curves labelled) | rule 3, BC-REP-08 on BC-SKL-08031 |
| BC-CON-08014 | figure | CHA-5B1 `motion` (a square slice moving along the axis across the base region, the solid built from the slices) | rule 2 [inferred reading, slices accumulating]; rule 3, BC-REP-08 on BC-SKL-08032, 08033, 08034 for the static fallback |
| BC-CON-08016 | figure | CHA-5B2, CHA-5B3 figure (the four slice shapes, the distance labelled as side, leg, hypotenuse or diameter) | rule 3, BC-REP-08 on BC-SKL-08036 to 08038; not promoted, BC-QA-08011 `difficulty_variables` vary a category ("the shape of the cross section") |
| BC-CON-08017 | figure | CHA-5C1 `motion` (the region swept about the axis into a solid, one disc highlighted with its radius) | rule 2 [inferred reading, a region revolved]; rule 3, BC-REP-08 on BC-SKL-08040 for the fallback |
| BC-CON-08018 | figure | CHA-5C2 `interactive` (the axis of revolution moved as a horizontal line \(y=k\); reading: the radius at a marked input and the unchanged limits) | rule 3 promoted, BC-REP-08 on BC-SKL-08044 to 08047; BC-QA-08012 `difficulty_variables` "whether the axis is a coordinate axis or another line", and the stem asks for the radius |
| BC-CON-08019 | figure | CHA-5C3 figure (the region held off the axis, one washer with R and r labelled) | rule 3, BC-REP-08 and BC-REP-02 on BC-SKL-08048; the sweep itself is taught in LSN-CON-08017 |
| BC-CON-08020 | figure | CHA-5C4 `interactive` (the axis line moved from below the region to above it; reading: which curve gives the outer radius) | rule 3 promoted, BC-REP-08 and 02 on BC-SKL-08054; BC-QA-08013 `difficulty_variables` "whether the axis lies above or below the region, which can exchange the radii" |
| BC-CON-08021 | text | CHA-6A1 text | rule 5, BC-REP-01, 04, 05, 09 on BC-SKL-08056 to 08059; no figure-bearing representation |

Where each mode fits, in summary:

- Motion: a region swept into a solid of revolution (LSN-CON-08017); a cross section slice moving along the axis across the base (LSN-CON-08014); an amount traced as the upper time moves from the initial amount (LSN-CON-08006). Every motion entry carries `reduced_motion` and a static fallback of three frames side by side (TEMPLATE, Delivery).
- Interactive: a representative rectangle dragged across a region whose boundary curves cross (LSN-CON-08013); the axis of revolution moved for the disc radius (LSN-CON-08018) and for the washer radii (LSN-CON-08020). One control per screen [inferred, per TEMPLATE].
- A static figure is enough: a region shaded with its bounding curves labelled and one representative rectangle (08010, 08011, 08012); the slice with its endpoints (08015); the slice shapes (08016); a single washer (08019); the average value rectangle (08001); signed and reflected velocity areas (08003, 08004).
- Text and step reveal only: average value against average rate (08002), position from an initial value (08005), rate in minus rate out (08007), the maximum argument (08008), interpretation (08009), and arc length (08021). Their representations are verbal, contextual, symbolic or calculator output, and the content is a sequence of written lines.

## Library gaps met

- Concept `misconceptions` lists name retired BC-MIS ids: BC-CON-08001 and BC-CON-08002 (BC-MIS-08001, successor BC-MIS-99006), BC-CON-08008 (BC-MIS-08008, successor BC-MIS-06010). BC-MIS-08003 is retired to BC-MIS-09008, which is the one the error records use. Designers take possible reasons from the BC-ERR record's `possible_misconceptions`.
- BC-QA-08003, 08009, 08010, 06015 and 99009 carry no `point_types`, so their lessons carry no scoring section (plan 15, R14). BC-QA-08003's pattern names sg-24:6 and sg-24:7, which BC-PT-99051, 99001, 99033 and 99004 would fit.
- BC-QA-08011 lists BC-PT-99056 and 99057 (integration by parts) as its point types. These come from the technique inside BC-FRQ-2022-Q5-B, not from the volume shape; a cross section volume point type (BC-PT-99058 would fit) is absent.
- No 2023 to 2025 BC free response part assessed a volume, an area in y or a split region; those scoring patterns are inferred (research/units/unit-08-applications-integration.md#Unresolved). The rectilinear motion pattern is transported from planar parts.
- The 2018 official records (BC-FRQ-2018-Q1-A to D, 2018-Q2-B) carry 0 points and no point types because no 2018 scoring guideline is in the corpus.
- The research file's archetype table still lists BC-QA-08004, 08005, 08007, which are retired (section opening).
- `PRODUCTIVE_FAILURE_TARGETS` holds no Unit 8 concept while BC-QA-08008 carries BC-DF-13; whether LSN-CON-08010 should get a productive-failure opener is open [settled by the plan owner adding or declining BC-CON-08010 in app/engine/constants.py].

## 7. Sources

- Concepts: BC-CON-08001 to BC-CON-08021. Skills: BC-SKL-08001 to BC-SKL-08059. Outside parents: BC-SKL-02021, BC-SKL-03002, BC-SKL-03015, BC-SKL-05010, BC-SKL-05014, BC-SKL-05020, BC-SKL-05026, BC-SKL-05028, BC-SKL-06001, BC-SKL-06028, BC-SKL-06031, BC-SKL-06034, BC-SKL-06036, BC-SKL-06037, BC-SKL-06038, BC-SKL-06039, BC-SKL-06047, BC-SKL-06050, BC-SKL-06057, BC-TOP-0402. Topics: BC-TOP-0801 to BC-TOP-0813, BC-TOP-0903.
- BC-PRQ-06002, 06005, 06007, BC-PRQ-08001 to BC-PRQ-08007.
- Archetypes: BC-QA-08001, 08002, 08003, 08006, 08008, 08009, 08010, 08011, 08012, 08013, 08014, BC-QA-06005, 06006, 06015, BC-QA-99007, 99008, 99009; retired BC-QA-06007, 08004, 08005, 08007.
- Point types: BC-PT-99001, 99002, 99003, 99004, 99005, 99006, 99009, 99010, 99011, 99013, 99020, 99021, 99022, 99033, 99051, 99053, 99056, 99057, 99058, 99059, 99064, 99068, 99069.
- Official records: BC-FRQ-2013-Q1-B, 2013-Q1-D, 2014-Q1-A, 2014-Q1-C, 2014-Q5-A, 2014-Q5-B, 2014-Q5-C, 2015-Q1-A, 2015-Q1-C, 2015-Q1-D, 2015-Q3-D, 2018-Q1-A, 2018-Q1-B, 2018-Q1-D, 2018-Q2-B, 2019-Q1-A, 2019-Q1-B, 2019-Q1-C, 2019-Q2-B, 2021-Q1-D, 2021-Q3-C, 2022-Q1-B, 2022-Q1-D, 2022-Q3-A, 2022-Q5-A, 2022-Q5-B, 2022-Q5-C, 2023-Q5-A, 2024-Q1-C, 2024-Q5-B, 2025-Q1-B, 2025-Q3-D, 2026-Q1-C, 2026-Q5-B, 2026-Q5-C; BC-MCQ-CED-010, BC-MCQ-SAMPLE-009, BC-MCQ-SAMPLE-016, BC-MCQ-PE2012-004, BC-MCQ-PE2012-035, BC-MCQ-PE2012-040, BC-MCQ-PE2012-042.
- Errors: BC-ERR-06013, BC-ERR-08001, 08009, 08010, 08011, 08012, 08013, 08016, 08019, 08020, 08023, 08024, 08026, 08027, 08030, 08033, 08034, 08037, 08038, 08039, 08040, 08041, 08042, 08043, 08044, 08045, BC-ERR-99002, 99004, 99005, 99006, 99009, 99010, 99011, 99015, 99019, 99021, 99022, 99027, 99030.
- Misconceptions: BC-MIS-08002, 08004, 08006, 08009, 08011, 08013, 08015, 08016, 08021, 08022, 08023, 08024, BC-MIS-09008; retired BC-MIS-08001 (to 99006), 08003 (to 09008), 08008 (to 06010).
- Difficulty factors: BC-DF-13, BC-DF-15. Representations: BC-REP-01, 02, 03, 04, 05, 08, 09.
- Essential knowledge: BC-EK-CHA-4B1, 4C1, 4D1, 4D2, 4E1, 5A1, 5A2, 5A3, 5B1, 5B2, 5B3, 5C1, 5C2, 5C3, 5C4, 6A1, 6B1.
- CED pages: ced:152, ced:153, ced:154, ced:155, ced:156, ced:157, ced:158, ced:159, ced:160, ced:161, ced:162, ced:163, ced:164, ced:173.
- Scoring guidelines: sg-23:4, sg-23:16, sg-23:17, sg-24:3, sg-24:4, sg-24:6, sg-24:7, sg-24:16, sg-25:3, sg-25:4, sg-25:5, sg-25:14, sg-26:9, sg-26:19. Sample responses: samples-14-q1:1.
- Chief reader reports: cr-22:14, cr-23:4, cr-23:7, cr-23:8, cr-23:16, cr-23:19, cr-23:27, cr-23:28, cr-23:30, cr-23:31, cr-24:3, cr-24:4, cr-24:8, cr-24:10, cr-24:19, cr-24:23, cr-24:26, cr-24:27, cr-24:28, cr-24:32, crabbc-25:3, crabbc-25:4, crabbc-25:7, crabbc-25:8, crabbc-25:12, crabbc-25:18, crabbc-25:23, crabbc-25:25, crabbc-25:26, crabbc-25:30, crabbc-25:35.
- Research headings: research/units/unit-08-applications-integration.md#Unit 8, Applications of Integration; research/units/unit-08-applications-integration.md#8.2 Connecting Position, Velocity, and Acceleration of Functions Using Integrals; research/units/unit-08-applications-integration.md#What Unit 8 depends on; research/units/unit-08-applications-integration.md#What depends on Unit 8; research/units/unit-08-applications-integration.md#Archetype summary; research/units/unit-08-applications-integration.md#Misconception summary; research/units/unit-08-applications-integration.md#Unresolved; research/units/unit-08-applications-integration.md#Official evidence index; research/exam/exam-structure.md#Section and part layout; research/exam/exam-structure.md#Free-response point totals; research/question-analysis/frq-analysis.md#The calculator questions and the no-calculator questions; research/question-analysis/frq-analysis.md#How concepts combine inside one question; research/question-analysis/frq-analysis.md#Shared AB and BC questions against BC-only questions; research/scoring/common-point-losses.md#Setup points; research/scoring/common-point-losses.md#Answer points; research/scoring/common-point-losses.md#Units points; research/scoring/common-point-losses.md#Interpretation points; research/scoring/common-point-losses.md#Justification points; research/scoring/common-point-losses.md#Notation points; research/scoring/common-point-losses.md#Precision and presentation points; research/scoring/notation-requirements.md#The equal sign; research/scoring/notation-requirements.md#The differential is normally optional; research/scoring/notation-requirements.md#Simplification; research/scoring/notation-requirements.md#What notation never costs; archetype entries under research/question-analysis/question-archetypes.md, one `###` heading per archetype in the table of section 2 (for example research/question-analysis/question-archetypes.md#BC-QA-08008 Area of a region between two curves in x).
- Plan and code: docs/plan/15-lessons.md (What a lesson is, and its granularity; Decision lessons for confusable sets; Fluency, measured and never credited; Pacing to the exam date); docs/lessons/TEMPLATE.md (Delivery); app/engine/constants.py (`PRODUCTIVE_FAILURE_TARGETS`); tools/check_lessons.py (`--sets`).
- [inferred] claims and what settles them: which steps are held in the head (timing per step from 10's fluency telemetry); FRQ point counts for BC-QA-08009, 08010, 99009 (a scoring guideline for that exact shape); why the volume and average value contrasts are not derived sets (component sizes from `app/lessons/confusable.py`); the rule 2 reading for volumes and every non-text delivery mode and the one-control rule (the modality A/B and the TEMPLATE owner); whether LSN-CON-08010 gets a productive-failure opener (the plan owner).
