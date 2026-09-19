---
title: Unit 2, Differentiation: Definition and Fundamental Properties
research_date: 2026-09-19
status: draft
purpose: Decompose CED Unit 2 into concepts, atomic skills, non-calculus prerequisites, question archetypes and variants, observed errors, candidate misconceptions, and diagnostic signals, each grounded in the CED text and in the 2023 to 2025 official free-response questions and scoring guidelines.
---

# Unit 2, Differentiation: Definition and Fundamental Properties

BC-UNIT-02 covers CED pages 60 to 69 and holds ten topics, all shared with AB. data/curriculum.json names the unit Differentiation: Definition and Fundamental Properties while the CED pages carry the running head Differentiation: Definition and Fundamental Properties; this file uses the curriculum record for the unit name and notes the difference under Unresolved. Unit weighting is in [../exam/exam-blueprint.md](../exam/exam-blueprint.md) and exam composition is in [../exam/exam-structure.md](../exam/exam-structure.md). [verified] (ced:60, ced:69)

## 2.1 Defining Average and Instantaneous Rates of Change at a Point

### Official mapping

Topic id BC-TOP-0201, CED code 2.1, name Defining Average and Instantaneous Rates of Change at a Point, scope shared, CED page 60. [verified] (ced:60)

- BC-LO-CHA-2A (CHA-2.A): Determine average rates of change using difference quotients.
  - BC-EK-CHA-2A1 (CHA-2.A.1): "The difference quotients (f(a + h) - f(a))/h and (f(x) - f(a))/(x - a) express the average rate of change of a function over an interval."
- BC-LO-CHA-2B (CHA-2.B): Represent the derivative of a function as the limit of a difference quotient.
  - BC-EK-CHA-2B1 (CHA-2.B.1): "The instantaneous rate of change of a function at x = a can be expressed by lim as h approaches 0 of (f(a + h) - f(a))/h or lim as x approaches a of (f(x) - f(a))/(x - a), provided the limit exists. These are equivalent forms of the definition of the derivative and are denoted f'(a)."
  - BC-EK-CHA-2B2 (CHA-2.B.2): "The derivative of f is the function whose value at x is lim as h approaches 0 of (f(x + h) - f(x))/h, provided this limit exists."
  - BC-EK-CHA-2B3 (CHA-2.B.3): "For y = f(x), notations for the derivative include dy/dx, f'(x), and y'."
  - BC-EK-CHA-2B4 (CHA-2.B.4): "The derivative can be represented graphically, numerically, analytically, and verbally."

Suggested practice skills: BC-MPS-2B (Practice skill 2.B). Weighting pointer: [../exam/exam-blueprint.md](../exam/exam-blueprint.md).

### Concept breakdown

- BC-CON-02001 Average rate of change as a difference quotient: An average rate is the change in the output divided by the change in the input over an interval.
- BC-CON-02002 Instantaneous rate of change as the limit of a difference quotient: The rate at a point is what the average rates approach as the interval shrinks to nothing.

- BC-SKL-02001 Compute an average rate of change from the increment difference quotient: Use the quotient of the change in the function over an increment added to the base point.
- BC-SKL-02002 Compute an average rate of change from the two point difference quotient: Use the quotient of the change in the function over the change in the input between two named inputs.
- BC-SKL-02003 Interpret an average rate of change in context with units: Say what the computed average rate means for the situation and attach its units.
- BC-SKL-02004 Distinguish an average rate of change from an instantaneous rate of change: Say which of the two describes an interval and which describes a single moment.
- BC-SKL-02005 Express an instantaneous rate of change as a limit of average rates: Write the rate at a point as the limit of the difference quotient.

### Prerequisites

- BC-PRQ-02001 -> BC-SKL-02001, supporting, [inferred], Prerequisite for Compute an average rate of change from the increment difference quotient.
- BC-PRQ-02005 -> BC-SKL-02001, supporting, [inferred], Prerequisite for Compute an average rate of change from the increment difference quotient.
- BC-SKL-01001 -> BC-SKL-02002, supporting, [inferred], Prerequisite for Compute an average rate of change from the two point difference quotient.
- BC-SKL-01001 -> BC-SKL-02003, supporting, [inferred], Prerequisite for Interpret an average rate of change in context with units.
- BC-SKL-01003 -> BC-SKL-02004, supporting, [inferred], Prerequisite for Distinguish an average rate of change from an instantaneous rate of change.
- BC-SKL-01003 -> BC-SKL-02005, supporting, [inferred], Prerequisite for Express an instantaneous rate of change as a limit of average rates.
- BC-SKL-01005 -> BC-SKL-02005, supporting, [inferred], Prerequisite for Express an instantaneous rate of change as a limit of average rates.
- BC-SKL-02004 -> BC-SKL-02005, hard_prerequisite, [inferred], Separating the two kinds of rate precedes writing the limit that connects them.
- BC-SKL-02003 -> BC-TOP-0401, hard_prerequisite, [inferred], Interpreting a derivative in context with units is the subject of Unit 4 topic 4.1.

### Required mathematical knowledge

**Difference quotients.** The two difference quotients, the quotient of f(a plus h) minus f(a) by h and the quotient of f(x) minus f(a) by x minus a, both express the average rate of change of a function over an interval (BC-EK-CHA-2A1).

**Instantaneous rate.** The instantaneous rate of change of a function at an input can be expressed by the limit of either difference quotient, provided the limit exists; the two are equivalent forms of the definition of the derivative and are denoted by the prime notation at that input (BC-EK-CHA-2B1).

**Cross-unit dependency.** The limit that defines the instantaneous rate is the Unit 1 limit concept (BC-SKL-01003), and the indeterminate form the difference quotient takes at zero increment is handled by the Unit 1 rewriting skills (BC-SKL-01024).

**Notation.** difference quotient; average rate of change; f prime of a.

### Representations

Representations in play: BC-REP-01 Symbolic (analytical) expression, BC-REP-03 Numerical table, BC-REP-05 Contextual model, BC-REP-04 Verbal description.

Conversions tested: contextual model to a difference quotient (BC-REP-05 to BC-REP-01), and a table of values to an average rate with units (BC-REP-03 to BC-REP-04).

### Assessment behaviour

MCQ forms ask for an average rate over a named interval or for the difference quotient that expresses it. FRQ forms compute an average rate with supporting work and units, and the 2025 scoring guideline requires both a difference and a quotient using table values for the answer point, with a separate point for units (sg-25:11, sg-24:2). Calculator variants supply a formula; no-calculator variants supply a table. Conceptual variants separate the average rate from the instantaneous rate; computational variants ask for the quotient; interpretation variants ask for the meaning with units; justification variants ask why a limit is needed for the rate at an instant. Multi-concept variants place the average rate in the same question as an existence argument built on the same table (sg-25:11, sg-25:12).

### Archetypes

- BC-QA-02001 Derivative estimated from a table with units
- BC-QA-02003 Limit recognised as a derivative of a known function
- BC-QA-02012 Derivative notation read or converted

### Errors and misconceptions

- BC-ERR-02001 Difference reported without the quotient
- BC-ERR-02003 Units omitted or given as the units of the quantity
- BC-MIS-02001 A rate is a difference, severity high
- BC-MIS-02008 Units are decoration rather than part of the answer, severity medium

### Diagnostic signals

- No signal is scoped to this topic; the unit level signal list in data/staging/unit-02.signals.json applies.

### Adaptive metadata summary

Skills in this topic carry calculator relevance none, optional. Remediation targets named across the topic: BC-PRQ-02001, BC-SKL-01001, BC-SKL-01003. Every skill record carries the full seven key adaptive block in data/staging/unit-02.skills.json. [inferred]

## 2.2 Defining the Derivative of a Function and Using Derivative Notation

### Official mapping

Topic id BC-TOP-0202, CED code 2.2, name Defining the Derivative of a Function and Using Derivative Notation, scope shared, CED page 61. [verified] (ced:61)

- BC-LO-CHA-2B (CHA-2.B): Represent the derivative of a function as the limit of a difference quotient.
  - BC-EK-CHA-2B1 (CHA-2.B.1): "The instantaneous rate of change of a function at x = a can be expressed by lim as h approaches 0 of (f(a + h) - f(a))/h or lim as x approaches a of (f(x) - f(a))/(x - a), provided the limit exists. These are equivalent forms of the definition of the derivative and are denoted f'(a)."
  - BC-EK-CHA-2B2 (CHA-2.B.2): "The derivative of f is the function whose value at x is lim as h approaches 0 of (f(x + h) - f(x))/h, provided this limit exists."
  - BC-EK-CHA-2B3 (CHA-2.B.3): "For y = f(x), notations for the derivative include dy/dx, f'(x), and y'."
  - BC-EK-CHA-2B4 (CHA-2.B.4): "The derivative can be represented graphically, numerically, analytically, and verbally."
- BC-LO-CHA-2C (CHA-2.C): Determine the equation of a line tangent to a curve at a given point.
  - BC-EK-CHA-2C1 (CHA-2.C.1): "The derivative of a function at a point is the slope of the line tangent to a graph of the function at that point."

Suggested practice skills: BC-MPS-1D (Practice skill 1.D), BC-MPS-4C (Practice skill 4.C). Weighting pointer: [../exam/exam-blueprint.md](../exam/exam-blueprint.md).

### Concept breakdown

- BC-CON-02002 Instantaneous rate of change as the limit of a difference quotient: The rate at a point is what the average rates approach as the interval shrinks to nothing.
- BC-CON-02003 The derivative as a function defined by a limit: The derivative is itself a function, whose value at each input is a limit of a difference quotient there.
- BC-CON-02004 Derivative notation and its equivalent forms: The same derivative can be written in prime form, Leibniz form, or as y prime.
- BC-CON-02005 The derivative at a point as the slope of the tangent line: The derivative value at a point is the slope of the line touching the curve there.

- BC-SKL-02006 Write the derivative at a point using the increment form of the limit: Write the limit as the increment tends to zero of the difference quotient at the base point.
- BC-SKL-02007 Write the derivative at a point using the two point form of the limit: Write the limit as the second input tends to the base point.
- BC-SKL-02008 Write the derivative function using the limit definition: Write the derivative as a function of the input rather than at one point.
- BC-SKL-02009 Evaluate a derivative from the limit definition: Expand the difference quotient, cancel the increment, and take the limit.
- BC-SKL-02010 Convert among the notations for a derivative: Move between the prime form, the Leibniz form, and the y prime form.
- BC-SKL-02011 Represent a derivative graphically, numerically, and verbally: Show the same derivative information as a slope on a graph, as a value in a table, and as a sentence.
- BC-SKL-02012 Interpret the derivative at a point as the slope of the tangent line: Say that the derivative value is the steepness of the line touching the curve there.
- BC-SKL-02013 Write the equation of the line tangent to a curve at a given point: Use the derivative value as the slope and the point of tangency in the point slope form.

