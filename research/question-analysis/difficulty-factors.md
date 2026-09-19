---
title: AP Calculus BC Difficulty Factors
research_date: 2026-09-19
status: draft
purpose: The BC-DF taxonomy of what makes a question hard, the evidence behind each factor, the archetypes each factor is mapped to, and how the factors combine.
---

# AP Calculus BC Difficulty Factors

17 difficulty factors are recorded in `../../data/taxonomies.json`. Each archetype in [question-archetypes.md](question-archetypes.md) carries a `difficulty_factors` list mapped from the difficulty variables its unit agent recorded, so a factor is a property of a question rather than of a student. Official free response parts are linked to factors through the archetypes, and the `official_examples` field on each factor is empty until the FRQ records are built.

## BC-DF-01 Number of concepts combined [inferred]

How many separately taught ideas a single part requires before any answer can be written; a part that joins two chapters of the course costs more than a part that exercises one rule.

**Evidence.** BC-QA-05011 joins modelling, domain restriction, and a global justification in one part; BC-QA-06005 joins antidifferentiation with an initial condition; BC-QA-09007 joins the speed expression with a total distance integral. [inferred] from the expected_solution_path lengths of those records. Sources: ced:87, sg-24:4.

**Mapped to 27 archetypes.** BC-QA-01014, BC-QA-02003, BC-QA-03003, BC-QA-04001, BC-QA-04007, BC-QA-05006, BC-QA-05010, BC-QA-05013, BC-QA-06001, BC-QA-06004, BC-QA-06006, BC-QA-06009, BC-QA-06010, BC-QA-07001, BC-QA-07002, BC-QA-07004, BC-QA-08013, BC-QA-09001, BC-QA-09003, BC-QA-09006, BC-QA-09007, BC-QA-09010, BC-QA-10006, BC-QA-10010, BC-QA-10011, BC-QA-10012, BC-QA-10020

## BC-DF-02 Prerequisite depth [inferred]

How far below the calculus step the response must reach into algebra, trigonometry, function behaviour, or geometry before the calculus can start.

**Evidence.** BC-QA-01004 rests on algebraic rewriting recorded as BC-PRQ prerequisites; BC-QA-04006 needs a geometric relation before differentiation; BC-QA-01008 needs a linear solve. [inferred] from the prerequisites arrays of those records. Sources: ced:87.

**Mapped to 30 archetypes.** BC-QA-01004, BC-QA-01007, BC-QA-01009, BC-QA-01015, BC-QA-02002, BC-QA-02007, BC-QA-02008, BC-QA-02013, BC-QA-03001, BC-QA-03007, BC-QA-03009, BC-QA-04006, BC-QA-05007, BC-QA-05011, BC-QA-06004, BC-QA-06008, BC-QA-06009, BC-QA-06010, BC-QA-06013, BC-QA-06015, BC-QA-07003, BC-QA-07009, BC-QA-07010, BC-QA-10001, BC-QA-10002, BC-QA-10013, BC-QA-10014, BC-QA-10016, BC-QA-10018, BC-QA-10020

## BC-DF-03 Unusual representation [verified]

The information arrives in a form the skill is less often practised in, so the reading step is itself work: a graph of a derivative rather than of a function, a table rather than a formula, a slope field, or a vector of components.

**Evidence.** BC-QA-03003 supplies graphs of the component functions for a chain rule; BC-QA-05009 relates the graphs of a function and its first two derivatives; BC-QA-10011 supplies derivative values in a table for a Taylor polynomial (sg-25:11). Sources: ced:12, sg-25:11.

