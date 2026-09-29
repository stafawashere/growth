---
title: LSN-CON-09002 Slope of a parametric curve as a quotient of derivatives
research_date: 2026-09-29
status: designed
purpose: Authoring spec for the concept lesson on BC-CON-09002, the slope of the tangent to a parametric path as dy/dt over dx/dt at a stated parameter value, built from authoring_bundle("BC-CON-09002") and the research files it cites, so an author fills plan 15's lesson record without making a teaching decision.
---

# LSN-CON-09002 Slope of a parametric curve as a quotient of derivatives

Concept BC-CON-09002 (skills BC-SKL-09002 to BC-SKL-09006), topic 9.1 of Unit 9, BC only (ced:171), loaded by BC-QA-09001 (family parametric-calculus) and, through BC-SKL-09002 and BC-SKL-09003, by BC-QA-99001 (family polar-calculus). Its Unit 9 hard parent is BC-CON-09001 (docs/lessons/unit-09/README.md, section 1), so both component derivatives are assumed.

## Prediction

Served first, both bands: an `mcq` on ex-1's own rates at its time, \(dx/dt=14/5\) and \(dy/dt=6\cos 2\), with the core claim that the slope is the rate of y over the rate of x. Key B, the quotient. The distractors are the reciprocal, \(dy/dt\) alone and the sum of the rates. Rise over run in a small time answers it before any rule is taught. The resolution gives the quotient and its value with no verdict. Source: BC-CON-09002 and the topic section the key idea cites.

## Orientation

From BC-CON-09002 `description_plain` ("The slope of the tangent is the rate of y divided by the rate of x") and the topic's Assessment behaviour paragraph (research/units/unit-09-parametric-polar-vector.md#9.1 Defining and Differentiating Parametric Equations): the response must communicate the quotient of the two rates, and the value follows. No count, no frequency.

## Key ideas

Every skill maps to BC-EK-CHA-3G2 (ced:171): one core block, both bands.

- ki-1 (core). Paraphrase of the Required mathematical knowledge paragraphs Parametric derivative (hypotheses: x and y differentiable, dx/dt not zero; conclusion: the quotient is the slope) and Notation (the parameter is not a coordinate). Notation line from the concept's `notation`. No anchor quote: the cached page prints the sentence as broken equation text, so no exact match is possible.

## Recognition

