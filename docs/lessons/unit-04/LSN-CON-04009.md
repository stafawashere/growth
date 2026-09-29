---
title: LSN-CON-04009 Substitution after differentiation
research_date: 2026-09-29
status: designed
purpose: Authoring spec for the concept lesson on BC-CON-04009, substituting values that hold only at one instant after the differentiation and recovering a missing value from the relating equation, built from authoring_bundle("BC-CON-04009") and the research files it cites.
---

# LSN-CON-04009 Substitution after differentiation

Concept BC-CON-04009 (skills BC-SKL-04023, BC-SKL-04026, BC-SKL-04027), topic 4.5, loaded by BC-QA-04006 (primary) and BC-QA-04007. Its hard parents are BC-CON-04007 and BC-CON-04008 (docs/lessons/unit-04/README.md, section 1).

## Prediction

Served first in both bands. Multiple choice on ex-1's relation \(x^2+y^2=225\) with the foot at \(x=9\): whether 9 goes in before or after differentiating in \(t\). Three options, key after; option A is before, shown as the BC-ERR-04020 result 2y dy/dt = 0 with the 18 dx/dt term lost (SymPy), and option C is either order. Substituting x = 9 into the relation to recover y = 12 is legitimate work (ex-1), so no option shows it. The resolution says \(x\) changes with time, so its rate term must stay, the concept's core claim in the record's words. Sources: BC-CON-04009 and the topic 4.5 section that ki-1 cites. Delivery: text.

## Orientation

Served text, from BC-CON-04009 `description_plain` and the topic's Assessment behaviour paragraph (research/units/unit-04-contextual-applications-differentiation.md#4.5 Solving Related Rates Problems): a response keeps every varying quantity as a variable through the differentiation, puts the instant's values in afterwards, and recovers any missing value from the relating equation.

## Key ideas

All three skills map to BC-EK-CHA-3E1 (ced:91), so one core block, both bands.

- ki-1 (core). Paraphrase of "Order of operations" and "Missing values": varying quantities stay variables until after the differentiation; constants may go in at any stage; a value needed but not supplied comes from the relating equation at the instant. The CED sample activity marks which information always applies and which applies only at an instant (ced:86). Anchor quote from ced:91.

## Recognition

