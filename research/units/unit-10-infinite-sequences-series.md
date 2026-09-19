---
title: Unit 10, Infinite Sequences and Series
research_date: 2026-09-19
status: draft
purpose: Decompose CED Unit 10 into concepts, atomic skills, non-calculus prerequisites, question archetypes and variants, observed errors, candidate misconceptions, and diagnostic signals, each grounded in the CED text and in the official free response questions and scoring guidelines of 2021 through 2025.
---

# Unit 10, Infinite Sequences and Series

BC-UNIT-10 covers CED pages 180 to 200 and holds fifteen topics, every one of them carrying the BC only marker in the CED and in data/curriculum.json. It is the largest BC only unit in the course. Unit weighting is in [../exam/exam-blueprint.md](../exam/exam-blueprint.md) and exam composition is in [../exam/exam-structure.md](../exam/exam-structure.md). [verified] (ced:186, ced:200)

Two learning objectives govern the convergence half of the unit, BC-LO-LIM-7A and BC-LO-LIM-7B, and seven govern the polynomial and series half, BC-LO-LIM-8A through BC-LO-LIM-8G. The CED closes the list of assessed convergence tests with an exclusion statement inside BC-EK-LIM-7A11: the nth term test for divergence, the integral test, the comparison test, the limit comparison test, the alternating series test, and the ratio test are assessed, and other methods are not. [verified] (ced:193)

## 10.1 Defining Convergent and Divergent Infinite Series

### Official mapping

Topic id BC-TOP-1001, CED code 10.1, name Defining Convergent and Divergent Infinite Series, scope BC_only, CED page 186. [verified] (ced:186)

- BC-LO-LIM-7A (LIM-7.A): Determine whether a series converges or diverges.
  - BC-EK-LIM-7A1 (LIM-7.A.1): "The nth partial sum is defined as the sum of the first n terms of a series."
  - BC-EK-LIM-7A2 (LIM-7.A.2): "An infinite series of numbers converges to a real number S (or has sum S), if and only if the limit of its sequence of partial sums exists and equals S."

Suggested practice skills: BC-MPS-3D (Practice skill 3.D). Weighting pointer: [../exam/exam-blueprint.md](../exam/exam-blueprint.md).

### Concept breakdown

- BC-CON-10001 Partial sums of an infinite series: The first n terms of a series add to a number that depends on n.
- BC-CON-10002 Convergence of a series as a limit of its partial sums: A series converges when its running totals settle on a single number.

- BC-SKL-10001 Determine whether a sequence converges and find its limit: Decide whether the terms of a sequence approach a single number and say which number.
- BC-SKL-10002 Compute the nth partial sum of a series: Add the first n terms and report the total as a function of n.
- BC-SKL-10003 Determine convergence of a series from the limit of its partial sums: Take the limit of the running totals and read off convergence or divergence.
- BC-SKL-10004 Evaluate a telescoping series through its partial sums: Cancel the interior terms of the running total and take the limit of what is left.
- BC-SKL-10005 Distinguish a sequence from its associated series: Say which object is being asked about, the list of terms or their total.

### Prerequisites

- BC-PRQ-10004 -> BC-SKL-10001, supporting, [inferred], Prerequisite for Determine whether a sequence converges and find its limit.
- BC-PRQ-06006 -> BC-SKL-10002, supporting, [inferred], Prerequisite for Compute the nth partial sum of a series.
- BC-PRQ-10008 -> BC-SKL-10002, supporting, [inferred], Prerequisite for Compute the nth partial sum of a series.
- BC-PRQ-10004 -> BC-SKL-10003, supporting, [inferred], Prerequisite for Determine convergence of a series from the limit of its partial sums.
- BC-PRQ-10003 -> BC-SKL-10004, supporting, [inferred], Prerequisite for Evaluate a telescoping series through its partial sums.
- BC-PRQ-10008 -> BC-SKL-10004, supporting, [inferred], Prerequisite for Evaluate a telescoping series through its partial sums.
- BC-PRQ-06005 -> BC-SKL-10005, supporting, [inferred], Prerequisite for Distinguish a sequence from its associated series.

### Required mathematical knowledge

**Partial sum.** For a series with terms a sub n, the nth partial sum is S sub n equals a sub 1 plus a sub 2 through a sub n (BC-EK-LIM-7A1).

**Convergence.** Hypotheses: the sequence of partial sums S sub n has a limit S as n increases without bound. Conclusion: the series converges and its sum is S. If that limit does not exist, the series diverges (BC-EK-LIM-7A2).

**Notation.** Sigma notation with an index and a starting value, a sub n for the general term, S sub n for the nth partial sum, and S for the value of a convergent series.

### Representations

Representations in play: BC-REP-10 Sequence, BC-REP-11 Series, BC-REP-01 Symbolic expression, BC-REP-04 Verbal description.

Conversions tested: expanded term list to sigma notation (BC-REP-11 to BC-REP-01), general term to the sequence of partial sums (BC-REP-01 to BC-REP-10), and a verbal statement of convergence to the corresponding limit statement (BC-REP-04 to BC-REP-01).

### Assessment behaviour

MCQ forms give a closed form for S sub n and ask for the sum, or give a general term and ask which of a sequence and a series converges. FRQ forms embed the definition inside a later part, where a conclusion must name which series is under discussion before it can be scored (sg-21:23). Calculator variants are not characteristic; the series question sits in the no calculator part of Section II (sg-23:19, sg-25:24). Conceptual variants ask what the limit of the partial sums means; computational variants ask for a numerical partial sum or a telescoping total; justification variants require the definition to be quoted as the reason.

### Archetypes

- BC-QA-10001 Selecting a convergence test for a given series
- BC-QA-10002 Value of a convergent series requested

### Errors and misconceptions

- BC-ERR-10001 Convergence of the sequence of terms reported as convergence of the series
- BC-ERR-10002 Value of a convergent series reported as a partial sum
- BC-ERR-10003 Conclusion states convergence without naming which series it is about
- BC-MIS-10001 A sequence and its series are the same object, severity high
- BC-MIS-10002 A partial sum is the value of the series, severity medium

### Diagnostic signals

- BC-SIG-10024 The first several terms are added and the total is reported as the value of the series.

### Adaptive metadata summary

Skills in this topic carry calculator relevance none. Remediation targets named across the topic: BC-PRQ-06005, BC-PRQ-06006, BC-PRQ-10003, BC-PRQ-10004. Every skill record carries the full seven key adaptive block in data/staging/unit-10.skills.json. [inferred]

## 10.2 Working with Geometric Series

### Official mapping

Topic id BC-TOP-1002, CED code 10.2, name Working with Geometric Series, scope BC_only, CED page 187. [verified] (ced:187)

- BC-LO-LIM-7A (LIM-7.A): Determine whether a series converges or diverges.
  - BC-EK-LIM-7A3 (LIM-7.A.3): "A geometric series is a series with a constant ratio between successive terms."
  - BC-EK-LIM-7A4 (LIM-7.A.4): "If a is a real number and r is a real number such that |r| < 1, then the geometric series the sum from n = 0 to infinity of a r^n = a/(1 - r)."

Suggested practice skills: BC-MPS-3D (Practice skill 3.D). Weighting pointer: [../exam/exam-blueprint.md](../exam/exam-blueprint.md).

### Concept breakdown

- BC-CON-10003 Geometric series and the constant ratio: A geometric series multiplies by the same number to get from one term to the next.
- BC-CON-10004 Convergence condition and sum of a geometric series: A geometric series adds to a finite total exactly when the ratio is smaller than one in size.

- BC-SKL-10006 Identify a series as geometric and state its first term and ratio: Check that consecutive terms share a constant quotient and name a and r.
- BC-SKL-10007 Apply the convergence condition for a geometric series: Decide convergence by comparing the size of the ratio with one.
- BC-SKL-10008 Compute the sum of a convergent geometric series: Divide the first term by one minus the ratio.
- BC-SKL-10009 Sum a geometric series whose index does not start at zero: Take the first term as the one the series actually starts with, not the n equals zero term.
- BC-SKL-10010 Sum a geometric series whose ratio contains the variable: Treat the expression in x as the ratio, sum it, and record where the sum is valid.

### Prerequisites

- BC-PRQ-10005 -> BC-SKL-10006, supporting, [inferred], Prerequisite for Identify a series as geometric and state its first term and ratio.
- BC-PRQ-10008 -> BC-SKL-10006, supporting, [inferred], Prerequisite for Identify a series as geometric and state its first term and ratio.
- BC-PRQ-10001 -> BC-SKL-10007, supporting, [inferred], Prerequisite for Apply the convergence condition for a geometric series.
- BC-PRQ-10005 -> BC-SKL-10008, supporting, [inferred], Prerequisite for Compute the sum of a convergent geometric series.
- BC-PRQ-10003 -> BC-SKL-10009, supporting, [inferred], Prerequisite for Sum a geometric series whose index does not start at zero.
- BC-PRQ-10008 -> BC-SKL-10009, supporting, [inferred], Prerequisite for Sum a geometric series whose index does not start at zero.
- BC-PRQ-10001 -> BC-SKL-10010, supporting, [inferred], Prerequisite for Sum a geometric series whose ratio contains the variable.
- BC-PRQ-10005 -> BC-SKL-10010, supporting, [inferred], Prerequisite for Sum a geometric series whose ratio contains the variable.

### Required mathematical knowledge

**Geometric series.** A series is geometric when successive terms have a constant ratio r (BC-EK-LIM-7A3).

**Sum.** Hypotheses: a is a real number and the absolute value of r is less than one. Conclusion: the geometric series with terms a r to the n, summed from n equals zero, converges to a divided by one minus r (BC-EK-LIM-7A4). When the absolute value of r is at least one the series diverges.

**First term.** The a in the formula is the first term of the series as written, whatever the starting index.

**Notation.** Sigma notation with a starting index, a and r, and the closed form a over one minus r.

### Representations

Representations in play: BC-REP-11 Series, BC-REP-01 Symbolic expression, BC-REP-04 Verbal description.

Conversions tested: sigma form to the pair a and r (BC-REP-11 to BC-REP-01), and a power series in x to a closed form function together with the inequality that bounds x (BC-REP-11 to BC-REP-01).

### Assessment behaviour

MCQ forms ask for the sum of a numerical geometric series or for the values of x for which a geometric power series converges. FRQ forms ask a response to recognise a Taylor series as geometric and to show that it sums to a given closed form, with a single verification point available (sg-25:26), and use the ratio at a stated input to decide convergence at a point (sg-25:27). Calculator status for these parts is no calculator (sg-25:24). Conceptual variants ask only for the ratio; computational variants ask for the value; justification variants require the convergence condition to be stated alongside the sum.

### Archetypes

- BC-QA-10001 Selecting a convergence test for a given series
- BC-QA-10002 Value of a convergent series requested
- BC-QA-10003 Geometric series summed in closed form
- BC-QA-10020 Convergence to the function at a specified input decided with a reason

### Errors and misconceptions

- BC-ERR-10002 Value of a convergent series reported as a partial sum
- BC-ERR-10004 Common ratio of a geometric series misidentified
- BC-ERR-10005 Geometric sum formula applied with a ratio of size at least one
- BC-ERR-10006 First term taken as the index zero term when the series starts elsewhere
- BC-MIS-10002 A partial sum is the value of the series, severity medium
- BC-MIS-10003 The geometric sum formula applies to any series that shrinks, severity medium
- BC-MIS-10004 The first term of a geometric series is always the index zero term, severity medium
- BC-MIS-10023 The open interval from the ratio test is the interval of convergence, severity high

### Diagnostic signals

- No signal is scoped to this topic; the unit level signal list in data/staging/unit-10.signals.json applies.

### Adaptive metadata summary

Skills in this topic carry calculator relevance none. Remediation targets named across the topic: BC-PRQ-10001, BC-PRQ-10003, BC-PRQ-10005. Every skill record carries the full seven key adaptive block in data/staging/unit-10.skills.json. [inferred]

## 10.3 The nth Term Test for Divergence

### Official mapping

Topic id BC-TOP-1003, CED code 10.3, name The nth Term Test for Divergence, scope BC_only, CED page 188. [verified] (ced:188)

- BC-LO-LIM-7A (LIM-7.A): Determine whether a series converges or diverges.
  - BC-EK-LIM-7A5 (LIM-7.A.5): "The nth term test is a test for divergence of a series."

Suggested practice skills: BC-MPS-3D (Practice skill 3.D). Weighting pointer: [../exam/exam-blueprint.md](../exam/exam-blueprint.md).

### Concept breakdown

- BC-CON-10005 The nth term test as a one directional test: If the terms do not shrink to zero the total cannot settle, but shrinking terms prove nothing.

- BC-SKL-10011 Evaluate the limit of the general term of a series: Take the limit of a sub n as the index grows.
- BC-SKL-10012 Conclude divergence when the general term does not approach zero: State divergence because the terms do not shrink to zero.
- BC-SKL-10013 State that the nth term test is inconclusive when the limit is zero: Say that terms going to zero settles nothing and another test is needed.

### Prerequisites

- BC-PRQ-10004 -> BC-SKL-10011, supporting, [inferred], Prerequisite for Evaluate the limit of the general term of a series.
- BC-PRQ-10008 -> BC-SKL-10011, supporting, [inferred], Prerequisite for Evaluate the limit of the general term of a series.
- BC-PRQ-10004 -> BC-SKL-10012, supporting, [inferred], Prerequisite for Conclude divergence when the general term does not approach zero.
- BC-PRQ-06005 -> BC-SKL-10013, supporting, [inferred], Prerequisite for State that the nth term test is inconclusive when the limit is zero.

### Required mathematical knowledge

**nth term test.** Hypotheses: the limit of a sub n as n increases without bound is not zero, or does not exist. Conclusion: the series diverges (BC-EK-LIM-7A5).

**One directional.** The CED names this a test for divergence. No converse is available: a limit of zero is consistent with convergence and with divergence, as the harmonic series shows (BC-EK-LIM-7A7).

**Notation.** The limit of a sub n, the name of the test, and the word diverges in the conclusion.

### Representations

