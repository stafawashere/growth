---
title: LSN-CON-06009 Behaviour of an accumulation function read from the integrand
research_date: 2026-09-29
status: designed
purpose: Authoring spec for the concept lesson on BC-CON-06009, where g(x) = the integral of f from a to x rises, falls, turns and bends, read from the graph of f with reasons tied to f, built from authoring_bundle("BC-CON-06009") and the research files it cites, so an author fills plan 15's lesson record without making a teaching decision.
---

# LSN-CON-06009 Behaviour of an accumulation function read from the integrand

Concept BC-CON-06009 (skills BC-SKL-06022 to BC-SKL-06027), topic 6.5 of Unit 6, loaded by one archetype, BC-QA-06003 (family accumulation-function-analysis), which FRQ writers give a whole multipart question. Hard parents: BC-CON-06007 and BC-CON-06008 (docs/lessons/unit-06/README.md, section 1).

## Orientation

Served text, from BC-CON-06009 `description_plain` and the topic's Assessment behaviour paragraph (research/units/unit-06-integration-accumulation.md#6.5 Interpreting the Behavior of Accumulation Functions Involving Area): the drawn curve is f, not g; a response reads g's rises and turns from the sign of f and g's bends from the slope of f, and every reason names f. No count, no frequency.

## Key ideas

All six skills map to BC-EK-FUN-5A3 (ced:122): one core block, both bands.

- ki-1 (core). Paraphrase of the Required mathematical knowledge paragraphs "Reading g from f" and "Absolute extrema": g' = f, so the sign of f gives where g rises or falls and a sign change of f gives a relative extremum of g; g'' = f', so where f rises or falls gives the concavity of g and a turning point of f gives an inflection point of g; an absolute extremum compares g at every zero of f and both endpoints. No anchor quote, to keep the brief band under its cap. Notation line from the concept record.

## Recognition

