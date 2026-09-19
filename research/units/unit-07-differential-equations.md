---
title: Unit 7, Differential Equations
research_date: 2026-09-19
status: draft
purpose: Decompose CED Unit 7 into concepts, atomic skills, non-calculus prerequisites, question archetypes and variants, observed errors, candidate misconceptions, and diagnostic signals, each grounded in the CED text and in the 2023 to 2025 official free-response questions and scoring guidelines.
---

# Unit 7, Differential Equations

BC-UNIT-07 covers CED pages 132 to 145 and holds nine topics. Topics 7.5 and 7.9 carry the BC only marker in the CED and in data/curriculum.json; the other seven are shared with AB. Unit weighting is in [../exam/exam-blueprint.md](../exam/exam-blueprint.md) and exam composition is in [../exam/exam-structure.md](../exam/exam-structure.md). [verified] (ced:137, ced:141, ced:145)

A differential equation question appeared in each of 2023, 2024, and 2025, and in each year the same three moves carried most of the points: a solution curve drawn on a supplied slope field, an analysis of the solution done from the equation itself without solving, and a separation of variables scored in four or five named stages. Euler's method appeared separately in 2024 and 2025 as a two step approximation. No part in those three years asked for a logistic model, and none asked for a slope field to be drawn from scratch. [verified] (sg-23:9, sg-23:11, sg-23:12, sg-24:9, sg-24:10, sg-24:11, sg-24:17, sg-25:23)

## 7.1 Modeling Situations with Differential Equations

### Official mapping

Topic id BC-TOP-0701, CED code 7.1, name Modeling Situations with Differential Equations, scope shared, CED page 137. [verified] (ced:137)

- BC-LO-FUN-7A (FUN-7.A): Interpret verbal statements of problems as differential equations involving a derivative expression.
  - BC-EK-FUN-7A1 (FUN-7.A.1): "Differential equations relate a function of an independent variable and the function's derivatives."

Suggested practice skills: BC-MPS-2C (Practice skill 2.C). Weighting pointer: [../exam/exam-blueprint.md](../exam/exam-blueprint.md).

### Concept breakdown

- BC-CON-07001 Differential equation as a relation between a function and its derivatives: A differential equation says how fast a quantity changes in terms of the quantity itself, the independent variable, or both.

- BC-SKL-07001 Translate a proportionality statement into a differential equation: Turn the rate of change is proportional to the amount into an equation.
- BC-SKL-07002 Translate a rate statement involving a difference into a differential equation: Turn a rate proportional to a gap into an equation with that gap in it.
- BC-SKL-07003 Assign the variables and their units from a verbal description: Say which quantity is which and in what units.
- BC-SKL-07004 Identify the initial condition stated in a context: Pick out the sentence that gives the value at a particular input.
- BC-SKL-07005 Distinguish a differential equation from an equation for the quantity: Tell an equation about the rate apart from an equation about the amount.

### Prerequisites

- BC-PRQ-07003 -> BC-SKL-07001, supporting, [inferred], Prerequisite for Translate a proportionality statement into a differential equation.
- BC-PRQ-07003 -> BC-SKL-07002, supporting, [inferred], Prerequisite for Translate a rate statement involving a difference into a differential equation.
- BC-PRQ-06005 -> BC-SKL-07003, supporting, [inferred], Prerequisite for Assign the variables and their units from a verbal description.
- BC-PRQ-06005 -> BC-SKL-07004, supporting, [inferred], Prerequisite for Identify the initial condition stated in a context.
- BC-PRQ-07002 -> BC-SKL-07005, supporting, [inferred], Prerequisite for Distinguish a differential equation from an equation for the quantity.

### Required mathematical knowledge

**Definition.** A differential equation relates a function of an independent variable to that function's derivatives (BC-EK-FUN-7A1). The equations of this unit are first order, so only the function and its first derivative appear.

**Translation rules.** Proportional to the size of the quantity gives a constant multiple of the quantity; jointly proportional to two quantities gives a constant multiple of their product; proportional to the difference between the quantity and a fixed level gives a constant multiple of that difference, which is the form the 2023 and 2024 questions used (frq-23:7, frq-24:7).

**Variables and units.** The dependent variable is the modelled quantity, the independent variable is usually time, and the derivative carries the units of the quantity divided by the units of the independent variable.

**Initial condition.** A statement of the value of the quantity at a stated input is the initial condition and is separate from the differential equation itself.

**Notation.** dy/dt; dH/dt; k for the constant of proportionality; the phrase at time t equal to zero.

### Representations

Representations in play: BC-REP-04 Verbal description, BC-REP-05 Contextual model, BC-REP-06 Differential equation.

Conversions tested: verbal rate statement to a differential equation (BC-REP-04 to BC-REP-06), and contextual model to the units of the derivative (BC-REP-05 to BC-REP-04).

### Assessment behaviour

MCQ forms give a sentence describing a rate and ask which equation models it. FRQ forms supply the equation ready made and use the modelling as context rather than as a scored step, so the scored work begins at the slope field or the separation (frq-23:7, frq-24:7). Calculator status is either. Conceptual variants ask what the constant of proportionality means; computational variants ask for the equation; interpretation variants ask for the units of the derivative; justification variants ask why a proposed equation does not match the sentence; multi-concept variants attach an initial condition and a later solving step.

### Archetypes

- BC-QA-07006 Differential equation written from a verbal rate statement

### Errors and misconceptions

- BC-ERR-07001 Proportionality written without a constant
- BC-ERR-07002 Difference reversed in a rate proportional to a gap
- BC-ERR-07003 Variables used with no units or meanings
- BC-ERR-99005 Chief Reader error record, see data/errors.json
- BC-ERR-99033 Chief Reader error record, see data/errors.json
- BC-ERR-07004 Initial condition folded into the differential equation
- BC-ERR-07005 Equation written for the quantity rather than its rate
- BC-MIS-07001 Proportional to means equal to, severity high
- BC-MIS-07002 A differential equation is an equation for the quantity, severity high
- BC-MIS-07003 An initial condition is part of the differential equation, severity medium

### Diagnostic signals

- BC-SIG-07001 Model written with no constant of proportionality
- BC-SIG-07002 Equation written in undefined letters
- BC-SIG-07003 Initial condition absorbed into the equation
- BC-SIG-07004 Formula produced where an equation was asked for

### Adaptive metadata summary

Skills in this topic carry calculator relevance none. Remediation targets named across the topic: BC-PRQ-06005, BC-PRQ-07002, BC-PRQ-07003. Every skill record carries the full seven key adaptive block in data/staging/unit-07.skills.json. [inferred]

## 7.2 Verifying Solutions for Differential Equations

### Official mapping

Topic id BC-TOP-0702, CED code 7.2, name Verifying Solutions for Differential Equations, scope shared, CED page 138. [verified] (ced:138)

- BC-LO-FUN-7B (FUN-7.B): Verify solutions to differential equations.
  - BC-EK-FUN-7B1 (FUN-7.B.1): "Derivatives can be used to verify that a function is a solution to a given differential equation."
  - BC-EK-FUN-7B2 (FUN-7.B.2): "There may be infinitely many solutions to a differential equation."

Suggested practice skills: BC-MPS-3G (Practice skill 3.G). Weighting pointer: [../exam/exam-blueprint.md](../exam/exam-blueprint.md).

### Concept breakdown

- BC-CON-07002 Verification of a proposed solution: A candidate function is a solution exactly when differentiating it and substituting reproduces the equation.
- BC-CON-07003 Families of solutions: One differential equation is satisfied by infinitely many functions, one through each point of the plane it covers.

- BC-SKL-07006 Differentiate a proposed solution and substitute it into the equation: Take the derivative of the candidate and put both into the equation.
- BC-SKL-07007 Confirm that a proposed solution satisfies the initial condition: Check the candidate passes through the given point.
- BC-SKL-07008 Show that a proposed function is not a solution: Point to the place where the two sides disagree.
- BC-SKL-07009 State that a differential equation may have infinitely many solutions: Say that a whole family of functions can satisfy the same equation.

### Prerequisites

- BC-PRQ-07002 -> BC-SKL-07006, supporting, [inferred], Prerequisite for Differentiate a proposed solution and substitute it into the equation.
- BC-SKL-07006 -> BC-SKL-07007, hard_prerequisite, [inferred], Prerequisite for Confirm that a proposed solution satisfies the initial condition.
- BC-PRQ-06005 -> BC-SKL-07007, supporting, [inferred], Prerequisite for Confirm that a proposed solution satisfies the initial condition.
- BC-SKL-07006 -> BC-SKL-07008, hard_prerequisite, [inferred], Prerequisite for Show that a proposed function is not a solution.
- BC-SKL-07006 -> BC-SKL-07009, hard_prerequisite, [inferred], Prerequisite for State that a differential equation may have infinitely many solutions.
- BC-TOP-0205 -> BC-SKL-07006, hard_prerequisite, [inferred], Differentiating a given function, a Unit 2 skill not yet in data/skills.json; the topic id stands in for it.

### Required mathematical knowledge

**Verification.** Hypotheses: a candidate function and a differential equation. Conclusion: the candidate is a solution on an interval when differentiating it and substituting both the function and its derivative turns the equation into a true statement there (BC-EK-FUN-7B1).

**Multiplicity of solutions.** BC-EK-FUN-7B2 reads in full: "There may be infinitely many solutions to a differential equation." This statement is listed among the Fall 2026 clarifications as reworded, and the cached CED text carries the clarified wording (ced:138, ced-clarifications-2026:2).

**Refutation.** One input at which the two sides disagree is enough to show that a candidate is not a solution.

**Notation.** y equal to a candidate expression; substituting into the equation; satisfies the initial condition.

### Representations

Representations in play: BC-REP-01 Symbolic (analytical) expression, BC-REP-06 Differential equation.

