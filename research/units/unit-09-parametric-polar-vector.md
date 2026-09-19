---
title: Unit 9, Parametric Equations, Polar Coordinates, and Vector-Valued Functions
research_date: 2026-09-19
status: draft
purpose: Decompose CED Unit 9 into concepts, atomic skills, non-calculus prerequisites, question archetypes and variants, observed errors, candidate misconceptions, and diagnostic signals, each grounded in the CED text and in the 2023 to 2025 official free-response questions and scoring guidelines.
---

# Unit 9, Parametric Equations, Polar Coordinates, and Vector-Valued Functions

BC-UNIT-09 covers CED pages 166 to 179 and holds nine topics. Every topic and every learning objective in the unit carries the BC only marker in the CED and in data/curriculum.json, so every record in this file has scope BC_only. The unit re-expresses the derivative and the definite integral in three new representations: parametric equations, vector-valued functions, and polar equations. Unit weighting is in [../exam/exam-blueprint.md](../exam/exam-blueprint.md) and exam composition is in [../exam/exam-structure.md](../exam/exam-structure.md). [verified] (ced:171, ced:179)

## 9.1 Defining and Differentiating Parametric Equations

### Official mapping

Topic id BC-TOP-0901, CED code 9.1, name Defining and Differentiating Parametric Equations, scope BC_only, CED page 171. [verified] (ced:171)

- BC-LO-CHA-3G (CHA-3.G): Calculate derivatives of parametric functions.
  - BC-EK-CHA-3G1 (CHA-3.G.1): "Methods for calculating derivatives of real-valued functions can be extended to parametric functions."
  - BC-EK-CHA-3G2 (CHA-3.G.2): "For a curve defined parametrically, the value of dy/dx at a point on the curve is the slope of the line tangent to the curve at that point. dy/dx, the slope of the line tangent to a curve defined using parametric equations, can be determined by dividing dy/dt by dx/dt, provided dx/dt does not equal zero."

Suggested practice skills: BC-MPS-2D (Practice skill 2.D). Weighting pointer: [../exam/exam-blueprint.md](../exam/exam-blueprint.md).

### Concept breakdown

- BC-CON-09001 Curve defined by parametric equations: Two functions of a parameter give the two coordinates of a moving point.
- BC-CON-09002 Slope of a parametric curve as a quotient of derivatives: The slope of the tangent is the rate of y divided by the rate of x.

- BC-SKL-09001 Differentiate each component of a parametric curve with respect to the parameter: Find dx/dt and dy/dt separately.
- BC-SKL-09002 Compute dy/dx for a parametric curve as a quotient of derivatives: Divide dy/dt by dx/dt to get the slope.
- BC-SKL-09003 State the condition that dx/dt is not zero: Say that the slope formula needs a nonzero rate in x.
- BC-SKL-09004 Evaluate the slope of the tangent at a parameter value: Put the parameter value into the slope quotient.
- BC-SKL-09005 Write the equation of the tangent line at a point on a parametric curve: Use the point and the slope to write the line.
- BC-SKL-09006 Locate parameter values where the tangent is horizontal or vertical: Horizontal where dy/dt is zero, vertical where dx/dt is zero.

### Prerequisites

- BC-PRQ-06005 -> BC-SKL-09001, supporting, [inferred], Prerequisite for Differentiate each component of a parametric curve with respect to the parameter.
- BC-PRQ-06005 -> BC-SKL-09002, supporting, [inferred], Prerequisite for Compute dy/dx for a parametric curve as a quotient of derivatives.
- BC-PRQ-06005 -> BC-SKL-09003, supporting, [inferred], Prerequisite for State the condition that dx/dt is not zero.
- BC-PRQ-08006 -> BC-SKL-09004, supporting, [inferred], Prerequisite for Evaluate the slope of the tangent at a parameter value.
- BC-PRQ-06005 -> BC-SKL-09005, supporting, [inferred], Prerequisite for Write the equation of the tangent line at a point on a parametric curve.
- BC-PRQ-08001 -> BC-SKL-09006, supporting, [inferred], Prerequisite for Locate parameter values where the tangent is horizontal or vertical.

### Required mathematical knowledge

**Parametric derivative.** Methods for calculating derivatives of real valued functions extend to parametric functions (BC-EK-CHA-3G1). Hypotheses: x and y differentiable at the parameter value, with dx/dt not zero there. Conclusion: dy/dx equals dy/dt divided by dx/dt, and its value is the slope of the line tangent to the curve at that point (BC-EK-CHA-3G2).

**Horizontal and vertical tangents.** The tangent is horizontal where dy/dt is zero and dx/dt is not, and vertical where dx/dt is zero and dy/dt is not.

**Communication.** The 2023 guideline required the response to show the quotient structure, not only its value; several presentations earned the point provided the quotient of the two parametric derivatives was visible (sg-23:7).

**Notation.** The parameter is not a coordinate, so dy/dx and dy/dt are different objects and the response must say which is being reported.

### Representations

Representations in play: BC-REP-12 Parametric equations, BC-REP-01 Symbolic, BC-REP-02 Graphical, BC-REP-09 Calculator-generated numerical result.

Conversions tested: parametric pair to a slope in the plane (BC-REP-12 to BC-REP-01), and a plotted path to a statement about the tangent (BC-REP-02 to BC-REP-04).

### Assessment behaviour

MCQ forms give a parametric pair and ask for dy/dx at a parameter value, with the reciprocal quotient and dy/dt alone as distractors. FRQ forms ask for the slope of the line tangent to the path at a time and require the quotient to be communicated; the point is earned by any presentation that shows dy/dt divided by dx/dt (sg-23:7). Calculator variants supply a derivative that cannot be antidifferentiated in closed form; no-calculator variants use elementary components. Conceptual variants ask where the tangent is vertical; computational variants ask for the slope; interpretation variants ask what the slope says about the path; justification variants ask why the quotient needs dx/dt nonzero. Multi-concept variants pair the slope with a coordinate recovered from an initial condition in the same part (sg-23:7).

### Archetypes

- BC-QA-09001 Slope of the tangent to a parametric path at a time

### Errors and misconceptions

- BC-ERR-09001 Component derivative computed incorrectly
- BC-ERR-09002 Slope written as dx/dt divided by dy/dt
- BC-ERR-09003 Rate of the vertical component reported as the slope
- BC-ERR-09004 Slope value presented without the quotient
- BC-ERR-09005 Condition that dx/dt is not zero omitted
- BC-ERR-09006 Intermediate value rounded before a later step
- BC-ERR-09007 Tangent line written through the velocity components rather than the position
- BC-ERR-09008 Horizontal and vertical tangent conditions exchanged
- BC-MIS-09001 The parameter is the horizontal coordinate, severity high
- BC-MIS-09002 The slope of a parametric path is the rate of the vertical component, severity high
- BC-MIS-09003 The order of the parametric quotient does not matter, severity medium

### Diagnostic signals

- BC-SIG-09001 Correct slope value with no quotient shown

### Adaptive metadata summary

Skills in this topic carry calculator relevance none, optional, typically_required. Remediation targets named across the topic: con.param_curve, con.param_slope. Every skill record carries the full seven key adaptive block in data/staging/unit-09.skills.json. [inferred]

## 9.2 Second Derivatives of Parametric Equations

### Official mapping

Topic id BC-TOP-0902, CED code 9.2, name Second Derivatives of Parametric Equations, scope BC_only, CED page 172. [verified] (ced:172)

- BC-LO-CHA-3G (CHA-3.G): Calculate derivatives of parametric functions.
  - BC-EK-CHA-3G3 (CHA-3.G.3): "d^2y/dx^2 can be calculated by dividing d/dt of (dy/dx) by dx/dt."

Suggested practice skills: BC-MPS-1E (Practice skill 1.E). Weighting pointer: [../exam/exam-blueprint.md](../exam/exam-blueprint.md).

### Concept breakdown

- BC-CON-09003 Second derivative of a parametric curve: Differentiate the slope with respect to the parameter, then divide by dx/dt again.

- BC-SKL-09007 Differentiate dy/dx with respect to the parameter: Treat the slope as a function of the parameter and differentiate it.
- BC-SKL-09008 Assemble the second derivative by dividing again by dx/dt: Divide the derivative of the slope by dx/dt.
- BC-SKL-09009 Evaluate the second derivative at a parameter value: Substitute the parameter value into the assembled expression.
- BC-SKL-09010 Determine the concavity of a parametric curve from the sign of the second derivative: Positive means concave up as a curve in the plane.

### Prerequisites

- BC-PRQ-06005 -> BC-SKL-09007, supporting, [inferred], Prerequisite for Differentiate dy/dx with respect to the parameter.
- BC-PRQ-06005 -> BC-SKL-09008, supporting, [inferred], Prerequisite for Assemble the second derivative by dividing again by dx/dt.
- BC-PRQ-08006 -> BC-SKL-09009, supporting, [inferred], Prerequisite for Evaluate the second derivative at a parameter value.
- BC-PRQ-06005 -> BC-SKL-09010, supporting, [inferred], Prerequisite for Determine the concavity of a parametric curve from the sign of the second derivative.

### Required mathematical knowledge

