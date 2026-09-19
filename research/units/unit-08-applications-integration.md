---
title: Unit 8, Applications of Integration
research_date: 2026-09-19
status: draft
purpose: Decompose CED Unit 8 into concepts, atomic skills, non-calculus prerequisites, question archetypes and variants, observed errors, candidate misconceptions, and diagnostic signals, each grounded in the CED text and in the 2023 to 2025 official free-response questions and scoring guidelines.
---

# Unit 8, Applications of Integration

BC-UNIT-08 covers CED pages 146 to 164 and holds thirteen topics. Topic 8.13 carries the BC only marker in the CED and in data/curriculum.json; topics 8.1 through 8.12 are shared with AB. Every topic in the unit is a definite integral applied to a quantity, so the unit depends on Unit 6 throughout. Unit weighting is in [../exam/exam-blueprint.md](../exam/exam-blueprint.md) and exam composition is in [../exam/exam-structure.md](../exam/exam-structure.md). [verified] (ced:152, ced:164)

## 8.1 Finding the Average Value of a Function on an Interval

### Official mapping

Topic id BC-TOP-0801, CED code 8.1, name Finding the Average Value of a Function on an Interval, scope shared, CED page 152. [verified] (ced:152)

- BC-LO-CHA-4B (CHA-4.B): Determine the average value of a function using definite integrals.
  - BC-EK-CHA-4B1 (CHA-4.B.1): "The average value of a continuous function f over an interval [a, b] is 1/(b - a) times the integral from a to b of f(x) dx."

Suggested practice skills: BC-MPS-1E (Practice skill 1.E). Weighting pointer: [../exam/exam-blueprint.md](../exam/exam-blueprint.md).

### Concept breakdown

- BC-CON-08001 Average value of a function over an interval: The average value of a function is its accumulated amount divided by the length of the interval.
- BC-CON-08002 Average value contrasted with average rate of change: Averaging a function is not the same as averaging its rate of change.

- BC-SKL-08001 Apply the average value formula to a function given by a formula: Integrate the function over the interval and divide by the length of the interval.
- BC-SKL-08002 Compute an average value from a graph using geometry: Get the area under the graph by geometry, then divide by the width of the interval.
- BC-SKL-08003 Present the calculator setup for an average value and report it: Write the integral and the division before reporting the decimal the calculator gives.
- BC-SKL-08004 Distinguish average value from average rate of change: Decide which of the two averages a question is asking for before computing.
- BC-SKL-08005 State the meaning and units of an average value in context: Say what the average stands for in the situation and attach its units.

### Prerequisites

- BC-PRQ-06005 -> BC-SKL-08001, supporting, [inferred], Prerequisite for Apply the average value formula to a function given by a formula.
- BC-PRQ-06007 -> BC-SKL-08002, supporting, [inferred], Prerequisite for Compute an average value from a graph using geometry.
- BC-PRQ-08006 -> BC-SKL-08003, supporting, [inferred], Prerequisite for Present the calculator setup for an average value and report it.
- BC-PRQ-06005 -> BC-SKL-08004, supporting, [inferred], Prerequisite for Distinguish average value from average rate of change.
- BC-PRQ-06005 -> BC-SKL-08005, supporting, [inferred], Prerequisite for State the meaning and units of an average value in context.
- BC-SKL-06034 -> BC-SKL-08001, hard_prerequisite, [verified], Evaluating a definite integral by antidifferentiation and endpoint substitution underlies the average value computation.
- BC-SKL-06038 -> BC-SKL-08001, hard_prerequisite, [verified], The Unit 6 average value skill is the same computation introduced with accumulation.
- BC-SKL-06028 -> BC-SKL-08002, hard_prerequisite, [verified], Evaluating a definite integral from a graph by geometry supports the average value from a graph.

### Required mathematical knowledge

**Average value.** Hypotheses: f continuous on [a,b] with a less than b. Conclusion: the average value of f over [a,b] is the definite integral of f over [a,b] divided by b minus a (BC-EK-CHA-4B1).

**Average rate of change.** For a function F on [a,b], the average rate of change is F(b) minus F(a) divided by b minus a. When F is an antiderivative of f the two averages coincide numerically, which is why the 2025 calculator question could accept several equivalent presentations of the average rate of change of C on an interval starting at zero (sg-25:4).

**Units.** An average value carries the units of the integrand. An average rate of change carries the units of the function divided by the units of the input.

**Notation.** The average value written as a single quotient or in two steps; both presentations score, and unclear linkage between the correct integral and the correct answer was treated as scratch work in 2025 (sg-25:3) but cost a point in 2023 (sg-23:4).

### Representations

Representations in play: BC-REP-01 Symbolic, BC-REP-02 Graphical, BC-REP-05 Contextual model, BC-REP-08 Geometric diagram, BC-REP-09 Calculator-generated numerical result.

Conversions tested: contextual prompt to an average value integral (BC-REP-05 to BC-REP-01), graph to signed area to average (BC-REP-02 to BC-REP-08), and calculator output to a reported decimal with units (BC-REP-09 to BC-REP-04).

### Assessment behaviour

MCQ forms give a formula or a graph and ask for the average value, or offer the difference quotient as a distractor. FRQ forms embed the average value in the calculator active question and score the formula and the answer separately (sg-25:2, sg-25:3). Calculator variants supply a model function and demand the setup before the decimal; no-calculator variants supply a piecewise linear or circular graph so the integral can be taken by geometry. Conceptual variants ask which of two averages a sentence describes; computational variants ask for the number; interpretation variants ask for the meaning with units (sg-24:3); justification variants are uncommon at this topic. Multi-concept variants pair the average value with a later part that sets the instantaneous rate equal to the average rate of change (sg-25:4).

### Archetypes

- BC-QA-08001 Average value of a function over an interval
- BC-QA-08002 Instantaneous rate set equal to an average rate of change
- BC-QA-08007 Interpreting a definite integral of a rate in context

### Errors and misconceptions

- BC-ERR-08001 Average value reported without dividing by the interval length
- BC-ERR-08002 Average taken over an interval the question did not name
- BC-ERR-08003 Region below the axis counted as positive area in an average
- BC-ERR-08004 Calculator answer presented with no setup
- BC-ERR-08005 Intermediate value rounded before the final computation
- BC-ERR-08006 Average value computed where an average rate of change was asked, or the reverse
- BC-ERR-08007 Units omitted or built from the wrong factors
- BC-MIS-08002 The integral of a function is its average, severity high
- BC-MIS-08003 A calculator answer stands on its own, severity medium
- BC-MIS-08001 Average value and average rate of change are the same quantity, severity high

### Diagnostic signals

- BC-SIG-08001 Correct integral with no division by the interval length
- BC-SIG-08002 Difference quotient produced where an average value was requested

### Adaptive metadata summary

Skills in this topic carry calculator relevance none, optional, typically_required. Remediation targets named across the topic: BC-PRQ-08006, con.average_value, con.average_vs_rate. Every skill record carries the full seven key adaptive block in data/staging/unit-08.skills.json. [inferred]

## 8.2 Connecting Position, Velocity, and Acceleration of Functions Using Integrals

### Official mapping

Topic id BC-TOP-0802, CED code 8.2, name Connecting Position, Velocity, and Acceleration of Functions Using Integrals, scope shared, CED page 153. [verified] (ced:153)

- BC-LO-CHA-4C (CHA-4.C): Determine values for positions and rates of change using definite integrals in problems involving rectilinear motion.
  - BC-EK-CHA-4C1 (CHA-4.C.1): "For a particle in rectilinear motion over an interval of time, the definite integral of velocity represents the particle's displacement over the interval of time, and the definite integral of speed represents the particle's total distance traveled over the interval of time."

Suggested practice skills: BC-MPS-1D (Practice skill 1.D). Weighting pointer: [../exam/exam-blueprint.md](../exam/exam-blueprint.md).

### Concept breakdown

- BC-CON-08003 Displacement as the definite integral of velocity: Integrating velocity gives the net change in position, not the length of the trip.
- BC-CON-08004 Total distance as the definite integral of speed: Integrating the absolute value of velocity gives how far the particle actually travelled.
- BC-CON-08005 Position and velocity recovered from an initial value: A later value equals the starting value plus the accumulated change.

- BC-SKL-08006 Compute displacement as the definite integral of velocity: Integrate velocity over the interval to get the net change in position.
- BC-SKL-08007 Compute total distance as the definite integral of speed: Integrate the absolute value of velocity over the interval.
- BC-SKL-08008 Split a time interval at the sign changes of velocity: Break the interval where the velocity crosses zero, then add the pieces without their signs.
- BC-SKL-08009 Determine a position value from an initial position and velocity: Add the accumulated change to the starting position.
- BC-SKL-08010 Determine a velocity value from an initial velocity and acceleration: Add the accumulated change in velocity to the starting velocity.
- BC-SKL-08011 Select displacement or total distance from the wording of a prompt: Read whether the question wants net change in position or the length of the trip.

### Prerequisites

- BC-PRQ-06005 -> BC-SKL-08006, supporting, [inferred], Prerequisite for Compute displacement as the definite integral of velocity.
- BC-PRQ-08003 -> BC-SKL-08007, supporting, [inferred], Prerequisite for Compute total distance as the definite integral of speed.
- BC-PRQ-08001 -> BC-SKL-08008, supporting, [inferred], Prerequisite for Split a time interval at the sign changes of velocity.
- BC-PRQ-08003 -> BC-SKL-08008, supporting, [inferred], Prerequisite for Split a time interval at the sign changes of velocity.
- BC-PRQ-06005 -> BC-SKL-08009, supporting, [inferred], Prerequisite for Determine a position value from an initial position and velocity.
- BC-PRQ-06005 -> BC-SKL-08010, supporting, [inferred], Prerequisite for Determine a velocity value from an initial velocity and acceleration.
- BC-PRQ-06005 -> BC-SKL-08011, supporting, [inferred], Prerequisite for Select displacement or total distance from the wording of a prompt.
- BC-SKL-06036 -> BC-SKL-08006, hard_prerequisite, [verified], Computing net change from a rate over an interval is the displacement integral in the motion setting.
- BC-SKL-06037 -> BC-SKL-08009, hard_prerequisite, [verified], A position value from an initial position is the Unit 6 initial condition skill in the motion setting.
- BC-TOP-0402 -> BC-SKL-08011, supporting, [inferred], The rectilinear motion vocabulary of Unit 4 fixes the meanings of displacement, speed, and total distance; no Unit 4 skill id exists yet.

### Required mathematical knowledge

**Displacement.** For a particle in rectilinear motion on [a,b], the definite integral of velocity over [a,b] is the displacement (BC-EK-CHA-4C1).

**Total distance.** The definite integral of speed, that is of the absolute value of velocity, over [a,b] is the total distance travelled (BC-EK-CHA-4C1). Where velocity keeps one sign the two quantities agree up to sign, and where velocity changes sign they differ.

**Recovering a value.** Hypotheses: v continuous on [a,b] and the position known at a. Conclusion: the position at b is the position at a plus the definite integral of v over [a,b].

**Notation.** Speed written as the absolute value of velocity; displacement and total distance named explicitly rather than both called distance.

### Representations

Representations in play: BC-REP-01 Symbolic, BC-REP-02 Graphical, BC-REP-04 Verbal description, BC-REP-05 Contextual model, BC-REP-09 Calculator-generated numerical result.

Conversions tested: verbal prompt to a choice of integrand (BC-REP-04 to BC-REP-01), velocity graph to signed and unsigned area (BC-REP-02 to BC-REP-01), and calculator evaluation to a reported value with units (BC-REP-09 to BC-REP-04).

### Assessment behaviour

MCQ forms give a velocity formula or graph and ask for displacement or total distance, with the other quantity offered as a distractor. FRQ forms ask for total distance in the calculator active section, where the integral of speed earns a setup point and the decimal earns the answer point; the planar analogue of that scoring is visible at sg-24:6. Calculator variants use a velocity that changes sign at a value found numerically; no-calculator variants use a piecewise linear velocity graph. Conceptual variants ask which integrand answers the question; computational variants ask for the number; interpretation variants ask for the meaning with units; justification variants ask why the two totals differ. Multi-concept variants combine the distance integral with a position value built from an initial condition (sg-24:7). The Chief Reader records in BC-ERR-99010 that displacement is reported where total distance is asked.