**Mapped to 30 archetypes.** BC-QA-01001, BC-QA-01002, BC-QA-01006, BC-QA-01007, BC-QA-01011, BC-QA-01012, BC-QA-01013, BC-QA-02004, BC-QA-02005, BC-QA-02009, BC-QA-03002, BC-QA-03006, BC-QA-04002, BC-QA-04009, BC-QA-05001, BC-QA-05003, BC-QA-05004, BC-QA-05009, BC-QA-06001, BC-QA-06004, BC-QA-06005, BC-QA-06006, BC-QA-06012, BC-QA-07008, BC-QA-07011, BC-QA-08001, BC-QA-08002, BC-QA-08003, BC-QA-09004, BC-QA-09011

## BC-DF-04 Notation complexity [verified]

The density and unfamiliarity of the symbols that must be read or produced, including Leibniz against prime notation, composite arguments, sigma notation, and vector components.

**Evidence.** BC-QA-02012 exists only to read or convert derivative notation; BC-QA-10016 demands the general term in sigma form; the scoring guidelines award notation dependent points such as BC-PT-99053 for limit notation on an improper integral. Sources: ced:12, sg-25:18.

**Mapped to 10 archetypes.** BC-QA-01009, BC-QA-02004, BC-QA-02012, BC-QA-03008, BC-QA-05005, BC-QA-06003, BC-QA-06014, BC-QA-09004, BC-QA-09010, BC-QA-10018

## BC-DF-05 Contextual interpretation [verified]

The response must translate a number or an expression back into the situation, naming the quantity, the interval, and the units rather than stopping at the value.

**Evidence.** BC-QA-06015 and BC-QA-04001 are interpretation archetypes whose points depend on naming quantity, interval, and units (sg-23:2, sg-24:2); BC-PT-99007 and BC-PT-99008 are the matching point types. Sources: sg-23:2, sg-24:2.

**Mapped to 15 archetypes.** BC-QA-01010, BC-QA-02009, BC-QA-02012, BC-QA-02013, BC-QA-04001, BC-QA-04004, BC-QA-04006, BC-QA-05011, BC-QA-06001, BC-QA-06006, BC-QA-07008, BC-QA-07009, BC-QA-08001, BC-QA-08014, BC-QA-09009

## BC-DF-06 Algebraic burden [inferred]

The volume and fragility of the manipulation between a correct setup and a correct value, where the calculus decision is settled early and the remaining cost is arithmetic or symbolic.

**Evidence.** BC-QA-06010 by linear partial fractions, BC-QA-06009 by parts, and BC-QA-03004 solving for dy/dx carry long manipulations after the method is chosen. [inferred] from the expected_solution_path of those records. Sources: ced:124.

**Mapped to 25 archetypes.** BC-QA-02008, BC-QA-02010, BC-QA-03001, BC-QA-03004, BC-QA-03009, BC-QA-04007, BC-QA-04008, BC-QA-04010, BC-QA-05002, BC-QA-06002, BC-QA-06005, BC-QA-06008, BC-QA-06009, BC-QA-06010, BC-QA-06011, BC-QA-06016, BC-QA-07003, BC-QA-08008, BC-QA-09002, BC-QA-09005, BC-QA-10003, BC-QA-10005, BC-QA-10016, BC-QA-10017, BC-QA-10019

## BC-DF-07 Calculator workflow [verified]

Whether a result comes from one of the four required calculator capabilities, and with it the obligation to write the setup beside the reported value and to round or truncate to three places after the decimal point.

**Evidence.** BC-QA-08001, BC-QA-06005, and BC-QA-09005 are calculator archetypes whose rubrics split a setup point from an answer point (sg-25:2, sg-25:3); the rule is recorded in ../research/exam/calculator-policy.md. Sources: ced:8, sg-25:2, sg-25:3.

**Mapped to 15 archetypes.** BC-QA-04002, BC-QA-04005, BC-QA-05002, BC-QA-06002, BC-QA-06005, BC-QA-06015, BC-QA-08001, BC-QA-08010, BC-QA-08011, BC-QA-09002, BC-QA-09004, BC-QA-09008, BC-QA-09009, BC-QA-09012, BC-QA-09013

## BC-DF-08 Multi-step dependency [verified]