Conversions tested: candidate function to a derivative and then to a substitution check (BC-REP-01 to BC-REP-06), and general solution family to one member (BC-REP-01 to BC-REP-01).

### Assessment behaviour

MCQ forms give an equation and four candidate functions and ask which is a solution. FRQ forms use verification as a check embedded in a longer question rather than as its own scored part in 2023 to 2025. Calculator status is no calculator. Conceptual variants ask how many solutions an equation has; computational variants ask for the substitution; justification variants ask for the reason a proposed function fails; multi-concept variants pair verification with an initial condition so that only one member of the family survives.

### Archetypes

- BC-QA-07007 Verification that a function solves a differential equation

### Errors and misconceptions

- BC-ERR-07006 Candidate substituted without being differentiated
- BC-ERR-07007 Initial condition not checked before a particular solution is claimed
- BC-ERR-07008 Failure claimed with no disagreeing input exhibited
- BC-ERR-07009 General solution reported as the only solution
- BC-MIS-07004 A plausible looking function is a solution, severity medium
- BC-MIS-07003 An initial condition is part of the differential equation, severity medium
- BC-MIS-07005 A differential equation has one solution, severity high

### Diagnostic signals

- BC-SIG-07005 Candidate substituted without its derivative
- BC-SIG-07006 Equation verified and the initial condition ignored
- BC-SIG-07007 Negative verdict with nothing exhibited
- BC-SIG-07008 Family treated as a single function

### Adaptive metadata summary

Skills in this topic carry calculator relevance none. Remediation targets named across the topic: BC-PRQ-06005, BC-PRQ-07002, BC-SKL-07006. Every skill record carries the full seven key adaptive block in data/staging/unit-07.skills.json. [inferred]

## 7.3 Sketching Slope Fields

### Official mapping

Topic id BC-TOP-0703, CED code 7.3, name Sketching Slope Fields, scope shared, CED page 139. [verified] (ced:139)

- BC-LO-FUN-7C (FUN-7.C): Estimate solutions to differential equations.
  - BC-EK-FUN-7C1 (FUN-7.C.1): "A slope field is a graphical representation of a differential equation on a finite set of points in the plane."
  - BC-EK-FUN-7C2 (FUN-7.C.2): "Slope fields provide information about the behavior of solutions to first-order differential equations."

Suggested practice skills: BC-MPS-2C (Practice skill 2.C). Weighting pointer: [../exam/exam-blueprint.md](../exam/exam-blueprint.md).

### Concept breakdown

- BC-CON-07004 Slope field as a plot of derivative values: A slope field draws a short segment at each of finitely many points, with the slope the equation assigns to that point.

- BC-SKL-07010 Compute the slope the equation assigns to a given point: Put the coordinates into the right side and get a number.
- BC-SKL-07011 Draw the segments of a slope field at given lattice points: Sketch short lines of the right steepness at the marked points.
- BC-SKL-07012 Identify where the slope field is horizontal: Find the points where the equation gives slope zero.
- BC-SKL-07013 Describe how a field depends on only one of the variables: Notice when the field repeats along rows or along columns.

### Prerequisites

- BC-PRQ-07006 -> BC-SKL-07010, supporting, [inferred], Prerequisite for Compute the slope the equation assigns to a given point.
- BC-PRQ-06005 -> BC-SKL-07010, supporting, [inferred], Prerequisite for Compute the slope the equation assigns to a given point.
- BC-SKL-07010 -> BC-SKL-07011, hard_prerequisite, [inferred], Prerequisite for Draw the segments of a slope field at given lattice points.
- BC-PRQ-07006 -> BC-SKL-07011, supporting, [inferred], Prerequisite for Draw the segments of a slope field at given lattice points.
- BC-SKL-07010 -> BC-SKL-07012, hard_prerequisite, [inferred], Prerequisite for Identify where the slope field is horizontal.
- BC-SKL-07010 -> BC-SKL-07013, hard_prerequisite, [inferred], Prerequisite for Describe how a field depends on only one of the variables.

### Required mathematical knowledge

**Construction.** At each point of a finite grid, evaluate the right side of the differential equation at that point and draw a short segment of that slope centred there (BC-EK-FUN-7C1).

**Zero slope locus.** Segments are horizontal exactly where the right side vanishes, which for an equation of the form a constant multiplied by a difference means where the quantity equals the fixed level.

**Independence.** If the right side does not contain the independent variable, the field is the same along every vertical line; if it does not contain the dependent variable, it is the same along every horizontal line.

**Notation.** a grid of short segments; slope at the point given as an ordered pair.

### Representations

Representations in play: BC-REP-06 Differential equation, BC-REP-07 Slope field, BC-REP-02 Graphical.

Conversions tested: differential equation to a slope value at a named point (BC-REP-06 to BC-REP-01), and differential equation to a drawn field (BC-REP-06 to BC-REP-07).

### Assessment behaviour

MCQ forms ask which field belongs to a given equation, or ask for the slope at a named lattice point. FRQ forms supply the field already drawn and score the use of it rather than its construction (sg-23:9, sg-24:9). Calculator status is no calculator. Conceptual variants ask where the field is horizontal; computational variants ask for a slope value; interpretation variants ask what a row of identical segments says about the equation; multi-concept variants continue into a sketched solution curve.

### Archetypes

- BC-QA-07002 Slope field matched to or built from a differential equation

### Errors and misconceptions

- BC-ERR-07010 Slope evaluated at the wrong lattice point
- BC-ERR-07011 Segments drawn with a uniform tilt
- BC-ERR-07012 Zero slope locus not identified
- BC-ERR-07013 Dependence on a variable misread from the field
- BC-MIS-07006 A slope field shows values of the solution, severity high
- BC-MIS-07007 A horizontal segment marks a maximum of every solution, severity medium

### Diagnostic signals

- BC-SIG-07009 Slope computed at a neighbouring lattice point
- BC-SIG-07010 Field drawn with uniform segments
- BC-SIG-07011 Zero slope locus never identified
- BC-SIG-07012 Dependence pattern misread from the field

### Adaptive metadata summary

Skills in this topic carry calculator relevance none. Remediation targets named across the topic: BC-PRQ-07006, BC-SKL-07010. Every skill record carries the full seven key adaptive block in data/staging/unit-07.skills.json. [inferred]

## 7.4 Reasoning Using Slope Fields

### Official mapping

Topic id BC-TOP-0704, CED code 7.4, name Reasoning Using Slope Fields, scope shared, CED page 140. [verified] (ced:140)

- BC-LO-FUN-7C (FUN-7.C): Estimate solutions to differential equations.
  - BC-EK-FUN-7C3 (FUN-7.C.3): "Solutions to differential equations are functions or families of functions."

Suggested practice skills: BC-MPS-4D (Practice skill 4.D). Weighting pointer: [../exam/exam-blueprint.md](../exam/exam-blueprint.md).

### Concept breakdown

- BC-CON-07005 Solution curves read off a slope field: A solution is a curve that follows the segments, and the field shows how solutions behave without any solving.

- BC-SKL-07014 Sketch a solution curve through a given point on a slope field: Draw a curve from the marked point that follows the segments.
- BC-SKL-07015 Keep a sketched curve on the correct side of an equilibrium level: Do not let the curve cross the line of horizontal segments.
- BC-SKL-07016 Match a slope field to a differential equation: Say which equation could have drawn the field.
- BC-SKL-07017 Describe the long-run behaviour of a solution from the field: Say where the curve is heading as the input grows.
- BC-SKL-07018 Read monotonicity and concavity of a solution from the equation or the field: Use the sign of the derivative and its rate of change to describe the curve.

### Prerequisites

- BC-PRQ-07006 -> BC-SKL-07014, supporting, [inferred], Prerequisite for Sketch a solution curve through a given point on a slope field.
- BC-SKL-07014 -> BC-SKL-07015, hard_prerequisite, [inferred], Prerequisite for Keep a sketched curve on the correct side of an equilibrium level.
- BC-SKL-07012 -> BC-SKL-07015, hard_prerequisite, [inferred], Prerequisite for Keep a sketched curve on the correct side of an equilibrium level.
- BC-SKL-07010 -> BC-SKL-07016, hard_prerequisite, [inferred], Prerequisite for Match a slope field to a differential equation.
- BC-SKL-07013 -> BC-SKL-07016, hard_prerequisite, [inferred], Prerequisite for Match a slope field to a differential equation.
- BC-SKL-07014 -> BC-SKL-07017, hard_prerequisite, [inferred], Prerequisite for Describe the long-run behaviour of a solution from the field.
- BC-SKL-07012 -> BC-SKL-07017, hard_prerequisite, [inferred], Prerequisite for Describe the long-run behaviour of a solution from the field.
- BC-SKL-07010 -> BC-SKL-07018, hard_prerequisite, [inferred], Prerequisite for Read monotonicity and concavity of a solution from the equation or the field.
- BC-TOP-0301 -> BC-SKL-07018, hard_prerequisite, [inferred], The chain rule applied to the dependent variable, a Unit 3 skill not yet in data/skills.json; the topic id stands in for it.
- BC-SKL-05014 -> BC-SKL-07018, supporting, [inferred], Reading monotonicity from the sign of a derivative expression, the Unit 5 skill this one applies to a solution never written down.
- BC-SKL-05030 -> BC-SKL-07018, supporting, [inferred], Reading concavity from the sign of a second derivative, the Unit 5 skill this one applies to a solution never written down.

### Required mathematical knowledge

**Solution curve.** A solution curve through a point follows the segments of the field, so it is tangent to the segment at every point it passes (BC-EK-FUN-7C3).

**Sketching standard.** The 2023 guideline required the drawn curve to pass through the stated point, to extend reasonably close to the left and right edges of the given rectangle, to avoid obvious conflicts with the drawn segments, and to stay entirely on the correct side of the horizontal segments that mark the equilibrium level (sg-23:9). Only the portion inside the given field is considered.

