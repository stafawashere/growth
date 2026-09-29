---
title: LSN-CON-04003 Position, velocity and acceleration
research_date: 2026-09-29
status: designed
purpose: Authoring spec for the concept lesson on BC-CON-04003, velocity and acceleration as successive derivatives of position, built from authoring_bundle("BC-CON-04003") and the research files it cites, so an author fills plan 15's lesson record without making a teaching decision.
---

# LSN-CON-04003 Position, velocity and acceleration

Concept BC-CON-04003 (skills BC-SKL-04006, BC-SKL-04007), topic 4.2 of Unit 4, loaded by BC-QA-04003 (motion-by-differentiation) and BC-QA-04010 (motion-by-accumulation). It has no in-unit hard parent and opens the motion chain that BC-CON-04004 and BC-CON-04005 continue (docs/lessons/unit-04/README.md, section 3).

## Prediction

Both bands, served first. Form `mcq`, three options, on ex-1's own function \(x(t)=t^3-3t^2-4t+2\). The student picks which function gives the acceleration: the position itself, its first derivative or its second. Key: the second derivative. The resolution states the chain (velocity is the derivative of position, acceleration the derivative of velocity) and never grades the choice. Sources: BC-CON-04003 and the 4.2 topic section that ki-1 cites (BC-EK-CHA-3B1, ced:88). Delivery: text. [inferred] Settled by the prediction's first-try rate in the build plan.

## Orientation

