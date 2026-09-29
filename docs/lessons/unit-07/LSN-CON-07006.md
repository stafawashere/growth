---
title: LSN-CON-07006 Euler's method as repeated local linearisation
research_date: 2026-09-29
status: designed
purpose: Authoring spec for the concept lesson on BC-CON-07006, approximating a solution value by Euler steps of equal size, built from authoring_bundle("BC-CON-07006") and the research files it cites, so an author fills plan 15's lesson record without making a teaching decision.
---

# LSN-CON-07006 Euler's method as repeated local linearisation

Concept BC-CON-07006 (skills BC-SKL-07019 to BC-SKL-07023), topic 7.5 of Unit 7 (BC only), loaded by BC-QA-07004 and BC-QA-07005, both family euler. Hard parents BC-CON-07004 and BC-CON-07005 (docs/lessons/unit-07/README.md, section 1).

## Prediction

Both bands, served first, before any rule. Form `mcq`, three options, on ex-1's numbers: \(dy/dx=2x+y+1\) through \((0,1)\), the estimate of \(y(1/2)\) from the slope at the start. Key: 2, the starting value plus the slope times \(1/2\); the other options leave \(y\) at 1 or add the slope without the step. The resolution states what the tangent gives (\(1+\tfrac12(2)=2\)) and that Euler's method repeats it from each new point, and never grades the choice. Sources: BC-CON-07006 and the 7.5 topic section that ki-1 cites (BC-EK-FUN-7C4, ced:141). Delivery: text. [inferred] Settled by the prediction's first-try rate in the build plan.

## Orientation

Served text, from BC-CON-07006 `description_plain` and the topic's Assessment behaviour paragraph (research/units/unit-07-differential-equations.md#7.5 Approximating Solutions Using Euler's Method): a response computes the step size, then each new value as the old one plus the step times the slope at the current point, shown step by step or in a labelled table. No count, no frequency.

## Key ideas

The five skills map to BC-EK-FUN-7C4 (ced:141); BC-SKL-07023 is absent from the bundle's skill records but its snapshot record names the same EK (library gap). One core block, both bands, from the Procedure and Step size paragraphs. Anchor quote from ced:141.

## Recognition