A later step cannot start until an earlier result exists, so one early slip propagates; the dependency may run inside a part or across parts of the same question.

**Evidence.** BC-QA-10013 needs the ratio limit before the interior and then the endpoints; BC-QA-05006 needs the critical points before the candidates comparison; BC-QA-07003 needs both antiderivatives and the constant before the particular solution (sg-25:18). Sources: sg-25:18.

**Mapped to 28 archetypes.** BC-QA-02006, BC-QA-02007, BC-QA-02008, BC-QA-02010, BC-QA-02011, BC-QA-02013, BC-QA-03004, BC-QA-04007, BC-QA-05006, BC-QA-05012, BC-QA-06010, BC-QA-06011, BC-QA-06013, BC-QA-07004, BC-QA-08001, BC-QA-08009, BC-QA-08012, BC-QA-09001, BC-QA-09002, BC-QA-09003, BC-QA-09005, BC-QA-09006, BC-QA-09007, BC-QA-09010, BC-QA-10001, BC-QA-10008, BC-QA-10017, BC-QA-10020

## BC-DF-09 Theorem recognition [verified]

The prompt does not name the tool, so the response must recognise which theorem or test applies and then state its hypotheses before its conclusion.

**Evidence.** BC-QA-01011 on the Intermediate Value Theorem, BC-QA-05010 on the Extreme Value Theorem, BC-QA-05001 on the Mean Value Theorem, and BC-QA-10001 on test selection all require the hypotheses to be checked; BC-PT-99016 and BC-PT-99017 are the matching point types. Sources: ced:87, sg-24:4.

**Mapped to 17 archetypes.** BC-QA-01003, BC-QA-01005, BC-QA-01011, BC-QA-03005, BC-QA-03006, BC-QA-04002, BC-QA-05001, BC-QA-06012, BC-QA-07007, BC-QA-08003, BC-QA-08006, BC-QA-08014, BC-QA-10001, BC-QA-10004, BC-QA-10005, BC-QA-10007, BC-QA-10013

## BC-DF-10 Required justification [verified]

A point depends on a written reason rather than on a value, so the response must say why the conclusion follows and must tie the reason to the given function.

**Evidence.** BC-QA-05005 requires a reason tied to the supplied graph, BC-QA-05008 requires the sign of the derivative as the reason, and BC-QA-06001 may require an over or under estimate justification; BC-PT-99010, BC-PT-99061, and BC-PT-99063 are the matching point types (sg-23:3). Sources: sg-23:3, sg-24:3.

**Mapped to 22 archetypes.** BC-QA-01001, BC-QA-01003, BC-QA-01004, BC-QA-01006, BC-QA-01007, BC-QA-01009, BC-QA-01012, BC-QA-01015, BC-QA-02004, BC-QA-02005, BC-QA-04008, BC-QA-04009, BC-QA-06001, BC-QA-06002, BC-QA-06003, BC-QA-06012, BC-QA-06016, BC-QA-08006, BC-QA-09008, BC-QA-09011, BC-QA-10018, BC-QA-10020

## BC-DF-11 Unfamiliar surface presentation [inferred]

The underlying structure is routine but the surface is dressed unusually, through an unfamiliar context, an unnamed function, a relation instead of a function, or a quantity defined by another question part.

**Evidence.** BC-QA-10010 builds a Taylor polynomial from a relation rather than from a formula; BC-QA-05007 classifies a critical point for a function given indirectly; BC-QA-04005 places a rate in a setting other than motion. [inferred] from the invariant_structure of those records. Sources: ced:87.

**Mapped to 4 archetypes.** BC-QA-01010, BC-QA-04010, BC-QA-05012, BC-QA-06008

## BC-DF-12 Sign and direction handling [verified]

The response must track a sign, a direction of motion, or a decreasing quantity, and a sign change inside the interval changes the correct procedure rather than only the arithmetic.

