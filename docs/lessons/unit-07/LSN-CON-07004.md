---
title: LSN-CON-07004 Slope field as a plot of derivative values
research_date: 2026-09-29
status: designed
purpose: Authoring spec for the concept lesson on BC-CON-07004, computing and drawing slope field segments and reading the zero slope locus, built from authoring_bundle("BC-CON-07004") and the research files it cites, so an author fills plan 15's lesson record without making a teaching decision.
---

# LSN-CON-07004 Slope field as a plot of derivative values

Concept BC-CON-07004 (skills BC-SKL-07010 to BC-SKL-07013), topic 7.3 of Unit 7, loaded by BC-QA-07002 (family slope-field) and BC-QA-07010 (family de-qualitative-behaviour). Hard parent BC-CON-07001 (docs/lessons/unit-07/README.md, section 1).

## Prediction

One `mcq`, both bands, on ex-1's equation dy/dx = 2(y - x + 1): what the segment centred at (2, 0) does. Key A, falls with slope -2. The distractors are the slope with its sign lost (rises, slope 2) and the zero slope (flat), the value of the flat locus mistaken for every point. The point (2, 0) is not one of ex-1's three points, so the question is not ex-1's own. The student can settle it by putting the coordinates into the right side, before any rule is taught. The resolution states that the slope is the right side at the point. Sources: BC-CON-07004 and the topic 7.3 section the key idea cites.

## Orientation

Served text, from BC-CON-07004 `description_plain` and the topic's Assessment behaviour paragraph (research/units/unit-07-differential-equations.md#7.3 Sketching Slope Fields): a response puts each point's coordinates into the right side, draws a segment of that slope there, and finds where the right side is zero. No count, no frequency.

## Key ideas

BC-SKL-07010 and 07011 map to BC-EK-FUN-7C1; BC-SKL-07012 and 07013 map to BC-EK-FUN-7C2 (ced:139). Two core blocks, both bands.

- ki-1 (core), BC-EK-FUN-7C1, from the Construction paragraph. No quote, to hold the brief band.
- ki-2 (core), BC-EK-FUN-7C2. The zero slope sentence is from the Zero slope locus paragraph. The independence sentence rests on BC-SKL-07013 (`description_formal`: whether the slope depends on the independent variable, the dependent variable, or both, and the resulting pattern) and the BC-ERR-07013 `discriminating_probe`, with the direction checked in SymPy: for dy/dx = 2(y + 1) the slope is 2 at (0, 0), (1, 0) and (2, 0) and 4 at (0, 1). It is not taken from the research 7.3 Independence paragraph, which states the direction reversed [inferred]. Anchor quote from ced:139.

## Recognition