**Second derivative.** The second derivative of y with respect to x can be calculated by dividing the derivative with respect to the parameter of dy/dx by dx/dt (BC-EK-CHA-3G3).

**Order of operations.** The slope must be assembled first, then differentiated with respect to the parameter, then divided by dx/dt. The quotient of the two second derivatives with respect to the parameter is a different expression and is not the second derivative of y with respect to x.

**Concavity.** The sign of the second derivative of y with respect to x describes the bending of the curve in the plane, not the bending of either component against the parameter.

**Notation.** The response must distinguish the derivative with respect to the parameter from the derivative with respect to x at every step.

### Representations

Representations in play: BC-REP-12 Parametric equations, BC-REP-01 Symbolic, BC-REP-09 Calculator-generated numerical result.

Conversions tested: a parametric pair to a second derivative expression (BC-REP-12 to BC-REP-01), and the sign of that expression to a verbal statement about concavity (BC-REP-01 to BC-REP-04).

### Assessment behaviour

MCQ forms offer the quotient of the two second parametric derivatives as the distractor. FRQ forms ask for the second derivative at a parameter value with the setup shown. Calculator variants evaluate numerically; no-calculator variants keep the expression symbolic. Conceptual variants ask which quantity must be differentiated first; computational variants ask for the value; interpretation variants ask about concavity; justification variants ask why a second division by dx/dt appears. Multi-concept variants follow a slope part in the same question. No 2023 to 2025 BC free response part asked for a parametric second derivative, so the scoring pattern is inferred from the slope scoring at sg-23:7.

### Archetypes

- BC-QA-09002 Second derivative of a parametric curve

### Errors and misconceptions

- BC-ERR-09009 Second derivative taken as a quotient of second derivatives
- BC-ERR-09010 Second division by dx/dt omitted
- BC-ERR-09006 Intermediate value rounded before a later step
- BC-ERR-09011 Numerical answer presented with no setup
- BC-ERR-09012 Concavity read from the sign of a component derivative
- BC-MIS-09004 The second derivative follows the same pattern as the first, severity high

### Diagnostic signals

- BC-SIG-09002 Second derivative assembled from two second derivatives

### Adaptive metadata summary

Skills in this topic carry calculator relevance none, optional, typically_required. Remediation targets named across the topic: con.param_second. Every skill record carries the full seven key adaptive block in data/staging/unit-09.skills.json. [inferred]

## 9.3 Finding Arc Lengths of Curves Given by Parametric Equations

### Official mapping

Topic id BC-TOP-0903, CED code 9.3, name Finding Arc Lengths of Curves Given by Parametric Equations, scope BC_only, CED page 173. [verified] (ced:173)

- BC-LO-CHA-6B (CHA-6.B): Determine the length of a curve in the plane defined by parametric functions, using a definite integral.
  - BC-EK-CHA-6B1 (CHA-6.B.1): "The length of a parametrically defined curve can be calculated using a definite integral."

Suggested practice skills: BC-MPS-1D (Practice skill 1.D). Weighting pointer: [../exam/exam-blueprint.md](../exam/exam-blueprint.md).

### Concept breakdown

- BC-CON-09004 Arc length of a parametric curve: The length is the integral of the magnitude of the pair of rates.

- BC-SKL-09011 Set up the arc length integral for a parametric curve: Integrate the square root of the sum of the squares of the two rates.
- BC-SKL-09012 Evaluate a parametric arc length integral with technology: Enter the radical integrand and report the decimal.
- BC-SKL-09013 Identify the parametric arc length integral as the distance travelled: The same integral measures the length of the path a particle traces.
- BC-SKL-09014 Identify the parameter interval over which a length is measured: Say which parameter values bound the piece being measured.

### Prerequisites

- BC-PRQ-08007 -> BC-SKL-09011, supporting, [inferred], Prerequisite for Set up the arc length integral for a parametric curve.
- BC-PRQ-08006 -> BC-SKL-09012, supporting, [inferred], Prerequisite for Evaluate a parametric arc length integral with technology.
- BC-PRQ-06005 -> BC-SKL-09013, supporting, [inferred], Prerequisite for Identify the parametric arc length integral as the distance travelled.
- BC-PRQ-09004 -> BC-SKL-09014, supporting, [inferred], Prerequisite for Identify the parameter interval over which a length is measured.
- BC-SKL-08056 -> BC-SKL-09011, hard_prerequisite, [verified], The arc length integral for a function is the single variable form of the parametric length integral.
- BC-SKL-08059 -> BC-SKL-09012, hard_prerequisite, [verified], Evaluating a radical length integral with technology is the Unit 8 skill applied to a parametric integrand.

### Required mathematical knowledge

**Parametric arc length.** The length of a parametrically defined curve can be calculated using a definite integral (BC-EK-CHA-6B1). Hypotheses: x and y have continuous derivatives on the parameter interval. Conclusion: the length is the definite integral of the square root of the sum of the squares of dx/dt and dy/dt.

**Length and distance.** For a particle in planar motion the same integral is the total distance travelled, because the integrand is the speed (BC-EK-FUN-8B2). The 2024 guideline scored exactly this integral as the setup point for total distance (sg-24:6).

**Tracing.** A parameter interval that traces part of the curve twice gives a length larger than the length of the curve.

**Notation.** Each component derivative is parenthesised before being squared; the 2023 guideline treated a missing parenthesis in a squared component as an error that cost the setup point while leaving the answer point available (sg-23:6).

### Representations

Representations in play: BC-REP-12 Parametric equations, BC-REP-01 Symbolic, BC-REP-09 Calculator-generated numerical result.

Conversions tested: parametric components to a radical integrand (BC-REP-12 to BC-REP-01), and an integral expression to a statement of distance travelled (BC-REP-01 to BC-REP-04).

### Assessment behaviour

MCQ forms ask which integral gives the length of a parametric curve, with the sum of the two component integrals as the distractor. FRQ forms ask for the total distance travelled by a particle over a time interval, scoring the integral and the value separately (sg-24:6). Calculator variants require numerical evaluation; no-calculator variants ask only for the setup. Conceptual variants ask what the integrand measures; computational variants ask for the number; interpretation variants ask for the meaning with units; justification variants ask why the speed appears inside the integral. Multi-concept variants place the length next to a speed part that supplies the same integrand (sg-23:6, sg-23:8).

### Archetypes

- BC-QA-09003 Length of a parametric curve
- BC-QA-09007 Total distance travelled by a particle in the plane

### Errors and misconceptions

- BC-ERR-09013 Component rates added instead of combined as a magnitude
- BC-ERR-09014 Parentheses lost inside a squared component
- BC-ERR-09006 Intermediate value rounded before a later step
- BC-ERR-09011 Numerical answer presented with no setup
- BC-ERR-09015 Magnitude of the displacement reported as the distance travelled
- BC-ERR-09016 Integration over an interval that traces the curve more than once
- BC-MIS-09005 A length in the plane is the sum of the two component contributions, severity high
- BC-MIS-09008 A calculator result stands without its expression, severity medium
- BC-MIS-09006 Distance travelled in the plane is the size of the net change in position, severity high
- BC-MIS-09007 Any interval containing the curve gives its length or area, severity medium

### Diagnostic signals

- BC-SIG-09003 Component rates added inside a speed or length
- BC-SIG-09004 Magnitude of displacement reported as distance travelled

### Adaptive metadata summary

Skills in this topic carry calculator relevance none, optional, typically_required. Remediation targets named across the topic: BC-PRQ-09004, con.param_arc_length. Every skill record carries the full seven key adaptive block in data/staging/unit-09.skills.json. [inferred]

## 9.4 Defining and Differentiating Vector-Valued Functions

### Official mapping

Topic id BC-TOP-0904, CED code 9.4, name Defining and Differentiating Vector-Valued Functions, scope BC_only, CED page 174. [verified] (ced:174)

- BC-LO-CHA-3H (CHA-3.H): Calculate derivatives of vector-valued functions.
  - BC-EK-CHA-3H1 (CHA-3.H.1): "Methods for calculating derivatives of real-valued functions can be extended to vector-valued functions."

Suggested practice skills: BC-MPS-1D (Practice skill 1.D). Weighting pointer: [../exam/exam-blueprint.md](../exam/exam-blueprint.md).

### Concept breakdown

- BC-CON-09005 Vector-valued function as a pair of component functions: A vector function is just two ordinary functions written together.
- BC-CON-09006 Derivative of a vector-valued function taken component by component: Differentiate each component separately.

- BC-SKL-09015 Differentiate a vector-valued function component by component: Differentiate each coordinate on its own.
- BC-SKL-09016 Evaluate the velocity vector at a given time: Report both components of the derivative of position at that time.
- BC-SKL-09017 Evaluate the acceleration vector as the derivative of velocity: Differentiate each velocity component again and evaluate.
- BC-SKL-09018 Convert between parametric equations and vector-valued notation: The same motion can be written as a pair of equations or as one vector.

### Prerequisites

