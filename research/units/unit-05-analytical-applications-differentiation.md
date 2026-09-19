---
title: Unit 5, Applying Derivatives to Analyze Functions
research_date: 2026-09-19
status: draft
purpose: Decompose CED Unit 5 into concepts, atomic skills, non-calculus prerequisites, question archetypes and variants, observed errors, candidate misconceptions, and diagnostic signals, each grounded in the CED text and in the 2023 to 2025 official free-response questions and scoring guidelines, with particular attention to what a justification point requires.
---

# Unit 5, Applying Derivatives to Analyze Functions

BC-UNIT-05 covers CED pages 94 to 110 and holds twelve topics, all of them shared with AB; no topic in this unit carries the BC only marker in data/curriculum.json. Unit weighting is in [../exam/exam-blueprint.md](../exam/exam-blueprint.md) and exam composition is in [../exam/exam-structure.md](../exam/exam-structure.md). [verified] (ced:99, ced:110)

Justification is the organising demand of this unit. Nine of the thirteen archetypes recorded here carry a separately scored reason or justification point, and the scoring guidelines read for 2023 to 2025 are explicit about what those points require: a sign statement tied to the named function rather than a bare sign chart (sg-25:17), a global argument naming every candidate including both endpoints rather than a local derivative test (sg-23:15, sg-25:19), and a hypothesis sentence before any existence conclusion (sg-23:3). Those three standards are captured as separate skills, separate errors, and separate misconceptions throughout the file. [verified] (sg-23:3, sg-23:13, sg-23:14, sg-23:15, sg-25:17, sg-25:19)

## 5.1 Using the Mean Value Theorem

### Official mapping

Topic id BC-TOP-0501, CED code 5.1, name Using the Mean Value Theorem, scope shared, CED page 99. [verified] (ced:99)

- BC-LO-FUN-1B (FUN-1.B): Justify conclusions about functions by applying the Mean Value Theorem over an interval.
  - BC-EK-FUN-1B1 (FUN-1.B.1): "If a function f is continuous over the interval [a, b] and differentiable over the interval (a, b), then the Mean Value Theorem guarantees a point within that open interval where the instantaneous rate of change equals the average rate of change over the interval."

Suggested practice skills: BC-MPS-3E (Practice skill 3.E). Weighting pointer: [../exam/exam-blueprint.md](../exam/exam-blueprint.md).

### Concept breakdown

- BC-CON-05001 Mean Value Theorem as an existence result: On a closed interval where a function is continuous and differentiable inside, some interior point has instantaneous rate equal to the average rate.

- BC-SKL-05001 State the hypotheses of the Mean Value Theorem for a function and an interval: Say what must be true of the function before the theorem may be used.
- BC-SKL-05002 Verify that the hypotheses hold on the given interval: Check the given information really does supply continuity and differentiability.
- BC-SKL-05003 Compute the average rate of change over a closed interval: Work out the change in output divided by the change in input across the interval.
- BC-SKL-05004 Conclude that a point with the average rate exists on the open interval: State that some interior point has instantaneous rate equal to the average rate, and say why.
- BC-SKL-05005 Solve for a value of c that the theorem provides: Set the derivative equal to the average rate and solve.
- BC-SKL-05006 Justify that a derivative takes a particular value using equal endpoint outputs: When the two endpoint outputs agree, argue that the derivative must be zero somewhere between them.

### Prerequisites

- BC-PRQ-05004 -> BC-SKL-05001, supporting, [inferred], Prerequisite for State the hypotheses of the Mean Value Theorem for a function and an interval.
- BC-SKL-05001 -> BC-SKL-05002, hard_prerequisite, [inferred], Prerequisite for Verify that the hypotheses hold on the given interval.
- BC-PRQ-05008 -> BC-SKL-05003, supporting, [inferred], Prerequisite for Compute the average rate of change over a closed interval.
- BC-PRQ-06005 -> BC-SKL-05003, supporting, [inferred], Prerequisite for Compute the average rate of change over a closed interval.
- BC-SKL-05002 -> BC-SKL-05004, hard_prerequisite, [inferred], Prerequisite for Conclude that a point with the average rate exists on the open interval.
- BC-SKL-05003 -> BC-SKL-05004, hard_prerequisite, [inferred], Prerequisite for Conclude that a point with the average rate exists on the open interval.
- BC-SKL-05003 -> BC-SKL-05005, hard_prerequisite, [inferred], Prerequisite for Solve for a value of c that the theorem provides.
- BC-PRQ-05001 -> BC-SKL-05005, supporting, [inferred], Prerequisite for Solve for a value of c that the theorem provides.
- BC-SKL-05003 -> BC-SKL-05006, hard_prerequisite, [inferred], Prerequisite for Justify that a derivative takes a particular value using equal endpoint outputs.
- BC-SKL-05004 -> BC-SKL-05006, hard_prerequisite, [inferred], Prerequisite for Justify that a derivative takes a particular value using equal endpoint outputs.
- BC-TOP-0102 -> BC-SKL-05002, hard_prerequisite, [inferred], Continuity on an interval, a Unit 1 skill not yet in data/skills.json; the topic id stands in for it.

### Required mathematical knowledge

**Mean Value Theorem.** Hypotheses: f is continuous on the closed interval [a,b] and differentiable on the open interval (a,b). Conclusion: there is at least one c in (a,b) with f'(c) equal to the average rate of change of f over [a,b] (BC-EK-FUN-1B1).

**Rolle case.** When f(a) equals f(b), the average rate of change is zero and the conclusion becomes f'(c) equal to zero. The 2023 scoring guideline accepted a reference to either the Mean Value Theorem or Rolle's Theorem and rejected a reference to the Intermediate Value Theorem (sg-23:3).

**Differentiability supplies continuity.** A response that is told the function is differentiable earns the continuity hypothesis by saying so; the 2023 guideline made stating that step a condition of the justification point (sg-23:3).

**Notation.** f'(c); the average rate of change written as a quotient of a difference of outputs over a difference of inputs; the strict inequalities a < c < b.

### Representations

Representations in play: BC-REP-01 Symbolic (analytical) expression, BC-REP-03 Numerical table, BC-REP-04 Verbal description, BC-REP-05 Contextual model.

Conversions tested: table of values to an average rate of change and then to an existence claim (BC-REP-03 to BC-REP-04), and symbolic function to a solved value of c (BC-REP-01 to BC-REP-01).

### Assessment behaviour

MCQ forms give a function and an interval and ask for the value of c, or ask which hypothesis fails for a function that is not differentiable somewhere inside the interval. FRQ forms embed the theorem in a table question and score the arithmetic setup and the justification as separate points (sg-23:3, sg-25:4). Calculator variants supply a modelled function whose equation is solved numerically (sg-25:4); no-calculator variants supply a short table. Conceptual variants ask only whether the hypotheses hold; computational variants ask for c; interpretation variants ask what the conclusion means for the modelled quantity; justification variants demand the continuity statement, the equal-outputs or average-rate computation, and an affirmative answer, all three (sg-23:3). Multi-concept variants put the theorem in the same question as a Riemann sum or an average value.

### Archetypes

- BC-QA-05001 Mean Value Theorem existence justification on an interval
- BC-QA-05002 Solving for the value the Mean Value Theorem provides

### Errors and misconceptions

- BC-ERR-05001 Theorem hypotheses not stated before the conclusion is used
- BC-ERR-99008 Chief Reader error record, see data/errors.json
- BC-ERR-05002 Continuity not drawn from the given differentiability
- BC-ERR-05003 Average rate of change formed incorrectly
- BC-ERR-05004 Existence asserted with no affirmative answer or no theorem
- BC-ERR-99001 Chief Reader error record, see data/errors.json
- BC-ERR-05005 Solved value reported outside the open interval
- BC-ERR-05006 Intermediate Value Theorem cited for a claim about the derivative
- BC-MIS-05001 Hypotheses are decoration and the conclusion is the theorem, severity high
- BC-MIS-05002 Naming a theorem is itself a justification, severity high
- BC-MIS-05003 Average rate of change is the average of the endpoint values, severity medium
- BC-MIS-05004 An existence theorem locates the point it asserts, severity medium
- BC-MIS-05005 One existence theorem serves for claims about values and about derivatives, severity high

### Diagnostic signals

- BC-SIG-05001 Conclusion correct with no hypothesis sentence
- BC-SIG-05002 Endpoint values averaged instead of a difference quotient
- BC-SIG-05003 Existence argued with the wrong theorem named
- BC-SIG-05004 Correct equation solved with a root outside the interval reported

### Adaptive metadata summary

Skills in this topic carry calculator relevance none, optional. Remediation targets named across the topic: BC-PRQ-05001, BC-PRQ-05004, BC-PRQ-05008, BC-SKL-05001, BC-SKL-05002, BC-SKL-05003. Every skill record carries the full seven key adaptive block in data/staging/unit-05.skills.json. [inferred]

## 5.2 Extreme Value Theorem, Global Versus Local Extrema, and Critical Points

### Official mapping

Topic id BC-TOP-0502, CED code 5.2, name Extreme Value Theorem, Global Versus Local Extrema, and Critical Points, scope shared, CED page 100. [verified] (ced:100)

- BC-LO-FUN-1C (FUN-1.C): Justify conclusions about functions by applying the Extreme Value Theorem.
  - BC-EK-FUN-1C1 (FUN-1.C.1): "If a function f is continuous over the interval [a, b], then the Extreme Value Theorem guarantees that f has at least one minimum value and at least one maximum value on [a, b]."
  - BC-EK-FUN-1C2 (FUN-1.C.2): "A point on a function where the first derivative equals zero or fails to exist is a critical point of the function."
  - BC-EK-FUN-1C3 (FUN-1.C.3): "All local (relative) extrema occur at critical points of a function, though not all critical points are local extrema."

Suggested practice skills: BC-MPS-3E (Practice skill 3.E). Weighting pointer: [../exam/exam-blueprint.md](../exam/exam-blueprint.md).

### Concept breakdown

- BC-CON-05002 Extreme Value Theorem as an existence result: A function continuous on a closed interval attains both a smallest and a largest value somewhere on that interval.
- BC-CON-05003 Critical points and the local versus global distinction: A critical point is an input where the derivative is zero or does not exist, and being a critical point does not by itself make a point extreme.

- BC-SKL-05007 State the hypothesis of the Extreme Value Theorem: Say that the function must be continuous on a closed interval.
- BC-SKL-05008 Verify continuity on the closed interval before applying the theorem: Check that the given information supplies continuity on the whole closed interval.
- BC-SKL-05009 Conclude that a minimum value and a maximum value exist: State that the function reaches a lowest and a highest value on the interval.
- BC-SKL-05010 Determine critical points where the first derivative equals zero: Solve the derivative equal to zero and keep the solutions in the domain.
- BC-SKL-05011 Determine critical points where the first derivative fails to exist: Find the domain inputs where the derivative does not exist.
- BC-SKL-05012 Distinguish a relative extremum from an absolute extremum: Say whether a claim is about nearby values or about the whole interval.
- BC-SKL-05013 Explain why a critical point need not be a relative extremum: Give a case where the derivative is zero but the function keeps going the same way.

### Prerequisites

- BC-PRQ-05004 -> BC-SKL-05007, supporting, [inferred], Prerequisite for State the hypothesis of the Extreme Value Theorem.
- BC-SKL-05007 -> BC-SKL-05008, hard_prerequisite, [inferred], Prerequisite for Verify continuity on the closed interval before applying the theorem.
- BC-SKL-05008 -> BC-SKL-05009, hard_prerequisite, [inferred], Prerequisite for Conclude that a minimum value and a maximum value exist.
- BC-PRQ-05001 -> BC-SKL-05010, supporting, [inferred], Prerequisite for Determine critical points where the first derivative equals zero.
- BC-PRQ-05003 -> BC-SKL-05010, supporting, [inferred], Prerequisite for Determine critical points where the first derivative equals zero.
- BC-PRQ-05001 -> BC-SKL-05011, supporting, [inferred], Prerequisite for Determine critical points where the first derivative fails to exist.
- BC-PRQ-05003 -> BC-SKL-05011, supporting, [inferred], Prerequisite for Determine critical points where the first derivative fails to exist.
- BC-PRQ-05006 -> BC-SKL-05012, supporting, [inferred], Prerequisite for Distinguish a relative extremum from an absolute extremum.
- BC-SKL-05010 -> BC-SKL-05013, hard_prerequisite, [inferred], Prerequisite for Explain why a critical point need not be a relative extremum.
- BC-TOP-0102 -> BC-SKL-05008, hard_prerequisite, [inferred], Continuity on a closed interval, a Unit 1 skill not yet in data/skills.json; the topic id stands in for it.
- BC-TOP-0115 -> BC-SKL-05011, supporting, [inferred], Classifying points of non-differentiability, a Unit 2 idea not yet in data/skills.json; the topic id stands in for it.
- BC-SKL-06021 -> BC-SKL-05010, supporting, [inferred], The Fundamental Theorem of Calculus supplies the derivative when the function is an accumulation, which is how BC-QA-05007 presents it.

### Required mathematical knowledge

**Extreme Value Theorem.** Hypotheses: f is continuous on the closed interval [a,b]. Conclusion: f attains at least one minimum value and at least one maximum value on [a,b]. The wording of BC-EK-FUN-1C1 was clarified for Fall 2026 and the clarified text is the one quoted above (ced-clarifications-2026:1).

**Critical point.** c is a critical point of f when f'(c) equals zero or f'(c) fails to exist, with c in the domain of f (BC-EK-FUN-1C2).

**One-way containment.** Every local extremum occurs at a critical point, and a critical point need not be a local extremum (BC-EK-FUN-1C3). A derivative that is zero without a sign change is the standard counterexample and was scored directly in 2023 (sg-23:13).