### Archetypes

- BC-QA-08003 Rectilinear motion analysed with definite integrals
- BC-QA-08004 Amount at a later time from an initial amount and a rate

### Errors and misconceptions

- BC-ERR-08008 Displacement reported where total distance was asked
- BC-ERR-08009 Speed written without the absolute value or the magnitude
- BC-ERR-08010 Interval not split where velocity changes sign
- BC-ERR-08011 Initial value not added to the accumulated change
- BC-MIS-08004 Distance travelled and net change in position are the same, severity high
- BC-MIS-08006 The integral of a rate is the amount of the quantity, severity high
- BC-MIS-08005 Speed is another name for velocity, severity medium

### Diagnostic signals

- BC-SIG-08003 Signed integral reported as total distance
- BC-SIG-08004 Accumulated change reported where an amount was asked

### Adaptive metadata summary

Skills in this topic carry calculator relevance none, optional, typically_required. Remediation targets named across the topic: BC-PRQ-08001, BC-PRQ-08003, con.displacement, con.motion_initial_value, con.total_distance. Every skill record carries the full seven key adaptive block in data/staging/unit-08.skills.json. [inferred]

## 8.3 Using Accumulation Functions and Definite Integrals in Applied Contexts

### Official mapping

Topic id BC-TOP-0803, CED code 8.3, name Using Accumulation Functions and Definite Integrals in Applied Contexts, scope shared, CED page 154. [verified] (ced:154)

- BC-LO-CHA-4D (CHA-4.D): Interpret the meaning of a definite integral in accumulation problems.
  - BC-EK-CHA-4D1 (CHA-4.D.1): "A function defined as an integral represents an accumulation of a rate of change."
  - BC-EK-CHA-4D2 (CHA-4.D.2): "The definite integral of the rate of change of a quantity over an interval gives the net change of that quantity over that interval."
- BC-LO-CHA-4E (CHA-4.E): Determine net change using definite integrals in applied contexts.
  - BC-EK-CHA-4E1 (CHA-4.E.1): "The definite integral can be used to express information about accumulation and net change in many applied contexts."

Suggested practice skills: BC-MPS-3D (Practice skill 3.D). Weighting pointer: [../exam/exam-blueprint.md](../exam/exam-blueprint.md).

### Concept breakdown

- BC-CON-08006 Amount at a time from an initial amount and a rate: The amount now is the amount at the start plus everything accumulated since.
- BC-CON-08007 Net rate as rate in minus rate out: When something enters and leaves at once, the net rate is the difference of the two rates.
- BC-CON-08008 Extreme value of an accumulated amount from the sign of the net rate: The stored amount is largest where the net rate changes from positive to negative, endpoints checked.
- BC-CON-08009 Meaning of a definite integral in context: An integral of a rate names a quantity, over a stated interval, in stated units.

- BC-SKL-08012 Express the amount at a time as an initial amount plus an integral: Write the later amount as the starting amount plus the integral of the rate.
- BC-SKL-08013 Set up a net rate as rate in minus rate out: Subtract the outflow rate from the inflow rate before integrating.
- BC-SKL-08014 Determine when an accumulated amount is maximal and justify globally: Find where the net rate changes from positive to negative, then compare the candidates.
- BC-SKL-08015 Interpret a definite integral of a rate in context with units: Say what the integral measures, over which interval, in which units.
- BC-SKL-08016 Write a definite integral expression that answers an applied question: Turn the sentence into an integral with the right integrand and limits.
- BC-SKL-08017 Evaluate an applied accumulation integral and report it in context: Compute the integral, then answer the question in a sentence with units.

### Prerequisites

- BC-PRQ-06005 -> BC-SKL-08012, supporting, [inferred], Prerequisite for Express the amount at a time as an initial amount plus an integral.
- BC-PRQ-06005 -> BC-SKL-08013, supporting, [inferred], Prerequisite for Set up a net rate as rate in minus rate out.
- BC-PRQ-08001 -> BC-SKL-08014, supporting, [inferred], Prerequisite for Determine when an accumulated amount is maximal and justify globally.
- BC-PRQ-06005 -> BC-SKL-08015, supporting, [inferred], Prerequisite for Interpret a definite integral of a rate in context with units.
- BC-PRQ-06005 -> BC-SKL-08016, supporting, [inferred], Prerequisite for Write a definite integral expression that answers an applied question.
- BC-PRQ-08006 -> BC-SKL-08017, supporting, [inferred], Prerequisite for Evaluate an applied accumulation integral and report it in context.
- BC-SKL-06037 -> BC-SKL-08012, hard_prerequisite, [verified], Computing a final value from an initial condition and an accumulated change is the Unit 6 form of this applied accumulation skill.
- BC-TOP-0504 -> BC-SKL-08014, hard_prerequisite, [inferred], The first derivative test from Unit 5 supplies the sign change argument for the maximum of an accumulated amount; no Unit 5 skill id exists yet.
- BC-TOP-0505 -> BC-SKL-08014, hard_prerequisite, [inferred], The candidates test from Unit 5 supplies the global argument required by the 2025 scoring guideline; no Unit 5 skill id exists yet.

### Required mathematical knowledge

**Accumulation.** A function defined as an integral represents an accumulation of a rate of change (BC-EK-CHA-4D1), and the definite integral of the rate of change of a quantity over an interval gives the net change of that quantity over that interval (BC-EK-CHA-4D2).

**Amount at a time.** Hypotheses: the rate is integrable on [a,t] and the amount is known at a. Conclusion: the amount at t equals the amount at a plus the definite integral of the rate from a to t. The 2024 calculator question used exactly this structure to move a temperature from time twelve to time twenty (sg-24:4).

**Net rate.** With an inflow rate and an outflow rate acting at once, the net rate is the difference, and the amount increases where that difference is positive.

**Maximum of an accumulated amount.** Hypotheses: the amount function is differentiable on a closed interval. Conclusion: its absolute maximum occurs where its derivative, the net rate, changes sign from positive to negative or at an endpoint. In 2025 the global argument was required: a first or second derivative test alone did not earn the justification point (sg-25:5).

**Interpretation.** A complete interpretation names the quantity, the interval, and the units (sg-23:2).

**Notation.** The differential is part of the integral expression; the Chief Reader records its omission as BC-ERR-99006.

### Representations

Representations in play: BC-REP-01 Symbolic, BC-REP-03 Numerical table, BC-REP-04 Verbal description, BC-REP-05 Contextual model, BC-REP-09 Calculator-generated numerical result.

Conversions tested: verbal context to an integral expression (BC-REP-05 to BC-REP-01), integral expression back to a sentence with units (BC-REP-01 to BC-REP-04), and tabulated rate to an accumulated amount (BC-REP-03 to BC-REP-01).

### Assessment behaviour

MCQ forms ask which expression gives the amount at a later time, or what an integral means in context. FRQ forms place this topic in the calculator active question, where the amount at a later time earns an integral point, an initial condition point, and an answer point (sg-24:4, sg-24:7), and where the maximum of an accumulated amount earns a point for considering the derivative equal to zero, a point for a global justification, and a point for the answer (sg-25:5). Calculator variants give a model function and demand the setup; no-calculator variants give a table or a graph and an antidifferentiable integrand (sg-25:14). Conceptual variants ask what a function defined as an integral represents; computational variants ask for the amount; interpretation variants ask for meaning and units (sg-24:3); justification variants ask for the global argument. Multi-concept variants build the amount function from a difference of two model rates and then ask for its maximum (sg-25:5). The Chief Reader records incomplete interpretation as BC-ERR-99027 and local arguments offered for global claims as BC-ERR-99004.

### Archetypes

- BC-QA-08004 Amount at a later time from an initial amount and a rate
- BC-QA-08005 Accumulation with a rate in and a rate out
- BC-QA-08006 Time at which an accumulated amount is maximal
- BC-QA-08007 Interpreting a definite integral of a rate in context

### Errors and misconceptions

- BC-ERR-08011 Initial value not added to the accumulated change
- BC-ERR-08012 Net change reported as the amount present
- BC-ERR-08013 Inflow and outflow rates added instead of subtracted
- BC-ERR-08014 Parentheses lost when a supplied expression is placed in an integrand
- BC-ERR-08015 Local argument offered for an absolute extremum
- BC-ERR-08016 Endpoints omitted from a candidates table
- BC-ERR-08007 Units omitted or built from the wrong factors
- BC-ERR-08017 Interpretation names the quantity but not the interval
- BC-ERR-08018 Differential omitted from an integral expression
- BC-ERR-08019 Limits of integration taken from the wrong inputs
- BC-ERR-08005 Intermediate value rounded before the final computation
- BC-MIS-08006 The integral of a rate is the amount of the quantity, severity high
- BC-MIS-08007 Two rates acting at once combine by addition, severity medium
- BC-MIS-08008 A local extremum argument settles an absolute extremum, severity high
- BC-MIS-08009 An interpretation is complete once the quantity is named, severity medium
- BC-MIS-08003 A calculator answer stands on its own, severity medium

### Diagnostic signals

- BC-SIG-08004 Accumulated change reported where an amount was asked
- BC-SIG-08005 Critical point found with only a local justification
- BC-SIG-08006 Interpretation naming the quantity and units but not the interval

### Adaptive metadata summary

Skills in this topic carry calculator relevance none, optional, typically_required. Remediation targets named across the topic: BC-PRQ-08001, BC-PRQ-08006, con.amount_from_rate, con.integral_meaning, con.net_rate. Every skill record carries the full seven key adaptive block in data/staging/unit-08.skills.json. [inferred]

## 8.4 Finding the Area Between Curves Expressed as Functions of x

### Official mapping

Topic id BC-TOP-0804, CED code 8.4, name Finding the Area Between Curves Expressed as Functions of x, scope shared, CED page 155. [verified] (ced:155)

- BC-LO-CHA-5A (CHA-5.A): Calculate areas in the plane using the definite integral.
  - BC-EK-CHA-5A1 (CHA-5.A.1): "Areas of regions in the plane can be calculated with definite integrals."

Suggested practice skills: BC-MPS-4C (Practice skill 4.C). Weighting pointer: [../exam/exam-blueprint.md](../exam/exam-blueprint.md).

### Concept breakdown

- BC-CON-08010 Area between two curves integrated in x: The area is the integral of the upper curve minus the lower curve across the interval.
- BC-CON-08011 Limits of integration from the boundary of the region: The limits come from where the curves meet or from the lines the region is bounded by.

- BC-SKL-08018 Identify which curve is upper on an interval: Decide which graph is on top before writing the difference.
- BC-SKL-08019 Set up the area integral of upper minus lower with respect to x: Write the integral of the top curve minus the bottom curve, dx.
- BC-SKL-08020 Find intersection points algebraically to set the limits: Solve the two expressions equal to each other by hand.
- BC-SKL-08021 Find intersection points with a calculator to set the limits: Use the solver or a graph to get the crossing inputs as decimals.
- BC-SKL-08022 Evaluate an area integral and report the area: Antidifferentiate or use technology, then state the area.

### Prerequisites

- BC-PRQ-06005 -> BC-SKL-08018, supporting, [inferred], Prerequisite for Identify which curve is upper on an interval.
- BC-PRQ-06005 -> BC-SKL-08019, supporting, [inferred], Prerequisite for Set up the area integral of upper minus lower with respect to x.
- BC-PRQ-08001 -> BC-SKL-08020, supporting, [inferred], Prerequisite for Find intersection points algebraically to set the limits.
- BC-PRQ-08006 -> BC-SKL-08021, supporting, [inferred], Prerequisite for Find intersection points with a calculator to set the limits.
- BC-PRQ-06002 -> BC-SKL-08022, supporting, [inferred], Prerequisite for Evaluate an area integral and report the area.
- BC-SKL-06034 -> BC-SKL-08022, hard_prerequisite, [verified], Evaluating a definite integral with the Fundamental Theorem of Calculus underlies every area and volume evaluation in this unit.

### Required mathematical knowledge

