---
title: Prerequisite Map
research_date: 2026-09-19
status: draft
purpose: Direct prerequisites of every CED unit grouped by category, the indirect chains that carry the ten most consequential skills forward, and the hidden non-calculus prerequisites with the observed errors they produce.
---

# Prerequisite Map

Two kinds of prerequisite appear. A BC-PRQ record is a non-calculus ability, minted in `../../data/skills.json` under `prerequisites`, that the CED assumes rather than teaches. A BC-SKL record from an earlier unit is calculus content the course has already covered. Both are edges in `../../data/prereq_edges.csv`, typed `hard_prerequisite` when the downstream skill cannot be performed without the upstream one and `supporting` otherwise. Counts in brackets after an id are the number of skills in that unit which carry an edge from it.

## How to read the groupings [inferred]

The `category` field on a BC-PRQ record takes eight values in the registry: algebra, trigonometry, function, precalculus, notation, conceptual, geometry, arithmetic. The headings below fold `function` and `precalculus` into one group, function knowledge, and keep the rest separate. The earlier calculus group is not a category on any record; it is derived by comparing the unit block of the two endpoint ids of each edge. Every BC-PRQ record in the registry carries `hidden: true`, so the hidden prerequisite section below is the whole prerequisite registry read from the error side rather than a subset of it.

## BC-UNIT-01 Limits and Continuity direct prerequisites [inferred]

68 skills, CED pages 32-53.

**Algebra.** BC-PRQ-01001 Factoring polynomials and dividing out a common factor [8]; BC-PRQ-01006 Absolute value rewritten as a piecewise expression [2]; BC-PRQ-01002 Rationalising a numerator or denominator with a conjugate [1]; BC-PRQ-01007 Simplifying a complex fraction [1].

**Trigonometry.** BC-PRQ-01005 Exact trigonometric values and the bounds on sine and cosine [4].

**Function knowledge.** BC-PRQ-01003 Reading a piecewise defined function rule [10]; BC-PRQ-01008 Domain of rational, radical, logarithmic, and trigonometric expressions [6]; BC-PRQ-01004 End behaviour of a rational function from degree comparison [5].

**Notation.** BC-PRQ-06005 Reading function notation, composition, and evaluation [23]; BC-PRQ-01010 Interval and inequality notation for open and closed intervals [7].

**Arithmetic and numeracy.** BC-PRQ-01009 Sign analysis of a quotient near a zero of the denominator [4].

**Earlier calculus.** None. This unit opens the course and carries its load on the non-calculus prerequisites above.

## BC-UNIT-02 Differentiation: Definition and Fundamental Properties direct prerequisites [inferred]

46 skills, CED pages 54-69.

**Algebra.** BC-PRQ-02001 Expanding and simplifying a difference quotient [3]; BC-PRQ-06002 Exponent rules including negative and fractional exponents [3]; BC-PRQ-06003 Logarithm rules and properties of the natural logarithm [1].

**Trigonometry.** BC-PRQ-02002 Reciprocal and quotient trigonometric identities [2]; BC-PRQ-01005 Exact trigonometric values and the bounds on sine and cosine [1].

**Function knowledge.** BC-PRQ-02005 Recognising a function value at a shifted input [5]; BC-PRQ-02003 Slope of a line through two points and the point slope form [2].

**Notation.** BC-PRQ-02004 Prime notation and Leibniz notation conventions [4].

**Earlier calculus.** BC-UNIT-01 supplies 14 upstream records across 21 edges: BC-SKL-01001, BC-SKL-01003, BC-SKL-01005, BC-SKL-01009, BC-SKL-01010, BC-SKL-01012, BC-SKL-01016, BC-SKL-01018, BC-SKL-01024, BC-SKL-01036, BC-SKL-01040, BC-SKL-01043, and others.

## BC-UNIT-03 Differentiation: Composite, Implicit, and Inverse Functions direct prerequisites [inferred]

34 skills, CED pages 70-80.

**Algebra.** BC-PRQ-03006 Simplifying rational and radical expressions [8]; BC-PRQ-03002 Solving a linear equation for an embedded factor [3]; BC-PRQ-03007 Deciding when an expression is zero or undefined [2].

**Trigonometry.** BC-PRQ-03004 Unit circle values, Pythagorean identities, and right triangle ratios [5].

**Function knowledge.** BC-PRQ-03001 Decomposing a formula into an outer and an inner function [9]; BC-PRQ-03003 Definition of an inverse function and reading matched pairs [6].

**Notation.** BC-PRQ-03005 Reading and writing prime and Leibniz derivative notation [9].

**Earlier calculus.** BC-UNIT-02 supplies 9 upstream records across 9 edges: BC-SKL-02021, BC-SKL-02027, BC-SKL-02036, BC-SKL-02039, BC-SKL-02046, BC-TOP-0202, BC-TOP-0207, BC-TOP-0208, BC-TOP-0209.

## BC-UNIT-04 Contextual Applications of Differentiation direct prerequisites [inferred]

38 skills, CED pages 82-93.

**Algebra.** BC-PRQ-04006 Point-slope form of a line [3]; BC-PRQ-04009 Sign analysis of an expression over an interval [3]; BC-PRQ-04005 Absolute value as size without sign [2]; BC-PRQ-04007 Solving a linear equation for one unknown quantity [2].

**Conceptual.** BC-PRQ-04008 Translating a verbal scenario into named variables [22].

**Geometry and measurement.** BC-PRQ-04001 Volume and area formulas for standard solids [1]; BC-PRQ-04002 The Pythagorean theorem and right triangle relations [1]; BC-PRQ-04003 Similar triangles and proportional reasoning [1].

**Arithmetic and numeracy.** BC-PRQ-04004 Unit analysis with compound units [5].

**Earlier calculus.** BC-UNIT-01 supplies 5 upstream records across 5 edges: BC-SKL-01028, BC-SKL-01058, BC-SKL-01060, BC-TOP-0102, BC-TOP-0111. BC-UNIT-02 supplies 6 upstream records across 6 edges: BC-SKL-02003, BC-SKL-02013, BC-TOP-0201, BC-TOP-0202, BC-TOP-0208, BC-TOP-0209. BC-UNIT-03 supplies 4 upstream records across 5 edges: BC-SKL-03028, BC-TOP-0301, BC-TOP-0302, BC-TOP-0306. BC-UNIT-05 supplies 1 upstream record across 1 edge: BC-TOP-0506.

## BC-UNIT-05 Applying Derivatives to Analyze Functions direct prerequisites [inferred]

