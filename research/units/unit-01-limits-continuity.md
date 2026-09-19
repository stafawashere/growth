---
title: Unit 1, Limits and Continuity
research_date: 2026-09-19
status: draft
purpose: Decompose CED Unit 1 into concepts, atomic skills, non-calculus prerequisites, question archetypes and variants, observed errors, candidate misconceptions, and diagnostic signals, each grounded in the CED text and in the 2023 to 2025 official free-response questions and scoring guidelines.
---

# Unit 1, Limits and Continuity

BC-UNIT-01 covers CED pages 38 to 53 and holds sixteen topics, all shared with AB. Topics 1.7 and 1.9 carry no learning objective or essential knowledge statement in the CED and are described there as skill focused topics. Unit weighting is in [../exam/exam-blueprint.md](../exam/exam-blueprint.md) and exam composition is in [../exam/exam-structure.md](../exam/exam-structure.md). [verified] (ced:38, ced:44, ced:46, ced:53)

## 1.1 Introducing Calculus: Can Change Occur at an Instant?

### Official mapping

Topic id BC-TOP-0101, CED code 1.1, name Introducing Calculus: Can Change Occur at an Instant?, scope shared, CED page 38. [verified] (ced:38)

- BC-LO-CHA-1A (CHA-1.A): Interpret the rate of change at an instant in terms of average rates of change over intervals containing that instant.
  - BC-EK-CHA-1A1 (CHA-1.A.1): "Calculus uses limits to understand and model dynamic change."
  - BC-EK-CHA-1A2 (CHA-1.A.2): "Because an average rate of change divides the change in one variable by the change in another, the average rate of change is undefined at a point where the change in the independent variable would be zero."
  - BC-EK-CHA-1A3 (CHA-1.A.3): "The limit concept allows us to define instantaneous rate of change in terms of average rates of change."

Suggested practice skills: BC-MPS-2B (Practice skill 2.B). Weighting pointer: [../exam/exam-blueprint.md](../exam/exam-blueprint.md).

### Concept breakdown

- BC-CON-01001 Instantaneous rate of change as a limit of average rates: An instantaneous rate is what average rates settle towards as the interval shrinks to nothing.

- BC-SKL-01001 Compute an average rate of change over an interval: Divide the change in the function by the change in the input over an interval.
- BC-SKL-01002 Explain why an average rate of change is undefined at a single point: Say why the quotient breaks down when the interval has zero length.
- BC-SKL-01003 Describe an instantaneous rate as a limit of average rates: Say that the rate at an instant is what the average rates approach as the interval closes in.
- BC-SKL-01004 Estimate an instantaneous rate from average rates over shrinking intervals: Compute average rates over smaller and smaller intervals and read off the value they approach.

### Prerequisites

- BC-PRQ-06005 -> BC-SKL-01001, supporting, [inferred], Prerequisite for Compute an average rate of change over an interval.
- BC-PRQ-06005 -> BC-SKL-01002, supporting, [inferred], Prerequisite for Explain why an average rate of change is undefined at a single point.
- BC-PRQ-06005 -> BC-SKL-01003, supporting, [inferred], Prerequisite for Describe an instantaneous rate as a limit of average rates.
- BC-PRQ-06005 -> BC-SKL-01004, supporting, [inferred], Prerequisite for Estimate an instantaneous rate from average rates over shrinking intervals.
- BC-SKL-01001 -> BC-SKL-01003, hard_prerequisite, [inferred], The limiting description is built on the average rate computation.
- BC-SKL-01003 -> BC-SKL-01004, hard_prerequisite, [inferred], Estimating an instantaneous rate applies the limiting description.
- BC-SKL-01003 -> BC-TOP-0201, hard_prerequisite, [inferred], The instantaneous rate as a limit of average rates is the Unit 2 definition of the derivative.

### Required mathematical knowledge

**Average rate of change.** For a function f and an interval from a to b with a not equal to b, the average rate of change is the quotient of f(b) minus f(a) by b minus a.

**Why a point gives no average rate.** The quotient divides by the change in the independent variable, so a single point makes the denominator zero and no average rate is defined there (BC-EK-CHA-1A2).

**Instantaneous rate.** The limit concept defines the instantaneous rate of change in terms of average rates over intervals containing the point (BC-EK-CHA-1A3). The rate at an instant is not computed by evaluating the quotient at a single point.

**Notation.** Average rate of change; instantaneous rate of change; the interval written as a closed interval with its endpoints named.

### Representations

Representations in play: BC-REP-01 Symbolic (analytical) expression, BC-REP-03 Numerical table, BC-REP-04 Verbal description, BC-REP-05 Contextual model.

Conversions tested: contextual model to a difference quotient (BC-REP-05 to BC-REP-01), and a table of values to a sequence of average rates (BC-REP-03 to BC-REP-01).

### Assessment behaviour

MCQ forms ask for an average rate over a named interval or for the statement that correctly relates the two kinds of rate. FRQ forms compute an average rate with supporting work and units, as the 2025 and 2024 opening questions do for a rate estimate (sg-25:11, sg-24:2). Calculator variants supply a formula for the quantity; no-calculator variants supply a short table. Conceptual variants ask why a rate at an instant needs a limit; computational variants ask for the quotient; interpretation variants ask for the meaning of the value with units; justification variants ask what the shrinking averages indicate. Multi-concept variants pair the average rate with an existence argument in a later part of the same question (sg-25:11, sg-25:12).

### Archetypes

- BC-QA-01012 Instantaneous rate approached through average rates over shrinking intervals

### Errors and misconceptions

- BC-ERR-01029 Average rate of change reported as a difference
- BC-ERR-01030 Average rate over an interval reported as the rate at an instant
- BC-MIS-01017 An average rate over an interval is the rate at a point in it, severity high

### Diagnostic signals

- BC-SIG-01016 Average rates computed correctly with no limiting statement, mastery state partially_mastered

### Adaptive metadata summary

Skills in this topic carry calculator relevance none, optional. Remediation targets named across the topic: BC-PRQ-06005. Every skill record carries the full seven key adaptive block in data/staging/unit-01.skills.json. [inferred]

## 1.2 Defining Limits and Using Limit Notation

### Official mapping

Topic id BC-TOP-0102, CED code 1.2, name Defining Limits and Using Limit Notation, scope shared, CED page 39. [verified] (ced:39)

- BC-LO-LIM-1A (LIM-1.A): Represent limits analytically using correct notation.
  - BC-EK-LIM-1A1 (LIM-1.A.1): "Given a function f, the limit of f(x) as x approaches c is a real number R if f(x) can be made arbitrarily close to R by taking x sufficiently close to c (but not equal to c). If the limit exists and is a real number, then the common notation is lim as x approaches c of f(x) = R."
- BC-LO-LIM-1B (LIM-1.B): Interpret limits expressed in analytic notation.
  - BC-EK-LIM-1B1 (LIM-1.B.1): "A limit can be expressed in multiple ways, including graphically, numerically, and analytically."

Suggested practice skills: BC-MPS-2B (Practice skill 2.B). Weighting pointer: [../exam/exam-blueprint.md](../exam/exam-blueprint.md).

### Concept breakdown

- BC-CON-01002 The limit of a function at a point: A limit is the single value the outputs crowd around as the inputs approach a target, whether or not the function is defined there.
- BC-CON-01003 Limit notation and its reading: The symbols for a limit, including the one sided arrows, say precisely which approach is meant.

- BC-SKL-01005 Write a limit statement in correct analytic notation: Turn a described approach into the limit symbols.
- BC-SKL-01006 Interpret a limit statement given in analytic notation: Say in words what a written limit statement claims about the function values.
- BC-SKL-01007 Write one sided limit notation: Use the left and right arrows to say which side the approach comes from.
- BC-SKL-01008 Distinguish the limit at a point from the function value at that point: Say that the limit describes nearby outputs and not the output at the point itself.

### Prerequisites

- BC-PRQ-06005 -> BC-SKL-01005, supporting, [inferred], Prerequisite for Write a limit statement in correct analytic notation.
- BC-PRQ-06005 -> BC-SKL-01006, supporting, [inferred], Prerequisite for Interpret a limit statement given in analytic notation.
- BC-PRQ-06005 -> BC-SKL-01007, supporting, [inferred], Prerequisite for Write one sided limit notation.
- BC-PRQ-06005 -> BC-SKL-01008, supporting, [inferred], Prerequisite for Distinguish the limit at a point from the function value at that point.
- BC-SKL-01005 -> BC-SKL-01007, hard_prerequisite, [inferred], One sided notation builds on the two sided limit notation.

### Required mathematical knowledge

**Definition.** Given a function f, the limit of f(x) as x approaches c is the real number R if f(x) can be made arbitrarily close to R by taking x sufficiently close to c and not equal to c (BC-EK-LIM-1A1).

**Exclusion.** The epsilon delta definition of a limit is not assessed on the AP Calculus AB or BC Exam, although it may be taught (ced:39).

**Notation.** lim as x approaches c of f(x) equals R; the one sided forms write the approach from the left and from the right. A limit expressed graphically, numerically, or analytically makes the same claim (BC-EK-LIM-1B1).

### Representations

Representations in play: BC-REP-01 Symbolic (analytical) expression, BC-REP-04 Verbal description, BC-REP-02 Graphical.

Conversions tested: verbal description of an approach to analytic notation (BC-REP-04 to BC-REP-01), and analytic notation to a statement about a graph (BC-REP-01 to BC-REP-02).

### Assessment behaviour

MCQ forms ask which notation records a described behaviour or what a written statement claims. FRQ forms require correct limit notation inside a larger argument, and a scoring guideline awards a separate point for presenting a limit expression at all (sg-25:4). Calculator variants do not arise for the notation itself; no-calculator variants dominate. Conceptual variants ask whether the function value matters; computational variants are rare; interpretation variants ask for a sentence in ordinary words; justification variants ask why a claimed limit statement is or is not consistent with given information. Multi-concept variants combine notation with a one sided analysis at a discontinuity.

### Archetypes

- BC-QA-01001 Limit estimated from a graph including one sided values
- BC-QA-01013 Limit claim matched across graphical, numerical, and analytic representations

### Errors and misconceptions

- BC-ERR-01001 Function value reported as the limit
- BC-ERR-01003 Nonexistence claimed because the function is undefined at the point
- BC-MIS-01001 The limit at a point is the value of the function there, severity high
- BC-MIS-01003 A limit is a prediction the function must eventually reach, severity medium

### Diagnostic signals

- BC-SIG-01002 Limit and value swapped at a marked break, mastery state not_mastered

### Adaptive metadata summary

Skills in this topic carry calculator relevance none. Remediation targets named across the topic: BC-PRQ-06005. Every skill record carries the full seven key adaptive block in data/staging/unit-01.skills.json. [inferred]

## 1.3 Estimating Limit Values from Graphs

### Official mapping

Topic id BC-TOP-0103, CED code 1.3, name Estimating Limit Values from Graphs, scope shared, CED page 40. [verified] (ced:40)

- BC-LO-LIM-1C (LIM-1.C): Estimate limits of functions.
  - BC-EK-LIM-1C1 (LIM-1.C.1): "The concept of a limit includes one sided limits."
  - BC-EK-LIM-1C2 (LIM-1.C.2): "Graphical information about a function can be used to estimate limits."
  - BC-EK-LIM-1C3 (LIM-1.C.3): "Because of issues of scale, graphical representations of functions may miss important function behavior."
  - BC-EK-LIM-1C4 (LIM-1.C.4): "A limit might not exist for some functions at particular values of x. Some ways that the limit might not exist are if the function is unbounded, if the function is oscillating near this value, or if the limit from the left does not equal the limit from the right."
  - BC-EK-LIM-1C5 (LIM-1.C.5): "Numerical information can be used to estimate limits."

Suggested practice skills: BC-MPS-2B (Practice skill 2.B). Weighting pointer: [../exam/exam-blueprint.md](../exam/exam-blueprint.md).

### Concept breakdown

- BC-CON-01002 The limit of a function at a point: A limit is the single value the outputs crowd around as the inputs approach a target, whether or not the function is defined there.
- BC-CON-01004 One sided limits and two sided existence: A two sided limit exists only when the approach from the left and the approach from the right give the same value.
- BC-CON-01005 Ways a limit can fail to exist: A limit can fail because the sides disagree, because the values grow without bound, or because the values keep oscillating.
- BC-CON-01006 Estimation of a limit from a graph or a table: A graph or a short table can suggest a limit value but cannot prove one.

