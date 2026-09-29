---
title: LSN-CON-04007 Related rates variables as functions of time
research_date: 2026-09-29
status: designed
purpose: Authoring spec for the concept lesson on BC-CON-04007, each quantity in a related rates problem as a function of time contributing its own rate, built from authoring_bundle("BC-CON-04007") and the research files it cites, so an author fills plan 15's lesson record without making a teaching decision.
---

# LSN-CON-04007 Related rates variables as functions of time

Concept BC-CON-04007 (skills BC-SKL-04017, BC-SKL-04019, BC-SKL-04022), topic 4.4 of Unit 4, loaded by BC-QA-04006 and BC-QA-04007 (family related-rates). Its hard parents are BC-CON-04006 and BC-CON-04008, a concept-level cycle resolved by the skill order (docs/lessons/unit-04/README.md, section 1).

## Prediction

Served first in both bands. Multiple choice on ex-1's relation \(x^2+y^2=225\), both \(x\) and \(y\) changing in time: what the derivative in \(t\) of the left side is. Three options, key \(2x\,dx/dt+2y\,dy/dt\), the others one rate factor missing or both dropped. The resolution says each varying quantity brings its own rate factor, the concept's core claim in the record's words. Sources: BC-CON-04007 and the topic 4.4 section that ki-1 cites. Delivery: text.

## Orientation

