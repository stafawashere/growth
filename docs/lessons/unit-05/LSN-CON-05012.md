---
title: LSN-CON-05012 Simultaneous reading of a function and its first two derivatives
research_date: 2026-09-29
status: designed
purpose: Authoring spec for the concept lesson on BC-CON-05012, assigning the roles f, f prime and f double prime to three related objects and reading one from another, built from authoring_bundle("BC-CON-05012") and the research files it cites, so an author fills plan 15's lesson record without making a teaching decision.
---

# LSN-CON-05012 Simultaneous reading of a function and its first two derivatives

Concept BC-CON-05012 (skills BC-SKL-05045 to BC-SKL-05048), topic 5.9 of Unit 5. One archetype loads its skills, BC-QA-05009 (family function-derivative-graph-relationship, tagged [inferred] in research). Unit parents BC-CON-05004, 05007, 05011 (docs/lessons/unit-05/README.md, section 1).

## Prediction

pr-1, `mcq`, both bands, served first, on ex-1's draw. Stem: curve B has horizontal tangents at x = -1 and x = 2 and curve C crosses the axis there; how are B and C related. Key: C is the derivative of B. Distractors: B is the derivative of C, and C is the second derivative of B. The resolution states the rule in the record's words and says nothing about the student. Sources: BC-CON-05012 and the topic's 5.9 section (research/units/unit-05-analytical-applications-differentiation.md#5.9 Connecting a Function, Its First Derivative, and Its Second Derivative). Tagged [inferred] in the record's `inferred` array.

## Orientation

Served text, from BC-CON-05012 `description_plain` and the topic's Assessment behaviour paragraph (research/units/unit-05-analytical-applications-differentiation.md#5.9 Connecting a Function, Its First Derivative, and Its Second Derivative): a response assigns f, f prime and f double prime by matching turning points of one object with sign-changing zeros of the next, twice, and names which object each reason is about. No count, no frequency.

## Key ideas

All four skills map to BC-EK-FUN-4A11 (ced:107): one core block, both bands.

- ki-1 (core). Paraphrase of Three way correspondence and Identification rule: extrema of f at sign changes of f prime, inflection of f at sign changes of f double prime (the extrema of f prime), concavity of f from the sign of f double prime; the rule applied twice orders three curves. Anchor quote from ced:107, 13 words.

## Recognition

