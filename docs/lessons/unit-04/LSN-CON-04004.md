---
title: LSN-CON-04004 Velocity, speed and direction
research_date: 2026-09-29
status: designed
purpose: Authoring spec for the concept lesson on BC-CON-04004, direction of motion from the sign of velocity and speed as its size, built from authoring_bundle("BC-CON-04004") and the research files it cites, so an author fills plan 15's lesson record without making a teaching decision.
---

# LSN-CON-04004 Velocity, speed and direction

Concept BC-CON-04004 (skills BC-SKL-04008, BC-SKL-04009, BC-SKL-04011), topic 4.2 of Unit 4, loaded by BC-QA-04004, BC-QA-04003 and BC-QA-04010. Its hard parents are BC-CON-04002 and BC-CON-04003 (docs/lessons/unit-04/README.md, section 1).

## Orientation

Served text, from BC-CON-04004 `description_plain` and the Assessment behaviour paragraph (research/units/unit-04-contextual-applications-differentiation.md#4.2 Straight-Line Motion: Connecting Position, Velocity, and Acceleration): direction from the sign of velocity, speed as its size, and intervals of a direction as the part the 2025 report describes (crabbc-25:20). No count, no frequency.

## Key ideas

All three skills map BC-EK-CHA-3B1 (ced:88): one core block, both bands.

- ki-1 (core, BC-EK-CHA-3B1). The Speed and Sign analysis paragraphs of Required mathematical knowledge (crabbc-25:22). No anchor quote: the one CHA-3.B.1 sentence on ced:88 is used by BC-CON-04003, and the block is held under the brief cap.

## Recognition

- BC-QA-04004 (research/question-analysis/question-archetypes.md#BC-QA-04004 Direction of motion and sign analysis over an interval): `typical_wording` "find the intervals of time during which the particles are moving in opposite directions"; `common_givens` a position function for one particle, a velocity function for another, an open time interval; `asked_to_produce` the intervals and a sign analysis over the whole interval. The signal: the word intervals with left, right or opposite directions. Shape: one part of a particle motion FRQ, ordinarily the hardest; no `official_examples` in the record.
- BC-QA-04003 (research/question-analysis/question-archetypes.md#BC-QA-04003 Straight-line motion with velocity, acceleration, and speed), same family: the speed at an instant, BC-SKL-04008.
- BC-QA-04010 (research/question-analysis/question-archetypes.md#BC-QA-04010 Position recovered from velocity with an initial condition): position from velocity, where BC-SKL-04011 meets the constant of integration.

Not this concept: whether the speed is increasing (BC-CON-04005), which needs the acceleration's sign too.

## Method choice

Two strategy blocks, one per archetype family (motion-by-differentiation, whose primary here is BC-QA-04004, and motion-by-accumulation); st-1 both bands, st-2 the low band.

- st-1, BC-QA-04004. Method, `expected_solution_path[0]`: solve the equation velocity equal to zero on the interval. Rival, `wrong_approaches`: sampling integer times (BC-ERR-04010), or reading direction from the sign of the position (BC-ERR-04008). Separating feature: the stem asks for intervals.
- st-2, BC-QA-04010. Method: the known position plus the accumulated change. Rival: the integral reported as the position (BC-ERR-08011).

Both archetypes carry `asked_to_produce` and `common_givens` in the snapshot, so both blocks are verified.

## Solution path

- ex-1, BC-QA-04004, both bands. Draw from `parameter_spec`: double_root 2, single_root 4, size 1, leading positive, horizon 8, direction left, time_units seconds. Position (t - 2)^2 (t - 4), velocity (t - 2)(3t - 10), turning time 10/3, not an integer as the spec's invariant requires. No published BC-QA-04004 item carries this draw.
- Steps follow `expected_solution_path`: position (new), velocity (differentiate), the zeros (solve), the sign on each piece in words (no value), the interval (new). A fluent solver writes steps 2 to 5; the sign on each piece is one line of words, not a chart ({JS}).

## Scoring

BC-QA-04004 lists no `point_types`, so no what_a_reader_scores entry and no point tag, and the served text names no point beyond the error records' scoring_consequence. For the author: the 2025 report ties the two analysis points to covering the whole stated interval (crabbc-25:22), and no drawn sign chart is required or earns a point by itself (research/scoring/justification-requirements.md#Sign analysis of a derivative).

## Traps

Seven active errors meet the skills; the first four in the bundle's order are served: BC-ERR-04007, BC-ERR-04008, BC-ERR-04010, BC-ERR-07026. Low band all four; mid band the first two. All on ex-1's draw.

- err-BC-ERR-04007: speed -1 at t = 3 against |v(3)| = 1. Possible reason from BC-MIS-04005.
- err-BC-ERR-04008: the intervals where x < 0 against where v < 0. No possible reason: neither linked description names the position.
- err-BC-ERR-04010: sampling gives (2, 3) against the solved (2, 10/3). Possible reason from BC-MIS-04017.
- err-BC-ERR-07026: position rebuilt from v without the constant -16 [inferred: the draw does not ask for this]. Possible reason from BC-MIS-07016.

Not served, past the cap of four: BC-ERR-08011, BC-ERR-09021, BC-ERR-99030.

## Representations

None as a separate block. The topic's Representations paragraph names a velocity graph to a sign analysis (BC-REP-02 to BC-REP-04); ki-1's interactive carries it.

## Prerequisite bridge

- BC-PRQ-04005 and BC-PRQ-04009, each from its `description_plain` and `failure_signature`.

## Time

BC-QA-04004 has calculator status either, so the lesson takes Section I Part A, 2.14 minutes per question (research/exam/exam-structure.md#Section and part layout) [inferred: the either status; the shape is an FRQ part with no scored example in the library, docs/lessons/unit-04/README.md, section 5]. The minutes go on solving v(t) = 0 and the words for each piece; the test value arithmetic is held in the head.

## Checks

- chk-1, completion of ex-1, both bands: velocity given, the student solves and reads. Key (2, 10/3).
- chk-2, isomorph, both bands. Draw: double_root 1, single_root 3, size 2, leading negative, horizon 6, direction right, minutes. Key (1, 7/3).
- chk-3, MCQ, low band. Draw: double_root 3, single_root 1, size 1, leading positive, horizon 6, direction left, seconds. Key A (speed 1, left); B carries BC-ERR-04007, C BC-ERR-04008, D BC-ERR-04010. A statement key, so options carry labels.

## Delivery

- orientation: text. Rule 5; the figure-bearing representation is served once, on ki-1.
- ki-1: interactive. Rule 3 promoted: BC-REP-02 on BC-SKL-04009; BC-QA-04004 `difficulty_variables` "whether a zero of the velocity is not an integer" and "whether the velocity changes sign more than once" name what varies, and the stem asks for intervals of a direction (docs/lessons/unit-04/README.md, section 6) [inferred; settled by the modality A/B]. One slider on t, labels inside, fallback the static line with sign intervals, keyboard arrows.
- ex-1 and the four error blocks: step_reveal. Rule 1.

## Band plan

- Low (full): orientation, ki-1, st-1, st-2, ex-1, four error blocks, chk-1 to chk-3, both bridges. 530 words, 3.6 minutes (cap 900 and 6).
- Mid (brief): orientation, ki-1, st-1, ex-1, err-BC-ERR-04007, err-BC-ERR-04008, chk-1, chk-2, both bridges. 340 words, 2.3 minutes (cap 450 and 3).
- Refresher: ki-1, the four error blocks, ex-1.

## Sources

- BC-CON-04004; BC-SKL-04008, BC-SKL-04009, BC-SKL-04011; BC-EK-CHA-3B1; ced:88
- BC-QA-04004, BC-QA-04003, BC-QA-04010; crabbc-25:20, crabbc-25:22, crabbc-25:23
- BC-ERR-04007, BC-ERR-04008, BC-ERR-04010, BC-ERR-07026; BC-MIS-04005, BC-MIS-04017, BC-MIS-07016
- BC-PRQ-04005, BC-PRQ-04009
- research/units/unit-04-contextual-applications-differentiation.md#4.2 Straight-Line Motion: Connecting Position, Velocity, and Acceleration
- research/question-analysis/question-archetypes.md#BC-QA-04004 Direction of motion and sign analysis over an interval
- research/question-analysis/question-archetypes.md#BC-QA-04003 Straight-line motion with velocity, acceleration, and speed
- research/question-analysis/question-archetypes.md#BC-QA-04010 Position recovered from velocity with an initial condition
- research/scoring/justification-requirements.md#Sign analysis of a derivative
- research/exam/exam-structure.md#Section and part layout
- [inferred] The exam part for an either archetype. Settled by a calculator status on BC-QA-04004.
- [inferred] ki-1 as an interactive. Settled by the modality A/B.
- [inferred] BC-ERR-07026 on the direction draw. Settled by a BC-QA-04010 example or a narrower error list.

## Machine record

```json
{
 "id": "LSN-CON-04004",
 "kind": "concept",
 "target_id": "BC-CON-04004",
 "unit": "04",
 "skills": [
  "BC-SKL-04008",
  "BC-SKL-04009",
  "BC-SKL-04011"
 ],
 "orientation": {
  "text": "The sign of velocity gives the direction of motion; speed is its size with the sign removed. For intervals of a direction, a response solves v(t) = 0, reads the sign on each piece, and covers the whole stated interval.",
  "sources": [
   "BC-CON-04004",
   "research/units/unit-04-contextual-applications-differentiation.md#4.2 Straight-Line Motion: Connecting Position, Velocity, and Acceleration"
  ]
 },
 "key_ideas": [
  {
   "id": "ki-1",
   "ek_id": "BC-EK-CHA-3B1",
   "depth": "core",
   "text": "Velocity positive: moving right; negative: moving left; zero: at rest. Speed is \\(|v(t)|\\), never negative. The zeros of \\(v\\) split the interval and the sign is constant between consecutive zeros, so the conclusion rests on solved zeros, not sampled inputs (crabbc-25:22).",
   "notation": "speed equals the absolute value of v of t",
   "quote": null,
   "sources": [
    "BC-EK-CHA-3B1",
    "ced:88",
    "crabbc-25:22",
    "research/units/unit-04-contextual-applications-differentiation.md#4.2 Straight-Line Motion: Connecting Position, Velocity, and Acceleration"
   ]
  }
 ],
 "strategy": [
  {
   "id": "st-1",
   "archetype_id": "BC-QA-04004",
   "cue": "A position or velocity function and an open time interval; the stem asks during which intervals the particle moves a stated way.",
   "method": "First line: \\(v(t)=0\\), solved on the interval.",
   "rival": "Rival: integer times sampled (BC-ERR-04010), or direction read from the position (BC-ERR-04008).",
   "separating_feature": "The word interval: only solved zeros can bound it.",
   "sources": [
    "BC-QA-04004"
   ],
   "evidence_tag": "verified"
  },
  {
   "id": "st-2",
   "archetype_id": "BC-QA-04010",
   "cue": "Velocity and the position at one time given; position at another time asked.",
   "method": "First line: position equals the known position plus the integral of velocity.",
   "rival": "Rival: the integral reported as the position (BC-ERR-08011).",
   "separating_feature": "A known position is supplied beside the velocity.",
   "sources": [
    "BC-QA-04010"
   ],
   "evidence_tag": "verified"
  }
 ],
 "worked_examples": [
  {
   "id": "ex-1",
   "archetype_id": "BC-QA-04004",
   "bands": [
    "low",
    "mid"
   ],
   "parameter_draw": {
    "double_root": 2,
    "single_root": 4,
    "size": 1,
    "leading": "positive",
    "horizon": 8,
    "direction": "left",
    "time_units": "seconds"
   },
   "problem": {
    "text": "A particle's position is \\(x(t)=(t-2)^2(t-4)\\) for \\(0<t<8\\) seconds. Find every interval on which the particle moves left.",
    "command_verb": "find"
   },
   "calculator_status": "no_calculator",
   "steps": [
    {
     "cue": "Direction asked: velocity decides.",
     "why": "Position is given.",
     "expr": "(t - 2)**2*(t - 4)",
     "relation": "new"
    },
    {
     "cue": "Differentiate position.",
     "why": "\\(v(t)=(t-2)(3t-10)\\).",
     "expr": "(t - 2)*(3*t - 10)",
     "relation": "differentiate",
     "variable": "t"
    },
    {
     "cue": "Interval asked: solve \\(v(t)=0\\).",
     "why": "\\(10/3\\) is not an integer.",
     "expr": "FiniteSet(2, 10/3)",
     "relation": "solve",
     "variable": "t"
    },
    {
     "cue": "Sign on each piece.",
     "why": "\\(v>0\\) on \\((0,2)\\), \\(v<0\\) on \\((2,10/3)\\), \\(v>0\\) on \\((10/3,8)\\)."
    },
    {
     "cue": "Left means \\(v<0\\).",
     "why": "Stated in words for the whole interval.",
     "expr": "Interval.open(2, 10/3)",
     "relation": "new"
    }
   ],
   "answer": {
    "form": "symbolic",
    "expr": "Interval.open(2, 10/3)"
   }
  }
 ],
 "what_a_reader_scores": [],
 "common_errors": [
  {
   "error_id": "BC-ERR-04007",
   "wrong_step": {
    "text": "Speed at \\(t=3\\) is \\(-1\\).",
    "expr": "-1"
   },
   "right_step": {
    "text": "Speed is \\(|v(3)|=1\\).",
    "expr": "Abs(-1)"
   },
   "relation": "distinct",
   "possible_reason": {
    "misconception_id": "BC-MIS-04005",
    "text": "reported as part of a speed"
   },
   "sources": [
    "BC-ERR-04007",
    "BC-MIS-04005"
   ],
   "observed_behavior": "A negative number is reported as the speed of the particle.",
   "scoring_consequence": "The answer point is lost."
  },
  {
   "error_id": "BC-ERR-04008",
   "wrong_step": {
    "text": "Left where \\(x(t)<0\\).",
    "expr": "Union(Interval.open(0, 2), Interval.open(2, 4))"
   },
   "right_step": {
    "text": "Left where \\(v(t)<0\\).",
    "expr": "Interval.open(2, 10/3)"
   },
   "relation": "distinct",
   "possible_reason": null,
   "sources": [
    "BC-ERR-04008"
   ],
   "observed_behavior": "The response argues the direction of travel from whether the position is positive or negative.",
   "scoring_consequence": "The reasoning point is lost; the 2022 Chief Reader report records responses arguing from the wrong function in a related part (cr-22:20)."
  },
  {
   "error_id": "BC-ERR-04010",
   "wrong_step": {
    "text": "Integers sampled: left on \\((2,3)\\).",
    "expr": "Interval.open(2, 3)"
   },
   "right_step": {
    "text": "Zeros solved: left on \\((2,10/3)\\).",
    "expr": "Interval.open(2, 10/3)"
   },
   "relation": "distinct",
   "possible_reason": {
    "misconception_id": "BC-MIS-04017",
    "text": "zeros between samples are missed"
   },
   "sources": [
    "BC-ERR-04010",
    "BC-MIS-04017"
   ],
   "observed_behavior": "Integer times are substituted into the velocity in place of solving the equation velocity equal to zero, so a non-integer zero is missed.",
   "scoring_consequence": "The 2025 Chief Reader report records this behaviour directly and links it to the loss of the two analysis points, whose mean scores were 0.04 and 0.03 (crabbc-25:20, crabbc-25:22)."
  },
  {
   "error_id": "BC-ERR-07026",
   "wrong_step": {
    "text": "Position rebuilt from \\(v\\) with no constant.",
    "expr": "t**3 - 8*t**2 + 20*t"
   },
   "right_step": {
    "text": "With \\(x(0)=-16\\) as the constant.",
    "expr": "(t - 2)**2*(t - 4)"
   },
   "relation": "distinct",
   "possible_reason": {
    "misconception_id": "BC-MIS-07016",
    "text": "antidifferentiates without a constant"
   },
   "sources": [
    "BC-ERR-07026",
    "BC-MIS-07016"
   ],
   "observed_behavior": "The antiderivative equation is written with no constant.",
   "scoring_consequence": "At most the first two points are available; the guideline caps the response there."
  }
 ],
 "representations": null,
 "prerequisite_bridges": [
  {
   "prq_id": "BC-PRQ-04005",
   "text": "Absolute value is size without sign; speed uses it, direction does not. The failure: a negative speed, or a direction answered with a size."
  },
  {
   "prq_id": "BC-PRQ-04009",
   "text": "Solve for the zeros, split the interval there, and find the sign on each piece. The failure: intervals reported from sampled integers."
  }
 ],
 "time": {
  "exam_part": "I-A",
  "budget_minutes": 2.14,
  "source": "research/exam/exam-structure.md#Section and part layout",
  "written_steps": {
   "ex-1": [
    2,
    3,
    4,
    5
   ]
  },
  "skipped_steps": {
   "ex-1": [
    1
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
   "archetype_id": "BC-QA-04004",
   "parameter_draw": {
    "double_root": 2,
    "single_root": 4,
    "size": 1,
    "leading": "positive",
    "horizon": 8,
    "direction": "left",
    "time_units": "seconds"
   },
   "completes": "ex-1",
   "stem": {
    "text": "\\(v(t)=(t-2)(3t-10)\\) on \\(0<t<8\\). From its zeros, find where the particle moves left.",
    "command_verb": "find"
   },
   "key": {
    "form": "symbolic",
    "expr": "Interval.open(2, 10/3)"
   },
   "steps": [
    {
     "text": "v(t).",
     "expr": "(t - 2)*(3*t - 10)",
     "relation": "new"
    },
    {
     "text": "Zeros.",
     "expr": "FiniteSet(2, 10/3)",
     "relation": "solve",
     "variable": "t"
    },
    {
     "text": "v < 0 between them.",
     "expr": "Interval.open(2, 10/3)",
     "relation": "new"
    }
   ],
   "calculator_status": "no_calculator",
   "skills": [
    "BC-SKL-04009",
    "BC-SKL-04011"
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
   "archetype_id": "BC-QA-04004",
   "parameter_draw": {
    "double_root": 1,
    "single_root": 3,
    "size": 2,
    "leading": "negative",
    "horizon": 6,
    "direction": "right",
    "time_units": "minutes"
   },
   "stem": {
    "text": "\\(x(t)=-2(t-1)^2(t-3)\\) for \\(0<t<6\\) minutes. Find where the particle moves right.",
    "command_verb": "find"
   },
   "key": {
    "form": "symbolic",
    "expr": "Interval.open(1, 7/3)"
   },
   "steps": [
    {
     "text": "Position.",
     "expr": "-2*(t - 1)**2*(t - 3)",
     "relation": "new"
    },
    {
     "text": "Velocity.",
     "expr": "-2*(t - 1)*(3*t - 7)",
     "relation": "differentiate",
     "variable": "t"
    },
    {
     "text": "Zeros.",
     "expr": "FiniteSet(1, 7/3)",
     "relation": "solve",
     "variable": "t"
    },
    {
     "text": "v > 0 between them.",
     "expr": "Interval.open(1, 7/3)",
     "relation": "new"
    }
   ],
   "calculator_status": "no_calculator",
   "skills": [
    "BC-SKL-04009",
    "BC-SKL-04011"
   ]
  },
  {
   "id": "chk-3",
   "check_kind": "mcq",
   "format": "mcq",
   "bands": [
    "low"
   ],
   "archetype_id": "BC-QA-04004",
   "parameter_draw": {
    "double_root": 3,
    "single_root": 1,
    "size": 1,
    "leading": "positive",
    "horizon": 6,
    "direction": "left",
    "time_units": "seconds"
   },
   "stem": {
    "text": "\\(x(t)=(t-3)^2(t-1)\\), so \\(v(t)=(t-3)(3t-5)\\). Which statement about \\(t=2\\) is correct?",
    "command_verb": "identify"
   },
   "key": {
    "form": "statement",
    "expr": "-1",
    "text": "A"
   },
   "steps": [
    {
     "text": "v(t).",
     "expr": "(t - 3)*(3*t - 5)",
     "relation": "new"
    },
    {
     "text": "v(2) = -1.",
     "expr": "-1",
     "relation": "evaluate",
     "subs": {
      "t": "2"
     }
    }
   ],
   "options": [
    {
     "id": "A",
     "is_key": true,
     "label": "Speed 1; moving left, since v(2) = -1 < 0.",
     "error_path": null
    },
    {
     "id": "B",
     "is_key": false,
     "label": "Speed -1; moving left.",
     "error_path": "BC-ERR-04007",
     "derivation": "the signed velocity reported as the speed"
    },
    {
     "id": "C",
     "is_key": false,
     "label": "Speed 1; moving right, since x(2) = 1 > 0.",
     "error_path": "BC-ERR-04008",
     "derivation": "direction read from the sign of the position"
    },
    {
     "id": "D",
     "is_key": false,
     "label": "Moving left on all of (1, 3), since v(2) < 0.",
     "error_path": "BC-ERR-04010",
     "derivation": "one sampled time taken to settle the sign on the interval, missing the zero at 5/3"
    }
   ],
   "calculator_status": "no_calculator",
   "skills": [
    "BC-SKL-04008",
    "BC-SKL-04009"
   ]
  }
 ],
 "delivery": [
  {
   "block": "orientation",
   "mode": "text",
   "reason": "rule 5 for a statement of what a response shows; the figure-bearing BC-REP-02 is served once, on ki-1",
   "sources": [
    "BC-SKL-04009"
   ]
  },
  {
   "block": "ki-1",
   "mode": "interactive",
   "reason": "rule 3 promoted: BC-REP-02 in BC-SKL-04009 representations; BC-QA-04004 difficulty_variables name a non-integer zero and more than one sign change, and the stem asks for intervals of a direction",
   "sources": [
    "BC-SKL-04009",
    "BC-QA-04004"
   ],
   "spec": {
    "kind": "particle_on_line",
    "representations": [
     "BC-REP-02",
     "BC-REP-01"
    ],
    "position": "(t - 2)^2 (t - 4)",
    "velocity": "(t - 2)(3t - 10)",
    "window": {
     "t": [
      0,
      8
     ],
     "x": [
      -2,
      25
     ]
    },
    "controls": [
     {
      "type": "slider",
      "variable": "t",
      "range": [
       0,
       8
      ],
      "step": 0.1,
      "start": 1
     }
    ],
    "drawn": [
     "the particle as a point on a horizontal line at x(t)",
     "an arrow showing the direction of v(t)",
     "the value of v(t) at the slider"
    ],
    "labels": [
     {
      "text": "v(t) > 0: moving right",
      "placement": "inside"
     },
     {
      "text": "v(t) < 0: moving left",
      "placement": "inside"
     },
     {
      "text": "v = 0 at t = 2 and t = 10/3",
      "placement": "inside"
     },
     {
      "text": "speed = |v(t)|",
      "placement": "inside"
     }
    ],
    "question": "On which intervals of 0 < t < 8 is the particle moving left?"
   },
   "fallback": "the static line with the sign intervals of v labelled inside: right on (0, 2), left on (2, 10/3), right on (10/3, 8)",
   "keyboard": "Tab focuses the slider; left and right arrow keys step t by 0.1; Enter reads out v(t) and the direction"
  },
  {
   "block": "ex-1",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  },
  {
   "block": "err-BC-ERR-04007",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  },
  {
   "block": "err-BC-ERR-04008",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  },
  {
   "block": "err-BC-ERR-04010",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  },
  {
   "block": "err-BC-ERR-07026",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  }
 ],
 "refresher": [
  "ki-1",
  "err-BC-ERR-04007",
  "err-BC-ERR-04008",
  "err-BC-ERR-04010",
  "err-BC-ERR-07026",
  "ex-1"
 ],
 "research_lines": [
  {
   "file": "research/scoring/justification-requirements.md",
   "line": "Nothing in the corpus read requires a drawn sign chart, and nothing in it awards a point for one."
  }
 ],
 "inferred": [
  {
   "claim": "BC-QA-04004 is calculator status either, so the lesson times it as Section I Part A at 2.14 minutes, although its multipart structure is one part of a particle motion FRQ.",
   "settles": "A calculator status of calculator or no_calculator on BC-QA-04004."
  },
  {
   "claim": "ki-1 is served as an interactive slider on t rather than a static figure.",
   "settles": "The modality A/B in the build plan: skip rate and time to first credited success by mode."
  },
  {
   "claim": "BC-ERR-07026 is shown on ex-1's draw as position rebuilt from its velocity, a use the draw does not ask for.",
   "settles": "An error list for BC-SKL-04011 limited to direction and rest, or a BC-QA-04010 worked example in this lesson."
  }
 ],
 "sources": [
  "BC-CON-04004",
  "BC-SKL-04008",
  "BC-SKL-04009",
  "BC-SKL-04011",
  "BC-EK-CHA-3B1",
  "ced:88",
  "crabbc-25:20",
  "crabbc-25:22",
  "crabbc-25:23",
  "BC-QA-04004",
  "BC-QA-04003",
  "BC-QA-04010",
  "BC-ERR-04007",
  "BC-ERR-04008",
  "BC-ERR-04010",
  "BC-ERR-07026",
  "BC-MIS-04005",
  "BC-MIS-04017",
  "BC-MIS-07016",
  "BC-PRQ-04005",
  "BC-PRQ-04009",
  "research/units/unit-04-contextual-applications-differentiation.md#4.2 Straight-Line Motion: Connecting Position, Velocity, and Acceleration",
  "research/question-analysis/question-archetypes.md#BC-QA-04004 Direction of motion and sign analysis over an interval",
  "research/question-analysis/question-archetypes.md#BC-QA-04003 Straight-line motion with velocity, acceleration, and speed",
  "research/question-analysis/question-archetypes.md#BC-QA-04010 Position recovered from velocity with an initial condition",
  "research/scoring/justification-requirements.md#Sign analysis of a derivative",
  "research/exam/exam-structure.md#Section and part layout"
 ],
 "word_count": {
  "full": 530,
  "brief": 340
 },
 "read_minutes": {
  "full": 3.6,
  "brief": 2.3
 }
}
```
