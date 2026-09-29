---
title: LSN-CON-08015 Cross sectional dimension read from the region
research_date: 2026-09-29
status: designed
purpose: Authoring spec for the concept lesson on BC-CON-08015, the side of a cross section written as the distance between the two boundary curves of the base, built from authoring_bundle("BC-CON-08015") and the research files it cites, so an author fills plan 15's lesson record without making a teaching decision.
---

# LSN-CON-08015 Cross sectional dimension read from the region

Concept BC-CON-08015 (skill BC-SKL-08031), topic 8.7 of Unit 8, loaded by one archetype, BC-QA-08011 (family cross-sectional-volume), which also loads the volume and slice shape concepts BC-CON-08014 and BC-CON-08016. Its hard parent is BC-CON-08010, and it is itself a hard parent of every volume concept (docs/lessons/unit-08/README.md, section 1).

## Prediction

One multiple choice question on worked example 1's own numbers, asked before the rule is shown: the base lies between f(x) = -x^2 + 3x + 1 and g(x) = x + 1 on [0, 2] with square cross sections perpendicular to the x-axis, and the student picks the side of the slice at x. The key is f(x) - g(x), ex-1's side; the distractors are f(x) alone (BC-ERR-08028) and the square of the difference, which is the slice area and not its side. The resolution states that the slice runs from g to f and that its side is the distance between them. No verdict word. Sources: BC-CON-08015 and the topic 8.7 section the key idea cites (ced:158).

## Orientation

Served text, from BC-CON-08015 `description_plain` and the topic's Assessment behaviour paragraph (research/units/unit-08-applications-integration.md#8.7 Volumes with Cross Sections: Squares and Rectangles): a response writes the side of each slice as the distance between the two boundary curves, upper minus lower, before any area formula or integral. No count, no frequency.

## Key ideas

BC-SKL-08031 maps to BC-EK-CHA-5B1 (ced:158): one core block, both bands.

- ki-1 (core). Paraphrase of the Required mathematical knowledge paragraphs (Cross section volume; Side length; Notation): the volume is the integral of the slice area over the interval the solid spans; the side is a distance in the base, so the difference of the two boundary functions, or one function only when the other boundary is an axis; no pi for a polygonal slice. Anchor quote from ced:158. Notation line from the concept record.

## Recognition