**Local against global.** A local extremum compares the value only with nearby values; an absolute extremum compares it with every value on the interval under discussion.

**Notation.** f'(c) = 0; f'(c) does not exist; relative (local) maximum; absolute (global) minimum; closed interval [a,b].

### Representations

Representations in play: BC-REP-01 Symbolic (analytical) expression, BC-REP-02 Graphical, BC-REP-04 Verbal description.

Conversions tested: symbolic derivative to a list of critical points (BC-REP-01 to BC-REP-04), and graph of f' to the critical points of f (BC-REP-02 to BC-REP-04).

### Assessment behaviour

MCQ forms ask how many critical points a given function has, or which of several functions fails the hypothesis of the Extreme Value Theorem on a stated interval. FRQ forms use the critical point list as the first scored step of a longer extremum argument, where considering the derivative equal to zero is its own point and merely listing zeros is not enough (sg-23:15, sg-25:19). Calculator variants solve the derivative equation numerically; no-calculator variants use factorable derivatives or graphs. Conceptual variants ask whether a critical point must be an extremum; computational variants ask for the critical points; justification variants require the statement that the derivative is zero or undefined rather than a bare list of inputs (sg-23:15).

### Archetypes

- BC-QA-05010 Extreme Value Theorem existence claim on a closed interval
- BC-QA-05006 Absolute extremum by the candidates test with a global justification
- BC-QA-05007 Critical point located and classified for a function given indirectly

### Errors and misconceptions

- BC-ERR-05007 Extreme Value Theorem invoked without continuity on the closed interval
- BC-ERR-99008 Chief Reader error record, see data/errors.json
- BC-ERR-05008 Existence theorem used to locate the extremum
- BC-ERR-05009 Zeros of the derivative listed without stating the derivative condition
- BC-ERR-05010 Solutions outside the domain retained as critical points
- BC-ERR-05011 Inputs where the derivative fails to exist omitted from the critical points
- BC-ERR-05012 Relative extremum reported as the absolute extremum
- BC-ERR-99004 Chief Reader error record, see data/errors.json
- BC-ERR-05013 Critical point with no sign change declared an extremum
- BC-MIS-05006 Continuity may be assumed on any interval, severity medium
- BC-MIS-05007 A relative extremum is an absolute extremum, severity high
- BC-MIS-05008 Every critical point is an extremum, severity high
- BC-MIS-05009 The derivative exists wherever the function does, severity medium

### Diagnostic signals

- BC-SIG-05005 Continuity asserted with no support
- BC-SIG-05006 Existence question answered with a located extremum
- BC-SIG-05007 Zeros listed with no derivative equation presented
- BC-SIG-05008 Critical point list missing the non-differentiable input
- BC-SIG-05009 Local claim offered for a global question
- BC-SIG-05010 Extremum declared where the derivative touches zero

### Adaptive metadata summary

Skills in this topic carry calculator relevance none, optional. Remediation targets named across the topic: BC-PRQ-05001, BC-PRQ-05004, BC-PRQ-05006, BC-SKL-05007, BC-SKL-05008, BC-SKL-05010. Every skill record carries the full seven key adaptive block in data/staging/unit-05.skills.json. [inferred]

## 5.3 Determining Intervals on Which a Function is Increasing or Decreasing

### Official mapping

Topic id BC-TOP-0503, CED code 5.3, name Determining Intervals on Which a Function is Increasing or Decreasing, scope shared, CED page 101. [verified] (ced:101)

- BC-LO-FUN-4A (FUN-4.A): Justify conclusions about the behavior of a function based on the behavior of its derivatives.
  - BC-EK-FUN-4A1 (FUN-4.A.1): "The first derivative of a function can provide information about the function and its graph, including intervals where the function is increasing or decreasing."

Suggested practice skills: BC-MPS-2E (Practice skill 2.E). Weighting pointer: [../exam/exam-blueprint.md](../exam/exam-blueprint.md).

### Concept breakdown

- BC-CON-05004 Monotonicity read from the sign of the first derivative: Where the derivative is positive the function rises, and where it is negative the function falls.

- BC-SKL-05014 Determine where the first derivative is positive or negative from a formula: Work out the sign of the derivative expression on each interval.
- BC-SKL-05015 Read intervals of increase and decrease from the graph of the derivative: Use where the derivative graph is above or below the axis.
- BC-SKL-05016 Build a sign chart on critical points and domain boundaries: Lay the critical points and gaps on a line and mark the sign in each gap.
- BC-SKL-05017 Justify increase or decrease from the sign of the named derivative: Write the reason in words, naming the function whose derivative has that sign.
- BC-SKL-05018 Restrict a monotonicity conclusion to the domain of the function: Do not claim behaviour across a gap in the domain.

### Prerequisites

- BC-PRQ-05001 -> BC-SKL-05014, supporting, [inferred], Prerequisite for Determine where the first derivative is positive or negative from a formula.
- BC-PRQ-05002 -> BC-SKL-05014, supporting, [inferred], Prerequisite for Determine where the first derivative is positive or negative from a formula.
- BC-PRQ-05006 -> BC-SKL-05015, supporting, [inferred], Prerequisite for Read intervals of increase and decrease from the graph of the derivative.
- BC-SKL-05014 -> BC-SKL-05016, hard_prerequisite, [inferred], Prerequisite for Build a sign chart on critical points and domain boundaries.
- BC-PRQ-05003 -> BC-SKL-05016, supporting, [inferred], Prerequisite for Build a sign chart on critical points and domain boundaries.
- BC-SKL-05016 -> BC-SKL-05017, hard_prerequisite, [inferred], Prerequisite for Justify increase or decrease from the sign of the named derivative.
- BC-PRQ-05003 -> BC-SKL-05018, supporting, [inferred], Prerequisite for Restrict a monotonicity conclusion to the domain of the function.
- BC-SKL-05016 -> BC-SKL-05018, hard_prerequisite, [inferred], Prerequisite for Restrict a monotonicity conclusion to the domain of the function.
- BC-TOP-0205 -> BC-SKL-05014, hard_prerequisite, [inferred], Differentiating with the power rule, a Unit 2 skill not yet in data/skills.json; the topic id stands in for it.

### Required mathematical knowledge

**Monotonicity test.** Hypotheses: f is differentiable on an open interval contained in its domain. Conclusion: f' positive throughout the interval gives f increasing there, and f' negative throughout gives f decreasing there (BC-EK-FUN-4A1).

**Partition points.** The candidates that split the number line are the zeros of f' and the inputs where f' or f is undefined.

**Justification standard.** The 2025 guideline made the reason point depend on tying the reason to the given representation, and refused a reason that restated the conclusion in other symbols or that used an unnamed referent such as the function or the graph (sg-25:17).

**Notation.** f'(x) > 0 on (a,b); increasing on (a,b); open intervals are the conventional form of the answer.

### Representations

Representations in play: BC-REP-01 Symbolic (analytical) expression, BC-REP-02 Graphical, BC-REP-03 Numerical table.

Conversions tested: symbolic derivative to a sign chart and then to intervals (BC-REP-01 to BC-REP-04), and graph of f' to intervals of increase of f (BC-REP-02 to BC-REP-04).

### Assessment behaviour

MCQ forms give a derivative formula or a graph of the derivative and ask for the intervals on which the function rises. FRQ forms ask for the intervals with a reason and score the intervals and the reason as separate points, with the reason point available only when the intervals are right (sg-23:14). Calculator variants allow a numerical solve of the derivative equation; no-calculator variants use factorable derivatives or a graph of the derivative made of segments and circular arcs (sg-23:13). Conceptual variants ask which graph could be the derivative of a function described as increasing; computational variants ask for the intervals; justification variants require the sign of the derivative to be named for the specific function on the specific interval; multi-concept variants pair the monotonicity claim with a concavity claim in the same question.

### Archetypes

- BC-QA-05008 Intervals of increase or decrease justified by the sign of the derivative

### Errors and misconceptions

- BC-ERR-05014 Sign of the derivative misread on an interval
- BC-ERR-05015 Plotted derivative read as the function itself
- BC-ERR-05016 Increase of the derivative confused with positivity of the derivative
- BC-ERR-05017 Sign chart omits a point where the function is undefined
- BC-ERR-05018 Justification uses an unnamed referent
- BC-ERR-99001 Chief Reader error record, see data/errors.json
- BC-ERR-05019 Interval of increase reported across a gap in the domain
- BC-MIS-05010 The sign of the derivative follows the sign of the function, severity high
- BC-MIS-05011 The plotted curve is the function under discussion, severity high
- BC-MIS-05012 A gap in the domain does not interrupt an interval of behaviour, severity medium
- BC-MIS-05013 Restating the conclusion counts as a reason, severity high

### Diagnostic signals

- BC-SIG-05011 Sign chart correct except on one interval
- BC-SIG-05012 Answer describes the plotted curve rather than the function
- BC-SIG-05013 Partition points taken from the function rather than the derivative
- BC-SIG-05014 Correct intervals with an unnamed referent in the reason
- BC-SIG-05015 Interval reported across an input where the function is undefined

### Adaptive metadata summary

Skills in this topic carry calculator relevance none. Remediation targets named across the topic: BC-PRQ-05001, BC-PRQ-05003, BC-PRQ-05006, BC-SKL-05016. Every skill record carries the full seven key adaptive block in data/staging/unit-05.skills.json. [inferred]

## 5.4 Using the First Derivative Test to Determine Relative (Local) Extrema

### Official mapping

Topic id BC-TOP-0504, CED code 5.4, name Using the First Derivative Test to Determine Relative (Local) Extrema, scope shared, CED page 102. [verified] (ced:102)

- BC-LO-FUN-4A (FUN-4.A): Justify conclusions about the behavior of a function based on the behavior of its derivatives.
  - BC-EK-FUN-4A2 (FUN-4.A.2): "The first derivative of a function can determine the location of relative (local) extrema of the function."

Suggested practice skills: BC-MPS-3D (Practice skill 3.D). Weighting pointer: [../exam/exam-blueprint.md](../exam/exam-blueprint.md).

### Concept breakdown

- BC-CON-05005 First derivative test for relative extrema: A critical point is a relative maximum or minimum according to how the sign of the derivative changes there.

- BC-SKL-05019 Assemble the candidate relative extrema at the critical points: List the critical points as the only places a relative extremum can sit.
- BC-SKL-05020 Classify a critical point from the sign change of the first derivative: Decide maximum or minimum from how the derivative sign flips there.
- BC-SKL-05021 Conclude neither extremum when the derivative keeps its sign: Say neither when the derivative does not flip sign at the point.
- BC-SKL-05022 Write a first derivative test justification with an explicit referent: Write the reason naming which derivative changes sign and where.
- BC-SKL-05023 Separate the location of a relative extremum from its value: Answer with the input or the output, whichever was asked for.

### Prerequisites

- BC-SKL-05010 -> BC-SKL-05019, hard_prerequisite, [inferred], Prerequisite for Assemble the candidate relative extrema at the critical points.
- BC-SKL-05011 -> BC-SKL-05019, hard_prerequisite, [inferred], Prerequisite for Assemble the candidate relative extrema at the critical points.
- BC-SKL-05016 -> BC-SKL-05020, hard_prerequisite, [inferred], Prerequisite for Classify a critical point from the sign change of the first derivative.
- BC-SKL-05019 -> BC-SKL-05020, hard_prerequisite, [inferred], Prerequisite for Classify a critical point from the sign change of the first derivative.
- BC-SKL-05020 -> BC-SKL-05021, hard_prerequisite, [inferred], Prerequisite for Conclude neither extremum when the derivative keeps its sign.
- BC-SKL-05020 -> BC-SKL-05022, hard_prerequisite, [inferred], Prerequisite for Write a first derivative test justification with an explicit referent.
- BC-SKL-05020 -> BC-SKL-05023, hard_prerequisite, [inferred], Prerequisite for Separate the location of a relative extremum from its value.
- BC-SKL-06023 -> BC-SKL-05020, supporting, [inferred], The Unit 6 record for applying the first derivative test to an accumulation function depends on this skill and is recorded there.

### Required mathematical knowledge

**First derivative test.** Hypotheses: f is continuous at c and c is a critical point of f. Conclusion: f' changing from positive to negative at c gives a relative maximum, from negative to positive gives a relative minimum, and no sign change gives neither (BC-EK-FUN-4A2).

**Sign change is the whole content.** The 2023 guideline accepted a bare declaration that the derivative does not change sign at the point as sufficient for the point, and rejected a response that only reported the derivative to be positive before and after the point, because that phrasing does not express the sign behaviour required (sg-23:13).

**Location against value.** The test locates an extremum; the extreme value is f(c) and takes a separate evaluation.

**Notation.** relative (local) maximum at x = c; f' changes from positive to negative; neither.

### Representations

Representations in play: BC-REP-01 Symbolic (analytical) expression, BC-REP-02 Graphical, BC-REP-03 Numerical table.

Conversions tested: graph of f' to a classified critical point of f (BC-REP-02 to BC-REP-04), and a sign chart to a classification statement (BC-REP-04 to BC-REP-04).

### Assessment behaviour

MCQ forms give a derivative and ask which inputs give relative maxima. FRQ forms ask whether a relative minimum, a relative maximum, or neither occurs at a named input and award a single point for the answer together with its reason, so an unsupported correct classification earns nothing (sg-23:13). Calculator status is either; the 2023 instance was no calculator with a piecewise derivative graph. Conceptual variants ask what the test cannot settle; computational variants ask for the classification; justification variants demand a sign change statement tied to the named derivative; multi-concept variants ask for the classification and then for the extreme value.

