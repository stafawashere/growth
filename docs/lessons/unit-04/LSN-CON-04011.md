---
title: LSN-CON-04011 The tangent line as a local linear approximation
research_date: 2026-09-29
status: designed
purpose: Authoring spec for the concept lesson on BC-CON-04011, approximating a function value near a point by the tangent line there, built from authoring_bundle("BC-CON-04011") and the research files it cites.
---

# LSN-CON-04011 The tangent line as a local linear approximation

Concept BC-CON-04011 (skills BC-SKL-04028, BC-SKL-04029, BC-SKL-04032), topic 4.6, loaded by BC-QA-04008 (family tangent-line-approximation). No hard parent in the unit (docs/lessons/unit-04/README.md, section 1).

## Orientation

Served text, from BC-CON-04011 `description_plain` and the topic's Assessment behaviour paragraph (research/units/unit-04-contextual-applications-differentiation.md#4.6 Approximating Values of a Function Using Local Linearity and Linearization): a response finds the slope at the point of tangency, writes the tangent line in point-slope form, and evaluates it at the nearby input, leaving the arithmetic unsimplified where it can.

## Key ideas

All three skills map to BC-EK-CHA-3F1 (ced:92), one core block.

- ki-1 (core). Paraphrase of "Local linearity", "Tangent line" and "Implicit curves": near the point of tangency the line and curve are close, so the line's height at a nearby input approximates the function; the slope is the derivative at the point, with both coordinates put in when dy/dx involves y; isolating y is not required (crabbc-25:25). Anchor quote from ced:92.

## Recognition

