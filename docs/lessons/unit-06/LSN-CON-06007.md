---
title: LSN-CON-06007 Accumulation function defined by a definite integral
research_date: 2026-09-29
status: designed
purpose: Authoring spec for the concept lesson on BC-CON-06007, the accumulation function g(x) as the definite integral of f from a fixed input to x, evaluated from the graph of f, built from authoring_bundle("BC-CON-06007") and the research files it cites, so an author fills plan 15's lesson record without making a teaching decision.
---

# LSN-CON-06007 Accumulation function defined by a definite integral

Concept BC-CON-06007 (skills BC-SKL-06017, BC-SKL-06020), topic 6.4 of Unit 6, loaded by three archetypes: BC-QA-06003 (primary, family accumulation-function-analysis), BC-QA-06004 (definite-integral-from-graph) and BC-QA-06012 (ftc-differentiation). BC-SKL-06028 (BC-CON-06010, signed area by geometry) is a hard parent of BC-SKL-06020, so the lesson assumes signed area by geometry (docs/lessons/unit-06/README.md, section 1). Every skill in the concept list names BC-CON-06007 as its own concept (plan 15 Q19, closed for Unit 6 in the README).

## Orientation

Served text, from BC-CON-06007 `description_plain` and the topic's Assessment behaviour paragraph (research/units/unit-06-integration-accumulation.md#6.4 The Fundamental Theorem of Calculus and Accumulation Functions): a response treats g(x) as a number that depends on the upper limit, finds it as signed area from the fixed lower limit, and keeps t inside the integral. No count, no frequency.

## Key ideas

BC-SKL-06017 maps to BC-EK-FUN-5A1; BC-SKL-06020 maps to BC-EK-FUN-5A1 and BC-EK-FUN-5A3. Two blocks: ki-1 core, ki-2 extended (low band), since BC-EK-FUN-5A3 is the core idea of LSN-CON-06009.

- ki-1 (core, BC-EK-FUN-5A1, ced:121). Paraphrase of the Required mathematical knowledge paragraphs "Accumulation function" and "Notation": the integral of f from a fixed a to x is a new function of x; t is bound and x sits only in the upper limit. Anchor quote from ced:121: "The definite integral can be used to define new functions." Notation line from the concept record.
- ki-2 (extended, BC-EK-FUN-5A3, ced:122). Paraphrase of the Representations paragraph's conversion "graph of the integrand to values of the accumulation function": g at an input is the signed area from a to that input, pieces below the axis negative, and a reversed pair of limits changes the sign. The EK text on ced:122 is cited for the representations claim; no quote.

## Recognition

