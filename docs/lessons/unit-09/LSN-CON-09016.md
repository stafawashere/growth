---
title: LSN-CON-09016 Area between two polar curves
research_date: 2026-09-29
status: designed
purpose: Authoring spec for the concept lesson on BC-CON-09016, the area between two polar curves as one half the integral of the outer radius squared minus the inner radius squared between the intersection angles, built from authoring_bundle("BC-CON-09016") and the research files it cites, so an author fills plan 15's lesson record without making a teaching decision.
---

# LSN-CON-09016 Area between two polar curves

Concept BC-CON-09016 (skills BC-SKL-09040, BC-SKL-09041, BC-SKL-09042, BC-SKL-09043), topic 9.9 of Unit 9, BC only (ced:179), loaded by one archetype, BC-QA-09013 (family polar-area). Hard parents in Unit 9: BC-CON-09015 and BC-CON-09017 (docs/lessons/unit-09/README.md, section 1); the intersection angles are found or given before this lesson's work starts. Outside hard parent BC-SKL-08018.

## Prediction

Served first, both bands: an `mcq` on ex-1's own curves at \(\theta=0\), radii 4 and 3, asking for the area of the thin slice between them for a small angle \(d\theta\). Key B, \(\tfrac12(4^2-3^2)\,d\theta\). Distractors: A the square of the difference (the BC-ERR-09040 form), C the difference of the radii alone, D half the product. Only B equals \(3.5\,d\theta\). It is answerable before the rule, because the area of a sector is \(\tfrac12r^2\) times its angle. The resolution states the two sectors and the general form, with no verdict. Source: BC-CON-09016 and the topic section the key idea cites.

## Orientation

Served text, from BC-CON-09016 `description_plain` ("subtract the squares of the two radii inside one half the integral") and the topic's Assessment behaviour paragraph (research/units/unit-09-parametric-polar-vector.md#9.9 Finding the Area of the Region Bounded by Two Polar Curves): a response squares each radius before subtracting and shows the limits and the factor one half, which the guideline assesses in the answer point. No count, no frequency.

## Key ideas

All four skills map to one essential knowledge statement, BC-EK-CHA-5D2 (ced:179): one core block, both bands.

- ki-1 (core). Paraphrase of the Required mathematical knowledge paragraphs Area between polar curves, Order of operations (squared before subtracted, as in the washer method) and Symmetry (an integral over half a symmetric region multiplied by two earns the same points, sg-25:8). The outer curve is the one with the larger radius (BC-SKL-09040 `description_plain`: test one angle). Notation line, the concept's `notation`. No anchor quote.

## Recognition

