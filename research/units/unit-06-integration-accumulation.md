---
title: Unit 6, Integration and Accumulation of Change
research_date: 2026-09-19
status: draft
purpose: Decompose CED Unit 6 into concepts, atomic skills, non-calculus prerequisites, question archetypes and variants, observed errors, candidate misconceptions, and diagnostic signals, each grounded in the CED text and in the 2023 to 2025 official free-response questions and scoring guidelines.
---

# Unit 6, Integration and Accumulation of Change

BC-UNIT-06 covers CED pages 112 to 131 and holds fourteen topics. Topics 6.11, 6.12, and 6.13 carry the BC only marker in the CED and in data/curriculum.json; topics 6.1 through 6.10 and topic 6.14 are shared with AB. Unit weighting is in [../exam/exam-blueprint.md](../exam/exam-blueprint.md) and exam composition is in [../exam/exam-structure.md](../exam/exam-structure.md). [verified] (ced:112, ced:128, ced:129, ced:130)

## 6.1 Exploring Accumulations of Change

### Official mapping

Topic id BC-TOP-0601, CED code 6.1, name Exploring Accumulations of Change, scope shared, CED page 118. [verified] (ced:118)

- BC-LO-CHA-4A (CHA-4.A): Interpret the meaning of areas associated with the graph of a rate of change in context.
  - BC-EK-CHA-4A1 (CHA-4.A.1): "The area of the region between the graph of a rate of change function and the x axis gives the accumulation of change."
  - BC-EK-CHA-4A2 (CHA-4.A.2): "In some cases, accumulation of change can be evaluated by using geometry."
  - BC-EK-CHA-4A3 (CHA-4.A.3): "If a rate of change is positive (negative) over an interval, then the accumulated change is positive (negative)."
  - BC-EK-CHA-4A4 (CHA-4.A.4): "The unit for the area of a region defined by rate of change is the unit for the rate of change multiplied by the unit for the independent variable."

Suggested practice skills: BC-MPS-4B (Practice skill 4.B). Weighting pointer: [../exam/exam-blueprint.md](../exam/exam-blueprint.md).

### Concept breakdown

- BC-CON-06001 Accumulation of change as area under a rate graph: The area between a rate of change graph and the horizontal axis measures how much the quantity changed.
- BC-CON-06002 Sign and units of accumulated change: The sign of the rate fixes the sign of the accumulated change, and the units multiply.

- BC-SKL-06001 Interpret the area under a rate of change graph as accumulated change: Say what the area between a rate graph and the axis measures in the situation described.
- BC-SKL-06002 State the units of an accumulated change: Give the units of an accumulation as rate units times independent variable units.
- BC-SKL-06003 Determine the sign of accumulated change from the sign of the rate: Decide whether the quantity rose or fell over an interval from whether the rate was positive or negative.
- BC-SKL-06004 Compute accumulated change from a piecewise linear rate graph using geometry: Add up triangle and rectangle areas under a rate graph to get the total change.

### Prerequisites

- BC-PRQ-06005 -> BC-SKL-06001, supporting, [inferred], Prerequisite for Interpret the area under a rate of change graph as accumulated change.
- BC-PRQ-06005 -> BC-SKL-06002, supporting, [inferred], Prerequisite for State the units of an accumulated change.
- BC-PRQ-06007 -> BC-SKL-06004, supporting, [inferred], Prerequisite for Compute accumulated change from a piecewise linear rate graph using geometry.

### Required mathematical knowledge

**Rate and accumulation.** For a rate of change function f on [a,b], the signed area of the region between the graph of f and the x axis over [a,b] is the accumulated change in the quantity whose rate is f.

**Units.** The unit of that area is the unit of f multiplied by the unit of the independent variable (BC-EK-CHA-4A4).

**Sign.** A rate positive on an interval gives positive accumulated change; a rate negative on an interval gives negative accumulated change (BC-EK-CHA-4A3).

**Notation.** Area of a region, accumulated change, units written as a product such as gallons per second multiplied by seconds.

### Representations

Representations in play: BC-REP-02 Graphical, BC-REP-04 Verbal description, BC-REP-05 Contextual model.

Conversions tested: graph of a rate to a verbal statement of accumulated change with units (BC-REP-02 to BC-REP-04), and contextual model to signed area (BC-REP-05 to BC-REP-02).

### Assessment behaviour

MCQ forms ask for the meaning of an area under a rate graph or for the units of an accumulation. FRQ forms embed the interpretation in a part that also demands a numerical approximation, and the interpretation is scored separately (sg-23:2). Calculator variants supply a formula for the rate; no-calculator variants supply a graph made of segments. Conceptual variants ask only for the sign or the units; computational variants ask for the accumulated amount from geometry; interpretation variants ask for a sentence naming the quantity, its units, and the interval; justification variants ask why the accumulation is positive or negative. Multi-concept variants combine the interpretation with a Riemann sum in the same part (sg-23:2).

### Archetypes

- BC-QA-06004 Definite integral evaluated from a graph by geometry
- BC-QA-06015 Interpreting a definite integral in context with units

### Errors and misconceptions

- BC-ERR-06013 Semicircular region given the area of a full circle
- BC-ERR-06014 Regions below the axis added as positive area
- BC-ERR-06029 Interpretation of a definite integral omits the interval or the units
- BC-ERR-06030 Average value expression interpreted as a total
- BC-MIS-06011 Area formulas are recalled without their fractional factors, severity medium
- BC-MIS-06012 The definite integral measures unsigned area, severity high
- BC-MIS-06014 Average value and accumulated amount are the same quantity, severity high
- BC-MIS-06025 An interpretation is complete once the quantity is named, severity medium

### Diagnostic signals

- No signal is scoped to this topic; the unit level signal list in data/staging/unit-06.signals.json applies.

### Adaptive metadata summary

Skills in this topic carry calculator relevance none. Remediation targets named across the topic: BC-CON-06002, BC-PRQ-06005, BC-PRQ-06007. Every skill record carries the full seven key adaptive block in data/staging/unit-06.skills.json. [inferred]

## 6.2 Approximating Areas with Riemann Sums

### Official mapping

Topic id BC-TOP-0602, CED code 6.2, name Approximating Areas with Riemann Sums, scope shared, CED page 119. [verified] (ced:119)

- BC-LO-LIM-5A (LIM-5.A): Approximate a definite integral using geometric and numerical methods.
  - BC-EK-LIM-5A1 (LIM-5.A.1): "Definite integrals can be approximated for functions that are represented graphically, numerically, analytically, and verbally."
  - BC-EK-LIM-5A2 (LIM-5.A.2): "Definite integrals can be approximated using a left Riemann sum, a right Riemann sum, a midpoint Riemann sum, or a trapezoidal sum; approximations can be computed using either uniform or nonuniform partitions."
  - BC-EK-LIM-5A3 (LIM-5.A.3): "Definite integrals can be approximated using numerical methods, with or without technology."
  - BC-EK-LIM-5A4 (LIM-5.A.4): "Depending on the behavior of a function, it may be possible to determine whether an approximation for a definite integral is an underestimate or overestimate for the value of the definite integral."

Suggested practice skills: BC-MPS-1F (Practice skill 1.F). Weighting pointer: [../exam/exam-blueprint.md](../exam/exam-blueprint.md).

### Concept breakdown

- BC-CON-06003 Riemann sum approximation of a definite integral: A definite integral can be estimated by adding function value times subinterval width over a partition.
- BC-CON-06004 Over and under estimate reasoning for approximations: Whether an approximation is too big or too small follows from how the function rises, falls, or bends.

- BC-SKL-06005 Compute a left Riemann sum from a table of values: Use the value at the left end of each subinterval times its width and add.
- BC-SKL-06006 Compute a right Riemann sum from a table of values: Use the value at the right end of each subinterval times its width and add.
- BC-SKL-06007 Compute a midpoint Riemann sum: Use the value at the centre of each subinterval times its width and add.
- BC-SKL-06008 Compute a trapezoidal sum from a table of values: Average the two endpoint values on each subinterval, multiply by the width, and add.
- BC-SKL-06009 Compute a Riemann sum for a function given by a graph or a formula: Read or evaluate the needed function values yourself, then build the sum.
- BC-SKL-06010 Justify whether a Riemann sum under or over estimates using monotonicity: Argue from the function increasing or decreasing which way the estimate is off.
- BC-SKL-06011 Justify whether a trapezoidal or midpoint sum under or over estimates using concavity: Argue from the bending of the graph which way the estimate is off.

Granularity note: Topic 6.2 carries seven skills because the CED names four distinct approximation methods in BC-EK-LIM-5A2, allows uniform and nonuniform partitions, admits graphical, numerical, analytical, and verbal presentations in BC-EK-LIM-5A1, and adds the over or under estimate determination in BC-EK-LIM-5A4; the methods differ in what the student must do.

### Prerequisites

- BC-PRQ-06005 -> BC-SKL-06005, supporting, [inferred], Prerequisite for Compute a left Riemann sum from a table of values.
- BC-PRQ-06012 -> BC-SKL-06005, supporting, [inferred], Prerequisite for Compute a left Riemann sum from a table of values.
- BC-PRQ-06005 -> BC-SKL-06006, supporting, [inferred], Prerequisite for Compute a right Riemann sum from a table of values.
- BC-PRQ-06012 -> BC-SKL-06006, supporting, [inferred], Prerequisite for Compute a right Riemann sum from a table of values.
- BC-PRQ-06012 -> BC-SKL-06007, supporting, [inferred], Prerequisite for Compute a midpoint Riemann sum.
- BC-PRQ-06007 -> BC-SKL-06008, supporting, [inferred], Prerequisite for Compute a trapezoidal sum from a table of values.
- BC-PRQ-06012 -> BC-SKL-06008, supporting, [inferred], Prerequisite for Compute a trapezoidal sum from a table of values.
- BC-PRQ-06005 -> BC-SKL-06009, supporting, [inferred], Prerequisite for Compute a Riemann sum for a function given by a graph or a formula.
- BC-PRQ-06008 -> BC-SKL-06010, supporting, [inferred], Prerequisite for Justify whether a Riemann sum under or over estimates using monotonicity.
- BC-SKL-06005 -> BC-SKL-06010, hard_prerequisite, [inferred], Prerequisite for Justify whether a Riemann sum under or over estimates using monotonicity.
- BC-SKL-06006 -> BC-SKL-06010, hard_prerequisite, [inferred], Prerequisite for Justify whether a Riemann sum under or over estimates using monotonicity.
- BC-PRQ-06008 -> BC-SKL-06011, supporting, [inferred], Prerequisite for Justify whether a trapezoidal or midpoint sum under or over estimates using concavity.
- BC-SKL-06008 -> BC-SKL-06011, hard_prerequisite, [inferred], Prerequisite for Justify whether a trapezoidal or midpoint sum under or over estimates using concavity.

### Required mathematical knowledge

**Riemann sum.** For a partition of [a,b] into subintervals, an approximation is the sum over subintervals of f at a chosen sample point multiplied by the width of that subinterval. Left, right, and midpoint sums differ only in the sample point.

**Trapezoidal sum.** Each subinterval contributes the average of the two endpoint values multiplied by the width.

**Error direction.** Hypotheses: f monotone on the interval. Conclusion: a left sum underestimates when f is increasing and overestimates when f is decreasing, with the reverse for a right sum. Hypotheses: f concave up on the interval. Conclusion: a trapezoidal sum overestimates and a midpoint sum underestimates, with both reversed when f is concave down.

**Notation.** L sub n, R sub n, M sub n, T sub n; delta x sub i for the width of the ith subinterval; partitions may be uniform or nonuniform (BC-EK-LIM-5A2).

### Representations

Representations in play: BC-REP-01 Symbolic (analytical) expression, BC-REP-02 Graphical, BC-REP-03 Numerical table, BC-REP-05 Contextual model.

Conversions tested: table to numerical approximation (BC-REP-03 to BC-REP-09), graph to numerical approximation (BC-REP-02 to BC-REP-09), and symbolic rate to a tabulated set of values (BC-REP-01 to BC-REP-03).

### Assessment behaviour

MCQ forms present a short table or a graph and ask for one named sum. FRQ forms supply a contextual rate at four tabulated inputs and ask for a left, right, or trapezoidal sum over the subintervals the data indicate (sg-23:2, sg-24:3, sg-25:13). Calculator variants appear in Part A and no-calculator variants in Part B, and the arithmetic in the no-calculator form is kept to integers (sg-25:13). Conceptual variants ask only whether the estimate is high or low; computational variants ask for the value; justification variants require monotonicity or concavity to be named; multi-concept variants attach an interpretation with units to the same part.

### Archetypes

- BC-QA-06001 Riemann sum from a table with over or under estimate reasoning
- BC-QA-06002 Trapezoidal approximation of an accumulated amount from a table

### Errors and misconceptions

- BC-ERR-06001 Uniform width applied to a nonuniform partition
- BC-ERR-06002 Endpoint opposite the one requested used in the Riemann sum
- BC-ERR-06003 Riemann sum reported as a sum of function values
- BC-ERR-06004 Trapezoidal sum with the factor of one half applied to only one term
- BC-ERR-06005 Over or under estimate claimed without reference to the behaviour of the function
- BC-ERR-06006 Under and over estimate directions interchanged for a monotone integrand
- BC-ERR-06007 Trapezoidal direction decided from monotonicity instead of concavity
- BC-MIS-06001 A Riemann sum is a sum of the listed values, severity high
- BC-MIS-06002 The endpoint convention is cosmetic, severity medium
- BC-MIS-06003 Riemann sums are exact, severity medium
- BC-MIS-06004 A trapezoid is a rectangle at the average height of the whole interval, severity medium
- BC-MIS-06005 Approximation direction follows from increase or decrease alone, severity high
- BC-MIS-06006 Concavity and monotonicity are the same property, severity high

### Diagnostic signals

- BC-SIG-06001 Correct Riemann sum products with an arithmetic slip in the total
- BC-SIG-06002 Single width applied across unequal subintervals
- BC-SIG-06003 Correct sum of the opposite endpoint type
- BC-SIG-06004 Sum of table values with no widths
- BC-SIG-06005 Left and right sums averaged without the halving
- BC-SIG-06006 Direction of an estimate asserted with no stated reason
- BC-SIG-06007 Monotonicity cited for a trapezoidal estimate

### Adaptive metadata summary

Skills in this topic carry calculator relevance none, optional. Remediation targets named across the topic: BC-PRQ-06005, BC-PRQ-06007, BC-PRQ-06012, BC-SKL-06005, BC-SKL-06008. Every skill record carries the full seven key adaptive block in data/staging/unit-06.skills.json. [inferred]

## 6.3 Riemann Sums, Summation Notation, and Definite Integral Notation

### Official mapping

Topic id BC-TOP-0603, CED code 6.3, name Riemann Sums, Summation Notation, and Definite Integral Notation, scope shared, CED page 120. [verified] (ced:120)

- BC-LO-LIM-5B (LIM-5.B): Interpret the limiting case of the Riemann sum as a definite integral.
  - BC-EK-LIM-5B1 (LIM-5.B.1): "The limit of an approximating Riemann sum can be interpreted as a definite integral."
  - BC-EK-LIM-5B2 (LIM-5.B.2): "A Riemann sum, which requires a partition of an interval I, is the sum of products, each of which is the value of the function at a point in a subinterval multiplied by the length of that subinterval of the partition."