Served text, from BC-CON-04007 `description_plain` and the Assessment behaviour paragraph (research/units/unit-04-contextual-applications-differentiation.md#4.4 Introduction to Related Rates): each varying quantity a function of time, the relation differentiated in t, the instant substituted after. No count, no frequency.

## Key ideas

BC-SKL-04017 and BC-SKL-04019 map BC-EK-CHA-3D1; BC-SKL-04022 maps BC-EK-CHA-3D1 and BC-EK-CHA-3D2. Two blocks: one core, one extended.

- ki-1 (core, BC-EK-CHA-3D1, ced:90). The Variables as functions of time paragraph of Required mathematical knowledge, with the fixed against instantaneous distinction of BC-MIS-04011's probe (docs/lessons/unit-04/README.md, section 6). Anchor quote from ced:90.
- ki-2 (extended, BC-EK-CHA-3D2, ced:90). The Other rules paragraph: the product rule on a mixed term. Anchor quote from ced:90. Extended to hold the brief band under its cap; ex-2 carries it in the low band.

## Recognition

- BC-QA-04006 (research/question-analysis/question-archetypes.md#BC-QA-04006 Related rates in a geometric setting): `typical_wording` "find the rate at which the stated quantity is changing at the instant described"; `common_givens` supplied rates, a formula relating the quantities, the dimensions at the instant, a figure; `asked_to_produce` the rate at the instant with units. The signal: the words at the instant when beside one supplied rate and a request for another. Shapes: one part of a multipart FRQ or a standalone MCQ (BC-FRQ-2019-Q4-A, BC-FRQ-2014-Q4-D, BC-FRQ-2022-Q4-D, BC-FRQ-2018-Q4-D, BC-MCQ-CED-005, BC-MCQ-SAMPLE-004, BC-MCQ-PE2012-038).
- BC-QA-04007 (research/question-analysis/question-archetypes.md#BC-QA-04007 Related rates on an implicitly defined curve), same family: a curve in x and y, a point, and one coordinate's rate at that instant; the closing part of the implicit differentiation FRQ (cr-24:18, crabbc-25:24).

Not this concept: a slope or dy/dx asked on the same curve (Unit 3 implicit differentiation). The rate of a coordinate supplied in time says differentiate in t (docs/lessons/unit-04/README.md, section 3).

The contrast pair on st-1 takes its near miss from that Unit 3 sibling: a ladder whose top's rate is wanted, beside \(dy/dx\) on \(x^2+y^2=169\) at a point. The separating feature is that the wanted rate is per unit of time.

## Method choice

One strategy block: BC-QA-04006 and BC-QA-04007 share the family related-rates, and BC-QA-04006 is listed first.

- st-1, BC-QA-04006. Method, `expected_solution_path[0]`: name each varying quantity and record the rates in derivative notation, served without a label. Rival, `wrong_approaches`: differentiating with respect to a length and stopping short of a rate in time (BC-ERR-04017); the other listed rivals are substituting before differentiating (BC-ERR-04020) and a lost product rule (BC-ERR-99013). Separating feature: the wanted rate is per unit of time. The archetype carries `asked_to_produce` and `common_givens`, so the block is verified.

## Solution path

- ex-1, BC-QA-04006, both bands, no calculator. Draw: shape ladder, size 9, rate 2, ratio 3, leg short, foot, second: a 15 foot ladder on the 9, 12, 15 triangle [inferred: size read as the named leg]. Key -3/2 feet per second. No published BC-QA-04006 item carries this draw.
- ex-2, BC-QA-04007, low band, faded from step 3. Draw: square_x 2, mixed 1, square_y 1, point (1, -2), rate_x 3: curve 2x^2 + xy + y^2 = 4; x_part 2, y_part -3, key 2; frozen rate 3/2 and slope 2/3 distinct as the spec requires.
- Steps follow `expected_solution_path`: relating equation (new), differentiated in t (new; SymPy has no implicit time here, so the rates are symbols dxdt and dydt), the instant substituted (evaluate), solved (solve), units. A fluent solver writes every line of ex-1; in ex-2 the curve is already on the page. Ex-2 shows steps 1 and 2, the curve and its differentiated form with the product rule, then the student writes dy/dt before steps 3 and 4 (the substitution and the solve) reveal. The fade falls there because the differentiation is this concept's own work and the substitution is the mechanical remainder.

## Scoring

BC-QA-04006 lists BC-PT-99023, BC-PT-99006, BC-PT-99004 and BC-PT-99022. ex-1 tags BC-PT-99023 on the differentiated equation, the point this concept owns; the line is reader_checks(["BC-PT-99023"]) copied exactly. BC-QA-04007 lists no `point_types`, so ex-2 carries no tag and no scoring entry.

For the author: the 2022 report records few responses recognising that the chain rule was needed to reach the rate with respect to time (cr-22:7); units losses are under research/scoring/common-point-losses.md#Units points, and derivative notation under research/scoring/notation-requirements.md#Derivative notation.

## Traps

Five active errors meet the skills; the first four in the bundle's order are served: BC-ERR-04015, BC-ERR-04017, BC-ERR-04018, BC-ERR-99013. Low band all four; mid band the first two. The first two sit on ex-1's draw, the last two on ex-2's. All four are fix prompts (relation distinct).

- err-BC-ERR-04015: the given rate 2 reported, against -3/2. No possible reason: the linked descriptions concern differentiation and substitution, not which rate is given.
- err-BC-ERR-04017: dy/dx = -3/4 at the instant, against dy/dt = -3/2. Possible reason from BC-MIS-04008.
- err-BC-ERR-04018: xy differentiated with x held constant, against the product rule. Possible reason from BC-MIS-04009.
- err-BC-ERR-99013: dy/dx = 2/3 reported, against dy/dt = 2. Possible reason from BC-MIS-99005.

Not served, past the cap of four: BC-ERR-99033.

## Representations

None as a separate block. The topic's Representations paragraph names a verbal scenario to a labelled diagram (BC-REP-05 to BC-REP-08); ki-1's interactive carries it.

## Prerequisite bridge

- BC-PRQ-04008, from its `description_plain` and `failure_signature`.

## Time

BC-QA-04006 has calculator status either, so the lesson takes Section I Part A, 2.14 minutes per question (research/exam/exam-structure.md#Section and part layout) [inferred: the either status]. As an FRQ part it takes 3.33 to 5.0 minutes of a 15.0 minute question (docs/lessons/unit-04/README.md, section 5). The minutes go on the relating equation, the differentiated equation with every rate factor, the substitution and the rate with units; the list of given and wanted rates is written once, as the first line.

## Checks

- chk-1, completion of ex-1, both bands: the substituted equation given, the student solves. Key -3/2.
- chk-2, isomorph, both bands. Draw: circle, size 6, rate 2, ratio 1, short, centimeter, minute. Key 24 pi square centimeters per minute.
- chk-3, MCQ, low band, on BC-QA-04007. Draw: square_x 1, mixed 3, square_y 2, point (1, 1), rate_x 2. Key -10/7; B 2 (BC-ERR-04015), C -4/7 (BC-ERR-04018, x held constant in 3xy), D -5/7 (BC-ERR-99013, the spec's slope_only).

## Delivery

- orientation: text. Rule 5; the diagram is served once, on ki-1.
- ki-1: interactive. Rule 3 promoted: BC-REP-08 on BC-SKL-04017, BC-QA-04006 `common_givens` "the dimensions at the instant" and "a figure of the configuration"; one slider on the foot, the reading being which labels move (docs/lessons/unit-04/README.md, section 6) [inferred; settled by the modality A/B].
- ki-2: text. Rule 5, BC-REP-01.
- ex-1, ex-2 and the four error blocks: step_reveal. Rule 1.

## Band plan

- Low (full), served order: prediction, orientation, bridge BC-PRQ-04008 when gated, ki-1, ki-2, st-1 with its contrast pair, ex-1 with its scoring line, chk-1, err-BC-ERR-04015, err-BC-ERR-04017, err-BC-ERR-04018, err-BC-ERR-99013, ex-2 faded, chk-2, chk-3. 661 words, 4.5 minutes (cap 900 and 6).
- Mid (brief): prediction, orientation, bridge when gated, ki-1, st-1 with its contrast pair, ex-1 with its scoring line, chk-1, err-BC-ERR-04015, err-BC-ERR-04017, chk-2. 448 words, 3.0 minutes (cap 450 and 3). The quote on ki-1 is cut to its first nine words to hold the cap.
- Refresher: ki-1, the four error blocks, ex-1.

## Sources

- BC-CON-04007; BC-SKL-04017, BC-SKL-04019, BC-SKL-04022; BC-EK-CHA-3D1, BC-EK-CHA-3D2; ced:90, ced:86, ced:84
- Prediction pr-1 and the contrast pair: BC-CON-04007, BC-ERR-04017
- BC-QA-04006, BC-QA-04007; BC-PT-99023; cr-22:7, cr-24:18, crabbc-25:24
- BC-ERR-04015, BC-ERR-04017, BC-ERR-04018, BC-ERR-99013; BC-MIS-04008, BC-MIS-04009, BC-MIS-99005; BC-PRQ-04008
- research/units/unit-04-contextual-applications-differentiation.md#4.4 Introduction to Related Rates
- research/question-analysis/question-archetypes.md#BC-QA-04006 Related rates in a geometric setting
- research/question-analysis/question-archetypes.md#BC-QA-04007 Related rates on an implicitly defined curve
- research/scoring/notation-requirements.md#Derivative notation
- research/scoring/common-point-losses.md#Units points
- research/exam/exam-structure.md#Section and part layout
- [inferred] The exam part for an either archetype. Settled by a calculator status on BC-QA-04006.
- [inferred] ki-1 as an interactive. Settled by the modality A/B.
- [inferred] The ladder draw's size read as the named leg. Settled by a parameter_spec note.

## Machine record

```json
{
 "id": "LSN-CON-04007",
 "kind": "concept",
 "target_id": "BC-CON-04007",
 "unit": "04",
 "skills": [
  "BC-SKL-04017",
  "BC-SKL-04019",
  "BC-SKL-04022"
 ],
 "prediction": {
  "id": "pr-1",
  "stem": {
   "text": "If x^2 + y^2 = 225 and x, y change in time, what is the t-derivative of the left side?",
   "command_verb": "predict"
  },
  "format": "mcq",
  "options": [
   {
    "id": "A",
    "label": "2x + 2y",
    "is_key": false
   },
   {
    "id": "B",
    "label": "2x dx/dt + 2y dy/dt",
    "is_key": true
   },
   {
    "id": "C",
    "label": "2y dy/dt",
    "is_key": false
   }
  ],
  "resolution": "Each varying quantity brings its own rate factor: 2x dx/dt + 2y dy/dt.",
  "sources": [
   "BC-CON-04007",
   "research/units/unit-04-contextual-applications-differentiation.md#4.4 Introduction to Related Rates"
  ]
 },
 "orientation": {
  "text": "Each changing quantity depends on time; differentiate in t, then substitute the instant.",
  "sources": [
   "BC-CON-04007",
   "research/units/unit-04-contextual-applications-differentiation.md#4.4 Introduction to Related Rates"
  ]
 },
 "key_ideas": [
  {
   "id": "ki-1",
   "ek_id": "BC-EK-CHA-3D1",
   "depth": "core",
   "text": "Each changing quantity is a function of time, so differentiating \\(x^2+y^2=225\\) in \\(t\\) gives \\(2x\\,\\frac{dx}{dt}+2y\\,\\frac{dy}{dt}=0\\): one rate per varying quantity. Instant values go in afterwards.",
   "notation": "dV/dt, dr/dt, dh/dt",
   "quote": {
    "text": "The chain rule is the basis for differentiating variables",
    "source": "ced:90"
   },
   "sources": [
    "BC-EK-CHA-3D1",
    "ced:90",
    "ced:86",
    "research/units/unit-04-contextual-applications-differentiation.md#4.4 Introduction to Related Rates"
   ]
  },
  {
   "id": "ki-2",
   "ek_id": "BC-EK-CHA-3D2",
   "depth": "extended",
   "text": "A term multiplying two changing quantities needs the product rule: \\(\\frac{d}{dt}(xy)=\\frac{dx}{dt}y+x\\frac{dy}{dt}\\), two rate factors, not one.",
   "notation": "dx/dt, dy/dt",
   "quote": {
    "text": "Other differentiation rules, such as the product rule and the quotient rule, may also be necessary",
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
   "cue": "Rates given, instant dimensions, another rate wanted.",
   "method": "Name the varying quantities and write the rates in t.",
   "rival": "Differentiating in a length, not time.",
   "separating_feature": "The wanted rate is per unit of time.",
   "sources": [
    "BC-QA-04006",
    "BC-ERR-04017"
   ],
   "evidence_tag": "verified",
   "contrast": {
    "this": {
     "text": "A 13 foot ladder's foot slides out at 3 feet per second. Find the top's rate when the foot is 5 feet out.",
     "archetype_id": "BC-QA-04006"
    },
    "not_this": {
     "text": "For x^2 + y^2 = 169, find dy/dx at (5, 12).",
     "why_not": "A slope in x: no time."
    },
    "feature": "Wanted rate is per unit of time."
   }
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
    "shape": "ladder",
    "size": 9,
    "rate": 2,
    "ratio": 3,
    "leg": "short",
    "length_unit": "foot",
    "time_unit": "second"
   },
   "problem": {
    "text": "A 15 foot ladder leans on a wall. Its foot slides away at 2 feet per second. When the foot is 9 feet out, how fast is the top moving?",
    "command_verb": "find"
   },
   "calculator_status": "no_calculator",
   "steps": [
    {
     "cue": "\\(x(t)\\), \\(y(t)\\) vary; 15 fixed.",
     "why": "Given \\(dx/dt=2\\); wanted \\(dy/dt\\).",
     "expr": "x**2 + y**2 = 225",
     "relation": "new"
    },
    {
     "cue": "Differentiate in \\(t\\).",
     "why": "One rate per quantity.",
     "expr": "2*x*dxdt + 2*y*dydt = 0",
     "relation": "new",
     "point_type_id": "BC-PT-99023"
    },
    {
     "cue": "Instant: \\(x=9\\), \\(y=12\\), \\(dx/dt=2\\).",
     "why": "\\(y=12\\) from \\(9^2+y^2=225\\).",
     "expr": "36 + 24*dydt = 0",
     "relation": "evaluate",
     "subs": {
      "x": "9",
      "y": "12",
      "dxdt": "2"
     }
    },
    {
     "cue": "Solve.",
     "why": "\\(dy/dt=-3/2\\).",
     "expr": "-3/2",
     "relation": "solve",
     "variable": "dydt"
    },
    {
     "cue": "Report with units.",
     "why": "The top falls 1.5 feet per second."
    }
   ],
   "answer": {
    "form": "numeric",
    "expr": "-3/2"
   }
  },
  {
   "id": "ex-2",
   "archetype_id": "BC-QA-04007",
   "bands": [
    "low"
   ],
   "parameter_draw": {
    "square_x": 2,
    "mixed": 1,
    "square_y": 1,
    "point_x": 1,
    "point_y": -2,
    "rate_x": 3
   },
   "problem": {
    "text": "A particle moves on \\(2x^2+xy+y^2=4\\). At \\((1,-2)\\), \\(dx/dt=3\\). Find \\(dy/dt\\) there.",
    "command_verb": "find"
   },
   "calculator_status": "no_calculator",
   "steps": [
    {
     "cue": "A rate in time supplied, the other asked.",
     "why": "Differentiate in \\(t\\), not \\(x\\).",
     "expr": "2*x**2 + x*y + y**2 = 4",
     "relation": "new"
    },
    {
     "cue": "The term \\(xy\\) multiplies two varying quantities.",
     "why": "Product rule: two rate factors.",
     "expr": "4*x*dxdt + y*dxdt + x*dydt + 2*y*dydt = 0",
     "relation": "new"
    },
    {
     "cue": "Substitute the point and \\(dx/dt=3\\).",
     "why": "\\(12-6+dy/dt-4\\,dy/dt\\).",
     "expr": "6 - 3*dydt = 0",
     "relation": "evaluate",
     "subs": {
      "x": "1",
      "y": "-2",
      "dxdt": "3"
     }
    },
    {
     "cue": "Solve.",
     "why": "\\(dy/dt=2\\).",
     "expr": "2",
     "relation": "solve",
     "variable": "dydt"
    }
   ],
   "answer": {
    "form": "numeric",
    "expr": "2"
   },
   "fade_from": 3
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
   "error_id": "BC-ERR-04015",
   "wrong_step": {
    "text": "\\(dy/dt=2\\), the given rate.",
    "expr": "2"
   },
   "right_step": {
    "text": "\\(dy/dt=-3/2\\).",
    "expr": "-3/2"
   },
   "relation": "distinct",
   "possible_reason": null,
   "sources": [
    "BC-ERR-04015"
   ],
   "observed_behavior": "The rate supplied in the stem is reported as the answer, or the requested rate is treated as known.",
   "scoring_consequence": "The answer point is lost; BC-ERR-99033 records variables introduced without being defined as a related communication failure.",
   "fix_prompt": true
  },
  {
   "error_id": "BC-ERR-04017",
   "wrong_step": {
    "text": "\\(dy/dx=-x/y=-3/4\\), stopped.",
    "expr": "-3/4"
   },
   "right_step": {
    "text": "\\(dy/dt=-3/2\\).",
    "expr": "-3/2"
   },
   "relation": "distinct",
   "possible_reason": {
    "misconception_id": "BC-MIS-04008",
    "text": "the rates with respect to time never appear"
   },
   "sources": [
    "BC-ERR-04017",
    "BC-MIS-04008"
   ],
   "observed_behavior": "The relating equation is differentiated with respect to a length or with respect to x, and the response stops there rather than continuing through the chain rule to a rate with respect to time.",
   "scoring_consequence": "The Chief Reader report for 2024 records that responses differentiating with respect to x needed to continue through the chain rule and that many provided no work beyond that step (cr-24:18); BC-ERR-99013 records the same family across years.",
   "fix_prompt": true
  },
  {
   "error_id": "BC-ERR-04018",
   "wrong_step": {
    "text": "\\(xy\\) differentiated with \\(x\\) held constant.",
    "expr": "4*x*dxdt + x*dydt + 2*y*dydt = 0"
   },
   "right_step": {
    "text": "Product rule on \\(xy\\).",
    "expr": "4*x*dxdt + y*dxdt + x*dydt + 2*y*dydt = 0"
   },
   "relation": "distinct",
   "possible_reason": {
    "misconception_id": "BC-MIS-04009",
    "text": "only one rate factor appears where two are needed"
   },
   "sources": [
    "BC-ERR-04018",
    "BC-MIS-04009"
   ],
   "observed_behavior": "A term that multiplies two varying quantities is differentiated as though one of them were constant.",
   "scoring_consequence": "The completely correct differentiation point is lost; BC-ERR-99013 names the missing product rule explicitly.",
   "fix_prompt": true
  },
  {
   "error_id": "BC-ERR-99013",
   "wrong_step": {
    "text": "\\(dy/dx\\) at \\((1,-2)\\) reported: \\(2/3\\).",
    "expr": "2/3"
   },
   "right_step": {
    "text": "\\(dy/dt=2\\).",
    "expr": "2"
   },
   "relation": "distinct",
   "possible_reason": {
    "misconception_id": "BC-MIS-99005",
    "text": "implicit differentiation with respect to time is carried out with respect to x"
   },
   "sources": [
    "BC-ERR-99013",
    "BC-MIS-99005"
   ],
   "observed_behavior": "Responses differentiate an implicit relation with respect to x when time is the independent variable, omit the product rule on a product of two changing quantities, or treat one quantity as constant, and confuse the notations for the several derivatives in play.",
   "scoring_consequence": "The differentiation points in the part are not earned, and the numerical answer point depends on them.",
   "fix_prompt": true
  }
 ],
 "representations": null,
 "prerequisite_bridges": [
  {
   "prq_id": "BC-PRQ-04008",
   "text": "Name each quantity, unit and whether it varies."
  }
 ],
 "time": {
  "exam_part": "I-A",
  "budget_minutes": 2.14,
  "source": "research/exam/exam-structure.md#Section and part layout",
  "written_steps": {
   "ex-1": [
    1,
    2,
    3,
    4,
    5
   ],
   "ex-2": [
    2,
    3,
    4
   ]
  },
  "skipped_steps": {
   "ex-1": [],
   "ex-2": [
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
   "archetype_id": "BC-QA-04006",
   "parameter_draw": {
    "shape": "ladder",
    "size": 9,
    "rate": 2,
    "ratio": 3,
    "leg": "short",
    "length_unit": "foot",
    "time_unit": "second"
   },
   "completes": "ex-1",
   "stem": {
    "text": "\\(2(9)(2)+2(12)\\,dy/dt=0\\). Find \\(dy/dt\\) with units.",
    "command_verb": "find"
   },
   "key": {
    "form": "numeric",
    "expr": "-3/2"
   },
   "steps": [
    {
     "text": "Substituted.",
     "expr": "36 + 24*dydt = 0",
     "relation": "new"
    },
    {
     "text": "-3/2 feet per second.",
     "expr": "-3/2",
     "relation": "solve",
     "variable": "dydt"
    }
   ],
   "calculator_status": "no_calculator",
   "skills": [
    "BC-SKL-04019"
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
    "shape": "circle",
    "size": 6,
    "rate": 2,
    "ratio": 1,
    "leg": "short",
    "length_unit": "centimeter",
    "time_unit": "minute"
   },
   "stem": {
    "text": "A circle's radius grows at 2 centimeters per minute. How fast is its area growing when the radius is 6 centimeters?",
    "command_verb": "find"
   },
   "key": {
    "form": "symbolic",
    "expr": "24*pi"
   },
   "steps": [
    {
     "text": "dA/dt = 2 pi r dr/dt.",
     "expr": "2*pi*r*drdt",
     "relation": "new"
    },
    {
     "text": "r = 6, dr/dt = 2.",
     "expr": "24*pi",
     "relation": "evaluate",
     "subs": {
      "r": "6",
      "drdt": "2"
     }
    }
   ],
   "calculator_status": "no_calculator",
   "skills": [
    "BC-SKL-04017",
    "BC-SKL-04019"
   ]
  },
  {
   "id": "chk-3",
   "check_kind": "mcq",
   "format": "mcq",
   "bands": [
    "low"
   ],
   "archetype_id": "BC-QA-04007",
   "parameter_draw": {
    "square_x": 1,
    "mixed": 3,
    "square_y": 2,
    "point_x": 1,
    "point_y": 1,
    "rate_x": 2
   },
   "stem": {
    "text": "On \\(x^2+3xy+2y^2=6\\), at \\((1,1)\\), \\(dx/dt=2\\). What is \\(dy/dt\\)?",
    "command_verb": "find"
   },
   "key": {
    "form": "numeric",
    "expr": "-10/7"
   },
   "steps": [
    {
     "text": "Differentiate in t.",
     "expr": "2*x*dxdt + 3*y*dxdt + 3*x*dydt + 4*y*dydt = 0",
     "relation": "new"
    },
    {
     "text": "Substitute.",
     "expr": "10 + 7*dydt = 0",
     "relation": "evaluate",
     "subs": {
      "x": "1",
      "y": "1",
      "dxdt": "2"
     }
    },
    {
     "text": "Solve.",
     "expr": "-10/7",
     "relation": "solve",
     "variable": "dydt"
    }
   ],
   "options": [
    {
     "id": "A",
     "is_key": true,
     "expr": "-10/7",
     "error_path": null
    },
    {
     "id": "B",
     "is_key": false,
     "expr": "2",
     "error_path": "BC-ERR-04015",
     "derivation": "the supplied rate dx/dt reported as dy/dt"
    },
    {
     "id": "C",
     "is_key": false,
     "expr": "-4/7",
     "error_path": "BC-ERR-04018",
     "derivation": "3xy differentiated with x held constant, so the 3y dx/dt term is lost: 4 + 7 dy/dt = 0"
    },
    {
     "id": "D",
     "is_key": false,
     "expr": "-5/7",
     "error_path": "BC-ERR-99013",
     "derivation": "dy/dx = -(2x + 3y)/(3x + 4y) reported where dy/dt is needed"
    }
   ],
   "calculator_status": "no_calculator",
   "skills": [
    "BC-SKL-04022"
   ]
  }
 ],
 "delivery": [
  {
   "block": "orientation",
   "mode": "text",
   "reason": "rule 5 for a statement of what a response shows; the figure-bearing BC-REP-08 is served once, on ki-1",
   "sources": [
    "BC-SKL-04017"
   ]
  },
  {
   "block": "ki-1",
   "mode": "interactive",
   "reason": "rule 3 promoted: BC-REP-08 in BC-SKL-04017, BC-REP-02 in BC-SKL-04022; BC-QA-04006 common_givens name the dimensions at the instant and a figure of the configuration, and the reading is which labels change as time moves",
   "sources": [
    "BC-SKL-04017",
    "BC-SKL-04022",
    "BC-QA-04006"
   ],
   "spec": {
    "kind": "geometric_diagram",
    "representations": [
     "BC-REP-08",
     "BC-REP-01"
    ],
    "controls": [
     {
      "type": "slider",
      "variable": "x",
      "range": [
       1,
       14
      ],
      "step": 0.5,
      "start": 9
     }
    ],
    "drawn": [
     "the wall, the ground and the ladder as a segment",
     "the foot at distance x from the wall and the top at height y"
    ],
    "labels": [
     {
      "text": "ladder 15 ft (fixed)",
      "placement": "inside",
      "at": [
       5,
       7
      ]
     },
     {
      "text": "x(t): foot to wall",
      "placement": "inside",
      "at": [
       3,
       1
      ]
     },
     {
      "text": "y(t): top height",
      "placement": "inside",
      "at": [
       0.5,
       14.5
      ]
     },
     {
      "text": "x = 9, y = 12 only at this instant",
      "placement": "inside",
      "at": [
       7,
       13
      ]
     }
    ],
    "question": "As the foot slides out, which labelled lengths change and which stay fixed?",
    "window": {
     "x": [
      -1,
      16
     ],
     "y": [
      -1,
      16
     ]
    },
    "segments": [
     {
      "from": [
       0,
       0
      ],
      "to": [
       0,
       15.5
      ]
     },
     {
      "from": [
       0,
       0
      ],
      "to": [
       15.5,
       0
      ]
     },
     {
      "from": [
       9,
       0
      ],
      "to": [
       0,
       12
      ]
     }
    ],
    "points": [
     {
      "x": "x",
      "y": 0
     },
     {
      "x": 0,
      "y": "sqrt(225 - x**2)"
     }
    ]
   },
   "fallback": "two static frames of the ladder at x = 9 and x = 12, with 15 fixed and x and y labelled inside each",
   "keyboard": "Tab focuses the slider; left and right arrow keys move the foot by 0.5 feet; Enter reads out x, y and the fixed length"
  },
  {
   "block": "ki-2",
   "mode": "text",
   "reason": "rule 5: CHA-3D2, the product rule, rests on BC-REP-01",
   "sources": [
    "BC-SKL-04022"
   ]
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
   "block": "err-BC-ERR-04015",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  },
  {
   "block": "err-BC-ERR-04017",
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
   "block": "err-BC-ERR-99013",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  }
 ],
 "refresher": [
  "ki-1",
  "err-BC-ERR-04015",
  "err-BC-ERR-04017",
  "err-BC-ERR-04018",
  "err-BC-ERR-99013",
  "ex-1"
 ],
 "research_lines": [
  {
   "file": "research/scoring/common-point-losses.md",
   "line": "Units are scored separately from the value"
  }
 ],
 "inferred": [
  {
   "claim": "BC-QA-04006 is calculator status either, so the lesson times it as Section I Part A at 2.14 minutes.",
   "settles": "A calculator status of calculator or no_calculator on BC-QA-04006."
  },
  {
   "claim": "ki-1 is served as an interactive slider on the ladder's foot rather than a static figure; the unit README's delivery table lists figure for this concept while its CHA-3D1 entry and its interactive note name the slider.",
   "settles": "The modality A/B in the build plan: skip rate and time to first credited success by mode."
  },
  {
   "claim": "For the ladder the draw's size is read as the leg named by leg, so short leg 9 with ratio 3 gives the 9, 12, 15 triangle; the parameter_spec notes do not define size for the ladder.",
   "settles": "A parameter_spec note on BC-QA-04006 defining size for each shape."
  }
 ],
 "sources": [
  "BC-CON-04007",
  "BC-SKL-04017",
  "BC-SKL-04019",
  "BC-SKL-04022",
  "BC-EK-CHA-3D1",
  "BC-EK-CHA-3D2",
  "ced:90",
  "ced:86",
  "ced:84",
  "cr-22:7",
  "cr-24:18",
  "crabbc-25:24",
  "BC-QA-04006",
  "BC-QA-04007",
  "BC-PT-99023",
  "BC-ERR-04015",
  "BC-ERR-04017",
  "BC-ERR-04018",
  "BC-ERR-99013",
  "BC-MIS-04008",
  "BC-MIS-04009",
  "BC-MIS-99005",
  "BC-PRQ-04008",
  "research/units/unit-04-contextual-applications-differentiation.md#4.4 Introduction to Related Rates",
  "research/question-analysis/question-archetypes.md#BC-QA-04006 Related rates in a geometric setting",
  "research/question-analysis/question-archetypes.md#BC-QA-04007 Related rates on an implicitly defined curve",
  "research/scoring/notation-requirements.md#Derivative notation",
  "research/scoring/common-point-losses.md#Units points",
  "research/exam/exam-structure.md#Section and part layout"
 ],
 "word_count": {
  "full": 660,
  "brief": 447
 },
 "read_minutes": {
  "full": 4.5,
  "brief": 3.0
 }
}
```
