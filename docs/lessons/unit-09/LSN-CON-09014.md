---
title: LSN-CON-09014 Slope of a polar curve in the plane
research_date: 2026-09-29
status: designed
purpose: Authoring spec for the concept lesson on BC-CON-09014, the slope of the tangent line to a polar curve as the quotient of the derivatives of y and x with respect to theta, and the point farthest from an axis, built from authoring_bundle("BC-CON-09014") and the research files it cites, so an author fills plan 15's lesson record without making a teaching decision.
---

# LSN-CON-09014 Slope of a polar curve in the plane

Concept BC-CON-09014 (skills BC-SKL-09033 and BC-SKL-09034), topic 9.7 of Unit 9, BC only (ced:177), loaded by six archetypes: BC-QA-99003, 99001, 99002, 09009 and 99006 (skill 09033) and BC-QA-09011 (skill 09034). Hard parents in Unit 9: BC-CON-09002, 09012 and 09013; outside hard parents BC-SKL-02036 and 05028 (docs/lessons/unit-09/README.md, section 1), so the product rule and the candidates test are assumed.

## Prediction

Served first, both bands: an `mcq` on ex-1's own curve \(r=5+2\cos2\theta\) at \(\theta=\pi/3\), where \(dr/d\theta=-2\sqrt3\), asking what gives the slope of the tangent line. Key C, \(dy/d\theta\) divided by \(dx/d\theta\). Distractors: A the rate of r itself (BC-MIS-09015), B the tangent of the angle, which is the slope of the radial line. Only C is true. It is answerable before the rule: the slope is a rate of y against x, and y and x are r times sine and cosine. The resolution states the quotient and what dr/dtheta measures, with no verdict. Source: BC-CON-09014 and the topic section the key idea cites.

## Orientation

Served text, from BC-CON-09014 `description_plain` ("write x and y in theta, then take the quotient of their rates") and the topic's Assessment behaviour paragraph (research/units/unit-09-parametric-polar-vector.md#9.7 Defining Polar Coordinates and Differentiating in Polar Form): a response shows both rates and the quotient, and the justification variants ask for the global argument behind an extreme coordinate. No count, no frequency.

## Key ideas

Both skills map to one essential knowledge statement, BC-EK-FUN-3G2 (ced:177): one core block, both bands.

- ki-1 (core). Paraphrase of the Required mathematical knowledge paragraphs Polar to Cartesian, Meaning of dr/dtheta (which is a rate of distance, not the slope) and Extreme coordinate (a point farthest from the y-axis is where x is largest: dx/dtheta equal to zero and a comparison of candidates; a local argument alone did not earn the justification point, sg-25:9). Notation line, the concept's `notation`. No anchor quote: the FUN-3.G.2 sentence on ced:177 is a list of derivatives that can give information, and adds nothing the paraphrase lacks.

## Recognition