Representations in play: BC-REP-11 Series, BC-REP-01 Symbolic expression, BC-REP-04 Verbal description.

Conversions tested: sigma form to the general term and its limit (BC-REP-11 to BC-REP-01), and a limit value to a verbal conclusion naming the test (BC-REP-01 to BC-REP-04).

### Assessment behaviour

MCQ forms present four series and ask which diverges by the nth term test, with distractors whose terms do go to zero. FRQ forms use the test as a screening step before a named test is applied to an endpoint series (sg-24:19). Parts are no calculator. Conceptual variants ask what a limit of zero permits; justification variants demand the test name and the limit value together; multi-concept variants pair the screening step with a comparison argument in the same part.

### Archetypes

- BC-QA-10001 Selecting a convergence test for a given series
- BC-QA-10004 Convergence or divergence established with a named test

### Errors and misconceptions

- BC-ERR-10007 Limit of the general term evaluated incorrectly
- BC-ERR-10008 Convergence concluded because the terms approach zero
- BC-ERR-10009 Test named without its hypotheses being checked
- BC-MIS-10005 Terms approaching zero make a series converge, severity high
- BC-MIS-10006 A test that establishes divergence also establishes convergence, severity high

### Diagnostic signals

- BC-SIG-10001 The response states that the terms approach zero and concludes that the series converges, with no other test applied.

### Adaptive metadata summary

Skills in this topic carry calculator relevance none. Remediation targets named across the topic: BC-PRQ-06005, BC-PRQ-10004. Every skill record carries the full seven key adaptive block in data/staging/unit-10.skills.json. [inferred]

## 10.4 Integral Test for Convergence

### Official mapping

Topic id BC-TOP-1004, CED code 10.4, name Integral Test for Convergence, scope BC_only, CED page 189. [verified] (ced:189)

- BC-LO-LIM-7A (LIM-7.A): Determine whether a series converges or diverges.
  - BC-EK-LIM-7A6 (LIM-7.A.6): "The integral test is a method to determine whether a series converges or diverges."

Suggested practice skills: BC-MPS-3D (Practice skill 3.D). Weighting pointer: [../exam/exam-blueprint.md](../exam/exam-blueprint.md).

### Concept breakdown

- BC-CON-10006 The integral test and its hypotheses: A series of terms read off a positive decreasing continuous function converges exactly when the matching improper integral does.

- BC-SKL-10014 State and verify the conditions required by the integral test: Check that the matching function is positive, decreasing, and continuous on the interval.
- BC-SKL-10015 Set up the improper integral that matches the series: Write the integral of f from the starting index to infinity as a limit.
- BC-SKL-10016 Evaluate the improper integral using limit notation: Antidifferentiate, evaluate at the variable bound, and take the limit.
- BC-SKL-10017 Conclude convergence or divergence of the series from the integral: Report that the series behaves as the integral does, without claiming the two have the same value.

### Prerequisites

- BC-PRQ-06005 -> BC-SKL-10014, supporting, [inferred], Prerequisite for State and verify the conditions required by the integral test.
- BC-PRQ-06005 -> BC-SKL-10015, supporting, [inferred], Prerequisite for Set up the improper integral that matches the series.
- BC-PRQ-06013 -> BC-SKL-10015, supporting, [inferred], Prerequisite for Set up the improper integral that matches the series.
- BC-PRQ-06002 -> BC-SKL-10016, supporting, [inferred], Prerequisite for Evaluate the improper integral using limit notation.
- BC-PRQ-06003 -> BC-SKL-10016, supporting, [inferred], Prerequisite for Evaluate the improper integral using limit notation.
- BC-PRQ-06005 -> BC-SKL-10017, supporting, [inferred], Prerequisite for Conclude convergence or divergence of the series from the integral.

### Required mathematical knowledge

**Integral test.** Hypotheses: f is positive, decreasing, and continuous on the interval from the starting index onward, and a sub n equals f of n. Conclusion: the series and the improper integral of f over that interval either both converge or both diverge (BC-EK-LIM-7A6). A 2021 scoring guideline requires all three conditions to be listed for the conditions point (sg-21:22).

**Value.** The convergent integral bounds the series but is not its sum.

**Improper integral.** The upper limit must be handled with limit notation; substituting the infinity symbol is not an evaluation (sg-21:22).

**Notation.** f of x, the improper integral, limit notation with b approaching infinity.

### Representations

Representations in play: BC-REP-01 Symbolic expression, BC-REP-11 Series, BC-REP-04 Verbal description.

Conversions tested: series general term to a continuous function of x (BC-REP-11 to BC-REP-01) and integral value to a statement about the series (BC-REP-01 to BC-REP-04).

### Assessment behaviour

MCQ forms ask which series the integral test settles, or which hypothesis fails for a given function. FRQ forms ask explicitly for the conditions to be stated and then for the integral to be evaluated, with separate points for the conditions, the improper integral, and the evaluation (sg-21:21). An incorrect lower limit costs the setup point but the response stays eligible for the evaluation point (sg-21:22). Parts are no calculator. Justification variants require limit notation to be carried through the evaluation.

### Archetypes

- BC-QA-10005 Integral test with its conditions stated

### Errors and misconceptions

- BC-ERR-10003 Conclusion states convergence without naming which series it is about
- BC-ERR-10009 Test named without its hypotheses being checked
- BC-ERR-10010 Integral test conditions incomplete or omitted
- BC-ERR-10011 Improper integral evaluated without limit notation
- BC-ERR-10012 Improper integral set up with the wrong lower limit
- BC-ERR-10013 Value of the improper integral reported as the sum of the series
- BC-MIS-10007 A convergence test can be applied without checking its conditions, severity high
- BC-MIS-10008 The improper integral and the series have the same value, severity medium

### Diagnostic signals

- BC-SIG-10009 Two of the three integral test conditions are listed and the third is omitted.
- BC-SIG-10010 The antiderivative is evaluated by substituting the infinity symbol rather than by taking a limit.

### Adaptive metadata summary

Skills in this topic carry calculator relevance none. Remediation targets named across the topic: BC-PRQ-06002, BC-PRQ-06005. Every skill record carries the full seven key adaptive block in data/staging/unit-10.skills.json. [inferred]

## 10.5 Harmonic Series and p-Series

### Official mapping

Topic id BC-TOP-1005, CED code 10.5, name Harmonic Series and p-Series, scope BC_only, CED page 190. [verified] (ced:190)

- BC-LO-LIM-7A (LIM-7.A): Determine whether a series converges or diverges.
  - BC-EK-LIM-7A7 (LIM-7.A.7): "In addition to geometric series, common series of numbers include the harmonic series, the alternating harmonic series, and p-series."

Suggested practice skills: BC-MPS-3B (Practice skill 3.B). Weighting pointer: [../exam/exam-blueprint.md](../exam/exam-blueprint.md).

### Concept breakdown

- BC-CON-10007 Harmonic series, alternating harmonic series, and p-series: A short list of standard series whose behaviour is known and used as a reference.
- BC-CON-10008 Selection of a convergence test from the form of the terms: Read the shape of the general term and pick the test it fits.

- BC-SKL-10018 Classify a series as harmonic, alternating harmonic, or p-series: Name which standard family a series belongs to.
- BC-SKL-10019 Apply the p-series criterion: Compare the exponent with one and state convergence or divergence.
- BC-SKL-10020 Recall the behaviour of the harmonic and alternating harmonic series: State that the harmonic series diverges and the alternating harmonic series converges.
- BC-SKL-10021 Select an appropriate convergence test from the form of the general term: Choose the test that matches the shape of the terms before computing anything.

### Prerequisites

- BC-PRQ-06002 -> BC-SKL-10018, supporting, [inferred], Prerequisite for Classify a series as harmonic, alternating harmonic, or p-series.
- BC-PRQ-10008 -> BC-SKL-10018, supporting, [inferred], Prerequisite for Classify a series as harmonic, alternating harmonic, or p-series.
- BC-PRQ-06002 -> BC-SKL-10019, supporting, [inferred], Prerequisite for Apply the p-series criterion.
- BC-PRQ-06005 -> BC-SKL-10020, supporting, [inferred], Prerequisite for Recall the behaviour of the harmonic and alternating harmonic series.
- BC-PRQ-10008 -> BC-SKL-10021, supporting, [inferred], Prerequisite for Select an appropriate convergence test from the form of the general term.
- BC-PRQ-10005 -> BC-SKL-10021, supporting, [inferred], Prerequisite for Select an appropriate convergence test from the form of the general term.

### Required mathematical knowledge

**Standard series.** In addition to geometric series, the common reference series are the harmonic series, the alternating harmonic series, and p-series (BC-EK-LIM-7A7).

**p-series.** Hypotheses: terms one over n to the p with p a real number. Conclusion: convergence when p is greater than one, divergence when p is at most one. The harmonic series is the case p equals one.

**Exclusion.** The CED states that the nth term test for divergence, the integral test, the comparison test, the limit comparison test, the alternating series test, and the ratio test are the tests assessed (BC-EK-LIM-7A11).

**Decision cues.** A constant quotient of consecutive terms points to the geometric test; factorials or nth powers point to the ratio test; a rational expression in n points to comparison or limit comparison against a p-series; a factor of negative one to the n points to the alternating series test; a term that is a positive decreasing continuous function of n points to the integral test.

### Representations

Representations in play: BC-REP-11 Series, BC-REP-01 Symbolic expression, BC-REP-04 Verbal description.

Conversions tested: general term to the name of a test whose hypotheses it satisfies (BC-REP-01 to BC-REP-04), and a standard series to its known behaviour (BC-REP-11 to BC-REP-04).

### Assessment behaviour

MCQ forms give a series and four candidate tests, or ask for the values of p that make a series converge. FRQ forms use a p-series or the harmonic series as the comparison partner at an endpoint, where the scoring guideline accepts direct comparison, limit comparison, or the integral test for the analysis point (sg-25:25), and where the harmonic series carries the argument in 2024 and 2025 (sg-24:19, sg-25:24). Parts are no calculator. Selection is scored implicitly: a test that does not fit the series earns nothing even when the conclusion is correct (sg-21:23).

### Archetypes

- BC-QA-10001 Selecting a convergence test for a given series
- BC-QA-10004 Convergence or divergence established with a named test
- BC-QA-10015 Endpoint series identified and tested

### Errors and misconceptions

- BC-ERR-10009 Test named without its hypotheses being checked
- BC-ERR-10014 p-series threshold applied incorrectly
- BC-ERR-10015 Endpoint series analysed with a test whose conditions it fails
- BC-MIS-10005 Terms approaching zero make a series converge, severity high
- BC-MIS-10007 A convergence test can be applied without checking its conditions, severity high
- BC-MIS-10009 The p-series threshold is misplaced, severity medium
- BC-MIS-10014 The ratio test settles every series, severity medium

### Diagnostic signals

- No signal is scoped to this topic; the unit level signal list in data/staging/unit-10.signals.json applies.

### Adaptive metadata summary

Skills in this topic carry calculator relevance none. Remediation targets named across the topic: BC-PRQ-06002, BC-PRQ-06005, BC-PRQ-10008. Every skill record carries the full seven key adaptive block in data/staging/unit-10.skills.json. [inferred]

## 10.6 Comparison Tests for Convergence

### Official mapping

Topic id BC-TOP-1006, CED code 10.6, name Comparison Tests for Convergence, scope BC_only, CED page 191. [verified] (ced:191)

- BC-LO-LIM-7A (LIM-7.A): Determine whether a series converges or diverges.
  - BC-EK-LIM-7A8 (LIM-7.A.8): "The comparison test is a method to determine whether a series converges or diverges."
  - BC-EK-LIM-7A9 (LIM-7.A.9): "The limit comparison test is a method to determine whether a series converges or diverges."

Suggested practice skills: BC-MPS-3D (Practice skill 3.D). Weighting pointer: [../exam/exam-blueprint.md](../exam/exam-blueprint.md).

### Concept breakdown

- BC-CON-10009 Direct comparison of series with nonnegative terms: A series squeezed under a convergent one converges, and a series above a divergent one diverges.
- BC-CON-10010 Limit comparison of series with nonnegative terms: Two series whose terms have a positive finite ratio in the limit behave alike.

- BC-SKL-10022 Choose a comparison series for a given series: Pick a standard series whose terms match the dominant behaviour.
- BC-SKL-10023 Establish the term-by-term inequality for a direct comparison: Show which series has the larger terms, for every index in range.
- BC-SKL-10024 Conclude convergence or divergence by direct comparison: Combine the inequality with the known behaviour of the comparison series.
- BC-SKL-10025 Set up the limit comparison ratio with limit notation: Write the limit of the quotient of the two general terms.
- BC-SKL-10026 Conclude from a positive finite limit in a limit comparison: Say that the limit is positive and finite, then transfer the behaviour of the comparison series.

### Prerequisites

- BC-PRQ-10004 -> BC-SKL-10022, supporting, [inferred], Prerequisite for Choose a comparison series for a given series.
- BC-PRQ-06002 -> BC-SKL-10022, supporting, [inferred], Prerequisite for Choose a comparison series for a given series.
- BC-PRQ-10004 -> BC-SKL-10023, supporting, [inferred], Prerequisite for Establish the term-by-term inequality for a direct comparison.
- BC-PRQ-06005 -> BC-SKL-10024, supporting, [inferred], Prerequisite for Conclude convergence or divergence by direct comparison.
- BC-PRQ-10004 -> BC-SKL-10025, supporting, [inferred], Prerequisite for Set up the limit comparison ratio with limit notation.
- BC-PRQ-10007 -> BC-SKL-10025, supporting, [inferred], Prerequisite for Set up the limit comparison ratio with limit notation.
- BC-PRQ-10004 -> BC-SKL-10026, supporting, [inferred], Prerequisite for Conclude from a positive finite limit in a limit comparison.

### Required mathematical knowledge

**Direct comparison test.** Hypotheses: both series have nonnegative terms and a term-by-term inequality holds from some index onward. Conclusion: a series dominated by a convergent series converges, and a series dominating a divergent series diverges (BC-EK-LIM-7A8).