**Area between curves.** Hypotheses: f and g continuous on [a,b] with f greater than or equal to g there. Conclusion: the area of the region between the graphs over [a,b] is the definite integral of f minus g with respect to x (BC-EK-CHA-5A1).

**Limits.** The limits are the inputs where the region begins and ends, which are either given as vertical lines or found by solving f equal g.

**Known partial information.** A region may be described so that one of the two integrals is supplied as a number, as in 2023 when the integral of the unspecified function over the interval was given and only the second antiderivative had to be found (sg-23:16).

**Notation.** An area is reported as a nonnegative quantity, and a response that writes the reversed difference and then reports the positive value without correcting the statement loses the answer point (sg-23:17).

### Representations

Representations in play: BC-REP-01 Symbolic, BC-REP-02 Graphical, BC-REP-08 Geometric diagram, BC-REP-09 Calculator-generated numerical result.

Conversions tested: figure of a shaded region to an integral expression (BC-REP-02 to BC-REP-01), and equations of the boundary curves to numerical limits (BC-REP-01 to BC-REP-09).

### Assessment behaviour

MCQ forms present a shaded region and ask which integral gives its area, with the reversed difference and the single function integral as distractors. FRQ forms ask for the area of a shaded region and score the integrand, an antiderivative, and the answer as separate points (sg-23:16). Calculator variants require intersection points found numerically; no-calculator variants use curves that meet at values found by hand or that are bounded by given vertical lines. Conceptual variants ask which difference belongs in the integrand; computational variants ask for the number; interpretation variants attach the area to a context; justification variants ask why one curve is above the other. Multi-concept variants supply the value of one of the two integrals and require the other by antidifferentiation (sg-23:16).

### Archetypes

- BC-QA-08008 Area of a region between two curves in x

### Errors and misconceptions

- BC-ERR-08020 Difference of the boundary functions taken in the wrong order
- BC-ERR-08018 Differential omitted from an integral expression
- BC-ERR-08019 Limits of integration taken from the wrong inputs
- BC-ERR-08005 Intermediate value rounded before the final computation
- BC-ERR-08021 Area asserted to equal an expression that is its negative
- BC-ERR-08022 Limits kept in the old variable after a substitution
- BC-MIS-08011 The order of subtraction in an area integrand does not matter, severity medium
- BC-MIS-08010 The area between curves is the integral of the curve that bounds it, severity high
- BC-MIS-08012 Limits of integration are a viewing window rather than a boundary, severity medium

### Diagnostic signals

- BC-SIG-08007 Negative value reported as an area or a volume
- BC-SIG-08008 Stored intersection values replaced by rounded decimals

### Adaptive metadata summary

Skills in this topic carry calculator relevance none, optional, typically_required. Remediation targets named across the topic: BC-PRQ-08001, BC-PRQ-08006, con.area_between_x. Every skill record carries the full seven key adaptive block in data/staging/unit-08.skills.json. [inferred]

## 8.5 Finding the Area Between Curves Expressed as Functions of y

### Official mapping

Topic id BC-TOP-0805, CED code 8.5, name Finding the Area Between Curves Expressed as Functions of y, scope shared, CED page 156. [verified] (ced:156)

- BC-LO-CHA-5A (CHA-5.A): Calculate areas in the plane using the definite integral.
  - BC-EK-CHA-5A2 (CHA-5.A.2): "Areas of regions in the plane can be calculated using functions of either x or y."

Suggested practice skills: BC-MPS-1E (Practice skill 1.E). Weighting pointer: [../exam/exam-blueprint.md](../exam/exam-blueprint.md).

### Concept breakdown

- BC-CON-08012 Area between two curves integrated in y: Slicing horizontally, the area is the integral of the right curve minus the left curve.

- BC-SKL-08023 Rewrite a curve as a function of y: Solve the equation so that x is written in terms of y.
- BC-SKL-08024 Identify which curve is to the right on an interval of y: Decide which graph is farther right before writing the difference.
- BC-SKL-08025 Set up and evaluate an area integral with respect to y: Write the integral of right minus left, dy, and evaluate it.
- BC-SKL-08026 Choose whether to integrate in x or in y for a given region: Pick the slicing direction that needs the fewest integrals.

### Prerequisites

- BC-PRQ-08002 -> BC-SKL-08023, supporting, [inferred], Prerequisite for Rewrite a curve as a function of y.
- BC-PRQ-06005 -> BC-SKL-08024, supporting, [inferred], Prerequisite for Identify which curve is to the right on an interval of y.
- BC-PRQ-08002 -> BC-SKL-08025, supporting, [inferred], Prerequisite for Set up and evaluate an area integral with respect to y.
- BC-PRQ-08002 -> BC-SKL-08026, supporting, [inferred], Prerequisite for Choose whether to integrate in x or in y for a given region.

### Required mathematical knowledge

**Area in y.** Hypotheses: the boundary curves are written as functions of y, continuous on [c,d], with one to the right of the other. Conclusion: the area is the definite integral of the right function minus the left function with respect to y (BC-EK-CHA-5A2).

**Choice of variable.** A region whose upper boundary changes needs either two integrals in x or one integral in y, and the converse holds for a region whose right boundary changes.

**Notation.** The differential dy and limits that are y values; mixing an integrand in x with a dy differential is a notation error as well as a set up error.

### Representations

Representations in play: BC-REP-01 Symbolic, BC-REP-02 Graphical, BC-REP-08 Geometric diagram.

Conversions tested: a curve given as y in terms of x converted to x in terms of y (BC-REP-01 to BC-REP-01 in the other variable), and a figure converted to a horizontal slice integral (BC-REP-02 to BC-REP-01).

### Assessment behaviour

MCQ forms ask which integral in y gives the area of a pictured region. FRQ forms ask for an area where the horizontal slice is the efficient choice, or ask for the same region both ways. Calculator variants allow numerical evaluation after the rewriting; no-calculator variants use curves that invert cleanly. Conceptual variants ask which variable of integration avoids splitting the region; computational variants ask for the value; interpretation variants are rare at this topic; justification variants ask why the horizontal slice needs only one integral. Multi-concept variants pair the choice of variable with a volume set up on the same region. No Unit 8 free response part in 2023 to 2025 required an area with respect to y, so the scoring pattern here is inferred from the area scoring in 2023 (sg-23:16).

### Archetypes

- BC-QA-08009 Area of a region integrated with respect to y
- BC-QA-08008 Area of a region between two curves in x

### Errors and misconceptions

- BC-ERR-08023 Integrand written in one variable with the differential of another
- BC-ERR-08020 Difference of the boundary functions taken in the wrong order
- BC-ERR-08024 Limits given as values of the variable not being integrated
- BC-ERR-08018 Differential omitted from an integral expression
- BC-MIS-08013 The differential can be changed without changing the integrand, severity high

### Diagnostic signals

- BC-SIG-08009 Differential dy attached to an integrand written in x
- BC-SIG-08007 Negative value reported as an area or a volume

### Adaptive metadata summary

Skills in this topic carry calculator relevance none, optional. Remediation targets named across the topic: BC-PRQ-08002, con.area_between_y. Every skill record carries the full seven key adaptive block in data/staging/unit-08.skills.json. [inferred]

## 8.6 Finding the Area Between Curves That Intersect at More Than Two Points

### Official mapping

Topic id BC-TOP-0806, CED code 8.6, name Finding the Area Between Curves That Intersect at More Than Two Points, scope shared, CED page 157. [verified] (ced:157)

- BC-LO-CHA-5A (CHA-5.A): Calculate areas in the plane using the definite integral.
  - BC-EK-CHA-5A3 (CHA-5.A.3): "Areas of certain regions in the plane may be calculated using a sum of two or more definite integrals or by evaluating a definite integral of the absolute value of the difference of two functions."

Suggested practice skills: BC-MPS-2B (Practice skill 2.B). Weighting pointer: [../exam/exam-blueprint.md](../exam/exam-blueprint.md).

### Concept breakdown

- BC-CON-08013 Region split where the boundary curves cross: Where the curves swap places the region has to be cut and the pieces added.

- BC-SKL-08027 Locate every intersection point and order them: Find all the crossings in the interval and list them in order.
- BC-SKL-08028 Determine which curve is greater on each subinterval: Test each piece separately to see which curve is on top there.
- BC-SKL-08029 Write the area as a sum of definite integrals over the subintervals: Add one integral per piece, each with its own order of subtraction.
- BC-SKL-08030 Write the area as the integral of the absolute value of the difference: Use one integral with absolute value bars instead of splitting.

### Prerequisites

- BC-PRQ-08001 -> BC-SKL-08027, supporting, [inferred], Prerequisite for Locate every intersection point and order them.
- BC-PRQ-06005 -> BC-SKL-08028, supporting, [inferred], Prerequisite for Determine which curve is greater on each subinterval.
- BC-PRQ-06005 -> BC-SKL-08029, supporting, [inferred], Prerequisite for Write the area as a sum of definite integrals over the subintervals.
- BC-PRQ-08003 -> BC-SKL-08030, supporting, [inferred], Prerequisite for Write the area as the integral of the absolute value of the difference.

### Required mathematical knowledge

**Split regions.** Areas of certain regions may be calculated using a sum of two or more definite integrals or by evaluating a definite integral of the absolute value of the difference of two functions (BC-EK-CHA-5A3).

**Where to split.** The interior intersection points are the split inputs, so every solution of the equation of the two curves in the interval must be found, not only the two that bound the whole region.

**Equivalence.** The sum of integrals and the single integral of the absolute value give the same number; the absolute value form is the one a calculator evaluates directly.

**Notation.** Each integral in the sum carries its own limits, and the absolute value bars belong inside the integral sign, not around the finished value.

### Representations

Representations in play: BC-REP-01 Symbolic, BC-REP-02 Graphical, BC-REP-09 Calculator-generated numerical result.

Conversions tested: a figure with several crossings converted to a sum of integrals (BC-REP-02 to BC-REP-01), and a sum of integrals converted to one absolute value integral for technology (BC-REP-01 to BC-REP-09).

### Assessment behaviour

MCQ forms offer a single integral of one difference as the distractor for a region whose curves cross. FRQ forms ask for the total area of a region made of two lobes, where the setup point requires both pieces. Calculator variants place the crossings at decimal inputs; no-calculator variants place them at values found by factoring. Conceptual variants ask how many integrals the region needs; computational variants ask for the value; interpretation variants attach a context; justification variants ask why the region must be split. Multi-concept variants combine the split area with a volume on the same region. No 2023 to 2025 Unit 8 free response part required a split region, so the scoring pattern here is inferred.

### Archetypes

- BC-QA-08010 Area of a region whose boundary curves cross

### Errors and misconceptions

- BC-ERR-08025 An interior intersection point not found
- BC-ERR-08020 Difference of the boundary functions taken in the wrong order
- BC-ERR-08026 One integral used across a crossing of the curves
- BC-ERR-08027 Absolute value dropped from a split region integrand
- BC-MIS-08014 One integral covers any region between two curves, severity high
- BC-MIS-08011 The order of subtraction in an area integrand does not matter, severity medium

### Diagnostic signals

- BC-SIG-08010 One integral spanning an interior crossing
- BC-SIG-08007 Negative value reported as an area or a volume

### Adaptive metadata summary

Skills in this topic carry calculator relevance optional, typically_required. Remediation targets named across the topic: BC-PRQ-08001, BC-PRQ-08003, con.split_region. Every skill record carries the full seven key adaptive block in data/staging/unit-08.skills.json. [inferred]

## 8.7 Volumes with Cross Sections: Squares and Rectangles

### Official mapping

Topic id BC-TOP-0807, CED code 8.7, name Volumes with Cross Sections: Squares and Rectangles, scope shared, CED page 158. [verified] (ced:158)

- BC-LO-CHA-5B (CHA-5.B): Calculate volumes of solids with known cross sections using definite integrals.
  - BC-EK-CHA-5B1 (CHA-5.B.1): "Volumes of solids with square and rectangular cross sections can be found using definite integrals and the area formulas for these shapes."

Suggested practice skills: BC-MPS-3D (Practice skill 3.D). Weighting pointer: [../exam/exam-blueprint.md](../exam/exam-blueprint.md).

