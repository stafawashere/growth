---
title: LSN-CON-08017 Disc method for a solid of revolution
research_date: 2026-09-29
status: designed
purpose: Authoring spec for the concept lesson on BC-CON-08017, the disc method for a region touching its axis of revolution, built from authoring_bundle("BC-CON-08017") and the research files it cites, so an author fills plan 15's lesson record without making a teaching decision.
---

# LSN-CON-08017 Disc method for a solid of revolution

Concept BC-CON-08017 (skills BC-SKL-08040, BC-SKL-08041, BC-SKL-08042, BC-SKL-08043), topic 8.9 of Unit 8, loaded by one archetype, BC-QA-08012 (family revolution-volume). Hard parents BC-CON-08012 and BC-CON-08015 (docs/lessons/unit-08/README.md, section 1). It opens the revolution chain: 08018 and 08019 build on it, then 08020.

## Orientation

Served text, from BC-CON-08017 `description_plain` and the topic's Assessment behaviour paragraph (research/units/unit-08-applications-integration.md#8.9 Volume with Disc Method: Revolving Around the x- or y-Axis): a response writes pi times the integral of the squared radius, with limits, and reports the volume, as a multiple of pi when no calculator is allowed. No count, no frequency.

## Key ideas

All four skills map to BC-EK-CHA-5C1 (ced:160): one core block, both bands.

- ki-1 (core). Paraphrase of the Disc method, Variable of integration and Notation paragraphs: the region meets the axis, so each slice is a disc whose radius is the distance from the curve to the axis; about the x-axis the integral is in x; pi multiplies the whole integral and the radius is squared before integrating. No anchor quote (brief band, Band plan).

## Recognition