- BC-PRQ-09001 -> BC-SKL-09015, supporting, [inferred], Prerequisite for Differentiate a vector-valued function component by component.
- BC-PRQ-09001 -> BC-SKL-09016, supporting, [inferred], Prerequisite for Evaluate the velocity vector at a given time.
- BC-PRQ-09001 -> BC-SKL-09017, supporting, [inferred], Prerequisite for Evaluate the acceleration vector as the derivative of velocity.
- BC-PRQ-09001 -> BC-SKL-09018, supporting, [inferred], Prerequisite for Convert between parametric equations and vector-valued notation.

### Required mathematical knowledge

**Vector derivative.** Methods for calculating derivatives of real valued functions extend to vector-valued functions (BC-EK-CHA-3H1), which means differentiating each component separately.

**Motion vectors.** The derivative of the position vector is the velocity vector and the derivative of the velocity vector is the acceleration vector.

**Presentation.** The 2023 guideline accepted the acceleration vector in several notations, including a listing of the two components, provided they were labelled; an unsupported correct vector earned one of the two available points (sg-23:6).

**Notation.** Ordered pair, angle bracket, and bracket notation are all acceptable, and the two components must be identifiable.

### Representations

Representations in play: BC-REP-14 Vector-valued function, BC-REP-12 Parametric equations, BC-REP-01 Symbolic, BC-REP-09 Calculator-generated numerical result.

Conversions tested: parametric pair to vector-valued function (BC-REP-12 to BC-REP-14), and a vector expression to a pair of numerical components (BC-REP-14 to BC-REP-09).

### Assessment behaviour

MCQ forms ask for a velocity or acceleration vector at a time. FRQ forms open the calculator active BC question with an acceleration vector, scoring one point for each component with its setup (sg-23:5). Calculator variants evaluate the components numerically; no-calculator variants keep them symbolic. Conceptual variants ask what the derivative of a vector-valued function means; computational variants ask for the components; interpretation variants ask what the acceleration says about the motion; justification variants are uncommon at this topic. Multi-concept variants continue into speed and distance parts in the same question (frq-23:4).

### Archetypes

- BC-QA-09004 Acceleration vector of a particle in planar motion
- BC-QA-09005 Coordinate of a particle recovered from an initial position

### Errors and misconceptions

- BC-ERR-09017 Vector components presented without labels or in the wrong order
- BC-ERR-09006 Intermediate value rounded before a later step
- BC-ERR-09011 Numerical answer presented with no setup
- BC-ERR-09018 Variable expression equated to a numerical value
- BC-MIS-09009 A vector answer is a pair of numbers with no structure, severity medium

### Diagnostic signals

- BC-SIG-09005 Correct vector with no supporting work

### Adaptive metadata summary

Skills in this topic carry calculator relevance none, optional, typically_required. Remediation targets named across the topic: BC-PRQ-09001. Every skill record carries the full seven key adaptive block in data/staging/unit-09.skills.json. [inferred]

## 9.5 Integrating Vector-Valued Functions

### Official mapping

Topic id BC-TOP-0905, CED code 9.5, name Integrating Vector-Valued Functions, scope BC_only, CED page 175. [verified] (ced:175)

- BC-LO-FUN-8A (FUN-8.A): Determine a particular solution given a rate vector and initial conditions.
  - BC-EK-FUN-8A1 (FUN-8.A.1): "Methods for calculating integrals of real-valued functions can be extended to parametric or vector-valued functions."

Suggested practice skills: BC-MPS-1E (Practice skill 1.E). Weighting pointer: [../exam/exam-blueprint.md](../exam/exam-blueprint.md).

### Concept breakdown

- BC-CON-09007 Integral of a vector-valued function taken component by component: Integrate each component separately to get a vector.
- BC-CON-09008 Particular position from a rate vector and an initial position: Each coordinate is its starting value plus the accumulated change.

- BC-SKL-09019 Antidifferentiate a vector-valued function component by component: Find an antiderivative of each component.
- BC-SKL-09020 Write the displacement as a definite integral of the velocity vector: Integrate each velocity component over the interval.
- BC-SKL-09021 Determine a coordinate of position from an initial position and a velocity component: Add the integral of that velocity component to the starting coordinate.
- BC-SKL-09022 Accumulate backwards in time from a known later position: Going back in time reverses the order of the limits.

### Prerequisites

- BC-PRQ-09001 -> BC-SKL-09019, supporting, [inferred], Prerequisite for Antidifferentiate a vector-valued function component by component.
- BC-PRQ-06005 -> BC-SKL-09020, supporting, [inferred], Prerequisite for Write the displacement as a definite integral of the velocity vector.
- BC-PRQ-06005 -> BC-SKL-09021, supporting, [inferred], Prerequisite for Determine a coordinate of position from an initial position and a velocity component.
- BC-PRQ-06005 -> BC-SKL-09022, supporting, [inferred], Prerequisite for Accumulate backwards in time from a known later position.
- BC-SKL-08006 -> BC-SKL-09020, hard_prerequisite, [verified], Displacement as the integral of velocity is the rectilinear skill applied componentwise.
- BC-SKL-06037 -> BC-SKL-09021, hard_prerequisite, [verified], Computing a final value from an initial condition and an accumulated change is the Unit 6 form of this skill.

### Required mathematical knowledge

**Vector integration.** Methods for calculating integrals of real valued functions extend to parametric or vector-valued functions (BC-EK-FUN-8A1), which means integrating each component separately.

**Particular solution.** Hypotheses: the velocity components are integrable on the interval and the position is known at one time. Conclusion: each coordinate at another time is its known value plus the definite integral of the corresponding velocity component between the two times.

**Direction of accumulation.** When the known position is later than the requested one, the integral is subtracted or its limits are reversed; the 2024 guideline listed both presentations as acceptable (sg-24:7).

**Notation.** Each component carries its own constant of integration.

### Representations

Representations in play: BC-REP-14 Vector-valued function, BC-REP-01 Symbolic, BC-REP-09 Calculator-generated numerical result.

Conversions tested: a rate vector with an initial condition to a coordinate value (BC-REP-14 to BC-REP-09), and a position statement back to an integral expression (BC-REP-04 to BC-REP-01).

### Assessment behaviour

MCQ forms ask which expression gives a coordinate at a later time. FRQ forms ask for one coordinate of the position at a time given the position at another time, scoring the definite integral, the use of the initial condition, and the answer (sg-24:7, sg-23:7). Calculator variants evaluate the integral numerically; no-calculator variants use antidifferentiable components. Conceptual variants ask what the integral of a velocity component gives; computational variants ask for the coordinate; interpretation variants ask for the meaning of the displacement vector; justification variants are uncommon. Multi-concept variants combine the coordinate with a slope or a speed part in the same question (sg-23:7).

### Archetypes

- BC-QA-09005 Coordinate of a particle recovered from an initial position

### Errors and misconceptions

- BC-ERR-09019 One constant of integration used for both components
- BC-ERR-09015 Magnitude of the displacement reported as the distance travelled
- BC-ERR-09020 Initial position not added to the accumulated change
- BC-ERR-09021 Accumulation run in the wrong direction in time
- BC-MIS-09009 A vector answer is a pair of numbers with no structure, severity medium
- BC-MIS-09006 Distance travelled in the plane is the size of the net change in position, severity high
- BC-MIS-09010 The integral of a velocity component is the coordinate, severity high

### Diagnostic signals

- BC-SIG-09004 Magnitude of displacement reported as distance travelled
- BC-SIG-09006 Definite integral reported as a coordinate
- BC-SIG-09007 Accumulation added when the known time is later

### Adaptive metadata summary

Skills in this topic carry calculator relevance optional, typically_required. Remediation targets named across the topic: BC-PRQ-09001, con.vector_initial_value, con.vector_integral. Every skill record carries the full seven key adaptive block in data/staging/unit-09.skills.json. [inferred]

## 9.6 Solving Motion Problems Using Parametric and Vector-Valued Functions

### Official mapping

Topic id BC-TOP-0906, CED code 9.6, name Solving Motion Problems Using Parametric and Vector-Valued Functions, scope BC_only, CED page 176. [verified] (ced:176)

- BC-LO-FUN-8B (FUN-8.B): Determine values for positions and rates of change in problems involving planar motion.
  - BC-EK-FUN-8B1 (FUN-8.B.1): "Derivatives can be used to determine velocity, speed, and acceleration for a particle moving along a curve in the plane defined using parametric or vector-valued functions."
  - BC-EK-FUN-8B2 (FUN-8.B.2): "For a particle in planar motion over an interval of time, the definite integral of the velocity vector represents the particle's displacement (net change in position) over the interval of time, from which we might determine its position. The definite integral of speed represents the particle's total distance traveled over the interval of time."

Suggested practice skills: BC-MPS-1E (Practice skill 1.E). Weighting pointer: [../exam/exam-blueprint.md](../exam/exam-blueprint.md).

### Concept breakdown

- BC-CON-09009 Speed as the magnitude of the velocity vector: Speed is the length of the velocity vector, not either component.
- BC-CON-09010 Total distance travelled as the integral of speed: Integrating speed over the interval gives the length of the path travelled.
- BC-CON-09011 Direction of motion read from the signs of the velocity components: Each component sign says which way the particle is moving along that axis.