- BC-LO-LIM-5C (LIM-5.C): Represent the limiting case of the Riemann sum as a definite integral.
  - BC-EK-LIM-5C1 (LIM-5.C.1): "The definite integral of a continuous function f over the interval [a, b], denoted by the integral from a to b of f(x) dx, is the limit of Riemann sums as the widths of the subintervals approach 0. That is, the integral from a to b of f(x) dx = lim as the maximum of delta x sub i approaches 0 of the sum from i = 1 to n of f(x sub i star) delta x sub i, where n is the number of subintervals, delta x sub i is the width of the ith subinterval, and x sub i star is a value in the ith subinterval."
  - BC-EK-LIM-5C2 (LIM-5.C.2): "A definite integral can be translated into the limit of a related Riemann sum, and the limit of a Riemann sum can be written as a definite integral."

Suggested practice skills: BC-MPS-2C (Practice skill 2.C). Weighting pointer: [../exam/exam-blueprint.md](../exam/exam-blueprint.md).

### Concept breakdown

- BC-CON-06005 Summation notation and the Riemann sum as a sum of products: Sigma notation writes a Riemann sum compactly as a sum of products.
- BC-CON-06006 Definite integral as the limit of Riemann sums: Letting every subinterval width go to zero turns the Riemann sum into the definite integral.

- BC-SKL-06012 Expand summation notation into an explicit Riemann sum: Write out the terms of a sigma expression as products of a value and a width.
- BC-SKL-06013 Write a Riemann sum in sigma notation for a given function, interval, and partition: Build the sigma expression from the function, the endpoints, and the number of subintervals.
- BC-SKL-06014 Convert the limit of a Riemann sum into a definite integral: Read the integrand and the limits of integration out of a limit of sums.
- BC-SKL-06015 Express a definite integral as the limit of a Riemann sum: Go the other way and write the integral as a limit of sums.
- BC-SKL-06016 State the limit definition of the definite integral: Recite the definition, including that the subinterval widths go to zero.

### Prerequisites

- BC-PRQ-06006 -> BC-SKL-06012, supporting, [inferred], Prerequisite for Expand summation notation into an explicit Riemann sum.
- BC-PRQ-06006 -> BC-SKL-06013, supporting, [inferred], Prerequisite for Write a Riemann sum in sigma notation for a given function, interval, and partition.
- BC-PRQ-06006 -> BC-SKL-06014, supporting, [inferred], Prerequisite for Convert the limit of a Riemann sum into a definite integral.
- BC-SKL-06012 -> BC-SKL-06014, hard_prerequisite, [inferred], Prerequisite for Convert the limit of a Riemann sum into a definite integral.
- BC-PRQ-06006 -> BC-SKL-06015, supporting, [inferred], Prerequisite for Express a definite integral as the limit of a Riemann sum.
- BC-SKL-06013 -> BC-SKL-06015, hard_prerequisite, [inferred], Prerequisite for Express a definite integral as the limit of a Riemann sum.
- BC-PRQ-06006 -> BC-SKL-06016, supporting, [inferred], Prerequisite for State the limit definition of the definite integral.
- BC-TOP-0102 -> BC-SKL-06016, hard_prerequisite, [inferred], Limit of a sequence of sums; Unit 1 limit skills do not exist yet so the topic id stands in; unmapped
- BC-SKL-01006 -> BC-SKL-06014, hard_prerequisite, [inferred], Evaluating a limit is required before a Riemann sum limit can be read as an integral

### Required mathematical knowledge

**Riemann sum as a sum of products.** A Riemann sum requires a partition of an interval and is the sum of products, each the value of the function at a point in a subinterval multiplied by the length of that subinterval (BC-EK-LIM-5B2).

**Definition of the definite integral.** Hypotheses: f continuous on [a,b]. Conclusion: the integral from a to b of f(x) dx is the limit of Riemann sums as the maximum of the subinterval widths approaches 0, that is the limit of the sum from i = 1 to n of f(x sub i star) times delta x sub i (BC-EK-LIM-5C1).

**Notation.** Sigma from i = 1 to n; delta x sub i; x sub i star for the sample point; the integral sign with lower and upper limits and a differential.

### Representations

Representations in play: BC-REP-01 Symbolic (analytical) expression, BC-REP-04 Verbal description.

Conversions tested: symbolic limit of a sum to symbolic definite integral and back (BC-REP-01 to BC-REP-01), which is itself the assessed ability (BC-EK-LIM-5C2).

### Assessment behaviour

MCQ forms give a limit of a sum in sigma notation and ask for the matching definite integral, or the reverse. FRQ use in 2023 to 2025 is indirect, through the definition underlying the approximation parts. Conceptual variants ask what each factor of a term represents; computational variants ask for an expanded sum; justification variants ask why the limit of the sum equals the integral; multi-concept variants pair the conversion with an area interpretation.

### Archetypes

- BC-QA-06014 Converting between a limit of Riemann sums and a definite integral

### Errors and misconceptions

- BC-ERR-06003 Riemann sum reported as a sum of function values

### Diagnostic signals

- No signal is scoped to this topic; the unit level signal list in data/staging/unit-06.signals.json applies.

### Adaptive metadata summary

Skills in this topic carry calculator relevance none. Remediation targets named across the topic: BC-PRQ-06006, BC-SKL-06012, BC-SKL-06013. Every skill record carries the full seven key adaptive block in data/staging/unit-06.skills.json. [inferred]

## 6.4 The Fundamental Theorem of Calculus and Accumulation Functions

### Official mapping

Topic id BC-TOP-0604, CED code 6.4, name The Fundamental Theorem of Calculus and Accumulation Functions, scope shared, CED page 121. [verified] (ced:121)

- BC-LO-FUN-5A (FUN-5.A): Represent accumulation functions using definite integrals.
  - BC-EK-FUN-5A1 (FUN-5.A.1): "The definite integral can be used to define new functions."
  - BC-EK-FUN-5A2 (FUN-5.A.2): "If f is a continuous function on an interval containing a, then d/dx of (the integral from a to x of f(t) dt) = f(x), where x is in the interval."

Suggested practice skills: BC-MPS-1D (Practice skill 1.D). Weighting pointer: [../exam/exam-blueprint.md](../exam/exam-blueprint.md).

### Concept breakdown

- BC-CON-06007 Accumulation function defined by a definite integral: A definite integral with a variable upper limit defines a new function of that limit.
- BC-CON-06008 Fundamental Theorem of Calculus part one: Differentiating an accumulation function returns the integrand evaluated at the upper limit.

- BC-SKL-06017 Write an accumulation function as a definite integral with a variable upper limit: Set up g(x) as the integral from a fixed start to x.
- BC-SKL-06018 Differentiate an accumulation function with a variable upper limit: Apply the Fundamental Theorem of Calculus part one to get g'(x) = f(x).
- BC-SKL-06019 Differentiate an accumulation function whose upper limit is a function of x: Combine the Fundamental Theorem of Calculus part one with the chain rule.
- BC-SKL-06020 Evaluate an accumulation function at a specified input from the graph of the integrand: Find g at a point by measuring signed area from the start value to that point.
- BC-SKL-06021 State the continuity hypothesis of the Fundamental Theorem of Calculus part one: Name what must be true of f before the theorem may be used.

### Prerequisites

- BC-PRQ-06013 -> BC-SKL-06017, supporting, [inferred], Prerequisite for Write an accumulation function as a definite integral with a variable upper limit.
- BC-PRQ-06005 -> BC-SKL-06017, supporting, [inferred], Prerequisite for Write an accumulation function as a definite integral with a variable upper limit.
- BC-PRQ-06013 -> BC-SKL-06018, supporting, [inferred], Prerequisite for Differentiate an accumulation function with a variable upper limit.
- BC-SKL-06017 -> BC-SKL-06018, hard_prerequisite, [inferred], Prerequisite for Differentiate an accumulation function with a variable upper limit.
- BC-PRQ-06005 -> BC-SKL-06019, supporting, [inferred], Prerequisite for Differentiate an accumulation function whose upper limit is a function of x.
- BC-SKL-06018 -> BC-SKL-06019, hard_prerequisite, [inferred], Prerequisite for Differentiate an accumulation function whose upper limit is a function of x.
- BC-PRQ-06007 -> BC-SKL-06020, supporting, [inferred], Prerequisite for Evaluate an accumulation function at a specified input from the graph of the integrand.
- BC-SKL-06028 -> BC-SKL-06020, hard_prerequisite, [inferred], Prerequisite for Evaluate an accumulation function at a specified input from the graph of the integrand.
- BC-TOP-0115 -> BC-SKL-06021, supporting, [inferred], Continuity on an interval is the hypothesis of the Fundamental Theorem of Calculus part one; unmapped
- BC-SKL-03002 -> BC-SKL-06019, hard_prerequisite, [inferred], The chain rule supplies the factor when the upper limit of an accumulation function is a function of x.

### Required mathematical knowledge

**Accumulation function.** For f continuous on an interval containing a, g(x) = the integral from a to x of f(t) dt defines a function on that interval (BC-EK-FUN-5A1).

**Fundamental Theorem of Calculus part one.** Hypotheses: f continuous on an interval containing a, and x in that interval. Conclusion: the derivative with respect to x of the integral from a to x of f(t) dt equals f(x) (BC-EK-FUN-5A2).

**Composite upper limit.** With the chain rule, the derivative of the integral from a to u(x) of f(t) dt equals f(u(x)) times u'(x).

**Notation.** The variable of integration t is a bound variable; the independent variable appears only in the limits.

### Representations

Representations in play: BC-REP-01 Symbolic (analytical) expression, BC-REP-02 Graphical, BC-REP-04 Verbal description, BC-REP-05 Contextual model.

Conversions tested: symbolic accumulation function to its derivative (BC-REP-01), and graph of the integrand to values of the accumulation function (BC-REP-02 to BC-REP-01).

### Assessment behaviour

MCQ forms ask for the derivative of an accumulation function at a point, with the upper limit equal to x or to a function of x. FRQ forms define a function by an integral and ask for its derivative with a reason, sometimes with the integrand supplied only as a table or a graph (sg-24:15, sg-25:16). Calculator status is usually no calculator. Conceptual variants ask what the theorem asserts; computational variants ask for a value; justification variants require the theorem to be named or exhibited; multi-concept variants chain the chain rule onto the theorem.

### Archetypes

- BC-QA-06003 Accumulation function analysed from the graph of the integrand
- BC-QA-06012 Differentiating an accumulation function with a variable upper limit

### Errors and misconceptions

- BC-ERR-06013 Semicircular region given the area of a full circle
- BC-ERR-06014 Regions below the axis added as positive area
- BC-ERR-06027 Chain rule factor omitted when the upper limit is a function of x
- BC-ERR-06028 Variable of integration substituted in place of the upper limit
- BC-MIS-06011 Area formulas are recalled without their fractional factors, severity medium
- BC-MIS-06012 The definite integral measures unsigned area, severity high
- BC-MIS-06023 The Fundamental Theorem of Calculus part one has no chain rule, severity medium
- BC-MIS-06024 The variable of integration is the independent variable, severity medium

### Diagnostic signals

- BC-SIG-06022 Chain rule factor missing from the derivative of an accumulation function

### Adaptive metadata summary

Skills in this topic carry calculator relevance none. Remediation targets named across the topic: BC-CON-06008, BC-PRQ-06013, BC-SKL-06017, BC-SKL-06018, BC-SKL-06028. Every skill record carries the full seven key adaptive block in data/staging/unit-06.skills.json. [inferred]

## 6.5 Interpreting the Behavior of Accumulation Functions Involving Area

### Official mapping

Topic id BC-TOP-0605, CED code 6.5, name Interpreting the Behavior of Accumulation Functions Involving Area, scope shared, CED page 122. [verified] (ced:122)

- BC-LO-FUN-5A (FUN-5.A): Represent accumulation functions using definite integrals.
  - BC-EK-FUN-5A3 (FUN-5.A.3): "Graphical, numerical, analytical, and verbal representations of a function f provide information about the function g defined as g(x) = the integral from a to x of f(t) dt."

Suggested practice skills: BC-MPS-2D (Practice skill 2.D). Weighting pointer: [../exam/exam-blueprint.md](../exam/exam-blueprint.md).

### Concept breakdown

- BC-CON-06009 Behaviour of an accumulation function read from the integrand: The graph of the integrand controls where the accumulation function rises, falls, and bends.

- BC-SKL-06022 Determine where an accumulation function increases or decreases from the sign of the integrand: Read intervals of increase and decrease of g off where f is above or below the axis.
- BC-SKL-06023 Locate relative extrema of an accumulation function from sign changes of the integrand: Find where f crosses the axis and say which way it crosses.
- BC-SKL-06024 Locate points of inflection of an accumulation function from turning points of the integrand: Find where f changes from increasing to decreasing or the reverse.
- BC-SKL-06025 Determine the concavity of an accumulation function from the monotonicity of the integrand: Say where g bends up or down based on whether f rises or falls.
- BC-SKL-06026 Determine an absolute extreme value of an accumulation function with a global argument: Compare candidate values at the critical points and both endpoints.
- BC-SKL-06027 Describe the graph of an accumulation function from the graph of the integrand: Assemble monotonicity, extrema, and concavity into a description of g.

### Prerequisites

- BC-SKL-06018 -> BC-SKL-06022, hard_prerequisite, [inferred], Prerequisite for Determine where an accumulation function increases or decreases from the sign of the integrand.
- BC-SKL-06018 -> BC-SKL-06023, hard_prerequisite, [inferred], Prerequisite for Locate relative extrema of an accumulation function from sign changes of the integrand.
- BC-SKL-06022 -> BC-SKL-06023, hard_prerequisite, [inferred], Prerequisite for Locate relative extrema of an accumulation function from sign changes of the integrand.
- BC-SKL-06018 -> BC-SKL-06024, hard_prerequisite, [inferred], Prerequisite for Locate points of inflection of an accumulation function from turning points of the integrand.
- BC-SKL-06018 -> BC-SKL-06025, hard_prerequisite, [inferred], Prerequisite for Determine the concavity of an accumulation function from the monotonicity of the integrand.
- BC-PRQ-06007 -> BC-SKL-06026, supporting, [inferred], Prerequisite for Determine an absolute extreme value of an accumulation function with a global argument.
- BC-SKL-06020 -> BC-SKL-06026, hard_prerequisite, [inferred], Prerequisite for Determine an absolute extreme value of an accumulation function with a global argument.
- BC-SKL-06023 -> BC-SKL-06026, hard_prerequisite, [inferred], Prerequisite for Determine an absolute extreme value of an accumulation function with a global argument.
- BC-SKL-06022 -> BC-SKL-06027, hard_prerequisite, [inferred], Prerequisite for Describe the graph of an accumulation function from the graph of the integrand.
- BC-SKL-06024 -> BC-SKL-06027, hard_prerequisite, [inferred], Prerequisite for Describe the graph of an accumulation function from the graph of the integrand.
- BC-SKL-06025 -> BC-SKL-06027, hard_prerequisite, [inferred], Prerequisite for Describe the graph of an accumulation function from the graph of the integrand.
- BC-SKL-05021 -> BC-SKL-06023, supporting, [inferred], Relative extremum reasoning from the sign of a derivative is applied to the accumulation function.
- BC-TOP-0506 -> BC-SKL-06025, supporting, [inferred], Concavity from the monotonicity of a derivative is applied to the accumulation function; unmapped
- BC-SKL-05029 -> BC-SKL-06026, supporting, [inferred], The candidates test for an absolute extremum on a closed interval is a Unit 5 procedure.