**Reading behaviour.** The field shows where solutions rise and fall, where they level off, and whether they approach a horizontal asymptote, all without solving.

**Notation.** the solution curve through the point; the equilibrium level; the given rectangle.

### Representations

Representations in play: BC-REP-06 Differential equation, BC-REP-07 Slope field, BC-REP-02 Graphical.

Conversions tested: slope field to a sketched solution curve (BC-REP-07 to BC-REP-02), and slope field to a matched differential equation (BC-REP-07 to BC-REP-06).

### Assessment behaviour

MCQ forms ask which equation produced a drawn field, or which sketched curve is a solution. FRQ forms open a differential equation question with a one point sketch on the supplied field, and the point is awarded on the four conditions the guideline lists (sg-23:9, sg-24:9). Calculator status is no calculator. Conceptual variants ask about long-run behaviour; computational variants ask for the slope at a point; interpretation variants ask what the levelling off means for the modelled quantity; justification variants ask which field belongs to which equation and why; multi-concept variants continue into a tangent line approximation or a separation.

### Archetypes

- BC-QA-07001 Solution curve sketched on a supplied slope field
- BC-QA-07002 Slope field matched to or built from a differential equation

### Errors and misconceptions

- BC-ERR-07014 Solution curve drawn without following the segments
- BC-ERR-99024 Chief Reader error record, see data/errors.json
- BC-ERR-07015 Solution curve drawn across an equilibrium level
- BC-ERR-07016 Field matched on visual impression
- BC-ERR-07017 Long-run behaviour asserted with no reference to the field or the equation
- BC-ERR-07018 Direction of an approximation claimed from increase or decrease
- BC-ERR-99020 Chief Reader error record, see data/errors.json
- BC-MIS-07008 A solution curve may be drawn freely through the field, severity high
- BC-MIS-07009 A solution may cross an equilibrium level, severity high
- BC-MIS-07006 A slope field shows values of the solution, severity high
- BC-MIS-07010 The direction of an approximation follows from increase or decrease, severity high

### Diagnostic signals

- BC-SIG-07013 Curve through the right point conflicting with the segments
- BC-SIG-07014 Curve drawn across the equilibrium level
- BC-SIG-07015 Equation matched on the look of the field
- BC-SIG-07016 Long-run claim with no supporting feature named
- BC-SIG-07017 Second derivative left in terms of the first

### Adaptive metadata summary

Skills in this topic carry calculator relevance none. Remediation targets named across the topic: BC-PRQ-07006, BC-SKL-07010, BC-SKL-07014. Every skill record carries the full seven key adaptive block in data/staging/unit-07.skills.json. [inferred]

## 7.5 Approximating Solutions Using Euler's Method

### Official mapping

Topic id BC-TOP-0705, CED code 7.5, name Approximating Solutions Using Euler's Method, scope BC_only, CED page 141. [verified] (ced:141)

- BC-LO-FUN-7C (FUN-7.C): Estimate solutions to differential equations.
  - BC-EK-FUN-7C4 (FUN-7.C.4): "Euler's method provides a procedure for approximating a solution to a differential equation or a point on a solution curve."

Suggested practice skills: BC-MPS-1E (Practice skill 1.E). Weighting pointer: [../exam/exam-blueprint.md](../exam/exam-blueprint.md).

### Concept breakdown

- BC-CON-07006 Euler's method as repeated local linearisation: Euler's method steps along tangent lines, using each new approximation as the starting point for the next step.

- BC-SKL-07019 Determine the step size from the interval and the number of steps: Divide the length of the interval by how many steps are asked for.
- BC-SKL-07020 Execute the first Euler step from the initial condition: Add the step size times the slope at the starting point.
- BC-SKL-07021 Use the previous approximation as the input for the next step: Start the second step from the value the first step produced.
- BC-SKL-07022 Lay out the computation as a labelled step table: Show the steps in a table with the columns named.
- BC-SKL-07023 Decide the direction of the Euler error from concavity: Say whether the estimate is too high or too low from the bending of the solution.

### Prerequisites

- BC-PRQ-07005 -> BC-SKL-07019, supporting, [inferred], Prerequisite for Determine the step size from the interval and the number of steps.
- BC-SKL-07019 -> BC-SKL-07020, hard_prerequisite, [inferred], Prerequisite for Execute the first Euler step from the initial condition.
- BC-SKL-07010 -> BC-SKL-07020, hard_prerequisite, [inferred], Prerequisite for Execute the first Euler step from the initial condition.
- BC-SKL-07020 -> BC-SKL-07021, hard_prerequisite, [inferred], Prerequisite for Use the previous approximation as the input for the next step.
- BC-PRQ-07005 -> BC-SKL-07021, supporting, [inferred], Prerequisite for Use the previous approximation as the input for the next step.
- BC-SKL-07021 -> BC-SKL-07022, hard_prerequisite, [inferred], Prerequisite for Lay out the computation as a labelled step table.
- BC-SKL-07020 -> BC-SKL-07023, hard_prerequisite, [inferred], Prerequisite for Decide the direction of the Euler error from concavity.
- BC-SKL-07018 -> BC-SKL-07023, hard_prerequisite, [inferred], Prerequisite for Decide the direction of the Euler error from concavity.
- BC-TOP-0406 -> BC-SKL-07020, supporting, [inferred], Tangent line approximation, a Unit 4 skill not yet in data/skills.json; the topic id stands in for it.
- BC-TOP-0406 -> BC-SKL-07023, supporting, [inferred], Reading an approximation as an over or under estimate through concavity, a Unit 4 idea not yet in data/skills.json; the topic id stands in for it.
- BC-SKL-05046 -> BC-SKL-07023, supporting, [inferred], Translating a second derivative statement into a statement about shape, the Unit 5 skill behind the direction of an Euler error.

### Required mathematical knowledge

**Procedure.** From a point, the next approximation is the current output plus the step size multiplied by the right side of the differential equation evaluated at the current point; the new point then replaces the old one (BC-EK-FUN-7C4).

**Step size.** With a stated number of equal steps across an interval, the step size is the length of the interval divided by the number of steps.

**Scoring shape.** Two points in both years read: one for demonstrating the steps with the correct initial condition, step size, and derivative expression, one for the answer with supporting work. The 2024 guideline asked for two demonstrated steps with at most one error and withheld the answer point if there was an error; the 2025 guideline asked only that the first step be demonstrated correctly and made subsequent simplification or rounding errors irrelevant to that point. Both allow the work to be laid out as a labelled table, and both allow an imported incorrect earlier value to earn the answer point with a consistent result (sg-24:17, sg-25:23).

**Accuracy direction.** Because each step follows a tangent line, a solution that is concave up over the interval is underestimated and one that is concave down is overestimated.

**Notation.** a table with columns for the input, the output, and the increment; the phrase two steps of equal size.

### Representations

Representations in play: BC-REP-03 Numerical table, BC-REP-06 Differential equation, BC-REP-01 Symbolic (analytical) expression.

Conversions tested: differential equation plus an initial condition to a table of approximations (BC-REP-06 to BC-REP-03), and a step table to a single approximate value (BC-REP-03 to BC-REP-01).

### Assessment behaviour

MCQ forms give an equation, an initial point, and a step size and ask for the approximation after one or two steps. FRQ forms ask for two steps of equal size and score the demonstration and the answer separately (sg-24:17, sg-25:23). Calculator status is no calculator in both instances read. Conceptual variants ask whether the approximation is high or low; computational variants ask for the value; justification variants ask for the concavity reason behind the direction of the error; multi-concept variants take the derivative expression from an earlier part of the same question.

### Archetypes

- BC-QA-07004 Euler's method over two steps of equal size

### Errors and misconceptions

- BC-ERR-07019 Step size taken as the whole interval
- BC-ERR-99026 Chief Reader error record, see data/errors.json
- BC-ERR-07020 First Euler step taken with the wrong initial values
- BC-ERR-07021 Second Euler step restarted from the initial value
- BC-ERR-07022 Approximation reported with no visible steps
- BC-ERR-99021 Chief Reader error record, see data/errors.json
- BC-ERR-07023 Euler direction claimed with no concavity statement
- BC-ERR-99020 Chief Reader error record, see data/errors.json
- BC-MIS-07011 Euler's method evaluates the derivative once, severity high
- BC-MIS-07012 Each Euler step restarts from the initial value, severity high
- BC-MIS-07013 An answer needs no visible steps, severity medium
- BC-MIS-07010 The direction of an approximation follows from increase or decrease, severity high

### Diagnostic signals

- BC-SIG-07018 Whole interval used as one step
- BC-SIG-07019 First step taken from the wrong point
- BC-SIG-07020 Second step evaluated at the initial point
- BC-SIG-07021 Bare value with no steps or labels
- BC-SIG-07022 Direction claimed with no concavity statement

### Adaptive metadata summary

Skills in this topic carry calculator relevance none. Remediation targets named across the topic: BC-PRQ-07005, BC-SKL-07019, BC-SKL-07020, BC-SKL-07021. Every skill record carries the full seven key adaptive block in data/staging/unit-07.skills.json. [inferred]

## 7.6 Finding General Solutions Using Separation of Variables

### Official mapping

Topic id BC-TOP-0706, CED code 7.6, name Finding General Solutions Using Separation of Variables, scope shared, CED page 142. [verified] (ced:142)

- BC-LO-FUN-7D (FUN-7.D): Determine general solutions to differential equations.
  - BC-EK-FUN-7D1 (FUN-7.D.1): "Some differential equations can be solved by separation of variables."
  - BC-EK-FUN-7D2 (FUN-7.D.2): "Antidifferentiation can be used to find general solutions to differential equations."

Suggested practice skills: BC-MPS-1E (Practice skill 1.E). Weighting pointer: [../exam/exam-blueprint.md](../exam/exam-blueprint.md).

