---
title: Unit 3, Differentiation: Composite, Implicit, and Inverse Functions
research_date: 2026-09-19
status: draft
purpose: Decompose CED Unit 3 into concepts, atomic skills, non-calculus prerequisites, question archetypes and variants, observed errors, candidate misconceptions, and diagnostic signals, each grounded in the CED text, in the 2023 to 2025 official scoring guidelines, and in the Chief Reader reports.
---

# Unit 3, Differentiation: Composite, Implicit, and Inverse Functions

BC-UNIT-03 covers CED pages 70 to 80 in the printed framework, indexed as pages 72 to 80 in this project's cache, and holds six topics. Every topic is shared with AB. One enduring understanding, FUN-3, carries the whole unit, and one learning objective covers topics 3.3 and 3.4 together. Topic 3.5 carries no learning objective and no essential knowledge statement: the CED presents it as a skill focus over the other objectives in the unit. Unit weighting is in [../exam/exam-blueprint.md](../exam/exam-blueprint.md) and exam composition is in [../exam/exam-structure.md](../exam/exam-structure.md). [verified] (ced:72, ced:75, ced:79, ced:80)

## 3.1 The Chain Rule

### Official mapping

Topic id BC-TOP-0301, CED code 3.1, name The Chain Rule, scope shared, CED page 75. [verified] (ced:75)

- BC-LO-FUN-3C (FUN-3.C): Calculate derivatives of compositions of differentiable functions.
  - BC-EK-FUN-3C1 (FUN-3.C.1): "The chain rule provides a way to differentiate composite functions."

Suggested practice skills: BC-MPS-1C (Practice skill 1.C). Weighting pointer: [../exam/exam-blueprint.md](../exam/exam-blueprint.md).

### Concept breakdown

- BC-CON-03001 Composite function structure: A composite function is one function evaluated at the output of another, and it can be split into an outer and an inner part.
- BC-CON-03002 Chain rule as a product of rates: The derivative of a composite is the derivative of the outer part times the derivative of the inner part.

- BC-SKL-03001 Decompose a composite function into outer and inner functions: Name which operation is applied last and which is applied first in a formula.
- BC-SKL-03002 Differentiate a two layer composite function with the chain rule: Differentiate the outside, keep the inside, then multiply by the derivative of the inside.
- BC-SKL-03003 Differentiate a composite with three or more layers: Keep applying the chain rule inward until nothing is left undifferentiated.
- BC-SKL-03004 Evaluate the derivative of a composite at a point from a table of values: Look up the inner value first, then look up the outer derivative at that value.
- BC-SKL-03005 Evaluate the derivative of a composite at a point from graphs: Read the inner output and the two slopes off the graphs, then multiply.
- BC-SKL-03006 Combine the chain rule with the product or quotient rule: Use the outer structure first, then apply the chain rule to whichever factor is itself composite.

### Prerequisites

- BC-PRQ-03001 -> BC-SKL-03001, supporting, [inferred], Prerequisite for Decompose a composite function into outer and inner functions.
- BC-PRQ-03001 -> BC-SKL-03002, supporting, [inferred], Prerequisite for Differentiate a two layer composite function with the chain rule.
- BC-PRQ-03001 -> BC-SKL-03003, supporting, [inferred], Prerequisite for Differentiate a composite with three or more layers.
- BC-PRQ-03001 -> BC-SKL-03004, supporting, [inferred], Prerequisite for Evaluate the derivative of a composite at a point from a table of values.
- BC-PRQ-03005 -> BC-SKL-03004, supporting, [inferred], Prerequisite for Evaluate the derivative of a composite at a point from a table of values.
- BC-PRQ-03001 -> BC-SKL-03005, supporting, [inferred], Prerequisite for Evaluate the derivative of a composite at a point from graphs.
- BC-PRQ-03005 -> BC-SKL-03005, supporting, [inferred], Prerequisite for Evaluate the derivative of a composite at a point from graphs.
- BC-PRQ-03001 -> BC-SKL-03006, supporting, [inferred], Prerequisite for Combine the chain rule with the product or quotient rule.
- BC-PRQ-03006 -> BC-SKL-03006, supporting, [inferred], Prerequisite for Combine the chain rule with the product or quotient rule.
- BC-SKL-03001 -> BC-SKL-03002, hard_prerequisite, [inferred], Decomposition precedes any chain rule application.
- BC-SKL-03002 -> BC-SKL-03003, hard_prerequisite, [inferred], A multi-layer composite repeats the two layer procedure.
- BC-SKL-03002 -> BC-SKL-03004, hard_prerequisite, [inferred], The table evaluation instantiates the symbolic chain rule.
- BC-SKL-03004 -> BC-SKL-03005, supporting, [inferred], Reading values from a graph parallels reading them from a table.
- BC-SKL-03002 -> BC-SKL-03006, hard_prerequisite, [inferred], The composite factor is differentiated inside the product or quotient rule.
- BC-TOP-0205 -> BC-SKL-03002, hard_prerequisite, [inferred], The power rule is the outer rule in most composite derivatives; no Unit 2 skill id exists yet, so the topic id stands in for it.
- BC-TOP-0207 -> BC-SKL-03002, hard_prerequisite, [inferred], Derivatives of the sine, cosine, exponential, and natural logarithm functions supply the outer derivatives; the topic id stands in for the Unit 2 skill.
- BC-TOP-0208 -> BC-SKL-03006, hard_prerequisite, [inferred], The product rule is applied around the composite factor; the topic id stands in for the Unit 2 skill.
- BC-TOP-0209 -> BC-SKL-03006, hard_prerequisite, [inferred], The quotient rule is applied around the composite factor; the topic id stands in for the Unit 2 skill.
- BC-TOP-0204 -> BC-SKL-03005, supporting, [inferred], Knowing where a derivative fails to exist is needed before a slope is read off a graph; the topic id stands in for the Unit 2 skill.

### Required mathematical knowledge

**Chain rule.** Hypotheses: g is differentiable at x and f is differentiable at g of x. Conclusion: the composite f of g is differentiable at x and its derivative is f prime of g of x multiplied by g prime of x.

**Leibniz form.** With y a function of u and u a function of x, dy/dx equals dy/du multiplied by du/dx, which the CED presents as the notation that records the two dependencies (ced:72).

**Decomposition.** Applying the rule requires naming the outer and the inner function first; the CED unit overview identifies decomposing a composite into its outer and inner components as a key skill (ced:72).

**Notation.** f of g of x, f prime of g of x, dy/du, du/dx, and the phrase times the derivative of the inner function.

### Representations

Representations in play: BC-REP-01 Symbolic (analytical) expression, BC-REP-02 Graphical, BC-REP-03 Numerical table, BC-REP-04 Verbal description.

Conversions tested: table of component values to a numerical derivative of the composite (BC-REP-03 to BC-REP-01), graphs of the components to a numerical derivative (BC-REP-02 to BC-REP-01), and a verbal description of a dependency chain to a symbolic chain rule statement (BC-REP-04 to BC-REP-01).

### Assessment behaviour

MCQ forms supply a formula and ask for its derivative, or supply a table or a pair of graphs and ask for the derivative of a composite at one input. FRQ forms rarely ask for a bare chain rule derivative; the rule appears as a scored element inside a larger task, and the 2025 BC scoring guidelines award a separate chain rule point where a composite is differentiated inside a second derivative calculation (sg-25:20). Calculator variants evaluate the resulting expression numerically; no-calculator variants keep the arithmetic exact. Conceptual variants ask which decomposition is correct; computational variants ask for the derivative; interpretation variants ask what each factor of the product measures; justification variants ask why a factor is present; multi-concept variants enclose the composite in a product or a quotient (ced:79).