### Archetypes

- BC-QA-05003 Relative extremum classified from the behaviour of the first derivative

### Errors and misconceptions

- BC-ERR-05020 Candidate extrema sought away from the critical points
- BC-ERR-05021 Direction of the sign change reversed in the classification
- BC-ERR-05022 Classification taken from the value of the derivative rather than its change
- BC-ERR-05013 Critical point with no sign change declared an extremum
- BC-ERR-05023 Positive before and after offered in place of no sign change
- BC-ERR-05018 Justification uses an unnamed referent
- BC-ERR-99001 Chief Reader error record, see data/errors.json
- BC-ERR-05024 Location reported where the value was asked for
- BC-MIS-05008 Every critical point is an extremum, severity high
- BC-MIS-05014 The classification comes from the derivative value rather than its change, severity high
- BC-MIS-05013 Restating the conclusion counts as a reason, severity high
- BC-MIS-05015 The location of an extremum and its value are the same answer, severity medium

### Diagnostic signals

- BC-SIG-05016 Classification reversed with a correct sign statement
- BC-SIG-05017 Correct extremum with the wrong quantity reported

### Adaptive metadata summary

Skills in this topic carry calculator relevance none. Remediation targets named across the topic: BC-SKL-05010, BC-SKL-05016, BC-SKL-05020. Every skill record carries the full seven key adaptive block in data/staging/unit-05.skills.json. [inferred]

## 5.5 Using the Candidates Test to Determine Absolute (Global) Extrema

### Official mapping

Topic id BC-TOP-0505, CED code 5.5, name Using the Candidates Test to Determine Absolute (Global) Extrema, scope shared, CED page 103. [verified] (ced:103)

- BC-LO-FUN-4A (FUN-4.A): Justify conclusions about the behavior of a function based on the behavior of its derivatives.
  - BC-EK-FUN-4A3 (FUN-4.A.3): "Absolute (global) extrema of a function on a closed interval can only occur at critical points or at endpoints."

Suggested practice skills: BC-MPS-1E (Practice skill 1.E). Weighting pointer: [../exam/exam-blueprint.md](../exam/exam-blueprint.md).

### Concept breakdown

- BC-CON-05006 Candidates test for absolute extrema on a closed interval: The largest and smallest values of a continuous function on a closed interval are found by comparing its values at every critical point and at both endpoints.

- BC-SKL-05024 Assemble the candidate list from critical points and both endpoints: Write down every critical point in the interval plus the two endpoints.
- BC-SKL-05025 Evaluate the function at every candidate: Work out the function value at each candidate input.
- BC-SKL-05026 Compare the candidate values and name the absolute extremum: Pick the largest or smallest of the candidate values.
- BC-SKL-05027 Report the extreme value rather than only its location: Give the value asked for, not just where it happens.
- BC-SKL-05028 Write a global justification covering every candidate: Show the comparison over all candidates, endpoints included, and nothing else.
- BC-SKL-05029 Justify an absolute extremum from the sign of the derivative across the interval: Argue globally from the derivative keeping one sign on each side.

### Prerequisites

- BC-SKL-05010 -> BC-SKL-05024, hard_prerequisite, [inferred], Prerequisite for Assemble the candidate list from critical points and both endpoints.
- BC-SKL-05011 -> BC-SKL-05024, hard_prerequisite, [inferred], Prerequisite for Assemble the candidate list from critical points and both endpoints.
- BC-PRQ-05004 -> BC-SKL-05024, supporting, [inferred], Prerequisite for Assemble the candidate list from critical points and both endpoints.
- BC-SKL-05024 -> BC-SKL-05025, hard_prerequisite, [inferred], Prerequisite for Evaluate the function at every candidate.
- BC-PRQ-06005 -> BC-SKL-05025, supporting, [inferred], Prerequisite for Evaluate the function at every candidate.
- BC-SKL-05025 -> BC-SKL-05026, hard_prerequisite, [inferred], Prerequisite for Compare the candidate values and name the absolute extremum.
- BC-SKL-05026 -> BC-SKL-05027, hard_prerequisite, [inferred], Prerequisite for Report the extreme value rather than only its location.
- BC-SKL-05025 -> BC-SKL-05028, hard_prerequisite, [inferred], Prerequisite for Write a global justification covering every candidate.
- BC-SKL-05026 -> BC-SKL-05028, hard_prerequisite, [inferred], Prerequisite for Write a global justification covering every candidate.
- BC-SKL-05016 -> BC-SKL-05029, hard_prerequisite, [inferred], Prerequisite for Justify an absolute extremum from the sign of the derivative across the interval.
- BC-SKL-05024 -> BC-SKL-05029, hard_prerequisite, [inferred], Prerequisite for Justify an absolute extremum from the sign of the derivative across the interval.
- BC-SKL-06026 -> BC-SKL-05028, supporting, [inferred], The Unit 6 record for the candidates test on an accumulation function depends on this skill and is recorded there.

### Required mathematical knowledge

**Candidates test.** Hypotheses: f is continuous on the closed interval [a,b]. Conclusion: the absolute extrema of f on [a,b] occur among the critical points in (a,b) and the endpoints a and b, so comparing the values of f at all of these locates them (BC-EK-FUN-4A3).

**Global argument requirement.** The 2025 guideline required the justification to provide evaluations or reasoning for every candidate and for no other inputs, and refused the justification point to a response offering a first derivative test or a second derivative test in its place, because those are local arguments (sg-25:19). The 2023 guideline refused the justification point to a response that did not consider both endpoints (sg-23:15).

**Alternate global argument.** A response may instead argue from the sign of f' across the whole interval, for example that f' is not positive to the left of the candidate and not negative to its right (sg-25:19).

**Value against location.** The 2023 guideline awarded the answer point only for the extreme value itself and not for the input where it occurs (sg-23:15).

**Notation.** a two column table of candidate inputs against function values; absolute minimum value; on the closed interval.

### Representations

Representations in play: BC-REP-01 Symbolic (analytical) expression, BC-REP-02 Graphical, BC-REP-03 Numerical table.

Conversions tested: graph of f' plus one known value of f to a table of candidate values of f (BC-REP-02 to BC-REP-03), and a candidate table to a single extreme value (BC-REP-03 to BC-REP-04).

### Assessment behaviour

MCQ forms give a function and a closed interval and ask for the absolute maximum value. FRQ forms ask for an absolute extremum with a justification and split the scoring into considering the derivative equal to zero, the global justification, and the value (sg-23:15, sg-25:19). Calculator variants evaluate the candidates numerically; no-calculator variants build the candidate values from areas under a plotted derivative (sg-25:18, sg-25:19). Conceptual variants ask why endpoints belong on the list; computational variants ask for the value; justification variants demand every candidate and no extras; multi-concept variants build the candidate values through an accumulation function before the comparison.

### Archetypes

- BC-QA-05006 Absolute extremum by the candidates test with a global justification

### Errors and misconceptions

- BC-ERR-05025 Critical points outside the interval included as candidates
- BC-ERR-05026 One or both endpoints omitted from the candidate comparison
- BC-ERR-05027 Function evaluated incorrectly at a candidate
- BC-ERR-05028 Extremum selected in the wrong direction
- BC-ERR-05024 Location reported where the value was asked for
- BC-ERR-05029 Local argument offered where a global argument is required
- BC-ERR-99004 Chief Reader error record, see data/errors.json
- BC-MIS-05016 The candidates are the critical points only, severity high
- BC-MIS-05017 The last candidate computed is the extremum, severity medium
- BC-MIS-05015 The location of an extremum and its value are the same answer, severity medium
- BC-MIS-05018 A local test settles a global question, severity high

### Diagnostic signals

- BC-SIG-05018 Candidate list missing an endpoint
- BC-SIG-05019 Candidate table with one wrong entry
- BC-SIG-05020 Comparison made in the wrong direction
- BC-SIG-05021 Justification built from a local test

### Adaptive metadata summary

Skills in this topic carry calculator relevance none, optional. Remediation targets named across the topic: BC-PRQ-05004, BC-PRQ-06005, BC-SKL-05016, BC-SKL-05025, BC-SKL-05026. Every skill record carries the full seven key adaptive block in data/staging/unit-05.skills.json. [inferred]

## 5.6 Determining Concavity of Functions over Their Domains

### Official mapping

Topic id BC-TOP-0506, CED code 5.6, name Determining Concavity of Functions over Their Domains, scope shared, CED page 104. [verified] (ced:104)

- BC-LO-FUN-4A (FUN-4.A): Justify conclusions about the behavior of a function based on the behavior of its derivatives.
  - BC-EK-FUN-4A4 (FUN-4.A.4): "The graph of a function is concave up (down) on an open interval if the function's derivative is increasing (decreasing) on that interval."
  - BC-EK-FUN-4A5 (FUN-4.A.5): "The second derivative of a function provides information about the function and its graph, including intervals of upward or downward concavity."
  - BC-EK-FUN-4A6 (FUN-4.A.6): "The second derivative of a function may be used to locate points of inflection for the graph of the original function."

Suggested practice skills: BC-MPS-2E (Practice skill 2.E). Weighting pointer: [../exam/exam-blueprint.md](../exam/exam-blueprint.md).

### Concept breakdown

- BC-CON-05007 Concavity as the monotonicity of the first derivative: A graph bends upward where the derivative is increasing and downward where the derivative is decreasing.
- BC-CON-05008 Point of inflection as a change of concavity: A point of inflection is where the bending direction actually changes, not merely where the second derivative is zero.

- BC-SKL-05030 Determine intervals of concavity from the sign of the second derivative: Use where the second derivative is positive or negative.
- BC-SKL-05031 Determine concavity from whether the derivative graph rises or falls: Read concavity off the slope behaviour of the derivative graph.
- BC-SKL-05032 Locate candidate points of inflection where the second derivative is zero or undefined: Find the inputs where the second derivative is zero or does not exist.
- BC-SKL-05033 Confirm a point of inflection by a sign change of the second derivative: Check the bending really changes direction there.
- BC-SKL-05034 Reject a candidate where the second derivative is zero without a sign change: Throw out a candidate where the bending does not change.
- BC-SKL-05035 Tie a concavity or inflection reason to the representation that was given: Write the reason in terms of the object the question actually supplied.

### Prerequisites

- BC-PRQ-05001 -> BC-SKL-05030, supporting, [inferred], Prerequisite for Determine intervals of concavity from the sign of the second derivative.
- BC-PRQ-05002 -> BC-SKL-05030, supporting, [inferred], Prerequisite for Determine intervals of concavity from the sign of the second derivative.
- BC-PRQ-05006 -> BC-SKL-05031, supporting, [inferred], Prerequisite for Determine concavity from whether the derivative graph rises or falls.
- BC-PRQ-05001 -> BC-SKL-05032, supporting, [inferred], Prerequisite for Locate candidate points of inflection where the second derivative is zero or undefined.
- BC-PRQ-05003 -> BC-SKL-05032, supporting, [inferred], Prerequisite for Locate candidate points of inflection where the second derivative is zero or undefined.
- BC-SKL-05032 -> BC-SKL-05033, hard_prerequisite, [inferred], Prerequisite for Confirm a point of inflection by a sign change of the second derivative.
- BC-SKL-05031 -> BC-SKL-05033, hard_prerequisite, [inferred], Prerequisite for Confirm a point of inflection by a sign change of the second derivative.
- BC-SKL-05033 -> BC-SKL-05034, hard_prerequisite, [inferred], Prerequisite for Reject a candidate where the second derivative is zero without a sign change.
- BC-SKL-05033 -> BC-SKL-05035, hard_prerequisite, [inferred], Prerequisite for Tie a concavity or inflection reason to the representation that was given.
- BC-TOP-0205 -> BC-SKL-05030, hard_prerequisite, [inferred], Producing a second derivative, a Unit 2 skill not yet in data/skills.json; the topic id stands in for it.
- BC-SKL-06025 -> BC-SKL-05033, supporting, [inferred], The Unit 6 record for concavity of an accumulation function depends on this skill and is recorded there.

### Required mathematical knowledge

**Concavity.** Hypotheses: f' exists on an open interval. Conclusion: the graph of f is concave up where f' is increasing, equivalently where f'' is positive, and concave down where f' is decreasing, equivalently where f'' is negative (BC-EK-FUN-4A4, BC-EK-FUN-4A5).

**Point of inflection.** Hypotheses: c lies in the domain of f. Conclusion: the graph of f has a point of inflection at c when f'' changes sign at c (BC-EK-FUN-4A6). A zero of f'' with no sign change is not a point of inflection.

**Justification standard.** The 2025 guideline gave the reason point only to a response that tied the reason to the given representation, so a reason phrased as the second derivative changing sign earned the answer but not the reason when the given object was a graph of the integrand (sg-25:17). The 2023 guideline required the reason to discuss the behaviour of the derivative or the slopes of the derivative, and it allowed partial credit for one of two correct intervals with a correct reason (sg-23:14).

**Notation.** concave down on the open interval (a,b); f'' < 0; point of inflection at x = c; answers are open intervals.

### Representations

Representations in play: BC-REP-01 Symbolic (analytical) expression, BC-REP-02 Graphical, BC-REP-03 Numerical table.

Conversions tested: graph of f' to intervals of concavity of f (BC-REP-02 to BC-REP-04), and symbolic f to the sign chart of f'' (BC-REP-01 to BC-REP-04).

### Assessment behaviour