### Concept breakdown

- BC-CON-07007 Separation of variables: When the equation factors into a part in one variable and a part in the other, both sides can be antidifferentiated separately.

- BC-SKL-07024 Separate the variables onto opposite sides of the equation: Move all the terms in one variable to one side with its differential.
- BC-SKL-07025 Antidifferentiate both sides of the separated equation: Integrate each side with respect to its own variable.
- BC-SKL-07026 Include a single constant of integration: Add one constant, on one side only.
- BC-SKL-07027 Solve the resulting equation for the dependent variable: Rearrange to get the dependent variable by itself.
- BC-SKL-07028 Recognise when a differential equation is not separable: Notice when the right side will not factor into the two pieces.

### Prerequisites

- BC-PRQ-07002 -> BC-SKL-07024, supporting, [inferred], Prerequisite for Separate the variables onto opposite sides of the equation.
- BC-SKL-07024 -> BC-SKL-07025, hard_prerequisite, [inferred], Prerequisite for Antidifferentiate both sides of the separated equation.
- BC-PRQ-06003 -> BC-SKL-07025, supporting, [inferred], Prerequisite for Antidifferentiate both sides of the separated equation.
- BC-SKL-07025 -> BC-SKL-07026, hard_prerequisite, [inferred], Prerequisite for Include a single constant of integration.
- BC-SKL-07026 -> BC-SKL-07027, hard_prerequisite, [inferred], Prerequisite for Solve the resulting equation for the dependent variable.
- BC-PRQ-07001 -> BC-SKL-07027, supporting, [inferred], Prerequisite for Solve the resulting equation for the dependent variable.
- BC-SKL-07024 -> BC-SKL-07028, hard_prerequisite, [inferred], Prerequisite for Recognise when a differential equation is not separable.
- BC-SKL-06034 -> BC-SKL-07025, hard_prerequisite, [inferred], Evaluating an antiderivative, the Unit 6 skill both sides of a separated equation need.
- BC-SKL-06047 -> BC-SKL-07025, supporting, [inferred], Antidifferentiation by substitution, needed when the independent side of a separated equation is a composite.

### Required mathematical knowledge

**Separation.** Hypotheses: the right side factors as a function of the independent variable multiplied by a function of the dependent variable. Conclusion: the equation can be rewritten with all dependent variable terms and the differential of the dependent variable on one side and all independent variable terms and its differential on the other (BC-EK-FUN-7D1).

**Antidifferentiation.** Antidifferentiating both sides produces the general solution, with a single constant of integration collected on one side (BC-EK-FUN-7D2).

**Scoring shape.** The 2023 guideline split four points as separating the variables, finding the antiderivatives, handling the constant of integration with the initial condition, and solving for the dependent variable. A response with no separation earns none of the four; a response with no constant of integration earns at most the first two; each later point requires the earlier ones; an antiderivative written without absolute value symbols stays eligible for all four (sg-23:12). The 2024 guideline split five points, awarding the two antiderivatives separately (sg-24:11).

**Notation.** the separated form with a differential on each side; a single constant C; the natural logarithm of an absolute value.

### Representations

Representations in play: BC-REP-01 Symbolic (analytical) expression, BC-REP-06 Differential equation.

Conversions tested: differential equation to separated form (BC-REP-06 to BC-REP-01), and antiderivative equation to an explicit function (BC-REP-01 to BC-REP-01).

### Assessment behaviour

MCQ forms ask for the general solution of a short separable equation. FRQ forms ask for a particular solution and score the separation, the antiderivatives, the constant, and the final solving as distinct points (sg-23:11, sg-23:12, sg-24:11). Calculator status is no calculator. Conceptual variants ask whether a given equation is separable; computational variants ask for the general solution; justification variants ask why the separation is legitimate for the given form; multi-concept variants attach the initial condition and the domain in the same part.

### Archetypes

- BC-QA-07003 Particular solution by separation of variables

### Errors and misconceptions

- BC-ERR-07024 Variables not separated before antidifferentiating
- BC-ERR-99014 Chief Reader error record, see data/errors.json
- BC-ERR-99006 Chief Reader error record, see data/errors.json
- BC-ERR-07025 Only one side antidifferentiated
- BC-ERR-07026 Constant of integration omitted
- BC-ERR-07027 Answer left implicit when an expression was asked for
- BC-ERR-07028 Separation attempted on an equation that does not factor
- BC-MIS-07014 Any differential equation can be separated, severity high
- BC-MIS-07015 Antidifferentiating one side is enough, severity high
- BC-MIS-07016 The constant of integration is optional, severity high
- BC-MIS-07017 An implicit relation is a finished solution, severity medium

### Diagnostic signals

- BC-SIG-07023 Integral signs written with both variables on one side
- BC-SIG-07024 One side antidifferentiated correctly and the other untouched
- BC-SIG-07025 Antiderivative equation with no constant
- BC-SIG-07026 Correct antiderivative equation left unsolved
- BC-SIG-07027 Separation attempted on a non-separable equation

### Adaptive metadata summary

Skills in this topic carry calculator relevance none. Remediation targets named across the topic: BC-PRQ-06003, BC-PRQ-07001, BC-PRQ-07002, BC-SKL-07024, BC-SKL-07025. Every skill record carries the full seven key adaptive block in data/staging/unit-07.skills.json. [inferred]

## 7.7 Finding Particular Solutions Using Initial Conditions and Separation of Variables

### Official mapping

Topic id BC-TOP-0707, CED code 7.7, name Finding Particular Solutions Using Initial Conditions and Separation of Variables, scope shared, CED page 143. [verified] (ced:143)

- BC-LO-FUN-7E (FUN-7.E): Determine particular solutions to differential equations.
  - BC-EK-FUN-7E1 (FUN-7.E.1): "A general solution may describe infinitely many solutions to a differential equation. There is only one particular solution passing through a given point."
  - BC-EK-FUN-7E2 (FUN-7.E.2): "The function F defined by F(x) = y sub 0 + the integral from a to x of f(t) dt is a particular solution to the differential equation dy/dx = f(x), satisfying F(a) = y sub 0."
  - BC-EK-FUN-7E3 (FUN-7.E.3): "Solutions to differential equations may be subject to domain restrictions."

Suggested practice skills: BC-MPS-1E (Practice skill 1.E). Weighting pointer: [../exam/exam-blueprint.md](../exam/exam-blueprint.md).

### Concept breakdown

- BC-CON-07008 Particular solution selected by an initial condition: The initial condition picks one curve out of the family and settles the constant and the sign.
- BC-CON-07009 Domain restrictions on a particular solution: A particular solution is valid only on the interval around the initial point where the expression stays defined.

- BC-SKL-07029 Substitute the initial condition to evaluate the constant of integration: Put the given point in and solve for the constant.
- BC-SKL-07030 Resolve an absolute value or a sign ambiguity from the initial condition: Use the given point to decide which sign applies.
- BC-SKL-07031 State the domain restriction the initial condition selects: Say on which interval the particular solution is valid.
- BC-SKL-07032 Write a particular solution as an accumulation function: Express the solution as the starting value plus an integral.
- BC-SKL-07033 Distinguish the general solution family from the particular solution: Say which answer carries a constant and which does not.

### Prerequisites

- BC-SKL-07026 -> BC-SKL-07029, hard_prerequisite, [inferred], Prerequisite for Substitute the initial condition to evaluate the constant of integration.
- BC-SKL-07004 -> BC-SKL-07029, hard_prerequisite, [inferred], Prerequisite for Substitute the initial condition to evaluate the constant of integration.
- BC-SKL-07029 -> BC-SKL-07030, hard_prerequisite, [inferred], Prerequisite for Resolve an absolute value or a sign ambiguity from the initial condition.
- BC-PRQ-07004 -> BC-SKL-07030, supporting, [inferred], Prerequisite for Resolve an absolute value or a sign ambiguity from the initial condition.
- BC-SKL-07027 -> BC-SKL-07031, hard_prerequisite, [inferred], Prerequisite for State the domain restriction the initial condition selects.
- BC-PRQ-05003 -> BC-SKL-07031, supporting, [inferred], Prerequisite for State the domain restriction the initial condition selects.
- BC-SKL-07004 -> BC-SKL-07032, hard_prerequisite, [inferred], Prerequisite for Write a particular solution as an accumulation function.
- BC-SKL-06044 -> BC-SKL-07032, hard_prerequisite, [inferred], Prerequisite for Write a particular solution as an accumulation function.
- BC-SKL-07029 -> BC-SKL-07033, hard_prerequisite, [inferred], Prerequisite for Distinguish the general solution family from the particular solution.
- BC-SKL-07009 -> BC-SKL-07033, hard_prerequisite, [inferred], Prerequisite for Distinguish the general solution family from the particular solution.
- BC-SKL-06044 -> BC-SKL-07029, hard_prerequisite, [inferred], Determining the constant of integration from an initial condition, recorded in Unit 6.

### Required mathematical knowledge

**Uniqueness through a point.** A general solution describes infinitely many solutions and exactly one of them passes through a given point (BC-EK-FUN-7E1).

**Accumulation form.** When the right side depends only on the independent variable, the particular solution is the initial value plus the definite integral of the right side from the initial input to the variable input (BC-EK-FUN-7E2). This is the bridge to the accumulation function skills recorded in Unit 6.

**Sign and branch.** The initial condition also settles the sign inside an absolute value. The 2023 solution used the stated bound on the quantity to remove the absolute value, and the 2024 solution used the initial value to conclude the enclosed expression was positive (sg-23:11, sg-24:11).

**Timing of the substitution.** The 2023 guideline gave the constant point for including the constant in an equation and substituting the initial values into it, and made the final solving point available only after the first three (sg-23:12).

**Domain restriction.** A particular solution is taken on the largest interval containing the initial input on which the expression is defined and continuous (BC-EK-FUN-7E3).

