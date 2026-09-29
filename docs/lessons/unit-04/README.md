---
title: Unit 4 attack map, Contextual Applications of Differentiation
research_date: 2026-09-29
status: draft
purpose: The map every designer of the fifteen Unit 4 concept lessons (BC-CON-04001 to BC-CON-04015) reads before designing, giving the concept order along the prerequisite edges, the exam shapes the unit feeds, the cross-concept recognition features and the confusable set, the recurring traps, the time budgets and the delivery mode each concept's blocks take under docs/lessons/TEMPLATE.md, all computed from the library records and the research files.
---

# Unit 4 attack map, Contextual Applications of Differentiation

BC-UNIT-04 holds seven topics, BC-TOP-0401 to BC-TOP-0407 (ced:87 to ced:93), fifteen concepts, thirty eight skills (BC-SKL-04001 to BC-SKL-04038) and ten archetypes (BC-QA-04001 to BC-QA-04010). Topics 4.1 to 4.6 sit under CHA-3 and topic 4.7 under LIM-4 (research/units/unit-04-contextual-applications-differentiation.md#Unit 4, Contextual Applications of Differentiation, ced:84). Every number below was computed from the snapshot (`app.content.loader.load_snapshot`), data/prereq_edges.csv, data/errors.json and data/misconceptions.json on 2026-09-29, or is quoted from a research heading. Nothing here is a lesson design; each concept lesson carries its own design under docs/lessons/unit-04/LSN-CON-040nn.md.

## 1. Concept order along the prerequisite edges

Method. A topological order over the `hard_prerequisite` edges in data/prereq_edges.csv whose two ends are both Unit 4 skills (32 such edges), ties broken by skill id, with every parent outside the unit taken as already reached. A concept is placed where the fringe first reaches one of its skills. At concept level the hard edges contain two cycles, so no topological order over concepts exists: BC-CON-04002 and BC-CON-04006 (BC-SKL-04001 to BC-SKL-04013 to BC-SKL-04014) and BC-CON-04007 and BC-CON-04008 (BC-SKL-04017 to BC-SKL-04018 to BC-SKL-04019 to BC-SKL-04020). The skill order is acyclic and is the one used.

Skill order (38): 04001, 04002, 04003, 04004, 04005, 04006, 04007, 04008, 04009, 04010, 04011, 04012, 04013, 04014, 04015, 04016, 04017, 04018, 04019, 04020, 04021, 04022, 04026, 04027, 04023, 04024, 04025, 04032, 04028, 04029, 04030, 04031, 04033, 04034, 04035, 04036, 04037, 04038 (each prefixed BC-SKL-).

"Unit 4 parents" are the concepts holding a Unit 4 hard parent of one of the concept's skills. "Outside parents" are the hard parents outside the unit (BC-SKL or BC-TOP stand-ins), with supporting edges marked. BC-PRQ parents are all `supporting` edges.

| # | Concept | Name | Skills | Unit 4 parents | Outside parents | BC-PRQ parents |
|---|---|---|---|---|---|---|
| 1 | BC-CON-04002 | Units of a derivative | BC-SKL-04001, BC-SKL-04004, BC-SKL-04014 | BC-CON-04006 (BC-SKL-04013 to BC-SKL-04014) | BC-SKL-02012, BC-SKL-02018, BC-TOP-0201 | BC-PRQ-04004 |
| 2 | BC-CON-04001 | The derivative as an instantaneous rate of change in context | BC-SKL-04002, BC-SKL-04003, BC-SKL-04005 | BC-CON-04002 | BC-SKL-02003, BC-SKL-02010 | BC-PRQ-04004, BC-PRQ-04008 |
| 3 | BC-CON-04003 | Position, velocity, and acceleration on a line | BC-SKL-04006, BC-SKL-04007 | none | BC-SKL-02025, BC-TOP-0202 | BC-PRQ-04008 |
| 4 | BC-CON-04004 | Velocity, speed, and direction | BC-SKL-04008, BC-SKL-04009, BC-SKL-04011 | BC-CON-04002 (BC-SKL-04001), BC-CON-04003 | none | BC-PRQ-04005, BC-PRQ-04009 |
| 5 | BC-CON-04005 | Speeding up and slowing down | BC-SKL-04010, BC-SKL-04012 | BC-CON-04003, BC-CON-04004 | none | BC-PRQ-04005, BC-PRQ-04009 |
| 6 | BC-CON-04006 | The common structure of contextual rate problems | BC-SKL-04013, BC-SKL-04015, BC-SKL-04016 | BC-CON-04002 | BC-SKL-01060 | BC-PRQ-04008 |
| 7 | BC-CON-04007 | Variables in a related rates problem as functions of time | BC-SKL-04017, BC-SKL-04019, BC-SKL-04022 | BC-CON-04006 (BC-SKL-04013), BC-CON-04008 (BC-SKL-04018) | BC-SKL-03007, BC-TOP-0301, BC-TOP-0302 | BC-PRQ-04008 |
| 8 | BC-CON-04008 | The relating equation | BC-SKL-04018, BC-SKL-04020, BC-SKL-04021 | BC-CON-04007 | BC-TOP-0208, BC-TOP-0209 (supporting) | BC-PRQ-04001, BC-PRQ-04002, BC-PRQ-04003, BC-PRQ-04008 |
| 9 | BC-CON-04009 | Substitution after differentiation | BC-SKL-04023, BC-SKL-04026, BC-SKL-04027 | BC-CON-04007, BC-CON-04008 | none | BC-PRQ-04007, BC-PRQ-04008 |
| 10 | BC-CON-04010 | Interpreting a related rate in context | BC-SKL-04024, BC-SKL-04025 | BC-CON-04009 | none | BC-PRQ-04004, BC-PRQ-04007 |
| 11 | BC-CON-04011 | The tangent line as a local linear approximation | BC-SKL-04028, BC-SKL-04029, BC-SKL-04032 | none | BC-SKL-02012, BC-SKL-03012, BC-TOP-0302 (supporting) | BC-PRQ-04006 |
| 12 | BC-CON-04012 | Direction of the approximation error | BC-SKL-04030, BC-SKL-04031 | BC-CON-04011 | BC-SKL-02013, BC-TOP-0306 (supporting), BC-TOP-0506 (supporting) | BC-PRQ-04008 |
| 13 | BC-CON-04013 | Indeterminate form | BC-SKL-04033 | none (BC-CON-04014 supporting, through BC-SKL-04038) | BC-SKL-01029, BC-TOP-0102 | BC-PRQ-04008 |
| 14 | BC-CON-04014 | The hypothesis of L'Hospital's rule | BC-SKL-04034, BC-SKL-04038 | none (BC-CON-04013 supporting, through BC-SKL-04033) | BC-SKL-01058, BC-SKL-02035, BC-TOP-0111 | BC-PRQ-04008 |
| 15 | BC-CON-04015 | The conclusion of L'Hospital's rule | BC-SKL-04035, BC-SKL-04036, BC-SKL-04037 | BC-CON-04013, BC-CON-04014 | BC-SKL-01028, BC-SKL-03028 (supporting) | BC-PRQ-04008 |

Notes for designers.

- BC-CON-04002 comes first although it is listed second in topic 4.1, because BC-SKL-04001 (units) is the only root of the 4.1 to 4.3 chain and is a hard parent of BC-SKL-04002, BC-SKL-04004, BC-SKL-04008, BC-SKL-04011, BC-SKL-04013 and BC-SKL-04014 (data/prereq_edges.csv). Only BC-SKL-04001 to BC-SKL-04004 is `verified` (sg-25:11 scores the units of the approximation separately).
- The edges BC-SKL-04001 to BC-SKL-04008 and BC-SKL-04001 to BC-SKL-04011 are `inferred`; the unit research lists neither in its 4.2 prerequisites (research/units/unit-04-contextual-applications-differentiation.md#Prerequisites under 4.2). [inferred] Settled by a review of the edge notes in data/prereq_edges.csv.
- BC-CON-04012 has a supporting edge from BC-TOP-0506 (Unit 5 concavity). A student reaching it before Unit 5 meets concavity as a used conclusion, which the research states: "Unit 4 uses the conclusion rather than deriving it" (research/units/unit-04-contextual-applications-differentiation.md#What Unit 4 depends on).
- The edges marked `verified` inside the motion, related rates, tangent and L'Hospital chains are BC-SKL-04007 to BC-SKL-04010 (crabbc-25 via the unit research), BC-SKL-04009 to BC-SKL-04012, BC-SKL-04019 to BC-SKL-04020 (BC-EK-CHA-3D2), BC-SKL-04030 to BC-SKL-04031 (BC-EK-CHA-3F2) and BC-SKL-04034 to BC-SKL-04035 (sg-23:14). Every other in-unit edge is `inferred`.

## 2. Exam question types the unit feeds

Exam parts and per-question minutes: Section I Part A, 29 questions in 62 minutes, no calculator (2.14 minutes each); Part B, 13 in 38 minutes, calculator required (2.92); Section II Part A, 2 questions in 30 minutes, calculator required, and Part B, 4 in 60 minutes, no calculator (15.0 each) (research/exam/exam-structure.md#Section and part layout). Each free response question carries 9 points (research/exam/exam-structure.md#Free-response point totals).

Point type names are the BC-PT record names: BC-PT-99004 Answer with or without supporting work; BC-PT-99005 Answer with supporting work or setup shown; BC-PT-99006 Units; BC-PT-99008 Interpretation of a derivative value in context with units; BC-PT-99010 Justification by sign analysis of a derivative; BC-PT-99014 Considers the sign of a derivative; BC-PT-99021 Average rate of change expression; BC-PT-99022 Product rule; BC-PT-99023 Chain rule; BC-PT-99025 Tangent line approximation; BC-PT-99027 Higher derivative expression evaluated at a point; BC-PT-99054 Limit expression for end behaviour; BC-PT-99055 L'Hospital's Rule application; BC-PT-99068 Verification for a show-that prompt.

| Family | Archetype | Calculator | MCQ part | FRQ shape and part | Point types | Official examples |
|---|---|---|---|---|---|---|
| derivative-in-context | BC-QA-04001 | either | I-A or I-B | one part of a multipart contextual question, often sharing the part with a computation; II-A in every listed example | BC-PT-99004, BC-PT-99008 | BC-FRQ-2013-Q1-A, BC-FRQ-2014-Q1-B, BC-FRQ-2023-Q1-D, BC-FRQ-2018-Q2-A (all calculator), BC-MCQ-SAMPLE-013 |
| derivative-in-context | BC-QA-04005 | calculator | I-B | a multipart calculator question on one contextual model; II-A | BC-PT-99027, BC-PT-99010, BC-PT-99014 | BC-FRQ-2019-Q1-D, BC-FRQ-2022-Q1-C (both calculator) |
| derivative-from-table | BC-QA-04002 | either | I-A or I-B | the opening part of a table based contextual question; II-A or II-B | BC-PT-99005, BC-PT-99008, BC-PT-99006 | BC-FRQ-2021-Q1-A, BC-FRQ-2024-Q1-A, BC-FRQ-2026-Q1-A (calculator), BC-FRQ-2022-Q4-A, BC-FRQ-2025-Q3-A (no calculator) |
| motion-by-differentiation | BC-QA-04003 | either | I-A or I-B | two or three parts of a particle motion question; II-B in both listed examples | BC-PT-99021, BC-PT-99027, BC-PT-99004 | BC-FRQ-2014-Q4-A, BC-FRQ-2015-Q3-C (no calculator), BC-MCQ-CED-012 (calculator) |
| motion-by-differentiation | BC-QA-04004 | either | I-A or I-B | one part of a particle motion question | none recorded | none recorded |
| motion-by-accumulation | BC-QA-04010 | either | I-A or I-B | the closing part of a particle motion question | none recorded | none recorded |
| related-rates | BC-QA-04006 | either | I-A or I-B | one part of a multipart question, or a standalone MCQ; II-B in every listed example | BC-PT-99023, BC-PT-99006, BC-PT-99004, BC-PT-99022 | BC-FRQ-2019-Q4-A, BC-FRQ-2014-Q4-D, BC-FRQ-2022-Q4-D, BC-FRQ-2018-Q4-D (all no calculator), BC-MCQ-CED-005, BC-MCQ-SAMPLE-004 (no calculator), BC-MCQ-PE2012-038 (calculator) |
| related-rates | BC-QA-04007 | no_calculator | I-A | the closing part of the implicit differentiation question; II-B | none recorded | none recorded |
| tangent-line-approximation | BC-QA-04008 | either | I-A or I-B | one part, ordinarily after a part that produced the derivative | BC-PT-99025, BC-PT-99068, BC-PT-99004, BC-PT-99005 | BC-FRQ-2014-Q1-D (calculator), BC-FRQ-2023-Q3-B (no calculator) |
| lhospital-limit | BC-QA-04009 | no_calculator | I-A | one part of a graphical analysis question; II-B | BC-PT-99055, BC-PT-99004, BC-PT-99005, BC-PT-99054 | BC-FRQ-2013-Q5-A, BC-FRQ-2021-Q4-C, BC-FRQ-2023-Q4-C, BC-MCQ-SAMPLE-001, BC-MCQ-PE2012-028 |

Multipart structures are the "Multipart structure" lines under each archetype's heading in research/question-analysis/question-archetypes.md (for example research/question-analysis/question-archetypes.md#BC-QA-04003 Straight-line motion with velocity, acceleration, and speed). The calculator status of each BC-FRQ record is its record field. The unit research's evidence index lists 43 FRQ part records with Unit 4 as primary or secondary unit and 7 sample MCQ records (research/units/unit-04-contextual-applications-differentiation.md#Official evidence index [verified]); these are observations over the indexed years, not a forecast.

Scope note. The particle motion, related rates and linearisation archetypes rest on AB free response questions read through the Chief Reader reports, because the BC form carried parametric and vector motion (Unit 9) in 2022 to 2025 (research/units/unit-04-contextual-applications-differentiation.md#Unresolved). Unit 4 skills enter BC Question 2 as secondary skills: BC-SKL-04008 (speed) in BC-FRQ-2023-Q2-B and BC-FRQ-2024-Q2-A, BC-SKL-04009 and BC-SKL-04012 in BC-FRQ-2024-Q2-D, BC-SKL-04019 and BC-SKL-04024 in BC-FRQ-2014-Q2-D and BC-FRQ-2025-Q2-D (research/units/unit-04-contextual-applications-differentiation.md#Official evidence index [verified]).

### What the particle motion parts score

- Speed. The 2025 rubric awards the speed point only when the response states the sign of the velocity and draws the conclusion; quoting the rule without applying it to the particle does not suffice (research/question-analysis/question-archetypes.md#BC-QA-04003 Straight-line motion with velocity, acceleration, and speed, citing crabbc-25:22 and crabbc-25:23). A speed conclusion from the sign of acceleration alone loses the justification point (research/scoring/common-point-losses.md#Justification points [verified], BC-ERR-99003, cr-23:7, cr-24:7). cr-22:21 names this the most common misconception on that question.
- Direction over an interval. One point for considering the sign of a velocity, one for the analysis for one particle, one for both particles over the whole interval; responses not addressing the entire interval did not earn the last two (research/question-analysis/question-archetypes.md#BC-QA-04004 Direction of motion and sign analysis over an interval). The justification is a sign statement; research/scoring/justification-requirements.md#Sign analysis of a derivative [verified] records that no drawn sign chart is required and none earns a point by itself.
- Notation. A general derivative expression equated to a number earns only one of the two acceleration points (sg-23:6, research/scoring/notation-requirements.md#The equal sign [verified]). A parenthesis error in a speed expression loses the setup point and keeps the answer point (sg-23:6, research/scoring/notation-requirements.md#Parentheses [verified]).
- Units. Units are not read in a part that does not ask for them (research/scoring/notation-requirements.md#What notation never costs [verified]).

### What the related rates parts score

- Differentiation. The implicit curve task scores an eligible attempt at differentiation with respect to time, a completely correct differentiation and the value; a response differentiating with respect to x must continue through the chain rule to earn beyond the first point; a sign error was the most common loss of the last point in 2025 (research/question-analysis/question-archetypes.md#BC-QA-04007 Related rates on an implicitly defined curve, cr-24:18). The geometric task's archetype lists BC-PT-99023 (chain rule), BC-PT-99022 (product rule), BC-PT-99004 and BC-PT-99006 (units).
- Units. A units point is scored separately from the value and is lost for absent units, units of the original quantity on a derived one, or an inverted ratio (research/scoring/common-point-losses.md#Units points [verified], BC-ERR-99005, cr-22:14, cr-23:7, cr-24:4).
- Interpretation. An interpretation names the quantity and the interval; a rate of a rate described as a rate, or with its direction omitted, loses the point (research/scoring/common-point-losses.md#Interpretation points [verified], BC-ERR-99027, cr-23:4, cr-24:4).

## 3. Cross-concept patterns

### How the stems combine concepts

- Motion stems chain BC-CON-04003, BC-CON-04004 and BC-CON-04005 in one question: velocity at an instant, intervals of a direction, whether speed increases at an instant, then position from velocity and an initial condition (BC-QA-04010) (research/units/unit-04-contextual-applications-differentiation.md#Assessment behaviour under 4.2).
- Table based contextual stems open with BC-CON-04002 (approximation and units, BC-QA-04002) and attach BC-CON-04001 (interpretation) to a later part (research/units/unit-04-contextual-applications-differentiation.md#Assessment behaviour under 4.1, sg-24:2, sg-25:11).
- The calculator contextual question joins BC-CON-04006 with an average value, a time where instantaneous and average rates agree, an end behaviour limit and a maximum (sg-25:4, research/units/unit-04-contextual-applications-differentiation.md#Assessment behaviour under 4.3).
- The implicit differentiation question (Unit 3) closes with BC-CON-04007, BC-CON-04008 and BC-CON-04009 on the same curve, and places BC-CON-04011 right after the part that produced the derivative (cr-24:18, research/units/unit-04-contextual-applications-differentiation.md#Assessment behaviour under 4.6).
- The graphical analysis question places BC-CON-04013 to BC-CON-04015 with one function known only through its derivative's graph, so BC-SKL-04038 (continuity from differentiability) supplies the numerator limit (sg-23:14).
- research/question-analysis/frq-analysis.md#How concepts combine inside one question [verified] names the Unit 2 with Unit 4 pairing: the derivative rule with the contextual reading of the value it produces.

### Recognition features between neighbouring concepts

| Neighbours | Feature in the stem that selects | First written line | Source |
|---|---|---|---|
| Speed (BC-CON-04004) against velocity (BC-CON-04004, BC-CON-04003) | "speed" asks for the size with the sign dropped; "velocity" or "direction" keeps the sign | speed: the absolute value of \(v(t)\) at the instant; direction: the sign of \(v(t)\) | BC-SKL-04008, BC-SKL-04009, BC-MIS-04005 probe |
| Speeding up (BC-CON-04005) against positive acceleration (BC-CON-04003) | "is the speed increasing" needs both signs; "find the acceleration" needs one value | \(v(t_0)\) and \(a(t_0)\) with both signs stated, then the comparison | BC-QA-04003 path, BC-SKL-04010, BC-MIS-04006 probe, cr-22:21 |
| Related rates (BC-CON-04007) against implicit differentiation (Unit 3) | a rate of one coordinate "at that instant" is supplied and the other coordinate's rate is asked: differentiate with respect to time; a slope or dy/dx is asked: differentiate with respect to x | the curve equation differentiated with respect to t, a rate factor on every varying quantity | BC-QA-04007 path and wrong approaches, BC-ERR-04017, BC-ERR-99013 |
| Linearisation (BC-CON-04011) against tangent line (BC-QA-02011, Unit 2) | "approximate the value at a nearby input" asks for the line evaluated there; "write an equation" asks for the line alone | slope at the point of tangency, then the point-slope line | BC-QA-04008 path, BC-ERR-04024 |
| L'Hospital's rule (BC-CON-04015) against a limit that is not indeterminate (BC-CON-04013) | the numerator and denominator limits, computed separately, are both 0 or both infinite; otherwise the rule does not apply | two separate limit statements, then the statement that the form is indeterminate | BC-QA-04009 path, ced:84, sg-23:14, BC-MIS-04015 probe |
| Contextual rate (BC-CON-04006) against motion (BC-CON-04003) | the quantity named in the stem is not a position | the quantity and its independent variable named | BC-SKL-04013, BC-SKL-04015, ced:84 |
| Rate (BC-CON-04001) against amount | "how fast" against "how much" | the derivative value, then quantity, instant, direction, units | BC-SKL-04003, BC-ERR-04003 |

### The confusable set

`tools/check_lessons.py --sets` returns one Unit 4 set, served by decision lesson LSN-DEC-04-01: BC-SKL-04028, BC-SKL-04029, BC-SKL-04030, BC-SKL-04031, BC-SKL-04032. All five skills are loaded by BC-QA-04008 and belong to BC-CON-04011 and BC-CON-04012. The member each stem selects follows the archetype's `asked_to_produce` entries:

| Member | Stem asks for | Selecting feature |
|---|---|---|
| BC-SKL-04032 | "the slope at the point of tangency" | a derivative expression is supplied (dy/dx or a differential equation) with a point |
| BC-SKL-04028 | an equation of the tangent line | "write an equation for the line tangent" |
| BC-SKL-04029 | "a tangent line approximation at a nearby input" | a second input near the point of tangency is named |
| BC-SKL-04030 | "an overestimate or underestimate judgement" | "is this an overestimate or an underestimate" |
| BC-SKL-04031 | the judgement "with a reason" | "give a reason" or "justify", which the concavity argument alone earns (BC-ERR-99020, cr-23:11, cr-23:12) |

The speed, related rates and L'Hospital neighbours above are not confusable sets: their `confusable_with` components exceed DECISION_SET_MAX (6) or cross units, so the tool drops them (docs/plan/15-lessons.md, Methods, decision lessons for confusable sets, app/lessons/confusable.py). Their discrimination is carried by each concept lesson's Recognition section and strategy blocks. [inferred] Settled by running `tools/check_lessons.py --sets` again after any change to `confusable_with`.

## 4. Recurring traps

Computed by mapping each record's `skills` to the Unit 4 concept that holds the skill and keeping records that meet two or more concepts.

### Errors across concepts (data/errors.json)

| Error | Name | Concepts | Scoring consequence (record text) | Linked misconceptions |
|---|---|---|---|---|
| BC-ERR-04001 | Units omitted or assembled the wrong way round | BC-CON-04001, BC-CON-04002, BC-CON-04010 | The units point is a separate point in the 2024 and 2025 table based questions and is lost outright (sg-24:2, sg-25:11); BC-ERR-99005 records the same behaviour across years. | BC-MIS-04003, BC-MIS-04001 |
| BC-ERR-04005 | Sign of a rate not interpreted | BC-CON-04001, BC-CON-04010 | The interpretation point is lost; BC-ERR-99030 records the same confusion of direction with quantity. | BC-MIS-04002, BC-MIS-04001 |
| BC-ERR-04018 | Product rule omitted inside a differentiation with respect to time | BC-CON-04007, BC-CON-04008 | The completely correct differentiation point is lost; BC-ERR-99013 names the missing product rule explicitly. | BC-MIS-04009, BC-MIS-04011 |
| BC-ERR-99013 | Related rates differentiated with respect to the wrong variable or without the product rule | BC-CON-04007, BC-CON-04008, BC-CON-04009 | The differentiation points in the part are not earned, and the numerical answer point depends on them. | BC-MIS-99005, BC-MIS-99014, BC-MIS-04008 |
| BC-ERR-99033 | Variable introduced without being defined | BC-CON-04007, BC-CON-04008 | The point for expressing the quantity as a function of the given variable is not earned, and the chain rule step that depends on it is unreachable. | BC-MIS-05022 |
| BC-ERR-04028 | Quotient written explicitly equal to an indeterminate form | BC-CON-04013, BC-CON-04014 | The 2023 rubric states that a response presenting a limit explicitly equal to zero over zero does not earn the first point, and the Chief Reader report names this arithmetic with infinity (sg-23:14, cr-23:15). | BC-MIS-04014, BC-MIS-99008 |
| BC-ERR-04029 | Rule applied with no verification of the form | BC-CON-04013, BC-CON-04014, BC-CON-04015 | The hypothesis point is lost; the CED unit overview states that students must show that the rule applies, and BC-ERR-99008 records unverified hypotheses across years (ced:84). | BC-MIS-04015, BC-MIS-04014 |
| BC-ERR-99022 | Unnecessary simplification introducing arithmetic or algebra errors | BC-CON-04011, BC-CON-04012 | A point already secured by the correct setup can be lost when the simplified final form is wrong. | none |

### Misconceptions across concepts (data/misconceptions.json)

| Misconception | Severity | Concepts |
|---|---|---|
| BC-MIS-04002 The sign of a rate is decoration | medium | BC-CON-04001, BC-CON-04010 |
| BC-MIS-04003 Units are an ornament on the answer | high | BC-CON-04002, BC-CON-04010 |
| BC-MIS-04009 A short product is a single varying symbol | high | BC-CON-04007, BC-CON-04008 |
| BC-MIS-04014 Indeterminate forms are numbers | high | BC-CON-04006, BC-CON-04013 |
| BC-MIS-04015 L'Hospital's rule applies to any awkward limit | high | BC-CON-04014, BC-CON-04015 |
| BC-MIS-04017 Sampled values establish behaviour on an interval | high | BC-CON-04004, BC-CON-04005 |

A misconception reaches the student only as the "possible reason" line of the error block it is linked to, in the record's own words (docs/lessons/TEMPLATE.md, Traps).

### Single-concept errors with a named scoring loss

- BC-ERR-99003 Speed decided from the sign of acceleration alone (BC-CON-04005): "The reasoning point for speeding up or slowing down is not earned, even when the reported acceleration value is correct."
- BC-ERR-99020 Over or underestimate claimed without appealing to concavity (BC-CON-04012): "The reasoning point is not earned; in 2022 this part was the most challenging of its question."
- BC-ERR-99027 Interpretation of a value in context left incomplete (BC-CON-04001): "The interpretation point requires the key phrases, so an answer missing the interval or the rate of a rate is not earned."
- BC-ERR-99008 Hypotheses of a theorem not verified before its conclusion is used (BC-CON-04015): "The condition point is not earned; in several years this was the point earned by the smallest proportion of responses on the question."
- BC-ERR-99007 Arithmetic performed with infinity and limit notation dropped (BC-CON-04006): "The response becomes ineligible for the final point of the part; in improper integral parts the evaluation points are lost."
- BC-ERR-99030 Direction of change confused with the sign of the quantity itself (BC-CON-04004): "The reasoning point is not earned even when the stated conclusion is correct."

### Point losses research/scoring names for this unit's shapes

- research/scoring/common-point-losses.md#Units points [verified]: absent units, the original quantity's units on a derived quantity, an inverted ratio (BC-ERR-99005). Shapes: BC-QA-04001, BC-QA-04002, BC-QA-04006.
- research/scoring/common-point-losses.md#Interpretation points [verified]: interval omitted; a rate of a rate described as a rate; a true statement that does not answer the question (BC-ERR-99027, BC-ERR-99030). Shapes: BC-QA-04001, BC-QA-04005, BC-CON-04010.
- research/scoring/common-point-losses.md#Justification points [verified]: unverified hypotheses of L'Hospital's rule (BC-ERR-99008, cr-23:4, cr-23:16); speed from acceleration alone (BC-ERR-99003); over or under estimate without concavity (BC-ERR-99020, cr-23:11, cr-23:12). Shapes: BC-QA-04009, BC-QA-04003, BC-QA-04008.
- research/scoring/common-point-losses.md#Notation points [verified]: an expression equated to a number (BC-ERR-99002, cr-24:8); vague referents such as "it" or "the function" (BC-ERR-99001, cr-23:16); limit notation dropped (BC-ERR-99007, cr-23:16). Shapes: BC-QA-04003, BC-QA-04005, BC-QA-04009.
- research/scoring/common-point-losses.md#Answer points [verified]: unrequired simplification introducing an error (BC-ERR-99022). Shape: BC-QA-04008.
- research/scoring/common-point-losses.md#Precision and presentation points [verified]: a correct answer boxed beside a second value (BC-ERR-99022, cr-24:3).
- research/scoring/justification-requirements.md#Theorem hypotheses [verified]: continuity is derived from differentiability, not asserted (sg-25:12), which is the step BC-SKL-04038 carries into BC-QA-04009 (sg-23:14).
- research/scoring/notation-requirements.md#Limit notation [verified]: arithmetic with infinity is scratch work and cannot earn the end behaviour value point (sg-25:4), which binds BC-SKL-04016.

## 5. Time budgets per archetype shape

Budgets from research/exam/exam-structure.md#Section and part layout, applied as docs/plan/15-lessons.md#Fluency, measured and never credited states: the Part A figure for a no calculator MCQ shape, the Part B figure for a calculator one, and a free response part's share of 15.0 minutes. The share below is points over 9 times 15.0, that is 1.67 minutes per point, taken from the listed example's `points` field. [inferred] The per-point share is plan 15's rule applied to 9-point questions; settled by the fluency telemetry the plan names.

| Archetype | MCQ budget | FRQ part budget (example, points) | Steps a fluent solver writes | Steps held in the head |
|---|---|---|---|---|
| BC-QA-04001 | 2.14 or 2.92 | 3.33 (BC-FRQ-2023-Q1-D, 2) | one sentence: quantity, instant, direction, value, units | the reading of the sign |
| BC-QA-04002 | 2.14 or 2.92 | 3.33 (BC-FRQ-2025-Q3-A, 2) | the difference over the difference with table values, the value, the units | choosing the bracketing rows |
| BC-QA-04003 | 2.14 or 2.92 | 1.67 to 3.33 (BC-FRQ-2014-Q4-A, 1; BC-FRQ-2015-Q3-C, 2) | \(v(t_0)\) and \(a(t_0)\) with signs, the conclusion naming both signs | the differentiation for a simple polynomial |
| BC-QA-04004 | 2.14 or 2.92 | no scored example in the library | \(v(t)=0\) solved, the sign on each subinterval in words, the interval stated | the test value arithmetic |
| BC-QA-04005 | 2.92 | 3.33 (BC-FRQ-2019-Q1-D, 2) | the equation or limit expression beside the calculator value to three decimals | the calculator keystrokes |
| BC-QA-04006 | 2.14 or 2.92 | 3.33 to 5.0 (BC-FRQ-2019-Q4-A, 2; BC-FRQ-2022-Q4-D, 3) | relating equation, differentiated equation with every rate factor, substituted equation, rate with units | the list of given and wanted rates |
| BC-QA-04007 | 2.14 | no scored example in the library | the differentiated curve equation in t, the substitution, the rate | which coordinate is supplied |
| BC-QA-04008 | 2.14 or 2.92 | 3.33 to 6.67 (BC-FRQ-2023-Q3-B, 2; BC-FRQ-2014-Q1-D, 4) | slope value, point-slope line, the line at the nearby input left unsimplified, the concavity reason | isolating y, which is not required (crabbc-25:25 via the unit research) |
| BC-QA-04009 | 2.14 | 3.33 to 5.0 (BC-FRQ-2021-Q4-C, 2; BC-FRQ-2023-Q4-C, 3) | the two separate limits, the ratio of derivatives in limit notation, the value | none: each written line carries a point (sg-23:14) |
| BC-QA-04010 | 2.14 or 2.92 | no scored example in the library | initial position plus the integral of velocity, the antiderivative, the value | none |

The written and held columns follow each archetype's `expected_solution_path` and the scoring lines of section 2; which lines a solver may skip is [inferred] wherever the rubric does not score the line. Settled by comparing the Chief Reader sample commentary for each listed example.

## 6. Delivery map

Rules from docs/lessons/TEMPLATE.md#Delivery: (1) worked examples and error blocks are `step_reveal`; (2) a key idea describing a process is `motion`, with a `model` on the example where a computed sequence is the idea; (3) a figure-bearing BC-REP (02, 07, 08, 12, 13, 14) on the skill gives `figure`, promoted to `interactive` when the archetype's `common_givens` or `difficulty_variables` name a varying quantity and the stem asks a reading; (4) BC-REP-03 givens give `table`; (5) everything else is `text`. Every entry below applies to the orientation and key ideas; every worked example and error block in all fifteen lessons is `step_reveal` by rule 1. Every non-text choice is [inferred], settled by the modality A/B in docs/lessons/BUILD-PLAN.md.

| Concept | Orientation | Key ideas (BC-EK) | Rule and triggering field |
|---|---|---|---|
| BC-CON-04002 | text | CHA-3A3 text; CHA-3A1 table; CHA-3C1 text | rule 4: BC-REP-03 in BC-SKL-04004 `representations` and BC-QA-04002 `common_givens` ("a table of values of a contextual quantity"); rule 5 for the rest (BC-REP-04, 05, 09) |
| BC-CON-04001 | text | CHA-3A1 text; CHA-3A2 text | rule 5: BC-SKL-04002, 04003, 04005 carry BC-REP-04 and BC-REP-05 only |
| BC-CON-04003 | text | CHA-3B1 text | rule 5: BC-SKL-04006, 04007 carry BC-REP-01 and BC-REP-05 |
| BC-CON-04004 | interactive | CHA-3B1 interactive | rule 3 promoted: BC-REP-02 in BC-SKL-04009 `representations`; BC-QA-04004 `difficulty_variables` "whether a zero of the velocity is not an integer" and "whether the velocity changes sign more than once", stem asks for intervals of a direction |
| BC-CON-04005 | text | CHA-3B1 text | rule 5: BC-SKL-04010 (BC-REP-01, 05) and BC-SKL-04012 (BC-REP-01, 04) carry no figure-bearing representation |
| BC-CON-04006 | text | CHA-3C1 text | rule 5: BC-REP-01, 04, 05; the end behaviour limit is scored as notation retained (sg-25:4), not as a process to watch |
| BC-CON-04007 | figure | CHA-3D1 interactive; CHA-3D2 text | rule 3 promoted: BC-REP-08 in BC-SKL-04017, BC-REP-02 in BC-SKL-04022; BC-QA-04006 `common_givens` "the dimensions at the instant" and "a figure of the configuration"; CHA-3D2 (product rule) rests on BC-REP-01 |
| BC-CON-04008 | figure | CHA-3D1 interactive; CHA-3D2 text | rule 3 promoted: BC-REP-08 in BC-SKL-04018 and BC-SKL-04021; BC-QA-04006 `difficulty_variables` "whether a second variable must be eliminated by similar triangles" |
| BC-CON-04009 | figure | CHA-3E1 interactive | rule 3 promoted: BC-REP-08 in BC-SKL-04026 and BC-SKL-04027; BC-QA-04006 `common_givens` "the dimensions at the instant"; the reading is which labels change as time moves |
| BC-CON-04010 | text | CHA-3E1 text | rule 5: BC-SKL-04024 (BC-REP-01, 09), BC-SKL-04025 (BC-REP-04, 05) |
| BC-CON-04011 | figure | CHA-3F1 motion | rule 2: BC-EK-CHA-3F1 describes closeness "near the point of tangency", a process of approach; rule 3 (BC-REP-02 in BC-SKL-04028, 04029) gives the orientation its figure |
| BC-CON-04012 | figure | CHA-3F2 interactive | rule 3 promoted: BC-REP-02 in BC-SKL-04030; BC-QA-04008 `common_givens` "the point of tangency and a nearby input"; the stem asks over or under, the template's "concavity against the tangent" reading |
| BC-CON-04013 | text | LIM-4A1 motion, with a model on the example | rule 2: BC-EK-LIM-4A1 describes a ratio that "tends to 0/0 ... in the limit", a limit being taken; the model is numerator, denominator and ratio values at shrinking distance, because the idea is that the ratio's behaviour is not read off the form [inferred] |
| BC-CON-04014 | text | LIM-4A2 text; LIM-4A1 figure | rule 3: BC-REP-02 in BC-SKL-04038 and BC-QA-04009 `common_givens` "a function known only through a graph of its derivative and one value"; no varying quantity is read, so no promotion; LIM-4A2 rests on BC-REP-01, 04 |
| BC-CON-04015 | text | LIM-4A2 text | rule 5: BC-SKL-04035, 04036, 04037 carry BC-REP-01 only |

Where each richer mode fits.

- Interactive, a particle on a line (BC-CON-04004): one slider on t moves a point along a horizontal line; the velocity sign and the direction arrow are labels inside the figure, and the question posed is "on which intervals is the particle moving left". A non-integer zero of \(v\) sits inside the range (BC-QA-04004 `difficulty_variables`, BC-MIS-04017 probe). Fallback: the static line with the sign intervals labelled. Keyboard: arrow keys step t. BC-CON-04005 stays text under rule 5; adding an acceleration readout to the same control would take a rule change, since BC-SKL-04010 lists no figure-bearing representation. [inferred] Settled by adding BC-REP-02 to BC-SKL-04010 if the library review supports it.
- Interactive, a related rates figure with one dimension sliding (BC-CON-04007, BC-CON-04008, BC-CON-04009): one slider on the varying dimension (the water height in a cone, the foot of a ladder), with the dependent dimension and the fixed ones labelled inside; the reading is which labels move and which stay fixed, which is BC-MIS-04011's probe ("which of the stated numbers would still hold one second later"). One control per screen. Fallback: two static frames at two times. Keyboard: arrow keys.
- Motion, a tangent line near the point (BC-CON-04011): discrete zoom frames centred on the point of tangency in which curve and tangent become indistinguishable, the gap at a nearby input labelled in each frame; auto-advance only under `prefers-reduced-motion: no-preference`. Fallback: the final and first frames side by side.
- Interactive, concavity against the tangent (BC-CON-04012): one draggable point of tangency on a curve with a concave up and a concave down region; the label inside reads "line above curve" or "line below curve" and the question is which one holds at the stated point.
- Text and step reveal only: BC-CON-04001, BC-CON-04003, BC-CON-04005, BC-CON-04006, BC-CON-04010 and BC-CON-04015 carry no figure-bearing representation; their key ideas are rules, and their worked examples and error blocks carry the method as step reveal.

## 7. Sources

Library ids: BC-UNIT-04; BC-TOP-0401 to BC-TOP-0407; BC-CON-04001 to BC-CON-04015; BC-SKL-04001 to BC-SKL-04038; BC-QA-04001 to BC-QA-04010, BC-QA-02011; BC-EK-CHA-3A1, BC-EK-CHA-3A2, BC-EK-CHA-3A3, BC-EK-CHA-3B1, BC-EK-CHA-3C1, BC-EK-CHA-3D1, BC-EK-CHA-3D2, BC-EK-CHA-3E1, BC-EK-CHA-3F1, BC-EK-CHA-3F2, BC-EK-LIM-4A1, BC-EK-LIM-4A2; BC-PRQ-04001 to BC-PRQ-04009; BC-PT-99004, BC-PT-99005, BC-PT-99006, BC-PT-99008, BC-PT-99010, BC-PT-99014, BC-PT-99021, BC-PT-99022, BC-PT-99023, BC-PT-99025, BC-PT-99027, BC-PT-99054, BC-PT-99055, BC-PT-99068; BC-ERR-04001, BC-ERR-04003, BC-ERR-04005, BC-ERR-04017, BC-ERR-04018, BC-ERR-04024, BC-ERR-04028, BC-ERR-04029, BC-ERR-99001, BC-ERR-99002, BC-ERR-99003, BC-ERR-99005, BC-ERR-99007, BC-ERR-99008, BC-ERR-99013, BC-ERR-99020, BC-ERR-99022, BC-ERR-99027, BC-ERR-99030, BC-ERR-99033; BC-MIS-04001 to BC-MIS-04017, BC-MIS-05022, BC-MIS-99005, BC-MIS-99008, BC-MIS-99014; BC-REP-01 to BC-REP-05, BC-REP-08, BC-REP-09.

Official records: BC-FRQ-2013-Q1-A, BC-FRQ-2013-Q5-A, BC-FRQ-2014-Q1-B, BC-FRQ-2014-Q1-D, BC-FRQ-2014-Q2-D, BC-FRQ-2014-Q4-A, BC-FRQ-2014-Q4-D, BC-FRQ-2015-Q3-C, BC-FRQ-2018-Q2-A, BC-FRQ-2018-Q4-D, BC-FRQ-2019-Q1-D, BC-FRQ-2019-Q4-A, BC-FRQ-2021-Q1-A, BC-FRQ-2021-Q4-C, BC-FRQ-2022-Q1-C, BC-FRQ-2022-Q4-A, BC-FRQ-2022-Q4-D, BC-FRQ-2023-Q1-D, BC-FRQ-2023-Q2-B, BC-FRQ-2023-Q3-B, BC-FRQ-2023-Q4-C, BC-FRQ-2024-Q1-A, BC-FRQ-2024-Q2-A, BC-FRQ-2024-Q2-D, BC-FRQ-2025-Q2-D, BC-FRQ-2025-Q3-A, BC-FRQ-2026-Q1-A; BC-MCQ-CED-005, BC-MCQ-CED-012, BC-MCQ-SAMPLE-001, BC-MCQ-SAMPLE-004, BC-MCQ-SAMPLE-013, BC-MCQ-PE2012-028, BC-MCQ-PE2012-038.

Pages: ced:84, ced:86, ced:87, ced:88, ced:89, ced:90, ced:91, ced:92, ced:93; sg-23:6, sg-23:14, sg-24:2, sg-25:4, sg-25:11, sg-25:12; cr-22:7, cr-22:14, cr-22:21, cr-23:4, cr-23:7, cr-23:11, cr-23:12, cr-23:15, cr-23:16, cr-24:3, cr-24:4, cr-24:7, cr-24:8, cr-24:18. Chief Reader 2025 AB and BC pages (crabbc-25:20, crabbc-25:22, crabbc-25:23, crabbc-25:25) are cited only as the research files cite them.

Research headings:

- research/units/unit-04-contextual-applications-differentiation.md#Unit 4, Contextual Applications of Differentiation
- research/units/unit-04-contextual-applications-differentiation.md#Prerequisites
- research/units/unit-04-contextual-applications-differentiation.md#Assessment behaviour
- research/units/unit-04-contextual-applications-differentiation.md#What Unit 4 depends on
- research/units/unit-04-contextual-applications-differentiation.md#Unresolved
- research/units/unit-04-contextual-applications-differentiation.md#Official evidence index [verified]
- research/exam/exam-structure.md#Section and part layout
- research/exam/exam-structure.md#Free-response point totals
- research/scoring/common-point-losses.md#Answer points [verified]
- research/scoring/common-point-losses.md#Units points [verified]
- research/scoring/common-point-losses.md#Interpretation points [verified]
- research/scoring/common-point-losses.md#Justification points [verified]
- research/scoring/common-point-losses.md#Notation points [verified]
- research/scoring/common-point-losses.md#Precision and presentation points [verified]
- research/scoring/justification-requirements.md#Sign analysis of a derivative [verified]
- research/scoring/justification-requirements.md#Theorem hypotheses [verified]
- research/scoring/notation-requirements.md#Limit notation [verified]
- research/scoring/notation-requirements.md#The equal sign [verified]
- research/scoring/notation-requirements.md#Parentheses [verified]
- research/scoring/notation-requirements.md#What notation never costs [verified]
- research/question-analysis/question-archetypes.md#BC-QA-04001 Interpreting the value of a derivative in context with units
- research/question-analysis/question-archetypes.md#BC-QA-04002 Approximating a derivative from a table with units
- research/question-analysis/question-archetypes.md#BC-QA-04003 Straight-line motion with velocity, acceleration, and speed
- research/question-analysis/question-archetypes.md#BC-QA-04004 Direction of motion and sign analysis over an interval
- research/question-analysis/question-archetypes.md#BC-QA-04005 Contextual rate in a setting other than motion
- research/question-analysis/question-archetypes.md#BC-QA-04006 Related rates in a geometric setting
- research/question-analysis/question-archetypes.md#BC-QA-04007 Related rates on an implicitly defined curve
- research/question-analysis/question-archetypes.md#BC-QA-04008 Tangent line approximation with an over or under estimate judgement
- research/question-analysis/question-archetypes.md#BC-QA-04009 Limit of an indeterminate form with L'Hospital's rule
- research/question-analysis/question-archetypes.md#BC-QA-04010 Position recovered from velocity with an initial condition
- research/question-analysis/frq-analysis.md#How concepts combine inside one question [verified]
- docs/plan/15-lessons.md, sections What a lesson is, and its granularity; Methods, thought process and scoring habits; Fluency, measured and never credited; Pacing to the exam date
- docs/lessons/TEMPLATE.md, Delivery

Inferred claims, with what settles each:

- The fringe order treats every outside parent as reached. Settled by the engine's fringe computation over the full snapshot.
- The edges BC-SKL-04001 to BC-SKL-04008 and to BC-SKL-04011 are inferred and absent from the unit research. Settled by an edge review in data/prereq_edges.csv.
- The per-point FRQ share of 1.67 minutes. Settled by the fluency telemetry.
- The written and held steps where no rubric line scores the step. Settled by the Chief Reader sample commentary.
- Every non-text delivery mode, and the model on BC-CON-04013's example. Settled by the modality A/B.
- The neighbour pairs of section 3 are served through Recognition sections, not decision lessons. Settled by rerunning `tools/check_lessons.py --sets`.

Library gaps:

- BC-QA-04004, BC-QA-04007 and BC-QA-04010 carry empty `point_types` and no `official_examples`, although the research scores them from the Chief Reader reports; their lessons carry no scoring section (plan 15, R14).
- BC-QA-04003 `point_types` (BC-PT-99021, BC-PT-99027, BC-PT-99004) hold no reason or justification type for the speed conclusion the research says is scored (crabbc-25:22 via research/question-analysis/question-archetypes.md#BC-QA-04003 Straight-line motion with velocity, acceleration, and speed).
- BC-QA-04002 `asked_to_produce` is filled in the snapshot while its research heading reads "none recorded"; the snapshot is used.
- Concept-level hard edges form two cycles (BC-CON-04002 with BC-CON-04006, BC-CON-04007 with BC-CON-04008), so concept order is derived from the skill order.
- The Unit 4 confusable set holds only the tangent line skills; the motion, related rates and L'Hospital neighbours have no decision lesson.
