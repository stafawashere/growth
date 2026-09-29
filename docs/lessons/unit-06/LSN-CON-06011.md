---
title: LSN-CON-06011 Algebraic properties of the definite integral
research_date: 2026-09-29
status: designed
purpose: Authoring spec for the concept lesson on BC-CON-06011, the constant multiple, sum, reversal, adjacent interval and degenerate interval properties and integrals across a jump, built from authoring_bundle("BC-CON-06011") and the research files it cites, so an author fills plan 15's lesson record without making a teaching decision.
---

# LSN-CON-06011 Algebraic properties of the definite integral

Concept BC-CON-06011 (skills BC-SKL-06029 to BC-SKL-06033), topic 6.6 of Unit 6, loaded by BC-QA-06013 (primary, family integral-properties) and BC-QA-99010 (integral-comparison-bound). Hard parent BC-CON-06005 (docs/lessons/unit-06/README.md, section 1).

## Orientation

Served text, from BC-CON-06011 `description_plain` and the topic's Assessment behaviour paragraph (research/units/unit-06-integration-accumulation.md#6.6 Applying Properties of Definite Integrals): a response rewrites the requested integral in terms of the supplied ones, by splitting, joining, factoring and reversing, and substitutes only at the end. No count, no frequency.

## Key ideas

BC-SKL-06029 to BC-SKL-06032 map to BC-EK-FUN-6A2 (ced:123); BC-SKL-06033 maps to BC-EK-FUN-6A3 (ced:123). Two blocks: ki-1 core, ki-2 extended (low band).

- ki-1 (core, BC-EK-FUN-6A2). Paraphrase of the Required mathematical knowledge paragraphs "Properties" and "Notation": constants factor out, a sum splits, reversing the limits changes the sign, adjacent intervals add, and the integral from a to a is 0. No anchor quote, to keep the brief band under its cap. Notation line from the concept record.
- ki-2 (extended, BC-EK-FUN-6A3). Paraphrase of the "Discontinuities" paragraph: a function with a jump is integrated piece by piece, split at the jump; the value at a single point does not change the integral.

## Recognition

