---
title: AP Calculus BC Free-Response Question Analysis
research_date: 2026-09-19
status: draft
purpose: How a BC free-response question is built out of parts, what the calculator slots ask that the others do not, how representations and units combine inside one question, and what each part distinguishes about a response.
---

# AP Calculus BC Free-Response Question Analysis

This file reads the 249 part records in `data/frq_records.json` as structure. Counts of how often a type recurs across administrations live only in [historical-frequency.md](historical-frequency.md).

## Structure of the free-response section [verified]

How many free-response questions there are, how the section is timed, and which questions permit a graphing calculator are stated in [../exam/exam-structure.md](../exam/exam-structure.md) and are not restated here. What matters for this file is the consequence of that structure: a question is not a single task but an ordered set of parts sharing one stem, and the stem is what carries the function, the table, the graph, the figure, or the context that every part then draws on. The 249 indexed part records belong to 67 questions, and no part in the corpus stands alone.

## The multi-part structure of a question [verified]

Sixty-one of the 67 indexed questions have a scoring guideline in the corpus. Sixty of those total 9 points and one, the 2021 Q4 question, totals 8. The remaining six questions are the 2018 set, where the free-response document was recovered and the scoring guideline was not, so those 22 parts carry 0 points by record convention rather than by rubric.

Forty-eight of the 67 questions have four parts and 19 have three. The 9 points do not spread evenly. Across the 227 scored parts the mean point value rises through the question, from 2.20 for a first part and 2.30 for a second to 2.66 for a third and 2.55 for a fourth, and the last part of a question carries the largest single share in 37 of the 61 scored questions. Two points is the most common part value at 116 of 249 parts, with 72 parts at 3, 21 at 1, 11 at 4, and 7 at 5.

Parts chain in two ways that the `scoring_behaviors` field makes visible. The first is a shared object: the 2019 Q3 stem hands every part the same graph, and each part reads different information off it, so a misread in one part does not carry into the next. The second is a produced object: BC-FRQ-2019-Q6-D must integrate a series term that BC-FRQ-2019-Q6-B produced, and BC-FRQ-2019-Q4-C depends on the relation built in BC-FRQ-2019-Q4-B. Rubrics handle the second case with a structural cap, so a wrong earlier value can still earn later method points but the part is capped, which is why records such as BC-FRQ-2013-Q5-C record two caps on one part.

## The calculator questions and the no-calculator questions [verified]

The split is exact in the corpus. All 44 part records for Q1 and all 42 for Q2 are `calculator`; all 163 records for Q3 through Q6 are `no_calculator`. The general calculator policy and the setup-plus-result rule are in [calculator-vs-noncalculator.md](calculator-vs-noncalculator.md); what follows is what the two calculator slots ask.

Q1 is a contextual modelling slot. Its parts carry the representation `Contextual model` in 43 of 44 records and `Symbolic (analytical) expression` in 41, with a `Calculator-generated numerical result` in 29 and a `Numerical table` in 12. The work is recovering an accumulated amount from a rate, reading an average value, locating an extremum of an accumulation, and interpreting a computed number back into the situation. Its primary unit is BC-UNIT-08 in 20 of 44 records and BC-UNIT-06 in 8.

Q2 is the BC-only applications slot. Its primary unit is BC-UNIT-09 in 36 of 42 records, and its representations are `Parametric equations` in 21, `Polar equation` in 19, and `Vector-valued function` in 16. The assessed work is speed, total distance, an acceleration vector, a coordinate recovered from an initial position, and an area between polar curves, all of which the policy expects to be produced numerically with the setup written beside the result.

Q3 through Q6 ask what a device would bypass. Their parts are the antidifferentiation techniques, the rule manipulations, the theorem statements, the separation of variables and Euler steps, and the whole of the series machinery. Q6 is BC-UNIT-10 in all 42 of its records, with `Series (finite partial sums or infinite)` present in 39.

## Representation mix by question slot [verified]

Each part record lists the representations its information arrives in, and the mix is slot-specific. Q1 is contextual and symbolic. Q2 is parametric, polar, and vector-valued. Q3 leans graphical, with `Graphical` in 22 of 42 records beside `Symbolic (analytical) expression` in 23 and `Contextual model` in 18. Q4 is the most mixed slot in the corpus, with `Graphical` in 23, `Numerical table` in 13, `Contextual model` in 13, `Symbolic (analytical) expression` in 12, and `Verbal description` in 11 across 42 records. Q5 is predominantly symbolic, 32 of 37, with `Differential equation` in 9. Q6 is series and symbol only, with a single graphical record and two tabular ones. The representation ids themselves and what each one demands of a reader are in [representation-types.md](representation-types.md).

## How concepts combine inside one question [verified]

Two fields record combination. `concepts_combined` counts the separately taught ideas a part needs: 15 of 249 parts name one concept, 104 name two, 120 name three, 9 name four, and 1 names five. `secondary_units` records when a part reaches outside its primary unit: 89 parts name none, 134 name one, and 26 name two.

