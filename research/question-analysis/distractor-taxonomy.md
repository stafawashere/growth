---
title: AP Calculus BC Multiple-Choice Distractor Taxonomy
research_date: 2026-09-19
status: draft
purpose: The mechanism categories that account for the wrong options in the indexed official multiple-choice questions, the evidence standing behind each, and how option choice could serve a future system as a diagnostic signal.
---

# AP Calculus BC Multiple-Choice Distractor Taxonomy

One section per mechanism category. Every category below is drawn from the `distractor_analysis` field of the 91 records in `../../data/mcq_records.json`, described in [mcq-analysis.md](mcq-analysis.md) and tabulated per question in [official-sample-question-index.md](../official-material/official-sample-question-index.md).

No official rationale exists for any option in any of the three source documents. Every mechanism named below is therefore an inference from the arithmetic or structure of the printed option, or an admission that the option could not be worked. Across the 91 records there are 318 option entries: 287 carry `inferred` and 31 carry `uncertain`, and none carries `verified`.

Where the primary text layer of a cached document dropped or garbled a stem or an option set, the question was worked instead from the OCR transcription in the matching `page-NNN.ocr.txt` file. That recovery moved 85 option entries out of the `not determined` category. OCR is a machine transcription rather than a second source, so the 42 records that depend on it are tagged `single-source`, and every mechanism drawn from one of them inherits that standing.

## Conceptual confusion [inferred]

The largest category, with 164 option entries across 74 records. The option is reachable by a correct calculation of the wrong object, or by applying a definition that names a different idea from the one the stem asks about.

Its clearest sub-pattern is reading a derivative as the function it came from, or the reverse. BC-MCQ-CED-007 offers the intervals on which a graphed integrand increases where the stem asks where the accumulation function increases. BC-MCQ-SAMPLE-011 and BC-MCQ-PE2012-041 both print candidate graphs of a function given the graph of its derivative. BC-MCQ-SAMPLE-013 offers a sentence naming a temperature where the stem asks about a rate. A second sub-pattern confuses one named object with a neighbouring one: BC-MCQ-PE2012-014 offers the exponential model where the stem asks which equation is logistic, BC-MCQ-CED-009 offers a field depending on the wrong variable, BC-MCQ-CED-017 offers the value at which a logistic population grows fastest where the stem asks for its limit, and BC-MCQ-PE2012-038 offers the value of a model where the stem asks for a rate. A third treats a structural feature as a different structural feature, as in BC-MCQ-PE2012-011 and BC-MCQ-PE2012-029, where a corner is offered as a discontinuity, a vertical asymptote, or a point of differentiability. No rationale is official for any of these.

## Not determined [uncertain]

Twenty-eight option entries across 15 records, and not a mechanism at all. It records that the option could not be worked, so none was asserted. The category held 101 entries before the OCR pass and now holds 28.

What remains is almost entirely figure-bound. BC-MCQ-SAMPLE-011 and BC-MCQ-PE2012-041 print candidate graphs of a function; BC-MCQ-PE2012-015, BC-MCQ-PE2012-018, and BC-MCQ-PE2012-031 depend on a graph whose areas cannot be measured from the transcription; BC-MCQ-SAMPLE-008 and BC-MCQ-SAMPLE-023 lost expressions that neither the text layer nor OCR renders. The rest are single option values that no plausible route reproduces, on BC-MCQ-SAMPLE-015, BC-MCQ-SAMPLE-016, BC-MCQ-SAMPLE-017, BC-MCQ-SAMPLE-021, BC-MCQ-SAMPLE-024, BC-MCQ-PE2012-035, BC-MCQ-PE2012-040, and BC-MCQ-PE2012-042. The correct option on each of those records comes from the printed answer key.

## Algebra slip [inferred]

Forty-four option entries across 31 records. The calculus step is set up correctly and the failure is in the manipulation that follows: a term dropped, a constant inverted, a root discarded, a substitution mishandled.

