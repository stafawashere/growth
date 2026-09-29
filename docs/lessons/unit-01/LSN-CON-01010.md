---
title: LSN-CON-01010 The squeeze theorem
research_date: 2026-09-29
status: designed
purpose: Authoring spec for the concept lesson on BC-CON-01010, the squeeze theorem, built from authoring_bundle("BC-CON-01010") and the research files it cites, so an author fills plan 15's lesson record without making a teaching decision.
---

# LSN-CON-01010 The squeeze theorem

Concept BC-CON-01010 (skills BC-SKL-01032 to BC-SKL-01035), topic 1.8 of Unit 1, loaded by BC-QA-01005 (primary). The unit attack map places it tenth, after BC-CON-01009, and its delivery map picks motion for the key idea.

## Orientation

Served text, from BC-CON-01010 `description_plain` and the topic's Assessment behaviour paragraph (research/units/unit-01-limits-continuity.md#1.8 Determining Limits Using the Squeeze Theorem): MCQ forms supply the inequality and ask for the limit; FRQ forms would demand the inequality and the two bound limits as separate steps. Stated as what a response shows. No count, no frequency. Delivered as a figure (Delivery).

## Key ideas

All four skills map to BC-EK-LIM-1E2 (ced:45): one core block, both bands.

- ki-1 (core). Paraphrase of the topic's Required mathematical knowledge paragraph (Squeeze theorem; Hypotheses as a separate demand, BC-MPS-3C on ced:45) and of BC-SKL-01035 (bound the oscillating part between negative one and one and multiply through). Anchor quote (13 words) from ced:45. Notation line from the concept record and the topic: squeeze theorem; the inequality written with the trapped function in the middle.

## Recognition