### Required mathematical knowledge

**Reading g from f.** For g(x) = the integral from a to x of f(t) dt: g' = f, so the sign of f gives the monotonicity of g and sign changes of f give the relative extrema of g; g'' = f', so the monotonicity of f gives the concavity of g and turning points of f give the points of inflection of g (BC-EK-FUN-5A3).

**Absolute extrema.** A global argument on a closed interval compares the values of g at every input where f is zero and at both endpoints.

**Notation.** g, g', g'' alongside f and f'; graphical, numerical, analytical, and verbal representations of f all inform g.

### Representations

Representations in play: BC-REP-02 Graphical.

Conversions tested: graph of the integrand to a described or sketched graph of the accumulation function (BC-REP-02 to BC-REP-02), and graph to a verbal justification (BC-REP-02 to BC-REP-04).

### Assessment behaviour

MCQ forms ask where an accumulation function is increasing, has an extremum, or changes concavity, given the graph of the integrand. FRQ forms devote a whole multipart question to this, asking for values of the accumulation function, its critical points, its inflection points, and an absolute extremum with a global justification (sg-25:15 through sg-25:19, sg-24:12 through sg-24:14). Calculator status is no calculator. Justification variants dominate, and the reason must be tied to the given graph of the integrand (sg-25:17).

### Archetypes

- BC-QA-06003 Accumulation function analysed from the graph of the integrand

### Errors and misconceptions

- BC-ERR-06008 Graph of the integrand treated as the graph of the accumulation function
- BC-ERR-06009 Inflection points of an accumulation function placed where the integrand crosses the axis
- BC-ERR-06010 Reason for a feature of the accumulation function phrased only in terms of g
- BC-ERR-06011 Local argument offered where a global extremum is requested
- BC-ERR-06012 Candidates comparison left incomplete
- BC-MIS-06006 Concavity and monotonicity are the same property, severity high
- BC-MIS-06007 The plotted curve is the function under discussion, severity high
- BC-MIS-06008 A zero of the integrand is a general turning feature of the accumulation function, severity high
- BC-MIS-06009 Restating a definition counts as a reason, severity medium
- BC-MIS-06010 A relative extremum test settles an absolute extremum, severity high

### Diagnostic signals

- BC-SIG-06008 Features of the accumulation function read off the plotted curve
- BC-SIG-06009 Inflection points of the accumulation function placed at zeros of the integrand
- BC-SIG-06010 Correct feature list with a reason phrased only in terms of the accumulation function
- BC-SIG-06011 Correct absolute extremum value with a local justification
- BC-SIG-06012 Candidates table missing an endpoint
- BC-SIG-06024 Complete accumulation function analysis with graph tied reasons

### Adaptive metadata summary

Skills in this topic carry calculator relevance none. Remediation targets named across the topic: BC-SKL-06018, BC-SKL-06020, BC-SKL-06022. Every skill record carries the full seven key adaptive block in data/staging/unit-06.skills.json. [inferred]

## 6.6 Applying Properties of Definite Integrals

### Official mapping

Topic id BC-TOP-0606, CED code 6.6, name Applying Properties of Definite Integrals, scope shared, CED page 123. [verified] (ced:123)

- BC-LO-FUN-6A (FUN-6.A): Calculate a definite integral using areas and properties of definite integrals.
  - BC-EK-FUN-6A1 (FUN-6.A.1): "In some cases, a definite integral can be evaluated by using geometry and the connection between the definite integral and area."
  - BC-EK-FUN-6A2 (FUN-6.A.2): "Properties of definite integrals include the integral of a constant times a function, the integral of the sum of two functions, reversal of limits of integration, and the integral of a function over adjacent intervals."
  - BC-EK-FUN-6A3 (FUN-6.A.3): "The definition of the definite integral may be extended to functions with removable or jump discontinuities."

Suggested practice skills: BC-MPS-3D (Practice skill 3.D). Weighting pointer: [../exam/exam-blueprint.md](../exam/exam-blueprint.md).

### Concept breakdown

- BC-CON-06010 Definite integral evaluated by geometry: When the graph is made of lines and circular arcs the integral is a sum of signed areas.
- BC-CON-06011 Algebraic properties of the definite integral: Constants factor out, sums split, reversing the limits flips the sign, and adjacent intervals add.

- BC-SKL-06028 Evaluate a definite integral from a graph using area formulas: Break the region into triangles, rectangles, and circular pieces and add with signs.
- BC-SKL-06029 Apply the constant multiple and sum properties of definite integrals: Pull constants out front and split an integral of a sum.
- BC-SKL-06030 Apply the reversal of limits property: Swapping the limits changes the sign of the integral.
- BC-SKL-06031 Apply the adjacent interval property of definite integrals: Integrals over touching intervals add to the integral over the union.
- BC-SKL-06032 Evaluate a definite integral over a degenerate interval: An integral from a point to itself is zero.
- BC-SKL-06033 Evaluate a definite integral of a function with a removable or jump discontinuity: Integrate piece by piece and ignore the value at a single point.

### Prerequisites

- BC-PRQ-06007 -> BC-SKL-06028, supporting, [inferred], Prerequisite for Evaluate a definite integral from a graph using area formulas.
- BC-SKL-06031 -> BC-SKL-06033, hard_prerequisite, [inferred], Prerequisite for Evaluate a definite integral of a function with a removable or jump discontinuity.
- BC-TOP-0115 -> BC-SKL-06033, supporting, [inferred], Classifying removable and jump discontinuities comes from Unit 1; unmapped

### Required mathematical knowledge

**Geometry.** In some cases a definite integral can be evaluated using geometry and the connection between the definite integral and area (BC-EK-FUN-6A1). Regions below the axis contribute negatively.

**Properties.** The integral of a constant times a function, the integral of a sum of two functions, reversal of the limits of integration, and the integral of a function over adjacent intervals (BC-EK-FUN-6A2). The integral from a to a of f is 0.

**Discontinuities.** The definition of the definite integral extends to functions with removable or jump discontinuities (BC-EK-FUN-6A3).

**Notation.** The integral from a to b equals the negative of the integral from b to a; the integral from a to c equals the integral from a to b plus the integral from b to c.

### Representations

Representations in play: BC-REP-01 Symbolic (analytical) expression, BC-REP-02 Graphical, BC-REP-03 Numerical table.

Conversions tested: graph to a numerical integral value (BC-REP-02 to BC-REP-01), and tabulated integral values to a new integral value (BC-REP-03 to BC-REP-01).

### Assessment behaviour

MCQ forms supply values of two integrals and ask for a third. FRQ forms use the properties inside other parts, for instance splitting an interval or reversing limits while evaluating an accumulation function from a graph (sg-25:18). Calculator status is no calculator. Conceptual variants ask which property licenses a step; computational variants ask for a value; reversed variants supply a total and one piece and ask for the missing piece.

### Archetypes

- BC-QA-06004 Definite integral evaluated from a graph by geometry
- BC-QA-06013 Manipulating definite integrals with their properties

### Errors and misconceptions

- BC-ERR-06013 Semicircular region given the area of a full circle
- BC-ERR-06014 Regions below the axis added as positive area
- BC-ERR-06031 Integral split at a discontinuity omitted
- BC-MIS-06011 Area formulas are recalled without their fractional factors, severity medium
- BC-MIS-06012 The definite integral measures unsigned area, severity high
- BC-MIS-06026 The Fundamental Theorem of Calculus part two needs no hypotheses, severity medium

### Diagnostic signals

- BC-SIG-06013 Signed integral reported as a plain area
- BC-SIG-06014 Semicircular contribution doubled

### Adaptive metadata summary

Skills in this topic carry calculator relevance none. Remediation targets named across the topic: BC-CON-06011, BC-PRQ-06007, BC-SKL-06031. Every skill record carries the full seven key adaptive block in data/staging/unit-06.skills.json. [inferred]

## 6.7 The Fundamental Theorem of Calculus and Definite Integrals

### Official mapping

Topic id BC-TOP-0607, CED code 6.7, name The Fundamental Theorem of Calculus and Definite Integrals, scope shared, CED page 124. [verified] (ced:124)

- BC-LO-FUN-6B (FUN-6.B): Evaluate definite integrals analytically using the Fundamental Theorem of Calculus.
  - BC-EK-FUN-6B1 (FUN-6.B.1): "An antiderivative of a function f is a function g whose derivative is f."
  - BC-EK-FUN-6B2 (FUN-6.B.2): "If a function f is continuous on an interval containing a, the function defined by F(x) = the integral from a to x of f(t) dt is an antiderivative of f for x in the interval."
  - BC-EK-FUN-6B3 (FUN-6.B.3): "If f is continuous on the interval [a, b] and F is an antiderivative of f, then the integral from a to b of f(x) dx = F(b) - F(a)."

Suggested practice skills: BC-MPS-3D (Practice skill 3.D). Weighting pointer: [../exam/exam-blueprint.md](../exam/exam-blueprint.md).

### Concept breakdown

- BC-CON-06012 Fundamental Theorem of Calculus part two and net change: An antiderivative evaluated at the endpoints gives the exact integral and the net change.
- BC-CON-06013 Average value of a function: The average value divides the accumulated amount by the length of the interval.

- BC-SKL-06034 Evaluate a definite integral by antidifferentiation and endpoint substitution: Find an antiderivative and subtract its value at the lower limit from its value at the upper limit.
- BC-SKL-06035 State the hypotheses and conclusion of the Fundamental Theorem of Calculus part two: Name the continuity and antiderivative conditions before using F(b) minus F(a).
- BC-SKL-06036 Compute net change in a quantity from its rate over an interval: Integrate the rate to get how much the quantity changed.
- BC-SKL-06037 Compute a final value from an initial condition and an accumulated change: Add the integral of the rate to the value you were given at the start.
- BC-SKL-06038 Compute the average value of a function on an interval: Divide the integral by the length of the interval.
- BC-SKL-06039 Set up a single definite integral for a rate in minus rate out situation: Subtract the outflow rate from the inflow rate inside one integral.

### Prerequisites

- BC-PRQ-06002 -> BC-SKL-06034, supporting, [inferred], Prerequisite for Evaluate a definite integral by antidifferentiation and endpoint substitution.
- BC-SKL-06040 -> BC-SKL-06034, hard_prerequisite, [inferred], Prerequisite for Evaluate a definite integral by antidifferentiation and endpoint substitution.
- BC-PRQ-06005 -> BC-SKL-06036, supporting, [inferred], Prerequisite for Compute net change in a quantity from its rate over an interval.
- BC-SKL-06034 -> BC-SKL-06036, hard_prerequisite, [inferred], Prerequisite for Compute net change in a quantity from its rate over an interval.
- BC-PRQ-06005 -> BC-SKL-06037, supporting, [inferred], Prerequisite for Compute a final value from an initial condition and an accumulated change.
- BC-SKL-06036 -> BC-SKL-06037, hard_prerequisite, [inferred], Prerequisite for Compute a final value from an initial condition and an accumulated change.
- BC-SKL-06034 -> BC-SKL-06038, hard_prerequisite, [inferred], Prerequisite for Compute the average value of a function on an interval.
- BC-SKL-06036 -> BC-SKL-06039, hard_prerequisite, [inferred], Prerequisite for Set up a single definite integral for a rate in minus rate out situation.
- BC-TOP-0115 -> BC-SKL-06035, supporting, [inferred], Continuity on the closed interval is a hypothesis of the Fundamental Theorem of Calculus part two; unmapped

### Required mathematical knowledge

**Antiderivative.** An antiderivative of f is a function g whose derivative is f (BC-EK-FUN-6B1).

**Fundamental Theorem of Calculus part one, restated.** Hypotheses: f continuous on an interval containing a. Conclusion: F(x) = the integral from a to x of f(t) dt is an antiderivative of f on that interval (BC-EK-FUN-6B2).

**Fundamental Theorem of Calculus part two.** Hypotheses: f continuous on [a,b] and F an antiderivative of f. Conclusion: the integral from a to b of f(x) dx equals F(b) minus F(a) (BC-EK-FUN-6B3).

**Net change and average value.** The net change in F over [a,b] is the integral of its rate; the average value of f over [a,b] is one over (b minus a) times that integral.

**Notation.** F(b) - F(a), often written with a vertical evaluation bar.

### Representations

Representations in play: BC-REP-01 Symbolic (analytical) expression, BC-REP-03 Numerical table, BC-REP-04 Verbal description, BC-REP-05 Contextual model, BC-REP-09 Calculator-generated numerical result.

Conversions tested: symbolic rate to a contextual amount with units (BC-REP-01 to BC-REP-05), and symbolic integrand to a calculator evaluated value (BC-REP-01 to BC-REP-09).

### Assessment behaviour

MCQ forms ask for a definite integral of a polynomial or basic transcendental integrand. FRQ forms ask for a total amount from a rate model, with points for the integrand, the antiderivative, and the value (sg-25:14), or for a value from an initial condition plus an integral (sg-24:3). Calculator variants evaluate the integral numerically; no-calculator variants require an exact antiderivative. Justification variants ask for the hypotheses of the theorem to be checked.

### Archetypes

- BC-QA-06005 Net change from a rate with an initial condition
- BC-QA-06006 Rate in minus rate out accumulation
- BC-QA-06007 Average value of a function over an interval
- BC-QA-06008 Antiderivative or definite integral by substitution
- BC-QA-06013 Manipulating definite integrals with their properties

### Errors and misconceptions

- BC-ERR-06015 Initial condition omitted from a net change computation
- BC-ERR-06016 Integral reported without the division in an average value
- BC-ERR-06017 Average rate of change computed where the average value is requested
- BC-ERR-06030 Average value expression interpreted as a total
- BC-ERR-06032 Calculator left in degree mode for a trigonometric integrand
- BC-MIS-06013 The integral of a rate is the amount of the quantity, severity high
- BC-MIS-06014 Average value and accumulated amount are the same quantity, severity high
- BC-MIS-06015 Average of a function and average rate of change are the same quantity, severity medium
- BC-MIS-06026 The Fundamental Theorem of Calculus part two needs no hypotheses, severity medium

### Diagnostic signals

- BC-SIG-06015 Accumulated change reported as the final value
- BC-SIG-06016 Integral reported where an average value was requested
- BC-SIG-06017 Difference quotient reported where an average value was requested
- BC-SIG-06023 Complete and correct multi step accumulation response

### Adaptive metadata summary

Skills in this topic carry calculator relevance none, typically_required. Remediation targets named across the topic: BC-CON-06012, BC-SKL-06034, BC-SKL-06036, BC-SKL-06040. Every skill record carries the full seven key adaptive block in data/staging/unit-06.skills.json. [inferred]

## 6.8 Finding Antiderivatives and Indefinite Integrals: Basic Rules and Notation

### Official mapping

Topic id BC-TOP-0608, CED code 6.8, name Finding Antiderivatives and Indefinite Integrals: Basic Rules and Notation, scope shared, CED page 125. [verified] (ced:125)

