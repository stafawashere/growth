---
title: Partial Credit Structure in the Scoring Guidelines
research_date: 2026-09-19
status: draft
purpose: How partial credit is built inside a part, which points survive an earlier error, which points are blocked by one, and how work is imported across parts.
---

# Partial Credit Structure in the Scoring Guidelines

Citations name the cached document and page, so `sg-25:25` is the cached 2025 scoring guidelines at page 25. The point families referenced here are catalogued in [point-taxonomy.md](point-taxonomy.md).

## Partial credit is built from independent points, then constrained [verified]

The default is independence. sg-22:7 states the second and third points can be earned independently, sg-22:16 states the product rule and chain rule points could be earned in either order, sg-22:10 states two value points may be earned in either order, and sg-26:23 states two series points are independent of each other and a response can earn one without the other.

Dependence is then added by explicit sentences. The three recurring forms are "to be eligible for", "a response must earn X to be eligible for Y", and "a response is eligible for Y only if it has earned X". sg-25:14 uses the first, sg-26:8 the second, sg-23:12 the third. Without such a sentence a point stands alone.

## Points that survive an earlier error [verified]

Answer points routinely survive the loss of a justification. sg-25:5 states a response presenting a local argument or an incorrect global argument does not earn the justification point but is eligible for the answer point with the correct answer. sg-25:9 and sg-25:19 repeat this. sg-26:17 inverts it with a special case where correct conclusions with an insufficient justification earn the minimum point but not the maximum point.

Interpretation points survive computational failure. sg-26:3 states the interpretation point can be earned whether or not the sum form and approximation points were earned.

Conclusion points survive a missing hypothesis. sg-25:12 and sg-26:5 both state a response does not need to earn the continuity point to be eligible for the theorem conclusion point.

Setup points survive a missing answer and answer points survive a missing setup, in different parts. sg-22:5 states that a response that does not earn the first point is still eligible for the remaining three points of the part. sg-26:18 and sg-26:14 both state an unsupported correct value earns the answer point but not the setup point. sg-25:16 gives the answer point on an implied application of the Fundamental Theorem when the explicit derivative point was not earned, and states that a response differencing the integrand at both limits earns the answer point but not the derivative point.

Partial answers earn partial credit by named special case. sg-25:17 gives the reason point but not the location point to a response with two of three correct inflection values and correct reasoning. sg-23:14 gives one of two points for exactly one of two correct intervals with a correct reason. sg-22:11 gives one of two for one of two inflection values with correct justification. sg-22:10 gives one of three for only one of two required function values, and two of three for one correct and one missing.

## Points that do not survive an earlier error [verified]

The strongest blocks are structural. sg-26:13 states a response with no separation of variables earns none of the five points in the part, sg-23:12 states the same for four points, sg-21:20 for five, and sg-19:5 carries the older note that the part scores zero out of four with no separation. sg-21:20 adds that a response with no constant of integration can earn at most three of the five, and sg-23:12 that it can earn at most the first two of four.

Arithmetic errors inside a sum block the value point. sg-25:13 and sg-26:3 both state that if any of the six factors is incorrect, the response does not earn the approximation point, while the form point may still stand on five correct factors. sg-22:15 applies the same rule at seven of eight factors. sg-23:2 states that if there is any error in the Riemann sum, the response does not earn the third point.

Errors in a limit evaluation block the limit point without touching the ratio point. sg-25:25 states the ratio point is banked but the limit point is not earned if there are any errors in simplification or evaluation of the limit.

Incorrect bounds block answer points. sg-22:18 states a definite integral with incorrect bounds does not earn either point of the part. sg-22:8 states a definite integral with incorrect limits is not eligible for the answer point and that an indefinite integral is likewise not eligible. sg-23:17 and sg-23:16 both state a response with incorrect limits of integration after a substitution is not eligible for the answer point.

Errors in a constant multiple block the answer while leaving the form. sg-22:18 states an integrand scaled by any nonzero constant earns the integral point, but a constant other than one will not earn the answer point. sg-22:19 states the same for a volume integral where the constant must be the circle constant.