- BC-SKL-01009 Estimate a two sided limit from a graph: Read the height the graph heads towards from both sides.
- BC-SKL-01010 Estimate one sided limits from a graph: Read separately the height approached from the left and from the right.
- BC-SKL-01011 Determine that a limit fails to exist because the one sided limits differ: Say the limit does not exist when the two sides head to different heights.
- BC-SKL-01012 Determine that a limit fails to exist because the function is unbounded: Say the limit does not exist when the values grow without bound.
- BC-SKL-01013 Determine that a limit fails to exist because the function oscillates: Say the limit does not exist when the values keep swinging without settling.
- BC-SKL-01014 Explain how the scale of a graph can hide function behaviour: Say why a graph on one window can mislead about a limit.

### Prerequisites

- BC-PRQ-06005 -> BC-SKL-01009, supporting, [inferred], Prerequisite for Estimate a two sided limit from a graph.
- BC-PRQ-06005 -> BC-SKL-01010, supporting, [inferred], Prerequisite for Estimate one sided limits from a graph.
- BC-PRQ-01003 -> BC-SKL-01011, supporting, [inferred], Prerequisite for Determine that a limit fails to exist because the one sided limits differ.
- BC-PRQ-01006 -> BC-SKL-01011, supporting, [inferred], Prerequisite for Determine that a limit fails to exist because the one sided limits differ.
- BC-PRQ-01009 -> BC-SKL-01012, supporting, [inferred], Prerequisite for Determine that a limit fails to exist because the function is unbounded.
- BC-PRQ-01005 -> BC-SKL-01013, supporting, [inferred], Prerequisite for Determine that a limit fails to exist because the function oscillates.
- BC-PRQ-06005 -> BC-SKL-01014, supporting, [inferred], Prerequisite for Explain how the scale of a graph can hide function behaviour.
- BC-SKL-01010 -> BC-SKL-01011, hard_prerequisite, [inferred], Reading one sided limits precedes concluding nonexistence from disagreement.

### Required mathematical knowledge

**One sided limits.** The concept of a limit includes one sided limits (BC-EK-LIM-1C1), and the two sided limit exists exactly when both one sided limits exist and agree.

**Failure modes.** A limit may fail to exist because the function is unbounded near the input, because it oscillates near the input, or because the one sided limits differ (BC-EK-LIM-1C4). The CED illustrates all three with a reciprocal square, a reciprocal, and a sine of a reciprocal (ced:40).

**Scale.** Graphical representations at a given scale may miss important function behaviour (BC-EK-LIM-1C3), so a graphical reading supports an estimate rather than a proof.

**Notation.** does not exist; left hand limit; right hand limit.

### Representations

Representations in play: BC-REP-02 Graphical, BC-REP-01 Symbolic (analytical) expression, BC-REP-09 Calculator-generated numerical result.

Conversions tested: graph to a limit statement (BC-REP-02 to BC-REP-01), and graph to a verbal description of nonexistence (BC-REP-02 to BC-REP-04).

### Assessment behaviour

MCQ forms present a graph with several marked breaks and ask for limits, one sided limits, and function values at named inputs. FRQ forms embed graph reading inside a larger question about a function defined by a graph. Calculator variants use a plotted window that conceals behaviour; no-calculator variants supply a drawn graph. Conceptual variants ask which failure mode applies; computational variants ask for values; interpretation variants ask for a sentence describing the behaviour; justification variants ask for a reason for a nonexistence claim. Multi-concept variants pair the reading with a classification of the discontinuity at the same input (BC-QA-01007).

### Archetypes

- BC-QA-01001 Limit estimated from a graph including one sided values
- BC-QA-01013 Limit claim matched across graphical, numerical, and analytic representations

### Errors and misconceptions

- BC-ERR-01001 Function value reported as the limit
- BC-ERR-01002 One sided value reported as the two sided limit
- BC-ERR-01004 Oscillation reported as a limit value
- BC-ERR-01020 Infinite limit reported as an existing real limit
- BC-MIS-01001 The limit at a point is the value of the function there, severity high
- BC-MIS-01002 A limit exists whenever the function approaches something on one side, severity high
- BC-MIS-01004 A table settles the behaviour of a function, severity medium
- BC-MIS-01012 Unbounded behaviour is the same on both sides, severity high

### Diagnostic signals

- BC-SIG-01001 One sided values correct with a two sided claim attached, mastery state partially_mastered

### Adaptive metadata summary

Skills in this topic carry calculator relevance none, optional. Remediation targets named across the topic: BC-PRQ-01003, BC-PRQ-01005, BC-PRQ-01009, BC-PRQ-06005. Every skill record carries the full seven key adaptive block in data/staging/unit-01.skills.json. [inferred]

## 1.4 Estimating Limit Values from Tables

### Official mapping

Topic id BC-TOP-0104, CED code 1.4, name Estimating Limit Values from Tables, scope shared, CED page 41. [verified] (ced:41)

- BC-LO-LIM-1C (LIM-1.C): Estimate limits of functions.
  - BC-EK-LIM-1C1 (LIM-1.C.1): "The concept of a limit includes one sided limits."
  - BC-EK-LIM-1C2 (LIM-1.C.2): "Graphical information about a function can be used to estimate limits."
  - BC-EK-LIM-1C3 (LIM-1.C.3): "Because of issues of scale, graphical representations of functions may miss important function behavior."
  - BC-EK-LIM-1C4 (LIM-1.C.4): "A limit might not exist for some functions at particular values of x. Some ways that the limit might not exist are if the function is unbounded, if the function is oscillating near this value, or if the limit from the left does not equal the limit from the right."
  - BC-EK-LIM-1C5 (LIM-1.C.5): "Numerical information can be used to estimate limits."

Suggested practice skills: BC-MPS-2B (Practice skill 2.B). Weighting pointer: [../exam/exam-blueprint.md](../exam/exam-blueprint.md).

### Concept breakdown

- BC-CON-01002 The limit of a function at a point: A limit is the single value the outputs crowd around as the inputs approach a target, whether or not the function is defined there.
- BC-CON-01004 One sided limits and two sided existence: A two sided limit exists only when the approach from the left and the approach from the right give the same value.
- BC-CON-01005 Ways a limit can fail to exist: A limit can fail because the sides disagree, because the values grow without bound, or because the values keep oscillating.
- BC-CON-01006 Estimation of a limit from a graph or a table: A graph or a short table can suggest a limit value but cannot prove one.

- BC-SKL-01015 Estimate a two sided limit from a table of values: Read the value the outputs crowd towards as the inputs close in from both sides.
- BC-SKL-01016 Estimate a one sided limit from a table of values: Use only the rows on one side of the target input.
- BC-SKL-01017 Judge whether a table supports a limit value or is inconclusive: Decide whether the tabulated values really settle or only appear to.

### Prerequisites

- BC-PRQ-06005 -> BC-SKL-01015, supporting, [inferred], Prerequisite for Estimate a two sided limit from a table of values.
- BC-PRQ-06005 -> BC-SKL-01016, supporting, [inferred], Prerequisite for Estimate a one sided limit from a table of values.
- BC-PRQ-06005 -> BC-SKL-01017, supporting, [inferred], Prerequisite for Judge whether a table supports a limit value or is inconclusive.
- BC-SKL-01009 -> BC-SKL-01015, supporting, [inferred], Graphical estimation and numerical estimation support the same limit concept.
- BC-SKL-01015 -> BC-TOP-1001, supporting, [inferred], Reading a limit from a sequence of values supports convergence of sequences at Unit 10 topic 10.1.

### Required mathematical knowledge

**Numerical estimation.** Numerical information can be used to estimate limits (BC-EK-LIM-1C5). Values at inputs approaching the target from both sides support an estimate of the two sided limit; values on one side support a one sided estimate only.

**Limits of the method.** A finite table does not determine the behaviour between its rows, so an estimate remains an estimate. The same caution that applies to graphical scale (BC-EK-LIM-1C3) applies to the spacing of a table.

**Notation.** estimate; the tabulated inputs written as approaching the target from the left and from the right.

### Representations

Representations in play: BC-REP-03 Numerical table, BC-REP-04 Verbal description, BC-REP-05 Contextual model.

Conversions tested: table to an estimated limit value (BC-REP-03 to BC-REP-01), and table to a statement about what the data do and do not establish (BC-REP-03 to BC-REP-04).

### Assessment behaviour

MCQ forms supply a short table and ask for the estimated limit. FRQ forms use tabulated values inside larger questions, where the reasoning from tabular data carries separate points (sg-25:11). Calculator variants generate the table from a formula; no-calculator variants supply it. Conceptual variants ask what a table can establish; computational variants ask for the estimate; interpretation variants attach units in a contextual setting; justification variants ask why the table is or is not conclusive. Multi-concept variants combine the estimate with an average rate computed from the same table.

### Archetypes

- BC-QA-01002 Limit estimated from a table of values

### Errors and misconceptions

- BC-ERR-01004 Oscillation reported as a limit value
- BC-ERR-01005 Table treated as proof of a limit
- BC-MIS-01004 A table settles the behaviour of a function, severity medium

### Diagnostic signals

- No signal is scoped to this topic; the unit level signal list in data/staging/unit-01.signals.json applies.

### Adaptive metadata summary

Skills in this topic carry calculator relevance none. Remediation targets named across the topic: BC-PRQ-06005. Every skill record carries the full seven key adaptive block in data/staging/unit-01.skills.json. [inferred]

## 1.5 Determining Limits Using Algebraic Properties of Limits

### Official mapping

Topic id BC-TOP-0105, CED code 1.5, name Determining Limits Using Algebraic Properties of Limits, scope shared, CED page 42. [verified] (ced:42)

- BC-LO-LIM-1D (LIM-1.D): Determine the limits of functions using limit theorems.
  - BC-EK-LIM-1D1 (LIM-1.D.1): "One-sided limits can be determined analytically or graphically."
  - BC-EK-LIM-1D2 (LIM-1.D.2): "Limits of sums, differences, products, quotients, and composite functions can be found using limit theorems."

Suggested practice skills: BC-MPS-1E (Practice skill 1.E). Weighting pointer: [../exam/exam-blueprint.md](../exam/exam-blueprint.md).

### Concept breakdown

- BC-CON-01004 One sided limits and two sided existence: A two sided limit exists only when the approach from the left and the approach from the right give the same value.
- BC-CON-01007 Limit theorems for combinations of functions: Limits pass through sums, differences, products, quotients, and compositions when the pieces have limits.

- BC-SKL-01018 Apply the sum and difference limit theorems: Split the limit of a sum into the sum of the limits.
- BC-SKL-01019 Apply the product and constant multiple limit theorems: Take the limit of each factor and multiply, and pull constants out.
- BC-SKL-01020 Apply the quotient limit theorem and check the denominator condition: Divide the limits, after checking that the bottom limit is not zero.
- BC-SKL-01021 Evaluate a limit by direct substitution where the function is continuous: Put the target value into the expression when that is legitimate.
- BC-SKL-01022 Apply the limit theorem for composite functions: Take the limit of the inside first, then apply the outside function.
- BC-SKL-01023 Determine a two sided limit by matching one sided limits of a piecewise rule: Evaluate each branch at the boundary and compare.

### Prerequisites

- BC-PRQ-06005 -> BC-SKL-01018, supporting, [inferred], Prerequisite for Apply the sum and difference limit theorems.
- BC-PRQ-06005 -> BC-SKL-01019, supporting, [inferred], Prerequisite for Apply the product and constant multiple limit theorems.
- BC-PRQ-06005 -> BC-SKL-01020, supporting, [inferred], Prerequisite for Apply the quotient limit theorem and check the denominator condition.
- BC-PRQ-01008 -> BC-SKL-01021, supporting, [inferred], Prerequisite for Evaluate a limit by direct substitution where the function is continuous.
- BC-PRQ-06005 -> BC-SKL-01022, supporting, [inferred], Prerequisite for Apply the limit theorem for composite functions.
- BC-PRQ-01003 -> BC-SKL-01023, supporting, [inferred], Prerequisite for Determine a two sided limit by matching one sided limits of a piecewise rule.
- BC-SKL-01021 -> BC-TOP-0202, supporting, [inferred], Direct substitution is the closing step of a derivative computed from the limit definition.

### Required mathematical knowledge

**Limit theorems.** Limits of sums, differences, products, quotients, and composite functions can be found using limit theorems (BC-EK-LIM-1D2). The quotient theorem requires that the limit of the denominator is not zero; the composite theorem requires the outer function to be continuous at the inner limit.

**One sided determination.** One sided limits can be determined analytically or graphically (BC-EK-LIM-1D1), and the two sided limit follows when the two agree.

