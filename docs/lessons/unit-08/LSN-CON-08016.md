---
title: LSN-CON-08016 Cross sectional area from the shape of the slice
research_date: 2026-09-29
status: designed
purpose: Authoring spec for the concept lesson on BC-CON-08016, the slice area of a triangular or semicircular cross section written from the distance between the curves, built from authoring_bundle("BC-CON-08016") and the research files it cites, so an author fills plan 15's lesson record without making a teaching decision.
---

# LSN-CON-08016 Cross sectional area from the shape of the slice

Concept BC-CON-08016 (skills BC-SKL-08036, BC-SKL-08037, BC-SKL-08038, BC-SKL-08039), topic 8.8 of Unit 8, loaded by one archetype, BC-QA-08011 (family cross-sectional-volume). Its hard parent is BC-CON-08015 (docs/lessons/unit-08/README.md, section 1): the distance between the curves is assumed, and this lesson decides what role that distance plays in the named shape.

## Orientation

Served text, from BC-CON-08016 `description_plain` and the topic's Assessment behaviour paragraph (research/units/unit-08-applications-integration.md#8.8 Volumes with Cross Sections: Triangles and Semicircles): the same distance between the curves goes into a different area formula for each named shape, and a response writes that formula with its constant before integrating. No count, no frequency.

## Key ideas

BC-SKL-08036 and BC-SKL-08037 map to BC-EK-CHA-5B2, BC-SKL-08038 to BC-EK-CHA-5B3, and BC-SKL-08039 to both (ced:159). Two core blocks, both bands.

- ki-1 (core, BC-EK-CHA-5B2). Paraphrase of the Triangular sections paragraph: equilateral area s^2 sqrt(3)/4; right isosceles half the square of a leg, or a quarter of the square of the hypotenuse. Anchor quote, the CHA-5.B.2 sentence on ced:159 (20 words).
- ki-2 (core, BC-EK-CHA-5B3). Paraphrase of the Semicircular sections paragraph: the distance is the diameter, the radius half of it, the area pi s^2/8. No anchor quote: the brief band holds one (Band plan).

## Recognition