63 skills, CED pages 94-110.

**Algebra.** BC-PRQ-05001 Solving equations and inequalities to locate where an expression is zero or undefined [8]; BC-PRQ-05007 Solving a system made of a defining relation and a derived equation [4].

**Function knowledge.** BC-PRQ-05003 Domain of a function, including piecewise, rational, and radical forms [6]; BC-PRQ-05006 Reading features of a graph, including where a graph rises, falls, and changes bending [4]; BC-PRQ-05008 Average rate of change over an interval as a difference quotient [1].

**Notation.** BC-PRQ-05004 Interval notation and the open versus closed distinction [3]; BC-PRQ-06005 Reading function notation, composition, and evaluation [3].

**Conceptual.** BC-PRQ-05002 Sign analysis of a factored expression across a number line [2].

**Geometry and measurement.** BC-PRQ-05005 Area, perimeter, volume, and similar figure relations used to build an objective and a constraint [2].

**Earlier calculus.** BC-UNIT-01 supplies 4 upstream records across 5 edges: BC-SKL-01059, BC-SKL-01067, BC-TOP-0102, BC-TOP-0115. BC-UNIT-02 supplies 3 upstream records across 3 edges: BC-SKL-02019, BC-SKL-02027, BC-TOP-0205. BC-UNIT-03 supplies 2 upstream records across 3 edges: BC-SKL-03014, BC-TOP-0301. BC-UNIT-04 supplies 2 upstream records across 2 edges: BC-SKL-04030, BC-TOP-0402. BC-UNIT-06 supplies 4 upstream records across 4 edges: BC-SKL-06021, BC-SKL-06023, BC-SKL-06025, BC-SKL-06026.

## BC-UNIT-06 Integration and Accumulation of Change direct prerequisites [inferred]

74 skills, CED pages 112-131.

**Algebra.** BC-PRQ-06001 Rewriting expressions to expose an inner function and its derivative [4]; BC-PRQ-06003 Logarithm rules and properties of the natural logarithm [4]; BC-PRQ-06002 Exponent rules including negative and fractional exponents [3]; BC-PRQ-06009 Polynomial long division [2]; BC-PRQ-06010 Completing the square [2]; BC-PRQ-06011 Solving for undetermined coefficients in a rational identity [1].

**Trigonometry.** BC-PRQ-06004 Trigonometric identities used in antidifferentiation [2].

**Notation.** BC-PRQ-06005 Reading function notation, composition, and evaluation [10]; BC-PRQ-06006 Summation notation [5]; BC-PRQ-06013 Bound variables and the dummy variable convention [2].

**Conceptual.** BC-PRQ-06008 Inequality reasoning about approximations [2].

**Geometry and measurement.** BC-PRQ-06007 Area formulas for rectangles, triangles, trapezoids, circles, and semicircles [5].

**Arithmetic and numeracy.** BC-PRQ-06012 Arithmetic with nonuniform subinterval widths [4].

**Earlier calculus.** BC-UNIT-01 supplies 4 upstream records across 7 edges: BC-SKL-01006, BC-SKL-01054, BC-TOP-0102, BC-TOP-0115. BC-UNIT-02 supplies 3 upstream records across 3 edges: BC-SKL-02027, BC-SKL-02035, BC-TOP-0208. BC-UNIT-03 supplies 2 upstream records across 3 edges: BC-SKL-03002, BC-SKL-03021. BC-UNIT-05 supplies 3 upstream records across 3 edges: BC-SKL-05021, BC-SKL-05029, BC-TOP-0506.

## BC-UNIT-07 Differential Equations direct prerequisites [inferred]

43 skills, CED pages 132-145.

**Algebra.** BC-PRQ-06003 Logarithm rules and properties of the natural logarithm [2]; BC-PRQ-07001 Solving an equation that contains a logarithm or an exponential [2]; BC-PRQ-05001 Solving equations and inequalities to locate where an expression is zero or undefined [1]; BC-PRQ-07004 Absolute value equations and selecting the branch consistent with a given point [1].

**Function knowledge.** BC-PRQ-07006 Plotting and reading lattice points in the coordinate plane [3]; BC-PRQ-05003 Domain of a function, including piecewise, rational, and radical forms [1].

**Notation.** BC-PRQ-06005 Reading function notation, composition, and evaluation [4]; BC-PRQ-07002 Leibniz notation and the differentials of a derivative expression [3].

**Conceptual.** BC-PRQ-07003 Proportionality and joint proportionality statements [4].

**Arithmetic and numeracy.** BC-PRQ-07005 Repeated arithmetic with a fixed step size in a table computation [2].

**Earlier calculus.** BC-UNIT-02 supplies 2 upstream records across 2 edges: BC-SKL-02013, BC-TOP-0205. BC-UNIT-03 supplies 1 upstream record across 1 edge: BC-TOP-0301. BC-UNIT-04 supplies 1 upstream record across 2 edges: BC-SKL-04030. BC-UNIT-05 supplies 4 upstream records across 4 edges: BC-SKL-05014, BC-SKL-05030, BC-SKL-05046, BC-SKL-05052. BC-UNIT-06 supplies 4 upstream records across 6 edges: BC-SKL-06034, BC-SKL-06044, BC-SKL-06047, BC-SKL-06064.

## BC-UNIT-08 Applications of Integration direct prerequisites [inferred]

59 skills, CED pages 146-164.

**Algebra.** BC-PRQ-08002 Rewriting an equation to express one variable in terms of the other [8]; BC-PRQ-06002 Exponent rules including negative and fractional exponents [5]; BC-PRQ-08001 Solving an equation to locate where two graphs meet [4]; BC-PRQ-08003 Absolute value read as a piecewise definition [3].

**Notation.** BC-PRQ-06005 Reading function notation, composition, and evaluation [18]; BC-PRQ-08006 Decimal reporting and rounding conventions on calculator answers [4].

**Geometry and measurement.** BC-PRQ-08004 Distance between two values measured along a coordinate axis [13]; BC-PRQ-06007 Area formulas for rectangles, triangles, trapezoids, circles, and semicircles [2]; BC-PRQ-08005 Area formulas for equilateral and right isosceles triangles [2]; BC-PRQ-08007 Magnitude of a two component quantity by the Pythagorean relation [1].