BC-QA-09013 (research/question-analysis/question-archetypes.md#BC-QA-09013 Area inside one polar curve and outside another) is the only archetype loading the four skills.

- `common_givens`: "two polar equations" and "a figure". `asked_to_produce`: "intersection angles", "an area integral", "a numerical area". `typical_wording`: "find the area of the region that lies inside one curve and outside the other, and show the setup for the calculations".
- The signal in the stem: a region described as inside one curve and outside another. `difficulty_variables`: a circle of constant radius, exact or decimal angles, an outer curve that changes inside the interval.
- Shapes: an MCQ, BC-MCQ-PE2012-044; the calculator FRQ part, BC-FRQ-2013-Q2-A, BC-FRQ-2014-Q2-A, BC-FRQ-2025-Q2-B, and the no calculator BC-FRQ-2018-Q5-A.

The near miss of the contrast pair is a stem of BC-QA-99006 (research/question-analysis/question-archetypes.md#BC-QA-99006 Rate of change with respect to theta of the gap between two polar curves): the same two curves on the same interval, asking how fast the gap between them changes. It subtracts the radii themselves, where area squares each radius before subtracting. What says "not this concept": one curve and stated rays (BC-CON-09015); "how far apart" or "rate of the distance" on one ray (BC-QA-99006).

## Method choice

- st-1, BC-QA-09013. Cue from `common_givens` and `asked_to_produce`. Method, `expected_solution_path[1]` and `[2]`: decide which curve is outer, then one half the integral of the difference of the squares. Rival, `wrong_approaches`: squaring the difference of the two radii. Separating feature: each radius is squared first, then the squares are subtracted. Both cue fields exist, so the block is not inferred. No served field opens with the reader's own label. The block carries the contrast pair.

## Solution path

- ex-1, BC-QA-09013, both bands, calculator. Draw: constant 2, coefficient 2, circle 3, orientation right, intersections given; \(r=2+2\cos\theta\) against \(r=3\), angles \(\pm\pi/3\). Chain: the integrand (`new`), the integral with limits (`new`), the value (`evaluate`, 4.653; SymPy 4.65264, exact \(\tfrac{9\sqrt3}{2}-\pi\)). No published item on BC-QA-09013 carries this draw (content/items_gen_unit09/ITM-GEN-09013-00 to 21).
- ex-2, low band, calculator, faded from step 3. Draw: constant 3, coefficient 2, circle 4, orientation up, intersections given; \(r=3+2\sin\theta\) against \(r=4\), angles \(\pi/6\) and \(5\pi/6\), symmetric about \(\theta=\pi/2\). Steps 1 and 2 (the outer curve, and the doubled half that leaves no fraction) are shown, the student writes the setup and the value, then steps 3 and 4 reveal. The fade falls there because the outer test and the integrand repeat ex-1, and the symmetry choice, the half region and the doubling, is what the student must decide. Value 6.022 (SymPy 6.02234).
- A fluent solver writes the integral with its limits and the value; the outer test is held. No productive-failure target: BC-CON-09015 is the unit's target.

## Scoring

BC-QA-09013 lists BC-PT-99048, 99001, 99004, 99002. ex-1 carries no tag and ex-2 tags BC-PT-99048 and BC-PT-99004: a scoring line costs 42 to 88 words and the brief band cannot carry one beside the prediction and the contrast pair. BC-PT-99001 and BC-PT-99002 are untagged for the same reason (inferred array). The lines are `reader_checks` output.

Point losses from research: the integrand point is lost when the square is missing, and later points in the part are typically unreachable (BC-ERR-99031; research/scoring/common-point-losses.md#Setup points, crabbc-25:29); the limits and the factor one half are assessed in the answer point (sg-25:7).

## Traps

Four errors meet the skills, in bundle order: BC-ERR-09035, 09039, 09040, 09041 (each linked to a high severity BC-MIS, then by id). BC-ERR-99031, 99002 and 99019 fall past the cap of 4. Low band all four, mid band the first two. All on ex-1's draw, all `fix_prompt` true, since each pair is distinct.

- err-BC-ERR-09035: the factor one half omitted. Possible reason, BC-MIS-08019.
- err-BC-ERR-09039: inner minus outer, giving \(-4.653\). No possible reason line: the record links BC-MIS-09018 and BC-MIS-09013, whose descriptions do not describe an exchange.
- err-BC-ERR-09040: \(\tfrac12(R-r)^2\). Possible reason, BC-MIS-09018.
- err-BC-ERR-09041: the half region from 0 to \(\pi/3\) not doubled, against the doubled half. No possible reason line: the linked BC-MIS-09018 and BC-MIS-09019 describe other failures.

## Representations

None as a separate block. The unit README delivers the shaded region and the outer and inner radii as a figure on the orientation and the key idea (docs/lessons/unit-09/README.md, section 6).

## Prerequisite bridge

- BC-PRQ-06005, BC-PRQ-08006, BC-PRQ-09002, BC-PRQ-09004, each from its `description_plain` and `failure_signature`.

## Time

BC-QA-09013 is a calculator shape: Section I Part B, 2.92 minutes (research/exam/exam-structure.md#Section and part layout); as a free response part, 3 points, 5.0 minutes (docs/lessons/unit-09/README.md, section 5). A fluent solver writes the integral with limits and the value; the outer test is held [inferred].

## Checks

- chk-1, completion of ex-1, both bands, calculator: the integral is given and the value asked. Key 4.653.
- chk-2, isomorph, both bands, calculator. Draw: constant 3, coefficient 3, circle 4, orientation right, intersections given; \(r=3+3\cos\theta\) against \(r=4\), angles \(\pm\arccos(1/3)\). Key 15.307 (SymPy 15.30738).
- chk-3, MCQ, low band, calculator. Draw: constant 5, coefficient 3, circle 7, orientation right, intersections given; \(r=5+3\cos\theta\) against \(r=7\), angles \(\pm\arccos(2/3)\). Key 8.196 (SymPy 8.19591). Distractors: 16.392, the one half omitted (BC-ERR-09035); \(-8.196\), radii exchanged (BC-ERR-09039); 0.441, the square of the difference (BC-ERR-09040).

## Delivery

- orientation, ki-1: figure. Rule 4 (README rule 3): BC-REP-13 and BC-REP-02 on BC-SKL-09040; not promoted, `difficulty_variables` name properties, not a varying quantity. The orientation shades the region; ki-1 marks R and r on one ray.
- ex-1, ex-2, the four error blocks: step_reveal. Rule 1.

## Band plan

- Low (full): prediction, orientation, bridges, ki-1, st-1 with the contrast pair, ex-1, chk-1, the four error blocks, ex-2 (faded from step 3) and its lines, chk-2, chk-3. 769 words, 5.2 minutes.
- Mid (brief): prediction, orientation, bridges, ki-1, st-1 with the contrast pair, ex-1, chk-1, err-BC-ERR-09035, err-BC-ERR-09039, chk-2. 447 words, 3.0 minutes.
- Refresher: ki-1, the four error blocks, ex-1.

## Sources

- BC-CON-09016; BC-SKL-09040, BC-SKL-09041, BC-SKL-09042, BC-SKL-09043; BC-EK-CHA-5D2; ced:179
- BC-QA-09013, BC-QA-99006; BC-FRQ-2013-Q2-A, BC-FRQ-2014-Q2-A, BC-FRQ-2025-Q2-B, BC-FRQ-2018-Q5-A, BC-MCQ-PE2012-044
- BC-PT-99048, BC-PT-99004, BC-PT-99002, BC-PT-99001
- BC-ERR-09035, BC-ERR-09039, BC-ERR-09040, BC-ERR-09041; BC-MIS-08019, BC-MIS-09018
- BC-PRQ-06005, BC-PRQ-08006, BC-PRQ-09002, BC-PRQ-09004
- sg-25:7, sg-25:8
- research/units/unit-09-parametric-polar-vector.md#9.9 Finding the Area of the Region Bounded by Two Polar Curves
- research/question-analysis/question-archetypes.md#BC-QA-09013 Area inside one polar curve and outside another
- research/scoring/common-point-losses.md#Setup points
- research/exam/exam-structure.md#Section and part layout
- [inferred] The held steps; the untagged point types; the limacon orientation reading. Each settled as the inferred array states.

## Machine record

```json
{
 "id": "LSN-CON-09016",
 "kind": "concept",
 "target_id": "BC-CON-09016",
 "unit": "09",
 "skills": [
  "BC-SKL-09040",
  "BC-SKL-09041",
  "BC-SKL-09042",
  "BC-SKL-09043"
 ],
 "prediction": {
  "id": "pr-1",
  "stem": {
   "text": "At \\(\\theta=0\\) the curves \\(r=2+2\\cos\\theta\\) and \\(r=3\\) have radii 4 and 3. Predict the area of the thin slice between them for a small angle \\(d\\theta\\).",
   "command_verb": "predict"
  },
  "format": "mcq",
  "options": [
   {
    "id": "A",
    "label": "\\(\\tfrac12(4-3)^2\\,d\\theta\\)",
    "is_key": false
   },
   {
    "id": "B",
    "label": "\\(\\tfrac12(4^2-3^2)\\,d\\theta\\)",
    "is_key": true
   },
   {
    "id": "C",
    "label": "\\((4-3)\\,d\\theta\\)",
    "is_key": false
   },
   {
    "id": "D",
    "label": "\\(\\tfrac12(4\\cdot 3)\\,d\\theta\\)",
    "is_key": false
   }
  ],
  "resolution": "Each radius sweeps a sector of area \\(\\tfrac12r^2\\,d\\theta\\), so the slice is \\(\\tfrac12(4^2-3^2)\\,d\\theta\\), and \\(\\tfrac12(R^2-r^2)\\,d\\theta\\) in general.",
  "sources": [
   "BC-CON-09016",
   "research/units/unit-09-parametric-polar-vector.md#9.9 Finding the Area of the Region Bounded by Two Polar Curves"
  ]
 },
 "orientation": {
  "text": "Between two curves the area is \\(\\tfrac12\\int_\\alpha^\\beta(R^2-r^2)\\,d\\theta\\), with \\(R\\) the outer radius. A response squares each radius before subtracting, and shows the limits and the factor one half.",
  "sources": [
   "BC-CON-09016",
   "research/units/unit-09-parametric-polar-vector.md#9.9 Finding the Area of the Region Bounded by Two Polar Curves"
  ]
 },
 "key_ideas": [
  {
   "id": "ki-1",
   "ek_id": "BC-EK-CHA-5D2",
   "depth": "core",
   "text": "The area inside one curve and outside another is one half the integral of the outer radius squared minus the inner radius squared, between the angles where the curves meet. Each radius is squared before the subtraction. The outer curve is the one with the larger radius, tested at one angle. A region symmetric about a ray is twice its half.",
   "notation": "one half the integral of the difference of squares",
   "quote": null,
   "sources": [
    "BC-EK-CHA-5D2",
    "ced:179",
    "sg-25:7",
    "sg-25:8",
    "research/units/unit-09-parametric-polar-vector.md#9.9 Finding the Area of the Region Bounded by Two Polar Curves"
   ]
  }
 ],
 "strategy": [
  {
   "id": "st-1",
   "archetype_id": "BC-QA-09013",
   "cue": "Inside one curve and outside another, angles known.",
   "method": "The outer curve, then \\(\\tfrac12\\int(R^2-r^2)\\,d\\theta\\).",
   "rival": "The square of the difference, \\(\\tfrac12\\int(R-r)^2\\,d\\theta\\).",
   "separating_feature": "Square each radius first, then subtract.",
   "sources": [
    "BC-QA-09013"
   ],
   "evidence_tag": "verified",
   "contrast": {
    "this": {
     "text": "Find the area of the region inside \\(r=2+2\\cos\\theta\\) and outside \\(r=3\\), between \\(\\theta=-\\pi/3\\) and \\(\\theta=\\pi/3\\).",
     "archetype_id": "BC-QA-09013"
    },
    "not_this": {
     "text": "For \\(-\\pi/3\\le\\theta\\le\\pi/3\\), the curves \\(r=2+2\\cos\\theta\\) and \\(r=3\\) are \\(g(\\theta)\\) apart on each ray. Find \\(g'(\\pi/6)\\).",
     "why_not": "It asks how fast the gap of radii changes, not an area."
    },
    "feature": "Area squares each radius; the gap uses the radii themselves."
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
    "intersections": "given"
   },
   "problem": {
    "text": "The curves \\(r=2+2\\cos\\theta\\) and \\(r=3\\) meet at \\(\\theta=\\pm\\pi/3\\). Using a calculator, find the area of the region inside the first curve and outside the second.",
    "command_verb": "find"
   },
   "calculator_status": "calculator",
   "steps": [
    {
     "cue": "Which curve is outer? Test \\(\\theta=0\\).",
     "why": "Radii 4 and 3, so the first curve is outer."
    },
    {
     "cue": "Outer squared minus inner squared, halved.",
     "why": "Square each radius, then subtract.",
     "expr": "((2 + 2*cos(theta))**2 - 9)/2",
     "relation": "new"
    },
    {
     "cue": "Limits are the given angles.",
     "why": "The integral shows the square of the outer radius.",
     "expr": "Integral(((2 + 2*cos(theta))**2 - 9)/2, (theta, -pi/3, pi/3))",
     "relation": "new"
    },
    {
     "cue": "Setup written, so the calculator evaluates.",
     "why": "Three places, no earlier rounding.",
     "expr": "4.653",
     "relation": "evaluate",
     "subs": {},
     "approx": true
    }
   ],
   "answer": {
    "form": "numeric",
    "expr": "4.653"
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
    "constant": "3",
    "coefficient": "2",
    "circle": "4",
    "orientation": "up",
    "intersections": "given"
   },
   "problem": {
    "text": "The curves \\(r=3+2\\sin\\theta\\) and \\(r=4\\) meet at \\(\\theta=\\pi/6\\) and \\(\\theta=5\\pi/6\\). Using a calculator, find the area of the region inside the first curve and outside the second.",
    "command_verb": "find"
   },
   "calculator_status": "calculator",
   "steps": [
    {
     "cue": "Test \\(\\theta=\\pi/2\\): radii 5 and 4.",
     "why": "The first curve is outer."
    },
    {
     "cue": "The region is symmetric about \\(\\theta=\\pi/2\\): double the half.",
     "why": "Twice one half leaves no fraction.",
     "expr": "(3 + 2*sin(theta))**2 - 16",
     "relation": "new"
    },
    {
     "cue": "Half the region runs from \\(\\pi/6\\) to \\(\\pi/2\\).",
     "why": "One integral of the squared radii.",
     "expr": "Integral((3 + 2*sin(theta))**2 - 16, (theta, pi/6, pi/2))",
     "relation": "new",
     "point_type_id": "BC-PT-99048"
    },
    {
     "cue": "Setup written, so the calculator evaluates.",
     "why": "Three places.",
     "expr": "6.022",
     "relation": "evaluate",
     "subs": {},
     "approx": true,
     "point_type_id": "BC-PT-99004"
    }
   ],
   "answer": {
    "form": "numeric",
    "expr": "6.022"
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
   "point_type_ids": [
    "BC-PT-99048",
    "BC-PT-99004"
   ],
   "lines": [
    {
     "point_type_id": "BC-PT-99048",
     "text": "Polar area integrand with the square of the radial function. Earned by: A definite integral whose integrand contains the square of the polar function, with or without the differential (sg-25:7, sg-26:7). Not earned by: An integrand using the radial function unsquared (sg-25:7)."
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
   "error_id": "BC-ERR-09035",
   "observed_behavior": "The area integrand is the square of r with no factor of one half.",
   "scoring_consequence": "The value is twice the area, so the answer point is lost; the factor is assessed with the limits (sg-25:7).",
   "wrong_step": {
    "text": "No factor \\(\\tfrac12\\).",
    "expr": "Integral((2 + 2*cos(theta))**2 - 9, (theta, -pi/3, pi/3))"
   },
   "right_step": {
    "text": "With the factor \\(\\tfrac12\\).",
    "expr": "Integral(((2 + 2*cos(theta))**2 - 9)/2, (theta, -pi/3, pi/3))"
   },
   "relation": "distinct",
   "fix_prompt": true,
   "possible_reason": {
    "misconception_id": "BC-MIS-08019",
    "text": "remembers the squared dimension but not the fraction in front of it"
   },
   "sources": [
    "BC-ERR-09035",
    "BC-MIS-08019"
   ]
  },
  {
   "error_id": "BC-ERR-09039",
   "observed_behavior": "The integrand subtracts the square of the outer radius from the square of the inner radius.",
   "scoring_consequence": "A negative area is produced and the integrand point is lost.",
   "wrong_step": {
    "text": "Inner minus outer.",
    "expr": "Integral((9 - (2 + 2*cos(theta))**2)/2, (theta, -pi/3, pi/3))"
   },
   "right_step": {
    "text": "Outer minus inner.",
    "expr": "Integral(((2 + 2*cos(theta))**2 - 9)/2, (theta, -pi/3, pi/3))"
   },
   "relation": "distinct",
   "fix_prompt": true,
   "possible_reason": null,
   "sources": [
    "BC-ERR-09039"
   ]
  },
  {
   "error_id": "BC-ERR-09040",
   "observed_behavior": "The integrand is the square of the difference of the two radius functions rather than the difference of their squares.",
   "scoring_consequence": "The integrand point is lost (sg-25:7).",
   "wrong_step": {
    "text": "\\(\\tfrac12(R-r)^2\\).",
    "expr": "Integral((2 + 2*cos(theta) - 3)**2/2, (theta, -pi/3, pi/3))"
   },
   "right_step": {
    "text": "\\(\\tfrac12(R^2-r^2)\\).",
    "expr": "Integral(((2 + 2*cos(theta))**2 - 9)/2, (theta, -pi/3, pi/3))"
   },
   "relation": "distinct",
   "fix_prompt": true,
   "possible_reason": {
    "misconception_id": "BC-MIS-09018",
    "text": "subtracts the radii before squaring"
   },
   "sources": [
    "BC-ERR-09040",
    "BC-MIS-09018"
   ]
  },
  {
   "error_id": "BC-ERR-09041",
   "observed_behavior": "Half of a symmetric region is integrated and the result is reported without doubling, or a full region is doubled as well.",
   "scoring_consequence": "The reported area is half or twice the correct value and the answer point is lost; the correctly doubled form earned all points in 2025 (sg-25:8).",
   "wrong_step": {
    "text": "The half from 0 to \\(\\pi/3\\), not doubled.",
    "expr": "Integral(((2 + 2*cos(theta))**2 - 9)/2, (theta, 0, pi/3))"
   },
   "right_step": {
    "text": "The half, doubled.",
    "expr": "2*Integral(((2 + 2*cos(theta))**2 - 9)/2, (theta, 0, pi/3))"
   },
   "relation": "distinct",
   "fix_prompt": true,
   "possible_reason": null,
   "sources": [
    "BC-ERR-09041"
   ]
  }
 ],
 "representations": null,
 "prerequisite_bridges": [
  {
   "prq_id": "BC-PRQ-06005",
   "text": "The integrand is a function of \\(\\theta\\)."
  },
  {
   "prq_id": "BC-PRQ-08006",
   "text": "Three places after the decimal point."
  },
  {
   "prq_id": "BC-PRQ-09002",
   "text": "Cosine and sine at the bounding angles."
  },
  {
   "prq_id": "BC-PRQ-09004",
   "text": "The angles trace the region once."
  }
 ],
 "time": {
  "exam_part": "I-B",
  "budget_minutes": 2.92,
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
   "archetype_id": "BC-QA-09013",
   "parameter_draw": {
    "constant": "2",
    "coefficient": "2",
    "circle": "3",
    "orientation": "right",
    "intersections": "given"
   },
   "completes": "ex-1",
   "stem": {
    "text": "The area inside \\(r=2+2\\cos\\theta\\) and outside \\(r=3\\) is \\(\\int_{-\\pi/3}^{\\pi/3}\\tfrac12\\left((2+2\\cos\\theta)^2-9\\right)d\\theta\\). Using a calculator, evaluate it.",
    "command_verb": "evaluate"
   },
   "key": {
    "form": "numeric",
    "expr": "4.653"
   },
   "steps": [
    {
     "text": "Integral.",
     "expr": "Integral(((2 + 2*cos(theta))**2 - 9)/2, (theta, -pi/3, pi/3))",
     "relation": "new"
    },
    {
     "text": "Calculator.",
     "expr": "4.653",
     "relation": "evaluate",
     "subs": {},
     "approx": true
    }
   ],
   "calculator_status": "calculator",
   "skills": [
    "BC-SKL-09042"
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
    "coefficient": "3",
    "circle": "4",
    "orientation": "right",
    "intersections": "given"
   },
   "stem": {
    "text": "The curves \\(r=3+3\\cos\\theta\\) and \\(r=4\\) meet at \\(\\theta=\\pm\\arccos(1/3)\\). Using a calculator, find the area inside the first and outside the second.",
    "command_verb": "find"
   },
   "key": {
    "form": "numeric",
    "expr": "15.307"
   },
   "steps": [
    {
     "text": "Integral.",
     "expr": "Integral(((3 + 3*cos(theta))**2 - 16)/2, (theta, -acos(1/3), acos(1/3)))",
     "relation": "new"
    },
    {
     "text": "Calculator.",
     "expr": "15.307",
     "relation": "evaluate",
     "subs": {},
     "approx": true
    }
   ],
   "calculator_status": "calculator",
   "skills": [
    "BC-SKL-09041"
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
    "constant": "5",
    "coefficient": "3",
    "circle": "7",
    "orientation": "right",
    "intersections": "given"
   },
   "stem": {
    "text": "The curves \\(r=5+3\\cos\\theta\\) and \\(r=7\\) meet at \\(\\theta=\\pm\\arccos(2/3)\\). Using a calculator, the area inside the first and outside the second is",
    "command_verb": "identify"
   },
   "key": {
    "form": "numeric",
    "expr": "8.196"
   },
   "steps": [
    {
     "text": "Integral.",
     "expr": "Integral(((5 + 3*cos(theta))**2 - 49)/2, (theta, -acos(2/3), acos(2/3)))",
     "relation": "new"
    },
    {
     "text": "Calculator.",
     "expr": "8.196",
     "relation": "evaluate",
     "subs": {},
     "approx": true
    }
   ],
   "options": [
    {
     "id": "A",
     "is_key": false,
     "label": "16.392",
     "expr": "16.392",
     "error_path": "BC-ERR-09035",
     "derivation": "the integral without the factor one half, twice the area"
    },
    {
     "id": "B",
     "is_key": true,
     "label": "8.196",
     "expr": "8.196",
     "error_path": null
    },
    {
     "id": "C",
     "is_key": false,
     "label": "-8.196",
     "expr": "-8.196",
     "error_path": "BC-ERR-09039",
     "derivation": "inner squared minus outer squared"
    },
    {
     "id": "D",
     "is_key": false,
     "label": "0.441",
     "expr": "0.441",
     "error_path": "BC-ERR-09040",
     "derivation": "the square of the difference of the radii"
    }
   ],
   "calculator_status": "calculator",
   "skills": [
    "BC-SKL-09041"
   ]
  }
 ],
 "delivery": [
  {
   "block": "orientation",
   "mode": "figure",
   "reason": "rule 4: BC-REP-13 and BC-REP-02 on BC-SKL-09040; not promoted, BC-QA-09013 difficulty_variables name properties (a circle, exact or decimal angles), not a varying quantity",
   "sources": [
    "BC-SKL-09040"
   ],
   "spec": {
    "kind": "polar_region",
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
    "shaded": "inside the first curve and outside the second, from -pi/3 to pi/3",
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
      "text": "shaded region",
      "placement": "inside"
     }
    ]
   },
   "fallback": "the same figure static, region shaded and labelled inside",
   "keyboard": "no control; the figure description is reached with Tab"
  },
  {
   "block": "ki-1",
   "mode": "figure",
   "reason": "rule 4: BC-REP-13 and BC-REP-02 on BC-SKL-09040; one ray is drawn with the outer radius R and the inner radius r marked, which is the slice the integrand sums",
   "sources": [
    "BC-SKL-09040"
   ],
   "spec": {
    "kind": "polar_region",
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
      "theta": "0",
      "segments": [
       {
        "from": 0,
        "to": 3,
        "label": "r = 3"
       },
       {
        "from": 3,
        "to": 4,
        "label": "R - r"
       }
      ]
     }
    ],
    "labels": [
     {
      "text": "R = 4 on this ray",
      "placement": "inside"
     },
     {
      "text": "r = 3 on this ray",
      "placement": "inside"
     },
     {
      "text": "shaded region",
      "placement": "inside"
     }
    ]
   },
   "fallback": "the same figure static with the ray and its radii labelled",
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
   "block": "err-BC-ERR-09035",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  },
  {
   "block": "err-BC-ERR-09039",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  },
  {
   "block": "err-BC-ERR-09040",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  },
  {
   "block": "err-BC-ERR-09041",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  }
 ],
 "refresher": [
  "ki-1",
  "err-BC-ERR-09035",
  "err-BC-ERR-09039",
  "err-BC-ERR-09040",
  "err-BC-ERR-09041",
  "ex-1"
 ],
 "research_lines": [
  {
   "file": "research/units/unit-09-parametric-polar-vector.md",
   "line": "The two radii are squared before they are subtracted, as in the washer method of Unit 8."
  }
 ],
 "inferred": [
  {
   "claim": "A fluent solver writes the integral with its limits and the value, and holds which curve is outer.",
   "settles": "Per-step timing from the fluency telemetry."
  },
  {
   "claim": "ex-1 carries no point tag and BC-PT-99002 and BC-PT-99001 are untagged: the brief band cannot carry a scoring line beside the prediction and the contrast pair.",
   "settles": "A brief cap that admits the further lines."
  },
  {
   "claim": "Orientation of the limacon (right, up) is read as r = c + b cos and c + b sin.",
   "settles": "The app/generation/templates/qa_09013.py orientation table."
  }
 ],
 "sources": [
  "BC-CON-09016",
  "BC-SKL-09040",
  "BC-SKL-09041",
  "BC-SKL-09042",
  "BC-SKL-09043",
  "BC-EK-CHA-5D2",
  "ced:179",
  "BC-QA-09013",
  "BC-PT-99048",
  "BC-PT-99004",
  "BC-PT-99002",
  "BC-PT-99001",
  "BC-ERR-09035",
  "BC-ERR-09039",
  "BC-ERR-09040",
  "BC-ERR-09041",
  "BC-MIS-08019",
  "BC-MIS-09018",
  "BC-PRQ-06005",
  "BC-PRQ-08006",
  "BC-PRQ-09002",
  "BC-PRQ-09004",
  "sg-25:7",
  "sg-25:8",
  "BC-FRQ-2013-Q2-A",
  "BC-FRQ-2014-Q2-A",
  "BC-FRQ-2025-Q2-B",
  "BC-FRQ-2018-Q5-A",
  "BC-MCQ-PE2012-044",
  "BC-QA-99006",
  "research/units/unit-09-parametric-polar-vector.md#9.9 Finding the Area of the Region Bounded by Two Polar Curves",
  "research/question-analysis/question-archetypes.md#BC-QA-09013 Area inside one polar curve and outside another",
  "research/scoring/common-point-losses.md#Setup points",
  "research/exam/exam-structure.md#Section and part layout"
 ],
 "word_count": {
  "full": 769,
  "brief": 447
 },
 "read_minutes": {
  "full": 5.2,
  "brief": 3.0
 }
}
```