- BC-LO-FUN-6C (FUN-6.C): Determine antiderivatives of functions and indefinite integrals, using knowledge of derivatives.
  - BC-EK-FUN-6C1 (FUN-6.C.1): "The integral of f(x) dx is an indefinite integral of the function f and can be expressed as the integral of f(x) dx = F(x) + C, where F'(x) = f(x) and C is any constant."
  - BC-EK-FUN-6C2 (FUN-6.C.2): "Differentiation rules provide the foundation for finding antiderivatives."
  - BC-EK-FUN-6C3 (FUN-6.C.3): "Many functions do not have closed-form antiderivatives."

Suggested practice skills: BC-MPS-4C (Practice skill 4.C). Weighting pointer: [../exam/exam-blueprint.md](../exam/exam-blueprint.md).

### Concept breakdown

- BC-CON-06014 Antiderivative and indefinite integral: An indefinite integral names the whole family of functions whose derivative is the integrand.

- BC-SKL-06040 Antidifferentiate power functions including negative and fractional exponents: Raise the exponent by one and divide, after rewriting radicals and reciprocals as powers.
- BC-SKL-06041 Antidifferentiate exponential and reciprocal integrands: Recognise the forms whose antiderivatives are exponentials and natural logarithms.
- BC-SKL-06042 Antidifferentiate basic trigonometric integrands: Read the trigonometric derivative rules backwards.
- BC-SKL-06043 Antidifferentiate integrands whose antiderivatives are inverse trigonometric: Recognise the one over one plus x squared and one over the root of one minus x squared forms.
- BC-SKL-06044 Include the constant of integration and determine it from an initial condition: Write plus C, then solve for it when a value of the antiderivative is given.
- BC-SKL-06045 Verify a proposed antiderivative by differentiating it: Differentiate the candidate and check it returns the integrand.
- BC-SKL-06046 Recognise an integrand with no closed-form antiderivative: Notice when no elementary antiderivative exists and keep the integral form.

Granularity note: Topic 6.8 carries seven skills because the CED groups five independent antiderivative families under one essential knowledge statement (BC-EK-FUN-6C2) and adds the constant of integration and the no closed-form antiderivative statement as separate demands; each family is independently testable in a single question part.

### Prerequisites

- BC-PRQ-06002 -> BC-SKL-06040, supporting, [inferred], Prerequisite for Antidifferentiate power functions including negative and fractional exponents.
- BC-PRQ-06003 -> BC-SKL-06041, supporting, [inferred], Prerequisite for Antidifferentiate exponential and reciprocal integrands.
- BC-PRQ-06004 -> BC-SKL-06042, supporting, [inferred], Prerequisite for Antidifferentiate basic trigonometric integrands.
- BC-PRQ-06004 -> BC-SKL-06043, supporting, [inferred], Prerequisite for Antidifferentiate integrands whose antiderivatives are inverse trigonometric.
- BC-SKL-06040 -> BC-SKL-06044, hard_prerequisite, [inferred], Prerequisite for Include the constant of integration and determine it from an initial condition.
- BC-SKL-02027 -> BC-SKL-06040, hard_prerequisite, [inferred], Antiderivative recognition reverses the power rule from Unit 2.
- BC-SKL-02035 -> BC-SKL-06042, hard_prerequisite, [inferred], Trigonometric derivative rules read backwards give the basic trigonometric antiderivatives
- BC-SKL-03021 -> BC-SKL-06043, supporting, [inferred], Inverse trigonometric derivatives from Unit 3 give the inverse trigonometric antiderivative forms

### Required mathematical knowledge

**Indefinite integral.** The integral of f(x) dx equals F(x) plus C, where F'(x) = f(x) and C is any constant (BC-EK-FUN-6C1).

**Source of the rules.** Differentiation rules provide the foundation for finding antiderivatives (BC-EK-FUN-6C2): the power rule reversed for every real exponent other than negative one, the exponential and natural logarithm forms, the basic trigonometric forms, and the inverse trigonometric forms.

**Limits of the method.** Many functions do not have closed-form antiderivatives (BC-EK-FUN-6C3); the CED names the integral of e to the negative t squared as an illustrative example (ced:121).

**Notation.** The indefinite integral sign, the differential, and the arbitrary constant C.

### Representations

Representations in play: BC-REP-01 Symbolic (analytical) expression.

Conversions tested: symbolic integrand to symbolic antiderivative (BC-REP-01 to BC-REP-01), with verification running in the reverse direction by differentiation.

### Assessment behaviour

MCQ forms ask for an antiderivative of a basic integrand or for the value of the constant of integration from an initial condition. FRQ forms embed basic antidifferentiation inside a larger technique part, where the antiderivative carries its own point (sg-25:14, sg-24:18). Calculator status is no calculator. Conceptual variants ask whether a proposed function is an antiderivative; computational variants ask for the antiderivative; multi-concept variants combine a basic rule with a rearrangement.

### Archetypes

- BC-QA-06016 Selecting an antidifferentiation technique from the form of the integrand

### Errors and misconceptions

- BC-ERR-06021 Constant of integration omitted from an indefinite integral
- BC-MIS-06018 An antiderivative is a single function, severity medium

### Diagnostic signals

- No signal is scoped to this topic; the unit level signal list in data/staging/unit-06.signals.json applies.

### Adaptive metadata summary

Skills in this topic carry calculator relevance none. Remediation targets named across the topic: BC-CON-06014, BC-PRQ-06002, BC-PRQ-06003, BC-PRQ-06004, BC-SKL-06040. Every skill record carries the full seven key adaptive block in data/staging/unit-06.skills.json. [inferred]

## 6.9 Integrating Using Substitution

### Official mapping

Topic id BC-TOP-0609, CED code 6.9, name Integrating Using Substitution, scope shared, CED page 126. [verified] (ced:126)

- BC-LO-FUN-6D (FUN-6.D): For integrands requiring substitution or rearrangements into equivalent forms: (a) Determine indefinite integrals. (b) Evaluate definite integrals.
  - BC-EK-FUN-6D1 (FUN-6.D.1): "Substitution of variables is a technique for finding antiderivatives."
  - BC-EK-FUN-6D2 (FUN-6.D.2): "For a definite integral, substitution of variables requires corresponding changes to the limits of integration."
  - BC-EK-FUN-6D3 (FUN-6.D.3): "Techniques for finding antiderivatives include rearrangements into equivalent forms, such as long division and completing the square."

Suggested practice skills: BC-MPS-1E (Practice skill 1.E). Weighting pointer: [../exam/exam-blueprint.md](../exam/exam-blueprint.md).

### Concept breakdown

- BC-CON-06015 Substitution of variables: Naming an inner expression u converts a composite integrand into a basic form.

- BC-SKL-06047 Select a substitution by identifying an inner function whose derivative appears: Pick u as the inside expression whose derivative is a factor of the integrand.
- BC-SKL-06048 Convert the differential and adjust the constant when substituting: Write du = g'(x) dx and balance any constant factor.
- BC-SKL-06049 Back-substitute to express an indefinite integral in the original variable: Replace u by the original expression at the end.
- BC-SKL-06050 Change the limits of integration when substituting in a definite integral: Replace the x limits by the matching u limits.
- BC-SKL-06051 Evaluate a definite integral by substitution with back-substitution before the limits are used: Keep the original limits only if you convert back to x first.
- BC-SKL-06052 Apply substitution to an integrand that antidifferentiates to a logarithm: Recognise the derivative over the function pattern.

### Prerequisites

- BC-PRQ-06001 -> BC-SKL-06047, supporting, [inferred], Prerequisite for Select a substitution by identifying an inner function whose derivative appears.
- BC-PRQ-06001 -> BC-SKL-06048, supporting, [inferred], Prerequisite for Convert the differential and adjust the constant when substituting.
- BC-SKL-06047 -> BC-SKL-06048, hard_prerequisite, [inferred], Prerequisite for Convert the differential and adjust the constant when substituting.
- BC-SKL-06048 -> BC-SKL-06049, hard_prerequisite, [inferred], Prerequisite for Back-substitute to express an indefinite integral in the original variable.
- BC-SKL-06048 -> BC-SKL-06050, hard_prerequisite, [inferred], Prerequisite for Change the limits of integration when substituting in a definite integral.
- BC-SKL-06049 -> BC-SKL-06051, hard_prerequisite, [inferred], Prerequisite for Evaluate a definite integral by substitution with back-substitution before the limits are used.
- BC-SKL-06050 -> BC-SKL-06051, hard_prerequisite, [inferred], Prerequisite for Evaluate a definite integral by substitution with back-substitution before the limits are used.
- BC-PRQ-06003 -> BC-SKL-06052, supporting, [inferred], Prerequisite for Apply substitution to an integrand that antidifferentiates to a logarithm.
- BC-SKL-06047 -> BC-SKL-06052, hard_prerequisite, [inferred], Prerequisite for Apply substitution to an integrand that antidifferentiates to a logarithm.
- BC-SKL-06048 -> BC-SKL-06052, hard_prerequisite, [inferred], Prerequisite for Apply substitution to an integrand that antidifferentiates to a logarithm.
- BC-SKL-03002 -> BC-SKL-06047, hard_prerequisite, [inferred], Substitution reverses the chain rule, so recognising a composite and its inner derivative comes first.

### Required mathematical knowledge

**Substitution.** Substitution of variables is a technique for finding antiderivatives (BC-EK-FUN-6D1). If u = g(x) and du = g'(x) dx, then the integral of f(g(x)) g'(x) dx equals the integral of f(u) du.

**Definite integrals.** For a definite integral, substitution of variables requires corresponding changes to the limits of integration (BC-EK-FUN-6D2); the alternative is to back-substitute before applying the original limits.

**Notation.** u, du, and converted limits g(a) and g(b); the natural logarithm of an absolute value for the derivative over function pattern.

### Representations

Representations in play: BC-REP-01 Symbolic (analytical) expression.

Conversions tested: symbolic integrand in x to an equivalent integral in u and back (BC-REP-01 to BC-REP-01), including the conversion of the limits of integration.

### Assessment behaviour

MCQ forms ask for an indefinite integral requiring a single substitution, or for a definite integral where the limits must be converted. FRQ forms embed substitution inside area and improper integral parts, where using the original limits on an expression written in the substituted variable forfeits the value point (sg-23:16, sg-23:17). Calculator status is no calculator. Justification variants ask for the substitution to be declared explicitly.

### Archetypes

- BC-QA-06008 Antiderivative or definite integral by substitution

### Errors and misconceptions

- BC-ERR-06018 Original limits of integration kept after a substitution
- BC-ERR-06019 Constant factor from the differential dropped
- BC-ERR-06020 Substitution attempted when the inner derivative is absent
- BC-ERR-06021 Constant of integration omitted from an indefinite integral
- BC-MIS-06016 Substitution renames a variable without changing the problem, severity high
- BC-MIS-06017 A composite integrand guarantees that substitution applies, severity high

### Diagnostic signals

- BC-SIG-06018 Original limits substituted into an expression written in the substituted variable
- BC-SIG-06019 Answer differs from the correct antiderivative by a constant factor

### Adaptive metadata summary

Skills in this topic carry calculator relevance none. Remediation targets named across the topic: BC-PRQ-06001, BC-SKL-06047, BC-SKL-06048, BC-SKL-06049. Every skill record carries the full seven key adaptive block in data/staging/unit-06.skills.json. [inferred]

## 6.10 Integrating Functions Using Long Division and Completing the Square

### Official mapping

Topic id BC-TOP-0610, CED code 6.10, name Integrating Functions Using Long Division and Completing the Square, scope shared, CED page 127. [verified] (ced:127)

- BC-LO-FUN-6D (FUN-6.D): For integrands requiring substitution or rearrangements into equivalent forms: (a) Determine indefinite integrals. (b) Evaluate definite integrals.
  - BC-EK-FUN-6D1 (FUN-6.D.1): "Substitution of variables is a technique for finding antiderivatives."
  - BC-EK-FUN-6D2 (FUN-6.D.2): "For a definite integral, substitution of variables requires corresponding changes to the limits of integration."
  - BC-EK-FUN-6D3 (FUN-6.D.3): "Techniques for finding antiderivatives include rearrangements into equivalent forms, such as long division and completing the square."

Suggested practice skills: BC-MPS-1E (Practice skill 1.E). Weighting pointer: [../exam/exam-blueprint.md](../exam/exam-blueprint.md).

### Concept breakdown

- BC-CON-06016 Rearrangement into an equivalent integrable form: Long division and completing the square turn an unworkable integrand into a standard one.

- BC-SKL-06053 Rewrite an improper rational integrand by polynomial long division: Divide first so the remainder term is proper.
- BC-SKL-06054 Complete the square in a quadratic denominator to reach a standard form: Rewrite the quadratic as a square plus a constant to expose an inverse trigonometric or logarithmic form.
- BC-SKL-06055 Rewrite an integrand by splitting or expanding before antidifferentiating: Break a single fraction into separate terms or multiply out a product first.
- BC-SKL-06056 Decide between rearrangement and substitution for a rational integrand: Check the degrees and the denominator structure before choosing.

### Prerequisites

- BC-PRQ-06009 -> BC-SKL-06053, supporting, [inferred], Prerequisite for Rewrite an improper rational integrand by polynomial long division.
- BC-PRQ-06010 -> BC-SKL-06054, supporting, [inferred], Prerequisite for Complete the square in a quadratic denominator to reach a standard form.
- BC-SKL-06043 -> BC-SKL-06054, hard_prerequisite, [inferred], Prerequisite for Complete the square in a quadratic denominator to reach a standard form.
- BC-SKL-06047 -> BC-SKL-06054, hard_prerequisite, [inferred], Prerequisite for Complete the square in a quadratic denominator to reach a standard form.
- BC-PRQ-06001 -> BC-SKL-06055, supporting, [inferred], Prerequisite for Rewrite an integrand by splitting or expanding before antidifferentiating.
- BC-PRQ-06002 -> BC-SKL-06055, supporting, [inferred], Prerequisite for Rewrite an integrand by splitting or expanding before antidifferentiating.
- BC-SKL-06040 -> BC-SKL-06055, hard_prerequisite, [inferred], Prerequisite for Rewrite an integrand by splitting or expanding before antidifferentiating.
- BC-PRQ-06009 -> BC-SKL-06056, supporting, [inferred], Prerequisite for Decide between rearrangement and substitution for a rational integrand.
- BC-PRQ-06010 -> BC-SKL-06056, supporting, [inferred], Prerequisite for Decide between rearrangement and substitution for a rational integrand.
- BC-SKL-06047 -> BC-SKL-06056, hard_prerequisite, [inferred], Prerequisite for Decide between rearrangement and substitution for a rational integrand.
- BC-SKL-06053 -> BC-SKL-06056, hard_prerequisite, [inferred], Prerequisite for Decide between rearrangement and substitution for a rational integrand.
- BC-SKL-06054 -> BC-SKL-06056, hard_prerequisite, [inferred], Prerequisite for Decide between rearrangement and substitution for a rational integrand.

### Required mathematical knowledge

**Rearrangement.** Techniques for finding antiderivatives include rearrangements into equivalent forms, such as long division and completing the square (BC-EK-FUN-6D3).

**Long division.** Applied when the numerator degree is at least the denominator degree, producing a polynomial plus a proper remainder term.

