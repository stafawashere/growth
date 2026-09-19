---
title: Scoring Point Taxonomy
research_date: 2026-09-19
status: draft
purpose: The derived catalogue of AP Calculus BC scoring point types, one section per family, with the rubric wording each field came from.
---

# Scoring Point Taxonomy

Derived from the official scoring guidelines cached as sg-19, sg-21, sg-22, sg-23, sg-24, sg-25 and sg-26, read page by page. Facts live in `../../data/scoring_points.json`; this file is a view over that registry.

Citations use the form `sg-25:11`, meaning the cached document sg-25 at page 11. Rubric instances use `sg-25:11 Q3(a) P1`. From sg-25 onward the guidelines number points P1 to P9 across a whole question, so P1 is the document's own label. In sg-19 through sg-24 the guidelines number points inside a part and label them ordinally, so `P1` there means the first point of that part as the model solution orders it.

Three candidate families were rejected during derivation. Limits of integration are never a point of their own: sg-25:7 states the limits and the outer factor are assessed in the answer point rather than in the integrand points, sg-26:19 states the limits need only be numerical for the arc length form point, and sg-22:18 states a definite integral with incorrect bounds earns neither the integral point nor the answer point. A constant of integration is not a point of its own either: sg-25:14 awards the antiderivative point with or without it, and it becomes scoreable only when bundled with the initial condition inside a separable differential equation (sg-26:13). A standalone equation or model setup family also failed to appear; every setup point in the corpus is tied to a named structure such as an average value formula (sg-25:2), a Riemann sum form (sg-26:3) or an average rate of change (sg-26:2).

## BC-PT-99001 Definite integral expression with correct limits [verified]

Scope shared. Sources sg-22:2, sg-26:4, sg-24:3, sg-22:17, sg-23:7.

- Earns: A definite integral whose limits match the requested interval and whose integrand matches the requested quantity, with or without the differential (sg-26:4, sg-22:2).
- Does not earn: An unsupported numerical value, or a definite integral whose bounds are wrong (sg-22:18).
- Requires previous work: no
- Setup alone earns: yes
- Simplification required: no
- Units required: no
- Interpretation required: no
- Justification required: no
- Hypotheses required: no
- Notation: Differential may be omitted; sg-22:2 accepts dx written for dt. sg-23:8 treats a missing differential as recoverable for this point but restricts later eligibility.
- Precision: Not a reported-value point, so the three-decimal rule does not apply.
- Dependency: Independent of other points in the rubrics reviewed.
- Eligibility after an error: sg-22:18 states a definite integral with incorrect bounds earns neither this point nor the answer point; sg-22:8 states a definite integral with incorrect limits is not eligible for the answer point.
- Rubric instances: sg-22:2 Q1(a) P1; sg-26:4 Q1(C) P6; sg-24:3 Q1(c) P1; sg-22:17 Q5(a) P1; sg-23:7 Q2(c) P2
- Notes: This family absorbs what would otherwise be a separate limits-of-integration family. Limits are scored inside the integral point or inside the answer point, never as a point of their own.

## BC-PT-99002 Integrand only, limits assessed elsewhere [verified]

Scope shared. Sources sg-25:7, sg-25:14, sg-23:16, sg-22:8, sg-26:19.

- Earns: A correct integrand inside an integral, whether or not the limits and outside constants are right (sg-25:7, sg-26:19).
- Does not earn: An integrand built from the wrong function, or an integrand presented with no integral sign (sg-25:7).
- Requires previous work: no
- Setup alone earns: yes
- Simplification required: no
- Units required: no
- Interpretation required: no
- Justification required: no
- Hypotheses required: no
- Notation: Differential optional (sg-25:7, sg-25:14). sg-26:19 requires the limits to be numerical but not correct.
- Precision: Not a reported-value point, so the three-decimal rule does not apply.
- Dependency: sg-25:7 states the limits and the factor one half are assessed in the answer point, not in the integrand points.
- Eligibility after an error: sg-25:7 special case: an indefinite integral with a correct integrand loses the r-squared point, earns the integrand point, and stays eligible for the answer point.
- Rubric instances: sg-25:7 Q2(b) P3; sg-25:14 Q3(d) P7; sg-23:16 Q5(a) P1; sg-22:8 Q2(c) P1; sg-26:19 Q5(B) P3

## BC-PT-99003 Antiderivative [verified]

Scope shared. Sources sg-25:14, sg-26:18, sg-26:20, sg-23:17, sg-22:19.

- Earns: A correct antiderivative of the presented integrand, with or without the constant of integration (sg-25:14).
- Does not earn: An antiderivative of the wrong form, or a jump from integral to value with no antiderivative shown (sg-26:18).
- Requires previous work: no
- Setup alone earns: n/a
- Simplification required: no
- Units required: no
- Interpretation required: no
- Justification required: no
- Hypotheses required: no
- Notation: No special notation requirement stated in the rubrics reviewed.
- Precision: Not a reported-value point, so the three-decimal rule does not apply.
- Dependency: sg-25:14 and sg-26:20 both state the answer point requires this point first.
- Eligibility after an error: sg-23:17 allows an antiderivative of the right form with a wrong constant to earn this point while blocking the answer point; sg-21:11 keeps u-substitution work with unconverted limits eligible for this point.
- Rubric instances: sg-25:14 Q3(d) P8; sg-26:18 Q5(A) P1; sg-26:20 Q5(D) P8; sg-23:17 Q5(b) P2; sg-22:19 Q5(c) P2

## BC-PT-99004 Answer with or without supporting work [verified]

Scope shared. Sources sg-25:3, sg-25:7, sg-26:4, sg-26:21, sg-26:18.

- Earns: The correct value on its own, with no supporting work required (sg-25:3, sg-26:4).
- Does not earn: A value outside the accepted precision, or a value inconsistent with a required earlier step where the rubric imposes one.
- Requires previous work: no
- Setup alone earns: no
- Simplification required: no
- Units required: no
- Interpretation required: no
- Justification required: no
- Hypotheses required: no
- Notation: No special notation requirement stated in the rubrics reviewed.
- Precision: A reported decimal answer must be accurate to three places after the decimal point, rounded or truncated; at most one point per question is lost to inappropriate rounding (sg-25:2, sg-26:2). sg-26:4 also accepts a stated rounding to the nearest integer and several truncations.
- Dependency: Independent of other points in the rubrics reviewed.
- Eligibility after an error: sg-25:3 treats incorrect or unclear communication between the integral and the answer as scratch work, so bad linkage does not cost this point.
- Rubric instances: sg-25:3 Q1(a) P2; sg-25:7 Q2(b) P4; sg-26:4 Q1(C) P7; sg-26:21 Q6(A) P2; sg-26:18 Q5(A) P2

## BC-PT-99005 Answer with supporting work or setup shown [verified]

Scope shared. Sources sg-25:4, sg-25:8, sg-25:23, sg-26:11, sg-26:2, sg-22:6.

- Earns: The correct value together with the setup the prompt demanded, such as a difference and a quotient from a table or an equation that produces the value (sg-26:2, sg-25:4).
- Does not earn: An unsupported value (sg-23:10, sg-22:9), or a setup with no value (sg-26:2).
- Requires previous work: yes
- Setup alone earns: no
- Simplification required: no
- Units required: no
- Interpretation required: no
- Justification required: no
- Hypotheses required: no
- Notation: sg-22:6 withholds this point for an equation of the form function equals constant, such as a derivative expression set equal to a number without evaluation.
- Precision: A reported decimal answer must be accurate to three places after the decimal point, rounded or truncated; at most one point per question is lost to inappropriate rounding (sg-25:2, sg-26:2).
- Dependency: Independent of other points in the rubrics reviewed.
- Eligibility after an error: sg-26:11 banks this point once a correct unsimplified expression appears, so later simplification errors do not remove it.
- Rubric instances: sg-25:4 Q1(b) P4; sg-25:8 Q2(c) P7; sg-25:23 Q5(D) P9; sg-26:11 Q3(B) P2; sg-26:2 Q1(A) P1; sg-22:6 Q2(a) P1

## BC-PT-99006 Units [verified]

Scope shared. Sources sg-25:11, sg-26:2, sg-22:13, sg-24:2.

- Earns: Correct units, whether or not they are attached to a numerical value (sg-25:11, sg-26:2); equivalent compact forms such as birds per day squared are accepted (sg-26:2).
- Does not earn: Units with no value present at all where the rubric ties them to a presented value (sg-22:13).
- Requires previous work: no
- Setup alone earns: n/a
- Simplification required: no
- Units required: yes
- Interpretation required: no
- Justification required: no
- Hypotheses required: no
- Notation: No special notation requirement stated in the rubrics reviewed.
- Precision: Not a reported-value point, so the three-decimal rule does not apply.
- Dependency: sg-22:13 allows the units point with an incorrect approximation but not with no presented value.
- Eligibility after an error: No eligibility restriction stated in the rubrics reviewed.
- Rubric instances: sg-25:11 Q3(a) P2; sg-26:2 Q1(A) P2; sg-22:13 Q4(a) P2; sg-24:2 Q1(a) P2
- Notes: Units are scored only where the prompt asks for them. sg-21:11, sg-22:15 and sg-22:16 state units are not required and are not read in those parts, and sg-26:4 states units are not considered in scoring.

## BC-PT-99007 Interpretation of an accumulated quantity with units and interval [verified]

Scope shared. Sources sg-23:2, sg-26:3, sg-24:3.

- Earns: A sentence naming the accumulated quantity in context together with the time or spatial interval (sg-26:3, sg-23:2).
- Does not earn: An interpretation that omits the interval, or that restates the integral without naming the quantity (sg-26:3).
- Requires previous work: no
- Setup alone earns: n/a
- Simplification required: no
- Units required: varies
- Interpretation required: yes
- Justification required: no
- Hypotheses required: no
- Notation: No special notation requirement stated in the rubrics reviewed.
- Precision: Not a reported-value point, so the three-decimal rule does not apply.
- Dependency: sg-26:3 states this point can be earned whether or not the sum and approximation points were earned.
- Eligibility after an error: No eligibility restriction stated in the rubrics reviewed.
- Rubric instances: sg-23:2 Q1(a) P1; sg-26:3 Q1(B) P5; sg-24:3 Q1(b) P3
- Notes: sg-26:3 says the response need not include units of time or the location name, so the unit demand varies by year.