**Earlier calculus.** BC-UNIT-02 supplies 1 upstream record across 1 edge: BC-SKL-02021. BC-UNIT-04 supplies 1 upstream record across 1 edge: BC-TOP-0402. BC-UNIT-05 supplies 2 upstream records across 2 edges: BC-SKL-05020, BC-SKL-05028. BC-UNIT-06 supplies 6 upstream records across 12 edges: BC-SKL-06028, BC-SKL-06034, BC-SKL-06036, BC-SKL-06037, BC-SKL-06038, BC-SKL-06047.

## BC-UNIT-09 Parametric Equations, Polar Coordinates, and Vector-Valued Functions direct prerequisites [inferred]

43 skills, CED pages 166-179.

**Algebra.** BC-PRQ-08001 Solving an equation to locate where two graphs meet [5].

**Trigonometry.** BC-PRQ-09002 Sine and cosine as coordinates and solving trigonometric equations on an interval [5].

**Notation.** BC-PRQ-06005 Reading function notation, composition, and evaluation [16]; BC-PRQ-09001 Reading vector and ordered pair notation for a position in the plane [6]; BC-PRQ-08006 Decimal reporting and rounding conventions on calculator answers [5]; BC-PRQ-09003 Radian measure as the calculator convention for trigonometric arguments [2].

**Conceptual.** BC-PRQ-09004 Deciding which parameter interval traces a curve exactly once [3].

**Geometry and measurement.** BC-PRQ-08007 Magnitude of a two component quantity by the Pythagorean relation [3].

**Earlier calculus.** BC-UNIT-02 supplies 1 upstream record across 1 edge: BC-SKL-02036. BC-UNIT-03 supplies 1 upstream record across 1 edge: BC-SKL-03006. BC-UNIT-05 supplies 1 upstream record across 1 edge: BC-SKL-05028. BC-UNIT-06 supplies 3 upstream records across 4 edges: BC-SKL-06028, BC-SKL-06034, BC-SKL-06037. BC-UNIT-07 supplies 1 upstream record across 1 edge: BC-SKL-07032. BC-UNIT-08 supplies 7 upstream records across 7 edges: BC-SKL-08006, BC-SKL-08007, BC-SKL-08009, BC-SKL-08019, BC-SKL-08051, BC-SKL-08056, BC-SKL-08059.

## BC-UNIT-10 Infinite Sequences and Series direct prerequisites [inferred]

73 skills, CED pages 180-200.

**Algebra.** BC-PRQ-06002 Exponent rules including negative and fractional exponents [12]; BC-PRQ-10001 Absolute value inequalities and their solution sets written as an interval [8]; BC-PRQ-10005 Recognising a geometric pattern and computing the common ratio [6]; BC-PRQ-10007 Simplification of ratios of powers with the same base [5]; BC-PRQ-06003 Logarithm rules and properties of the natural logarithm [1].

**Function knowledge.** BC-PRQ-10004 Limits of ratios of polynomial and exponential expressions in the index [12].

**Notation.** BC-PRQ-06005 Reading function notation, composition, and evaluation [22]; BC-PRQ-10008 Reading a general term out of sigma notation, including an alternating factor [19]; BC-PRQ-10002 Factorial notation and simplification of ratios of factorials [11]; BC-PRQ-10003 Index shifting and re-indexing of a sum [4]; BC-PRQ-10006 Interval notation with open and closed endpoints [4]; BC-PRQ-06013 Bound variables and the dummy variable convention [2]; BC-PRQ-06006 Summation notation [1].

**Earlier calculus.** BC-UNIT-01 supplies 1 upstream record across 1 edge: BC-SKL-01015. BC-UNIT-02 supplies 1 upstream record across 1 edge: BC-SKL-02008. BC-UNIT-06 supplies 2 upstream records across 2 edges: BC-SKL-06047, BC-SKL-06067. BC-UNIT-07 supplies 1 upstream record across 1 edge: BC-SKL-07018.

## Indirect chains for the ten most consequential skills [inferred]

A chain is a path of `hard_prerequisite` edges. Length 2 means two edges and three nodes. Only chains of length 2 to 4 are listed, and a skill is called consequential here when its transitive dependent set is among the largest in the graph. Each entry names the skill, the route in prose, and then the paths as ids.

### BC-SKL-03008 Apply the product rule to a term containing both x and y [inferred]

Route: implicit differentiation of a product term to related rates.

- BC-SKL-03008 -> BC-SKL-03009 -> BC-SKL-03010 (length 2). Ends at Solve the differentiated equation for dy/dx.
- BC-SKL-03008 -> BC-SKL-03009 -> BC-SKL-03023 (length 2). Ends at Derive an inverse trigonometric derivative by implicit differentiation.
- BC-SKL-03008 -> BC-SKL-03033 -> BC-SKL-03034 (length 2). Ends at Evaluate a second derivative at a point using dy/dx there.
- BC-SKL-03008 -> BC-SKL-03009 -> BC-SKL-03010 -> BC-SKL-03011 (length 3). Ends at Evaluate dy/dx at a stated point on the curve.
- BC-SKL-03008 -> BC-SKL-03009 -> BC-SKL-03010 -> BC-SKL-03012 (length 3). Ends at Locate a point where the tangent to an implicit curve is horizontal.
- BC-SKL-03008 -> BC-SKL-03009 -> BC-SKL-03010 -> BC-SKL-03013 (length 3). Ends at Locate a point where the tangent to an implicit curve is vertical.
- BC-SKL-03008 -> BC-SKL-03009 -> BC-SKL-03010 -> BC-SKL-03014 (length 3). Ends at Verify a supplied expression for dy/dx by implicit differentiation.

### BC-SKL-06034 Evaluate a definite integral by antidifferentiation and endpoint substitution [inferred]

Route: evaluating a definite integral with the Fundamental Theorem of Calculus to every accumulation application.