**Direct substitution.** For a function continuous at the input, the limit equals the function value, which is what makes substitution legitimate (BC-EK-LIM-2B2 supplies the families).

**Notation.** limit theorems; the constant multiple written outside the limit symbol.

### Representations

Representations in play: BC-REP-01 Symbolic (analytical) expression, BC-REP-03 Numerical table, BC-REP-02 Graphical.

Conversions tested: supplied limits to the limit of a combination (BC-REP-01 to BC-REP-01), and a piecewise rule to matched one sided limits (BC-REP-01 to BC-REP-02).

### Assessment behaviour

MCQ forms supply the limits of two functions and ask for the limit of a combination. FRQ forms use the theorems implicitly while evaluating limits inside a larger argument. Calculator variants are uncommon; no-calculator variants dominate. Conceptual variants test the denominator condition; computational variants ask for a value; interpretation variants ask what a supplied limit says about a function; justification variants ask which theorem was used and whether its condition holds. Multi-concept variants combine the theorems with a piecewise boundary so that one sided limits must be matched first.

### Archetypes

- BC-QA-01003 Limit evaluated by limit theorems from given limits or tabulated values
- BC-QA-01006 Continuity at a point tested against the three conditions
- BC-QA-01014 Procedure selected for a limit from the form of the expression

### Errors and misconceptions

- BC-ERR-01006 Quotient limit theorem applied with a zero denominator limit
- BC-ERR-01007 Composition evaluated in the wrong order
- BC-ERR-01017 Wrong branch evaluated at a boundary
- BC-MIS-01005 Limit theorems apply unconditionally, severity high

### Diagnostic signals

- No signal is scoped to this topic; the unit level signal list in data/staging/unit-01.signals.json applies.

### Adaptive metadata summary

Skills in this topic carry calculator relevance none. Remediation targets named across the topic: BC-PRQ-01003, BC-PRQ-01008, BC-PRQ-06005. Every skill record carries the full seven key adaptive block in data/staging/unit-01.skills.json. [inferred]

## 1.6 Determining Limits Using Algebraic Manipulation

### Official mapping

Topic id BC-TOP-0106, CED code 1.6, name Determining Limits Using Algebraic Manipulation, scope shared, CED page 43. [verified] (ced:43)

- BC-LO-LIM-1E (LIM-1.E): Determine the limits of functions using equivalent expressions for the function or the squeeze theorem.
  - BC-EK-LIM-1E1 (LIM-1.E.1): "It may be necessary or helpful to rearrange expressions into equivalent forms before evaluating limits."
  - BC-EK-LIM-1E2 (LIM-1.E.2): "The limit of a function may be found by using the squeeze theorem."

Suggested practice skills: BC-MPS-1C (Practice skill 1.C). Weighting pointer: [../exam/exam-blueprint.md](../exam/exam-blueprint.md).

### Concept breakdown

- BC-CON-01008 Indeterminate form handled by rewriting: When substitution gives zero over zero the expression must be rewritten before the limit can be read off.

- BC-SKL-01024 Evaluate an indeterminate limit by factoring and dividing out a common factor: Factor top and bottom, cancel the shared factor, then substitute.
- BC-SKL-01025 Evaluate an indeterminate limit by multiplying by a conjugate: Clear the radical with the conjugate, then cancel and substitute.
- BC-SKL-01026 Evaluate an indeterminate limit by simplifying a complex fraction: Clear the nested fractions first, then cancel and substitute.
- BC-SKL-01027 Evaluate an indeterminate limit by rewriting with trigonometric identities: Use an identity to turn the expression into one that can be evaluated.
- BC-SKL-01028 Recognise an indeterminate form as a signal that rewriting is needed: See that zero over zero carries no value and that the expression must be changed.

### Prerequisites

- BC-PRQ-01001 -> BC-SKL-01024, supporting, [inferred], Prerequisite for Evaluate an indeterminate limit by factoring and dividing out a common factor.
- BC-PRQ-01002 -> BC-SKL-01025, supporting, [inferred], Prerequisite for Evaluate an indeterminate limit by multiplying by a conjugate.
- BC-PRQ-01007 -> BC-SKL-01026, supporting, [inferred], Prerequisite for Evaluate an indeterminate limit by simplifying a complex fraction.
- BC-PRQ-01005 -> BC-SKL-01027, supporting, [inferred], Prerequisite for Evaluate an indeterminate limit by rewriting with trigonometric identities.
- BC-PRQ-01001 -> BC-SKL-01028, supporting, [inferred], Prerequisite for Recognise an indeterminate form as a signal that rewriting is needed.
- BC-SKL-01028 -> BC-SKL-01024, hard_prerequisite, [inferred], Recognising the indeterminate form precedes selecting a rewriting technique.
- BC-SKL-01028 -> BC-SKL-01025, hard_prerequisite, [inferred], Recognising the indeterminate form precedes selecting a rewriting technique.
- BC-SKL-01028 -> BC-SKL-01026, hard_prerequisite, [inferred], Recognising the indeterminate form precedes selecting a rewriting technique.
- BC-SKL-01028 -> BC-SKL-01027, hard_prerequisite, [inferred], Recognising the indeterminate form precedes selecting a rewriting technique.
- BC-SKL-01024 -> BC-TOP-0202, hard_prerequisite, [inferred], Evaluating an indeterminate limit by rewriting is the technique used on the difference quotient limit in Unit 2 topic 2.2.
- BC-SKL-01028 -> BC-TOP-0407, hard_prerequisite, [inferred], Identifying an indeterminate form is the entry condition for L'Hospital's rule at Unit 4 topic 4.7.

### Required mathematical knowledge

**Rewriting.** It may be necessary or helpful to rearrange expressions into equivalent forms before evaluating limits (BC-EK-LIM-1E1). The CED names factoring and dividing out common factors, multiplying by an expression involving the conjugate, and using alternate forms of trigonometric functions (ced:43).

**Equivalence.** The rewritten expression agrees with the original at every input near the target other than the target itself, which is exactly what the limit concept requires.

**Cross-unit dependency.** L'Hospital's rule is not available in Unit 1. It enters the course at Unit 4 topic 4.7 (BC-TOP-0407), and a 2023 free response part resolves an indeterminate quotient with it rather than by algebra (sg-23:14). Within Unit 1 the same forms are handled by rewriting only.

**Notation.** indeterminate form zero over zero.

### Representations

Representations in play: BC-REP-01 Symbolic (analytical) expression.

Conversions tested: an expression that is indeterminate at the target to an equivalent expression valid near it (BC-REP-01 to BC-REP-01).

### Assessment behaviour

MCQ forms present a quotient that is indeterminate under substitution and ask for its value. FRQ forms embed the evaluation inside a larger question, where a scoring guideline requires the limits of numerator and denominator to be presented separately and refuses the point to a limit written as equal to zero over zero (sg-23:14). Calculator variants are uncommon; no-calculator variants dominate. Conceptual variants ask what the indeterminate form signals; computational variants ask for the value; interpretation variants are rare; justification variants ask why the rewritten expression has the same limit. Multi-concept variants place the indeterminate quotient at a boundary of a piecewise rule or inside a continuity question.

### Archetypes

- BC-QA-01004 Indeterminate limit resolved by algebraic rewriting

### Errors and misconceptions

- BC-ERR-01008 Indeterminate form read as the answer zero
- BC-ERR-01009 Indeterminate form read as nonexistence
- BC-ERR-01010 A term cancelled instead of a factor
- BC-ERR-01011 Limit written as equal to zero over zero
- BC-MIS-01006 An indeterminate form is a value, severity high
- BC-MIS-01007 Rewriting an expression may change any matching symbols, severity high

### Diagnostic signals

- BC-SIG-01003 Correct rewriting with an arithmetic slip in the final evaluation, mastery state partially_mastered
- BC-SIG-01004 Indeterminate form named and then abandoned, mastery state not_mastered
- BC-SIG-01005 Limit written as equal to zero over zero with correct subsequent work, mastery state partially_mastered

### Adaptive metadata summary

Skills in this topic carry calculator relevance none. Remediation targets named across the topic: BC-PRQ-01001, BC-PRQ-01002, BC-PRQ-01005, BC-PRQ-01007. Every skill record carries the full seven key adaptive block in data/staging/unit-01.skills.json. [inferred]

## 1.7 Selecting Procedures for Determining Limits

### Official mapping

Topic id BC-TOP-0107, CED code 1.7, name Selecting Procedures for Determining Limits, scope shared, CED page 44. [verified] (ced:44)

This topic carries no learning objective or essential knowledge statement in the CED. It is described as focusing on the skill of selecting an appropriate procedure for determining limits and on practising all the learning objectives that relate to determining limits (ced:44). [verified] (ced:44)

Suggested practice skills: BC-MPS-1C (Practice skill 1.C). Weighting pointer: [../exam/exam-blueprint.md](../exam/exam-blueprint.md).

### Concept breakdown

- BC-CON-01008 Indeterminate form handled by rewriting: When substitution gives zero over zero the expression must be rewritten before the limit can be read off.
- BC-CON-01009 Selection of a procedure for a limit: The form the expression takes under substitution decides which method to use.

- BC-SKL-01029 Classify a limit expression by its form under substitution: Substitute first and name what comes out: a value, zero over zero, or an unbounded quotient.
- BC-SKL-01030 Select an appropriate procedure for a given limit expression: Pick the method that suits the form the expression takes.
- BC-SKL-01031 Recognise when substitution already settles the limit: Stop rewriting when the direct value is legitimate.

### Prerequisites

- BC-PRQ-01001 -> BC-SKL-01029, supporting, [inferred], Prerequisite for Classify a limit expression by its form under substitution.
- BC-PRQ-01001 -> BC-SKL-01030, supporting, [inferred], Prerequisite for Select an appropriate procedure for a given limit expression.
- BC-PRQ-01008 -> BC-SKL-01031, supporting, [inferred], Prerequisite for Recognise when substitution already settles the limit.
- BC-SKL-01021 -> BC-SKL-01029, hard_prerequisite, [inferred], Substitution must be available before an expression can be classified by its form under substitution.
- BC-SKL-01029 -> BC-SKL-01030, hard_prerequisite, [inferred], Classification of the form precedes selection of the procedure.

### Required mathematical knowledge

**Classification under substitution.** Substituting the target input produces a determinate value, the indeterminate form zero over zero, or a nonzero number over zero. The first is the answer, the second calls for rewriting, and the third calls for one sided sign analysis.

**Procedure set available in Unit 1.** Direct substitution, the limit theorems, algebraic rewriting, the squeeze theorem, one sided analysis, and end behaviour comparison. L'Hospital's rule belongs to Unit 4 topic 4.7 and is not part of this selection set.

**Notation.** The classification stated in words before any computation.

### Representations

Representations in play: BC-REP-01 Symbolic (analytical) expression, BC-REP-04 Verbal description.

Conversions tested: an expression to a named procedure (BC-REP-01 to BC-REP-04).

### Assessment behaviour

MCQ forms offer several limits and ask which method applies, or ask for the value once the method is chosen. FRQ forms do not present procedure selection as a separate task, so the archetype here is inferred from the CED description of the topic (ced:44). Calculator variants are uncommon; no-calculator variants dominate. Conceptual variants ask for the classification alone; computational variants ask for the value; interpretation variants are rare; justification variants ask why the chosen method fits the form. Multi-concept variants mix a determinate substitution, an indeterminate quotient, and a limit at infinity in one item.

### Archetypes

- BC-QA-01014 Procedure selected for a limit from the form of the expression

### Errors and misconceptions

- BC-ERR-01006 Quotient limit theorem applied with a zero denominator limit
- BC-ERR-01008 Indeterminate form read as the answer zero
- BC-ERR-01009 Indeterminate form read as nonexistence
- BC-MIS-01006 An indeterminate form is a value, severity high

### Diagnostic signals

- No signal is scoped to this topic; the unit level signal list in data/staging/unit-01.signals.json applies.

### Adaptive metadata summary

Skills in this topic carry calculator relevance none. Remediation targets named across the topic: BC-PRQ-01001, BC-PRQ-01008. Every skill record carries the full seven key adaptive block in data/staging/unit-01.skills.json. [inferred]

## 1.8 Determining Limits Using the Squeeze Theorem

### Official mapping

Topic id BC-TOP-0108, CED code 1.8, name Determining Limits Using the Squeeze Theorem, scope shared, CED page 45. [verified] (ced:45)