## BC-PT-99008 Interpretation of a derivative value in context with units [single-source]

Scope shared. Sources sg-23:4, sg-21:2, sg-21:3.

- Earns: A sentence giving the rate of change of the named quantity, its value, its units, and the instant it applies to (sg-21:3, sg-23:4).
- Does not earn: An interpretation whose sign language contradicts the presented value, such as decreasing at a rate of a negative number (sg-23:4).
- Requires previous work: yes
- Setup alone earns: n/a
- Simplification required: no
- Units required: yes
- Interpretation required: yes
- Justification required: no
- Hypotheses required: no
- Notation: No special notation requirement stated in the rubrics reviewed.
- Precision: Not a reported-value point, so the three-decimal rule does not apply.
- Dependency: sg-23:4 and sg-21:3 both require some presented numerical value for the derivative before this point is available.
- Eligibility after an error: No eligibility restriction stated in the rubrics reviewed.
- Rubric instances: sg-23:4 Q1(d) P2; sg-21:2 Q1(a) P2
- Notes: Only two rubric instances in the documents read, so tagged single-source.

## BC-PT-99009 Interpretation of an integral as an arc length over an interval [single-source]

Scope BC_only. Sources sg-24:16.

- Earns: Naming the integral as the arc length of the given curve, and naming the interval it is taken over; the rubrics split these as two points (sg-24:16).
- Does not earn: Naming the quantity as a distance travelled or an area rather than the length of the graph (sg-24:16).
- Requires previous work: no
- Setup alone earns: n/a
- Simplification required: no
- Units required: no
- Interpretation required: yes
- Justification required: no
- Hypotheses required: no
- Notation: No special notation requirement stated in the rubrics reviewed.
- Precision: Not a reported-value point, so the three-decimal rule does not apply.
- Dependency: Independent of other points in the rubrics reviewed.
- Eligibility after an error: No eligibility restriction stated in the rubrics reviewed.
- Rubric instances: sg-24:16 Q5(b) P1; sg-24:16 Q5(b) P2
- Notes: One document only in the corpus read, so tagged single-source.

## BC-PT-99010 Justification by sign analysis of a derivative [verified]

Scope shared. Sources sg-25:5, sg-25:9, sg-25:19, sg-22:12.

- Earns: A statement that the derivative is positive on one side and negative on the other, closed by a global claim about the whole interval (sg-25:5, sg-25:9).
- Does not earn: A local argument only, such as a bare First or Second Derivative Test with no statement that the critical point is the only one on the interval (sg-25:5, sg-22:12).
- Requires previous work: no
- Setup alone earns: n/a
- Simplification required: no
- Units required: no
- Interpretation required: no
- Justification required: yes
- Hypotheses required: no
- Notation: No special notation requirement stated in the rubrics reviewed.
- Precision: Not a reported-value point, so the three-decimal rule does not apply.
- Dependency: sg-25:5 and sg-25:9 keep the answer point available to a response that fails this point with a local or incorrect global argument.
- Eligibility after an error: sg-22:12 states that a local argument must also state the critical point is the only one, otherwise the justification point is lost while the answer stands.
- Rubric instances: sg-25:5 Q1(D) P8; sg-25:9 Q2(C) P6; sg-25:19 Q4(d) P8; sg-22:12 Q3(d) P2

## BC-PT-99011 Justification by candidates test [verified]

Scope shared. Sources sg-25:5, sg-25:19, sg-23:15, sg-22:4.

- Earns: A global argument that evaluates the function at every interior critical point and at both endpoints, with the evaluations correct to the stated precision (sg-25:5, sg-25:19).
- Does not earn: A candidates table missing an endpoint (sg-23:15), containing an evaluation error (sg-23:15), or listing extra x-values (sg-25:19).
- Requires previous work: no
- Setup alone earns: n/a
- Simplification required: no
- Units required: no
- Interpretation required: no
- Justification required: yes
- Hypotheses required: no
- Notation: No special notation requirement stated in the rubrics reviewed.
- Precision: sg-25:5 and sg-25:9 require candidate evaluations correct to the first digit after the decimal, rounded or truncated; sg-22:5 allows up to three decimals or correctly rounded integers.
- Dependency: sg-25:19 allows candidate values to be imported from an earlier part, and lets the answer point follow the imported values.
- Eligibility after an error: sg-22:5 states a correct justification earns its point even when the answer point is lost to a decimal presentation error.
- Rubric instances: sg-25:5 Q1(D) P8; sg-25:19 Q4(d) P8; sg-23:15 Q4(d) P2; sg-22:4 Q1(d) P4

## BC-PT-99012 Classification of a critical point by a derivative test [verified]

Scope shared. Sources sg-26:8, sg-24:10, sg-23:13.

- Earns: Correct classification of the critical point as a relative maximum, relative minimum, or neither, with analysis using a first or second derivative test; the test need not be named (sg-26:8).
- Does not earn: A candidates test, which sg-26:8 states is not sufficient justification here; an assertion with no supporting sign or second-derivative analysis.
- Requires previous work: no
- Setup alone earns: n/a
- Simplification required: no
- Units required: no
- Interpretation required: no
- Justification required: yes
- Hypotheses required: no
- Notation: No special notation requirement stated in the rubrics reviewed.
- Precision: Not a reported-value point, so the three-decimal rule does not apply.
- Dependency: sg-26:8 requires the critical-value point first, and does not require the value to be restated here.
- Eligibility after an error: No eligibility restriction stated in the rubrics reviewed.
- Rubric instances: sg-26:8 Q2(C) P7; sg-24:10 Q3(b) P3; sg-23:13 Q4(a) P1
- Notes: sg-23:13 accepts the shorter form that the derivative does not change sign, so neither extremum occurs.

## BC-PT-99013 Considers the derivative set equal to zero [verified]

Scope shared. Sources sg-25:5, sg-25:8, sg-25:19, sg-26:17, sg-23:15, sg-22:12.

- Earns: Presenting the equation derivative equals zero, or an equivalent equation, or discussing the sign change of the derivative, or using the phrase critical points of the function (sg-25:5, sg-26:17).
- Does not earn: Presenting only the solved critical value, which sg-25:5, sg-25:9, sg-26:17 and sg-25:19 all state is not sufficient.
- Requires previous work: no
- Setup alone earns: yes
- Simplification required: no
- Units required: no
- Interpretation required: no
- Justification required: no
- Hypotheses required: no
- Notation: No special notation requirement stated in the rubrics reviewed.
- Precision: Not a reported-value point, so the three-decimal rule does not apply.
- Dependency: sg-22:5 states a response that misses this point is still eligible for the remaining points of the part.
- Eligibility after an error: sg-22:12 gives the point to a response that isolates the single critical number without writing the equation explicitly.
- Rubric instances: sg-25:5 Q1(D) P7; sg-25:8 Q2(C) P5; sg-25:19 Q4(d) P7; sg-26:17 Q4(D) P7; sg-23:15 Q4(d) P1; sg-22:12 Q3(d) P1

## BC-PT-99014 Considers the sign of a derivative [verified]

Scope shared. Sources sg-24:8, sg-24:10, sg-26:11, sg-26:12, sg-22:4.

- Earns: An explicit statement about whether a first or second derivative is positive, negative, or zero on the relevant interval, symbolically or in words (sg-26:12, sg-24:8).
- Does not earn: A statement about the sign of the function rather than the derivative, or a reference to the concavity of the derivative itself (sg-26:12).
- Requires previous work: no
- Setup alone earns: yes
- Simplification required: no
- Units required: no
- Interpretation required: no
- Justification required: no
- Hypotheses required: no
- Notation: No special notation requirement stated in the rubrics reviewed.
- Precision: Not a reported-value point, so the three-decimal rule does not apply.
- Dependency: sg-26:12 and sg-22:4 both make the reason point eligible only after this point is earned.
- Eligibility after an error: No eligibility restriction stated in the rubrics reviewed.
- Rubric instances: sg-24:8 Q2(d) P1; sg-24:10 Q3(b) P1; sg-26:11 Q3(C) P3; sg-22:4 Q1(c) P1

## BC-PT-99015 Differentiable implies continuous [verified]

Scope shared. Sources sg-25:12, sg-26:5, sg-23:3, sg-22:14.

- Earns: An explicit statement that the function is continuous because it is differentiable, or an equivalent chain from twice differentiable through differentiable to continuous (sg-25:12, sg-26:5, sg-22:14).
- Does not earn: A bare statement that the function is continuous with no justification (sg-25:12, sg-26:5).
- Requires previous work: no
- Setup alone earns: n/a
- Simplification required: no
- Units required: no
- Interpretation required: no
- Justification required: yes
- Hypotheses required: yes
- Notation: No special notation requirement stated in the rubrics reviewed.
- Precision: Not a reported-value point, so the three-decimal rule does not apply.
- Dependency: sg-25:12 and sg-26:5 state the response does not need this point to be eligible for the conclusion point, and sg-26:5 lets a response that earned it skip restating continuity.
- Eligibility after an error: No eligibility restriction stated in the rubrics reviewed.
- Rubric instances: sg-25:12 Q3(b) P3; sg-26:5 Q1(D) P8; sg-23:3 Q1(b) P2; sg-22:14 Q4(b) P2

## BC-PT-99016 Intermediate Value Theorem conclusion [verified]

Scope shared. Sources sg-25:12, sg-26:5, sg-22:14.

