---
title: LSN-CON-08012 Area between two curves integrated in y
research_date: 2026-09-29
status: designed
purpose: Authoring spec for the concept lesson on BC-CON-08012, the area of a region as the integral of right minus left in y, built from authoring_bundle("BC-CON-08012") and the research files it cites, so an author fills plan 15's lesson record without making a teaching decision.
---

# LSN-CON-08012 Area between two curves integrated in y

Concept BC-CON-08012 (skills BC-SKL-08023, BC-SKL-08024, BC-SKL-08025, BC-SKL-08026), topic 8.5 of Unit 8, loaded by one archetype, BC-QA-08009 (family area-between-curves). Its hard parent is BC-CON-08010, and every volume concept has it as a hard parent (docs/lessons/unit-08/README.md, section 1).

## Orientation

Served text, from BC-CON-08012 `description_plain` and the topic's Assessment behaviour paragraph (research/units/unit-08-applications-integration.md#8.5 Finding the Area Between Curves Expressed as Functions of y): a response rewrites both boundaries as x in terms of y and integrates right minus left in dy between y limits, one integral where x would need two. No count, no frequency.

## Key ideas

All four skills map to BC-EK-CHA-5A2 (ced:156): one core block, both bands.

- ki-1 (core). Paraphrase of the Required mathematical knowledge paragraphs (Area in y; Choice of variable; Notation): with both boundaries written as functions of y, the area is the integral of right minus left in y; a region whose upper boundary changes needs two integrals in x or one in y; dy goes with y limits and an integrand in y. Anchor quote from ced:156. Notation line from the concept record.

## Recognition