- BC-SKL-06034 -> BC-SKL-06036 -> BC-SKL-06037 (length 2). Ends at Compute a final value from an initial condition and an accumulated change.
- BC-SKL-06034 -> BC-SKL-06036 -> BC-SKL-06039 (length 2). Ends at Set up a single definite integral for a rate in minus rate out situation.
- BC-SKL-06034 -> BC-SKL-06036 -> BC-SKL-08004 (length 2). Ends at Distinguish average value from average rate of change.
- BC-SKL-06034 -> BC-SKL-06036 -> BC-SKL-08006 (length 2). Ends at Compute displacement as the definite integral of velocity.
- BC-SKL-06034 -> BC-SKL-06038 -> BC-SKL-08001 (length 2). Ends at Apply the average value formula to a function given by a formula.
- BC-SKL-06034 -> BC-SKL-07025 -> BC-SKL-07026 (length 2). Ends at Include a single constant of integration.
- BC-SKL-06034 -> BC-SKL-06036 -> BC-SKL-06037 -> BC-SKL-08009 (length 3). Ends at Determine a position value from an initial position and velocity.
- BC-SKL-06034 -> BC-SKL-06036 -> BC-SKL-06037 -> BC-SKL-08012 (length 3). Ends at Express the amount at a time as an initial amount plus an integral.
- BC-SKL-06034 -> BC-SKL-06036 -> BC-SKL-06037 -> BC-SKL-09021 (length 3). Ends at Determine a coordinate of position from an initial position and a velocity component.
- BC-SKL-06034 -> BC-SKL-06036 -> BC-SKL-08006 -> BC-SKL-09020 (length 3). Ends at Write the displacement as a definite integral of the velocity vector.
- BC-SKL-06034 -> BC-SKL-07025 -> BC-SKL-07026 -> BC-SKL-07027 (length 3). Ends at Solve the resulting equation for the dependent variable.
- BC-SKL-06034 -> BC-SKL-07025 -> BC-SKL-07026 -> BC-SKL-07029 (length 3). Ends at Substitute the initial condition to evaluate the constant of integration.

### BC-SKL-01028 Recognise an indeterminate form as a signal that rewriting is needed [inferred]

Route: recognising an indeterminate form to the algebraic resolution it triggers, and on into Unit 2; the onward links to L'Hospital's rule at BC-TOP-0407 and to improper integrals at BC-TOP-0613 are still topic-level edges whose notes end in unmapped.

- BC-SKL-01028 -> BC-SKL-01024 -> BC-TOP-0202 (length 2). Ends at BC-TOP-0202.
- BC-SKL-01028 -> BC-SKL-01024 -> BC-TOP-0202 -> BC-SKL-03030 (length 3). Ends at Differentiate a first derivative to obtain the second derivative.
- BC-SKL-01028 -> BC-SKL-01024 -> BC-TOP-0202 -> BC-SKL-04006 (length 3). Ends at Differentiate a position function to obtain velocity.

### BC-SKL-03002 Differentiate a two layer composite function with the chain rule [inferred]

Route: the chain rule to substitution and to the Fundamental Theorem with a composite upper limit.

- BC-SKL-03002 -> BC-SKL-03006 -> BC-SKL-09032 (length 2). Ends at Relate the rate of the distance from the origin in time to dr/dtheta.
- BC-SKL-03002 -> BC-SKL-03007 -> BC-SKL-03008 (length 2). Ends at Apply the product rule to a term containing both x and y.
- BC-SKL-03002 -> BC-SKL-03007 -> BC-SKL-03009 (length 2). Ends at Differentiate both sides of an implicit equation term by term.
- BC-SKL-03002 -> BC-SKL-03022 -> BC-SKL-03025 (length 2). Ends at Combine an inverse trigonometric derivative with the product or quotient rule.
- BC-SKL-03002 -> BC-SKL-06047 -> BC-SKL-06048 (length 2). Ends at Convert the differential and adjust the constant when substituting.
- BC-SKL-03002 -> BC-SKL-06047 -> BC-SKL-06052 (length 2). Ends at Apply substitution to an integrand that antidifferentiates to a logarithm.
- BC-SKL-03002 -> BC-SKL-06047 -> BC-SKL-06054 (length 2). Ends at Complete the square in a quadratic denominator to reach a standard form.
- BC-SKL-03002 -> BC-SKL-06047 -> BC-SKL-06056 (length 2). Ends at Decide between rearrangement and substitution for a rational integrand.
- BC-SKL-03002 -> BC-SKL-06047 -> BC-SKL-06071 (length 2). Ends at Classify an integrand to select an antidifferentiation technique.
- BC-SKL-03002 -> BC-SKL-06047 -> BC-SKL-07024 (length 2). Ends at Separate the variables onto opposite sides of the equation.
- BC-SKL-03002 -> BC-SKL-06047 -> BC-SKL-10069 (length 2). Ends at Integrate a power series term by term and determine the constant.
- BC-SKL-03002 -> BC-SKL-03007 -> BC-SKL-03008 -> BC-SKL-03009 (length 3). Ends at Differentiate both sides of an implicit equation term by term.
- BC-SKL-03002 -> BC-SKL-03007 -> BC-SKL-03008 -> BC-SKL-03033 (length 3). Ends at Differentiate a derivative expression that still contains y.
- BC-SKL-03002 -> BC-SKL-03007 -> BC-SKL-03009 -> BC-SKL-03010 (length 3). Ends at Solve the differentiated equation for dy/dx.
- 11 further chains of the same shape are in ../../data/prereq_edges.csv.

### BC-SKL-02036 Apply the product rule to a product of two differentiable functions [inferred]

Route: the product rule to integration by parts and to implicit differentiation.

- BC-SKL-02036 -> BC-SKL-02039 -> BC-SKL-02040 (length 2). Ends at Keep the order of the terms in the quotient rule numerator.
- BC-SKL-02036 -> BC-SKL-02039 -> BC-SKL-02041 (length 2). Ends at Apply the quotient rule with values supplied by a table or a graph.
- BC-SKL-02036 -> BC-SKL-02039 -> BC-SKL-02044 (length 2). Ends at Differentiate tangent and cotangent.
- BC-SKL-02036 -> BC-SKL-02039 -> BC-SKL-02045 (length 2). Ends at Differentiate secant and cosecant.
- BC-SKL-02036 -> BC-SKL-02039 -> BC-SKL-03020 (length 2). Ends at Derive the inverse derivative rule from the chain rule.
- BC-SKL-02036 -> BC-SKL-03006 -> BC-SKL-09032 (length 2). Ends at Relate the rate of the distance from the origin in time to dr/dtheta.
- BC-SKL-02036 -> BC-TOP-0302 -> BC-SKL-04022 (length 2). Ends at Differentiate an implicitly defined curve with respect to time.

### BC-SKL-06047 Select a substitution by identifying an inner function whose derivative appears [inferred]

Route: substitution to separation of variables and to term by term integration of a power series.

