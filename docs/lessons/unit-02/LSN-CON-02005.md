---
title: LSN-CON-02005 The derivative at a point as the slope of the tangent line
research_date: 2026-09-29
status: designed
purpose: Authoring spec for the concept lesson on BC-CON-02005, the derivative at a point as the slope of the tangent line, built from authoring_bundle("BC-CON-02005") and the research files it cites, so an author fills plan 15's lesson record without making a teaching decision.
---

# LSN-CON-02005 The derivative at a point as the slope of the tangent line

Concept BC-CON-02005 (skills BC-SKL-02012, BC-SKL-02013), topic 2.2 of Unit 2, loaded by BC-QA-02011 (listed first) and BC-QA-02014. Its hard parent is BC-CON-02002; BC-CON-02007 and BC-CON-02009 build on it (unit README section 1).

## Orientation

Served text (42 words), from BC-CON-02005 `description_plain` and the topic's Assessment behaviour paragraph (research/units/unit-02-differentiation-definition-properties.md#2.2 Defining the Derivative of a Function and Using Derivative Notation): a response reads \(f'(a)\) as the slope of the line touching the curve at \((a,f(a))\) and writes that line from the slope and the point. No count, no frequency.

## Key ideas

Both skills map BC-EK-CHA-2C1 (ced:61), so one core block, both bands.

- ki-1 (core). The derivative at a point as the tangent slope, and the tangent line from the slope and the point of tangency, paraphrased from the topic's Tangent line paragraph; the two numbers from one input have separate roles (BC-MIS-02014's description names the swap). Anchor quote (22 words) from ced:61. Notation line: tangent line.

## Recognition

