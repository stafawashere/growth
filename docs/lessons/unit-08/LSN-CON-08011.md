---
title: LSN-CON-08011 Limits of integration from the boundary of the region
research_date: 2026-09-29
status: designed
purpose: Authoring spec for the concept lesson on BC-CON-08011, limits of an area integral taken from where the region begins and ends, built from authoring_bundle("BC-CON-08011") and the research files it cites, so an author fills plan 15's lesson record without making a teaching decision.
---

# LSN-CON-08011 Limits of integration from the boundary of the region

Concept BC-CON-08011 (skills BC-SKL-08020, BC-SKL-08021), topic 8.4 of Unit 8, loaded by one archetype, BC-QA-08008 (family area-between-curves), shared with BC-CON-08010. It has no Unit 8 hard parent and opens the region strand; it is served before LSN-CON-08010 (docs/lessons/unit-08/README.md, section 1).

## Prediction

One multiple choice question on worked example 1's own numbers, asked before the rule is shown: f(x) = -x^2 + 6x - 4 and g(x) = 2x - 1 enclose a region and no vertical line is given, and the student picks the limits of integration. The key is x = 1 and x = 3, ex-1's solved values; the distractors are 1 and 5 (the y values of the meeting points, the input BC-ERR-08019 records) and 3 and 5 (mixed x and y values). The resolution states that the limits solve f = g and that the meeting points' y values are not limits. No verdict word. Sources: BC-CON-08011 and the topic 8.4 section the key idea cites (ced:155).

## Orientation

Served text, from BC-CON-08011 `description_plain` and the topic's Assessment behaviour paragraph (research/units/unit-08-applications-integration.md#8.4 Finding the Area Between Curves Expressed as Functions of x): a response takes the limits from where the curves meet or from the vertical lines that bound the region, solving f(x) = g(x) by hand or with a calculator. No count, no frequency.

## Key ideas

Both skills map to BC-EK-CHA-5A1 (ced:155): one core block, both bands.

- ki-1 (core). Paraphrase of the Required mathematical knowledge paragraph (Limits): the limits are the inputs where the region begins and ends, either given vertical lines or the solutions of f = g; every solution is found and those bounding the region kept (BC-SKL-08020 `adaptive.mastered_if`); on a calculator the crossings are stored rather than retyped (BC-SKL-08021 `adaptive.mastered_if`). Anchor quote from ced:155. Notation line from the concept record.

## Recognition