BC-QA-06013 (research/question-analysis/question-archetypes.md#BC-QA-06013 Manipulating definite integrals with their properties): `typical_wording` "the values of two definite integrals over stated intervals are given; find the value of a third definite integral"; `common_givens` the value of a definite integral over a stated interval, a graph of a piecewise linear function; `asked_to_produce` the value over a different interval, the integral of a linear combination. The signal: integral values supplied as numbers and a requested integral whose interval or integrand differs from theirs. Shapes: MCQ (BC-MCQ-PE2012-031) and parts inside FRQ (BC-FRQ-2019-Q3-A, BC-FRQ-2019-Q3-B).

BC-QA-99010 (research/question-analysis/question-archetypes.md#BC-QA-99010 Accumulation bounded above by a comparison function with a supplied improper integral): a total over a split interval, with an unknown function bounded by a comparison function.

What says "not this concept": an integrand given by a formula with no supplied values selects part two (BC-CON-06012); a graph with no supplied values selects geometry (BC-CON-06010).

## Method choice

Two strategy blocks; st-1 serves both bands.

- st-1, BC-QA-06013. Method, `expected_solution_path[0]`: match each requested integral to the supplied ones. Rival from `wrong_approaches`: the sign kept when the limits are reversed (BC-ERR-99012). Separating feature: the requested lower limit exceeds the upper.
- st-2, BC-QA-99010. Method: split the accumulation where the model changes. Rival: claiming the total converges rather than bounding it. Separating feature: the second function is unknown, so only a bound is available.

## Solution path

- ex-1, BC-QA-06013, both bands, no calculator. Draw from `parameter_spec`: direction reversed, start 0, gaps [1, 2, 1], first_value 4, whole_value 9, multiple 3, steps [2, -1]. So a = 0, b = 1, d = 3, c = 4; forward_value 18, key -18; jump_error -12, lower_error 18, limit_error -30, pairwise distinct as the constraints require. No published BC-QA-06013 item carries this draw.
- Steps follow `expected_solution_path`: the integral of f from 1 to 4 as 9 - 4 (new, adjacent intervals), its value (equivalent), the combination with h split at the jump 3 (new), its value (equivalent), the reversal (new, tagged BC-PT-99004). A fluent solver writes the combination line and the answer; the matching is held.

## Scoring

BC-QA-06013 lists BC-PT-99005, BC-PT-99069 and BC-PT-99004; its `scoring_pattern` records that a correct value alone earns the point (sg-25:18), so ex-1 tags BC-PT-99004 on the answer and its reader_checks line is in the machine record. An incorrect interval forfeits the point (same record). A wrong value imported into a later part carries its error forward (research/scoring/common-point-losses.md#Answer points).

## Traps

Three active errors meet the skills, in the bundle's order (linked BC-MIS at severity high, then medium): BC-ERR-06031, BC-ERR-99012, BC-ERR-99032. Low band all three, mid band the first two. All on ex-1's draw.

- err-BC-ERR-06031: h taken as -1 across all of [1, 4], giving -12, against -18. Possible reason, words from BC-MIS-06026.
- err-BC-ERR-99012: the sign kept on reversal, 18, against -18. Possible reason, words from BC-MIS-99004.
- err-BC-ERR-99032: the whole supplied integral from 0 to 4 used, -30, against -18. Possible reason, words from BC-MIS-08012.

## Representations

None as a separate block; ki-1's table and ki-2's figure carry the topic's two conversions.

## Prerequisite bridge

None.

## Time

BC-QA-06013 is `no_calculator`, one part of a multipart FRQ or a single MCQ; the MCQ is its native shape here ("MCQ forms supply values of two integrals and ask for a third"), so Section I Part A, 2.14 minutes (research/exam/exam-structure.md#Section and part layout). The minutes go on the combination line; matching supplied integrals is held (docs/lessons/unit-06/README.md, section 5).

## Checks

- chk-1, completion of ex-1, both bands: the forward value 18 is given; the student reverses. Key -18.
- chk-2, isomorph, both bands. Draw: forward, start -1, gaps [2, 1, 2], first_value -3, whole_value 5, multiple 2, steps [1, 3]. Key 23.
- chk-3, MCQ, low band. Draw: reversed, start 1, gaps [2, 1, 1], first_value -2, whole_value 6, multiple -2, steps [3, -2]. Key 15. Distractors: 20 (BC-ERR-06031, jump_error), -15 (BC-ERR-99012, lower_error), 11 (BC-ERR-99032, limit_error).

## Delivery

- orientation: text. Rule 6.
- ki-1: table. Rule 5: BC-REP-03 on BC-SKL-06031, supplied integral values over adjacent intervals (docs/lessons/unit-06/README.md, section 6).
- ki-2: figure. Rule 4: BC-REP-02 on BC-SKL-06033, a jump discontinuity with the integral split at the jump [inferred; settled by the modality A/B].
- ex-1 and the three error blocks: step_reveal. Rule 1.

## Band plan

- Low (full): orientation, ki-1, ki-2, st-1, st-2, ex-1 with its scoring line, the three error blocks, chk-1 to chk-3. 650 words, 4.4 minutes (cap 900 and 6).
- Mid (brief): orientation, ki-1, st-1, ex-1 with its scoring line, err-BC-ERR-06031, err-BC-ERR-99012, chk-1, chk-2. 446 words, 3.0 minutes (cap 450 and 3).
- Refresher: ki-1, the three error blocks, ex-1.

## Sources

- BC-CON-06011; BC-SKL-06029, BC-SKL-06030, BC-SKL-06031, BC-SKL-06032, BC-SKL-06033; BC-EK-FUN-6A2, BC-EK-FUN-6A3; ced:123
- BC-QA-06013, BC-QA-99010; BC-PT-99004; sg-25:18
- BC-ERR-06031, BC-ERR-99012, BC-ERR-99032; BC-MIS-06026, BC-MIS-99004, BC-MIS-08012
- research/units/unit-06-integration-accumulation.md#6.6 Applying Properties of Definite Integrals
- research/question-analysis/question-archetypes.md#BC-QA-06013 Manipulating definite integrals with their properties
- research/question-analysis/question-archetypes.md#BC-QA-99010 Accumulation bounded above by a comparison function with a supplied improper integral
- research/scoring/common-point-losses.md#Answer points
- research/exam/exam-structure.md#Section and part layout
- [inferred] ki-2 as a static figure. Settled by the modality A/B.
- [inferred] BC-QA-06013's scoring is itself inferred in the record from parts where a value alone earns the point. Settled by a scoring guideline for a dedicated properties part.

## Machine record

```json
{
 "id": "LSN-CON-06011",
 "kind": "concept",
 "target_id": "BC-CON-06011",
 "unit": "06",
 "skills": ["BC-SKL-06029", "BC-SKL-06030", "BC-SKL-06031", "BC-SKL-06032", "BC-SKL-06033"],
 "orientation": {
  "text": "A response rewrites the requested integral in terms of the supplied ones, by splitting, joining, factoring and reversing, and substitutes the numbers only at the end.",
  "sources": ["BC-CON-06011", "research/units/unit-06-integration-accumulation.md#6.6 Applying Properties of Definite Integrals"]
 },
 "key_ideas": [
  {
   "id": "ki-1",
   "ek_id": "BC-EK-FUN-6A2",
   "depth": "core",
   "text": "Constants factor out; sums split. Reversed limits change the sign. Adjacent intervals add: a to b plus b to c is a to c. From a to a is 0.",
   "notation": "integral from a to b = minus integral from b to a",
   "quote": null,
   "sources": ["BC-EK-FUN-6A2", "ced:123", "research/units/unit-06-integration-accumulation.md#6.6 Applying Properties of Definite Integrals"]
  },
  {
   "id": "ki-2",
   "ek_id": "BC-EK-FUN-6A3",
   "depth": "extended",
   "text": "A function with a jump is integrated piece by piece, split at the jump. One point's value changes nothing.",
   "notation": "split at the discontinuity",
   "quote": null,
   "sources": ["BC-EK-FUN-6A3", "ced:123", "research/units/unit-06-integration-accumulation.md#6.6 Applying Properties of Definite Integrals"]
  }
 ],
 "strategy": [
  {
   "id": "st-1",
   "archetype_id": "BC-QA-06013",
   "cue": "Values of two integrals supplied; a third, over another interval or integrand, asked.",
   "method": "First line: the requested integral matched to the supplied ones.",
   "rival": "Rival: the sign kept on reversed limits (BC-ERR-99012).",
   "separating_feature": "A requested lower limit above the upper.",
   "sources": ["BC-QA-06013"],
   "evidence_tag": "verified"
  },
  {
   "id": "st-2",
   "archetype_id": "BC-QA-99010",
   "cue": "A model on a first interval, a comparison function beyond, its improper integral supplied; a bound asked.",
   "method": "First line: the accumulation split where the model changes.",
   "rival": "Rival: claiming the total converges rather than bounding it.",
   "separating_feature": "The second function is unknown, so only a bound is available.",
   "sources": ["BC-QA-99010"],
   "evidence_tag": "verified"
  }
 ],
 "worked_examples": [
  {
   "id": "ex-1",
   "archetype_id": "BC-QA-06013",
   "bands": ["low", "mid"],
   "parameter_draw": {"direction": "reversed", "start": 0, "gaps": [1, 2, 1], "first_value": 4, "whole_value": 9, "multiple": 3, "steps": [2, -1]},
   "problem": {"text": "f from 0 to 1 is 4; from 0 to 4 is 9. h = 2 for x < 3, -1 after. Find the integral from 4 to 1 of (3f + h).", "command_verb": "find"},
   "calculator_status": "no_calculator",
   "steps": [
    {"cue": "Request spans 1 to 4; supplied ones start at 0.", "why": "Adjacent intervals.", "expr": "9 - 4", "relation": "new"},
    {"cue": "Subtract.", "why": "f from 1 to 4.", "expr": "5", "relation": "equivalent"},
    {"cue": "h jumps at 3.", "why": "Factor 3; split h at 3.", "expr": "3*5 + 2*(3 - 1) + (-1)*(4 - 3)", "relation": "new"},
    {"cue": "Add.", "why": "Forward value.", "expr": "18", "relation": "equivalent"},
    {"cue": "The stem runs 4 to 1.", "why": "Reversal changes the sign.", "expr": "-18", "relation": "new", "point_type_id": "BC-PT-99004"}
   ],
   "answer": {"form": "symbolic", "expr": "-18"}
  }
 ],
 "what_a_reader_scores": [
  {"example_id": "ex-1", "point_type_ids": ["BC-PT-99004"], "lines": [{"point_type_id": "BC-PT-99004", "text": "Answer with or without supporting work. Earned by: The correct value on its own, with no supporting work required (sg-25:3, sg-26:4). Not earned by: A value outside the accepted precision, or a value inconsistent with a required earlier step where the rubric imposes one. Precision: A reported decimal answer must be accurate to three places after the decimal point, rounded or truncated; at most one point per question is lost to inappropriate rounding (sg-25:2, sg-26:2). sg-26:4 also accepts a stated rounding to the nearest integer and several truncations."}]}
 ],
 "common_errors": [
  {
   "error_id": "BC-ERR-06031",
   "observed_behavior": "A function with a jump on the interval of integration is antidifferentiated as a single expression across the jump.",
   "scoring_consequence": "The value point is lost because the antiderivative used is not valid across the whole interval.",
   "wrong_step": {"text": "h as -1 on all of [1, 4].", "expr": "-(3*5 + (-1)*(4 - 1))"},
   "right_step": {"text": "h split at 3.", "expr": "-18"},
   "relation": "distinct",
   "possible_reason": {"misconception_id": "BC-MIS-06026", "text": "applies F(b) minus F(a) without checking that the integrand is continuous on the interval"},
   "sources": ["BC-ERR-06031", "BC-MIS-06026"]
  },
  {
   "error_id": "BC-ERR-99012",
   "observed_behavior": "Responses write the integral of f prime from a to x as f of x, ignoring the value at the lower limit, or mishandle a reversed pair of limits and report the wrong sign for an accumulated area.",
   "scoring_consequence": "The value or setup point in that part is not earned, and the error usually propagates to later parts that build on the value.",
   "wrong_step": {"text": "Sign kept.", "expr": "18"},
   "right_step": {"text": "Sign changed.", "expr": "-18"},
   "relation": "distinct",
   "possible_reason": {"misconception_id": "BC-MIS-99004", "text": "the direction of the limits play no role"},
   "sources": ["BC-ERR-99012", "BC-MIS-99004"]
  },
  {
   "error_id": "BC-ERR-99032",
   "observed_behavior": "Responses asked for an integral expression write statements that are not integral expressions, such as the function set equal to its own integral, a summation sign placed in front of an integral, or a constant of integration attached to a definite integral, and some reverse the limits or use limits that were never given.",
   "scoring_consequence": "The expression point is not earned, since the requested object is an integral expression and nothing else is being scored in that part.",
   "wrong_step": {"text": "f over 0 to 4 used.", "expr": "-(3*9 + 2*2 + (-1)*1)"},
   "right_step": {"text": "f over 1 to 4.", "expr": "-18"},
   "relation": "distinct",
   "possible_reason": {"misconception_id": "BC-MIS-08012", "text": "from the stated domain instead of from where the region actually begins and ends"},
   "sources": ["BC-ERR-99032", "BC-MIS-08012"]
  }
 ],
 "representations": null,
 "prerequisite_bridges": [],
 "time": {"exam_part": "I-A", "budget_minutes": 2.14, "source": "research/exam/exam-structure.md#Section and part layout", "written_steps": {"ex-1": [3, 5]}, "skipped_steps": {"ex-1": [1, 2, 4]}},
 "checks": [
  {
   "id": "chk-1",
   "check_kind": "completion",
   "format": "short_answer",
   "bands": ["low", "mid"],
   "archetype_id": "BC-QA-06013",
   "parameter_draw": {"direction": "reversed", "start": 0, "gaps": [1, 2, 1], "first_value": 4, "whole_value": 9, "multiple": 3, "steps": [2, -1]},
   "completes": "ex-1",
   "stem": {"text": "From 1 to 4 it is 18. Find it from 4 to 1.", "command_verb": "find"},
   "key": {"form": "symbolic", "expr": "-18"},
   "steps": [
    {"text": "Forward value.", "expr": "18", "relation": "new"},
    {"text": "Reversed.", "expr": "-18", "relation": "new"}
   ],
   "calculator_status": "no_calculator",
   "skills": ["BC-SKL-06030"]
  },
  {
   "id": "chk-2",
   "check_kind": "isomorph",
   "format": "short_answer",
   "bands": ["low", "mid"],
   "archetype_id": "BC-QA-06013",
   "parameter_draw": {"direction": "forward", "start": -1, "gaps": [2, 1, 2], "first_value": -3, "whole_value": 5, "multiple": 2, "steps": [1, 3]},
   "stem": {"text": "f from -1 to 1 is -3; from -1 to 4 is 5. h = 1 for x < 2, 3 after. Find 1 to 4 of (2f + h).", "command_verb": "find"},
   "key": {"form": "symbolic", "expr": "23"},
   "steps": [
    {"text": "f from 1 to 4.", "expr": "5 - (-3)", "relation": "new"},
    {"text": "Combination.", "expr": "2*8 + 1*(2 - 1) + 3*(4 - 2)", "relation": "new"},
    {"text": "Value.", "expr": "23", "relation": "equivalent"}
   ],
   "calculator_status": "no_calculator",
   "skills": ["BC-SKL-06031"]
  },
  {
   "id": "chk-3",
   "check_kind": "mcq",
   "format": "mcq",
   "bands": ["low"],
   "archetype_id": "BC-QA-06013",
   "parameter_draw": {"direction": "reversed", "start": 1, "gaps": [2, 1, 1], "first_value": -2, "whole_value": 6, "multiple": -2, "steps": [3, -2]},
   "stem": {"text": "f from 1 to 3 is -2; from 1 to 5 is 6. h = 3 for x < 4, -2 after. The integral from 5 to 3 of (-2f + h) is", "command_verb": "identify"},
   "key": {"form": "symbolic", "expr": "15"},
   "steps": [
    {"text": "f from 3 to 5.", "expr": "6 - (-2)", "relation": "new"},
    {"text": "Forward combination.", "expr": "-2*8 + 3*(4 - 3) + (-2)*(5 - 4)", "relation": "new"},
    {"text": "Value.", "expr": "-15", "relation": "equivalent"},
    {"text": "Reversed.", "expr": "15", "relation": "new"}
   ],
   "options": [
    {"id": "A", "is_key": false, "expr": "20", "error_path": "BC-ERR-06031", "derivation": "h taken as -2 across the whole interval, no split at the jump"},
    {"id": "B", "is_key": false, "expr": "-15", "error_path": "BC-ERR-99012", "derivation": "the forward value, sign kept on reversal"},
    {"id": "C", "is_key": true, "expr": "15", "error_path": null},
    {"id": "D", "is_key": false, "expr": "11", "error_path": "BC-ERR-99032", "derivation": "the supplied integral from 1 to 5 used in place of 3 to 5"}
   ],
   "calculator_status": "no_calculator",
   "skills": ["BC-SKL-06030"]
  }
 ],
 "delivery": [
  {"block": "orientation", "mode": "text", "reason": "rule 6: a statement of what a response writes", "sources": ["BC-SKL-06029"]},
  {"block": "ki-1", "mode": "table", "reason": "rule 5: BC-REP-03 on BC-SKL-06031, supplied integral values over adjacent intervals", "sources": ["BC-SKL-06031"],
   "spec": {"kind": "table", "representations": ["BC-REP-03"], "columns": ["interval", "[0, 1]", "[1, 4]", "[0, 4]"], "rows": [["integral of f", "4", "?", "9"]],
    "labels": [{"text": "[0, 1] + [1, 4] = [0, 4]", "placement": "inside"}, {"text": "? = 9 - 4", "placement": "inside"}]},
   "fallback": "the table as plain text rows", "keyboard": "Tab moves between cells; no control"},
  {"block": "ki-2", "mode": "figure", "reason": "rule 4: BC-REP-02 on BC-SKL-06033, a jump discontinuity with the integral split at the jump", "sources": ["BC-SKL-06033"],
   "spec": {"kind": "graph", "representations": ["BC-REP-02"], "window": {"x": [0, 5], "y": [-2, 3]},
    "curves": [{"expr": "2", "domain": [1, 3], "open_end": 3}, {"expr": "-1", "domain": [3, 4], "closed_start": 3}],
    "drawn": ["rectangle of height 2 on [1, 3] shaded above", "rectangle of height -1 on [3, 4] shaded below"],
    "labels": [{"text": "jump at 3: split here", "placement": "inside"}, {"text": "2 times 2 = 4", "placement": "inside"}, {"text": "-1 times 1 = -1", "placement": "inside"}]},
   "fallback": "the same figure described in text: h is 2 on [1, 3] and -1 on [3, 4], integrated as 4 plus -1",
   "keyboard": "none needed; the figure has no control"},
  {"block": "ex-1", "mode": "step_reveal", "reason": "rule 1", "sources": []},
  {"block": "err-BC-ERR-06031", "mode": "step_reveal", "reason": "rule 1", "sources": []},
  {"block": "err-BC-ERR-99012", "mode": "step_reveal", "reason": "rule 1", "sources": []},
  {"block": "err-BC-ERR-99032", "mode": "step_reveal", "reason": "rule 1", "sources": []}
 ],
 "refresher": ["ki-1", "err-BC-ERR-06031", "err-BC-ERR-99012", "err-BC-ERR-99032", "ex-1"],
 "read_minutes": {"full": 4.4, "brief": 3.0},
 "word_count": {"full": 650, "brief": 446},
 "research_lines": [
  {"file": "research/units/unit-06-integration-accumulation.md", "line": "The integral from a to b equals the negative of the integral from b to a"}
 ],
 "inferred": [
  {"claim": "ki-2 is served as a static figure rather than text.", "settles": "The modality A/B in the build plan: skip rate and time to first credited success by mode."},
  {"claim": "BC-QA-06013's scoring pattern is inferred in the record from parts where a correct value alone earns the point.", "settles": "A scoring guideline for a dedicated properties part."}
 ],
 "sources": ["BC-CON-06011", "BC-SKL-06029", "BC-SKL-06030", "BC-SKL-06031", "BC-SKL-06032", "BC-SKL-06033", "BC-EK-FUN-6A2", "BC-EK-FUN-6A3", "ced:123", "BC-QA-06013", "BC-QA-99010", "BC-PT-99004", "sg-25:18", "BC-ERR-06031", "BC-ERR-99012", "BC-ERR-99032", "BC-MIS-06026", "BC-MIS-99004", "BC-MIS-08012", "research/units/unit-06-integration-accumulation.md#6.6 Applying Properties of Definite Integrals", "research/question-analysis/question-archetypes.md#BC-QA-06013 Manipulating definite integrals with their properties", "research/exam/exam-structure.md#Section and part layout"]
}
```