- Earns: Showing the target value lies strictly between two function values, stating the function is continuous, and answering yes (sg-25:12, sg-26:5).
- Does not earn: A bare yes with the theorem named, which sg-26:5 states is not sufficient; a naming of the wrong theorem (sg-25:12).
- Requires previous work: no
- Setup alone earns: n/a
- Simplification required: no
- Units required: no
- Interpretation required: no
- Justification required: yes
- Hypotheses required: yes
- Notation: sg-22:14 rejects a bracketing statement that lists the two endpoint values without saying the target lies between them, but allows that response to recover the conclusion point.
- Precision: Not a reported-value point, so the three-decimal rule does not apply.
- Dependency: Independent of other points in the rubrics reviewed.
- Eligibility after an error: sg-25:12 and sg-26:5 both state the theorem need not be named, but a named theorem must be the correct one.
- Rubric instances: sg-25:12 Q3(b) P4; sg-26:5 Q1(D) P9; sg-22:14 Q4(b) P1; sg-22:14 Q4(b) P2

## BC-PT-99017 Mean Value Theorem or Rolle conclusion [verified]

Scope shared. Sources sg-23:3, sg-21:17.

- Earns: A correct average rate of change together with a statement of differentiability on the open interval and continuity on the closed interval, and a yes (sg-23:3, sg-21:17).
- Does not earn: An appeal to the Intermediate Value Theorem, which sg-23:3 states cannot earn the conclusion point here.
- Requires previous work: no
- Setup alone earns: n/a
- Simplification required: no
- Units required: no
- Interpretation required: no
- Justification required: yes
- Hypotheses required: yes
- Notation: No special notation requirement stated in the rubrics reviewed.
- Precision: Not a reported-value point, so the three-decimal rule does not apply.
- Dependency: sg-23:3 requires the difference point first; sg-21:17 instead allows the conclusion point with a correct setup but an incorrect or missing evaluation.
- Eligibility after an error: No eligibility restriction stated in the rubrics reviewed.
- Rubric instances: sg-23:3 Q1(b) P1; sg-23:3 Q1(b) P2; sg-21:17 Q4(d) P2
- Notes: Both documents state the theorem need not be named provided the hypotheses and conclusion are given. Rolle is accepted as an alternative in sg-23:3.

## BC-PT-99018 Form of a Riemann or trapezoidal sum [verified]

Scope shared. Sources sg-25:13, sg-26:3, sg-23:2, sg-22:15, sg-24:3.

- Earns: A sum whose terms each show a value factor and a width factor, with at least five of the six factors correct for three subintervals (sg-25:13, sg-26:3, sg-23:2) or seven of eight for four subintervals (sg-22:15).
- Does not earn: A left or right sum where a midpoint or trapezoidal sum was asked for (sg-26:3, sg-25:13); an unsupported total (sg-26:3, sg-22:15).
- Requires previous work: no
- Setup alone earns: yes
- Simplification required: no
- Units required: no
- Interpretation required: no
- Justification required: no
- Hypotheses required: no
- Notation: sg-25:13 and sg-26:3 instruct readers to read an equals sign as approximately equal for this point.
- Precision: Not a reported-value point, so the three-decimal rule does not apply.
- Dependency: Independent of other points in the rubrics reviewed.
- Eligibility after an error: sg-25:13 and sg-26:3 state any single incorrect factor blocks the approximation point while the form point can still stand; sg-25:13 and sg-26:3 both give the form point but not the value point to a completely correct sum of the wrong type.
- Rubric instances: sg-25:13 Q3(c) P5; sg-26:3 Q1(B) P3; sg-23:2 Q1(a) P2; sg-22:15 Q4(c) P1; sg-24:3 Q1(b) P1

## BC-PT-99019 Approximation value supported by the sum [verified]

Scope shared. Sources sg-25:13, sg-26:3, sg-23:2, sg-22:15.

- Earns: The numerical value of the sum with the supporting products present (sg-25:13, sg-23:2).
- Does not earn: The value alone with no work (sg-26:3, sg-22:15, sg-23:2).
- Requires previous work: yes
- Setup alone earns: n/a
- Simplification required: varies
- Units required: no
- Interpretation required: no
- Justification required: no
- Hypotheses required: no
- Notation: No special notation requirement stated in the rubrics reviewed.
- Precision: Not a reported-value point, so the three-decimal rule does not apply.
- Dependency: sg-25:13 requires the form point before this point; sg-26:3 explicitly allows this point without the form point, for example from a correct sum of products.
- Eligibility after an error: sg-25:13, sg-26:3 and sg-23:2 all bank this point once a correct unsimplified sum appears, so later arithmetic slips do not remove it.
- Rubric instances: sg-25:13 Q3(c) P6; sg-26:3 Q1(B) P4; sg-23:2 Q1(a) P3; sg-22:15 Q4(c) P2

## BC-PT-99020 Average value formula [verified]

Scope shared. Sources sg-25:2, sg-25:3, sg-26:9, sg-23:3, sg-22:3, crabbc-25:3.

- Earns: The definite integral over the interval together with evidence of division by the interval length; a correct answer alongside a correct integral counts as that evidence (sg-25:3, sg-26:9).
- Does not earn: An integral with the wrong integrand, such as the derivative in place of the function (crabbc-25:3); a formula divided by the wrong length (sg-22:3).
- Requires previous work: no
- Setup alone earns: yes
- Simplification required: no
- Units required: no
- Interpretation required: no
- Justification required: no
- Hypotheses required: no
- Notation: Differential optional (sg-26:9). The formula may be presented in one step or across several (sg-25:3, sg-22:3).
- Precision: Not a reported-value point, so the three-decimal rule does not apply.
- Dependency: Independent of other points in the rubrics reviewed.
- Eligibility after an error: sg-25:3 and sg-26:9 treat incorrect linkage between integral and answer as scratch work; sg-23:4 is stricter and takes one of two points for the same pattern, which is a year-to-year change in treatment.
- Rubric instances: sg-25:2 Q1(a) P1; sg-26:9 Q2(D) P8; sg-23:3 Q1(c) P1; sg-22:3 Q1(b) P1

## BC-PT-99021 Average rate of change expression [verified]

Scope shared. Sources sg-25:4, sg-25:11, sg-26:2, sg-22:13, sg-21:17.

- Earns: An expression showing both a difference of function values and a quotient by the difference of inputs, or its correct value (sg-26:2, sg-25:11).
- Does not earn: A bare quotient template with no values substituted (sg-25:11, sg-26:2); the solved value alone where the prompt demanded the setup (sg-25:4).
- Requires previous work: yes
- Setup alone earns: no
- Simplification required: varies
- Units required: no
- Interpretation required: no
- Justification required: no
- Hypotheses required: no
- Notation: No special notation requirement stated in the rubrics reviewed.
- Precision: sg-22:13 and sg-21:17 do not require simplification, but any simplification presented must be correct.
- Dependency: Independent of other points in the rubrics reviewed.
- Eligibility after an error: sg-25:4 lists several equivalent forms, including an integral of the derivative over the interval divided by the length.
- Rubric instances: sg-25:4 Q1(b) P3; sg-25:11 Q3(a) P1; sg-26:2 Q1(A) P1; sg-22:13 Q4(a) P1; sg-21:17 Q4(d) P1

## BC-PT-99022 Product rule [verified]

Scope shared. Sources sg-25:20, sg-25:21, sg-22:16, sg-23:19.

- Earns: A differentiation that correctly applies the product rule to the given expression (sg-25:20, sg-22:16).
- Does not earn: A response that treats one factor as constant, which sg-22:16 states is eligible for the chain rule point but not this one.
- Requires previous work: no
- Setup alone earns: n/a
- Simplification required: no
- Units required: no
- Interpretation required: no
- Justification required: no
- Hypotheses required: no
- Notation: No special notation requirement stated in the rubrics reviewed.
- Precision: Not a reported-value point, so the three-decimal rule does not apply.
- Dependency: sg-22:16 states the product rule and chain rule points may be earned in either order and that the answer point requires both.
- Eligibility after an error: sg-25:21 allows a quotient rule applied to a separated-variables solution to stand in for the product rule.
- Rubric instances: sg-25:20 Q5(a) P1; sg-22:16 Q4(d) P1; sg-23:19 Q6(a) P1

## BC-PT-99023 Chain rule [verified]

Scope shared. Sources sg-25:20, sg-25:21, sg-22:16.

- Earns: Correct differentiation of the inner function, including the required differentials (sg-22:16, sg-25:21).
- Does not earn: A product rule written without one or both differentials, which sg-22:16 states earns the product rule point but not this one.
- Requires previous work: no
- Setup alone earns: n/a
- Simplification required: no
- Units required: no
- Interpretation required: no
- Justification required: no
- Hypotheses required: no
- Notation: sg-22:16 treats a missing differential as the defining failure for this point.
- Precision: Not a reported-value point, so the three-decimal rule does not apply.
- Dependency: sg-25:21 keeps the value point available to a response that earns the chain rule point but not the product rule point, provided the substitution is consistent.
- Eligibility after an error: No eligibility restriction stated in the rubrics reviewed.
- Rubric instances: sg-25:20 Q5(a) P2; sg-22:16 Q4(d) P2; sg-25:21 Q5(a) P2

## BC-PT-99024 Derivative of an accumulation function by the Fundamental Theorem [verified]

Scope shared. Sources sg-25:16, sg-24:13, sg-24:15, sg-24:14.

- Earns: Writing the derivative of the accumulation function as the integrand evaluated at the variable, in general or at the requested value (sg-25:16, sg-24:13).
- Does not earn: Differencing the integrand at the two limits, which sg-25:16 states earns the answer point but not this one.
- Requires previous work: no
- Setup alone earns: yes
- Simplification required: no
- Units required: no
- Interpretation required: no
- Justification required: no
- Hypotheses required: no
- Notation: No special notation requirement stated in the rubrics reviewed.
- Precision: Not a reported-value point, so the three-decimal rule does not apply.
- Dependency: sg-25:16 allows the answer point on an implied application of the theorem even when this point is not earned.
- Eligibility after an error: No eligibility restriction stated in the rubrics reviewed.
- Rubric instances: sg-25:16 Q4(a) P1; sg-24:13 Q4(b) P1; sg-24:15 Q5(a) P1; sg-24:14 Q4(c) P1

