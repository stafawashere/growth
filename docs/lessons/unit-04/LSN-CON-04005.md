---
title: LSN-CON-04005 Speeding up and slowing down
research_date: 2026-09-29
status: designed
purpose: Authoring spec for the concept lesson on BC-CON-04005, deciding whether speed increases from the signs of velocity and acceleration, built from authoring_bundle("BC-CON-04005") and the research files it cites, so an author fills plan 15's lesson record without making a teaching decision.
---

# LSN-CON-04005 Speeding up and slowing down

Concept BC-CON-04005 (skills BC-SKL-04010, BC-SKL-04012), topic 4.2 of Unit 4, loaded by BC-QA-04003 and BC-QA-04004. Its hard parents are BC-CON-04003 and BC-CON-04004 (docs/lessons/unit-04/README.md, section 1).

## Orientation

Served text, from BC-CON-04005 `description_plain` and the Assessment behaviour paragraph (research/units/unit-04-contextual-applications-differentiation.md#4.2 Straight-Line Motion: Connecting Position, Velocity, and Acceleration), whose justification variants require both signs named and applied to the particle in the problem (crabbc-25:23). No count, no frequency.

## Key ideas

Both skills map BC-EK-CHA-3B1: one core block, both bands.

- ki-1 (core, BC-EK-CHA-3B1, ced:88). The Speeding up and slowing down paragraph of Required mathematical knowledge, hypotheses then conclusion (cr-22:21), with the Sign analysis paragraph's reading in words (crabbc-25:22). No anchor quote: the bundle's `ced_pages` for this concept is empty (library gap), so no quote can be checked against a bundle page; ced:88 is cited from the skill's BC-EK.

## Recognition

- BC-QA-04003 (research/question-analysis/question-archetypes.md#BC-QA-04003 Straight-line motion with velocity, acceleration, and speed): `typical_wording` "is the speed of the particle increasing, decreasing, or neither at the stated time, and give a reason"; `common_givens` a position or velocity function, sometimes the sign of the acceleration at an instant; `asked_to_produce` a decision with a reason. The signal: the word speed with increasing or decreasing and give a reason. Shapes: a part of the particle motion FRQ (BC-FRQ-2014-Q4-A, BC-FRQ-2015-Q3-C) and an MCQ (BC-MCQ-CED-012).
- BC-QA-04004 (research/question-analysis/question-archetypes.md#BC-QA-04004 Direction of motion and sign analysis over an interval), same family: the sign analysis over an interval whose reading must be stated in words, BC-SKL-04012.

Not this concept: find the acceleration (one value, BC-CON-04003), or which way the particle moves (one sign, BC-CON-04004).

## Method choice

One strategy block: BC-QA-04003 and BC-QA-04004 share the family motion-by-differentiation, and BC-QA-04003 is listed first.

- st-1, BC-QA-04003. Method, `expected_solution_path[0]` with its next step: differentiate as needed, then evaluate velocity and acceleration at the instant. Rival, `wrong_approaches`: the speed decided from the acceleration alone (BC-ERR-99003). Separating feature: speed is a size, so the direction of motion enters. The archetype carries `asked_to_produce` and `common_givens` in the snapshot, so the block is verified.

## Solution path

- ex-1, BC-QA-04003, both bands, no calculator. Draw: cubic 1, quadratic -2, free 4, speed_value 3, instant 2, given velocity, heading left. Derived: constant -11, v(t) = t^3 - 2t^2 + 4t - 11, v(2) = -3, a(2) = 8. Heading left makes the acceleration-only verdict wrong, as the spec's notes intend. No published BC-QA-04003 item carries this draw.
- Steps: velocity (new), acceleration (differentiate), a(2) (evaluate, BC-PT-99027), v(2) (new), the comparison in words (no value). The answer is a statement. A fluent solver writes steps 2 to 5; the conclusion names both signs and this particle.

## Scoring

BC-QA-04003 lists BC-PT-99021, BC-PT-99027 and BC-PT-99004. ex-1 tags BC-PT-99027 on a(2); the line is reader_checks(["BC-PT-99027"]) copied exactly. The reason for the speed conclusion is scored in the 2025 rubric only when the sign of the velocity is stated and applied (crabbc-25:22, crabbc-25:23), but no point type on the archetype holds it, so the step is untagged (library gap).

Point losses for the author: speed from the sign of acceleration alone (BC-ERR-99003, cr-23:7, cr-24:7; research/scoring/common-point-losses.md#Justification points). No drawn sign chart is required, and none earns a point by itself (research/scoring/justification-requirements.md#Sign analysis of a derivative).

## Traps

Two active errors meet the skills, in the bundle's order: BC-ERR-04011, BC-ERR-99003. Both bands show both, on ex-1's draw.

- err-BC-ERR-04011: the two signs listed with no sentence, against the same signs with the reading in words; the values agree, so the relation is equivalent and the loss is the missing reading. Possible reason from BC-MIS-04017.
- err-BC-ERR-99003: a(2) > 0 read as speeding up, against the product v(2)a(2) < 0. Possible reason from BC-MIS-99001.

## Representations

None. BC-SKL-04010 and BC-SKL-04012 list no figure-bearing representation (docs/lessons/unit-04/README.md, section 6).

## Prerequisite bridge

- BC-PRQ-04005 and BC-PRQ-04009, each from its `description_plain` and `failure_signature`.

## Time

BC-QA-04003 has calculator status either, so the lesson takes Section I Part A, 2.14 minutes per question (research/exam/exam-structure.md#Section and part layout) [inferred: the either status]. As an FRQ part it takes 1.67 to 3.33 minutes of a 15.0 minute question (docs/lessons/unit-04/README.md, section 5). The minutes go on the two values with their signs and the sentence; the differentiation of a cubic is fast.

## Checks

- chk-1, completion of ex-1, both bands: v(2) and a(2) given, the student decides and gives the reason. Key: decreasing.
- chk-2, isomorph, both bands. Draw: cubic 1, quadratic 1, free -6, speed_value 2, instant 1, given velocity, heading left; v(1) = -2, a(1) = -1. Key: increasing.
- No chk-3: two errors in the bundle, fewer than the three error paths an MCQ needs (inferred array).

## Delivery

- orientation, ki-1: text. Rule 5: no figure-bearing representation on BC-SKL-04010 or BC-SKL-04012 (docs/lessons/unit-04/README.md, section 6).
- ex-1, err-BC-ERR-04011, err-BC-ERR-99003: step_reveal. Rule 1.

## Band plan

- Low (full): orientation, ki-1, st-1, ex-1 with its scoring line, both error blocks, chk-1, chk-2, both bridges. 446 words, 3.0 minutes (cap 900 and 6).
- Mid (brief): the same blocks, since the lesson has one core key idea, one strategy block, two error blocks and two checks. 446 words, 3.0 minutes (cap 450 and 3).
- Refresher: ki-1, err-BC-ERR-04011, err-BC-ERR-99003, ex-1.

## Sources

- BC-CON-04005; BC-SKL-04010, BC-SKL-04012; BC-EK-CHA-3B1; ced:88
- BC-QA-04003, BC-QA-04004; BC-PT-99027; cr-22:21, crabbc-25:22, crabbc-25:23, cr-23:7, cr-24:7
- BC-ERR-04011, BC-ERR-99003; BC-MIS-04017, BC-MIS-99001; BC-PRQ-04005, BC-PRQ-04009
- research/units/unit-04-contextual-applications-differentiation.md#4.2 Straight-Line Motion: Connecting Position, Velocity, and Acceleration
- research/question-analysis/question-archetypes.md#BC-QA-04003 Straight-line motion with velocity, acceleration, and speed
- research/question-analysis/question-archetypes.md#BC-QA-04004 Direction of motion and sign analysis over an interval
- research/scoring/common-point-losses.md#Justification points
- research/scoring/justification-requirements.md#Sign analysis of a derivative
- research/exam/exam-structure.md#Section and part layout
- [inferred] The exam part for an either archetype. Settled by a calculator status on BC-QA-04003.
- [inferred] Two checks only. Settled by a third error linked to the concept's skills.
- [inferred] No anchor quote. Settled by a ced source on the concept.
- [inferred] No point tag on the speed reason. Settled by a justification point type on BC-QA-04003.

## Machine record

```json
{
 "id": "LSN-CON-04005",
 "kind": "concept",
 "target_id": "BC-CON-04005",
 "unit": "04",
 "skills": [
  "BC-SKL-04010",
  "BC-SKL-04012"
 ],
 "orientation": {
  "text": "Whether a particle speeds up at an instant needs two signs: velocity and acceleration there. A response states both, compares them, and applies the conclusion to this particle at this instant.",
  "sources": [
   "BC-CON-04005",
   "research/units/unit-04-contextual-applications-differentiation.md#4.2 Straight-Line Motion: Connecting Position, Velocity, and Acceleration"
  ]
 },
 "key_ideas": [
  {
   "id": "ki-1",
   "ek_id": "BC-EK-CHA-3B1",
   "depth": "core",
   "text": "With \\(v(t_0)\\) and \\(a(t_0)\\) both known: the same sign means the speed is increasing, opposite signs mean it is decreasing. The sign of the acceleration alone does not settle it (cr-22:21). Over an interval, the reading of a sign analysis is written in words for the whole interval (crabbc-25:22).",
   "notation": "signs of v of t and a of t compared",
   "quote": null,
   "sources": [
    "BC-EK-CHA-3B1",
    "ced:88",
    "cr-22:21",
    "crabbc-25:22",
    "research/units/unit-04-contextual-applications-differentiation.md#4.2 Straight-Line Motion: Connecting Position, Velocity, and Acceleration"
   ]
  }
 ],
 "strategy": [
  {
   "id": "st-1",
   "archetype_id": "BC-QA-04003",
   "cue": "The stem asks: is the speed increasing, decreasing, or neither at the stated time, and give a reason.",
   "method": "First line: \\(v(t_0)\\) and \\(a(t_0)\\), each with its sign.",
   "rival": "Rival: the conclusion from the sign of acceleration alone (BC-ERR-99003).",
   "separating_feature": "Speed is a size, so direction enters: both signs.",
   "sources": [
    "BC-QA-04003"
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
    "quadratic": -2,
    "free": 4,
    "speed_value": 3,
    "instant": 2,
    "given": "velocity",
    "heading": "left"
   },
   "problem": {
    "text": "A particle's velocity is \\(v(t)=t^3-2t^2+4t-11\\). Is its speed increasing or decreasing at \\(t=2\\)? Give a reason.",
    "command_verb": "determine"
   },
   "calculator_status": "no_calculator",
   "steps": [
    {
     "cue": "Speed asked: two signs needed.",
     "why": "Velocity is given.",
     "expr": "t**3 - 2*t**2 + 4*t - 11",
     "relation": "new"
    },
    {
     "cue": "Acceleration: differentiate velocity.",
     "why": "\\(a(t)=v'(t)\\).",
     "expr": "3*t**2 - 4*t + 4",
     "relation": "differentiate",
     "variable": "t"
    },
    {
     "cue": "At \\(t=2\\).",
     "why": "\\(a(2)=8>0\\).",
     "expr": "8",
     "relation": "evaluate",
     "subs": {
      "t": "2"
     },
     "point_type_id": "BC-PT-99027"
    },
    {
     "cue": "Velocity at \\(t=2\\).",
     "why": "\\(v(2)=-3<0\\).",
     "expr": "-3",
     "relation": "new"
    },
    {
     "cue": "Signs differ.",
     "why": "Speed decreasing at \\(t=2\\): \\(v(2)<0\\) and \\(a(2)>0\\)."
    }
   ],
   "answer": {
    "form": "statement",
    "expr": "decreasing",
    "text": "The speed is decreasing at t = 2 because v(2) = -3 < 0 and a(2) = 8 > 0 have opposite signs."
   }
  }
 ],
 "what_a_reader_scores": [
  {
   "example_id": "ex-1",
   "point_type_ids": [
    "BC-PT-99027"
   ],
   "lines": [
    {
     "point_type_id": "BC-PT-99027",
     "text": "Higher derivative expression evaluated at a point. Earned by: A correct expression for the second or higher derivative, evaluated at the requested point, consistent with the earlier derivative work (sg-25:20, sg-23:10). Not earned by: An expression left in terms of the first derivative where the prompt asked for it in terms of the dependent variable (sg-23:11)."
    }
   ]
  }
 ],
 "common_errors": [
  {
   "error_id": "BC-ERR-04011",
   "wrong_step": {
    "text": "Signs listed, no sentence.",
    "expr": "FiniteSet(-3, 8)"
   },
   "right_step": {
    "text": "Signs listed, then the reading in words.",
    "expr": "FiniteSet(-3, 8)"
   },
   "relation": "equivalent",
   "possible_reason": {
    "misconception_id": "BC-MIS-04017",
    "text": "the communicated conclusion does not cover the interval"
   },
   "sources": [
    "BC-ERR-04011",
    "BC-MIS-04017"
   ],
   "observed_behavior": "A number line or table of signs appears with no sentence saying what it shows about the direction of motion over the interval.",
   "scoring_consequence": "The 2025 report records that responses failing to communicate what the chart showed over the whole interval did not earn the analysis points (crabbc-25:22, crabbc-25:23); BC-ERR-99001 records vague referents in justification across years."
  },
  {
   "error_id": "BC-ERR-99003",
   "wrong_step": {
    "text": "\\(a(2)>0\\), so speeding up.",
    "expr": "8"
   },
   "right_step": {
    "text": "\\(v(2)a(2)<0\\), so slowing down.",
    "expr": "-3*8"
   },
   "relation": "distinct",
   "possible_reason": {
    "misconception_id": "BC-MIS-99001",
    "text": "the sign of acceleration by itself decides whether a particle is speeding up or slowing down"
   },
   "sources": [
    "BC-ERR-99003",
    "BC-MIS-99001"
   ],
   "observed_behavior": "Responses conclude that a particle is speeding up or slowing down from the sign of acceleration by itself, without also considering the sign of velocity at that instant.",
   "scoring_consequence": "The reasoning point for speeding up or slowing down is not earned, even when the reported acceleration value is correct."
  }
 ],
 "representations": null,
 "prerequisite_bridges": [
  {
   "prq_id": "BC-PRQ-04005",
   "text": "Absolute value is size without sign; speed is \\(|v|\\). The failure: a negative speed, or a direction answered with a size."
  },
  {
   "prq_id": "BC-PRQ-04009",
   "text": "Solve for zeros, split the interval, find each piece's sign. The failure: intervals from sampled integers."
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
   "archetype_id": "BC-QA-04003",
   "parameter_draw": {
    "cubic": 1,
    "quadratic": -2,
    "free": 4,
    "speed_value": 3,
    "instant": 2,
    "given": "velocity",
    "heading": "left"
   },
   "completes": "ex-1",
   "stem": {
    "text": "\\(v(2)=-3\\) and \\(a(2)=8\\). Is the speed increasing or decreasing at \\(t=2\\)? Give a reason.",
    "command_verb": "determine"
   },
   "key": {
    "form": "statement",
    "expr": "decreasing",
    "text": "Decreasing: v(2) and a(2) have opposite signs."
   },
   "steps": [
    {
     "text": "The product of the signs.",
     "expr": "-3*8",
     "relation": "new"
    },
    {
     "text": "Negative: opposite signs.",
     "expr": "-24",
     "relation": "equivalent"
    }
   ],
   "calculator_status": "no_calculator",
   "skills": [
    "BC-SKL-04010"
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
    "cubic": 1,
    "quadratic": 1,
    "free": -6,
    "speed_value": 2,
    "instant": 1,
    "given": "velocity",
    "heading": "left"
   },
   "stem": {
    "text": "\\(v(t)=t^3+t^2-6t+2\\). Is the speed increasing or decreasing at \\(t=1\\)? Give a reason.",
    "command_verb": "determine"
   },
   "key": {
    "form": "statement",
    "expr": "increasing",
    "text": "Increasing: v(1) = -2 and a(1) = -1 share a sign."
   },
   "steps": [
    {
     "text": "v(t).",
     "expr": "t**3 + t**2 - 6*t + 2",
     "relation": "new"
    },
    {
     "text": "v(1).",
     "expr": "-2",
     "relation": "evaluate",
     "subs": {
      "t": "1"
     }
    },
    {
     "text": "a(t).",
     "expr": "3*t**2 + 2*t - 6",
     "relation": "new"
    },
    {
     "text": "a(1).",
     "expr": "-1",
     "relation": "evaluate",
     "subs": {
      "t": "1"
     }
    }
   ],
   "calculator_status": "no_calculator",
   "skills": [
    "BC-SKL-04010"
   ]
  }
 ],
 "delivery": [
  {
   "block": "orientation",
   "mode": "text",
   "reason": "rule 5: BC-SKL-04010 carries BC-REP-01 and BC-REP-05, BC-SKL-04012 BC-REP-01 and BC-REP-04",
   "sources": [
    "BC-SKL-04010"
   ]
  },
  {
   "block": "ki-1",
   "mode": "text",
   "reason": "rule 5: a sign comparison rule with no figure-bearing representation",
   "sources": [
    "BC-SKL-04010",
    "BC-SKL-04012"
   ]
  },
  {
   "block": "ex-1",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  },
  {
   "block": "err-BC-ERR-04011",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  },
  {
   "block": "err-BC-ERR-99003",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  }
 ],
 "refresher": [
  "ki-1",
  "err-BC-ERR-04011",
  "err-BC-ERR-99003",
  "ex-1"
 ],
 "research_lines": [
  {
   "file": "research/scoring/common-point-losses.md",
   "line": "Speed conclusion drawn from the sign of acceleration alone"
  }
 ],
 "inferred": [
  {
   "claim": "BC-QA-04003 is calculator status either, so the lesson times it as Section I Part A at 2.14 minutes.",
   "settles": "A calculator status of calculator or no_calculator on BC-QA-04003."
  },
  {
   "claim": "The lesson carries 2 checks: the bundle lists two errors, fewer than the three distractors an MCQ check 3 needs.",
   "settles": "A third active BC-ERR linked to BC-SKL-04010 or BC-SKL-04012."
  },
  {
   "claim": "ki-1 carries no anchor quote because the bundle's ced_pages for this concept is empty.",
   "settles": "A ced source on BC-CON-04005 or its skills, such as ced:88 for BC-EK-CHA-3B1."
  },
  {
   "claim": "The speed conclusion step carries no point tag: BC-QA-04003 point_types hold no reason or justification type for it.",
   "settles": "A justification point type on BC-QA-04003 for the speed reason scored in crabbc-25:22."
  }
 ],
 "sources": [
  "BC-CON-04005",
  "BC-SKL-04010",
  "BC-SKL-04012",
  "BC-EK-CHA-3B1",
  "ced:88",
  "cr-22:21",
  "crabbc-25:22",
  "crabbc-25:23",
  "cr-23:7",
  "cr-24:7",
  "BC-QA-04003",
  "BC-QA-04004",
  "BC-PT-99027",
  "BC-ERR-04011",
  "BC-ERR-99003",
  "BC-MIS-04017",
  "BC-MIS-99001",
  "BC-PRQ-04005",
  "BC-PRQ-04009",
  "research/units/unit-04-contextual-applications-differentiation.md#4.2 Straight-Line Motion: Connecting Position, Velocity, and Acceleration",
  "research/question-analysis/question-archetypes.md#BC-QA-04003 Straight-line motion with velocity, acceleration, and speed",
  "research/question-analysis/question-archetypes.md#BC-QA-04004 Direction of motion and sign analysis over an interval",
  "research/scoring/common-point-losses.md#Justification points",
  "research/scoring/justification-requirements.md#Sign analysis of a derivative",
  "research/exam/exam-structure.md#Section and part layout"
 ],
 "word_count": {
  "full": 446,
  "brief": 446
 },
 "read_minutes": {
  "full": 3.0,
  "brief": 3.0
 }
}
```