- BC-SKL-09023 Compute the speed of a particle as the magnitude of its velocity: Square both components, add, take the square root.
- BC-SKL-09024 Solve for a time at which the speed has a stated value: Set the speed expression equal to the number and solve on the interval.
- BC-SKL-09025 Compute the total distance travelled as the integral of speed: Integrate the speed expression over the time interval.
- BC-SKL-09026 Determine a coordinate of the particle at a time from an initial condition: Add the integral of the matching velocity component to the known coordinate.
- BC-SKL-09027 Determine when a particle moves toward or away from a coordinate axis: Compare the sign of the coordinate with the sign of its rate.
- BC-SKL-09028 Present the acceleration vector at a time with its setup: Show the derivative of each velocity component before the two numbers.

### Prerequisites

- BC-PRQ-08007 -> BC-SKL-09023, supporting, [inferred], Prerequisite for Compute the speed of a particle as the magnitude of its velocity.
- BC-PRQ-08001 -> BC-SKL-09024, supporting, [inferred], Prerequisite for Solve for a time at which the speed has a stated value.
- BC-PRQ-09003 -> BC-SKL-09024, supporting, [inferred], Prerequisite for Solve for a time at which the speed has a stated value.
- BC-PRQ-08007 -> BC-SKL-09025, supporting, [inferred], Prerequisite for Compute the total distance travelled as the integral of speed.
- BC-PRQ-06005 -> BC-SKL-09026, supporting, [inferred], Prerequisite for Determine a coordinate of the particle at a time from an initial condition.
- BC-PRQ-08001 -> BC-SKL-09027, supporting, [inferred], Prerequisite for Determine when a particle moves toward or away from a coordinate axis.
- BC-PRQ-09001 -> BC-SKL-09028, supporting, [inferred], Prerequisite for Present the acceleration vector at a time with its setup.
- BC-SKL-08007 -> BC-SKL-09025, hard_prerequisite, [verified], Total distance as the integral of speed is the rectilinear skill transported to planar motion.
- BC-SKL-08009 -> BC-SKL-09026, hard_prerequisite, [verified], A position value from an initial position is the rectilinear skill applied componentwise.

### Required mathematical knowledge

**Velocity, speed, acceleration.** Derivatives determine velocity, speed, and acceleration for a particle moving along a curve in the plane defined using parametric or vector-valued functions (BC-EK-FUN-8B1). Speed is the magnitude of the velocity vector, so it is the square root of the sum of the squares of the components.

**Displacement and distance.** The definite integral of the velocity vector is the displacement, from which the position may be determined, and the definite integral of speed is the total distance travelled (BC-EK-FUN-8B2).

**Direction of motion.** A particle in the first quadrant moves toward the x axis exactly when its y coordinate is positive and its y rate is negative; the 2024 guideline scored one point for considering the sign of that rate and one for the answer with the reason (sg-24:8).

**Imported work.** The 2023 guideline allowed an incorrect speed expression declared in an earlier part to be carried into the distance integral for the setup point but not for the answer point (sg-23:8).

**Notation.** Parenthesis errors inside a squared component cost the speed setup point in 2023 while leaving the answer point available (sg-23:6). Calculator work must be in radian mode; responses computed in degree mode did not earn the first point they would otherwise have earned (sg-23:6).

### Representations

Representations in play: BC-REP-14 Vector-valued function, BC-REP-12 Parametric equations, BC-REP-09 Calculator-generated numerical result, BC-REP-05 Contextual model.

Conversions tested: component rates to a speed (BC-REP-14 to BC-REP-01), speed to a total distance (BC-REP-01 to BC-REP-09), and signs of components to a verbal statement about direction (BC-REP-14 to BC-REP-04).

### Assessment behaviour

MCQ forms ask for the speed at a time or for the integral that gives the distance travelled. FRQ forms build the whole calculator active BC question from this topic: an acceleration vector with setup, a time at which the speed takes a value, a coordinate recovered from an initial condition, a total distance, and a direction of motion argument (frq-23:4, frq-24:4). Calculator variants dominate, because the speed integrand rarely antidifferentiates; no-calculator variants ask for the setup alone. Conceptual variants ask which quantity the integral of speed gives; computational variants ask for values; interpretation variants ask for units; justification variants ask for the reason a particle approaches an axis (sg-24:8). Multi-concept variants chain four parts across position, velocity, speed, and distance in one question.

### Archetypes

- BC-QA-09006 Speed of a particle in planar motion
- BC-QA-09007 Total distance travelled by a particle in the plane
- BC-QA-09005 Coordinate of a particle recovered from an initial position
- BC-QA-09008 Times at which a particle moves toward a coordinate axis
- BC-QA-09004 Acceleration vector of a particle in planar motion

### Errors and misconceptions

- BC-ERR-09013 Component rates added instead of combined as a magnitude
- BC-ERR-09014 Parentheses lost inside a squared component
- BC-ERR-09022 Time reported with no speed equation
- BC-ERR-09023 Calculator work performed in degree mode
- BC-ERR-09015 Magnitude of the displacement reported as the distance travelled
- BC-ERR-09024 Incorrect speed expression carried into the distance integral
- BC-ERR-09020 Initial position not added to the accumulated change
- BC-ERR-09018 Variable expression equated to a numerical value
- BC-ERR-09025 Direction of motion read from the sign of the coordinate
- BC-ERR-09026 Interval reported with no reason
- BC-ERR-09011 Numerical answer presented with no setup
- BC-MIS-09011 Speed is one of the two velocity components, severity high
- BC-MIS-09006 Distance travelled in the plane is the size of the net change in position, severity high
- BC-MIS-09010 The integral of a velocity component is the coordinate, severity high
- BC-MIS-09012 The direction of motion is given by the sign of the position, severity high
- BC-MIS-09009 A vector answer is a pair of numbers with no structure, severity medium

### Diagnostic signals

- BC-SIG-09003 Component rates added inside a speed or length
- BC-SIG-09008 Time reported with no equation
- BC-SIG-09004 Magnitude of displacement reported as distance travelled
- BC-SIG-09006 Definite integral reported as a coordinate
- BC-SIG-09009 Correct interval of approach with no sign argument
- BC-SIG-09005 Correct vector with no supporting work

### Adaptive metadata summary

Skills in this topic carry calculator relevance typically_required. Remediation targets named across the topic: BC-PRQ-09001, con.planar_direction, con.planar_distance, con.planar_speed. Every skill record carries the full seven key adaptive block in data/staging/unit-09.skills.json. [inferred]

## 9.7 Defining Polar Coordinates and Differentiating in Polar Form

### Official mapping

Topic id BC-TOP-0907, CED code 9.7, name Defining Polar Coordinates and Differentiating in Polar Form, scope BC_only, CED page 177. [verified] (ced:177)

- BC-LO-FUN-3G (FUN-3.G): Calculate derivatives of functions written in polar coordinates.
  - BC-EK-FUN-3G1 (FUN-3.G.1): "Methods for calculating derivatives of real-valued functions can be extended to functions in polar coordinates."
  - BC-EK-FUN-3G2 (FUN-3.G.2): "For a curve given by a polar equation r = f(theta), derivatives of r, x, and y with respect to theta, and first and second derivatives of y with respect to x can provide information about the curve."

Suggested practice skills: BC-MPS-2D (Practice skill 2.D). Weighting pointer: [../exam/exam-blueprint.md](../exam/exam-blueprint.md).

### Concept breakdown

- BC-CON-09012 Polar to Cartesian relations: The coordinates of a polar point are r times cosine and r times sine of the angle.
- BC-CON-09013 Rate of change of r with respect to theta: The derivative of r says how fast the distance from the origin changes with the angle.
- BC-CON-09014 Slope of a polar curve in the plane: Write x and y in theta, then take the quotient of their rates.

- BC-SKL-09029 Convert a point on a polar curve to Cartesian coordinates: Multiply r by cosine and by sine of the angle.
- BC-SKL-09030 Compute dr/dtheta for a polar curve and evaluate it: Differentiate r with respect to the angle and substitute.
- BC-SKL-09031 Interpret dr/dtheta as the rate at which the distance from the origin changes: Say that it measures how the distance from the origin changes with the angle.
- BC-SKL-09032 Relate the rate of the distance from the origin in time to dr/dtheta: Multiply dr/dtheta by the rate at which the angle changes.
- BC-SKL-09033 Compute dy/dx for a polar curve: Differentiate r cosine and r sine with respect to theta and divide.
- BC-SKL-09034 Locate the point on a polar curve farthest from a coordinate axis: Set the derivative of that coordinate equal to zero and compare candidates.

### Prerequisites

- BC-PRQ-09002 -> BC-SKL-09029, supporting, [inferred], Prerequisite for Convert a point on a polar curve to Cartesian coordinates.
- BC-PRQ-09003 -> BC-SKL-09030, supporting, [inferred], Prerequisite for Compute dr/dtheta for a polar curve and evaluate it.
- BC-PRQ-06005 -> BC-SKL-09031, supporting, [inferred], Prerequisite for Interpret dr/dtheta as the rate at which the distance from the origin changes.
- BC-PRQ-06005 -> BC-SKL-09032, supporting, [inferred], Prerequisite for Relate the rate of the distance from the origin in time to dr/dtheta.
- BC-PRQ-09002 -> BC-SKL-09033, supporting, [inferred], Prerequisite for Compute dy/dx for a polar curve.
- BC-PRQ-08001 -> BC-SKL-09034, supporting, [inferred], Prerequisite for Locate the point on a polar curve farthest from a coordinate axis.
- BC-TOP-0301 -> BC-SKL-09032, hard_prerequisite, [inferred], The chain rule supplies the product of dr/dtheta with dtheta/dt; no Unit 3 skill id exists yet.
- BC-TOP-0208 -> BC-SKL-09033, hard_prerequisite, [inferred], The product rule is needed to differentiate r times a trigonometric factor; no Unit 2 skill id exists yet.
- BC-TOP-0505 -> BC-SKL-09034, hard_prerequisite, [inferred], The candidates test supplies the global argument the 2025 guideline required; no Unit 5 skill id exists yet.