Granularity note: Topic 2.2 carries eight skills because BC-EK-CHA-2B1 names two equivalent limit forms at a point, BC-EK-CHA-2B2 adds the derivative as a function, BC-EK-CHA-2B3 names three notations, BC-EK-CHA-2B4 requires four representations, and BC-EK-CHA-2C1 adds the tangent line, and these are independently testable.

### Prerequisites

- BC-PRQ-02005 -> BC-SKL-02006, supporting, [inferred], Prerequisite for Write the derivative at a point using the increment form of the limit.
- BC-PRQ-02005 -> BC-SKL-02007, supporting, [inferred], Prerequisite for Write the derivative at a point using the two point form of the limit.
- BC-PRQ-02005 -> BC-SKL-02008, supporting, [inferred], Prerequisite for Write the derivative function using the limit definition.
- BC-PRQ-02001 -> BC-SKL-02009, supporting, [inferred], Prerequisite for Evaluate a derivative from the limit definition.
- BC-SKL-01024 -> BC-SKL-02009, supporting, [inferred], Prerequisite for Evaluate a derivative from the limit definition.
- BC-PRQ-02004 -> BC-SKL-02010, supporting, [inferred], Prerequisite for Convert among the notations for a derivative.
- BC-SKL-01036 -> BC-SKL-02011, supporting, [inferred], Prerequisite for Represent a derivative graphically, numerically, and verbally.
- BC-PRQ-02003 -> BC-SKL-02012, supporting, [inferred], Prerequisite for Interpret the derivative at a point as the slope of the tangent line.
- BC-PRQ-02003 -> BC-SKL-02013, supporting, [inferred], Prerequisite for Write the equation of the line tangent to a curve at a given point.
- BC-SKL-02001 -> BC-SKL-02006, hard_prerequisite, [inferred], The limit form of the derivative is built on the increment difference quotient.
- BC-SKL-02002 -> BC-SKL-02007, hard_prerequisite, [inferred], The two point limit form is built on the two point difference quotient.
- BC-SKL-02006 -> BC-SKL-02008, hard_prerequisite, [inferred], The derivative function generalises the derivative at a point.
- BC-SKL-02006 -> BC-SKL-02007, co_requisite, [inferred], The two forms of the definition are equivalent and are learned together.
- BC-SKL-02012 -> BC-SKL-02013, hard_prerequisite, [inferred], The tangent line uses the derivative read as a slope.
- BC-SKL-02009 -> BC-TOP-0301, hard_prerequisite, [inferred], The limit definition underlies the chain rule development at Unit 3 topic 3.1.
- BC-SKL-02013 -> BC-TOP-0406, hard_prerequisite, [inferred], Linear approximation at Unit 4 topic 4.6 is the tangent line used as an estimate.
- BC-SKL-02008 -> BC-TOP-0407, supporting, [inferred], L'Hospital's rule at Unit 4 topic 4.7 replaces the algebraic handling of indeterminate forms that Unit 1 and the derivative definition use.
- BC-SKL-02013 -> BC-TOP-0702, supporting, [inferred], Slope fields at Unit 7 topic 7.2 read a differential equation as a prescription of tangent slopes.
- BC-SKL-02008 -> BC-TOP-1011, supporting, [inferred], Taylor polynomials at Unit 10 are built from derivative values at a base point.

### Required mathematical knowledge

**Derivative at a point.** The instantaneous rate of change at an input can be written as the limit of either difference quotient, provided the limit exists, and both forms denote the same number (BC-EK-CHA-2B1).

**Derivative function.** The derivative of f is the function whose value at x is the limit as h tends to zero of the quotient of f(x plus h) minus f(x) by h, provided this limit exists (BC-EK-CHA-2B2).

**Notation.** For y equal to f(x), notations for the derivative include dy by dx, f prime of x, and y prime (BC-EK-CHA-2B3). The derivative can be represented graphically, numerically, analytically, and verbally (BC-EK-CHA-2B4).

**Tangent line.** The derivative of a function at a point is the slope of the line tangent to the graph at that point (BC-EK-CHA-2C1), and with the point of tangency it determines the line.

**Method.** The difference quotient is indeterminate at zero increment, so the increment is divided out of the numerator before the limit is taken.

### Representations

Representations in play: BC-REP-01 Symbolic (analytical) expression, BC-REP-02 Graphical, BC-REP-03 Numerical table, BC-REP-04 Verbal description.

Conversions tested: limit definition to a derivative value (BC-REP-01 to BC-REP-01), derivative value to a tangent slope on a graph (BC-REP-01 to BC-REP-02), and one notation to another (BC-REP-01 to BC-REP-01).

### Assessment behaviour

MCQ forms ask for a derivative computed from the definition, for the notation that denotes a stated quantity, or for a tangent line. FRQ forms use derivative notation throughout and require tangent lines inside application parts; no 2023 to 2025 free response part asks for a derivative from the definition, so BC-QA-02002 is inferred. Calculator variants are uncommon for the definition itself; no-calculator variants dominate. Conceptual variants ask what the notation denotes; computational variants evaluate the limit; interpretation variants read the derivative as a slope or a rate; justification variants ask why the increment may be divided out. Multi-concept variants combine the tangent line with an approximation in a later unit.

### Archetypes

- BC-QA-02002 Derivative computed from the limit definition
- BC-QA-02011 Tangent line written at a point on a curve
- BC-QA-02012 Derivative notation read or converted

### Errors and misconceptions

- BC-ERR-02005 Increment set to zero before the common factor is divided out
- BC-ERR-02006 Limit symbol dropped during the computation
- BC-ERR-02007 Shifted term expanded incorrectly
- BC-ERR-02008 Derivative produced by rule where the definition was demanded
- BC-ERR-02027 Function value used as the slope of the tangent line
- BC-ERR-02028 Derivative evaluated at the wrong input for a tangent line
- BC-ERR-02029 Leibniz notation read as a quotient of two separate quantities
- BC-ERR-02030 Derivative function confused with its value at a point
- BC-MIS-02002 The definition of the derivative is a formality to be written and then abandoned, severity high
- BC-MIS-02003 The limit symbol is decoration on the final line, severity medium
- BC-MIS-02014 The derivative and the function value are interchangeable at a point, severity high
- BC-MIS-02015 Derivative notation is a set of interchangeable labels, severity medium

### Diagnostic signals

- BC-SIG-02004 Difference quotient set up correctly then collapsed, mastery state partially_mastered
- BC-SIG-02005 Correct derivative with the limit symbol absent from the work, mastery state partially_mastered
- BC-SIG-02016 Tangent line correct in slope but through the wrong point, mastery state partially_mastered

### Adaptive metadata summary

Skills in this topic carry calculator relevance none. Remediation targets named across the topic: BC-PRQ-02001, BC-PRQ-02003, BC-PRQ-02004, BC-PRQ-02005, BC-SKL-01036. Every skill record carries the full seven key adaptive block in data/staging/unit-02.skills.json. [inferred]

## 2.3 Estimating Derivatives of a Function at a Point

### Official mapping

Topic id BC-TOP-0203, CED code 2.3, name Estimating Derivatives of a Function at a Point, scope shared, CED page 62. [verified] (ced:62)

- BC-LO-CHA-2D (CHA-2.D): Estimate derivatives.
  - BC-EK-CHA-2D1 (CHA-2.D.1): "The derivative at a point can be estimated from information given in tables or graphs."
  - BC-EK-CHA-2D2 (CHA-2.D.2): "Technology can be used to calculate or estimate the value of a derivative of a function at a point."

Suggested practice skills: BC-MPS-1E (Practice skill 1.E). Weighting pointer: [../exam/exam-blueprint.md](../exam/exam-blueprint.md).

### Concept breakdown

- BC-CON-02007 Estimation of a derivative from tabular or graphical information: A derivative at a point can be estimated from nearby values or from the steepness of the graph.

- BC-SKL-02014 Estimate a derivative at a point from a table using a difference quotient: Use the two tabulated inputs on either side of the point and divide the change in the values by the change in the inputs.
- BC-SKL-02015 State the units of an estimated derivative in context: Give the units as the units of the quantity per unit of the independent variable.
- BC-SKL-02016 Select the interval of a table that supports the requested estimate: Choose the tabulated inputs the question names, or the pair that brackets the point.
- BC-SKL-02017 Estimate a derivative at a point from a graph: Read the steepness of the curve at the point from the graph.
- BC-SKL-02018 Estimate a derivative at a point using technology: Use the numerical derivative capability of the calculator at the named input.

### Prerequisites

- BC-SKL-01001 -> BC-SKL-02014, supporting, [inferred], Prerequisite for Estimate a derivative at a point from a table using a difference quotient.
- BC-SKL-01001 -> BC-SKL-02015, supporting, [inferred], Prerequisite for State the units of an estimated derivative in context.
- BC-SKL-01016 -> BC-SKL-02016, supporting, [inferred], Prerequisite for Select the interval of a table that supports the requested estimate.
- BC-SKL-01009 -> BC-SKL-02017, supporting, [inferred], Prerequisite for Estimate a derivative at a point from a graph.
- BC-PRQ-02004 -> BC-SKL-02018, supporting, [inferred], Prerequisite for Estimate a derivative at a point using technology.
- BC-SKL-02016 -> BC-SKL-02014, hard_prerequisite, [inferred], The interval must be chosen before the estimate is computed.
- BC-SKL-02014 -> BC-SKL-02015, co_requisite, [inferred], The units are demanded with the estimate in the same part.
- BC-SKL-02014 -> BC-TOP-0402, supporting, [inferred], Estimating a derivative from a table supports the motion analysis of Unit 4 topic 4.2.

### Required mathematical knowledge

**Estimation.** The derivative at a point can be estimated from information given in tables or graphs (BC-EK-CHA-2D1), and technology can calculate or estimate the value of a derivative at a point (BC-EK-CHA-2D2).