- BC-QA-01005 (family squeeze-theorem, one FRQ part or a single MCQ, no calculator; research/question-analysis/question-archetypes.md#BC-QA-01005 Limit determined by the squeeze theorem with its hypotheses stated). `typical_wording`: "The stated inequality holds near the given input. Use it to determine the limit of the trapped function and justify your answer." `common_givens`: a function trapped between two bounding functions; a bounding inequality that holds near the input. `asked_to_produce`: a bounding inequality, the limits of the two bounds, the limit with justification. No official example. The signal is a sine or cosine of a reciprocal, or any factor with no limit of its own, multiplied by a factor that vanishes at the target, or a supplied inequality.

What says "not this concept": every factor has its own limit, so the product theorem settles it (BC-CON-01007; unit-01 README, Squeeze against direct substitution); a quotient giving zero over zero with polynomial parts (BC-CON-01008).

## Method choice

- st-1, BC-QA-01005, low and mid bands, verified (`asked_to_produce` and `common_givens` present). Method, `expected_solution_path[0]`: bound the oscillating factor between fixed values. Rival, `wrong_approaches`: substituting the target into the bounds instead of taking their limits (BC-ERR-01013). Separating feature: the oscillating factor has no limit, so the product theorem cannot be used and the bounds must be built.

## Solution path

- ex-1, BC-QA-01005, both bands, no calculator. Draw: target 1, shift 2, coefficient 3, power 1, wave sin, naming open, giving \(f(x)=2+3(x-1)\sin\frac{1}{x-1}\) (the `parameter_spec` notes). Power 1 makes the vanishing factor negative left of 1, the case the constraint forces. No published BC-QA-01005 draw matches. Steps follow `expected_solution_path`: bound the oscillation (no value); multiply and record the direction, written with \(3|x-1|\) so one inequality holds on both sides [inferred] (lower bound `new`); the two bound limits (`limit`, each after its bound); the conclusion (no value).

A fluent solver writes the inequality, both bound limits and the conclusion, and holds the bound on the sine in the head [inferred].

## Scoring

None. BC-QA-01005 lists no `point_types`; its `scoring_pattern` names three points (inequality, bound limits, conclusion) with no official free response part in 2023 to 2025 (research/question-analysis/question-archetypes.md#BC-QA-01005 Limit determined by the squeeze theorem with its hypotheses stated), so no `what_a_reader_scores` entry and no point tag. For the author only: hypothesis verification is the family the research describes for other theorems (research/scoring/common-point-losses.md#Justification points; research/scoring/justification-requirements.md#Theorem hypotheses); the lesson does not state a point.

## Traps

Three active errors meet the skills, in the bundle's order (BC-ERR-01012 and 01013 link BC-MIS-01008, medium; BC-ERR-99008 links BC-MIS-99009, high). Low band all three, mid band the first two. All on ex-1's draw.

- err-BC-ERR-01012. Wrong: \(2-3(x-1)\) as the lower bound. Right: \(2-3|x-1|\). Distinct. Reason, words from BC-MIS-01008.
- err-BC-ERR-01013. Wrong: the bound evaluated at 1, value 2. Right: the bound's limit, 2. Equivalent: the value agrees, the theorem is not applied, which is the record's consequence. Reason, words from BC-MIS-01008.
- err-BC-ERR-99008. Wrong: the conclusion 2 with no inequality. Right: the bound \(3|x-1|\) on the oscillating product shown first. Distinct. Reason, words from BC-MIS-99009. The record names other theorems; its skills include this concept's, and the block reads it as the squeeze hypotheses [inferred].

## Representations

None as a separate block. The topic's Representations paragraph names one graphical conversion (a graph showing the trapped curve to the stated inequality); the orientation figure and the ki-1 motion carry it, so a third figure would add a representation with nothing new to read.

## Prerequisite bridge

Two BC-PRQ parents, supporting edges, gated by state: BC-PRQ-01005 (bounds on sine and cosine) and BC-PRQ-01010 (interval notation). Each restates `description_plain` and names the `failure_signature`.

## Time

BC-QA-01005 is `no_calculator`, one FRQ part or a single MCQ. The MCQ shape is Section I Part A, 2.14 minutes (research/exam/exam-structure.md#Section and part layout); the FRQ shape has no official example to fix its share [inferred]. On the MCQ a fluent solver writes the bound line and reads the limit; on a free response part every valued line of ex-1 is written, and the sine bound (step 1) is held in the head [inferred].

## Checks

- chk-1, completion of ex-1, both bands: the inequality is given, the student takes the limits. Key 2.
- chk-2, isomorph, both bands: target \(-2\), shift \(-1\), coefficient \(-2\), power 2, wave cos, naming named. Key \(-1\).
- chk-3, MCQ, low band, key form statement: which line justifies \(\lim_{x\to0}(3+x^3\sin\frac1x)=3\). Every option reaches 3, so the options are justifications, not values: the three errors change the argument, not the number. Distractors carry BC-ERR-01013 (bounds evaluated at 0), BC-ERR-01012 (\(x^3\) bounds not reversed for \(x<0\)), BC-ERR-99008 (theorem named, hypotheses unshown).

## Delivery

- orientation: figure. Rule 3, BC-REP-02 on BC-SKL-01033 and BC-SKL-01035; the unit-01 README gives figure. Spec: the two bounds dashed, \(f\) solid, the open point \((1,2)\), labels inside.
- ki-1: motion. Rule 2, a limit being taken (the bounds pinching toward 1), as the README names. Three frames at half-widths 1, 0.1 and 0.01; arrow keys step; reduced motion cross-fades on key press; the fallback is the static strip.
- ex-1 and the three error blocks: step_reveal. Rule 1.

Every non-text choice is [inferred], settled by the modality A/B.

## Band plan

- Low (full): orientation, ki-1, st-1, ex-1, err-BC-ERR-01012, err-BC-ERR-01013, err-BC-ERR-99008, chk-1, chk-2, chk-3, two bridges when gated in. 572 words, 3.9 minutes (cap 900 and 6).
- Mid (brief): orientation, ki-1, st-1, ex-1, err-BC-ERR-01012, err-BC-ERR-01013, chk-1, chk-2, bridges when gated in. 449 words, 3.0 minutes (cap 450 and 3).
- Refresher: ki-1, the three error blocks, ex-1.

## Sources

- BC-CON-01010; BC-SKL-01032, BC-SKL-01033, BC-SKL-01034, BC-SKL-01035; BC-EK-LIM-1E2; ced:45
- BC-QA-01005
- BC-ERR-01012, BC-ERR-01013, BC-ERR-99008; BC-MIS-01008, BC-MIS-99009
- BC-PRQ-01005, BC-PRQ-01010
- research/units/unit-01-limits-continuity.md#1.8 Determining Limits Using the Squeeze Theorem
- research/question-analysis/question-archetypes.md#BC-QA-01005 Limit determined by the squeeze theorem with its hypotheses stated
- research/exam/exam-structure.md#Section and part layout
- research/scoring/common-point-losses.md#Justification points
- research/scoring/justification-requirements.md#Theorem hypotheses
- [inferred] Non-text delivery modes. Settled by the modality A/B.
- [inferred] The absolute value form of the bound. Settled by an official guideline or CED example.
- [inferred] BC-ERR-99008 read as the squeeze hypotheses. Settled by a squeeze-scoped error record.
- [inferred] Part I-A for the squeeze archetype. Settled by an official FRQ part with a guideline.

## Machine record

```json
{
 "id": "LSN-CON-01010",
 "kind": "concept",
 "target_id": "BC-CON-01010",
 "unit": "01",
 "skills": [
  "BC-SKL-01032",
  "BC-SKL-01033",
  "BC-SKL-01034",
  "BC-SKL-01035"
 ],
 "orientation": {
  "text": "A response shows the trapped function between two bounds near the target, the limit of each bound, and the conclusion that the trapped function shares that limit. The inequality is either supplied or built from an oscillating factor.",
  "sources": [
   "BC-CON-01010",
   "research/units/unit-01-limits-continuity.md#1.8 Determining Limits Using the Squeeze Theorem"
  ]
 },
 "key_ideas": [
  {
   "id": "ki-1",
   "ek_id": "BC-EK-LIM-1E2",
   "depth": "core",
   "text": "If \\(g(x)\\le f(x)\\le h(x)\\) for all \\(x\\) near \\(c\\), except possibly at \\(c\\), and \\(g\\) and \\(h\\) both have limit \\(L\\) at \\(c\\), then \\(\\lim_{x\\to c}f(x)=L\\). The hypotheses are their own demand: the inequality is shown to hold near \\(c\\), and each bound's limit is taken. The usual case bounds an oscillating factor between \\(-1\\) and 1, then multiplies through by the vanishing factor.",
   "notation": "squeeze theorem; the inequality written with the trapped function in the middle",
   "quote": {
    "text": "The limit of a function may be found by using the squeeze theorem.",
    "source": "ced:45"
   },
   "sources": [
    "BC-EK-LIM-1E2",
    "ced:45",
    "research/units/unit-01-limits-continuity.md#1.8 Determining Limits Using the Squeeze Theorem"
   ]
  }
 ],
 "strategy": [
  {
   "id": "st-1",
   "archetype_id": "BC-QA-01005",
   "cue": "A function trapped between two bounds, or an oscillating factor times a vanishing factor, with the limit asked.",
   "method": "First line: bound the oscillating factor between fixed values.",
   "rival": "Rival: substituting the target into the bounds instead of taking their limits (BC-ERR-01013).",
   "separating_feature": "The oscillating factor has no limit of its own, so the product theorem has nothing to multiply.",
   "sources": [
    "BC-QA-01005"
   ],
   "evidence_tag": "verified"
  }
 ],
 "worked_examples": [
  {
   "id": "ex-1",
   "archetype_id": "BC-QA-01005",
   "bands": [
    "low",
    "mid"
   ],
   "parameter_draw": {
    "target": 1,
    "shift": 2,
    "coefficient": 3,
    "power": 1,
    "wave": "sin",
    "naming": "open"
   },
   "problem": {
    "text": "Let \\(f(x)=2+3(x-1)\\sin\\frac{1}{x-1}\\). Find \\(\\lim_{x\\to1}f(x)\\) and justify the answer.",
    "command_verb": "find"
   },
   "calculator_status": "no_calculator",
   "steps": [
    {
     "cue": "\\(\\sin\\frac{1}{x-1}\\) oscillates near 1 and has no limit there.",
     "why": "It is bounded: \\(-1\\le\\sin\\frac{1}{x-1}\\le1\\) for every \\(x\\ne1\\)."
    },
    {
     "cue": "The vanishing factor \\(3(x-1)\\) is negative left of 1.",
     "why": "Bounding by \\(3|x-1|\\) keeps one inequality valid on both sides: \\(f(x)\\ge2-3|x-1|\\).",
     "expr": "2 - 3*Abs(x-1)",
     "relation": "new"
    },
    {
     "cue": "The stem asks for a limit, so take the limit of the lower bound.",
     "why": "\\(2-3|x-1|\\to2\\) as \\(x\\to1\\).",
     "expr": "2",
     "relation": "limit",
     "variable": "x",
     "point": "1"
    },
    {
     "cue": "The same bound gives \\(f(x)\\le2+3|x-1|\\).",
     "why": "The upper bound is needed too; one side alone traps nothing.",
     "expr": "2 + 3*Abs(x-1)",
     "relation": "new"
    },
    {
     "cue": "Take the limit of the upper bound.",
     "why": "\\(2+3|x-1|\\to2\\) as \\(x\\to1\\).",
     "expr": "2",
     "relation": "limit",
     "variable": "x",
     "point": "1"
    },
    {
     "cue": "Both bounds tend to 2 and trap \\(f\\) near 1.",
     "why": "By the squeeze theorem, \\(\\lim_{x\\to1}f(x)=2\\)."
    }
   ],
   "answer": {
    "form": "numeric",
    "expr": "2"
   }
  }
 ],
 "what_a_reader_scores": [],
 "common_errors": [
  {
   "error_id": "BC-ERR-01012",
   "observed_behavior": "The response multiplies the bounding inequality by a factor that is negative on one side of the target without reversing the inequality there.",
   "scoring_consequence": "The point for establishing the bounding inequality is lost.",
   "wrong_step": {
    "text": "Multiplying by \\(3(x-1)\\) without reversal: \\(2-3(x-1)\\le f(x)\\), false for \\(x<1\\).",
    "expr": "2 - 3*(x-1)"
   },
   "right_step": {
    "text": "With \\(3|x-1|\\): \\(2-3|x-1|\\le f(x)\\) on both sides.",
    "expr": "2 - 3*Abs(x-1)"
   },
   "relation": "distinct",
   "possible_reason": {
    "misconception_id": "BC-MIS-01008",
    "text": "handles the inequality as an equation"
   },
   "sources": [
    "BC-ERR-01012",
    "BC-MIS-01008"
   ]
  },
  {
   "error_id": "BC-ERR-01013",
   "observed_behavior": "The response substitutes the target input into the bounding functions rather than evaluating their limits.",
   "scoring_consequence": "The conclusion point is lost because the theorem has not been applied.",
   "wrong_step": {
    "text": "\\(x=1\\) is put into the bound: \\(2-3|1-1|=2\\).",
    "expr": "2 - 3*Abs(1-1)"
   },
   "right_step": {
    "text": "The limit of the bound: \\(\\lim_{x\\to1}(2-3|x-1|)=2\\).",
    "expr": "2"
   },
   "relation": "equivalent",
   "possible_reason": {
    "misconception_id": "BC-MIS-01008",
    "text": "treats the bounding functions as things to evaluate at the target rather than as functions whose limits must agree"
   },
   "sources": [
    "BC-ERR-01013",
    "BC-MIS-01008"
   ]
  },
  {
   "error_id": "BC-ERR-99008",
   "observed_behavior": "Responses apply the Mean Value Theorem, the Intermediate Value Theorem or L'Hospital's Rule without establishing continuity from differentiability, without bounding the target value between two function values, or without confirming the indeterminate form.",
   "scoring_consequence": "The condition point is not earned; in several years this was the point earned by the smallest proportion of responses on the question.",
   "wrong_step": {
    "text": "The limit is stated as 2 by the squeeze theorem, with no inequality shown.",
    "expr": "2"
   },
   "right_step": {
    "text": "First shown: \\(\\left|3(x-1)\\sin\\frac{1}{x-1}\\right|\\le3|x-1|\\) for \\(x\\ne1\\).",
    "expr": "3*Abs(x-1)"
   },
   "relation": "distinct",
   "possible_reason": {
    "misconception_id": "BC-MIS-99009",
    "text": "applies it without establishing the conditions"
   },
   "sources": [
    "BC-ERR-99008",
    "BC-MIS-99009"
   ]
  }
 ],
 "representations": null,
 "prerequisite_bridges": [
  {
   "prq_id": "BC-PRQ-01005",
   "text": "Sine and cosine stay between \\(-1\\) and 1. Treating an oscillating factor as unbounded marks this gap."
  },
  {
   "prq_id": "BC-PRQ-01010",
   "text": "Read open and closed intervals as inequalities. A conclusion stated on the wrong interval marks this gap."
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
    5,
    6
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
   "archetype_id": "BC-QA-01005",
   "parameter_draw": {
    "target": 1,
    "shift": 2,
    "coefficient": 3,
    "power": 1,
    "wave": "sin",
    "naming": "open"
   },
   "completes": "ex-1",
   "stem": {
    "text": "For \\(x\\ne1\\), \\(2-3|x-1|\\le f(x)\\le2+3|x-1|\\). Find \\(\\lim_{x\\to1}f(x)\\).",
    "command_verb": "find"
   },
   "key": {
    "form": "numeric",
    "expr": "2"
   },
   "steps": [
    {
     "text": "The upper bound.",
     "expr": "2 + 3*Abs(x-1)",
     "relation": "new"
    },
    {
     "text": "Its limit at 1 is 2, as is the lower bound's.",
     "expr": "2",
     "relation": "limit",
     "variable": "x",
     "point": "1"
    }
   ],
   "calculator_status": "no_calculator",
   "skills": [
    "BC-SKL-01034"
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
   "archetype_id": "BC-QA-01005",
   "parameter_draw": {
    "target": -2,
    "shift": -1,
    "coefficient": -2,
    "power": 2,
    "wave": "cos",
    "naming": "named"
   },
   "stem": {
    "text": "Use the squeeze theorem to find \\(\\lim_{x\\to-2}\\left(-1-2(x+2)^2\\cos\\frac{1}{x+2}\\right)\\).",
    "command_verb": "find"
   },
   "key": {
    "form": "numeric",
    "expr": "-1"
   },
   "steps": [
    {
     "text": "Upper bound \\(-1+2(x+2)^2\\).",
     "expr": "-1 + 2*(x+2)**2",
     "relation": "new"
    },
    {
     "text": "Its limit at \\(-2\\).",
     "expr": "-1",
     "relation": "limit",
     "variable": "x",
     "point": "-2"
    }
   ],
   "calculator_status": "no_calculator",
   "skills": [
    "BC-SKL-01035"
   ]
  },
  {
   "id": "chk-3",
   "check_kind": "mcq",
   "format": "mcq",
   "bands": [
    "low"
   ],
   "archetype_id": "BC-QA-01005",
   "parameter_draw": {
    "target": 0,
    "shift": 3,
    "coefficient": 1,
    "power": 3,
    "wave": "sin",
    "naming": "open"
   },
   "stem": {
    "text": "Which line justifies \\(\\lim_{x\\to0}\\left(3+x^3\\sin\\frac{1}{x}\\right)=3\\)?",
    "command_verb": "identify"
   },
   "key": {
    "form": "statement",
    "expr": "abs_bounds_then_limits"
   },
   "steps": [
    {
     "text": "Upper bound \\(3+|x|^3\\).",
     "expr": "3 + Abs(x)**3",
     "relation": "new"
    },
    {
     "text": "Its limit at 0.",
     "expr": "3",
     "relation": "limit",
     "variable": "x",
     "point": "0"
    }
   ],
   "options": [
    {
     "id": "A",
     "is_key": false,
     "label": "At \\(x=0\\) the bounds \\(3-|x|^3\\) and \\(3+|x|^3\\) both equal 3.",
     "error_path": "BC-ERR-01013",
     "derivation": "bounds evaluated at the target"
    },
    {
     "id": "B",
     "is_key": false,
     "label": "\\(3-x^3\\le f(x)\\le3+x^3\\) near 0, and both bounds tend to 3.",
     "error_path": "BC-ERR-01012",
     "derivation": "inequality not reversed where x cubed is negative"
    },
    {
     "id": "C",
     "is_key": false,
     "label": "The limit is 3 by the squeeze theorem.",
     "error_path": "BC-ERR-99008",
     "derivation": "hypotheses not verified"
    },
    {
     "id": "D",
     "is_key": true,
     "label": "\\(3-|x|^3\\le f(x)\\le3+|x|^3\\) for \\(x\\ne0\\), and both bounds tend to 3.",
     "error_path": null
    }
   ],
   "calculator_status": "no_calculator",
   "skills": [
    "BC-SKL-01032",
    "BC-SKL-01033",
    "BC-SKL-01034"
   ]
  }
 ],
 "delivery": [
  {
   "block": "orientation",
   "mode": "figure",
   "reason": "rule 3: BC-REP-02 on BC-SKL-01033 and BC-SKL-01035 (unit-01 README delivery map)",
   "sources": [
    "BC-SKL-01033",
    "BC-SKL-01035"
   ],
   "spec": {
    "kind": "graph",
    "window": {
     "x": [
      0,
      2
     ],
     "y": [
      -1,
      5
     ]
    },
    "curves": [
     {
      "expr": "2 - 3*Abs(x-1)",
      "style": "dashed",
      "label": {
       "text": "lower bound",
       "placement": "inside"
      }
     },
     {
      "expr": "2 + 3*Abs(x-1)",
      "style": "dashed",
      "label": {
       "text": "upper bound",
       "placement": "inside"
      }
     },
     {
      "expr": "2 + 3*(x-1)*sin(1/(x-1))",
      "style": "solid",
      "label": {
       "text": "f",
       "placement": "inside"
      }
     }
    ],
    "points": [
     {
      "x": 1,
      "y": 2,
      "style": "open",
      "label": {
       "text": "(1, 2)",
       "placement": "inside"
      }
     }
    ],
    "labels": [
     {
      "text": "trapped between the bounds",
      "placement": "inside"
     }
    ],
    "representations": [
     "graph"
    ]
   },
   "fallback": "Alt text and the inequality \\(2-3|x-1|\\le f(x)\\le2+3|x-1|\\) in words, with the point \\((1,2)\\) named.",
   "keyboard": "none needed: a static figure"
  },
  {
   "block": "ki-1",
   "mode": "motion",
   "reason": "rule 2: a limit being taken, the bounds pinching toward the input; rule 3, BC-REP-02 on BC-SKL-01033 and BC-SKL-01035",
   "sources": [
    "BC-SKL-01033",
    "BC-SKL-01035"
   ],
   "spec": {
    "kind": "graph_sweep",
    "parameter": "half-width of the window about x = 1",
    "curves": [
     {
      "expr": "2 - 3*Abs(x-1)",
      "label": {
       "text": "g",
       "placement": "inside"
      }
     },
     {
      "expr": "2 + 3*Abs(x-1)",
      "label": {
       "text": "h",
       "placement": "inside"
      }
     },
     {
      "expr": "2 + 3*(x-1)*sin(1/(x-1))",
      "label": {
       "text": "f",
       "placement": "inside"
      }
     }
    ],
    "frames": [
     {
      "window": {
       "x": [
        0,
        2
       ],
       "y": [
        -1,
        5
       ]
      },
      "label": {
       "text": "half-width 1",
       "placement": "inside"
      }
     },
     {
      "window": {
       "x": [
        0.9,
        1.1
       ],
       "y": [
        1.7,
        2.3
       ]
      },
      "label": {
       "text": "half-width 0.1",
       "placement": "inside"
      }
     },
     {
      "window": {
       "x": [
        0.99,
        1.01
       ],
       "y": [
        1.97,
        2.03
       ]
      },
      "label": {
       "text": "half-width 0.01",
       "placement": "inside"
      }
     }
    ],
    "labels": [
     {
      "text": "g and h meet at height 2",
      "placement": "inside"
     }
    ],
    "representations": [
     "graph"
    ]
   },
   "fallback": "The three frames as a static strip, each labelled with its half-width, the gap between g and h stated under each.",
   "keyboard": "Left and right arrow keys step between frames; Home returns to the first frame.",
   "reduced_motion": "No auto-advance; each key press cross-fades to the next frame."
  },
  {
   "block": "ex-1",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  },
  {
   "block": "err-BC-ERR-01012",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  },
  {
   "block": "err-BC-ERR-01013",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  },
  {
   "block": "err-BC-ERR-99008",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  }
 ],
 "refresher": [
  "ki-1",
  "err-BC-ERR-01012",
  "err-BC-ERR-01013",
  "err-BC-ERR-99008",
  "ex-1"
 ],
 "research_lines": [
  {
   "file": "research/question-analysis/question-archetypes.md",
   "line": "No official free response part in 2023 to 2025 assesses the squeeze theorem."
  }
 ],
 "inferred": [
  {
   "claim": "The non-text delivery modes chosen here serve the content better than text and step reveal.",
   "settles": "The modality A/B in the build plan: skip rate and time to first credited success by mode."
  },
  {
   "claim": "Bounding by the absolute value of the vanishing factor, rather than splitting the two sides, is the first written inequality a fluent solver uses.",
   "settles": "An official scoring guideline or CED example writing the squeeze inequality with an absolute value."
  },
  {
   "claim": "BC-ERR-99008 is linked to this concept's skills though its record names the Mean Value Theorem, the IVT and L'Hospital's Rule; its block is read here as the squeeze hypotheses not verified.",
   "settles": "An error record scoped to the squeeze theorem's hypotheses, or a record note extending BC-ERR-99008 to it."
  },
  {
   "claim": "The squeeze archetype sits in Section I Part A; no free response part in 2023 to 2025 assesses it.",
   "settles": "An official free response part on the squeeze theorem with its scoring guideline."
  }
 ],
 "sources": [
  "BC-CON-01010",
  "BC-SKL-01032",
  "BC-SKL-01033",
  "BC-SKL-01034",
  "BC-SKL-01035",
  "BC-EK-LIM-1E2",
  "ced:45",
  "BC-QA-01005",
  "BC-ERR-01012",
  "BC-ERR-01013",
  "BC-ERR-99008",
  "BC-MIS-01008",
  "BC-MIS-99009",
  "BC-PRQ-01005",
  "BC-PRQ-01010",
  "research/units/unit-01-limits-continuity.md#1.8 Determining Limits Using the Squeeze Theorem",
  "research/question-analysis/question-archetypes.md#BC-QA-01005 Limit determined by the squeeze theorem with its hypotheses stated",
  "research/exam/exam-structure.md#Section and part layout",
  "research/scoring/justification-requirements.md#Theorem hypotheses",
  "research/scoring/common-point-losses.md#Justification points"
 ],
 "read_minutes": {
  "full": 3.9,
  "brief": 3.0
 },
 "word_count": {
  "full": 572,
  "brief": 449
 }
}
```