**Limit comparison test.** Hypotheses: both series have positive terms and the limit of the quotient of general terms is a positive finite number. Conclusion: the two series converge together or diverge together (BC-EK-LIM-7A9). The 2021 guideline requires the limit to be reported as positive, and comparing the limit with one instead does not earn the explanation point (sg-21:23).

**Limit notation.** Limit notation is required in the setup of a limit comparison (sg-21:23).

**Naming.** When several series are present in a part, the conclusion must name which series it is about (sg-21:23).

### Representations

Representations in play: BC-REP-11 Series, BC-REP-01 Symbolic expression, BC-REP-04 Verbal description.

Conversions tested: general term to a comparison partner (BC-REP-01 to BC-REP-11) and limit value to a named conclusion about a specific series (BC-REP-01 to BC-REP-04).

### Assessment behaviour

MCQ forms ask which comparison settles a given series. FRQ forms ask for the analysis of an endpoint series by comparison to the harmonic series, with a point for considering the endpoint series and a point for the answer with reason (sg-24:19), or direct the response to a named comparison series and require the limit comparison to be carried out exactly as named (sg-21:23). Parts are no calculator. Justification variants require both the inequality direction and the behaviour of the comparison series; multi-concept variants attach the comparison to an absolute convergence classification in the same part (sg-21:23).

### Archetypes

- BC-QA-10004 Convergence or divergence established with a named test
- BC-QA-10006 Limit comparison used to classify a series
- BC-QA-10015 Endpoint series identified and tested

### Errors and misconceptions

- BC-ERR-10003 Conclusion states convergence without naming which series it is about
- BC-ERR-10015 Endpoint series analysed with a test whose conditions it fails
- BC-ERR-10016 Comparison inequality stated in the direction that does not support the conclusion
- BC-ERR-10017 Limit taken without limit notation
- BC-ERR-10018 Absolute values omitted when absolute convergence is the target
- BC-ERR-10019 Limit comparison conclusion drawn by comparing the limit with one
- BC-MIS-10009 The p-series threshold is misplaced, severity medium
- BC-MIS-10010 The comparison inequality works in either direction, severity high
- BC-MIS-10011 The limit comparison value is compared with one, severity medium

### Diagnostic signals

- BC-SIG-10011 The limit comparison ratio is evaluated correctly and then compared with one to reach the conclusion.
- BC-SIG-10013 A correct comparison series is chosen but the inequality is stated in the direction that does not support the conclusion.

### Adaptive metadata summary

Skills in this topic carry calculator relevance none. Remediation targets named across the topic: BC-PRQ-06005, BC-PRQ-10004. Every skill record carries the full seven key adaptive block in data/staging/unit-10.skills.json. [inferred]

## 10.7 Alternating Series Test for Convergence

### Official mapping

Topic id BC-TOP-1007, CED code 10.7, name Alternating Series Test for Convergence, scope BC_only, CED page 192. [verified] (ced:192)

- BC-LO-LIM-7A (LIM-7.A): Determine whether a series converges or diverges.
  - BC-EK-LIM-7A10 (LIM-7.A.10): "The alternating series test is a method to determine whether an alternating series converges."

Suggested practice skills: BC-MPS-3D (Practice skill 3.D). Weighting pointer: [../exam/exam-blueprint.md](../exam/exam-blueprint.md).

### Concept breakdown

- BC-CON-10011 The alternating series test and its two conditions: An alternating series converges when its term sizes shrink steadily to zero.

- BC-SKL-10027 Recognise a series as alternating: Spot the factor that flips the sign from term to term.
- BC-SKL-10028 Verify that the terms decrease in absolute value: Check that each term is smaller in size than the one before it.
- BC-SKL-10029 Verify that the terms tend to zero: Check that the size of the terms has limit zero.
- BC-SKL-10030 Conclude convergence by the alternating series test with both conditions stated: Name the test and state that the terms decrease in magnitude to zero.

### Prerequisites

- BC-PRQ-10008 -> BC-SKL-10027, supporting, [inferred], Prerequisite for Recognise a series as alternating.
- BC-PRQ-10004 -> BC-SKL-10028, supporting, [inferred], Prerequisite for Verify that the terms decrease in absolute value.
- BC-PRQ-10004 -> BC-SKL-10029, supporting, [inferred], Prerequisite for Verify that the terms tend to zero.
- BC-PRQ-06005 -> BC-SKL-10030, supporting, [inferred], Prerequisite for Conclude convergence by the alternating series test with both conditions stated.

### Required mathematical knowledge

**Alternating series test.** Hypotheses: the terms alternate in sign, the absolute values of the terms decrease, and the limit of the absolute values is zero. Conclusion: the series converges (BC-EK-LIM-7A10).

**Both conditions.** Scoring guidelines that rest on the test require the response to state that the series alternates and that its terms decrease in absolute value to zero (sg-22:21, sg-24:21).

**No converse.** The test gives convergence only; it says nothing when the terms fail to decrease.

**Notation.** The alternating factor written as negative one to the n or negative one to the n plus one, absolute values of terms, and the name of the test in the conclusion.

### Representations

Representations in play: BC-REP-11 Series, BC-REP-01 Symbolic expression, BC-REP-04 Verbal description.

Conversions tested: sigma form to the sequence of absolute values (BC-REP-11 to BC-REP-10) and verified conditions to a named conclusion (BC-REP-01 to BC-REP-04).

### Assessment behaviour

MCQ forms ask which alternating series converge, with distractors whose terms do not decrease. FRQ forms use the test at an endpoint of an interval of convergence, where naming the test is accepted as the analysis at that endpoint (sg-25:25, sg-22:20), and as the gate before an alternating series error bound is applied (sg-22:21, sg-24:21). Parts are no calculator. Justification variants score the statement of the two conditions rather than the conclusion alone.

### Archetypes

- BC-QA-10004 Convergence or divergence established with a named test
- BC-QA-10008 Alternating series error bound compared with a tolerance
- BC-QA-10015 Endpoint series identified and tested

### Errors and misconceptions

- BC-ERR-10008 Convergence concluded because the terms approach zero
- BC-ERR-10009 Test named without its hypotheses being checked
- BC-ERR-10015 Endpoint series analysed with a test whose conditions it fails
- BC-ERR-10020 Alternating series test applied without both conditions stated
- BC-MIS-10005 Terms approaching zero make a series converge, severity high
- BC-MIS-10007 A convergence test can be applied without checking its conditions, severity high
- BC-MIS-10012 Alternating signs alone give convergence, severity high
- BC-MIS-10013 Decreasing and tending to zero are a single condition, severity medium

### Diagnostic signals

- No signal is scoped to this topic; the unit level signal list in data/staging/unit-10.signals.json applies.

### Adaptive metadata summary

Skills in this topic carry calculator relevance none. Remediation targets named across the topic: BC-PRQ-06005, BC-PRQ-10004, BC-PRQ-10008. Every skill record carries the full seven key adaptive block in data/staging/unit-10.skills.json. [inferred]

## 10.8 Ratio Test for Convergence

### Official mapping

Topic id BC-TOP-1008, CED code 10.8, name Ratio Test for Convergence, scope BC_only, CED page 193. [verified] (ced:193)

- BC-LO-LIM-7A (LIM-7.A): Determine whether a series converges or diverges.
  - BC-EK-LIM-7A11 (LIM-7.A.11): "The ratio test is a method to determine whether a series of numbers converges or diverges."

Suggested practice skills: BC-MPS-3D (Practice skill 3.D). Weighting pointer: [../exam/exam-blueprint.md](../exam/exam-blueprint.md).

### Concept breakdown

- BC-CON-10012 The ratio test and its three cases: Compare the size of consecutive terms in the limit and read off convergence, divergence, or nothing.

- BC-SKL-10031 Set up the ratio of consecutive terms of a series: Write the next term over the current term, in absolute value.
- BC-SKL-10032 Evaluate the limit of the ratio of consecutive terms: Simplify the quotient and take its limit as the index grows.
- BC-SKL-10033 Conclude from the value of the ratio limit, including the inconclusive case: Compare the limit with one and state convergence, divergence, or no conclusion.

### Prerequisites

- BC-PRQ-10002 -> BC-SKL-10031, supporting, [inferred], Prerequisite for Set up the ratio of consecutive terms of a series.
- BC-PRQ-10007 -> BC-SKL-10031, supporting, [inferred], Prerequisite for Set up the ratio of consecutive terms of a series.
- BC-PRQ-10008 -> BC-SKL-10031, supporting, [inferred], Prerequisite for Set up the ratio of consecutive terms of a series.
- BC-PRQ-10002 -> BC-SKL-10032, supporting, [inferred], Prerequisite for Evaluate the limit of the ratio of consecutive terms.
- BC-PRQ-10004 -> BC-SKL-10032, supporting, [inferred], Prerequisite for Evaluate the limit of the ratio of consecutive terms.
- BC-PRQ-10007 -> BC-SKL-10032, supporting, [inferred], Prerequisite for Evaluate the limit of the ratio of consecutive terms.
- BC-PRQ-10001 -> BC-SKL-10033, supporting, [inferred], Prerequisite for Conclude from the value of the ratio limit, including the inconclusive case.

### Required mathematical knowledge

**Ratio test.** Hypotheses: the limit L of the absolute value of a sub n plus one over a sub n exists or is infinite. Conclusion: the series converges absolutely when L is less than one, diverges when L is greater than one, and the test gives no information when L equals one (BC-EK-LIM-7A11).

**Presentation.** A correct ratio earns its point with or without absolute values, and once earned that point is banked; the limit point is lost for any error in simplification or evaluation (sg-25:25). A reciprocal ratio is accepted for the setup and keeps the response eligible for the interior of the interval, but not for the final interval point (sg-25:25).

**Substitution.** Every occurrence of the index must be replaced, including inside an exponent such as two n plus one (sg-22:21).

**Notation.** Absolute value bars, limit notation, and the index substitution n to n plus one.

### Representations

Representations in play: BC-REP-11 Series, BC-REP-01 Symbolic expression.

Conversions tested: general term to the ratio of consecutive terms (BC-REP-11 to BC-REP-01) and ratio limit to an inequality in the variable (BC-REP-01 to BC-REP-01).

### Assessment behaviour

MCQ forms give a series with factorials or nth powers and ask what the ratio test shows. FRQ forms make the ratio the first scored step of the interval of convergence question, with one point for the ratio and one for its limit (sg-25:24, sg-22:20), or ask for a radius of convergence where the ratio and the limit are scored separately from the radius itself (sg-21:24). Parts are no calculator. A response that presents no ratio is not eligible for the limit point (sg-25:25).

### Archetypes

- BC-QA-10001 Selecting a convergence test for a given series
- BC-QA-10004 Convergence or divergence established with a named test
- BC-QA-10013 Interval of convergence by the ratio test with endpoint analysis
- BC-QA-10014 Radius of convergence from a given series

### Errors and misconceptions

- BC-ERR-10009 Test named without its hypotheses being checked
- BC-ERR-10017 Limit taken without limit notation
- BC-ERR-10021 Index substitution incomplete in the ratio of consecutive terms
- BC-ERR-10022 Ratio test carried out without absolute values
- BC-MIS-10014 The ratio test settles every series, severity medium

### Diagnostic signals

- BC-SIG-10002 The ratio of consecutive terms is correct but the limit is evaluated incorrectly.

### Adaptive metadata summary

Skills in this topic carry calculator relevance none. Remediation targets named across the topic: BC-PRQ-10001, BC-PRQ-10002. Every skill record carries the full seven key adaptive block in data/staging/unit-10.skills.json. [inferred]

## 10.9 Determining Absolute or Conditional Convergence

### Official mapping

Topic id BC-TOP-1009, CED code 10.9, name Determining Absolute or Conditional Convergence, scope BC_only, CED page 194. [verified] (ced:194)

- BC-LO-LIM-7A (LIM-7.A): Determine whether a series converges or diverges.
  - BC-EK-LIM-7A12 (LIM-7.A.12): "A series may be absolutely convergent, conditionally convergent, or divergent."
  - BC-EK-LIM-7A13 (LIM-7.A.13): "If a series converges absolutely, then it converges."
  - BC-EK-LIM-7A14 (LIM-7.A.14): "If a series converges absolutely, then any series obtained from it by regrouping or rearranging the terms has the same value."

Suggested practice skills: BC-MPS-3D (Practice skill 3.D). Weighting pointer: [../exam/exam-blueprint.md](../exam/exam-blueprint.md).

### Concept breakdown

- BC-CON-10013 Absolute convergence and its consequences: A series whose absolute values add to a finite total converges, and its value is unaffected by rearrangement.
- BC-CON-10014 Conditional convergence as a separate classification: A series can converge while the series of its absolute values diverges.

- BC-SKL-10034 Test the series of absolute values: Strip the signs and decide whether that series converges.
- BC-SKL-10035 Classify a series as absolutely convergent: Say the series converges absolutely because the absolute value series converges.
- BC-SKL-10036 Classify a series as conditionally convergent: Say the series converges but its absolute value series does not.
- BC-SKL-10037 Use absolute convergence to conclude convergence: Move from convergence of the absolute value series to convergence of the series itself.
- BC-SKL-10038 State the effect of rearrangement on an absolutely convergent series: Say that reordering the terms of an absolutely convergent series leaves its value alone.

### Prerequisites

- BC-PRQ-10008 -> BC-SKL-10034, supporting, [inferred], Prerequisite for Test the series of absolute values.
- BC-PRQ-06005 -> BC-SKL-10035, supporting, [inferred], Prerequisite for Classify a series as absolutely convergent.
- BC-PRQ-06005 -> BC-SKL-10036, supporting, [inferred], Prerequisite for Classify a series as conditionally convergent.
- BC-PRQ-06005 -> BC-SKL-10037, supporting, [inferred], Prerequisite for Use absolute convergence to conclude convergence.
- BC-PRQ-06005 -> BC-SKL-10038, supporting, [inferred], Prerequisite for State the effect of rearrangement on an absolutely convergent series.

### Required mathematical knowledge

**Three outcomes.** A series may be absolutely convergent, conditionally convergent, or divergent (BC-EK-LIM-7A12).

**Absolute convergence implies convergence.** Hypotheses: the series of absolute values converges. Conclusion: the series converges (BC-EK-LIM-7A13).

