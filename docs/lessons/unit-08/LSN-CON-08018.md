---
title: LSN-CON-08018 Radius measured from a line other than an axis
research_date: 2026-09-29
status: designed
purpose: Authoring spec for the concept lesson on BC-CON-08018, the disc radius as a distance from a horizontal or vertical line that is not a coordinate axis, built from authoring_bundle("BC-CON-08018") and the research files it cites, so an author fills plan 15's lesson record without making a teaching decision.
---

# LSN-CON-08018 Radius measured from a line other than an axis

Concept BC-CON-08018 (skills BC-SKL-08044, BC-SKL-08045, BC-SKL-08046, BC-SKL-08047), topic 8.10 of Unit 8, loaded by BC-QA-08012 (family revolution-volume), the same archetype as LSN-CON-08017 with its axis parameter set to shifted. Hard parents BC-CON-08012 and BC-CON-08017 (docs/lessons/unit-08/README.md, section 1).

## Orientation

Served text, from BC-CON-08018 `description_plain` and the topic's Assessment behaviour paragraph (research/units/unit-08-applications-integration.md#8.10 Volume with Disc Method: Revolving Around Other Axes): when the axis is the line y = k, a response writes the radius as a difference from k, squares it, and keeps the limits where the region puts them. No count, no frequency.

## Key ideas

All four skills map to BC-EK-CHA-5C2 (ced:161): one core block, both bands.

- ki-1 (core). Paraphrase of the Radius and Limits paragraphs: the radius is the distance from the curve to the line, f(x) - k when the region lies above y = k and k - f(x) when below; the limits describe the region in the slicing variable and do not move with the axis. No anchor quote: the CHA-5.C.2 sentence on ced:161 is 25 words the brief band does not have.

## Recognition