- BC-QA-02011 (family tangent-line-approximation, one FRQ part or MCQ, no calculator; research/question-analysis/question-archetypes.md#BC-QA-02011 Tangent line written at a point on a curve): `typical_wording` "Write an equation for the line tangent to the graph of the given function at the named point"; `common_givens` a function rule and a named point or input; `asked_to_produce` an equation of the tangent line. The signal is the word tangent with one point or input. Official examples BC-FRQ-2015-Q5-A and BC-MCQ-PE2012-019; the second loads the quotient rule as well (unit README section 3).
- BC-QA-02014 (family derivative-definition-limit): the rate at one named instant, whose value is the tangent slope there (BC-SKL-02012).

What says "not this concept": a notation conversion (BC-CON-02004); a slope read from data rather than a rule (BC-CON-02007); the line then used to approximate a value (Unit 4, BC-QA-04008). The LSN-DEC-02-02 selector is what the stem asks to produce.

## Method choice

One block per family: tangent-line-approximation (BC-QA-02011) and derivative-definition-limit (BC-QA-02014).

- st-1, BC-QA-02011. Cue from `asked_to_produce` and `common_givens`. Method, `expected_solution_path[0]`: differentiate the function. Rival, `wrong_approaches`: the function value used as the slope (BC-ERR-02027). Separating feature: the slope comes from \(f'\), the point from \(f\).
- st-2, BC-QA-02014. Method, `expected_solution_path[0]`: the average rate over a short interval starting at the instant. Rival, `wrong_approaches`: averaging over the whole interval from the start. Separating feature: one instant, whose rate is the tangent slope.

Both archetypes carry `asked_to_produce` and `common_givens`, so neither block is tagged inferred.

## Solution path

- ex-1, BC-QA-02011, both bands, no calculator. Draw: square \(-1\), linear 4, constant 2, at 3, given input, so \(f(x)=-x^2+4x+2\), slope \(-2\), height 5 (the spec's derived `slope` and `height`; its `wrong_slope`, \(f'(5)=-6\), is BC-ERR-02028's value). Steps follow `expected_solution_path`: differentiate (valued), evaluate the derivative at 3 (evaluate, tagged BC-PT-99082), evaluate the function at 3 (valued, new chain), point slope form (valued, tagged BC-PT-99082). A fluent solver writes all four; the height is computed on the page because the stem gives only the input.

## Scoring

BC-QA-02011 lists BC-PT-99005, BC-PT-99004 and BC-PT-99082. ex-1 tags BC-PT-99082 on the slope and on the line; the line is `reader_checks(["BC-PT-99082"])`, copied into the machine record. The archetype's `scoring_pattern` gives one point each for the slope, the point and the equation. BC-PT-99005 and BC-PT-99004 are not tagged: the example's work is the tangent line itself.

Point losses the scoring research names for this shape: a general derivative expression equated to a number (research/scoring/common-point-losses.md#Notation points, BC-ERR-99002); a "function equals constant" equation (research/scoring/notation-requirements.md#The equal sign; sg-22:6, sg-23:6). The line need not be solved for \(y\), and isolating \(y\) is where BC-ERR-04023's record places sign and parenthesis errors (crabbc-25:25).

## Traps

Three active errors meet the concept's skills, in the bundle's order. Low band all three, mid band the first two.

- err-BC-ERR-02027 (BC-MIS-02014, BC-MIS-02015). Wrong step on ex-1's draw: slope 5, \(y=5+5(x-3)\). Right: \(y=5-2(x-3)\). Distinct. Possible reason from BC-MIS-02014.
- err-BC-ERR-02028 (BC-MIS-02014, BC-MIS-02004). Wrong: \(f'(5)=-6\), \(y=5-6(x-3)\). Right: \(y=5-2(x-3)\). Distinct. Possible reason from BC-MIS-02014.
- err-BC-ERR-04023 (BC-MIS-04012, BC-MIS-99011). Wrong: \(y=-2+5(x-3)\), height and slope exchanged. Right: \(y=5-2(x-3)\). Distinct. Possible reason null: neither linked description names the exchange.

## Representations

None as a separate block. The topic's Representations paragraph names the conversion derivative value to a tangent slope on a graph (BC-REP-01 to BC-REP-02), and the orientation and ki-1 carry it as figures.

## Prerequisite bridge

- BC-PRQ-02003 (supporting parent of both skills), from `description_plain` and `failure_signature`: the point slope form, needed when a correct derivative value does not become a line.

## Time

BC-QA-02011 is `no_calculator` and its `multipart_structure` is one part of a multipart free response question, so the part is Section II Part B, 15.0 minutes per question (research/exam/exam-structure.md#Section and part layout); BC-FRQ-2015-Q5-A gives the part 2 points, 3.33 minutes of the 15.0 (unit README section 5). As an MCQ it is a Part A item. A fluent solver writes the slope, the point and the equation, and skips simplifying the line.

## Checks

- chk-1, completion of ex-1, both bands: slope \(-2\) and point \((3,5)\) are given. Key \(y=5-2(x-3)\), equal to ex-1's answer.
- chk-2, isomorph on BC-QA-02011, both bands: square 1, linear \(-2\), constant 4, at \(-1\), given input. Key \(y=7-4(x+1)\).
- chk-3, MCQ on BC-QA-02011, low band: square \(-2\), linear 1, constant 3, at 1, given point. Key \(y=2-3(x-1)\). Distractors: \(y=2+2(x-1)\) (BC-ERR-02027), \(y=2-7(x-1)\) (BC-ERR-02028, the spec's `wrong_slope`), \(y=-3+2(x-1)\) (BC-ERR-04023).

No draw equals a published BC-QA-02011 `parameter_draw` (content/items_gen_unit02, content/items_unit02_agent).

## Delivery

- orientation: figure. Rule 3; BC-SKL-02012 and BC-SKL-02013 list BC-REP-02, and the unit README's delivery map names a figure. Spec: the graph of ex-1's \(f\) with the tangent touching at \((3,5)\).
- ki-1: figure. Rule 3, the same trigger; no promotion to interactive, since BC-QA-02011 names no varying quantity read as a relationship. Spec: the same graph with the height 5 and the slope \(-2\) labelled in their places.
- ex-1: step_reveal. Rule 1.
- err-BC-ERR-02027, err-BC-ERR-02028, err-BC-ERR-04023: step_reveal. Rule 1.

Both figure choices are [inferred], settled by the modality A/B.

## Band plan

- Low (full): orientation, ki-1, st-1, st-2, ex-1 with its scoring line, the three error blocks, chk-1, chk-2, chk-3, the bridge. 555 words, 3.8 minutes (cap 900 and 6).
- Mid (brief): orientation, ki-1, st-1, ex-1 with its scoring line, err-02027, err-02028, chk-1, chk-2, the bridge. 445 words, 3.0 minutes (cap 450 and 3).
- Refresher: ki-1, err-BC-ERR-02027, err-BC-ERR-02028, err-BC-ERR-04023, ex-1.

## Sources

- BC-CON-02005; BC-SKL-02012, BC-SKL-02013; BC-EK-CHA-2C1; ced:61
- BC-QA-02011, BC-QA-02014, BC-QA-04008; BC-FRQ-2015-Q5-A, BC-MCQ-PE2012-019
- BC-PT-99082, BC-PT-99005, BC-PT-99004; samples-15-q5:1; sg-22:6, sg-23:6; crabbc-25:25; BC-ERR-99002
- BC-ERR-02027, BC-ERR-02028, BC-ERR-04023; BC-MIS-02014, BC-MIS-02015, BC-MIS-02004, BC-MIS-04012, BC-MIS-99011
- BC-PRQ-02003
- research/units/unit-02-differentiation-definition-properties.md#2.2 Defining the Derivative of a Function and Using Derivative Notation
- research/question-analysis/question-archetypes.md#BC-QA-02011 Tangent line written at a point on a curve
- research/scoring/common-point-losses.md#Notation points
- research/scoring/notation-requirements.md#The equal sign
- research/exam/exam-structure.md#Section and part layout
- [inferred] The figure deliveries for the orientation and ki-1. Settled by the modality A/B.

## Machine record

```json
{
 "id": "LSN-CON-02005",
 "kind": "concept",
 "target_id": "BC-CON-02005",
 "unit": "02",
 "skills": ["BC-SKL-02012", "BC-SKL-02013"],
 "orientation": {
  "text": "A response reads \\(f'(a)\\) as the slope of the line touching the curve at \\((a,f(a))\\), and writes that line from two numbers with different roles: the slope \\(f'(a)\\) and the height \\(f(a)\\). Stems ask for the tangent line at a named point.",
  "sources": ["BC-CON-02005", "research/units/unit-02-differentiation-definition-properties.md#2.2 Defining the Derivative of a Function and Using Derivative Notation"]
 },
 "key_ideas": [
  {
   "id": "ki-1",
   "ek_id": "BC-EK-CHA-2C1",
   "depth": "core",
   "text": "\\(f'(a)\\) is the slope of the tangent at \\((a,f(a))\\) (BC-EK-CHA-2C1, ced:61), and with that point it fixes the line: \\(y=f(a)+f'(a)(x-a)\\). One input gives two numbers: the height places the line, the slope tilts it.",
   "notation": "tangent line",
   "quote": {"text": "The derivative of a function at a point is the slope of the line tangent to a graph of the function at that point.", "source": "ced:61"},
   "sources": ["BC-EK-CHA-2C1", "ced:61", "BC-MIS-02014", "research/units/unit-02-differentiation-definition-properties.md#2.2 Defining the Derivative of a Function and Using Derivative Notation"]
  }
 ],
 "strategy": [
  {
   "id": "st-1",
   "archetype_id": "BC-QA-02011",
   "cue": "A function rule and a named point or input; the stem asks for the tangent line.",
   "method": "First line: differentiate the function.",
   "rival": "Rival: the function value used as the slope (BC-ERR-02027).",
   "separating_feature": "The slope comes from \\(f'\\), the point from \\(f\\).",
   "sources": ["BC-QA-02011"],
   "evidence_tag": "verified"
  },
  {
   "id": "st-2",
   "archetype_id": "BC-QA-02014",
   "cue": "A polynomial model and one named instant; the stem asks for the rate at that instant.",
   "method": "First line: the average rate over a short interval starting at the instant.",
   "rival": "Rival: averaging over the whole interval from the start.",
   "separating_feature": "One instant: its rate is the tangent slope there.",
   "sources": ["BC-QA-02014"],
   "evidence_tag": "verified"
  }
 ],
 "worked_examples": [
  {
   "id": "ex-1",
   "archetype_id": "BC-QA-02011",
   "bands": ["low", "mid"],
   "parameter_draw": {"square": -1, "linear": 4, "constant": 2, "at": 3, "given": "input"},
   "problem": {"text": "Let \\(f(x)=-x^2+4x+2\\). Write an equation for the line tangent to the graph of \\(f\\) at \\(x=3\\).", "command_verb": "write"},
   "calculator_status": "no_calculator",
   "steps": [
    {"cue": "The stem asks for a tangent line; its slope comes from \\(f'\\).", "why": "Differentiate first.", "expr": "-2*x + 4", "relation": "new"},
    {"cue": "The tangency is at \\(x=3\\).", "why": "The slope is \\(f'(3)=-2\\).", "expr": "-2", "relation": "evaluate", "subs": {"x": "3"}, "point_type_id": "BC-PT-99082"},
    {"cue": "The stem gives the input only, so the height is computed.", "why": "\\(f(3)=5\\): the point is \\((3,5)\\).", "expr": "5", "relation": "new"},
    {"cue": "Slope and point in hand: point slope form.", "why": "The slope multiplies \\(x-3\\); the height stands alone.", "expr": "y = 5 - 2*(x - 3)", "relation": "new", "point_type_id": "BC-PT-99082"}
   ],
   "answer": {"form": "symbolic", "expr": "y = 5 - 2*(x - 3)"}
  }
 ],
 "what_a_reader_scores": [
  {"example_id": "ex-1", "point_type_ids": ["BC-PT-99082"], "lines": [{"point_type_id": "BC-PT-99082", "text": "Slope and equation of a tangent line at a point on a curve. Earned by: Two separable pieces of work: the value of the derivative at the stated input, and an equation of the line through the point on the curve with that slope. samples-15-q5:1 awards one point for the slope and a second for the tangent line equation, so a correct slope earns its point even when no line is written. Not earned by: A line written through the point with an unstated or incorrect slope, or a slope reported with no equation when the part asks for an equation; the two points are awarded separately (samples-15-q5:1)."}]}
 ],
 "common_errors": [
  {
   "error_id": "BC-ERR-02027",
   "observed_behavior": "The response writes the tangent line using the value of the function at the point as its slope.",
   "scoring_consequence": "The slope point and the equation point are both lost.",
   "wrong_step": {"text": "Slope \\(f(3)=5\\): \\(y=5+5(x-3)\\).", "expr": "y = 5 + 5*(x - 3)"},
   "right_step": {"text": "Slope \\(f'(3)=-2\\): \\(y=5-2(x-3)\\).", "expr": "y = 5 - 2*(x - 3)"},
   "relation": "distinct",
   "possible_reason": {"misconception_id": "BC-MIS-02014", "text": "the height is used as a slope"},
   "sources": ["BC-ERR-02027", "BC-MIS-02014"]
  },
  {
   "error_id": "BC-ERR-02028",
   "observed_behavior": "The response differentiates correctly but substitutes an input other than the point of tangency.",
   "scoring_consequence": "The slope point is lost and the equation point with it.",
   "wrong_step": {"text": "\\(f'(5)=-6\\): \\(y=5-6(x-3)\\).", "expr": "y = 5 - 6*(x - 3)"},
   "right_step": {"text": "\\(f'(3)=-2\\): \\(y=5-2(x-3)\\).", "expr": "y = 5 - 2*(x - 3)"},
   "relation": "distinct",
   "possible_reason": {"misconception_id": "BC-MIS-02014", "text": "treats the two numbers computed at the point of tangency as playing the same role"},
   "sources": ["BC-ERR-02028", "BC-MIS-02014"]
  },
  {
   "error_id": "BC-ERR-04023",
   "observed_behavior": "The point-slope form is assembled incorrectly, so the coordinates appear where the slope belongs or the line does not pass through the point.",
   "scoring_consequence": "The approximation point is lost; the 2025 report records multiple sign and parenthesis errors arising while isolating the dependent variable, which was not required (crabbc-25:25).",
   "wrong_step": {"text": "\\(y=-2+5(x-3)\\): height and slope exchanged.", "expr": "y = -2 + 5*(x - 3)"},
   "right_step": {"text": "\\(y=5-2(x-3)\\).", "expr": "y = 5 - 2*(x - 3)"},
   "relation": "distinct",
   "possible_reason": null,
   "sources": ["BC-ERR-04023", "crabbc-25:25"]
  }
 ],
 "representations": null,
 "prerequisite_bridges": [
  {"prq_id": "BC-PRQ-02003", "text": "Through \\((a,b)\\) with slope \\(m\\): \\(y=b+m(x-a)\\). A correct slope with no line is this gap."}
 ],
 "time": {"exam_part": "II-B", "budget_minutes": 15.0, "source": "research/exam/exam-structure.md#Section and part layout", "written_steps": {"ex-1": [1, 2, 3, 4]}, "skipped_steps": {"ex-1": []}},
 "checks": [
  {
   "id": "chk-1",
   "check_kind": "completion",
   "format": "short_answer",
   "bands": ["low", "mid"],
   "archetype_id": "BC-QA-02011",
   "parameter_draw": {"square": -1, "linear": 4, "constant": 2, "at": 3, "given": "input"},
   "completes": "ex-1",
   "stem": {"text": "\\(f'(3)=-2\\) and \\(f(3)=5\\). Write the tangent line at \\(x=3\\).", "command_verb": "write"},
   "key": {"form": "symbolic", "expr": "y = 5 - 2*(x - 3)"},
   "steps": [
    {"text": "\\(y=5-2(x-3)\\).", "expr": "y = 5 - 2*(x - 3)", "relation": "new", "point_type_id": "BC-PT-99082"}
   ],
   "calculator_status": "no_calculator",
   "skills": ["BC-SKL-02013"]
  },
  {
   "id": "chk-2",
   "check_kind": "isomorph",
   "format": "short_answer",
   "bands": ["low", "mid"],
   "archetype_id": "BC-QA-02011",
   "parameter_draw": {"square": 1, "linear": -2, "constant": 4, "at": -1, "given": "input"},
   "stem": {"text": "Let \\(f(x)=x^2-2x+4\\). Write an equation for the line tangent to the graph of \\(f\\) at \\(x=-1\\).", "command_verb": "write"},
   "key": {"form": "symbolic", "expr": "y = 7 - 4*(x + 1)"},
   "steps": [
    {"text": "\\(f'(x)=2x-2\\).", "expr": "2*x - 2", "relation": "new"},
    {"text": "\\(f'(-1)=-4\\).", "expr": "-4", "relation": "evaluate", "subs": {"x": "-1"}, "point_type_id": "BC-PT-99082"},
    {"text": "\\(f(-1)=7\\).", "expr": "7", "relation": "new"},
    {"text": "\\(y=7-4(x+1)\\).", "expr": "y = 7 - 4*(x + 1)", "relation": "new", "point_type_id": "BC-PT-99082"}
   ],
   "calculator_status": "no_calculator",
   "skills": ["BC-SKL-02012", "BC-SKL-02013"]
  },
  {
   "id": "chk-3",
   "check_kind": "mcq",
   "format": "mcq",
   "bands": ["low"],
   "archetype_id": "BC-QA-02011",
   "parameter_draw": {"square": -2, "linear": 1, "constant": 3, "at": 1, "given": "point"},
   "stem": {"text": "Which is the line tangent to \\(y=-2x^2+x+3\\) at \\((1,2)\\)?", "command_verb": "choose"},
   "key": {"form": "symbolic", "expr": "y = 2 - 3*(x - 1)"},
   "steps": [
    {"text": "\\(y'=-4x+1\\).", "expr": "-4*x + 1", "relation": "new"},
    {"text": "At 1 the slope is \\(-3\\).", "expr": "-3", "relation": "evaluate", "subs": {"x": "1"}, "point_type_id": "BC-PT-99082"},
    {"text": "\\(y=2-3(x-1)\\).", "expr": "y = 2 - 3*(x - 1)", "relation": "new", "point_type_id": "BC-PT-99082"}
   ],
   "options": [
    {"id": "A", "is_key": false, "expr": "y = 2 + 2*(x - 1)", "error_path": "BC-ERR-02027", "derivation": "the height 2 used as the slope"},
    {"id": "B", "is_key": true, "expr": "y = 2 - 3*(x - 1)", "error_path": null},
    {"id": "C", "is_key": false, "expr": "y = 2 - 7*(x - 1)", "error_path": "BC-ERR-02028", "derivation": "the derivative evaluated at the height 2: -4(2) + 1"},
    {"id": "D", "is_key": false, "expr": "y = -3 + 2*(x - 1)", "error_path": "BC-ERR-04023", "derivation": "height and slope exchanged in point slope form"}
   ],
   "calculator_status": "no_calculator",
   "skills": ["BC-SKL-02013"]
  }
 ],
 "delivery": [
  {"block": "orientation", "mode": "figure", "reason": "rule 3: BC-SKL-02012 and BC-SKL-02013 list BC-REP-02 (unit README delivery map)", "sources": ["BC-SKL-02012"],
   "spec": {"kind": "graph", "representations": ["BC-REP-02"], "axes": {"x": [-1, 5], "y": [-4, 8]},
    "curves": [{"expr": "-x**2 + 4*x + 2", "domain": [-1, 5]}, {"expr": "5 - 2*(x - 3)", "domain": [1.5, 4.5], "role": "tangent"}],
    "points": [{"at": [3, 5], "label": {"text": "(3, 5)", "placement": "inside", "at": "just above the point"}}],
    "labels": [{"text": "y = f(x)", "placement": "inside", "at": "near the vertex of the curve"}, {"text": "tangent at x = 3", "placement": "inside", "at": "along the tangent, right of the point"}]},
   "fallback": "the text: the tangent to y = -x^2 + 4x + 2 touches the curve at (3, 5)",
   "keyboard": "none needed; the figure is static and its text alternative is read in place"},
  {"block": "ki-1", "mode": "figure", "reason": "rule 3: BC-REP-02 on BC-SKL-02012; no promotion, BC-QA-02011 names no varying quantity read as a relationship", "sources": ["BC-SKL-02012", "BC-QA-02011"],
   "spec": {"kind": "graph", "representations": ["BC-REP-02"], "axes": {"x": [-1, 5], "y": [-4, 8]},
    "curves": [{"expr": "-x**2 + 4*x + 2", "domain": [-1, 5]}, {"expr": "5 - 2*(x - 3)", "domain": [1.5, 4.5], "role": "tangent"}],
    "points": [{"at": [3, 5], "label": {"text": "(3, f(3)) = (3, 5)", "placement": "inside", "at": "just above the point"}}],
    "segments": [{"from": [3, 0], "to": [3, 5], "style": "dashed"}, {"from": [3, 5], "to": [4, 5], "style": "run"}, {"from": [4, 5], "to": [4, 3], "style": "rise"}],
    "labels": [{"text": "height f(3) = 5", "placement": "inside", "at": "beside the dashed vertical segment"}, {"text": "run 1, rise -2: slope f'(3) = -2", "placement": "inside", "at": "beside the slope triangle"}, {"text": "y = 5 - 2(x - 3)", "placement": "inside", "at": "along the tangent"}]},
   "fallback": "the text: height f(3) = 5 places the line; slope f'(3) = -2 tilts it; y = 5 - 2(x - 3)",
   "keyboard": "none needed; the figure is static and its text alternative reads the height, the slope and the line in order"},
  {"block": "ex-1", "mode": "step_reveal", "reason": "rule 1", "sources": []},
  {"block": "err-BC-ERR-02027", "mode": "step_reveal", "reason": "rule 1", "sources": []},
  {"block": "err-BC-ERR-02028", "mode": "step_reveal", "reason": "rule 1", "sources": []},
  {"block": "err-BC-ERR-04023", "mode": "step_reveal", "reason": "rule 1", "sources": []}
 ],
 "refresher": ["ki-1", "err-BC-ERR-02027", "err-BC-ERR-02028", "err-BC-ERR-04023", "ex-1"],
 "read_minutes": {"full": 3.8, "brief": 3.0},
 "word_count": {"full": 555, "brief": 445},
 "research_lines": [
  {"file": "research/units/unit-02-differentiation-definition-properties.md", "line": "The derivative of a function at a point is the slope of the line tangent to the graph at that point"},
  {"file": "research/scoring/notation-requirements.md", "line": "a response with an incorrect equation of the form \"function equals constant\" will not earn the point"}
 ],
 "inferred": [
  {"claim": "Static figures on the orientation and ki-1 serve better than text.", "settles": "The modality A/B in the build plan: skip rate and time to first credited success by mode."}
 ],
 "sources": ["BC-CON-02005", "BC-SKL-02012", "BC-SKL-02013", "BC-EK-CHA-2C1", "ced:61", "BC-QA-02011", "BC-QA-02014", "BC-QA-04008", "BC-FRQ-2015-Q5-A", "BC-MCQ-PE2012-019", "BC-PT-99082", "BC-PT-99005", "BC-PT-99004", "sg-22:6", "sg-23:6", "crabbc-25:25", "BC-ERR-99002", "BC-ERR-02027", "BC-ERR-02028", "BC-ERR-04023", "BC-MIS-02014", "BC-MIS-02015", "BC-MIS-02004", "BC-MIS-04012", "BC-MIS-99011", "BC-PRQ-02003", "research/units/unit-02-differentiation-definition-properties.md#2.2 Defining the Derivative of a Function and Using Derivative Notation", "research/scoring/common-point-losses.md#Notation points", "research/scoring/notation-requirements.md#The equal sign", "research/exam/exam-structure.md#Section and part layout"]
}
```