### Required mathematical knowledge

**Polar to Cartesian.** For a curve given by a polar equation, x equals r times the cosine of theta and y equals r times the sine of theta (BC-EK-FUN-3G2).

**Derivatives in polar form.** Methods for calculating derivatives extend to functions in polar coordinates (BC-EK-FUN-3G1). Derivatives of r, x, and y with respect to theta, and first and second derivatives of y with respect to x, provide information about the curve (BC-EK-FUN-3G2).

**Meaning of dr/dtheta.** Because r is the distance from the origin, dr/dtheta is the rate at which that distance changes as the angle increases. When a particle travels along the curve with a known dtheta/dt, the rate at which its distance from the origin changes with time is dr/dtheta multiplied by dtheta/dt, which the 2025 guideline scored as its own point (sg-25:10).

**Extreme coordinate.** A point farthest from the y axis is one where x attains its maximum, so the condition is dx/dtheta equal to zero together with a comparison of candidates; a local argument alone did not earn the justification point in 2025 (sg-25:9).

**Notation.** A response must indicate differentiation of r, not only a value; the 2025 guideline accepted several notations but required the differentiation to be visible (sg-25:7).

### Representations

Representations in play: BC-REP-13 Polar equation, BC-REP-02 Graphical, BC-REP-01 Symbolic, BC-REP-09 Calculator-generated numerical result.

Conversions tested: polar equation to Cartesian coordinates of a point (BC-REP-13 to BC-REP-01), polar equation to a rate of change of distance from the origin (BC-REP-13 to BC-REP-04), and a plotted polar curve to a statement about a tangent (BC-REP-02 to BC-REP-04).

### Assessment behaviour

MCQ forms ask for dr/dtheta or for dy/dx at an angle on a polar curve. FRQ forms open the calculator active BC question with a rate of change of r and close it with a rate in time, scoring the derivative with setup and the chain rule product as separate points (sg-25:6, sg-25:10). Calculator variants evaluate at decimal angles in radian mode; no-calculator variants keep the differentiation symbolic. Conceptual variants ask what dr/dtheta measures; computational variants ask for its value; interpretation variants ask what the sign says about the curve; justification variants ask for the global argument behind an extreme coordinate (sg-25:9). Multi-concept variants combine the derivative with an area part on the same curve (frq-25:4).

### Archetypes

- BC-QA-09009 Derivative of r with respect to theta on a polar curve
- BC-QA-09011 Point on a polar curve farthest from a coordinate axis
- BC-QA-09010 Rate at which a particle's distance from the origin changes

### Errors and misconceptions

- BC-ERR-09027 Polar radius used as a Cartesian coordinate
- BC-ERR-09028 Polar derivative value given with no sign of differentiation
- BC-ERR-09006 Intermediate value rounded before a later step
- BC-ERR-09029 Rate of change of r described as the speed of the particle
- BC-ERR-09030 Rate of the angle omitted from a chain rule product
- BC-ERR-09031 Slope of a polar curve given as dr/dtheta
- BC-ERR-09032 Product rule omitted when differentiating r times a trigonometric factor
- BC-ERR-09033 Local argument offered for a farthest point
- BC-ERR-09034 Critical angle presented with no equation
- BC-MIS-09013 The polar radius is a Cartesian coordinate, severity high
- BC-MIS-09014 The derivative of r is the speed along the curve, severity high
- BC-MIS-09015 The slope of a polar curve is the derivative of r, severity medium
- BC-MIS-09016 A local extremum argument settles a farthest point, severity high

### Diagnostic signals

- BC-SIG-09010 Polar derivative value with no differentiation shown
- BC-SIG-09011 Critical angle found with only a local justification

### Adaptive metadata summary

Skills in this topic carry calculator relevance none, optional, typically_required. Remediation targets named across the topic: BC-PRQ-09002, BC-PRQ-09003, con.polar_dr, con.polar_slope. Every skill record carries the full seven key adaptive block in data/staging/unit-09.skills.json. [inferred]

## 9.8 Find the Area of a Polar Region or the Area Bounded by a Single Polar Curve

### Official mapping

Topic id BC-TOP-0908, CED code 9.8, name Find the Area of a Polar Region or the Area Bounded by a Single Polar Curve, scope BC_only, CED page 178. [verified] (ced:178)

- BC-LO-CHA-5D (CHA-5.D): Calculate areas of regions defined by polar curves using definite integrals.
  - BC-EK-CHA-5D1 (CHA-5.D.1): "The concept of calculating areas in rectangular coordinates can be extended to polar coordinates."

Suggested practice skills: BC-MPS-3D (Practice skill 3.D). Weighting pointer: [../exam/exam-blueprint.md](../exam/exam-blueprint.md).

### Concept breakdown

- BC-CON-09015 Area of a polar region as an integral of one half r squared: Sum the areas of thin circular sectors across the angle interval.

- BC-SKL-09035 State the polar area integral for a single curve: Write one half the integral of r squared with respect to the angle.
- BC-SKL-09036 Determine the angles that bound a polar region: Find the angles where the region starts and stops being swept.
- BC-SKL-09037 Identify the angle interval that traces one loop of a polar curve: Use consecutive zeros of r to bound one petal.
- BC-SKL-09038 Evaluate a polar area integral and report the area: Compute the integral with technology and state the area.

### Prerequisites

- BC-PRQ-06005 -> BC-SKL-09035, supporting, [inferred], Prerequisite for State the polar area integral for a single curve.
- BC-PRQ-09004 -> BC-SKL-09036, supporting, [inferred], Prerequisite for Determine the angles that bound a polar region.
- BC-PRQ-09002 -> BC-SKL-09037, supporting, [inferred], Prerequisite for Identify the angle interval that traces one loop of a polar curve.
- BC-PRQ-08006 -> BC-SKL-09038, supporting, [inferred], Prerequisite for Evaluate a polar area integral and report the area.
- BC-SKL-06034 -> BC-SKL-09038, hard_prerequisite, [verified], Evaluating a definite integral by antidifferentiation underlies the polar area evaluation.

### Required mathematical knowledge

**Polar area.** The concept of calculating areas in rectangular coordinates extends to polar coordinates (BC-EK-CHA-5D1). Hypotheses: r continuous on the angle interval, which sweeps the region exactly once. Conclusion: the area is one half the definite integral of the square of r with respect to theta.

**Limits.** The limits are angles, not x values. Consecutive zeros of r bound one loop of a curve that has several.

**Factor and square.** The one half and the square of r are both part of the integrand; in 2025 the presence of the square of r earned the first point and the factor of one half was assessed with the limits in the answer point (sg-25:7).

**Notation.** The differential is d theta, and the integrand is r squared rather than r.

### Representations

Representations in play: BC-REP-13 Polar equation, BC-REP-02 Graphical, BC-REP-01 Symbolic, BC-REP-09 Calculator-generated numerical result.

Conversions tested: a plotted polar region to an angle interval (BC-REP-02 to BC-REP-01), and a polar equation to an area integral (BC-REP-13 to BC-REP-01).

### Assessment behaviour

MCQ forms ask which integral gives the area of a pictured polar region, with the missing factor of one half and the unsquared r as distractors. FRQ forms ask for the area of a region described in polar form, scoring an integral containing the square of r, then the correct integrand, then the value with the limits and the factor of one half (sg-25:7). Calculator variants evaluate numerically and require the setup; no-calculator variants use an integrand that antidifferentiates with a double angle identity. Conceptual variants ask why the integrand is squared; computational variants ask for the value; interpretation variants ask what region the limits describe; justification variants ask why an interval traces the loop once. Multi-concept variants pair the area with a derivative part on the same curve (frq-25:4).

### Archetypes

- BC-QA-09012 Area of a region bounded by a single polar curve

### Errors and misconceptions

- BC-ERR-09035 Factor of one half omitted from a polar area integral
- BC-ERR-09036 Polar area integrand written without squaring r
- BC-ERR-09016 Integration over an interval that traces the curve more than once
- BC-ERR-09037 Polar limits taken from the wrong angles
- BC-ERR-09006 Intermediate value rounded before a later step
- BC-ERR-09011 Numerical answer presented with no setup
- BC-MIS-09017 A polar area is an integral of the curve itself, severity high
- BC-MIS-09007 Any interval containing the curve gives its length or area, severity medium
- BC-MIS-09008 A calculator result stands without its expression, severity medium

### Diagnostic signals

- BC-SIG-09012 Polar area integral without the factor of one half

### Adaptive metadata summary

