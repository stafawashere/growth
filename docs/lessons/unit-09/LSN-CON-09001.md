---
title: LSN-CON-09001 Curve defined by parametric equations
research_date: 2026-09-29
status: designed
purpose: Authoring spec for the concept lesson on BC-CON-09001, a curve whose two coordinates are functions of one parameter, built from authoring_bundle("BC-CON-09001") and the research files it cites, so an author fills plan 15's lesson record without making a teaching decision.
---

# LSN-CON-09001 Curve defined by parametric equations

Concept BC-CON-09001 (skill BC-SKL-09001), topic 9.1 of Unit 9, loaded by BC-QA-09001 only. It is the first concept of the unit (docs/lessons/unit-09/README.md, section 1): every later parametric and vector concept differentiates the components this lesson differentiates.

## Prediction

Posed on ex-1's numbers, both bands, before any rule. Stem: a particle at \((2t+\ln(1+t^2), 4\sin(t^2/2))\), and what \(dx/dt\) describes at \(t=3/2\). Form `mcq`, three options, key B, "How fast the horizontal coordinate changes per unit of \(t\)". The other two options, "The slope of the path" and "The rate of \(y\) with respect to \(x\)", are the slope readings BC-MIS-09001 and BC-MIS-09002 name, and neither is true of \(dx/dt\). The resolution states the core claim of ki-1: each coordinate is differentiated on its own, and the parameter is not a coordinate. Sources: BC-CON-09001, BC-EK-CHA-3G1 and the Required mathematical knowledge paragraph of topic 9.1.

## Orientation

Served text (18 words), from BC-CON-09001 `description_plain` and the topic's Assessment behaviour paragraph (research/units/unit-09-parametric-polar-vector.md#9.1 Defining and Differentiating Parametric Equations): a response treats \(x(t)\) and \(y(t)\) as two separate functions of the parameter, differentiates each with respect to \(t\), and labels both rates before any slope is formed. No count, no frequency.

## Key ideas

One BC-EK maps to the skill, BC-EK-CHA-3G1 (ced:171), so one core block, both bands.

- ki-1 (core). Derivative rules for ordinary functions apply to each component; the parameter is not a coordinate, so \(dx/dt\) and \(dy/dt\) are rates in time, not slopes; a component with an inner function needs the chain rule. Paraphrased from the Required mathematical knowledge paragraph (Parametric derivative, Notation). Anchor quote (14 words) from ced:171. Notation line from the concept record: \(x(t)\), \(y(t)\); the parameter \(t\).

## Recognition

Stem features that say "this concept":

