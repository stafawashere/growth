---
title: LSN-CON-09015 Area of a polar region as an integral of one half r squared
research_date: 2026-09-29
status: designed
purpose: Authoring spec for the concept lesson on BC-CON-09015, the area of a region swept by rays from the pole as one half the integral of r squared over angles that trace it once, a productive-failure target, built from authoring_bundle("BC-CON-09015") and the research files it cites, so an author fills plan 15's lesson record without making a teaching decision.
---

# LSN-CON-09015 Area of a polar region as an integral of one half r squared

Concept BC-CON-09015 (skills BC-SKL-09035, BC-SKL-09036, BC-SKL-09037, BC-SKL-09038), topic 9.8 of Unit 9, BC only (ced:178), loaded by two archetypes, BC-QA-09012 (family polar-area, either) and BC-QA-09014 (the opener, no calculator). Hard parent in Unit 9: BC-CON-09012; outside hard parents BC-SKL-06028 and BC-SKL-06034 (docs/lessons/unit-09/README.md, section 1). It is a productive-failure target through BC-QA-09014 (BC-DF-15), listed in `PRODUCTIVE_FAILURE_TARGETS`.

## Prediction

Served first, both bands: an `mcq` on ex-1's own curve \(r=3+\cos\theta\), radius 4 at \(\theta=0\), asking for the area of the thin sector between the rays \(\theta=0\) and \(\theta=d\theta\). Key B, \(8\,d\theta\). Distractors: A \(4\,d\theta\), the radius times the angle (the rectangle BC-QA-09014 lists in `wrong_approaches`); C \(16\,d\theta\), the square without the half; D \(2\,d\theta\). Only B is the sector area. It is answerable before the rule, because a circular sector has area one half \(r^2\) times its angle. The resolution states that area and the sum it gives, with no verdict. Source: BC-CON-09015 and the topic section the key idea cites.

## Orientation

Served text, from BC-CON-09015 `description_plain` ("sum the areas of thin circular sectors across the angle interval") and the topic's Assessment behaviour paragraph (research/units/unit-09-parametric-polar-vector.md#9.8 Find the Area of a Polar Region or the Area Bounded by a Single Polar Curve): a response shows the square of r, the factor one half and limits that trace the region once. No count, no frequency.

## Key ideas

All four skills map to one essential knowledge statement, BC-EK-CHA-5D1 (ced:178): one core block, both bands.

- ki-1 (core). Paraphrase of the Required mathematical knowledge paragraphs Polar area (hypothesis: r continuous on an interval that sweeps the region exactly once), Limits (angles, not x values; consecutive zeros of r bound one loop) and Factor and square (sg-25:7). The sector reading is the concept's `description_plain` and BC-QA-09014's `expected_solution_path`. Notation line, the concept's `notation`. No anchor quote: the CHA-5.D.1 sentence on ced:178 says the idea extends to polar coordinates and adds no content.

## Recognition