Skills in this topic carry calculator relevance optional, typically_required. Remediation targets named across the topic: BC-PRQ-09002, BC-PRQ-09004, con.polar_area. Every skill record carries the full seven key adaptive block in data/staging/unit-09.skills.json. [inferred]

## 9.9 Finding the Area of the Region Bounded by Two Polar Curves

### Official mapping

Topic id BC-TOP-0909, CED code 9.9, name Finding the Area of the Region Bounded by Two Polar Curves, scope BC_only, CED page 179. [verified] (ced:179)

- BC-LO-CHA-5D (CHA-5.D): Calculate areas of regions defined by polar curves using definite integrals.
  - BC-EK-CHA-5D2 (CHA-5.D.2): "Areas of regions bounded by polar curves can be calculated with definite integrals."

Suggested practice skills: BC-MPS-3D (Practice skill 3.D). Weighting pointer: [../exam/exam-blueprint.md](../exam/exam-blueprint.md).

### Concept breakdown

- BC-CON-09016 Area between two polar curves: Subtract the squares of the two radii inside one half the integral.
- BC-CON-09017 Intersection angles of two polar curves: The curves meet where their radii agree at the same angle.

- BC-SKL-09039 Find the intersection angles of two polar curves: Set the two radius expressions equal and solve for the angles.
- BC-SKL-09040 Determine which polar curve is outer on an angle interval: Test one angle in the interval to see which radius is larger.
- BC-SKL-09041 Set up the area integral between two polar curves: Write one half the integral of outer squared minus inner squared.
- BC-SKL-09042 Evaluate the area between two polar curves and report it: Compute the integral and state the area.
- BC-SKL-09043 Use symmetry or a sum of integrals for a polar region with several pieces: Double half the region, or add one integral per piece.

### Prerequisites

- BC-PRQ-09002 -> BC-SKL-09039, supporting, [inferred], Prerequisite for Find the intersection angles of two polar curves.
- BC-PRQ-08001 -> BC-SKL-09039, supporting, [inferred], Prerequisite for Find the intersection angles of two polar curves.
- BC-PRQ-09002 -> BC-SKL-09040, supporting, [inferred], Prerequisite for Determine which polar curve is outer on an angle interval.
- BC-PRQ-06005 -> BC-SKL-09041, supporting, [inferred], Prerequisite for Set up the area integral between two polar curves.
- BC-PRQ-08006 -> BC-SKL-09042, supporting, [inferred], Prerequisite for Evaluate the area between two polar curves and report it.
- BC-PRQ-09004 -> BC-SKL-09043, supporting, [inferred], Prerequisite for Use symmetry or a sum of integrals for a polar region with several pieces.
- BC-SKL-08051 -> BC-SKL-09041, supporting, [verified], Subtracting the squares of the radii rather than squaring their difference is the washer skill of Unit 8.
- BC-SKL-08019 -> BC-SKL-09041, supporting, [inferred], Setting up an area as a difference of boundary curves is the Cartesian form of the polar area between curves.

### Required mathematical knowledge

**Area between polar curves.** Areas of regions bounded by polar curves can be calculated with definite integrals (BC-EK-CHA-5D2). The area inside one curve and outside another is one half the definite integral of the square of the outer radius minus the square of the inner radius, taken between the angles at which the curves meet.

**Intersection angles.** The limits are found by setting the two radius functions equal on the interval; in 2025 the two bounding angles were the solutions of that equation and were assessed in the answer point rather than in the setup points (sg-25:7).

**Order of operations.** The two radii are squared before they are subtracted, as in the washer method of Unit 8.

**Symmetry.** An integral over half a symmetric region multiplied by two earns the same points as the full integral (sg-25:8).

**Notation.** Unclear communication between a correct integral and a correct value was treated as scratch work in 2025 and did not cost a point (sg-25:8).

### Representations

Representations in play: BC-REP-13 Polar equation, BC-REP-02 Graphical, BC-REP-01 Symbolic, BC-REP-09 Calculator-generated numerical result.

Conversions tested: two plotted polar curves to a pair of intersection angles (BC-REP-02 to BC-REP-09), and a described region to an integrand built from two squared radii (BC-REP-04 to BC-REP-01).

### Assessment behaviour

MCQ forms ask which integral gives the area inside one polar curve and outside another. FRQ forms ask for that area with the setup shown, scoring an integral containing the square of the outer radius, then the full integrand, then the value with the limits and the factor of one half (sg-25:7). Calculator variants dominate, with intersection angles found numerically and stored. Conceptual variants ask which curve is outer; computational variants ask for the value; interpretation variants ask what region the limits describe; justification variants ask why the region needs two integrals when the outer curve changes. Multi-concept variants place the area between a derivative part and a motion part on the same curve (frq-25:4).

### Archetypes

- BC-QA-09013 Area inside one polar curve and outside another

### Errors and misconceptions

- BC-ERR-09037 Polar limits taken from the wrong angles
- BC-ERR-09038 One intersection angle not found
- BC-ERR-09039 Inner and outer polar radii exchanged
- BC-ERR-09040 Square of the difference of the radii used in a polar area
- BC-ERR-09035 Factor of one half omitted from a polar area integral
- BC-ERR-09006 Intermediate value rounded before a later step
- BC-ERR-09018 Variable expression equated to a numerical value
- BC-ERR-09041 Symmetry used without the compensating factor
- BC-MIS-09019 The limits of a polar area are the whole interval of the figure, severity high
- BC-MIS-09018 The area between polar curves uses the difference of the radii, severity high
- BC-MIS-09008 A calculator result stands without its expression, severity medium

### Diagnostic signals

- BC-SIG-09013 Polar area limits spanning the whole figure
- BC-SIG-09012 Polar area integral without the factor of one half

### Adaptive metadata summary

Skills in this topic carry calculator relevance optional, typically_required. Remediation targets named across the topic: BC-PRQ-09002, BC-PRQ-09004, con.polar_area_between. Every skill record carries the full seven key adaptive block in data/staging/unit-09.skills.json. [inferred]

## Cross-unit connections

Cross-unit edges to Units 6 and 8 use the skill ids already present in data/skills.json. Edges to Units 2, 3, and 5 use BC-TOP ids as the node on the other unit's side, because no skills exist in data/skills.json for those units yet; the `notes` field on each edge in data/staging/unit-09.edges.csv describes the skill that the topic id stands in for. [inferred]

### What Unit 9 depends on

**Unit 8 applications of integration.** The planar motion skills are the two component form of the rectilinear motion skills: BC-SKL-09025 rests on BC-SKL-08007, BC-SKL-09026 on BC-SKL-08009, and BC-SKL-09020 on BC-SKL-08006. The parametric arc length skills rest on BC-SKL-08056 and BC-SKL-08059. The area between two polar curves rests on the washer habit recorded as BC-SKL-08051, that the radii are squared before they are subtracted, and on the area set up skill BC-SKL-08019.

**Unit 6 integration and accumulation.** BC-SKL-09038 evaluates a polar area integral with BC-SKL-06034, and BC-SKL-09021 recovers a coordinate from an initial condition with BC-SKL-06037.

**Unit 2 and Unit 3 derivatives.** The product rule is needed for the derivatives of r times a trigonometric factor, recorded as an edge from BC-TOP-0208, and the chain rule supplies the product of dr/dtheta with dtheta/dt, recorded as an edge from BC-TOP-0301.

**Unit 5 analytical applications.** The justification that a point on a polar curve is farthest from an axis uses the candidates test, recorded as an edge from BC-TOP-0505. The 2025 scoring guideline required the global form of that argument (sg-25:9).

### What depends on Unit 9

**Unit 10.** No Unit 10 topic depends on this unit directly. The parametric and polar representations recorded here are the last new representations the course introduces, and the series unit works in the symbolic representation alone.

## Archetype summary

13 archetypes with 32 variants are recorded in data/staging/unit-09.archetypes.json. Variant dimensions used are representation, reasoning direction, notation, context, and calculator. [verified] (sg-23:5, sg-23:6, sg-23:7, sg-23:8, sg-24:5, sg-24:6, sg-24:7, sg-24:8, sg-25:6, sg-25:7, sg-25:8, sg-25:9, sg-25:10)

| Archetype | Name | Scope | Calculator | Official parts read |
|---|---|---|---|---|
| BC-QA-09001 | Slope of the tangent to a parametric path at a time | BC_only | calculator | 2023 Q2(c) |
| BC-QA-09002 | Second derivative of a parametric curve | BC_only | either | no parametric second derivative appears in the 2023 to 2025 BC free response questions |
| BC-QA-09003 | Length of a parametric curve | BC_only | calculator | 2023 Q2(d), 2024 Q2(b) |
| BC-QA-09004 | Acceleration vector of a particle in planar motion | BC_only | calculator | 2023 Q2(a) |
| BC-QA-09005 | Coordinate of a particle recovered from an initial position | BC_only | calculator | 2024 Q2(c), 2023 Q2(c) |
| BC-QA-09006 | Speed of a particle in planar motion | BC_only | calculator | 2023 Q2(b), 2024 Q2(a) |
| BC-QA-09007 | Total distance travelled by a particle in the plane | BC_only | calculator | 2023 Q2(d), 2024 Q2(b) |
| BC-QA-09008 | Times at which a particle moves toward a coordinate axis | BC_only | calculator | 2024 Q2(d) |
| BC-QA-09009 | Derivative of r with respect to theta on a polar curve | BC_only | calculator | 2025 Q2(A) |
| BC-QA-09010 | Rate at which a particle's distance from the origin changes | BC_only | calculator | 2025 Q2(D) |
| BC-QA-09011 | Point on a polar curve farthest from a coordinate axis | BC_only | calculator | 2025 Q2(C) |
| BC-QA-09012 | Area of a region bounded by a single polar curve | BC_only | either | 2025 Q2(B) |
| BC-QA-09013 | Area inside one polar curve and outside another | BC_only | calculator | 2025 Q2(B) |