The pairings are not arbitrary. BC-UNIT-06 with BC-UNIT-08 is the dominant one, because an application of integration is almost always executed as an accumulation, and BC-UNIT-05 with BC-UNIT-06 is the next, because an extremum of an accumulated quantity needs both the candidates argument and the integral that produced the quantity. BC-UNIT-02 with BC-UNIT-04 pairs the derivative rule with the contextual reading of the value it produces, and BC-UNIT-08 with BC-UNIT-09 covers the parametric and polar parts that are area or length computations underneath. The observed counts for every pairing are in [historical-frequency.md](historical-frequency.md).

## Shared AB and BC questions against BC-only questions [verified]

The `shared_with_ab` field splits the corpus 128 shared against 121 BC-only, and it aligns with the question slot rather than with the topic. Every Q1, Q3, and Q4 record is shared; every Q2, Q5, and Q6 record is BC-only. The `scope` field matches exactly, 128 `shared` and 121 `BC_only`.

The unit profile of the two halves differs sharply. The shared parts sit in BC-UNIT-06 (30), BC-UNIT-05 (23), BC-UNIT-08 (23), BC-UNIT-04 (15), BC-UNIT-07 (15), BC-UNIT-02 (14), BC-UNIT-01 (6), and BC-UNIT-03 (2), and never in BC-UNIT-09 or BC-UNIT-10. The BC-only parts concentrate in BC-UNIT-10 (45) and BC-UNIT-09 (39), then BC-UNIT-08 (12), BC-UNIT-06 (11), BC-UNIT-07 (6), BC-UNIT-05 (3), and small numbers elsewhere. Where a BC-only part sits in a shared unit, the BC-specific element is the technique rather than the topic: improper integrals and integration by parts inside BC-UNIT-06, arc length and logistic behaviour inside BC-UNIT-08 and BC-UNIT-07.

## Justification and interpretation demands [verified]

`justification_requirements` records what a part demands in writing beyond a value. One hundred and nine of the 249 parts carry a demand and 140 record none. Of the 109, the recurring forms are a conclusion that must be written out rather than implied (31 parts), an argument resting on the sign of a derivative (21), a named theorem or test with its hypotheses stated (17), an interval that must be stated with the claim (17), a global rather than local argument (8), and units carried into the reason (6).

`notation_requirements` is populated on all 249 parts, because every part has something that must be written correctly even when nothing must be argued. Integral notation with its limits appears in 70 records, units or labels in 30, Leibniz or prime notation in 19, limit notation in 11, sigma or general-term notation in 6, and vector or ordered-pair notation in 6.

The command verbs make the same demand from the prompt side. Across 407 verb references on 249 parts, BC-CV-01 (find a value, expression, or vector) appears 150 times, BC-CV-14 (show the work that leads to your answer) 29 times, BC-CV-07 (justify your answer) 28, BC-CV-02 (determine whether, or which case holds) 24, BC-CV-08 (give a reason for your answer) 21, BC-CV-13 (show the setup) 16, BC-CV-20 (show that a stated result holds) 12, and BC-CV-10 (interpret the meaning in context) 11. All 29 verbs in `data/taxonomies.json` are attested. The full verb readings are in [../scoring/command-verbs.md](../scoring/command-verbs.md), the justification rules in [../scoring/justification-requirements.md](../scoring/justification-requirements.md), and the notation rules in [../scoring/notation-requirements.md](../scoring/notation-requirements.md).

## The diagnostic value of an FRQ part [verified]

Every one of the 249 records carries a `diagnostic_distinctions` list, 798 entries in total, each naming two responses that score differently and saying what separates them. The value of a part for diagnosis is exactly this: what a wrong answer on it rules in and rules out.

Six distinctions recur across the corpus.

- Global against local justification, 25 entries. A candidates or extremum argument that checks only a neighbourhood and never compares the endpoints. Seen on BC-FRQ-2013-Q1-D, BC-FRQ-2013-Q4-B, BC-FRQ-2015-Q1-C, BC-FRQ-2018-Q1-D, and BC-FRQ-2019-Q1-C.
- Setup correct against value correct, 25 entries. The two failures are opposite and the rubric scores them separately. Seen on BC-FRQ-2012-Q6-A, BC-FRQ-2019-Q1-B, BC-FRQ-2019-Q2-A, and BC-FRQ-2019-Q2-D.
- Chain rule factor omitted, 16 entries. The outer derivative is right and the inner factor is missing, which separates a rule gap from an arithmetic gap. Seen on BC-FRQ-2013-Q3-D, BC-FRQ-2013-Q4-D, BC-FRQ-2014-Q3-D, BC-FRQ-2018-Q2-B, and BC-FRQ-2019-Q2-B.
- Interval not split where the sign or the rule changes, 14 entries. Seen on BC-FRQ-2013-Q4-A, BC-FRQ-2014-Q3-A, BC-FRQ-2015-Q5-B, BC-FRQ-2018-Q1-A, and BC-FRQ-2018-Q1-C.
- Initial condition or constant of integration dropped, 13 entries. The antidifferentiation is right and the particular solution is not. Seen on BC-FRQ-2013-Q6-C, BC-FRQ-2019-Q4-C, BC-FRQ-2021-Q5-A, BC-FRQ-2023-Q2-C, and BC-FRQ-2023-Q3-A.
- Units written against the correct quantity named, 13 entries. A unit string can be present and still describe the wrong object, most often a rate where an amount was asked. Seen on BC-FRQ-2013-Q3-A, BC-FRQ-2014-Q1-A, BC-FRQ-2019-Q4-A, and BC-FRQ-2021-Q1-A.