**Rearrangement.** Hypotheses: the series converges absolutely. Conclusion: any series obtained from it by regrouping or rearranging its terms has the same value (BC-EK-LIM-7A14).

**Conditional convergence.** A series that converges while the series of its absolute values diverges is conditionally convergent; the alternating harmonic series is the standard instance (BC-EK-LIM-7A7).

**Notation.** Absolute value bars around the general term, the words absolutely and conditionally in the classification.

### Representations

Representations in play: BC-REP-11 Series, BC-REP-01 Symbolic expression, BC-REP-04 Verbal description.

Conversions tested: a signed series to its absolute value series (BC-REP-11 to BC-REP-11) and a pair of test outcomes to a single classification word (BC-REP-01 to BC-REP-04).

### Assessment behaviour

MCQ forms give a series and ask which of the three classifications applies. FRQ forms direct a named comparison at the absolute value series and require the conclusion to state absolute convergence of a specific series, with the absolute value symbols required explicitly or implicitly for the explanation point (sg-21:23). Parts are no calculator. Conceptual variants ask what follows from absolute convergence; justification variants require both halves of a conditional convergence claim.

### Archetypes

- BC-QA-10006 Limit comparison used to classify a series
- BC-QA-10007 Absolute or conditional convergence classified
- BC-QA-10015 Endpoint series identified and tested

### Errors and misconceptions

- BC-ERR-10003 Conclusion states convergence without naming which series it is about
- BC-ERR-10018 Absolute values omitted when absolute convergence is the target
- BC-ERR-10023 Absolute and conditional convergence labels interchanged
- BC-MIS-10015 Absolute and conditional convergence are the same distinction, severity high
- BC-MIS-10016 Conditional convergence is a weaker form of absolute convergence, severity medium

### Diagnostic signals

- BC-SIG-10012 The conclusion states that the series converges absolutely without identifying which of the several series in the part is meant.

### Adaptive metadata summary

Skills in this topic carry calculator relevance none. Remediation targets named across the topic: BC-PRQ-06005, BC-PRQ-10008. Every skill record carries the full seven key adaptive block in data/staging/unit-10.skills.json. [inferred]

## 10.10 Alternating Series Error Bound

### Official mapping

Topic id BC-TOP-1010, CED code 10.10, name Alternating Series Error Bound, scope BC_only, CED page 195. [verified] (ced:195)

- BC-LO-LIM-7B (LIM-7.B): Approximate the sum of a series.
  - BC-EK-LIM-7B1 (LIM-7.B.1): "If an alternating series converges by the alternating series test, then the alternating series error bound can be used to bound how far a partial sum is from the value of the infinite series."

Suggested practice skills: BC-MPS-1E (Practice skill 1.E). Weighting pointer: [../exam/exam-blueprint.md](../exam/exam-blueprint.md).

### Concept breakdown

- BC-CON-10015 The alternating series error bound: For a series that converges by the alternating series test, the error in a partial sum is no larger than the first term left out.

- BC-SKL-10039 Confirm the alternating series test conditions before bounding the error: State that the series alternates and its terms decrease to zero before using the bound.
- BC-SKL-10040 Identify the first omitted term of the partial sum: Find the term just past the last one used.
- BC-SKL-10041 Evaluate the bounding term at the given input: Substitute the stated value into the first omitted term and compute its size.
- BC-SKL-10042 Compare the error bound with a stated tolerance: Write the chain of inequalities that puts the error under the required number.

### Prerequisites

- BC-PRQ-06005 -> BC-SKL-10039, supporting, [inferred], Prerequisite for Confirm the alternating series test conditions before bounding the error.
- BC-PRQ-10008 -> BC-SKL-10040, supporting, [inferred], Prerequisite for Identify the first omitted term of the partial sum.
- BC-PRQ-10003 -> BC-SKL-10040, supporting, [inferred], Prerequisite for Identify the first omitted term of the partial sum.
- BC-PRQ-06002 -> BC-SKL-10041, supporting, [inferred], Prerequisite for Evaluate the bounding term at the given input.
- BC-PRQ-10008 -> BC-SKL-10041, supporting, [inferred], Prerequisite for Evaluate the bounding term at the given input.
- BC-PRQ-10001 -> BC-SKL-10042, supporting, [inferred], Prerequisite for Compare the error bound with a stated tolerance.

### Required mathematical knowledge

**Alternating series error bound.** Hypotheses: the alternating series converges by the alternating series test. Conclusion: the absolute difference between the series value and a partial sum is at most the absolute value of the first omitted term (BC-EK-LIM-7B1).

**Strictness of the write up.** Scoring guidelines award the second point only when the conditions are stated and the inequality is presented; writing the error as equal to the bounding term does not earn it (sg-22:21, sg-24:21).

**Which term.** The bound uses the first term not included in the partial sum; using a later term does not earn the point (sg-22:21).

**Notation.** Error, absolute value bars, the inequality symbol at most, and the index of the first omitted term.

### Representations

Representations in play: BC-REP-11 Series, BC-REP-01 Symbolic expression, BC-REP-04 Verbal description.

Conversions tested: a partial sum statement to the index of the first omitted term (BC-REP-11 to BC-REP-01) and an evaluated term to an inequality chain against a tolerance (BC-REP-01 to BC-REP-04).

### Assessment behaviour

MCQ forms ask for the smallest number of terms that brings the error under a stated tolerance. FRQ forms ask a response to show that a partial sum differs from the value of the series by less than a given number, with one point for using the correct omitted term and one for the justification, and the justification point requires the conditions and the inequality (sg-22:21, sg-24:21). A part may instead ask only for an upper bound on the error, scored as a single point (sg-21:25). Parts are no calculator. Multi-concept variants attach the bound to a Taylor polynomial approximation, which is where the CED allows it as an alternative to the Lagrange bound (BC-EK-LIM-8C2).

### Archetypes

- BC-QA-10008 Alternating series error bound compared with a tolerance

### Errors and misconceptions

- BC-ERR-10020 Alternating series test applied without both conditions stated
- BC-ERR-10024 Bounding term taken from the wrong position in the series
- BC-ERR-10025 Bounding term evaluated at the wrong input
- BC-ERR-10026 Error written as equal to the bounding term
- BC-ERR-10027 Comparison with the tolerance left incomplete
- BC-MIS-10017 An error bound can be used without checking its conditions, severity high
- BC-MIS-10018 The bound is the error, severity high

### Diagnostic signals

- BC-SIG-10014 The correct bounding term is found and the error is then written as equal to it.
- BC-SIG-10015 The bound is applied with the correct term and the alternating and decreasing conditions are never stated.
- BC-SIG-10016 A term of higher degree than the first omitted one is used as the bound.

### Adaptive metadata summary

Skills in this topic carry calculator relevance none. Remediation targets named across the topic: BC-PRQ-06002, BC-PRQ-06005, BC-PRQ-10001, BC-PRQ-10008. Every skill record carries the full seven key adaptive block in data/staging/unit-10.skills.json. [inferred]

## 10.11 Finding Taylor Polynomial Approximations of Functions

### Official mapping

Topic id BC-TOP-1011, CED code 10.11, name Finding Taylor Polynomial Approximations of Functions, scope BC_only, CED page 196. [verified] (ced:196)

- BC-LO-LIM-8A (LIM-8.A): Represent a function at a point as a Taylor polynomial.
  - BC-EK-LIM-8A1 (LIM-8.A.1): "The coefficient of the nth degree term in a Taylor polynomial for a function f centered at x = a is f^(n)(a)/n!."
  - BC-EK-LIM-8A2 (LIM-8.A.2): "In many cases, as the degree of a Taylor polynomial increases, the nth degree polynomial will approach the original function over some interval."
- BC-LO-LIM-8B (LIM-8.B): Approximate function values using a Taylor polynomial.
  - BC-EK-LIM-8B1 (LIM-8.B.1): "Taylor polynomials for a function f centered at x = a can be used to approximate function values of f near x = a."

Suggested practice skills: BC-MPS-2C (Practice skill 2.C), BC-MPS-3D (Practice skill 3.D). Weighting pointer: [../exam/exam-blueprint.md](../exam/exam-blueprint.md).

### Concept breakdown

- BC-CON-10016 Taylor polynomial coefficients from derivative values: Each coefficient comes from a derivative at the centre divided by a factorial.
- BC-CON-10017 Taylor polynomials as approximations near the centre: Near the centre the polynomial value stands in for the function value.

- BC-SKL-10043 Compute successive derivatives of a function at the centre: Differentiate repeatedly and evaluate each derivative at the centre.
- BC-SKL-10044 Build a Taylor polynomial from derivative values at the centre: Divide each derivative value by the matching factorial and attach the power.
- BC-SKL-10045 Build a Taylor polynomial from a table of derivative values: Read the derivative values out of the table and place them in the coefficients.
- BC-SKL-10046 Write a Maclaurin polynomial as the Taylor polynomial about zero: Use the centre zero so the powers are plain powers of x.
- BC-SKL-10047 Build a Taylor polynomial for a related function from a known series: Combine known series by multiplying, differentiating, or antidifferentiating, then keep the needed degrees.
- BC-SKL-10048 Approximate a function value with a Taylor polynomial: Substitute the input into the polynomial and report the value.

Granularity note: Topic 10.11 carries six skills because the CED separates representing a function as a Taylor polynomial (BC-LO-LIM-8A) from approximating function values with it (BC-LO-LIM-8B), and because the official free response material supplies the derivative values in three distinct ways, through repeated differentiation of a relation, through a table, and through operations on a known series, each of which is independently testable.

### Prerequisites

- BC-PRQ-06005 -> BC-SKL-10043, supporting, [inferred], Prerequisite for Compute successive derivatives of a function at the centre.
- BC-PRQ-10002 -> BC-SKL-10044, supporting, [inferred], Prerequisite for Build a Taylor polynomial from derivative values at the centre.
- BC-PRQ-10002 -> BC-SKL-10045, supporting, [inferred], Prerequisite for Build a Taylor polynomial from a table of derivative values.
- BC-PRQ-06005 -> BC-SKL-10045, supporting, [inferred], Prerequisite for Build a Taylor polynomial from a table of derivative values.
- BC-PRQ-10002 -> BC-SKL-10046, supporting, [inferred], Prerequisite for Write a Maclaurin polynomial as the Taylor polynomial about zero.
- BC-PRQ-10002 -> BC-SKL-10047, supporting, [inferred], Prerequisite for Build a Taylor polynomial for a related function from a known series.
- BC-PRQ-06005 -> BC-SKL-10047, supporting, [inferred], Prerequisite for Build a Taylor polynomial for a related function from a known series.
- BC-PRQ-06005 -> BC-SKL-10048, supporting, [inferred], Prerequisite for Approximate a function value with a Taylor polynomial.

### Required mathematical knowledge

**Taylor coefficient.** The coefficient of the nth degree term of the Taylor polynomial for f about x equals a is the nth derivative of f at a divided by n factorial (BC-EK-LIM-8A1).

**Approximation.** Taylor polynomials about a approximate values of f near a (BC-EK-LIM-8B1), and in many cases the nth degree polynomial approaches f over an interval as the degree increases (BC-EK-LIM-8A2).

**Degree discipline.** A polynomial presented with terms of degree higher than requested, or with a trailing ellipsis, is not the requested polynomial (sg-23:19, sg-23:20).

**Notation.** T sub n of x, f superscript n of a, factorial notation, and the centre written inside the powers as x minus a.

### Representations

Representations in play: BC-REP-01 Symbolic expression, BC-REP-03 Numerical table, BC-REP-11 Series, BC-REP-09 Calculator generated numerical result.

Conversions tested: a table of derivative values to a polynomial (BC-REP-03 to BC-REP-01), a defining relation for derivatives to derivative values at the centre (BC-REP-01 to BC-REP-03), and a known series to a polynomial for a related function (BC-REP-11 to BC-REP-01).

### Assessment behaviour

MCQ forms give derivative values and ask for one coefficient or for the polynomial. FRQ forms supply a relation for the second and third derivatives, ask for the next derivative and then the fourth degree polynomial, with separate points for the form of the product rule, the derivative itself, the first two terms, and the remaining terms (sg-23:19). Another form defines a second function from the first and asks for its second degree polynomial, with points for the derivative relation, the first two terms, and the complete polynomial, and with an alternate solution through known Maclaurin series accepted (sg-23:20, sg-23:21). Parts are no calculator. A presented polynomial of the right shape can earn a term point without supporting work, but a coefficient with no support does not earn the final point (sg-23:20).

### Archetypes

- BC-QA-10009 Lagrange error bound with a supplied derivative bound
- BC-QA-10010 Taylor polynomial built from repeated differentiation of a relation
- BC-QA-10011 Taylor polynomial built from a table of derivative values
- BC-QA-10012 Taylor polynomial for a related function built from a known series

### Errors and misconceptions

- BC-ERR-10028 Higher derivative computed without the product or chain rule
- BC-ERR-10029 Taylor coefficient written without dividing by the factorial
- BC-ERR-10030 Polynomial presented with extra terms or a trailing ellipsis
- BC-ERR-10031 Derivative values taken from the wrong row or order
- BC-MIS-10019 Taylor coefficients are the derivative values, severity high
- BC-MIS-10020 A Taylor polynomial and a Taylor series are interchangeable, severity medium
- BC-MIS-10021 A function equals its Maclaurin series everywhere, severity high

### Diagnostic signals

- BC-SIG-10018 Derivative values appear directly as coefficients with no factorial denominators.
- BC-SIG-10019 The form of the product rule is displayed correctly but the resulting derivative expression is incomplete.
- BC-SIG-10020 The requested polynomial is correct through the requested degree and carries an extra term or a trailing ellipsis.

### Adaptive metadata summary

Skills in this topic carry calculator relevance none, optional. Remediation targets named across the topic: BC-PRQ-06005, BC-PRQ-10002. Every skill record carries the full seven key adaptive block in data/staging/unit-10.skills.json. [inferred]

## 10.12 Lagrange Error Bound

### Official mapping