BC-QA-09012 (research/question-analysis/question-archetypes.md#BC-QA-09012 Area of a region bounded by a single polar curve) and BC-QA-09014 (research/question-analysis/question-archetypes.md#BC-QA-09014 Area of a polar region found before the polar area integral is taught) load the skills.

- BC-QA-09012 `common_givens`: "a polar equation" and "a figure or an angle interval". `asked_to_produce`: "a polar area integral" and "a numerical area". `typical_wording`: "find the area of the region bounded by the polar curve on the stated interval and show the setup for the calculations". Shapes: BC-FRQ-2019-Q2-A, BC-FRQ-2019-Q2-C, BC-FRQ-2019-Q2-D, BC-FRQ-2026-Q2-A and the MCQ BC-MCQ-CED-021.
- BC-QA-09014 `common_givens`: "a polar equation" and the rays that bound the region; `asked_to_produce`: "the exact area"; `typical_wording`: "find the area of the region enclosed by the polar curve". It is served as an opener, before the rule (`multipart_structure`), and has no official examples.
- The signal in the stem: a polar equation and the word area for a region it encloses, or two rays that bound it.

The near miss of the contrast pair is the Cartesian area under \(y=3+\cos x\) between vertical lines, which looks like the polar curve and calls for the Unit 8 integral of the function: BC-MIS-09017 (a polar area is an integral of the curve itself) is what the near miss invites. What says "not this concept": an x interval and a graph \(y=f(x)\) (BC-CON-08010); two curves bounding the region (BC-CON-09016); a rate of r (BC-CON-09013).

## Method choice

- st-1, BC-QA-09012. Cue from `common_givens` and `asked_to_produce`. Method, `expected_solution_path[1]` "write one half the integral of the square of r", with `[0]` the bounding angles. Rival: `common_distractors` "the integral of r without the square" and `wrong_approaches` "integrating over an interval that traces the loop twice". Separating feature: sectors of area one half r squared, over one tracing. Both cue fields exist, so the block is not inferred. No served field opens with the reader's own label. The block carries the contrast pair, a polar region beside a Cartesian region, with the feature that separates them.

## Solution path

- ex-1, BC-QA-09014, both bands, no calculator. Draw: region full, trig cos, frequency 1, base 3, amplitude 1; \(r=3+\cos\theta\), enclosed once on 0 to \(2\pi\). Chain: the sector area \(\tfrac12r^2\) (`new`), the integral (`new`, tagged BC-PT-99048), the exact value \(\tfrac{19\pi}{2}\) (`evaluate`). No published item on BC-QA-09014 carries this draw (content/items_gen_unit09/ITM-GEN-09014-00 to 21).
- ex-2, low band, no calculator, faded from step 3. BC-QA-09012. Draw: shape petal, constant 2, coefficient 4, frequency 2, trig sin, sweep first; one petal of \(r=4\sin2\theta\), zeros at 0 and \(\pi/2\), area \(2\pi\). Steps 1 and 2 (the zero equation and the two consecutive zeros) are shown, the student writes the integral and the value, then steps 3 and 4 reveal. The fade falls there because finding the limits is the new skill of the example and the integral repeats ex-1. No published item on BC-QA-09012 carries this draw (content/items_gen_unit09/ITM-GEN-09012-00 to 21; the constant is ignored by a petal).
- Comparison gap for the productive-failure target: when the BC-QA-09014 opener preceded the lesson, ex-1 opens with a comparison callout naming the gap between the opener attempt and the canonical method. The attempt is a rectangle in the angle and the radius, or the Cartesian integral of the curve (BC-QA-09014 `wrong_approaches`, BC-ERR-09036, BC-MIS-09017); the canonical method cuts the region into thin sectors of area one half r squared times the angle and adds them (BC-QA-09014 `expected_solution_path`; docs/plan/15-lessons.md Within a concept, step 2).
- A fluent solver writes the integral with its limits and the value; the cutting into sectors is held (docs/lessons/unit-09/README.md, section 5).

## Scoring

BC-QA-09012 lists BC-PT-99048, 99004, 99001, 99005; BC-QA-09014 lists BC-PT-99048. ex-1 carries no tag: a scoring line costs 42 to 88 words and the brief band cannot carry one beside the prediction and the contrast pair (inferred array). ex-2 tags BC-PT-99048 on the integral and BC-PT-99004 on the value. BC-PT-99001 and BC-PT-99005 are untagged: the limits and the factor one half are assessed in the answer point (sg-25:7), and the archetype's calculator setup point does not apply to an exact value. The lines are `reader_checks` output.

Point losses from research: the integrand point is lost when the square is missing (BC-ERR-99031; research/scoring/common-point-losses.md#Setup points, crabbc-25:29); the value is twice the area when the factor one half is missing (BC-ERR-09035, sg-25:7).

## Traps

Four errors meet the skills, in bundle order: BC-ERR-09016, 09035, 09036, 09037 (each linked to a high severity BC-MIS, then by id). BC-ERR-99031, 99019 and 99021 fall past the cap of 4. Low band all four, mid band the first two. All four carry `fix_prompt` true, since each pair is distinct.

- err-BC-ERR-09016: on ex-1's draw, limits 0 to \(4\pi\) against 0 to \(2\pi\). No possible reason line, for the brief band words; the record links BC-MIS-09007 and BC-MIS-09019.
- err-BC-ERR-09035: on ex-1's draw, the factor one half omitted. No possible reason line, for the brief band words; the record links BC-MIS-09017 and BC-MIS-08019.
- err-BC-ERR-09036: on ex-1's draw, the integral of r against the integral of one half r squared. Possible reason, BC-MIS-09017.
- err-BC-ERR-09037: on ex-2's draw, the petal over 0 to \(2\pi\) against 0 to \(\pi/2\). Its record text names the intersection angles of two curves, which a single petal does not have; the BC-QA-09012 generator pairs this error with an even frequency petal and the same wrong sweep (app/generation/templates/qa_09012.py), which is the pairing shown. No possible reason line: BC-MIS-09019 describes two curves.

## Representations

One block, low band, delivered as `model`: the topic's Representations paragraph names a plotted polar region converted to an angle interval and a polar equation converted to an integral (BC-REP-02 to BC-REP-01, BC-REP-13 to BC-REP-01). The sector sums table shows the sum of \(\tfrac12r^2\,\Delta\theta\) at 1, 2, 4, 16, 64 and 256 sectors for \(r=3+\cos\theta\) from 0 to \(\pi/2\): 12.566, 11.680, 11.110, 10.631, 10.504, 10.472, closing on the integral 10.461. The quarter sweep is used because the full turn of ex-1's periodic integrand is exact at 4 sectors and would show no approach.

## Prerequisite bridge

- BC-PRQ-06005, BC-PRQ-08006, BC-PRQ-09002, BC-PRQ-09004, each from its `description_plain` and `failure_signature`.

## Time

ex-1 is the opener shape, Section I Part A, 2.14 minutes (research/exam/exam-structure.md#Section and part layout; BC-QA-09014 is no calculator, and BC-QA-09012 is I-A or I-B). As a free response part, BC-QA-09012 is 2 points, 3.33 minutes (3 points, 5.0 in BC-FRQ-2019-Q2-C; docs/lessons/unit-09/README.md, section 5). A fluent solver writes the bounding angles, the integral and the value; the zeros of r and the cutting into sectors are held [inferred].

## Checks

- chk-1, completion of ex-1, both bands: the integral is given and the exact value asked. Key \(\tfrac{19\pi}{2}\).
- chk-2, isomorph, both bands, no calculator. BC-QA-09014. Draw: region quarter, trig cos, frequency 1, base 5, amplitude 2; \(r=5+2\cos\theta\) between \(\theta=0\) and \(\pi/2\). Key \(10+\tfrac{27\pi}{4}\).
- chk-3, MCQ, low band, no calculator. BC-QA-09014. Draw: region half, trig sin, frequency 1, base 4, amplitude 1; \(r=4+\sin\theta\) between 0 and \(\pi\). Key \(8+\tfrac{33\pi}{4}\). Distractors: \(16+\tfrac{33\pi}{2}\), the one half omitted (BC-ERR-09035); \(2+4\pi\), the integral of r (BC-ERR-09036); \(\tfrac{33\pi}{2}\), the limits of the whole figure, 0 to \(2\pi\) (BC-ERR-09037).

## Delivery

- orientation: figure. Rule 4 (README rule 3): BC-REP-13 and BC-REP-02 on BC-SKL-09036 and BC-SKL-09037; not promoted, the stem asks for an area.
- ki-1: motion. Rule 2: a region swept by rays from the pole, each sector filling the area as the angle advances (docs/lessons/unit-09/README.md, section 6). Five frames, reduced motion and a static fallback in the record.
- representations: model. The template model row and the productive-failure target; the sector sums table above.
- ex-1, ex-2, the four error blocks: step_reveal. Rule 1.

## Band plan

- Low (full): prediction, orientation, bridges, ki-1, st-1 with the contrast pair, ex-1, chk-1, the four error blocks, ex-2 (faded from step 3) and its lines, chk-2, representations, chk-3. 789 words, 5.3 minutes.
- Mid (brief): prediction, orientation, bridges, ki-1, st-1 with the contrast pair, ex-1, chk-1, err-BC-ERR-09016, err-BC-ERR-09035, chk-2. 447 words, 3.0 minutes.
- Refresher: ki-1, the four error blocks, ex-1.

## Sources

- BC-CON-09015; BC-SKL-09035, BC-SKL-09036, BC-SKL-09037, BC-SKL-09038; BC-EK-CHA-5D1; ced:178
- BC-QA-09012, BC-QA-09014; BC-FRQ-2019-Q2-A, BC-FRQ-2019-Q2-C, BC-FRQ-2019-Q2-D, BC-FRQ-2026-Q2-A, BC-MCQ-CED-021
- BC-PT-99048, BC-PT-99004, BC-PT-99001, BC-PT-99005
- BC-ERR-09016, BC-ERR-09035, BC-ERR-09036, BC-ERR-09037; BC-MIS-09007, BC-MIS-08019, BC-MIS-09017
- BC-PRQ-06005, BC-PRQ-08006, BC-PRQ-09002, BC-PRQ-09004
- sg-25:7, sg-25:8
- research/units/unit-09-parametric-polar-vector.md#9.8 Find the Area of a Polar Region or the Area Bounded by a Single Polar Curve
- research/question-analysis/question-archetypes.md#BC-QA-09012 Area of a region bounded by a single polar curve
- research/question-analysis/question-archetypes.md#BC-QA-09014 Area of a polar region found before the polar area integral is taught
- research/scoring/common-point-losses.md#Setup points
- research/exam/exam-structure.md#Section and part layout
- [inferred] The held steps; the empty ex-1 scoring entry; the quarter sweep table; the single curve reading of BC-ERR-09037. Each settled as the inferred array states.

## Machine record

```json
{
 "id": "LSN-CON-09015",
 "kind": "concept",
 "target_id": "BC-CON-09015",
 "unit": "09",
 "skills": [
  "BC-SKL-09035",
  "BC-SKL-09036",
  "BC-SKL-09037",
  "BC-SKL-09038"
 ],
 "prediction": {
  "id": "pr-1",
  "stem": {
   "text": "The curve \\(r=3+\\cos\\theta\\) has radius 4 at \\(\\theta=0\\). Predict the area of the thin sector between the rays \\(\\theta=0\\) and \\(\\theta=d\\theta\\), for a small \\(d\\theta\\).",
   "command_verb": "predict"
  },
  "format": "mcq",
  "options": [
   {
    "id": "A",
    "label": "\\(4\\,d\\theta\\)",
    "is_key": false
   },
   {
    "id": "B",
    "label": "\\(8\\,d\\theta\\)",
    "is_key": true
   },
   {
    "id": "C",
    "label": "\\(16\\,d\\theta\\)",
    "is_key": false
   },
   {
    "id": "D",
    "label": "\\(2\\,d\\theta\\)",
    "is_key": false
   }
  ],
  "resolution": "A sector of radius \\(r\\) and angle \\(d\\theta\\) has area \\(\\tfrac12r^2\\,d\\theta\\), here \\(8\\,d\\theta\\). Adding the sectors over the angles gives \\(\\tfrac12\\int r^2\\,d\\theta\\).",
  "sources": [
   "BC-CON-09015",
   "research/units/unit-09-parametric-polar-vector.md#9.8 Find the Area of a Polar Region or the Area Bounded by a Single Polar Curve"
  ]
 },
 "orientation": {
  "text": "Polar area is one half the integral of \\(r^2\\) over angles that sweep the region once. A response shows the square, the factor one half, and limits that trace the region once.",
  "sources": [
   "BC-CON-09015",
   "research/units/unit-09-parametric-polar-vector.md#9.8 Find the Area of a Polar Region or the Area Bounded by a Single Polar Curve"
  ]
 },
 "key_ideas": [
  {
   "id": "ki-1",
   "ek_id": "BC-EK-CHA-5D1",
   "depth": "core",
   "text": "The area swept by rays from the pole is a sum of thin sectors, each \\(\\tfrac12r^2\\) times its angle, so it is \\(\\tfrac12\\int_\\alpha^\\beta r^2\\,d\\theta\\). The limits are angles that trace the region once: consecutive zeros of r bound one loop, and tracing twice doubles the area.",
   "notation": "one half the integral of r squared d theta",
   "quote": null,
   "sources": [
    "BC-EK-CHA-5D1",
    "ced:178",
    "sg-25:7",
    "research/units/unit-09-parametric-polar-vector.md#9.8 Find the Area of a Polar Region or the Area Bounded by a Single Polar Curve"
   ]
  }
 ],
 "strategy": [
  {
   "id": "st-1",
   "archetype_id": "BC-QA-09012",
   "cue": "A polar curve, and a region it encloses or two rays bound.",
   "method": "\\(\\tfrac12\\int r^2\\,d\\theta\\) over angles that trace the region once.",
   "rival": "The integral of r, or a sweep that traces the loop twice.",
   "separating_feature": "Sectors of area one half r squared, over one tracing.",
   "sources": [
    "BC-QA-09012"
   ],
   "evidence_tag": "verified",
   "contrast": {
    "this": {
     "text": "Find the area of the region enclosed by the polar curve \\(r=3+\\cos\\theta\\).",
     "archetype_id": "BC-QA-09012"
    },
    "not_this": {
     "text": "Find the area of the region between \\(y=3+\\cos x\\), the x-axis, \\(x=0\\) and \\(x=2\\pi\\).",
     "why_not": "It is a region under a graph in x, so the integrand is y."
    },
    "feature": "Rays sweep the region, so the integrand is one half r squared."
   }
  }
 ],
 "worked_examples": [
  {
   "id": "ex-1",
   "archetype_id": "BC-QA-09014",
   "bands": [
    "low",
    "mid"
   ],
   "parameter_draw": {
    "region": "full",
    "trig": "cos",
    "frequency": "1",
    "base": "3",
    "amplitude": "1"
   },
   "problem": {
    "text": "Find the exact area of the region enclosed by the polar curve \\(r=3+\\cos\\theta\\).",
    "command_verb": "find"
   },
   "calculator_status": "no_calculator",
   "steps": [
    {
     "cue": "Cut the region by rays from the pole.",
     "why": "Each ray sweeps a thin sector."
    },
    {
     "cue": "One sector: half r squared times its angle.",
     "why": "A sector of radius r has that area.",
     "expr": "(3 + cos(theta))**2/2",
     "relation": "new"
    },
    {
     "cue": "Add the sectors over one full turn.",
     "why": "r is never 0, so 0 to \\(2\\pi\\) traces it once.",
     "expr": "Integral((3 + cos(theta))**2/2, (theta, 0, 2*pi))",
     "relation": "new"
    },
    {
     "cue": "Expand the square and integrate.",
     "why": "The cosine term integrates to zero over a turn.",
     "expr": "19*pi/2",
     "relation": "evaluate",
     "subs": {}
    }
   ],
   "answer": {
    "form": "symbolic",
    "expr": "19*pi/2"
   }
  },
  {
   "id": "ex-2",
   "archetype_id": "BC-QA-09012",
   "bands": [
    "low"
   ],
   "fade_from": 3,
   "parameter_draw": {
    "shape": "petal",
    "constant": "2",
    "coefficient": "4",
    "frequency": "2",
    "trig": "sin",
    "sweep": "first"
   },
   "problem": {
    "text": "The polar curve \\(r=4\\sin2\\theta\\) is a rose with four petals. Find the exact area of the region enclosed by one petal.",
    "command_verb": "find"
   },
   "calculator_status": "no_calculator",
   "steps": [
    {
     "cue": "One petal lies between zeros of r.",
     "why": "r is 0 where the petal starts and ends.",
     "expr": "4*sin(2*theta) = 0",
     "relation": "new"
    },
    {
     "cue": "Consecutive zeros, 0 and \\(\\pi/2\\).",
     "why": "Both are solutions, and no zero lies between.",
     "expr": "FiniteSet(0, pi/2)",
     "relation": "solve",
     "variable": "theta"
    },
    {
     "cue": "Half the square of r over those angles.",
     "why": "The integral shows the square.",
     "expr": "Integral((4*sin(2*theta))**2/2, (theta, 0, pi/2))",
     "relation": "new",
     "point_type_id": "BC-PT-99048"
    },
    {
     "cue": "Use the double angle identity to integrate.",
     "why": "The exact value has no decimal.",
     "expr": "2*pi",
     "relation": "evaluate",
     "subs": {},
     "point_type_id": "BC-PT-99004"
    }
   ],
   "answer": {
    "form": "symbolic",
    "expr": "2*pi"
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
   "error_id": "BC-ERR-09016",
   "observed_behavior": "A length or an area is computed over an angle or parameter interval that covers the same piece of curve twice.",
   "scoring_consequence": "The reported value is a multiple of the correct one and the answer point is lost.",
   "wrong_step": {
    "text": "Limits 0 to \\(4\\pi\\), the curve traced twice.",
    "expr": "Integral((3 + cos(theta))**2/2, (theta, 0, 4*pi))"
   },
   "right_step": {
    "text": "Limits 0 to \\(2\\pi\\), traced once.",
    "expr": "Integral((3 + cos(theta))**2/2, (theta, 0, 2*pi))"
   },
   "relation": "distinct",
   "fix_prompt": true,
   "possible_reason": null,
   "sources": [
    "BC-ERR-09016"
   ]
  },
  {
   "error_id": "BC-ERR-09035",
   "observed_behavior": "The area integrand is the square of r with no factor of one half.",
   "scoring_consequence": "The value is twice the area, so the answer point is lost; the factor is assessed with the limits (sg-25:7).",
   "wrong_step": {
    "text": "No factor \\(\\tfrac12\\).",
    "expr": "Integral((3 + cos(theta))**2, (theta, 0, 2*pi))"
   },
   "right_step": {
    "text": "With the factor \\(\\tfrac12\\).",
    "expr": "Integral((3 + cos(theta))**2/2, (theta, 0, 2*pi))"
   },
   "relation": "distinct",
   "fix_prompt": true,
   "possible_reason": null,
   "sources": [
    "BC-ERR-09035"
   ]
  },
  {
   "error_id": "BC-ERR-09036",
   "observed_behavior": "The integral is of r with respect to theta rather than of the square of r.",
   "scoring_consequence": "The first point, which requires an integral containing the square of r, is lost (sg-25:7).",
   "wrong_step": {
    "text": "The integral of r.",
    "expr": "Integral(3 + cos(theta), (theta, 0, 2*pi))"
   },
   "right_step": {
    "text": "The integral of half of r squared.",
    "expr": "Integral((3 + cos(theta))**2/2, (theta, 0, 2*pi))"
   },
   "relation": "distinct",
   "fix_prompt": true,
   "possible_reason": {
    "misconception_id": "BC-MIS-09017",
    "text": "transports the Cartesian area formula unchanged"
   },
   "sources": [
    "BC-ERR-09036",
    "BC-MIS-09017"
   ]
  },
  {
   "error_id": "BC-ERR-09037",
   "observed_behavior": "The area integral runs over the angle interval of the figure rather than between the intersection angles of the two curves.",
   "scoring_consequence": "The answer point is lost, since the limits are assessed there (sg-25:7).",
   "wrong_step": {
    "text": "One petal of \\(r=4\\sin2\\theta\\) over 0 to \\(2\\pi\\).",
    "expr": "Integral((4*sin(2*theta))**2/2, (theta, 0, 2*pi))"
   },
   "right_step": {
    "text": "The petal over 0 to \\(\\pi/2\\), consecutive zeros of r.",
    "expr": "Integral((4*sin(2*theta))**2/2, (theta, 0, pi/2))"
   },
   "relation": "distinct",
   "fix_prompt": true,
   "possible_reason": null,
   "sources": [
    "BC-ERR-09037"
   ]
  }
 ],
 "representations": {
  "text": "Sector sums \\(\\sum\\tfrac12r^2\\,\\Delta\\theta\\) for \\(r=3+\\cos\\theta\\) from \\(\\theta=0\\) to \\(\\theta=\\pi/2\\) settle on one value as the sectors thin.",
  "figure": {
   "kind": "numeric_experiment"
  }
 },
 "prerequisite_bridges": [
  {
   "prq_id": "BC-PRQ-06005",
   "text": "Integrands are functions of \\(\\theta\\)."
  },
  {
   "prq_id": "BC-PRQ-08006",
   "text": "Three decimal places."
  },
  {
   "prq_id": "BC-PRQ-09002",
   "text": "Sine and cosine at bounding angles."
  },
  {
   "prq_id": "BC-PRQ-09004",
   "text": "Angles that trace the region once."
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
   "archetype_id": "BC-QA-09014",
   "parameter_draw": {
    "region": "full",
    "trig": "cos",
    "frequency": "1",
    "base": "3",
    "amplitude": "1"
   },
   "completes": "ex-1",
   "stem": {
    "text": "The area enclosed by \\(r=3+\\cos\\theta\\) is \\(\\int_0^{2\\pi}\\tfrac12(3+\\cos\\theta)^2\\,d\\theta\\). Find its exact value.",
    "command_verb": "find"
   },
   "key": {
    "form": "symbolic",
    "expr": "19*pi/2"
   },
   "steps": [
    {
     "text": "Integral.",
     "expr": "Integral((3 + cos(theta))**2/2, (theta, 0, 2*pi))",
     "relation": "new"
    },
    {
     "text": "Integrate.",
     "expr": "19*pi/2",
     "relation": "evaluate",
     "subs": {}
    }
   ],
   "calculator_status": "no_calculator",
   "skills": [
    "BC-SKL-09038"
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
   "archetype_id": "BC-QA-09014",
   "parameter_draw": {
    "region": "quarter",
    "trig": "cos",
    "frequency": "1",
    "base": "5",
    "amplitude": "2"
   },
   "stem": {
    "text": "Find the exact area of the region bounded by \\(r=5+2\\cos\\theta\\) and the rays \\(\\theta=0\\) and \\(\\theta=\\pi/2\\).",
    "command_verb": "find"
   },
   "key": {
    "form": "symbolic",
    "expr": "10 + 27*pi/4"
   },
   "steps": [
    {
     "text": "Integral.",
     "expr": "Integral((5 + 2*cos(theta))**2/2, (theta, 0, pi/2))",
     "relation": "new"
    },
    {
     "text": "Integrate.",
     "expr": "10 + 27*pi/4",
     "relation": "evaluate",
     "subs": {}
    }
   ],
   "calculator_status": "no_calculator",
   "skills": [
    "BC-SKL-09035"
   ]
  },
  {
   "id": "chk-3",
   "check_kind": "mcq",
   "format": "mcq",
   "bands": [
    "low"
   ],
   "archetype_id": "BC-QA-09014",
   "parameter_draw": {
    "region": "half",
    "trig": "sin",
    "frequency": "1",
    "base": "4",
    "amplitude": "1"
   },
   "stem": {
    "text": "The exact area of the region bounded by \\(r=4+\\sin\\theta\\) and the rays \\(\\theta=0\\) and \\(\\theta=\\pi\\) is",
    "command_verb": "identify"
   },
   "key": {
    "form": "symbolic",
    "expr": "8 + 33*pi/4"
   },
   "steps": [
    {
     "text": "Integral.",
     "expr": "Integral((4 + sin(theta))**2/2, (theta, 0, pi))",
     "relation": "new"
    },
    {
     "text": "Integrate.",
     "expr": "8 + 33*pi/4",
     "relation": "evaluate",
     "subs": {}
    }
   ],
   "options": [
    {
     "id": "A",
     "is_key": false,
     "label": "\\(16+\\tfrac{33\\pi}{2}\\)",
     "expr": "16 + 33*pi/2",
     "error_path": "BC-ERR-09035",
     "derivation": "the integral without the factor one half, twice the area"
    },
    {
     "id": "B",
     "is_key": true,
     "label": "\\(8+\\tfrac{33\\pi}{4}\\)",
     "expr": "8 + 33*pi/4",
     "error_path": null
    },
    {
     "id": "C",
     "is_key": false,
     "label": "\\(2+4\\pi\\)",
     "expr": "2 + 4*pi",
     "error_path": "BC-ERR-09036",
     "derivation": "the integral of r with no square"
    },
    {
     "id": "D",
     "is_key": false,
     "label": "\\(\\tfrac{33\\pi}{2}\\)",
     "expr": "33*pi/2",
     "error_path": "BC-ERR-09037",
     "derivation": "the limits of the whole figure, 0 to 2 pi"
    }
   ],
   "calculator_status": "no_calculator",
   "skills": [
    "BC-SKL-09036"
   ]
  }
 ],
 "delivery": [
  {
   "block": "orientation",
   "mode": "figure",
   "reason": "rule 4: BC-REP-13 and BC-REP-02 on BC-SKL-09036 and BC-SKL-09037; not promoted, the stem asks for an area, not a reading of a varying quantity",
   "sources": [
    "BC-SKL-09036",
    "BC-SKL-09037"
   ],
   "spec": {
    "kind": "polar_region",
    "representations": [
     "BC-REP-13",
     "BC-REP-02"
    ],
    "curves": [
     {
      "r": "3 + cos(theta)",
      "domain": [
       "0",
       "2*pi"
      ]
     }
    ],
    "shaded": "the region enclosed by the curve, with one thin sector drawn between two rays",
    "labels": [
     {
      "text": "r = 3 + cos θ",
      "placement": "inside"
     },
     {
      "text": "thin sector, angle dθ",
      "placement": "inside"
     },
     {
      "text": "pole",
      "placement": "inside"
     }
    ]
   },
   "fallback": "the same figure static, region shaded and one sector drawn, labelled inside",
   "keyboard": "no control; the figure description is reached with Tab"
  },
  {
   "block": "ki-1",
   "mode": "motion",
   "reason": "rule 2: a region swept by rays from the pole, each thin sector filling the area as the angle advances; rule 4 (README rule 3), BC-REP-13 on BC-SKL-09036, for the static fallback",
   "sources": [
    "BC-SKL-09036",
    "BC-SKL-09037"
   ],
   "spec": {
    "kind": "polar_sweep",
    "representations": [
     "BC-REP-13",
     "BC-REP-02"
    ],
    "curves": [
     {
      "r": "3 + cos(theta)",
      "domain": [
       "0",
       "2*pi"
      ]
     }
    ],
    "frames": [
     {
      "theta": "0"
     },
     {
      "theta": "pi/2"
     },
     {
      "theta": "pi"
     },
     {
      "theta": "3*pi/2"
     },
     {
      "theta": "2*pi"
     }
    ],
    "drawn": [
     "the ray at the frame's angle",
     "the sectors filled up to that ray"
    ],
    "labels": [
     {
      "text": "θ, the angle swept",
      "placement": "inside"
     },
     {
      "text": "area so far",
      "placement": "inside"
     },
     {
      "text": "r = 3 + cos θ",
      "placement": "inside"
     }
    ]
   },
   "fallback": "five frames side by side, static, each with its three labels inside",
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
   "block": "err-BC-ERR-09016",
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
   "block": "err-BC-ERR-09036",
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
   "block": "representations",
   "mode": "model",
   "reason": "template model row: the meaning is a computed sequence of sector sums at a growing number of sectors, and BC-QA-09014 carries BC-DF-15 (BC-CON-09015 is a productive-failure target)",
   "sources": [
    "BC-QA-09014"
   ],
   "spec": {
    "kind": "numeric_experiment",
    "representations": [
     "BC-REP-13",
     "BC-REP-03"
    ],
    "curve": "3 + cos(theta)",
    "from": "0",
    "to": "pi/2",
    "n_values": [
     1,
     2,
     4,
     16,
     64,
     256
    ],
    "computed": "sum over i of (1/2)*(3 + cos(i*dt))**2*dt with dt = (pi/2)/n",
    "rows": [
     [
      1,
      12.566
     ],
     [
      2,
      11.68
     ],
     [
      4,
      11.11
     ],
     [
      16,
      10.631
     ],
     [
      64,
      10.504
     ],
     [
      256,
      10.472
     ]
    ],
    "columns": [
     "sectors n",
     "sum of sector areas"
    ],
    "labels": [
     {
      "text": "sectors n",
      "placement": "inside"
     },
     {
      "text": "sums approach the integral 10.461",
      "placement": "inside"
     }
    ]
   },
   "fallback": "the six computed rows printed as a static table with the closing label",
   "keyboard": "a Run control reached by Tab and pressed with Enter or Space adds one row per press; the table is read in row order"
  }
 ],
 "refresher": [
  "ki-1",
  "err-BC-ERR-09016",
  "err-BC-ERR-09035",
  "err-BC-ERR-09036",
  "err-BC-ERR-09037",
  "ex-1"
 ],
 "research_lines": [
  {
   "file": "research/units/unit-09-parametric-polar-vector.md",
   "line": "The one half and the square of r are both part of the integrand"
  }
 ],
 "inferred": [
  {
   "claim": "A fluent solver writes the integral with its limits and the value, and holds the cutting into sectors.",
   "settles": "Per-step timing from the fluency telemetry."
  },
  {
   "claim": "ex-1 is drawn from BC-QA-09014 because it is the exact, no calculator shape whose path begins by cutting the region into sectors; the ex-1 scoring entry is empty because BC-PT-99048's line does not fit the brief band beside the prediction and the contrast pair.",
   "settles": "A brief cap that admits the scoring line."
  },
  {
   "claim": "The sector sum table covers the quarter sweep of the ex-1 curve, because the full turn of a periodic integrand is exact at 4 sectors and would show no approach.",
   "settles": "The modality A/B in the build plan, skip rate and time to first credited success by mode."
  },
  {
   "claim": "BC-ERR-09037 is shown on ex-2's petal, the pairing the BC-QA-09012 generator uses; its record text names two curves, which a single curve draw does not have.",
   "settles": "A BC-ERR record for the single curve limits mistake."
  }
 ],
 "sources": [
  "BC-CON-09015",
  "BC-SKL-09035",
  "BC-SKL-09036",
  "BC-SKL-09037",
  "BC-SKL-09038",
  "BC-EK-CHA-5D1",
  "ced:178",
  "BC-QA-09012",
  "BC-QA-09014",
  "BC-PT-99048",
  "BC-PT-99004",
  "BC-PT-99001",
  "BC-PT-99005",
  "BC-ERR-09016",
  "BC-ERR-09035",
  "BC-ERR-09036",
  "BC-ERR-09037",
  "BC-MIS-09017",
  "BC-MIS-09007",
  "BC-MIS-08019",
  "BC-PRQ-06005",
  "BC-PRQ-08006",
  "BC-PRQ-09002",
  "BC-PRQ-09004",
  "sg-25:7",
  "sg-25:8",
  "BC-FRQ-2019-Q2-A",
  "BC-FRQ-2019-Q2-C",
  "BC-FRQ-2019-Q2-D",
  "BC-FRQ-2026-Q2-A",
  "BC-MCQ-CED-021",
  "research/units/unit-09-parametric-polar-vector.md#9.8 Find the Area of a Polar Region or the Area Bounded by a Single Polar Curve",
  "research/question-analysis/question-archetypes.md#BC-QA-09012 Area of a region bounded by a single polar curve",
  "research/question-analysis/question-archetypes.md#BC-QA-09014 Area of a polar region found before the polar area integral is taught",
  "research/scoring/common-point-losses.md#Setup points",
  "research/exam/exam-structure.md#Section and part layout"
 ],
 "word_count": {
  "full": 789,
  "brief": 447
 },
 "read_minutes": {
  "full": 5.3,
  "brief": 3.0
 }
}
```
