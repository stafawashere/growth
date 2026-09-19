---
title: AP Calculus BC Multiple-Choice Distractor Taxonomy
research_date: 2026-09-19
status: draft
purpose: The mechanism categories that account for the wrong options in the indexed official multiple-choice questions, the evidence standing behind each, and how option choice could serve a future system as a diagnostic signal.
---

# AP Calculus BC Multiple-Choice Distractor Taxonomy

One section per mechanism category. Every category below is drawn from the `distractor_analysis` field of the 91 records in `../../data/mcq_records.json`, described in [mcq-analysis.md](mcq-analysis.md) and tabulated per question in [official-sample-question-index.md](../official-material/official-sample-question-index.md).

No official rationale exists for any option in any of the three source documents. Every mechanism named below is therefore an inference from the arithmetic or structure of the printed option, or an admission that the option could not be worked. Across the 91 records there are 318 option entries: 205 carry `inferred` and 113 carry `uncertain`, and none carries `verified`.

## Conceptual confusion [inferred]

The largest category, with 116 option entries across 50 records. The option is reachable by a correct calculation of the wrong object, or by applying a definition that names a different idea from the one the stem asks about.

Its clearest sub-pattern is reading a derivative as the function it came from, or the reverse. BC-MCQ-CED-007 offers the intervals on which a graphed integrand increases where the stem asks where the accumulation function increases. BC-MCQ-SAMPLE-011 and BC-MCQ-PE2012-041 both print candidate graphs of a function given the graph of its derivative. BC-MCQ-SAMPLE-013 offers a sentence naming a temperature where the stem asks about a rate. A second sub-pattern confuses one named object with a neighbouring one: BC-MCQ-PE2012-014 offers the exponential model where the stem asks which equation is logistic, and BC-MCQ-CED-009 offers a field depending on the wrong variable. A third treats a structural feature as a different structural feature, as in BC-MCQ-PE2012-011 and BC-MCQ-PE2012-029, where a corner is offered as a discontinuity, a vertical asymptote, or a point of differentiability. No rationale is official for any of these.

## Not determined [uncertain]

The second largest category, with 101 option entries across 34 records, and not a mechanism at all. It records that the option, the stem, or the figure is not recoverable from the cached text, so no mechanism was asserted.

It covers every option of BC-MCQ-CED-013, BC-MCQ-CED-015, BC-MCQ-CED-017, BC-MCQ-CED-018, and BC-MCQ-CED-019, most of the standalone sample set, whose mathematics the text layer drops entirely, and BC-MCQ-PE2012-010, BC-MCQ-PE2012-015, BC-MCQ-PE2012-018, BC-MCQ-PE2012-035, BC-MCQ-PE2012-037, BC-MCQ-PE2012-040, and BC-MCQ-PE2012-042, whose stems or figures are lost. The correct option on each of those records still comes from the printed answer key.

## Algebra slip [inferred]

Thirty-seven option entries across 26 records. The calculus step is set up correctly and the failure is in the manipulation that follows: a term dropped, a constant inverted, a root discarded, a substitution mishandled.

Examples are BC-MCQ-CED-003, where the three tabulated contributions are combined wrongly; BC-MCQ-CED-016, where the boundary term of an integration by parts is evaluated wrongly; BC-MCQ-PE2012-013, where an extra factor survives the solution of the ratio inequality; and BC-MCQ-PE2012-019, where only one root of the resulting quadratic is kept. This category is the hardest to assert confidently without a rationale, because more than one manipulation can land on the same number. No rationale is official.

## Sign error [inferred]

Sixteen option entries across 14 records. The option differs from the correct one by the sign of a term or of a whole expression.

BC-MCQ-CED-005 offers a growing height where the stem states a shrinking one. BC-MCQ-CED-016 adds the given integral to the boundary term where the integration by parts formula subtracts it. BC-MCQ-PE2012-012 reverses the sign convention of the second derivative test. BC-MCQ-PE2012-045 takes a reflection symmetry to make two endpoint derivatives equal rather than opposite. No rationale is official.

## Wrong limits [inferred]

Twelve option entries across 6 records, concentrated in integration and in polar area. The integrand is right and the interval is not.

BC-MCQ-CED-006 offers Riemann sums whose sample points omit the left endpoint offset or whose width is the upper limit rather than the difference of the endpoints. BC-MCQ-CED-021 offers a polar area taken over a full revolution rather than over the shaded region. BC-MCQ-PE2012-006 keeps the original limits after a substitution. BC-MCQ-PE2012-008 uses the endpoints opposite to the ones the requested Riemann sum needs. No rationale is official.

## Reversed quantities [inferred]

Eight option entries across 7 records. The two objects in a ratio, a difference, or a pairing are exchanged.

BC-MCQ-CED-010 integrates the curve instead of the width between the boundaries. BC-MCQ-PE2012-024 reports the derivative where the function is asked for. BC-MCQ-PE2012-028 takes the ratio in an indeterminate limit the other way round. BC-MCQ-PE2012-044 reports the petal area rather than the region outside the petals, and in another option adds it to the circle rather than subtracting it. No rationale is official.

## Chain rule omitted [inferred]

Eight option entries across 5 records. The inner derivative factor is dropped, or the wrong layer of a composite is differentiated.

BC-MCQ-CED-001 offers the value that a small-angle limit gives when the doubled inner argument is dropped from the numerator. BC-MCQ-CED-020 offers the series for the unscaled exponential and, separately, a series whose leading factor survives but whose powers do not carry the scaling. BC-MCQ-PE2012-001 offers both a cubed cosine and a squared cosine. BC-MCQ-PE2012-038 offers the derivative with respect to the model variable without multiplying by the rate at which that variable changes. No rationale is official.