**Completing the square.** Applied to a quadratic denominator to reach a standard logarithmic or inverse trigonometric antiderivative form.

**Notation.** Quotient plus remainder over divisor; a perfect square plus or minus a constant.

### Representations

Representations in play: BC-REP-01 Symbolic (analytical) expression.

Conversions tested: symbolic integrand to an algebraically equivalent integrand (BC-REP-01 to BC-REP-01).

### Assessment behaviour

MCQ forms present an improper rational integrand or a quadratic denominator and ask for the antiderivative. FRQ use in 2023 to 2025 is indirect. Calculator status is no calculator. Conceptual variants ask which rearrangement applies; computational variants ask for the antiderivative; multi-concept variants combine the rearrangement with a substitution.

### Archetypes

- BC-QA-06016 Selecting an antidifferentiation technique from the form of the integrand

### Errors and misconceptions

- BC-ERR-06026 Improper rational integrand decomposed without a preliminary division
- BC-MIS-06022 Technique choice follows the surface look of the integrand, severity high

### Diagnostic signals

- No signal is scoped to this topic; the unit level signal list in data/staging/unit-06.signals.json applies.

### Adaptive metadata summary

Skills in this topic carry calculator relevance none. Remediation targets named across the topic: BC-PRQ-06009, BC-SKL-06040, BC-SKL-06043, BC-SKL-06047. Every skill record carries the full seven key adaptive block in data/staging/unit-06.skills.json. [inferred]

## 6.11 Integrating Using Integration by Parts

### Official mapping

Topic id BC-TOP-0611, CED code 6.11, name Integrating Using Integration by Parts, scope BC_only, CED page 128. [verified] (ced:128)

- BC-LO-FUN-6E (FUN-6.E): For integrands requiring integration by parts: (a) Determine indefinite integrals. (b) Evaluate definite integrals.
  - BC-EK-FUN-6E1 (FUN-6.E.1): "Integration by parts is a technique for finding antiderivatives."

Suggested practice skills: BC-MPS-1E (Practice skill 1.E). Weighting pointer: [../exam/exam-blueprint.md](../exam/exam-blueprint.md).

### Concept breakdown

- BC-CON-06017 Integration by parts: Parts trades one integral for a simpler one using the product rule in reverse.

- BC-SKL-06057 Choose u and dv for an integration by parts: Assign one factor to differentiate and the other to antidifferentiate.
- BC-SKL-06058 Apply the integration by parts formula: Write uv minus the integral of v du and finish the remaining integral.
- BC-SKL-06059 Apply integration by parts more than once: Repeat the process when the new integral is still a product.
- BC-SKL-06060 Evaluate a definite integral using integration by parts: Evaluate the uv boundary term at both limits and subtract the remaining integral.
- BC-SKL-06061 Apply integration by parts to an integrand containing an unknown function and its derivative: Use parts when the integrand is x times f'(x) and only values of f are supplied.

### Prerequisites

- BC-SKL-06040 -> BC-SKL-06057, hard_prerequisite, [inferred], Prerequisite for Choose u and dv for an integration by parts.
- BC-SKL-06042 -> BC-SKL-06057, hard_prerequisite, [inferred], Prerequisite for Choose u and dv for an integration by parts.
- BC-SKL-06057 -> BC-SKL-06058, hard_prerequisite, [inferred], Prerequisite for Apply the integration by parts formula.
- BC-SKL-06058 -> BC-SKL-06059, hard_prerequisite, [inferred], Prerequisite for Apply integration by parts more than once.
- BC-SKL-06058 -> BC-SKL-06060, hard_prerequisite, [inferred], Prerequisite for Evaluate a definite integral using integration by parts.
- BC-SKL-06034 -> BC-SKL-06060, hard_prerequisite, [inferred], Prerequisite for Evaluate a definite integral using integration by parts.
- BC-PRQ-06005 -> BC-SKL-06061, supporting, [inferred], Prerequisite for Apply integration by parts to an integrand containing an unknown function and its derivative.
- BC-SKL-06058 -> BC-SKL-06061, hard_prerequisite, [inferred], Prerequisite for Apply integration by parts to an integrand containing an unknown function and its derivative.
- BC-TOP-0208 -> BC-SKL-06057, hard_prerequisite, [inferred], Integration by parts is the product rule read as an antidifferentiation technique; unmapped

### Required mathematical knowledge

**Integration by parts.** Integration by parts is a technique for finding antiderivatives (BC-EK-FUN-6E1). The integral of u dv equals u times v minus the integral of v du, which is the product rule for derivatives read as an antidifferentiation technique.

**Definite form.** The boundary term u times v is evaluated at both limits and the remaining definite integral is subtracted.

**Notation.** u, dv, du, v; a tabular arrangement is an accepted presentation (sg-23:18).

### Representations

Representations in play: BC-REP-01 Symbolic (analytical) expression, BC-REP-04 Verbal description.

Conversions tested: symbolic product integrand to the uv minus the integral of v du form (BC-REP-01 to BC-REP-01), and supplied values of an unknown function to a numerical result (BC-REP-04 to BC-REP-01).

### Assessment behaviour

MCQ forms ask for an antiderivative of a product of unlike factors. FRQ forms ask for an indefinite integral requiring parts (sg-24:18) or for a definite integral of x times the derivative of an unknown function whose values are supplied (sg-23:18). Calculator status is no calculator. The choice of u and dv is scored separately from the resulting expression and from the value.

### Archetypes

- BC-QA-06009 Antiderivative by integration by parts

### Errors and misconceptions

- BC-ERR-06022 Factors of a product antidifferentiated separately
- BC-ERR-06023 Minus sign dropped in the integration by parts expression
- BC-MIS-06019 Antidifferentiation distributes across a product, severity high

### Diagnostic signals

- BC-SIG-06020 Product antidifferentiated factor by factor

### Adaptive metadata summary

Skills in this topic carry calculator relevance none. Remediation targets named across the topic: BC-SKL-06040, BC-SKL-06057, BC-SKL-06058. Every skill record carries the full seven key adaptive block in data/staging/unit-06.skills.json. [inferred]

## 6.12 Integrating Using Linear Partial Fractions

### Official mapping

Topic id BC-TOP-0612, CED code 6.12, name Integrating Using Linear Partial Fractions, scope BC_only, CED page 129. [verified] (ced:129)

- BC-LO-FUN-6F (FUN-6.F): For integrands requiring integration by linear partial fractions: (a) Determine indefinite integrals. (b) Evaluate definite integrals.
  - BC-EK-FUN-6F1 (FUN-6.F.1): "Some rational functions can be decomposed into sums of ratios of linear, nonrepeating factors to which basic integration techniques can be applied."

Suggested practice skills: BC-MPS-1E (Practice skill 1.E). Weighting pointer: [../exam/exam-blueprint.md](../exam/exam-blueprint.md).

### Concept breakdown

- BC-CON-06018 Linear partial fraction decomposition: A rational function with distinct linear factors splits into simple fractions that integrate to logarithms.

- BC-SKL-06062 Factor a denominator into distinct linear factors: Factor the quadratic or higher denominator before decomposing.
- BC-SKL-06063 Solve for the constants in a linear partial fraction decomposition: Clear denominators and solve for the numerators.
- BC-SKL-06064 Antidifferentiate a linear partial fraction decomposition: Each simple fraction becomes a constant times a natural logarithm.
- BC-SKL-06065 Evaluate a definite integral of a rational function by partial fractions: Decompose, antidifferentiate, then substitute the limits.

### Prerequisites

- BC-PRQ-06011 -> BC-SKL-06063, supporting, [inferred], Prerequisite for Solve for the constants in a linear partial fraction decomposition.
- BC-SKL-06062 -> BC-SKL-06063, hard_prerequisite, [inferred], Prerequisite for Solve for the constants in a linear partial fraction decomposition.
- BC-PRQ-06003 -> BC-SKL-06064, supporting, [inferred], Prerequisite for Antidifferentiate a linear partial fraction decomposition.
- BC-SKL-06063 -> BC-SKL-06064, hard_prerequisite, [inferred], Prerequisite for Antidifferentiate a linear partial fraction decomposition.
- BC-SKL-06052 -> BC-SKL-06064, hard_prerequisite, [inferred], Prerequisite for Antidifferentiate a linear partial fraction decomposition.
- BC-PRQ-06003 -> BC-SKL-06065, supporting, [inferred], Prerequisite for Evaluate a definite integral of a rational function by partial fractions.
- BC-SKL-06064 -> BC-SKL-06065, hard_prerequisite, [inferred], Prerequisite for Evaluate a definite integral of a rational function by partial fractions.
- BC-SKL-06034 -> BC-SKL-06065, hard_prerequisite, [inferred], Prerequisite for Evaluate a definite integral of a rational function by partial fractions.

### Required mathematical knowledge

**Decomposition.** Some rational functions can be decomposed into sums of ratios of linear, nonrepeating factors to which basic integration techniques can be applied (BC-EK-FUN-6F1).

**Procedure.** Factor the denominator into distinct linear factors, write the decomposition with unknown constant numerators, clear denominators, solve for the constants, and antidifferentiate each term into a constant times the natural logarithm of an absolute value.

**Notation.** A over (x minus r) plus B over (x minus s).

### Representations

Representations in play: BC-REP-01 Symbolic (analytical) expression.

Conversions tested: symbolic rational integrand to a sum of simple fractions (BC-REP-01 to BC-REP-01).

### Assessment behaviour

MCQ forms ask for the decomposition or for the resulting logarithmic antiderivative. No Unit 6 partial fraction part appears in the 2023 to 2025 free response questions read for this unit; the technique surfaces there through the logistic differential equation of Unit 7. Calculator status is no calculator. Conceptual variants ask whether a decomposition is available; computational variants ask for the constants or for the antiderivative.

### Archetypes

- BC-QA-06010 Antiderivative by linear partial fractions

### Errors and misconceptions

- BC-ERR-06026 Improper rational integrand decomposed without a preliminary division

### Diagnostic signals

- No signal is scoped to this topic; the unit level signal list in data/staging/unit-06.signals.json applies.

### Adaptive metadata summary

Skills in this topic carry calculator relevance none. Remediation targets named across the topic: BC-CON-06018, BC-SKL-06062, BC-SKL-06063, BC-SKL-06064. Every skill record carries the full seven key adaptive block in data/staging/unit-06.skills.json. [inferred]

## 6.13 Evaluating Improper Integrals

### Official mapping

Topic id BC-TOP-0613, CED code 6.13, name Evaluating Improper Integrals, scope BC_only, CED page 130. [verified] (ced:130)

- BC-LO-LIM-6A (LIM-6.A): Evaluate an improper integral or determine that the integral diverges.
  - BC-EK-LIM-6A1 (LIM-6.A.1): "An improper integral is an integral that has one or both limits infinite or has an integrand that is unbounded in the interval of integration."
  - BC-EK-LIM-6A2 (LIM-6.A.2): "Improper integrals can be determined using limits of definite integrals."

Suggested practice skills: BC-MPS-1E (Practice skill 1.E). Weighting pointer: [../exam/exam-blueprint.md](../exam/exam-blueprint.md).

### Concept breakdown

- BC-CON-06019 Improper integral and convergence: An integral with an infinite limit or an unbounded integrand is defined as a limit of ordinary integrals.

- BC-SKL-06066 Classify an integral as improper and name the cause: Say whether the limit is infinite or the integrand is unbounded.
- BC-SKL-06067 Rewrite an improper integral as a limit of definite integrals: Replace the offending limit by a variable and take a limit.
- BC-SKL-06068 Evaluate the limit to determine the value of a convergent improper integral: Antidifferentiate, substitute, then take the limit.
- BC-SKL-06069 Conclude that an improper integral diverges: Say the integral diverges when the limit is infinite or fails to exist.
- BC-SKL-06070 Split an improper integral that is improper at more than one place: Break the interval so each piece has a single source of impropriety.

### Prerequisites

- BC-SKL-06066 -> BC-SKL-06067, hard_prerequisite, [inferred], Prerequisite for Rewrite an improper integral as a limit of definite integrals.
- BC-SKL-06067 -> BC-SKL-06068, hard_prerequisite, [inferred], Prerequisite for Evaluate the limit to determine the value of a convergent improper integral.
- BC-SKL-06034 -> BC-SKL-06068, hard_prerequisite, [inferred], Prerequisite for Evaluate the limit to determine the value of a convergent improper integral.
- BC-SKL-06067 -> BC-SKL-06069, hard_prerequisite, [inferred], Prerequisite for Conclude that an improper integral diverges.
- BC-SKL-06066 -> BC-SKL-06070, hard_prerequisite, [inferred], Prerequisite for Split an improper integral that is improper at more than one place.
- BC-SKL-06031 -> BC-SKL-06070, hard_prerequisite, [inferred], Prerequisite for Split an improper integral that is improper at more than one place.
- BC-TOP-0102 -> BC-SKL-06067, hard_prerequisite, [inferred], Improper integrals are defined by limits, including limits at infinity; unmapped

### Required mathematical knowledge

**Definition.** An improper integral is an integral that has one or both limits infinite or has an integrand that is unbounded in the interval of integration (BC-EK-LIM-6A1).

**Evaluation.** Improper integrals can be determined using limits of definite integrals (BC-EK-LIM-6A2). The integral converges when the limit exists and diverges otherwise.

**Notation.** The limit as b approaches infinity of the integral from a to b; limit notation must be carried through the whole computation and arithmetic with infinity is not accepted (sg-23:17).

### Representations

Representations in play: BC-REP-01 Symbolic (analytical) expression.

Conversions tested: symbolic improper integral to a limit of definite integrals (BC-REP-01 to BC-REP-01), and unbounded graph to a finite value statement (BC-REP-02 to BC-REP-01).

### Assessment behaviour

MCQ forms ask whether an improper integral converges and, if so, for its value. FRQ forms ask for the value of an improper integral or for a demonstration that it diverges, with a point reserved for correct limit notation throughout (sg-23:17). Calculator status is no calculator. Justification variants require the conclusion to be stated as convergence or divergence rather than as a bare number.

### Archetypes

- BC-QA-06011 Improper integral convergence or divergence

### Errors and misconceptions

- BC-ERR-06024 Arithmetic with infinity written in place of a limit
- BC-ERR-06025 Value reported for a divergent improper integral
- BC-MIS-06020 Infinity is a number that can be substituted, severity high
- BC-MIS-06021 Every improper integral of a decaying integrand converges, severity medium

### Diagnostic signals

- BC-SIG-06021 Improper integral evaluated by substituting infinity

### Adaptive metadata summary

Skills in this topic carry calculator relevance none. Remediation targets named across the topic: BC-CON-06019, BC-SKL-06066, BC-SKL-06067. Every skill record carries the full seven key adaptive block in data/staging/unit-06.skills.json. [inferred]

## 6.14 Selecting Techniques for Antidifferentiation

### Official mapping

Topic id BC-TOP-0614, CED code 6.14, name Selecting Techniques for Antidifferentiation, scope shared, CED page 131. [verified] (ced:131)

- No learning objective is listed for this topic in data/curriculum.json; the CED describes it as a skill focused topic drawing on the antidifferentiation learning objectives of the unit (ced:131).

Suggested practice skills: BC-MPS-1C (Practice skill 1.C). Weighting pointer: [../exam/exam-blueprint.md](../exam/exam-blueprint.md).