- BC-LO-LIM-1E (LIM-1.E): Determine the limits of functions using equivalent expressions for the function or the squeeze theorem.
  - BC-EK-LIM-1E1 (LIM-1.E.1): "It may be necessary or helpful to rearrange expressions into equivalent forms before evaluating limits."
  - BC-EK-LIM-1E2 (LIM-1.E.2): "The limit of a function may be found by using the squeeze theorem."

Suggested practice skills: BC-MPS-3C (Practice skill 3.C). Weighting pointer: [../exam/exam-blueprint.md](../exam/exam-blueprint.md).

### Concept breakdown

- BC-CON-01010 The squeeze theorem: If a function is trapped between two functions that meet at a value, it meets them there too.

- BC-SKL-01032 State the hypotheses of the squeeze theorem: Name what must hold before the theorem may be used.
- BC-SKL-01033 Verify the bounding inequality on an interval around the point: Show the function really sits between the two bounds near the point.
- BC-SKL-01034 Conclude a limit value from matching bounds: Once both bounds have the same limit, state that the trapped function has it too.
- BC-SKL-01035 Apply the squeeze theorem to a bounded oscillating factor: Bound the oscillating part between negative one and one and multiply through.

### Prerequisites

- BC-PRQ-01010 -> BC-SKL-01032, supporting, [inferred], Prerequisite for State the hypotheses of the squeeze theorem.
- BC-PRQ-01005 -> BC-SKL-01033, supporting, [inferred], Prerequisite for Verify the bounding inequality on an interval around the point.
- BC-PRQ-01010 -> BC-SKL-01034, supporting, [inferred], Prerequisite for Conclude a limit value from matching bounds.
- BC-PRQ-01005 -> BC-SKL-01035, supporting, [inferred], Prerequisite for Apply the squeeze theorem to a bounded oscillating factor.
- BC-SKL-01032 -> BC-SKL-01034, hard_prerequisite, [inferred], The conclusion of the squeeze theorem rests on its stated hypotheses.
- BC-SKL-01033 -> BC-SKL-01035, hard_prerequisite, [inferred], Bounding an oscillating factor is the step that produces the inequality.

### Required mathematical knowledge

**Squeeze theorem.** If g(x) is less than or equal to f(x) and f(x) is less than or equal to h(x) for all x near c except possibly at c, and the limits of g and h at c are both L, then the limit of f at c is L (BC-EK-LIM-1E2).

**Hypotheses as a separate demand.** The suggested practice skill for this topic is confirming whether the hypotheses or conditions of a selected definition, theorem, or test have been satisfied (BC-MPS-3C, ced:45), so stating and checking the hypotheses is itself assessable and is recorded here as BC-SKL-01032 and BC-SKL-01033.

**Illustrative use.** The CED names the theorem as the route to the limit of sine x over x and of one minus cosine x over x at zero (ced:45).

**Notation.** squeeze theorem; the inequality written with the trapped function in the middle.

### Representations

Representations in play: BC-REP-01 Symbolic (analytical) expression, BC-REP-02 Graphical, BC-REP-04 Verbal description.

Conversions tested: a bounding inequality to a limit conclusion (BC-REP-01 to BC-REP-01), and a graph showing the trapped curve to the stated inequality (BC-REP-02 to BC-REP-01).

### Assessment behaviour

MCQ forms supply the bounding inequality and ask for the limit. FRQ forms would demand the verification of the inequality and the two bounding limits as separate steps; no free response part in 2023 to 2025 assesses the squeeze theorem, so the archetype is inferred. Calculator variants are uncommon; no-calculator variants dominate. Conceptual variants ask which hypotheses are needed; computational variants ask for the value; interpretation variants ask what the inequality says about the trapped function; justification variants ask for the full argument. Multi-concept variants pair the theorem with the bounds on a trigonometric factor.

### Archetypes

- BC-QA-01005 Limit determined by the squeeze theorem with its hypotheses stated

### Errors and misconceptions

- BC-ERR-01012 Inequality multiplied by a sign changing factor without reversal
- BC-ERR-01013 Bounds evaluated at the point instead of taken as limits
- BC-MIS-01008 The squeeze theorem is a substitution rule, severity medium
- BC-MIS-01010 Restating a definition counts as a justification, severity high

### Diagnostic signals

- BC-SIG-01018 Squeeze bounds correct with the conclusion drawn from evaluation, mastery state partially_mastered

### Adaptive metadata summary

Skills in this topic carry calculator relevance none. Remediation targets named across the topic: BC-PRQ-01005, BC-PRQ-01010. Every skill record carries the full seven key adaptive block in data/staging/unit-01.skills.json. [inferred]

## 1.9 Connecting Multiple Representations of Limits

### Official mapping

Topic id BC-TOP-0109, CED code 1.9, name Connecting Multiple Representations of Limits, scope shared, CED page 46. [verified] (ced:46)

This topic carries no learning objective or essential knowledge statement in the CED. It is described as focusing on connecting representations and on practising the limit learning objectives while translating information within and across representations (ced:46). [verified] (ced:46)

Suggested practice skills: BC-MPS-2C (Practice skill 2.C). Weighting pointer: [../exam/exam-blueprint.md](../exam/exam-blueprint.md).

### Concept breakdown

- BC-CON-01003 Limit notation and its reading: The symbols for a limit, including the one sided arrows, say precisely which approach is meant.
- BC-CON-01011 Connecting graphical, numerical, analytical, and verbal limit statements: The same limit fact can be shown by a graph, a table, a formula, or a sentence, and these must agree.

- BC-SKL-01036 Match a graph, a table, and an analytic expression of the same limit: Check that the three presentations of one limit agree.
- BC-SKL-01037 Translate a limit statement into a verbal description of behaviour: Say in ordinary words what the symbols claim about the function near the point.
- BC-SKL-01038 Sketch a graph consistent with stated limit and value conditions: Draw a curve that meets every limit and value condition given.

### Prerequisites

- BC-PRQ-06005 -> BC-SKL-01036, supporting, [inferred], Prerequisite for Match a graph, a table, and an analytic expression of the same limit.
- BC-PRQ-06005 -> BC-SKL-01037, supporting, [inferred], Prerequisite for Translate a limit statement into a verbal description of behaviour.
- BC-PRQ-01003 -> BC-SKL-01038, supporting, [inferred], Prerequisite for Sketch a graph consistent with stated limit and value conditions.
- BC-SKL-01006 -> BC-SKL-01037, supporting, [inferred], Verbal translation of a limit statement builds on reading the notation.

### Required mathematical knowledge

**Equivalence across representations.** A limit claim carried by a graph, a table, an expression, or a sentence is the same claim, and a conversion must preserve the target input, the direction of approach, and the claimed value.

**What conversion must not lose.** The distinction between the limit and the function value, the distinction between a one sided and a two sided claim, and the distinction between an infinite limit and a limit at infinity.

**Notation.** All the limit notation of topic 1.2 together with the infinite forms of topics 1.14 and 1.15.

### Representations

Representations in play: BC-REP-01 Symbolic (analytical) expression, BC-REP-02 Graphical, BC-REP-03 Numerical table, BC-REP-04 Verbal description.

Conversions tested: graph to table (BC-REP-02 to BC-REP-03), analytic statement to verbal description (BC-REP-01 to BC-REP-04), and stated conditions to a sketched graph (BC-REP-04 to BC-REP-02).

### Assessment behaviour

MCQ forms ask which of several representations matches a stated limit behaviour. FRQ forms ask for a description in words of behaviour presented analytically, and a separate point can attach to presenting a limit expression rather than only a value (sg-25:4). Calculator variants use a plotted window; no-calculator variants supply a drawn graph or a table. Conceptual variants test the distinctions above; computational variants are rare; interpretation variants ask for the verbal form; justification variants ask why a candidate representation fails. Multi-concept variants require a graph to be produced satisfying several stated limit and value conditions at once.

### Archetypes

- BC-QA-01013 Limit claim matched across graphical, numerical, and analytic representations

### Errors and misconceptions

- BC-ERR-01033 Limit at infinity confused with an infinite limit
- BC-MIS-01018 All limit notation with an infinity symbol means the same thing, severity medium

### Diagnostic signals

- No signal is scoped to this topic; the unit level signal list in data/staging/unit-01.signals.json applies.

### Adaptive metadata summary

Skills in this topic carry calculator relevance none. Remediation targets named across the topic: BC-PRQ-01003, BC-PRQ-06005. Every skill record carries the full seven key adaptive block in data/staging/unit-01.skills.json. [inferred]

## 1.10 Exploring Types of Discontinuities

### Official mapping

Topic id BC-TOP-0110, CED code 1.10, name Exploring Types of Discontinuities, scope shared, CED page 47. [verified] (ced:47)

- BC-LO-LIM-2A (LIM-2.A): Justify conclusions about continuity at a point using the definition.
  - BC-EK-LIM-2A1 (LIM-2.A.1): "Types of discontinuities include removable discontinuities, jump discontinuities, and discontinuities due to vertical asymptotes."
  - BC-EK-LIM-2A2 (LIM-2.A.2): "A function f is continuous at x = c provided that f(c) exists, lim as x approaches c of f(x) exists, and lim as x approaches c of f(x) = f(c)."

Suggested practice skills: BC-MPS-3B (Practice skill 3.B). Weighting pointer: [../exam/exam-blueprint.md](../exam/exam-blueprint.md).

### Concept breakdown

- BC-CON-01012 Classification of discontinuities: A break in a graph is removable, a jump, or an infinite break at a vertical asymptote.

- BC-SKL-01039 Classify a removable discontinuity: Name a break removable when the limit exists but the value does not match it.
- BC-SKL-01040 Classify a jump discontinuity: Name a break a jump when both sides settle but at different heights.
- BC-SKL-01041 Classify a discontinuity due to a vertical asymptote: Name a break infinite when the values grow without bound on at least one side.
- BC-SKL-01042 Identify the discontinuities of a piecewise defined function from its rule: Check each branch boundary and each point excluded from a branch domain.

### Prerequisites

- BC-PRQ-01001 -> BC-SKL-01039, supporting, [inferred], Prerequisite for Classify a removable discontinuity.
- BC-PRQ-01003 -> BC-SKL-01040, supporting, [inferred], Prerequisite for Classify a jump discontinuity.
- BC-PRQ-01006 -> BC-SKL-01040, supporting, [inferred], Prerequisite for Classify a jump discontinuity.
- BC-PRQ-01009 -> BC-SKL-01041, supporting, [inferred], Prerequisite for Classify a discontinuity due to a vertical asymptote.
- BC-PRQ-01003 -> BC-SKL-01042, supporting, [inferred], Prerequisite for Identify the discontinuities of a piecewise defined function from its rule.
- BC-PRQ-01008 -> BC-SKL-01042, supporting, [inferred], Prerequisite for Identify the discontinuities of a piecewise defined function from its rule.
- BC-SKL-01040 -> BC-TOP-0204, supporting, [inferred], Jump discontinuity classification supports the Unit 2 treatment of points where a derivative fails to exist.

### Required mathematical knowledge

**Types.** Types of discontinuities include removable discontinuities, jump discontinuities, and discontinuities due to vertical asymptotes (BC-EK-LIM-2A1).

**Deciding rule.** The classification is settled by the one sided limits. Both exist and agree gives removable; both exist and differ gives a jump; at least one is infinite gives a vertical asymptote. The function value at the input plays no part in the classification, only in whether a discontinuity is present.

**Notation.** removable discontinuity; jump discontinuity; discontinuity due to a vertical asymptote.

### Representations

Representations in play: BC-REP-01 Symbolic (analytical) expression, BC-REP-02 Graphical.

Conversions tested: a rule to a classification (BC-REP-01 to BC-REP-04), and a graph to a classification (BC-REP-02 to BC-REP-04).

### Assessment behaviour

MCQ forms ask for the classification of each break of a given function. FRQ forms use the classification inside larger questions about functions defined piecewise or by graphs. Calculator variants are uncommon; no-calculator variants dominate. Conceptual variants ask which classification applies; computational variants require the one sided limits first; interpretation variants ask what the break means for a modelled quantity; justification variants demand the limits that support the classification. Multi-concept variants combine the classification with a question about whether the break can be removed (BC-QA-01008).

### Archetypes

- BC-QA-01006 Continuity at a point tested against the three conditions
- BC-QA-01007 Discontinuity classified from a rule or a graph
- BC-QA-01009 Vertical asymptote located and the one sided infinite limits stated

### Errors and misconceptions

- BC-ERR-01003 Nonexistence claimed because the function is undefined at the point
- BC-ERR-01017 Wrong branch evaluated at a boundary
- BC-ERR-01018 Cancelling factor reported as a vertical asymptote
- BC-MIS-01011 Every input missing from the domain is an asymptote, severity high

