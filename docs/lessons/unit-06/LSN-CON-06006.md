---
title: LSN-CON-06006 Definite integral as the limit of Riemann sums
research_date: 2026-09-29
status: designed
purpose: Authoring spec for the concept lesson on BC-CON-06006, the definite integral as the limit of Riemann sums and the conversion between the two forms, built from authoring_bundle("BC-CON-06006") and the research files it cites.
---

# LSN-CON-06006 Definite integral as the limit of Riemann sums

Concept BC-CON-06006 (skills BC-SKL-06014, BC-SKL-06015, BC-SKL-06016), topic 6.3 of Unit 6, loaded by one archetype, BC-QA-06014 (family riemann-limit-to-integral). Its hard parents are BC-CON-06003 and BC-CON-06005 (docs/lessons/unit-06/README.md, section 1).

## Prediction

One multiple choice question on worked example 1's own term, \(3(1+2i/n)^2(2/n)\), asked before the rule is shown: over what interval the sample points run. The key is "From 1 to 3", the interval ex-1's integral is taken over. The distractors are the interval read off the width alone (the BC-ERR-99032 path) and an interval with the right start and a wrong length. The resolution, shown on the key idea screen beside the choice, states that the width gives the length and the first sample point gives the start. No verdict word. Sources: BC-CON-06006 and the topic 6.3 section the key ideas cite.

## Orientation

Served text, from BC-CON-06006 `description_plain` and the topic's Assessment behaviour paragraph (research/units/unit-06-integration-accumulation.md#6.3 Riemann Sums, Summation Notation, and Definite Integral Notation): MCQ forms give a limit of a sum in sigma notation and ask for the matching integral, or the reverse. No count, no frequency.

## Key ideas

Three BC-EK across three skills; two core, one extended.

- ki-1 (core), BC-EK-LIM-5C1 (BC-SKL-06016), ced:120. Paraphrase of the Definition of the definite integral paragraph of Required mathematical knowledge, hypothesis (f continuous) and conclusion. Anchor quote, 14 words, found on ced:120.
- ki-2 (core), BC-EK-LIM-5C2 (BC-SKL-06014, 06015), ced:120. The conversion read from the term, from the topic's Representations paragraph (limit of a sum to integral and back). No quote: the LIM-5.C.2 sentence is 27 words.
- ki-3 (extended), BC-EK-LIM-5B1 (BC-SKL-06014), ced:120. Anchor quote, 14 words.

Each carries the concept notation line.

## Recognition