BC-QA-08011 (research/question-analysis/question-archetypes.md#BC-QA-08011 Volume of a solid with known cross sections): `common_givens` a base region, the shape of the cross sections, the axis they are perpendicular to; `asked_to_produce` an integrand, the volume; `difficulty_variables` "whether the distance is a side, a leg, a hypotenuse, or a diameter". The signal is the shape word and the phrase that places the distance: "whose diameters lie in the base", "whose hypotenuses lie in the base". The MCQ holds the base fixed and varies the shape (research/units/unit-08-applications-integration.md#8.8 Volumes with Cross Sections: Triangles and Semicircles).

What says "not this concept": a square or rectangle (BC-CON-08014), or "revolved about" (BC-CON-08017).

## Method choice

One strategy block, both bands.

- st-1, BC-QA-08011. Cue from `common_givens` and `difficulty_variables`. Method, `expected_solution_path[1]` after the distance: substitute it into the area formula of the named shape. Rival, `wrong_approaches` and `common_distractors`: using the full circle area for a semicircular section, or the distance as the radius. Separating feature: the phrase saying which part of the shape lies in the base. Both cue fields exist, so not inferred.

## Solution path

- ex-1, BC-QA-08011, both bands, no calculator. Draw: shape semicircle, tool by_hand, left 1, width 2, bulge 1, slope 0, intercept 1 (height_ratio 2, peak 3, spread 2, drop 1, reach 2, presentation formula). g = 1, f = 1 + (x - 1)(3 - x). No published item carries it.
- ex-2, low band: shape hypotenuse, left 0, width 2, bulge 2, slope -1, intercept 2; g = 2 - x, f = 2 - x + 2x(2 - x).
- Steps: the distance (new), its role and the radius (new), the slice area (new), the integral (new), the value (equivalent). A fluent solver writes the area with its constant, the integral and the value; the radius is held.

## Scoring

BC-QA-08011 lists BC-PT-99001, BC-PT-99056, BC-PT-99057, BC-PT-99004; the parts pair is not the volume shape (docs/lessons/unit-08/README.md, Library gaps met). ex-1 tags BC-PT-99001; ex-2 tags BC-PT-99001 and BC-PT-99004. ex-1's answer point is untagged for the brief band (inferred array). Point loss: the wrong volume family (research/scoring/common-point-losses.md#Setup points).

## Traps

Five errors meet the skills; the first four in bundle order are served: BC-ERR-08030, BC-ERR-08033, BC-ERR-08034, BC-ERR-06013. BC-ERR-08032 falls past the cap. Each wrong step sits beside the right one on ex-1's distance s = (x - 1)(3 - x); the leg against hypotenuse pair is the slice area on that distance.

- err-BC-ERR-08030: pi/8 times f squared minus g squared. Possible reason, BC-MIS-08017.
- err-BC-ERR-08033: s^2/2 for a hypotenuse. Possible reason, BC-MIS-08019.
- err-BC-ERR-08034: the distance as the radius. Possible reason, BC-MIS-08018.
- err-BC-ERR-06013: pi r^2 for a semicircle. Possible reason, BC-MIS-08019.

## Representations

None as a separate block. The Representations paragraph's conversion of the slice diagram to the role of the distance (BC-REP-08 to BC-REP-01) is carried by the two key idea figures.

## Prerequisite bridge

- BC-PRQ-06002, BC-PRQ-06007, BC-PRQ-08005, each from its `description_plain` and `failure_signature`.

## Time

BC-QA-08011 is `either`, so Section I Part A, 2.14 minutes (research/exam/exam-structure.md#Section and part layout) [inferred]. As a free response part, 2 points, 3.33 minutes (docs/lessons/unit-08/README.md, section 5). The minutes go on expanding the squared distance.

## Checks

- chk-1, completion of ex-1: the integral is given, the student evaluates. Key 2pi/15.
- chk-2, isomorph: equilateral, left -1, width 2, bulge 1, slope 1, intercept 2; distance 1 - x^2. Key 4 sqrt(3)/15.
- chk-3, MCQ, low band: semicircle, left 0, width 3, bulge 1, slope 0, intercept -1. Key 81pi/80. Distractors 81pi/20 (BC-ERR-08034), 81pi/40 (BC-ERR-06013), -9pi/80 (BC-ERR-08030).

## Delivery

- orientation: text. Rule 6.
- ki-1, ki-2: figure. Rule 4, BC-REP-08 on BC-SKL-08036 to 08038; not promoted, since the varying quantity is a category (docs/lessons/unit-08/README.md, section 6) [inferred; the modality A/B].
- ex-1, ex-2 and the four error blocks: step_reveal. Rule 1.

## Band plan

- Low (full): orientation, ki-1, ki-2, st-1, ex-1 and its line, the four error blocks, chk-1 to chk-3, ex-2 and its lines, the bridges. 762 words, 5.1 minutes.
- Mid (brief): orientation, ki-1, ki-2, st-1, ex-1 and its line, err-BC-ERR-08030, err-BC-ERR-08033, chk-1, chk-2, the bridges. 425 words, 2.9 minutes.
- Refresher: ki-1, ki-2, the four error blocks, ex-1.

## Sources

- BC-CON-08016; BC-SKL-08036, BC-SKL-08037, BC-SKL-08038, BC-SKL-08039; BC-EK-CHA-5B2, BC-EK-CHA-5B3; ced:159
- BC-QA-08011; BC-PT-99001, BC-PT-99004
- BC-ERR-08030, BC-ERR-08033, BC-ERR-08034, BC-ERR-06013; BC-MIS-08017, BC-MIS-08018, BC-MIS-08019
- BC-PRQ-06002, BC-PRQ-06007, BC-PRQ-08005
- research/units/unit-08-applications-integration.md#8.8 Volumes with Cross Sections: Triangles and Semicircles
- research/question-analysis/question-archetypes.md#BC-QA-08011 Volume of a solid with known cross sections
- research/scoring/common-point-losses.md#Setup points
- research/exam/exam-structure.md#Section and part layout
- [inferred] Part A for an either archetype; ex-1's answer point untagged; the key idea figures; BC-ERR-08032 past the cap. Each settled as the machine record's inferred array states.

## Machine record

```json
{
 "id": "LSN-CON-08016",
 "kind": "concept",
 "target_id": "BC-CON-08016",
 "unit": "08",
 "skills": ["BC-SKL-08036", "BC-SKL-08037", "BC-SKL-08038", "BC-SKL-08039"],
 "orientation": {
  "text": "The distance between the curves goes into a different area formula for each named shape. A response writes that area, constant included, then integrates it over the base.",
  "sources": ["BC-CON-08016", "research/units/unit-08-applications-integration.md#8.8 Volumes with Cross Sections: Triangles and Semicircles"]
 },
 "key_ideas": [
  {
   "id": "ki-1",
   "ek_id": "BC-EK-CHA-5B2",
   "depth": "core",
   "text": "Triangles, distance s: equilateral area s^2 sqrt(3)/4; right isosceles s^2/2 when s is a leg, s^2/4 when s is the hypotenuse.",
   "notation": "area formulas for triangles and semicircles",
   "quote": {"text": "Volumes of solids with triangular cross sections can be found using definite integrals and the area formulas for these shapes.", "source": "ced:159"},
   "sources": ["BC-EK-CHA-5B2", "ced:159", "research/units/unit-08-applications-integration.md#8.8 Volumes with Cross Sections: Triangles and Semicircles"]
  },
  {
   "id": "ki-2",
   "ek_id": "BC-EK-CHA-5B3",
   "depth": "core",
   "text": "Semicircle, diameter in the base: radius s/2, area pi s^2/8.",
   "notation": "",
   "quote": null,
   "sources": ["BC-EK-CHA-5B3", "ced:159", "research/units/unit-08-applications-integration.md#8.8 Volumes with Cross Sections: Triangles and Semicircles"]
  }
 ],
 "strategy": [
  {
   "id": "st-1",
   "archetype_id": "BC-QA-08011",
   "cue": "A named shape; the stem says which part lies in the base.",
   "method": "Put the distance into that shape's area formula.",
   "rival": "Full circle area, or the distance as radius.",
   "separating_feature": "The phrase fixing the distance's role.",
   "sources": ["BC-QA-08011"],
   "evidence_tag": "verified"
  }
 ],
 "worked_examples": [
  {
   "id": "ex-1",
   "archetype_id": "BC-QA-08011",
   "bands": ["low", "mid"],
   "parameter_draw": {"shape": "semicircle", "tool": "by_hand", "left": 1, "width": 2, "bulge": 1, "slope": 0, "intercept": 1, "height_ratio": 2, "peak": 3, "spread": 2, "drop": "1", "reach": "2", "presentation": "formula"},
   "problem": {"text": "R lies between f(x) = 1 + (x - 1)(3 - x) and g(x) = 1. Cross sections perpendicular to the x-axis are semicircles with diameters in R. Find the volume.", "command_verb": "find"},
   "calculator_status": "no_calculator",
   "steps": [
    {"cue": "Diameter spans g to f.", "why": "Upper minus lower.", "expr": "(x - 1)*(3 - x)", "relation": "new"},
    {"cue": "Diameters in the base.", "why": "Radius is half.", "expr": "(x - 1)*(3 - x)/2", "relation": "new"},
    {"cue": "Half a circle.", "why": "pi s^2/8.", "expr": "pi*(x - 1)**2*(3 - x)**2/8", "relation": "new"},
    {"cue": "Curves meet at 1 and 3.", "why": "Limits.", "expr": "Integral(pi*(x - 1)**2*(3 - x)**2/8, (x, 1, 3))", "relation": "new", "point_type_id": "BC-PT-99001"},
    {"cue": "Integrate.", "why": "Exact.", "expr": "2*pi/15", "relation": "equivalent"}
   ],
   "answer": {"form": "symbolic", "expr": "2*pi/15"}
  },
  {
   "id": "ex-2",
   "archetype_id": "BC-QA-08011",
   "bands": ["low"],
   "parameter_draw": {"shape": "hypotenuse", "tool": "by_hand", "left": 0, "width": 2, "bulge": 2, "slope": -1, "intercept": 2, "height_ratio": 2, "peak": 3, "spread": 2, "drop": "1", "reach": "2", "presentation": "formula"},
   "problem": {"text": "R lies between f(x) = 2 - x + 2x(2 - x) and g(x) = 2 - x. Cross sections perpendicular to the x-axis are isosceles right triangles with hypotenuses in R. Find the volume.", "command_verb": "find"},
   "calculator_status": "no_calculator",
   "steps": [
    {"cue": "Hypotenuse spans g to f.", "why": "Upper minus lower.", "expr": "2*x*(2 - x)", "relation": "new"},
    {"cue": "Hypotenuse, not leg.", "why": "Area a quarter of its square.", "expr": "x**2*(2 - x)**2", "relation": "new"},
    {"cue": "Curves meet at 0 and 2.", "why": "Limits.", "expr": "Integral(x**2*(2 - x)**2, (x, 0, 2))", "relation": "new", "point_type_id": "BC-PT-99001"},
    {"cue": "Integrate.", "why": "Exact.", "expr": "16/15", "relation": "equivalent", "point_type_id": "BC-PT-99004"}
   ],
   "answer": {"form": "numeric", "expr": "16/15"}
  }
 ],
 "what_a_reader_scores": [
  {"example_id": "ex-1", "point_type_ids": ["BC-PT-99001"], "lines": [
   {"point_type_id": "BC-PT-99001", "text": "Definite integral expression with correct limits. Earned by: A definite integral whose limits match the requested interval and whose integrand matches the requested quantity, with or without the differential (sg-26:4, sg-22:2). Not earned by: An unsupported numerical value, or a definite integral whose bounds are wrong (sg-22:18). Notation: Differential may be omitted; sg-22:2 accepts dx written for dt. sg-23:8 treats a missing differential as recoverable for this point but restricts later eligibility."}
  ]},
  {"example_id": "ex-2", "point_type_ids": ["BC-PT-99001", "BC-PT-99004"], "lines": [
   {"point_type_id": "BC-PT-99001", "text": "Definite integral expression with correct limits. Earned by: A definite integral whose limits match the requested interval and whose integrand matches the requested quantity, with or without the differential (sg-26:4, sg-22:2). Not earned by: An unsupported numerical value, or a definite integral whose bounds are wrong (sg-22:18). Notation: Differential may be omitted; sg-22:2 accepts dx written for dt. sg-23:8 treats a missing differential as recoverable for this point but restricts later eligibility."},
   {"point_type_id": "BC-PT-99004", "text": "Answer with or without supporting work. Earned by: The correct value on its own, with no supporting work required (sg-25:3, sg-26:4). Not earned by: A value outside the accepted precision, or a value inconsistent with a required earlier step where the rubric imposes one. Precision: A reported decimal answer must be accurate to three places after the decimal point, rounded or truncated; at most one point per question is lost to inappropriate rounding (sg-25:2, sg-26:2). sg-26:4 also accepts a stated rounding to the nearest integer and several truncations."}
  ]}
 ],
 "common_errors": [
  {
   "error_id": "BC-ERR-08030",
   "observed_behavior": "A washer integrand is written as the square of the difference of the two radii, or a squared difference is expanded term by term.",
   "scoring_consequence": "The setup point is lost, and the value is wrong by the cross term.",
   "wrong_step": {"text": "f^2 - g^2.", "expr": "Integral(pi*((1 + (x - 1)*(3 - x))**2 - 1)/8, (x, 1, 3))"},
   "right_step": {"text": "(f - g)^2.", "expr": "Integral(pi*(x - 1)**2*(3 - x)**2/8, (x, 1, 3))"},
   "relation": "distinct",
   "possible_reason": {"misconception_id": "BC-MIS-08017", "text": "treats squaring as distributing over subtraction"},
   "sources": ["BC-ERR-08030", "BC-MIS-08017"]
  },
  {
   "error_id": "BC-ERR-08033",
   "observed_behavior": "A right isosceles section is given the leg formula although the stated distance is the hypotenuse.",
   "scoring_consequence": "The integrand is off by a factor of two, so the setup point is lost.",
   "wrong_step": {"text": "s^2/2.", "expr": "(x - 1)**2*(3 - x)**2/2"},
   "right_step": {"text": "s^2/4.", "expr": "(x - 1)**2*(3 - x)**2/4"},
   "relation": "distinct",
   "possible_reason": {"misconception_id": "BC-MIS-08019", "text": "remembers the squared dimension but not the fraction in front of it"},
   "sources": ["BC-ERR-08033", "BC-MIS-08019"]
  },
  {
   "error_id": "BC-ERR-08034",
   "observed_behavior": "The semicircular section is given a radius equal to the whole distance between the boundary curves.",
   "scoring_consequence": "The volume is four times too large and the setup point is lost.",
   "wrong_step": {"text": "Radius s.", "expr": "Integral(pi*(x - 1)**2*(3 - x)**2/2, (x, 1, 3))"},
   "right_step": {"text": "Radius s/2.", "expr": "Integral(pi*(x - 1)**2*(3 - x)**2/8, (x, 1, 3))"},
   "relation": "distinct",
   "possible_reason": {"misconception_id": "BC-MIS-08018", "text": "substitutes the distance between the boundary curves into every circular formula without asking whether it is a radius or a diameter"},
   "sources": ["BC-ERR-08034", "BC-MIS-08018"]
  },
  {
   "error_id": "BC-ERR-06013",
   "observed_behavior": "The area of a semicircular piece of the region is computed as pi times the radius squared.",
   "scoring_consequence": "The value point for that integral is lost.",
   "wrong_step": {"text": "Full circle.", "expr": "Integral(pi*(x - 1)**2*(3 - x)**2/4, (x, 1, 3))"},
   "right_step": {"text": "Half circle.", "expr": "Integral(pi*(x - 1)**2*(3 - x)**2/8, (x, 1, 3))"},
   "relation": "distinct",
   "possible_reason": {"misconception_id": "BC-MIS-08019", "text": "semicircular sections lose their constants"},
   "sources": ["BC-ERR-06013", "BC-MIS-08019"]
  }
 ],
 "representations": null,
 "prerequisite_bridges": [
  {"prq_id": "BC-PRQ-06002", "text": "Rewrite radicals and reciprocals as powers before antidifferentiating."},
  {"prq_id": "BC-PRQ-06007", "text": "A semicircle is half a circle's area, not the full area."},
  {"prq_id": "BC-PRQ-08005", "text": "Right isosceles area from a leg or the hypotenuse; not base times base."}
 ],
 "time": {"exam_part": "I-A", "budget_minutes": 2.14, "source": "research/exam/exam-structure.md#Section and part layout", "written_steps": {"ex-1": [3, 4, 5]}, "skipped_steps": {"ex-1": [1, 2]}},
 "checks": [
  {
   "id": "chk-1",
   "check_kind": "completion",
   "format": "short_answer",
   "bands": ["low", "mid"],
   "archetype_id": "BC-QA-08011",
   "parameter_draw": {"shape": "semicircle", "tool": "by_hand", "left": 1, "width": 2, "bulge": 1, "slope": 0, "intercept": 1, "height_ratio": 2, "peak": 3, "spread": 2, "drop": "1", "reach": "2", "presentation": "formula"},
   "completes": "ex-1",
   "stem": {"text": "Evaluate (pi/8) times the integral of (x - 1)^2 (3 - x)^2 from 1 to 3.", "command_verb": "evaluate"},
   "key": {"form": "symbolic", "expr": "2*pi/15"},
   "steps": [
    {"text": "The integral.", "expr": "Integral(pi*(x - 1)**2*(3 - x)**2/8, (x, 1, 3))", "relation": "new"},
    {"text": "u = x - 2.", "expr": "Integral(pi*(1 - x**2)**2/8, (x, -1, 1))", "relation": "equivalent"},
    {"text": "Value.", "expr": "2*pi/15", "relation": "equivalent"}
   ],
   "calculator_status": "no_calculator",
   "skills": ["BC-SKL-08039"]
  },
  {
   "id": "chk-2",
   "check_kind": "isomorph",
   "format": "short_answer",
   "bands": ["low", "mid"],
   "archetype_id": "BC-QA-08011",
   "parameter_draw": {"shape": "equilateral", "tool": "by_hand", "left": -1, "width": 2, "bulge": 1, "slope": 1, "intercept": 2, "height_ratio": 2, "peak": 3, "spread": 2, "drop": "1", "reach": "2", "presentation": "formula"},
   "stem": {"text": "R lies between f(x) = x + 2 + (x + 1)(1 - x) and g(x) = x + 2. Sections perpendicular to the x-axis are equilateral triangles. Find the volume.", "command_verb": "find"},
   "key": {"form": "symbolic", "expr": "4*sqrt(3)/15"},
   "steps": [
    {"text": "Side.", "expr": "1 - x**2", "relation": "new"},
    {"text": "Area.", "expr": "sqrt(3)*(1 - x**2)**2/4", "relation": "new"},
    {"text": "Limits -1 and 1.", "expr": "Integral(sqrt(3)*(1 - x**2)**2/4, (x, -1, 1))", "relation": "new"},
    {"text": "Value.", "expr": "4*sqrt(3)/15", "relation": "equivalent"}
   ],
   "calculator_status": "no_calculator",
   "skills": ["BC-SKL-08036"]
  },
  {
   "id": "chk-3",
   "check_kind": "mcq",
   "format": "mcq",
   "bands": ["low"],
   "archetype_id": "BC-QA-08011",
   "parameter_draw": {"shape": "semicircle", "tool": "by_hand", "left": 0, "width": 3, "bulge": 1, "slope": 0, "intercept": -1, "height_ratio": 2, "peak": 3, "spread": 2, "drop": "1", "reach": "2", "presentation": "formula"},
   "stem": {"text": "R lies between f(x) = -1 + x(3 - x) and g(x) = -1. Sections perpendicular to the x-axis are semicircles with diameters in R. The volume is", "command_verb": "identify"},
   "key": {"form": "symbolic", "expr": "81*pi/80"},
   "steps": [
    {"text": "Diameter x(3 - x); area pi/8 times its square.", "expr": "pi*x**2*(3 - x)**2/8", "relation": "new"},
    {"text": "Limits 0 and 3.", "expr": "Integral(pi*x**2*(3 - x)**2/8, (x, 0, 3))", "relation": "new"},
    {"text": "Value.", "expr": "81*pi/80", "relation": "equivalent"}
   ],
   "options": [
    {"id": "A", "is_key": false, "expr": "81*pi/20", "error_path": "BC-ERR-08034", "derivation": "the distance used as the radius"},
    {"id": "B", "is_key": true, "expr": "81*pi/80", "error_path": null},
    {"id": "C", "is_key": false, "expr": "81*pi/40", "error_path": "BC-ERR-06013", "derivation": "a full circle on the half distance"},
    {"id": "D", "is_key": false, "expr": "-9*pi/80", "error_path": "BC-ERR-08030", "derivation": "pi/8 times f squared minus g squared"}
   ],
   "calculator_status": "no_calculator",
   "skills": ["BC-SKL-08038"]
  }
 ],
 "delivery": [
  {"block": "orientation", "mode": "text", "reason": "rule 6: a statement of what a response shows", "sources": ["BC-CON-08016"]},
  {"block": "ki-1", "mode": "figure", "reason": "rule 4: BC-REP-08 on BC-SKL-08036 and BC-SKL-08037; not promoted, the BC-QA-08011 difficulty_variables vary a category", "sources": ["BC-SKL-08036", "BC-SKL-08037"],
   "spec": {
    "kind": "slice_shapes",
    "representations": [
     "BC-REP-08"
    ],
    "panels": [
     {
      "distance_role": "side",
      "window": {
       "x": [
        -0.5,
        2.5
       ],
       "y": [
        -0.5,
        2.2
       ]
      },
      "segments": [
       {
        "from": [
         0,
         0
        ],
        "to": [
         2,
         0
        ]
       },
       {
        "from": [
         2,
         0
        ],
        "to": [
         1,
         1.732
        ]
       },
       {
        "from": [
         1,
         1.732
        ],
        "to": [
         0,
         0
        ]
       }
      ],
      "points": [
       [
        0,
        0
       ],
       [
        2,
        0
       ]
      ]
     },
     {
      "distance_role": "leg",
      "window": {
       "x": [
        -0.5,
        2.5
       ],
       "y": [
        -0.5,
        2.2
       ]
      },
      "segments": [
       {
        "from": [
         0,
         0
        ],
        "to": [
         2,
         0
        ]
       },
       {
        "from": [
         2,
         0
        ],
        "to": [
         0,
         2
        ]
       },
       {
        "from": [
         0,
         2
        ],
        "to": [
         0,
         0
        ]
       }
      ],
      "points": [
       [
        0,
        0
       ],
       [
        2,
        0
       ]
      ]
     },
     {
      "distance_role": "hypotenuse",
      "window": {
       "x": [
        -0.5,
        2.5
       ],
       "y": [
        -0.5,
        2.2
       ]
      },
      "segments": [
       {
        "from": [
         0,
         0
        ],
        "to": [
         2,
         0
        ]
       },
       {
        "from": [
         2,
         0
        ],
        "to": [
         1,
         1
        ]
       },
       {
        "from": [
         1,
         1
        ],
        "to": [
         0,
         0
        ]
       }
      ],
      "points": [
       [
        0,
        0
       ],
       [
        2,
        0
       ]
      ]
     }
    ],
    "labels": [
     {
      "text": "s = side: s^2 sqrt(3)/4",
      "placement": "inside"
     },
     {
      "text": "s = leg: s^2/2",
      "placement": "inside"
     },
     {
      "text": "s = hypotenuse: s^2/4",
      "placement": "inside"
     }
    ]
   },
   "fallback": "the same three panels as a static image with the three labels, and the formulas as text beneath", "keyboard": "none needed: the figure has no control"},
  {"block": "ki-2", "mode": "figure", "reason": "rule 4: BC-REP-08 on BC-SKL-08038", "sources": ["BC-SKL-08038"],
   "spec": {
    "kind": "slice_shapes",
    "representations": [
     "BC-REP-08"
    ],
    "panels": [
     {
      "distance_role": "diameter",
      "window": {
       "x": [
        -0.5,
        2.5
       ],
       "y": [
        -0.5,
        1.5
       ]
      },
      "curves": [
       {
        "type": "semicircle",
        "center": [
         1,
         0
        ],
        "radius": 1
       }
      ],
      "segments": [
       {
        "from": [
         0,
         0
        ],
        "to": [
         2,
         0
        ]
       },
       {
        "from": [
         1,
         0
        ],
        "to": [
         1,
         1
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
        0
       ]
      ]
     }
    ],
    "labels": [
     {
      "text": "s = diameter",
      "placement": "inside"
     },
     {
      "text": "r = s/2",
      "placement": "inside"
     },
     {
      "text": "area pi s^2/8",
      "placement": "inside"
     }
    ]
   },
   "fallback": "the semicircle as a static image with the three labels", "keyboard": "none needed: the figure has no control"},
  {"block": "ex-1", "mode": "step_reveal", "reason": "rule 1", "sources": []},
  {"block": "ex-2", "mode": "step_reveal", "reason": "rule 1", "sources": []},
  {"block": "err-BC-ERR-08030", "mode": "step_reveal", "reason": "rule 1", "sources": []},
  {"block": "err-BC-ERR-08033", "mode": "step_reveal", "reason": "rule 1", "sources": []},
  {"block": "err-BC-ERR-08034", "mode": "step_reveal", "reason": "rule 1", "sources": []},
  {"block": "err-BC-ERR-06013", "mode": "step_reveal", "reason": "rule 1", "sources": []}
 ],
 "refresher": ["ki-1", "ki-2", "err-BC-ERR-08030", "err-BC-ERR-08033", "err-BC-ERR-08034", "err-BC-ERR-06013", "ex-1"],
 "read_minutes": {"full": 5.1, "brief": 2.9},
 "word_count": {"full": 762, "brief": 425},
 "research_lines": [
  {"file": "research/units/unit-08-applications-integration.md", "line": "the radius is half that distance and the area is pi over eight times the square of the distance"}
 ],
 "inferred": [
  {"claim": "BC-QA-08011 is calculator status either, so the lesson takes Section I Part A and its 2.14 minute budget.", "settles": "Timing data on cross section items split by exam part."},
  {"claim": "ex-1's answer step earns BC-PT-99004 but is not tagged, because its reader line would take the brief band past 450 words; ex-2 carries the tag.", "settles": "A shorter BC-PT-99004 reader line or a brief cap that admits it."},
  {"claim": "The key ideas are served as static figures of the slice shapes.", "settles": "The modality A/B in the build plan: skip rate and time to first credited success by mode."},
  {"claim": "BC-ERR-08032 meets the skills but falls past the cap of four error blocks.", "settles": "A cap change in plan 15 or a severity reorder in the bundle."},
  {"claim": "The leg against hypotenuse error is shown on ex-1's distance, as a slice area, since ex-1's shape is a semicircle.", "settles": "An author review of whether the error block may move to ex-2's hypotenuse draw."}
 ],
 "sources": ["BC-CON-08016", "BC-SKL-08036", "BC-SKL-08037", "BC-SKL-08038", "BC-SKL-08039", "BC-EK-CHA-5B2", "BC-EK-CHA-5B3", "ced:159", "BC-QA-08011", "BC-PT-99001", "BC-PT-99004", "BC-ERR-08030", "BC-ERR-08033", "BC-ERR-08034", "BC-ERR-06013", "BC-MIS-08017", "BC-MIS-08018", "BC-MIS-08019", "BC-PRQ-06002", "BC-PRQ-06007", "BC-PRQ-08005", "research/units/unit-08-applications-integration.md#8.8 Volumes with Cross Sections: Triangles and Semicircles", "research/question-analysis/question-archetypes.md#BC-QA-08011 Volume of a solid with known cross sections", "research/scoring/common-point-losses.md#Setup points", "research/exam/exam-structure.md#Section and part layout"]
}
```
