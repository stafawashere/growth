---
title: LSN-CON-05004 Monotonicity read from the sign of the first derivative
research_date: 2026-09-29
status: designed
purpose: Authoring spec for the concept lesson on BC-CON-05004, monotonicity read from the sign of the first derivative, built from authoring_bundle("BC-CON-05004") and the research files it cites, so an author fills plan 15's lesson record without making a teaching decision.
---

# LSN-CON-05004 Monotonicity read from the sign of the first derivative

Concept BC-CON-05004 (skills BC-SKL-05014 to BC-SKL-05018), topic 5.3 of Unit 5, loaded by one archetype, BC-QA-05008 (family monotonicity-analysis, tagged [inferred] in the research). No unit parent (docs/lessons/unit-05/README.md, section 1). The written reason, the sign of the named derivative on the named interval, is the object of the lesson.

## Orientation

Served text, from BC-CON-05004 `description_plain` and the topic's Assessment behaviour paragraph (research/units/unit-05-analytical-applications-differentiation.md#5.3 Determining Intervals on Which a Function is Increasing or Decreasing): a response partitions at the zeros of f' and where f' or f is undefined, reports open intervals, and gives as reason the sign of f' on each. No count, no frequency.

## Key ideas

All five skills map to BC-EK-FUN-4A1 (ced:101), so one core block, both bands.

- ki-1 (core). Paraphrase of the Required mathematical knowledge paragraph (Monotonicity test, Partition points, Justification standard): f' positive on an open interval gives f increasing there, negative gives decreasing; the partition points are the zeros of f' and the inputs where f' or f is undefined; the reason names f' and its sign (sg-25:17). Anchor quote (13 words) from ced:101. Notation line from the concept record.

## Recognition