**Notation.** the particular solution; F(a) equal to the initial value; the interval containing the initial input.

### Representations

Representations in play: BC-REP-01 Symbolic (analytical) expression, BC-REP-05 Contextual model, BC-REP-06 Differential equation.

Conversions tested: general solution plus a point to one particular solution (BC-REP-01 to BC-REP-01), and differential equation in the independent variable alone to an accumulation function (BC-REP-06 to BC-REP-01).

### Assessment behaviour

MCQ forms give a general solution and a point and ask for the particular solution, or ask for the domain of a particular solution. FRQ forms ask for the particular solution in context and score the constant handling and the final explicit form as separate points (sg-23:12, sg-24:11). Calculator status is no calculator. Conceptual variants ask how many solutions pass through a point; computational variants ask for the expression; interpretation variants ask what the solution says about the modelled quantity; justification variants ask why the domain is restricted; multi-concept variants continue from an earlier slope field or tangent line part of the same question.

### Archetypes

- BC-QA-07003 Particular solution by separation of variables
- BC-QA-07011 Particular solution with a domain restriction or an accumulation form

### Errors and misconceptions

- BC-ERR-07029 Constant evaluated after the exponentiation instead of before
- BC-ERR-99014 Chief Reader error record, see data/errors.json
- BC-ERR-07030 Absolute value dropped without checking the sign
- BC-ERR-99037 Chief Reader error record, see data/errors.json
- BC-ERR-07031 Domain restriction omitted or wrongly chosen
- BC-ERR-07032 Accumulation form written without the initial value or the differential
- BC-ERR-99006 Chief Reader error record, see data/errors.json
- BC-ERR-07033 General and particular solutions interchanged
- BC-MIS-07016 The constant of integration is optional, severity high
- BC-MIS-07018 An absolute value can be dropped without checking, severity medium
- BC-MIS-07019 A solution formula holds on every input, severity medium
- BC-MIS-07020 A particular solution must be written in closed form, severity medium
- BC-MIS-07005 A differential equation has one solution, severity high

### Diagnostic signals

- BC-SIG-07028 Initial condition substituted after exponentiating
- BC-SIG-07029 Branch chosen against the initial condition
- BC-SIG-07030 Solution reported with no interval
- BC-SIG-07031 Accumulation form written without the initial value
- BC-SIG-07032 Answer of the wrong kind for the question

### Adaptive metadata summary

Skills in this topic carry calculator relevance none. Remediation targets named across the topic: BC-PRQ-05003, BC-PRQ-07004, BC-SKL-07004, BC-SKL-07026, BC-SKL-07029. Every skill record carries the full seven key adaptive block in data/staging/unit-07.skills.json. [inferred]

## 7.8 Exponential Models with Differential Equations

### Official mapping

Topic id BC-TOP-0708, CED code 7.8, name Exponential Models with Differential Equations, scope shared, CED page 144. [verified] (ced:144)

- BC-LO-FUN-7F (FUN-7.F): Interpret the meaning of a differential equation and its variables in context.
  - BC-EK-FUN-7F1 (FUN-7.F.1): "Specific applications of finding general and particular solutions to differential equations include motion along a line and exponential growth and decay."
  - BC-EK-FUN-7F2 (FUN-7.F.2): "The model for exponential growth and decay that arises from the statement “The rate of change of a quantity is proportional to the size of the quantity” is dy/dt = ky."
- BC-LO-FUN-7G (FUN-7.G): Determine general and particular solutions for problems involving differential equations in context.
  - BC-EK-FUN-7G1 (FUN-7.G.1): "The exponential growth and decay model, dy/dt = ky, with initial condition y = y sub 0 when t = 0, has solutions of the form y = y sub 0 e^(kt)."

Suggested practice skills: BC-MPS-3G (Practice skill 3.G). Weighting pointer: [../exam/exam-blueprint.md](../exam/exam-blueprint.md).

### Concept breakdown

- BC-CON-07010 Exponential growth and decay model: When the rate of change is proportional to the amount present, the amount is an exponential function of the independent variable.

- BC-SKL-07034 Write the exponential model from a proportionality statement: Turn rate proportional to amount into the standard equation.
- BC-SKL-07035 Produce the exponential solution from the model and the initial value: Write the solution as the starting amount times an exponential.
- BC-SKL-07036 Determine the constant of proportionality from a second data pair: Use another known value to pin down the constant.
- BC-SKL-07037 Interpret the sign and size of the constant in context: Say what the constant means for the situation.
- BC-SKL-07038 Apply a differential equation model to motion along a line: Use the same machinery when the quantity is a position or a velocity.

### Prerequisites

- BC-SKL-07001 -> BC-SKL-07034, hard_prerequisite, [inferred], Prerequisite for Write the exponential model from a proportionality statement.
- BC-PRQ-07003 -> BC-SKL-07034, supporting, [inferred], Prerequisite for Write the exponential model from a proportionality statement.
- BC-SKL-07034 -> BC-SKL-07035, hard_prerequisite, [inferred], Prerequisite for Produce the exponential solution from the model and the initial value.
- BC-SKL-07027 -> BC-SKL-07035, hard_prerequisite, [inferred], Prerequisite for Produce the exponential solution from the model and the initial value.
- BC-SKL-07029 -> BC-SKL-07035, hard_prerequisite, [inferred], Prerequisite for Produce the exponential solution from the model and the initial value.
- BC-SKL-07035 -> BC-SKL-07036, hard_prerequisite, [inferred], Prerequisite for Determine the constant of proportionality from a second data pair.
- BC-PRQ-07001 -> BC-SKL-07036, supporting, [inferred], Prerequisite for Determine the constant of proportionality from a second data pair.
- BC-PRQ-06003 -> BC-SKL-07036, supporting, [inferred], Prerequisite for Determine the constant of proportionality from a second data pair.
- BC-SKL-07036 -> BC-SKL-07037, hard_prerequisite, [inferred], Prerequisite for Interpret the sign and size of the constant in context.
- BC-SKL-07003 -> BC-SKL-07037, hard_prerequisite, [inferred], Prerequisite for Interpret the sign and size of the constant in context.
- BC-SKL-07029 -> BC-SKL-07038, hard_prerequisite, [inferred], Prerequisite for Apply a differential equation model to motion along a line.
- BC-SKL-07032 -> BC-SKL-07038, hard_prerequisite, [inferred], Prerequisite for Apply a differential equation model to motion along a line.

### Required mathematical knowledge

**Model and solution.** Hypotheses: the rate of change of a quantity is proportional to the size of the quantity, with the value y sub 0 at input zero. Conclusion: the equation is dy/dt equal to k y and the solution is y equal to y sub 0 multiplied by e to the k t (BC-EK-FUN-7F2, BC-EK-FUN-7G1).

**Sign of the constant.** A positive constant gives growth and a negative one gives decay; the size of the constant sets how fast.

**Determining the constant.** One further data pair beyond the initial condition determines the constant through a logarithm.

**Other applications.** Motion along a line is the other application the CED names for particular solutions in context (BC-EK-FUN-7F1).

**Notation.** dy/dt = ky; y sub 0; e to the k t; half-life and doubling behaviour expressed through the constant.

### Representations

Representations in play: BC-REP-01 Symbolic (analytical) expression, BC-REP-05 Contextual model, BC-REP-06 Differential equation.

Conversions tested: verbal proportionality to an equation and then to an exponential formula (BC-REP-04 to BC-REP-01), and two data pairs to a determined constant (BC-REP-03 to BC-REP-01).

### Assessment behaviour

MCQ forms ask for the amount remaining after a stated input, or for the constant from two data pairs. FRQ forms embed the model in a context and score the separation, the constant, and the solved form, as in the general separable case. Calculator status is either; a numerical solve for the constant needs technology. Conceptual variants ask what the sign of the constant means; computational variants ask for a value; interpretation variants ask what the model says about the situation with units; justification variants ask why the model is exponential rather than linear; multi-concept variants pair the model with a limit as the independent variable grows.

### Archetypes

- BC-QA-07008 Exponential growth or decay model solved and interpreted

### Errors and misconceptions

- BC-ERR-07034 Exponential model written as a linear one
- BC-ERR-07035 Exponential solution written with the constant in the wrong place
- BC-ERR-07036 Rate constant read from a single data pair
- BC-ERR-07037 Interpretation of the rate constant omits units or direction
- BC-ERR-99005 Chief Reader error record, see data/errors.json
- BC-ERR-99027 Chief Reader error record, see data/errors.json
- BC-ERR-07038 Motion model treated as though the derivative were the position
- BC-MIS-07001 Proportional to means equal to, severity high
- BC-MIS-07021 Proportional growth is linear growth, severity high
- BC-MIS-07022 The constant of proportionality can be read off one data pair, severity medium
- BC-MIS-07023 A numerical answer is a complete interpretation, severity medium
- BC-MIS-07020 A particular solution must be written in closed form, severity medium

### Diagnostic signals

- BC-SIG-07033 Linear model offered for proportional growth
- BC-SIG-07034 Exponential written with the constants misplaced
- BC-SIG-07035 Rate constant produced from the initial condition alone
- BC-SIG-07036 Constant reported with no direction or units
- BC-SIG-07037 Motion quantity reported one derivative away

### Adaptive metadata summary

Skills in this topic carry calculator relevance none, optional. Remediation targets named across the topic: BC-PRQ-07001, BC-PRQ-07003, BC-SKL-07029, BC-SKL-07034, BC-SKL-07036. Every skill record carries the full seven key adaptive block in data/staging/unit-07.skills.json. [inferred]

## 7.9 Logistic Models with Differential Equations

### Official mapping

Topic id BC-TOP-0709, CED code 7.9, name Logistic Models with Differential Equations, scope BC_only, CED page 145. [verified] (ced:145)