**Method from a table.** Use the average rate of change over an interval from the table that contains or abuts the point, and present both the difference and the quotient.

**Units.** The units of the estimate are the units of the modelled quantity divided by the units of the independent variable, and a scoring guideline awards them their own point whether or not they are attached to a numerical value (sg-25:11).

**Notation.** approximately equal to; the compound unit written as a quotient or as a squared denominator where the two units agree.

### Representations

Representations in play: BC-REP-03 Numerical table, BC-REP-02 Graphical, BC-REP-05 Contextual model, BC-REP-09 Calculator-generated numerical result.

Conversions tested: table to an estimated derivative with units (BC-REP-03 to BC-REP-04), and graph to an estimated slope (BC-REP-02 to BC-REP-01).

### Assessment behaviour

MCQ forms ask for the best estimate of a derivative from a short table or a graph. FRQ forms open with this task: a 2025 part requires the answer with the supporting work of a difference and a quotient using table values and awards units separately, and a 2024 part does the same over an interval bracketing the point (sg-25:11, sg-24:2). Calculator variants use the numerical derivative capability on a supplied model; no-calculator variants use the table. Conceptual variants ask which interval supports the estimate; computational variants produce the value; interpretation variants explain the value in context; justification variants ask why the estimate is only an approximation. Multi-concept variants continue from the estimate to an existence argument or an accumulation in the same question (sg-25:11).

### Archetypes

- BC-QA-02001 Derivative estimated from a table with units
- BC-QA-02009 Derivative of a product or quotient evaluated from supplied values
- BC-QA-02013 Derivative at a point produced with technology

### Errors and misconceptions

- BC-ERR-02001 Difference reported without the quotient
- BC-ERR-02002 Quotient expression presented with no evaluated value
- BC-ERR-02003 Units omitted or given as the units of the quantity
- BC-ERR-02004 Rows used that do not match the requested interval
- BC-ERR-02031 Calculator derivative reported without a setup
- BC-ERR-02032 Calculator value rounded to too few places
- BC-MIS-02001 A rate is a difference, severity high
- BC-MIS-02008 Units are decoration rather than part of the answer, severity medium
- BC-MIS-02015 Derivative notation is a set of interchangeable labels, severity medium

### Diagnostic signals

- BC-SIG-02001 Correct difference with the division omitted, mastery state partially_mastered
- BC-SIG-02002 Correct quotient with no value reported, mastery state partially_mastered
- BC-SIG-02003 Correct estimate with the units of the quantity attached, mastery state partially_mastered
- BC-SIG-02017 Calculator value correct with no setup shown, mastery state partially_mastered

### Adaptive metadata summary

Skills in this topic carry calculator relevance none, typically_required. Remediation targets named across the topic: BC-PRQ-02004, BC-SKL-01001, BC-SKL-01009, BC-SKL-01016. Every skill record carries the full seven key adaptive block in data/staging/unit-02.skills.json. [inferred]

## 2.4 Connecting Differentiability and Continuity: Determining When Derivatives Do and Do Not Exist

### Official mapping

Topic id BC-TOP-0204, CED code 2.4, name Connecting Differentiability and Continuity: Determining When Derivatives Do and Do Not Exist, scope shared, CED page 63. [verified] (ced:63)

- BC-LO-FUN-2A (FUN-2.A): Explain the relationship between differentiability and continuity.
  - BC-EK-FUN-2A1 (FUN-2.A.1): "If a function is differentiable at a point, then it is continuous at that point. In particular, if a point is not in the domain of f, then it is not in the domain of f '."
  - BC-EK-FUN-2A2 (FUN-2.A.2): "A continuous function may fail to be differentiable at a point in its domain."

Suggested practice skills: BC-MPS-3E (Practice skill 3.E). Weighting pointer: [../exam/exam-blueprint.md](../exam/exam-blueprint.md).

### Concept breakdown

- BC-CON-02008 Differentiability implies continuity: A function that has a derivative at a point must be continuous there.
- BC-CON-02009 Ways a derivative fails to exist at a point of continuity: A continuous function can still have no derivative, at a corner, a cusp, or a vertical tangent.

- BC-SKL-02019 State that differentiability at a point implies continuity at that point: Say that having a derivative at a point forces continuity there.
- BC-SKL-02020 Use differentiability to justify continuity in a written argument: Write that the function is continuous because it is differentiable, as the reason inside a larger argument.
- BC-SKL-02021 Give a continuous function that fails to be differentiable at a point: Produce an example showing that the converse of the implication fails.
- BC-SKL-02022 Identify a corner from unequal one sided limits of the difference quotient: Show that the slope approached from the left differs from the slope approached from the right.
- BC-SKL-02023 Identify a vertical tangent as a failure of differentiability: Say that a tangent line with no slope means no derivative.
- BC-SKL-02024 Conclude non-differentiability from a discontinuity: Read the implication backwards to rule out a derivative where the function breaks.

### Prerequisites

- BC-SKL-01043 -> BC-SKL-02019, supporting, [inferred], Prerequisite for State that differentiability at a point implies continuity at that point.
- BC-SKL-01065 -> BC-SKL-02020, supporting, [inferred], Prerequisite for Use differentiability to justify continuity in a written argument.
- BC-SKL-01040 -> BC-SKL-02021, supporting, [inferred], Prerequisite for Give a continuous function that fails to be differentiable at a point.
- BC-SKL-01010 -> BC-SKL-02022, supporting, [inferred], Prerequisite for Identify a corner from unequal one sided limits of the difference quotient.
- BC-PRQ-02001 -> BC-SKL-02022, supporting, [inferred], Prerequisite for Identify a corner from unequal one sided limits of the difference quotient.
- BC-SKL-01012 -> BC-SKL-02023, supporting, [inferred], Prerequisite for Identify a vertical tangent as a failure of differentiability.
- BC-SKL-01044 -> BC-SKL-02024, supporting, [inferred], Prerequisite for Conclude non-differentiability from a discontinuity.
- BC-SKL-02019 -> BC-SKL-02020, hard_prerequisite, [inferred], Using the implication in an argument rests on stating it.
- BC-SKL-02019 -> BC-SKL-02024, hard_prerequisite, [inferred], The contrapositive rests on the implication.
- BC-SKL-02021 -> BC-SKL-02022, supporting, [inferred], Examples of non-differentiability are analysed through the one sided difference quotients.
- BC-SKL-02019 -> BC-TOP-0116, supporting, [inferred], Differentiability supplies the continuity hypothesis of the Intermediate Value Theorem at Unit 1 topic 1.16.
- BC-SKL-02019 -> BC-TOP-0501, hard_prerequisite, [inferred], The Mean Value Theorem at Unit 5 topic 5.1 carries both a continuity and a differentiability hypothesis.

### Required mathematical knowledge

**Implication.** If a function is differentiable at a point then it is continuous at that point; in particular, if a point is not in the domain of f then it is not in the domain of f prime (BC-EK-FUN-2A1).

**Converse fails.** A continuous function may fail to be differentiable at a point in its domain (BC-EK-FUN-2A2). The CED names two routes: unequal one sided limits of the difference quotient, as at the corner of an absolute value, and a vertical tangent with no slope, as at the origin of a cube root (ced:63).

**Contrapositive.** A function discontinuous at a point has no derivative there.

**Justification standard.** A scoring guideline awards a point for stating that a function is continuous because it is differentiable and refuses it for a bare claim of continuity (sg-25:12); a 2023 part runs the same implication at a single point before evaluating a limit (sg-23:14).

**Notation.** differentiable implies continuous; corner; vertical tangent.

### Representations

Representations in play: BC-REP-01 Symbolic (analytical) expression, BC-REP-02 Graphical, BC-REP-04 Verbal description, BC-REP-03 Numerical table.

Conversions tested: a differentiability statement to a continuity conclusion (BC-REP-04 to BC-REP-04), and a graph to a verdict on differentiability (BC-REP-02 to BC-REP-04).

### Assessment behaviour

MCQ forms ask whether a function is differentiable at a named point and why. FRQ forms use the implication as a step: the 2025 question derives continuity from differentiability to reach an Intermediate Value Theorem conclusion, and the 2023 question uses it to replace a limit by a function value before applying L'Hospital's rule (sg-25:12, sg-23:14). Calculator variants are uncommon; no-calculator variants dominate. Conceptual variants ask which direction of the implication holds; computational variants evaluate one sided difference quotients; interpretation variants read the failure off a graph; justification variants demand the reason, which carries its own point. Multi-concept variants pair the continuity conclusion with an existence theorem in the same part (sg-25:12).

### Archetypes

- BC-QA-02004 Continuity deduced from differentiability inside a larger argument
- BC-QA-02005 Point of non-differentiability identified on a continuous function

### Errors and misconceptions

- BC-ERR-02011 Continuity asserted with no basis in an argument about a differentiable function
- BC-ERR-02012 Implication run backwards from continuity to differentiability
- BC-ERR-02013 Non-differentiability claimed from the appearance of the graph alone
- BC-ERR-02014 Vertical tangent treated as a horizontal one
- BC-MIS-02005 A hypothesis holds because the setting supplies it, severity high
- BC-MIS-02006 Differentiability and continuity are the same property, severity high
- BC-MIS-02007 Differentiability is a visual property of the graph, severity medium

### Diagnostic signals

- BC-SIG-02007 Continuity used correctly but stated without its reason, mastery state partially_mastered
- BC-SIG-02008 Implication stated in the wrong direction, mastery state not_mastered
- BC-SIG-02009 Correct verdict on differentiability with a visual reason, mastery state partially_mastered

### Adaptive metadata summary

Skills in this topic carry calculator relevance none. Remediation targets named across the topic: BC-SKL-01010, BC-SKL-01012, BC-SKL-01040, BC-SKL-01043, BC-SKL-01044, BC-SKL-01065. Every skill record carries the full seven key adaptive block in data/staging/unit-02.skills.json. [inferred]

## 2.5 Applying the Power Rule

### Official mapping

Topic id BC-TOP-0205, CED code 2.5, name Applying the Power Rule, scope shared, CED page 64. [verified] (ced:64)