MCQ forms ask for the number of points of inflection of a function given by a formula or by the graph of its derivative. FRQ forms ask for the intervals of concavity or for the points of inflection with a reason, scoring the intervals or list and the reason separately and making the reason conditional on the list being exactly right (sg-23:14, sg-25:17). Calculator status is either. Conceptual variants ask whether a zero of the second derivative must be a point of inflection; computational variants ask for the list; justification variants require the reason to be phrased in terms of the object the question supplied; multi-concept variants combine concavity with an over or under estimate claim about a tangent line approximation (sg-23:11).

### Archetypes

- BC-QA-05004 Intervals of concavity from derivative information with a reason
- BC-QA-05005 Points of inflection identified with a reason tied to the given graph

### Errors and misconceptions

- BC-ERR-05030 Sign of the second derivative misread
- BC-ERR-05031 Concavity read from the sign of the plotted derivative
- BC-ERR-05016 Increase of the derivative confused with positivity of the derivative
- BC-ERR-05032 Second derivative zeros taken outside the domain of the function
- BC-ERR-05033 Point of inflection declared with no sign change checked
- BC-ERR-99023 Chief Reader error record, see data/errors.json
- BC-ERR-05034 Touching zero retained as a point of inflection
- BC-ERR-05035 Inflection reason restated in second derivative symbols
- BC-ERR-99001 Chief Reader error record, see data/errors.json
- BC-MIS-05019 The second derivative behaves like the first, severity medium
- BC-MIS-05011 The plotted curve is the function under discussion, severity high
- BC-MIS-05020 Concavity and monotonicity are the same property, severity high
- BC-MIS-05021 A zero of the second derivative is a point of inflection, severity high
- BC-MIS-05013 Restating the conclusion counts as a reason, severity high
- BC-MIS-05022 A reason is complete once symbols appear, severity medium

### Diagnostic signals

- BC-SIG-05022 Concavity intervals correct with the wrong sign reported once
- BC-SIG-05023 Concavity reported where the derivative is positive
- BC-SIG-05024 Candidate inflection list includes an input outside the domain
- BC-SIG-05025 Every zero of the second derivative declared an inflection point
- BC-SIG-05026 One extra input in an otherwise correct inflection list
- BC-SIG-05027 Correct list with the reason phrased in second derivative symbols

### Adaptive metadata summary

Skills in this topic carry calculator relevance none. Remediation targets named across the topic: BC-PRQ-05001, BC-PRQ-05006, BC-SKL-05032, BC-SKL-05033. Every skill record carries the full seven key adaptive block in data/staging/unit-05.skills.json. [inferred]

## 5.7 Using the Second Derivative Test to Determine Extrema

### Official mapping

Topic id BC-TOP-0507, CED code 5.7, name Using the Second Derivative Test to Determine Extrema, scope shared, CED page 105. [verified] (ced:105)

- BC-LO-FUN-4A (FUN-4.A): Justify conclusions about the behavior of a function based on the behavior of its derivatives.
  - BC-EK-FUN-4A7 (FUN-4.A.7): "The second derivative of a function may determine whether a critical point is the location of a relative (local) maximum or minimum."
  - BC-EK-FUN-4A8 (FUN-4.A.8): "When a continuous function has only one critical point on an interval on its domain and the critical point corresponds to a relative (local) extremum of the function on the interval, then that critical point also corresponds to the absolute (global) extremum of the function on the interval."

Suggested practice skills: BC-MPS-3D (Practice skill 3.D). Weighting pointer: [../exam/exam-blueprint.md](../exam/exam-blueprint.md).

### Concept breakdown

- BC-CON-05009 Second derivative test at a critical point: At a critical point where the derivative is zero, the bending direction settles whether the point is a high point or a low point.
- BC-CON-05010 A sole relative extremum as an absolute extremum: If a continuous function has only one critical point on an interval and it is a relative extremum, it is also the extreme value on the whole interval.

- BC-SKL-05036 Apply the second derivative test at a critical point: Use the sign of the second derivative at the point to classify it.
- BC-SKL-05037 State the inconclusive case of the second derivative test: Say that a zero second derivative settles nothing and switch tests.
- BC-SKL-05038 Extend a sole relative extremum to an absolute extremum on the interval: When there is only one critical point, a relative extremum there is the extreme value overall.
- BC-SKL-05039 Choose between the first and second derivative tests for a given presentation: Pick the test the given information actually supports.

### Prerequisites

- BC-SKL-05010 -> BC-SKL-05036, hard_prerequisite, [inferred], Prerequisite for Apply the second derivative test at a critical point.
- BC-SKL-05030 -> BC-SKL-05036, hard_prerequisite, [inferred], Prerequisite for Apply the second derivative test at a critical point.
- BC-SKL-05036 -> BC-SKL-05037, hard_prerequisite, [inferred], Prerequisite for State the inconclusive case of the second derivative test.
- BC-SKL-05036 -> BC-SKL-05038, hard_prerequisite, [inferred], Prerequisite for Extend a sole relative extremum to an absolute extremum on the interval.
- BC-SKL-05020 -> BC-SKL-05038, hard_prerequisite, [inferred], Prerequisite for Extend a sole relative extremum to an absolute extremum on the interval.
- BC-SKL-05020 -> BC-SKL-05039, hard_prerequisite, [inferred], Prerequisite for Choose between the first and second derivative tests for a given presentation.
- BC-SKL-05036 -> BC-SKL-05039, hard_prerequisite, [inferred], Prerequisite for Choose between the first and second derivative tests for a given presentation.

### Required mathematical knowledge

**Second derivative test.** Hypotheses: f'(c) equals zero and f'' exists near c. Conclusion: f''(c) negative gives a relative maximum at c, f''(c) positive gives a relative minimum at c, and f''(c) equal to zero leaves the test inconclusive (BC-EK-FUN-4A7).

**Sole critical point extension.** Hypotheses: f is continuous on an interval and has exactly one critical point there, which is a relative extremum. Conclusion: that point is the absolute extremum on the interval (BC-EK-FUN-4A8). This is the standard closing step of an applied optimisation argument.

**Local scope.** The 2025 guideline treated a second derivative test as a local argument and refused it the justification point where a global argument was demanded (sg-25:19). The 2024 guideline accepted a second derivative evaluation as an alternate route for classifying a critical point of a solution of a differential equation (sg-24:10).

**Notation.** f''(c) < 0; inconclusive; sole critical point on the interval.

### Representations

Representations in play: BC-REP-01 Symbolic (analytical) expression, BC-REP-03 Numerical table, BC-REP-06 Differential equation.

Conversions tested: symbolic critical point to a second derivative value and a classification (BC-REP-01 to BC-REP-04), and a differential equation to a second derivative expression evaluated at a point (BC-REP-06 to BC-REP-01).

### Assessment behaviour

MCQ forms supply a function and a critical point and ask for the classification. FRQ forms offer the test as an alternate solution to a classification part and score it the same as a first derivative argument (sg-24:10), while refusing it where a global claim was asked for (sg-25:19). Calculator status is either. Conceptual variants ask what happens when the second derivative is zero at the critical point; computational variants ask for the classification; justification variants require the critical point condition and the sign of the second derivative both to be stated; multi-concept variants use the sole critical point rule to close an optimisation argument.

### Archetypes

- BC-QA-05013 Second derivative test applied at a critical point

### Errors and misconceptions

- BC-ERR-05036 Second derivative test applied where the first derivative is not zero
- BC-ERR-05037 Sign convention of the second derivative test reversed
- BC-ERR-05038 Inconclusive case treated as a conclusion
- BC-ERR-05039 Sole critical point claim made without stating uniqueness
- BC-ERR-99004 Chief Reader error record, see data/errors.json
- BC-ERR-05040 Derivative test chosen that the given information cannot support
- BC-MIS-05023 The second derivative test always decides, severity medium
- BC-MIS-05024 The two derivative tests are interchangeable in every setting, severity medium
- BC-MIS-05018 A local test settles a global question, severity high

### Diagnostic signals

- BC-SIG-05028 Second derivative evaluated correctly with the classification reversed
- BC-SIG-05029 Zero second derivative read as a verdict
- BC-SIG-05030 Global claim made with no uniqueness statement
- BC-SIG-05031 Test chosen that the given object cannot supply

### Adaptive metadata summary

Skills in this topic carry calculator relevance none. Remediation targets named across the topic: BC-SKL-05010, BC-SKL-05020, BC-SKL-05036. Every skill record carries the full seven key adaptive block in data/staging/unit-05.skills.json. [inferred]

## 5.8 Sketching Graphs of Functions and Their Derivatives

### Official mapping

Topic id BC-TOP-0508, CED code 5.8, name Sketching Graphs of Functions and Their Derivatives, scope shared, CED page 106. [verified] (ced:106)

- BC-LO-FUN-4A (FUN-4.A): Justify conclusions about the behavior of a function based on the behavior of its derivatives.
  - BC-EK-FUN-4A9 (FUN-4.A.9): "Key features of functions and their derivatives can be identified and related to their graphical, numerical, and analytical representations."
  - BC-EK-FUN-4A10 (FUN-4.A.10): "Graphical, numerical, and analytical information from f' and f'' can be used to predict and explain the behavior of f."

Suggested practice skills: BC-MPS-2D (Practice skill 2.D). Weighting pointer: [../exam/exam-blueprint.md](../exam/exam-blueprint.md).

### Concept breakdown

- BC-CON-05011 Graph of a function reconstructed from its derivative graphs: The shape of a curve can be drawn from where its derivative is positive, negative, or turning, and the derivative can be drawn from the curve.

- BC-SKL-05040 Sketch the graph of the derivative from the graph of a function: Turn the slopes of a curve into a new plotted curve.
- BC-SKL-05041 Sketch a possible graph of a function from the graph of its derivative: Turn a derivative plot back into a curve with the right rises, falls, and bends.
- BC-SKL-05042 Match a named feature of a function with the corresponding feature of its derivative: Say which feature of one graph corresponds to a feature of the other.
- BC-SKL-05043 Place extrema and points of inflection consistently on a sketch: Put the turning points and bending changes where the derivative information puts them.
- BC-SKL-05044 Recognise the vertical shift ambiguity when a curve is drawn from its derivative: Note that one known value is needed to pin the curve down.

### Prerequisites

- BC-PRQ-05006 -> BC-SKL-05040, supporting, [inferred], Prerequisite for Sketch the graph of the derivative from the graph of a function.
- BC-SKL-05015 -> BC-SKL-05041, hard_prerequisite, [inferred], Prerequisite for Sketch a possible graph of a function from the graph of its derivative.
- BC-SKL-05031 -> BC-SKL-05041, hard_prerequisite, [inferred], Prerequisite for Sketch a possible graph of a function from the graph of its derivative.
- BC-SKL-05015 -> BC-SKL-05042, hard_prerequisite, [inferred], Prerequisite for Match a named feature of a function with the corresponding feature of its derivative.
- BC-SKL-05031 -> BC-SKL-05042, hard_prerequisite, [inferred], Prerequisite for Match a named feature of a function with the corresponding feature of its derivative.
- BC-SKL-05041 -> BC-SKL-05043, hard_prerequisite, [inferred], Prerequisite for Place extrema and points of inflection consistently on a sketch.
- BC-SKL-05033 -> BC-SKL-05043, hard_prerequisite, [inferred], Prerequisite for Place extrema and points of inflection consistently on a sketch.
- BC-SKL-05041 -> BC-SKL-05044, hard_prerequisite, [inferred], Prerequisite for Recognise the vertical shift ambiguity when a curve is drawn from its derivative.

### Required mathematical knowledge

**Feature correspondence.** A zero of f' with a sign change marks an extremum of f; an extremum of f' marks a point of inflection of f; f' positive marks f rising; f' increasing marks f concave up (BC-EK-FUN-4A9, BC-EK-FUN-4A10).

**Vertical indeterminacy.** A sketch of f built from f' alone is settled only up to an additive constant, so one value of f fixes the curve. The 2023 question supplied f(2) for exactly this reason (frq-23:8).

**Corner and cusp.** A corner on the graph of f shows as a jump in the graph of f'; a vertical tangent on f shows as an unbounded f'.

**Notation.** graph of f'; the derivative of f; sketch a possible graph of f.

### Representations

Representations in play: BC-REP-01 Symbolic (analytical) expression, BC-REP-02 Graphical, BC-REP-03 Numerical table.

Conversions tested: graph of f to graph of f' (BC-REP-02 to BC-REP-02), graph of f' to a possible graph of f (BC-REP-02 to BC-REP-02), and symbolic f with a table of signs to a sketch (BC-REP-01 to BC-REP-02).

### Assessment behaviour

MCQ forms present a graph and ask which of four graphs could be its derivative. FRQ forms rarely ask for the sketch itself and instead ask for the features the sketch encodes, such as extrema, concavity, and points of inflection (sg-23:13, sg-23:14, sg-25:17). Calculator status is no calculator, since the object is a sketch. Conceptual variants ask what feature of f corresponds to a named feature of f'; computational variants ask for the inputs where a feature occurs; justification variants require the correspondence to be named; multi-concept variants supply one value of f so that the sketch is fully determined.

### Archetypes

- BC-QA-05009 Relating the graphs of a function and its first two derivatives

### Errors and misconceptions

- BC-ERR-05041 Derivative sketch drawn with turning points at the zeros of the function
- BC-ERR-05042 Curve sketched with turning points at the zeros of the wrong object
- BC-ERR-05016 Increase of the derivative confused with positivity of the derivative
- BC-ERR-05043 Feature of the function matched with the wrong derivative
- BC-ERR-05044 Point of inflection drawn at a turning point of the sketch
- BC-ERR-05045 Sketch treated as unique with no reference to the constant
- BC-MIS-05011 The plotted curve is the function under discussion, severity high
- BC-MIS-05020 Concavity and monotonicity are the same property, severity high
- BC-MIS-05025 A derivative determines its function uniquely, severity medium