Topic id BC-TOP-1012, CED code 10.12, name Lagrange Error Bound, scope BC_only, CED page 197. [verified] (ced:197)

- BC-LO-LIM-8C (LIM-8.C): Determine the error bound associated with a Taylor polynomial approximation.
  - BC-EK-LIM-8C1 (LIM-8.C.1): "The Lagrange error bound can be used to determine a maximum interval for the error of a Taylor polynomial approximation to a function."
  - BC-EK-LIM-8C2 (LIM-8.C.2): "In some situations, the alternating series error bound can be used to bound the error of a Taylor polynomial approximation to the value of a function."

Suggested practice skills: BC-MPS-1F (Practice skill 1.F). Weighting pointer: [../exam/exam-blueprint.md](../exam/exam-blueprint.md).

### Concept breakdown

- BC-CON-10018 The Lagrange error bound: The error of a Taylor polynomial is no larger than a term built from a bound on the next derivative.
- BC-CON-10019 Choosing between the Lagrange and alternating series bounds: Two bounds are available and the hypotheses decide which one applies.

- BC-SKL-10049 Identify the maximum of the next derivative on the interval: Find or use the supplied bound on the derivative one order past the polynomial.
- BC-SKL-10050 Write the Lagrange error bound in the correct form: Assemble the bound from the derivative bound, the power, and the factorial.
- BC-SKL-10051 Compare the Lagrange bound with a stated tolerance: Evaluate the bound and show it is at most the number required.
- BC-SKL-10052 Choose between the Lagrange and alternating series error bounds: Pick the bound whose conditions the situation satisfies.

### Prerequisites

- BC-PRQ-06005 -> BC-SKL-10049, supporting, [inferred], Prerequisite for Identify the maximum of the next derivative on the interval.
- BC-PRQ-10002 -> BC-SKL-10050, supporting, [inferred], Prerequisite for Write the Lagrange error bound in the correct form.
- BC-PRQ-06002 -> BC-SKL-10050, supporting, [inferred], Prerequisite for Write the Lagrange error bound in the correct form.
- BC-PRQ-10001 -> BC-SKL-10051, supporting, [inferred], Prerequisite for Compare the Lagrange bound with a stated tolerance.
- BC-PRQ-10002 -> BC-SKL-10051, supporting, [inferred], Prerequisite for Compare the Lagrange bound with a stated tolerance.
- BC-PRQ-06005 -> BC-SKL-10052, supporting, [inferred], Prerequisite for Choose between the Lagrange and alternating series error bounds.

### Required mathematical knowledge

**Lagrange error bound.** Hypotheses: f has derivatives of the required order on the interval between the centre a and the input x, and the absolute value of the n plus first derivative is at most M there. Conclusion: the absolute error of the nth degree Taylor polynomial at x is at most M multiplied by the absolute value of x minus a to the n plus first power, divided by n plus one factorial (BC-EK-LIM-8C1).

**Alternating alternative.** In some situations the alternating series error bound can bound the error of a Taylor polynomial approximation instead (BC-EK-LIM-8C2).

**Presentation.** The form of the bound and the final comparison are scored separately; a response that writes the error as equal to the bound, rather than at most the bound, does not earn the comparison point (sg-23:20).

**Notation.** The maximum of the absolute value of the derivative over the closed interval, factorial notation, and the inequality symbol at most.

### Representations

Representations in play: BC-REP-01 Symbolic expression, BC-REP-04 Verbal description.

Conversions tested: a supplied derivative bound and an input to an assembled bound expression (BC-REP-04 to BC-REP-01) and an evaluated bound to an inequality chain (BC-REP-01 to BC-REP-04).

### Assessment behaviour

MCQ forms ask for the form of the bound or for which degree brings the bound under a tolerance. FRQ forms supply a bound on the fifth derivative on a stated interval and ask a response to show that a fourth degree approximation is within a given tolerance, with one point for the form of the bound and one for communicating the inequality against the tolerance (sg-23:20). Parts are no calculator. Subsequent simplification errors after a correct form cost the second point but not the first (sg-23:20).

### Archetypes

- BC-QA-10008 Alternating series error bound compared with a tolerance
- BC-QA-10009 Lagrange error bound with a supplied derivative bound

### Errors and misconceptions

- BC-ERR-10026 Error written as equal to the bounding term
- BC-ERR-10027 Comparison with the tolerance left incomplete
- BC-ERR-10032 Lagrange bound assembled in the wrong form
- BC-ERR-10033 Error bound chosen whose conditions the situation does not meet
- BC-MIS-10017 An error bound can be used without checking its conditions, severity high
- BC-MIS-10018 The bound is the error, severity high

### Diagnostic signals

- BC-SIG-10017 The bound is assembled with the derivative of the same order as the polynomial rather than one order higher.

### Adaptive metadata summary

Skills in this topic carry calculator relevance none. Remediation targets named across the topic: BC-PRQ-06005, BC-PRQ-10001, BC-PRQ-10002. Every skill record carries the full seven key adaptive block in data/staging/unit-10.skills.json. [inferred]

## 10.13 Radius and Interval of Convergence of Power Series

### Official mapping

Topic id BC-TOP-1013, CED code 10.13, name Radius and Interval of Convergence of Power Series, scope BC_only, CED page 198. [verified] (ced:198)

- BC-LO-LIM-8D (LIM-8.D): Determine the radius of convergence and interval of convergence for a power series.
  - BC-EK-LIM-8D1 (LIM-8.D.1): "A power series is a series of the form the sum from n = 0 to infinity of a sub n (x - r)^n, where n is a non-negative integer, {a sub n} is a sequence of real numbers, and r is a real number."
  - BC-EK-LIM-8D2 (LIM-8.D.2): "If a power series converges, it either converges at a single point or has an interval of convergence."
  - BC-EK-LIM-8D3 (LIM-8.D.3): "The ratio test can be used to determine the radius of convergence of a power series."
  - BC-EK-LIM-8D4 (LIM-8.D.4): "The radius of convergence of a power series can be used to identify an open interval on which the series converges, but it is necessary to test both endpoints of the interval to determine the interval of convergence."
  - BC-EK-LIM-8D5 (LIM-8.D.5): "If a power series has a positive radius of convergence, then the power series is the Taylor series of the function to which it converges over the open interval."
  - BC-EK-LIM-8D6 (LIM-8.D.6): "The radius of convergence of a power series obtained by term-by-term differentiation or term- by-term integration is the same as the radius of convergence of the original power series."

Suggested practice skills: BC-MPS-2C (Practice skill 2.C). Weighting pointer: [../exam/exam-blueprint.md](../exam/exam-blueprint.md).

### Concept breakdown

- BC-CON-10020 Power series and their centre: A power series is built from powers of x minus a fixed number.
- BC-CON-10021 Radius of convergence from the ratio test: The ratio test turns a power series into an inequality that bounds the distance from the centre.
- BC-CON-10022 Endpoint testing and the interval of convergence: The two ends of the interval have to be checked one at a time with a suitable test.

- BC-SKL-10053 Identify a power series and its centre: Read off the number the powers are taken around.
- BC-SKL-10054 Apply the ratio test to a power series: Form the ratio of consecutive terms of the series in x and take its limit.
- BC-SKL-10055 Solve the ratio inequality for the interior of the interval: Turn the inequality in absolute value into a two sided inequality in x.
- BC-SKL-10056 State the radius of convergence explicitly: Name the radius as a number, not as an interval.
- BC-SKL-10057 Substitute each endpoint to produce the two numerical series: Put each endpoint value into the general term and simplify to a series of numbers.
- BC-SKL-10058 Test each endpoint series with an appropriate test: Apply a test that fits each endpoint series, which may differ between the two ends.
- BC-SKL-10059 State the interval of convergence with the correct endpoint inclusion: Report the interval with each end open or closed as its test showed.

Granularity note: Topic 10.13 carries seven skills because the 2025 scoring guideline allots five separate points inside one part, for the ratio, the limit, the interior, the endpoint consideration, and the endpoint analysis with the interval, and because the CED separates the radius (BC-EK-LIM-8D3) from the interval that requires endpoint testing (BC-EK-LIM-8D4). Each scored step is independently testable.

### Prerequisites

- BC-PRQ-10008 -> BC-SKL-10053, supporting, [inferred], Prerequisite for Identify a power series and its centre.
- BC-PRQ-10002 -> BC-SKL-10054, supporting, [inferred], Prerequisite for Apply the ratio test to a power series.
- BC-PRQ-10007 -> BC-SKL-10054, supporting, [inferred], Prerequisite for Apply the ratio test to a power series.
- BC-PRQ-10004 -> BC-SKL-10054, supporting, [inferred], Prerequisite for Apply the ratio test to a power series.
- BC-PRQ-10001 -> BC-SKL-10055, supporting, [inferred], Prerequisite for Solve the ratio inequality for the interior of the interval.
- BC-PRQ-10006 -> BC-SKL-10055, supporting, [inferred], Prerequisite for Solve the ratio inequality for the interior of the interval.
- BC-PRQ-10001 -> BC-SKL-10056, supporting, [inferred], Prerequisite for State the radius of convergence explicitly.
- BC-PRQ-10008 -> BC-SKL-10057, supporting, [inferred], Prerequisite for Substitute each endpoint to produce the two numerical series.
- BC-PRQ-06002 -> BC-SKL-10057, supporting, [inferred], Prerequisite for Substitute each endpoint to produce the two numerical series.
- BC-PRQ-06005 -> BC-SKL-10058, supporting, [inferred], Prerequisite for Test each endpoint series with an appropriate test.
- BC-PRQ-10006 -> BC-SKL-10059, supporting, [inferred], Prerequisite for State the interval of convergence with the correct endpoint inclusion.

### Required mathematical knowledge

**Power series.** A power series has the form the sum of a sub n times x minus r to the n, with r the centre (BC-EK-LIM-8D1). A convergent power series converges either at a single point or on an interval (BC-EK-LIM-8D2).

**Radius by ratio test.** The ratio test determines the radius of convergence (BC-EK-LIM-8D3).

**Endpoints.** The radius identifies an open interval of convergence, and both endpoints must be tested to determine the interval of convergence (BC-EK-LIM-8D4). Naming an appropriate test at each endpoint suffices for the analysis, and direct comparison, limit comparison, or the integral test are accepted alongside the model solution's tests (sg-25:25).

**Taylor identification.** A power series with a positive radius of convergence is the Taylor series of the function to which it converges on the open interval (BC-EK-LIM-8D5).

**Presentation.** The interior must be given as a compound inequality or interval, since an inequality in absolute value alone is not sufficient (sg-22:21, sg-25:25). A radius must be named as a radius; an interval alone does not earn the radius point (sg-21:24).

### Representations

Representations in play: BC-REP-11 Series, BC-REP-01 Symbolic expression, BC-REP-04 Verbal description.

Conversions tested: power series to a ratio and its limit (BC-REP-11 to BC-REP-01), inequality to an interval (BC-REP-01 to BC-REP-01), and endpoint value to a numerical series (BC-REP-01 to BC-REP-11).

### Assessment behaviour

MCQ forms ask for the radius or for the interval of a given power series. FRQ forms make this the opening part of the series question, with five points distributed over the ratio, its limit, the interior, considering both endpoints, and the analysis with the final interval (sg-25:24), or four points when the endpoints share an argument (sg-22:20). A separate form asks only for the radius, with points for the ratio, the limit, and the explicit radius (sg-21:24). Parts are no calculator. A reciprocal ratio keeps a response eligible for every point except the final interval point (sg-25:25), and endpoint consideration is scored even when the interior found earlier was wrong (sg-25:25).

### Archetypes

- BC-QA-10013 Interval of convergence by the ratio test with endpoint analysis
- BC-QA-10014 Radius of convergence from a given series
- BC-QA-10015 Endpoint series identified and tested

### Errors and misconceptions

- BC-ERR-10015 Endpoint series analysed with a test whose conditions it fails
- BC-ERR-10017 Limit taken without limit notation
- BC-ERR-10021 Index substitution incomplete in the ratio of consecutive terms
- BC-ERR-10034 Endpoint value substituted into the wrong place in the general term
- BC-ERR-10035 Absolute value dropped when the ratio inequality is solved
- BC-ERR-10036 Interval presented where the radius of convergence was requested
- BC-ERR-10037 Endpoints of the interval left untested
- BC-ERR-10038 Interval reported with endpoint inclusion that contradicts the endpoint analysis
- BC-MIS-10007 A convergence test can be applied without checking its conditions, severity high
- BC-MIS-10014 The ratio test settles every series, severity medium
- BC-MIS-10022 Radius and interval of convergence are interchangeable, severity medium
- BC-MIS-10023 The open interval from the ratio test is the interval of convergence, severity high
- BC-MIS-10024 The two endpoints behave the same way, severity medium

### Diagnostic signals

- BC-SIG-10003 The reciprocal of the required ratio is presented and carried through consistently.
- BC-SIG-10004 The open interval is reported as the interval of convergence with no endpoint work shown.
- BC-SIG-10005 One endpoint is tested correctly and the verdict is transferred to the other without a second test.
- BC-SIG-10006 An endpoint series of positive terms is analysed with the alternating series test, or an alternating one with a direct comparison.
- BC-SIG-10007 The inequality is solved without absolute value and a one sided interval is reported.
- BC-SIG-10008 A correct interval is presented where the radius was requested, with no value named as the radius.

### Adaptive metadata summary

Skills in this topic carry calculator relevance none. Remediation targets named across the topic: BC-PRQ-06005, BC-PRQ-10001, BC-PRQ-10002, BC-PRQ-10006, BC-PRQ-10008. Every skill record carries the full seven key adaptive block in data/staging/unit-10.skills.json. [inferred]

## 10.14 Finding Taylor or Maclaurin Series for a Function

### Official mapping

Topic id BC-TOP-1014, CED code 10.14, name Finding Taylor or Maclaurin Series for a Function, scope BC_only, CED page 199. [verified] (ced:199)

- BC-LO-LIM-8E (LIM-8.E): Represent a function as a Taylor series or a Maclaurin series.
  - BC-EK-LIM-8E1 (LIM-8.E.1): "A Taylor polynomial for f (x) is a partial sum of the Taylor series for f (x)."