### Diagnostic signals

- No signal is scoped to this topic; the unit level signal list in data/staging/unit-01.signals.json applies.

### Adaptive metadata summary

Skills in this topic carry calculator relevance none. Remediation targets named across the topic: BC-PRQ-01001, BC-PRQ-01003, BC-PRQ-01009. Every skill record carries the full seven key adaptive block in data/staging/unit-01.skills.json. [inferred]

## 1.11 Defining Continuity at a Point

### Official mapping

Topic id BC-TOP-0111, CED code 1.11, name Defining Continuity at a Point, scope shared, CED page 48. [verified] (ced:48)

- BC-LO-LIM-2A (LIM-2.A): Justify conclusions about continuity at a point using the definition.
  - BC-EK-LIM-2A1 (LIM-2.A.1): "Types of discontinuities include removable discontinuities, jump discontinuities, and discontinuities due to vertical asymptotes."
  - BC-EK-LIM-2A2 (LIM-2.A.2): "A function f is continuous at x = c provided that f(c) exists, lim as x approaches c of f(x) exists, and lim as x approaches c of f(x) = f(c)."

Suggested practice skills: BC-MPS-3C (Practice skill 3.C). Weighting pointer: [../exam/exam-blueprint.md](../exam/exam-blueprint.md).

### Concept breakdown

- BC-CON-01013 Continuity at a point as three conditions: Continuity at a point needs the function value, the limit, and their agreement.

- BC-SKL-01043 State the three conditions of continuity at a point: Name the value, the limit, and their agreement.
- BC-SKL-01044 Test continuity at a point by checking the three conditions: Work through the three conditions in order and report the outcome.
- BC-SKL-01045 Justify a continuity conclusion by naming the failed condition: Point to the exact condition that breaks rather than restating the definition.

### Prerequisites

- BC-PRQ-06005 -> BC-SKL-01043, supporting, [inferred], Prerequisite for State the three conditions of continuity at a point.
- BC-PRQ-01003 -> BC-SKL-01044, supporting, [inferred], Prerequisite for Test continuity at a point by checking the three conditions.
- BC-PRQ-06005 -> BC-SKL-01045, supporting, [inferred], Prerequisite for Justify a continuity conclusion by naming the failed condition.
- BC-SKL-01023 -> BC-SKL-01044, hard_prerequisite, [inferred], Testing continuity at a boundary requires the one sided limits of the branches.
- BC-SKL-01043 -> BC-SKL-01044, hard_prerequisite, [inferred], The three conditions must be stated before they can be tested.
- BC-SKL-01044 -> BC-SKL-01045, hard_prerequisite, [inferred], A justification names the condition that the test found to fail.
- BC-SKL-01043 -> BC-TOP-0204, hard_prerequisite, [inferred], Continuity at a point is the conclusion drawn from differentiability in Unit 2 topic 2.4; no Unit 2 skill id exists in data/skills.json at the time of writing.

### Required mathematical knowledge

**Definition.** A function f is continuous at x equals c provided that f(c) exists, the limit of f(x) as x approaches c exists, and that limit equals f(c) (BC-EK-LIM-2A2). The three conditions are separate demands and the third presupposes the first two.

**Hypothesis checking as a skill.** The suggested practice skill for this topic is confirming whether the conditions of a selected definition have been satisfied (BC-MPS-3C, ced:48), so the three conditions are recorded as a stated skill (BC-SKL-01043) distinct from the test itself (BC-SKL-01044).

**Justification standard.** A scoring guideline refuses credit for a bare statement that a function is continuous and requires the reason, in that case that the function is differentiable (sg-25:12).

**Notation.** continuous at a point; the three conditions written as separate lines.

### Representations

Representations in play: BC-REP-01 Symbolic (analytical) expression, BC-REP-02 Graphical, BC-REP-04 Verbal description.

Conversions tested: a rule to a verdict with a reason (BC-REP-01 to BC-REP-04), and a graph to the same verdict (BC-REP-02 to BC-REP-04).

### Assessment behaviour

MCQ forms ask whether a piecewise function is continuous at a boundary. FRQ forms require continuity statements with reasons inside existence arguments, where the reason carries its own point (sg-25:12). Calculator variants are uncommon; no-calculator variants dominate. Conceptual variants ask which condition fails; computational variants require the one sided limits and the value; interpretation variants ask what a failure means for the graph; justification variants demand the failed condition and the values that show it. Multi-concept variants solve for a parameter in the same part (BC-QA-01008).

### Archetypes

- BC-QA-01006 Continuity at a point tested against the three conditions

### Errors and misconceptions

- BC-ERR-01001 Function value reported as the limit
- BC-ERR-01014 Continuity claimed from the function value alone
- BC-ERR-01015 Continuity claimed from matching one sided limits alone
- BC-ERR-01016 Definition restated in place of a reason
- BC-ERR-01017 Wrong branch evaluated at a boundary
- BC-MIS-01001 The limit at a point is the value of the function there, severity high
- BC-MIS-01009 Continuity is a single condition, severity high
- BC-MIS-01010 Restating a definition counts as a justification, severity high

### Diagnostic signals

- BC-SIG-01006 Three conditions listed but only one checked, mastery state partially_mastered
- BC-SIG-01007 Correct branch limits with the wrong conclusion about continuity, mastery state partially_mastered

### Adaptive metadata summary

Skills in this topic carry calculator relevance none. Remediation targets named across the topic: BC-PRQ-01003, BC-PRQ-06005. Every skill record carries the full seven key adaptive block in data/staging/unit-01.skills.json. [inferred]

## 1.12 Confirming Continuity over an Interval

### Official mapping

Topic id BC-TOP-0112, CED code 1.12, name Confirming Continuity over an Interval, scope shared, CED page 49. [verified] (ced:49)

- BC-LO-LIM-2B (LIM-2.B): Determine intervals over which a function is continuous.
  - BC-EK-LIM-2B1 (LIM-2.B.1): "A function is continuous on an interval if the function is continuous at each point in the interval."
  - BC-EK-LIM-2B2 (LIM-2.B.2): "Polynomial, rational, power, exponential, logarithmic, and trigonometric functions are continuous on all points in their domains."

Suggested practice skills: BC-MPS-1E (Practice skill 1.E). Weighting pointer: [../exam/exam-blueprint.md](../exam/exam-blueprint.md).

### Concept breakdown

- BC-CON-01014 Continuity on an interval: A function is continuous on an interval when it is continuous at every point of that interval.

- BC-SKL-01046 Determine intervals of continuity from the domain of an expression: Exclude the inputs where the expression is undefined and report the rest as intervals.
- BC-SKL-01047 Name the function families continuous on their domains: Recall which standard families are continuous wherever they are defined.
- BC-SKL-01048 Determine continuity of a piecewise function on an interval: Check each branch on its own and then each boundary.
- BC-SKL-01049 Distinguish continuity on an open interval from continuity on a closed interval: Treat the endpoints of a closed interval with one sided limits.

### Prerequisites

- BC-PRQ-01008 -> BC-SKL-01046, supporting, [inferred], Prerequisite for Determine intervals of continuity from the domain of an expression.
- BC-PRQ-01008 -> BC-SKL-01047, supporting, [inferred], Prerequisite for Name the function families continuous on their domains.
- BC-PRQ-01003 -> BC-SKL-01048, supporting, [inferred], Prerequisite for Determine continuity of a piecewise function on an interval.
- BC-PRQ-01010 -> BC-SKL-01049, supporting, [inferred], Prerequisite for Distinguish continuity on an open interval from continuity on a closed interval.
- BC-SKL-01047 -> BC-SKL-01046, hard_prerequisite, [inferred], Naming the families continuous on their domains supports reading intervals of continuity off the domain.
- BC-SKL-01046 -> BC-SKL-01048, hard_prerequisite, [inferred], Branch by branch continuity uses the domain based determination.

### Required mathematical knowledge

**Interval continuity.** A function is continuous on an interval if it is continuous at each point of the interval (BC-EK-LIM-2B1). At an endpoint of a closed interval the relevant condition is one sided.

**Families.** Polynomial, rational, power, exponential, logarithmic, and trigonometric functions are continuous on all points in their domains (BC-EK-LIM-2B2). The restriction to the domain is the working part of the statement.

**Notation.** continuous on an interval; open, closed, and half open interval notation.

### Representations

Representations in play: BC-REP-01 Symbolic (analytical) expression, BC-REP-04 Verbal description.

Conversions tested: an expression to a set of intervals (BC-REP-01 to BC-REP-01), and a family statement to a justification (BC-REP-04 to BC-REP-04).

### Assessment behaviour

MCQ forms ask for the intervals on which a given function is continuous. FRQ forms use interval continuity as the hypothesis of an existence or accumulation argument. Calculator variants are uncommon; no-calculator variants dominate. Conceptual variants ask why the domain restriction matters; computational variants require the excluded inputs; interpretation variants ask what continuity on an interval permits; justification variants require the family to be named. Multi-concept variants supply the hypothesis for the Intermediate Value Theorem in the following topic (BC-QA-01011).

### Archetypes

- BC-QA-01015 Intervals of continuity determined from the domain of an expression

### Errors and misconceptions

- BC-ERR-01031 Excluded input included inside a stated interval of continuity
- BC-ERR-01032 Closed bracket written at an excluded input
- BC-MIS-01019 Continuity is a property of a formula rather than of a domain, severity medium

### Diagnostic signals

- BC-SIG-01017 Intervals of continuity correct with a closed bracket at an excluded input, mastery state partially_mastered

### Adaptive metadata summary

Skills in this topic carry calculator relevance none. Remediation targets named across the topic: BC-PRQ-01003, BC-PRQ-01008, BC-PRQ-01010. Every skill record carries the full seven key adaptive block in data/staging/unit-01.skills.json. [inferred]

## 1.13 Removing Discontinuities

### Official mapping

Topic id BC-TOP-0113, CED code 1.13, name Removing Discontinuities, scope shared, CED page 50. [verified] (ced:50)

- BC-LO-LIM-2C (LIM-2.C): Determine values of x or solve for parameters that make discontinuous functions continuous, if possible.
  - BC-EK-LIM-2C1 (LIM-2.C.1): "If the limit of a function exists at a discontinuity in its graph, then it is possible to remove the discontinuity by defining or redefining the value of the function at that point, so it equals the value of the limit of the function as x approaches that point."
  - BC-EK-LIM-2C2 (LIM-2.C.2): "In order for a piecewise-defined function to be continuous at a boundary to the partition of its domain, the value of the expression defining the function on one side of the boundary must equal the value of the expression defining the other side of the boundary, as well as the value of the function at the boundary."

Suggested practice skills: BC-MPS-1E (Practice skill 1.E). Weighting pointer: [../exam/exam-blueprint.md](../exam/exam-blueprint.md).

### Concept breakdown

- BC-CON-01015 Removing a discontinuity and matching a piecewise function: A removable break can be repaired by defining the value to equal the limit, and a piecewise rule is made continuous by matching the two branch values at a boundary.

- BC-SKL-01050 Redefine a function value to remove a removable discontinuity: Set the value at the point equal to the limit there.
- BC-SKL-01051 Solve for a parameter making a piecewise function continuous at a boundary: Set the two branch values equal at the boundary and solve.
- BC-SKL-01052 Solve for two parameters using continuity conditions at two boundaries: Write one equation per boundary and solve the pair together.
- BC-SKL-01053 Decide whether a discontinuity can be removed: Check whether the limit exists before claiming the break can be repaired.

### Prerequisites

- BC-PRQ-01001 -> BC-SKL-01050, supporting, [inferred], Prerequisite for Redefine a function value to remove a removable discontinuity.
- BC-PRQ-01003 -> BC-SKL-01051, supporting, [inferred], Prerequisite for Solve for a parameter making a piecewise function continuous at a boundary.
- BC-PRQ-01003 -> BC-SKL-01052, supporting, [inferred], Prerequisite for Solve for two parameters using continuity conditions at two boundaries.
- BC-PRQ-01003 -> BC-SKL-01053, supporting, [inferred], Prerequisite for Decide whether a discontinuity can be removed.
- BC-SKL-01039 -> BC-SKL-01050, hard_prerequisite, [inferred], Removing a discontinuity requires that it be classified as removable first.
- BC-SKL-01044 -> BC-SKL-01051, hard_prerequisite, [inferred], Solving for a parameter applies the continuity test with an unknown in place.
- BC-SKL-01051 -> BC-SKL-01052, hard_prerequisite, [inferred], Two boundary conditions extend the single boundary case.

### Required mathematical knowledge