Examples are BC-MCQ-CED-003, where the three tabulated contributions are combined wrongly; BC-MCQ-CED-016, where the boundary term of an integration by parts is evaluated wrongly; BC-MCQ-PE2012-013, where an extra factor survives the solution of the ratio inequality; BC-MCQ-PE2012-019, where only one root of the resulting quadratic is kept; and BC-MCQ-PE2012-010, where the antiderivative is divided by the original exponent rather than by one more than it. This category is the hardest to assert confidently without a rationale, because more than one manipulation can land on the same number. No rationale is official.

## Sign error [inferred]

Twenty-three option entries across 19 records. The option differs from the correct one by the sign of a term or of a whole expression.

BC-MCQ-CED-005 offers a growing height where the stem states a shrinking one. BC-MCQ-CED-016 adds the given integral to the boundary term where the integration by parts formula subtracts it. BC-MCQ-PE2012-012 reverses the sign convention of the second derivative test. BC-MCQ-PE2012-045 takes a reflection symmetry to make two endpoint derivatives equal rather than opposite. BC-MCQ-PE2012-037 reports the complement of an interval of concavity, and BC-MCQ-PE2012-018 accumulates a signed area in the wrong direction from the point where the function value is known. No rationale is official.

## Wrong limits [inferred]

Twelve option entries across 6 records, concentrated in integration and in polar area. The integrand is right and the interval is not.

BC-MCQ-CED-006 offers Riemann sums whose sample points omit the left endpoint offset or whose width is the upper limit rather than the difference of the endpoints. BC-MCQ-CED-021 offers a polar area taken over a full revolution rather than over the shaded region. BC-MCQ-PE2012-006 keeps the original limits after a substitution. BC-MCQ-PE2012-008 uses the endpoints opposite to the ones the requested Riemann sum needs. No rationale is official.

## Reversed quantities [inferred]

Ten option entries across 9 records. The two objects in a ratio, a difference, or a pairing are exchanged.

BC-MCQ-CED-010 integrates the curve instead of the width between the boundaries. BC-MCQ-PE2012-024 reports the derivative where the function is asked for. BC-MCQ-PE2012-028 takes the ratio in an indeterminate limit the other way round. BC-MCQ-PE2012-044 reports the petal area rather than the region outside the petals, and in another option adds it to the circle rather than subtracting it. BC-MCQ-SAMPLE-017 divides the two component derivatives the other way round, giving the reciprocal of a parametric slope, and BC-MCQ-SAMPLE-019 reports the value an integral takes in place of the parameter that was asked for. No rationale is official.

## Chain rule omitted [inferred]

Twelve option entries across 8 records. The inner derivative factor is dropped, or the wrong layer of a composite is differentiated.

BC-MCQ-CED-001 offers the value that a small-angle limit gives when the doubled inner argument is dropped from the numerator. BC-MCQ-CED-020 offers the series for the unscaled exponential and, separately, a series whose leading factor survives but whose powers do not carry the scaling. BC-MCQ-PE2012-001 offers both a cubed cosine and a squared cosine. BC-MCQ-PE2012-038 offers the derivative with respect to the model variable without multiplying by the rate at which that variable changes. BC-MCQ-SAMPLE-007 offers three variations at once: the chain rule factor dropped, the composite upper limit not substituted, and both together. BC-MCQ-SAMPLE-001 drops a doubled inner argument, and BC-MCQ-SAMPLE-004 omits the radius rate from a surface area derivative. No rationale is official.

## Product rule omitted [inferred]

Five option entries across 5 records. A product is differentiated as the product of the derivatives, or one of the two terms is dropped.

BC-MCQ-CED-003 multiplies the two tabulated derivatives together. BC-MCQ-CED-004 drops the contribution of the mixed term. BC-MCQ-CED-005 and BC-MCQ-CED-012 each leave one term of a two-term product rule result. BC-MCQ-PE2012-026 drops the product rule when differentiating a radius times a trigonometric factor. No rationale is official.

## Theorem condition ignored [inferred]

Seven option entries across 7 records. A named theorem or a convergence test is applied or withheld without its hypotheses being checked.

