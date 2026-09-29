---
title: LSN-CON-08020 Washer radii measured from a line other than an axis
research_date: 2026-09-29
status: designed
purpose: Authoring spec for the concept lesson on BC-CON-08020, both washer radii written as distances from a horizontal line other than the x-axis, with the outer radius taken from the farther curve, built from authoring_bundle("BC-CON-08020") and the research files it cites, so an author fills plan 15's lesson record without making a teaching decision.
---

# LSN-CON-08020 Washer radii measured from a line other than an axis

Concept BC-CON-08020 (skills BC-SKL-08052, BC-SKL-08053, BC-SKL-08054, BC-SKL-08055), topic 8.12 of Unit 8, loaded by BC-QA-08013 (family revolution-volume) with its axis parameter set to below or above. Hard parents BC-CON-08018 and BC-CON-08019 (docs/lessons/unit-08/README.md, section 1): the shifted radius and the washer are both assumed.

## Prediction

Served first, both bands: an `mcq` on ex-1's own numbers with the core claim that the outer radius belongs to the curve farther from the axis. The question is which of f and g is farther from y = 3 at x = 1, where f is 2 and g is 1. Key B, the lower curve g, which is 2 below the line against 1 for f. The distractors are the higher curve (the position reading BC-MIS-08023 describes) and an even split. A distance to a horizontal line is answerable before any method is taught. The resolution states which curve is farther and that it gives the outer radius, with no verdict. Source: BC-CON-08020 and the topic section the key idea cites.

## Orientation

Served text, from BC-CON-08020 `description_plain` and the topic's Assessment behaviour paragraph (research/units/unit-08-applications-integration.md#8.12 Volume with Washer Method: Revolving Around Other Axes): both radii become distances from the line, and a response decides which curve is farther from that line before writing pi times the integral of R squared minus r squared. No count, no frequency.

## Key ideas

All four skills map to BC-EK-CHA-5C4 (ced:163): one core block, both bands.

- ki-1 (core). Paraphrase of the Which radius is outer and Notation paragraphs: the outer radius belongs to the curve farther from the axis; with the axis above the region the lower curve is farther, so the roles exchange; each shifted radius is a parenthesised difference, squared whole. No anchor quote (brief band, Band plan).

## Recognition

