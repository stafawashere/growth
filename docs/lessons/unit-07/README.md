---
title: Unit 7 attack map, Differential Equations
research_date: 2026-09-29
status: draft
purpose: The map every designer of the 12 Unit 7 concept lessons reads first. It fixes the concept order along the prerequisite edges, the exam question types the unit feeds and the points they score, the cross-concept recognition features and the unit's confusable set, the recurring traps, the time budgets per archetype shape, and the delivery mode per concept under the TEMPLATE selection rules, all computed from the library or cited to research and cached pages.
---

# Unit 7 attack map, Differential Equations

Scope: BC-UNIT-07, topics BC-TOP-0701 to BC-TOP-0709, CED pages ced:137 to ced:145; topics 7.5 and 7.9 are BC only (research/units/unit-07-differential-equations.md#Unit 7, Differential Equations). Every count below was computed on 2026-09-29 from the content snapshot (`app.content.loader.load_snapshot`), `data/prereq_edges.csv`, `data/errors.json`, `data/misconceptions.json` and `tools/check_lessons.py --sets`. A claim with no library or research source is tagged [inferred] with what would settle it.

Three library facts shape the whole map.

- The concept graph over hard edges has one 2-cycle: BC-CON-07011 and BC-CON-07012. BC-SKL-07039 (BC-CON-07011) is a hard parent of BC-SKL-07040 (BC-CON-07012), and BC-SKL-07041 and BC-SKL-07042 (BC-CON-07012) are hard parents of BC-SKL-07043 (BC-CON-07011). A concept-level topological sort stalls after BC-CON-07010. The skill-level sort has no cycle (all 43 skills are reached), so section 1 orders concepts by the first of their skills the fringe reaches.
- Every edge into a Unit 7 skill carries evidence tag inferred (`data/prereq_edges.csv`, `evidence_tag` column).
- Every Unit 7 archetype is either `no_calculator` or `either`; none is `calculator`. BC-QA-07006, 07008, 07009 and 07011 carry no `point_types`, so their lessons carry no scoring section (docs/lessons/TEMPLATE.md, Scoring; plan 15 R14).

## 1. Concept order along the prerequisite edges

Computed: Kahn's topological sort over `hard_prerequisite` edges between the 43 Unit 7 skills, ties by id; each concept is listed where its first skill is reached. "Hard parents in Unit 7" are concepts holding a skill with a hard edge into one of this concept's skills. "Outside hard" are hard edges from other units or topic stand-ins. "Supporting" are non-PRQ supporting edges. "BC-PRQ" are the supporting non-calculus parents.

| # | Concept | Name | Skills | Hard parents in Unit 7 | Outside hard parents | Supporting (non-PRQ) | BC-PRQ parents |
|---|---|---|---|---|---|---|---|
| 1 | BC-CON-07001 | Differential equation as a relation between a function and its derivatives | BC-SKL-07001 to 07005 | none | BC-SKL-04001, BC-SKL-04013, BC-SKL-06057 | none | BC-PRQ-06005, BC-PRQ-07002, BC-PRQ-07003 |
| 2 | BC-CON-07002 | Verification of a proposed solution | BC-SKL-07006, 07007, 07008 | none | BC-SKL-03002, BC-TOP-0205 | none | BC-PRQ-06005, BC-PRQ-07002 |
| 3 | BC-CON-07003 | Families of solutions | BC-SKL-07009 | BC-CON-07002 | none | BC-SKL-02013 | none |
| 4 | BC-CON-07004 | Slope field as a plot of derivative values | BC-SKL-07010 to 07013 | BC-CON-07001 | none | none | BC-PRQ-06005, BC-PRQ-07006 |
| 5 | BC-CON-07005 | Solution curves read off a slope field | BC-SKL-07014 to 07018 | BC-CON-07004 | BC-TOP-0301 | BC-SKL-05014, BC-SKL-05030 | BC-PRQ-07006 |
| 6 | BC-CON-07006 | Euler's method as repeated local linearisation | BC-SKL-07019 to 07023 | BC-CON-07004, BC-CON-07005 | none | BC-SKL-04030, BC-SKL-05046 | BC-PRQ-07005 |
| 7 | BC-CON-07007 | Separation of variables | BC-SKL-07024 to 07028 | BC-CON-07004 | BC-SKL-06034, BC-SKL-06047 | BC-SKL-06047 | BC-PRQ-06003, BC-PRQ-07001, BC-PRQ-07002 |
| 8 | BC-CON-07008 | Particular solution selected by an initial condition | BC-SKL-07029, 07030, 07032, 07033 | BC-CON-07001, BC-CON-07003, BC-CON-07007 | BC-SKL-06044 | none | BC-PRQ-07004 |
| 9 | BC-CON-07009 | Domain restrictions on a particular solution | BC-SKL-07031 | BC-CON-07007 | none | none | BC-PRQ-05003 |
| 10 | BC-CON-07010 | Exponential growth and decay model | BC-SKL-07034 to 07038 | BC-CON-07001, BC-CON-07007, BC-CON-07008 | none | none | BC-PRQ-06003, BC-PRQ-07001, BC-PRQ-07003 |
| 11 | BC-CON-07011 | Logistic differential equation | BC-SKL-07039, 07043 | BC-CON-07001, BC-CON-07012 (through BC-SKL-07043 only) | BC-SKL-06064 | none | BC-PRQ-07003 |
| 12 | BC-CON-07012 | Carrying capacity and the point of fastest change | BC-SKL-07040, 07041, 07042 | BC-CON-07005, BC-CON-07011 | BC-SKL-05052 | none | BC-PRQ-05001 |

Order notes.

- BC-CON-07004 sits under almost everything: BC-SKL-07010 (compute the slope the equation assigns to a point) is a hard parent of nine skills, including BC-SKL-07019, 07020 (Euler) and BC-SKL-07028 (not separable). A designer of LSN-CON-07006 or LSN-CON-07007 may assume evaluating the right side at a point.
- The separation chain is BC-SKL-07024, 07025, 07026, then 07027 and 07029, then 07030, 07031, 07033, 07035. BC-CON-07008 needs BC-CON-07003 because BC-SKL-07009 (infinitely many solutions) is a hard parent of BC-SKL-07033 (general against particular).
- BC-CON-07011 and BC-CON-07012 interleave: BC-SKL-07039 (write the logistic equation), then BC-SKL-07040, 07041, 07042, then BC-SKL-07043 (interpret the model). LSN-CON-07011 is reached first but its interpretation skill cannot be credited before LSN-CON-07012's two skills are. [inferred: whether the lesson gate handles a concept whose skills straddle another concept is settled by the first-contact trigger in docs/plan/15-lessons.md#What a lesson is, and its granularity, which reads every skill an item loads.]
- BC-SKL-06057 (integration by parts) as a hard parent of BC-SKL-07004 (identify the initial condition in a context) has no stated reason in the research file's edge list (research/units/unit-07-differential-equations.md#What Unit 7 depends on names Unit 6 edges into BC-SKL-07025, 07029, 07032 only). Flagged as a library gap below.

## 2. Exam question types the unit feeds

Budgets from (research/exam/exam-structure.md#Section and part layout): Section I Part A (29 questions, 62 minutes, no calculator) 2.14 minutes per question; Part B (13 questions, 38 minutes, calculator) 2.92; Section II (Part A 2 questions in 30 minutes, calculator; Part B 4 in 60, no calculator) 15.0 per question, 9 points each (research/exam/exam-structure.md#Free-response point totals). Every recorded Unit 7 free-response part in the evidence index is `no_calculator` (research/units/unit-07-differential-equations.md#Official evidence index [verified]), and Q3 to Q6 are the no-calculator slots whose parts include "the separation of variables and Euler steps" (research/question-analysis/frq-analysis.md#The calculator questions and the no-calculator questions).

The table lists every archetype whose `skills` meets a Unit 7 skill (all active; none from another unit loads a Unit 7 skill), grouped by `family`.

| Family | Archetype | Calculator | MCQ part | FRQ part | Point types | Official examples |
|---|---|---|---|---|---|---|
| slope-field | BC-QA-07001 Solution curve sketched on a supplied slope field | no_calculator | I-A | II-B, opening part, 1 point | BC-PT-99065 | BC-FRQ-2023-Q3-A, BC-FRQ-2024-Q3-A |
| slope-field | BC-QA-07002 Slope field matched to or built from a differential equation | no_calculator | I-A | II-B, short part | BC-PT-99065, 99066, 99083 | BC-FRQ-2015-Q4-A, BC-FRQ-2026-Q3-A, BC-MCQ-CED-009, BC-MCQ-SAMPLE-005 |
| separation-of-variables | BC-QA-07003 Particular solution by separation of variables | no_calculator | I-A | II-B, closing part, 4 or 5 points | BC-PT-99028, 99029, 99031, 99032, 99033, 99030 | BC-FRQ-2019-Q4-C, 2013-Q5-C, 2021-Q5-C, 2023-Q3-D, 2024-Q3-C, 2026-Q3-D |
| separation-of-variables | BC-QA-07011 Particular solution with a domain restriction or an accumulation form | no_calculator | I-A | II-B | none | none |
| separation-of-variables | BC-QA-07012 Differential equation judged separable or not, and a separable one separated | no_calculator | I-A (single MCQ or short answer) | first step of every II-B separation part | BC-PT-99028 | none |
| euler | BC-QA-07004 Euler's method over two steps of equal size | no_calculator | I-A | II-B, 2 points | BC-PT-99034, 99004, 99005 | BC-FRQ-2013-Q5-B, 2021-Q5-B, 2024-Q5-C, 2025-Q5-D, BC-MCQ-SAMPLE-018, BC-MCQ-PE2012-016 |
| euler | BC-QA-07005 Direction of an approximation decided from the second derivative of a solution | no_calculator | I-A | II-B, 2 points | BC-PT-99027, 99026 | BC-FRQ-2023-Q3-C, BC-FRQ-2026-Q3-C |
| de-qualitative-behaviour | BC-QA-07010 Behaviour of a solution obtained from the differential equation itself | no_calculator | I-A | II-B, 3 points | BC-PT-99027, 99023, 99010, 99063, 99005 | BC-FRQ-2019-Q4-B, 2015-Q4-B, 2026-Q3-B, BC-MCQ-PE2012-012 |
| de-verification | BC-QA-07007 Verification that a function solves a differential equation | no_calculator | I-A | II-B, short part | BC-PT-99005, 99068, 99004 | BC-FRQ-2015-Q4-D |
| de-modelling | BC-QA-07006 Differential equation written from a verbal rate statement | either | I-A or I-B | opening of II-A or II-B | none | BC-MCQ-PE2012-023 |
| exponential-model | BC-QA-07008 Exponential growth or decay model solved and interpreted | either | I-A or I-B | II-A or II-B | none | BC-MCQ-SAMPLE-010 |
| logistic-model | BC-QA-07009 Logistic model interpreted without solving | either | I-A or I-B | one or two parts of II-A or II-B | none | BC-MCQ-CED-017, BC-MCQ-PE2012-014 |

Research tags de-modelling, de-verification, exponential-model and logistic-model `[inferred]` (research/question-analysis/question-archetypes.md, Family de-modelling, Family de-verification, Family exponential-model, Family logistic-model), and records no free-response part in 2023 to 2025 for BC-QA-07002, 07006, 07007, 07008, 07009 and 07011 (research/units/unit-07-differential-equations.md#Unresolved). BC-QA-07012 is not in the research file's archetype table of eleven (research/units/unit-07-differential-equations.md#Archetype summary); its record is in research/question-analysis/question-archetypes.md under `### BC-QA-07012`.

### The differential-equation free-response question and the points it scores

The official records place slope field, qualitative behaviour, direction of an approximation, Euler and separation parts inside one question: BC-FRQ-2023-Q3 (A sketch, C direction, D separation), BC-FRQ-2024-Q3 (A sketch, C separation), BC-FRQ-2026-Q3 (A field, B behaviour, C direction, D separation), BC-FRQ-2015-Q4 (A field, B behaviour, D verification), BC-FRQ-2013-Q5 and BC-FRQ-2021-Q5 (B Euler, C separation) (research/units/unit-07-differential-equations.md#Official evidence index [verified]). No logistic part appears in 2023 to 2025 (research/units/unit-07-differential-equations.md#Unit 7, Differential Equations).

- Slope field sketch (BC-QA-07001), 1 point, BC-PT-99065: the curve passes through the stated point, extends close to both edges, has no obvious conflict with the segments, and lies entirely on the correct side of the horizontal segments; a curve crossing the equilibrium level does not earn it; only the portion inside the printed field is read (sg-23:9, sg-24:9). A drawn field (BC-QA-07002) earns BC-PT-99083 for segments at the indicated points only, scored in groups by the value of the independent variable (samples-15-q4:1). An explanation about a field earns BC-PT-99066 only when it references the sign of the drawn segments' slopes; "sign of the slope field", "slope of the slope field", "slope of the differential equation" and "increasing behaviour of the slope field" fail (sg-26:11; research/scoring/justification-requirements.md#Reasons about slope fields and concavity).
- Separation with an initial condition (BC-QA-07003), 4 points in 2023 and 5 in 2024 and 2026:
  - Separation point BC-PT-99028: each variable with its own differential. With no separation the whole part scores zero (sg-26:13, sg-23:12, sg-21:20, sg-19:5).
  - Antiderivative points BC-PT-99029 and BC-PT-99030: one consistent antiderivative each; in the 4-point shape both sides share one point (sg-23:12), in the 5-point shape they are scored separately (sg-24:11, sg-26:13). A logarithm written with parentheses or with absolute value is accepted (sg-26:13, sg-23:12; research/scoring/notation-requirements.md#Parentheses).
  - Constant and initial condition point BC-PT-99031: the constant included in an equation and the initial values substituted to solve for it. No constant anywhere blocks this point and the solve point, so a response with no constant earns at most the first two points (sg-26:13, sg-23:12).
  - Answer point BC-PT-99032: the dependent variable isolated, in any equivalent form. An implicit logarithmic form, or a solution with no constant shown, does not earn it (sg-26:13). Each later point requires the earlier ones (sg-23:12).
  - BC-QA-07003 also lists BC-PT-99033, whose `earns` text is the initial value added to a definite integral (sg-24:3, sg-22:8); it fits the accumulation form of BC-SKL-07032 (BC-EK-FUN-7E2), not the separation part. Listed as a gap below.
- Euler (BC-QA-07004), 2 points: BC-PT-99034 for the demonstration (correct initial condition, step size and derivative expression), then the answer (BC-PT-99004 on the 2013 and 2021 and 2024 records, BC-PT-99005 on 2025). 2024 required two demonstrated steps with at most one error and withheld the answer point on any error; 2025 required only the first step and discounted later simplification or rounding (sg-24:17, sg-25:23). A table must be labelled when the answer is missing or wrong (research/scoring/notation-requirements.md#Labels; sg-25:23, sg-21:19). Whether the 2025 wording is durable is recorded as unresolved (research/units/unit-07-differential-equations.md#Unresolved).
- Direction of an approximation (BC-QA-07005), 2 points: BC-PT-99027 for the second derivative in terms of the dependent variable (an expression left in the first derivative does not earn it, sg-23:11), BC-PT-99026 for the direction with a reason from the sign of the second derivative, a decreasing first derivative, or concavity, closed by the conclusion; an argument at a single point fails (sg-23:10, sg-26:12).
- Behaviour from the equation (BC-QA-07010), 3 points in 2024: considering the sign of the derivative, the input, the answer with justification; a second derivative evaluation is an accepted alternate (sg-24:10). The recorded parts carry BC-PT-99027, 99023, 99010, 99063 and 99005.
- Verification (BC-QA-07007): BC-PT-99005, 99068 (a chain closed on the target), 99004 on BC-FRQ-2015-Q4-D; the scoring pattern is recorded by analogy (sg-23:12).

## 3. Cross-concept patterns

### Which concepts the stems combine

Computed from each archetype's `skills` mapped to concepts:

- BC-CON-07005 is loaded by four archetypes (BC-QA-07001, 07002, 07005, 07010) and BC-CON-07008 by three (BC-QA-07003, 07007, 07011); every other concept by one or two.
- BC-QA-07003 joins BC-CON-07007 and BC-CON-07008 (separate, then fix the constant and the branch). BC-QA-07011 joins BC-CON-07008, BC-CON-07009 and BC-CON-07010.
- BC-QA-07002 and BC-QA-07010 join BC-CON-07004 and BC-CON-07005 (the zero-slope locus and the solution's behaviour). BC-QA-07005 joins BC-CON-07005 and BC-CON-07006 (concavity of the solution decides the approximation's direction).
- BC-QA-07007 joins BC-CON-07002, BC-CON-07003 and BC-CON-07008. BC-QA-07009 joins BC-CON-07011 and BC-CON-07012.
- Across units: the direction question reaches Unit 4 tangent lines and Unit 5 concavity (BC-FRQ-2023-Q3-B is BC-QA-04008; BC-FRQ-2023-Q3-C loads BC-SKL-04030, 04031, 05046), the behaviour question reaches Unit 5 (BC-FRQ-2024-Q3-B is BC-QA-05007), Euler and separation share a question with Unit 10 series parts (BC-FRQ-2021-Q5-A, BC-FRQ-2025-Q5-A and B), and separation reaches Unit 6 antidifferentiation (research/units/unit-07-differential-equations.md#What Unit 7 depends on; research/units/unit-07-differential-equations.md#What depends on Unit 7).

### Recognition features between neighbouring concepts, and the first written line

| Neighbours | What in the stem selects each | First written line | Source |
|---|---|---|---|
| Separable against not separable (BC-CON-07007) | The right side factors as a function of the independent variable times a function of the dependent variable; a sum in both variables with no common factor is not separable | separable: the equation with the dependent factor and its differential on one side and the independent factor and its differential on the other; not separable: the statement that no such factoring exists | BC-QA-07012 `expected_solution_path`, `wrong_approaches` ("dividing each term by y separately"); research/units/unit-07-differential-equations.md#7.6 Finding General Solutions Using Separation of Variables; BC-ERR-07028 |
| General against particular solution (BC-CON-07003, BC-CON-07008) | "the particular solution ... with the given initial condition" or a stated value selects particular; "general solution" or no condition selects the family with \(C\) left | general: the antiderivative equation with one \(C\); particular: the same equation with the initial values substituted before solving | BC-QA-07003 `typical_wording`; BC-SKL-07033; BC-EK-FUN-7E1 (ced:143); BC-ERR-07009, BC-ERR-07033 |
| Verifying against solving (BC-CON-07002, BC-CON-07007) | "show that the given function is a solution" or "which of the following functions is a solution" supplies a candidate; "use separation of variables to find" supplies none | verify: the derivative of the candidate, then both sides with the candidate substituted; solve: the separated form | BC-QA-07007 `wrong_approaches` ("solving the equation from scratch when a verification was asked for"); BC-QA-07003 |
| Slope field against solution curve (BC-CON-07004, BC-CON-07005) | "sketch the slope field ... at the indicated points" asks for segments; "sketch the solution curve through the given point" on a printed field asks for one curve | field: the slope value at each indicated point; curve: the initial point located, then the curve following the segments both ways | BC-QA-07002, BC-QA-07001 `typical_wording` and `expected_solution_path`; BC-PT-99083 `does_not_earn` (a solution curve drawn in place of the field) |
| Euler's method against exact solution (BC-CON-07006, BC-CON-07007) | "use Euler's method ... with two steps of equal size ... approximate" selects stepping; "find the particular solution" selects separation. BC-QA-07004's rival is solving and evaluating | Euler: the step size, then \(y_1=y_0+\Delta x\cdot f(x_0,y_0)\); exact: the separated form | BC-QA-07004 `wrong_approaches`; BC-QA-07003 |
| Tangent-line direction against Euler value (BC-CON-07005, BC-CON-07006) | "is the approximation an overestimate or an underestimate ... give a reason" asks for the second derivative, not a new value | \(\frac{d^2y}{dx^2}\) differentiated implicitly with the equation substituted for \(\frac{dy}{dx}\) | BC-QA-07005 `expected_solution_path`; BC-ERR-07018 |
| Exponential against logistic growth (BC-CON-07010, BC-CON-07011) | "proportional to the quantity" gives \(\frac{dy}{dt}=ky\); "jointly proportional to the quantity and the difference between the quantity and" a level gives \(\frac{dy}{dt}=ky(a-y)\) | the equation with the constant of proportionality written | BC-EK-FUN-7F2 (ced:144), BC-EK-FUN-7H1 (ced:145); BC-ERR-07039; BC-MIS-07024 |
| Carrying capacity from the equation against from the graph (BC-CON-07012, BC-CON-07005) | An equation in the stem: the nonzero zero of the right side. A printed field or graph: the level of the horizontal segments the curves approach | equation: the right side set to zero; field: the horizontal segments located | BC-SKL-07040, BC-QA-07009 `expected_solution_path`; BC-SKL-07017 (long-run behaviour from the field); research/units/unit-07-differential-equations.md#7.9 Logistic Models with Differential Equations. No Unit 7 skill reads a carrying capacity from a solution graph; the field reading is BC-SKL-07017 [inferred that the two readings coincide for a logistic field; settled by an archetype loading BC-SKL-07017 and BC-SKL-07040 on one stem] |
| Behaviour from the equation against from a solution (BC-CON-07005) | "for the stated range, find the input at which ... has a critical point" with an equation supplied selects the right side set to zero; solving first is BC-QA-07010's rival | the right side set equal to zero | BC-QA-07010; BC-ERR-99035 |

### The confusable set

`tools/check_lessons.py --sets` prints ten sets; one is in Unit 7.

- LSN-DEC-07-01: BC-SKL-07041 (determine the limiting value without solving the equation) against BC-SKL-07042 (determine the value at which the quantity changes fastest). Both are in BC-CON-07012; each names the other in `confusable_with` (with BC-SKL-06065). Archetype: BC-QA-07009, which loads both. Selecting feature, from its `typical_wording`: "the limit of the quantity as the independent variable grows without bound" selects BC-SKL-07041, whose first line is the zeros of the right side and the sign of the right side on the side of the initial value; "the value of the quantity when it is changing fastest" selects BC-SKL-07042, whose first line is the right side as a quadratic in the quantity, maximised at half the carrying capacity (BC-EK-FUN-7H3, BC-EK-FUN-7H4, ced:145). Errors the wrong choice produces: BC-ERR-07042 (fastest change value reported as the carrying capacity), BC-ERR-07041 (limiting value asserted with no reference to the sign of the rate). Misconceptions: BC-MIS-07027 (the quantity changes fastest at the carrying capacity), BC-MIS-07026.

The other contrasts in the table above (verify against solve, Euler against exact, exponential against logistic) are not derived sets, so they are taught inside the concept lessons' Recognition and Method choice sections, not in a decision lesson.

## 4. Recurring traps

### Error records across two or more Unit 7 concepts

Computed: each BC-ERR in `data/errors.json` whose `skills` meet two or more Unit 7 concepts. Scoring consequences are quoted from the records.

| Error | Concepts | Scoring consequence (record) |
|---|---|---|
| BC-ERR-99014 Separable differential equation separated or antidifferentiated incorrectly | BC-CON-07007, 07008 | "The separation, antiderivative and constant points are assessed separately, so an early slip costs several points in the part." |
| BC-ERR-99024 Solution curve sketched incorrectly on a slope field | BC-CON-07004, 07005 | "a curve that crosses the asymptote or stops short loses the point." |
| BC-ERR-99035 Differential equation solved where it already supplies the slope | BC-CON-07001, 07004 | "The slope point is at risk and the part is often left incomplete." |
| BC-ERR-07001 Proportionality written without a constant | BC-CON-07001, 07010 | "The model is wrong by a factor and every later value built on it is wrong." |
| BC-ERR-07009 General solution reported as the only solution | BC-CON-07003, 07008 | "The distinction the essential knowledge draws between a family and a particular solution is lost." |
| BC-ERR-07013 Dependence on a variable misread from the field | BC-CON-07004, 07005 | "The match to a candidate equation is made on a false feature." |
| BC-ERR-07018 Direction of an approximation claimed from increase or decrease | BC-CON-07005, 07006 | "The reason point is lost; the guideline requires the second derivative, the monotonicity of the first derivative, or the concavity." |
| BC-ERR-07044 Logistic equation solved where reasoning from it was asked for | BC-CON-07011, 07012 | "Time is spent on work the question did not ask for, and an error inside it costs the value that the equation alone would have given." |

Single-concept records with the heaviest stated consequences, which designers of those lessons meet first: BC-ERR-07024 (no separation: "All four points of the separation part are lost"), BC-ERR-07026 (constant omitted: "At most the first two points are available"), BC-ERR-07027 (answer left implicit: "The final solving point is lost"), BC-ERR-07015 (curve across an equilibrium level), BC-ERR-07021 (second Euler step restarted from the initial value), BC-ERR-07022 (no visible steps).

The research file maps the Chief Reader records to the unit records: BC-ERR-99014 to BC-ERR-07024, 07025, 07029; BC-ERR-99024 to 07014, 07015; BC-ERR-99026 to 07019, 07020, 07021; BC-ERR-99035 to 07041, 07044; BC-ERR-99020 to 07018, 07023 (research/units/unit-07-differential-equations.md#Archetype summary; cr-22:18, cr-23:11, cr-24:11, crabbc-25:34).

### Misconception records across two or more Unit 7 concepts

Computed from `data/misconceptions.json` `skills` mapped to concepts:

| Misconception | Severity | Concepts |
|---|---|---|
| BC-MIS-07001 Proportional to means equal to | high | BC-CON-07001, 07010 |
| BC-MIS-07003 An initial condition is part of the differential equation | medium | BC-CON-07001, 07002 |
| BC-MIS-07005 A differential equation has one solution | high | BC-CON-07003, 07008 |
| BC-MIS-07006 A slope field shows values of the solution | high | BC-CON-07004, 07005 |
| BC-MIS-07010 The direction of an approximation follows from increase or decrease | high | BC-CON-07005, 07006 |
| BC-MIS-07016 The constant of integration is optional | high | BC-CON-07007, 07008 |
| BC-MIS-07020 A particular solution must be written in closed form | medium | BC-CON-07008, 07010 |
| BC-MIS-07023 A numerical answer is a complete interpretation | medium | BC-CON-07010, 07011 |
| BC-MIS-07026 The limit of a solution needs the solution formula | high | BC-CON-07011, 07012 |

The research file names four highest-severity clusters: separation without both differentials and the constant (BC-MIS-07014, 07015, 07016, sg-23:12); the field read as solution values or a curve drawn across an equilibrium (BC-MIS-07006, 07008, 07009, sg-23:9); each Euler step restarted from the initial value (BC-MIS-07011, 07012, sg-24:17); a logistic model that must be solved first (BC-MIS-07025, 07026, ced:145) (research/units/unit-07-differential-equations.md#Misconception summary). No concept's `misconceptions` list names a retired record. Traps blocks copy `observed_behavior` and `scoring_consequence` and never state the error as a belief (docs/lessons/TEMPLATE.md, Traps).

### Point losses research/scoring names for this unit's shapes

- Separable equation separated with a constant on the wrong side, or antidifferentiated incorrectly, BC-ERR-99014 (research/scoring/common-point-losses.md#Setup points; cr-23:12, cr-24:11, cr-24:12).
- Euler's method run with the wrong initial value, step size or slope, BC-ERR-99026 (research/scoring/common-point-losses.md#Answer points; cr-24:32, crabbc-25:34).
- Over or underestimate claimed without appealing to concavity, BC-ERR-99020 (research/scoring/common-point-losses.md#Justification points; cr-23:11, cr-23:12).
- Solution curve on a slope field that crosses an asymptote, stops short, or shows a family, BC-ERR-99024 (research/scoring/common-point-losses.md#Precision and presentation points; cr-23:12, cr-24:11).
- Differentials and derivatives mixed, BC-ERR-99013, and vague referents such as "the slope", BC-ERR-99001 (research/scoring/common-point-losses.md#Notation points).
- A slope field reason must name the sign of the drawn segments; a direction reason must run from the second derivative to concavity to the tangent line's position (research/scoring/justification-requirements.md#Reasons about slope fields and concavity).
- A critical point classification from the equation needs sign analysis closed by a claim over the interval (research/scoring/justification-requirements.md#Sign analysis of a derivative; BC-PT-99010).
- What is not a loss: absolute value on a logarithm is optional in separation (sg-23:12, sg-26:13, sg-21:20), and an Euler table need not be labelled when the answer is correct (sg-25:23, sg-21:19) (research/scoring/notation-requirements.md#Parentheses; research/scoring/notation-requirements.md#Labels).
- The diagnostic distinction "Initial condition or constant of integration dropped" is recorded on 13 entries, including BC-FRQ-2019-Q4-C (research/question-analysis/frq-analysis.md#The diagnostic value of an FRQ part).

## 5. Time budgets per archetype shape

MCQ budgets are the part figures. An FRQ part's budget is its share of the 15.0 minutes by points out of 9, per plan 15 (docs/plan/15-lessons.md, Fluency, measured and never credited); point counts come from `scoring_pattern` or the official FRQ records. "Writes" names the steps that carry a point; "held" names steps with no point of their own. Which steps a fluent solver holds in the head is [inferred] from where the points sit; settled by timing data per step once the fluency telemetry exists.

| Shape | MCQ budget | FRQ points and budget | A fluent solver writes | Held |
|---|---|---|---|---|
| BC-QA-07001 sketch on a field | I-A 2.14 | 1 = 1.67 | the one curve through the point, edge to edge, on one side of the equilibrium | locating the horizontal segments |
| BC-QA-07002 field drawn or matched | I-A 2.14 | 2 on BC-FRQ-2015-Q4-A = 3.33; 1 on BC-FRQ-2026-Q3-A = 1.67 | the segments at the indicated points; for an explanation, one sentence on the sign of the segments' slopes | the slope arithmetic at each point |
| BC-QA-07003 separation with initial condition | I-A 2.14 | 4 = 6.67 (2019, 2023); 5 = 8.33 (2013, 2021, 2024, 2026) | separated form with both differentials; both antiderivatives with \(+C\); the initial values substituted; the explicit solution | the choice of branch when the initial value settles it in one line |
| BC-QA-07011 domain or accumulation form | I-A 2.14 | no points recorded | the particular solution and the interval containing the initial input; or \(y_0+\int_a^x f(t)\,dt\) | where the expression is undefined |
| BC-QA-07012 separable or not | I-A 2.14 | first point of a separation part | the factored right side, then the separated form, or the not-separable statement | the search for a common factor |
| BC-QA-07004 Euler | I-A 2.14 | 2 = 3.33 | the step size; each step as old value plus step size times slope at the current point, or a labelled table; the approximation | nothing further, since the steps are the demonstration point |
| BC-QA-07005 direction of an approximation | I-A 2.14 | 2 = 3.33 | the second derivative in the dependent variable; its sign on the interval; the direction with the concavity reason | the substitution of \(\frac{dy}{dx}\) |
| BC-QA-07010 behaviour from the equation | I-A 2.14 | 3 = 5.0 (2024, 2019); 2 on 2015; 1 on 2026 | the right side set to zero, the input, the sign on each side with the classification | using the supplied bound to cancel a factor |
| BC-QA-07007 verification | I-A 2.14 | 3 on BC-FRQ-2015-Q4-D = 5.0 | the derivative of the candidate, both sides substituted, the verdict, the initial check | nothing (every step is the demonstration) |
| BC-QA-07006 modelling | I-A 2.14 or I-B 2.92 | no points recorded | the equation with \(k\), the initial condition on its own line | naming the variables and units |
| BC-QA-07008 exponential model | I-A 2.14 or I-B 2.92 | no points recorded [inferred from the scoring pattern: the separation points plus one interpretation point; settled by a rubric] | \(y=y_0e^{kt}\), the equation for \(k\) from the second pair, the interpretation with units | the separation when the form is known (BC-EK-FUN-7G1) |
| BC-QA-07009 logistic without solving | I-A 2.14 or I-B 2.92 | no points recorded [inferred: value and reason per result; settled by a rubric] | the carrying capacity with the reason from the equation's zeros and sign; half the carrying capacity for fastest change | the quadratic's vertex |

## 6. Delivery map

TEMPLATE selection rules (docs/lessons/TEMPLATE.md, Delivery): 1 worked examples and error blocks are `step_reveal`; 2 a key idea describing a process is `motion`, with `model` on the example only where a computed sequence of values is the idea; 3 figure-bearing BC-REP (02, 07, 08, 12, 13, 14) gives `figure`, promoted to `interactive` when `common_givens` or `difficulty_variables` name a varying quantity and the stem asks for a reading; 4 BC-REP-03 givens give `table`; 5 everything else is `text`. Rule 1 applies to every concept's worked examples and error blocks, so it is not repeated per row. Key idea wording is from the topic's Required mathematical knowledge paragraph (research/units/unit-07-differential-equations.md, each topic's `### Required mathematical knowledge`). Every non-text choice is [inferred], settled by the modality A/B the TEMPLATE names.

| Concept | Orientation | Key ideas (BC-EK) and mode | Rule and triggering field |
|---|---|---|---|
| BC-CON-07001 | text | FUN-7A1 text | rule 5, representations BC-REP-04, 05, 06 on BC-SKL-07001 to 07005 |
| BC-CON-07002 | text | FUN-7B1 text | rule 5, BC-REP-01, 06 on BC-SKL-07006, 07007, 07008 |
| BC-CON-07003 | text | FUN-7B2 text | rule 5, BC-REP-01, 04, 06 on BC-SKL-07009 |
| BC-CON-07004 | figure | FUN-7C1 figure (a grid of segments, the slope value written inside at two lattice points); FUN-7C2 figure (the horizontal row at the zero-slope level, and a field constant along vertical lines) | rule 3, BC-REP-07 on all four skills; not promoted, since BC-QA-07002 `difficulty_variables` vary a form ("whether the right side contains one variable or both", "whether the zero slope locus is a line or a curve"), not a quantity |
| BC-CON-07005 | interactive (a printed field with one draggable initial point; the curve through it redrawn; reading: which side of the equilibrium the curve stays on and what it approaches) | FUN-7C3 `motion` (a solution curve traced through the field, tangent to the segment at each point it passes, frames stepping left and right from the initial point) | orientation: rule 3 promoted, BC-REP-07 and 02 on BC-SKL-07014 to 07017, BC-QA-07001 `common_givens` "an initial condition" and `difficulty_variables` "where the initial point sits relative to it", stem asks for a reading ("sketch the solution curve through the given point"). FUN-7C3: rule 2, "follows the segments of the field, so it is tangent to the segment at every point it passes" is a curve being traced |
| BC-CON-07006 | table (step table: input, output, slope, increment) | FUN-7C4 `motion` (Euler steps stepping along: tangent segment from the current point, the new point replacing the old, the true curve beside); example: `model` (Euler's method computed step by step in a table, with the figure of the steps) | orientation: rule 4, BC-REP-03 on BC-SKL-07019 to 07022 and BC-QA-07004 `representations`. FUN-7C4: rule 2, "the new point then replaces the old one" is a process, and the computed sequence of approximations is the idea, so `model` on the example |
| BC-CON-07007 | text | FUN-7D1 text; FUN-7D2 text | rule 5, BC-REP-01, 06 only on BC-SKL-07024 to 07028. The content is a sequence of written lines (separate, antidifferentiate, one constant, solve), which `step_reveal` carries in the worked example |
| BC-CON-07008 | text | FUN-7E1 text; FUN-7E2 text | rule 5, BC-REP-01, 04, 06 on BC-SKL-07029, 07030, 07032, 07033 |
| BC-CON-07009 | text | FUN-7E3 text | rule 5, BC-REP-01, 04 on BC-SKL-07031 |
| BC-CON-07010 | text | FUN-7F1 text; FUN-7F2 text; FUN-7G1 table (the initial value and the second data pair, then \(k\)) | rule 5 for BC-SKL-07034, 07035, 07037, 07038; rule 4, BC-REP-03 on BC-SKL-07036 |
| BC-CON-07011 | text | FUN-7H1 text; FUN-7H2 text | rule 5, BC-REP-04, 05, 06 on BC-SKL-07039, 07043 |
| BC-CON-07012 | text | FUN-7H3 text; FUN-7H4 text | rule 5, BC-REP-06, 04, 01 on BC-SKL-07040 to 07042; see the interactive note below |

Where each mode fits, in summary:

- Motion: a solution curve traced through a slope field (LSN-CON-07005, FUN-7C3) and Euler steps stepping along (LSN-CON-07006, FUN-7C4). Both are processes the TEMPLATE mode table names ("Euler steps", "a slope field being traced"). Every motion entry carries `reduced_motion` and a static fallback of frames side by side (TEMPLATE, Delivery).
- Model: Euler's method computed step by step in a table, on LSN-CON-07006's example. No Unit 7 concept is in `PRODUCTIVE_FAILURE_TARGETS` (app/engine/constants.py). BC-QA-07012 carries BC-DF-15, one of `PRODUCTIVE_FAILURE_FACTORS`, which the TEMPLATE mode table ties to `model`; a separability judgment is not a computed sequence of values, so LSN-CON-07007 stays text and step reveal [inferred; settled by the build plan deciding whether the BC-DF-15 clause applies to a concept outside `PRODUCTIVE_FAILURE_TARGETS`].
- Interactive: a slope field with a draggable initial point (LSN-CON-07005 orientation). A logistic curve with the carrying capacity moved is not selected by the rules: BC-SKL-07040 to 07042 carry no figure-bearing BC-REP and the 7.9 Representations paragraph names no graphical conversion (research/units/unit-07-differential-equations.md#7.9 Logistic Models with Differential Equations), although BC-QA-07009 `difficulty_variables` names a varying quantity ("whether the initial value is above or below the carrying capacity"). Serving it needs BC-REP-02 on BC-SKL-07041 or a TEMPLATE amendment [inferred]; until then LSN-CON-07012 is text.
- Static figure or table is enough: the slope field grid and its zero-slope row (LSN-CON-07004), the step table orientation (LSN-CON-07006), the data pairs that fix \(k\) (LSN-CON-07010).
- Text and step reveal only: separation of variables (LSN-CON-07007), the particular solution and its domain (07008, 07009), modelling, verification and families (07001, 07002, 07003), and the logistic reasoning (07011, 07012). Their representations are BC-REP-01, 04, 05 and 06, none figure-bearing.

## Library gaps met

- Concept cycle: BC-CON-07011 and BC-CON-07012 are each other's hard parents through BC-SKL-07039 to 07040 and BC-SKL-07041, 07042 to 07043. Either BC-SKL-07043 belongs in BC-CON-07012, or the lesson order must be read at skill level as in section 1.
- BC-SKL-06057 (integration by parts) is a hard parent of BC-SKL-07004 (identify the initial condition in a context) with no reason in the research file's edge narrative; likely a mis-keyed edge [inferred; settled by the edge's `note` in data/staging/unit-07.edges.csv].
- BC-QA-07003 lists BC-PT-99033, whose `earns` text is an initial value added to a definite integral; the separation rubric's constant point is BC-PT-99031. BC-PT-99033 appears only on BC-FRQ-2013-Q5-C among the separation records.
- BC-QA-07006, 07008, 07009 and 07011 carry no `point_types`; BC-QA-07008's scoring pattern names an interpretation point (sg-23:2) that BC-PT-99007 would fit.
- No Unit 7 skill reads a carrying capacity from a solution graph or field; the "from the graph" contrast rests on BC-SKL-07017.
- BC-QA-07012 is absent from the research file's archetype table (eleven listed).
- No logistic, from-scratch field, verification or exponential free-response part in 2023 to 2025 (research/units/unit-07-differential-equations.md#Unresolved).
- Most Unit 7 BC-ERR records have no `status` field set (only BC-ERR-07026 among unit records reads active); the loader treated them as present.

## 7. Sources

Library records: BC-UNIT-07; BC-TOP-0701 to BC-TOP-0709; BC-CON-07001 to BC-CON-07012; BC-SKL-07001 to BC-SKL-07043; BC-EK-FUN-7A1, 7B1, 7B2, 7C1 to 7C4, 7D1, 7D2, 7E1 to 7E3, 7F1, 7F2, 7G1, 7H1 to 7H4; BC-QA-07001 to BC-QA-07012; BC-QA-04008, BC-QA-05007; BC-PT-99004, 99005, 99007, 99010, 99023, 99026, 99027, 99028, 99029, 99030, 99031, 99032, 99033, 99034, 99063, 99065, 99066, 99068, 99083; BC-ERR-99001, 99004, 99013, 99014, 99020, 99024, 99026, 99035, BC-ERR-07001 to BC-ERR-07044; BC-MIS-07001 to BC-MIS-07027; BC-DF-15; BC-REP-01 to 07; BC-PRQ-05001, 05003, 06003, 06005, 07001 to 07006; outside skills BC-SKL-02013, 03002, 04001, 04013, 04030, 05014, 05030, 05046, 05052, 06034, 06044, 06047, 06057, 06064, 06065; BC-TOP-0205, BC-TOP-0301.

Official records: BC-FRQ-2013-Q5-B, 2013-Q5-C, 2015-Q4-A, 2015-Q4-B, 2015-Q4-D, 2019-Q4-B, 2019-Q4-C, 2021-Q5-A, 2021-Q5-B, 2021-Q5-C, 2023-Q3-A to D, 2024-Q3-A to C, 2024-Q5-C, 2025-Q5-A, 2025-Q5-B, 2025-Q5-D, 2026-Q3-A to D; BC-MCQ-CED-009, CED-017, SAMPLE-005, SAMPLE-010, SAMPLE-018, PE2012-012, PE2012-014, PE2012-016, PE2012-023.

Pages: ced:137, ced:138, ced:139, ced:140, ced:141, ced:142, ced:143, ced:144, ced:145; sg-19:5, sg-21:19, sg-21:20, sg-22:8, sg-23:2, sg-23:9, sg-23:10, sg-23:11, sg-23:12, sg-24:3, sg-24:9, sg-24:10, sg-24:11, sg-24:17, sg-25:23, sg-26:11, sg-26:12, sg-26:13; samples-15-q4:1; cr-22:18, cr-23:11, cr-23:12, cr-24:11, cr-24:12, cr-24:32, crabbc-25:34.

Research headings:
- research/units/unit-07-differential-equations.md: Unit 7, Differential Equations; each topic's Required mathematical knowledge, Representations and Assessment behaviour (7.1 to 7.9); What Unit 7 depends on; What depends on Unit 7; Archetype summary; Misconception summary; Unresolved; Official evidence index [verified].
- research/exam/exam-structure.md: Section and part layout; Free-response point totals.
- research/scoring/common-point-losses.md: Setup points; Answer points; Justification points; Notation points; Precision and presentation points.
- research/scoring/notation-requirements.md: Labels; Parentheses.
- research/scoring/justification-requirements.md: Sign analysis of a derivative; Reasons about slope fields and concavity.
- research/question-analysis/question-archetypes.md: Family de-modelling; Family de-qualitative-behaviour; Family de-verification; Family euler; Family exponential-model; Family logistic-model; Family separation-of-variables; Family slope-field; BC-QA-07012.
- research/question-analysis/frq-analysis.md: The calculator questions and the no-calculator questions; The diagnostic value of an FRQ part.

Repository files: docs/lessons/TEMPLATE.md (Delivery, Scoring, Traps); docs/plan/15-lessons.md (What a lesson is, and its granularity; Methods, thought process and scoring habits; Fluency, measured and never credited); data/prereq_edges.csv; data/errors.json; data/misconceptions.json; app/engine/constants.py (`PRODUCTIVE_FAILURE_TARGETS`, `PRODUCTIVE_FAILURE_FACTORS`); tools/check_lessons.py --sets.