- BC-LO-LIM-8F (LIM-8.F): Interpret Taylor series and Maclaurin series.
  - BC-EK-LIM-8F1 (LIM-8.F.1): "The Maclaurin series for 1/(1 - x) is a geometric series."
  - BC-EK-LIM-8F2 (LIM-8.F.2): "The Maclaurin series for sin x, cos x, and ex provides the foundation for constructing the Maclaurin series for other functions."

Suggested practice skills: BC-MPS-2C (Practice skill 2.C). Weighting pointer: [../exam/exam-blueprint.md](../exam/exam-blueprint.md).

### Concept breakdown

- BC-CON-10023 Taylor series and the general term: The Taylor series continues the polynomial pattern without stopping.
- BC-CON-10024 The standard Maclaurin series: Four series are recalled rather than rederived.

- BC-SKL-10060 Write the general term of a Taylor series: Give the pattern that produces every term, with the index in it.
- BC-SKL-10061 Recall the Maclaurin series for the exponential function: Write the series for e to the x from memory.
- BC-SKL-10062 Recall the Maclaurin series for sine and cosine: Write the sine and cosine series from memory, with the correct parities.
- BC-SKL-10063 Recall the Maclaurin series for one over one minus x: Write the geometric series for one over one minus x and its interval.
- BC-SKL-10064 Construct a Maclaurin series by substitution into a known series: Replace x in a known series by the expression given and simplify.
- BC-SKL-10065 Construct a series by multiplying a known series by an expression: Multiply every term of a known series by the given factor.
- BC-SKL-10066 Evaluate a Taylor series at a point to obtain a numerical series: Substitute the input into the series and read the numbers that result.
- BC-SKL-10067 Identify a Taylor polynomial as a partial sum of the Taylor series: Say that cutting the series off at a degree gives the polynomial.

Granularity note: Topic 10.14 carries eight skills because the CED lists both the general term construction from derivatives (BC-EK-LIM-8E1) and three distinct recall targets in BC-EK-LIM-8F1 and BC-EK-LIM-8F2, and because the construction operations of substitution and multiplication are scored separately from recall in the official material. Recall of the exponential, the trigonometric, and the geometric series is kept as three skills because a student may hold one and not another.

### Prerequisites

- BC-PRQ-10008 -> BC-SKL-10060, supporting, [inferred], Prerequisite for Write the general term of a Taylor series.
- BC-PRQ-10003 -> BC-SKL-10060, supporting, [inferred], Prerequisite for Write the general term of a Taylor series.
- BC-PRQ-10002 -> BC-SKL-10061, supporting, [inferred], Prerequisite for Recall the Maclaurin series for the exponential function.
- BC-PRQ-10002 -> BC-SKL-10062, supporting, [inferred], Prerequisite for Recall the Maclaurin series for sine and cosine.
- BC-PRQ-10008 -> BC-SKL-10062, supporting, [inferred], Prerequisite for Recall the Maclaurin series for sine and cosine.
- BC-PRQ-10005 -> BC-SKL-10063, supporting, [inferred], Prerequisite for Recall the Maclaurin series for one over one minus x.
- BC-PRQ-06002 -> BC-SKL-10064, supporting, [inferred], Prerequisite for Construct a Maclaurin series by substitution into a known series.
- BC-PRQ-10007 -> BC-SKL-10064, supporting, [inferred], Prerequisite for Construct a Maclaurin series by substitution into a known series.
- BC-PRQ-06002 -> BC-SKL-10065, supporting, [inferred], Prerequisite for Construct a series by multiplying a known series by an expression.
- BC-PRQ-10008 -> BC-SKL-10066, supporting, [inferred], Prerequisite for Evaluate a Taylor series at a point to obtain a numerical series.
- BC-PRQ-06002 -> BC-SKL-10066, supporting, [inferred], Prerequisite for Evaluate a Taylor series at a point to obtain a numerical series.
- BC-PRQ-06005 -> BC-SKL-10067, supporting, [inferred], Prerequisite for Identify a Taylor polynomial as a partial sum of the Taylor series.

### Required mathematical knowledge

**Taylor series.** A Taylor polynomial for f is a partial sum of the Taylor series for f (BC-EK-LIM-8E1), whose nth term uses the nth derivative at the centre divided by n factorial (BC-EK-LIM-8A1).

**Standard series.** The Maclaurin series for one over one minus x is a geometric series (BC-EK-LIM-8F1). The Maclaurin series for sin x, cos x, and e to the x are the foundation for constructing other Maclaurin series (BC-EK-LIM-8F2).

**Construction.** A power series for a given function can be derived from a known series by substitution, by algebraic operations, by term-by-term differentiation, or by term-by-term integration (BC-EK-LIM-8G1).

**Caution.** Recognising that a function's series exists does not by itself establish that the function equals the sum of its Maclaurin series on the interval of convergence; a 2023 scoring guideline notes this explicitly while accepting the identification (sg-23:21).

**Notation.** Sigma notation with a general term, factorials, and the alternating factor.

### Representations

Representations in play: BC-REP-11 Series, BC-REP-01 Symbolic expression, BC-REP-04 Verbal description.

Conversions tested: first terms to a general term (BC-REP-11 to BC-REP-01), a function to a series through substitution into a known series (BC-REP-01 to BC-REP-11), and a series evaluated at a point to a numerical series (BC-REP-11 to BC-REP-11).

### Assessment behaviour

MCQ forms ask for the coefficient of a named power in a series built by substitution, or for the general term. FRQ forms ask for the first three nonzero terms and the general term of a series, scored as two separate points (sg-25:26), for the general term of a differentiated series (sg-24:22), or for a polynomial built from known series in an accepted alternate solution (sg-23:21). Parts are no calculator. Recall of the standard series is scored indirectly, since a response that misremembers one loses the terms that depend on it.

### Archetypes

- BC-QA-10002 Value of a convergent series requested
- BC-QA-10003 Geometric series summed in closed form
- BC-QA-10008 Alternating series error bound compared with a tolerance
- BC-QA-10012 Taylor polynomial for a related function built from a known series
- BC-QA-10016 First nonzero terms and the general term of a series
- BC-QA-10017 Maclaurin series built from a known series by substitution or multiplication
- BC-QA-10018 Series differentiated term by term with its radius carried over

### Errors and misconceptions

- BC-ERR-10005 Geometric sum formula applied with a ratio of size at least one
- BC-ERR-10030 Polynomial presented with extra terms or a trailing ellipsis
- BC-ERR-10034 Endpoint value substituted into the wrong place in the general term
- BC-ERR-10039 General term of a series mis-differentiated or mis-assembled
- BC-ERR-10040 Standard Maclaurin series recalled incorrectly
- BC-ERR-10041 Substitution into a known series carried out incorrectly
- BC-MIS-10003 The geometric sum formula applies to any series that shrinks, severity medium
- BC-MIS-10020 A Taylor polynomial and a Taylor series are interchangeable, severity medium
- BC-MIS-10021 A function equals its Maclaurin series everywhere, severity high
- BC-MIS-10026 Substituting into a known series changes where it is centred, severity medium

### Diagnostic signals

- BC-SIG-10021 The first nonzero terms are correct and the general term does not reproduce them.

### Adaptive metadata summary

Skills in this topic carry calculator relevance none. Remediation targets named across the topic: BC-PRQ-06002, BC-PRQ-06005, BC-PRQ-10002, BC-PRQ-10005, BC-PRQ-10008. Every skill record carries the full seven key adaptive block in data/staging/unit-10.skills.json. [inferred]

## 10.15 Representing Functions as Power Series

### Official mapping

Topic id BC-TOP-1015, CED code 10.15, name Representing Functions as Power Series, scope BC_only, CED page 200. [verified] (ced:200)

- BC-LO-LIM-8G (LIM-8.G): Represent a given function as a power series.
  - BC-EK-LIM-8G1 (LIM-8.G.1): "Using a known series, a power series for a given function can be derived using operations such as term-by-term differentiation or term-by- term integration, and by various methods (e.g., algebraic processes, substitutions, or using properties of geometric series)."

Suggested practice skills: BC-MPS-3D (Practice skill 3.D). Weighting pointer: [../exam/exam-blueprint.md](../exam/exam-blueprint.md).

### Concept breakdown

- BC-CON-10025 Term-by-term differentiation and integration of a power series: A power series can be differentiated or integrated one term at a time.
- BC-CON-10026 Radius preserved and endpoints rechecked: The derived series reaches just as far, but the ends may behave differently.

- BC-SKL-10068 Differentiate a power series term by term: Differentiate each term, including the general term.
- BC-SKL-10069 Integrate a power series term by term and determine the constant: Antidifferentiate each term and fix the constant from a known value.
- BC-SKL-10070 Apply the preserved radius to a differentiated or integrated series: Carry the radius across to the new series without recomputing it.
- BC-SKL-10071 Recheck the endpoints for a derived power series: Test the ends again for the new series rather than copying the old interval.
- BC-SKL-10072 Represent a power series in closed form by recognising a geometric series: Match the series to the geometric pattern and write the function it sums to.
- BC-SKL-10073 Decide whether a series converges to the function at a stated input: Check whether the input lies inside the interval and say what follows.

### Prerequisites

- BC-PRQ-06002 -> BC-SKL-10068, supporting, [inferred], Prerequisite for Differentiate a power series term by term.
- BC-PRQ-10008 -> BC-SKL-10068, supporting, [inferred], Prerequisite for Differentiate a power series term by term.
- BC-PRQ-06002 -> BC-SKL-10069, supporting, [inferred], Prerequisite for Integrate a power series term by term and determine the constant.
- BC-PRQ-06013 -> BC-SKL-10069, supporting, [inferred], Prerequisite for Integrate a power series term by term and determine the constant.
- BC-PRQ-06005 -> BC-SKL-10070, supporting, [inferred], Prerequisite for Apply the preserved radius to a differentiated or integrated series.
- BC-PRQ-10008 -> BC-SKL-10071, supporting, [inferred], Prerequisite for Recheck the endpoints for a derived power series.
- BC-PRQ-10006 -> BC-SKL-10071, supporting, [inferred], Prerequisite for Recheck the endpoints for a derived power series.
- BC-PRQ-10005 -> BC-SKL-10072, supporting, [inferred], Prerequisite for Represent a power series in closed form by recognising a geometric series.
- BC-PRQ-10001 -> BC-SKL-10072, supporting, [inferred], Prerequisite for Represent a power series in closed form by recognising a geometric series.
- BC-PRQ-10006 -> BC-SKL-10073, supporting, [inferred], Prerequisite for Decide whether a series converges to the function at a stated input.

### Required mathematical knowledge

**Construction.** Using a known series, a power series for a given function can be derived by term-by-term differentiation, by term-by-term integration, and by algebraic processes, substitutions, or properties of geometric series (BC-EK-LIM-8G1).

**Radius.** Hypotheses: a power series with radius of convergence R. Conclusion: the series obtained by term-by-term differentiation or integration has the same radius R (BC-EK-LIM-8D6). The endpoints are not covered by this statement and must be tested for the new series (BC-EK-LIM-8D4).

**Identification.** A power series with positive radius of convergence is the Taylor series of the function to which it converges on the open interval (BC-EK-LIM-8D5).

**Notation.** Term-by-term operations written on both the displayed terms and the general term, plus a constant of integration determined from a given value.

### Representations

Representations in play: BC-REP-11 Series, BC-REP-01 Symbolic expression, BC-REP-04 Verbal description.

Conversions tested: a series to the series of its derivative or antiderivative (BC-REP-11 to BC-REP-11), a geometric power series to a closed form function (BC-REP-11 to BC-REP-01), and an interval of convergence to a verdict about a specific input (BC-REP-01 to BC-REP-04).

### Assessment behaviour

MCQ forms ask for a series representation of a function built from a known series by an operation. FRQ forms ask for the first three nonzero terms and the general term of a differentiated series, each a separate point (sg-25:26), for the general term together with the radius of the differentiated series, where the radius point rests on the preservation statement (sg-24:22), for a verification that a geometric series sums to a given closed form (sg-25:26), and for a reasoned decision about convergence at a specific input, where a short answer naming the position relative to the interval earns the point (sg-25:27). Parts are no calculator. Multi-concept variants chain the interval from an earlier part into the decision at a point, and the guideline allows a conclusion consistent with an incorrect earlier interval (sg-25:27).

### Archetypes

- BC-QA-10003 Geometric series summed in closed form
- BC-QA-10015 Endpoint series identified and tested
- BC-QA-10018 Series differentiated term by term with its radius carried over
- BC-QA-10019 Function represented by term-by-term integration of a known series
- BC-QA-10020 Convergence to the function at a specified input decided with a reason

### Errors and misconceptions

- BC-ERR-10005 Geometric sum formula applied with a ratio of size at least one
- BC-ERR-10006 First term taken as the index zero term when the series starts elsewhere
- BC-ERR-10015 Endpoint series analysed with a test whose conditions it fails
- BC-ERR-10037 Endpoints of the interval left untested
- BC-ERR-10039 General term of a series mis-differentiated or mis-assembled
- BC-ERR-10042 Radius of a differentiated or integrated series recomputed or claimed to change
- BC-ERR-10043 Convergence at a specified input asserted without a reason
- BC-MIS-10003 The geometric sum formula applies to any series that shrinks, severity medium
- BC-MIS-10020 A Taylor polynomial and a Taylor series are interchangeable, severity medium
- BC-MIS-10021 A function equals its Maclaurin series everywhere, severity high
- BC-MIS-10022 Radius and interval of convergence are interchangeable, severity medium
- BC-MIS-10023 The open interval from the ratio test is the interval of convergence, severity high
- BC-MIS-10024 The two endpoints behave the same way, severity medium
- BC-MIS-10025 A differentiated or integrated series inherits the whole interval, severity high

### Diagnostic signals

- BC-SIG-10022 The differentiated series is correct and its radius is recomputed to a value inconsistent with the original.
- BC-SIG-10023 The verdict about convergence at a specific input is correct and no reason is attached.

### Adaptive metadata summary

