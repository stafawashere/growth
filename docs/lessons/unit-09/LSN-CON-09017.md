---
title: LSN-CON-09017 Intersection angles of two polar curves
research_date: 2026-09-29
status: designed
purpose: Authoring spec for the concept lesson on BC-CON-09017, the angles at which two polar curves meet, found by setting the radius functions equal on the stated interval and used as the limits of a polar area, built from authoring_bundle("BC-CON-09017") and the research files it cites, so an author fills plan 15's lesson record without making a teaching decision.
---

# LSN-CON-09017 Intersection angles of two polar curves

Concept BC-CON-09017 (skill BC-SKL-09039), topic 9.9 of Unit 9, BC only (ced:179), loaded by one archetype, BC-QA-09013 (family polar-area). It has no Unit 9 hard parent and precedes BC-CON-09016, because BC-SKL-09039 is a hard parent of BC-SKL-09041 (docs/lessons/unit-09/README.md, section 1). BC-SKL-08018 (outside hard parent) and the two BC-PRQ parents assume that an equation setting two expressions equal is solved on an interval.

## Prediction

Served first, both bands: an `mcq` on ex-1's own curves, \(r=2+2\cos\theta\) and \(r=3\), asking which condition gives the angles where the curves meet. Key A, \(2+2\cos\theta=3\). Distractors: B, \(2+2\cos\theta=0\), where the limacon reaches the pole, and C, the ends \(-\pi\) and \(\pi\) of the interval, the limits BC-MIS-09019 names. Only A is true. It is answerable before the rule from the geometry of two curves meeting at one angle. The resolution states the condition and the two angles, with no verdict. Source: BC-CON-09017 and the topic section the key idea cites.

## Orientation

Served text, from BC-CON-09017 `description_plain` ("the curves meet where their radii agree at the same angle") and the topic's Assessment behaviour paragraph (research/units/unit-09-parametric-polar-vector.md#9.9 Finding the Area of the Region Bounded by Two Polar Curves): the FRQ scores the limits in the answer point, and calculator variants find the angles numerically and store them. The orientation states what a response shows: the equation, every solution, and the pair that bounds the region. No count, no frequency.

## Key ideas

The skill maps to one essential knowledge statement, BC-EK-CHA-5D2 (ced:179): one core block, both bands.

- ki-1 (core). Paraphrase of the Required mathematical knowledge paragraph Intersection angles (limits found by setting the two radius functions equal on the interval, assessed in the answer point, sg-25:7) and of the concept's `description_formal`. Notation line, the concept's `notation`: "intersection angles". No anchor quote: the CHA-5.D.2 sentence on ced:179 states area by definite integrals, not the limits, so it costs words and adds nothing here.

## Recognition