**Removing a discontinuity.** If the limit of a function exists at a discontinuity in its graph, the discontinuity can be removed by defining or redefining the value of the function at that point so that it equals the limit (BC-EK-LIM-2C1).

**Piecewise matching.** For a piecewise defined function to be continuous at a boundary of the partition, the value of the expression defining the function on one side must equal the value of the expression on the other side and the value of the function at the boundary (BC-EK-LIM-2C2). All three quantities enter the condition, not only the two one sided limits.

**When removal is impossible.** A jump or an infinite discontinuity cannot be removed, because the limit does not exist there.

**Notation.** the redefined function written as a piecewise rule with the repaired value.

### Representations

Representations in play: BC-REP-01 Symbolic (analytical) expression, BC-REP-02 Graphical.

Conversions tested: a rule with an unknown constant to an equation in that constant (BC-REP-01 to BC-REP-01).

### Assessment behaviour

MCQ forms ask for the constant that makes a piecewise function continuous. FRQ forms embed the matching condition in questions about functions defined in pieces. Calculator variants are uncommon; no-calculator variants dominate. Conceptual variants ask whether a given break can be removed at all; computational variants solve for one or two constants; interpretation variants describe the repair in words; justification variants require the matching equation to be displayed. Multi-concept variants combine the matching with a classification of the original break (BC-QA-01007).

### Archetypes

- BC-QA-01008 Parameter solved so that a piecewise function is continuous

### Errors and misconceptions

- BC-ERR-01003 Nonexistence claimed because the function is undefined at the point
- BC-ERR-01015 Continuity claimed from matching one sided limits alone
- BC-ERR-01017 Wrong branch evaluated at a boundary
- BC-MIS-01009 Continuity is a single condition, severity high

### Diagnostic signals

- BC-SIG-01008 Parameter solved from the limits with the function value unchecked, mastery state partially_mastered

### Adaptive metadata summary

Skills in this topic carry calculator relevance none. Remediation targets named across the topic: BC-PRQ-01001, BC-PRQ-01003. Every skill record carries the full seven key adaptive block in data/staging/unit-01.skills.json. [inferred]

## 1.14 Connecting Infinite Limits and Vertical Asymptotes

### Official mapping

Topic id BC-TOP-0114, CED code 1.14, name Connecting Infinite Limits and Vertical Asymptotes, scope shared, CED page 51. [verified] (ced:51)

- BC-LO-LIM-2D (LIM-2.D): Interpret the behavior of functions using limits involving infinity.
  - BC-EK-LIM-2D1 (LIM-2.D.1): "The concept of a limit can be extended to include infinite limits."
  - BC-EK-LIM-2D2 (LIM-2.D.2): "Asymptotic and unbounded behavior of functions can be described and explained using limits."
  - BC-EK-LIM-2D3 (LIM-2.D.3): "The concept of a limit can be extended to include limits at infinity."
  - BC-EK-LIM-2D4 (LIM-2.D.4): "Limits at infinity describe end behavior."
  - BC-EK-LIM-2D5 (LIM-2.D.5): "Relative magnitudes of functions and their rates of change can be compared using limits."

Suggested practice skills: BC-MPS-3D (Practice skill 3.D). Weighting pointer: [../exam/exam-blueprint.md](../exam/exam-blueprint.md).

### Concept breakdown

- BC-CON-01016 Infinite limits and vertical asymptotes: Values that grow without bound near an input mark a vertical asymptote there.

- BC-SKL-01054 Write an infinite limit using correct notation: Use the infinity symbol to record unbounded growth, with the side when it matters.
- BC-SKL-01055 Determine one sided infinite limits by sign analysis near a zero of the denominator: Work out the sign of the quotient on each side of the bad input.
- BC-SKL-01056 Identify vertical asymptotes from an expression after simplification: Simplify first, then read off where the remaining denominator vanishes.
- BC-SKL-01057 Distinguish a vertical asymptote from a removable discontinuity at the same input: Decide whether the factor cancels or survives.

### Prerequisites

- BC-PRQ-01009 -> BC-SKL-01054, supporting, [inferred], Prerequisite for Write an infinite limit using correct notation.
- BC-PRQ-01009 -> BC-SKL-01055, supporting, [inferred], Prerequisite for Determine one sided infinite limits by sign analysis near a zero of the denominator.
- BC-PRQ-01001 -> BC-SKL-01056, supporting, [inferred], Prerequisite for Identify vertical asymptotes from an expression after simplification.
- BC-PRQ-01001 -> BC-SKL-01057, supporting, [inferred], Prerequisite for Distinguish a vertical asymptote from a removable discontinuity at the same input.
- BC-SKL-01041 -> BC-SKL-01057, supporting, [inferred], Distinguishing an asymptote from a removable break uses both classifications.
- BC-SKL-01055 -> BC-SKL-01054, supporting, [inferred], Sign analysis supplies the content that the infinite limit notation records.
- BC-SKL-01054 -> BC-TOP-0613, hard_prerequisite, [inferred], Infinite limits underlie the improper integral treatment at Unit 6 topic 6.13.

### Required mathematical knowledge

**Infinite limits.** The concept of a limit can be extended to include infinite limits (BC-EK-LIM-2D1), and asymptotic and unbounded behaviour of functions can be described and explained using limits (BC-EK-LIM-2D2).

**What the notation claims.** A statement that a limit is infinite records unbounded growth and is not a claim that a real limit exists. The two sides must be treated separately whenever the sign of the quotient differs across the input.

**Locating asymptotes.** Simplify first. A factor that divides out produces a removable discontinuity rather than a vertical asymptote.

**Notation.** vertical asymptote; the one sided infinite limit written with the side marked.

### Representations

Representations in play: BC-REP-01 Symbolic (analytical) expression, BC-REP-02 Graphical.

Conversions tested: a rational expression to one sided infinite limit statements (BC-REP-01 to BC-REP-01), and those statements to a described graph (BC-REP-01 to BC-REP-02).

### Assessment behaviour

MCQ forms ask for the vertical asymptotes of a given function or for the behaviour near one. FRQ forms use unbounded behaviour inside questions about improper integrals and about graph analysis in later units. Calculator variants plot the behaviour; no-calculator variants use the algebraic form. Conceptual variants ask whether an infinite limit is an existing limit; computational variants ask for the locations; interpretation variants describe the behaviour in words; justification variants demand the sign analysis. Multi-concept variants place a removable break and an asymptote in the same expression (BC-QA-01009).

### Archetypes

- BC-QA-01007 Discontinuity classified from a rule or a graph
- BC-QA-01009 Vertical asymptote located and the one sided infinite limits stated

### Errors and misconceptions

- BC-ERR-01018 Cancelling factor reported as a vertical asymptote
- BC-ERR-01019 Two sided infinite limit written where the sides differ in sign
- BC-ERR-01020 Infinite limit reported as an existing real limit
- BC-MIS-01011 Every input missing from the domain is an asymptote, severity high
- BC-MIS-01012 Unbounded behaviour is the same on both sides, severity high
- BC-MIS-01018 All limit notation with an infinity symbol means the same thing, severity medium

### Diagnostic signals

- BC-SIG-01009 Asymptote located without simplification, mastery state not_mastered
- BC-SIG-01010 Correct asymptote with a single two sided infinite statement, mastery state partially_mastered

### Adaptive metadata summary

Skills in this topic carry calculator relevance none. Remediation targets named across the topic: BC-PRQ-01001, BC-PRQ-01009. Every skill record carries the full seven key adaptive block in data/staging/unit-01.skills.json. [inferred]

## 1.15 Connecting Limits at Infinity and Horizontal Asymptotes

### Official mapping

Topic id BC-TOP-0115, CED code 1.15, name Connecting Limits at Infinity and Horizontal Asymptotes, scope shared, CED page 52. [verified] (ced:52)

- BC-LO-LIM-2D (LIM-2.D): Interpret the behavior of functions using limits involving infinity.
  - BC-EK-LIM-2D1 (LIM-2.D.1): "The concept of a limit can be extended to include infinite limits."
  - BC-EK-LIM-2D2 (LIM-2.D.2): "Asymptotic and unbounded behavior of functions can be described and explained using limits."
  - BC-EK-LIM-2D3 (LIM-2.D.3): "The concept of a limit can be extended to include limits at infinity."
  - BC-EK-LIM-2D4 (LIM-2.D.4): "Limits at infinity describe end behavior."
  - BC-EK-LIM-2D5 (LIM-2.D.5): "Relative magnitudes of functions and their rates of change can be compared using limits."

Suggested practice skills: BC-MPS-2D (Practice skill 2.D). Weighting pointer: [../exam/exam-blueprint.md](../exam/exam-blueprint.md).

### Concept breakdown

- BC-CON-01017 Limits at infinity and horizontal asymptotes: The value a function settles towards for inputs of large magnitude is its end behaviour, and a finite value there is a horizontal asymptote.
- BC-CON-01018 Relative magnitude of growth compared by limits: A quotient of two growing quantities tells which one grows faster.

- BC-SKL-01058 Evaluate the limit of a rational function at infinity by comparing degrees: Compare the top and bottom degrees to get the end value.
- BC-SKL-01059 Identify horizontal asymptotes from limits at infinity: Turn a finite end behaviour value into a horizontal asymptote.
- BC-SKL-01060 Write a limit expression describing end behaviour in context: Write the limit statement that answers a question about long run behaviour.
- BC-SKL-01061 Evaluate limits at infinity for expressions containing radicals: Divide by the dominant power and treat the sign of the variable carefully under the radical.
- BC-SKL-01062 Compare relative magnitudes of growth using limits: Use the limit of a quotient to say which quantity outgrows the other.
- BC-SKL-01063 Distinguish the limit at positive infinity from the limit at negative infinity: Check both ends separately because they can differ.

### Prerequisites

- BC-PRQ-01004 -> BC-SKL-01058, supporting, [inferred], Prerequisite for Evaluate the limit of a rational function at infinity by comparing degrees.
- BC-PRQ-01004 -> BC-SKL-01059, supporting, [inferred], Prerequisite for Identify horizontal asymptotes from limits at infinity.
- BC-PRQ-06005 -> BC-SKL-01060, supporting, [inferred], Prerequisite for Write a limit expression describing end behaviour in context.
- BC-PRQ-01004 -> BC-SKL-01061, supporting, [inferred], Prerequisite for Evaluate limits at infinity for expressions containing radicals.
- BC-PRQ-01004 -> BC-SKL-01062, supporting, [inferred], Prerequisite for Compare relative magnitudes of growth using limits.
- BC-PRQ-01004 -> BC-SKL-01063, supporting, [inferred], Prerequisite for Distinguish the limit at positive infinity from the limit at negative infinity.
- BC-SKL-01058 -> BC-SKL-01059, hard_prerequisite, [inferred], A horizontal asymptote is read off a limit at infinity.
- BC-SKL-01058 -> BC-SKL-01061, hard_prerequisite, [inferred], The radical case extends the degree comparison method.
- BC-SKL-01059 -> BC-SKL-01063, supporting, [inferred], Two ends are handled by the same method applied twice.
- BC-SKL-01058 -> BC-TOP-0407, hard_prerequisite, [inferred], Limits at infinity and indeterminate forms are the setting for L'Hospital's rule at Unit 4 topic 4.7.
- BC-SKL-01059 -> BC-TOP-0506, supporting, [inferred], Horizontal asymptotes contribute to the graph analysis of Unit 5.
- BC-SKL-01058 -> BC-TOP-0613, hard_prerequisite, [inferred], Limits at infinity underlie the improper integral treatment at Unit 6 topic 6.13.
- BC-SKL-01062 -> BC-TOP-1004, supporting, [inferred], Relative magnitude comparison by limits supports the comparison tests of Unit 10.

### Required mathematical knowledge

**Limits at infinity.** The concept of a limit can be extended to include limits at infinity (BC-EK-LIM-2D3) and limits at infinity describe end behaviour (BC-EK-LIM-2D4).

**Horizontal asymptotes.** A finite limit L as the variable increases or decreases without bound gives the horizontal asymptote y equals L. The two ends may give different values.

**Relative magnitudes.** Relative magnitudes of functions and their rates of change can be compared using limits (BC-EK-LIM-2D5).

**Method.** Divide numerator and denominator by the dominant power, or compare degrees. Under a square root the dominant power carries a sign that depends on the end being examined.

**Notation.** horizontal asymptote; end behaviour; the limit written with the variable increasing or decreasing without bound.

### Representations

Representations in play: BC-REP-01 Symbolic (analytical) expression, BC-REP-02 Graphical, BC-REP-05 Contextual model.