BC-QA-08011 (research/question-analysis/question-archetypes.md#BC-QA-08011 Volume of a solid with known cross sections): `typical_wording` "the base of a solid is the given region and its cross sections perpendicular to the stated axis are the named shape; find the volume of the solid"; `common_givens` a base region, the shape of the cross sections, the axis they are perpendicular to; `asked_to_produce` an integrand, the volume. The signal: "base" and "cross sections perpendicular to", with a base bounded by two curves (BC-SKL-08031 `adaptive.diagnostic_archetypes`). Shapes: an MCQ (BC-MCQ-PE2012-040) and a part of the region question after the area part (BC-FRQ-2022-Q5-B).

The near miss served in the contrast pair of st-1 comes from the sibling archetype BC-QA-08013 (washer method, BC-CON-08019) and the `wrong_approaches` entry that squares the boundary functions separately: the same two curves revolved about the x-axis, where each radius is squared separately. The pair differs in the one thing the feature names, squares standing on the base against a revolution.

What says "not this concept": "revolved about" (disc or washer, BC-CON-08017, BC-CON-08019); a base bounded by one curve and an axis, where the side is one function value.

## Method choice

One strategy block, both bands.

- st-1, BC-QA-08011, carrying the contrast pair. Cue from `asked_to_produce` and `common_givens`. Method, `expected_solution_path[0]`: write the distance between the boundary curves. Rival, `wrong_approaches`: squaring the boundary functions separately (BC-ERR-99011). Separating feature: the slice has two ends, one on each curve, so both appear in the side. Both fields are present, so the block is not tagged inferred.

## Solution path

- ex-1, BC-QA-08011, both bands, no calculator. Draw from `parameter_spec`: shape square, tool by_hand, left 0, width 2, bulge 1, slope 1, intercept 1, height_ratio 2, peak 2, spread 2, drop 1, reach 2, presentation formula; so the base lies between f(x) = -x^2 + 3x + 1 and g(x) = x + 1 on [0, 2], the side is 2x - x^2 and the volume 16/15. No published BC-QA-08011 item carries this draw.
- Steps follow `expected_solution_path`: which end is upper (no value); the side as f minus g (new); simplified (equivalent); the integral of the side squared (new, tagged BC-PT-99001); expanded and evaluated (equivalent); the volume (equivalent). A fluent solver writes steps 2 to 6 and holds the upper end test [inferred].

## Scoring

BC-QA-08011 lists BC-PT-99001, 99056, 99057 and 99004. ex-1 tags BC-PT-99001 on the integral with limits; the reader line is `reader_checks(["BC-PT-99001"])` copied exactly. BC-PT-99056 and 99057 (integration by parts) are not on this draw's path. For the author: the archetype's scoring pattern is a setup point for the integrand with the limits and an answer point, and integrands from the wrong area or volume family are recorded as BC-ERR-99011 (research/scoring/common-point-losses.md#Setup points).

## Traps

Three active errors meet the skill, in the bundle's order: BC-ERR-08028, BC-ERR-99011, BC-ERR-99033. Low band all three; mid band the first two. All on ex-1's draw. All three are fix prompts (`fix_prompt` true, relation distinct).

- err-BC-ERR-08028: the side taken as f alone. Possible reason, words from BC-MIS-08016.
- err-BC-ERR-99011: pi placed in front of a square slice. Possible reason, words from BC-MIS-08015.
- err-BC-ERR-99033: the side named s and never defined, so the integral of s^2 does not define a number. No possible reason line: the linked BC-MIS-05022 describes derivative notation, not this setup.

## Representations

None as a separate block. The topic's Representations paragraph names a verbal description of the solid converted to a diagram of one slice (BC-REP-04 to BC-REP-08), which the orientation and ki-1 figures carry.

## Prerequisite bridge

- BC-PRQ-08004, from its `description_plain` and `failure_signature`.

## Time

BC-QA-08011 is `either`; the design takes Section I Part A, 2.14 minutes per question (research/exam/exam-structure.md#Section and part layout) [inferred: an either archetype placed in I-A]. As a free response part it is two points, 3.33 minutes (docs/lessons/unit-08/README.md, section 5). The minutes go on expanding the squared side and the antiderivative.

## Checks

- chk-1, completion of ex-1, both bands: evaluate the integral of the squared side. Key 16/15.
- chk-2, isomorph, both bands. Draw: square, by_hand, left 1, width 3, bulge 1, slope -1, intercept 2, height_ratio 2, peak 2, spread 2, drop 1, reach 2, formula; base between -x^2 + 4x - 2 and 2 - x on [1, 4]. Key 81/10.
- chk-3, MCQ, low band. Draw: square, by_hand, left -1, width 2, bulge 2, slope 0, intercept 1, height_ratio 2, peak 2, spread 2, drop 1, reach 2, formula; base between 3 - 2x^2 and y = 1 on [-1, 1]. Key the integral of (2 - 2x^2)^2, 64/15. Distractors: f alone squared (BC-ERR-08028), pi times the key (BC-ERR-99011), f^2 - g^2 (BC-ERR-99011).

## Delivery

- orientation: figure. Rule 4: BC-REP-08 on BC-SKL-08031; unit README delivery map.
- ki-1: figure. Rule 4, same field: one slice drawn across the base region with both endpoints on the curves labelled. Not promoted: the concept's archetype varies a category, not a quantity read from the figure [inferred; settled by the modality A/B].
- ex-1: step_reveal. Rule 1.
- err-BC-ERR-08028, err-BC-ERR-99011, err-BC-ERR-99033: step_reveal. Rule 1.

## Band plan

- Low (full), in served order: prediction, orientation, the bridge, ki-1, st-1 with the contrast pair, ex-1 with its reader line, chk-1, the three error blocks, chk-2, chk-3. 532 words, 3.6 minutes (cap 900 and 6). There is no second example, so nothing is faded.
- Mid (brief): prediction, orientation, the bridge, ki-1, st-1 with the contrast pair, ex-1 with its reader line, chk-1, err-BC-ERR-08028, err-BC-ERR-99011, chk-2. 446 words, 3.0 minutes (cap 450 and 3). To fit the cap the orientation, ki-1 (the sentence on the integral of the slice area is dropped, ki-1 of LSN-CON-08014 carries it), the strategy fields, the step cues and whys and the bridge were shortened; the anchor quote and the scoring tag were kept.
- Refresher: ki-1, err-BC-ERR-08028, err-BC-ERR-99011, err-BC-ERR-99033, ex-1.

## Sources

- BC-CON-08015; BC-SKL-08031; BC-EK-CHA-5B1; ced:158
- BC-QA-08011, BC-QA-08013 (the contrast pair's near miss); BC-PT-99001; BC-MCQ-PE2012-040; BC-FRQ-2022-Q5-B
- BC-ERR-08028, BC-ERR-99011, BC-ERR-99033; BC-MIS-08015, BC-MIS-08016, BC-MIS-05022
- BC-PRQ-08004
- research/units/unit-08-applications-integration.md#8.7 Volumes with Cross Sections: Squares and Rectangles
- research/question-analysis/question-archetypes.md#BC-QA-08011 Volume of a solid with known cross sections
- research/scoring/common-point-losses.md#Setup points
- research/exam/exam-structure.md#Section and part layout
- [inferred] BC-QA-08011 is either; the lesson takes I-A. Settled by a ruling on which part an either archetype's budget comes from.
- [inferred] BC-PT-99004 is earned on ex-1's last step but not tagged, to keep the brief band under 450 words. Settled by a brief cap that exempts reader lines.
- [inferred] The orientation and ki-1 figures, and the held upper end test. Settled by the modality A/B and timing data per step.

## Machine record

```json
{
 "id": "LSN-CON-08015",
 "kind": "concept",
 "target_id": "BC-CON-08015",
 "unit": "08",
 "skills": [
  "BC-SKL-08031"
 ],
 "prediction": {
  "id": "pr-1",
  "stem": {
   "text": "A solid's base lies between \\(f(x)=-x^2+3x+1\\) and \\(g(x)=x+1\\) for \\(0\\le x\\le 2\\), with square cross sections perpendicular to the x-axis. What is the side of the slice at x?",
   "command_verb": "predict"
  },
  "format": "mcq",
  "options": [
   {
    "id": "A",
    "label": "\\(f(x)\\)",
    "is_key": false
   },
   {
    "id": "B",
    "label": "\\(f(x)-g(x)\\)",
    "is_key": true
   },
   {
    "id": "C",
    "label": "\\((f(x)-g(x))^2\\)",
    "is_key": false
   }
  ],
  "resolution": "The slice runs from g to f, so its side is \\(f(x)-g(x)=2x-x^2\\), not f(x) alone.",
  "sources": [
   "BC-CON-08015",
   "ced:158"
  ]
 },
 "orientation": {
  "text": "A response writes each side as upper minus lower before any area formula.",
  "sources": [
   "BC-CON-08015",
   "research/units/unit-08-applications-integration.md#8.7 Volumes with Cross Sections: Squares and Rectangles"
  ]
 },
 "key_ideas": [
  {
   "id": "ki-1",
   "ek_id": "BC-EK-CHA-5B1",
   "depth": "core",
   "text": "The side of a slice is upper boundary minus lower, or one function when the other boundary is an axis. No pi for a polygonal slice.",
   "notation": "side length as a difference of functions",
   "quote": {
    "text": "Volumes of solids with square and rectangular cross sections can be found using definite integrals",
    "source": "ced:158"
   },
   "sources": [
    "BC-EK-CHA-5B1",
    "ced:158",
    "research/units/unit-08-applications-integration.md#8.7 Volumes with Cross Sections: Squares and Rectangles"
   ]
  }
 ],
 "strategy": [
  {
   "id": "st-1",
   "archetype_id": "BC-QA-08011",
   "cue": "Base region, named cross section; volume asked.",
   "method": "The side as the distance between the curves.",
   "rival": "Each function squared separately.",
   "separating_feature": "The slice has one end on each curve.",
   "sources": [
    "BC-QA-08011",
    "BC-QA-08013",
    "BC-ERR-99011"
   ],
   "evidence_tag": "verified",
   "contrast": {
    "this": {
     "text": "The base between \\(y=x^2\\) and \\(y=x+2\\) has square cross sections perpendicular to the x-axis. Find the volume.",
     "archetype_id": "BC-QA-08011"
    },
    "not_this": {
     "text": "The region between \\(y=x^2\\) and \\(y=x+2\\) is revolved about the x-axis. Find the volume.",
     "why_not": "Revolution gives washers, with radii squared separately."
    },
    "feature": "Squares stand on the base."
   }
  }
 ],
 "worked_examples": [
  {
   "id": "ex-1",
   "archetype_id": "BC-QA-08011",
   "bands": [
    "low",
    "mid"
   ],
   "parameter_draw": {
    "shape": "square",
    "tool": "by_hand",
    "left": 0,
    "width": 2,
    "bulge": 1,
    "slope": 1,
    "intercept": 1,
    "height_ratio": 2,
    "peak": 2,
    "spread": 2,
    "drop": "1",
    "reach": "2",
    "presentation": "formula"
   },
   "problem": {
    "text": "A solid's base lies between \\(f(x)=-x^2+3x+1\\) and \\(g(x)=x+1\\) for \\(0\\le x\\le 2\\). Cross sections perpendicular to the x-axis are squares. Find the volume.",
    "command_verb": "find"
   },
   "calculator_status": "no_calculator",
   "steps": [
    {
     "cue": "Which end is upper?",
     "why": "\\(f(1)=3\\), \\(g(1)=2\\)."
    },
    {
     "cue": "Side: distance between curves.",
     "why": "Both ends appear.",
     "expr": "-x**2 + 3*x + 1 - (x + 1)",
     "relation": "new"
    },
    {
     "cue": "Simplify.",
     "why": "The side at x.",
     "expr": "2*x - x**2",
     "relation": "equivalent"
    },
    {
     "cue": "Area is side squared.",
     "why": "No pi for a square.",
     "expr": "Integral((2*x - x**2)**2, (x, 0, 2))",
     "relation": "new",
     "point_type_id": "BC-PT-99001"
    },
    {
     "cue": "Expand, then integrate.",
     "why": "\\(4x^2-4x^3+x^4\\).",
     "expr": "32/3 - 16 + 32/5",
     "relation": "equivalent"
    },
    {
     "cue": "The volume is asked.",
     "why": "Exact.",
     "expr": "16/15",
     "relation": "equivalent"
    }
   ],
   "answer": {
    "form": "numeric",
    "expr": "16/15"
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
   "error_id": "BC-ERR-08028",
   "observed_behavior": "The side of the slice is taken as the upper curve alone although the region is bounded by two curves.",
   "scoring_consequence": "The integrand is wrong, so the setup point is lost.",
   "wrong_step": {
    "text": "Side \\(f(x)\\).",
    "expr": "-x**2 + 3*x + 1"
   },
   "right_step": {
    "text": "Side \\(f(x)-g(x)\\).",
    "expr": "2*x - x**2"
   },
   "relation": "distinct",
   "possible_reason": {
    "misconception_id": "BC-MIS-08016",
    "text": "reads the slice as reaching from the axis to the curve"
   },
   "sources": [
    "BC-ERR-08028",
    "BC-MIS-08016"
   ],
   "fix_prompt": true
  },
  {
   "error_id": "BC-ERR-99011",
   "observed_behavior": "Responses square a difference of functions when an area was asked, insert pi where no revolution occurs, square each function separately instead of squaring their difference, or revolve about the wrong line.",
   "scoring_consequence": "The integrand point is not earned; where the form point is separate, an eligible form may still earn it.",
   "wrong_step": {
    "text": "pi in front.",
    "expr": "pi*Integral((2*x - x**2)**2, (x, 0, 2))"
   },
   "right_step": {
    "text": "No pi.",
    "expr": "Integral((2*x - x**2)**2, (x, 0, 2))"
   },
   "relation": "distinct",
   "possible_reason": {
    "misconception_id": "BC-MIS-08015",
    "text": "associates pi with volume rather than with circular cross sections"
   },
   "sources": [
    "BC-ERR-99011",
    "BC-MIS-08015"
   ],
   "fix_prompt": true
  },
  {
   "error_id": "BC-ERR-99033",
   "observed_behavior": "Responses invent a symbol for an intermediate quantity, differentiate with it, and never state what it stands for, so the connection between the new symbol and the functions given in the stem cannot be read.",
   "scoring_consequence": "The point for expressing the quantity as a function of the given variable is not earned, and the chain rule step that depends on it is unreachable.",
   "wrong_step": {
    "text": "\\(\\int_0^2 s^2\\,dx\\), s never defined.",
    "expr": "Integral(s**2, (x, 0, 2))"
   },
   "right_step": {
    "text": "s written as \\(2x-x^2\\).",
    "expr": "Integral((2*x - x**2)**2, (x, 0, 2))"
   },
   "relation": "distinct",
   "possible_reason": null,
   "sources": [
    "BC-ERR-99033"
   ],
   "fix_prompt": true
  }
 ],
 "representations": null,
 "prerequisite_bridges": [
  {
   "prq_id": "BC-PRQ-08004",
   "text": "A distance is larger minus smaller."
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
   "archetype_id": "BC-QA-08011",
   "parameter_draw": {
    "shape": "square",
    "tool": "by_hand",
    "left": 0,
    "width": 2,
    "bulge": 1,
    "slope": 1,
    "intercept": 1,
    "height_ratio": 2,
    "peak": 2,
    "spread": 2,
    "drop": "1",
    "reach": "2",
    "presentation": "formula"
   },
   "completes": "ex-1",
   "stem": {
    "text": "Evaluate \\(\\int_0^2 (2x-x^2)^2\\,dx\\).",
    "command_verb": "evaluate"
   },
   "key": {
    "form": "numeric",
    "expr": "16/15"
   },
   "steps": [
    {
     "text": "The integral.",
     "expr": "Integral((2*x - x**2)**2, (x, 0, 2))",
     "relation": "new"
    },
    {
     "text": "Evaluated.",
     "expr": "16/15",
     "relation": "equivalent"
    }
   ],
   "calculator_status": "no_calculator",
   "skills": [
    "BC-SKL-08031"
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
   "archetype_id": "BC-QA-08011",
   "parameter_draw": {
    "shape": "square",
    "tool": "by_hand",
    "left": 1,
    "width": 3,
    "bulge": 1,
    "slope": -1,
    "intercept": 2,
    "height_ratio": 2,
    "peak": 2,
    "spread": 2,
    "drop": "1",
    "reach": "2",
    "presentation": "formula"
   },
   "stem": {
    "text": "Base between \\(-x^2+4x-2\\) and \\(2-x\\) on \\([1,4]\\); square slices perpendicular to the x-axis. Find the volume.",
    "command_verb": "find"
   },
   "key": {
    "form": "numeric",
    "expr": "81/10"
   },
   "steps": [
    {
     "text": "Side.",
     "expr": "-x**2 + 4*x - 2 - (2 - x)",
     "relation": "new"
    },
    {
     "text": "Simplified.",
     "expr": "-x**2 + 5*x - 4",
     "relation": "equivalent"
    },
    {
     "text": "Integral of the side squared.",
     "expr": "Integral((-x**2 + 5*x - 4)**2, (x, 1, 4))",
     "relation": "new",
     "point_type_id": "BC-PT-99001"
    },
    {
     "text": "Evaluated.",
     "expr": "81/10",
     "relation": "equivalent"
    }
   ],
   "calculator_status": "no_calculator",
   "skills": [
    "BC-SKL-08031"
   ]
  },
  {
   "id": "chk-3",
   "check_kind": "mcq",
   "format": "mcq",
   "bands": [
    "low"
   ],
   "archetype_id": "BC-QA-08011",
   "parameter_draw": {
    "shape": "square",
    "tool": "by_hand",
    "left": -1,
    "width": 2,
    "bulge": 2,
    "slope": 0,
    "intercept": 1,
    "height_ratio": 2,
    "peak": 2,
    "spread": 2,
    "drop": "1",
    "reach": "2",
    "presentation": "formula"
   },
   "stem": {
    "text": "Base between \\(y=3-2x^2\\) and \\(y=1\\); square slices perpendicular to the x-axis. Which gives the volume?",
    "command_verb": "identify"
   },
   "key": {
    "form": "numeric",
    "expr": "64/15"
   },
   "steps": [
    {
     "text": "Side \\(2-2x^2\\) on \\([-1,1]\\).",
     "expr": "Integral((2 - 2*x**2)**2, (x, -1, 1))",
     "relation": "new"
    },
    {
     "text": "Evaluated.",
     "expr": "64/15",
     "relation": "equivalent"
    }
   ],
   "options": [
    {
     "id": "A",
     "is_key": false,
     "expr": "Integral((3 - 2*x**2)**2, (x, -1, 1))",
     "error_path": "BC-ERR-08028",
     "derivation": "the upper curve alone as the side"
    },
    {
     "id": "B",
     "is_key": true,
     "expr": "Integral((2 - 2*x**2)**2, (x, -1, 1))",
     "error_path": null
    },
    {
     "id": "C",
     "is_key": false,
     "expr": "pi*Integral((2 - 2*x**2)**2, (x, -1, 1))",
     "error_path": "BC-ERR-99011",
     "derivation": "pi placed in front of a square slice"
    },
    {
     "id": "D",
     "is_key": false,
     "expr": "Integral((3 - 2*x**2)**2 - 1, (x, -1, 1))",
     "error_path": "BC-ERR-99011",
     "derivation": "each boundary squared separately"
    }
   ],
   "calculator_status": "no_calculator",
   "skills": [
    "BC-SKL-08031"
   ]
  }
 ],
 "delivery": [
  {
   "block": "orientation",
   "mode": "figure",
   "reason": "rule 4: BC-REP-08 on BC-SKL-08031; unit README delivery map",
   "sources": [
    "BC-SKL-08031"
   ],
   "spec": {
    "kind": "region",
    "representations": [
     "BC-REP-08"
    ],
    "window": {
     "x": [
      -0.5,
      2.5
     ],
     "y": [
      0,
      4
     ]
    },
    "curves": [
     {
      "expr": "-x**2 + 3*x + 1",
      "domain": [
       0,
       2
      ]
     },
     {
      "expr": "x + 1",
      "domain": [
       0,
       2
      ]
     }
    ],
    "shade": {
     "between": [
      "-x**2 + 3*x + 1",
      "x + 1"
     ],
     "x": [
      0,
      2
     ]
    },
    "labels": [
     {
      "text": "base region",
      "placement": "inside"
     },
     {
      "text": "square slices stand on it",
      "placement": "inside"
     }
    ]
   },
   "fallback": "the same base region static with its labels",
   "keyboard": "no control; the figure description is reached with Tab"
  },
  {
   "block": "ki-1",
   "mode": "figure",
   "reason": "rule 4: BC-REP-08 on BC-SKL-08031; not promoted, BC-QA-08011 difficulty_variables vary a category",
   "sources": [
    "BC-SKL-08031",
    "BC-QA-08011"
   ],
   "spec": {
    "kind": "region",
    "representations": [
     "BC-REP-08",
     "BC-REP-01"
    ],
    "window": {
     "x": [
      -0.5,
      2.5
     ],
     "y": [
      0,
      4
     ]
    },
    "curves": [
     {
      "expr": "-x**2 + 3*x + 1",
      "domain": [
       0,
       2
      ]
     },
     {
      "expr": "x + 1",
      "domain": [
       0,
       2
      ]
     }
    ],
    "segments": [
     {
      "x": 1,
      "from": [
       1,
       2
      ],
      "to": [
       1,
       3
      ]
     }
    ],
    "labels": [
     {
      "text": "top end on f: (1, 3)",
      "placement": "inside"
     },
     {
      "text": "bottom end on g: (1, 2)",
      "placement": "inside"
     },
     {
      "text": "side = f(x) - g(x)",
      "placement": "inside"
     }
    ]
   },
   "fallback": "the static base with one slice at x = 1 and both endpoints labelled",
   "keyboard": "no control; the figure description is reached with Tab"
  },
  {
   "block": "ex-1",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  },
  {
   "block": "err-BC-ERR-08028",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  },
  {
   "block": "err-BC-ERR-99011",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  },
  {
   "block": "err-BC-ERR-99033",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  }
 ],
 "refresher": [
  "ki-1",
  "err-BC-ERR-08028",
  "err-BC-ERR-99011",
  "err-BC-ERR-99033",
  "ex-1"
 ],
 "read_minutes": {
  "full": 3.6,
  "brief": 3.0
 },
 "word_count": {
  "full": 531,
  "brief": 445
 },
 "research_lines": [
  {
   "file": "research/units/unit-08-applications-integration.md",
   "line": "The side is a distance in the plane region, so it is the difference of the two boundary functions"
  }
 ],
 "inferred": [
  {
   "claim": "BC-QA-08011 is an either archetype; the lesson takes Section I Part A and its 2.14 minute budget.",
   "settles": "A ruling on which exam part an either archetype's budget comes from."
  },
  {
   "claim": "BC-PT-99004 is earned on ex-1's last step but not tagged, because its reader line pushes the brief band past 450 words.",
   "settles": "A brief word cap that exempts reader lines, or a shorter reader_checks form."
  },
  {
   "claim": "The orientation and ki-1 are static figures, and the upper end test is held in the head.",
   "settles": "The modality A/B in the build plan, and timing data per step from 10's fluency telemetry."
  }
 ],
 "sources": [
  "BC-CON-08015",
  "BC-SKL-08031",
  "BC-EK-CHA-5B1",
  "ced:158",
  "BC-QA-08011",
  "BC-PT-99001",
  "BC-MCQ-PE2012-040",
  "BC-FRQ-2022-Q5-B",
  "BC-ERR-08028",
  "BC-ERR-99011",
  "BC-ERR-99033",
  "BC-MIS-08015",
  "BC-MIS-08016",
  "BC-MIS-05022",
  "BC-PRQ-08004",
  "research/units/unit-08-applications-integration.md#8.7 Volumes with Cross Sections: Squares and Rectangles",
  "research/question-analysis/question-archetypes.md#BC-QA-08011 Volume of a solid with known cross sections",
  "research/scoring/common-point-losses.md#Setup points",
  "research/exam/exam-structure.md#Section and part layout"
 ]
}
```