### Archetypes

- BC-QA-03001 Chain rule derivative of a composite given symbolically
- BC-QA-03002 Composite derivative evaluated from a table of values
- BC-QA-03003 Composite derivative read from graphs of the component functions

### Errors and misconceptions

- BC-ERR-03001 Inner derivative omitted from a chain rule application
- BC-ERR-03002 One layer of a multi-layer composite left undifferentiated
- BC-ERR-03003 Outer derivative read at the input rather than at the inner output
- BC-ERR-03004 Table entries combined by addition rather than by the chain rule
- BC-ERR-03005 Slope read at a point where a graph is not differentiable
- BC-ERR-03006 Product or quotient rule omitted when a composite is one factor
- BC-MIS-03001 Differentiation acts only on the outermost shell, severity high
- BC-MIS-03002 The chain rule factors are evaluated at the same input, severity high
- BC-MIS-03012 The differentiation rule follows from the look of the expression, severity high

### Diagnostic signals

- BC-SIG-03001 Outer derivative correct with no inner factor, mastery state partially_mastered
- BC-SIG-03002 All layers present with one factor misplaced, mastery state partially_mastered
- BC-SIG-03003 Chain rule written symbolically then evaluated at one input, mastery state partially_mastered

### Adaptive metadata summary

Skills in this topic carry calculator relevance none. Remediation targets named across the topic: BC-PRQ-03001, BC-SKL-03001, BC-SKL-03002, BC-SKL-03004. Every skill record carries the full seven key adaptive block in data/staging/unit-03.skills.json. [inferred]

## 3.2 Implicit Differentiation

### Official mapping

Topic id BC-TOP-0302, CED code 3.2, name Implicit Differentiation, scope shared, CED page 76. [verified] (ced:76)

- BC-LO-FUN-3D (FUN-3.D): Calculate derivatives of implicitly defined functions.
  - BC-EK-FUN-3D1 (FUN-3.D.1): "The chain rule is the basis for implicit differentiation."

Suggested practice skills: BC-MPS-1E (Practice skill 1.E). Weighting pointer: [../exam/exam-blueprint.md](../exam/exam-blueprint.md).

### Concept breakdown

- BC-CON-03003 A dependent variable inside an equation: When y depends on x, every y term differentiates with an extra dy/dx factor because the chain rule applies to y as well.
- BC-CON-03004 Solving a differentiated relation for dy/dx: After differentiating both sides, the dy/dx terms are collected on one side and factored out to isolate dy/dx.
- BC-CON-03005 Tangent line behaviour on an implicit curve: A horizontal tangent needs the numerator of dy/dx to vanish and a vertical tangent needs the denominator to vanish, and in both cases the point must also lie on the curve.

- BC-SKL-03007 Differentiate a term in y with respect to x producing a dy/dx factor: Treat y as a function of x, so every y term picks up a dy/dx.
- BC-SKL-03008 Apply the product rule to a term containing both x and y: A term like x times y needs the product rule, and the y factor still carries dy/dx.
- BC-SKL-03009 Differentiate both sides of an implicit equation term by term: Differentiate every term on both sides, and keep the equation an equation.
- BC-SKL-03010 Solve the differentiated equation for dy/dx: Gather the dy/dx terms, factor dy/dx out, and divide.
- BC-SKL-03011 Evaluate dy/dx at a stated point on the curve: Substitute both coordinates into the expression for dy/dx.
- BC-SKL-03012 Locate a point where the tangent to an implicit curve is horizontal: Set the numerator of dy/dx to zero, then check the candidate against the curve equation.
- BC-SKL-03013 Locate a point where the tangent to an implicit curve is vertical: Set the denominator of dy/dx to zero, then check the candidate against the curve equation.
- BC-SKL-03014 Verify a supplied expression for dy/dx by implicit differentiation: Do the differentiation yourself and show the algebra that turns it into the given form.

Granularity note: Topic 3.2 carries eight skills because the single essential knowledge statement compresses a procedure whose steps fail independently in the record: attaching the dy/dx factor to a y term, applying the product rule to a mixed term, keeping the equation an equation, isolating dy/dx, evaluating at a point, and locating horizontal and vertical tangents are each scored separately in the tasks the Chief Reader reports describe (cr-23:22, cr-24:17, crabbc-25:24). This topic is also the hidden prerequisite for the Unit 4 related rates topics, where the same six steps recur with time as the independent variable.

### Prerequisites

- BC-PRQ-03005 -> BC-SKL-03007, supporting, [inferred], Prerequisite for Differentiate a term in y with respect to x producing a dy/dx factor.
- BC-PRQ-03005 -> BC-SKL-03008, supporting, [inferred], Prerequisite for Apply the product rule to a term containing both x and y.
- BC-PRQ-03005 -> BC-SKL-03009, supporting, [inferred], Prerequisite for Differentiate both sides of an implicit equation term by term.
- BC-PRQ-03002 -> BC-SKL-03010, supporting, [inferred], Prerequisite for Solve the differentiated equation for dy/dx.
- BC-PRQ-03006 -> BC-SKL-03011, supporting, [inferred], Prerequisite for Evaluate dy/dx at a stated point on the curve.
- BC-PRQ-03007 -> BC-SKL-03012, supporting, [inferred], Prerequisite for Locate a point where the tangent to an implicit curve is horizontal.
- BC-PRQ-03007 -> BC-SKL-03013, supporting, [inferred], Prerequisite for Locate a point where the tangent to an implicit curve is vertical.
- BC-PRQ-03002 -> BC-SKL-03014, supporting, [inferred], Prerequisite for Verify a supplied expression for dy/dx by implicit differentiation.
- BC-PRQ-03006 -> BC-SKL-03014, supporting, [inferred], Prerequisite for Verify a supplied expression for dy/dx by implicit differentiation.
- BC-SKL-03002 -> BC-SKL-03007, hard_prerequisite, [verified], BC-EK-FUN-3D1 states that the chain rule is the basis for implicit differentiation.
- BC-SKL-03007 -> BC-SKL-03008, hard_prerequisite, [inferred], The y factor inside a product still carries dy/dx.
- BC-SKL-03007 -> BC-SKL-03009, hard_prerequisite, [inferred], Term by term differentiation applies the single term procedure across the equation.
- BC-SKL-03008 -> BC-SKL-03009, hard_prerequisite, [inferred], Mixed terms must be handled before the equation is complete.
- BC-SKL-03009 -> BC-SKL-03010, hard_prerequisite, [inferred], The equation must exist before dy/dx can be isolated.
- BC-SKL-03010 -> BC-SKL-03011, hard_prerequisite, [inferred], An expression for dy/dx is needed before it can be evaluated.
- BC-SKL-03010 -> BC-SKL-03012, hard_prerequisite, [inferred], The numerator condition is read off the expression for dy/dx.
- BC-SKL-03010 -> BC-SKL-03013, hard_prerequisite, [inferred], The denominator condition is read off the expression for dy/dx.
- BC-SKL-03010 -> BC-SKL-03014, hard_prerequisite, [inferred], Verification reproduces the derivation and then matches the stated form.
- BC-TOP-0208 -> BC-SKL-03008, hard_prerequisite, [verified], BC-EK-CHA-3D2 names the product rule as needed inside implicit differentiation; the topic id stands in for the Unit 2 skill.

### Required mathematical knowledge

**Implicit differentiation.** Hypotheses: an equation in x and y determines y as a differentiable function of x near the point of interest. Conclusion: differentiating both sides with respect to x, with the chain rule applied to every term in y, produces an equation that is linear in dy/dx.