Conversions tested: a model in context to a limit expression (BC-REP-05 to BC-REP-01), and a limit at infinity to a horizontal asymptote on a graph (BC-REP-01 to BC-REP-02).

### Assessment behaviour

MCQ forms ask for a limit at infinity or for the horizontal asymptotes of a graph. FRQ forms ask for a limit expression describing end behaviour in a contextual model and then for its value, with separate points for the expression and the value; the expression point is available for the limit of either the amount or its rate, a response presenting the limit of the amount is not eligible for the value point, and arithmetic performed with the infinity symbol is treated as scratch work (sg-25:4). Calculator variants supply a formula in a modelling context; no-calculator variants use a bare rational or radical expression. Conceptual variants ask what end behaviour means; computational variants ask for the value; interpretation variants ask what the long run behaviour says about the modelled quantity; justification variants ask why the comparison of degrees settles the value. Multi-concept variants compare the growth of two quantities in the same part.

### Archetypes

- BC-QA-01010 End behaviour described by a limit at infinity

### Errors and misconceptions

- BC-ERR-01021 Infinity substituted as a number
- BC-ERR-01022 Limit of the amount presented where the limit of the rate was requested
- BC-ERR-01023 End behaviour decided by the leading coefficients without comparing degrees
- BC-ERR-01024 Sign under a radical ignored at negative infinity
- BC-ERR-01033 Limit at infinity confused with an infinite limit
- BC-MIS-01013 Infinity is a number that can be substituted, severity high
- BC-MIS-01014 The end behaviour of a quantity and of its rate are interchangeable, severity high
- BC-MIS-01018 All limit notation with an infinity symbol means the same thing, severity medium

### Diagnostic signals

- BC-SIG-01011 End behaviour value correct with no limit expression presented, mastery state partially_mastered
- BC-SIG-01012 Limit expression written for the amount rather than the rate, mastery state not_mastered

### Adaptive metadata summary

Skills in this topic carry calculator relevance none, optional. Remediation targets named across the topic: BC-PRQ-01004, BC-PRQ-06005. Every skill record carries the full seven key adaptive block in data/staging/unit-01.skills.json. [inferred]

## 1.16 Working with the Intermediate Value Theorem (IVT)

### Official mapping

Topic id BC-TOP-0116, CED code 1.16, name Working with the Intermediate Value Theorem (IVT), scope shared, CED page 53. [verified] (ced:53)

- BC-LO-FUN-1A (FUN-1.A): Explain the behavior of a function on an interval using the Intermediate Value Theorem.
  - BC-EK-FUN-1A1 (FUN-1.A.1): "If f is a continuous function on the closed interval [a, b] and d is a number between f(a) and f(b), then the Intermediate Value Theorem guarantees that there is at least one number c between a and b, such that f(c) = d."

Suggested practice skills: BC-MPS-3E (Practice skill 3.E). Weighting pointer: [../exam/exam-blueprint.md](../exam/exam-blueprint.md).

### Concept breakdown

- BC-CON-01019 The Intermediate Value Theorem: A continuous function on a closed interval takes every value between its endpoint values at least once.

- BC-SKL-01064 State the hypotheses of the Intermediate Value Theorem: Name continuity on a closed interval and the target value lying between the endpoint values.
- BC-SKL-01065 Verify the continuity hypothesis before applying the theorem: Say why the function is continuous on the interval, with a reason.
- BC-SKL-01066 Verify that the target value lies between the endpoint values: Show the wanted output sits between the two endpoint outputs.
- BC-SKL-01067 State the conclusion of the theorem with the correct interval: Say that at least one input in the open interval gives the wanted output.
- BC-SKL-01068 Apply the Intermediate Value Theorem to a function given by a table: Use two table rows that straddle the target value, having first established continuity.

### Prerequisites

- BC-PRQ-01010 -> BC-SKL-01064, supporting, [inferred], Prerequisite for State the hypotheses of the Intermediate Value Theorem.
- BC-PRQ-01008 -> BC-SKL-01065, supporting, [inferred], Prerequisite for Verify the continuity hypothesis before applying the theorem.
- BC-PRQ-01010 -> BC-SKL-01066, supporting, [inferred], Prerequisite for Verify that the target value lies between the endpoint values.
- BC-PRQ-01010 -> BC-SKL-01067, supporting, [inferred], Prerequisite for State the conclusion of the theorem with the correct interval.
- BC-PRQ-01010 -> BC-SKL-01068, supporting, [inferred], Prerequisite for Apply the Intermediate Value Theorem to a function given by a table.
- BC-SKL-01064 -> BC-SKL-01065, hard_prerequisite, [inferred], The hypotheses must be known before one of them can be verified.
- BC-SKL-01064 -> BC-SKL-01066, hard_prerequisite, [inferred], The hypotheses must be known before one of them can be verified.
- BC-SKL-01065 -> BC-SKL-01067, hard_prerequisite, [inferred], The conclusion may be stated only once the hypotheses are established.
- BC-SKL-01066 -> BC-SKL-01067, hard_prerequisite, [inferred], The conclusion may be stated only once the hypotheses are established.
- BC-SKL-01067 -> BC-SKL-01068, hard_prerequisite, [inferred], The tabular application assembles the hypotheses and the conclusion.
- BC-SKL-01043 -> BC-SKL-01065, hard_prerequisite, [inferred], Verifying the continuity hypothesis rests on the definition of continuity.
- BC-SKL-01065 -> BC-TOP-0504, supporting, [inferred], The continuity hypothesis recurs in the existence theorems of Unit 5.
- BC-SKL-01067 -> BC-TOP-0501, supporting, [inferred], Existence conclusions of the Intermediate Value Theorem pattern the Mean Value Theorem conclusions in Unit 5 topic 5.1.

### Required mathematical knowledge

**Intermediate Value Theorem.** If f is a continuous function on the closed interval from a to b and d is a number between f(a) and f(b), then the theorem guarantees that there is at least one number c between a and b such that f(c) equals d (BC-EK-FUN-1A1).

**Hypotheses stated separately.** Two hypotheses must hold: continuity on the closed interval, and the target value lying between the endpoint values. They are recorded here as BC-SKL-01064, BC-SKL-01065, and BC-SKL-01066 because a scoring guideline awards a point for the continuity hypothesis on its own and requires a reason for it (sg-25:12).

**Conclusion.** Existence of at least one input, not uniqueness and not a located value. The conclusion is stated on the open interval named in the question.

**Notation.** Intermediate Value Theorem; the straddling inequality written with the target value in the middle.

### Representations

Representations in play: BC-REP-03 Numerical table, BC-REP-04 Verbal description, BC-REP-05 Contextual model, BC-REP-02 Graphical.

Conversions tested: a table of values to an existence claim (BC-REP-03 to BC-REP-04), and a contextual model to the hypotheses of the theorem (BC-REP-05 to BC-REP-04).

### Assessment behaviour

MCQ forms ask whether the theorem guarantees a solution on an interval. FRQ forms ask whether there must be an input at which a tabulated quantity attains a named value and demand a justification; one point is earned for stating that the function is continuous because it is differentiable, with a bare continuity claim refused, and a second point requires the straddling values, a continuity statement, and an affirmative answer, where naming the theorem is optional but a named theorem must be correct (sg-25:12). Calculator variants supply a formula and a numerical solve; no-calculator variants supply a table. Conceptual variants ask which hypothesis is missing; computational variants evaluate the endpoint values; interpretation variants phrase the conclusion in the language of the context; justification variants demand the full argument. Multi-concept variants pair the existence argument with a derivative estimate from the same table (sg-25:11, sg-25:12).

### Archetypes

- BC-QA-01011 Existence of a solution argued from the Intermediate Value Theorem

### Errors and misconceptions

- BC-ERR-01016 Definition restated in place of a reason
- BC-ERR-01025 Continuity asserted without a reason in an existence argument
- BC-ERR-01026 Straddling inequality omitted or reversed
- BC-ERR-01027 Uniqueness claimed from an existence theorem
- BC-ERR-01028 Wrong existence theorem named
- BC-MIS-01010 Restating a definition counts as a justification, severity high
- BC-MIS-01015 A hypothesis is satisfied because the question implies it, severity high
- BC-MIS-01016 An existence theorem locates or counts solutions, severity medium

### Diagnostic signals

- BC-SIG-01013 Straddling inequality correct with continuity asserted bare, mastery state partially_mastered
- BC-SIG-01014 Continuity justified correctly with no straddling values shown, mastery state partially_mastered
- BC-SIG-01015 Existence argument complete but phrased as a unique solution, mastery state partially_mastered

### Adaptive metadata summary

Skills in this topic carry calculator relevance none. Remediation targets named across the topic: BC-PRQ-01008, BC-PRQ-01010. Every skill record carries the full seven key adaptive block in data/staging/unit-01.skills.json. [inferred]

## Cross-unit connections

Cross-unit edges use BC-TOP ids as the node on the other unit's side wherever no skill exists in data/skills.json for that unit; the `notes` field on each edge in data/staging/unit-01.edges.csv describes the skill that the topic id stands in for. [inferred]

### What Unit 1 depends on

Unit 1 opens the course, so it depends on no other unit. Its ten non-calculus prerequisites BC-PRQ-01001 to BC-PRQ-01010 carry that load, together with the existing BC-PRQ-06005 for reading function notation, composition, and evaluation, which is reused rather than minted again. [inferred]

### What depends on Unit 1

**Unit 2.** BC-SKL-01003, the instantaneous rate as a limit of average rates, is the definition of the derivative at BC-TOP-0201 and BC-TOP-0202. BC-SKL-01024 and BC-SKL-01021, algebraic rewriting and direct substitution, are the steps that resolve the difference quotient limit at BC-TOP-0202. BC-SKL-01043, the three conditions of continuity, and BC-SKL-01040, jump classification, are what BC-TOP-0204 reasons with when it relates differentiability to continuity, and a 2023 scoring guideline runs that implication in the direction Unit 2 states it, from differentiability at a point to continuity there (sg-23:14).

**Unit 4.** BC-SKL-01028, recognising an indeterminate form, and BC-SKL-01058, limits at infinity, are the entry conditions for L'Hospital's rule at BC-TOP-0407. Unit 1 handles the same forms by algebra only; the rule itself is out of scope here, and the 2023 free response part that resolves an indeterminate quotient does so with the rule and so belongs to Unit 4 (sg-23:14).

**Unit 5.** BC-SKL-01065 and BC-SKL-01067, the continuity hypothesis and the existence conclusion, pattern the Mean Value Theorem and the Extreme Value Theorem arguments at BC-TOP-0501 and BC-TOP-0504, and BC-SKL-01059 contributes horizontal asymptotes to the graph analysis at BC-TOP-0506.

**Unit 6.** BC-SKL-01054 and BC-SKL-01058 are what make an improper integral meaningful at BC-TOP-0613, since the integral is rewritten as a limit of definite integrals.

**Unit 10.** BC-SKL-01015, reading a limit from a sequence of values, supports convergence of sequences at BC-TOP-1001, and BC-SKL-01062, relative magnitude comparison, supports the comparison tests at BC-TOP-1004.

## Archetype summary

Fifteen archetypes with forty eight variants are recorded in data/staging/unit-01.archetypes.json. Variant dimensions used are representation, reasoning direction, notation, and context. Free response grounding for Unit 1 in 2023 to 2025 is thin: continuity and limit work appears inside larger questions rather than as questions of its own, so only BC-QA-01010 and BC-QA-01011 are tagged verified against a rubric, BC-QA-01004 is tagged single-source against the 2023 indeterminate form part whose resolution belongs to Unit 4, and the remaining twelve are tagged inferred. [verified] (sg-25:4, sg-25:12, sg-23:14)