**Evidence.** BC-QA-08003 separates displacement from total distance by the sign of velocity, BC-QA-04004 decides direction of motion, and BC-QA-08010 handles boundary curves that cross (sg-24:6). Sources: sg-24:6, ced:153.

**Mapped to 25 archetypes.** BC-QA-01009, BC-QA-02006, BC-QA-02007, BC-QA-04001, BC-QA-04002, BC-QA-04003, BC-QA-04004, BC-QA-04007, BC-QA-05005, BC-QA-05007, BC-QA-05008, BC-QA-06005, BC-QA-06006, BC-QA-06014, BC-QA-06015, BC-QA-07004, BC-QA-07005, BC-QA-07008, BC-QA-07010, BC-QA-08003, BC-QA-08006, BC-QA-09002, BC-QA-09008, BC-QA-09011, BC-QA-10014

## BC-DF-13 Reversed reasoning direction [inferred]

The question runs backwards from the practised order, supplying the output and asking for the input, the parameter, or the function that produced it.

**Evidence.** BC-QA-01008 solves for the parameter that makes a piecewise function continuous, BC-QA-05002 solves for the value the Mean Value Theorem provides, and BC-QA-07007 verifies a supplied solution instead of producing one. [inferred] from the variants tagged with the reasoning direction dimension. Sources: ced:87.

**Mapped to 14 archetypes.** BC-QA-01005, BC-QA-01013, BC-QA-03002, BC-QA-03004, BC-QA-03006, BC-QA-04003, BC-QA-05003, BC-QA-05009, BC-QA-05011, BC-QA-06004, BC-QA-06016, BC-QA-08008, BC-QA-09009, BC-QA-10003

## BC-DF-14 Missing or implicit given [inferred]

Something the procedure needs is not handed over: the interval, the endpoints, the initial condition, or the point of evaluation must be located or derived first.

**Evidence.** BC-QA-08008 requires the intersection points before the limits of integration, BC-QA-06005 may require the initial condition to be located, and BC-QA-02001 variants leave the interval to be chosen. [inferred] from the difficulty_variables of those records. Sources: sg-24:3.

**Mapped to 34 archetypes.** BC-QA-01003, BC-QA-01006, BC-QA-01009, BC-QA-01011, BC-QA-01015, BC-QA-03003, BC-QA-03004, BC-QA-04002, BC-QA-04010, BC-QA-05001, BC-QA-06001, BC-QA-06004, BC-QA-06005, BC-QA-06006, BC-QA-06008, BC-QA-06010, BC-QA-06013, BC-QA-06014, BC-QA-06015, BC-QA-07006, BC-QA-07007, BC-QA-07008, BC-QA-08003, BC-QA-08008, BC-QA-08009, BC-QA-09005, BC-QA-09007, BC-QA-09008, BC-QA-09012, BC-QA-10009, BC-QA-10013, BC-QA-10015, BC-QA-10018, BC-QA-10020

## BC-DF-15 Unsignposted procedure selection [verified]

The part names no method, so choosing the technique is the assessed step and a wrong choice costs the whole part rather than one point.

**Evidence.** BC-QA-06016, BC-QA-03009, BC-QA-01014, and BC-QA-10001 exist as selection archetypes; the Chief Reader commentary on test selection in series work supports the separation (cr-24:23). Sources: cr-24:23, ced:186.

**Mapped to 3 archetypes.** BC-QA-01013, BC-QA-06001, BC-QA-06016

## BC-DF-16 Units and labelling demand [verified]

Units, labels, or a named variable are scored separately from the value, so a correct number can still lose the point.

**Evidence.** BC-PT-99006 is a units point and BC-PT-99064 a labelled values point; BC-QA-04002 and BC-QA-06015 both carry the units demand inside the part (sg-24:2). Sources: sg-24:2, ced:12.

**Mapped to 11 archetypes.** BC-QA-01002, BC-QA-01012, BC-QA-02012, BC-QA-03003, BC-QA-04001, BC-QA-04002, BC-QA-06001, BC-QA-07009, BC-QA-08001, BC-QA-09004, BC-QA-09007