BC-QA-05009 (research/question-analysis/question-archetypes.md#BC-QA-05009 Relating the graphs of a function and its first two derivatives): `typical_wording` "which of the graphs shown could be the function, its derivative, and its second derivative"; `common_givens` two or three plotted curves, or a table of signs; `asked_to_produce` an assignment of roles. The signal: three unlabelled curves on one set of axes, or a sign table with rows for f prime and f double prime. Shape: MCQ (BC-MCQ-SAMPLE-011, BC-MCQ-PE2012-029, 033, 041, 045); in an FRQ, one object is given and a feature of another is asked, and a confusion of the plotted object is penalised (sg-25:16, sg-25:17).

What says "not this concept": only f prime plotted and a sketch of f asked (BC-CON-05011), or one feature of f asked from the graph of f prime alone (BC-QA-05004, BC-CON-05007).
The contrast pair on st-1 comes from the paragraph above. `this` gives three lettered curves to sort. `not_this` gives only the graph of f prime and asks where f is concave down, the BC-QA-05004 `typical_wording` "on what open intervals, if any, is the graph of the function concave down" from outside this archetype (BC-CON-05007): one curve read for one feature of f, nothing sorted. `feature` is how many curves are plotted and what is asked of them.

## Method choice

One strategy block, both bands.

- st-1, BC-QA-05009. Method, `expected_solution_path[0]`: find the turning points of each curve. Rival, `wrong_approaches`: deciding the order from the vertical scale of the plots. Separating feature: the curve whose sign-changing zeros sit under another's turning points is that curve's derivative; scale plays no part. Tagged inferred (the archetype record is inferred).
The strategy fields carry no leading label, because the reader prints Cue, First line, Rival and Separating feature itself. st-1 carries the contrast pair described under Recognition. The fields, the orientation, the key idea and the bridge are cut to fit the brief cap once the prediction and the contrast are served; the key idea keeps its anchor quote.

## Solution path

- ex-1, BC-QA-05009, both bands, no calculator. Draw: first_root -1, root_gap 3 (second_root 2), steepness 1, orientation -1, lift 0, lettering BCA, framing derivatives. So f prime is y = -(x + 1)(x - 2) and f double prime is y = 1 - 2x [inferred: the spec's notes fix the zeros, not the formula]; lettering BCA puts f on B, f prime on C and f double prime on A, the order the published items read it in. No published BC-QA-05009 item carries this draw.
- Steps follow `expected_solution_path`: curve C (new); its zeros, the turning points of B (solve); C is the derivative of B (no value); curve A (new); its zero, the turning point of C (solve); the assignment (no value). A fluent solver reads the four features off the figure and writes the one-line assignment with one pairing as reason.

## Scoring

BC-QA-05009 lists no `point_types`, so no what_a_reader_scores entry and no point tag. For the author: the FRQ forms score the features with the reason about the plotted object (sg-25:17; research/scoring/justification-requirements.md#Reasons tied to the object the prompt names).

## Traps

Four active errors, in the bundle's order: BC-ERR-05046, BC-ERR-05047, BC-ERR-05048, BC-ERR-05049. Low band all four; mid band the first two. All on ex-1's draw.

- err-BC-ERR-05046: B and A exchanged. Statement-shaped. Possible reason, words from BC-MIS-05011.
- err-BC-ERR-05047: concave up where f double prime decreases (everywhere) against where it is positive (x < 1/2). Possible reason, words from BC-MIS-05020.
- err-BC-ERR-05048: the sign table cut at zeros of f. Statement-shaped. Possible reason, words from BC-MIS-05010.
- err-BC-ERR-05049: decrease claimed on a whole interval from three tabulated values of f prime, false between the entries. Statement-shaped. Possible reason, words from BC-MIS-05026.
All four blocks have `relation` distinct, so all four carry `fix_prompt` true: the student writes the right step before it is shown.

## Representations

One block, low band: the sign table for ex-1's draw, from the topic's Representations paragraph (a sign table to a description of shape, BC-REP-03 to BC-REP-04). Cut at -1, 1/2 and 2, the zeros of f prime and f double prime.

## Prerequisite bridge

- BC-PRQ-06005, from its `description_plain` and `failure_signature`.

## Time

BC-QA-05009 is `either`, so Section I Part A, 2.14 minutes per question (research/exam/exam-structure.md#Section and part layout) [inferred]. The minutes go on reading four features; nothing is computed (the archetype's `invariant_structure`).

## Checks

- chk-1, completion of ex-1, both bands: the two pairings given; the student writes the assignment. Key: B is f, C is f prime, A is f double prime.
- chk-2, isomorph, both bands. Draw: first_root -4, root_gap 5, steepness 1/3, orientation 1, lift -1, lettering CAB, framing derivatives. Key: C is f, A is f prime, B is f double prime.
- chk-3, MCQ, low band. Draw: first_root 1, root_gap 2, steepness 1/2, orientation 1, lift -2, lettering BAC, framing derivatives. Key: B is f, C is f double prime, f concave up where C is positive. Distractors: B and C exchanged (BC-ERR-05046), concave up where C decreases (BC-ERR-05047), table cut where B crosses the axis (BC-ERR-05048).

## Delivery

- orientation: figure. Rule 4 on BC-REP-02 in BC-SKL-05045 (docs/lessons/unit-05/README.md, section 6).
- ki-1: interactive, three stacked graphs with one point sliding along x. Rule 4 promoted by BC-QA-05009 `difficulty_variables` "whether three objects are in play rather than two".
- representations: table. Rule 5 on BC-REP-03 in BC-SKL-05047, 05048.
- ex-1 and the four error blocks: step_reveal. Rule 1.
- pr-1: text. Rule 6; the three curves are drawn on the orientation. Figure presence: the lesson already draws the orientation, ki-1 and the table, so no `no_figure_reason`.

## Band plan
- Low (full): pr-1, orientation, the bridge, ki-1, st-1 with its contrast pair, ex-1, chk-1, the four error blocks, chk-2, representations, chk-3. 700 words, 5.0 minutes (cap 900 and 6).
- Mid (brief): pr-1, orientation, the bridge, ki-1, st-1 with its contrast pair, ex-1, chk-1, err-BC-ERR-05046, err-BC-ERR-05047, chk-2. 448 words, 3.0 minutes (cap 450 and 3).
- Refresher: ki-1, the four error blocks, ex-1. No prediction and no check.

## Sources

- BC-CON-05012; BC-SKL-05045, BC-SKL-05046, BC-SKL-05047, BC-SKL-05048; BC-EK-FUN-4A11; ced:107
- BC-QA-05004, BC-CON-05007 (the not-this stem of the contrast pair); research/question-analysis/question-archetypes.md#BC-QA-05004 Intervals of concavity from derivative information with a reason
- BC-QA-05009; BC-MCQ-SAMPLE-011, BC-MCQ-PE2012-029, BC-MCQ-PE2012-033, BC-MCQ-PE2012-041, BC-MCQ-PE2012-045; sg-25:16, sg-25:17
- BC-ERR-05046, BC-ERR-05047, BC-ERR-05048, BC-ERR-05049; BC-MIS-05011, BC-MIS-05020, BC-MIS-05010, BC-MIS-05026
- BC-PRQ-06005
- research/units/unit-05-analytical-applications-differentiation.md#5.9 Connecting a Function, Its First Derivative, and Its Second Derivative
- research/question-analysis/question-archetypes.md#BC-QA-05009 Relating the graphs of a function and its first two derivatives
- research/scoring/justification-requirements.md#Reasons tied to the object the prompt names
- research/exam/exam-structure.md#Section and part layout
- [inferred] Section I Part A for an either archetype. Settled by a calculator status on BC-QA-05009.
- [inferred] The formulas of the curves from the draw. Settled by formulas in the BC-QA-05009 parameter_spec notes.
- [inferred] The figure, interactive and table modes. Settled by the modality A/B.
- [inferred] The prediction and the contrast stems, authored on ex-1's draw. Settled by the blind re-solve and a pretest measurement.

## Machine record

```json
{
 "id": "LSN-CON-05012",
 "kind": "concept",
 "target_id": "BC-CON-05012",
 "unit": "05",
 "skills": ["BC-SKL-05045", "BC-SKL-05046", "BC-SKL-05047", "BC-SKL-05048"],
 "prediction": {"id": "pr-1", "stem": {"text": "Curve B has horizontal tangents at \\(x=-1\\) and \\(x=2\\), and curve C crosses the axis there. How are B and C related?", "command_verb": "predict"}, "format": "mcq", "options": [{"id": "A", "label": "C is the derivative of B", "is_key": true}, {"id": "B", "label": "B is the derivative of C", "is_key": false}, {"id": "C", "label": "C is the second derivative of B", "is_key": false}], "resolution": "A curve crossing where B has horizontal tangents is its derivative. Here C is \\(f'\\) and B is \\(f\\).", "sources": ["BC-CON-05012", "research/units/unit-05-analytical-applications-differentiation.md#5.9 Connecting a Function, Its First Derivative, and Its Second Derivative"]},
 "orientation": {"text": "A response matches turning points with zeros, twice, and names the object each reason is about.", "sources": ["BC-CON-05012", "research/units/unit-05-analytical-applications-differentiation.md#5.9 Connecting a Function, Its First Derivative, and Its Second Derivative"]},
 "key_ideas": [
  {"id": "ki-1", "ek_id": "BC-EK-FUN-4A11", "depth": "core", "text": "Extrema of \\(f\\) sit where \\(f'\\) changes sign; inflection points where \\(f''\\) does, at the turning points of \\(f'\\). A curve whose zeros sit under another's turning points is its derivative.", "notation": "f, f', f''", "quote": {"text": "Key features of the graphs of f, f', and f\" are related to one another.", "source": "ced:107"}, "sources": ["BC-EK-FUN-4A11", "ced:107", "research/units/unit-05-analytical-applications-differentiation.md#5.9 Connecting a Function, Its First Derivative, and Its Second Derivative"]}
 ],
 "strategy": [
  {"id": "st-1", "archetype_id": "BC-QA-05009", "cue": "Two or three plotted curves.", "method": "Find the turning points of each curve.", "rival": "Ordering the plots by vertical scale.", "separating_feature": "Zeros under a curve's turning points mark its derivative.", "sources": ["BC-QA-05009"], "evidence_tag": "inferred", "contrast": {"this": {"text": "Curves A, B, C are \\(f\\), \\(f'\\), \\(f''\\) in some order. C crosses where B turns. Assign the roles.", "archetype_id": "BC-QA-05009"}, "not_this": {"text": "Only \\(f'\\) is plotted. On what intervals is \\(f\\) concave down?", "why_not": "One curve, read for concavity."}, "feature": "Three curves to sort, or one to read."}}
 ],
 "worked_examples": [
  {"id": "ex-1", "archetype_id": "BC-QA-05009", "bands": ["low", "mid"], "parameter_draw": {"first_root": -1, "root_gap": 3, "steepness": "1", "orientation": -1, "lift": 0, "lettering": "BCA", "framing": "derivatives"}, "problem": {"text": "Curves A, B, C are \\(f\\), \\(f'\\), \\(f''\\) in some order. B has horizontal tangents at \\(x=-1\\) and \\(x=2\\). C is \\(y=-(x+1)(x-2)\\). A is \\(y=1-2x\\). Identify each.", "command_verb": "identify"}, "calculator_status": "no_calculator", "steps": [{"cue": "B turns at \\(-1\\) and \\(2\\).", "why": "Which curve crosses the axis there?", "expr": "-(x + 1)*(x - 2)", "relation": "new"}, {"cue": "Zeros of C.", "why": "C changes sign at \\(-1\\) and \\(2\\).", "expr": "FiniteSet(-1, 2)", "relation": "solve", "variable": "x"}, {"cue": "C's zeros sit under B's turning points.", "why": "So C is the derivative of B."}, {"cue": "Apply the rule again: C turns at its vertex.", "why": "Which curve crosses there?", "expr": "1 - 2*x", "relation": "new"}, {"cue": "Zero of A.", "why": "A changes sign at \\(\\frac{1}{2}\\), the vertex of C.", "expr": "1/2", "relation": "solve", "variable": "x"}, {"cue": "Two links: B to C, C to A.", "why": "B is \\(f\\), C is \\(f'\\), A is \\(f''\\)."}], "answer": {"form": "statement", "expr": "B_is_f_C_is_f1_A_is_f2"}}
 ],
 "what_a_reader_scores": [],
 "common_errors": [
  {"error_id": "BC-ERR-05046", "observed_behavior": "The response labels the function as the second derivative and the second derivative as the function.", "scoring_consequence": "Every feature question about the triple is answered about the wrong object.", "wrong_step": {"text": "A is \\(f\\), C is \\(f'\\), B is \\(f''\\).", "expr": "A_is_f_C_is_f1_B_is_f2"}, "right_step": {"text": "B is \\(f\\), C is \\(f'\\), A is \\(f''\\).", "expr": "B_is_f_C_is_f1_A_is_f2"}, "relation": "distinct", "possible_reason": {"misconception_id": "BC-MIS-05011", "text": "reading features of whatever curve is drawn"}, "sources": ["BC-ERR-05046", "BC-MIS-05011"], "fix_prompt": true},
  {"error_id": "BC-ERR-05047", "observed_behavior": "The response states that the graph is concave up where the second derivative is decreasing rather than positive.", "scoring_consequence": "The concavity claim is wrong and any inflection list built from it inherits the error.", "wrong_step": {"text": "\\(f''\\) decreases everywhere, so concave up everywhere.", "expr": "Interval(-oo, oo)"}, "right_step": {"text": "\\(f''=1-2x>0\\) for \\(x<\\frac{1}{2}\\).", "expr": "Interval.open(-oo, 1/2)"}, "relation": "distinct", "possible_reason": {"misconception_id": "BC-MIS-05020", "text": "the sign and the direction of the derivative are used interchangeably"}, "sources": ["BC-ERR-05047", "BC-MIS-05020"], "fix_prompt": true},
  {"error_id": "BC-ERR-05048", "observed_behavior": "The response partitions the number line at the zeros of the function instead of at the zeros of its derivatives.", "scoring_consequence": "The partition does not align with the sign changes that matter, so the reported behaviour is wrong.", "wrong_step": {"text": "Sign table cut where B crosses the axis.", "expr": "cut_at_zeros_of_f"}, "right_step": {"text": "Cut at \\(-1\\), \\(\\frac{1}{2}\\), \\(2\\), the zeros of \\(f'\\) and \\(f''\\).", "expr": "cut_at_zeros_of_f1_and_f2"}, "relation": "distinct", "possible_reason": {"misconception_id": "BC-MIS-05010", "text": "decides increase and decrease from whether the function values are positive or negative"}, "sources": ["BC-ERR-05048", "BC-MIS-05010"], "fix_prompt": true},
  {"error_id": "BC-ERR-05049", "observed_behavior": "The response claims monotonicity or concavity across a whole interval from three tabulated derivative values.", "scoring_consequence": "The claim exceeds what the data support and cannot earn a justification point.", "wrong_step": {"text": "\\(f'(-2)=-4\\), \\(f'(2.5)=-1.75\\), \\(f'(3)=-4\\), so \\(f\\) decreases on \\([-2,3]\\).", "expr": "decreasing_on_whole_interval"}, "right_step": {"text": "The table gives \\(f'<0\\) at three inputs only; between them \\(f'>0\\) on \\((-1,2)\\), so \\(f\\) rises there.", "expr": "negative_at_listed_inputs_only"}, "relation": "distinct", "possible_reason": {"misconception_id": "BC-MIS-05026", "text": "treats a finite table of derivative values as a full description of the function"}, "sources": ["BC-ERR-05049", "BC-MIS-05026"], "fix_prompt": true}
 ],
 "representations": {"text": "The sign table cuts at \\(-1\\), \\(\\frac{1}{2}\\), \\(2\\). Each piece carries the sign of \\(f'\\) and of \\(f''\\), read together as rising or falling and concave up or down.", "figure": {"kind": "table", "representations": ["BC-REP-03"], "columns": ["x", "x < -1", "-1 < x < 1/2", "1/2 < x < 2", "x > 2"], "rows": [["f'", "negative", "positive", "positive", "negative"], ["f''", "positive", "positive", "negative", "negative"], ["f", "falling, concave up", "rising, concave up", "rising, concave down", "falling, concave down"]], "labels": [{"text": "cuts at zeros of f' and f'' only", "placement": "inside"}]}, "sources": ["BC-SKL-05047", "research/units/unit-05-analytical-applications-differentiation.md#5.9 Connecting a Function, Its First Derivative, and Its Second Derivative"]},
 "prerequisite_bridges": [
  {"prq_id": "BC-PRQ-06005", "text": "Name which curve is which first."}
 ],
 "time": {"exam_part": "I-A", "budget_minutes": 2.14, "source": "research/exam/exam-structure.md#Section and part layout", "written_steps": {"ex-1": [3, 6]}, "skipped_steps": {"ex-1": [1, 2, 4, 5]}},
 "checks": [
  {"id": "chk-1", "check_kind": "completion", "format": "short_answer", "bands": ["low", "mid"], "archetype_id": "BC-QA-05009", "parameter_draw": {"first_root": -1, "root_gap": 3, "steepness": "1", "orientation": -1, "lift": 0, "lettering": "BCA", "framing": "derivatives"}, "completes": "ex-1", "stem": {"text": "C crosses the axis where B turns; A crosses where C turns. Assign \\(f\\), \\(f'\\), \\(f''\\).", "command_verb": "identify"}, "key": {"form": "statement", "expr": "B_is_f_C_is_f1_A_is_f2"}, "steps": [{"text": "Zeros of C.", "expr": "-(x + 1)*(x - 2)", "relation": "new"}, {"text": "At the turning points of B.", "expr": "FiniteSet(-1, 2)", "relation": "solve", "variable": "x"}], "calculator_status": "no_calculator", "skills": ["BC-SKL-05045"]},
  {"id": "chk-2", "check_kind": "isomorph", "format": "short_answer", "bands": ["low", "mid"], "archetype_id": "BC-QA-05009", "parameter_draw": {"first_root": -4, "root_gap": 5, "steepness": "1/3", "orientation": 1, "lift": -1, "lettering": "CAB", "framing": "derivatives"}, "stem": {"text": "C turns at \\(x=-4\\) and \\(x=1\\). A is \\(y=\\frac{1}{3}(x+4)(x-1)\\). B crosses the axis only at \\(x=-\\frac{3}{2}\\). Assign roles.", "command_verb": "identify"}, "key": {"form": "statement", "expr": "C_is_f_A_is_f1_B_is_f2"}, "steps": [{"text": "A.", "expr": "(x + 4)*(x - 1)/3", "relation": "new"}, {"text": "A crosses at C's turning points.", "expr": "FiniteSet(-4, 1)", "relation": "solve", "variable": "x"}, {"text": "Slope of A.", "expr": "(2*x + 3)/3", "relation": "new"}, {"text": "A turns where B crosses.", "expr": "-3/2", "relation": "solve", "variable": "x"}], "calculator_status": "no_calculator", "skills": ["BC-SKL-05045"]},
  {"id": "chk-3", "check_kind": "mcq", "format": "mcq", "bands": ["low"], "archetype_id": "BC-QA-05009", "parameter_draw": {"first_root": 1, "root_gap": 2, "steepness": "1/2", "orientation": 1, "lift": -2, "lettering": "BAC", "framing": "derivatives"}, "stem": {"text": "B turns at \\(x=1\\) and \\(x=3\\). A crosses the axis at 1 and 3 and turns at 2. C crosses at 2. Which is true?", "command_verb": "identify"}, "key": {"form": "statement", "expr": "B_is_f_C_is_f2_concave_up_where_C_positive"}, "steps": [{"text": "A is \\(\\frac{1}{2}(x-1)(x-3)\\).", "expr": "(x - 1)*(x - 3)/2", "relation": "new"}, {"text": "A crosses at B's turning points.", "expr": "FiniteSet(1, 3)", "relation": "solve", "variable": "x"}], "options": [{"id": "A", "is_key": true, "label": "B is \\(f\\) and C is \\(f''\\); \\(f\\) is concave up where C is positive.", "error_path": null}, {"id": "B", "is_key": false, "label": "C is \\(f\\) and B is \\(f''\\); \\(f\\) is concave up where B is positive.", "error_path": "BC-ERR-05046", "derivation": "the function and the second derivative exchanged"}, {"id": "C", "is_key": false, "label": "B is \\(f\\) and C is \\(f''\\); \\(f\\) is concave up where C is decreasing.", "error_path": "BC-ERR-05047", "derivation": "concavity read from the direction of f'' instead of its sign"}, {"id": "D", "is_key": false, "label": "B is \\(f\\) and C is \\(f''\\); the sign table is cut where B crosses the axis.", "error_path": "BC-ERR-05048", "derivation": "partition at the zeros of f"}], "calculator_status": "no_calculator", "skills": ["BC-SKL-05045"]}
 ],
 "delivery": [
  {"block": "pr-1", "mode": "text", "reason": "rule 6: a question on two named curves; the three curves are drawn on the orientation", "sources": ["BC-CON-05012"]},
  {"block": "orientation", "mode": "figure", "reason": "rule 4: BC-REP-02 on BC-SKL-05045; three fixed curves", "sources": ["BC-SKL-05045"], "spec": {"kind": "graph", "representations": ["BC-REP-02"], "curves": [{"expr": "-x**3/3 + x**2/2 + 2*x", "name": "B"}, {"expr": "-(x + 1)*(x - 2)", "name": "C"}, {"expr": "1 - 2*x", "name": "A"}], "window": {"x": [-3, 4], "y": [-5, 5]}, "labels": [{"text": "A", "placement": "inside"}, {"text": "B", "placement": "inside"}, {"text": "C", "placement": "inside"}]}, "fallback": "the same three curves, static, each lettered inside the figure", "keyboard": "none needed; no control"},
  {"block": "ki-1", "mode": "interactive", "reason": "rule 4 promoted: BC-REP-02 on BC-SKL-05045; BC-QA-05009 difficulty_variables 'whether three objects are in play rather than two' and the stem asks for a reading along x", "sources": ["BC-SKL-05045", "BC-QA-05009"], "spec": {"kind": "stacked_graphs", "representations": ["BC-REP-02"], "panels": [{"curve": "-x**3/3 + x**2/2 + 2*x", "name": "f"}, {"curve": "-(x + 1)*(x - 2)", "name": "f'"}, {"curve": "1 - 2*x", "name": "f''"}], "window": {"x": [-3, 4]}, "controls": [{"type": "slider", "parameter": "x", "range": [-3, 4], "step": 0.5, "start": -2}], "drawn": ["one vertical line through all three panels at x", "the signs of f' and f'' at x"], "labels": [{"text": "sign of f'", "placement": "inside"}, {"text": "sign of f''", "placement": "inside"}, {"text": "f turns where f' crosses", "placement": "inside"}], "question": "At this x, is f rising or falling, and concave up or down?"}, "fallback": "the three panels, static, with vertical lines at x = -1, 1/2 and 2 and the signs written in each piece", "keyboard": "Tab focuses the slider; left and right arrow keys move x by 0.5; the two signs are announced"},
  {"block": "representations", "mode": "table", "reason": "rule 5: BC-REP-03 on BC-SKL-05047 and 05048", "sources": ["BC-SKL-05047", "BC-SKL-05048"], "spec": {"kind": "table", "representations": ["BC-REP-03"], "columns": ["x", "x < -1", "-1 < x < 1/2", "1/2 < x < 2", "x > 2"], "rows": [["f'", "-", "+", "+", "-"], ["f''", "+", "+", "-", "-"]], "labels": [{"text": "cuts at zeros of f' and f'' only", "placement": "inside"}]}, "fallback": "the table as plain text rows", "keyboard": "Tab moves between cells; no control"},
  {"block": "ex-1", "mode": "step_reveal", "reason": "rule 1", "sources": []},
  {"block": "err-BC-ERR-05046", "mode": "step_reveal", "reason": "rule 1", "sources": []},
  {"block": "err-BC-ERR-05047", "mode": "step_reveal", "reason": "rule 1", "sources": []},
  {"block": "err-BC-ERR-05048", "mode": "step_reveal", "reason": "rule 1", "sources": []},
  {"block": "err-BC-ERR-05049", "mode": "step_reveal", "reason": "rule 1", "sources": []}
 ],
 "refresher": ["ki-1", "err-BC-ERR-05046", "err-BC-ERR-05047", "err-BC-ERR-05048", "err-BC-ERR-05049", "ex-1"],
 "read_minutes": {"full": 5.0, "brief": 3.0},
 "word_count": {"full": 699, "brief": 447},
 "research_lines": [
  {"file": "research/scoring/justification-requirements.md", "line": "the reason point is earned only by reasoning about the graphed object"}
 ],
 "inferred": [
  {"claim": "BC-QA-05009 has calculator_status either; the lesson places it in Section I Part A at 2.14 minutes.", "settles": "A single calculator status on BC-QA-05009 or an official example fixing its part."},
  {"claim": "The curve formulas for each draw are read from the parameter_spec notes (f' as orientation times steepness times (x - first_root)(x - second_root)), which fix only the zeros.", "settles": "Formulas for the plotted curves in the BC-QA-05009 parameter_spec."},
  {"claim": "The orientation is a static figure, ki-1 an interactive slider and the representations block a table.", "settles": "The modality A/B in the build plan: skip rate and time to first credited success by mode."},
  {"claim": "The prediction and the contrast stems are authored on ex-1's draw and on the archetype's typical wording; no record supplies them.", "settles": "The blind re-solve of the prediction key and a pretest measurement of the prediction's option choices."}
 ],
 "sources": ["BC-CON-05012", "BC-SKL-05045", "BC-SKL-05046", "BC-SKL-05047", "BC-SKL-05048", "BC-EK-FUN-4A11", "ced:107", "BC-QA-05009", "BC-QA-05004", "BC-CON-05007", "sg-25:16", "sg-25:17", "BC-ERR-05046", "BC-ERR-05047", "BC-ERR-05048", "BC-ERR-05049", "BC-MIS-05011", "BC-MIS-05020", "BC-MIS-05010", "BC-MIS-05026", "BC-PRQ-06005", "research/units/unit-05-analytical-applications-differentiation.md#5.9 Connecting a Function, Its First Derivative, and Its Second Derivative", "research/question-analysis/question-archetypes.md#BC-QA-05009 Relating the graphs of a function and its first two derivatives", "research/scoring/justification-requirements.md#Reasons tied to the object the prompt names", "research/exam/exam-structure.md#Section and part layout"]
}
```
