---
title: LSN-CON-01005 Ways a limit can fail to exist
research_date: 2026-09-29
status: designed
purpose: Authoring spec for the concept lesson on BC-CON-01005, the three ways a limit fails to exist (sides that disagree, unbounded values, oscillation), built from authoring_bundle("BC-CON-01005") and the research files it cites, so an author fills plan 15's lesson record without making a teaching decision.
---

# LSN-CON-01005 Ways a limit can fail to exist

Concept BC-CON-01005 (skills BC-SKL-01011, BC-SKL-01012, BC-SKL-01013), topics 1.3 and 1.4 of Unit 1, loaded by one archetype, BC-QA-01001 (family limit-from-graph). Its hard parent is BC-CON-01004 (docs/lessons/unit-01/README.md, section 1).

## Orientation

Served text, from BC-CON-01005 `description_plain` and the topic 1.3 Assessment behaviour paragraph, which asks which failure mode applies and for a reason for a nonexistence claim (research/units/unit-01-limits-continuity.md#1.3 Estimating Limit Values from Graphs). No count, no frequency.

## Key ideas

All three skills map one BC-EK, BC-EK-LIM-1C4 (ced:40), so one core block, both bands.

- ki-1 (core, BC-EK-LIM-1C4). A limit fails to exist when the one sided limits differ, when the values grow without bound, or when they keep oscillating; the CED illustrates the three with a reciprocal square, a reciprocal and a sine of a reciprocal (ced:40, via the topic 1.3 Failure modes paragraph). No quote, to hold the brief band at its cap. Notation from the concept record: does not exist.

## Recognition

- BC-QA-01001 (research/question-analysis/question-archetypes.md#BC-QA-01001 Limit estimated from a graph including one sided values): `typical_wording` "Using the graph of f shown, find the stated limits or explain why a limit does not exist"; `common_givens` a graph with one or more breaks; `asked_to_produce` includes "a statement that a limit does not exist with a reason". The signal is the phrase "or explain why", or a graph where the curve jumps, rises without bound, or wiggles faster near the input. `difficulty_variables` include "whether an infinite branch is included" and "whether a nonexistence answer must be justified". Official example BC-MCQ-CED-011.

What says "not this concept": two sides heading to one height at an open circle is a limit that exists (BC-CON-01002); a stem asking for the sign of an infinite limit or an asymptote belongs to BC-CON-01016.

## Method choice

One strategy block, both bands.

- st-1, BC-QA-01001. Cue from `asked_to_produce` and `common_givens`. Method, `expected_solution_path[0]`: locate the named input, then read each side. Rival, `wrong_approaches`: one side read and reported as the two sided limit (BC-ERR-01002). Separating feature: the reason names the failure mode, which of the three.

The archetype carries `asked_to_produce` and `common_givens` in the snapshot, so the block is verified.

## Solution path

- ex-1, BC-QA-01001, both bands, no calculator. Draw: hole_x 3, jump_x 5, start_y 2, hole_y -2, hole_value 1, left_limit 4, right_limit 0, end_y -3, jump_value 2, value_mark marked, justify justified, request jump. Near \(x=5\) the left segment is \(3x-11\) and the right \(5-x\). Steps: each branch (valued, new) and its one sided limit (valued), then the reason naming the failure mode (no value). Answer: a statement, the limit does not exist because the one sided limits, 4 and 0, differ.

The parameter spec builds only jumps and removable breaks, so the unbounded and oscillating modes are shown on the CED's own illustrations in the error blocks and chk-3 [inferred]. A fluent solver writes the two one sided heights and one sentence naming the mode (docs/lessons/unit-01/README.md, section 5).

## Scoring

None. BC-QA-01001 lists no `point_types`, so the lesson carries no scoring entry and says nothing about points (plan 15, R14).

## Traps

Three active errors, in the bundle's order; the mid band shows the first two.

- err-BC-ERR-01002 (BC-MIS-01002, BC-MIS-01001). On ex-1's draw: the left height 4 reported as the limit. Right: the limit does not exist (expr `DNE`). Distinct. Possible reason from BC-MIS-01002.
- err-BC-ERR-01020 (BC-MIS-01012, BC-MIS-99008). On the CED illustration \(1/x^2\) at 0 (ced:40): the limit written as infinity and read as existing (expr `oo`). Right: no real limit, the values grow without bound. Distinct. Possible reason from BC-MIS-01012.
- err-BC-ERR-01004 (BC-MIS-01004, BC-MIS-01003). On the CED illustration \(\sin(1/x)\) at 0 (ced:40): the value 1 reported as the limit. Right: no limit. Distinct. No possible reason: the linked descriptions speak of tables and of attaining a value, not of a graph that oscillates.

## Representations

None. The topic 1.3 Representations paragraph names graph to limit statement and graph to a verbal description of nonexistence, carried by the orientation figure and ki-1's motion.

## Prerequisite bridge

Four bridges, gated by state: BC-PRQ-01003 and BC-PRQ-01006 (supporting parents of BC-SKL-01011), BC-PRQ-01009 (of BC-SKL-01012), BC-PRQ-01005 (of BC-SKL-01013), each from its `description_plain` and `failure_signature`.

## Time

BC-QA-01001 is `no_calculator`, a single MCQ or one part of a larger question: Section I Part A, 2.14 minutes (research/exam/exam-structure.md#Section and part layout). On a justified part the minutes go to the two one sided readings and the one-sentence reason.

## Checks

- chk-1, completion of ex-1, both bands: the heights 4 and 0 are given, the student states the result with its mode. Key: does not exist.
- chk-2, isomorph on BC-QA-01001, both bands: jump at \(x=6\), heights \(-1\) and 2. Key: does not exist.
- chk-3, MCQ on BC-QA-01001, low band: \(f(x)=\sin(1/x)\) left of 0 and \(x+2\) right of 0 (outside the spec, [inferred]). Key: does not exist. Distractors: 2 (BC-ERR-01002, the right side reported), 1 and \(-1\) (BC-ERR-01004, a value the oscillation reaches).

## Delivery

- orientation: figure. Rule 3, BC-REP-02 on all three skills; the unit README picks figure for jump and unbounded. Two panels, ex-1's jump and \(1/x^2\) near 0 (two representations, the cap).
- ki-1: motion. Rule 2, the window narrowing on \(\sin(1/x)\) near 0, the oscillation never settling; the unit README names motion for oscillation.
- ex-1, err blocks: step_reveal, rule 1.

Every non-text choice is [inferred], settled by the modality A/B.

## Band plan

- Low (full): orientation, ki-1, st-1, ex-1, three error blocks, chk-1, chk-2, chk-3, bridges when gated.
- Mid (brief): orientation, ki-1, st-1, ex-1, err-BC-ERR-01002, err-BC-ERR-01020, chk-1, chk-2, bridges when gated.
- Totals: full 529 words, 3.6 minutes (cap 900 and 6); brief 450 words, 3.0 minutes (cap 450 and 3).
- Refresher: ki-1, the three error blocks, ex-1.

## Sources

- BC-CON-01005; BC-SKL-01011, BC-SKL-01012, BC-SKL-01013; BC-EK-LIM-1C4; ced:40
- BC-QA-01001; BC-MCQ-CED-011
- BC-ERR-01002, BC-ERR-01020, BC-ERR-01004; BC-MIS-01001, BC-MIS-01002, BC-MIS-01003, BC-MIS-01004, BC-MIS-01012, BC-MIS-99008
- BC-PRQ-01003, BC-PRQ-01005, BC-PRQ-01006, BC-PRQ-01009
- research/units/unit-01-limits-continuity.md#1.3 Estimating Limit Values from Graphs
- research/question-analysis/question-archetypes.md#BC-QA-01001 Limit estimated from a graph including one sided values
- research/exam/exam-structure.md#Section and part layout
- [inferred] The unbounded and oscillating cases sit on the CED illustrations and on a chk-3 graph outside BC-QA-01001's parameter_spec. Settled by a spec parameter for an infinite or oscillating branch.
- [inferred] Figure and motion as delivery modes. Settled by the modality A/B.
- Library gap: BC-QA-01001 `parameter_spec` has no parameter for an infinite branch, although its `difficulty_variables` name one.

## Machine record

```json
{
 "id": "LSN-CON-01005",
 "kind": "concept",
 "target_id": "BC-CON-01005",
 "unit": "01",
 "skills": [
  "BC-SKL-01011",
  "BC-SKL-01012",
  "BC-SKL-01013"
 ],
 "orientation": {
  "text": "A response that says a limit does not exist names why: sides that differ, values unbounded, or values oscillating. Stems give a graph and ask for the limit or the reason.",
  "sources": [
   "BC-CON-01005",
   "research/units/unit-01-limits-continuity.md#1.3 Estimating Limit Values from Graphs"
  ]
 },
 "key_ideas": [
  {
   "id": "ki-1",
   "ek_id": "BC-EK-LIM-1C4",
   "depth": "core",
   "text": "Three failure modes (BC-EK-LIM-1C4, ced:40): sides that differ, as |x|/x at 0 from each side; values unbounded, as 1/x^2 at 0; values oscillating, as sin(1/x) at 0. Each needs its mode named.",
   "notation": "does not exist",
   "quote": null,
   "sources": [
    "BC-EK-LIM-1C4",
    "ced:40",
    "research/units/unit-01-limits-continuity.md#1.3 Estimating Limit Values from Graphs"
   ]
  }
 ],
 "strategy": [
  {
   "id": "st-1",
   "archetype_id": "BC-QA-01001",
   "cue": "A graph with breaks and the words or explain why a limit does not exist.",
   "method": "First line: locate the input, then read each side.",
   "rival": "One side reported as the two sided limit (BC-ERR-01002).",
   "separating_feature": "The reason names which of the three modes applies.",
   "sources": [
    "BC-QA-01001"
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
    "hole_x": 3,
    "jump_x": 5,
    "start_y": 2,
    "hole_y": -2,
    "hole_value": 1,
    "left_limit": 4,
    "right_limit": 0,
    "end_y": -3,
    "jump_value": 2,
    "value_mark": "marked",
    "justify": "justified",
    "request": "jump"
   },
   "problem": {
    "text": "f has a segment (3, -2) to (5, 4), open at (5, 4), a segment (5, 0) to (8, -3), and a dot at (5, 2). Find the limit at x = 5 or explain why it does not exist.",
    "command_verb": "explain"
   },
   "calculator_status": "no_calculator",
   "steps": [
    {
     "cue": "Left of 5 the segment rises to (5, 4).",
     "why": "There f(x) = 3x - 11.",
     "expr": "3*x - 11",
     "relation": "new"
    },
    {
     "cue": "Read the left height.",
     "why": "It heads to 4.",
     "expr": "4",
     "relation": "limit",
     "variable": "x",
     "point": "5",
     "dir": "-"
    },
    {
     "cue": "Right of 5 the segment starts at (5, 0).",
     "why": "There f(x) = 5 - x.",
     "expr": "5 - x",
     "relation": "new"
    },
    {
     "cue": "Read the right height.",
     "why": "It heads to 0.",
     "expr": "0",
     "relation": "limit",
     "variable": "x",
     "point": "5",
     "dir": "+"
    },
    {
     "cue": "The stem says explain why: name the mode.",
     "why": "Sides differ, 4 and 0: no limit. The dot at 2 plays no part."
    }
   ],
   "answer": {
    "form": "statement",
    "expr": "DNE",
    "text": "The limit does not exist because the left hand limit 4 and the right hand limit 0 differ."
   }
  }
 ],
 "what_a_reader_scores": [],
 "common_errors": [
  {
   "error_id": "BC-ERR-01002",
   "observed_behavior": "The response reports the value approached from one side as the limit although the two sides differ.",
   "scoring_consequence": "The value point is lost because the correct response is that the limit does not exist.",
   "wrong_step": {
    "text": "The left height 4 reported as the limit.",
    "expr": "4"
   },
   "right_step": {
    "text": "Sides 4 and 0 differ: no limit.",
    "expr": "DNE"
   },
   "relation": "distinct",
   "possible_reason": {
    "misconception_id": "BC-MIS-01002",
    "text": "a single one sided approach as sufficient"
   },
   "sources": [
    "BC-ERR-01002",
    "BC-MIS-01002"
   ]
  },
  {
   "error_id": "BC-ERR-01020",
   "observed_behavior": "The response writes that the limit equals infinity and then treats that statement as an existence claim for a real limit.",
   "scoring_consequence": "A point requiring a statement about existence is lost.",
   "wrong_step": {
    "text": "For 1/x^2 at 0: the limit is infinity, so it exists.",
    "expr": "oo"
   },
   "right_step": {
    "text": "The values grow without bound: no real limit.",
    "expr": "DNE"
   },
   "relation": "distinct",
   "possible_reason": {
    "misconception_id": "BC-MIS-01012",
    "text": "reads the infinity symbol as a real value"
   },
   "sources": [
    "BC-ERR-01020",
    "BC-MIS-01012"
   ]
  },
  {
   "error_id": "BC-ERR-01004",
   "observed_behavior": "The response reports one of the values the function oscillates between as the limit near the input.",
   "scoring_consequence": "The value point is lost because no limit exists.",
   "wrong_step": {
    "text": "For sin(1/x) at 0: 1 reported as the limit.",
    "expr": "1"
   },
   "right_step": {
    "text": "The values keep swinging between -1 and 1: no limit.",
    "expr": "DNE"
   },
   "relation": "distinct",
   "possible_reason": null,
   "sources": [
    "BC-ERR-01004"
   ]
  }
 ],
 "representations": null,
 "prerequisite_bridges": [
  {
   "prq_id": "BC-PRQ-01003",
   "text": "Piecewise rules: pick the branch whose condition holds. The failure: the wrong branch at a boundary."
  },
  {
   "prq_id": "BC-PRQ-01006",
   "text": "An absolute value splits into two branches. The failure: its two one sided limits treated as equal."
  },
  {
   "prq_id": "BC-PRQ-01009",
   "text": "The sign of a quotient on each side of a zero of its denominator. The failure: one infinite limit written where the signs differ."
  },
  {
   "prq_id": "BC-PRQ-01005",
   "text": "Sine and cosine stay between -1 and 1. The failure: an oscillating factor treated as unbounded."
  }
 ],
 "time": {
  "exam_part": "I-A",
  "budget_minutes": 2.14,
  "source": "research/exam/exam-structure.md#Section and part layout",
  "written_steps": {
   "ex-1": [
    2,
    4,
    5
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
   "archetype_id": "BC-QA-01001",
   "parameter_draw": {
    "hole_x": 3,
    "jump_x": 5,
    "start_y": 2,
    "hole_y": -2,
    "hole_value": 1,
    "left_limit": 4,
    "right_limit": 0,
    "end_y": -3,
    "jump_value": 2,
    "value_mark": "marked",
    "justify": "justified",
    "request": "jump"
   },
   "completes": "ex-1",
   "stem": {
    "text": "In ex-1 the left height at x = 5 is 4, the right 0. State the limit and why.",
    "command_verb": "state"
   },
   "key": {
    "form": "statement",
    "expr": "DNE",
    "text": "The limit does not exist; the one sided limits differ."
   },
   "steps": [
    {
     "text": "Left 4.",
     "expr": "4",
     "relation": "new"
    },
    {
     "text": "Right 0.",
     "expr": "0",
     "relation": "new"
    }
   ],
   "calculator_status": "no_calculator",
   "skills": [
    "BC-SKL-01011"
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
    "start_y": 0,
    "hole_y": 3,
    "hole_value": -3,
    "left_limit": -1,
    "right_limit": 2,
    "end_y": 4,
    "jump_value": 3,
    "value_mark": "unmarked",
    "justify": "bare",
    "request": "jump"
   },
   "stem": {
    "text": "f has a segment (1, 3) to (6, -1), open at (6, -1), and a segment (6, 2) to (8, 4). Find the limit at x = 6 or explain.",
    "command_verb": "find"
   },
   "key": {
    "form": "statement",
    "expr": "DNE",
    "text": "The limit does not exist; the sides give -1 and 2."
   },
   "steps": [
    {
     "text": "Left piece (19 - 4x)/5.",
     "expr": "(19 - 4*x)/5",
     "relation": "new"
    },
    {
     "text": "It heads to -1.",
     "expr": "-1",
     "relation": "limit",
     "variable": "x",
     "point": "6",
     "dir": "-"
    },
    {
     "text": "Right piece x - 4.",
     "expr": "x - 4",
     "relation": "new"
    },
    {
     "text": "It heads to 2.",
     "expr": "2",
     "relation": "limit",
     "variable": "x",
     "point": "6",
     "dir": "+"
    }
   ],
   "calculator_status": "no_calculator",
   "skills": [
    "BC-SKL-01011"
   ]
  },
  {
   "id": "chk-3",
   "check_kind": "mcq",
   "format": "mcq",
   "bands": [
    "low"
   ],
   "archetype_id": "BC-QA-01001",
   "parameter_draw": {
    "left_branch": "sin(1/x)",
    "right_branch": "x + 2",
    "input": 0
   },
   "stem": {
    "text": "The graph of f is sin(1/x) left of 0 and x + 2 right of 0. What is the limit of f at x = 0?",
    "command_verb": "find"
   },
   "key": {
    "form": "statement",
    "expr": "DNE",
    "text": "The limit does not exist."
   },
   "steps": [
    {
     "text": "Right piece x + 2.",
     "expr": "x + 2",
     "relation": "new"
    },
    {
     "text": "It heads to 2; the left side oscillates.",
     "expr": "2",
     "relation": "limit",
     "variable": "x",
     "point": "0",
     "dir": "+"
    }
   ],
   "options": [
    {
     "id": "A",
     "is_key": false,
     "label": "2",
     "error_path": "BC-ERR-01002",
     "derivation": "the right side reported as the two sided limit"
    },
    {
     "id": "B",
     "is_key": false,
     "label": "1",
     "error_path": "BC-ERR-01004",
     "derivation": "a value the oscillation reaches reported as the limit"
    },
    {
     "id": "C",
     "is_key": true,
     "label": "The limit does not exist",
     "error_path": null
    },
    {
     "id": "D",
     "is_key": false,
     "label": "-1",
     "error_path": "BC-ERR-01004",
     "derivation": "the other value the oscillation reaches"
    }
   ],
   "calculator_status": "no_calculator",
   "skills": [
    "BC-SKL-01013",
    "BC-SKL-01011"
   ]
  }
 ],
 "delivery": [
  {
   "block": "orientation",
   "mode": "figure",
   "reason": "rule 3: BC-REP-02 on BC-SKL-01011 and BC-SKL-01012; unit README delivery map",
   "sources": [
    "BC-SKL-01011",
    "BC-SKL-01012"
   ],
   "spec": {
    "kind": "graph_pair",
    "representations": [
     "jump graph",
     "unbounded graph"
    ],
    "panels": [
     {
      "curves": [
       {
        "expr": "3*x - 11",
        "domain": [
         3,
         5
        ]
       },
       {
        "expr": "5 - x",
        "domain": [
         5,
         8
        ]
       }
      ],
      "points": [
       {
        "at": [
         5,
         4
        ],
        "style": "open"
       },
       {
        "at": [
         5,
         2
        ],
        "style": "filled"
       }
      ]
     },
     {
      "curves": [
       {
        "expr": "1/x**2",
        "domain": [
         -2,
         2
        ],
        "exclude": [
         0
        ]
       }
      ],
      "window": {
       "y": [
        0,
        20
       ]
      }
     }
    ],
    "labels": [
     {
      "text": "sides differ: 4 and 0",
      "placement": "inside"
     },
     {
      "text": "unbounded at 0",
      "placement": "inside"
     }
    ]
   },
   "fallback": "both panels static side by side with their labels",
   "keyboard": "no control; the figure description is reached with Tab"
  },
  {
   "block": "ki-1",
   "mode": "motion",
   "reason": "rule 2: a window narrowing toward the input on an oscillating function (BC-SKL-01013)",
   "sources": [
    "BC-SKL-01013"
   ],
   "spec": {
    "kind": "graph_zoom",
    "curves": [
     {
      "expr": "sin(1/x)",
      "exclude": [
       0
      ]
     }
    ],
    "parameter": {
     "name": "half_width",
     "frames": [
      1,
      0.1,
      0.01,
      0.001
     ]
    },
    "window": {
     "y": [
      -1.2,
      1.2
     ]
    },
    "labels": [
     {
      "text": "sin(1/x) near 0",
      "placement": "inside"
     },
     {
      "text": "still between -1 and 1: no single height",
      "placement": "inside"
     }
    ]
   },
   "fallback": "four static frames at half widths 1, 0.1, 0.01 and 0.001, labels inside each",
   "keyboard": "Right and Left arrow keys step the frames; Space pauses auto-advance",
   "reduced_motion": "no auto-advance; each key press cross-fades to the next frame"
  },
  {
   "block": "ex-1",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  },
  {
   "block": "err-BC-ERR-01002",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  },
  {
   "block": "err-BC-ERR-01020",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  },
  {
   "block": "err-BC-ERR-01004",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  }
 ],
 "refresher": [
  "ki-1",
  "err-BC-ERR-01002",
  "err-BC-ERR-01020",
  "err-BC-ERR-01004",
  "ex-1"
 ],
 "read_minutes": {
  "full": 3.6,
  "brief": 3.0
 },
 "word_count": {
  "full": 529,
  "brief": 450
 },
 "research_lines": [
  {
   "file": "research/units/unit-01-limits-continuity.md",
   "line": "The CED illustrates all three with a reciprocal square, a reciprocal, and a sine of a reciprocal"
  }
 ],
 "inferred": [
  {
   "claim": "The unbounded and oscillating error blocks sit on the CED illustrations 1/x^2 and sin(1/x), and chk-3 on a graph outside BC-QA-01001's parameter_spec.",
   "settles": "A BC-QA-01001 spec parameter for an infinite or oscillating branch, which its difficulty_variables already name."
  },
  {
   "claim": "A fluent solver writes the two one sided heights and one sentence naming the mode.",
   "settles": "Timing of written against held steps in the modality A/B."
  },
  {
   "claim": "Figure and motion serve these blocks better than text.",
   "settles": "The modality A/B in the build plan: skip rate and time to first credited success by mode."
  }
 ],
 "sources": [
  "BC-CON-01005",
  "BC-SKL-01011",
  "BC-SKL-01012",
  "BC-SKL-01013",
  "BC-EK-LIM-1C4",
  "ced:40",
  "BC-QA-01001",
  "BC-ERR-01002",
  "BC-ERR-01020",
  "BC-ERR-01004",
  "BC-MIS-01002",
  "BC-MIS-01012",
  "BC-PRQ-01003",
  "BC-PRQ-01005",
  "BC-PRQ-01006",
  "BC-PRQ-01009",
  "research/units/unit-01-limits-continuity.md#1.3 Estimating Limit Values from Graphs",
  "research/exam/exam-structure.md#Section and part layout"
 ]
}
```