- BC-LO-FUN-3A (FUN-3.A): Calculate derivatives of familiar functions.
  - BC-EK-FUN-3A1 (FUN-3.A.1): "Direct application of the definition of the derivative and specific rules can be used to calculate the derivative for functions of the form f(x) = x^r."
  - BC-EK-FUN-3A2 (FUN-3.A.2): "Sums, differences, and constant multiples of functions can be differentiated using derivative rules."
  - BC-EK-FUN-3A3 (FUN-3.A.3): "The power rule combined with sum, difference, and constant multiple properties can be used to find the derivatives for polynomial functions."
  - BC-EK-FUN-3A4 (FUN-3.A.4): "Specific rules can be used to find the derivatives for sine, cosine, exponential, and logarithmic functions."

Suggested practice skills: BC-MPS-1E (Practice skill 1.E). Weighting pointer: [../exam/exam-blueprint.md](../exam/exam-blueprint.md).

### Concept breakdown

- BC-CON-02010 The power rule: The derivative of a power drops the exponent by one and multiplies by the old exponent.

- BC-SKL-02025 Differentiate a power function with an integer exponent: Multiply by the exponent and reduce the exponent by one.
- BC-SKL-02026 Differentiate a power function after rewriting a radical or a reciprocal as a power: Turn the root or the fraction into an exponent first, then apply the rule.
- BC-SKL-02027 Derive a power rule case from the limit definition: Get the rule for a particular power out of the difference quotient.

### Prerequisites

- BC-PRQ-06002 -> BC-SKL-02025, supporting, [inferred], Prerequisite for Differentiate a power function with an integer exponent.
- BC-PRQ-06002 -> BC-SKL-02026, supporting, [inferred], Prerequisite for Differentiate a power function after rewriting a radical or a reciprocal as a power.
- BC-SKL-02009 -> BC-SKL-02027, hard_prerequisite, [inferred], Prerequisite for Derive a power rule case from the limit definition.
- BC-SKL-02025 -> BC-SKL-02026, hard_prerequisite, [inferred], The rewriting case extends the integer exponent case.
- BC-SKL-02025 -> BC-TOP-0607, hard_prerequisite, [inferred], Antiderivative recognition at Unit 6 reverses the power rule.

### Required mathematical knowledge

**Power rule.** Direct application of the definition of the derivative and specific rules can be used to calculate the derivative for functions of the form f(x) equal to x to the power r (BC-EK-FUN-3A1). The derivative is r times x to the power r minus one.

**Scope of the exponent.** The rule is stated for a general real exponent, so radicals and reciprocals are differentiated by first rewriting them as powers.

**Relation to the definition.** The rule can be obtained for a specific exponent by expanding the difference quotient and dividing out the increment, which links this topic back to topic 2.2.

**Notation.** power rule; the exponent written as a fraction or a negative number.

### Representations

Representations in play: BC-REP-01 Symbolic (analytical) expression.

Conversions tested: a radical or reciprocal expression to a power (BC-REP-01 to BC-REP-01).

### Assessment behaviour

MCQ forms ask for the derivative of a power or of an expression that becomes one after rewriting. FRQ forms use the rule inside larger computations rather than as a task of its own. Calculator variants are uncommon; no-calculator variants dominate. Conceptual variants ask why a radical must be rewritten; computational variants produce the derivative; interpretation variants are rare; justification variants derive a case from the definition. Multi-concept variants combine the rule with the sum and constant multiple properties in the following topic.

### Archetypes

- BC-QA-02002 Derivative computed from the limit definition
- BC-QA-02006 Derivative of a polynomial or power expression by rule

### Errors and misconceptions

- BC-ERR-02005 Increment set to zero before the common factor is divided out
- BC-ERR-02008 Derivative produced by rule where the definition was demanded
- BC-ERR-02015 Exponent reduced without multiplying by it
- BC-ERR-02017 Radical or reciprocal left undifferentiated
- BC-MIS-02002 The definition of the derivative is a formality to be written and then abandoned, severity high
- BC-MIS-02009 The power rule is a move on the exponent alone, severity high

### Diagnostic signals

- BC-SIG-02010 Exponents reduced correctly with the coefficients dropped, mastery state not_mastered
- BC-SIG-02011 Polynomial terms differentiated with a radical term copied, mastery state partially_mastered

### Adaptive metadata summary

Skills in this topic carry calculator relevance none. Remediation targets named across the topic: BC-PRQ-06002, BC-SKL-02009. Every skill record carries the full seven key adaptive block in data/staging/unit-02.skills.json. [inferred]

## 2.6 Derivative Rules: Constant, Sum, Difference, and Constant Multiple

### Official mapping

Topic id BC-TOP-0206, CED code 2.6, name Derivative Rules: Constant, Sum, Difference, and Constant Multiple, scope shared, CED page 65. [verified] (ced:65)

- BC-LO-FUN-3A (FUN-3.A): Calculate derivatives of familiar functions.
  - BC-EK-FUN-3A1 (FUN-3.A.1): "Direct application of the definition of the derivative and specific rules can be used to calculate the derivative for functions of the form f(x) = x^r."
  - BC-EK-FUN-3A2 (FUN-3.A.2): "Sums, differences, and constant multiples of functions can be differentiated using derivative rules."
  - BC-EK-FUN-3A3 (FUN-3.A.3): "The power rule combined with sum, difference, and constant multiple properties can be used to find the derivatives for polynomial functions."
  - BC-EK-FUN-3A4 (FUN-3.A.4): "Specific rules can be used to find the derivatives for sine, cosine, exponential, and logarithmic functions."

Suggested practice skills: BC-MPS-1E (Practice skill 1.E). Weighting pointer: [../exam/exam-blueprint.md](../exam/exam-blueprint.md).

### Concept breakdown

- BC-CON-02011 Linearity of differentiation: Constants come out, constants differentiate to zero, and sums differentiate term by term.

- BC-SKL-02028 Differentiate a constant function: Give zero as the derivative of a constant.
- BC-SKL-02029 Apply the constant multiple rule: Pull the constant out and differentiate what remains.
- BC-SKL-02030 Apply the sum and difference rules: Differentiate term by term.
- BC-SKL-02031 Differentiate a polynomial function: Combine the power rule with the term by term and constant multiple rules.

### Prerequisites

- BC-PRQ-02004 -> BC-SKL-02028, supporting, [inferred], Prerequisite for Differentiate a constant function.
- BC-PRQ-02004 -> BC-SKL-02029, supporting, [inferred], Prerequisite for Apply the constant multiple rule.
- BC-SKL-01018 -> BC-SKL-02030, supporting, [inferred], Prerequisite for Apply the sum and difference rules.
- BC-SKL-02025 -> BC-SKL-02031, hard_prerequisite, [inferred], Prerequisite for Differentiate a polynomial function.
- BC-SKL-02029 -> BC-SKL-02031, hard_prerequisite, [inferred], Polynomial differentiation combines the power rule with the constant multiple rule.
- BC-SKL-02030 -> BC-SKL-02031, hard_prerequisite, [inferred], Polynomial differentiation combines the power rule with the sum rule.
- BC-SKL-02031 -> BC-TOP-0502, hard_prerequisite, [inferred], The first derivative test at Unit 5 topic 5.2 needs the derivative of the given rule.

### Required mathematical knowledge

**Linearity.** Sums, differences, and constant multiples of functions can be differentiated using derivative rules (BC-EK-FUN-3A2), and the power rule combined with these properties differentiates any polynomial (BC-EK-FUN-3A3).

**Constants.** The derivative of a constant function is zero, which is the constant multiple rule applied to the zeroth power.

**Notation.** constant multiple rule; sum rule; difference rule.

### Representations

Representations in play: BC-REP-01 Symbolic (analytical) expression.

Conversions tested: a polynomial expression to its derivative term by term (BC-REP-01 to BC-REP-01).

### Assessment behaviour

MCQ forms ask for the derivative of a polynomial or of a linear combination. FRQ forms differentiate supplied models inside application parts. Calculator variants are uncommon; no-calculator variants dominate. Conceptual variants ask why a constant differentiates to zero; computational variants produce the derivative; interpretation variants read a derivative in context; justification variants name the rules used. Multi-concept variants continue to a second derivative or to a tangent line.

### Archetypes

- BC-QA-02006 Derivative of a polynomial or power expression by rule

### Errors and misconceptions

- BC-ERR-02015 Exponent reduced without multiplying by it
- BC-ERR-02016 Constant term differentiated to itself
- BC-MIS-02009 The power rule is a move on the exponent alone, severity high

### Diagnostic signals

- No signal is scoped to this topic; the unit level signal list in data/staging/unit-02.signals.json applies.

### Adaptive metadata summary

Skills in this topic carry calculator relevance none. Remediation targets named across the topic: BC-PRQ-02004, BC-SKL-01018, BC-SKL-02025. Every skill record carries the full seven key adaptive block in data/staging/unit-02.skills.json. [inferred]

## 2.7 Derivatives of cos x, sin x, e^x, and ln x

### Official mapping

Topic id BC-TOP-0207, CED code 2.7, name Derivatives of cos x, sin x, e^x, and ln x, scope shared, CED page 66. [verified] (ced:66)

- BC-LO-FUN-3A (FUN-3.A): Calculate derivatives of familiar functions.
  - BC-EK-FUN-3A1 (FUN-3.A.1): "Direct application of the definition of the derivative and specific rules can be used to calculate the derivative for functions of the form f(x) = x^r."
  - BC-EK-FUN-3A2 (FUN-3.A.2): "Sums, differences, and constant multiples of functions can be differentiated using derivative rules."
  - BC-EK-FUN-3A3 (FUN-3.A.3): "The power rule combined with sum, difference, and constant multiple properties can be used to find the derivatives for polynomial functions."
  - BC-EK-FUN-3A4 (FUN-3.A.4): "Specific rules can be used to find the derivatives for sine, cosine, exponential, and logarithmic functions."
- BC-LO-LIM-3A (LIM-3.A): Interpret a limit as a definition of a derivative.
  - BC-EK-LIM-3A1 (LIM-3.A.1): "In some cases, recognizing an expression for the definition of the derivative of a function whose derivative is known offers a strategy for determining a limit."

Suggested practice skills: BC-MPS-1E (Practice skill 1.E). Weighting pointer: [../exam/exam-blueprint.md](../exam/exam-blueprint.md).

### Concept breakdown

- BC-CON-02006 Recognising a limit as a derivative of a known function: A limit that has the shape of a difference quotient can be read as a derivative already known.
- BC-CON-02012 Derivatives of the basic transcendental functions: Sine, cosine, the natural exponential, and the natural logarithm each have a rule of their own.