### Concept breakdown

- BC-CON-08014 Volume as the integral of a cross sectional area: Add up the areas of the slices across the interval.
- BC-CON-08015 Cross sectional dimension read from the region: The side of each slice is the distance between the two boundary curves.

- BC-SKL-08031 Express the side of a cross section as the distance between the curves: Write the side as the top curve minus the bottom curve at that input.
- BC-SKL-08032 Set up the volume integral for square cross sections: Square the side and integrate it over the interval.
- BC-SKL-08033 Set up the volume integral for rectangular cross sections: Multiply the side by the stated second dimension, then integrate.
- BC-SKL-08034 Determine the axis the cross sections are perpendicular to: Read whether the slices stand on the x axis or the y axis and integrate in that variable.
- BC-SKL-08035 Evaluate a cross section volume integral: Expand or use technology, then report the volume.

### Prerequisites

- BC-PRQ-08004 -> BC-SKL-08031, supporting, [inferred], Prerequisite for Express the side of a cross section as the distance between the curves.
- BC-PRQ-08004 -> BC-SKL-08032, supporting, [inferred], Prerequisite for Set up the volume integral for square cross sections.
- BC-PRQ-08004 -> BC-SKL-08033, supporting, [inferred], Prerequisite for Set up the volume integral for rectangular cross sections.
- BC-PRQ-08002 -> BC-SKL-08034, supporting, [inferred], Prerequisite for Determine the axis the cross sections are perpendicular to.
- BC-PRQ-06002 -> BC-SKL-08035, supporting, [inferred], Prerequisite for Evaluate a cross section volume integral.
- BC-SKL-06047 -> BC-SKL-08035, supporting, [inferred], Substitution is often the antidifferentiation route for an expanded squared difference.

### Required mathematical knowledge

**Cross section volume.** Hypotheses: the solid has cross sections perpendicular to an axis whose area at each input is A. Conclusion: the volume is the definite integral of A over the interval the solid spans (BC-EK-CHA-5B1).

**Square and rectangular sections.** The area of a square section is the square of the side; the area of a rectangular section is the side times the second dimension the problem states.

**Side length.** The side is a distance in the plane region, so it is the difference of the two boundary functions, or the single function when one boundary is an axis.

**Notation.** No factor of pi appears for a polygonal cross section; the Chief Reader records integrands taken from the wrong area or volume family as BC-ERR-99011.

### Representations

Representations in play: BC-REP-01 Symbolic, BC-REP-02 Graphical, BC-REP-04 Verbal description, BC-REP-08 Geometric diagram.

Conversions tested: a verbal description of the solid to a diagram of one slice (BC-REP-04 to BC-REP-08), and the slice to an integrand (BC-REP-08 to BC-REP-01).

### Assessment behaviour

MCQ forms ask which integral gives the volume of a solid whose base is a pictured region. FRQ forms ask for the volume with a setup point for the integrand and limits and an answer point. Calculator variants use a base region with decimal intersection points; no-calculator variants use an antidifferentiable squared difference. Conceptual variants ask what the integrand represents; computational variants ask for the number; interpretation variants attach units of volume; justification variants ask why no factor of pi appears. Multi-concept variants build the base region from an area part earlier in the same question. No 2023 to 2025 BC free response part asked for a volume with known cross sections, so the scoring pattern is inferred from the general setup and answer structure used for area (sg-23:16).

### Archetypes

- BC-QA-08011 Volume of a solid with known cross sections

### Errors and misconceptions

- BC-ERR-08028 Cross sectional side written as one function value
- BC-ERR-08029 Factor of pi placed in a polygonal cross section integrand
- BC-ERR-08030 Square of a difference used where a difference of squares is needed
- BC-ERR-08031 Second dimension of a rectangular cross section omitted
- BC-ERR-08023 Integrand written in one variable with the differential of another
- BC-ERR-08005 Intermediate value rounded before the final computation
- BC-MIS-08016 The cross sectional dimension is a function value, severity high
- BC-MIS-08015 Every volume integral carries a factor of pi, severity medium
- BC-MIS-08013 The differential can be changed without changing the integrand, severity high
- BC-MIS-08017 The difference of squares equals the square of the difference, severity high

### Diagnostic signals

- BC-SIG-08011 Factor of pi in a polygonal cross section integrand
- BC-SIG-08009 Differential dy attached to an integrand written in x

### Adaptive metadata summary

Skills in this topic carry calculator relevance none, optional. Remediation targets named across the topic: BC-PRQ-08002, BC-PRQ-08004, con.cross_section_volume. Every skill record carries the full seven key adaptive block in data/staging/unit-08.skills.json. [inferred]

## 8.8 Volumes with Cross Sections: Triangles and Semicircles

### Official mapping

Topic id BC-TOP-0808, CED code 8.8, name Volumes with Cross Sections: Triangles and Semicircles, scope shared, CED page 159. [verified] (ced:159)

- BC-LO-CHA-5B (CHA-5.B): Calculate volumes of solids with known cross sections using definite integrals.
  - BC-EK-CHA-5B2 (CHA-5.B.2): "Volumes of solids with triangular cross sections can be found using definite integrals and the area formulas for these shapes."
  - BC-EK-CHA-5B3 (CHA-5.B.3): "Volumes of solids with semicircular and other geometrically defined cross sections can be found using definite integrals and the area formulas for these shapes."

Suggested practice skills: BC-MPS-3D (Practice skill 3.D). Weighting pointer: [../exam/exam-blueprint.md](../exam/exam-blueprint.md).

### Concept breakdown

- BC-CON-08016 Cross sectional area from the shape of the slice: Each named shape has its own area formula, applied to the same distance.

- BC-SKL-08036 Write the area of an equilateral triangular cross section: Use the equilateral triangle formula with the distance as the side.
- BC-SKL-08037 Write the area of a right isosceles triangular cross section: Decide whether the distance is a leg or the hypotenuse, then use the matching formula.
- BC-SKL-08038 Write the area of a semicircular cross section from the diameter: Halve the distance to get the radius before squaring.
- BC-SKL-08039 Set up and evaluate the volume integral for a named cross section: Put the shape formula in the integral and evaluate it.

### Prerequisites

- BC-PRQ-08005 -> BC-SKL-08036, supporting, [inferred], Prerequisite for Write the area of an equilateral triangular cross section.
- BC-PRQ-08005 -> BC-SKL-08037, supporting, [inferred], Prerequisite for Write the area of a right isosceles triangular cross section.
- BC-PRQ-06007 -> BC-SKL-08038, supporting, [inferred], Prerequisite for Write the area of a semicircular cross section from the diameter.
- BC-PRQ-06002 -> BC-SKL-08039, supporting, [inferred], Prerequisite for Set up and evaluate the volume integral for a named cross section.

### Required mathematical knowledge

**Triangular sections.** Volumes of solids with triangular cross sections are found with the area formulas for those triangles (BC-EK-CHA-5B2). For an equilateral triangle of side s the area is s squared times the square root of three over four; for a right isosceles triangle the area is half the square of a leg, or one quarter of the square of the hypotenuse.

**Semicircular sections.** Volumes of solids with semicircular and other geometrically defined cross sections are found with the area formulas for those shapes (BC-EK-CHA-5B3). When the distance between the curves is the diameter, the radius is half that distance and the area is pi over eight times the square of the distance.

**Notation.** The fractional factor belongs inside the integral, and the distance between the curves is squared as a whole rather than term by term.

### Representations

Representations in play: BC-REP-01 Symbolic, BC-REP-04 Verbal description, BC-REP-08 Geometric diagram.

Conversions tested: the named shape to its area formula (BC-REP-04 to BC-REP-01), and the diagram of the slice to the correct role of the distance as side, leg, hypotenuse, or diameter (BC-REP-08 to BC-REP-01).

### Assessment behaviour

MCQ forms vary the named shape while holding the base region fixed, so the discriminating feature is the area formula. FRQ forms ask for the volume with a setup point and an answer point. Calculator variants evaluate numerically; no-calculator variants keep the constant factor symbolic. Conceptual variants ask what the distance between the curves represents in the slice; computational variants ask for the value; interpretation variants attach units; justification variants ask why the radius is half the distance. Multi-concept variants reuse a base region from an area part. No 2023 to 2025 BC free response part asked for such a volume, so the scoring pattern is inferred.

### Archetypes

- BC-QA-08011 Volume of a solid with known cross sections

### Errors and misconceptions

- BC-ERR-08032 Constant factor of a cross sectional area formula wrong or missing
- BC-ERR-08033 Distance between the curves used as a leg when it is the hypotenuse
- BC-ERR-08034 Distance between the curves used as the radius of a semicircle
- BC-ERR-08035 Full circle area used for a semicircular cross section
- BC-ERR-08030 Square of a difference used where a difference of squares is needed
- BC-MIS-08019 Area formulas are recalled without their constant factors, severity medium
- BC-MIS-08018 The distance between the curves is always the radius, severity high

### Diagnostic signals

- BC-SIG-08012 Full circle area used for a semicircular section

### Adaptive metadata summary

Skills in this topic carry calculator relevance none, optional. Remediation targets named across the topic: BC-PRQ-08005, con.shape_area_formulas. Every skill record carries the full seven key adaptive block in data/staging/unit-08.skills.json. [inferred]

## 8.9 Volume with Disc Method: Revolving Around the x- or y-Axis

### Official mapping

Topic id BC-TOP-0809, CED code 8.9, name Volume with Disc Method: Revolving Around the x- or y-Axis, scope shared, CED page 160. [verified] (ced:160)

- BC-LO-CHA-5C (CHA-5.C): Calculate volumes of solids of revolution using definite integrals.
  - BC-EK-CHA-5C1 (CHA-5.C.1): "Volumes of solids of revolution around the x- or y-axis may be found by using definite integrals with the disc method."

Suggested practice skills: BC-MPS-3D (Practice skill 3.D). Weighting pointer: [../exam/exam-blueprint.md](../exam/exam-blueprint.md).

### Concept breakdown

- BC-CON-08017 Disc method for a solid of revolution: Revolving a region against the axis makes discs whose radius is the curve.

- BC-SKL-08040 Identify the radius of a disc as the distance to the axis: The radius is the function value when the axis is the x axis.
- BC-SKL-08041 Set up the disc integral about the x axis: Integrate pi times the square of the function with respect to x.
- BC-SKL-08042 Set up the disc integral about the y axis: Rewrite the curve in y, then integrate pi times the square with respect to y.
- BC-SKL-08043 Evaluate a disc volume and report it with the factor of pi: Do the integral and keep pi in the answer.

### Prerequisites

- BC-PRQ-08004 -> BC-SKL-08040, supporting, [inferred], Prerequisite for Identify the radius of a disc as the distance to the axis.
- BC-PRQ-08004 -> BC-SKL-08041, supporting, [inferred], Prerequisite for Set up the disc integral about the x axis.
- BC-PRQ-08002 -> BC-SKL-08042, supporting, [inferred], Prerequisite for Set up the disc integral about the y axis.
- BC-PRQ-06002 -> BC-SKL-08043, supporting, [inferred], Prerequisite for Evaluate a disc volume and report it with the factor of pi.

### Required mathematical knowledge

**Disc method.** Volumes of solids of revolution around the x or y axis may be found using definite integrals with the disc method (BC-EK-CHA-5C1). Hypotheses: the region is bounded by the curve and the axis of revolution, with no gap between them. Conclusion: the volume is pi times the definite integral of the square of the distance from the curve to the axis.

**Variable of integration.** Revolution about the x axis integrates in x; revolution about the y axis integrates in y, which requires the curve written as a function of y.

**Notation.** The factor pi multiplies the whole integral, and the radius is squared before integration rather than after.

### Representations

Representations in play: BC-REP-01 Symbolic, BC-REP-02 Graphical, BC-REP-08 Geometric diagram, BC-REP-09 Calculator-generated numerical result.

Conversions tested: a pictured region and an axis to a disc diagram (BC-REP-02 to BC-REP-08), and the disc to an integrand in the correct variable (BC-REP-08 to BC-REP-01).

### Assessment behaviour