### Diagnostic signals

- BC-SIG-05032 Derivative sketch with extrema at the zeros of the function
- BC-SIG-05033 Sketch with extrema and inflection points interchanged
- BC-SIG-05034 Feature matched one derivative away
- BC-SIG-05035 Sketch presented as the only possible curve

### Adaptive metadata summary

Skills in this topic carry calculator relevance none. Remediation targets named across the topic: BC-PRQ-05006, BC-SKL-05015, BC-SKL-05041. Every skill record carries the full seven key adaptive block in data/staging/unit-05.skills.json. [inferred]

## 5.9 Connecting a Function, Its First Derivative, and Its Second Derivative

### Official mapping

Topic id BC-TOP-0509, CED code 5.9, name Connecting a Function, Its First Derivative, and Its Second Derivative, scope shared, CED page 107. [verified] (ced:107)

- BC-LO-FUN-4A (FUN-4.A): Justify conclusions about the behavior of a function based on the behavior of its derivatives.
  - BC-EK-FUN-4A11 (FUN-4.A.11): "Key features of the graphs of f, f', and f'' are related to one another."

Suggested practice skills: BC-MPS-2D (Practice skill 2.D). Weighting pointer: [../exam/exam-blueprint.md](../exam/exam-blueprint.md).

### Concept breakdown

- BC-CON-05012 Simultaneous reading of a function and its first two derivatives: A single scenario may present any of f, f prime, and f double prime as a graph, a table, or a formula, and every feature of one constrains the others.

- BC-SKL-05045 Identify which of several graphs is the function, the derivative, and the second derivative: Sort three unlabelled curves into the right roles.
- BC-SKL-05046 Translate a statement about the second derivative into a statement about shape: Turn a claim about the second derivative into a claim about bending.
- BC-SKL-05047 Build a combined sign table for the first and second derivatives: Record both derivative signs interval by interval.
- BC-SKL-05048 Answer a question about a function from tabulated derivative values: Use a table of derivative values to say what the function does.

### Prerequisites

- BC-SKL-05042 -> BC-SKL-05045, hard_prerequisite, [inferred], Prerequisite for Identify which of several graphs is the function, the derivative, and the second derivative.
- BC-SKL-05031 -> BC-SKL-05046, hard_prerequisite, [inferred], Prerequisite for Translate a statement about the second derivative into a statement about shape.
- BC-SKL-05016 -> BC-SKL-05047, hard_prerequisite, [inferred], Prerequisite for Build a combined sign table for the first and second derivatives.
- BC-SKL-05030 -> BC-SKL-05047, hard_prerequisite, [inferred], Prerequisite for Build a combined sign table for the first and second derivatives.
- BC-SKL-05047 -> BC-SKL-05048, hard_prerequisite, [inferred], Prerequisite for Answer a question about a function from tabulated derivative values.
- BC-PRQ-06005 -> BC-SKL-05048, supporting, [inferred], Prerequisite for Answer a question about a function from tabulated derivative values.
- BC-TOP-0406 -> BC-SKL-05046, supporting, [inferred], Reading a tangent line approximation against concavity, a Unit 4 idea not yet in data/skills.json; the topic id stands in for it.

### Required mathematical knowledge

**Three way correspondence.** Extrema of f sit at sign changes of f'; points of inflection of f sit at sign changes of f'', which are the extrema of f'; concavity of f matches the sign of f'' and the monotonicity of f' (BC-EK-FUN-4A11).

**Identification rule.** Among three plotted curves, the one whose zeros with sign change align with the turning points of another identifies the derivative relationship, and the ordering follows by applying the rule twice.

**Reading a table.** A table listing the sign of f' and the sign of f'' on successive intervals determines the shape of f piece by piece, up to a vertical shift.

**Notation.** f, f', f''; a sign table with rows for f' and f''; the phrase the graph of f is concave up and increasing.

### Representations

Representations in play: BC-REP-01 Symbolic (analytical) expression, BC-REP-02 Graphical, BC-REP-03 Numerical table.

Conversions tested: three unlabelled graphs to an assignment of f, f', f'' (BC-REP-02 to BC-REP-04), and a sign table to a description of shape (BC-REP-03 to BC-REP-04).

### Assessment behaviour

MCQ forms give three curves and ask which is which, or give a sign table and ask which description fits. FRQ forms present one of the three objects and ask for features of another, with the scoring notes penalising any confusion of which object is plotted (sg-25:16, sg-25:17). Calculator status is either. Conceptual variants ask which pair of features must coincide; computational variants ask for inputs; justification variants require the relationship, not just the answer; multi-concept variants combine the identification with a question about an accumulation function of the plotted curve.

### Archetypes

- BC-QA-05009 Relating the graphs of a function and its first two derivatives

### Errors and misconceptions

- BC-ERR-05046 Three graphs ordered in the reverse derivative direction
- BC-ERR-05047 Concavity read from the wrong direction of the second derivative
- BC-ERR-05048 Sign table built on the zeros of the function
- BC-ERR-05049 Finite table read as settling behaviour between the listed inputs
- BC-MIS-05011 The plotted curve is the function under discussion, severity high
- BC-MIS-05020 Concavity and monotonicity are the same property, severity high
- BC-MIS-05012 A gap in the domain does not interrupt an interval of behaviour, severity medium
- BC-MIS-05026 A table of values settles behaviour between the listed inputs, severity medium

### Diagnostic signals

- BC-SIG-05036 Three graphs labelled in the reverse order
- BC-SIG-05037 Second derivative statement translated into the wrong shape claim
- BC-SIG-05038 Combined sign table with one row correct
- BC-SIG-05039 Behaviour claimed between tabulated inputs

### Adaptive metadata summary

Skills in this topic carry calculator relevance none. Remediation targets named across the topic: BC-PRQ-06005, BC-SKL-05016, BC-SKL-05031, BC-SKL-05042. Every skill record carries the full seven key adaptive block in data/staging/unit-05.skills.json. [inferred]

## 5.10 Introduction to Optimization Problems

### Official mapping

Topic id BC-TOP-0510, CED code 5.10, name Introduction to Optimization Problems, scope shared, CED page 108. [verified] (ced:108)

- BC-LO-FUN-4B (FUN-4.B): Calculate minimum and maximum values in applied contexts or analysis of functions.
  - BC-EK-FUN-4B1 (FUN-4.B.1): "The derivative can be used to solve optimization problems; that is, finding a minimum or maximum value of a function on a given interval."

Suggested practice skills: BC-MPS-2A (Practice skill 2.A). Weighting pointer: [../exam/exam-blueprint.md](../exam/exam-blueprint.md).

### Concept breakdown

- BC-CON-05013 Optimisation model with an objective and a constraint: An applied maximum or minimum question becomes a calculus question once one quantity is written as a function of one variable on a stated domain.

- BC-SKL-05049 Name the quantity to be optimised and assign the variables: Say what is being made largest or smallest and label the unknowns.
- BC-SKL-05050 Use the constraint to write the objective as a function of one variable: Substitute the constraint so only one unknown is left.
- BC-SKL-05051 Determine the domain of the objective from the context: Work out which inputs the situation actually allows.
- BC-SKL-05052 Differentiate the objective and solve for critical points: Take the derivative of the objective and find where it is zero or undefined.
- BC-SKL-05053 Verify that the critical point gives the required extremum on the domain: Show the critical point really is the maximum or minimum wanted.

### Prerequisites

- BC-PRQ-05005 -> BC-SKL-05049, supporting, [inferred], Prerequisite for Name the quantity to be optimised and assign the variables.
- BC-SKL-05049 -> BC-SKL-05050, hard_prerequisite, [inferred], Prerequisite for Use the constraint to write the objective as a function of one variable.
- BC-PRQ-05005 -> BC-SKL-05050, supporting, [inferred], Prerequisite for Use the constraint to write the objective as a function of one variable.
- BC-SKL-05050 -> BC-SKL-05051, hard_prerequisite, [inferred], Prerequisite for Determine the domain of the objective from the context.
- BC-PRQ-05003 -> BC-SKL-05051, supporting, [inferred], Prerequisite for Determine the domain of the objective from the context.
- BC-SKL-05050 -> BC-SKL-05052, hard_prerequisite, [inferred], Prerequisite for Differentiate the objective and solve for critical points.
- BC-SKL-05010 -> BC-SKL-05052, hard_prerequisite, [inferred], Prerequisite for Differentiate the objective and solve for critical points.
- BC-SKL-05052 -> BC-SKL-05053, hard_prerequisite, [inferred], Prerequisite for Verify that the critical point gives the required extremum on the domain.
- BC-SKL-05028 -> BC-SKL-05053, hard_prerequisite, [inferred], Prerequisite for Verify that the critical point gives the required extremum on the domain.
- BC-SKL-05038 -> BC-SKL-05053, hard_prerequisite, [inferred], Prerequisite for Verify that the critical point gives the required extremum on the domain.
- BC-TOP-0402 -> BC-SKL-05049, supporting, [inferred], Building a model from a verbal situation, a Unit 4 skill not yet in data/skills.json; the topic id stands in for it.

### Required mathematical knowledge

**Model.** An optimisation problem supplies an objective quantity to be made largest or smallest and a constraint relating the variables. Substituting the constraint reduces the objective to one variable (BC-EK-FUN-4B1).

**Domain.** The domain of the reduced objective comes from the context, for example a length that cannot be negative or exceed a fixed total. The domain decides whether the endpoints are candidates.

**Closing the argument.** Either the candidates test on a closed contextual domain, or the sole critical point rule of BC-EK-FUN-4A8 on an open one, settles that the critical point gives the required extremum.

**Notation.** objective function; constraint equation; a domain written as an interval in the contextual variable.

### Representations

Representations in play: BC-REP-01 Symbolic (analytical) expression, BC-REP-04 Verbal description, BC-REP-05 Contextual model, BC-REP-08 Geometric diagram.

Conversions tested: verbal situation to an objective and a constraint (BC-REP-04 to BC-REP-01), diagram to a constraint equation (BC-REP-08 to BC-REP-01), and reduced objective to a contextual domain (BC-REP-01 to BC-REP-05).

### Assessment behaviour

MCQ forms supply the reduced objective already and ask for the extremum. FRQ forms build the model inside a longer applied question and score the setup, the differentiation, and the verification separately. Calculator variants solve the derivative equation numerically and demand the setup to be shown before the numerical answer; no-calculator variants keep the algebra factorable. Conceptual variants ask what the domain should be; computational variants ask for the critical point; justification variants require the verification that the critical point gives the extremum on the stated domain; multi-concept variants attach a related rate or an interpretation with units.

### Archetypes

- BC-QA-05011 Applied optimisation with model setup, domain, and verification

### Errors and misconceptions

- BC-ERR-05050 Variables used without being defined
- BC-ERR-99033 Chief Reader error record, see data/errors.json
- BC-ERR-05051 Constraint not substituted, leaving two variables
- BC-ERR-05052 Contextual domain omitted or taken as all inputs
- BC-ERR-05053 Objective differentiated with respect to the wrong variable
- BC-ERR-05054 No verification that the critical point gives the extremum
- BC-ERR-99004 Chief Reader error record, see data/errors.json
- BC-MIS-05027 An optimisation answer is the critical point of whatever expression appears first, severity high
- BC-MIS-05028 The contextual domain is all inputs, severity medium
- BC-MIS-05018 A local test settles a global question, severity high
- BC-MIS-05029 Finding a critical point finishes an optimisation, severity high

### Diagnostic signals

- BC-SIG-05040 Objective written with undefined letters
- BC-SIG-05041 Two variables carried into the differentiation
- BC-SIG-05042 No contextual domain stated
- BC-SIG-05043 Critical point reported with no verification

### Adaptive metadata summary

Skills in this topic carry calculator relevance none, optional. Remediation targets named across the topic: BC-PRQ-05003, BC-PRQ-05005, BC-SKL-05050, BC-SKL-05052. Every skill record carries the full seven key adaptive block in data/staging/unit-05.skills.json. [inferred]

## 5.11 Solving Optimization Problems

### Official mapping

Topic id BC-TOP-0511, CED code 5.11, name Solving Optimization Problems, scope shared, CED page 109. [verified] (ced:109)

- BC-LO-FUN-4C (FUN-4.C): Interpret minimum and maximum values calculated in applied contexts.
  - BC-EK-FUN-4C1 (FUN-4.C.1): "Minimum and maximum values of a function take on specific meanings in applied contexts."

Suggested practice skills: BC-MPS-3F (Practice skill 3.F). Weighting pointer: [../exam/exam-blueprint.md](../exam/exam-blueprint.md).

### Concept breakdown

- BC-CON-05014 Interpretation of an optimal value in context: The answer to an applied optimisation question is a statement about the situation, with units, not only a number.

- BC-SKL-05054 Report the optimal value with its units and the input where it occurs: Give the best value, its units, and where it happens.
- BC-SKL-05055 Interpret the optimal value as a statement about the situation: Say in words what the number means for the thing being modelled.
- BC-SKL-05056 Check the optimum against the endpoints of the contextual domain: Compare the interior candidate with the ends of the allowed range.
- BC-SKL-05057 Answer the question asked in an applied optimisation: Return the thing the question wanted, value or dimensions.

### Prerequisites

- BC-SKL-05053 -> BC-SKL-05054, hard_prerequisite, [inferred], Prerequisite for Report the optimal value with its units and the input where it occurs.
- BC-SKL-05054 -> BC-SKL-05055, hard_prerequisite, [inferred], Prerequisite for Interpret the optimal value as a statement about the situation.
- BC-SKL-05051 -> BC-SKL-05056, hard_prerequisite, [inferred], Prerequisite for Check the optimum against the endpoints of the contextual domain.
- BC-SKL-05028 -> BC-SKL-05056, hard_prerequisite, [inferred], Prerequisite for Check the optimum against the endpoints of the contextual domain.
- BC-SKL-05054 -> BC-SKL-05057, hard_prerequisite, [inferred], Prerequisite for Answer the question asked in an applied optimisation.

