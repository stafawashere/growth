---
title: LSN-CON-08010 Area between two curves integrated in x
research_date: 2026-09-29
status: designed
purpose: Authoring spec for the concept lesson on BC-CON-08010, the area of a region between two curves as the integral of upper minus lower in x, built from authoring_bundle("BC-CON-08010") and the research files it cites, so an author fills plan 15's lesson record without making a teaching decision.
---

# LSN-CON-08010 Area between two curves integrated in x

Concept BC-CON-08010 (skills BC-SKL-08018, BC-SKL-08019, BC-SKL-08022), topic 8.4 of Unit 8, loaded by one archetype, BC-QA-08008 (family area-between-curves), which also loads the limits concept BC-CON-08011. BC-CON-08011 is its hard parent, so the lesson may take the limits as found (docs/lessons/unit-08/README.md, section 1).

## Orientation

Served text, from BC-CON-08010 `description_plain` and the topic's Assessment behaviour paragraph (research/units/unit-08-applications-integration.md#8.4 Finding the Area Between Curves Expressed as Functions of x): a response writes one definite integral of upper minus lower in x, antidifferentiates, and reports a nonnegative number. No count, no frequency.

## Key ideas

All three skills map to BC-EK-CHA-5A1 (ced:155), so one core block, both bands.

- ki-1 (core). Paraphrase of the Required mathematical knowledge paragraphs (Area between curves; Notation): with f at or above g on [a, b], the area is the integral of f minus g in x; the upper curve is named first, by the figure or by one interior input, and that fixes the order; the area is reported nonnegative, and a reversed difference asserted equal to the positive area loses the answer point (sg-23:17). Anchor quote from ced:155. Notation line from the concept record.

## Recognition