MCQ forms ask which integral gives the volume, with the unsquared radius and the missing pi as distractors. FRQ forms score the integrand and limits as a setup point and the value as an answer point. Calculator variants evaluate numerically; no-calculator variants leave the answer as a multiple of pi. Conceptual variants ask what the radius is; computational variants ask for the number; interpretation variants attach units of volume; justification variants ask why the region touches the axis. Multi-concept variants share a region with an area part. No 2023 to 2025 BC free response part asked for a solid of revolution, so the scoring pattern is inferred.

### Archetypes

- BC-QA-08012 Volume of a solid of revolution by the disc method

### Errors and misconceptions

- BC-ERR-08036 Radius left unsquared in a solid of revolution integrand
- BC-ERR-08037 Factor of pi omitted from a solid of revolution integrand
- BC-ERR-08023 Integrand written in one variable with the differential of another
- BC-ERR-08024 Limits given as values of the variable not being integrated
- BC-ERR-08005 Intermediate value rounded before the final computation
- BC-MIS-08020 A volume of revolution integrates the radius rather than its square, severity high
- BC-MIS-08013 The differential can be changed without changing the integrand, severity high

### Diagnostic signals

- BC-SIG-08013 Solid of revolution volume reported without pi
- BC-SIG-08009 Differential dy attached to an integrand written in x

### Adaptive metadata summary

Skills in this topic carry calculator relevance none, optional. Remediation targets named across the topic: BC-PRQ-08002, BC-PRQ-08004, con.disc_method. Every skill record carries the full seven key adaptive block in data/staging/unit-08.skills.json. [inferred]

## 8.10 Volume with Disc Method: Revolving Around Other Axes

### Official mapping

Topic id BC-TOP-0810, CED code 8.10, name Volume with Disc Method: Revolving Around Other Axes, scope shared, CED page 161. [verified] (ced:161)

- BC-LO-CHA-5C (CHA-5.C): Calculate volumes of solids of revolution using definite integrals.
  - BC-EK-CHA-5C2 (CHA-5.C.2): "Volumes of solids of revolution around any horizontal or vertical line in the plane may be found by using definite integrals with the disc method."

Suggested practice skills: BC-MPS-2D (Practice skill 2.D). Weighting pointer: [../exam/exam-blueprint.md](../exam/exam-blueprint.md).

### Concept breakdown

- BC-CON-08018 Radius measured from a line other than an axis: When the axis moves, the radius becomes a difference from that line.

- BC-SKL-08044 Write the radius as the distance from a curve to a horizontal line: Subtract the line from the curve, or the curve from the line, whichever is positive.
- BC-SKL-08045 Write the radius as the distance from a curve to a vertical line: Use the horizontal distance to the vertical line as the radius.
- BC-SKL-08046 Set up the disc integral about a line other than an axis: Integrate pi times the square of the shifted radius.
- BC-SKL-08047 Keep the limits of integration unchanged when the axis shifts: Moving the axis changes the radius, not the interval.

### Prerequisites

- BC-PRQ-08004 -> BC-SKL-08044, supporting, [inferred], Prerequisite for Write the radius as the distance from a curve to a horizontal line.
- BC-PRQ-08002 -> BC-SKL-08045, supporting, [inferred], Prerequisite for Write the radius as the distance from a curve to a vertical line.
- BC-PRQ-08004 -> BC-SKL-08046, supporting, [inferred], Prerequisite for Set up the disc integral about a line other than an axis.
- BC-PRQ-08004 -> BC-SKL-08047, supporting, [inferred], Prerequisite for Keep the limits of integration unchanged when the axis shifts.

### Required mathematical knowledge

**Shifted axis.** Volumes of solids of revolution around any horizontal or vertical line in the plane may be found with the disc method (BC-EK-CHA-5C2).

**Radius.** The radius is the distance from the curve to the axis of revolution, so revolving about y equal k gives a radius of the function value minus k when the region is above the line and k minus the function value when it is below.

**Limits.** The limits still describe the extent of the region in the variable of slicing; they do not move when the axis moves.

**Notation.** Writing the radius as a single parenthesised difference guards against the parenthesis loss the Chief Reader records as BC-ERR-99009.

### Representations

Representations in play: BC-REP-01 Symbolic, BC-REP-02 Graphical, BC-REP-08 Geometric diagram.

Conversions tested: a figure with a drawn axis of revolution to a radius expression (BC-REP-02 to BC-REP-01), and a verbal statement of the axis to a labelled slice (BC-REP-04 to BC-REP-08).

### Assessment behaviour

MCQ forms hold the region fixed and vary the axis of revolution, so the discriminating feature is the shifted radius. FRQ forms score the setup and the value. Calculator variants evaluate numerically; no-calculator variants keep pi symbolic. Conceptual variants ask how the radius changes when the axis moves; computational variants ask for the number; interpretation variants attach units; justification variants ask why the limits are unchanged. Multi-concept variants revolve the same region about two different lines in consecutive parts. No 2023 to 2025 BC free response part asked for a solid of revolution about a shifted axis, so the scoring pattern is inferred.

### Archetypes

- BC-QA-08012 Volume of a solid of revolution by the disc method

### Errors and misconceptions

- BC-ERR-08038 Radius measured from a coordinate axis when the axis of revolution is elsewhere
- BC-ERR-08023 Integrand written in one variable with the differential of another
- BC-ERR-08039 Limits of integration moved along with the axis of revolution
- BC-MIS-08021 The radius is the function value whatever the axis of revolution is, severity high
- BC-MIS-08022 Moving the axis of revolution moves the limits of integration, severity medium

### Diagnostic signals

- BC-SIG-08015 Radius written as the bare function value about a shifted axis

### Adaptive metadata summary

Skills in this topic carry calculator relevance none, optional. Remediation targets named across the topic: BC-PRQ-08002, BC-PRQ-08004. Every skill record carries the full seven key adaptive block in data/staging/unit-08.skills.json. [inferred]

## 8.11 Volume with Washer Method: Revolving Around the x- or y-Axis

### Official mapping

Topic id BC-TOP-0811, CED code 8.11, name Volume with Washer Method: Revolving Around the x- or y-Axis, scope shared, CED page 162. [verified] (ced:162)

- BC-LO-CHA-5C (CHA-5.C): Calculate volumes of solids of revolution using definite integrals.
  - BC-EK-CHA-5C3 (CHA-5.C.3): "Volumes of solids of revolution around the x- or y-axis whose cross sections are ring shaped may be found using definite integrals with the washer method."

Suggested practice skills: BC-MPS-4E (Practice skill 4.E). Weighting pointer: [../exam/exam-blueprint.md](../exam/exam-blueprint.md).

### Concept breakdown

- BC-CON-08019 Washer method for a region held away from the axis: When the region does not touch the axis the slices are rings with two radii.

- BC-SKL-08048 Identify the outer and inner radii of a washer: The curve farther from the axis gives the outer radius.
- BC-SKL-08049 Set up the washer integral about the x axis: Integrate pi times outer squared minus inner squared with respect to x.
- BC-SKL-08050 Set up the washer integral about the y axis: Rewrite both curves in y, then integrate the difference of squares.
- BC-SKL-08051 Subtract the squares of the radii rather than squaring their difference: Square each radius first, then subtract.

### Prerequisites

- BC-PRQ-08004 -> BC-SKL-08048, supporting, [inferred], Prerequisite for Identify the outer and inner radii of a washer.
- BC-PRQ-08004 -> BC-SKL-08049, supporting, [inferred], Prerequisite for Set up the washer integral about the x axis.
- BC-PRQ-08002 -> BC-SKL-08050, supporting, [inferred], Prerequisite for Set up the washer integral about the y axis.
- BC-PRQ-06002 -> BC-SKL-08051, supporting, [inferred], Prerequisite for Subtract the squares of the radii rather than squaring their difference.

### Required mathematical knowledge

**Washer method.** Volumes of solids of revolution around the x or y axis whose cross sections are ring shaped may be found with the washer method (BC-EK-CHA-5C3). Hypotheses: the region lies between two curves and does not meet the axis of revolution on the interior of the interval. Conclusion: the volume is pi times the definite integral of the outer radius squared minus the inner radius squared.

**Order of operations.** The two radii are squared before they are subtracted. The square of a difference is not the difference of the squares, and this is the algebraic step that separates a correct washer integrand from a common incorrect one.

**Notation.** Each radius is parenthesised before being squared.

### Representations

Representations in play: BC-REP-01 Symbolic, BC-REP-02 Graphical, BC-REP-08 Geometric diagram.

Conversions tested: a pictured region separated from the axis to a ring diagram (BC-REP-02 to BC-REP-08), and the ring to an integrand with two squared radii (BC-REP-08 to BC-REP-01).

### Assessment behaviour

MCQ forms offer the squared difference of the radii as a distractor. FRQ forms score the integrand and limits as a setup point and the value as an answer point. Calculator variants evaluate numerically; no-calculator variants expand the squares and antidifferentiate. Conceptual variants ask which radius is outer; computational variants ask for the value; interpretation variants attach units; justification variants ask why a washer rather than a disc is needed. Multi-concept variants attach the volume to a region whose area was found earlier. No 2023 to 2025 BC free response part asked for a washer volume, so the scoring pattern is inferred.

### Archetypes

- BC-QA-08013 Volume of a solid of revolution by the washer method

### Errors and misconceptions

- BC-ERR-08040 Outer and inner radii of a washer exchanged
- BC-ERR-08030 Square of a difference used where a difference of squares is needed
- BC-ERR-08037 Factor of pi omitted from a solid of revolution integrand
- BC-ERR-08023 Integrand written in one variable with the differential of another
- BC-ERR-08024 Limits given as values of the variable not being integrated
- BC-MIS-08017 The difference of squares equals the square of the difference, severity high
- BC-MIS-08013 The differential can be changed without changing the integrand, severity high

### Diagnostic signals

- BC-SIG-08016 Negative volume from exchanged radii
- BC-SIG-08014 Washer integrand written as one squared difference
- BC-SIG-08009 Differential dy attached to an integrand written in x

### Adaptive metadata summary

Skills in this topic carry calculator relevance none, optional. Remediation targets named across the topic: BC-PRQ-08002, BC-PRQ-08004, con.washer_method. Every skill record carries the full seven key adaptive block in data/staging/unit-08.skills.json. [inferred]

## 8.12 Volume with Washer Method: Revolving Around Other Axes

### Official mapping

Topic id BC-TOP-0812, CED code 8.12, name Volume with Washer Method: Revolving Around Other Axes, scope shared, CED page 163. [verified] (ced:163)

- BC-LO-CHA-5C (CHA-5.C): Calculate volumes of solids of revolution using definite integrals.
  - BC-EK-CHA-5C4 (CHA-5.C.4): "Volumes of solids of revolution around any horizontal or vertical line whose cross sections are ring shaped may be found using definite integrals with the washer method."

Suggested practice skills: BC-MPS-2D (Practice skill 2.D). Weighting pointer: [../exam/exam-blueprint.md](../exam/exam-blueprint.md).

### Concept breakdown

- BC-CON-08020 Washer radii measured from a line other than an axis: Both radii become distances from the shifted line.

- BC-SKL-08052 Write both washer radii as distances from a horizontal line: Subtract the line value from each curve before squaring.
- BC-SKL-08053 Write both washer radii as distances from a vertical line: Use horizontal distances from the vertical line for both curves.
- BC-SKL-08054 Determine which boundary curve is farther from the shifted axis: Check which curve is farther from the line, which can differ from which is higher.
- BC-SKL-08055 Set up the washer integral about a line other than an axis: Integrate pi times the difference of the squares of the two shifted radii.

### Prerequisites

- BC-PRQ-08004 -> BC-SKL-08052, supporting, [inferred], Prerequisite for Write both washer radii as distances from a horizontal line.
- BC-PRQ-08002 -> BC-SKL-08053, supporting, [inferred], Prerequisite for Write both washer radii as distances from a vertical line.
- BC-PRQ-08004 -> BC-SKL-08054, supporting, [inferred], Prerequisite for Determine which boundary curve is farther from the shifted axis.
- BC-PRQ-08004 -> BC-SKL-08055, supporting, [inferred], Prerequisite for Set up the washer integral about a line other than an axis.

### Required mathematical knowledge