**The dy/dx factor.** Differentiating a term in y with respect to x gives the derivative of that term with respect to y multiplied by dy/dx; this is the chain rule statement of BC-EK-FUN-3D1.

**Mixed terms.** A term containing both variables is a product, so the product rule applies and the factor in y still carries dy/dx (cr-23:23).

**Tangent conditions.** Hypotheses: the point lies on the curve and dy/dx is expressed as a quotient. Conclusion: the tangent is horizontal where the numerator is zero and the denominator is not, and vertical where the denominator is zero and the numerator is not; a candidate satisfying only the condition on dy/dx need not correspond to a point of the curve (cr-23:22, cr-24:17).

**Notation.** d/dx applied to both sides, dy/dx as the unknown factor, and the equals zero that remains on the right hand side when the original right hand side is constant (crabbc-25:25).

### Representations

Representations in play: BC-REP-01 Symbolic (analytical) expression, BC-REP-02 Graphical, BC-REP-08 Geometric diagram.

Conversions tested: an equation in two variables to an expression for the slope field of its solution curves (BC-REP-01 to BC-REP-02), and a condition on dy/dx to a geometric statement about the tangent line (BC-REP-01 to BC-REP-08).

### Assessment behaviour

MCQ forms supply an equation and ask for dy/dx or for its value at a point. FRQ forms build a multipart question on one curve: the opening part derives or verifies dy/dx, later parts use it for a tangent line approximation, for a horizontal or vertical tangent, and for a related rates part on a second curve, which is the structure the Chief Reader reports describe for 2023, 2024, and 2025 (cr-23:22, cr-24:17, crabbc-25:24). These questions sit in the no-calculator part. Conceptual variants ask what the extra factor records; computational variants ask for dy/dx; interpretation variants ask what a zero denominator means for the curve; justification variants ask why no point of a given kind exists; multi-concept variants attach a linearisation or a related rate to the same curve.

### Archetypes

- BC-QA-03004 Implicit differentiation producing or verifying dy/dx
- BC-QA-03005 Horizontal or vertical tangent on an implicitly defined curve

### Errors and misconceptions

- BC-ERR-03007 A term in y differentiated without the dy/dx factor
- BC-ERR-03008 Product rule omitted on a term containing both variables
- BC-ERR-03009 Right hand side of the equation dropped after differentiating
- BC-ERR-03010 dy/dx terms divided before they are collected
- BC-ERR-03011 Only one coordinate substituted into dy/dx
- BC-ERR-03012 Horizontal and vertical tangent conditions exchanged
- BC-ERR-03013 Tangent condition satisfied but the point is not checked against the curve
- BC-MIS-03004 In an equation, y is an independent symbol, severity high
- BC-MIS-03005 A short mixed term is a single symbol, severity high
- BC-MIS-03006 dy/dx is a number rather than an expression in both variables, severity medium
- BC-MIS-03007 A tangent condition is a condition on dy/dx alone, severity high

### Diagnostic signals

- BC-SIG-03004 Some y terms carry dy/dx and others do not, mastery state partially_mastered
- BC-SIG-03005 Differentiated equation correct but never solved for dy/dx, mastery state prerequisite_gap
- BC-SIG-03006 Correct dy/dx with a substitution slip at the point, mastery state partially_mastered
- BC-SIG-03007 Tangent condition solved but the curve equation not used, mastery state partially_mastered

### Adaptive metadata summary

Skills in this topic carry calculator relevance none. Remediation targets named across the topic: BC-PRQ-03002, BC-SKL-03002, BC-SKL-03007, BC-SKL-03010. Every skill record carries the full seven key adaptive block in data/staging/unit-03.skills.json. [inferred]

## 3.3 Differentiating Inverse Functions

### Official mapping

Topic id BC-TOP-0303, CED code 3.3, name Differentiating Inverse Functions, scope shared, CED page 77. [verified] (ced:77)

- BC-LO-FUN-3E (FUN-3.E): Calculate derivatives of inverse and inverse trigonometric functions.
  - BC-EK-FUN-3E1 (FUN-3.E.1): "The chain rule and definition of an inverse function can be used to find the derivative of an inverse function, provided the derivative exists."

Suggested practice skills: BC-MPS-3G (Practice skill 3.G). Weighting pointer: [../exam/exam-blueprint.md](../exam/exam-blueprint.md).

### Concept breakdown

- BC-CON-03006 Derivative of an inverse function: The slope of an inverse function at a point is the reciprocal of the slope of the original function at the matching point.

- BC-SKL-03015 State the inverse function derivative rule with its hypotheses: Say the rule and say what has to be true for it to apply.
- BC-SKL-03016 Locate the matching input on the original function: Find the input whose output is the number you were given.
- BC-SKL-03017 Compute the derivative of an inverse at a point from a formula: Differentiate the original function, evaluate at the matching input, and take the reciprocal.
- BC-SKL-03018 Compute the derivative of an inverse at a point from a table: Read the matching row of the table, then take the reciprocal of the listed derivative.
- BC-SKL-03019 Compute the derivative of an inverse at a point from a graph: Find the point on the graph with the given height, read the slope there, and invert it.
- BC-SKL-03020 Derive the inverse derivative rule from the chain rule: Differentiate f of g of x equals x and solve for g prime.

### Prerequisites

- BC-PRQ-03003 -> BC-SKL-03015, supporting, [inferred], Prerequisite for State the inverse function derivative rule with its hypotheses.
- BC-PRQ-03003 -> BC-SKL-03016, supporting, [inferred], Prerequisite for Locate the matching input on the original function.
- BC-PRQ-03003 -> BC-SKL-03017, supporting, [inferred], Prerequisite for Compute the derivative of an inverse at a point from a formula.
- BC-PRQ-03006 -> BC-SKL-03017, supporting, [inferred], Prerequisite for Compute the derivative of an inverse at a point from a formula.
- BC-PRQ-03003 -> BC-SKL-03018, supporting, [inferred], Prerequisite for Compute the derivative of an inverse at a point from a table.
- BC-PRQ-03003 -> BC-SKL-03019, supporting, [inferred], Prerequisite for Compute the derivative of an inverse at a point from a graph.
- BC-PRQ-03003 -> BC-SKL-03020, supporting, [inferred], Prerequisite for Derive the inverse derivative rule from the chain rule.
- BC-SKL-03002 -> BC-SKL-03020, hard_prerequisite, [verified], BC-EK-FUN-3E1 derives the inverse rule from the chain rule.
- BC-SKL-03015 -> BC-SKL-03017, hard_prerequisite, [inferred], The rule must be available before it is applied.
- BC-SKL-03016 -> BC-SKL-03017, hard_prerequisite, [inferred], The matching input is located before the reciprocal is taken.
- BC-SKL-03016 -> BC-SKL-03018, hard_prerequisite, [inferred], The matching row is located before the reciprocal is taken.
- BC-SKL-03016 -> BC-SKL-03019, hard_prerequisite, [inferred], The matching point is located before the slope is read.

### Required mathematical knowledge

**Derivative of an inverse.** Hypotheses: f is differentiable and invertible on an interval, g is the inverse of f, and f prime of g of a is not zero. Conclusion: g prime of a equals one divided by f prime of g of a. The proviso that the derivative exists is part of the essential knowledge statement.

**Derivation.** Differentiating the identity f of g of x equal to x with the chain rule gives f prime of g of x multiplied by g prime of x equal to one, and solving gives the rule.

**Matched pairs.** f of c equal to b is equivalent to g of b equal to c, so the derivative of the inverse at b is read from the behaviour of f at c, not at b.

**Notation.** g as the inverse of f, f prime of g of a, and the reciprocal written as a single fraction.

