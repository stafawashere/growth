---
title: AP Calculus BC Skill Taxonomy
research_date: 2026-09-19
status: draft
purpose: The full inventory of atomic skills in data/skills.json, one table per CED unit, with counts per unit and per topic, the ID scheme reminder, and the granularity justifications collected from the unit files.
---

# AP Calculus BC Skill Taxonomy

This file is a view over `../../data/skills.json`. The registry is the source of truth for every column below. Names are reproduced verbatim from the `name` field; the `description_plain` and `description_formal` fields, the adaptive metadata, and the error and misconception links stay in the registry and are not duplicated here.

## ID scheme reminder [inferred]

Minted ids use a two-digit block followed by a three-digit sequence, where the block is the CED unit number, 00 for cross-cutting records, and 99 for synthesis records. BC-SKL-06017 is therefore the seventeenth atomic skill minted in the Unit 6 block. Deterministic ids are derived instead of minted: BC-UNIT-06 from the unit number, BC-TOP-0603 from the unit and topic numbers, BC-LO-FUN-6A and BC-EK-FUN-6A1 from the CED codes with the dots removed. CED codes are attributes on records and never keys, so a CED rewording does not retire an id. Ids are append-only; a retired id keeps a tombstone with `superseded_by` in `../../data/ids.json`. Concepts (BC-CON), non-calculus prerequisites (BC-PRQ), archetypes (BC-QA), errors (BC-ERR), misconceptions (BC-MIS), and diagnostic signals (BC-SIG) use the same block plus sequence form. Full table in ../README.md.

## Counts per unit [inferred]

| Unit | Name | Topics | Concepts | Skills | BC-PRQ minted in block |
|---|---|---|---|---|---|
| BC-UNIT-01 | Limits and Continuity | 16 | 19 | 68 | 10 |
| BC-UNIT-02 | Differentiation: Definition and Fundamental Properties | 10 | 15 | 46 | 5 |
| BC-UNIT-03 | Differentiation: Composite, Implicit, and Inverse Functions | 6 | 10 | 34 | 7 |
| BC-UNIT-04 | Contextual Applications of Differentiation | 7 | 15 | 38 | 9 |
| BC-UNIT-05 | Applying Derivatives to Analyze Functions | 12 | 15 | 63 | 8 |
| BC-UNIT-06 | Integration and Accumulation of Change | 14 | 20 | 74 | 13 |
| BC-UNIT-07 | Differential Equations | 9 | 12 | 43 | 6 |
| BC-UNIT-08 | Applications of Integration | 13 | 21 | 59 | 7 |
| BC-UNIT-09 | Parametric Equations, Polar Coordinates, and Vector-Valued Functions | 9 | 17 | 43 | 4 |
| BC-UNIT-10 | Infinite Sequences and Series | 15 | 26 | 73 | 8 |
| Total | | 111 | 170 | 541 | 77 |

## Counts per topic [inferred]

Topics with no skills registered against them do not appear. Counts are of BC-SKL records whose `topic` field names the topic.

| Topic | CED code | Name | Skills |
|---|---|---|---|
| BC-TOP-0101 | 1.1 | Introducing Calculus: Can Change Occur at an Instant? | 4 |
| BC-TOP-0102 | 1.2 | Defining Limits and Using Limit Notation | 4 |
| BC-TOP-0103 | 1.3 | Estimating Limit Values from Graphs | 6 |
| BC-TOP-0104 | 1.4 | Estimating Limit Values from Tables | 3 |
| BC-TOP-0105 | 1.5 | Determining Limits Using Algebraic Properties of Limits | 6 |
| BC-TOP-0106 | 1.6 | Determining Limits Using Algebraic Manipulation | 5 |
| BC-TOP-0107 | 1.7 | Selecting Procedures for Determining Limits | 3 |
| BC-TOP-0108 | 1.8 | Determining Limits Using the Squeeze Theorem | 4 |
| BC-TOP-0109 | 1.9 | Connecting Multiple Representations of Limits | 3 |
| BC-TOP-0110 | 1.10 | Exploring Types of Discontinuities | 4 |
| BC-TOP-0111 | 1.11 | Defining Continuity at a Point | 3 |
| BC-TOP-0112 | 1.12 | Confirming Continuity over an Interval | 4 |
| BC-TOP-0113 | 1.13 | Removing Discontinuities | 4 |
| BC-TOP-0114 | 1.14 | Connecting Infinite Limits and Vertical Asymptotes | 4 |
| BC-TOP-0115 | 1.15 | Connecting Limits at Infinity and Horizontal Asymptotes | 6 |
| BC-TOP-0116 | 1.16 | Working with the Intermediate Value Theorem (IVT) | 5 |
| BC-TOP-0201 | 2.1 | Defining Average and Instantaneous Rates of Change at a Point | 5 |
| BC-TOP-0202 | 2.2 | Defining the Derivative of a Function and Using Derivative Notation | 8 |
| BC-TOP-0203 | 2.3 | Estimating Derivatives of a Function at a Point | 5 |
| BC-TOP-0204 | 2.4 | Connecting Differentiability and Continuity: Determining When Derivatives Do and Do Not Exist | 6 |
| BC-TOP-0205 | 2.5 | Applying the Power Rule | 3 |
| BC-TOP-0206 | 2.6 | Derivative Rules: Constant, Sum, Difference, and Constant Multiple | 4 |
| BC-TOP-0207 | 2.7 | Derivatives of cos x, sin x, e^x, and ln x | 4 |
| BC-TOP-0208 | 2.8 | The Product Rule | 3 |
| BC-TOP-0209 | 2.9 | The Quotient Rule | 4 |
| BC-TOP-0210 | 2.10 | Finding the Derivatives of Tangent, Cotangent, Secant, and/or Cosecant Functions | 4 |
| BC-TOP-0301 | 3.1 | The Chain Rule | 6 |
| BC-TOP-0302 | 3.2 | Implicit Differentiation | 8 |
| BC-TOP-0303 | 3.3 | Differentiating Inverse Functions | 6 |
| BC-TOP-0304 | 3.4 | Differentiating Inverse Trigonometric Functions | 5 |
| BC-TOP-0305 | 3.5 | Selecting Procedures for Calculating Derivatives | 4 |
| BC-TOP-0306 | 3.6 | Calculating Higher-Order Derivatives | 5 |
| BC-TOP-0401 | 4.1 | Interpreting the Meaning of the Derivative in Context | 5 |
| BC-TOP-0402 | 4.2 | Straight-Line Motion: Connecting Position, Velocity, and Acceleration | 7 |
| BC-TOP-0403 | 4.3 | Rates of Change in Applied Contexts Other Than Motion | 4 |
| BC-TOP-0404 | 4.4 | Introduction to Related Rates | 6 |
| BC-TOP-0405 | 4.5 | Solving Related Rates Problems | 5 |
| BC-TOP-0406 | 4.6 | Approximating Values of a Function Using Local Linearity and Linearization | 5 |
| BC-TOP-0407 | 4.7 | Using L’Hospital’s Rule for Determining Limits of Indeterminate Forms | 6 |
| BC-TOP-0501 | 5.1 | Using the Mean Value Theorem | 6 |
| BC-TOP-0502 | 5.2 | Extreme Value Theorem, Global Versus Local Extrema, and Critical Points | 7 |
| BC-TOP-0503 | 5.3 | Determining Intervals on Which a Function is Increasing or Decreasing | 5 |
| BC-TOP-0504 | 5.4 | Using the First Derivative Test to Determine Relative (Local) Extrema | 5 |
| BC-TOP-0505 | 5.5 | Using the Candidates Test to Determine Absolute (Global) Extrema | 6 |
| BC-TOP-0506 | 5.6 | Determining Concavity of Functions over Their Domains | 6 |
| BC-TOP-0507 | 5.7 | Using the Second Derivative Test to Determine Extrema | 4 |
| BC-TOP-0508 | 5.8 | Sketching Graphs of Functions and Their Derivatives | 5 |
| BC-TOP-0509 | 5.9 | Connecting a Function, Its First Derivative, and Its Second Derivative | 4 |
| BC-TOP-0510 | 5.10 | Introduction to Optimization Problems | 5 |
| BC-TOP-0511 | 5.11 | Solving Optimization Problems | 4 |
| BC-TOP-0512 | 5.12 | Exploring Behaviors of Implicit Relations | 6 |
| BC-TOP-0601 | 6.1 | Exploring Accumulations of Change | 4 |
| BC-TOP-0602 | 6.2 | Approximating Areas with Riemann Sums | 7 |
| BC-TOP-0603 | 6.3 | Riemann Sums, Summation Notation, and Definite Integral Notation | 5 |
| BC-TOP-0604 | 6.4 | The Fundamental Theorem of Calculus and Accumulation Functions | 5 |
| BC-TOP-0605 | 6.5 | Interpreting the Behavior of Accumulation Functions Involving Area | 6 |
| BC-TOP-0606 | 6.6 | Applying Properties of Definite Integrals | 6 |
| BC-TOP-0607 | 6.7 | The Fundamental Theorem of Calculus and Definite Integrals | 6 |
| BC-TOP-0608 | 6.8 | Finding Antiderivatives and Indefinite Integrals: Basic Rules and Notation | 7 |
| BC-TOP-0609 | 6.9 | Integrating Using Substitution | 6 |
| BC-TOP-0610 | 6.10 | Integrating Functions Using Long Division and Completing the Square | 4 |
| BC-TOP-0611 | 6.11 | Integrating Using Integration by Parts | 5 |
| BC-TOP-0612 | 6.12 | Integrating Using Linear Partial Fractions | 4 |
| BC-TOP-0613 | 6.13 | Evaluating Improper Integrals | 5 |
| BC-TOP-0614 | 6.14 | Selecting Techniques for Antidifferentiation | 4 |
| BC-TOP-0701 | 7.1 | Modeling Situations with Differential Equations | 5 |
| BC-TOP-0702 | 7.2 | Verifying Solutions for Differential Equations | 4 |
| BC-TOP-0703 | 7.3 | Sketching Slope Fields | 4 |
| BC-TOP-0704 | 7.4 | Reasoning Using Slope Fields | 5 |
| BC-TOP-0705 | 7.5 | Approximating Solutions Using Euler’s Method | 5 |
| BC-TOP-0706 | 7.6 | Finding General Solutions Using Separation of Variables | 5 |
| BC-TOP-0707 | 7.7 | Finding Particular Solutions Using Initial Conditions and Separation of Variables | 5 |
| BC-TOP-0708 | 7.8 | Exponential Models with Differential Equations | 5 |
| BC-TOP-0709 | 7.9 | Logistic Models with Differential Equations | 5 |
| BC-TOP-0801 | 8.1 | Finding the Average Value of a Function on an Interval | 5 |
| BC-TOP-0802 | 8.2 | Connecting Position, Velocity, and Acceleration of Functions Using Integrals | 6 |
| BC-TOP-0803 | 8.3 | Using Accumulation Functions and Definite Integrals in Applied Contexts | 6 |
| BC-TOP-0804 | 8.4 | Finding the Area Between Curves Expressed as Functions of x | 5 |
| BC-TOP-0805 | 8.5 | Finding the Area Between Curves Expressed as Functions of y | 4 |
| BC-TOP-0806 | 8.6 | Finding the Area Between Curves That Intersect at More Than Two Points | 4 |
| BC-TOP-0807 | 8.7 | Volumes with Cross Sections: Squares and Rectangles | 5 |
| BC-TOP-0808 | 8.8 | Volumes with Cross Sections: Triangles and Semicircles | 4 |
| BC-TOP-0809 | 8.9 | Volume with Disc Method: Revolving Around the x- or y-Axis | 4 |
| BC-TOP-0810 | 8.10 | Volume with Disc Method: Revolving Around Other Axes | 4 |
| BC-TOP-0811 | 8.11 | Volume with Washer Method: Revolving Around the x- or y-Axis | 4 |
| BC-TOP-0812 | 8.12 | Volume with Washer Method: Revolving Around Other Axes | 4 |
| BC-TOP-0813 | 8.13 | The Arc Length of a Smooth, Planar Curve and Distance Traveled | 4 |
| BC-TOP-0901 | 9.1 | Defining and Differentiating Parametric Equations | 6 |
| BC-TOP-0902 | 9.2 | Second Derivatives of Parametric Equations | 4 |
| BC-TOP-0903 | 9.3 | Finding Arc Lengths of Curves Given by Parametric Equations | 4 |
| BC-TOP-0904 | 9.4 | Defining and Differentiating Vector-Valued Functions | 4 |
| BC-TOP-0905 | 9.5 | Integrating Vector-Valued Functions | 4 |
| BC-TOP-0906 | 9.6 | Solving Motion Problems Using Parametric and Vector-Valued Functions | 6 |
| BC-TOP-0907 | 9.7 | Defining Polar Coordinates and Differentiating in Polar Form | 6 |
| BC-TOP-0908 | 9.8 | Find the Area of a Polar Region or the Area Bounded by a Single Polar Curve | 4 |
| BC-TOP-0909 | 9.9 | Finding the Area of the Region Bounded by Two Polar Curves | 5 |
| BC-TOP-1001 | 10.1 | Defining Convergent and Divergent Infinite Series | 5 |
| BC-TOP-1002 | 10.2 | Working with Geometric Series | 5 |
| BC-TOP-1003 | 10.3 | The nth Term Test for Divergence | 3 |
| BC-TOP-1004 | 10.4 | Integral Test for Convergence | 4 |
| BC-TOP-1005 | 10.5 | Harmonic Series and p-Series | 4 |
| BC-TOP-1006 | 10.6 | Comparison Tests for Convergence | 5 |
| BC-TOP-1007 | 10.7 | Alternating Series Test for Convergence | 4 |
| BC-TOP-1008 | 10.8 | Ratio Test for Convergence | 3 |
| BC-TOP-1009 | 10.9 | Determining Absolute or Conditional Convergence | 5 |
| BC-TOP-1010 | 10.10 | Alternating Series Error Bound | 4 |
| BC-TOP-1011 | 10.11 | Finding Taylor Polynomial Approximations of Functions | 6 |
| BC-TOP-1012 | 10.12 | Lagrange Error Bound | 4 |
| BC-TOP-1013 | 10.13 | Radius and Interval of Convergence of Power Series | 7 |
| BC-TOP-1014 | 10.14 | Finding Taylor or Maclaurin Series for a Function | 8 |
| BC-TOP-1015 | 10.15 | Representing Functions as Power Series | 6 |

## Granularity notes [inferred]

Topics that carry six or more skills record why the decomposition is that fine. These notes are collected verbatim from the unit files; the remaining topics decompose one skill per essential knowledge demand and carry no note.

- Granularity note: Topic 2.2 carries eight skills because BC-EK-CHA-2B1 names two equivalent limit forms at a point, BC-EK-CHA-2B2 adds the derivative as a function, BC-EK-CHA-2B3 names three notations, BC-EK-CHA-2B4 requires four representations, and BC-EK-CHA-2C1 adds the tangent line, and these are independently testable.

- Granularity note: Topic 3.2 carries eight skills because the single essential knowledge statement compresses a procedure whose steps fail independently in the record: attaching the dy/dx factor to a y term, applying the product rule to a mixed term, keeping the equation an equation, isolating dy/dx, evaluating at a point, and locating horizontal and vertical tangents are each scored separately in the tasks the Chief Reader reports describe (cr-23:22, cr-24:17, crabbc-25:24). This topic is also the hidden prerequisite for the Unit 4 related rates topics, where the same six steps recur with time as the independent variable.

