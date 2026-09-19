---
title: AP Calculus BC Question Archetypes
research_date: 2026-09-19
status: draft
purpose: The full catalogue of question archetypes grouped by reasoning family, with the structure, scoring behaviour, variation space, and difficulty factors of each.
---

# AP Calculus BC Question Archetypes

One entry per archetype record in `../../data/archetypes.json`. 129 archetypes are active and 5 are retired into a canonical record after cross-unit consolidation. Families group archetypes whose reasoning structure is the same; two archetypes stay apart whenever the reasoning differs, even where the topic is shared. Variant dimensions are catalogued in [archetype-variants.md](archetype-variants.md), representations in [representation-types.md](representation-types.md), difficulty factors in [difficulty-factors.md](difficulty-factors.md), and calculator behaviour in [calculator-vs-noncalculator.md](calculator-vs-noncalculator.md).

## Family absolute-extremum-candidates [verified]

1 archetype(s): BC-QA-05006.

### BC-QA-05006 Absolute extremum by the candidates test with a global justification

Evidence tag: verified. Scope: shared. Primary unit: BC-UNIT-05. Units: BC-UNIT-05. Sources: sg-23:15, sg-25:19, frq-23:8, frq-25:7.

**Description.** The response must find the absolute maximum or minimum of a function on a closed interval and justify the choice over the whole interval.

**Concepts and skills required.** BC-SKL-05010, BC-SKL-05024, BC-SKL-05025, BC-SKL-05026, BC-SKL-05027, BC-SKL-05028, BC-SKL-05029

**Prerequisites.** BC-PRQ-05001, BC-PRQ-05004

**Typical wording.**
- find the absolute minimum value of the function on the closed interval and justify the answer
- find the input at which the function attains an absolute minimum on the closed interval and justify the answer

**Common givens.**
- a function or its derivative
- one known function value
- a closed interval

**What is produced.**
- the derivative condition considered
- a candidate table
- the extremum

**Representations.** BC-REP-01 (Symbolic (analytical) expression), BC-REP-02 (Graphical), BC-REP-03 (Numerical table)

**Calculator status.** either

**Multipart structure.** One part of a multipart free response question, worth three points.

**Scoring pattern.** One point for considering the derivative equal to zero, which listing the zeros alone does not earn; one point for the justification, which in 2023 required every candidate and both endpoints to be handled and no evaluation error at any candidate, and in 2025 required evaluations or reasoning for each candidate and for no other inputs; one point for the answer, which in 2023 was given only for the extreme value and not for its location. A local first or second derivative argument does not earn the justification point but leaves the answer point available (sg-23:15, sg-25:19).

**Scoring point types.** none recorded. Point type definitions are in [../scoring/point-taxonomy.md](../scoring/point-taxonomy.md).

**Common distractors.**
- omitting one or both endpoints from the comparison
- reporting the location where the value was asked for
- offering a first derivative test as the justification
- including inputs that are not candidates

**Wrong approaches.**
- appealing to the Extreme Value Theorem as though it located the extremum

**Misconceptions.** BC-MIS-05007, BC-MIS-05015, BC-MIS-05016, BC-MIS-05017, BC-MIS-05018

**Variants.** 3 recorded: BC-QV-05006-01, BC-QV-05006-02, BC-QV-05006-03

**Official examples notes.** 2023 Q4(d), 2025 Q4(D)

**Invariant structure.** The interval is closed, the candidate list is the critical points together with both endpoints, and the justification is scored as a separate point from the derivative condition and from the value.

**Safe variables.**
- the letter for the function
- the interval endpoints
- the supplied function value

**Difficulty variables.**
- how many critical points lie inside the interval
- whether candidate values come from a formula or from accumulated area
- whether a critical point can be eliminated by reference to an earlier part
- whether the minimum or the maximum is asked for

Mapped difficulty factors: BC-DF-01 (Number of concepts combined), BC-DF-08 (Multi-step dependency)

**Expected solution path.**
- consider the derivative equal to zero and solve
- form the candidate list with both endpoints
- evaluate the function at every candidate
- compare and report the extreme value

**Prohibited shortcuts.**
- none recorded in this record

**Multi-skill extensions.**
- none recorded in this record

## Family accumulation-extremum [verified]

1 archetype(s): BC-QA-08006.

### BC-QA-08006 Time at which an accumulated amount is maximal

Evidence tag: verified. Scope: shared. Primary unit: BC-UNIT-08. Units: BC-UNIT-08. Sources: sg-25:5, crabbc-25:4, frq-25:3.

**Description.** An amount function defined with an integral is given on a closed interval, and the response finds where it attains its maximum and justifies the claim globally.

**Concepts and skills required.** BC-SKL-08014, BC-SKL-08012

**Prerequisites.** BC-PRQ-08001

**Typical wording.**
- at what time in the stated interval does the modelled amount attain its maximum value, and justify the answer

**Common givens.**
- an amount function defined with a definite integral
- a closed interval

**What is produced.**
- an equation for the critical point
- a global justification
- the time of the maximum

**Representations.** BC-REP-05 (Contextual model), BC-REP-09 (Calculator-generated numerical result), BC-REP-01 (Symbolic (analytical) expression)

**Calculator status.** calculator

**Multipart structure.** The closing part of the calculator active free response question.

**Scoring pattern.** Three points: considering the derivative equal to zero, a global justification, and the answer; a first or second derivative test presented alone does not earn the justification point but leaves the answer point available (sg-25:5).

**Scoring point types.** none recorded. Point type definitions are in [../scoring/point-taxonomy.md](../scoring/point-taxonomy.md).

**Common distractors.**
- a first derivative test offered alone
- the endpoint of the interval
- the critical point of the rate rather than of the amount

**Wrong approaches.**
- presenting a local argument for a global claim
- omitting one endpoint from the candidates table

**Misconceptions.** BC-MIS-08008

**Variants.** 3 recorded: BC-QV-08006-01, BC-QV-08006-02, BC-QV-08006-03

**Official examples notes.** 2025 Q1(D)

**Invariant structure.** One amount function on a closed interval, one critical point found by setting its derivative equal to zero, and a justification that compares the candidate with both endpoints or argues from a unique sign change.

**Safe variables.**
- the modelled quantity
- the interval
- the form of the two competing terms

**Difficulty variables.**
- whether the derivative must be assembled from a given rate and a subtracted term
- whether the candidates test or a sign change argument is used
- the number of candidates in the interval

Mapped difficulty factors: BC-DF-09 (Theorem recognition), BC-DF-10 (Required justification), BC-DF-12 (Sign and direction handling)

**Expected solution path.**
- differentiate the amount function
- set the derivative equal to zero and solve numerically
- evaluate the amount at the candidate and at both endpoints, or argue from a unique sign change
- report the time

**Prohibited shortcuts.**
- none recorded in this record

**Multi-skill extensions.**
- none recorded in this record

## Family accumulation-function-analysis [verified]

1 archetype(s): BC-QA-06003.

### BC-QA-06003 Accumulation function analysed from the graph of the integrand

Evidence tag: verified. Scope: shared. Primary unit: BC-UNIT-06. Units: BC-UNIT-06. Sources: sg-25:15, sg-25:16, sg-25:17, sg-25:18, sg-25:19, sg-24:12, sg-24:13, frq-25:7, frq-24:8.

**Description.** A function f is given by a graph made of segments and circular arcs, an accumulation function g is defined as the integral of f from a fixed input to x, and the response evaluates g, differentiates g, and locates extrema and points of inflection of g.

**Concepts and skills required.** BC-SKL-06020, BC-SKL-06022, BC-SKL-06023, BC-SKL-06024, BC-SKL-06025, BC-SKL-06026, BC-SKL-06027, BC-SKL-06018

**Prerequisites.** BC-PRQ-06007, BC-PRQ-06013

**Typical wording.**
- let g be the function defined by the integral of f from a fixed input to x; find the value of g prime at a stated input and give a reason
- find all values of x at which the graph of g has a point of inflection and give a reason
- find the value of x at which g attains an absolute minimum on the closed interval and justify your answer

**Common givens.**
- none recorded in this record

**What is produced.**
- none recorded in this record

**Representations.** BC-REP-02 (Graphical)

**Calculator status.** no_calculator

**Multipart structure.** Typically one part of a multipart free response question, or a single multiple choice item.

**Scoring pattern.** Separate points for the answer and for the reason, with the reason point requiring the argument to be tied to the given graph of f; a reason phrased only in terms of g double prime or of g changing concavity earns the answer point but not the reason point, and a global candidates argument must evaluate g at every critical input and at both endpoints (sg-25:17, sg-25:19). Any extra declared inflection input costs both points of that part (sg-25:17).

**Scoring point types.** none recorded. Point type definitions are in [../scoring/point-taxonomy.md](../scoring/point-taxonomy.md).

**Common distractors.**
- treating the graph shown as the graph of g rather than of f
- locating inflection points of g where f crosses the axis
- giving a relative extremum argument where a global argument is demanded
- counting a semicircular region as a full circle
- reporting a signed area as an unsigned area

**Wrong approaches.**
- none recorded in this record; see ../misconceptions/error-to-concept-map.md

**Misconceptions.** BC-MIS-06006, BC-MIS-06007, BC-MIS-06008, BC-MIS-06009, BC-MIS-06010, BC-MIS-06011, BC-MIS-06012

**Variants.** 3 recorded: BC-QV-06003-01, BC-QV-06003-02, BC-QV-06003-03

**Official examples notes.** 2025 Q4(A), 2025 Q4(B), 2025 Q4(C), 2025 Q4(D), 2024 Q4(a), 2024 Q4(b)

**Invariant structure.** The integrand is presented only as a graph whose pieces have computable areas; the accumulation function has a fixed lower limit and a variable upper limit; every question about g is answered from a feature of f rather than from a formula.

**Safe variables.**
- the shapes making up the graph
- the location of the fixed lower limit
- the names of the functions
- the closed interval

**Difficulty variables.**
- whether the lower limit lies inside or at an end of the displayed interval
- whether regions below the axis are involved
- whether a global or a local argument is demanded
- whether the question asks about g, g prime, or g double prime
- whether a second function defined by the integral of f prime is also introduced

Mapped difficulty factors: BC-DF-04 (Notation complexity), BC-DF-10 (Required justification)

**Expected solution path.**
- evaluate g at the requested inputs as signed areas
- use the Fundamental Theorem of Calculus to write g prime equal to f
- locate sign changes of f for extrema of g and turning points of f for inflection points of g
- for an absolute extreme value, evaluate g at every critical input and at both endpoints and compare

**Prohibited shortcuts.**
- none recorded in this record

**Multi-skill extensions.**
- none recorded in this record

## Family accumulation-interpretation [verified]

1 archetype(s): BC-QA-06015.

### BC-QA-06015 Interpreting a definite integral in context with units

Evidence tag: verified. Scope: shared. Primary unit: BC-UNIT-06. Units: BC-UNIT-06, BC-UNIT-08. Sources: sg-23:2, sg-24:3, frq-23:3, frq-24:3.

**Description.** A definite integral of a contextual rate is displayed and the response states in words what it measures, with correct units and the correct time or input interval.

**Concepts and skills required.** BC-SKL-06001, BC-SKL-06002, BC-SKL-06003, BC-SKL-06038, BC-SKL-08015, BC-SKL-08005

**Prerequisites.** BC-PRQ-06005

**Typical wording.**
- using correct units, interpret the meaning of the displayed definite integral in the context of the problem

**Common givens.**
- a contextual rate function
- a definite integral expression

**What is produced.**
- a sentence with quantity, interval, and units

**Representations.** BC-REP-04 (Verbal description), BC-REP-05 (Contextual model), BC-REP-01 (Symbolic (analytical) expression)

**Calculator status.** either

**Multipart structure.** Typically one part of a multipart free response question, or a single multiple choice item.

**Scoring pattern.** One interpretation point that requires both the accumulated quantity with its units and the interval of accumulation; an interpretation that omits the interval does not earn the point (sg-23:2). Where the displayed expression is an average value, the interpretation must say average over the stated interval (sg-24:3).

**Scoring point types.** none recorded. Point type definitions are in [../scoring/point-taxonomy.md](../scoring/point-taxonomy.md).

**Common distractors.**
- describing the integral as a rate rather than as an accumulated amount
- omitting the interval
- reporting the units of the rate rather than of the accumulation
- describing an average value expression as a total
- the rate at an endpoint
- the average value of the rate
- the amount present rather than the change

**Wrong approaches.**
- naming the quantity without the interval
- giving the units of the rate rather than of the accumulation

**Misconceptions.** BC-MIS-06014, BC-MIS-06025, BC-MIS-08009, BC-MIS-08001

**Variants.** 5 recorded: BC-QV-06015-01, BC-QV-06015-02, BC-QV-06015-03, BC-QV-08007-01, BC-QV-08007-02

**Official examples notes.** 2023 Q1(a), 2024 Q1(b); 2023 Q1(a), 2024 Q1(b)

**Invariant structure.** The integral of a rate over an interval measures the accumulated change in the associated quantity across that interval; the interpretation must name the quantity, the units, and the interval.

**Safe variables.**
- the quantity
- the unit of the rate
- the interval endpoints
- the units
- the endpoints of the interval

**Difficulty variables.**
- whether the displayed expression is a plain integral or an average value
- whether the rate is positive throughout
- whether the response must also produce a numerical value
- whether the quantity accumulates or depletes
- whether the expression carries a factor that makes it an average
- whether the integrand is a rate or a quantity
- whether the interval is stated in the stem or only in the limits

Mapped difficulty factors: BC-DF-02 (Prerequisite depth), BC-DF-07 (Calculator workflow), BC-DF-12 (Sign and direction handling), BC-DF-14 (Missing or implicit given)

**Expected solution path.**
- identify what the integrand measures per unit input
- multiply the units
- state the accumulated quantity over the named interval
- identify the integrand as a rate
- name the quantity accumulated
- name the interval from the limits
- attach the units

**Prohibited shortcuts.**
- none recorded in this record

**Multi-skill extensions.**
- none recorded in this record

## Family accumulation-with-initial-condition [verified]

1 archetype(s): BC-QA-06005.

### BC-QA-06005 Net change from a rate with an initial condition

Evidence tag: verified. Scope: shared. Primary unit: BC-UNIT-06. Units: BC-UNIT-06, BC-UNIT-08. Sources: sg-24:3, sg-24:4, sg-25:14, frq-24:3, frq-25:6, sg-24:7.

**Description.** A rate of change is given analytically over an interval together with the value of the quantity at one endpoint, and the response computes the value at the other endpoint or the total amount accumulated.

**Concepts and skills required.** BC-SKL-06036, BC-SKL-06037, BC-SKL-06034, BC-SKL-08012, BC-SKL-08016, BC-SKL-08017, BC-SKL-08009

**Prerequisites.** BC-PRQ-06002, BC-PRQ-06005, BC-PRQ-08006

**Typical wording.**
- the rate of change of the quantity is modelled by the given function; find the value of the quantity at the later time, showing the setup for your calculations
- based on the model, how much of the quantity has accumulated by the end of the interval
- find the value of the modelled quantity at the later time and show the setup for the calculations

**Common givens.**
- a rate function
- a known value of the quantity at one time

**What is produced.**
- an integral expression with the initial value
- a numerical value with units

**Representations.** BC-REP-01 (Symbolic (analytical) expression), BC-REP-05 (Contextual model), BC-REP-09 (Calculator-generated numerical result)

**Calculator status.** either

**Multipart structure.** Typically one part of a multipart free response question, or a single multiple choice item.

**Scoring pattern.** Separate points for the integral, for the use of the initial condition, and for the answer; a response that presents only the integral value without adding the initial condition does not earn the initial condition point (sg-24:3, sg-24:4). Where no initial condition is present the points fall to the integrand, the antiderivative, and the value, and eligibility for the answer point requires the antiderivative point (sg-25:14).

**Scoring point types.** none recorded. Point type definitions are in [../scoring/point-taxonomy.md](../scoring/point-taxonomy.md).

**Common distractors.**
- reporting the integral alone as the final value
- omitting the initial value
- using the rate value at an endpoint in place of the integral
- subtracting rather than adding the accumulated change when the rate is negative
- the value of the integral reported as the amount
- the initial value subtracted rather than added
- the rate evaluated at the endpoint

**Wrong approaches.**
- reporting the net change as the amount
- antidifferentiating and substituting only the upper limit

**Misconceptions.** BC-MIS-06013, BC-MIS-08006

**Variants.** 6 recorded: BC-QV-06005-01, BC-QV-06005-02, BC-QV-06005-03, BC-QV-08004-01, BC-QV-08004-02, BC-QV-08004-03

**Official examples notes.** 2024 Q1(c), 2025 Q3(D); 2024 Q1(c), 2025 Q3(D), 2024 Q2(c)

**Invariant structure.** The quantity is recovered as the initial value plus the definite integral of its rate; the integral supplies the change and the initial condition supplies the level.

**Safe variables.**
- the context and units
- the interval endpoints
- the algebraic form of the rate
- the modelled quantity
- the units
- the two times involved

**Difficulty variables.**
- whether an initial condition is supplied or must be located
- whether the rate has an elementary antiderivative
- calculator versus no calculator
- whether the rate changes sign on the interval
- whether the question asks for the value or only for the change
- whether the rate is given by a formula, a table, or a graph
- whether the initial value is given directly or must be read
- whether the integrand is antidifferentiable by hand

Mapped difficulty factors: BC-DF-03 (Unusual representation), BC-DF-06 (Algebraic burden), BC-DF-07 (Calculator workflow), BC-DF-12 (Sign and direction handling), BC-DF-14 (Missing or implicit given), BC-DF-17 (Case splitting at a boundary)

**Expected solution path.**
- write the value at the later input as the value at the earlier input plus the definite integral of the rate
- evaluate the integral analytically or with technology
- combine with the initial value
- report with units
- write the amount as the known value plus the definite integral of the rate
- evaluate the integral
- add the known value

**Prohibited shortcuts.**
- none recorded in this record

**Multi-skill extensions.**
- none recorded in this record

## Family antidifferentiation-technique [verified]

3 archetype(s): BC-QA-06008, BC-QA-06009, BC-QA-06010.

### BC-QA-06008 Antiderivative or definite integral by substitution

Evidence tag: verified. Scope: shared. Primary unit: BC-UNIT-06. Units: BC-UNIT-06. Sources: ced:126, sg-23:17, sg-23:16.

**Description.** An integrand is a composite multiplied by a constant multiple of the derivative of its inner expression, and the response finds the indefinite integral or evaluates a definite integral by substitution.

**Concepts and skills required.** BC-SKL-06047, BC-SKL-06048, BC-SKL-06049, BC-SKL-06050, BC-SKL-06051, BC-SKL-06052, BC-SKL-06034

**Prerequisites.** BC-PRQ-06001, BC-PRQ-06002, BC-PRQ-06003

**Typical wording.**
- find the indefinite integral of the given composite expression, showing the work that leads to your answer
- evaluate the definite integral of the given expression over the stated interval

**Common givens.**
- none recorded in this record

**What is produced.**
- none recorded in this record

**Representations.** BC-REP-01 (Symbolic (analytical) expression)

**Calculator status.** no_calculator

**Multipart structure.** Typically one part of a multipart free response question, or a single multiple choice item.

**Scoring pattern.** A response that applies the original limits to an expression still written in u is not eligible for the answer point even when the numerical value is correct (sg-23:17, sg-23:16).

**Scoring point types.** none recorded. Point type definitions are in [../scoring/point-taxonomy.md](../scoring/point-taxonomy.md).

**Common distractors.**
- forgetting the constant factor introduced by du
- leaving the original limits attached to an expression written in u
- omitting the constant of integration in an indefinite integral
- omitting the absolute value inside a logarithmic antiderivative

**Wrong approaches.**
- none recorded in this record; see ../misconceptions/error-to-concept-map.md

**Misconceptions.** BC-MIS-06016, BC-MIS-06017, BC-MIS-06018

**Variants.** 3 recorded: BC-QV-06008-01, BC-QV-06008-02, BC-QV-06008-03

**Official examples notes.** 2023 Q5(a), 2023 Q5(b)

**Invariant structure.** There is an inner expression whose derivative appears as a factor up to a constant; replacing it by u reduces the integrand to a basic form; a definite integral additionally requires either converted limits or back-substitution.

**Safe variables.**
- the outer function
- the inner linear or polynomial expression
- whether the integral is definite or indefinite

**Difficulty variables.**
- whether a constant adjustment is needed
- whether the answer is logarithmic, exponential, trigonometric, or a power
- definite versus indefinite
- whether the limits must be converted
- whether the substitution is disguised by a prior rearrangement

Mapped difficulty factors: BC-DF-02 (Prerequisite depth), BC-DF-06 (Algebraic burden), BC-DF-11 (Unfamiliar surface presentation), BC-DF-14 (Missing or implicit given)

**Expected solution path.**
- choose u as the inner expression
- compute du and adjust the constant
- rewrite the integral entirely in u
- antidifferentiate
- back-substitute or convert the limits and evaluate

**Prohibited shortcuts.**
- none recorded in this record

**Multi-skill extensions.**
- none recorded in this record

### BC-QA-06009 Antiderivative by integration by parts

Evidence tag: verified. Scope: BC_only. Primary unit: BC-UNIT-06. Units: BC-UNIT-06. Sources: sg-24:18, sg-23:18, frq-24:9, frq-23:9.

**Description.** An integrand is a product of unlike factors, one of which simplifies on differentiation, and the response applies integration by parts to find an indefinite integral or evaluate a definite one.

**Concepts and skills required.** BC-SKL-06057, BC-SKL-06058, BC-SKL-06059, BC-SKL-06060, BC-SKL-06061, BC-SKL-06034

**Prerequisites.** BC-PRQ-06002, BC-PRQ-06005

**Typical wording.**
- find the indefinite integral of the given product, showing the work that leads to your answer
- let h be defined as x times the derivative of an unknown function; find the value of the definite integral of h over the stated interval

**Common givens.**
- none recorded in this record

**What is produced.**
- none recorded in this record

**Representations.** BC-REP-01 (Symbolic (analytical) expression)

**Calculator status.** no_calculator

**Multipart structure.** Typically one part of a multipart free response question, or a single multiple choice item.

**Scoring pattern.** One point for the choice of u and dv, one for the u times v minus the integral of v du expression, and one for the answer; u and dv may be implied by the presence of the correct expression, the tabular arrangement is accepted, and the answer point is available only if the first two points were earned (sg-23:18, sg-24:18).

**Scoring point types.** none recorded. Point type definitions are in [../scoring/point-taxonomy.md](../scoring/point-taxonomy.md).

**Common distractors.**
- swapping the roles of u and dv so the remaining integral is harder
- dropping the minus sign before the integral of v du
- antidifferentiating the two factors separately and multiplying
- omitting the boundary term when the integral is definite

**Wrong approaches.**
- none recorded in this record; see ../misconceptions/error-to-concept-map.md

**Misconceptions.** BC-MIS-06019

**Variants.** 3 recorded: BC-QV-06009-01, BC-QV-06009-02, BC-QV-06009-03

**Official examples notes.** 2023 Q5(c), 2024 Q5(d)

**Invariant structure.** The integrand splits into u and dv so that du is simpler and v is obtainable; the answer is u times v minus the integral of v du, with the remaining integral resolvable by a basic rule.

**Safe variables.**
- the polynomial factor
- the transcendental factor
- the interval when the integral is definite

**Difficulty variables.**
- whether parts must be applied more than once
- definite versus indefinite
- whether the non polynomial factor is trigonometric, exponential, or logarithmic
- whether the integrand contains an unknown function and its derivative
- whether supplied values of the unknown function must be imported

Mapped difficulty factors: BC-DF-01 (Number of concepts combined), BC-DF-02 (Prerequisite depth), BC-DF-06 (Algebraic burden)

**Expected solution path.**
- declare u and dv and compute du and v
- write u times v minus the integral of v du
- evaluate the remaining integral
- apply the limits or add the constant of integration

**Prohibited shortcuts.**
- none recorded in this record

**Multi-skill extensions.**
- none recorded in this record

### BC-QA-06010 Antiderivative by linear partial fractions

Evidence tag: inferred. Scope: BC_only. Primary unit: BC-UNIT-06. Units: BC-UNIT-06. Sources: ced:129.

**Description.** A rational integrand with a denominator that factors into distinct linear factors is decomposed and antidifferentiated into a combination of natural logarithms.

**Concepts and skills required.** BC-SKL-06062, BC-SKL-06063, BC-SKL-06064, BC-SKL-06065

**Prerequisites.** BC-PRQ-06003, BC-PRQ-06011

**Typical wording.**
- find the indefinite integral of the given rational expression by decomposing it into partial fractions

**Common givens.**
- none recorded in this record

**What is produced.**
- none recorded in this record

**Representations.** BC-REP-01 (Symbolic (analytical) expression)

**Calculator status.** no_calculator

**Multipart structure.** Typically one part of a multipart free response question, or a single multiple choice item.

**Scoring pattern.** No Unit 6 partial fraction part appears in the 2023 to 2025 scoring guidelines read for this unit, so the point structure is inferred from the technique parts of those years, where the technique setup and the antiderivative carry separate points and the value point depends on the antiderivative point.

**Scoring point types.** none recorded. Point type definitions are in [../scoring/point-taxonomy.md](../scoring/point-taxonomy.md).

**Common distractors.**
- sign errors when solving for the constants
- omitting the absolute value inside each logarithm
- decomposing without first dividing an improper rational integrand
- antidifferentiating a reciprocal of a linear factor without dividing by its leading coefficient

**Wrong approaches.**
- none recorded in this record; see ../misconceptions/error-to-concept-map.md

**Misconceptions.** BC-MIS-06022

**Variants.** 3 recorded: BC-QV-06010-01, BC-QV-06010-02, BC-QV-06010-03

**Official examples notes.** none in 2023 to 2025

**Invariant structure.** The denominator factors into distinct linear factors and the numerator degree is lower; the decomposition into constant over linear terms antidifferentiates term by term into logarithms.

**Safe variables.**
- the roots of the denominator
- the numerator constant
- definite versus indefinite

**Difficulty variables.**
- whether the numerator degree forces a division first
- whether the constants must be found by substitution or by equating coefficients
- whether the logarithms must be combined
- whether a definite integral requires the limits

Mapped difficulty factors: BC-DF-01 (Number of concepts combined), BC-DF-02 (Prerequisite depth), BC-DF-06 (Algebraic burden), BC-DF-08 (Multi-step dependency), BC-DF-14 (Missing or implicit given)

**Expected solution path.**
- factor the denominator
- write the decomposition with unknown constants
- clear denominators and solve for the constants
- antidifferentiate each term as a logarithm
- combine or evaluate at the limits

**Prohibited shortcuts.**
- none recorded in this record

**Multi-skill extensions.**
- none recorded in this record

## Family arc-length [verified]

2 archetype(s): BC-QA-08014, BC-QA-09003.

### BC-QA-08014 Arc length of a curve given by a function

Evidence tag: verified. Scope: BC_only. Primary unit: BC-UNIT-08. Units: BC-UNIT-08. Sources: sg-24:16, frq-24:9, ced:164.

**Description.** A function is given on an interval and the response either writes and evaluates the arc length integral or identifies a displayed integral as an arc length.

**Concepts and skills required.** BC-SKL-08056, BC-SKL-08057, BC-SKL-08058, BC-SKL-08059

**Prerequisites.** BC-PRQ-08007, BC-PRQ-08006

**Typical wording.**
- what information does the displayed integral give about the graph of the function
- find the length of the curve on the stated interval and show the setup

**Common givens.**
- a function, sometimes only through a table of its derivative
- a closed interval

**What is produced.**
- an integral expression, or a sentence naming arc length and the interval
- a numerical length

**Representations.** BC-REP-01 (Symbolic (analytical) expression), BC-REP-04 (Verbal description), BC-REP-09 (Calculator-generated numerical result)

**Calculator status.** either

**Multipart structure.** One part of a multipart BC only no calculator question, or a calculator active setup and value part.

**Scoring pattern.** In 2024 the identification was worth two points, one for naming the arc length of the function and one for naming the interval (sg-24:16); a numerical arc length part is scored as a setup point and an answer point.

**Scoring point types.** none recorded. Point type definitions are in [../scoring/point-taxonomy.md](../scoring/point-taxonomy.md).

**Common distractors.**
- the area under the curve
- the total distance travelled by a particle on the x axis
- the average value of the derivative

**Wrong approaches.**
- naming the arc length without naming the interval
- omitting the square on the derivative

**Misconceptions.** BC-MIS-08024

**Variants.** 3 recorded: BC-QV-08014-01, BC-QV-08014-02, BC-QV-08014-03

**Official examples notes.** 2024 Q5(b)

**Invariant structure.** One differentiable function, one closed interval, and the integral of the square root of one plus the square of the derivative, read in either direction between expression and meaning.

**Safe variables.**
- the function
- the interval
- the letters used

**Difficulty variables.**
- whether the response must produce the integral or interpret a supplied one
- whether the interval must be named explicitly
- whether the integrand is evaluated numerically

Mapped difficulty factors: BC-DF-05 (Contextual interpretation), BC-DF-09 (Theorem recognition)

**Expected solution path.**
- differentiate the function
- square the derivative and add one
- take the square root and integrate over the interval
- report the length, or name the length and its interval when interpreting

**Prohibited shortcuts.**
- none recorded in this record

**Multi-skill extensions.**
- none recorded in this record

### BC-QA-09003 Length of a parametric curve

Evidence tag: verified. Scope: BC_only. Primary unit: BC-UNIT-09. Units: BC-UNIT-09. Sources: sg-23:8, sg-24:6.

**Description.** The response writes and evaluates the integral of the magnitude of the pair of component rates over a parameter interval.

**Concepts and skills required.** BC-SKL-09011, BC-SKL-09012, BC-SKL-09013, BC-SKL-09014

**Prerequisites.** BC-PRQ-08007, BC-PRQ-08006

**Typical wording.**
- find the length of the curve on the stated parameter interval, or the total distance travelled by the particle over the stated time interval, and show the setup

**Common givens.**
- a parametric pair or a velocity vector
- a parameter or time interval

**What is produced.**
- a definite integral of a radical integrand
- a numerical length

**Representations.** BC-REP-12 (Parametric equations), BC-REP-01 (Symbolic (analytical) expression), BC-REP-09 (Calculator-generated numerical result)

**Calculator status.** calculator

**Multipart structure.** One part of the calculator active BC free response question.

**Scoring pattern.** Two points: the integral and the value; an incorrect speed integrand imported from an earlier part earns the integral point but not the answer point, and parenthesis errors already assessed in an earlier part are not assessed again (sg-23:8, sg-24:6).

**Scoring point types.** none recorded. Point type definitions are in [../scoring/point-taxonomy.md](../scoring/point-taxonomy.md).

**Common distractors.**
- the sum of the two component integrals
- the magnitude of the displacement vector
- the integral of one component alone

**Wrong approaches.**
- adding the component rates before squaring
- integrating over an interval that repeats part of the curve

**Misconceptions.** BC-MIS-09005, BC-MIS-09006

**Variants.** 3 recorded: BC-QV-09003-01, BC-QV-09003-02, BC-QV-09003-03

**Official examples notes.** 2023 Q2(d), 2024 Q2(b)

**Invariant structure.** One radical integrand built from the two component rates, one parameter interval that traces the piece once, one numerical value.

**Safe variables.**
- the components
- the interval
- the letters used

**Difficulty variables.**
- whether the curve is described as a path of a particle
- whether the interval traces the curve once
- whether an integrand is imported from an earlier speed part

Mapped difficulty factors: BC-DF-01 (Number of concepts combined), BC-DF-08 (Multi-step dependency)

**Expected solution path.**
- compute both component rates
- square each and add
- take the square root and integrate over the interval
- report the value

**Prohibited shortcuts.**
- none recorded in this record

**Multi-skill extensions.**
- none recorded in this record

## Family area-between-curves [verified]

3 archetype(s): BC-QA-08008, BC-QA-08009, BC-QA-08010.

### BC-QA-08008 Area of a region between two curves in x

Evidence tag: verified. Scope: shared. Primary unit: BC-UNIT-08. Units: BC-UNIT-08. Sources: sg-23:16, sg-23:17, frq-23:9.

**Description.** A shaded region bounded by two graphs is shown and the response sets up and evaluates the area integral in x.

**Concepts and skills required.** BC-SKL-08018, BC-SKL-08019, BC-SKL-08020, BC-SKL-08021, BC-SKL-08022

**Prerequisites.** BC-PRQ-08001

**Typical wording.**
- find the area of the shaded region enclosed by the graphs of the two functions

**Common givens.**
- a figure with a shaded region
- one or both curve equations
- sometimes the value of one definite integral

**What is produced.**
- an integrand
- an antiderivative or a numerical value
- the area

**Representations.** BC-REP-02 (Graphical), BC-REP-01 (Symbolic (analytical) expression), BC-REP-09 (Calculator-generated numerical result)

**Calculator status.** either

**Multipart structure.** The opening part of a multipart no calculator question, or one part of a calculator active question.

**Scoring pattern.** Three points in 2023: the integrand, an antiderivative of the explicitly given function, and the answer; a response writing the reversed difference and asserting it equals the positive area did not earn the answer point, while the same work stated correctly earned all three (sg-23:16, sg-23:17).

**Scoring point types.** none recorded. Point type definitions are in [../scoring/point-taxonomy.md](../scoring/point-taxonomy.md).

**Common distractors.**
- the reversed difference
- the integral of one function alone
- the difference of the two areas taken with the wrong sign

**Wrong approaches.**
- integrating the difference over an interval that extends past an intersection
- reporting a negative value as an area

**Misconceptions.** BC-MIS-08010, BC-MIS-08011

**Variants.** 3 recorded: BC-QV-08008-01, BC-QV-08008-02, BC-QV-08008-03

**Official examples notes.** 2023 Q5(a)

**Invariant structure.** Two boundary curves, one interval, one integrand that is the upper curve minus the lower curve, and a nonnegative reported value.

**Safe variables.**
- the two functions
- the letters used
- the position of the region in the plane

**Difficulty variables.**
- whether the limits require a numerical solve
- whether one of the two integrals is supplied as a number
- whether an antiderivative is needed by hand
- whether the region is bounded by a vertical line rather than an intersection

Mapped difficulty factors: BC-DF-06 (Algebraic burden), BC-DF-13 (Reversed reasoning direction), BC-DF-14 (Missing or implicit given)

**Expected solution path.**
- decide which curve is upper
- write the integral of the difference with the correct limits
- evaluate, using a supplied integral value where one is given
- report the area

**Prohibited shortcuts.**
- none recorded in this record

**Multi-skill extensions.**
- none recorded in this record

### BC-QA-08009 Area of a region integrated with respect to y

Evidence tag: inferred. Scope: shared. Primary unit: BC-UNIT-08. Units: BC-UNIT-08. Sources: ced:156.

**Description.** A region whose left and right boundaries are curves is presented, and the response integrates the difference of the curves with respect to y.

**Concepts and skills required.** BC-SKL-08023, BC-SKL-08024, BC-SKL-08025, BC-SKL-08026

**Prerequisites.** BC-PRQ-08002

**Typical wording.**
- find the area of the region bounded by the two curves by integrating with respect to y

**Common givens.**
- a figure
- curve equations in x or in y

**What is produced.**
- an integrand in y
- the area

**Representations.** BC-REP-02 (Graphical), BC-REP-01 (Symbolic (analytical) expression)

**Calculator status.** either

**Multipart structure.** One part of a multipart question, or a single multiple choice item.

**Scoring pattern.** A setup point for the integrand and limits in y and an answer point for the value, following the area scoring pattern of 2023 (sg-23:16).

**Scoring point types.** none recorded. Point type definitions are in [../scoring/point-taxonomy.md](../scoring/point-taxonomy.md).

**Common distractors.**
- an integrand in x paired with a dy differential
- limits taken as x values
- the reversed difference

**Wrong approaches.**
- integrating the original functions of x between y limits

**Misconceptions.** BC-MIS-08013

**Variants.** 2 recorded: BC-QV-08009-01, BC-QV-08009-02

**Official examples notes.** no area with respect to y appears in the 2023 to 2025 BC free response questions

**Invariant structure.** Two boundary curves written as functions of y, one interval of y values, and an integrand that is the right curve minus the left curve.

**Safe variables.**
- the two curves
- the orientation of the region
- the letters used

**Difficulty variables.**
- whether the curves must be inverted first
- whether the region would need two integrals in x
- whether limits are y values read from the figure

Mapped difficulty factors: BC-DF-08 (Multi-step dependency), BC-DF-14 (Missing or implicit given)

**Expected solution path.**
- write both boundaries as functions of y
- decide which is to the right
- integrate the difference with respect to y over the y interval
- report the area

**Prohibited shortcuts.**
- none recorded in this record

**Multi-skill extensions.**
- none recorded in this record

### BC-QA-08010 Area of a region whose boundary curves cross

Evidence tag: inferred. Scope: shared. Primary unit: BC-UNIT-08. Units: BC-UNIT-08. Sources: ced:157.

**Description.** Two curves cross inside the interval, so the area is a sum of integrals or a single integral of an absolute value.

**Concepts and skills required.** BC-SKL-08027, BC-SKL-08028, BC-SKL-08029, BC-SKL-08030

**Prerequisites.** BC-PRQ-08001, BC-PRQ-08003

**Typical wording.**
- find the total area of the region bounded by the two graphs over the stated interval

**Common givens.**
- two curve equations
- an interval or a figure

**What is produced.**
- a sum of definite integrals or one absolute value integral
- the total area

**Representations.** BC-REP-02 (Graphical), BC-REP-01 (Symbolic (analytical) expression), BC-REP-09 (Calculator-generated numerical result)

**Calculator status.** either

**Multipart structure.** One part of a multipart question, or a single multiple choice item.

**Scoring pattern.** The setup point requires every piece of the region, so a single integral across a crossing loses it, and the answer point follows the setup, in the pattern the 2023 area part uses (sg-23:16).

**Scoring point types.** none recorded. Point type definitions are in [../scoring/point-taxonomy.md](../scoring/point-taxonomy.md).

**Common distractors.**
- one integral of the difference across the whole interval
- the sum of the signed contributions
- only the larger lobe

**Wrong approaches.**
- integrating a fixed difference across a crossing

**Misconceptions.** BC-MIS-08014, BC-MIS-08011

**Variants.** 3 recorded: BC-QV-08010-01, BC-QV-08010-02, BC-QV-08010-03

**Official examples notes.** no split region area appears in the 2023 to 2025 BC free response questions

**Invariant structure.** Two curves with at least one interior intersection; the area is additive over the subintervals and each contribution is nonnegative.

**Safe variables.**
- the two curves
- the number of lobes
- the letters used

**Difficulty variables.**
- the number of interior crossings
- whether the crossings are exact or decimal
- whether the absolute value form is allowed by the calculator status

Mapped difficulty factors: BC-DF-07 (Calculator workflow), BC-DF-17 (Case splitting at a boundary)

**Expected solution path.**
- solve for every intersection in the interval
- order the crossings
- fix the order of subtraction on each piece
- sum the integrals or integrate the absolute value

**Prohibited shortcuts.**
- none recorded in this record

**Multi-skill extensions.**
- none recorded in this record

## Family average-value [verified]

1 archetype(s): BC-QA-08001.

### BC-QA-08001 Average value of a function over an interval

Evidence tag: verified. Scope: shared. Primary unit: BC-UNIT-08. Units: BC-UNIT-08, BC-UNIT-06. Sources: sg-25:2, sg-25:3, sg-23:4, sg-24:3, sg-23:3, frq-23:3, frq-25:3.

**Description.** A function is given by a model formula or a graph, and the response computes its average value over a stated interval and reports it in context.

**Concepts and skills required.** BC-SKL-08001, BC-SKL-08002, BC-SKL-08003, BC-SKL-08005, BC-SKL-06038, BC-SKL-06036

**Prerequisites.** BC-PRQ-08006, BC-PRQ-06005

**Typical wording.**
- find the average value of the modelled quantity over the stated time interval and show the setup for the calculations
- using correct units, interpret the meaning of the average you found
- find the average value of the function over the stated interval, showing the setup for your calculations
- interpret the meaning of one over the length of the interval times the definite integral of the rate in the context of the problem

**Common givens.**
- a model function in a context
- a closed interval of the independent variable

**What is produced.**
- an integral quotient
- a decimal value
- a sentence with units

**Representations.** BC-REP-01 (Symbolic (analytical) expression), BC-REP-05 (Contextual model), BC-REP-09 (Calculator-generated numerical result)

**Calculator status.** calculator

**Multipart structure.** One part of the calculator active free response question, or a single multiple choice item.

**Scoring pattern.** Two points: one for the correct integral together with evidence of division by the length of the interval, and one for the correct value reported to three decimal places; in 2025 unclear communication between the integral and the answer was treated as scratch work and both points were awarded (sg-25:3), while a 2023 response presenting the same kind of unlinked chain earned one of two points (sg-23:4).

**Scoring point types.** none recorded. Point type definitions are in [../scoring/point-taxonomy.md](../scoring/point-taxonomy.md).

**Common distractors.**
- the difference quotient of the function at the endpoints
- the value of the integral without the division
- the average of the endpoint values
- division by the number of data points
- reporting the integral without dividing
- dividing by the number of data points rather than the interval length
- computing the average rate of change of the function instead of the average value
- using a calculator in degree mode

**Wrong approaches.**
- averaging the two endpoint values
- dividing by the upper limit alone

**Misconceptions.** BC-MIS-08001, BC-MIS-08002, BC-MIS-06014, BC-MIS-06015

**Variants.** 6 recorded: BC-QV-06007-01, BC-QV-06007-02, BC-QV-06007-03, BC-QV-08001-01, BC-QV-08001-02, BC-QV-08001-03

**Official examples notes.** 2025 Q1(A), 2023 Q1(c), 2024 Q1(b); 2023 Q1(c), 2025 Q1(A), 2024 Q1(b)

**Invariant structure.** One function, one closed interval, one quotient: the definite integral of the function over the interval divided by the length of the interval, with the setup shown before the decimal.

**Safe variables.**
- the modelled quantity
- the units of the function
- the length of the interval
- the letters used for the variables
- the context
- the interval
- the algebraic form of the function

**Difficulty variables.**
- formula versus graph presentation
- whether the interval starts at zero
- whether an interpretation with units is demanded
- whether the average value is compared with an average rate of change in a later part
- whether the function is a rate or an amount
- whether an interpretation with units is required
- whether the average value of a function is confused with the average rate of change
- calculator versus no calculator

Mapped difficulty factors: BC-DF-03 (Unusual representation), BC-DF-05 (Contextual interpretation), BC-DF-07 (Calculator workflow), BC-DF-08 (Multi-step dependency), BC-DF-16 (Units and labelling demand)

**Expected solution path.**
- write the definite integral of the function over the interval
- divide by the length of the interval
- evaluate with technology
- report to three places after the decimal point with units
- write one over the length of the interval times the definite integral
- evaluate the integral
- divide and report to the required accuracy
- interpret in context when asked

**Prohibited shortcuts.**
- none recorded in this record

**Multi-skill extensions.**
- none recorded in this record

## Family concavity-analysis [verified]

2 archetype(s): BC-QA-05004, BC-QA-05005.

### BC-QA-05004 Intervals of concavity from derivative information with a reason

Evidence tag: verified. Scope: shared. Primary unit: BC-UNIT-05. Units: BC-UNIT-05. Sources: sg-23:14, frq-23:8.

**Description.** The response must name the open intervals on which the graph of a function is concave up or concave down and give a reason drawn from the given representation.

**Concepts and skills required.** BC-SKL-05030, BC-SKL-05031, BC-SKL-05035

**Prerequisites.** BC-PRQ-05006, BC-PRQ-05004

**Typical wording.**
- on what open intervals, if any, is the graph of the function concave down, and give a reason for the answer

**Common givens.**
- a graph of the derivative
- or a formula for the function

**What is produced.**
- a list of open intervals
- a reason about the behaviour of the derivative

**Representations.** BC-REP-01 (Symbolic (analytical) expression), BC-REP-02 (Graphical)

**Calculator status.** either

**Multipart structure.** One part of a multipart free response question, worth two points.

**Scoring pattern.** One point for the intervals and one for the reason, with the reason point available only when the intervals are correct. Endpoints may be included or excluded. A reason must discuss the behaviour of the derivative or the slopes of the derivative. A response giving exactly one of two correct intervals with a correct reason earns one of the two points (sg-23:14).

**Scoring point types.** none recorded. Point type definitions are in [../scoring/point-taxonomy.md](../scoring/point-taxonomy.md).

**Common distractors.**
- reporting where the derivative is positive instead of where it is increasing
- reporting closed intervals or single points
- giving one interval and omitting the other
- reasoning that the function is concave down because it is concave down

**Wrong approaches.**
- computing a second derivative formula when only a graph of the derivative is supplied

**Misconceptions.** BC-MIS-05011, BC-MIS-05013, BC-MIS-05020

**Variants.** 3 recorded: BC-QV-05004-01, BC-QV-05004-02, BC-QV-05004-03

**Official examples notes.** 2023 Q4(b)

**Invariant structure.** Concavity is asked for as open intervals, the given object is the derivative rather than the function, and the reason is scored separately from the intervals.

**Safe variables.**
- the shape of the derivative graph
- the interval of definition
- the letter for the function

**Difficulty variables.**
- whether more than one interval is correct
- whether the derivative graph includes a semicircular arc
- whether the question asks for concave up or concave down

Mapped difficulty factors: BC-DF-03 (Unusual representation)

**Expected solution path.**
- identify where the derivative is decreasing
- write those stretches as open intervals
- state the reason in terms of the derivative decreasing

**Prohibited shortcuts.**
- none recorded in this record

**Multi-skill extensions.**
- none recorded in this record

### BC-QA-05005 Points of inflection identified with a reason tied to the given graph

Evidence tag: verified. Scope: shared. Primary unit: BC-UNIT-05. Units: BC-UNIT-05. Sources: sg-25:17, frq-25:7.

**Description.** The response must list every input at which the graph of a function has a point of inflection and justify the list from the representation the question supplied.

**Concepts and skills required.** BC-SKL-05032, BC-SKL-05033, BC-SKL-05034, BC-SKL-05035

**Prerequisites.** BC-PRQ-05006

**Typical wording.**
- find all values in the open interval at which the graph has a point of inflection, and give a reason for the answer

**Common givens.**
- a graph of the derivative or of an integrand
- an open interval

**What is produced.**
- the complete list of inputs
- a reason phrased through the given function

**Representations.** BC-REP-02 (Graphical), BC-REP-04 (Verbal description)

**Calculator status.** no_calculator

**Multipart structure.** One part of a multipart free response question, worth two points.

**Scoring pattern.** One point for the answer and one for the reason. The answer point is lost if any extra input inside the interval is declared; consideration of the interval endpoints does not affect scoring. The reason point requires the reason to be tied to the given graph, so a reason phrased as the given function changing from increasing to decreasing earns it while a reason phrased as the second derivative changing sign does not; an ambiguous referent such as the function or the graph forfeits it. Two of three correct values with a correct reason earn the reason point but not the answer point (sg-25:17).

**Scoring point types.** none recorded. Point type definitions are in [../scoring/point-taxonomy.md](../scoring/point-taxonomy.md).

**Common distractors.**
- listing every zero of the given plotted function
- omitting a value where the given plot turns without crossing the axis
- phrasing the reason as the second derivative changing sign
- phrasing the reason with an unnamed referent

**Wrong approaches.**
- testing candidates with a second derivative test

**Misconceptions.** BC-MIS-05013, BC-MIS-05021, BC-MIS-05022

**Variants.** 3 recorded: BC-QV-05005-01, BC-QV-05005-02, BC-QV-05005-03

**Official examples notes.** 2025 Q4(B)

**Invariant structure.** The list must be exactly right for the answer point, the reason must be phrased in terms of the given object rather than restated in second derivative symbols, and the open interval of consideration excludes the endpoints.

**Safe variables.**
- the shape of the given graph
- the letters used
- the interval

**Difficulty variables.**
- how many points of inflection there are
- whether a candidate is a touching zero with no sign change
- whether the given object is f, f prime, or an integrand

Mapped difficulty factors: BC-DF-04 (Notation complexity), BC-DF-12 (Sign and direction handling)

**Expected solution path.**
- find where the given plot changes from increasing to decreasing or the reverse
- list exactly those inputs
- state the reason through the given plotted function

**Prohibited shortcuts.**
- none recorded in this record

**Multi-skill extensions.**
- none recorded in this record

## Family continuity-at-a-point [inferred]

1 archetype(s): BC-QA-01006.

### BC-QA-01006 Continuity at a point tested against the three conditions

Evidence tag: inferred. Scope: shared. Primary unit: BC-UNIT-01. Units: BC-UNIT-01. Sources: ced:48, ced:47.

**Description.** A piecewise defined function is given and the response determines whether it is continuous at a named input, naming the condition that fails when it is not.

**Concepts and skills required.** BC-SKL-01043, BC-SKL-01044, BC-SKL-01045, BC-SKL-01042, BC-SKL-01023

**Prerequisites.** BC-PRQ-01003

**Typical wording.**
- Determine whether the given function is continuous at the named input. Justify your answer.

**Common givens.**
- none recorded in this record

**What is produced.**
- none recorded in this record

**Representations.** BC-REP-01 (Symbolic (analytical) expression), BC-REP-02 (Graphical)

**Calculator status.** no_calculator

**Multipart structure.** Typically one part of a multipart free response question or a single multiple choice item.

**Scoring pattern.** One point for the value and the limit, and a separate justification point that requires naming which condition fails rather than restating the definition.

**Scoring point types.** none recorded. Point type definitions are in [../scoring/point-taxonomy.md](../scoring/point-taxonomy.md).

**Common distractors.**
- checking only that the function is defined at the input
- checking only that the one sided limits agree and stopping there
- evaluating the wrong branch at the boundary
- restating the definition in place of a reason

**Wrong approaches.**
- none recorded in this record; see ../misconceptions/error-to-concept-map.md

**Misconceptions.** BC-MIS-01009, BC-MIS-01010

**Variants.** 3 recorded: BC-QV-01006-01, BC-QV-01006-02, BC-QV-01006-03

**Official examples notes.** none in 2023 to 2025 as a standalone part [inferred]

**Invariant structure.** The named input is a boundary of the partition or a point excluded from a branch expression, so the test requires separate evaluation of the function value and of the one sided limits.

**Safe variables.**
- the branch expressions
- the boundary input
- the variable name

**Difficulty variables.**
- whether the function value is defined at the boundary
- whether the one sided limits agree
- whether the justification must name the failed condition
- whether the function is given by a rule or by a graph

Mapped difficulty factors: BC-DF-03 (Unusual representation), BC-DF-10 (Required justification), BC-DF-14 (Missing or implicit given), BC-DF-17 (Case splitting at a boundary)

**Expected solution path.**
- evaluate the function at the named input
- evaluate the left hand limit from the branch on that side
- evaluate the right hand limit from the branch on that side
- compare the limit with the function value
- state the conclusion and name the condition that fails when it does

**Prohibited shortcuts.**
- none recorded in this record

**Multi-skill extensions.**
- none recorded in this record

## Family continuity-interval [inferred]

1 archetype(s): BC-QA-01015.

### BC-QA-01015 Intervals of continuity determined from the domain of an expression

Evidence tag: inferred. Scope: shared. Primary unit: BC-UNIT-01. Units: BC-UNIT-01. Sources: ced:49.

**Description.** A function given by a rule is presented and the response states the intervals on which it is continuous.

**Concepts and skills required.** BC-SKL-01046, BC-SKL-01047, BC-SKL-01048, BC-SKL-01049

**Prerequisites.** BC-PRQ-01008, BC-PRQ-01010

**Typical wording.**
- State the intervals on which the given function is continuous and give a reason for your answer.

**Common givens.**
- none recorded in this record

**What is produced.**
- none recorded in this record

**Representations.** BC-REP-01 (Symbolic (analytical) expression)

**Calculator status.** no_calculator

**Multipart structure.** Typically a single multiple choice item.

**Scoring pattern.** One point for the intervals and one for the reason naming the family and its domain.

**Scoring point types.** none recorded. Point type definitions are in [../scoring/point-taxonomy.md](../scoring/point-taxonomy.md).

**Common distractors.**
- including an excluded input inside a stated interval
- writing the domain as a single interval when it has several pieces
- using closed brackets at an excluded input
- omitting the reason when one is demanded

**Wrong approaches.**
- none recorded in this record; see ../misconceptions/error-to-concept-map.md

**Misconceptions.** BC-MIS-01019

**Variants.** 3 recorded: BC-QV-01015-01, BC-QV-01015-02, BC-QV-01015-03

**Official examples notes.** none in 2023 to 2025 [inferred]

**Invariant structure.** The function belongs to families continuous on their domains, so the intervals of continuity are the maximal intervals of the domain, and every excluded input must be found from the rule.

**Safe variables.**
- the expression
- the variable name
- the number of excluded inputs

**Difficulty variables.**
- rational against radical against logarithmic against piecewise
- whether an endpoint requires a one sided argument
- whether the answer must be justified by naming the family
- whether the domain restriction is stated in the question

Mapped difficulty factors: BC-DF-02 (Prerequisite depth), BC-DF-10 (Required justification), BC-DF-14 (Missing or implicit given), BC-DF-17 (Case splitting at a boundary)

**Expected solution path.**
- identify every input at which the expression is undefined
- state the family to which the expression belongs and that it is continuous on its domain
- write the maximal intervals of continuity
- treat any endpoint with the appropriate one sided limit

**Prohibited shortcuts.**
- none recorded in this record

**Multi-skill extensions.**
- none recorded in this record

## Family convergence-test [verified]

4 archetype(s): BC-QA-10004, BC-QA-10005, BC-QA-10006, BC-QA-10007.

### BC-QA-10004 Convergence or divergence established with a named test

Evidence tag: verified. Scope: BC_only. Primary unit: BC-UNIT-10. Units: BC-UNIT-10. Sources: sg-24:19, sg-24:20, ced:191.

**Description.** A numerical series is given together with, or in need of, a specific test, and the response applies it with its conditions.

**Concepts and skills required.** BC-SKL-10011, BC-SKL-10012, BC-SKL-10013, BC-SKL-10018, BC-SKL-10019, BC-SKL-10020, BC-SKL-10022, BC-SKL-10023, BC-SKL-10024, BC-SKL-10027, BC-SKL-10028, BC-SKL-10029, BC-SKL-10030, BC-SKL-10033

**Prerequisites.** none recorded

**Typical wording.**
- determine whether the series converges or diverges, and give a reason for your answer

**Common givens.**
- none recorded in this record

**What is produced.**
- none recorded in this record

**Representations.** BC-REP-11 (Series (finite partial sums or infinite)), BC-REP-04 (Verbal description)

**Calculator status.** no_calculator

**Multipart structure.** Typically one part of the multipart free response question that closes Section II Part B, or a single multiple choice item.

**Scoring pattern.** Two points are typical, one for considering the right object and one for the answer with a reason (sg-24:19). A conclusion with no supporting condition earns the first point only.

**Scoring point types.** none recorded. Point type definitions are in [../scoring/point-taxonomy.md](../scoring/point-taxonomy.md).

**Common distractors.**
- stating the conclusion with no conditions
- reversing the comparison inequality
- concluding convergence from terms approaching zero

**Wrong approaches.**
- none recorded in this record; see ../misconceptions/error-to-concept-map.md

**Misconceptions.** BC-MIS-10005, BC-MIS-10006, BC-MIS-10007, BC-MIS-10009, BC-MIS-10010, BC-MIS-10012, BC-MIS-10013, BC-MIS-10017

**Variants.** 3 recorded: BC-QV-10004-01, BC-QV-10004-02, BC-QV-10004-03

**Official examples notes.** 2024 Q6(a)

**Invariant structure.** The series has nonnegative terms or an alternating factor; the response establishes the conditions of the named test and states the conclusion with the series identified.

**Safe variables.**
- the comparison partner chosen
- the letters in the general term
- the starting index

**Difficulty variables.**
- whether the test is named by the prompt
- whether the comparison partner must be supplied by the response
- whether the terms alternate

Mapped difficulty factors: BC-DF-09 (Theorem recognition)

**Expected solution path.**
- name the test
- state its conditions and verify them for this series
- carry out the computation the test requires
- state the conclusion naming the series

**Prohibited shortcuts.**
- none recorded in this record

**Multi-skill extensions.**
- none recorded in this record

### BC-QA-10005 Integral test with its conditions stated

Evidence tag: verified. Scope: BC_only. Primary unit: BC-UNIT-10. Units: BC-UNIT-10. Sources: sg-21:21, sg-21:22.

**Description.** The response states the three conditions the integral test requires, sets up the matching improper integral, evaluates it with limit notation, and transfers the conclusion.

**Concepts and skills required.** BC-SKL-10014, BC-SKL-10015, BC-SKL-10016, BC-SKL-10017

**Prerequisites.** none recorded

**Typical wording.**
- state the conditions necessary to use the integral test, then use the test to show that the series converges

**Common givens.**
- none recorded in this record

**What is produced.**
- none recorded in this record

**Representations.** BC-REP-11 (Series (finite partial sums or infinite)), BC-REP-01 (Symbolic (analytical) expression)

**Calculator status.** no_calculator

**Multipart structure.** Typically one part of the multipart free response question that closes Section II Part B, or a single multiple choice item.

**Scoring pattern.** Three points are typical, for the conditions, the improper integral, and the evaluation; all three conditions are required for the first, an incorrect lower limit costs the second while leaving the third reachable, and an evaluation written with the infinity symbol does not earn the third (sg-21:21, sg-21:22).

**Scoring point types.** none recorded. Point type definitions are in [../scoring/point-taxonomy.md](../scoring/point-taxonomy.md).

**Common distractors.**
- listing fewer than three conditions
- starting the integral at an index the series does not use
- substituting the infinity symbol into the antiderivative
- reporting the integral's value as the sum

**Wrong approaches.**
- none recorded in this record; see ../misconceptions/error-to-concept-map.md

**Misconceptions.** BC-MIS-10001, BC-MIS-10007, BC-MIS-10008

**Variants.** 3 recorded: BC-QV-10005-01, BC-QV-10005-02, BC-QV-10005-03

**Official examples notes.** 2021 Q6(a)

**Invariant structure.** The general term is the value at n of a function that is positive, decreasing, and continuous on the interval from the starting index onward; the series and the improper integral share a verdict.

**Safe variables.**
- the function chosen to match the terms
- the letter used for the variable bound
- the starting index

**Difficulty variables.**
- whether the conditions are requested explicitly
- whether the antiderivative needs substitution
- whether the integral diverges

Mapped difficulty factors: BC-DF-06 (Algebraic burden), BC-DF-09 (Theorem recognition)

**Expected solution path.**
- state that the function is positive, decreasing, and continuous on the interval
- write the improper integral with the correct lower limit
- evaluate with limit notation
- conclude about the series

**Prohibited shortcuts.**
- none recorded in this record

**Multi-skill extensions.**
- none recorded in this record

### BC-QA-10006 Limit comparison used to classify a series

Evidence tag: verified. Scope: BC_only. Primary unit: BC-UNIT-10. Units: BC-UNIT-10. Sources: sg-21:23.

**Description.** A comparison series is named or chosen, the limit of the ratio of general terms is computed with limit notation, and the conclusion is transferred to a specified series.

**Concepts and skills required.** BC-SKL-10025, BC-SKL-10026, BC-SKL-10034, BC-SKL-10035

**Prerequisites.** none recorded

**Typical wording.**
- use the limit comparison test with the given series to show that the series converges absolutely

**Common givens.**
- none recorded in this record

**What is produced.**
- none recorded in this record

**Representations.** BC-REP-11 (Series (finite partial sums or infinite)), BC-REP-01 (Symbolic (analytical) expression)

**Calculator status.** no_calculator

**Multipart structure.** Typically one part of the multipart free response question that closes Section II Part B, or a single multiple choice item.

**Scoring pattern.** Two points are typical, one for the setup with limit notation and one for the explanation; the reciprocal quotient is accepted, the explanation requires the limit to be positive, and the conclusion must name the series in question (sg-21:23).

**Scoring point types.** none recorded. Point type definitions are in [../scoring/point-taxonomy.md](../scoring/point-taxonomy.md).

**Common distractors.**
- comparing the limit with one
- omitting limit notation
- omitting absolute values when absolute convergence is the claim
- concluding about an unnamed series

**Wrong approaches.**
- none recorded in this record; see ../misconceptions/error-to-concept-map.md

**Misconceptions.** BC-MIS-10001, BC-MIS-10011, BC-MIS-10014, BC-MIS-10015

**Variants.** 3 recorded: BC-QV-10006-01, BC-QV-10006-02, BC-QV-10006-03

**Official examples notes.** 2021 Q6(b)

**Invariant structure.** Two series of positive terms are placed in a quotient whose limit is a positive finite number, and the known behaviour of the comparison series decides the other.

**Safe variables.**
- which of the two quotients is formed
- the letters in the general terms

**Difficulty variables.**
- whether absolute values are needed for an absolute convergence claim
- whether the comparison series is supplied
- whether several series are present so the conclusion must name one

Mapped difficulty factors: BC-DF-01 (Number of concepts combined)

**Expected solution path.**
- form the quotient of the general terms
- write the limit with limit notation
- evaluate and state that the limit is positive and finite
- transfer the behaviour of the comparison series, naming the series concluded about

**Prohibited shortcuts.**
- none recorded in this record

**Multi-skill extensions.**
- none recorded in this record

### BC-QA-10007 Absolute or conditional convergence classified

Evidence tag: verified. Scope: BC_only. Primary unit: BC-UNIT-10. Units: BC-UNIT-10. Sources: ced:194, sg-21:23.

**Description.** A series with mixed signs is classified as absolutely convergent, conditionally convergent, or divergent, with both tests reported.

**Concepts and skills required.** BC-SKL-10034, BC-SKL-10035, BC-SKL-10036, BC-SKL-10037, BC-SKL-10038

**Prerequisites.** none recorded

**Typical wording.**
- determine whether the series converges absolutely, converges conditionally, or diverges

**Common givens.**
- none recorded in this record

**What is produced.**
- none recorded in this record

**Representations.** BC-REP-11 (Series (finite partial sums or infinite)), BC-REP-04 (Verbal description)

**Calculator status.** no_calculator

**Multipart structure.** Typically one part of the multipart free response question that closes Section II Part B, or a single multiple choice item.

**Scoring pattern.** The explanation point requires absolute value symbols to appear, explicitly or implicitly, and requires the conclusion to specify which series is meant (sg-21:23).

**Scoring point types.** none recorded. Point type definitions are in [../scoring/point-taxonomy.md](../scoring/point-taxonomy.md).

**Common distractors.**
- swapping the two labels
- testing only one of the two series
- treating conditional convergence as a weaker absolute convergence

**Wrong approaches.**
- none recorded in this record; see ../misconceptions/error-to-concept-map.md

**Misconceptions.** BC-MIS-10015, BC-MIS-10016

**Variants.** 2 recorded: BC-QV-10007-01, BC-QV-10007-02

**Official examples notes.** 2021 Q6(b)

**Invariant structure.** Two questions are in play, the behaviour of the signed series and the behaviour of the absolute value series; the classification follows from the pair of answers.

**Safe variables.**
- the general term
- the starting index
- which test settles each of the two series

**Difficulty variables.**
- whether the absolute value series needs a separate test
- whether the series is the alternating harmonic series or a variant
- whether the prompt names the target classification

Mapped difficulty factors: BC-DF-09 (Theorem recognition)

**Expected solution path.**
- test the series of absolute values
- test the signed series if needed
- combine the two findings into one of the three classifications
- name the series in the conclusion

**Prohibited shortcuts.**
- none recorded in this record

**Multi-skill extensions.**
- none recorded in this record

## Family cross-sectional-volume [inferred]

1 archetype(s): BC-QA-08011.

### BC-QA-08011 Volume of a solid with known cross sections

Evidence tag: inferred. Scope: shared. Primary unit: BC-UNIT-08. Units: BC-UNIT-08. Sources: ced:158, ced:159, cr-24:23.

**Description.** A plane region is the base of a solid whose cross sections perpendicular to an axis are a named shape, and the response integrates the area of those sections.

**Concepts and skills required.** BC-SKL-08031, BC-SKL-08032, BC-SKL-08033, BC-SKL-08034, BC-SKL-08035, BC-SKL-08036, BC-SKL-08037, BC-SKL-08038, BC-SKL-08039

**Prerequisites.** BC-PRQ-08005, BC-PRQ-08004

**Typical wording.**
- the base of a solid is the given region and its cross sections perpendicular to the stated axis are the named shape; find the volume of the solid

**Common givens.**
- a base region
- the shape of the cross sections
- the axis they are perpendicular to

**What is produced.**
- an integrand
- the volume

**Representations.** BC-REP-08 (Geometric diagram), BC-REP-01 (Symbolic (analytical) expression), BC-REP-09 (Calculator-generated numerical result)

**Calculator status.** either

**Multipart structure.** One part of a multipart question that often opens with an area part on the same region.

**Scoring pattern.** A setup point for the integrand together with the limits and an answer point for the value; the Chief Reader records integrands taken from the wrong area or volume family as BC-ERR-99011.

**Scoring point types.** none recorded. Point type definitions are in [../scoring/point-taxonomy.md](../scoring/point-taxonomy.md).

**Common distractors.**
- an integrand carrying a factor of pi
- the area of the base region
- a semicircle area using the distance as the radius

**Wrong approaches.**
- using the full circle area for a semicircular section
- squaring the boundary functions separately

**Misconceptions.** BC-MIS-08015, BC-MIS-08018, BC-MIS-08019

**Variants.** 4 recorded: BC-QV-08011-01, BC-QV-08011-02, BC-QV-08011-03, BC-QV-08011-04

**Official examples notes.** no known cross section volume appears in the 2023 to 2025 BC free response questions

**Invariant structure.** One base region, one axis of slicing, one named shape whose area formula is applied to the distance between the boundary curves, and one integral over the spanning interval.

**Safe variables.**
- the base region
- the named shape
- the letters used

**Difficulty variables.**
- the shape of the cross section
- whether the distance is a side, a leg, a hypotenuse, or a diameter
- whether the slicing axis is x or y
- whether technology may evaluate the integral

Mapped difficulty factors: BC-DF-07 (Calculator workflow), BC-DF-17 (Case splitting at a boundary)

**Expected solution path.**
- write the distance between the boundary curves
- substitute it into the area formula of the named shape
- integrate over the spanning interval
- report the volume

**Prohibited shortcuts.**
- none recorded in this record

**Multi-skill extensions.**
- none recorded in this record

## Family de-modelling [inferred]

1 archetype(s): BC-QA-07006.

### BC-QA-07006 Differential equation written from a verbal rate statement

Evidence tag: inferred. Scope: shared. Primary unit: BC-UNIT-07. Units: BC-UNIT-07. Sources: ced:137, frq-23:7, frq-24:7.

**Description.** A situation is described in words and the response must write the differential equation and identify the initial condition.

**Concepts and skills required.** BC-SKL-07001, BC-SKL-07002, BC-SKL-07003, BC-SKL-07004, BC-SKL-07005

**Prerequisites.** BC-PRQ-07003, BC-PRQ-06005

**Typical wording.**
- write a differential equation that models the described rate of change, and state the initial condition

**Common givens.**
- a verbal description of a rate
- a value of the quantity at a stated input

**What is produced.**
- the differential equation
- the initial condition
- the meaning of each variable

**Representations.** BC-REP-04 (Verbal description), BC-REP-05 (Contextual model), BC-REP-06 (Differential equation)

**Calculator status.** either

**Multipart structure.** A single multiple choice item, or the opening of a multipart free response question.

**Scoring pattern.** Scored as the setup stage of the separable question family: the equation must carry a constant of proportionality and the correct derivative, and the initial condition is used later to fix the constant of integration (sg-23:12).

**Scoring point types.** none recorded. Point type definitions are in [../scoring/point-taxonomy.md](../scoring/point-taxonomy.md).

**Common distractors.**
- writing an equality with no constant of proportionality
- writing an equation for the quantity rather than its rate
- reversing the difference in a rate proportional to a gap
- folding the initial condition into the equation

**Wrong approaches.**
- writing an exponential formula instead of the equation

**Misconceptions.** BC-MIS-07001, BC-MIS-07002, BC-MIS-07003

**Variants.** 3 recorded: BC-QV-07006-01, BC-QV-07006-02, BC-QV-07006-03

**Official examples notes.** none in 2023 to 2025

**Invariant structure.** A proportionality word supplies a constant multiple, the derivative is of the modelled quantity with respect to the stated independent variable, and the initial condition is a separate statement.

**Safe variables.**
- the modelled quantity
- the units
- the letters used

**Difficulty variables.**
- whether the rate is proportional to the quantity or to a difference
- whether the independent variable is time
- whether an initial condition is also demanded

Mapped difficulty factors: BC-DF-14 (Missing or implicit given)

**Expected solution path.**
- name the dependent and independent variables
- translate the proportionality into a constant multiple
- write the derivative equal to that expression
- record the initial condition separately

**Prohibited shortcuts.**
- none recorded in this record

**Multi-skill extensions.**
- none recorded in this record

## Family de-qualitative-behaviour [verified]

1 archetype(s): BC-QA-07010.

### BC-QA-07010 Behaviour of a solution obtained from the differential equation itself

Evidence tag: verified. Scope: shared. Primary unit: BC-UNIT-07. Units: BC-UNIT-07. Sources: sg-24:10, frq-24:7.

**Description.** Without solving, the response must locate a critical point of a solution, classify it, or describe where the solution rises and falls.

**Concepts and skills required.** BC-SKL-07012, BC-SKL-07018

**Prerequisites.** BC-PRQ-05001, BC-PRQ-05002

**Typical wording.**
- for the stated range, find the input at which the modelled quantity has a critical point and determine whether it is the location of a relative minimum, a relative maximum, or neither

**Common givens.**
- a differential equation
- a stated bound on the quantity
- a range for the independent variable

**What is produced.**
- the sign consideration
- the critical input
- the classification

**Representations.** BC-REP-06 (Differential equation), BC-REP-01 (Symbolic (analytical) expression)

**Calculator status.** no_calculator

**Multipart structure.** One part of a multipart free response question, worth three points.

**Scoring pattern.** Three points: considering the sign of the derivative, identifying the input, and the answer with justification. A second derivative evaluation at the input is accepted as an alternate justification (sg-24:10).

**Scoring point types.** none recorded. Point type definitions are in [../scoring/point-taxonomy.md](../scoring/point-taxonomy.md).

**Common distractors.**
- setting the quantity rather than its derivative equal to zero
- ignoring the supplied bound that removes one factor
- classifying with no sign statement

**Wrong approaches.**
- solving the differential equation first

**Misconceptions.** BC-MIS-07007, BC-MIS-07010

**Variants.** 3 recorded: BC-QV-07010-01, BC-QV-07010-02, BC-QV-07010-03

**Official examples notes.** 2024 Q3(b)

**Invariant structure.** The derivative is handed over by the equation, a supplied sign fact isolates the factor that can vanish, and the classification rests on the sign of the right side on each side of the critical input.

**Safe variables.**
- the modelled context
- the letters used
- the stated range

**Difficulty variables.**
- whether a supplied bound is needed to isolate a factor
- whether the classification is by sign change or by second derivative
- how many critical inputs lie in the range

Mapped difficulty factors: BC-DF-02 (Prerequisite depth), BC-DF-12 (Sign and direction handling)

**Expected solution path.**
- set the right side equal to zero
- use the supplied bound to reduce the equation
- solve for the input inside the range
- argue the sign of the right side on each side

**Prohibited shortcuts.**
- none recorded in this record

**Multi-skill extensions.**
- none recorded in this record

## Family de-verification [inferred]

1 archetype(s): BC-QA-07007.

### BC-QA-07007 Verification that a function solves a differential equation

Evidence tag: inferred. Scope: shared. Primary unit: BC-UNIT-07. Units: BC-UNIT-07. Sources: ced:138, ced-clarifications-2026:2.

**Description.** A candidate function is offered and the response must decide whether it satisfies the equation, and sometimes the initial condition too.

**Concepts and skills required.** BC-SKL-07006, BC-SKL-07007, BC-SKL-07008, BC-SKL-07009, BC-SKL-07033

**Prerequisites.** BC-PRQ-07002

**Typical wording.**
- show that the given function is a solution to the differential equation
- which of the following functions is a solution to the given differential equation

**Common givens.**
- a differential equation
- one or more candidate functions
- sometimes an initial condition

**What is produced.**
- the derivative of the candidate
- the substitution
- a verdict

**Representations.** BC-REP-01 (Symbolic (analytical) expression), BC-REP-06 (Differential equation)

**Calculator status.** no_calculator

**Multipart structure.** A single multiple choice item, or a short free response part.

**Scoring pattern.** Scored as a demonstration: the derivative and the substitution must both be visible, and the conclusion must be stated. Scored here by analogy with the justification standards of the separable family (sg-23:12).

**Scoring point types.** none recorded. Point type definitions are in [../scoring/point-taxonomy.md](../scoring/point-taxonomy.md).

**Common distractors.**
- checking only the initial condition
- checking only that the shapes look alike
- substituting the function but not its derivative

**Wrong approaches.**
- solving the equation from scratch when a verification was asked for

**Misconceptions.** BC-MIS-07004, BC-MIS-07005

**Variants.** 3 recorded: BC-QV-07007-01, BC-QV-07007-02, BC-QV-07007-03

**Official examples notes.** none in 2023 to 2025

**Invariant structure.** The check is a differentiation followed by a substitution into both sides, and a single disagreeing input settles a negative answer.

**Safe variables.**
- the letters used
- the candidate function
- the context

**Difficulty variables.**
- whether the candidate carries an arbitrary constant
- whether an initial condition must also be checked
- whether the candidate fails only on part of the domain

Mapped difficulty factors: BC-DF-09 (Theorem recognition), BC-DF-14 (Missing or implicit given)

**Expected solution path.**
- differentiate the candidate
- substitute the candidate and its derivative into both sides
- compare
- state the verdict and check any initial condition

**Prohibited shortcuts.**
- none recorded in this record

**Multi-skill extensions.**
- none recorded in this record

## Family definite-integral-from-graph [verified]

1 archetype(s): BC-QA-06004.

### BC-QA-06004 Definite integral evaluated from a graph by geometry

Evidence tag: verified. Scope: shared. Primary unit: BC-UNIT-06. Units: BC-UNIT-06. Sources: sg-25:18, sg-24:12, ced:123.

**Description.** The graph of a function composed of line segments and circular arcs is given and the response evaluates a definite integral over a stated interval as a sum of signed areas.

**Concepts and skills required.** BC-SKL-06028, BC-SKL-06004, BC-SKL-06020

**Prerequisites.** BC-PRQ-06007

**Typical wording.**
- the graph of f consists of line segments and semicircles; evaluate the definite integral of f over the stated interval

**Common givens.**
- none recorded in this record

**What is produced.**
- none recorded in this record

**Representations.** BC-REP-02 (Graphical)

**Calculator status.** no_calculator

**Multipart structure.** Typically one part of a multipart free response question, or a single multiple choice item.

**Scoring pattern.** The value alone earns the point, with or without supporting work, but the value must be attached to the correct label when two integrals are requested in one part; incorrect linkage between the label and the value is treated as scratch work (sg-25:18).

**Scoring point types.** none recorded. Point type definitions are in [../scoring/point-taxonomy.md](../scoring/point-taxonomy.md).

**Common distractors.**
- adding the areas of regions below the axis as positive
- using the area of a full circle for a semicircular region
- using the wrong radius or base length read off the figure
- reversing the sign of the whole integral

**Wrong approaches.**
- none recorded in this record; see ../misconceptions/error-to-concept-map.md

**Misconceptions.** BC-MIS-06011, BC-MIS-06012

**Variants.** 3 recorded: BC-QV-06004-01, BC-QV-06004-02, BC-QV-06004-03

**Official examples notes.** 2025 Q4(C), 2024 Q4(a)

**Invariant structure.** The region between the graph and the horizontal axis decomposes into shapes with elementary area formulas; regions below the axis contribute negatively; no antiderivative is available or needed.

**Safe variables.**
- the shapes used
- the interval of integration
- the scale of the axes

**Difficulty variables.**
- whether any region lies below the axis
- whether a circular region appears
- whether the limits are reversed relative to the graph orientation
- whether a property of integrals must be combined with the geometry

Mapped difficulty factors: BC-DF-01 (Number of concepts combined), BC-DF-02 (Prerequisite depth), BC-DF-03 (Unusual representation), BC-DF-13 (Reversed reasoning direction), BC-DF-14 (Missing or implicit given)

**Expected solution path.**
- partition the region at the points where the graph changes character
- compute each piece with an area formula
- attach a negative sign to pieces below the axis
- add the signed contributions

**Prohibited shortcuts.**
- none recorded in this record

**Multi-skill extensions.**
- none recorded in this record

## Family derivative-definition-limit [inferred]

3 archetype(s): BC-QA-01012, BC-QA-02002, BC-QA-02003.

### BC-QA-01012 Instantaneous rate approached through average rates over shrinking intervals

Evidence tag: inferred. Scope: shared. Primary unit: BC-UNIT-01. Units: BC-UNIT-01. Sources: ced:38.

**Description.** A quantity is given by a formula or a table and the response computes average rates of change over intervals closing on a point and describes what those averages approach.

**Concepts and skills required.** BC-SKL-01001, BC-SKL-01002, BC-SKL-01003, BC-SKL-01004

**Prerequisites.** BC-PRQ-06005

**Typical wording.**
- Compute the average rate of change over each of the given intervals and describe what these values indicate about the rate at the named instant.

**Common givens.**
- none recorded in this record

**What is produced.**
- none recorded in this record

**Representations.** BC-REP-03 (Numerical table), BC-REP-05 (Contextual model), BC-REP-01 (Symbolic (analytical) expression)

**Calculator status.** either

**Multipart structure.** Typically one part of a multipart free response question.

**Scoring pattern.** One point for the average rates with supporting work and one for the description of what they approach.

**Scoring point types.** none recorded. Point type definitions are in [../scoring/point-taxonomy.md](../scoring/point-taxonomy.md).

**Common distractors.**
- reporting the difference in outputs without dividing
- using the wrong interval endpoints
- calling the last average the exact instantaneous rate
- omitting the units

**Wrong approaches.**
- none recorded in this record; see ../misconceptions/error-to-concept-map.md

**Misconceptions.** BC-MIS-01017

**Variants.** 3 recorded: BC-QV-01012-01, BC-QV-01012-02, BC-QV-01012-03

**Official examples notes.** none in 2023 to 2025 as a standalone part [inferred]

**Invariant structure.** The averages are computed over a nested family of intervals containing the point of interest, and the response must separate the average rate over an interval from the rate at the instant.

**Safe variables.**
- the modelled quantity
- the units
- the point of interest
- the widths of the intervals

**Difficulty variables.**
- whether a table or a formula is supplied
- whether units are demanded
- whether the response must state the limit form
- whether the intervals are one sided

Mapped difficulty factors: BC-DF-03 (Unusual representation), BC-DF-10 (Required justification), BC-DF-16 (Units and labelling demand)

**Expected solution path.**
- compute the average rate over each interval
- record the sequence of values
- state the value the averages approach
- name that value as the instantaneous rate at the point

**Prohibited shortcuts.**
- none recorded in this record

**Multi-skill extensions.**
- none recorded in this record

### BC-QA-02002 Derivative computed from the limit definition

Evidence tag: inferred. Scope: shared. Primary unit: BC-UNIT-02. Units: BC-UNIT-02. Sources: ced:61, ced:64.

**Description.** A rule is given and the response produces the derivative by setting up and evaluating the limit of a difference quotient rather than by a rule.

**Concepts and skills required.** BC-SKL-02006, BC-SKL-02007, BC-SKL-02008, BC-SKL-02009, BC-SKL-02027

**Prerequisites.** BC-PRQ-02001, BC-PRQ-02005

**Typical wording.**
- Use the definition of the derivative to find the derivative of the given function, or its value at the named input.

**Common givens.**
- none recorded in this record

**What is produced.**
- none recorded in this record

**Representations.** BC-REP-01 (Symbolic (analytical) expression)

**Calculator status.** no_calculator

**Multipart structure.** Typically a single multiple choice item or one part of a larger question.

**Scoring pattern.** One point for a correct difference quotient inside a limit, one for the simplification, and one for the value. No free response part in 2023 to 2025 asks for a derivative from the definition, so the pattern is drawn from the CED description of the topic.

**Scoring point types.** none recorded. Point type definitions are in [../scoring/point-taxonomy.md](../scoring/point-taxonomy.md).

**Common distractors.**
- setting the increment to zero before cancelling
- omitting the limit symbol until the final line
- expanding the shifted term incorrectly
- differentiating by rule and presenting the result as the definition

**Wrong approaches.**
- none recorded in this record; see ../misconceptions/error-to-concept-map.md

**Misconceptions.** BC-MIS-02002, BC-MIS-02003

**Variants.** 4 recorded: BC-QV-02002-01, BC-QV-02002-02, BC-QV-02002-03, BC-QV-02002-04

**Official examples notes.** none in 2023 to 2025 [inferred]

**Invariant structure.** The difference quotient is indeterminate at zero increment, so the increment must be divided out of the numerator before the limit can be taken, and the final step is a substitution into the simplified quotient.

**Safe variables.**
- the rule
- the base point or the general input
- the variable name
- which of the two forms is demanded

**Difficulty variables.**
- polynomial against radical against rational rule
- derivative at a point against derivative function
- increment form against two point form
- whether the setup alone or the value is demanded

Mapped difficulty factors: BC-DF-02 (Prerequisite depth)

**Expected solution path.**
- write the difference quotient for the given rule
- expand and simplify the numerator
- divide out the increment
- evaluate the limit by substitution

**Prohibited shortcuts.**
- none recorded in this record

**Multi-skill extensions.**
- none recorded in this record

### BC-QA-02003 Limit recognised as a derivative of a known function

Evidence tag: inferred. Scope: shared. Primary unit: BC-UNIT-02. Units: BC-UNIT-02. Sources: ced:66.

**Description.** A limit in difference quotient form is presented and the response evaluates it by identifying the underlying function and base point.

**Concepts and skills required.** BC-SKL-02035, BC-SKL-02005

**Prerequisites.** BC-PRQ-02005

**Typical wording.**
- Evaluate the given limit.

**Common givens.**
- none recorded in this record

**What is produced.**
- none recorded in this record

**Representations.** BC-REP-01 (Symbolic (analytical) expression)

**Calculator status.** no_calculator

**Multipart structure.** Typically a single multiple choice item.

**Scoring pattern.** One point for the value, with the identification expected in a justified response. No free response part in 2023 to 2025 assesses this task in isolation.

**Scoring point types.** none recorded. Point type definitions are in [../scoring/point-taxonomy.md](../scoring/point-taxonomy.md).

**Common distractors.**
- applying a rewriting technique that does not resolve the form
- identifying the wrong base point
- reporting the value of the function rather than of its derivative
- concluding that the limit does not exist

**Wrong approaches.**
- none recorded in this record; see ../misconceptions/error-to-concept-map.md

**Misconceptions.** BC-MIS-02004

**Variants.** 3 recorded: BC-QV-02003-01, BC-QV-02003-02, BC-QV-02003-03

**Official examples notes.** none in 2023 to 2025 [inferred]

**Invariant structure.** The limit cannot be evaluated by substitution, and the numerator is the difference of the values of a known function at a shifted and a base input, so the answer is a derivative value already available from a rule.

**Safe variables.**
- the underlying function
- the base point
- the variable used for the increment

**Difficulty variables.**
- whether the base point is a standard angle or value
- whether the two point form is used
- whether the underlying function is transcendental
- whether the response must name the function

Mapped difficulty factors: BC-DF-01 (Number of concepts combined)

**Expected solution path.**
- compare the numerator with a difference of function values
- identify the function and the base point
- state the limit as the derivative of that function at that point
- evaluate using the derivative rule

**Prohibited shortcuts.**
- none recorded in this record

**Multi-skill extensions.**
- none recorded in this record

## Family derivative-from-graph [inferred]

1 archetype(s): BC-QA-03003.

### BC-QA-03003 Composite derivative read from graphs of the component functions

Evidence tag: inferred. Scope: shared. Primary unit: BC-UNIT-03. Units: BC-UNIT-03. Sources: ced:75, ced:72.

**Description.** Graphs of two functions are supplied and the response evaluates the derivative of their composite at a stated input by reading values and slopes off the figures.

**Concepts and skills required.** BC-SKL-03005

**Prerequisites.** BC-PRQ-03001, BC-PRQ-03005

**Typical wording.**
- use the graphs shown to find the derivative of the composite function at the stated input

**Common givens.**
- none recorded in this record

**What is produced.**
- none recorded in this record

**Representations.** BC-REP-02 (Graphical), BC-REP-01 (Symbolic (analytical) expression)

**Calculator status.** no_calculator

**Multipart structure.** A single multiple choice item.

**Scoring pattern.** Scored as an answer point; a response that reads a slope where the graph is not differentiable does not earn it.

**Scoring point types.** none recorded. Point type definitions are in [../scoring/point-taxonomy.md](../scoring/point-taxonomy.md).

**Common distractors.**
- the slope of the outer graph read at the input rather than at the inner output
- the product of the two function values
- a slope read at a point where the graph has a corner

**Wrong approaches.**
- none recorded in this record; see ../misconceptions/error-to-concept-map.md

**Misconceptions.** BC-MIS-03002

**Variants.** 2 recorded: BC-QV-03003-01, BC-QV-03003-02

**Official examples notes.** none in the 2023 to 2025 BC free response questions read for this unit

**Invariant structure.** The graphs are piecewise linear or otherwise readable; the chain rule product is built from one function value and two slopes, each read at the input the rule names.

**Safe variables.**
- the shapes of the graphs
- the labelled grid values
- the function names

**Difficulty variables.**
- whether a slope must be read at a corner
- whether the inner output lands between labelled grid values
- whether the composite is combined with a product

Mapped difficulty factors: BC-DF-01 (Number of concepts combined), BC-DF-14 (Missing or implicit given), BC-DF-16 (Units and labelling demand)

**Expected solution path.**
- read the inner function value at the given input
- read the slope of the outer graph at that value
- read the slope of the inner graph at the given input
- multiply the two slopes

**Prohibited shortcuts.**
- none recorded in this record

**Multi-skill extensions.**
- none recorded in this record

## Family derivative-from-table [verified]

3 archetype(s): BC-QA-02009, BC-QA-03002, BC-QA-04002.

### BC-QA-02009 Derivative of a product or quotient evaluated from supplied values

Evidence tag: inferred. Scope: shared. Primary unit: BC-UNIT-02. Units: BC-UNIT-02. Sources: ced:67, ced:68.

**Description.** The values of two functions and of their derivatives at an input are supplied in a table or read from graphs and the response evaluates the derivative of their product or quotient there.

**Concepts and skills required.** BC-SKL-02037, BC-SKL-02041, BC-SKL-02017

**Prerequisites.** BC-PRQ-06005

**Typical wording.**
- The table gives values of f, g, and their derivatives at selected inputs. Find the derivative of the indicated product or quotient at the named input.

**Common givens.**
- none recorded in this record

**What is produced.**
- none recorded in this record

**Representations.** BC-REP-03 (Numerical table), BC-REP-02 (Graphical)

**Calculator status.** no_calculator

**Multipart structure.** Typically a single multiple choice item.

**Scoring pattern.** One point for the rule with the supplied values correctly placed and one for the value.

**Scoring point types.** none recorded. Point type definitions are in [../scoring/point-taxonomy.md](../scoring/point-taxonomy.md).

**Common distractors.**
- reading a value of the function where a value of the derivative is needed
- swapping the two functions in the rule
- using the wrong row of the table
- omitting the denominator square

**Wrong approaches.**
- none recorded in this record; see ../misconceptions/error-to-concept-map.md

**Misconceptions.** BC-MIS-02011

**Variants.** 3 recorded: BC-QV-02009-01, BC-QV-02009-02, BC-QV-02009-03

**Official examples notes.** none in 2023 to 2025 as a standalone part [inferred]

**Invariant structure.** No formula for either function is given, so the response must place four supplied numbers into the correct positions of the rule and evaluate.

**Safe variables.**
- the function names
- the supplied values
- the input at which the derivative is requested

**Difficulty variables.**
- table against graphs
- product against quotient
- whether one of the supplied values must itself be read as a slope
- whether the answer must be interpreted in context

Mapped difficulty factors: BC-DF-03 (Unusual representation), BC-DF-05 (Contextual interpretation)

**Expected solution path.**
- record the four supplied values at the named input
- write the product or quotient rule with the names in place
- substitute the values
- evaluate and report

**Prohibited shortcuts.**
- none recorded in this record

**Multi-skill extensions.**
- none recorded in this record

### BC-QA-03002 Composite derivative evaluated from a table of values

Evidence tag: inferred. Scope: shared. Primary unit: BC-UNIT-03. Units: BC-UNIT-03. Sources: ced:75, ced:72, sg-24:2, sg-25:11.

**Description.** A table gives values of two functions and their derivatives at selected inputs, and the response evaluates the derivative of a composite or of a combination at one input.

**Concepts and skills required.** BC-SKL-03004, BC-SKL-03006

**Prerequisites.** BC-PRQ-03001, BC-PRQ-03005

**Typical wording.**
- use the table of values to find the derivative of the composite function at the stated input

**Common givens.**
- none recorded in this record

**What is produced.**
- none recorded in this record

**Representations.** BC-REP-03 (Numerical table), BC-REP-01 (Symbolic (analytical) expression)

**Calculator status.** either

**Multipart structure.** A single multiple choice item, or one part of a table based free response question.

**Scoring pattern.** In a free response setting the value alone without a visible assembly of the chain rule factors does not communicate the method; the analogous table based parts in 2024 and 2025 award a point for supporting work of a difference and a quotient and a separate point for the value (sg-24:2, sg-25:11).

**Scoring point types.** none recorded. Point type definitions are in [../scoring/point-taxonomy.md](../scoring/point-taxonomy.md).

**Common distractors.**
- f prime and g prime evaluated at the same input and multiplied
- the outer derivative read at the input rather than at the inner output
- the sum of the two derivatives
- the value of the composite rather than of its derivative

**Wrong approaches.**
- none recorded in this record; see ../misconceptions/error-to-concept-map.md

**Misconceptions.** BC-MIS-03002

**Variants.** 3 recorded: BC-QV-03002-01, BC-QV-03002-02, BC-QV-03002-03

**Official examples notes.** none in the 2023 to 2025 BC free response questions read for this unit

**Invariant structure.** Values of f, f prime, g, and g prime appear at a small set of inputs; the requested derivative is assembled from exactly the entries the chain rule names, and the inner output must be looked up before the outer derivative.

**Safe variables.**
- the function names
- the inputs listed
- the numerical entries
- the context, if any

**Difficulty variables.**
- whether the composite is nested inside a product or quotient
- whether the needed inner output is itself in the table
- whether a distractor row matches the input rather than the output
- how many table rows are supplied

Mapped difficulty factors: BC-DF-03 (Unusual representation), BC-DF-13 (Reversed reasoning direction)

**Expected solution path.**
- evaluate the inner function at the given input
- locate the outer derivative at that output
- evaluate the inner derivative at the given input
- multiply the two
- report the numerical value

**Prohibited shortcuts.**
- none recorded in this record

**Multi-skill extensions.**
- none recorded in this record

### BC-QA-04002 Approximating a derivative from a table with units

Evidence tag: verified. Scope: shared. Primary unit: BC-UNIT-04. Units: BC-UNIT-04, BC-UNIT-02. Sources: sg-24:2, sg-25:11, ced:62.

**Description.** A quantity is tabulated at selected inputs and the response approximates the derivative at an interior input using an average rate of change over an interval the prompt names.

**Concepts and skills required.** BC-SKL-04004, BC-SKL-04001, BC-SKL-02014, BC-SKL-02015, BC-SKL-02016, BC-SKL-02002, BC-SKL-02003

**Prerequisites.** BC-PRQ-04004, BC-PRQ-06005, BC-PRQ-02003

**Typical wording.**
- approximate the derivative at the stated input using the average rate of change over the named interval; show the work and indicate units of measure
- Approximate the derivative at the named input using the average rate of change over the given interval. Show the work that leads to your answer and indicate units of measure.

**Common givens.**
- none recorded in this record

**What is produced.**
- none recorded in this record

**Representations.** BC-REP-03 (Numerical table), BC-REP-05 (Contextual model)

**Calculator status.** either

**Multipart structure.** The opening part of a table based contextual free response question.

**Scoring pattern.** Scored as one point for the answer with supporting work of a difference and a quotient using values from the table, and a separate point for the units; the setup expression alone without a value does not earn the first point, and the units point is earned whether or not the units are attached to a number (sg-25:11, sg-24:2).

**Scoring point types.** none recorded. Point type definitions are in [../scoring/point-taxonomy.md](../scoring/point-taxonomy.md).

**Common distractors.**
- the quotient written without the difference
- the two values subtracted in the wrong order
- the interval taken from the wrong pair of rows
- the units given as those of the quantity alone
- reporting the difference of the values without dividing
- using rows that do not bracket the point
- inverting the quotient
- omitting the units
- giving the units of the quantity rather than of its rate

**Wrong approaches.**
- none recorded in this record; see ../misconceptions/error-to-concept-map.md

**Misconceptions.** BC-MIS-04003, BC-MIS-02001, BC-MIS-02008

**Variants.** 3 recorded: BC-QV-04002-01, BC-QV-04002-02, BC-QV-04002-03

**Official examples notes.** 2024 Q1(a), 2025 Q3(A); 2025 Q3(A), 2024 Q1(a)

**Invariant structure.** The approximation is a difference of two tabulated values divided by the difference of the corresponding inputs; both the difference and the quotient must be visible, and the units are those of the quantity divided by those of the input.

**Safe variables.**
- the quantity
- its units
- the tabulated values
- the interval named in the prompt
- the modelled quantity
- the units
- the tabulated inputs
- the point of interest

**Difficulty variables.**
- whether the interval is centred on the point
- whether the units are compound as in a rate of a rate
- whether the table is decreasing
- calculator or no calculator
- whether the interval is named or must be chosen
- whether the point lies inside the interval or at an end
- whether the table is evenly spaced
- whether the units carry their own point

Mapped difficulty factors: BC-DF-03 (Unusual representation), BC-DF-07 (Calculator workflow), BC-DF-09 (Theorem recognition), BC-DF-12 (Sign and direction handling), BC-DF-14 (Missing or implicit given), BC-DF-16 (Units and labelling demand)

**Expected solution path.**
- select the two tabulated values the named interval determines
- form the difference of the values and the difference of the inputs
- divide
- attach the units
- identify the two tabulated inputs the estimate uses
- compute the difference of the function values
- divide by the difference of the inputs
- report the value and attach the units

**Prohibited shortcuts.**
- none recorded in this record

**Multi-skill extensions.**
- none recorded in this record

## Family derivative-in-context [verified]

2 archetype(s): BC-QA-04001, BC-QA-04005.

### BC-QA-04001 Interpreting the value of a derivative in context with units

Evidence tag: verified. Scope: shared. Primary unit: BC-UNIT-04. Units: BC-UNIT-04. Sources: ced:87, sg-24:2, sg-25:11, cr-24:3, cr-24:4.

**Description.** A modelled quantity and a numerical rate are supplied and the response writes what that rate means in the situation, with units.

**Concepts and skills required.** BC-SKL-04001, BC-SKL-04002, BC-SKL-04003, BC-SKL-04005

**Prerequisites.** BC-PRQ-04004, BC-PRQ-04008

**Typical wording.**
- using correct units, interpret the meaning of the stated value in the context of the problem

**Common givens.**
- none recorded in this record

**What is produced.**
- none recorded in this record

**Representations.** BC-REP-04 (Verbal description), BC-REP-05 (Contextual model)

**Calculator status.** either

**Multipart structure.** One part of a multipart contextual free response question, often sharing the part with a numerical computation.

**Scoring pattern.** The units carry their own scoring point in the 2024 and 2025 table based questions, awarded whether or not they are attached to a numerical value (sg-24:2, sg-25:11); the Chief Reader reports record incomplete interpretations and missing or malformed units as recurring losses (BC-ERR-99005, BC-ERR-99027).

**Scoring point types.** none recorded. Point type definitions are in [../scoring/point-taxonomy.md](../scoring/point-taxonomy.md).

**Common distractors.**
- an interpretation of the amount rather than of the rate
- units inverted
- the interval or instant omitted
- a restatement of the notation with no reference to the situation

**Wrong approaches.**
- none recorded in this record; see ../misconceptions/error-to-concept-map.md

**Misconceptions.** BC-MIS-04001, BC-MIS-04002, BC-MIS-04003

**Variants.** 3 recorded: BC-QV-04001-01, BC-QV-04001-02, BC-QV-04001-03

**Official examples notes.** 2024 Q1(a), 2025 Q3(A)

**Invariant structure.** The interpretation must name the quantity, the instant or the interval, the direction of change, and the units; the units are the units of the quantity divided by the units of the independent variable.

**Safe variables.**
- the quantity modelled
- the units of the quantity
- the letters naming the function and the variable
- the instant chosen

**Difficulty variables.**
- whether the interpretation shares a part with a computation
- whether the rate is negative
- whether a second derivative is the subject
- whether the units are compound

Mapped difficulty factors: BC-DF-01 (Number of concepts combined), BC-DF-05 (Contextual interpretation), BC-DF-12 (Sign and direction handling), BC-DF-16 (Units and labelling demand)

**Expected solution path.**
- name the quantity and the instant
- state whether the quantity is increasing or decreasing
- attach the units as quantity units per independent variable unit
- keep the sentence about the rate rather than about the amount

**Prohibited shortcuts.**
- none recorded in this record

**Multi-skill extensions.**
- none recorded in this record

### BC-QA-04005 Contextual rate in a setting other than motion

Evidence tag: verified. Scope: shared. Primary unit: BC-UNIT-04. Units: BC-UNIT-04. Sources: ced:89, ced:84, sg-25:2, sg-25:4, sg-24:2.

**Description.** A quantity such as a temperature, a population, an affected area, or a reading rate is modelled, and the response computes or interprets its rate of change, sometimes including the end behaviour of that rate.

**Concepts and skills required.** BC-SKL-04013, BC-SKL-04014, BC-SKL-04015, BC-SKL-04016

**Prerequisites.** BC-PRQ-04004, BC-PRQ-04008

**Typical wording.**
- find the time at which the instantaneous rate of change equals the average rate of change over the stated interval
- write a limit expression that describes the end behaviour of the rate of change and evaluate it

**Common givens.**
- none recorded in this record

**What is produced.**
- none recorded in this record

**Representations.** BC-REP-05 (Contextual model), BC-REP-01 (Symbolic (analytical) expression), BC-REP-09 (Calculator-generated numerical result)

**Calculator status.** calculator

**Multipart structure.** A multipart calculator active free response question built on one contextual model.

**Scoring pattern.** The 2025 rubric awards a point for using the average rate of change and a point for the answer supported by the appropriate equation, and separately a point for the limit expression and a point for its value, with arithmetic involving infinity treated as scratch work that cannot earn the value point (sg-25:4).

**Scoring point types.** none recorded. Point type definitions are in [../scoring/point-taxonomy.md](../scoring/point-taxonomy.md).

**Common distractors.**
- a value of the model reported where a rate was requested
- motion vocabulary used for a non-motion quantity
- arithmetic performed with infinity in place of a limit expression
- an inappropriately rounded decimal answer

**Wrong approaches.**
- none recorded in this record; see ../misconceptions/error-to-concept-map.md

**Misconceptions.** BC-MIS-04007, BC-MIS-04001, BC-MIS-04014

**Variants.** 3 recorded: BC-QV-04005-01, BC-QV-04005-02, BC-QV-04005-03

**Official examples notes.** 2025 Q1 parts B and C, 2024 Q1(a)

**Invariant structure.** The context supplies the quantity and the independent variable; the mathematics is the same as for motion but the language must be the language of the context, and every reported rate carries its own units.

**Safe variables.**
- the modelled quantity
- the units
- the letters naming the model
- the instant or interval

**Difficulty variables.**
- whether the rate expression is supplied in the stem
- whether an end behaviour limit is requested
- whether an average value or average rate of change must be compared with an instantaneous rate
- whether the answer must be reported to three decimal places

Mapped difficulty factors: BC-DF-07 (Calculator workflow)

**Expected solution path.**
- identify the quantity and its independent variable
- differentiate the model or use the derivative supplied in the stem
- evaluate at the requested input
- report the value with units and in the vocabulary of the context
- write and evaluate a limit expression when end behaviour is requested

**Prohibited shortcuts.**
- none recorded in this record

**Multi-skill extensions.**
- none recorded in this record

## Family differentiability-and-continuity [verified]

2 archetype(s): BC-QA-02004, BC-QA-02005.

### BC-QA-02004 Continuity deduced from differentiability inside a larger argument

Evidence tag: verified. Scope: shared. Primary unit: BC-UNIT-02. Units: BC-UNIT-02. Sources: ced:63, sg-25:12, sg-23:14.

**Description.** A function is stated to be differentiable and the response establishes that it is continuous in order to use a theorem that requires continuity.

**Concepts and skills required.** BC-SKL-02019, BC-SKL-02020, BC-SKL-02024

**Prerequisites.** BC-PRQ-06005

**Typical wording.**
- Justify the conclusion, stating any property of the function that your argument relies on.

**Common givens.**
- none recorded in this record

**What is produced.**
- none recorded in this record

**Representations.** BC-REP-04 (Verbal description), BC-REP-03 (Numerical table), BC-REP-05 (Contextual model)

**Calculator status.** no_calculator

**Multipart structure.** Typically one part of a multipart free response question.

**Scoring pattern.** A point is earned for stating that the function is continuous because it is differentiable or the equivalent, and a response that states only that the function is continuous does not earn it; the following point does not depend on earning it (sg-25:12). A 2023 part uses the same implication at a point before evaluating a limit (sg-23:14).

**Scoring point types.** none recorded. Point type definitions are in [../scoring/point-taxonomy.md](../scoring/point-taxonomy.md).

**Common distractors.**
- asserting continuity with no reason
- reversing the implication and claiming differentiability from continuity
- citing differentiability of the wrong function
- omitting the step entirely

**Wrong approaches.**
- none recorded in this record; see ../misconceptions/error-to-concept-map.md

**Misconceptions.** BC-MIS-02005, BC-MIS-02006

**Variants.** 3 recorded: BC-QV-02004-01, BC-QV-02004-02, BC-QV-02004-03

**Official examples notes.** 2025 Q3(B), 2023 Q4(c)

**Invariant structure.** The differentiability statement appears in the stem rather than in the part, and the continuity conclusion is a step towards an existence or evaluation argument rather than the answer itself.

**Safe variables.**
- the modelled quantity
- the interval
- the theorem the continuity feeds

**Difficulty variables.**
- whether the continuity claim carries its own point
- whether the function is given by a table or a rule
- whether the argument continues to an existence conclusion or to a limit evaluation
- whether the implication must be stated in general terms

Mapped difficulty factors: BC-DF-03 (Unusual representation), BC-DF-04 (Notation complexity), BC-DF-10 (Required justification)

**Expected solution path.**
- read the differentiability statement from the stem
- state that the function is therefore continuous
- use the continuity as the hypothesis of the theorem or the limit step
- complete the argument

**Prohibited shortcuts.**
- none recorded in this record

**Multi-skill extensions.**
- none recorded in this record

### BC-QA-02005 Point of non-differentiability identified on a continuous function

Evidence tag: inferred. Scope: shared. Primary unit: BC-UNIT-02. Units: BC-UNIT-02. Sources: ced:63.

**Description.** A function continuous at a point is presented and the response determines whether the derivative exists there and gives a reason.

**Concepts and skills required.** BC-SKL-02021, BC-SKL-02022, BC-SKL-02023

**Prerequisites.** BC-PRQ-02001, BC-PRQ-01006

**Typical wording.**
- Is the given function differentiable at the named input? Give a reason for your answer.

**Common givens.**
- none recorded in this record

**What is produced.**
- none recorded in this record

**Representations.** BC-REP-01 (Symbolic (analytical) expression), BC-REP-02 (Graphical)

**Calculator status.** no_calculator

**Multipart structure.** Typically a single multiple choice item or one part of a larger question.

**Scoring pattern.** One point for the verdict and one for the reason, where the reason must refer to the one sided behaviour of the difference quotient or to the tangent line rather than to the appearance of the graph alone.

**Scoring point types.** none recorded. Point type definitions are in [../scoring/point-taxonomy.md](../scoring/point-taxonomy.md).

**Common distractors.**
- concluding differentiability from continuity
- concluding non-differentiability from the shape without the slopes
- reporting one of the two one sided slopes as the derivative
- treating a vertical tangent as a slope of zero

**Wrong approaches.**
- none recorded in this record; see ../misconceptions/error-to-concept-map.md

**Misconceptions.** BC-MIS-02006, BC-MIS-02007

**Variants.** 3 recorded: BC-QV-02005-01, BC-QV-02005-02, BC-QV-02005-03

**Official examples notes.** none in 2023 to 2025 as a standalone part [inferred]

**Invariant structure.** The function is continuous at the point in question, so the verdict turns on the behaviour of the difference quotient rather than on the existence of the function value or the limit.

**Safe variables.**
- the rule or the shape of the graph
- the input in question
- the variable name

**Difficulty variables.**
- corner against cusp against vertical tangent
- rule against graph
- whether a reason is demanded
- whether the point is also a boundary of a piecewise rule

Mapped difficulty factors: BC-DF-03 (Unusual representation), BC-DF-10 (Required justification), BC-DF-17 (Case splitting at a boundary)

**Expected solution path.**
- confirm that the function is continuous at the input
- evaluate the one sided limits of the difference quotient, or read the one sided slopes from the graph
- compare them
- state whether the derivative exists and name the reason

**Prohibited shortcuts.**
- none recorded in this record

**Multi-skill extensions.**
- none recorded in this record

## Family discontinuity-classification [inferred]

1 archetype(s): BC-QA-01007.

### BC-QA-01007 Discontinuity classified from a rule or a graph

Evidence tag: inferred. Scope: shared. Primary unit: BC-UNIT-01. Units: BC-UNIT-01. Sources: ced:47.

**Description.** A function with one or more breaks is presented and the response classifies each break as removable, a jump, or due to a vertical asymptote.

**Concepts and skills required.** BC-SKL-01039, BC-SKL-01040, BC-SKL-01041, BC-SKL-01057

**Prerequisites.** BC-PRQ-01001, BC-PRQ-01006

**Typical wording.**
- Classify each discontinuity of the given function and give a reason for each classification.

**Common givens.**
- none recorded in this record

**What is produced.**
- none recorded in this record

**Representations.** BC-REP-01 (Symbolic (analytical) expression), BC-REP-02 (Graphical)

**Calculator status.** no_calculator

**Multipart structure.** Typically a single multiple choice item.

**Scoring pattern.** One point per classification with a reason point when justification is demanded.

**Scoring point types.** none recorded. Point type definitions are in [../scoring/point-taxonomy.md](../scoring/point-taxonomy.md).

**Common distractors.**
- classifying a cancelling factor as a vertical asymptote
- calling a removable break a jump because the value is missing
- treating any undefined point as an asymptote
- classifying from the function value rather than the limits

**Wrong approaches.**
- none recorded in this record; see ../misconceptions/error-to-concept-map.md

**Misconceptions.** BC-MIS-01011

**Variants.** 3 recorded: BC-QV-01007-01, BC-QV-01007-02, BC-QV-01007-03

**Official examples notes.** none in 2023 to 2025 [inferred]

**Invariant structure.** Every break admits exactly one classification determined by the existence and finiteness of the one sided limits, and the classification does not depend on the function value.

**Safe variables.**
- the expression or the shape of the graph
- the inputs where breaks occur
- the number of breaks

**Difficulty variables.**
- whether a cancelling factor is present
- whether an absolute value produces the jump
- whether the graph or the rule is given
- whether the classification must be justified

Mapped difficulty factors: BC-DF-02 (Prerequisite depth), BC-DF-03 (Unusual representation), BC-DF-10 (Required justification)

**Expected solution path.**
- locate the inputs where the function is undefined or the rule changes
- evaluate the one sided limits at each such input
- classify from whether the one sided limits exist, agree, and are finite

**Prohibited shortcuts.**
- none recorded in this record

**Multi-skill extensions.**
- none recorded in this record

## Family end-behaviour-limit [verified]

1 archetype(s): BC-QA-01010.

### BC-QA-01010 End behaviour described by a limit at infinity

Evidence tag: verified. Scope: shared. Primary unit: BC-UNIT-01. Units: BC-UNIT-01. Sources: ced:52, sg-25:4.

**Description.** A function or a contextual model is given and the response writes the limit expression describing behaviour for inputs of large magnitude and evaluates it.

**Concepts and skills required.** BC-SKL-01058, BC-SKL-01059, BC-SKL-01060, BC-SKL-01061, BC-SKL-01063, BC-SKL-01062

**Prerequisites.** BC-PRQ-01004, BC-PRQ-06005

**Typical wording.**
- Write a limit expression that describes the long run behaviour of the given quantity and evaluate it.

**Common givens.**
- none recorded in this record

**What is produced.**
- none recorded in this record

**Representations.** BC-REP-01 (Symbolic (analytical) expression), BC-REP-05 (Contextual model), BC-REP-02 (Graphical)

**Calculator status.** either

**Multipart structure.** Typically one part of a multipart free response question.

**Scoring pattern.** A separate point is awarded for the limit expression and another for its value; the expression point may be earned by the limit of either the amount or its rate, while a response presenting the limit of the amount is not eligible for the value point, and arithmetic performed with the infinity symbol is treated as scratch work (sg-25:4).

**Scoring point types.** none recorded. Point type definitions are in [../scoring/point-taxonomy.md](../scoring/point-taxonomy.md).

**Common distractors.**
- writing the limit of the amount when the rate was requested
- substituting infinity into the expression as though it were a number
- reporting the limit of the rate as the limit of the amount
- omitting the limit expression and giving only a value

**Wrong approaches.**
- none recorded in this record; see ../misconceptions/error-to-concept-map.md

**Misconceptions.** BC-MIS-01013, BC-MIS-01014

**Variants.** 4 recorded: BC-QV-01010-01, BC-QV-01010-02, BC-QV-01010-03, BC-QV-01010-04

**Official examples notes.** 2025 Q2(C)

**Invariant structure.** The response must produce the limit expression itself as well as its value, and the expression must name the correct function, which in a contextual setting may be the rate rather than the amount.

**Safe variables.**
- the modelled quantity
- the variable name
- the algebraic form of the model

**Difficulty variables.**
- whether the expression as well as the value is demanded
- whether the rate or the amount is the subject
- whether the two ends differ
- whether a radical is present
- whether the setting is contextual

Mapped difficulty factors: BC-DF-05 (Contextual interpretation), BC-DF-11 (Unfamiliar surface presentation)

**Expected solution path.**
- identify the function whose end behaviour is requested
- write the limit expression as the variable increases without bound
- divide by the dominant power or compare degrees
- report the value

**Prohibited shortcuts.**
- none recorded in this record

**Multi-skill extensions.**
- none recorded in this record

## Family euler [verified]

2 archetype(s): BC-QA-07004, BC-QA-07005.

### BC-QA-07004 Euler's method over two steps of equal size

Evidence tag: verified. Scope: BC_only. Primary unit: BC-UNIT-07. Units: BC-UNIT-07. Sources: sg-24:17, sg-25:23, frq-24:9, frq-25:8.

**Description.** A differential equation and an initial point are given and the response must approximate the solution at a stated input using a named number of equal steps.

**Concepts and skills required.** BC-SKL-07019, BC-SKL-07020, BC-SKL-07021, BC-SKL-07022, BC-SKL-07023

**Prerequisites.** BC-PRQ-07005, BC-PRQ-07006

**Typical wording.**
- use Euler's method, starting at the given input with two steps of equal size, to approximate the value of the solution at the stated input; show the computations that lead to the answer

**Common givens.**
- a differential equation
- an initial condition
- a target input
- a number of equal steps

**What is produced.**
- the step size
- each step's increment
- the approximation

**Representations.** BC-REP-03 (Numerical table), BC-REP-06 (Differential equation), BC-REP-01 (Symbolic (analytical) expression)

**Calculator status.** no_calculator

**Multipart structure.** One part of a multipart free response question, worth two points.

**Scoring pattern.** Two points: one for the demonstration and one for the answer with supporting work. The 2024 guideline required two demonstrated steps with the correct derivative expression and at most one error, and withheld the answer point when there was an error, while requiring an incorrect first approximation to be imported into the second step. The 2025 guideline required only the first step, with the correct initial condition, step size, and derivative expression, and discounted later simplification or rounding errors for that point. Both accept a labelled table, and both allow an incorrect value imported from an earlier part to earn the answer point with a consistent result (sg-24:17, sg-25:23).

**Scoring point types.** none recorded. Point type definitions are in [../scoring/point-taxonomy.md](../scoring/point-taxonomy.md).

**Common distractors.**
- restarting the second step from the initial point
- using the whole interval as the step size
- evaluating the derivative at the target input
- reporting a value with no visible steps

**Wrong approaches.**
- solving the differential equation and evaluating the solution

**Misconceptions.** BC-MIS-07011, BC-MIS-07012, BC-MIS-07013

**Variants.** 3 recorded: BC-QV-07004-01, BC-QV-07004-02, BC-QV-07004-03

**Official examples notes.** 2024 Q5(c), 2025 Q5(D)

**Invariant structure.** The step size is the interval divided by the number of steps, the derivative is evaluated afresh at each new approximation, and the work must be visible as expressions or as a labelled table.

**Safe variables.**
- the letters used
- the initial values
- the context

**Difficulty variables.**
- whether the derivative expression depends on both variables
- whether the derivative expression is imported from an earlier part
- how many steps are asked for
- whether a direction of error is also demanded

Mapped difficulty factors: BC-DF-01 (Number of concepts combined), BC-DF-08 (Multi-step dependency), BC-DF-12 (Sign and direction handling)

**Expected solution path.**
- compute the step size
- evaluate the derivative at the initial point and advance
- evaluate the derivative at the new point and advance again
- report the approximation with the steps shown

**Prohibited shortcuts.**
- none recorded in this record

**Multi-skill extensions.**
- none recorded in this record

### BC-QA-07005 Direction of an approximation decided from the second derivative of a solution

Evidence tag: verified. Scope: shared. Primary unit: BC-UNIT-07. Units: BC-UNIT-07. Sources: sg-23:10, sg-23:11, frq-23:7.

**Description.** A tangent line or Euler approximation to a solution has been produced and the response must say whether it is an overestimate or an underestimate, with a reason.

**Concepts and skills required.** BC-SKL-07018, BC-SKL-07023

**Prerequisites.** BC-PRQ-07002

**Typical wording.**
- is the approximation an overestimate or an underestimate of the value of the solution, and give a reason for the answer

**Common givens.**
- a differential equation
- an approximation already computed
- sometimes a stated range for the quantity

**What is produced.**
- the second derivative expression
- its sign on the interval
- the direction with a reason

**Representations.** BC-REP-01 (Symbolic (analytical) expression), BC-REP-06 (Differential equation)

**Calculator status.** no_calculator

**Multipart structure.** One part of a multipart free response question, worth two points.

**Scoring pattern.** One point for the second derivative expressed in terms of the dependent variable, one for the direction with the reason. An expression left in terms of the first derivative does not earn the first point but stays eligible for the second. The reason must state that the second derivative is negative, or that the first derivative is decreasing, or that the graph is concave down, and must reach the conclusion; an argument resting on the second derivative at a single point does not earn the point (sg-23:11).

**Scoring point types.** none recorded. Point type definitions are in [../scoring/point-taxonomy.md](../scoring/point-taxonomy.md).

**Common distractors.**
- arguing from whether the solution is increasing or decreasing
- evaluating the second derivative at one point only
- leaving the second derivative in terms of the first derivative
- stating the direction with no reason

**Wrong approaches.**
- solving the equation and comparing numerically

**Misconceptions.** BC-MIS-07010

**Variants.** 3 recorded: BC-QV-07005-01, BC-QV-07005-02, BC-QV-07005-03

**Official examples notes.** 2023 Q3(b), 2023 Q3(c)

**Invariant structure.** The second derivative is produced by differentiating the right side of the differential equation, the sign of that expression is settled over the whole interval rather than at one point, and the direction of the error follows from the concavity.

**Safe variables.**
- the modelled context
- the letters used
- the approximation already found

**Difficulty variables.**
- whether the sign of the second derivative can be settled from a stated bound
- whether the expression must be reduced to the dependent variable alone
- whether the approximation is a tangent line or an Euler step

Mapped difficulty factors: BC-DF-12 (Sign and direction handling)

**Expected solution path.**
- differentiate the right side with respect to the independent variable
- substitute the equation to remove the first derivative
- determine the sign over the interval
- state the direction with that reason

**Prohibited shortcuts.**
- none recorded in this record

**Multi-skill extensions.**
- none recorded in this record

## Family evt-existence [inferred]

1 archetype(s): BC-QA-05010.

### BC-QA-05010 Extreme Value Theorem existence claim on a closed interval

Evidence tag: inferred. Scope: shared. Primary unit: BC-UNIT-05. Units: BC-UNIT-05. Sources: ced:100, sg-23:3, sg-25:12.

**Description.** The response must decide whether a function is assured of attaining a largest and a smallest value on a closed interval, and say why.

**Concepts and skills required.** BC-SKL-05007, BC-SKL-05008, BC-SKL-05009, BC-SKL-05012

**Prerequisites.** BC-PRQ-05004, BC-PRQ-05003

**Typical wording.**
- must the function attain a maximum value on the closed interval, and justify the answer

**Common givens.**
- a continuity or differentiability statement
- or a graph with a break
- a closed interval

**What is produced.**
- a yes or no answer
- the continuity statement
- the named theorem

**Representations.** BC-REP-02 (Graphical), BC-REP-04 (Verbal description)

**Calculator status.** no_calculator

**Multipart structure.** A single multiple choice item, or a short part of a free response question.

**Scoring pattern.** Scored in the same shape as the Mean Value Theorem existence part: a point for establishing the hypothesis and a point for the conclusion with the theorem named, where a hypothesis merely asserted without support does not count (sg-23:3, sg-25:12).

**Scoring point types.** none recorded. Point type definitions are in [../scoring/point-taxonomy.md](../scoring/point-taxonomy.md).

**Common distractors.**
- asserting existence for an open interval
- citing the theorem for a function with a jump inside the interval
- naming the location of the extremum as the answer

**Wrong approaches.**
- differentiating to find the extremum when only existence was asked

**Misconceptions.** BC-MIS-05001, BC-MIS-05004, BC-MIS-05006, BC-MIS-05007

**Variants.** 3 recorded: BC-QV-05010-01, BC-QV-05010-02, BC-QV-05010-03

**Official examples notes.** none in 2023 to 2025 as a standalone part

**Invariant structure.** The only hypothesis at issue is continuity on the closed interval, and the conclusion is existence rather than location.

**Safe variables.**
- the letter for the function
- the interval
- the context

**Difficulty variables.**
- whether the interval is closed
- whether continuity is stated or must be inferred from differentiability
- whether a discontinuity is planted inside the interval

Mapped difficulty factors: BC-DF-01 (Number of concepts combined)

**Expected solution path.**
- check the interval is closed
- establish continuity from the given information
- state that a minimum value and a maximum value are attained
- name the theorem

**Prohibited shortcuts.**
- none recorded in this record

**Multi-skill extensions.**
- none recorded in this record

## Family exponential-model [inferred]

1 archetype(s): BC-QA-07008.

### BC-QA-07008 Exponential growth or decay model solved and interpreted

Evidence tag: inferred. Scope: shared. Primary unit: BC-UNIT-07. Units: BC-UNIT-07. Sources: ced:144, sg-23:12, sg-23:2.

**Description.** A quantity whose rate of change is proportional to itself is modelled, solved, and read back into the situation.

**Concepts and skills required.** BC-SKL-07034, BC-SKL-07035, BC-SKL-07036, BC-SKL-07037, BC-SKL-07038

**Prerequisites.** BC-PRQ-07001, BC-PRQ-07003, BC-PRQ-06002, BC-PRQ-06003

**Typical wording.**
- the rate of change of the quantity is proportional to the quantity; find an expression for the quantity at time t and state what the constant means in context

**Common givens.**
- a proportionality statement
- an initial value
- usually a second data pair

**What is produced.**
- the equation
- the exponential solution
- the constant
- an interpretation with units

**Representations.** BC-REP-01 (Symbolic (analytical) expression), BC-REP-05 (Contextual model), BC-REP-06 (Differential equation)

**Calculator status.** either

**Multipart structure.** A multipart free response question, or a single multiple choice item.

**Scoring pattern.** Scored as the separable family with the exponential form as the target: separation, antiderivatives, constant with the initial condition, and the explicit solution (sg-23:12), with a further point for an interpretation naming the quantity, the units, and the input (sg-23:2).

**Scoring point types.** none recorded. Point type definitions are in [../scoring/point-taxonomy.md](../scoring/point-taxonomy.md).

**Common distractors.**
- writing a linear model for proportional growth
- omitting the constant of proportionality
- reading the constant off a single data pair
- reporting a number with no units

**Wrong approaches.**
- treating the constant of proportionality and the constant of integration as the same object

**Misconceptions.** BC-MIS-07001, BC-MIS-07021, BC-MIS-07022, BC-MIS-07023

**Variants.** 3 recorded: BC-QV-07008-01, BC-QV-07008-02, BC-QV-07008-03

**Official examples notes.** none in 2023 to 2025

**Invariant structure.** The equation is the constant multiple form, the solution is the initial value multiplied by an exponential, and one further data pair determines the constant.

**Safe variables.**
- the modelled quantity
- the units
- the initial value

**Difficulty variables.**
- whether the constant is positive or negative
- whether a second data pair is supplied or must be read from a table
- whether an interpretation is demanded

Mapped difficulty factors: BC-DF-03 (Unusual representation), BC-DF-05 (Contextual interpretation), BC-DF-12 (Sign and direction handling), BC-DF-14 (Missing or implicit given)

**Expected solution path.**
- write the proportional model
- separate and solve
- use the initial value
- use a second pair to find the constant
- interpret with units

**Prohibited shortcuts.**
- none recorded in this record

**Multi-skill extensions.**
- none recorded in this record

## Family extremum-classification [verified]

3 archetype(s): BC-QA-05003, BC-QA-05007, BC-QA-05013.

### BC-QA-05003 Relative extremum classified from the behaviour of the first derivative

Evidence tag: verified. Scope: shared. Primary unit: BC-UNIT-05. Units: BC-UNIT-05. Sources: sg-23:13, frq-23:8.

**Description.** The response must say whether a named input is the location of a relative minimum, a relative maximum, or neither, and give a reason.

**Concepts and skills required.** BC-SKL-05019, BC-SKL-05020, BC-SKL-05021, BC-SKL-05022, BC-SKL-05023

**Prerequisites.** BC-PRQ-05006, BC-PRQ-05002

**Typical wording.**
- does the function have a relative minimum, a relative maximum, or neither at the named input, and give a reason for the answer

**Common givens.**
- a graph of the derivative made of segments and arcs
- or a derivative formula
- a named input

**What is produced.**
- the classification
- a reason naming the sign behaviour of the derivative

**Representations.** BC-REP-01 (Symbolic (analytical) expression), BC-REP-02 (Graphical), BC-REP-03 (Numerical table)

**Calculator status.** either

**Multipart structure.** One part of a multipart free response question, worth one point.

**Scoring pattern.** A single point for the answer together with its reason. A declaration that the derivative does not change sign at the input, so neither, is enough; intervals need not be presented, but any presented interval must be correct; a response stating only that the derivative is positive before and after the input does not earn the point (sg-23:13).

**Scoring point types.** none recorded. Point type definitions are in [../scoring/point-taxonomy.md](../scoring/point-taxonomy.md).

**Common distractors.**
- reading the plotted derivative as the function and reporting its own turning behaviour
- reversing the direction of the sign change
- classifying from the value of the derivative rather than its change
- declaring an extremum wherever the derivative is zero

**Wrong approaches.**
- applying the second derivative test where only the derivative graph is available and its slope is not discussed

**Misconceptions.** BC-MIS-05008, BC-MIS-05011, BC-MIS-05014

**Variants.** 3 recorded: BC-QV-05003-01, BC-QV-05003-02, BC-QV-05003-03

**Official examples notes.** 2023 Q4(a)

**Invariant structure.** The information supplied is about the derivative, the candidate input is named in the question rather than found, and the single available point covers both the classification and its reason.

**Safe variables.**
- the letter used for the function
- the shape of the derivative graph
- the named input

**Difficulty variables.**
- whether the answer is neither rather than an extremum
- whether the derivative is zero or undefined at the input
- whether the derivative is given as a graph, a table, or a formula

Mapped difficulty factors: BC-DF-03 (Unusual representation), BC-DF-13 (Reversed reasoning direction)

**Expected solution path.**
- locate the named input on the derivative information
- determine the sign of the derivative on each side
- state the sign change or its absence
- give the classification with that reason

**Prohibited shortcuts.**
- none recorded in this record

**Multi-skill extensions.**
- none recorded in this record

### BC-QA-05007 Critical point located and classified for a function given indirectly

Evidence tag: verified. Scope: shared. Primary unit: BC-UNIT-05. Units: BC-UNIT-05. Sources: sg-24:10, sg-24:13, frq-24:7, frq-24:8.

**Description.** A function is supplied through a differential equation or an accumulation function rather than by a formula, and the response must find a critical point and say what kind it is.

**Concepts and skills required.** BC-SKL-05010, BC-SKL-05020, BC-SKL-05039

**Prerequisites.** BC-PRQ-05001, BC-PRQ-05002

**Typical wording.**
- find the input in the stated range at which the modelled quantity has a critical point, and determine whether it is the location of a relative minimum, a relative maximum, or neither
- find all inputs in the stated interval at which the graph of the accumulation function has a critical point, and give a reason

**Common givens.**
- a differential equation with a stated sign fact
- or an accumulation function built on a plotted integrand

**What is produced.**
- the sign consideration
- the critical input
- the classification with justification

**Representations.** BC-REP-01 (Symbolic (analytical) expression), BC-REP-06 (Differential equation)

**Calculator status.** no_calculator

**Multipart structure.** One part of a multipart free response question, worth two or three points.

**Scoring pattern.** In 2024 three points were split as considering the sign of the derivative, identifying the input, and the answer with justification, with a second derivative evaluation accepted as an alternate justification (sg-24:10). In the accumulation form two points were split as the Fundamental Theorem of Calculus step and the answer with reason, and explicitly presenting the accumulation function with the wrong lower limit cost the first point (sg-24:13).

**Scoring point types.** none recorded. Point type definitions are in [../scoring/point-taxonomy.md](../scoring/point-taxonomy.md).

**Common distractors.**
- setting the given function rather than its derivative equal to zero
- ignoring the supplied sign fact that removes one factor
- classifying with no sign statement
- reading the plotted integrand as the accumulation function

**Wrong approaches.**
- solving the differential equation before locating the critical point

**Misconceptions.** BC-MIS-05008, BC-MIS-05011, BC-MIS-05024

**Variants.** 3 recorded: BC-QV-05007-01, BC-QV-05007-02, BC-QV-05007-03

**Official examples notes.** 2024 Q3(b), 2024 Q4(b)

**Invariant structure.** The derivative is available directly from the given relation, the critical point comes from setting that expression to zero within a stated range, and the classification needs a sign argument or a second derivative evaluation.

**Safe variables.**
- the modelled context
- the letters used
- the stated range

**Difficulty variables.**
- whether a supplied sign fact must be used to isolate the factor
- whether the classification is by sign change or by second derivative
- whether the given object is a differential equation or an accumulation function

Mapped difficulty factors: BC-DF-02 (Prerequisite depth), BC-DF-12 (Sign and direction handling)

**Expected solution path.**
- write the derivative from the given relation
- use the supplied sign fact to reduce the equation
- solve for the critical input inside the range
- argue the sign on each side or evaluate the second derivative

**Prohibited shortcuts.**
- none recorded in this record

**Multi-skill extensions.**
- none recorded in this record

### BC-QA-05013 Second derivative test applied at a critical point

Evidence tag: verified. Scope: shared. Primary unit: BC-UNIT-05. Units: BC-UNIT-05. Sources: sg-24:10, sg-25:19.

**Description.** The response must classify a critical point using the sign of the second derivative there, or state that the test is inconclusive.

**Concepts and skills required.** BC-SKL-05036, BC-SKL-05037, BC-SKL-05038, BC-SKL-05039

**Prerequisites.** BC-PRQ-05001

**Typical wording.**
- determine whether the critical point is the location of a relative minimum, a relative maximum, or neither

**Common givens.**
- a function, a differential equation, or an implicit relation
- a critical point

**What is produced.**
- the second derivative at the point
- the classification

**Representations.** BC-REP-01 (Symbolic (analytical) expression), BC-REP-06 (Differential equation)

**Calculator status.** either

**Multipart structure.** One part of a multipart free response question, or a single multiple choice item.

**Scoring pattern.** Accepted in 2024 as an alternate justification for a classification part, earning the same point as the sign argument (sg-24:10). Refused the justification point in 2025 where the demand was a global claim, while the answer point remained available (sg-25:19).

**Scoring point types.** none recorded. Point type definitions are in [../scoring/point-taxonomy.md](../scoring/point-taxonomy.md).

**Common distractors.**
- applying the test at an input where the first derivative is not zero
- reversing the sign convention
- treating a zero second derivative as proof of neither

**Wrong approaches.**
- classifying from the sign of the function value

**Misconceptions.** BC-MIS-05018, BC-MIS-05023, BC-MIS-05024

**Variants.** 3 recorded: BC-QV-05013-01, BC-QV-05013-02, BC-QV-05013-03

**Official examples notes.** 2024 Q3(b) alternate solution

**Invariant structure.** The critical point is already known or found in an earlier step, and the classification rests on one evaluation rather than on a sign analysis across an interval.

**Safe variables.**
- the function
- the critical point
- the context

**Difficulty variables.**
- whether the second derivative is zero at the point
- whether the question demands a global claim
- whether the second derivative must itself be derived implicitly

Mapped difficulty factors: BC-DF-01 (Number of concepts combined)

**Expected solution path.**
- confirm the first derivative is zero at the point
- evaluate the second derivative there
- classify by its sign or declare the test inconclusive

**Prohibited shortcuts.**
- none recorded in this record

**Multi-skill extensions.**
- none recorded in this record

## Family ftc-differentiation [verified]

1 archetype(s): BC-QA-06012.

### BC-QA-06012 Differentiating an accumulation function with a variable upper limit

Evidence tag: verified. Scope: shared. Primary unit: BC-UNIT-06. Units: BC-UNIT-06. Sources: sg-24:15, sg-25:16, frq-24:9, frq-25:7.

**Description.** A function is defined as a definite integral with a variable upper limit and the response differentiates it, possibly with a composite upper limit, and evaluates the derivative at a point.

**Concepts and skills required.** BC-SKL-06018, BC-SKL-06019, BC-SKL-06017, BC-SKL-06021

**Prerequisites.** BC-PRQ-06005, BC-PRQ-06013

**Typical wording.**
- the function h is defined by the integral from a fixed input to x of the given expression; find the value of h prime at a stated input, showing the work that leads to your answer

**Common givens.**
- none recorded in this record

**What is produced.**
- none recorded in this record

**Representations.** BC-REP-01 (Symbolic (analytical) expression), BC-REP-02 (Graphical), BC-REP-03 (Numerical table)

**Calculator status.** no_calculator

**Multipart structure.** Typically one part of a multipart free response question, or a single multiple choice item.

**Scoring pattern.** One point for using the Fundamental Theorem of Calculus and one for the value; the theorem point may be earned by presenting the derivative in terms of the integrand, while a response that reaches the correct value without exhibiting the theorem can still earn the answer point through an implied application (sg-24:15, sg-25:16).

**Scoring point types.** none recorded. Point type definitions are in [../scoring/point-taxonomy.md](../scoring/point-taxonomy.md).

**Common distractors.**
- substituting the variable of integration instead of the upper limit
- forgetting the chain rule factor for a composite upper limit
- differentiating the integrand as well as evaluating it
- treating the accumulation function as the integrand

**Wrong approaches.**
- none recorded in this record; see ../misconceptions/error-to-concept-map.md

**Misconceptions.** BC-MIS-06023, BC-MIS-06024

**Variants.** 3 recorded: BC-QV-06012-01, BC-QV-06012-02, BC-QV-06012-03

**Official examples notes.** 2024 Q5(a), 2025 Q4(A)

**Invariant structure.** The Fundamental Theorem of Calculus part one converts the derivative of the accumulation into the integrand evaluated at the upper limit, multiplied by the derivative of that limit when it is a function of x.

**Safe variables.**
- the integrand
- the fixed lower limit
- the point of evaluation
- the letter used for the variable of integration

**Difficulty variables.**
- upper limit equal to x versus a function of x
- integrand given by a formula, a graph, or a table
- whether a reason naming the theorem is demanded
- whether values of the integrand must come from a table

Mapped difficulty factors: BC-DF-03 (Unusual representation), BC-DF-09 (Theorem recognition), BC-DF-10 (Required justification)

**Expected solution path.**
- state that the derivative of the accumulation equals the integrand at the upper limit
- multiply by the derivative of the upper limit when it is composite
- substitute the requested input
- evaluate using the supplied representation of the integrand

**Prohibited shortcuts.**
- none recorded in this record

**Multi-skill extensions.**
- none recorded in this record

## Family function-derivative-graph-relationship [inferred]

1 archetype(s): BC-QA-05009.

### BC-QA-05009 Relating the graphs of a function and its first two derivatives

Evidence tag: inferred. Scope: shared. Primary unit: BC-UNIT-05. Units: BC-UNIT-05. Sources: ced:106, ced:107, sg-23:13, sg-25:17.

**Description.** Three related objects are in play and the response must identify which is which, or read a feature of one off another.

**Concepts and skills required.** BC-SKL-05040, BC-SKL-05041, BC-SKL-05042, BC-SKL-05043, BC-SKL-05044, BC-SKL-05045, BC-SKL-05046, BC-SKL-05047, BC-SKL-05048

**Prerequisites.** BC-PRQ-05006

**Typical wording.**
- which of the graphs shown could be the function, its derivative, and its second derivative
- sketch a possible graph of the function on the given interval

**Common givens.**
- two or three plotted curves
- or a table of signs
- sometimes one known function value

**What is produced.**
- an assignment of roles
- or a sketch with the correct features

**Representations.** BC-REP-01 (Symbolic (analytical) expression), BC-REP-02 (Graphical), BC-REP-03 (Numerical table)

**Calculator status.** either

**Multipart structure.** A single multiple choice item, or a part of a free response question phrased as a feature question.

**Scoring pattern.** Where the free response questions of 2023 to 2025 use this relationship they score the features rather than the drawing, awarding separate points for the list of inputs and for the reason (sg-23:13, sg-25:17).

**Scoring point types.** none recorded. Point type definitions are in [../scoring/point-taxonomy.md](../scoring/point-taxonomy.md).

**Common distractors.**
- ordering the three curves in the reverse derivative direction
- matching turning points with turning points instead of with zeros
- treating the plotted derivative as the function

**Wrong approaches.**
- deciding the order from the vertical scale of the plots

**Misconceptions.** BC-MIS-05011, BC-MIS-05020, BC-MIS-05025, BC-MIS-05026

**Variants.** 3 recorded: BC-QV-05009-01, BC-QV-05009-02, BC-QV-05009-03

**Official examples notes.** none in 2023 to 2025 as a standalone part

**Invariant structure.** Turning points of one object sit at sign changes of the next, and the question tests the correspondence rather than any computation.

**Safe variables.**
- the shapes of the curves
- the labelling letters
- the plotted window

**Difficulty variables.**
- whether three objects are in play rather than two
- whether a known value is supplied to fix the sketch
- whether the presentation is graphical or tabular

Mapped difficulty factors: BC-DF-03 (Unusual representation), BC-DF-13 (Reversed reasoning direction)

**Expected solution path.**
- find the turning points of each curve
- match them with the zeros of another
- apply the rule twice to order all three

**Prohibited shortcuts.**
- none recorded in this record

**Multi-skill extensions.**
- none recorded in this record

## Family higher-order-derivative [verified]

1 archetype(s): BC-QA-03008.

### BC-QA-03008 Higher-order derivative of a function or of a derivative expression

Evidence tag: verified. Scope: shared. Primary unit: BC-UNIT-03. Units: BC-UNIT-03. Sources: ced:80, sg-25:20.

**Description.** A function, a derivative, or a differential equation is supplied and the response produces the second or a higher derivative, often evaluating it at a point.

**Concepts and skills required.** BC-SKL-03030, BC-SKL-03031, BC-SKL-03032, BC-SKL-03033, BC-SKL-03034

**Prerequisites.** BC-PRQ-03005, BC-PRQ-03006

**Typical wording.**
- find the value of the second derivative at the given point, showing the work that leads to the answer

**Common givens.**
- none recorded in this record

**What is produced.**
- none recorded in this record

**Representations.** BC-REP-01 (Symbolic (analytical) expression), BC-REP-06 (Differential equation)

**Calculator status.** no_calculator

**Multipart structure.** Ordinarily the opening part of a Taylor polynomial question or of a differential equation question.

**Scoring pattern.** The 2025 BC scoring guidelines award one point for the product rule, one point for the chain rule, and one point for the value of the second derivative at the point, so a response can earn the two rule points with an arithmetic slip in the final value (sg-25:20).

**Scoring point types.** none recorded. Point type definitions are in [../scoring/point-taxonomy.md](../scoring/point-taxonomy.md).

**Common distractors.**
- the dependent variable treated as a constant when differentiating
- the product rule omitted on a mixed term
- the first derivative value not substituted
- the second derivative reported in the wrong notation

**Wrong approaches.**
- none recorded in this record; see ../misconceptions/error-to-concept-map.md

**Misconceptions.** BC-MIS-03013, BC-MIS-03014, BC-MIS-03005

**Variants.** 3 recorded: BC-QV-03008-01, BC-QV-03008-02, BC-QV-03008-03

**Official examples notes.** 2025 Q5(A)

**Invariant structure.** Each order of differentiation is a separate application of the rules; when the expression being differentiated contains the dependent variable, the product rule and the chain rule both appear, and the first derivative value must be substituted before a numerical second derivative can be reported.

**Safe variables.**
- the function or derivative supplied
- the point of evaluation
- the order requested
- the notation used in the prompt

**Difficulty variables.**
- whether the expression contains the dependent variable
- whether a product term forces the product rule
- whether the order requested is above two
- whether the answer must be expressed in the notation of the prompt

Mapped difficulty factors: BC-DF-04 (Notation complexity)

**Expected solution path.**
- differentiate the supplied expression with respect to the independent variable
- apply the product rule to mixed terms and the chain rule to terms in the dependent variable
- substitute the coordinates of the point
- substitute the value of the first derivative at that point
- report the numerical value

**Prohibited shortcuts.**
- none recorded in this record

**Multi-skill extensions.**
- none recorded in this record

## Family implicit-differentiation [verified]

3 archetype(s): BC-QA-03004, BC-QA-03005, BC-QA-05012.

### BC-QA-03004 Implicit differentiation producing or verifying dy/dx

Evidence tag: verified. Scope: shared. Primary unit: BC-UNIT-03. Units: BC-UNIT-03. Sources: ced:76, cr-23:22, cr-24:17, crabbc-25:24, crabbc-25:25.

**Description.** An equation in x and y is supplied and the response differentiates implicitly, solves for dy/dx, and in many cases verifies a stated expression or evaluates the slope at a point.

**Concepts and skills required.** BC-SKL-03007, BC-SKL-03008, BC-SKL-03009, BC-SKL-03010, BC-SKL-03011, BC-SKL-03014

**Prerequisites.** BC-PRQ-03002, BC-PRQ-03005

**Typical wording.**
- show that dy/dx is equal to the stated expression for the given curve
- find dy/dx for the curve defined by the given equation

**Common givens.**
- none recorded in this record

**What is produced.**
- none recorded in this record

**Representations.** BC-REP-01 (Symbolic (analytical) expression)

**Calculator status.** no_calculator

**Multipart structure.** Ordinarily the opening part of a multipart free response question whose later parts reuse the same curve.

**Scoring pattern.** The Chief Reader reports describe this task scored as one point for an eligible attempt at implicit differentiation and a second point for a completely correct differentiation, with a further point for the algebraic verification or evaluation; 2025 awards separate product rule and chain rule points when the differentiation is of a derivative expression (crabbc-25:24, sg-25:20).

**Scoring point types.** none recorded. Point type definitions are in [../scoring/point-taxonomy.md](../scoring/point-taxonomy.md).

**Common distractors.**
- y terms differentiated without the dy/dx factor
- a mixed term differentiated as though one variable were constant
- the right hand side of the equation dropped
- dy/dx solved for before the terms are collected

**Wrong approaches.**
- none recorded in this record; see ../misconceptions/error-to-concept-map.md

**Misconceptions.** BC-MIS-03004, BC-MIS-03005, BC-MIS-03006

**Variants.** 4 recorded: BC-QV-03004-01, BC-QV-03004-02, BC-QV-03004-03, BC-QV-03004-04

**Official examples notes.** 2023 AB Q6(a), 2024 AB Q5, 2025 AB Q6 part A as described in the Chief Reader reports

**Invariant structure.** The equation mixes x and y in at least one term that needs the product rule; every y term contributes a dy/dx factor; the differentiated equation is linear in dy/dx and the answer generally involves both variables.

**Safe variables.**
- the specific equation
- the letters naming the variables
- the point at which the slope is requested

**Difficulty variables.**
- whether a mixed product term is present
- whether the expression for dy/dx is supplied to be verified or must be derived
- whether the result must be evaluated at a point
- whether the same curve is reused for later parts

Mapped difficulty factors: BC-DF-06 (Algebraic burden), BC-DF-08 (Multi-step dependency), BC-DF-13 (Reversed reasoning direction), BC-DF-14 (Missing or implicit given)

**Expected solution path.**
- differentiate every term of both sides with respect to x
- attach a dy/dx factor to each y term
- apply the product rule to mixed terms
- collect and factor the dy/dx terms
- divide to isolate dy/dx
- substitute the point when a numerical slope is requested

**Prohibited shortcuts.**
- none recorded in this record

**Multi-skill extensions.**
- none recorded in this record

### BC-QA-03005 Horizontal or vertical tangent on an implicitly defined curve

Evidence tag: verified. Scope: shared. Primary unit: BC-UNIT-03. Units: BC-UNIT-03. Sources: cr-23:22, cr-23:23, cr-24:17, crabbc-25:24, crabbc-25:25.

**Description.** Given a curve and its dy/dx, the response decides where the tangent line is horizontal or vertical, or whether a stated line can be tangent to the curve.

**Concepts and skills required.** BC-SKL-03012, BC-SKL-03013, BC-SKL-03011

**Prerequisites.** BC-PRQ-03007, BC-PRQ-03002

**Typical wording.**
- find the coordinates of a point on the curve at which the tangent line is vertical, or explain why no such point exists
- determine whether the stated horizontal line is tangent to the curve

**Common givens.**
- none recorded in this record

**What is produced.**
- none recorded in this record

**Representations.** BC-REP-01 (Symbolic (analytical) expression), BC-REP-02 (Graphical)

**Calculator status.** no_calculator

**Multipart structure.** One or two parts inside the implicit differentiation question, reusing the curve from the opening part.

**Scoring pattern.** The Chief Reader reports record that responses commonly determined the correct condition on dy/dx but failed to connect it to the defining equation, and that a response could earn the points without showing the numerator is nonzero in the 2025 version (cr-23:23, cr-24:17, crabbc-25:25).

**Scoring point types.** none recorded. Point type definitions are in [../scoring/point-taxonomy.md](../scoring/point-taxonomy.md).

**Common distractors.**
- a coordinate that satisfies the condition on dy/dx but not the curve equation
- the two conditions swapped, so a zero denominator is read as a horizontal tangent
- only one of two candidate values reported
- a conclusion stated without connecting dy/dx to the curve

**Wrong approaches.**
- none recorded in this record; see ../misconceptions/error-to-concept-map.md

**Misconceptions.** BC-MIS-03007, BC-MIS-03006

**Variants.** 3 recorded: BC-QV-03005-01, BC-QV-03005-02, BC-QV-03005-03

**Official examples notes.** 2023 AB Q6(b) and (c), 2024 AB Q5(b) and (c), 2025 AB Q6 part C as described in the Chief Reader reports

**Invariant structure.** The condition on dy/dx and the defining equation must both hold; a candidate that satisfies only one of the two is not a point of the required kind.

**Safe variables.**
- the curve
- which of the two tangent directions is asked for
- the letters naming the variables

**Difficulty variables.**
- whether the answer is that no such point exists
- whether more than one candidate value of the variable arises
- whether the numerator must also be checked to be nonzero
- whether the question is posed as testing a stated line

Mapped difficulty factors: BC-DF-09 (Theorem recognition)

**Expected solution path.**
- set the numerator or the denominator of dy/dx equal to zero as the direction requires
- solve for the coordinate that condition fixes
- substitute into the defining equation to find the other coordinate
- discard candidates that do not lie on the curve
- state the conclusion in words

**Prohibited shortcuts.**
- none recorded in this record

**Multi-skill extensions.**
- none recorded in this record

### BC-QA-05012 Critical points and second derivative behaviour of an implicit relation

Evidence tag: verified. Scope: shared. Primary unit: BC-UNIT-05. Units: BC-UNIT-05. Sources: sg-25:21, frq-25:8.

**Description.** A curve is given by an equation in two variables or by a differential equation, and the response must find critical points or evaluate a second derivative at a point on it.

**Concepts and skills required.** BC-SKL-05058, BC-SKL-05059, BC-SKL-05060, BC-SKL-05061, BC-SKL-05062, BC-SKL-05063

**Prerequisites.** BC-PRQ-05007, BC-PRQ-05001

**Typical wording.**
- find the value of the second derivative at the given point on the curve, showing the work that leads to the answer
- find the coordinates of every point on the curve at which the tangent line is horizontal

**Common givens.**
- an implicit equation or a differential equation
- a point on the curve

**What is produced.**
- the differentiated expression
- the substitution of the first derivative
- the numerical value or the coordinates

**Representations.** BC-REP-01 (Symbolic (analytical) expression), BC-REP-02 (Graphical), BC-REP-06 (Differential equation)

**Calculator status.** no_calculator

**Multipart structure.** One part of a multipart free response question, worth two or three points.

**Scoring pattern.** Separate points for the differentiation and for the substitution of the derivative expression, with the value point available from either route: a response that differentiates correctly but does not substitute earns the first and not the second, a response that substitutes correctly inside a faulty differentiation earns the second and stays eligible for the value with a consistent answer (sg-25:21).

**Scoring point types.** none recorded. Point type definitions are in [../scoring/point-taxonomy.md](../scoring/point-taxonomy.md).

**Common distractors.**
- differentiating as though the second variable were constant
- leaving the first derivative symbol unsubstituted in the final value
- reporting an input value with no matching output on the curve
- treating a vanishing denominator as a horizontal tangent

**Wrong approaches.**
- solving the relation explicitly when it is not solvable

**Misconceptions.** BC-MIS-05031, BC-MIS-05032, BC-MIS-05033

**Variants.** 3 recorded: BC-QV-05012-01, BC-QV-05012-02, BC-QV-05012-03

**Official examples notes.** 2025 Q5(A)

**Invariant structure.** The derivative is a relation in both variables, a point on the curve must satisfy the defining equation as well as the derived condition, and the second derivative is an expression in both variables and the first derivative.

**Safe variables.**
- the relation
- the given point
- the letters used

**Difficulty variables.**
- whether the second derivative is asked for or only the first
- whether the relation is polynomial or transcendental
- whether the critical points need both conditions solved together

Mapped difficulty factors: BC-DF-08 (Multi-step dependency), BC-DF-11 (Unfamiliar surface presentation)

**Expected solution path.**
- differentiate the relation implicitly
- differentiate again keeping both variables
- substitute the first derivative and the coordinates
- report the value or the coordinates

**Prohibited shortcuts.**
- none recorded in this record

**Multi-skill extensions.**
- none recorded in this record

## Family improper-integral [verified]

1 archetype(s): BC-QA-06011.

### BC-QA-06011 Improper integral convergence or divergence

Evidence tag: verified. Scope: BC_only. Primary unit: BC-UNIT-06. Units: BC-UNIT-06. Sources: sg-23:17, frq-23:9.

**Description.** An integral with an infinite limit of integration or an unbounded integrand is rewritten as a limit of definite integrals and evaluated, or shown to diverge.

**Concepts and skills required.** BC-SKL-06066, BC-SKL-06067, BC-SKL-06068, BC-SKL-06069, BC-SKL-06070

**Prerequisites.** none recorded

**Typical wording.**
- evaluate the improper integral of the given expression, or show that the integral diverges

**Common givens.**
- none recorded in this record

**What is produced.**
- none recorded in this record

**Representations.** BC-REP-01 (Symbolic (analytical) expression), BC-REP-02 (Graphical)

**Calculator status.** no_calculator

**Multipart structure.** Typically one part of a multipart free response question, or a single multiple choice item.

**Scoring pattern.** One point for correct limit notation carried throughout with no arithmetic involving infinity, one for the antiderivative of the required form, and one for the value; substituting into the antiderivative while the expression is still in the substituted variable forfeits eligibility for the value point (sg-23:17).

**Scoring point types.** none recorded. Point type definitions are in [../scoring/point-taxonomy.md](../scoring/point-taxonomy.md).

**Common distractors.**
- writing arithmetic with infinity in place of a limit
- dropping the limit notation once the antiderivative is found
- reporting a value for a divergent integral
- keeping the original limits after a substitution

**Wrong approaches.**
- none recorded in this record; see ../misconceptions/error-to-concept-map.md

**Misconceptions.** BC-MIS-06016, BC-MIS-06020, BC-MIS-06021

**Variants.** 3 recorded: BC-QV-06011-01, BC-QV-06011-02, BC-QV-06011-03

**Official examples notes.** 2023 Q5(b)

**Invariant structure.** The impropriety is isolated by replacing the offending limit with a variable; limit notation must be carried through the whole computation; the conclusion is a finite value or a statement of divergence.

**Safe variables.**
- the integrand
- the finite limit of integration
- which end is improper

**Difficulty variables.**
- infinite limit versus unbounded integrand
- convergent versus divergent
- whether the integrand requires substitution first
- whether the integral is improper at more than one place

Mapped difficulty factors: BC-DF-06 (Algebraic burden), BC-DF-08 (Multi-step dependency)

**Expected solution path.**
- name the impropriety and replace the offending limit by a variable
- write the limit of the definite integral
- antidifferentiate and substitute both limits
- evaluate the limit and state convergence with a value or divergence

**Prohibited shortcuts.**
- none recorded in this record

**Multi-skill extensions.**
- none recorded in this record

## Family infinite-limit-asymptote [inferred]

1 archetype(s): BC-QA-01009.

### BC-QA-01009 Vertical asymptote located and the one sided infinite limits stated

Evidence tag: inferred. Scope: shared. Primary unit: BC-UNIT-01. Units: BC-UNIT-01. Sources: ced:51.

**Description.** A rational or logarithmic expression is presented and the response locates the vertical asymptotes and states the behaviour on each side.

**Concepts and skills required.** BC-SKL-01054, BC-SKL-01055, BC-SKL-01056, BC-SKL-01041

**Prerequisites.** BC-PRQ-01009, BC-PRQ-01001

**Typical wording.**
- Find the vertical asymptotes of the graph of the given function and describe the behaviour of the function near each one.

**Common givens.**
- none recorded in this record

**What is produced.**
- none recorded in this record

**Representations.** BC-REP-01 (Symbolic (analytical) expression), BC-REP-02 (Graphical)

**Calculator status.** no_calculator

**Multipart structure.** Typically a single multiple choice item.

**Scoring pattern.** One point for the locations and one for the one sided behaviour stated in correct notation.

**Scoring point types.** none recorded. Point type definitions are in [../scoring/point-taxonomy.md](../scoring/point-taxonomy.md).

**Common distractors.**
- naming an asymptote at a cancelled factor
- writing a single two sided infinite limit when the signs differ
- reporting the limit as a real number
- omitting the side in the notation

**Wrong approaches.**
- none recorded in this record; see ../misconceptions/error-to-concept-map.md

**Misconceptions.** BC-MIS-01012

**Variants.** 3 recorded: BC-QV-01009-01, BC-QV-01009-02, BC-QV-01009-03

**Official examples notes.** none in 2023 to 2025 [inferred]

**Invariant structure.** At least one zero of the original denominator cancels, so locating the asymptotes requires simplification before the sign analysis, and the two sides can carry opposite signs.

**Safe variables.**
- the rational expression
- the variable name
- the number of zeros of the denominator

**Difficulty variables.**
- whether a factor cancels
- whether the two sides have the same sign
- whether the response must state the limits in notation
- whether a logarithmic asymptote is included

Mapped difficulty factors: BC-DF-02 (Prerequisite depth), BC-DF-04 (Notation complexity), BC-DF-10 (Required justification), BC-DF-12 (Sign and direction handling), BC-DF-14 (Missing or implicit given)

**Expected solution path.**
- factor numerator and denominator
- divide out common factors and record where this was done
- identify the remaining zeros of the denominator
- determine the sign of the quotient on each side
- write the one sided infinite limit statements

**Prohibited shortcuts.**
- none recorded in this record

**Multi-skill extensions.**
- none recorded in this record

## Family integral-approximation [verified]

2 archetype(s): BC-QA-06001, BC-QA-06002.

### BC-QA-06001 Riemann sum from a table with over or under estimate reasoning

Evidence tag: verified. Scope: shared. Primary unit: BC-UNIT-06. Units: BC-UNIT-06. Sources: sg-23:2, sg-23:3, sg-24:3, frq-23:3, frq-24:3.

**Description.** A contextual rate is given at selected times in a table; the response approximates the definite integral of the rate with a left or right Riemann sum over the subintervals the data indicate, and may be asked whether the approximation is an under or over estimate.

**Concepts and skills required.** BC-SKL-06005, BC-SKL-06006, BC-SKL-06010, BC-SKL-06036

**Prerequisites.** BC-PRQ-06005, BC-PRQ-06008, BC-PRQ-06012

**Typical wording.**
- approximate the value of the definite integral of the rate using a Riemann sum with the subintervals indicated by the data in the table
- using correct units, interpret the meaning of the definite integral of the rate over the stated interval in the context of the problem

**Common givens.**
- none recorded in this record

**What is produced.**
- none recorded in this record

**Representations.** BC-REP-03 (Numerical table), BC-REP-05 (Contextual model)

**Calculator status.** calculator

**Multipart structure.** Typically one part of a multipart free response question, or a single multiple choice item.

**Scoring pattern.** One point for the form of the Riemann sum and one point for the value, with the form point requiring at least five of the six factors correct, and any error in the sum costing the answer point; a fully correct sum using the wrong endpoint earns one of the two points (sg-23:2, sg-23:3). A bare numerical answer with no supporting products earns neither point (sg-23:3).

**Scoring point types.** none recorded. Point type definitions are in [../scoring/point-taxonomy.md](../scoring/point-taxonomy.md).

**Common distractors.**
- using a single uniform width for unevenly spaced data
- using the opposite endpoint from the one requested
- reporting the sum of the rate values without multiplying by widths
- dividing by the number of subintervals as though averaging

**Wrong approaches.**
- none recorded in this record; see ../misconceptions/error-to-concept-map.md

**Misconceptions.** BC-MIS-06001, BC-MIS-06002, BC-MIS-06003, BC-MIS-06005

**Variants.** 3 recorded: BC-QV-06001-01, BC-QV-06001-02, BC-QV-06001-03

**Official examples notes.** 2023 Q1(a), 2024 Q1(b)

**Invariant structure.** A differentiable rate function is tabulated at unevenly spaced inputs; the number of subintervals equals the number of gaps in the table; the sum is built from values read directly out of the table and widths taken as differences of consecutive table inputs.

**Safe variables.**
- the quantity being accumulated
- the unit of the rate
- the number of table rows
- the names of the variables

**Difficulty variables.**
- nonuniform versus uniform subinterval widths
- left versus right endpoint selection
- whether an over or under estimate justification is demanded
- whether an interpretation with units is demanded in the same part
- whether the table is monotone

Mapped difficulty factors: BC-DF-01 (Number of concepts combined), BC-DF-03 (Unusual representation), BC-DF-05 (Contextual interpretation), BC-DF-10 (Required justification), BC-DF-14 (Missing or implicit given), BC-DF-15 (Unsignposted procedure selection), BC-DF-16 (Units and labelling demand)

**Expected solution path.**
- identify the subintervals indicated by the table
- select the endpoint value on each subinterval
- multiply each value by the width of its subinterval
- sum the products
- state the approximation, and when asked, compare with the exact integral using monotonicity

**Prohibited shortcuts.**
- none recorded in this record

**Multi-skill extensions.**
- none recorded in this record

### BC-QA-06002 Trapezoidal approximation of an accumulated amount from a table

Evidence tag: verified. Scope: shared. Primary unit: BC-UNIT-06. Units: BC-UNIT-06. Sources: sg-25:13, frq-25:6.

**Description.** A contextual rate is tabulated and the response approximates its definite integral with a trapezoidal sum over the subintervals indicated by the data.

**Concepts and skills required.** BC-SKL-06008, BC-SKL-06011, BC-SKL-06036

**Prerequisites.** BC-PRQ-06005, BC-PRQ-06007, BC-PRQ-06008, BC-PRQ-06012

**Typical wording.**
- use a trapezoidal sum with the subintervals indicated by the data in the table to approximate the value of the definite integral of the rate

**Common givens.**
- none recorded in this record

**What is produced.**
- none recorded in this record

**Representations.** BC-REP-03 (Numerical table), BC-REP-05 (Contextual model)

**Calculator status.** no_calculator

**Multipart structure.** Typically one part of a multipart free response question, or a single multiple choice item.

**Scoring pattern.** One point for the form of the trapezoidal sum, defined as three terms each a product of two factors with the one half incorporated, requiring at least five of six factors correct, and one point for the value; a completely correct left or right Riemann sum earns the form point but not the answer point, and the average of a correct left and right sum earns both (sg-25:13).

**Scoring point types.** none recorded. Point type definitions are in [../scoring/point-taxonomy.md](../scoring/point-taxonomy.md).

**Common distractors.**
- halving only one of the terms
- applying a single common width to unevenly spaced data
- using the average of all table values times the total width
- adding the left and right sums without dividing by two

**Wrong approaches.**
- none recorded in this record; see ../misconceptions/error-to-concept-map.md

**Misconceptions.** BC-MIS-06001, BC-MIS-06002, BC-MIS-06003, BC-MIS-06004, BC-MIS-06005, BC-MIS-06006

**Variants.** 3 recorded: BC-QV-06002-01, BC-QV-06002-02, BC-QV-06002-03

**Official examples notes.** 2025 Q3(C)

**Invariant structure.** A differentiable rate is tabulated at three or more inputs; each subinterval contributes the average of its two endpoint values multiplied by its width; the number of trapezoids equals the number of gaps in the table.

**Safe variables.**
- the context and quantity
- the unit of the rate
- the spacing of the table inputs

**Difficulty variables.**
- nonuniform versus uniform widths
- whether the sum must be simplified to a single number
- whether a concavity based over or under estimate justification is required
- calculator versus no calculator

Mapped difficulty factors: BC-DF-06 (Algebraic burden), BC-DF-07 (Calculator workflow), BC-DF-10 (Required justification)

**Expected solution path.**
- form each trapezoid as the average of the two endpoint values times the width
- sum the three contributions
- simplify to a single value

**Prohibited shortcuts.**
- none recorded in this record

**Multi-skill extensions.**
- none recorded in this record

## Family integral-properties [inferred]

1 archetype(s): BC-QA-06013.

### BC-QA-06013 Manipulating definite integrals with their properties

Evidence tag: inferred. Scope: shared. Primary unit: BC-UNIT-06. Units: BC-UNIT-06. Sources: ced:123.

**Description.** Values of definite integrals over stated intervals are supplied and the response combines them using the constant multiple, sum, reversal, and adjacent interval properties to produce the value of a different integral.

**Concepts and skills required.** BC-SKL-06029, BC-SKL-06030, BC-SKL-06031, BC-SKL-06032, BC-SKL-06033, BC-SKL-06035

**Prerequisites.** none recorded

**Typical wording.**
- the values of two definite integrals over stated intervals are given; find the value of a third definite integral

**Common givens.**
- none recorded in this record

**What is produced.**
- none recorded in this record

**Representations.** BC-REP-01 (Symbolic (analytical) expression), BC-REP-03 (Numerical table), BC-REP-04 (Verbal description)

**Calculator status.** no_calculator

**Multipart structure.** Typically one part of a multipart free response question, or a single multiple choice item.

**Scoring pattern.** No dedicated properties part appears in the 2023 to 2025 free response questions read for this unit; the scoring behaviour is inferred from parts where a correct value alone earns the point and an incorrect interval forfeits it (sg-25:18).

**Scoring point types.** none recorded. Point type definitions are in [../scoring/point-taxonomy.md](../scoring/point-taxonomy.md).

**Common distractors.**
- adding integrals over overlapping rather than adjacent intervals
- forgetting the sign change when the limits are reversed
- distributing an integral across a product or a quotient
- treating the integral of a constant as the constant itself

**Wrong approaches.**
- none recorded in this record; see ../misconceptions/error-to-concept-map.md

**Misconceptions.** BC-MIS-06026

**Variants.** 3 recorded: BC-QV-06013-01, BC-QV-06013-02, BC-QV-06013-03

**Official examples notes.** none in 2023 to 2025

**Invariant structure.** No integrand is evaluated; only the supplied values and the algebraic properties of the integral are used, with the interval endpoints determining which property applies.

**Safe variables.**
- the supplied values
- the names of the functions
- the interval endpoints

**Difficulty variables.**
- whether a reversal of limits is required
- whether an interval must be split or joined
- whether a constant multiple or a sum appears
- whether an integral of a constant must be computed geometrically

Mapped difficulty factors: BC-DF-02 (Prerequisite depth), BC-DF-08 (Multi-step dependency), BC-DF-14 (Missing or implicit given), BC-DF-17 (Case splitting at a boundary)

**Expected solution path.**
- match each requested integral to the supplied ones
- apply reversal, additivity, and linearity to rewrite
- substitute the supplied values
- simplify

**Prohibited shortcuts.**
- none recorded in this record

**Multi-skill extensions.**
- none recorded in this record

## Family inverse-function-derivative [inferred]

1 archetype(s): BC-QA-03006.

### BC-QA-03006 Derivative of an inverse function at a point

Evidence tag: inferred. Scope: shared. Primary unit: BC-UNIT-03. Units: BC-UNIT-03. Sources: ced:77, ced:72.

**Description.** A function is supplied by formula, table, or graph and the response computes the derivative of its inverse at a stated value.

**Concepts and skills required.** BC-SKL-03015, BC-SKL-03016, BC-SKL-03017, BC-SKL-03018, BC-SKL-03019

**Prerequisites.** BC-PRQ-03003

**Typical wording.**
- the function g is the inverse of f; find the derivative of g at the stated value

**Common givens.**
- none recorded in this record

**What is produced.**
- none recorded in this record

**Representations.** BC-REP-01 (Symbolic (analytical) expression), BC-REP-02 (Graphical), BC-REP-03 (Numerical table)

**Calculator status.** either

**Multipart structure.** A single multiple choice item, or one part of a multi-representation free response question.

**Scoring pattern.** Scored as an answer point in multiple choice; in free response the matching input has to be visible for the method to be communicated.

**Scoring point types.** none recorded. Point type definitions are in [../scoring/point-taxonomy.md](../scoring/point-taxonomy.md).

**Common distractors.**
- the reciprocal of the derivative taken at the stated value rather than at the matching input
- the derivative of the original function reported unchanged
- the negative of the derivative
- the reciprocal of the function value

**Wrong approaches.**
- none recorded in this record; see ../misconceptions/error-to-concept-map.md

**Misconceptions.** BC-MIS-03008, BC-MIS-03009

**Variants.** 3 recorded: BC-QV-03006-01, BC-QV-03006-02, BC-QV-03006-03

**Official examples notes.** none in the 2023 to 2025 BC free response questions read for this unit

**Invariant structure.** The value at which the derivative of the inverse is requested is an output of the original function; the answer is the reciprocal of the original derivative at the matching input, and the rule needs that derivative to be nonzero.

**Safe variables.**
- the representation of the original function
- the letters naming the function and its inverse
- the value requested

**Difficulty variables.**
- whether the matching input must be solved for rather than read
- whether a distractor input equal to the requested value exists
- whether the hypotheses must be stated
- whether the original function is given only graphically

Mapped difficulty factors: BC-DF-03 (Unusual representation), BC-DF-09 (Theorem recognition), BC-DF-13 (Reversed reasoning direction)

**Expected solution path.**
- identify the input whose output is the stated value
- differentiate the original function or read its derivative there
- check that this derivative is not zero
- report the reciprocal

**Prohibited shortcuts.**
- none recorded in this record

**Multi-skill extensions.**
- none recorded in this record

## Family ivt-existence [verified]

1 archetype(s): BC-QA-01011.

### BC-QA-01011 Existence of a solution argued from the Intermediate Value Theorem

Evidence tag: verified. Scope: shared. Primary unit: BC-UNIT-01. Units: BC-UNIT-01. Sources: ced:53, sg-25:12.

**Description.** A function known to be continuous or differentiable is given by a table, a graph, or a rule, and the response argues that the function attains a stated value somewhere in an interval.

**Concepts and skills required.** BC-SKL-01064, BC-SKL-01065, BC-SKL-01066, BC-SKL-01067, BC-SKL-01068

**Prerequisites.** BC-PRQ-01010, BC-PRQ-01008

**Typical wording.**
- Must there be a value in the stated open interval at which the function equals the given number? Justify your answer.

**Common givens.**
- none recorded in this record

**What is produced.**
- none recorded in this record

**Representations.** BC-REP-03 (Numerical table), BC-REP-05 (Contextual model), BC-REP-02 (Graphical)

**Calculator status.** no_calculator

**Multipart structure.** Typically one part of a multipart free response question.

**Scoring pattern.** One point is earned for stating that the function is continuous because it is differentiable or equivalent, and a bare statement that the function is continuous without that justification does not earn it; a second point requires the straddling inequality, a statement of continuity, and an affirmative answer, and the theorem need not be named although a named theorem must be the correct one (sg-25:12). The second point is available whether or not the first was earned.

**Scoring point types.** none recorded. Point type definitions are in [../scoring/point-taxonomy.md](../scoring/point-taxonomy.md).

**Common distractors.**
- asserting continuity without a reason
- using the endpoints in the wrong order so the target is not between them
- claiming a unique solution
- naming a different theorem
- locating a value rather than arguing existence

**Wrong approaches.**
- none recorded in this record; see ../misconceptions/error-to-concept-map.md

**Misconceptions.** BC-MIS-01015, BC-MIS-01016

**Variants.** 4 recorded: BC-QV-01011-01, BC-QV-01011-02, BC-QV-01011-03, BC-QV-01011-04

**Official examples notes.** 2025 Q3(B)

**Invariant structure.** The continuity hypothesis must be established from a stated property rather than assumed, the target value must be shown to lie between two attained values, and the conclusion asserts existence without locating the input.

**Safe variables.**
- the modelled quantity
- the target value
- the endpoints of the interval
- the units

**Difficulty variables.**
- whether continuity must be deduced from differentiability
- whether the straddling pair must be chosen from a table
- whether the theorem must be named
- whether the answer must be phrased as a yes or no decision

Mapped difficulty factors: BC-DF-03 (Unusual representation), BC-DF-09 (Theorem recognition), BC-DF-14 (Missing or implicit given)

**Expected solution path.**
- state that the function is continuous and give the reason
- display the two attained values that straddle the target
- state that the target lies between them
- conclude that at least one input in the open interval gives the target value

**Prohibited shortcuts.**
- none recorded in this record

**Multi-skill extensions.**
- none recorded in this record

## Family lhospital-limit [verified]

1 archetype(s): BC-QA-04009.

### BC-QA-04009 Limit of an indeterminate form with L'Hospital's rule

Evidence tag: verified. Scope: shared. Primary unit: BC-UNIT-04. Units: BC-UNIT-04. Sources: ced:93, ced:84, sg-23:14, cr-23:14, cr-23:15.

**Description.** A limit of a quotient is supplied, often with one function known only through given properties, and the response establishes the indeterminate form and applies the rule.

**Concepts and skills required.** BC-SKL-04033, BC-SKL-04034, BC-SKL-04035, BC-SKL-04036, BC-SKL-04037, BC-SKL-04038

**Prerequisites.** BC-PRQ-04008

**Typical wording.**
- find the value of the stated limit, or show that it does not exist, and justify the answer

**Common givens.**
- none recorded in this record

**What is produced.**
- none recorded in this record

**Representations.** BC-REP-01 (Symbolic (analytical) expression), BC-REP-02 (Graphical)

**Calculator status.** no_calculator

**Multipart structure.** One part of a graphical analysis free response question.

**Scoring pattern.** The 2023 rubric awards one point for presenting two separate limits for the numerator and the denominator, one for applying the rule by presenting at least one correct derivative in the limit of a ratio of derivatives, and one for the correct answer with supporting work; a response that presents a limit explicitly equal to zero over zero does not earn the first point (sg-23:14).

**Scoring point types.** none recorded. Point type definitions are in [../scoring/point-taxonomy.md](../scoring/point-taxonomy.md).

**Common distractors.**
- the quotient written explicitly equal to zero over zero
- the quotient rule applied instead of separate derivatives
- the rule applied with no check of the form
- an incorrect derivative of the numerator when it contains an unknown function

**Wrong approaches.**
- none recorded in this record; see ../misconceptions/error-to-concept-map.md

**Misconceptions.** BC-MIS-04014, BC-MIS-04015, BC-MIS-04016

**Variants.** 3 recorded: BC-QV-04009-01, BC-QV-04009-02, BC-QV-04009-03

**Official examples notes.** 2023 Q4(c)

**Invariant structure.** The hypothesis has to be established before the rule is used, and it is established by presenting the limit of the numerator and the limit of the denominator as two separate statements; the conclusion is the limit of the quotient of the two derivatives, which is not the derivative of the quotient.

**Safe variables.**
- the functions in the quotient
- the point approached
- whether the form is zero over zero or infinity over infinity
- the way the unknown function is supplied

**Difficulty variables.**
- whether one function is supplied only as a graph or through stated values
- whether differentiability must be used to evaluate a limit in the numerator
- whether the rule must be applied more than once
- whether the answer must be justified as well as produced

Mapped difficulty factors: BC-DF-03 (Unusual representation), BC-DF-10 (Required justification)

**Expected solution path.**
- evaluate the limit of the numerator, using continuity where the function is known to be differentiable
- evaluate the limit of the denominator
- state that the form is indeterminate
- differentiate numerator and denominator separately
- evaluate the resulting limit

**Prohibited shortcuts.**
- none recorded in this record

**Multi-skill extensions.**
- none recorded in this record

## Family limit-algebraic-rewrite [single-source]

1 archetype(s): BC-QA-01004.

### BC-QA-01004 Indeterminate limit resolved by algebraic rewriting

Evidence tag: single-source. Scope: shared. Primary unit: BC-UNIT-01. Units: BC-UNIT-01. Sources: ced:43, sg-23:14.

**Description.** A quotient that gives zero over zero under substitution is presented and the response rewrites it into an equivalent form and evaluates the limit.

**Concepts and skills required.** BC-SKL-01024, BC-SKL-01025, BC-SKL-01026, BC-SKL-01027, BC-SKL-01028

**Prerequisites.** BC-PRQ-01001, BC-PRQ-01002, BC-PRQ-01007

**Typical wording.**
- Find the value of the given limit, or show that it does not exist.

**Common givens.**
- none recorded in this record

**What is produced.**
- none recorded in this record

**Representations.** BC-REP-01 (Symbolic (analytical) expression)

**Calculator status.** no_calculator

**Multipart structure.** Typically a single multiple choice item or one part of a larger question.

**Scoring pattern.** A response that presents a limit explicitly set equal to zero over zero does not earn the point for identifying the form; the form is established by presenting the two limits separately (sg-23:14). Remaining points are for the rewriting and for the value.

**Scoring point types.** none recorded. Point type definitions are in [../scoring/point-taxonomy.md](../scoring/point-taxonomy.md).

**Common distractors.**
- reporting zero because the numerator tends to zero
- reporting that the limit does not exist on seeing zero over zero
- cancelling a term rather than a factor
- dropping the sign introduced by the conjugate

**Wrong approaches.**
- none recorded in this record; see ../misconceptions/error-to-concept-map.md

**Misconceptions.** BC-MIS-01006, BC-MIS-01007

**Variants.** 4 recorded: BC-QV-01004-01, BC-QV-01004-02, BC-QV-01004-03, BC-QV-01004-04

**Official examples notes.** 2023 Q4(c) treats the same indeterminate form through L'Hospital's rule rather than algebraic rewriting

**Invariant structure.** Substitution produces zero over zero, the rewriting step is available without calculus, and the rewritten expression agrees with the original for all inputs near the target other than the target itself.

**Safe variables.**
- the specific polynomial, radical, or trigonometric expression
- the target input
- the variable name

**Difficulty variables.**
- factoring against conjugate against complex fraction against identity
- whether the factor to be divided out is repeated
- whether the target is a boundary of a piecewise rule
- whether the response must state the indeterminate form explicitly

Mapped difficulty factors: BC-DF-02 (Prerequisite depth), BC-DF-10 (Required justification), BC-DF-17 (Case splitting at a boundary)

**Expected solution path.**
- substitute and observe the indeterminate form
- rewrite the expression into an equivalent form
- divide out the common factor or simplify
- evaluate the simplified expression at the target

**Prohibited shortcuts.**
- none recorded in this record

**Multi-skill extensions.**
- none recorded in this record

## Family limit-by-theorems [inferred]

1 archetype(s): BC-QA-01003.

### BC-QA-01003 Limit evaluated by limit theorems from given limits or tabulated values

Evidence tag: inferred. Scope: shared. Primary unit: BC-UNIT-01. Units: BC-UNIT-01. Sources: ced:42.

**Description.** The limits of two functions at a point are supplied and the response evaluates the limit of a sum, difference, product, quotient, or composite built from them.

**Concepts and skills required.** BC-SKL-01018, BC-SKL-01019, BC-SKL-01020, BC-SKL-01022

**Prerequisites.** BC-PRQ-06005

**Typical wording.**
- Given the stated limits of f and g at the named input, find the limit of the indicated combination.

**Common givens.**
- none recorded in this record

**What is produced.**
- none recorded in this record

**Representations.** BC-REP-01 (Symbolic (analytical) expression), BC-REP-03 (Numerical table)

**Calculator status.** no_calculator

**Multipart structure.** Typically a single multiple choice item.

**Scoring pattern.** One point for the value, with the denominator condition expected in a justified response. No official free response part in 2023 to 2025 assesses this task in isolation.

**Scoring point types.** none recorded. Point type definitions are in [../scoring/point-taxonomy.md](../scoring/point-taxonomy.md).

**Common distractors.**
- applying the quotient theorem when the denominator limit is zero
- composing in the wrong order
- adding when a product is requested
- asserting that a limit of a quotient is the quotient of the function values

**Wrong approaches.**
- none recorded in this record; see ../misconceptions/error-to-concept-map.md

**Misconceptions.** BC-MIS-01005

**Variants.** 3 recorded: BC-QV-01003-01, BC-QV-01003-02, BC-QV-01003-03

**Official examples notes.** none in 2023 to 2025 [inferred]

**Invariant structure.** The individual limits are given rather than computed, and the task is the correct selection and application of the limit theorem, including the denominator condition for a quotient.

**Safe variables.**
- the names of the functions
- the target input
- which combination is requested

**Difficulty variables.**
- whether the denominator limit is zero
- whether a composite is involved
- whether one of the supplied limits is one sided
- whether the answer must be justified by naming the theorem

Mapped difficulty factors: BC-DF-09 (Theorem recognition), BC-DF-10 (Required justification), BC-DF-14 (Missing or implicit given)

**Expected solution path.**
- record the supplied limits
- identify the combination requested
- check the denominator condition when a quotient is requested
- apply the theorem and report the value

**Prohibited shortcuts.**
- none recorded in this record

**Multi-skill extensions.**
- none recorded in this record

## Family limit-from-graph [inferred]

1 archetype(s): BC-QA-01001.

### BC-QA-01001 Limit estimated from a graph including one sided values

Evidence tag: inferred. Scope: shared. Primary unit: BC-UNIT-01. Units: BC-UNIT-01. Sources: ced:40, ced:47.

**Description.** A graph of a function with one or more breaks is given and the response reports two sided and one sided limits and function values at named inputs, or states that a limit does not exist.

**Concepts and skills required.** BC-SKL-01009, BC-SKL-01010, BC-SKL-01011, BC-SKL-01012, BC-SKL-01013, BC-SKL-01008

**Prerequisites.** BC-PRQ-06005, BC-PRQ-01003

**Typical wording.**
- Using the graph of f shown, find the stated limits or explain why a limit does not exist.

**Common givens.**
- none recorded in this record

**What is produced.**
- none recorded in this record

**Representations.** BC-REP-02 (Graphical), BC-REP-01 (Symbolic (analytical) expression)

**Calculator status.** no_calculator

**Multipart structure.** Typically a single multiple choice item or one part of a larger question.

**Scoring pattern.** Reading points are awarded per requested value, with a separate point for a stated reason when nonexistence must be justified. No official free response part in 2023 to 2025 assesses this task in isolation, so the pattern is drawn from the CED description of the topic.

**Scoring point types.** none recorded. Point type definitions are in [../scoring/point-taxonomy.md](../scoring/point-taxonomy.md).

**Common distractors.**
- reporting the plotted function value as the limit
- reporting one of the two one sided values as the two sided limit
- answering that the limit is the open circle height when a closed point sits elsewhere
- answering that the limit does not exist merely because the function is undefined there

**Wrong approaches.**
- none recorded in this record; see ../misconceptions/error-to-concept-map.md

**Misconceptions.** BC-MIS-01001, BC-MIS-01002, BC-MIS-01003

**Variants.** 3 recorded: BC-QV-01001-01, BC-QV-01001-02, BC-QV-01001-03

**Official examples notes.** none in 2023 to 2025 [inferred]

**Invariant structure.** The graph carries at least one input where the limit and the function value differ and at least one input where the one sided limits differ; every requested value is read from the picture without computation.

**Safe variables.**
- the shape of the curve
- the names of the inputs
- the number of breaks
- the labelling of the axes

**Difficulty variables.**
- whether a removable and a jump break appear on the same graph
- whether the function value at a break is marked
- whether a nonexistence answer must be justified
- whether an infinite branch is included

Mapped difficulty factors: BC-DF-03 (Unusual representation), BC-DF-10 (Required justification)

**Expected solution path.**
- locate the named input on the horizontal axis
- read the output approached from the left
- read the output approached from the right
- compare the two and report the limit or its nonexistence
- read the plotted function value separately when it is asked for

**Prohibited shortcuts.**
- none recorded in this record

**Multi-skill extensions.**
- none recorded in this record

## Family limit-from-table [inferred]

1 archetype(s): BC-QA-01002.

### BC-QA-01002 Limit estimated from a table of values

Evidence tag: inferred. Scope: shared. Primary unit: BC-UNIT-01. Units: BC-UNIT-01. Sources: ced:41.

**Description.** Selected values of a function at inputs approaching a target from both sides are tabulated and the response reports the estimated limit, or a one sided estimate, from the table.

**Concepts and skills required.** BC-SKL-01015, BC-SKL-01016, BC-SKL-01017

**Prerequisites.** BC-PRQ-06005

**Typical wording.**
- Selected values of f are given in the table. Estimate the stated limit or explain why the table does not determine it.

**Common givens.**
- none recorded in this record

**What is produced.**
- none recorded in this record

**Representations.** BC-REP-03 (Numerical table)

**Calculator status.** either

**Multipart structure.** Typically a single multiple choice item.

**Scoring pattern.** One point for the estimate, with a separate point when an explanation of the limitation of a table is demanded. No official free response part in 2023 to 2025 assesses this task in isolation.

**Scoring point types.** none recorded. Point type definitions are in [../scoring/point-taxonomy.md](../scoring/point-taxonomy.md).

**Common distractors.**
- reading the output at the row nearest the target as the limit
- averaging the two nearest outputs
- reporting a value the table only approaches on one side
- treating an estimate as an exact value

**Wrong approaches.**
- none recorded in this record; see ../misconceptions/error-to-concept-map.md

**Misconceptions.** BC-MIS-01004

**Variants.** 3 recorded: BC-QV-01002-01, BC-QV-01002-02, BC-QV-01002-03

**Official examples notes.** none in 2023 to 2025 [inferred]

**Invariant structure.** The tabulated inputs approach the target from both sides without reaching it, and the outputs are given to a fixed number of decimal places so that the estimate is read rather than computed exactly.

**Safe variables.**
- the function being tabulated
- the target input
- the number of rows
- the precision of the outputs

**Difficulty variables.**
- whether the two sides agree
- whether only one side is tabulated
- whether the table is deliberately inconclusive
- whether units are demanded

Mapped difficulty factors: BC-DF-03 (Unusual representation), BC-DF-16 (Units and labelling demand)

**Expected solution path.**
- identify the rows approaching from the left
- identify the rows approaching from the right
- state the value the outputs approach on each side
- report the estimate or state that the table does not settle the question

**Prohibited shortcuts.**
- none recorded in this record

**Multi-skill extensions.**
- none recorded in this record

## Family logistic-model [inferred]

1 archetype(s): BC-QA-07009.

### BC-QA-07009 Logistic model interpreted without solving

Evidence tag: inferred. Scope: BC_only. Primary unit: BC-UNIT-07. Units: BC-UNIT-07. Sources: ced:145.

**Description.** A logistic differential equation and an initial condition are given and the response must state the carrying capacity, the limiting value, and the quantity at which the change is fastest.

**Concepts and skills required.** BC-SKL-07039, BC-SKL-07040, BC-SKL-07041, BC-SKL-07042, BC-SKL-07043

**Prerequisites.** BC-PRQ-07003, BC-PRQ-05001

**Typical wording.**
- the quantity is modelled by the given logistic differential equation with the given initial value; find the limit of the quantity as the independent variable grows without bound, and the value of the quantity when it is changing fastest

**Common givens.**
- a logistic differential equation
- an initial value strictly between zero and the carrying capacity

**What is produced.**
- the carrying capacity
- the limiting value
- the fastest change value
- an interpretation

**Representations.** BC-REP-06 (Differential equation), BC-REP-05 (Contextual model), BC-REP-04 (Verbal description)

**Calculator status.** either

**Multipart structure.** One or two parts of a multipart free response question, or a single multiple choice item.

**Scoring pattern.** Scored as reasoning from the equation: a point for the value and a point for the reason drawn from the equation rather than from a solved formula, in the shape the CED prescribes for interpreting the model without solving (ced:145). A response that solves the equation and then reports the limit answers a harder question than the one asked and risks the reason point in the way the Chief Reader records describe (BC-ERR-99035).

**Scoring point types.** none recorded. Point type definitions are in [../scoring/point-taxonomy.md](../scoring/point-taxonomy.md).

**Common distractors.**
- reporting the carrying capacity as the fastest change value
- reporting the initial value as the limit
- solving the equation before answering
- using the wrong zero of the right side

**Wrong approaches.**
- separating the logistic equation with partial fractions when only the limit was asked for

**Misconceptions.** BC-MIS-07024, BC-MIS-07025, BC-MIS-07026, BC-MIS-07027

**Variants.** 3 recorded: BC-QV-07009-01, BC-QV-07009-02, BC-QV-07009-03

**Official examples notes.** none in 2023 to 2025

**Invariant structure.** Every answer comes from the equation and the initial condition alone; the equation is never solved, and the right side is a quadratic in the dependent variable with zeros at zero and at the carrying capacity.

**Safe variables.**
- the modelled population
- the units
- the letters used
- the numerical carrying capacity

**Difficulty variables.**
- whether the equation is written with the carrying capacity factored out
- whether the initial value is above or below the carrying capacity
- whether an interpretation with units is demanded

Mapped difficulty factors: BC-DF-02 (Prerequisite depth), BC-DF-05 (Contextual interpretation), BC-DF-16 (Units and labelling demand)

**Expected solution path.**
- read the zeros of the right side
- name the nonzero one as the carrying capacity
- use the sign of the right side and the initial value to state the limit
- maximise the quadratic right side to get half the carrying capacity

**Prohibited shortcuts.**
- none recorded in this record

**Multi-skill extensions.**
- none recorded in this record

## Family mean-value-theorem [verified]

3 archetype(s): BC-QA-05001, BC-QA-05002, BC-QA-08002.

### BC-QA-05001 Mean Value Theorem existence justification on an interval

Evidence tag: verified. Scope: shared. Primary unit: BC-UNIT-05. Units: BC-UNIT-05. Sources: sg-23:3, sg-25:4, frq-23:3, frq-25:3.

**Description.** A function is stated to be differentiable and selected values are supplied; the response must decide whether some interior input has a named instantaneous rate of change and justify the decision.

**Concepts and skills required.** BC-SKL-05001, BC-SKL-05002, BC-SKL-05003, BC-SKL-05004, BC-SKL-05006

**Prerequisites.** BC-PRQ-05008, BC-PRQ-05004

**Typical wording.**
- must there be a value of c in the open interval at which the derivative takes a stated value, and justify the answer
- find the time at which the instantaneous rate of change equals the average rate of change over the stated interval

**Common givens.**
- a differentiable modelled function
- a short table of values
- a closed interval

**What is produced.**
- a yes or no answer
- a statement that continuity follows from differentiability
- the average rate of change
- a named theorem

**Representations.** BC-REP-03 (Numerical table), BC-REP-04 (Verbal description), BC-REP-05 (Contextual model)

**Calculator status.** either

**Multipart structure.** One part of a multipart free response question, worth two points.

**Scoring pattern.** One point for the arithmetic fact that fixes the average rate of change, and one point for the answer with justification. The justification point requires the first point, a statement that the function is continuous because it is differentiable, and an affirmative answer; a reference to the Intermediate Value Theorem forfeits it (sg-23:3). In the 2025 instance the first point was earned by any correct presentation of the average rate of change and the second by the correct solved value with the supporting equation (sg-25:4).

**Scoring point types.** none recorded. Point type definitions are in [../scoring/point-taxonomy.md](../scoring/point-taxonomy.md).

**Common distractors.**
- citing the Intermediate Value Theorem for a claim about the derivative
- asserting the conclusion without the continuity statement
- computing the average of the two endpoint values
- reporting an input outside the open interval

**Wrong approaches.**
- treating the table as a complete description of the function
- solving for c when only existence was asked

**Misconceptions.** BC-MIS-05001, BC-MIS-05002, BC-MIS-05003, BC-MIS-05005

**Variants.** 3 recorded: BC-QV-05001-01, BC-QV-05001-02, BC-QV-05001-03

**Official examples notes.** 2023 Q1(b), 2025 Q1(B)

**Invariant structure.** The hypotheses are handed over as a differentiability statement, two endpoint values determine the average rate of change, and the demand is an existence claim about the derivative rather than a located value.

**Safe variables.**
- the modelled quantity
- the units
- the letters used for the variables
- the endpoint values

**Difficulty variables.**
- whether the endpoint values are equal or merely produce a computable average
- whether the theorem must be named
- whether the function is given by a table, a graph, or a formula
- whether a value of c is also demanded

Mapped difficulty factors: BC-DF-03 (Unusual representation), BC-DF-09 (Theorem recognition), BC-DF-14 (Missing or implicit given)

**Expected solution path.**
- state that differentiability supplies continuity on the closed interval
- compute the average rate of change over the interval
- invoke the Mean Value Theorem
- answer yes and name the interior interval

**Prohibited shortcuts.**
- none recorded in this record

**Multi-skill extensions.**
- none recorded in this record

### BC-QA-05002 Solving for the value the Mean Value Theorem provides

Evidence tag: verified. Scope: shared. Primary unit: BC-UNIT-05. Units: BC-UNIT-05. Sources: sg-25:4, frq-25:3.

**Description.** A function and a closed interval are given and the response must produce the interior input at which the instantaneous rate of change equals the average rate of change.

**Concepts and skills required.** BC-SKL-05003, BC-SKL-05005

**Prerequisites.** BC-PRQ-05008, BC-PRQ-05001

**Typical wording.**
- find the value in the open interval at which the instantaneous rate of change equals the average rate of change over that interval

**Common givens.**
- a function given by a formula
- a closed interval

**What is produced.**
- the average rate of change
- the solved input value

**Representations.** BC-REP-01 (Symbolic (analytical) expression), BC-REP-09 (Calculator-generated numerical result)

**Calculator status.** either

**Multipart structure.** One part of a multipart free response question, or a single multiple choice item.

**Scoring pattern.** One point for using the average rate of change and one point for the answer with supporting work; a bare numerical value with no supporting equation earns neither (sg-25:4).

**Scoring point types.** none recorded. Point type definitions are in [../scoring/point-taxonomy.md](../scoring/point-taxonomy.md).

**Common distractors.**
- reporting the average rate of change itself as the answer
- solving the derivative equal to zero instead
- accepting a solution outside the open interval

**Wrong approaches.**
- differentiating the average rate of change expression

**Misconceptions.** BC-MIS-05003, BC-MIS-05004

**Variants.** 3 recorded: BC-QV-05002-01, BC-QV-05002-02, BC-QV-05002-03

**Official examples notes.** 2025 Q1(B)

**Invariant structure.** The average rate of change is computable from the two endpoint values, the derivative is available symbolically, and the answer is the solution of one equation restricted to the open interval.

**Safe variables.**
- the function rule
- the interval endpoints
- the context

**Difficulty variables.**
- whether the resulting equation is solvable by hand
- whether more than one solution lies inside the interval
- calculator availability

Mapped difficulty factors: BC-DF-06 (Algebraic burden), BC-DF-07 (Calculator workflow)

**Expected solution path.**
- compute the average rate of change
- set the derivative equal to that value
- solve
- discard solutions outside the open interval

**Prohibited shortcuts.**
- none recorded in this record

**Multi-skill extensions.**
- none recorded in this record

### BC-QA-08002 Instantaneous rate set equal to an average rate of change

Evidence tag: verified. Scope: shared. Primary unit: BC-UNIT-08. Units: BC-UNIT-08. Sources: sg-25:4, frq-25:3.

**Description.** The response computes the average rate of change of a modelled quantity over an interval and solves for the time at which the derivative equals that value.

**Concepts and skills required.** BC-SKL-08004, BC-SKL-08003

**Prerequisites.** BC-PRQ-08001

**Typical wording.**
- find the time at which the instantaneous rate of change of the modelled quantity equals its average rate of change over the stated interval, and show the setup

**Common givens.**
- a model function
- its derivative
- a closed interval

**What is produced.**
- an equation
- a solved input value

**Representations.** BC-REP-01 (Symbolic (analytical) expression), BC-REP-09 (Calculator-generated numerical result), BC-REP-05 (Contextual model)

**Calculator status.** calculator

**Multipart structure.** One part of the calculator active free response question.

**Scoring pattern.** Two points: one for using the average rate of change, which several equivalent expressions earn, and one for the answer with the supporting equation; presenting the value of the average rate of change alone as the answer earns neither (sg-25:4).

**Scoring point types.** none recorded. Point type definitions are in [../scoring/point-taxonomy.md](../scoring/point-taxonomy.md).

**Common distractors.**
- the value of the average rate of change reported as the answer
- the average value of the function used in place of the average rate of change

**Wrong approaches.**
- reporting the average rate of change itself as the time

**Misconceptions.** BC-MIS-08001

**Variants.** 2 recorded: BC-QV-08002-01, BC-QV-08002-02

**Official examples notes.** 2025 Q1(B)

**Invariant structure.** A difference quotient of the modelling function over the interval, set equal to the given derivative, solved numerically for one input in the interval.

**Safe variables.**
- the modelled quantity
- the interval
- the form of the model

**Difficulty variables.**
- whether the interval starts where the function is zero, which makes several equivalent expressions acceptable
- whether the derivative is supplied or must be computed

Mapped difficulty factors: BC-DF-03 (Unusual representation)

**Expected solution path.**
- compute the average rate of change over the interval
- set the given derivative equal to that value
- solve numerically on the interval
- report the input to three decimal places

**Prohibited shortcuts.**
- none recorded in this record

**Multi-skill extensions.**
- none recorded in this record

## Family monotonicity-analysis [inferred]

1 archetype(s): BC-QA-05008.

### BC-QA-05008 Intervals of increase or decrease justified by the sign of the derivative

Evidence tag: inferred. Scope: shared. Primary unit: BC-UNIT-05. Units: BC-UNIT-05. Sources: ced:101, sg-25:17, sg-23:14.

**Description.** The response must give the intervals on which a function rises or falls and support them with the sign of its derivative.

**Concepts and skills required.** BC-SKL-05014, BC-SKL-05015, BC-SKL-05016, BC-SKL-05017, BC-SKL-05018

**Prerequisites.** BC-PRQ-05002, BC-PRQ-05003, BC-PRQ-05004

**Typical wording.**
- on what open intervals is the function increasing, and give a reason for the answer

**Common givens.**
- a function or its derivative
- an interval of definition

**What is produced.**
- a union of open intervals
- a reason naming the sign of the derivative

**Representations.** BC-REP-01 (Symbolic (analytical) expression), BC-REP-02 (Graphical), BC-REP-03 (Numerical table)

**Calculator status.** either

**Multipart structure.** One part of a multipart free response question, or a single multiple choice item.

**Scoring pattern.** Intervals and reason score separately, with the reason requiring the sign of the named derivative on the stated interval rather than a restatement of the conclusion; an unnamed referent forfeits the reason (sg-25:17). Scored here by analogy with the concavity part of the same family (sg-23:14).

**Scoring point types.** none recorded. Point type definitions are in [../scoring/point-taxonomy.md](../scoring/point-taxonomy.md).

**Common distractors.**
- reporting closed intervals
- merging two intervals across a break in the domain
- reading increase of the derivative as increase of the function
- offering a bare sign chart with no sentence

**Wrong approaches.**
- testing a single input and generalising

**Misconceptions.** BC-MIS-05010, BC-MIS-05011, BC-MIS-05012, BC-MIS-05013

**Variants.** 3 recorded: BC-QV-05008-01, BC-QV-05008-02, BC-QV-05008-03

**Official examples notes.** none in 2023 to 2025 as a standalone part

**Invariant structure.** The partition points are the critical points and the domain breaks, the answer is a union of open intervals, and the reason must name the derivative of the given function.

**Safe variables.**
- the function rule
- the letters used
- the interval of definition

**Difficulty variables.**
- whether the domain has a break
- whether the derivative changes sign at an undefined point
- whether the given object is the function or its derivative

Mapped difficulty factors: BC-DF-12 (Sign and direction handling), BC-DF-17 (Case splitting at a boundary)

**Expected solution path.**
- find the zeros and undefined points of the derivative
- determine the sign on each piece
- write the intervals
- state the reason naming the derivative

**Prohibited shortcuts.**
- none recorded in this record

**Multi-skill extensions.**
- none recorded in this record

## Family motion-by-accumulation [verified]

2 archetype(s): BC-QA-04010, BC-QA-08003.

### BC-QA-04010 Position recovered from velocity with an initial condition

Evidence tag: verified. Scope: shared. Primary unit: BC-UNIT-04. Units: BC-UNIT-04. Sources: ced:88, crabbc-25:20, crabbc-25:22.

**Description.** A velocity function and a position at one time are supplied, and the response finds the position at another time.

**Concepts and skills required.** BC-SKL-04006, BC-SKL-04011

**Prerequisites.** BC-PRQ-04008

**Typical wording.**
- find the position of the particle at the stated time, showing the work that leads to the answer

**Common givens.**
- none recorded in this record

**What is produced.**
- none recorded in this record

**Representations.** BC-REP-01 (Symbolic (analytical) expression), BC-REP-05 (Contextual model)

**Calculator status.** either

**Multipart structure.** The closing part of a particle motion free response question.

**Scoring pattern.** The 2025 rubric awards one point for a correct integrand, one for the correct antiderivative, and one for incorporating the initial condition and reporting the value; the Chief Reader report records missing differentials and unchanged substitution limits as the common losses (crabbc-25:20, crabbc-25:22).

**Scoring point types.** none recorded. Point type definitions are in [../scoring/point-taxonomy.md](../scoring/point-taxonomy.md).

**Common distractors.**
- the displacement reported where the position was requested
- the initial condition omitted
- the speed integrated in place of the velocity
- the limits of integration left unchanged after a substitution

**Wrong approaches.**
- none recorded in this record; see ../misconceptions/error-to-concept-map.md

**Misconceptions.** BC-MIS-04004, BC-MIS-04005

**Variants.** 2 recorded: BC-QV-04010-01, BC-QV-04010-02

**Official examples notes.** 2025 AB Q5 part D as described in the Chief Reader report

**Invariant structure.** Position is recovered from velocity by accumulation over the interval and the initial position is added; the antidifferentiation itself belongs to Unit 6 while the motion reading of the quantities belongs here.

**Safe variables.**
- the velocity formula
- the initial time and position
- the target time

**Difficulty variables.**
- whether the antiderivative needs a substitution
- whether the initial condition is given at a time other than zero
- whether the displacement or the position is requested

Mapped difficulty factors: BC-DF-06 (Algebraic burden), BC-DF-11 (Unfamiliar surface presentation), BC-DF-14 (Missing or implicit given)

**Expected solution path.**
- write the position as the initial position plus the accumulated change in position
- evaluate the definite integral of the velocity
- add the initial position
- report the position

**Prohibited shortcuts.**
- none recorded in this record

**Multi-skill extensions.**
- none recorded in this record

### BC-QA-08003 Rectilinear motion analysed with definite integrals

Evidence tag: verified. Scope: shared. Primary unit: BC-UNIT-08. Units: BC-UNIT-08. Sources: ced:153, sg-24:6, sg-24:7.

**Description.** A velocity function is given for a particle on a line, and the response produces displacement, total distance, or a position value from an initial condition.

**Concepts and skills required.** BC-SKL-08006, BC-SKL-08007, BC-SKL-08008, BC-SKL-08009, BC-SKL-08010, BC-SKL-08011

**Prerequisites.** BC-PRQ-08003

**Typical wording.**
- find the total distance travelled by the particle over the stated time interval and show the setup
- find the position of the particle at the later time

**Common givens.**
- a velocity function or graph
- an initial position
- a time interval

**What is produced.**
- a definite integral
- a numerical value with units

**Representations.** BC-REP-01 (Symbolic (analytical) expression), BC-REP-02 (Graphical), BC-REP-05 (Contextual model)

**Calculator status.** either

**Multipart structure.** Usually two or three parts of a multipart question, or a single multiple choice item.

**Scoring pattern.** The integral of speed earns a setup point and the decimal earns the answer point, the pattern the planar analogue uses at sg-24:6; a position value earns a point for the definite integral, a point for using the initial condition, and a point for the answer (sg-24:7).

**Scoring point types.** none recorded. Point type definitions are in [../scoring/point-taxonomy.md](../scoring/point-taxonomy.md).

**Common distractors.**
- the displacement offered where total distance is asked
- the integral of velocity without the initial position
- the value of velocity at an endpoint

**Wrong approaches.**
- integrating velocity and taking the absolute value of the result
- adding the absolute values of the endpoint velocities

**Misconceptions.** BC-MIS-08004, BC-MIS-08006

**Variants.** 3 recorded: BC-QV-08003-01, BC-QV-08003-02, BC-QV-08003-03

**Official examples notes.** no rectilinear part in the 2023 to 2025 BC free response questions; the planar analogue appears at 2024 Q2(b) and 2024 Q2(c)

**Invariant structure.** One velocity function on a time interval; the requested quantity fixes the integrand as velocity, as the absolute value of velocity, or as velocity added to a known initial position.

**Safe variables.**
- the moving object
- the units of position and time
- the letters used

**Difficulty variables.**
- whether velocity changes sign inside the interval
- whether the question asks for displacement or total distance
- whether an initial condition must be used
- graph versus formula presentation

Mapped difficulty factors: BC-DF-03 (Unusual representation), BC-DF-09 (Theorem recognition), BC-DF-12 (Sign and direction handling), BC-DF-14 (Missing or implicit given), BC-DF-17 (Case splitting at a boundary)

**Expected solution path.**
- classify the requested quantity
- write the matching definite integral
- use the initial condition when a position value is requested
- evaluate and report with units

**Prohibited shortcuts.**
- none recorded in this record

**Multi-skill extensions.**
- none recorded in this record

## Family motion-by-differentiation [verified]

2 archetype(s): BC-QA-04003, BC-QA-04004.

### BC-QA-04003 Straight-line motion with velocity, acceleration, and speed

Evidence tag: verified. Scope: shared. Primary unit: BC-UNIT-04. Units: BC-UNIT-04. Sources: ced:88, cr-22:20, cr-22:21, crabbc-25:20, crabbc-25:22.

**Description.** A particle moves on a line with position or velocity supplied as a function of time, and the response produces velocity, acceleration, or speed at an instant and decides whether the speed is increasing.

**Concepts and skills required.** BC-SKL-04006, BC-SKL-04007, BC-SKL-04008, BC-SKL-04010

**Prerequisites.** BC-PRQ-04005, BC-PRQ-04008

**Typical wording.**
- find the velocity of the particle at the stated time
- is the speed of the particle increasing, decreasing, or neither at the stated time, and give a reason

**Common givens.**
- none recorded in this record

**What is produced.**
- none recorded in this record

**Representations.** BC-REP-01 (Symbolic (analytical) expression), BC-REP-05 (Contextual model)

**Calculator status.** either

**Multipart structure.** Two or three parts of a particle motion free response question.

**Scoring pattern.** The 2025 rubric awards the speed point only when the response states the sign of the velocity and draws the conclusion, and the Chief Reader report records that quoting the rule without applying it to the particular problem does not suffice (crabbc-25:20, crabbc-25:22, crabbc-25:23); the 2022 report records deciding speed from the acceleration alone as the most common misconception on that question (cr-22:21).

**Scoring point types.** none recorded. Point type definitions are in [../scoring/point-taxonomy.md](../scoring/point-taxonomy.md).

**Common distractors.**
- the speed decided from the sign of the acceleration alone
- speed reported as a negative number
- the position value reported where a velocity was asked for
- a general rule quoted without being applied to the given particle

**Wrong approaches.**
- none recorded in this record; see ../misconceptions/error-to-concept-map.md

**Misconceptions.** BC-MIS-04004, BC-MIS-04005, BC-MIS-04006

**Variants.** 4 recorded: BC-QV-04003-01, BC-QV-04003-02, BC-QV-04003-03, BC-QV-04003-04

**Official examples notes.** 2022 AB Q6(a) and (b), 2025 AB Q5 parts A and C, as described in the Chief Reader reports

**Invariant structure.** Velocity is the derivative of position and acceleration is the derivative of velocity; the speed question is settled by comparing the signs of velocity and acceleration at the instant, and never by the sign of the acceleration alone.

**Safe variables.**
- the particle's name
- the formula supplied
- the instant chosen
- whether position or velocity is the given function

**Difficulty variables.**
- whether the given function is position or velocity
- whether one of the two signs is supplied rather than computed
- whether the differentiation needs the product or chain rule
- whether the conclusion must be applied to the particular problem rather than stated as a general rule

Mapped difficulty factors: BC-DF-12 (Sign and direction handling), BC-DF-13 (Reversed reasoning direction)

**Expected solution path.**
- differentiate the supplied function as many times as the question needs
- evaluate the velocity and the acceleration at the instant
- compare their signs
- state the conclusion about the speed for that particle at that instant

**Prohibited shortcuts.**
- none recorded in this record

**Multi-skill extensions.**
- none recorded in this record

### BC-QA-04004 Direction of motion and sign analysis over an interval

Evidence tag: verified. Scope: shared. Primary unit: BC-UNIT-04. Units: BC-UNIT-04. Sources: ced:88, crabbc-25:20, crabbc-25:22, crabbc-25:23.

**Description.** The response determines when a particle moves in a stated direction, when it is at rest, or when two particles move in opposite directions, from the sign of velocity across a whole interval.

**Concepts and skills required.** BC-SKL-04009, BC-SKL-04011, BC-SKL-04012

**Prerequisites.** BC-PRQ-04009

**Typical wording.**
- find the intervals of time during which the particles are moving in opposite directions

**Common givens.**
- none recorded in this record

**What is produced.**
- none recorded in this record

**Representations.** BC-REP-01 (Symbolic (analytical) expression), BC-REP-02 (Graphical), BC-REP-04 (Verbal description)

**Calculator status.** either

**Multipart structure.** One part of a particle motion free response question, ordinarily the hardest.

**Scoring pattern.** The 2025 rubric attaches one point to considering the sign of a velocity, one to the analysis for one particle, and one to the analysis for both and the resulting interval; the Chief Reader report records that responses failing to address the entire stated interval did not earn the last two points, whose mean scores were 0.04 and 0.03 (crabbc-25:20, crabbc-25:22).

**Scoring point types.** none recorded. Point type definitions are in [../scoring/point-taxonomy.md](../scoring/point-taxonomy.md).

**Common distractors.**
- integer inputs sampled instead of the equation being solved
- a sign chart presented with no stated reading
- an interval reported that covers only part of the prompt's interval
- direction reported from the sign of the position

**Wrong approaches.**
- none recorded in this record; see ../misconceptions/error-to-concept-map.md

**Misconceptions.** BC-MIS-04005, BC-MIS-04017

**Variants.** 3 recorded: BC-QV-04004-01, BC-QV-04004-02, BC-QV-04004-03

**Official examples notes.** 2025 AB Q5 part B as described in the Chief Reader report

**Invariant structure.** The zeros of the velocity split the interval, the sign of the velocity is constant between consecutive zeros, and the conclusion must cover the entire interval named in the prompt rather than sampled instants.

**Safe variables.**
- the velocity formula
- the interval
- the number of particles
- the names of the particles

**Difficulty variables.**
- whether a zero of the velocity is not an integer
- whether two particles must be compared
- whether the analysis must be communicated in words as well as in a chart
- whether the velocity changes sign more than once

Mapped difficulty factors: BC-DF-05 (Contextual interpretation), BC-DF-12 (Sign and direction handling), BC-DF-17 (Case splitting at a boundary)

**Expected solution path.**
- solve the equation velocity equal to zero on the interval
- determine the sign of the velocity on each resulting subinterval
- state in words what each sign means for the direction of motion
- combine the two analyses when two particles are compared

**Prohibited shortcuts.**
- none recorded in this record

**Multi-skill extensions.**
- none recorded in this record

## Family notation-translation [inferred]

1 archetype(s): BC-QA-02012.

### BC-QA-02012 Derivative notation read or converted

Evidence tag: inferred. Scope: shared. Primary unit: BC-UNIT-02. Units: BC-UNIT-02. Sources: ced:61.

**Description.** A derivative is presented in one notation and the response writes it in another or states what it denotes.

**Concepts and skills required.** BC-SKL-02010, BC-SKL-02011, BC-SKL-02004

**Prerequisites.** BC-PRQ-02004

**Typical wording.**
- Which of the given expressions denotes the same quantity as the expression shown?

**Common givens.**
- none recorded in this record

**What is produced.**
- none recorded in this record

**Representations.** BC-REP-01 (Symbolic (analytical) expression), BC-REP-04 (Verbal description), BC-REP-02 (Graphical), BC-REP-03 (Numerical table)

**Calculator status.** no_calculator

**Multipart structure.** Typically a single multiple choice item.

**Scoring pattern.** One point for the conversion.

**Scoring point types.** none recorded. Point type definitions are in [../scoring/point-taxonomy.md](../scoring/point-taxonomy.md).

**Common distractors.**
- reading the Leibniz form as a quotient of two quantities
- losing the point of evaluation when converting
- changing the independent variable
- confusing the derivative function with its value at a point

**Wrong approaches.**
- none recorded in this record; see ../misconceptions/error-to-concept-map.md

**Misconceptions.** BC-MIS-02015

**Variants.** 3 recorded: BC-QV-02012-01, BC-QV-02012-02, BC-QV-02012-03

**Official examples notes.** none in 2023 to 2025 as a standalone part [inferred]

**Invariant structure.** The task is the notation itself, so the underlying function may be left unspecified, and the independent variable must be identified from the notation rather than assumed.

**Safe variables.**
- the function name
- the variable names
- which notation is supplied

**Difficulty variables.**
- prime against Leibniz against y prime
- whether a value at a point is involved
- whether the notation carries a context with units
- whether a second derivative is involved

Mapped difficulty factors: BC-DF-04 (Notation complexity), BC-DF-05 (Contextual interpretation), BC-DF-16 (Units and labelling demand)

**Expected solution path.**
- identify the function and the independent variable from the supplied notation
- state what the expression denotes
- write the equivalent expression in the requested notation

**Prohibited shortcuts.**
- none recorded in this record

**Multi-skill extensions.**
- none recorded in this record

## Family optimisation [inferred]

1 archetype(s): BC-QA-05011.

### BC-QA-05011 Applied optimisation with model setup, domain, and verification

Evidence tag: inferred. Scope: shared. Primary unit: BC-UNIT-05. Units: BC-UNIT-05. Sources: ced:108, ced:109, sg-25:19, sg-23:2.

**Description.** A situation is described and the response must build a one variable objective, find the extremum on the contextual domain, verify it, and interpret it.

**Concepts and skills required.** BC-SKL-05049, BC-SKL-05050, BC-SKL-05051, BC-SKL-05052, BC-SKL-05053, BC-SKL-05054, BC-SKL-05055, BC-SKL-05056, BC-SKL-05057

**Prerequisites.** BC-PRQ-05005, BC-PRQ-05003

**Typical wording.**
- find the dimensions that make the described quantity as large as possible, and justify that the value found is the maximum
- using correct units, state the largest value the modelled quantity attains on the stated interval

**Common givens.**
- a verbal situation or a diagram
- a fixed total or a geometric relation
- a contextual range

**What is produced.**
- the objective in one variable
- the domain
- the critical point
- the verification
- the interpreted value

**Representations.** BC-REP-01 (Symbolic (analytical) expression), BC-REP-05 (Contextual model), BC-REP-08 (Geometric diagram)

**Calculator status.** either

**Multipart structure.** A multipart free response question, or a multiple choice item that supplies the reduced objective.

**Scoring pattern.** Separate points for the setup, for the derivative condition, for the verification that the critical point gives the extremum, and for the interpreted value with units. A verification that argues only locally does not satisfy a demand for the extremum on a closed contextual domain (sg-25:19), and an interpretation that omits the units or the interval is incomplete (sg-23:2).

**Scoring point types.** none recorded. Point type definitions are in [../scoring/point-taxonomy.md](../scoring/point-taxonomy.md).

**Common distractors.**
- optimising the constraint instead of the objective
- taking the domain as all real numbers
- stopping at the critical point with no verification
- reporting the dimensions when the optimal value was asked for

**Wrong approaches.**
- substituting a numerical value before differentiating

**Misconceptions.** BC-MIS-05015, BC-MIS-05027, BC-MIS-05028, BC-MIS-05029, BC-MIS-05030

**Variants.** 3 recorded: BC-QV-05011-01, BC-QV-05011-02, BC-QV-05011-03

**Official examples notes.** none in 2023 to 2025 as a standalone part

**Invariant structure.** A constraint reduces two variables to one, the domain comes from the context, and the verification step is scored separately from the location of the critical point.

**Safe variables.**
- the modelled quantity
- the units
- the shape in the diagram
- the fixed total

**Difficulty variables.**
- whether the contextual domain is closed
- whether the constraint is linear or geometric
- whether a verification is demanded explicitly
- whether an interpretation sentence is demanded

Mapped difficulty factors: BC-DF-02 (Prerequisite depth), BC-DF-05 (Contextual interpretation), BC-DF-13 (Reversed reasoning direction)

**Expected solution path.**
- define the variables and write the objective
- substitute the constraint
- state the domain
- differentiate and solve
- verify the extremum on that domain
- report the value with units

**Prohibited shortcuts.**
- none recorded in this record

**Multi-skill extensions.**
- none recorded in this record

## Family parameter-for-continuity [inferred]

1 archetype(s): BC-QA-01008.

### BC-QA-01008 Parameter solved so that a piecewise function is continuous

Evidence tag: inferred. Scope: shared. Primary unit: BC-UNIT-01. Units: BC-UNIT-01. Sources: ced:50.

**Description.** A piecewise rule containing one or two unknown constants is given and the response determines the constants that make the function continuous.

**Concepts and skills required.** BC-SKL-01051, BC-SKL-01052, BC-SKL-01050, BC-SKL-01053

**Prerequisites.** BC-PRQ-01003

**Typical wording.**
- Find the value or values of the constants for which the given piecewise function is continuous.

**Common givens.**
- none recorded in this record

**What is produced.**
- none recorded in this record

**Representations.** BC-REP-01 (Symbolic (analytical) expression)

**Calculator status.** no_calculator

**Multipart structure.** Typically a single multiple choice item or one part of a larger question.

**Scoring pattern.** One point for the matching equation at each boundary and one for the solution.

**Scoring point types.** none recorded. Point type definitions are in [../scoring/point-taxonomy.md](../scoring/point-taxonomy.md).

**Common distractors.**
- matching only the two limits and ignoring the defined value
- substituting the boundary into the wrong branch
- solving one equation for two unknowns
- reporting a value that makes the branches equal at the wrong input

**Wrong approaches.**
- none recorded in this record; see ../misconceptions/error-to-concept-map.md

**Misconceptions.** BC-MIS-01009

**Variants.** 3 recorded: BC-QV-01008-01, BC-QV-01008-02, BC-QV-01008-03

**Official examples notes.** none in 2023 to 2025 [inferred]

**Invariant structure.** Continuity at each boundary yields exactly one equation, so the number of boundaries at which matching is demanded equals the number of equations available for the unknowns.

**Safe variables.**
- the branch expressions
- the names of the constants
- the boundary inputs

**Difficulty variables.**
- one unknown against two unknowns
- one boundary against two boundaries
- whether the branch expressions are linear
- whether the response must also confirm the function value at the boundary

Mapped difficulty factors: BC-DF-17 (Case splitting at a boundary)

**Expected solution path.**
- evaluate the one sided limit from each branch at the boundary
- set the two expressions equal at the boundary
- include the function value in the equality
- solve for the unknown or solve the system for two unknowns

**Prohibited shortcuts.**
- none recorded in this record

**Multi-skill extensions.**
- none recorded in this record

## Family parametric-calculus [verified]

2 archetype(s): BC-QA-09001, BC-QA-09002.

### BC-QA-09001 Slope of the tangent to a parametric path at a time

Evidence tag: verified. Scope: BC_only. Primary unit: BC-UNIT-09. Units: BC-UNIT-09. Sources: sg-23:7, frq-23:4.

**Description.** A particle moves on a parametric path and the response reports the slope of the tangent line at a given time as a quotient of parametric derivatives.

**Concepts and skills required.** BC-SKL-09001, BC-SKL-09002, BC-SKL-09004, BC-SKL-09005, BC-SKL-09003, BC-SKL-09006

**Prerequisites.** BC-PRQ-09003

**Typical wording.**
- find the slope of the line tangent to the path of the particle at the given time and show the work that leads to the answer

**Common givens.**
- a parametric or vector description of a path
- a time

**What is produced.**
- a quotient of parametric derivatives
- a numerical slope

**Representations.** BC-REP-12 (Parametric equations), BC-REP-01 (Symbolic (analytical) expression), BC-REP-09 (Calculator-generated numerical result)

**Calculator status.** calculator

**Multipart structure.** One part of the calculator active BC free response question, often sharing a part with a position coordinate.

**Scoring pattern.** One point, earned only when the response communicates that dy/dx is dy/dt divided by dx/dt; several presentations earn it, including labelled values of the two derivatives followed by the slope, and an incorrect component imported from an earlier part is accepted when it was declared there (sg-23:7).

**Scoring point types.** none recorded. Point type definitions are in [../scoring/point-taxonomy.md](../scoring/point-taxonomy.md).

**Common distractors.**
- dy/dt alone
- dx/dt divided by dy/dt
- the second derivative

**Wrong approaches.**
- reporting a value with no quotient shown
- using a component derivative that was never declared

**Misconceptions.** BC-MIS-09002, BC-MIS-09003

**Variants.** 3 recorded: BC-QV-09001-01, BC-QV-09001-02, BC-QV-09001-03

**Official examples notes.** 2023 Q2(c)

**Invariant structure.** Two component rates at one parameter value and one quotient, with the quotient structure visible in the response rather than only its value.

**Safe variables.**
- the moving object
- the letters for the components
- the time at which the slope is requested

**Difficulty variables.**
- whether one component is given only through its derivative
- whether the slope is followed by a tangent line
- whether a component derivative must be imported from an earlier part

Mapped difficulty factors: BC-DF-01 (Number of concepts combined), BC-DF-08 (Multi-step dependency)

**Expected solution path.**
- compute dy/dt and dx/dt
- form the quotient
- evaluate at the given time
- report the slope

**Prohibited shortcuts.**
- none recorded in this record

**Multi-skill extensions.**
- none recorded in this record

### BC-QA-09002 Second derivative of a parametric curve

Evidence tag: inferred. Scope: BC_only. Primary unit: BC-UNIT-09. Units: BC-UNIT-09. Sources: ced:172.

**Description.** The response assembles the second derivative of y with respect to x for a parametric curve and evaluates it or reads its sign.

**Concepts and skills required.** BC-SKL-09007, BC-SKL-09008, BC-SKL-09009, BC-SKL-09010

**Prerequisites.** BC-PRQ-06005

**Typical wording.**
- find the second derivative of y with respect to x at the given parameter value, or state the concavity of the curve there

**Common givens.**
- a parametric pair
- a parameter value

**What is produced.**
- a second derivative expression
- a value or a statement of concavity

**Representations.** BC-REP-12 (Parametric equations), BC-REP-01 (Symbolic (analytical) expression)

**Calculator status.** either

**Multipart structure.** One part of a multipart question, or a single multiple choice item.

**Scoring pattern.** A setup point for the assembled expression and an answer point for the value, following the parametric derivative scoring pattern of 2023 (sg-23:7).

**Scoring point types.** none recorded. Point type definitions are in [../scoring/point-taxonomy.md](../scoring/point-taxonomy.md).

**Common distractors.**
- the quotient of the two second parametric derivatives
- the derivative of the slope with respect to the parameter without the second division
- the sign of dy/dt

**Wrong approaches.**
- dividing the second derivative of y by the second derivative of x

**Misconceptions.** BC-MIS-09004

**Variants.** 2 recorded: BC-QV-09002-01, BC-QV-09002-02

**Official examples notes.** no parametric second derivative appears in the 2023 to 2025 BC free response questions

**Invariant structure.** The slope is assembled first, differentiated with respect to the parameter, and divided once more by dx/dt.

**Safe variables.**
- the components
- the parameter value
- the letters used

**Difficulty variables.**
- whether the slope simplifies before the second differentiation
- whether a sign or a value is requested
- whether technology may be used

Mapped difficulty factors: BC-DF-06 (Algebraic burden), BC-DF-07 (Calculator workflow), BC-DF-08 (Multi-step dependency), BC-DF-12 (Sign and direction handling)

**Expected solution path.**
- form dy/dx
- differentiate it with respect to the parameter
- divide by dx/dt
- evaluate or read the sign

**Prohibited shortcuts.**
- none recorded in this record

**Multi-skill extensions.**
- none recorded in this record

## Family parametric-motion [verified]

5 archetype(s): BC-QA-09004, BC-QA-09005, BC-QA-09006, BC-QA-09007, BC-QA-09008.

### BC-QA-09004 Acceleration vector of a particle in planar motion

Evidence tag: verified. Scope: BC_only. Primary unit: BC-UNIT-09. Units: BC-UNIT-09. Sources: sg-23:5, sg-23:6, frq-23:4.

**Description.** The response differentiates each velocity component and reports the acceleration vector at a time with the setup shown.

**Concepts and skills required.** BC-SKL-09015, BC-SKL-09016, BC-SKL-09017, BC-SKL-09018, BC-SKL-09028

**Prerequisites.** BC-PRQ-09001, BC-PRQ-09003

**Typical wording.**
- find the acceleration vector of the particle at the given time and show the setup for the calculations

**Common givens.**
- a velocity vector or a pair of component rates
- a time

**What is produced.**
- two derivative expressions
- a labelled vector of two values

**Representations.** BC-REP-14 (Vector-valued function), BC-REP-12 (Parametric equations), BC-REP-09 (Calculator-generated numerical result)

**Calculator status.** calculator

**Multipart structure.** The opening part of the calculator active BC free response question.

**Scoring pattern.** One point for each component with its setup; an unsupported correct acceleration vector earns one of the two points, a response that equates a variable expression to a numerical value earns one of the two, and degree mode work does not earn the first point it would otherwise have earned (sg-23:5, sg-23:6).

**Scoring point types.** none recorded. Point type definitions are in [../scoring/point-taxonomy.md](../scoring/point-taxonomy.md).

**Common distractors.**
- the velocity vector
- the magnitude of the acceleration
- the components in the wrong order

**Wrong approaches.**
- equating a variable expression to a numerical value
- reporting an unsupported vector

**Misconceptions.** BC-MIS-09009

**Variants.** 2 recorded: BC-QV-09004-01, BC-QV-09004-02

**Official examples notes.** 2023 Q2(a)

**Invariant structure.** Two component derivatives evaluated at one time and presented as one vector, each with visible supporting work.

**Safe variables.**
- the particle
- the units of the components
- the time

**Difficulty variables.**
- whether one component is given only through its derivative
- whether the notation must be a vector or may be two labelled numbers
- whether the calculator is in radian mode

Mapped difficulty factors: BC-DF-03 (Unusual representation), BC-DF-04 (Notation complexity), BC-DF-07 (Calculator workflow), BC-DF-16 (Units and labelling demand)

**Expected solution path.**
- differentiate each velocity component
- evaluate both at the time
- present the pair as a vector

**Prohibited shortcuts.**
- none recorded in this record

**Multi-skill extensions.**
- none recorded in this record

### BC-QA-09005 Coordinate of a particle recovered from an initial position

Evidence tag: verified. Scope: BC_only. Primary unit: BC-UNIT-09. Units: BC-UNIT-09. Sources: sg-24:7, sg-23:7, sg-23:8.

**Description.** A velocity component and a known position at one time are given, and the response reports a coordinate at another time.

**Concepts and skills required.** BC-SKL-09019, BC-SKL-09020, BC-SKL-09021, BC-SKL-09022, BC-SKL-09026, BC-SKL-09018

**Prerequisites.** BC-PRQ-06005

**Typical wording.**
- find the coordinate of the position of the particle at the stated time and show the setup for the calculations

**Common givens.**
- a velocity component
- the position at one time
- a second time

**What is produced.**
- an expression with an integral and the initial value
- a numerical coordinate

**Representations.** BC-REP-14 (Vector-valued function), BC-REP-01 (Symbolic (analytical) expression), BC-REP-09 (Calculator-generated numerical result)

**Calculator status.** calculator

**Multipart structure.** One part of the calculator active BC free response question.

**Scoring pattern.** Three points: the definite integral, the use of the initial condition, and the answer; several equivalent arrangements of the subtraction and of the limits earn the first two points (sg-24:7). A missing differential can keep the integral point while blocking the answer point when the expression is also equated to a value (sg-23:8).

**Scoring point types.** none recorded. Point type definitions are in [../scoring/point-taxonomy.md](../scoring/point-taxonomy.md).

**Common distractors.**
- the value of the integral alone
- the initial value with the integral subtracted in the wrong direction
- the other coordinate

**Wrong approaches.**
- omitting the initial condition
- integrating forwards when the known position is later

**Misconceptions.** BC-MIS-09010

**Variants.** 3 recorded: BC-QV-09005-01, BC-QV-09005-02, BC-QV-09005-03

**Official examples notes.** 2024 Q2(c), 2023 Q2(c)

**Invariant structure.** A known coordinate at one time plus the definite integral of the matching velocity component between the two times, with the direction of accumulation matching the order of the times.

**Safe variables.**
- the particle
- which coordinate is requested
- the units

**Difficulty variables.**
- whether the requested time is before or after the known time
- whether the integrand antidifferentiates in closed form
- whether the initial condition is stated as a point

Mapped difficulty factors: BC-DF-06 (Algebraic burden), BC-DF-08 (Multi-step dependency), BC-DF-14 (Missing or implicit given)

**Expected solution path.**
- write the coordinate as the known value plus the definite integral of the velocity component
- evaluate the integral
- add the known value
- report with units

**Prohibited shortcuts.**
- none recorded in this record

**Multi-skill extensions.**
- none recorded in this record

### BC-QA-09006 Speed of a particle in planar motion

Evidence tag: verified. Scope: BC_only. Primary unit: BC-UNIT-09. Units: BC-UNIT-09. Sources: sg-23:6, sg-23:7, sg-24:5.

**Description.** The response computes the speed at a time as the magnitude of the velocity vector, or solves for a time at which the speed takes a given value.

**Concepts and skills required.** BC-SKL-09023, BC-SKL-09024

**Prerequisites.** BC-PRQ-08007, BC-PRQ-09003

**Typical wording.**
- find the speed of the particle at the given time and show the setup
- find the first time at which the speed of the particle equals the stated value and show the work

**Common givens.**
- two velocity components
- a time or a target speed

**What is produced.**
- a magnitude expression
- a numerical speed or time

**Representations.** BC-REP-14 (Vector-valued function), BC-REP-09 (Calculator-generated numerical result)

**Calculator status.** calculator

**Multipart structure.** One part of the calculator active BC free response question.

**Scoring pattern.** Two points: the setup for the speed and the answer. An equation with an implied speed earns both, the words speed equals the value alone do not earn the setup point, a bare time value earns neither, and a parenthesis error in a squared component costs the setup point but not the answer point (sg-23:6, sg-24:5).

**Scoring point types.** none recorded. Point type definitions are in [../scoring/point-taxonomy.md](../scoring/point-taxonomy.md).

**Common distractors.**
- the sum of the two components
- one component alone
- the magnitude of the acceleration

**Wrong approaches.**
- reporting a time with no equation shown
- working in degree mode

**Misconceptions.** BC-MIS-09011

**Variants.** 2 recorded: BC-QV-09006-01, BC-QV-09006-02

**Official examples notes.** 2023 Q2(b), 2024 Q2(a)

**Invariant structure.** One magnitude of a two component velocity, either evaluated at a time or set equal to a stated value and solved on the interval.

**Safe variables.**
- the particle
- the units
- the time or the target speed

**Difficulty variables.**
- whether a value or a time is requested
- whether the first such time is demanded
- whether a component must be imported from an earlier part

Mapped difficulty factors: BC-DF-01 (Number of concepts combined), BC-DF-08 (Multi-step dependency)

**Expected solution path.**
- square both velocity components
- add and take the square root
- evaluate at the time, or set equal to the target and solve
- report the value

**Prohibited shortcuts.**
- none recorded in this record

**Multi-skill extensions.**
- none recorded in this record

### BC-QA-09007 Total distance travelled by a particle in the plane

Evidence tag: verified. Scope: BC_only. Primary unit: BC-UNIT-09. Units: BC-UNIT-09. Sources: sg-23:8, sg-24:6.

**Description.** The response integrates the speed over a time interval and reports the distance travelled.

**Concepts and skills required.** BC-SKL-09025, BC-SKL-09013

**Prerequisites.** BC-PRQ-08007

**Typical wording.**
- find the total distance travelled by the particle over the stated time interval and show the setup for the calculations

**Common givens.**
- two velocity components
- a time interval

**What is produced.**
- a definite integral of the speed
- a numerical distance

**Representations.** BC-REP-14 (Vector-valued function), BC-REP-09 (Calculator-generated numerical result)

**Calculator status.** calculator

**Multipart structure.** One part of the calculator active BC free response question.

**Scoring pattern.** Two points: the correct integrand inside a definite integral and the value; an incorrect speed imported from an earlier part earns the integral point and loses the answer point, and an unsupported correct value earns neither (sg-23:8, sg-24:6).

**Scoring point types.** none recorded. Point type definitions are in [../scoring/point-taxonomy.md](../scoring/point-taxonomy.md).

**Common distractors.**
- the magnitude of the displacement
- the integral of one component
- the difference of the endpoint positions

**Wrong approaches.**
- integrating the velocity components and then taking a magnitude

**Misconceptions.** BC-MIS-09006

**Variants.** 2 recorded: BC-QV-09007-01, BC-QV-09007-02

**Official examples notes.** 2023 Q2(d), 2024 Q2(b)

**Invariant structure.** The definite integral of the magnitude of the velocity over the time interval, reported as a length in the units of position.

**Safe variables.**
- the particle
- the units
- the interval

**Difficulty variables.**
- whether the speed expression is imported from an earlier part
- whether units are demanded
- whether the interval starts at the time of the initial condition

Mapped difficulty factors: BC-DF-01 (Number of concepts combined), BC-DF-08 (Multi-step dependency), BC-DF-14 (Missing or implicit given), BC-DF-16 (Units and labelling demand)

**Expected solution path.**
- write the speed as the magnitude of velocity
- integrate over the time interval
- evaluate numerically
- report with units

**Prohibited shortcuts.**
- none recorded in this record

**Multi-skill extensions.**
- none recorded in this record

### BC-QA-09008 Times at which a particle moves toward a coordinate axis

Evidence tag: verified. Scope: BC_only. Primary unit: BC-UNIT-09. Units: BC-UNIT-09. Sources: sg-24:8, frq-24:4.

**Description.** The response uses the sign of a velocity component, together with the sign of the corresponding coordinate, to say when the particle approaches an axis.

**Concepts and skills required.** BC-SKL-09027

**Prerequisites.** BC-PRQ-08001

**Typical wording.**
- find all times in the stated interval at which the particle is moving toward the named axis and give a reason for the answer

**Common givens.**
- a velocity component
- a statement about the quadrant the particle stays in
- an interval

**What is produced.**
- a sign argument
- a subinterval of times

**Representations.** BC-REP-14 (Vector-valued function), BC-REP-09 (Calculator-generated numerical result), BC-REP-04 (Verbal description)

**Calculator status.** calculator

**Multipart structure.** The closing part of the calculator active BC free response question.

**Scoring pattern.** Two points: one for considering the sign of the relevant velocity component and one for the answer with the reason; the reported interval may be open, closed, or half open (sg-24:8).

**Scoring point types.** none recorded. Point type definitions are in [../scoring/point-taxonomy.md](../scoring/point-taxonomy.md).

**Common distractors.**
- the times at which the coordinate itself is negative
- the times at which the other component is negative
- the whole interval

**Wrong approaches.**
- reading the direction from the sign of the position rather than of its rate

**Misconceptions.** BC-MIS-09012

**Variants.** 2 recorded: BC-QV-09008-01, BC-QV-09008-02

**Official examples notes.** 2024 Q2(d)

**Invariant structure.** One coordinate of known sign on the interval and one velocity component whose sign decides the direction, with the answer stated as a subinterval and a reason.

**Safe variables.**
- the particle
- which axis is named
- the interval

**Difficulty variables.**
- whether the sign of the coordinate is given or must be argued
- whether the endpoint of the subinterval is a decimal
- whether the answer must be justified

Mapped difficulty factors: BC-DF-07 (Calculator workflow), BC-DF-10 (Required justification), BC-DF-12 (Sign and direction handling), BC-DF-14 (Missing or implicit given)

**Expected solution path.**
- state the sign of the coordinate on the interval
- solve for where the corresponding velocity component is zero
- determine the subinterval on which it is negative
- state the answer with the reason

**Prohibited shortcuts.**
- none recorded in this record

**Multi-skill extensions.**
- none recorded in this record

## Family polar-area [verified]

2 archetype(s): BC-QA-09012, BC-QA-09013.

### BC-QA-09012 Area of a region bounded by a single polar curve

Evidence tag: verified. Scope: BC_only. Primary unit: BC-UNIT-09. Units: BC-UNIT-09. Sources: sg-25:7, sg-25:8.

**Description.** The response writes one half the integral of the square of r over the angles that sweep the region and evaluates it.

**Concepts and skills required.** BC-SKL-09035, BC-SKL-09036, BC-SKL-09037, BC-SKL-09038

**Prerequisites.** BC-PRQ-09004, BC-PRQ-08006

**Typical wording.**
- find the area of the region bounded by the polar curve on the stated interval and show the setup for the calculations

**Common givens.**
- a polar equation
- a figure or an angle interval

**What is produced.**
- a polar area integral
- a numerical area

**Representations.** BC-REP-13 (Polar equation), BC-REP-02 (Graphical), BC-REP-09 (Calculator-generated numerical result)

**Calculator status.** either

**Multipart structure.** One part of the calculator active BC free response question.

**Scoring pattern.** The first point is earned by a definite integral containing the square of r, the second by the full correct integrand, and the limits together with the factor of one half are assessed in the answer point (sg-25:7).

**Scoring point types.** none recorded. Point type definitions are in [../scoring/point-taxonomy.md](../scoring/point-taxonomy.md).

**Common distractors.**
- the integral of r without the square
- the integral without the factor of one half
- limits covering a full turn when one loop was wanted

**Wrong approaches.**
- integrating over an interval that traces the loop twice

**Misconceptions.** BC-MIS-09017, BC-MIS-09007

**Variants.** 3 recorded: BC-QV-09012-01, BC-QV-09012-02, BC-QV-09012-03

**Official examples notes.** 2025 Q2(B)

**Invariant structure.** One polar curve, one angle interval that sweeps the region exactly once, one integrand equal to one half the square of r.

**Safe variables.**
- the polar curve
- the region described
- the letters used

**Difficulty variables.**
- whether the limits are given or must be found from zeros of r
- whether the region is one loop of several
- whether technology evaluates the integral

Mapped difficulty factors: BC-DF-07 (Calculator workflow), BC-DF-14 (Missing or implicit given)

**Expected solution path.**
- identify the bounding angles
- write one half the integral of the square of r
- evaluate
- report the area

**Prohibited shortcuts.**
- none recorded in this record

**Multi-skill extensions.**
- none recorded in this record

### BC-QA-09013 Area inside one polar curve and outside another

Evidence tag: verified. Scope: BC_only. Primary unit: BC-UNIT-09. Units: BC-UNIT-09. Sources: sg-25:7, sg-25:8, frq-25:4.

**Description.** Two polar curves bound a region and the response integrates one half the difference of the squares of their radii between the intersection angles.

**Concepts and skills required.** BC-SKL-09039, BC-SKL-09040, BC-SKL-09041, BC-SKL-09042, BC-SKL-09043

**Prerequisites.** BC-PRQ-09002, BC-PRQ-08006

**Typical wording.**
- find the area of the region that lies inside one curve and outside the other, and show the setup for the calculations

**Common givens.**
- two polar equations
- a figure

**What is produced.**
- intersection angles
- an area integral
- a numerical area

**Representations.** BC-REP-13 (Polar equation), BC-REP-02 (Graphical), BC-REP-09 (Calculator-generated numerical result)

**Calculator status.** calculator

**Multipart structure.** One part of the calculator active BC free response question.

**Scoring pattern.** Three points: a definite integral containing the square of the outer radius, the full correct integrand, and the answer, which carries the limits and the factor of one half; unclear communication between the correct integral and the correct value was treated as scratch work, and a symmetry presentation earned all three points (sg-25:7, sg-25:8).

**Scoring point types.** none recorded. Point type definitions are in [../scoring/point-taxonomy.md](../scoring/point-taxonomy.md).

**Common distractors.**
- the square of the difference of the radii
- limits spanning the whole interval of the figure
- the difference of two separately computed areas taken with the wrong sign

**Wrong approaches.**
- squaring the difference of the two radii
- using the full angle interval instead of the intersection angles

**Misconceptions.** BC-MIS-09018, BC-MIS-09019

**Variants.** 3 recorded: BC-QV-09013-01, BC-QV-09013-02, BC-QV-09013-03

**Official examples notes.** 2025 Q2(B)

**Invariant structure.** Two radius functions, two intersection angles as limits, and an integrand equal to one half the square of the outer radius minus the square of the inner radius.

**Safe variables.**
- the two curves
- which is inside and which is outside
- the letters used

**Difficulty variables.**
- whether one curve is a circle of constant radius
- whether the intersection angles are exact or decimal
- whether the outer curve changes inside the interval

Mapped difficulty factors: BC-DF-07 (Calculator workflow)

**Expected solution path.**
- set the two radii equal and solve for the bounding angles
- decide which curve is outer
- write one half the integral of the difference of the squares
- evaluate and report

**Prohibited shortcuts.**
- none recorded in this record

**Multi-skill extensions.**
- none recorded in this record

## Family polar-calculus [verified]

3 archetype(s): BC-QA-09009, BC-QA-09010, BC-QA-09011.

### BC-QA-09009 Derivative of r with respect to theta on a polar curve

Evidence tag: verified. Scope: BC_only. Primary unit: BC-UNIT-09. Units: BC-UNIT-09. Sources: sg-25:6, sg-25:7, frq-25:4.

**Description.** The response differentiates a polar equation and reports the rate of change of r with respect to theta at a stated angle.

**Concepts and skills required.** BC-SKL-09030, BC-SKL-09031, BC-SKL-09029, BC-SKL-09033

**Prerequisites.** BC-PRQ-09003, BC-PRQ-09002

**Typical wording.**
- find the rate of change of r with respect to theta at the point on the curve where theta has the stated value, and show the setup

**Common givens.**
- a polar equation
- an angle

**What is produced.**
- a derivative expression
- a numerical value

**Representations.** BC-REP-13 (Polar equation), BC-REP-09 (Calculator-generated numerical result), BC-REP-01 (Symbolic (analytical) expression)

**Calculator status.** calculator

**Multipart structure.** The opening part of the calculator active BC free response question.

**Scoring pattern.** One point, earned when the response indicates differentiation of r and gives the correct value; exact and decimal forms both earn it, and several loose notations were accepted in 2025 provided the derivative was identifiable (sg-25:6, sg-25:7).

**Scoring point types.** none recorded. Point type definitions are in [../scoring/point-taxonomy.md](../scoring/point-taxonomy.md).

**Common distractors.**
- the value of r itself
- dy/dx at the same angle
- the derivative evaluated in degree mode

**Wrong approaches.**
- reporting a value with no indication that r was differentiated

**Misconceptions.** BC-MIS-09014, BC-MIS-09015

**Variants.** 2 recorded: BC-QV-09009-01, BC-QV-09009-02

**Official examples notes.** 2025 Q2(A)

**Invariant structure.** One polar equation, one angle, one derivative with respect to theta whose differentiation is visible in the response.

**Safe variables.**
- the polar curve
- the angle
- the letters used

**Difficulty variables.**
- whether an exact or a decimal answer is presented
- whether the interpretation as a rate of distance from the origin is demanded
- whether dy/dx is requested instead of dr/dtheta

Mapped difficulty factors: BC-DF-05 (Contextual interpretation), BC-DF-07 (Calculator workflow), BC-DF-13 (Reversed reasoning direction)

**Expected solution path.**
- differentiate r with respect to theta
- evaluate at the given angle
- report the value with the differentiation shown

**Prohibited shortcuts.**
- none recorded in this record

**Multi-skill extensions.**
- none recorded in this record

### BC-QA-09010 Rate at which a particle's distance from the origin changes

Evidence tag: verified. Scope: BC_only. Primary unit: BC-UNIT-09. Units: BC-UNIT-09. Sources: sg-25:10, frq-25:4.

**Description.** A particle travels along a polar curve with a given rate of change of the angle, and the response reports how fast its distance from the origin changes.

**Concepts and skills required.** BC-SKL-09032, BC-SKL-09030, BC-SKL-09031

**Prerequisites.** BC-PRQ-09003

**Typical wording.**
- find the rate at which the distance of the particle from the origin changes with respect to time at the stated angle, and show the setup

**Common givens.**
- a polar equation
- a constant rate of change of the angle
- an angle

**What is produced.**
- a chain rule product
- a numerical rate

**Representations.** BC-REP-13 (Polar equation), BC-REP-09 (Calculator-generated numerical result)

**Calculator status.** calculator

**Multipart structure.** The closing part of the calculator active BC free response question.

**Scoring pattern.** Two points: one for the chain rule product, presented symbolically or numerically and possibly in several steps, and one for the value; the answer from the earlier derivative part multiplied by the given rate earns both (sg-25:10).

**Scoring point types.** none recorded. Point type definitions are in [../scoring/point-taxonomy.md](../scoring/point-taxonomy.md).

**Common distractors.**
- dr/dtheta alone
- the speed of the particle along the curve
- r multiplied by the rate of the angle

**Wrong approaches.**
- omitting the factor giving the rate of the angle

**Misconceptions.** BC-MIS-09014

**Variants.** 2 recorded: BC-QV-09010-01, BC-QV-09010-02

**Official examples notes.** 2025 Q2(D)

**Invariant structure.** The product of dr/dtheta at the stated angle with the given dtheta/dt, presented either symbolically or numerically.

**Safe variables.**
- the particle
- the constant rate of the angle
- the angle

**Difficulty variables.**
- whether the derivative may be imported from an earlier part
- whether the chain rule product must be shown symbolically

Mapped difficulty factors: BC-DF-01 (Number of concepts combined), BC-DF-04 (Notation complexity), BC-DF-08 (Multi-step dependency)

**Expected solution path.**
- identify dr/dtheta at the angle
- multiply by the given rate of change of the angle
- report the value

**Prohibited shortcuts.**
- none recorded in this record

**Multi-skill extensions.**
- none recorded in this record

### BC-QA-09011 Point on a polar curve farthest from a coordinate axis

Evidence tag: verified. Scope: BC_only. Primary unit: BC-UNIT-09. Units: BC-UNIT-09. Sources: sg-25:8, sg-25:9, frq-25:4.

**Description.** The response maximises a Cartesian coordinate along a polar curve by setting its derivative with respect to theta equal to zero and justifying globally.

**Concepts and skills required.** BC-SKL-09034, BC-SKL-09029

**Prerequisites.** BC-PRQ-08001

**Typical wording.**
- find the value of the angle that corresponds to the point on the curve farthest from the named axis, and justify the answer

**Common givens.**
- a polar equation
- the derivative of the relevant coordinate
- an angle interval

**What is produced.**
- an equation for the critical angle
- a global justification
- the angle

**Representations.** BC-REP-13 (Polar equation), BC-REP-09 (Calculator-generated numerical result), BC-REP-02 (Graphical)

**Calculator status.** calculator

**Multipart structure.** One part of the calculator active BC free response question.

**Scoring pattern.** Three points: considering the derivative of the coordinate equal to zero, a global justification, and the answer with supporting work; a local argument does not earn the justification point but leaves the answer point available, and presenting the solution angle alone earns neither of the first two (sg-25:8, sg-25:9).

**Scoring point types.** none recorded. Point type definitions are in [../scoring/point-taxonomy.md](../scoring/point-taxonomy.md).

**Common distractors.**
- the angle at which r is largest
- an endpoint of the interval
- a local argument offered as the justification

**Wrong approaches.**
- presenting a first or second derivative test as the whole justification

**Misconceptions.** BC-MIS-09016, BC-MIS-09013

**Variants.** 3 recorded: BC-QV-09011-01, BC-QV-09011-02, BC-QV-09011-03

**Official examples notes.** 2025 Q2(C)

**Invariant structure.** One coordinate expressed in theta, one critical angle from setting its derivative equal to zero, and a comparison of the coordinate at that angle with its values at the endpoints.

**Safe variables.**
- the polar curve
- which axis the distance is measured from
- the angle interval

**Difficulty variables.**
- whether the derivative of the coordinate is supplied
- whether the justification is a candidates table or a sign change with uniqueness
- the number of critical angles in the interval

Mapped difficulty factors: BC-DF-03 (Unusual representation), BC-DF-10 (Required justification), BC-DF-12 (Sign and direction handling)

**Expected solution path.**
- express the coordinate in theta
- set its derivative equal to zero and solve
- compare the coordinate at the candidate and at both endpoints
- report the angle

**Prohibited shortcuts.**
- none recorded in this record

**Multi-skill extensions.**
- none recorded in this record

## Family procedure-selection [verified]

4 archetype(s): BC-QA-01014, BC-QA-03009, BC-QA-06016, BC-QA-10001.

### BC-QA-01014 Procedure selected for a limit from the form of the expression

Evidence tag: inferred. Scope: shared. Primary unit: BC-UNIT-01. Units: BC-UNIT-01. Sources: ced:44.

**Description.** Several limit expressions are presented and the response identifies which procedure resolves each, or resolves one after classifying it.

**Concepts and skills required.** BC-SKL-01029, BC-SKL-01030, BC-SKL-01031, BC-SKL-01021

**Prerequisites.** BC-PRQ-01001, BC-PRQ-01008

**Typical wording.**
- For each of the given limits, identify an appropriate method and use it to determine the limit.

**Common givens.**
- none recorded in this record

**What is produced.**
- none recorded in this record

**Representations.** BC-REP-01 (Symbolic (analytical) expression)

**Calculator status.** no_calculator

**Multipart structure.** Typically a single multiple choice item.

**Scoring pattern.** One point for the classification and one for the resulting value.

**Scoring point types.** none recorded. Point type definitions are in [../scoring/point-taxonomy.md](../scoring/point-taxonomy.md).

**Common distractors.**
- rewriting an expression that substitution already settles
- applying a rewriting technique that does not fit the form
- treating a nonzero number over zero as an indeterminate form
- reporting that a limit does not exist without considering one sided behaviour

**Wrong approaches.**
- none recorded in this record; see ../misconceptions/error-to-concept-map.md

**Misconceptions.** BC-MIS-01006

**Variants.** 3 recorded: BC-QV-01014-01, BC-QV-01014-02, BC-QV-01014-03

**Official examples notes.** none in 2023 to 2025 [inferred]

**Invariant structure.** The expressions are chosen so that substitution settles some of them, rewriting is required for others, and at least one is an unbounded quotient, so classification precedes computation.

**Safe variables.**
- the specific expressions
- the target inputs
- the number of expressions offered

**Difficulty variables.**
- whether the classification must be stated
- whether an indeterminate form is present
- whether a one sided analysis is required
- whether a limit at infinity is included

Mapped difficulty factors: BC-DF-01 (Number of concepts combined)

**Expected solution path.**
- substitute the target input into each expression
- classify the resulting form
- name the procedure that the form calls for
- carry out that procedure when a value is demanded

**Prohibited shortcuts.**
- none recorded in this record

**Multi-skill extensions.**
- none recorded in this record

### BC-QA-03009 Selecting the differentiation procedure for a given expression

Evidence tag: single-source. Scope: shared. Primary unit: BC-UNIT-03. Units: BC-UNIT-03. Sources: ced:79, ced:72, cr-22:21.

**Description.** An expression is supplied whose differentiation needs the right rule chosen first, and the response must classify the structure before differentiating.

**Concepts and skills required.** BC-SKL-03026, BC-SKL-03027, BC-SKL-03028, BC-SKL-03029, BC-SKL-03006

**Prerequisites.** BC-PRQ-03001, BC-PRQ-03006

**Typical wording.**
- find the derivative of the given expression
- identify the rule needed to differentiate the given expression

**Common givens.**
- none recorded in this record

**What is produced.**
- none recorded in this record

**Representations.** BC-REP-01 (Symbolic (analytical) expression), BC-REP-04 (Verbal description)

**Calculator status.** no_calculator

**Multipart structure.** A single multiple choice item, or a differentiation step inside a longer question.

**Scoring pattern.** Scored as an answer point; the Chief Reader reports record rule choice driven by the shape of an expression as a recurring source of lost credit (cr-22:21).

**Scoring point types.** none recorded. Point type definitions are in [../scoring/point-taxonomy.md](../scoring/point-taxonomy.md).

**Common distractors.**
- the product rule applied to a composite
- the chain rule applied to a product
- the power rule applied to an exponential
- a rule applied in the wrong order

**Wrong approaches.**
- none recorded in this record; see ../misconceptions/error-to-concept-map.md

**Misconceptions.** BC-MIS-03012, BC-MIS-03001

**Variants.** 3 recorded: BC-QV-03009-01, BC-QV-03009-02, BC-QV-03009-03

**Official examples notes.** none in the 2023 to 2025 BC free response questions read for this unit

**Invariant structure.** The expression is built so that a rule chosen from its surface appearance gives a wrong answer; the outermost operation decides the opening rule and the nesting decides the order of the rest.

**Safe variables.**
- the family of the functions involved
- the constants
- the letters naming the variables

**Difficulty variables.**
- whether an algebraic rewrite removes the need for a rule
- how many rules the expression needs
- whether the expression resembles a different family on the surface
- whether the response must name the rule as well as apply it

Mapped difficulty factors: BC-DF-02 (Prerequisite depth), BC-DF-06 (Algebraic burden)

**Expected solution path.**
- classify the outermost operation
- name the rule that structure requires
- apply the rules from the outside inward
- rewrite first when the rewrite is safe and shorter

**Prohibited shortcuts.**
- none recorded in this record

**Multi-skill extensions.**
- none recorded in this record

### BC-QA-06016 Selecting an antidifferentiation technique from the form of the integrand

Evidence tag: verified. Scope: shared. Primary unit: BC-UNIT-06. Units: BC-UNIT-06. Sources: ced:131.

**Description.** Several integrands of different structure are presented and the response classifies each and names or applies the technique that its structure calls for.

**Concepts and skills required.** BC-SKL-06071, BC-SKL-06072, BC-SKL-06073, BC-SKL-06074, BC-SKL-06056

**Prerequisites.** BC-PRQ-06001, BC-PRQ-06009, BC-PRQ-06010

**Typical wording.**
- find the indefinite integral, showing the work that leads to your answer

**Common givens.**
- none recorded in this record

**What is produced.**
- none recorded in this record

**Representations.** BC-REP-01 (Symbolic (analytical) expression)

**Calculator status.** no_calculator

**Multipart structure.** Typically one part of a multipart free response question, or a single multiple choice item.

**Scoring pattern.** The scoring behaviour of the applied technique governs, since the CED frames this topic as the skill of selecting a procedure rather than as a separate question type (ced:131); the technique setup and the antiderivative carry separate points in the 2023 and 2024 technique parts (sg-23:18, sg-24:18).

**Scoring point types.** none recorded. Point type definitions are in [../scoring/point-taxonomy.md](../scoring/point-taxonomy.md).

**Common distractors.**
- attempting substitution when the derivative of the proposed inner expression is not present
- attempting parts on a composite that substitution resolves
- dividing a rational integrand that is already proper
- antidifferentiating an integrand that has no closed-form antiderivative

**Wrong approaches.**
- none recorded in this record; see ../misconceptions/error-to-concept-map.md

**Misconceptions.** BC-MIS-06017, BC-MIS-06019, BC-MIS-06022

**Variants.** 3 recorded: BC-QV-06016-01, BC-QV-06016-02, BC-QV-06016-03

**Official examples notes.** 2024 Q5(d)

**Invariant structure.** Each integrand carries a structural marker, such as an inner derivative present, a product of unlike factors, a numerator degree at least the denominator degree, a factorable linear denominator, or an unbounded integrand, and the marker selects the technique.

**Safe variables.**
- the specific functions used
- the order in which the integrands are presented

**Difficulty variables.**
- whether more than one technique is needed in sequence
- whether a plausible but inapplicable technique is invited
- whether the integrand has no elementary antiderivative
- whether the response must justify the choice rather than only apply it

Mapped difficulty factors: BC-DF-06 (Algebraic burden), BC-DF-10 (Required justification), BC-DF-13 (Reversed reasoning direction), BC-DF-15 (Unsignposted procedure selection)

**Expected solution path.**
- inspect the integrand for structural markers
- name the technique the markers select
- rule out techniques whose preconditions fail
- apply the chosen technique, chaining a second one if the first leaves a non basic integral

**Prohibited shortcuts.**
- none recorded in this record

**Multi-skill extensions.**
- none recorded in this record

### BC-QA-10001 Selecting a convergence test for a given series

Evidence tag: verified. Scope: BC_only. Primary unit: BC-UNIT-10. Units: BC-UNIT-10. Sources: ced:190, sg-24:19, sg-25:25.

**Description.** A numerical series is presented and the response must name a test whose conditions it satisfies and apply it to a verdict.

**Concepts and skills required.** BC-SKL-10001, BC-SKL-10005, BC-SKL-10006, BC-SKL-10011, BC-SKL-10013, BC-SKL-10018, BC-SKL-10021, BC-SKL-10033

**Prerequisites.** none recorded

**Typical wording.**
- determine whether the series converges or diverges, and justify your answer

**Common givens.**
- none recorded in this record

**What is produced.**
- none recorded in this record

**Representations.** BC-REP-11 (Series (finite partial sums or infinite)), BC-REP-01 (Symbolic (analytical) expression)

**Calculator status.** no_calculator

**Multipart structure.** Typically one part of the multipart free response question that closes Section II Part B, or a single multiple choice item.

**Scoring pattern.** Where a test is named by the prompt, only that test earns credit (sg-21:23). Where the choice is free, the verdict earns nothing unless the conditions of the chosen test are established (sg-25:25).

**Scoring point types.** none recorded. Point type definitions are in [../scoring/point-taxonomy.md](../scoring/point-taxonomy.md).

**Common distractors.**
- concluding convergence because the terms approach zero
- applying the alternating series test to a series of positive terms
- using the geometric formula on a series without a constant ratio

**Wrong approaches.**
- none recorded in this record; see ../misconceptions/error-to-concept-map.md

**Misconceptions.** BC-MIS-10001, BC-MIS-10005, BC-MIS-10006

**Variants.** 3 recorded: BC-QV-10001-01, BC-QV-10001-02, BC-QV-10001-03

**Official examples notes.** 2024 Q6(a), 2025 Q6(A)

**Invariant structure.** A series of numbers is given in sigma or expanded form; the form of the general term determines which of the six assessed tests applies; the response names the test, checks its conditions, and states the verdict.

**Safe variables.**
- the letters used for the index
- the starting index
- the constants inside the general term

**Difficulty variables.**
- whether more than one test applies
- whether the terms alternate
- whether a factorial or an nth power is present
- whether the nth term test screens the series first

Mapped difficulty factors: BC-DF-02 (Prerequisite depth), BC-DF-08 (Multi-step dependency), BC-DF-09 (Theorem recognition)

**Expected solution path.**
- read the general term
- match its form to a test whose conditions it meets
- verify the conditions
- apply the test
- state the verdict naming the series

**Prohibited shortcuts.**
- none recorded in this record

**Multi-skill extensions.**
- none recorded in this record

## Family radius-interval [verified]

3 archetype(s): BC-QA-10013, BC-QA-10014, BC-QA-10015.

### BC-QA-10013 Interval of convergence by the ratio test with endpoint analysis

Evidence tag: verified. Scope: BC_only. Primary unit: BC-UNIT-10. Units: BC-UNIT-10. Sources: sg-25:24, sg-25:25, sg-22:20, sg-22:21.

**Description.** A power series is given and the response finds the interval of convergence, justifying the interior with the ratio test and each endpoint with a suitable test.

**Concepts and skills required.** BC-SKL-10031, BC-SKL-10032, BC-SKL-10053, BC-SKL-10054, BC-SKL-10055, BC-SKL-10057, BC-SKL-10059

**Prerequisites.** none recorded

**Typical wording.**
- using the ratio test, find the interval of convergence of the series and justify the answer

**Common givens.**
- none recorded in this record

**What is produced.**
- none recorded in this record

**Representations.** BC-REP-11 (Series (finite partial sums or infinite)), BC-REP-01 (Symbolic (analytical) expression)

**Calculator status.** no_calculator

**Multipart structure.** Typically one part of the multipart free response question that closes Section II Part B, or a single multiple choice item.

**Scoring pattern.** Five points are typical, for the ratio, the limit, the interior, considering both endpoints, and the analysis with the final interval; the ratio point is banked once earned, a reciprocal ratio blocks only the final point, an incorrect interior that earned its point still supports the endpoint point, and naming an appropriate test at each endpoint suffices for the analysis (sg-25:24, sg-25:25). A four point form appears where both endpoints take the same test (sg-22:20).

**Scoring point types.** none recorded. Point type definitions are in [../scoring/point-taxonomy.md](../scoring/point-taxonomy.md).

**Common distractors.**
- stopping at the open interval
- dropping the absolute value when solving
- using one endpoint verdict at both ends
- naming a test whose conditions the endpoint series fails

**Wrong approaches.**
- none recorded in this record; see ../misconceptions/error-to-concept-map.md

**Misconceptions.** BC-MIS-10007, BC-MIS-10011, BC-MIS-10014, BC-MIS-10022, BC-MIS-10023, BC-MIS-10024

**Variants.** 4 recorded: BC-QV-10013-01, BC-QV-10013-02, BC-QV-10013-03, BC-QV-10013-04

**Official examples notes.** 2025 Q6(A), 2022 Q6(a)

**Invariant structure.** The ratio of consecutive terms produces a limit that is a multiple of the absolute value of the displacement from the centre; the inequality gives the interior, and the two endpoint series are examined separately.

**Safe variables.**
- the centre
- the coefficients
- the letters in the general term

**Difficulty variables.**
- whether the endpoints behave alike
- whether the coefficients involve factorials
- whether the interior is symmetric about a nonzero centre
- the tests required at the two endpoints

Mapped difficulty factors: BC-DF-02 (Prerequisite depth), BC-DF-09 (Theorem recognition), BC-DF-14 (Missing or implicit given)

**Expected solution path.**
- form the ratio of consecutive terms
- evaluate its limit
- set the limit less than one and solve for the interior
- substitute each endpoint and identify the resulting series
- test each endpoint
- state the interval with the matching brackets

**Prohibited shortcuts.**
- none recorded in this record

**Multi-skill extensions.**
- none recorded in this record

### BC-QA-10014 Radius of convergence from a given series

Evidence tag: verified. Scope: BC_only. Primary unit: BC-UNIT-10. Units: BC-UNIT-10. Sources: sg-21:24.

**Description.** A Maclaurin or Taylor series is supplied and only the radius of convergence is requested.

**Concepts and skills required.** BC-SKL-10031, BC-SKL-10032, BC-SKL-10053, BC-SKL-10054, BC-SKL-10056

**Prerequisites.** none recorded

**Typical wording.**
- determine the radius of convergence of the series

**Common givens.**
- none recorded in this record

**What is produced.**
- none recorded in this record

**Representations.** BC-REP-11 (Series (finite partial sums or infinite)), BC-REP-01 (Symbolic (analytical) expression)

**Calculator status.** no_calculator

**Multipart structure.** Typically one part of the multipart free response question that closes Section II Part B, or a single multiple choice item.

**Scoring pattern.** Three points are typical, for the ratio, for the limit, and for the explicit radius; the limit point requires the ratio point first, and an interval presented without naming the radius does not earn the third point (sg-21:24).

**Scoring point types.** none recorded. Point type definitions are in [../scoring/point-taxonomy.md](../scoring/point-taxonomy.md).

**Common distractors.**
- presenting an interval instead of a radius
- inverting the coefficient quotient
- reporting the limit of the coefficients as the radius

**Wrong approaches.**
- none recorded in this record; see ../misconceptions/error-to-concept-map.md

**Misconceptions.** BC-MIS-10011, BC-MIS-10014, BC-MIS-10022

**Variants.** 2 recorded: BC-QV-10014-01, BC-QV-10014-02

**Official examples notes.** 2021 Q6(c)

**Invariant structure.** The ratio test yields an inequality in the absolute value of the variable whose bound is the radius, which must be named as a value.

**Safe variables.**
- the coefficients
- the centre
- the letters in the general term

**Difficulty variables.**
- whether the coefficients are exponential in the index
- whether the radius is irrational
- whether the series is centred away from zero

Mapped difficulty factors: BC-DF-02 (Prerequisite depth), BC-DF-12 (Sign and direction handling)

**Expected solution path.**
- form the ratio of consecutive terms
- evaluate its limit
- set the limit less than one and solve for the displacement
- state the radius explicitly

**Prohibited shortcuts.**
- none recorded in this record

**Multi-skill extensions.**
- none recorded in this record

### BC-QA-10015 Endpoint series identified and tested

Evidence tag: verified. Scope: BC_only. Primary unit: BC-UNIT-10. Units: BC-UNIT-10. Sources: sg-24:19, sg-24:20, sg-25:24.

**Description.** The value at one end of an interval is substituted into a power series and the resulting numerical series is tested by a named test.

**Concepts and skills required.** BC-SKL-10020, BC-SKL-10021, BC-SKL-10022, BC-SKL-10024, BC-SKL-10025, BC-SKL-10027, BC-SKL-10030, BC-SKL-10036, BC-SKL-10057, BC-SKL-10058, BC-SKL-10071

**Prerequisites.** none recorded

**Typical wording.**
- determine whether the series converges or diverges at the stated endpoint, and give a reason

**Common givens.**
- none recorded in this record

**What is produced.**
- none recorded in this record

**Representations.** BC-REP-11 (Series (finite partial sums or infinite)), BC-REP-04 (Verbal description)

**Calculator status.** no_calculator

**Multipart structure.** Typically one part of the multipart free response question that closes Section II Part B, or a single multiple choice item.

**Scoring pattern.** Two points are typical, one for considering the endpoint series and one for the answer with a reason; the comparison to the harmonic series carries the 2024 part, and the reason point is lost when the test named does not fit the series (sg-24:19, sg-24:20).

**Scoring point types.** none recorded. Point type definitions are in [../scoring/point-taxonomy.md](../scoring/point-taxonomy.md).

**Common distractors.**
- substituting into the index
- losing the alternating factor
- applying a comparison test to an alternating series
- assuming the other endpoint behaves the same way

**Wrong approaches.**
- none recorded in this record; see ../misconceptions/error-to-concept-map.md

**Misconceptions.** BC-MIS-10001, BC-MIS-10005, BC-MIS-10006, BC-MIS-10007, BC-MIS-10009, BC-MIS-10010, BC-MIS-10023, BC-MIS-10024

**Variants.** 3 recorded: BC-QV-10015-01, BC-QV-10015-02, BC-QV-10015-03

**Official examples notes.** 2024 Q6(a), 2025 Q6(A), 2022 Q6(a)

**Invariant structure.** The substitution collapses the power series into a numerical series whose form, alternating or positive, dictates the test; the verdict decides whether that endpoint belongs to the interval.

**Safe variables.**
- which endpoint is used
- the coefficients
- the comparison partner

**Difficulty variables.**
- whether the endpoint produces an alternating series
- whether the comparison partner must be chosen
- whether the prompt supplies the endpoint

Mapped difficulty factors: BC-DF-14 (Missing or implicit given)

**Expected solution path.**
- substitute the endpoint value for the variable
- simplify to a numerical series
- name a test whose conditions it meets
- apply the test and state the verdict

**Prohibited shortcuts.**
- none recorded in this record

**Multi-skill extensions.**
- none recorded in this record

## Family rate-in-rate-out [verified]

1 archetype(s): BC-QA-06006.

### BC-QA-06006 Rate in minus rate out accumulation

Evidence tag: verified. Scope: shared. Primary unit: BC-UNIT-06. Units: BC-UNIT-06, BC-UNIT-08. Sources: ced:124, sg-24:4, ced:154, cr-24:23.

**Description.** Two rates act on the same quantity over an interval and the response expresses or computes the net accumulation as the integral of their difference, possibly combined with an initial amount.

**Concepts and skills required.** BC-SKL-06039, BC-SKL-06037, BC-SKL-06036, BC-SKL-08013, BC-SKL-08016, BC-SKL-08012

**Prerequisites.** BC-PRQ-06005, BC-PRQ-08006

**Typical wording.**
- water enters at one rate and leaves at another; find the amount present at the end of the interval, showing the setup for your calculations
- the quantity enters at one modelled rate and leaves at another; find the amount present at the stated time and show the setup

**Common givens.**
- an inflow rate
- an outflow rate
- an initial amount

**What is produced.**
- a net rate expression
- an integral
- a value with units

**Representations.** BC-REP-01 (Symbolic (analytical) expression), BC-REP-04 (Verbal description), BC-REP-05 (Contextual model), BC-REP-09 (Calculator-generated numerical result)

**Calculator status.** calculator

**Multipart structure.** Typically one part of a multipart free response question, or a single multiple choice item.

**Scoring pattern.** Points attach to the integral of the difference and to the use of the initial amount, in the same pattern as the single rate net change question, where presenting the integral without the initial value forfeits the initial condition point (sg-24:4).

**Scoring point types.** none recorded. Point type definitions are in [../scoring/point-taxonomy.md](../scoring/point-taxonomy.md).

**Common distractors.**
- integrating each rate over a different interval
- reversing which rate is subtracted
- forgetting the initial amount
- using the net rate at a single input instead of its integral
- the sum of the two rates in place of the difference
- the integral of the inflow alone
- the difference taken in the wrong order

**Wrong approaches.**
- integrating each rate and subtracting the wrong way round
- dropping the parentheses around the outflow rate

**Misconceptions.** BC-MIS-06013, BC-MIS-08007

**Variants.** 6 recorded: BC-QV-06006-01, BC-QV-06006-02, BC-QV-06006-03, BC-QV-08005-01, BC-QV-08005-02, BC-QV-08005-03

**Official examples notes.** 2024 Q1(c); no rate in and rate out part appears in the 2023 to 2025 BC free response questions

**Invariant structure.** The net rate is the inflow rate minus the outflow rate; the amount present is the initial amount plus the integral of the net rate over the interval.

**Safe variables.**
- the physical quantity
- the names of the two rate functions
- the interval
- the stored quantity
- the units
- the names of the two processes

**Difficulty variables.**
- whether the two rates are given by formulas or partly in words
- whether the question asks for the amount or for the net change
- whether the interval is stated or must be found
- whether the net rate changes sign
- whether the two rates are both formulas or one is tabulated
- whether the question asks for an amount, a net change, or a time of maximum
- whether the interval is split where the net rate changes sign

Mapped difficulty factors: BC-DF-01 (Number of concepts combined), BC-DF-03 (Unusual representation), BC-DF-05 (Contextual interpretation), BC-DF-12 (Sign and direction handling), BC-DF-14 (Missing or implicit given), BC-DF-17 (Case splitting at a boundary)

**Expected solution path.**
- identify which rate increases and which decreases the quantity
- write the net rate as the difference
- integrate the net rate over the interval
- add the initial amount if one is given
- write the net rate as inflow minus outflow
- add the initial amount when an amount is requested
- report with units

**Prohibited shortcuts.**
- none recorded in this record

**Multi-skill extensions.**
- none recorded in this record

## Family related-rates [verified]

2 archetype(s): BC-QA-04006, BC-QA-04007.

### BC-QA-04006 Related rates in a geometric setting

Evidence tag: verified. Scope: shared. Primary unit: BC-UNIT-04. Units: BC-UNIT-04. Sources: ced:90, ced:91, cr-22:6, cr-22:7.

**Description.** A geometric configuration changes with time, one or more rates are supplied, and the response finds the rate of change of another quantity at a stated instant.

**Concepts and skills required.** BC-SKL-04017, BC-SKL-04018, BC-SKL-04019, BC-SKL-04021, BC-SKL-04023, BC-SKL-04024, BC-SKL-04025, BC-SKL-04026, BC-SKL-04027

**Prerequisites.** BC-PRQ-04001, BC-PRQ-04002, BC-PRQ-04003, BC-PRQ-04007, BC-PRQ-04008

**Typical wording.**
- find the rate at which the stated quantity is changing at the instant described

**Common givens.**
- none recorded in this record

**What is produced.**
- none recorded in this record

**Representations.** BC-REP-08 (Geometric diagram), BC-REP-05 (Contextual model), BC-REP-01 (Symbolic (analytical) expression)

**Calculator status.** either

**Multipart structure.** One part of a multipart free response question, or a standalone multiple choice item.

**Scoring pattern.** The 2022 Chief Reader report records that few responses expressed the changing quantity as a correct function of the varying dimension or recognised that the chain rule was needed to reach the rate with respect to time (cr-22:7); the Chief Reader entry BC-ERR-99013 records differentiating with respect to the wrong variable and omitting the product rule as a standing error family.

**Scoring point types.** none recorded. Point type definitions are in [../scoring/point-taxonomy.md](../scoring/point-taxonomy.md).

**Common distractors.**
- values substituted before the differentiation
- a varying dimension treated as a constant
- the chain rule factor omitted so that the derivative is taken with respect to a length rather than time
- the requested rate confused with the supplied one

**Wrong approaches.**
- none recorded in this record; see ../misconceptions/error-to-concept-map.md

**Misconceptions.** BC-MIS-04008, BC-MIS-04010, BC-MIS-04011

**Variants.** 4 recorded: BC-QV-04006-01, BC-QV-04006-02, BC-QV-04006-03, BC-QV-04006-04

**Official examples notes.** 2022 AB Q2(d) as described in the Chief Reader report

**Invariant structure.** A relating equation is differentiated with respect to time so that each varying quantity contributes its own rate; instantaneous values enter only after the differentiation, and the answer is a rate with units.

**Safe variables.**
- the solid or figure
- the units of length and time
- the instant chosen
- which rate is supplied and which is requested

**Difficulty variables.**
- whether a second variable must be eliminated by similar triangles
- whether a needed value must be recovered from the relating equation
- whether a product term forces the product rule
- whether the answer must be interpreted in words
- whether the geometry is supplied as a figure or only in words

Mapped difficulty factors: BC-DF-02 (Prerequisite depth), BC-DF-05 (Contextual interpretation)

**Expected solution path.**
- name each varying quantity and record the rates in derivative notation
- write the relating equation
- eliminate any variable the supplied rates cannot support
- differentiate with respect to time
- substitute the instantaneous values
- solve for the requested rate and report it with units

**Prohibited shortcuts.**
- none recorded in this record

**Multi-skill extensions.**
- none recorded in this record

### BC-QA-04007 Related rates on an implicitly defined curve

Evidence tag: verified. Scope: shared. Primary unit: BC-UNIT-04. Units: BC-UNIT-04. Sources: ced:90, cr-23:22, cr-23:23, cr-24:17, cr-24:18, crabbc-25:24.

**Description.** A particle moves along a curve given by an equation in two variables, one coordinate rate is supplied, and the response finds the other coordinate rate at a stated point.

**Concepts and skills required.** BC-SKL-04022, BC-SKL-04019, BC-SKL-04020, BC-SKL-04023, BC-SKL-04024

**Prerequisites.** BC-PRQ-04007, BC-PRQ-04008

**Typical wording.**
- at the instant when the particle is at the stated point, the coordinate is changing at the stated rate; find the rate of change of the other coordinate at that instant

**Common givens.**
- none recorded in this record

**What is produced.**
- none recorded in this record

**Representations.** BC-REP-01 (Symbolic (analytical) expression), BC-REP-02 (Graphical)

**Calculator status.** no_calculator

**Multipart structure.** The closing part of the implicit differentiation free response question.

**Scoring pattern.** The Chief Reader reports describe four scoring points on this task: an eligible attempt at implicit differentiation with respect to time, a completely correct differentiation, and the correct numerical value, with responses that differentiate with respect to x needing to continue through the chain rule to earn beyond the first point; the most common reason for losing the final point in 2025 was a sign error (cr-24:18, crabbc-25:24, crabbc-25:25).

**Scoring point types.** none recorded. Point type definitions are in [../scoring/point-taxonomy.md](../scoring/point-taxonomy.md).

**Common distractors.**
- differentiation with respect to x with no further work
- dy/dx and dy/dt confused
- the product rule omitted on the mixed term
- a sign error in the substituted rate

**Wrong approaches.**
- none recorded in this record; see ../misconceptions/error-to-concept-map.md

**Misconceptions.** BC-MIS-04008, BC-MIS-04009, BC-MIS-04011

**Variants.** 3 recorded: BC-QV-04007-01, BC-QV-04007-02, BC-QV-04007-03

**Official examples notes.** 2023 AB Q6(d), 2024 AB Q5(d), 2025 AB Q6 part D, as described in the Chief Reader reports

**Invariant structure.** The defining equation is differentiated with respect to time, so every term in x carries dx/dt and every term in y carries dy/dt; a mixed term needs the product rule, and the point and the supplied rate are substituted only afterwards.

**Safe variables.**
- the curve
- the point
- which coordinate rate is supplied
- the units

**Difficulty variables.**
- whether a mixed term is present
- whether the response must instead route through dy/dx and the chain rule
- whether the sign of the supplied rate is negative
- whether the same curve appeared in earlier parts

Mapped difficulty factors: BC-DF-01 (Number of concepts combined), BC-DF-06 (Algebraic burden), BC-DF-08 (Multi-step dependency), BC-DF-12 (Sign and direction handling)

**Expected solution path.**
- differentiate the defining equation with respect to time
- apply the product rule to any mixed term
- substitute the coordinates of the point and the supplied rate
- solve for the requested rate

**Prohibited shortcuts.**
- none recorded in this record

**Multi-skill extensions.**
- none recorded in this record

## Family representation-consistency [inferred]

1 archetype(s): BC-QA-01013.

### BC-QA-01013 Limit claim matched across graphical, numerical, and analytic representations

Evidence tag: inferred. Scope: shared. Primary unit: BC-UNIT-01. Units: BC-UNIT-01. Sources: ced:46, ced:39.

**Description.** A limit fact is presented in one representation and the response selects or produces the equivalent presentation in another.

**Concepts and skills required.** BC-SKL-01036, BC-SKL-01037, BC-SKL-01038, BC-SKL-01005, BC-SKL-01006, BC-SKL-01007, BC-SKL-01014

**Prerequisites.** BC-PRQ-06005

**Typical wording.**
- Which of the given representations is consistent with the stated limit behaviour of f at the named input?

**Common givens.**
- none recorded in this record

**What is produced.**
- none recorded in this record

**Representations.** BC-REP-01 (Symbolic (analytical) expression), BC-REP-02 (Graphical), BC-REP-03 (Numerical table), BC-REP-04 (Verbal description)

**Calculator status.** no_calculator

**Multipart structure.** Typically a single multiple choice item.

**Scoring pattern.** One point for the correct conversion.

**Scoring point types.** none recorded. Point type definitions are in [../scoring/point-taxonomy.md](../scoring/point-taxonomy.md).

**Common distractors.**
- matching on the function value rather than the limit
- matching a one sided statement with a two sided graph
- choosing a representation that agrees away from the target input only
- confusing an infinite limit with a limit at infinity

**Wrong approaches.**
- none recorded in this record; see ../misconceptions/error-to-concept-map.md

**Misconceptions.** BC-MIS-01018

**Variants.** 3 recorded: BC-QV-01013-01, BC-QV-01013-02, BC-QV-01013-03

**Official examples notes.** none in 2023 to 2025 [inferred]

**Invariant structure.** The same limit behaviour at one input is carried by all the offered representations except the distractors, so the task is conversion rather than evaluation.

**Safe variables.**
- the function
- the target input
- which representation is supplied

**Difficulty variables.**
- graph to table against table to expression against expression to verbal
- whether a one sided statement is involved
- whether an infinite limit is involved
- whether a graph must be produced rather than selected

Mapped difficulty factors: BC-DF-03 (Unusual representation), BC-DF-13 (Reversed reasoning direction), BC-DF-15 (Unsignposted procedure selection)

**Expected solution path.**
- read the limit behaviour from the supplied representation
- state the behaviour in neutral terms
- test each candidate representation against that behaviour
- select or produce the one that matches

**Prohibited shortcuts.**
- none recorded in this record

**Multi-skill extensions.**
- none recorded in this record

## Family revolution-volume [inferred]

2 archetype(s): BC-QA-08012, BC-QA-08013.

### BC-QA-08012 Volume of a solid of revolution by the disc method

Evidence tag: inferred. Scope: shared. Primary unit: BC-UNIT-08. Units: BC-UNIT-08. Sources: ced:160, ced:161.

**Description.** A region touching its axis of revolution is revolved and the response integrates pi times the square of the radius.

**Concepts and skills required.** BC-SKL-08040, BC-SKL-08041, BC-SKL-08042, BC-SKL-08043, BC-SKL-08044, BC-SKL-08045, BC-SKL-08046, BC-SKL-08047

**Prerequisites.** BC-PRQ-08004, BC-PRQ-08002

**Typical wording.**
- the region is revolved about the stated line; find the volume of the solid generated

**Common givens.**
- a region
- an axis of revolution

**What is produced.**
- an integrand with a squared radius
- the volume

**Representations.** BC-REP-08 (Geometric diagram), BC-REP-01 (Symbolic (analytical) expression), BC-REP-09 (Calculator-generated numerical result)

**Calculator status.** either

**Multipart structure.** One part of a multipart question built on a region introduced earlier.

**Scoring pattern.** A setup point for pi with the squared radius and the limits, and an answer point for the value; the Chief Reader records the wrong volume family as BC-ERR-99011.

**Scoring point types.** none recorded. Point type definitions are in [../scoring/point-taxonomy.md](../scoring/point-taxonomy.md).

**Common distractors.**
- the radius left unsquared
- the factor of pi omitted
- the radius written without the shift when the axis is not a coordinate axis

**Wrong approaches.**
- shifting the limits of integration along with the axis

**Misconceptions.** BC-MIS-08020, BC-MIS-08021, BC-MIS-08022

**Variants.** 3 recorded: BC-QV-08012-01, BC-QV-08012-02, BC-QV-08012-03

**Official examples notes.** no solid of revolution appears in the 2023 to 2025 BC free response questions

**Invariant structure.** One curve, one axis of revolution that the region meets, a radius equal to the distance from the curve to that axis, and a volume equal to pi times the integral of the square of that radius.

**Safe variables.**
- the curve
- the interval
- the letters used

**Difficulty variables.**
- whether the axis is a coordinate axis or another line
- whether the slicing variable is x or y
- whether the answer is left as a multiple of pi

Mapped difficulty factors: BC-DF-08 (Multi-step dependency)

**Expected solution path.**
- write the radius as a distance to the axis
- square it and multiply by pi
- integrate over the spanning interval
- report the volume

**Prohibited shortcuts.**
- none recorded in this record

**Multi-skill extensions.**
- none recorded in this record

### BC-QA-08013 Volume of a solid of revolution by the washer method

Evidence tag: inferred. Scope: shared. Primary unit: BC-UNIT-08. Units: BC-UNIT-08. Sources: ced:162, ced:163.

**Description.** A region separated from its axis of revolution is revolved and the response integrates pi times the difference of the squares of the two radii.

**Concepts and skills required.** BC-SKL-08048, BC-SKL-08049, BC-SKL-08050, BC-SKL-08051, BC-SKL-08052, BC-SKL-08053, BC-SKL-08054, BC-SKL-08055

**Prerequisites.** BC-PRQ-08004, BC-PRQ-08002

**Typical wording.**
- the region between the two curves is revolved about the stated line; find the volume of the solid generated

**Common givens.**
- two boundary curves
- an axis of revolution the region does not meet

**What is produced.**
- an integrand with two squared radii
- the volume

**Representations.** BC-REP-08 (Geometric diagram), BC-REP-01 (Symbolic (analytical) expression), BC-REP-09 (Calculator-generated numerical result)

**Calculator status.** either

**Multipart structure.** One part of a multipart question built on a region introduced earlier.

**Scoring pattern.** A setup point for the two squared radii with pi and the limits, and an answer point for the value; a swapped pair of radii produces a negative value and loses the answer point.

**Scoring point types.** none recorded. Point type definitions are in [../scoring/point-taxonomy.md](../scoring/point-taxonomy.md).

**Common distractors.**
- the square of the difference of the radii
- the radii assigned by which curve is higher rather than which is farther
- the shift omitted from both radii

**Wrong approaches.**
- squaring the difference of the two functions
- reporting a negative volume from swapped radii

**Misconceptions.** BC-MIS-08017, BC-MIS-08023, BC-MIS-08021

**Variants.** 3 recorded: BC-QV-08013-01, BC-QV-08013-02, BC-QV-08013-03

**Official examples notes.** no washer volume appears in the 2023 to 2025 BC free response questions

**Invariant structure.** Two boundary curves, one axis of revolution the region does not meet, and an integrand equal to the square of the outer radius minus the square of the inner radius, both measured from the axis.

**Safe variables.**
- the two curves
- the interval
- the letters used

**Difficulty variables.**
- whether the axis is a coordinate axis or another line
- whether the axis lies above or below the region, which can exchange the radii
- whether the slicing variable is x or y

Mapped difficulty factors: BC-DF-01 (Number of concepts combined)

**Expected solution path.**
- decide which curve is farther from the axis
- write both radii as distances
- square each radius and subtract
- multiply by pi and integrate
- report the volume

**Prohibited shortcuts.**
- none recorded in this record

**Multi-skill extensions.**
- none recorded in this record

## Family riemann-limit-to-integral [inferred]

1 archetype(s): BC-QA-06014.

### BC-QA-06014 Converting between a limit of Riemann sums and a definite integral

Evidence tag: inferred. Scope: shared. Primary unit: BC-UNIT-06. Units: BC-UNIT-06. Sources: ced:120.

**Description.** A limit of Riemann sums in sigma notation is given and the response writes the equivalent definite integral, or a definite integral is given and the response writes it as a limit of Riemann sums.

**Concepts and skills required.** BC-SKL-06012, BC-SKL-06013, BC-SKL-06014, BC-SKL-06015, BC-SKL-06016

**Prerequisites.** BC-PRQ-06006

**Typical wording.**
- express the given limit of a Riemann sum as a definite integral
- write the given definite integral as the limit of a Riemann sum

**Common givens.**
- none recorded in this record

**What is produced.**
- none recorded in this record

**Representations.** BC-REP-01 (Symbolic (analytical) expression)

**Calculator status.** no_calculator

**Multipart structure.** Typically one part of a multipart free response question, or a single multiple choice item.

**Scoring pattern.** No conversion part appears in the 2023 to 2025 free response questions read for this unit; the scoring behaviour is inferred from the essential knowledge requirement that the limit of a Riemann sum and the definite integral are interchangeable representations (ced:120).

**Scoring point types.** none recorded. Point type definitions are in [../scoring/point-taxonomy.md](../scoring/point-taxonomy.md).

**Common distractors.**
- reading the interval as zero to one when the width expression says otherwise
- omitting the width factor from the integrand
- using the number of subintervals as a limit of integration
- treating the index of summation as the variable of integration

**Wrong approaches.**
- none recorded in this record; see ../misconceptions/error-to-concept-map.md

**Misconceptions.** none recorded

**Variants.** 3 recorded: BC-QV-06014-01, BC-QV-06014-02, BC-QV-06014-03

**Official examples notes.** none in 2023 to 2025

**Invariant structure.** The general term of the sum factors into a function value at a sample point and a subinterval width; matching that factorisation to the limits of integration and the integrand produces the definite integral, and the conversion runs in both directions.

**Safe variables.**
- the function
- the interval endpoints
- the sample point convention

**Difficulty variables.**
- conversion direction
- uniform versus general partition
- whether the sample point is a left endpoint, right endpoint, or midpoint
- whether the interval must be inferred from the general term

Mapped difficulty factors: BC-DF-04 (Notation complexity), BC-DF-12 (Sign and direction handling), BC-DF-14 (Missing or implicit given)

**Expected solution path.**
- separate the general term into a value and a width
- identify the subinterval width and hence the interval length
- identify the sample point expression and hence the lower limit
- write the integrand and the limits of integration

**Prohibited shortcuts.**
- none recorded in this record

**Multi-skill extensions.**
- none recorded in this record

## Family rule-manipulation [verified]

6 archetype(s): BC-QA-02006, BC-QA-02007, BC-QA-02008, BC-QA-02010, BC-QA-03001, BC-QA-03007.

### BC-QA-02006 Derivative of a polynomial or power expression by rule

Evidence tag: inferred. Scope: shared. Primary unit: BC-UNIT-02. Units: BC-UNIT-02. Sources: ced:64, ced:65.

**Description.** An expression built from powers, radicals, and reciprocals is presented and the response differentiates it using the power, constant multiple, sum, and difference rules.

**Concepts and skills required.** BC-SKL-02025, BC-SKL-02026, BC-SKL-02028, BC-SKL-02029, BC-SKL-02030, BC-SKL-02031

**Prerequisites.** BC-PRQ-06002

**Typical wording.**
- Find the derivative of the given function.

**Common givens.**
- none recorded in this record

**What is produced.**
- none recorded in this record

**Representations.** BC-REP-01 (Symbolic (analytical) expression)

**Calculator status.** no_calculator

**Multipart structure.** Typically a single multiple choice item.

**Scoring pattern.** One point for the derivative, with an evaluation point when a value at an input is demanded.

**Scoring point types.** none recorded. Point type definitions are in [../scoring/point-taxonomy.md](../scoring/point-taxonomy.md).

**Common distractors.**
- reducing the exponent without multiplying by it
- differentiating a constant to itself
- leaving a radical undifferentiated
- dropping the negative sign produced by a negative exponent

**Wrong approaches.**
- none recorded in this record; see ../misconceptions/error-to-concept-map.md

**Misconceptions.** BC-MIS-02009

**Variants.** 3 recorded: BC-QV-02006-01, BC-QV-02006-02, BC-QV-02006-03

**Official examples notes.** none in 2023 to 2025 as a standalone part [inferred]

**Invariant structure.** Every term can be written as a constant times a power of the variable, so the derivative is obtained term by term without any product, quotient, or chain structure.

**Safe variables.**
- the coefficients
- the exponents
- the variable name
- the number of terms

**Difficulty variables.**
- integer against negative against fractional exponents
- whether a rewriting step is needed first
- whether the derivative is then evaluated at a point
- whether a second derivative is demanded

Mapped difficulty factors: BC-DF-08 (Multi-step dependency), BC-DF-12 (Sign and direction handling)

**Expected solution path.**
- rewrite radicals and reciprocals as powers
- differentiate each term by the power rule
- carry the constants through
- combine and return to the requested form

**Prohibited shortcuts.**
- none recorded in this record

**Multi-skill extensions.**
- none recorded in this record

### BC-QA-02007 Derivative of an expression built from the basic transcendental functions

Evidence tag: inferred. Scope: shared. Primary unit: BC-UNIT-02. Units: BC-UNIT-02. Sources: ced:66.

**Description.** An expression containing sine, cosine, the natural exponential, or the natural logarithm is presented and the response differentiates it.

**Concepts and skills required.** BC-SKL-02032, BC-SKL-02033, BC-SKL-02034

**Prerequisites.** BC-PRQ-01005, BC-PRQ-06003

**Typical wording.**
- Find the derivative of the given function.

**Common givens.**
- none recorded in this record

**What is produced.**
- none recorded in this record

**Representations.** BC-REP-01 (Symbolic (analytical) expression)

**Calculator status.** no_calculator

**Multipart structure.** Typically a single multiple choice item.

**Scoring pattern.** One point for the derivative.

**Scoring point types.** none recorded. Point type definitions are in [../scoring/point-taxonomy.md](../scoring/point-taxonomy.md).

**Common distractors.**
- giving sine as the derivative of cosine without the negative sign
- differentiating the natural exponential to a power one lower
- giving the logarithm rule with the wrong reciprocal
- treating the exponential base as a variable

**Wrong approaches.**
- none recorded in this record; see ../misconceptions/error-to-concept-map.md

**Misconceptions.** BC-MIS-02010

**Variants.** 3 recorded: BC-QV-02007-01, BC-QV-02007-02, BC-QV-02007-03

**Official examples notes.** none in 2023 to 2025 as a standalone part [inferred]

**Invariant structure.** Each transcendental term has a rule of its own, and the surrounding structure is a sum or a constant multiple, so no chain rule is required.

**Safe variables.**
- which transcendental functions appear
- the coefficients
- the variable name

**Difficulty variables.**
- whether a sign must be carried from the cosine rule
- whether a logarithm domain restriction is relevant
- whether the derivative is then evaluated at a point
- whether the expression mixes powers with transcendental terms

Mapped difficulty factors: BC-DF-02 (Prerequisite depth), BC-DF-08 (Multi-step dependency), BC-DF-12 (Sign and direction handling)

**Expected solution path.**
- identify the rule for each term
- differentiate term by term
- carry the constants and the signs
- combine the terms

**Prohibited shortcuts.**
- none recorded in this record

**Multi-skill extensions.**
- none recorded in this record

### BC-QA-02008 Derivative of a product or a quotient by rule

Evidence tag: inferred. Scope: shared. Primary unit: BC-UNIT-02. Units: BC-UNIT-02. Sources: ced:67, ced:68.

**Description.** A product or a quotient of two differentiable expressions is presented and the response differentiates it.

**Concepts and skills required.** BC-SKL-02036, BC-SKL-02038, BC-SKL-02039, BC-SKL-02040, BC-SKL-02042

**Prerequisites.** BC-PRQ-06002

**Typical wording.**
- Find the derivative of the given function.

**Common givens.**
- none recorded in this record

**What is produced.**
- none recorded in this record

**Representations.** BC-REP-01 (Symbolic (analytical) expression)

**Calculator status.** no_calculator

**Multipart structure.** Typically a single multiple choice item or one part of a larger question.

**Scoring pattern.** One point for the correct rule applied with both derivatives present and one for the simplified result.

**Scoring point types.** none recorded. Point type definitions are in [../scoring/point-taxonomy.md](../scoring/point-taxonomy.md).

**Common distractors.**
- multiplying the two derivatives together
- reversing the two terms in the quotient numerator
- omitting the square on the denominator
- applying the quotient rule where the denominator is a constant

**Wrong approaches.**
- none recorded in this record; see ../misconceptions/error-to-concept-map.md

**Misconceptions.** BC-MIS-02011, BC-MIS-02012

**Variants.** 4 recorded: BC-QV-02008-01, BC-QV-02008-02, BC-QV-02008-03, BC-QV-02008-04

**Official examples notes.** none in 2023 to 2025 as a standalone part [inferred]

**Invariant structure.** Neither factor is constant and the expression does not simplify to a sum of powers, so the product or quotient rule is required, and in the quotient case the order of the two numerator terms carries a sign.

**Safe variables.**
- the two factors
- the variable name
- whether the expression is a product or a quotient

**Difficulty variables.**
- polynomial factors against transcendental factors
- whether the denominator is constant
- whether the result must be simplified
- whether the derivative is then evaluated at a point

Mapped difficulty factors: BC-DF-02 (Prerequisite depth), BC-DF-06 (Algebraic burden), BC-DF-08 (Multi-step dependency)

**Expected solution path.**
- identify the two factors and their derivatives
- substitute into the product or quotient rule
- keep the order of the terms in the quotient numerator
- simplify as requested

**Prohibited shortcuts.**
- none recorded in this record

**Multi-skill extensions.**
- none recorded in this record

### BC-QA-02010 Derivative of a tangent, cotangent, secant, or cosecant expression

Evidence tag: inferred. Scope: shared. Primary unit: BC-UNIT-02. Units: BC-UNIT-02. Sources: ced:69.

**Description.** An expression containing one of the remaining trigonometric functions is presented and the response differentiates it after rewriting.

**Concepts and skills required.** BC-SKL-02043, BC-SKL-02044, BC-SKL-02045, BC-SKL-02046

**Prerequisites.** BC-PRQ-02002

**Typical wording.**
- Find the derivative of the given function.

**Common givens.**
- none recorded in this record

**What is produced.**
- none recorded in this record

**Representations.** BC-REP-01 (Symbolic (analytical) expression)

**Calculator status.** no_calculator

**Multipart structure.** Typically a single multiple choice item.

**Scoring pattern.** One point for the rewriting and the rule and one for the simplified result.

**Scoring point types.** none recorded. Point type definitions are in [../scoring/point-taxonomy.md](../scoring/point-taxonomy.md).

**Common distractors.**
- giving secant squared as the derivative of cotangent
- dropping the negative sign on a cofunction derivative
- differentiating numerator and denominator separately
- leaving the result in a form the question does not accept

**Wrong approaches.**
- none recorded in this record; see ../misconceptions/error-to-concept-map.md

**Misconceptions.** BC-MIS-02013

**Variants.** 3 recorded: BC-QV-02010-01, BC-QV-02010-02, BC-QV-02010-03

**Official examples notes.** none in 2023 to 2025 as a standalone part [inferred]

**Invariant structure.** No rule for the function is assumed, so the response rewrites it with sine and cosine, applies the quotient rule, and simplifies with a Pythagorean identity.

**Safe variables.**
- which trigonometric function appears
- the coefficients
- the variable name

**Difficulty variables.**
- tangent against secant against the cofunctions
- whether the simplified form is demanded
- whether the expression also contains a product
- whether the derivative is then evaluated at a standard angle

Mapped difficulty factors: BC-DF-06 (Algebraic burden), BC-DF-08 (Multi-step dependency)

**Expected solution path.**
- rewrite the function using sine and cosine
- apply the quotient rule
- simplify the numerator with a Pythagorean identity
- write the result in the requested trigonometric form

**Prohibited shortcuts.**
- none recorded in this record

**Multi-skill extensions.**
- none recorded in this record

### BC-QA-03001 Chain rule derivative of a composite given symbolically

Evidence tag: verified. Scope: shared. Primary unit: BC-UNIT-03. Units: BC-UNIT-03. Sources: ced:75, ced:72, sg-25:20.

**Description.** A formula built by composition is supplied and the response produces its derivative, often with a product, quotient, or second layer inside.

**Concepts and skills required.** BC-SKL-03002, BC-SKL-03003, BC-SKL-03006

**Prerequisites.** BC-PRQ-03001, BC-PRQ-03006

**Typical wording.**
- find the derivative of the given function
- find dy/dx for the given expression

**Common givens.**
- none recorded in this record

**What is produced.**
- none recorded in this record

**Representations.** BC-REP-01 (Symbolic (analytical) expression)

**Calculator status.** no_calculator

**Multipart structure.** Usually a single multiple choice item, or an opening step inside a multipart free response question.

**Scoring pattern.** Derivative questions of this form are scored as a single answer point in multiple choice, and inside a free response part the chain rule factor is the discriminating element; the 2025 BC scoring guidelines award a separate chain rule point where a composite is differentiated inside a larger task (sg-25:20).

**Scoring point types.** none recorded. Point type definitions are in [../scoring/point-taxonomy.md](../scoring/point-taxonomy.md).

**Common distractors.**
- the derivative of the outer function with the inner derivative omitted
- the derivative of the inner function alone
- the product of the two derivatives evaluated at the same input
- the outer derivative with the inner function differentiated in the wrong place

**Wrong approaches.**
- none recorded in this record; see ../misconceptions/error-to-concept-map.md

**Misconceptions.** BC-MIS-03001, BC-MIS-03002, BC-MIS-03012

**Variants.** 3 recorded: BC-QV-03001-01, BC-QV-03001-02, BC-QV-03001-03

**Official examples notes.** 2025 Q5(A) awards a chain rule point inside a larger differentiation task

**Invariant structure.** The expression is a composition of differentiable functions; the derivative is the product of the derivative of each layer evaluated at the layer inside it, and no layer may be left undifferentiated.

**Safe variables.**
- the named outer function
- the inner expression
- the letters used for the variables
- the constants inside the inner function

**Difficulty variables.**
- number of layers
- whether a product or quotient encloses the composite
- whether the inner function is trigonometric, exponential, or logarithmic
- whether the answer must be simplified

Mapped difficulty factors: BC-DF-02 (Prerequisite depth), BC-DF-06 (Algebraic burden)

**Expected solution path.**
- identify the outer and inner functions
- differentiate the outer function at the inner expression
- multiply by the derivative of the inner expression
- repeat inward for further layers
- simplify only as far as is safe

**Prohibited shortcuts.**
- none recorded in this record

**Multi-skill extensions.**
- none recorded in this record

### BC-QA-03007 Inverse trigonometric derivative with an inner function

Evidence tag: verified. Scope: shared. Primary unit: BC-UNIT-03. Units: BC-UNIT-03. Sources: ced:78, sg-25:2, sg-25:4.

**Description.** An expression containing an inverse trigonometric function is supplied and the response differentiates it, often evaluating the result at a point.

**Concepts and skills required.** BC-SKL-03021, BC-SKL-03022, BC-SKL-03024, BC-SKL-03025

**Prerequisites.** BC-PRQ-03004, BC-PRQ-03006

**Typical wording.**
- find the derivative of the given inverse trigonometric expression
- find the rate of change of the modelled quantity at the stated time

**Common givens.**
- none recorded in this record

**What is produced.**
- none recorded in this record

**Representations.** BC-REP-01 (Symbolic (analytical) expression)

**Calculator status.** either

**Multipart structure.** A single multiple choice item, or a differentiation step inside a contextual free response question.

**Scoring pattern.** In the 2025 contextual question the derivative of an inverse tangent model is supplied in the stem and later parts are scored on the use of that expression rather than on producing it (sg-25:2, sg-25:4).

**Scoring point types.** none recorded. Point type definitions are in [../scoring/point-taxonomy.md](../scoring/point-taxonomy.md).

**Common distractors.**
- the standard formula used without the inner derivative
- the inner expression left unsquared inside the radical or denominator
- the inverse sine formula used for the inverse tangent
- the derivative of the ordinary trigonometric function reported

**Wrong approaches.**
- none recorded in this record; see ../misconceptions/error-to-concept-map.md

**Misconceptions.** BC-MIS-03010, BC-MIS-03011, BC-MIS-03001

**Variants.** 3 recorded: BC-QV-03007-01, BC-QV-03007-02, BC-QV-03007-03

**Official examples notes.** 2025 Q1 supplies the derivative of an inverse tangent model in the stem

**Invariant structure.** The standard formula is applied with the inner expression in place of the variable and is multiplied by the derivative of that inner expression; the radical or the quadratic denominator carries the inner expression squared.

**Safe variables.**
- which inverse trigonometric function appears
- the inner expression
- the constants in the inner expression
- the context, when the function models a quantity

**Difficulty variables.**
- whether the inner function is nonlinear
- whether a product or quotient encloses the inverse trigonometric factor
- whether the derivative must be evaluated numerically
- whether the derivative is supplied in the stem instead

Mapped difficulty factors: BC-DF-02 (Prerequisite depth)

**Expected solution path.**
- write the standard derivative with the inner expression substituted
- multiply by the derivative of the inner expression
- simplify the radical or rational expression
- evaluate at the stated input when asked

**Prohibited shortcuts.**
- none recorded in this record

**Multi-skill extensions.**
- none recorded in this record

## Family separation-of-variables [verified]

2 archetype(s): BC-QA-07003, BC-QA-07011.

### BC-QA-07003 Particular solution by separation of variables

Evidence tag: verified. Scope: shared. Primary unit: BC-UNIT-07. Units: BC-UNIT-07. Sources: sg-23:11, sg-23:12, sg-24:11, frq-23:7, frq-24:7.

**Description.** A separable differential equation and an initial condition are given and the response must produce the particular solution explicitly.

**Concepts and skills required.** BC-SKL-07024, BC-SKL-07025, BC-SKL-07026, BC-SKL-07027, BC-SKL-07029, BC-SKL-07030, BC-SKL-07033

**Prerequisites.** BC-PRQ-07001, BC-PRQ-07002, BC-PRQ-07004, BC-PRQ-06003

**Typical wording.**
- use separation of variables to find an expression for the particular solution to the differential equation with the given initial condition

**Common givens.**
- a separable differential equation
- an initial condition
- sometimes a stated bound on the quantity

**What is produced.**
- the separated form
- the antiderivatives
- the evaluated constant
- the explicit solution

**Representations.** BC-REP-01 (Symbolic (analytical) expression), BC-REP-06 (Differential equation), BC-REP-05 (Contextual model)

**Calculator status.** no_calculator

**Multipart structure.** The closing part of a multipart free response question, worth four or five points.

**Scoring pattern.** Four points in 2023: separating the variables, finding the antiderivatives, including the constant of integration and using the initial condition, and solving for the dependent variable. A response with no separation earns none of the four; a response with no constant earns at most the first two; the third point requires the first two and the fourth requires the first three; an antiderivative written without absolute value symbols stays eligible for all four (sg-23:12). Five points in 2024, with the two antiderivatives scored separately (sg-24:11).

**Scoring point types.** none recorded. Point type definitions are in [../scoring/point-taxonomy.md](../scoring/point-taxonomy.md).

**Common distractors.**
- antidifferentiating only one side
- omitting the constant of integration
- adding the constant after the exponentiation instead of before
- keeping both branches of an absolute value when the initial condition settles one

**Wrong approaches.**
- treating the equation as though the dependent variable were a constant

**Misconceptions.** BC-MIS-07014, BC-MIS-07015, BC-MIS-07016, BC-MIS-07017, BC-MIS-07018

**Variants.** 3 recorded: BC-QV-07003-01, BC-QV-07003-02, BC-QV-07003-03

**Official examples notes.** 2023 Q3(d), 2024 Q3(c)

**Invariant structure.** The right side factors, both sides are antidifferentiated, one constant is carried, the initial condition fixes it, and the answer is solved for the dependent variable.

**Safe variables.**
- the modelled context
- the letters used
- the initial values

**Difficulty variables.**
- whether the dependent side antidifferentiates to a logarithm or a power
- whether an absolute value must be resolved
- whether the independent side needs a substitution
- whether the answer must be explicit

Mapped difficulty factors: BC-DF-02 (Prerequisite depth), BC-DF-06 (Algebraic burden)

**Expected solution path.**
- separate the variables with a differential on each side
- antidifferentiate both sides
- include one constant
- substitute the initial condition and solve for the constant
- solve for the dependent variable

**Prohibited shortcuts.**
- none recorded in this record

**Multi-skill extensions.**
- none recorded in this record

### BC-QA-07011 Particular solution with a domain restriction or an accumulation form

Evidence tag: inferred. Scope: shared. Primary unit: BC-UNIT-07. Units: BC-UNIT-07. Sources: ced:143, sg-23:12, sg-24:11.

**Description.** The response must produce a particular solution and say on what interval it holds, or write it as the initial value plus an integral.

**Concepts and skills required.** BC-SKL-07030, BC-SKL-07031, BC-SKL-07032, BC-SKL-07038

**Prerequisites.** BC-PRQ-07004, BC-PRQ-05003

**Typical wording.**
- find the particular solution to the differential equation with the given initial condition, and state the interval on which the solution is valid

**Common givens.**
- a differential equation
- an initial condition

**What is produced.**
- the particular solution
- the interval of validity, or the accumulation form

**Representations.** BC-REP-01 (Symbolic (analytical) expression), BC-REP-06 (Differential equation), BC-REP-05 (Contextual model)

**Calculator status.** no_calculator

**Multipart structure.** One part of a multipart free response question, or a single multiple choice item.

**Scoring pattern.** Scored as the separable family, with the branch choice folded into the constant point and the domain statement scored as part of the final answer where it is demanded (sg-23:12, sg-24:11).

**Scoring point types.** none recorded. Point type definitions are in [../scoring/point-taxonomy.md](../scoring/point-taxonomy.md).

**Common distractors.**
- keeping both branches of an absolute value
- reporting an interval that does not contain the initial input
- claiming the formula holds for every input
- leaving the answer implicit

**Wrong approaches.**
- choosing the branch by the sign of the constant rather than by the initial condition

**Misconceptions.** BC-MIS-07018, BC-MIS-07019, BC-MIS-07020

**Variants.** 3 recorded: BC-QV-07011-01, BC-QV-07011-02, BC-QV-07011-03

**Official examples notes.** none in 2023 to 2025

**Invariant structure.** The initial point lies in the interior of the interval of validity, the branch and the sign are settled by the initial condition, and the accumulation form is available whenever the right side involves only the independent variable.

**Safe variables.**
- the letters used
- the initial values
- the context

**Difficulty variables.**
- whether the solution expression has a vertical asymptote
- whether an absolute value must be resolved
- whether the accumulation form is acceptable

Mapped difficulty factors: BC-DF-03 (Unusual representation)

**Expected solution path.**
- produce the general solution
- use the initial condition to fix the constant and the branch
- identify where the expression fails to be defined
- report the interval containing the initial input

**Prohibited shortcuts.**
- none recorded in this record

**Multi-skill extensions.**
- none recorded in this record

## Family series-value [verified]

2 archetype(s): BC-QA-10002, BC-QA-10003.

### BC-QA-10002 Value of a convergent series requested

Evidence tag: single-source. Scope: BC_only. Primary unit: BC-UNIT-10. Units: BC-UNIT-10. Sources: ced:186, ced:187, cr-22:30.

**Description.** A convergent series is given and the response must produce its value rather than a partial sum.

**Concepts and skills required.** BC-SKL-10002, BC-SKL-10003, BC-SKL-10004, BC-SKL-10008, BC-SKL-10066

**Prerequisites.** none recorded

**Typical wording.**
- find the value of the series, or state that it diverges

**Common givens.**
- none recorded in this record

**What is produced.**
- none recorded in this record

**Representations.** BC-REP-11 (Series (finite partial sums or infinite)), BC-REP-01 (Symbolic (analytical) expression)

**Calculator status.** no_calculator

**Multipart structure.** Typically one part of the multipart free response question that closes Section II Part B, or a single multiple choice item.

**Scoring pattern.** A partial sum presented as the value earns no value point, and the chief reader reports describe responses that add the first several terms instead of summing the series (cr-22:30).

**Scoring point types.** none recorded. Point type definitions are in [../scoring/point-taxonomy.md](../scoring/point-taxonomy.md).

**Common distractors.**
- adding the first few terms and reporting the total
- using the index zero term as the first term
- reporting the limit of the general term

**Wrong approaches.**
- none recorded in this record; see ../misconceptions/error-to-concept-map.md

**Misconceptions.** BC-MIS-10001, BC-MIS-10002, BC-MIS-10005

**Variants.** 2 recorded: BC-QV-10002-01, BC-QV-10002-02

**Official examples notes.** none in 2021 to 2025 as a standalone part

**Invariant structure.** A series with a recognisable closed form, geometric or telescoping, is given; the response identifies the structure and takes the limit of the partial sums or applies the closed form.

**Safe variables.**
- the constants in the general term
- the starting index
- the variable name

**Difficulty variables.**
- geometric versus telescoping structure
- whether the starting index is zero
- whether the series arrives from a Taylor series evaluated at a point

Mapped difficulty factors: BC-DF-02 (Prerequisite depth)

**Expected solution path.**
- identify the structure of the series
- write the partial sum or the pair of first term and ratio
- take the limit or apply the closed form
- report the value

**Prohibited shortcuts.**
- none recorded in this record

**Multi-skill extensions.**
- none recorded in this record

### BC-QA-10003 Geometric series summed in closed form

Evidence tag: verified. Scope: BC_only. Primary unit: BC-UNIT-10. Units: BC-UNIT-10. Sources: sg-25:26, ced:187.

**Description.** A series, numerical or in a variable, is recognised as geometric and summed with the closed form, with the convergence condition recorded.

**Concepts and skills required.** BC-SKL-10006, BC-SKL-10007, BC-SKL-10008, BC-SKL-10009, BC-SKL-10010, BC-SKL-10063, BC-SKL-10072

**Prerequisites.** none recorded

**Typical wording.**
- show that the sum of the series equals the given expression on the interval of convergence

**Common givens.**
- none recorded in this record

**What is produced.**
- none recorded in this record

**Representations.** BC-REP-11 (Series (finite partial sums or infinite)), BC-REP-01 (Symbolic (analytical) expression)

**Calculator status.** no_calculator

**Multipart structure.** Typically one part of the multipart free response question that closes Section II Part B, or a single multiple choice item.

**Scoring pattern.** A single verification point is available where the closed form is supplied by the prompt, and presenting the unsimplified quotient of first term by one minus ratio is sufficient (sg-25:26).

**Scoring point types.** none recorded. Point type definitions are in [../scoring/point-taxonomy.md](../scoring/point-taxonomy.md).

**Common distractors.**
- taking the coefficient as the ratio
- applying the formula without checking the size of the ratio
- using the index zero term when the series starts elsewhere

**Wrong approaches.**
- none recorded in this record; see ../misconceptions/error-to-concept-map.md

**Misconceptions.** BC-MIS-10002, BC-MIS-10003, BC-MIS-10004

**Variants.** 3 recorded: BC-QV-10003-01, BC-QV-10003-02, BC-QV-10003-03

**Official examples notes.** 2025 Q6(C)

**Invariant structure.** Consecutive terms of the given series have a constant quotient; the response identifies the first term and the ratio and presents the quotient of the first term by one minus the ratio.

**Safe variables.**
- the centre of the powers
- the constants in the first term
- the direction of the algebra in the final simplification

**Difficulty variables.**
- numerical ratio versus a ratio containing the variable
- whether the series starts at index zero
- whether a given closed form must be verified rather than produced

Mapped difficulty factors: BC-DF-06 (Algebraic burden), BC-DF-13 (Reversed reasoning direction)

**Expected solution path.**
- divide consecutive terms to find the ratio
- identify the first term as written
- state the condition on the size of the ratio
- form the quotient and simplify to the requested closed form

**Prohibited shortcuts.**
- none recorded in this record

**Multi-skill extensions.**
- none recorded in this record

## Family slope-field [verified]

2 archetype(s): BC-QA-07001, BC-QA-07002.

### BC-QA-07001 Solution curve sketched on a supplied slope field

Evidence tag: verified. Scope: shared. Primary unit: BC-UNIT-07. Units: BC-UNIT-07. Sources: sg-23:9, sg-24:9, frq-23:7, frq-24:7.

**Description.** A slope field for a given differential equation is printed and the response must draw the solution curve through a stated point.

**Concepts and skills required.** BC-SKL-07014, BC-SKL-07015, BC-SKL-07017

**Prerequisites.** BC-PRQ-07006

**Typical wording.**
- a portion of the slope field for the differential equation is shown; sketch the solution curve through the given point

**Common givens.**
- a differential equation
- a printed slope field
- an initial condition

**What is produced.**
- one drawn curve

**Representations.** BC-REP-07 (Slope field), BC-REP-02 (Graphical), BC-REP-06 (Differential equation)

**Calculator status.** no_calculator

**Multipart structure.** The opening part of a multipart free response question, worth one point.

**Scoring pattern.** One point, awarded only when the curve passes through the stated point, extends reasonably close to the left and right edges of the given rectangle, has no obvious conflict with the drawn segments, and lies entirely on the correct side of the horizontal segments marking the equilibrium level. Only the portion inside the printed field is considered (sg-23:9, sg-24:9).

**Scoring point types.** none recorded. Point type definitions are in [../scoring/point-taxonomy.md](../scoring/point-taxonomy.md).

**Common distractors.**
- a curve that crosses the equilibrium level
- a curve that stops short of the edges of the rectangle
- a curve drawn through the wrong point
- a curve whose slope conflicts with the nearby segments

**Wrong approaches.**
- solving the differential equation first and plotting the formula

**Misconceptions.** BC-MIS-07006, BC-MIS-07008, BC-MIS-07009

**Variants.** 3 recorded: BC-QV-07001-01, BC-QV-07001-02, BC-QV-07001-03

**Official examples notes.** 2023 Q3(a), 2024 Q3(a)

**Invariant structure.** The field is supplied rather than built, the initial point is marked or stated, and the whole part is worth one point awarded on the geometry of the drawn curve.

**Safe variables.**
- the modelled context
- the letters used
- the window of the field

**Difficulty variables.**
- whether an equilibrium level runs through the window
- where the initial point sits relative to it
- how far the curve must extend

Mapped difficulty factors: BC-DF-01 (Number of concepts combined)

**Expected solution path.**
- locate the initial point in the field
- follow the segments to the right and to the left
- keep the curve on the correct side of the horizontal segments
- extend to the edges of the rectangle

**Prohibited shortcuts.**
- none recorded in this record

**Multi-skill extensions.**
- none recorded in this record

### BC-QA-07002 Slope field matched to or built from a differential equation

Evidence tag: inferred. Scope: shared. Primary unit: BC-UNIT-07. Units: BC-UNIT-07. Sources: ced:139, ced:140, sg-23:9.

**Description.** The response must produce the segments of a field at named points, or decide which of several equations produced a printed field.

**Concepts and skills required.** BC-SKL-07010, BC-SKL-07011, BC-SKL-07012, BC-SKL-07013, BC-SKL-07016

**Prerequisites.** BC-PRQ-07006

**Typical wording.**
- sketch the slope field for the given differential equation at the indicated points
- which of the following differential equations could have produced the slope field shown

**Common givens.**
- a differential equation or a printed field
- a set of lattice points

**What is produced.**
- segment slopes at named points
- or a matched equation

**Representations.** BC-REP-06 (Differential equation), BC-REP-07 (Slope field)

**Calculator status.** no_calculator

**Multipart structure.** A single multiple choice item, or a short free response part.

**Scoring pattern.** Scored in the same shape as the printed field part: the drawing is accepted when the segments agree with the computed slopes, including the horizontal ones (sg-23:9).

**Scoring point types.** none recorded. Point type definitions are in [../scoring/point-taxonomy.md](../scoring/point-taxonomy.md).

**Common distractors.**
- evaluating the right side at the wrong lattice point
- drawing all segments with the same tilt
- matching on the visual density of the field rather than on the zero slope locus

**Wrong approaches.**
- solving the equation and differentiating the solution

**Misconceptions.** BC-MIS-07006, BC-MIS-07007

**Variants.** 3 recorded: BC-QV-07002-01, BC-QV-07002-02, BC-QV-07002-03

**Official examples notes.** none in 2023 to 2025

**Invariant structure.** The slope at a point comes from substituting the coordinates into the right side, and the pattern of the field is settled by which variables the right side contains.

**Safe variables.**
- the grid spacing
- the letters used
- the window

**Difficulty variables.**
- whether the right side contains one variable or both
- whether the zero slope locus is a line or a curve
- how many candidate equations share a feature

Mapped difficulty factors: BC-DF-01 (Number of concepts combined)

**Expected solution path.**
- find where the right side vanishes
- evaluate the right side at two or three distinguishing points
- compare with the printed field

**Prohibited shortcuts.**
- none recorded in this record

**Multi-skill extensions.**
- none recorded in this record

## Family squeeze-theorem [inferred]

1 archetype(s): BC-QA-01005.

### BC-QA-01005 Limit determined by the squeeze theorem with its hypotheses stated

Evidence tag: inferred. Scope: shared. Primary unit: BC-UNIT-01. Units: BC-UNIT-01. Sources: ced:45.

**Description.** A function trapped between two bounding functions is presented and the response verifies the bounding inequality, evaluates the bounds, and concludes the limit.

**Concepts and skills required.** BC-SKL-01032, BC-SKL-01033, BC-SKL-01034, BC-SKL-01035

**Prerequisites.** BC-PRQ-01005, BC-PRQ-01010

**Typical wording.**
- The stated inequality holds near the given input. Use it to determine the limit of the trapped function and justify your answer.

**Common givens.**
- none recorded in this record

**What is produced.**
- none recorded in this record

**Representations.** BC-REP-01 (Symbolic (analytical) expression), BC-REP-02 (Graphical)

**Calculator status.** no_calculator

**Multipart structure.** Typically one part of a multipart free response question or a single multiple choice item.

**Scoring pattern.** One point for establishing the bounding inequality, one for the limits of the two bounds, and one for the conclusion. No official free response part in 2023 to 2025 assesses the squeeze theorem.

**Scoring point types.** none recorded. Point type definitions are in [../scoring/point-taxonomy.md](../scoring/point-taxonomy.md).

**Common distractors.**
- multiplying the inequality by a factor that changes sign without reversing it
- evaluating the bounds at the target rather than taking their limits
- concluding from a bound on one side only
- omitting the statement that the bounds share a limit

**Wrong approaches.**
- none recorded in this record; see ../misconceptions/error-to-concept-map.md

**Misconceptions.** BC-MIS-01008

**Variants.** 3 recorded: BC-QV-01005-01, BC-QV-01005-02, BC-QV-01005-03

**Official examples notes.** none in 2023 to 2025 [inferred]

**Invariant structure.** The bounding inequality holds near the target but not necessarily at it, and the two bounds share a limit there, so the conclusion rests on the theorem rather than on direct evaluation.

**Safe variables.**
- the bounded oscillating factor
- the vanishing factor
- the target input

**Difficulty variables.**
- whether the bounding functions are supplied or must be produced
- whether the inequality must be verified in the response
- whether the target is zero or another input
- whether the theorem must be named

Mapped difficulty factors: BC-DF-09 (Theorem recognition), BC-DF-13 (Reversed reasoning direction)

**Expected solution path.**
- bound the oscillating factor between fixed values
- multiply the inequality by the vanishing factor and record the direction of the inequality
- evaluate the limits of the two bounds
- observe that they agree and state the conclusion

**Prohibited shortcuts.**
- none recorded in this record

**Multi-skill extensions.**
- none recorded in this record

## Family tangent-line-approximation [verified]

2 archetype(s): BC-QA-02011, BC-QA-04008.

### BC-QA-02011 Tangent line written at a point on a curve

Evidence tag: inferred. Scope: shared. Primary unit: BC-UNIT-02. Units: BC-UNIT-02. Sources: ced:61.

**Description.** A function is given and the response produces the equation of the line tangent to its graph at a named point.

**Concepts and skills required.** BC-SKL-02012, BC-SKL-02013

**Prerequisites.** BC-PRQ-02003

**Typical wording.**
- Write an equation for the line tangent to the graph of the given function at the named point.

**Common givens.**
- none recorded in this record

**What is produced.**
- none recorded in this record

**Representations.** BC-REP-01 (Symbolic (analytical) expression), BC-REP-02 (Graphical)

**Calculator status.** no_calculator

**Multipart structure.** Typically one part of a multipart free response question.

**Scoring pattern.** One point for the slope from the derivative, one for the point of tangency, and one for the equation.

**Scoring point types.** none recorded. Point type definitions are in [../scoring/point-taxonomy.md](../scoring/point-taxonomy.md).

**Common distractors.**
- using the function value as the slope
- using the derivative value as the point
- writing the line through the origin
- evaluating the derivative at the wrong input

**Wrong approaches.**
- none recorded in this record; see ../misconceptions/error-to-concept-map.md

**Misconceptions.** BC-MIS-02014

**Variants.** 3 recorded: BC-QV-02011-01, BC-QV-02011-02, BC-QV-02011-03

**Official examples notes.** none in 2023 to 2025 as a standalone part [inferred]

**Invariant structure.** The slope comes from the derivative evaluated at the input and the point of tangency comes from the function evaluated there, so two separate evaluations feed one line equation.

**Safe variables.**
- the function
- the point of tangency
- the variable names

**Difficulty variables.**
- whether the point of tangency must be computed
- whether the derivative needs a product or quotient rule
- whether the line is then used to approximate a value
- whether the answer must be in a stated form

Mapped difficulty factors: BC-DF-08 (Multi-step dependency)

**Expected solution path.**
- differentiate the function
- evaluate the derivative at the input to get the slope
- evaluate the function at the input to get the point
- write the line in point slope form

**Prohibited shortcuts.**
- none recorded in this record

**Multi-skill extensions.**
- none recorded in this record

### BC-QA-04008 Tangent line approximation with an over or under estimate judgement

Evidence tag: verified. Scope: shared. Primary unit: BC-UNIT-04. Units: BC-UNIT-04. Sources: ced:92, cr-24:17, crabbc-25:24, crabbc-25:25.

**Description.** A point on a curve and the derivative there are supplied, and the response approximates a nearby function value with the tangent line and may be asked whether the approximation is too large or too small.

**Concepts and skills required.** BC-SKL-04028, BC-SKL-04029, BC-SKL-04030, BC-SKL-04031, BC-SKL-04032

**Prerequisites.** BC-PRQ-04006, BC-PRQ-04008

**Typical wording.**
- use the line tangent to the curve at the stated point to approximate the value of the function at a nearby input

**Common givens.**
- none recorded in this record

**What is produced.**
- none recorded in this record

**Representations.** BC-REP-01 (Symbolic (analytical) expression), BC-REP-02 (Graphical)

**Calculator status.** either

**Multipart structure.** One part of a multipart free response question, ordinarily following a part that produced the derivative.

**Scoring pattern.** The Chief Reader reports record that most responses that found the slope also wrote the tangent line and produced an approximation, with arithmetic errors arising from unnecessary simplification, and that a response could earn the approximation point on an incorrect slope (cr-24:17, crabbc-25:25); a claim about the direction of the error that does not appeal to concavity is recorded as a standing error (BC-ERR-99020).

**Scoring point types.** none recorded. Point type definitions are in [../scoring/point-taxonomy.md](../scoring/point-taxonomy.md).

**Common distractors.**
- the point and the slope exchanged in the point-slope form
- the direction of the error argued from whether the function is increasing
- the approximation evaluated at the point of tangency rather than at the nearby input
- an arithmetic error introduced while isolating the dependent variable unnecessarily

**Wrong approaches.**
- none recorded in this record; see ../misconceptions/error-to-concept-map.md

**Misconceptions.** BC-MIS-04012, BC-MIS-04013

**Variants.** 3 recorded: BC-QV-04008-01, BC-QV-04008-02, BC-QV-04008-03

**Official examples notes.** 2024 AB Q5(a), 2025 AB Q6 part B, as described in the Chief Reader reports

**Invariant structure.** The tangent line at the point of tangency is evaluated at the nearby input; the direction of the error follows from the concavity of the graph on an interval containing both inputs, not from the sign of the first derivative.

**Safe variables.**
- the curve
- the point of tangency
- the nearby input
- whether the curve is given explicitly or implicitly

**Difficulty variables.**
- whether the slope must be computed by implicit differentiation
- whether an over or under estimate judgement is demanded
- whether the second derivative must be produced to support the judgement
- whether the answer must be simplified

Mapped difficulty factors: BC-DF-06 (Algebraic burden), BC-DF-10 (Required justification)

**Expected solution path.**
- find the slope at the point of tangency
- write the tangent line in point-slope form
- evaluate at the nearby input
- determine the concavity near the point
- state the direction of the error with the concavity as the reason

**Prohibited shortcuts.**
- none recorded in this record

**Multi-skill extensions.**
- none recorded in this record

## Family taylor-construction [verified]

7 archetype(s): BC-QA-10010, BC-QA-10011, BC-QA-10012, BC-QA-10016, BC-QA-10017, BC-QA-10018, BC-QA-10019.

### BC-QA-10010 Taylor polynomial built from repeated differentiation of a relation

Evidence tag: verified. Scope: BC_only. Primary unit: BC-UNIT-10. Units: BC-UNIT-10. Sources: sg-23:19.

**Description.** Derivatives are defined by a relation, the response differentiates to the required order, evaluates at the centre, and assembles the polynomial.

**Concepts and skills required.** BC-SKL-10043, BC-SKL-10044, BC-SKL-10046

**Prerequisites.** none recorded

**Typical wording.**
- find the next derivative and write the Taylor polynomial of the stated degree about the centre, showing the work that leads to the answer

**Common givens.**
- none recorded in this record

**What is produced.**
- none recorded in this record

**Representations.** BC-REP-01 (Symbolic (analytical) expression)

**Calculator status.** no_calculator

**Multipart structure.** Typically one part of the multipart free response question that closes Section II Part B, or a single multiple choice item.

**Scoring pattern.** Four points are typical, for the form of the product rule, the derivative itself, two terms of the polynomial, and the remaining terms; a response that earns the form point but not the derivative point may still use its own value consistently, and a polynomial with a nonzero term of the wrong degree or a trailing ellipsis loses the final point (sg-23:19).

**Scoring point types.** none recorded. Point type definitions are in [../scoring/point-taxonomy.md](../scoring/point-taxonomy.md).

**Common distractors.**
- omitting a product rule factor
- placing derivative values directly as coefficients
- including a term of higher degree than requested

**Wrong approaches.**
- none recorded in this record; see ../misconceptions/error-to-concept-map.md

**Misconceptions.** BC-MIS-10019, BC-MIS-10020

**Variants.** 3 recorded: BC-QV-10010-01, BC-QV-10010-02, BC-QV-10010-03

**Official examples notes.** 2023 Q6(a)

**Invariant structure.** Values of the function and its first derivatives at the centre are given, with later derivatives defined by an expression in the earlier ones; each new derivative requires a product or chain rule step.

**Safe variables.**
- the centre
- the initial values
- the order requested

**Difficulty variables.**
- the order of differentiation required
- whether a product rule is needed
- whether some coefficients vanish

Mapped difficulty factors: BC-DF-01 (Number of concepts combined)

**Expected solution path.**
- differentiate the given relation
- evaluate each derivative at the centre in order
- divide each value by the matching factorial
- write the polynomial to the requested degree and no further

**Prohibited shortcuts.**
- none recorded in this record

**Multi-skill extensions.**
- none recorded in this record

### BC-QA-10011 Taylor polynomial built from a table of derivative values

Evidence tag: inferred. Scope: BC_only. Primary unit: BC-UNIT-10. Units: BC-UNIT-10. Sources: ced:196, sg-23:19.

**Description.** A table lists the function and several derivatives at a point and the response assembles the requested Taylor polynomial.

**Concepts and skills required.** BC-SKL-10044, BC-SKL-10045

**Prerequisites.** none recorded

**Typical wording.**
- use the values in the table to write the Taylor polynomial of the stated degree for the function about the given centre

**Common givens.**
- none recorded in this record

**What is produced.**
- none recorded in this record

**Representations.** BC-REP-03 (Numerical table), BC-REP-01 (Symbolic (analytical) expression)

**Calculator status.** no_calculator

**Multipart structure.** Typically one part of the multipart free response question that closes Section II Part B, or a single multiple choice item.

**Scoring pattern.** Scored as a polynomial construction, with the coefficients carrying the credit; no rubric for this exact task appears in the 2021 to 2025 free response material read for this unit, so the pattern is inferred from the closely related construction parts (sg-23:19).

**Scoring point types.** none recorded. Point type definitions are in [../scoring/point-taxonomy.md](../scoring/point-taxonomy.md).

**Common distractors.**
- omitting the factorials
- pairing a derivative with the wrong power
- extending the polynomial beyond the requested degree

**Wrong approaches.**
- none recorded in this record; see ../misconceptions/error-to-concept-map.md

**Misconceptions.** BC-MIS-10019

**Variants.** 2 recorded: BC-QV-10011-01, BC-QV-10011-02

**Official examples notes.** none in 2021 to 2025

**Invariant structure.** The derivative values at the centre are supplied rather than computed; the work lies in matching each value to its factorial and power.

**Safe variables.**
- the centre
- the values in the table
- the letters naming the function

**Difficulty variables.**
- the degree requested
- whether the centre is zero
- whether an approximation of a function value follows

Mapped difficulty factors: BC-DF-01 (Number of concepts combined)

**Expected solution path.**
- read the derivative values of the needed orders
- divide each by the matching factorial
- attach the power of the displacement from the centre
- present the polynomial of the requested degree

**Prohibited shortcuts.**
- none recorded in this record

**Multi-skill extensions.**
- none recorded in this record

### BC-QA-10012 Taylor polynomial for a related function built from a known series

Evidence tag: verified. Scope: BC_only. Primary unit: BC-UNIT-10. Units: BC-UNIT-10. Sources: sg-23:20, sg-23:21.

**Description.** A second function is defined from the first by a product, a derivative, or an antiderivative, and its Taylor polynomial is requested.

**Concepts and skills required.** BC-SKL-10046, BC-SKL-10047, BC-SKL-10048, BC-SKL-10061, BC-SKL-10065

**Prerequisites.** none recorded

**Typical wording.**
- write the Taylor polynomial of the stated degree for the second function about the given centre

**Common givens.**
- none recorded in this record

**What is produced.**
- none recorded in this record

**Representations.** BC-REP-01 (Symbolic (analytical) expression), BC-REP-11 (Series (finite partial sums or infinite))

**Calculator status.** no_calculator

**Multipart structure.** Typically one part of the multipart free response question that closes Section II Part B, or a single multiple choice item.

**Scoring pattern.** Three points are typical, for the derivative relation, for the first two terms, and for the complete polynomial; a polynomial of the right shape earns the terms point without supporting work, while a coefficient with no support does not earn the final point, and an alternate solution through known Maclaurin series earns the same three points (sg-23:20, sg-23:21).

**Scoring point types.** none recorded. Point type definitions are in [../scoring/point-taxonomy.md](../scoring/point-taxonomy.md).

**Common distractors.**
- misremembering a standard series
- omitting a product rule factor
- presenting a polynomial with terms of higher degree

**Wrong approaches.**
- none recorded in this record; see ../misconceptions/error-to-concept-map.md

**Misconceptions.** BC-MIS-10020, BC-MIS-10021

**Variants.** 3 recorded: BC-QV-10012-01, BC-QV-10012-02, BC-QV-10012-03

**Official examples notes.** 2023 Q6(c)

**Invariant structure.** The polynomial for the related function can be reached either by differentiating the defining relation and evaluating at the centre, or by operating on known Maclaurin series and truncating.

**Safe variables.**
- the defining relation
- the centre
- the degree requested

**Difficulty variables.**
- whether a product rule is needed
- whether an initial value fixes a constant
- whether the known series route is shorter

Mapped difficulty factors: BC-DF-01 (Number of concepts combined)

**Expected solution path.**
- differentiate or expand the defining relation
- evaluate the needed derivatives at the centre, or multiply the known series
- divide by the factorials
- present the polynomial of the requested degree

**Prohibited shortcuts.**
- none recorded in this record

**Multi-skill extensions.**
- none recorded in this record

### BC-QA-10016 First nonzero terms and the general term of a series

Evidence tag: verified. Scope: BC_only. Primary unit: BC-UNIT-10. Units: BC-UNIT-10. Sources: sg-25:26, sg-24:22.

**Description.** The response presents a stated number of nonzero terms of a Taylor series together with its general term.

**Concepts and skills required.** BC-SKL-10060, BC-SKL-10067

**Prerequisites.** none recorded

**Typical wording.**
- find the first three nonzero terms and the general term of the Taylor series for the function about the given centre

**Common givens.**
- none recorded in this record

**What is produced.**
- none recorded in this record

**Representations.** BC-REP-11 (Series (finite partial sums or infinite)), BC-REP-01 (Symbolic (analytical) expression)

**Calculator status.** no_calculator

**Multipart structure.** Typically one part of the multipart free response question that closes Section II Part B, or a single multiple choice item.

**Scoring pattern.** Two points are typical, one for the first terms presented in a list or as part of a series, and one for the general term identified individually or inside the series (sg-25:26).

**Scoring point types.** none recorded. Point type definitions are in [../scoring/point-taxonomy.md](../scoring/point-taxonomy.md).

**Common distractors.**
- a general term that does not reproduce the displayed terms
- an index offset by one
- a missing alternating factor

**Wrong approaches.**
- none recorded in this record; see ../misconceptions/error-to-concept-map.md

**Misconceptions.** BC-MIS-10020

**Variants.** 3 recorded: BC-QV-10016-01, BC-QV-10016-02, BC-QV-10016-03

**Official examples notes.** 2025 Q6(B)

**Invariant structure.** The terms and the general term are scored separately; the general term must reproduce the displayed terms when the index takes its first values.

**Safe variables.**
- the centre
- the function
- the number of terms requested

**Difficulty variables.**
- whether an alternating factor is present
- whether the series is the derivative or the antiderivative of a given series
- whether factorials appear

Mapped difficulty factors: BC-DF-02 (Prerequisite depth), BC-DF-06 (Algebraic burden)

**Expected solution path.**
- produce the required terms from derivatives or from a known series
- detect the pattern in the coefficients and the powers
- write a general term in the index
- check the general term against the displayed terms

**Prohibited shortcuts.**
- none recorded in this record

**Multi-skill extensions.**
- none recorded in this record

### BC-QA-10017 Maclaurin series built from a known series by substitution or multiplication

Evidence tag: verified. Scope: BC_only. Primary unit: BC-UNIT-10. Units: BC-UNIT-10. Sources: ced:199, ced:200, sg-23:21.

**Description.** A function is written as a substitution into, or a multiple of, one of the standard Maclaurin series and the resulting series is requested.

**Concepts and skills required.** BC-SKL-10061, BC-SKL-10062, BC-SKL-10063, BC-SKL-10064, BC-SKL-10065

**Prerequisites.** none recorded

**Typical wording.**
- use a known Maclaurin series to find the series for the given function

**Common givens.**
- none recorded in this record

**What is produced.**
- none recorded in this record

**Representations.** BC-REP-01 (Symbolic (analytical) expression), BC-REP-11 (Series (finite partial sums or infinite))

**Calculator status.** no_calculator

**Multipart structure.** Typically one part of the multipart free response question that closes Section II Part B, or a single multiple choice item.

**Scoring pattern.** Scored through the terms produced, as in the 2023 alternate solution where the series identifications carry the points for a related polynomial (sg-23:21).

**Scoring point types.** none recorded. Point type definitions are in [../scoring/point-taxonomy.md](../scoring/point-taxonomy.md).

**Common distractors.**
- substituting without raising the whole expression to the power
- misremembering the parity or the signs of a standard series
- shifting the centre

**Wrong approaches.**
- none recorded in this record; see ../misconceptions/error-to-concept-map.md

**Misconceptions.** BC-MIS-10021, BC-MIS-10026

**Variants.** 3 recorded: BC-QV-10017-01, BC-QV-10017-02, BC-QV-10017-03

**Official examples notes.** 2023 Q6(c) alternate solution

**Invariant structure.** The standard series for the exponential, the sine, the cosine, or one over one minus x is recalled and transformed term by term; the centre stays where it was.

**Safe variables.**
- which standard series is used
- the substituted expression
- the multiplying factor

**Difficulty variables.**
- whether the substitution raises the powers
- whether a constant multiple is also involved
- whether the interval of convergence must be adjusted

Mapped difficulty factors: BC-DF-06 (Algebraic burden), BC-DF-08 (Multi-step dependency)

**Expected solution path.**
- recall the standard series
- substitute the expression for the variable, raising every power
- multiply through by any factor
- collect the first terms and the general term

**Prohibited shortcuts.**
- none recorded in this record

**Multi-skill extensions.**
- none recorded in this record

### BC-QA-10018 Series differentiated term by term with its radius carried over

Evidence tag: verified. Scope: BC_only. Primary unit: BC-UNIT-10. Units: BC-UNIT-10. Sources: sg-24:22, sg-25:26, ced:198.

**Description.** A power series is differentiated term by term and the response reports the new series and its radius of convergence.

**Concepts and skills required.** BC-SKL-10060, BC-SKL-10068, BC-SKL-10070, BC-SKL-10071

**Prerequisites.** none recorded

**Typical wording.**
- find the general term of the series for the derivative and state its radius of convergence

**Common givens.**
- none recorded in this record

**What is produced.**
- none recorded in this record

**Representations.** BC-REP-11 (Series (finite partial sums or infinite)), BC-REP-01 (Symbolic (analytical) expression)

**Calculator status.** no_calculator

**Multipart structure.** Typically one part of the multipart free response question that closes Section II Part B, or a single multiple choice item.

**Scoring pattern.** Two points are typical, one for the general term and one for the radius, with the radius point resting on the statement that term-by-term differentiation preserves it (sg-24:22). The 2025 form scores the first terms and the general term separately (sg-25:26).

**Scoring point types.** none recorded. Point type definitions are in [../scoring/point-taxonomy.md](../scoring/point-taxonomy.md).

**Common distractors.**
- differentiating with respect to the index
- recomputing and misreporting the radius
- carrying the original interval including its endpoints

**Wrong approaches.**
- none recorded in this record; see ../misconceptions/error-to-concept-map.md

**Misconceptions.** BC-MIS-10020, BC-MIS-10022, BC-MIS-10023, BC-MIS-10024, BC-MIS-10025

**Variants.** 3 recorded: BC-QV-10018-01, BC-QV-10018-02, BC-QV-10018-03

**Official examples notes.** 2024 Q6(c), 2025 Q6(B)

**Invariant structure.** Each displayed term and the general term are differentiated; the radius is inherited from the original series rather than recomputed, while endpoint behaviour is a separate question.

**Safe variables.**
- the original series
- the centre
- the number of terms requested

**Difficulty variables.**
- whether the general term carries a factorial
- whether the radius must be justified by the preservation statement
- whether the endpoints must be rechecked

Mapped difficulty factors: BC-DF-02 (Prerequisite depth), BC-DF-04 (Notation complexity), BC-DF-10 (Required justification), BC-DF-14 (Missing or implicit given)

**Expected solution path.**
- differentiate the displayed terms
- differentiate the general term with respect to the variable
- state that the radius is unchanged
- recheck the endpoints if the interval is requested

**Prohibited shortcuts.**
- none recorded in this record

**Multi-skill extensions.**
- none recorded in this record

### BC-QA-10019 Function represented by term-by-term integration of a known series

Evidence tag: verified. Scope: BC_only. Primary unit: BC-UNIT-10. Units: BC-UNIT-10. Sources: ced:200, sg-23:21.

**Description.** A known series is integrated term by term to represent an antiderivative, with the constant fixed by a given value.

**Concepts and skills required.** BC-SKL-10069

**Prerequisites.** none recorded

**Typical wording.**
- use a known series to find a power series representation of the function

**Common givens.**
- none recorded in this record

**What is produced.**
- none recorded in this record

**Representations.** BC-REP-11 (Series (finite partial sums or infinite)), BC-REP-01 (Symbolic (analytical) expression)

**Calculator status.** no_calculator

**Multipart structure.** Typically one part of the multipart free response question that closes Section II Part B, or a single multiple choice item.

**Scoring pattern.** Scored through the terms and the constant; the 2023 alternate solution treats the antidifferentiated series and the constant determined from the initial value as the supporting work for the requested polynomial (sg-23:21).

**Scoring point types.** none recorded. Point type definitions are in [../scoring/point-taxonomy.md](../scoring/point-taxonomy.md).

**Common distractors.**
- omitting the constant of integration
- integrating with respect to the index
- changing the radius

**Wrong approaches.**
- none recorded in this record; see ../misconceptions/error-to-concept-map.md

**Misconceptions.** BC-MIS-10020

**Variants.** 2 recorded: BC-QV-10019-01, BC-QV-10019-02

**Official examples notes.** 2023 Q6(c) alternate solution

**Invariant structure.** Each term of the known series is antidifferentiated, the general term follows the same pattern, and a supplied value at one input determines the constant.

**Safe variables.**
- the known series used
- the input where the value is supplied
- the centre

**Difficulty variables.**
- whether the constant is zero
- whether the integrand arrives from a substitution
- whether the radius or the interval is requested afterwards

Mapped difficulty factors: BC-DF-06 (Algebraic burden)

**Expected solution path.**
- write the series for the integrand
- antidifferentiate term by term including the general term
- determine the constant from the supplied value
- state the radius as unchanged if it is requested

**Prohibited shortcuts.**
- none recorded in this record

**Multi-skill extensions.**
- none recorded in this record

## Family taylor-error [verified]

3 archetype(s): BC-QA-10008, BC-QA-10009, BC-QA-10020.

### BC-QA-10008 Alternating series error bound compared with a tolerance

Evidence tag: verified. Scope: BC_only. Primary unit: BC-UNIT-10. Units: BC-UNIT-10. Sources: sg-22:21, sg-24:21, sg-21:25.

**Description.** A partial sum approximates the value of an alternating series and the response bounds the error by the first omitted term and compares it with a stated number.

**Concepts and skills required.** BC-SKL-10028, BC-SKL-10029, BC-SKL-10039, BC-SKL-10040, BC-SKL-10041, BC-SKL-10042, BC-SKL-10052, BC-SKL-10066

**Prerequisites.** none recorded

**Typical wording.**
- show that the partial sum differs from the value of the series by less than the given amount

**Common givens.**
- none recorded in this record

**What is produced.**
- none recorded in this record

**Representations.** BC-REP-11 (Series (finite partial sums or infinite)), BC-REP-01 (Symbolic (analytical) expression)

**Calculator status.** no_calculator

**Multipart structure.** Typically one part of the multipart free response question that closes Section II Part B, or a single multiple choice item.

**Scoring pattern.** Two points are typical, one for using the correct omitted term and one for the justification; the justification requires the conditions and the inequality, and an equality statement does not earn it (sg-22:21, sg-24:21). A single point form asks only for an upper bound on the error (sg-21:25).

**Scoring point types.** none recorded. Point type definitions are in [../scoring/point-taxonomy.md](../scoring/point-taxonomy.md).

**Common distractors.**
- using a term already inside the partial sum
- using a term further along than the first omitted one
- writing the error as equal to the bound
- omitting the statement of the conditions

**Wrong approaches.**
- none recorded in this record; see ../misconceptions/error-to-concept-map.md

**Misconceptions.** BC-MIS-10012, BC-MIS-10013, BC-MIS-10017, BC-MIS-10018

**Variants.** 3 recorded: BC-QV-10008-01, BC-QV-10008-02, BC-QV-10008-03

**Official examples notes.** 2022 Q6(b), 2024 Q6(b), 2021 Q6(d)

**Invariant structure.** The series alternates with terms decreasing in absolute value to zero; the error of the stated partial sum is at most the absolute value of the next term, which is evaluated and compared with a tolerance.

**Safe variables.**
- the number of terms in the partial sum
- the input at which the series is evaluated
- the tolerance

**Difficulty variables.**
- whether the tolerance is supplied or an upper bound alone is requested
- whether the series arrives from a Taylor series evaluated at a point
- the index of the first omitted term

Mapped difficulty factors: BC-DF-08 (Multi-step dependency)

**Expected solution path.**
- state that the series alternates and its terms decrease in absolute value to zero
- identify the first omitted term
- evaluate that term at the given input
- present the inequality that the error is at most that value and that value is at most the tolerance

**Prohibited shortcuts.**
- none recorded in this record

**Multi-skill extensions.**
- none recorded in this record

### BC-QA-10009 Lagrange error bound with a supplied derivative bound

Evidence tag: verified. Scope: BC_only. Primary unit: BC-UNIT-10. Units: BC-UNIT-10. Sources: sg-23:20.

**Description.** A bound on the next derivative is supplied on an interval and the response shows that a Taylor polynomial approximation lies within a stated tolerance.

**Concepts and skills required.** BC-SKL-10048, BC-SKL-10049, BC-SKL-10050, BC-SKL-10051, BC-SKL-10052

**Prerequisites.** none recorded

**Typical wording.**
- use the Lagrange error bound to show that the approximation is within the stated amount of the exact value

**Common givens.**
- none recorded in this record

**What is produced.**
- none recorded in this record

**Representations.** BC-REP-01 (Symbolic (analytical) expression), BC-REP-04 (Verbal description)

**Calculator status.** no_calculator

**Multipart structure.** Typically one part of the multipart free response question that closes Section II Part B, or a single multiple choice item.

**Scoring pattern.** Two points are typical, one for the form of the bound and one for showing the error is at most the tolerance; subsequent simplification errors cost the second point only, and an equality statement earns neither the second point (sg-23:20).

**Scoring point types.** none recorded. Point type definitions are in [../scoring/point-taxonomy.md](../scoring/point-taxonomy.md).

**Common distractors.**
- using the derivative of the same order as the polynomial
- omitting the factorial
- writing the error as equal to the bound
- stopping before the comparison with the tolerance

**Wrong approaches.**
- none recorded in this record; see ../misconceptions/error-to-concept-map.md

**Misconceptions.** BC-MIS-10017, BC-MIS-10018

**Variants.** 2 recorded: BC-QV-10009-01, BC-QV-10009-02

**Official examples notes.** 2023 Q6(b)

**Invariant structure.** A polynomial of stated degree approximates a function value near the centre; the bound is the supplied maximum of the next derivative times the power of the displacement divided by the factorial of the next order.

**Safe variables.**
- the degree of the polynomial
- the centre
- the supplied derivative bound
- the tolerance

**Difficulty variables.**
- whether the derivative bound is supplied or must be found
- the displacement from the centre
- whether the comparison with the tolerance must be shown

Mapped difficulty factors: BC-DF-14 (Missing or implicit given)

**Expected solution path.**
- identify the order of the derivative the bound needs
- write the bound in the correct form
- evaluate it
- present the inequality against the tolerance

**Prohibited shortcuts.**
- none recorded in this record

**Multi-skill extensions.**
- none recorded in this record

### BC-QA-10020 Convergence to the function at a specified input decided with a reason

Evidence tag: verified. Scope: BC_only. Primary unit: BC-UNIT-10. Units: BC-UNIT-10. Sources: sg-25:27.

**Description.** The response decides whether a series converges to the function at a stated input and gives the position of that input relative to the interval as the reason.

**Concepts and skills required.** BC-SKL-10007, BC-SKL-10010, BC-SKL-10073

**Prerequisites.** none recorded

**Typical wording.**
- does the series converge to the function at the stated input, and give a reason for the answer

**Common givens.**
- none recorded in this record

**What is produced.**
- none recorded in this record

**Representations.** BC-REP-11 (Series (finite partial sums or infinite)), BC-REP-04 (Verbal description)

**Calculator status.** no_calculator

**Multipart structure.** Typically one part of the multipart free response question that closes Section II Part B, or a single multiple choice item.

**Scoring pattern.** One point for the answer with a reason; a short response naming the input as outside the interval suffices, the point is available with an interval imported from an earlier part even when that interval is wrong, and a geometric ratio argument is an accepted alternative (sg-25:27).

**Scoring point types.** none recorded. Point type definitions are in [../scoring/point-taxonomy.md](../scoring/point-taxonomy.md).

**Common distractors.**
- answering with no reason
- treating the series as valid for all inputs
- using the interior of the interval as though it were closed

**Wrong approaches.**
- none recorded in this record; see ../misconceptions/error-to-concept-map.md

**Misconceptions.** BC-MIS-10003, BC-MIS-10023

**Variants.** 2 recorded: BC-QV-10020-01, BC-QV-10020-02

**Official examples notes.** 2025 Q6(D)

**Invariant structure.** An interval of convergence, found earlier or supplied, is compared with a specific input, and the verdict follows from whether the input lies inside it.

**Safe variables.**
- the input chosen
- the closed form supplied
- the interval imported from an earlier part

**Difficulty variables.**
- whether the input lies just outside an endpoint
- whether the interval must be imported from an earlier part
- whether a geometric argument is available as an alternative

Mapped difficulty factors: BC-DF-01 (Number of concepts combined), BC-DF-02 (Prerequisite depth), BC-DF-08 (Multi-step dependency), BC-DF-10 (Required justification), BC-DF-14 (Missing or implicit given)

**Expected solution path.**
- state the interval of convergence in play
- locate the input relative to it
- state whether the series converges to the function there
- give the position as the reason

**Prohibited shortcuts.**
- none recorded in this record

**Multi-skill extensions.**
- none recorded in this record

## Family technology-numerical-result [single-source]

1 archetype(s): BC-QA-02013.

### BC-QA-02013 Derivative at a point produced with technology

Evidence tag: single-source. Scope: shared. Primary unit: BC-UNIT-02. Units: BC-UNIT-02. Sources: ced:62, sg-25:4.

**Description.** A function is supplied in a calculator active setting and the response reports the value of its derivative at a named input.

**Concepts and skills required.** BC-SKL-02018

**Prerequisites.** BC-PRQ-02004

**Typical wording.**
- Find the value of the derivative at the named input. Show the setup for your calculations.

**Common givens.**
- none recorded in this record

**What is produced.**
- none recorded in this record

**Representations.** BC-REP-09 (Calculator-generated numerical result), BC-REP-05 (Contextual model)

**Calculator status.** calculator

**Multipart structure.** Typically one part of a multipart free response question.

**Scoring pattern.** One point for the setup that names the quantity computed and one for the value, where an answer is expected to three places after the decimal point and an inappropriately rounded answer does not earn the point unless an earlier point was already lost to rounding (sg-25:4).

**Scoring point types.** none recorded. Point type definitions are in [../scoring/point-taxonomy.md](../scoring/point-taxonomy.md).

**Common distractors.**
- reporting the function value instead of the derivative value
- evaluating at the wrong input
- rounding to fewer places than required
- presenting a bare value with no setup

**Wrong approaches.**
- none recorded in this record; see ../misconceptions/error-to-concept-map.md

**Misconceptions.** BC-MIS-02015

**Variants.** 3 recorded: BC-QV-02013-01, BC-QV-02013-02, BC-QV-02013-03

**Official examples notes.** 2023 Q1(d) evaluates a derivative from a supplied model in a calculator active part

**Invariant structure.** The value is produced by calculator capability rather than by hand, and the response must present the setup that identifies the quantity being computed as well as the value to the required precision.

**Safe variables.**
- the modelled quantity
- the formula
- the input at which the derivative is requested
- the units

**Difficulty variables.**
- whether the setup must be shown
- whether the answer must be interpreted in context
- whether an equation must be solved before the derivative is evaluated
- whether the precision requirement is the deciding factor

Mapped difficulty factors: BC-DF-02 (Prerequisite depth), BC-DF-05 (Contextual interpretation), BC-DF-08 (Multi-step dependency)

**Expected solution path.**
- enter the function
- request the numerical derivative at the named input
- report the value to three places after the decimal point
- interpret the value with units when asked

**Prohibited shortcuts.**
- none recorded in this record

**Multi-skill extensions.**
- none recorded in this record

## Retired archetypes and their canonical records [inferred]

Two unit agents wrote the same reasoning structure from their own side of the course. The weaker record is retired with a tombstone in `../../data/ids.json`, and the canonical record carries the union of the skills, variants, units, and official example notes of both.

| Retired | Name | Superseded by | Canonical family |
|---|---|---|---|
| BC-QA-02001 | Derivative estimated from a table with units | BC-QA-04002 | derivative-from-table |
| BC-QA-06007 | Average value of a function over an interval | BC-QA-08001 | average-value |
| BC-QA-08004 | Amount at a later time from an initial amount and a rate | BC-QA-06005 | accumulation-with-initial-condition |
| BC-QA-08005 | Accumulation with a rate in and a rate out | BC-QA-06006 | rate-in-rate-out |
| BC-QA-08007 | Interpreting a definite integral of a rate in context | BC-QA-06015 | accumulation-interpretation |

Genuinely different reasoning structures stayed apart. BC-QA-04003 and BC-QA-08003 both treat rectilinear motion but one differentiates a position function and the other integrates a velocity function. BC-QA-08012 and BC-QA-08013 both revolve a region but the washer method carries an inner radius that the disc method has no analogue for. BC-QA-08014 and BC-QA-09003 both produce a length but from different integrands.

## Archetypes added from documented gaps [inferred]

Ten archetypes were minted in block 99 from the archetype gaps recorded in the notes of `../../data/frq_records.json` and listed in [../evidence/unresolved-questions.md](../evidence/unresolved-questions.md). Each one was minted only where the reasoning structure differs from the closest existing record, which is the rule the catalogue above follows. One documented gap did not meet that rule: the average value of a radial function along a polar curve keeps the invariant structure of BC-QA-08001, one function over one interval divided by the length of the interval, so it is recorded as the variant BC-QV-08001-04 (Average value of a radial function over an angle interval, harder, dimension representation, from frq-19:3 and sg-19:3) rather than as an archetype. The section is tagged inferred because the decision to split a reasoning structure is a research judgement, not a College Board statement; the sources on each record are the documents the structure and the scoring were read from.

### BC-QA-99001 Polar tangent slope relation solved for the derivative of the horizontal coordinate

Evidence tag: verified. Scope: BC_only. Primary unit: BC-UNIT-09. Units: BC-UNIT-09, BC-UNIT-03. Sources: frq-26:4, sg-26:7.

**Description.** A polar curve is given, the slope of the tangent line at an unnamed point is supplied, and the derivative of the vertical coordinate with respect to the angle at that same point is supplied. The response must write the chain rule relation among the three Leibniz derivatives and solve it for the derivative of the horizontal coordinate with respect to the angle.

**Family.** polar-calculus

**Concepts and skills required.** BC-SKL-09033, BC-SKL-09002, BC-SKL-09003, BC-SKL-03002

**Prerequisites.** BC-PRQ-09003, BC-PRQ-03002

**Typical wording.**
- there is a point on the curve at which the slope of the line tangent to the curve is a given value
- find the derivative of the horizontal coordinate with respect to the angle at this point, showing the work that leads to the answer

**Common givens.**
- a polar equation
- the derivative of the radial function
- the slope of the tangent at an unnamed point
- the derivative of the vertical coordinate with respect to the angle at that point

**What is produced.**
- the chain rule relation
- the substitution of the supplied values
- the value of the derivative of the horizontal coordinate

**Representations.** BC-REP-13 (Polar equation), BC-REP-01 (Symbolic (analytical) expression)

**Calculator status.** calculator

**Multipart structure.** One part of a multipart polar free response question, worth three points.

**Scoring pattern.** Three points. One for any correct arrangement of the chain rule relation among the three Leibniz derivatives, one for stating or substituting the supplied slope into an equation that contains the wanted derivative, and one for the value with or without supporting work. A single equation that combines the relation and the substituted values earns all three when the later simplification is correct (sg-26:7).

**Scoring point types.** BC-PT-99049, BC-PT-99005, BC-PT-99004. Point type definitions are in [../scoring/point-taxonomy.md](../scoring/point-taxonomy.md).

**Common distractors.**
- the reciprocal of the correct value
- the value of the derivative of the radial function
- the slope itself reported as the answer
- the correct magnitude with the sign lost

**Wrong approaches.**
- differentiating the polar equation and reporting dr/dtheta

**Misconceptions.** BC-MIS-09014, BC-MIS-09015

**Official examples.** BC-FRQ-2026-Q2-B

**Invariant structure.** The relation dy/dx equals dy/dtheta divided by dx/dtheta is used in reverse: two of the three derivatives are supplied and the third is the unknown, so the response rearranges the relation algebraically before substituting. No differentiation of the polar equation is required.

**Safe variables.**
- the polar equation
- the supplied slope
- the supplied vertical derivative
- the names of the coordinates

**Difficulty variables.**
- which of the three derivatives is withheld
- whether the supplied slope is negative
- whether the point is named by an angle or left unnamed
- whether the work must be shown

Mapped difficulty factors: BC-DF-04 (Notation complexity), BC-DF-08 (Multi-step dependency), BC-DF-13 (Reversed reasoning direction)

**Expected solution path.**
- write dy/dx as the quotient of dy/dtheta by dx/dtheta
- rearrange the relation so that dx/dtheta stands alone
- substitute the supplied slope and the supplied vertical derivative
- report the value

**Prohibited shortcuts.**
- multiplying the slope by the vertical derivative instead of dividing
- substituting the derivative of the radial function for the derivative of the horizontal coordinate

**Multi-skill extensions.**
- the same part may first require the area of the polar region, as in 2026 Q2

**Record note.** Split from BC-QA-09001 because the relation is solved rather than evaluated; the reasoning direction is reversed. Recorded from the documented archetype gap on BC-FRQ-2026-Q2-B.

### BC-QA-99002 Derivative of a Cartesian coordinate with respect to theta on a polar curve

Evidence tag: verified. Scope: BC_only. Primary unit: BC-UNIT-09. Units: BC-UNIT-09, BC-UNIT-03. Sources: samples-14-q2:1.

**Description.** A polar equation is given and the response must produce the derivative with respect to the angle of one Cartesian coordinate of the curve, which means writing that coordinate as the radial function times the cosine or sine of the angle and differentiating the product before evaluating at a stated angle.

**Family.** polar-calculus

**Concepts and skills required.** BC-SKL-09030, BC-SKL-09031, BC-SKL-09029, BC-SKL-09033

**Prerequisites.** BC-PRQ-09003, BC-PRQ-09002

**Typical wording.**
- for the given polar curve, find the value of the derivative of the horizontal coordinate with respect to the angle at a stated angle

**Common givens.**
- a polar equation
- a stated angle

**What is produced.**
- an expression for the Cartesian coordinate in terms of the angle
- the value of its derivative at the stated angle

**Representations.** BC-REP-13 (Polar equation), BC-REP-01 (Symbolic (analytical) expression), BC-REP-09 (Calculator-generated numerical result)

**Calculator status.** calculator

**Multipart structure.** One part of a multipart polar free response question, worth two points.

**Scoring pattern.** Two points. One for a correct expression for the Cartesian coordinate or its derivative in terms of the angle, and one for the value at the stated angle; the expression point is separate from the answer point, so a value with no displayed expression forfeits the first (samples-14-q2:1).

**Scoring point types.** BC-PT-99049, BC-PT-99005, BC-PT-99004. Point type definitions are in [../scoring/point-taxonomy.md](../scoring/point-taxonomy.md).

**Common distractors.**
- the derivative of the radial function
- the radial function evaluated at the angle
- the product rule reduced to one term
- the sign of the sine term lost

**Wrong approaches.**
- treating the coordinate as the radial function itself

**Misconceptions.** BC-MIS-09014, BC-MIS-09015

**Official examples.** BC-FRQ-2014-Q2-B

**Invariant structure.** The conversion from the polar equation to a Cartesian coordinate happens first and the product rule is applied to that conversion; the derivative of the radial function alone is an intermediate quantity and never the answer.

**Safe variables.**
- the polar equation
- which Cartesian coordinate is requested
- the stated angle

**Difficulty variables.**
- horizontal versus vertical coordinate
- whether the expression for the coordinate must be displayed
- whether the radial function itself needs the chain rule
- whether the angle is a multiple of a familiar value

Mapped difficulty factors: BC-DF-04 (Notation complexity), BC-DF-06 (Algebraic burden), BC-DF-13 (Reversed reasoning direction)

**Expected solution path.**
- write the requested coordinate as the radial function times the cosine or the sine of the angle
- differentiate the product with respect to the angle
- substitute the stated angle
- report the value

**Prohibited shortcuts.**
- reporting the derivative of the radial function as the answer

**Multi-skill extensions.**
- the same expression is reused when a tangent slope or a position vector is requested later in the question

**Record note.** Split from BC-QA-09009 because the polar to Cartesian conversion and the product rule are the reasoning, not the differentiation of the radial function. Recorded from the documented archetype gap on BC-FRQ-2014-Q2-B.

### BC-QA-99003 Slope of the tangent line to a polar curve at a stated angle

Evidence tag: single-source. Scope: BC_only. Primary unit: BC-UNIT-09. Units: BC-UNIT-09, BC-UNIT-03. Sources: frq-18:6.

**Description.** A polar equation is given and the response must produce the slope of the tangent line to the curve in the plane at a stated angle, which requires both Cartesian coordinates to be written in terms of the angle, both differentiated, and the quotient formed.

**Family.** polar-calculus

**Concepts and skills required.** BC-SKL-09030, BC-SKL-09031, BC-SKL-09029, BC-SKL-09033

**Prerequisites.** BC-PRQ-09003, BC-PRQ-09002

**Typical wording.**
- find the slope of the line tangent to the graph of the polar curve at a stated angle

**Common givens.**
- a polar equation
- a figure showing the curve
- a stated angle

**What is produced.**
- both Cartesian coordinates as functions of the angle
- both derivatives
- the slope as their quotient

**Representations.** BC-REP-13 (Polar equation), BC-REP-02 (Graphical), BC-REP-01 (Symbolic (analytical) expression)

**Calculator status.** no_calculator

**Multipart structure.** One part of a multipart polar free response question.

**Scoring pattern.** No scoring guideline for 2018 is in the corpus, so no rubric wording is recorded for this archetype and the record is tagged single-source from the free-response document alone (frq-18:6).

**Scoring point types.** none recorded. Point type definitions are in [../scoring/point-taxonomy.md](../scoring/point-taxonomy.md).

**Common distractors.**
- the derivative of the radial function
- the reciprocal of the slope
- the tangent of the stated angle
- a quotient built from the radial function and its derivative

**Wrong approaches.**
- using the parametric slope formula with the radial function as one coordinate

**Misconceptions.** BC-MIS-09014, BC-MIS-09015

**Official examples.** BC-FRQ-2018-Q5-B

**Invariant structure.** Two conversions and two product rule differentiations feed one quotient; the slope is a Cartesian quantity built from a polar description, so neither the radial function nor its derivative can stand in for it.

**Safe variables.**
- the polar equation
- the stated angle
- whether a figure is supplied

**Difficulty variables.**
- whether the stated angle makes one derivative vanish
- whether the derivative of the radial function is supplied
- whether a calculator is available
- whether the curve is one of two in the figure

Mapped difficulty factors: BC-DF-01 (Number of concepts combined), BC-DF-04 (Notation complexity), BC-DF-06 (Algebraic burden), BC-DF-08 (Multi-step dependency)

**Expected solution path.**
- write the horizontal and vertical coordinates as the radial function times the cosine and the sine of the angle
- differentiate each product with respect to the angle
- evaluate both derivatives at the stated angle
- report the quotient of the vertical derivative by the horizontal derivative

**Prohibited shortcuts.**
- reporting the derivative of the radial function as the slope
- reporting the reciprocal quotient

**Multi-skill extensions.**
- the same derivatives support a related rates part later in the question

**Record note.** Split from BC-QA-09009 because the quantity produced is a Cartesian slope rather than the derivative of the radial function. Recorded from the documented archetype gap on BC-FRQ-2018-Q5-B. Tagged single-source because only the free-response document is cached for 2018.

### BC-QA-99004 Time at which a Cartesian coordinate of a particle on a polar path reaches a value

Evidence tag: verified. Scope: BC_only. Primary unit: BC-UNIT-09. Units: BC-UNIT-09. Sources: samples-13-q2:1.

**Description.** A particle travels a polar curve with the angle given as a function of time. The response must express one Cartesian coordinate in terms of time and solve the resulting equation for the time at which that coordinate equals a stated value, within a stated time interval.

**Family.** polar-motion

**Concepts and skills required.** BC-SKL-09030, BC-SKL-09029, BC-SKL-09032

**Prerequisites.** BC-PRQ-09003, BC-PRQ-09002

**Typical wording.**
- find the time in the stated interval for which the horizontal coordinate of the particle's position is a given value

**Common givens.**
- a polar equation
- the angle as a function of time
- a target coordinate value
- a time interval

**What is produced.**
- the coordinate as a function of the angle or of time
- the equation set equal to the target value
- the time

**Representations.** BC-REP-13 (Polar equation), BC-REP-05 (Contextual model), BC-REP-09 (Calculator-generated numerical result)

**Calculator status.** calculator

**Multipart structure.** One part of a multipart polar motion free response question, worth three points.

**Scoring pattern.** Three points. One for the coordinate written in terms of the angle or of time, one for the equation set equal to the stated value in either variable, and one for the time; the expression and equation points are awarded separately, so an unsupported numerical time earns only the answer point (samples-13-q2:1).

**Scoring point types.** BC-PT-99005, BC-PT-99004. Point type definitions are in [../scoring/point-taxonomy.md](../scoring/point-taxonomy.md).

**Common distractors.**
- the angle at which the coordinate reaches the value
- a time outside the stated interval
- the radial value rather than the Cartesian coordinate
- the vertical coordinate solved in place of the horizontal

**Wrong approaches.**
- equating the radial function to the stated coordinate value

**Misconceptions.** BC-MIS-09014

**Official examples.** BC-FRQ-2013-Q2-B

**Invariant structure.** Two substitutions and one equation: the radial function is converted to a Cartesian coordinate, the angle is replaced by its expression in time, and the resulting single equation is solved numerically inside the stated interval, which is what makes the solution unique.

**Safe variables.**
- the polar equation
- the relation between the angle and time
- the target value
- the interval

**Difficulty variables.**
- whether the coordinate is written in the angle or directly in time
- whether the interval contains more than one solution to the untruncated equation
- which Cartesian coordinate is named
- whether the target value is attained at an endpoint

Mapped difficulty factors: BC-DF-01 (Number of concepts combined), BC-DF-07 (Calculator workflow), BC-DF-08 (Multi-step dependency), BC-DF-14 (Missing or implicit given)

**Expected solution path.**
- write the requested Cartesian coordinate as the radial function times the cosine or sine of the angle
- substitute the angle as a function of time
- set the expression equal to the stated value
- solve numerically inside the stated interval and report the time

**Prohibited shortcuts.**
- solving for the angle and reporting it as the time

**Multi-skill extensions.**
- the expression built here is reused for the position vector in the following part

**Record note.** No existing archetype covers converting a polar path to a Cartesian coordinate function of time and solving an equation against it. Recorded from the documented archetype gap on BC-FRQ-2013-Q2-B.

### BC-QA-99005 Position and velocity vectors for a particle travelling a polar curve

Evidence tag: verified. Scope: BC_only. Primary unit: BC-UNIT-09. Units: BC-UNIT-09. Sources: samples-13-q2:1.

**Description.** A particle travels a polar curve with the angle given as a function of time. The response must give the position vector in terms of time, built from both Cartesian conversions, and then the velocity vector at a stated time by differentiating both components.

**Family.** polar-motion

**Concepts and skills required.** BC-SKL-09030, BC-SKL-09029, BC-SKL-09015, BC-SKL-09016

**Prerequisites.** BC-PRQ-09003, BC-PRQ-09001

**Typical wording.**
- find the position vector in terms of time and find the velocity vector at a stated time

**Common givens.**
- a polar equation
- the angle as a function of time
- a stated time

**What is produced.**
- the position vector as an ordered pair in time
- the velocity vector at the stated time

**Representations.** BC-REP-13 (Polar equation), BC-REP-14 (Vector-valued function), BC-REP-09 (Calculator-generated numerical result)

**Calculator status.** calculator

**Multipart structure.** One part of a multipart polar motion free response question, worth three points.

**Scoring pattern.** Three points, two for the position vector and one for the velocity vector, so the two components of the position carry the weight and the velocity is a single point at the stated time (samples-13-q2:1).

**Scoring point types.** BC-PT-99064, BC-PT-99005, BC-PT-99004. Point type definitions are in [../scoring/point-taxonomy.md](../scoring/point-taxonomy.md).

**Common distractors.**
- the polar pair given as the position vector
- one component differentiated and the other copied
- the velocity reported as a speed
- the vector evaluated at the wrong time

**Wrong approaches.**
- differentiating the radial function alone and calling it the velocity

**Misconceptions.** BC-MIS-09009, BC-MIS-09014

**Official examples.** BC-FRQ-2013-Q2-C

**Invariant structure.** One ordered pair is assembled from two polar conversions and then differentiated componentwise; the same conversion supports both the position and the velocity, so an error in either component propagates into both vectors.

**Safe variables.**
- the polar equation
- the relation between the angle and time
- the stated time

**Difficulty variables.**
- whether the position vector is requested in the angle or in time
- whether the velocity is requested symbolically or numerically
- whether the components must be labelled
- whether the derivative is taken by hand or on the calculator

Mapped difficulty factors: BC-DF-01 (Number of concepts combined), BC-DF-04 (Notation complexity), BC-DF-07 (Calculator workflow), BC-DF-08 (Multi-step dependency)

**Expected solution path.**
- write both Cartesian coordinates as the radial function times the cosine and the sine of the angle
- substitute the angle as a function of time in both components
- present the ordered pair as the position vector
- differentiate both components and evaluate at the stated time for the velocity vector

**Prohibited shortcuts.**
- reporting the radial function and the angle as the position vector

**Multi-skill extensions.**
- a speed or total distance part can be built on the same components

**Record note.** Distinct from BC-QA-09004, which differentiates supplied component velocities; here the components must first be built from a polar description. Recorded from the documented archetype gap on BC-FRQ-2013-Q2-C.

### BC-QA-99006 Rate of change with respect to theta of the gap between two polar curves

Evidence tag: verified. Scope: BC_only. Primary unit: BC-UNIT-09. Units: BC-UNIT-09. Sources: samples-14-q2:1.

**Description.** Two polar curves are given over an angle interval on which they do not meet. The response must write the distance between them along a ray as the difference of the two radial functions, differentiate that difference with respect to the angle, and evaluate at a stated angle.

**Family.** polar-calculus

**Concepts and skills required.** BC-SKL-09029, BC-SKL-09031, BC-SKL-09033

**Prerequisites.** BC-PRQ-09003, BC-PRQ-09002

**Typical wording.**
- the distance between the two curves changes over an angle interval; find the rate at which the distance between the two curves is changing with respect to the angle at a stated angle

**Common givens.**
- two polar equations
- a figure showing both curves
- an angle interval on which they do not meet
- a stated angle

**What is produced.**
- an expression for the distance between the curves
- the value of its derivative at the stated angle

**Representations.** BC-REP-13 (Polar equation), BC-REP-02 (Graphical), BC-REP-09 (Calculator-generated numerical result)

**Calculator status.** calculator

**Multipart structure.** One part of a multipart polar free response question, worth two points.

**Scoring pattern.** Two points. One for an expression for the distance between the curves and one for the value of its derivative at the stated angle, so a correct value with no displayed difference forfeits the first point (samples-14-q2:1).

**Scoring point types.** BC-PT-99005, BC-PT-99004. Point type definitions are in [../scoring/point-taxonomy.md](../scoring/point-taxonomy.md).

**Common distractors.**
- the derivative of one curve only
- the difference evaluated instead of its derivative
- the sign of the difference reversed
- an area of the region between the curves

**Wrong approaches.**
- measuring the gap as a Cartesian distance between two points

**Misconceptions.** BC-MIS-09014, BC-MIS-09017

**Official examples.** BC-FRQ-2014-Q2-C

**Invariant structure.** A new function is defined as the difference of the two radial functions before any differentiation occurs; the derivative is taken of that difference, not of either curve separately, and the sign of the difference is fixed by which curve is outside on the interval.

**Safe variables.**
- the two polar equations
- which curve is outside
- the stated angle
- the interval

**Difficulty variables.**
- whether one of the curves is a constant radius
- whether the expression for the distance must be displayed
- whether the sign of the difference must be argued from the figure
- whether the stated angle is inside the region shown

Mapped difficulty factors: BC-DF-01 (Number of concepts combined), BC-DF-08 (Multi-step dependency), BC-DF-12 (Sign and direction handling), BC-DF-14 (Missing or implicit given)

**Expected solution path.**
- decide from the figure or the interval which radial function is larger
- write the distance as that difference
- differentiate the difference with respect to the angle
- evaluate at the stated angle and report the value

**Prohibited shortcuts.**
- differentiating only the non-constant curve without writing the difference

**Multi-skill extensions.**
- the area of the region between the same two curves is a natural neighbouring part

**Record note.** Distinct from BC-QA-09009 because a difference function must be defined before any differentiation. Recorded from the documented archetype gap on BC-FRQ-2014-Q2-C.

### BC-QA-99007 Average rate of change reported on its own with units

Evidence tag: verified. Scope: shared. Primary unit: BC-UNIT-08. Units: BC-UNIT-08, BC-UNIT-02. Sources: samples-14-q1:1.

**Description.** A modelling function is given on a closed interval and the response must report the average rate of change of that function over the interval, with units, and nothing else. No equation is formed and no derivative is used.

**Family.** average-rate-of-change

**Concepts and skills required.** BC-SKL-08004, BC-SKL-08003

**Prerequisites.** BC-PRQ-08001

**Typical wording.**
- find the average rate of change of the modelling function over the stated interval, indicating units of measure

**Common givens.**
- a modelling function
- a closed interval
- the units of the modelled quantity

**What is produced.**
- the value of the difference quotient with units

**Representations.** BC-REP-01 (Symbolic (analytical) expression), BC-REP-05 (Contextual model), BC-REP-09 (Calculator-generated numerical result)

**Calculator status.** calculator

**Multipart structure.** The opening part of a multipart contextual free response question, worth one point.

**Scoring pattern.** One point for the answer with units, so the setup earns nothing on its own and a correct value without units earns nothing either (samples-14-q1:1).

**Scoring point types.** BC-PT-99021, BC-PT-99006, BC-PT-99004. Point type definitions are in [../scoring/point-taxonomy.md](../scoring/point-taxonomy.md).

**Common distractors.**
- the derivative at an endpoint
- the average value of the function over the interval
- the difference of the endpoint values with no division
- the value reported without units

**Wrong approaches.**
- integrating the function and dividing by the interval length

**Misconceptions.** BC-MIS-08001

**Official examples.** BC-FRQ-2014-Q1-A

**Invariant structure.** One difference quotient over the stated interval, evaluated and reported; the interval endpoints supply both the numerator differences and the denominator, and the answer carries the units of the modelled quantity per unit of the input.

**Safe variables.**
- the modelled quantity
- the formula
- the interval endpoints
- the units

**Difficulty variables.**
- whether the function is given by a formula, a table, or a graph
- whether units are demanded in the same part
- whether the quantity is decreasing so the answer is negative
- whether the endpoints must be evaluated on a calculator

Mapped difficulty factors: BC-DF-05 (Contextual interpretation), BC-DF-07 (Calculator workflow), BC-DF-12 (Sign and direction handling), BC-DF-16 (Units and labelling demand)

**Expected solution path.**
- evaluate the function at both endpoints of the interval
- divide the difference of the values by the length of the interval
- report the value with units

**Prohibited shortcuts.**
- reporting the derivative at an endpoint in place of the average rate

**Multi-skill extensions.**
- a later part of the same question may set an instantaneous rate equal to this value, which is BC-QA-08002

**Record note.** Split from BC-QA-08002, whose invariant requires the difference quotient to be set equal to a derivative and solved. Recorded from the documented archetype gap on BC-FRQ-2014-Q1-A.

### BC-QA-99008 Total amount from a rate over an interval with no initial condition and no rate out

Evidence tag: verified. Scope: shared. Primary unit: BC-UNIT-06. Units: BC-UNIT-06, BC-UNIT-08. Sources: samples-13-q1:1, samples-15-q1:1, frq-18:2.

**Description.** A single contextual rate is given over a closed interval and the response must report the total amount that the rate accounts for over that interval. No starting amount is supplied and no second rate removes anything, so the definite integral of the rate is the whole answer.

**Family.** accumulation-total-from-rate

**Concepts and skills required.** BC-SKL-06036, BC-SKL-06037, BC-SKL-08012

**Prerequisites.** BC-PRQ-06002, BC-PRQ-06005

**Typical wording.**
- find the total amount of the quantity that arrives during the hours of operation
- how many units of the quantity flow in during the stated time interval

**Common givens.**
- a rate function, possibly piecewise
- a closed interval
- the units of the rate

**What is produced.**
- the definite integral of the rate over the interval
- its value

**Representations.** BC-REP-01 (Symbolic (analytical) expression), BC-REP-05 (Contextual model), BC-REP-09 (Calculator-generated numerical result)

**Calculator status.** calculator

**Multipart structure.** Usually the opening part of a multipart contextual free response question, worth two points.

**Scoring pattern.** Two points, one for the integral or the integrand and one for the value; the distractor is the level term and the outflow rate that the stem supplies for later parts, and neither belongs in this integral (samples-13-q1:1, samples-15-q1:1).

**Scoring point types.** BC-PT-99001, BC-PT-99002, BC-PT-99004. Point type definitions are in [../scoring/point-taxonomy.md](../scoring/point-taxonomy.md).

**Common distractors.**
- the initial amount added to the integral
- the outflow rate subtracted inside the integral
- the rate evaluated at an endpoint
- the net change of the stored quantity rather than the inflow

**Wrong approaches.**
- treating the part as a net change question because the stem gives an initial condition

**Misconceptions.** BC-MIS-06013, BC-MIS-08006

**Official examples.** BC-FRQ-2013-Q1-B, BC-FRQ-2015-Q1-A, BC-FRQ-2018-Q1-A

**Invariant structure.** One rate, one interval, one definite integral, and no level term: the question names the quantity that flows in rather than the quantity present, so nothing is added to the integral and nothing is subtracted from it.

**Safe variables.**
- the quantity accumulating
- the formula for the rate
- the interval endpoints
- the units

**Difficulty variables.**
- whether the rate is piecewise so the interval must be split or the correct branch chosen
- whether a second rate is present in the stem but irrelevant to this part
- whether an initial amount is stated in the stem but not used in this part
- whether the answer must be rounded to a whole number

Mapped difficulty factors: BC-DF-07 (Calculator workflow), BC-DF-14 (Missing or implicit given), BC-DF-15 (Unsignposted procedure selection), BC-DF-17 (Case splitting at a boundary)

**Expected solution path.**
- read the interval out of the wording of the part
- write the definite integral of the rate over that interval
- evaluate on the calculator
- report the value, rounded as the part demands

**Prohibited shortcuts.**
- adding the stated initial amount, which belongs to a different part
- subtracting the second rate, which belongs to a different part

**Multi-skill extensions.**
- the neighbouring parts of the same question are usually BC-QA-06005 or BC-QA-06006, which do use the level term and the second rate

**Record note.** Split from BC-QA-06005, whose invariant requires an initial value added to the integral. Recorded from the documented archetype gap on BC-FRQ-2013-Q1-B, BC-FRQ-2015-Q1-A, and BC-FRQ-2018-Q1-A.

### BC-QA-99009 Density accumulated over a spatial interval scaled by a constant cross-section

Evidence tag: single-source. Scope: BC_only. Primary unit: BC-UNIT-08. Units: BC-UNIT-08, BC-UNIT-06. Sources: frq-18:3.

**Description.** A density per unit volume is modelled as a function of depth and a column of constant horizontal cross-sectional area is described. The response must integrate the density over the depth interval and multiply by the constant area to report the total amount in the column.

**Family.** accumulation-of-density

**Concepts and skills required.** BC-SKL-06036, BC-SKL-08012, BC-SKL-08005

**Prerequisites.** BC-PRQ-06005, BC-PRQ-08006

**Typical wording.**
- consider a vertical column with horizontal cross sections of constant area; to the nearest million, how many units are in this column between the stated depths

**Common givens.**
- a density function of depth
- a constant cross-sectional area
- a depth interval
- a rounding instruction

**What is produced.**
- the integral of the density over the depth interval
- the product with the constant area
- the rounded count

**Representations.** BC-REP-01 (Symbolic (analytical) expression), BC-REP-05 (Contextual model), BC-REP-09 (Calculator-generated numerical result)

**Calculator status.** calculator

**Multipart structure.** One part of a multipart contextual free response question.

**Scoring pattern.** No scoring guideline for 2018 is in the corpus, so no rubric wording is recorded for this archetype and the record is tagged single-source from the free-response document alone (frq-18:3).

**Scoring point types.** none recorded. Point type definitions are in [../scoring/point-taxonomy.md](../scoring/point-taxonomy.md).

**Common distractors.**
- the integral reported without the constant factor
- the density evaluated at a depth
- the area multiplied by a density value rather than by the integral
- the answer left unrounded against the instruction

**Wrong approaches.**
- treating the constant cross-section as a variable cross-section and squaring it

**Misconceptions.** BC-MIS-06014, BC-MIS-08015

**Official examples.** BC-FRQ-2018-Q2-B

**Invariant structure.** The integral is taken over a length and the constant area converts the result into a count; the accumulating variable is a depth rather than a time, and the constant factor sits outside the integral because the cross-section does not vary.

**Safe variables.**
- the modelled population
- the density formula
- the cross-sectional area
- the depth interval

**Difficulty variables.**
- whether the constant factor is stated in the same part or earlier in the stem
- whether the density is given piecewise across the depth interval
- whether the answer must be rounded to a named place
- whether the units of the density are per unit volume or per unit length

Mapped difficulty factors: BC-DF-03 (Unusual representation), BC-DF-05 (Contextual interpretation), BC-DF-07 (Calculator workflow), BC-DF-11 (Unfamiliar surface presentation)

**Expected solution path.**
- write the definite integral of the density over the stated depth interval
- multiply by the constant cross-sectional area
- evaluate on the calculator
- round as the part instructs and report with the stated unit

**Prohibited shortcuts.**
- reporting the integral of the density without the area factor

**Multi-skill extensions.**
- the following part of the same question bounds the accumulation below the modelled depth, which is BC-QA-99010

**Record note.** Distinct from BC-QA-06005 and from BC-QA-08011 because the accumulating variable is a depth and the geometric factor is a constant outside the integral. Recorded from the documented archetype gap on BC-FRQ-2018-Q2-B. Tagged single-source because only the free-response document is cached for 2018.

### BC-QA-99010 Accumulation bounded above by a comparison function with a supplied improper integral

Evidence tag: single-source. Scope: BC_only. Primary unit: BC-UNIT-06. Units: BC-UNIT-06, BC-UNIT-08. Sources: frq-18:3.

**Description.** A function is modelled explicitly on one interval and only bounded above by a comparison function beyond it, with the improper integral of the comparison function supplied. The response must write the whole accumulation as a sum of integrals and then explain why the total cannot exceed a stated bound.

**Family.** integral-comparison-bound

**Concepts and skills required.** BC-SKL-06029, BC-SKL-06030, BC-SKL-06035

**Prerequisites.** BC-PRQ-06005

**Typical wording.**
- write an expression involving one or more integrals that gives the total quantity in the entire column
- explain why the total quantity is less than or equal to the stated bound

**Common givens.**
- a function modelled on a first interval
- a comparison function bounding it beyond that interval
- the value of the improper integral of the comparison function
- an unknown finite endpoint

**What is produced.**
- the sum of integrals for the whole interval
- an inequality argument for the stated bound

**Representations.** BC-REP-01 (Symbolic (analytical) expression), BC-REP-04 (Verbal description), BC-REP-05 (Contextual model)

**Calculator status.** calculator

**Multipart structure.** One part of a multipart contextual free response question, combining an expression and an explanation.

**Scoring pattern.** No scoring guideline for 2018 is in the corpus, so no rubric wording is recorded for this archetype and the record is tagged single-source from the free-response document alone (frq-18:3).

**Scoring point types.** none recorded. Point type definitions are in [../scoring/point-taxonomy.md](../scoring/point-taxonomy.md).

**Common distractors.**
- the comparison function used as the model on the second interval
- the improper integral used as the whole answer
- the split point omitted so a single integral is written
- the bound asserted without the inequality

**Wrong approaches.**
- claiming the total converges rather than bounding it

**Misconceptions.** BC-MIS-06026

**Official examples.** BC-FRQ-2018-Q2-C

**Invariant structure.** Additivity splits the interval at the point where the model changes, and the comparison inequality bounds the second piece; the supplied improper integral is an upper bound for a definite integral over any finite interval beyond the split, so the explanation rests on the inequality rather than on evaluating anything.

**Safe variables.**
- the modelled quantity
- the split point
- the bound supplied for the improper integral
- the name of the unknown endpoint

**Difficulty variables.**
- whether the comparison function is given explicitly or only named
- whether the endpoint beyond the split is unknown
- whether the constant factor from an earlier part must be carried in
- whether the explanation must reference the nonnegativity of the function

Mapped difficulty factors: BC-DF-08 (Multi-step dependency), BC-DF-09 (Theorem recognition), BC-DF-10 (Required justification), BC-DF-14 (Missing or implicit given)

**Expected solution path.**
- split the accumulation at the depth where the model changes
- write the first piece as a definite integral of the explicit model and the second as a definite integral of the unknown function
- bound the second piece by the integral of the comparison function and then by its supplied improper value
- add the two bounds and state that the total cannot exceed the stated figure

**Prohibited shortcuts.**
- evaluating the unknown function, which is not given explicitly

**Multi-skill extensions.**
- the preceding part of the same question supplies the first integral, which is BC-QA-99009

**Record note.** Distinct from BC-QA-06013 because an inequality between two functions carries the argument rather than the algebraic properties of the integral alone. Recorded from the documented archetype gap on BC-FRQ-2018-Q2-C. Tagged single-source because only the free-response document is cached for 2018.
