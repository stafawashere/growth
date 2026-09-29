---
title: LSN-CON-05011 Graph of a function reconstructed from its derivative graphs
research_date: 2026-09-29
status: designed
purpose: Authoring spec for the concept lesson on BC-CON-05011, reading the extrema, monotonicity and inflection of f from a graph of f prime and the constant a derivative leaves open, built from authoring_bundle("BC-CON-05011") and the research files it cites, so an author fills plan 15's lesson record without making a teaching decision.
---

# LSN-CON-05011 Graph of a function reconstructed from its derivative graphs

Concept BC-CON-05011 (skills BC-SKL-05040 to BC-SKL-05044), topic 5.8 of Unit 5. One archetype loads its skills, BC-QA-05009 (family function-derivative-graph-relationship, tagged [inferred] in research). Unit parents BC-CON-05004, 05007, 05008 (docs/lessons/unit-05/README.md, section 1).

## Prediction

pr-1, `mcq`, both bands, served first, on ex-1's draw. Stem: the graph of f prime is y = x^2/2 - 2, and the question asks where f has its inflection point. Key: x = 0, the vertex of the graph of f prime. Distractors: the crossings x = -2 and x = 2, which are the extrema of f, and the claim that the graph of f prime cannot decide it. The resolution states the correspondence in the record's words and says nothing about the student. Sources: BC-CON-05011 and the topic's 5.8 section (research/units/unit-05-analytical-applications-differentiation.md#5.8 Sketching Graphs of Functions and Their Derivatives). Tagged [inferred] in the record's `inferred` array.

## Orientation

Served text, from BC-CON-05011 `description_plain` and the topic's Assessment behaviour paragraph (research/units/unit-05-analytical-applications-differentiation.md#5.8 Sketching Graphs of Functions and Their Derivatives): a response names the plotted object, reads extrema of f where the graph of f prime crosses the axis and inflection where it turns, and states the reason about the graph of f prime. No count, no frequency.

## Key ideas

Two BC-EK ids: one core block for both bands, one extended block for the low band, to keep the brief form under 450 words.

- ki-1 (core, BC-EK-FUN-4A9, skills BC-SKL-05040, 05042). Paraphrase of Feature correspondence: a sign change of f prime marks an extremum of f, an extremum of f prime marks an inflection of f. No anchor quote, for length.
- ki-2 (extended, BC-EK-FUN-4A10, skills BC-SKL-05041, 05043, 05044). Paraphrase of Feature correspondence (f prime positive, f rising; f prime increasing, f concave up) and Vertical indeterminacy: f prime fixes f only up to a constant; one value of f fixes the curve (frq-23:8 per the topic paragraph). Anchor quote from ced:106, 19 words.

## Recognition