## BC-PT-99025 Tangent line approximation [verified]

Scope shared. Sources sg-23:10, sg-26:11.

- Earns: An approximation computed from a line through the given point whose slope is the declared derivative value (sg-23:10).
- Does not earn: An unsupported approximation (sg-23:10); an approximation simplified incorrectly (sg-23:10).
- Requires previous work: yes
- Setup alone earns: n/a
- Simplification required: no
- Units required: no
- Interpretation required: no
- Justification required: no
- Hypotheses required: no
- Notation: No special notation requirement stated in the rubrics reviewed.
- Precision: Not a reported-value point, so the three-decimal rule does not apply.
- Dependency: sg-23:10 makes the approximation point contingent on a nonzero slope declared as the derivative value.
- Eligibility after an error: sg-26:11 states presentation of a tangent line equation is not considered in scoring for the slope point, and banks the slope point once an unsimplified correct expression appears.
- Rubric instances: sg-23:10 Q3(b) P1; sg-23:10 Q3(b) P2; sg-26:11 Q3(B) P2

## BC-PT-99026 Over or underestimate decided from concavity [verified]

Scope shared. Sources sg-23:10, sg-26:11, sg-26:12, sg-24:4.

- Earns: Citing the sign of the second derivative or the concavity of the graph, and concluding that the tangent line lies above or below the curve (sg-23:10, sg-26:12).
- Does not earn: An argument from concavity at a single point (sg-23:10, sg-26:12); a reference to the concavity of the derivative rather than of the function (sg-26:12).
- Requires previous work: no
- Setup alone earns: n/a
- Simplification required: no
- Units required: no
- Interpretation required: no
- Justification required: yes
- Hypotheses required: no
- Notation: No special notation requirement stated in the rubrics reviewed.
- Precision: Not a reported-value point, so the three-decimal rule does not apply.
- Dependency: sg-26:12 states eligibility for this point requires the sign-of-second-derivative point first; sg-23:11 allows it with an incorrect second derivative provided that expression is a nonconstant linear function negative over the relevant range.
- Eligibility after an error: No eligibility restriction stated in the rubrics reviewed.
- Rubric instances: sg-23:10 Q3(c) P2; sg-26:11 Q3(C) P4; sg-24:4 Q1(d) P1

## BC-PT-99027 Higher derivative expression evaluated at a point [verified]

Scope shared. Sources sg-25:20, sg-25:21, sg-23:10, sg-23:11, sg-23:19, sg-23:20.

- Earns: A correct expression for the second or higher derivative, evaluated at the requested point, consistent with the earlier derivative work (sg-25:20, sg-23:10).
- Does not earn: An expression left in terms of the first derivative where the prompt asked for it in terms of the dependent variable (sg-23:11).
- Requires previous work: no
- Setup alone earns: n/a
- Simplification required: no
- Units required: no
- Interpretation required: no
- Justification required: no
- Hypotheses required: no
- Notation: No special notation requirement stated in the rubrics reviewed.
- Precision: Not a reported-value point, so the three-decimal rule does not apply.
- Dependency: sg-25:21 ties eligibility to the product and chain rule points and permits a consistent value from a partially correct expression.
- Eligibility after an error: sg-25:21 states a correct unsimplified substitution earns the point regardless of later simplification errors.
- Rubric instances: sg-25:20 Q5(a) P3; sg-23:10 Q3(c) P1; sg-23:19 Q6(a) P2; sg-23:20 Q6(c) P1

## BC-PT-99028 Separation of variables [verified]

Scope BC_only. Sources sg-26:12, sg-26:13, sg-23:11, sg-23:12, sg-24:11, sg-21:20, sg-19:5.

- Earns: Rearranging the differential equation so each variable sits with its own differential, in the form constant times the dependent differential over the dependent expression equals constant times the independent differential (sg-26:13).
- Does not earn: Any attempt that leaves both variables on the same side; sg-26:13, sg-23:12, sg-21:20 and sg-19:5 all state that without separation the entire part scores zero.
- Requires previous work: no
- Setup alone earns: yes
- Simplification required: no
- Units required: no
- Interpretation required: no
- Justification required: no
- Hypotheses required: no
- Notation: No special notation requirement stated in the rubrics reviewed.
- Precision: Not a reported-value point, so the three-decimal rule does not apply.
- Dependency: This point gates every later point in the part (sg-26:13, sg-23:12, sg-21:20).
- Eligibility after an error: sg-21:20 states that if an error in separation leaves one side correct, only the matching antiderivative point remains available; sg-26:13 gives a special case where a sign error in the denominator keeps the constant point but blocks the solve point.
- Rubric instances: sg-26:12 Q3(D) P5; sg-23:11 Q3(d) P1; sg-24:11 Q3(c) P1; sg-21:20 Q5(c) P1; sg-19:5 Q4(b) P1
- Notes: Scope marked BC_only because the AP Calculus BC differential equation questions carry the BC-only header in sg-26:12, although separable equations themselves are shared content.

## BC-PT-99029 First antiderivative in a separated equation [verified]

Scope shared. Sources sg-26:12, sg-26:13, sg-24:11, sg-21:20.

- Earns: One consistent antiderivative, either the logarithmic side written with parentheses or absolute value, or the independent-variable side (sg-26:13).
- Does not earn: An antiderivative inconsistent with the separated form (sg-26:13).
- Requires previous work: no
- Setup alone earns: n/a
- Simplification required: no
- Units required: no
- Interpretation required: no
- Justification required: no
- Hypotheses required: no
- Notation: sg-26:13 accepts either parentheses or absolute value on the logarithm; sg-23:12 states an antiderivative written without absolute value symbols stays eligible for all points; sg-21:20 accepts either form.
- Precision: Not a reported-value point, so the three-decimal rule does not apply.
- Dependency: Requires the separation point (sg-26:13).
- Eligibility after an error: No eligibility restriction stated in the rubrics reviewed.
- Rubric instances: sg-26:12 Q3(D) P6; sg-24:11 Q3(c) P2; sg-21:20 Q5(c) P2

## BC-PT-99030 Second antiderivative in a separated equation [verified]

Scope shared. Sources sg-26:12, sg-26:13, sg-24:11, sg-21:20.

- Earns: A second consistent antiderivative, so that both sides of the separated equation are integrated (sg-26:13).
- Does not earn: A single antiderivative with the other side left unintegrated (sg-26:13).
- Requires previous work: no
- Setup alone earns: n/a
- Simplification required: no
- Units required: no
- Interpretation required: no
- Justification required: no
- Hypotheses required: no
- Notation: No special notation requirement stated in the rubrics reviewed.
- Precision: Not a reported-value point, so the three-decimal rule does not apply.
- Dependency: sg-26:13 awards this point only when two consistent antiderivatives are present. sg-23:11 collapses the two antiderivative points into one, which is a year-to-year structural difference.
- Eligibility after an error: No eligibility restriction stated in the rubrics reviewed.
- Rubric instances: sg-26:12 Q3(D) P7; sg-24:11 Q3(c) P3; sg-21:20 Q5(c) P3

## BC-PT-99031 Constant of integration used with the initial condition [verified]

Scope shared. Sources sg-26:12, sg-26:13, sg-23:11, sg-23:12, sg-24:11, sg-21:20, sg-19:5.

- Earns: Including the constant in an equation and substituting the given initial values to solve for it (sg-26:13, sg-21:20).
- Does not earn: Work with no constant of integration at all, which sg-26:13 and sg-23:12 state blocks this point and the solve point.
- Requires previous work: no
- Setup alone earns: n/a
- Simplification required: no
- Units required: no
- Interpretation required: no
- Justification required: no
- Hypotheses required: no
- Notation: No special notation requirement stated in the rubrics reviewed.
- Precision: Not a reported-value point, so the three-decimal rule does not apply.
- Dependency: sg-26:13 requires the separation point and one antiderivative point; sg-23:12 requires the first two points of the part; sg-21:20 requires separation and at least one of the two antiderivative points.
- Eligibility after an error: No eligibility restriction stated in the rubrics reviewed.
- Rubric instances: sg-26:12 Q3(D) P8; sg-23:11 Q3(d) P3; sg-24:11 Q3(c) P4; sg-21:20 Q5(c) P4; sg-19:5 Q4(b) P3

## BC-PT-99032 Solves for the particular solution [verified]

Scope shared. Sources sg-26:12, sg-26:13, sg-23:12, sg-24:11, sg-21:20.

- Earns: Isolating the dependent variable to give the particular solution, in any equivalent exponential form (sg-26:13).
- Does not earn: A solution left in implicit logarithmic form; a solution with no constant of integration shown anywhere (sg-26:13).
- Requires previous work: yes
- Setup alone earns: n/a
- Simplification required: no
- Units required: no
- Interpretation required: no
- Justification required: no
- Hypotheses required: no
- Notation: No special notation requirement stated in the rubrics reviewed.
- Precision: Not a reported-value point, so the three-decimal rule does not apply.
- Dependency: sg-26:13 requires separation and both antiderivative points; sg-23:12 and sg-21:20 require all earlier points of the part.
- Eligibility after an error: sg-26:13 allows this point without explicit constant work when the final function is correct, and states no justification is needed for the sign of the exponential coefficient.
- Rubric instances: sg-26:12 Q3(D) P9; sg-23:12 Q3(d) P4; sg-24:11 Q3(c) P5; sg-21:20 Q5(c) P5

## BC-PT-99033 Uses the initial condition in an accumulation expression [verified]

Scope shared. Sources sg-24:3, sg-24:4, sg-24:6, sg-24:7, sg-22:8.

