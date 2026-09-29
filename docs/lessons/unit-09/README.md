---
title: Unit 9 attack map, Parametric Equations, Polar Coordinates, and Vector-Valued Functions
research_date: 2026-09-29
status: draft
purpose: The map every designer of the 17 Unit 9 concept lessons reads first. It fixes the concept order along the prerequisite edges, the exam question types the unit feeds and the points they score, the cross-concept recognition features, the recurring traps, the time budgets per archetype shape, and the delivery mode per concept under the TEMPLATE selection rules, all computed from the library or cited to research and cached pages.
---

# Unit 9 attack map, Parametric Equations, Polar Coordinates, and Vector-Valued Functions

Scope: BC-UNIT-09, topics BC-TOP-0901 to BC-TOP-0909, CED pages ced:171 to ced:179 (PDF page index; the printed pages run 166 to 174) (research/units/unit-09-parametric-polar-vector.md#Unresolved). Every topic in the unit is BC only (research/units/unit-09-parametric-polar-vector.md#Unit 9, Parametric Equations, Polar Coordinates, and Vector-Valued Functions). Every count below was computed on 2026-09-29 from the content snapshot (`app.content.loader.load_snapshot`), `data/prereq_edges.csv`, `data/errors.json`, `data/misconceptions.json`, `data/scoring_points.json`, `data/taxonomies.json` and `tools/check_lessons.py --sets`. A claim with no library or research source is tagged [inferred] with what would settle it.

Three library facts shape the whole map.

- Every one of the 43 Unit 9 skills (BC-SKL-09001 to BC-SKL-09043) sits in the `skills` list of exactly the concept its own `concept` field names, and no skill is left out of a list. No back-reference correction is needed, unlike Unit 6.
- Unit 9 has no derived confusable set. `tools/check_lessons.py --sets` prints 10 sets and none holds a BC-SKL-09 id, so no LSN-DEC-09 lesson exists. The skills' `confusable_with` fields are filled by `tools/derive_confusable.py` and are read from the snapshot below; the neighbour contrasts they point to are carried in the recognition table of section 3 and in each concept's `strategy` blocks, not in a decision lesson.
- BC-CON-09015 is one of the five productive-failure targets in `PRODUCTIVE_FAILURE_TARGETS` (app/engine/constants.py), reached through BC-QA-09014, whose `difficulty_factors` hold BC-DF-15 (Unsignposted procedure selection), one of the two `PRODUCTIVE_FAILURE_FACTORS`.

## 1. Concept order along the prerequisite edges

Computed: a concept is a parent of another when a `hard_prerequisite` edge in `data/prereq_edges.csv` runs from one of its skills to one of the other's skills. Kahn's topological sort over those concept edges, ties broken by id, reaches all 17 concepts, so the concept graph has no cycle and no skill-level fallback was needed. "Hard parents in Unit 9" are Unit 9 concepts; "outside" lists edges from other units' skills with their type; "BC-PRQ" lists the non-calculus parents, every one of which is a `supporting` edge. Of the 125 edges into Unit 9 skills, 118 carry evidence tag `inferred` and 7 `verified`.

| # | Concept | Name | Skills | Hard parents in Unit 9 | Outside parents | BC-PRQ parents |
|---|---|---|---|---|---|---|
| 1 | BC-CON-09001 | Curve defined by parametric equations | BC-SKL-09001 | none | BC-SKL-03002 (hard) | BC-PRQ-06005 |
| 2 | BC-CON-09002 | Slope of a parametric curve as a quotient of derivatives | BC-SKL-09002 to 09006 | BC-CON-09001 | none | BC-PRQ-06005, 08001, 08006 |
| 3 | BC-CON-09003 | Second derivative of a parametric curve | BC-SKL-09007 to 09010 | BC-CON-09001, 09002 | BC-SKL-02039, BC-SKL-05030 (hard); BC-SKL-02036 (supporting) | BC-PRQ-06005, 08006 |
| 4 | BC-CON-09004 | Arc length of a parametric curve | BC-SKL-09011 to 09014 | BC-CON-09001 | BC-SKL-06034, 08056, 08059 (hard); BC-SKL-06047 (supporting) | BC-PRQ-06005, 08006, 08007, 09004 |
| 5 | BC-CON-09005 | Vector-valued function as a pair of component functions | BC-SKL-09018 | BC-CON-09001 | BC-SKL-07032 (supporting) | BC-PRQ-09001 |
| 6 | BC-CON-09006 | Derivative of a vector-valued function taken component by component | BC-SKL-09015, 09016, 09017 | BC-CON-09001 | none | BC-PRQ-09001 |
| 7 | BC-CON-09007 | Integral of a vector-valued function taken component by component | BC-SKL-09019, 09020 | BC-CON-09006 | BC-SKL-08006 (hard) | BC-PRQ-06005, 09001 |
| 8 | BC-CON-09008 | Particular position from a rate vector and an initial position | BC-SKL-09021, 09022 | BC-CON-09007 | BC-SKL-06037 (hard) | BC-PRQ-06005 |
| 9 | BC-CON-09009 | Speed as the magnitude of the velocity vector | BC-SKL-09023, 09024, 09028 | BC-CON-09006 | none | BC-PRQ-08001, 08007, 09001, 09003 |
| 10 | BC-CON-09010 | Total distance travelled as the integral of speed | BC-SKL-09025, 09026 | BC-CON-09004, 09008, 09009 | BC-SKL-08007, 08009 (hard) | BC-PRQ-06005, 08007 |
| 11 | BC-CON-09011 | Direction of motion read from the signs of the velocity components | BC-SKL-09027 | BC-CON-09001 | none | BC-PRQ-08001 |
| 12 | BC-CON-09012 | Polar to Cartesian relations | BC-SKL-09029 | BC-CON-09007 | none | BC-PRQ-09002 |
| 13 | BC-CON-09013 | Rate of change of r with respect to theta | BC-SKL-09030, 09031, 09032 | none | BC-SKL-03002, 03006 (hard) | BC-PRQ-06005, 09003 |
| 14 | BC-CON-09014 | Slope of a polar curve in the plane | BC-SKL-09033, 09034 | BC-CON-09002, 09012, 09013 | BC-SKL-02036, 05028 (hard) | BC-PRQ-08001, 09002 |
| 15 | BC-CON-09015 | Area of a polar region as an integral of one half r squared | BC-SKL-09035 to 09038 | BC-CON-09012 | BC-SKL-06028, 06034 (hard); BC-SKL-06047 (supporting) | BC-PRQ-06005, 08006, 09002, 09004 |
| 16 | BC-CON-09017 | Intersection angles of two polar curves | BC-SKL-09039 | none | BC-SKL-08018 (hard) | BC-PRQ-08001, 09002 |
| 17 | BC-CON-09016 | Area between two polar curves | BC-SKL-09040 to 09043 | BC-CON-09015, 09017 | BC-SKL-08018 (hard); BC-SKL-08019, 08051 (supporting) | BC-PRQ-06005, 08006, 09002, 09004 |

Order notes.

- BC-CON-09017 precedes BC-CON-09016 although its id is larger, because BC-SKL-09039 (find the intersection angles) is a hard parent of BC-SKL-09041 (set up the area integral between two polar curves). A designer of LSN-CON-09016 may assume the intersection angles are found.
- BC-CON-09012 sits after the whole vector strand only because of one edge, BC-SKL-09019 to BC-SKL-09029, whose note reads "Converting a polar point to Cartesian coordinates treats x and y as functions of the angle as in a parametric representation." The note justifies a link to parametric representation (BC-SKL-09001 or BC-SKL-09018), not to antidifferentiating a vector. This looks like a mis-anchored edge; see Library gaps.
- BC-CON-09013 has no Unit 9 hard parent and could be reached as soon as the chain rule (BC-SKL-03002, BC-SKL-03006) is placed.
- The distance concept BC-CON-09010 is the join of three strands: arc length (BC-SKL-09011 to BC-SKL-09025), position recovery (BC-SKL-09021 to BC-SKL-09026) and speed (BC-SKL-09023 to BC-SKL-09025).
- Within BC-CON-09015, BC-SKL-09036 (bounding angles) is a hard parent of BC-SKL-09035 (state the integral), so the angles are found before the integral is written.

## 2. Exam question types the unit feeds

Budgets (research/exam/exam-structure.md#Section and part layout): Section I Part A, 29 questions in 62 minutes, no calculator, 2.14 minutes per question; Part B, 13 questions in 38 minutes, calculator required, 2.92; Section II Part A, 2 questions in 30 minutes, calculator required, and Part B, 4 questions in 60 minutes, no calculator, 15.0 minutes per question, 9 points each (research/exam/exam-structure.md#Free-response point totals). In the FRQ corpus, Q2 is the BC-only applications slot: its primary unit is BC-UNIT-09 in 36 of 42 part records, every Q2 record is `calculator`, and its assessed work is speed, total distance, an acceleration vector, a coordinate recovered from an initial position, and an area between polar curves (research/question-analysis/frq-analysis.md#The calculator questions and the no-calculator questions). BC-UNIT-08 with BC-UNIT-09 is a recorded pairing, because parametric and polar parts are area or length computations underneath (research/question-analysis/frq-analysis.md#How concepts combine inside one question).

The table lists every active archetype whose `skills` meets a Unit 9 skill, grouped by `family`. MCQ part follows `calculator_status`; FRQ part is II-A for every record whose `multipart_structure` names the calculator active question or whose official examples are Q2 parts, and II-B for the 2018 Q5 no-calculator polar records.

| Family | Archetype | Calculator | MCQ part | FRQ part | Point types | Official examples |
|---|---|---|---|---|---|---|
| parametric-calculus | BC-QA-09001 Slope of the tangent to a parametric path at a time | calculator | I-B (the two MCQ examples are no-calculator, I-A) | II-A | BC-PT-99005, 99049, 99004, 99001 | BC-FRQ-2022-Q2-A, 2015-Q2-B, 2023-Q2-C, 2026-Q2-B; BC-MCQ-SAMPLE-017, BC-MCQ-PE2012-002 |
| parametric-calculus | BC-QA-09002 Second derivative of a parametric curve | either | I-A or I-B | none observed | none | BC-MCQ-CED-018 only |
| arc-length | BC-QA-09003 Length of a parametric curve | calculator | I-B | II-A | none | none |
| parametric-motion | BC-QA-09004 Acceleration vector of a particle in planar motion | calculator | I-B | II-A, opening part | BC-PT-99064, 99052, 99050, 99005 | BC-FRQ-2013-Q2-C, 2022-Q2-B, 2023-Q2-A |
| parametric-motion | BC-QA-09005 Coordinate of a particle recovered from an initial position | calculator | I-B | II-A | BC-PT-99013, 99010, 99033, 99004, 99005, 99002, 99001 | BC-FRQ-2021-Q2-C, 2022-Q2-C, 2015-Q2-A, 2024-Q2-C |
| parametric-motion | BC-QA-09006 Speed of a particle in planar motion | calculator | I-B | II-A | BC-PT-99050, 99052, 99004 | BC-FRQ-2021-Q2-A, 2015-Q2-C, 2023-Q2-B, 2024-Q2-A |
| parametric-motion | BC-QA-09007 Total distance travelled by a particle in the plane | calculator | I-B | II-A | BC-PT-99051, 99004 | BC-FRQ-2021-Q2-B, 2022-Q2-D, 2015-Q2-D, 2023-Q2-D, 2024-Q2-B, 2018-Q2-D; BC-MCQ-SAMPLE-023 |
| parametric-motion | BC-QA-09008 Times at which a particle moves toward a coordinate axis | calculator | I-B | II-A, closing part | BC-PT-99014, 99010 | BC-FRQ-2024-Q2-D |
| polar-calculus | BC-QA-09009 Derivative of r with respect to theta on a polar curve | calculator | I-B (BC-MCQ-PE2012-026 is I-A) | II-A, opening part | BC-PT-99049, 99004, 99005 | BC-FRQ-2014-Q2-B, 2014-Q2-C, 2025-Q2-A, 2018-Q5-B; BC-MCQ-PE2012-026 |
| polar-calculus | BC-QA-09010 Rate at which a particle's distance from the origin changes | calculator | I-B | II-A, closing part (2018-Q5-C is II-B) | BC-PT-99005, 99068, 99004, 99049 | BC-FRQ-2013-Q2-B, 2014-Q2-D, 2025-Q2-D, 2018-Q5-C |
| polar-calculus | BC-QA-09011 Point on a polar curve farthest from a coordinate axis | calculator | I-B | II-A | BC-PT-99013, 99011, 99005 | BC-FRQ-2025-Q2-C |
| polar-calculus | BC-QA-99001 Polar tangent slope relation solved for the derivative of the horizontal coordinate | calculator | I-B | II-A, three points | BC-PT-99049, 99005, 99004 | BC-FRQ-2026-Q2-B |
| polar-calculus | BC-QA-99002 Derivative of a Cartesian coordinate with respect to theta on a polar curve | calculator | I-B | II-A, two points | BC-PT-99049, 99005, 99004 | BC-FRQ-2014-Q2-B |
| polar-calculus | BC-QA-99003 Slope of the tangent line to a polar curve at a stated angle | no_calculator | I-A | II-B | none | BC-FRQ-2018-Q5-B |
| polar-calculus | BC-QA-99006 Rate of change with respect to theta of the gap between two polar curves | calculator | I-B | II-A, two points | BC-PT-99005, 99004 | BC-FRQ-2014-Q2-C |
| polar-motion | BC-QA-99004 Time at which a Cartesian coordinate of a particle on a polar path reaches a value | calculator | I-B | II-A, three points | BC-PT-99005, 99004, 99068 | BC-FRQ-2013-Q2-B |
| polar-motion | BC-QA-99005 Position and velocity vectors for a particle travelling a polar curve | calculator | I-B | II-A, three points | BC-PT-99064, 99005, 99004, 99052 | BC-FRQ-2013-Q2-C |
| polar-area | BC-QA-09012 Area of a region bounded by a single polar curve | either | I-A or I-B | II-A | BC-PT-99048, 99004, 99001, 99005 | BC-FRQ-2019-Q2-A, 2019-Q2-C, 2019-Q2-D, 2026-Q2-A; BC-MCQ-CED-021 |
| polar-area | BC-QA-09013 Area inside one polar curve and outside another | calculator | I-B | II-A (2018-Q5-A is II-B) | BC-PT-99048, 99001, 99004, 99002 | BC-FRQ-2013-Q2-A, 2014-Q2-A, 2025-Q2-B, 2018-Q5-A; BC-MCQ-PE2012-044 |
| polar-area | BC-QA-09014 Area of a polar region found before the polar area integral is taught | no_calculator | I-A shape, served as an opener | none | BC-PT-99048 | none |

The 2018 records carry 0 points in the evidence index because no 2018 scoring guideline is in the corpus (BC-QA-99003 `scoring_pattern`, frq-18:6). The FRQ records BC-FRQ-2019-Q2-B and BC-FRQ-2026-Q2-C, 2026-Q2-D are secondary Unit 9 parts scored under BC-QA-08001, BC-QA-05007 and BC-QA-06007 (research/units/unit-09-parametric-polar-vector.md#Official evidence index [verified]).

### The planar-motion question (Q2 shape) and the points it scores

What each point is for, from the archetype `scoring_pattern` and the BC-PT `earns` fields.

- Acceleration vector (BC-QA-09004). One point per component with its setup, BC-PT-99052: each component obtained by differentiating the matching velocity component and evaluating at the time. An unsupported correct vector earns one of the two points; a variable expression equated to a number earns one of the two; degree mode work loses the first point it would have earned (sg-23:5, sg-23:6). Separate components must be labelled (BC-PT-99064; research/scoring/notation-requirements.md#Labels).
- Speed (BC-QA-09006). Setup point BC-PT-99050, the square root of the sum of squares of the two component derivatives with the setup visible, then answer point BC-PT-99004. The words "speed equals" and the value do not earn the setup; a bare time earns neither; a parenthesis error in a squared component costs the setup point but not the answer point (sg-23:6, sg-24:5).
- Distance travelled (BC-QA-09007, BC-QA-09003). Setup point BC-PT-99051, a definite integral of the square root of the sum of the squares of the component derivatives, then the value. An incorrect speed imported from an earlier part earns the integral point and loses the answer point; an unsupported correct value earns neither (sg-23:8, sg-24:6).
- Position from velocity (BC-QA-09005). Three points: the definite integral (BC-PT-99001), the use of the initial condition (BC-PT-99033, the known value added to the integral), and the answer. Several arrangements of the subtraction and limits earn the first two (sg-24:7). A missing differential can keep the integral point and block the answer point when the expression is also equated to a value (sg-23:8; research/scoring/notation-requirements.md#The differential is normally optional).
- Slope of the path (BC-QA-09001). One point, earned only when the response communicates dy/dx as dy/dt divided by dx/dt (BC-PT-99049); labelled values of the two derivatives followed by the slope earn it, and a declared incorrect component from an earlier part is accepted (sg-23:7).
- Direction toward an axis (BC-QA-09008). One point for considering the sign of the relevant velocity component (BC-PT-99014), one for the answer with the reason (BC-PT-99010); the interval may be open, closed or half open (sg-24:8).

### The polar parts and the points they score

- Area of one region (BC-QA-09012) and between two curves (BC-QA-09013). First point: a definite integral containing the square of r (BC-PT-99048), with or without the differential; second point: the full correct integrand (BC-PT-99002 or BC-PT-99001); the limits and the factor of one half are assessed in the answer point. Unclear communication between the correct integral and the correct value is scratch work; a symmetry presentation earned all three points (sg-25:7, sg-25:8).
- dr/dtheta (BC-QA-09009). One point, earned when the response indicates differentiation of r and gives the value; exact and decimal forms both earn it (sg-25:6, sg-25:7).
- Rate of distance from the origin in time (BC-QA-09010). One point for the chain rule product (dr/dtheta times dtheta/dt), one for the value (sg-25:10).
- Farthest point from an axis (BC-QA-09011). Three points: the derivative of the coordinate set equal to zero (BC-PT-99013), a global justification (BC-PT-99011), the answer with work; a local argument loses the justification point and keeps the answer available (sg-25:8, sg-25:9).
- Tangent relation in polar form (BC-QA-99001). One point for the relation among the three Leibniz derivatives, one for substituting the supplied slope, one for the value (sg-26:7).

### The three-decimal, calculator-setup and units points

- Three decimals. A decimal answer must be accurate to three places after the decimal point, rounded or truncated; within one free-response question at most one point is lost for inappropriate rounding (research/exam/calculator-policy.md#Rounding and reporting). Fewer than three places, or an intermediate value rounded before reuse, is BC-ERR-99019 (research/scoring/common-point-losses.md#Answer points), and a decimal error carried through several parts of one response is named separately (research/scoring/common-point-losses.md#Precision and presentation points).
- Calculator setup. A result from one of the four required capabilities (graph, solve, numerical derivative, numerical integral) must be shown with the setup: the equation being solved or the derivative or integral being evaluated (research/exam/calculator-policy.md#The setup-plus-result rule). No setup before a numerical answer is BC-ERR-99021 (research/scoring/common-point-losses.md#Setup points). Every Q2 part is calculator active, so this rule governs the whole slot.
- Units. Scored only where the prompt asks; not read otherwise (research/scoring/notation-requirements.md#What notation never costs). Missing units where asked is BC-ERR-99005 (research/scoring/common-point-losses.md#Units points). BC-QA-09005's `expected_solution_path` ends "report with units", and BC-QA-09007's `difficulty_variables` include "whether units are demanded".
- Radian mode. Degree mode work loses the first point it would otherwise have earned (BC-ERR-09023, sg-23:6, sg-23:7).

## 3. Cross-concept patterns

### Which concepts the stems combine

Computed from the archetypes' `skills` mapped to concepts.

- BC-QA-09005 joins BC-CON-09005, 09007, 09008 and 09010 (vector notation, component integration, initial position, coordinate at a time); the 2023 and 2022 records add Unit 6 accumulation (BC-SKL-06037) and 2021 adds Unit 5 extremum skills.
- BC-QA-09004 joins BC-CON-09005, 09006 and 09009 (notation, component derivative, acceleration with setup).
- BC-QA-09001 joins BC-CON-09001 and 09002; BC-QA-99001 joins BC-CON-09002 and 09014 with BC-SKL-03002.
- BC-QA-09007 joins BC-CON-09004 and 09010: the distance integral is the arc length integral in time (edge note on BC-SKL-09011 to BC-SKL-09025).
- BC-QA-09009, 99002 and 99003 each join BC-CON-09012, 09013 and 09014; BC-QA-99005 joins BC-CON-09012, 09013 and 09006 (polar path to vectors).
- BC-QA-09013 joins BC-CON-09016 and 09017; BC-QA-09012 is BC-CON-09015 alone.
- Across the Q2 slot, one question strings four to five of these shapes in sequence: acceleration, speed or a speed time, a coordinate from an initial position, total distance, direction (research/units/unit-09-parametric-polar-vector.md#Assessment behaviour under 9.6; frq-23:4, frq-24:4), or polar derivative, area, farthest point, rate in time (research/units/unit-09-parametric-polar-vector.md#Assessment behaviour under 9.7). An earlier declared value can be imported into a later part (sg-23:7, sg-23:8).

### Recognition features between neighbouring concepts, and the first written line

The rival column is the `confusable_with` field on the snapshot skills; the separating feature and first line are from the archetype and error records.

| Neighbours | What in the stem selects each | First written line | Source |
|---|---|---|---|
| dy/dx for a parametric curve against dy/dt (BC-SKL-09002 against BC-SKL-09001; BC-SKL-09002 lists BC-SKL-09005, 09006 as confusable) | "Slope of the line tangent to the path" selects the quotient; "rate of change of y" or the vertical velocity selects dy/dt alone | \(\frac{dy}{dx}=\frac{dy/dt}{dx/dt}\) with both derivatives labelled at the time | BC-QA-09001 `scoring_pattern` (sg-23:7); BC-ERR-09002, BC-ERR-09003, BC-ERR-09004; BC-MIS-09002, BC-MIS-09003 |
| First against second parametric derivative (BC-SKL-09008 lists BC-SKL-09002) | "d²y/dx²" or "concave" | \(\frac{d}{dt}\left(\frac{dy}{dx}\right)\) written, then divided by \(\frac{dx}{dt}\) | BC-EK-CHA-3G3 (ced:172); BC-QA-09002 `wrong_approaches`; BC-ERR-09009, BC-ERR-09010; BC-MIS-09004 |
| Horizontal against vertical tangent (BC-SKL-09006) | Horizontal: dy/dt = 0 with dx/dt ≠ 0; vertical: dx/dt = 0 with dy/dt ≠ 0 | the component derivative set to 0, and the other checked nonzero | BC-SKL-09003, BC-SKL-09006; BC-ERR-03012, BC-ERR-09005 |
| Speed against velocity vector (BC-CON-09009 against BC-CON-09006; BC-SKL-09023 lists BC-SKL-09011) | "Speed" asks for one number, the magnitude; "velocity vector" or "acceleration vector" asks for an ordered pair | Speed: \(\sqrt{(x'(t))^2+(y'(t))^2}\). Vector: \(\langle x'(t), y'(t)\rangle\) with components labelled or in order | BC-QA-09006, BC-QA-09004; BC-ERR-09013, BC-ERR-09014, BC-ERR-09017; BC-MIS-09005, BC-MIS-09011 |
| Distance travelled against displacement in the plane (BC-SKL-09025 lists BC-SKL-09020) | "Total distance travelled" selects the integral of speed; "displacement", "change in position" or a position at a later time selects the integral of each velocity component | Distance: \(\int_a^b\sqrt{(x')^2+(y')^2}\,dt\). Displacement: \(\langle\int_a^b x'(t)\,dt,\int_a^b y'(t)\,dt\rangle\) | BC-EK-FUN-8B2 (ced:176); BC-QA-09007 `wrong_approaches` (integrating the components and then taking a magnitude); BC-ERR-99010; BC-MIS-08004 |
| Position from velocity with an initial condition against displacement alone (BC-SKL-09021, 09026 against BC-SKL-09020) | A known position at one time and a request for the coordinate at another time | \(x(b)=x(a)+\int_a^b x'(t)\,dt\); backwards in time when the known time is later: \(x(a)=x(b)-\int_a^b x'(t)\,dt\) | BC-QA-09005 `expected_solution_path`, `wrong_approaches`; BC-ERR-08011, BC-ERR-09021; BC-MIS-09010 |
| Direction toward an axis against sign of position (BC-SKL-09027 lists BC-SKL-09016, 09021) | "Moving toward the y-axis" asks for the sign of the rate relative to the sign of the coordinate | the sign of the coordinate on the interval stated, then where the matching velocity component is 0 | BC-QA-09008 `expected_solution_path`; BC-ERR-09025, BC-ERR-09026; BC-MIS-09012 |
| Arc length against distance (BC-SKL-09013 lists BC-SKL-09025) | Same integral; a curve with a parameter asks for "length", a particle with time asks for "distance travelled" | the radical integrand inside a definite integral over the stated interval | BC-EK-CHA-6B1 (ced:173); research/units/unit-09-parametric-polar-vector.md#Required mathematical knowledge under 9.3 |
| Polar derivative dr/dtheta against dy/dx (BC-SKL-09030 lists BC-SKL-09002, 09004; BC-SKL-09033 lists BC-SKL-09031) | "Rate of change of r" or "distance from the origin" selects dr/dθ; "slope of the tangent line" selects dy/dx through x = r cos θ, y = r sin θ | dr/dθ: \(r'(\theta)\) at the angle, differentiation indicated. dy/dx: \(x=r\cos\theta\), \(y=r\sin\theta\), then \(\frac{dy/d\theta}{dx/d\theta}\) | BC-QA-09009 `difficulty_variables`; BC-QA-99003; BC-ERR-09028, BC-ERR-09031, BC-ERR-09032; BC-MIS-09014, BC-MIS-09015 |
| dr/dθ against dr/dt (BC-SKL-09032 lists BC-SKL-09033, 09024) | A stated rate dθ/dt and a request for a rate in time | \(\frac{dr}{dt}=\frac{dr}{d\theta}\cdot\frac{d\theta}{dt}\) | BC-QA-09010; BC-ERR-09030 |
| Radius against a Cartesian coordinate (BC-SKL-09029 lists BC-SKL-09001, 09002) | "Distance from the x-axis" or "y-coordinate" asks for \(r\sin\theta\), not r | \(y=r(\theta)\sin\theta\) | BC-QA-09011, BC-QA-99004 `wrong_approaches`; BC-ERR-09027; BC-MIS-09013 |
| Polar area of one region against area between two curves (BC-SKL-09035 lists BC-SKL-09040) | One curve and the rays that bound it, or one loop, against "inside one curve and outside another" | One region: \(\frac12\int_\alpha^\beta r^2\,d\theta\). Between two: the intersection angles first, then \(\frac12\int_\alpha^\beta (R^2-r^2)\,d\theta\) with R the outer radius | BC-QA-09012, BC-QA-09013 `expected_solution_path` and `wrong_approaches` (squaring the difference); BC-ERR-09035, 09036, 09040, 09039; BC-MIS-09017, BC-MIS-09018 |
| A curve traced more than once (BC-SKL-09014, 09037 list each other and BC-SKL-09036, 09039) | A loop or a length where the parameter interval could revisit points already passed | the angle or parameter interval that traces the loop or curve exactly once, stated before the integral | BC-QA-09003, BC-QA-09012 `wrong_approaches`; BC-ERR-09016, BC-ERR-09037; BC-MIS-09007, BC-MIS-09019; research/units/unit-09-parametric-polar-vector.md#Required mathematical knowledge under 9.3 (Tracing) |
| Intersection angles against the full interval of the figure (BC-SKL-09039 lists BC-SKL-09036) | Two curves drawn, a region between them | the two radii set equal and solved for the bounding angles | BC-QA-09013 `expected_solution_path`; BC-ERR-09038; BC-MIS-09019 |

## 4. Recurring traps

Computed: an active BC-ERR or BC-MIS whose `skills` meet the skills of two or more Unit 9 concepts. Scoring consequences are the record text.

| Record | Concepts | Scoring consequence (record) |
|---|---|---|
| BC-ERR-99019 Decimal presentation error or premature rounding | 09002, 09003, 09004, 09006, 09013, 09015, 09016 | The answer point is not earned; the report notes this recurs across several parts of the same response. |
| BC-ERR-99021 Calculator setup not shown before a numerical answer | 09003, 09004, 09006, 09009, 09015 | The setup point is not earned, and an unsupported answer generally receives no credit in a multi point part. |
| BC-ERR-99002 Linkage error equating a variable expression with a numerical value | 09006, 09009, 09010, 09016 | The presentation point or the setup point is lost, and in some parts the response becomes ineligible for later points in that part. |
| BC-ERR-99029 Parametric and vector motion quantity set up incorrectly | 09002, 09004, 09006, 09011 | The setup point for the requested quantity is lost, and the answer point follows it. |
| BC-ERR-99031 Polar area and polar motion setup incorrect | 09013, 09014, 09015, 09016 | The integrand point is lost when the square is missing, and later points in the part are typically unreachable. |
| BC-ERR-99010 Displacement reported where total distance was asked | 09004, 09007, 09010 | The setup point for total distance is not earned; the numerical answer point follows the setup. |
| BC-ERR-08011 Initial value not added to the accumulated change | 09008, 09010 | The initial condition point is lost and the answer point falls with it (sg-24:7). |
| BC-ERR-09013 Component rates added instead of combined as a magnitude | 09004, 09009 | The setup point is lost. |
| BC-ERR-09014 Parentheses lost inside a squared component | 09004, 09009 | The setup point is lost while the answer point remains available, and the same error is not assessed again in a later part (sg-23:6, sg-23:8). |
| BC-ERR-09016 Integration over an interval that traces the curve more than once | 09004, 09015 | The reported value is a multiple of the correct one and the answer point is lost. |
| BC-ERR-09017 Vector components presented without labels or in the wrong order | 09005, 09006 | The guideline accepts separate components only when they are labelled, so an unlabelled pair can lose a point (sg-23:6). |
| BC-ERR-09023 Calculator work performed in degree mode | 09009, 09013 | The response does not earn the first point it would otherwise have earned and is generally eligible for the rest (sg-23:6, sg-23:7). |
| BC-ERR-09035 Factor of one half omitted from a polar area integral | 09015, 09016 | The value is twice the area, so the answer point is lost; the factor is assessed with the limits (sg-25:7). |
| BC-ERR-09037 Polar limits taken from the wrong angles | 09015, 09017 | The answer point is lost, since the limits are assessed there (sg-25:7). |
| BC-ERR-09039 Inner and outer polar radii exchanged | 09013, 09016 | A negative area is produced and the integrand point is lost. |

Misconceptions across two or more concepts (severity from the record): BC-MIS-08004 distance travelled and net change in position are the same (09004, 09007, 09010; high); BC-MIS-09008 a calculator result stands without its expression (09004, 09009, 09015; medium); BC-MIS-09001 the parameter is the horizontal coordinate (09001, 09002; high); BC-MIS-09005 a length in the plane is the sum of the two component contributions (09004, 09009; high); BC-MIS-09007 any interval containing the curve gives its length or area (09004, 09015; medium); BC-MIS-09009 a vector answer is a pair of numbers with no structure (09006, 09007; medium); BC-MIS-09010 the integral of a velocity component is the coordinate (09008, 09010; high); BC-MIS-09013 the polar radius is a Cartesian coordinate (09012, 09014; high); BC-MIS-09019 the limits of a polar area are the whole interval of the figure (09015, 09017; high). BC-MIS-06010 (a relative extremum test settles an absolute extremum; high) reaches BC-CON-09014 through BC-SKL-09034 as the successor of the retired BC-MIS-09016.

Point losses research/scoring names for this unit's shapes:

- (research/scoring/common-point-losses.md#Setup points): no calculator setup before a numerical answer (BC-ERR-99021; cr-23:7, cr-24:4, cr-24:28, crabbc-25:30); displacement setup where total distance was asked (BC-ERR-99010; cr-23:8, cr-24:8); a parametric or vector quantity assembled from the wrong derivatives, including an inverted slope quotient and a separated distance integral (BC-ERR-99029; cr-23:27, cr-24:27); a polar area integrand without the square, or limits that do not match the intersection angles (BC-ERR-99031; crabbc-25:29, crabbc-25:30).
- (research/scoring/common-point-losses.md#Answer points): fewer than three digits after the decimal, or an intermediate value rounded before reuse (BC-ERR-99019; cr-23:27, cr-24:26, crabbc-25:30).
- (research/scoring/common-point-losses.md#Units points): units missing where the prompt asks (BC-ERR-99005; cr-23:7).
- (research/scoring/common-point-losses.md#Justification points): a local sign change where a global argument or complete candidates test was required (BC-ERR-99004; crabbc-25:30), the farthest-point shape of BC-QA-09011.
- (research/scoring/common-point-losses.md#Notation points): a variable expression equated to a numerical value (BC-ERR-99002; cr-24:8, cr-24:27); parentheses omitted when a given expression replaces a named function (BC-ERR-99009).
- (research/scoring/common-point-losses.md#Precision and presentation points): a decimal presentation error carried through several parts of one response (BC-ERR-99019; cr-24:26, crabbc-25:30).
- (research/scoring/notation-requirements.md#Labels): vector components listed separately must be labelled; reversed components lose both points (sg-23:6, sg-22:7). (research/scoring/notation-requirements.md#Parentheses): a parenthesis error in a speed component costs the setup point once and is not reassessed later (sg-23:6, sg-23:8). (research/scoring/notation-requirements.md#The equal sign): an equated expression costs one of two acceleration points in 2023 (sg-23:6), while in 2025 unclear communication between a correct polar integral and a correct value is scratch work (sg-25:3, sg-25:8); whether this is a durable change is unresolved (research/units/unit-09-parametric-polar-vector.md#Unresolved).

The five highest severity clusters the unit research ties to scoring guidelines: speed as a component or sum rather than a magnitude (sg-24:5), the integral of a velocity component reported as a coordinate (sg-24:7), direction read from the position rather than its rate (sg-24:8), a local argument for a farthest point (sg-25:9), and the polar area without the square and the factor of one half (sg-25:7) (research/units/unit-09-parametric-polar-vector.md#Misconception summary).

## 5. Time budgets per archetype shape

MCQ budgets are the part figures. An FRQ part's budget is its share of 15.0 minutes by points out of 9 (1.67 minutes per point), per plan 15 (docs/plan/15-lessons.md, Fluency, measured and never credited); point counts come from `scoring_pattern` and the evidence index. "Writes" names the steps that carry a point; "held" names steps with no point of their own. Which steps a fluent solver holds is [inferred] from where the points sit; settled by per-step timing once 10's fluency telemetry exists.

| Shape | MCQ budget | FRQ points and budget | A fluent solver writes | Held |
|---|---|---|---|---|
| BC-QA-09001 parametric slope | I-B 2.92 (I-A 2.14 for its no-calculator MCQs) | 1 = 1.67 (2 = 3.33 in 2015) | dy/dt and dx/dt labelled at the time, the quotient, the value to three places | the calculator derivatives |
| BC-QA-09002 parametric second derivative | I-A 2.14 or I-B 2.92 | none observed; setup and answer [inferred 2 = 3.33, settled by a scoring guideline for this shape] | d/dt of dy/dx, the division by dx/dt, the value or sign | simplifying dy/dx |
| BC-QA-09003 parametric length | I-B 2.92 | 2 = 3.33 | the definite integral of the radical with limits, the value | squaring each rate |
| BC-QA-09004 acceleration vector | I-B 2.92 | 2 = 3.33 (3 = 5.0 in 2022) | each component as the derivative of velocity at the time, labelled; the vector | the numerical derivative keystrokes |
| BC-QA-09005 coordinate from initial position | I-B 2.92 | 3 = 5.0 | \(x(b)=x(a)+\int_a^b x'(t)\,dt\), the value | the direction of accumulation |
| BC-QA-09006 speed | I-B 2.92 | 2 = 3.33 | the magnitude expression set equal or evaluated, the value or time | the squaring |
| BC-QA-09007 distance travelled | I-B 2.92 | 2 = 3.33 | the integral of speed with limits, the value with units where asked | an imported speed expression |
| BC-QA-09008 direction toward an axis | I-B 2.92 | 2 = 3.33 | the sign of the coordinate, the zero of the velocity component, the interval with the reason | locating the zero on the calculator |
| BC-QA-09009 dr/dθ | I-B 2.92 | 1 = 1.67 | r'(θ) indicated and the value | nothing further |
| BC-QA-09010 rate from the origin in time | I-B 2.92 | 2 = 3.33 | dr/dθ times dθ/dt, the value | the imported dr/dθ |
| BC-QA-09011 farthest point from an axis | I-B 2.92 | 3 = 5.0 | the coordinate in θ, its derivative set to 0, the candidates table with both endpoints, the angle | solving on the calculator |
| BC-QA-09012 area of one region | I-A 2.14 or I-B 2.92 | 2 = 3.33 (3 = 5.0 in 2019-Q2-C) | the bounding angles, \(\frac12\int r^2\,d\theta\), the value | the zeros of r |
| BC-QA-09013 area between two curves | I-B 2.92 | 3 = 5.0 | the intersection angles, \(\frac12\int(R^2-r^2)\,d\theta\), the value | which curve is outer |
| BC-QA-09014 opener | I-A 2.14 | not scored (opener) | the sector area \(\frac12 r^2\Delta\theta\), the integral, the exact value | the cutting into sectors |
| BC-QA-99001 polar tangent relation | I-B 2.92 | 3 = 5.0 | the relation among dy/dθ, dx/dθ, dy/dx, the substitution, the value | the rearrangement |
| BC-QA-99002 dx/dθ or dy/dθ | I-B 2.92 | 2 = 3.33 | \(y=r\sin\theta\) displayed, its derivative, the value | the product rule terms |
| BC-QA-99003 polar slope | I-A 2.14 | none recorded (no 2018 guideline) | x and y in θ, both derivatives, the quotient | the evaluation |
| BC-QA-99004 time a coordinate reaches a value | I-B 2.92 | 3 = 5.0 | the coordinate in θ or t, the equation set to the value, the time | the numerical solve |
| BC-QA-99005 position and velocity on a polar path | I-B 2.92 | 3 = 5.0 | both coordinates in t as an ordered pair, the velocity at the time | the substitution θ(t) |
| BC-QA-99006 rate of the gap between two curves | I-B 2.92 | 2 = 3.33 | the difference of radii displayed, its derivative at the angle | which radius is larger |

## 6. Delivery map

TEMPLATE selection rules (docs/lessons/TEMPLATE.md, Delivery): 1 worked examples and error blocks are `step_reveal`; 2 a key idea describing a process (a limit being taken, a partition refining, terms accumulating, a curve being traced) is `motion`, with `model` on the example only where a computed sequence of values is the idea; 3 figure-bearing BC-REP (02, 07, 08, 12, 13, 14) gives `figure`, promoted to `interactive` when `common_givens` or `difficulty_variables` name a varying quantity and the stem asks for a reading; 4 BC-REP-03 givens give `table`; 5 everything else is `text`.

Every Unit 9 skill carries BC-REP-12 (Parametric equations), BC-REP-13 (Polar equation) or BC-REP-14 (Vector-valued function), so rule 3 fires for every orientation and no orientation falls to rule 5. No Unit 9 skill or archetype carries BC-REP-03, so rule 4 never fires. Key ideas below are named by their topic's BC-EK (research/units/unit-09-parametric-polar-vector.md, Official mapping under each topic).

| Concept | Orientation | Key ideas (BC-EK) and mode | Rule and triggering field |
|---|---|---|---|
| BC-CON-09001 | figure | CHA-3G1 `motion` (a particle tracing the parametric curve as t advances, x(t) and y(t) read off at each frame) | rule 3, BC-REP-12 on BC-SKL-09001; rule 2, the idea is a curve being traced; BC-MIS-09001 (parameter taken as x) is what the frames separate |
| BC-CON-09002 | figure | CHA-3G2 `interactive` (one draggable point on the curve, parameter t as the control, the velocity vector and tangent line drawn at the point, dy/dt, dx/dt and their quotient shown; reading: the slope and where dx/dt = 0 makes the tangent vertical) | rule 3 promoted: BC-REP-12 on BC-SKL-09002 to 09006; BC-QA-09001 `common_givens` "a time", stem asks for the slope at that time |
| BC-CON-09003 | figure | CHA-3G3 figure (the curve with its concave up and concave down arcs labelled with the sign of d²y/dx²) | rule 3, BC-REP-12 on BC-SKL-09007 to 09010; not promoted, BC-QA-09002 `difficulty_variables` vary a form (simplification, value or sign) |
| BC-CON-09004 | figure | CHA-6B1 figure (the path with the stated interval marked); the tracing paragraph `motion` (the curve traced over a parameter interval that revisits an arc, the retraced arc highlighted on the second pass) | rule 3, BC-REP-12 on BC-SKL-09011 to 09014; rule 2, "a parameter interval that traces part of the curve twice" (research/units/unit-09-parametric-polar-vector.md#Required mathematical knowledge under 9.3) is a curve being traced; BC-QA-09003 `difficulty_variables` "whether the interval traces the curve once" |
| BC-CON-09005 | figure | CHA-3H1 figure (the position vector from the origin to the point, labelled with the pair and the vector notation) | rule 3, BC-REP-12 and BC-REP-14 on BC-SKL-09018; not promoted, the skill is a notation conversion |
| BC-CON-09006 | figure | CHA-3H1 `interactive` (one draggable time on the path, velocity and acceleration vectors drawn from the point, components labelled; reading: the components at the time) | rule 3 promoted: BC-REP-14 on BC-SKL-09015 to 09017; BC-QA-09004 `common_givens` "a time", stem asks for the vector at that time |
| BC-CON-09007 | figure | FUN-8A1 figure (the displacement vector between two positions, components as the two integrals) | rule 3, BC-REP-14 on BC-SKL-09019, 09020; not promoted, the stem asks for a value, not a reading |
| BC-CON-09008 | figure | FUN-8B2 figure (the known position marked, the displacement arrow forward or backward in time to the requested position) | rule 3, BC-REP-14 on BC-SKL-09021, 09022; not promoted: BC-QA-09005 `difficulty_variables` "whether the requested time is before or after the known time" is a form of the stem, and the stem asks for a coordinate value |
| BC-CON-09009 | figure | FUN-8B1 `interactive` (one draggable time, the velocity vector with its components as the legs and its length as the speed; reading: the time at which the speed has a stated value) | rule 3 promoted: BC-REP-14 on BC-SKL-09023, 09024, 09028; BC-QA-09006 `common_givens` "a time or a target speed", `difficulty_variables` "whether a value or a time is requested" |
| BC-CON-09010 | figure | FUN-8B2 `motion` (the particle traces the path while the distance travelled accumulates beside the displacement; on a path that returns to its start the two readings separate) | rule 3, BC-REP-14 on BC-SKL-09025, 09026; rule 2, distance accumulating along a traced path; BC-MIS-08004's probe is a particle that returns to its start (research/units/unit-09-parametric-polar-vector.md#Misconception summary, under BC-MIS-09006) |
| BC-CON-09011 | figure | FUN-8B1 `interactive` (one draggable time; the sign of the coordinate and the sign of its velocity component shown with the particle's approach to the axis; reading: toward or away) | rule 3 promoted: BC-REP-14 on BC-SKL-09027; BC-QA-09008 `common_givens` "a velocity component", "an interval", stem asks for a sign argument |
| BC-CON-09012 | figure | FUN-3G2 figure (a point at angle θ and distance r, with x = r cos θ and y = r sin θ as the legs) | rule 3, BC-REP-13 on BC-SKL-09029; not promoted, the conversion is a single evaluation |
| BC-CON-09013 | figure | FUN-3G1 and FUN-3G2 `interactive` (the polar angle dragged along the curve with r read off at each angle and the sign of dr/dθ shown as the distance from the pole growing or shrinking; reading: what dr/dθ says about the distance from the origin) | rule 3 promoted: BC-REP-13 on BC-SKL-09030 to 09032; BC-QA-09009 `common_givens` "an angle", `difficulty_variables` "whether the interpretation as a rate of distance from the origin is demanded" |
| BC-CON-09014 | figure | FUN-3G2 figure (the tangent line at a point on the polar curve beside the radial segment, dy/dx against dr/dθ labelled); the farthest-point idea figure (candidates at the critical angle and both endpoints marked) | rule 3, BC-REP-13 on BC-SKL-09033, 09034, BC-REP-02 on BC-QA-09011; not promoted, the stem asks for a slope value or a justified angle |
| BC-CON-09015 | figure | CHA-5D1 `motion` (the polar curve swept as θ advances, each thin sector filling the area as it is swept); example 1 `model` (sums of sector areas \(\frac12 r^2\Delta\theta\) at a growing number of sectors, shown as a table beside the figure, approaching the integral) | rule 3, BC-REP-13 and BC-REP-02 on BC-SKL-09036, 09037; rule 2, a region swept by rays; `model` because BC-CON-09015 is a productive-failure target (`PRODUCTIVE_FAILURE_TARGETS`, app/engine/constants.py) through BC-QA-09014 (BC-DF-15), whose `expected_solution_path` begins "cut the region into thin sectors by rays from the pole" |
| BC-CON-09017 | figure | CHA-5D2 figure (the two curves with the intersection rays drawn and the angles labelled) | rule 3, BC-REP-13 on BC-SKL-09039; not promoted, the stem asks for angles, found by solving |
| BC-CON-09016 | figure | CHA-5D2 figure (the region inside one curve and outside the other shaded, outer radius R and inner radius r labelled on one ray) | rule 3, BC-REP-13 and BC-REP-02 on BC-SKL-09040; not promoted: BC-QA-09013 `difficulty_variables` name properties (a circle of constant radius, exact or decimal angles, the outer curve changing), not a varying quantity |

Where each mode fits, in summary:

- Motion: a particle tracing a parametric curve as t advances (LSN-CON-09001); a parameter interval that retraces an arc (LSN-CON-09004); distance accumulating against displacement along a traced path (LSN-CON-09010); a polar curve swept as θ advances with the area sectors filling (LSN-CON-09015). Every motion entry carries `reduced_motion` behaviour and a static fallback of frames side by side (TEMPLATE, Delivery).
- Model: the sector sums of the productive-failure example of LSN-CON-09015 only.
- Interactive: a point on a parametric curve with its velocity vector and tangent (LSN-CON-09002); velocity and acceleration vectors at a dragged time (LSN-CON-09006); the velocity vector's length as speed (LSN-CON-09009); signs of coordinate and rate against the approach to an axis (LSN-CON-09011); the polar angle dragged with r read off (LSN-CON-09013). One control per screen [inferred, per TEMPLATE]. Five interactives in one unit share one pattern (a single time or angle control on a declarative curve), so one spec shape can serve all five [inferred; settled by the spec review of the first two built].
- A static figure is enough: the concavity arcs (09003), vector notation (09005), displacement between two positions (09007), the initial-position arrow (09008), polar to Cartesian legs (09012), tangent against radial segment and the candidates (09014), intersection rays (09017), and the shaded region between two curves (09016).
- Text and step reveal: every worked example and every error block in the unit is `step_reveal` (rule 1), and those carry the written lines the Q2 points score (the quotient, the magnitude, the initial condition plus the integral, one half the integral of r squared). No orientation or key idea falls to rule 5, because every Unit 9 skill carries a figure-bearing BC-REP. For BC-CON-09003, 09005 and 09007 the rule 3 figure adds little beyond the notation; whether a BC-REP-12 or 14 trigger with no plotted curve in the stem should fall to `text` is a TEMPLATE question [inferred; settled by a TEMPLATE ruling on whether BC-REP-12, 13 and 14 are figure-bearing when the archetype's `common_givens` supply no figure].

## Library gaps met

- The hard edge BC-SKL-09019 (antidifferentiate a vector-valued function) to BC-SKL-09029 (convert a polar point to Cartesian coordinates) carries a note about parametric representation, which fits BC-SKL-09001 or BC-SKL-09018 as the parent. As recorded, it places BC-CON-09012 and the whole polar strand after vector integration.
- Concept `misconceptions` list a retired id: BC-CON-09010 names BC-MIS-09006, retired with `superseded_by` BC-MIS-08004 (data/ids.json). BC-MIS-09016 is retired to BC-MIS-06010 and no concept lists either.
- BC-QA-09002, BC-QA-09003 and BC-QA-99003 carry no `point_types`, so their lessons carry no scoring section; BC-QA-09003's `scoring_pattern` names an integral point and a value point that BC-PT-99051 and BC-PT-99004 would fit, as on BC-QA-09007.
- BC-QA-09003 lists no official examples although the Q2 distance records (BC-FRQ-2015-Q2-D, 2021-Q2-B, 2022-Q2-D) load all four of its skills; they are filed under BC-QA-09007.
- BC-QA-09002 has no free-response part in the corpus; its scoring pattern is inferred from sg-23:7 (research/units/unit-09-parametric-polar-vector.md#Unresolved).
- The seven polar `archetype_gap` records (BC-FRQ-2013-Q2-B, 2013-Q2-C, 2014-Q2-B, 2014-Q2-C, 2018-Q5-B, 2026-Q2-B, 2019-Q2-B) are noted in research as candidates (research/question-analysis/frq-analysis.md#Archetype gaps recorded in the notes [inferred]); BC-QA-99001 to 99006 now cover six of them, and the polar average value part (BC-FRQ-2019-Q2-B) stays under BC-QA-08001.
- No 2018 scoring guideline is in the corpus, so the four 2018 Unit 9 records carry 0 points.
- Misconception literature for this unit could not be confirmed from the cache; causes are inferred from scoring guidelines (research/units/unit-09-parametric-polar-vector.md#Unresolved).

## 7. Sources

- Concepts: BC-CON-09001 to BC-CON-09017. Skills: BC-SKL-09001 to BC-SKL-09043. Outside parents: BC-SKL-02036, BC-SKL-02039, BC-SKL-03002, BC-SKL-03006, BC-SKL-05028, BC-SKL-05030, BC-SKL-06028, BC-SKL-06034, BC-SKL-06037, BC-SKL-06047, BC-SKL-07032, BC-SKL-08006, BC-SKL-08007, BC-SKL-08009, BC-SKL-08018, BC-SKL-08019, BC-SKL-08051, BC-SKL-08056, BC-SKL-08059.
- BC-PRQ-06005, BC-PRQ-08001, BC-PRQ-08006, BC-PRQ-08007, BC-PRQ-09001, BC-PRQ-09002, BC-PRQ-09003, BC-PRQ-09004.
- Topics: BC-TOP-0901 to BC-TOP-0909. Unit: BC-UNIT-09.
- Archetypes: BC-QA-09001 to BC-QA-09014, BC-QA-99001 to BC-QA-99006; secondary: BC-QA-08001, BC-QA-05007, BC-QA-06007.
- Point types: BC-PT-99001, 99002, 99004, 99005, 99010, 99011, 99013, 99014, 99033, 99048, 99049, 99050, 99051, 99052, 99064, 99068.
- Errors: BC-ERR-03012, BC-ERR-05028, BC-ERR-08011, BC-ERR-09001 to 09005, 09007, 09009, 09010, 09012 to 09014, 09016, 09017, 09019, 09021 to 09041 (as listed in sections 3 and 4), BC-ERR-99002, 99004, 99005, 99009, 99010, 99019, 99021, 99029, 99031.
- Misconceptions: BC-MIS-06010, BC-MIS-08004, BC-MIS-09001 to 09005, 09007 to 09015, 09017 to 09019; retired BC-MIS-09006, BC-MIS-09016.
- Difficulty factors: BC-DF-15 (and BC-DF-13 as the second productive-failure factor). Representations: BC-REP-01, 02, 03, 04, 09, 12, 13, 14.
- Essential knowledge: BC-EK-CHA-3G1, 3G2, 3G3, BC-EK-CHA-6B1, BC-EK-CHA-3H1, BC-EK-FUN-8A1, BC-EK-FUN-8B1, 8B2, BC-EK-FUN-3G1, 3G2, BC-EK-CHA-5D1, 5D2.
- FRQ and MCQ records: BC-FRQ-2013-Q2-A to C, 2014-Q2-A to D, 2015-Q2-A to D, 2018-Q2-D, 2018-Q5-A to C, 2019-Q2-A to D, 2021-Q2-A to C, 2022-Q2-A to D, 2023-Q2-A to D, 2024-Q2-A to D, 2025-Q2-A to D, 2026-Q2-A to D; BC-MCQ-CED-018, BC-MCQ-CED-021, BC-MCQ-SAMPLE-017, BC-MCQ-SAMPLE-023, BC-MCQ-PE2012-002, BC-MCQ-PE2012-026, BC-MCQ-PE2012-044.
- CED pages: ced:171, ced:172, ced:173, ced:174, ced:175, ced:176, ced:177, ced:178, ced:179.
- Scoring guidelines and samples: sg-22:7, sg-23:5, sg-23:6, sg-23:7, sg-23:8, sg-24:5, sg-24:6, sg-24:7, sg-24:8, sg-25:3, sg-25:6, sg-25:7, sg-25:8, sg-25:9, sg-25:10, sg-26:7; samples-13-q2:1, samples-14-q2:1; frq-18:6, frq-23:4, frq-24:4.
- Chief reader reports: cr-23:7, cr-23:8, cr-23:27, cr-24:4, cr-24:8, cr-24:26, cr-24:27, cr-24:28, crabbc-25:29, crabbc-25:30.
- Research headings: research/units/unit-09-parametric-polar-vector.md#Unit 9, Parametric Equations, Polar Coordinates, and Vector-Valued Functions; #Required mathematical knowledge (under 9.3); #Assessment behaviour (under 9.6 and 9.7); #Misconception summary; #Unresolved; #Official evidence index [verified]. research/exam/exam-structure.md#Section and part layout; #Free-response point totals. research/exam/calculator-policy.md#The setup-plus-result rule; #Rounding and reporting. research/scoring/common-point-losses.md#Setup points; #Answer points; #Units points; #Justification points; #Notation points; #Precision and presentation points. research/scoring/notation-requirements.md#The differential is normally optional; #The equal sign; #Labels; #Parentheses; #What notation never costs. research/question-analysis/frq-analysis.md#The calculator questions and the no-calculator questions; #How concepts combine inside one question; #Archetype gaps recorded in the notes [inferred]. research/question-analysis/question-archetypes.md (Family arc-length, parametric-calculus, parametric-motion, polar-area, polar-calculus, polar-motion).
- Plan and code: docs/plan/15-lessons.md (What a lesson is, and its granularity; Methods, thought process and scoring habits; Fluency, measured and never credited; Pacing to the exam date); docs/lessons/TEMPLATE.md (Delivery); app/engine/constants.py (`PRODUCTIVE_FAILURE_TARGETS`, `PRODUCTIVE_FAILURE_FACTORS`); tools/check_lessons.py (`--sets`); tools/derive_confusable.py; data/ids.json.
- [inferred] claims and what settles them: which steps are held in the head (per-step timing from 10's fluency telemetry); the FRQ point count for BC-QA-09002 (a scoring guideline for that shape); the one-control rule and every non-text delivery mode (the modality A/B); one spec shape for the five interactives (spec review of the first two built); whether BC-REP-12, 13 and 14 trigger rule 3 when no figure is given (a TEMPLATE ruling).