BC-QA-04008 (research/question-analysis/question-archetypes.md#BC-QA-04008 Tangent line approximation with an over or under estimate judgement): `typical_wording` "use the line tangent to the curve at the stated point to approximate the value of the function at a nearby input"; `common_givens` a supplied dy/dx or differential equation with a point, "the point of tangency and a nearby input"; `asked_to_produce` the slope and the approximation. The signal: two inputs, one where f is known and one nearby, and the word approximate. Shapes: MCQ, or one FRQ part after the part that produced the derivative (BC-FRQ-2023-Q3-B, BC-FRQ-2014-Q1-D).

Not this concept: "write an equation for the tangent line" with no second input (BC-QA-02011, the line alone).

## Method choice

- st-1, BC-QA-04008. Method, `expected_solution_path[0]`: the slope at the point of tangency, then point-slope form. Rival from `wrong_approaches`: evaluating the line at the point of tangency (BC-ERR-04024), or solving the differential equation (BC-ERR-99035). Separating feature: the derivative is supplied, so it is evaluated, never solved.

## Solution path

- ex-1, BC-QA-04008, both bands, no calculator. Draw: curvature 2, offset -3, anchor 1, height 4, step 1/10, judgement off; f(1) = 4, f'(x) = 2x^2 - 3, approximate f(1.1). Not a published draw.
- Steps: f' (new); slope at 1 (evaluate); the line (new); the line at 1.1 (evaluate). A fluent solver writes the slope value, the line and the evaluated line unsimplified.

## Scoring

BC-QA-04008 lists BC-PT-99025, BC-PT-99068, BC-PT-99004 and BC-PT-99005. ex-1 tags BC-PT-99025 on the slope and the approximation. For the author: unrequired simplification can lose a secured point (research/scoring/common-point-losses.md#Answer points); the 2025 report records sign and parenthesis errors while isolating y (crabbc-25:25).

## Traps

Five active errors meet the skills; the first four in the bundle's order are served: BC-ERR-04024, BC-ERR-99035, BC-ERR-04023, BC-ERR-04027. BC-ERR-99022 is fifth and falls outside the four-block cap. BC-ERR-04027's record describes a derivative in both coordinates evaluated off the point of tangency; ex-1 supplies f'(x) in x alone, so the block shows the same slip as f' evaluated at the nearby input, an [inferred] carry-over. On ex-1's draw; mid band the first two.

- err-BC-ERR-04024: the line at x = 1 returns 4. Reason words from BC-MIS-04012.
- err-BC-ERR-99035: f''(1) = 4 used for the slope. Reason words from BC-MIS-07002.
- err-BC-ERR-04023: slope and height exchanged. No reason line.
- err-BC-ERR-04027: f' evaluated at the nearby input 1.1, slope -29/50 in place of f'(1) = -1. Reason words from BC-MIS-04012.

## Representations

None as a separate block; the orientation figure and ki-1's motion carry the curve and tangent (BC-REP-02). Both draw the true f(x) = (2/3)x^3 - 3x + 19/3, the antiderivative of 2x^2 - 3 through (1, 4).

## Prerequisite bridge

- BC-PRQ-04006, from `description_plain` and `failure_signature`.

## Time

BC-QA-04008 has `calculator_status` either, so Section I Part A, 2.14 minutes (research/exam/exam-structure.md#Section and part layout) [inferred]. Written: slope value, point-slope line, the line at the nearby input. Skipped: isolating y and simplifying (crabbc-25:25).

## Checks

- chk-1, completion of ex-1, both bands. Key 39/10.
- chk-2, isomorph, both bands: curvature 3, offset -1, anchor 1, height -2, step 1/5. Key -8/5.
- chk-3, MCQ, low band: curvature -1, offset 5, anchor 2, height 3, step -1/5. Key 14/5. Distractors: 3 (BC-ERR-04024), 2/5 (BC-ERR-04023), 331/125 (BC-ERR-04027: slope f'(1.8) = 44/25 in the line through (2, 3), at 1.8).

## Delivery

- orientation: figure. Rule 3: BC-REP-02 in BC-SKL-04028 and BC-SKL-04029 [inferred].
- ki-1: motion. Rule 2: BC-EK-CHA-3F1 describes closeness near the point of tangency, a process of approach (docs/lessons/unit-04/README.md, section 6) [inferred].
- ex-1 and the four error blocks: step_reveal. Rule 1.

## Band plan

- Low (full): orientation, ki-1, st-1, ex-1 with its scoring line, four error blocks, chk-1 to chk-3, the bridge. 551 words, 3.71 minutes (cap 900 and 6).
- Mid (brief): orientation, ki-1, st-1, ex-1 with its scoring line, err-BC-ERR-04024, err-BC-ERR-99035, chk-1, chk-2, the bridge. 410 words, 2.8 minutes (cap 450 and 3).
- Refresher: ki-1, err-BC-ERR-04024, err-BC-ERR-99035, err-BC-ERR-04023, err-BC-ERR-04027, ex-1.

## Sources

- BC-CON-04011; BC-SKL-04028, BC-SKL-04029, BC-SKL-04032; BC-EK-CHA-3F1; ced:92
- BC-QA-04008, BC-QA-02011; BC-PT-99025; crabbc-25:25
- BC-ERR-04024, BC-ERR-99035, BC-ERR-04023, BC-ERR-04027; BC-MIS-04012, BC-MIS-07002
- BC-PRQ-04006
- research/units/unit-04-contextual-applications-differentiation.md#4.6 Approximating Values of a Function Using Local Linearity and Linearization
- research/question-analysis/question-archetypes.md#BC-QA-04008 Tangent line approximation with an over or under estimate judgement
- research/scoring/common-point-losses.md#Answer points
- research/exam/exam-structure.md#Section and part layout
- [inferred] I-A for an either archetype. Settled by a plan 15 budget rule for calculator_status either.
- [inferred] The figure and motion modes. Settled by the modality A/B.
- [inferred] BC-ERR-04027 shown as f' evaluated at the nearby input, since the draws supply f'(x) in x alone. Settled by a BC-QA-04008 draw with a two-coordinate derivative, or an error record scoped to an explicit f'(x).

## Machine record

```json
{
 "id": "LSN-CON-04011",
 "kind": "concept",
 "target_id": "BC-CON-04011",
 "unit": "04",
 "skills": [
  "BC-SKL-04028",
  "BC-SKL-04029",
  "BC-SKL-04032"
 ],
 "orientation": {
  "text": "Find the slope at the point of tangency, write the tangent line in point-slope form, and evaluate it at the nearby input. Leave the arithmetic unsimplified where it can be.",
  "sources": [
   "BC-CON-04011",
   "research/units/unit-04-contextual-applications-differentiation.md#4.6 Approximating Values of a Function Using Local Linearity and Linearization"
  ]
 },
 "key_ideas": [
  {
   "id": "ki-1",
   "ek_id": "BC-EK-CHA-3F1",
   "depth": "core",
   "text": "Near the point of tangency the curve and its tangent line are close, so the line's height at a nearby input approximates the function there. The slope is the derivative at the point; when dy/dx involves y, both coordinates go in. Point-slope form is enough.",
   "notation": "f(a) + f'(a)(x - a)",
   "quote": {
    "text": "The tangent line is the graph of a locally linear approximation of the function near the point of tangency.",
    "source": "ced:92"
   },
   "sources": [
    "BC-EK-CHA-3F1",
    "ced:92",
    "crabbc-25:25",
    "research/units/unit-04-contextual-applications-differentiation.md#4.6 Approximating Values of a Function Using Local Linearity and Linearization"
   ]
  }
 ],
 "strategy": [
  {
   "id": "st-1",
   "archetype_id": "BC-QA-04008",
   "cue": "A known point, a supplied derivative, \"approximate\" at a nearby input.",
   "method": "First line: the derivative evaluated at the point of tangency.",
   "rival": "Rival: the line evaluated at the point itself (BC-ERR-04024).",
   "separating_feature": "Two inputs: slope from the first, evaluation at the second.",
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
    "curvature": 2,
    "offset": -3,
    "anchor": 1,
    "height": 4,
    "step": "1/10",
    "judgement": "off"
   },
   "problem": {
    "text": "f(1) = 4 and f'(x) = 2x^2 - 3. Use the tangent line at x = 1 to approximate f(1.1).",
    "command_verb": "approximate"
   },
   "calculator_status": "no_calculator",
   "steps": [
    {
     "cue": "The derivative is supplied.",
     "why": "Evaluate it; nothing to solve.",
     "expr": "2*x**2 - 3",
     "relation": "new"
    },
    {
     "cue": "Tangency at x = 1.",
     "why": "Slope there.",
     "expr": "-1",
     "relation": "evaluate",
     "subs": {
      "x": "1"
     },
     "point_type_id": "BC-PT-99025"
    },
    {
     "cue": "Point (1, 4), slope -1.",
     "why": "Point-slope form.",
     "expr": "4 - (x - 1)",
     "relation": "new"
    },
    {
     "cue": "Nearby input 1.1.",
     "why": "Line height approximates f(1.1).",
     "expr": "39/10",
     "relation": "evaluate",
     "subs": {
      "x": "11/10"
     },
     "point_type_id": "BC-PT-99025"
    }
   ],
   "answer": {
    "form": "symbolic",
    "expr": "39/10"
   }
  }
 ],
 "what_a_reader_scores": [
  {
   "example_id": "ex-1",
   "point_type_ids": [
    "BC-PT-99025"
   ],
   "lines": [
    {
     "point_type_id": "BC-PT-99025",
     "text": "Tangent line approximation. Earned by: An approximation computed from a line through the given point whose slope is the declared derivative value (sg-23:10). Not earned by: An unsupported approximation (sg-23:10); an approximation simplified incorrectly (sg-23:10)."
    }
   ]
  }
 ],
 "common_errors": [
  {
   "error_id": "BC-ERR-04024",
   "observed_behavior": "The approximation is produced by substituting the point of tangency rather than the nearby input, so the function value at the known point is returned.",
   "scoring_consequence": "The approximation point is lost.",
   "wrong_step": {
    "text": "At x = 1.",
    "expr": "4"
   },
   "right_step": {
    "text": "At x = 1.1.",
    "expr": "39/10"
   },
   "relation": "distinct",
   "possible_reason": {
    "misconception_id": "BC-MIS-04012",
    "text": "treats the tangent line value as the function value rather than as an approximation"
   },
   "sources": [
    "BC-ERR-04024",
    "BC-MIS-04012"
   ]
  },
  {
   "error_id": "BC-ERR-99035",
   "observed_behavior": "Responses asked for a tangent line or an approximation from a given differential equation first attempt to find the general solution by separation of variables, or compute a second derivative, instead of evaluating the given equation at the point.",
   "scoring_consequence": "The slope point is at risk and the part is often left incomplete, since the unnecessary work consumes the part without producing the requested value.",
   "wrong_step": {
    "text": "f''(1).",
    "expr": "4"
   },
   "right_step": {
    "text": "f'(1).",
    "expr": "-1"
   },
   "relation": "distinct",
   "possible_reason": {
    "misconception_id": "BC-MIS-07002",
    "text": "does not separate a constraint on the rate from a formula for the amount"
   },
   "sources": [
    "BC-ERR-99035",
    "BC-MIS-07002"
   ]
  },
  {
   "error_id": "BC-ERR-04023",
   "observed_behavior": "The point-slope form is assembled incorrectly, so the coordinates appear where the slope belongs or the line does not pass through the point.",
   "scoring_consequence": "The approximation point is lost; the 2025 report records multiple sign and parenthesis errors arising while isolating the dependent variable, which was not required (crabbc-25:25).",
   "wrong_step": {
    "text": "Exchanged.",
    "expr": "-1 + 4*(x - 1)"
   },
   "right_step": {
    "text": "Point-slope.",
    "expr": "4 - (x - 1)"
   },
   "relation": "distinct",
   "possible_reason": null,
   "sources": [
    "BC-ERR-04023"
   ]
  },
  {
   "error_id": "BC-ERR-04027",
   "observed_behavior": "An expression for the derivative involving both coordinates is evaluated at coordinates other than the point of tangency.",
   "scoring_consequence": "The slope point is lost, though the approximation point may still be earned on the incorrect slope (crabbc-25:25).",
   "wrong_step": {
    "text": "f' at the nearby input: f'(1.1) = 2(1.1)^2 - 3.",
    "expr": "2*(11/10)**2 - 3"
   },
   "right_step": {
    "text": "f' at the point of tangency: f'(1) = -1.",
    "expr": "-1"
   },
   "relation": "distinct",
   "possible_reason": {
    "misconception_id": "BC-MIS-04012",
    "text": "the distinction between the two inputs and the question of error direction do not arise"
   },
   "sources": [
    "BC-ERR-04027",
    "BC-MIS-04012",
    "crabbc-25:25"
   ]
  }
 ],
 "representations": null,
 "prerequisite_bridges": [
  {
   "prq_id": "BC-PRQ-04006",
   "text": "A line through a point with a given slope, evaluated at another input; otherwise point and slope get exchanged."
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
    4
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
    "curvature": 2,
    "offset": -3,
    "anchor": 1,
    "height": 4,
    "step": "1/10",
    "judgement": "off"
   },
   "completes": "ex-1",
   "stem": {
    "text": "For ex-1 the tangent line is y = 4 - (x - 1). Approximate f(1.1).",
    "command_verb": "approximate"
   },
   "key": {
    "form": "symbolic",
    "expr": "39/10"
   },
   "steps": [
    {
     "text": "Line.",
     "expr": "4 - (x - 1)",
     "relation": "new"
    },
    {
     "text": "At 1.1.",
     "expr": "39/10",
     "relation": "evaluate",
     "subs": {
      "x": "11/10"
     }
    }
   ],
   "calculator_status": "no_calculator",
   "skills": [
    "BC-SKL-04029"
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
    "curvature": 3,
    "offset": -1,
    "anchor": 1,
    "height": -2,
    "step": "1/5",
    "judgement": "off"
   },
   "stem": {
    "text": "f(1) = -2 and f'(x) = 3x^2 - 1. Use the tangent line at x = 1 to approximate f(1.2).",
    "command_verb": "approximate"
   },
   "key": {
    "form": "symbolic",
    "expr": "-8/5"
   },
   "steps": [
    {
     "text": "f'.",
     "expr": "3*x**2 - 1",
     "relation": "new"
    },
    {
     "text": "Slope.",
     "expr": "2",
     "relation": "evaluate",
     "subs": {
      "x": "1"
     }
    },
    {
     "text": "Line.",
     "expr": "-2 + 2*(x - 1)",
     "relation": "new"
    },
    {
     "text": "At 1.2.",
     "expr": "-8/5",
     "relation": "evaluate",
     "subs": {
      "x": "6/5"
     }
    }
   ],
   "calculator_status": "no_calculator",
   "skills": [
    "BC-SKL-04032"
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
    "curvature": -1,
    "offset": 5,
    "anchor": 2,
    "height": 3,
    "step": "-1/5",
    "judgement": "off"
   },
   "stem": {
    "text": "f(2) = 3 and f'(x) = -x^2 + 5. The tangent line at x = 2 approximates f(1.8) as which value?",
    "command_verb": "identify"
   },
   "key": {
    "form": "symbolic",
    "expr": "14/5"
   },
   "steps": [
    {
     "text": "f'.",
     "expr": "-x**2 + 5",
     "relation": "new"
    },
    {
     "text": "Slope.",
     "expr": "1",
     "relation": "evaluate",
     "subs": {
      "x": "2"
     }
    },
    {
     "text": "Line.",
     "expr": "3 + (x - 2)",
     "relation": "new"
    },
    {
     "text": "At 1.8.",
     "expr": "14/5",
     "relation": "evaluate",
     "subs": {
      "x": "9/5"
     }
    }
   ],
   "options": [
    {
     "id": "A",
     "is_key": false,
     "expr": "3",
     "error_path": "BC-ERR-04024",
     "derivation": "line evaluated at x = 2"
    },
    {
     "id": "B",
     "is_key": true,
     "expr": "14/5",
     "error_path": null
    },
    {
     "id": "C",
     "is_key": false,
     "expr": "2/5",
     "error_path": "BC-ERR-04023",
     "derivation": "y = 1 + 3(x - 2), point and slope exchanged"
    },
    {
     "id": "D",
     "is_key": false,
     "expr": "331/125",
     "error_path": "BC-ERR-04027",
     "derivation": "slope taken at the nearby input, f'(1.8) = 44/25, in the line 3 + (44/25)(x - 2), at x = 1.8"
    }
   ],
   "calculator_status": "no_calculator",
   "skills": [
    "BC-SKL-04029"
   ]
  }
 ],
 "delivery": [
  {
   "block": "orientation",
   "mode": "figure",
   "reason": "rule 3: BC-REP-02 on BC-SKL-04028 and BC-SKL-04029",
   "sources": [
    "BC-SKL-04028",
    "BC-SKL-04029"
   ],
   "spec": {
    "kind": "graph",
    "representations": [
     "BC-REP-02"
    ],
    "window": {
     "x": [
      0.5,
      1.5
     ],
     "y": [
      3,
      5
     ]
    },
    "curves": [
     {
      "expr": "4 - (x - 1)"
     },
     {
      "expr": "2*x**3/3 - 3*x + 19/3"
     }
    ],
    "points": [
     {
      "x": 1,
      "y": 4
     },
     {
      "x": 1.1,
      "y": 3.9
     }
    ],
    "labels": [
     {
      "text": "(1, 4): point of tangency",
      "placement": "inside"
     },
     {
      "text": "x = 1.1: nearby input",
      "placement": "inside"
     }
    ]
   },
   "fallback": "the same graph as a static image with its two labels",
   "keyboard": "none needed: the figure has no control"
  },
  {
   "block": "ki-1",
   "mode": "motion",
   "reason": "rule 2: BC-EK-CHA-3F1 describes closeness near the point of tangency, a process of approach",
   "sources": [
    "BC-SKL-04028",
    "BC-SKL-04029"
   ],
   "spec": {
    "kind": "graph",
    "representations": [
     "BC-REP-02"
    ],
    "center": [
     1,
     4
    ],
    "frames": [
     {
      "half_width": 1
     },
     {
      "half_width": 0.5
     },
     {
      "half_width": 0.2
     },
     {
      "half_width": 0.1
     }
    ],
    "drawn": [
     "curve and tangent line at x = 1",
     "the vertical gap at the nearby input"
    ],
    "labels": [
     {
      "text": "gap at the nearby input",
      "placement": "inside"
     },
     {
      "text": "point of tangency",
      "placement": "inside"
     }
    ],
    "curves": [
     {
      "expr": "2*x**3/3 - 3*x + 19/3"
     },
     {
      "expr": "4 - (x - 1)"
     }
    ],
    "points": [
     {
      "x": 1,
      "y": 4
     },
     {
      "x": "1 + half_width/2",
      "y": "4 - half_width/2 + half_width**2/2 + half_width**3/12"
     },
     {
      "x": "1 + half_width/2",
      "y": "4 - half_width/2"
     }
    ]
   },
   "fallback": "the first and last frames side by side",
   "keyboard": "Right arrow steps to the next zoom frame, Left arrow to the previous; Space pauses auto-advance",
   "reduced_motion": "no auto-advance; each key press cross-fades to the next frame"
  },
  {
   "block": "ex-1",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  },
  {
   "block": "err-BC-ERR-04024",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  },
  {
   "block": "err-BC-ERR-99035",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  },
  {
   "block": "err-BC-ERR-04023",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  },
  {
   "block": "err-BC-ERR-04027",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  }
 ],
 "refresher": [
  "ki-1",
  "err-BC-ERR-04024",
  "err-BC-ERR-99035",
  "err-BC-ERR-04023",
  "err-BC-ERR-04027",
  "ex-1"
 ],
 "research_lines": [
  {
   "file": "research/units/unit-04-contextual-applications-differentiation.md",
   "line": "The tangent line at a point is the graph of a locally linear approximation of the function near the point of tangency"
  }
 ],
 "inferred": [
  {
   "claim": "BC-QA-04008 has calculator_status either, so the exam part is taken as I-A.",
   "settles": "A plan 15 budget rule for calculator_status either."
  },
  {
   "claim": "The orientation figure and the ki-1 motion serve better than text.",
   "settles": "The modality A/B in the build plan: skip rate and time to first credited success by mode."
  },
  {
   "claim": "BC-ERR-04027's record describes a derivative in both coordinates evaluated off the point of tangency; the BC-QA-04008 draws supply f'(x) in x alone, so the block and chk-3 option D show the slip as f' evaluated at the nearby input.",
   "settles": "A BC-QA-04008 draw with an implicit or two-coordinate derivative, or an error record scoped to an explicit f'(x)."
  }
 ],
 "sources": [
  "BC-CON-04011",
  "BC-SKL-04028",
  "BC-SKL-04029",
  "BC-SKL-04032",
  "BC-EK-CHA-3F1",
  "ced:92",
  "BC-QA-04008",
  "BC-QA-02011",
  "BC-PT-99025",
  "crabbc-25:25",
  "BC-ERR-04024",
  "BC-ERR-99035",
  "BC-ERR-04023",
  "BC-ERR-04027",
  "BC-MIS-04012",
  "BC-MIS-07002",
  "BC-PRQ-04006",
  "research/units/unit-04-contextual-applications-differentiation.md#4.6 Approximating Values of a Function Using Local Linearity and Linearization",
  "research/question-analysis/question-archetypes.md#BC-QA-04008 Tangent line approximation with an over or under estimate judgement",
  "research/scoring/common-point-losses.md#Answer points",
  "research/exam/exam-structure.md#Section and part layout"
 ],
 "word_count": {
  "full": 551,
  "brief": 410
 },
 "read_minutes": {
  "full": 3.71,
  "brief": 2.8
 }
}
```