BC-QA-05009 (research/question-analysis/question-archetypes.md#BC-QA-05009 Relating the graphs of a function and its first two derivatives): `typical_wording` "sketch a possible graph of the function on the given interval", "which of the graphs shown could be the function, its derivative, and its second derivative"; `common_givens` two or three plotted curves, a table of signs, sometimes one known function value; `asked_to_produce` a sketch with the correct features or an assignment of roles. The signal: a caption or axis label naming the plot "the graph of f prime" while the question asks about f. Shape: MCQ (BC-MCQ-SAMPLE-011, BC-MCQ-PE2012-029, 033, 041, 045); FRQs ask for the features, scored as a list point and a reason point (sg-23:13, sg-25:17).

What says "not this concept": the plotted curve is f itself (read features directly), or three curves to sort (BC-CON-05012).
The contrast pair on st-1 comes from the paragraph above. `this` plots the graph of f prime and asks for features of f. `not_this` plots f itself, the near miss the "not this concept" line names: its features are read straight off the plotted curve (BC-CON-05004 and BC-CON-05007). `feature` is which function the plotted curve is.

## Method choice

One strategy block, both bands.

- st-1, BC-QA-05009. Method, `expected_solution_path[0]`: find the turning points of each curve, then match them with the zeros of the other. Rival, `wrong_approaches`: deciding the order from the vertical scale of the plots. Separating feature: a zero of f prime with a sign change sits under an extremum of f, whatever the scale. The reason is written about the graph of f prime (research/scoring/justification-requirements.md#Reasons tied to the object the prompt names). Not tagged inferred.
The strategy fields carry no leading label, because the reader prints Cue, First line, Rival and Separating feature itself. st-1 carries the contrast pair described under Recognition. The fields are cut to fit the brief cap once the prediction and the contrast are served.

## Solution path

- ex-1, BC-QA-05009, both bands, no calculator. Draw from `parameter_spec`: first_root -2, root_gap 4 (second_root 2), steepness 1/2, orientation 1, lift 1, lettering ABC, framing derivatives. The graph of f prime is the parabola y = x^2/2 - 2 [inferred: the spec's notes fix the zeros, not the formula]. No published BC-QA-05009 item carries this draw.
- Steps: f prime (new); its zeros (solve); the sign change at x = 2 (no value, the reason); the turning point of f prime, where its slope x is zero (new, solve); the answer pair (new). A fluent solver reads the zeros and the vertex off the graph and writes the two reasons.

## Scoring

BC-QA-05009 lists no `point_types`, so no what_a_reader_scores entry and no point tag. For the author: a reason that says "f changes concavity" or uses "the function" or "the graph" as subject does not earn the reason point where the graph of f prime is given (sg-25:17, sg-26:15; research/scoring/common-point-losses.md#Justification points).

## Traps

Six active errors meet the skills; the first four in the bundle's order are served: BC-ERR-05016, BC-ERR-05041, BC-ERR-05042, BC-ERR-05043. Low band all four; mid band the first two. BC-ERR-05044 and BC-ERR-05045 are left out by the cap of 4. All on ex-1's draw.

- err-BC-ERR-05016: f increasing reported on x > 0, where the graph of f prime rises. Possible reason, words from BC-MIS-05020.
- err-BC-ERR-05041: a derivative sketch with its extremum at a zero of f. Statement-shaped. Possible reason, words from BC-MIS-05011.
- err-BC-ERR-05042: extrema of f placed at x = 0, where f prime turns. Possible reason, words from BC-MIS-05011.
- err-BC-ERR-05043: inflection paired with the zeros of f prime. Possible reason, words from BC-MIS-05020.
All four blocks have `relation` distinct, so all four carry `fix_prompt` true: the student writes the right step before it is shown.

## Representations

None as a separate block. The topic's Representations paragraph names graph of f prime to a possible graph of f (BC-REP-02 to BC-REP-02); ki-1's figure and ki-2's interactive carry it.

## Prerequisite bridge

- BC-PRQ-05006, from its `description_plain` and `failure_signature`.

## Time

BC-QA-05009 is `either`, an MCQ or one FRQ feature question, so Section I Part A, 2.14 minutes per question (research/exam/exam-structure.md#Section and part layout) [inferred]. The minutes go on reading zeros and the vertex; no computation is required by the archetype's `invariant_structure`.

## Checks

- chk-1, completion of ex-1, both bands: the zeros -2 and 2 and the vertex at x = 0 given. Key (2, 0).
- chk-2, isomorph, both bands. Draw: first_root -3, root_gap 2, steepness 1, orientation -1, lift 0, lettering ACB, framing derivatives; f prime is y = -(x + 3)(x + 1). Key (-3, -2).
- chk-3, MCQ, low band. Draw: first_root 0, root_gap 2, steepness 1, orientation 1, lift 2, lettering CBA, framing derivatives; f prime is y = x^2 - 2x. Key: relative minimum at x = 2, inflection at x = 1. Distractors: minimum at x = 1 (BC-ERR-05042), f increasing on x > 1 (BC-ERR-05016), inflection at x = 0 and x = 2 (BC-ERR-05043).

## Delivery

- orientation: figure. Rule 3 on BC-REP-02 in BC-SKL-05040 to 05044 (docs/lessons/unit-05/README.md, section 6).
- ki-1: figure. Rule 3, not promoted: the correspondence is a fixed feature.
- ki-2: interactive, one slider for the added constant. Rule 3 promoted by BC-QA-05009 `difficulty_variables` "whether a known value is supplied to fix the sketch", with the question "which features stay fixed?".
- ex-1 and the four error blocks: step_reveal. Rule 1.
- pr-1: text. Rule 6; the figure is served on the orientation. Figure presence: the lesson already draws the orientation, ki-1 and ki-2, so no `no_figure_reason`.

## Band plan
- Low (full): pr-1, orientation, the bridge, ki-1, ki-2, st-1 with its contrast pair, ex-1, chk-1, the four error blocks, chk-2, chk-3. 690 words, 5.0 minutes (cap 900 and 6).
- Mid (brief): pr-1, orientation, the bridge, ki-1, st-1 with its contrast pair, ex-1, chk-1, err-BC-ERR-05016, err-BC-ERR-05041, chk-2. 447 words, 3.0 minutes (cap 450 and 3).
- Refresher: ki-1, the four error blocks, ex-1. No prediction and no check.

## Sources

- BC-CON-05011; BC-SKL-05040, BC-SKL-05041, BC-SKL-05042, BC-SKL-05043, BC-SKL-05044; BC-EK-FUN-4A9, BC-EK-FUN-4A10; ced:106
- BC-QA-05009; BC-MCQ-SAMPLE-011, BC-MCQ-PE2012-029, BC-MCQ-PE2012-033, BC-MCQ-PE2012-041, BC-MCQ-PE2012-045; sg-23:13, sg-25:17, sg-26:15
- BC-ERR-05016, BC-ERR-05041, BC-ERR-05042, BC-ERR-05043; BC-MIS-05011, BC-MIS-05020
- BC-PRQ-05006
- research/units/unit-05-analytical-applications-differentiation.md#5.8 Sketching Graphs of Functions and Their Derivatives
- research/question-analysis/question-archetypes.md#BC-QA-05009 Relating the graphs of a function and its first two derivatives
- research/scoring/justification-requirements.md#Reasons tied to the object the prompt names
- research/scoring/common-point-losses.md#Justification points
- research/exam/exam-structure.md#Section and part layout
- [inferred] Section I Part A for an either archetype. Settled by a calculator status on BC-QA-05009.
- [inferred] The formula of f prime from the draw. Settled by a formula in the BC-QA-05009 parameter_spec notes.
- [inferred] The figure and interactive modes. Settled by the modality A/B.
- [inferred] The prediction and the contrast stems, authored on ex-1's draw. Settled by the blind re-solve and a pretest measurement.

## Machine record

```json
{
 "id": "LSN-CON-05011",
 "kind": "concept",
 "target_id": "BC-CON-05011",
 "unit": "05",
 "skills": ["BC-SKL-05040", "BC-SKL-05041", "BC-SKL-05042", "BC-SKL-05043", "BC-SKL-05044"],
 "prediction": {"id": "pr-1", "stem": {"text": "Predict: the graph of \\(f'\\) is \\(y=\\frac{x^2}{2}-2\\). Where does \\(f\\) have an inflection point?", "command_verb": "predict"}, "format": "mcq", "options": [{"id": "A", "label": "At \\(x=-2\\) and \\(x=2\\)", "is_key": false}, {"id": "B", "label": "At \\(x=0\\)", "is_key": true}, {"id": "C", "label": "Cannot be found from \\(f'\\)", "is_key": false}], "resolution": "An inflection point of \\(f\\) sits where the graph of \\(f'\\) turns, at \\(x=0\\). The crossings mark extrema of \\(f\\).", "sources": ["BC-CON-05011", "research/units/unit-05-analytical-applications-differentiation.md#5.8 Sketching Graphs of Functions and Their Derivatives"]},
 "orientation": {"text": "A response reads \\(f\\) from the graph of \\(f'\\): extrema at crossings, inflection where it turns, reasons about \\(f'\\).", "sources": ["BC-CON-05011", "research/units/unit-05-analytical-applications-differentiation.md#5.8 Sketching Graphs of Functions and Their Derivatives"]},
 "key_ideas": [
  {"id": "ki-1", "ek_id": "BC-EK-FUN-4A9", "depth": "core", "text": "A sign-changing zero of \\(f'\\) is an extremum of \\(f\\). A turning point of the graph of \\(f'\\) is an inflection point of \\(f\\).", "notation": "graph of f; graph of f'", "quote": null, "sources": ["BC-EK-FUN-4A9", "ced:106", "research/units/unit-05-analytical-applications-differentiation.md#5.8 Sketching Graphs of Functions and Their Derivatives"]},
  {"id": "ki-2", "ek_id": "BC-EK-FUN-4A10", "depth": "extended", "text": "Where \\(f'>0\\), \\(f\\) rises; where \\(f'\\) is increasing, \\(f\\) is concave up. Rising of \\(f'\\) is about concavity, not about \\(f\\) rising. The graph of \\(f'\\) fixes the shape of \\(f\\) but not its height: any vertical shift has the same derivative. One given value of \\(f\\) pins the curve down.", "notation": "sketch a possible graph of f", "quote": {"text": "Graphical, numerical, and analytical information from f' and f\" can be used to predict and explain the behavior of f.", "source": "ced:106"}, "sources": ["BC-EK-FUN-4A10", "ced:106", "research/units/unit-05-analytical-applications-differentiation.md#5.8 Sketching Graphs of Functions and Their Derivatives"]}
 ],
 "strategy": [
  {"id": "st-1", "archetype_id": "BC-QA-05009", "cue": "Plotted curves or a sign table.", "method": "Match the turning points of each curve with the zeros of the other.", "rival": "Ordering the plots by vertical scale.", "separating_feature": "A sign change of \\(f'\\) marks an extremum of \\(f\\).", "sources": ["BC-QA-05009"], "evidence_tag": "verified", "contrast": {"this": {"text": "The graph of \\(f'\\) crosses the axis at \\(-2\\) and \\(2\\). Find the minimum and inflection of \\(f\\).", "archetype_id": "BC-QA-05009"}, "not_this": {"text": "The graph of \\(f\\) is \\(y=\\frac{x^2}{2}-2\\). Find its minimum.", "why_not": "The plotted curve is \\(f\\), read directly."}, "feature": "Which function the plotted curve is."}}
 ],
 "worked_examples": [
  {"id": "ex-1", "archetype_id": "BC-QA-05009", "bands": ["low", "mid"], "parameter_draw": {"first_root": -2, "root_gap": 4, "steepness": "1/2", "orientation": 1, "lift": 1, "lettering": "ABC", "framing": "derivatives"}, "problem": {"text": "The graph of \\(f'\\) is the parabola \\(y=\\frac{x^2}{2}-2\\). Find the \\(x\\)-coordinate of the relative minimum of \\(f\\) and of the inflection point of \\(f\\). Give reasons.", "command_verb": "find"}, "calculator_status": "no_calculator", "steps": [{"cue": "The plot is \\(f'\\); the question is about \\(f\\).", "why": "Read one derivative down.", "expr": "x**2/2 - 2", "relation": "new"}, {"cue": "Extrema of \\(f\\): where the graph of \\(f'\\) crosses the axis.", "why": "Zeros at \\(-2\\) and \\(2\\).", "expr": "FiniteSet(-2, 2)", "relation": "solve", "variable": "x"}, {"cue": "Minimum asked: which crossing goes from below to above?", "why": "At \\(x=2\\) the graph of \\(f'\\) changes from negative to positive: relative minimum."}, {"cue": "Inflection of \\(f\\): where the graph of \\(f'\\) turns.", "why": "The slope of the parabola is \\(x\\).", "expr": "x", "relation": "new"}, {"cue": "The vertex of the graph of \\(f'\\).", "why": "At \\(x=0\\) the graph of \\(f'\\) changes from decreasing to increasing.", "expr": "0", "relation": "solve", "variable": "x"}, {"cue": "Both inputs asked.", "why": "Minimum at 2, inflection at 0.", "expr": "Tuple(2, 0)", "relation": "new"}], "answer": {"form": "symbolic", "expr": "Tuple(2, 0)"}}
 ],
 "what_a_reader_scores": [],
 "common_errors": [
  {"error_id": "BC-ERR-05016", "observed_behavior": "The response reports concavity where monotonicity was asked for, or reports increase of the function where the derivative graph is rising.", "scoring_consequence": "The intervals reported belong to the other question and the reason point is unavailable.", "wrong_step": {"text": "The graph of \\(f'\\) rises on \\(x>0\\), so \\(f\\) increases there.", "expr": "Interval.open(0, oo)"}, "right_step": {"text": "\\(f'>0\\) on \\(x<-2\\) and \\(x>2\\), so \\(f\\) increases there.", "expr": "Union(Interval.open(-oo, -2), Interval.open(2, oo))"}, "relation": "distinct", "possible_reason": {"misconception_id": "BC-MIS-05020", "text": "does not distinguish rising from bending upward"}, "sources": ["BC-ERR-05016", "BC-MIS-05020"], "fix_prompt": true},
  {"error_id": "BC-ERR-05041", "observed_behavior": "The response places the extrema of the derivative sketch where the original curve crosses the axis.", "scoring_consequence": "The sketch fails every feature check that follows.", "wrong_step": {"text": "Sketching \\(f'\\) from \\(f\\): an extremum of \\(f'\\) drawn where \\(f\\) crosses the axis.", "expr": "extremum_of_f_prime_at_zero_of_f"}, "right_step": {"text": "The extremum of \\(f'\\) sits at the inflection point of \\(f\\), \\(x=0\\).", "expr": "extremum_of_f_prime_at_inflection_of_f"}, "relation": "distinct", "possible_reason": {"misconception_id": "BC-MIS-05011", "text": "reading features of whatever curve is drawn"}, "sources": ["BC-ERR-05041", "BC-MIS-05011"], "fix_prompt": true},
  {"error_id": "BC-ERR-05042", "observed_behavior": "The response draws the function with extrema where the derivative graph turns rather than where it crosses the axis.", "scoring_consequence": "Extrema and points of inflection are interchanged throughout the sketch.", "wrong_step": {"text": "Extremum of \\(f\\) at the vertex of the graph of \\(f'\\).", "expr": "FiniteSet(0)"}, "right_step": {"text": "Extrema of \\(f\\) at the crossings of the graph of \\(f'\\).", "expr": "FiniteSet(-2, 2)"}, "relation": "distinct", "possible_reason": {"misconception_id": "BC-MIS-05011", "text": "reading features of whatever curve is drawn"}, "sources": ["BC-ERR-05042", "BC-MIS-05011"], "fix_prompt": true},
  {"error_id": "BC-ERR-05043", "observed_behavior": "The response pairs a point of inflection with a zero of the first derivative, or an extremum with a zero of the second.", "scoring_consequence": "Every answer that rests on the correspondence is displaced by one derivative.", "wrong_step": {"text": "Inflection of \\(f\\) at the zeros of \\(f'\\).", "expr": "FiniteSet(-2, 2)"}, "right_step": {"text": "Inflection of \\(f\\) where the graph of \\(f'\\) turns.", "expr": "FiniteSet(0)"}, "relation": "distinct", "possible_reason": {"misconception_id": "BC-MIS-05020", "text": "the sign and the direction of the derivative are used interchangeably"}, "sources": ["BC-ERR-05043", "BC-MIS-05020"], "fix_prompt": true}
 ],
 "representations": null,
 "prerequisite_bridges": [
  {"prq_id": "BC-PRQ-05006", "text": "Name the plotted curve first."}
 ],
 "time": {"exam_part": "I-A", "budget_minutes": 2.14, "source": "research/exam/exam-structure.md#Section and part layout", "written_steps": {"ex-1": [2, 3, 5, 6]}, "skipped_steps": {"ex-1": [1, 4]}},
 "checks": [
  {"id": "chk-1", "check_kind": "completion", "format": "short_answer", "bands": ["low", "mid"], "archetype_id": "BC-QA-05009", "parameter_draw": {"first_root": -2, "root_gap": 4, "steepness": "1/2", "orientation": 1, "lift": 1, "lettering": "ABC", "framing": "derivatives"}, "completes": "ex-1", "stem": {"text": "\\(f'\\) is negative on \\((-2, 2)\\), zero at \\(-2\\) and \\(2\\), and turns at \\(0\\). Give (minimum, inflection) of \\(f\\).", "command_verb": "find"}, "key": {"form": "symbolic", "expr": "Tuple(2, 0)"}, "steps": [{"text": "The graph of \\(f'\\) goes from negative to positive at 2.", "expr": "x**2/2 - 2", "relation": "new"}, {"text": "Crossings.", "expr": "FiniteSet(-2, 2)", "relation": "solve", "variable": "x"}, {"text": "Minimum at 2; the graph of \\(f'\\) turns at 0.", "expr": "Tuple(2, 0)", "relation": "new"}], "calculator_status": "no_calculator", "skills": ["BC-SKL-05043"]},
  {"id": "chk-2", "check_kind": "isomorph", "format": "short_answer", "bands": ["low", "mid"], "archetype_id": "BC-QA-05009", "parameter_draw": {"first_root": -3, "root_gap": 2, "steepness": "1", "orientation": -1, "lift": 0, "lettering": "ACB", "framing": "derivatives"}, "stem": {"text": "The graph of \\(f'\\) is \\(y=-(x+3)(x+1)\\). Give (relative minimum of \\(f\\), inflection of \\(f\\)).", "command_verb": "find"}, "key": {"form": "symbolic", "expr": "Tuple(-3, -2)"}, "steps": [{"text": "The graph of \\(f'\\).", "expr": "-(x + 3)*(x + 1)", "relation": "new"}, {"text": "Crossings at \\(-3\\) and \\(-1\\); negative to positive at \\(-3\\).", "expr": "FiniteSet(-3, -1)", "relation": "solve", "variable": "x"}, {"text": "Slope of the graph of \\(f'\\).", "expr": "-2*x - 4", "relation": "new"}, {"text": "It turns at \\(-2\\).", "expr": "-2", "relation": "solve", "variable": "x"}, {"text": "The pair.", "expr": "Tuple(-3, -2)", "relation": "new"}], "calculator_status": "no_calculator", "skills": ["BC-SKL-05043"]},
  {"id": "chk-3", "check_kind": "mcq", "format": "mcq", "bands": ["low"], "archetype_id": "BC-QA-05009", "parameter_draw": {"first_root": 0, "root_gap": 2, "steepness": "1", "orientation": 1, "lift": 2, "lettering": "CBA", "framing": "derivatives"}, "stem": {"text": "The graph of \\(f'\\) is \\(y=x^2-2x\\). Which statement about \\(f\\) is true?", "command_verb": "identify"}, "key": {"form": "statement", "expr": "minimum_at_2_inflection_at_1"}, "steps": [{"text": "Crossings of the graph of \\(f'\\).", "expr": "x**2 - 2*x", "relation": "new"}, {"text": "At 0 and 2; negative to positive at 2.", "expr": "FiniteSet(0, 2)", "relation": "solve", "variable": "x"}, {"text": "It turns at 1.", "expr": "2*x - 2", "relation": "new"}, {"text": "Vertex.", "expr": "1", "relation": "solve", "variable": "x"}], "options": [{"id": "A", "is_key": false, "label": "\\(f\\) has a relative minimum at \\(x=1\\).", "error_path": "BC-ERR-05042", "derivation": "the extremum placed where the graph of f' turns"}, {"id": "B", "is_key": false, "label": "\\(f\\) is increasing on \\(x>1\\).", "error_path": "BC-ERR-05016", "derivation": "f read as increasing where the graph of f' rises"}, {"id": "C", "is_key": true, "label": "\\(f\\) has a relative minimum at \\(x=2\\) and an inflection point at \\(x=1\\).", "error_path": null}, {"id": "D", "is_key": false, "label": "\\(f\\) has inflection points at \\(x=0\\) and \\(x=2\\).", "error_path": "BC-ERR-05043", "derivation": "inflection paired with the zeros of f'"}], "calculator_status": "no_calculator", "skills": ["BC-SKL-05043"]}
 ],
 "delivery": [
  {"block": "pr-1", "mode": "text", "reason": "rule 6: a question on a symbolic curve; the figure is served on the orientation", "sources": ["BC-CON-05011"]},
  {"block": "orientation", "mode": "figure", "reason": "rule 3: BC-REP-02 on BC-SKL-05040 to 05044; a fixed feature, not promoted", "sources": ["BC-SKL-05040"], "spec": {"kind": "graph", "representations": ["BC-REP-02"], "curves": [{"expr": "x**2/2 - 2", "domain": [-4, 4]}], "window": {"x": [-4, 4], "y": [-3, 5]}, "labels": [{"text": "graph of f'", "placement": "inside"}, {"text": "crosses: extremum of f", "placement": "inside"}, {"text": "turns: inflection of f", "placement": "inside"}]}, "fallback": "the same parabola, static, with the two crossings and the vertex marked and each label inside", "keyboard": "none needed; no control"},
  {"block": "ki-1", "mode": "figure", "reason": "rule 3: BC-REP-02 on BC-SKL-05040 and 05042; the correspondence is a fixed feature, so static", "sources": ["BC-SKL-05040", "BC-SKL-05042"], "spec": {"kind": "stacked_graphs", "representations": ["BC-REP-02"], "panels": [{"curve": "x**3/6 - 2*x + 1", "name": "f"}, {"curve": "x**2/2 - 2", "name": "f'"}], "window": {"x": [-4, 4]}, "guides": ["vertical line at x = -2", "vertical line at x = 0", "vertical line at x = 2"], "labels": [{"text": "f' crosses: f max at -2, f min at 2", "placement": "inside"}, {"text": "f' turns: f inflects at 0", "placement": "inside"}]}, "fallback": "the two panels, static, with the three guide lines and labels inside", "keyboard": "none needed; no control"},
  {"block": "ki-2", "mode": "interactive", "reason": "rule 3 promoted: BC-REP-02 on BC-SKL-05041, 05043, 05044; BC-QA-05009 difficulty_variables 'whether a known value is supplied to fix the sketch' names a varying quantity and the stem asks for a reading", "sources": ["BC-SKL-05044", "BC-QA-05009"], "spec": {"kind": "stacked_graphs", "representations": ["BC-REP-02"], "panels": [{"curve": "x**3/6 - 2*x + C", "name": "f"}, {"curve": "x**2/2 - 2", "name": "f'"}], "window": {"x": [-4, 4]}, "controls": [{"type": "slider", "parameter": "C", "range": [-3, 3], "step": 1, "start": 1}], "labels": [{"text": "f' unchanged for every C", "placement": "inside"}, {"text": "extrema and inflection stay at the same x", "placement": "inside"}], "question": "Which features of f stay fixed as C moves, and what one fact would fix C?"}, "fallback": "three static copies of the f panel at C = -2, 1 and 3 above one f' panel, labels inside", "keyboard": "Tab focuses the slider; left and right arrow keys change C by 1; the reading is announced"},
  {"block": "ex-1", "mode": "step_reveal", "reason": "rule 1", "sources": []},
  {"block": "err-BC-ERR-05016", "mode": "step_reveal", "reason": "rule 1", "sources": []},
  {"block": "err-BC-ERR-05041", "mode": "step_reveal", "reason": "rule 1", "sources": []},
  {"block": "err-BC-ERR-05042", "mode": "step_reveal", "reason": "rule 1", "sources": []},
  {"block": "err-BC-ERR-05043", "mode": "step_reveal", "reason": "rule 1", "sources": []}
 ],
 "refresher": ["ki-1", "err-BC-ERR-05016", "err-BC-ERR-05041", "err-BC-ERR-05042", "err-BC-ERR-05043", "ex-1"],
 "read_minutes": {"full": 5.0, "brief": 3.0},
 "word_count": {"full": 690, "brief": 447},
 "research_lines": [
  {"file": "research/scoring/justification-requirements.md", "line": "the reason point is earned only by reasoning about the graphed object"}
 ],
 "inferred": [
  {"claim": "BC-QA-05009 has calculator_status either; the lesson places it in Section I Part A at 2.14 minutes.", "settles": "A single calculator status on BC-QA-05009 or an official example fixing its part."},
  {"claim": "The formula of f' for each draw (y = orientation times steepness times (x - first_root)(x - second_root)) is read from the parameter_spec notes, which fix only the zeros.", "settles": "A formula for the plotted curves in the BC-QA-05009 parameter_spec."},
  {"claim": "The orientation and ki-1 are static figures and ki-2 an interactive slider.", "settles": "The modality A/B in the build plan: skip rate and time to first credited success by mode."},
  {"claim": "The prediction and the contrast stems are authored on ex-1's draw and on the archetype's typical wording; no record supplies them.", "settles": "The blind re-solve of the prediction key and a pretest measurement of the prediction's option choices."}
 ],
 "sources": ["BC-CON-05011", "BC-SKL-05040", "BC-SKL-05041", "BC-SKL-05042", "BC-SKL-05043", "BC-SKL-05044", "BC-EK-FUN-4A9", "BC-EK-FUN-4A10", "ced:106", "BC-QA-05009", "sg-23:13", "sg-25:17", "sg-26:15", "BC-ERR-05016", "BC-ERR-05041", "BC-ERR-05042", "BC-ERR-05043", "BC-MIS-05011", "BC-MIS-05020", "BC-PRQ-05006", "research/units/unit-05-analytical-applications-differentiation.md#5.8 Sketching Graphs of Functions and Their Derivatives", "research/question-analysis/question-archetypes.md#BC-QA-05009 Relating the graphs of a function and its first two derivatives", "research/scoring/justification-requirements.md#Reasons tied to the object the prompt names", "research/scoring/common-point-losses.md#Justification points", "research/exam/exam-structure.md#Section and part layout"]
}
```