- BC-SKL-06047 -> BC-SKL-06048 -> BC-SKL-06049 (length 2). Ends at Back-substitute to express an indefinite integral in the original variable.
- BC-SKL-06047 -> BC-SKL-06048 -> BC-SKL-06050 (length 2). Ends at Change the limits of integration when substituting in a definite integral.
- BC-SKL-06047 -> BC-SKL-06048 -> BC-SKL-06052 (length 2). Ends at Apply substitution to an integrand that antidifferentiates to a logarithm.
- BC-SKL-06047 -> BC-SKL-06052 -> BC-SKL-06064 (length 2). Ends at Antidifferentiate a linear partial fraction decomposition.
- BC-SKL-06047 -> BC-SKL-06054 -> BC-SKL-06056 (length 2). Ends at Decide between rearrangement and substitution for a rational integrand.
- BC-SKL-06047 -> BC-SKL-06071 -> BC-SKL-06072 (length 2). Ends at Rule out a technique whose structural precondition is absent.
- BC-SKL-06047 -> BC-SKL-06071 -> BC-SKL-06073 (length 2). Ends at Chain two antidifferentiation techniques in one problem.
- BC-SKL-06047 -> BC-SKL-06071 -> BC-SKL-06074 (length 2). Ends at Recognise when no elementary technique applies and use an integral or numerical representation.
- BC-SKL-06047 -> BC-SKL-07024 -> BC-SKL-07025 (length 2). Ends at Antidifferentiate both sides of the separated equation.
- BC-SKL-06047 -> BC-SKL-07024 -> BC-SKL-07028 (length 2). Ends at Recognise when a differential equation is not separable.
- BC-SKL-06047 -> BC-SKL-06048 -> BC-SKL-06049 -> BC-SKL-06051 (length 3). Ends at Evaluate a definite integral by substitution with back-substitution before the limits are used.
- BC-SKL-06047 -> BC-SKL-06048 -> BC-SKL-06050 -> BC-SKL-06051 (length 3). Ends at Evaluate a definite integral by substitution with back-substitution before the limits are used.
- BC-SKL-06047 -> BC-SKL-06048 -> BC-SKL-06052 -> BC-SKL-06064 (length 3). Ends at Antidifferentiate a linear partial fraction decomposition.
- BC-SKL-06047 -> BC-SKL-06052 -> BC-SKL-06064 -> BC-SKL-06065 (length 3). Ends at Evaluate a definite integral of a rational function by partial fractions.
- 3 further chains of the same shape are in ../../data/prereq_edges.csv.

### BC-SKL-05020 Classify a critical point from the sign change of the first derivative [inferred]

Route: the first derivative test to accumulation function analysis and to differential equation solutions.

- BC-SKL-05020 -> BC-SKL-05038 -> BC-SKL-05053 (length 2). Ends at Verify that the critical point gives the required extremum on the domain.
- BC-SKL-05020 -> BC-SKL-05038 -> BC-SKL-05053 -> BC-SKL-05054 (length 3). Ends at Report the optimal value with its units and the input where it occurs.

### BC-SKL-07010 Compute the slope the equation assigns to a given point [inferred]

Route: the slope a differential equation assigns to a point, feeding slope field reading and Euler's method.

- BC-SKL-07010 -> BC-SKL-07012 -> BC-SKL-07015 (length 2). Ends at Keep a sketched curve on the correct side of an equilibrium level.
- BC-SKL-07010 -> BC-SKL-07012 -> BC-SKL-07017 (length 2). Ends at Describe the long-run behaviour of a solution from the field.
- BC-SKL-07010 -> BC-SKL-07013 -> BC-SKL-07016 (length 2). Ends at Match a slope field to a differential equation.
- BC-SKL-07010 -> BC-SKL-07018 -> BC-SKL-07023 (length 2). Ends at Decide the direction of the Euler error from concavity.
- BC-SKL-07010 -> BC-SKL-07020 -> BC-SKL-07021 (length 2). Ends at Use the previous approximation as the input for the next step.
- BC-SKL-07010 -> BC-SKL-07020 -> BC-SKL-07023 (length 2). Ends at Decide the direction of the Euler error from concavity.
- BC-SKL-07010 -> BC-SKL-07012 -> BC-SKL-07017 -> BC-SKL-07041 (length 3). Ends at Determine the limiting value without solving the equation.
- BC-SKL-07010 -> BC-SKL-07020 -> BC-SKL-07021 -> BC-SKL-07022 (length 3). Ends at Lay out the computation as a labelled step table.

### BC-SKL-06018 Differentiate an accumulation function with a variable upper limit [inferred]

Route: the derivative of an accumulation function feeding the analysis of that function.

- BC-SKL-06018 -> BC-SKL-06022 -> BC-SKL-06023 (length 2). Ends at Locate relative extrema of an accumulation function from sign changes of the integrand.
- BC-SKL-06018 -> BC-SKL-06022 -> BC-SKL-06027 (length 2). Ends at Describe the graph of an accumulation function from the graph of the integrand.
- BC-SKL-06018 -> BC-SKL-06023 -> BC-SKL-06026 (length 2). Ends at Determine an absolute extreme value of an accumulation function with a global argument.
- BC-SKL-06018 -> BC-SKL-06024 -> BC-SKL-06027 (length 2). Ends at Describe the graph of an accumulation function from the graph of the integrand.
- BC-SKL-06018 -> BC-SKL-06025 -> BC-SKL-06027 (length 2). Ends at Describe the graph of an accumulation function from the graph of the integrand.
- BC-SKL-06018 -> BC-SKL-06022 -> BC-SKL-06023 -> BC-SKL-06026 (length 3). Ends at Determine an absolute extreme value of an accumulation function with a global argument.

### BC-SKL-05016 Build a sign chart on critical points and domain boundaries [inferred]

Route: the sign chart feeding the derivative tests and the global justifications of the applications units.

- BC-SKL-05016 -> BC-SKL-05020 -> BC-SKL-05021 (length 2). Ends at Conclude neither extremum when the derivative keeps its sign.
- BC-SKL-05016 -> BC-SKL-05020 -> BC-SKL-05022 (length 2). Ends at Write a first derivative test justification with an explicit referent.
- BC-SKL-05016 -> BC-SKL-05020 -> BC-SKL-05023 (length 2). Ends at Separate the location of a relative extremum from its value.
- BC-SKL-05016 -> BC-SKL-05020 -> BC-SKL-05038 (length 2). Ends at Extend a sole relative extremum to an absolute extremum on the interval.
- BC-SKL-05016 -> BC-SKL-05020 -> BC-SKL-05039 (length 2). Ends at Choose between the first and second derivative tests for a given presentation.
- BC-SKL-05016 -> BC-SKL-05020 -> BC-SKL-08014 (length 2). Ends at Determine when an accumulated amount is maximal and justify globally.
- BC-SKL-05016 -> BC-SKL-05047 -> BC-SKL-05048 (length 2). Ends at Answer a question about a function from tabulated derivative values.
- BC-SKL-05016 -> BC-SKL-05020 -> BC-SKL-05038 -> BC-SKL-05053 (length 3). Ends at Verify that the critical point gives the required extremum on the domain.