- BC-SKL-02032 Differentiate sine and cosine: Recall that sine gives cosine and cosine gives negative sine.
- BC-SKL-02033 Differentiate the natural exponential function: Recall that the natural exponential is its own derivative.
- BC-SKL-02034 Differentiate the natural logarithm: Recall that the natural logarithm gives one over the input.
- BC-SKL-02035 Evaluate a limit by recognising it as the derivative of a known function: Match the limit to a difference quotient and read off the derivative value.

### Prerequisites

- BC-PRQ-01005 -> BC-SKL-02032, supporting, [inferred], Prerequisite for Differentiate sine and cosine.
- BC-PRQ-06002 -> BC-SKL-02033, supporting, [inferred], Prerequisite for Differentiate the natural exponential function.
- BC-PRQ-06003 -> BC-SKL-02034, supporting, [inferred], Prerequisite for Differentiate the natural logarithm.
- BC-SKL-02006 -> BC-SKL-02035, hard_prerequisite, [inferred], Prerequisite for Evaluate a limit by recognising it as the derivative of a known function.
- BC-PRQ-02005 -> BC-SKL-02035, supporting, [inferred], Prerequisite for Evaluate a limit by recognising it as the derivative of a known function.
- BC-SKL-02008 -> BC-SKL-02035, supporting, [inferred], Recognising a limit as a derivative rests on the definition being fluent in both directions.
- BC-SKL-02032 -> BC-TOP-0607, hard_prerequisite, [inferred], Antiderivative recognition at Unit 6 reverses the basic transcendental derivatives.

### Required mathematical knowledge

**Specific rules.** Specific rules can be used to find the derivatives for sine, cosine, exponential, and logarithmic functions (BC-EK-FUN-3A4). The derivative of sine is cosine, the derivative of cosine is the negative of sine, the natural exponential is its own derivative, and the derivative of the natural logarithm is the reciprocal of the input.

**Limit read as a derivative.** In some cases, recognising an expression for the definition of the derivative of a function whose derivative is known offers a strategy for determining a limit (BC-EK-LIM-3A1). The CED attaches this learning objective to the same topic as the transcendental rules (ced:66).

**Notation.** The logarithm derivative stated on the domain where the logarithm is defined.

### Representations

Representations in play: BC-REP-01 Symbolic (analytical) expression.

Conversions tested: a limit in difference quotient form to a derivative value (BC-REP-01 to BC-REP-01).

### Assessment behaviour

MCQ forms ask for the derivative of a transcendental expression or for the value of a limit that is a difference quotient of a known function. FRQ forms differentiate supplied transcendental models inside application parts. Calculator variants are uncommon; no-calculator variants dominate. Conceptual variants ask which rule applies; computational variants produce the derivative or the limit value; interpretation variants are rare; justification variants identify the underlying function and base point of a recognised limit. Multi-concept variants combine a transcendental factor with the product or quotient rule.

### Archetypes

- BC-QA-02003 Limit recognised as a derivative of a known function
- BC-QA-02007 Derivative of an expression built from the basic transcendental functions

### Errors and misconceptions

- BC-ERR-02009 Limit in derivative form reported as nonexistent
- BC-ERR-02010 Wrong base point identified in a limit read as a derivative
- BC-ERR-02018 Sign dropped from the derivative of cosine
- BC-ERR-02019 Exponential differentiated by the power rule
- BC-MIS-02004 A limit is resolved only by algebra, severity medium
- BC-MIS-02010 Every function is differentiated by the power rule, severity high

### Diagnostic signals

- BC-SIG-02006 Limit identified as a derivative with the wrong base point, mastery state partially_mastered
- BC-SIG-02012 Trigonometric derivative correct except for the sign, mastery state partially_mastered

### Adaptive metadata summary

Skills in this topic carry calculator relevance none. Remediation targets named across the topic: BC-PRQ-01005, BC-PRQ-06002, BC-PRQ-06003, BC-SKL-02006. Every skill record carries the full seven key adaptive block in data/staging/unit-02.skills.json. [inferred]

## 2.8 The Product Rule

### Official mapping

Topic id BC-TOP-0208, CED code 2.8, name The Product Rule, scope shared, CED page 67. [verified] (ced:67)

- BC-LO-FUN-3B (FUN-3.B): Calculate derivatives of products and quotients of differentiable functions.
  - BC-EK-FUN-3B1 (FUN-3.B.1): "Derivatives of products of differentiable functions can be found using the product rule."
  - BC-EK-FUN-3B2 (FUN-3.B.2): "Derivatives of quotients of differentiable functions can be found using the quotient rule."
  - BC-EK-FUN-3B3 (FUN-3.B.3): "Rearranging tangent, cotangent, secant, and cosecant functions using identities allows differentiation using derivative rules."

Suggested practice skills: BC-MPS-1E (Practice skill 1.E). Weighting pointer: [../exam/exam-blueprint.md](../exam/exam-blueprint.md).

### Concept breakdown

- BC-CON-02013 The product rule: The derivative of a product is the first times the derivative of the second plus the second times the derivative of the first.

- BC-SKL-02036 Apply the product rule to a product of two differentiable functions: Differentiate one factor at a time and add the two results.
- BC-SKL-02037 Apply the product rule with values supplied by a table or a graph: Substitute the four supplied values into the rule at the named input.
- BC-SKL-02038 Decide whether to expand a product or to apply the product rule: Choose the cheaper route when the product can be multiplied out.

### Prerequisites

- BC-SKL-02031 -> BC-SKL-02036, hard_prerequisite, [inferred], Prerequisite for Apply the product rule to a product of two differentiable functions.
- BC-SKL-02036 -> BC-SKL-02037, hard_prerequisite, [inferred], Prerequisite for Apply the product rule with values supplied by a table or a graph.
- BC-SKL-02031 -> BC-SKL-02038, hard_prerequisite, [inferred], Prerequisite for Decide whether to expand a product or to apply the product rule.
- BC-SKL-02036 -> BC-SKL-02037, hard_prerequisite, [inferred], Evaluating from supplied values applies the rule.
- BC-SKL-02036 -> BC-TOP-0302, hard_prerequisite, [inferred], Implicit differentiation at Unit 3 topic 3.2 applies the product rule to mixed terms.
- BC-SKL-02036 -> BC-TOP-0611, hard_prerequisite, [inferred], Integration by parts at Unit 6 topic 6.11 is the product rule read as an antidifferentiation technique.

### Required mathematical knowledge

**Product rule.** Derivatives of products of differentiable functions can be found using the product rule (BC-EK-FUN-3B1): the derivative of a product is the first factor times the derivative of the second plus the second factor times the derivative of the first.

**Not a product of derivatives.** The derivative of a product is not the product of the derivatives, which is checked at once by expanding a simple product and differentiating term by term.

**When expansion is available.** A product of polynomials can be expanded and differentiated term by term instead, which is sometimes the shorter route.

**Notation.** product rule.

### Representations

Representations in play: BC-REP-01 Symbolic (analytical) expression, BC-REP-03 Numerical table, BC-REP-02 Graphical.

Conversions tested: supplied values of two functions and their derivatives to a derivative of their product (BC-REP-03 to BC-REP-01).

### Assessment behaviour

MCQ forms ask for the derivative of a product, either symbolically or from supplied values at a point. FRQ forms use the rule inside larger computations. Calculator variants are uncommon; no-calculator variants dominate. Conceptual variants test the structure of the rule; computational variants produce the derivative; interpretation variants read the result in context; justification variants ask which rule applies and why. Multi-concept variants supply the values from a table shared with other parts of the same question.

### Archetypes

- BC-QA-02008 Derivative of a product or a quotient by rule
- BC-QA-02009 Derivative of a product or quotient evaluated from supplied values

### Errors and misconceptions

- BC-ERR-02020 Product differentiated as a product of derivatives
- BC-ERR-02023 Quotient rule applied where the denominator is constant
- BC-ERR-02024 Function value used where a derivative value was required
- BC-MIS-02011 Differentiation distributes across a product, severity high

### Diagnostic signals

- BC-SIG-02013 Product rule written correctly with one derivative value misread, mastery state partially_mastered

### Adaptive metadata summary

Skills in this topic carry calculator relevance none. Remediation targets named across the topic: BC-SKL-02031, BC-SKL-02036. Every skill record carries the full seven key adaptive block in data/staging/unit-02.skills.json. [inferred]

## 2.9 The Quotient Rule

### Official mapping

Topic id BC-TOP-0209, CED code 2.9, name The Quotient Rule, scope shared, CED page 68. [verified] (ced:68)

- BC-LO-FUN-3B (FUN-3.B): Calculate derivatives of products and quotients of differentiable functions.
  - BC-EK-FUN-3B1 (FUN-3.B.1): "Derivatives of products of differentiable functions can be found using the product rule."
  - BC-EK-FUN-3B2 (FUN-3.B.2): "Derivatives of quotients of differentiable functions can be found using the quotient rule."
  - BC-EK-FUN-3B3 (FUN-3.B.3): "Rearranging tangent, cotangent, secant, and cosecant functions using identities allows differentiation using derivative rules."

Suggested practice skills: BC-MPS-1E (Practice skill 1.E). Weighting pointer: [../exam/exam-blueprint.md](../exam/exam-blueprint.md).

### Concept breakdown

- BC-CON-02014 The quotient rule: The derivative of a quotient has a subtraction in the numerator whose order matters and the denominator squared below.

- BC-SKL-02039 Apply the quotient rule to a quotient of two differentiable functions: Use the denominator times the derivative of the numerator minus the numerator times the derivative of the denominator, all over the denominator squared.
- BC-SKL-02040 Keep the order of the terms in the quotient rule numerator: Put the subtraction the right way round.
- BC-SKL-02041 Apply the quotient rule with values supplied by a table or a graph: Substitute the four supplied values into the rule at the named input.
- BC-SKL-02042 Rewrite a quotient with a constant denominator instead of using the quotient rule: Pull out the constant when the bottom carries no variable.

### Prerequisites