### Representations

Representations in play: BC-REP-01 Symbolic (analytical) expression, BC-REP-02 Graphical, BC-REP-03 Numerical table, BC-REP-04 Verbal description.

Conversions tested: a table of values of a function to the derivative of its inverse (BC-REP-03 to BC-REP-01), and the graph of a function to the slope of the graph of its inverse (BC-REP-02 to BC-REP-01). The CED unit overview names connecting graphs, tables, and algebraic reasoning as the route into differentiating inverse functions (ced:72).

### Assessment behaviour

MCQ forms supply a formula, a table, or a graph and ask for the derivative of the inverse at one value, with the distractor set built around evaluating at the wrong member of the matched pair. FRQ forms embed the rule in a multi-representation question. The suggested practice skill for this topic is 3.G, confirming that solutions are accurate and appropriate, which points at the nonzero hypothesis as an assessed element (ced:77). Calculator variants evaluate a messy reciprocal; no-calculator variants keep the numbers small. Conceptual variants ask what the reciprocal relationship means geometrically; computational variants ask for the number; justification variants ask why the rule applies at the stated value.

### Archetypes

- BC-QA-03006 Derivative of an inverse function at a point

### Errors and misconceptions

- BC-ERR-03014 Inverse derivative rule stated without its nonzero hypothesis
- BC-ERR-03015 Inverse derivative evaluated at the given value rather than at the matching input
- BC-ERR-03016 Reciprocal of the function value reported instead of the reciprocal of the derivative
- BC-MIS-03009 The inverse derivative rule has no hypotheses, severity medium
- BC-MIS-03008 The inverse is evaluated wherever the original is, severity high

### Diagnostic signals

- BC-SIG-03008 Inverse rule written without the nonzero condition, mastery state partially_mastered
- BC-SIG-03009 Reciprocal taken at the wrong input, mastery state prerequisite_gap

### Adaptive metadata summary

Skills in this topic carry calculator relevance none. Remediation targets named across the topic: BC-PRQ-03003, BC-SKL-03002, BC-SKL-03015, BC-SKL-03016. Every skill record carries the full seven key adaptive block in data/staging/unit-03.skills.json. [inferred]

## 3.4 Differentiating Inverse Trigonometric Functions

### Official mapping

Topic id BC-TOP-0304, CED code 3.4, name Differentiating Inverse Trigonometric Functions, scope shared, CED page 78. [verified] (ced:78)

- BC-LO-FUN-3E (FUN-3.E): Calculate derivatives of inverse and inverse trigonometric functions.
  - BC-EK-FUN-3E2 (FUN-3.E.2): "The chain rule applied with the definition of an inverse function, or the formula for the derivative of an inverse function, can be used to find the derivatives of inverse trigonometric functions."

Suggested practice skills: BC-MPS-1E (Practice skill 1.E). Weighting pointer: [../exam/exam-blueprint.md](../exam/exam-blueprint.md).

### Concept breakdown

- BC-CON-03007 Derivatives of inverse trigonometric functions: Each inverse trigonometric function has a fixed derivative formula, and a composite version carries an extra factor from the inside.

- BC-SKL-03021 State the derivatives of the inverse sine, cosine, and tangent functions: Recall the three standard inverse trigonometric derivative formulas.
- BC-SKL-03022 Differentiate an inverse trigonometric function of an inner expression: Use the formula with the inner expression in place of x, then multiply by the derivative of the inner expression.
- BC-SKL-03023 Derive an inverse trigonometric derivative by implicit differentiation: Start from the equivalent trigonometric equation, differentiate implicitly, and rewrite using an identity.
- BC-SKL-03024 Evaluate an inverse trigonometric derivative at a point: Substitute the input into the derivative formula and simplify the radical or fraction.
- BC-SKL-03025 Combine an inverse trigonometric derivative with the product or quotient rule: Apply the outer structural rule first, then substitute the inverse trigonometric derivative where it belongs.

### Prerequisites

- BC-PRQ-03004 -> BC-SKL-03021, supporting, [inferred], Prerequisite for State the derivatives of the inverse sine, cosine, and tangent functions.
- BC-PRQ-03004 -> BC-SKL-03022, supporting, [inferred], Prerequisite for Differentiate an inverse trigonometric function of an inner expression.
- BC-PRQ-03004 -> BC-SKL-03023, supporting, [inferred], Prerequisite for Derive an inverse trigonometric derivative by implicit differentiation.
- BC-PRQ-03004 -> BC-SKL-03024, supporting, [inferred], Prerequisite for Evaluate an inverse trigonometric derivative at a point.
- BC-PRQ-03006 -> BC-SKL-03024, supporting, [inferred], Prerequisite for Evaluate an inverse trigonometric derivative at a point.
- BC-PRQ-03004 -> BC-SKL-03025, supporting, [inferred], Prerequisite for Combine an inverse trigonometric derivative with the product or quotient rule.
- BC-PRQ-03006 -> BC-SKL-03025, supporting, [inferred], Prerequisite for Combine an inverse trigonometric derivative with the product or quotient rule.
- BC-SKL-03021 -> BC-SKL-03022, hard_prerequisite, [inferred], The standard formula is needed before the composite version.
- BC-SKL-03002 -> BC-SKL-03022, hard_prerequisite, [verified], BC-EK-FUN-3E2 applies the chain rule to inverse trigonometric functions.
- BC-SKL-03009 -> BC-SKL-03023, hard_prerequisite, [inferred], The derivation differentiates a trigonometric equation implicitly.
- BC-SKL-03021 -> BC-SKL-03024, hard_prerequisite, [inferred], Evaluation follows the formula.
- BC-SKL-03022 -> BC-SKL-03025, hard_prerequisite, [inferred], The composite derivative is inserted into the structural rule.

### Required mathematical knowledge

**Standard derivatives.** The derivative of the inverse sine of x is one over the square root of one minus x squared, the derivative of the inverse cosine of x is the negative of that, and the derivative of the inverse tangent of x is one over one plus x squared.

**Composite form.** With an inner function u of x, the derivative of the inverse tangent of u is u prime divided by one plus u squared, and the other formulas carry the same extra factor; this is the chain rule route named in BC-EK-FUN-3E2.

**Derivation.** Hypotheses: the inverse trigonometric function is differentiable on the interior of its domain. Conclusion: writing the equivalent trigonometric equation, differentiating implicitly, and rewriting with a Pythagorean identity recovers the standard formula.

**Notation.** arcsin, arccos, arctan, or the inverse superscript notation; the inner expression squared inside the radical or the denominator.

### Representations

Representations in play: BC-REP-01 Symbolic (analytical) expression, BC-REP-05 Contextual model, BC-REP-09 Calculator-generated numerical result.

Conversions tested: a contextual model written with an inverse trigonometric function to a rate expression (BC-REP-05 to BC-REP-01), and a rate expression to a numerical value reported to three decimal places (BC-REP-01 to BC-REP-09), which is the pattern of the 2025 calculator active contextual question (sg-25:2, sg-25:4).

### Assessment behaviour

MCQ forms supply an inverse trigonometric expression, usually with a nonlinear inner function, and ask for its derivative. FRQ forms use an inverse trigonometric model in a contextual question and state the derivative in the stem, so the scored work is the use of that expression rather than its production; the 2025 BC question does exactly this and then scores an equation comparing the instantaneous rate with an average rate, and a limit of the rate expression (sg-25:2, sg-25:4). Calculator variants dominate the contextual form; no-calculator variants dominate the symbolic form. Conceptual variants ask which formula belongs to which function; computational variants ask for the derivative; interpretation variants ask what the rate expression measures in the situation.