BC-QA-08012 (research/question-analysis/question-archetypes.md#BC-QA-08012 Volume of a solid of revolution by the disc method): `common_givens` a region, an axis of revolution; `asked_to_produce` an integrand with a squared radius, the volume; `difficulty_variables` "whether the axis is a coordinate axis or another line". The signal: "revolved about the line y = k" with the region bounded by that same line. The MCQ holds the region and moves the axis, so the shifted radius is what discriminates (research/units/unit-08-applications-integration.md#8.10 Volume with Disc Method: Revolving Around Other Axes).

What says "not this concept": the axis is the x-axis or y-axis itself (BC-CON-08017); the region is held away from the line (BC-CON-08020).

## Method choice

- st-1, BC-QA-08012. Cue from `common_givens` and `difficulty_variables`. Method, `expected_solution_path[0]`: write the radius as a distance to the axis. Rival, `wrong_approaches`: shifting the limits of integration along with the axis; and `common_distractors`, the radius written without the shift. Separating feature: the axis moves the radius, never the interval. Both cue fields exist, so not inferred.

## Solution path

- ex-1, BC-QA-08012, both bands, no calculator. Draw: form square, scale 1, left 0, width 2, level 2, presentation formula, axis shifted. f(x) = x^2 + 2 on [0, 2], region between f and y = 2, revolved about y = 2. No published item carries it.
- ex-2, low band: form linear, scale 1, left 1, width 2, level -2, axis shifted; f(x) = x - 2 on [1, 3] about y = -2.
- Steps: the radius as a difference (new, then simplified), the disc area (new), the integral with the region's limits (new), the value (equivalent). A fluent solver writes the parenthesised difference, the integral and the value.

## Scoring

BC-QA-08012 lists BC-PT-99058, 99001, 99003, 99004, 99053. ex-1 tags BC-PT-99058 on the disc area and BC-PT-99001 on the integral; ex-2 tags BC-PT-99004 on the value. ex-1's answer point is untagged for the brief band (inferred array). Notation: the radius as one parenthesised difference guards against the parenthesis loss recorded as BC-ERR-99009 (research/units/unit-08-applications-integration.md#8.10 Volume with Disc Method: Revolving Around Other Axes; research/scoring/notation-requirements.md#Parentheses).

## Traps

Two errors meet the skills, in bundle order: BC-ERR-08038, BC-ERR-08039. Both served in both bands. On ex-1's draw.

- err-BC-ERR-08038: x^2 + 2 used as the radius. Possible reason, BC-MIS-08021.
- err-BC-ERR-08039: the limits moved up by 2 to [2, 4]. Possible reason, BC-MIS-08022.

## Representations

None as a separate block. The Representations paragraph's figure with a drawn axis to a radius expression (BC-REP-02 to BC-REP-01) is carried by ki-1's interactive.

## Prerequisite bridge

- BC-PRQ-08002, BC-PRQ-08004, each from its `description_plain` and `failure_signature`.

## Time

BC-QA-08012 is `either`: Section I Part A, 2.14 minutes (research/exam/exam-structure.md#Section and part layout) [inferred]. As a free response part, 2 points, 3.33 minutes (docs/lessons/unit-08/README.md, section 5). The seconds saved by writing the difference before expanding go on the antiderivative.

## Checks

- chk-1, completion of ex-1. Key 32pi/5.
- chk-2, isomorph: form root, scale 2, left 0, width 4, level 1, axis shifted; f = 1 + 2 sqrt(x) about y = 1. Key 32pi.
- No chk-3: the bundle holds two errors, and a 4-option MCQ needs three distractor paths (inferred array).

## Delivery

- orientation: text. Rule 6.
- ki-1: interactive. Rule 4 promoted: BC-REP-08 on BC-SKL-08044 to 08047, and BC-QA-08012 `difficulty_variables` name the axis as the varying quantity with the stem asking for the radius (docs/lessons/unit-08/README.md, section 6) [inferred; the modality A/B].
- ex-1, ex-2, the two error blocks: step_reveal. Rule 1.

## Band plan

- Low (full): orientation, ki-1, st-1, ex-1 and its lines, the two error blocks, chk-1, chk-2, ex-2 and its line, the bridges. 585 words, 4.0 minutes.
- Mid (brief): the same less ex-2. 442 words, 3.0 minutes.
- Refresher: ki-1, err-BC-ERR-08038, err-BC-ERR-08039, ex-1.

## Sources

- BC-CON-08018; BC-SKL-08044, BC-SKL-08045, BC-SKL-08046, BC-SKL-08047; BC-EK-CHA-5C2; ced:161
- BC-QA-08012; BC-PT-99058, BC-PT-99001, BC-PT-99004; BC-ERR-99009
- BC-ERR-08038, BC-ERR-08039; BC-MIS-08021, BC-MIS-08022
- BC-PRQ-08002, BC-PRQ-08004
- research/units/unit-08-applications-integration.md#8.10 Volume with Disc Method: Revolving Around Other Axes
- research/question-analysis/question-archetypes.md#BC-QA-08012 Volume of a solid of revolution by the disc method
- research/scoring/notation-requirements.md#Parentheses
- research/exam/exam-structure.md#Section and part layout
- [inferred] Part A for an either archetype; ex-1's answer point untagged; two checks only; ki-1 as an interactive. Each settled as the inferred array states.

## Machine record

```json
{
 "id": "LSN-CON-08018",
 "kind": "concept",
 "target_id": "BC-CON-08018",
 "unit": "08",
 "skills": ["BC-SKL-08044", "BC-SKL-08045", "BC-SKL-08046", "BC-SKL-08047"],
 "orientation": {
  "text": "About a line y = k, a response writes the radius as a difference from k, squares it, and keeps the region's limits.",
  "sources": ["BC-CON-08018", "research/units/unit-08-applications-integration.md#8.10 Volume with Disc Method: Revolving Around Other Axes"]
 },
 "key_ideas": [
  {
   "id": "ki-1",
   "ek_id": "BC-EK-CHA-5C2",
   "depth": "core",
   "text": "Radius: curve to line, f(x) - k with the region above y = k, k - f(x) below. The limits describe the region; they stay put.",
   "notation": "radius as f minus k or k minus f",
   "quote": null,
   "sources": ["BC-EK-CHA-5C2", "ced:161", "research/units/unit-08-applications-integration.md#8.10 Volume with Disc Method: Revolving Around Other Axes"]
  }
 ],
 "strategy": [
  {
   "id": "st-1",
   "archetype_id": "BC-QA-08012",
   "cue": "Revolved about a line y = k that bounds the region.",
   "method": "First line: radius = (f(x) - k).",
   "rival": "Shifting the limits with the axis, or the bare f(x).",
   "separating_feature": "The axis moves the radius, never the interval.",
   "sources": ["BC-QA-08012"],
   "evidence_tag": "verified"
  }
 ],
 "worked_examples": [
  {
   "id": "ex-1",
   "archetype_id": "BC-QA-08012",
   "bands": ["low", "mid"],
   "parameter_draw": {"form": "square", "scale": 1, "left": 0, "width": 2, "level": 2, "presentation": "formula", "axis": "shifted"},
   "problem": {"text": "R is bounded by y = x^2 + 2, y = 2 and x = 2. Find the volume about y = 2.", "command_verb": "find"},
   "calculator_status": "no_calculator",
   "steps": [
    {"cue": "Axis y = 2, R above.", "why": "Curve minus line.", "expr": "(x**2 + 2) - 2", "relation": "new"},
    {"cue": "Simplify.", "why": "Radius x^2.", "expr": "x**2", "relation": "equivalent"},
    {"cue": "Disc area.", "why": "pi r squared.", "expr": "pi*x**4", "relation": "new", "point_type_id": "BC-PT-99058"},
    {"cue": "R spans x = 0 to 2.", "why": "Limits unmoved.", "expr": "Integral(pi*x**4, (x, 0, 2))", "relation": "new", "point_type_id": "BC-PT-99001"},
    {"cue": "Integrate.", "why": "Keep pi.", "expr": "32*pi/5", "relation": "equivalent"}
   ],
   "answer": {"form": "symbolic", "expr": "32*pi/5"}
  },
  {
   "id": "ex-2",
   "archetype_id": "BC-QA-08012",
   "bands": ["low"],
   "parameter_draw": {"form": "linear", "scale": 1, "left": 1, "width": 2, "level": -2, "presentation": "formula", "axis": "shifted"},
   "problem": {"text": "R is bounded by y = x - 2, y = -2, x = 1 and x = 3. Find the volume when R is revolved about y = -2.", "command_verb": "find"},
   "calculator_status": "no_calculator",
   "steps": [
    {"cue": "Axis y = -2, R above it.", "why": "Curve minus line.", "expr": "(x - 2) - (-2)", "relation": "new"},
    {"cue": "Disc area.", "why": "pi r squared.", "expr": "pi*x**2", "relation": "new"},
    {"cue": "R spans 1 to 3.", "why": "Limits unmoved.", "expr": "Integral(pi*x**2, (x, 1, 3))", "relation": "new"},
    {"cue": "Integrate.", "why": "Keep pi.", "expr": "26*pi/3", "relation": "equivalent", "point_type_id": "BC-PT-99004"}
   ],
   "answer": {"form": "symbolic", "expr": "26*pi/3"}
  }
 ],
 "what_a_reader_scores": [
  {"example_id": "ex-1", "point_type_ids": ["BC-PT-99058", "BC-PT-99001"], "lines": [
   {"point_type_id": "BC-PT-99058", "text": "Volume integrand form. Earned by: An integrand of the correct volume form, a nonzero constant times the square of the function for a disc, or the stated cross-section area (sg-26:19, sg-22:18). Not earned by: A constant other than pi where pi is required, which sg-22:19 states blocks the answer point; a rotation about the wrong axis, which sg-26:19 lets earn the form point only."},
   {"point_type_id": "BC-PT-99001", "text": "Definite integral expression with correct limits. Earned by: A definite integral whose limits match the requested interval and whose integrand matches the requested quantity, with or without the differential (sg-26:4, sg-22:2). Not earned by: An unsupported numerical value, or a definite integral whose bounds are wrong (sg-22:18). Notation: Differential may be omitted; sg-22:2 accepts dx written for dt. sg-23:8 treats a missing differential as recoverable for this point but restricts later eligibility."}
  ]},
  {"example_id": "ex-2", "point_type_ids": ["BC-PT-99004"], "lines": [
   {"point_type_id": "BC-PT-99004", "text": "Answer with or without supporting work. Earned by: The correct value on its own, with no supporting work required (sg-25:3, sg-26:4). Not earned by: A value outside the accepted precision, or a value inconsistent with a required earlier step where the rubric imposes one. Precision: A reported decimal answer must be accurate to three places after the decimal point, rounded or truncated; at most one point per question is lost to inappropriate rounding (sg-25:2, sg-26:2). sg-26:4 also accepts a stated rounding to the nearest integer and several truncations."}
  ]}
 ],
 "common_errors": [
  {
   "error_id": "BC-ERR-08038",
   "observed_behavior": "The response revolves about a line other than an axis but writes the radius as the bare function value.",
   "scoring_consequence": "The setup point is lost.",
   "wrong_step": {"text": "Radius x^2 + 2.", "expr": "Integral(pi*(x**2 + 2)**2, (x, 0, 2))"},
   "right_step": {"text": "Radius x^2.", "expr": "Integral(pi*x**4, (x, 0, 2))"},
   "relation": "distinct",
   "possible_reason": {"misconception_id": "BC-MIS-08021", "text": "treats the disc and washer formulas as fixed in the function rather than as built from a distance to the axis"},
   "sources": ["BC-ERR-08038", "BC-MIS-08021"]
  },
  {
   "error_id": "BC-ERR-08039",
   "observed_behavior": "The interval of integration is translated by the same amount as the axis.",
   "scoring_consequence": "The setup point is lost and the value is wrong.",
   "wrong_step": {"text": "Limits 2 to 4.", "expr": "Integral(pi*x**4, (x, 2, 4))"},
   "right_step": {"text": "Limits 0 to 2.", "expr": "Integral(pi*x**4, (x, 0, 2))"},
   "relation": "distinct",
   "possible_reason": {"misconception_id": "BC-MIS-08022", "text": "treats the translation as applying to the whole integral rather than to the radius alone"},
   "sources": ["BC-ERR-08039", "BC-MIS-08022"]
  }
 ],
 "representations": null,
 "prerequisite_bridges": [
  {"prq_id": "BC-PRQ-08002", "text": "Integrating in y needs x written as a function of y."},
  {"prq_id": "BC-PRQ-08004", "text": "A distance to a line is the larger value minus the smaller, not a bare function value."}
 ],
 "time": {"exam_part": "I-A", "budget_minutes": 2.14, "source": "research/exam/exam-structure.md#Section and part layout", "written_steps": {"ex-1": [1, 4, 5]}, "skipped_steps": {"ex-1": [2, 3]}},
 "checks": [
  {
   "id": "chk-1",
   "check_kind": "completion",
   "format": "short_answer",
   "bands": ["low", "mid"],
   "archetype_id": "BC-QA-08012",
   "parameter_draw": {"form": "square", "scale": 1, "left": 0, "width": 2, "level": 2, "presentation": "formula", "axis": "shifted"},
   "completes": "ex-1",
   "stem": {"text": "Evaluate pi times the integral of x^4 from 0 to 2.", "command_verb": "evaluate"},
   "key": {"form": "symbolic", "expr": "32*pi/5"},
   "steps": [
    {"text": "The integral.", "expr": "Integral(pi*x**4, (x, 0, 2))", "relation": "new"},
    {"text": "pi x^5/5 from 0 to 2.", "expr": "32*pi/5", "relation": "equivalent"}
   ],
   "calculator_status": "no_calculator",
   "skills": ["BC-SKL-08046"]
  },
  {
   "id": "chk-2",
   "check_kind": "isomorph",
   "format": "short_answer",
   "bands": ["low", "mid"],
   "archetype_id": "BC-QA-08012",
   "parameter_draw": {"form": "root", "scale": 2, "left": 0, "width": 4, "level": 1, "presentation": "formula", "axis": "shifted"},
   "stem": {"text": "R is bounded by y = 1 + 2 sqrt(x), y = 1 and x = 4. Find the volume about y = 1.", "command_verb": "find"},
   "key": {"form": "symbolic", "expr": "32*pi"},
   "steps": [
    {"text": "Radius.", "expr": "(1 + 2*sqrt(x)) - 1", "relation": "new"},
    {"text": "Disc area.", "expr": "4*pi*x", "relation": "new"},
    {"text": "Limits 0 and 4.", "expr": "Integral(4*pi*x, (x, 0, 4))", "relation": "new"},
    {"text": "Value.", "expr": "32*pi", "relation": "equivalent"}
   ],
   "calculator_status": "no_calculator",
   "skills": ["BC-SKL-08044"]
  }
 ],
 "delivery": [
  {"block": "orientation", "mode": "text", "reason": "rule 6: a statement of what a response shows", "sources": ["BC-CON-08018"]},
  {"block": "ki-1", "mode": "interactive", "reason": "rule 4 promoted: BC-REP-08 on BC-SKL-08044 to BC-SKL-08047; BC-QA-08012 difficulty_variables name the axis as the varying quantity and the stem asks for the radius", "sources": ["BC-SKL-08044", "BC-SKL-08047", "BC-QA-08012"],
   "spec": {"kind": "region_with_axis", "representations": ["BC-REP-02", "BC-REP-08"],
    "curve": "y = x^2 + 2", "interval": [0, 2], "region_lower": "y = 2",
    "controls": [{"type": "slider", "name": "k", "range": [-2, 2], "step": 1, "start": 0, "drives": "the axis line y = k"}],
    "drawn": ["the axis y = k", "the radius at x = 1 from the curve to the axis", "the limits x = 0 and x = 2 marked on the region"],
    "labels": [{"text": "r = (x^2 + 2) - k", "placement": "inside"}, {"text": "x = 0", "placement": "inside"}, {"text": "x = 2", "placement": "inside"}],
    "question": "As k moves, what happens to the radius at x = 1, and to the limits?"},
   "fallback": "a static figure with the axis at y = 0 and at y = 2, the radius at x = 1 marked on each, the limits marked once, labels inside",
   "keyboard": "Tab focuses the slider; Up and Down arrow keys move k by 1; Enter reads the radius at x = 1"},
  {"block": "ex-1", "mode": "step_reveal", "reason": "rule 1", "sources": []},
  {"block": "ex-2", "mode": "step_reveal", "reason": "rule 1", "sources": []},
  {"block": "err-BC-ERR-08038", "mode": "step_reveal", "reason": "rule 1", "sources": []},
  {"block": "err-BC-ERR-08039", "mode": "step_reveal", "reason": "rule 1", "sources": []}
 ],
 "refresher": ["ki-1", "err-BC-ERR-08038", "err-BC-ERR-08039", "ex-1"],
 "read_minutes": {"full": 4.0, "brief": 3.0},
 "word_count": {"full": 585, "brief": 442},
 "research_lines": [
  {"file": "research/units/unit-08-applications-integration.md", "line": "they do not move when the axis moves"}
 ],
 "inferred": [
  {"claim": "BC-QA-08012 is calculator status either, so the lesson takes Section I Part A and its 2.14 minute budget.", "settles": "Timing data on shifted disc items split by exam part."},
  {"claim": "ex-1's answer point (BC-PT-99004) is earned but not tagged, because its reader line would take the brief band past 450 words; ex-2 carries the tag.", "settles": "A shorter reader line or a brief cap that admits it."},
  {"claim": "The lesson carries two checks: the bundle holds two errors, fewer than the three distractor paths a 4-option MCQ needs.", "settles": "A third BC-ERR on the skills of BC-CON-08018."},
  {"claim": "ki-1 is served as an interactive with one slider for the axis line.", "settles": "The modality A/B in the build plan: skip rate and time to first credited success by mode."},
  {"claim": "The k - f(x) case, a region below the axis, is stated in ki-1 but not drawn: BC-QA-08012's parameter_spec places every region above its line.", "settles": "A parameter_spec that draws a region below a shifted axis."}
 ],
 "sources": ["BC-CON-08018", "BC-SKL-08044", "BC-SKL-08045", "BC-SKL-08046", "BC-SKL-08047", "BC-EK-CHA-5C2", "ced:161", "BC-QA-08012", "BC-PT-99058", "BC-PT-99001", "BC-PT-99004", "BC-ERR-99009", "BC-ERR-08038", "BC-ERR-08039", "BC-MIS-08021", "BC-MIS-08022", "BC-PRQ-08002", "BC-PRQ-08004", "research/units/unit-08-applications-integration.md#8.10 Volume with Disc Method: Revolving Around Other Axes", "research/question-analysis/question-archetypes.md#BC-QA-08012 Volume of a solid of revolution by the disc method", "research/scoring/notation-requirements.md#Parentheses", "research/exam/exam-structure.md#Section and part layout"]
}
```
