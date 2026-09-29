---
title: LSN-CON-01006 Estimation of a limit from a graph or a table
research_date: 2026-09-29
status: designed
purpose: Authoring spec for the concept lesson on BC-CON-01006, estimating a limit from a graph or a table and knowing what the estimate does not establish, built from authoring_bundle("BC-CON-01006") and the research files it cites, so an author fills plan 15's lesson record without making a teaching decision.
---

# LSN-CON-01006 Estimation of a limit from a graph or a table

Concept BC-CON-01006 (skills BC-SKL-01009, BC-SKL-01014, BC-SKL-01015, BC-SKL-01017), topics 1.3 and 1.4 of Unit 1, loaded by BC-QA-01001 (limit-from-graph), BC-QA-01002 (limit-from-table) and BC-QA-01013 (representation-consistency). It sits fourth in the unit's concept order because four concepts hang from it (docs/lessons/unit-01/README.md, section 1).

## Prediction

Served first, both bands. Pose on ex-1's own numbers: both sides of the graph approach an open circle at \((3,2)\) and a dot sits below it at \((3,0)\), and ask which statement holds for the limit. The stem names both sides so that only the key is true; with the circle and dot alone a jump reading makes "It does not exist" true as well. Form `mcq`, three short options, key: the limit is 2. The resolution states that the limit is the height both sides approach and that the dot is the value of \(f\) at 3, from BC-CON-01006 and the topic 1.3 paragraph. Nothing is graded and the resolution carries no verdict word.

## Orientation