### Archetypes

- BC-QA-03007 Inverse trigonometric derivative with an inner function

### Errors and misconceptions

- BC-ERR-03017 Inverse trigonometric derivative formula recalled incorrectly
- BC-ERR-03018 Inner expression not substituted throughout an inverse trigonometric formula
- BC-ERR-03006 Product or quotient rule omitted when a composite is one factor
- BC-MIS-03010 The inverse trigonometric formulas are interchangeable, severity medium
- BC-MIS-03001 Differentiation acts only on the outermost shell, severity high
- BC-MIS-03011 An inverse trigonometric derivative cannot be derived, severity low
- BC-MIS-03012 The differentiation rule follows from the look of the expression, severity high

### Diagnostic signals

- BC-SIG-03010 Correct inverse trigonometric formula with the inner expression missing, mastery state partially_mastered

### Adaptive metadata summary

Skills in this topic carry calculator relevance none, optional. Remediation targets named across the topic: BC-PRQ-03004, BC-SKL-03009, BC-SKL-03021, BC-SKL-03022. Every skill record carries the full seven key adaptive block in data/staging/unit-03.skills.json. [inferred]

## 3.5 Selecting Procedures for Calculating Derivatives

### Official mapping

Topic id BC-TOP-0305, CED code 3.5, name Selecting Procedures for Calculating Derivatives, scope shared, CED page 79. [verified] (ced:79)

This topic carries no learning objective and no essential knowledge statement in the CED. The framework states that the topic focuses on the skill of selecting an appropriate procedure for calculating derivatives and that students should practise when and how to apply all of the learning objectives that concern calculating derivatives (ced:79). Skills here are therefore tagged verified against that page and carry empty learning objective lists.

Suggested practice skills: BC-MPS-1C (Practice skill 1.C). Weighting pointer: [../exam/exam-blueprint.md](../exam/exam-blueprint.md).

### Concept breakdown

- BC-CON-03008 Classification of an expression before differentiating: The outermost operation of an expression decides which differentiation rule opens the work.

- BC-SKL-03026 Classify an expression by its outermost operation: Decide whether the expression is at heart a sum, a product, a quotient, or a composition.
- BC-SKL-03027 Select the differentiation rule that the classification indicates: Match the structure you found to the rule that handles it.
- BC-SKL-03028 Order several differentiation rules within one problem: Work from the outside in so each rule is applied to the right piece.
- BC-SKL-03029 Rewrite an expression algebraically before differentiating: Simplify or rewrite first when that turns a hard rule into an easy one.

### Prerequisites

- BC-PRQ-03001 -> BC-SKL-03026, supporting, [inferred], Prerequisite for Classify an expression by its outermost operation.
- BC-PRQ-03001 -> BC-SKL-03027, supporting, [inferred], Prerequisite for Select the differentiation rule that the classification indicates.
- BC-PRQ-03001 -> BC-SKL-03028, supporting, [inferred], Prerequisite for Order several differentiation rules within one problem.
- BC-PRQ-03006 -> BC-SKL-03029, supporting, [inferred], Prerequisite for Rewrite an expression algebraically before differentiating.
- BC-SKL-03026 -> BC-SKL-03027, hard_prerequisite, [inferred], Classification precedes rule selection.
- BC-SKL-03027 -> BC-SKL-03028, hard_prerequisite, [inferred], Rule selection precedes ordering several rules.
- BC-TOP-0210 -> BC-SKL-03028, supporting, [inferred], Derivatives of the remaining trigonometric functions widen the set of rules to be selected among; the topic id stands in for the Unit 2 skill.

### Required mathematical knowledge

**Classification.** An expression is classified by the operation applied last: a sum, a constant multiple, a product, a quotient, a composition, or a basic named function. That classification selects the opening rule.

**Order of rules.** Nested structure is handled from the outside inward, so each rule acts on the piece the classification assigns to it. The CED unit overview records that students struggle with the order of operations when multiple rules apply (ced:72).

**Rewriting.** An algebraic rewrite that does not change the function may replace a quotient rule by a power rule or remove a composition; the rewrite has to be checked before it is used.

**Notation.** The rule names as they appear in Units 2 and 3: power, constant multiple, sum, product, quotient, chain, inverse function, and inverse trigonometric.

### Representations

Representations in play: BC-REP-01 Symbolic (analytical) expression, BC-REP-04 Verbal description.

Conversions tested: a symbolic expression to a named rule (BC-REP-01 to BC-REP-04), and a verbal statement of a rule to the symbolic step it licenses (BC-REP-04 to BC-REP-01).

### Assessment behaviour

MCQ forms supply an expression whose surface appearance suggests one family and whose structure requires another, and ask for the derivative or for the rule. FRQ forms do not assess this topic on its own; it surfaces as the opening decision inside a differentiation part, and the 2022 Chief Reader report records rule choice driven by the shape of an expression as an observed behaviour (cr-22:21). These items sit in the no-calculator part. Conceptual variants ask only for the rule; computational variants ask for the derivative; justification variants ask the student to say why that rule applies; multi-concept variants need three or more rules in one expression.

### Archetypes

- BC-QA-03009 Selecting the differentiation procedure for a given expression

### Errors and misconceptions

- BC-ERR-03019 Rule chosen from the surface appearance of the expression
- BC-ERR-03002 One layer of a multi-layer composite left undifferentiated
- BC-ERR-03006 Product or quotient rule omitted when a composite is one factor
- BC-ERR-03020 Unnecessary simplification introduces an algebra error
- BC-MIS-03012 The differentiation rule follows from the look of the expression, severity high

### Diagnostic signals

- BC-SIG-03011 Correct rules applied in the wrong order, mastery state partially_mastered
- BC-SIG-03012 Correct derivative spoiled by a later simplification, mastery state partially_mastered

### Adaptive metadata summary

Skills in this topic carry calculator relevance none. Remediation targets named across the topic: BC-PRQ-03001, BC-PRQ-03006, BC-SKL-03026, BC-SKL-03027. Every skill record carries the full seven key adaptive block in data/staging/unit-03.skills.json. [inferred]

## 3.6 Calculating Higher-Order Derivatives

### Official mapping

Topic id BC-TOP-0306, CED code 3.6, name Calculating Higher-Order Derivatives, scope shared, CED page 80. [verified] (ced:80)

- BC-LO-FUN-3F (FUN-3.F): Determine higher order derivatives of a function.
  - BC-EK-FUN-3F1 (FUN-3.F.1): "Differentiating f' produces the second derivative f'', provided the derivative of f' exists; repeating this process produces higher-order derivatives of f."
  - BC-EK-FUN-3F2 (FUN-3.F.2): "Higher-order derivatives are represented with a variety of notations."

Suggested practice skills: BC-MPS-1E (Practice skill 1.E). Weighting pointer: [../exam/exam-blueprint.md](../exam/exam-blueprint.md).

### Concept breakdown

- BC-CON-03009 Repeated differentiation: Differentiating a derivative gives the next derivative, and the process repeats as long as each derivative exists.
- BC-CON-03010 Notation for higher-order derivatives: The same higher derivative can be written in prime notation or in Leibniz notation, and the two must be read interchangeably.

- BC-SKL-03030 Differentiate a first derivative to obtain the second derivative: Differentiate what you already differentiated once.
- BC-SKL-03031 Produce a third or higher order derivative by repeating differentiation: Keep differentiating, one order at a time.
- BC-SKL-03032 Read and write higher-order derivative notation: Move between prime notation and Leibniz notation without changing the meaning.
- BC-SKL-03033 Differentiate a derivative expression that still contains y: Differentiate the expression for dy/dx, using the product and chain rules on the y parts.
- BC-SKL-03034 Evaluate a second derivative at a point using dy/dx there: Work out dy/dx at the point first, then substitute both coordinates and that slope.