- Granularity note: Topic 4.2 carries seven skills because the single essential knowledge statement names four quantities, position, speed, velocity, and acceleration, and the scoring record separates abilities that the statement compresses. The 2025 rubric attaches separate points to considering the sign of a velocity, to analysing that sign for one particle, to analysing it for both particles across the whole interval, and to the speed conclusion, and the Chief Reader report records mean scores of 0.04 and 0.03 on the two analysis points (crabbc-25:20, crabbc-25:22). Producing velocity, producing acceleration, converting velocity to speed, reading direction, deciding whether speed increases, locating rest, and communicating the analysis therefore stand as separate testable abilities.

- Granularity note: Topic 6.2 carries seven skills because the CED names four distinct approximation methods in BC-EK-LIM-5A2, allows uniform and nonuniform partitions, admits graphical, numerical, analytical, and verbal presentations in BC-EK-LIM-5A1, and adds the over or under estimate determination in BC-EK-LIM-5A4; the methods differ in what the student must do.

- Granularity note: Topic 6.8 carries seven skills because the CED groups five independent antiderivative families under one essential knowledge statement (BC-EK-FUN-6C2) and adds the constant of integration and the no closed-form antiderivative statement as separate demands; each family is independently testable in a single question part.

- Granularity note: Topic 10.11 carries six skills because the CED separates representing a function as a Taylor polynomial (BC-LO-LIM-8A) from approximating function values with it (BC-LO-LIM-8B), and because the official free response material supplies the derivative values in three distinct ways, through repeated differentiation of a relation, through a table, and through operations on a known series, each of which is independently testable.

- Granularity note: Topic 10.13 carries seven skills because the 2025 scoring guideline allots five separate points inside one part, for the ratio, the limit, the interior, the endpoint consideration, and the endpoint analysis with the interval, and because the CED separates the radius (BC-EK-LIM-8D3) from the interval that requires endpoint testing (BC-EK-LIM-8D4). Each scored step is independently testable.

- Granularity note: Topic 10.14 carries eight skills because the CED lists both the general term construction from derivatives (BC-EK-LIM-8E1) and three distinct recall targets in BC-EK-LIM-8F1 and BC-EK-LIM-8F2, and because the construction operations of substitution and multiplication are scored separately from recall in the official material. Recall of the exponential, the trigonometric, and the geometric series is kept as three skills because a student may hold one and not another.

## BC-UNIT-01 Limits and Continuity skill inventory [inferred]

68 skills across 16 topics, CED pages 32-53. Calculator relevance is the registry value, one of `required`, `useful`, `none`. Representations are BC-REP ids from ../../data/taxonomies.json. Archetypes are BC-QA ids from ../../data/archetypes.json. Scope is `shared`, `BC_only`, `AB_only`, or `n/a`.

| Skill | Name | Topic | Calculator | Representations | Archetypes | Scope |
|---|---|---|---|---|---|---|
| BC-SKL-01001 | Compute an average rate of change over an interval | BC-TOP-0101 | none | BC-REP-01, BC-REP-03 | BC-QA-01012 | shared |
| BC-SKL-01002 | Explain why an average rate of change is undefined at a single point | BC-TOP-0101 | none | BC-REP-04 | BC-QA-01012 | shared |
| BC-SKL-01003 | Describe an instantaneous rate as a limit of average rates | BC-TOP-0101 | none | BC-REP-04, BC-REP-01 | BC-QA-01012 | shared |
| BC-SKL-01004 | Estimate an instantaneous rate from average rates over shrinking intervals | BC-TOP-0101 | optional | BC-REP-03, BC-REP-05 | BC-QA-01012 | shared |
| BC-SKL-01005 | Write a limit statement in correct analytic notation | BC-TOP-0102 | none | BC-REP-01, BC-REP-04 | BC-QA-01013 | shared |
| BC-SKL-01006 | Interpret a limit statement given in analytic notation | BC-TOP-0102 | none | BC-REP-04, BC-REP-01 | BC-QA-01013 | shared |
| BC-SKL-01007 | Write one sided limit notation | BC-TOP-0102 | none | BC-REP-01 | BC-QA-01013 | shared |
| BC-SKL-01008 | Distinguish the limit at a point from the function value at that point | BC-TOP-0102 | none | BC-REP-02, BC-REP-04 | BC-QA-01001 | shared |
| BC-SKL-01009 | Estimate a two sided limit from a graph | BC-TOP-0103 | none | BC-REP-02 | BC-QA-01001 | shared |
| BC-SKL-01010 | Estimate one sided limits from a graph | BC-TOP-0103 | none | BC-REP-02 | BC-QA-01001 | shared |
| BC-SKL-01011 | Determine that a limit fails to exist because the one sided limits differ | BC-TOP-0103 | none | BC-REP-02, BC-REP-01 | BC-QA-01001 | shared |
| BC-SKL-01012 | Determine that a limit fails to exist because the function is unbounded | BC-TOP-0103 | none | BC-REP-02, BC-REP-01 | BC-QA-01001 | shared |
| BC-SKL-01013 | Determine that a limit fails to exist because the function oscillates | BC-TOP-0103 | none | BC-REP-02, BC-REP-01 | BC-QA-01001 | shared |
| BC-SKL-01014 | Explain how the scale of a graph can hide function behaviour | BC-TOP-0103 | optional | BC-REP-02, BC-REP-09 | BC-QA-01013 | shared |
| BC-SKL-01015 | Estimate a two sided limit from a table of values | BC-TOP-0104 | none | BC-REP-03 | BC-QA-01002 | shared |
| BC-SKL-01016 | Estimate a one sided limit from a table of values | BC-TOP-0104 | none | BC-REP-03 | BC-QA-01002 | shared |
| BC-SKL-01017 | Judge whether a table supports a limit value or is inconclusive | BC-TOP-0104 | none | BC-REP-03, BC-REP-04 | BC-QA-01002 | shared |
| BC-SKL-01018 | Apply the sum and difference limit theorems | BC-TOP-0105 | none | BC-REP-01, BC-REP-03 | BC-QA-01003 | shared |
| BC-SKL-01019 | Apply the product and constant multiple limit theorems | BC-TOP-0105 | none | BC-REP-01, BC-REP-03 | BC-QA-01003 | shared |
| BC-SKL-01020 | Apply the quotient limit theorem and check the denominator condition | BC-TOP-0105 | none | BC-REP-01, BC-REP-03 | BC-QA-01003 | shared |
| BC-SKL-01021 | Evaluate a limit by direct substitution where the function is continuous | BC-TOP-0105 | none | BC-REP-01 | BC-QA-01014 | shared |
| BC-SKL-01022 | Apply the limit theorem for composite functions | BC-TOP-0105 | none | BC-REP-01 | BC-QA-01003 | shared |
| BC-SKL-01023 | Determine a two sided limit by matching one sided limits of a piecewise rule | BC-TOP-0105 | none | BC-REP-01, BC-REP-02 | BC-QA-01006 | shared |
| BC-SKL-01024 | Evaluate an indeterminate limit by factoring and dividing out a common factor | BC-TOP-0106 | none | BC-REP-01 | BC-QA-01004 | shared |
| BC-SKL-01025 | Evaluate an indeterminate limit by multiplying by a conjugate | BC-TOP-0106 | none | BC-REP-01 | BC-QA-01004 | shared |
| BC-SKL-01026 | Evaluate an indeterminate limit by simplifying a complex fraction | BC-TOP-0106 | none | BC-REP-01 | BC-QA-01004 | shared |
| BC-SKL-01027 | Evaluate an indeterminate limit by rewriting with trigonometric identities | BC-TOP-0106 | none | BC-REP-01 | BC-QA-01004 | shared |
| BC-SKL-01028 | Recognise an indeterminate form as a signal that rewriting is needed | BC-TOP-0106 | none | BC-REP-01, BC-REP-04 | BC-QA-01004 | shared |
| BC-SKL-01029 | Classify a limit expression by its form under substitution | BC-TOP-0107 | none | BC-REP-01 | BC-QA-01014 | shared |
| BC-SKL-01030 | Select an appropriate procedure for a given limit expression | BC-TOP-0107 | none | BC-REP-01, BC-REP-04 | BC-QA-01014 | shared |
| BC-SKL-01031 | Recognise when substitution already settles the limit | BC-TOP-0107 | none | BC-REP-01 | BC-QA-01014 | shared |
| BC-SKL-01032 | State the hypotheses of the squeeze theorem | BC-TOP-0108 | none | BC-REP-04, BC-REP-01 | BC-QA-01005 | shared |
| BC-SKL-01033 | Verify the bounding inequality on an interval around the point | BC-TOP-0108 | none | BC-REP-01, BC-REP-02 | BC-QA-01005 | shared |
| BC-SKL-01034 | Conclude a limit value from matching bounds | BC-TOP-0108 | none | BC-REP-01 | BC-QA-01005 | shared |
| BC-SKL-01035 | Apply the squeeze theorem to a bounded oscillating factor | BC-TOP-0108 | none | BC-REP-01, BC-REP-02 | BC-QA-01005 | shared |
| BC-SKL-01036 | Match a graph, a table, and an analytic expression of the same limit | BC-TOP-0109 | none | BC-REP-01, BC-REP-02, BC-REP-03 | BC-QA-01013 | shared |
| BC-SKL-01037 | Translate a limit statement into a verbal description of behaviour | BC-TOP-0109 | none | BC-REP-01, BC-REP-04 | BC-QA-01013 | shared |
| BC-SKL-01038 | Sketch a graph consistent with stated limit and value conditions | BC-TOP-0109 | none | BC-REP-02, BC-REP-04 | BC-QA-01013 | shared |
| BC-SKL-01039 | Classify a removable discontinuity | BC-TOP-0110 | none | BC-REP-01, BC-REP-02 | BC-QA-01007 | shared |
| BC-SKL-01040 | Classify a jump discontinuity | BC-TOP-0110 | none | BC-REP-01, BC-REP-02 | BC-QA-01007 | shared |
| BC-SKL-01041 | Classify a discontinuity due to a vertical asymptote | BC-TOP-0110 | none | BC-REP-01, BC-REP-02 | BC-QA-01007, BC-QA-01009 | shared |
| BC-SKL-01042 | Identify the discontinuities of a piecewise defined function from its rule | BC-TOP-0110 | none | BC-REP-01 | BC-QA-01006 | shared |
| BC-SKL-01043 | State the three conditions of continuity at a point | BC-TOP-0111 | none | BC-REP-04, BC-REP-01 | BC-QA-01006 | shared |
| BC-SKL-01044 | Test continuity at a point by checking the three conditions | BC-TOP-0111 | none | BC-REP-01, BC-REP-02 | BC-QA-01006 | shared |
| BC-SKL-01045 | Justify a continuity conclusion by naming the failed condition | BC-TOP-0111 | none | BC-REP-04 | BC-QA-01006 | shared |
| BC-SKL-01046 | Determine intervals of continuity from the domain of an expression | BC-TOP-0112 | none | BC-REP-01 | BC-QA-01015 | shared |
| BC-SKL-01047 | Name the function families continuous on their domains | BC-TOP-0112 | none | BC-REP-04, BC-REP-01 | BC-QA-01015 | shared |
| BC-SKL-01048 | Determine continuity of a piecewise function on an interval | BC-TOP-0112 | none | BC-REP-01 | BC-QA-01015 | shared |
| BC-SKL-01049 | Distinguish continuity on an open interval from continuity on a closed interval | BC-TOP-0112 | none | BC-REP-01, BC-REP-04 | BC-QA-01015 | shared |
| BC-SKL-01050 | Redefine a function value to remove a removable discontinuity | BC-TOP-0113 | none | BC-REP-01, BC-REP-02 | BC-QA-01008 | shared |
| BC-SKL-01051 | Solve for a parameter making a piecewise function continuous at a boundary | BC-TOP-0113 | none | BC-REP-01 | BC-QA-01008 | shared |
| BC-SKL-01052 | Solve for two parameters using continuity conditions at two boundaries | BC-TOP-0113 | none | BC-REP-01 | BC-QA-01008 | shared |
| BC-SKL-01053 | Decide whether a discontinuity can be removed | BC-TOP-0113 | none | BC-REP-01, BC-REP-02 | BC-QA-01008 | shared |
| BC-SKL-01054 | Write an infinite limit using correct notation | BC-TOP-0114 | none | BC-REP-01 | BC-QA-01009 | shared |
| BC-SKL-01055 | Determine one sided infinite limits by sign analysis near a zero of the denominator | BC-TOP-0114 | none | BC-REP-01 | BC-QA-01009 | shared |
| BC-SKL-01056 | Identify vertical asymptotes from an expression after simplification | BC-TOP-0114 | none | BC-REP-01, BC-REP-02 | BC-QA-01009 | shared |
| BC-SKL-01057 | Distinguish a vertical asymptote from a removable discontinuity at the same input | BC-TOP-0114 | none | BC-REP-01, BC-REP-02 | BC-QA-01007 | shared |
| BC-SKL-01058 | Evaluate the limit of a rational function at infinity by comparing degrees | BC-TOP-0115 | none | BC-REP-01 | BC-QA-01010 | shared |
| BC-SKL-01059 | Identify horizontal asymptotes from limits at infinity | BC-TOP-0115 | none | BC-REP-01, BC-REP-02 | BC-QA-01010 | shared |
| BC-SKL-01060 | Write a limit expression describing end behaviour in context | BC-TOP-0115 | optional | BC-REP-05, BC-REP-01 | BC-QA-01010 | shared |
| BC-SKL-01061 | Evaluate limits at infinity for expressions containing radicals | BC-TOP-0115 | none | BC-REP-01 | BC-QA-01010 | shared |
| BC-SKL-01062 | Compare relative magnitudes of growth using limits | BC-TOP-0115 | none | BC-REP-01 | BC-QA-01010 | shared |
| BC-SKL-01063 | Distinguish the limit at positive infinity from the limit at negative infinity | BC-TOP-0115 | none | BC-REP-01, BC-REP-02 | BC-QA-01010 | shared |
| BC-SKL-01064 | State the hypotheses of the Intermediate Value Theorem | BC-TOP-0116 | none | BC-REP-04, BC-REP-01 | BC-QA-01011 | shared |
| BC-SKL-01065 | Verify the continuity hypothesis before applying the theorem | BC-TOP-0116 | none | BC-REP-04, BC-REP-03 | BC-QA-01011 | shared |
| BC-SKL-01066 | Verify that the target value lies between the endpoint values | BC-TOP-0116 | none | BC-REP-03, BC-REP-01 | BC-QA-01011 | shared |
| BC-SKL-01067 | State the conclusion of the theorem with the correct interval | BC-TOP-0116 | none | BC-REP-04 | BC-QA-01011 | shared |
| BC-SKL-01068 | Apply the Intermediate Value Theorem to a function given by a table | BC-TOP-0116 | none | BC-REP-03, BC-REP-05 | BC-QA-01011 | shared |

## BC-UNIT-02 Differentiation: Definition and Fundamental Properties skill inventory [inferred]

46 skills across 10 topics, CED pages 54-69. Calculator relevance is the registry value, one of `required`, `useful`, `none`. Representations are BC-REP ids from ../../data/taxonomies.json. Archetypes are BC-QA ids from ../../data/archetypes.json. Scope is `shared`, `BC_only`, `AB_only`, or `n/a`.