Served text, from BC-CON-04003 `description_plain` and the Assessment behaviour paragraph (research/units/unit-04-contextual-applications-differentiation.md#4.2 Straight-Line Motion: Connecting Position, Velocity, and Acceleration), which lists velocity or acceleration at an instant as the opening parts of the particle motion question (crabbc-25:20). Cut to 20 words to fit the brief cap. No count, no frequency.

## Key ideas

Both skills map BC-EK-CHA-3B1 (ced:88): one core block, both bands.

- ki-1 (core, BC-EK-CHA-3B1). The Position, velocity, acceleration paragraph of Required mathematical knowledge, turned into a count of derivatives from the given letter to the requested one. Anchor quote from ced:88.

## Recognition

- BC-QA-04003 (research/question-analysis/question-archetypes.md#BC-QA-04003 Straight-line motion with velocity, acceleration, and speed): `typical_wording` "find the velocity of the particle at the stated time"; `common_givens` a position or a velocity function of time; `asked_to_produce` the velocity, the acceleration. The signal: a function named x, s or v of t, and a request for another of the three at a number. Shapes: two or three parts of a particle motion FRQ (BC-FRQ-2014-Q4-A, BC-FRQ-2015-Q3-C, no calculator) and an MCQ (BC-MCQ-CED-012).
- BC-QA-04010 (research/question-analysis/question-archetypes.md#BC-QA-04010 Position recovered from velocity with an initial condition), the other family: velocity and a known position given, position asked. The signal is a position at one time supplied beside the velocity.

Not this concept: speed or direction (BC-CON-04004), whether the speed is increasing (BC-CON-04005).
The contrast pair on st-1 sets a velocity given and an acceleration asked beside a velocity given with a known position and a position asked. Where the near miss comes from: the sibling family BC-QA-04010, whose position-from-velocity stem shares the function of time and the instant but runs the chain backward. The separating feature is the position at one time given beside a velocity (BC-QA-04010 `common_givens`); a position function alone, as in BC-QA-04003 `common_givens`, is differentiated.

## Method choice

Two strategy blocks, one per archetype family; st-1 both bands, st-2 the low band. The reader prints its own labels, so no field starts with one, and the error ids sit in `sources`.

- st-1, BC-QA-04003. Method, `expected_solution_path[0]`: differentiate the supplied function as many times as the question needs. Rival, `wrong_approaches`: the wrong number of differentiations (BC-ERR-04006). Separating feature: the given letter against the requested letter. Carries the contrast pair.
- st-2, BC-QA-04010. Method: position as the initial position plus the accumulated change. Rival: the integral reported as the position (BC-ERR-08011). Separating feature: the direction of the chain.

Both archetypes carry `asked_to_produce` and `common_givens` in the snapshot, so both blocks are verified.

## Solution path

- ex-1, BC-QA-04003, both bands, no calculator. Draw: cubic 1, quadratic -3, free 2, speed_value 4, instant 2, given position, heading left. Derived: linear -4, constant 2, so x(t) = t^3 - 3t^2 - 4t + 2, v(2) = -4, a(2) = 6, misread velocity x(2) = -10. No published BC-QA-04003 item carries this draw.
- Steps: position (new), velocity (differentiate), v(2) (evaluate, BC-PT-99004), acceleration (new), a(2) (evaluate, BC-PT-99027), both values (new). A fluent solver writes steps 2 to 5 and skips the restated position and the final pairing.
One example, so it is not faded and carries no `fade_from`.

## Scoring

BC-QA-04003 lists BC-PT-99021, BC-PT-99027 and BC-PT-99004. ex-1 tags BC-PT-99004 on v(2) and BC-PT-99027 on a(2); the lines are reader_checks(["BC-PT-99004", "BC-PT-99027"]) copied exactly.

For the author: the speed conclusion that follows these parts is scored only when the sign of the velocity is stated and applied to the particle (crabbc-25:22), which BC-CON-04005 carries. Answer point losses are listed under research/scoring/common-point-losses.md#Answer points.

## Traps

One active error meets the skills: BC-ERR-04006 (linked BC-MIS-04004, severity medium, and BC-MIS-04001). Both bands.

- err-BC-ERR-04006: x(2) = -10 reported as the velocity, against v(2) = -4. Possible reason in words from BC-MIS-04004. Distinct, so `fix_prompt` true. Every value is an integer, so the decimal rule changes no expression.

## Representations

None. The topic's Representations paragraph names BC-REP-02 to BC-REP-04 for a velocity graph, which belongs to the sign analysis of BC-CON-04004; this concept's skills carry BC-REP-01 and BC-REP-05 only.

## Prerequisite bridge

- BC-PRQ-04008, from its `description_plain` and `failure_signature`.

## Time

BC-QA-04003 has calculator status either, so the lesson takes Section I Part A, 2.14 minutes per question (research/exam/exam-structure.md#Section and part layout) [inferred: the either status]. As FRQ parts it takes 1.67 to 3.33 minutes of a 15.0 minute question (docs/lessons/unit-04/README.md, section 5). The minutes go on two derivatives and two evaluations; the polynomial differentiation is fast.

## Checks

- chk-1, completion of ex-1, both bands: both derivatives given, the student evaluates. Key {v = -4, a = 6}.
- chk-2, isomorph, both bands. Draw: cubic -1, quadratic 2, free 3, speed_value 5, instant 1, given velocity, heading left; v(t) = -t^3 + 2t^2 + 3t - 9. Key a(1) = 4.
- No chk-3: one error in the bundle, fewer than the three error paths an MCQ needs (inferred array).

## Delivery

- pr-1: text. Rule 6, a prediction on ex-1's function with no picture in the question.
- orientation, ki-1: text. Rule 6: BC-REP-01 and BC-REP-05 only (docs/lessons/unit-04/README.md, section 6).
- ex-1, err-BC-ERR-04006: step_reveal. Rule 1.

Figure presence: no drawn block. No rule of 2 to 5 applies, because both skills carry BC-REP-01 and BC-REP-05 and the key idea describes no process, so the record carries `no_figure_reason`.

## Band plan

- Low (full): prediction, orientation, bridge, ki-1, st-1 with its contrast, st-2, ex-1 with its scoring lines, chk-1, the error block, chk-2. 475 words, 3.2 minutes (cap 900 and 6).
- Mid (brief): prediction, orientation, bridge, ki-1, st-1 with its contrast, ex-1 with its scoring lines, chk-1, the error block, chk-2. 428 words, 2.9 minutes (cap 450 and 3). The orientation, the st-1 fields and the bridge were shortened to fit.
- Refresher: ki-1, err-BC-ERR-04006, ex-1.

## Sources

- BC-CON-04003; BC-SKL-04006, BC-SKL-04007; BC-EK-CHA-3B1; ced:88
- BC-QA-04003, BC-QA-04010; BC-PT-99004, BC-PT-99027; crabbc-25:20, crabbc-25:22, cr-22:20
- BC-ERR-04006; BC-MIS-04004; BC-PRQ-04008
- research/units/unit-04-contextual-applications-differentiation.md#4.2 Straight-Line Motion: Connecting Position, Velocity, and Acceleration
- research/question-analysis/question-archetypes.md#BC-QA-04003 Straight-line motion with velocity, acceleration, and speed
- research/question-analysis/question-archetypes.md#BC-QA-04010 Position recovered from velocity with an initial condition
- research/scoring/common-point-losses.md#Answer points
- research/exam/exam-structure.md#Section and part layout
- [inferred] The exam part for an either archetype. Settled by a calculator status on BC-QA-04003.
- [inferred] Two checks only. Settled by more errors linked to the concept's skills.

## Machine record

```json
{
 "id": "LSN-CON-04003",
 "kind": "concept",
 "target_id": "BC-CON-04003",
 "unit": "04",
 "skills": [
  "BC-SKL-04006",
  "BC-SKL-04007"
 ],
 "prediction": {
  "id": "pr-1",
  "stem": {
   "text": "Predict which function gives the particle's acceleration, for position \\(x(t)=t^3-3t^2-4t+2\\).",
   "command_verb": "predict"
  },
  "format": "mcq",
  "options": [
   {
    "id": "A",
    "label": "\\(x(t)\\) itself",
    "is_key": false
   },
   {
    "id": "B",
    "label": "\\(x'(t)\\), the first derivative",
    "is_key": false
   },
   {
    "id": "C",
    "label": "\\(x''(t)\\), the second derivative",
    "is_key": true
   }
  ],
  "resolution": "Velocity is the derivative of position and acceleration the derivative of velocity, so \\(a(t)=x''(t)=6t-6\\).",
  "sources": [
   "BC-CON-04003",
   "BC-EK-CHA-3B1",
   "ced:88",
   "research/units/unit-04-contextual-applications-differentiation.md#4.2 Straight-Line Motion: Connecting Position, Velocity, and Acceleration"
  ]
 },
 "no_figure_reason": "The two skills carry BC-REP-01 and BC-REP-05 only, a symbolic rule and a sentence, and the key idea describes no process. The velocity graph belongs to BC-CON-04004.",
 "orientation": {
  "text": "Velocity is the derivative of position, acceleration the derivative of velocity. A response differentiates as often as the request needs.",
  "sources": [
   "BC-CON-04003",
   "research/units/unit-04-contextual-applications-differentiation.md#4.2 Straight-Line Motion: Connecting Position, Velocity, and Acceleration"
  ]
 },
 "key_ideas": [
  {
   "id": "ki-1",
   "ek_id": "BC-EK-CHA-3B1",
   "depth": "core",
   "text": "For a particle on a line, \\(v(t)=x'(t)\\) and \\(a(t)=v'(t)=x''(t)\\). Count the steps from the given function to the requested one: position to velocity is one derivative, position to acceleration two, velocity to acceleration one.",
   "notation": "x of t, v of t, a of t",
   "quote": {
    "text": "The derivative can be used to solve rectilinear motion problems involving position, speed, velocity, and acceleration.",
    "source": "ced:88"
   },
   "sources": [
    "BC-EK-CHA-3B1",
    "ced:88",
    "research/units/unit-04-contextual-applications-differentiation.md#4.2 Straight-Line Motion: Connecting Position, Velocity, and Acceleration"
   ]
  }
 ],
 "strategy": [
  {
   "id": "st-1",
   "archetype_id": "BC-QA-04003",
   "cue": "A function of time; velocity or acceleration asked.",
   "method": "\\(v(t)=\\) or \\(a(t)=\\), the derivative the request needs.",
   "rival": "The wrong number of derivatives.",
   "separating_feature": "Given letter against requested letter.",
   "sources": [
    "BC-QA-04003",
    "BC-ERR-04006"
   ],
   "evidence_tag": "verified",
   "contrast": {
    "this": {
     "text": "A particle's velocity is \\(v(t)=t^2-5t\\). Find its acceleration at \\(t=4\\).",
     "archetype_id": "BC-QA-04003"
    },
    "not_this": {
     "text": "\\(v(t)=t^2-5t\\) and \\(x(0)=3\\). Find the position at \\(t=4\\).",
     "why_not": "Position from velocity is an integral."
    },
    "feature": "A velocity plus the position at one time means accumulate."
   }
  },
  {
   "id": "st-2",
   "archetype_id": "BC-QA-04010",
   "cue": "A velocity function and the position at one time are given; the stem asks for the position at another time.",
   "method": "Position equals the known position plus the integral of velocity.",
   "rival": "The integral reported without the known position.",
   "separating_feature": "Going from velocity back to position runs the chain backward.",
   "sources": [
    "BC-QA-04010",
    "BC-ERR-08011"
   ],
   "evidence_tag": "verified"
  }
 ],
 "worked_examples": [
  {
   "id": "ex-1",
   "archetype_id": "BC-QA-04003",
   "bands": [
    "low",
    "mid"
   ],
   "parameter_draw": {
    "cubic": 1,
    "quadratic": -3,
    "free": 2,
    "speed_value": 4,
    "instant": 2,
    "given": "position",
    "heading": "left"
   },
   "problem": {
    "text": "A particle's position is \\(x(t)=t^3-3t^2-4t+2\\). Find its velocity and its acceleration at \\(t=2\\).",
    "command_verb": "find"
   },
   "calculator_status": "no_calculator",
   "steps": [
    {
     "cue": "The given function is position.",
     "why": "Velocity is one derivative away.",
     "expr": "t**3 - 3*t**2 - 4*t + 2",
     "relation": "new"
    },
    {
     "cue": "Velocity requested.",
     "why": "\\(v(t)=x'(t)\\).",
     "expr": "3*t**2 - 6*t - 4",
     "relation": "differentiate",
     "variable": "t"
    },
    {
     "cue": "At \\(t=2\\).",
     "why": "\\(12-12-4\\).",
     "expr": "-4",
     "relation": "evaluate",
     "subs": {
      "t": "2"
     },
     "point_type_id": "BC-PT-99004"
    },
    {
     "cue": "Acceleration: differentiate velocity.",
     "why": "\\(a(t)=v'(t)\\).",
     "expr": "6*t - 6",
     "relation": "new"
    },
    {
     "cue": "At \\(t=2\\).",
     "why": "\\(12-6\\).",
     "expr": "6",
     "relation": "evaluate",
     "subs": {
      "t": "2"
     },
     "point_type_id": "BC-PT-99027"
    },
    {
     "cue": "Both values requested.",
     "why": "Each labelled.",
     "expr": "FiniteSet(Eq(v, -4), Eq(a, 6))",
     "relation": "new"
    }
   ],
   "answer": {
    "form": "symbolic",
    "expr": "FiniteSet(Eq(v, -4), Eq(a, 6))"
   }
  }
 ],
 "what_a_reader_scores": [
  {
   "example_id": "ex-1",
   "point_type_ids": [
    "BC-PT-99004",
    "BC-PT-99027"
   ],
   "lines": [
    {
     "point_type_id": "BC-PT-99004",
     "text": "Answer with or without supporting work. Earned by: The correct value on its own, with no supporting work required (sg-25:3, sg-26:4). Not earned by: A value outside the accepted precision, or a value inconsistent with a required earlier step where the rubric imposes one. Precision: A reported decimal answer must be accurate to three places after the decimal point, rounded or truncated; at most one point per question is lost to inappropriate rounding (sg-25:2, sg-26:2). sg-26:4 also accepts a stated rounding to the nearest integer and several truncations."
    },
    {
     "point_type_id": "BC-PT-99027",
     "text": "Higher derivative expression evaluated at a point. Earned by: A correct expression for the second or higher derivative, evaluated at the requested point, consistent with the earlier derivative work (sg-25:20, sg-23:10). Not earned by: An expression left in terms of the first derivative where the prompt asked for it in terms of the dependent variable (sg-23:11)."
    }
   ]
  }
 ],
 "common_errors": [
  {
   "error_id": "BC-ERR-04006",
   "wrong_step": {
    "text": "\\(x(2)=-10\\) reported as velocity.",
    "expr": "-10"
   },
   "right_step": {
    "text": "\\(v(2)=x'(2)=-4\\).",
    "expr": "-4"
   },
   "relation": "distinct",
   "possible_reason": {
    "misconception_id": "BC-MIS-04004",
    "text": "which one to differentiate is decided by guesswork"
   },
   "sources": [
    "BC-ERR-04006",
    "BC-MIS-04004"
   ],
   "observed_behavior": "Acceleration is reported where velocity was asked for, or position where velocity was asked for.",
   "scoring_consequence": "The answer point is lost although each differentiation performed is correct.",
   "fix_prompt": true
  }
 ],
 "representations": null,
 "prerequisite_bridges": [
  {
   "prq_id": "BC-PRQ-04008",
   "text": "Name each quantity and its unit; here, which letter is position and which velocity."
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
    1,
    6
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
   "archetype_id": "BC-QA-04003",
   "parameter_draw": {
    "cubic": 1,
    "quadratic": -3,
    "free": 2,
    "speed_value": 4,
    "instant": 2,
    "given": "position",
    "heading": "left"
   },
   "completes": "ex-1",
   "stem": {
    "text": "\\(v(t)=3t^2-6t-4\\) and \\(a(t)=6t-6\\). Give \\(v(2)\\) and \\(a(2)\\).",
    "command_verb": "give"
   },
   "key": {
    "form": "symbolic",
    "expr": "FiniteSet(Eq(v, -4), Eq(a, 6))"
   },
   "steps": [
    {
     "text": "v(t).",
     "expr": "3*t**2 - 6*t - 4",
     "relation": "new"
    },
    {
     "text": "v(2).",
     "expr": "-4",
     "relation": "evaluate",
     "subs": {
      "t": "2"
     }
    },
    {
     "text": "a(t).",
     "expr": "6*t - 6",
     "relation": "new"
    },
    {
     "text": "a(2).",
     "expr": "6",
     "relation": "evaluate",
     "subs": {
      "t": "2"
     }
    },
    {
     "text": "Both.",
     "expr": "FiniteSet(Eq(v, -4), Eq(a, 6))",
     "relation": "new"
    }
   ],
   "calculator_status": "no_calculator",
   "skills": [
    "BC-SKL-04006",
    "BC-SKL-04007"
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
   "archetype_id": "BC-QA-04003",
   "parameter_draw": {
    "cubic": -1,
    "quadratic": 2,
    "free": 3,
    "speed_value": 5,
    "instant": 1,
    "given": "velocity",
    "heading": "left"
   },
   "stem": {
    "text": "A particle's velocity is \\(v(t)=-t^3+2t^2+3t-9\\). Find its acceleration at \\(t=1\\).",
    "command_verb": "find"
   },
   "key": {
    "form": "numeric",
    "expr": "4"
   },
   "steps": [
    {
     "text": "Velocity given.",
     "expr": "-t**3 + 2*t**2 + 3*t - 9",
     "relation": "new"
    },
    {
     "text": "One derivative.",
     "expr": "-3*t**2 + 4*t + 3",
     "relation": "differentiate",
     "variable": "t"
    },
    {
     "text": "At t = 1.",
     "expr": "4",
     "relation": "evaluate",
     "subs": {
      "t": "1"
     }
    }
   ],
   "calculator_status": "no_calculator",
   "skills": [
    "BC-SKL-04007"
   ]
  }
 ],
 "delivery": [
  {
   "block": "pr-1",
   "mode": "text",
   "reason": "rule 6: a prediction on ex-1's function with no picture in the question",
   "sources": [
    "BC-SKL-04006"
   ]
  },
  {
   "block": "orientation",
   "mode": "text",
   "reason": "rule 6: BC-SKL-04006 and BC-SKL-04007 carry BC-REP-01 and BC-REP-05",
   "sources": [
    "BC-SKL-04006"
   ]
  },
  {
   "block": "ki-1",
   "mode": "text",
   "reason": "rule 6: a symbolic rule, BC-REP-01 and BC-REP-05",
   "sources": [
    "BC-SKL-04007"
   ]
  },
  {
   "block": "ex-1",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  },
  {
   "block": "err-BC-ERR-04006",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  }
 ],
 "refresher": [
  "ki-1",
  "err-BC-ERR-04006",
  "ex-1"
 ],
 "research_lines": [
  {
   "file": "research/question-analysis/question-archetypes.md",
   "line": "Velocity is the derivative of position and acceleration is the derivative of velocity"
  }
 ],
 "inferred": [
  {
   "claim": "BC-QA-04003 is calculator status either, so the lesson times it as Section I Part A at 2.14 minutes.",
   "settles": "A calculator status of calculator or no_calculator on BC-QA-04003."
  },
  {
   "claim": "The lesson carries 2 checks: the bundle lists one error, fewer than the three distractors an MCQ check 3 needs.",
   "settles": "Two more active BC-ERR records linked to BC-SKL-04006 or BC-SKL-04007."
  }
 ],
 "sources": [
  "BC-CON-04003",
  "BC-SKL-04006",
  "BC-SKL-04007",
  "BC-EK-CHA-3B1",
  "ced:88",
  "BC-QA-04003",
  "BC-QA-04010",
  "BC-PT-99004",
  "BC-PT-99027",
  "BC-ERR-04006",
  "BC-MIS-04004",
  "BC-PRQ-04008",
  "crabbc-25:20",
  "cr-22:20",
  "research/units/unit-04-contextual-applications-differentiation.md#4.2 Straight-Line Motion: Connecting Position, Velocity, and Acceleration",
  "research/question-analysis/question-archetypes.md#BC-QA-04003 Straight-line motion with velocity, acceleration, and speed",
  "research/question-analysis/question-archetypes.md#BC-QA-04010 Position recovered from velocity with an initial condition",
  "research/scoring/common-point-losses.md#Answer points",
  "research/exam/exam-structure.md#Section and part layout"
 ],
 "word_count": {
  "full": 475,
  "brief": 428
 },
 "read_minutes": {
  "full": 3.2,
  "brief": 2.9
 }
}
```