BC-QA-08013 (research/question-analysis/question-archetypes.md#BC-QA-08013 Volume of a solid of revolution by the washer method): `common_givens` two boundary curves, an axis of revolution the region does not meet; `asked_to_produce` an integrand with two squared radii, the volume; `difficulty_variables` "whether the axis lies above or below the region, which can exchange the radii". The signal: "revolved about the line y = k" with k outside the region's range. The MCQ holds the region and moves the axis so the curves exchange roles (research/units/unit-08-applications-integration.md#8.12 Volume with Washer Method: Revolving Around Other Axes).

The near miss of the contrast pair comes from the sibling archetype BC-QA-08012 (disc about a shifted line, LSN-CON-08018): the same curves with the line moved onto the lower curve, so the line bounds the region and one shifted radius is enough.

What says "not this concept": the x-axis itself (BC-CON-08019); the line bounds the region (BC-CON-08018).

## Method choice

- st-1, BC-QA-08013. Cue from `common_givens` and `difficulty_variables`. Method, `expected_solution_path[0]`: decide which curve is farther from the axis. Rival, `common_distractors`: the radii assigned by which curve is higher rather than which is farther; and `wrong_approaches`, a negative volume from swapped radii. Separating feature: where the line sits relative to the region. Both cue fields exist, so not inferred. The block also carries the contrast pair, a line clear of the region beside a line that bounds it, with the feature that separates them. No served field opens with the reader's own label, so the method reads as the step itself; the rival is shortened to the higher curve taken as outer for the brief cap, and the negative volume it gives is the error block's.

## Solution path

- ex-1, BC-QA-08013, both bands, no calculator. Draw: axis above, left 0, width 2, bulge 1, slope 0, intercept 1, depth 1, presentation formula; the derived level is 1 + 0 + 1 + 1 = 3. g = 1, f = 1 + 2x - x^2, revolved about y = 3. No published item carries it.
- ex-2, low band: axis below, left 1, width 2, bulge 1, slope 0, intercept 2, depth 1; g = 2, f = -x^2 + 4x - 1, about y = -1.
- ex-2 is faded from step 3: steps 1 and 2 (which curve is farther, and the ring area with R = f + 1 and r = 3) are shown, the student writes the answer, and steps 3 and 4 (the integral with the meeting points as limits and the value) then reveal. The fade falls there because the axis-below reading and the ring area are the new content and repeat ex-1's pattern, and the limits and the integration are what the student must produce.
- Steps: which curve is farther (no value), R (new), r (new), the washer area (new), the integral (new), the value (equivalent). A fluent solver writes the two radii and the integral; the farther curve is one clause.

## Scoring

BC-QA-08013 lists BC-PT-99058 and BC-PT-99001. ex-1 tags BC-PT-99058 on the washer area only, and its BC-PT-99001 tag on the integral is dropped to fit the brief cap once the prediction and contrast pair are served (inferred array); ex-2 tags BC-PT-99058. No answer point type is listed although the `scoring_pattern` names one (library gap). Parentheses on each difference (research/scoring/notation-requirements.md#Parentheses).

## Traps

Four errors meet the skills, in bundle order: BC-ERR-08023, BC-ERR-08030, BC-ERR-08038, BC-ERR-08040. Low band all four, mid band the first two. On ex-1's draw. All four carry `fix_prompt` true, since each pair is distinct. The first two carry no possible reason line, for the brief cap (inferred array).

- err-BC-ERR-08023: the integrand in x with dy. Possible reason, BC-MIS-08013.
- err-BC-ERR-08030: (R - r)^2. Possible reason, BC-MIS-08017.
- err-BC-ERR-08038: f and g as the radii. Possible reason, BC-MIS-08021.
- err-BC-ERR-08040: the higher curve taken as outer. Possible reason, BC-MIS-08023.

## Representations

None as a separate block. The Representations paragraph's axis drawn above or beside the region to a pair of radii (BC-REP-02 to BC-REP-01) is ki-1's interactive.

## Prerequisite bridge

- BC-PRQ-08002, BC-PRQ-08004, each from its `description_plain` and `failure_signature`.

## Time

BC-QA-08013 is `either`: Section I Part A, 2.14 minutes (research/exam/exam-structure.md#Section and part layout) [inferred]. As a free response part, 3 points on BC-FRQ-2014-Q5-B, 5.0 minutes (docs/lessons/unit-08/README.md, section 5). The minutes go on expanding the squared inner radius.

## Checks

- chk-1, completion of ex-1. Key 64pi/15.
- chk-2, isomorph: axis above, left 1, width 1, bulge 2, slope 1, intercept 1, depth 1; level 4; g = x + 1, f = -2x^2 + 7x - 3. Key 13pi/15.
- chk-3, MCQ, low band: axis above, left 0, width 1, bulge 1, slope 0, intercept 2, depth 2; level 4; g = 2, f = 2 + x(1 - x). Key 19pi/30. Distractors pi/30 (BC-ERR-08030), 7pi/10 (BC-ERR-08038), -19pi/30 (BC-ERR-08040).

## Delivery

- orientation: text. Rule 6.
- ki-1: interactive. Rule 4 promoted: BC-REP-08 and BC-REP-02 on BC-SKL-08054, and BC-QA-08013 `difficulty_variables` name the axis position as the quantity that exchanges the radii (docs/lessons/unit-08/README.md, section 6) [inferred; the modality A/B]. Figure presence: ki-1 is a drawn block, so the record carries no `no_figure_reason`.
- ex-1, ex-2, the four error blocks: step_reveal. Rule 1.

## Band plan

- Low (full): prediction, orientation, bridges, ki-1, st-1 with the contrast pair, ex-1 and its line, chk-1, the four error blocks, ex-2 (faded from step 3) and its line, chk-2, chk-3. 691 words, 4.7 minutes.
- Mid (brief): prediction, orientation, bridges, ki-1, st-1 with the contrast pair, ex-1 and its line, chk-1, err-BC-ERR-08023, err-BC-ERR-08030, chk-2. 449 words, 3.0 minutes.
- Refresher: ki-1, the four error blocks, ex-1.

## Sources

- BC-CON-08020; BC-SKL-08052, BC-SKL-08053, BC-SKL-08054, BC-SKL-08055; BC-EK-CHA-5C4; ced:163
- BC-QA-08013; BC-PT-99058, BC-PT-99001
- BC-ERR-08023, BC-ERR-08030, BC-ERR-08038, BC-ERR-08040; BC-MIS-08013, BC-MIS-08017, BC-MIS-08021, BC-MIS-08023
- BC-PRQ-08002, BC-PRQ-08004
- research/units/unit-08-applications-integration.md#8.12 Volume with Washer Method: Revolving Around Other Axes
- research/question-analysis/question-archetypes.md#BC-QA-08013 Volume of a solid of revolution by the washer method
- research/scoring/notation-requirements.md#Parentheses
- research/exam/exam-structure.md#Section and part layout
- [inferred] Part A for an either archetype; no answer point type; ex-1's limits point untagged and two possible reason lines dropped; ki-1 as an interactive. Each settled as the inferred array states.

## Machine record

```json
{
 "id": "LSN-CON-08020",
 "kind": "concept",
 "target_id": "BC-CON-08020",
 "unit": "08",
 "skills": ["BC-SKL-08052", "BC-SKL-08053", "BC-SKL-08054", "BC-SKL-08055"],
 "prediction": {
  "id": "pr-1",
  "stem": {"text": "R lies between \\(f(x)=1+2x-x^2\\) and \\(g(x)=1\\) and is revolved about \\(y=3\\). Predict which curve is farther from the line at \\(x=1\\).", "command_verb": "predict"},
  "format": "mcq",
  "options": [{"id": "A", "label": "\\(f\\), the higher curve", "is_key": false}, {"id": "B", "label": "\\(g\\), the lower curve", "is_key": true}, {"id": "C", "label": "Both are equally far", "is_key": false}],
  "resolution": "The line lies above R, so the lower curve \\(g\\) is farther, and the farther curve gives the outer radius.",
  "sources": ["BC-CON-08020", "research/units/unit-08-applications-integration.md#8.12 Volume with Washer Method: Revolving Around Other Axes"]
 },
 "orientation": {
  "text": "About y = k, both radii are distances from k. A response names the farther curve as outer, then integrates pi (R^2 - r^2).",
  "sources": ["BC-CON-08020", "research/units/unit-08-applications-integration.md#8.12 Volume with Washer Method: Revolving Around Other Axes"]
 },
 "key_ideas": [
  {
   "id": "ki-1",
   "ek_id": "BC-EK-CHA-5C4",
   "depth": "core",
   "text": "Outer radius: the curve farther from the axis. With the axis above the region, the lower curve is farther. Each radius is a parenthesised difference.",
   "notation": "outer and inner radii as shifted differences",
   "quote": null,
   "sources": ["BC-EK-CHA-5C4", "ced:163", "research/units/unit-08-applications-integration.md#8.12 Volume with Washer Method: Revolving Around Other Axes"]
  }
 ],
 "strategy": [
  {
   "id": "st-1",
   "archetype_id": "BC-QA-08013",
   "cue": "Two curves revolved about y = k, outside the region.",
   "method": "Which curve is farther from y = k.",
   "rival": "Higher curve as outer.",
   "separating_feature": "Whether the line sits above or below the region.",
   "sources": ["BC-QA-08013"],
   "evidence_tag": "verified",
   "contrast": {
    "this": {"text": "R lies between \\(f(x)=2+x-x^2\\) and \\(g(x)=2\\) and is revolved about \\(y=4\\). Find the volume.", "archetype_id": "BC-QA-08013"},
    "not_this": {"text": "R lies between \\(y=2+x-x^2\\) and \\(y=2\\) and is revolved about \\(y=2\\). Find the volume.", "why_not": "The line bounds the region, so the slices are discs with one shifted radius."},
    "feature": "A line clear of the region gives two radii measured from it."
   }
  }
 ],
 "worked_examples": [
  {
   "id": "ex-1",
   "archetype_id": "BC-QA-08013",
   "bands": ["low", "mid"],
   "parameter_draw": {"left": 0, "width": 2, "bulge": 1, "slope": 0, "intercept": 1, "depth": 1, "presentation": "formula", "axis": "above"},
   "problem": {"text": "R lies between f(x) = 1 + 2x - x^2 and g(x) = 1. Find the volume about y = 3.", "command_verb": "find"},
   "calculator_status": "no_calculator",
   "steps": [
    {"cue": "y = 3 lies above R.", "why": "g is lower, so farther: outer."},
    {"cue": "Outer: line minus g.", "why": "Distance down to g.", "expr": "3 - 1", "relation": "new"},
    {"cue": "Inner: line minus f.", "why": "Parenthesise.", "expr": "3 - (1 + 2*x - x**2)", "relation": "new"},
    {"cue": "Ring area.", "why": "Squares, then subtract.", "expr": "pi*(2**2 - (x**2 - 2*x + 2)**2)", "relation": "new", "point_type_id": "BC-PT-99058"},
    {"cue": "Curves meet at 0 and 2.", "why": "Limits unmoved.", "expr": "Integral(pi*(4 - (x**2 - 2*x + 2)**2), (x, 0, 2))", "relation": "new"},
    {"cue": "Integrate.", "why": "Positive.", "expr": "64*pi/15", "relation": "equivalent"}
   ],
   "answer": {"form": "symbolic", "expr": "64*pi/15"}
  },
  {
   "id": "ex-2",
   "archetype_id": "BC-QA-08013",
   "bands": ["low"],
   "parameter_draw": {"left": 1, "width": 2, "bulge": 1, "slope": 0, "intercept": 2, "depth": 1, "presentation": "formula", "axis": "below"},
   "problem": {"text": "R lies between f(x) = -x^2 + 4x - 1 and g(x) = 2. Find the volume about y = -1.", "command_verb": "find"},
   "calculator_status": "no_calculator",
   "steps": [
    {"cue": "y = -1 lies below R.", "why": "f is farther: outer."},
    {"cue": "Ring area.", "why": "R = f + 1, r = 3.", "expr": "pi*((-x**2 + 4*x - 1 + 1)**2 - 3**2)", "relation": "new", "point_type_id": "BC-PT-99058"},
    {"cue": "Curves meet at 1 and 3.", "why": "Limits.", "expr": "Integral(pi*((4*x - x**2)**2 - 9), (x, 1, 3))", "relation": "new"},
    {"cue": "Integrate.", "why": "Keep pi.", "expr": "136*pi/15", "relation": "equivalent"}
   ],
   "answer": {"form": "symbolic", "expr": "136*pi/15"},
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
   "wrong_step": {"text": "dy.", "expr": "Integral(pi*(4 - (x**2 - 2*x + 2)**2), (y, 0, 2))"},
   "right_step": {"text": "dx.", "expr": "Integral(pi*(4 - (x**2 - 2*x + 2)**2), (x, 0, 2))"},
   "relation": "distinct",
   "possible_reason": null,
   "sources": ["BC-ERR-08023", "BC-MIS-08013"],
   "fix_prompt": true
  },
  {
   "error_id": "BC-ERR-08030",
   "observed_behavior": "A washer integrand is written as the square of the difference of the two radii, or a squared difference is expanded term by term.",
   "scoring_consequence": "The setup point is lost, and the value is wrong by the cross term.",
   "wrong_step": {"text": "(R - r)^2.", "expr": "Integral(pi*(2 - (x**2 - 2*x + 2))**2, (x, 0, 2))"},
   "right_step": {"text": "R^2 - r^2.", "expr": "Integral(pi*(4 - (x**2 - 2*x + 2)**2), (x, 0, 2))"},
   "relation": "distinct",
   "possible_reason": null,
   "sources": ["BC-ERR-08030", "BC-MIS-08017"],
   "fix_prompt": true
  },
  {
   "error_id": "BC-ERR-08038",
   "observed_behavior": "The response revolves about a line other than an axis but writes the radius as the bare function value.",
   "scoring_consequence": "The setup point is lost.",
   "wrong_step": {"text": "R = f, r = g.", "expr": "Integral(pi*((1 + 2*x - x**2)**2 - 1), (x, 0, 2))"},
   "right_step": {"text": "R = 3 - g, r = 3 - f.", "expr": "Integral(pi*(4 - (x**2 - 2*x + 2)**2), (x, 0, 2))"},
   "relation": "distinct",
   "possible_reason": {"misconception_id": "BC-MIS-08021", "text": "treats the disc and washer formulas as fixed in the function rather than as built from a distance to the axis"},
   "sources": ["BC-ERR-08038", "BC-MIS-08021"],
   "fix_prompt": true
  },
  {
   "error_id": "BC-ERR-08040",
   "observed_behavior": "The nearer curve is used as the outer radius, giving a negative integrand.",
   "scoring_consequence": "A negative volume is reported and the answer point is lost.",
   "wrong_step": {"text": "Higher curve outer.", "expr": "Integral(pi*((x**2 - 2*x + 2)**2 - 4), (x, 0, 2))"},
   "right_step": {"text": "Farther curve outer.", "expr": "Integral(pi*(4 - (x**2 - 2*x + 2)**2), (x, 0, 2))"},
   "relation": "distinct",
   "possible_reason": {"misconception_id": "BC-MIS-08023", "text": "assigns the radii by position in the plane rather than by distance from the axis"},
   "sources": ["BC-ERR-08040", "BC-MIS-08023"],
   "fix_prompt": true
  }
 ],
 "representations": null,
 "prerequisite_bridges": [{"prq_id": "BC-PRQ-08002", "text": "Integrating in y needs x in terms of y."}, {"prq_id": "BC-PRQ-08004", "text": "A distance is larger minus smaller."}],
 "time": {"exam_part": "I-A", "budget_minutes": 2.14, "source": "research/exam/exam-structure.md#Section and part layout", "written_steps": {"ex-1": [2, 3, 5, 6]}, "skipped_steps": {"ex-1": [1, 4]}},
 "checks": [
  {
   "id": "chk-1",
   "check_kind": "completion",
   "format": "short_answer",
   "bands": ["low", "mid"],
   "archetype_id": "BC-QA-08013",
   "parameter_draw": {"left": 0, "width": 2, "bulge": 1, "slope": 0, "intercept": 1, "depth": 1, "presentation": "formula", "axis": "above"},
   "completes": "ex-1",
   "stem": {"text": "Evaluate pi times the integral of 4 - (x^2 - 2x + 2)^2 from 0 to 2.", "command_verb": "evaluate"},
   "key": {"form": "symbolic", "expr": "64*pi/15"},
   "steps": [
    {"text": "The integral.", "expr": "Integral(pi*(4 - (x**2 - 2*x + 2)**2), (x, 0, 2))", "relation": "new"},
    {"text": "u = x - 1.", "expr": "Integral(pi*(4 - (x**2 + 1)**2), (x, -1, 1))", "relation": "equivalent"},
    {"text": "Value.", "expr": "64*pi/15", "relation": "equivalent"}
   ],
   "calculator_status": "no_calculator",
   "skills": ["BC-SKL-08055"]
  },
  {
   "id": "chk-2",
   "check_kind": "isomorph",
   "format": "short_answer",
   "bands": ["low", "mid"],
   "archetype_id": "BC-QA-08013",
   "parameter_draw": {"left": 1, "width": 1, "bulge": 2, "slope": 1, "intercept": 1, "depth": 1, "presentation": "formula", "axis": "above"},
   "stem": {"text": "R lies between f(x) = -2x^2 + 7x - 3 and g(x) = x + 1. Find the volume about y = 4.", "command_verb": "find"},
   "key": {"form": "symbolic", "expr": "13*pi/15"},
   "steps": [
    {"text": "g farther: R = 3 - x, r = 2x^2 - 7x + 7.", "expr": "pi*((3 - x)**2 - (2*x**2 - 7*x + 7)**2)", "relation": "new"},
    {"text": "Limits 1 and 2.", "expr": "Integral(pi*((3 - x)**2 - (2*x**2 - 7*x + 7)**2), (x, 1, 2))", "relation": "new"},
    {"text": "Value.", "expr": "13*pi/15", "relation": "equivalent"}
   ],
   "calculator_status": "no_calculator",
   "skills": ["BC-SKL-08054"]
  },
  {
   "id": "chk-3",
   "check_kind": "mcq",
   "format": "mcq",
   "bands": ["low"],
   "archetype_id": "BC-QA-08013",
   "parameter_draw": {"left": 0, "width": 1, "bulge": 1, "slope": 0, "intercept": 2, "depth": 2, "presentation": "formula", "axis": "above"},
   "stem": {"text": "R lies between f(x) = 2 + x(1 - x) and g(x) = 2. The volume about y = 4 is", "command_verb": "identify"},
   "key": {"form": "symbolic", "expr": "19*pi/30"},
   "steps": [
    {"text": "R = 2, r = x^2 - x + 2.", "expr": "pi*(4 - (x**2 - x + 2)**2)", "relation": "new"},
    {"text": "Limits 0 and 1.", "expr": "Integral(pi*(4 - (x**2 - x + 2)**2), (x, 0, 1))", "relation": "new"},
    {"text": "Value.", "expr": "19*pi/30", "relation": "equivalent"}
   ],
   "options": [
    {"id": "A", "is_key": false, "expr": "pi/30", "error_path": "BC-ERR-08030", "derivation": "pi times (R - r) squared"},
    {"id": "B", "is_key": false, "expr": "7*pi/10", "error_path": "BC-ERR-08038", "derivation": "f and g as the radii, measured from the x-axis"},
    {"id": "C", "is_key": false, "expr": "-19*pi/30", "error_path": "BC-ERR-08040", "derivation": "the higher curve taken as outer"},
    {"id": "D", "is_key": true, "expr": "19*pi/30", "error_path": null}
   ],
   "calculator_status": "no_calculator",
   "skills": ["BC-SKL-08054"]
  }
 ],
 "delivery": [
  {"block": "orientation", "mode": "text", "reason": "rule 6: a statement of what a response shows", "sources": ["BC-CON-08020"]},
  {
   "block": "ki-1",
   "mode": "interactive",
   "reason": "rule 4 promoted: BC-REP-08 and BC-REP-02 on BC-SKL-08054; BC-QA-08013 difficulty_variables name the axis position as the quantity that exchanges the radii, and the stem asks which curve is outer",
   "sources": ["BC-SKL-08054", "BC-QA-08013"],
   "spec": {
    "kind": "region_with_axis",
    "representations": ["BC-REP-02", "BC-REP-08"],
    "region": {"upper": "y = 1 + 2x - x^2", "lower": "y = 1", "interval": [0, 2]},
    "controls": [{"type": "slider", "name": "k", "values": [-1, 3], "start": -1, "drives": "the axis line y = k"}],
    "drawn": ["the axis y = k", "at x = 1, the two radii from the axis to each curve, the longer one marked outer"],
    "labels": [{"text": "outer R", "placement": "inside"}, {"text": "inner r", "placement": "inside"}, {"text": "y = k", "placement": "inside"}],
    "question": "When the line moves from below R to above it, which curve gives the outer radius?"
   },
   "fallback": "two static panels side by side, the axis at y = -1 and at y = 3, each with R and r marked at x = 1, labels inside",
   "keyboard": "Tab focuses the slider; Up and Down arrow keys move the line between y = -1 and y = 3; Enter reads R and r at x = 1"
  },
  {"block": "ex-1", "mode": "step_reveal", "reason": "rule 1", "sources": []},
  {"block": "ex-2", "mode": "step_reveal", "reason": "rule 1", "sources": []},
  {"block": "err-BC-ERR-08023", "mode": "step_reveal", "reason": "rule 1", "sources": []},
  {"block": "err-BC-ERR-08030", "mode": "step_reveal", "reason": "rule 1", "sources": []},
  {"block": "err-BC-ERR-08038", "mode": "step_reveal", "reason": "rule 1", "sources": []},
  {"block": "err-BC-ERR-08040", "mode": "step_reveal", "reason": "rule 1", "sources": []}
 ],
 "refresher": ["ki-1", "err-BC-ERR-08023", "err-BC-ERR-08030", "err-BC-ERR-08038", "err-BC-ERR-08040", "ex-1"],
 "read_minutes": {"full": 4.7, "brief": 3.0},
 "word_count": {"full": 691, "brief": 449},
 "research_lines": [{"file": "research/units/unit-08-applications-integration.md", "line": "When the axis lies above the region, the lower curve is the farther one, so the roles of the two curves exchange."}],
 "inferred": [
  {"claim": "BC-QA-08013 is calculator status either, so the lesson takes Section I Part A and its 2.14 minute budget.", "settles": "Timing data on shifted washer items split by exam part."},
  {"claim": "The answer point the scoring_pattern names is not tagged: BC-QA-08013 lists no answer point type.", "settles": "BC-PT-99004 added to BC-QA-08013's point_types."},
  {"claim": "ki-1 is served as an interactive with one slider for the axis line.", "settles": "The modality A/B in the build plan: skip rate and time to first credited success by mode."},
  {"claim": "Only horizontal axes are drawn: BC-QA-08013's parameter_spec has no vertical line, so BC-SKL-08053 is stated in ki-1 but not worked.", "settles": "A parameter_spec that draws a region revolved about x = h."},
  {
   "claim": "ex-1's limits point (BC-PT-99001) is earned but not tagged, and the possible_reason lines of the first two error blocks are dropped, because the prediction and contrast pair take the words they need in the brief band.",
   "settles": "A brief cap that admits the reader line and the reasons, or a shorter prediction and contrast."
  }
 ],
 "sources": [
  "BC-CON-08020",
  "BC-SKL-08052",
  "BC-SKL-08053",
  "BC-SKL-08054",
  "BC-SKL-08055",
  "BC-EK-CHA-5C4",
  "ced:163",
  "BC-QA-08013",
  "BC-PT-99058",
  "BC-PT-99001",
  "BC-ERR-08023",
  "BC-ERR-08030",
  "BC-ERR-08038",
  "BC-ERR-08040",
  "BC-MIS-08013",
  "BC-MIS-08017",
  "BC-MIS-08021",
  "BC-MIS-08023",
  "BC-PRQ-08002",
  "BC-PRQ-08004",
  "research/units/unit-08-applications-integration.md#8.12 Volume with Washer Method: Revolving Around Other Axes",
  "research/question-analysis/question-archetypes.md#BC-QA-08013 Volume of a solid of revolution by the washer method",
  "research/scoring/notation-requirements.md#Parentheses",
  "research/exam/exam-structure.md#Section and part layout"
 ]
}
```