BC-QA-06003 (research/question-analysis/question-archetypes.md#BC-QA-06003 Accumulation function analysed from the graph of the integrand): `typical_wording` "let g be the function defined by the integral of f from a fixed input to x"; `common_givens` a graph of f of segments and semicircles, an accumulation function g with a fixed lower limit; `asked_to_produce` "the values of g at stated inputs". The signal: a letter defined by an integral whose upper limit is x, and a picture of f. Shapes: the no-calculator graph FRQ (BC-FRQ-2024-Q4-B, BC-FRQ-2019-Q3-C) and MCQ items (BC-MCQ-CED-007).

BC-QA-06004 (research/question-analysis/question-archetypes.md#BC-QA-06004 Definite integral evaluated from a graph by geometry): numerical limits on the same kind of picture; the method is the same signed-area sum.

BC-QA-06012 (research/question-analysis/question-archetypes.md#BC-QA-06012 Differentiating an accumulation function with a variable upper limit): the same definition with a request for h prime. That request says "not this concept": it belongs to BC-CON-06008.

## Method choice

Three strategy blocks; st-1 serves both bands.

- st-1, BC-QA-06003. Method, `expected_solution_path[0]`: evaluate g at the requested inputs as signed areas. Rival from `wrong_approaches`: features of g read off the plotted f (BC-ERR-06008). Separating feature: the plotted curve is f, and g is the area under it.
- st-2, BC-QA-06004. Method: partition where the graph changes character. Rival: regions below the axis added as positive area (BC-ERR-06014). Separating feature: a piece below the axis enters with a minus sign.
- st-3, BC-QA-06012. Method: the derivative equals the integrand at the upper limit. Rival: the chain factor dropped (BC-ERR-06027). Separating feature: an upper limit that is a function of x, not x itself.

All three archetypes carry `asked_to_produce` and `common_givens`, so no block is tagged inferred.

## Solution path

- ex-1, BC-QA-06003, both bands, no calculator. Draw from `parameter_spec`: heights [2, 0, -2, -2], lower 2, circle above, half_point 1/2, letters fg, ask value. Constraints hold: heights[3] is -2, linear_total is -8, and a vertex after the lower limit is negative. The graph joins (0, 2), (2, 0), (4, -2), (6, -2), (8, 0), then a semicircle of radius 2 above the axis on [8, 12]; g(12) = -8 + 2 pi. No published BC-QA-06003 item carries this draw.
- Steps follow `expected_solution_path[0]`: the three linear pieces from 2 to 8 as signed trapezoid and triangle areas (new), their sum (equivalent), the semicircle added (new), the value (equivalent, tagged BC-PT-99069). A fluent solver writes the sum of signed pieces and the value; each area formula is held.

## Scoring

BC-QA-06003 lists BC-PT-99069; ex-1's value step earns it. The reader_checks line for BC-PT-99069 is quoted in the machine record. The value alone earns the point (BC-QA-06004 `scoring_pattern`, sg-25:18), and a value from the wrong starting limit does not (research/scoring/point-taxonomy.md#BC-PT-99069 Value of an accumulation function found from geometry of a graph). A wrong value imported into a later part carries its error forward (research/scoring/common-point-losses.md#Answer points).

## Traps

Five active errors meet the skills; the first four in the bundle's order are served: BC-ERR-06014 and BC-ERR-99012 (linked BC-MIS at severity high), BC-ERR-06013 and BC-ERR-06028 (medium). BC-ERR-99032 is the fifth and is not served (cap 4). Mid band: the first two. All on ex-1's draw.

- err-BC-ERR-06014: 8 + 2 pi against -8 + 2 pi. Possible reason, words from BC-MIS-08024.
- err-BC-ERR-99012: the area counted from x = 0, -6 + 2 pi, against -8 + 2 pi. Possible reason, words from BC-MIS-08012.
- err-BC-ERR-06013: the semicircle given 4 pi, -8 + 4 pi. Possible reason, words from BC-MIS-08019.
- err-BC-ERR-06028: g'(5) left as f(t) against f(5) = -2. Possible reason, words from BC-MIS-06024.

## Representations

None as a separate block. The topic's Representations paragraph names the graph of the integrand to values of g; ki-1's motion and ki-2's interactive carry it.

## Prerequisite bridge

- BC-PRQ-06005, BC-PRQ-06007, BC-PRQ-06013, each from its `description_plain` and `failure_signature`.

## Time

BC-QA-06003 is `no_calculator`, one part of a multipart free response question or a single MCQ item, so the FRQ shape is Section II Part B, 15.0 minutes per question (research/exam/exam-structure.md#Section and part layout). The value part carries one point, a share of about 1.67 minutes by points out of 9 [inferred: docs/lessons/unit-06/README.md, section 5]. The minutes go on the sign of each piece; each area formula is held.

## Checks

- chk-1, completion of ex-1, both bands: the linear total -8 is given; the student adds the semicircle. Key -8 + 2 pi.
- chk-2, isomorph, both bands. Draw: heights [1, 0, -1, -1], lower 2, circle below. Key -4 - 2 pi.
- chk-3, MCQ, low band. Draw: heights [-2, 0, 2, 1], lower 2, circle below. Key 6 - 2 pi. Distractors: 6 + 2 pi (BC-ERR-06014), 4 - 2 pi (BC-ERR-99012, counted from x = 0), 6 - 4 pi (BC-ERR-06013).

## Delivery

- orientation: text. Rule 6; the figure-bearing BC-REP-02 is served on ki-1 and ki-2.
- ki-1: motion. Rule 2: "used to define new functions" is a quantity accumulating as the upper limit moves (docs/lessons/unit-06/README.md, section 6) [inferred; settled by the modality A/B].
- ki-2: interactive. Rule 4 promoted: BC-REP-02 on BC-SKL-06020; BC-QA-06003 `common_givens` "an accumulation function g with a fixed lower limit" and `difficulty_variables` "whether regions below the axis are involved" name a varying quantity, and the stem asks for values of g [inferred; settled by the modality A/B].
- ex-1, the four error blocks: step_reveal. Rule 1.

## Band plan

- Low (full): orientation, ki-1, ki-2, st-1 to st-3, ex-1 with its scoring line, the four error blocks, chk-1 to chk-3, the three bridges. 694 words, 4.7 minutes (cap 900 and 6).
- Mid (brief): orientation, ki-1, st-1, ex-1 with its scoring line, err-BC-ERR-06014, err-BC-ERR-99012, chk-1, chk-2, the three bridges. 450 words, 3.0 minutes (cap 450 and 3).
- Refresher: ki-1, the four error blocks, ex-1.

## Sources

- BC-CON-06007; BC-SKL-06017, BC-SKL-06020; BC-EK-FUN-5A1, BC-EK-FUN-5A3; ced:121, ced:122
- BC-QA-06003, BC-QA-06004, BC-QA-06012; BC-PT-99069; sg-25:18
- BC-ERR-06014, BC-ERR-99012, BC-ERR-06013, BC-ERR-06028; BC-MIS-08024, BC-MIS-08012, BC-MIS-08019, BC-MIS-06024
- BC-PRQ-06005, BC-PRQ-06007, BC-PRQ-06013
- research/units/unit-06-integration-accumulation.md#6.4 The Fundamental Theorem of Calculus and Accumulation Functions
- research/question-analysis/question-archetypes.md#BC-QA-06003 Accumulation function analysed from the graph of the integrand
- research/question-analysis/question-archetypes.md#BC-QA-06004 Definite integral evaluated from a graph by geometry
- research/question-analysis/question-archetypes.md#BC-QA-06012 Differentiating an accumulation function with a variable upper limit
- research/scoring/point-taxonomy.md#BC-PT-99069 Value of an accumulation function found from geometry of a graph
- research/scoring/common-point-losses.md#Answer points
- research/exam/exam-structure.md#Section and part layout
- [inferred] The share of the 15.0 minutes for a one-point value part. Settled by timing data per part.
- [inferred] ki-1 as motion and ki-2 as interactive. Settled by the modality A/B.

## Machine record

```json
{
 "id": "LSN-CON-06007",
 "kind": "concept",
 "target_id": "BC-CON-06007",
 "unit": "06",
 "skills": ["BC-SKL-06017", "BC-SKL-06020"],
 "orientation": {
  "text": "A response finds g at an input as signed area from the fixed lower limit, with t kept inside the integral.",
  "sources": ["BC-CON-06007", "research/units/unit-06-integration-accumulation.md#6.4 The Fundamental Theorem of Calculus and Accumulation Functions"]
 },
 "key_ideas": [
  {
   "id": "ki-1",
   "ek_id": "BC-EK-FUN-5A1",
   "depth": "core",
   "text": "For each x, the integral of f from a fixed a to x is one number, so it defines a function of x. t is bound; x sits only in the limit.",
   "notation": "g(x) = integral from a to x of f(t) dt",
   "quote": {"text": "The definite integral can be used to define new functions.", "source": "ced:121"},
   "sources": ["BC-EK-FUN-5A1", "ced:121", "research/units/unit-06-integration-accumulation.md#6.4 The Fundamental Theorem of Calculus and Accumulation Functions"]
  },
  {
   "id": "ki-2",
   "ek_id": "BC-EK-FUN-5A3",
   "depth": "extended",
   "text": "From a graph of f, g(b) is the signed area from a to b: pieces above the axis add, pieces below subtract, and b left of a flips the sign.",
   "notation": "g(a) = 0",
   "quote": null,
   "sources": ["BC-EK-FUN-5A3", "ced:122", "research/units/unit-06-integration-accumulation.md#6.4 The Fundamental Theorem of Calculus and Accumulation Functions"]
  }
 ],
 "strategy": [
  {
   "id": "st-1",
   "archetype_id": "BC-QA-06003",
   "cue": "g is an integral of a graphed f from a fixed input; values of g asked.",
   "method": "First line: g(b) as signed areas from the lower limit to b.",
   "rival": "Rival: features read off the plotted f (BC-ERR-06008).",
   "separating_feature": "The curve drawn is f, not g.",
   "sources": ["BC-QA-06003"],
   "evidence_tag": "verified"
  },
  {
   "id": "st-2",
   "archetype_id": "BC-QA-06004",
   "cue": "Segments and semicircles, with numerical limits.",
   "method": "First line: the region split where the graph changes character, each piece with its sign.",
   "rival": "Rival: regions below the axis added as positive area (BC-ERR-06014).",
   "separating_feature": "A piece below the axis enters with a minus sign.",
   "sources": ["BC-QA-06004"],
   "evidence_tag": "verified"
  },
  {
   "id": "st-3",
   "archetype_id": "BC-QA-06012",
   "cue": "The same definition, but h prime is asked.",
   "method": "First line: h'(x) equals the integrand at the upper limit.",
   "rival": "Rival: the chain factor dropped (BC-ERR-06027).",
   "separating_feature": "An upper limit that is a function of x, not x itself.",
   "sources": ["BC-QA-06012"],
   "evidence_tag": "verified"
  }
 ],
 "worked_examples": [
  {
   "id": "ex-1",
   "archetype_id": "BC-QA-06003",
   "bands": ["low", "mid"],
   "parameter_draw": {"heights": [2, 0, -2, -2], "lower": 2, "circle": "above", "half_point": "1/2", "letters": "fg", "ask": "value"},
   "problem": {"text": "f: segments through (0, 2), (2, 0), (4, -2), (6, -2), (8, 0), then a radius 2 semicircle above the axis. g(x) = integral of f from 2 to x. Find g(12).", "command_verb": "find"},
   "calculator_status": "no_calculator",
   "steps": [
    {"cue": "Start at the lower limit 2.", "why": "Three pieces below the axis.", "expr": "-2 - 4 - 2", "relation": "new"},
    {"cue": "Add them.", "why": "Signed total to 8.", "expr": "-8", "relation": "equivalent"},
    {"cue": "Semicircle above the axis.", "why": "Half of pi r squared, positive.", "expr": "-8 + pi*2**2/2", "relation": "new"},
    {"cue": "The stem asks for g(12).", "why": "The value is scored.", "expr": "-8 + 2*pi", "relation": "equivalent", "point_type_id": "BC-PT-99069"}
   ],
   "answer": {"form": "symbolic", "expr": "-8 + 2*pi"}
  }
 ],
 "what_a_reader_scores": [
  {"example_id": "ex-1", "point_type_ids": ["BC-PT-99069"], "lines": [{"point_type_id": "BC-PT-99069", "text": "Value of an accumulation function found from geometry of a graph. Earned by: The value of the accumulation function at the requested input, computed from areas of the regions under the graph, with the correct sign for reversed limits (sg-25:18, sg-24:12). Not earned by: A value from the wrong starting limit; sg-24:13 has a special case where an explicitly wrong lower limit forfeits the first point it would otherwise have earned."}]}
 ],
 "common_errors": [
  {
   "error_id": "BC-ERR-06014",
   "observed_behavior": "Every piece of the region is added with a positive sign, so a signed integral is reported as a plain area.",
   "scoring_consequence": "The value point is lost, and any later part that imports the value inherits the error.",
   "wrong_step": {"text": "8 + 2 pi.", "expr": "8 + 2*pi"},
   "right_step": {"text": "-8 + 2 pi.", "expr": "-8 + 2*pi"},
   "relation": "distinct",
   "possible_reason": {"misconception_id": "BC-MIS-08024", "text": "reads every definite integral as area under a graph"},
   "sources": ["BC-ERR-06014", "BC-MIS-08024"]
  },
  {
   "error_id": "BC-ERR-99012",
   "observed_behavior": "Responses write the integral of f prime from a to x as f of x, ignoring the value at the lower limit, or mishandle a reversed pair of limits and report the wrong sign for an accumulated area.",
   "scoring_consequence": "The value or setup point in that part is not earned, and the error usually propagates to later parts that build on the value.",
   "wrong_step": {"text": "From x = 0.", "expr": "2 - 8 + 2*pi"},
   "right_step": {"text": "From x = 2.", "expr": "-8 + 2*pi"},
   "relation": "distinct",
   "possible_reason": {"misconception_id": "BC-MIS-08012", "text": "chooses limits from the axes of the picture"},
   "sources": ["BC-ERR-99012", "BC-MIS-08012"]
  },
  {
   "error_id": "BC-ERR-06013",
   "observed_behavior": "The area of a semicircular piece of the region is computed as pi times the radius squared.",
   "scoring_consequence": "The value point for that integral is lost.",
   "wrong_step": {"text": "Semicircle as 4 pi.", "expr": "-8 + 4*pi"},
   "right_step": {"text": "Semicircle as 2 pi.", "expr": "-8 + 2*pi"},
   "relation": "distinct",
   "possible_reason": {"misconception_id": "BC-MIS-08019", "text": "remembers the squared dimension but not the fraction in front of it"},
   "sources": ["BC-ERR-06013", "BC-MIS-08019"]
  },
  {
   "error_id": "BC-ERR-06028",
   "observed_behavior": "The response evaluates the integrand at the dummy variable or leaves the answer in terms of t.",
   "scoring_consequence": "The answer point is not earned because the derivative is not expressed in the independent variable.",
   "wrong_step": {"text": "g'(5) = f(t).", "expr": "f(t)"},
   "right_step": {"text": "g'(5) = f(5) = -2.", "expr": "-2"},
   "relation": "distinct",
   "possible_reason": {"misconception_id": "BC-MIS-06024", "text": "does not distinguish the bound variable inside the integral from the variable in the upper limit"},
   "sources": ["BC-ERR-06028", "BC-MIS-06024"]
  }
 ],
 "representations": null,
 "prerequisite_bridges": [
  {"prq_id": "BC-PRQ-06005", "text": "Read f at the stated input; keep f and f prime apart."},
  {"prq_id": "BC-PRQ-06007", "text": "A trapezoid is not a rectangle; a semicircle is half a circle."},
  {"prq_id": "BC-PRQ-06013", "text": "t stays inside; only the limits carry x."}
 ],
 "time": {"exam_part": "II-B", "budget_minutes": 15.0, "source": "research/exam/exam-structure.md#Section and part layout", "written_steps": {"ex-1": [2, 4]}, "skipped_steps": {"ex-1": [1, 3]}},
 "checks": [
  {
   "id": "chk-1",
   "check_kind": "completion",
   "format": "short_answer",
   "bands": ["low", "mid"],
   "archetype_id": "BC-QA-06003",
   "parameter_draw": {"heights": [2, 0, -2, -2], "lower": 2, "circle": "above", "half_point": "1/2", "letters": "fg", "ask": "value"},
   "completes": "ex-1",
   "stem": {"text": "Same f. Pieces from 2 to 8 total -8. Find g(12).", "command_verb": "find"},
   "key": {"form": "symbolic", "expr": "-8 + 2*pi"},
   "steps": [
    {"text": "Semicircle added.", "expr": "-8 + pi*2**2/2", "relation": "new"},
    {"text": "g(12).", "expr": "-8 + 2*pi", "relation": "equivalent"}
   ],
   "calculator_status": "no_calculator",
   "skills": ["BC-SKL-06020"]
  },
  {
   "id": "chk-2",
   "check_kind": "isomorph",
   "format": "short_answer",
   "bands": ["low", "mid"],
   "archetype_id": "BC-QA-06003",
   "parameter_draw": {"heights": [1, 0, -1, -1], "lower": 2, "circle": "below", "half_point": "1/2", "letters": "fg", "ask": "value"},
   "stem": {"text": "As ex-1, with vertices (0, 1), (2, 0), (4, -1), (6, -1), (8, 0) and the semicircle below. Find g(12).", "command_verb": "find"},
   "key": {"form": "symbolic", "expr": "-4 - 2*pi"},
   "steps": [
    {"text": "Linear pieces from 2 to 8.", "expr": "-1 - 2 - 1", "relation": "new"},
    {"text": "Semicircle below.", "expr": "-4 - pi*2**2/2", "relation": "new"},
    {"text": "g(12).", "expr": "-4 - 2*pi", "relation": "equivalent"}
   ],
   "calculator_status": "no_calculator",
   "skills": ["BC-SKL-06020"]
  },
  {
   "id": "chk-3",
   "check_kind": "mcq",
   "format": "mcq",
   "bands": ["low"],
   "archetype_id": "BC-QA-06003",
   "parameter_draw": {"heights": [-2, 0, 2, 1], "lower": 2, "circle": "below", "half_point": "1/2", "letters": "fg", "ask": "value"},
   "stem": {"text": "f joins (0, -2), (2, 0), (4, 2), (6, 1), (8, 0), then a semicircle of radius 2 below the axis. g(x) = integral of f from 2 to x. g(12) is", "command_verb": "identify"},
   "key": {"form": "symbolic", "expr": "6 - 2*pi"},
   "steps": [
    {"text": "Linear pieces from 2 to 8.", "expr": "2 + 3 + 1", "relation": "new"},
    {"text": "Semicircle below.", "expr": "6 - pi*2**2/2", "relation": "new"},
    {"text": "g(12).", "expr": "6 - 2*pi", "relation": "equivalent"}
   ],
   "options": [
    {"id": "A", "is_key": false, "expr": "6 + 2*pi", "error_path": "BC-ERR-06014", "derivation": "the semicircle below the axis added as positive area"},
    {"id": "B", "is_key": false, "expr": "4 - 2*pi", "error_path": "BC-ERR-99012", "derivation": "the area counted from x = 0 instead of the lower limit 2"},
    {"id": "C", "is_key": true, "expr": "6 - 2*pi", "error_path": null},
    {"id": "D", "is_key": false, "expr": "6 - 4*pi", "error_path": "BC-ERR-06013", "derivation": "the semicircle given the area of a full circle"}
   ],
   "calculator_status": "no_calculator",
   "skills": ["BC-SKL-06020"]
  }
 ],
 "delivery": [
  {"block": "orientation", "mode": "text", "reason": "rule 6: a statement of what a response shows; BC-REP-02 is served on ki-1 and ki-2", "sources": ["BC-SKL-06017"]},
  {"block": "ki-1", "mode": "motion", "reason": "rule 2: a quantity accumulating as the upper limit moves, per the unit delivery map for FUN-5A1", "sources": ["BC-SKL-06017", "BC-SKL-06020"],
   "spec": {"kind": "graph", "representations": ["BC-REP-02"], "window": {"x": [0, 12], "y": [-3, 3]},
    "curves": [{"piecewise_linear": [[0, 2], [2, 0], [4, -2], [6, -2], [8, 0]]}, {"semicircle": {"centre": [10, 0], "radius": 2, "side": "above"}}],
    "frames": [{"x": 2, "g": "0"}, {"x": 4, "g": "-2"}, {"x": 6, "g": "-6"}, {"x": 8, "g": "-8"}, {"x": 10, "g": "-8 + pi"}, {"x": 12, "g": "-8 + 2 pi"}],
    "drawn": ["the region from 2 to the frame's x shaded, above the axis in one colour and below in another"],
    "labels": [{"text": "lower limit 2", "placement": "inside"}, {"text": "g(x) = shaded signed area", "placement": "inside"}, {"text": "below the axis: subtract", "placement": "inside"}]},
   "fallback": "three frames side by side, at x = 4, 8 and 12, each with its shaded region and its g value inside the figure",
   "reduced_motion": "no auto-advance; each key press cross-fades to the next frame",
   "keyboard": "Right arrow steps to the next frame, Left arrow to the previous; Space pauses auto-advance"},
  {"block": "ki-2", "mode": "interactive", "reason": "rule 4 promoted: BC-REP-02 on BC-SKL-06020; BC-QA-06003 common_givens and difficulty_variables name a varying upper limit and regions below the axis, and the stem asks for values of g", "sources": ["BC-SKL-06020", "BC-QA-06003"],
   "spec": {"kind": "graph", "representations": ["BC-REP-02"], "window": {"x": [0, 12], "y": [-3, 3]},
    "curves": [{"piecewise_linear": [[0, 2], [2, 0], [4, -2], [6, -2], [8, 0]]}, {"semicircle": {"centre": [10, 0], "radius": 2, "side": "above"}}],
    "controls": [{"type": "draggable_point", "constrained_to": "x-axis", "range": [0, 12], "start": 2, "name": "upper limit b"}],
    "drawn": ["signed area from 2 to b shaded", "the value of g(b) shown beside the point"],
    "labels": [{"text": "b", "placement": "inside"}, {"text": "g(b)", "placement": "inside"}, {"text": "b left of 2: sign flips", "placement": "inside"}],
    "question": "As b moves right across a piece below the axis, does g(b) rise or fall?"},
   "fallback": "a static figure with g marked at x = 0, 2, 4, 6, 8 and 12, each label inside the figure",
   "keyboard": "Tab focuses the point; left and right arrow keys move b by 1; Enter reads out g(b)"},
  {"block": "ex-1", "mode": "step_reveal", "reason": "rule 1", "sources": []},
  {"block": "err-BC-ERR-06014", "mode": "step_reveal", "reason": "rule 1", "sources": []},
  {"block": "err-BC-ERR-99012", "mode": "step_reveal", "reason": "rule 1", "sources": []},
  {"block": "err-BC-ERR-06013", "mode": "step_reveal", "reason": "rule 1", "sources": []},
  {"block": "err-BC-ERR-06028", "mode": "step_reveal", "reason": "rule 1", "sources": []}
 ],
 "refresher": ["ki-1", "err-BC-ERR-06014", "err-BC-ERR-99012", "err-BC-ERR-06013", "err-BC-ERR-06028", "ex-1"],
 "read_minutes": {"full": 4.7, "brief": 3.0},
 "word_count": {"full": 694, "brief": 450},
 "research_lines": [
  {"file": "research/units/unit-06-integration-accumulation.md", "line": "The variable of integration t is a bound variable; the independent variable appears only in the limits."}
 ],
 "inferred": [
  {"claim": "A one-point value part takes about 1.67 of the 15.0 Section II minutes.", "settles": "Timing data per part once the fluency telemetry exists."},
  {"claim": "ki-1 is served as motion and ki-2 as an interactive draggable upper limit rather than static figures.", "settles": "The modality A/B in the build plan: skip rate and time to first credited success by mode."}
 ],
 "sources": ["BC-CON-06007", "BC-SKL-06017", "BC-SKL-06020", "BC-EK-FUN-5A1", "BC-EK-FUN-5A3", "ced:121", "ced:122", "BC-QA-06003", "BC-QA-06004", "BC-QA-06012", "BC-PT-99069", "sg-25:18", "BC-ERR-06014", "BC-ERR-99012", "BC-ERR-06013", "BC-ERR-06028", "BC-MIS-08024", "BC-MIS-08012", "BC-MIS-08019", "BC-MIS-06024", "BC-PRQ-06005", "BC-PRQ-06007", "BC-PRQ-06013", "research/units/unit-06-integration-accumulation.md#6.4 The Fundamental Theorem of Calculus and Accumulation Functions", "research/question-analysis/question-archetypes.md#BC-QA-06003 Accumulation function analysed from the graph of the integrand", "research/exam/exam-structure.md#Section and part layout"]
}
```