- BC-SKL-02036 -> BC-SKL-02039, hard_prerequisite, [inferred], Prerequisite for Apply the quotient rule to a quotient of two differentiable functions.
- BC-SKL-02039 -> BC-SKL-02040, hard_prerequisite, [inferred], Prerequisite for Keep the order of the terms in the quotient rule numerator.
- BC-SKL-02039 -> BC-SKL-02041, hard_prerequisite, [inferred], Prerequisite for Apply the quotient rule with values supplied by a table or a graph.
- BC-SKL-02029 -> BC-SKL-02042, hard_prerequisite, [inferred], Prerequisite for Rewrite a quotient with a constant denominator instead of using the quotient rule.
- BC-SKL-02039 -> BC-SKL-02041, hard_prerequisite, [inferred], Evaluating from supplied values applies the rule.
- BC-SKL-02039 -> BC-TOP-0303, hard_prerequisite, [inferred], Derivatives of inverse functions at Unit 3 topic 3.3 rest on the quotient and chain rules.

### Required mathematical knowledge

**Quotient rule.** Derivatives of quotients of differentiable functions can be found using the quotient rule (BC-EK-FUN-3B2): the numerator is the denominator times the derivative of the numerator minus the numerator times the derivative of the denominator, and the denominator is the square of the original denominator.

**Order matters.** Reversing the two terms in the numerator changes the sign of the whole derivative.

**Constant denominator.** When the denominator carries no variable the constant multiple rule is the shorter route.

**Notation.** quotient rule.

### Representations

Representations in play: BC-REP-01 Symbolic (analytical) expression, BC-REP-03 Numerical table, BC-REP-02 Graphical.

Conversions tested: supplied values of two functions and their derivatives to a derivative of their quotient (BC-REP-03 to BC-REP-01).

### Assessment behaviour

MCQ forms ask for the derivative of a quotient, either symbolically or from supplied values. FRQ forms use the rule inside larger computations. Calculator variants are uncommon; no-calculator variants dominate. Conceptual variants test the order of the numerator terms; computational variants produce the derivative; interpretation variants read the result in context; justification variants ask why the quotient rule rather than the constant multiple rule applies. Multi-concept variants feed the result into the trigonometric derivatives of the following topic.

### Archetypes

- BC-QA-02008 Derivative of a product or a quotient by rule
- BC-QA-02009 Derivative of a product or quotient evaluated from supplied values

### Errors and misconceptions

- BC-ERR-02021 Quotient rule numerator terms reversed
- BC-ERR-02022 Denominator square omitted
- BC-ERR-02023 Quotient rule applied where the denominator is constant
- BC-ERR-02024 Function value used where a derivative value was required
- BC-MIS-02012 The quotient rule is symmetric, severity high

### Diagnostic signals

- BC-SIG-02014 Quotient rule applied with the numerator terms reversed, mastery state partially_mastered

### Adaptive metadata summary

Skills in this topic carry calculator relevance none. Remediation targets named across the topic: BC-SKL-02029, BC-SKL-02036, BC-SKL-02039. Every skill record carries the full seven key adaptive block in data/staging/unit-02.skills.json. [inferred]

## 2.10 Finding the Derivatives of Tangent, Cotangent, Secant, and/or Cosecant Functions

### Official mapping

Topic id BC-TOP-0210, CED code 2.10, name Finding the Derivatives of Tangent, Cotangent, Secant, and/or Cosecant Functions, scope shared, CED page 69. [verified] (ced:69)

- BC-LO-FUN-3B (FUN-3.B): Calculate derivatives of products and quotients of differentiable functions.
  - BC-EK-FUN-3B1 (FUN-3.B.1): "Derivatives of products of differentiable functions can be found using the product rule."
  - BC-EK-FUN-3B2 (FUN-3.B.2): "Derivatives of quotients of differentiable functions can be found using the quotient rule."
  - BC-EK-FUN-3B3 (FUN-3.B.3): "Rearranging tangent, cotangent, secant, and cosecant functions using identities allows differentiation using derivative rules."

Suggested practice skills: BC-MPS-1D (Practice skill 1.D). Weighting pointer: [../exam/exam-blueprint.md](../exam/exam-blueprint.md).

### Concept breakdown

- BC-CON-02015 Derivatives of the remaining trigonometric functions by rewriting: Tangent, cotangent, secant, and cosecant are differentiated by writing them with sine and cosine and applying the quotient rule.

- BC-SKL-02043 Rewrite tangent, cotangent, secant, and cosecant using sine and cosine: Turn the other trigonometric functions into quotients of sine and cosine.
- BC-SKL-02044 Differentiate tangent and cotangent: Apply the quotient rule to the rewritten form and simplify with the Pythagorean identity.
- BC-SKL-02045 Differentiate secant and cosecant: Apply the quotient rule to the reciprocal form and write the result as a product.
- BC-SKL-02046 Select the identity that makes a trigonometric expression differentiable by rule: Choose the rewriting that leaves an expression the available rules can handle.

### Prerequisites

- BC-PRQ-02002 -> BC-SKL-02043, supporting, [inferred], Prerequisite for Rewrite tangent, cotangent, secant, and cosecant using sine and cosine.
- BC-SKL-02043 -> BC-SKL-02044, hard_prerequisite, [inferred], Prerequisite for Differentiate tangent and cotangent.
- BC-SKL-02039 -> BC-SKL-02044, hard_prerequisite, [inferred], Prerequisite for Differentiate tangent and cotangent.
- BC-SKL-02043 -> BC-SKL-02045, hard_prerequisite, [inferred], Prerequisite for Differentiate secant and cosecant.
- BC-SKL-02039 -> BC-SKL-02045, hard_prerequisite, [inferred], Prerequisite for Differentiate secant and cosecant.
- BC-PRQ-02002 -> BC-SKL-02046, supporting, [inferred], Prerequisite for Select the identity that makes a trigonometric expression differentiable by rule.
- BC-SKL-02039 -> BC-SKL-02044, hard_prerequisite, [inferred], The tangent and cotangent derivatives are obtained by the quotient rule.
- BC-SKL-02039 -> BC-SKL-02045, hard_prerequisite, [inferred], The secant and cosecant derivatives are obtained by the quotient rule.
- BC-SKL-02043 -> BC-SKL-02046, hard_prerequisite, [inferred], Selecting an identity rests on being able to carry out the rewriting.
- BC-SKL-02032 -> BC-SKL-02044, supporting, [inferred], The sine and cosine derivatives feed the quotient rule computation.

### Required mathematical knowledge

**Rewriting.** Rearranging tangent, cotangent, secant, and cosecant using identities allows differentiation using derivative rules (BC-EK-FUN-3B3). Each of the four is a quotient built from sine and cosine.

**Results.** The quotient rule applied to the rewritten forms and simplified with the Pythagorean identity gives secant squared for tangent, the negative of cosecant squared for cotangent, secant times tangent for secant, and the negative of cosecant times cotangent for cosecant.

**Why the rewriting matters.** The suggested practice skill for this topic is identifying an appropriate rule or procedure based on the relationship between concepts or processes (BC-MPS-1D, ced:69), so the selection of the identity is itself part of the assessed work.

**Notation.** The result written in the trigonometric form the question requests.

### Representations

Representations in play: BC-REP-01 Symbolic (analytical) expression, BC-REP-04 Verbal description.

Conversions tested: a reciprocal or quotient trigonometric expression to a sine and cosine form (BC-REP-01 to BC-REP-01).

### Assessment behaviour

MCQ forms ask for the derivative of an expression containing one of the four functions. FRQ forms use these derivatives inside larger computations. Calculator variants are uncommon; no-calculator variants dominate. Conceptual variants ask which identity to apply; computational variants produce the derivative; interpretation variants are rare; justification variants derive the result from the quotient rule rather than quoting it. Multi-concept variants combine the rewriting with a product or with a chain structure belonging to Unit 3.

### Archetypes

- BC-QA-02010 Derivative of a tangent, cotangent, secant, or cosecant expression

### Errors and misconceptions

- BC-ERR-02025 Cofunction derivative given without its negative sign
- BC-ERR-02026 Trigonometric quotient differentiated term by term
- BC-MIS-02013 The remaining trigonometric derivatives are independent facts, severity medium

### Diagnostic signals

- BC-SIG-02015 Trigonometric rewriting correct with the quotient rule misapplied, mastery state partially_mastered

### Adaptive metadata summary

Skills in this topic carry calculator relevance none. Remediation targets named across the topic: BC-PRQ-02002, BC-SKL-02043. Every skill record carries the full seven key adaptive block in data/staging/unit-02.skills.json. [inferred]

## Cross-unit connections

Cross-unit edges use BC-TOP ids as the node on the other unit's side wherever no skill exists in data/skills.json for that unit; the `notes` field on each edge in data/staging/unit-02.edges.csv describes the skill that the topic id stands in for. Unit 1 is already merged into data/skills.json, so edges into Unit 1 use skill ids directly. [inferred]

### What Unit 2 depends on

**Unit 1 limits.** BC-SKL-02005, BC-SKL-02006, BC-SKL-02007, and BC-SKL-02008 rest on the Unit 1 limit concept recorded as BC-SKL-01003, and BC-SKL-02009 rests on BC-SKL-01024, the algebraic resolution of an indeterminate quotient, since the difference quotient is indeterminate at zero increment. BC-SKL-02022 uses the Unit 1 one sided limit reading BC-SKL-01010 and BC-SKL-02023 uses the unbounded case BC-SKL-01012.

**Unit 1 continuity.** BC-SKL-02019 rests on BC-SKL-01043, the three conditions of continuity at a point, BC-SKL-02020 on BC-SKL-01065, verifying the continuity hypothesis with a reason, and BC-SKL-02024 on BC-SKL-01044, the continuity test itself. BC-SKL-02021 uses BC-SKL-01040, the classification of a jump, to produce a continuous function with no derivative.

**Unit 1 estimation and representation.** BC-SKL-02014 and BC-SKL-02003 rest on BC-SKL-01001, BC-SKL-02016 on BC-SKL-01016, BC-SKL-02017 on BC-SKL-01009, and BC-SKL-02011 on BC-SKL-01036.

**Non-calculus prerequisites.** Five are minted here, BC-PRQ-02001 to BC-PRQ-02005. Three existing prerequisites are reused rather than minted again: BC-PRQ-06002 for exponent rules, BC-PRQ-06003 for logarithm properties, and BC-PRQ-01005 for exact trigonometric values.

### What depends on Unit 2

**Unit 1.** The dependency runs back as well as forward: BC-SKL-02019 supplies the continuity hypothesis that BC-TOP-0116 requires, which is how the 2025 free response question reaches its Intermediate Value Theorem conclusion (sg-25:12).