BC-QA-99003 (research/question-analysis/question-archetypes.md#BC-QA-99003 Slope of the tangent line to a polar curve at a stated angle) carries the slope, BC-QA-09011 (research/question-analysis/question-archetypes.md#BC-QA-09011 Point on a polar curve farthest from a coordinate axis) the farthest point; BC-QA-99001, 99002, 09009 and 99006 also load BC-SKL-09033.

- BC-QA-99003 `common_givens`: "a polar equation", "a figure showing the curve", "a stated angle". `asked_to_produce`: both Cartesian coordinates in the angle, both derivatives, the quotient. `typical_wording`: "find the slope of the line tangent to the graph of the polar curve at a stated angle". Official example BC-FRQ-2018-Q5-B; no scoring guideline for 2018 is in the corpus, so the archetype carries no point types.
- BC-QA-09011 `asked_to_produce`: "an equation for the critical angle", "a global justification", "the angle". `typical_wording`: "find the value of the angle that corresponds to the point on the curve farthest from the named axis, and justify the answer". Official example BC-FRQ-2025-Q2-C.
- BC-QA-99001 (BC-FRQ-2026-Q2-B) solves the same quotient for dx/dtheta from a supplied slope; BC-QA-99002 (BC-FRQ-2014-Q2-B) asks for one derivative alone.
- The signal in the stem: the words slope or tangent line with a polar equation; or farthest from an axis.

The near miss of the contrast pair is a stem of BC-QA-09009: the same curve at the same angle asking for the rate of change of r, which is a derivative and not a slope (`common_distractors` "dy/dx at the same angle" runs the other way). What says "not this concept": a rate of change of r or a distance from the origin (BC-CON-09013); a rate in time (BC-CON-09013's chain rule product); an x and y pair given in a parameter t (BC-CON-09002).

## Method choice

- st-1, BC-QA-99003, both bands. Cue from `common_givens` and `asked_to_produce`. Method, `expected_solution_path[0]` and the entries that follow: write x and y as r times cosine and sine, differentiate, and divide. Rival, `prohibited_shortcuts`: reporting the derivative of the radial function as the slope. Separating feature: the slope is a rate of y against x. The block carries the contrast pair.
- st-2, BC-QA-09011, low band. Method, `expected_solution_path[0]` to `[2]`: the coordinate in theta, its derivative set to zero, every candidate compared. Rival, `wrong_approaches`: a first or second derivative test as the whole justification. Separating feature: both endpoints and the critical angle are compared.
- Both archetypes carry `asked_to_produce` and `common_givens`, so neither block is tagged inferred. No served field opens with the reader's own label.

## Solution path

- ex-1, BC-QA-99003, both bands, no calculator. Draw: constant 5, amplitude 2, sign 1, trig cos, angle_turns 1/3; \(r=5+2\cos2\theta\) at \(\theta=\pi/3\). Chain: y (`new`), \(dy/d\theta\) (`differentiate`), x (`new`), \(dx/d\theta\) (`differentiate`), the quotient (`new`), the value \(\tfrac{\sqrt3}{9}\) (`evaluate`, \(\theta=\pi/3\)). \(dy/d\theta=-1\), \(dx/d\theta=-3\sqrt3\). No published item on BC-QA-99003 carries this draw (content/items_gen_unit09/ITM-GEN-99003-00 to 04; the agent items ITM-AGT-99003 in content/items_unit09_agent carry a parameter_draw of another shape, a polar equation and an angle).
- ex-2, BC-QA-09011, low band, calculator, faded from step 3. Draw: constant 4, amplitude 3, start 1/5, end 19/10, axis y-axis, presentation equation; \(r=4+3\sin\theta\) on \(0.2\le\theta\le1.9\), \(x=r\cos\theta\). The critical angle is \(\arcsin\frac{\sqrt{22}-2}{6}=0.46498\), reported 0.465; \(|x|\) is 4.504, 4.778 and 2.211 at 0.2, 0.465 and 1.9. Steps 1 and 2 (the coordinate and its derivative) are shown, the student writes the equation, the angle and the comparison, then steps 3 to 5 reveal. No published item on BC-QA-09011 carries this draw (content/items_gen_unit09/ITM-GEN-09011-00 to 21).
- A fluent solver writes both rates, the quotient and the value; the recognition and the rewriting of x and y are held (docs/lessons/unit-09/README.md, section 5) [inferred]. No productive-failure target: BC-CON-09015 is the unit's target.

## Scoring

BC-QA-99003 has no `point_types`, so ex-1 carries no tag and no scoring line; the slope point BC-PT-99049 (the chain relation among the derivatives, sg-26:7, sg-23:7) is taught in ki-1 and carried by BC-QA-99001 and BC-QA-09009 (inferred array). ex-2 is on BC-QA-09011, which lists BC-PT-99013, 99011, 99005: it tags BC-PT-99013 on the solved equation and BC-PT-99011 on the comparison. BC-PT-99005 is untagged, the answer with supporting work. The lines are `reader_checks` output.

Point losses from research: a local argument where a global one is required (BC-ERR-99004; research/scoring/common-point-losses.md#Justification points, crabbc-25:30); presenting only the solved critical value earns neither of the first two points (sg-25:8, sg-25:9).

## Traps

Six errors meet the skills, in bundle order: BC-ERR-09031, 09032, 99004, 99031, then 05028 and 09034, which fall past the cap of 4. Low band all four, mid band the first two. All carry `fix_prompt` true, since each pair is distinct.

- err-BC-ERR-09031: on ex-1's draw, \(dr/d\theta=-2\sqrt3\) reported against the slope \(\tfrac{\sqrt3}{9}\). Possible reason, BC-MIS-09015.
- err-BC-ERR-09032: on ex-1's draw, \(dy/d\theta\) as \(r'\sin\theta\) against the product rule form.
- err-BC-ERR-99004: on ex-2's draw, the comparison of one angle against the three candidates. Possible reason, BC-MIS-05018.
- err-BC-ERR-99031: the record covers polar area, limits, a rate in time and the derivative of r; the clause used is differentiating the polar radius incorrectly, shown as the chain factor dropped from \(-4\sin2\theta\) on ex-1's draw. No possible reason line.

## Representations

None as a separate block. The topic's Representations paragraph names a plotted polar curve converted to a statement about a tangent (BC-REP-02 to BC-REP-04); the unit README delivers it as a figure on the orientation and the key idea (docs/lessons/unit-09/README.md, section 6).

## Prerequisite bridge

- BC-PRQ-08001 and BC-PRQ-09002, each from its `description_plain` and `failure_signature`.

## Time

ex-1 is the no calculator MCQ shape of BC-QA-99003, Section I Part A, 2.14 minutes (research/exam/exam-structure.md#Section and part layout). ex-2 is the calculator shape of BC-QA-09011: Section I Part B, 2.92 minutes, or a 3 point free response part, 5.0 minutes (docs/lessons/unit-09/README.md, section 5). A fluent solver writes both rates, the quotient and the value; the evaluation is held.

## Checks

- chk-1, completion of ex-1, both bands: \(dy/d\theta\) and \(dx/d\theta\) are given and the slope asked. Key \(\tfrac{\sqrt3}{9}\).
- chk-2, isomorph, both bands, no calculator. Draw: constant 3, amplitude 2, sign 1, trig cos, angle_turns 2/3; \(r=3+2\cos2\theta\) at \(\theta=2\pi/3\); \(dy/d\theta=2\), \(dx/d\theta=-2\sqrt3\). Key \(-\tfrac{\sqrt3}{3}\).
- chk-3, MCQ, low band, no calculator. Draw: constant 6, amplitude 2, sign -1, trig cos, angle_turns 2/3; \(r=6-2\cos2\theta\) at \(\theta=2\pi/3\); \(dy/d\theta=-\tfrac{13}{2}\), \(dx/d\theta=-\tfrac{5\sqrt3}{2}\). Key \(\tfrac{13\sqrt3}{15}\). Distractors: \(-2\sqrt3\), \(dr/d\theta\) (BC-ERR-09031); \(-\sqrt3\), the tangent of the angle from \(r'\) times the trigonometric factor only (BC-ERR-09032); \(\tfrac{5\sqrt3}{9}\), \(dr/d\theta\) with the chain factor dropped (BC-ERR-99031).

## Delivery

- orientation, ki-1: figure. Rule 4 (README rule 3): BC-REP-13 on BC-SKL-09033 and 09034; not promoted, the stem asks for a slope value or a justified angle. The orientation draws the radial segment beside the tangent line at \(\theta=\pi/3\); ki-1 marks the three candidates of ex-2's curve (docs/lessons/unit-09/README.md, section 6).
- ex-1, ex-2, the four error blocks: step_reveal. Rule 1.

## Band plan

- Low (full): prediction, orientation, bridges, ki-1, st-1 with the contrast pair, st-2, ex-1, chk-1, the four error blocks, ex-2 (faded from step 3) and its lines, chk-2, chk-3. 830 words, 5.6 minutes.
- Mid (brief): prediction, orientation, bridges, ki-1, st-1 with the contrast pair, ex-1, chk-1, err-BC-ERR-09031, err-BC-ERR-09032, chk-2. 397 words, 2.7 minutes.
- Refresher: ki-1, the four error blocks, ex-1.

## Sources

- BC-CON-09014; BC-SKL-09033, BC-SKL-09034; BC-EK-FUN-3G2; ced:177
- BC-QA-99003, BC-QA-09011, BC-QA-09009; BC-FRQ-2018-Q5-B, BC-FRQ-2025-Q2-C
- BC-PT-99013, BC-PT-99011, BC-PT-99049
- BC-ERR-09031, BC-ERR-09032, BC-ERR-99004, BC-ERR-99031; BC-MIS-09015, BC-MIS-05018
- BC-PRQ-08001, BC-PRQ-09002
- sg-25:7, sg-25:9
- research/units/unit-09-parametric-polar-vector.md#9.7 Defining Polar Coordinates and Differentiating in Polar Form
- research/question-analysis/question-archetypes.md#BC-QA-99003 Slope of the tangent line to a polar curve at a stated angle
- research/question-analysis/question-archetypes.md#BC-QA-09011 Point on a polar curve farthest from a coordinate axis
- research/scoring/common-point-losses.md#Justification points
- research/exam/exam-structure.md#Section and part layout
- [inferred] The held steps; the untagged slope point; the reading of BC-ERR-99031; the timing of ex-2. Each settled as the inferred array states.

## Machine record

```json
{
 "id": "LSN-CON-09014",
 "kind": "concept",
 "target_id": "BC-CON-09014",
 "unit": "09",
 "skills": [
  "BC-SKL-09033",
  "BC-SKL-09034"
 ],
 "prediction": {
  "id": "pr-1",
  "stem": {
   "text": "On \\(r=5+2\\cos2\\theta\\), \\(dr/d\\theta=-2\\sqrt3\\) at \\(\\theta=\\pi/3\\). Predict what gives the slope of the tangent line there.",
   "command_verb": "predict"
  },
  "format": "mcq",
  "options": [
   {
    "id": "A",
    "label": "\\(dr/d\\theta\\), so the slope is \\(-2\\sqrt3\\)",
    "is_key": false
   },
   {
    "id": "B",
    "label": "\\(\\tan(\\pi/3)\\), so the slope is \\(\\sqrt3\\)",
    "is_key": false
   },
   {
    "id": "C",
    "label": "\\(dy/d\\theta\\) divided by \\(dx/d\\theta\\)",
    "is_key": true
   }
  ],
  "resolution": "With \\(x=r\\cos\\theta\\) and \\(y=r\\sin\\theta\\), the slope is \\(\\frac{dy/d\\theta}{dx/d\\theta}\\). The rate of r alone measures the distance from the origin, not the slope.",
  "sources": [
   "BC-CON-09014",
   "research/units/unit-09-parametric-polar-vector.md#9.7 Defining Polar Coordinates and Differentiating in Polar Form"
  ]
 },
 "orientation": {
  "text": "The slope of a polar curve is \\(\\frac{dy/d\\theta}{dx/d\\theta}\\), with \\(x=r\\cos\\theta\\) and \\(y=r\\sin\\theta\\). A response shows both rates and the quotient. A farthest point sets one coordinate's derivative to zero and compares candidates.",
  "sources": [
   "BC-CON-09014",
   "research/units/unit-09-parametric-polar-vector.md#9.7 Defining Polar Coordinates and Differentiating in Polar Form"
  ]
 },
 "key_ideas": [
  {
   "id": "ki-1",
   "ek_id": "BC-EK-FUN-3G2",
   "depth": "core",
   "text": "On a polar curve, \\(x=r\\cos\\theta\\) and \\(y=r\\sin\\theta\\), so \\(\\frac{dy}{dx}=\\frac{dy/d\\theta}{dx/d\\theta}\\), with the product rule in each rate. It is not \\(dr/d\\theta\\). The point farthest from an axis sets that coordinate's derivative to zero, then compares every candidate, endpoints included.",
   "notation": "dy/dx for a polar curve",
   "quote": null,
   "sources": [
    "BC-EK-FUN-3G2",
    "ced:177",
    "sg-25:9",
    "research/units/unit-09-parametric-polar-vector.md#9.7 Defining Polar Coordinates and Differentiating in Polar Form"
   ]
  }
 ],
 "strategy": [
  {
   "id": "st-1",
   "archetype_id": "BC-QA-99003",
   "cue": "A polar equation, a stated angle, the slope of the tangent line.",
   "method": "\\(x=r\\cos\\theta\\), \\(y=r\\sin\\theta\\), then \\(\\frac{dy/d\\theta}{dx/d\\theta}\\) at the angle.",
   "rival": "Reporting \\(dr/d\\theta\\) as the slope.",
   "separating_feature": "A slope is a rate of y against x, not of r.",
   "sources": [
    "BC-QA-99003"
   ],
   "evidence_tag": "verified",
   "contrast": {
    "this": {
     "text": "Find the slope of the line tangent to the polar curve \\(r=5+2\\cos2\\theta\\) at \\(\\theta=\\pi/3\\).",
     "archetype_id": "BC-QA-99003"
    },
    "not_this": {
     "text": "Find the rate of change of r with respect to \\(\\theta\\) on \\(r=5+2\\cos2\\theta\\) at \\(\\theta=\\pi/3\\).",
     "why_not": "It asks how the distance from the origin changes, not a slope."
    },
    "feature": "The tangent line's slope, not the rate of r."
   }
  },
  {
   "id": "st-2",
   "archetype_id": "BC-QA-09011",
   "cue": "The point farthest from an axis, with a justification.",
   "method": "The coordinate in \\(\\theta\\), its derivative set to 0, then every candidate compared.",
   "rival": "A sign change at one angle as the whole justification.",
   "separating_feature": "Both endpoints and the critical angle are compared.",
   "sources": [
    "BC-QA-09011"
   ],
   "evidence_tag": "verified"
  }
 ],
 "worked_examples": [
  {
   "id": "ex-1",
   "archetype_id": "BC-QA-99003",
   "bands": [
    "low",
    "mid"
   ],
   "parameter_draw": {
    "constant": "5",
    "amplitude": "2",
    "sign": "1",
    "trig": "cos",
    "angle_turns": "1/3"
   },
   "problem": {
    "text": "For the polar curve \\(r=5+2\\cos2\\theta\\), find the slope of the line tangent to the curve at \\(\\theta=\\pi/3\\).",
    "command_verb": "find"
   },
   "calculator_status": "no_calculator",
   "steps": [
    {
     "cue": "Slope in the plane: write y in \\(\\theta\\).",
     "why": "\\(y=r\\sin\\theta\\).",
     "expr": "(5 + 2*cos(2*theta))*sin(theta)",
     "relation": "new"
    },
    {
     "cue": "Product rule; chain rule inside r.",
     "why": "This is \\(dy/d\\theta\\).",
     "expr": "-4*sin(2*theta)*sin(theta) + (5 + 2*cos(2*theta))*cos(theta)",
     "relation": "differentiate",
     "variable": "theta"
    },
    {
     "cue": "Now x in \\(\\theta\\).",
     "why": "\\(x=r\\cos\\theta\\).",
     "expr": "(5 + 2*cos(2*theta))*cos(theta)",
     "relation": "new"
    },
    {
     "cue": "Same rules.",
     "why": "This is \\(dx/d\\theta\\).",
     "expr": "-4*sin(2*theta)*cos(theta) - (5 + 2*cos(2*theta))*sin(theta)",
     "relation": "differentiate",
     "variable": "theta"
    },
    {
     "cue": "Quotient of the two rates.",
     "why": "\\(dy/dx=\\frac{dy/d\\theta}{dx/d\\theta}\\).",
     "expr": "(-4*sin(2*theta)*sin(theta) + (5 + 2*cos(2*theta))*cos(theta))/(-4*sin(2*theta)*cos(theta) - (5 + 2*cos(2*theta))*sin(theta))",
     "relation": "new"
    },
    {
     "cue": "Evaluate at \\(\\theta=\\pi/3\\).",
     "why": "Exact values, no decimals.",
     "expr": "sqrt(3)/9",
     "relation": "evaluate",
     "subs": {
      "theta": "pi/3"
     }
    }
   ],
   "answer": {
    "form": "symbolic",
    "expr": "sqrt(3)/9"
   }
  },
  {
   "id": "ex-2",
   "archetype_id": "BC-QA-09011",
   "bands": [
    "low"
   ],
   "fade_from": 3,
   "parameter_draw": {
    "constant": "4",
    "amplitude": "3",
    "start": "1/5",
    "end": "19/10",
    "axis": "y-axis",
    "presentation": "equation"
   },
   "problem": {
    "text": "Consider \\(r=4+3\\sin\\theta\\) for \\(0.2\\le\\theta\\le1.9\\). Using a calculator, find \\(\\theta\\) at the point farthest from the y-axis. Justify your answer.",
    "command_verb": "find"
   },
   "calculator_status": "calculator",
   "steps": [
    {
     "cue": "Distance from the y-axis is \\(|x|\\).",
     "why": "\\(x=r\\cos\\theta\\).",
     "expr": "(4 + 3*sin(theta))*cos(theta)",
     "relation": "new"
    },
    {
     "cue": "Differentiate x.",
     "why": "A farthest point is a critical point or an endpoint.",
     "expr": "3*cos(theta)**2 - (4 + 3*sin(theta))*sin(theta)",
     "relation": "differentiate",
     "variable": "theta"
    },
    {
     "cue": "Set \\(dx/d\\theta=0\\) and solve.",
     "why": "The equation must be written.",
     "expr": "asin((sqrt(22) - 2)/6)",
     "relation": "solve",
     "variable": "theta",
     "point_type_id": "BC-PT-99013"
    },
    {
     "cue": "Keep the exact angle until the last line.",
     "why": "Three places.",
     "expr": "0.465",
     "relation": "evaluate",
     "subs": {},
     "approx": true
    },
    {
     "cue": "Compare \\(|x|\\) at 0.2, 0.465 and 1.9.",
     "why": "About 4.504, 4.778 and 2.211: a global argument.",
     "point_type_id": "BC-PT-99011"
    }
   ],
   "answer": {
    "form": "numeric",
    "expr": "0.465"
   }
  }
 ],
 "what_a_reader_scores": [
  {
   "example_id": "ex-2",
   "point_type_ids": [
    "BC-PT-99013",
    "BC-PT-99011"
   ],
   "lines": [
    {
     "point_type_id": "BC-PT-99013",
     "text": "Considers the derivative set equal to zero. Earned by: Presenting the equation derivative equals zero, or an equivalent equation, or discussing the sign change of the derivative, or using the phrase critical points of the function (sg-25:5, sg-26:17). Not earned by: Presenting only the solved critical value, which sg-25:5, sg-25:9, sg-26:17 and sg-25:19 all state is not sufficient."
    },
    {
     "point_type_id": "BC-PT-99011",
     "text": "Justification by candidates test. Earned by: A global argument that evaluates the function at every interior critical point and at both endpoints, with the evaluations correct to the stated precision (sg-25:5, sg-25:19). Not earned by: A candidates table missing an endpoint (sg-23:15), containing an evaluation error (sg-23:15), or listing extra x-values (sg-25:19). Precision: sg-25:5 and sg-25:9 require candidate evaluations correct to the first digit after the decimal, rounded or truncated; sg-22:5 allows up to three decimals or correctly rounded integers."
    }
   ]
  }
 ],
 "common_errors": [
  {
   "error_id": "BC-ERR-09031",
   "observed_behavior": "The response reports the derivative of r where the slope of the tangent line in the plane was requested.",
   "scoring_consequence": "The slope point is lost.",
   "wrong_step": {
    "text": "\\(dr/d\\theta\\) reported as the slope.",
    "expr": "-2*sqrt(3)"
   },
   "right_step": {
    "text": "\\(dy/d\\theta\\) over \\(dx/d\\theta\\).",
    "expr": "sqrt(3)/9"
   },
   "relation": "distinct",
   "fix_prompt": true,
   "possible_reason": {
    "misconception_id": "BC-MIS-09015",
    "text": "transfers the single variable pattern that the derivative of the given function is the slope"
   },
   "sources": [
    "BC-ERR-09031",
    "BC-MIS-09015"
   ]
  },
  {
   "error_id": "BC-ERR-09032",
   "observed_behavior": "The derivative of a Cartesian coordinate in polar form is taken as the product of the two derivatives or of one derivative alone.",
   "scoring_consequence": "The derivative and everything built from it are wrong.",
   "wrong_step": {
    "text": "\\(dy/d\\theta=r'\\sin\\theta\\).",
    "expr": "-4*sin(2*theta)*sin(theta)"
   },
   "right_step": {
    "text": "\\(dy/d\\theta=r'\\sin\\theta+r\\cos\\theta\\).",
    "expr": "-4*sin(2*theta)*sin(theta) + (5 + 2*cos(2*theta))*cos(theta)"
   },
   "relation": "distinct",
   "fix_prompt": true,
   "possible_reason": null,
   "sources": [
    "BC-ERR-09032"
   ]
  },
  {
   "error_id": "BC-ERR-99004",
   "observed_behavior": "Responses justify an absolute maximum or minimum on a closed interval by a sign change at one point, or run an incomplete candidates test that omits an endpoint or an interior critical point.",
   "scoring_consequence": "The justification point for the absolute extremum is not earned; the answer point may still be available.",
   "wrong_step": {
    "text": "A sign change at 0.465 as the whole argument.",
    "expr": "FiniteSet(0.465)"
   },
   "right_step": {
    "text": "\\(|x|\\) compared at 0.2, 0.465 and 1.9.",
    "expr": "FiniteSet(0.2, 0.465, 1.9)"
   },
   "relation": "distinct",
   "fix_prompt": true,
   "possible_reason": {
    "misconception_id": "BC-MIS-05018",
    "text": "treats a first or second derivative test as a proof that the extremum is the largest or smallest on the whole interval"
   },
   "sources": [
    "BC-ERR-99004",
    "BC-MIS-05018"
   ]
  },
  {
   "error_id": "BC-ERR-99031",
   "observed_behavior": "Responses omit the square on the polar radius in an area integrand, choose limits of integration that do not correspond to the intersection angles, differentiate the polar radius incorrectly, or form the chain rule product for a rate with respect to time from the wrong pair of derivatives.",
   "scoring_consequence": "The integrand point is lost when the square is missing, and later points in the part are typically unreachable.",
   "wrong_step": {
    "text": "\\(dr/d\\theta\\) without the chain factor.",
    "expr": "-2*sin(2*theta)"
   },
   "right_step": {
    "text": "\\(dr/d\\theta\\) with the chain factor.",
    "expr": "-4*sin(2*theta)"
   },
   "relation": "distinct",
   "fix_prompt": true,
   "possible_reason": null,
   "sources": [
    "BC-ERR-99031"
   ]
  }
 ],
 "representations": null,
 "prerequisite_bridges": [
  {
   "prq_id": "BC-PRQ-08001",
   "text": "Set two expressions equal and keep every solution."
  },
  {
   "prq_id": "BC-PRQ-09002",
   "text": "Sine and cosine as coordinates on a circle."
  }
 ],
 "time": {
  "exam_part": "I-A",
  "budget_minutes": 2.14,
  "source": "research/exam/exam-structure.md#Section and part layout",
  "written_steps": {
   "ex-1": [
    2,
    4,
    5,
    6
   ]
  },
  "skipped_steps": {
   "ex-1": [
    1,
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
   "archetype_id": "BC-QA-99003",
   "parameter_draw": {
    "constant": "5",
    "amplitude": "2",
    "sign": "1",
    "trig": "cos",
    "angle_turns": "1/3"
   },
   "completes": "ex-1",
   "stem": {
    "text": "On \\(r=5+2\\cos2\\theta\\) at \\(\\theta=\\pi/3\\), \\(dy/d\\theta=-1\\) and \\(dx/d\\theta=-3\\sqrt3\\). Find the slope of the tangent line.",
    "command_verb": "find"
   },
   "key": {
    "form": "symbolic",
    "expr": "sqrt(3)/9"
   },
   "steps": [
    {
     "text": "Quotient.",
     "expr": "(-1)/(-3*sqrt(3))",
     "relation": "new"
    },
    {
     "text": "Simplify.",
     "expr": "sqrt(3)/9",
     "relation": "equivalent"
    }
   ],
   "calculator_status": "no_calculator",
   "skills": [
    "BC-SKL-09033"
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
   "archetype_id": "BC-QA-99003",
   "parameter_draw": {
    "constant": "3",
    "amplitude": "2",
    "sign": "1",
    "trig": "cos",
    "angle_turns": "2/3"
   },
   "stem": {
    "text": "For \\(r=3+2\\cos2\\theta\\), find the slope of the line tangent to the curve at \\(\\theta=2\\pi/3\\).",
    "command_verb": "find"
   },
   "key": {
    "form": "symbolic",
    "expr": "-sqrt(3)/3"
   },
   "steps": [
    {
     "text": "y.",
     "expr": "(3 + 2*cos(2*theta))*sin(theta)",
     "relation": "new"
    },
    {
     "text": "dy.",
     "expr": "-4*sin(2*theta)*sin(theta) + (3 + 2*cos(2*theta))*cos(theta)",
     "relation": "differentiate",
     "variable": "theta"
    },
    {
     "text": "x.",
     "expr": "(3 + 2*cos(2*theta))*cos(theta)",
     "relation": "new"
    },
    {
     "text": "dx.",
     "expr": "-4*sin(2*theta)*cos(theta) - (3 + 2*cos(2*theta))*sin(theta)",
     "relation": "differentiate",
     "variable": "theta"
    },
    {
     "text": "Quotient.",
     "expr": "(2)/(-2*sqrt(3))",
     "relation": "new"
    },
    {
     "text": "Simplify.",
     "expr": "-sqrt(3)/3",
     "relation": "equivalent"
    }
   ],
   "calculator_status": "no_calculator",
   "skills": [
    "BC-SKL-09033"
   ]
  },
  {
   "id": "chk-3",
   "check_kind": "mcq",
   "format": "mcq",
   "bands": [
    "low"
   ],
   "archetype_id": "BC-QA-99003",
   "parameter_draw": {
    "constant": "6",
    "amplitude": "2",
    "sign": "-1",
    "trig": "cos",
    "angle_turns": "2/3"
   },
   "stem": {
    "text": "For \\(r=6-2\\cos2\\theta\\), the slope of the line tangent to the curve at \\(\\theta=2\\pi/3\\) is",
    "command_verb": "identify"
   },
   "key": {
    "form": "symbolic",
    "expr": "13*sqrt(3)/15"
   },
   "steps": [
    {
     "text": "y.",
     "expr": "(6 - 2*cos(2*theta))*sin(theta)",
     "relation": "new"
    },
    {
     "text": "dy.",
     "expr": "4*sin(2*theta)*sin(theta) + (6 - 2*cos(2*theta))*cos(theta)",
     "relation": "differentiate",
     "variable": "theta"
    },
    {
     "text": "x.",
     "expr": "(6 - 2*cos(2*theta))*cos(theta)",
     "relation": "new"
    },
    {
     "text": "dx.",
     "expr": "4*sin(2*theta)*cos(theta) - (6 - 2*cos(2*theta))*sin(theta)",
     "relation": "differentiate",
     "variable": "theta"
    },
    {
     "text": "Quotient.",
     "expr": "(-13/2)/(-5*sqrt(3)/2)",
     "relation": "new"
    },
    {
     "text": "Simplify.",
     "expr": "13*sqrt(3)/15",
     "relation": "equivalent"
    }
   ],
   "options": [
    {
     "id": "A",
     "is_key": false,
     "label": "\\(-2\\sqrt3\\)",
     "expr": "-2*sqrt(3)",
     "error_path": "BC-ERR-09031",
     "derivation": "dr/dtheta at the angle reported as the slope"
    },
    {
     "id": "B",
     "is_key": false,
     "label": "\\(-\\sqrt3\\)",
     "expr": "-sqrt(3)",
     "error_path": "BC-ERR-09032",
     "derivation": "each coordinate's derivative taken as r' times the trigonometric factor only, so the slope is tan of the angle"
    },
    {
     "id": "C",
     "is_key": true,
     "label": "\\(\\frac{13\\sqrt3}{15}\\)",
     "expr": "13*sqrt(3)/15",
     "error_path": null
    },
    {
     "id": "D",
     "is_key": false,
     "label": "\\(\\frac{5\\sqrt3}{9}\\)",
     "expr": "5*sqrt(3)/9",
     "error_path": "BC-ERR-99031",
     "derivation": "dr/dtheta with the chain factor dropped"
    }
   ],
   "calculator_status": "no_calculator",
   "skills": [
    "BC-SKL-09033"
   ]
  }
 ],
 "delivery": [
  {
   "block": "orientation",
   "mode": "figure",
   "reason": "rule 4 (README rule 3): BC-REP-13 on BC-SKL-09033 and BC-SKL-09034; not promoted, the stem asks for a slope value or a justified angle, not a reading of a varying quantity",
   "sources": [
    "BC-SKL-09033",
    "BC-SKL-09034"
   ],
   "spec": {
    "kind": "polar_curve",
    "representations": [
     "BC-REP-13",
     "BC-REP-02"
    ],
    "curves": [
     {
      "r": "5 + 2*cos(2*theta)",
      "domain": [
       "0",
       "pi"
      ]
     }
    ],
    "marks": [
     {
      "theta": "pi/3"
     }
    ],
    "drawn": [
     "the radial segment from the pole to the point",
     "the tangent line at the point"
    ],
    "labels": [
     {
      "text": "r = 5 + 2cos 2θ",
      "placement": "inside"
     },
     {
      "text": "radial segment: dr/dθ",
      "placement": "inside"
     },
     {
      "text": "tangent line: dy/dx",
      "placement": "inside"
     }
    ]
   },
   "fallback": "the same figure static, radial segment and tangent line labelled inside",
   "keyboard": "no control; the figure description is reached with Tab"
  },
  {
   "block": "ki-1",
   "mode": "figure",
   "reason": "rule 4 (README rule 3): BC-REP-13 and BC-REP-09 on BC-SKL-09034; the candidates at the critical angle and both endpoints are marked on the curve",
   "sources": [
    "BC-SKL-09034"
   ],
   "spec": {
    "kind": "polar_curve",
    "representations": [
     "BC-REP-13",
     "BC-REP-02"
    ],
    "curves": [
     {
      "r": "4 + 3*sin(theta)",
      "domain": [
       "0.2",
       "1.9"
      ]
     }
    ],
    "marks": [
     {
      "theta": "0.2"
     },
     {
      "theta": "0.465"
     },
     {
      "theta": "1.9"
     }
    ],
    "labels": [
     {
      "text": "θ = 0.2",
      "placement": "inside"
     },
     {
      "text": "θ = 0.465",
      "placement": "inside"
     },
     {
      "text": "θ = 1.9",
      "placement": "inside"
     },
     {
      "text": "distance from the y-axis: |x|",
      "placement": "inside"
     }
    ]
   },
   "fallback": "the same figure static with the three candidates marked and labelled",
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
   "block": "err-BC-ERR-09031",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  },
  {
   "block": "err-BC-ERR-09032",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  },
  {
   "block": "err-BC-ERR-99004",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  },
  {
   "block": "err-BC-ERR-99031",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  }
 ],
 "refresher": [
  "ki-1",
  "err-BC-ERR-09031",
  "err-BC-ERR-09032",
  "err-BC-ERR-99004",
  "err-BC-ERR-99031",
  "ex-1"
 ],
 "research_lines": [
  {
   "file": "research/units/unit-09-parametric-polar-vector.md",
   "line": "The product rule is needed to differentiate r times a trigonometric factor"
  }
 ],
 "inferred": [
  {
   "claim": "A fluent solver writes both rates, the quotient and the value, and holds the recognition and the x and y rewriting.",
   "settles": "Per-step timing from the fluency telemetry."
  },
  {
   "claim": "BC-QA-99003 has no point_types, so ex-1 carries no tag and no scoring line; the slope point BC-PT-99049 is taught in ki-1 but tagged on no step.",
   "settles": "A scoring guideline for the 2018 shape, or a point_types entry on BC-QA-99003."
  },
  {
   "claim": "BC-ERR-99031 is shown for its clause about differentiating the polar radius incorrectly, as a dropped chain factor on ex-1's draw; its other clauses concern polar area and motion.",
   "settles": "A BC-ERR record specific to the chain factor in dr/dtheta."
  },
  {
   "claim": "ex-2 is timed against Section I Part B; the lesson time entry is Part A for ex-1.",
   "settles": "Timing data per archetype shape."
  }
 ],
 "sources": [
  "BC-CON-09014",
  "BC-SKL-09033",
  "BC-SKL-09034",
  "BC-EK-FUN-3G2",
  "ced:177",
  "BC-QA-99003",
  "BC-QA-09011",
  "BC-PT-99013",
  "BC-PT-99011",
  "BC-PT-99049",
  "BC-ERR-09031",
  "BC-ERR-09032",
  "BC-ERR-99004",
  "BC-ERR-99031",
  "BC-MIS-09015",
  "BC-MIS-05018",
  "BC-PRQ-08001",
  "BC-PRQ-09002",
  "sg-25:9",
  "sg-25:7",
  "BC-FRQ-2018-Q5-B",
  "BC-FRQ-2025-Q2-C",
  "BC-QA-09009",
  "research/units/unit-09-parametric-polar-vector.md#9.7 Defining Polar Coordinates and Differentiating in Polar Form",
  "research/question-analysis/question-archetypes.md#BC-QA-99003 Slope of the tangent line to a polar curve at a stated angle",
  "research/question-analysis/question-archetypes.md#BC-QA-09011 Point on a polar curve farthest from a coordinate axis",
  "research/scoring/common-point-losses.md#Justification points",
  "research/exam/exam-structure.md#Section and part layout"
 ],
 "word_count": {
  "full": 830,
  "brief": 397
 },
 "read_minutes": {
  "full": 5.6,
  "brief": 2.7
 }
}
```
