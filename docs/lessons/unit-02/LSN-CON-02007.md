---
title: LSN-CON-02007 Estimation of a derivative from tabular or graphical information
research_date: 2026-09-29
status: designed
purpose: Authoring spec for the concept lesson on BC-CON-02007, estimating a derivative from a table, a graph or technology, built from authoring_bundle("BC-CON-02007") and the research files it cites, so an author fills plan 15's lesson record without making a teaching decision.
---

# LSN-CON-02007 Estimation of a derivative from tabular or graphical information

Concept BC-CON-02007 (skills BC-SKL-02014, BC-SKL-02015, BC-SKL-02016, BC-SKL-02017, BC-SKL-02018), topic 2.3 of Unit 2, loaded by BC-QA-02013 (listed first), BC-QA-02009 and BC-QA-04002. Its hard parents are BC-CON-02002 and BC-CON-02005 (unit README section 1). It shares LSN-DEC-02-01 with BC-CON-02001 and LSN-DEC-02-02 with BC-CON-02004 and BC-CON-02005.

## Orientation

Served text (46 words), from BC-CON-02007 `description_plain` and the topic's Assessment behaviour paragraph (research/units/unit-02-differentiation-definition-properties.md#2.3 Estimating Derivatives of a Function at a Point): a response estimates the derivative at a point by an average rate over an interval that brackets or abuts the point, shows the difference and the quotient, and attaches compound units; from a graph, a tangent slope; with technology, a named setup and three decimals. No count, no frequency.

## Key ideas

BC-SKL-02014 to BC-SKL-02017 map BC-EK-CHA-2D1; BC-SKL-02018 maps BC-EK-CHA-2D2. Two blocks, both on ced:62.

- ki-1 (core, BC-EK-CHA-2D1). The table method and the graph method, and the units rule, paraphrased from the topic's Estimation, Method from a table and Units paragraphs. Anchor quote (15 words) from ced:62. Notation line: approximately equal to.
- ki-2 (core, BC-EK-CHA-2D2). Core so that the mid band teaches BC-SKL-02018, which no other mid block holds (plan 15, Sourcing, Pipeline step 2). Technology gives the value; the written work names what was computed and reports three decimals (BC-QA-02013 `asked_to_produce`). Anchor quote (19 words) from ced:62.

## Recognition