- Earns: Adding the known function value at one endpoint to a definite integral of the rate (sg-24:3, sg-22:8).
- Does not earn: A definite integral alone with the known value never added (sg-22:8).
- Requires previous work: no
- Setup alone earns: n/a
- Simplification required: no
- Units required: no
- Interpretation required: no
- Justification required: no
- Hypotheses required: no
- Notation: sg-22:8 lists cases where a missing differential shifts which of the three points are available.
- Precision: Not a reported-value point, so the three-decimal rule does not apply.
- Dependency: sg-22:8 requires the value to be added to a definite integral, and lets a response that misses the integral point still earn the answer point on a consistent value.
- Eligibility after an error: No eligibility restriction stated in the rubrics reviewed.
- Rubric instances: sg-24:3 Q1(c) P2; sg-24:6 Q2(c) P2; sg-22:8 Q2(c) P2

## BC-PT-99034 Euler method step [verified]

Scope BC_only. Sources sg-25:23, sg-24:17, sg-21:19.

- Earns: Demonstrating the required number of steps with the correct initial condition, correct step size, and the correct or imported derivative expression (sg-25:23, sg-21:19).
- Does not earn: A single step where two were asked for (sg-24:17); a table that is neither labelled nor accompanied by a correct answer (sg-25:23, sg-21:19).
- Requires previous work: no
- Setup alone earns: yes
- Simplification required: no
- Units required: no
- Interpretation required: no
- Justification required: no
- Hypotheses required: no
- Notation: Steps may be explicit expressions or a table; sg-25:23 and sg-21:19 state an unlabelled table suffices when the answer is correct, and must be labelled when it is not.
- Precision: Not a reported-value point, so the three-decimal rule does not apply.
- Dependency: Independent of other points in the rubrics reviewed.
- Eligibility after an error: sg-25:23 states later simplification or rounding errors do not affect this point; sg-24:17 and sg-21:19 allow at most one error and block the answer point if one occurs; sg-21:19 does not count an imported wrong intermediate value as a second error.
- Rubric instances: sg-25:23 Q5(D) P8; sg-24:17 Q5(c) P1; sg-21:19 Q5(b) P1

## BC-PT-99035 First terms of a Taylor or Maclaurin polynomial [verified]

Scope BC_only. Sources sg-25:22, sg-26:22, sg-26:23, sg-23:19, sg-23:20.

- Earns: The first two nonzero terms, in a list or as part of a polynomial or series (sg-26:22, sg-25:22).
- Does not earn: A correct expanded form that is not written in powers of the centre, which sg-25:22 states earns this point but not the remaining-term point.
- Requires previous work: no
- Setup alone earns: n/a
- Simplification required: no
- Units required: no
- Interpretation required: no
- Justification required: no
- Hypotheses required: no
- Notation: No special notation requirement stated in the rubrics reviewed.
- Precision: Not a reported-value point, so the three-decimal rule does not apply.
- Dependency: Independent of other points in the rubrics reviewed.
- Eligibility after an error: sg-25:22 lets both polynomial points follow from incorrect derivative values imported from an earlier part; sg-26:22 and sg-26:23 treat extraneous terms as scratch work.
- Rubric instances: sg-25:22 Q5(b) P4; sg-26:22 Q6(B) P3; sg-23:19 Q6(a) P3; sg-26:23 Q6(D) P8; sg-23:20 Q6(c) P2

## BC-PT-99036 Remaining terms of a Taylor or Maclaurin polynomial [verified]

Scope BC_only. Sources sg-25:22, sg-26:22, sg-26:23, sg-23:19, sg-23:21.

- Earns: The remaining required terms, completing the polynomial to the requested degree (sg-26:22, sg-25:22).
- Does not earn: A polynomial carrying terms of higher degree than asked, or an ellipsis suggesting the series continues (sg-25:22, sg-23:19, sg-23:21).
- Requires previous work: yes
- Setup alone earns: n/a
- Simplification required: varies
- Units required: no
- Interpretation required: no
- Justification required: no
- Hypotheses required: no
- Notation: No special notation requirement stated in the rubrics reviewed.
- Precision: Not a reported-value point, so the three-decimal rule does not apply.
- Dependency: sg-26:22 and sg-26:23 require the first-terms point before this point; sg-26:23 has a special case where a polynomial that could be simplified to the correct terms earns the first point but not this one.
- Eligibility after an error: No eligibility restriction stated in the rubrics reviewed.
- Rubric instances: sg-25:22 Q5(b) P5; sg-26:22 Q6(B) P4; sg-23:19 Q6(a) P4; sg-26:23 Q6(D) P9

## BC-PT-99037 First nonzero terms of a series for a related function [verified]

Scope BC_only. Sources sg-25:26, sg-26:23, sg-22:22.

- Earns: The requested count of nonzero terms for the derivative, antiderivative, or product function, listed or as part of a series (sg-25:26, sg-22:22).
- Does not earn: Terms whose construction does not follow from the given series (sg-26:23).
- Requires previous work: no
- Setup alone earns: n/a
- Simplification required: no
- Units required: no
- Interpretation required: no
- Justification required: no
- Hypotheses required: no
- Notation: No special notation requirement stated in the rubrics reviewed.
- Precision: Not a reported-value point, so the three-decimal rule does not apply.
- Dependency: sg-26:23 states the series-for-the-exponential point and the first-terms point for the combined function are independent of one another.
- Eligibility after an error: No eligibility restriction stated in the rubrics reviewed.
- Rubric instances: sg-25:26 Q6(B) P6; sg-26:23 Q6(D) P7; sg-22:22 Q6(c) P1

## BC-PT-99038 General term of a series [verified]

Scope BC_only. Sources sg-25:26, sg-24:22, sg-22:22.

- Earns: The correct general term, presented on its own or as the closing term of a polynomial or series (sg-25:26, sg-22:22).
- Does not earn: An ellipsis with no closed form for the nth term (sg-22:22).
- Requires previous work: no
- Setup alone earns: n/a
- Simplification required: no
- Units required: no
- Interpretation required: no
- Justification required: no
- Hypotheses required: no
- Notation: No special notation requirement stated in the rubrics reviewed.
- Precision: Not a reported-value point, so the three-decimal rule does not apply.
- Dependency: Independent of other points in the rubrics reviewed.
- Eligibility after an error: No eligibility restriction stated in the rubrics reviewed.
- Rubric instances: sg-25:26 Q6(B) P7; sg-24:22 Q6(c) P1; sg-22:22 Q6(c) P2

## BC-PT-99039 Lagrange error bound form [single-source]

Scope BC_only. Sources sg-25:22, sg-23:20.

- Earns: The bound written as the maximum of the next derivative over the interval, divided by the factorial, times the distance raised to the matching power, or its evaluated form (sg-25:22, sg-23:20).
- Does not earn: A bound with the wrong factorial or the wrong power of the distance (sg-23:20).
- Requires previous work: no
- Setup alone earns: yes
- Simplification required: no
- Units required: no
- Interpretation required: no
- Justification required: no
- Hypotheses required: no
- Notation: No special notation requirement stated in the rubrics reviewed.
- Precision: Not a reported-value point, so the three-decimal rule does not apply.
- Dependency: Independent of other points in the rubrics reviewed.
- Eligibility after an error: sg-25:22 and sg-23:20 both state that later simplification errors block the analysis point while the form point stands.
- Rubric instances: sg-25:22 Q5(c) P6; sg-23:20 Q6(b) P1
- Notes: Two rubric instances in the corpus read, so tagged single-source.

## BC-PT-99040 Alternating series error bound, first omitted term [verified]

Scope BC_only. Sources sg-26:22, sg-24:21, sg-22:21, sg-19:7.

- Earns: Evaluating the first omitted term of the alternating series at the requested value (sg-26:22, sg-22:21).
- Does not earn: Using a term of the wrong degree; sg-22:21 states any term of degree five or higher does not earn the point, and sg-22:21 states listing the term inside a polynomial is insufficient.
- Requires previous work: no
- Setup alone earns: n/a
- Simplification required: no
- Units required: no
- Interpretation required: no
- Justification required: no
- Hypotheses required: no
- Notation: No special notation requirement stated in the rubrics reviewed.
- Precision: Not a reported-value point, so the three-decimal rule does not apply.
- Dependency: Independent of other points in the rubrics reviewed.
- Eligibility after an error: sg-26:22 awards this point for correctly evaluating the third-degree term found earlier even when that term is wrong, but then blocks the justification point.
- Rubric instances: sg-26:22 Q6(C) P5; sg-24:21 Q6(b) P1; sg-22:21 Q6(b) P1; sg-19:7 Q6(d) P2

## BC-PT-99041 Error bound analysis with an explicit inequality [verified]

Scope BC_only. Sources sg-25:22, sg-26:22, sg-23:20, sg-22:21, sg-24:21.

- Earns: Connecting the computed bound to the target value with an inequality, for example writing that the error is at most the stated number (sg-25:22, sg-22:21).
- Does not earn: Declaring the error equal to the bound rather than bounded by it; sg-25:22, sg-26:22, sg-23:20 and sg-22:21 all withhold the point for an equality claim.
- Requires previous work: yes
- Setup alone earns: n/a
- Simplification required: no
- Units required: no
- Interpretation required: no
- Justification required: yes
- Hypotheses required: no
- Notation: No special notation requirement stated in the rubrics reviewed.
- Precision: Not a reported-value point, so the three-decimal rule does not apply.
- Dependency: Every instance requires the matching bound point first (sg-25:22, sg-26:22, sg-22:21).
- Eligibility after an error: No eligibility restriction stated in the rubrics reviewed.
- Rubric instances: sg-25:22 Q5(c) P7; sg-26:22 Q6(C) P6; sg-23:20 Q6(b) P2; sg-22:21 Q6(b) P2; sg-24:21 Q6(b) P2
- Notes: sg-26:22 and sg-22:21 additionally require the response to state that the series is a convergent alternating series whose terms decrease to zero.

## BC-PT-99042 Ratio setup for the ratio test [verified]

Scope BC_only. Sources sg-25:24, sg-25:25, sg-24:23, sg-22:20, sg-21:24.