## BC-DF-17 Case splitting at a boundary [verified]

The interval must be cut where a sign changes, where a piecewise rule changes, or where a curve crosses, and the response must supply the cut as well as the pieces.

**Evidence.** BC-QA-08010 splits where the boundary curves cross, BC-QA-06006 may split where the net rate changes sign, and BC-QA-01006 tests a piecewise rule at the join (sg-24:6). Sources: sg-24:6.

**Mapped to 13 archetypes.** BC-QA-01004, BC-QA-01006, BC-QA-01008, BC-QA-01015, BC-QA-02005, BC-QA-04004, BC-QA-05008, BC-QA-06005, BC-QA-06006, BC-QA-06013, BC-QA-08003, BC-QA-08010, BC-QA-08011

## How the factors combine [inferred]

Factors are not independent. A part carrying several factors at once costs more than the sum of its parts would suggest, because an early factor blocks the step where a later factor would be exercised. The distribution over the active archetypes is: 1 factors on 32 archetypes, 2 factors on 40 archetypes, 3 factors on 32 archetypes, 4 factors on 15 archetypes, 5 factors on 6 archetypes, 6 factors on 3 archetypes, 7 factors on 1 archetypes.

The pairs that co-occur most often across the archetype records:

| Pair | Archetypes | Reading |
|---|---|---|
| BC-DF-03 with BC-DF-10 | 10 | both factors sit in the same part and each can end the response before the other is reached |
| BC-DF-03 with BC-DF-14 | 10 | both factors sit in the same part and each can end the response before the other is reached |
| BC-DF-02 with BC-DF-14 | 10 | both factors sit in the same part and each can end the response before the other is reached |
| BC-DF-01 with BC-DF-08 | 10 | both factors sit in the same part and each can end the response before the other is reached |
| BC-DF-12 with BC-DF-14 | 9 | both factors sit in the same part and each can end the response before the other is reached |
| BC-DF-06 with BC-DF-08 | 9 | long manipulation feeding a later step, so one slip carries forward |
| BC-DF-10 with BC-DF-14 | 8 | both factors sit in the same part and each can end the response before the other is reached |
| BC-DF-02 with BC-DF-06 | 8 | both factors sit in the same part and each can end the response before the other is reached |
| BC-DF-01 with BC-DF-14 | 7 | both factors sit in the same part and each can end the response before the other is reached |
| BC-DF-06 with BC-DF-14 | 7 | both factors sit in the same part and each can end the response before the other is reached |
| BC-DF-02 with BC-DF-08 | 7 | both factors sit in the same part and each can end the response before the other is reached |
| BC-DF-08 with BC-DF-14 | 7 | both factors sit in the same part and each can end the response before the other is reached |
| BC-DF-09 with BC-DF-14 | 7 | both factors sit in the same part and each can end the response before the other is reached |
| BC-DF-03 with BC-DF-16 | 6 | both factors sit in the same part and each can end the response before the other is reached |

Three combinations are worth naming with their archetypes. BC-QA-05011 carries the modelling step, the domain restriction, and the global justification at once, so BC-DF-01, BC-DF-02, BC-DF-10, and BC-DF-14 all act inside one part. BC-QA-10013 chains BC-DF-08 with BC-DF-09: the ratio limit must be produced before the endpoint tests can be chosen, and each endpoint needs its own named test. BC-QA-06005 shows how BC-DF-07 changes the shape of a part rather than only its load: with a calculator the antidifferentiation disappears and the setup-plus-result rule replaces it, and without one BC-DF-06 returns in its place.

The factors that appear most often across the catalogue are BC-DF-14 on 34 archetypes, BC-DF-03 on 30 archetypes, BC-DF-02 on 30 archetypes, BC-DF-08 on 28 archetypes, BC-DF-01 on 27 archetypes.