BC-QA-09001 (research/question-analysis/question-archetypes.md#BC-QA-09001 Slope of the tangent to a parametric path at a time): `common_givens` "a parametric or vector description of a path" and "a time"; `asked_to_produce` "a quotient of parametric derivatives" and "a numerical slope"; `typical_wording` "find the slope of the line tangent to the path of the particle at the given time and show the work". Shapes: a calculator part of the Q2 slot, often beside a coordinate part (BC-FRQ-2022-Q2-A, 2015-Q2-B, 2023-Q2-C, 2026-Q2-B), and an MCQ giving the pair with the reciprocal and dy/dt alone as distractors (BC-MCQ-SAMPLE-017, BC-MCQ-PE2012-002).

BC-QA-99001 loads BC-SKL-09002 and BC-SKL-09003 on a polar curve where the quotient is used backward: the slope and dy/dθ are supplied and dx/dθ is wanted.

The near miss of the contrast pair is the rate of one coordinate in time on the same path (the archetype's `common_distractors`, "dy/dt alone"), which belongs to BC-CON-09001. The two stems share a path and a time and differ in what they ask for. What says "not this concept": a rate of change of y, a vertical velocity, or a speed; a second derivative (BC-CON-09003).

## Method choice

- st-1, BC-QA-09001. Cue from `common_givens` and `asked_to_produce`. Method from `expected_solution_path[0..1]`, "compute dy/dt and dx/dt" and "form the quotient". Rival: `common_distractors` "dy/dt alone" and "dx/dt divided by dy/dt". Separating feature: a slope of a tangent line. It carries the contrast pair, a slope stem beside a stem for the rate of y on one path. No field opens with the reader's label.
- st-2, BC-QA-99001, low band only. Cue from `common_givens` and `asked_to_produce`; method `expected_solution_path[0..2]`; rival `wrong_approaches` "differentiating the polar equation and reporting dr/dtheta"; the feature is the backward use of the quotient.

## Solution path

- ex-1, BC-QA-09001, both bands, calculator. Draw: drift 2, height 3, rate 1/2, vertical sine, time 2, object bead, given positions. \(x=2t+\ln(1+t^2)\), \(y=3\sin(t^2/2)\); \(dx/dt=14/5\), \(dy/dt=6\cos 2\), slope \(-0.8917\) by SymPy, reported -0.892. No published item on BC-QA-09001 carries this draw (content/items_gen_unit09, ITM-GEN-09001-00 to 20).
- ex-2, low band, calculator, faded from step 3. Draw: drift 1, height 5, rate 1/2, vertical exponential, time 3/2, object drone, given rate_of_x. \(y=5e^{-t^2/2}\), \(dx/dt=25/13\) at the time, slope \(-1.2661\), reported -1.266. Steps 1 and 2 (the two rates) are shown and the student writes the slope; steps 3 and 4 (the quotient and the value) then reveal, because the quotient and the single rounding are what the student must produce.
- A fluent solver writes both rates and the quotient; the calculator evaluation is held. No productive-failure comparison: BC-CON-09002 is not in `PRODUCTIVE_FAILURE_TARGETS`.

## Scoring

BC-QA-09001 lists BC-PT-99005, 99049, 99004, 99001. ex-1 tags BC-PT-99049 on the quotient; ex-2 tags BC-PT-99049 and BC-PT-99004. BC-PT-99005 and BC-PT-99001 stay untagged to fit the brief band (inferred array shows the value of the quotient point). Lines are `reader_checks` output.

Point losses from research: the slope point needs the quotient shown, and a bare decimal does not earn it (sg-23:7; BC-ERR-09004); a decimal short of three places or an intermediate rounded early loses the answer point (research/scoring/common-point-losses.md#Answer points, BC-ERR-99019); a calculator value with no setup earns nothing (research/scoring/common-point-losses.md#Setup points, BC-ERR-99021).

## Traps

Bundle order is BC-ERR-03012, 09002, 09003, 09004, 09005, 09007, 99029, 99019. The blocks are BC-ERR-03012, 09002, 09003 and 99019, on ex-1's draw, all `fix_prompt` true. BC-ERR-09004 (a correct decimal with no quotient) is left out because its wrong and right steps share a value, and check 3 needs a value distractor for BC-ERR-99019, the fourth block; the quotient-shown rule is taught in ki-1 and scored in the reader lines. Mid band shows the first two.

- err-BC-ERR-03012: dx/dt set to zero for a horizontal tangent, against dy/dt. Both sides are equations. No possible reason line.
- err-BC-ERR-09002: the reciprocal quotient. Possible reason, BC-MIS-09003.
- err-BC-ERR-09003: dy/dt alone, 6cos 2, against the quotient.
- err-BC-ERR-99019: -0.893 from rates rounded to two places, against -0.892.

## Representations

None. The path figure is carried by the orientation and ki-1 delivery entries, which the topic's Representations paragraph supports (a plotted path to a statement about the tangent, BC-REP-02 to BC-REP-04).

## Prerequisite bridge

- BC-PRQ-06005, BC-PRQ-08001 and BC-PRQ-08006, each from its `description_plain` and `failure_signature`.

## Time

The MCQ form of the archetype is Section I Part B, 2.92 minutes (research/exam/exam-structure.md#Section and part layout); as one free response part it is 1 point, 1.67 minutes, in the Q2 slot (docs/lessons/unit-09/README.md, section 5). A fluent solver writes both rates and the quotient and holds the calculator evaluation. The minutes go on the chain rule in \(dy/dt\).

## Checks

- chk-1, completion of ex-1, both bands: the two rates given, the value asked. Key -0.892.
- chk-2, isomorph, both bands. Draw: drift 4, height 2, rate 1/4, vertical cosine, time 3, object drone, given positions. Key -0.507.
- chk-3, MCQ, low band. Draw: drift 1, height 3, rate 3/4, vertical cosine, time 1, object bead, given positions. Key -1.534 (SymPy -1.53369). Distractors: -0.652, the reciprocal (BC-ERR-09002); -3.067, dy/dt alone (BC-ERR-09003); -1.535, dy/dt rounded to -3.07 first (BC-ERR-99019). No published draw matches any of these.

## Delivery

- orientation: figure. Rule 4 (README rule 3): BC-REP-12 on BC-SKL-09002 to 09006; the path with the tangent line at t = 2.
- ki-1: interactive. README delivery map, promoted: one draggable time, the tangent line and the two rates drawn at the point; the reading is where the tangent is flat. One control.
- ex-1, ex-2, the four error blocks: step_reveal. Rule 1.

## Band plan

- Low (full): prediction, orientation, bridges, ki-1, st-1 with the contrast pair, st-2, ex-1 and its line, chk-1, the four error blocks, ex-2 (faded from step 3) and its lines, chk-2, chk-3. 804 words, 5.5 minutes.
- Mid (brief): prediction, orientation, bridges, ki-1, st-1 with the contrast pair, ex-1 and its line, chk-1, err-BC-ERR-03012, err-BC-ERR-09002, chk-2. 421 words, 3.0 minutes.
- Refresher: ki-1, the four error blocks, ex-1.

## Sources

- BC-CON-09002; BC-SKL-09002 to BC-SKL-09006; BC-EK-CHA-3G2; ced:171
- BC-QA-09001, BC-QA-99001; BC-PT-99049, BC-PT-99004
- BC-ERR-03012, BC-ERR-09002, BC-ERR-09003, BC-ERR-99019; BC-MIS-09003
- BC-PRQ-06005, BC-PRQ-08001, BC-PRQ-08006
- sg-23:7
- research/units/unit-09-parametric-polar-vector.md#9.1 Defining and Differentiating Parametric Equations
- research/question-analysis/question-archetypes.md#BC-QA-09001 Slope of the tangent to a parametric path at a time
- research/exam/exam-structure.md#Section and part layout
- [inferred] The held steps; the prediction's first-attempt behaviour; every non-text delivery mode. Each settled as the inferred array states.

## Machine record

```json
{
 "id": "LSN-CON-09002",
 "kind": "concept",
 "target_id": "BC-CON-09002",
 "unit": "09",
 "skills": [
  "BC-SKL-09002",
  "BC-SKL-09003",
  "BC-SKL-09004",
  "BC-SKL-09005",
  "BC-SKL-09006"
 ],
 "prediction": {
  "id": "pr-1",
  "stem": {
   "text": "At \\(t=2\\) a bead has \\(dx/dt=14/5\\) and \\(dy/dt=6\\cos2\\). Predict the slope of its tangent line.",
   "command_verb": "predict"
  },
  "format": "mcq",
  "options": [
   {
    "id": "A",
    "label": "\\(\\dfrac{14/5}{6\\cos2}\\)",
    "is_key": false
   },
   {
    "id": "B",
    "label": "\\(\\dfrac{6\\cos2}{14/5}\\)",
    "is_key": true
   },
   {
    "id": "C",
    "label": "\\(6\\cos2\\)",
    "is_key": false
   },
   {
    "id": "D",
    "label": "\\(\\dfrac{14}{5}\\cdot6\\cos2\\)",
    "is_key": false
   }
  ],
  "resolution": "Rise over run per unit time: \\(\\dfrac{6\\cos2}{14/5}\\approx-0.892\\), the rate of y over the rate of x.",
  "sources": [
   "BC-CON-09002",
   "research/units/unit-09-parametric-polar-vector.md#9.1 Defining and Differentiating Parametric Equations"
  ]
 },
 "orientation": {
  "text": "The slope of a parametric path's tangent line is the rate of y over the rate of x at the stated parameter value. A response shows that quotient, then the value to three places.",
  "sources": [
   "BC-CON-09002",
   "research/units/unit-09-parametric-polar-vector.md#9.1 Defining and Differentiating Parametric Equations"
  ]
 },
 "key_ideas": [
  {
   "id": "ki-1",
   "ek_id": "BC-EK-CHA-3G2",
   "depth": "core",
   "text": "On a parametric curve \\(dy/dx\\) is the slope of the tangent line and equals \\(dy/dt\\) over \\(dx/dt\\) where \\(dx/dt\\ne0\\). The rate \\(dy/dt\\) alone is a rate in time, not a slope.",
   "notation": "dy/dx as dy/dt over dx/dt",
   "quote": null,
   "sources": [
    "BC-EK-CHA-3G2",
    "ced:171",
    "research/units/unit-09-parametric-polar-vector.md#9.1 Defining and Differentiating Parametric Equations"
   ]
  }
 ],
 "strategy": [
  {
   "id": "st-1",
   "archetype_id": "BC-QA-09001",
   "cue": "A path \\((x(t),y(t))\\), a time, a tangent slope.",
   "method": "Write both rates, then \\(\\dfrac{dy/dt}{dx/dt}\\).",
   "rival": "\\(dy/dt\\) alone, or the quotient inverted.",
   "separating_feature": "A tangent slope is asked, not a rate in time.",
   "sources": [
    "BC-QA-09001"
   ],
   "evidence_tag": "verified",
   "contrast": {
    "this": {
     "text": "Position \\((3t+\\ln(1+t^2),4\\cos(t^2/3))\\). Find the tangent slope at \\(t=2\\).",
     "archetype_id": "BC-QA-09001"
    },
    "not_this": {
     "text": "Position \\((3t+\\ln(1+t^2),4\\cos(t^2/3))\\). Find how fast the height changes at \\(t=2\\).",
     "why_not": "It asks for the rate of y in time, with no division."
    },
    "feature": "Tangent slope, not a rate in time."
   }
  },
  {
   "id": "st-2",
   "archetype_id": "BC-QA-99001",
   "cue": "A polar curve, the slope of its tangent at a point, and \\(dy/d\\theta\\) there.",
   "method": "Write \\(\\dfrac{dy}{dx}=\\dfrac{dy/d\\theta}{dx/d\\theta}\\), rearrange for \\(dx/d\\theta\\), and substitute.",
   "rival": "Differentiating the polar equation and reporting \\(dr/d\\theta\\).",
   "separating_feature": "The quotient is used backward: two of the three derivatives are supplied.",
   "sources": [
    "BC-QA-99001"
   ],
   "evidence_tag": "verified"
  }
 ],
 "worked_examples": [
  {
   "id": "ex-1",
   "archetype_id": "BC-QA-09001",
   "bands": [
    "low",
    "mid"
   ],
   "parameter_draw": {
    "drift": "2",
    "height": "3",
    "rate": "1/2",
    "vertical": "sine",
    "time": "2",
    "object": "bead",
    "given": "positions"
   },
   "problem": {
    "text": "A bead has position \\((2t+\\ln(1+t^2),3\\sin(t^2/2))\\). Using a calculator, find the tangent slope at \\(t=2\\), to three decimals.",
    "command_verb": "find"
   },
   "calculator_status": "calculator",
   "steps": [
    {
     "cue": "Differentiate \\(x\\).",
     "why": "The slope needs both rates.",
     "expr": "2 + 2*t/(1+t**2)",
     "relation": "new"
    },
    {
     "cue": "Differentiate \\(y\\).",
     "why": "Chain rule gives the factor \\(t\\).",
     "expr": "3*t*cos(t**2/2)",
     "relation": "new"
    },
    {
     "cue": "A slope: rate of \\(y\\) over rate of \\(x\\).",
     "why": "The written quotient is scored.",
     "expr": "3*t*cos(t**2/2)/(2 + 2*t/(1+t**2))",
     "relation": "new",
     "point_type_id": "BC-PT-99049"
    },
    {
     "cue": "\\(t=2\\), three places.",
     "why": "Round once, at the end.",
     "expr": "-0.892",
     "relation": "evaluate",
     "subs": {
      "t": "2"
     },
     "approx": true
    }
   ],
   "answer": {
    "form": "numeric",
    "expr": "-0.892"
   }
  },
  {
   "id": "ex-2",
   "archetype_id": "BC-QA-09001",
   "bands": [
    "low"
   ],
   "parameter_draw": {
    "drift": "1",
    "height": "5",
    "rate": "1/2",
    "vertical": "exponential",
    "time": "3/2",
    "object": "drone",
    "given": "rate_of_x"
   },
   "problem": {
    "text": "A drone moves so that \\(dx/dt=1+\\dfrac{2t}{1+t^2}\\) and \\(y(t)=5e^{-t^2/2}\\). Using a calculator, find the slope of the line tangent to its path at \\(t=3/2\\). Show the setup.",
    "command_verb": "find"
   },
   "calculator_status": "calculator",
   "steps": [
    {
     "cue": "The stem gives \\(dx/dt\\) directly.",
     "why": "No differentiation of \\(x\\) is needed.",
     "expr": "1 + 2*t/(1+t**2)",
     "relation": "new"
    },
    {
     "cue": "\\(y\\) is an exponential with inner \\(-t^2/2\\).",
     "why": "Chain rule gives the factor \\(-t\\).",
     "expr": "-5*t*exp(-t**2/2)",
     "relation": "new"
    },
    {
     "cue": "Slope: rate of \\(y\\) over rate of \\(x\\).",
     "why": "The quotient is written before any value.",
     "expr": "-5*t*exp(-t**2/2)/(1 + 2*t/(1+t**2))",
     "relation": "new",
     "point_type_id": "BC-PT-99049"
    },
    {
     "cue": "Time \\(3/2\\), three places.",
     "why": "The calculator value, rounded once.",
     "expr": "-1.266",
     "relation": "evaluate",
     "subs": {
      "t": "3/2"
     },
     "approx": true,
     "point_type_id": "BC-PT-99004"
    }
   ],
   "answer": {
    "form": "numeric",
    "expr": "-1.266"
   },
   "fade_from": 3
  }
 ],
 "what_a_reader_scores": [
  {
   "example_id": "ex-1",
   "point_type_ids": [
    "BC-PT-99049"
   ],
   "lines": [
    {
     "point_type_id": "BC-PT-99049",
     "text": "Derivative of one variable with respect to another by the chain rule in polar or parametric form. Earned by: A correct chain or quotient relation among the derivatives, presented symbolically or numerically (sg-26:7, sg-23:7). Not earned by: An equation of the form expression equals constant that equates a general expression to a single value (sg-22:6, sg-23:6). Notation: sg-25:7 accepts several loose notations for an evaluated derivative, including one written without the evaluation bar, and still awards the point."
    }
   ]
  },
  {
   "example_id": "ex-2",
   "point_type_ids": [
    "BC-PT-99049",
    "BC-PT-99004"
   ],
   "lines": [
    {
     "point_type_id": "BC-PT-99049",
     "text": "Derivative of one variable with respect to another by the chain rule in polar or parametric form. Earned by: A correct chain or quotient relation among the derivatives, presented symbolically or numerically (sg-26:7, sg-23:7). Not earned by: An equation of the form expression equals constant that equates a general expression to a single value (sg-22:6, sg-23:6). Notation: sg-25:7 accepts several loose notations for an evaluated derivative, including one written without the evaluation bar, and still awards the point."
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
   "error_id": "BC-ERR-03012",
   "observed_behavior": "The denominator of dy/dx is set to zero when a horizontal tangent is requested, or the numerator when a vertical tangent is requested.",
   "scoring_consequence": "The reported point is wrong and the reasoning point is not available.",
   "wrong_step": {
    "text": "\\(dx/dt=0\\).",
    "expr": "2 + 2*t/(1+t**2) = 0"
   },
   "right_step": {
    "text": "\\(dy/dt=0\\).",
    "expr": "3*t*cos(t**2/2) = 0"
   },
   "relation": "distinct",
   "fix_prompt": true,
   "possible_reason": null,
   "sources": [
    "BC-ERR-03012"
   ]
  },
  {
   "error_id": "BC-ERR-09002",
   "observed_behavior": "The quotient of parametric derivatives is taken in the reciprocal order.",
   "scoring_consequence": "The slope point is lost.",
   "wrong_step": {
    "text": "\\(dx/dt\\) over \\(dy/dt\\).",
    "expr": "(2 + 2*t/(1+t**2))/(3*t*cos(t**2/2))"
   },
   "right_step": {
    "text": "\\(dy/dt\\) over \\(dx/dt\\).",
    "expr": "3*t*cos(t**2/2)/(2 + 2*t/(1+t**2))"
   },
   "relation": "distinct",
   "fix_prompt": true,
   "possible_reason": {
    "misconception_id": "BC-MIS-09003",
    "text": "the reciprocal looks equally acceptable"
   },
   "sources": [
    "BC-ERR-09002",
    "BC-MIS-09003"
   ]
  },
  {
   "error_id": "BC-ERR-09003",
   "observed_behavior": "The response gives dy/dt where the slope of the tangent line was requested.",
   "scoring_consequence": "The slope point is lost because the quotient structure is absent (sg-23:7).",
   "wrong_step": {
    "text": "\\(dy/dt\\) alone.",
    "expr": "6*cos(2)"
   },
   "right_step": {
    "text": "The quotient.",
    "expr": "6*cos(2)/(14/5)"
   },
   "relation": "distinct",
   "fix_prompt": true,
   "possible_reason": null,
   "sources": [
    "BC-ERR-09003"
   ]
  },
  {
   "error_id": "BC-ERR-99019",
   "observed_behavior": "Responses report fewer than three digits after the decimal point, round an intermediate value before it is used again, or read a value off a trace rather than solving for it.",
   "scoring_consequence": "The answer point is not earned; the report notes this recurs across several parts of the same response.",
   "wrong_step": {
    "text": "Rates rounded first.",
    "expr": "-0.893"
   },
   "right_step": {
    "text": "Rounded once.",
    "expr": "-0.892"
   },
   "relation": "distinct",
   "fix_prompt": true,
   "possible_reason": null,
   "sources": [
    "BC-ERR-99019"
   ]
  }
 ],
 "representations": null,
 "prerequisite_bridges": [
  {
   "prq_id": "BC-PRQ-06005",
   "text": "\\(x'(t)\\) and \\(x(t)\\) are different functions, each read at the stated input."
  },
  {
   "prq_id": "BC-PRQ-08001",
   "text": "Set the two expressions equal and solve for every root."
  },
  {
   "prq_id": "BC-PRQ-08006",
   "text": "Three places after the point, rounded once, at the end."
  }
 ],
 "time": {
  "exam_part": "I-B",
  "budget_minutes": 2.92,
  "source": "research/exam/exam-structure.md#Section and part layout",
  "written_steps": {
   "ex-1": [
    1,
    2,
    3
   ]
  },
  "skipped_steps": {
   "ex-1": [
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
   "archetype_id": "BC-QA-09001",
   "parameter_draw": {
    "drift": "2",
    "height": "3",
    "rate": "1/2",
    "vertical": "sine",
    "time": "2",
    "object": "bead",
    "given": "positions"
   },
   "completes": "ex-1",
   "stem": {
    "text": "At \\(t=2\\), \\(dx/dt=14/5\\) and \\(dy/dt=6\\cos2\\). Write the slope to three decimals.",
    "command_verb": "write"
   },
   "key": {
    "form": "numeric",
    "expr": "-0.892"
   },
   "steps": [
    {
     "text": "The quotient of the rates.",
     "expr": "6*cos(2)/(14/5)",
     "relation": "new",
     "point_type_id": "BC-PT-99049"
    },
    {
     "text": "To three decimals.",
     "expr": "-0.892",
     "relation": "evaluate",
     "subs": {},
     "approx": true
    }
   ],
   "calculator_status": "calculator",
   "skills": [
    "BC-SKL-09004"
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
   "archetype_id": "BC-QA-09001",
   "parameter_draw": {
    "drift": "4",
    "height": "2",
    "rate": "1/4",
    "vertical": "cosine",
    "time": "3",
    "object": "drone",
    "given": "positions"
   },
   "stem": {
    "text": "Position \\((4t+\\ln(1+t^2),2\\cos(t^2/4))\\). Find the tangent slope at \\(t=3\\), to three decimals.",
    "command_verb": "find"
   },
   "key": {
    "form": "numeric",
    "expr": "-0.507"
   },
   "steps": [
    {
     "text": "\\(dx/dt\\).",
     "expr": "4 + 2*t/(1+t**2)",
     "relation": "new"
    },
    {
     "text": "\\(dy/dt\\) by the chain rule.",
     "expr": "-t*sin(t**2/4)",
     "relation": "new"
    },
    {
     "text": "The quotient.",
     "expr": "-t*sin(t**2/4)/(4 + 2*t/(1+t**2))",
     "relation": "new",
     "point_type_id": "BC-PT-99049"
    },
    {
     "text": "At \\(t=3\\), three decimals.",
     "expr": "-0.507",
     "relation": "evaluate",
     "subs": {
      "t": "3"
     },
     "approx": true
    }
   ],
   "calculator_status": "calculator",
   "skills": [
    "BC-SKL-09004"
   ]
  },
  {
   "id": "chk-3",
   "check_kind": "mcq",
   "format": "mcq",
   "bands": [
    "low"
   ],
   "archetype_id": "BC-QA-09001",
   "parameter_draw": {
    "drift": "1",
    "height": "3",
    "rate": "3/4",
    "vertical": "cosine",
    "time": "1",
    "object": "bead",
    "given": "positions"
   },
   "stem": {
    "text": "A bead has position \\((t+\\ln(1+t^2),\\,3\\cos(3t^2/4))\\). Using a calculator, find the slope of the line tangent to its path at \\(t=1\\).",
    "command_verb": "find"
   },
   "key": {
    "form": "numeric",
    "expr": "-1.534"
   },
   "steps": [
    {
     "text": "\\(dx/dt\\).",
     "expr": "1 + 2*t/(1+t**2)",
     "relation": "new"
    },
    {
     "text": "\\(dy/dt\\).",
     "expr": "-9*t*sin(3*t**2/4)/2",
     "relation": "new"
    },
    {
     "text": "The quotient.",
     "expr": "(-9*t*sin(3*t**2/4)/2)/(1 + 2*t/(1+t**2))",
     "relation": "new"
    },
    {
     "text": "At \\(t=1\\).",
     "expr": "-1.534",
     "relation": "evaluate",
     "subs": {
      "t": "1"
     },
     "approx": true
    }
   ],
   "options": [
    {
     "id": "A",
     "is_key": false,
     "expr": "-0.652",
     "error_path": "BC-ERR-09002",
     "derivation": "dx/dt over dy/dt: 2 divided by -9 sin(3/4)/2"
    },
    {
     "id": "B",
     "is_key": false,
     "expr": "-3.067",
     "error_path": "BC-ERR-09003",
     "derivation": "dy/dt alone at t = 1, which is -9 sin(3/4)/2"
    },
    {
     "id": "C",
     "is_key": true,
     "expr": "-1.534",
     "error_path": null
    },
    {
     "id": "D",
     "is_key": false,
     "expr": "-1.535",
     "error_path": "BC-ERR-99019",
     "derivation": "dy/dt rounded to -3.07 before dividing by 2"
    }
   ],
   "calculator_status": "calculator",
   "skills": [
    "BC-SKL-09004"
   ]
  }
 ],
 "delivery": [
  {
   "block": "orientation",
   "mode": "figure",
   "reason": "rule 4: BC-REP-12 on BC-SKL-09002 to 09006; not promoted here because ki-1 carries the reading",
   "sources": [
    "BC-SKL-09002"
   ],
   "spec": {
    "kind": "parametric_path",
    "representations": [
     "BC-REP-12"
    ],
    "x": "2*t + log(1 + t**2)",
    "y": "3*sin(t**2/2)",
    "t_range": [
     0,
     3
    ],
    "marks": [
     {
      "t": 2
     }
    ],
    "drawn": [
     "the path",
     "the point at t = 2",
     "the tangent line at that point"
    ],
    "labels": [
     {
      "text": "t = 2",
      "placement": "inside"
     },
     {
      "text": "tangent line",
      "placement": "inside"
     },
     {
      "text": "(x(t), y(t))",
      "placement": "inside"
     }
    ]
   },
   "fallback": "the same path static with the tangent line at t = 2 and its labels",
   "keyboard": "no control; the figure description is reached with Tab"
  },
  {
   "block": "ki-1",
   "mode": "interactive",
   "reason": "rule 4 promoted: BC-REP-12 on BC-SKL-09002 to 09006, and BC-QA-09001 common_givens name a time with a stem that asks for the slope there",
   "sources": [
    "BC-SKL-09002",
    "BC-QA-09001"
   ],
   "spec": {
    "kind": "parametric_tangent",
    "representations": [
     "BC-REP-12"
    ],
    "x": "2*t + log(1 + t**2)",
    "y": "3*sin(t**2/2)",
    "t_range": [
     0,
     3
    ],
    "controls": [
     {
      "name": "t",
      "type": "slider",
      "min": 0,
      "max": 3,
      "step": 0.1,
      "initial": 2
     }
    ],
    "drawn": [
     "the path",
     "the point at t",
     "the tangent line",
     "dx/dt and dy/dt as the legs of the velocity vector"
    ],
    "reading": "At what t is the tangent line flat, and what is dy/dt there?",
    "labels": [
     {
      "text": "dx/dt",
      "placement": "inside"
     },
     {
      "text": "dy/dt",
      "placement": "inside"
     },
     {
      "text": "dy/dx",
      "placement": "inside"
     }
    ]
   },
   "fallback": "three static frames at t = 1, 2 and 3, each with its labelled rates and slope",
   "keyboard": "Left and Right arrows move t by 0.1; Home and End set t to 0 and 3"
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
   "block": "err-BC-ERR-03012",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  },
  {
   "block": "err-BC-ERR-09002",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  },
  {
   "block": "err-BC-ERR-09003",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  },
  {
   "block": "err-BC-ERR-99019",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  }
 ],
 "refresher": [
  "ki-1",
  "err-BC-ERR-03012",
  "err-BC-ERR-09002",
  "err-BC-ERR-09003",
  "err-BC-ERR-99019",
  "ex-1"
 ],
 "research_lines": [
  {
   "file": "research/units/unit-09-parametric-polar-vector.md",
   "line": "The parameter is not a coordinate, so dy/dx and dy/dt are different objects and the response must say which is being reported."
  }
 ],
 "inferred": [
  {
   "claim": "A fluent solver writes the two rates and the quotient and holds the calculator evaluation.",
   "settles": "Timing data per step once the fluency telemetry exists."
  },
  {
   "claim": "The prediction gives the exact rates of ex-1 at its time and asks for the slope, which rise over run settles before the rule is stated.",
   "settles": "The first-attempt rate on the prediction across bands."
  },
  {
   "claim": "Every non-text delivery choice.",
   "settles": "The modality A/B in the build plan: skip rate and time to first credited success by mode."
  }
 ],
 "sources": [
  "BC-CON-09002",
  "BC-SKL-09002",
  "BC-SKL-09003",
  "BC-SKL-09004",
  "BC-SKL-09005",
  "BC-SKL-09006",
  "BC-EK-CHA-3G2",
  "ced:171",
  "BC-QA-09001",
  "BC-QA-99001",
  "BC-PT-99049",
  "BC-PT-99004",
  "BC-ERR-03012",
  "BC-ERR-09002",
  "BC-ERR-09003",
  "BC-ERR-99019",
  "BC-MIS-09003",
  "BC-PRQ-06005",
  "BC-PRQ-08001",
  "BC-PRQ-08006",
  "sg-23:7",
  "research/units/unit-09-parametric-polar-vector.md#9.1 Defining and Differentiating Parametric Equations",
  "research/question-analysis/question-archetypes.md#BC-QA-09001 Slope of the tangent to a parametric path at a time",
  "research/exam/exam-structure.md#Section and part layout"
 ],
 "word_count": {
  "full": 804,
  "brief": 421
 },
 "read_minutes": {
  "full": 5.5,
  "brief": 3.0
 }
}
```