## Hidden prerequisites and the errors they produce [inferred]

Every BC-PRQ record carries `hidden: true`, meaning the CED does not list the ability as content but the skills that depend on it cannot be completed without it. The failure signature on each record states what a response looks like when the ability is absent. The errors column lists BC-ERR ids recorded against the skills that depend on the prerequisite, which is the observable evidence that the hidden prerequisite is the failing layer rather than the calculus step.

| BC-PRQ | Name | Category | Dependent skills | Errors observed on those skills |
|---|---|---|---|---|
| BC-PRQ-01001 | Factoring polynomials and dividing out a common factor | algebra | 8 | BC-ERR-01003, BC-ERR-01006, BC-ERR-01008, BC-ERR-01009, BC-ERR-01010, BC-ERR-01011, BC-ERR-01018 |
| BC-PRQ-01002 | Rationalising a numerator or denominator with a conjugate | algebra | 1 | none recorded |
| BC-PRQ-01003 | Reading a piecewise defined function rule | function | 10 | BC-ERR-01001, BC-ERR-01002, BC-ERR-01003, BC-ERR-01014, BC-ERR-01015, BC-ERR-01017, BC-ERR-01031 |
| BC-PRQ-01004 | End behaviour of a rational function from degree comparison | function | 5 | BC-ERR-01021, BC-ERR-01023, BC-ERR-01024, BC-ERR-01033 |
| BC-PRQ-01005 | Exact trigonometric values and the bounds on sine and cosine | trigonometry | 5 | BC-ERR-01004, BC-ERR-01012, BC-ERR-02018 |
| BC-PRQ-01006 | Absolute value rewritten as a piecewise expression | algebra | 2 | BC-ERR-01002 |
| BC-PRQ-01007 | Simplifying a complex fraction | algebra | 1 | BC-ERR-01010 |
| BC-PRQ-01008 | Domain of rational, radical, logarithmic, and trigonometric expressions | function | 6 | BC-ERR-01016, BC-ERR-01017, BC-ERR-01025, BC-ERR-01031, BC-ERR-01032 |
| BC-PRQ-01009 | Sign analysis of a quotient near a zero of the denominator | arithmetic | 4 | BC-ERR-01018, BC-ERR-01019, BC-ERR-01020 |
| BC-PRQ-01010 | Interval and inequality notation for open and closed intervals | notation | 7 | BC-ERR-01013, BC-ERR-01025, BC-ERR-01026, BC-ERR-01027, BC-ERR-01028, BC-ERR-01031, BC-ERR-01032 |
| BC-PRQ-02001 | Expanding and simplifying a difference quotient | algebra | 3 | BC-ERR-02001, BC-ERR-02005, BC-ERR-02006, BC-ERR-02007, BC-ERR-02013 |
| BC-PRQ-02002 | Reciprocal and quotient trigonometric identities | trigonometry | 2 | BC-ERR-02026 |
| BC-PRQ-02003 | Slope of a line through two points and the point slope form | function | 2 | BC-ERR-02027, BC-ERR-02028 |
| BC-PRQ-02004 | Prime notation and Leibniz notation conventions | notation | 4 | BC-ERR-02016, BC-ERR-02029, BC-ERR-02030, BC-ERR-02031, BC-ERR-02032 |
| BC-PRQ-02005 | Recognising a function value at a shifted input | function | 5 | BC-ERR-02001, BC-ERR-02006, BC-ERR-02008, BC-ERR-02009, BC-ERR-02010, BC-ERR-02030 |
| BC-PRQ-03001 | Decomposing a formula into an outer and an inner function | function | 9 | BC-ERR-03001, BC-ERR-03002, BC-ERR-03003, BC-ERR-03004, BC-ERR-03005, BC-ERR-03006, BC-ERR-03019 |
| BC-PRQ-03002 | Solving a linear equation for an embedded factor | algebra | 3 | BC-ERR-03008, BC-ERR-03010, BC-ERR-03023 |
| BC-PRQ-03003 | Definition of an inverse function and reading matched pairs | function | 6 | BC-ERR-03014, BC-ERR-03015, BC-ERR-03016 |
| BC-PRQ-03004 | Unit circle values, Pythagorean identities, and right triangle ratios | trigonometry | 5 | BC-ERR-03006, BC-ERR-03017, BC-ERR-03018 |
| BC-PRQ-03005 | Reading and writing prime and Leibniz derivative notation | notation | 9 | BC-ERR-03003, BC-ERR-03004, BC-ERR-03005, BC-ERR-03007, BC-ERR-03008, BC-ERR-03009, BC-ERR-03021, BC-ERR-03022, and 1 more |
| BC-PRQ-03006 | Simplifying rational and radical expressions | algebra | 8 | BC-ERR-03002, BC-ERR-03006, BC-ERR-03010, BC-ERR-03011, BC-ERR-03015, BC-ERR-03016, BC-ERR-03018, BC-ERR-03020, and 1 more |
| BC-PRQ-03007 | Deciding when an expression is zero or undefined | algebra | 2 | BC-ERR-03012, BC-ERR-03013 |
| BC-PRQ-04001 | Volume and area formulas for standard solids | geometry | 1 | BC-ERR-04016 |
| BC-PRQ-04002 | The Pythagorean theorem and right triangle relations | geometry | 1 | BC-ERR-04016 |
| BC-PRQ-04003 | Similar triangles and proportional reasoning | geometry | 1 | BC-ERR-04019 |
| BC-PRQ-04004 | Unit analysis with compound units | arithmetic | 5 | BC-ERR-04001, BC-ERR-04002, BC-ERR-04004, BC-ERR-04005 |
| BC-PRQ-04005 | Absolute value as size without sign | algebra | 2 | BC-ERR-04007, BC-ERR-04009 |
| BC-PRQ-04006 | Point-slope form of a line | algebra | 3 | BC-ERR-04023, BC-ERR-04024, BC-ERR-04027 |
| BC-PRQ-04007 | Solving a linear equation for one unknown quantity | algebra | 2 | BC-ERR-04021, BC-ERR-04022 |
| BC-PRQ-04008 | Translating a verbal scenario into named variables | conceptual | 22 | BC-ERR-04001, BC-ERR-04002, BC-ERR-04003, BC-ERR-04005, BC-ERR-04006, BC-ERR-04012, BC-ERR-04013, BC-ERR-04014, and 10 more |
| BC-PRQ-04009 | Sign analysis of an expression over an interval | algebra | 3 | BC-ERR-04008, BC-ERR-04010, BC-ERR-04011 |
| BC-PRQ-05001 | Solving equations and inequalities to locate where an expression is zero or undefined | algebra | 9 | BC-ERR-05005, BC-ERR-05009, BC-ERR-05010, BC-ERR-05011, BC-ERR-05014, BC-ERR-05030, BC-ERR-05032, BC-ERR-05057, and 2 more |
| BC-PRQ-05002 | Sign analysis of a factored expression across a number line | conceptual | 2 | BC-ERR-05014, BC-ERR-05030 |
| BC-PRQ-05003 | Domain of a function, including piecewise, rational, and radical forms | function | 7 | BC-ERR-05009, BC-ERR-05010, BC-ERR-05011, BC-ERR-05017, BC-ERR-05019, BC-ERR-05032, BC-ERR-05052, BC-ERR-07031 |
| BC-PRQ-05004 | Interval notation and the open versus closed distinction | notation | 3 | BC-ERR-05001, BC-ERR-05007, BC-ERR-05025, BC-ERR-05026, BC-ERR-99008 |
| BC-PRQ-05005 | Area, perimeter, volume, and similar figure relations used to build an objective and a constraint | geometry | 2 | BC-ERR-05050, BC-ERR-05051, BC-ERR-99033 |
| BC-PRQ-05006 | Reading features of a graph, including where a graph rises, falls, and changes bending | function | 4 | BC-ERR-05012, BC-ERR-05015, BC-ERR-05016, BC-ERR-05031, BC-ERR-05041, BC-ERR-99004 |
| BC-PRQ-05007 | Solving a system made of a defining relation and a derived equation | algebra | 4 | BC-ERR-05057, BC-ERR-05058, BC-ERR-05059, BC-ERR-05060 |
| BC-PRQ-05008 | Average rate of change over an interval as a difference quotient | precalculus | 1 | BC-ERR-05003 |
| BC-PRQ-06001 | Rewriting expressions to expose an inner function and its derivative | algebra | 4 | BC-ERR-06019, BC-ERR-06020, BC-ERR-06022 |
| BC-PRQ-06002 | Exponent rules including negative and fractional exponents | algebra | 23 | BC-ERR-02015, BC-ERR-02017, BC-ERR-02019, BC-ERR-06032, BC-ERR-08005, BC-ERR-08021, BC-ERR-08022, BC-ERR-08030, and 12 more |
| BC-PRQ-06003 | Logarithm rules and properties of the natural logarithm | algebra | 8 | BC-ERR-07025, BC-ERR-07036, BC-ERR-10011, BC-ERR-99014 |
| BC-PRQ-06004 | Trigonometric identities used in antidifferentiation | trigonometry | 2 | none recorded |
| BC-PRQ-06005 | Reading function notation, composition, and evaluation | notation | 96 | BC-ERR-01001, BC-ERR-01002, BC-ERR-01003, BC-ERR-01004, BC-ERR-01005, BC-ERR-01006, BC-ERR-01007, BC-ERR-01014, and 80 more |
| BC-PRQ-06006 | Summation notation | notation | 6 | BC-ERR-06003, BC-ERR-10002 |
| BC-PRQ-06007 | Area formulas for rectangles, triangles, trapezoids, circles, and semicircles | geometry | 7 | BC-ERR-06001, BC-ERR-06004, BC-ERR-06011, BC-ERR-06012, BC-ERR-06013, BC-ERR-06014, BC-ERR-08001, BC-ERR-08003, and 2 more |
| BC-PRQ-06008 | Inequality reasoning about approximations | conceptual | 2 | BC-ERR-06005, BC-ERR-06006, BC-ERR-06007 |
| BC-PRQ-06009 | Polynomial long division | algebra | 2 | BC-ERR-06026 |
| BC-PRQ-06010 | Completing the square | algebra | 2 | BC-ERR-06026 |
| BC-PRQ-06011 | Solving for undetermined coefficients in a rational identity | algebra | 1 | none recorded |
| BC-PRQ-06012 | Arithmetic with nonuniform subinterval widths | arithmetic | 4 | BC-ERR-06001, BC-ERR-06002, BC-ERR-06003, BC-ERR-06004 |
| BC-PRQ-06013 | Bound variables and the dummy variable convention | notation | 4 | BC-ERR-06027, BC-ERR-06028, BC-ERR-10011, BC-ERR-10012, BC-ERR-10039 |
| BC-PRQ-07001 | Solving an equation that contains a logarithm or an exponential | algebra | 2 | BC-ERR-07027, BC-ERR-07036 |
| BC-PRQ-07002 | Leibniz notation and the differentials of a derivative expression | notation | 3 | BC-ERR-07005, BC-ERR-07006, BC-ERR-07024, BC-ERR-99006, BC-ERR-99014 |
| BC-PRQ-07003 | Proportionality and joint proportionality statements | conceptual | 4 | BC-ERR-07001, BC-ERR-07002, BC-ERR-07034, BC-ERR-07039 |
| BC-PRQ-07004 | Absolute value equations and selecting the branch consistent with a given point | algebra | 1 | BC-ERR-07030, BC-ERR-99037 |
| BC-PRQ-07005 | Repeated arithmetic with a fixed step size in a table computation | arithmetic | 2 | BC-ERR-07019, BC-ERR-07021, BC-ERR-99026 |
| BC-PRQ-07006 | Plotting and reading lattice points in the coordinate plane | function | 3 | BC-ERR-07010, BC-ERR-07011, BC-ERR-07014, BC-ERR-99024 |
| BC-PRQ-08001 | Solving an equation to locate where two graphs meet | algebra | 9 | BC-ERR-08010, BC-ERR-08015, BC-ERR-08016, BC-ERR-08019, BC-ERR-08025, BC-ERR-09008, BC-ERR-09022, BC-ERR-09023, and 6 more |
| BC-PRQ-08002 | Rewriting an equation to express one variable in terms of the other | algebra | 8 | BC-ERR-08018, BC-ERR-08023, BC-ERR-08024, BC-ERR-08038 |
| BC-PRQ-08003 | Absolute value read as a piecewise definition | algebra | 3 | BC-ERR-08008, BC-ERR-08009, BC-ERR-08010, BC-ERR-08027 |
| BC-PRQ-08004 | Distance between two values measured along a coordinate axis | geometry | 13 | BC-ERR-08028, BC-ERR-08029, BC-ERR-08030, BC-ERR-08031, BC-ERR-08036, BC-ERR-08037, BC-ERR-08038, BC-ERR-08039, and 1 more |
| BC-PRQ-08005 | Area formulas for equilateral and right isosceles triangles | geometry | 2 | BC-ERR-08032, BC-ERR-08033 |
| BC-PRQ-08006 | Decimal reporting and rounding conventions on calculator answers | notation | 9 | BC-ERR-08004, BC-ERR-08005, BC-ERR-08007, BC-ERR-08019, BC-ERR-08045, BC-ERR-09004, BC-ERR-09006, BC-ERR-09011, and 1 more |
| BC-PRQ-08007 | Magnitude of a two component quantity by the Pythagorean relation | geometry | 4 | BC-ERR-08041, BC-ERR-09013, BC-ERR-09014, BC-ERR-09015, BC-ERR-09024 |
| BC-PRQ-09001 | Reading vector and ordered pair notation for a position in the plane | notation | 6 | BC-ERR-09006, BC-ERR-09011, BC-ERR-09017, BC-ERR-09018, BC-ERR-09019 |
| BC-PRQ-09002 | Sine and cosine as coordinates and solving trigonometric equations on an interval | trigonometry | 5 | BC-ERR-09016, BC-ERR-09027, BC-ERR-09031, BC-ERR-09032, BC-ERR-09037, BC-ERR-09038, BC-ERR-09039 |
| BC-PRQ-09003 | Radian measure as the calculator convention for trigonometric arguments | notation | 2 | BC-ERR-09006, BC-ERR-09022, BC-ERR-09023, BC-ERR-09028 |
| BC-PRQ-09004 | Deciding which parameter interval traces a curve exactly once | conceptual | 3 | BC-ERR-09016, BC-ERR-09037, BC-ERR-09041 |
| BC-PRQ-10001 | Absolute value inequalities and their solution sets written as an interval | algebra | 8 | BC-ERR-10005, BC-ERR-10006, BC-ERR-10009, BC-ERR-10026, BC-ERR-10027, BC-ERR-10035, BC-ERR-10036 |
| BC-PRQ-10002 | Factorial notation and simplification of ratios of factorials | notation | 11 | BC-ERR-10017, BC-ERR-10021, BC-ERR-10022, BC-ERR-10026, BC-ERR-10027, BC-ERR-10028, BC-ERR-10029, BC-ERR-10030, and 3 more |
| BC-PRQ-10003 | Index shifting and re-indexing of a sum | notation | 4 | BC-ERR-10002, BC-ERR-10006, BC-ERR-10024, BC-ERR-10039 |
| BC-PRQ-10004 | Limits of ratios of polynomial and exponential expressions in the index | function | 12 | BC-ERR-10001, BC-ERR-10003, BC-ERR-10007, BC-ERR-10008, BC-ERR-10009, BC-ERR-10015, BC-ERR-10016, BC-ERR-10017, and 4 more |
| BC-PRQ-10005 | Recognising a geometric pattern and computing the common ratio | algebra | 6 | BC-ERR-10002, BC-ERR-10004, BC-ERR-10005, BC-ERR-10006, BC-ERR-10009, BC-ERR-10015, BC-ERR-10040 |
| BC-PRQ-10006 | Interval notation with open and closed endpoints | notation | 4 | BC-ERR-10015, BC-ERR-10035, BC-ERR-10037, BC-ERR-10038, BC-ERR-10043 |
| BC-PRQ-10007 | Simplification of ratios of powers with the same base | algebra | 5 | BC-ERR-10017, BC-ERR-10018, BC-ERR-10021, BC-ERR-10022, BC-ERR-10041 |
| BC-PRQ-10008 | Reading a general term out of sigma notation, including an alternating factor | notation | 19 | BC-ERR-10002, BC-ERR-10004, BC-ERR-10006, BC-ERR-10007, BC-ERR-10009, BC-ERR-10014, BC-ERR-10015, BC-ERR-10018, and 8 more |