- BC-LO-FUN-7H (FUN-7.H): Interpret the meaning of the logistic growth model in context.
  - BC-EK-FUN-7H1 (FUN-7.H.1): "The model for logistic growth that arises from the statement “The rate of change of a quantity is jointly proportional to the size of the quantity and the difference between the quantity and the carrying capacity” is dy/dt = ky(a - y)."
  - BC-EK-FUN-7H2 (FUN-7.H.2): "The logistic differential equation and initial conditions can be interpreted without solving the differential equation."
  - BC-EK-FUN-7H3 (FUN-7.H.3): "The limiting value (carrying capacity) of a logistic differential equation as the independent variable approaches infinity can be determined using the logistic growth model and initial conditions."
  - BC-EK-FUN-7H4 (FUN-7.H.4): "The value of the dependent variable in a logistic differential equation at the point when it is changing fastest can be determined using the logistic growth model and initial conditions."

Suggested practice skills: BC-MPS-3F (Practice skill 3.F). Weighting pointer: [../exam/exam-blueprint.md](../exam/exam-blueprint.md).

### Concept breakdown

- BC-CON-07011 Logistic differential equation: When growth is limited, the rate depends on both the amount present and how much room is left.
- BC-CON-07012 Carrying capacity and the point of fastest change: A logistic model has a ceiling, and the quantity grows fastest when it is halfway there.

- BC-SKL-07039 Write the logistic equation from a joint proportionality statement: Turn jointly proportional to the amount and the room left into an equation.
- BC-SKL-07040 Identify the carrying capacity from the form of the equation: Read the ceiling straight off the equation.
- BC-SKL-07041 Determine the limiting value without solving the equation: Say where the quantity is heading, using the equation and the starting value.
- BC-SKL-07042 Determine the value at which the quantity changes fastest: Find where the rate is largest, which is half of the ceiling.
- BC-SKL-07043 Interpret a logistic model in context: Say what the equation means for the population being modelled.

### Prerequisites

- BC-PRQ-07003 -> BC-SKL-07039, supporting, [inferred], Prerequisite for Write the logistic equation from a joint proportionality statement.
- BC-SKL-07001 -> BC-SKL-07039, hard_prerequisite, [inferred], Prerequisite for Write the logistic equation from a joint proportionality statement.
- BC-SKL-07039 -> BC-SKL-07040, hard_prerequisite, [inferred], Prerequisite for Identify the carrying capacity from the form of the equation.
- BC-PRQ-05001 -> BC-SKL-07040, supporting, [inferred], Prerequisite for Identify the carrying capacity from the form of the equation.
- BC-SKL-07040 -> BC-SKL-07041, hard_prerequisite, [inferred], Prerequisite for Determine the limiting value without solving the equation.
- BC-SKL-07017 -> BC-SKL-07041, hard_prerequisite, [inferred], Prerequisite for Determine the limiting value without solving the equation.
- BC-SKL-07040 -> BC-SKL-07042, hard_prerequisite, [inferred], Prerequisite for Determine the value at which the quantity changes fastest.
- BC-SKL-05052 -> BC-SKL-07042, hard_prerequisite, [inferred], Prerequisite for Determine the value at which the quantity changes fastest.
- BC-SKL-07041 -> BC-SKL-07043, hard_prerequisite, [inferred], Prerequisite for Interpret a logistic model in context.
- BC-SKL-07042 -> BC-SKL-07043, hard_prerequisite, [inferred], Prerequisite for Interpret a logistic model in context.
- BC-SKL-07003 -> BC-SKL-07043, hard_prerequisite, [inferred], Prerequisite for Interpret a logistic model in context.
- BC-SKL-05052 -> BC-SKL-07042, hard_prerequisite, [inferred], Differentiating an objective and solving for critical points, the Unit 5 skill that maximises the logistic rate.

### Required mathematical knowledge

**Model.** The statement that the rate of change is jointly proportional to the quantity and to the difference between the quantity and the carrying capacity gives the equation with the derivative equal to a constant multiplied by the quantity multiplied by the difference between the carrying capacity and the quantity (BC-EK-FUN-7H1).

**Reasoning without solving.** BC-EK-FUN-7H2 states that the equation and the initial conditions can be interpreted without solving. The carrying capacity and the value at which the quantity changes fastest both follow from the equation alone (BC-EK-FUN-7H3, BC-EK-FUN-7H4).

**Carrying capacity.** The right side vanishes at zero and at the carrying capacity, so those are the equilibrium levels; a solution starting strictly between them increases toward the carrying capacity, which is therefore the limit as the independent variable grows without bound.

**Fastest change.** The right side is a quadratic in the quantity with zeros at zero and at the carrying capacity, so it is largest at half the carrying capacity, which is where the quantity changes fastest and where the solution has a point of inflection.

**Notation.** dy/dt = ky(a - y); carrying capacity a; half of the carrying capacity; the limit as t grows without bound.

### Representations

Representations in play: BC-REP-04 Verbal description, BC-REP-05 Contextual model, BC-REP-06 Differential equation.

Conversions tested: verbal joint proportionality to a logistic equation (BC-REP-04 to BC-REP-06), and logistic equation to a limiting value and a fastest change value (BC-REP-06 to BC-REP-01).

### Assessment behaviour

MCQ forms give a logistic equation and ask for the carrying capacity or for the value at which the quantity grows fastest. FRQ forms ask for the limit and the fastest change value with a reason drawn from the equation, and no part in 2023 to 2025 asked for the logistic model to be solved. Calculator status is either. Conceptual variants ask what the carrying capacity means in the situation; computational variants ask for the two values; interpretation variants ask what the model says about the modelled population; justification variants require the reason to come from the equation rather than from a solved formula; multi-concept variants pair the limit with a concavity statement about the solution.

### Archetypes

- BC-QA-07009 Logistic model interpreted without solving

### Errors and misconceptions

- BC-ERR-07039 Logistic equation written without the limiting factor
- BC-ERR-07040 Carrying capacity read from the wrong factor
- BC-ERR-07041 Limiting value asserted with no reference to the sign of the rate
- BC-ERR-07044 Logistic equation solved where reasoning from it was asked for
- BC-ERR-99035 Chief Reader error record, see data/errors.json
- BC-ERR-07042 Fastest change value reported as the carrying capacity
- BC-ERR-07043 Logistic interpretation omits the units or the modelled quantity
- BC-ERR-99027 Chief Reader error record, see data/errors.json
- BC-ERR-99005 Chief Reader error record, see data/errors.json
- BC-MIS-07024 The logistic model is the exponential model with a harmless extra factor, severity high
- BC-MIS-07025 The carrying capacity must be found by solving the equation, severity high
- BC-MIS-07026 The limit of a solution needs the solution formula, severity high
- BC-MIS-07027 The quantity changes fastest at the carrying capacity, severity high
- BC-MIS-07023 A numerical answer is a complete interpretation, severity medium

### Diagnostic signals

- BC-SIG-07038 Logistic equation written without the limiting factor
- BC-SIG-07039 Wrong factor read as the carrying capacity
- BC-SIG-07040 Correct limit with no sign argument
- BC-SIG-07041 Fastest change reported at the capacity
- BC-SIG-07042 Two correct values with no interpretation

### Adaptive metadata summary

Skills in this topic carry calculator relevance none. Remediation targets named across the topic: BC-PRQ-05001, BC-PRQ-07003, BC-SKL-07040, BC-SKL-07041. Every skill record carries the full seven key adaptive block in data/staging/unit-07.skills.json. [inferred]

## Cross-unit connections

Cross-unit edges use BC-TOP ids as the node on the other unit's side where no skill exists in data/skills.json yet; Unit 5 and Unit 6 skills do exist and are referenced by id. The `notes` field on each edge in data/staging/unit-07.edges.csv says which skill a topic id stands in for. [inferred]

### What Unit 7 depends on

**Unit 2 and Unit 3 differentiation.** Verifying a solution differentiates a candidate (BC-SKL-07006), and reading the concavity of a solution differentiates the right side of the equation with the chain rule, since the dependent variable is itself a function of the independent one. Those edges run from BC-TOP-0205 and BC-TOP-0301.

**Unit 4 linearisation.** Euler's method is repeated tangent line approximation, and the 2023 question built a tangent line approximation and then decided its direction from the second derivative (sg-23:10, sg-23:11). The edge runs from BC-TOP-0406 to BC-SKL-07020 and BC-SKL-07023.

**Unit 5 analysis of functions.** The solution of a differential equation is analysed by Unit 5 methods applied to a function that is never written down. BC-SKL-07018 depends on BC-SKL-05014 and BC-SKL-05030, BC-SKL-07023 on BC-SKL-05046, and BC-SKL-07042 on BC-SKL-05052 because finding where a logistic quantity changes fastest is an optimisation of the right side. The 2024 question located and classified a critical point of a solution straight from the equation, which is BC-QA-05007 (sg-24:10).

**Unit 6 antidifferentiation.** Separation of variables is two antidifferentiations. BC-SKL-07025 depends on BC-SKL-06034 and BC-SKL-06047, and BC-SKL-07029 and BC-SKL-07032 depend on BC-SKL-06044, the constant of integration skill, and on the accumulation form of a particular solution that BC-EK-FUN-7E2 states.

### What depends on Unit 7

**Unit 8.** Motion along a line solved from a differential equation is the same object the applications unit treats as an accumulation of a rate, so BC-TOP-0802 carries an edge from BC-SKL-07038.

**Unit 9.** A parametric or vector motion question that supplies a derivative and an initial position is a particular solution question in two coordinates, recorded as an edge from BC-SKL-07032 to BC-TOP-0904.

**Unit 10.** The 2025 question took the second derivative of a solution of a differential equation and used the value as the quadratic coefficient of a Taylor polynomial, so BC-TOP-1011 carries an edge from BC-SKL-07018 (sg-25:21, sg-25:22).

## Archetype summary

