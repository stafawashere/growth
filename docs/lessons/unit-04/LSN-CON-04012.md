---
title: LSN-CON-04012 Direction of the approximation error
research_date: 2026-09-29
status: designed
purpose: Authoring spec for the concept lesson on BC-CON-04012, deciding whether a tangent line approximation over or underestimates from the sign of the second derivative, built from authoring_bundle("BC-CON-04012") and the research files it cites.
---

# LSN-CON-04012 Direction of the approximation error

Concept BC-CON-04012 (skills BC-SKL-04030, BC-SKL-04031), topic 4.6, loaded by BC-QA-04008. Its hard parent is BC-CON-04011; concavity is used as a conclusion from Unit 5 (docs/lessons/unit-04/README.md, section 1).

## Orientation

Served text, from BC-CON-04012 `description_plain` and the topic's Direction of the error paragraph (research/units/unit-04-contextual-applications-differentiation.md#4.6 Approximating Values of a Function Using Local Linearity and Linearization): a response states the sign of the second derivative on the interval between the point of tangency and the nearby input, names the concavity, and concludes over or under from it.

## Key ideas

Both skills map to BC-EK-CHA-3F2 (ced:92), one core block.

- ki-1 (core). Paraphrase of "Direction of the error": with concavity known on an interval holding both inputs, concave up puts the line below the curve (underestimate) and concave down puts it above (overestimate); a reason from increase or decrease is an observed error (BC-ERR-99020). Anchor quote from ced:92.

## Recognition