| Skill | Name | Topic | Calculator | Representations | Archetypes | Scope |
|---|---|---|---|---|---|---|
| BC-SKL-02001 | Compute an average rate of change from the increment difference quotient | BC-TOP-0201 | none | BC-REP-01 | none | shared |
| BC-SKL-02002 | Compute an average rate of change from the two point difference quotient | BC-TOP-0201 | none | BC-REP-01, BC-REP-03 | BC-QA-02001 | shared |
| BC-SKL-02003 | Interpret an average rate of change in context with units | BC-TOP-0201 | optional | BC-REP-05, BC-REP-04 | BC-QA-02001 | shared |
| BC-SKL-02004 | Distinguish an average rate of change from an instantaneous rate of change | BC-TOP-0201 | none | BC-REP-04 | BC-QA-02012 | shared |
| BC-SKL-02005 | Express an instantaneous rate of change as a limit of average rates | BC-TOP-0201 | none | BC-REP-01 | BC-QA-02003 | shared |
| BC-SKL-02006 | Write the derivative at a point using the increment form of the limit | BC-TOP-0202 | none | BC-REP-01 | BC-QA-02002 | shared |
| BC-SKL-02007 | Write the derivative at a point using the two point form of the limit | BC-TOP-0202 | none | BC-REP-01 | BC-QA-02002 | shared |
| BC-SKL-02008 | Write the derivative function using the limit definition | BC-TOP-0202 | none | BC-REP-01 | BC-QA-02002 | shared |
| BC-SKL-02009 | Evaluate a derivative from the limit definition | BC-TOP-0202 | none | BC-REP-01 | BC-QA-02002 | shared |
| BC-SKL-02010 | Convert among the notations for a derivative | BC-TOP-0202 | none | BC-REP-01, BC-REP-04 | BC-QA-02012 | shared |
| BC-SKL-02011 | Represent a derivative graphically, numerically, and verbally | BC-TOP-0202 | none | BC-REP-01, BC-REP-02, BC-REP-03, BC-REP-04 | BC-QA-02012 | shared |
| BC-SKL-02012 | Interpret the derivative at a point as the slope of the tangent line | BC-TOP-0202 | none | BC-REP-02, BC-REP-04 | BC-QA-02011 | shared |
| BC-SKL-02013 | Write the equation of the line tangent to a curve at a given point | BC-TOP-0202 | none | BC-REP-01, BC-REP-02 | BC-QA-02011 | shared |
| BC-SKL-02014 | Estimate a derivative at a point from a table using a difference quotient | BC-TOP-0203 | none | BC-REP-03, BC-REP-05 | BC-QA-02001 | shared |
| BC-SKL-02015 | State the units of an estimated derivative in context | BC-TOP-0203 | none | BC-REP-05, BC-REP-04 | BC-QA-02001 | shared |
| BC-SKL-02016 | Select the interval of a table that supports the requested estimate | BC-TOP-0203 | none | BC-REP-03 | BC-QA-02001 | shared |
| BC-SKL-02017 | Estimate a derivative at a point from a graph | BC-TOP-0203 | none | BC-REP-02 | BC-QA-02009 | shared |
| BC-SKL-02018 | Estimate a derivative at a point using technology | BC-TOP-0203 | typically_required | BC-REP-09, BC-REP-01 | BC-QA-02013 | shared |
| BC-SKL-02019 | State that differentiability at a point implies continuity at that point | BC-TOP-0204 | none | BC-REP-04 | BC-QA-02004 | shared |
| BC-SKL-02020 | Use differentiability to justify continuity in a written argument | BC-TOP-0204 | none | BC-REP-04, BC-REP-03 | BC-QA-02004 | shared |
| BC-SKL-02021 | Give a continuous function that fails to be differentiable at a point | BC-TOP-0204 | none | BC-REP-01, BC-REP-02 | BC-QA-02005 | shared |
| BC-SKL-02022 | Identify a corner from unequal one sided limits of the difference quotient | BC-TOP-0204 | none | BC-REP-01, BC-REP-02 | BC-QA-02005 | shared |
| BC-SKL-02023 | Identify a vertical tangent as a failure of differentiability | BC-TOP-0204 | none | BC-REP-01, BC-REP-02 | BC-QA-02005 | shared |
| BC-SKL-02024 | Conclude non-differentiability from a discontinuity | BC-TOP-0204 | none | BC-REP-01, BC-REP-02 | BC-QA-02004 | shared |
| BC-SKL-02025 | Differentiate a power function with an integer exponent | BC-TOP-0205 | none | BC-REP-01 | BC-QA-02006 | shared |
| BC-SKL-02026 | Differentiate a power function after rewriting a radical or a reciprocal as a power | BC-TOP-0205 | none | BC-REP-01 | BC-QA-02006 | shared |
| BC-SKL-02027 | Derive a power rule case from the limit definition | BC-TOP-0205 | none | BC-REP-01 | BC-QA-02002 | shared |
| BC-SKL-02028 | Differentiate a constant function | BC-TOP-0206 | none | BC-REP-01 | BC-QA-02006 | shared |
| BC-SKL-02029 | Apply the constant multiple rule | BC-TOP-0206 | none | BC-REP-01 | BC-QA-02006 | shared |
| BC-SKL-02030 | Apply the sum and difference rules | BC-TOP-0206 | none | BC-REP-01 | BC-QA-02006 | shared |
| BC-SKL-02031 | Differentiate a polynomial function | BC-TOP-0206 | none | BC-REP-01 | BC-QA-02006 | shared |
| BC-SKL-02032 | Differentiate sine and cosine | BC-TOP-0207 | none | BC-REP-01 | BC-QA-02007 | shared |
| BC-SKL-02033 | Differentiate the natural exponential function | BC-TOP-0207 | none | BC-REP-01 | BC-QA-02007 | shared |
| BC-SKL-02034 | Differentiate the natural logarithm | BC-TOP-0207 | none | BC-REP-01 | BC-QA-02007 | shared |
| BC-SKL-02035 | Evaluate a limit by recognising it as the derivative of a known function | BC-TOP-0207 | none | BC-REP-01 | BC-QA-02003 | shared |
| BC-SKL-02036 | Apply the product rule to a product of two differentiable functions | BC-TOP-0208 | none | BC-REP-01 | BC-QA-02008 | shared |
| BC-SKL-02037 | Apply the product rule with values supplied by a table or a graph | BC-TOP-0208 | none | BC-REP-03, BC-REP-02 | BC-QA-02009 | shared |
| BC-SKL-02038 | Decide whether to expand a product or to apply the product rule | BC-TOP-0208 | none | BC-REP-01 | BC-QA-02008 | shared |
| BC-SKL-02039 | Apply the quotient rule to a quotient of two differentiable functions | BC-TOP-0209 | none | BC-REP-01 | BC-QA-02008 | shared |
| BC-SKL-02040 | Keep the order of the terms in the quotient rule numerator | BC-TOP-0209 | none | BC-REP-01 | BC-QA-02008 | shared |
| BC-SKL-02041 | Apply the quotient rule with values supplied by a table or a graph | BC-TOP-0209 | none | BC-REP-03, BC-REP-02 | BC-QA-02009 | shared |
| BC-SKL-02042 | Rewrite a quotient with a constant denominator instead of using the quotient rule | BC-TOP-0209 | none | BC-REP-01 | BC-QA-02008 | shared |
| BC-SKL-02043 | Rewrite tangent, cotangent, secant, and cosecant using sine and cosine | BC-TOP-0210 | none | BC-REP-01 | BC-QA-02010 | shared |
| BC-SKL-02044 | Differentiate tangent and cotangent | BC-TOP-0210 | none | BC-REP-01 | BC-QA-02010 | shared |
| BC-SKL-02045 | Differentiate secant and cosecant | BC-TOP-0210 | none | BC-REP-01 | BC-QA-02010 | shared |
| BC-SKL-02046 | Select the identity that makes a trigonometric expression differentiable by rule | BC-TOP-0210 | none | BC-REP-01, BC-REP-04 | BC-QA-02010 | shared |

## BC-UNIT-03 Differentiation: Composite, Implicit, and Inverse Functions skill inventory [inferred]

34 skills across 6 topics, CED pages 70-80. Calculator relevance is the registry value, one of `required`, `useful`, `none`. Representations are BC-REP ids from ../../data/taxonomies.json. Archetypes are BC-QA ids from ../../data/archetypes.json. Scope is `shared`, `BC_only`, `AB_only`, or `n/a`.

| Skill | Name | Topic | Calculator | Representations | Archetypes | Scope |
|---|---|---|---|---|---|---|
| BC-SKL-03001 | Decompose a composite function into outer and inner functions | BC-TOP-0301 | none | BC-REP-01, BC-REP-04 | BC-QA-03001, BC-QA-03009 | shared |
| BC-SKL-03002 | Differentiate a two layer composite function with the chain rule | BC-TOP-0301 | none | BC-REP-01 | BC-QA-03001 | shared |
| BC-SKL-03003 | Differentiate a composite with three or more layers | BC-TOP-0301 | none | BC-REP-01 | BC-QA-03001 | shared |
| BC-SKL-03004 | Evaluate the derivative of a composite at a point from a table of values | BC-TOP-0301 | none | BC-REP-03, BC-REP-01 | BC-QA-03002 | shared |
| BC-SKL-03005 | Evaluate the derivative of a composite at a point from graphs | BC-TOP-0301 | none | BC-REP-02, BC-REP-01 | BC-QA-03003 | shared |
| BC-SKL-03006 | Combine the chain rule with the product or quotient rule | BC-TOP-0301 | none | BC-REP-01 | BC-QA-03001, BC-QA-03009 | shared |
| BC-SKL-03007 | Differentiate a term in y with respect to x producing a dy/dx factor | BC-TOP-0302 | none | BC-REP-01 | BC-QA-03004 | shared |
| BC-SKL-03008 | Apply the product rule to a term containing both x and y | BC-TOP-0302 | none | BC-REP-01 | BC-QA-03004 | shared |
| BC-SKL-03009 | Differentiate both sides of an implicit equation term by term | BC-TOP-0302 | none | BC-REP-01 | BC-QA-03004 | shared |
| BC-SKL-03010 | Solve the differentiated equation for dy/dx | BC-TOP-0302 | none | BC-REP-01 | BC-QA-03004 | shared |
| BC-SKL-03011 | Evaluate dy/dx at a stated point on the curve | BC-TOP-0302 | none | BC-REP-01 | BC-QA-03004, BC-QA-03005 | shared |
| BC-SKL-03012 | Locate a point where the tangent to an implicit curve is horizontal | BC-TOP-0302 | none | BC-REP-01, BC-REP-02 | BC-QA-03005 | shared |
| BC-SKL-03013 | Locate a point where the tangent to an implicit curve is vertical | BC-TOP-0302 | none | BC-REP-01, BC-REP-02 | BC-QA-03005 | shared |
| BC-SKL-03014 | Verify a supplied expression for dy/dx by implicit differentiation | BC-TOP-0302 | none | BC-REP-01 | BC-QA-03004 | shared |
| BC-SKL-03015 | State the inverse function derivative rule with its hypotheses | BC-TOP-0303 | none | BC-REP-01, BC-REP-04 | BC-QA-03006 | shared |
| BC-SKL-03016 | Locate the matching input on the original function | BC-TOP-0303 | none | BC-REP-03, BC-REP-02, BC-REP-01 | BC-QA-03006 | shared |
| BC-SKL-03017 | Compute the derivative of an inverse at a point from a formula | BC-TOP-0303 | none | BC-REP-01 | BC-QA-03006 | shared |
| BC-SKL-03018 | Compute the derivative of an inverse at a point from a table | BC-TOP-0303 | none | BC-REP-03 | BC-QA-03006 | shared |
| BC-SKL-03019 | Compute the derivative of an inverse at a point from a graph | BC-TOP-0303 | none | BC-REP-02 | BC-QA-03006 | shared |
| BC-SKL-03020 | Derive the inverse derivative rule from the chain rule | BC-TOP-0303 | none | BC-REP-01, BC-REP-04 | BC-QA-03006 | shared |
| BC-SKL-03021 | State the derivatives of the inverse sine, cosine, and tangent functions | BC-TOP-0304 | none | BC-REP-01 | BC-QA-03007 | shared |
| BC-SKL-03022 | Differentiate an inverse trigonometric function of an inner expression | BC-TOP-0304 | none | BC-REP-01 | BC-QA-03007 | shared |
| BC-SKL-03023 | Derive an inverse trigonometric derivative by implicit differentiation | BC-TOP-0304 | none | BC-REP-01 | BC-QA-03007 | shared |
| BC-SKL-03024 | Evaluate an inverse trigonometric derivative at a point | BC-TOP-0304 | optional | BC-REP-01, BC-REP-09 | BC-QA-03007 | shared |
| BC-SKL-03025 | Combine an inverse trigonometric derivative with the product or quotient rule | BC-TOP-0304 | none | BC-REP-01 | BC-QA-03007, BC-QA-03009 | shared |
| BC-SKL-03026 | Classify an expression by its outermost operation | BC-TOP-0305 | none | BC-REP-01, BC-REP-04 | BC-QA-03009 | shared |
| BC-SKL-03027 | Select the differentiation rule that the classification indicates | BC-TOP-0305 | none | BC-REP-01, BC-REP-04 | BC-QA-03009 | shared |
| BC-SKL-03028 | Order several differentiation rules within one problem | BC-TOP-0305 | none | BC-REP-01 | BC-QA-03009 | shared |
| BC-SKL-03029 | Rewrite an expression algebraically before differentiating | BC-TOP-0305 | none | BC-REP-01 | BC-QA-03009 | shared |
| BC-SKL-03030 | Differentiate a first derivative to obtain the second derivative | BC-TOP-0306 | none | BC-REP-01 | BC-QA-03008 | shared |
| BC-SKL-03031 | Produce a third or higher order derivative by repeating differentiation | BC-TOP-0306 | none | BC-REP-01 | BC-QA-03008 | shared |
| BC-SKL-03032 | Read and write higher-order derivative notation | BC-TOP-0306 | none | BC-REP-01, BC-REP-04 | BC-QA-03008 | shared |
| BC-SKL-03033 | Differentiate a derivative expression that still contains y | BC-TOP-0306 | none | BC-REP-01 | BC-QA-03008 | shared |
| BC-SKL-03034 | Evaluate a second derivative at a point using dy/dx there | BC-TOP-0306 | none | BC-REP-01 | BC-QA-03008 | shared |

## BC-UNIT-04 Contextual Applications of Differentiation skill inventory [inferred]

38 skills across 7 topics, CED pages 82-93. Calculator relevance is the registry value, one of `required`, `useful`, `none`. Representations are BC-REP ids from ../../data/taxonomies.json. Archetypes are BC-QA ids from ../../data/archetypes.json. Scope is `shared`, `BC_only`, `AB_only`, or `n/a`.