Eleven archetypes with thirty three variants are recorded in data/staging/unit-07.archetypes.json. Variant dimensions used are representation, reasoning direction, notation, calculator, and difficulty. [verified] (sg-23:9, sg-23:11, sg-23:12, sg-24:9, sg-24:10, sg-24:11, sg-24:17, sg-25:23)

| Archetype | Name | Scope | Calculator | Official parts read |
|---|---|---|---|---|
| BC-QA-07001 | Solution curve sketched on a supplied slope field | shared | no_calculator | 2023 Q3(a), 2024 Q3(a) |
| BC-QA-07002 | Slope field matched to or built from a differential equation | shared | no_calculator | none in 2023 to 2025 |
| BC-QA-07003 | Particular solution by separation of variables | shared | no_calculator | 2023 Q3(d), 2024 Q3(c) |
| BC-QA-07004 | Euler's method over two steps of equal size | BC_only | no_calculator | 2024 Q5(c), 2025 Q5(D) |
| BC-QA-07005 | Direction of an approximation decided from the second derivative of a solution | shared | no_calculator | 2023 Q3(b), 2023 Q3(c) |
| BC-QA-07006 | Differential equation written from a verbal rate statement | shared | either | none in 2023 to 2025 |
| BC-QA-07007 | Verification that a function solves a differential equation | shared | no_calculator | none in 2023 to 2025 |
| BC-QA-07008 | Exponential growth or decay model solved and interpreted | shared | either | none in 2023 to 2025 |
| BC-QA-07009 | Logistic model interpreted without solving | BC_only | either | none in 2023 to 2025 |
| BC-QA-07010 | Behaviour of a solution obtained from the differential equation itself | shared | no_calculator | 2024 Q3(b) |
| BC-QA-07011 | Particular solution with a domain restriction or an accumulation form | shared | no_calculator | none in 2023 to 2025 |

Six archetypes have no matching free response part in 2023 to 2025 and are tagged inferred: BC-QA-07002, BC-QA-07006, BC-QA-07007, BC-QA-07008, BC-QA-07009, and BC-QA-07011. Their scoring patterns are drawn from the CED text and from the nearest scored analogues, chiefly the separation parts of 2023 Q3 and 2024 Q3.

