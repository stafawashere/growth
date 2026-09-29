---
title: LSN-CON-08014 Volume as the integral of a cross sectional area
research_date: 2026-09-29
status: designed
purpose: Authoring spec for the concept lesson on BC-CON-08014, the volume of a solid with square or rectangular cross sections as the integral of the slice area, built from authoring_bundle("BC-CON-08014") and the research files it cites, so an author fills plan 15's lesson record without making a teaching decision.
---

# LSN-CON-08014 Volume as the integral of a cross sectional area

Concept BC-CON-08014 (skills BC-SKL-08032, BC-SKL-08033, BC-SKL-08034, BC-SKL-08035), topic 8.7 of Unit 8, loaded by one archetype, BC-QA-08011 (family cross-sectional-volume). Its hard parents are BC-CON-08012 and BC-CON-08015 (docs/lessons/unit-08/README.md, section 1), so the side as the distance between the curves is assumed and used here, not taught.

## Prediction

One multiple choice question on worked example 1's own numbers, asked before the rule is shown: R lies between f(x) = -x^2 + 3x + 1 and g(x) = x + 1 with rectangular cross sections of height twice the base, and the student picks the slice area at x. The key is 2(f(x) - g(x))^2, ex-1's slice area; the distractors are 2f(x)^2 - 2g(x)^2 (BC-ERR-08030) and (f(x) - g(x))^2 (BC-ERR-08031). The resolution states the base as the distance between the curves, the height as twice it, and the slice area that follows. No verdict word. Sources: BC-CON-08014 and the topic 8.7 section the key idea cites (ced:158).

## Orientation

Served text, from BC-CON-08014 `description_plain` and the topic's Assessment behaviour paragraph (research/units/unit-08-applications-integration.md#8.7 Volumes with Cross Sections: Squares and Rectangles): a response writes the area of one slice from the side, integrates it over the interval the base spans, and reports the volume, with no factor of pi. No count, no frequency.

## Key ideas

All four skills map to BC-EK-CHA-5B1 (ced:158), so one core block, both bands.

- ki-1 (core). Paraphrase of the Required mathematical knowledge paragraphs (Cross section volume; Square and rectangular sections; Notation): the volume is the definite integral of the slice area over the interval; a square slice has area side squared, a rectangle side times the stated second dimension; no pi for a polygonal slice. No anchor quote: the CHA-5.B.1 sentence on ced:158 costs 18 words the brief band does not have (Band plan). Notation line from the concept record.

## Recognition