| Skill | Name | Topic | Calculator | Representations | Archetypes | Scope |
|---|---|---|---|---|---|---|
| BC-SKL-04001 | State the units of a derivative in context | BC-TOP-0401 | none | BC-REP-04, BC-REP-05 | BC-QA-04001, BC-QA-04002 | shared |
| BC-SKL-04002 | Write a sentence interpreting a derivative value in context | BC-TOP-0401 | none | BC-REP-04, BC-REP-05 | BC-QA-04001 | shared |
| BC-SKL-04003 | Distinguish the value of a function from the value of its derivative in context | BC-TOP-0401 | none | BC-REP-04, BC-REP-05 | BC-QA-04001 | shared |
| BC-SKL-04004 | Approximate a derivative from an average rate of change with units | BC-TOP-0401 | optional | BC-REP-03, BC-REP-05 | BC-QA-04002 | shared |
| BC-SKL-04005 | Interpret the sign and size of a derivative in context | BC-TOP-0401 | none | BC-REP-04, BC-REP-05 | BC-QA-04001 | shared |
| BC-SKL-04006 | Differentiate a position function to obtain velocity | BC-TOP-0402 | optional | BC-REP-01, BC-REP-05 | BC-QA-04003 | shared |
| BC-SKL-04007 | Differentiate a velocity function to obtain acceleration | BC-TOP-0402 | optional | BC-REP-01, BC-REP-05 | BC-QA-04003 | shared |
| BC-SKL-04008 | Compute the speed of a particle from its velocity | BC-TOP-0402 | optional | BC-REP-01, BC-REP-05 | BC-QA-04003 | shared |
| BC-SKL-04009 | Determine the direction of motion from the sign of velocity | BC-TOP-0402 | optional | BC-REP-01, BC-REP-02 | BC-QA-04004 | shared |
| BC-SKL-04010 | Determine whether speed is increasing from the signs of velocity and acceleration | BC-TOP-0402 | optional | BC-REP-01, BC-REP-05 | BC-QA-04003 | shared |
| BC-SKL-04011 | Find when a particle is at rest or changes direction | BC-TOP-0402 | optional | BC-REP-01, BC-REP-09 | BC-QA-04004 | shared |
| BC-SKL-04012 | Communicate a sign analysis of velocity across a whole interval | BC-TOP-0402 | optional | BC-REP-01, BC-REP-04 | BC-QA-04004 | shared |
| BC-SKL-04013 | Identify the quantity and its independent variable in a non-motion context | BC-TOP-0403 | none | BC-REP-04, BC-REP-05 | BC-QA-04005 | shared |
| BC-SKL-04014 | Compute and report a rate of change with context-appropriate units | BC-TOP-0403 | typically_required | BC-REP-01, BC-REP-05, BC-REP-09 | BC-QA-04005 | shared |
| BC-SKL-04015 | Use context vocabulary rather than motion vocabulary | BC-TOP-0403 | none | BC-REP-04, BC-REP-05 | BC-QA-04005 | shared |
| BC-SKL-04016 | Interpret an end behaviour limit of a rate in context | BC-TOP-0403 | optional | BC-REP-01, BC-REP-05 | BC-QA-04005 | shared |
| BC-SKL-04017 | Identify the variables and which rates are given and wanted | BC-TOP-0404 | none | BC-REP-04, BC-REP-05, BC-REP-08 | BC-QA-04006 | shared |
| BC-SKL-04018 | Write an equation relating the varying quantities | BC-TOP-0404 | none | BC-REP-08, BC-REP-01 | BC-QA-04006 | shared |
| BC-SKL-04019 | Differentiate a relation with respect to time using the chain rule | BC-TOP-0404 | none | BC-REP-01 | BC-QA-04006, BC-QA-04007 | shared |
| BC-SKL-04020 | Apply the product rule inside a related rates differentiation | BC-TOP-0404 | none | BC-REP-01 | BC-QA-04007 | shared |
| BC-SKL-04021 | Reduce the number of variables before differentiating | BC-TOP-0404 | none | BC-REP-08, BC-REP-01 | BC-QA-04006 | shared |
| BC-SKL-04022 | Differentiate an implicitly defined curve with respect to time | BC-TOP-0404 | none | BC-REP-01, BC-REP-02 | BC-QA-04007 | shared |
| BC-SKL-04023 | Substitute instantaneous values only after differentiating | BC-TOP-0405 | none | BC-REP-01 | BC-QA-04006, BC-QA-04007 | shared |
| BC-SKL-04024 | Solve the differentiated equation for the unknown rate | BC-TOP-0405 | optional | BC-REP-01, BC-REP-09 | BC-QA-04006, BC-QA-04007 | shared |
| BC-SKL-04025 | Report a related rate with units and interpret its sign | BC-TOP-0405 | none | BC-REP-04, BC-REP-05 | BC-QA-04006 | shared |
| BC-SKL-04026 | Compute a missing instantaneous value from the relating equation | BC-TOP-0405 | none | BC-REP-01, BC-REP-08 | BC-QA-04006 | shared |
| BC-SKL-04027 | Distinguish quantities constant in time from quantities varying in time | BC-TOP-0405 | none | BC-REP-04, BC-REP-08 | BC-QA-04006 | shared |
| BC-SKL-04028 | Write the equation of the tangent line at a point | BC-TOP-0406 | none | BC-REP-01, BC-REP-02 | BC-QA-04008 | shared |
| BC-SKL-04029 | Approximate a function value with the tangent line | BC-TOP-0406 | optional | BC-REP-01, BC-REP-02 | BC-QA-04008 | shared |
| BC-SKL-04030 | Decide whether a tangent line approximation over or under estimates | BC-TOP-0406 | none | BC-REP-02, BC-REP-01 | BC-QA-04008 | shared |
| BC-SKL-04031 | Justify the estimate direction with the sign of the second derivative | BC-TOP-0406 | none | BC-REP-01, BC-REP-04 | BC-QA-04008 | shared |
| BC-SKL-04032 | Use a supplied derivative expression to obtain the slope at the point of tangency | BC-TOP-0406 | none | BC-REP-01 | BC-QA-04008 | shared |
| BC-SKL-04033 | Verify that a limit has an indeterminate form | BC-TOP-0407 | none | BC-REP-01 | BC-QA-04009 | shared |
| BC-SKL-04034 | State L'Hospital's rule with its hypotheses | BC-TOP-0407 | none | BC-REP-01, BC-REP-04 | BC-QA-04009 | shared |
| BC-SKL-04035 | Apply the rule by differentiating numerator and denominator separately | BC-TOP-0407 | none | BC-REP-01 | BC-QA-04009 | shared |
| BC-SKL-04036 | Evaluate the limit that the rule produces | BC-TOP-0407 | none | BC-REP-01 | BC-QA-04009 | shared |
| BC-SKL-04037 | Apply the rule again when the form is still indeterminate | BC-TOP-0407 | none | BC-REP-01 | BC-QA-04009 | shared |
| BC-SKL-04038 | Use differentiability to evaluate a limit of a given function | BC-TOP-0407 | none | BC-REP-01, BC-REP-02 | BC-QA-04009 | shared |

## BC-UNIT-05 Applying Derivatives to Analyze Functions skill inventory [inferred]

63 skills across 12 topics, CED pages 94-110. Calculator relevance is the registry value, one of `required`, `useful`, `none`. Representations are BC-REP ids from ../../data/taxonomies.json. Archetypes are BC-QA ids from ../../data/archetypes.json. Scope is `shared`, `BC_only`, `AB_only`, or `n/a`.

| Skill | Name | Topic | Calculator | Representations | Archetypes | Scope |
|---|---|---|---|---|---|---|
| BC-SKL-05001 | State the hypotheses of the Mean Value Theorem for a function and an interval | BC-TOP-0501 | none | BC-REP-04 | BC-QA-05001 | shared |
| BC-SKL-05002 | Verify that the hypotheses hold on the given interval | BC-TOP-0501 | none | BC-REP-03, BC-REP-04, BC-REP-05 | BC-QA-05001 | shared |
| BC-SKL-05003 | Compute the average rate of change over a closed interval | BC-TOP-0501 | optional | BC-REP-01, BC-REP-03 | BC-QA-05001, BC-QA-05002 | shared |
| BC-SKL-05004 | Conclude that a point with the average rate exists on the open interval | BC-TOP-0501 | none | BC-REP-04 | BC-QA-05001 | shared |
| BC-SKL-05005 | Solve for a value of c that the theorem provides | BC-TOP-0501 | optional | BC-REP-01, BC-REP-09 | BC-QA-05002 | shared |
| BC-SKL-05006 | Justify that a derivative takes a particular value using equal endpoint outputs | BC-TOP-0501 | none | BC-REP-03, BC-REP-05 | BC-QA-05001 | shared |
| BC-SKL-05007 | State the hypothesis of the Extreme Value Theorem | BC-TOP-0502 | none | BC-REP-04 | BC-QA-05010 | shared |
| BC-SKL-05008 | Verify continuity on the closed interval before applying the theorem | BC-TOP-0502 | none | BC-REP-02, BC-REP-04, BC-REP-05 | BC-QA-05010 | shared |
| BC-SKL-05009 | Conclude that a minimum value and a maximum value exist | BC-TOP-0502 | none | BC-REP-04 | BC-QA-05010 | shared |
| BC-SKL-05010 | Determine critical points where the first derivative equals zero | BC-TOP-0502 | optional | BC-REP-01, BC-REP-02 | BC-QA-05006, BC-QA-05007 | shared |
| BC-SKL-05011 | Determine critical points where the first derivative fails to exist | BC-TOP-0502 | none | BC-REP-01, BC-REP-02 | BC-QA-05006 | shared |
| BC-SKL-05012 | Distinguish a relative extremum from an absolute extremum | BC-TOP-0502 | none | BC-REP-02, BC-REP-04 | BC-QA-05006, BC-QA-05010 | shared |
| BC-SKL-05013 | Explain why a critical point need not be a relative extremum | BC-TOP-0502 | none | BC-REP-01, BC-REP-02 | BC-QA-05003 | shared |
| BC-SKL-05014 | Determine where the first derivative is positive or negative from a formula | BC-TOP-0503 | none | BC-REP-01 | BC-QA-05008 | shared |
| BC-SKL-05015 | Read intervals of increase and decrease from the graph of the derivative | BC-TOP-0503 | none | BC-REP-02 | BC-QA-05008, BC-QA-05009 | shared |
| BC-SKL-05016 | Build a sign chart on critical points and domain boundaries | BC-TOP-0503 | none | BC-REP-01, BC-REP-04 | BC-QA-05008 | shared |
| BC-SKL-05017 | Justify increase or decrease from the sign of the named derivative | BC-TOP-0503 | none | BC-REP-04 | BC-QA-05008 | shared |
| BC-SKL-05018 | Restrict a monotonicity conclusion to the domain of the function | BC-TOP-0503 | none | BC-REP-01, BC-REP-04 | BC-QA-05008 | shared |
| BC-SKL-05019 | Assemble the candidate relative extrema at the critical points | BC-TOP-0504 | none | BC-REP-01, BC-REP-02 | BC-QA-05003 | shared |
| BC-SKL-05020 | Classify a critical point from the sign change of the first derivative | BC-TOP-0504 | none | BC-REP-01, BC-REP-02, BC-REP-03 | BC-QA-05003 | shared |
| BC-SKL-05021 | Conclude neither extremum when the derivative keeps its sign | BC-TOP-0504 | none | BC-REP-01, BC-REP-02 | BC-QA-05003 | shared |
| BC-SKL-05022 | Write a first derivative test justification with an explicit referent | BC-TOP-0504 | none | BC-REP-04 | BC-QA-05003 | shared |
| BC-SKL-05023 | Separate the location of a relative extremum from its value | BC-TOP-0504 | none | BC-REP-01, BC-REP-04 | BC-QA-05003, BC-QA-05006 | shared |
| BC-SKL-05024 | Assemble the candidate list from critical points and both endpoints | BC-TOP-0505 | none | BC-REP-01, BC-REP-02 | BC-QA-05006 | shared |
| BC-SKL-05025 | Evaluate the function at every candidate | BC-TOP-0505 | optional | BC-REP-01, BC-REP-02, BC-REP-03 | BC-QA-05006 | shared |
| BC-SKL-05026 | Compare the candidate values and name the absolute extremum | BC-TOP-0505 | none | BC-REP-03, BC-REP-04 | BC-QA-05006 | shared |
| BC-SKL-05027 | Report the extreme value rather than only its location | BC-TOP-0505 | none | BC-REP-04 | BC-QA-05006 | shared |
| BC-SKL-05028 | Write a global justification covering every candidate | BC-TOP-0505 | none | BC-REP-03, BC-REP-04 | BC-QA-05006 | shared |
| BC-SKL-05029 | Justify an absolute extremum from the sign of the derivative across the interval | BC-TOP-0505 | none | BC-REP-01, BC-REP-02 | BC-QA-05006 | shared |
| BC-SKL-05030 | Determine intervals of concavity from the sign of the second derivative | BC-TOP-0506 | none | BC-REP-01 | BC-QA-05004 | shared |
| BC-SKL-05031 | Determine concavity from whether the derivative graph rises or falls | BC-TOP-0506 | none | BC-REP-02 | BC-QA-05004, BC-QA-05009 | shared |
| BC-SKL-05032 | Locate candidate points of inflection where the second derivative is zero or undefined | BC-TOP-0506 | none | BC-REP-01, BC-REP-02 | BC-QA-05005 | shared |
| BC-SKL-05033 | Confirm a point of inflection by a sign change of the second derivative | BC-TOP-0506 | none | BC-REP-01, BC-REP-02 | BC-QA-05005 | shared |
| BC-SKL-05034 | Reject a candidate where the second derivative is zero without a sign change | BC-TOP-0506 | none | BC-REP-01, BC-REP-02 | BC-QA-05005 | shared |
| BC-SKL-05035 | Tie a concavity or inflection reason to the representation that was given | BC-TOP-0506 | none | BC-REP-02, BC-REP-04 | BC-QA-05005, BC-QA-05004 | shared |
| BC-SKL-05036 | Apply the second derivative test at a critical point | BC-TOP-0507 | none | BC-REP-01, BC-REP-06 | BC-QA-05013 | shared |
| BC-SKL-05037 | State the inconclusive case of the second derivative test | BC-TOP-0507 | none | BC-REP-01, BC-REP-04 | BC-QA-05013 | shared |
| BC-SKL-05038 | Extend a sole relative extremum to an absolute extremum on the interval | BC-TOP-0507 | none | BC-REP-01, BC-REP-04, BC-REP-05 | BC-QA-05011, BC-QA-05013 | shared |
| BC-SKL-05039 | Choose between the first and second derivative tests for a given presentation | BC-TOP-0507 | none | BC-REP-01, BC-REP-02, BC-REP-06 | BC-QA-05013, BC-QA-05007 | shared |
| BC-SKL-05040 | Sketch the graph of the derivative from the graph of a function | BC-TOP-0508 | none | BC-REP-02 | BC-QA-05009 | shared |
| BC-SKL-05041 | Sketch a possible graph of a function from the graph of its derivative | BC-TOP-0508 | none | BC-REP-02 | BC-QA-05009 | shared |
| BC-SKL-05042 | Match a named feature of a function with the corresponding feature of its derivative | BC-TOP-0508 | none | BC-REP-01, BC-REP-02, BC-REP-03 | BC-QA-05009 | shared |
| BC-SKL-05043 | Place extrema and points of inflection consistently on a sketch | BC-TOP-0508 | none | BC-REP-02 | BC-QA-05009 | shared |
| BC-SKL-05044 | Recognise the vertical shift ambiguity when a curve is drawn from its derivative | BC-TOP-0508 | none | BC-REP-02, BC-REP-04 | BC-QA-05009 | shared |
| BC-SKL-05045 | Identify which of several graphs is the function, the derivative, and the second derivative | BC-TOP-0509 | none | BC-REP-02 | BC-QA-05009 | shared |
| BC-SKL-05046 | Translate a statement about the second derivative into a statement about shape | BC-TOP-0509 | none | BC-REP-01, BC-REP-04 | BC-QA-05009, BC-QA-05004 | shared |
| BC-SKL-05047 | Build a combined sign table for the first and second derivatives | BC-TOP-0509 | none | BC-REP-01, BC-REP-03 | BC-QA-05009 | shared |
| BC-SKL-05048 | Answer a question about a function from tabulated derivative values | BC-TOP-0509 | none | BC-REP-03 | BC-QA-05009 | shared |
| BC-SKL-05049 | Name the quantity to be optimised and assign the variables | BC-TOP-0510 | none | BC-REP-04, BC-REP-05, BC-REP-08 | BC-QA-05011 | shared |
| BC-SKL-05050 | Use the constraint to write the objective as a function of one variable | BC-TOP-0510 | none | BC-REP-01, BC-REP-08 | BC-QA-05011 | shared |
| BC-SKL-05051 | Determine the domain of the objective from the context | BC-TOP-0510 | none | BC-REP-01, BC-REP-05 | BC-QA-05011 | shared |
| BC-SKL-05052 | Differentiate the objective and solve for critical points | BC-TOP-0510 | optional | BC-REP-01, BC-REP-09 | BC-QA-05011 | shared |
| BC-SKL-05053 | Verify that the critical point gives the required extremum on the domain | BC-TOP-0510 | none | BC-REP-01, BC-REP-04 | BC-QA-05011 | shared |
| BC-SKL-05054 | Report the optimal value with its units and the input where it occurs | BC-TOP-0511 | optional | BC-REP-04, BC-REP-05 | BC-QA-05011 | shared |
| BC-SKL-05055 | Interpret the optimal value as a statement about the situation | BC-TOP-0511 | none | BC-REP-04, BC-REP-05 | BC-QA-05011 | shared |
| BC-SKL-05056 | Check the optimum against the endpoints of the contextual domain | BC-TOP-0511 | none | BC-REP-01, BC-REP-05 | BC-QA-05011 | shared |
| BC-SKL-05057 | Answer the question asked in an applied optimisation | BC-TOP-0511 | none | BC-REP-04, BC-REP-05 | BC-QA-05011 | shared |
| BC-SKL-05058 | Determine where the derivative of an implicit relation equals zero | BC-TOP-0512 | none | BC-REP-01 | BC-QA-05012 | shared |
| BC-SKL-05059 | Determine where the derivative of an implicit relation fails to exist | BC-TOP-0512 | none | BC-REP-01 | BC-QA-05012 | shared |
| BC-SKL-05060 | Solve the defining relation and the derived condition together | BC-TOP-0512 | none | BC-REP-01, BC-REP-02 | BC-QA-05012 | shared |
| BC-SKL-05061 | Compute a second derivative of an implicit relation | BC-TOP-0512 | none | BC-REP-01, BC-REP-06 | BC-QA-05012 | shared |
| BC-SKL-05062 | Substitute the derivative expression to evaluate a second derivative at a point | BC-TOP-0512 | none | BC-REP-01, BC-REP-06 | BC-QA-05012 | shared |
| BC-SKL-05063 | Classify a critical point of an implicit relation using the second derivative | BC-TOP-0512 | none | BC-REP-01, BC-REP-02 | BC-QA-05012, BC-QA-05013 | shared |