### Required mathematical knowledge

**Interpretation.** The extreme value of the objective and the input at which it occurs both carry meaning and units in the modelled situation (BC-EK-FUN-4C1).

**Completeness of an interpretation.** Scoring guidelines for interpretation points in adjacent units required the quantity, the units, and the interval or instant to be named together (sg-23:2), and treated an interpretation that names only the quantity as incomplete (cited here as the same standard applied to an optimal value).

**Value against location.** A question asking for the largest volume wants the volume, while a question asking for the dimensions that give the largest volume wants the inputs.

**Notation.** units written as a product or a quotient of the modelled units; the phrase at time t equal to, or when the length is.

### Representations

Representations in play: BC-REP-04 Verbal description, BC-REP-05 Contextual model, BC-REP-09 Calculator-generated numerical result.

Conversions tested: numerical extremum to a sentence about the situation (BC-REP-09 to BC-REP-04), and contextual model to the units of the optimal value (BC-REP-05 to BC-REP-04).

### Assessment behaviour

MCQ forms ask what an optimal value means in the stated situation. FRQ forms add an interpretation sentence to the optimisation part and score it separately from the computation. Calculator variants report a decimal to three places; no-calculator variants report an exact value. Conceptual variants ask which units the answer carries; computational variants ask for the value; interpretation variants ask for a sentence naming the quantity, the units, and the input at which the extremum occurs; justification variants require the verification to be in the same response as the interpretation; multi-concept variants pair the interpretation with an endpoint comparison.

### Archetypes

- BC-QA-05011 Applied optimisation with model setup, domain, and verification

### Errors and misconceptions

- BC-ERR-05055 Units omitted from the reported optimum
- BC-ERR-99005 Chief Reader error record, see data/errors.json
- BC-ERR-05056 Interpretation omits the quantity or the input where the extremum occurs
- BC-ERR-99027 Chief Reader error record, see data/errors.json
- BC-ERR-05026 One or both endpoints omitted from the candidate comparison
- BC-ERR-99004 Chief Reader error record, see data/errors.json
- BC-ERR-05024 Location reported where the value was asked for
- BC-MIS-05030 A numerical answer is a complete interpretation, severity medium
- BC-MIS-05028 The contextual domain is all inputs, severity medium
- BC-MIS-05015 The location of an extremum and its value are the same answer, severity medium

### Diagnostic signals

- BC-SIG-05044 Optimal value reported without units
- BC-SIG-05045 Interpretation naming the quantity only

### Adaptive metadata summary

Skills in this topic carry calculator relevance none, optional. Remediation targets named across the topic: BC-SKL-05051, BC-SKL-05053, BC-SKL-05054. Every skill record carries the full seven key adaptive block in data/staging/unit-05.skills.json. [inferred]

## 5.12 Exploring Behaviors of Implicit Relations

### Official mapping

Topic id BC-TOP-0512, CED code 5.12, name Exploring Behaviors of Implicit Relations, scope shared, CED page 110. [verified] (ced:110)

- BC-LO-FUN-4D (FUN-4.D): Determine critical points of implicit relations.
  - BC-EK-FUN-4D1 (FUN-4.D.1): "A point on an implicit relation where the first derivative equals zero or does not exist is a critical point of the function."
- BC-LO-FUN-4E (FUN-4.E): Justify conclusions about the behavior of an implicitly defined function based on evidence from its derivatives.
  - BC-EK-FUN-4E1 (FUN-4.E.1): "Applications of derivatives can be extended to implicitly defined functions."
  - BC-EK-FUN-4E2 (FUN-4.E.2): "Second derivatives involving implicit differentiation may be relations of x, y, and dy/dx."

Suggested practice skills: BC-MPS-1E (Practice skill 1.E), BC-MPS-3E (Practice skill 3.E). Weighting pointer: [../exam/exam-blueprint.md](../exam/exam-blueprint.md).

### Concept breakdown

- BC-CON-05015 Critical points and behaviour of an implicit relation: A curve defined by an equation in two variables has critical points and bending, found from the derivative expression obtained implicitly.

- BC-SKL-05058 Determine where the derivative of an implicit relation equals zero: Find the points on the curve with a horizontal tangent.
- BC-SKL-05059 Determine where the derivative of an implicit relation fails to exist: Find the points on the curve with a vertical tangent.
- BC-SKL-05060 Solve the defining relation and the derived condition together: Use both equations to get the actual point on the curve.
- BC-SKL-05061 Compute a second derivative of an implicit relation: Differentiate the derivative expression again, keeping both variables.
- BC-SKL-05062 Substitute the derivative expression to evaluate a second derivative at a point: Put the value of the first derivative back in to get a number.
- BC-SKL-05063 Classify a critical point of an implicit relation using the second derivative: Use the sign of the second derivative at the point to call it a high or low point.

### Prerequisites

- BC-PRQ-05007 -> BC-SKL-05058, supporting, [inferred], Prerequisite for Determine where the derivative of an implicit relation equals zero.
- BC-PRQ-05001 -> BC-SKL-05058, supporting, [inferred], Prerequisite for Determine where the derivative of an implicit relation equals zero.
- BC-PRQ-05007 -> BC-SKL-05059, supporting, [inferred], Prerequisite for Determine where the derivative of an implicit relation fails to exist.
- BC-PRQ-05001 -> BC-SKL-05059, supporting, [inferred], Prerequisite for Determine where the derivative of an implicit relation fails to exist.
- BC-SKL-05058 -> BC-SKL-05060, hard_prerequisite, [inferred], Prerequisite for Solve the defining relation and the derived condition together.
- BC-SKL-05059 -> BC-SKL-05060, hard_prerequisite, [inferred], Prerequisite for Solve the defining relation and the derived condition together.
- BC-PRQ-05007 -> BC-SKL-05060, supporting, [inferred], Prerequisite for Solve the defining relation and the derived condition together.
- BC-PRQ-05007 -> BC-SKL-05061, supporting, [inferred], Prerequisite for Compute a second derivative of an implicit relation.
- BC-SKL-05061 -> BC-SKL-05062, hard_prerequisite, [inferred], Prerequisite for Substitute the derivative expression to evaluate a second derivative at a point.
- BC-SKL-05062 -> BC-SKL-05063, hard_prerequisite, [inferred], Prerequisite for Classify a critical point of an implicit relation using the second derivative.
- BC-SKL-05036 -> BC-SKL-05063, hard_prerequisite, [inferred], Prerequisite for Classify a critical point of an implicit relation using the second derivative.
- BC-TOP-0301 -> BC-SKL-05061, hard_prerequisite, [inferred], The chain rule, a Unit 3 skill not yet in data/skills.json; the topic id stands in for it.
- BC-TOP-0302 -> BC-SKL-05058, hard_prerequisite, [inferred], Implicit differentiation, a Unit 3 skill not yet in data/skills.json; the topic id stands in for it.
- BC-TOP-0302 -> BC-SKL-05061, hard_prerequisite, [inferred], Implicit differentiation, a Unit 3 skill not yet in data/skills.json; the topic id stands in for it.

### Required mathematical knowledge

**Critical points of a relation.** For a relation in x and y, a point is critical where dy/dx equals zero, which for a quotient form means the numerator vanishes while the denominator does not, or where dy/dx fails to exist, which means the denominator vanishes (BC-EK-FUN-4D1).

**Two conditions at once.** A critical point of a relation is a point on the curve, so the coordinates must satisfy both the defining equation and the derived condition (BC-PRQ-05007).

**Second derivative form.** Implicit differentiation of dy/dx produces an expression in x, y, and dy/dx, and evaluating it at a point needs the value of dy/dx there substituted in (BC-EK-FUN-4E2). The 2025 guideline scored the substitution of the derivative expression and the differentiation itself as separate points, and allowed a response that erred in one to remain eligible for the value point through the other (sg-25:21).

**Notation.** dy/dx written as a quotient in x and y; d2y/dx2 written in terms of x, y, and dy/dx; a point given as an ordered pair.

### Representations

Representations in play: BC-REP-01 Symbolic (analytical) expression, BC-REP-02 Graphical, BC-REP-06 Differential equation.

Conversions tested: defining equation to a derivative expression in two variables (BC-REP-01 to BC-REP-01), and derivative expression plus the relation to a point on the curve (BC-REP-01 to BC-REP-02).

### Assessment behaviour

MCQ forms give a relation and ask at which listed point the tangent is horizontal or vertical. FRQ forms ask for the second derivative at a point on a curve defined implicitly or by a differential equation and score the differentiation and the substitution separately (sg-25:21). Calculator status is no calculator for the symbolic work. Conceptual variants ask what makes a point critical on a relation; computational variants ask for the coordinates or the second derivative value; justification variants require the classification to cite the sign of the second derivative at the point; multi-concept variants continue into a Taylor polynomial or a tangent line approximation built on the same values.

### Archetypes

- BC-QA-05012 Critical points and second derivative behaviour of an implicit relation

### Errors and misconceptions

- BC-ERR-05057 Horizontal tangent points found without checking the denominator
- BC-ERR-05058 Vertical tangent points reported without a matching point on the relation
- BC-ERR-05059 One coordinate reported where a point was asked for
- BC-ERR-05060 Second derivative of a relation taken as though the second variable were constant
- BC-ERR-05061 First derivative left unsubstituted in the second derivative
- BC-ERR-99002 Chief Reader error record, see data/errors.json
- BC-ERR-05062 Sign of the second derivative at the point misread for the classification
- BC-MIS-05031 A relation has critical points only where its derivative is zero, severity medium
- BC-MIS-05032 A single coordinate names a point on a relation, severity medium
- BC-MIS-05033 Implicit differentiation may treat the dependent variable as a constant, severity high
- BC-MIS-05023 The second derivative test always decides, severity medium

### Diagnostic signals

- BC-SIG-05046 Numerator zeros reported with no denominator check
- BC-SIG-05047 Denominator zeros reported without checking the relation
- BC-SIG-05048 One coordinate reported for a point on a relation
- BC-SIG-05049 Second derivative taken with the dependent variable held fixed
- BC-SIG-05050 Derivative symbol left in a numerical answer

### Adaptive metadata summary

Skills in this topic carry calculator relevance none. Remediation targets named across the topic: BC-PRQ-05007, BC-SKL-05061, BC-SKL-05062. Every skill record carries the full seven key adaptive block in data/staging/unit-05.skills.json. [inferred]

## Cross-unit connections

Cross-unit edges use BC-TOP ids as the node on the other unit's side, because no skills exist in data/skills.json for Units 1 to 4 yet; the `notes` field on each edge in data/staging/unit-05.edges.csv describes the skill that the topic id stands in for. Unit 6 skills already exist in data/skills.json and are referenced by id. [inferred]

### What Unit 5 depends on

**Unit 1 limits and continuity.** Both existence theorems of this unit rest on continuity over an interval. BC-SKL-05002 and BC-SKL-05008 carry edges from BC-TOP-0102 for that reason. The Extreme Value Theorem hypothesis is a continuity check and nothing else (BC-EK-FUN-1C1).

**Unit 2 derivatives.** Every sign analysis in the unit presupposes that a derivative can be produced. BC-SKL-05014 and BC-SKL-05030 carry edges from BC-TOP-0205, and BC-SKL-05011 draws on the classification of points where a derivative fails to exist, recorded as an edge from BC-TOP-0115.

**Unit 3 composite and implicit differentiation.** Topic 5.12 is Unit 3 applied: BC-SKL-05058 and BC-SKL-05061 carry edges from BC-TOP-0302, and BC-SKL-05061 also from BC-TOP-0301 because the second differentiation of a relation is a chain rule on the dependent variable.

**Unit 4 contextual modelling.** BC-SKL-05049 carries an edge from BC-TOP-0402 because building an objective from a verbal situation is the same modelling move as building a related rates equation, and BC-SKL-05046 carries an edge from BC-TOP-0406 because a tangent line approximation is read as an over or under estimate through concavity (sg-23:11).

### What depends on Unit 5

**Unit 6.** The accumulation function questions of Unit 6 are Unit 5 questions about a function defined by an integral. BC-SKL-06023, BC-SKL-06025, and BC-SKL-06026 in data/skills.json apply the first derivative test, the concavity test, and the candidates test respectively, and the edges file records them against BC-SKL-05020, BC-SKL-05033, and BC-SKL-05028. BC-SKL-06021 supplies the derivative of an accumulation function that BC-SKL-05010 then sets equal to zero, which is exactly the form of BC-QA-05007 (sg-24:13, sg-25:16).

**Unit 7.** A solution of a differential equation is analysed without being solved: the 2024 question located a critical point of the solution from the differential equation and classified it (sg-24:10), which is BC-QA-05007 with a differential equation as the given. The second derivative of a solution, used to decide whether a tangent line approximation is an over or under estimate, is BC-SKL-05061 and BC-SKL-05062 applied to a differential equation (sg-23:11).

**Unit 8 and Unit 9.** Extreme values of contextual and parametric quantities reuse BC-SKL-05024 through BC-SKL-05029 unchanged; the 2025 polar question located a leftmost point by setting a derivative equal to zero and was scored for considering that condition rather than for the solved value (sg-25:9).

**Unit 10.** The second derivative values produced by BC-SKL-05061 and BC-SKL-05062 are the coefficients of a second degree Taylor polynomial, which is how the 2025 question chained the two parts (sg-25:21, sg-25:22).