- Earns: A correct ratio of consecutive terms, with or without absolute values (sg-25:25, sg-22:21).
- Does not earn: A response that presents no ratio at all, which sg-25:25 states leaves the limit point unavailable.
- Requires previous work: no
- Setup alone earns: yes
- Simplification required: no
- Units required: no
- Interpretation required: no
- Justification required: no
- Hypotheses required: no
- Notation: No special notation requirement stated in the rubrics reviewed.
- Precision: Not a reported-value point, so the three-decimal rule does not apply.
- Dependency: Independent of other points in the rubrics reviewed.
- Eligibility after an error: sg-25:25 and sg-21:24 both bank this point once earned. sg-25:25 accepts several reciprocal ratios, which keep the response eligible for the middle points but not for the final interval point. sg-22:21 keeps a substitution error in the exponent eligible for the first three points only.
- Rubric instances: sg-25:24 Q6(a) P1; sg-24:23 Q6(d) P1; sg-22:20 Q6(a) P1; sg-21:24 Q6(c) P1

## BC-PT-99043 Limit of the ratio [verified]

Scope BC_only. Sources sg-25:24, sg-25:25, sg-24:23, sg-21:24.

- Earns: Correct evaluation of the limit of the ratio, including correct limit notation (sg-22:21, sg-21:24).
- Does not earn: Any error in simplification or evaluation of the limit, which sg-25:25 states forfeits this point even when the ratio point stands.
- Requires previous work: yes
- Setup alone earns: n/a
- Simplification required: no
- Units required: no
- Interpretation required: no
- Justification required: no
- Hypotheses required: no
- Notation: sg-22:21 requires correct limit notation and either the absolute value of the ratio or a resolution to a squared inequality; sg-25:25 states a response not using absolute value can still earn both the ratio and the limit points.
- Precision: Not a reported-value point, so the three-decimal rule does not apply.
- Dependency: sg-21:24 states this point cannot be earned without the ratio point.
- Eligibility after an error: No eligibility restriction stated in the rubrics reviewed.
- Rubric instances: sg-25:24 Q6(a) P2; sg-24:23 Q6(d) P2; sg-21:24 Q6(c) P2

## BC-PT-99044 Interior of the interval of convergence [single-source]

Scope BC_only. Sources sg-25:24, sg-25:25, sg-22:20, sg-22:21.

- Earns: Resolving the inequality to a two-sided inequality or an interval for the variable (sg-25:25, sg-22:21).
- Does not earn: An absolute value inequality left unresolved; sg-25:25 states the bare form with the centre and radius is not sufficient unless it is resolved to a two-sided inequality, and sg-22:21 states a one-sided bound is insufficient.
- Requires previous work: no
- Setup alone earns: n/a
- Simplification required: no
- Units required: no
- Interpretation required: no
- Justification required: no
- Hypotheses required: no
- Notation: No special notation requirement stated in the rubrics reviewed.
- Precision: Not a reported-value point, so the three-decimal rule does not apply.
- Dependency: Independent of other points in the rubrics reviewed.
- Eligibility after an error: sg-25:25 keeps a response with an incorrect but positive limit denominator eligible, scoring the point for the matching interval; sg-22:21 lists one incorrect interval that remains eligible for the endpoint point.
- Rubric instances: sg-25:24 Q6(a) P3; sg-22:20 Q6(a) P2
- Notes: Two rubric instances in the corpus read, so tagged single-source.

## BC-PT-99045 Considers both endpoints [single-source]

Scope BC_only. Sources sg-25:24, sg-25:25, sg-22:20, sg-22:21.

- Earns: Substituting both endpoints of the interval and writing the two resulting series (sg-25:25, sg-22:20).
- Does not earn: Considering one endpoint only (sg-22:21).
- Requires previous work: no
- Setup alone earns: n/a
- Simplification required: no
- Units required: no
- Interpretation required: no
- Justification required: no
- Hypotheses required: no
- Notation: No special notation requirement stated in the rubrics reviewed.
- Precision: Not a reported-value point, so the three-decimal rule does not apply.
- Dependency: sg-25:25 awards this point for both endpoints of the correct interval or of an incorrect interval that earned the interior point.
- Eligibility after an error: No eligibility restriction stated in the rubrics reviewed.
- Rubric instances: sg-25:24 Q6(a) P4; sg-22:20 Q6(a) P3
- Notes: Two rubric instances in the corpus read, so tagged single-source.

## BC-PT-99046 Endpoint analysis with a named test and the stated interval [verified]

Scope BC_only. Sources sg-25:24, sg-25:25, sg-22:20, sg-24:19.

- Earns: Correct analysis of the series at each endpoint plus an explicit statement of the interval of convergence; naming an appropriate test is sufficient analysis (sg-25:25).
- Does not earn: An interval stated with no endpoint analysis (sg-25:25); analysis from a reciprocal ratio, which sg-25:25 states is not eligible for this point.
- Requires previous work: yes
- Setup alone earns: n/a
- Simplification required: no
- Units required: no
- Interpretation required: no
- Justification required: yes
- Hypotheses required: no
- Notation: No special notation requirement stated in the rubrics reviewed.
- Precision: Not a reported-value point, so the three-decimal rule does not apply.
- Dependency: sg-25:25 accepts the alternating series test, direct or limit comparison, and the integral test as named analyses.
- Eligibility after an error: No eligibility restriction stated in the rubrics reviewed.
- Rubric instances: sg-25:24 Q6(a) P5; sg-22:20 Q6(a) P4; sg-24:19 Q6(a) P2

## BC-PT-99047 Radius of convergence stated explicitly [verified]

Scope BC_only. Sources sg-24:22, sg-24:23, sg-21:24.

- Earns: An explicit statement of the radius, obtained either from the ratio test inequality or by citing the radius of a related series (sg-21:24, sg-24:22).
- Does not earn: An interval presented with no identification of the radius, which sg-21:24 states does not earn the point.
- Requires previous work: no
- Setup alone earns: n/a
- Simplification required: no
- Units required: no
- Interpretation required: no
- Justification required: no
- Hypotheses required: no
- Notation: No special notation requirement stated in the rubrics reviewed.
- Precision: Not a reported-value point, so the three-decimal rule does not apply.
- Dependency: sg-21:24 requires a finite nonzero limit for the coefficient before this point is available.
- Eligibility after an error: No eligibility restriction stated in the rubrics reviewed.
- Rubric instances: sg-24:22 Q6(c) P2; sg-24:23 Q6(d) P3; sg-21:24 Q6(c) P3

## BC-PT-99048 Polar area integrand with the square of the radial function [verified]

Scope BC_only. Sources sg-25:7, sg-26:6, sg-26:7, sg-19:3.

- Earns: A definite integral whose integrand contains the square of the polar function, with or without the differential (sg-25:7, sg-26:7).
- Does not earn: An integrand using the radial function unsquared (sg-25:7).
- Requires previous work: no
- Setup alone earns: yes
- Simplification required: no
- Units required: no
- Interpretation required: no
- Justification required: no
- Hypotheses required: no
- Notation: No special notation requirement stated in the rubrics reviewed.
- Precision: Not a reported-value point, so the three-decimal rule does not apply.
- Dependency: sg-25:7 assesses the outer one-half factor and the angular limits in the answer point rather than here; sg-26:7 requires numerical limits for its single setup point.
- Eligibility after an error: sg-25:7 gives all three points of the part to a correct half-region integral doubled by symmetry.
- Rubric instances: sg-25:7 Q2(b) P2; sg-26:6 Q2(A) P1; sg-19:3 Q2(a) P1

## BC-PT-99049 Derivative of one variable with respect to another by the chain rule in polar or parametric form [verified]

Scope BC_only. Sources sg-26:7, sg-23:7, sg-22:6, sg-25:6, sg-25:7.

- Earns: A correct chain or quotient relation among the derivatives, presented symbolically or numerically (sg-26:7, sg-23:7).
- Does not earn: An equation of the form expression equals constant that equates a general expression to a single value (sg-22:6, sg-23:6).
- Requires previous work: no
- Setup alone earns: n/a
- Simplification required: no
- Units required: no
- Interpretation required: no
- Justification required: no
- Hypotheses required: no
- Notation: sg-25:7 accepts several loose notations for an evaluated derivative, including one written without the evaluation bar, and still awards the point.
- Precision: Not a reported-value point, so the three-decimal rule does not apply.
- Dependency: Independent of other points in the rubrics reviewed.
- Eligibility after an error: sg-23:7 allows an incorrect derivative expression imported from an earlier part provided it was declared there.
- Rubric instances: sg-26:7 Q2(B) P3; sg-23:7 Q2(c) P1; sg-22:6 Q2(a) P1; sg-25:6 Q2(a) P1

## BC-PT-99050 Speed of a parametric or vector-valued motion [verified]

Scope BC_only. Sources sg-24:5, sg-22:7, sg-23:6.

- Earns: The square root of the sum of squares of the two component derivatives, with the setup visible (sg-24:5, sg-22:7).
- Does not earn: A bare statement that speed equals the target value, which sg-23:6 states does not earn the point.
- Requires previous work: no
- Setup alone earns: yes
- Simplification required: no
- Units required: no
- Interpretation required: no
- Justification required: no
- Hypotheses required: no
- Notation: No special notation requirement stated in the rubrics reviewed.
- Precision: Not a reported-value point, so the three-decimal rule does not apply.
- Dependency: Independent of other points in the rubrics reviewed.
- Eligibility after an error: sg-23:6 states a parenthesis error in either component blocks this point but leaves the answer point available, and sg-23:8 carries that decision forward so the same error is not penalised twice.
- Rubric instances: sg-24:5 Q2(a) P1; sg-22:7 Q2(b) P1; sg-23:6 Q2(b) P1

## BC-PT-99051 Arc length or total distance integrand [verified]

Scope BC_only. Sources sg-24:6, sg-22:9, sg-23:8, sg-26:19.

