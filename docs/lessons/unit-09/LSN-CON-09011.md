---
title: LSN-CON-09011 Direction of motion read from the signs of the velocity components
research_date: 2026-09-29
status: designed
purpose: Authoring spec for the concept lesson on BC-CON-09011, a particle moving toward an axis when its coordinate and that coordinate's rate have opposite signs, built from authoring_bundle("BC-CON-09011") and the research files it cites, so an author fills plan 15's lesson record without making a teaching decision.
---

# LSN-CON-09011 Direction of motion read from the signs of the velocity components

Concept BC-CON-09011 (skill BC-SKL-09027), topic 9.6 of Unit 9, BC only (ced:176), loaded by one archetype, BC-QA-09008 (family parametric-motion). The Unit 9 hard parent is BC-CON-09001 (docs/lessons/unit-09/README.md, section 1), so a curve given by component functions is assumed.

## Prediction

Served first, both bands: an `mcq` on ex-1's own numbers. The coordinate \(x(t)=2\sin t-t^2/2-6\) is negative on the interval and \(x'(0)=2\). Key A, toward the y-axis, because x rises toward 0. The distractors are the sign-of-position reading (away because x is negative) and a rising-means-away reading. The distance from the axis is \(|x|\), which shrinks from 6, so the question is answerable before any rule. The resolution states the opposite-signs condition with no verdict word. Source: BC-CON-09011 and the topic section the key idea cites.

## Orientation

Served text, from BC-CON-09011 `description_plain` ("Each component sign says which way the particle is moving along that axis") and the topic's Assessment behaviour paragraph (research/units/unit-09-parametric-polar-vector.md#9.6 Solving Motion Problems Using Parametric and Vector-Valued Functions): the justification variants ask for the reason a particle approaches an axis. The orientation states what a response shows. No count, no frequency.

## Key ideas

One essential knowledge statement, BC-EK-FUN-8B1 (ced:176): one core block, both bands.

- ki-1 (core). Paraphrase of the Required mathematical knowledge paragraphs Velocity, speed, acceleration and Direction of motion: derivatives give velocity on a planar path, and a particle in the first quadrant moves toward the x axis exactly when y is positive and its rate negative, scored as a sign consideration and an answer with the reason (sg-24:8). Notation line: the concept's `notation`. No anchor quote.

## Recognition

