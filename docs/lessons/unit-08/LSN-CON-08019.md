---
title: LSN-CON-08019 Washer method for a region held away from the axis
research_date: 2026-09-29
status: designed
purpose: Authoring spec for the concept lesson on BC-CON-08019, the washer method for a region between two curves revolved about a coordinate axis it does not meet, built from authoring_bundle("BC-CON-08019") and the research files it cites, so an author fills plan 15's lesson record without making a teaching decision.
---

# LSN-CON-08019 Washer method for a region held away from the axis

Concept BC-CON-08019 (skills BC-SKL-08048, BC-SKL-08049, BC-SKL-08050, BC-SKL-08051), topic 8.11 of Unit 8, loaded by one archetype, BC-QA-08013 (family revolution-volume). Hard parents BC-CON-08010, BC-CON-08012 and BC-CON-08017 (docs/lessons/unit-08/README.md, section 1).

## Prediction

Served first, both bands: an `mcq` on ex-1's own numbers with the core claim that a ring's area is pi times the outer radius squared minus the inner radius squared. The question is the cross-section area at x = 1, where the curves stand 2 and 1 above the axis. Key B, 3 pi. The distractors are pi (the squared difference of the radii) and 4 pi (the outer disc with no hole), the two slips the Traps block and the rival name. The ring's area is answerable from circle areas before any method is taught. The resolution states the squared radii and the subtraction, with no verdict. Source: BC-CON-08019 and the topic section the key idea cites.

## Orientation

Served text, from BC-CON-08019 `description_plain` and the topic's Assessment behaviour paragraph (research/units/unit-08-applications-integration.md#8.11 Volume with Washer Method: Revolving Around the x- or y-Axis): a region that does not touch the axis gives ring slices, and a response writes pi times the integral of the outer radius squared minus the inner radius squared, with limits. No count, no frequency.

## Key ideas

All four skills map to BC-EK-CHA-5C3 (ced:162): one core block, both bands.

- ki-1 (core). Paraphrase of the Washer method and Order of operations paragraphs: the region lies between two curves and misses the axis, so each slice is a ring; the curve farther from the axis gives R, the nearer gives r; each radius is squared before subtracting, since the square of a difference is not the difference of the squares. No anchor quote (brief band, Band plan).

## Recognition