BC-QA-08008 (research/question-analysis/question-archetypes.md#BC-QA-08008 Area of a region between two curves in x): `typical_wording` "find the area of the shaded region enclosed by the graphs of the two functions"; `common_givens` a figure with a shaded region, one or both curve equations; `asked_to_produce` an integrand, an antiderivative or a numerical value, the area. The signal for this concept is the word "enclosed" or "bounded by the graphs" with no vertical line named: the limits are not in the stem. `difficulty_variables` name the cases: limits needing a numerical solve, and a region bounded by a vertical line rather than an intersection. Official parts: BC-FRQ-2014-Q5-A, BC-FRQ-2022-Q5-A, BC-FRQ-2023-Q5-A.

The near miss served in the contrast pair of st-1 comes from the sibling archetype BC-QA-08010 (family area-between-curves), whose `typical_wording` gives "the total area of the region bounded by the two graphs over the stated interval": the same two curves, but the stated interval supplies the limits and the graphs may cross inside it. The pair differs in the one thing the feature names, an enclosed region with no interval against a stated interval.

What says "not this concept": "for 0 ≤ x ≤ 3" or "the vertical line x = 3" in the stem, where the limits are given.

## Method choice

One strategy block, both bands.

- st-1, BC-QA-08008, carrying the contrast pair. Cue from `asked_to_produce` and `common_givens`, with the reader's own label left off every strategy field. Method, `expected_solution_path[0]` is the upper curve; for this concept the first line written is the equation f(x) = g(x), whose solutions fix the limits the path's second entry needs [inferred reading of the path]. Rival, `wrong_approaches`: integrating over an interval that extends past an intersection (BC-ERR-08019 takes limits from the wrong inputs). Separating feature: no vertical line in the stem means the limits come from f = g.

## Solution path

- ex-1, BC-QA-08008, both bands, no calculator. Draw: left 1, width 2, bulge 1, slope 2, intercept -1, lift 1, limits intersections, presentation formula; so g(x) = 2x - 1, f(x) = -x^2 + 6x - 4, meeting at 1 and 3, area 4/3. No published BC-QA-08008 item carries this draw.
- Steps: the equation f = g (new); its solutions (solve); the integral with those limits (new, tagged BC-PT-99001); the antiderivative at the limits (equivalent); the value (equivalent). A fluent solver writes all five; the interior test at x = 2 is held [inferred].

## Scoring

BC-QA-08008 lists BC-PT-99059, 99003, 99004 and 99001. ex-1 tags BC-PT-99001, the definite integral with correct limits, which is this concept's point; the reader line is `reader_checks(["BC-PT-99001"])` copied exactly. For the author: in 2023 incorrect limits made a response ineligible for the final area point (sg-23:16), and a decimal with fewer than three places loses the answer point (research/scoring/common-point-losses.md#Answer points).

## Traps

Both blocks are fix prompts (`fix_prompt` true, relation distinct). Two active errors meet the skills, in the bundle's order: BC-ERR-08019, BC-ERR-99019. Both bands serve both. On ex-1's draw.

- err-BC-ERR-08019: the meeting points are (1, 1) and (3, 5); their y coordinates 1 and 5 used as limits give -16/3 against 4/3. Possible reason, words from BC-MIS-08012.
- err-BC-ERR-99019: the area reported as 1.3 against 1.333 (the right step is written as a decimal, so the rendered value matches its sentence). No possible reason line: the linked descriptions (BC-MIS-09008, BC-MIS-07023) describe the written expression and the missing context, not the rounding.

## Representations

None as a separate block. The topic's Representations paragraph names equations of the boundary curves to numerical limits (BC-REP-01 to BC-REP-09); ki-1's figure marks the limits at the meeting points.

## Prerequisite bridge

- BC-PRQ-08001, from its `description_plain` and `failure_signature`.
- BC-PRQ-08006, from its `description_plain` and `failure_signature`.

## Time

BC-QA-08008 is `either`; the design takes Section I Part A, 2.14 minutes per question (research/exam/exam-structure.md#Section and part layout) [inferred: an either archetype placed in I-A]. As a free response opening part it is three points, 5.0 minutes (docs/lessons/unit-08/README.md, section 5). The minutes go on the factoring of f - g and on the antiderivative at both limits.

## Checks

- chk-1, completion of ex-1, both bands: with the limits 1 and 3 found, evaluate. Key 4/3.
- chk-2, isomorph, both bands. Draw: left -1, width 4, bulge 1, slope -1, intercept 2, lift 2, intersections, formula; f(x) = -x^2 + x + 5, g(x) = 2 - x, meeting at -1 and 3. Key 32/3.
- chk-3, MCQ, low band. Draw: left 0, width 2, bulge 2, slope 1, intercept -2, lift 1, intersections, formula; f(x) = -2x^2 + 5x - 2, g(x) = x - 2. Key 8/3. Distractors: the y coordinates -2 and 0 as limits, -40/3 (BC-ERR-08019); 2.7 and 2.66 (BC-ERR-99019).

## Delivery

- orientation: figure. Rule 4: BC-REP-02 on BC-SKL-08021; unit README delivery map.
- ki-1: figure. Rule 4, same field: the region with its two meeting points marked and the limits read from them. Not promoted: BC-QA-08008 `difficulty_variables` are presence flags [inferred; settled by the modality A/B].
- ex-1: step_reveal. Rule 1.
- err-BC-ERR-08019, err-BC-ERR-99019: step_reveal. Rule 1.

## Band plan

- Low (full), in served order: prediction, orientation, both bridges, ki-1, st-1 with the contrast pair, ex-1 with its reader line, chk-1, both error blocks, chk-2, chk-3. 456 words, 3.1 minutes (cap 900 and 6). There is no second example, so nothing is faded.
- Mid (brief): prediction, orientation, both bridges, ki-1, st-1 with the contrast pair, ex-1 with its reader line, chk-1, both error blocks, chk-2. 447 words, 3.0 minutes (cap 450 and 3). To fit the cap with the prediction and the contrast pair the orientation, ki-1, the strategy fields, the step cues and whys and the bridges were shortened; the anchor quote and the scoring tag were kept.
- Refresher: ki-1, err-BC-ERR-08019, err-BC-ERR-99019, ex-1.

## Sources

- BC-CON-08011; BC-SKL-08020, BC-SKL-08021; BC-EK-CHA-5A1; ced:155
- BC-QA-08008, BC-QA-08010 (the contrast pair's near miss); BC-PT-99001; sg-23:16
- BC-ERR-08019, BC-ERR-99019; BC-MIS-08012, BC-MIS-09008, BC-MIS-07023
- BC-PRQ-08001, BC-PRQ-08006
- research/units/unit-08-applications-integration.md#8.4 Finding the Area Between Curves Expressed as Functions of x
- research/question-analysis/question-archetypes.md#BC-QA-08008 Area of a region between two curves in x
- research/scoring/common-point-losses.md#Answer points
- research/exam/exam-structure.md#Section and part layout
- [inferred] The first written line is f = g, read from the path's second entry. Settled by an archetype record whose path names the intersection solve.
- [inferred] BC-QA-08008 is either; the lesson takes I-A. Settled by a ruling on which part an either archetype's budget comes from.
- [inferred] BC-PT-99003 and BC-PT-99004 are earned on ex-1 but not tagged, to keep the brief band under 450 words. Settled by a brief cap that exempts reader lines.
- [inferred] The orientation and ki-1 figures, and the held interior test. Settled by the modality A/B and by timing data per step.

## Machine record

```json
{
 "id": "LSN-CON-08011",
 "kind": "concept",
 "target_id": "BC-CON-08011",
 "unit": "08",
 "skills": [
  "BC-SKL-08020",
  "BC-SKL-08021"
 ],
 "prediction": {
  "id": "pr-1",
  "stem": {
   "text": "Predict: \\(f(x)=-x^2+6x-4\\) and \\(g(x)=2x-1\\) enclose a region with no vertical lines given. What are its limits?",
   "command_verb": "predict"
  },
  "format": "mcq",
  "options": [
   {
    "id": "A",
    "label": "\\(x=1\\) and \\(x=5\\)",
    "is_key": false
   },
   {
    "id": "B",
    "label": "\\(x=1\\) and \\(x=3\\)",
    "is_key": true
   },
   {
    "id": "C",
    "label": "\\(x=3\\) and \\(x=5\\)",
    "is_key": false
   }
  ],
  "resolution": "The region begins and ends where the graphs meet. \\(f(x)=g(x)\\) gives \\(x=1\\) and \\(x=3\\), the limits; 1 and 5 are y values.",
  "sources": [
   "BC-CON-08011",
   "ced:155"
  ]
 },
 "orientation": {
  "text": "A response takes the limits from where the curves meet or from the named vertical lines.",
  "sources": [
   "BC-CON-08011",
   "research/units/unit-08-applications-integration.md#8.4 Finding the Area Between Curves Expressed as Functions of x"
  ]
 },
 "key_ideas": [
  {
   "id": "ki-1",
   "ek_id": "BC-EK-CHA-5A1",
   "depth": "core",
   "text": "The limits are the inputs where the region begins and ends: named vertical lines, or the solutions of \\(f(x)=g(x)\\) that bound it. Calculator crossings are stored.",
   "notation": "intersection points as limits",
   "quote": {
    "text": "Areas of regions in the plane can be calculated with definite integrals.",
    "source": "ced:155"
   },
   "sources": [
    "BC-EK-CHA-5A1",
    "ced:155",
    "BC-SKL-08020",
    "BC-SKL-08021",
    "research/units/unit-08-applications-integration.md#8.4 Finding the Area Between Curves Expressed as Functions of x"
   ]
  }
 ],
 "strategy": [
  {
   "id": "st-1",
   "archetype_id": "BC-QA-08008",
   "cue": "Area enclosed by graphs, no vertical line named.",
   "method": "\\(f(x)=g(x)\\), solved for every input; the solutions are the limits.",
   "rival": "Limits from y coordinates.",
   "separating_feature": "No vertical line: the limits come from f = g.",
   "sources": [
    "BC-QA-08008",
    "BC-QA-08010",
    "BC-ERR-08019"
   ],
   "evidence_tag": "verified",
   "contrast": {
    "this": {
     "text": "\\(f(x)=x^2-2x\\) and \\(g(x)=x\\) enclose a region R. Write an integral for its area.",
     "archetype_id": "BC-QA-08008"
    },
    "not_this": {
     "text": "Find the total area between \\(f(x)=x^2-2x\\) and \\(g(x)=x\\) for \\(0\\le x\\le 4\\).",
     "why_not": "The stated interval gives the limits."
    },
    "feature": "The stem names no interval."
   }
  }
 ],
 "worked_examples": [
  {
   "id": "ex-1",
   "archetype_id": "BC-QA-08008",
   "bands": [
    "low",
    "mid"
   ],
   "parameter_draw": {
    "left": 1,
    "width": 2,
    "bulge": 1,
    "slope": 2,
    "intercept": -1,
    "lift": 1,
    "presentation": "formula",
    "limits": "intersections"
   },
   "problem": {
    "text": "Find the area of the region enclosed by \\(f(x)=-x^2+6x-4\\) and \\(g(x)=2x-1\\).",
    "command_verb": "find"
   },
   "calculator_status": "no_calculator",
   "steps": [
    {
     "cue": "No line named: solve \\(f=g\\).",
     "why": "The region starts and ends at \\(f=g\\).",
     "expr": "-x**2 + 6*x - 4 = 2*x - 1",
     "relation": "new"
    },
    {
     "cue": "Collect and factor.",
     "why": "\\(x^2-4x+3=(x-1)(x-3)\\).",
     "expr": "FiniteSet(1, 3)",
     "relation": "solve",
     "variable": "x"
    },
    {
     "cue": "Limits 1 and 3.",
     "why": "Upper minus lower.",
     "expr": "Integral(-x**2 + 6*x - 4 - (2*x - 1), (x, 1, 3))",
     "relation": "new",
     "point_type_id": "BC-PT-99001"
    },
    {
     "cue": "Antiderivative at the limits.",
     "why": "\\(F(x)=-x^3/3+2x^2-3x\\).",
     "expr": "(-9 + 18 - 9) - (-1/3 + 2 - 3)",
     "relation": "equivalent"
    },
    {
     "cue": "An area is asked.",
     "why": "Exact and nonnegative.",
     "expr": "4/3",
     "relation": "equivalent"
    }
   ],
   "answer": {
    "form": "numeric",
    "expr": "4/3"
   }
  }
 ],
 "what_a_reader_scores": [
  {
   "example_id": "ex-1",
   "point_type_ids": [
    "BC-PT-99001"
   ],
   "lines": [
    {
     "point_type_id": "BC-PT-99001",
     "text": "Definite integral expression with correct limits. Earned by: A definite integral whose limits match the requested interval and whose integrand matches the requested quantity, with or without the differential (sg-26:4, sg-22:2). Not earned by: An unsupported numerical value, or a definite integral whose bounds are wrong (sg-22:18). Notation: Differential may be omitted; sg-22:2 accepts dx written for dt. sg-23:8 treats a missing differential as recoverable for this point but restricts later eligibility."
    }
   ]
  }
 ],
 "common_errors": [
  {
   "error_id": "BC-ERR-08019",
   "observed_behavior": "The integral is set up with limits that are not the boundary of the region or the interval requested.",
   "scoring_consequence": "The answer point is lost, and in 2023 incorrect limits also made a response ineligible for the final area point (sg-23:16).",
   "wrong_step": {
    "text": "The y values 1 and 5 as limits.",
    "expr": "Integral(-x**2 + 4*x - 3, (x, 1, 5))"
   },
   "right_step": {
    "text": "The x values 1 and 3.",
    "expr": "Integral(-x**2 + 4*x - 3, (x, 1, 3))"
   },
   "relation": "distinct",
   "possible_reason": {
    "misconception_id": "BC-MIS-08012",
    "text": "chooses limits from the axes of the picture"
   },
   "sources": [
    "BC-ERR-08019",
    "BC-MIS-08012"
   ],
   "fix_prompt": true
  },
  {
   "error_id": "BC-ERR-99019",
   "observed_behavior": "Responses report fewer than three digits after the decimal point, round an intermediate value before it is used again, or read a value off a trace rather than solving for it.",
   "scoring_consequence": "The answer point is not earned; the report notes this recurs across several parts of the same response.",
   "wrong_step": {
    "text": "1.3",
    "expr": "1.3"
   },
   "right_step": {
    "text": "4/3, or 1.333",
    "expr": "1.333"
   },
   "relation": "distinct",
   "possible_reason": null,
   "sources": [
    "BC-ERR-99019"
   ],
   "fix_prompt": true
  }
 ],
 "representations": null,
 "prerequisite_bridges": [
  {
   "prq_id": "BC-PRQ-08001",
   "text": "Two expressions set equal and every solution found; else limits are missing."
  },
  {
   "prq_id": "BC-PRQ-08006",
   "text": "Decimals kept to three places; else a right setup loses its value."
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
    5
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
   "archetype_id": "BC-QA-08008",
   "parameter_draw": {
    "left": 1,
    "width": 2,
    "bulge": 1,
    "slope": 2,
    "intercept": -1,
    "lift": 1,
    "presentation": "formula",
    "limits": "intersections"
   },
   "completes": "ex-1",
   "stem": {
    "text": "The limits are 1 and 3. Evaluate \\(\\int_1^3 (-x^2+4x-3)\\,dx\\).",
    "command_verb": "evaluate"
   },
   "key": {
    "form": "numeric",
    "expr": "4/3"
   },
   "steps": [
    {
     "text": "The integral.",
     "expr": "Integral(-x**2 + 4*x - 3, (x, 1, 3))",
     "relation": "new"
    },
    {
     "text": "\\(F(3)-F(1)\\).",
     "expr": "4/3",
     "relation": "equivalent"
    }
   ],
   "calculator_status": "no_calculator",
   "skills": [
    "BC-SKL-08020"
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
   "archetype_id": "BC-QA-08008",
   "parameter_draw": {
    "left": -1,
    "width": 4,
    "bulge": 1,
    "slope": -1,
    "intercept": 2,
    "lift": 2,
    "presentation": "formula",
    "limits": "intersections"
   },
   "stem": {
    "text": "Find the area enclosed by \\(f(x)=-x^2+x+5\\) and \\(g(x)=2-x\\).",
    "command_verb": "find"
   },
   "key": {
    "form": "numeric",
    "expr": "32/3"
   },
   "steps": [
    {
     "text": "\\(f=g\\).",
     "expr": "-x**2 + x + 5 = 2 - x",
     "relation": "new"
    },
    {
     "text": "Limits.",
     "expr": "FiniteSet(-1, 3)",
     "relation": "solve",
     "variable": "x"
    },
    {
     "text": "The integral.",
     "expr": "Integral(-x**2 + 2*x + 3, (x, -1, 3))",
     "relation": "new",
     "point_type_id": "BC-PT-99001"
    },
    {
     "text": "Evaluated.",
     "expr": "32/3",
     "relation": "equivalent"
    }
   ],
   "calculator_status": "no_calculator",
   "skills": [
    "BC-SKL-08020"
   ]
  },
  {
   "id": "chk-3",
   "check_kind": "mcq",
   "format": "mcq",
   "bands": [
    "low"
   ],
   "archetype_id": "BC-QA-08008",
   "parameter_draw": {
    "left": 0,
    "width": 2,
    "bulge": 2,
    "slope": 1,
    "intercept": -2,
    "lift": 1,
    "presentation": "formula",
    "limits": "intersections"
   },
   "stem": {
    "text": "What is the area enclosed by \\(f(x)=-2x^2+5x-2\\) and \\(g(x)=x-2\\)?",
    "command_verb": "find"
   },
   "key": {
    "form": "numeric",
    "expr": "8/3"
   },
   "steps": [
    {
     "text": "\\(f=g\\).",
     "expr": "-2*x**2 + 5*x - 2 = x - 2",
     "relation": "new"
    },
    {
     "text": "Limits 0 and 2.",
     "expr": "FiniteSet(0, 2)",
     "relation": "solve",
     "variable": "x"
    },
    {
     "text": "The integral.",
     "expr": "Integral(-2*x**2 + 4*x, (x, 0, 2))",
     "relation": "new"
    },
    {
     "text": "Evaluated.",
     "expr": "8/3",
     "relation": "equivalent"
    }
   ],
   "options": [
    {
     "id": "A",
     "is_key": false,
     "expr": "-40/3",
     "error_path": "BC-ERR-08019",
     "derivation": "the y coordinates -2 and 0 of the meeting points used as limits"
    },
    {
     "id": "B",
     "is_key": false,
     "expr": "2.7",
     "error_path": "BC-ERR-99019",
     "derivation": "8/3 rounded to one decimal place"
    },
    {
     "id": "C",
     "is_key": true,
     "expr": "8/3",
     "error_path": null
    },
    {
     "id": "D",
     "is_key": false,
     "expr": "2.66",
     "error_path": "BC-ERR-99019",
     "derivation": "8/3 truncated to two decimal places"
    }
   ],
   "calculator_status": "no_calculator",
   "skills": [
    "BC-SKL-08020"
   ]
  }
 ],
 "delivery": [
  {
   "block": "orientation",
   "mode": "figure",
   "reason": "rule 4: BC-REP-02 on BC-SKL-08021; unit README delivery map",
   "sources": [
    "BC-SKL-08021"
   ],
   "spec": {
    "kind": "graph",
    "representations": [
     "BC-REP-02"
    ],
    "window": {
     "x": [
      0,
      4
     ],
     "y": [
      -1,
      6
     ]
    },
    "curves": [
     {
      "expr": "-x**2 + 6*x - 4",
      "domain": [
       0,
       4
      ]
     },
     {
      "expr": "2*x - 1",
      "domain": [
       0,
       4
      ]
     }
    ],
    "shade": {
     "between": [
      "-x**2 + 6*x - 4",
      "2*x - 1"
     ],
     "x": [
      1,
      3
     ]
    },
    "labels": [
     {
      "text": "region enclosed by f and g",
      "placement": "inside"
     }
    ]
   },
   "fallback": "the same shaded region static with its label",
   "keyboard": "no control; the figure description is reached with Tab"
  },
  {
   "block": "ki-1",
   "mode": "figure",
   "reason": "rule 4: BC-REP-02 on BC-SKL-08021; not promoted, BC-QA-08008 difficulty_variables are presence flags",
   "sources": [
    "BC-SKL-08021",
    "BC-QA-08008"
   ],
   "spec": {
    "kind": "graph",
    "representations": [
     "BC-REP-02",
     "BC-REP-01"
    ],
    "window": {
     "x": [
      0,
      4
     ],
     "y": [
      -1,
      6
     ]
    },
    "curves": [
     {
      "expr": "-x**2 + 6*x - 4",
      "domain": [
       0,
       4
      ]
     },
     {
      "expr": "2*x - 1",
      "domain": [
       0,
       4
      ]
     }
    ],
    "points": [
     {
      "at": [
       1,
       1
      ],
      "style": "filled"
     },
     {
      "at": [
       3,
       5
      ],
      "style": "filled"
     }
    ],
    "guides": [
     {
      "vertical": 1
     },
     {
      "vertical": 3
     }
    ],
    "labels": [
     {
      "text": "(1, 1): lower limit x = 1",
      "placement": "inside"
     },
     {
      "text": "(3, 5): upper limit x = 3",
      "placement": "inside"
     },
     {
      "text": "limits are x values, not y values",
      "placement": "inside"
     }
    ]
   },
   "fallback": "the static region with both meeting points, their vertical guides and labels",
   "keyboard": "no control; the figure description is reached with Tab"
  },
  {
   "block": "ex-1",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  },
  {
   "block": "err-BC-ERR-08019",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  },
  {
   "block": "err-BC-ERR-99019",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  }
 ],
 "refresher": [
  "ki-1",
  "err-BC-ERR-08019",
  "err-BC-ERR-99019",
  "ex-1"
 ],
 "read_minutes": {
  "full": 3.1,
  "brief": 3.0
 },
 "word_count": {
  "full": 456,
  "brief": 447
 },
 "research_lines": [
  {
   "file": "research/units/unit-08-applications-integration.md",
   "line": "The limits are the inputs where the region begins and ends"
  }
 ],
 "inferred": [
  {
   "claim": "The first written line is the equation f = g, read from the second entry of BC-QA-08008's expected_solution_path, which needs the limits.",
   "settles": "An archetype record whose expected_solution_path names the intersection solve."
  },
  {
   "claim": "BC-QA-08008 is an either archetype; the lesson takes Section I Part A and its 2.14 minute budget.",
   "settles": "A ruling on which exam part an either archetype's budget comes from."
  },
  {
   "claim": "BC-PT-99003 and BC-PT-99004 are earned on ex-1 steps 4 and 5 but not tagged, because their reader lines push the brief band past 450 words.",
   "settles": "A brief word cap that exempts reader lines, or a shorter reader_checks form."
  },
  {
   "claim": "The orientation and ki-1 are static figures, and the interior test at x = 2 is held in the head.",
   "settles": "The modality A/B in the build plan, and timing data per step from 10's fluency telemetry."
  }
 ],
 "sources": [
  "BC-CON-08011",
  "BC-SKL-08020",
  "BC-SKL-08021",
  "BC-EK-CHA-5A1",
  "ced:155",
  "BC-QA-08008",
  "BC-PT-99001",
  "sg-23:16",
  "BC-ERR-08019",
  "BC-ERR-99019",
  "BC-MIS-08012",
  "BC-MIS-09008",
  "BC-PRQ-08001",
  "BC-PRQ-08006",
  "research/units/unit-08-applications-integration.md#8.4 Finding the Area Between Curves Expressed as Functions of x",
  "research/question-analysis/question-archetypes.md#BC-QA-08008 Area of a region between two curves in x",
  "research/scoring/common-point-losses.md#Answer points",
  "research/exam/exam-structure.md#Section and part layout"
 ]
}
```