Imports of the wrong expression block a following point even when the point before was earned. sg-23:8 states that if the integrand is an incorrect speed function imported from an earlier part, the response earns the integrand point and does not earn the answer point. sg-25:21 states a response applying the quotient rule but not the chain rule earns the product rule point, does not earn the chain rule point, and is not eligible for the value point.

## Imported and consistent answers [verified]

The guidelines let a wrong value from one part travel into later parts without being penalised twice. The recurring words are "import" and "consistent".

sg-25:22 states the two polynomial points can be earned with an answer consistent with incorrect derivative values imported from an earlier part. sg-25:23 states a response that imports an incorrect derivative value from either of two earlier parts is eligible for the answer point with a consistent answer. sg-25:19 states candidate values can be imported from an earlier part and the answer point can follow the imported values. sg-25:27 states the reasoning point can be earned with a response consistent with an incorrect interval of convergence imported from an earlier part. sg-26:19 states a response importing an incorrect function from an earlier part is eligible for both volume points. sg-23:7 allows an incorrect derivative expression to be imported provided it was declared in the earlier part. sg-22:12 and sg-22:22 both make a point available only for an answer consistent with the earlier import.

Importing is bounded in two ways. sg-22:12 states a response that imports one particular incorrect derivative relation is eligible for the first point but not the second. sg-25:21 states an imported separation-of-variables solution has not yet earned any of the three points in the part until the differentiation work is done.

## Precision failures as partial credit [verified]

Rounding is handled as a capped deduction rather than a block. The general note caps it at one point per question (sg-25:2, sg-26:2), and the individual notes implement the cap with the clause "unless an earlier point was not earned due to inappropriate rounding" (sg-25:4, sg-25:7, sg-25:8, sg-25:10, sg-25:23, sg-26:7, sg-26:8, sg-26:9).

A decimal presentation error can cost the answer point while leaving the justification point intact. sg-22:5 states a correct justification earns its point even if the answer point is not earned because of a decimal presentation error.

Candidate values inside a justification carry their own precision rule, correct to the first digit after the decimal in sg-25:5 and sg-25:9, and up to three decimal places with correctly rounded integers acceptable in sg-22:5.

## Degree mode as a single deduction [verified]

sg-23:4 states a response presenting answers obtained with a calculator in degree mode does not earn the first point it would otherwise have earned, and is generally eligible for all subsequent points, with two stated exceptions: where no answer is possible in degree mode, or where the question is made simpler by using degree mode. The same paragraph appears at sg-23:6, sg-23:7, sg-23:8 and sg-22:3. sg-23:7 adds that a response finding no solution cannot be assumed to be working in degree mode. The identical single-deduction structure is used at sg-24:13 for a response that explicitly writes an accumulation function with the wrong lower limit.

## Wrong method, partial credit [verified]

A completely correct execution of the wrong named method earns some but not all of the points. sg-25:13 states a completely correct left or right Riemann sum earns the form point but not the value point where a trapezoidal sum was asked. sg-26:3 inverts the allocation for the same situation, giving the value point and not the form point. sg-23:2 and sg-22:15 each state a completely correct left sum earns one of the last two points, and that a left sum with any error or missing factor earns neither.

Two further cases follow this shape. sg-26:19 states a response that correctly rotates the region about the wrong axis earns the integrand form point and is not eligible for the answer point. sg-25:7 states an indefinite integral with a correct integrand does not earn the first integrand point, earns the second, and stays eligible for the answer point.

## Alternate solutions carry full credit [verified]

Nothing in the corpus read reserves credit for the model route. sg-25:5 and sg-25:9 list alternate justifications worth the same point, sg-26:8 lists a second derivative route, sg-25:21 lists a separation-of-variables route through the product and chain rule points, sg-23:21 maps a series-composition route onto all three points of a part, sg-22:12 gives a candidates-test route to a part whose model used sign analysis, and sg-25:25 lists four acceptable convergence tests at an endpoint. sg-21:2 notes that these guidelines can be applied to alternate approaches to ensure those approaches are scored appropriately, which is the general statement behind the practice.