## BC-UNIT-06 Integration and Accumulation of Change skill inventory [inferred]

74 skills across 14 topics, CED pages 112-131. Calculator relevance is the registry value, one of `required`, `useful`, `none`. Representations are BC-REP ids from ../../data/taxonomies.json. Archetypes are BC-QA ids from ../../data/archetypes.json. Scope is `shared`, `BC_only`, `AB_only`, or `n/a`.

| Skill | Name | Topic | Calculator | Representations | Archetypes | Scope |
|---|---|---|---|---|---|---|
| BC-SKL-06001 | Interpret the area under a rate of change graph as accumulated change | BC-TOP-0601 | none | BC-REP-02, BC-REP-05, BC-REP-04 | BC-QA-06015 | shared |
| BC-SKL-06002 | State the units of an accumulated change | BC-TOP-0601 | none | BC-REP-04, BC-REP-05 | BC-QA-06015 | shared |
| BC-SKL-06003 | Determine the sign of accumulated change from the sign of the rate | BC-TOP-0601 | none | BC-REP-02, BC-REP-04 | BC-QA-06004 | shared |
| BC-SKL-06004 | Compute accumulated change from a piecewise linear rate graph using geometry | BC-TOP-0601 | none | BC-REP-02, BC-REP-05 | BC-QA-06004 | shared |
| BC-SKL-06005 | Compute a left Riemann sum from a table of values | BC-TOP-0602 | optional | BC-REP-03, BC-REP-05 | BC-QA-06001 | shared |
| BC-SKL-06006 | Compute a right Riemann sum from a table of values | BC-TOP-0602 | optional | BC-REP-03, BC-REP-05 | BC-QA-06001 | shared |
| BC-SKL-06007 | Compute a midpoint Riemann sum | BC-TOP-0602 | optional | BC-REP-01, BC-REP-02, BC-REP-03 | BC-QA-06001 | shared |
| BC-SKL-06008 | Compute a trapezoidal sum from a table of values | BC-TOP-0602 | optional | BC-REP-03, BC-REP-05 | BC-QA-06002 | shared |
| BC-SKL-06009 | Compute a Riemann sum for a function given by a graph or a formula | BC-TOP-0602 | optional | BC-REP-01, BC-REP-02 | BC-QA-06001 | shared |
| BC-SKL-06010 | Justify whether a Riemann sum under or over estimates using monotonicity | BC-TOP-0602 | none | BC-REP-01, BC-REP-02, BC-REP-03 | BC-QA-06001 | shared |
| BC-SKL-06011 | Justify whether a trapezoidal or midpoint sum under or over estimates using concavity | BC-TOP-0602 | none | BC-REP-01, BC-REP-02 | BC-QA-06002 | shared |
| BC-SKL-06012 | Expand summation notation into an explicit Riemann sum | BC-TOP-0603 | none | BC-REP-01 | BC-QA-06014 | shared |
| BC-SKL-06013 | Write a Riemann sum in sigma notation for a given function, interval, and partition | BC-TOP-0603 | none | BC-REP-01 | BC-QA-06014 | shared |
| BC-SKL-06014 | Convert the limit of a Riemann sum into a definite integral | BC-TOP-0603 | none | BC-REP-01 | BC-QA-06014 | shared |
| BC-SKL-06015 | Express a definite integral as the limit of a Riemann sum | BC-TOP-0603 | none | BC-REP-01 | BC-QA-06014 | shared |
| BC-SKL-06016 | State the limit definition of the definite integral | BC-TOP-0603 | none | BC-REP-01, BC-REP-04 | BC-QA-06014 | shared |
| BC-SKL-06017 | Write an accumulation function as a definite integral with a variable upper limit | BC-TOP-0604 | none | BC-REP-01, BC-REP-04, BC-REP-05 | BC-QA-06012 | shared |
| BC-SKL-06018 | Differentiate an accumulation function with a variable upper limit | BC-TOP-0604 | none | BC-REP-01, BC-REP-02 | BC-QA-06012 | shared |
| BC-SKL-06019 | Differentiate an accumulation function whose upper limit is a function of x | BC-TOP-0604 | none | BC-REP-01 | BC-QA-06012 | shared |
| BC-SKL-06020 | Evaluate an accumulation function at a specified input from the graph of the integrand | BC-TOP-0604 | none | BC-REP-02 | BC-QA-06003 | shared |
| BC-SKL-06021 | State the continuity hypothesis of the Fundamental Theorem of Calculus part one | BC-TOP-0604 | none | BC-REP-04 | BC-QA-06012 | shared |
| BC-SKL-06022 | Determine where an accumulation function increases or decreases from the sign of the integrand | BC-TOP-0605 | none | BC-REP-02 | BC-QA-06003 | shared |
| BC-SKL-06023 | Locate relative extrema of an accumulation function from sign changes of the integrand | BC-TOP-0605 | none | BC-REP-02 | BC-QA-06003 | shared |
| BC-SKL-06024 | Locate points of inflection of an accumulation function from turning points of the integrand | BC-TOP-0605 | none | BC-REP-02 | BC-QA-06003 | shared |
| BC-SKL-06025 | Determine the concavity of an accumulation function from the monotonicity of the integrand | BC-TOP-0605 | none | BC-REP-02 | BC-QA-06003 | shared |
| BC-SKL-06026 | Determine an absolute extreme value of an accumulation function with a global argument | BC-TOP-0605 | none | BC-REP-02 | BC-QA-06003 | shared |
| BC-SKL-06027 | Describe the graph of an accumulation function from the graph of the integrand | BC-TOP-0605 | none | BC-REP-02 | BC-QA-06003 | shared |
| BC-SKL-06028 | Evaluate a definite integral from a graph using area formulas | BC-TOP-0606 | none | BC-REP-02 | BC-QA-06004 | shared |
| BC-SKL-06029 | Apply the constant multiple and sum properties of definite integrals | BC-TOP-0606 | none | BC-REP-01 | BC-QA-06013 | shared |
| BC-SKL-06030 | Apply the reversal of limits property | BC-TOP-0606 | none | BC-REP-01 | BC-QA-06013 | shared |
| BC-SKL-06031 | Apply the adjacent interval property of definite integrals | BC-TOP-0606 | none | BC-REP-01, BC-REP-03 | BC-QA-06013 | shared |
| BC-SKL-06032 | Evaluate a definite integral over a degenerate interval | BC-TOP-0606 | none | BC-REP-01 | BC-QA-06013 | shared |
| BC-SKL-06033 | Evaluate a definite integral of a function with a removable or jump discontinuity | BC-TOP-0606 | none | BC-REP-01, BC-REP-02 | BC-QA-06013 | shared |
| BC-SKL-06034 | Evaluate a definite integral by antidifferentiation and endpoint substitution | BC-TOP-0607 | none | BC-REP-01 | BC-QA-06008 | shared |
| BC-SKL-06035 | State the hypotheses and conclusion of the Fundamental Theorem of Calculus part two | BC-TOP-0607 | none | BC-REP-04 | BC-QA-06013 | shared |
| BC-SKL-06036 | Compute net change in a quantity from its rate over an interval | BC-TOP-0607 | typically_required | BC-REP-01, BC-REP-05 | BC-QA-06005 | shared |
| BC-SKL-06037 | Compute a final value from an initial condition and an accumulated change | BC-TOP-0607 | typically_required | BC-REP-01, BC-REP-03, BC-REP-05 | BC-QA-06005 | shared |
| BC-SKL-06038 | Compute the average value of a function on an interval | BC-TOP-0607 | typically_required | BC-REP-01, BC-REP-05, BC-REP-09 | BC-QA-06007 | shared |
| BC-SKL-06039 | Set up a single definite integral for a rate in minus rate out situation | BC-TOP-0607 | typically_required | BC-REP-01, BC-REP-05 | BC-QA-06006 | shared |
| BC-SKL-06040 | Antidifferentiate power functions including negative and fractional exponents | BC-TOP-0608 | none | BC-REP-01 | BC-QA-06016 | shared |
| BC-SKL-06041 | Antidifferentiate exponential and reciprocal integrands | BC-TOP-0608 | none | BC-REP-01 | BC-QA-06016 | shared |
| BC-SKL-06042 | Antidifferentiate basic trigonometric integrands | BC-TOP-0608 | none | BC-REP-01 | BC-QA-06016 | shared |
| BC-SKL-06043 | Antidifferentiate integrands whose antiderivatives are inverse trigonometric | BC-TOP-0608 | none | BC-REP-01 | BC-QA-06016 | shared |
| BC-SKL-06044 | Include the constant of integration and determine it from an initial condition | BC-TOP-0608 | none | BC-REP-01 | BC-QA-06016 | shared |
| BC-SKL-06045 | Verify a proposed antiderivative by differentiating it | BC-TOP-0608 | none | BC-REP-01 | BC-QA-06016 | shared |
| BC-SKL-06046 | Recognise an integrand with no closed-form antiderivative | BC-TOP-0608 | none | BC-REP-01 | BC-QA-06016 | shared |
| BC-SKL-06047 | Select a substitution by identifying an inner function whose derivative appears | BC-TOP-0609 | none | BC-REP-01 | BC-QA-06008 | shared |
| BC-SKL-06048 | Convert the differential and adjust the constant when substituting | BC-TOP-0609 | none | BC-REP-01 | BC-QA-06008 | shared |
| BC-SKL-06049 | Back-substitute to express an indefinite integral in the original variable | BC-TOP-0609 | none | BC-REP-01 | BC-QA-06008 | shared |
| BC-SKL-06050 | Change the limits of integration when substituting in a definite integral | BC-TOP-0609 | none | BC-REP-01 | BC-QA-06008 | shared |
| BC-SKL-06051 | Evaluate a definite integral by substitution with back-substitution before the limits are used | BC-TOP-0609 | none | BC-REP-01 | BC-QA-06008 | shared |
| BC-SKL-06052 | Apply substitution to an integrand that antidifferentiates to a logarithm | BC-TOP-0609 | none | BC-REP-01 | BC-QA-06008 | shared |
| BC-SKL-06053 | Rewrite an improper rational integrand by polynomial long division | BC-TOP-0610 | none | BC-REP-01 | BC-QA-06016 | shared |
| BC-SKL-06054 | Complete the square in a quadratic denominator to reach a standard form | BC-TOP-0610 | none | BC-REP-01 | BC-QA-06016 | shared |
| BC-SKL-06055 | Rewrite an integrand by splitting or expanding before antidifferentiating | BC-TOP-0610 | none | BC-REP-01 | BC-QA-06016 | shared |
| BC-SKL-06056 | Decide between rearrangement and substitution for a rational integrand | BC-TOP-0610 | none | BC-REP-01 | BC-QA-06016 | shared |
| BC-SKL-06057 | Choose u and dv for an integration by parts | BC-TOP-0611 | none | BC-REP-01 | BC-QA-06009 | BC_only |
| BC-SKL-06058 | Apply the integration by parts formula | BC-TOP-0611 | none | BC-REP-01 | BC-QA-06009 | BC_only |
| BC-SKL-06059 | Apply integration by parts more than once | BC-TOP-0611 | none | BC-REP-01 | BC-QA-06009 | BC_only |
| BC-SKL-06060 | Evaluate a definite integral using integration by parts | BC-TOP-0611 | none | BC-REP-01 | BC-QA-06009 | BC_only |
| BC-SKL-06061 | Apply integration by parts to an integrand containing an unknown function and its derivative | BC-TOP-0611 | none | BC-REP-01, BC-REP-04 | BC-QA-06009 | BC_only |
| BC-SKL-06062 | Factor a denominator into distinct linear factors | BC-TOP-0612 | none | BC-REP-01 | BC-QA-06010 | BC_only |
| BC-SKL-06063 | Solve for the constants in a linear partial fraction decomposition | BC-TOP-0612 | none | BC-REP-01 | BC-QA-06010 | BC_only |
| BC-SKL-06064 | Antidifferentiate a linear partial fraction decomposition | BC-TOP-0612 | none | BC-REP-01 | BC-QA-06010 | BC_only |
| BC-SKL-06065 | Evaluate a definite integral of a rational function by partial fractions | BC-TOP-0612 | none | BC-REP-01 | BC-QA-06010 | BC_only |
| BC-SKL-06066 | Classify an integral as improper and name the cause | BC-TOP-0613 | none | BC-REP-01 | BC-QA-06011 | BC_only |
| BC-SKL-06067 | Rewrite an improper integral as a limit of definite integrals | BC-TOP-0613 | none | BC-REP-01 | BC-QA-06011 | BC_only |
| BC-SKL-06068 | Evaluate the limit to determine the value of a convergent improper integral | BC-TOP-0613 | none | BC-REP-01 | BC-QA-06011 | BC_only |
| BC-SKL-06069 | Conclude that an improper integral diverges | BC-TOP-0613 | none | BC-REP-01 | BC-QA-06011 | BC_only |
| BC-SKL-06070 | Split an improper integral that is improper at more than one place | BC-TOP-0613 | none | BC-REP-01 | BC-QA-06011 | BC_only |
| BC-SKL-06071 | Classify an integrand to select an antidifferentiation technique | BC-TOP-0614 | none | BC-REP-01 | BC-QA-06016 | shared |
| BC-SKL-06072 | Rule out a technique whose structural precondition is absent | BC-TOP-0614 | none | BC-REP-01 | BC-QA-06016 | shared |
| BC-SKL-06073 | Chain two antidifferentiation techniques in one problem | BC-TOP-0614 | none | BC-REP-01 | BC-QA-06016 | shared |
| BC-SKL-06074 | Recognise when no elementary technique applies and use an integral or numerical representation | BC-TOP-0614 | typically_required | BC-REP-01, BC-REP-09 | BC-QA-06016 | shared |

