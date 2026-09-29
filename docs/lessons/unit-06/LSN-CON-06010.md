---
title: LSN-CON-06010 Definite integral evaluated by geometry
research_date: 2026-09-29
status: designed
purpose: Authoring spec for the concept lesson on BC-CON-06010, a definite integral evaluated as a sum of signed areas from a graph of segments and semicircles, built from authoring_bundle("BC-CON-06010") and the research files it cites.
---

# LSN-CON-06010 Definite integral evaluated by geometry

Concept BC-CON-06010 (skill BC-SKL-06028), topic 6.6 of Unit 6, loaded by one archetype, BC-QA-06004 (family definite-integral-from-graph). Its hard parent concept is BC-CON-06001 (docs/lessons/unit-06/README.md, section 1).

## Prediction

One multiple choice question on worked example 1's own second piece, asked before the rule is shown: on [2, 4] f lies below the axis and encloses area 2, and the question is how that piece enters the integral from 1 to 8. The key is "It subtracts 2", the -2 of ex-1's third step. The distractors are the piece added as area (the BC-ERR-06014 path) and the piece adding nothing. The resolution, shown on the key idea screen beside the choice, states that a piece below the axis contributes the negative of its area. No verdict word. Sources: BC-CON-06010 and the topic 6.6 section the key idea cites.

## Orientation

Served text, from BC-CON-06010 `description_plain` and the topic's Assessment behaviour paragraph (research/units/unit-06-integration-accumulation.md#6.6 Applying Properties of Definite Integrals): a response writes the integral as a sum of signed areas and attaches the value to its label. No count, no frequency.

## Key ideas

BC-SKL-06028 maps to BC-EK-FUN-6A1 alone, so one core block, both bands.

- ki-1 (core), BC-EK-FUN-6A1, ced:123. Paraphrase of the Geometry paragraph of Required mathematical knowledge: partition where the graph changes character, one area formula per piece, pieces below the axis negative. Anchor quote, 9 words, found on ced:123. Notation line "signed area" from the concept record. The Properties and Discontinuities paragraphs map to BC-EK-FUN-6A2 and 6A3, which no skill of this concept lists; they belong to LSN-CON-06011.

## Recognition