### Prerequisites

- BC-PRQ-03005 -> BC-SKL-03030, supporting, [inferred], Prerequisite for Differentiate a first derivative to obtain the second derivative.
- BC-PRQ-03005 -> BC-SKL-03031, supporting, [inferred], Prerequisite for Produce a third or higher order derivative by repeating differentiation.
- BC-PRQ-03005 -> BC-SKL-03032, supporting, [inferred], Prerequisite for Read and write higher-order derivative notation.
- BC-PRQ-03005 -> BC-SKL-03033, supporting, [inferred], Prerequisite for Differentiate a derivative expression that still contains y.
- BC-PRQ-03002 -> BC-SKL-03033, supporting, [inferred], Prerequisite for Differentiate a derivative expression that still contains y.
- BC-PRQ-03006 -> BC-SKL-03034, supporting, [inferred], Prerequisite for Evaluate a second derivative at a point using dy/dx there.
- BC-SKL-03030 -> BC-SKL-03031, hard_prerequisite, [inferred], Each order builds on the one before.
- BC-SKL-03008 -> BC-SKL-03033, hard_prerequisite, [verified], The second derivative of an implicit relation needs the product rule inside the implicit differentiation (sg-25:20).
- BC-SKL-03011 -> BC-SKL-03034, hard_prerequisite, [verified], The value of dy/dx at the point is substituted into the second derivative (sg-25:20).
- BC-SKL-03033 -> BC-SKL-03034, hard_prerequisite, [inferred], The expression must exist before it is evaluated.
- BC-TOP-0202 -> BC-SKL-03030, hard_prerequisite, [inferred], Higher-order differentiation repeats the definition and notation of the derivative; the topic id stands in for the Unit 2 skill.

### Required mathematical knowledge

**Repeated differentiation.** Hypotheses: the derivative of f prime exists. Conclusion: that derivative is f double prime, and repeating the process produces higher-order derivatives of f, which is BC-EK-FUN-3F1 in full.

**Notation.** For y equal to f of x, the second derivative is written d squared y over d x squared, f double prime of x, or y double prime, and the nth derivative is written d to the n y over d x to the n or f superscript n of x (BC-EK-FUN-3F2). The verbatim text of BC-EK-FUN-3F2 continues with the notation list; the quotation above is truncated at the end of its first sentence because the cached page renders the symbols imperfectly (ced:80).

**Second derivatives of implicit relations.** When the first derivative is an expression in both variables, differentiating it again needs the product rule on mixed terms and the chain rule on terms in the dependent variable, so dy/dx reappears and must be replaced by its value before a number is reported (sg-25:20).

**Evaluation order.** A numerical second derivative at a point needs the coordinates of the point and the value of the first derivative there, in that order (sg-25:20).

### Representations

Representations in play: BC-REP-01 Symbolic (analytical) expression, BC-REP-04 Verbal description, BC-REP-06 Differential equation.

Conversions tested: a differential equation supplying the first derivative to a second derivative expression (BC-REP-06 to BC-REP-01), and prime notation to Leibniz notation (BC-REP-01 to BC-REP-04).

### Assessment behaviour

MCQ forms ask for a second or third derivative of a formula, or for the meaning of a notation. FRQ forms open a Taylor polynomial question or a differential equation question with a second derivative at a point: the 2025 BC question supplies dy/dx as a differential equation in both variables and scores the product rule, the chain rule, and the value separately (sg-25:20). These parts sit in the no-calculator part. Conceptual variants ask what operation produces the next derivative; computational variants ask for the expression; interpretation variants ask what the notation names; multi-concept variants continue into a Taylor polynomial or a concavity conclusion.

### Archetypes

- BC-QA-03008 Higher-order derivative of a function or of a derivative expression

### Errors and misconceptions

- BC-ERR-03021 Differentiation stopped one order short of the order requested
- BC-ERR-03022 Higher-order derivative notation written incorrectly
- BC-ERR-03008 Product rule omitted on a term containing both variables
- BC-ERR-03023 First derivative value not substituted into the second derivative
- BC-ERR-03011 Only one coordinate substituted into dy/dx
- BC-MIS-03013 A higher derivative is a different kind of object, severity medium
- BC-MIS-03014 Derivative notation is decorative, severity medium
- BC-MIS-03005 A short mixed term is a single symbol, severity high
- BC-MIS-03006 dy/dx is a number rather than an expression in both variables, severity medium

### Diagnostic signals

- BC-SIG-03013 Differentiation stops one order short, mastery state partially_mastered
- BC-SIG-03014 Notation mixed within a single line, mastery state partially_mastered
- BC-SIG-03015 Product and chain rules correct with the first derivative value omitted, mastery state partially_mastered

### Adaptive metadata summary

Skills in this topic carry calculator relevance none. Remediation targets named across the topic: BC-PRQ-03005, BC-SKL-03008, BC-SKL-03030, BC-SKL-03033. Every skill record carries the full seven key adaptive block in data/staging/unit-03.skills.json. [inferred]

## Cross-unit connections

Cross-unit edges use BC-TOP ids as the node on the other unit's side, because no skills for Units 1, 2, 4, and 5 exist in data/skills.json at the time this file was written; the `notes` field on each edge in data/staging/unit-03.edges.csv describes the skill that the topic id stands in for. [inferred]

### What Unit 3 depends on

**Unit 2 derivative rules.** Every chain rule application needs an outer derivative from Unit 2. BC-SKL-03002 rests on the power rule (BC-TOP-0205) and on the derivatives of the sine, cosine, exponential, and natural logarithm functions (BC-TOP-0207). BC-SKL-03006 rests on the product rule (BC-TOP-0208) and the quotient rule (BC-TOP-0209). BC-SKL-03008 rests on the product rule, which BC-EK-CHA-3D2 names explicitly as needed when variables are differentiated with respect to a common variable. BC-SKL-03030 rests on the definition and notation of the derivative (BC-TOP-0202), and BC-SKL-03028 draws on the derivatives of the remaining trigonometric functions (BC-TOP-0210) to widen the set of rules that must be chosen among.

**Unit 2 differentiability.** BC-SKL-03005 reads a slope off a graph, so it depends on knowing where a derivative fails to exist (BC-TOP-0204); a corner in a supplied graph is the discriminating feature of BC-QV-03003-01.

**Unit 1 limits.** No Unit 3 skill in this decomposition depends directly on a limit skill. The derivative rules the unit composes were themselves established from limits in Units 1 and 2. [inferred]

### What depends on Unit 3

**Unit 4.** The chain rule is the stated basis of related rates in BC-EK-CHA-3D1, and the product rule inside an implicit differentiation is named in BC-EK-CHA-3D2, so BC-TOP-0404 and BC-TOP-0405 depend on BC-SKL-03002, BC-SKL-03007, BC-SKL-03008, BC-SKL-03009, and BC-SKL-03010. The tangent line approximation at BC-TOP-0406 depends on BC-SKL-03011 whenever the curve is given implicitly, which is the structure the Chief Reader reports describe for 2024 and 2025 (cr-24:17, crabbc-25:24). The L'Hospital rule topic BC-TOP-0407 depends on BC-SKL-03028 because the derivatives of the numerator and the denominator are taken separately and each may need its own rule.

**Unit 5.** Concavity and the second derivative test at BC-TOP-0506 and BC-TOP-0507 depend on BC-SKL-03030, and exploring the behaviour of implicit relations at BC-TOP-0512 depends on BC-SKL-03010, BC-SKL-03012, and BC-SKL-03013.