BC-QA-04006 (research/question-analysis/question-archetypes.md#BC-QA-04006 Related rates in a geometric setting): `common_givens` "the dimensions at the instant"; `asked_to_produce` the rate at the stated instant. The signal: "at the instant when" followed by a dimension, and a second dimension the stem does not state. BC-QA-04007 (research/question-analysis/question-archetypes.md#BC-QA-04007 Related rates on an implicitly defined curve): "at the instant when the particle is at the stated point"; the point goes in after the differentiation.

Not this concept: a quantity fixed for the whole motion, such as a ladder's length, which may be substituted at any stage.

The contrast pair on st-1 takes its near miss from that case: a ladder whose foot distance is a one-instant value, beside the fixed length L, which may go in first. The separating feature is whether the value holds throughout or at one instant.

## Method choice

- st-1, BC-QA-04006. Method, `expected_solution_path[4]` placed after [3]: differentiate first, then substitute (served without a label). Rival from `wrong_approaches`: substituting instantaneous values before differentiating (BC-ERR-04020). Separating feature: does the value hold only "at the instant"?
- st-2, BC-QA-04007. Method, `expected_solution_path[2]` after [0]: the point and the supplied rate go into the differentiated curve equation. Rival: the point substituted into the curve before differentiating. Separating feature: the coordinates are one instant's values.

## Solution path

- ex-1, BC-QA-04006, both bands, no calculator. Draw: shape ladder, size 9, rate 2, ratio 3, leg short, meter, second; a 15 meter ladder, foot 9 meters out sliding away at 2 meters per second. No published BC-QA-04006 item carries this draw.
- Steps: relating equation (new); x = 9 put into it (evaluate); y = 12 (solve); differentiation in t (new); the instant substituted (evaluate); the rate (solve). The first three recover the missing value; a fluent solver writes all six.

## Scoring

BC-QA-04006 lists BC-PT-99023, BC-PT-99006, BC-PT-99004 and BC-PT-99022. ex-1 tags BC-PT-99023 on the differentiation. For the author: the implicit task scores an eligible differentiation with respect to time, a completely correct one and the value, and a sign error was the most common loss of the last point in 2025 (cr-24:18, crabbc-25:25).

## Traps

Three active errors, in the bundle's order: BC-ERR-04020, BC-ERR-04022, BC-ERR-99013. On ex-1's draw; the mid band shows the first two. All three are fix prompts (relation distinct).

- err-BC-ERR-04020: x = 9 put in before differentiating, so dx/dt vanishes. Reason words from BC-MIS-04011.
- err-BC-ERR-04022: y never computed, so the rate is left as -18/y. No reason line: the linked descriptions do not describe the missing value.
- err-BC-ERR-99013: dy/dx = -x/y reported. Reason words from BC-MIS-04008.

## Representations

None as a separate block; the orientation figure and ki-1's interactive carry the diagram (BC-REP-08).

## Prerequisite bridge

- BC-PRQ-04007 and BC-PRQ-04008, from `description_plain` and `failure_signature`.

## Time

BC-QA-04006 has `calculator_status` either, so Section I Part A, 2.14 minutes (research/exam/exam-structure.md#Section and part layout) [inferred]. Written: the relating equation, the missing value, the differentiated equation, the substituted equation, the rate. Held: the square root arithmetic.

## Checks

- chk-1, completion of ex-1, both bands: the differentiated equation and y = 12 are given. Key -3/2.
- chk-2, isomorph, both bands: ladder, size 6, rate 5, ratio 2, leg short, foot, minute; a 10 foot ladder, foot 6 feet out at 5 feet per minute. Key -15/4.
- chk-3, MCQ, low band: ladder, size 4, rate 6, ratio 1, leg long, foot, second; a 5 foot ladder, foot 4 feet out at 6 feet per second. Key -8. Distractors: 0 (BC-ERR-04020), -24/5 (BC-ERR-04022, y replaced by the ladder length), -4/3 (BC-ERR-99013).

## Delivery

- orientation: figure. Rule 4: BC-REP-08 on BC-SKL-04026 and BC-SKL-04027 [inferred].
- ki-1: interactive. Rule 4 promoted: BC-QA-04006 `common_givens` "the dimensions at the instant"; one slider on x, the reading is which labels change as time moves (docs/lessons/unit-04/README.md, section 6) [inferred].
- ex-1 and the three error blocks: step_reveal. Rule 1.

## Band plan

- Low (full), served order: prediction, orientation, bridges BC-PRQ-04007 and 04008 when gated, ki-1, st-1 with its contrast pair, st-2, ex-1 with its scoring line, chk-1, the three error blocks, chk-2, chk-3. 578 words, 3.9 minutes (cap 900 and 6). This design has one worked example, so nothing is faded.
- Mid (brief): prediction, orientation, bridges when gated, ki-1, st-1 with its contrast pair, ex-1 with its scoring line, chk-1, err-BC-ERR-04020, err-BC-ERR-04022, chk-2. 450 words, 3.0 minutes (cap 450 and 3). The two bridges are one short phrase each to hold the cap; the ki-1 quote stays.
- Refresher: ki-1, the three error blocks, ex-1.

## Sources

- BC-CON-04009; BC-SKL-04023, BC-SKL-04026, BC-SKL-04027; BC-EK-CHA-3E1; ced:86, ced:91
- Prediction pr-1 and the contrast pair: BC-CON-04009, BC-ERR-04020
- BC-QA-04006, BC-QA-04007; BC-PT-99023; cr-24:18, crabbc-25:25
- BC-ERR-04020, BC-ERR-04022, BC-ERR-99013; BC-MIS-04011, BC-MIS-04008
- BC-PRQ-04007, BC-PRQ-04008
- research/units/unit-04-contextual-applications-differentiation.md#4.5 Solving Related Rates Problems
- research/question-analysis/question-archetypes.md#BC-QA-04006 Related rates in a geometric setting
- research/question-analysis/question-archetypes.md#BC-QA-04007 Related rates on an implicitly defined curve
- research/exam/exam-structure.md#Section and part layout
- [inferred] I-A for an either archetype. Settled by a plan 15 budget rule for calculator_status either.
- [inferred] The figure and interactive modes. Settled by the modality A/B.
- [inferred] The chk-3 distractor for BC-ERR-04022 takes the ladder length as the invented value. Settled by response data on the check.

## Machine record

```json
{
 "id": "LSN-CON-04009",
 "kind": "concept",
 "target_id": "BC-CON-04009",
 "unit": "04",
 "skills": [
  "BC-SKL-04023",
  "BC-SKL-04026",
  "BC-SKL-04027"
 ],
 "prediction": {
  "id": "pr-1",
  "stem": {
   "text": "Predict. On x^2 + y^2 = 225 the foot is at x = 9. Does 9 go in before or after differentiating in t?",
   "command_verb": "predict"
  },
  "format": "mcq",
  "options": [
   {
    "id": "A",
    "label": "Before: 2y dy/dt = 0.",
    "is_key": false
   },
   {
    "id": "B",
    "label": "After: x varies.",
    "is_key": true
   },
   {
    "id": "C",
    "label": "Either order.",
    "is_key": false
   }
  ],
  "resolution": "After: x changes with time, so its rate term must stay.",
  "sources": [
   "BC-CON-04009",
   "research/units/unit-04-contextual-applications-differentiation.md#4.5 Solving Related Rates Problems"
  ]
 },
 "orientation": {
  "text": "Keep varying quantities as variables through differentiation; substitute the instant afterwards.",
  "sources": [
   "BC-CON-04009",
   "research/units/unit-04-contextual-applications-differentiation.md#4.5 Solving Related Rates Problems"
  ]
 },
 "key_ideas": [
  {
   "id": "ki-1",
   "ek_id": "BC-EK-CHA-3E1",
   "depth": "core",
   "text": "A one-instant value goes in after differentiating; a value fixed throughout may go in at any stage. A missing value comes from the relating equation.",
   "notation": "values substituted into the differentiated equation",
   "quote": {
    "text": "relating it to other quantities whose rates of change are known",
    "source": "ced:91"
   },
   "sources": [
    "BC-EK-CHA-3E1",
    "ced:91",
    "ced:86",
    "research/units/unit-04-contextual-applications-differentiation.md#4.5 Solving Related Rates Problems"
   ]
  }
 ],
 "strategy": [
  {
   "id": "st-1",
   "archetype_id": "BC-QA-04006",
   "cue": "\"At the instant when\" a value is given.",
   "method": "Differentiate first; substitute after.",
   "rival": "The value put in first.",
   "separating_feature": "Instant values change; fixed lengths do not.",
   "sources": [
    "BC-QA-04006",
    "BC-ERR-04020"
   ],
   "evidence_tag": "verified",
   "contrast": {
    "this": {
     "text": "A 13 foot ladder's foot slides out at 3 feet per second. Find dy/dt at foot 5 feet.",
     "archetype_id": "BC-QA-04006"
    },
    "not_this": {
     "text": "L = 13 throughout in x^2 + y^2 = L^2. May 13 go in first?",
     "why_not": "L is fixed."
    },
    "feature": "Fixed, or true at one instant?"
   }
  },
  {
   "id": "st-2",
   "archetype_id": "BC-QA-04007",
   "cue": "A point on a curve and one coordinate rate.",
   "method": "Differentiate the curve in t, then put in the point and the rate.",
   "rival": "The point substituted before differentiating.",
   "separating_feature": "The point holds for one instant only.",
   "sources": [
    "BC-QA-04007"
   ],
   "evidence_tag": "verified"
  }
 ],
 "worked_examples": [
  {
   "id": "ex-1",
   "archetype_id": "BC-QA-04006",
   "bands": [
    "low",
    "mid"
   ],
   "parameter_draw": {
    "shape": "ladder",
    "size": 9,
    "rate": 2,
    "ratio": 3,
    "leg": "short",
    "length_unit": "meter",
    "time_unit": "second"
   },
   "problem": {
    "text": "A 15 meter ladder leans on a wall; its foot slides away at 2 meters per second. Find dy/dt for the top when the foot is 9 meters out.",
    "command_verb": "find"
   },
   "calculator_status": "no_calculator",
   "steps": [
    {
     "cue": "Ladder length is fixed.",
     "why": "15 is constant.",
     "expr": "x**2 + y**2 = 225",
     "relation": "new"
    },
    {
     "cue": "y not given.",
     "why": "Recover it.",
     "expr": "81 + y**2 = 225",
     "relation": "evaluate",
     "subs": {
      "x": "9"
     }
    },
    {
     "cue": "Solve for y.",
     "why": "Positive root.",
     "expr": "12",
     "relation": "solve",
     "variable": "y"
    },
    {
     "cue": "General equation.",
     "why": "x and y both vary.",
     "expr": "2*x*dxdt + 2*y*dydt = 0",
     "relation": "new",
     "point_type_id": "BC-PT-99023"
    },
    {
     "cue": "The instant.",
     "why": "x = 9, y = 12, dx/dt = 2.",
     "expr": "36 + 24*dydt = 0",
     "relation": "evaluate",
     "subs": {
      "x": "9",
      "y": "12",
      "dxdt": "2"
     }
    },
    {
     "cue": "One unknown.",
     "why": "Meters per second, falling.",
     "expr": "-3/2",
     "relation": "solve",
     "variable": "dydt"
    }
   ],
   "answer": {
    "form": "symbolic",
    "expr": "-3/2"
   }
  }
 ],
 "what_a_reader_scores": [
  {
   "example_id": "ex-1",
   "point_type_ids": [
    "BC-PT-99023"
   ],
   "lines": [
    {
     "point_type_id": "BC-PT-99023",
     "text": "Chain rule. Earned by: Correct differentiation of the inner function, including the required differentials (sg-22:16, sg-25:21). Not earned by: A product rule written without one or both differentials, which sg-22:16 states earns the product rule point but not this one. Notation: sg-22:16 treats a missing differential as the defining failure for this point."
    }
   ]
  }
 ],
 "common_errors": [
  {
   "error_id": "BC-ERR-04020",
   "observed_behavior": "A dimension that varies with time is replaced by its value at the instant before the equation is differentiated, so its rate never appears.",
   "scoring_consequence": "The differentiated equation is wrong and the answer follows it; the CED sample activity asks students to mark which given information always applies and which applies only at an instant, which is the distinction at stake (ced:86).",
   "wrong_step": {
    "text": "x = 9 first.",
    "expr": "2*y*dydt = 0"
   },
   "right_step": {
    "text": "Differentiate first.",
    "expr": "2*x*dxdt + 2*y*dydt = 0"
   },
   "relation": "distinct",
   "possible_reason": {
    "misconception_id": "BC-MIS-04011",
    "text": "so they are substituted before the differentiation"
   },
   "sources": [
    "BC-ERR-04020",
    "BC-MIS-04011"
   ],
   "fix_prompt": true
  },
  {
   "error_id": "BC-ERR-04022",
   "observed_behavior": "A quantity needed for the substitution is absent from the stem and the response substitutes nothing in its place or invents a value.",
   "scoring_consequence": "The substitution is incomplete and the answer point is lost.",
   "wrong_step": {
    "text": "y left.",
    "expr": "-18/y"
   },
   "right_step": {
    "text": "y = 12.",
    "expr": "-3/2"
   },
   "relation": "distinct",
   "possible_reason": null,
   "sources": [
    "BC-ERR-04022"
   ],
   "fix_prompt": true
  },
  {
   "error_id": "BC-ERR-99013",
   "observed_behavior": "Responses differentiate an implicit relation with respect to x when time is the independent variable, omit the product rule on a product of two changing quantities, or treat one quantity as constant, and confuse the notations for the several derivatives in play.",
   "scoring_consequence": "The differentiation points in the part are not earned, and the numerical answer point depends on them.",
   "wrong_step": {
    "text": "dy/dx.",
    "expr": "-3/4"
   },
   "right_step": {
    "text": "dy/dt.",
    "expr": "-3/2"
   },
   "relation": "distinct",
   "possible_reason": {
    "misconception_id": "BC-MIS-04008",
    "text": "so the rates with respect to time never appear"
   },
   "sources": [
    "BC-ERR-99013",
    "BC-MIS-04008"
   ],
   "fix_prompt": true
  }
 ],
 "representations": null,
 "prerequisite_bridges": [
  {
   "prq_id": "BC-PRQ-04007",
   "text": "Solve a linear equation."
  },
  {
   "prq_id": "BC-PRQ-04008",
   "text": "Naming quantities."
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
    3,
    4,
    5,
    6
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
   "archetype_id": "BC-QA-04006",
   "parameter_draw": {
    "shape": "ladder",
    "size": 9,
    "rate": 2,
    "ratio": 3,
    "leg": "short",
    "length_unit": "meter",
    "time_unit": "second"
   },
   "completes": "ex-1",
   "stem": {
    "text": "In the example above, 2x dx/dt + 2y dy/dt = 0 and y = 12 when x = 9. Find dy/dt.",
    "command_verb": "find"
   },
   "key": {
    "form": "symbolic",
    "expr": "-3/2"
   },
   "steps": [
    {
     "text": "Differentiated.",
     "expr": "2*x*dxdt + 2*y*dydt = 0",
     "relation": "new"
    },
    {
     "text": "Instant.",
     "expr": "36 + 24*dydt = 0",
     "relation": "evaluate",
     "subs": {
      "x": "9",
      "y": "12",
      "dxdt": "2"
     }
    },
    {
     "text": "Solve.",
     "expr": "-3/2",
     "relation": "solve",
     "variable": "dydt"
    }
   ],
   "calculator_status": "no_calculator",
   "skills": [
    "BC-SKL-04023"
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
   "archetype_id": "BC-QA-04006",
   "parameter_draw": {
    "shape": "ladder",
    "size": 6,
    "rate": 5,
    "ratio": 2,
    "leg": "short",
    "length_unit": "foot",
    "time_unit": "minute"
   },
   "stem": {
    "text": "A 10 foot ladder's foot slides out at 5 feet per minute. Find dy/dt for the top when the foot is 6 feet out.",
    "command_verb": "find"
   },
   "key": {
    "form": "symbolic",
    "expr": "-15/4"
   },
   "steps": [
    {
     "text": "Relation.",
     "expr": "x**2 + y**2 = 100",
     "relation": "new"
    },
    {
     "text": "x = 6.",
     "expr": "36 + y**2 = 100",
     "relation": "evaluate",
     "subs": {
      "x": "6"
     }
    },
    {
     "text": "y = 8.",
     "expr": "8",
     "relation": "solve",
     "variable": "y"
    },
    {
     "text": "Differentiate.",
     "expr": "2*x*dxdt + 2*y*dydt = 0",
     "relation": "new"
    },
    {
     "text": "Instant.",
     "expr": "60 + 16*dydt = 0",
     "relation": "evaluate",
     "subs": {
      "x": "6",
      "y": "8",
      "dxdt": "5"
     }
    },
    {
     "text": "Solve.",
     "expr": "-15/4",
     "relation": "solve",
     "variable": "dydt"
    }
   ],
   "calculator_status": "no_calculator",
   "skills": [
    "BC-SKL-04026"
   ]
  },
  {
   "id": "chk-3",
   "check_kind": "mcq",
   "format": "mcq",
   "bands": [
    "low"
   ],
   "archetype_id": "BC-QA-04006",
   "parameter_draw": {
    "shape": "ladder",
    "size": 4,
    "rate": 6,
    "ratio": 1,
    "leg": "long",
    "length_unit": "foot",
    "time_unit": "second"
   },
   "stem": {
    "text": "A 5 foot ladder's foot slides out at 6 feet per second. Find dy/dt for the top when the foot is 4 feet out.",
    "command_verb": "find"
   },
   "key": {
    "form": "symbolic",
    "expr": "-8"
   },
   "steps": [
    {
     "text": "Relation.",
     "expr": "x**2 + y**2 = 25",
     "relation": "new"
    },
    {
     "text": "x = 4.",
     "expr": "16 + y**2 = 25",
     "relation": "evaluate",
     "subs": {
      "x": "4"
     }
    },
    {
     "text": "y = 3.",
     "expr": "3",
     "relation": "solve",
     "variable": "y"
    },
    {
     "text": "Differentiate.",
     "expr": "2*x*dxdt + 2*y*dydt = 0",
     "relation": "new"
    },
    {
     "text": "Instant.",
     "expr": "48 + 6*dydt = 0",
     "relation": "evaluate",
     "subs": {
      "x": "4",
      "y": "3",
      "dxdt": "6"
     }
    },
    {
     "text": "Solve.",
     "expr": "-8",
     "relation": "solve",
     "variable": "dydt"
    }
   ],
   "options": [
    {
     "id": "A",
     "is_key": false,
     "expr": "0",
     "error_path": "BC-ERR-04020",
     "derivation": "x = 4 put in first, so 2y dy/dt = 0"
    },
    {
     "id": "B",
     "is_key": false,
     "expr": "-24/5",
     "error_path": "BC-ERR-04022",
     "derivation": "y never computed; the ladder length 5 used in its place"
    },
    {
     "id": "C",
     "is_key": true,
     "expr": "-8",
     "error_path": null
    },
    {
     "id": "D",
     "is_key": false,
     "expr": "-4/3",
     "error_path": "BC-ERR-99013",
     "derivation": "dy/dx = -x/y reported"
    }
   ],
   "calculator_status": "no_calculator",
   "skills": [
    "BC-SKL-04023"
   ]
  }
 ],
 "delivery": [
  {
   "block": "orientation",
   "mode": "figure",
   "reason": "rule 4: BC-REP-08 on BC-SKL-04026 and BC-SKL-04027",
   "sources": [
    "BC-SKL-04026",
    "BC-SKL-04027"
   ],
   "spec": {
    "kind": "diagram",
    "representations": [
     "BC-REP-08"
    ],
    "labels": [
     {
      "text": "15: fixed",
      "placement": "inside",
      "at": [
       5,
       7
      ]
     },
     {
      "text": "x: varies",
      "placement": "inside",
      "at": [
       4,
       1
      ]
     },
     {
      "text": "y: varies",
      "placement": "inside",
      "at": [
       0.5,
       6
      ]
     }
    ],
    "window": {
     "x": [
      -1,
      16
     ],
     "y": [
      -1,
      16
     ]
    },
    "segments": [
     {
      "from": [
       0,
       0
      ],
      "to": [
       0,
       15.5
      ]
     },
     {
      "from": [
       0,
       0
      ],
      "to": [
       15.5,
       0
      ]
     },
     {
      "from": [
       9,
       0
      ],
      "to": [
       0,
       12
      ]
     }
    ],
    "points": [
     [
      9,
      0
     ],
     [
      0,
      12
     ]
    ]
   },
   "fallback": "the same labelled ladder as a static image",
   "keyboard": "none needed: the figure has no control"
  },
  {
   "block": "ki-1",
   "mode": "interactive",
   "reason": "rule 4 promoted: BC-REP-08 on BC-SKL-04026 and BC-SKL-04027; BC-QA-04006 common_givens name the dimensions at the instant, and the reading is which labels change as time moves",
   "sources": [
    "BC-SKL-04026",
    "BC-SKL-04027",
    "BC-QA-04006"
   ],
   "spec": {
    "kind": "diagram",
    "representations": [
     "BC-REP-08",
     "BC-REP-01"
    ],
    "controls": [
     {
      "type": "slider",
      "parameter": "x",
      "range": [
       3,
       14
      ],
      "step": 1,
      "start": 9
     }
    ],
    "drawn": [
     "the ladder at foot distance x",
     "y from x squared plus y squared equals 225"
    ],
    "labels": [
     {
      "text": "x: changes",
      "placement": "inside",
      "at": [
       3,
       1
      ]
     },
     {
      "text": "y: changes",
      "placement": "inside",
      "at": [
       0.5,
       14.5
      ]
     },
     {
      "text": "15: stays",
      "placement": "inside",
      "at": [
       5,
       7
      ]
     }
    ],
    "question": "Which of the stated numbers would still hold one second later?",
    "window": {
     "x": [
      -1,
      16
     ],
     "y": [
      -1,
      16
     ]
    },
    "segments": [
     {
      "from": [
       0,
       0
      ],
      "to": [
       0,
       15.5
      ]
     },
     {
      "from": [
       0,
       0
      ],
      "to": [
       15.5,
       0
      ]
     },
     {
      "from": [
       9,
       0
      ],
      "to": [
       0,
       12
      ]
     }
    ],
    "points": [
     {
      "x": "x",
      "y": 0
     },
     {
      "x": 0,
      "y": "sqrt(225 - x**2)"
     }
    ]
   },
   "fallback": "two static frames at x = 9 and x = 11 with the same labels",
   "keyboard": "Tab focuses the slider; left and right arrow keys step x by 1"
  },
  {
   "block": "ex-1",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  },
  {
   "block": "err-BC-ERR-04020",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  },
  {
   "block": "err-BC-ERR-04022",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  },
  {
   "block": "err-BC-ERR-99013",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  }
 ],
 "refresher": [
  "ki-1",
  "err-BC-ERR-04020",
  "err-BC-ERR-04022",
  "err-BC-ERR-99013",
  "ex-1"
 ],
 "research_lines": [
  {
   "file": "research/units/unit-04-contextual-applications-differentiation.md",
   "line": "A quantity needed for the substitution but not supplied is recovered from the relating equation at the instant in question."
  }
 ],
 "inferred": [
  {
   "claim": "BC-QA-04006 has calculator_status either, so the exam part is taken as I-A.",
   "settles": "A plan 15 budget rule for calculator_status either."
  },
  {
   "claim": "The orientation figure and ki-1 interactive serve better than text.",
   "settles": "The modality A/B in the build plan: skip rate and time to first credited success by mode."
  },
  {
   "claim": "The chk-3 distractor for BC-ERR-04022 uses the ladder length as the invented value.",
   "settles": "Response data on chk-3 showing which value is invented."
  }
 ],
 "sources": [
  "BC-CON-04009",
  "BC-SKL-04023",
  "BC-SKL-04026",
  "BC-SKL-04027",
  "BC-EK-CHA-3E1",
  "ced:86",
  "ced:91",
  "BC-QA-04006",
  "BC-QA-04007",
  "BC-PT-99023",
  "cr-24:18",
  "crabbc-25:25",
  "BC-ERR-04020",
  "BC-ERR-04022",
  "BC-ERR-99013",
  "BC-MIS-04011",
  "BC-MIS-04008",
  "BC-PRQ-04007",
  "BC-PRQ-04008",
  "research/units/unit-04-contextual-applications-differentiation.md#4.5 Solving Related Rates Problems",
  "research/question-analysis/question-archetypes.md#BC-QA-04006 Related rates in a geometric setting",
  "research/question-analysis/question-archetypes.md#BC-QA-04007 Related rates on an implicitly defined curve",
  "research/exam/exam-structure.md#Section and part layout"
 ],
 "word_count": {
  "full": 578,
  "brief": 450
 },
 "read_minutes": {
  "full": 3.9,
  "brief": 3.0
 }
}
```