**Shifted washer.** Volumes of solids of revolution around any horizontal or vertical line whose cross sections are ring shaped may be found with the washer method (BC-EK-CHA-5C4).

**Which radius is outer.** The outer radius belongs to the curve farther from the axis of revolution. When the axis lies above the region, the lower curve is the farther one, so the roles of the two curves exchange.

**Notation.** Each shifted radius is written as a parenthesised difference and squared as a whole.

### Representations

Representations in play: BC-REP-01 Symbolic, BC-REP-02 Graphical, BC-REP-08 Geometric diagram.

Conversions tested: a figure with the axis of revolution drawn above or beside the region to a pair of radius expressions (BC-REP-02 to BC-REP-01).

### Assessment behaviour

MCQ forms hold the region fixed and move the axis so that the roles of the curves exchange. FRQ forms score the integrand and limits as a setup point and the value as an answer point. Calculator variants evaluate numerically; no-calculator variants keep pi symbolic. Conceptual variants ask which curve gives the outer radius; computational variants ask for the number; interpretation variants attach units; justification variants ask why the roles exchange. Multi-concept variants revolve the same region about several lines across parts. No 2023 to 2025 BC free response part asked for a shifted washer volume, so the scoring pattern is inferred.

### Archetypes

- BC-QA-08013 Volume of a solid of revolution by the washer method

### Errors and misconceptions

- BC-ERR-08038 Radius measured from a coordinate axis when the axis of revolution is elsewhere
- BC-ERR-08040 Outer and inner radii of a washer exchanged
- BC-ERR-08023 Integrand written in one variable with the differential of another
- BC-ERR-08030 Square of a difference used where a difference of squares is needed
- BC-MIS-08021 The radius is the function value whatever the axis of revolution is, severity high
- BC-MIS-08013 The differential can be changed without changing the integrand, severity high
- BC-MIS-08023 The upper curve always gives the outer radius, severity medium
- BC-MIS-08017 The difference of squares equals the square of the difference, severity high

### Diagnostic signals

- BC-SIG-08015 Radius written as the bare function value about a shifted axis
- BC-SIG-08016 Negative volume from exchanged radii
- BC-SIG-08014 Washer integrand written as one squared difference

### Adaptive metadata summary

Skills in this topic carry calculator relevance none, optional. Remediation targets named across the topic: BC-PRQ-08002, BC-PRQ-08004. Every skill record carries the full seven key adaptive block in data/staging/unit-08.skills.json. [inferred]

## 8.13 The Arc Length of a Smooth, Planar Curve and Distance Traveled

### Official mapping

Topic id BC-TOP-0813, CED code 8.13, name The Arc Length of a Smooth, Planar Curve and Distance Traveled, scope BC_only, CED page 164. [verified] (ced:164)

- BC-LO-CHA-6A (CHA-6.A): Determine the length of a curve in the plane defined by a function, using a definite integral.
  - BC-EK-CHA-6A1 (CHA-6.A.1): "The length of a planar curve defined by a function can be calculated using a definite integral."

Suggested practice skills: BC-MPS-3D (Practice skill 3.D). Weighting pointer: [../exam/exam-blueprint.md](../exam/exam-blueprint.md).

### Concept breakdown

- BC-CON-08021 Arc length of a curve given by a function: The length of a graph is the integral of the square root of one plus the square of the slope.

- BC-SKL-08056 State the arc length integral for a function on an interval: Write the integral of the square root of one plus the derivative squared.
- BC-SKL-08057 Set up an arc length integral from a described curve: Differentiate the given function and place it inside the radical.
- BC-SKL-08058 Identify a given integral as an arc length and name the interval: Recognise the radical form and say which curve and interval it measures.
- BC-SKL-08059 Evaluate an arc length integral with technology: Enter the radical integrand and report the decimal.

### Prerequisites

- BC-PRQ-08007 -> BC-SKL-08056, supporting, [inferred], Prerequisite for State the arc length integral for a function on an interval.
- BC-PRQ-06005 -> BC-SKL-08057, supporting, [inferred], Prerequisite for Set up an arc length integral from a described curve.
- BC-PRQ-06005 -> BC-SKL-08058, supporting, [inferred], Prerequisite for Identify a given integral as an arc length and name the interval.
- BC-PRQ-08006 -> BC-SKL-08059, supporting, [inferred], Prerequisite for Evaluate an arc length integral with technology.
- BC-SKL-06034 -> BC-SKL-08059, supporting, [verified], Arc length integrals are definite integrals evaluated by the Fundamental Theorem of Calculus or with technology.
- BC-TOP-0204 -> BC-SKL-08057, hard_prerequisite, [inferred], Differentiating the given function precedes the arc length integrand; no Unit 2 skill id exists yet.

### Required mathematical knowledge

**Arc length.** The length of a planar curve defined by a function can be calculated using a definite integral (BC-EK-CHA-6A1). Hypotheses: f has a continuous derivative on [a,b]. Conclusion: the length of the graph of f over [a,b] is the definite integral of the square root of one plus the square of f prime, with respect to x.

**Identification.** A response asked what such an integral tells about the graph must name both the quantity and the interval; in 2024 these were two separate points, one for arc length and one for the interval (sg-24:16).

**Scope.** This topic carries the BC only marker in the CED (ced:164).

**Notation.** The derivative is squared inside the radical; the radical covers the whole sum.

### Representations

Representations in play: BC-REP-01 Symbolic, BC-REP-04 Verbal description, BC-REP-09 Calculator-generated numerical result.

Conversions tested: an integral expression to a verbal statement of what it measures (BC-REP-01 to BC-REP-04), and a function with an interval to a numerical length (BC-REP-01 to BC-REP-09).

### Assessment behaviour

MCQ forms ask which integral gives the length of a curve, with the volume and area forms as distractors. FRQ forms ask what a displayed integral tells about the graph of a function, scoring the identification and the interval separately (sg-24:16), or ask for the length of a described curve in the calculator active section. Calculator variants require numerical evaluation of a radical integrand; no-calculator variants ask only for the setup or the identification. Conceptual variants ask what the integrand measures; computational variants ask for the value; interpretation variants ask for the meaning in a context; justification variants ask why the derivative appears squared. Multi-concept variants place the arc length part next to an Euler method part and an integration by parts part in the same question (frq-24:9).

### Archetypes

- BC-QA-08014 Arc length of a curve given by a function

### Errors and misconceptions

- BC-ERR-08041 Arc length integrand written without the radical or without the added one
- BC-ERR-08042 Derivative not squared inside the arc length radical
- BC-ERR-08019 Limits of integration taken from the wrong inputs
- BC-ERR-08043 Arc length identified without naming the interval
- BC-ERR-08044 Arc length integral described as an area
- BC-ERR-08005 Intermediate value rounded before the final computation
- BC-ERR-08045 Numerical length or volume reported with no integral shown
- BC-MIS-08024 An integral over an interval measures an area, severity high
- BC-MIS-08003 A calculator answer stands on its own, severity medium

### Diagnostic signals

- BC-SIG-08017 Arc length named with no interval

### Adaptive metadata summary

Skills in this topic carry calculator relevance none, optional, typically_required. Remediation targets named across the topic: BC-PRQ-08006, BC-PRQ-08007, con.arc_length. Every skill record carries the full seven key adaptive block in data/staging/unit-08.skills.json. [inferred]

## Cross-unit connections

Cross-unit edges to Unit 6 use the skill ids already present in data/skills.json. Edges to Units 2, 4, and 5 use BC-TOP ids as the node on the other unit's side, because no skills exist in data/skills.json for those units yet; the `notes` field on each edge in data/staging/unit-08.edges.csv describes the skill that the topic id stands in for. [inferred]

### What Unit 8 depends on

**Unit 6 integration and accumulation.** Every topic of this unit is a definite integral applied to a quantity. The average value skills rest on BC-SKL-06038 and BC-SKL-06034; the motion and applied accumulation skills rest on BC-SKL-06036 and BC-SKL-06037; the area, volume, and arc length evaluations rest on BC-SKL-06034, on BC-SKL-06028 where the integral is read from a graph, and on BC-SKL-06047 where an expanded squared difference is antidifferentiated by substitution.

**Unit 2 derivatives.** BC-SKL-08057, the arc length setup, differentiates the given function before the integrand can be written, recorded as an edge from BC-TOP-0204.

**Unit 4 contextual applications.** The vocabulary that separates displacement, speed, and total distance is introduced with rectilinear motion in Unit 4, recorded as an edge from BC-TOP-0402.

**Unit 5 analytical applications.** The justification that an accumulated amount is maximal uses the first derivative test and the candidates test, recorded as edges from BC-TOP-0504 and BC-TOP-0505. The 2025 scoring guideline required the global form of that argument (sg-25:5).

### What depends on Unit 8

**Unit 9.** The planar motion skills of Unit 9 are the two component form of the rectilinear motion skills recorded here, and the polar area skills are the area between curves skills transported to a new coordinate system. The parametric arc length topic BC-TOP-0903 is the parametric form of BC-TOP-0813.

## Archetype summary

14 archetypes with 40 variants are recorded in data/staging/unit-08.archetypes.json. Variant dimensions used are representation, reasoning direction, notation, and calculator. [verified] (sg-23:2, sg-23:16, sg-23:17, sg-24:3, sg-24:4, sg-24:7, sg-24:16, sg-25:2, sg-25:5)

| Archetype | Name | Scope | Calculator | Official parts read |
|---|---|---|---|---|
| BC-QA-08001 | Average value of a function over an interval | shared | calculator | 2025 Q1(A), 2023 Q1(c), 2024 Q1(b) |
| BC-QA-08002 | Instantaneous rate set equal to an average rate of change | shared | calculator | 2025 Q1(B) |
| BC-QA-08003 | Rectilinear motion analysed with definite integrals | shared | either | no rectilinear part in the 2023 to 2025 BC free response questions; the planar analogue appears at 2024 Q2(b) and 2024 Q2(c) |
| BC-QA-08004 | Amount at a later time from an initial amount and a rate | shared | calculator | 2024 Q1(c), 2025 Q3(D), 2024 Q2(c) |
| BC-QA-08005 | Accumulation with a rate in and a rate out | shared | calculator | no rate in and rate out part appears in the 2023 to 2025 BC free response questions |
| BC-QA-08006 | Time at which an accumulated amount is maximal | shared | calculator | 2025 Q1(D) |
| BC-QA-08007 | Interpreting a definite integral of a rate in context | shared | either | 2023 Q1(a), 2024 Q1(b) |
| BC-QA-08008 | Area of a region between two curves in x | shared | either | 2023 Q5(a) |
| BC-QA-08009 | Area of a region integrated with respect to y | shared | either | no area with respect to y appears in the 2023 to 2025 BC free response questions |
| BC-QA-08010 | Area of a region whose boundary curves cross | shared | either | no split region area appears in the 2023 to 2025 BC free response questions |
| BC-QA-08011 | Volume of a solid with known cross sections | shared | either | no known cross section volume appears in the 2023 to 2025 BC free response questions |
| BC-QA-08012 | Volume of a solid of revolution by the disc method | shared | either | no solid of revolution appears in the 2023 to 2025 BC free response questions |
| BC-QA-08013 | Volume of a solid of revolution by the washer method | shared | either | no washer volume appears in the 2023 to 2025 BC free response questions |
| BC-QA-08014 | Arc length of a curve given by a function | BC_only | either | 2024 Q5(b) |

Four archetypes are grounded directly in 2023 to 2025 scoring guidelines: the average value computation (sg-25:2), the accumulated amount from an initial value (sg-24:4, sg-24:7), the maximum of an accumulated amount (sg-25:5), and the area between two curves (sg-23:16). The volume archetypes carry inferred scoring patterns because no 2023 to 2025 BC free response part asked for a volume.

## Misconception summary

24 misconceptions are recorded in data/staging/unit-08.misconceptions.json, each with the rival it is most easily confused with and a probe that separates them. [inferred]

