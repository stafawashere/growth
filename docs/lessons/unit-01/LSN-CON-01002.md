---
title: LSN-CON-01002 The limit of a function at a point
research_date: 2026-09-29
status: designed
purpose: Authoring spec for the concept lesson on BC-CON-01002, the limit at a point as the value approached and not the value attained, built from authoring_bundle("BC-CON-01002") and the research files it cites, so an author fills plan 15's lesson record without making a teaching decision.
---

# LSN-CON-01002 The limit of a function at a point

Concept BC-CON-01002 (skills BC-SKL-01006, BC-SKL-01008), topics 1.2 to 1.4 of Unit 1, loaded by BC-QA-01001 (family limit-from-graph) and BC-QA-01013 (family representation-consistency). It is a root of the unit's concept order (docs/lessons/unit-01/README.md, section 1).

## Orientation

Served text, from BC-CON-01002 `description_plain` and the Assessment behaviour paragraphs of topics 1.2 and 1.3, which ask what a written statement claims, whether the function value matters, and for limits and function values at named inputs of a graph (research/units/unit-01-limits-continuity.md#1.2 Defining Limits and Using Limit Notation; research/units/unit-01-limits-continuity.md#1.3 Estimating Limit Values from Graphs). No count, no frequency.

## Key ideas

The two skills map two BC-EK on ced:39: BC-EK-LIM-1A1 (both skills) and BC-EK-LIM-1B1 (BC-SKL-01006).

- ki-1 (core, BC-EK-LIM-1A1). The limit is the real number the outputs can be made arbitrarily close to by taking inputs close to c and not equal to c; the value at c plays no part. Paraphrased from the topic 1.2 Definition paragraph. No quote, to hold the brief band under its cap. Notation from the concept record: lim as x approaches c of f(x) equals R.
- ki-2 (extended, BC-EK-LIM-1B1). A graph, a table and a written statement can carry the same limit claim. Anchor quote (13 words) from ced:39.

The epsilon delta definition is excluded from assessment (ced:39), so no block states it.

## Recognition

- BC-QA-01001 (research/question-analysis/question-archetypes.md#BC-QA-01001 Limit estimated from a graph including one sided values): `typical_wording` "Using the graph of f shown, find the stated limits or explain why a limit does not exist"; `common_givens` a graph of a function with one or more breaks; `asked_to_produce` two sided and one sided limits, function values at named inputs, a nonexistence statement with a reason. The signal is an open circle and a filled point at one input with the stem asking for both a limit and a value. Official example BC-MCQ-CED-011.
- BC-QA-01013 (research/question-analysis/question-archetypes.md#BC-QA-01013 Limit claim matched across graphical, numerical, and analytic representations): `typical_wording` "Which of the given representations is consistent with the stated limit behaviour of f at the named input?"; `common_givens` a limit fact in one representation and candidate representations. The signal is a stem that gives a limit statement and asks which picture, table or sentence matches it.

What says "not this concept": a superscript sign on the arrow or a stem naming a side asks for a one sided limit (BC-CON-01004); a stem asking whether f is continuous asks for the value, the limit and their comparison (BC-CON-01013), per the unit README's neighbour table.

## Method choice

Two strategy blocks, low band both, mid band st-1.

- st-1, BC-QA-01001. Cue from `common_givens` and `asked_to_produce`. Method, `expected_solution_path[0]`: locate the named input on the horizontal axis, then read each side. Rival, `wrong_approaches`: reading the plotted value (BC-ERR-01001) or calling the limit absent where f is undefined (BC-ERR-01003). Separating feature: the limit is read from the curve beside the input, the value from the dot at the input.
- st-2, BC-QA-01013. Method, `expected_solution_path[0]`: read the limit behaviour from the supplied representation. Rival, `wrong_approaches`: matching a one sided value to a two sided statement (BC-ERR-01002). Separating feature: a match keeps the input, the side and the value.

Both archetypes carry `asked_to_produce` and `common_givens` in the snapshot, so neither block is tagged inferred.

## Solution path

- ex-1, BC-QA-01001, both bands, no calculator. Draw: hole_x 2, jump_x 5, start_y 0, hole_y 3, hole_value -1, left_limit 4, right_limit 1, end_y 2, jump_value -2, value_mark marked, justify bare, request hole. Every constraint of the spec holds. The segments near \(x=2\) are \(f(x)=3x/2\) on the left and \(f(x)=(x+7)/3\) on the right, both heading to 3, with a filled point at \((2,-1)\). Steps follow `expected_solution_path`: the left branch (valued, new) and its one sided limit (valued, limit from the left), the right branch (valued, new) and its limit (valued, limit from the right), then the plotted value read separately (no value, since it is not the limit).

On an MCQ a fluent solver writes nothing and reads both sides in the head; on an FRQ part the two one sided values and the comparison are written (docs/lessons/unit-01/README.md, section 5) [inferred: settled by timing in the modality A/B].

## Scoring

None. BC-QA-01001 and BC-QA-01013 list no `point_types`, so the lesson carries no scoring entry, no step carries a point tag and the lesson says nothing about points (plan 15, R14).

## Traps

Two active errors, in the bundle's order, both served in both bands.

- err-BC-ERR-01001 (BC-MIS-01001, BC-MIS-01003). Wrong step on ex-1's draw: \(f(2)=-1\) reported as the limit. Right step: 3. Distinct. Possible reason from BC-MIS-01001: the limit is treated as another name for evaluation.
- err-BC-ERR-01003 (BC-MIS-01001, BC-MIS-01009). Wrong step on ex-1's draw with the filled point removed: the limit called nonexistent (expr `DNE`). Right step: 3. Distinct. Possible reason from BC-MIS-01001: a missing or displaced function value is read as a missing or displaced limit.

## Representations

None. The topic Representations paragraphs name BC-REP-01, 02 and 04 and the conversion from analytic notation to a statement about a graph; the orientation figure and ki-1's motion already carry the graph, so a third drawn block would pass the per-screen cap without a new reading.

## Prerequisite bridge

One bridge, BC-PRQ-06005 (supporting parent of both skills), gated by state.

## Time

BC-QA-01001 is `no_calculator` and a single MCQ or one part of a larger question, so the part is Section I Part A, 2.14 minutes per question (research/exam/exam-structure.md#Section and part layout). Inside that budget the reading is done without writing on an MCQ; the one sided heights are the only lines worth writing when the part is free response.

## Checks

- chk-1, completion of ex-1, both bands. Key 3, equal to ex-1's answer.
- chk-2, isomorph on BC-QA-01001, both bands: hole at \(x=1\), segments \(4x-2\) and \((12-2x)/5\), filled point \((1,4)\). Key 2.

Two checks only: the bundle holds two errors for this concept, and a 4-option MCQ needs three distractors each produced by an error block on one draw; BC-ERR-01001 and BC-ERR-01003 give two values (the plotted value and a nonexistence claim). Listed under inferred.

## Delivery

- orientation: figure. Rule 3, BC-REP-02 on BC-SKL-01008; the unit README's delivery map picks figure. The graph of ex-1's draw near \(x=2\), open circle at \((2,3)\), filled point at \((2,-1)\).
- ki-1: motion. Rule 2, a limit being taken: the window zooms toward \(x=2\) in four frames, the curve crowding on height 3 while the filled point stays at \(-1\).
- ki-2: text. Rule 5; BC-SKL-01006 carries BC-REP-04 and BC-REP-01 only.
- ex-1, err-BC-ERR-01001, err-BC-ERR-01003: step_reveal, rule 1.

Every non-text choice is [inferred], settled by the modality A/B.

## Band plan

- Low (full): orientation, ki-1, ki-2, st-1, st-2, ex-1, err-BC-ERR-01001, err-BC-ERR-01003, chk-1, chk-2, bridge when gated. 539 words, 3.6 minutes (cap 900 and 6).
- Mid (brief): orientation, ki-1, st-1, ex-1, both error blocks, chk-1, chk-2, bridge when gated. 448 words, 3.0 minutes (cap 450 and 3).
- Refresher: ki-1, err-BC-ERR-01001, err-BC-ERR-01003, ex-1.

## Sources

- BC-CON-01002; BC-SKL-01006, BC-SKL-01008; BC-EK-LIM-1A1, BC-EK-LIM-1B1; ced:39
- BC-QA-01001, BC-QA-01013; BC-MCQ-CED-011
- BC-ERR-01001, BC-ERR-01003, BC-ERR-01002; BC-MIS-01001, BC-MIS-01003, BC-MIS-01009
- BC-PRQ-06005
- research/units/unit-01-limits-continuity.md#1.2 Defining Limits and Using Limit Notation
- research/units/unit-01-limits-continuity.md#1.3 Estimating Limit Values from Graphs
- research/question-analysis/question-archetypes.md#BC-QA-01001 Limit estimated from a graph including one sided values
- research/question-analysis/question-archetypes.md#BC-QA-01013 Limit claim matched across graphical, numerical, and analytic representations
- research/exam/exam-structure.md#Section and part layout
- [inferred] Two checks, because two errors cannot give three distinct distractors on one draw. Settled by a third active error on BC-SKL-01006 or BC-SKL-01008.
- [inferred] Written and held steps. Settled by timing in the modality A/B.
- [inferred] Figure and motion as delivery modes. Settled by the modality A/B.
- Library gap: research/question-analysis/question-archetypes.md records no common givens or produced objects for BC-QA-01001 and BC-QA-01013, while the snapshot records hold both.

## Machine record

```json
{
 "id": "LSN-CON-01002",
 "kind": "concept",
 "target_id": "BC-CON-01002",
 "unit": "01",
 "skills": [
  "BC-SKL-01006",
  "BC-SKL-01008"
 ],
 "orientation": {
  "text": "A response reports the value f(x) approaches as x nears the input, kept apart from f at the input, which can differ or be missing. Stems give a graph or a limit statement.",
  "sources": [
   "BC-CON-01002",
   "research/units/unit-01-limits-continuity.md#1.2 Defining Limits and Using Limit Notation",
   "research/units/unit-01-limits-continuity.md#1.3 Estimating Limit Values from Graphs"
  ]
 },
 "key_ideas": [
  {
   "id": "ki-1",
   "ek_id": "BC-EK-LIM-1A1",
   "depth": "core",
   "text": "The limit of f(x) as x approaches c is the number R that f(x) gets arbitrarily close to for x near c, x not equal to c (BC-EK-LIM-1A1, ced:39). The value f(c) plays no part.",
   "notation": "lim as x approaches c of f(x) equals R",
   "quote": null,
   "sources": [
    "BC-EK-LIM-1A1",
    "ced:39"
   ]
  },
  {
   "id": "ki-2",
   "ek_id": "BC-EK-LIM-1B1",
   "depth": "extended",
   "text": "A graph, a table and a written statement can carry one limit claim; reading any of them means naming the input approached and the value approached (BC-EK-LIM-1B1, ced:39).",
   "notation": "",
   "quote": {
    "text": "A limit can be expressed in multiple ways, including graphically, numerically, and analytically.",
    "source": "ced:39"
   },
   "sources": [
    "BC-EK-LIM-1B1",
    "ced:39"
   ]
  }
 ],
 "strategy": [
  {
   "id": "st-1",
   "archetype_id": "BC-QA-01001",
   "cue": "A graph with breaks; limits or function values asked at named inputs.",
   "method": "First line: locate the input, then read each side's height.",
   "rival": "Reading the dot (BC-ERR-01001), or calling the limit absent where f is undefined (BC-ERR-01003).",
   "separating_feature": "The limit comes from the curve beside the input, the value from the dot.",
   "sources": [
    "BC-QA-01001"
   ],
   "evidence_tag": "verified"
  },
  {
   "id": "st-2",
   "archetype_id": "BC-QA-01013",
   "cue": "A limit fact in one representation, and candidate graphs, tables or expressions to match against it.",
   "method": "First line: read the limit behaviour from the supplied representation, in neutral words.",
   "rival": "Matching a one sided value to a two sided statement (BC-ERR-01002).",
   "separating_feature": "A match keeps the input, the side and the value.",
   "sources": [
    "BC-QA-01013"
   ],
   "evidence_tag": "verified"
  }
 ],
 "worked_examples": [
  {
   "id": "ex-1",
   "archetype_id": "BC-QA-01001",
   "bands": [
    "low",
    "mid"
   ],
   "parameter_draw": {
    "hole_x": 2,
    "jump_x": 5,
    "start_y": 0,
    "hole_y": 3,
    "hole_value": -1,
    "left_limit": 4,
    "right_limit": 1,
    "end_y": 2,
    "jump_value": -2,
    "value_mark": "marked",
    "justify": "bare",
    "request": "hole"
   },
   "problem": {
    "text": "The graph of f has segments (0, 0) to (2, 3) and (2, 3) to (5, 4), an open circle at (2, 3) and a dot at (2, -1). Find the limit of f at x = 2, and f(2).",
    "command_verb": "find"
   },
   "calculator_status": "no_calculator",
   "steps": [
    {
     "cue": "Left of x = 2 the segment starts at (0, 0).",
     "why": "There f(x) = 3x/2.",
     "expr": "3*x/2",
     "relation": "new"
    },
    {
     "cue": "Read the height approached from the left.",
     "why": "An open circle marks a height approached.",
     "expr": "3",
     "relation": "limit",
     "variable": "x",
     "point": "2",
     "dir": "-"
    },
    {
     "cue": "The right segment runs to (5, 4).",
     "why": "There f(x) = (x + 7)/3.",
     "expr": "(x + 7)/3",
     "relation": "new"
    },
    {
     "cue": "Read the height approached from the right.",
     "why": "Both sides give 3, so the limit is 3.",
     "expr": "3",
     "relation": "limit",
     "variable": "x",
     "point": "2",
     "dir": "+"
    },
    {
     "cue": "The stem also asks for f(2): the filled point.",
     "why": "f(2) = -1, a separate answer."
    }
   ],
   "answer": {
    "form": "numeric",
    "expr": "3"
   }
  }
 ],
 "what_a_reader_scores": [],
 "common_errors": [
  {
   "error_id": "BC-ERR-01001",
   "observed_behavior": "The response gives the plotted or defined value of the function at the input in place of the value the function approaches there.",
   "scoring_consequence": "The reading point is lost, and in a continuity part the comparison of limit with value collapses.",
   "wrong_step": {
    "text": "f(2) = -1 reported as the limit.",
    "expr": "-1"
   },
   "right_step": {
    "text": "Both sides head to 3.",
    "expr": "3"
   },
   "relation": "distinct",
   "possible_reason": {
    "misconception_id": "BC-MIS-01001",
    "text": "the limit as another name for evaluation"
   },
   "sources": [
    "BC-ERR-01001",
    "BC-MIS-01001"
   ]
  },
  {
   "error_id": "BC-ERR-01003",
   "observed_behavior": "The response states that the limit does not exist on the grounds that the function has no value at the input.",
   "scoring_consequence": "Both the value point and any justification point are lost.",
   "wrong_step": {
    "text": "With the dot removed, the limit is called nonexistent.",
    "expr": "DNE"
   },
   "right_step": {
    "text": "Both sides still head to 3.",
    "expr": "3"
   },
   "relation": "distinct",
   "possible_reason": {
    "misconception_id": "BC-MIS-01001",
    "text": "a missing or displaced function value is read as a missing or displaced limit"
   },
   "sources": [
    "BC-ERR-01003",
    "BC-MIS-01001"
   ]
  }
 ],
 "representations": null,
 "prerequisite_bridges": [
  {
   "prq_id": "BC-PRQ-06005",
   "text": "Graph reading rests on evaluating f at a stated input and telling f from its value at a point. The failure: a height read at the wrong input."
  }
 ],
 "time": {
  "exam_part": "I-A",
  "budget_minutes": 2.14,
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
    3,
    5
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
   "archetype_id": "BC-QA-01001",
   "parameter_draw": {
    "hole_x": 2,
    "jump_x": 5,
    "start_y": 0,
    "hole_y": 3,
    "hole_value": -1,
    "left_limit": 4,
    "right_limit": 1,
    "end_y": 2,
    "jump_value": -2,
    "value_mark": "marked",
    "justify": "bare",
    "request": "hole"
   },
   "completes": "ex-1",
   "stem": {
    "text": "Both segments of f head to height 3 at x = 2; the dot is at (2, -1). Write the limit of f at x = 2.",
    "command_verb": "write"
   },
   "key": {
    "form": "numeric",
    "expr": "3"
   },
   "steps": [
    {
     "text": "Left of 2, f(x) = 3x/2.",
     "expr": "3*x/2",
     "relation": "new"
    },
    {
     "text": "It heads to 3.",
     "expr": "3",
     "relation": "limit",
     "variable": "x",
     "point": "2",
     "dir": "-"
    }
   ],
   "calculator_status": "no_calculator",
   "skills": [
    "BC-SKL-01008"
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
   "archetype_id": "BC-QA-01001",
   "parameter_draw": {
    "hole_x": 1,
    "jump_x": 6,
    "start_y": -2,
    "hole_y": 2,
    "hole_value": 4,
    "left_limit": 0,
    "right_limit": 3,
    "end_y": -1,
    "jump_value": 1,
    "value_mark": "unmarked",
    "justify": "bare",
    "request": "hole"
   },
   "stem": {
    "text": "f has segments (0, -2) to (1, 2) and (1, 2) to (6, 0), an open circle at (1, 2), a dot at (1, 4). Find the limit of f at x = 1.",
    "command_verb": "find"
   },
   "key": {
    "form": "numeric",
    "expr": "2"
   },
   "steps": [
    {
     "text": "Left of 1, f(x) = 4x - 2.",
     "expr": "4*x - 2",
     "relation": "new"
    },
    {
     "text": "It heads to 2.",
     "expr": "2",
     "relation": "limit",
     "variable": "x",
     "point": "1",
     "dir": "-"
    },
    {
     "text": "Right of 1, f(x) = (12 - 2x)/5.",
     "expr": "(12 - 2*x)/5",
     "relation": "new"
    },
    {
     "text": "It also heads to 2.",
     "expr": "2",
     "relation": "limit",
     "variable": "x",
     "point": "1",
     "dir": "+"
    }
   ],
   "calculator_status": "no_calculator",
   "skills": [
    "BC-SKL-01008"
   ]
  }
 ],
 "delivery": [
  {
   "block": "orientation",
   "mode": "figure",
   "reason": "rule 3: BC-REP-02 on BC-SKL-01008; unit README delivery map",
   "sources": [
    "BC-SKL-01008"
   ],
   "spec": {
    "kind": "graph",
    "window": {
     "x": [
      0,
      5
     ],
     "y": [
      -2,
      5
     ]
    },
    "curves": [
     {
      "expr": "3*x/2",
      "domain": [
       0,
       2
      ]
     },
     {
      "expr": "(x + 7)/3",
      "domain": [
       2,
       5
      ]
     }
    ],
    "points": [
     {
      "at": [
       2,
       3
      ],
      "style": "open"
     },
     {
      "at": [
       2,
       -1
      ],
      "style": "filled"
     }
    ],
    "labels": [
     {
      "text": "height approached: 3",
      "placement": "inside"
     },
     {
      "text": "f(2) = -1",
      "placement": "inside"
     },
     {
      "text": "x = 2",
      "placement": "inside"
     }
    ]
   },
   "fallback": "the same graph as a static image with its labels, and a sentence naming the open circle and the filled point",
   "keyboard": "no control; the figure's description is reached with Tab"
  },
  {
   "block": "ki-1",
   "mode": "motion",
   "reason": "rule 2: a limit being taken, the window zooming toward the input (BC-SKL-01008)",
   "sources": [
    "BC-SKL-01008"
   ],
   "spec": {
    "kind": "graph_zoom",
    "curves": [
     {
      "expr": "3*x/2",
      "domain": [
       0,
       2
      ]
     },
     {
      "expr": "(x + 7)/3",
      "domain": [
       2,
       5
      ]
     }
    ],
    "points": [
     {
      "at": [
       2,
       3
      ],
      "style": "open"
     },
     {
      "at": [
       2,
       -1
      ],
      "style": "filled"
     }
    ],
    "parameter": {
     "name": "half_width",
     "frames": [
      2,
      1,
      0.5,
      0.1
     ]
    },
    "labels": [
     {
      "text": "outputs crowd on 3",
      "placement": "inside"
     },
     {
      "text": "f(2) = -1 stays apart",
      "placement": "inside"
     }
    ]
   },
   "fallback": "four static frames in a row at half widths 2, 1, 0.5 and 0.1, labels inside each",
   "keyboard": "Right and Left arrow keys step the frames; Space pauses auto-advance",
   "reduced_motion": "no auto-advance; each key press cross-fades to the next frame"
  },
  {
   "block": "ki-2",
   "mode": "text",
   "reason": "rule 5: BC-SKL-01006 carries BC-REP-04 and BC-REP-01 only",
   "sources": [
    "BC-SKL-01006"
   ]
  },
  {
   "block": "ex-1",
   "mode": "step_reveal",
   "reason": "rule 1; the graph of the draw sits above the steps",
   "sources": [
    "BC-SKL-01008"
   ]
  },
  {
   "block": "err-BC-ERR-01001",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  },
  {
   "block": "err-BC-ERR-01003",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  }
 ],
 "refresher": [
  "ki-1",
  "err-BC-ERR-01001",
  "err-BC-ERR-01003",
  "ex-1"
 ],
 "read_minutes": {
  "full": 3.6,
  "brief": 3.0
 },
 "word_count": {
  "full": 539,
  "brief": 448
 },
 "research_lines": [
  {
   "file": "research/units/unit-01-limits-continuity.md",
   "line": "Conceptual variants ask whether the function value matters"
  }
 ],
 "inferred": [
  {
   "claim": "Two checks: the two active errors give two distinct wrong values on one draw, short of the three distractors check 3 needs.",
   "settles": "A third active error on BC-SKL-01006 or BC-SKL-01008, or a published MCQ on BC-QA-01001 whose distractors carry these error paths."
  },
  {
   "claim": "On an MCQ a fluent solver writes no step; on a free response part the two one sided heights are written.",
   "settles": "Timing of written against held steps in the modality A/B."
  },
  {
   "claim": "Figure for the orientation and motion for ki-1 serve better than text.",
   "settles": "The modality A/B in the build plan: skip rate and time to first credited success by mode."
  }
 ],
 "sources": [
  "BC-CON-01002",
  "BC-SKL-01006",
  "BC-SKL-01008",
  "BC-EK-LIM-1A1",
  "BC-EK-LIM-1B1",
  "ced:39",
  "BC-QA-01001",
  "BC-QA-01013",
  "BC-MCQ-CED-011",
  "BC-ERR-01001",
  "BC-ERR-01003",
  "BC-MIS-01001",
  "BC-MIS-01003",
  "BC-MIS-01009",
  "BC-PRQ-06005",
  "research/units/unit-01-limits-continuity.md#1.2 Defining Limits and Using Limit Notation",
  "research/units/unit-01-limits-continuity.md#1.3 Estimating Limit Values from Graphs",
  "research/exam/exam-structure.md#Section and part layout"
 ]
}
```
