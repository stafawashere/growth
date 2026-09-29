---
title: LSN-CON-04008 The relating equation
research_date: 2026-09-29
status: designed
purpose: Authoring spec for the concept lesson on BC-CON-04008, the equation that ties the varying quantities of a related rates problem together before any differentiation, built from authoring_bundle("BC-CON-04008") and the research files it cites.
---

# LSN-CON-04008 The relating equation

Concept BC-CON-04008 (skills BC-SKL-04018, BC-SKL-04020, BC-SKL-04021), topic 4.4, loaded by BC-QA-04006 (primary) and BC-QA-04007, both in family related-rates. Its hard parent is BC-CON-04007 (docs/lessons/unit-04/README.md, section 1).

## Orientation

Served text, from BC-CON-04008 `description_plain` and the topic's Assessment behaviour paragraph (research/units/unit-04-contextual-applications-differentiation.md#4.4 Introduction to Related Rates): a response writes one equation among the quantities of the figure, from a formula, the Pythagorean theorem or a similar triangles proportion, and cuts it to the variables the supplied rates support before differentiating.

## Key ideas

BC-SKL-04018 and BC-SKL-04021 map to BC-EK-CHA-3D1; BC-SKL-04020 maps to BC-EK-CHA-3D2 (ced:90).

- ki-1 (core), BC-EK-CHA-3D1. Paraphrase of "The relating equation" and "Variables as functions of time": a formula, the Pythagorean theorem or a similar triangles proportion ties the quantities together, and an extra varying dimension is eliminated first. Anchor quote from ced:90 (14 words).
- ki-2 (extended, low band), BC-EK-CHA-3D2. Paraphrase of "Other rules": a term multiplying two varying quantities needs the product rule. Anchor quote from ced:90.

## Recognition