BC-QA-08008 (research/question-analysis/question-archetypes.md#BC-QA-08008 Area of a region between two curves in x): `typical_wording` "find the area of the shaded region enclosed by the graphs of the two functions"; `common_givens` a figure with a shaded region, one or both curve equations, sometimes the value of one definite integral; `asked_to_produce` an integrand, an antiderivative or a numerical value, the area. The signal is the word area beside two named graphs with one curve on top throughout. Shapes: an MCQ offering the reversed difference and the single function integral as distractors, and the opening part of the no calculator region question (BC-FRQ-2014-Q5-A, BC-FRQ-2022-Q5-A, BC-FRQ-2023-Q5-A).

What says "not this concept": boundaries given as x in terms of y, or a right boundary that stays one curve while the upper one changes (area in y, BC-CON-08012); curves that cross inside the interval (split region, BC-CON-08013); the word "volume" or "cross sections" (BC-CON-08014, BC-CON-08015).

## Method choice

One strategy block, both bands.

- st-1, BC-QA-08008. Cue from `asked_to_produce` and `common_givens`. Method, `expected_solution_path[0]`: decide which curve is upper, then write the integral of upper minus lower with its limits. Rival, `wrong_approaches`: reporting a negative value as an area (the reversed order, BC-ERR-08020). Separating feature: one interior input evaluated in both functions fixes the order before the integral is written. Both fields are present, so the block is not tagged inferred.

## Solution path

- ex-1, BC-QA-08008, both bands, no calculator. Draw from `parameter_spec`: left 2, width 3, bulge 1, slope -1, intercept 3, lift 1, limits intersections, presentation formula. So g(x) = 3 - x and f(x) = -x^2 + 6x - 7 meet at x = 2 and x = 5 and the area is bulge times width cubed over 6 = 9/2. No published BC-QA-08008 item carries this draw.
- Steps follow `expected_solution_path`: the upper curve (no value); the integral of f minus g with limits (new, tagged BC-PT-99059); the integrand collected (equivalent); the antiderivative evaluated at the limits (equivalent); the value (equivalent). A fluent solver writes steps 2, 4 and 5 and holds the interior test and the collection in the head [inferred].

## Scoring

BC-QA-08008 lists BC-PT-99059, 99003, 99004 and 99001. ex-1 tags BC-PT-99059 on the integral with limits, the part this concept owns; the reader line is `reader_checks(["BC-PT-99059"])` copied exactly. For the author: in 2023 the area part scored the integrand, the antiderivative and the answer separately, and a reversed difference asserted equal to the positive area lost the answer point (sg-23:16, sg-23:17; research/scoring/common-point-losses.md#Answer points). The equal sign rule applies (research/scoring/notation-requirements.md#The equal sign). The antiderivative and answer tags are not served: with them the brief band passes 450 words (see Sources, inferred).

## Traps

Six active errors meet the skills; the first four in the bundle's order are served (cap 4): BC-ERR-06018, BC-ERR-08020, BC-ERR-99006, BC-ERR-99011. BC-ERR-08021 and BC-ERR-99009 are left out by the cap. Low band all four; mid band the first two. All on ex-1's draw.

- err-BC-ERR-06018: with u = x - 2 the integrand is u(3 - u); the x limits 2 and 5 kept give -15/2 against 9/2 on 0 to 3. Possible reason, words from BC-MIS-06016.
- err-BC-ERR-08020: g minus f integrated, -9/2. Possible reason, words from BC-MIS-08011.
- err-BC-ERR-99006: the same integral written with no dx; the value is unchanged, so the relation is equivalent and the loss is in the reading of the setup. No possible reason line.
- err-BC-ERR-99011: the difference squared, 81/10. Possible reason, words from BC-MIS-99003.

## Representations

None as a separate block. The topic's Representations paragraph names the conversion of a shaded figure to an integral (BC-REP-02 to BC-REP-01), which the orientation and ki-1 figures carry.

## Prerequisite bridge

- BC-PRQ-06002, from its `description_plain` and `failure_signature`.
- BC-PRQ-06005, from its `description_plain` and `failure_signature`.

## Time

BC-QA-08008 is `either`; the design takes Section I Part A, 2.14 minutes per question (research/exam/exam-structure.md#Section and part layout) [inferred: an either archetype placed in I-A]. As a free response opening part it is three points of a 15.0 minute question, 5.0 minutes (docs/lessons/unit-08/README.md, section 5). The minutes go on the antiderivative evaluated at both limits; the upper curve and the collected integrand are held.

## Checks

- chk-1, completion of ex-1, both bands: evaluate the collected integral. Key 9/2.
- chk-2, isomorph, both bands. Draw: left -2, width 3, bulge 2, slope 1, intercept 2, lift 1, intersections, formula; f(x) = 6 - x - 2x^2, g(x) = x + 2 meeting at -2 and 1. Key 9.
- chk-3, MCQ, low band. Draw: left 1, width 2, bulge 2, slope 1, intercept 1, lift 2, intersections, formula; f(x) = -2x^2 + 9x - 5, g(x) = x + 1. Key the integral of f minus g on [1, 3], 8/3. Distractors: g minus f (BC-ERR-08020), the squared difference (BC-ERR-99011), the u form with the x limits kept (BC-ERR-06018).

## Delivery

- orientation: figure. Rule 4: BC-REP-02 on BC-SKL-08018 and BC-SKL-08019; the unit README delivery map puts a figure on the orientation.
- ki-1: figure. Rule 4, same field: the shaded region, both curves labelled, one vertical rectangle from lower to upper curve. Not promoted: BC-QA-08008 `difficulty_variables` are presence flags, not a varying quantity read from the figure (docs/lessons/unit-08/README.md, section 6) [inferred; settled by the modality A/B].
- ex-1: step_reveal. Rule 1.
- err-BC-ERR-06018, err-BC-ERR-08020, err-BC-ERR-99006, err-BC-ERR-99011: step_reveal. Rule 1.

## Band plan

- Low (full): orientation, ki-1, st-1, ex-1 with its reader line, the four error blocks, chk-1 to chk-3, both bridges. 573 words, 3.9 minutes (cap 900 and 6).
- Mid (brief): orientation, ki-1, st-1, ex-1 with its reader line, err-BC-ERR-06018, err-BC-ERR-08020, chk-1, chk-2, both bridges. 442 words, 3.0 minutes (cap 450 and 3).
- Refresher: ki-1, err-BC-ERR-06018, err-BC-ERR-08020, err-BC-ERR-99006, err-BC-ERR-99011, ex-1.

## Sources

- BC-CON-08010; BC-SKL-08018, BC-SKL-08019, BC-SKL-08022; BC-EK-CHA-5A1; ced:155
- BC-QA-08008; BC-PT-99059; sg-23:16, sg-23:17
- BC-ERR-06018, BC-ERR-08020, BC-ERR-99006, BC-ERR-99011; BC-MIS-06016, BC-MIS-08011, BC-MIS-99003
- BC-PRQ-06002, BC-PRQ-06005
- research/units/unit-08-applications-integration.md#8.4 Finding the Area Between Curves Expressed as Functions of x
- research/question-analysis/question-archetypes.md#BC-QA-08008 Area of a region between two curves in x
- research/scoring/common-point-losses.md#Answer points
- research/scoring/notation-requirements.md#The equal sign
- research/exam/exam-structure.md#Section and part layout
- [inferred] BC-QA-08008 is either; the lesson takes I-A. Settled by a ruling on which part an either archetype's budget comes from.
- [inferred] BC-PT-99003 and BC-PT-99004 are not tagged on ex-1 although its steps earn them: their reader lines push the brief band past 450 words. Settled by a word cap that exempts reader lines, or a shorter reader_checks form.
- [inferred] Which steps are held in the head. Settled by timing data per step from 10's fluency telemetry.
- [inferred] The orientation and ki-1 figures. Settled by the modality A/B.

## Machine record

```json
{
 "id": "LSN-CON-08010",
 "kind": "concept",
 "target_id": "BC-CON-08010",
 "unit": "08",
 "skills": ["BC-SKL-08018", "BC-SKL-08019", "BC-SKL-08022"],
 "orientation": {
  "text": "A response writes one definite integral of upper curve minus lower curve in x, with the region's limits, antidifferentiates, and reports a nonnegative area.",
  "sources": ["BC-CON-08010", "research/units/unit-08-applications-integration.md#8.4 Finding the Area Between Curves Expressed as Functions of x"]
 },
 "key_ideas": [
  {
   "id": "ki-1",
   "ek_id": "BC-EK-CHA-5A1",
   "depth": "core",
   "text": "With f at or above g on [a, b], the area between the graphs is the integral of f minus g in x. The upper curve, named from the figure or from one interior input, fixes the order of subtraction. The area is nonnegative; writing the reversed difference as equal to the positive area loses the answer point (sg-23:17).",
   "notation": "upper minus lower; dx",
   "quote": {"text": "Areas of regions in the plane can be calculated with definite integrals.", "source": "ced:155"},
   "sources": ["BC-EK-CHA-5A1", "ced:155", "sg-23:17", "research/units/unit-08-applications-integration.md#8.4 Finding the Area Between Curves Expressed as Functions of x"]
  }
 ],
 "strategy": [
  {
   "id": "st-1",
   "archetype_id": "BC-QA-08008",
   "cue": "The stem asks for the area of a region between two graphs, from the curve equations or a shaded figure.",
   "method": "First written line: the upper curve named, then the integral of upper minus lower with its limits.",
   "rival": "Rival: the reversed order, reported as a negative area (BC-ERR-08020).",
   "separating_feature": "One interior input in both functions fixes the order.",
   "sources": ["BC-QA-08008"],
   "evidence_tag": "verified"
  }
 ],
 "worked_examples": [
  {
   "id": "ex-1",
   "archetype_id": "BC-QA-08008",
   "bands": ["low", "mid"],
   "parameter_draw": {"left": 2, "width": 3, "bulge": 1, "slope": -1, "intercept": 3, "lift": 1, "presentation": "formula", "limits": "intersections"},
   "problem": {"text": "\\(f(x)=-x^2+6x-7\\) and \\(g(x)=3-x\\) meet at \\(x=2\\) and \\(x=5\\). Find the area of the region they enclose.", "command_verb": "find"},
   "calculator_status": "no_calculator",
   "steps": [
    {"cue": "Area between two graphs: which is upper?", "why": "At \\(x=3\\): \\(f=2\\), \\(g=0\\), so \\(f\\) is upper."},
    {"cue": "Upper minus lower, limits at the meeting points.", "why": "\\(f\\) stays upper on \\([2,5]\\), so one integral.", "expr": "Integral(-x**2 + 6*x - 7 - (3 - x), (x, 2, 5))", "relation": "new", "point_type_id": "BC-PT-99059"},
    {"cue": "Parentheses around \\(g\\), then collect.", "why": "\\(-(3-x)=x-3\\).", "expr": "Integral(-x**2 + 7*x - 10, (x, 2, 5))", "relation": "equivalent"},
    {"cue": "Antiderivative, upper limit minus lower limit.", "why": "\\(F(x)=-x^3/3+7x^2/2-10x\\).", "expr": "(-125/3 + 175/2 - 50) - (-8/3 + 14 - 20)", "relation": "equivalent"},
    {"cue": "The stem asks for an area.", "why": "Positive, so the order was right.", "expr": "9/2", "relation": "equivalent"}
   ],
   "answer": {"form": "numeric", "expr": "9/2"}
  }
 ],
 "what_a_reader_scores": [
  {"example_id": "ex-1", "point_type_ids": ["BC-PT-99059"], "lines": [{"point_type_id": "BC-PT-99059", "text": "Area integrand for a region between curves. Earned by: The difference of the two functions, in either order or inside an absolute value, placed in a definite integral (sg-23:16). Not earned by: An integrand with incorrect limits, which sg-23:16 states blocks the answer point; incorrect u-substitution limits, which sg-23:17 states also block it."}]}
 ],
 "common_errors": [
  {
   "error_id": "BC-ERR-06018",
   "observed_behavior": "The antiderivative is written in the substituted variable and the original x limits are substituted into it.",
   "scoring_consequence": "The response is not eligible for the answer point even when the numerical value is correct (sg-23:17, sg-23:16).",
   "wrong_step": {"text": "\\(u=x-2\\), limits 2 and 5 kept.", "expr": "Integral(u*(3 - u), (u, 2, 5))"},
   "right_step": {"text": "Limits become 0 and 3.", "expr": "Integral(u*(3 - u), (u, 0, 3))"},
   "relation": "distinct",
   "possible_reason": {"misconception_id": "BC-MIS-06016", "text": "limits of integration and differentials carry over unchanged"},
   "sources": ["BC-ERR-06018", "BC-MIS-06016"]
  },
  {
   "error_id": "BC-ERR-08020",
   "observed_behavior": "The integrand is the lower curve minus the upper curve, or the left curve minus the right curve.",
   "scoring_consequence": "The integrand point may survive, since either order earned it in 2023, but a negative value reported as an area loses the answer point (sg-23:16, sg-23:17).",
   "wrong_step": {"text": "\\(g-f\\): \\(-9/2\\).", "expr": "Integral(3 - x - (-x**2 + 6*x - 7), (x, 2, 5))"},
   "right_step": {"text": "\\(f-g\\): \\(9/2\\).", "expr": "Integral(-x**2 + 6*x - 7 - (3 - x), (x, 2, 5))"},
   "relation": "distinct",
   "possible_reason": {"misconception_id": "BC-MIS-08011", "text": "any sign problem can be repaired at the end"},
   "sources": ["BC-ERR-08020", "BC-MIS-08011"]
  },
  {
   "error_id": "BC-ERR-99006",
   "observed_behavior": "Responses present a definite integral with no differential, or with a differential in the wrong variable, producing a setup the reader cannot interpret.",
   "scoring_consequence": "The setup point is not earned when the resulting expression is ambiguous; in some parts later points in that part are also lost.",
   "wrong_step": {"text": "\\(\\int_2^5 (-x^2+7x-10)\\) with no \\(dx\\).", "expr": "Integral(-x**2 + 7*x - 10, (x, 2, 5))"},
   "right_step": {"text": "\\(\\int_2^5 (-x^2+7x-10)\\,dx\\).", "expr": "Integral(-x**2 + 7*x - 10, (x, 2, 5))"},
   "relation": "equivalent",
   "possible_reason": null,
   "sources": ["BC-ERR-99006"]
  },
  {
   "error_id": "BC-ERR-99011",
   "observed_behavior": "Responses square a difference of functions when an area was asked, insert pi where no revolution occurs, square each function separately instead of squaring their difference, or revolve about the wrong line.",
   "scoring_consequence": "The integrand point is not earned; where the form point is separate, an eligible form may still earn it.",
   "wrong_step": {"text": "Difference squared: \\(81/10\\).", "expr": "Integral((-x**2 + 7*x - 10)**2, (x, 2, 5))"},
   "right_step": {"text": "Difference itself: \\(9/2\\).", "expr": "Integral(-x**2 + 7*x - 10, (x, 2, 5))"},
   "relation": "distinct",
   "possible_reason": {"misconception_id": "BC-MIS-99003", "text": "squaring a difference of functions for an area"},
   "sources": ["BC-ERR-99011", "BC-MIS-99003"]
  }
 ],
 "representations": null,
 "prerequisite_bridges": [
  {"prq_id": "BC-PRQ-06002", "text": "Powers rewritten as exponents before the reverse power rule; otherwise the antiderivative stalls."},
  {"prq_id": "BC-PRQ-06005", "text": "\\(f(3)\\) is a value at one input; reading the wrong input, or \\(f'\\) for \\(f\\), names the wrong upper curve."}
 ],
 "time": {"exam_part": "I-A", "budget_minutes": 2.14, "source": "research/exam/exam-structure.md#Section and part layout", "written_steps": {"ex-1": [2, 4, 5]}, "skipped_steps": {"ex-1": [1, 3]}},
 "checks": [
  {
   "id": "chk-1",
   "check_kind": "completion",
   "format": "short_answer",
   "bands": ["low", "mid"],
   "archetype_id": "BC-QA-08008",
   "parameter_draw": {"left": 2, "width": 3, "bulge": 1, "slope": -1, "intercept": 3, "lift": 1, "presentation": "formula", "limits": "intersections"},
   "completes": "ex-1",
   "stem": {"text": "Evaluate the area \\(\\int_2^5 (-x^2+7x-10)\\,dx\\).", "command_verb": "evaluate"},
   "key": {"form": "numeric", "expr": "9/2"},
   "steps": [
    {"text": "The collected integral.", "expr": "Integral(-x**2 + 7*x - 10, (x, 2, 5))", "relation": "new"},
    {"text": "\\(F(5)-F(2)\\).", "expr": "9/2", "relation": "equivalent"}
   ],
   "calculator_status": "no_calculator",
   "skills": ["BC-SKL-08022"]
  },
  {
   "id": "chk-2",
   "check_kind": "isomorph",
   "format": "short_answer",
   "bands": ["low", "mid"],
   "archetype_id": "BC-QA-08008",
   "parameter_draw": {"left": -2, "width": 3, "bulge": 2, "slope": 1, "intercept": 2, "lift": 1, "presentation": "formula", "limits": "intersections"},
   "stem": {"text": "\\(f(x)=6-x-2x^2\\) and \\(g(x)=x+2\\) meet at \\(x=-2\\) and \\(x=1\\). Find the enclosed area.", "command_verb": "find"},
   "key": {"form": "numeric", "expr": "9"},
   "steps": [
    {"text": "\\(f\\) is upper: \\(f(0)=6\\), \\(g(0)=2\\).", "expr": "Integral(6 - x - 2*x**2 - (x + 2), (x, -2, 1))", "relation": "new", "point_type_id": "BC-PT-99059"},
    {"text": "Evaluated.", "expr": "9", "relation": "equivalent"}
   ],
   "calculator_status": "no_calculator",
   "skills": ["BC-SKL-08019"]
  },
  {
   "id": "chk-3",
   "check_kind": "mcq",
   "format": "mcq",
   "bands": ["low"],
   "archetype_id": "BC-QA-08008",
   "parameter_draw": {"left": 1, "width": 2, "bulge": 2, "slope": 1, "intercept": 1, "lift": 2, "presentation": "formula", "limits": "intersections"},
   "stem": {"text": "\\(f(x)=-2x^2+9x-5\\) and \\(g(x)=x+1\\) meet at \\(x=1\\) and \\(x=3\\). Which gives the enclosed area?", "command_verb": "identify"},
   "key": {"form": "numeric", "expr": "8/3"},
   "steps": [
    {"text": "\\(f\\) is upper on \\([1,3]\\).", "expr": "Integral(-2*x**2 + 8*x - 6, (x, 1, 3))", "relation": "new"},
    {"text": "Evaluated.", "expr": "8/3", "relation": "equivalent"}
   ],
   "options": [
    {"id": "A", "is_key": false, "expr": "Integral(2*x**2 - 8*x + 6, (x, 1, 3))", "error_path": "BC-ERR-08020", "derivation": "g minus f, value -8/3"},
    {"id": "B", "is_key": false, "expr": "Integral((-2*x**2 + 8*x - 6)**2, (x, 1, 3))", "error_path": "BC-ERR-99011", "derivation": "the difference squared, value 64/15"},
    {"id": "C", "is_key": true, "expr": "Integral(-2*x**2 + 8*x - 6, (x, 1, 3))", "error_path": null},
    {"id": "D", "is_key": false, "expr": "Integral(2*u*(2 - u), (u, 1, 3))", "error_path": "BC-ERR-06018", "derivation": "u = x - 1 with the x limits kept, value -4/3"}
   ],
   "calculator_status": "no_calculator",
   "skills": ["BC-SKL-08019"]
  }
 ],
 "delivery": [
  {"block": "orientation", "mode": "figure", "reason": "rule 4: BC-REP-02 on BC-SKL-08018 and BC-SKL-08019; unit README delivery map", "sources": ["BC-SKL-08018", "BC-SKL-08019"],
   "spec": {"kind": "graph", "representations": ["BC-REP-02"], "window": {"x": [1, 6], "y": [-3, 3]}, "curves": [{"expr": "-x**2 + 6*x - 7", "domain": [1, 6]}, {"expr": "3 - x", "domain": [1, 6]}], "shade": {"between": ["-x**2 + 6*x - 7", "3 - x"], "x": [2, 5]}, "labels": [{"text": "f, upper", "placement": "inside"}, {"text": "g, lower", "placement": "inside"}, {"text": "area = integral of f minus g", "placement": "inside"}]},
   "fallback": "the same shaded region static, with both labels and the area label", "keyboard": "no control; the figure description is reached with Tab"},
  {"block": "ki-1", "mode": "figure", "reason": "rule 4: BC-REP-02 on BC-SKL-08018 and BC-SKL-08019; not promoted, BC-QA-08008 difficulty_variables are presence flags", "sources": ["BC-SKL-08018", "BC-SKL-08019", "BC-QA-08008"],
   "spec": {"kind": "graph", "representations": ["BC-REP-02", "BC-REP-01"], "window": {"x": [1, 6], "y": [-3, 3]}, "curves": [{"expr": "-x**2 + 6*x - 7", "domain": [1, 6]}, {"expr": "3 - x", "domain": [1, 6]}], "rectangles": [{"x": 3, "from": "3 - x", "to": "-x**2 + 6*x - 7", "width": 0.2}], "labels": [{"text": "height f(x) - g(x)", "placement": "inside"}, {"text": "x = 2", "placement": "inside"}, {"text": "x = 5", "placement": "inside"}]},
   "fallback": "the static region with one vertical rectangle from g up to f at x = 3 and both limits marked", "keyboard": "no control; the figure description is reached with Tab"},
  {"block": "ex-1", "mode": "step_reveal", "reason": "rule 1", "sources": []},
  {"block": "err-BC-ERR-06018", "mode": "step_reveal", "reason": "rule 1", "sources": []},
  {"block": "err-BC-ERR-08020", "mode": "step_reveal", "reason": "rule 1", "sources": []},
  {"block": "err-BC-ERR-99006", "mode": "step_reveal", "reason": "rule 1", "sources": []},
  {"block": "err-BC-ERR-99011", "mode": "step_reveal", "reason": "rule 1", "sources": []}
 ],
 "refresher": ["ki-1", "err-BC-ERR-06018", "err-BC-ERR-08020", "err-BC-ERR-99006", "err-BC-ERR-99011", "ex-1"],
 "read_minutes": {"full": 3.9, "brief": 3.0},
 "word_count": {"full": 572, "brief": 441},
 "research_lines": [
  {"file": "research/units/unit-08-applications-integration.md", "line": "An area is reported as a nonnegative quantity"}
 ],
 "inferred": [
  {"claim": "BC-QA-08008 is an either archetype; the lesson takes Section I Part A and its 2.14 minute budget.", "settles": "A ruling on which exam part an either archetype's budget comes from."},
  {"claim": "BC-PT-99003 and BC-PT-99004 are earned on ex-1 steps 4 and 5 but not tagged, because their reader lines push the brief band past 450 words.", "settles": "A brief word cap that exempts reader lines, or a shorter reader_checks form."},
  {"claim": "A fluent solver holds the interior test and the collected integrand in the head.", "settles": "Timing data per step from 10's fluency telemetry."},
  {"claim": "The orientation and ki-1 are served as static figures rather than text.", "settles": "The modality A/B in the build plan: skip rate and time to first credited success by mode."}
 ],
 "sources": ["BC-CON-08010", "BC-SKL-08018", "BC-SKL-08019", "BC-SKL-08022", "BC-EK-CHA-5A1", "ced:155", "BC-QA-08008", "BC-PT-99059", "sg-23:16", "sg-23:17", "BC-ERR-06018", "BC-ERR-08020", "BC-ERR-99006", "BC-ERR-99011", "BC-MIS-06016", "BC-MIS-08011", "BC-MIS-99003", "BC-PRQ-06002", "BC-PRQ-06005", "research/units/unit-08-applications-integration.md#8.4 Finding the Area Between Curves Expressed as Functions of x", "research/question-analysis/question-archetypes.md#BC-QA-08008 Area of a region between two curves in x", "research/scoring/common-point-losses.md#Answer points", "research/scoring/notation-requirements.md#The equal sign", "research/exam/exam-structure.md#Section and part layout"]
}
```