BC-QA-09013 (research/question-analysis/question-archetypes.md#BC-QA-09013 Area inside one polar curve and outside another) is the only archetype loading BC-SKL-09039.

- `common_givens`: "two polar equations" and "a figure". `asked_to_produce`: "intersection angles", "an area integral", "a numerical area". `typical_wording`: "find the area of the region that lies inside one curve and outside the other, and show the setup for the calculations".
- The signal in the stem: two polar equations and a region described by both. The limits are not stated; the intersections dial (`found`) leaves them to the response. `difficulty_variables`: whether one curve is a circle, whether the angles are exact or decimal, whether the outer curve changes.
- Shapes: an MCQ asking which integral gives the area inside one curve and outside another (BC-MCQ-PE2012-044); the calculator FRQ part, BC-FRQ-2013-Q2-A, BC-FRQ-2014-Q2-A, BC-FRQ-2025-Q2-B, and the no calculator BC-FRQ-2018-Q5-A.

The near miss of the contrast pair is the area enclosed by one of the same curves, a stem of BC-QA-09012 (the single curve archetype), where a stated interval or the zeros of r supply the limits and no second curve exists. The `wrong_approaches` entry "using the full angle interval instead of the intersection angles" is the mistake the near miss invites. What says "not this concept": one curve and stated rays (BC-CON-09015); a region described by the difference of two radii at one angle (BC-QA-99006).

## Method choice

- st-1, BC-QA-09013. Cue from `common_givens` and `asked_to_produce`. Method, `expected_solution_path[0]` "set the two radii equal and solve for the bounding angles". Rival, `wrong_approaches`: the angle range of the figure as the limits. Separating feature: the curves meet where the radii agree, not where the figure is drawn. Both cue fields exist, so the block is not inferred. No served field opens with the reader's own label. The block carries the contrast pair, an area between two curves beside an area of one curve, with the feature that separates them.

## Solution path

- ex-1, BC-QA-09013, both bands, no calculator. Draw: constant 2, coefficient 2, circle 3, orientation right, intersections found; \(r=2+2\cos\theta\) against \(r=3\) on \(-\pi\le\theta\le\pi\). Chain: the equation (`new`), the cosine isolated (`equivalent`), the two angles \(\pm\pi/3\) (`solve`). No published item on BC-QA-09013 carries this draw (content/items_gen_unit09/ITM-GEN-09013-00 to 21).
- ex-2, low band, calculator, faded from step 3. Draw: constant 2, coefficient 3, circle 3, orientation left, intersections found; \(r=2-3\cos\theta\), \(\cos\theta=-1/3\), \(\alpha=\arccos(-1/3)=1.9106\), reported 1.911. Steps 1 and 2 (the equation and the isolated cosine) are shown, the student writes \(\alpha\), then steps 3 and 4 reveal. The fade falls there because the setup repeats ex-1 and the sign of the cosine, which puts \(\alpha\) past \(\pi/2\), is what the student must decide.
- A fluent solver writes the equation set equal and the solutions; the isolation of the cosine is held. No productive-failure target: BC-CON-09015 is the unit's target.

## Scoring

BC-QA-09013 lists BC-PT-99048, 99001, 99004, 99002. Neither example ends in an integral or an area, so no step carries a tag and both scoring entries are empty. The angles are assessed inside the answer point: sg-25:7 assesses the limits and the factor one half there, not in the integrand points (research/scoring/common-point-losses.md#Setup points). BC-ERR-09037 records the consequence: the answer point is lost when the limits are not the intersection angles. The polar area concepts (BC-CON-09015, BC-CON-09016) carry the scoring lines.

## Traps

Two errors meet BC-SKL-09039: BC-ERR-09037 and BC-ERR-09038, in the bundle's order; both highest linked severity high. Low band both, mid band both. Both on ex-1's draw, both `fix_prompt` true, since each pair is distinct.

- err-BC-ERR-09037: limits \(-\pi\) and \(\pi\), the ends of the interval, against the intersection angles \(\pm\pi/3\). Possible reason, BC-MIS-09019.
- err-BC-ERR-09038: only \(\pi/3\) found, against both angles. The record links BC-MIS-09019 and BC-MIS-09007, whose descriptions do not describe a missed solution, so no possible reason.
- Check 3 needs three distractors and only two errors exist. It uses BC-ERR-09038 twice, once for each single solution, and BC-ERR-09037 once. Reported under gaps.

## Representations

None as a separate block. The topic's Representations paragraph names a plotted pair of polar curves converted to intersection angles (BC-REP-02 to BC-REP-09); the unit README delivers it as a figure on the orientation and the key idea (docs/lessons/unit-09/README.md, section 6), so a `representations` block would repeat it.

## Prerequisite bridge

- BC-PRQ-08001 and BC-PRQ-09002, each from its `description_plain` and `failure_signature`.

## Time

ex-1 lives in the Section I Part B calculator shape of BC-QA-09013 (I-B, 2.92 minutes, research/exam/exam-structure.md#Section and part layout); as a free response part the archetype is 3 points, 5.0 minutes (docs/lessons/unit-09/README.md, section 5). A fluent solver writes the equation and its solutions; the isolation of the cosine and the calculator solve keystrokes are held [inferred].

## Checks

- chk-1, completion of ex-1, both bands: the equation \(2\cos\theta=1\) is given and the angles asked. Key \(\{-\pi/3,\pi/3\}\).
- chk-2, isomorph, both bands, no calculator. Draw: constant 3, coefficient 2, circle 4, orientation up, intersections found; \(r=3+2\sin\theta\) against \(r=4\) on \(0\le\theta\le\pi\). Key \(\{\pi/6,5\pi/6\}\).
- chk-3, MCQ, low band, no calculator. Draw: constant 4, coefficient 2, circle 5, orientation down, intersections found; \(r=4-2\sin\theta\) against \(r=5\) on \(-\pi\le\theta\le0\). Key \(\{-5\pi/6,-\pi/6\}\). Distractors: \(\{-\pi/6\}\) and \(\{-5\pi/6\}\) (BC-ERR-09038, one solution each), \(\{-\pi,0\}\) (BC-ERR-09037, the ends of the drawn interval).

## Delivery

- orientation, ki-1: figure. Rule 4 (README rule 3): BC-REP-13 and BC-REP-09 on BC-SKL-09039; not promoted, the stem asks for angles found by solving. The orientation draws the two curves; ki-1 adds the two intersection rays (docs/lessons/unit-09/README.md, section 6).
- ex-1, ex-2, the two error blocks: step_reveal. Rule 1.

## Band plan

- Low (full): prediction, orientation, bridges, ki-1, st-1 with the contrast pair, ex-1, chk-1, the two error blocks, ex-2 (faded from step 3), chk-2, chk-3. 494 words, 3.3 minutes.
- Mid (brief): prediction, orientation, bridges, ki-1, st-1 with the contrast pair, ex-1, chk-1, the two error blocks, chk-2. 409 words, 2.8 minutes.
- Refresher: ki-1, the two error blocks, ex-1.

## Sources

- BC-CON-09017; BC-SKL-09039; BC-EK-CHA-5D2; ced:179
- BC-QA-09013; BC-FRQ-2013-Q2-A, BC-FRQ-2014-Q2-A, BC-FRQ-2025-Q2-B, BC-FRQ-2018-Q5-A, BC-MCQ-PE2012-044
- BC-ERR-09037, BC-ERR-09038; BC-MIS-09019
- BC-PRQ-08001, BC-PRQ-09002
- sg-25:7
- research/units/unit-09-parametric-polar-vector.md#9.9 Finding the Area of the Region Bounded by Two Polar Curves
- research/question-analysis/question-archetypes.md#BC-QA-09013 Area inside one polar curve and outside another
- research/scoring/common-point-losses.md#Setup points
- research/exam/exam-structure.md#Section and part layout
- [inferred] The held steps; the limacon orientation reading; the two figure entries. Each settled as the inferred array states.

## Machine record

```json
{
 "id": "LSN-CON-09017",
 "kind": "concept",
 "target_id": "BC-CON-09017",
 "unit": "09",
 "skills": [
  "BC-SKL-09039"
 ],
 "prediction": {
  "id": "pr-1",
  "stem": {
   "text": "The curves \\(r=2+2\\cos\\theta\\) and \\(r=3\\) bound a region for \\(-\\pi\\le\\theta\\le\\pi\\). Predict which condition gives the angles where the curves meet.",
   "command_verb": "predict"
  },
  "format": "mcq",
  "options": [
   {
    "id": "A",
    "label": "\\(2+2\\cos\\theta=3\\)",
    "is_key": true
   },
   {
    "id": "B",
    "label": "\\(2+2\\cos\\theta=0\\)",
    "is_key": false
   },
   {
    "id": "C",
    "label": "\\(\\theta=-\\pi\\) and \\(\\theta=\\pi\\)",
    "is_key": false
   }
  ],
  "resolution": "The curves meet where both radii are equal at one angle, so \\(2+2\\cos\\theta=3\\), which gives \\(\\theta=\\pm\\pi/3\\).",
  "sources": [
   "BC-CON-09017",
   "research/units/unit-09-parametric-polar-vector.md#9.9 Finding the Area of the Region Bounded by Two Polar Curves"
  ]
 },
 "orientation": {
  "text": "The curves meet where \\(r_1(\\theta)=r_2(\\theta)\\) on the stated interval. A response solves that equation, keeps every solution, and takes the two that bound the region as limits.",
  "sources": [
   "BC-CON-09017",
   "research/units/unit-09-parametric-polar-vector.md#9.9 Finding the Area of the Region Bounded by Two Polar Curves"
  ]
 },
 "key_ideas": [
  {
   "id": "ki-1",
   "ek_id": "BC-EK-CHA-5D2",
   "depth": "core",
   "text": "The limits of a polar area between two curves are the angles where the radius functions are equal. Set them equal on the stated interval, solve for every solution, and select the pair that bounds the region. The angle range in which the figure is drawn does not supply the limits.",
   "notation": "intersection angles",
   "quote": null,
   "sources": [
    "BC-EK-CHA-5D2",
    "ced:179",
    "sg-25:7",
    "research/units/unit-09-parametric-polar-vector.md#9.9 Finding the Area of the Region Bounded by Two Polar Curves"
   ]
  }
 ],
 "strategy": [
  {
   "id": "st-1",
   "archetype_id": "BC-QA-09013",
   "cue": "Two polar equations, a region between them, limits not given.",
   "method": "\\(r_1(\\theta)=r_2(\\theta)\\), solved on the stated interval for every angle.",
   "rival": "The angle range of the figure as the limits.",
   "separating_feature": "Where the curves meet, not where the figure is drawn.",
   "sources": [
    "BC-QA-09013"
   ],
   "evidence_tag": "verified",
   "contrast": {
    "this": {
     "text": "Find the area of the region inside \\(r=2+2\\cos\\theta\\) and outside \\(r=3\\).",
     "archetype_id": "BC-QA-09013"
    },
    "not_this": {
     "text": "Find the area of the region enclosed by \\(r=2+2\\cos\\theta\\) for \\(-\\pi\\le\\theta\\le\\pi\\).",
     "why_not": "One curve and a stated interval bound it, so nothing is intersected."
    },
    "feature": "A second curve bounds the region, so the limits are where the radii agree."
   }
  }
 ],
 "worked_examples": [
  {
   "id": "ex-1",
   "archetype_id": "BC-QA-09013",
   "bands": [
    "low",
    "mid"
   ],
   "parameter_draw": {
    "constant": "2",
    "coefficient": "2",
    "circle": "3",
    "orientation": "right",
    "intersections": "found"
   },
   "problem": {
    "text": "The curves \\(r=2+2\\cos\\theta\\) and \\(r=3\\) bound a region. For \\(-\\pi\\le\\theta\\le\\pi\\), find the angles at which the curves meet.",
    "command_verb": "find"
   },
   "calculator_status": "no_calculator",
   "steps": [
    {
     "cue": "The curves meet where the radii agree.",
     "why": "Equal radii at one angle.",
     "expr": "2 + 2*cos(theta) = 3",
     "relation": "new"
    },
    {
     "cue": "Isolate the cosine.",
     "why": "Subtract 2 from both sides.",
     "expr": "2*cos(theta) = 1",
     "relation": "equivalent"
    },
    {
     "cue": "Solve on \\(-\\pi\\) to \\(\\pi\\).",
     "why": "Cosine is even, so both signs.",
     "expr": "FiniteSet(-pi/3, pi/3)",
     "relation": "solve",
     "variable": "theta"
    }
   ],
   "answer": {
    "form": "symbolic",
    "expr": "FiniteSet(-pi/3, pi/3)"
   }
  },
  {
   "id": "ex-2",
   "archetype_id": "BC-QA-09013",
   "bands": [
    "low"
   ],
   "fade_from": 3,
   "parameter_draw": {
    "constant": "2",
    "coefficient": "3",
    "circle": "3",
    "orientation": "left",
    "intersections": "found"
   },
   "problem": {
    "text": "The curves \\(r=2-3\\cos\\theta\\) and \\(r=3\\) meet at \\(\\theta=-\\alpha\\) and \\(\\theta=\\alpha\\), with \\(0<\\alpha<\\pi\\). Using a calculator, find \\(\\alpha\\).",
    "command_verb": "find"
   },
   "calculator_status": "calculator",
   "steps": [
    {
     "cue": "Set the radii equal.",
     "why": "Meeting angles satisfy this.",
     "expr": "2 - 3*cos(theta) = 3",
     "relation": "new"
    },
    {
     "cue": "Isolate the cosine term.",
     "why": "Subtract 2 from both sides.",
     "expr": "-3*cos(theta) = 1",
     "relation": "equivalent"
    },
    {
     "cue": "Solve for the positive angle.",
     "why": "The cosine is negative, so \\(\\alpha\\) is past \\(\\pi/2\\).",
     "expr": "acos(-1/3)",
     "relation": "solve",
     "variable": "theta"
    },
    {
     "cue": "Keep the exact angle until the last line.",
     "why": "Three places, no earlier rounding.",
     "expr": "1.911",
     "relation": "evaluate",
     "subs": {},
     "approx": true
    }
   ],
   "answer": {
    "form": "numeric",
    "expr": "1.911"
   }
  }
 ],
 "what_a_reader_scores": [
  {
   "example_id": "ex-1",
   "point_type_ids": [],
   "lines": []
  },
  {
   "example_id": "ex-2",
   "point_type_ids": [],
   "lines": []
  }
 ],
 "common_errors": [
  {
   "error_id": "BC-ERR-09037",
   "observed_behavior": "The area integral runs over the angle interval of the figure rather than between the intersection angles of the two curves.",
   "scoring_consequence": "The answer point is lost, since the limits are assessed there (sg-25:7).",
   "wrong_step": {
    "text": "Limits \\(-\\pi\\) and \\(\\pi\\), the ends of the interval.",
    "expr": "FiniteSet(-pi, pi)"
   },
   "right_step": {
    "text": "Limits \\(-\\pi/3\\) and \\(\\pi/3\\), where the radii agree.",
    "expr": "FiniteSet(-pi/3, pi/3)"
   },
   "relation": "distinct",
   "fix_prompt": true,
   "possible_reason": {
    "misconception_id": "BC-MIS-09019",
    "text": "takes the angle range in which the picture is drawn as the limits instead of the angles where the curves meet"
   },
   "sources": [
    "BC-ERR-09037",
    "BC-MIS-09019"
   ]
  },
  {
   "error_id": "BC-ERR-09038",
   "observed_behavior": "Only one solution of the equation setting the radii equal is found, so the region is bounded incorrectly.",
   "scoring_consequence": "The limits are wrong and the answer point is lost.",
   "wrong_step": {
    "text": "Only \\(\\pi/3\\).",
    "expr": "FiniteSet(pi/3)"
   },
   "right_step": {
    "text": "Both \\(-\\pi/3\\) and \\(\\pi/3\\).",
    "expr": "FiniteSet(-pi/3, pi/3)"
   },
   "relation": "distinct",
   "fix_prompt": true,
   "possible_reason": null,
   "sources": [
    "BC-ERR-09038"
   ]
  }
 ],
 "representations": null,
 "prerequisite_bridges": [
  {
   "prq_id": "BC-PRQ-08001",
   "text": "Set two expressions equal and keep every solution in the interval."
  },
  {
   "prq_id": "BC-PRQ-09002",
   "text": "Solve the trigonometric equation on the stated interval, counting both signs."
  }
 ],
 "time": {
  "exam_part": "I-B",
  "budget_minutes": 2.92,
  "source": "research/exam/exam-structure.md#Section and part layout",
  "written_steps": {
   "ex-1": [
    1,
    3
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
   "archetype_id": "BC-QA-09013",
   "parameter_draw": {
    "constant": "2",
    "coefficient": "2",
    "circle": "3",
    "orientation": "right",
    "intersections": "found"
   },
   "completes": "ex-1",
   "stem": {
    "text": "\\(2\\cos\\theta=1\\) for \\(-\\pi\\le\\theta\\le\\pi\\). Write the angles where \\(r=2+2\\cos\\theta\\) meets \\(r=3\\).",
    "command_verb": "write"
   },
   "key": {
    "form": "symbolic",
    "expr": "FiniteSet(-pi/3, pi/3)"
   },
   "steps": [
    {
     "text": "Equation.",
     "expr": "2*cos(theta) = 1",
     "relation": "new"
    },
    {
     "text": "Solve.",
     "expr": "FiniteSet(-pi/3, pi/3)",
     "relation": "solve",
     "variable": "theta"
    }
   ],
   "calculator_status": "no_calculator",
   "skills": [
    "BC-SKL-09039"
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
   "archetype_id": "BC-QA-09013",
   "parameter_draw": {
    "constant": "3",
    "coefficient": "2",
    "circle": "4",
    "orientation": "up",
    "intersections": "found"
   },
   "stem": {
    "text": "The curves \\(r=3+2\\sin\\theta\\) and \\(r=4\\) bound a region for \\(0\\le\\theta\\le\\pi\\). Write the angles where they meet.",
    "command_verb": "write"
   },
   "key": {
    "form": "symbolic",
    "expr": "FiniteSet(pi/6, 5*pi/6)"
   },
   "steps": [
    {
     "text": "Radii equal.",
     "expr": "3 + 2*sin(theta) = 4",
     "relation": "new"
    },
    {
     "text": "Isolate.",
     "expr": "2*sin(theta) = 1",
     "relation": "equivalent"
    },
    {
     "text": "Solve.",
     "expr": "FiniteSet(pi/6, 5*pi/6)",
     "relation": "solve",
     "variable": "theta"
    }
   ],
   "calculator_status": "no_calculator",
   "skills": [
    "BC-SKL-09039"
   ]
  },
  {
   "id": "chk-3",
   "check_kind": "mcq",
   "format": "mcq",
   "bands": [
    "low"
   ],
   "archetype_id": "BC-QA-09013",
   "parameter_draw": {
    "constant": "4",
    "coefficient": "2",
    "circle": "5",
    "orientation": "down",
    "intersections": "found"
   },
   "stem": {
    "text": "The curves \\(r=4-2\\sin\\theta\\) and \\(r=5\\) are drawn for \\(-\\pi\\le\\theta\\le0\\). They meet at the angles",
    "command_verb": "identify"
   },
   "key": {
    "form": "symbolic",
    "expr": "FiniteSet(-5*pi/6, -pi/6)"
   },
   "steps": [
    {
     "text": "Radii equal.",
     "expr": "4 - 2*sin(theta) = 5",
     "relation": "new"
    },
    {
     "text": "Isolate.",
     "expr": "-2*sin(theta) = 1",
     "relation": "equivalent"
    },
    {
     "text": "Solve.",
     "expr": "FiniteSet(-5*pi/6, -pi/6)",
     "relation": "solve",
     "variable": "theta"
    }
   ],
   "options": [
    {
     "id": "A",
     "is_key": false,
     "label": "\\(-\\pi/6\\) only",
     "expr": "FiniteSet(-pi/6)",
     "error_path": "BC-ERR-09038",
     "derivation": "one solution of the equation, the second not found"
    },
    {
     "id": "B",
     "is_key": true,
     "label": "\\(-5\\pi/6\\) and \\(-\\pi/6\\)",
     "expr": "FiniteSet(-5*pi/6, -pi/6)",
     "error_path": null
    },
    {
     "id": "C",
     "is_key": false,
     "label": "\\(-\\pi\\) and \\(0\\)",
     "expr": "FiniteSet(-pi, 0)",
     "error_path": "BC-ERR-09037",
     "derivation": "the ends of the drawn interval"
    },
    {
     "id": "D",
     "is_key": false,
     "label": "\\(-5\\pi/6\\) only",
     "expr": "FiniteSet(-5*pi/6)",
     "error_path": "BC-ERR-09038",
     "derivation": "the other solution alone"
    }
   ],
   "calculator_status": "no_calculator",
   "skills": [
    "BC-SKL-09039"
   ]
  }
 ],
 "delivery": [
  {
   "block": "orientation",
   "mode": "figure",
   "reason": "rule 4: BC-REP-13 and BC-REP-09 on BC-SKL-09039; not promoted, the stem asks for angles found by solving, not a reading of a varying quantity",
   "sources": [
    "BC-SKL-09039"
   ],
   "spec": {
    "kind": "polar_curves",
    "representations": [
     "BC-REP-13",
     "BC-REP-02"
    ],
    "curves": [
     {
      "r": "2 + 2*cos(theta)",
      "domain": [
       "-pi",
       "pi"
      ]
     },
     {
      "r": "3",
      "domain": [
       "-pi",
       "pi"
      ]
     }
    ],
    "labels": [
     {
      "text": "r = 2 + 2cos θ",
      "placement": "inside"
     },
     {
      "text": "r = 3",
      "placement": "inside"
     },
     {
      "text": "O",
      "placement": "inside"
     }
    ]
   },
   "fallback": "the same two curves static, labelled inside",
   "keyboard": "no control; the figure description is reached with Tab"
  },
  {
   "block": "ki-1",
   "mode": "figure",
   "reason": "rule 4: the intersection rays drawn on the two curves show the limits as where the radii agree, not the ends of the figure",
   "sources": [
    "BC-SKL-09039"
   ],
   "spec": {
    "kind": "polar_curves",
    "representations": [
     "BC-REP-13",
     "BC-REP-02"
    ],
    "curves": [
     {
      "r": "2 + 2*cos(theta)",
      "domain": [
       "-pi",
       "pi"
      ]
     },
     {
      "r": "3",
      "domain": [
       "-pi",
       "pi"
      ]
     }
    ],
    "rays": [
     {
      "theta": "pi/3"
     },
     {
      "theta": "-pi/3"
     }
    ],
    "labels": [
     {
      "text": "θ = π/3",
      "placement": "inside"
     },
     {
      "text": "θ = -π/3",
      "placement": "inside"
     },
     {
      "text": "r = 3",
      "placement": "inside"
     },
     {
      "text": "r = 2 + 2cos θ",
      "placement": "inside"
     }
    ]
   },
   "fallback": "the same figure static with both rays drawn and labelled",
   "keyboard": "no control; the figure description is reached with Tab"
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
   "block": "err-BC-ERR-09037",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  },
  {
   "block": "err-BC-ERR-09038",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  }
 ],
 "refresher": [
  "ki-1",
  "err-BC-ERR-09037",
  "err-BC-ERR-09038",
  "ex-1"
 ],
 "research_lines": [
  {
   "file": "research/units/unit-09-parametric-polar-vector.md",
   "line": "The limits are found by setting the two radius functions equal on the interval"
  }
 ],
 "inferred": [
  {
   "claim": "A fluent solver writes the equation set equal and the solutions, and holds the isolation of the cosine.",
   "settles": "Per-step timing from the fluency telemetry."
  },
  {
   "claim": "The orientation and ki-1 both draw the two curves; the second adds the rays.",
   "settles": "The modality A/B in the build plan, skip rate and time to first credited success by mode."
  },
  {
   "claim": "Orientation of the limacon (right, up, left, down) is read as r = c + b cos, c + b sin, c - b cos, c - b sin.",
   "settles": "The app/generation/templates/qa_09013.py orientation table."
  }
 ],
 "sources": [
  "BC-CON-09017",
  "BC-SKL-09039",
  "BC-EK-CHA-5D2",
  "ced:179",
  "BC-QA-09013",
  "BC-ERR-09037",
  "BC-ERR-09038",
  "BC-MIS-09019",
  "BC-PRQ-08001",
  "BC-PRQ-09002",
  "sg-25:7",
  "BC-FRQ-2013-Q2-A",
  "BC-FRQ-2014-Q2-A",
  "BC-FRQ-2025-Q2-B",
  "BC-FRQ-2018-Q5-A",
  "BC-MCQ-PE2012-044",
  "research/units/unit-09-parametric-polar-vector.md#9.9 Finding the Area of the Region Bounded by Two Polar Curves",
  "research/question-analysis/question-archetypes.md#BC-QA-09013 Area inside one polar curve and outside another",
  "research/exam/exam-structure.md#Section and part layout"
 ],
 "word_count": {
  "full": 494,
  "brief": 409
 },
 "read_minutes": {
  "full": 3.3,
  "brief": 2.8
 }
}
```