Failure signatures for the prerequisites with the widest reach:

- BC-PRQ-06005 Reading function notation, composition, and evaluation (notation, 96 dependent skills). Values are pulled from a table or a graph for the wrong input, or f' and f are interchanged.

- BC-PRQ-06002 Exponent rules including negative and fractional exponents (algebra, 23 dependent skills). Radical or reciprocal integrands are left unrewritten, or the power rule is applied to an exponent of negative one.

- BC-PRQ-04008 Translating a verbal scenario into named variables (conceptual, 22 dependent skills). The response cannot begin because the quantities in the scenario were never named; the CED unit overview records this translation as a recurring difficulty (ced:84).

- BC-PRQ-10008 Reading a general term out of sigma notation, including an alternating factor (notation, 19 dependent skills). Student substitutes a value of the variable into the index, or loses the alternating factor.

- BC-PRQ-08004 Distance between two values measured along a coordinate axis (geometry, 13 dependent skills). Student writes a radius as a bare function value when the axis of revolution is not a coordinate axis.

- BC-PRQ-10004 Limits of ratios of polynomial and exponential expressions in the index (function, 12 dependent skills). Student reports the limit of a quotient of like degree polynomials as zero or as infinity.

- BC-PRQ-10002 Factorial notation and simplification of ratios of factorials (notation, 11 dependent skills). Student cancels factorials termwise or treats (n+1)! as n! plus one.

- BC-PRQ-01003 Reading a piecewise defined function rule (function, 10 dependent skills). The student evaluates the wrong branch at a boundary input or ignores the branch condition.

- BC-PRQ-03001 Decomposing a formula into an outer and an inner function (function, 9 dependent skills). The student differentiates the outer shell and stops, or differentiates the inner expression and reports that as the whole derivative.

- BC-PRQ-03005 Reading and writing prime and Leibniz derivative notation (notation, 9 dependent skills). The response writes dy in place of dy/dx, or dy/dx in place of the operator d/dx, and the differentiated equation loses its meaning.

- BC-PRQ-08001 Solving an equation to locate where two graphs meet (algebra, 9 dependent skills). Student writes the correct area or volume integrand but cannot produce the limits of integration.

- BC-PRQ-08006 Decimal reporting and rounding conventions on calculator answers (notation, 9 dependent skills). Student presents a correct setup and loses the answer point to a rounded intermediate value.