- BC-QA-04002 (family derivative-from-table, the opening part of a table based FRQ; research/question-analysis/question-archetypes.md#BC-QA-04002 Approximating a derivative from a table with units): `common_givens` a table of values of a contextual quantity and the interval; `asked_to_produce` an approximation at an interior input, a difference and a quotient, and units. The signal is a table and a derivative symbol at a tabulated input. `difficulty_variables` include whether the interval is named or must be chosen, and whether the point lies inside the interval or at an end; ex-1 takes the chosen, bracketing form. Official examples BC-FRQ-2021-Q1-A, BC-FRQ-2022-Q4-A, BC-FRQ-2024-Q1-A, BC-FRQ-2025-Q3-A, BC-FRQ-2026-Q1-A.
- BC-QA-02013 (family technology-numerical-result, one calculator FRQ part; research/question-analysis/question-archetypes.md#BC-QA-02013 Derivative at a point produced with technology): `typical_wording` "Find the value of the derivative at the named input. Show the setup for your calculations"; `common_givens` a function model in a calculator active part. The signal is a formula model and a calculator part.
- BC-QA-02009 (family derivative-from-table): loads BC-SKL-02017 where one supplied value must be read as a slope from a graph (`difficulty_variables`); its rule half belongs to BC-CON-02013 and BC-CON-02014.

What says "not this concept": the interval is named and no point is estimated, which is an average rate (BC-CON-02001, the LSN-DEC-02-01 selector); a function rule with no data and no calculator (the rules). No archetype isolates BC-SKL-02017 (unit README section 3).

## Method choice

One block per family: derivative-from-table (BC-QA-04002 stands for it) and technology-numerical-result (BC-QA-02013).

- st-1, BC-QA-04002. Cue from `asked_to_produce` and `common_givens`. Method, `expected_solution_path[0]`: select the two tabulated values the interval determines, here the rows bracketing the point. Rival, `wrong_approaches`: a pair of rows other than the named or bracketing interval (BC-ERR-02004). Separating feature: the two rows sit on either side of the point.
- st-2, BC-QA-02013. Method, `expected_solution_path[0]`: enter the function, with the written setup naming \(W'(2)\). The archetype's `wrong_approaches` and `prohibited_shortcuts` are empty, so the rival is taken from its error record, a value with no setup (BC-ERR-02031) [inferred]. Separating feature: a formula in a calculator part.

Both archetypes carry `asked_to_produce` and `common_givens`, so neither block is tagged inferred; the st-2 rival is listed under Sources.

## Solution path

- ex-1, BC-QA-04002, both bands, no calculator. Draw: times 0, 4, 6, 10, 12; readings 86, 71, 50, 38, 25 (served pairing); context oven; trend decreasing, so \(H(0)=86\), \(H(4)=71\), \(H(6)=50\), \(H(10)=38\), \(H(12)=25\), point \(t=6\), bracketing rows \(t=4\) and \(t=10\). Steps follow `expected_solution_path`: choose the rows (no value), difference over difference (valued), divide (valued), units (no value). A fluent solver writes the quotient, the value and the units; the row choice is read.
- ex-2, BC-QA-02013, low band, calculator. Draw: level 24, swing 3, scale 4, at 2, context traffic, framing context, so \(W(t)=24+3\sin(\frac{t^2}{4})+\ln(1+t)\) hundred cars. Valued chain: \(W\) (new), \(W'\) (differentiate, what the calculator computes), \(W'(2)\approx1.954\) (evaluate, approx). Written: the setup naming \(W'(2)\) and the value; the keystrokes are not written.

The bundle lists BC-QA-02013 first; ex-1 is BC-QA-04002 because the first four error blocks in the bundle's order are table errors and fall on its draw [inferred].

## Scoring

ex-1's archetype lists BC-PT-99005, BC-PT-99008 and BC-PT-99006, so ex-1 carries a scoring entry, and no step is tagged, so it holds no lines: the generated BC-PT-99005 line (117 words) breaks the brief cap, and the generated BC-PT-99006 line quotes an accepted compound unit that the style check rejects. The two conditions reach the student verbatim as the scoring consequences of err-BC-ERR-02001, err-BC-ERR-02002 and err-BC-ERR-02003 (sg-25:11). ex-2's archetype, BC-QA-02013, lists no `point_types`: no entry, no tags.

Point losses the scoring research names: units missing, of the quantity, or wrong in numerator or denominator (research/scoring/common-point-losses.md#Units points, BC-ERR-99005; cr-22:14, cr-24:4); no setup before a calculator value (research/scoring/common-point-losses.md#Setup points, BC-ERR-99021); fewer than three decimals (research/scoring/common-point-losses.md#Answer points, BC-ERR-99019; sg-25:4).

## Traps

Eight active errors meet the concept's skills; the cap is 4, so the first four in the bundle's order are shown, all on ex-1's draw. Low band all four, mid band the first two.

- err-BC-ERR-02001 (BC-MIS-02001, BC-MIS-02008). Wrong: \(38-71=-33\). Right: \(\frac{38-71}{10-4}\). Distinct. Possible reason from BC-MIS-02001.
- err-BC-ERR-02002 (BC-MIS-02001, BC-MIS-02003). Wrong: the quotient left unevaluated. Right: \(-\frac{11}{2}\). Equivalent, which is the record's point: the quotient alone is not the answer. Possible reason null.
- err-BC-ERR-02003 (BC-MIS-02008, BC-MIS-02001). Wrong: \(-\frac{11}{2}\) degrees Fahrenheit. Right: per minute. Equivalent values. Possible reason from BC-MIS-02008.
- err-BC-ERR-02004 (BC-MIS-02001, BC-MIS-02004). Wrong: rows 4 and 6, \(-\frac{21}{2}\). Right: \(-\frac{11}{2}\). Distinct. Possible reason from BC-MIS-02001.

Not shown: BC-ERR-02024, BC-ERR-02031, BC-ERR-02032, BC-ERR-09023. BC-ERR-02031 and BC-ERR-02032 are the technology traps ex-2 sits beside.

## Representations

One block, low band, from the topic's Representations paragraph (graph to an estimated slope, BC-REP-02 to BC-REP-01) and BC-SKL-02017: a static graph with the tangent drawn at a point and two points read off it. The curve is illustrative [inferred], since no archetype isolates BC-SKL-02017.

## Prerequisite bridge

- BC-PRQ-02004 (supporting parent of BC-SKL-02018), from `description_plain` and `failure_signature`: the setup names the variable of differentiation.

## Time

BC-QA-04002 is "either" on calculator status, so by the template's rule the part is Section I Part A, 2.14 minutes (research/exam/exam-structure.md#Section and part layout) [inferred]; as an FRQ opening part it is 2 points, 3.33 minutes of 15.0. BC-QA-02013 is a calculator part: Section II Part A as an FRQ part, Part B's 2.92 minutes when MCQ shaped (unit README section 5). A fluent solver writes three lines on ex-1 and two on ex-2.

## Checks

- chk-1, completion of ex-1, both bands: the quotient is given. Key \(-\frac{11}{2}\), equal to ex-1's answer.
- chk-2, isomorph on BC-QA-04002, both bands: context download, times 1, 3, 4, 8, 9, readings 12, 20, 27, 44, 60, point 4. Key \(\frac{24}{5}\).
- chk-3, MCQ on BC-QA-04002, low band: context rainfall, times 0, 2, 5, 6, 10, readings 10, 14, 23, 35, 40, point 5. Key \(\frac{21}{4}\). Distractors: 21 (BC-ERR-02001), 3 and 12 (BC-ERR-02004, the one-sided pairs the spec's notes name).

No draw equals a published BC-QA-04002 or BC-QA-02013 `parameter_draw` (content/items_gen_unit04, content/items_gen_unit02).

## Delivery

- orientation: text. Rule 5.
- ki-1: table. Rule 4; BC-SKL-02014 and BC-SKL-02016 list BC-REP-03 (unit README delivery map). Spec: ex-1's table with the point row and its two bracketing rows marked.
- ki-2: text. Rule 5; BC-REP-09 is not figure-bearing.
- ex-1, ex-2: step_reveal. Rule 1.
- err-BC-ERR-02001, err-BC-ERR-02002, err-BC-ERR-02003, err-BC-ERR-02004: step_reveal. Rule 1.
- representations: figure. Rule 3; BC-SKL-02017 lists BC-REP-02. Static: nothing varies in the stem's reading.

Every non-text choice is [inferred], settled by the modality A/B.

## Band plan

- Low (full): orientation, ki-1, ki-2, st-1, st-2, ex-1, the four error blocks, chk-1, ex-2, chk-2, representations, chk-3, the bridge. 699 words, 4.7 minutes (cap 900 and 6).
- Mid (brief): orientation, ki-1, ki-2, st-1, ex-1, err-02001, err-02002, chk-1, chk-2, the bridge. 417 words, 2.8 minutes (cap 450 and 3).
- Refresher: ki-1, ki-2, err-BC-ERR-02001, err-BC-ERR-02002, err-BC-ERR-02003, err-BC-ERR-02004, ex-1.

## Sources

- BC-CON-02007; BC-SKL-02014, BC-SKL-02015, BC-SKL-02016, BC-SKL-02017, BC-SKL-02018; BC-EK-CHA-2D1, BC-EK-CHA-2D2; ced:62
- BC-QA-04002, BC-QA-02013, BC-QA-02009; BC-FRQ-2021-Q1-A, BC-FRQ-2022-Q4-A, BC-FRQ-2024-Q1-A, BC-FRQ-2025-Q3-A, BC-FRQ-2026-Q1-A
- BC-PT-99005, BC-PT-99006, BC-PT-99008; sg-25:11, sg-25:4; cr-22:14, cr-24:4; BC-ERR-99005, BC-ERR-99019, BC-ERR-99021
- BC-ERR-02001, BC-ERR-02002, BC-ERR-02003, BC-ERR-02004, BC-ERR-02024, BC-ERR-02031, BC-ERR-02032, BC-ERR-09023; BC-MIS-02001, BC-MIS-02003, BC-MIS-02004, BC-MIS-02008
- BC-PRQ-02004
- research/units/unit-02-differentiation-definition-properties.md#2.3 Estimating Derivatives of a Function at a Point
- research/question-analysis/question-archetypes.md#BC-QA-04002 Approximating a derivative from a table with units
- research/question-analysis/question-archetypes.md#BC-QA-02013 Derivative at a point produced with technology
- research/scoring/common-point-losses.md#Units points
- research/scoring/common-point-losses.md#Setup points
- research/scoring/common-point-losses.md#Answer points
- research/exam/exam-structure.md#Section and part layout
- [inferred] The "either" archetype takes I-A. Settled by one calculator status on BC-QA-04002.
- [inferred] ex-1 on BC-QA-04002 rather than the first-listed BC-QA-02013. Settled by a primary-archetype field on the concept.
- [inferred] st-2's rival, BC-ERR-02031, because BC-QA-02013 has no wrong_approaches or prohibited_shortcuts. Settled by filling those fields.
- [inferred] ex-1 tags no point type (Scoring). Settled by a shorter BC-PT-99005 reader line and BC-PT-99006 wording the style check accepts.
- [inferred] The illustrative curve in the representations figure and every non-text mode. Settled by an archetype isolating BC-SKL-02017 and by the modality A/B.

## Machine record

```json
{
 "id": "LSN-CON-02007",
 "kind": "concept",
 "target_id": "BC-CON-02007",
 "unit": "02",
 "skills": ["BC-SKL-02014", "BC-SKL-02015", "BC-SKL-02016", "BC-SKL-02017", "BC-SKL-02018"],
 "orientation": {
  "text": "A response estimates a derivative at a point from nearby values: the average rate over rows that bracket the point, with the difference, the quotient and compound units shown. From a graph it is the tangent's slope; from a calculator, a value with its setup named.",
  "sources": ["BC-CON-02007", "research/units/unit-02-differentiation-definition-properties.md#2.3 Estimating Derivatives of a Function at a Point"]
 },
 "key_ideas": [
  {
   "id": "ki-1",
   "ek_id": "BC-EK-CHA-2D1",
   "depth": "core",
   "text": "From a table (BC-EK-CHA-2D1, ced:62): the average rate over an interval that contains or abuts the point, difference and quotient both shown. From a graph: the slope of the tangent at the point, from two points on it. Units: the quantity's units per unit of input.",
   "notation": "approximately equal to",
   "quote": {"text": "The derivative at a point can be estimated from information given in tables or graphs.", "source": "ced:62"},
   "sources": ["BC-EK-CHA-2D1", "ced:62", "research/units/unit-02-differentiation-definition-properties.md#2.3 Estimating Derivatives of a Function at a Point"]
  },
  {
   "id": "ki-2",
   "ek_id": "BC-EK-CHA-2D2",
   "depth": "core",
   "text": "Technology gives the derivative of a supplied model at a point (BC-EK-CHA-2D2, ced:62). The written line names what was computed, such as \\(W'(2)\\), and the value is reported to three decimal places.",
   "notation": "approximately equal to",
   "quote": {"text": "Technology can be used to calculate or estimate the value of a derivative of a function at a point.", "source": "ced:62"},
   "sources": ["BC-EK-CHA-2D2", "ced:62", "BC-QA-02013"]
  }
 ],
 "strategy": [
  {
   "id": "st-1",
   "archetype_id": "BC-QA-04002",
   "cue": "A table of a contextual quantity; the stem asks to approximate a derivative at a tabulated input, with units.",
   "method": "First line: the two rows that bracket the point, differenced, over their inputs' difference.",
   "rival": "Rival: a pair of rows other than the bracketing pair (BC-ERR-02004).",
   "separating_feature": "The two rows sit on either side of the point.",
   "sources": ["BC-QA-04002"],
   "evidence_tag": "verified"
  },
  {
   "id": "st-2",
   "archetype_id": "BC-QA-02013",
   "cue": "A function model in a calculator part; the stem asks for the derivative at an input, with setup.",
   "method": "First line: the setup naming the quantity, such as \\(W'(2)\\), then the calculator value.",
   "rival": "Rival: a bare calculator number with no setup (BC-ERR-02031).",
   "separating_feature": "A formula and a calculator part, not a table.",
   "sources": ["BC-QA-02013", "BC-ERR-02031"],
   "evidence_tag": "verified"
  }
 ],
 "worked_examples": [
  {
   "id": "ex-1",
   "archetype_id": "BC-QA-04002",
   "bands": ["low", "mid"],
   "parameter_draw": {"times": [0, 4, 6, 10, 12], "readings": [86, 71, 50, 38, 25], "context": "oven", "trend": "decreasing"},
   "problem": {"text": "An oven is at \\(H(t)\\) degrees Fahrenheit at \\(t\\) minutes: \\(H(0)=86\\), \\(H(4)=71\\), \\(H(6)=50\\), \\(H(10)=38\\), \\(H(12)=25\\). Approximate \\(H'(6)\\) from the rows that bracket \\(t=6\\), with units.", "command_verb": "approximate"},
   "calculator_status": "no_calculator",
   "steps": [
    {"cue": "The point 6 is a row; its neighbours 4 and 10 bracket it.", "why": "Use \\(H(4)=71\\) and \\(H(10)=38\\)."},
    {"cue": "An estimate from data is an average rate.", "why": "Difference and quotient both go on the page.", "expr": "(38 - 71)/(10 - 4)", "relation": "new"},
    {"cue": "The stem asks for a value; no calculator.", "why": "\\(-\\frac{33}{6}=-\\frac{11}{2}\\).", "expr": "-11/2", "relation": "equivalent"},
    {"cue": "The stem says units.", "why": "Degrees Fahrenheit per minute."}
   ],
   "answer": {"form": "numeric", "expr": "-11/2"}
  },
  {
   "id": "ex-2",
   "archetype_id": "BC-QA-02013",
   "bands": ["low"],
   "parameter_draw": {"level": 24, "swing": 3, "scale": 4, "at": 2, "context": "traffic", "framing": "context"},
   "problem": {"text": "Cars on a highway number \\(W(t)=24+3\\sin(\\frac{t^2}{4})+\\ln(1+t)\\) hundred at \\(t\\) hours, \\(0\\le t\\le4\\). Using a calculator, find \\(W'(2)\\) to three decimal places, with units.", "command_verb": "find"},
   "calculator_status": "calculator",
   "steps": [
    {"cue": "The stem asks for \\(W'(2)\\) with a calculator: name it first.", "why": "The setup line says what is computed.", "expr": "24 + 3*sin(t**2/4) + log(1 + t)", "relation": "new"},
    {"cue": "The calculator differentiates the entered \\(W\\) numerically, in radian mode.", "why": "It evaluates \\(W'(t)=\\frac{3t}{2}\\cos(\\frac{t^2}{4})+\\frac{1}{1+t}\\).", "expr": "3*t/2*cos(t**2/4) + 1/(1 + t)", "relation": "differentiate", "variable": "t"},
    {"cue": "The stem says three decimal places.", "why": "\\(W'(2)\\approx1.954\\) hundred cars per hour.", "expr": "1.954", "relation": "evaluate", "subs": {"t": "2"}, "approx": true}
   ],
   "answer": {"form": "numeric", "expr": "1.954"}
  }
 ],
 "what_a_reader_scores": [
  {"example_id": "ex-1", "point_type_ids": [], "lines": []}
 ],
 "common_errors": [
  {
   "error_id": "BC-ERR-02001",
   "observed_behavior": "The response reports the change in the function values over the interval without dividing by the change in the inputs.",
   "scoring_consequence": "The answer point requires both a difference and a quotient using values from the table, so a difference alone does not earn it (sg-25:11).",
   "wrong_step": {"text": "\\(38-71=-33\\).", "expr": "38 - 71"},
   "right_step": {"text": "\\(\\frac{38-71}{10-4}\\).", "expr": "(38 - 71)/(10 - 4)"},
   "relation": "distinct",
   "possible_reason": {"misconception_id": "BC-MIS-02001", "text": "the division by the change in the input is omitted"},
   "sources": ["BC-ERR-02001", "BC-MIS-02001"]
  },
  {
   "error_id": "BC-ERR-02002",
   "observed_behavior": "The response writes the difference quotient correctly but stops before producing a number.",
   "scoring_consequence": "The quotient presented by itself is not sufficient for the answer point (sg-25:11).",
   "wrong_step": {"text": "\\(\\frac{38-71}{10-4}\\), and no number.", "expr": "(38 - 71)/(10 - 4)"},
   "right_step": {"text": "\\(-\\frac{11}{2}\\).", "expr": "-11/2"},
   "relation": "equivalent",
   "possible_reason": null,
   "sources": ["BC-ERR-02002"]
  },
  {
   "error_id": "BC-ERR-02003",
   "observed_behavior": "The response reports an estimated derivative with no units, or with the units of the modelled quantity rather than of its rate.",
   "scoring_consequence": "The units point is lost; it is earned for the correct compound units whether or not they are attached to a value, and an equivalent compound form is accepted (sg-25:11).",
   "wrong_step": {"text": "\\(-\\frac{11}{2}\\) degrees Fahrenheit.", "expr": "-11/2"},
   "right_step": {"text": "\\(-\\frac{11}{2}\\) degrees Fahrenheit per minute.", "expr": "(38 - 71)/(10 - 4)"},
   "relation": "equivalent",
   "possible_reason": {"misconception_id": "BC-MIS-02008", "text": "copies them from the table header"},
   "sources": ["BC-ERR-02003", "BC-MIS-02008"]
  },
  {
   "error_id": "BC-ERR-02004",
   "observed_behavior": "The response estimates the derivative from a pair of tabulated inputs other than the pair the question names or the pair that brackets the point.",
   "scoring_consequence": "The answer point is lost because the supporting work does not use the values the question specifies.",
   "wrong_step": {"text": "Rows 4 and 6: \\(\\frac{50-71}{6-4}=-\\frac{21}{2}\\).", "expr": "(50 - 71)/(6 - 4)"},
   "right_step": {"text": "Rows 4 and 10: \\(-\\frac{11}{2}\\).", "expr": "(38 - 71)/(10 - 4)"},
   "relation": "distinct",
   "possible_reason": {"misconception_id": "BC-MIS-02001", "text": "applied to the wrong pair of values"},
   "sources": ["BC-ERR-02004", "BC-MIS-02001"]
  }
 ],
 "representations": {
  "text": "From a graph: draw the tangent at the point, read two points on it, and take rise over run.",
  "figure": {"kind": "graph", "curves": [{"expr": "x**2/4 + 1", "domain": [-1, 5]}], "tangent": {"at": 2, "slope": 1}, "labels": [{"text": "(0, 0) and (4, 4) on the tangent: slope 4/4 = 1", "placement": "inside", "at": "beside the tangent"}]},
  "sources": ["BC-SKL-02017", "research/units/unit-02-differentiation-definition-properties.md#2.3 Estimating Derivatives of a Function at a Point"]
 },
 "prerequisite_bridges": [
  {"prq_id": "BC-PRQ-02004", "text": "The setup names the variable: \\(W'(2)\\) is \\(\\frac{dW}{dt}\\) at \\(t=2\\)."}
 ],
 "time": {"exam_part": "I-A", "budget_minutes": 2.14, "source": "research/exam/exam-structure.md#Section and part layout", "written_steps": {"ex-1": [2, 3, 4], "ex-2": [1, 3]}, "skipped_steps": {"ex-1": [1], "ex-2": [2]}},
 "checks": [
  {
   "id": "chk-1",
   "check_kind": "completion",
   "format": "short_answer",
   "bands": ["low", "mid"],
   "archetype_id": "BC-QA-04002",
   "parameter_draw": {"times": [0, 4, 6, 10, 12], "readings": [86, 71, 50, 38, 25], "context": "oven", "trend": "decreasing"},
   "completes": "ex-1",
   "stem": {"text": "The work reads \\(H'(6)\\approx\\frac{38-71}{10-4}\\). Give the value.", "command_verb": "give"},
   "key": {"form": "numeric", "expr": "-11/2"},
   "steps": [
    {"text": "\\(\\frac{38-71}{10-4}\\).", "expr": "(38 - 71)/(10 - 4)", "relation": "new"},
    {"text": "\\(-\\frac{11}{2}\\).", "expr": "-11/2", "relation": "equivalent"}
   ],
   "calculator_status": "no_calculator",
   "skills": ["BC-SKL-02014"]
  },
  {
   "id": "chk-2",
   "check_kind": "isomorph",
   "format": "short_answer",
   "bands": ["low", "mid"],
   "archetype_id": "BC-QA-04002",
   "parameter_draw": {"times": [1, 3, 4, 8, 9], "readings": [12, 20, 27, 44, 60], "context": "download", "trend": "increasing"},
   "stem": {"text": "\\(F(t)\\) megabytes have downloaded at \\(t\\) seconds: \\(F(1)=12\\), \\(F(3)=20\\), \\(F(4)=27\\), \\(F(8)=44\\), \\(F(9)=60\\). Approximate \\(F'(4)\\) from the rows that bracket \\(t=4\\).", "command_verb": "approximate"},
   "key": {"form": "numeric", "expr": "24/5"},
   "steps": [
    {"text": "\\(\\frac{44-20}{8-3}\\).", "expr": "(44 - 20)/(8 - 3)", "relation": "new"},
    {"text": "\\(\\frac{24}{5}\\) megabytes per second.", "expr": "24/5", "relation": "equivalent"}
   ],
   "calculator_status": "no_calculator",
   "skills": ["BC-SKL-02014", "BC-SKL-02016"]
  },
  {
   "id": "chk-3",
   "check_kind": "mcq",
   "format": "mcq",
   "bands": ["low"],
   "archetype_id": "BC-QA-04002",
   "parameter_draw": {"times": [0, 2, 5, 6, 10], "readings": [10, 14, 23, 35, 40], "context": "rainfall", "trend": "increasing"},
   "stem": {"text": "A barrel holds water \\(W(t)\\) centimeters deep at \\(t\\) hours: \\(W(0)=10\\), \\(W(2)=14\\), \\(W(5)=23\\), \\(W(6)=35\\), \\(W(10)=40\\). From the rows bracketing \\(t=5\\), \\(W'(5)\\) is approximately", "command_verb": "approximate"},
   "key": {"form": "numeric", "expr": "21/4"},
   "steps": [
    {"text": "\\(\\frac{35-14}{6-2}\\).", "expr": "(35 - 14)/(6 - 2)", "relation": "new"},
    {"text": "\\(\\frac{21}{4}\\).", "expr": "21/4", "relation": "equivalent"}
   ],
   "options": [
    {"id": "A", "is_key": false, "expr": "21", "error_path": "BC-ERR-02001", "derivation": "the difference 35 - 14 without the division"},
    {"id": "B", "is_key": false, "expr": "3", "error_path": "BC-ERR-02004", "derivation": "rows 2 and 5: (23 - 14)/3"},
    {"id": "C", "is_key": true, "expr": "21/4", "error_path": null},
    {"id": "D", "is_key": false, "expr": "12", "error_path": "BC-ERR-02004", "derivation": "rows 5 and 6: (35 - 23)/1"}
   ],
   "calculator_status": "no_calculator",
   "skills": ["BC-SKL-02014", "BC-SKL-02016"]
  }
 ],
 "delivery": [
  {"block": "orientation", "mode": "text", "reason": "rule 5: a statement of what a response shows", "sources": ["BC-CON-02007"]},
  {"block": "ki-1", "mode": "table", "reason": "rule 4: BC-SKL-02014 and BC-SKL-02016 list BC-REP-03 (unit README delivery map)", "sources": ["BC-SKL-02014", "BC-SKL-02016"],
   "spec": {"kind": "table", "representations": ["BC-REP-03"], "columns": ["t (minutes)", "H(t) (degrees Fahrenheit)"], "rows": [[0, 86], [4, 71], [6, 50], [10, 38], [12, 25]], "marked_rows": [2, 3, 4],
    "labels": [{"text": "point t = 6", "placement": "inside", "at": "row 3, right margin inside the frame"}, {"text": "bracketing rows t = 4 and t = 10", "placement": "inside", "at": "bracket joining rows 2 and 4"}, {"text": "(38 - 71)/(10 - 4) = -11/2 degrees Fahrenheit per minute", "placement": "inside", "at": "last line of the table frame"}]},
   "fallback": "the five rows as a text list with the point row and the bracketing rows named, followed by the quotient",
   "keyboard": "none needed; the table is read row by row by a screen reader, with the marked rows announced"},
  {"block": "ki-2", "mode": "text", "reason": "rule 5: BC-REP-09 and BC-REP-01 on BC-SKL-02018, neither figure-bearing", "sources": ["BC-SKL-02018"]},
  {"block": "ex-1", "mode": "step_reveal", "reason": "rule 1", "sources": []},
  {"block": "ex-2", "mode": "step_reveal", "reason": "rule 1", "sources": []},
  {"block": "err-BC-ERR-02001", "mode": "step_reveal", "reason": "rule 1", "sources": []},
  {"block": "err-BC-ERR-02002", "mode": "step_reveal", "reason": "rule 1", "sources": []},
  {"block": "err-BC-ERR-02003", "mode": "step_reveal", "reason": "rule 1", "sources": []},
  {"block": "err-BC-ERR-02004", "mode": "step_reveal", "reason": "rule 1", "sources": []},
  {"block": "representations", "mode": "figure", "reason": "rule 3: BC-SKL-02017 lists BC-REP-02; static, since the stem asks for one reading of a fixed graph", "sources": ["BC-SKL-02017"],
   "spec": {"kind": "graph", "representations": ["BC-REP-02"], "axes": {"x": [-1, 5], "y": [-1, 7]},
    "curves": [{"expr": "x**2/4 + 1", "domain": [-1, 5], "role": "illustrative"}, {"expr": "x", "domain": [-0.5, 4.5], "role": "tangent at x = 2"}],
    "points": [{"at": [2, 2], "label": {"text": "(2, 2)", "placement": "inside", "at": "left of the point"}}, {"at": [0, 0], "label": {"text": "(0, 0)", "placement": "inside", "at": "below right of the point"}}, {"at": [4, 4], "label": {"text": "(4, 4)", "placement": "inside", "at": "below right of the point"}}],
    "labels": [{"text": "tangent slope = (4 - 0)/(4 - 0) = 1", "placement": "inside", "at": "upper left corner"}]},
   "fallback": "the text: the tangent at (2, 2) passes through (0, 0) and (4, 4), so the estimated derivative is 1",
   "keyboard": "none needed; the figure is static and its text alternative reads the two points and the slope"}
 ],
 "refresher": ["ki-1", "ki-2", "err-BC-ERR-02001", "err-BC-ERR-02002", "err-BC-ERR-02003", "err-BC-ERR-02004", "ex-1"],
 "read_minutes": {"full": 4.7, "brief": 2.8},
 "word_count": {"full": 699, "brief": 417},
 "research_lines": [
  {"file": "research/units/unit-02-differentiation-definition-properties.md", "line": "Use the average rate of change over an interval from the table that contains or abuts the point, and present both the difference and the quotient."},
  {"file": "research/scoring/common-point-losses.md", "line": "Units are scored separately from the value"}
 ],
 "inferred": [
  {"claim": "BC-QA-04002 carries calculator status either, so the lesson takes Section I Part A by the template's rule.", "settles": "A single calculator status on the archetype, or the FRQ records' part assignments."},
  {"claim": "ex-1 is drawn from BC-QA-04002 rather than the first-listed BC-QA-02013, because the first four error blocks are table errors.", "settles": "A primary-archetype field on the concept record."},
  {"claim": "st-2's rival is BC-ERR-02031, since BC-QA-02013 has no wrong_approaches or prohibited_shortcuts.", "settles": "Those fields filled on BC-QA-02013."},
  {"claim": "ex-1 tags no point type: the BC-PT-99005 reader line would break the brief cap and the BC-PT-99006 line fails the style check.", "settles": "A shorter reader_checks form for BC-PT-99005 and BC-PT-99006 wording the style check accepts."},
  {"claim": "The curve in the representations figure is illustrative, since no archetype isolates BC-SKL-02017; the table, text and figure modes are unmeasured.", "settles": "An archetype for BC-SKL-02017, and the modality A/B in the build plan."}
 ],
 "sources": ["BC-CON-02007", "BC-SKL-02014", "BC-SKL-02015", "BC-SKL-02016", "BC-SKL-02017", "BC-SKL-02018", "BC-EK-CHA-2D1", "BC-EK-CHA-2D2", "ced:62", "BC-QA-04002", "BC-QA-02013", "BC-QA-02009", "BC-FRQ-2021-Q1-A", "BC-FRQ-2022-Q4-A", "BC-FRQ-2024-Q1-A", "BC-FRQ-2025-Q3-A", "BC-FRQ-2026-Q1-A", "BC-PT-99005", "BC-PT-99006", "BC-PT-99008", "sg-25:11", "sg-25:4", "cr-22:14", "cr-24:4", "BC-ERR-99005", "BC-ERR-99019", "BC-ERR-99021", "BC-ERR-02001", "BC-ERR-02002", "BC-ERR-02003", "BC-ERR-02004", "BC-ERR-02024", "BC-ERR-02031", "BC-ERR-02032", "BC-ERR-09023", "BC-MIS-02001", "BC-MIS-02003", "BC-MIS-02004", "BC-MIS-02008", "BC-PRQ-02004", "research/units/unit-02-differentiation-definition-properties.md#2.3 Estimating Derivatives of a Function at a Point", "research/scoring/common-point-losses.md#Units points", "research/scoring/common-point-losses.md#Setup points", "research/scoring/common-point-losses.md#Answer points", "research/exam/exam-structure.md#Section and part layout"]
}
```