BC-QA-08012 (research/question-analysis/question-archetypes.md#BC-QA-08012 Volume of a solid of revolution by the disc method): `typical_wording` "the region is revolved about the stated line; find the volume of the solid generated"; `common_givens` a region, an axis of revolution; `asked_to_produce` an integrand with a squared radius, the volume. The signal: "revolved about" with a region bounded by the curve and that axis. Shapes: an MCQ with the unsquared radius and the missing pi as distractors, or one part built on a region from an earlier area part (official examples BC-FRQ-2021-Q3-C, BC-FRQ-2022-Q5-C, BC-FRQ-2026-Q5-B).

What says "not this concept": a gap between the region and the axis selects a washer (BC-CON-08019); "cross sections perpendicular" with nothing revolved selects BC-CON-08014 (docs/lessons/unit-08/README.md, section 3).

## Method choice

- st-1, BC-QA-08012. Cue from `asked_to_produce` and `common_givens`. Method, `expected_solution_path[0]`: write the radius as a distance to the axis. Rival, `common_distractors`: the radius left unsquared, pi omitted. The archetype's `wrong_approaches` entry (limits shifted with the axis) belongs to LSN-CON-08018. Separating feature: a disc is a circle, so its area is pi r squared. Both cue fields exist, so not inferred.

## Solution path

- ex-1, BC-QA-08012, both bands, no calculator. Draw: form root, scale 1, left 0, width 4, level 1, presentation formula, axis x_axis. f(x) = sqrt(x) on [0, 4], revolved about the x-axis. No published item carries it.
- ex-2, low band: form square, scale 1, left 0, width 2, level 1, axis x_axis; f(x) = x^2 on [0, 2].
- Steps: the radius (new), the disc area (new), the integral with limits (new), the value (equivalent). A fluent solver writes the integral and the value; the radius is held when it is the function itself.

## Scoring

BC-QA-08012 lists BC-PT-99058, 99001, 99003, 99004, 99053. ex-1 tags BC-PT-99001 on the integral; ex-2 tags BC-PT-99058 on the disc area and BC-PT-99004 on the value. ex-1's form and answer points are untagged for the brief band (inferred array). BC-PT-99003 and 99053 name no step here (no antiderivative line is written; no improper integral). Point loss: a revolution with a missing constant is the wrong volume family (research/scoring/common-point-losses.md#Setup points).

## Traps

Six errors meet the skills; the first four in bundle order are served: BC-ERR-08023, BC-ERR-08024, BC-ERR-08036, BC-ERR-08037. BC-ERR-99011 and BC-ERR-99019 fall past the cap. On ex-1's draw.

- err-BC-ERR-08023: pi x integrated in y. Possible reason, BC-MIS-08013.
- err-BC-ERR-08024: the y values 0 and 2 used as the x limits. Possible reason, BC-MIS-08012.
- err-BC-ERR-08036: sqrt(x) unsquared. Possible reason, BC-MIS-08020.
- err-BC-ERR-08037: pi dropped. Possible reason, BC-MIS-08019.

## Representations

None as a separate block. The Representations paragraph's region and axis to a disc diagram (BC-REP-02 to BC-REP-08) is carried by ki-1's motion.

## Prerequisite bridge

- BC-PRQ-06002, BC-PRQ-08002, BC-PRQ-08004, each from its `description_plain` and `failure_signature`.

## Time

BC-QA-08012 is `either`: Section I Part A, 2.14 minutes (research/exam/exam-structure.md#Section and part layout) [inferred]. As a free response part, 2 points, 3.33 minutes (docs/lessons/unit-08/README.md, section 5). The minutes go on the antiderivative of the squared radius.

## Checks

- chk-1, completion of ex-1. Key 8pi.
- chk-2, isomorph: form linear, scale 3, left 0, width 2, level 1, axis x_axis; f = 3x. Key 24pi.
- chk-3, MCQ, low band: form root, scale 2, left 1, width 3, level 2, axis x_axis; f = 2 sqrt(x) on [1, 4]. Key 30pi. Distractors 24pi (BC-ERR-08024, y values 2 and 4 as limits), 28pi/3 (BC-ERR-08036), 30 (BC-ERR-08037).

## Delivery

- orientation: text. Rule 6.
- ki-1: motion. Rule 2, a region swept about the axis into a solid (docs/lessons/unit-08/README.md, section 6); BC-REP-08 on BC-SKL-08040 for the fallback [inferred; the modality A/B].
- ex-1, ex-2, the four error blocks: step_reveal. Rule 1.

## Band plan

- Low (full): orientation, ki-1, st-1, ex-1 and its line, the four error blocks, chk-1 to chk-3, ex-2 and its lines, the bridges. 764 words, 5.1 minutes.
- Mid (brief): orientation, ki-1, st-1, ex-1 and its line, err-BC-ERR-08023, err-BC-ERR-08024, chk-1, chk-2, the bridges. 446 words, 3.0 minutes.
- Refresher: ki-1, the four error blocks, ex-1.

## Sources

- BC-CON-08017; BC-SKL-08040, BC-SKL-08041, BC-SKL-08042, BC-SKL-08043; BC-EK-CHA-5C1; ced:160
- BC-QA-08012; BC-PT-99058, BC-PT-99001, BC-PT-99004
- BC-ERR-08023, BC-ERR-08024, BC-ERR-08036, BC-ERR-08037; BC-MIS-08012, BC-MIS-08013, BC-MIS-08019, BC-MIS-08020
- BC-PRQ-06002, BC-PRQ-08002, BC-PRQ-08004
- research/units/unit-08-applications-integration.md#8.9 Volume with Disc Method: Revolving Around the x- or y-Axis
- research/question-analysis/question-archetypes.md#BC-QA-08012 Volume of a solid of revolution by the disc method
- research/scoring/common-point-losses.md#Setup points
- research/exam/exam-structure.md#Section and part layout
- [inferred] Part A for an either archetype; ex-1's form and answer points untagged; ki-1 as motion; two errors past the cap. Each settled as the inferred array states.

## Machine record

```json
{
 "id": "LSN-CON-08017",
 "kind": "concept",
 "target_id": "BC-CON-08017",
 "unit": "08",
 "skills": ["BC-SKL-08040", "BC-SKL-08041", "BC-SKL-08042", "BC-SKL-08043"],
 "orientation": {
  "text": "A region touching its axis, revolved, is a stack of discs. A response writes pi times the integral of the squared radius, with limits, and reports the volume, as a multiple of pi without a calculator.",
  "sources": ["BC-CON-08017", "research/units/unit-08-applications-integration.md#8.9 Volume with Disc Method: Revolving Around the x- or y-Axis"]
 },
 "key_ideas": [
  {
   "id": "ki-1",
   "ek_id": "BC-EK-CHA-5C1",
   "depth": "core",
   "text": "The region meets the axis, so each slice is a disc; its radius is the distance from curve to axis. About the x-axis, integrate in x. Pi multiplies the integral; the radius is squared before integrating.",
   "notation": "pi times the integral of the radius squared",
   "quote": null,
   "sources": ["BC-EK-CHA-5C1", "ced:160", "research/units/unit-08-applications-integration.md#8.9 Volume with Disc Method: Revolving Around the x- or y-Axis"]
  }
 ],
 "strategy": [
  {
   "id": "st-1",
   "archetype_id": "BC-QA-08012",
   "cue": "A region against its axis, revolved; asked for the volume.",
   "method": "First line: the radius as distance to the axis.",
   "rival": "Radius unsquared, or pi dropped.",
   "separating_feature": "A disc is a circle: pi r squared.",
   "sources": ["BC-QA-08012"],
   "evidence_tag": "verified"
  }
 ],
 "worked_examples": [
  {
   "id": "ex-1",
   "archetype_id": "BC-QA-08012",
   "bands": ["low", "mid"],
   "parameter_draw": {"form": "root", "scale": 1, "left": 0, "width": 4, "level": 1, "presentation": "formula", "axis": "x_axis"},
   "problem": {"text": "R is bounded by y = sqrt(x), the x-axis and x = 4. Find the volume when R is revolved about the x-axis.", "command_verb": "find"},
   "calculator_status": "no_calculator",
   "steps": [
    {"cue": "R touches the x-axis, the axis.", "why": "Radius: curve to axis.", "expr": "sqrt(x)", "relation": "new"},
    {"cue": "Each slice is a disc.", "why": "pi r squared.", "expr": "pi*x", "relation": "new"},
    {"cue": "R runs from x = 0 to 4.", "why": "Slices in x.", "expr": "Integral(pi*x, (x, 0, 4))", "relation": "new", "point_type_id": "BC-PT-99001"},
    {"cue": "Integrate.", "why": "Keep pi.", "expr": "8*pi", "relation": "equivalent"}
   ],
   "answer": {"form": "symbolic", "expr": "8*pi"}
  },
  {
   "id": "ex-2",
   "archetype_id": "BC-QA-08012",
   "bands": ["low"],
   "parameter_draw": {"form": "square", "scale": 1, "left": 0, "width": 2, "level": 1, "presentation": "formula", "axis": "x_axis"},
   "problem": {"text": "R is bounded by y = x^2, the x-axis and x = 2. Find the volume when R is revolved about the x-axis.", "command_verb": "find"},
   "calculator_status": "no_calculator",
   "steps": [
    {"cue": "R touches the axis.", "why": "Radius x^2.", "expr": "x**2", "relation": "new"},
    {"cue": "Disc area.", "why": "pi r squared.", "expr": "pi*x**4", "relation": "new", "point_type_id": "BC-PT-99058"},
    {"cue": "x from 0 to 2.", "why": "Limits.", "expr": "Integral(pi*x**4, (x, 0, 2))", "relation": "new"},
    {"cue": "Integrate.", "why": "Keep pi.", "expr": "32*pi/5", "relation": "equivalent", "point_type_id": "BC-PT-99004"}
   ],
   "answer": {"form": "symbolic", "expr": "32*pi/5"}
  }
 ],
 "what_a_reader_scores": [
  {"example_id": "ex-1", "point_type_ids": ["BC-PT-99001"], "lines": [
   {"point_type_id": "BC-PT-99001", "text": "Definite integral expression with correct limits. Earned by: A definite integral whose limits match the requested interval and whose integrand matches the requested quantity, with or without the differential (sg-26:4, sg-22:2). Not earned by: An unsupported numerical value, or a definite integral whose bounds are wrong (sg-22:18). Notation: Differential may be omitted; sg-22:2 accepts dx written for dt. sg-23:8 treats a missing differential as recoverable for this point but restricts later eligibility."}
  ]},
  {"example_id": "ex-2", "point_type_ids": ["BC-PT-99058", "BC-PT-99004"], "lines": [
   {"point_type_id": "BC-PT-99058", "text": "Volume integrand form. Earned by: An integrand of the correct volume form, a nonzero constant times the square of the function for a disc, or the stated cross-section area (sg-26:19, sg-22:18). Not earned by: A constant other than pi where pi is required, which sg-22:19 states blocks the answer point; a rotation about the wrong axis, which sg-26:19 lets earn the form point only."},
   {"point_type_id": "BC-PT-99004", "text": "Answer with or without supporting work. Earned by: The correct value on its own, with no supporting work required (sg-25:3, sg-26:4). Not earned by: A value outside the accepted precision, or a value inconsistent with a required earlier step where the rubric imposes one. Precision: A reported decimal answer must be accurate to three places after the decimal point, rounded or truncated; at most one point per question is lost to inappropriate rounding (sg-25:2, sg-26:2). sg-26:4 also accepts a stated rounding to the nearest integer and several truncations."}
  ]}
 ],
 "common_errors": [
  {
   "error_id": "BC-ERR-08023",
   "observed_behavior": "A function of x is integrated with respect to y, or the reverse, without being rewritten.",
   "scoring_consequence": "The setup point is lost because the expression does not define a number.",
   "wrong_step": {"text": "dy.", "expr": "Integral(pi*x, (y, 0, 4))"},
   "right_step": {"text": "dx.", "expr": "Integral(pi*x, (x, 0, 4))"},
   "relation": "distinct",
   "possible_reason": {"misconception_id": "BC-MIS-08013", "text": "treats dx and dy as labels for the direction of slicing"},
   "sources": ["BC-ERR-08023", "BC-MIS-08013"]
  },
  {
   "error_id": "BC-ERR-08024",
   "observed_behavior": "An integral in y carries x values as its limits.",
   "scoring_consequence": "The setup point is lost and the value is wrong.",
   "wrong_step": {"text": "y values as limits.", "expr": "Integral(pi*x, (x, 0, 2))"},
   "right_step": {"text": "x from 0 to 4.", "expr": "Integral(pi*x, (x, 0, 4))"},
   "relation": "distinct",
   "possible_reason": {"misconception_id": "BC-MIS-08012", "text": "chooses limits from the axes of the picture"},
   "sources": ["BC-ERR-08024", "BC-MIS-08012"]
  },
  {
   "error_id": "BC-ERR-08036",
   "observed_behavior": "The disc integrand is pi times the function rather than pi times the square of the function.",
   "scoring_consequence": "The setup point is lost.",
   "wrong_step": {"text": "Unsquared.", "expr": "Integral(pi*sqrt(x), (x, 0, 4))"},
   "right_step": {"text": "Squared.", "expr": "Integral(pi*x, (x, 0, 4))"},
   "relation": "distinct",
   "possible_reason": {"misconception_id": "BC-MIS-08020", "text": "carries the circle formula only as far as the factor pi"},
   "sources": ["BC-ERR-08036", "BC-MIS-08020"]
  },
  {
   "error_id": "BC-ERR-08037",
   "observed_behavior": "A disc or washer volume is reported without the constant factor pi.",
   "scoring_consequence": "The answer point is lost.",
   "wrong_step": {"text": "No pi.", "expr": "Integral(x, (x, 0, 4))"},
   "right_step": {"text": "pi.", "expr": "Integral(pi*x, (x, 0, 4))"},
   "relation": "distinct",
   "possible_reason": {"misconception_id": "BC-MIS-08019", "text": "remembers the squared dimension but not the fraction in front of it"},
   "sources": ["BC-ERR-08037", "BC-MIS-08019"]
  }
 ],
 "representations": null,
 "prerequisite_bridges": [
  {"prq_id": "BC-PRQ-06002", "text": "Rewrite radicals as powers before antidifferentiating."},
  {"prq_id": "BC-PRQ-08002", "text": "Integrating in y needs x as a function of y."},
  {"prq_id": "BC-PRQ-08004", "text": "A distance is larger minus smaller, not a bare function value."}
 ],
 "time": {"exam_part": "I-A", "budget_minutes": 2.14, "source": "research/exam/exam-structure.md#Section and part layout", "written_steps": {"ex-1": [3, 4]}, "skipped_steps": {"ex-1": [1, 2]}},
 "checks": [
  {
   "id": "chk-1",
   "check_kind": "completion",
   "format": "short_answer",
   "bands": ["low", "mid"],
   "archetype_id": "BC-QA-08012",
   "parameter_draw": {"form": "root", "scale": 1, "left": 0, "width": 4, "level": 1, "presentation": "formula", "axis": "x_axis"},
   "completes": "ex-1",
   "stem": {"text": "Evaluate pi times the integral of x from 0 to 4.", "command_verb": "evaluate"},
   "key": {"form": "symbolic", "expr": "8*pi"},
   "steps": [
    {"text": "The integral.", "expr": "Integral(pi*x, (x, 0, 4))", "relation": "new"},
    {"text": "pi x^2/2 from 0 to 4.", "expr": "8*pi", "relation": "equivalent"}
   ],
   "calculator_status": "no_calculator",
   "skills": ["BC-SKL-08043"]
  },
  {
   "id": "chk-2",
   "check_kind": "isomorph",
   "format": "short_answer",
   "bands": ["low", "mid"],
   "archetype_id": "BC-QA-08012",
   "parameter_draw": {"form": "linear", "scale": 3, "left": 0, "width": 2, "level": 1, "presentation": "formula", "axis": "x_axis"},
   "stem": {"text": "R is bounded by y = 3x, the x-axis and x = 2. Find the volume about the x-axis.", "command_verb": "find"},
   "key": {"form": "symbolic", "expr": "24*pi"},
   "steps": [
    {"text": "Disc area.", "expr": "pi*(3*x)**2", "relation": "new"},
    {"text": "Limits 0 and 2.", "expr": "Integral(pi*(3*x)**2, (x, 0, 2))", "relation": "new"},
    {"text": "Value.", "expr": "24*pi", "relation": "equivalent"}
   ],
   "calculator_status": "no_calculator",
   "skills": ["BC-SKL-08041"]
  },
  {
   "id": "chk-3",
   "check_kind": "mcq",
   "format": "mcq",
   "bands": ["low"],
   "archetype_id": "BC-QA-08012",
   "parameter_draw": {"form": "root", "scale": 2, "left": 1, "width": 3, "level": 2, "presentation": "formula", "axis": "x_axis"},
   "stem": {"text": "R is bounded by y = 2 sqrt(x), the x-axis, x = 1 and x = 4. The volume about the x-axis is", "command_verb": "identify"},
   "key": {"form": "symbolic", "expr": "30*pi"},
   "steps": [
    {"text": "Disc area 4 pi x.", "expr": "4*pi*x", "relation": "new"},
    {"text": "Limits 1 and 4.", "expr": "Integral(4*pi*x, (x, 1, 4))", "relation": "new"},
    {"text": "Value.", "expr": "30*pi", "relation": "equivalent"}
   ],
   "options": [
    {"id": "A", "is_key": false, "expr": "24*pi", "error_path": "BC-ERR-08024", "derivation": "the y values 2 and 4 used as the limits"},
    {"id": "B", "is_key": false, "expr": "28*pi/3", "error_path": "BC-ERR-08036", "derivation": "pi times 2 sqrt(x), unsquared"},
    {"id": "C", "is_key": true, "expr": "30*pi", "error_path": null},
    {"id": "D", "is_key": false, "expr": "30", "error_path": "BC-ERR-08037", "derivation": "pi dropped"}
   ],
   "calculator_status": "no_calculator",
   "skills": ["BC-SKL-08041"]
  }
 ],
 "delivery": [
  {"block": "orientation", "mode": "text", "reason": "rule 6: a statement of what a response shows", "sources": ["BC-CON-08017"]},
  {"block": "ki-1", "mode": "motion", "reason": "rule 2: a region revolved about its axis into a solid, a process; rule 4, BC-REP-08 on BC-SKL-08040, for the static fallback", "sources": ["BC-SKL-08040", "BC-SKL-08041"],
   "spec": {"kind": "solid_of_revolution", "representations": ["BC-REP-02", "BC-REP-08"],
    "curve": "y = sqrt(x)", "interval": [0, 4], "axis": "y = 0",
    "frames": [{"angle_degrees": 0}, {"angle_degrees": 90}, {"angle_degrees": 180}, {"angle_degrees": 270}, {"angle_degrees": 360}],
    "highlight": {"disc_at_x": 2, "radius": "sqrt(2)"},
    "labels": [{"text": "axis of revolution", "placement": "inside"}, {"text": "r = sqrt(x)", "placement": "inside"}, {"text": "disc area pi r^2", "placement": "inside"}]},
   "fallback": "three frames side by side (0, 180 and 360 degrees), static, the disc at x = 2 marked with its radius, labels inside",
   "keyboard": "Right arrow steps to the next frame, Left arrow to the previous; Space pauses auto-advance",
   "reduced_motion": "no auto-advance; each key press cross-fades to the next frame"},
  {"block": "ex-1", "mode": "step_reveal", "reason": "rule 1", "sources": []},
  {"block": "ex-2", "mode": "step_reveal", "reason": "rule 1", "sources": []},
  {"block": "err-BC-ERR-08023", "mode": "step_reveal", "reason": "rule 1", "sources": []},
  {"block": "err-BC-ERR-08024", "mode": "step_reveal", "reason": "rule 1", "sources": []},
  {"block": "err-BC-ERR-08036", "mode": "step_reveal", "reason": "rule 1", "sources": []},
  {"block": "err-BC-ERR-08037", "mode": "step_reveal", "reason": "rule 1", "sources": []}
 ],
 "refresher": ["ki-1", "err-BC-ERR-08023", "err-BC-ERR-08024", "err-BC-ERR-08036", "err-BC-ERR-08037", "ex-1"],
 "read_minutes": {"full": 5.1, "brief": 3.0},
 "word_count": {"full": 764, "brief": 446},
 "research_lines": [
  {"file": "research/units/unit-08-applications-integration.md", "line": "The factor pi multiplies the whole integral, and the radius is squared before integration rather than after."}
 ],
 "inferred": [
  {"claim": "BC-QA-08012 is calculator status either, so the lesson takes Section I Part A and its 2.14 minute budget.", "settles": "Timing data on disc items split by exam part."},
  {"claim": "ex-1's form point (BC-PT-99058) and answer point (BC-PT-99004) are earned but not tagged, because their reader lines would take the brief band past 450 words; ex-2 carries both tags.", "settles": "Shorter reader lines or a brief cap that admits them."},
  {"claim": "ki-1 is served as a motion of the region sweeping about the axis rather than a static figure.", "settles": "The modality A/B in the build plan: skip rate and time to first credited success by mode."},
  {"claim": "BC-ERR-99011 and BC-ERR-99019 meet the skills but fall past the cap of four error blocks.", "settles": "A cap change in plan 15 or a severity reorder in the bundle."},
  {"claim": "BC-ERR-08024 is shown as an x integral carrying the region's y values, the mirror of the record's wording, since BC-QA-08012's parameter_spec draws only regions sliced in x.", "settles": "A parameter_spec that draws a region revolved about the y-axis."}
 ],
 "sources": ["BC-CON-08017", "BC-SKL-08040", "BC-SKL-08041", "BC-SKL-08042", "BC-SKL-08043", "BC-EK-CHA-5C1", "ced:160", "BC-QA-08012", "BC-PT-99058", "BC-PT-99001", "BC-PT-99004", "BC-ERR-08023", "BC-ERR-08024", "BC-ERR-08036", "BC-ERR-08037", "BC-MIS-08012", "BC-MIS-08013", "BC-MIS-08019", "BC-MIS-08020", "BC-PRQ-06002", "BC-PRQ-08002", "BC-PRQ-08004", "research/units/unit-08-applications-integration.md#8.9 Volume with Disc Method: Revolving Around the x- or y-Axis", "research/question-analysis/question-archetypes.md#BC-QA-08012 Volume of a solid of revolution by the disc method", "research/scoring/common-point-losses.md#Setup points", "research/exam/exam-structure.md#Section and part layout"]
}
```