Eleven of the thirteen archetypes are grounded in 2023 to 2025 scoring guidelines, because the calculator active BC question was a planar motion question in 2023 and 2024 and a polar question in 2025. Only the parametric second derivative archetype and the parametric length of a non motion curve carry inferred scoring patterns.

## Misconception summary

19 misconceptions are recorded in data/staging/unit-09.misconceptions.json, each with the rival it is most easily confused with and a probe that separates them. Misconception literature for this unit could not be confirmed from the sources in this project's cache, so causes are drawn from scoring guideline evidence and are tagged inferred where no guideline names the behaviour. [inferred]

| Misconception | Severity | Rivals | Discriminating probe |
|---|---|---|---|
| BC-MIS-09001 The parameter is the horizontal coordinate | high | BC-MIS-09002 | Ask for the coordinates of the point at a stated parameter value and then for the slope there. |
| BC-MIS-09002 The slope of a parametric path is the rate of the vertical component | high | BC-MIS-09003 | Give a path whose horizontal rate is two and ask for both dy/dt and the slope. |
| BC-MIS-09003 The order of the parametric quotient does not matter | medium | BC-MIS-09002 | Ask what the slope should be on a path where the horizontal rate is large and the vertical rate is small. |
| BC-MIS-09004 The second derivative follows the same pattern as the first | high | BC-MIS-09003 | Ask which function is being differentiated at the second step and with respect to which variable. |
| BC-MIS-09005 A length in the plane is the sum of the two component contributions | high | BC-MIS-09011 | Ask for the speed of a particle with component rates three and four. |
| BC-MIS-09006 Distance travelled in the plane is the size of the net change in position | high | BC-MIS-09005 | Ask for both quantities for a particle that returns to its starting point. |
| BC-MIS-09007 Any interval containing the curve gives its length or area | medium | BC-MIS-09019 | Ask at which parameter values the curve revisits a point it has already passed. |
| BC-MIS-09008 A calculator result stands without its expression | medium | BC-MIS-09009 | Ask the student to write the expression the calculator evaluated, without using the calculator. |
| BC-MIS-09009 A vector answer is a pair of numbers with no structure | medium | BC-MIS-09008 | Ask which of the two reported numbers is the horizontal component and why. |
| BC-MIS-09010 The integral of a velocity component is the coordinate | high | BC-MIS-09006 | Ask for the same coordinate with the known position moved to a different point. |
| BC-MIS-09011 Speed is one of the two velocity components | high | BC-MIS-09005 | Ask for the speed at a time when one component is zero and the other is not. |
| BC-MIS-09012 The direction of motion is given by the sign of the position | high | BC-MIS-09010 | Ask what the rate is doing at a time when the coordinate is positive and the particle is approaching the axis. |
| BC-MIS-09013 The polar radius is a Cartesian coordinate | high | BC-MIS-09015 | Ask for both Cartesian coordinates of the point at a stated angle on the curve. |
| BC-MIS-09014 The derivative of r is the speed along the curve | high | BC-MIS-09015 | Ask what quantity r measures, and then what the units of the requested rate are. |
| BC-MIS-09015 The slope of a polar curve is the derivative of r | medium | BC-MIS-09014 | Ask for the slope of the tangent to a circle of constant radius, where dr/dtheta is zero everywhere. |
| BC-MIS-09016 A local extremum argument settles a farthest point | high | BC-MIS-09008 | Ask for the value of the coordinate at both ends of the angle interval. |
| BC-MIS-09017 A polar area is an integral of the curve itself | high | BC-MIS-09018 | Ask for the area of a circular sector of stated radius and angle, then compare with the integral written. |
| BC-MIS-09018 The area between polar curves uses the difference of the radii | high | BC-MIS-09017 | Ask the student to evaluate both expressions with the radii two and one. |
| BC-MIS-09019 The limits of a polar area are the whole interval of the figure | high | BC-MIS-09007 | Ask at which angles the two curves meet before any integral is written. |

The highest severity clusters are the five that official scoring guidelines document directly: speed treated as a component or as a sum rather than as a magnitude (sg-24:5), the integral of a velocity component reported as a coordinate (sg-24:7), direction of motion read from the position rather than from its rate (sg-24:8), a local argument offered for a farthest point (sg-25:9), and the polar area formula transported from rectangular coordinates without the square and the factor of one half (sg-25:7).

## Unresolved

- Misconception literature for parametric, polar, and vector-valued topics is thin, and nothing in this project's cache confirms a specific published study. Every cause recorded here is inferred from official scoring guidelines and from the CED, and is tagged accordingly. [inferred]
- No 2023 to 2025 BC free response part asked for the second derivative of a parametric curve, so the scoring pattern for BC-QA-09002 is inferred from the first derivative scoring at sg-23:7. [uncertain]
- The 2023 and 2025 guidelines treat an unclear linkage between a correct expression and a correct value differently: the 2023 acceleration part awarded one of two points for equating an expression to a value (sg-23:6), while the 2025 polar area part treated the same kind of chain as scratch work (sg-25:8). Whether this is a durable change in scoring practice is not established here. [uncertain]
- Topic 9.7 lists first and second derivatives of y with respect to x among the tools a polar equation supports, but no 2023 to 2025 free response part required the second derivative of a polar curve, so no skill for it is recorded beyond BC-SKL-09033. [uncertain]
- The CED page numbers used in citations are the PDF page index, which for this unit runs 171 to 179 while the printed page numbers run 166 to 174. [verified] (ced:171, ced:179)

<!-- generated:official-evidence:start -->

## Official evidence index [verified]

Generated from data/frq_records.json and data/mcq_records.json. Every record cites its cached document and page; counts are observations over the indexed years only, not predictions. FRQ part records with BC-UNIT-09 as primary or secondary unit: 42. Public sample MCQ records tagged to this unit: 7.