Served text, from BC-CON-01006 `description_plain` and the Assessment behaviour paragraphs of topics 1.3 and 1.4, which ask for limits and values at marked breaks of a graph, for the estimate from a short table, and for what a table can establish (research/units/unit-01-limits-continuity.md#1.3 Estimating Limit Values from Graphs; research/units/unit-01-limits-continuity.md#1.4 Estimating Limit Values from Tables). No count, no frequency.

## Key ideas

The four skills map three BC-EK: BC-EK-LIM-1C2 (BC-SKL-01009, ced:40), BC-EK-LIM-1C3 (BC-SKL-01014, 01017, ced:40) and BC-EK-LIM-1C5 (BC-SKL-01015, 01017, ced:41).

- ki-1 (core, BC-EK-LIM-1C5). Values at inputs approaching the target from both sides support an estimate of the two sided limit; one side supports a one sided estimate; a finite table leaves the behaviour between its rows open. Paraphrased from the topic 1.4 paragraphs. No quote. Notation: estimate.
- ki-2 (extended, BC-EK-LIM-1C2). A graph supports an estimate read from the heights approached on each side. Anchor quote from ced:40 (11 words).
- ki-3 (core, BC-EK-LIM-1C3). Core so that the mid band teaches BC-SKL-01014 (say why a graph on one window can mislead about a limit), which no other mid block holds (plan 15, Sourcing, Pipeline step 2); the two core blocks are ki-1 and ki-3. A window at one scale can hide behaviour, so a graphical reading supports an estimate, not a proof. Anchor quote from ced:40 (12 words).

## Recognition

- BC-QA-01001 (research/question-analysis/question-archetypes.md#BC-QA-01001 Limit estimated from a graph including one sided values): `common_givens` a graph of a function with one or more breaks; `asked_to_produce` limits, one sided limits and values at named inputs. The signal is a drawn graph with open circles and dots and a request at named inputs.
- BC-QA-01002 (research/question-analysis/question-archetypes.md#BC-QA-01002 Limit estimated from a table of values): `typical_wording` "Selected values of f are given in the table. Estimate the stated limit or explain why the table does not determine it"; `common_givens` a table at inputs approaching the target from both sides. The signal is rows at shrinking distances on each side of one input.
- BC-QA-01013 (research/question-analysis/question-archetypes.md#BC-QA-01013 Limit claim matched across graphical, numerical, and analytic representations): a limit fact in one representation and candidates to match.

What says "not this concept": a formula to evaluate with no graph or table points to the analytic concepts (BC-CON-01007, 01008); the unit README's neighbour table names the feature that splits an estimate from a settled limit, a table that is deliberately inconclusive or covers one side only.

The contrast pair on st-1 takes its near miss from the analytic sibling: `this` is a graph with a hole and a dot on BC-QA-01001, `not_this` is a formula whose limit at the same input is evaluated algebraically (BC-CON-01007), and the feature is a drawn graph against a formula alone.

## Method choice

Three strategy blocks, low band all, mid band st-1.

- st-1, BC-QA-01001. Method, `expected_solution_path[0]`: locate the named input on the horizontal axis. Rival: the plotted value read as the limit (BC-ERR-01001). Separating feature: the limit is read beside the input, the value at it.
- st-2, BC-QA-01002. Method: identify the rows approaching from the left. Rival: agreement to several places taken as proof (BC-ERR-01005). Separating feature: the answer is phrased as what the table suggests.
- st-3, BC-QA-01013. Method: read the limit behaviour from the supplied representation. Rival: a one sided value matched to a two sided statement (BC-ERR-01002). Separating feature: input, side and value all kept.

All three archetypes carry `asked_to_produce` and `common_givens` in the snapshot, so no block is tagged inferred.

## Solution path

- ex-1, BC-QA-01001, both bands, no calculator. Draw: hole_x 3, jump_x 6, start_y -1, hole_y 2, hole_value 0, left_limit -2, right_limit 1, end_y 3, jump_value 4, value_mark marked, justify bare, request hole. Near \(x=3\) the left segment is \(x-1\) and the right segment \(6-4x/3\), both heading to 2, with a dot at \((3,0)\). Steps: each branch (valued, new) and its one sided limit (valued, limit from each side). Answer 2.
- ex-2, BC-QA-01002, low band only. Draw: target 1, left_value 2, right_value -1, left_slope 3, right_slope -2, curvature 0, behaviour oscillate. The rows at distances 0.1, 0.01, 0.001, 0.0001 on each side read 2.3000, -1.0200, 2.0030, -1.0002 (the spec's notes: outputs alternate between the two approached values, plus slope times distance). Steps: group the rows by side and read the value every other output closes in on (2, valued), read the value the rows between close in on (\(-1\), valued), conclude (DNE). Answer: a statement, the table suggests that the limit does not exist.

ex-2 is faded from step 3: the shown steps read the two values the outputs alternate between, 2 and \(-1\), and the student writes the suggestion before step 3, which carries DNE, appears. The fade falls there because the first two steps only read the table and the last is the sentence a written response must supply.

A fluent solver writes nothing on the MCQ shape and holds the row grouping in the head (docs/lessons/unit-01/README.md, section 5) [inferred].

## Scoring

None. BC-QA-01001, BC-QA-01002 and BC-QA-01013 list no `point_types`, so the lesson carries no scoring entry and says nothing about points (plan 15, R14).

## Traps

Five active errors meet the concept's skills; the cap is 4, so the first four in the bundle's order are served (BC-ERR-01005 is fifth and appears only as st-2's rival). Mid band shows the first two.

- err-BC-ERR-01001 (BC-MIS-01001). Wrong: the dot's height 0 reported as the limit. Right: 2. Distinct.
- err-BC-ERR-01002 (BC-MIS-01002). On ex-1's graph at \(x=6\): the left height \(-2\) reported as the limit. Right: the limit does not exist (expr `DNE`). Distinct.
- err-BC-ERR-01003 (BC-MIS-01001). With the dot at \((3,0)\) removed: the limit called nonexistent. Right: 2. Distinct.
- err-BC-ERR-01004 (BC-MIS-01004). On ex-2's table: the value near 2 reported as the limit. Right: no limit is suggested. Distinct.

Possible reasons are substrings of the linked BC-MIS descriptions.

## Representations

None. The topic Representations paragraphs name the graph, the table and a calculator window; each is carried by a delivery block (orientation figure, ki-1 motion, ki-3 figure), so no separate block is served.

## Prerequisite bridge

One bridge, BC-PRQ-06005 (supporting parent of all four skills), gated by state.

## Time

BC-QA-01001 is `no_calculator`, a single MCQ or one part of a larger question: Section I Part A, 2.14 minutes (research/exam/exam-structure.md#Section and part layout). On the MCQ both sides are read without writing; on a free response part the two one sided heights are written before the estimate.

## Checks

- chk-1, completion of ex-1, both bands. Key 2.
- chk-2, isomorph on BC-QA-01001, both bands: hole at \(x=1\), segments \(4-3x\) and \(2-x\), dot at \((1,3)\). Key 1.
- chk-3, MCQ on BC-QA-01001 with request jump, low band: heights 3 from the left and \(-2\) from the right of \(x=5\), dot at \((5,0)\). Key: the limit does not exist (statement). Distractors: 3 and \(-2\) (BC-ERR-01002, one side reported), 0 (BC-ERR-01001, the dot).

## Delivery

- orientation: figure. Rule 3, BC-REP-02 on BC-SKL-01009; the unit README picks figure. ex-1's graph near \(x=3\).
- ki-1: motion. Rule 2, a limit process: a table fills in from both sides toward the target, one row pair per frame. The unit README also names a model on the example; the example is step_reveal by rule 1, so the computed rows sit in ki-1's frames.
- ki-2: figure. Rule 3, BC-REP-02 on BC-SKL-01009: arrows along each side of the graph toward the open circle.
- ki-3: figure. Rule 3, BC-REP-02 on BC-SKL-01014: the same curve in two windows, the hole of \((x^2-4)/(x-2)\) at \(x=2\) invisible in the wide window.
- ex-1, ex-2, err blocks: step_reveal, rule 1; ex-2's rows render as a table inside the problem.

Every non-text choice is [inferred], settled by the modality A/B.

## Band plan

- Low (full): pr-1, orientation, bridge when gated, ki-1, ki-2, ki-3, st-1 with its contrast, st-2, st-3, ex-1, chk-1, four error blocks, ex-2 faded from step 3, chk-2, chk-3.
- Mid (brief): pr-1, orientation, bridge when gated, ki-1, ki-3, st-1 with its contrast, ex-1, chk-1, err-BC-ERR-01001, err-BC-ERR-01002, chk-2.
- Totals: full 814 words, 5.43 minutes (cap 900 and 6); brief 447 words, 2.98 minutes (cap 450 and 3).
- Refresher: ki-1, ki-3, the four error blocks, ex-1.

## Sources

- BC-CON-01006; BC-SKL-01009, BC-SKL-01014, BC-SKL-01015, BC-SKL-01017; BC-EK-LIM-1C2, BC-EK-LIM-1C3, BC-EK-LIM-1C5; ced:40, ced:41
- BC-QA-01001, BC-QA-01002, BC-QA-01013
- BC-ERR-01001, BC-ERR-01002, BC-ERR-01003, BC-ERR-01004, BC-ERR-01005; BC-MIS-01001, BC-MIS-01002, BC-MIS-01003, BC-MIS-01004, BC-MIS-01009
- BC-PRQ-06005
- research/units/unit-01-limits-continuity.md#1.3 Estimating Limit Values from Graphs
- research/units/unit-01-limits-continuity.md#1.4 Estimating Limit Values from Tables
- research/question-analysis/question-archetypes.md#BC-QA-01001 Limit estimated from a graph including one sided values
- research/question-analysis/question-archetypes.md#BC-QA-01002 Limit estimated from a table of values
- research/question-analysis/question-archetypes.md#BC-QA-01013 Limit claim matched across graphical, numerical, and analytic representations
- research/exam/exam-structure.md#Section and part layout
- [inferred] The ki-3 example function \((x^2-4)/(x-2)\) for a window hiding a hole. Settled by a CED or scoring example of a concealing window.
- [inferred] Nothing written on the MCQ. Settled by timing in the modality A/B.
- [inferred] Figure, motion as delivery modes. Settled by the modality A/B.
- Library gap: BC-ERR-01005 falls outside the four-block cap; research/question-analysis/question-archetypes.md records no common givens for BC-QA-01001, 01002 and 01013 while the snapshot records hold them.

## Machine record

```json
{
 "id": "LSN-CON-01006",
 "kind": "concept",
 "target_id": "BC-CON-01006",
 "unit": "01",
 "skills": ["BC-SKL-01009", "BC-SKL-01014", "BC-SKL-01015", "BC-SKL-01017"],
 "prediction": {"id": "pr-1", "stem": {"text": "Predict. Both sides of f's graph approach an open circle at (3, 2). A dot sits at (3, 0). What is the limit at x = 3?", "command_verb": "predict"}, "format": "mcq",
  "options": [{"id": "A", "label": "0", "is_key": false}, {"id": "B", "label": "2", "is_key": true}, {"id": "C", "label": "It does not exist", "is_key": false}],
  "resolution": "The limit is the height both sides approach, 2; the dot gives f(3), not the limit.", "sources": ["BC-CON-01006", "research/units/unit-01-limits-continuity.md#1.3 Estimating Limit Values from Graphs"]},
 "orientation": {
  "text": "A response reads the height each side approaches.",
  "sources": ["BC-CON-01006", "research/units/unit-01-limits-continuity.md#1.3 Estimating Limit Values from Graphs", "research/units/unit-01-limits-continuity.md#1.4 Estimating Limit Values from Tables"]
 },
 "key_ideas": [
  {"id": "ki-1", "ek_id": "BC-EK-LIM-1C5", "depth": "core", "text": "Values approaching from both sides support an estimate; a finite table leaves the rows between open.", "notation": "estimate", "quote": null, "sources": ["BC-EK-LIM-1C5", "ced:41", "research/units/unit-01-limits-continuity.md#1.4 Estimating Limit Values from Tables"]},
  {"id": "ki-2", "ek_id": "BC-EK-LIM-1C2", "depth": "extended", "text": "On a graph, the estimate is the height the curve approaches from each side of the input.", "notation": "", "quote": {"text": "Graphical information about a function can be used to estimate limits.", "source": "ced:40"}, "sources": ["BC-EK-LIM-1C2", "ced:40"]},
  {"id": "ki-3", "ek_id": "BC-EK-LIM-1C3", "depth": "core", "text": "A window can hide a hole, so a graph supports an estimate.", "notation": "", "quote": null, "sources": ["BC-EK-LIM-1C3", "ced:40"]}
 ],
 "strategy": [
  {"id": "st-1", "archetype_id": "BC-QA-01001", "cue": "A graph with named inputs.", "method": "Read each side's height.", "rival": "The dot read as the limit.", "separating_feature": "Read beside the input.", "sources": ["BC-QA-01001", "BC-ERR-01001"], "evidence_tag": "verified",
   "contrast": {"this": {"text": "A graph has a hole at x = 2 and a dot at (2, 5). Estimate the limit at x = 2.", "archetype_id": "BC-QA-01001"}, "not_this": {"text": "Evaluate the limit of \\((x^2 - 4)/(x - 2)\\) at x = 2.", "why_not": "Only a formula is given."}, "feature": "A graph, not a formula."}},
  {"id": "st-2", "archetype_id": "BC-QA-01002", "cue": "A table at inputs approaching the target from both sides, and a request for an estimate.", "method": "Group the rows approaching from the left, then from the right.", "rival": "Agreement to several places taken as proof.", "separating_feature": "The answer says what the table suggests.", "sources": ["BC-QA-01002", "BC-ERR-01005"], "evidence_tag": "verified"},
  {"id": "st-3", "archetype_id": "BC-QA-01013", "cue": "A limit fact in one form, and candidate graphs or tables to match.", "method": "Read the behaviour as input, side and value.", "rival": "A one sided value matched to a two sided statement.", "separating_feature": "A match keeps input, side and value.", "sources": ["BC-QA-01013", "BC-ERR-01002"], "evidence_tag": "verified"}
 ],
 "worked_examples": [
  {
   "id": "ex-1",
   "archetype_id": "BC-QA-01001",
   "bands": ["low", "mid"],
   "parameter_draw": {"hole_x": 3, "jump_x": 6, "start_y": -1, "hole_y": 2, "hole_value": 0, "left_limit": -2, "right_limit": 1, "end_y": 3, "jump_value": 4, "value_mark": "marked", "justify": "bare", "request": "hole"},
   "problem": {"text": "The graph of f has segments (0, -1) to (3, 2) and (3, 2) to (6, -2), an open circle at (3, 2) and a dot at (3, 0). Estimate the limit of f at x = 3.", "command_verb": "estimate"},
   "calculator_status": "no_calculator",
   "steps": [
    {"cue": "Left of x = 3 the segment starts at (0, -1).", "why": "There f(x) = x - 1.", "expr": "x - 1", "relation": "new"},
    {"cue": "Read the height from the left.", "why": "The open circle marks a height approached.", "expr": "2", "relation": "limit", "variable": "x", "point": "3", "dir": "-"},
    {"cue": "Right of 3 the segment falls to (6, -2).", "why": "There f(x) = 6 - 4x/3.", "expr": "6 - 4*x/3", "relation": "new"},
    {"cue": "Read the height from the right.", "why": "Both sides give 2; the dot at 0 is the value, not the limit.", "expr": "2", "relation": "limit", "variable": "x", "point": "3", "dir": "+"}
   ],
   "answer": {"form": "numeric", "expr": "2"}
  },
  {
   "id": "ex-2",
   "archetype_id": "BC-QA-01002",
   "bands": ["low"],
   "fade_from": 3,
   "parameter_draw": {"target": 1, "left_value": 2, "right_value": -1, "left_slope": 3, "right_slope": -2, "curvature": 0, "behaviour": "oscillate"},
   "problem": {"text": "The table gives f at x = 0.9, 0.99, 0.999, 0.9999 as 2.3000, -1.0200, 2.0030, -1.0002, and at x = 1.1, 1.01, 1.001, 1.0001 with the same values. State what the table suggests about the limit of f at x = 1, and why.", "command_verb": "estimate"},
   "calculator_status": "no_calculator",
   "steps": [
    {"cue": "Group the rows by side. On each side every other output closes in on 2.", "why": "2.3000, then 2.0030.", "expr": "2", "relation": "new"},
    {"cue": "The rows between them close in on -1.", "why": "-1.0200, then -1.0002.", "expr": "-1", "relation": "new"},
    {"cue": "The stem allows an explanation instead of an estimate.", "why": "The outputs alternate between 2 and -1, so the table suggests the limit does not exist. It proves nothing between rows.", "expr": "DNE", "relation": "new"}
   ],
   "answer": {"form": "statement", "expr": "DNE", "text": "The table suggests that the limit does not exist, since the outputs alternate near 2 and near -1 on both sides."}
  }
 ],
 "what_a_reader_scores": [],
 "common_errors": [
  {"error_id": "BC-ERR-01001", "observed_behavior": "The response gives the plotted or defined value of the function at the input in place of the value the function approaches there.", "scoring_consequence": "The reading point is lost, and in a continuity part the comparison of limit with value collapses.", "wrong_step": {"text": "The dot's height 0 reported as the limit.", "expr": "0"}, "right_step": {"text": "Both sides head to 2.", "expr": "2"}, "relation": "distinct", "fix_prompt": true, "possible_reason": {"misconception_id": "BC-MIS-01001", "text": "the limit as another name for evaluation"}, "sources": ["BC-ERR-01001", "BC-MIS-01001"]},
  {"error_id": "BC-ERR-01002", "observed_behavior": "The response reports the value approached from one side as the limit although the two sides differ.", "scoring_consequence": "The value point is lost because the correct response is that the limit does not exist.", "wrong_step": {"text": "At x = 6, the left height -2 reported as the limit.", "expr": "-2"}, "right_step": {"text": "The sides give -2 and 1: no limit.", "expr": "DNE"}, "relation": "distinct", "fix_prompt": true, "possible_reason": {"misconception_id": "BC-MIS-01002", "text": "a single one sided approach as sufficient"}, "sources": ["BC-ERR-01002", "BC-MIS-01002"]},
  {"error_id": "BC-ERR-01003", "observed_behavior": "The response states that the limit does not exist on the grounds that the function has no value at the input.", "scoring_consequence": "Both the value point and any justification point are lost.", "wrong_step": {"text": "With the dot at (3, 0) removed, the limit is called nonexistent.", "expr": "DNE"}, "right_step": {"text": "Both sides still head to 2.", "expr": "2"}, "relation": "distinct", "fix_prompt": true, "possible_reason": {"misconception_id": "BC-MIS-01001", "text": "a missing or displaced function value is read as a missing or displaced limit"}, "sources": ["BC-ERR-01003", "BC-MIS-01001"]},
  {"error_id": "BC-ERR-01004", "observed_behavior": "The response reports one of the values the function oscillates between as the limit near the input.", "scoring_consequence": "The value point is lost because no limit exists.", "wrong_step": {"text": "In the second example's table, 2 reported as the limit.", "expr": "2"}, "right_step": {"text": "The outputs keep alternating: no limit is suggested.", "expr": "DNE"}, "relation": "distinct", "fix_prompt": true, "possible_reason": {"misconception_id": "BC-MIS-01004", "text": "oscillation or behaviour between the tabulated inputs is not considered"}, "sources": ["BC-ERR-01004", "BC-MIS-01004"]}
 ],
 "representations": null,
 "prerequisite_bridges": [
  {"prq_id": "BC-PRQ-06005", "text": "Estimating reads f at a stated input from a graph or table."}
 ],
 "time": {"exam_part": "I-A", "budget_minutes": 2.14, "source": "research/exam/exam-structure.md#Section and part layout", "written_steps": {"ex-1": [2, 4], "ex-2": []}, "skipped_steps": {"ex-1": [1, 3], "ex-2": [1, 2, 3]}},
 "checks": [
  {"id": "chk-1", "check_kind": "completion", "format": "short_answer", "bands": ["low", "mid"], "archetype_id": "BC-QA-01001",
   "parameter_draw": {"hole_x": 3, "jump_x": 6, "start_y": -1, "hole_y": 2, "hole_value": 0, "left_limit": -2, "right_limit": 1, "end_y": 3, "jump_value": 4, "value_mark": "marked", "justify": "bare", "request": "hole"},
   "completes": "ex-1",
   "stem": {"text": "Left of x = 3, f(x) = x - 1; right of 3, f(x) = 6 - 4x/3; the dot is (3, 0). Estimate the limit at x = 3.", "command_verb": "estimate"},
   "key": {"form": "numeric", "expr": "2"},
   "steps": [{"text": "The right piece.", "expr": "6 - 4*x/3", "relation": "new"}, {"text": "It heads to 2.", "expr": "2", "relation": "limit", "variable": "x", "point": "3", "dir": "+"}],
   "calculator_status": "no_calculator", "skills": ["BC-SKL-01009"]},
  {"id": "chk-2", "check_kind": "isomorph", "format": "short_answer", "bands": ["low", "mid"], "archetype_id": "BC-QA-01001",
   "parameter_draw": {"hole_x": 1, "jump_x": 5, "start_y": 4, "hole_y": 1, "hole_value": 3, "left_limit": -3, "right_limit": 2, "end_y": 0, "jump_value": 0, "value_mark": "marked", "justify": "bare", "request": "hole"},
   "stem": {"text": "f has segments (0, 4) to (1, 1) and (1, 1) to (5, -3), an open circle at (1, 1), a dot at (1, 3). Estimate the limit at x = 1.", "command_verb": "estimate"},
   "key": {"form": "numeric", "expr": "1"},
   "steps": [{"text": "Left piece 4 - 3x.", "expr": "4 - 3*x", "relation": "new"}, {"text": "It heads to 1.", "expr": "1", "relation": "limit", "variable": "x", "point": "1", "dir": "-"}, {"text": "Right piece 2 - x.", "expr": "2 - x", "relation": "new"}, {"text": "It heads to 1.", "expr": "1", "relation": "limit", "variable": "x", "point": "1", "dir": "+"}],
   "calculator_status": "no_calculator", "skills": ["BC-SKL-01009"]},
  {"id": "chk-3", "check_kind": "mcq", "format": "mcq", "bands": ["low"], "archetype_id": "BC-QA-01001",
   "parameter_draw": {"hole_x": 2, "jump_x": 5, "start_y": 1, "hole_y": -1, "hole_value": 2, "left_limit": 3, "right_limit": -2, "end_y": 1, "jump_value": 0, "value_mark": "marked", "justify": "bare", "request": "jump"},
   "stem": {"text": "The graph of f approaches 3 from the left of x = 5 and -2 from the right, with a dot at (5, 0). What is the limit of f at x = 5?", "command_verb": "find"},
   "key": {"form": "statement", "expr": "DNE", "text": "The limit does not exist."},
   "steps": [{"text": "Left height 3.", "expr": "3", "relation": "new"}, {"text": "Right height -2, which differs.", "expr": "-2", "relation": "new"}],
   "options": [
    {"id": "A", "is_key": false, "label": "3", "error_path": "BC-ERR-01002", "derivation": "the left height reported as the limit"},
    {"id": "B", "is_key": false, "label": "-2", "error_path": "BC-ERR-01002", "derivation": "the right height reported as the limit"},
    {"id": "C", "is_key": false, "label": "0", "error_path": "BC-ERR-01001", "derivation": "the dot's height reported as the limit"},
    {"id": "D", "is_key": true, "label": "The limit does not exist", "error_path": null}
   ],
   "calculator_status": "no_calculator", "skills": ["BC-SKL-01009"]}
 ],
 "delivery": [
  {"block": "orientation", "mode": "figure", "reason": "rule 3: BC-REP-02 on BC-SKL-01009; unit README delivery map", "sources": ["BC-SKL-01009"],
   "spec": {"kind": "graph", "window": {"x": [0, 6], "y": [-3, 4]}, "curves": [{"expr": "x - 1", "domain": [0, 3]}, {"expr": "6 - 4*x/3", "domain": [3, 6]}], "points": [{"at": [3, 2], "style": "open"}, {"at": [3, 0], "style": "filled"}], "labels": [{"text": "height approached: 2", "placement": "inside"}, {"text": "f(3) = 0", "placement": "inside"}]},
   "fallback": "the same graph static, with a sentence naming the open circle and the dot", "keyboard": "no control; the figure description is reached with Tab"},
  {"block": "ki-1", "mode": "motion", "reason": "rule 2: a limit process, a table filling in from both sides toward the target (BC-SKL-01015, BC-SKL-01017)", "sources": ["BC-SKL-01015", "BC-SKL-01017"],
   "spec": {"kind": "table_sweep", "columns": ["x from the left", "f(x)", "x from the right", "f(x)"], "frames": [["1.9", "3.2100", "2.1", "2.5100"], ["1.99", "3.0201", "2.01", "2.9501"], ["1.999", "3.0020", "2.001", "2.9950"], ["1.9999", "3.0002", "2.0001", "2.9995"]], "model": {"target": 2, "value": 3, "left_slope": 2, "right_slope": -5, "curvature": 1}, "labels": [{"text": "both sides near 3", "placement": "inside"}, {"text": "estimate: 3; nothing proved between rows", "placement": "inside"}]},
   "fallback": "the full four-row table, static, with both labels",
   "keyboard": "Right and Left arrow keys add or remove a row pair; Space pauses auto-advance",
   "reduced_motion": "no auto-advance; each key press cross-fades in the next row pair"},
  {"block": "ki-2", "mode": "figure", "reason": "rule 3: BC-REP-02 on BC-SKL-01009", "sources": ["BC-SKL-01009"],
   "spec": {"kind": "graph", "curves": [{"expr": "x - 1", "domain": [0, 3]}, {"expr": "6 - 4*x/3", "domain": [3, 6]}], "points": [{"at": [3, 2], "style": "open"}], "arrows": [{"along": "left branch", "toward": [3, 2]}, {"along": "right branch", "toward": [3, 2]}], "labels": [{"text": "from the left: 2", "placement": "inside"}, {"text": "from the right: 2", "placement": "inside"}]},
   "fallback": "the static graph with its two labels", "keyboard": "no control"},
  {"block": "ki-3", "mode": "figure", "reason": "rule 3: BC-REP-02 on BC-SKL-01014, a scale that hides behaviour", "sources": ["BC-SKL-01014"],
   "spec": {"kind": "graph_pair", "representations": ["wide window", "narrow window"], "curves": [{"expr": "(x**2 - 4)/(x - 2)", "domain": [-10, 10]}], "panels": [{"window": {"x": [-10, 10], "y": [-10, 14]}, "shows": "an unbroken line"}, {"window": {"x": [1.9, 2.1], "y": [3.9, 4.1]}, "shows": "an open circle at (2, 4)"}], "labels": [{"text": "wide window: no gap visible", "placement": "inside"}, {"text": "narrow window: hole at x = 2", "placement": "inside"}]},
   "fallback": "both panels static side by side with their labels", "keyboard": "no control"},
  {"block": "ex-1", "mode": "step_reveal", "reason": "rule 1", "sources": []},
  {"block": "ex-2", "mode": "step_reveal", "reason": "rule 1; the rows render as a table inside the problem (BC-REP-03 given)", "sources": ["BC-SKL-01017"]},
  {"block": "err-BC-ERR-01001", "mode": "step_reveal", "reason": "rule 1", "sources": []},
  {"block": "err-BC-ERR-01002", "mode": "step_reveal", "reason": "rule 1", "sources": []},
  {"block": "err-BC-ERR-01003", "mode": "step_reveal", "reason": "rule 1", "sources": []},
  {"block": "err-BC-ERR-01004", "mode": "step_reveal", "reason": "rule 1", "sources": []}
 ],
 "refresher": ["ki-1", "ki-3", "err-BC-ERR-01001", "err-BC-ERR-01002", "err-BC-ERR-01003", "err-BC-ERR-01004", "ex-1"],
 "read_minutes": {"full": 5.44, "brief": 2.98},
 "word_count": {"full": 816, "brief": 447},
 "research_lines": [
  {"file": "research/units/unit-01-limits-continuity.md", "line": "A finite table does not determine the behaviour between its rows, so an estimate remains an estimate."}
 ],
 "inferred": [
  {"claim": "The ki-3 window example uses (x^2 - 4)/(x - 2), whose hole at x = 2 no wide window shows.", "settles": "A CED or scoring guideline example of a concealing calculator window."},
  {"claim": "On the MCQ a fluent solver writes nothing and groups rows in the head.", "settles": "Timing of written against held steps in the modality A/B."},
  {"claim": "Figure and motion serve these blocks better than text.", "settles": "The modality A/B in the build plan: skip rate and time to first credited success by mode."}
 ],
 "sources": ["BC-CON-01006", "BC-SKL-01009", "BC-SKL-01014", "BC-SKL-01015", "BC-SKL-01017", "BC-EK-LIM-1C2", "BC-EK-LIM-1C3", "BC-EK-LIM-1C5", "ced:40", "ced:41", "BC-QA-01001", "BC-QA-01002", "BC-QA-01013", "BC-ERR-01001", "BC-ERR-01002", "BC-ERR-01003", "BC-ERR-01004", "BC-ERR-01005", "BC-MIS-01001", "BC-MIS-01002", "BC-MIS-01004", "BC-PRQ-06005", "research/units/unit-01-limits-continuity.md#1.3 Estimating Limit Values from Graphs", "research/units/unit-01-limits-continuity.md#1.4 Estimating Limit Values from Tables", "research/exam/exam-structure.md#Section and part layout"]
}
```