**Unit 6.** Substitution reverses the chain rule and the Fundamental Theorem of Calculus with a composite upper limit applies it, so BC-SKL-06019 and BC-SKL-06047 depend on BC-SKL-03002, and BC-SKL-06043, the inverse trigonometric antiderivative skill, depends on BC-SKL-03021 and BC-SKL-03022.

**Units 7, 9, and 10.** Separation of variables and the parametric derivative both differentiate a relation in which one variable depends on another, and a Taylor polynomial is built from higher-order derivatives, so BC-TOP-0706, BC-TOP-0902, and BC-TOP-1011 depend on BC-SKL-03031 and BC-SKL-03033. The 2025 BC question that opens with a second derivative from a differential equation and continues into a Taylor polynomial is the worked instance of that dependency (sg-25:20).

## Archetype summary

Nine archetypes with twenty seven variants are recorded in data/staging/unit-03.archetypes.json. Variant dimensions used are representation, reasoning direction, notation, context, and calculator. [verified] (sg-25:20, sg-25:2, cr-22:21, cr-23:22, cr-24:17, crabbc-25:24)

| Archetype | Name | Scope | Calculator | Official parts read |
|---|---|---|---|---|
| BC-QA-03001 | Chain rule derivative of a composite given symbolically | shared | no_calculator | 2025 Q5(A) awards a chain rule point inside a larger task |
| BC-QA-03002 | Composite derivative evaluated from a table of values | shared | either | none in 2023 to 2025 BC |
| BC-QA-03003 | Composite derivative read from graphs of the component functions | shared | no_calculator | none in 2023 to 2025 BC |
| BC-QA-03004 | Implicit differentiation producing or verifying dy/dx | shared | no_calculator | 2023 AB Q6(a), 2024 AB Q5, 2025 AB Q6 part A, via the Chief Reader reports |
| BC-QA-03005 | Horizontal or vertical tangent on an implicitly defined curve | shared | no_calculator | 2023 AB Q6(b) and (c), 2024 AB Q5(b) and (c), 2025 AB Q6 part C, via the Chief Reader reports |
| BC-QA-03006 | Derivative of an inverse function at a point | shared | either | none in 2023 to 2025 BC |
| BC-QA-03007 | Inverse trigonometric derivative with an inner function | shared | either | 2025 Q1 supplies the derivative of an inverse tangent model |
| BC-QA-03008 | Higher-order derivative of a function or of a derivative expression | shared | no_calculator | 2025 Q5(A) |
| BC-QA-03009 | Selecting the differentiation procedure for a given expression | shared | no_calculator | none in 2023 to 2025 BC |

Four archetypes, BC-QA-03002, BC-QA-03003, BC-QA-03006, and BC-QA-03009, have no matching part in the 2023 to 2025 BC free response questions and are tagged inferred or single-source; their scoring patterns are drawn from the nearest analogous parts and from the CED text rather than from a rubric for that exact task. BC-QA-03004 and BC-QA-03005 are grounded in the Chief Reader reports, which describe the AB questions in which the tasks appeared; the underlying content is shared with BC.

## Misconception summary

Fourteen misconceptions are recorded in data/staging/unit-03.misconceptions.json against twenty three observed errors in data/staging/unit-03.errors.json. The mapping is many to many: an error lists every misconception that could produce it together with non-conceptual causes such as an arithmetic slip, a misread, or time pressure, and every misconception carries rival misconceptions and a discriminating probe. [verified] (cr-22:21, cr-23:23, cr-24:18, crabbc-25:25, sg-25:20)

| Misconception | Severity | Rivals | Discriminating probe |
|---|---|---|---|
| BC-MIS-03001 Differentiation acts only on the outermost shell | high | BC-MIS-03002, BC-MIS-03012 | Ask the student to differentiate the same outer function with a linear inside and with a quadratic inside and to compare the two answers. |
| BC-MIS-03002 The chain rule factors are evaluated at the same input | high | BC-MIS-03001 | Give a table in which the inner output is itself a listed input and ask where the outer derivative should be read. |
| BC-MIS-03003 Leibniz notation is a fraction that cancels | medium | BC-MIS-03014 | Ask the student to say what du/dx measures in the situation before any cancellation is written. |
| BC-MIS-03004 In an equation, y is an independent symbol | high | BC-MIS-03005 | Ask the student what dy/dx would mean if y did not depend on x. |
| BC-MIS-03005 A short mixed term is a single symbol | high | BC-MIS-03004, BC-MIS-03012 | Ask the student to name the two factors of the mixed term before differentiating it. |
| BC-MIS-03006 dy/dx is a number rather than an expression in both variables | medium | BC-MIS-03004 | Ask the student for the slope at two different points of the same curve with the same x coordinate. |
| BC-MIS-03007 A tangent condition is a condition on dy/dx alone | high | BC-MIS-03006 | Ask the student to verify that the candidate point satisfies the original equation, as a separate step. |
| BC-MIS-03008 The inverse is evaluated wherever the original is | high | BC-MIS-03009 | Ask the student to write the ordered pair on the original function that corresponds to the point on the inverse. |
| BC-MIS-03009 The inverse derivative rule has no hypotheses | medium | BC-MIS-03008 | Ask what the tangent line to the inverse looks like at a point where the original curve has a horizontal tangent. |
| BC-MIS-03010 The inverse trigonometric formulas are interchangeable | medium | BC-MIS-03011 | Ask the student to say which of the three derivatives has a square root and why. |
| BC-MIS-03011 An inverse trigonometric derivative cannot be derived | low | BC-MIS-03010 | Ask the student to start from the equation relating the sine of an angle to the variable and to recover the derivative. |
| BC-MIS-03012 The differentiation rule follows from the look of the expression | high | BC-MIS-03001, BC-MIS-03005 | Ask the student to state the last operation performed when the expression is evaluated at a number. |
| BC-MIS-03013 A higher derivative is a different kind of object | medium | BC-MIS-03014 | Ask the student to say what operation turns the first derivative into the second. |
| BC-MIS-03014 Derivative notation is decorative | medium | BC-MIS-03003, BC-MIS-03013 | Ask the student to say aloud what the expression d/dx of y means and how it differs from dy/dx. |

The highest severity cluster is the one the Chief Reader reports document directly: treating y as an independent symbol and reading a short mixed term as a single object, which together account for the responses that lost the completely correct implicit differentiation point in 2023, 2024, and 2025 (cr-23:23, cr-24:18, crabbc-25:25). The second cluster is the tangent condition read in isolation from the curve, which the 2023 and 2024 reports record as a failure to connect dy/dx with the defining equation (cr-23:23, cr-24:18).

## Unresolved

- No Unit 3 topic is the sole subject of a BC free response question in 2023 to 2025. The implicit differentiation and related rates question sat at AB6 in 2023, AB5 in 2024, and AB6 in 2025, and is documented here from the Chief Reader reports rather than from a BC scoring guideline. Whether an equivalent BC part exists in the multiple choice sections cannot be established from the material indexed so far. [uncertain]
- The anchor text of BC-EK-FUN-3F2 in data/curriculum.json continues past the sentence quoted in topic 3.6 with a list of notations whose symbols the cached CED page renders imperfectly. The quotation here is truncated at a sentence boundary rather than reproduced in full. [verified] (ced:80)
- Topic 3.5 has no learning objective or essential knowledge statement, so its four skills are grounded on the topic page statement of intent alone. Their evidence tags are verified against ced:79, but no essential knowledge text constrains their wording. [verified] (ced:79)
- The archetypes with no official part read, BC-QA-03002, BC-QA-03003, BC-QA-03006, and BC-QA-03009, have inferred scoring patterns. These should be revisited when the official multiple choice material is indexed. [uncertain]
- Misconception records are tagged inferred unless a Chief Reader report or a scoring guideline names the behaviour directly. No misconception literature is cited, because none could be confirmed from the sources available in this project's cache. [inferred]