BC-QA-08011 (research/question-analysis/question-archetypes.md#BC-QA-08011 Volume of a solid with known cross sections): `typical_wording` "the base of a solid is the given region and its cross sections perpendicular to the stated axis are the named shape; find the volume of the solid"; `common_givens` a base region, the shape of the cross sections, the axis they are perpendicular to; `asked_to_produce` an integrand, the volume. The signal is the pair "base" and "cross sections perpendicular to": nothing is revolved. Shapes: an MCQ asking which integral gives the volume, or one part of a free response that opens with an area part on the same region (`multipart_structure`; official examples BC-FRQ-2022-Q5-B, BC-MCQ-PE2012-040).

The near miss served in the contrast pair of st-1 comes from the sibling archetype BC-QA-08013 (washer method, BC-CON-08019): the same two curves, but the region is revolved about the x-axis, so the slices are washers and pi appears. The pair differs in the one thing the feature names, cross sections of a named shape against a revolution.

What says "not this concept": "revolved about" selects a disc or washer (BC-CON-08017, 08019), and the named shape triangle or semicircle moves the constant to BC-CON-08016 (docs/lessons/unit-08/README.md, section 3).

## Method choice

One strategy block, both bands.

- st-1, BC-QA-08011, carrying the contrast pair. Cue from `asked_to_produce` and `common_givens`. Method, `expected_solution_path[0]`: write the distance between the boundary curves, then the shape's area. Rival, `wrong_approaches`: squaring the boundary functions separately (BC-ERR-08030). Separating feature: the side is one length, the difference, so the difference is squared as a whole. The archetype carries both cue fields, so the block is not tagged inferred.

## Solution path

- ex-1, BC-QA-08011, both bands, no calculator. Draw from `parameter_spec`: shape rectangle, tool by_hand, left 0, width 2, bulge 1, slope 1, intercept 1, height_ratio 2 (peak 3, spread 2, drop 1, reach 2, presentation formula, unused by hand). So g(x) = x + 1, f(x) = -x^2 + 3x + 1, meeting at x = 0 and 2; rectangles with height twice the base. No published BC-QA-08011 item carries this draw.
- ex-2, BC-QA-08011, low band, no calculator, faded from step 3 (`fade_from` 3): shape square, left -1, width 2, bulge 2, slope 0, intercept 1, so g = 1 and f = 1 + 2(x + 1)(1 - x). Steps 1 and 2 (the side and the slice area) are shown and the student writes the volume; steps 3 and 4 (the integral with its limits, the value) are then revealed. The fade falls there because the side and the slice area are the concept's own content, already worked in ex-1, and the limits and the evaluation are the routine part the student now produces.
- Steps follow `expected_solution_path`: the side (new, then simplified), the slice area (new), the integral with limits (new), the value (equivalent). A fluent solver writes the side, the integral and the value; the simplification is held in the head.

## Scoring

BC-QA-08011 lists BC-PT-99001, BC-PT-99056, BC-PT-99057 and BC-PT-99004. The integration by parts pair belongs to BC-FRQ-2022-Q5-B's technique, not to the volume shape (docs/lessons/unit-08/README.md, Library gaps met), so neither example tags them. ex-1 tags BC-PT-99001 on the integral; ex-2 tags BC-PT-99001 and BC-PT-99004. The answer point on ex-1 is not tagged, to hold the brief band at 450 words (inferred array). Point losses: an integrand from the wrong volume family (research/scoring/common-point-losses.md#Setup points) and a decimal with fewer than three places on a technology variant (research/scoring/common-point-losses.md#Answer points).

## Traps

Seven errors meet the skills; the first four in the bundle's order are served: BC-ERR-08023, BC-ERR-08029, BC-ERR-08030, BC-ERR-08031. BC-ERR-99011, BC-ERR-08045 and BC-ERR-99019 fall past the cap of 4. All on ex-1's draw. All four are fix prompts (`fix_prompt` true, relation distinct).

- err-BC-ERR-08023: the integral written with dy on an integrand in x. Possible reason, words from BC-MIS-08013.
- err-BC-ERR-08029: pi placed on the rectangle integrand. Possible reason, words from BC-MIS-08015.
- err-BC-ERR-08030: f squared minus g squared in place of the squared side. Possible reason, words from BC-MIS-08017.
- err-BC-ERR-08031: the rectangle treated as a square. No possible reason line: neither linked description (BC-MIS-08016, BC-MIS-08019) names the second dimension.

## Representations

None as a separate block. The topic's Representations paragraph names the verbal solid to one slice diagram (BC-REP-04 to BC-REP-08); ki-1's motion carries it.

## Prerequisite bridge

- BC-PRQ-06002, BC-PRQ-08002, BC-PRQ-08004, each from its `description_plain` and `failure_signature`.

## Time

BC-QA-08011 is `either` on calculator status, so the lesson takes Section I Part A, 2.14 minutes per question (research/exam/exam-structure.md#Section and part layout) [inferred: an either archetype placed in Part A]. As a free response part it is 2 points of 9, 3.33 minutes (docs/lessons/unit-08/README.md, section 5). The minutes go on the expansion of the squared side; the side itself is held.

## Checks

- chk-1, completion of ex-1, both bands: the integral is given, the student evaluates. Key 32/15.
- chk-2, isomorph, both bands: square, left 0, width 3, bulge 1, slope 1, intercept 0; g = x, f = 4x - x^2. Key 81/10.
- chk-3, MCQ, low band: rectangle, height_ratio 3, left 0, width 1, bulge 2, slope -1, intercept 2; g = 2 - x, f = 2 - x + 2x(1 - x). Key 2/5. Distractors: 2pi/5 (BC-ERR-08029), 17/5 (BC-ERR-08030), 2/15 (BC-ERR-08031).

## Delivery

- orientation: text. Rule 6.
- ki-1: motion. Rule 2, slices accumulating along the axis (docs/lessons/unit-08/README.md, section 6); rule 4 on BC-REP-08 for the static fallback [inferred; settled by the modality A/B].
- ex-1, ex-2: step_reveal. Rule 1.
- the four error blocks: step_reveal. Rule 1.

## Band plan

- Low (full), in served order: prediction, orientation, the three bridges, ki-1, st-1 with the contrast pair, ex-1 with its scoring line, chk-1, the four error blocks, ex-2 faded with its scoring lines, chk-2, chk-3. 783 words, 5.3 minutes (cap 900 and 6).
- Mid (brief): prediction, orientation, the three bridges, ki-1, st-1 with the contrast pair, ex-1 with its scoring line, chk-1, err-BC-ERR-08023, err-BC-ERR-08029, chk-2. 448 words, 3.0 minutes (cap 450 and 3). To fit the cap the orientation, ki-1, the strategy fields, the ex-1 cues and whys and the bridges were shortened; there is no anchor quote and the scoring tag was kept.
- Refresher: ki-1, the four error blocks, ex-1.

## Sources

- BC-CON-08014; BC-SKL-08032, BC-SKL-08033, BC-SKL-08034, BC-SKL-08035; BC-EK-CHA-5B1; ced:158
- BC-QA-08011, BC-QA-08013 (the contrast pair's near miss); BC-PT-99001, BC-PT-99004
- BC-ERR-08023, BC-ERR-08029, BC-ERR-08030, BC-ERR-08031; BC-MIS-08013, BC-MIS-08015, BC-MIS-08016, BC-MIS-08017
- BC-PRQ-06002, BC-PRQ-08002, BC-PRQ-08004
- research/units/unit-08-applications-integration.md#8.7 Volumes with Cross Sections: Squares and Rectangles
- research/question-analysis/question-archetypes.md#BC-QA-08011 Volume of a solid with known cross sections
- research/scoring/common-point-losses.md#Setup points
- research/scoring/common-point-losses.md#Answer points
- research/exam/exam-structure.md#Section and part layout
- [inferred] Part A for an either archetype. Settled by timing data on the cross section items by part.
- [inferred] The answer point on ex-1 left untagged. Settled by raising the brief cap or a shorter BC-PT-99004 reader line.
- [inferred] ki-1 as motion. Settled by the modality A/B.

## Machine record

```json
{
 "id": "LSN-CON-08014",
 "kind": "concept",
 "target_id": "BC-CON-08014",
 "unit": "08",
 "skills": [
  "BC-SKL-08032",
  "BC-SKL-08033",
  "BC-SKL-08034",
  "BC-SKL-08035"
 ],
 "prediction": {
  "id": "pr-1",
  "stem": {
   "text": "Predict: R lies between \\(f(x)=-x^2+3x+1\\) and \\(g(x)=x+1\\); cross sections perpendicular to the x-axis are rectangles of height twice the base. What is the slice area?",
   "command_verb": "predict"
  },
  "format": "mcq",
  "options": [
   {
    "id": "A",
    "label": "\\(2(f(x)-g(x))^2\\)",
    "is_key": true
   },
   {
    "id": "B",
    "label": "\\(2f(x)^2-2g(x)^2\\)",
    "is_key": false
   },
   {
    "id": "C",
    "label": "\\((f(x)-g(x))^2\\)",
    "is_key": false
   }
  ],
  "resolution": "The base is \\(f(x)-g(x)\\) and the height twice that, so the slice area is \\(2(f(x)-g(x))^2\\).",
  "sources": [
   "BC-CON-08014",
   "ced:158"
  ]
 },
 "orientation": {
  "text": "A response integrates the slice area over the base; a polygonal slice carries no pi.",
  "sources": [
   "BC-CON-08014",
   "research/units/unit-08-applications-integration.md#8.7 Volumes with Cross Sections: Squares and Rectangles"
  ]
 },
 "key_ideas": [
  {
   "id": "ki-1",
   "ek_id": "BC-EK-CHA-5B1",
   "depth": "core",
   "text": "Volume is the integral of slice area over the base. The side is the distance between the curves; a square has area side squared, a rectangle side times the other dimension.",
   "notation": "volume as the integral of A",
   "quote": null,
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
   "cue": "Base region, perpendicular cross sections; volume asked.",
   "method": "The side as upper minus lower curve.",
   "rival": "Squaring the boundary functions separately.",
   "separating_feature": "The difference is squared whole.",
   "sources": [
    "BC-QA-08011",
    "BC-QA-08013"
   ],
   "evidence_tag": "verified",
   "contrast": {
    "this": {
     "text": "R, between \\(y=x^2\\) and \\(y=2x\\), is the base of a solid with square cross sections. Find the volume.",
     "archetype_id": "BC-QA-08011"
    },
    "not_this": {
     "text": "R lies between \\(y=x^2\\) and \\(y=2x\\) and is revolved about the x-axis. Find the volume.",
     "why_not": "Revolving gives washers, with pi."
    },
    "feature": "Named-shape cross sections, not a revolution."
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
    "shape": "rectangle",
    "tool": "by_hand",
    "left": 0,
    "width": 2,
    "bulge": 1,
    "slope": 1,
    "intercept": 1,
    "height_ratio": 2,
    "peak": 3,
    "spread": 2,
    "drop": "1",
    "reach": "2",
    "presentation": "formula"
   },
   "problem": {
    "text": "R lies between f(x) = -x^2 + 3x + 1 and g(x) = x + 1. Cross sections perpendicular to the x-axis are rectangles of height twice the base. Find the volume.",
    "command_verb": "find"
   },
   "calculator_status": "no_calculator",
   "steps": [
    {
     "cue": "Base from g to f.",
     "why": "Upper minus lower.",
     "expr": "(-x**2 + 3*x + 1) - (x + 1)",
     "relation": "new"
    },
    {
     "cue": "Simplify first.",
     "why": "Zero at 0 and 2.",
     "expr": "x*(2 - x)",
     "relation": "equivalent"
    },
    {
     "cue": "Height twice the base.",
     "why": "Base times height.",
     "expr": "2*x**2*(2 - x)**2",
     "relation": "new"
    },
    {
     "cue": "Limits: 0 and 2.",
     "why": "No pi: rectangles.",
     "expr": "Integral(2*x**2*(2 - x)**2, (x, 0, 2))",
     "relation": "new",
     "point_type_id": "BC-PT-99001"
    },
    {
     "cue": "Expand and integrate.",
     "why": "Cubic units.",
     "expr": "32/15",
     "relation": "equivalent"
    }
   ],
   "answer": {
    "form": "numeric",
    "expr": "32/15"
   }
  },
  {
   "id": "ex-2",
   "archetype_id": "BC-QA-08011",
   "bands": [
    "low"
   ],
   "parameter_draw": {
    "shape": "square",
    "tool": "by_hand",
    "left": -1,
    "width": 2,
    "bulge": 2,
    "slope": 0,
    "intercept": 1,
    "height_ratio": 2,
    "peak": 3,
    "spread": 2,
    "drop": "1",
    "reach": "2",
    "presentation": "formula"
   },
   "problem": {
    "text": "R lies between f(x) = 1 + 2(x + 1)(1 - x) and g(x) = 1. Cross sections perpendicular to the x-axis are squares. Find the volume.",
    "command_verb": "find"
   },
   "calculator_status": "no_calculator",
   "steps": [
    {
     "cue": "Squares on the x-axis: side from g to f.",
     "why": "The constant 1 cancels.",
     "expr": "2*(x + 1)*(1 - x)",
     "relation": "new"
    },
    {
     "cue": "Square slice.",
     "why": "Side squared.",
     "expr": "4*(x + 1)**2*(1 - x)**2",
     "relation": "new"
    },
    {
     "cue": "The curves meet at x = -1 and 1.",
     "why": "Limits from the base.",
     "expr": "Integral(4*(x + 1)**2*(1 - x)**2, (x, -1, 1))",
     "relation": "new",
     "point_type_id": "BC-PT-99001"
    },
    {
     "cue": "Expand and integrate.",
     "why": "Exact value.",
     "expr": "64/15",
     "relation": "equivalent",
     "point_type_id": "BC-PT-99004"
    }
   ],
   "answer": {
    "form": "numeric",
    "expr": "64/15"
   },
   "fade_from": 3
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
  },
  {
   "example_id": "ex-2",
   "point_type_ids": [
    "BC-PT-99001",
    "BC-PT-99004"
   ],
   "lines": [
    {
     "point_type_id": "BC-PT-99001",
     "text": "Definite integral expression with correct limits. Earned by: A definite integral whose limits match the requested interval and whose integrand matches the requested quantity, with or without the differential (sg-26:4, sg-22:2). Not earned by: An unsupported numerical value, or a definite integral whose bounds are wrong (sg-22:18). Notation: Differential may be omitted; sg-22:2 accepts dx written for dt. sg-23:8 treats a missing differential as recoverable for this point but restricts later eligibility."
    },
    {
     "point_type_id": "BC-PT-99004",
     "text": "Answer with or without supporting work. Earned by: The correct value on its own, with no supporting work required (sg-25:3, sg-26:4). Not earned by: A value outside the accepted precision, or a value inconsistent with a required earlier step where the rubric imposes one. Precision: A reported decimal answer must be accurate to three places after the decimal point, rounded or truncated; at most one point per question is lost to inappropriate rounding (sg-25:2, sg-26:2). sg-26:4 also accepts a stated rounding to the nearest integer and several truncations."
    }
   ]
  }
 ],
 "common_errors": [
  {
   "error_id": "BC-ERR-08023",
   "observed_behavior": "A function of x is integrated with respect to y, or the reverse, without being rewritten.",
   "scoring_consequence": "The setup point is lost because the expression does not define a number.",
   "wrong_step": {
    "text": "dy on an x integrand.",
    "expr": "Integral(2*x**2*(2 - x)**2, (y, 0, 2))"
   },
   "right_step": {
    "text": "dx.",
    "expr": "Integral(2*x**2*(2 - x)**2, (x, 0, 2))"
   },
   "relation": "distinct",
   "possible_reason": {
    "misconception_id": "BC-MIS-08013",
    "text": "treats dx and dy as labels for the direction of slicing"
   },
   "sources": [
    "BC-ERR-08023",
    "BC-MIS-08013"
   ],
   "fix_prompt": true
  },
  {
   "error_id": "BC-ERR-08029",
   "observed_behavior": "A square or triangular cross section volume carries a factor of pi.",
   "scoring_consequence": "The setup point is lost because the integrand belongs to the wrong volume family.",
   "wrong_step": {
    "text": "pi attached.",
    "expr": "pi*Integral(2*x**2*(2 - x)**2, (x, 0, 2))"
   },
   "right_step": {
    "text": "No pi.",
    "expr": "Integral(2*x**2*(2 - x)**2, (x, 0, 2))"
   },
   "relation": "distinct",
   "possible_reason": {
    "misconception_id": "BC-MIS-08015",
    "text": "associates pi with volume rather than with circular cross sections"
   },
   "sources": [
    "BC-ERR-08029",
    "BC-MIS-08015"
   ],
   "fix_prompt": true
  },
  {
   "error_id": "BC-ERR-08030",
   "observed_behavior": "A washer integrand is written as the square of the difference of the two radii, or a squared difference is expanded term by term.",
   "scoring_consequence": "The setup point is lost, and the value is wrong by the cross term.",
   "wrong_step": {
    "text": "Each function squared.",
    "expr": "Integral(2*((-x**2 + 3*x + 1)**2 - (x + 1)**2), (x, 0, 2))"
   },
   "right_step": {
    "text": "The side squared.",
    "expr": "Integral(2*((-x**2 + 3*x + 1) - (x + 1))**2, (x, 0, 2))"
   },
   "relation": "distinct",
   "possible_reason": {
    "misconception_id": "BC-MIS-08017",
    "text": "treats squaring as distributing over subtraction"
   },
   "sources": [
    "BC-ERR-08030",
    "BC-MIS-08017"
   ],
   "fix_prompt": true
  },
  {
   "error_id": "BC-ERR-08031",
   "observed_behavior": "A rectangular section whose height is a stated multiple of its base is treated as a square.",
   "scoring_consequence": "The setup point is lost.",
   "wrong_step": {
    "text": "Area side squared.",
    "expr": "Integral(x**2*(2 - x)**2, (x, 0, 2))"
   },
   "right_step": {
    "text": "Area twice that.",
    "expr": "Integral(2*x**2*(2 - x)**2, (x, 0, 2))"
   },
   "relation": "distinct",
   "possible_reason": null,
   "sources": [
    "BC-ERR-08031"
   ],
   "fix_prompt": true
  }
 ],
 "representations": null,
 "prerequisite_bridges": [
  {
   "prq_id": "BC-PRQ-06002",
   "text": "Rewrite radicals as powers before antidifferentiating."
  },
  {
   "prq_id": "BC-PRQ-08002",
   "text": "Slicing in y needs x as a function of y."
  },
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
    1,
    4,
    5
   ]
  },
  "skipped_steps": {
   "ex-1": [
    2,
    3
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
    "shape": "rectangle",
    "tool": "by_hand",
    "left": 0,
    "width": 2,
    "bulge": 1,
    "slope": 1,
    "intercept": 1,
    "height_ratio": 2,
    "peak": 3,
    "spread": 2,
    "drop": "1",
    "reach": "2",
    "presentation": "formula"
   },
   "completes": "ex-1",
   "stem": {
    "text": "The volume is the integral of 2x^2 (2 - x)^2 from 0 to 2. Evaluate it.",
    "command_verb": "evaluate"
   },
   "key": {
    "form": "numeric",
    "expr": "32/15"
   },
   "steps": [
    {
     "text": "The integral.",
     "expr": "Integral(2*x**2*(2 - x)**2, (x, 0, 2))",
     "relation": "new"
    },
    {
     "text": "Expanded: 8x^2 - 8x^3 + 2x^4.",
     "expr": "Integral(8*x**2 - 8*x**3 + 2*x**4, (x, 0, 2))",
     "relation": "equivalent"
    },
    {
     "text": "64/3 - 32 + 64/5.",
     "expr": "32/15",
     "relation": "equivalent"
    }
   ],
   "calculator_status": "no_calculator",
   "skills": [
    "BC-SKL-08035"
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
    "left": 0,
    "width": 3,
    "bulge": 1,
    "slope": 1,
    "intercept": 0,
    "height_ratio": 2,
    "peak": 3,
    "spread": 2,
    "drop": "1",
    "reach": "2",
    "presentation": "formula"
   },
   "stem": {
    "text": "R lies between f(x) = 4x - x^2 and g(x) = x. Cross sections perpendicular to the x-axis are squares. Find the volume.",
    "command_verb": "find"
   },
   "key": {
    "form": "numeric",
    "expr": "81/10"
   },
   "steps": [
    {
     "text": "Side.",
     "expr": "(4*x - x**2) - x",
     "relation": "new"
    },
    {
     "text": "Area.",
     "expr": "(3*x - x**2)**2",
     "relation": "new"
    },
    {
     "text": "Limits 0 and 3.",
     "expr": "Integral((3*x - x**2)**2, (x, 0, 3))",
     "relation": "new"
    },
    {
     "text": "Value.",
     "expr": "81/10",
     "relation": "equivalent"
    }
   ],
   "calculator_status": "no_calculator",
   "skills": [
    "BC-SKL-08032"
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
    "shape": "rectangle",
    "tool": "by_hand",
    "left": 0,
    "width": 1,
    "bulge": 2,
    "slope": -1,
    "intercept": 2,
    "height_ratio": 3,
    "peak": 3,
    "spread": 2,
    "drop": "1",
    "reach": "2",
    "presentation": "formula"
   },
   "stem": {
    "text": "R lies between f(x) = 2 - x + 2x(1 - x) and g(x) = 2 - x. Cross sections perpendicular to the x-axis are rectangles of height three times the base. The volume is",
    "command_verb": "identify"
   },
   "key": {
    "form": "numeric",
    "expr": "2/5"
   },
   "steps": [
    {
     "text": "Side 2x(1 - x); area 3 times its square.",
     "expr": "12*x**2*(1 - x)**2",
     "relation": "new"
    },
    {
     "text": "Limits 0 and 1.",
     "expr": "Integral(12*x**2*(1 - x)**2, (x, 0, 1))",
     "relation": "new"
    },
    {
     "text": "Value.",
     "expr": "2/5",
     "relation": "equivalent"
    }
   ],
   "options": [
    {
     "id": "A",
     "is_key": false,
     "expr": "2*pi/5",
     "error_path": "BC-ERR-08029",
     "derivation": "pi placed on the rectangle integrand"
    },
    {
     "id": "B",
     "is_key": false,
     "expr": "17/5",
     "error_path": "BC-ERR-08030",
     "derivation": "3 times f squared minus g squared"
    },
    {
     "id": "C",
     "is_key": true,
     "expr": "2/5",
     "error_path": null
    },
    {
     "id": "D",
     "is_key": false,
     "expr": "2/15",
     "error_path": "BC-ERR-08031",
     "derivation": "the rectangle taken as a square, side squared only"
    }
   ],
   "calculator_status": "no_calculator",
   "skills": [
    "BC-SKL-08033"
   ]
  }
 ],
 "delivery": [
  {
   "block": "orientation",
   "mode": "text",
   "reason": "rule 6: a statement of what a response shows",
   "sources": [
    "BC-CON-08014"
   ]
  },
  {
   "block": "ki-1",
   "mode": "motion",
   "reason": "rule 2: slices accumulating along the axis into a solid; rule 4, BC-REP-08 on BC-SKL-08032 and BC-SKL-08033, for the static fallback",
   "sources": [
    "BC-SKL-08032",
    "BC-SKL-08033",
    "BC-SKL-08034"
   ],
   "spec": {
    "kind": "solid_from_slices",
    "representations": [
     "BC-REP-08",
     "BC-REP-02"
    ],
    "base": {
     "upper": "-x^2 + 3x + 1",
     "lower": "x + 1",
     "interval": [
      0,
      2
     ]
    },
    "slice_shape": "rectangle",
    "height_ratio": 2,
    "frames": [
     {
      "x": 0.25
     },
     {
      "x": 0.5
     },
     {
      "x": 1.0
     },
     {
      "x": 1.5
     },
     {
      "x": 1.75
     }
    ],
    "drawn": [
     "the base region in the plane",
     "one rectangle standing on the slice at x",
     "earlier slices left in place, so the solid builds"
    ],
    "labels": [
     {
      "text": "side = f(x) - g(x)",
      "placement": "inside"
     },
     {
      "text": "height = 2 times side",
      "placement": "inside"
     },
     {
      "text": "A(x) = 2 side^2",
      "placement": "inside"
     }
    ]
   },
   "fallback": "three frames side by side (x = 0.5, 1, 1.5), static, each with its three labels inside",
   "keyboard": "Right arrow steps to the next frame, Left arrow to the previous; Space pauses auto-advance",
   "reduced_motion": "no auto-advance; each key press cross-fades to the next frame"
  },
  {
   "block": "ex-1",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  },
  {
   "block": "ex-2",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  },
  {
   "block": "err-BC-ERR-08023",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  },
  {
   "block": "err-BC-ERR-08029",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  },
  {
   "block": "err-BC-ERR-08030",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  },
  {
   "block": "err-BC-ERR-08031",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  }
 ],
 "refresher": [
  "ki-1",
  "err-BC-ERR-08023",
  "err-BC-ERR-08029",
  "err-BC-ERR-08030",
  "err-BC-ERR-08031",
  "ex-1"
 ],
 "read_minutes": {
  "full": 5.3,
  "brief": 3.0
 },
 "word_count": {
  "full": 783,
  "brief": 448
 },
 "research_lines": [
  {
   "file": "research/units/unit-08-applications-integration.md",
   "line": "No factor of pi appears for a polygonal cross section"
  }
 ],
 "inferred": [
  {
   "claim": "BC-QA-08011 is calculator status either, so the lesson takes Section I Part A and its 2.14 minute budget.",
   "settles": "Timing data on cross section items split by exam part."
  },
  {
   "claim": "ex-1's answer step earns BC-PT-99004 but is not tagged, because its reader line would take the brief band past 450 words; ex-2 carries the tag.",
   "settles": "A shorter BC-PT-99004 reader line or a brief cap that admits it."
  },
  {
   "claim": "ki-1 is served as a motion of slices accumulating rather than a static figure.",
   "settles": "The modality A/B in the build plan: skip rate and time to first credited success by mode."
  },
  {
   "claim": "BC-ERR-99011, BC-ERR-08045 and BC-ERR-99019 meet the skills but fall past the cap of four error blocks.",
   "settles": "A cap change in plan 15 or a severity reorder in the bundle."
  }
 ],
 "sources": [
  "BC-CON-08014",
  "BC-SKL-08032",
  "BC-SKL-08033",
  "BC-SKL-08034",
  "BC-SKL-08035",
  "BC-EK-CHA-5B1",
  "ced:158",
  "BC-QA-08011",
  "BC-PT-99001",
  "BC-PT-99004",
  "BC-ERR-08023",
  "BC-ERR-08029",
  "BC-ERR-08030",
  "BC-ERR-08031",
  "BC-MIS-08013",
  "BC-MIS-08015",
  "BC-MIS-08016",
  "BC-MIS-08017",
  "BC-PRQ-06002",
  "BC-PRQ-08002",
  "BC-PRQ-08004",
  "research/units/unit-08-applications-integration.md#8.7 Volumes with Cross Sections: Squares and Rectangles",
  "research/question-analysis/question-archetypes.md#BC-QA-08011 Volume of a solid with known cross sections",
  "research/scoring/common-point-losses.md#Setup points",
  "research/scoring/common-point-losses.md#Answer points",
  "research/exam/exam-structure.md#Section and part layout"
 ]
}
```