BC-QA-06014 (research/question-analysis/question-archetypes.md#BC-QA-06014 Converting between a limit of Riemann sums and a definite integral). `typical_wording`: "express the given limit of a Riemann sum as a definite integral", "write the given definite integral as the limit of a Riemann sum". `common_givens`: a definite integral with stated limits, a limit of a Riemann sum in sigma notation. `asked_to_produce`: an equivalent definite integral, an equivalent limit of Riemann sums. Official examples are MCQ only: BC-MCQ-CED-006, BC-MCQ-SAMPLE-008.

The signal: "lim as n approaches infinity" in front of Σ, or "as the limit of a Riemann sum". Not this concept: Σ with no limit and a stated n (BC-CON-06005), or a request to approximate (BC-CON-06003).

Contrast pair on st-1: this stem is on BC-QA-06014, a limit of a sum written as an integral; not this stem is a right sum with n = 4 for an integral already given, the near miss from BC-CON-06003, which calls for a finite sum and no limit. The separating feature is the limit in front of the sum.

## Method choice

- st-1, BC-QA-06014, both bands. Cue from `asked_to_produce` and `common_givens`. Method, `expected_solution_path[0]`: separate the general term into a value and a width. Rival: BC-QA-06014 records no `wrong_approaches` or `prohibited_shortcuts`, so the rival is taken from BC-ERR-99032 (limits that were never given); the block carries `evidence_tag: inferred`. Separating feature: the sample point fixes the lower limit, the width fixes the length. The reader prints its own labels, so no field of the block begins with one.

## Solution path

- ex-1, BC-QA-06014, both bands, no calculator. Draw from `parameter_spec`: direction to_integral, function square, coefficient 3, start 1, width 2, convention right, letter x (derived finish 3). No published BC-QA-06014 item carries this draw.
- Steps follow `expected_solution_path`: the given limit (new); split into value and width (no value); width, so length (no value); sample point, so lower limit (no value); the integral (equivalent; the CAS confirms both equal 26).

A fluent solver writes the integral only and holds the split, the width and the start [inferred]. There is no example 2, so nothing is faded.

## Scoring

BC-QA-06014 lists no `point_types`, so no what_a_reader_scores entry and no point tag; the lesson says nothing about points beyond the error records' scoring_consequence (plan 15, R14).

## Traps

Two active errors meet the skills, in the bundle's order: BC-ERR-99028 (linked BC-MIS-06001, severity high), BC-ERR-99032 (BC-MIS-99011 and BC-MIS-08012, medium). Both bands. Both relations are distinct, so both are fix prompts (`fix_prompt` true). On ex-1's draw:

- err-BC-ERR-99028: the width factor lost, ∫_0^1 3(1 + 2x)^2 dx, against ∫_1^3 3x^2 dx. Possible reason, words from BC-MIS-06001.
- err-BC-ERR-99032: limits never given, 0 to 2, against 1 to 3. No possible reason line: neither linked description names limits read from a width.

## Representations

One block, low band, from the topic's Representations paragraph (limit of a sum to integral): right sums of ex-1's integrand at n = 2, 4, 8, 16, 100, computed and shown as a table, settling on 26. Served as a model under the unit README's delivery map.

## Prerequisite bridge

- BC-PRQ-06006, from its `description_plain` (index, limits, general term) and `failure_signature` (index substituted wrongly, off by one).

## Time

BC-QA-06014 is `no_calculator`, MCQ only in the record, so Section I Part A, 2.14 minutes per question (research/exam/exam-structure.md#Section and part layout). The minutes go on reading the start and length off the term.

## Checks

- chk-1, completion of ex-1, both bands: width, height and range given; key ∫_1^3 3x^2 dx.
- chk-2, isomorph, both bands. Draw: to_integral, cube, coefficient 2, start 2, width 2, left, t. Key ∫_2^4 2t^3 dt.
- chk-3, MCQ, low band. Draw: to_integral, square, coefficient 1, start 2, width 3, right, x. Key ∫_2^5 x^2 dx (value 39). Distractors: ∫_0^3 x^2 dx (BC-ERR-99032, value 9), ∫_5^2 x^2 dx (BC-ERR-99032, value -39), ∫_0^1 (2 + 3x)^2 dx (BC-ERR-99028, value 13).

## Delivery

- prediction: text [inferred; settled by the modality A/B].
- orientation, ki-2, ki-3: text. Rule 6, BC-REP-01.
- ki-1: motion, rectangles refining under 3x^2 as n grows. Rule 2 (unit README section 6). Rule 3 would allow one stepper on n instead; motion is kept to match the unit map [inferred].
- ex-1 and both error blocks: step_reveal. Rule 1.
- representations: model, right sums at growing n.

Drawn blocks already present (ki-1 motion, the representations model), so no figure is added and no `no_figure_reason` is stated. Every non-text choice is [inferred]; settled by the modality A/B.

## Band plan

- Low (full), in served order: prediction, orientation, the bridge, ki-1 to ki-3, st-1 with its contrast pair, ex-1, chk-1, both error blocks, chk-2, the model, chk-3. 515 words, 3.5 minutes (cap 900 and 6). There is no example 2, so nothing is faded, and BC-QA-06014 lists no `point_types`, so no scoring lines.
- Mid (brief): prediction, orientation, the bridge, ki-1, ki-2, st-1 with its contrast pair, ex-1, chk-1, both error blocks, chk-2. 450 words, 3.0 minutes (cap 450 and 3). The orientation, both core key ideas, the strategy fields, the contrast and the bridge were shortened to fit; the ki-1 anchor quote and every check stem stay.
- Refresher: ki-1, ki-2, both error blocks, ex-1.

## Sources

- BC-CON-06006; BC-SKL-06014, BC-SKL-06015, BC-SKL-06016; BC-EK-LIM-5C1, 5C2, 5B1; ced:120
- BC-QA-06014
- BC-ERR-99028, BC-ERR-99032; BC-MIS-06001
- BC-PRQ-06006
- research/units/unit-06-integration-accumulation.md#6.3 Riemann Sums, Summation Notation, and Definite Integral Notation (the prediction and the contrast pair)
- research/question-analysis/question-archetypes.md#BC-QA-06014 Converting between a limit of Riemann sums and a definite integral
- research/exam/exam-structure.md#Section and part layout
- [inferred] The rival from BC-ERR-99032. Settled by wrong_approaches on BC-QA-06014.
- [inferred] I-A for an archetype with no FRQ part. Settled by a conversion rubric.
- [inferred] The function label read as a formula. Settled by a formula template.
- [inferred] Motion and model rather than a stepper. Settled by the modality A/B.
- [inferred] The contrast near miss, a right sum with n = 4, is a sibling-concept stem written for this pair. Settled by a published near-miss item.
- [inferred] Which steps a fluent solver holds. Settled by timing data per step.

## Machine record

```json
{
 "id": "LSN-CON-06006",
 "kind": "concept",
 "target_id": "BC-CON-06006",
 "unit": "06",
 "skills": [
  "BC-SKL-06014",
  "BC-SKL-06015",
  "BC-SKL-06016"
 ],
 "prediction": {
  "id": "pr-1",
  "stem": {
   "text": "Predict. In \\(\\lim_{n\\to\\infty}\\sum_{i=1}^n 3(1+2i/n)^2(2/n)\\), the sample points run over what interval?",
   "command_verb": "predict"
  },
  "format": "mcq",
  "options": [
   {
    "id": "A",
    "label": "From 0 to 2",
    "is_key": false
   },
   {
    "id": "B",
    "label": "From 1 to 3",
    "is_key": true
   },
   {
    "id": "C",
    "label": "From 1 to 2",
    "is_key": false
   }
  ],
  "resolution": "The width \\(2/n\\) gives length 2, and the first sample point is 1. The interval is \\([1,3]\\), so the limit is \\(\\int_1^3 3x^2\\,dx\\).",
  "sources": [
   "BC-CON-06006",
   "research/units/unit-06-integration-accumulation.md#6.3 Riemann Sums, Summation Notation, and Definite Integral Notation"
  ]
 },
 "orientation": {
  "text": "Letting widths go to zero turns a Riemann sum into an integral. A response converts between them.",
  "sources": [
   "BC-CON-06006",
   "research/units/unit-06-integration-accumulation.md#6.3 Riemann Sums, Summation Notation, and Definite Integral Notation"
  ]
 },
 "key_ideas": [
  {
   "id": "ki-1",
   "ek_id": "BC-EK-LIM-5C1",
   "depth": "core",
   "text": "For continuous f, the integral is the limit of Riemann sums as widths go to 0.",
   "notation": "\\(\\int_a^b f(x)\\,dx\\)",
   "quote": {
    "text": "is the limit of Riemann sums as the widths of the subintervals approach 0",
    "source": "ced:120"
   },
   "sources": [
    "BC-EK-LIM-5C1",
    "ced:120",
    "research/units/unit-06-integration-accumulation.md#6.3 Riemann Sums, Summation Notation, and Definite Integral Notation"
   ]
  },
  {
   "id": "ki-2",
   "ek_id": "BC-EK-LIM-5C2",
   "depth": "core",
   "text": "Split the term. The width fixes b - a, the first sample point fixes a, the height gives f.",
   "notation": "\\(\\int_a^b f(x)\\,dx\\)",
   "quote": null,
   "sources": [
    "BC-EK-LIM-5C2",
    "ced:120",
    "research/units/unit-06-integration-accumulation.md#6.3 Riemann Sums, Summation Notation, and Definite Integral Notation"
   ]
  },
  {
   "id": "ki-3",
   "ek_id": "BC-EK-LIM-5B1",
   "depth": "extended",
   "text": "An approximating sum and its limit are different objects: the sum estimates, the limit is the integral.",
   "notation": "\\(\\int_a^b f(x)\\,dx\\)",
   "quote": {
    "text": "The limit of an approximating Riemann sum can be interpreted as a definite integral.",
    "source": "ced:120"
   },
   "sources": [
    "BC-EK-LIM-5B1",
    "ced:120",
    "research/units/unit-06-integration-accumulation.md#6.3 Riemann Sums, Summation Notation, and Definite Integral Notation"
   ]
  }
 ],
 "strategy": [
  {
   "id": "st-1",
   "archetype_id": "BC-QA-06014",
   "cue": "A limit of a sum, or an integral; the other form asked.",
   "method": "Split the term into value and width.",
   "rival": "Limits read off the width alone.",
   "separating_feature": "The sample point, not the width, gives the lower limit.",
   "sources": [
    "BC-QA-06014"
   ],
   "evidence_tag": "inferred",
   "contrast": {
    "this": {
     "text": "Write lim_(n→∞) Σ_(i=1)^n (1 + 4i/n)^3 (4/n) as an integral.",
     "archetype_id": "BC-QA-06014"
    },
    "not_this": {
     "text": "Approximate the integral of x^2 from 1 to 5 with a right sum, n = 4.",
     "why_not": "It asks for a finite sum, not a limit."
    },
    "feature": "The limit as n approaches infinity precedes the sum."
   }
  }
 ],
 "worked_examples": [
  {
   "id": "ex-1",
   "archetype_id": "BC-QA-06014",
   "bands": [
    "low",
    "mid"
   ],
   "parameter_draw": {
    "direction": "to_integral",
    "function": "square",
    "coefficient": 3,
    "start": 1,
    "width": 2,
    "convention": "right",
    "letter": "x"
   },
   "problem": {
    "text": "Write lim_(n→∞) Σ_(i=1)^n 3(1 + 2i/n)^2 (2/n) as a definite integral.",
    "command_verb": "write"
   },
   "calculator_status": "no_calculator",
   "steps": [
    {
     "cue": "lim of Σ: a definite integral.",
     "why": "Widths go to 0.",
     "expr": "Limit(Sum(3*(1 + 2*i/n)**2*(2/n), (i, 1, n)), n, oo)",
     "relation": "new"
    },
    {
     "cue": "Split the term: 2/n times 3(1 + 2i/n)^2.",
     "why": "Width times height."
    },
    {
     "cue": "Width 2/n.",
     "why": "b - a = 2."
    },
    {
     "cue": "Sample point 1 + 2i/n starts at 1.",
     "why": "a = 1, so b = 3; height 3x^2."
    },
    {
     "cue": "Write the integral.",
     "why": "Same value as the limit.",
     "expr": "Integral(3*x**2, (x, 1, 3))",
     "relation": "equivalent"
    }
   ],
   "answer": {
    "form": "symbolic",
    "expr": "Integral(3*x**2, (x, 1, 3))"
   }
  }
 ],
 "what_a_reader_scores": [],
 "common_errors": [
  {
   "error_id": "BC-ERR-99028",
   "observed_behavior": "Responses assume a common subinterval width where the table gives unequal ones, present the sum of the values without the widths, use the wrong sum type, or apply an incorrect trapezoid area formula.",
   "scoring_consequence": "The setup point requires the sum of the appropriate products to be visible; the answer point follows it.",
   "wrong_step": {
    "text": "Width factor lost.",
    "expr": "Integral(3*(1 + 2*x)**2, (x, 0, 1))"
   },
   "right_step": {
    "text": "Width 2/n kept.",
    "expr": "Integral(3*x**2, (x, 1, 3))"
   },
   "relation": "distinct",
   "possible_reason": {
    "misconception_id": "BC-MIS-06001",
    "text": "the partition widths play no role"
   },
   "sources": [
    "BC-ERR-99028",
    "BC-MIS-06001"
   ],
   "fix_prompt": true
  },
  {
   "error_id": "BC-ERR-99032",
   "observed_behavior": "Responses asked for an integral expression write statements that are not integral expressions, such as the function set equal to its own integral, a summation sign placed in front of an integral, or a constant of integration attached to a definite integral, and some reverse the limits or use limits that were never given.",
   "scoring_consequence": "The expression point is not earned, since the requested object is an integral expression and nothing else is being scored in that part.",
   "wrong_step": {
    "text": "Limits 0 to 2.",
    "expr": "Integral(3*x**2, (x, 0, 2))"
   },
   "right_step": {
    "text": "Limits 1 to 3.",
    "expr": "Integral(3*x**2, (x, 1, 3))"
   },
   "relation": "distinct",
   "possible_reason": null,
   "sources": [
    "BC-ERR-99032"
   ],
   "fix_prompt": true
  }
 ],
 "representations": {
  "text": "Right sums for ex-1 at n = 2, 4, 8, 16, 100: 39, 32.25, 29.06, 27.52, 26.24. They settle on 26, the integral.",
  "figure": {
   "kind": "numeric_experiment",
   "function": "3*x**2",
   "interval": [
    1,
    3
   ],
   "sum": "right",
   "n_values": [
    2,
    4,
    8,
    16,
    100
   ],
   "columns": [
    "n",
    "right sum"
   ],
   "labels": [
    {
     "text": "sums approach 26",
     "placement": "inside",
     "at": "row below the last value"
    }
   ]
  },
  "sources": [
   "research/units/unit-06-integration-accumulation.md#6.3 Riemann Sums, Summation Notation, and Definite Integral Notation",
   "BC-QA-06014"
  ]
 },
 "prerequisite_bridges": [
  {
   "prq_id": "BC-PRQ-06006",
   "text": "Sigma notation: one term per index value. A wrong substitution moves the sample point."
  }
 ],
 "time": {
  "exam_part": "I-A",
  "budget_minutes": 2.14,
  "source": "research/exam/exam-structure.md#Section and part layout",
  "written_steps": {
   "ex-1": [
    5
   ]
  },
  "skipped_steps": {
   "ex-1": [
    1,
    2,
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
   "archetype_id": "BC-QA-06014",
   "parameter_draw": {
    "direction": "to_integral",
    "function": "square",
    "coefficient": 3,
    "start": 1,
    "width": 2,
    "convention": "right",
    "letter": "x"
   },
   "completes": "ex-1",
   "stem": {
    "text": "Width 2/n, height 3(1 + 2i/n)^2, sample points running from 1 to 3. Write the integral.",
    "command_verb": "write"
   },
   "key": {
    "form": "symbolic",
    "expr": "Integral(3*x**2, (x, 1, 3))"
   },
   "steps": [
    {
     "text": "Height 3x^2 on [1, 3].",
     "expr": "Integral(3*x**2, (x, 1, 3))",
     "relation": "new"
    }
   ],
   "calculator_status": "no_calculator",
   "skills": [
    "BC-SKL-06014"
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
   "archetype_id": "BC-QA-06014",
   "parameter_draw": {
    "direction": "to_integral",
    "function": "cube",
    "coefficient": 2,
    "start": 2,
    "width": 2,
    "convention": "left",
    "letter": "t"
   },
   "stem": {
    "text": "Write lim_(n→∞) Σ_(i=1)^n 2(2 + 2(i - 1)/n)^3 (2/n) as a definite integral.",
    "command_verb": "write"
   },
   "key": {
    "form": "symbolic",
    "expr": "Integral(2*t**3, (t, 2, 4))"
   },
   "steps": [
    {
     "text": "The limit.",
     "expr": "Limit(Sum(2*(2 + 2*(i - 1)/n)**3*(2/n), (i, 1, n)), n, oo)",
     "relation": "new"
    },
    {
     "text": "Width 2/n, start 2, height 2t^3.",
     "expr": "Integral(2*t**3, (t, 2, 4))",
     "relation": "equivalent"
    }
   ],
   "calculator_status": "no_calculator",
   "skills": [
    "BC-SKL-06014"
   ]
  },
  {
   "id": "chk-3",
   "check_kind": "mcq",
   "format": "mcq",
   "bands": [
    "low"
   ],
   "archetype_id": "BC-QA-06014",
   "parameter_draw": {
    "direction": "to_integral",
    "function": "square",
    "coefficient": 1,
    "start": 2,
    "width": 3,
    "convention": "right",
    "letter": "x"
   },
   "stem": {
    "text": "Which integral equals lim_(n→∞) Σ_(i=1)^n (2 + 3i/n)^2 (3/n)?",
    "command_verb": "identify"
   },
   "key": {
    "form": "symbolic",
    "expr": "Integral(x**2, (x, 2, 5))"
   },
   "steps": [
    {
     "text": "The limit.",
     "expr": "Limit(Sum((2 + 3*i/n)**2*(3/n), (i, 1, n)), n, oo)",
     "relation": "new"
    },
    {
     "text": "Width 3/n, start 2, height x^2.",
     "expr": "Integral(x**2, (x, 2, 5))",
     "relation": "equivalent"
    }
   ],
   "options": [
    {
     "id": "A",
     "is_key": false,
     "expr": "Integral(x**2, (x, 0, 3))",
     "error_path": "BC-ERR-99032",
     "derivation": "limits never given, read off the width as 0 to 3"
    },
    {
     "id": "B",
     "is_key": true,
     "expr": "Integral(x**2, (x, 2, 5))",
     "error_path": null
    },
    {
     "id": "C",
     "is_key": false,
     "expr": "Integral((2 + 3*x)**2, (x, 0, 1))",
     "error_path": "BC-ERR-99028",
     "derivation": "the width factor 3 dropped when i/n becomes x"
    },
    {
     "id": "D",
     "is_key": false,
     "expr": "Integral(x**2, (x, 5, 2))",
     "error_path": "BC-ERR-99032",
     "derivation": "the limits reversed"
    }
   ],
   "calculator_status": "no_calculator",
   "skills": [
    "BC-SKL-06014"
   ]
  }
 ],
 "delivery": [
  {
   "block": "orientation",
   "mode": "text",
   "reason": "rule 6: BC-REP-01 on every skill (unit README delivery map)",
   "sources": [
    "BC-SKL-06014",
    "BC-SKL-06015",
    "BC-SKL-06016"
   ]
  },
  {
   "block": "ki-1",
   "mode": "motion",
   "reason": "rule 2: the EK text 'the limit of Riemann sums as the widths of the subintervals approach 0' (ced:120) is a process, rectangles refining under a curve (unit README delivery map)",
   "sources": [
    "BC-EK-LIM-5C1",
    "BC-SKL-06016"
   ],
   "spec": {
    "kind": "graph_sweep",
    "representations": [
     "BC-REP-02"
    ],
    "axes": {
     "x": [
      0.5,
      3.5
     ],
     "y": [
      0,
      30
     ]
    },
    "curves": [
     {
      "expr": "3*x**2",
      "domain": [
       1,
       3
      ]
     }
    ],
    "parameter": {
     "name": "n",
     "frames": [
      2,
      4,
      8,
      16
     ]
    },
    "rectangles": {
     "sum": "right",
     "interval": [
      1,
      3
     ]
    },
    "labels": [
     {
      "text": "n = frame value",
      "placement": "inside",
      "at": "top left corner"
     },
     {
      "text": "right sum",
      "placement": "inside",
      "at": "top right corner"
     },
     {
      "text": "integral 26",
      "placement": "inside",
      "at": "under the curve on the last frame"
     }
    ]
   },
   "fallback": "the four frames as static small panels in one row, n increasing left to right, each with its sum printed inside",
   "keyboard": "left and right arrow keys step between frames; Home returns to n = 2; each frame announces n and the sum",
   "reduced_motion": "no auto-advance: each arrow key press cross-fades to the next frame"
  },
  {
   "block": "ki-2",
   "mode": "text",
   "reason": "rule 6: a symbolic conversion, BC-REP-01 only",
   "sources": [
    "BC-SKL-06014",
    "BC-SKL-06015"
   ]
  },
  {
   "block": "ki-3",
   "mode": "text",
   "reason": "rule 6: a statement about two objects, BC-REP-01 only",
   "sources": [
    "BC-SKL-06014"
   ]
  },
  {
   "block": "ex-1",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  },
  {
   "block": "err-BC-ERR-99028",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  },
  {
   "block": "err-BC-ERR-99032",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  },
  {
   "block": "representations",
   "mode": "model",
   "reason": "template model row and rule 2: the idea is the behaviour of a computed sequence, Riemann sums at growing n (unit README delivery map)",
   "sources": [
    "BC-QA-06014",
    "BC-EK-LIM-5C1"
   ],
   "spec": {
    "kind": "numeric_experiment",
    "representations": [
     "BC-REP-03"
    ],
    "function": "3*x**2",
    "interval": [
     1,
     3
    ],
    "sum": "right",
    "n_values": [
     2,
     4,
     8,
     16,
     100
    ],
    "columns": [
     "n",
     "right sum"
    ],
    "labels": [
     {
      "text": "n",
      "placement": "inside",
      "at": "first column header"
     },
     {
      "text": "sums approach 26",
      "placement": "inside",
      "at": "row below the last value"
     }
    ]
   },
   "fallback": "the five computed rows printed as a static table with the closing label",
   "keyboard": "a Run control reached by Tab and pressed with Enter or Space adds one row per press; the table is read in row order"
  }
 ],
 "refresher": [
  "ki-1",
  "ki-2",
  "err-BC-ERR-99028",
  "err-BC-ERR-99032",
  "ex-1"
 ],
 "research_lines": [
  {
   "file": "research/units/unit-06-integration-accumulation.md",
   "line": "Conversions tested: symbolic limit of a sum to symbolic definite integral and back (BC-REP-01 to BC-REP-01), which is itself the assessed ability (BC-EK-LIM-5C2)."
  }
 ],
 "inferred": [
  {
   "claim": "The rival, limits read off the width, is taken from BC-ERR-99032; BC-QA-06014 has no wrong_approaches or prohibited_shortcuts.",
   "settles": "wrong_approaches on BC-QA-06014."
  },
  {
   "claim": "BC-QA-06014 has no FRQ part recorded, so the time part is I-A.",
   "settles": "A free response rubric with a conversion part."
  },
  {
   "claim": "The function label is read as a formula: square with coefficient 3 as 3x^2, cube with coefficient 2 as 2t^3.",
   "settles": "An explicit formula template in BC-QA-06014's parameter_spec."
  },
  {
   "claim": "ki-1 as motion and the representations block as a model rather than one interactive stepper on n.",
   "settles": "The modality A/B in the build plan: skip rate and time to first credited success by mode."
  },
  {
   "claim": "A fluent solver writes only the integral and holds the split, the width and the start.",
   "settles": "Timing data per step once the fluency telemetry exists."
  }
 ],
 "sources": [
  "BC-CON-06006",
  "BC-SKL-06014",
  "BC-SKL-06015",
  "BC-SKL-06016",
  "BC-EK-LIM-5B1",
  "BC-EK-LIM-5C1",
  "BC-EK-LIM-5C2",
  "ced:120",
  "BC-QA-06014",
  "BC-ERR-99028",
  "BC-ERR-99032",
  "BC-MIS-06001",
  "BC-PRQ-06006",
  "research/units/unit-06-integration-accumulation.md#6.3 Riemann Sums, Summation Notation, and Definite Integral Notation",
  "research/question-analysis/question-archetypes.md#BC-QA-06014 Converting between a limit of Riemann sums and a definite integral",
  "research/exam/exam-structure.md#Section and part layout"
 ],
 "read_minutes": {
  "full": 3.5,
  "brief": 3.0
 },
 "word_count": {
  "full": 515,
  "brief": 450
 }
}
```