BC-QA-08013 (research/question-analysis/question-archetypes.md#BC-QA-08013 Volume of a solid of revolution by the washer method): `typical_wording` "the region between the two curves is revolved about the stated line; find the volume of the solid generated"; `common_givens` two boundary curves, an axis of revolution the region does not meet; `asked_to_produce` an integrand with two squared radii, the volume. The signal: "revolved" with a gap between the region and the axis. Shapes: an MCQ offering the squared difference of the radii as a distractor; one part built on a region whose area was found earlier (official example BC-FRQ-2014-Q5-B).

The near miss of the contrast pair comes from the sibling archetype BC-QA-08012 (disc, LSN-CON-08017): a parabola resting on the x-axis, revolved about it, so the region meets the axis and one radius is enough.

What says "not this concept": the region touches the axis, a disc (BC-CON-08017); the axis is a line y = k other than the x-axis (BC-CON-08020).

## Method choice

- st-1, BC-QA-08013. Cue from `asked_to_produce` and `common_givens`. Method, `expected_solution_path[0]`: decide which curve is farther from the axis. Rival, `wrong_approaches`: squaring the difference of the two functions. Separating feature: two radii means two circles, so two squares. Both cue fields exist, so not inferred. The block also carries the contrast pair, a region off the axis beside a region on it, with the feature that separates them. No served field opens with the reader's own label, so the method reads as the step itself.

## Solution path

- ex-1, BC-QA-08013, both bands, no calculator. Draw: axis x_axis, left 0, width 2, bulge 1, slope 0, intercept 1, depth 1, presentation formula. g = 1, f = 1 + 2x - x^2, meeting at x = 0 and 2; revolved about the x-axis. No published item carries it.
- ex-2, low band: axis x_axis, left 1, width 1, bulge 2, slope 1, intercept 1, depth 2; g = x + 1, f = -2x^2 + 7x - 3.
- ex-2 is faded from step 3: steps 1 and 2 (which curve is outer, and the ring area) are shown, the student writes the answer, and steps 3 and 4 (the integral with the meeting points as limits and the value) then reveal. The fade falls there because the outer choice and the ring area repeat ex-1's pattern, and the limits and the expansion are what the student must produce.
- Steps: which curve is outer (no value), R and r (new), the washer area (new), the integral (new), the value (equivalent). A fluent solver writes the integral and the value; the outer choice is one clause.

## Scoring

BC-QA-08013 lists BC-PT-99058 and BC-PT-99001 and no answer point type. ex-1 tags BC-PT-99058 on the washer area only, and its BC-PT-99001 tag on the integral is dropped to fit the brief cap once the prediction and contrast pair are served (inferred array); ex-2 tags BC-PT-99058. The archetype's `scoring_pattern` names an answer point that no BC-PT on the record carries (library gap). Point loss: squared difference and missing constant are wrong volume families (research/scoring/common-point-losses.md#Setup points).

## Traps

Five errors meet the skills; the first four in bundle order are served: BC-ERR-08023, BC-ERR-08024, BC-ERR-08030, BC-ERR-08037. BC-ERR-08040 (radii exchanged) falls past the cap here and is served in LSN-CON-08020. On ex-1's draw. All four carry `fix_prompt` true, since each pair is distinct. The first two carry no possible reason line, for the brief cap (inferred array).

- err-BC-ERR-08023: the integrand in x with dy. Possible reason, BC-MIS-08013.
- err-BC-ERR-08024: the region's y values 1 and 2 used as limits. Possible reason, BC-MIS-08012.
- err-BC-ERR-08030: (f - 1)^2. Possible reason, BC-MIS-08017.
- err-BC-ERR-08037: pi dropped. Possible reason, BC-MIS-08019.

## Representations

None as a separate block. The Representations paragraph's region to a ring diagram (BC-REP-02 to BC-REP-08) is ki-1's figure.

## Prerequisite bridge

- BC-PRQ-06002, BC-PRQ-08002, BC-PRQ-08004, each from its `description_plain` and `failure_signature`.

## Time

BC-QA-08013 is `either`: Section I Part A, 2.14 minutes (research/exam/exam-structure.md#Section and part layout) [inferred]. As a free response part, 3 points on BC-FRQ-2014-Q5-B, 5.0 minutes (docs/lessons/unit-08/README.md, section 5). The minutes go on expanding R squared.

## Checks

- chk-1, completion of ex-1. Key 56pi/15.
- chk-2, isomorph: x_axis, left 0, width 2, bulge 1, slope 1, intercept 1, depth 1; g = x + 1, f = 1 + 3x - x^2. Key 32pi/5.
- chk-3, MCQ, low band: x_axis, left 0, width 2, bulge 1, slope 0, intercept 3, depth 1; g = 3, f = 3 + x(2 - x). Key 136pi/15. Distractors 16pi/15 (BC-ERR-08030), 136/15 (BC-ERR-08037), -22pi/15 (BC-ERR-08024, the y values 3 and 4 as limits).

## Delivery

- orientation: text. Rule 6.
- ki-1: figure. Rule 4, BC-REP-08 and BC-REP-02 on BC-SKL-08048; the sweep is taught in LSN-CON-08017 (docs/lessons/unit-08/README.md, section 6) [inferred; the modality A/B]. Figure presence: ki-1 is a drawn block, so the record carries no `no_figure_reason`.
- ex-1, ex-2, the four error blocks: step_reveal. Rule 1.

## Band plan

- Low (full): prediction, orientation, bridges, ki-1, st-1 with the contrast pair, ex-1 and its line, chk-1, the four error blocks, ex-2 (faded from step 3) and its line, chk-2, chk-3. 659 words, 4.4 minutes.
- Mid (brief): prediction, orientation, bridges, ki-1, st-1 with the contrast pair, ex-1 and its line, chk-1, err-BC-ERR-08023, err-BC-ERR-08024, chk-2. 447 words, 3.0 minutes.
- Refresher: ki-1, the four error blocks, ex-1.

## Sources

- BC-CON-08019; BC-SKL-08048, BC-SKL-08049, BC-SKL-08050, BC-SKL-08051; BC-EK-CHA-5C3; ced:162
- BC-QA-08013; BC-PT-99058, BC-PT-99001
- BC-ERR-08023, BC-ERR-08024, BC-ERR-08030, BC-ERR-08037, BC-ERR-08040; BC-MIS-08012, BC-MIS-08013, BC-MIS-08017, BC-MIS-08019
- BC-PRQ-06002, BC-PRQ-08002, BC-PRQ-08004
- research/units/unit-08-applications-integration.md#8.11 Volume with Washer Method: Revolving Around the x- or y-Axis
- research/question-analysis/question-archetypes.md#BC-QA-08013 Volume of a solid of revolution by the washer method
- research/scoring/common-point-losses.md#Setup points
- research/exam/exam-structure.md#Section and part layout
- [inferred] Part A for an either archetype; no answer point type; ex-1's limits point untagged and two possible reason lines dropped; BC-ERR-08040 past the cap; ki-1 as a figure. Each settled as the inferred array states.

## Machine record

```json
{
 "id": "LSN-CON-08019",
 "kind": "concept",
 "target_id": "BC-CON-08019",
 "unit": "08",
 "skills": ["BC-SKL-08048", "BC-SKL-08049", "BC-SKL-08050", "BC-SKL-08051"],
 "prediction": {
  "id": "pr-1",
  "stem": {"text": "R lies between \\(f(x)=1+2x-x^2\\) and \\(g(x)=1\\) and is revolved about the x-axis. Predict the cross-section area at \\(x=1\\).", "command_verb": "predict"},
  "format": "mcq",
  "options": [{"id": "A", "label": "\\(\\pi\\)", "is_key": false}, {"id": "B", "label": "\\(3\\pi\\)", "is_key": true}, {"id": "C", "label": "\\(4\\pi\\)", "is_key": false}],
  "resolution": "At \\(x=1\\) the slice is a ring with outer radius 2 and inner radius 1, so its area is \\(\\pi(2^2-1^2)=3\\pi\\). Each radius is squared, then subtracted.",
  "sources": ["BC-CON-08019", "research/units/unit-08-applications-integration.md#8.11 Volume with Washer Method: Revolving Around the x- or y-Axis"]
 },
 "orientation": {
  "text": "A region held off the axis gives ring slices. A response writes pi times the integral of outer radius squared minus inner radius squared, with limits.",
  "sources": ["BC-CON-08019", "research/units/unit-08-applications-integration.md#8.11 Volume with Washer Method: Revolving Around the x- or y-Axis"]
 },
 "key_ideas": [
  {
   "id": "ki-1",
   "ek_id": "BC-EK-CHA-5C3",
   "depth": "core",
   "text": "Each slice is a ring. The curve farther from the axis gives R, the nearer gives r. Square each radius, then subtract: the square of a difference is not the difference of squares.",
   "notation": "pi times the integral of outer squared minus inner squared",
   "quote": null,
   "sources": ["BC-EK-CHA-5C3", "ced:162", "research/units/unit-08-applications-integration.md#8.11 Volume with Washer Method: Revolving Around the x- or y-Axis"]
  }
 ],
 "strategy": [
  {
   "id": "st-1",
   "archetype_id": "BC-QA-08013",
   "cue": "Two curves, revolved about an axis the region misses.",
   "method": "Which curve is farther from the axis.",
   "rival": "Squaring the difference of the functions.",
   "separating_feature": "Two radii, two circles, two squares.",
   "sources": ["BC-QA-08013"],
   "evidence_tag": "verified",
   "contrast": {
    "this": {"text": "R lies between \\(f(x)=2+x-x^2\\) and \\(g(x)=2\\) and is revolved about the x-axis. Find the volume.", "archetype_id": "BC-QA-08013"},
    "not_this": {"text": "R is bounded by \\(y=2+x-x^2\\) and the x-axis, and is revolved about the x-axis. Find the volume.", "why_not": "The region meets the axis, so the slices are discs with one radius."},
    "feature": "A gap between region and axis gives two radii, contact gives one."
   }
  }
 ],
 "worked_examples": [
  {
   "id": "ex-1",
   "archetype_id": "BC-QA-08013",
   "bands": ["low", "mid"],
   "parameter_draw": {"left": 0, "width": 2, "bulge": 1, "slope": 0, "intercept": 1, "depth": 1, "presentation": "formula", "axis": "x_axis"},
   "problem": {"text": "R lies between f(x) = 1 + 2x - x^2 and g(x) = 1. Find the volume when R is revolved about the x-axis.", "command_verb": "find"},
   "calculator_status": "no_calculator",
   "steps": [
    {"cue": "R sits above y = 1.", "why": "f is farther: outer."},
    {"cue": "Distances to y = 0.", "why": "R = f, r = 1.", "expr": "(1 + 2*x - x**2)**2 - 1**2", "relation": "new"},
    {"cue": "Ring area.", "why": "Squares first, then subtract.", "expr": "pi*((1 + 2*x - x**2)**2 - 1)", "relation": "new", "point_type_id": "BC-PT-99058"},
    {"cue": "Curves meet at 0 and 2.", "why": "Limits.", "expr": "Integral(pi*((1 + 2*x - x**2)**2 - 1), (x, 0, 2))", "relation": "new"},
    {"cue": "Expand, integrate.", "why": "Keep pi.", "expr": "56*pi/15", "relation": "equivalent"}
   ],
   "answer": {"form": "symbolic", "expr": "56*pi/15"}
  },
  {
   "id": "ex-2",
   "archetype_id": "BC-QA-08013",
   "bands": ["low"],
   "parameter_draw": {"left": 1, "width": 1, "bulge": 2, "slope": 1, "intercept": 1, "depth": 2, "presentation": "formula", "axis": "x_axis"},
   "problem": {"text": "R lies between f(x) = -2x^2 + 7x - 3 and g(x) = x + 1. Find the volume about the x-axis.", "command_verb": "find"},
   "calculator_status": "no_calculator",
   "steps": [
    {"cue": "f is above g, both above the axis.", "why": "f outer."},
    {"cue": "Ring area.", "why": "Squares first.", "expr": "pi*((-2*x**2 + 7*x - 3)**2 - (x + 1)**2)", "relation": "new", "point_type_id": "BC-PT-99058"},
    {"cue": "Curves meet at 1 and 2.", "why": "Limits.", "expr": "Integral(pi*((-2*x**2 + 7*x - 3)**2 - (x + 1)**2), (x, 1, 2))", "relation": "new"},
    {"cue": "Integrate.", "why": "Keep pi.", "expr": "9*pi/5", "relation": "equivalent"}
   ],
   "answer": {"form": "symbolic", "expr": "9*pi/5"},
   "fade_from": 3
  }
 ],
 "what_a_reader_scores": [
  {
   "example_id": "ex-1",
   "point_type_ids": ["BC-PT-99058"],
   "lines": [
    {
     "point_type_id": "BC-PT-99058",
     "text": "Volume integrand form. Earned by: An integrand of the correct volume form, a nonzero constant times the square of the function for a disc, or the stated cross-section area (sg-26:19, sg-22:18). Not earned by: A constant other than pi where pi is required, which sg-22:19 states blocks the answer point; a rotation about the wrong axis, which sg-26:19 lets earn the form point only."
    }
   ]
  },
  {
   "example_id": "ex-2",
   "point_type_ids": ["BC-PT-99058"],
   "lines": [
    {
     "point_type_id": "BC-PT-99058",
     "text": "Volume integrand form. Earned by: An integrand of the correct volume form, a nonzero constant times the square of the function for a disc, or the stated cross-section area (sg-26:19, sg-22:18). Not earned by: A constant other than pi where pi is required, which sg-22:19 states blocks the answer point; a rotation about the wrong axis, which sg-26:19 lets earn the form point only."
    }
   ]
  }
 ],
 "common_errors": [
  {
   "error_id": "BC-ERR-08023",
   "observed_behavior": "A function of x is integrated with respect to y, or the reverse, without being rewritten.",
   "scoring_consequence": "The setup point is lost because the expression does not define a number.",
   "wrong_step": {"text": "dy.", "expr": "Integral(pi*((1 + 2*x - x**2)**2 - 1), (y, 0, 2))"},
   "right_step": {"text": "dx.", "expr": "Integral(pi*((1 + 2*x - x**2)**2 - 1), (x, 0, 2))"},
   "relation": "distinct",
   "possible_reason": null,
   "sources": ["BC-ERR-08023", "BC-MIS-08013"],
   "fix_prompt": true
  },
  {
   "error_id": "BC-ERR-08024",
   "observed_behavior": "An integral in y carries x values as its limits.",
   "scoring_consequence": "The setup point is lost and the value is wrong.",
   "wrong_step": {"text": "y from 1 to 2.", "expr": "Integral(pi*((1 + 2*x - x**2)**2 - 1), (x, 1, 2))"},
   "right_step": {"text": "x from 0 to 2.", "expr": "Integral(pi*((1 + 2*x - x**2)**2 - 1), (x, 0, 2))"},
   "relation": "distinct",
   "possible_reason": null,
   "sources": ["BC-ERR-08024", "BC-MIS-08012"],
   "fix_prompt": true
  },
  {
   "error_id": "BC-ERR-08030",
   "observed_behavior": "A washer integrand is written as the square of the difference of the two radii, or a squared difference is expanded term by term.",
   "scoring_consequence": "The setup point is lost, and the value is wrong by the cross term.",
   "wrong_step": {"text": "(R - r)^2.", "expr": "Integral(pi*(2*x - x**2)**2, (x, 0, 2))"},
   "right_step": {"text": "R^2 - r^2.", "expr": "Integral(pi*((1 + 2*x - x**2)**2 - 1), (x, 0, 2))"},
   "relation": "distinct",
   "possible_reason": {"misconception_id": "BC-MIS-08017", "text": "treats squaring as distributing over subtraction"},
   "sources": ["BC-ERR-08030", "BC-MIS-08017"],
   "fix_prompt": true
  },
  {
   "error_id": "BC-ERR-08037",
   "observed_behavior": "A disc or washer volume is reported without the constant factor pi.",
   "scoring_consequence": "The answer point is lost.",
   "wrong_step": {"text": "No pi.", "expr": "56/15"},
   "right_step": {"text": "pi.", "expr": "56*pi/15"},
   "relation": "distinct",
   "possible_reason": {"misconception_id": "BC-MIS-08019", "text": "remembers the squared dimension but not the fraction in front of it"},
   "sources": ["BC-ERR-08037", "BC-MIS-08019"],
   "fix_prompt": true
  }
 ],
 "representations": null,
 "prerequisite_bridges": [{"prq_id": "BC-PRQ-06002", "text": "Radicals become powers before antidifferentiating."}, {"prq_id": "BC-PRQ-08002", "text": "Integrating in y needs x in terms of y."}, {"prq_id": "BC-PRQ-08004", "text": "A distance is larger minus smaller."}],
 "time": {"exam_part": "I-A", "budget_minutes": 2.14, "source": "research/exam/exam-structure.md#Section and part layout", "written_steps": {"ex-1": [4, 5]}, "skipped_steps": {"ex-1": [1, 2, 3]}},
 "checks": [
  {
   "id": "chk-1",
   "check_kind": "completion",
   "format": "short_answer",
   "bands": ["low", "mid"],
   "archetype_id": "BC-QA-08013",
   "parameter_draw": {"left": 0, "width": 2, "bulge": 1, "slope": 0, "intercept": 1, "depth": 1, "presentation": "formula", "axis": "x_axis"},
   "completes": "ex-1",
   "stem": {"text": "Evaluate pi times the integral of (1 + 2x - x^2)^2 - 1 from 0 to 2.", "command_verb": "evaluate"},
   "key": {"form": "symbolic", "expr": "56*pi/15"},
   "steps": [
    {"text": "The integral.", "expr": "Integral(pi*((1 + 2*x - x**2)**2 - 1), (x, 0, 2))", "relation": "new"},
    {"text": "Expanded.", "expr": "Integral(pi*(x**4 - 4*x**3 + 2*x**2 + 4*x), (x, 0, 2))", "relation": "equivalent"},
    {"text": "Value.", "expr": "56*pi/15", "relation": "equivalent"}
   ],
   "calculator_status": "no_calculator",
   "skills": ["BC-SKL-08049"]
  },
  {
   "id": "chk-2",
   "check_kind": "isomorph",
   "format": "short_answer",
   "bands": ["low", "mid"],
   "archetype_id": "BC-QA-08013",
   "parameter_draw": {"left": 0, "width": 2, "bulge": 1, "slope": 1, "intercept": 1, "depth": 1, "presentation": "formula", "axis": "x_axis"},
   "stem": {"text": "R lies between f(x) = 1 + 3x - x^2 and g(x) = x + 1. Find the volume about the x-axis.", "command_verb": "find"},
   "key": {"form": "symbolic", "expr": "32*pi/5"},
   "steps": [
    {"text": "f outer.", "expr": "pi*((1 + 3*x - x**2)**2 - (x + 1)**2)", "relation": "new"},
    {"text": "Limits 0 and 2.", "expr": "Integral(pi*((1 + 3*x - x**2)**2 - (x + 1)**2), (x, 0, 2))", "relation": "new"},
    {"text": "Value.", "expr": "32*pi/5", "relation": "equivalent"}
   ],
   "calculator_status": "no_calculator",
   "skills": ["BC-SKL-08049"]
  },
  {
   "id": "chk-3",
   "check_kind": "mcq",
   "format": "mcq",
   "bands": ["low"],
   "archetype_id": "BC-QA-08013",
   "parameter_draw": {"left": 0, "width": 2, "bulge": 1, "slope": 0, "intercept": 3, "depth": 1, "presentation": "formula", "axis": "x_axis"},
   "stem": {"text": "R lies between f(x) = 3 + x(2 - x) and g(x) = 3. The volume about the x-axis is", "command_verb": "identify"},
   "key": {"form": "symbolic", "expr": "136*pi/15"},
   "steps": [
    {"text": "R = f, r = 3.", "expr": "pi*((3 + x*(2 - x))**2 - 9)", "relation": "new"},
    {"text": "Limits 0 and 2.", "expr": "Integral(pi*((3 + x*(2 - x))**2 - 9), (x, 0, 2))", "relation": "new"},
    {"text": "Value.", "expr": "136*pi/15", "relation": "equivalent"}
   ],
   "options": [
    {"id": "A", "is_key": false, "expr": "16*pi/15", "error_path": "BC-ERR-08030", "derivation": "pi times (f - 3) squared"},
    {"id": "B", "is_key": true, "expr": "136*pi/15", "error_path": null},
    {"id": "C", "is_key": false, "expr": "136/15", "error_path": "BC-ERR-08037", "derivation": "pi dropped"},
    {"id": "D", "is_key": false, "expr": "-22*pi/15", "error_path": "BC-ERR-08024", "derivation": "the y values 3 and 4 used as limits"}
   ],
   "calculator_status": "no_calculator",
   "skills": ["BC-SKL-08051"]
  }
 ],
 "delivery": [
  {"block": "orientation", "mode": "text", "reason": "rule 6: a statement of what a response shows", "sources": ["BC-CON-08019"]},
  {
   "block": "ki-1",
   "mode": "figure",
   "reason": "rule 4: BC-REP-08 and BC-REP-02 on BC-SKL-08048; the sweep itself is taught in LSN-CON-08017",
   "sources": ["BC-SKL-08048"],
   "spec": {
    "kind": "washer",
    "representations": ["BC-REP-02", "BC-REP-08"],
    "region": {"upper": "y = 1 + 2x - x^2", "lower": "y = 1", "interval": [0, 2]},
    "axis": "y = 0",
    "slice_at_x": 1,
    "drawn": ["the region above y = 1", "one ring at x = 1, outer circle through the upper curve, inner circle through y = 1"],
    "labels": [{"text": "R = f(x), farther", "placement": "inside"}, {"text": "r = 1, nearer", "placement": "inside"}, {"text": "area pi (R^2 - r^2)", "placement": "inside"}]
   },
   "fallback": "the same figure as a static image with its three labels",
   "keyboard": "none needed: the figure has no control"
  },
  {"block": "ex-1", "mode": "step_reveal", "reason": "rule 1", "sources": []},
  {"block": "ex-2", "mode": "step_reveal", "reason": "rule 1", "sources": []},
  {"block": "err-BC-ERR-08023", "mode": "step_reveal", "reason": "rule 1", "sources": []},
  {"block": "err-BC-ERR-08024", "mode": "step_reveal", "reason": "rule 1", "sources": []},
  {"block": "err-BC-ERR-08030", "mode": "step_reveal", "reason": "rule 1", "sources": []},
  {"block": "err-BC-ERR-08037", "mode": "step_reveal", "reason": "rule 1", "sources": []}
 ],
 "refresher": ["ki-1", "err-BC-ERR-08023", "err-BC-ERR-08024", "err-BC-ERR-08030", "err-BC-ERR-08037", "ex-1"],
 "read_minutes": {"full": 4.4, "brief": 3.0},
 "word_count": {"full": 659, "brief": 447},
 "research_lines": [{"file": "research/units/unit-08-applications-integration.md", "line": "The two radii are squared before they are subtracted."}],
 "inferred": [
  {"claim": "BC-QA-08013 is calculator status either, so the lesson takes Section I Part A and its 2.14 minute budget.", "settles": "Timing data on washer items split by exam part."},
  {"claim": "The answer point the scoring_pattern names is not tagged: BC-QA-08013 lists no answer point type.", "settles": "BC-PT-99004 added to BC-QA-08013's point_types."},
  {"claim": "BC-ERR-08040 meets the skills but falls fifth, past the cap of four error blocks.", "settles": "A cap change in plan 15 or a severity reorder in the bundle."},
  {"claim": "ki-1 is served as a static figure of one washer.", "settles": "The modality A/B in the build plan: skip rate and time to first credited success by mode."},
  {
   "claim": "BC-ERR-08024 is shown as an x integral carrying the region's y values, the mirror of the record's wording, since BC-QA-08013's parameter_spec draws only regions sliced in x.",
   "settles": "A parameter_spec that draws a region revolved about the y-axis."
  },
  {
   "claim": "ex-1's limits point (BC-PT-99001) is earned but not tagged, and the possible_reason lines of the first two error blocks are dropped, because the prediction and contrast pair take the words they need in the brief band.",
   "settles": "A brief cap that admits the reader line and the reasons, or a shorter prediction and contrast."
  }
 ],
 "sources": [
  "BC-CON-08019",
  "BC-SKL-08048",
  "BC-SKL-08049",
  "BC-SKL-08050",
  "BC-SKL-08051",
  "BC-EK-CHA-5C3",
  "ced:162",
  "BC-QA-08013",
  "BC-PT-99058",
  "BC-PT-99001",
  "BC-ERR-08023",
  "BC-ERR-08024",
  "BC-ERR-08030",
  "BC-ERR-08037",
  "BC-ERR-08040",
  "BC-MIS-08012",
  "BC-MIS-08013",
  "BC-MIS-08017",
  "BC-MIS-08019",
  "BC-PRQ-06002",
  "BC-PRQ-08002",
  "BC-PRQ-08004",
  "research/units/unit-08-applications-integration.md#8.11 Volume with Washer Method: Revolving Around the x- or y-Axis",
  "research/question-analysis/question-archetypes.md#BC-QA-08013 Volume of a solid of revolution by the washer method",
  "research/scoring/common-point-losses.md#Setup points",
  "research/exam/exam-structure.md#Section and part layout"
 ]
}
```