BC-QA-04008 (research/question-analysis/question-archetypes.md#BC-QA-04008 Tangent line approximation with an over or under estimate judgement): `asked_to_produce` "an overestimate or underestimate judgement with a reason" and "an expression for the second derivative"; `difficulty_variables` "whether the second derivative must be produced to support the judgement". The signal: "overestimate or underestimate" and "give a reason". The FRQ places it after the approximation part (BC-FRQ-2023-Q3-B).

Not this concept: "approximate f at the nearby input" alone (BC-CON-04011).

## Method choice

- st-1, BC-QA-04008. Method, `expected_solution_path[3]` and [4]: the concavity near the point, then the direction with concavity as the reason. Rival from `wrong_approaches`: judging without concavity (BC-ERR-99020). Separating feature: the stem's parameter draw makes f' and f'' disagree in sign, so a verdict from f' is wrong (`parameter_spec` notes).

## Solution path

- ex-1, BC-QA-04008, both bands, no calculator. Draw: curvature -2, offset 3, anchor 1, height 2, step 1/5, judgement on; f(1) = 2, f'(x) = -2x^2 + 3, estimate f(1.2) = 2.2 from the line. Not a published draw.
- Steps: f' (new); f'' (differentiate); the sign on [1, 1.2] and the verdict (no value). The answer is a statement. A fluent solver writes f'' and one sentence naming its sign, the concavity and the verdict.

## Scoring

BC-QA-04008 lists BC-PT-99005 among its point types; ex-1 tags it on the verdict with its reason. A claim without concavity loses the reasoning point (research/scoring/common-point-losses.md#Justification points, cr-23:11, cr-23:12); the reason is tied to the object the prompt gives (research/scoring/justification-requirements.md#Reasons tied to the object the prompt names).

## Traps

Three active errors in the bundle's order: BC-ERR-04026, BC-ERR-99020, BC-ERR-99022. On ex-1's draw; mid band the first two.

- err-BC-ERR-04026: "f'' < 0" asserted with no link to the given f', against f''(x) = -4x < 0. Reason words from BC-MIS-05022.
- err-BC-ERR-99020: f'(1) = 1 > 0 used as the reason, against f''. Reason words from BC-MIS-07010.
- err-BC-ERR-99022: 2 + (1/5) rewritten as 9/5, against 11/5. No linked misconception.

## Representations

None as a separate block; ki-1's interactive carries the curve against its tangent (BC-REP-02 to BC-REP-04).

## Prerequisite bridge

- BC-PRQ-04008, from `description_plain` and `failure_signature`.

## Time

BC-QA-04008 has `calculator_status` either, so Section I Part A, 2.14 minutes (research/exam/exam-structure.md#Section and part layout) [inferred]. Written: f'', its sign on the interval, the verdict with the concavity reason. Held: the sign check for x > 0.

## Checks

- chk-1, completion of ex-1, both bands: f''(x) = -4x is given. Key: overestimate.
- chk-2, isomorph, both bands: curvature 1, offset -4, anchor 1, height 3, step 1/10. Key: underestimate, f''(x) = 2x > 0.
- chk-3, MCQ, low band, on ex-1's approximation with a statement key: distractors carry BC-ERR-99020 (reason from f'), BC-ERR-04026 (concavity asserted unlinked), BC-ERR-99022 (a wrongly simplified estimate).

## Delivery

- orientation: figure. Rule 3: BC-REP-02 on BC-SKL-04030 [inferred].
- ki-1: interactive. Rule 3 promoted: BC-QA-04008 `common_givens` "the point of tangency and a nearby input"; one draggable point of tangency, the reading "line above curve" or "line below curve" (docs/lessons/unit-04/README.md, section 6) [inferred].
- ex-1 and the three error blocks: step_reveal. Rule 1.

## Band plan

- Low (full): orientation, ki-1, st-1, ex-1 with its scoring line, three error blocks, chk-1 to chk-3, the bridge. 555 words, 3.7 minutes (cap 900 and 6).
- Mid (brief): orientation, ki-1, st-1, ex-1 with its scoring line, err-BC-ERR-04026, err-BC-ERR-99020, chk-1, chk-2, the bridge. 444 words, 3.0 minutes (cap 450 and 3).
- Refresher: ki-1, err-BC-ERR-04026, err-BC-ERR-99020, err-BC-ERR-99022, ex-1.

## Sources

- BC-CON-04012; BC-SKL-04030, BC-SKL-04031; BC-EK-CHA-3F2; ced:92
- BC-QA-04008; BC-PT-99005; cr-23:11, cr-23:12
- BC-ERR-04026, BC-ERR-99020, BC-ERR-99022; BC-MIS-05022, BC-MIS-07010
- BC-PRQ-04008
- research/units/unit-04-contextual-applications-differentiation.md#4.6 Approximating Values of a Function Using Local Linearity and Linearization
- research/question-analysis/question-archetypes.md#BC-QA-04008 Tangent line approximation with an over or under estimate judgement
- research/scoring/common-point-losses.md#Justification points
- research/scoring/justification-requirements.md#Reasons tied to the object the prompt names
- research/exam/exam-structure.md#Section and part layout
- [inferred] I-A for an either archetype. Settled by a plan 15 budget rule for calculator_status either.
- [inferred] The figure and interactive modes. Settled by the modality A/B.

## Machine record

```json
{
 "id": "LSN-CON-04012",
 "kind": "concept",
 "target_id": "BC-CON-04012",
 "unit": "04",
 "skills": [
  "BC-SKL-04030",
  "BC-SKL-04031"
 ],
 "orientation": {
  "text": "State the sign of f'' between the point of tangency and the nearby input, name the concavity, and conclude over or under from it.",
  "sources": [
   "BC-CON-04012",
   "research/units/unit-04-contextual-applications-differentiation.md#4.6 Approximating Values of a Function Using Local Linearity and Linearization"
  ]
 },
 "key_ideas": [
  {
   "id": "ki-1",
   "ek_id": "BC-EK-CHA-3F2",
   "depth": "core",
   "text": "With the concavity known on an interval holding both inputs: concave up puts the tangent line below the curve, an underestimate; concave down puts it above, an overestimate. Whether f increases decides nothing.",
   "notation": "sign of f'' near the point",
   "quote": {
    "text": "may determine whether a tangent line value is an underestimate or an overestimate",
    "source": "ced:92"
   },
   "sources": [
    "BC-EK-CHA-3F2",
    "ced:92",
    "research/units/unit-04-contextual-applications-differentiation.md#4.6 Approximating Values of a Function Using Local Linearity and Linearization"
   ]
  }
 ],
 "strategy": [
  {
   "id": "st-1",
   "archetype_id": "BC-QA-04008",
   "cue": "\"Overestimate or underestimate? Give a reason.\"",
   "method": "First line: f'' and its sign between the two inputs.",
   "rival": "Rival: the sign of f' (BC-ERR-99020).",
   "separating_feature": "The asked word is estimate direction, which is bending, not rising.",
   "sources": [
    "BC-QA-04008"
   ],
   "evidence_tag": "verified"
  }
 ],
 "worked_examples": [
  {
   "id": "ex-1",
   "archetype_id": "BC-QA-04008",
   "bands": [
    "low",
    "mid"
   ],
   "parameter_draw": {
    "curvature": -2,
    "offset": 3,
    "anchor": 1,
    "height": 2,
    "step": "1/5",
    "judgement": "on"
   },
   "problem": {
    "text": "f(1) = 2, f'(x) = -2x^2 + 3; the tangent line at x = 1 gives f(1.2) about 2.2. Over or underestimate? Give a reason.",
    "command_verb": "justify"
   },
   "calculator_status": "no_calculator",
   "steps": [
    {
     "cue": "Direction asked: bending decides.",
     "why": "Start from f'.",
     "expr": "-2*x**2 + 3",
     "relation": "new"
    },
    {
     "cue": "Bending is f''.",
     "why": "Differentiate f'.",
     "expr": "-4*x",
     "relation": "differentiate",
     "variable": "x"
    },
    {
     "cue": "Sign on [1, 1.2].",
     "why": "Negative, concave down: line above curve, so overestimate.",
     "point_type_id": "BC-PT-99005"
    }
   ],
   "answer": {
    "form": "statement",
    "expr": "overestimate"
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
   "error_id": "BC-ERR-04026",
   "observed_behavior": "The response states that the second derivative has a sign without connecting that claim to the graph, table, or formula supplied.",
   "scoring_consequence": "The justification point is lost; BC-ERR-99001 records vague referents in justifications and the 2023 report records reasons not connected to the given graph (cr-23:15).",
   "wrong_step": {
    "text": "f'' < 0, unlinked.",
    "expr": "fpp"
   },
   "right_step": {
    "text": "f''(x) = -4x < 0.",
    "expr": "-4*x"
   },
   "relation": "distinct",
   "possible_reason": {
    "misconception_id": "BC-MIS-05022",
    "text": "supplies derivative notation in place of a statement about the object"
   },
   "sources": [
    "BC-ERR-04026",
    "BC-MIS-05022"
   ]
  },
  {
   "error_id": "BC-ERR-99020",
   "observed_behavior": "Responses decide whether a tangent line approximation is an overestimate or an underestimate without using the sign of the second derivative, or state the correct conclusion with reasoning that does not mention concavity.",
   "scoring_consequence": "The reasoning point is not earned; in 2022 this part was the most challenging of its question.",
   "wrong_step": {
    "text": "f'(1) = 1.",
    "expr": "1"
   },
   "right_step": {
    "text": "f''(x) = -4x.",
    "expr": "-4*x"
   },
   "relation": "distinct",
   "possible_reason": {
    "misconception_id": "BC-MIS-07010",
    "text": "from the monotonicity of the solution rather than from its concavity"
   },
   "sources": [
    "BC-ERR-99020",
    "BC-MIS-07010"
   ]
  },
  {
   "error_id": "BC-ERR-99022",
   "observed_behavior": "Responses simplify a numerical or algebraic expression that the exam does not require to be simplified, and introduce sign, order of operations or fraction errors that spoil an otherwise correct result.",
   "scoring_consequence": "A point already secured by the correct setup can be lost when the simplified final form is wrong.",
   "wrong_step": {
    "text": "9/5.",
    "expr": "9/5"
   },
   "right_step": {
    "text": "11/5.",
    "expr": "11/5"
   },
   "relation": "distinct",
   "possible_reason": null,
   "sources": [
    "BC-ERR-99022"
   ]
  }
 ],
 "representations": null,
 "prerequisite_bridges": [
  {
   "prq_id": "BC-PRQ-04008",
   "text": "Name each quantity in the setting, its unit, and whether it varies."
  }
 ],
 "time": {
  "exam_part": "I-A",
  "budget_minutes": 2.14,
  "source": "research/exam/exam-structure.md#Section and part layout",
  "written_steps": {
   "ex-1": [
    2,
    3
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
   "archetype_id": "BC-QA-04008",
   "parameter_draw": {
    "curvature": -2,
    "offset": 3,
    "anchor": 1,
    "height": 2,
    "step": "1/5",
    "judgement": "on"
   },
   "completes": "ex-1",
   "stem": {
    "text": "For ex-1, f''(x) = -4x. Is 2.2 an over or underestimate of f(1.2)?",
    "command_verb": "justify"
   },
   "key": {
    "form": "statement",
    "expr": "overestimate"
   },
   "steps": [
    {
     "text": "f'' negative on [1, 1.2].",
     "expr": "-4*x",
     "relation": "new"
    }
   ],
   "calculator_status": "no_calculator",
   "skills": [
    "BC-SKL-04031"
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
   "archetype_id": "BC-QA-04008",
   "parameter_draw": {
    "curvature": 1,
    "offset": -4,
    "anchor": 1,
    "height": 3,
    "step": "1/10",
    "judgement": "on"
   },
   "stem": {
    "text": "f(1) = 3, f'(x) = x^2 - 4; the tangent line gives f(1.1) about 2.7. Over or underestimate? Why?",
    "command_verb": "justify"
   },
   "key": {
    "form": "statement",
    "expr": "underestimate"
   },
   "steps": [
    {
     "text": "f'.",
     "expr": "x**2 - 4",
     "relation": "new"
    },
    {
     "text": "f'' positive: concave up.",
     "expr": "2*x",
     "relation": "differentiate",
     "variable": "x"
    }
   ],
   "calculator_status": "no_calculator",
   "skills": [
    "BC-SKL-04030"
   ]
  },
  {
   "id": "chk-3",
   "check_kind": "mcq",
   "format": "mcq",
   "bands": [
    "low"
   ],
   "archetype_id": "BC-QA-04008",
   "parameter_draw": {
    "curvature": -3,
    "offset": 7,
    "anchor": 1,
    "height": 1,
    "step": "1/10",
    "judgement": "on"
   },
   "stem": {
    "text": "f(1) = 1 and f'(x) = -3x^2 + 7. Which response approximates f(1.1) with the tangent line and judges it correctly?",
    "command_verb": "identify"
   },
   "key": {
    "form": "statement",
    "expr": "overestimate",
    "label": "1.4, an overestimate, because f''(x) = -6x < 0 on [1, 1.1]."
   },
   "steps": [
    {
     "text": "f'.",
     "expr": "-3*x**2 + 7",
     "relation": "new"
    },
    {
     "text": "f''.",
     "expr": "-6*x",
     "relation": "differentiate",
     "variable": "x"
    }
   ],
   "options": [
    {
     "id": "A",
     "is_key": false,
     "label": "1.4, an underestimate, because f'(1) = 4 > 0.",
     "error_path": "BC-ERR-99020",
     "derivation": "verdict from the sign of f'"
    },
    {
     "id": "B",
     "is_key": true,
     "label": "1.4, an overestimate, because f''(x) = -6x < 0 on [1, 1.1].",
     "error_path": null
    },
    {
     "id": "C",
     "is_key": false,
     "label": "1.4, an overestimate, because the graph is concave down.",
     "error_path": "BC-ERR-04026",
     "derivation": "concavity asserted with no link to the given f'"
    },
    {
     "id": "D",
     "is_key": false,
     "label": "0.6, an overestimate, because f''(x) = -6x < 0.",
     "error_path": "BC-ERR-99022",
     "derivation": "1 + 4(0.1) simplified as 1 - 0.4"
    }
   ],
   "calculator_status": "no_calculator",
   "skills": [
    "BC-SKL-04031"
   ]
  }
 ],
 "delivery": [
  {
   "block": "orientation",
   "mode": "figure",
   "reason": "rule 3: BC-REP-02 on BC-SKL-04030",
   "sources": [
    "BC-SKL-04030"
   ],
   "spec": {
    "kind": "graph",
    "representations": [
     "BC-REP-02"
    ],
    "window": {
     "x": [
      0.6,
      1.4
     ],
     "y": [
      1.5,
      2.6
     ]
    },
    "curves": [
     {
      "expr": "f near x = 1, concave down"
     },
     {
      "expr": "tangent line 2 + (x - 1)"
     }
    ],
    "labels": [
     {
      "text": "line above curve",
      "placement": "inside"
     },
     {
      "text": "f'' < 0",
      "placement": "inside"
     }
    ]
   },
   "fallback": "the same graph as a static image with its two labels",
   "keyboard": "none needed: the figure has no control"
  },
  {
   "block": "ki-1",
   "mode": "interactive",
   "reason": "rule 3 promoted: BC-REP-02 on BC-SKL-04030; BC-QA-04008 common_givens name the point of tangency and a nearby input, and the stem asks over or under",
   "sources": [
    "BC-SKL-04030",
    "BC-QA-04008"
   ],
   "spec": {
    "kind": "graph",
    "representations": [
     "BC-REP-02",
     "BC-REP-04"
    ],
    "curve": "a curve concave down for x < 0 and concave up for x > 0",
    "controls": [
     {
      "type": "draggable_point",
      "constrained_to": "curve",
      "start": [
       1,
       1
      ]
     }
    ],
    "drawn": [
     "the tangent line at the point",
     "the sign of f'' at the point"
    ],
    "labels": [
     {
      "text": "line above curve",
      "placement": "inside"
     },
     {
      "text": "line below curve",
      "placement": "inside"
     }
    ],
    "question": "At the chosen point, does the tangent line over or underestimate nearby values?"
   },
   "fallback": "two static frames, one point in each concavity region, with the label that holds",
   "keyboard": "Tab focuses the point; left and right arrow keys move it along the curve"
  },
  {
   "block": "ex-1",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  },
  {
   "block": "err-BC-ERR-04026",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  },
  {
   "block": "err-BC-ERR-99020",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  },
  {
   "block": "err-BC-ERR-99022",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  }
 ],
 "refresher": [
  "ki-1",
  "err-BC-ERR-04026",
  "err-BC-ERR-99020",
  "err-BC-ERR-99022",
  "ex-1"
 ],
 "research_lines": [
  {
   "file": "research/units/unit-04-contextual-applications-differentiation.md",
   "line": "the tangent line lies below the curve where the graph is concave up, so the approximation underestimates"
  }
 ],
 "inferred": [
  {
   "claim": "BC-QA-04008 has calculator_status either, so the exam part is taken as I-A.",
   "settles": "A plan 15 budget rule for calculator_status either."
  },
  {
   "claim": "The orientation figure and ki-1 interactive serve better than text.",
   "settles": "The modality A/B in the build plan: skip rate and time to first credited success by mode."
  },
  {
   "claim": "The BC-ERR-99022 distractor simplifies 1 + 4(0.1) as 1 - 0.4.",
   "settles": "Response data on chk-3."
  }
 ],
 "sources": [
  "BC-CON-04012",
  "BC-SKL-04030",
  "BC-SKL-04031",
  "BC-EK-CHA-3F2",
  "ced:92",
  "BC-QA-04008",
  "BC-PT-99005",
  "cr-23:11",
  "cr-23:12",
  "BC-ERR-04026",
  "BC-ERR-99020",
  "BC-ERR-99022",
  "BC-MIS-05022",
  "BC-MIS-07010",
  "BC-PRQ-04008",
  "research/units/unit-04-contextual-applications-differentiation.md#4.6 Approximating Values of a Function Using Local Linearity and Linearization",
  "research/question-analysis/question-archetypes.md#BC-QA-04008 Tangent line approximation with an over or under estimate judgement",
  "research/scoring/common-point-losses.md#Justification points",
  "research/scoring/justification-requirements.md#Reasons tied to the object the prompt names",
  "research/exam/exam-structure.md#Section and part layout"
 ],
 "word_count": {
  "full": 555,
  "brief": 444
 },
 "read_minutes": {
  "full": 3.7,
  "brief": 3.0
 }
}
```