## Archetype summary

Thirteen archetypes with thirty nine variants are recorded in data/staging/unit-05.archetypes.json. Variant dimensions used are representation, reasoning direction, notation, calculator, and difficulty. [verified] (sg-23:3, sg-23:13, sg-23:14, sg-23:15, sg-24:10, sg-24:13, sg-25:4, sg-25:17, sg-25:19, sg-25:21)

| Archetype | Name | Scope | Calculator | Official parts read |
|---|---|---|---|---|
| BC-QA-05001 | Mean Value Theorem existence justification on an interval | shared | either | 2023 Q1(b), 2025 Q1(B) |
| BC-QA-05002 | Solving for the value the Mean Value Theorem provides | shared | either | 2025 Q1(B) |
| BC-QA-05003 | Relative extremum classified from the behaviour of the first derivative | shared | either | 2023 Q4(a) |
| BC-QA-05004 | Intervals of concavity from derivative information with a reason | shared | either | 2023 Q4(b) |
| BC-QA-05005 | Points of inflection identified with a reason tied to the given graph | shared | no_calculator | 2025 Q4(B) |
| BC-QA-05006 | Absolute extremum by the candidates test with a global justification | shared | either | 2023 Q4(d), 2025 Q4(D) |
| BC-QA-05007 | Critical point located and classified for a function given indirectly | shared | no_calculator | 2024 Q3(b), 2024 Q4(b) |
| BC-QA-05008 | Intervals of increase or decrease justified by the sign of the derivative | shared | either | none in 2023 to 2025 |
| BC-QA-05009 | Relating the graphs of a function and its first two derivatives | shared | either | none in 2023 to 2025 |
| BC-QA-05010 | Extreme Value Theorem existence claim on a closed interval | shared | no_calculator | none in 2023 to 2025 |
| BC-QA-05011 | Applied optimisation with model setup, domain, and verification | shared | either | none in 2023 to 2025 |
| BC-QA-05012 | Critical points and second derivative behaviour of an implicit relation | shared | no_calculator | 2025 Q5(A) |
| BC-QA-05013 | Second derivative test applied at a critical point | shared | either | 2024 Q3(b) alternate solution |

Four archetypes, BC-QA-05008, BC-QA-05009, BC-QA-05010, and BC-QA-05011, have no matching free response part in 2023 to 2025 and are tagged inferred. Their scoring patterns are drawn from the nearest analogous scored parts, chiefly the concavity part of 2023 Q4 and the inflection part of 2025 Q4, together with the CED text.

Two of the thirteen are the justification archetypes that the Chief Reader error records in data/errors.json speak to directly. BC-ERR-99001 (vague referent in a justification) matches BC-ERR-05018 and BC-ERR-05035; BC-ERR-99004 (local argument offered where a global argument is required) matches BC-ERR-05012, BC-ERR-05029, and BC-ERR-05039; BC-ERR-99008 (hypotheses of a theorem not verified before its conclusion is used) matches BC-ERR-05001, BC-ERR-05002, and BC-ERR-05007; and BC-ERR-99023 (points of inflection misidentified or justified without the given representation) matches BC-ERR-05033 and BC-ERR-05035. Those four Chief Reader ids are listed in the `common_errors` field of the corresponding skill records so that the link is machine readable without editing the shared records. [verified] (cr-22:14, cr-23:16, crabbc-25:18)

## Misconception summary

Thirty three misconceptions are recorded in data/staging/unit-05.misconceptions.json against sixty two observed errors in data/staging/unit-05.errors.json. The mapping is many to many: an error lists every misconception that could produce it together with non-conceptual causes such as an arithmetic slip, a misread, or time pressure, and every misconception carries rival misconceptions and a discriminating probe. [verified] (sg-23:3, sg-23:13, sg-23:15, sg-25:17, sg-25:19)

| Misconception | Severity | Rivals | Discriminating probe |
|---|---|---|---|
| BC-MIS-05001 Hypotheses are decoration and the conclusion is the theorem | high | BC-MIS-05002 | Give a function with a jump inside the interval and ask whether the conclusion still holds. |
| BC-MIS-05002 Naming a theorem is itself a justification | high | BC-MIS-05001, BC-MIS-05013 | Ask which sentence would convince a reader who had never heard of the theorem. |
| BC-MIS-05003 Average rate of change is the average of the endpoint values | medium | BC-MIS-05015 | Ask for the units of the quantity just computed. |
| BC-MIS-05004 An existence theorem locates the point it asserts | medium | BC-MIS-05002 | Ask what the theorem tells you about where the point is. |
| BC-MIS-05005 One existence theorem serves for values and for derivatives | high | BC-MIS-05002 | Ask which of the two theorems concerns the derivative. |
| BC-MIS-05006 Continuity may be assumed on any interval | medium | BC-MIS-05001 | Ask for a function on an open interval with no largest value. |
| BC-MIS-05007 A relative extremum is an absolute extremum | high | BC-MIS-05018 | Ask whether an endpoint can beat the interior candidate. |
| BC-MIS-05008 Every critical point is an extremum | high | BC-MIS-05014 | Ask for a function with a zero derivative at an input that is not an extremum. |
| BC-MIS-05009 The derivative exists wherever the function does | medium | BC-MIS-05008 | Ask for the derivative of the absolute value function at zero. |
| BC-MIS-05010 The sign of the derivative follows the sign of the function | high | BC-MIS-05011 | Ask for a function that is negative everywhere and increasing everywhere. |
| BC-MIS-05011 The plotted curve is the function under discussion | high | BC-MIS-05020 | Ask the student to label the plotted curve and the function under discussion separately. |
| BC-MIS-05012 A gap in the domain does not interrupt an interval of behaviour | medium | BC-MIS-05010 | Ask for the domain before any interval is reported. |
| BC-MIS-05013 Restating the conclusion counts as a reason | high | BC-MIS-05022 | Ask what feature of the given graph makes the stated claim true. |
| BC-MIS-05014 The classification comes from the derivative value rather than its change | high | BC-MIS-05008 | Ask for the sign of the derivative on each side, in those words. |
| BC-MIS-05015 The location of an extremum and its value are the same answer | medium | BC-MIS-05030 | Ask for both the input and the value. |
| BC-MIS-05016 The candidates are the critical points only | high | BC-MIS-05007 | Ask for the function value at each end of the interval. |
| BC-MIS-05017 The last candidate computed is the extremum | medium | BC-MIS-05016 | Ask which of the tabulated values is smallest and why. |
| BC-MIS-05018 A local test settles a global question | high | BC-MIS-05007 | Ask how the candidate compares with the value at the far end of the interval. |
| BC-MIS-05019 The second derivative behaves like the first | medium | BC-MIS-05020 | Ask what a positive second derivative says about the function and about the first derivative. |
| BC-MIS-05020 Concavity and monotonicity are the same property | high | BC-MIS-05011 | Ask the student to sketch a decreasing concave up curve. |
| BC-MIS-05021 A zero of the second derivative is a point of inflection | high | BC-MIS-05008 | Ask what the second derivative does on each side of the disputed input. |
| BC-MIS-05022 A reason is complete once symbols appear | medium | BC-MIS-05013 | Ask the student to write the same reason without any derivative symbols. |
| BC-MIS-05023 The second derivative test always decides | medium | BC-MIS-05024 | Ask what the test says when the second derivative is zero at the critical point. |
| BC-MIS-05024 The two derivative tests are interchangeable in every setting | medium | BC-MIS-05018 | Ask which derivative the given object shows and what the question is claiming. |
| BC-MIS-05025 A derivative determines its function uniquely | medium | BC-MIS-05011 | Ask the student to name two different functions with the same given derivative. |
| BC-MIS-05026 A table of values settles behaviour between the listed inputs | medium | BC-MIS-05010 | Ask whether another function through the same table could behave differently. |
| BC-MIS-05027 An optimisation answer is the critical point of whatever expression appears first | high | BC-MIS-05029 | Ask which quantity is to be made largest and which one is fixed. |
| BC-MIS-05028 The contextual domain is all inputs | medium | BC-MIS-05016 | Ask whether a negative length would make sense in the situation. |
| BC-MIS-05029 Finding a critical point finishes an optimisation | high | BC-MIS-05018, BC-MIS-05027 | Ask how the student knows it is a maximum rather than a minimum. |
| BC-MIS-05030 A numerical answer is a complete interpretation | medium | BC-MIS-05015 | Ask what the number measures and when it is attained. |
| BC-MIS-05031 A relation has critical points only where its derivative is zero | medium | BC-MIS-05009 | Ask what happens to the tangent line where the denominator vanishes. |
| BC-MIS-05032 A single coordinate names a point on a relation | medium | BC-MIS-05031 | Ask which outputs the relation pairs with the reported input. |
| BC-MIS-05033 Implicit differentiation may treat the dependent variable as a constant | high | BC-MIS-05025 | Ask for the derivative of the square of the dependent variable with respect to the independent one. |

The highest severity clusters are the four the scoring guidelines document directly: reading features of a function off whatever curve happens to be plotted (BC-MIS-05011, sg-25:16 and sg-25:17), accepting a local argument for a global extremum (BC-MIS-05007 and BC-MIS-05018, sg-23:15 and sg-25:19), offering a restatement in place of a reason tied to the given representation (BC-MIS-05013 and BC-MIS-05022, sg-25:17), and treating a zero derivative or a zero second derivative as the conclusion rather than the candidate condition (BC-MIS-05008 and BC-MIS-05021, sg-23:13 and sg-25:17).

## Unresolved

- BC-EK-FUN-1C1 is tagged single-source in data/curriculum.json because the Fall 2026 clarifications list it as reworded while the cached CED text already carries the new wording. The pre-2026 wording is not recoverable from this project's cache, so the records that quote it (BC-SKL-05007, BC-SKL-05009) inherit the single-source tag. [uncertain] (ced:100, ced-clarifications-2026:1)
- Four archetypes have no matching free response part in 2023 to 2025 (BC-QA-05008, BC-QA-05009, BC-QA-05010, BC-QA-05011). Applied optimisation in particular did not appear as a scored free response task in those three years, so BC-QA-05011 rests on the CED text and on the verification standard borrowed from the candidates test parts. This should be revisited when earlier years or official multiple choice material are indexed. [uncertain]
- The 2023 and 2025 guidelines phrase the justification requirement for an absolute extremum differently: 2023 requires both endpoints and no evaluation error at any candidate (sg-23:15), while 2025 requires evaluations or reasoning for each candidate and for no other inputs, and names the first and second derivative tests as insufficient (sg-25:19). Whether the 2025 wording is a tightening of practice or a question-specific decision is not established here. [uncertain]
- The 2023 guideline for the relative extremum part accepts a declaration that the derivative does not change sign while refusing a response that reports the derivative positive before and after the input (sg-23:13). The two statements are mathematically equivalent for that function, so the distinction is a communication standard rather than a mathematical one; it is recorded as BC-ERR-05023 for that reason. [verified] (sg-23:13)
- Misconception records are tagged inferred unless a scoring guideline names the behaviour directly. No misconception literature is cited, because none could be confirmed from the sources available in this project's cache. [inferred]

<!-- generated:official-evidence:start -->

## Official evidence index [verified]

Generated from data/frq_records.json and data/mcq_records.json. Every record cites its cached document and page; counts are observations over the indexed years only, not predictions. FRQ part records with BC-UNIT-05 as primary or secondary unit: 50. Public sample MCQ records tagged to this unit: 14.