BC-QA-06003 (research/question-analysis/question-archetypes.md#BC-QA-06003 Accumulation function analysed from the graph of the integrand): `typical_wording` "find all values of x at which the graph of g has a point of inflection and give a reason", "find the value of x at which g attains an absolute minimum on the closed interval and justify your answer"; `common_givens` a graph of f of segments and semicircles, an accumulation function g with a fixed lower limit, a closed interval; `asked_to_produce` the critical points, the inflection points with a reason tied to the graph of f, the absolute extremum with a justification. The signal: a picture labelled "graph of f" and questions about g. Shapes: MCQ (BC-MCQ-CED-007, BC-MCQ-PE2012-015) and the no-calculator FRQ (BC-FRQ-2024-Q4-B, BC-FRQ-2021-Q4-A, BC-FRQ-2019-Q3-C).

What says "not this concept": a request for a value of g (BC-CON-06007) or for g prime at a point (BC-CON-06008). What says "this one": increasing, relative maximum, concave, point of inflection, absolute minimum, each asked of g.

## Method choice

One strategy block, both bands.

- st-1, BC-QA-06003. Method: the archetype's `expected_solution_path[0]` is the value step taught in LSN-CON-06007, so the block names the path's next two entries, g' = f by the theorem, then sign changes of f for extrema and turning points of f for inflection points (library gap: the path puts the value step first for every ask). Rival from `wrong_approaches`: features read off the plotted f (BC-ERR-06008). Separating feature: the curve drawn is f, so its peaks are not g's peaks.

## Solution path

- ex-1, BC-QA-06003, both bands, no calculator. Draw from `parameter_spec`: heights [-2, 2, -1, 1], lower 0, circle below, half_point 3/2, letters fg, ask value. The constraints hold (heights[3] is 1, linear_total is 2). The spec's `ask` parameter offers only value and chain, so the draw fixes the graph and the problem asks a feature question on it [inferred; library gap, `parameter_spec.parameters.ask` has no feature value]. f is negative on (0, 1), positive on (1, 10/3), negative on (10/3, 5), positive on (5, 8), negative on (8, 12). No published BC-QA-06003 item carries this draw.
- Steps: g' = f named (no value, tagged BC-PT-99024); the zeros of f where it changes sign (new, tagged BC-PT-99013); the ones where f goes from positive to negative (new). A fluent solver writes g' = f, the sign change and the answer; the zero locations are read off the figure.

## Scoring

BC-QA-06003 lists BC-PT-99024 and BC-PT-99013 among its point types; ex-1's steps tag both, and their reader_checks lines are in the machine record. Answer and reason earn separate points; the reason must be tied to the graph of f, and a reason in terms of g alone earns the answer point only (BC-QA-06003 `scoring_pattern`, sg-25:17; research/scoring/justification-requirements.md#Reasons tied to the object the prompt names). A vague subject such as "the function" does not carry the reason point (same heading). An absolute extremum needs every critical input and both endpoints (research/scoring/justification-requirements.md#The candidates test, sg-25:19).

## Traps

Six active errors meet the skills; the first four in the bundle's order are served (all with linked BC-MIS at severity high): BC-ERR-06008, BC-ERR-06009, BC-ERR-06010, BC-ERR-06012. BC-ERR-99004 and BC-ERR-99030 are not served (cap 4). Mid band: the first two. All on ex-1's draw.

- err-BC-ERR-06008: g's maxima put at the peaks of the drawn f, {2, 6}, against {10/3, 8}. Possible reason, words from BC-MIS-05011.
- err-BC-ERR-06009: inflection points at the zeros of f, {1, 10/3, 5, 8}, against the turning points {2, 4, 6, 10}. Possible reason, words from BC-MIS-06008.
- err-BC-ERR-06010: the right set with a reason about g only; the sets are equivalent, the reason is not. Possible reason, words from BC-MIS-01010.
- err-BC-ERR-06012: candidates {1, 10/3, 5, 8} with the endpoints dropped, against {0, 1, 10/3, 5, 8, 12}. Possible reason, words from BC-MIS-99010.

## Representations

None as a separate block; ki-1's interactive carries the graph of f.

## Prerequisite bridge

- BC-PRQ-06007, from its `description_plain` and `failure_signature`.

## Time

BC-QA-06003 is `no_calculator`, one part of a multipart FRQ or a single MCQ; the FRQ shape is Section II Part B, 15.0 minutes per question (research/exam/exam-structure.md#Section and part layout), about 3.33 minutes per two-point part (docs/lessons/unit-06/README.md, section 5) [inferred]. The minutes go on the reason sentence naming f; the zeros are read, not computed.

## Checks

- chk-1, completion of ex-1, both bands: the sign changes of f are given; the student keeps the positive-to-negative ones. Key {10/3, 8}.
- chk-2, isomorph, both bands. Draw: heights [1, -2, 2, -1], lower 0, circle above. Key {2/3, 16/3}.
- chk-3, MCQ, low band, statement key on ex-1's graph: every inflection point of g with an accepted reason. Distractors: the zeros of f (BC-ERR-06009), the right points with a reason about g (BC-ERR-06010), "none, the drawn curve has no inflection point" (BC-ERR-06008).

## Delivery

- orientation: text. Rule 6; BC-REP-02 is served once, on ki-1.
- ki-1: interactive. Rule 4 promoted: BC-REP-02 on all six skills; BC-QA-06003 `difficulty_variables` "whether the question asks about g, g prime, or g double prime" and the stem asks for a reading of the relationship (docs/lessons/unit-06/README.md, section 6) [inferred; settled by the modality A/B].
- ex-1 and the four error blocks: step_reveal. Rule 1.

## Band plan

- Low (full): orientation, ki-1, st-1, ex-1 with its scoring lines, the four error blocks, chk-1 to chk-3, the bridge. 628 words, 4.2 minutes (cap 900 and 6).
- Mid (brief): orientation, ki-1, st-1, ex-1 with its scoring lines, err-BC-ERR-06008, err-BC-ERR-06009, chk-1, chk-2, the bridge. 450 words, 3.0 minutes (cap 450 and 3).
- Refresher: ki-1, the four error blocks, ex-1.

## Sources

- BC-CON-06009; BC-SKL-06022, BC-SKL-06023, BC-SKL-06024, BC-SKL-06025, BC-SKL-06026, BC-SKL-06027; BC-EK-FUN-5A3; ced:122
- BC-QA-06003; BC-PT-99024, BC-PT-99013; sg-25:17, sg-25:19
- BC-ERR-06008, BC-ERR-06009, BC-ERR-06010, BC-ERR-06012; BC-MIS-05011, BC-MIS-06008, BC-MIS-01010, BC-MIS-99010
- BC-PRQ-06007
- research/units/unit-06-integration-accumulation.md#6.5 Interpreting the Behavior of Accumulation Functions Involving Area
- research/question-analysis/question-archetypes.md#BC-QA-06003 Accumulation function analysed from the graph of the integrand
- research/scoring/justification-requirements.md#Reasons tied to the object the prompt names
- research/scoring/justification-requirements.md#The candidates test
- research/exam/exam-structure.md#Section and part layout
- [inferred] A feature question posed on a value-ask draw. Settled by a feature value for `ask` in BC-QA-06003's parameter_spec.
- [inferred] The 3.33 minute share per part. Settled by timing data per part.
- [inferred] ki-1 as an interactive. Settled by the modality A/B.

## Machine record

```json
{
 "id": "LSN-CON-06009",
 "kind": "concept",
 "target_id": "BC-CON-06009",
 "unit": "06",
 "skills": ["BC-SKL-06022", "BC-SKL-06023", "BC-SKL-06024", "BC-SKL-06025", "BC-SKL-06026", "BC-SKL-06027"],
 "orientation": {
  "text": "The drawn curve is f. g rises and turns with the sign of f, bends with the slope of f; every reason names f.",
  "sources": ["BC-CON-06009", "research/units/unit-06-integration-accumulation.md#6.5 Interpreting the Behavior of Accumulation Functions Involving Area"]
 },
 "key_ideas": [
  {
   "id": "ki-1",
   "ek_id": "BC-EK-FUN-5A3",
   "depth": "core",
   "text": "g' = f: f positive, g rises; f changes sign, g has an extremum. g'' = f': f rising, g concave up; f turns, g inflects. Absolute: compare every zero of f and both endpoints.",
   "notation": "g', g'' in terms of f, f'",
   "quote": null,
   "sources": ["BC-EK-FUN-5A3", "ced:122", "research/units/unit-06-integration-accumulation.md#6.5 Interpreting the Behavior of Accumulation Functions Involving Area"]
  }
 ],
 "strategy": [
  {
   "id": "st-1",
   "archetype_id": "BC-QA-06003",
   "cue": "Graph of f; features of g asked, with a reason.",
   "method": "First line: g' = f. Sign changes of f give extrema; turns of f give inflection.",
   "rival": "Rival: features read off the plotted f (BC-ERR-06008).",
   "separating_feature": "The drawn peaks belong to f, not g.",
   "sources": ["BC-QA-06003"],
   "evidence_tag": "verified"
  }
 ],
 "worked_examples": [
  {
   "id": "ex-1",
   "archetype_id": "BC-QA-06003",
   "bands": ["low", "mid"],
   "parameter_draw": {"heights": [-2, 2, -1, 1], "lower": 0, "circle": "below", "half_point": "3/2", "letters": "fg", "ask": "value"},
   "problem": {"text": "f: segments through (0, -2), (2, 2), (4, -1), (6, 1), (8, 0), then a radius 2 semicircle below. g(x) = integral of f from 0 to x. Find each relative maximum of g.", "command_verb": "find"},
   "calculator_status": "no_calculator",
   "steps": [
    {"cue": "Features of g asked.", "why": "g' = f by the theorem.", "point_type_id": "BC-PT-99024"},
    {"cue": "g' = 0 where f crosses the axis.", "why": "Read off the graph.", "expr": "FiniteSet(1, 10/3, 5, 8)", "relation": "new", "point_type_id": "BC-PT-99013"},
    {"cue": "Maximum: g' from positive to negative.", "why": "Reason: f changes from positive to negative.", "expr": "FiniteSet(10/3, 8)", "relation": "new"}
   ],
   "answer": {"form": "symbolic", "expr": "FiniteSet(10/3, 8)"}
  }
 ],
 "what_a_reader_scores": [
  {"example_id": "ex-1", "point_type_ids": ["BC-PT-99024", "BC-PT-99013"], "lines": [
   {"point_type_id": "BC-PT-99024", "text": "Derivative of an accumulation function by the Fundamental Theorem. Earned by: Writing the derivative of the accumulation function as the integrand evaluated at the variable, in general or at the requested value (sg-25:16, sg-24:13). Not earned by: Differencing the integrand at the two limits, which sg-25:16 states earns the answer point but not this one."},
   {"point_type_id": "BC-PT-99013", "text": "Considers the derivative set equal to zero. Earned by: Presenting the equation derivative equals zero, or an equivalent equation, or discussing the sign change of the derivative, or using the phrase critical points of the function (sg-25:5, sg-26:17). Not earned by: Presenting only the solved critical value, which sg-25:5, sg-25:9, sg-26:17 and sg-25:19 all state is not sufficient."}
  ]}
 ],
 "common_errors": [
  {
   "error_id": "BC-ERR-06008",
   "observed_behavior": "Extrema or inflection points of g are read directly off the visible extrema and inflection points of the plotted curve.",
   "scoring_consequence": "Both the answer and the reason points of the part are lost, and any extra declared input costs both points (sg-25:17).",
   "wrong_step": {"text": "2 and 6.", "expr": "FiniteSet(2, 6)"},
   "right_step": {"text": "10/3 and 8.", "expr": "FiniteSet(10/3, 8)"},
   "relation": "distinct",
   "possible_reason": {"misconception_id": "BC-MIS-05011", "text": "answers questions about the function by reading features of whatever curve is drawn"},
   "sources": ["BC-ERR-06008", "BC-MIS-05011"]
  },
  {
   "error_id": "BC-ERR-06009",
   "observed_behavior": "The response reports inflection points of g at the zeros of f rather than at the turning points of f.",
   "scoring_consequence": "The answer point is not earned, and an extra declared input forfeits the reason point as well (sg-25:17).",
   "wrong_step": {"text": "Zeros of f.", "expr": "FiniteSet(1, 10/3, 5, 8)"},
   "right_step": {"text": "Turning points of f.", "expr": "FiniteSet(2, 4, 6, 10)"},
   "relation": "distinct",
   "possible_reason": {"misconception_id": "BC-MIS-06008", "text": "uses the zeros of f for every feature of g"},
   "sources": ["BC-ERR-06009", "BC-MIS-06008"]
  },
  {
   "error_id": "BC-ERR-06010",
   "observed_behavior": "The response says that g has an inflection point because g changes concavity, without tying the claim to the given graph of f.",
   "scoring_consequence": "The answer point is earned but the reason point is not, because the reason must be tied to the given graph of f (sg-25:17).",
   "wrong_step": {"text": "2, 4, 6, 10: g changes concavity.", "expr": "FiniteSet(2, 4, 6, 10)"},
   "right_step": {"text": "2, 4, 6, 10: f changes between increasing and decreasing.", "expr": "FiniteSet(10, 6, 4, 2)"},
   "relation": "equivalent",
   "possible_reason": {"misconception_id": "BC-MIS-01010", "text": "treats naming the definition or the theorem as the argument"},
   "sources": ["BC-ERR-06010", "BC-MIS-01010"]
  },
  {
   "error_id": "BC-ERR-06012",
   "observed_behavior": "A candidates table omits an endpoint or a critical input, or includes an input that is neither.",
   "scoring_consequence": "The justification point requires evaluations or reasoning at every critical input and both endpoints and no others (sg-25:19).",
   "wrong_step": {"text": "Endpoints dropped.", "expr": "FiniteSet(1, 10/3, 5, 8)"},
   "right_step": {"text": "With 0 and 12.", "expr": "FiniteSet(0, 1, 10/3, 5, 8, 12)"},
   "relation": "distinct",
   "possible_reason": {"misconception_id": "BC-MIS-99010", "text": "endpoints and other critical points are never compared"},
   "sources": ["BC-ERR-06012", "BC-MIS-99010"]
  }
 ],
 "representations": null,
 "prerequisite_bridges": [
  {"prq_id": "BC-PRQ-06007", "text": "A semicircle is half a circle; a trapezoid is not a rectangle."}
 ],
 "time": {"exam_part": "II-B", "budget_minutes": 15.0, "source": "research/exam/exam-structure.md#Section and part layout", "written_steps": {"ex-1": [1, 3]}, "skipped_steps": {"ex-1": [2]}},
 "checks": [
  {
   "id": "chk-1",
   "check_kind": "completion",
   "format": "short_answer",
   "bands": ["low", "mid"],
   "archetype_id": "BC-QA-06003",
   "parameter_draw": {"heights": [-2, 2, -1, 1], "lower": 0, "circle": "below", "half_point": "3/2", "letters": "fg", "ask": "value"},
   "completes": "ex-1",
   "stem": {"text": "f changes sign at 1, 10/3, 5, 8. g's relative maxima?", "command_verb": "find"},
   "key": {"form": "symbolic", "expr": "FiniteSet(10/3, 8)"},
   "steps": [
    {"text": "Sign changes of f.", "expr": "FiniteSet(1, 10/3, 5, 8)", "relation": "new"},
    {"text": "Positive to negative.", "expr": "FiniteSet(10/3, 8)", "relation": "new"}
   ],
   "calculator_status": "no_calculator",
   "skills": ["BC-SKL-06023"]
  },
  {
   "id": "chk-2",
   "check_kind": "isomorph",
   "format": "short_answer",
   "bands": ["low", "mid"],
   "archetype_id": "BC-QA-06003",
   "parameter_draw": {"heights": [1, -2, 2, -1], "lower": 0, "circle": "above", "half_point": "3/2", "letters": "fg", "ask": "value"},
   "stem": {"text": "As ex-1 with vertices (0, 1), (2, -2), (4, 2), (6, -1), (8, 0), semicircle above. Find each relative maximum of g.", "command_verb": "find"},
   "key": {"form": "symbolic", "expr": "FiniteSet(2/3, 16/3)"},
   "steps": [
    {"text": "Sign changes of f.", "expr": "FiniteSet(2/3, 3, 16/3, 8)", "relation": "new"},
    {"text": "Positive to negative.", "expr": "FiniteSet(2/3, 16/3)", "relation": "new"}
   ],
   "calculator_status": "no_calculator",
   "skills": ["BC-SKL-06023"]
  },
  {
   "id": "chk-3",
   "check_kind": "mcq",
   "format": "mcq",
   "bands": ["low"],
   "archetype_id": "BC-QA-06003",
   "parameter_draw": {"heights": [-2, 2, -1, 1], "lower": 0, "circle": "below", "half_point": "3/2", "letters": "fg", "ask": "value"},
   "stem": {"text": "Same f as ex-1. Which gives every inflection point of g on (0, 12) with a reason a reader accepts?", "command_verb": "identify"},
   "key": {"form": "statement", "expr": "FiniteSet(2, 4, 6, 10)"},
   "steps": [],
   "options": [
    {"id": "A", "is_key": false, "label": "1, 10/3, 5, 8: f changes sign there.", "error_path": "BC-ERR-06009", "derivation": "inflection points placed at the zeros of f"},
    {"id": "B", "is_key": true, "label": "2, 4, 6, 10: f changes between increasing and decreasing there.", "error_path": null},
    {"id": "C", "is_key": false, "label": "2, 4, 6, 10: g changes concavity there.", "error_path": "BC-ERR-06010", "derivation": "the right inputs with a reason not tied to the graph of f"},
    {"id": "D", "is_key": false, "label": "None: the drawn curve has no inflection point.", "error_path": "BC-ERR-06008", "derivation": "inflection points of g read off the plotted curve"}
   ],
   "calculator_status": "no_calculator",
   "skills": ["BC-SKL-06024"]
  }
 ],
 "delivery": [
  {"block": "orientation", "mode": "text", "reason": "rule 6: a statement of what a response shows; BC-REP-02 is served on ki-1", "sources": ["BC-SKL-06022"]},
  {"block": "ki-1", "mode": "interactive", "reason": "rule 4 promoted: BC-REP-02 on all six skills; BC-QA-06003 difficulty_variables name g, g prime or g double prime and the stem asks for a reading of the relationship", "sources": ["BC-SKL-06022", "BC-SKL-06024", "BC-QA-06003"],
   "spec": {"kind": "graph", "representations": ["BC-REP-02"], "window": {"x": [0, 12], "y": [-3, 3]},
    "curves": [{"piecewise_linear": [[0, -2], [2, 2], [4, -1], [6, 1], [8, 0]]}, {"semicircle": {"centre": [10, 0], "radius": 2, "side": "below"}}],
    "controls": [{"type": "draggable_point", "constrained_to": "curve", "range": [0, 12], "start": 3, "name": "input x"}],
    "drawn": ["the sign of f at x", "whether f is rising or falling at x"],
    "labels": [{"text": "graph of f", "placement": "inside"}, {"text": "f > 0: g increasing", "placement": "inside"}, {"text": "f rising: g concave up", "placement": "inside"}],
    "question": "Where the point crosses the axis going down, what does g do? Where the curve turns, what does g do?"},
   "fallback": "a static graph of f with the sign intervals shaded and the turning points 2, 4, 6, 10 marked, each label inside the figure",
   "keyboard": "Tab focuses the point; left and right arrow keys move it by 1/3 along the curve; Enter reads out the sign and the slope of f"},
  {"block": "ex-1", "mode": "step_reveal", "reason": "rule 1", "sources": []},
  {"block": "err-BC-ERR-06008", "mode": "step_reveal", "reason": "rule 1", "sources": []},
  {"block": "err-BC-ERR-06009", "mode": "step_reveal", "reason": "rule 1", "sources": []},
  {"block": "err-BC-ERR-06010", "mode": "step_reveal", "reason": "rule 1", "sources": []},
  {"block": "err-BC-ERR-06012", "mode": "step_reveal", "reason": "rule 1", "sources": []}
 ],
 "refresher": ["ki-1", "err-BC-ERR-06008", "err-BC-ERR-06009", "err-BC-ERR-06010", "err-BC-ERR-06012", "ex-1"],
 "read_minutes": {"full": 4.2, "brief": 3.0},
 "word_count": {"full": 628, "brief": 450},
 "research_lines": [
  {"file": "research/scoring/justification-requirements.md", "line": "Where a question gives the graph of a derivative and asks about the original function, the reason point is earned only by reasoning about the graphed object."}
 ],
 "inferred": [
  {"claim": "ex-1 and the checks pose feature questions (extrema, inflection) on draws whose ask parameter reads value, because BC-QA-06003 parameter_spec offers only value and chain asks.", "settles": "A feature value for the ask parameter in BC-QA-06003's parameter_spec."},
  {"claim": "The method line names expected_solution_path entries two and three, since entry one is the value step.", "settles": "An expected_solution_path per ask on BC-QA-06003."},
  {"claim": "A two-point feature part takes about 3.33 of the 15.0 Section II minutes.", "settles": "Timing data per part once the fluency telemetry exists."},
  {"claim": "ki-1 is served as an interactive draggable input rather than a static figure.", "settles": "The modality A/B in the build plan: skip rate and time to first credited success by mode."}
 ],
 "sources": ["BC-CON-06009", "BC-SKL-06022", "BC-SKL-06023", "BC-SKL-06024", "BC-SKL-06025", "BC-SKL-06026", "BC-SKL-06027", "BC-EK-FUN-5A3", "ced:122", "BC-QA-06003", "BC-PT-99024", "BC-PT-99013", "sg-25:17", "sg-25:19", "BC-ERR-06008", "BC-ERR-06009", "BC-ERR-06010", "BC-ERR-06012", "BC-MIS-05011", "BC-MIS-06008", "BC-MIS-01010", "BC-MIS-99010", "BC-PRQ-06007", "research/units/unit-06-integration-accumulation.md#6.5 Interpreting the Behavior of Accumulation Functions Involving Area", "research/question-analysis/question-archetypes.md#BC-QA-06003 Accumulation function analysed from the graph of the integrand", "research/scoring/justification-requirements.md#Reasons tied to the object the prompt names", "research/exam/exam-structure.md#Section and part layout"]
}
```