## BC-UNIT-07 Differential Equations skill inventory [inferred]

43 skills across 9 topics, CED pages 132-145. Calculator relevance is the registry value, one of `required`, `useful`, `none`. Representations are BC-REP ids from ../../data/taxonomies.json. Archetypes are BC-QA ids from ../../data/archetypes.json. Scope is `shared`, `BC_only`, `AB_only`, or `n/a`.

| Skill | Name | Topic | Calculator | Representations | Archetypes | Scope |
|---|---|---|---|---|---|---|
| BC-SKL-07001 | Translate a proportionality statement into a differential equation | BC-TOP-0701 | none | BC-REP-04, BC-REP-06 | BC-QA-07006 | shared |
| BC-SKL-07002 | Translate a rate statement involving a difference into a differential equation | BC-TOP-0701 | none | BC-REP-04, BC-REP-06 | BC-QA-07006 | shared |
| BC-SKL-07003 | Assign the variables and their units from a verbal description | BC-TOP-0701 | none | BC-REP-04, BC-REP-05 | BC-QA-07006 | shared |
| BC-SKL-07004 | Identify the initial condition stated in a context | BC-TOP-0701 | none | BC-REP-04, BC-REP-05 | BC-QA-07006, BC-QA-07003 | shared |
| BC-SKL-07005 | Distinguish a differential equation from an equation for the quantity | BC-TOP-0701 | none | BC-REP-04, BC-REP-06 | BC-QA-07006, BC-QA-07007 | shared |
| BC-SKL-07006 | Differentiate a proposed solution and substitute it into the equation | BC-TOP-0702 | none | BC-REP-01, BC-REP-06 | BC-QA-07007 | shared |
| BC-SKL-07007 | Confirm that a proposed solution satisfies the initial condition | BC-TOP-0702 | none | BC-REP-01, BC-REP-06 | BC-QA-07007 | shared |
| BC-SKL-07008 | Show that a proposed function is not a solution | BC-TOP-0702 | none | BC-REP-01, BC-REP-06 | BC-QA-07007 | shared |
| BC-SKL-07009 | State that a differential equation may have infinitely many solutions | BC-TOP-0702 | none | BC-REP-01, BC-REP-04, BC-REP-06 | BC-QA-07007 | shared |
| BC-SKL-07010 | Compute the slope the equation assigns to a given point | BC-TOP-0703 | none | BC-REP-06, BC-REP-07 | BC-QA-07002 | shared |
| BC-SKL-07011 | Draw the segments of a slope field at given lattice points | BC-TOP-0703 | none | BC-REP-06, BC-REP-07 | BC-QA-07002 | shared |
| BC-SKL-07012 | Identify where the slope field is horizontal | BC-TOP-0703 | none | BC-REP-06, BC-REP-07 | BC-QA-07002, BC-QA-07010 | shared |
| BC-SKL-07013 | Describe how a field depends on only one of the variables | BC-TOP-0703 | none | BC-REP-06, BC-REP-07 | BC-QA-07002 | shared |
| BC-SKL-07014 | Sketch a solution curve through a given point on a slope field | BC-TOP-0704 | none | BC-REP-07, BC-REP-02 | BC-QA-07001 | shared |
| BC-SKL-07015 | Keep a sketched curve on the correct side of an equilibrium level | BC-TOP-0704 | none | BC-REP-07, BC-REP-02 | BC-QA-07001 | shared |
| BC-SKL-07016 | Match a slope field to a differential equation | BC-TOP-0704 | none | BC-REP-06, BC-REP-07 | BC-QA-07002 | shared |
| BC-SKL-07017 | Describe the long-run behaviour of a solution from the field | BC-TOP-0704 | none | BC-REP-07, BC-REP-04 | BC-QA-07001, BC-QA-07009 | shared |
| BC-SKL-07018 | Read monotonicity and concavity of a solution from the equation or the field | BC-TOP-0704 | none | BC-REP-06, BC-REP-07 | BC-QA-07005, BC-QA-07010 | shared |
| BC-SKL-07019 | Determine the step size from the interval and the number of steps | BC-TOP-0705 | none | BC-REP-01, BC-REP-03 | BC-QA-07004 | BC_only |
| BC-SKL-07020 | Execute the first Euler step from the initial condition | BC-TOP-0705 | none | BC-REP-01, BC-REP-03, BC-REP-06 | BC-QA-07004 | BC_only |
| BC-SKL-07021 | Use the previous approximation as the input for the next step | BC-TOP-0705 | none | BC-REP-01, BC-REP-03, BC-REP-06 | BC-QA-07004 | BC_only |
| BC-SKL-07022 | Lay out the computation as a labelled step table | BC-TOP-0705 | none | BC-REP-03 | BC-QA-07004 | BC_only |
| BC-SKL-07023 | Decide the direction of the Euler error from concavity | BC-TOP-0705 | none | BC-REP-01, BC-REP-06 | BC-QA-07004, BC-QA-07005 | BC_only |
| BC-SKL-07024 | Separate the variables onto opposite sides of the equation | BC-TOP-0706 | none | BC-REP-01, BC-REP-06 | BC-QA-07003 | shared |
| BC-SKL-07025 | Antidifferentiate both sides of the separated equation | BC-TOP-0706 | none | BC-REP-01 | BC-QA-07003 | shared |
| BC-SKL-07026 | Include a single constant of integration | BC-TOP-0706 | none | BC-REP-01 | BC-QA-07003 | shared |
| BC-SKL-07027 | Solve the resulting equation for the dependent variable | BC-TOP-0706 | none | BC-REP-01 | BC-QA-07003 | shared |
| BC-SKL-07028 | Recognise when a differential equation is not separable | BC-TOP-0706 | none | BC-REP-06 | BC-QA-07003 | shared |
| BC-SKL-07029 | Substitute the initial condition to evaluate the constant of integration | BC-TOP-0707 | none | BC-REP-01, BC-REP-06 | BC-QA-07003 | shared |
| BC-SKL-07030 | Resolve an absolute value or a sign ambiguity from the initial condition | BC-TOP-0707 | none | BC-REP-01, BC-REP-06 | BC-QA-07003, BC-QA-07011 | shared |
| BC-SKL-07031 | State the domain restriction the initial condition selects | BC-TOP-0707 | none | BC-REP-01, BC-REP-04 | BC-QA-07011 | shared |
| BC-SKL-07032 | Write a particular solution as an accumulation function | BC-TOP-0707 | none | BC-REP-01, BC-REP-06 | BC-QA-07011 | shared |
| BC-SKL-07033 | Distinguish the general solution family from the particular solution | BC-TOP-0707 | none | BC-REP-01, BC-REP-04 | BC-QA-07003, BC-QA-07007 | shared |
| BC-SKL-07034 | Write the exponential model from a proportionality statement | BC-TOP-0708 | none | BC-REP-04, BC-REP-06 | BC-QA-07008 | shared |
| BC-SKL-07035 | Produce the exponential solution from the model and the initial value | BC-TOP-0708 | none | BC-REP-01, BC-REP-06 | BC-QA-07008 | shared |
| BC-SKL-07036 | Determine the constant of proportionality from a second data pair | BC-TOP-0708 | optional | BC-REP-01, BC-REP-03 | BC-QA-07008 | shared |
| BC-SKL-07037 | Interpret the sign and size of the constant in context | BC-TOP-0708 | none | BC-REP-04, BC-REP-05 | BC-QA-07008 | shared |
| BC-SKL-07038 | Apply a differential equation model to motion along a line | BC-TOP-0708 | none | BC-REP-01, BC-REP-05, BC-REP-06 | BC-QA-07008, BC-QA-07011 | shared |
| BC-SKL-07039 | Write the logistic equation from a joint proportionality statement | BC-TOP-0709 | none | BC-REP-04, BC-REP-06 | BC-QA-07009 | BC_only |
| BC-SKL-07040 | Identify the carrying capacity from the form of the equation | BC-TOP-0709 | none | BC-REP-06 | BC-QA-07009 | BC_only |
| BC-SKL-07041 | Determine the limiting value without solving the equation | BC-TOP-0709 | none | BC-REP-06, BC-REP-04 | BC-QA-07009 | BC_only |
| BC-SKL-07042 | Determine the value at which the quantity changes fastest | BC-TOP-0709 | none | BC-REP-06, BC-REP-01 | BC-QA-07009 | BC_only |
| BC-SKL-07043 | Interpret a logistic model in context | BC-TOP-0709 | none | BC-REP-04, BC-REP-05 | BC-QA-07009 | BC_only |

## BC-UNIT-08 Applications of Integration skill inventory [inferred]

59 skills across 13 topics, CED pages 146-164. Calculator relevance is the registry value, one of `required`, `useful`, `none`. Representations are BC-REP ids from ../../data/taxonomies.json. Archetypes are BC-QA ids from ../../data/archetypes.json. Scope is `shared`, `BC_only`, `AB_only`, or `n/a`.