Forty entries turn on endpoint or interval handling and 49 on a sign or a direction, which is why so many parts distinguish a communication failure from a computation failure rather than distinguishing right from wrong. The mapping from these distinctions to error and misconception records is in [../misconceptions/diagnostic-signals.md](../misconceptions/diagnostic-signals.md).

## Difficulty factors observed on the records [inferred]

Each record's `difficulty_notes` is free text written when the record was created. Those notes were mapped onto the BC-DF taxonomy in `data/taxonomies.json` by keyword, staged as `data/staging/frq-difficulty-map.json`, merged, and propagated into each factor's `official_examples` by `tools/link_official_evidence.py`. The mapping is keyword-driven, so it is [inferred] and a note that describes a factor in words the rules do not catch is not counted. Twenty-two of the 249 records matched no factor.

Across the 227 records that matched at least one, 492 factor assignments were made: BC-DF-01 number of concepts combined, 79 records; BC-DF-08 multi-step dependency, 61; BC-DF-06 algebraic burden, 48; BC-DF-03 unusual representation, 36; BC-DF-10 required justification, 36; BC-DF-02 prerequisite depth, 32; BC-DF-07 calculator workflow, 31; BC-DF-04 notation complexity, 30; BC-DF-09 theorem recognition, 30; BC-DF-12 sign and direction handling, 23; BC-DF-14 missing or implicit given, 21; BC-DF-05 contextual interpretation, 17; BC-DF-16 units and labelling demand, 17; BC-DF-17 case splitting at a boundary, 13; BC-DF-13 reversed reasoning direction, 10; BC-DF-15 unsignposted procedure selection, 5; BC-DF-11 unfamiliar surface presentation, 3.

Two factors sit near the floor and should be read as artefacts of the notes rather than of the questions. BC-DF-15 and BC-DF-11 describe properties a note tends to state implicitly, by describing the method the response had to choose rather than saying that no method was named. The readings of each factor are in [difficulty-factors.md](difficulty-factors.md).

## Archetype gaps recorded in the notes [inferred]

Thirteen part records carry an `archetype_gap` note, meaning the part was tagged with the closest available archetype and the record says so. They are candidates for new archetypes, not confirmed ones.

- BC-FRQ-2013-Q1-B and BC-FRQ-2015-Q1-A: a definite integral of a rate on a calculator with no initial condition and no rate out.
- BC-FRQ-2018-Q1-A: the same, with a piecewise rate.
- BC-FRQ-2013-Q2-B: solving for the time at which a Cartesian coordinate of a particle on a polar curve reaches a stated value.
- BC-FRQ-2013-Q2-C: position vector of a particle on a polar curve together with its velocity vector.
- BC-FRQ-2014-Q2-B: derivative of a Cartesian coordinate with respect to the angle on a polar curve, as distinct from the derivative of the radial function.
- BC-FRQ-2014-Q2-C: rate of change with respect to the angle of the gap between two polar curves.
- BC-FRQ-2018-Q5-B and BC-FRQ-2026-Q2-B: the tangent slope to a polar curve in the plane, and solving that relation for the derivative of the horizontal coordinate; BC-QA-09001 is the closest match for both.
- BC-FRQ-2019-Q2-B: average value of a radial function along a polar curve.
- BC-FRQ-2014-Q1-A: an average rate of change reported on its own, with no equation solved against it.
- BC-FRQ-2018-Q2-B: accumulation of a density over a depth interval scaled by a constant cross-sectional area.
- BC-FRQ-2018-Q2-C: bounding an accumulation with a comparison function whose improper integral is supplied.

Seven of the 13 are polar, which is the clearest concentration. Nine further records carry a `point_type_gap` note, where the rubric point has no exact BC-PT counterpart, and those are a separate matter for [../scoring/point-taxonomy.md](../scoring/point-taxonomy.md).

## Unresolved [uncertain]

- The 2018 parts have no rubric in the corpus, so nothing in the point-split, point-type, or scoring-behaviour analysis above rests on them. Their structure claims rest on the free-response document alone.
- The difficulty-factor mapping is keyword-driven over prose written for another purpose. Twenty-two records matched nothing and BC-DF-15 matched five, so the tail of the distribution measures the notes rather than the parts. A re-read of each note against the 17 factor definitions would replace it.
- Pre-2019 records carry inferred archetype and unit mappings, so the shared and BC-only unit profiles above are firmest for 2019 onward.
- Whether the 13 `archetype_gap` notes should become archetypes or variants of existing ones is not settled. The polar cluster in particular could be one archetype with variants rather than seven.
- 2021 carries an administration anomaly on all 21 of its records and its form is unidentified, so its parts are included in structural counts here while being excluded from year denominators in [historical-frequency.md](historical-frequency.md).