| FRQ record | Role | Calculator | Archetype | Skills (first six) | Points | Point types |
|---|---|---|---|---|---|---|
| BC-FRQ-2013-Q1-C | secondary | calculator | BC-QA-08005 | BC-SKL-08013, BC-SKL-08014, BC-SKL-04012, BC-SKL-05017 | 2 | BC-PT-99005, BC-PT-99010 |
| BC-FRQ-2013-Q1-D | secondary | calculator | BC-QA-08006 | BC-SKL-08012, BC-SKL-08014, BC-SKL-05010, BC-SKL-05024, BC-SKL-05025, BC-SKL-05026 | 3 | BC-PT-99013, BC-PT-99004, BC-PT-99011 |
| BC-FRQ-2013-Q3-B | primary | no_calculator | BC-QA-05001 | BC-SKL-05001, BC-SKL-05002, BC-SKL-05003, BC-SKL-05004, BC-SKL-02019, BC-SKL-02020 | 2 | BC-PT-99021, BC-PT-99017 |
| BC-FRQ-2013-Q4-A | primary | no_calculator | BC-QA-05003 | BC-SKL-05015, BC-SKL-05019, BC-SKL-05020, BC-SKL-05022 | 1 | BC-PT-99012 |
| BC-FRQ-2013-Q4-B | primary | no_calculator | BC-QA-05006 | BC-SKL-05024, BC-SKL-05025, BC-SKL-05026, BC-SKL-05027, BC-SKL-05028, BC-SKL-06028 | 3 | BC-PT-99013, BC-PT-99004, BC-PT-99011 |
| BC-FRQ-2013-Q4-C | primary | no_calculator | BC-QA-05004 | BC-SKL-05015, BC-SKL-05017, BC-SKL-05031, BC-SKL-05035 | 2 | BC-PT-99062, BC-PT-99063 |
| BC-FRQ-2014-Q3-B | secondary | no_calculator | BC-QA-05004 | BC-SKL-06022, BC-SKL-06025, BC-SKL-05031, BC-SKL-05035, BC-SKL-05017 | 2 | BC-PT-99062, BC-PT-99063 |
| BC-FRQ-2015-Q1-B | secondary | calculator | BC-QA-08005 | BC-SKL-08013, BC-SKL-08014, BC-SKL-04012, BC-SKL-05017 | 2 | BC-PT-99014, BC-PT-99010 |
| BC-FRQ-2015-Q1-C | secondary | calculator | BC-QA-08006 | BC-SKL-08012, BC-SKL-08014, BC-SKL-05010, BC-SKL-05024, BC-SKL-05025, BC-SKL-05026 | 3 | BC-PT-99013, BC-PT-99004, BC-PT-99011 |
| BC-FRQ-2015-Q4-B | secondary | no_calculator | BC-QA-07010 | BC-SKL-03030, BC-SKL-03033, BC-SKL-05030, BC-SKL-07018 | 2 | BC-PT-99027, BC-PT-99063 |
| BC-FRQ-2015-Q4-C | primary | no_calculator | BC-QA-05003 | BC-SKL-07010, BC-SKL-05010, BC-SKL-05021, BC-SKL-05022 | 2 | BC-PT-99013, BC-PT-99012 |
| BC-FRQ-2015-Q5-B | primary | no_calculator | BC-QA-05003 | BC-SKL-05010, BC-SKL-05020, BC-SKL-05022, BC-SKL-05039 | 2 | BC-PT-99013, BC-PT-99012 |
| BC-FRQ-2015-Q5-C | primary | no_calculator | BC-QA-05007 | BC-SKL-05010, BC-SKL-05058 | 1 | BC-PT-99004 |
| BC-FRQ-2018-Q1-D | secondary | calculator | BC-QA-08006 | BC-SKL-08012, BC-SKL-08014, BC-SKL-05010, BC-SKL-05024, BC-SKL-05025, BC-SKL-05026 | 0 |  |
| BC-FRQ-2018-Q3-C | secondary | no_calculator | BC-QA-05004 | BC-SKL-06022, BC-SKL-06025, BC-SKL-05031, BC-SKL-05035, BC-SKL-05017 | 0 |  |
| BC-FRQ-2018-Q3-D | primary | no_calculator | BC-QA-05005 | BC-SKL-06024, BC-SKL-05032, BC-SKL-05033, BC-SKL-05035 | 0 |  |
| BC-FRQ-2018-Q4-B | primary | no_calculator | BC-QA-05001 | BC-SKL-05001, BC-SKL-05002, BC-SKL-05003, BC-SKL-05004, BC-SKL-02019, BC-SKL-02020 | 0 |  |
| BC-FRQ-2019-Q1-C | secondary | calculator | BC-QA-08006 | BC-SKL-08013, BC-SKL-08014, BC-SKL-05029, BC-SKL-06026, BC-SKL-05024 | 3 | BC-PT-99013, BC-PT-99004, BC-PT-99010 |
| BC-FRQ-2019-Q1-D | secondary | calculator | BC-QA-04005 | BC-SKL-04014, BC-SKL-04005, BC-SKL-03030, BC-SKL-05014 | 2 | BC-PT-99027, BC-PT-99010 |
| BC-FRQ-2019-Q3-C | secondary | no_calculator | BC-QA-06003 | BC-SKL-06018, BC-SKL-06023, BC-SKL-06026, BC-SKL-05024, BC-SKL-05026 | 3 | BC-PT-99024, BC-PT-99013, BC-PT-99011 |
| BC-FRQ-2019-Q4-B | secondary | no_calculator | BC-QA-07010 | BC-SKL-07018, BC-SKL-03030, BC-SKL-03034, BC-SKL-05014 | 3 | BC-PT-99027, BC-PT-99023, BC-PT-99010 |
| BC-FRQ-2021-Q1-C | secondary | calculator | BC-QA-06001 | BC-SKL-06010, BC-SKL-02036, BC-SKL-05017 | 2 | BC-PT-99022, BC-PT-99026 |
| BC-FRQ-2021-Q2-C | secondary | calculator | BC-QA-09005 | BC-SKL-09021, BC-SKL-09026, BC-SKL-09019, BC-SKL-05020, BC-SKL-05029 | 5 | BC-PT-99013, BC-PT-99010, BC-PT-99033, BC-PT-99004, BC-PT-99005 |
| BC-FRQ-2021-Q3-B | primary | no_calculator | BC-QA-05007 | BC-SKL-05010, BC-SKL-05019, BC-SKL-05023, BC-SKL-08040 | 2 | BC-PT-99013, BC-PT-99005 |
| BC-FRQ-2021-Q4-A | secondary | no_calculator | BC-QA-06003 | BC-SKL-06025, BC-SKL-06018, BC-SKL-05031, BC-SKL-05035 | 1 | BC-PT-99062 |
| BC-FRQ-2021-Q4-D | primary | no_calculator | BC-QA-05001 | BC-SKL-05003, BC-SKL-05001, BC-SKL-05002, BC-SKL-05004, BC-SKL-06020 | 2 | BC-PT-99021, BC-PT-99017 |
| BC-FRQ-2022-Q1-C | secondary | calculator | BC-QA-04005 | BC-SKL-04014, BC-SKL-04005, BC-SKL-05014, BC-SKL-05017 | 2 | BC-PT-99014, BC-PT-99010 |
| BC-FRQ-2022-Q1-D | secondary | calculator | BC-QA-08006 | BC-SKL-08013, BC-SKL-08014, BC-SKL-06018, BC-SKL-05024, BC-SKL-05026, BC-SKL-05028 | 4 | BC-PT-99013, BC-PT-99064, BC-PT-99004, BC-PT-99011 |
| BC-FRQ-2022-Q3-B | primary | no_calculator | BC-QA-05005 | BC-SKL-05032, BC-SKL-05033, BC-SKL-05035, BC-SKL-05031 | 2 | BC-PT-99060, BC-PT-99061 |
| BC-FRQ-2022-Q3-C | primary | no_calculator | BC-QA-05008 | BC-SKL-05015, BC-SKL-05017, BC-SKL-02030, BC-SKL-05014 | 2 | BC-PT-99005, BC-PT-99063 |
| BC-FRQ-2022-Q3-D | primary | no_calculator | BC-QA-05006 | BC-SKL-05010, BC-SKL-05024, BC-SKL-05026, BC-SKL-05028, BC-SKL-05027 | 2 | BC-PT-99013, BC-PT-99011 |
| BC-FRQ-2023-Q1-B | primary | calculator | BC-QA-05001 | BC-SKL-05006, BC-SKL-05003, BC-SKL-02019, BC-SKL-05001 | 2 | BC-PT-99021, BC-PT-99017 |
| BC-FRQ-2023-Q3-C | secondary | no_calculator | BC-QA-07005 | BC-SKL-03033, BC-SKL-07018, BC-SKL-04030, BC-SKL-04031, BC-SKL-05046 | 2 | BC-PT-99027, BC-PT-99026 |
| BC-FRQ-2023-Q4-A | primary | no_calculator | BC-QA-05003 | BC-SKL-05020, BC-SKL-05021, BC-SKL-05015, BC-SKL-05022 | 1 | BC-PT-99012 |
| BC-FRQ-2023-Q4-B | primary | no_calculator | BC-QA-05004 | BC-SKL-05031, BC-SKL-05030, BC-SKL-05035, BC-SKL-05015 | 2 | BC-PT-99062, BC-PT-99063 |
| BC-FRQ-2023-Q4-D | primary | no_calculator | BC-QA-05006 | BC-SKL-05024, BC-SKL-05025, BC-SKL-05026, BC-SKL-05027, BC-SKL-05028, BC-SKL-06020 | 3 | BC-PT-99013, BC-PT-99011, BC-PT-99004 |
| BC-FRQ-2024-Q1-D | primary | calculator | BC-QA-05008 | BC-SKL-05014, BC-SKL-05017, BC-SKL-04005, BC-SKL-04015 | 1 | BC-PT-99010 |
| BC-FRQ-2024-Q2-D | secondary | calculator | BC-QA-09008 | BC-SKL-09027, BC-SKL-04009, BC-SKL-04012, BC-SKL-05014 | 2 | BC-PT-99014, BC-PT-99010 |
| BC-FRQ-2024-Q3-B | secondary | no_calculator | BC-QA-05007 | BC-SKL-07018, BC-SKL-05010, BC-SKL-05020, BC-SKL-05022, BC-SKL-07010 | 3 | BC-PT-99014, BC-PT-99004, BC-PT-99012 |
| BC-FRQ-2024-Q4-B | secondary | no_calculator | BC-QA-06003 | BC-SKL-06018, BC-SKL-06022, BC-SKL-05010, BC-SKL-05022 | 2 | BC-PT-99024, BC-PT-99013 |
| BC-FRQ-2025-Q1-B | secondary | calculator | BC-QA-08002 | BC-SKL-02001, BC-SKL-02004, BC-SKL-05003, BC-SKL-05005, BC-SKL-08004 | 2 | BC-PT-99021, BC-PT-99005 |
| BC-FRQ-2025-Q1-D | primary | calculator | BC-QA-05006 | BC-SKL-06018, BC-SKL-05010, BC-SKL-05024, BC-SKL-05025, BC-SKL-05026, BC-SKL-05028 | 3 | BC-PT-99013, BC-PT-99011, BC-PT-99005 |
| BC-FRQ-2025-Q2-C | secondary | calculator | BC-QA-09011 | BC-SKL-09034, BC-SKL-09029, BC-SKL-05010, BC-SKL-05024, BC-SKL-05025, BC-SKL-05028 | 3 | BC-PT-99013, BC-PT-99011, BC-PT-99005 |
| BC-FRQ-2025-Q4-B | primary | no_calculator | BC-QA-05005 | BC-SKL-06024, BC-SKL-05032, BC-SKL-05033, BC-SKL-05035, BC-SKL-05031 | 2 | BC-PT-99060, BC-PT-99061 |
| BC-FRQ-2025-Q4-D | primary | no_calculator | BC-QA-05006 | BC-SKL-06026, BC-SKL-05024, BC-SKL-05025, BC-SKL-05026, BC-SKL-05028, BC-SKL-05029 | 3 | BC-PT-99013, BC-PT-99011, BC-PT-99004 |
| BC-FRQ-2026-Q2-C | primary | calculator | BC-QA-05007 | BC-SKL-05010, BC-SKL-05020, BC-SKL-05036, BC-SKL-05039, BC-SKL-09030 | 2 | BC-PT-99004, BC-PT-99012 |
| BC-FRQ-2026-Q3-C | secondary | no_calculator | BC-QA-07005 | BC-SKL-07018, BC-SKL-04030, BC-SKL-04031, BC-SKL-05046, BC-SKL-05030 | 2 | BC-PT-99027, BC-PT-99026 |
| BC-FRQ-2026-Q4-B | primary | no_calculator | BC-QA-05005 | BC-SKL-05032, BC-SKL-05033, BC-SKL-05031, BC-SKL-05035, BC-SKL-05042 | 2 | BC-PT-99060, BC-PT-99061 |
| BC-FRQ-2026-Q4-C | primary | no_calculator | BC-QA-05004 | BC-SKL-05015, BC-SKL-05031, BC-SKL-05017, BC-SKL-05047, BC-SKL-05035 | 2 | BC-PT-99062, BC-PT-99063 |
| BC-FRQ-2026-Q4-D | primary | no_calculator | BC-QA-05006 | BC-SKL-05024, BC-SKL-05029, BC-SKL-05026, BC-SKL-05028, BC-SKL-05015, BC-SKL-06028 | 3 | BC-PT-99013, BC-PT-99011, BC-PT-99011 |

| MCQ record | Calculator | Archetype | Skills |
|---|---|---|---|
| BC-MCQ-CED-013 | calculator | BC-QA-05001 | BC-SKL-05001, BC-SKL-05004, BC-SKL-05048 |
| BC-MCQ-CED-014 | calculator | BC-QA-05005 | BC-SKL-05032, BC-SKL-05033, BC-SKL-05031 |
| BC-MCQ-SAMPLE-011 | calculator | BC-QA-05009 | BC-SKL-05041, BC-SKL-05042, BC-SKL-02019 |
| BC-MCQ-SAMPLE-012 | calculator | BC-QA-05008 | BC-SKL-05014, BC-SKL-05016, BC-SKL-05017 |
| BC-MCQ-SAMPLE-014 | calculator | BC-QA-05001 | BC-SKL-05001, BC-SKL-05002, BC-SKL-05004 |
| BC-MCQ-PE2012-012 | no_calculator | BC-QA-07010 | BC-SKL-07006, BC-SKL-05036, BC-SKL-05033 |
| BC-MCQ-PE2012-029 | calculator | BC-QA-05009 | BC-SKL-02022, BC-SKL-05011, BC-SKL-05031 |
| BC-MCQ-PE2012-030 | calculator | BC-QA-05008 | BC-SKL-05014, BC-SKL-02033, BC-SKL-08021 |
| BC-MCQ-PE2012-033 | calculator | BC-QA-05009 | BC-SKL-05015, BC-SKL-05031, BC-SKL-05020 |
| BC-MCQ-PE2012-034 | calculator | BC-QA-05005 | BC-SKL-05033, BC-SKL-05032, BC-SKL-05047 |
| BC-MCQ-PE2012-037 | calculator | BC-QA-05004 | BC-SKL-05030, BC-SKL-05031, BC-SKL-05032 |
| BC-MCQ-PE2012-039 | calculator | BC-QA-06003 | BC-SKL-06036, BC-SKL-05014, BC-SKL-06028 |
| BC-MCQ-PE2012-041 | calculator | BC-QA-05009 | BC-SKL-05041, BC-SKL-05031, BC-SKL-05043 |
| BC-MCQ-PE2012-045 | calculator | BC-QA-05009 | BC-SKL-05042, BC-SKL-06031, BC-SKL-05020 |

<!-- generated:official-evidence:end -->