Chief Reader error records in data/errors.json match this unit at five places and are listed in the `common_errors` field of the corresponding skill records so that the link is machine readable without editing the shared records: BC-ERR-99014 (separable differential equation separated or antidifferentiated incorrectly) matches BC-ERR-07024, BC-ERR-07025, and BC-ERR-07029; BC-ERR-99024 (solution curve sketched incorrectly on a slope field) matches BC-ERR-07014 and BC-ERR-07015; BC-ERR-99026 (Euler's method step size or initial value applied incorrectly) matches BC-ERR-07019, BC-ERR-07020, and BC-ERR-07021; BC-ERR-99035 (differential equation solved where it already supplies the slope) matches BC-ERR-07041 and BC-ERR-07044; and BC-ERR-99020 (over or underestimate claimed without appealing to concavity) matches BC-ERR-07018 and BC-ERR-07023. [verified] (cr-22:18, cr-23:11, cr-24:11, crabbc-25:34)

## Misconception summary

Twenty seven misconceptions are recorded in data/staging/unit-07.misconceptions.json against forty four observed errors in data/staging/unit-07.errors.json. The mapping is many to many: an error lists every misconception that could produce it together with non-conceptual causes such as an arithmetic slip, a misread, or time pressure, and every misconception carries rival misconceptions and a discriminating probe. [verified] (sg-23:9, sg-23:11, sg-23:12, sg-24:11, sg-25:23)

| Misconception | Severity | Rivals | Discriminating probe |
|---|---|---|---|
| BC-MIS-07001 Proportional to means equal to | high | BC-MIS-07021 | Ask where the constant of proportionality went. |
| BC-MIS-07002 A differential equation is an equation for the quantity | high | BC-MIS-07001 | Ask what the left side of the written equation measures. |
| BC-MIS-07003 An initial condition is part of the differential equation | medium | BC-MIS-07016 | Ask which sentence of the problem would change if the starting value were different. |
| BC-MIS-07004 A plausible looking function is a solution | medium | BC-MIS-07005 | Ask the student to differentiate the candidate and compare both sides. |
| BC-MIS-07005 A differential equation has one solution | high | BC-MIS-07016 | Ask the student to name two different functions that satisfy the same equation. |
| BC-MIS-07006 A slope field shows values of the solution | high | BC-MIS-07008 | Ask what the length and the tilt of one segment represent. |
| BC-MIS-07007 A horizontal segment marks a maximum of every solution | medium | BC-MIS-07009 | Ask what the constant function at that level does in the equation. |
| BC-MIS-07008 A solution curve may be drawn freely through the field | high | BC-MIS-07006 | Ask whether the drawn curve is tangent to the segment at each point it passes. |
| BC-MIS-07009 A solution may cross an equilibrium level | high | BC-MIS-07007 | Ask what the rate of change is exactly at that level. |
| BC-MIS-07010 The direction of an approximation follows from increase or decrease | high | BC-MIS-07011 | Give an increasing concave down solution and ask for the direction of a tangent line estimate. |
| BC-MIS-07011 Euler's method evaluates the derivative once | high | BC-MIS-07012 | Ask which point the slope is evaluated at on the second step. |
| BC-MIS-07012 Each Euler step restarts from the initial value | high | BC-MIS-07011 | Ask for the input and the output used at the start of the second step. |
| BC-MIS-07013 An answer needs no visible steps | medium | BC-MIS-07011 | Ask the student to label the columns of their own table. |
| BC-MIS-07014 Any differential equation can be separated | high | BC-MIS-07015 | Give an equation whose right side is a sum in both variables and ask for the separated form. |
| BC-MIS-07015 Antidifferentiating one side is enough | high | BC-MIS-07014 | Ask what happened to the differential on the other side. |
| BC-MIS-07016 The constant of integration is optional | high | BC-MIS-07005 | Ask what the answer would be if the starting value were doubled. |
| BC-MIS-07017 An implicit relation is a finished solution | medium | BC-MIS-07016 | Ask for the value of the dependent variable at a stated input. |
| BC-MIS-07018 An absolute value can be dropped without checking | medium | BC-MIS-07019 | Ask whether the enclosed expression is positive or negative at the initial point. |
| BC-MIS-07019 A solution formula holds on every input | medium | BC-MIS-07018 | Ask what happens to the formula at the input where its denominator vanishes. |
| BC-MIS-07020 A particular solution must be written in closed form | medium | BC-MIS-07017 | Ask whether the initial value plus an integral is an acceptable answer. |
| BC-MIS-07021 Proportional growth is linear growth | high | BC-MIS-07001 | Ask what the solution looks like when the rate doubles as the amount doubles. |
| BC-MIS-07022 The constant of proportionality can be read off one data pair | medium | BC-MIS-07021 | Ask which two pieces of data the constant needs. |
| BC-MIS-07023 A numerical answer is a complete interpretation | medium | BC-MIS-07002 | Ask what the number measures and in what units. |
| BC-MIS-07024 The logistic equation is the exponential equation with an extra factor of no consequence | high | BC-MIS-07021 | Ask what happens to the rate when the quantity reaches the carrying capacity. |
| BC-MIS-07025 The carrying capacity must be found by solving the equation | high | BC-MIS-07026 | Ask what value of the quantity makes the rate zero. |
| BC-MIS-07026 The limit of a solution needs the solution formula | high | BC-MIS-07025 | Ask which values of the quantity make the rate positive and which make it negative. |
| BC-MIS-07027 The quantity changes fastest at the carrying capacity | high | BC-MIS-07025 | Ask for the rate exactly at the carrying capacity. |

The highest severity clusters are the four that the scoring guidelines and the CED text point to directly: separating or antidifferentiating without keeping both differentials and the constant (BC-MIS-07014, BC-MIS-07015, BC-MIS-07016, sg-23:12), treating a slope field as a plot of solution values or drawing a curve across an equilibrium level (BC-MIS-07006, BC-MIS-07008, BC-MIS-07009, sg-23:9), restarting each Euler step from the initial value (BC-MIS-07011, BC-MIS-07012, sg-24:17), and believing a logistic model must be solved before anything can be said about it (BC-MIS-07025, BC-MIS-07026, ced:145).

## Unresolved

- BC-EK-FUN-7B2 is tagged single-source in data/curriculum.json because the Fall 2026 clarifications list it as reworded while the cached CED text already carries the new wording. The pre-2026 wording is not recoverable from this project's cache, so BC-SKL-07009, which quotes it, inherits the single-source tag. [uncertain] (ced:138, ced-clarifications-2026:2)
- No free response part in 2023 to 2025 assesses the logistic model, the construction of a slope field from scratch, the verification of a proposed solution, or an exponential growth model. BC-QA-07002, BC-QA-07006, BC-QA-07007, BC-QA-07008, BC-QA-07009, and BC-QA-07011 are therefore tagged inferred and should be revisited when earlier years or official multiple choice material are indexed. [uncertain]
- The 2024 and 2025 guidelines state the Euler's method demonstration point differently: 2024 asks for two steps with at most one error and withholds the answer point if there is an error, while 2025 asks only for the first step and explicitly discounts later simplification or rounding errors for that point (sg-24:17, sg-25:23). Whether this is a durable change in scoring practice or a question-specific decision is not established here. [uncertain]
- The 2023 and 2024 separation parts award different numbers of points for the same work: four in 2023 with both antiderivatives in one point, five in 2024 with the two antiderivatives scored separately (sg-23:12, sg-24:11). The archetype records the 2023 shape as the base pattern and the 2024 shape as a variant. [verified] (sg-23:12, sg-24:11)
- Misconception records are tagged inferred unless a scoring guideline or the CED text names the behaviour directly. No misconception literature is cited, because none could be confirmed from the sources available in this project's cache. [inferred]

<!-- generated:official-evidence:start -->

## Official evidence index [verified]

Generated from data/frq_records.json and data/mcq_records.json. Every record cites its cached document and page; counts are observations over the indexed years only, not predictions. FRQ part records with BC-UNIT-07 as primary or secondary unit: 28. Public sample MCQ records tagged to this unit: 9.

| FRQ record | Role | Calculator | Archetype | Skills (first six) | Points | Point types |
|---|---|---|---|---|---|---|
| BC-FRQ-2013-Q5-A | secondary | no_calculator | BC-QA-04009 | BC-SKL-04033, BC-SKL-04034, BC-SKL-04035, BC-SKL-04036, BC-SKL-04038 | 2 | BC-PT-99055, BC-PT-99004 |
| BC-FRQ-2013-Q5-B | primary | no_calculator | BC-QA-07004 | BC-SKL-07019, BC-SKL-07020, BC-SKL-07021, BC-SKL-07022 | 2 | BC-PT-99034, BC-PT-99004 |
| BC-FRQ-2013-Q5-C | primary | no_calculator | BC-QA-07003 | BC-SKL-07024, BC-SKL-07025, BC-SKL-07026, BC-SKL-07029, BC-SKL-07027, BC-SKL-07031 | 5 | BC-PT-99028, BC-PT-99029, BC-PT-99031, BC-PT-99033, BC-PT-99032 |
| BC-FRQ-2015-Q4-A | primary | no_calculator | BC-QA-07002 | BC-SKL-07010, BC-SKL-07011, BC-SKL-07012 | 2 | BC-PT-99065, BC-PT-99065 |
| BC-FRQ-2015-Q4-B | primary | no_calculator | BC-QA-07010 | BC-SKL-03030, BC-SKL-03033, BC-SKL-05030, BC-SKL-07018 | 2 | BC-PT-99027, BC-PT-99063 |
| BC-FRQ-2015-Q4-C | secondary | no_calculator | BC-QA-05003 | BC-SKL-07010, BC-SKL-05010, BC-SKL-05021, BC-SKL-05022 | 2 | BC-PT-99013, BC-PT-99012 |
| BC-FRQ-2015-Q4-D | primary | no_calculator | BC-QA-07007 | BC-SKL-07006, BC-SKL-07008, BC-SKL-07005, BC-SKL-07033 | 3 | BC-PT-99005, BC-PT-99068, BC-PT-99004 |
| BC-FRQ-2019-Q4-A | secondary | no_calculator | BC-QA-04006 | BC-SKL-04018, BC-SKL-04019, BC-SKL-04023, BC-SKL-04025, BC-SKL-04027 | 2 | BC-PT-99023, BC-PT-99006 |
| BC-FRQ-2019-Q4-B | primary | no_calculator | BC-QA-07010 | BC-SKL-07018, BC-SKL-03030, BC-SKL-03034, BC-SKL-05014 | 3 | BC-PT-99027, BC-PT-99023, BC-PT-99010 |
| BC-FRQ-2019-Q4-C | primary | no_calculator | BC-QA-07003 | BC-SKL-07024, BC-SKL-07025, BC-SKL-07026, BC-SKL-07029, BC-SKL-07027, BC-SKL-06040 | 4 | BC-PT-99028, BC-PT-99029, BC-PT-99031, BC-PT-99032 |
| BC-FRQ-2021-Q5-A | secondary | no_calculator | BC-QA-10010 | BC-SKL-10043, BC-SKL-10044, BC-SKL-10048 | 2 | BC-PT-99035, BC-PT-99004 |
| BC-FRQ-2021-Q5-B | primary | no_calculator | BC-QA-07004 | BC-SKL-07019, BC-SKL-07020, BC-SKL-07021, BC-SKL-07022 | 2 | BC-PT-99034, BC-PT-99004 |
| BC-FRQ-2021-Q5-C | primary | no_calculator | BC-QA-07003 | BC-SKL-07024, BC-SKL-07025, BC-SKL-07026, BC-SKL-07029, BC-SKL-07027, BC-SKL-06057 | 5 | BC-PT-99028, BC-PT-99029, BC-PT-99030, BC-PT-99031, BC-PT-99032 |
| BC-FRQ-2023-Q3-A | primary | no_calculator | BC-QA-07001 | BC-SKL-07014, BC-SKL-07015, BC-SKL-07018 | 1 | BC-PT-99065 |
| BC-FRQ-2023-Q3-B | secondary | no_calculator | BC-QA-04008 | BC-SKL-04028, BC-SKL-04029, BC-SKL-04032, BC-SKL-07010 | 2 | BC-PT-99005, BC-PT-99025 |
| BC-FRQ-2023-Q3-C | primary | no_calculator | BC-QA-07005 | BC-SKL-03033, BC-SKL-07018, BC-SKL-04030, BC-SKL-04031, BC-SKL-05046 | 2 | BC-PT-99027, BC-PT-99026 |
| BC-FRQ-2023-Q3-D | primary | no_calculator | BC-QA-07003 | BC-SKL-07024, BC-SKL-07025, BC-SKL-07026, BC-SKL-07029, BC-SKL-07030, BC-SKL-07027 | 4 | BC-PT-99028, BC-PT-99029, BC-PT-99031, BC-PT-99032 |
| BC-FRQ-2024-Q3-A | primary | no_calculator | BC-QA-07001 | BC-SKL-07014, BC-SKL-07018, BC-SKL-07015 | 1 | BC-PT-99065 |
| BC-FRQ-2024-Q3-B | primary | no_calculator | BC-QA-05007 | BC-SKL-07018, BC-SKL-05010, BC-SKL-05020, BC-SKL-05022, BC-SKL-07010 | 3 | BC-PT-99014, BC-PT-99004, BC-PT-99012 |
| BC-FRQ-2024-Q3-C | primary | no_calculator | BC-QA-07003 | BC-SKL-07024, BC-SKL-07025, BC-SKL-07026, BC-SKL-07029, BC-SKL-07030, BC-SKL-07027 | 5 | BC-PT-99028, BC-PT-99029, BC-PT-99030, BC-PT-99031, BC-PT-99032 |
| BC-FRQ-2024-Q5-C | primary | no_calculator | BC-QA-07004 | BC-SKL-07019, BC-SKL-07020, BC-SKL-07021, BC-SKL-07022, BC-SKL-04029 | 2 | BC-PT-99034, BC-PT-99004 |
| BC-FRQ-2025-Q5-A | secondary | no_calculator | BC-QA-03008 | BC-SKL-02036, BC-SKL-03002, BC-SKL-03033, BC-SKL-03034, BC-SKL-07018 | 3 | BC-PT-99022, BC-PT-99023, BC-PT-99027 |
| BC-FRQ-2025-Q5-B | secondary | no_calculator | BC-QA-10010 | BC-SKL-10044, BC-SKL-10043, BC-SKL-10067 | 2 | BC-PT-99035, BC-PT-99036 |
| BC-FRQ-2025-Q5-D | primary | no_calculator | BC-QA-07004 | BC-SKL-07019, BC-SKL-07020, BC-SKL-07021, BC-SKL-07022, BC-SKL-04029 | 2 | BC-PT-99034, BC-PT-99005 |
| BC-FRQ-2026-Q3-A | primary | no_calculator | BC-QA-07002 | BC-SKL-07010, BC-SKL-07016, BC-SKL-07012, BC-SKL-07018 | 1 | BC-PT-99066 |
| BC-FRQ-2026-Q3-B | primary | no_calculator | BC-QA-07010 | BC-SKL-07010, BC-SKL-04032, BC-SKL-02012 | 1 | BC-PT-99005 |
| BC-FRQ-2026-Q3-C | primary | no_calculator | BC-QA-07005 | BC-SKL-07018, BC-SKL-04030, BC-SKL-04031, BC-SKL-05046, BC-SKL-05030 | 2 | BC-PT-99027, BC-PT-99026 |
| BC-FRQ-2026-Q3-D | primary | no_calculator | BC-QA-07003 | BC-SKL-07024, BC-SKL-07025, BC-SKL-07026, BC-SKL-07029, BC-SKL-07030, BC-SKL-07027 | 5 | BC-PT-99028, BC-PT-99029, BC-PT-99030, BC-PT-99031, BC-PT-99032 |

| MCQ record | Calculator | Archetype | Skills |
|---|---|---|---|
| BC-MCQ-CED-009 | no_calculator | BC-QA-07002 | BC-SKL-07016, BC-SKL-07012, BC-SKL-07013 |
| BC-MCQ-CED-017 | no_calculator | BC-QA-07009 | BC-SKL-07040, BC-SKL-07041, BC-SKL-07043 |
| BC-MCQ-SAMPLE-005 | no_calculator | BC-QA-07002 | BC-SKL-07016, BC-SKL-07012, BC-SKL-07013 |
| BC-MCQ-SAMPLE-010 | no_calculator | BC-QA-07008 | BC-SKL-07034, BC-SKL-07035, BC-SKL-07036 |
| BC-MCQ-SAMPLE-018 | no_calculator | BC-QA-07004 | BC-SKL-07019, BC-SKL-07020, BC-SKL-07021 |
| BC-MCQ-PE2012-012 | no_calculator | BC-QA-07010 | BC-SKL-07006, BC-SKL-05036, BC-SKL-05033 |
| BC-MCQ-PE2012-014 | no_calculator | BC-QA-07009 | BC-SKL-07039, BC-SKL-07040, BC-SKL-07034 |
| BC-MCQ-PE2012-016 | no_calculator | BC-QA-07004 | BC-SKL-07019, BC-SKL-07020, BC-SKL-07021 |
| BC-MCQ-PE2012-023 | no_calculator | BC-QA-07006 | BC-SKL-07001, BC-SKL-07005, BC-SKL-07003 |

<!-- generated:official-evidence:end -->