| FRQ record | Role | Calculator | Archetype | Skills (first six) | Points | Point types |
|---|---|---|---|---|---|---|
| BC-FRQ-2013-Q2-A | primary | calculator | BC-QA-09013 | BC-SKL-09035, BC-SKL-09036, BC-SKL-09039, BC-SKL-09040, BC-SKL-09041, BC-SKL-09042 | 3 | BC-PT-99048, BC-PT-99001, BC-PT-99004 |
| BC-FRQ-2013-Q2-B | primary | calculator | BC-QA-09010 | BC-SKL-09029, BC-SKL-09033, BC-SKL-09026 | 3 | BC-PT-99005, BC-PT-99068, BC-PT-99004 |
| BC-FRQ-2013-Q2-C | primary | calculator | BC-QA-09004 | BC-SKL-09029, BC-SKL-09018, BC-SKL-09015, BC-SKL-09016 | 3 | BC-PT-99064, BC-PT-99052 |
| BC-FRQ-2014-Q2-A | primary | calculator | BC-QA-09013 | BC-SKL-09035, BC-SKL-09036, BC-SKL-09039, BC-SKL-09040, BC-SKL-09041, BC-SKL-09043 | 3 | BC-PT-99048, BC-PT-99001, BC-PT-99004 |
| BC-FRQ-2014-Q2-B | primary | calculator | BC-QA-09009 | BC-SKL-09029, BC-SKL-09030, BC-SKL-09033 | 2 | BC-PT-99049, BC-PT-99004 |
| BC-FRQ-2014-Q2-C | primary | calculator | BC-QA-09009 | BC-SKL-09030, BC-SKL-03002, BC-SKL-03027 | 2 | BC-PT-99005, BC-PT-99004 |
| BC-FRQ-2014-Q2-D | primary | calculator | BC-QA-09010 | BC-SKL-09030, BC-SKL-09032, BC-SKL-04019 | 2 | BC-PT-99049, BC-PT-99004 |
| BC-FRQ-2015-Q2-A | primary | calculator | BC-QA-09005 | BC-SKL-09019, BC-SKL-09020, BC-SKL-09021, BC-SKL-09026 | 3 | BC-PT-99001, BC-PT-99033, BC-PT-99004 |
| BC-FRQ-2015-Q2-B | primary | calculator | BC-QA-09001 | BC-SKL-09002, BC-SKL-09003, BC-SKL-09004 | 2 | BC-PT-99049, BC-PT-99004 |
| BC-FRQ-2015-Q2-C | primary | calculator | BC-QA-09006 | BC-SKL-09023, BC-SKL-09024 | 2 | BC-PT-99050, BC-PT-99004 |
| BC-FRQ-2015-Q2-D | primary | calculator | BC-QA-09007 | BC-SKL-09011, BC-SKL-09012, BC-SKL-09025, BC-SKL-09013 | 2 | BC-PT-99051, BC-PT-99004 |
| BC-FRQ-2018-Q2-D | primary | calculator | BC-QA-09007 | BC-SKL-09011, BC-SKL-09012, BC-SKL-09025, BC-SKL-09013 | 0 |  |
| BC-FRQ-2018-Q5-A | primary | no_calculator | BC-QA-09013 | BC-SKL-09035, BC-SKL-09036, BC-SKL-09039, BC-SKL-09040, BC-SKL-09041 | 0 |  |
| BC-FRQ-2018-Q5-B | primary | no_calculator | BC-QA-09009 | BC-SKL-09029, BC-SKL-09030, BC-SKL-09033 | 0 |  |
| BC-FRQ-2018-Q5-C | primary | no_calculator | BC-QA-09010 | BC-SKL-09030, BC-SKL-09031, BC-SKL-09032, BC-SKL-04024 | 0 |  |
| BC-FRQ-2019-Q2-A | primary | calculator | BC-QA-09012 | BC-SKL-09035, BC-SKL-09036, BC-SKL-09038 | 2 | BC-PT-99048, BC-PT-99004 |
| BC-FRQ-2019-Q2-B | secondary | calculator | BC-QA-08001 | BC-SKL-08001, BC-SKL-08003, BC-SKL-09029 | 2 | BC-PT-99020, BC-PT-99004 |
| BC-FRQ-2019-Q2-C | primary | calculator | BC-QA-09012 | BC-SKL-09035, BC-SKL-09036, BC-SKL-09043, BC-SKL-09029 | 3 | BC-PT-99048, BC-PT-99001, BC-PT-99005 |
| BC-FRQ-2019-Q2-D | primary | calculator | BC-QA-09012 | BC-SKL-09035, BC-SKL-09036, BC-SKL-09038, BC-SKL-01060 | 2 | BC-PT-99001, BC-PT-99005 |
| BC-FRQ-2021-Q2-A | primary | calculator | BC-QA-09006 | BC-SKL-09023, BC-SKL-09017, BC-SKL-09028, BC-SKL-09015 | 2 | BC-PT-99050, BC-PT-99052 |
| BC-FRQ-2021-Q2-B | primary | calculator | BC-QA-09007 | BC-SKL-09025, BC-SKL-09011, BC-SKL-09013, BC-SKL-09012 | 2 | BC-PT-99051, BC-PT-99004 |
| BC-FRQ-2021-Q2-C | primary | calculator | BC-QA-09005 | BC-SKL-09021, BC-SKL-09026, BC-SKL-09019, BC-SKL-05020, BC-SKL-05029 | 5 | BC-PT-99013, BC-PT-99010, BC-PT-99033, BC-PT-99004, BC-PT-99005 |
| BC-FRQ-2022-Q2-A | primary | calculator | BC-QA-09001 | BC-SKL-09002, BC-SKL-09004, BC-SKL-09003 | 1 | BC-PT-99005 |
| BC-FRQ-2022-Q2-B | primary | calculator | BC-QA-09004 | BC-SKL-09023, BC-SKL-09017, BC-SKL-09028, BC-SKL-09015 | 3 | BC-PT-99050, BC-PT-99052, BC-PT-99052 |
| BC-FRQ-2022-Q2-C | primary | calculator | BC-QA-09005 | BC-SKL-09021, BC-SKL-09026, BC-SKL-08012, BC-SKL-06037 | 3 | BC-PT-99002, BC-PT-99033, BC-PT-99004 |
| BC-FRQ-2022-Q2-D | primary | calculator | BC-QA-09007 | BC-SKL-09025, BC-SKL-09011, BC-SKL-09013, BC-SKL-09012 | 2 | BC-PT-99051, BC-PT-99004 |
| BC-FRQ-2023-Q2-A | primary | calculator | BC-QA-09004 | BC-SKL-09015, BC-SKL-09017, BC-SKL-09028, BC-SKL-03002 | 2 | BC-PT-99052, BC-PT-99005 |
| BC-FRQ-2023-Q2-B | primary | calculator | BC-QA-09006 | BC-SKL-09023, BC-SKL-09024, BC-SKL-04008 | 2 | BC-PT-99050, BC-PT-99004 |
| BC-FRQ-2023-Q2-C | primary | calculator | BC-QA-09001 | BC-SKL-09002, BC-SKL-09004, BC-SKL-09021, BC-SKL-09026, BC-SKL-06037 | 3 | BC-PT-99049, BC-PT-99001, BC-PT-99004 |
| BC-FRQ-2023-Q2-D | primary | calculator | BC-QA-09007 | BC-SKL-09025, BC-SKL-09011, BC-SKL-09013, BC-SKL-08007 | 2 | BC-PT-99051, BC-PT-99004 |
| BC-FRQ-2024-Q2-A | primary | calculator | BC-QA-09006 | BC-SKL-09023, BC-SKL-09016, BC-SKL-04008 | 2 | BC-PT-99050, BC-PT-99004 |
| BC-FRQ-2024-Q2-B | primary | calculator | BC-QA-09007 | BC-SKL-09025, BC-SKL-09011, BC-SKL-09013, BC-SKL-08007 | 2 | BC-PT-99051, BC-PT-99004 |
| BC-FRQ-2024-Q2-C | primary | calculator | BC-QA-09005 | BC-SKL-09021, BC-SKL-09022, BC-SKL-09026, BC-SKL-06037, BC-SKL-08012 | 3 | BC-PT-99001, BC-PT-99033, BC-PT-99004 |
| BC-FRQ-2024-Q2-D | primary | calculator | BC-QA-09008 | BC-SKL-09027, BC-SKL-04009, BC-SKL-04012, BC-SKL-05014 | 2 | BC-PT-99014, BC-PT-99010 |
| BC-FRQ-2025-Q2-A | primary | calculator | BC-QA-09009 | BC-SKL-09030, BC-SKL-03002, BC-SKL-02018 | 1 | BC-PT-99005 |
| BC-FRQ-2025-Q2-B | primary | calculator | BC-QA-09013 | BC-SKL-09039, BC-SKL-09040, BC-SKL-09041, BC-SKL-09042, BC-SKL-09036 | 3 | BC-PT-99048, BC-PT-99002, BC-PT-99004 |
| BC-FRQ-2025-Q2-C | primary | calculator | BC-QA-09011 | BC-SKL-09034, BC-SKL-09029, BC-SKL-05010, BC-SKL-05024, BC-SKL-05025, BC-SKL-05028 | 3 | BC-PT-99013, BC-PT-99011, BC-PT-99005 |
| BC-FRQ-2025-Q2-D | primary | calculator | BC-QA-09010 | BC-SKL-09031, BC-SKL-09032, BC-SKL-04019, BC-SKL-04024 | 2 | BC-PT-99049, BC-PT-99004 |
| BC-FRQ-2026-Q2-A | primary | calculator | BC-QA-09012 | BC-SKL-09035, BC-SKL-09036, BC-SKL-09038 | 2 | BC-PT-99048, BC-PT-99004 |
| BC-FRQ-2026-Q2-B | primary | calculator | BC-QA-09001 | BC-SKL-09033, BC-SKL-09002, BC-SKL-09003, BC-SKL-03002 | 3 | BC-PT-99049, BC-PT-99004, BC-PT-99004 |
| BC-FRQ-2026-Q2-C | secondary | calculator | BC-QA-05007 | BC-SKL-05010, BC-SKL-05020, BC-SKL-05036, BC-SKL-05039, BC-SKL-09030 | 2 | BC-PT-99004, BC-PT-99012 |
| BC-FRQ-2026-Q2-D | secondary | calculator | BC-QA-06007 | BC-SKL-08001, BC-SKL-08003, BC-SKL-06038, BC-SKL-09031 | 2 | BC-PT-99020, BC-PT-99004 |

| MCQ record | Calculator | Archetype | Skills |
|---|---|---|---|
| BC-MCQ-CED-018 | no_calculator | BC-QA-09002 | BC-SKL-09007, BC-SKL-09008, BC-SKL-09002 |
| BC-MCQ-CED-021 | calculator | BC-QA-09012 | BC-SKL-09036, BC-SKL-09037, BC-SKL-09038 |
| BC-MCQ-SAMPLE-017 | no_calculator | BC-QA-09001 | BC-SKL-09001, BC-SKL-09002, BC-SKL-09004 |
| BC-MCQ-SAMPLE-023 | calculator | BC-QA-09007 | BC-SKL-09025, BC-SKL-09023, BC-SKL-09011 |
| BC-MCQ-PE2012-002 | no_calculator | BC-QA-09001 | BC-SKL-09001, BC-SKL-09016, BC-SKL-04011 |
| BC-MCQ-PE2012-026 | no_calculator | BC-QA-09009 | BC-SKL-09033, BC-SKL-09030, BC-SKL-09029 |
| BC-MCQ-PE2012-044 | calculator | BC-QA-09013 | BC-SKL-09039, BC-SKL-09040, BC-SKL-09042 |

<!-- generated:official-evidence:end -->