Skills in this topic carry calculator relevance none. Remediation targets named across the topic: BC-PRQ-06002, BC-PRQ-06005, BC-PRQ-10005, BC-PRQ-10006, BC-PRQ-10008. Every skill record carries the full seven key adaptive block in data/staging/unit-10.skills.json. [inferred]

## Cross-unit connections

Unit 10 is the only unit whose objects are sequences and series, so its incoming dependencies are about limits, improper integrals, and antidifferentiation rather than about series themselves. [inferred]

The integral test skills BC-SKL-10014 through BC-SKL-10017 rest on improper integrals, which live in topic 6.13 of Unit 6 and are carried by BC-SKL-06067, BC-SKL-06068, and BC-SKL-06069 in data/skills.json; the same limit notation discipline that a 2021 guideline enforces for the integral test is enforced for improper integrals in Unit 6 (sg-21:22). [verified] (sg-21:22)

Term-by-term integration in topic 10.15 uses the antidifferentiation skills of topics 6.7 through 6.11, and the constant of integration is fixed the same way an initial condition fixes it in Unit 6 and in the differential equations of Unit 7. [inferred]

Limits of the general term, in BC-SKL-10001, BC-SKL-10011, and the ratio test skills, depend on limit evaluation for ratios of polynomial and exponential expressions. Unit 1 skills for limits do not yet exist in data/skills.json, so the prerequisite is carried here by BC-PRQ-10004 and, in the graph, by edges whose source is that prerequisite rather than a Unit 1 skill. [inferred]

Repeated differentiation for Taylor coefficients, in BC-SKL-10043 and BC-SKL-10047, depends on the product and chain rules of Units 2 and 3, which have no records in data/skills.json yet; BC-ERR-99013 records the chief reader finding about product rule omissions across the exam. [single-source] (cr-23:24)

Chief reader error records that cover this unit across years are BC-ERR-99016 for error bound conditions, BC-ERR-99017 for endpoint testing, BC-ERR-99018 for general terms of power series, BC-ERR-99037 for the absolute value inequality, BC-ERR-99038 for the value of a convergent series, and BC-ERR-99007 for limit notation with infinity. Each unit 10 error record that matches one of them names it in its notes field. [verified] (cr-22:30, cr-23:35, cr-24:36, crabbc-25:37)

## Archetype summary

Twenty archetypes are recorded in data/staging/unit-10.archetypes.json with fifty four variants. Fifteen are grounded in a scoring guideline from 2021 to 2025; the remainder are grounded in the CED text and in the nearest analogous scored part. [verified] (sg-21:21, sg-22:20, sg-23:19, sg-24:19, sg-25:24)

| Archetype | Name | Scope | Calculator | Official examples |
|---|---|---|---|---|
| BC-QA-10001 | Selecting a convergence test for a given series | BC_only | no_calculator | 2024 Q6(a), 2025 Q6(A) |
| BC-QA-10002 | Value of a convergent series requested | BC_only | no_calculator | none in 2021 to 2025 as a standalone part |
| BC-QA-10003 | Geometric series summed in closed form | BC_only | no_calculator | 2025 Q6(C) |
| BC-QA-10004 | Convergence or divergence established with a named test | BC_only | no_calculator | 2024 Q6(a) |
| BC-QA-10005 | Integral test with its conditions stated | BC_only | no_calculator | 2021 Q6(a) |
| BC-QA-10006 | Limit comparison used to classify a series | BC_only | no_calculator | 2021 Q6(b) |
| BC-QA-10007 | Absolute or conditional convergence classified | BC_only | no_calculator | 2021 Q6(b) |
| BC-QA-10008 | Alternating series error bound compared with a tolerance | BC_only | no_calculator | 2022 Q6(b), 2024 Q6(b), 2021 Q6(d) |
| BC-QA-10009 | Lagrange error bound with a supplied derivative bound | BC_only | no_calculator | 2023 Q6(b) |
| BC-QA-10010 | Taylor polynomial built from repeated differentiation of a relation | BC_only | no_calculator | 2023 Q6(a) |
| BC-QA-10011 | Taylor polynomial built from a table of derivative values | BC_only | no_calculator | none in 2021 to 2025 |
| BC-QA-10012 | Taylor polynomial for a related function built from a known series | BC_only | no_calculator | 2023 Q6(c) |
| BC-QA-10013 | Interval of convergence by the ratio test with endpoint analysis | BC_only | no_calculator | 2025 Q6(A), 2022 Q6(a) |
| BC-QA-10014 | Radius of convergence from a given series | BC_only | no_calculator | 2021 Q6(c) |
| BC-QA-10015 | Endpoint series identified and tested | BC_only | no_calculator | 2024 Q6(a), 2025 Q6(A), 2022 Q6(a) |
| BC-QA-10016 | First nonzero terms and the general term of a series | BC_only | no_calculator | 2025 Q6(B) |
| BC-QA-10017 | Maclaurin series built from a known series by substitution or multiplication | BC_only | no_calculator | 2023 Q6(c) alternate solution |
| BC-QA-10018 | Series differentiated term by term with its radius carried over | BC_only | no_calculator | 2024 Q6(c), 2025 Q6(B) |
| BC-QA-10019 | Function represented by term-by-term integration of a known series | BC_only | no_calculator | 2023 Q6(c) alternate solution |
| BC-QA-10020 | Convergence to the function at a specified input decided with a reason | BC_only | no_calculator | 2025 Q6(D) |

The BC series free response question is question 6 in each year read for this unit, and it is a no calculator question in Part B of Section II (sg-21:21, sg-22:20, sg-23:19, sg-24:19, sg-25:24). Across 2021 to 2025 it opened with an interval or radius of convergence part in 2021, 2022, and 2025, with a convergence test at an endpoint in 2024, and with a Taylor polynomial construction in 2023.

## Misconception summary

Twenty six misconceptions are recorded in data/staging/unit-10.misconceptions.json against forty three observed errors in data/staging/unit-10.errors.json. The mapping is many to many: an error lists every misconception that could produce it together with non-conceptual causes such as an arithmetic slip, a misread, or time pressure, and every misconception carries rival misconceptions and a discriminating probe. [verified] (sg-21:22, sg-22:21, sg-23:20, sg-24:21, sg-25:25)

The pair the brief singles out is recorded that way. BC-ERR-10008, convergence concluded because the terms approach zero, lists BC-MIS-10005, terms approaching zero make a series converge, and BC-MIS-10006, a test that establishes divergence also establishes convergence, as possible causes, and lists a rushed reading of the prompt and time pressure among its non-conceptual causes. BC-SIG-10001 is the signal that separates them: a student who withdraws the claim once the harmonic series is named was reading quickly, while one who defends it holds the converse. [verified] (ced:188, sg-24:19)

Absolute and conditional convergence are separated both as skills and as misconceptions. BC-SKL-10035 and BC-SKL-10036 are distinct skills, and BC-MIS-10015, the two labels are the same distinction, is distinct from BC-MIS-10016, conditional convergence is a weaker form of absolute convergence, with rearrangement as the discriminating probe. [verified] (ced:194)

| Misconception | Severity | Rivals | Discriminating probe |
|---|---|---|---|
| BC-MIS-10001 A sequence and its series are the same object | high | BC-MIS-10002, BC-MIS-10005 | Give one general term and ask separately whether the sequence converges and whether the series converges. |
| BC-MIS-10002 A partial sum is the value of the series | medium | BC-MIS-10001 | Ask for the third and the fourth partial sums and whether both can be the value of the series. |
| BC-MIS-10003 The geometric sum formula applies to any series that shrinks | medium | BC-MIS-10004, BC-MIS-10005 | Give a p-series and ask for its common ratio. |
| BC-MIS-10004 The first term of a geometric series is always the index zero term | medium | BC-MIS-10003 | Ask the student to write the first two terms of a series whose sigma notation starts at index two. |
| BC-MIS-10005 Terms approaching zero make a series converge | high | BC-MIS-10006, BC-MIS-10001 | Ask what the harmonic series does and whether its terms approach zero. |
| BC-MIS-10006 A test that establishes divergence also establishes convergence | high | BC-MIS-10005, BC-MIS-10007 | Ask what conclusion the nth term test permits when the limit is zero. |
| BC-MIS-10007 A convergence test can be applied without checking its conditions | high | BC-MIS-10006, BC-MIS-10024 | Ask the student to state the conditions of the chosen test and point to where each one holds. |
| BC-MIS-10008 The improper integral and the series have the same value | medium | BC-MIS-10002 | Ask whether the first term of the series equals the area over the first subinterval. |
| BC-MIS-10009 The p-series threshold is misplaced | medium | BC-MIS-10005 | Ask for the behaviour of the series with exponent one and with exponent two. |
| BC-MIS-10010 The comparison inequality works in either direction | high | BC-MIS-10011 | Ask what follows when the terms are larger than those of a convergent series. |
| BC-MIS-10011 The limit comparison value is compared with one | medium | BC-MIS-10010, BC-MIS-10014 | Ask what the limit comparison test concludes when the limit is three. |
| BC-MIS-10012 Alternating signs alone give convergence | high | BC-MIS-10013, BC-MIS-10005 | Give an alternating series whose terms do not approach zero and ask whether it converges. |
| BC-MIS-10013 Decreasing and tending to zero are a single condition | medium | BC-MIS-10012 | Ask for a sequence that decreases but does not approach zero. |
| BC-MIS-10014 The ratio test settles every series | medium | BC-MIS-10011, BC-MIS-10007 | Apply the ratio test to the harmonic series and ask what it shows. |
| BC-MIS-10015 Absolute and conditional convergence are the same distinction | high | BC-MIS-10016 | Ask which of the two tests was run and what the other one would show. |
| BC-MIS-10016 Conditional convergence is a weaker form of absolute convergence | medium | BC-MIS-10015 | Ask whether rearranging the terms of the alternating harmonic series must leave its value unchanged. |
| BC-MIS-10017 An error bound can be used without checking its conditions | high | BC-MIS-10018, BC-MIS-10007 | Ask what has to be true of the series before the alternating series error bound may be used. |
| BC-MIS-10018 The bound is the error | high | BC-MIS-10017 | Ask whether the approximation is off by exactly that amount or by at most that amount. |
| BC-MIS-10019 Taylor coefficients are the derivative values | high | BC-MIS-10020 | Ask what coefficient a second derivative of six produces in the second degree term. |
| BC-MIS-10020 A Taylor polynomial and a Taylor series are interchangeable | medium | BC-MIS-10019, BC-MIS-10021 | Ask how many terms the requested object has and whether it ends. |
| BC-MIS-10021 A function equals its Maclaurin series everywhere | high | BC-MIS-10023 | Ask at which inputs the series for one over one minus x gives the function value. |
| BC-MIS-10022 Radius and interval of convergence are interchangeable | medium | BC-MIS-10023 | Ask for the radius and for the interval of the same series in turn. |
| BC-MIS-10023 The open interval from the ratio test is the interval of convergence | high | BC-MIS-10024, BC-MIS-10022 | Ask what the ratio test says at an endpoint where the limit equals one. |
| BC-MIS-10024 The two endpoints behave the same way | medium | BC-MIS-10023, BC-MIS-10007 | Ask what the series becomes at each endpoint and whether the two look alike. |
| BC-MIS-10025 A differentiated or integrated series inherits the whole interval | high | BC-MIS-10022, BC-MIS-10024 | Ask what the CED guarantees about a term-by-term derivative and what it does not. |
| BC-MIS-10026 Substituting into a known series changes where it is centred | medium | BC-MIS-10021 | Ask what the centre of the resulting series is after the substitution and what its powers are in. |

The highest severity clusters are the four the scoring guidelines document directly: stopping at the interior of the interval and leaving the endpoints untested (BC-MIS-10023, BC-MIS-10024, sg-25:24), using an error bound without its conditions or writing the bound as the error (BC-MIS-10017, BC-MIS-10018, sg-22:21 and sg-23:20), attaching derivative values to powers without the factorials (BC-MIS-10019, sg-23:19), and treating a one way test as reversible (BC-MIS-10005, BC-MIS-10006, ced:188).

## Unresolved

- The CED attaches no essential knowledge statement to sequence convergence on its own; BC-EK-LIM-7A1 and BC-EK-LIM-7A2 define partial sums and the limit of the sequence of partial sums. BC-SKL-10001 records the sequence limit as a skill because the definition of series convergence cannot be applied without it, and it is tagged against ced:186 rather than against a statement of its own. [uncertain]
- No free response part in 2021 to 2025 builds a Taylor polynomial from a table of derivative values, so BC-QA-10012 is tagged inferred and its scoring pattern is drawn from the construction parts that do appear (sg-23:19). The same applies to BC-QA-10002, the value of a convergent series as a standalone request, whose grounding is a chief reader observation rather than a rubric (cr-22:30). [uncertain]
- Misconception literature for infinite series could not be confirmed from the sources available in this project's cache, so every misconception record is tagged verified only where a scoring guideline or the CED states the behaviour, and inferred otherwise. No author or year is cited. [inferred]
- The 2025 guideline accepts a reciprocal ratio for every point of the interval of convergence part except the final interval point (sg-25:25), while the 2022 guideline treats a substitution error in the exponent as blocking only the fourth point (sg-22:21). Whether these are the same banking principle stated twice or two question specific decisions is not established here. [uncertain]
- The CED page numbering in data/curriculum.json (pages 186 to 200) is the PDF page index; the printed page numbers on those pages run 181 to 195. Citations in this file use the PDF index to match cache/text/ced. [verified] (ced:186, ced:200)

<!-- generated:official-evidence:start -->

## Official evidence index [verified]

Generated from data/frq_records.json and data/mcq_records.json. Every record cites its cached document and page; counts are observations over the indexed years only, not predictions. FRQ part records with BC-UNIT-10 as primary or secondary unit: 45. Public sample MCQ records tagged to this unit: 15.