BC-QA-06004 (research/question-analysis/question-archetypes.md#BC-QA-06004 Definite integral evaluated from a graph by geometry). `typical_wording`: "the graph of f consists of line segments and semicircles; evaluate the definite integral of f over the stated interval". `common_givens`: a graph of f made of line segments and semicircles, an accumulation function with a fixed lower limit, the area of a region bounded by the graph. `asked_to_produce`: the value of a definite integral over a stated interval, labelled values of an accumulation function. Official examples: BC-FRQ-2024-Q4-A, BC-FRQ-2025-Q4-C, BC-FRQ-2018-Q3-B, and the MCQ BC-MCQ-PE2012-003.

Contrast pair on st-1: this stem is on BC-QA-06004, a graph of segments and a semicircle with an integral value asked; not this stem is an integral of x^2 + 1 with numerical limits, the near miss from BC-CON-06012, where f is a formula and an antiderivative gives the value. The separating feature is a drawn graph with no formula for f.

The signal: a drawn graph of pieces with elementary shapes, no formula for f, and a request for a number. What says "not this concept": a formula for f (antiderivative, BC-CON-06012), a table (Riemann sum, BC-CON-06003), or a request for g prime or an extremum of g (BC-CON-06008, BC-CON-06009).

## Method choice

One strategy block, both bands.

- st-1, BC-QA-06004. Cue from `common_givens` and `asked_to_produce`. Method, `expected_solution_path[0]`: partition the region at the points where the graph changes character. Rival from `wrong_approaches`: adding regions below the axis as positive area (BC-ERR-06014). Separating feature: the integral is signed, so the side of the axis fixes each piece's sign. The reader prints its own labels, so no strategy field begins with one. The second `wrong_approaches` entry (reversed limits, BC-ERR-99012) is not an error this concept's skill holds, so it is not the named rival.

## Solution path

- ex-1, BC-QA-06004, both bands, no calculator. Draw from `parameter_spec`: heights 1, 3, 0, -2, lower 1, circle above, direction forward, so segments join (0, 1), (1, 3), (2, 0), (3, -2), (4, 0) and a radius 2 semicircle sits above [4, 8]; derived `linear_area` = -1/2. No published BC-QA-06004 item carries this draw.
- Steps follow `expected_solution_path`: partition (no value); triangle above, 3/2 (new); triangle below, -2 (new); semicircle, 2π (new); signed sum (new, BC-PT-99069); 2π - 1/2 (equivalent).

A fluent solver writes the signed sum and the labelled value; the partition and each formula are held in the head (unit README section 5) [inferred]. The value point needs no supporting work (sg-25:18). There is no example 2, so nothing is faded. The step's why line no longer cites sg-25:18, since served text carries no citation; it stays in Scoring and Sources.

## Scoring

BC-QA-06004 lists BC-PT-99069; ex-1 tags it on the signed sum. The reader line is `reader_checks(["BC-PT-99069"])` copied exactly. From the archetype `scoring_pattern`: the value alone earns the point, but a value attached to the wrong label is scratch work (sg-25:18); reversed limits need the sign change (sg-24:12).

## Traps

Both active errors meeting BC-SKL-06028, in the bundle's order: BC-ERR-06014 (linked BC-MIS-08024, severity high), then BC-ERR-06013 (BC-MIS-08019, medium). Both bands show both. Both relations are distinct, so both are fix prompts (`fix_prompt` true). On ex-1's draw:

- err-BC-ERR-06014: 3/2 + 2 + 2π against 3/2 - 2 + 2π. Possible reason, words from BC-MIS-08024.
- err-BC-ERR-06013: the semicircle as 4π against 2π. Possible reason, words from BC-MIS-08019.

## Representations

None as a separate block. The topic's conversion, graph to a numerical integral value (BC-REP-02 to BC-REP-01), is carried by the orientation and ki-1 figures.

## Prerequisite bridge

- BC-PRQ-06007, from its `description_plain` (area formulas read off a figure) and `failure_signature` (trapezoid as rectangle, semicircle as full circle).

## Time

BC-QA-06004 is `no_calculator`; as one part of a no-calculator free response question it sits in Section II Part B, 15.0 minutes per question (research/exam/exam-structure.md#Section and part layout). Its one point is a 1.67 minute share by the unit README's points rule [inferred]; as an MCQ it takes the Part A 2.14. The minutes go on reading the vertices and the signs; the arithmetic is short.

## Checks

- chk-1, completion of ex-1, both bands: the three signed pieces are given; key 2π - 1/2.
- chk-2, isomorph, both bands. Draw: heights -2, 0, 2, 2, lower 0, circle below, forward. Key 3 - 2π.
- chk-3, MCQ, low band. Draw: heights 3, 1, 0, -1, lower 0, circle below, forward. Key 3/2 - 2π. Distractors: 7/2 + 2π and 3/2 + 2π (BC-ERR-06014, all pieces positive, and the semicircle positive), 3/2 - 4π (BC-ERR-06013).

## Delivery

- prediction: text [inferred; settled by the modality A/B].
- orientation: figure. Rule 4: BC-REP-02 on BC-SKL-06028; not promoted to interactive, since BC-QA-06004's `difficulty_variables` are presence flags (unit README section 6) [inferred; settled by the modality A/B].
- ki-1: figure, the pieces with their formulas inside. Rule 4.
- ex-1, err-BC-ERR-06014, err-BC-ERR-06013: step_reveal. Rule 1.

The drawn blocks (orientation and ki-1 figures) are already present, so no figure is added and no `no_figure_reason` is stated.

## Band plan

- Low (full), in served order: prediction, orientation, ki-1, st-1 with its contrast pair, ex-1 with its reader line, chk-1, both error blocks, chk-2, chk-3, the bridge. 474 words, 3.2 minutes (cap 900 and 6). There is no example 2, so nothing is faded, and no representations block.
- Mid (brief): the same blocks less chk-3. 449 words, 3.0 minutes (cap 450 and 3). The orientation, ki-1 (its text and its anchor quote, shortened to a shorter stretch of the same sentence on ced:123), the st-1 fields, the contrast, the prediction and the bridge were shortened to fit; the scoring tag stays.
- Refresher: ki-1, err-BC-ERR-06014, err-BC-ERR-06013, ex-1.

## Sources

- BC-CON-06010; BC-SKL-06028; BC-EK-FUN-6A1; ced:123
- BC-QA-06004; BC-PT-99069; sg-25:18, sg-24:12
- BC-ERR-06014, BC-ERR-06013; BC-MIS-08024, BC-MIS-08019
- BC-PRQ-06007
- research/units/unit-06-integration-accumulation.md#6.6 Applying Properties of Definite Integrals
- research/question-analysis/question-archetypes.md#BC-QA-06004 Definite integral evaluated from a graph by geometry
- research/exam/exam-structure.md#Section and part layout
- [inferred] The 1.67 minute share of the Section II question. Settled by timing data per step.
- [inferred] The contrast near miss, an integral of a formula, is a stem written for this pair. Settled by a published near-miss item.
- [inferred] Static figures for the orientation and ki-1. Settled by the modality A/B.
- [inferred] Which steps a fluent solver holds in the head. Settled by timing data per step.

## Machine record

```json
{
 "id": "LSN-CON-06010",
 "kind": "concept",
 "target_id": "BC-CON-06010",
 "unit": "06",
 "skills": [
  "BC-SKL-06028"
 ],
 "prediction": {
  "id": "pr-1",
  "stem": {
   "text": "On [2, 4], f is below the axis, area 2. How does it enter \\(\\int_1^8 f(x)\\,dx\\)?",
   "command_verb": "predict"
  },
  "format": "mcq",
  "options": [
   {
    "id": "A",
    "label": "It adds 2",
    "is_key": false
   },
   {
    "id": "B",
    "label": "It subtracts 2",
    "is_key": true
   },
   {
    "id": "C",
    "label": "It adds nothing",
    "is_key": false
   }
  ],
  "resolution": "A piece below the axis contributes the negative of its area: \\(-2\\).",
  "sources": [
   "BC-CON-06010",
   "research/units/unit-06-integration-accumulation.md#6.6 Applying Properties of Definite Integrals"
  ]
 },
 "orientation": {
  "text": "A response writes the integral as signed areas and labels it.",
  "sources": [
   "BC-CON-06010",
   "research/units/unit-06-integration-accumulation.md#6.6 Applying Properties of Definite Integrals"
  ]
 },
 "key_ideas": [
  {
   "id": "ki-1",
   "ek_id": "BC-EK-FUN-6A1",
   "depth": "core",
   "text": "Split where the graph changes character. Each piece has an area formula, negative below the axis. The integral is the signed sum.",
   "notation": "signed area",
   "quote": {
    "text": "a definite integral can be evaluated by using geometry",
    "source": "ced:123"
   },
   "sources": [
    "BC-EK-FUN-6A1",
    "ced:123",
    "research/units/unit-06-integration-accumulation.md#6.6 Applying Properties of Definite Integrals"
   ]
  }
 ],
 "strategy": [
  {
   "id": "st-1",
   "archetype_id": "BC-QA-06004",
   "cue": "A graph of segments and semicircles; an integral value asked.",
   "method": "Partition where the graph changes character.",
   "rival": "Every piece added as positive area.",
   "separating_feature": "The side of the axis fixes each sign.",
   "sources": [
    "BC-QA-06004"
   ],
   "evidence_tag": "verified",
   "contrast": {
    "this": {
     "text": "Graphed f is segments and a semicircle. Evaluate the integral from 0 to 6.",
     "archetype_id": "BC-QA-06004"
    },
    "not_this": {
     "text": "Evaluate the integral of x^2 + 1 from 0 to 6.",
     "why_not": "f is a formula: use an antiderivative."
    },
    "feature": "A drawn graph, with no formula for f."
   }
  }
 ],
 "worked_examples": [
  {
   "id": "ex-1",
   "archetype_id": "BC-QA-06004",
   "bands": [
    "low",
    "mid"
   ],
   "parameter_draw": {
    "heights": [
     1,
     3,
     0,
     -2
    ],
    "lower": 1,
    "circle": "above",
    "direction": "forward"
   },
   "problem": {
    "text": "f: segments through (0, 1), (1, 3), (2, 0), (3, -2), (4, 0), then a radius 2 semicircle above [4, 8]. Find ∫_1^8 f(x) dx.",
    "command_verb": "find"
   },
   "calculator_status": "no_calculator",
   "steps": [
    {
     "cue": "Segments and an arc: split at x = 2 and x = 4.",
     "why": "One shape per piece, one side of the axis."
    },
    {
     "cue": "[1, 2]: triangle above.",
     "why": "Added.",
     "expr": "(1/2)*1*3",
     "relation": "new"
    },
    {
     "cue": "[2, 4]: triangle below.",
     "why": "Enters negatively.",
     "expr": "-(1/2)*2*2",
     "relation": "new"
    },
    {
     "cue": "[4, 8]: semicircle above.",
     "why": "Half of pi r squared.",
     "expr": "(1/2)*pi*2**2",
     "relation": "new"
    },
    {
     "cue": "The integral is the signed total.",
     "why": "Adjacent intervals add.",
     "expr": "3/2 - 2 + 2*pi",
     "relation": "new",
     "point_type_id": "BC-PT-99069"
    },
    {
     "cue": "Label the value.",
     "why": "A mislabelled value is scratch work.",
     "expr": "2*pi - 1/2",
     "relation": "equivalent"
    }
   ],
   "answer": {
    "form": "symbolic",
    "expr": "2*pi - 1/2"
   }
  }
 ],
 "what_a_reader_scores": [
  {
   "example_id": "ex-1",
   "point_type_ids": [
    "BC-PT-99069"
   ],
   "lines": [
    {
     "point_type_id": "BC-PT-99069",
     "text": "Value of an accumulation function found from geometry of a graph. Earned by: The value of the accumulation function at the requested input, computed from areas of the regions under the graph, with the correct sign for reversed limits (sg-25:18, sg-24:12). Not earned by: A value from the wrong starting limit; sg-24:13 has a special case where an explicitly wrong lower limit forfeits the first point it would otherwise have earned."
    }
   ]
  }
 ],
 "common_errors": [
  {
   "error_id": "BC-ERR-06014",
   "observed_behavior": "Every piece of the region is added with a positive sign, so a signed integral is reported as a plain area.",
   "scoring_consequence": "The value point is lost, and any later part that imports the value inherits the error.",
   "wrong_step": {
    "text": "[2, 4] added.",
    "expr": "3/2 + 2 + 2*pi"
   },
   "right_step": {
    "text": "[2, 4] subtracted.",
    "expr": "3/2 - 2 + 2*pi"
   },
   "relation": "distinct",
   "possible_reason": {
    "misconception_id": "BC-MIS-08024",
    "text": "reads every definite integral as area under a graph"
   },
   "sources": [
    "BC-ERR-06014",
    "BC-MIS-08024"
   ],
   "fix_prompt": true
  },
  {
   "error_id": "BC-ERR-06013",
   "observed_behavior": "The area of a semicircular piece of the region is computed as pi times the radius squared.",
   "scoring_consequence": "The value point for that integral is lost.",
   "wrong_step": {
    "text": "Semicircle as 4π.",
    "expr": "3/2 - 2 + 4*pi"
   },
   "right_step": {
    "text": "Semicircle as 2π.",
    "expr": "3/2 - 2 + 2*pi"
   },
   "relation": "distinct",
   "possible_reason": {
    "misconception_id": "BC-MIS-08019",
    "text": "remembers the squared dimension but not the fraction in front of it"
   },
   "sources": [
    "BC-ERR-06013",
    "BC-MIS-08019"
   ],
   "fix_prompt": true
  }
 ],
 "representations": null,
 "prerequisite_bridges": [
  {
   "prq_id": "BC-PRQ-06007",
   "text": "A semicircle is half a circle."
  }
 ],
 "time": {
  "exam_part": "II-B",
  "budget_minutes": 15.0,
  "source": "research/exam/exam-structure.md#Section and part layout",
  "written_steps": {
   "ex-1": [
    5,
    6
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
   "archetype_id": "BC-QA-06004",
   "parameter_draw": {
    "heights": [
     1,
     3,
     0,
     -2
    ],
    "lower": 1,
    "circle": "above",
    "direction": "forward"
   },
   "completes": "ex-1",
   "stem": {
    "text": "The signed pieces of ∫_1^8 f(x) dx are 3/2, -2 and 2π. Find the integral.",
    "command_verb": "find"
   },
   "key": {
    "form": "symbolic",
    "expr": "2*pi - 1/2"
   },
   "steps": [
    {
     "text": "Add the signed pieces.",
     "expr": "3/2 - 2 + 2*pi",
     "relation": "new"
    },
    {
     "text": "Simplify.",
     "expr": "2*pi - 1/2",
     "relation": "equivalent"
    }
   ],
   "calculator_status": "no_calculator",
   "skills": [
    "BC-SKL-06028"
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
   "archetype_id": "BC-QA-06004",
   "parameter_draw": {
    "heights": [
     -2,
     0,
     2,
     2
    ],
    "lower": 0,
    "circle": "below",
    "direction": "forward"
   },
   "stem": {
    "text": "f: segments through (0, -2), (1, 0), (2, 2), (3, 2), (4, 0), then a radius 2 semicircle below [4, 8]. Find ∫_0^8 f(x) dx.",
    "command_verb": "find"
   },
   "key": {
    "form": "symbolic",
    "expr": "3 - 2*pi"
   },
   "steps": [
    {
     "text": "Triangle below on [0, 1].",
     "expr": "-(1/2)*1*2",
     "relation": "new"
    },
    {
     "text": "Trapezoid above on [1, 4], parallel sides 3 and 1, height 2.",
     "expr": "(3 + 1)/2*2",
     "relation": "new"
    },
    {
     "text": "Semicircle below on [4, 8].",
     "expr": "-(1/2)*pi*2**2",
     "relation": "new"
    },
    {
     "text": "Sum.",
     "expr": "-1 + 4 - 2*pi",
     "relation": "new"
    },
    {
     "text": "Simplify.",
     "expr": "3 - 2*pi",
     "relation": "equivalent"
    }
   ],
   "calculator_status": "no_calculator",
   "skills": [
    "BC-SKL-06028"
   ]
  },
  {
   "id": "chk-3",
   "check_kind": "mcq",
   "format": "mcq",
   "bands": [
    "low"
   ],
   "archetype_id": "BC-QA-06004",
   "parameter_draw": {
    "heights": [
     3,
     1,
     0,
     -1
    ],
    "lower": 0,
    "circle": "below",
    "direction": "forward"
   },
   "stem": {
    "text": "f: segments through (0, 3), (1, 1), (2, 0), (3, -1), (4, 0), then a radius 2 semicircle below [4, 8]. Find ∫_0^8 f(x) dx.",
    "command_verb": "identify"
   },
   "key": {
    "form": "symbolic",
    "expr": "3/2 - 2*pi"
   },
   "steps": [
    {
     "text": "Above on [0, 2].",
     "expr": "(3 + 1)/2*1 + (1/2)*1*1",
     "relation": "new"
    },
    {
     "text": "Below on [2, 4].",
     "expr": "-(1/2)*2*1",
     "relation": "new"
    },
    {
     "text": "Semicircle below.",
     "expr": "-(1/2)*pi*2**2",
     "relation": "new"
    },
    {
     "text": "Sum.",
     "expr": "5/2 - 1 - 2*pi",
     "relation": "new"
    },
    {
     "text": "Simplify.",
     "expr": "3/2 - 2*pi",
     "relation": "equivalent"
    }
   ],
   "options": [
    {
     "id": "A",
     "is_key": false,
     "expr": "7/2 + 2*pi",
     "error_path": "BC-ERR-06014",
     "derivation": "every piece added as positive area"
    },
    {
     "id": "B",
     "is_key": false,
     "expr": "3/2 + 2*pi",
     "error_path": "BC-ERR-06014",
     "derivation": "the semicircle below the axis added as positive area"
    },
    {
     "id": "C",
     "is_key": true,
     "expr": "3/2 - 2*pi",
     "error_path": null
    },
    {
     "id": "D",
     "is_key": false,
     "expr": "3/2 - 4*pi",
     "error_path": "BC-ERR-06013",
     "derivation": "the semicircle given the full circle's area 4π"
    }
   ],
   "calculator_status": "no_calculator",
   "skills": [
    "BC-SKL-06028"
   ]
  }
 ],
 "delivery": [
  {
   "block": "orientation",
   "mode": "figure",
   "reason": "rule 4: BC-REP-02 on BC-SKL-06028; not promoted, since BC-QA-06004's difficulty_variables are presence flags, not a varying quantity (unit README delivery map)",
   "sources": [
    "BC-SKL-06028",
    "BC-QA-06004"
   ],
   "spec": {
    "kind": "graph",
    "representations": [
     "BC-REP-02"
    ],
    "window": {
     "x": [
      0,
      8
     ],
     "y": [
      -3,
      4
     ]
    },
    "curves": [
     {
      "type": "polyline",
      "points": [
       [
        0,
        1
       ],
       [
        1,
        3
       ],
       [
        2,
        0
       ],
       [
        3,
        -2
       ],
       [
        4,
        0
       ]
      ]
     },
     {
      "type": "semicircle",
      "center": [
       6,
       0
      ],
      "radius": 2,
      "side": "above"
     }
    ],
    "shading": [
     {
      "between": "graph and x axis",
      "interval": [
       1,
       8
      ],
      "above": "plus",
      "below": "minus"
     }
    ],
    "labels": [
     {
      "text": "+",
      "placement": "inside",
      "at": "region on [1, 2]"
     },
     {
      "text": "-",
      "placement": "inside",
      "at": "region on [2, 4]"
     },
     {
      "text": "+",
      "placement": "inside",
      "at": "semicircle"
     }
    ]
   },
   "fallback": "the same graph as a static image with the three signed regions marked",
   "keyboard": "none needed: the figure has no control"
  },
  {
   "block": "ki-1",
   "mode": "figure",
   "reason": "rule 4: BC-REP-02 on BC-SKL-06028; the pieces and their formulas are read off one static graph",
   "sources": [
    "BC-SKL-06028"
   ],
   "spec": {
    "kind": "graph",
    "representations": [
     "BC-REP-02"
    ],
    "window": {
     "x": [
      0,
      8
     ],
     "y": [
      -3,
      4
     ]
    },
    "curves": [
     {
      "type": "polyline",
      "points": [
       [
        0,
        1
       ],
       [
        1,
        3
       ],
       [
        2,
        0
       ],
       [
        3,
        -2
       ],
       [
        4,
        0
       ]
      ]
     },
     {
      "type": "semicircle",
      "center": [
       6,
       0
      ],
      "radius": 2,
      "side": "above"
     }
    ],
    "partition": [
     1,
     2,
     4,
     8
    ],
    "labels": [
     {
      "text": "(1/2)(1)(3)",
      "placement": "inside",
      "at": "triangle on [1, 2]"
     },
     {
      "text": "-(1/2)(2)(2)",
      "placement": "inside",
      "at": "triangle on [2, 4]"
     },
     {
      "text": "(1/2)π(2)^2",
      "placement": "inside",
      "at": "semicircle"
     }
    ]
   },
   "fallback": "the same graph, static, with the three area formulas written in their regions",
   "keyboard": "none needed: the figure has no control"
  },
  {
   "block": "ex-1",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  },
  {
   "block": "err-BC-ERR-06014",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  },
  {
   "block": "err-BC-ERR-06013",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  }
 ],
 "refresher": [
  "ki-1",
  "err-BC-ERR-06014",
  "err-BC-ERR-06013",
  "ex-1"
 ],
 "research_lines": [
  {
   "file": "research/units/unit-06-integration-accumulation.md",
   "line": "In some cases a definite integral can be evaluated using geometry and the connection between the definite integral and area (BC-EK-FUN-6A1). Regions below the axis contribute negatively."
  }
 ],
 "inferred": [
  {
   "claim": "The geometry part takes about 1.67 of the 15.0 Section II minutes, one point of nine.",
   "settles": "Timing data per step once the fluency telemetry exists (unit README section 5)."
  },
  {
   "claim": "The orientation and ki-1 are served as static figures rather than text.",
   "settles": "The modality A/B in the build plan: skip rate and time to first credited success by mode."
  },
  {
   "claim": "A fluent solver holds the partition and each area formula in the head and writes the signed sum and the labelled value.",
   "settles": "Timing data per step once the fluency telemetry exists."
  }
 ],
 "sources": [
  "BC-CON-06010",
  "BC-SKL-06028",
  "BC-EK-FUN-6A1",
  "ced:123",
  "BC-QA-06004",
  "BC-PT-99069",
  "sg-25:18",
  "sg-24:12",
  "BC-ERR-06014",
  "BC-ERR-06013",
  "BC-MIS-08024",
  "BC-MIS-08019",
  "BC-PRQ-06007",
  "research/units/unit-06-integration-accumulation.md#6.6 Applying Properties of Definite Integrals",
  "research/question-analysis/question-archetypes.md#BC-QA-06004 Definite integral evaluated from a graph by geometry",
  "research/exam/exam-structure.md#Section and part layout"
 ],
 "read_minutes": {
  "full": 3.2,
  "brief": 3.0
 },
 "word_count": {
  "full": 473,
  "brief": 448
 }
}
```