| Misconception | Severity | Rivals | Discriminating probe |
|---|---|---|---|
| BC-MIS-08001 Average value and average rate of change are the same quantity | high | BC-MIS-08002 | Ask which of the two answers carries the units of the function and which carries the units of a rate. |
| BC-MIS-08002 The integral of a function is its average | high | BC-MIS-08001 | Ask for the average value of the constant function two over an interval of length five. |
| BC-MIS-08003 A calculator answer stands on its own | medium | BC-MIS-08009 | Ask the student to write, without the calculator, the expression whose value the calculator reported. |
| BC-MIS-08004 Distance travelled and net change in position are the same | high | BC-MIS-08005 | Give a velocity that is positive on the first half of an interval and the negative of that on the second half, and ask for both quantities. |
| BC-MIS-08005 Speed is another name for velocity | medium | BC-MIS-08004 | Ask for the speed of a particle whose velocity is a stated negative number. |
| BC-MIS-08006 The integral of a rate is the amount of the quantity | high | BC-MIS-08009 | Give one rate and two different starting amounts and ask for the value at the later time in each case. |
| BC-MIS-08007 Two rates acting at once combine by addition | medium | BC-MIS-08006 | Ask what the stored amount does at a time when the two rates are equal. |
| BC-MIS-08008 A local extremum argument settles an absolute extremum | high | BC-MIS-08006 | Give a function whose only interior critical point is a relative maximum but whose largest value on the interval is at an endpoint. |
| BC-MIS-08009 An interpretation is complete once the quantity is named | medium | BC-MIS-08006 | Ask what would change in the sentence if the limits of the integral were different. |
| BC-MIS-08010 The area between curves is the integral of the curve that bounds it | high | BC-MIS-08011 | Ask for the area between two horizontal lines and compare it with the integral of the upper line alone. |
| BC-MIS-08011 The order of subtraction in an area integrand does not matter | medium | BC-MIS-08010 | Ask the student to write the statement that links the integral to the area and then to check it numerically. |
| BC-MIS-08012 Limits of integration are a viewing window rather than a boundary | medium | BC-MIS-08014 | Ask which inputs bound the shaded region and why those and not the ends of the axes. |
| BC-MIS-08013 The differential can be changed without changing the integrand | high | BC-MIS-08012 | Ask the student to name every variable that appears in the integrand and compare it with the differential. |
| BC-MIS-08014 One integral covers any region between two curves | high | BC-MIS-08011 | Ask for the sign of the integrand on each side of the interior crossing. |
| BC-MIS-08015 Every volume integral carries a factor of pi | medium | BC-MIS-08020 | Ask which shape the area formula inside the integral describes. |
| BC-MIS-08016 The cross sectional dimension is a function value | high | BC-MIS-08015 | Ask the student to draw the slice on the figure and label both of its endpoints. |
| BC-MIS-08017 The difference of squares equals the square of the difference | high | BC-MIS-08023 | Ask the student to evaluate both expressions with the radii five and three. |
| BC-MIS-08018 The distance between the curves is always the radius | high | BC-MIS-08019 | Ask for the radius of a semicircle whose diameter is a stated length. |
| BC-MIS-08019 Area formulas are recalled without their constant factors | medium | BC-MIS-08018 | Ask for the area of one slice of the named shape with a numerical dimension. |
| BC-MIS-08020 A volume of revolution integrates the radius rather than its square | high | BC-MIS-08015 | Ask for the area of a single disc of a stated radius before the integral is written. |
| BC-MIS-08021 The radius is the function value whatever the axis of revolution is | high | BC-MIS-08022 | Ask for the distance from a named point on the curve to the stated axis of revolution. |
| BC-MIS-08022 Moving the axis of revolution moves the limits of integration | medium | BC-MIS-08021 | Ask which inputs the region occupies before the axis of revolution is named. |
| BC-MIS-08023 The upper curve always gives the outer radius | medium | BC-MIS-08017 | Revolve the same region about a line above it and ask which curve is farther from that line. |
| BC-MIS-08024 An integral over an interval measures an area | high | BC-MIS-08009 | Ask what integrand would give the area under the same graph and compare it with the one displayed. |

The highest severity clusters are the four that official scoring guidelines document directly: averaging the function values confused with averaging the rate of change (sg-25:4), the integral of a rate reported as the amount itself (sg-24:4, sg-24:7), a local argument offered for a global maximum (sg-25:5), and a definite integral read as an area whatever its integrand (sg-24:16).

## Unresolved

- No 2023 to 2025 BC free response part assessed a volume, by cross sections or by revolution, and none assessed an area with respect to y or a split region. The scoring patterns for BC-QA-08011, BC-QA-08012, BC-QA-08013, BC-QA-08009, and BC-QA-08010 are inferred from the area and setup scoring used in 2023 and should be revisited when earlier years or official multiple choice material are indexed. [uncertain]
- The 2023 and 2025 scoring guidelines treat unclear communication between a correct average value integral and a correct quotient differently: 2023 awards one of two points (sg-23:4) and 2025 treats the linkage as scratch work and awards both (sg-25:3). Whether this is a durable change in scoring practice or a question specific decision is not established here. [uncertain]
- Topic 8.2 is stated for rectilinear motion, while the 2023 to 2025 BC free response questions test the same ideas only in the planar setting of Unit 9 (sg-23:8, sg-24:6). The rectilinear scoring pattern recorded for BC-QA-08003 is therefore transported from the planar parts. [single-source]
- Misconception records are tagged inferred unless a scoring guideline names the behaviour directly. No misconception literature is cited, because none could be confirmed from the sources available in this project's cache. [inferred]
- The CED page numbers used in citations are the PDF page index, which for this unit runs 152 to 164 while the printed page numbers run 147 to 159. [verified] (ced:152, ced:164)

<!-- generated:official-evidence:start -->

## Official evidence index [verified]

Generated from data/frq_records.json and data/mcq_records.json. Every record cites its cached document and page; counts are observations over the indexed years only, not predictions. FRQ part records with BC-UNIT-08 as primary or secondary unit: 64. Public sample MCQ records tagged to this unit: 10.