### Concept breakdown

- BC-CON-06020 Selecting an antidifferentiation technique: The structure of the integrand decides which technique applies.

- BC-SKL-06071 Classify an integrand to select an antidifferentiation technique: Look at the structure and name the procedure it calls for.
- BC-SKL-06072 Rule out a technique whose structural precondition is absent: Explain why a technique does not apply to a given integrand.
- BC-SKL-06073 Chain two antidifferentiation techniques in one problem: Apply one technique, then a second to what remains.
- BC-SKL-06074 Recognise when no elementary technique applies and use an integral or numerical representation: Leave the answer as a definite integral or approximate it when no antiderivative is available.

### Prerequisites

- BC-PRQ-06001 -> BC-SKL-06071, supporting, [inferred], Prerequisite for Classify an integrand to select an antidifferentiation technique.
- BC-SKL-06047 -> BC-SKL-06071, hard_prerequisite, [inferred], Prerequisite for Classify an integrand to select an antidifferentiation technique.
- BC-SKL-06053 -> BC-SKL-06071, hard_prerequisite, [inferred], Prerequisite for Classify an integrand to select an antidifferentiation technique.
- BC-SKL-06057 -> BC-SKL-06071, hard_prerequisite, [inferred], Prerequisite for Classify an integrand to select an antidifferentiation technique.
- BC-SKL-06062 -> BC-SKL-06071, hard_prerequisite, [inferred], Prerequisite for Classify an integrand to select an antidifferentiation technique.
- BC-SKL-06066 -> BC-SKL-06071, hard_prerequisite, [inferred], Prerequisite for Classify an integrand to select an antidifferentiation technique.
- BC-SKL-06071 -> BC-SKL-06072, hard_prerequisite, [inferred], Prerequisite for Rule out a technique whose structural precondition is absent.
- BC-SKL-06071 -> BC-SKL-06073, hard_prerequisite, [inferred], Prerequisite for Chain two antidifferentiation techniques in one problem.
- BC-SKL-06058 -> BC-SKL-06073, hard_prerequisite, [inferred], Prerequisite for Chain two antidifferentiation techniques in one problem.
- BC-SKL-06064 -> BC-SKL-06073, hard_prerequisite, [inferred], Prerequisite for Chain two antidifferentiation techniques in one problem.
- BC-SKL-06046 -> BC-SKL-06074, hard_prerequisite, [inferred], Prerequisite for Recognise when no elementary technique applies and use an integral or numerical representation.
- BC-SKL-06071 -> BC-SKL-06074, hard_prerequisite, [inferred], Prerequisite for Recognise when no elementary technique applies and use an integral or numerical representation.

### Required mathematical knowledge

**Selection.** This topic is framed by the CED as the skill of selecting an appropriate procedure for antidifferentiation, drawing on all the antidifferentiation learning objectives of the unit (ced:131).

**Structural markers.** A composite with its inner derivative present selects substitution; a product of unlike factors selects integration by parts; a numerator degree at least the denominator degree selects long division; a factorable nonrepeating linear denominator selects partial fractions; an infinite limit or an unbounded integrand selects the improper integral treatment; an integrand with no closed-form antiderivative selects a definite integral or numerical representation.

**Notation.** No new notation; the notation of the selected technique applies.

### Representations

Representations in play: BC-REP-01 Symbolic (analytical) expression, BC-REP-09 Calculator-generated numerical result.

Conversions tested: symbolic integrand to a named technique (BC-REP-01 to BC-REP-04), and, when no antiderivative exists, symbolic integrand to a numerical result (BC-REP-01 to BC-REP-09).

### Assessment behaviour

MCQ forms present several integrands and ask which technique applies, or ask for an antiderivative whose technique is not signalled. FRQ forms present an unsignalled integrand and score the technique setup and the antiderivative separately (sg-24:18). Calculator status is no calculator. Conceptual variants ask for the technique to be named and the precondition stated; multi-concept variants require two techniques chained.

### Archetypes

- BC-QA-06016 Selecting an antidifferentiation technique from the form of the integrand

### Errors and misconceptions

- BC-ERR-06020 Substitution attempted when the inner derivative is absent
- BC-ERR-06022 Factors of a product antidifferentiated separately
- BC-MIS-06017 A composite integrand guarantees that substitution applies, severity high
- BC-MIS-06022 Technique choice follows the surface look of the integrand, severity high

### Diagnostic signals

- No signal is scoped to this topic; the unit level signal list in data/staging/unit-06.signals.json applies.

### Adaptive metadata summary

Skills in this topic carry calculator relevance none, typically_required. Remediation targets named across the topic: BC-SKL-06046, BC-SKL-06047, BC-SKL-06071. Every skill record carries the full seven key adaptive block in data/staging/unit-06.skills.json. [inferred]

## Cross-unit connections

Cross-unit edges use BC-TOP ids as the node on the other unit's side, because no skills exist in data/skills.json for those units yet; the `notes` field on each edge in data/staging/unit-06.edges.csv describes the skill that the topic id stands in for. [inferred]

### What Unit 6 depends on

**Unit 1 limits.** BC-SKL-06016 (stating the limit definition of the definite integral) and BC-SKL-06014 (reading a limit of Riemann sums as a definite integral) rest on the Unit 1 ability to evaluate a limit, recorded as edges from BC-TOP-0102. BC-SKL-06067 (rewriting an improper integral as a limit of definite integrals) rests on the same ability together with limits at infinity. BC-SKL-06021 and BC-SKL-06035 (the continuity hypotheses of the two parts of the Fundamental Theorem of Calculus) and BC-SKL-06033 (integrating across a removable or jump discontinuity) draw on continuity and discontinuity classification, recorded as edges from BC-TOP-0115.

**Unit 2 and Unit 3 derivatives.** Antiderivative recognition is the derivative rules read backwards, as BC-EK-FUN-6C2 states. BC-SKL-06040 depends on the power rule (BC-TOP-0205), BC-SKL-06042 on the derivatives of the basic transcendental functions (BC-TOP-0207), BC-SKL-06043 on inverse trigonometric derivatives (BC-TOP-0304), and BC-SKL-06057 on the product rule (BC-TOP-0208), since integration by parts is the product rule read as an antidifferentiation technique. BC-SKL-06019, the Fundamental Theorem of Calculus part one with a composite upper limit, depends on the chain rule (BC-TOP-0301), as does BC-SKL-06047, since substitution reverses the chain rule. BC-SKL-06023, BC-SKL-06025, and BC-SKL-06026 apply the Unit 5 first derivative test, concavity test, and candidates test to the accumulation function (BC-TOP-0504, BC-TOP-0506, BC-TOP-0505).

### What depends on Unit 6

**Unit 7.** Separation of variables integrates both sides, so BC-TOP-0706 depends on BC-SKL-06034 and BC-SKL-06047, and BC-TOP-0707 depends on BC-SKL-06044 because a particular solution is fixed by determining the constant of integration from an initial condition. The logistic model at BC-TOP-0709 depends on BC-SKL-06064, the linear partial fraction antiderivative.

**Unit 8.** Every application is an integral. BC-TOP-0801 depends on BC-SKL-06036 and the average value skill BC-SKL-06038; BC-TOP-0802 depends on BC-SKL-06037; BC-TOP-0804 depends on BC-SKL-06028; BC-TOP-0807 and BC-TOP-0813 depend on BC-SKL-06034.

**Unit 9.** Arc length of a parametric curve at BC-TOP-0903 depends on BC-SKL-06034, and the area bounded by a polar curve at BC-TOP-0908 depends on BC-SKL-06028 and the same evaluation skill.

**Unit 10.** Representing a function as a power series by term by term integration at BC-TOP-1015 depends on BC-SKL-06047 and the basic antiderivative skills, and the integral test at BC-TOP-1004 depends on BC-SKL-06067.

## Archetype summary

Sixteen archetypes with forty eight variants are recorded in data/staging/unit-06.archetypes.json. Variant dimensions used are representation, reasoning direction, notation, context, and calculator. [verified] (sg-23:2, sg-23:17, sg-23:18, sg-24:15, sg-24:18, sg-25:13, sg-25:17, sg-25:19)

| Archetype | Name | Scope | Calculator | Official parts read |
|---|---|---|---|---|
| BC-QA-06001 | Riemann sum from a table with over or under estimate reasoning | shared | calculator | 2023 Q1(a), 2024 Q1(b) |
| BC-QA-06002 | Trapezoidal approximation of an accumulated amount from a table | shared | no_calculator | 2025 Q3(C) |
| BC-QA-06003 | Accumulation function analysed from the graph of the integrand | shared | no_calculator | 2025 Q4(A), 2025 Q4(B), 2025 Q4(C), 2025 Q4(D), 2024 Q4(a), 2024 Q4(b) |
| BC-QA-06004 | Definite integral evaluated from a graph by geometry | shared | no_calculator | 2025 Q4(C), 2024 Q4(a) |
| BC-QA-06005 | Net change from a rate with an initial condition | shared | either | 2024 Q1(c), 2025 Q3(D) |
| BC-QA-06006 | Rate in minus rate out accumulation | shared | calculator | 2024 Q1(c) |
| BC-QA-06007 | Average value of a function over an interval | shared | calculator | 2023 Q1(c), 2025 Q1(A), 2024 Q1(b) |
| BC-QA-06008 | Antiderivative or definite integral by substitution | shared | no_calculator | 2023 Q5(a), 2023 Q5(b) |
| BC-QA-06009 | Antiderivative by integration by parts | BC_only | no_calculator | 2023 Q5(c), 2024 Q5(d) |
| BC-QA-06010 | Antiderivative by linear partial fractions | BC_only | no_calculator | none in 2023 to 2025 |
| BC-QA-06011 | Improper integral convergence or divergence | BC_only | no_calculator | 2023 Q5(b) |
| BC-QA-06012 | Differentiating an accumulation function with a variable upper limit | shared | no_calculator | 2024 Q5(a), 2025 Q4(A) |
| BC-QA-06013 | Manipulating definite integrals with their properties | shared | no_calculator | none in 2023 to 2025 |
| BC-QA-06014 | Converting between a limit of Riemann sums and a definite integral | shared | no_calculator | none in 2023 to 2025 |
| BC-QA-06015 | Interpreting a definite integral in context with units | shared | either | 2023 Q1(a), 2024 Q1(b) |
| BC-QA-06016 | Selecting an antidifferentiation technique from the form of the integrand | shared | no_calculator | 2024 Q5(d) |

Three archetypes, BC-QA-06010, BC-QA-06013, and BC-QA-06014, have no matching part in the 2023 to 2025 free response questions read for this unit and are tagged inferred; their scoring patterns are drawn from the nearest analogous parts and from the CED text rather than from a rubric for that exact task.

## Misconception summary

Twenty six misconceptions are recorded in data/staging/unit-06.misconceptions.json against thirty two observed errors in data/staging/unit-06.errors.json. The mapping is many to many: an error lists every misconception that could produce it together with non-conceptual causes such as an arithmetic slip, a misread, or time pressure, and every misconception carries rival misconceptions and a discriminating probe. [verified] (sg-23:2, sg-25:17, sg-25:19, sg-24:4)

| Misconception | Severity | Rivals | Discriminating probe |
|---|---|---|---|
| BC-MIS-06001 A Riemann sum is a sum of the listed values | high | BC-MIS-06002, BC-MIS-06003 | Present a table whose inputs are unevenly spaced and ask for the value of one term of the sum together with its units. |
| BC-MIS-06002 The endpoint convention is cosmetic | medium | BC-MIS-06001 | Ask for the left and the right sum on the same monotone table and ask whether the two values must agree. |
| BC-MIS-06003 Riemann sums are exact | medium | BC-MIS-06005 | Ask whether the reported sum is larger or smaller than the integral and how the student knows. |
| BC-MIS-06004 A trapezoid is a rectangle at the average height of the whole interval | medium | BC-MIS-06001 | Ask for the area of the single trapezoid on the first subinterval. |
| BC-MIS-06005 Approximation direction follows from increase or decrease alone | high | BC-MIS-06006 | Give an increasing concave down rate and ask for the direction of a trapezoidal estimate and of a left sum separately. |
| BC-MIS-06006 Concavity and monotonicity are the same property | high | BC-MIS-06005 | Ask the student to sketch a decreasing concave up curve. |
| BC-MIS-06007 The plotted curve is the function under discussion | high | BC-MIS-06008 | Ask the student to label the plotted curve and the accumulation function separately before answering. |
| BC-MIS-06008 A zero of the integrand is a general turning feature of the accumulation function | high | BC-MIS-06007 | Ask where g has extrema and where g has inflection points on the same graph and compare the two lists. |
| BC-MIS-06009 Restating a definition counts as a reason | medium | BC-MIS-06010 | Ask what feature of the given graph makes the stated claim true. |
| BC-MIS-06010 A relative extremum test settles an absolute extremum | high | BC-MIS-06009 | Ask whether the endpoints can beat the interior candidate and how that is checked. |
| BC-MIS-06011 Area formulas are recalled without their fractional factors | medium | BC-MIS-06012 | Ask for the area of a single semicircle of a stated radius. |
| BC-MIS-06012 The definite integral measures unsigned area | high | BC-MIS-06011 | Ask for the integral of a rate that is negative on the whole interval. |
| BC-MIS-06013 The integral of a rate is the amount of the quantity | high | BC-MIS-06014 | Give a rate and two different initial values and ask for the value at the later input in each case. |
| BC-MIS-06014 Average value and accumulated amount are the same quantity | high | BC-MIS-06015 | Show both expressions side by side and ask for the units of each. |
| BC-MIS-06015 Average of a function and average rate of change are the same quantity | medium | BC-MIS-06014 | Ask which of the two answers has the units of the function and which has the units of a rate. |
| BC-MIS-06016 Substitution renames a variable without changing the problem | high | BC-MIS-06017 | Ask what the lower limit becomes after the substitution and why. |
| BC-MIS-06017 A composite integrand guarantees that substitution applies | high | BC-MIS-06016 | Ask the student to write du and point to it inside the integrand. |
| BC-MIS-06018 An antiderivative is a single function | medium | none recorded | Ask the student to name two different functions with the same given derivative. |
| BC-MIS-06019 Antidifferentiation distributes across a product | high | BC-MIS-06017 | Ask the student to differentiate the proposed product and compare with the integrand. |
| BC-MIS-06020 Infinity is a number that can be substituted | high | BC-MIS-06021 | Ask the student to write the improper integral as a limit before antidifferentiating. |
| BC-MIS-06021 Every improper integral of a decaying integrand converges | medium | BC-MIS-06020 | Compare the integrals of one over x and one over x squared on the same infinite interval. |
| BC-MIS-06022 Technique choice follows the surface look of the integrand | high | BC-MIS-06017 | Ask the student to state the condition the chosen technique requires and to point to it in the integrand. |
| BC-MIS-06023 The Fundamental Theorem of Calculus part one has no chain rule | medium | BC-MIS-06024 | Ask for the derivative of the upper limit on its own before the theorem is applied. |
| BC-MIS-06024 The variable of integration is the independent variable | medium | BC-MIS-06023 | Ask whether changing the letter of the variable of integration changes the function. |
| BC-MIS-06025 An interpretation is complete once the quantity is named | medium | BC-MIS-06014 | Ask what would change in the sentence if the interval were different. |
| BC-MIS-06026 The Fundamental Theorem of Calculus part two needs no hypotheses | medium | none recorded | Give an integrand with a jump inside the interval and ask whether the theorem applies directly. |