BC-QA-04006 (research/question-analysis/question-archetypes.md#BC-QA-04006 Related rates in a geometric setting): `typical_wording` "find the rate at which the stated quantity is changing at the instant described"; `common_givens` supplied rates, a formula, the dimensions at the instant, a figure; `asked_to_produce` the rate and its units. The signal: a named solid, ladder or tank with one rate given and another asked. Shapes: a standalone MCQ or one part of a multipart FRQ (BC-FRQ-2019-Q4-A, BC-FRQ-2022-Q4-D, BC-MCQ-CED-005).

BC-QA-04007 (research/question-analysis/question-archetypes.md#BC-QA-04007 Related rates on an implicitly defined curve): a curve equation in x and y, a point and one coordinate rate; the relating equation is supplied, so the work starts at the differentiation, with the product rule on a mixed term.

Not this concept: a stem that supplies the quantity as a function of time; no relating equation is built.

## Method choice

- st-1, BC-QA-04006. Method, `expected_solution_path[1]` after naming the quantities: write the relating equation, then eliminate what the rates cannot support. Rival from `wrong_approaches`: a varying dimension treated as constant (BC-ERR-99013). Separating feature: whether the stem gives a rate for every varying dimension.
- st-2, BC-QA-04007. Method, `expected_solution_path[0]`: differentiate the curve equation with respect to time. Rival: the mixed term differentiated as though one variable were constant (BC-ERR-04018). Separating feature: a term such as xy.

## Solution path

- ex-1, BC-QA-04006, both bands, no calculator. Draw: shape cone, size 4, rate 6, ratio 1, leg short, foot, minute; so the tank's height is 2 times its top radius, water enters at 6 cubic feet per minute, depth 4 feet. No published BC-QA-04006 item carries this draw.
- Steps: the cone formula (new); the proportion r = h/2 (no value); the radius eliminated (evaluate); the differentiation with respect to t (new); the instant substituted (evaluate); the rate (solve). A fluent solver writes all of them; the proportion is one line beside the figure.

## Scoring

BC-QA-04006 lists BC-PT-99023, BC-PT-99006, BC-PT-99004 and BC-PT-99022. ex-1 tags BC-PT-99023 on the differentiation step; the served line is `reader_checks(["BC-PT-99023"])`. For the author: the 2022 report records that few responses expressed the changing quantity as a function of the varying dimension or saw that the chain rule was needed (cr-22:7). A units point is scored separately from the value (research/scoring/common-point-losses.md#Units points).

## Traps

Five active errors meet the skills; the first four in the bundle's order are served: BC-ERR-04016, BC-ERR-04018, BC-ERR-04019, BC-ERR-99013. BC-ERR-99033 (variable never defined) is left out by the cap of four. All on ex-1's draw; the mid band shows the first two.

- err-BC-ERR-04016: the cylinder formula against the cone formula. Reason words from BC-MIS-04010.
- err-BC-ERR-04018: the radius held constant in V = (1/3) pi r^2 h, against the product rule. Reason words from BC-MIS-04009.
- err-BC-ERR-04019: r kept, so two unknown rates, against the eliminated form. Reason words from BC-MIS-04010.
- err-BC-ERR-99013: dV/dh in place of dV/dt. Reason words from BC-MIS-04008.

## Representations

None as a separate block. The topic's Representations paragraph names a verbal scenario to a labelled diagram and a diagram to a relating equation (BC-REP-05 to BC-REP-08 to BC-REP-01); the orientation figure and ki-1's interactive carry it.

## Prerequisite bridge

- BC-PRQ-04001, BC-PRQ-04002, BC-PRQ-04003, BC-PRQ-04008: one short paragraph each from `description_plain` and `failure_signature`.

## Time

BC-QA-04006 has `calculator_status` either, so Section I Part A, 2.14 minutes (research/exam/exam-structure.md#Section and part layout) [inferred: an either archetype is taken as I-A]. Written: the formula, the eliminated form, the differentiated equation, the substituted equation, the rate. Held in the head: the proportion arithmetic. Most of the minutes go on the elimination.

## Checks

- chk-1, completion of ex-1, both bands: the differentiated equation is given; key 3/(2 pi).
- chk-2, isomorph, both bands: ladder, size 5, rate 3, ratio 2, leg long, foot, second; ladder 10 feet, foot 8 feet from the wall. Key -4.
- chk-3, MCQ, low band: cone, size 3, rate 9, ratio 2, leg long, centimeter, second. Key 9/pi. Distractors: 3/pi (BC-ERR-04016, cylinder), 27/pi (BC-ERR-04018, radius frozen at 1), pi (BC-ERR-99013, dV/dh).

## Delivery

- orientation: figure. Rule 3: BC-REP-08 on BC-SKL-04018 and BC-SKL-04021 (docs/lessons/unit-04/README.md, section 6) [inferred].
- ki-1: interactive. Rule 3 promoted: BC-QA-04006 `difficulty_variables` "whether a second variable must be eliminated by similar triangles"; one slider on the water depth, the reading is which labels move [inferred].
- ki-2: text. Rule 5: BC-SKL-04020 carries BC-REP-01 only.
- ex-1 and the four error blocks: step_reveal. Rule 1.

## Band plan

- Low (full): orientation, ki-1, ki-2, st-1, st-2, ex-1 with its scoring line, four error blocks, chk-1 to chk-3, four bridges. 656 words, 4.4 minutes (cap 900 and 6).
- Mid (brief): orientation, ki-1, st-1, ex-1 with its scoring line, err-BC-ERR-04016, err-BC-ERR-04018, chk-1, chk-2, four bridges. 428 words, 2.9 minutes (cap 450 and 3).
- Refresher: ki-1, err-BC-ERR-04016, err-BC-ERR-04018, err-BC-ERR-04019, err-BC-ERR-99013, ex-1.

## Sources

- BC-CON-04008; BC-SKL-04018, BC-SKL-04020, BC-SKL-04021; BC-EK-CHA-3D1, BC-EK-CHA-3D2; ced:90
- BC-QA-04006, BC-QA-04007; BC-PT-99023; cr-22:7
- BC-ERR-04016, BC-ERR-04018, BC-ERR-04019, BC-ERR-99013; BC-MIS-04008, BC-MIS-04009, BC-MIS-04010
- BC-PRQ-04001, BC-PRQ-04002, BC-PRQ-04003, BC-PRQ-04008
- research/units/unit-04-contextual-applications-differentiation.md#4.4 Introduction to Related Rates
- research/question-analysis/question-archetypes.md#BC-QA-04006 Related rates in a geometric setting
- research/question-analysis/question-archetypes.md#BC-QA-04007 Related rates on an implicitly defined curve
- research/scoring/common-point-losses.md#Units points
- research/exam/exam-structure.md#Section and part layout
- [inferred] I-A for an either archetype. Settled by a plan 15 budget rule for calculator_status either.
- [inferred] The figure and interactive modes. Settled by the modality A/B.

## Machine record

```json
{
 "id": "LSN-CON-04008",
 "kind": "concept",
 "target_id": "BC-CON-04008",
 "unit": "04",
 "skills": [
  "BC-SKL-04018",
  "BC-SKL-04020",
  "BC-SKL-04021"
 ],
 "orientation": {
  "text": "Before differentiating, write one equation tying the figure's quantities together, from a formula, the Pythagorean theorem or similar triangles, cut to the variables the given rates support.",
  "sources": [
   "BC-CON-04008",
   "research/units/unit-04-contextual-applications-differentiation.md#4.4 Introduction to Related Rates"
  ]
 },
 "key_ideas": [
  {
   "id": "ki-1",
   "ek_id": "BC-EK-CHA-3D1",
   "depth": "core",
   "text": "Each changing quantity is a function of time, tied to the others by one equation. When only one dimension has a given rate, a second varying dimension is written in terms of it before differentiating.",
   "notation": "dV/dt, dr/dt, dh/dt",
   "quote": {
    "text": "The chain rule is the basis for differentiating variables in a related rates problem",
    "source": "ced:90"
   },
   "sources": [
    "BC-EK-CHA-3D1",
    "ced:90",
    "research/units/unit-04-contextual-applications-differentiation.md#4.4 Introduction to Related Rates"
   ]
  },
  {
   "id": "ki-2",
   "ek_id": "BC-EK-CHA-3D2",
   "depth": "extended",
   "text": "A term multiplying two varying quantities, such as r squared times h, differentiates by the product rule, giving one rate factor for each.",
   "notation": "product rule",
   "quote": {
    "text": "such as the product rule and the quotient rule, may also be necessary",
    "source": "ced:90"
   },
   "sources": [
    "BC-EK-CHA-3D2",
    "ced:90",
    "research/units/unit-04-contextual-applications-differentiation.md#4.4 Introduction to Related Rates"
   ]
  }
 ],
 "strategy": [
  {
   "id": "st-1",
   "archetype_id": "BC-QA-04006",
   "cue": "A figure, one supplied rate, another rate asked at an instant.",
   "method": "First line: the formula for the figure, then eliminate every dimension with no supplied rate.",
   "rival": "Rival: a varying dimension held constant (BC-ERR-99013).",
   "separating_feature": "Count the varying dimensions against the supplied rates.",
   "sources": [
    "BC-QA-04006"
   ],
   "evidence_tag": "verified"
  },
  {
   "id": "st-2",
   "archetype_id": "BC-QA-04007",
   "cue": "A curve in x and y, a point and one coordinate rate.",
   "method": "First line: the curve equation differentiated with respect to t.",
   "rival": "Rival: xy differentiated with one factor constant (BC-ERR-04018).",
   "separating_feature": "A product of two varying quantities.",
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
    "shape": "cone",
    "size": 4,
    "rate": 6,
    "ratio": 1,
    "leg": "short",
    "length_unit": "foot",
    "time_unit": "minute"
   },
   "problem": {
    "text": "Water enters a vertex-down cone, height 2 times top radius, at 6 cubic feet per minute. Find dh/dt at depth 4 feet.",
    "command_verb": "find"
   },
   "calculator_status": "no_calculator",
   "steps": [
    {
     "cue": "A cone of water.",
     "why": "Its volume formula ties V, r and h.",
     "expr": "V = pi*r**2*h/3",
     "relation": "new"
    },
    {
     "cue": "Only dV/dt is given.",
     "why": "Similar triangles: r = h/2."
    },
    {
     "cue": "r has no rate.",
     "why": "Eliminate it.",
     "expr": "V = pi*h**3/12",
     "relation": "evaluate",
     "subs": {
      "r": "h/2"
     }
    },
    {
     "cue": "One variable left.",
     "why": "Differentiate with respect to t.",
     "expr": "dVdt = pi*h**2*dhdt/4",
     "relation": "new",
     "point_type_id": "BC-PT-99023"
    },
    {
     "cue": "Now the instant.",
     "why": "h = 4, dV/dt = 6.",
     "expr": "6 = 4*pi*dhdt",
     "relation": "evaluate",
     "subs": {
      "h": "4",
      "dVdt": "6"
     }
    },
    {
     "cue": "One unknown rate.",
     "why": "Feet per minute.",
     "expr": "3/(2*pi)",
     "relation": "solve",
     "variable": "dhdt"
    }
   ],
   "answer": {
    "form": "symbolic",
    "expr": "3/(2*pi)"
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
   "error_id": "BC-ERR-04016",
   "observed_behavior": "No equation ties the quantities together, or the formula used does not describe the configuration.",
   "scoring_consequence": "Nothing downstream can be earned; BC-ERR-99011 records integrands chosen from the wrong area or volume family as the analogous failure in Unit 8.",
   "wrong_step": {
    "text": "Cylinder.",
    "expr": "V = pi*r**2*h"
   },
   "right_step": {
    "text": "Cone.",
    "expr": "V = pi*r**2*h/3"
   },
   "relation": "distinct",
   "possible_reason": {
    "misconception_id": "BC-MIS-04010",
    "text": "the equation is skipped or is chosen by resemblance"
   },
   "sources": [
    "BC-ERR-04016",
    "BC-MIS-04010"
   ]
  },
  {
   "error_id": "BC-ERR-04018",
   "observed_behavior": "A term that multiplies two varying quantities is differentiated as though one of them were constant.",
   "scoring_consequence": "The completely correct differentiation point is lost; BC-ERR-99013 names the missing product rule explicitly.",
   "wrong_step": {
    "text": "r held constant.",
    "expr": "dVdt = pi*r**2*dhdt/3"
   },
   "right_step": {
    "text": "Product rule.",
    "expr": "dVdt = pi*(2*r*h*drdt + r**2*dhdt)/3"
   },
   "relation": "distinct",
   "possible_reason": {
    "misconception_id": "BC-MIS-04009",
    "text": "only one rate factor appears where two are needed"
   },
   "sources": [
    "BC-ERR-04018",
    "BC-MIS-04009"
   ]
  },
  {
   "error_id": "BC-ERR-04019",
   "observed_behavior": "The relating equation keeps two varying dimensions that the supplied rates cannot support, and the differentiation produces an equation with two unknown rates.",
   "scoring_consequence": "The requested rate cannot be isolated, so the answer point is lost.",
   "wrong_step": {
    "text": "r kept: two unknown rates.",
    "expr": "6 = pi*(16*drdt + 4*dhdt)/3"
   },
   "right_step": {
    "text": "r eliminated.",
    "expr": "6 = 4*pi*dhdt"
   },
   "relation": "distinct",
   "possible_reason": {
    "misconception_id": "BC-MIS-04010",
    "text": "expects the supplied rates to determine the answer without a geometric relation"
   },
   "sources": [
    "BC-ERR-04019",
    "BC-MIS-04010"
   ]
  },
  {
   "error_id": "BC-ERR-99013",
   "observed_behavior": "Responses differentiate an implicit relation with respect to x when time is the independent variable, omit the product rule on a product of two changing quantities, or treat one quantity as constant, and confuse the notations for the several derivatives in play.",
   "scoring_consequence": "The differentiation points in the part are not earned, and the numerical answer point depends on them.",
   "wrong_step": {
    "text": "With respect to h.",
    "expr": "dVdh = pi*h**2/4"
   },
   "right_step": {
    "text": "With respect to t.",
    "expr": "dVdt = pi*h**2*dhdt/4"
   },
   "relation": "distinct",
   "possible_reason": {
    "misconception_id": "BC-MIS-04008",
    "text": "so the rates with respect to time never appear"
   },
   "sources": [
    "BC-ERR-99013",
    "BC-MIS-04008"
   ]
  }
 ],
 "representations": null,
 "prerequisite_bridges": [
  {
   "prq_id": "BC-PRQ-04001",
   "text": "Standard volume and area formulas; without them no relating equation starts."
  },
  {
   "prq_id": "BC-PRQ-04002",
   "text": "The Pythagorean theorem; without it a ladder distance has no equation."
  },
  {
   "prq_id": "BC-PRQ-04003",
   "text": "Similar triangles remove one variable; without them two stay."
  },
  {
   "prq_id": "BC-PRQ-04008",
   "text": "Name each quantity, its unit, and whether it varies."
  }
 ],
 "time": {
  "exam_part": "I-A",
  "budget_minutes": 2.14,
  "source": "research/exam/exam-structure.md#Section and part layout",
  "written_steps": {
   "ex-1": [
    1,
    3,
    4,
    5,
    6
   ]
  },
  "skipped_steps": {
   "ex-1": [
    2
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
   "archetype_id": "BC-QA-04006",
   "parameter_draw": {
    "shape": "cone",
    "size": 4,
    "rate": 6,
    "ratio": 1,
    "leg": "short",
    "length_unit": "foot",
    "time_unit": "minute"
   },
   "completes": "ex-1",
   "stem": {
    "text": "For the tank of ex-1, dV/dt = (pi h^2/4) dh/dt. With dV/dt = 6 and h = 4, find dh/dt.",
    "command_verb": "find"
   },
   "key": {
    "form": "symbolic",
    "expr": "3/(2*pi)"
   },
   "steps": [
    {
     "text": "Differentiated equation.",
     "expr": "dVdt = pi*h**2*dhdt/4",
     "relation": "new"
    },
    {
     "text": "The instant.",
     "expr": "6 = 4*pi*dhdt",
     "relation": "evaluate",
     "subs": {
      "h": "4",
      "dVdt": "6"
     }
    },
    {
     "text": "Solve.",
     "expr": "3/(2*pi)",
     "relation": "solve",
     "variable": "dhdt"
    }
   ],
   "calculator_status": "no_calculator",
   "skills": [
    "BC-SKL-04021"
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
    "size": 8,
    "rate": 3,
    "ratio": 2,
    "leg": "long",
    "length_unit": "foot",
    "time_unit": "second"
   },
   "stem": {
    "text": "A 10 foot ladder's foot slides from a wall at 3 feet per second. Find the rate of change of the top's height when the foot is 8 feet out.",
    "command_verb": "find"
   },
   "key": {
    "form": "symbolic",
    "expr": "-4"
   },
   "steps": [
    {
     "text": "Pythagorean theorem.",
     "expr": "x**2 + y**2 = 100",
     "relation": "new"
    },
    {
     "text": "x = 8.",
     "expr": "64 + y**2 = 100",
     "relation": "evaluate",
     "subs": {
      "x": "8"
     }
    },
    {
     "text": "y = 6.",
     "expr": "6",
     "relation": "solve",
     "variable": "y"
    },
    {
     "text": "Differentiate in t.",
     "expr": "2*x*dxdt + 2*y*dydt = 0",
     "relation": "new"
    },
    {
     "text": "Substitute.",
     "expr": "48 + 12*dydt = 0",
     "relation": "evaluate",
     "subs": {
      "x": "8",
      "y": "6",
      "dxdt": "3"
     }
    },
    {
     "text": "Solve.",
     "expr": "-4",
     "relation": "solve",
     "variable": "dydt"
    }
   ],
   "calculator_status": "no_calculator",
   "skills": [
    "BC-SKL-04018"
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
    "shape": "cone",
    "size": 3,
    "rate": 9,
    "ratio": 2,
    "leg": "long",
    "length_unit": "centimeter",
    "time_unit": "second"
   },
   "stem": {
    "text": "Water enters a vertex-down cone, height 3 times top radius, at 9 cubic centimeters per second. Find dh/dt when the depth is 3 centimeters.",
    "command_verb": "find"
   },
   "key": {
    "form": "symbolic",
    "expr": "9/pi"
   },
   "steps": [
    {
     "text": "r = h/3 eliminated.",
     "expr": "V = pi*h**3/27",
     "relation": "new"
    },
    {
     "text": "Differentiate in t.",
     "expr": "dVdt = pi*h**2*dhdt/9",
     "relation": "new"
    },
    {
     "text": "h = 3, dV/dt = 9.",
     "expr": "9 = pi*dhdt",
     "relation": "evaluate",
     "subs": {
      "h": "3",
      "dVdt": "9"
     }
    },
    {
     "text": "Solve.",
     "expr": "9/pi",
     "relation": "solve",
     "variable": "dhdt"
    }
   ],
   "options": [
    {
     "id": "A",
     "is_key": false,
     "expr": "3/pi",
     "error_path": "BC-ERR-04016",
     "derivation": "cylinder formula, which drops the factor 1/3"
    },
    {
     "id": "B",
     "is_key": true,
     "expr": "9/pi",
     "error_path": null
    },
    {
     "id": "C",
     "is_key": false,
     "expr": "27/pi",
     "error_path": "BC-ERR-04018",
     "derivation": "radius frozen at 1, so dV/dt = (pi/3) dh/dt"
    },
    {
     "id": "D",
     "is_key": false,
     "expr": "pi",
     "error_path": "BC-ERR-99013",
     "derivation": "dV/dh = pi h^2/9 at h = 3 reported"
    }
   ],
   "calculator_status": "no_calculator",
   "skills": [
    "BC-SKL-04018"
   ]
  }
 ],
 "delivery": [
  {
   "block": "orientation",
   "mode": "figure",
   "reason": "rule 3: BC-REP-08 on BC-SKL-04018 and BC-SKL-04021",
   "sources": [
    "BC-SKL-04018",
    "BC-SKL-04021"
   ],
   "spec": {
    "kind": "diagram",
    "representations": [
     "BC-REP-08"
    ],
    "labels": [
     {
      "text": "h",
      "placement": "inside",
      "at": [
       0.2,
       2
      ]
     },
     {
      "text": "r",
      "placement": "inside",
      "at": [
       0.6,
       4.5
      ]
     },
     {
      "text": "height = 2 times top radius",
      "placement": "inside",
      "at": [
       -3.8,
       6.8
      ]
     }
    ],
    "window": {
     "x": [
      -4,
      4
     ],
     "y": [
      -0.5,
      7
     ]
    },
    "segments": [
     {
      "from": [
       -3,
       6
      ],
      "to": [
       0,
       0
      ]
     },
     {
      "from": [
       0,
       0
      ],
      "to": [
       3,
       6
      ]
     },
     {
      "from": [
       3,
       6
      ],
      "to": [
       -3,
       6
      ]
     },
     {
      "from": [
       -2,
       4
      ],
      "to": [
       2,
       4
      ]
     },
     {
      "from": [
       0,
       0
      ],
      "to": [
       0,
       4
      ],
      "style": "dashed"
     },
     {
      "from": [
       0,
       4
      ],
      "to": [
       2,
       4
      ],
      "style": "dashed"
     }
    ],
    "points": [
     [
      0,
      0
     ],
     [
      2,
      4
     ]
    ]
   },
   "fallback": "the same labelled cone as a static image",
   "keyboard": "none needed: the figure has no control"
  },
  {
   "block": "ki-1",
   "mode": "interactive",
   "reason": "rule 3 promoted: BC-REP-08 on BC-SKL-04018; BC-QA-04006 difficulty_variables name a second variable eliminated by similar triangles, and the reading is which labels move",
   "sources": [
    "BC-SKL-04018",
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
      "parameter": "h",
      "range": [
       0.5,
       6
      ],
      "step": 0.5,
      "start": 4
     }
    ],
    "drawn": [
     "the water surface at depth h",
     "r read from the similar triangle"
    ],
    "labels": [
     {
      "text": "h: varies",
      "placement": "inside",
      "at": [
       0.2,
       1
      ]
     },
     {
      "text": "r = h/2: varies",
      "placement": "inside",
      "at": [
       -3.8,
       0.5
      ]
     },
     {
      "text": "cone shape: fixed",
      "placement": "inside",
      "at": [
       -3.8,
       6.8
      ]
     }
    ],
    "question": "Which labels change as the depth changes, and which equation ties them?",
    "window": {
     "x": [
      -4,
      4
     ],
     "y": [
      -0.5,
      7
     ]
    },
    "segments": [
     {
      "from": [
       -3,
       6
      ],
      "to": [
       0,
       0
      ]
     },
     {
      "from": [
       0,
       0
      ],
      "to": [
       3,
       6
      ]
     },
     {
      "from": [
       3,
       6
      ],
      "to": [
       -3,
       6
      ]
     },
     {
      "from": [
       0,
       0
      ],
      "to": [
       0,
       6
      ],
      "style": "dashed"
     }
    ],
    "curves": [
     {
      "expr": "h + 0*sqrt(h**2/4 - x**2)"
     }
    ],
    "points": [
     {
      "x": "-h/2",
      "y": "h"
     },
     {
      "x": "h/2",
      "y": "h"
     }
    ]
   },
   "fallback": "two static frames of the cone at h = 2 and h = 4 with the same labels",
   "keyboard": "Tab focuses the slider; left and right arrow keys step h by 0.5"
  },
  {
   "block": "ki-2",
   "mode": "text",
   "reason": "rule 5: BC-SKL-04020 carries BC-REP-01 only",
   "sources": [
    "BC-SKL-04020"
   ]
  },
  {
   "block": "ex-1",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  },
  {
   "block": "err-BC-ERR-04016",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  },
  {
   "block": "err-BC-ERR-04018",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  },
  {
   "block": "err-BC-ERR-04019",
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
  "err-BC-ERR-04016",
  "err-BC-ERR-04018",
  "err-BC-ERR-04019",
  "err-BC-ERR-99013",
  "ex-1"
 ],
 "research_lines": [
  {
   "file": "research/units/unit-04-contextual-applications-differentiation.md",
   "line": "Where the supplied rates cannot support two varying dimensions, one is eliminated before differentiating."
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
   "claim": "BC-ERR-99033 is not served because the cap of four error blocks is reached.",
   "settles": "A review of error order for BC-CON-04008."
  }
 ],
 "sources": [
  "BC-CON-04008",
  "BC-SKL-04018",
  "BC-SKL-04020",
  "BC-SKL-04021",
  "BC-EK-CHA-3D1",
  "BC-EK-CHA-3D2",
  "ced:90",
  "BC-QA-04006",
  "BC-QA-04007",
  "BC-PT-99023",
  "cr-22:7",
  "BC-ERR-04016",
  "BC-ERR-04018",
  "BC-ERR-04019",
  "BC-ERR-99013",
  "BC-MIS-04008",
  "BC-MIS-04009",
  "BC-MIS-04010",
  "BC-PRQ-04001",
  "BC-PRQ-04002",
  "BC-PRQ-04003",
  "BC-PRQ-04008",
  "research/units/unit-04-contextual-applications-differentiation.md#4.4 Introduction to Related Rates",
  "research/question-analysis/question-archetypes.md#BC-QA-04006 Related rates in a geometric setting",
  "research/question-analysis/question-archetypes.md#BC-QA-04007 Related rates on an implicitly defined curve",
  "research/scoring/common-point-losses.md#Units points",
  "research/exam/exam-structure.md#Section and part layout"
 ],
 "word_count": {
  "full": 656,
  "brief": 428
 },
 "read_minutes": {
  "full": 4.4,
  "brief": 2.9
 }
}
```