BC-MCQ-SAMPLE-014 offers the claim that no condition beyond continuity is needed for the Mean Value Theorem conclusion, and separately offers existence of the derivative at one point in place of differentiability across the interval. BC-MCQ-SAMPLE-022 declares divergence without checking the alternating series conditions. BC-MCQ-PE2012-020 judges an integral improper although both roots of the denominator lie outside the interval. BC-MCQ-PE2012-028 declares a limit nonexistent without recognising the indeterminate form. BC-MCQ-CED-019 applies the alternating series test without checking that the terms tend to zero, and BC-MCQ-SAMPLE-024 reverses the conclusion of the integral test. No rationale is official.

## Forgot constant [inferred]

Six option entries across 6 records. A constant factor introduced by a substitution, or a term the formula requires, is omitted.

BC-MCQ-CED-016 omits the subtraction of the given integral from the boundary term. BC-MCQ-PE2012-006 omits the differential factor from the substitution. BC-MCQ-PE2012-025 omits the same factor in an improper integral. BC-MCQ-PE2012-032 uses derivative values as Taylor coefficients without dividing by the factorials. BC-MCQ-CED-015 antidifferentiates an exponential without dividing by the constant in its exponent, and BC-MCQ-SAMPLE-018 drops the constant term of a slope expression at the second Euler step. No rationale is official.

## Compound mechanisms [inferred]

Four option entries across 4 records, where one option carries two of the categories above at once.

BC-MCQ-CED-022 uses both the wrong derivative bound and the wrong factorial and power in a Lagrange error bound. BC-MCQ-PE2012-007 uses both the inverse tangent derivative and an unsubstituted dependent variable. BC-MCQ-PE2012-026 pairs a reversed quantity with a sign error. BC-MCQ-PE2012-040 omits the square of a cross-sectional side and introduces the factor of pi that the disc method would bring. These are recorded as single entries rather than split, because option choice cannot separate the two failures. No rationale is official.

## Calculator mechanism [uncertain]

Three option entries across two records. On BC-MCQ-CED-012 a value sits close to the correct one without matching it, and a calculator mode or window issue is the most economical explanation; that entry is tagged `uncertain` because the printed value could equally follow from an algebraic slip. On BC-MCQ-CED-014 two options undercount the points of inflection of a function given only through its derivative, which a viewing window that hides a turning point near an endpoint would produce. Calculator-specific mechanisms stay rare in these sets because a wrong window or a degree-mode setting usually produces a value that is not among the printed options at all.

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

Three properties of these sets bound how far such a signal reaches. First, 28 of the 318 option entries carry no mechanism at all, almost all of them on questions whose figures exist only as images, so those wrong choices map to nothing. Second, the algebra slip category has no stable counterpart in `../../data/errors.json`, because a slip is defined by the manipulation and not by the calculus idea, and the same number can be reached several ways. Third, a compound option confounds two mechanisms in one choice, so the signal it carries is weaker than a single-mechanism option of the same superficial shape. The full signal registry is `../../data/diagnostic_signals.json` and the reasoning about it is in [../misconceptions/diagnostic-signals.md](../misconceptions/diagnostic-signals.md).

## Unresolved [uncertain]

The mapping table above has not been checked against any student response data, because none of the three source documents publishes option-level response frequencies. Whether the mechanism a distractor was designed to catch is the mechanism that students who choose it actually used cannot be established from these documents.

Whether the mechanisms named here are the mechanisms the item writers intended is also unestablished. The inference runs from the printed number back to a plausible route, and for the algebra slip category in particular more than one route reaches the same option.

The discrepancy previously recorded for the 2012 practice exam question 82, BC-MCQ-PE2012-035, is resolved: the OCR transcription shows a radical that the primary text layer had lost, and the recomputed average matches the official key. One of its four options still resists attribution.

Every mechanism drawn from an OCR transcription inherits that transcription's faults. The OCR pass disagrees with the primary text layer on one tabulated value behind BC-MCQ-CED-013 and drops minus signs from two of its options, and it renders one option of BC-MCQ-PE2012-015 upside down. Where the two layers disagree, the primary layer was preferred and the disagreement recorded on the record; which layer is right has not been settled against the published document itself.