BC-QA-08009 (research/question-analysis/question-archetypes.md#BC-QA-08009 Area of a region integrated with respect to y): `typical_wording` "find the area of the region bounded by the two curves by integrating with respect to y"; `common_givens` a figure, curve equations in x or in y; `asked_to_produce` an integrand in y, the area. The signal: "with respect to y" in the stem, curves given as x = g(y), or a region whose top changes from one curve to another while its left and right edges each stay one curve (`difficulty_variables`: whether the region would need two integrals in x). Shapes: one part of a multipart question or an MCQ (BC-MCQ-CED-010); no 2023 to 2025 BC free response part used it.

What says "not this concept": one curve on top across the whole x span (area in x, BC-CON-08010); curves that swap places (BC-CON-08013).

## Method choice

One strategy block, both bands.

- st-1, BC-QA-08009. Cue from `asked_to_produce` and `common_givens`. Method, `expected_solution_path[0]`: write both boundaries as functions of y. Rival, `wrong_approaches`: integrating the original functions of x between y limits (BC-ERR-08023). Separating feature: dy demands an integrand with no x in it. Both fields are present, so the block is not tagged inferred.

## Solution path

- ex-1, BC-QA-08009, both bands, no calculator. Draw from `parameter_spec`: stretch 1, height 2, run 1, shift 0, letters fg, presentation formula; so offset 2, the curves are x = y^2 (given as y = sqrt(x)) and x = y + 2 (given as y = x - 2), meeting at y = 2, with the x-axis below; area 10/3. No published BC-QA-08009 item carries this draw.
- Steps follow `expected_solution_path`: both boundaries in y (no value); the right curve (no value); the meeting point in y (new, solve); the integral in y (new); the value (equivalent). A fluent solver writes the rewrites, the integral and the value; the right curve test is held [inferred].

## Scoring

BC-QA-08009 lists no `point_types`, so the lesson carries no what_a_reader_scores entry, no point tag, and says nothing about points beyond the error records' `scoring_consequence`. For the author: the archetype's scoring pattern is a setup and an answer, inferred from the 2023 area part (sg-23:16; research/units/unit-08-applications-integration.md#Unresolved).

## Traps

Four active errors meet the skills, in the bundle's order: BC-ERR-08020, BC-ERR-08023, BC-ERR-08024, BC-ERR-99006. Low band all four; mid band the first two. All on ex-1's draw.

- err-BC-ERR-08020: left minus right, -10/3. Possible reason, words from BC-MIS-08011.
- err-BC-ERR-08023: the x forms sqrt(x) - (x - 2) under dy; the result still holds x. Possible reason, words from BC-MIS-08013.
- err-BC-ERR-08024: the x limits 0 and 4 on the y integral, -16/3. Possible reason, words from BC-MIS-08012.
- err-BC-ERR-99006: the integral with no dy; the same value, so equivalent. No possible reason line.

## Representations

None as a separate block. The topic's Representations paragraph names the figure converted to a horizontal slice integral (BC-REP-02 to BC-REP-01), which the orientation and ki-1 figures carry.

## Prerequisite bridge

- BC-PRQ-06005, from its `description_plain` and `failure_signature`.
- BC-PRQ-08002, from its `description_plain` and `failure_signature`.

## Time

BC-QA-08009 is `either`; the design takes Section I Part A, 2.14 minutes per question (research/exam/exam-structure.md#Section and part layout) [inferred: an either archetype placed in I-A]. As a free response part it is two points [inferred from sg-23:16], 3.33 minutes (docs/lessons/unit-08/README.md, section 5). The minutes go on the rewrites and the antiderivative; which curve is right is held.

## Checks

- chk-1, completion of ex-1, both bands: evaluate the y integral. Key 10/3.
- chk-2, isomorph, both bands. Draw: stretch 1, height 3, run 1, shift 0, letters hk, formula; curves y = sqrt(x), y = x - 6, the x-axis. Key 27/2.
- chk-3, MCQ, low band. Draw: stretch 2, height 2, run 2, shift 0, letters pq, formula; curves y = sqrt(x/2), y = (x - 4)/2, the x-axis. Key the integral of 2y + 4 - 2y^2 on [0, 2], 20/3. Distractors: left minus right (BC-ERR-08020), the x forms under dy (BC-ERR-08023), the x limits 0 and 8 (BC-ERR-08024).

## Delivery

- orientation: figure. Rule 4: BC-REP-02 on BC-SKL-08024 and BC-SKL-08025; unit README delivery map.
- ki-1: figure. Rule 4: BC-REP-08 on BC-SKL-08026, BC-REP-02 on BC-SKL-08024: the region with a horizontal rectangle from left curve to right curve and the y limits on the axis. Not promoted: BC-QA-08009 `difficulty_variables` are presence flags [inferred; settled by the modality A/B].
- ex-1: step_reveal. Rule 1.
- err-BC-ERR-08020, err-BC-ERR-08023, err-BC-ERR-08024, err-BC-ERR-99006: step_reveal. Rule 1.

## Band plan

- Low (full): orientation, ki-1, st-1, ex-1, the four error blocks, chk-1 to chk-3, both bridges. 511 words, 3.5 minutes (cap 900 and 6).
- Mid (brief): orientation, ki-1, st-1, ex-1, err-BC-ERR-08020, err-BC-ERR-08023, chk-1, chk-2, both bridges. 406 words, 2.8 minutes (cap 450 and 3).
- Refresher: ki-1, err-BC-ERR-08020, err-BC-ERR-08023, err-BC-ERR-08024, err-BC-ERR-99006, ex-1.

## Sources

- BC-CON-08012; BC-SKL-08023, BC-SKL-08024, BC-SKL-08025, BC-SKL-08026; BC-EK-CHA-5A2; ced:156
- BC-QA-08009; BC-MCQ-CED-010; sg-23:16
- BC-ERR-08020, BC-ERR-08023, BC-ERR-08024, BC-ERR-99006; BC-MIS-08011, BC-MIS-08012, BC-MIS-08013
- BC-PRQ-06005, BC-PRQ-08002
- research/units/unit-08-applications-integration.md#8.5 Finding the Area Between Curves Expressed as Functions of y
- research/units/unit-08-applications-integration.md#Unresolved
- research/question-analysis/question-archetypes.md#BC-QA-08009 Area of a region integrated with respect to y
- research/exam/exam-structure.md#Section and part layout
- [inferred] BC-QA-08009 is either; the lesson takes I-A. Settled by a ruling on which part an either archetype's budget comes from.
- [inferred] The free response point count. Settled by a scoring guideline for an area in y part.
- [inferred] The orientation and ki-1 figures, and the held right curve test. Settled by the modality A/B and timing data per step.

## Machine record

```json
{
 "id": "LSN-CON-08012",
 "kind": "concept",
 "target_id": "BC-CON-08012",
 "unit": "08",
 "skills": ["BC-SKL-08023", "BC-SKL-08024", "BC-SKL-08025", "BC-SKL-08026"],
 "orientation": {
  "text": "A response rewrites both boundaries as x in terms of y, then integrates the right curve minus the left curve in dy between y limits: one integral where slicing in x would need two.",
  "sources": ["BC-CON-08012", "research/units/unit-08-applications-integration.md#8.5 Finding the Area Between Curves Expressed as Functions of y"]
 },
 "key_ideas": [
  {
   "id": "ki-1",
   "ek_id": "BC-EK-CHA-5A2",
   "depth": "core",
   "text": "With both boundaries written as x in terms of y, the area is the integral of right minus left with respect to y. A region whose top changes curve needs two integrals in x but one in y, when each side stays one curve. With dy, the integrand holds only y and the limits are y values.",
   "notation": "right minus left; dy",
   "quote": {"text": "Areas of regions in the plane can be calculated using functions of either x or y.", "source": "ced:156"},
   "sources": ["BC-EK-CHA-5A2", "ced:156", "research/units/unit-08-applications-integration.md#8.5 Finding the Area Between Curves Expressed as Functions of y"]
  }
 ],
 "strategy": [
  {
   "id": "st-1",
   "archetype_id": "BC-QA-08009",
   "cue": "The stem asks for an area by integrating in y, from a figure and curve equations in x or y.",
   "method": "First written line: both boundaries as x in terms of y.",
   "rival": "Rival: the original functions of x integrated between y limits (BC-ERR-08023).",
   "separating_feature": "dy demands an integrand with no x.",
   "sources": ["BC-QA-08009"],
   "evidence_tag": "verified"
  }
 ],
 "worked_examples": [
  {
   "id": "ex-1",
   "archetype_id": "BC-QA-08009",
   "bands": ["low", "mid"],
   "parameter_draw": {"stretch": 1, "height": 2, "run": "1", "shift": 0, "letters": "fg", "presentation": "formula"},
   "problem": {"text": "R is bounded by \\(y=\\sqrt{x}\\), \\(y=x-2\\) and the x-axis. Find its area by integrating in y.", "command_verb": "find"},
   "calculator_status": "no_calculator",
   "steps": [
    {"cue": "In y: each boundary as x in terms of y.", "why": "\\(x=y^2\\) and \\(x=y+2\\)."},
    {"cue": "Which is right? Test \\(y=1\\).", "why": "\\(y+2=3\\) exceeds \\(y^2=1\\): the line is right."},
    {"cue": "y limits: the x-axis, \\(y=0\\), and where the curves meet.", "why": "Only \\(y=2\\) lies in R; \\(y=-1\\) is on the discarded branch.", "expr": "y**2 = y + 2", "relation": "new"},
    {"cue": "Solve.", "why": "Top of R.", "expr": "FiniteSet(2)", "relation": "solve", "variable": "y"},
    {"cue": "Right minus left, dy, limits 0 and 2.", "why": "One integral covers R.", "expr": "Integral(y + 2 - y**2, (y, 0, 2))", "relation": "new"},
    {"cue": "Evaluate.", "why": "\\(2+4-8/3\\).", "expr": "10/3", "relation": "equivalent"}
   ],
   "answer": {"form": "numeric", "expr": "10/3"}
  }
 ],
 "what_a_reader_scores": [],
 "common_errors": [
  {
   "error_id": "BC-ERR-08020",
   "observed_behavior": "The integrand is the lower curve minus the upper curve, or the left curve minus the right curve.",
   "scoring_consequence": "The integrand point may survive, since either order earned it in 2023, but a negative value reported as an area loses the answer point (sg-23:16, sg-23:17).",
   "wrong_step": {"text": "Left minus right: \\(-10/3\\).", "expr": "Integral(y**2 - (y + 2), (y, 0, 2))"},
   "right_step": {"text": "Right minus left: \\(10/3\\).", "expr": "Integral(y + 2 - y**2, (y, 0, 2))"},
   "relation": "distinct",
   "possible_reason": {"misconception_id": "BC-MIS-08011", "text": "any sign problem can be repaired at the end"},
   "sources": ["BC-ERR-08020", "BC-MIS-08011"]
  },
  {
   "error_id": "BC-ERR-08023",
   "observed_behavior": "A function of x is integrated with respect to y, or the reverse, without being rewritten.",
   "scoring_consequence": "The setup point is lost because the expression does not define a number.",
   "wrong_step": {"text": "\\(\\sqrt{x}-(x-2)\\) under dy.", "expr": "Integral(sqrt(x) - (x - 2), (y, 0, 2))"},
   "right_step": {"text": "\\(y+2-y^2\\) under dy.", "expr": "Integral(y + 2 - y**2, (y, 0, 2))"},
   "relation": "distinct",
   "possible_reason": {"misconception_id": "BC-MIS-08013", "text": "dx and dy as labels for the direction of slicing"},
   "sources": ["BC-ERR-08023", "BC-MIS-08013"]
  },
  {
   "error_id": "BC-ERR-08024",
   "observed_behavior": "An integral in y carries x values as its limits.",
   "scoring_consequence": "The setup point is lost and the value is wrong.",
   "wrong_step": {"text": "x limits 0 and 4: \\(-16/3\\).", "expr": "Integral(y + 2 - y**2, (y, 0, 4))"},
   "right_step": {"text": "y limits 0 and 2.", "expr": "Integral(y + 2 - y**2, (y, 0, 2))"},
   "relation": "distinct",
   "possible_reason": {"misconception_id": "BC-MIS-08012", "text": "chooses limits from the axes of the picture"},
   "sources": ["BC-ERR-08024", "BC-MIS-08012"]
  },
  {
   "error_id": "BC-ERR-99006",
   "observed_behavior": "Responses present a definite integral with no differential, or with a differential in the wrong variable, producing a setup the reader cannot interpret.",
   "scoring_consequence": "The setup point is not earned when the resulting expression is ambiguous; in some parts later points in that part are also lost.",
   "wrong_step": {"text": "\\(\\int_0^2 (y+2-y^2)\\) with no dy.", "expr": "Integral(y + 2 - y**2, (y, 0, 2))"},
   "right_step": {"text": "\\(\\int_0^2 (y+2-y^2)\\,dy\\).", "expr": "Integral(y + 2 - y**2, (y, 0, 2))"},
   "relation": "equivalent",
   "possible_reason": null,
   "sources": ["BC-ERR-99006"]
  }
 ],
 "representations": null,
 "prerequisite_bridges": [
  {"prq_id": "BC-PRQ-06005", "text": "\\(f(1)\\) is one value at one input; reading the wrong input, or \\(f'\\) for \\(f\\), names the wrong right curve."},
  {"prq_id": "BC-PRQ-08002", "text": "An equation solved for x in terms of y, with the branch the region needs; without it, dy gets an integrand in x."}
 ],
 "time": {"exam_part": "I-A", "budget_minutes": 2.14, "source": "research/exam/exam-structure.md#Section and part layout", "written_steps": {"ex-1": [1, 3, 4, 5, 6]}, "skipped_steps": {"ex-1": [2]}},
 "checks": [
  {
   "id": "chk-1",
   "check_kind": "completion",
   "format": "short_answer",
   "bands": ["low", "mid"],
   "archetype_id": "BC-QA-08009",
   "parameter_draw": {"stretch": 1, "height": 2, "run": "1", "shift": 0, "letters": "fg", "presentation": "formula"},
   "completes": "ex-1",
   "stem": {"text": "Evaluate \\(\\int_0^2 (y+2-y^2)\\,dy\\).", "command_verb": "evaluate"},
   "key": {"form": "numeric", "expr": "10/3"},
   "steps": [
    {"text": "The integral.", "expr": "Integral(y + 2 - y**2, (y, 0, 2))", "relation": "new"},
    {"text": "Evaluated.", "expr": "10/3", "relation": "equivalent"}
   ],
   "calculator_status": "no_calculator",
   "skills": ["BC-SKL-08025"]
  },
  {
   "id": "chk-2",
   "check_kind": "isomorph",
   "format": "short_answer",
   "bands": ["low", "mid"],
   "archetype_id": "BC-QA-08009",
   "parameter_draw": {"stretch": 1, "height": 3, "run": "1", "shift": 0, "letters": "hk", "presentation": "formula"},
   "stem": {"text": "R is bounded by \\(y=\\sqrt{x}\\), \\(y=x-6\\) and the x-axis. Find its area in y.", "command_verb": "find"},
   "key": {"form": "numeric", "expr": "27/2"},
   "steps": [
    {"text": "\\(x=y^2\\), \\(x=y+6\\) meet at \\(y=3\\).", "expr": "y**2 = y + 6", "relation": "new"},
    {"text": "The root in R.", "expr": "FiniteSet(3)", "relation": "solve", "variable": "y"},
    {"text": "Right minus left.", "expr": "Integral(y + 6 - y**2, (y, 0, 3))", "relation": "new"},
    {"text": "Evaluated.", "expr": "27/2", "relation": "equivalent"}
   ],
   "calculator_status": "no_calculator",
   "skills": ["BC-SKL-08025"]
  },
  {
   "id": "chk-3",
   "check_kind": "mcq",
   "format": "mcq",
   "bands": ["low"],
   "archetype_id": "BC-QA-08009",
   "parameter_draw": {"stretch": 2, "height": 2, "run": "2", "shift": 0, "letters": "pq", "presentation": "formula"},
   "stem": {"text": "R is bounded by \\(y=\\sqrt{x/2}\\), \\(y=(x-4)/2\\) and the x-axis. Which gives its area?", "command_verb": "identify"},
   "key": {"form": "numeric", "expr": "20/3"},
   "steps": [
    {"text": "\\(x=2y^2\\) left, \\(x=2y+4\\) right, meeting at \\(y=2\\).", "expr": "Integral(2*y + 4 - 2*y**2, (y, 0, 2))", "relation": "new"},
    {"text": "Evaluated.", "expr": "20/3", "relation": "equivalent"}
   ],
   "options": [
    {"id": "A", "is_key": true, "expr": "Integral(2*y + 4 - 2*y**2, (y, 0, 2))", "error_path": null},
    {"id": "B", "is_key": false, "expr": "Integral(2*y**2 - (2*y + 4), (y, 0, 2))", "error_path": "BC-ERR-08020", "derivation": "left minus right"},
    {"id": "C", "is_key": false, "expr": "Integral(sqrt(x/2) - (x - 4)/2, (y, 0, 2))", "error_path": "BC-ERR-08023", "derivation": "the given functions of x under dy"},
    {"id": "D", "is_key": false, "expr": "Integral(2*y + 4 - 2*y**2, (y, 0, 8))", "error_path": "BC-ERR-08024", "derivation": "the x value 8 of the meeting point used as the upper limit"}
   ],
   "calculator_status": "no_calculator",
   "skills": ["BC-SKL-08025"]
  }
 ],
 "delivery": [
  {"block": "orientation", "mode": "figure", "reason": "rule 4: BC-REP-02 on BC-SKL-08024 and BC-SKL-08025; unit README delivery map", "sources": ["BC-SKL-08024", "BC-SKL-08025"],
   "spec": {"kind": "graph", "representations": ["BC-REP-02"], "window": {"x": [-1, 5], "y": [-1, 3]}, "curves": [{"expr": "sqrt(x)", "domain": [0, 5]}, {"expr": "x - 2", "domain": [2, 5]}], "shade": {"region": "between x = y**2 and x = y + 2 for 0 <= y <= 2"}, "labels": [{"text": "left: x = y^2", "placement": "inside"}, {"text": "right: x = y + 2", "placement": "inside"}]},
   "fallback": "the same shaded region static with both labels", "keyboard": "no control; the figure description is reached with Tab"},
  {"block": "ki-1", "mode": "figure", "reason": "rule 4: BC-REP-08 on BC-SKL-08026 and BC-REP-02 on BC-SKL-08024; not promoted, BC-QA-08009 difficulty_variables are presence flags", "sources": ["BC-SKL-08026", "BC-SKL-08024", "BC-QA-08009"],
   "spec": {"kind": "graph", "representations": ["BC-REP-02", "BC-REP-08"], "window": {"x": [-1, 5], "y": [-1, 3]}, "curves": [{"expr": "sqrt(x)", "domain": [0, 5]}, {"expr": "x - 2", "domain": [2, 5]}], "rectangles": [{"y": 1, "from_x": "y**2", "to_x": "y + 2", "height": 0.15}], "labels": [{"text": "width (y + 2) - y^2", "placement": "inside"}, {"text": "y = 0", "placement": "inside"}, {"text": "y = 2", "placement": "inside"}]},
   "fallback": "the static region with one horizontal rectangle at y = 1 and the y limits marked on the axis", "keyboard": "no control; the figure description is reached with Tab"},
  {"block": "ex-1", "mode": "step_reveal", "reason": "rule 1", "sources": []},
  {"block": "err-BC-ERR-08020", "mode": "step_reveal", "reason": "rule 1", "sources": []},
  {"block": "err-BC-ERR-08023", "mode": "step_reveal", "reason": "rule 1", "sources": []},
  {"block": "err-BC-ERR-08024", "mode": "step_reveal", "reason": "rule 1", "sources": []},
  {"block": "err-BC-ERR-99006", "mode": "step_reveal", "reason": "rule 1", "sources": []}
 ],
 "refresher": ["ki-1", "err-BC-ERR-08020", "err-BC-ERR-08023", "err-BC-ERR-08024", "err-BC-ERR-99006", "ex-1"],
 "read_minutes": {"full": 3.5, "brief": 2.8},
 "word_count": {"full": 511, "brief": 406},
 "research_lines": [
  {"file": "research/units/unit-08-applications-integration.md", "line": "A region whose upper boundary changes needs either two integrals in x or one integral in y"}
 ],
 "inferred": [
  {"claim": "BC-QA-08009 is an either archetype; the lesson takes Section I Part A and its 2.14 minute budget.", "settles": "A ruling on which exam part an either archetype's budget comes from."},
  {"claim": "The free response part is worth two points, taken from the 2023 area in x pattern.", "settles": "A scoring guideline for an area with respect to y part."},
  {"claim": "The orientation and ki-1 are static figures, and the right curve test is held in the head.", "settles": "The modality A/B in the build plan, and timing data per step from 10's fluency telemetry."}
 ],
 "sources": ["BC-CON-08012", "BC-SKL-08023", "BC-SKL-08024", "BC-SKL-08025", "BC-SKL-08026", "BC-EK-CHA-5A2", "ced:156", "BC-QA-08009", "BC-MCQ-CED-010", "sg-23:16", "BC-ERR-08020", "BC-ERR-08023", "BC-ERR-08024", "BC-ERR-99006", "BC-MIS-08011", "BC-MIS-08012", "BC-MIS-08013", "BC-PRQ-06005", "BC-PRQ-08002", "research/units/unit-08-applications-integration.md#8.5 Finding the Area Between Curves Expressed as Functions of y", "research/units/unit-08-applications-integration.md#Unresolved", "research/question-analysis/question-archetypes.md#BC-QA-08009 Area of a region integrated with respect to y", "research/exam/exam-structure.md#Section and part layout"]
}
```