- BC-QA-05008 (research/question-analysis/question-archetypes.md#BC-QA-05008 Intervals of increase or decrease justified by the sign of the derivative): `typical_wording` "on what open intervals is the function increasing, and give a reason for the answer"; `common_givens` a function or its derivative, an interval of definition; `asked_to_produce` a union of open intervals, a reason naming the sign of the derivative. The signal: "increasing" or "decreasing" with "on what intervals". FRQ appearances BC-FRQ-2022-Q3-C, BC-FRQ-2024-Q1-D; MCQ BC-MCQ-SAMPLE-012, BC-MCQ-PE2012-030.

What says "not this concept": "concave up" asks whether f' rises, not its sign (BC-CON-05007; BC-ERR-05016, sg-23:14); "relative maximum at x = c" asks for a sign change at one input (BC-CON-05005).

## Method choice

One strategy block, both bands.

- st-1, BC-QA-05008. Method, `expected_solution_path[0]`: find the zeros and undefined points of the derivative. Rival, `wrong_approaches`: testing a single input and generalising. Separating feature: every partition point, including where f is undefined, ends an interval. The archetype carries `asked_to_produce` and `common_givens`, so the block is not tagged inferred.

## Solution path

- ex-1, BC-QA-05008, both bands, no calculator. Draw: first_zero -1, second_zero 3, gap 1, scale 2, direction increasing, leading_sign 1, domain_break odd, so f'(x) = 2(x + 1)(x - 3)/(x - 1) per the spec's notes, with f undefined at x = 1. No published BC-QA-05008 item carries this draw. Steps follow `expected_solution_path`: zeros of the numerator (new, solve), the undefined input (no value), signs by test values (no value), the intervals (new), the reason (no value, tagged BC-PT-99005: the intervals with the sign analysis that produces them).

A fluent solver writes the partition points, the intervals and the reason sentence; test values are held in the head. A drawn sign chart earns nothing on its own (research/scoring/justification-requirements.md#Sign analysis of a derivative).

## Scoring

BC-QA-05008 lists BC-PT-99005, BC-PT-99063 and BC-PT-99010. ex-1 tags BC-PT-99005 on the reason step: ex-1 asks a single condition, and BC-PT-99063 earns only a reason matched to a compound condition (sg-26:16), so the intervals with their sign analysis are scored as an answer with supporting work; its line is `reader_checks(["BC-PT-99005"])`. For the author: an unnamed referent such as the function or the graph forfeits the reason (sg-25:17, research/scoring/justification-requirements.md#Reasons tied to the object the prompt names; research/scoring/common-point-losses.md#Notation points).

## Traps

Eight active errors meet the skills; the first four in the bundle's order are served (low band all four, mid band the first two). BC-ERR-05018, 05019, 99001 and 99030 are left out by the cap of 4.

- err-BC-ERR-05014: the sign on (-oo, -1) misread, adding that interval. No possible reason line: neither linked description names a misread test value.
- err-BC-ERR-05015: the rise of a plotted f' read as the rise of f. Statement-shaped. Possible reason, words from BC-MIS-05011.
- err-BC-ERR-05016: f' increasing cited for f increasing. Statement-shaped. Possible reason, words from BC-MIS-05020.
- err-BC-ERR-05017: x = 1 left off the partition, giving (-1, 3). Possible reason, words from BC-MIS-05012.

## Representations

None as a separate block. The topic's Representations paragraph names the graph of f' to intervals of increase of f (BC-REP-02 to BC-REP-04), which ki-1's interactive carries.

## Prerequisite bridge

- BC-PRQ-05001, BC-PRQ-05002, BC-PRQ-05003, BC-PRQ-05006, each from its `description_plain` and `failure_signature`.

## Time

BC-QA-05008 has `calculator_status` either, so the lesson takes Section I Part A, 2.14 minutes per question (research/exam/exam-structure.md#Section and part layout) [inferred: an either archetype sits in either part; as an FRQ part it takes a share of 15.0 minutes]. The minutes go on the partition and the reason sentence; the sign chart is scratch work.

## Checks

- chk-1, completion of ex-1, both bands: the signs on each piece are given, the student writes the intervals. Key (-1, 1) union (3, oo).
- chk-2, isomorph, both bands. Draw: first_zero -2, second_zero 2, gap 0, scale 1, direction decreasing, leading_sign 1, domain_break none; f'(x) = (x + 2)(x - 2). Key (-2, 2).
- chk-3, MCQ, low band. Draw: first_zero 0, second_zero 4, gap 2, scale 1, direction increasing, leading_sign 1, domain_break odd; f'(x) = x(x - 4)/(x - 2). Key (0, 2) union (4, oo). Distractors: (-oo, 0) added (BC-ERR-05014); where f' rises, (-oo, 2) union (2, oo) (BC-ERR-05016); x = 2 left off, (0, 4) union (4, oo) (BC-ERR-05017).

## Delivery

- orientation: figure. Rule 3 on BC-REP-02 in BC-SKL-05015 (docs/lessons/unit-05/README.md, section 6).
- ki-1: interactive, one draggable point on the graph of f' with the question "is f rising here?". Rule 3 promoted by BC-QA-05008 `difficulty_variables` "whether the derivative changes sign at an undefined point" and the stem's reading of intervals [inferred; settled by the modality A/B].
- ex-1 and the four error blocks: step_reveal. Rule 1.

## Band plan

- Low (full): orientation, ki-1, st-1, ex-1 with its scoring line, the four error blocks, chk-1 to chk-3, the four bridges. 581 words, 3.9 minutes (cap 900 and 6).
- Mid (brief): orientation, ki-1, st-1, ex-1 with its scoring line, err-BC-ERR-05014, err-BC-ERR-05015, chk-1, chk-2, the bridges. 446 words, 3.0 minutes (cap 450 and 3).
- Refresher: ki-1, err-BC-ERR-05014, err-BC-ERR-05015, err-BC-ERR-05016, err-BC-ERR-05017, ex-1.

## Sources

- BC-CON-05004; BC-SKL-05014 to BC-SKL-05018; BC-EK-FUN-4A1; ced:101
- BC-QA-05008; BC-FRQ-2022-Q3-C, BC-FRQ-2024-Q1-D, BC-MCQ-SAMPLE-012, BC-MCQ-PE2012-030
- BC-PT-99063, BC-PT-99005, BC-PT-99010; sg-25:17, sg-23:14
- BC-ERR-05014, BC-ERR-05015, BC-ERR-05016, BC-ERR-05017, BC-ERR-05018, BC-ERR-05019, BC-ERR-99001, BC-ERR-99030; BC-MIS-05011, BC-MIS-05012, BC-MIS-05020
- BC-PRQ-05001, BC-PRQ-05002, BC-PRQ-05003, BC-PRQ-05006
- research/units/unit-05-analytical-applications-differentiation.md#5.3 Determining Intervals on Which a Function is Increasing or Decreasing
- research/question-analysis/question-archetypes.md#BC-QA-05008 Intervals of increase or decrease justified by the sign of the derivative
- research/scoring/justification-requirements.md#Sign analysis of a derivative
- research/scoring/justification-requirements.md#Reasons tied to the object the prompt names
- research/scoring/common-point-losses.md#Notation points
- research/exam/exam-structure.md#Section and part layout
- [inferred] BC-QA-05008 is an either archetype placed in Section I Part A. Settled by a calculator_status of calculator or no_calculator on the archetype.
- [inferred] The reason point scored by analogy with the concavity part. Settled by a released scoring guideline for a monotonicity part.
- [inferred] The orientation figure and the ki-1 interactive. Settled by the modality A/B.

## Machine record

```json
{
 "id": "LSN-CON-05004",
 "kind": "concept",
 "target_id": "BC-CON-05004",
 "unit": "05",
 "skills": [
  "BC-SKL-05014",
  "BC-SKL-05015",
  "BC-SKL-05016",
  "BC-SKL-05017",
  "BC-SKL-05018"
 ],
 "orientation": {
  "text": "A response splits the line at zeros of f' and where f' or f is undefined, reports open intervals, and gives the sign of f' on each as its reason.",
  "sources": [
   "BC-CON-05004",
   "research/units/unit-05-analytical-applications-differentiation.md#5.3 Determining Intervals on Which a Function is Increasing or Decreasing"
  ]
 },
 "key_ideas": [
  {
   "id": "ki-1",
   "ek_id": "BC-EK-FUN-4A1",
   "depth": "core",
   "text": "f' > 0 on an open interval means f increases there; f' < 0 means it decreases. The intervals end at zeros of f' and where f' or f is undefined. The reason names f' and its sign on that interval.",
   "notation": "f' > 0; f' < 0; increasing; decreasing",
   "quote": {
    "text": "including intervals where the function is increasing or decreasing.",
    "source": "ced:101"
   },
   "sources": [
    "BC-EK-FUN-4A1",
    "ced:101",
    "sg-25:17",
    "research/units/unit-05-analytical-applications-differentiation.md#5.3 Determining Intervals on Which a Function is Increasing or Decreasing"
   ]
  }
 ],
 "strategy": [
  {
   "id": "st-1",
   "archetype_id": "BC-QA-05008",
   "cue": "On what open intervals is f increasing, from f or f'?",
   "method": "First line: zeros of f' and inputs where f' or f is undefined.",
   "rival": "Rival: testing one input and generalising.",
   "separating_feature": "Every partition point, including a domain gap, ends an interval.",
   "sources": [
    "BC-QA-05008"
   ],
   "evidence_tag": "verified"
  }
 ],
 "worked_examples": [
  {
   "id": "ex-1",
   "archetype_id": "BC-QA-05008",
   "bands": [
    "low",
    "mid"
   ],
   "parameter_draw": {
    "first_zero": -1,
    "second_zero": 3,
    "gap": 1,
    "scale": 2,
    "direction": "increasing",
    "leading_sign": 1,
    "domain_break": "odd"
   },
   "problem": {
    "text": "f is defined for x ≠ 1, with f'(x) = 2(x + 1)(x - 3)/(x - 1). On what open intervals is f increasing? Give a reason.",
    "command_verb": "find"
   },
   "calculator_status": "no_calculator",
   "steps": [
    {
     "cue": "Intervals asked: partition first.",
     "why": "Numerator zeros.",
     "expr": "2*(x + 1)*(x - 3) = 0",
     "relation": "new"
    },
    {
     "cue": "Solve.",
     "why": "Two zeros.",
     "expr": "FiniteSet(-1, 3)",
     "relation": "solve",
     "variable": "x"
    },
    {
     "cue": "Denominator x - 1.",
     "why": "f and f' undefined at 1: a partition point."
    },
    {
     "cue": "Sign on each piece.",
     "why": "f'(0) = 6, f'(2) = -6, f'(4) > 0, f'(-2) < 0."
    },
    {
     "cue": "Keep the positive pieces.",
     "why": "Open intervals, split at 1.",
     "expr": "Union(Interval.open(-1, 1), Interval.open(3, oo))",
     "relation": "new"
    },
    {
     "cue": "Give a reason.",
     "why": "f is increasing there because f'(x) > 0 on (-1, 1) and (3, oo).",
     "point_type_id": "BC-PT-99005"
    }
   ],
   "answer": {
    "form": "symbolic",
    "expr": "Union(Interval.open(-1, 1), Interval.open(3, oo))"
   }
  }
 ],
 "what_a_reader_scores": [
  {
   "example_id": "ex-1",
   "point_type_ids": [
    "BC-PT-99005"
   ],
   "lines": [
    {
     "point_type_id": "BC-PT-99005",
     "text": "Answer with supporting work or setup shown. Earned by: The correct value together with the setup the prompt demanded, such as a difference and a quotient from a table or an equation that produces the value (sg-26:2, sg-25:4). Not earned by: An unsupported value (sg-23:10, sg-22:9), or a setup with no value (sg-26:2). Notation: sg-22:6 withholds this point for an equation of the form function equals constant, such as a derivative expression set equal to a number without evaluation. Precision: A reported decimal answer must be accurate to three places after the decimal point, rounded or truncated; at most one point per question is lost to inappropriate rounding (sg-25:2, sg-26:2)."
    }
   ]
  }
 ],
 "common_errors": [
  {
   "error_id": "BC-ERR-05014",
   "wrong_step": {
    "text": "(-oo, -1) added.",
    "expr": "Union(Interval.open(-oo, -1), Interval.open(-1, 1), Interval.open(3, oo))"
   },
   "right_step": {
    "text": "f'(-2) < 0: left out.",
    "expr": "Union(Interval.open(-1, 1), Interval.open(3, oo))"
   },
   "relation": "distinct",
   "possible_reason": null,
   "sources": [
    "BC-ERR-05014"
   ],
   "observed_behavior": "The response assigns the wrong sign to the derivative expression on one of the intervals of its sign chart.",
   "scoring_consequence": "The reported intervals are wrong, which also forfeits the reason point."
  },
  {
   "error_id": "BC-ERR-05015",
   "wrong_step": {
    "text": "Where the plotted f' rises.",
    "expr": "plotted_curve_rises"
   },
   "right_step": {
    "text": "Where the plotted f' is above the axis.",
    "expr": "plotted_curve_above_axis"
   },
   "relation": "distinct",
   "possible_reason": {
    "misconception_id": "BC-MIS-05011",
    "text": "answers questions about the function by reading features of whatever curve is drawn"
   },
   "sources": [
    "BC-ERR-05015",
    "BC-MIS-05011"
   ],
   "observed_behavior": "The response answers a question about the function by describing features of the curve shown, which is the derivative.",
   "scoring_consequence": "Every part that rests on the plotted object is answered about the wrong function."
  },
  {
   "error_id": "BC-ERR-05016",
   "wrong_step": {
    "text": "Because f' is increasing.",
    "expr": "f_prime_increasing"
   },
   "right_step": {
    "text": "Because f' > 0.",
    "expr": "f_prime_positive"
   },
   "relation": "distinct",
   "possible_reason": {
    "misconception_id": "BC-MIS-05020",
    "text": "the sign and the direction of the derivative are used interchangeably"
   },
   "sources": [
    "BC-ERR-05016",
    "BC-MIS-05020"
   ],
   "observed_behavior": "The response reports concavity where monotonicity was asked for, or reports increase of the function where the derivative graph is rising.",
   "scoring_consequence": "The intervals reported belong to the other question and the reason point is unavailable."
  },
  {
   "error_id": "BC-ERR-05017",
   "wrong_step": {
    "text": "No split at 1.",
    "expr": "Union(Interval.open(-1, 3), Interval.open(3, oo))"
   },
   "right_step": {
    "text": "Split at 1.",
    "expr": "Union(Interval.open(-1, 1), Interval.open(3, oo))"
   },
   "relation": "distinct",
   "possible_reason": {
    "misconception_id": "BC-MIS-05012",
    "text": "reports one interval of increase or concavity spanning an input where the function does not exist"
   },
   "sources": [
    "BC-ERR-05017",
    "BC-MIS-05012"
   ],
   "observed_behavior": "The response partitions the number line at the zeros of the derivative only and ignores a vertical asymptote or a domain gap.",
   "scoring_consequence": "An interval spans a break, so the reported behaviour is claimed where the function does not exist."
  }
 ],
 "representations": null,
 "prerequisite_bridges": [
  {
   "prq_id": "BC-PRQ-05001",
   "text": "Set each factor and the denominator to zero."
  },
  {
   "prq_id": "BC-PRQ-05002",
   "text": "One test value per piece fixes its sign."
  },
  {
   "prq_id": "BC-PRQ-05003",
   "text": "No interval crosses an input where f is undefined."
  },
  {
   "prq_id": "BC-PRQ-05006",
   "text": "Read the axis label: f or f'?"
  }
 ],
 "time": {
  "exam_part": "I-A",
  "budget_minutes": 2.14,
  "source": "research/exam/exam-structure.md#Section and part layout",
  "written_steps": {
   "ex-1": [
    1,
    2,
    5,
    6
   ]
  },
  "skipped_steps": {
   "ex-1": [
    3,
    4
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
   "archetype_id": "BC-QA-05008",
   "parameter_draw": {
    "first_zero": -1,
    "second_zero": 3,
    "gap": 1,
    "scale": 2,
    "direction": "increasing",
    "leading_sign": 1,
    "domain_break": "odd"
   },
   "completes": "ex-1",
   "stem": {
    "text": "Signs of f' on (-oo, -1), (-1, 1), (1, 3), (3, oo): -, +, -, +. Where is f increasing?",
    "command_verb": "find"
   },
   "key": {
    "form": "symbolic",
    "expr": "Union(Interval.open(-1, 1), Interval.open(3, oo))"
   },
   "steps": [
    {
     "text": "The positive pieces.",
     "expr": "Union(Interval.open(-1, 1), Interval.open(3, oo))",
     "relation": "new"
    }
   ],
   "calculator_status": "no_calculator",
   "skills": [
    "BC-SKL-05016"
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
   "archetype_id": "BC-QA-05008",
   "parameter_draw": {
    "first_zero": -2,
    "second_zero": 2,
    "gap": 0,
    "scale": 1,
    "direction": "decreasing",
    "leading_sign": 1,
    "domain_break": "none"
   },
   "stem": {
    "text": "f'(x) = (x + 2)(x - 2). On what open intervals is f decreasing?",
    "command_verb": "find"
   },
   "key": {
    "form": "symbolic",
    "expr": "Interval.open(-2, 2)"
   },
   "steps": [
    {
     "text": "Zeros.",
     "expr": "(x + 2)*(x - 2) = 0",
     "relation": "new"
    },
    {
     "text": "x = -2, 2.",
     "expr": "FiniteSet(-2, 2)",
     "relation": "solve",
     "variable": "x"
    },
    {
     "text": "f'(0) = -4 < 0.",
     "expr": "Interval.open(-2, 2)",
     "relation": "new"
    }
   ],
   "calculator_status": "no_calculator",
   "skills": [
    "BC-SKL-05014",
    "BC-SKL-05016"
   ]
  },
  {
   "id": "chk-3",
   "check_kind": "mcq",
   "format": "mcq",
   "bands": [
    "low"
   ],
   "archetype_id": "BC-QA-05008",
   "parameter_draw": {
    "first_zero": 0,
    "second_zero": 4,
    "gap": 2,
    "scale": 1,
    "direction": "increasing",
    "leading_sign": 1,
    "domain_break": "odd"
   },
   "stem": {
    "text": "f is undefined at x = 2 and f'(x) = x(x - 4)/(x - 2). Where is f increasing?",
    "command_verb": "identify"
   },
   "key": {
    "form": "symbolic",
    "expr": "Union(Interval.open(0, 2), Interval.open(4, oo))"
   },
   "steps": [
    {
     "text": "Zeros.",
     "expr": "x*(x - 4) = 0",
     "relation": "new"
    },
    {
     "text": "x = 0, 4.",
     "expr": "FiniteSet(0, 4)",
     "relation": "solve",
     "variable": "x"
    },
    {
     "text": "Split also at 2; positive on (0, 2) and (4, oo).",
     "expr": "Union(Interval.open(0, 2), Interval.open(4, oo))",
     "relation": "new"
    }
   ],
   "options": [
    {
     "id": "A",
     "is_key": false,
     "expr": "Union(Interval.open(-oo, 0), Interval.open(0, 2), Interval.open(4, oo))",
     "error_path": "BC-ERR-05014",
     "derivation": "the sign on (-oo, 0) misread as positive"
    },
    {
     "id": "B",
     "is_key": true,
     "expr": "Union(Interval.open(0, 2), Interval.open(4, oo))",
     "error_path": null
    },
    {
     "id": "C",
     "is_key": false,
     "expr": "Union(Interval.open(-oo, 2), Interval.open(2, oo))",
     "error_path": "BC-ERR-05016",
     "derivation": "where f' rises: f''(x) = (x^2 - 4x + 8)/(x - 2)^2 > 0"
    },
    {
     "id": "D",
     "is_key": false,
     "expr": "Union(Interval.open(0, 4), Interval.open(4, oo))",
     "error_path": "BC-ERR-05017",
     "derivation": "x = 2 left off the partition"
    }
   ],
   "calculator_status": "no_calculator",
   "skills": [
    "BC-SKL-05014",
    "BC-SKL-05018"
   ]
  }
 ],
 "delivery": [
  {
   "block": "orientation",
   "mode": "figure",
   "reason": "rule 3: BC-REP-02 on BC-SKL-05015; unit README delivery map",
   "sources": [
    "BC-SKL-05015"
   ],
   "spec": {
    "kind": "graph",
    "representations": [
     "BC-REP-02"
    ],
    "curve": "f'(x) = 2(x + 1)(x - 3)/(x - 1)",
    "window": {
     "x": [
      -3,
      6
     ],
     "y": [
      -15,
      15
     ]
    },
    "shade": "where f' > 0",
    "labels": [
     {
      "text": "f' > 0: f increasing",
      "placement": "inside"
     },
     {
      "text": "f' < 0: f decreasing",
      "placement": "inside"
     },
     {
      "text": "x = 1: f undefined",
      "placement": "inside"
     }
    ]
   },
   "fallback": "the same graph static with the shading and labels",
   "keyboard": "no control; the figure description is reached with Tab"
  },
  {
   "block": "ki-1",
   "mode": "interactive",
   "reason": "rule 3 promoted: BC-REP-02 on BC-SKL-05015; BC-QA-05008 difficulty_variables whether the derivative changes sign at an undefined point, and the stem asks for a reading of intervals",
   "sources": [
    "BC-SKL-05015",
    "BC-QA-05008"
   ],
   "spec": {
    "kind": "graph",
    "representations": [
     "BC-REP-02"
    ],
    "curve": "f'(x) = 2(x + 1)(x - 3)/(x - 1)",
    "window": {
     "x": [
      -3,
      6
     ],
     "y": [
      -15,
      15
     ]
    },
    "controls": [
     {
      "type": "draggable_point",
      "constrained_to": "curve",
      "start": [
       -2,
       -3.33
      ],
      "exclude": [
       1
      ]
     }
    ],
    "readout": "sign of f' at the point",
    "question": "Is f rising here?",
    "labels": [
     {
      "text": "graph of f'",
      "placement": "inside"
     },
     {
      "text": "x = 1: no point",
      "placement": "inside"
     }
    ]
   },
   "fallback": "three static frames with the point at x = -2, 0 and 2, the sign of f' and the answer beside each",
   "keyboard": "Tab focuses the point; Left and Right arrow keys move it by 0.1; Enter reads the sign of f' aloud"
  },
  {
   "block": "ex-1",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  },
  {
   "block": "err-BC-ERR-05014",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  },
  {
   "block": "err-BC-ERR-05015",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  },
  {
   "block": "err-BC-ERR-05016",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  },
  {
   "block": "err-BC-ERR-05017",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  }
 ],
 "refresher": [
  "ki-1",
  "err-BC-ERR-05014",
  "err-BC-ERR-05015",
  "err-BC-ERR-05016",
  "err-BC-ERR-05017",
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
   "claim": "BC-QA-05008 has calculator_status either, so the lesson places it in Section I Part A.",
   "settles": "A calculator_status of calculator or no_calculator on BC-QA-05008."
  },
  {
   "claim": "The reason point for a monotonicity interval is scored as the concavity reason is (sg-23:14), by the research's analogy.",
   "settles": "A released scoring guideline for a monotonicity interval part."
  },
  {
   "claim": "The orientation is a static figure and ki-1 an interactive draggable point.",
   "settles": "The modality A/B in the build plan: skip rate and time to first credited success by mode."
  }
 ],
 "sources": [
  "BC-CON-05004",
  "BC-EK-FUN-4A1",
  "ced:101",
  "BC-QA-05008",
  "BC-PT-99063",
  "BC-PT-99005",
  "BC-PT-99010",
  "sg-25:17",
  "sg-23:14",
  "BC-ERR-05014",
  "BC-ERR-05015",
  "BC-ERR-05016",
  "BC-ERR-05017",
  "BC-MIS-05011",
  "BC-MIS-05012",
  "BC-MIS-05020",
  "BC-PRQ-05001",
  "BC-PRQ-05002",
  "BC-PRQ-05003",
  "BC-PRQ-05006",
  "research/units/unit-05-analytical-applications-differentiation.md#5.3 Determining Intervals on Which a Function is Increasing or Decreasing",
  "research/question-analysis/question-archetypes.md#BC-QA-05008 Intervals of increase or decrease justified by the sign of the derivative",
  "research/scoring/justification-requirements.md#Sign analysis of a derivative",
  "research/scoring/justification-requirements.md#Reasons tied to the object the prompt names",
  "research/scoring/common-point-losses.md#Notation points",
  "research/exam/exam-structure.md#Section and part layout"
 ],
 "word_count": {
  "full": 581,
  "brief": 446
 },
 "read_minutes": {
  "full": 3.9,
  "brief": 3.0
 }
}
```