- Earns: A definite integral whose integrand is the square root of one plus the square of the derivative, or the square root of the sum of the squares of the component derivatives (sg-26:19, sg-22:9).
- Does not earn: An unsupported value (sg-22:9); an integrand imported from an incorrect speed function, which sg-23:8 allows for this point but not for the answer point.
- Requires previous work: no
- Setup alone earns: yes
- Simplification required: no
- Units required: no
- Interpretation required: no
- Justification required: no
- Hypotheses required: no
- Notation: sg-26:19 requires the limits to be numerical but not correct for this point, and assesses the derivative expression and the straight boundaries in the following point.
- Precision: Not a reported-value point, so the three-decimal rule does not apply.
- Dependency: Independent of other points in the rubrics reviewed.
- Eligibility after an error: No eligibility restriction stated in the rubrics reviewed.
- Rubric instances: sg-24:6 Q2(b) P1; sg-22:9 Q2(d) P1; sg-23:8 Q2(d) P1; sg-26:19 Q5(C) P5

## BC-PT-99052 Acceleration vector components [verified]

Scope BC_only. Sources sg-23:5, sg-23:6, sg-22:7.

- Earns: Each component of the acceleration vector obtained by differentiating the matching velocity component and evaluating at the requested time; the rubrics award one point per component (sg-22:7, sg-23:5).
- Does not earn: Components presented in reversed order, which sg-22:7 states loses both points; an unsupported vector, which earns only one of the two (sg-22:7, sg-23:6).
- Requires previous work: no
- Setup alone earns: n/a
- Simplification required: no
- Units required: no
- Interpretation required: no
- Justification required: no
- Hypotheses required: no
- Notation: sg-23:6 accepts several bracket styles and allows components listed separately provided they are labelled; sg-22:7 requires labels when no ordered pair is used.
- Precision: Not a reported-value point, so the three-decimal rule does not apply.
- Dependency: sg-22:7 states the two component points are independent of each other.
- Eligibility after an error: No eligibility restriction stated in the rubrics reviewed.
- Rubric instances: sg-23:5 Q2(a) P1; sg-23:5 Q2(a) P2; sg-22:7 Q2(b) P2; sg-22:7 Q2(b) P3

## BC-PT-99053 Limit notation on an improper integral [verified]

Scope BC_only. Sources sg-26:20, sg-23:17, sg-22:19.

- Earns: Replacing the infinite limit with a variable and writing the limit of the resulting expression, applied to the integral or to an antiderivative of the correct form (sg-26:20).
- Does not earn: Arithmetic with infinity written in place of a limit, which sg-23:17, sg-22:19 and sg-26:20 all treat as a failure of this point.
- Requires previous work: no
- Setup alone earns: n/a
- Simplification required: no
- Units required: no
- Interpretation required: no
- Justification required: no
- Hypotheses required: no
- Notation: sg-23:17 requires correct limit notation throughout; sg-26:20 banks the point once correct notation appears, so later arithmetic with infinity does not remove it, which is a change from the earlier treatment.
- Precision: Not a reported-value point, so the three-decimal rule does not apply.
- Dependency: Independent of other points in the rubrics reviewed.
- Eligibility after an error: sg-22:19 places the no-arithmetic-with-infinity requirement on the answer point instead of the notation point.
- Rubric instances: sg-26:20 Q5(D) P7; sg-23:17 Q5(b) P1; sg-22:19 Q5(c) P1

## BC-PT-99054 Limit expression for end behaviour [single-source]

Scope shared. Sources sg-25:4, crabbc-25:3.

- Earns: Writing the requested limit symbolically as the variable tends to infinity, for either the function or its derivative (sg-25:4).
- Does not earn: Setting up the limit so the variable tends to zero (crabbc-25:3); arithmetic with infinity in place of the value, which sg-25:4 treats as scratch work.
- Requires previous work: no
- Setup alone earns: yes
- Simplification required: no
- Units required: no
- Interpretation required: no
- Justification required: no
- Hypotheses required: no
- Notation: No special notation requirement stated in the rubrics reviewed.
- Precision: Not a reported-value point, so the three-decimal rule does not apply.
- Dependency: sg-25:4 states a response whose limit is taken on the function rather than its derivative is not eligible for the value point.
- Eligibility after an error: No eligibility restriction stated in the rubrics reviewed.
- Rubric instances: sg-25:4 Q1(c) P5; sg-25:4 Q1(c) P6
- Notes: One document in the corpus read, so tagged single-source.

## BC-PT-99055 L'Hospital's Rule application [verified]

Scope shared. Sources sg-23:14.

- Earns: Separate limits for numerator and denominator establishing the indeterminate form, then a ratio of derivatives with at least one derivative correct (sg-23:14).
- Does not earn: A limit written explicitly as zero over zero, which sg-23:14 states does not earn the form point.
- Requires previous work: yes
- Setup alone earns: n/a
- Simplification required: no
- Units required: no
- Interpretation required: no
- Justification required: no
- Hypotheses required: no
- Notation: No special notation requirement stated in the rubrics reviewed.
- Precision: Not a reported-value point, so the three-decimal rule does not apply.
- Dependency: Independent of other points in the rubrics reviewed.
- Eligibility after an error: No eligibility restriction stated in the rubrics reviewed.
- Rubric instances: sg-23:14 Q4(c) P1; sg-23:14 Q4(c) P2; sg-23:14 Q4(c) P3
- Notes: One document in the corpus read, so tagged single-source.

## BC-PT-99056 Integration by parts assignment of u and dv [verified]

Scope BC_only. Sources sg-24:18, sg-23:18, sg-22:18.

- Earns: A choice of u and dv together with du and v, or an implied choice visible in the resulting expression (sg-23:18, sg-22:18).
- Does not earn: A jump straight to an answer with no parts structure visible (sg-24:18).
- Requires previous work: no
- Setup alone earns: yes
- Simplification required: no
- Units required: no
- Interpretation required: no
- Justification required: no
- Hypotheses required: no
- Notation: sg-23:18 and sg-22:18 accept the tabular method, earning this point for columns, labelled or not, that begin with the two chosen factors.
- Precision: Not a reported-value point, so the three-decimal rule does not apply.
- Dependency: Independent of other points in the rubrics reviewed.
- Eligibility after an error: sg-22:18 states an incorrect integral that still requires parts remains eligible for this point and the next.
- Rubric instances: sg-24:18 Q5(d) P1; sg-23:18 Q5(c) P1; sg-22:18 Q5(b) P2

## BC-PT-99057 Integration by parts expression uv minus the integral of v du [verified]

Scope BC_only. Sources sg-24:18, sg-23:18, sg-22:18.

- Earns: The parts expression written out with the remaining integral (sg-23:18, sg-22:18).
- Does not earn: An expression missing the subtracted integral term (sg-24:18).
- Requires previous work: yes
- Setup alone earns: n/a
- Simplification required: no
- Units required: no
- Interpretation required: no
- Justification required: no
- Hypotheses required: no
- Notation: sg-23:18 and sg-22:18 state limits of integration may be present, omitted, or partially present in the parts work.
- Precision: Not a reported-value point, so the three-decimal rule does not apply.
- Dependency: sg-23:18 and sg-22:18 make the answer point available only after both parts points are earned.
- Eligibility after an error: No eligibility restriction stated in the rubrics reviewed.
- Rubric instances: sg-24:18 Q5(d) P2; sg-23:18 Q5(c) P2; sg-22:18 Q5(b) P3

## BC-PT-99058 Volume integrand form [verified]

Scope shared. Sources sg-26:19, sg-22:18, sg-22:19.

- Earns: An integrand of the correct volume form, a nonzero constant times the square of the function for a disc, or the stated cross-section area (sg-26:19, sg-22:18).
- Does not earn: A constant other than pi where pi is required, which sg-22:19 states blocks the answer point; a rotation about the wrong axis, which sg-26:19 lets earn the form point only.
- Requires previous work: no
- Setup alone earns: yes
- Simplification required: no
- Units required: no
- Interpretation required: no
- Justification required: no
- Hypotheses required: no
- Notation: No special notation requirement stated in the rubrics reviewed.
- Precision: Not a reported-value point, so the three-decimal rule does not apply.
- Dependency: Independent of other points in the rubrics reviewed.
- Eligibility after an error: sg-26:19 allows an incorrect function imported from an earlier part to remain eligible for both volume points.
- Rubric instances: sg-26:19 Q5(B) P3; sg-26:19 Q5(B) P4; sg-22:18 Q5(b) P1; sg-22:19 Q5(c) P1

## BC-PT-99059 Area integrand for a region between curves [verified]

Scope shared. Sources sg-23:16, sg-23:17, sg-22:17, sg-21:11.

- Earns: The difference of the two functions, in either order or inside an absolute value, placed in a definite integral (sg-23:16).
- Does not earn: An integrand with incorrect limits, which sg-23:16 states blocks the answer point; incorrect u-substitution limits, which sg-23:17 states also block it.
- Requires previous work: no
- Setup alone earns: yes
- Simplification required: no
- Units required: no
- Interpretation required: no
- Justification required: no
- Hypotheses required: no
- Notation: No special notation requirement stated in the rubrics reviewed.
- Precision: Not a reported-value point, so the three-decimal rule does not apply.
- Dependency: Independent of other points in the rubrics reviewed.
- Eligibility after an error: sg-23:17 accepts an implied integrand for one function alongside an explicit integrand for the other. sg-21:11 requires limits to be present but not correct for this point.
- Rubric instances: sg-23:16 Q5(a) P1; sg-22:17 Q5(a) P1; sg-21:11 Q3(a) P1

## BC-PT-99060 Point of inflection location [verified]

Scope shared. Sources sg-25:17, sg-26:15, sg-22:11.

- Earns: The complete correct list of x-values where the second derivative changes sign (sg-25:17, sg-26:15).
- Does not earn: Any extra or additional declared value inside the open interval, which sg-25:17 and sg-26:15 state forfeits both this point and the reason point.
- Requires previous work: no
- Setup alone earns: n/a
- Simplification required: no
- Units required: no
- Interpretation required: no
- Justification required: no
- Hypotheses required: no
- Notation: sg-22:11 requires correct y-coordinates when the answer is given as ordered pairs; sg-26:15 states an ordered pair with an arbitrary second coordinate earns this point but blocks the reason point.
- Precision: Not a reported-value point, so the three-decimal rule does not apply.
- Dependency: sg-25:17 has a special case where two of three correct values with correct reasoning earn the reason point but not this one.
- Eligibility after an error: No eligibility restriction stated in the rubrics reviewed.
- Rubric instances: sg-25:17 Q4(b) P3; sg-26:15 Q4(B) P3; sg-22:11 Q3(b) P1