- BC-QA-09001 (family parametric-calculus, calculator, one part of the calculator active BC free response question; research/question-analysis/question-archetypes.md#BC-QA-09001 Slope of the tangent to a parametric path at a time): `common_givens` a parametric or vector description of a path and a time; `asked_to_produce` a quotient of parametric derivatives and a numerical slope; `typical_wording` "find the slope of the line tangent to the path of the particle at the given time". The signal is two coordinates written in one letter that is neither \(x\) nor \(y\). Official appearances: BC-FRQ-2022-Q2-A, BC-FRQ-2015-Q2-B, BC-FRQ-2023-Q2-C, BC-FRQ-2026-Q2-B; MCQ BC-MCQ-SAMPLE-017, BC-MCQ-PE2012-002.

What says "not this concept": a single function \(y=f(x)\) (ordinary differentiation); a polar equation \(r=f(\theta)\) (BC-CON-09013); an ordered pair of rates already given, where the work starts at the quotient (BC-CON-09002).

The contrast pair in st-1 draws its near miss from outside the archetype: a stem for \(dy/dx\) of a single function \(y=f(x)\), where nothing is parametric and the ordinary derivative is the whole task. It is the first item above the line. The separating feature is whether a parameter appears at all.

## Method choice

One strategy block, both bands.

- st-1, BC-QA-09001, with the contrast pair. Cue: a path given as \((x(t), y(t))\) and a time, and the stem asks for a slope (`common_givens`, `asked_to_produce`). Method, `expected_solution_path[0]`: compute \(dy/dt\) and \(dx/dt\). First written line: both rates, labelled, each differentiated in \(t\). Rival, `wrong_approaches`: using a component derivative that was never declared. Separating feature: each rate is written and labelled before it enters any quotient, so a dropped chain factor is visible where it happens.

BC-QA-09001 carries `asked_to_produce` and `common_givens`, so the block is not tagged inferred. The pair: this, a drone at \((5t+\ln(1+t^2), 3\sin(t^2))\) and the slope at \(t=1\); not this, the slope of \(y=x^3-2x\) at \(x=2\), which calls for the ordinary derivative; feature, whether both coordinates are written in a parameter.

## Solution path

- ex-1, BC-QA-09001, both bands, calculator. Draw: drift 2, height 4, rate 1/2, vertical sine, time 3/2, object particle, given positions, so \(x(t)=2t+\ln(1+t^2)\), \(y(t)=4\sin(t^2/2)\). Steps follow `expected_solution_path`: \(dx/dt\) (valued, new), its value at \(t=3/2\) (evaluate), \(dy/dt\) by the chain rule (valued, new), its value (evaluate), the quotient (valued, new, tagged BC-PT-99049), the slope to three decimals (evaluate, approx). A fluent solver writes the two labelled rates and the quotient, and lets the calculator carry the decimals.

No productive-failure opener targets this concept (BC-CON-09015 is Unit 9's target), so no comparison callout.

## Scoring

BC-QA-09001 lists BC-PT-99005, BC-PT-99049, BC-PT-99004 and BC-PT-99001. The example tags BC-PT-99049 only, because the archetype's `scoring_pattern` gives this part one point, earned when the quotient of the two rates is communicated (sg-23:7). The line, generated by `reader_checks(["BC-PT-99049"])`:

Derivative of one variable with respect to another by the chain rule in polar or parametric form. Earned by: A correct chain or quotient relation among the derivatives, presented symbolically or numerically (sg-26:7, sg-23:7). Not earned by: An equation of the form expression equals constant that equates a general expression to a single value (sg-22:6, sg-23:6). Notation: sg-25:7 accepts several loose notations for an evaluated derivative, including one written without the evaluation bar, and still awards the point.

Point losses the scoring research names for this shape: a wrong component costs the point that depends on it, but a declared component may be imported into later parts (BC-ERR-09001, sg-23:7); a quotient assembled from the wrong derivatives loses the setup point (research/scoring/common-point-losses.md#Setup points, BC-ERR-99029).

## Traps

One active error meets the concept's skill, BC-ERR-09001 (linked BC-MIS-09001 at severity high). Both bands.

- err-BC-ERR-09001. Wrong step on ex-1's draw: \(dy/dt=4\cos(t^2/2)\), the chain factor \(t\) dropped, giving \(4\cos(9/8)\) at \(t=3/2\). Right step: \(dy/dt=4t\cos(t^2/2)\), giving \(6\cos(9/8)\). Distinct. No possible reason is attached: the dropped chain factor is one of the record's `non_conceptual_causes`, and BC-MIS-09001's description names a different mechanism.

## Representations

None. The topic's Representations paragraph names a plotted path to a tangent statement (BC-REP-02 to BC-REP-04), which belongs to the slope concept BC-CON-09002; the orientation figure carries the path here.

## Prerequisite bridge

- BC-PRQ-06005, from its `description_plain` and `failure_signature`: \(x(t)\) is the value of one function at the input \(t\), and \(x'(t)\) is a different function; reading one for the other, or evaluating at the wrong input, spoils every later rate.

## Time

BC-QA-09001 is `calculator` and its `multipart_structure` is one part of the calculator active BC free response question, so the part is Section II Part A, 15.0 minutes per question (research/exam/exam-structure.md#Section and part layout; plan 15, Fluency). The part carries one point, a 1.67 minute share at 9 points per question (docs/lessons/unit-09/README.md, section 5). A fluent solver writes the two labelled rates and the quotient (steps 1, 3, 5) and holds the evaluations for the calculator (steps 2, 4, 6) [inferred; settled by per-step timing from the fluency telemetry].

## Checks

- chk-1, completion of ex-1, both bands, short answer: the two rates at \(t=3/2\) are given, the student forms the quotient and reports three decimals. Key 0.885, equal to ex-1's answer.
- chk-2, isomorph on BC-QA-09001, both bands: drift 3, height 2, rate 1/3, vertical cosine, time 5/2, drone, positions, \(x=3t+\ln(1+t^2)\), \(y=2\cos(t^2/3)\). Key \(-0.787\).
- chk-3, MCQ on BC-QA-09001, low band: drift 1, height 3, rate 3/4, sine, time 1, bead, positions. Key 1.646. Distractors, each BC-ERR-09001 made on the draw: 1.098 (chain factor dropped in \(dy/dt\)), 2.195 (chain factor dropped in \(dx/dt\)), 2.250 (degree mode, a `non_conceptual_causes` entry).

No check or example draw equals a published BC-QA-09001 `parameter_draw` (content/items_gen_unit09).

## Delivery

- orientation: figure. Rule 4 (README rule 3): BC-REP-12 on BC-SKL-09001. The path with three parameter values marked, each labelled with its \(t\) and its point.
- ki-1: motion. Rule 2: the idea is a curve being traced as \(t\) advances; the frames show \(x(t)\) and \(y(t)\) read off separately at each \(t\), which separates the parameter from the horizontal coordinate (BC-MIS-09001). Static fallback: the frames side by side.
- ex-1: step_reveal. Rule 1.
- err-BC-ERR-09001: step_reveal. Rule 1.

Every non-text mode is [inferred]; settled by the modality A/B in the build plan.

## Band plan

- Low (full): prediction, orientation, bridge, ki-1, st-1 with the contrast pair, ex-1 with its scoring line, chk-1, err-BC-ERR-09001, chk-2, chk-3. 468 words, 3.2 minutes (cap 900 and 6).
- Mid (brief): prediction, orientation, bridge, ki-1, st-1 with the contrast pair, ex-1 with its scoring line, chk-1, err-BC-ERR-09001, chk-2. 446 words, 3.0 minutes (cap 450 and 3).
- Refresher: ki-1, err-BC-ERR-09001, ex-1.

## Sources

- BC-CON-09001; BC-MIS-09002; BC-SKL-09001; BC-EK-CHA-3G1; ced:171
- BC-QA-09001; BC-FRQ-2022-Q2-A, BC-FRQ-2015-Q2-B, BC-FRQ-2023-Q2-C, BC-FRQ-2026-Q2-B, BC-MCQ-SAMPLE-017, BC-MCQ-PE2012-002
- BC-PT-99049; sg-23:7
- BC-ERR-09001; BC-MIS-09001; BC-ERR-99029
- BC-PRQ-06005
- research/units/unit-09-parametric-polar-vector.md#9.1 Defining and Differentiating Parametric Equations
- research/question-analysis/question-archetypes.md#BC-QA-09001 Slope of the tangent to a parametric path at a time
- research/scoring/common-point-losses.md#Setup points
- research/exam/exam-structure.md#Section and part layout
- [inferred] Which steps a fluent solver writes and which the calculator holds. Settled by per-step timing from the fluency telemetry.
- [inferred] The figure and motion modes. Settled by the modality A/B.

## Machine record

```json
{
 "id": "LSN-CON-09001",
 "kind": "concept",
 "target_id": "BC-CON-09001",
 "unit": "09",
 "skills": ["BC-SKL-09001"],
 "prediction": {"id": "pr-1", "stem": {"text": "Before the rule: a particle has position \\((2t+\\ln(1+t^2), 4\\sin(t^2/2))\\). What does \\(dx/dt\\) describe at \\(t=3/2\\)?", "command_verb": "predict"}, "format": "mcq",
  "options": [{"id": "A", "label": "The slope of the path", "is_key": false}, {"id": "B", "label": "The rate of \\(x\\) per unit of \\(t\\)", "is_key": true}, {"id": "C", "label": "The rate of \\(y\\) with respect to \\(x\\)", "is_key": false}],
  "resolution": "\\(dx/dt\\) is a rate in \\(t\\), here \\(38/13\\). The parameter is not a coordinate, so it is not a slope; each coordinate is differentiated on its own.",
  "sources": ["BC-CON-09001", "BC-EK-CHA-3G1", "research/units/unit-09-parametric-polar-vector.md#9.1 Defining and Differentiating Parametric Equations"]},
 "orientation": {
  "text": "Each coordinate is a function of \\(t\\). A response differentiates both and labels the rates before any slope.",
  "sources": ["BC-CON-09001", "research/units/unit-09-parametric-polar-vector.md#9.1 Defining and Differentiating Parametric Equations"]
 },
 "key_ideas": [
  {
   "id": "ki-1",
   "ek_id": "BC-EK-CHA-3G1",
   "depth": "core",
   "text": "The usual derivative rules apply to each coordinate separately. The parameter is not a coordinate, so \\(dx/dt\\) and \\(dy/dt\\) are rates in time, not slopes. An inner function needs the chain rule.",
   "notation": "x(t), y(t); the parameter t",
   "quote": {"text": "Methods for calculating derivatives of real-valued functions can be extended to parametric functions.", "source": "ced:171"},
   "sources": ["BC-EK-CHA-3G1", "ced:171", "research/units/unit-09-parametric-polar-vector.md#9.1 Defining and Differentiating Parametric Equations"]
  }
 ],
 "strategy": [
  {
   "id": "st-1",
   "archetype_id": "BC-QA-09001",
   "cue": "A path in \\(t\\), a time, a slope.",
   "method": "Both labelled rates, \\(dy/dt\\) and \\(dx/dt\\).",
   "rival": "A component derivative never declared.",
   "separating_feature": "Each rate is labelled before any quotient.",
   "sources": ["BC-QA-09001"],
   "evidence_tag": "verified",
   "contrast": {
    "this": {"text": "A drone has position \\((5t+\\ln(1+t^2), 3\\sin(t^2))\\). Find the tangent slope at \\(t=1\\).", "archetype_id": "BC-QA-09001"},
    "not_this": {"text": "Find the tangent slope of \\(y=x^3-2x\\) at \\(x=2\\).", "why_not": "It asks for an ordinary derivative; no parameter appears."},
    "feature": "Both coordinates are written in a parameter."
   }
  }
 ],
 "worked_examples": [
  {
   "id": "ex-1",
   "archetype_id": "BC-QA-09001",
   "bands": ["low", "mid"],
   "parameter_draw": {"drift": "2", "height": "4", "rate": "1/2", "vertical": "sine", "time": "3/2", "object": "particle", "given": "positions"},
   "problem": {"text": "A particle has position \\((2t+\\ln(1+t^2), 4\\sin(t^2/2))\\). Using a calculator, find the slope of the tangent line to the path at \\(t=3/2\\), to three decimals.", "command_verb": "find"},
   "calculator_status": "calculator",
   "steps": [
    {"cue": "Differentiate \\(x\\).", "why": "The logarithm's inner \\(1+t^2\\) gives the factor \\(2t\\).", "expr": "2 + 2*t/(1+t**2)", "relation": "new"},
    {"cue": "The stem gives \\(t\\).", "why": "\\(2+3/3.25=38/13\\).", "expr": "38/13", "relation": "evaluate", "subs": {"t": "3/2"}},
    {"cue": "The sine has an inner \\(t^2/2\\).", "why": "Chain rule: \\(4\\cos(t^2/2)\\) times the inner derivative \\(t\\).", "expr": "4*t*cos(t**2/2)", "relation": "new"},
    {"cue": "Same time.", "why": "Labelled \\(dy/dt\\), so the quotient cites a declared value.", "expr": "6*cos(9/8)", "relation": "evaluate", "subs": {"t": "3/2"}},
    {"cue": "A slope: divide the rates.", "why": "\\(dy/dx\\) is \\(dy/dt\\) over \\(dx/dt\\); the written quotient is scored.", "expr": "6*cos(9/8)/(38/13)", "relation": "new", "point_type_id": "BC-PT-99049"},
    {"cue": "Three decimals asked.", "why": "Rounded only at the end.", "expr": "0.885", "relation": "evaluate", "subs": {}, "approx": true}
   ],
   "answer": {"form": "numeric", "expr": "0.885"}
  }
 ],
 "what_a_reader_scores": [
  {"example_id": "ex-1", "point_type_ids": ["BC-PT-99049"], "lines": [{"point_type_id": "BC-PT-99049", "text": "Derivative of one variable with respect to another by the chain rule in polar or parametric form. Earned by: A correct chain or quotient relation among the derivatives, presented symbolically or numerically (sg-26:7, sg-23:7). Not earned by: An equation of the form expression equals constant that equates a general expression to a single value (sg-22:6, sg-23:6). Notation: sg-25:7 accepts several loose notations for an evaluated derivative, including one written without the evaluation bar, and still awards the point."}]}
 ],
 "common_errors": [
  {
   "error_id": "BC-ERR-09001",
   "observed_behavior": "One of dx/dt or dy/dt is wrong, so every later quantity built from it is wrong.",
   "scoring_consequence": "The point that depends on that component is lost, though a declared incorrect component may be imported into later parts without further loss (sg-23:7).",
   "wrong_step": {"text": "Chain factor dropped: \\(4\\cos(9/8)\\).", "expr": "4*cos(9/8)"},
   "right_step": {"text": "With it, \\(6\\cos(9/8)\\).", "expr": "6*cos(9/8)"},
   "relation": "distinct",
   "fix_prompt": true,
   "possible_reason": null,
   "sources": ["BC-ERR-09001"]
  }
 ],
 "representations": null,
 "prerequisite_bridges": [
  {"prq_id": "BC-PRQ-06005", "text": "\\(x(t)\\) and \\(x'(t)\\) are different functions; confusing them spoils every later rate."}
 ],
 "time": {"exam_part": "II-A", "budget_minutes": 15.0, "source": "research/exam/exam-structure.md#Section and part layout", "written_steps": {"ex-1": [1, 3, 5]}, "skipped_steps": {"ex-1": [2, 4, 6]}},
 "checks": [
  {
   "id": "chk-1",
   "check_kind": "completion",
   "format": "short_answer",
   "bands": ["low", "mid"],
   "archetype_id": "BC-QA-09001",
   "parameter_draw": {"drift": "2", "height": "4", "rate": "1/2", "vertical": "sine", "time": "3/2", "object": "particle", "given": "positions"},
   "completes": "ex-1",
   "stem": {"text": "At \\(t=3/2\\), \\(dx/dt=38/13\\) and \\(dy/dt=6\\cos(9/8)\\). Write the slope to three decimals.", "command_verb": "write"},
   "key": {"form": "numeric", "expr": "0.885"},
   "steps": [
    {"text": "The slope is \\(dy/dt\\) divided by \\(dx/dt\\).", "expr": "6*cos(9/8)/(38/13)", "relation": "new", "point_type_id": "BC-PT-99049"},
    {"text": "To three decimals, 0.885.", "expr": "0.885", "relation": "evaluate", "subs": {}, "approx": true}
   ],
   "calculator_status": "calculator",
   "skills": ["BC-SKL-09001"]
  },
  {
   "id": "chk-2",
   "check_kind": "isomorph",
   "format": "short_answer",
   "bands": ["low", "mid"],
   "archetype_id": "BC-QA-09001",
   "parameter_draw": {"drift": "3", "height": "2", "rate": "1/3", "vertical": "cosine", "time": "5/2", "object": "drone", "given": "positions"},
   "stem": {"text": "A drone has position \\((3t+\\ln(1+t^2), 2\\cos(t^2/3))\\). Find the slope of the tangent line at \\(t=5/2\\), to three decimals.", "command_verb": "find"},
   "key": {"form": "numeric", "expr": "-0.787"},
   "steps": [
    {"text": "\\(dx/dt=3+2t/(1+t^2)\\).", "expr": "3 + 2*t/(1+t**2)", "relation": "new"},
    {"text": "At \\(t=5/2\\), \\(dx/dt=107/29\\).", "expr": "107/29", "relation": "evaluate", "subs": {"t": "5/2"}},
    {"text": "By the chain rule, \\(dy/dt=-(4t/3)\\sin(t^2/3)\\).", "expr": "-(4*t/3)*sin(t**2/3)", "relation": "new"},
    {"text": "At \\(t=5/2\\), \\(dy/dt=-(10/3)\\sin(25/12)\\).", "expr": "-(10/3)*sin(25/12)", "relation": "evaluate", "subs": {"t": "5/2"}},
    {"text": "The slope is \\(dy/dt\\) over \\(dx/dt\\).", "expr": "(-(10/3)*sin(25/12))/(107/29)", "relation": "new", "point_type_id": "BC-PT-99049"},
    {"text": "To three decimals, \\(-0.787\\).", "expr": "-0.787", "relation": "evaluate", "subs": {}, "approx": true}
   ],
   "calculator_status": "calculator",
   "skills": ["BC-SKL-09001"]
  },
  {
   "id": "chk-3",
   "check_kind": "mcq",
   "format": "mcq",
   "bands": ["low"],
   "archetype_id": "BC-QA-09001",
   "parameter_draw": {"drift": "1", "height": "3", "rate": "3/4", "vertical": "sine", "time": "1", "object": "bead", "given": "positions"},
   "stem": {"text": "A bead moves with position \\((t+\\ln(1+t^2), 3\\sin(3t^2/4))\\). Using a calculator, find the slope of the line tangent to its path at \\(t=1\\).", "command_verb": "find"},
   "key": {"form": "numeric", "expr": "1.646"},
   "steps": [
    {"text": "\\(dx/dt=1+2t/(1+t^2)\\), which is 2 at \\(t=1\\).", "expr": "1 + 2*t/(1+t**2)", "relation": "new"},
    {"text": "At \\(t=1\\), \\(dx/dt=2\\).", "expr": "2", "relation": "evaluate", "subs": {"t": "1"}},
    {"text": "By the chain rule, \\(dy/dt=(9t/2)\\cos(3t^2/4)\\).", "expr": "(9*t/2)*cos(3*t**2/4)", "relation": "new"},
    {"text": "At \\(t=1\\), \\(dy/dt=(9/2)\\cos(3/4)\\).", "expr": "(9/2)*cos(3/4)", "relation": "evaluate", "subs": {"t": "1"}},
    {"text": "The slope is the quotient of the two rates.", "expr": "((9/2)*cos(3/4))/2", "relation": "new", "point_type_id": "BC-PT-99049"},
    {"text": "To three decimals, 1.646.", "expr": "1.646", "relation": "evaluate", "subs": {}, "approx": true}
   ],
   "options": [
    {"id": "A", "is_key": false, "expr": "1.098", "error_path": "BC-ERR-09001", "derivation": "chain factor dropped in dy/dt: 3cos(3/4) divided by 2"},
    {"id": "B", "is_key": true, "expr": "1.646", "error_path": null},
    {"id": "C", "is_key": false, "expr": "2.195", "error_path": "BC-ERR-09001", "derivation": "chain factor 2t dropped in dx/dt, so dx/dt = 3/2: (9/2)cos(3/4) divided by 3/2"},
    {"id": "D", "is_key": false, "expr": "2.250", "error_path": "BC-ERR-09001", "derivation": "calculator in degree mode: (9/2)cos(0.75 degrees) divided by 2"}
   ],
   "calculator_status": "calculator",
   "skills": ["BC-SKL-09001"]
  }
 ],
 "delivery": [
  {"block": "orientation", "mode": "figure", "reason": "rule 4 (README rule 3): BC-REP-12 on BC-SKL-09001; not promoted, the orientation states what a response shows and asks for no reading", "sources": ["BC-SKL-09001"],
   "spec": {"kind": "parametric_path", "representations": ["BC-REP-12"], "x": "2*t + log(1 + t**2)", "y": "4*sin(t**2/2)", "t_range": [0, 2.2],
    "marks": [{"t": 0.5}, {"t": 1.0}, {"t": 1.5}],
    "labels": [{"text": "t = 0.5", "placement": "inside"}, {"text": "t = 1", "placement": "inside"}, {"text": "t = 1.5", "placement": "inside"}, {"text": "(x(t), y(t))", "placement": "inside"}]},
   "fallback": "the same path static with the three marked points and their labels", "keyboard": "no control; the figure description is reached with Tab"},
  {"block": "ki-1", "mode": "motion", "reason": "rule 2: a curve being traced as t advances; the frames read x(t) and y(t) off separately, which separates the parameter from the horizontal coordinate (BC-MIS-09001); rule 4, BC-REP-12 on BC-SKL-09001, for the static fallback", "sources": ["BC-SKL-09001", "BC-MIS-09001"],
   "spec": {"kind": "parametric_trace", "representations": ["BC-REP-12", "BC-REP-01"], "x": "2*t + log(1 + t**2)", "y": "4*sin(t**2/2)",
    "frames": [{"t": 0}, {"t": 0.5}, {"t": 1.0}, {"t": 1.5}, {"t": 2.0}],
    "drawn": ["the path traced up to the frame's t", "the particle at (x(t), y(t))", "dashed drops from the particle to both axes"],
    "labels": [{"text": "t, the parameter", "placement": "inside"}, {"text": "x(t)", "placement": "inside"}, {"text": "y(t)", "placement": "inside"}]},
   "fallback": "three frames side by side (t = 0.5, 1, 1.5), static, each with its three labels inside",
   "keyboard": "Right arrow steps to the next frame, Left arrow to the previous; Space pauses auto-advance",
   "reduced_motion": "no auto-advance; each key press cross-fades to the next frame"},
  {"block": "ex-1", "mode": "step_reveal", "reason": "rule 1", "sources": []},
  {"block": "err-BC-ERR-09001", "mode": "step_reveal", "reason": "rule 1", "sources": []}
 ],
 "refresher": ["ki-1", "err-BC-ERR-09001", "ex-1"],
 "read_minutes": {"full": 3.2, "brief": 3.0},
 "word_count": {"full": 468, "brief": 446},
 "research_lines": [
  {"file": "research/units/unit-09-parametric-polar-vector.md", "line": "The parameter is not a coordinate, so dy/dx and dy/dt are different objects and the response must say which is being reported."},
  {"file": "research/question-analysis/question-archetypes.md", "line": "using a component derivative that was never declared"}
 ],
 "inferred": [
  {"claim": "A fluent solver writes the two labelled rates and the quotient and holds the evaluations for the calculator.", "settles": "Per-step timing from the fluency telemetry."},
  {"claim": "Figure and motion delivery serve this concept better than text.", "settles": "The modality A/B in the build plan: skip rate and time to first credited success by mode."}
 ],
 "sources": ["BC-CON-09001", "BC-SKL-09001", "BC-EK-CHA-3G1", "ced:171", "BC-QA-09001", "BC-PT-99049", "sg-23:7", "BC-ERR-09001", "BC-MIS-09001", "BC-ERR-99029", "BC-PRQ-06005", "BC-FRQ-2022-Q2-A", "BC-FRQ-2015-Q2-B", "BC-FRQ-2023-Q2-C", "BC-FRQ-2026-Q2-B", "BC-MCQ-SAMPLE-017", "BC-MCQ-PE2012-002", "research/units/unit-09-parametric-polar-vector.md#9.1 Defining and Differentiating Parametric Equations", "research/question-analysis/question-archetypes.md#BC-QA-09001 Slope of the tangent to a parametric path at a time", "research/scoring/common-point-losses.md#Setup points", "research/exam/exam-structure.md#Section and part layout"]
}
```