**Unit 3.** BC-SKL-02009 underlies the chain rule at BC-TOP-0301, BC-SKL-02036 underlies implicit differentiation at BC-TOP-0302, and BC-SKL-02039 underlies the inverse function derivatives at BC-TOP-0303.

**Unit 4.** BC-SKL-02003 is the subject of BC-TOP-0401, BC-SKL-02014 supports the motion analysis at BC-TOP-0402, BC-SKL-02013 becomes linear approximation at BC-TOP-0406, and BC-SKL-02008 marks where L'Hospital's rule at BC-TOP-0407 takes over the indeterminate forms that Unit 1 and Unit 2 handle by algebra.

**Unit 5.** BC-SKL-02019 supplies one of the two hypotheses of the Mean Value Theorem at BC-TOP-0501, and BC-SKL-02031 supplies the derivative that the first derivative test at BC-TOP-0502 analyses.

**Unit 6.** Antiderivative recognition reverses these rules: BC-SKL-02025 and BC-SKL-02032 feed BC-TOP-0607, and BC-SKL-02036 becomes integration by parts at BC-TOP-0611.

**Unit 7 and Unit 10.** BC-SKL-02013 supports slope fields at BC-TOP-0702, and BC-SKL-02008 supports the Taylor polynomial construction at BC-TOP-1011.

## Archetype summary

Thirteen archetypes with forty two variants are recorded in data/staging/unit-02.archetypes.json. Variant dimensions used are representation, reasoning direction, notation, and context. Free response grounding for Unit 2 in 2023 to 2025 is thin: only the derivative estimate from a table (BC-QA-02001) and the continuity deduced from differentiability (BC-QA-02004) match rubric bearing parts, BC-QA-02013 is single-source against the rounding and setup conventions of a calculator active part, and the remaining ten archetypes are tagged inferred from the CED text. [verified] (sg-25:11, sg-25:12, sg-24:2, sg-23:14)

| Archetype | Name | Scope | Calculator | Official parts read |
|---|---|---|---|---|
| BC-QA-02001 | Derivative estimated from a table with units | shared | either | 2025 Q3(A), 2024 Q1(a) |
| BC-QA-02002 | Derivative computed from the limit definition | shared | no_calculator | none in 2023 to 2025 [inferred] |
| BC-QA-02003 | Limit recognised as a derivative of a known function | shared | no_calculator | none in 2023 to 2025 [inferred] |
| BC-QA-02004 | Continuity deduced from differentiability inside a larger argument | shared | no_calculator | 2025 Q3(B), 2023 Q4(c) |
| BC-QA-02005 | Point of non-differentiability identified on a continuous function | shared | no_calculator | none in 2023 to 2025 as a standalone part [inferred] |
| BC-QA-02006 | Derivative of a polynomial or power expression by rule | shared | no_calculator | none in 2023 to 2025 as a standalone part [inferred] |
| BC-QA-02007 | Derivative of an expression built from the basic transcendental functions | shared | no_calculator | none in 2023 to 2025 as a standalone part [inferred] |
| BC-QA-02008 | Derivative of a product or a quotient by rule | shared | no_calculator | none in 2023 to 2025 as a standalone part [inferred] |
| BC-QA-02009 | Derivative of a product or quotient evaluated from supplied values | shared | no_calculator | none in 2023 to 2025 as a standalone part [inferred] |
| BC-QA-02010 | Derivative of a tangent, cotangent, secant, or cosecant expression | shared | no_calculator | none in 2023 to 2025 as a standalone part [inferred] |
| BC-QA-02011 | Tangent line written at a point on a curve | shared | no_calculator | none in 2023 to 2025 as a standalone part [inferred] |
| BC-QA-02012 | Derivative notation read or converted | shared | no_calculator | none in 2023 to 2025 as a standalone part [inferred] |
| BC-QA-02013 | Derivative at a point produced with technology | shared | calculator | 2023 Q1(d) evaluates a derivative from a supplied model in a calculator active part |

## Misconception summary

Fifteen misconceptions are recorded in data/staging/unit-02.misconceptions.json against thirty two observed errors in data/staging/unit-02.errors.json. The mapping is many to many: an error lists every misconception that could produce it together with non-conceptual causes such as an arithmetic slip, a misread, or time pressure, and every misconception carries rival misconceptions and a discriminating probe. Three misconceptions are tagged verified because a scoring guideline names the behaviour directly; the rest are inferred from the CED text. [verified] (sg-25:11, sg-25:12, sg-24:2)

| Misconception | Severity | Rivals | Discriminating probe |
|---|---|---|---|
| BC-MIS-02001 A rate is a difference | high | BC-MIS-02008 | Ask for the units of the reported number and compare them with the units the question asks for. |
| BC-MIS-02002 The definition of the derivative is a formality to be written and then abandoned | high | BC-MIS-02003 | Ask the student to point to the step in the work where the increment stops appearing in the denominator, and why it may be removed there. |
| BC-MIS-02003 The limit symbol is decoration on the final line | medium | BC-MIS-02002 | Ask the student to read the second line of the work as a sentence and say whether it is true for every increment. |
| BC-MIS-02004 A limit is resolved only by algebra | medium | BC-MIS-02002 | Ask the student to name a function whose values appear in the numerator and what input it is evaluated at. |
| BC-MIS-02005 A hypothesis holds because the setting supplies it | high | BC-MIS-02006 | Ask what in the question establishes that the function is continuous. |
| BC-MIS-02006 Differentiability and continuity are the same property | high | BC-MIS-02005 | Ask for a function continuous at a point at which it has no derivative, and then for one differentiable but not continuous there. |
| BC-MIS-02007 Differentiability is a visual property of the graph | medium | BC-MIS-02006 | Ask for the slope approached from each side as two separate numbers before the verdict is given. |
| BC-MIS-02008 Units are decoration rather than part of the answer | medium | BC-MIS-02001 | Ask what the denominator of the quotient measures and what the resulting compound unit is. |
| BC-MIS-02009 The power rule is a move on the exponent alone | high | BC-MIS-02010 | Ask the student to differentiate a squared term from the definition and compare the result with the rule. |
| BC-MIS-02010 Every function is differentiated by the power rule | high | BC-MIS-02009 | Ask which of the base and the exponent contains the variable in the expression being differentiated. |
| BC-MIS-02011 Differentiation distributes across a product | high | BC-MIS-02012 | Ask the student to expand a simple product, differentiate term by term, and compare with the proposed answer. |
| BC-MIS-02012 The quotient rule is symmetric | high | BC-MIS-02011 | Ask the student to apply the rule to a reciprocal whose derivative the power rule already gives and compare the two results. |
| BC-MIS-02013 The remaining trigonometric derivatives are independent facts | medium | BC-MIS-02012 | Ask the student to obtain the derivative from the sine and cosine form rather than from memory. |
| BC-MIS-02014 The derivative and the function value are interchangeable at a point | high | BC-MIS-02015 | Ask which of the two computed numbers has the units of a slope. |
| BC-MIS-02015 Derivative notation is a set of interchangeable labels | medium | BC-MIS-02014 | Ask what the symbol denotes and whether the object it names depends on the variable. |

## Unresolved

- data/curriculum.json names the unit Differentiation: Definition and Fundamental Properties. The CED pages for this unit carry the running head Differentiation: Definition and Fundamental Properties (ced:60, ced:69). The file follows the curriculum record for the unit name and records the CED wording here. [verified] (ced:60, ced:69)
- No 2023 to 2025 free response question assesses Unit 2 as its main subject. The parts that touch it are 2025 Q3(A), a derivative estimated from a table with units (sg-25:11), 2024 Q1(a), the same task over a bracketing interval (sg-24:2), 2025 Q3(B), which uses differentiability to establish continuity (sg-25:12), and 2023 Q4(c), which uses the same implication at a point (sg-23:14). Archetypes BC-QA-02002, BC-QA-02003, BC-QA-02005, BC-QA-02006, BC-QA-02007, BC-QA-02008, BC-QA-02009, BC-QA-02010, BC-QA-02011, and BC-QA-02012 have no matching free response part in those years and are tagged inferred; their scoring patterns are drawn from the CED description of the topic rather than from a rubric for that exact task. [uncertain]
- BC-QA-02013 records the calculator active derivative evaluation. The rounding and setup conventions quoted for it are general scoring notes that apply across a question rather than a rubric written for that task, so the archetype is tagged single-source. [single-source] (sg-25:4)
- The derivative rules of topics 2.5 to 2.10 are stated in the CED without the exclusion or inclusion of a proof requirement. BC-SKL-02027 records deriving a power rule case from the definition because BC-EK-FUN-3A1 names direct application of the definition alongside the specific rules; whether a free response part would demand that derivation is not established here. [uncertain] (ced:64)
- The CED page numbering used in citations is the PDF page index in cache/text/ced, which runs five ahead of the printed page numbers on those pages for this unit. [verified] (ced:60, ced:69)
- No misconception literature is cited. None could be confirmed from the sources available in this project's cache, so every misconception record is tagged inferred unless a scoring guideline names the behaviour directly. [inferred]

<!-- generated:official-evidence:start -->

## Official evidence index [verified]

Generated from data/frq_records.json and data/mcq_records.json. Every record cites its cached document and page; counts are observations over the indexed years only, not predictions. FRQ part records with BC-UNIT-02 as primary or secondary unit: 37. Public sample MCQ records tagged to this unit: 8.