BC-QA-07004 (research/question-analysis/question-archetypes.md#BC-QA-07004 Euler's method over two steps of equal size): `typical_wording` "use Euler's method, starting at the given input with two steps of equal size, to approximate ... show the computations"; `common_givens` an equation, an initial condition, a target input, a number of steps; `asked_to_produce` the step size, each increment, the approximation. Shapes: MCQ (BC-MCQ-SAMPLE-018, BC-MCQ-PE2012-016) and a 2 point FRQ part (BC-FRQ-2021-Q5-B, BC-FRQ-2024-Q5-C, BC-FRQ-2025-Q5-D). BC-QA-07005 (research/question-analysis/question-archetypes.md#BC-QA-07005 Direction of an approximation decided from the second derivative of a solution) follows it with "overestimate or underestimate".

What says "not this concept": "find the particular solution" selects separation (BC-CON-07007).

The contrast pair on st-1 sets an Euler stem beside its near miss. Where the near miss comes from: the `wrong_approaches` entry that solves the equation and evaluates, so the near-miss stem gives \(dy/dx=2xy\) with a point and asks for \(y(1)\), which calls for separation and an exact value. The separating feature is that Euler's method and equal steps are named.

## Method choice

One strategy block for the euler family, from BC-QA-07004: method `expected_solution_path[0]`, the step size; rival `wrong_approaches`, solving and evaluating; feature: "Euler's method" and "steps of equal size" in the stem. Not tagged inferred. The reader prints its own labels, so no field starts with one. The block carries the contrast pair: an Euler stem beside an exact-solution stem.

## Solution path

- ex-1, both bands. Draw: form both, x_coefficient 2, y_coefficient 1, constant 1, start_x 0, start_y 1, span 1: dy/dx = 2x + y + 1, y(0) = 1, two steps to x = 1. The spec's derived values: key 4, one_step 3, full_steps 9, target_slope_first 11/2, all distinct. No published draw matches.
- Steps: step size; slope at (0, 1); y1 = 2; slope at (1/2, 2); y2 = 4. Every step is written: the steps are the demonstration point. One example, so it is not faded and carries no `fade_from`.

## Scoring

BC-QA-07004 lists BC-PT-99034, 99004, 99005. ex-1 tags BC-PT-99034 on the first step; the line is reader_checks output. The answer tag (BC-PT-99005) is dropped to keep the brief band under 450 words [inferred]. A table needs labels when the answer is missing or wrong (research/scoring/notation-requirements.md#Labels; sg-25:23, sg-21:19). Wrong initial value, step size or slope is the recorded answer loss (research/scoring/common-point-losses.md#Answer points).

## Traps

Nine active errors meet the skills; the first four in the bundle's order: BC-ERR-07018, 07019, 07020, 07021. All on ex-1's draw. All four are distinct, so every block carries `fix_prompt` true. The texts write fractions (11/2, 7/2), so the expressions stay fractions. In BC-ERR-07020 and 07021 each line names the slope used and the resulting approximation of y(1), and the expression is that approximation (11/2 and 7/2 against 4). Possible reasons from BC-MIS-07010, 07011, 07012.

## Representations

The topic's Representations paragraph names equation plus initial condition to a table of approximations (BC-REP-06 to BC-REP-03): served as a model, the steps computed row by row.

## Prerequisite bridge

- BC-PRQ-07005, from `description_plain` and `failure_signature`.

## Time

BC-QA-07004 is `no_calculator`, one 2 point part of a free-response question, so Section II Part B, 15.0 minutes per question (research/exam/exam-structure.md#Section and part layout); 2 of 9 points, 3.33 minutes (docs/lessons/unit-07/README.md, section 5).

## Checks

- chk-1, completion of ex-1: y1 = 2 given. Key 4.
- chk-2, isomorph. Draw: x_only, x_coefficient 2, y_coefficient 1, constant -1, start (1, 3), span 1. Key 9/2.
- chk-3, MCQ, low band. Draw: both, 1, 2, 0, start (0, 1), span 1: dy/dx = x + 2y. Key 17/4. Distractors 3 (BC-ERR-07019), 21/4 (BC-ERR-07020), 13/4 (BC-ERR-07021).

## Delivery

- orientation: table. Rule 5: BC-REP-03 on BC-SKL-07019 to 07022.
- ki-1: motion. Rule 2: the new point replaces the old.
- representations: model. Rule 2: the computed sequence of approximations is the idea (docs/lessons/unit-07/README.md, section 6) [inferred].
- pr-1: text. Rule 6, a prediction on the worked example's numbers with nothing to draw.
- ex-1, error blocks: step_reveal. Rule 1.

Figure presence: the orientation table, the ki-1 motion and the representations model are drawn blocks, so the record carries no `no_figure_reason`.

## Band plan

- Low (full): prediction, orientation, bridge, ki-1, st-1 with its contrast, ex-1 with its line, chk-1, four error blocks, chk-2, representations, chk-3. 605 words, 4.1 minutes (cap 900 and 6).
- Mid (brief): prediction, orientation, bridge, ki-1, st-1 with its contrast, ex-1 with its line, chk-1, err-BC-ERR-07018, err-BC-ERR-07019, chk-2. 450 words, 3.0 minutes (cap 450 and 3). The orientation, ki-1 (text and notation), the bridge, the st-1 fields, the prediction and ex-1's cues were shortened to fit; the anchor quote and the scoring tag stay.
- Refresher: ki-1, the four error blocks, ex-1.

## Sources

- BC-CON-07006; BC-SKL-07019 to BC-SKL-07023; BC-EK-FUN-7C4; ced:141
- BC-QA-07004, BC-QA-07005; BC-MCQ-SAMPLE-018, BC-MCQ-PE2012-016, BC-FRQ-2021-Q5-B, BC-FRQ-2024-Q5-C, BC-FRQ-2025-Q5-D; BC-PT-99034, BC-PT-99005; sg-25:23, sg-21:19
- BC-ERR-07018, BC-ERR-07019, BC-ERR-07020, BC-ERR-07021; BC-MIS-07010, BC-MIS-07011, BC-MIS-07012
- BC-PRQ-07005
- research/units/unit-07-differential-equations.md#7.5 Approximating Solutions Using Euler's Method
- research/question-analysis/question-archetypes.md#BC-QA-07004 Euler's method over two steps of equal size
- research/question-analysis/question-archetypes.md#BC-QA-07005 Direction of an approximation decided from the second derivative of a solution
- research/scoring/notation-requirements.md#Labels
- research/scoring/common-point-losses.md#Answer points
- research/exam/exam-structure.md#Section and part layout
- [inferred] Table, motion and model modes. Settled by the modality A/B.

## Machine record

```json
{
 "id": "LSN-CON-07006",
 "kind": "concept",
 "target_id": "BC-CON-07006",
 "unit": "07",
 "skills": [
  "BC-SKL-07019",
  "BC-SKL-07020",
  "BC-SKL-07021",
  "BC-SKL-07022",
  "BC-SKL-07023"
 ],
 "prediction": {
  "id": "pr-1",
  "stem": {
   "text": "\\(dy/dx=2x+y+1\\) and \\(y(0)=1\\). Using the slope at the start, estimate \\(y(1/2)\\).",
   "command_verb": "predict"
  },
  "format": "mcq",
  "options": [
   {
    "id": "A",
    "label": "2: 1 plus slope times \\(1/2\\).",
    "is_key": true
   },
   {
    "id": "B",
    "label": "1: \\(y\\) stays put.",
    "is_key": false
   },
   {
    "id": "C",
    "label": "3: 1 plus the slope.",
    "is_key": false
   }
  ],
  "resolution": "The slope at \\((0,1)\\) is 2, so \\(1+\\tfrac12(2)=2\\). Euler's method repeats this at each new point.",
  "sources": [
   "BC-CON-07006",
   "BC-EK-FUN-7C4",
   "ced:141",
   "research/units/unit-07-differential-equations.md#7.5 Approximating Solutions Using Euler's Method"
  ]
 },
 "orientation": {
  "text": "Step size, then step times slope at each point. Show every step or a labelled table.",
  "sources": [
   "BC-CON-07006",
   "research/units/unit-07-differential-equations.md#7.5 Approximating Solutions Using Euler's Method"
  ]
 },
 "key_ideas": [
  {
   "id": "ki-1",
   "ek_id": "BC-EK-FUN-7C4",
   "depth": "core",
   "text": "Step size is interval length over steps. New y is old y plus step times the slope there; the new point replaces the old.",
   "notation": "step size",
   "quote": {
    "text": "Euler's method provides a procedure for approximating a solution to a differential equation or a point on a solution curve.",
    "source": "ced:141"
   },
   "sources": [
    "BC-EK-FUN-7C4",
    "ced:141",
    "research/units/unit-07-differential-equations.md#7.5 Approximating Solutions Using Euler's Method"
   ]
  }
 ],
 "strategy": [
  {
   "id": "st-1",
   "archetype_id": "BC-QA-07004",
   "cue": "Euler, equal steps, a target input.",
   "method": "The step size, then y1 = y0 + step times f(x0, y0).",
   "rival": "Solving the equation and evaluating.",
   "separating_feature": "The stem names Euler.",
   "sources": [
    "BC-QA-07004"
   ],
   "evidence_tag": "verified",
   "contrast": {
    "this": {
     "text": "\\(dy/dx=x+3y\\), \\(y(0)=2\\). Euler's method, two equal steps: approximate \\(y(1)\\).",
     "archetype_id": "BC-QA-07004"
    },
    "not_this": {
     "text": "\\(dy/dx=2xy\\), \\(y(0)=2\\). Find \\(y(1)\\).",
     "why_not": "Exact solution, by separation."
    },
    "feature": "Euler and equal steps are named."
   }
  }
 ],
 "worked_examples": [
  {
   "id": "ex-1",
   "archetype_id": "BC-QA-07004",
   "bands": [
    "low",
    "mid"
   ],
   "parameter_draw": {
    "form": "both",
    "x_coefficient": 2,
    "y_coefficient": 1,
    "constant": 1,
    "start_x": 0,
    "start_y": 1,
    "span": 1
   },
   "problem": {
    "text": "dy/dx = 2x + y + 1, y(0) = 1. Use Euler's method with two equal steps to approximate y(1).",
    "command_verb": "approximate"
   },
   "calculator_status": "no_calculator",
   "steps": [
    {
     "cue": "Two equal steps, 0 to 1.",
     "why": "1/2.",
     "expr": "1/2",
     "relation": "new"
    },
    {
     "cue": "Slope at the initial point.",
     "why": "At (0, 1).",
     "expr": "2*x + y + 1",
     "relation": "new"
    },
    {
     "cue": "Evaluate.",
     "why": "2.",
     "expr": "2",
     "relation": "evaluate",
     "subs": {
      "x": "0",
      "y": "1"
     }
    },
    {
     "cue": "Advance.",
     "why": "1 + (1/2)(2).",
     "expr": "2",
     "relation": "new",
     "point_type_id": "BC-PT-99034"
    },
    {
     "cue": "Slope at the new point.",
     "why": "It replaces the old.",
     "expr": "2*x + y + 1",
     "relation": "new"
    },
    {
     "cue": "Evaluate.",
     "why": "4.",
     "expr": "4",
     "relation": "evaluate",
     "subs": {
      "x": "1/2",
      "y": "2"
     }
    },
    {
     "cue": "Advance.",
     "why": "2 + (1/2)(4).",
     "expr": "4",
     "relation": "new"
    }
   ],
   "answer": {
    "form": "numeric",
    "expr": "4"
   }
  }
 ],
 "what_a_reader_scores": [
  {
   "example_id": "ex-1",
   "point_type_ids": [
    "BC-PT-99034"
   ],
   "lines": [
    {
     "point_type_id": "BC-PT-99034",
     "text": "Euler method step. Earned by: Demonstrating the required number of steps with the correct initial condition, correct step size, and the correct or imported derivative expression (sg-25:23, sg-21:19). Not earned by: A single step where two were asked for (sg-24:17); a table that is neither labelled nor accompanied by a correct answer (sg-25:23, sg-21:19). Notation: Steps may be explicit expressions or a table; sg-25:23 and sg-21:19 state an unlabelled table suffices when the answer is correct, and must be labelled when it is not."
    }
   ]
  }
 ],
 "common_errors": [
  {
   "error_id": "BC-ERR-07018",
   "observed_behavior": "The response argues that the estimate is high or low because the solution is increasing or decreasing.",
   "scoring_consequence": "The reason point is lost; the guideline requires the second derivative, the monotonicity of the first derivative, or the concavity.",
   "wrong_step": {
    "text": "Sign of dy/dx.",
    "expr": "2*x + y + 1"
   },
   "right_step": {
    "text": "Sign of the second derivative.",
    "expr": "2*x + y + 3"
   },
   "relation": "distinct",
   "possible_reason": {
    "misconception_id": "BC-MIS-07010",
    "text": "decides whether an estimate is high or low from the monotonicity of the solution rather than from its concavity"
   },
   "sources": [
    "BC-ERR-07018",
    "BC-MIS-07010"
   ],
   "fix_prompt": true
  },
  {
   "error_id": "BC-ERR-07019",
   "observed_behavior": "The response uses the full distance to the target input as one step although several equal steps were asked for.",
   "scoring_consequence": "The demonstration point is lost because the step size is wrong.",
   "wrong_step": {
    "text": "One step of 1.",
    "expr": "3"
   },
   "right_step": {
    "text": "Two of 1/2.",
    "expr": "4"
   },
   "relation": "distinct",
   "possible_reason": {
    "misconception_id": "BC-MIS-07011",
    "text": "treats the procedure as a single tangent line extended over the whole interval"
   },
   "sources": [
    "BC-ERR-07019",
    "BC-MIS-07011"
   ],
   "fix_prompt": true
  },
  {
   "error_id": "BC-ERR-07020",
   "observed_behavior": "The first step starts from a point other than the given initial condition, or evaluates the derivative at the target input.",
   "scoring_consequence": "The demonstration point is lost; the 2025 guideline names the correct initial condition as one of its three conditions.",
   "wrong_step": {
    "text": "First slope taken at (1, 1) is 4; resulting y(1) is 11/2.",
    "expr": "11/2"
   },
   "right_step": {
    "text": "First slope at (0, 1) is 2; resulting y(1) is 4.",
    "expr": "4"
   },
   "relation": "distinct",
   "possible_reason": null,
   "sources": [
    "BC-ERR-07020"
   ],
   "fix_prompt": true
  },
  {
   "error_id": "BC-ERR-07021",
   "observed_behavior": "The response evaluates the derivative again at the initial point instead of at the approximation the first step produced.",
   "scoring_consequence": "The demonstration point is lost in the 2024 shape, where two correct steps are required.",
   "wrong_step": {
    "text": "Second slope at (1/2, 1) is 3; resulting y(1) is 7/2.",
    "expr": "7/2"
   },
   "right_step": {
    "text": "Second slope at (1/2, 2) is 4; resulting y(1) is 4.",
    "expr": "4"
   },
   "relation": "distinct",
   "possible_reason": {
    "misconception_id": "BC-MIS-07012",
    "text": "advances the input but not the output"
   },
   "sources": [
    "BC-ERR-07021",
    "BC-MIS-07012"
   ],
   "fix_prompt": true
  }
 ],
 "representations": {
  "text": "The equation and initial condition become a table of approximations, one row per step.",
  "figure": null
 },
 "prerequisite_bridges": [
  {
   "prq_id": "BC-PRQ-07005",
   "text": "Each row starts from the row above."
  }
 ],
 "time": {
  "exam_part": "II-B",
  "budget_minutes": 15.0,
  "source": "research/exam/exam-structure.md#Section and part layout",
  "written_steps": {
   "ex-1": [
    1,
    2,
    3,
    4,
    5,
    6,
    7
   ]
  },
  "skipped_steps": {
   "ex-1": []
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
   "archetype_id": "BC-QA-07004",
   "parameter_draw": {
    "form": "both",
    "x_coefficient": 2,
    "y_coefficient": 1,
    "constant": 1,
    "start_x": 0,
    "start_y": 1,
    "span": 1
   },
   "completes": "ex-1",
   "stem": {
    "text": "dy/dx = 2x + y + 1, step 1/2, first step gives y(1/2) = 2. Finish to approximate y(1).",
    "command_verb": "approximate"
   },
   "key": {
    "form": "numeric",
    "expr": "4"
   },
   "steps": [
    {
     "text": "Slope.",
     "expr": "2*x + y + 1",
     "relation": "new"
    },
    {
     "text": "At (1/2, 2).",
     "expr": "4",
     "relation": "evaluate",
     "subs": {
      "x": "1/2",
      "y": "2"
     }
    },
    {
     "text": "Advance.",
     "expr": "2 + 4/2",
     "relation": "new"
    }
   ],
   "calculator_status": "no_calculator",
   "skills": [
    "BC-SKL-07021"
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
   "archetype_id": "BC-QA-07004",
   "parameter_draw": {
    "form": "x_only",
    "x_coefficient": 2,
    "y_coefficient": 1,
    "constant": -1,
    "start_x": 1,
    "start_y": 3,
    "span": 1
   },
   "stem": {
    "text": "dy/dx = 2x - 1, y(1) = 3. Two equal Euler steps: approximate y(2).",
    "command_verb": "approximate"
   },
   "key": {
    "form": "numeric",
    "expr": "9/2"
   },
   "steps": [
    {
     "text": "Step.",
     "expr": "1/2",
     "relation": "new"
    },
    {
     "text": "Slope.",
     "expr": "2*x - 1",
     "relation": "new"
    },
    {
     "text": "At 1.",
     "expr": "1",
     "relation": "evaluate",
     "subs": {
      "x": "1"
     }
    },
    {
     "text": "y1.",
     "expr": "7/2",
     "relation": "new"
    },
    {
     "text": "Slope.",
     "expr": "2*x - 1",
     "relation": "new"
    },
    {
     "text": "At 3/2.",
     "expr": "2",
     "relation": "evaluate",
     "subs": {
      "x": "3/2"
     }
    },
    {
     "text": "y2.",
     "expr": "9/2",
     "relation": "new"
    }
   ],
   "calculator_status": "no_calculator",
   "skills": [
    "BC-SKL-07019",
    "BC-SKL-07021"
   ]
  },
  {
   "id": "chk-3",
   "check_kind": "mcq",
   "format": "mcq",
   "bands": [
    "low"
   ],
   "archetype_id": "BC-QA-07004",
   "parameter_draw": {
    "form": "both",
    "x_coefficient": 1,
    "y_coefficient": 2,
    "constant": 0,
    "start_x": 0,
    "start_y": 1,
    "span": 1
   },
   "stem": {
    "text": "dy/dx = x + 2y, y(0) = 1. Two equal Euler steps approximate y(1) as",
    "command_verb": "identify"
   },
   "key": {
    "form": "numeric",
    "expr": "17/4"
   },
   "steps": [
    {
     "text": "Slope.",
     "expr": "x + 2*y",
     "relation": "new"
    },
    {
     "text": "At (0, 1).",
     "expr": "2",
     "relation": "evaluate",
     "subs": {
      "x": "0",
      "y": "1"
     }
    },
    {
     "text": "y1 = 2.",
     "expr": "x + 2*y",
     "relation": "new"
    },
    {
     "text": "At (1/2, 2).",
     "expr": "9/2",
     "relation": "evaluate",
     "subs": {
      "x": "1/2",
      "y": "2"
     }
    },
    {
     "text": "y2.",
     "expr": "2 + 9/4",
     "relation": "new"
    }
   ],
   "options": [
    {
     "id": "A",
     "is_key": false,
     "expr": "3",
     "error_path": "BC-ERR-07019",
     "derivation": "one step of size 1"
    },
    {
     "id": "B",
     "is_key": false,
     "expr": "21/4",
     "error_path": "BC-ERR-07020",
     "derivation": "first slope taken at x = 1"
    },
    {
     "id": "C",
     "is_key": false,
     "expr": "13/4",
     "error_path": "BC-ERR-07021",
     "derivation": "second slope at (1/2, 1)"
    },
    {
     "id": "D",
     "is_key": true,
     "expr": "17/4",
     "error_path": null
    }
   ],
   "calculator_status": "no_calculator",
   "skills": [
    "BC-SKL-07020",
    "BC-SKL-07021"
   ]
  }
 ],
 "delivery": [
  {
   "block": "pr-1",
   "mode": "text",
   "reason": "rule 6: a prediction on the worked example's numbers with nothing to draw",
   "sources": [
    "BC-SKL-07021"
   ]
  },
  {
   "block": "orientation",
   "mode": "table",
   "reason": "rule 5: BC-REP-03 on BC-SKL-07019 to 07022 and BC-QA-07004 representations",
   "sources": [
    "BC-SKL-07022",
    "BC-QA-07004"
   ],
   "spec": {
    "kind": "table",
    "representations": [
     "BC-REP-03"
    ],
    "columns": [
     "x",
     "y",
     "slope",
     "increment"
    ],
    "rows": [
     [
      "0",
      "1",
      "2",
      "1"
     ],
     [
      "1/2",
      "2",
      "4",
      "2"
     ],
     [
      "1",
      "4",
      "",
      ""
     ]
    ],
    "labels": [
     {
      "text": "step 1/2",
      "placement": "inside",
      "at": "table caption row"
     }
    ]
   },
   "fallback": "the table as plain text rows",
   "keyboard": "Tab moves between cells; no control"
  },
  {
   "block": "ki-1",
   "mode": "motion",
   "reason": "rule 2: the new point replaces the old, a process",
   "sources": [
    "BC-EK-FUN-7C4",
    "BC-SKL-07021"
   ],
   "spec": {
    "kind": "euler_steps",
    "representations": [
     "BC-REP-02",
     "BC-REP-06"
    ],
    "equation": "dy/dx = 2*x + y + 1",
    "window": {
     "x": [
      0,
      1.2
     ],
     "y": [
      0,
      8
     ]
    },
    "start": [
     0,
     1
    ],
    "step": 0.5,
    "frames": [
     {
      "point": [
       0,
       1
      ]
     },
     {
      "point": [
       0.5,
       2
      ]
     },
     {
      "point": [
       1,
       4
      ]
     }
    ],
    "true_curve": "y = 4*exp(x) - 2*x - 3",
    "labels": [
     {
      "text": "tangent segment from the current point",
      "placement": "inside",
      "at": "along the segment"
     },
     {
      "text": "true solution",
      "placement": "inside",
      "at": "near the curve's right end"
     }
    ]
   },
   "fallback": "the three frames as small static panels in one row",
   "keyboard": "Right arrow steps to the next frame, Left arrow back; Space pauses auto-advance",
   "reduced_motion": "no auto-advance; each key press cross-fades to the next frame"
  },
  {
   "block": "representations",
   "mode": "model",
   "reason": "rule 2: a computed sequence of approximations is the idea, so model on the example's draw",
   "sources": [
    "BC-QA-07004"
   ],
   "spec": {
    "kind": "numeric_experiment",
    "representations": [
     "BC-REP-03",
     "BC-REP-06"
    ],
    "equation": "dy/dx = 2*x + y + 1",
    "start": [
     0,
     1
    ],
    "step": 0.5,
    "computed": "y + step*(2*x + y + 1)",
    "columns": [
     "x",
     "y",
     "slope"
    ],
    "labels": [
     {
      "text": "each row starts from the row above",
      "placement": "inside",
      "at": "row below the last value"
     }
    ]
   },
   "fallback": "the computed rows printed as a static table",
   "keyboard": "a Step control reached by Tab and pressed with Enter or Space adds one row per press"
  },
  {
   "block": "ex-1",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  },
  {
   "block": "err-BC-ERR-07018",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  },
  {
   "block": "err-BC-ERR-07019",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  },
  {
   "block": "err-BC-ERR-07020",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  },
  {
   "block": "err-BC-ERR-07021",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  }
 ],
 "refresher": [
  "ki-1",
  "err-BC-ERR-07018",
  "err-BC-ERR-07019",
  "err-BC-ERR-07020",
  "err-BC-ERR-07021",
  "ex-1"
 ],
 "read_minutes": {
  "full": 4.1,
  "brief": 3.0
 },
 "word_count": {
  "full": 604,
  "brief": 449
 },
 "research_lines": [
  {
   "file": "research/units/unit-07-differential-equations.md",
   "line": "the new point then replaces the old one"
  }
 ],
 "inferred": [
  {
   "claim": "The answer point tag BC-PT-99005 is dropped from ex-1 because its reader line would take the brief band above 450 words.",
   "settles": "A band cap that excludes reader lines, or a shorter reader_checks line for BC-PT-99005."
  },
  {
   "claim": "The orientation is a table, ki-1 a motion and the representations block a model.",
   "settles": "The modality A/B in the build plan."
  },
  {
   "claim": "BC-SKL-07023 carries BC-EK-FUN-7C4 in the snapshot but is missing from the authoring bundle's skill records.",
   "settles": "The bundle including every skill of BC-CON-07006."
  }
 ],
 "sources": [
  "BC-CON-07006",
  "BC-SKL-07019",
  "BC-SKL-07020",
  "BC-SKL-07021",
  "BC-SKL-07022",
  "BC-SKL-07023",
  "BC-EK-FUN-7C4",
  "ced:141",
  "BC-QA-07004",
  "BC-QA-07005",
  "BC-MCQ-SAMPLE-018",
  "BC-MCQ-PE2012-016",
  "BC-FRQ-2021-Q5-B",
  "BC-FRQ-2024-Q5-C",
  "BC-FRQ-2025-Q5-D",
  "BC-PT-99034",
  "BC-PT-99005",
  "sg-25:23",
  "sg-21:19",
  "BC-ERR-07018",
  "BC-ERR-07019",
  "BC-ERR-07020",
  "BC-ERR-07021",
  "BC-MIS-07010",
  "BC-MIS-07011",
  "BC-MIS-07012",
  "BC-PRQ-07005",
  "research/units/unit-07-differential-equations.md#7.5 Approximating Solutions Using Euler's Method",
  "research/question-analysis/question-archetypes.md#BC-QA-07004 Euler's method over two steps of equal size",
  "research/question-analysis/question-archetypes.md#BC-QA-07005 Direction of an approximation decided from the second derivative of a solution",
  "research/scoring/notation-requirements.md#Labels",
  "research/scoring/common-point-losses.md#Answer points",
  "research/exam/exam-structure.md#Section and part layout"
 ]
}
```