| Archetype | Name | Scope | Calculator | Official parts read |
|---|---|---|---|---|
| BC-QA-01001 | Limit estimated from a graph including one sided values | shared | no_calculator | none in 2023 to 2025 [inferred] |
| BC-QA-01002 | Limit estimated from a table of values | shared | either | none in 2023 to 2025 [inferred] |
| BC-QA-01003 | Limit evaluated by limit theorems from given limits or tabulated values | shared | no_calculator | none in 2023 to 2025 [inferred] |
| BC-QA-01004 | Indeterminate limit resolved by algebraic rewriting | shared | no_calculator | 2023 Q4(c) treats the same indeterminate form through L'Hospital's rule rather than algebraic rewriting |
| BC-QA-01005 | Limit determined by the squeeze theorem with its hypotheses stated | shared | no_calculator | none in 2023 to 2025 [inferred] |
| BC-QA-01006 | Continuity at a point tested against the three conditions | shared | no_calculator | none in 2023 to 2025 as a standalone part [inferred] |
| BC-QA-01007 | Discontinuity classified from a rule or a graph | shared | no_calculator | none in 2023 to 2025 [inferred] |
| BC-QA-01008 | Parameter solved so that a piecewise function is continuous | shared | no_calculator | none in 2023 to 2025 [inferred] |
| BC-QA-01009 | Vertical asymptote located and the one sided infinite limits stated | shared | no_calculator | none in 2023 to 2025 [inferred] |
| BC-QA-01010 | End behaviour described by a limit at infinity | shared | either | 2025 Q2(C) |
| BC-QA-01011 | Existence of a solution argued from the Intermediate Value Theorem | shared | no_calculator | 2025 Q3(B) |
| BC-QA-01012 | Instantaneous rate approached through average rates over shrinking intervals | shared | either | none in 2023 to 2025 as a standalone part [inferred] |
| BC-QA-01013 | Limit claim matched across graphical, numerical, and analytic representations | shared | no_calculator | none in 2023 to 2025 [inferred] |
| BC-QA-01014 | Procedure selected for a limit from the form of the expression | shared | no_calculator | none in 2023 to 2025 [inferred] |
| BC-QA-01015 | Intervals of continuity determined from the domain of an expression | shared | no_calculator | none in 2023 to 2025 [inferred] |

## Misconception summary

Nineteen misconceptions are recorded in data/staging/unit-01.misconceptions.json against thirty three observed errors in data/staging/unit-01.errors.json. The mapping is many to many: an error lists every misconception that could produce it together with non-conceptual causes such as an arithmetic slip, a misread, or time pressure, and every misconception carries rival misconceptions and a discriminating probe. Six misconceptions are tagged verified or single-source because a scoring guideline names the behaviour directly; the rest are inferred from the CED text. [verified] (sg-25:4, sg-25:12, sg-23:14)

| Misconception | Severity | Rivals | Discriminating probe |
|---|---|---|---|
| BC-MIS-01001 The limit at a point is the value of the function there | high | BC-MIS-01002 | Give a graph with an open circle at one height and a closed point at another over the same input and ask for the limit and the value separately. |
| BC-MIS-01002 A limit exists whenever the function approaches something on one side | high | BC-MIS-01001 | Ask for the left hand limit and the right hand limit as separate answers, then ask whether the two sided limit exists. |
| BC-MIS-01003 A limit is a prediction the function must eventually reach | medium | BC-MIS-01001 | Ask whether a function can have a limit at an input where it is undefined, and ask for an example. |
| BC-MIS-01004 A table settles the behaviour of a function | medium | BC-MIS-01003 | Ask what the function does at inputs between two adjacent rows of the table. |
| BC-MIS-01005 Limit theorems apply unconditionally | high | BC-MIS-01006 | Ask the student to state the condition each theorem requires and to point to where it was checked. |
| BC-MIS-01006 An indeterminate form is a value | high | BC-MIS-01005 | Give two expressions with the same indeterminate form and different limits and ask for both values. |
| BC-MIS-01007 Rewriting an expression may change any matching symbols | high | BC-MIS-01006 | Ask the student to evaluate the original and the rewritten expression at one convenient input and compare. |
| BC-MIS-01008 The squeeze theorem is a substitution rule | medium | BC-MIS-01010 | Ask whether the bounding inequality must hold at the target input itself for the theorem to apply. |
| BC-MIS-01009 Continuity is a single condition | high | BC-MIS-01001 | Give one function defined at the point with unequal one sided limits and one whose limit exists but differs from the value, and ask about continuity in both. |
| BC-MIS-01010 Restating a definition counts as a justification | high | BC-MIS-01009 | Ask which feature of the given function or table makes the stated claim true. |
| BC-MIS-01011 Every input missing from the domain is an asymptote | high | BC-MIS-01012 | Ask for the limit of the expression at that input after factoring numerator and denominator. |
| BC-MIS-01012 Unbounded behaviour is the same on both sides | high | BC-MIS-01011 | Ask for the sign of the quotient just to the left and just to the right of the input. |
| BC-MIS-01013 Infinity is a number that can be substituted | high | BC-MIS-01012 | Ask the student to divide numerator and denominator by the dominant power and to say what each resulting term approaches. |
| BC-MIS-01014 The end behaviour of a quantity and of its rate are interchangeable | high | BC-MIS-01013 | Ask for the units of the limit just written and compare them with the units the question asks about. |
| BC-MIS-01015 A hypothesis is satisfied because the question implies it | high | BC-MIS-01010 | Ask what in the question establishes that the function is continuous on the interval. |
| BC-MIS-01016 An existence theorem locates or counts solutions | medium | BC-MIS-01015 | Ask whether the theorem rules out a second input with the same output and what it would take to find one. |
| BC-MIS-01017 An average rate over an interval is the rate at a point in it | high | BC-MIS-01018 | Ask for the average rate over two different intervals containing the same point and ask which one is the rate at that point. |
| BC-MIS-01018 All limit notation with an infinity symbol means the same thing | medium | BC-MIS-01013 | Ask the student to point to where the infinity symbol sits in each of two statements and to say what each claims. |
| BC-MIS-01019 Continuity is a property of a formula rather than of a domain | medium | BC-MIS-01011 | Ask for the inputs at which the expression is undefined before any interval is written. |

## Unresolved

- No 2023 to 2025 free response question assesses Unit 1 as its main subject. The parts that touch it are 2025 Q3(B), an Intermediate Value Theorem argument (sg-25:12), 2025 Q2(C), an end behaviour limit expression (sg-25:4), and 2023 Q4(c), an indeterminate quotient resolved by L'Hospital's rule and opened by the statement that differentiability at a point gives continuity there (sg-23:14). Archetypes BC-QA-01001, BC-QA-01002, BC-QA-01003, BC-QA-01005, BC-QA-01006, BC-QA-01007, BC-QA-01008, BC-QA-01009, BC-QA-01012, BC-QA-01013, BC-QA-01014, and BC-QA-01015 have no matching free response part in those years and are tagged inferred; their scoring patterns are drawn from the CED description of the topic and from the nearest analogous rubric rather than from a rubric for that exact task. [uncertain]
- BC-QA-01004 covers indeterminate forms resolved by algebra, which is what Unit 1 topic 1.6 requires. The only official part read here with that form resolves it by L'Hospital's rule, which the CED places at topic 4.7 (BC-TOP-0407). The scoring behaviour quoted for the archetype, that a limit presented as equal to zero over zero does not earn the point for establishing the form, comes from that part and is carried across as a single-source claim about how the form must be presented. [single-source] (sg-23:14)
- data/curriculum.json records no learning objective for topics 1.7 and 1.9, and ced:44 and ced:46 confirm that the CED states only a skill focus for both. Skills for these topics are therefore attached to concepts rather than to essential knowledge statements, and their `learning_objectives` and `essential_knowledge` fields are empty. [verified] (ced:44, ced:46)
- The CED page numbering used in citations is the PDF page index in cache/text/ced, which runs eleven ahead of the printed page numbers on those pages for this unit. [verified] (ced:38, ced:53)
- The epsilon delta definition of a limit is excluded from assessment by an explicit exclusion statement, so no skill is recorded for it. [verified] (ced:39)
- No misconception literature is cited. None could be confirmed from the sources available in this project's cache, so every misconception record is tagged inferred unless a scoring guideline names the behaviour directly. [inferred]

<!-- generated:official-evidence:start -->

## Official evidence index [verified]

Generated from data/frq_records.json and data/mcq_records.json. Every record cites its cached document and page; counts are observations over the indexed years only, not predictions. FRQ part records with BC-UNIT-01 as primary or secondary unit: 12. Public sample MCQ records tagged to this unit: 8.

| FRQ record | Role | Calculator | Archetype | Skills (first six) | Points | Point types |
|---|---|---|---|---|---|---|
| BC-FRQ-2014-Q4-B | primary | no_calculator | BC-QA-01011 | BC-SKL-01064, BC-SKL-01065, BC-SKL-01066, BC-SKL-01067, BC-SKL-01068, BC-SKL-02019 | 2 | BC-PT-99015, BC-PT-99016 |
| BC-FRQ-2019-Q2-D | secondary | calculator | BC-QA-09012 | BC-SKL-09035, BC-SKL-09036, BC-SKL-09038, BC-SKL-01060 | 2 | BC-PT-99001, BC-PT-99005 |
| BC-FRQ-2019-Q3-D | primary | no_calculator | BC-QA-01003 | BC-SKL-01018, BC-SKL-01019, BC-SKL-01020, BC-SKL-01021 | 1 | BC-PT-99004 |
| BC-FRQ-2019-Q5-C | secondary | no_calculator | BC-QA-06011 | BC-SKL-06066, BC-SKL-06067, BC-SKL-06069, BC-SKL-06070 | 3 | BC-PT-99053, BC-PT-99003, BC-PT-99005 |
| BC-FRQ-2021-Q4-C | secondary | no_calculator | BC-QA-04009 | BC-SKL-04033, BC-SKL-04034, BC-SKL-04035, BC-SKL-04036, BC-SKL-06018 | 2 | BC-PT-99055, BC-PT-99005 |
| BC-FRQ-2022-Q4-B | primary | no_calculator | BC-QA-01011 | BC-SKL-01064, BC-SKL-01065, BC-SKL-01066, BC-SKL-01067, BC-SKL-02019 | 2 | BC-PT-99015, BC-PT-99016 |
| BC-FRQ-2023-Q4-C | secondary | no_calculator | BC-QA-04009 | BC-SKL-04033, BC-SKL-04034, BC-SKL-04035, BC-SKL-04036, BC-SKL-02019, BC-SKL-04038 | 3 | BC-PT-99054, BC-PT-99055, BC-PT-99005 |
| BC-FRQ-2023-Q5-B | secondary | no_calculator | BC-QA-06011 | BC-SKL-06066, BC-SKL-06067, BC-SKL-06068, BC-SKL-06040, BC-SKL-01058 | 3 | BC-PT-99053, BC-PT-99003, BC-PT-99004 |
| BC-FRQ-2025-Q1-C | primary | calculator | BC-QA-01010 | BC-SKL-01060, BC-SKL-01058, BC-SKL-01054, BC-SKL-04016 | 2 | BC-PT-99054, BC-PT-99004 |
| BC-FRQ-2025-Q3-B | primary | no_calculator | BC-QA-01011 | BC-SKL-01064, BC-SKL-01065, BC-SKL-01066, BC-SKL-01067, BC-SKL-01068, BC-SKL-02019 | 2 | BC-PT-99015, BC-PT-99016 |
| BC-FRQ-2026-Q1-D | primary | calculator | BC-QA-01011 | BC-SKL-01064, BC-SKL-01065, BC-SKL-01066, BC-SKL-01067, BC-SKL-02019 | 2 | BC-PT-99015, BC-PT-99016 |
| BC-FRQ-2026-Q5-D | secondary | no_calculator | BC-QA-06011 | BC-SKL-06066, BC-SKL-06067, BC-SKL-06068, BC-SKL-06041, BC-SKL-01058 | 3 | BC-PT-99053, BC-PT-99003, BC-PT-99004 |

| MCQ record | Calculator | Archetype | Skills |
|---|---|---|---|
| BC-MCQ-CED-001 | no_calculator | BC-QA-01004 | BC-SKL-01027, BC-SKL-01024, BC-SKL-01028 |
| BC-MCQ-CED-011 | calculator | BC-QA-01001 | BC-SKL-01010, BC-SKL-01008, BC-SKL-01011 |
| BC-MCQ-SAMPLE-002 | no_calculator | BC-QA-01004 | BC-SKL-01027, BC-SKL-01024, BC-SKL-01007 |
| BC-MCQ-SAMPLE-003 | no_calculator | BC-QA-02005 | BC-SKL-02022, BC-SKL-02023, BC-SKL-01042 |
| BC-MCQ-SAMPLE-006 | no_calculator | BC-QA-02002 | BC-SKL-02006, BC-SKL-02007, BC-SKL-01007 |
| BC-MCQ-PE2012-011 | no_calculator | BC-QA-02005 | BC-SKL-02022, BC-SKL-02021, BC-SKL-01044 |
| BC-MCQ-PE2012-021 | no_calculator | BC-QA-01010 | BC-SKL-01058, BC-SKL-01059, BC-SKL-01063 |
| BC-MCQ-PE2012-036 | calculator | BC-QA-01006 | BC-SKL-01043, BC-SKL-01044, BC-SKL-01045 |

<!-- generated:official-evidence:end -->