The highest severity clusters are the four that the scoring guidelines document directly: reading features of the accumulation function off the plotted integrand (BC-MIS-06007, BC-MIS-06008, sg-25:17), accepting a local argument for a global extremum (BC-MIS-06010, sg-25:19 and sg-25:5), treating the integral of a rate as the amount itself (BC-MIS-06013, sg-24:4), and treating a substitution as a renaming that leaves the limits of integration untouched (BC-MIS-06016, sg-23:16 and sg-23:17).

## Unresolved

- The task brief described topic 6.13 as the BC only integration by parts topic. data/curriculum.json and ced:128 to ced:130 show otherwise: 6.11 is integration by parts, 6.12 is linear partial fractions, 6.13 is improper integrals, and all three carry the BC only marker. The file follows the curriculum record. [verified] (ced:128, ced:129, ced:130)
- No Unit 6 free response part in 2023 to 2025 assesses linear partial fractions (BC-QA-06010), definite integral properties in isolation (BC-QA-06013), or the Riemann sum to definite integral conversion (BC-QA-06014). Their scoring patterns are inferred and should be revisited when earlier years or official multiple choice material are indexed. [uncertain]
- The 2023 and 2025 scoring guidelines treat unclear communication between a correct average value integral and a correct quotient differently: 2023 awards one of two points (sg-23:4) and 2025 treats the linkage as scratch work and awards both (sg-25:3). Whether this is a durable change in scoring practice or a question-specific decision is not established here. [uncertain]
- The CED page numbering in data/curriculum.json (pages 118 to 131) is the PDF page index; the printed page numbers on those pages run 113 to 126. Citations in this file use the PDF index to match cache/text/ced. [verified] (ced:118, ced:131)
- Misconception records are tagged inferred unless a scoring guideline names the behaviour directly. No misconception literature is cited, because none could be confirmed from the sources available in this project's cache. [inferred]

<!-- generated:official-evidence:start -->

## Official evidence index [verified]

Generated from data/frq_records.json and data/mcq_records.json. Every record cites its cached document and page; counts are observations over the indexed years only, not predictions. FRQ part records with BC-UNIT-06 as primary or secondary unit: 90. Public sample MCQ records tagged to this unit: 23.

| FRQ record | Role | Calculator | Archetype | Skills (first six) | Points | Point types |
|---|---|---|---|---|---|---|
| BC-FRQ-2013-Q1-B | primary | calculator | BC-QA-99008 | BC-SKL-06036, BC-SKL-08016, BC-SKL-08017 | 2 | BC-PT-99001, BC-PT-99004 |
| BC-FRQ-2013-Q3-C | primary | no_calculator | BC-QA-06007 | BC-SKL-06007, BC-SKL-06009, BC-SKL-08001, BC-SKL-08005, BC-SKL-06038 | 3 | BC-PT-99018, BC-PT-99019, BC-PT-99007 |
| BC-FRQ-2013-Q4-B | secondary | no_calculator | BC-QA-05006 | BC-SKL-05024, BC-SKL-05025, BC-SKL-05026, BC-SKL-05027, BC-SKL-05028, BC-SKL-06028 | 3 | BC-PT-99013, BC-PT-99004, BC-PT-99011 |
| BC-FRQ-2014-Q1-C | secondary | calculator | BC-QA-08002 | BC-SKL-08001, BC-SKL-08003, BC-SKL-08021, BC-SKL-08004 | 2 | BC-PT-99020, BC-PT-99004 |
| BC-FRQ-2014-Q3-A | primary | no_calculator | BC-QA-06003 | BC-SKL-06020, BC-SKL-06028, BC-SKL-06031, BC-SKL-06004 | 1 | BC-PT-99069 |
| BC-FRQ-2014-Q3-B | primary | no_calculator | BC-QA-05004 | BC-SKL-06022, BC-SKL-06025, BC-SKL-05031, BC-SKL-05035, BC-SKL-05017 | 2 | BC-PT-99062, BC-PT-99063 |
| BC-FRQ-2014-Q3-C | secondary | no_calculator | BC-QA-02008 | BC-SKL-02039, BC-SKL-02040, BC-SKL-06018, BC-SKL-06020 | 3 | BC-PT-99080, BC-PT-99004 |
| BC-FRQ-2014-Q4-C | primary | no_calculator | BC-QA-06002 | BC-SKL-06008, BC-SKL-08009, BC-SKL-08012, BC-SKL-06036 | 3 | BC-PT-99033, BC-PT-99018, BC-PT-99019 |
| BC-FRQ-2014-Q5-A | secondary | no_calculator | BC-QA-08008 | BC-SKL-08018, BC-SKL-08019, BC-SKL-08022, BC-SKL-06047, BC-SKL-06048 | 3 | BC-PT-99059, BC-PT-99003, BC-PT-99004 |
| BC-FRQ-2014-Q6-C | secondary | no_calculator | BC-QA-10019 | BC-SKL-10006, BC-SKL-10008, BC-SKL-10072, BC-SKL-10069, BC-SKL-06052, BC-SKL-07029 | 3 | BC-PT-99067, BC-PT-99003, BC-PT-99004 |
| BC-FRQ-2015-Q1-A | primary | calculator | BC-QA-99008 | BC-SKL-06036, BC-SKL-08016, BC-SKL-08017 | 2 | BC-PT-99002, BC-PT-99004 |
| BC-FRQ-2015-Q1-D | secondary | calculator | BC-QA-06006 | BC-SKL-08012, BC-SKL-08013, BC-SKL-08016, BC-SKL-06039, BC-SKL-06017 | 2 | BC-PT-99001, BC-PT-99068 |
| BC-FRQ-2015-Q3-B | primary | no_calculator | BC-QA-06001 | BC-SKL-06006, BC-SKL-06009, BC-SKL-08015, BC-SKL-08007, BC-SKL-08006 | 3 | BC-PT-99007, BC-PT-99018, BC-PT-99019 |
| BC-FRQ-2015-Q3-D | secondary | no_calculator | BC-QA-08001 | BC-SKL-08001, BC-SKL-06034, BC-SKL-06040 | 3 | BC-PT-99020, BC-PT-99003, BC-PT-99004 |
| BC-FRQ-2015-Q5-D | primary | no_calculator | BC-QA-06010 | BC-SKL-06062, BC-SKL-06063, BC-SKL-06064, BC-SKL-06044, BC-SKL-06052 | 4 | BC-PT-99081, BC-PT-99003 |
| BC-FRQ-2018-Q1-A | primary | calculator | BC-QA-99008 | BC-SKL-06036, BC-SKL-08016, BC-SKL-08017 | 0 |  |
| BC-FRQ-2018-Q1-B | secondary | calculator | BC-QA-06006 | BC-SKL-08012, BC-SKL-08013, BC-SKL-06039, BC-SKL-06037 | 0 |  |
| BC-FRQ-2018-Q2-B | primary | calculator | BC-QA-99009 | BC-SKL-06036, BC-SKL-08016, BC-SKL-08017 | 0 |  |
| BC-FRQ-2018-Q2-C | primary | calculator | BC-QA-99010 | BC-SKL-06031, BC-SKL-06029, BC-SKL-06066, BC-SKL-06067, BC-SKL-08016 | 0 |  |
| BC-FRQ-2018-Q3-A | primary | no_calculator | BC-QA-06003 | BC-SKL-06020, BC-SKL-06028, BC-SKL-06031, BC-SKL-06037 | 0 |  |
| BC-FRQ-2018-Q3-B | primary | no_calculator | BC-QA-06004 | BC-SKL-06028, BC-SKL-06031, BC-SKL-06034, BC-SKL-06040 | 0 |  |
| BC-FRQ-2018-Q3-C | primary | no_calculator | BC-QA-05004 | BC-SKL-06022, BC-SKL-06025, BC-SKL-05031, BC-SKL-05035, BC-SKL-05017 | 0 |  |
| BC-FRQ-2018-Q3-D | secondary | no_calculator | BC-QA-05005 | BC-SKL-06024, BC-SKL-05032, BC-SKL-05033, BC-SKL-05035 | 0 |  |
| BC-FRQ-2018-Q4-C | primary | no_calculator | BC-QA-06002 | BC-SKL-06008, BC-SKL-08001, BC-SKL-08005 | 0 |  |
| BC-FRQ-2019-Q1-A | secondary | calculator | BC-QA-06005 | BC-SKL-08016, BC-SKL-08017, BC-SKL-06036, BC-SKL-08003 | 2 | BC-PT-99001, BC-PT-99004 |
| BC-FRQ-2019-Q1-B | secondary | calculator | BC-QA-08001 | BC-SKL-08001, BC-SKL-08003, BC-SKL-08004, BC-SKL-08005 | 2 | BC-PT-99001, BC-PT-99004 |
| BC-FRQ-2019-Q1-C | secondary | calculator | BC-QA-08006 | BC-SKL-08013, BC-SKL-08014, BC-SKL-05029, BC-SKL-06026, BC-SKL-05024 | 3 | BC-PT-99013, BC-PT-99004, BC-PT-99010 |
| BC-FRQ-2019-Q2-A | secondary | calculator | BC-QA-09012 | BC-SKL-09035, BC-SKL-09036, BC-SKL-09038 | 2 | BC-PT-99048, BC-PT-99004 |
| BC-FRQ-2019-Q2-C | secondary | calculator | BC-QA-09012 | BC-SKL-09035, BC-SKL-09036, BC-SKL-09043, BC-SKL-09029 | 3 | BC-PT-99048, BC-PT-99001, BC-PT-99005 |
| BC-FRQ-2019-Q2-D | secondary | calculator | BC-QA-09012 | BC-SKL-09035, BC-SKL-09036, BC-SKL-09038, BC-SKL-01060 | 2 | BC-PT-99001, BC-PT-99005 |
| BC-FRQ-2019-Q3-A | primary | no_calculator | BC-QA-06013 | BC-SKL-06031, BC-SKL-06028, BC-SKL-06004 | 3 | BC-PT-99005, BC-PT-99069, BC-PT-99004 |
| BC-FRQ-2019-Q3-B | primary | no_calculator | BC-QA-06013 | BC-SKL-06034, BC-SKL-06029, BC-SKL-06035 | 2 | BC-PT-99005, BC-PT-99004 |
| BC-FRQ-2019-Q3-C | primary | no_calculator | BC-QA-06003 | BC-SKL-06018, BC-SKL-06023, BC-SKL-06026, BC-SKL-05024, BC-SKL-05026 | 3 | BC-PT-99024, BC-PT-99013, BC-PT-99011 |
| BC-FRQ-2019-Q4-C | secondary | no_calculator | BC-QA-07003 | BC-SKL-07024, BC-SKL-07025, BC-SKL-07026, BC-SKL-07029, BC-SKL-07027, BC-SKL-06040 | 4 | BC-PT-99028, BC-PT-99029, BC-PT-99031, BC-PT-99032 |
| BC-FRQ-2019-Q5-B | primary | no_calculator | BC-QA-06010 | BC-SKL-06062, BC-SKL-06063, BC-SKL-06064, BC-SKL-06065 | 3 | BC-PT-99005, BC-PT-99003, BC-PT-99004 |
| BC-FRQ-2019-Q5-C | primary | no_calculator | BC-QA-06011 | BC-SKL-06066, BC-SKL-06067, BC-SKL-06069, BC-SKL-06070 | 3 | BC-PT-99053, BC-PT-99003, BC-PT-99005 |
| BC-FRQ-2019-Q6-C | secondary | no_calculator | BC-QA-10019 | BC-SKL-10069, BC-SKL-10048, BC-SKL-06017, BC-SKL-06040 | 2 | BC-PT-99003, BC-PT-99004 |
| BC-FRQ-2019-Q6-D | secondary | no_calculator | BC-QA-10008 | BC-SKL-10039, BC-SKL-10040, BC-SKL-10041, BC-SKL-10042, BC-SKL-10069 | 3 | BC-PT-99036, BC-PT-99040, BC-PT-99041 |
| BC-FRQ-2021-Q1-B | primary | calculator | BC-QA-06001 | BC-SKL-06006, BC-SKL-06009, BC-SKL-06013 | 2 | BC-PT-99018, BC-PT-99019 |
| BC-FRQ-2021-Q1-C | primary | calculator | BC-QA-06001 | BC-SKL-06010, BC-SKL-02036, BC-SKL-05017 | 2 | BC-PT-99022, BC-PT-99026 |
| BC-FRQ-2021-Q1-D | secondary | calculator | BC-QA-08001 | BC-SKL-08001, BC-SKL-08003, BC-SKL-08004 | 3 | BC-PT-99001, BC-PT-99020, BC-PT-99004 |
| BC-FRQ-2021-Q3-A | primary | no_calculator | BC-QA-06008 | BC-SKL-06047, BC-SKL-06048, BC-SKL-06050, BC-SKL-08019, BC-SKL-08020 | 3 | BC-PT-99002, BC-PT-99003, BC-PT-99004 |
| BC-FRQ-2021-Q3-C | secondary | no_calculator | BC-QA-08012 | BC-SKL-08040, BC-SKL-08041, BC-SKL-08043, BC-SKL-06034, BC-SKL-06055 | 4 | BC-PT-99058, BC-PT-99001, BC-PT-99003, BC-PT-99004 |
| BC-FRQ-2021-Q4-A | primary | no_calculator | BC-QA-06003 | BC-SKL-06025, BC-SKL-06018, BC-SKL-05031, BC-SKL-05035 | 1 | BC-PT-99062 |
| BC-FRQ-2021-Q4-B | secondary | no_calculator | BC-QA-02009 | BC-SKL-02036, BC-SKL-02037, BC-SKL-06018, BC-SKL-06020, BC-SKL-06028 | 3 | BC-PT-99022, BC-PT-99069, BC-PT-99004 |
| BC-FRQ-2021-Q4-C | secondary | no_calculator | BC-QA-04009 | BC-SKL-04033, BC-SKL-04034, BC-SKL-04035, BC-SKL-04036, BC-SKL-06018 | 2 | BC-PT-99055, BC-PT-99005 |
| BC-FRQ-2021-Q4-D | secondary | no_calculator | BC-QA-05001 | BC-SKL-05003, BC-SKL-05001, BC-SKL-05002, BC-SKL-05004, BC-SKL-06020 | 2 | BC-PT-99021, BC-PT-99017 |
| BC-FRQ-2021-Q5-C | secondary | no_calculator | BC-QA-07003 | BC-SKL-07024, BC-SKL-07025, BC-SKL-07026, BC-SKL-07029, BC-SKL-07027, BC-SKL-06057 | 5 | BC-PT-99028, BC-PT-99029, BC-PT-99030, BC-PT-99031, BC-PT-99032 |
| BC-FRQ-2021-Q6-A | secondary | no_calculator | BC-QA-10005 | BC-SKL-10014, BC-SKL-10015, BC-SKL-10016, BC-SKL-10017, BC-SKL-06067 | 3 | BC-PT-99005, BC-PT-99053, BC-PT-99003 |
| BC-FRQ-2022-Q1-A | secondary | calculator | BC-QA-08007 | BC-SKL-08016, BC-SKL-06036, BC-SKL-08015 | 1 | BC-PT-99001 |
| BC-FRQ-2022-Q1-B | secondary | calculator | BC-QA-08001 | BC-SKL-08001, BC-SKL-08003, BC-SKL-08005 | 2 | BC-PT-99020, BC-PT-99004 |
| BC-FRQ-2022-Q1-D | secondary | calculator | BC-QA-08006 | BC-SKL-08013, BC-SKL-08014, BC-SKL-06018, BC-SKL-05024, BC-SKL-05026, BC-SKL-05028 | 4 | BC-PT-99013, BC-PT-99064, BC-PT-99004, BC-PT-99011 |
| BC-FRQ-2022-Q2-C | secondary | calculator | BC-QA-09005 | BC-SKL-09021, BC-SKL-09026, BC-SKL-08012, BC-SKL-06037 | 3 | BC-PT-99002, BC-PT-99033, BC-PT-99004 |
| BC-FRQ-2022-Q3-A | primary | no_calculator | BC-QA-06005 | BC-SKL-06028, BC-SKL-06034, BC-SKL-06037, BC-SKL-06004, BC-SKL-06030 | 3 | BC-PT-99069, BC-PT-99004, BC-PT-99004 |
| BC-FRQ-2022-Q3-D | secondary | no_calculator | BC-QA-05006 | BC-SKL-05010, BC-SKL-05024, BC-SKL-05026, BC-SKL-05028, BC-SKL-05027 | 2 | BC-PT-99013, BC-PT-99011 |
| BC-FRQ-2022-Q4-C | primary | no_calculator | BC-QA-06001 | BC-SKL-06006, BC-SKL-06009, BC-SKL-06013 | 2 | BC-PT-99018, BC-PT-99019 |
| BC-FRQ-2022-Q5-A | secondary | no_calculator | BC-QA-08008 | BC-SKL-08019, BC-SKL-08022, BC-SKL-06041, BC-SKL-06034 | 2 | BC-PT-99001, BC-PT-99004 |
| BC-FRQ-2022-Q5-B | secondary | no_calculator | BC-QA-08011 | BC-SKL-08033, BC-SKL-08035, BC-SKL-06057, BC-SKL-06058, BC-SKL-06060 | 4 | BC-PT-99001, BC-PT-99056, BC-PT-99057, BC-PT-99004 |
| BC-FRQ-2022-Q5-C | secondary | no_calculator | BC-QA-08012 | BC-SKL-08041, BC-SKL-08043, BC-SKL-06066, BC-SKL-06067, BC-SKL-06068 | 3 | BC-PT-99053, BC-PT-99003, BC-PT-99004 |
| BC-FRQ-2023-Q1-A | primary | calculator | BC-QA-06001 | BC-SKL-06006, BC-SKL-06002, BC-SKL-08015 | 3 | BC-PT-99007, BC-PT-99018, BC-PT-99019 |
| BC-FRQ-2023-Q1-C | secondary | calculator | BC-QA-06007 | BC-SKL-08001, BC-SKL-08003, BC-SKL-06038, BC-SKL-08004 | 2 | BC-PT-99020, BC-PT-99004 |
| BC-FRQ-2023-Q2-C | secondary | calculator | BC-QA-09001 | BC-SKL-09002, BC-SKL-09004, BC-SKL-09021, BC-SKL-09026, BC-SKL-06037 | 3 | BC-PT-99049, BC-PT-99001, BC-PT-99004 |
| BC-FRQ-2023-Q3-D | secondary | no_calculator | BC-QA-07003 | BC-SKL-07024, BC-SKL-07025, BC-SKL-07026, BC-SKL-07029, BC-SKL-07030, BC-SKL-07027 | 4 | BC-PT-99028, BC-PT-99029, BC-PT-99031, BC-PT-99032 |
| BC-FRQ-2023-Q4-D | secondary | no_calculator | BC-QA-05006 | BC-SKL-05024, BC-SKL-05025, BC-SKL-05026, BC-SKL-05027, BC-SKL-05028, BC-SKL-06020 | 3 | BC-PT-99013, BC-PT-99011, BC-PT-99004 |
| BC-FRQ-2023-Q5-A | secondary | no_calculator | BC-QA-08008 | BC-SKL-08018, BC-SKL-08019, BC-SKL-06029, BC-SKL-06052, BC-SKL-06034 | 3 | BC-PT-99059, BC-PT-99003, BC-PT-99004 |
| BC-FRQ-2023-Q5-B | primary | no_calculator | BC-QA-06011 | BC-SKL-06066, BC-SKL-06067, BC-SKL-06068, BC-SKL-06040, BC-SKL-01058 | 3 | BC-PT-99053, BC-PT-99003, BC-PT-99004 |
| BC-FRQ-2023-Q5-C | primary | no_calculator | BC-QA-06009 | BC-SKL-06057, BC-SKL-06058, BC-SKL-06060, BC-SKL-06061, BC-SKL-06029 | 3 | BC-PT-99056, BC-PT-99057, BC-PT-99004 |
| BC-FRQ-2024-Q1-B | primary | calculator | BC-QA-06001 | BC-SKL-06005, BC-SKL-08005, BC-SKL-08004, BC-SKL-06038 | 3 | BC-PT-99018, BC-PT-99019, BC-PT-99007 |
| BC-FRQ-2024-Q1-C | secondary | calculator | BC-QA-06005 | BC-SKL-06036, BC-SKL-06037, BC-SKL-08012, BC-SKL-08017, BC-SKL-06046 | 3 | BC-PT-99001, BC-PT-99033, BC-PT-99004 |
| BC-FRQ-2024-Q2-C | secondary | calculator | BC-QA-09005 | BC-SKL-09021, BC-SKL-09022, BC-SKL-09026, BC-SKL-06037, BC-SKL-08012 | 3 | BC-PT-99001, BC-PT-99033, BC-PT-99004 |
| BC-FRQ-2024-Q3-C | secondary | no_calculator | BC-QA-07003 | BC-SKL-07024, BC-SKL-07025, BC-SKL-07026, BC-SKL-07029, BC-SKL-07030, BC-SKL-07027 | 5 | BC-PT-99028, BC-PT-99029, BC-PT-99030, BC-PT-99031, BC-PT-99032 |
| BC-FRQ-2024-Q4-A | primary | no_calculator | BC-QA-06004 | BC-SKL-06020, BC-SKL-06028, BC-SKL-06030, BC-SKL-06031, BC-SKL-06004 | 3 | BC-PT-99069, BC-PT-99069, BC-PT-99069 |
| BC-FRQ-2024-Q4-B | primary | no_calculator | BC-QA-06003 | BC-SKL-06018, BC-SKL-06022, BC-SKL-05010, BC-SKL-05022 | 2 | BC-PT-99024, BC-PT-99013 |
| BC-FRQ-2024-Q4-C | primary | no_calculator | BC-QA-06012 | BC-SKL-06018, BC-SKL-06035, BC-SKL-03030, BC-SKL-03032, BC-SKL-06034 | 4 | BC-PT-99024, BC-PT-99004, BC-PT-99004, BC-PT-99004 |
| BC-FRQ-2024-Q5-A | primary | no_calculator | BC-QA-06012 | BC-SKL-06018, BC-SKL-06021, BC-SKL-03002 | 2 | BC-PT-99024, BC-PT-99004 |
| BC-FRQ-2024-Q5-D | primary | no_calculator | BC-QA-06009 | BC-SKL-06057, BC-SKL-06058, BC-SKL-06042, BC-SKL-06044, BC-SKL-06047 | 3 | BC-PT-99056, BC-PT-99057, BC-PT-99004 |
| BC-FRQ-2025-Q1-A | secondary | calculator | BC-QA-06007 | BC-SKL-08001, BC-SKL-08003, BC-SKL-06038, BC-SKL-08004, BC-SKL-08005 | 2 | BC-PT-99020, BC-PT-99004 |
| BC-FRQ-2025-Q1-D | secondary | calculator | BC-QA-05006 | BC-SKL-06018, BC-SKL-05010, BC-SKL-05024, BC-SKL-05025, BC-SKL-05026, BC-SKL-05028 | 3 | BC-PT-99013, BC-PT-99011, BC-PT-99005 |
| BC-FRQ-2025-Q3-C | primary | no_calculator | BC-QA-06002 | BC-SKL-06008, BC-SKL-06009, BC-SKL-06005, BC-SKL-06006 | 2 | BC-PT-99018, BC-PT-99019 |
| BC-FRQ-2025-Q3-D | secondary | no_calculator | BC-QA-06005 | BC-SKL-06036, BC-SKL-06040, BC-SKL-06034, BC-SKL-08016, BC-SKL-08017 | 3 | BC-PT-99002, BC-PT-99003, BC-PT-99004 |
| BC-FRQ-2025-Q4-A | primary | no_calculator | BC-QA-06012 | BC-SKL-06018, BC-SKL-06021, BC-SKL-06027 | 2 | BC-PT-99024, BC-PT-99004 |
| BC-FRQ-2025-Q4-B | secondary | no_calculator | BC-QA-05005 | BC-SKL-06024, BC-SKL-05032, BC-SKL-05033, BC-SKL-05035, BC-SKL-05031 | 2 | BC-PT-99060, BC-PT-99061 |
| BC-FRQ-2025-Q4-C | primary | no_calculator | BC-QA-06004 | BC-SKL-06020, BC-SKL-06028, BC-SKL-06030, BC-SKL-06004 | 2 | BC-PT-99069, BC-PT-99069 |
| BC-FRQ-2025-Q4-D | secondary | no_calculator | BC-QA-05006 | BC-SKL-06026, BC-SKL-05024, BC-SKL-05025, BC-SKL-05026, BC-SKL-05028, BC-SKL-05029 | 3 | BC-PT-99013, BC-PT-99011, BC-PT-99004 |
| BC-FRQ-2026-Q1-B | primary | calculator | BC-QA-06001 | BC-SKL-06007, BC-SKL-06009, BC-SKL-08015, BC-SKL-06002 | 3 | BC-PT-99018, BC-PT-99019, BC-PT-99007 |
| BC-FRQ-2026-Q1-C | secondary | calculator | BC-QA-06005 | BC-SKL-06036, BC-SKL-08016, BC-SKL-08017, BC-SKL-06046 | 2 | BC-PT-99001, BC-PT-99004 |
| BC-FRQ-2026-Q3-D | secondary | no_calculator | BC-QA-07003 | BC-SKL-07024, BC-SKL-07025, BC-SKL-07026, BC-SKL-07029, BC-SKL-07030, BC-SKL-07027 | 5 | BC-PT-99028, BC-PT-99029, BC-PT-99030, BC-PT-99031, BC-PT-99032 |
| BC-FRQ-2026-Q4-D | secondary | no_calculator | BC-QA-05006 | BC-SKL-05024, BC-SKL-05029, BC-SKL-05026, BC-SKL-05028, BC-SKL-05015, BC-SKL-06028 | 3 | BC-PT-99013, BC-PT-99011, BC-PT-99011 |
| BC-FRQ-2026-Q5-A | primary | no_calculator | BC-QA-06008 | BC-SKL-06047, BC-SKL-06040, BC-SKL-06034, BC-SKL-06051 | 2 | BC-PT-99003, BC-PT-99004 |
| BC-FRQ-2026-Q5-D | primary | no_calculator | BC-QA-06011 | BC-SKL-06066, BC-SKL-06067, BC-SKL-06068, BC-SKL-06041, BC-SKL-01058 | 3 | BC-PT-99053, BC-PT-99003, BC-PT-99004 |