| FRQ record | Role | Calculator | Archetype | Skills (first six) | Points | Point types |
|---|---|---|---|---|---|---|
| BC-FRQ-2012-Q6-A | primary | no_calculator | BC-QA-10013 | BC-SKL-10053, BC-SKL-10054, BC-SKL-10031, BC-SKL-10032, BC-SKL-10055, BC-SKL-10057 | 5 | BC-PT-99042, BC-PT-99043, BC-PT-99044, BC-PT-99045, BC-PT-99046 |
| BC-FRQ-2012-Q6-B | primary | no_calculator | BC-QA-10008 | BC-SKL-10039, BC-SKL-10040, BC-SKL-10041, BC-SKL-10042 | 2 | BC-PT-99040, BC-PT-99041 |
| BC-FRQ-2012-Q6-C | primary | no_calculator | BC-QA-10018 | BC-SKL-10068, BC-SKL-10060, BC-SKL-10070 | 2 | BC-PT-99037, BC-PT-99038 |
| BC-FRQ-2013-Q6-A | primary | no_calculator | BC-QA-10010 | BC-SKL-10044, BC-SKL-10046, BC-SKL-10048, BC-SKL-10067 | 2 | BC-PT-99035, BC-PT-99068 |
| BC-FRQ-2013-Q6-B | primary | no_calculator | BC-QA-10010 | BC-SKL-10043, BC-SKL-10044, BC-SKL-10046 | 3 | BC-PT-99035, BC-PT-99036, BC-PT-99036 |
| BC-FRQ-2013-Q6-C | primary | no_calculator | BC-QA-10012 | BC-SKL-10047, BC-SKL-10064, BC-SKL-10069, BC-SKL-10044 | 4 | BC-PT-99037, BC-PT-99035, BC-PT-99036 |
| BC-FRQ-2014-Q6-A | primary | no_calculator | BC-QA-10014 | BC-SKL-10053, BC-SKL-10054, BC-SKL-10031, BC-SKL-10032, BC-SKL-10055, BC-SKL-10056 | 3 | BC-PT-99042, BC-PT-99043, BC-PT-99047 |
| BC-FRQ-2014-Q6-B | primary | no_calculator | BC-QA-10018 | BC-SKL-10068, BC-SKL-10060, BC-SKL-10070 | 3 | BC-PT-99037, BC-PT-99038 |
| BC-FRQ-2014-Q6-C | primary | no_calculator | BC-QA-10019 | BC-SKL-10006, BC-SKL-10008, BC-SKL-10072, BC-SKL-10069, BC-SKL-06052, BC-SKL-07029 | 3 | BC-PT-99067, BC-PT-99003, BC-PT-99004 |
| BC-FRQ-2015-Q6-A | primary | no_calculator | BC-QA-10014 | BC-SKL-10053, BC-SKL-10054, BC-SKL-10031, BC-SKL-10032, BC-SKL-10055, BC-SKL-10056 | 3 | BC-PT-99042, BC-PT-99043, BC-PT-99047 |
| BC-FRQ-2015-Q6-B | primary | no_calculator | BC-QA-10018 | BC-SKL-10068, BC-SKL-10006, BC-SKL-10008, BC-SKL-10072 | 3 | BC-PT-99037, BC-PT-99067 |
| BC-FRQ-2015-Q6-C | primary | no_calculator | BC-QA-10012 | BC-SKL-10061, BC-SKL-10065, BC-SKL-10047, BC-SKL-10067 | 3 | BC-PT-99037, BC-PT-99036 |
| BC-FRQ-2018-Q6-A | primary | no_calculator | BC-QA-10017 | BC-SKL-10064, BC-SKL-10065, BC-SKL-10060, BC-SKL-10063 | 0 |  |
| BC-FRQ-2018-Q6-B | primary | no_calculator | BC-QA-10013 | BC-SKL-10054, BC-SKL-10055, BC-SKL-10057, BC-SKL-10058, BC-SKL-10059, BC-SKL-10027 | 0 |  |
| BC-FRQ-2018-Q6-C | primary | no_calculator | BC-QA-10008 | BC-SKL-10039, BC-SKL-10040, BC-SKL-10041, BC-SKL-10067 | 0 |  |
| BC-FRQ-2019-Q6-A | primary | no_calculator | BC-QA-10011 | BC-SKL-10044, BC-SKL-10045, BC-SKL-10046 | 2 | BC-PT-99035, BC-PT-99036 |
| BC-FRQ-2019-Q6-B | primary | no_calculator | BC-QA-10012 | BC-SKL-10061, BC-SKL-10065, BC-SKL-10047 | 2 | BC-PT-99037, BC-PT-99035 |
| BC-FRQ-2019-Q6-C | primary | no_calculator | BC-QA-10019 | BC-SKL-10069, BC-SKL-10048, BC-SKL-06017, BC-SKL-06040 | 2 | BC-PT-99003, BC-PT-99004 |
| BC-FRQ-2019-Q6-D | primary | no_calculator | BC-QA-10008 | BC-SKL-10039, BC-SKL-10040, BC-SKL-10041, BC-SKL-10042, BC-SKL-10069 | 3 | BC-PT-99036, BC-PT-99040, BC-PT-99041 |
| BC-FRQ-2021-Q5-A | primary | no_calculator | BC-QA-10010 | BC-SKL-10043, BC-SKL-10044, BC-SKL-10048 | 2 | BC-PT-99035, BC-PT-99004 |
| BC-FRQ-2021-Q6-A | primary | no_calculator | BC-QA-10005 | BC-SKL-10014, BC-SKL-10015, BC-SKL-10016, BC-SKL-10017, BC-SKL-06067 | 3 | BC-PT-99005, BC-PT-99053, BC-PT-99003 |
| BC-FRQ-2021-Q6-B | primary | no_calculator | BC-QA-10006 | BC-SKL-10025, BC-SKL-10026, BC-SKL-10034, BC-SKL-10035 | 2 | BC-PT-99042, BC-PT-99005 |
| BC-FRQ-2021-Q6-C | primary | no_calculator | BC-QA-10014 | BC-SKL-10054, BC-SKL-10031, BC-SKL-10032, BC-SKL-10055, BC-SKL-10056 | 3 | BC-PT-99042, BC-PT-99043, BC-PT-99047 |
| BC-FRQ-2021-Q6-D | primary | no_calculator | BC-QA-10008 | BC-SKL-10039, BC-SKL-10040, BC-SKL-10041 | 1 | BC-PT-99040 |
| BC-FRQ-2022-Q6-A | primary | no_calculator | BC-QA-10013 | BC-SKL-10054, BC-SKL-10055, BC-SKL-10057, BC-SKL-10058, BC-SKL-10059, BC-SKL-10030 | 4 | BC-PT-99042, BC-PT-99044, BC-PT-99045, BC-PT-99046 |
| BC-FRQ-2022-Q6-B | primary | no_calculator | BC-QA-10008 | BC-SKL-10039, BC-SKL-10040, BC-SKL-10041, BC-SKL-10042, BC-SKL-10028, BC-SKL-10029 | 2 | BC-PT-99040, BC-PT-99041 |
| BC-FRQ-2022-Q6-C | primary | no_calculator | BC-QA-10018 | BC-SKL-10068, BC-SKL-10060, BC-SKL-10070 | 2 | BC-PT-99037, BC-PT-99038 |
| BC-FRQ-2022-Q6-D | primary | no_calculator | BC-QA-10003 | BC-SKL-10006, BC-SKL-10007, BC-SKL-10008, BC-SKL-10072 | 1 | BC-PT-99067 |
| BC-FRQ-2023-Q6-A | primary | no_calculator | BC-QA-10010 | BC-SKL-02036, BC-SKL-03002, BC-SKL-03031, BC-SKL-10043, BC-SKL-10044, BC-SKL-10046 | 4 | BC-PT-99022, BC-PT-99027, BC-PT-99035, BC-PT-99036 |
| BC-FRQ-2023-Q6-B | primary | no_calculator | BC-QA-10009 | BC-SKL-10049, BC-SKL-10050, BC-SKL-10051, BC-SKL-10048 | 2 | BC-PT-99039, BC-PT-99041 |
| BC-FRQ-2023-Q6-C | primary | no_calculator | BC-QA-10012 | BC-SKL-02036, BC-SKL-03030, BC-SKL-10044, BC-SKL-10047, BC-SKL-10065 | 3 | BC-PT-99027, BC-PT-99035, BC-PT-99036 |
| BC-FRQ-2024-Q6-A | primary | no_calculator | BC-QA-10004 | BC-SKL-10057, BC-SKL-10022, BC-SKL-10023, BC-SKL-10024, BC-SKL-10018 | 2 | BC-PT-99005, BC-PT-99005 |
| BC-FRQ-2024-Q6-B | primary | no_calculator | BC-QA-10008 | BC-SKL-10039, BC-SKL-10040, BC-SKL-10041, BC-SKL-10042 | 2 | BC-PT-99040, BC-PT-99041 |
| BC-FRQ-2024-Q6-C | primary | no_calculator | BC-QA-10018 | BC-SKL-10068, BC-SKL-10070, BC-SKL-10060, BC-SKL-10056 | 2 | BC-PT-99038, BC-PT-99047 |
| BC-FRQ-2024-Q6-D | primary | no_calculator | BC-QA-10014 | BC-SKL-10031, BC-SKL-10032, BC-SKL-10054, BC-SKL-10055, BC-SKL-10056 | 3 | BC-PT-99042, BC-PT-99043, BC-PT-99047 |
| BC-FRQ-2025-Q5-B | primary | no_calculator | BC-QA-10010 | BC-SKL-10044, BC-SKL-10043, BC-SKL-10067 | 2 | BC-PT-99035, BC-PT-99036 |
| BC-FRQ-2025-Q5-C | primary | no_calculator | BC-QA-10009 | BC-SKL-10049, BC-SKL-10050, BC-SKL-10051, BC-SKL-10048 | 2 | BC-PT-99039, BC-PT-99041 |
| BC-FRQ-2025-Q6-A | primary | no_calculator | BC-QA-10013 | BC-SKL-10054, BC-SKL-10031, BC-SKL-10032, BC-SKL-10055, BC-SKL-10057, BC-SKL-10058 | 5 | BC-PT-99042, BC-PT-99043, BC-PT-99044, BC-PT-99045, BC-PT-99046 |
| BC-FRQ-2025-Q6-B | primary | no_calculator | BC-QA-10018 | BC-SKL-10068, BC-SKL-10060, BC-SKL-10070 | 2 | BC-PT-99037, BC-PT-99038 |
| BC-FRQ-2025-Q6-C | primary | no_calculator | BC-QA-10003 | BC-SKL-10006, BC-SKL-10008, BC-SKL-10010, BC-SKL-10072 | 1 | BC-PT-99068 |
| BC-FRQ-2025-Q6-D | primary | no_calculator | BC-QA-10020 | BC-SKL-10073, BC-SKL-10070, BC-SKL-10007, BC-SKL-10059 | 1 | BC-PT-99005 |
| BC-FRQ-2026-Q6-A | primary | no_calculator | BC-QA-10003 | BC-SKL-10006, BC-SKL-10007, BC-SKL-10008, BC-SKL-10066 | 2 | BC-PT-99067, BC-PT-99004 |
| BC-FRQ-2026-Q6-B | primary | no_calculator | BC-QA-10018 | BC-SKL-10068, BC-SKL-10070, BC-SKL-10060 | 2 | BC-PT-99035, BC-PT-99036 |
| BC-FRQ-2026-Q6-C | primary | no_calculator | BC-QA-10008 | BC-SKL-10039, BC-SKL-10040, BC-SKL-10041, BC-SKL-10042, BC-SKL-10052 | 2 | BC-PT-99040, BC-PT-99041 |
| BC-FRQ-2026-Q6-D | primary | no_calculator | BC-QA-10017 | BC-SKL-10061, BC-SKL-10065, BC-SKL-10064, BC-SKL-10067 | 3 | BC-PT-99037, BC-PT-99035, BC-PT-99036 |

| MCQ record | Calculator | Archetype | Skills |
|---|---|---|---|
| BC-MCQ-CED-019 | no_calculator | BC-QA-10007 | BC-SKL-10034, BC-SKL-10036, BC-SKL-10030 |
| BC-MCQ-CED-020 | no_calculator | BC-QA-10018 | BC-SKL-10061, BC-SKL-10064, BC-SKL-10068 |
| BC-MCQ-CED-022 | calculator | BC-QA-10009 | BC-SKL-10049, BC-SKL-10050, BC-SKL-10051 |
| BC-MCQ-SAMPLE-020 | no_calculator | BC-QA-10008 | BC-SKL-10039, BC-SKL-10040, BC-SKL-10042 |
| BC-MCQ-SAMPLE-021 | no_calculator | BC-QA-10011 | BC-SKL-10045, BC-SKL-10044, BC-SKL-10046 |
| BC-MCQ-SAMPLE-022 | no_calculator | BC-QA-10007 | BC-SKL-10034, BC-SKL-10035, BC-SKL-10036 |
| BC-MCQ-SAMPLE-024 | calculator | BC-QA-10005 | BC-SKL-10014, BC-SKL-10015, BC-SKL-10017 |
| BC-MCQ-PE2012-005 | no_calculator | BC-QA-10003 | BC-SKL-10006, BC-SKL-10007, BC-SKL-10008 |
| BC-MCQ-PE2012-009 | no_calculator | BC-QA-10001 | BC-SKL-10021, BC-SKL-10031, BC-SKL-10022 |
| BC-MCQ-PE2012-013 | no_calculator | BC-QA-10014 | BC-SKL-10054, BC-SKL-10055, BC-SKL-10056 |
| BC-MCQ-PE2012-017 | no_calculator | BC-QA-10017 | BC-SKL-10062, BC-SKL-10065, BC-SKL-10064 |
| BC-MCQ-PE2012-022 | no_calculator | BC-QA-10013 | BC-SKL-10053, BC-SKL-10055, BC-SKL-10059 |
| BC-MCQ-PE2012-027 | no_calculator | BC-QA-10004 | BC-SKL-10019, BC-SKL-10007, BC-SKL-10018 |
| BC-MCQ-PE2012-032 | calculator | BC-QA-10010 | BC-SKL-10044, BC-SKL-10043, BC-SKL-10046 |
| BC-MCQ-PE2012-043 | calculator | BC-QA-10004 | BC-SKL-10023, BC-SKL-10024, BC-SKL-10011 |

<!-- generated:official-evidence:end -->