BC-QA-07002 (research/question-analysis/question-archetypes.md#BC-QA-07002 Slope field matched to or built from a differential equation): `typical_wording` "sketch the slope field for the given differential equation at the indicated points", "which of the following differential equations could have produced the slope field shown"; `common_givens` an equation or a printed field and a set of lattice points; `asked_to_produce` segment slopes at named points, or a matched equation. BC-QA-07010 (research/question-analysis/question-archetypes.md#BC-QA-07010 Behaviour of a solution obtained from the differential equation itself) reads the zero slope locus as a critical point. Shapes: MCQ matching (BC-MCQ-CED-009, BC-MCQ-SAMPLE-005) and short FRQ parts (BC-FRQ-2015-Q4-A, BC-FRQ-2026-Q3-A).

The contrast pair sits on st-1. Its near miss is the sibling BC-CON-07005 (docs/lessons/unit-07/README.md, section 3): a printed field and a request for the solution curve through one point, which draws a curve, not segments at named points. What says "not this concept": "sketch the solution curve through the given point" on a printed field (BC-CON-07005; docs/lessons/unit-07/README.md, section 3).

## Method choice

- st-1, BC-QA-07002: method `expected_solution_path[0]`, find where the right side vanishes, then evaluate at distinguishing points; rival `wrong_approaches`, solving the equation and differentiating the solution; feature: the stem names points, so each slope is a substitution.
- st-2, BC-QA-07010: method, set the right side equal to zero; rival, solving the equation first; feature: "critical point" with the equation given.

Both archetypes carry `asked_to_produce` and `common_givens`, so neither block is tagged inferred. st-1 carries the contrast pair, and no strategy field opens with its own label, because the reader prints Cue, First line, Rival and Separating feature.

## Solution path

- ex-1, BC-QA-07002, both bands. Draw: locus line, slope 1, intercept -1, orientation 1, scale 2, letters xy, so dy/dx = 2(y - x + 1). No published item carries this draw.
- Steps: right side zero (new); locus y = x - 1 (solve); slope at (0, 0), (1, 0), (0, 1) (new then evaluate, three times); the triple (new). A fluent solver writes the locus and the three values; the substitutions are held.

## Scoring

BC-QA-07002 lists BC-PT-99065, 99066, 99083. ex-1 tags BC-PT-99083 on the drawn segments; the line is reader_checks output. An explanation about a field references the sign of the segments' slopes (research/scoring/justification-requirements.md#Reasons about slope fields and concavity; sg-26:11).

## Traps

Six active errors meet the skills; the first four in the bundle's order: BC-ERR-07010, 07011, 07012, 07013. Low band all four; mid band the first two. All on ex-1's draw. All four relations are `distinct`, so all four blocks carry `fix_prompt: true`; no wrong or right text writes a decimal. Possible reason on BC-ERR-07011 only, words from BC-MIS-99015; the other linked descriptions do not name the slip.

## Representations

None as a separate block; the two key idea figures carry the slope field (BC-REP-07).

## Prerequisite bridge

- BC-PRQ-06005 and BC-PRQ-07006, from `description_plain` and `failure_signature`.

## Time

BC-QA-07002 is `no_calculator` and its `multipart_structure` names a single MCQ first, so Section I Part A, 2.14 minutes (research/exam/exam-structure.md#Section and part layout). The minutes go on the zero locus, which rules out most candidates at once.

## Checks

- chk-1, completion of ex-1: two slopes given, the third found. Key (2, 0, 4).
- chk-2, isomorph. Draw: line, slope -2, intercept 1, orientation -1, scale 1, ty; dy/dt = -(y + 2t - 1). Key (1, -1, 0).
- chk-3, MCQ, low band. Draw: parabola, slope 1, intercept 2, orientation 1, scale 1, xy; dy/dx = y - x^2 - 2, slope at (2, 3). Key -3. Distractors -9 (BC-ERR-07010), -2 (BC-ERR-07011), 1 (BC-ERR-07013).

## Delivery

- prediction: text. Rule 6: the question asks for a value from a substitution, not a reading of a picture. The drawn blocks below stay, so the lesson adds no figure.
- orientation, ki-1, ki-2: figure. Rule 4: BC-REP-07 on all four skills; not promoted, since BC-QA-07002 `difficulty_variables` vary a form, not a quantity (docs/lessons/unit-07/README.md, section 6) [inferred].
- ex-1 and the four error blocks: step_reveal. Rule 1.

## Band plan

- Low (full), in served order: prediction, orientation, two bridges when gated, ki-1, ki-2, st-1 with its contrast pair, st-2, ex-1 and its line, chk-1, four error blocks, chk-2, chk-3. 587 words, 4.0 minutes (cap 900 and 6). The lesson has one worked example, so nothing is faded.
- Mid (brief), in served order: prediction, orientation, bridges, ki-1, ki-2, st-1 with its contrast pair, ex-1 and its line, chk-1, err-BC-ERR-07010, err-BC-ERR-07011, chk-2. 449 words, 3.0 minutes (cap 450 and 3). The orientation, prediction, contrast texts, bridges, strategy fields and ex-1 step cues were shortened to fit; no anchor quote or scoring tag was dropped.
- Refresher: ki-1, ki-2, the four error blocks, ex-1.

## Sources

- BC-CON-07004; BC-SKL-07010 to BC-SKL-07013; BC-EK-FUN-7C1, BC-EK-FUN-7C2; ced:139
- BC-QA-07002, BC-QA-07010; BC-PT-99083; sg-26:11; BC-MCQ-CED-009, BC-MCQ-SAMPLE-005, BC-FRQ-2015-Q4-A, BC-FRQ-2026-Q3-A
- BC-ERR-07010, BC-ERR-07011, BC-ERR-07012, BC-ERR-07013; BC-MIS-99015
- BC-PRQ-06005, BC-PRQ-07006
- research/units/unit-07-differential-equations.md#7.3 Sketching Slope Fields
- research/question-analysis/question-archetypes.md#BC-QA-07002 Slope field matched to or built from a differential equation
- research/question-analysis/question-archetypes.md#BC-QA-07010 Behaviour of a solution obtained from the differential equation itself
- research/scoring/justification-requirements.md#Reasons about slope fields and concavity
- research/exam/exam-structure.md#Section and part layout
- [inferred] Figures rather than text. Settled by the modality A/B.
- [inferred] ki-2's independence direction, from BC-SKL-07013 and SymPy, since the research 7.3 Independence paragraph states it reversed. Settled by a corrected research paragraph or a CED line.

## Machine record

```json
{
 "id": "LSN-CON-07004",
 "kind": "concept",
 "target_id": "BC-CON-07004",
 "unit": "07",
 "skills": ["BC-SKL-07010", "BC-SKL-07011", "BC-SKL-07012", "BC-SKL-07013"],
 "prediction": {
  "id": "pr-1",
  "stem": {"text": "For dy/dx = 2(y - x + 1), what does the segment at (2, 0) do?", "command_verb": "predict"},
  "format": "mcq",
  "options": [{"id": "A", "label": "Falls, slope -2", "is_key": true}, {"id": "B", "label": "Rises, slope 2", "is_key": false}, {"id": "C", "label": "Lies flat", "is_key": false}],
  "resolution": "The slope there is 2(0 - 2 + 1) = -2.",
  "sources": ["BC-CON-07004", "research/units/unit-07-differential-equations.md#7.3 Sketching Slope Fields"]
 },
 "orientation": {
  "text": "A segment's slope is the right side at its point.",
  "sources": ["BC-CON-07004", "research/units/unit-07-differential-equations.md#7.3 Sketching Slope Fields"]
 },
 "key_ideas": [
  {
   "id": "ki-1",
   "ek_id": "BC-EK-FUN-7C1",
   "depth": "core",
   "text": "Evaluate the right side at each grid point and draw a segment of that slope.",
   "notation": "slope field; lattice point",
   "quote": null,
   "sources": ["BC-EK-FUN-7C1", "ced:139", "research/units/unit-07-differential-equations.md#7.3 Sketching Slope Fields"]
  },
  {
   "id": "ki-2",
   "ek_id": "BC-EK-FUN-7C2",
   "depth": "core",
   "text": "Segments are flat where the right side vanishes. With no x in it, they repeat along horizontal lines; with no y, along vertical lines.",
   "notation": "segment slope",
   "quote": {"text": "Slope fields provide information about the behavior of solutions to first-order differential equations.", "source": "ced:139"},
   "sources": ["BC-EK-FUN-7C2", "ced:139", "BC-SKL-07013", "BC-ERR-07013", "research/units/unit-07-differential-equations.md#7.3 Sketching Slope Fields"]
  }
 ],
 "strategy": [
  {
   "id": "st-1",
   "archetype_id": "BC-QA-07002",
   "cue": "Named points, or a field to match.",
   "method": "Right side zero, then its value at each point.",
   "rival": "Solving, then differentiating.",
   "separating_feature": "Each slope is a substitution.",
   "sources": ["BC-QA-07002"],
   "evidence_tag": "verified",
   "contrast": {
    "this": {"text": "Sketch the slope field of dy/dx = y - 2x at (0, 0).", "archetype_id": "BC-QA-07002"},
    "not_this": {"text": "Sketch the solution curve through (0, 1) on the printed slope field.", "why_not": "It asks for a curve, not segments."},
    "feature": "Segments, or a curve."
   }
  },
  {
   "id": "st-2",
   "archetype_id": "BC-QA-07010",
   "cue": "An equation, a bound on the quantity, and a request for a critical point.",
   "method": "The right side set equal to zero.",
   "rival": "Solving the differential equation first.",
   "separating_feature": "The equation already gives dy/dx, so zero slope is read from it.",
   "sources": ["BC-QA-07010"],
   "evidence_tag": "verified"
  }
 ],
 "worked_examples": [
  {
   "id": "ex-1",
   "archetype_id": "BC-QA-07002",
   "bands": ["low", "mid"],
   "parameter_draw": {"locus": "line", "slope": 1, "intercept": -1, "orientation": 1, "scale": 2, "letters": "xy"},
   "problem": {"text": "For dy/dx = 2(y - x + 1), sketch the slope field at (0, 0), (1, 0) and (0, 1).", "command_verb": "sketch"},
   "calculator_status": "no_calculator",
   "steps": [
    {"cue": "Right side zero.", "why": "Flat.", "expr": "2*(y - x + 1) = 0", "relation": "new"},
    {"cue": "Solve.", "why": "Flat on y = x - 1.", "expr": "x - 1", "relation": "solve", "variable": "y"},
    {"cue": "Named point.", "why": "Substitute.", "expr": "2*(y - x + 1)", "relation": "new"},
    {"cue": "At (0, 0).", "why": "Slope 2.", "expr": "2", "relation": "evaluate", "subs": {"x": "0", "y": "0"}},
    {"cue": "Next.", "why": "Substitute.", "expr": "2*(y - x + 1)", "relation": "new"},
    {"cue": "At (1, 0).", "why": "Flat.", "expr": "0", "relation": "evaluate", "subs": {"x": "1", "y": "0"}},
    {"cue": "Next.", "why": "Substitute.", "expr": "2*(y - x + 1)", "relation": "new"},
    {"cue": "At (0, 1).", "why": "Steeper: 4.", "expr": "4", "relation": "evaluate", "subs": {"x": "0", "y": "1"}},
    {"cue": "Draw.", "why": "Named points only.", "expr": "Tuple(2, 0, 4)", "relation": "new", "point_type_id": "BC-PT-99083"}
   ],
   "answer": {"form": "symbolic", "expr": "Tuple(2, 0, 4)"}
  }
 ],
 "what_a_reader_scores": [
  {
   "example_id": "ex-1",
   "point_type_ids": ["BC-PT-99083"],
   "lines": [
    {
     "point_type_id": "BC-PT-99083",
     "text": "Slope field drawn at the indicated points. Earned by: Short segments drawn at the indicated points whose slopes match the differential equation there. samples-15-q4:1 splits the two points of the part by the value of the independent variable, so the segments at each value of that variable are scored as a group. Not earned by: Segments drawn at points other than the indicated ones, or a solution curve drawn in place of the field; the rubric scores the segments at the indicated points only (samples-15-q4:1)."
    }
   ]
  }
 ],
 "common_errors": [
  {
   "error_id": "BC-ERR-07010",
   "observed_behavior": "The response computes the segment slope using coordinates taken from a neighbouring point of the grid.",
   "scoring_consequence": "The drawn or matched field is wrong at the points that distinguish the candidates.",
   "wrong_step": {"text": "Swapped x and y.", "expr": "4"},
   "right_step": {"text": "At (1, 0).", "expr": "0"},
   "relation": "distinct",
   "possible_reason": null,
   "sources": ["BC-ERR-07010"],
   "fix_prompt": true
  },
  {
   "error_id": "BC-ERR-07011",
   "observed_behavior": "The drawn field uses the same steepness everywhere regardless of the computed slopes.",
   "scoring_consequence": "The field carries no information and no solution curve can be read from it.",
   "wrong_step": {"text": "Tilt of (0, 0) reused.", "expr": "2"},
   "right_step": {"text": "Computed.", "expr": "0"},
   "relation": "distinct",
   "possible_reason": {"misconception_id": "BC-MIS-99015", "text": "takes the slope field to show one tangent line through the chosen point"},
   "sources": ["BC-ERR-07011", "BC-MIS-99015"],
   "fix_prompt": true
  },
  {
   "error_id": "BC-ERR-07012",
   "observed_behavior": "The response never solves the right side equal to zero, so the horizontal segments are missed.",
   "scoring_consequence": "The equilibrium level is unavailable, which costs the sketch point and the critical point work that follows.",
   "wrong_step": {"text": "Right side left unsolved.", "expr": "2*(y - x + 1)"},
   "right_step": {"text": "Flat on y = x - 1.", "expr": "y = x - 1"},
   "relation": "distinct",
   "possible_reason": null,
   "sources": ["BC-ERR-07012"],
   "fix_prompt": true
  },
  {
   "error_id": "BC-ERR-07013",
   "observed_behavior": "The response claims the slope varies along a line on which the printed segments are identical, or the reverse.",
   "scoring_consequence": "The match to a candidate equation is made on a false feature.",
   "wrong_step": {"text": "Read as y only.", "expr": "2*(y + 1)"},
   "right_step": {"text": "Depends on both.", "expr": "2*(y - x + 1)"},
   "relation": "distinct",
   "possible_reason": null,
   "sources": ["BC-ERR-07013"],
   "fix_prompt": true
  }
 ],
 "representations": null,
 "prerequisite_bridges": [
  {"prq_id": "BC-PRQ-06005", "text": "x = 1, y = 0 at (1, 0)."},
  {"prq_id": "BC-PRQ-07006", "text": "Use the point's own coordinates."}
 ],
 "time": {
  "exam_part": "I-A",
  "budget_minutes": 2.14,
  "source": "research/exam/exam-structure.md#Section and part layout",
  "written_steps": {"ex-1": [2, 4, 6, 8, 9]},
  "skipped_steps": {"ex-1": [1, 3, 5, 7]}
 },
 "checks": [
  {
   "id": "chk-1",
   "check_kind": "completion",
   "format": "short_answer",
   "bands": ["low", "mid"],
   "archetype_id": "BC-QA-07002",
   "parameter_draw": {"locus": "line", "slope": 1, "intercept": -1, "orientation": 1, "scale": 2, "letters": "xy"},
   "completes": "ex-1",
   "stem": {"text": "dy/dx = 2(y - x + 1) has slopes 2 at (0, 0) and 0 at (1, 0). Give the slopes at (0, 0), (1, 0), (0, 1).", "command_verb": "find"},
   "key": {"form": "symbolic", "expr": "Tuple(2, 0, 4)"},
   "steps": [
    {"text": "Right side.", "expr": "2*(y - x + 1)", "relation": "new"},
    {"text": "At (0, 1).", "expr": "4", "relation": "evaluate", "subs": {"x": "0", "y": "1"}},
    {"text": "The three.", "expr": "Tuple(2, 0, 4)", "relation": "new"}
   ],
   "calculator_status": "no_calculator",
   "skills": ["BC-SKL-07010"]
  },
  {
   "id": "chk-2",
   "check_kind": "isomorph",
   "format": "short_answer",
   "bands": ["low", "mid"],
   "archetype_id": "BC-QA-07002",
   "parameter_draw": {"locus": "line", "slope": -2, "intercept": 1, "orientation": -1, "scale": 1, "letters": "ty"},
   "stem": {"text": "For dy/dt = -(y + 2t - 1), give the slopes at (0, 0), (1, 0), (0, 1).", "command_verb": "find"},
   "key": {"form": "symbolic", "expr": "Tuple(1, -1, 0)"},
   "steps": [
    {"text": "Right side.", "expr": "-(y + 2*t - 1)", "relation": "new"},
    {"text": "(0, 0).", "expr": "1", "relation": "evaluate", "subs": {"t": "0", "y": "0"}},
    {"text": "Right side.", "expr": "-(y + 2*t - 1)", "relation": "new"},
    {"text": "(1, 0).", "expr": "-1", "relation": "evaluate", "subs": {"t": "1", "y": "0"}},
    {"text": "Right side.", "expr": "-(y + 2*t - 1)", "relation": "new"},
    {"text": "(0, 1).", "expr": "0", "relation": "evaluate", "subs": {"t": "0", "y": "1"}},
    {"text": "The three.", "expr": "Tuple(1, -1, 0)", "relation": "new"}
   ],
   "calculator_status": "no_calculator",
   "skills": ["BC-SKL-07010"]
  },
  {
   "id": "chk-3",
   "check_kind": "mcq",
   "format": "mcq",
   "bands": ["low"],
   "archetype_id": "BC-QA-07002",
   "parameter_draw": {"locus": "parabola", "slope": 1, "intercept": 2, "orientation": 1, "scale": 1, "letters": "xy"},
   "stem": {"text": "For dy/dx = y - x^2 - 2, what is the slope of the segment at (2, 3)?", "command_verb": "identify"},
   "key": {"form": "numeric", "expr": "-3"},
   "steps": [{"text": "Right side.", "expr": "y - x**2 - 2", "relation": "new"}, {"text": "At (2, 3).", "expr": "-3", "relation": "evaluate", "subs": {"x": "2", "y": "3"}}],
   "options": [
    {"id": "A", "is_key": false, "expr": "-9", "error_path": "BC-ERR-07010", "derivation": "evaluated at (3, 2)"},
    {"id": "B", "is_key": true, "expr": "-3", "error_path": null},
    {"id": "C", "is_key": false, "expr": "-2", "error_path": "BC-ERR-07011", "derivation": "the tilt at (0, 0) used everywhere"},
    {"id": "D", "is_key": false, "expr": "1", "error_path": "BC-ERR-07013", "derivation": "x read as absent: y - 2"}
   ],
   "calculator_status": "no_calculator",
   "skills": ["BC-SKL-07010", "BC-SKL-07013"]
  }
 ],
 "delivery": [
  {
   "block": "orientation",
   "mode": "figure",
   "reason": "rule 4: BC-REP-07 on BC-SKL-07010 to 07013; not promoted, the difficulty_variables vary a form",
   "sources": ["BC-SKL-07010"],
   "spec": {
    "kind": "slope_field",
    "representations": ["BC-REP-07", "BC-REP-06"],
    "equation": "dy/dx = 2*(y - x + 1)",
    "window": {"x": [-2, 2], "y": [-2, 2]},
    "lattice_step": 1,
    "labels": [{"text": "dy/dx = 2(y - x + 1)", "placement": "inside", "at": "top left corner"}]
   },
   "fallback": "a static grid of segments with the equation written inside",
   "keyboard": "no control; Tab reaches the figure's text description"
  },
  {
   "block": "ki-1",
   "mode": "figure",
   "reason": "rule 4: BC-REP-07 on BC-SKL-07010, 07011",
   "sources": ["BC-SKL-07010", "BC-SKL-07011"],
   "spec": {
    "kind": "slope_field",
    "representations": ["BC-REP-07"],
    "equation": "dy/dx = 2*(y - x + 1)",
    "window": {"x": [-2, 2], "y": [-2, 2]},
    "lattice_step": 1,
    "marked": [[0, 0], [0, 1]],
    "labels": [{"text": "slope 2 at (0, 0)", "placement": "inside", "at": "beside (0, 0)"}, {"text": "slope 4 at (0, 1)", "placement": "inside", "at": "beside (0, 1)"}]
   },
   "fallback": "the same grid, static, with the two slope values listed inside",
   "keyboard": "no control; Tab reaches the figure's text description"
  },
  {
   "block": "ki-2",
   "mode": "figure",
   "reason": "rule 4: BC-REP-07 on BC-SKL-07012, 07013",
   "sources": ["BC-SKL-07012", "BC-SKL-07013"],
   "spec": {
    "kind": "slope_field",
    "representations": ["BC-REP-07"],
    "equation": "dy/dx = 2*(y - x + 1)",
    "window": {"x": [-2, 2], "y": [-2, 2]},
    "lattice_step": 1,
    "highlight": "the flat segments on y = x - 1",
    "labels": [{"text": "flat on y = x - 1", "placement": "inside", "at": "along the flat segments"}]
   },
   "fallback": "the same grid, static, with the flat segments drawn heavier and labelled inside",
   "keyboard": "no control; Tab reaches the figure's text description"
  },
  {"block": "ex-1", "mode": "step_reveal", "reason": "rule 1", "sources": []},
  {"block": "err-BC-ERR-07010", "mode": "step_reveal", "reason": "rule 1", "sources": []},
  {"block": "err-BC-ERR-07011", "mode": "step_reveal", "reason": "rule 1", "sources": []},
  {"block": "err-BC-ERR-07012", "mode": "step_reveal", "reason": "rule 1", "sources": []},
  {"block": "err-BC-ERR-07013", "mode": "step_reveal", "reason": "rule 1", "sources": []}
 ],
 "refresher": ["ki-1", "ki-2", "err-BC-ERR-07010", "err-BC-ERR-07011", "err-BC-ERR-07012", "err-BC-ERR-07013", "ex-1"],
 "read_minutes": {
  "full": 4.0,
  "brief": 3.0
 },
 "word_count": {
  "full": 586,
  "brief": 448
 },
 "research_lines": [
  {"file": "research/units/unit-07-differential-equations.md", "line": "Segments are horizontal exactly where the right side vanishes"}
 ],
 "inferred": [
  {
   "claim": "The orientation and both key ideas are served as static figures rather than text.",
   "settles": "The modality A/B in the build plan: skip rate and time to first credited success by mode."
  },
  {
   "claim": "ki-2's independence direction (no x: identical along each horizontal line; no y: along each vertical line) is derived from BC-SKL-07013 and checked in SymPy, because research/units/unit-07-differential-equations.md 7.3 Independence states it reversed.",
   "settles": "A corrected Independence paragraph in the research file, or a CED line stating the pattern."
  }
 ],
 "sources": ["BC-CON-07004", "BC-SKL-07010", "BC-SKL-07011", "BC-SKL-07012", "BC-SKL-07013", "BC-EK-FUN-7C1", "BC-EK-FUN-7C2", "ced:139", "BC-QA-07002", "BC-QA-07010", "BC-PT-99083", "sg-26:11", "BC-ERR-07010", "BC-ERR-07011", "BC-ERR-07012", "BC-ERR-07013", "BC-MIS-99015", "BC-PRQ-06005", "BC-PRQ-07006", "research/units/unit-07-differential-equations.md#7.3 Sketching Slope Fields", "research/question-analysis/question-archetypes.md#BC-QA-07002 Slope field matched to or built from a differential equation", "research/question-analysis/question-archetypes.md#BC-QA-07010 Behaviour of a solution obtained from the differential equation itself", "research/scoring/justification-requirements.md#Reasons about slope fields and concavity", "research/exam/exam-structure.md#Section and part layout"]
}
```