## Product rule omitted [inferred]

Five option entries across 5 records. A product is differentiated as the product of the derivatives, or one of the two terms is dropped.

BC-MCQ-CED-003 multiplies the two tabulated derivatives together. BC-MCQ-CED-004 drops the contribution of the mixed term. BC-MCQ-CED-005 and BC-MCQ-CED-012 each leave one term of a two-term product rule result. BC-MCQ-PE2012-026 drops the product rule when differentiating a radius times a trigonometric factor. No rationale is official.

## Theorem condition ignored [inferred]

Six option entries across 5 records. A named theorem or a convergence test is applied or withheld without its hypotheses being checked.

BC-MCQ-SAMPLE-014 offers the claim that no condition beyond continuity is needed for the Mean Value Theorem conclusion, and separately offers existence of the derivative at one point in place of differentiability across the interval. BC-MCQ-SAMPLE-022 declares divergence without checking the alternating series conditions. BC-MCQ-PE2012-020 judges an integral improper although both roots of the denominator lie outside the interval. BC-MCQ-PE2012-028 declares a limit nonexistent without recognising the indeterminate form. No rationale is official.

## Forgot constant [inferred]

Four option entries across 4 records. A constant factor introduced by a substitution, or a term the formula requires, is omitted.

BC-MCQ-CED-016 omits the subtraction of the given integral from the boundary term. BC-MCQ-PE2012-006 omits the differential factor from the substitution. BC-MCQ-PE2012-025 omits the same factor in an improper integral. BC-MCQ-PE2012-032 uses derivative values as Taylor coefficients without dividing by the factorials. No rationale is official.

## Compound mechanisms [inferred]

Four option entries across 4 records, where one option carries two of the categories above at once.

BC-MCQ-CED-022 uses both the wrong derivative bound and the wrong factorial and power in a Lagrange error bound. BC-MCQ-PE2012-007 uses both the inverse tangent derivative and an unsubstituted dependent variable. BC-MCQ-PE2012-026 pairs a reversed quantity with a sign error. BC-MCQ-PE2012-040 omits the square of a cross-sectional side and introduces the factor of pi that the disc method would bring. These are recorded as single entries rather than split, because option choice cannot separate the two failures. No rationale is official.

## Calculator mechanism [uncertain]

One option entry, on BC-MCQ-CED-012, where a value sits close to the correct one without matching it and a calculator mode or window issue is the most economical explanation. The entry is tagged `uncertain` because the printed value could equally follow from an algebraic slip. Calculator-specific mechanisms are rare in these sets because a wrong window or a degree-mode setting usually produces a value that is not among the printed options at all.

## Option choice as a diagnostic signal [inferred]

A future system that records which option a student chose, and not only whether the choice was correct, gains a coarse signal about why. The mapping below is stated as consistency, not as identification: a single option choice is consistent with the mechanism named and with other routes to the same number, and no official rationale supports any of it.

| Mechanism category | Consistent with error | Consistent with misconception |
|---|---|---|
| Chain rule omitted | BC-ERR-03001, BC-ERR-06027 | BC-MIS-03002, BC-MIS-06023 |
| Product rule omitted | BC-ERR-03008, BC-ERR-04018 | BC-MIS-05033 |
| Sign error | BC-ERR-05021, BC-ERR-05037, BC-ERR-07002 | BC-MIS-04002 |
| Wrong limits | BC-ERR-06018, BC-ERR-06002, BC-ERR-08019 | BC-MIS-08012 |
| Reversed quantities | BC-ERR-02021, BC-ERR-99013 | BC-MIS-09012 |
| Forgot constant | BC-ERR-06021, BC-ERR-07026 | BC-MIS-07016, BC-MIS-08019 |
| Theorem condition ignored | BC-ERR-10022, BC-ERR-99017, BC-ERR-10037 | BC-MIS-10012, BC-MIS-99010 |
| Conceptual confusion, derivative read as function | BC-ERR-05015, BC-ERR-06008 | BC-MIS-05010 |
| Conceptual confusion, signed against unsigned area | BC-ERR-08019 | BC-MIS-06012 |
| Calculator mechanism | BC-ERR-99021, BC-ERR-02032 | BC-MIS-08003 |
| Algebra slip | BC-ERR-10014, BC-ERR-10038 | no stable match established |
| Not determined | no match | no match |

Three properties of these sets bound how far such a signal reaches. First, only about two thirds of the option entries carry any mechanism at all, so a third of wrong choices in this corpus map to nothing. Second, the algebra slip category has no stable counterpart in `../../data/errors.json`, because a slip is defined by the manipulation and not by the calculus idea, and the same number can be reached several ways. Third, a compound option confounds two mechanisms in one choice, so the signal it carries is weaker than a single-mechanism option of the same superficial shape. The full signal registry is `../../data/diagnostic_signals.json` and the reasoning about it is in [../misconceptions/diagnostic-signals.md](../misconceptions/diagnostic-signals.md).

## Unresolved [uncertain]

The mapping table above has not been checked against any student response data, because none of the three source documents publishes option-level response frequencies. Whether the mechanism a distractor was designed to catch is the mechanism that students who choose it actually used cannot be established from these documents.

Whether the mechanisms named here are the mechanisms the item writers intended is also unestablished. The inference runs from the printed number back to a plausible route, and for the algebra slip category in particular more than one route reaches the same option.

For the 2012 practice exam question 82, recorded as BC-MCQ-PE2012-035, the cached option list does not contain the value a direct computation gives, so the option set and the official key could not be reconciled and no mechanism was assigned to any option. Whether the cache lost an option or the printed set differs from expectation is open.