| Skill | Name | Topic | Calculator | Representations | Archetypes | Scope |
|---|---|---|---|---|---|---|
| BC-SKL-08001 | Apply the average value formula to a function given by a formula | BC-TOP-0801 | optional | BC-REP-01, BC-REP-09 | BC-QA-08001 | shared |
| BC-SKL-08002 | Compute an average value from a graph using geometry | BC-TOP-0801 | none | BC-REP-02, BC-REP-08 | BC-QA-08001 | shared |
| BC-SKL-08003 | Present the calculator setup for an average value and report it | BC-TOP-0801 | typically_required | BC-REP-09, BC-REP-05 | BC-QA-08001 | shared |
| BC-SKL-08004 | Distinguish average value from average rate of change | BC-TOP-0801 | none | BC-REP-04, BC-REP-01 | BC-QA-08001, BC-QA-08002 | shared |
| BC-SKL-08005 | State the meaning and units of an average value in context | BC-TOP-0801 | none | BC-REP-04, BC-REP-05 | BC-QA-08001, BC-QA-08007 | shared |
| BC-SKL-08006 | Compute displacement as the definite integral of velocity | BC-TOP-0802 | optional | BC-REP-01, BC-REP-05 | BC-QA-08003 | shared |
| BC-SKL-08007 | Compute total distance as the definite integral of speed | BC-TOP-0802 | typically_required | BC-REP-01, BC-REP-09 | BC-QA-08003 | shared |
| BC-SKL-08008 | Split a time interval at the sign changes of velocity | BC-TOP-0802 | optional | BC-REP-01, BC-REP-02 | BC-QA-08003 | shared |
| BC-SKL-08009 | Determine a position value from an initial position and velocity | BC-TOP-0802 | optional | BC-REP-01, BC-REP-05 | BC-QA-08003, BC-QA-08004 | shared |
| BC-SKL-08010 | Determine a velocity value from an initial velocity and acceleration | BC-TOP-0802 | optional | BC-REP-01 | BC-QA-08003 | shared |
| BC-SKL-08011 | Select displacement or total distance from the wording of a prompt | BC-TOP-0802 | none | BC-REP-04, BC-REP-05 | BC-QA-08003 | shared |
| BC-SKL-08012 | Express the amount at a time as an initial amount plus an integral | BC-TOP-0803 | typically_required | BC-REP-05, BC-REP-01, BC-REP-09 | BC-QA-08004 | shared |
| BC-SKL-08013 | Set up a net rate as rate in minus rate out | BC-TOP-0803 | typically_required | BC-REP-05, BC-REP-01 | BC-QA-08005 | shared |
| BC-SKL-08014 | Determine when an accumulated amount is maximal and justify globally | BC-TOP-0803 | typically_required | BC-REP-05, BC-REP-09 | BC-QA-08006 | shared |
| BC-SKL-08015 | Interpret a definite integral of a rate in context with units | BC-TOP-0803 | none | BC-REP-04, BC-REP-05 | BC-QA-08007 | shared |
| BC-SKL-08016 | Write a definite integral expression that answers an applied question | BC-TOP-0803 | optional | BC-REP-05, BC-REP-01 | BC-QA-08004, BC-QA-08005 | shared |
| BC-SKL-08017 | Evaluate an applied accumulation integral and report it in context | BC-TOP-0803 | optional | BC-REP-09, BC-REP-05 | BC-QA-08004 | shared |
| BC-SKL-08018 | Identify which curve is upper on an interval | BC-TOP-0804 | optional | BC-REP-02, BC-REP-01 | BC-QA-08008 | shared |
| BC-SKL-08019 | Set up the area integral of upper minus lower with respect to x | BC-TOP-0804 | optional | BC-REP-01, BC-REP-02 | BC-QA-08008 | shared |
| BC-SKL-08020 | Find intersection points algebraically to set the limits | BC-TOP-0804 | none | BC-REP-01 | BC-QA-08008 | shared |
| BC-SKL-08021 | Find intersection points with a calculator to set the limits | BC-TOP-0804 | typically_required | BC-REP-09, BC-REP-02 | BC-QA-08008 | shared |
| BC-SKL-08022 | Evaluate an area integral and report the area | BC-TOP-0804 | optional | BC-REP-01, BC-REP-09 | BC-QA-08008 | shared |
| BC-SKL-08023 | Rewrite a curve as a function of y | BC-TOP-0805 | none | BC-REP-01 | BC-QA-08009 | shared |
| BC-SKL-08024 | Identify which curve is to the right on an interval of y | BC-TOP-0805 | optional | BC-REP-02, BC-REP-01 | BC-QA-08009 | shared |
| BC-SKL-08025 | Set up and evaluate an area integral with respect to y | BC-TOP-0805 | optional | BC-REP-01, BC-REP-02 | BC-QA-08009 | shared |
| BC-SKL-08026 | Choose whether to integrate in x or in y for a given region | BC-TOP-0805 | none | BC-REP-02, BC-REP-08 | BC-QA-08009, BC-QA-08008 | shared |
| BC-SKL-08027 | Locate every intersection point and order them | BC-TOP-0806 | optional | BC-REP-01, BC-REP-02 | BC-QA-08010 | shared |
| BC-SKL-08028 | Determine which curve is greater on each subinterval | BC-TOP-0806 | optional | BC-REP-01, BC-REP-02 | BC-QA-08010 | shared |
| BC-SKL-08029 | Write the area as a sum of definite integrals over the subintervals | BC-TOP-0806 | optional | BC-REP-01 | BC-QA-08010 | shared |
| BC-SKL-08030 | Write the area as the integral of the absolute value of the difference | BC-TOP-0806 | typically_required | BC-REP-01, BC-REP-09 | BC-QA-08010 | shared |
| BC-SKL-08031 | Express the side of a cross section as the distance between the curves | BC-TOP-0807 | none | BC-REP-08, BC-REP-01 | BC-QA-08011 | shared |
| BC-SKL-08032 | Set up the volume integral for square cross sections | BC-TOP-0807 | optional | BC-REP-01, BC-REP-08 | BC-QA-08011 | shared |
| BC-SKL-08033 | Set up the volume integral for rectangular cross sections | BC-TOP-0807 | optional | BC-REP-01, BC-REP-08 | BC-QA-08011 | shared |
| BC-SKL-08034 | Determine the axis the cross sections are perpendicular to | BC-TOP-0807 | none | BC-REP-04, BC-REP-08 | BC-QA-08011 | shared |
| BC-SKL-08035 | Evaluate a cross section volume integral | BC-TOP-0807 | optional | BC-REP-01, BC-REP-09 | BC-QA-08011 | shared |
| BC-SKL-08036 | Write the area of an equilateral triangular cross section | BC-TOP-0808 | none | BC-REP-08, BC-REP-01 | BC-QA-08011 | shared |
| BC-SKL-08037 | Write the area of a right isosceles triangular cross section | BC-TOP-0808 | none | BC-REP-08, BC-REP-01 | BC-QA-08011 | shared |
| BC-SKL-08038 | Write the area of a semicircular cross section from the diameter | BC-TOP-0808 | none | BC-REP-08, BC-REP-01 | BC-QA-08011 | shared |
| BC-SKL-08039 | Set up and evaluate the volume integral for a named cross section | BC-TOP-0808 | optional | BC-REP-01, BC-REP-09 | BC-QA-08011 | shared |
| BC-SKL-08040 | Identify the radius of a disc as the distance to the axis | BC-TOP-0809 | none | BC-REP-08, BC-REP-01 | BC-QA-08012 | shared |
| BC-SKL-08041 | Set up the disc integral about the x axis | BC-TOP-0809 | optional | BC-REP-01, BC-REP-08 | BC-QA-08012 | shared |
| BC-SKL-08042 | Set up the disc integral about the y axis | BC-TOP-0809 | optional | BC-REP-01, BC-REP-08 | BC-QA-08012 | shared |
| BC-SKL-08043 | Evaluate a disc volume and report it with the factor of pi | BC-TOP-0809 | optional | BC-REP-01, BC-REP-09 | BC-QA-08012 | shared |
| BC-SKL-08044 | Write the radius as the distance from a curve to a horizontal line | BC-TOP-0810 | none | BC-REP-08, BC-REP-01 | BC-QA-08012 | shared |
| BC-SKL-08045 | Write the radius as the distance from a curve to a vertical line | BC-TOP-0810 | none | BC-REP-08, BC-REP-01 | BC-QA-08012 | shared |
| BC-SKL-08046 | Set up the disc integral about a line other than an axis | BC-TOP-0810 | optional | BC-REP-01, BC-REP-08 | BC-QA-08012 | shared |
| BC-SKL-08047 | Keep the limits of integration unchanged when the axis shifts | BC-TOP-0810 | none | BC-REP-08, BC-REP-04 | BC-QA-08012 | shared |
| BC-SKL-08048 | Identify the outer and inner radii of a washer | BC-TOP-0811 | none | BC-REP-08, BC-REP-02 | BC-QA-08013 | shared |
| BC-SKL-08049 | Set up the washer integral about the x axis | BC-TOP-0811 | optional | BC-REP-01, BC-REP-08 | BC-QA-08013 | shared |
| BC-SKL-08050 | Set up the washer integral about the y axis | BC-TOP-0811 | optional | BC-REP-01, BC-REP-08 | BC-QA-08013 | shared |
| BC-SKL-08051 | Subtract the squares of the radii rather than squaring their difference | BC-TOP-0811 | none | BC-REP-01, BC-REP-08 | BC-QA-08013 | shared |
| BC-SKL-08052 | Write both washer radii as distances from a horizontal line | BC-TOP-0812 | none | BC-REP-08, BC-REP-01 | BC-QA-08013 | shared |
| BC-SKL-08053 | Write both washer radii as distances from a vertical line | BC-TOP-0812 | none | BC-REP-08, BC-REP-01 | BC-QA-08013 | shared |
| BC-SKL-08054 | Determine which boundary curve is farther from the shifted axis | BC-TOP-0812 | none | BC-REP-08, BC-REP-02 | BC-QA-08013 | shared |
| BC-SKL-08055 | Set up the washer integral about a line other than an axis | BC-TOP-0812 | optional | BC-REP-01, BC-REP-08 | BC-QA-08013 | shared |
| BC-SKL-08056 | State the arc length integral for a function on an interval | BC-TOP-0813 | optional | BC-REP-01 | BC-QA-08014 | BC_only |
| BC-SKL-08057 | Set up an arc length integral from a described curve | BC-TOP-0813 | optional | BC-REP-01, BC-REP-05 | BC-QA-08014 | BC_only |
| BC-SKL-08058 | Identify a given integral as an arc length and name the interval | BC-TOP-0813 | none | BC-REP-01, BC-REP-04 | BC-QA-08014 | BC_only |
| BC-SKL-08059 | Evaluate an arc length integral with technology | BC-TOP-0813 | typically_required | BC-REP-09 | BC-QA-08014 | BC_only |

## BC-UNIT-09 Parametric Equations, Polar Coordinates, and Vector-Valued Functions skill inventory [inferred]

43 skills across 9 topics, CED pages 166-179. Calculator relevance is the registry value, one of `required`, `useful`, `none`. Representations are BC-REP ids from ../../data/taxonomies.json. Archetypes are BC-QA ids from ../../data/archetypes.json. Scope is `shared`, `BC_only`, `AB_only`, or `n/a`.

| Skill | Name | Topic | Calculator | Representations | Archetypes | Scope |
|---|---|---|---|---|---|---|
| BC-SKL-09001 | Differentiate each component of a parametric curve with respect to the parameter | BC-TOP-0901 | optional | BC-REP-12, BC-REP-01 | BC-QA-09001 | BC_only |
| BC-SKL-09002 | Compute dy/dx for a parametric curve as a quotient of derivatives | BC-TOP-0901 | optional | BC-REP-12, BC-REP-01 | BC-QA-09001 | BC_only |
| BC-SKL-09003 | State the condition that dx/dt is not zero | BC-TOP-0901 | none | BC-REP-12, BC-REP-04 | BC-QA-09001 | BC_only |
| BC-SKL-09004 | Evaluate the slope of the tangent at a parameter value | BC-TOP-0901 | typically_required | BC-REP-12, BC-REP-09 | BC-QA-09001 | BC_only |
| BC-SKL-09005 | Write the equation of the tangent line at a point on a parametric curve | BC-TOP-0901 | optional | BC-REP-12, BC-REP-01 | BC-QA-09001 | BC_only |
| BC-SKL-09006 | Locate parameter values where the tangent is horizontal or vertical | BC-TOP-0901 | optional | BC-REP-12, BC-REP-01 | BC-QA-09001 | BC_only |
| BC-SKL-09007 | Differentiate dy/dx with respect to the parameter | BC-TOP-0902 | optional | BC-REP-12, BC-REP-01 | BC-QA-09002 | BC_only |
| BC-SKL-09008 | Assemble the second derivative by dividing again by dx/dt | BC-TOP-0902 | optional | BC-REP-12, BC-REP-01 | BC-QA-09002 | BC_only |
| BC-SKL-09009 | Evaluate the second derivative at a parameter value | BC-TOP-0902 | typically_required | BC-REP-12, BC-REP-09 | BC-QA-09002 | BC_only |
| BC-SKL-09010 | Determine the concavity of a parametric curve from the sign of the second derivative | BC-TOP-0902 | none | BC-REP-12, BC-REP-04 | BC-QA-09002 | BC_only |
| BC-SKL-09011 | Set up the arc length integral for a parametric curve | BC-TOP-0903 | optional | BC-REP-12, BC-REP-01 | BC-QA-09003 | BC_only |
| BC-SKL-09012 | Evaluate a parametric arc length integral with technology | BC-TOP-0903 | typically_required | BC-REP-09, BC-REP-12 | BC-QA-09003 | BC_only |
| BC-SKL-09013 | Identify the parametric arc length integral as the distance travelled | BC-TOP-0903 | none | BC-REP-12, BC-REP-04 | BC-QA-09003, BC-QA-09007 | BC_only |
| BC-SKL-09014 | Identify the parameter interval over which a length is measured | BC-TOP-0903 | none | BC-REP-12, BC-REP-04 | BC-QA-09003 | BC_only |
| BC-SKL-09015 | Differentiate a vector-valued function component by component | BC-TOP-0904 | optional | BC-REP-14, BC-REP-01 | BC-QA-09004 | BC_only |
| BC-SKL-09016 | Evaluate the velocity vector at a given time | BC-TOP-0904 | typically_required | BC-REP-14, BC-REP-09 | BC-QA-09004 | BC_only |
| BC-SKL-09017 | Evaluate the acceleration vector as the derivative of velocity | BC-TOP-0904 | typically_required | BC-REP-14, BC-REP-09 | BC-QA-09004 | BC_only |
| BC-SKL-09018 | Convert between parametric equations and vector-valued notation | BC-TOP-0904 | none | BC-REP-12, BC-REP-14 | BC-QA-09004, BC-QA-09005 | BC_only |
| BC-SKL-09019 | Antidifferentiate a vector-valued function component by component | BC-TOP-0905 | optional | BC-REP-14, BC-REP-01 | BC-QA-09005 | BC_only |
| BC-SKL-09020 | Write the displacement as a definite integral of the velocity vector | BC-TOP-0905 | typically_required | BC-REP-14, BC-REP-01 | BC-QA-09005 | BC_only |
| BC-SKL-09021 | Determine a coordinate of position from an initial position and a velocity component | BC-TOP-0905 | typically_required | BC-REP-14, BC-REP-09 | BC-QA-09005 | BC_only |
| BC-SKL-09022 | Accumulate backwards in time from a known later position | BC-TOP-0905 | typically_required | BC-REP-14, BC-REP-01 | BC-QA-09005 | BC_only |
| BC-SKL-09023 | Compute the speed of a particle as the magnitude of its velocity | BC-TOP-0906 | typically_required | BC-REP-14, BC-REP-09 | BC-QA-09006 | BC_only |
| BC-SKL-09024 | Solve for a time at which the speed has a stated value | BC-TOP-0906 | typically_required | BC-REP-09, BC-REP-14 | BC-QA-09006 | BC_only |
| BC-SKL-09025 | Compute the total distance travelled as the integral of speed | BC-TOP-0906 | typically_required | BC-REP-14, BC-REP-09 | BC-QA-09007 | BC_only |
| BC-SKL-09026 | Determine a coordinate of the particle at a time from an initial condition | BC-TOP-0906 | typically_required | BC-REP-14, BC-REP-09 | BC-QA-09005 | BC_only |
| BC-SKL-09027 | Determine when a particle moves toward or away from a coordinate axis | BC-TOP-0906 | typically_required | BC-REP-14, BC-REP-09 | BC-QA-09008 | BC_only |
| BC-SKL-09028 | Present the acceleration vector at a time with its setup | BC-TOP-0906 | typically_required | BC-REP-14, BC-REP-09 | BC-QA-09004 | BC_only |
| BC-SKL-09029 | Convert a point on a polar curve to Cartesian coordinates | BC-TOP-0907 | typically_required | BC-REP-13, BC-REP-09 | BC-QA-09009, BC-QA-09011 | BC_only |
| BC-SKL-09030 | Compute dr/dtheta for a polar curve and evaluate it | BC-TOP-0907 | typically_required | BC-REP-13, BC-REP-09 | BC-QA-09009 | BC_only |
| BC-SKL-09031 | Interpret dr/dtheta as the rate at which the distance from the origin changes | BC-TOP-0907 | none | BC-REP-13, BC-REP-04 | BC-QA-09009 | BC_only |
| BC-SKL-09032 | Relate the rate of the distance from the origin in time to dr/dtheta | BC-TOP-0907 | typically_required | BC-REP-13, BC-REP-09 | BC-QA-09010 | BC_only |
| BC-SKL-09033 | Compute dy/dx for a polar curve | BC-TOP-0907 | optional | BC-REP-13, BC-REP-01 | BC-QA-09009 | BC_only |
| BC-SKL-09034 | Locate the point on a polar curve farthest from a coordinate axis | BC-TOP-0907 | typically_required | BC-REP-13, BC-REP-09 | BC-QA-09011 | BC_only |
| BC-SKL-09035 | State the polar area integral for a single curve | BC-TOP-0908 | optional | BC-REP-13, BC-REP-01 | BC-QA-09012 | BC_only |
| BC-SKL-09036 | Determine the angles that bound a polar region | BC-TOP-0908 | optional | BC-REP-13, BC-REP-02 | BC-QA-09012 | BC_only |
| BC-SKL-09037 | Identify the angle interval that traces one loop of a polar curve | BC-TOP-0908 | optional | BC-REP-13, BC-REP-02 | BC-QA-09012 | BC_only |
| BC-SKL-09038 | Evaluate a polar area integral and report the area | BC-TOP-0908 | typically_required | BC-REP-09, BC-REP-13 | BC-QA-09012 | BC_only |
| BC-SKL-09039 | Find the intersection angles of two polar curves | BC-TOP-0909 | typically_required | BC-REP-13, BC-REP-09 | BC-QA-09013 | BC_only |
| BC-SKL-09040 | Determine which polar curve is outer on an angle interval | BC-TOP-0909 | optional | BC-REP-13, BC-REP-02 | BC-QA-09013 | BC_only |
| BC-SKL-09041 | Set up the area integral between two polar curves | BC-TOP-0909 | typically_required | BC-REP-13, BC-REP-01 | BC-QA-09013 | BC_only |
| BC-SKL-09042 | Evaluate the area between two polar curves and report it | BC-TOP-0909 | typically_required | BC-REP-09, BC-REP-13 | BC-QA-09013 | BC_only |
| BC-SKL-09043 | Use symmetry or a sum of integrals for a polar region with several pieces | BC-TOP-0909 | typically_required | BC-REP-13, BC-REP-01 | BC-QA-09013 | BC_only |

## BC-UNIT-10 Infinite Sequences and Series skill inventory [inferred]