| FRQ record | Role | Calculator | Archetype | Skills (first six) | Points | Point types |
|---|---|---|---|---|---|---|
| BC-FRQ-2013-Q1-B | secondary | calculator | BC-QA-06005 | BC-SKL-06036, BC-SKL-08016, BC-SKL-08017 | 2 | BC-PT-99001, BC-PT-99004 |
| BC-FRQ-2013-Q1-C | primary | calculator | BC-QA-08005 | BC-SKL-08013, BC-SKL-08014, BC-SKL-04012, BC-SKL-05017 | 2 | BC-PT-99005, BC-PT-99010 |
| BC-FRQ-2013-Q1-D | primary | calculator | BC-QA-08006 | BC-SKL-08012, BC-SKL-08014, BC-SKL-05010, BC-SKL-05024, BC-SKL-05025, BC-SKL-05026 | 3 | BC-PT-99013, BC-PT-99004, BC-PT-99011 |
| BC-FRQ-2013-Q3-C | secondary | no_calculator | BC-QA-06007 | BC-SKL-06007, BC-SKL-06009, BC-SKL-08001, BC-SKL-08005, BC-SKL-06038 | 3 | BC-PT-99018, BC-PT-99019, BC-PT-99007 |
| BC-FRQ-2014-Q1-C | primary | calculator | BC-QA-08002 | BC-SKL-08001, BC-SKL-08003, BC-SKL-08021, BC-SKL-08004 | 2 | BC-PT-99020, BC-PT-99004 |
| BC-FRQ-2014-Q4-C | secondary | no_calculator | BC-QA-06002 | BC-SKL-06008, BC-SKL-08009, BC-SKL-08012, BC-SKL-06036 | 3 | BC-PT-99033, BC-PT-99018, BC-PT-99019 |
| BC-FRQ-2014-Q5-A | primary | no_calculator | BC-QA-08008 | BC-SKL-08018, BC-SKL-08019, BC-SKL-08022, BC-SKL-06047, BC-SKL-06048 | 3 | BC-PT-99059, BC-PT-99003, BC-PT-99004 |
| BC-FRQ-2014-Q5-B | primary | no_calculator | BC-QA-08013 | BC-SKL-08048, BC-SKL-08051, BC-SKL-08052, BC-SKL-08054, BC-SKL-08055 | 3 | BC-PT-99058, BC-PT-99001 |
| BC-FRQ-2014-Q5-C | primary | no_calculator | BC-QA-08014 | BC-SKL-08056, BC-SKL-08057, BC-SKL-02036, BC-SKL-03002 | 3 | BC-PT-99022, BC-PT-99051, BC-PT-99004 |
| BC-FRQ-2015-Q1-A | secondary | calculator | BC-QA-06005 | BC-SKL-06036, BC-SKL-08016, BC-SKL-08017 | 2 | BC-PT-99002, BC-PT-99004 |
| BC-FRQ-2015-Q1-B | primary | calculator | BC-QA-08005 | BC-SKL-08013, BC-SKL-08014, BC-SKL-04012, BC-SKL-05017 | 2 | BC-PT-99014, BC-PT-99010 |
| BC-FRQ-2015-Q1-C | primary | calculator | BC-QA-08006 | BC-SKL-08012, BC-SKL-08014, BC-SKL-05010, BC-SKL-05024, BC-SKL-05025, BC-SKL-05026 | 3 | BC-PT-99013, BC-PT-99004, BC-PT-99011 |
| BC-FRQ-2015-Q1-D | primary | calculator | BC-QA-06006 | BC-SKL-08012, BC-SKL-08013, BC-SKL-08016, BC-SKL-06039, BC-SKL-06017 | 2 | BC-PT-99001, BC-PT-99068 |
| BC-FRQ-2015-Q3-B | secondary | no_calculator | BC-QA-06001 | BC-SKL-06006, BC-SKL-06009, BC-SKL-08015, BC-SKL-08007, BC-SKL-08006 | 3 | BC-PT-99007, BC-PT-99018, BC-PT-99019 |
| BC-FRQ-2015-Q3-D | primary | no_calculator | BC-QA-08001 | BC-SKL-08001, BC-SKL-06034, BC-SKL-06040 | 3 | BC-PT-99020, BC-PT-99003, BC-PT-99004 |
| BC-FRQ-2018-Q1-A | secondary | calculator | BC-QA-06005 | BC-SKL-06036, BC-SKL-08016, BC-SKL-08017 | 0 |  |
| BC-FRQ-2018-Q1-B | primary | calculator | BC-QA-06006 | BC-SKL-08012, BC-SKL-08013, BC-SKL-06039, BC-SKL-06037 | 0 |  |
| BC-FRQ-2018-Q1-C | primary | calculator | BC-QA-08004 | BC-SKL-08012, BC-SKL-08009, BC-SKL-08017 | 0 |  |
| BC-FRQ-2018-Q1-D | primary | calculator | BC-QA-08006 | BC-SKL-08012, BC-SKL-08014, BC-SKL-05010, BC-SKL-05024, BC-SKL-05025, BC-SKL-05026 | 0 |  |
| BC-FRQ-2018-Q2-B | secondary | calculator | BC-QA-06005 | BC-SKL-06036, BC-SKL-08016, BC-SKL-08017 | 0 |  |
| BC-FRQ-2018-Q2-C | secondary | calculator | BC-QA-06013 | BC-SKL-06031, BC-SKL-06029, BC-SKL-06066, BC-SKL-06067, BC-SKL-08016 | 0 |  |
| BC-FRQ-2018-Q4-C | secondary | no_calculator | BC-QA-06002 | BC-SKL-06008, BC-SKL-08001, BC-SKL-08005 | 0 |  |
| BC-FRQ-2019-Q1-A | primary | calculator | BC-QA-06005 | BC-SKL-08016, BC-SKL-08017, BC-SKL-06036, BC-SKL-08003 | 2 | BC-PT-99001, BC-PT-99004 |
| BC-FRQ-2019-Q1-B | primary | calculator | BC-QA-08001 | BC-SKL-08001, BC-SKL-08003, BC-SKL-08004, BC-SKL-08005 | 2 | BC-PT-99001, BC-PT-99004 |
| BC-FRQ-2019-Q1-C | primary | calculator | BC-QA-08006 | BC-SKL-08013, BC-SKL-08014, BC-SKL-05029, BC-SKL-06026, BC-SKL-05024 | 3 | BC-PT-99013, BC-PT-99004, BC-PT-99010 |
| BC-FRQ-2019-Q2-B | primary | calculator | BC-QA-08001 | BC-SKL-08001, BC-SKL-08003, BC-SKL-09029 | 2 | BC-PT-99020, BC-PT-99004 |
| BC-FRQ-2021-Q1-B | secondary | calculator | BC-QA-06001 | BC-SKL-06006, BC-SKL-06009, BC-SKL-06013 | 2 | BC-PT-99018, BC-PT-99019 |
| BC-FRQ-2021-Q1-D | primary | calculator | BC-QA-08001 | BC-SKL-08001, BC-SKL-08003, BC-SKL-08004 | 3 | BC-PT-99001, BC-PT-99020, BC-PT-99004 |
| BC-FRQ-2021-Q2-B | secondary | calculator | BC-QA-09007 | BC-SKL-09025, BC-SKL-09011, BC-SKL-09013, BC-SKL-09012 | 2 | BC-PT-99051, BC-PT-99004 |
| BC-FRQ-2021-Q2-C | secondary | calculator | BC-QA-09005 | BC-SKL-09021, BC-SKL-09026, BC-SKL-09019, BC-SKL-05020, BC-SKL-05029 | 5 | BC-PT-99013, BC-PT-99010, BC-PT-99033, BC-PT-99004, BC-PT-99005 |
| BC-FRQ-2021-Q3-A | secondary | no_calculator | BC-QA-06008 | BC-SKL-06047, BC-SKL-06048, BC-SKL-06050, BC-SKL-08019, BC-SKL-08020 | 3 | BC-PT-99002, BC-PT-99003, BC-PT-99004 |
| BC-FRQ-2021-Q3-B | secondary | no_calculator | BC-QA-05007 | BC-SKL-05010, BC-SKL-05019, BC-SKL-05023, BC-SKL-08040 | 2 | BC-PT-99013, BC-PT-99005 |
| BC-FRQ-2021-Q3-C | primary | no_calculator | BC-QA-08012 | BC-SKL-08040, BC-SKL-08041, BC-SKL-08043, BC-SKL-06034, BC-SKL-06055 | 4 | BC-PT-99058, BC-PT-99001, BC-PT-99003, BC-PT-99004 |
| BC-FRQ-2022-Q1-A | primary | calculator | BC-QA-08007 | BC-SKL-08016, BC-SKL-06036, BC-SKL-08015 | 1 | BC-PT-99001 |
| BC-FRQ-2022-Q1-B | primary | calculator | BC-QA-08001 | BC-SKL-08001, BC-SKL-08003, BC-SKL-08005 | 2 | BC-PT-99020, BC-PT-99004 |
| BC-FRQ-2022-Q1-D | primary | calculator | BC-QA-08006 | BC-SKL-08013, BC-SKL-08014, BC-SKL-06018, BC-SKL-05024, BC-SKL-05026, BC-SKL-05028 | 4 | BC-PT-99013, BC-PT-99064, BC-PT-99004, BC-PT-99011 |
| BC-FRQ-2022-Q2-C | secondary | calculator | BC-QA-09005 | BC-SKL-09021, BC-SKL-09026, BC-SKL-08012, BC-SKL-06037 | 3 | BC-PT-99002, BC-PT-99033, BC-PT-99004 |
| BC-FRQ-2022-Q2-D | secondary | calculator | BC-QA-09007 | BC-SKL-09025, BC-SKL-09011, BC-SKL-09013, BC-SKL-09012 | 2 | BC-PT-99051, BC-PT-99004 |
| BC-FRQ-2022-Q3-A | secondary | no_calculator | BC-QA-06005 | BC-SKL-06028, BC-SKL-06034, BC-SKL-06037, BC-SKL-06004, BC-SKL-06030 | 3 | BC-PT-99069, BC-PT-99004, BC-PT-99004 |
| BC-FRQ-2022-Q4-C | secondary | no_calculator | BC-QA-06001 | BC-SKL-06006, BC-SKL-06009, BC-SKL-06013 | 2 | BC-PT-99018, BC-PT-99019 |
| BC-FRQ-2022-Q5-A | primary | no_calculator | BC-QA-08008 | BC-SKL-08019, BC-SKL-08022, BC-SKL-06041, BC-SKL-06034 | 2 | BC-PT-99001, BC-PT-99004 |
| BC-FRQ-2022-Q5-B | primary | no_calculator | BC-QA-08011 | BC-SKL-08033, BC-SKL-08035, BC-SKL-06057, BC-SKL-06058, BC-SKL-06060 | 4 | BC-PT-99001, BC-PT-99056, BC-PT-99057, BC-PT-99004 |
| BC-FRQ-2022-Q5-C | primary | no_calculator | BC-QA-08012 | BC-SKL-08041, BC-SKL-08043, BC-SKL-06066, BC-SKL-06067, BC-SKL-06068 | 3 | BC-PT-99053, BC-PT-99003, BC-PT-99004 |
| BC-FRQ-2023-Q1-A | secondary | calculator | BC-QA-06001 | BC-SKL-06006, BC-SKL-06002, BC-SKL-08015 | 3 | BC-PT-99007, BC-PT-99018, BC-PT-99019 |
| BC-FRQ-2023-Q1-C | primary | calculator | BC-QA-06007 | BC-SKL-08001, BC-SKL-08003, BC-SKL-06038, BC-SKL-08004 | 2 | BC-PT-99020, BC-PT-99004 |
| BC-FRQ-2023-Q2-C | secondary | calculator | BC-QA-09001 | BC-SKL-09002, BC-SKL-09004, BC-SKL-09021, BC-SKL-09026, BC-SKL-06037 | 3 | BC-PT-99049, BC-PT-99001, BC-PT-99004 |
| BC-FRQ-2023-Q2-D | secondary | calculator | BC-QA-09007 | BC-SKL-09025, BC-SKL-09011, BC-SKL-09013, BC-SKL-08007 | 2 | BC-PT-99051, BC-PT-99004 |
| BC-FRQ-2023-Q5-A | primary | no_calculator | BC-QA-08008 | BC-SKL-08018, BC-SKL-08019, BC-SKL-06029, BC-SKL-06052, BC-SKL-06034 | 3 | BC-PT-99059, BC-PT-99003, BC-PT-99004 |
| BC-FRQ-2024-Q1-B | secondary | calculator | BC-QA-06001 | BC-SKL-06005, BC-SKL-08005, BC-SKL-08004, BC-SKL-06038 | 3 | BC-PT-99018, BC-PT-99019, BC-PT-99007 |
| BC-FRQ-2024-Q1-C | primary | calculator | BC-QA-06005 | BC-SKL-06036, BC-SKL-06037, BC-SKL-08012, BC-SKL-08017, BC-SKL-06046 | 3 | BC-PT-99001, BC-PT-99033, BC-PT-99004 |
| BC-FRQ-2024-Q2-B | secondary | calculator | BC-QA-09007 | BC-SKL-09025, BC-SKL-09011, BC-SKL-09013, BC-SKL-08007 | 2 | BC-PT-99051, BC-PT-99004 |
| BC-FRQ-2024-Q2-C | secondary | calculator | BC-QA-09005 | BC-SKL-09021, BC-SKL-09022, BC-SKL-09026, BC-SKL-06037, BC-SKL-08012 | 3 | BC-PT-99001, BC-PT-99033, BC-PT-99004 |
| BC-FRQ-2024-Q4-A | secondary | no_calculator | BC-QA-06004 | BC-SKL-06020, BC-SKL-06028, BC-SKL-06030, BC-SKL-06031, BC-SKL-06004 | 3 | BC-PT-99069, BC-PT-99069, BC-PT-99069 |
| BC-FRQ-2024-Q5-B | primary | no_calculator | BC-QA-08014 | BC-SKL-08058, BC-SKL-08056, BC-SKL-09014 | 2 | BC-PT-99009, BC-PT-99009 |
| BC-FRQ-2025-Q1-A | primary | calculator | BC-QA-06007 | BC-SKL-08001, BC-SKL-08003, BC-SKL-06038, BC-SKL-08004, BC-SKL-08005 | 2 | BC-PT-99020, BC-PT-99004 |
| BC-FRQ-2025-Q2-B | secondary | calculator | BC-QA-09013 | BC-SKL-09039, BC-SKL-09040, BC-SKL-09041, BC-SKL-09042, BC-SKL-09036 | 3 | BC-PT-99048, BC-PT-99002, BC-PT-99004 |
| BC-FRQ-2025-Q3-C | secondary | no_calculator | BC-QA-06002 | BC-SKL-06008, BC-SKL-06009, BC-SKL-06005, BC-SKL-06006 | 2 | BC-PT-99018, BC-PT-99019 |
| BC-FRQ-2025-Q3-D | primary | no_calculator | BC-QA-06005 | BC-SKL-06036, BC-SKL-06040, BC-SKL-06034, BC-SKL-08016, BC-SKL-08017 | 3 | BC-PT-99002, BC-PT-99003, BC-PT-99004 |
| BC-FRQ-2026-Q1-B | secondary | calculator | BC-QA-06001 | BC-SKL-06007, BC-SKL-06009, BC-SKL-08015, BC-SKL-06002 | 3 | BC-PT-99018, BC-PT-99019, BC-PT-99007 |
| BC-FRQ-2026-Q1-C | primary | calculator | BC-QA-06005 | BC-SKL-06036, BC-SKL-08016, BC-SKL-08017, BC-SKL-06046 | 2 | BC-PT-99001, BC-PT-99004 |
| BC-FRQ-2026-Q2-A | secondary | calculator | BC-QA-09012 | BC-SKL-09035, BC-SKL-09036, BC-SKL-09038 | 2 | BC-PT-99048, BC-PT-99004 |
| BC-FRQ-2026-Q2-D | primary | calculator | BC-QA-06007 | BC-SKL-08001, BC-SKL-08003, BC-SKL-06038, BC-SKL-09031 | 2 | BC-PT-99020, BC-PT-99004 |
| BC-FRQ-2026-Q5-B | primary | no_calculator | BC-QA-08012 | BC-SKL-08040, BC-SKL-08041, BC-SKL-08034, BC-SKL-06046 | 2 | BC-PT-99058, BC-PT-99001 |
| BC-FRQ-2026-Q5-C | primary | no_calculator | BC-QA-08014 | BC-SKL-08056, BC-SKL-08057, BC-SKL-08004, BC-SKL-02026 | 2 | BC-PT-99051, BC-PT-99001 |

| MCQ record | Calculator | Archetype | Skills |
|---|---|---|---|
| BC-MCQ-CED-010 | no_calculator | BC-QA-08009 | BC-SKL-08023, BC-SKL-08024, BC-SKL-08025 |
| BC-MCQ-CED-015 | calculator | BC-QA-08004 | BC-SKL-08016, BC-SKL-08017, BC-SKL-06034 |
| BC-MCQ-SAMPLE-009 | no_calculator | BC-QA-08001 | BC-SKL-08002, BC-SKL-06028, BC-SKL-08001 |
| BC-MCQ-SAMPLE-015 | calculator | BC-QA-08004 | BC-SKL-08012, BC-SKL-06037, BC-SKL-06034 |
| BC-MCQ-SAMPLE-016 | calculator | BC-QA-08003 | BC-SKL-08010, BC-SKL-08006, BC-SKL-06040 |
| BC-MCQ-PE2012-004 | no_calculator | BC-QA-08014 | BC-SKL-08056, BC-SKL-08057, BC-SKL-02034 |
| BC-MCQ-PE2012-008 | no_calculator | BC-QA-06001 | BC-SKL-06006, BC-SKL-08012, BC-SKL-06005 |
| BC-MCQ-PE2012-035 | calculator | BC-QA-08001 | BC-SKL-08001, BC-SKL-08003, BC-SKL-08004 |
| BC-MCQ-PE2012-040 | calculator | BC-QA-08011 | BC-SKL-08032, BC-SKL-08031, BC-SKL-08035 |
| BC-MCQ-PE2012-042 | calculator | BC-QA-08003 | BC-SKL-08010, BC-SKL-06037, BC-SKL-08003 |

<!-- generated:official-evidence:end -->