- BC-QA-09008 (research/question-analysis/question-archetypes.md#BC-QA-09008 Times at which a particle moves toward a coordinate axis): `common_givens` a velocity component, a statement about the quadrant the particle stays in, and an interval; `asked_to_produce` a sign argument and a subinterval of times; `typical_wording` find all times at which the particle is moving toward the named axis and give a reason. The closing part of the calculator FRQ, BC-FRQ-2024-Q2-D.

What says this concept: moving toward an axis, with a stated sign for the coordinate. What says a different concept: the sign of a coordinate alone, a speed, or a slope of the path. The contrast pair takes the near miss from the rival in `wrong_approaches`, reading the direction from the sign of the position: the same position, asked as the times at which the coordinate is negative.

## Method choice

- st-1, BC-QA-09008. Method, `expected_solution_path[0]` to `[2]`: state the sign of the coordinate, solve for where the velocity component is zero, determine the subinterval on which the signs differ. Rival, `wrong_approaches`: reading the direction from the sign of the position. Separating feature: the comparison of the two signs. Both cue fields exist, so the block is not inferred. The block carries the contrast pair. No served field opens with the reader's own label.

## Solution path

- ex-1, BC-QA-09008, both bands, calculator. Draw: offset 6, amplitude 2, divisor 2, end_time 3, other_turn 2, shape rising, axis y-axis, sign_given stated, side negative. No published item on BC-QA-09008 carries this draw (content/items_*). Zero of \(x'\) at 1.030 by SymPy.
- ex-2, low band, calculator. Draw: offset 7, amplitude 3, divisor 3, end_time 5/2, other_turn 3, shape falling, axis x-axis, sign_given stated, side positive. No published item carries it. Zero of \(y'\) at 1.282, approach after it.
- ex-2 is faded from step 3: the coordinate and its rate are shown, the student writes the interval, and the zero and the interval then reveal. The fade falls there because the setup repeats ex-1 and the sign argument is what the student must produce.
- Steps follow `expected_solution_path`: the coordinate (new), its rate (differentiate), the zero (solve), the interval (new). A fluent solver writes the rate and the interval with its reason and holds the coordinate's sign and the calculator solve.

No productive-failure opener targets this concept, so no comparison callout.

## Scoring

BC-QA-09008 lists BC-PT-99014 and BC-PT-99010. ex-1 tags nothing, since the brief cap has no room for a reader line (inferred array); ex-2 tags BC-PT-99014 on the rate step and BC-PT-99010 on the closing interval. The lines are `reader_checks` output.

Point losses research names for this shape: a local argument where a global one was required (research/scoring/common-point-losses.md#Justification points); a variable expression equated to a numerical value (research/scoring/common-point-losses.md#Notation points).

## Traps

Three errors meet the skill, in the bundle's order: BC-ERR-09025, BC-ERR-09026, BC-ERR-99029. Low band all three, mid band the first two. All on ex-1's draw. 09025 and 99029 carry `fix_prompt` true, since each pair is distinct; 09026 is equivalent (the same interval, with and without the reason), so its `fix_prompt` is false. Possible reason lines are dropped to fit the brief cap.

## Representations

None. The topic's Representations paragraph names BC-REP-14, 12, 09 and 05 and conversions from signs to a verbal statement; the figure it would carry is the orientation figure, so a second block would repeat it.

## Prerequisite bridge

- BC-PRQ-08001, from its `description_plain` and `failure_signature`.

## Time

The MCQ form is Section I Part B, calculator, 2.92 minutes (research/exam/exam-structure.md#Section and part layout). As the closing free response part: 2 points, 3.33 minutes (docs/lessons/unit-09/README.md, section 5). A fluent solver writes the rate and the interval with its reason; the coordinate's sign and the calculator solve are held.

## Checks

- chk-1, completion of ex-1, both bands: the sign of x' given, the interval asked. Key \((0, 1.030)\).
- chk-2, isomorph, both bands. Draw: offset 8, amplitude 3, divisor 2, end_time 3, other_turn 1, shape rising, axis x-axis, sign_given stated, side positive. Key \((0, 1.170)\).
- chk-3, MCQ, low band. Draw: offset 6, amplitude 3, divisor 2, end_time 3, other_turn 3, shape falling, axis y-axis, sign_given stated, side negative. Key \((1.170, 3)\). Distractors: \((0,3)\), the sign of x read as direction (BC-ERR-09025); \((0, 1.170)\), the times with a negative rate (BC-ERR-09025); \((0, 1.732)\), the other component (BC-ERR-99029). BC-ERR-09025 serves two distractors, because BC-ERR-09026 is a missing sentence and has no value.

## Delivery

- orientation: figure. Rule 4: BC-REP-14 on BC-SKL-09027. The path with the y-axis and two marked times.
- ki-1: interactive. Rule 4 promoted: BC-QA-09008 `common_givens` name a velocity component and an interval, and the stem asks for a sign argument. One slider, the time; the reading is toward or away and the two signs that decide it.
- ex-1, ex-2, the three error blocks: step_reveal. Rule 1.

## Band plan

- Low (full): prediction, orientation, bridges, ki-1, st-1 with the contrast pair, ex-1 and its line, chk-1, the three error blocks, ex-2 (faded from step 3) and its lines, chk-2, chk-3. 773 words, 5.2 minutes.
- Mid (brief): prediction, orientation, bridges, ki-1, st-1 with the contrast pair, ex-1 and its line, chk-1, err-BC-ERR-09025, err-BC-ERR-09026, chk-2. 449 words, 3.0 minutes.
- Refresher: ki-1, the three error blocks, ex-1.

## Sources

- BC-CON-09011; BC-SKL-09027; BC-EK-FUN-8B1; ced:176
- BC-QA-09008; BC-PT-99014, BC-PT-99010
- BC-ERR-09025, BC-ERR-09026, BC-ERR-99029; BC-MIS-09012
- BC-PRQ-08001
- sg-24:8
- research/units/unit-09-parametric-polar-vector.md#9.6 Solving Motion Problems Using Parametric and Vector-Valued Functions
- research/question-analysis/question-archetypes.md#BC-QA-09008 Times at which a particle moves toward a coordinate axis
- research/exam/exam-structure.md#Section and part layout
- [inferred] the held steps; the untagged points on ex-1; every non-text delivery mode. Each settled as the inferred array states.

## Machine record

```json
{
 "id": "LSN-CON-09011",
 "kind": "concept",
 "target_id": "BC-CON-09011",
 "unit": "09",
 "skills": [
  "BC-SKL-09027"
 ],
 "prediction": {
  "id": "pr-1",
  "stem": {
   "text": "A particle has \\(x(t)=2\\sin t-\\frac{t^2}{2}-6<0\\) on \\(0\\le t\\le 3\\), with \\(x'(0)=2\\). Predict whether it moves toward or away from the y-axis at \\(t=0\\).",
   "command_verb": "predict"
  },
  "format": "mcq",
  "options": [
   {
    "id": "A",
    "label": "Toward, because \\(x\\) is rising toward 0",
    "is_key": true
   },
   {
    "id": "B",
    "label": "Away, because \\(x\\) is negative",
    "is_key": false
   },
   {
    "id": "C",
    "label": "Away, because \\(x\\) is rising",
    "is_key": false
   }
  ],
  "resolution": "At \\(t=0\\), \\(x=-6\\) and \\(x'=2\\), so \\(|x|\\) shrinks and the particle approaches the y-axis. Approach means the coordinate and its rate have opposite signs.",
  "sources": [
   "BC-CON-09011",
   "research/units/unit-09-parametric-polar-vector.md#9.6 Solving Motion Problems Using Parametric and Vector-Valued Functions"
  ]
 },
 "orientation": {
  "text": "A response compares the sign of the coordinate with the sign of its velocity component, finds where that component changes sign, and gives the interval with the reason.",
  "sources": [
   "BC-CON-09011",
   "research/units/unit-09-parametric-polar-vector.md#9.6 Solving Motion Problems Using Parametric and Vector-Valued Functions"
  ]
 },
 "key_ideas": [
  {
   "id": "ki-1",
   "ek_id": "BC-EK-FUN-8B1",
   "depth": "core",
   "text": "Derivatives give velocity on a planar path. A particle moves toward the x-axis when \\(y\\) and \\(y'\\) have opposite signs, and toward the y-axis when \\(x\\) and \\(x'\\) do. The answer states the sign of the rate as its reason.",
   "notation": "sign of a velocity component",
   "quote": null,
   "sources": [
    "BC-EK-FUN-8B1",
    "ced:176",
    "sg-24:8",
    "research/units/unit-09-parametric-polar-vector.md#9.6 Solving Motion Problems Using Parametric and Vector-Valued Functions"
   ]
  }
 ],
 "strategy": [
  {
   "id": "st-1",
   "archetype_id": "BC-QA-09008",
   "cue": "A stated coordinate sign, a velocity component, moving toward an axis.",
   "method": "The sign of the coordinate, the zero of its rate, then the interval where the signs differ.",
   "rival": "Reading the direction from the sign of the position.",
   "separating_feature": "Approach compares the coordinate's sign with its rate's sign.",
   "sources": [
    "BC-QA-09008"
   ],
   "evidence_tag": "verified",
   "contrast": {
    "this": {
     "text": "A particle has position \\((3\\sin t-\\frac{t^2}{4}-9,\\ t^2)\\), with \\(x(t)<0\\) on \\([0,2]\\). Find when it moves toward the y-axis.",
     "archetype_id": "BC-QA-09008"
    },
    "not_this": {
     "text": "A particle has position \\((3\\sin t-\\frac{t^2}{4}-9,\\ t^2)\\). Find when its x-coordinate is negative on \\([0,2]\\).",
     "why_not": "It asks about the sign of the position; no rate is compared."
    },
    "feature": "Approach needs the rate's sign, not the position's."
   }
  }
 ],
 "worked_examples": [
  {
   "id": "ex-1",
   "archetype_id": "BC-QA-09008",
   "bands": [
    "low",
    "mid"
   ],
   "parameter_draw": {
    "offset": 6,
    "amplitude": 2,
    "divisor": 2,
    "end_time": 3,
    "other_turn": 2,
    "shape": "rising",
    "axis": "y-axis",
    "sign_given": "stated",
    "side": "negative"
   },
   "problem": {
    "text": "A particle has position \\((2\\sin t-\\frac{t^2}{2}-6,\\ 2t-\\frac{t^3}{3})\\), with \\(x(t)<0\\) for \\(0\\le t\\le 3\\). Using a calculator, find the times \\(0<t<3\\) at which it moves toward the y-axis, with a reason.",
    "command_verb": "find"
   },
   "calculator_status": "calculator",
   "steps": [
    {
     "cue": "The y-axis: track x.",
     "why": "Negative x approaches 0 when x rises.",
     "expr": "-t**2/2 + 2*sin(t) - 6",
     "relation": "new"
    },
    {
     "cue": "Its rate says whether x rises.",
     "why": "Rising x with negative x means approach.",
     "expr": "2*cos(t) - t",
     "relation": "differentiate",
     "variable": "t"
    },
    {
     "cue": "The rate changes sign at zero.",
     "why": "Calculator solve, radian mode.",
     "expr": "1.029866529322259",
     "relation": "solve",
     "variable": "t"
    },
    {
     "cue": "The rate is positive before it.",
     "why": "Signs of x and x' differ there.",
     "expr": "Interval.open(0, 1.030)",
     "relation": "new"
    }
   ],
   "answer": {
    "form": "symbolic",
    "expr": "Interval.open(0, 1.030)"
   }
  },
  {
   "id": "ex-2",
   "archetype_id": "BC-QA-09008",
   "bands": [
    "low"
   ],
   "parameter_draw": {
    "offset": 7,
    "amplitude": 3,
    "divisor": 3,
    "end_time": "5/2",
    "other_turn": 3,
    "shape": "falling",
    "axis": "x-axis",
    "sign_given": "stated",
    "side": "positive"
   },
   "problem": {
    "text": "A particle has position \\((3t-\\frac{t^3}{3},\\ 7+3\\sin t-\\frac{t^2}{3})\\) for \\(0\\le t\\le 5/2\\), and \\(y(t)>0\\). Using a calculator, find all times \\(0<t<5/2\\) at which it moves toward the x-axis. Give a reason.",
    "command_verb": "find"
   },
   "calculator_status": "calculator",
   "steps": [
    {
     "cue": "Toward the x-axis: the y-coordinate is the one to track.",
     "why": "Positive y approaches 0 when y falls.",
     "expr": "-t**2/3 + 3*sin(t) + 7",
     "relation": "new"
    },
    {
     "cue": "Its rate decides whether y falls.",
     "why": "Falling y with positive y means approach.",
     "expr": "3*cos(t) - 2*t/3",
     "relation": "differentiate",
     "variable": "t",
     "point_type_id": "BC-PT-99014"
    },
    {
     "cue": "The rate changes sign where it is zero.",
     "why": "Calculator solve, radian mode.",
     "expr": "1.281923540625690",
     "relation": "solve",
     "variable": "t"
    },
    {
     "cue": "The rate is negative after that time.",
     "why": "There y is positive and y' negative, so opposite signs.",
     "expr": "Interval.open(1.282, 5/2)",
     "relation": "new",
     "point_type_id": "BC-PT-99010"
    }
   ],
   "answer": {
    "form": "symbolic",
    "expr": "Interval.open(1.282, 5/2)"
   },
   "fade_from": 3
  }
 ],
 "what_a_reader_scores": [
  {
   "example_id": "ex-1",
   "point_type_ids": [],
   "lines": []
  },
  {
   "example_id": "ex-2",
   "point_type_ids": [
    "BC-PT-99014",
    "BC-PT-99010"
   ],
   "lines": [
    {
     "point_type_id": "BC-PT-99014",
     "text": "Considers the sign of a derivative. Earned by: An explicit statement about whether a first or second derivative is positive, negative, or zero on the relevant interval, symbolically or in words (sg-26:12, sg-24:8). Not earned by: A statement about the sign of the function rather than the derivative, or a reference to the concavity of the derivative itself (sg-26:12)."
    },
    {
     "point_type_id": "BC-PT-99010",
     "text": "Justification by sign analysis of a derivative. Earned by: A statement that the derivative is positive on one side and negative on the other, closed by a global claim about the whole interval (sg-25:5, sg-25:9). Not earned by: A local argument only, such as a bare First or Second Derivative Test with no statement that the critical point is the only one on the interval (sg-25:5, sg-22:12)."
    }
   ]
  }
 ],
 "common_errors": [
  {
   "error_id": "BC-ERR-09025",
   "observed_behavior": "The response says the particle approaches an axis on the interval where the coordinate itself is negative.",
   "scoring_consequence": "The point for considering the sign of the rate is lost (sg-24:8).",
   "wrong_step": {
    "text": "Toward for \\(0<t<3\\), because \\(x<0\\).",
    "expr": "Interval.open(0, 3)"
   },
   "right_step": {
    "text": "Toward for \\(0<t<1.030\\), because \\(x<0\\) and \\(x'>0\\).",
    "expr": "Interval.open(0, 1.030)"
   },
   "relation": "distinct",
   "possible_reason": null,
   "sources": [
    "BC-ERR-09025"
   ],
   "fix_prompt": true
  },
  {
   "error_id": "BC-ERR-09026",
   "observed_behavior": "A correct subinterval of times is given with no statement about the sign of the relevant rate.",
   "scoring_consequence": "The answer with reason point is lost (sg-24:8).",
   "wrong_step": {
    "text": "Toward for \\(0<t<1.030\\).",
    "expr": "Interval.open(0, 1.030)"
   },
   "right_step": {
    "text": "Toward for \\(0<t<1.030\\), because \\(x<0\\) and \\(x'>0\\).",
    "expr": "Interval.open(0, 1.030)"
   },
   "relation": "equivalent",
   "possible_reason": null,
   "sources": [
    "BC-ERR-09026"
   ],
   "fix_prompt": false
  },
  {
   "error_id": "BC-ERR-99029",
   "observed_behavior": "Responses invert the quotient for the slope of the path, report a velocity vector where an acceleration vector was asked or reverse its components, compute a one-dimensional arc length or a Pythagorean combination of two separate integrals for total distance, or reason from dy/dx where dy/dt determines the direction of motion.",
   "scoring_consequence": "The setup point for the requested quantity is lost, and the answer point follows it.",
   "wrong_step": {
    "text": "The other component's rate: \\(y'(t)=2-t^2>0\\) for \\(0<t<1.414\\).",
    "expr": "Interval.open(0, 1.414)"
   },
   "right_step": {
    "text": "The rate of the named coordinate: \\(x'>0\\) for \\(0<t<1.030\\).",
    "expr": "Interval.open(0, 1.030)"
   },
   "relation": "distinct",
   "possible_reason": null,
   "sources": [
    "BC-ERR-99029"
   ],
   "fix_prompt": true
  }
 ],
 "representations": null,
 "prerequisite_bridges": [
  {
   "prq_id": "BC-PRQ-08001",
   "text": "Solve the rate equal to 0 on the interval."
  }
 ],
 "time": {
  "exam_part": "I-B",
  "budget_minutes": 2.92,
  "source": "research/exam/exam-structure.md#Section and part layout",
  "written_steps": {
   "ex-1": [
    2,
    4
   ]
  },
  "skipped_steps": {
   "ex-1": [
    1,
    3
   ]
  }
 },
 "checks": [
  {
   "id": "chk-1",
   "check_kind": "completion",
   "format": "short_answer",
   "bands": [
    "low",
    "mid"
   ],
   "archetype_id": "BC-QA-09008",
   "parameter_draw": {
    "offset": 6,
    "amplitude": 2,
    "divisor": 2,
    "end_time": 3,
    "other_turn": 2,
    "shape": "rising",
    "axis": "y-axis",
    "sign_given": "stated",
    "side": "negative"
   },
   "completes": "ex-1",
   "stem": {
    "text": "With \\(x(t)<0\\), \\(x'(t)=2\\cos t-t\\) is positive for \\(t<1.030\\) and negative after. Write the times in \\(0<t<3\\) at which the particle moves toward the y-axis.",
    "command_verb": "write"
   },
   "key": {
    "form": "symbolic",
    "expr": "Interval.open(0, 1.030)"
   },
   "steps": [
    {
     "text": "x' positive while x is negative.",
     "expr": "Interval.open(0, 1.030)",
     "relation": "new"
    }
   ],
   "calculator_status": "calculator",
   "skills": [
    "BC-SKL-09027"
   ]
  },
  {
   "id": "chk-2",
   "check_kind": "isomorph",
   "format": "short_answer",
   "bands": [
    "low",
    "mid"
   ],
   "archetype_id": "BC-QA-09008",
   "parameter_draw": {
    "offset": 8,
    "amplitude": 3,
    "divisor": 2,
    "end_time": 3,
    "other_turn": 1,
    "shape": "rising",
    "axis": "x-axis",
    "sign_given": "stated",
    "side": "positive"
   },
   "stem": {
    "text": "A particle has position \\((t-\\frac{t^3}{3},\\ 8+\\frac{t^2}{2}-3\\sin t)\\) for \\(0\\le t\\le 3\\), and \\(y(t)>0\\). Using a calculator, find all times \\(0<t<3\\) at which it moves toward the x-axis.",
    "command_verb": "find"
   },
   "key": {
    "form": "symbolic",
    "expr": "Interval.open(0, 1.170)"
   },
   "steps": [
    {
     "text": "The y-coordinate.",
     "expr": "t**2/2 - 3*sin(t) + 8",
     "relation": "new"
    },
    {
     "text": "Its rate.",
     "expr": "t - 3*cos(t)",
     "relation": "differentiate",
     "variable": "t"
    },
    {
     "text": "Rate zero.",
     "expr": "1.170120950002626",
     "relation": "solve",
     "variable": "t"
    },
    {
     "text": "Rate negative before it.",
     "expr": "Interval.open(0, 1.170)",
     "relation": "new"
    }
   ],
   "calculator_status": "calculator",
   "skills": [
    "BC-SKL-09027"
   ]
  },
  {
   "id": "chk-3",
   "check_kind": "mcq",
   "format": "mcq",
   "bands": [
    "low"
   ],
   "archetype_id": "BC-QA-09008",
   "parameter_draw": {
    "offset": 6,
    "amplitude": 3,
    "divisor": 2,
    "end_time": 3,
    "other_turn": 3,
    "shape": "falling",
    "axis": "y-axis",
    "sign_given": "stated",
    "side": "negative"
   },
   "stem": {
    "text": "A particle has position \\((\\frac{t^2}{2}-3\\sin t-6,\\ 3t-\\frac{t^3}{3})\\) for \\(0\\le t\\le 3\\), and \\(x(t)<0\\). Using a calculator, find all times \\(0<t<3\\) at which it moves toward the y-axis.",
    "command_verb": "find"
   },
   "key": {
    "form": "symbolic",
    "expr": "Interval.open(1.170, 3)"
   },
   "steps": [
    {
     "text": "The x-coordinate.",
     "expr": "t**2/2 - 3*sin(t) - 6",
     "relation": "new"
    },
    {
     "text": "Its rate.",
     "expr": "t - 3*cos(t)",
     "relation": "differentiate",
     "variable": "t"
    },
    {
     "text": "Rate zero.",
     "expr": "1.170120950002626",
     "relation": "solve",
     "variable": "t"
    },
    {
     "text": "Rate positive after it.",
     "expr": "Interval.open(1.170, 3)",
     "relation": "new"
    }
   ],
   "options": [
    {
     "id": "A",
     "is_key": false,
     "expr": "Interval.open(0, 3)",
     "error_path": "BC-ERR-09025",
     "derivation": "the sign of the coordinate read as the direction, so every time with x negative counted"
    },
    {
     "id": "B",
     "is_key": true,
     "expr": "Interval.open(1.170, 3)",
     "error_path": null
    },
    {
     "id": "C",
     "is_key": false,
     "expr": "Interval.open(0, 1.170)",
     "error_path": "BC-ERR-09025",
     "derivation": "approach read as a negative rate, so the times with x' negative reported"
    },
    {
     "id": "D",
     "is_key": false,
     "expr": "Interval.open(0, 1.732)",
     "error_path": "BC-ERR-99029",
     "derivation": "the other velocity component used, so the times with y' positive reported"
    }
   ],
   "calculator_status": "calculator",
   "skills": [
    "BC-SKL-09027"
   ]
  }
 ],
 "delivery": [
  {
   "block": "orientation",
   "mode": "figure",
   "reason": "rule 4: BC-REP-14 on BC-SKL-09027; not promoted, the orientation states what a response shows and asks for no reading",
   "sources": [
    "BC-SKL-09027"
   ],
   "spec": {
    "kind": "parametric_path",
    "representations": [
     "BC-REP-14"
    ],
    "x": "-t**2/2 + 2*sin(t) - 6",
    "y": "2*t - t**3/3",
    "t_range": [
     0,
     3
    ],
    "marks": [
     {
      "t": 0
     },
     {
      "t": 1.03
     }
    ],
    "labels": [
     {
      "text": "y-axis",
      "placement": "inside"
     },
     {
      "text": "t = 0",
      "placement": "inside"
     },
     {
      "text": "t = 1.03",
      "placement": "inside"
     }
    ]
   },
   "fallback": "the same path static with the y-axis and the two marked points labelled",
   "keyboard": "no control; the figure description is reached with Tab"
  },
  {
   "block": "ki-1",
   "mode": "interactive",
   "reason": "rule 4 promoted: BC-REP-14 on BC-SKL-09027, and BC-QA-09008 `common_givens` name a velocity component and an interval, and the stem asks for a sign argument; one control, the time t",
   "sources": [
    "BC-SKL-09027",
    "BC-QA-09008"
   ],
   "spec": {
    "kind": "parametric_path",
    "representations": [
     "BC-REP-14",
     "BC-REP-04"
    ],
    "x": "-t**2/2 + 2*sin(t) - 6",
    "y": "2*t - t**3/3",
    "t_range": [
     0,
     3
    ],
    "controls": [
     {
      "name": "t",
      "type": "slider",
      "range": [
       0,
       3
      ],
      "step": 0.05
     }
    ],
    "readouts": [
     "sign of x(t)",
     "sign of x'(t)",
     "toward or away from the y-axis"
    ],
    "reading": "Toward or away from the y-axis at this time, and which two signs decide it?",
    "labels": [
     {
      "text": "x(t)",
      "placement": "inside"
     },
     {
      "text": "x'(t)",
      "placement": "inside"
     },
     {
      "text": "toward",
      "placement": "inside"
     },
     {
      "text": "away",
      "placement": "inside"
     }
    ]
   },
   "fallback": "three static frames (t = 0.5, 1.03, 2), each with its two signs and the word toward or away",
   "keyboard": "Left and Right arrows move t by 0.05, Shift with an arrow by 0.5; the readouts are announced on each change"
  },
  {
   "block": "ex-1",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  },
  {
   "block": "ex-2",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  },
  {
   "block": "err-BC-ERR-09025",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  },
  {
   "block": "err-BC-ERR-09026",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  },
  {
   "block": "err-BC-ERR-99029",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  }
 ],
 "refresher": [
  "ki-1",
  "err-BC-ERR-09025",
  "err-BC-ERR-09026",
  "err-BC-ERR-99029",
  "ex-1"
 ],
 "read_minutes": {
  "full": 5.2,
  "brief": 3.0
 },
 "word_count": {
  "full": 773,
  "brief": 449
 },
 "research_lines": [
  {
   "file": "research/units/unit-09-parametric-polar-vector.md",
   "line": "A particle in the first quadrant moves toward the x axis exactly when its y coordinate is positive and its y rate is negative"
  }
 ],
 "inferred": [
  {
   "claim": "A fluent solver writes the rate, its zero and the interval with the sign reason, and holds the sign of the coordinate.",
   "settles": "Timing data per step once the fluency telemetry exists."
  },
  {
   "claim": "ex-1 tags no point type, because the prediction, contrast pair and a reader line of 59 or more words do not fit the brief cap; ex-2 tags BC-PT-99014 and BC-PT-99010.",
   "settles": "A brief cap that admits a second reader line."
  },
  {
   "claim": "Every non-text delivery mode chosen here is a proposal.",
   "settles": "The modality A/B on skip rate and time to first credited success by mode."
  }
 ],
 "sources": [
  "BC-CON-09011",
  "BC-SKL-09027",
  "BC-EK-FUN-8B1",
  "ced:176",
  "BC-QA-09008",
  "BC-PT-99014",
  "BC-PT-99010",
  "BC-ERR-09025",
  "BC-ERR-09026",
  "BC-ERR-99029",
  "BC-MIS-09012",
  "BC-PRQ-08001",
  "sg-24:8",
  "research/units/unit-09-parametric-polar-vector.md#9.6 Solving Motion Problems Using Parametric and Vector-Valued Functions",
  "research/question-analysis/question-archetypes.md#BC-QA-09008 Times at which a particle moves toward a coordinate axis",
  "research/exam/exam-structure.md#Section and part layout"
 ]
}
```