## BC-PT-99061 Reason for a point of inflection tied to the given graph [verified]

Scope shared. Sources sg-25:17, sg-26:15, sg-22:11.

- Earns: A reason stated in terms of the graphed derivative changing from increasing to decreasing or the reverse, the slope of that graph changing sign, or that graph attaining a relative extremum (sg-25:17, sg-26:15).
- Does not earn: A reason in terms of the function changing concavity, or in terms of the second derivative changing sign, both of which sg-25:17 and sg-26:15 state earn the answer point but not this one; a reason using an ambiguous term such as the function or the graph.
- Requires previous work: no
- Setup alone earns: n/a
- Simplification required: no
- Units required: no
- Interpretation required: no
- Justification required: yes
- Hypotheses required: no
- Notation: No special notation requirement stated in the rubrics reviewed.
- Precision: Not a reported-value point, so the three-decimal rule does not apply.
- Dependency: sg-26:15 requires the location point first; sg-25:17 allows the reason point without it in one special case.
- Eligibility after an error: No eligibility restriction stated in the rubrics reviewed.
- Rubric instances: sg-25:17 Q4(b) P4; sg-26:15 Q4(B) P4; sg-22:11 Q3(b) P2

## BC-PT-99062 Interval answer for increasing, decreasing, or concavity [verified]

Scope shared. Sources sg-26:16, sg-23:14, sg-22:11.

- Earns: The correct open interval or intervals, with endpoints optional (sg-26:16, sg-23:14).
- Does not earn: Only one of two required intervals, which sg-23:14 scores as one of two points; an interval that answers only half the compound condition (sg-26:16).
- Requires previous work: no
- Setup alone earns: n/a
- Simplification required: no
- Units required: no
- Interpretation required: no
- Justification required: no
- Hypotheses required: no
- Notation: No special notation requirement stated in the rubrics reviewed.
- Precision: Not a reported-value point, so the three-decimal rule does not apply.
- Dependency: sg-26:16 and sg-23:14 both require this point before the reason point.
- Eligibility after an error: No eligibility restriction stated in the rubrics reviewed.
- Rubric instances: sg-26:16 Q4(C) P5; sg-23:14 Q4(b) P1; sg-22:11 Q3(c) P2

## BC-PT-99063 Reason for an interval answer citing the derivative's behaviour [verified]

Scope shared. Sources sg-26:16, sg-23:14, sg-22:11.

- Earns: A reason citing the sign of the derivative and the increasing or decreasing behaviour of the derivative, matched to the compound condition asked (sg-26:16, sg-23:14).
- Does not earn: A reason addressing only one half of a compound condition, which sg-26:16 lists as two special cases earning the interval point but not this one.
- Requires previous work: no
- Setup alone earns: n/a
- Simplification required: no
- Units required: no
- Interpretation required: no
- Justification required: yes
- Hypotheses required: no
- Notation: No special notation requirement stated in the rubrics reviewed.
- Precision: Not a reported-value point, so the three-decimal rule does not apply.
- Dependency: Requires the interval point (sg-26:16, sg-23:14).
- Eligibility after an error: No eligibility restriction stated in the rubrics reviewed.
- Rubric instances: sg-26:16 Q4(C) P6; sg-23:14 Q4(b) P2; sg-22:11 Q3(c) P1

## BC-PT-99064 Labelled values [verified]

Scope shared. Sources sg-25:18, sg-22:10.

- Earns: Each requested value presented with the label that identifies which quantity it is (sg-25:18, sg-22:10).
- Does not earn: Unlabelled values, which sg-25:18 states earn neither point; a single unlabelled value, which sg-22:10 states earns nothing.
- Requires previous work: no
- Setup alone earns: n/a
- Simplification required: no
- Units required: no
- Interpretation required: no
- Justification required: no
- Hypotheses required: no
- Notation: sg-25:18 treats incorrect communication between a label and its value as scratch work with no effect on scoring; sg-22:10 reads unlabelled pairs left to right and top to bottom.
- Precision: Not a reported-value point, so the three-decimal rule does not apply.
- Dependency: sg-22:10 states the two value points may be earned in either order.
- Eligibility after an error: No eligibility restriction stated in the rubrics reviewed.
- Rubric instances: sg-25:18 Q4(c) P5; sg-25:18 Q4(c) P6; sg-22:10 Q3(a) P2; sg-22:10 Q3(a) P3

## BC-PT-99065 Solution curve sketched on a slope field [single-source]

Scope shared. Sources sg-23:9, sg-24:9.

- Earns: A curve through the given point that extends close to both edges of the given field, with no obvious conflict with the drawn segments, and that respects the stated asymptote (sg-23:9).
- Does not earn: A curve crossing the horizontal segments that mark the equilibrium value (sg-23:9).
- Requires previous work: no
- Setup alone earns: n/a
- Simplification required: no
- Units required: no
- Interpretation required: no
- Justification required: no
- Hypotheses required: no
- Notation: No special notation requirement stated in the rubrics reviewed.
- Precision: Not a reported-value point, so the three-decimal rule does not apply.
- Dependency: Independent of other points in the rubrics reviewed.
- Eligibility after an error: No eligibility restriction stated in the rubrics reviewed.
- Rubric instances: sg-23:9 Q3(a) P1; sg-24:9 Q3(a) P1
- Notes: Two rubric instances in the corpus read, so tagged single-source. sg-23:9 states only the portion inside the given field is considered.

## BC-PT-99066 Explanation referencing the sign of the slopes in a slope field [single-source]

Scope shared. Sources sg-26:10, sg-26:11.

- Earns: An explanation referencing the sign of the slopes of the drawn segments, or what that sign implies for the graph of the solution (sg-26:11).
- Does not earn: A reference to the sign of the derivative with no connection to the field; references to the sign of the slope field, the slope of the slope field, or the increasing behaviour of the slope field, all of which sg-26:11 lists as communication failures.
- Requires previous work: no
- Setup alone earns: n/a
- Simplification required: no
- Units required: no
- Interpretation required: no
- Justification required: yes
- Hypotheses required: no
- Notation: No special notation requirement stated in the rubrics reviewed.
- Precision: Not a reported-value point, so the three-decimal rule does not apply.
- Dependency: Independent of other points in the rubrics reviewed.
- Eligibility after an error: sg-26:11 accepts a local argument at any point in the field in place of a global one.
- Rubric instances: sg-26:10 Q3(A) P1
- Notes: One rubric instance in the corpus read, so tagged single-source.

## BC-PT-99067 Geometric series sum from first term and common ratio [verified]

Scope BC_only. Sources sg-26:21, sg-22:22, sg-25:26.

- Earns: Use of the first term over one minus the common ratio, with a nonzero first term and a ratio of the correct magnitude (sg-26:21).
- Does not earn: A sum formula built on a ratio of magnitude at least one; a series imported from an earlier part that is not geometric, which sg-22:22 states makes the point unavailable.
- Requires previous work: no
- Setup alone earns: yes
- Simplification required: no
- Units required: no
- Interpretation required: no
- Justification required: no
- Hypotheses required: no
- Notation: No special notation requirement stated in the rubrics reviewed.
- Precision: Not a reported-value point, so the three-decimal rule does not apply.
- Dependency: Independent of other points in the rubrics reviewed.
- Eligibility after an error: sg-22:22 awards the point for a consistent answer from an incorrect geometric series imported from an earlier part.
- Rubric instances: sg-26:21 Q6(A) P1; sg-22:22 Q6(d) P1; sg-25:26 Q6(C) P8

## BC-PT-99068 Verification for a show-that prompt [verified]

Scope shared. Sources sg-25:26, sg-26:22, sg-23:20, sg-22:21.

- Earns: An algebraic chain that lands on the stated target expression or inequality, closed with the target itself (sg-25:26).
- Does not earn: A chain that stops before the target, or that asserts equality where the prompt asked for a bound (sg-25:22, sg-22:21).
- Requires previous work: no
- Setup alone earns: n/a
- Simplification required: no
- Units required: no
- Interpretation required: no
- Justification required: yes
- Hypotheses required: no
- Notation: No special notation requirement stated in the rubrics reviewed.
- Precision: Not a reported-value point, so the three-decimal rule does not apply.
- Dependency: sg-26:22, sg-23:20 and sg-22:21 all require the preceding setup point before the verification point is available.
- Eligibility after an error: No eligibility restriction stated in the rubrics reviewed.
- Rubric instances: sg-25:26 Q6(C) P8; sg-26:22 Q6(C) P6; sg-23:20 Q6(b) P2; sg-22:21 Q6(b) P2

## BC-PT-99069 Value of an accumulation function found from geometry of a graph [verified]

Scope shared. Sources sg-25:18, sg-24:12, sg-24:13.

- Earns: The value of the accumulation function at the requested input, computed from areas of the regions under the graph, with the correct sign for reversed limits (sg-25:18, sg-24:12).
- Does not earn: A value from the wrong starting limit; sg-24:13 has a special case where an explicitly wrong lower limit forfeits the first point it would otherwise have earned.
- Requires previous work: no
- Setup alone earns: n/a
- Simplification required: no
- Units required: no
- Interpretation required: no
- Justification required: no
- Hypotheses required: no
- Notation: No special notation requirement stated in the rubrics reviewed.
- Precision: Not a reported-value point, so the three-decimal rule does not apply.
- Dependency: Independent of other points in the rubrics reviewed.
- Eligibility after an error: sg-24:13 keeps the response eligible for all later points of the part with consistent answers and supporting work; sg-25:19 allows these values to be imported into a later candidates test.
- Rubric instances: sg-25:18 Q4(c) P5; sg-24:12 Q4(a) P1; sg-24:12 Q4(a) P2; sg-24:12 Q4(a) P3