<!-- generated:official-evidence:start -->

## Official evidence index [verified]

Generated from data/frq_records.json and data/mcq_records.json. Every record cites its cached document and page; counts are observations over the indexed years only, not predictions. FRQ part records with BC-UNIT-03 as primary or secondary unit: 22. Public sample MCQ records tagged to this unit: 5.

| FRQ record | Role | Calculator | Archetype | Skills (first six) | Points | Point types |
|---|---|---|---|---|---|---|
| BC-FRQ-2013-Q3-D | secondary | no_calculator | BC-QA-02007 | BC-SKL-02033, BC-SKL-03002, BC-SKL-02029, BC-SKL-04014 | 2 | BC-PT-99023, BC-PT-99004 |
| BC-FRQ-2013-Q4-D | primary | no_calculator | BC-QA-03001 | BC-SKL-03002, BC-SKL-03005, BC-SKL-03006, BC-SKL-02012 | 3 | BC-PT-99023, BC-PT-99004 |
| BC-FRQ-2014-Q2-C | secondary | calculator | BC-QA-99006 | BC-SKL-09030, BC-SKL-03002, BC-SKL-03027 | 2 | BC-PT-99005, BC-PT-99004 |
| BC-FRQ-2014-Q3-D | primary | no_calculator | BC-QA-03001 | BC-SKL-03002, BC-SKL-03005, BC-SKL-03006 | 3 | BC-PT-99023, BC-PT-99004 |
| BC-FRQ-2015-Q4-B | secondary | no_calculator | BC-QA-07010 | BC-SKL-03030, BC-SKL-03033, BC-SKL-05030, BC-SKL-07018 | 2 | BC-PT-99027, BC-PT-99063 |
| BC-FRQ-2018-Q4-D | secondary | no_calculator | BC-QA-04006 | BC-SKL-04017, BC-SKL-04019, BC-SKL-04024, BC-SKL-04026, BC-SKL-02039, BC-SKL-03002 | 0 |  |
| BC-FRQ-2019-Q1-D | secondary | calculator | BC-QA-04005 | BC-SKL-04014, BC-SKL-04005, BC-SKL-03030, BC-SKL-05014 | 2 | BC-PT-99027, BC-PT-99010 |
| BC-FRQ-2019-Q4-A | secondary | no_calculator | BC-QA-04006 | BC-SKL-04018, BC-SKL-04019, BC-SKL-04023, BC-SKL-04025, BC-SKL-04027 | 2 | BC-PT-99023, BC-PT-99006 |
| BC-FRQ-2019-Q4-B | secondary | no_calculator | BC-QA-07010 | BC-SKL-07018, BC-SKL-03030, BC-SKL-03034, BC-SKL-05014 | 3 | BC-PT-99027, BC-PT-99023, BC-PT-99010 |
| BC-FRQ-2019-Q5-A | secondary | no_calculator | BC-QA-02008 | BC-SKL-02039, BC-SKL-03002, BC-SKL-02012, BC-SKL-05001 | 3 | BC-PT-99005, BC-PT-99005, BC-PT-99004 |
| BC-FRQ-2022-Q2-B | secondary | calculator | BC-QA-09004 | BC-SKL-09023, BC-SKL-09017, BC-SKL-09028, BC-SKL-09015 | 3 | BC-PT-99050, BC-PT-99052, BC-PT-99052 |
| BC-FRQ-2022-Q4-A | secondary | no_calculator | BC-QA-04002 | BC-SKL-02014, BC-SKL-02016, BC-SKL-02015, BC-SKL-04004, BC-SKL-03030 | 2 | BC-PT-99005, BC-PT-99006 |
| BC-FRQ-2022-Q4-D | secondary | no_calculator | BC-QA-04006 | BC-SKL-04018, BC-SKL-04019, BC-SKL-04020, BC-SKL-04023, BC-SKL-04024 | 3 | BC-PT-99022, BC-PT-99023, BC-PT-99004 |
| BC-FRQ-2023-Q1-D | secondary | calculator | BC-QA-04001 | BC-SKL-04002, BC-SKL-04005, BC-SKL-04014, BC-SKL-02018, BC-SKL-04015 | 2 | BC-PT-99004, BC-PT-99008 |
| BC-FRQ-2023-Q2-A | secondary | calculator | BC-QA-09004 | BC-SKL-09015, BC-SKL-09017, BC-SKL-09028, BC-SKL-03002 | 2 | BC-PT-99052, BC-PT-99005 |
| BC-FRQ-2023-Q6-A | secondary | no_calculator | BC-QA-10010 | BC-SKL-02036, BC-SKL-03002, BC-SKL-03031, BC-SKL-10043, BC-SKL-10044, BC-SKL-10046 | 4 | BC-PT-99022, BC-PT-99027, BC-PT-99035, BC-PT-99036 |
| BC-FRQ-2024-Q4-C | secondary | no_calculator | BC-QA-06012 | BC-SKL-06018, BC-SKL-06035, BC-SKL-03030, BC-SKL-03032, BC-SKL-06034 | 4 | BC-PT-99024, BC-PT-99004, BC-PT-99004, BC-PT-99004 |
| BC-FRQ-2024-Q5-A | secondary | no_calculator | BC-QA-06012 | BC-SKL-06018, BC-SKL-06021, BC-SKL-03002 | 2 | BC-PT-99024, BC-PT-99004 |
| BC-FRQ-2025-Q2-A | secondary | calculator | BC-QA-09009 | BC-SKL-09030, BC-SKL-03002, BC-SKL-02018 | 1 | BC-PT-99005 |
| BC-FRQ-2025-Q2-D | secondary | calculator | BC-QA-09010 | BC-SKL-09031, BC-SKL-09032, BC-SKL-04019, BC-SKL-04024 | 2 | BC-PT-99049, BC-PT-99004 |
| BC-FRQ-2025-Q5-A | primary | no_calculator | BC-QA-03008 | BC-SKL-02036, BC-SKL-03002, BC-SKL-03033, BC-SKL-03034, BC-SKL-07018 | 3 | BC-PT-99022, BC-PT-99023, BC-PT-99027 |
| BC-FRQ-2026-Q2-B | secondary | calculator | BC-QA-99001 | BC-SKL-09033, BC-SKL-09002, BC-SKL-09003, BC-SKL-03002 | 3 | BC-PT-99049, BC-PT-99004, BC-PT-99004 |

| MCQ record | Calculator | Archetype | Skills |
|---|---|---|---|
| BC-MCQ-CED-004 | no_calculator | BC-QA-03004 | BC-SKL-03009, BC-SKL-03008, BC-SKL-03010 |
| BC-MCQ-SAMPLE-007 | no_calculator | BC-QA-06012 | BC-SKL-06019, BC-SKL-06018, BC-SKL-03002 |
| BC-MCQ-PE2012-001 | no_calculator | BC-QA-03001 | BC-SKL-03001, BC-SKL-03002, BC-SKL-02032 |
| BC-MCQ-PE2012-007 | no_calculator | BC-QA-03007 | BC-SKL-03022, BC-SKL-03009, BC-SKL-02034 |
| BC-MCQ-PE2012-038 | calculator | BC-QA-04006 | BC-SKL-04019, BC-SKL-04023, BC-SKL-03002 |

<!-- generated:official-evidence:end -->