73 skills across 15 topics, CED pages 180-200. Calculator relevance is the registry value, one of `required`, `useful`, `none`. Representations are BC-REP ids from ../../data/taxonomies.json. Archetypes are BC-QA ids from ../../data/archetypes.json. Scope is `shared`, `BC_only`, `AB_only`, or `n/a`.

| Skill | Name | Topic | Calculator | Representations | Archetypes | Scope |
|---|---|---|---|---|---|---|
| BC-SKL-10001 | Determine whether a sequence converges and find its limit | BC-TOP-1001 | none | BC-REP-10, BC-REP-01 | BC-QA-10001 | BC_only |
| BC-SKL-10002 | Compute the nth partial sum of a series | BC-TOP-1001 | none | BC-REP-11, BC-REP-01 | BC-QA-10002 | BC_only |
| BC-SKL-10003 | Determine convergence of a series from the limit of its partial sums | BC-TOP-1001 | none | BC-REP-11, BC-REP-10 | BC-QA-10002 | BC_only |
| BC-SKL-10004 | Evaluate a telescoping series through its partial sums | BC-TOP-1001 | none | BC-REP-11, BC-REP-01 | BC-QA-10002 | BC_only |
| BC-SKL-10005 | Distinguish a sequence from its associated series | BC-TOP-1001 | none | BC-REP-10, BC-REP-11, BC-REP-04 | BC-QA-10001 | BC_only |
| BC-SKL-10006 | Identify a series as geometric and state its first term and ratio | BC-TOP-1002 | none | BC-REP-11, BC-REP-01 | BC-QA-10003, BC-QA-10001 | BC_only |
| BC-SKL-10007 | Apply the convergence condition for a geometric series | BC-TOP-1002 | none | BC-REP-11, BC-REP-04 | BC-QA-10003, BC-QA-10020 | BC_only |
| BC-SKL-10008 | Compute the sum of a convergent geometric series | BC-TOP-1002 | none | BC-REP-11, BC-REP-01 | BC-QA-10003, BC-QA-10002 | BC_only |
| BC-SKL-10009 | Sum a geometric series whose index does not start at zero | BC-TOP-1002 | none | BC-REP-11, BC-REP-01 | BC-QA-10003 | BC_only |
| BC-SKL-10010 | Sum a geometric series whose ratio contains the variable | BC-TOP-1002 | none | BC-REP-11, BC-REP-01 | BC-QA-10003, BC-QA-10020 | BC_only |
| BC-SKL-10011 | Evaluate the limit of the general term of a series | BC-TOP-1003 | none | BC-REP-11, BC-REP-01 | BC-QA-10004, BC-QA-10001 | BC_only |
| BC-SKL-10012 | Conclude divergence when the general term does not approach zero | BC-TOP-1003 | none | BC-REP-11, BC-REP-04 | BC-QA-10004 | BC_only |
| BC-SKL-10013 | State that the nth term test is inconclusive when the limit is zero | BC-TOP-1003 | none | BC-REP-11, BC-REP-04 | BC-QA-10004, BC-QA-10001 | BC_only |
| BC-SKL-10014 | State and verify the conditions required by the integral test | BC-TOP-1004 | none | BC-REP-01, BC-REP-04 | BC-QA-10005 | BC_only |
| BC-SKL-10015 | Set up the improper integral that matches the series | BC-TOP-1004 | none | BC-REP-01, BC-REP-11 | BC-QA-10005 | BC_only |
| BC-SKL-10016 | Evaluate the improper integral using limit notation | BC-TOP-1004 | none | BC-REP-01 | BC-QA-10005 | BC_only |
| BC-SKL-10017 | Conclude convergence or divergence of the series from the integral | BC-TOP-1004 | none | BC-REP-04, BC-REP-11 | BC-QA-10005 | BC_only |
| BC-SKL-10018 | Classify a series as harmonic, alternating harmonic, or p-series | BC-TOP-1005 | none | BC-REP-11, BC-REP-01 | BC-QA-10004, BC-QA-10001 | BC_only |
| BC-SKL-10019 | Apply the p-series criterion | BC-TOP-1005 | none | BC-REP-11, BC-REP-04 | BC-QA-10004 | BC_only |
| BC-SKL-10020 | Recall the behaviour of the harmonic and alternating harmonic series | BC-TOP-1005 | none | BC-REP-11, BC-REP-04 | BC-QA-10004, BC-QA-10015 | BC_only |
| BC-SKL-10021 | Select an appropriate convergence test from the form of the general term | BC-TOP-1005 | none | BC-REP-11, BC-REP-04 | BC-QA-10001, BC-QA-10015 | BC_only |
| BC-SKL-10022 | Choose a comparison series for a given series | BC-TOP-1006 | none | BC-REP-11, BC-REP-01 | BC-QA-10004, BC-QA-10015 | BC_only |
| BC-SKL-10023 | Establish the term-by-term inequality for a direct comparison | BC-TOP-1006 | none | BC-REP-01, BC-REP-11 | BC-QA-10004 | BC_only |
| BC-SKL-10024 | Conclude convergence or divergence by direct comparison | BC-TOP-1006 | none | BC-REP-04, BC-REP-11 | BC-QA-10004, BC-QA-10015 | BC_only |
| BC-SKL-10025 | Set up the limit comparison ratio with limit notation | BC-TOP-1006 | none | BC-REP-01 | BC-QA-10006, BC-QA-10015 | BC_only |
| BC-SKL-10026 | Conclude from a positive finite limit in a limit comparison | BC-TOP-1006 | none | BC-REP-04, BC-REP-01 | BC-QA-10006 | BC_only |
| BC-SKL-10027 | Recognise a series as alternating | BC-TOP-1007 | none | BC-REP-11, BC-REP-01 | BC-QA-10004, BC-QA-10015 | BC_only |
| BC-SKL-10028 | Verify that the terms decrease in absolute value | BC-TOP-1007 | none | BC-REP-01, BC-REP-10 | BC-QA-10004, BC-QA-10008 | BC_only |
| BC-SKL-10029 | Verify that the terms tend to zero | BC-TOP-1007 | none | BC-REP-01, BC-REP-10 | BC-QA-10004, BC-QA-10008 | BC_only |
| BC-SKL-10030 | Conclude convergence by the alternating series test with both conditions stated | BC-TOP-1007 | none | BC-REP-04, BC-REP-11 | BC-QA-10004, BC-QA-10015 | BC_only |
| BC-SKL-10031 | Set up the ratio of consecutive terms of a series | BC-TOP-1008 | none | BC-REP-01, BC-REP-11 | BC-QA-10013, BC-QA-10014 | BC_only |
| BC-SKL-10032 | Evaluate the limit of the ratio of consecutive terms | BC-TOP-1008 | none | BC-REP-01 | BC-QA-10013, BC-QA-10014 | BC_only |
| BC-SKL-10033 | Conclude from the value of the ratio limit, including the inconclusive case | BC-TOP-1008 | none | BC-REP-04, BC-REP-01 | BC-QA-10004, BC-QA-10001 | BC_only |
| BC-SKL-10034 | Test the series of absolute values | BC-TOP-1009 | none | BC-REP-11, BC-REP-01 | BC-QA-10006, BC-QA-10007 | BC_only |
| BC-SKL-10035 | Classify a series as absolutely convergent | BC-TOP-1009 | none | BC-REP-04, BC-REP-11 | BC-QA-10007, BC-QA-10006 | BC_only |
| BC-SKL-10036 | Classify a series as conditionally convergent | BC-TOP-1009 | none | BC-REP-04, BC-REP-11 | BC-QA-10007, BC-QA-10015 | BC_only |
| BC-SKL-10037 | Use absolute convergence to conclude convergence | BC-TOP-1009 | none | BC-REP-04 | BC-QA-10007 | BC_only |
| BC-SKL-10038 | State the effect of rearrangement on an absolutely convergent series | BC-TOP-1009 | none | BC-REP-04, BC-REP-11 | BC-QA-10007 | BC_only |
| BC-SKL-10039 | Confirm the alternating series test conditions before bounding the error | BC-TOP-1010 | none | BC-REP-11, BC-REP-04 | BC-QA-10008 | BC_only |
| BC-SKL-10040 | Identify the first omitted term of the partial sum | BC-TOP-1010 | none | BC-REP-11, BC-REP-01 | BC-QA-10008 | BC_only |
| BC-SKL-10041 | Evaluate the bounding term at the given input | BC-TOP-1010 | none | BC-REP-01 | BC-QA-10008 | BC_only |
| BC-SKL-10042 | Compare the error bound with a stated tolerance | BC-TOP-1010 | none | BC-REP-01, BC-REP-04 | BC-QA-10008 | BC_only |
| BC-SKL-10043 | Compute successive derivatives of a function at the centre | BC-TOP-1011 | none | BC-REP-01 | BC-QA-10010 | BC_only |
| BC-SKL-10044 | Build a Taylor polynomial from derivative values at the centre | BC-TOP-1011 | none | BC-REP-01, BC-REP-11 | BC-QA-10010, BC-QA-10011 | BC_only |
| BC-SKL-10045 | Build a Taylor polynomial from a table of derivative values | BC-TOP-1011 | none | BC-REP-03, BC-REP-01 | BC-QA-10011 | BC_only |
| BC-SKL-10046 | Write a Maclaurin polynomial as the Taylor polynomial about zero | BC-TOP-1011 | none | BC-REP-01 | BC-QA-10010, BC-QA-10012 | BC_only |
| BC-SKL-10047 | Build a Taylor polynomial for a related function from a known series | BC-TOP-1011 | none | BC-REP-01, BC-REP-11 | BC-QA-10012 | BC_only |
| BC-SKL-10048 | Approximate a function value with a Taylor polynomial | BC-TOP-1011 | optional | BC-REP-01, BC-REP-09 | BC-QA-10012, BC-QA-10009 | BC_only |
| BC-SKL-10049 | Identify the maximum of the next derivative on the interval | BC-TOP-1012 | none | BC-REP-01, BC-REP-04 | BC-QA-10009 | BC_only |
| BC-SKL-10050 | Write the Lagrange error bound in the correct form | BC-TOP-1012 | none | BC-REP-01 | BC-QA-10009 | BC_only |
| BC-SKL-10051 | Compare the Lagrange bound with a stated tolerance | BC-TOP-1012 | none | BC-REP-01, BC-REP-04 | BC-QA-10009 | BC_only |
| BC-SKL-10052 | Choose between the Lagrange and alternating series error bounds | BC-TOP-1012 | none | BC-REP-04, BC-REP-11 | BC-QA-10009, BC-QA-10008 | BC_only |
| BC-SKL-10053 | Identify a power series and its centre | BC-TOP-1013 | none | BC-REP-11, BC-REP-01 | BC-QA-10013, BC-QA-10014 | BC_only |
| BC-SKL-10054 | Apply the ratio test to a power series | BC-TOP-1013 | none | BC-REP-11, BC-REP-01 | BC-QA-10013, BC-QA-10014 | BC_only |
| BC-SKL-10055 | Solve the ratio inequality for the interior of the interval | BC-TOP-1013 | none | BC-REP-01 | BC-QA-10013 | BC_only |
| BC-SKL-10056 | State the radius of convergence explicitly | BC-TOP-1013 | none | BC-REP-01, BC-REP-04 | BC-QA-10014 | BC_only |
| BC-SKL-10057 | Substitute each endpoint to produce the two numerical series | BC-TOP-1013 | none | BC-REP-11, BC-REP-01 | BC-QA-10015, BC-QA-10013 | BC_only |
| BC-SKL-10058 | Test each endpoint series with an appropriate test | BC-TOP-1013 | none | BC-REP-11, BC-REP-04 | BC-QA-10015 | BC_only |
| BC-SKL-10059 | State the interval of convergence with the correct endpoint inclusion | BC-TOP-1013 | none | BC-REP-01, BC-REP-04 | BC-QA-10013 | BC_only |
| BC-SKL-10060 | Write the general term of a Taylor series | BC-TOP-1014 | none | BC-REP-11, BC-REP-01 | BC-QA-10016, BC-QA-10018 | BC_only |
| BC-SKL-10061 | Recall the Maclaurin series for the exponential function | BC-TOP-1014 | none | BC-REP-11, BC-REP-01 | BC-QA-10017, BC-QA-10012 | BC_only |
| BC-SKL-10062 | Recall the Maclaurin series for sine and cosine | BC-TOP-1014 | none | BC-REP-11, BC-REP-01 | BC-QA-10017 | BC_only |
| BC-SKL-10063 | Recall the Maclaurin series for one over one minus x | BC-TOP-1014 | none | BC-REP-11, BC-REP-01 | BC-QA-10017, BC-QA-10003 | BC_only |
| BC-SKL-10064 | Construct a Maclaurin series by substitution into a known series | BC-TOP-1014 | none | BC-REP-11, BC-REP-01 | BC-QA-10017 | BC_only |
| BC-SKL-10065 | Construct a series by multiplying a known series by an expression | BC-TOP-1014 | none | BC-REP-11, BC-REP-01 | BC-QA-10017, BC-QA-10012 | BC_only |
| BC-SKL-10066 | Evaluate a Taylor series at a point to obtain a numerical series | BC-TOP-1014 | none | BC-REP-11, BC-REP-01 | BC-QA-10008, BC-QA-10002 | BC_only |
| BC-SKL-10067 | Identify a Taylor polynomial as a partial sum of the Taylor series | BC-TOP-1014 | none | BC-REP-11, BC-REP-01, BC-REP-04 | BC-QA-10016 | BC_only |
| BC-SKL-10068 | Differentiate a power series term by term | BC-TOP-1015 | none | BC-REP-11, BC-REP-01 | BC-QA-10018 | BC_only |
| BC-SKL-10069 | Integrate a power series term by term and determine the constant | BC-TOP-1015 | none | BC-REP-11, BC-REP-01 | BC-QA-10019 | BC_only |
| BC-SKL-10070 | Apply the preserved radius to a differentiated or integrated series | BC-TOP-1015 | none | BC-REP-11, BC-REP-04 | BC-QA-10018 | BC_only |
| BC-SKL-10071 | Recheck the endpoints for a derived power series | BC-TOP-1015 | none | BC-REP-11, BC-REP-01 | BC-QA-10018, BC-QA-10015 | BC_only |
| BC-SKL-10072 | Represent a power series in closed form by recognising a geometric series | BC-TOP-1015 | none | BC-REP-11, BC-REP-01 | BC-QA-10003 | BC_only |
| BC-SKL-10073 | Decide whether a series converges to the function at a stated input | BC-TOP-1015 | none | BC-REP-11, BC-REP-04 | BC-QA-10020 | BC_only |

## Representation key [verified]

| Id | Name |
|---|---|
| BC-REP-01 | Symbolic (analytical) expression |
| BC-REP-02 | Graphical |
| BC-REP-03 | Numerical table |
| BC-REP-04 | Verbal description |
| BC-REP-05 | Contextual model |
| BC-REP-06 | Differential equation |
| BC-REP-07 | Slope field |
| BC-REP-08 | Geometric diagram |
| BC-REP-09 | Calculator-generated numerical result |
| BC-REP-10 | Sequence |
| BC-REP-11 | Series (finite partial sums or infinite) |
| BC-REP-12 | Parametric equations |
| BC-REP-13 | Polar equation |
| BC-REP-14 | Vector-valued function |