| MCQ record | Calculator | Archetype | Skills |
|---|---|---|---|
| BC-MCQ-CED-006 | no_calculator | BC-QA-06014 | BC-SKL-06015, BC-SKL-06013, BC-SKL-06014 |
| BC-MCQ-CED-007 | no_calculator | BC-QA-06003 | BC-SKL-06022, BC-SKL-06027, BC-SKL-06020 |
| BC-MCQ-CED-008 | no_calculator | BC-QA-06008 | BC-SKL-06047, BC-SKL-06048, BC-SKL-06043 |
| BC-MCQ-CED-016 | no_calculator | BC-QA-06009 | BC-SKL-06061, BC-SKL-06060, BC-SKL-06058 |
| BC-MCQ-SAMPLE-007 | no_calculator | BC-QA-06012 | BC-SKL-06019, BC-SKL-06018, BC-SKL-03002 |
| BC-MCQ-SAMPLE-008 | no_calculator | BC-QA-06014 | BC-SKL-06015, BC-SKL-06014, BC-SKL-06013 |
| BC-MCQ-SAMPLE-009 | no_calculator | BC-QA-08001 | BC-SKL-08002, BC-SKL-06028, BC-SKL-08001 |
| BC-MCQ-SAMPLE-015 | calculator | BC-QA-08004 | BC-SKL-08012, BC-SKL-06037, BC-SKL-06034 |
| BC-MCQ-SAMPLE-016 | calculator | BC-QA-08003 | BC-SKL-08010, BC-SKL-08006, BC-SKL-06040 |
| BC-MCQ-SAMPLE-019 | no_calculator | BC-QA-06011 | BC-SKL-06066, BC-SKL-06067, BC-SKL-06068 |
| BC-MCQ-PE2012-003 | no_calculator | BC-QA-06004 | BC-SKL-06028, BC-SKL-06004, BC-SKL-06031 |
| BC-MCQ-PE2012-006 | no_calculator | BC-QA-06008 | BC-SKL-06050, BC-SKL-06048, BC-SKL-06047 |
| BC-MCQ-PE2012-008 | no_calculator | BC-QA-06001 | BC-SKL-06006, BC-SKL-08012, BC-SKL-06005 |
| BC-MCQ-PE2012-010 | no_calculator | BC-QA-06008 | BC-SKL-06034, BC-SKL-06040, BC-SKL-06035 |
| BC-MCQ-PE2012-015 | no_calculator | BC-QA-06003 | BC-SKL-06020, BC-SKL-06022, BC-SKL-06025 |
| BC-MCQ-PE2012-018 | no_calculator | BC-QA-06003 | BC-SKL-06031, BC-SKL-06030, BC-SKL-06028 |
| BC-MCQ-PE2012-020 | no_calculator | BC-QA-06010 | BC-SKL-06062, BC-SKL-06063, BC-SKL-06064 |
| BC-MCQ-PE2012-024 | no_calculator | BC-QA-06009 | BC-SKL-06057, BC-SKL-06058, BC-SKL-06061 |
| BC-MCQ-PE2012-025 | no_calculator | BC-QA-06011 | BC-SKL-06067, BC-SKL-06068, BC-SKL-06047 |
| BC-MCQ-PE2012-028 | no_calculator | BC-QA-04009 | BC-SKL-04033, BC-SKL-04035, BC-SKL-06018 |
| BC-MCQ-PE2012-031 | calculator | BC-QA-06013 | BC-SKL-06029, BC-SKL-06028, BC-SKL-06031 |
| BC-MCQ-PE2012-039 | calculator | BC-QA-06003 | BC-SKL-06036, BC-SKL-05014, BC-SKL-06028 |
| BC-MCQ-PE2012-045 | calculator | BC-QA-05009 | BC-SKL-05042, BC-SKL-06031, BC-SKL-05020 |

<!-- generated:official-evidence:end -->