| FRQ record | Role | Calculator | Archetype | Skills (first six) | Points | Point types |
|---|---|---|---|---|---|---|
| BC-FRQ-2013-Q3-A | primary | no_calculator | BC-QA-02001 | BC-SKL-02014, BC-SKL-02016, BC-SKL-02015, BC-SKL-04004, BC-SKL-04001 | 2 | BC-PT-99021, BC-PT-99006 |
| BC-FRQ-2013-Q3-B | secondary | no_calculator | BC-QA-05001 | BC-SKL-05001, BC-SKL-05002, BC-SKL-05003, BC-SKL-05004, BC-SKL-02019, BC-SKL-02020 | 2 | BC-PT-99021, BC-PT-99017 |
| BC-FRQ-2013-Q3-D | primary | no_calculator | BC-QA-02007 | BC-SKL-02033, BC-SKL-03002, BC-SKL-02029, BC-SKL-04014 | 2 | BC-PT-99023, BC-PT-99004 |
| BC-FRQ-2013-Q4-D | secondary | no_calculator | BC-QA-03001 | BC-SKL-03002, BC-SKL-03005, BC-SKL-03006, BC-SKL-02012 | 3 | BC-PT-99023, BC-PT-99004 |
| BC-FRQ-2014-Q1-A | primary | calculator | BC-QA-99007 | BC-SKL-01001, BC-SKL-02003, BC-SKL-04001, BC-SKL-02002 | 1 | BC-PT-99021 |
| BC-FRQ-2014-Q1-D | secondary | calculator | BC-QA-04008 | BC-SKL-04028, BC-SKL-04029, BC-SKL-04032, BC-SKL-02013 | 4 | BC-PT-99025, BC-PT-99068, BC-PT-99004 |
| BC-FRQ-2014-Q3-C | primary | no_calculator | BC-QA-02008 | BC-SKL-02039, BC-SKL-02040, BC-SKL-06018, BC-SKL-06020 | 3 | BC-PT-99080, BC-PT-99004 |
| BC-FRQ-2014-Q3-D | secondary | no_calculator | BC-QA-03001 | BC-SKL-03002, BC-SKL-03005, BC-SKL-03006 | 3 | BC-PT-99023, BC-PT-99004 |
| BC-FRQ-2014-Q4-A | secondary | no_calculator | BC-QA-04003 | BC-SKL-01001, BC-SKL-02002, BC-SKL-04007, BC-SKL-02003 | 1 | BC-PT-99021 |
| BC-FRQ-2014-Q4-B | secondary | no_calculator | BC-QA-01011 | BC-SKL-01064, BC-SKL-01065, BC-SKL-01066, BC-SKL-01067, BC-SKL-01068, BC-SKL-02019 | 2 | BC-PT-99015, BC-PT-99016 |
| BC-FRQ-2014-Q5-C | secondary | no_calculator | BC-QA-08014 | BC-SKL-08056, BC-SKL-08057, BC-SKL-02036, BC-SKL-03002 | 3 | BC-PT-99022, BC-PT-99051, BC-PT-99004 |
| BC-FRQ-2015-Q3-A | primary | no_calculator | BC-QA-02001 | BC-SKL-02014, BC-SKL-02016, BC-SKL-04007 | 1 | BC-PT-99021 |
| BC-FRQ-2015-Q3-C | secondary | no_calculator | BC-QA-04003 | BC-SKL-04007, BC-SKL-02031, BC-SKL-02025 | 2 | BC-PT-99027, BC-PT-99004 |
| BC-FRQ-2015-Q5-A | primary | no_calculator | BC-QA-02011 | BC-SKL-02012, BC-SKL-02013 | 2 | BC-PT-99082, BC-PT-99004 |
| BC-FRQ-2018-Q4-A | primary | no_calculator | BC-QA-02001 | BC-SKL-02014, BC-SKL-02016, BC-SKL-02015, BC-SKL-04002, BC-SKL-04004 | 0 |  |
| BC-FRQ-2018-Q4-B | secondary | no_calculator | BC-QA-05001 | BC-SKL-05001, BC-SKL-05002, BC-SKL-05003, BC-SKL-05004, BC-SKL-02019, BC-SKL-02020 | 0 |  |
| BC-FRQ-2018-Q4-D | secondary | no_calculator | BC-QA-04006 | BC-SKL-04017, BC-SKL-04019, BC-SKL-04024, BC-SKL-04026, BC-SKL-02039, BC-SKL-03002 | 0 |  |
| BC-FRQ-2019-Q5-A | primary | no_calculator | BC-QA-02008 | BC-SKL-02039, BC-SKL-03002, BC-SKL-02012, BC-SKL-05001 | 3 | BC-PT-99005, BC-PT-99005, BC-PT-99004 |
| BC-FRQ-2021-Q1-A | primary | calculator | BC-QA-04002 | BC-SKL-02014, BC-SKL-02016, BC-SKL-02015, BC-SKL-04002, BC-SKL-04001 | 2 | BC-PT-99005, BC-PT-99008 |
| BC-FRQ-2021-Q1-C | secondary | calculator | BC-QA-06001 | BC-SKL-06010, BC-SKL-02036, BC-SKL-05017 | 2 | BC-PT-99022, BC-PT-99026 |
| BC-FRQ-2021-Q4-B | primary | no_calculator | BC-QA-02009 | BC-SKL-02036, BC-SKL-02037, BC-SKL-06018, BC-SKL-06020, BC-SKL-06028 | 3 | BC-PT-99022, BC-PT-99069, BC-PT-99004 |
| BC-FRQ-2022-Q2-A | secondary | calculator | BC-QA-09001 | BC-SKL-09002, BC-SKL-09004, BC-SKL-09003 | 1 | BC-PT-99005 |
| BC-FRQ-2022-Q3-C | secondary | no_calculator | BC-QA-05008 | BC-SKL-05015, BC-SKL-05017, BC-SKL-02030, BC-SKL-05014 | 2 | BC-PT-99005, BC-PT-99063 |
| BC-FRQ-2022-Q4-A | primary | no_calculator | BC-QA-04002 | BC-SKL-02014, BC-SKL-02016, BC-SKL-02015, BC-SKL-04004, BC-SKL-03030 | 2 | BC-PT-99005, BC-PT-99006 |
| BC-FRQ-2022-Q4-B | secondary | no_calculator | BC-QA-01011 | BC-SKL-01064, BC-SKL-01065, BC-SKL-01066, BC-SKL-01067, BC-SKL-02019 | 2 | BC-PT-99015, BC-PT-99016 |
| BC-FRQ-2022-Q4-D | secondary | no_calculator | BC-QA-04006 | BC-SKL-04018, BC-SKL-04019, BC-SKL-04020, BC-SKL-04023, BC-SKL-04024 | 3 | BC-PT-99022, BC-PT-99023, BC-PT-99004 |
| BC-FRQ-2023-Q1-B | secondary | calculator | BC-QA-05001 | BC-SKL-05006, BC-SKL-05003, BC-SKL-02019, BC-SKL-05001 | 2 | BC-PT-99021, BC-PT-99017 |
| BC-FRQ-2023-Q4-C | secondary | no_calculator | BC-QA-04009 | BC-SKL-04033, BC-SKL-04034, BC-SKL-04035, BC-SKL-04036, BC-SKL-02019, BC-SKL-04038 | 3 | BC-PT-99054, BC-PT-99055, BC-PT-99005 |
| BC-FRQ-2023-Q6-A | secondary | no_calculator | BC-QA-10010 | BC-SKL-02036, BC-SKL-03002, BC-SKL-03031, BC-SKL-10043, BC-SKL-10044, BC-SKL-10046 | 4 | BC-PT-99022, BC-PT-99027, BC-PT-99035, BC-PT-99036 |
| BC-FRQ-2023-Q6-C | secondary | no_calculator | BC-QA-10012 | BC-SKL-02036, BC-SKL-03030, BC-SKL-10044, BC-SKL-10047, BC-SKL-10065 | 3 | BC-PT-99027, BC-PT-99035, BC-PT-99036 |
| BC-FRQ-2024-Q1-A | primary | calculator | BC-QA-04002 | BC-SKL-02014, BC-SKL-02016, BC-SKL-02015, BC-SKL-04004, BC-SKL-04001 | 2 | BC-PT-99005, BC-PT-99006 |
| BC-FRQ-2025-Q1-B | primary | calculator | BC-QA-08002 | BC-SKL-02001, BC-SKL-02004, BC-SKL-05003, BC-SKL-05005, BC-SKL-08004 | 2 | BC-PT-99021, BC-PT-99005 |
| BC-FRQ-2025-Q3-A | primary | no_calculator | BC-QA-04002 | BC-SKL-02014, BC-SKL-02016, BC-SKL-02015, BC-SKL-04004, BC-SKL-04001 | 2 | BC-PT-99005, BC-PT-99006 |
| BC-FRQ-2025-Q3-B | secondary | no_calculator | BC-QA-01011 | BC-SKL-01064, BC-SKL-01065, BC-SKL-01066, BC-SKL-01067, BC-SKL-01068, BC-SKL-02019 | 2 | BC-PT-99015, BC-PT-99016 |
| BC-FRQ-2026-Q1-A | primary | calculator | BC-QA-04002 | BC-SKL-02014, BC-SKL-02016, BC-SKL-02015, BC-SKL-04004, BC-SKL-04001 | 2 | BC-PT-99005, BC-PT-99006 |
| BC-FRQ-2026-Q1-D | secondary | calculator | BC-QA-01011 | BC-SKL-01064, BC-SKL-01065, BC-SKL-01066, BC-SKL-01067, BC-SKL-02019 | 2 | BC-PT-99015, BC-PT-99016 |
| BC-FRQ-2026-Q4-A | primary | no_calculator | BC-QA-02007 | BC-SKL-02034, BC-SKL-02030, BC-SKL-02029, BC-SKL-02017 | 2 | BC-PT-99005, BC-PT-99004 |

| MCQ record | Calculator | Archetype | Skills |
|---|---|---|---|
| BC-MCQ-CED-002 | no_calculator | BC-QA-02005 | BC-SKL-02024, BC-SKL-02022, BC-SKL-01023 |
| BC-MCQ-CED-003 | no_calculator | BC-QA-02009 | BC-SKL-02037, BC-SKL-02036, BC-SKL-02029 |
| BC-MCQ-SAMPLE-003 | no_calculator | BC-QA-02005 | BC-SKL-02022, BC-SKL-02023, BC-SKL-01042 |
| BC-MCQ-SAMPLE-006 | no_calculator | BC-QA-02002 | BC-SKL-02006, BC-SKL-02007, BC-SKL-01007 |
| BC-MCQ-PE2012-011 | no_calculator | BC-QA-02005 | BC-SKL-02022, BC-SKL-02021, BC-SKL-01044 |
| BC-MCQ-PE2012-019 | no_calculator | BC-QA-02011 | BC-SKL-02039, BC-SKL-02012, BC-SKL-02013 |
| BC-MCQ-PE2012-029 | calculator | BC-QA-05009 | BC-SKL-02022, BC-SKL-05011, BC-SKL-05031 |
| BC-MCQ-PE2012-030 | calculator | BC-QA-05008 | BC-SKL-05014, BC-SKL-02033, BC-SKL-08021 |

<!-- generated:official-evidence:end -->
