---
title: LSN-CON-07008 Particular solution selected by an initial condition
research_date: 2026-09-29
status: designed
purpose: Authoring spec for the concept lesson on BC-CON-07008, the particular solution an initial condition selects, built from authoring_bundle("BC-CON-07008") and the research files it cites, so an author fills plan 15's lesson record without making a teaching decision.
---

# LSN-CON-07008 Particular solution selected by an initial condition

Concept BC-CON-07008 (skills BC-SKL-07029, BC-SKL-07030, BC-SKL-07032, BC-SKL-07033), topic 7.7 of Unit 7, loaded by BC-QA-07011, BC-QA-07003 and BC-QA-07007. Its hard parents in Unit 7 are BC-CON-07001, BC-CON-07003 and BC-CON-07007 (docs/lessons/unit-07/README.md, section 1).

## Prediction

Both bands, served first, before any rule. Form `mcq`, three options, on ex-1's equation \(dy/dx=2e^{-x^2}\) and the point \((1,3)\): the student is told that its solutions differ by a constant and says how many pass through the point. Key: exactly one. The distractors are infinitely many and none because no formula for \(y\) exists. The resolution states that the solutions differ by a constant, so one passes through the point and the initial condition picks it, and never grades the choice. Sources: BC-CON-07008 and the 7.7 topic section that ki-1 cites (BC-EK-FUN-7E1, ced:143). Delivery: text. [inferred] Settled by the prediction's first-try rate in the build plan.

## Orientation

Served text, from BC-CON-07008 `description_plain` and the topic's Assessment behaviour paragraph (research/units/unit-07-differential-equations.md#7.7 Finding Particular Solutions Using Initial Conditions and Separation of Variables): the constant is fixed by substituting into the equation that holds it, the same values choose the sign, and the answer is one function.

## Key ideas

- ki-1 (core, both bands), BC-EK-FUN-7E1 (ced:143). Paraphrase of the Uniqueness through a point, Sign and branch, and Timing of the substitution paragraphs (sg-23:11, sg-23:12, sg-24:11). Notation line from the concept record. No anchor quote.
- ki-2 (extended, low band), BC-EK-FUN-7E2 (ced:143). Paraphrase of the Accumulation form paragraph. Notation: F(a) equal to the initial value.

## Recognition

BC-QA-07011 (research/question-analysis/question-archetypes.md#BC-QA-07011 Particular solution with a domain restriction or an accumulation form): `typical_wording` "find the particular solution to the differential equation with the given initial condition"; `common_givens` a differential equation and an initial condition. The signal for the accumulation form: a right side in x alone with no elementary antiderivative. No `official_examples`.

BC-QA-07003 (research/question-analysis/question-archetypes.md#BC-QA-07003 Particular solution by separation of variables): "with the given initial condition" beside "use separation of variables"; the constant and the explicit solution are distinct points (BC-FRQ-2023-Q3-D, BC-FRQ-2024-Q3-C).

BC-QA-07007: "show that the given function is a solution" with an initial condition to check (BC-FRQ-2015-Q4-D).

Not this concept: "general solution" with no stated value asks for the family (BC-CON-07003).

The contrast pair on st-1 sets a particular-solution stem beside its near miss. Where the near miss comes from: the sibling concept BC-CON-07003, so the near-miss stem gives the same equation with no initial condition and asks for the general solution, the family. The separating feature is the initial condition.

## Method choice

- st-1, BC-QA-07011, both bands. Method, `expected_solution_path[0]`: produce the general solution; for a right side in x alone that is the initial value plus an integral. Rival, `wrong_approaches`: choosing the branch by the sign of the constant. Separating feature: the initial condition fixes value and branch.
- st-2, BC-QA-07003, low band. Method: substitute the initial condition into the equation holding C (`expected_solution_path` step 4). Rival, `wrong_approaches`: treating the dependent variable as a constant.
- BC-QA-07007 gets no block: the full band reaches its 900-word cap, and verification is LSN-CON-07002's method [inferred].

Both archetypes carry `asked_to_produce` and `common_givens`. The reader prints its own labels, so no field starts with one, and no method begins with a label such as "First written line". st-1 carries the contrast pair: a particular-solution stem beside a general-solution stem.

## Solution path

- ex-1, BC-QA-07011, both bands, no calculator. Draw: form accumulation, rate 2, initial 3, start 1, integrand gauss, read as dy/dx = 2e^(-x^2) with y(1) = 3 [inferred reading of the labels]. No published BC-QA-07011 draw matches. Steps: the right side (new); the choice of the lower limit (no value); the accumulation function (integrate in x).
- ex-2, BC-QA-07003, low band, no calculator. Draw: square_root, rate 2, power 1, start 1, initial 3 (9 is not 2 * 1^2), so dy/dx = 2x/y with y(1) = 3. No published draw matches. Steps: separated (new); antiderivatives with C (new); initial values into the equation holding C (evaluate); C (solve); the positive root (new).
- ex-2 is faded, `fade_from` 4: steps 1 to 3 (the separated equation, the antiderivatives with C and the initial values substituted into the equation holding C) are shown, and the student solves for C and writes the positive root before steps 4 and 5 reveal. The fade falls there because the last two steps are the constant and the branch, the two things the concept fixes (sg-23:12).
- A fluent solver writes ex-1's lines 1 and 3 and every line of ex-2; the choice of limit is held [inferred].

## Scoring

ex-1's archetype BC-QA-07011 lists no `point_types`, so ex-1 carries no reader lines and no tags. ex-2's archetype BC-QA-07003 lists BC-PT-99028, 99029, 99031, 99032, 99033, 99030; ex-2 tags 99028, 99029, 99031, 99032, and the lines are reader_checks output. The constant point is earned by including the constant in an equation and substituting the initial values into it (sg-23:12). Point losses: BC-ERR-99014 (research/scoring/common-point-losses.md#Setup points).

## Traps

Six errors meet the skills; all four served are distinct, so each carries `fix_prompt` true; the first four in the bundle's order are served: BC-ERR-07009, BC-ERR-07029, BC-ERR-07033, BC-ERR-99014. Mid band the first two. All on ex-2's draw, where the constant and the branch live.

- err-BC-ERR-07009: the family given as the answer. Possible reason from BC-MIS-07005.
- err-BC-ERR-07029: C = 7/2 carried into the rooted form. No possible reason line: the linked descriptions do not name the change of form.
- err-BC-ERR-07033: C fixed where the general solution was asked for. No possible reason line.
- err-BC-ERR-99014: y left in the denominator. No possible reason line.

## Representations

None. The topic's Representations paragraph names BC-REP-01, BC-REP-05 and BC-REP-06 with symbolic conversions only.

## Prerequisite bridge

- BC-PRQ-07004, from its `description_plain` and `failure_signature`.

## Time

BC-QA-07011 is `no_calculator`, one FRQ part or one MCQ; the FRQ form is taken, Section II Part B, 15.0 minutes per question (research/exam/exam-structure.md#Section and part layout) [inferred]. The constant and answer lines of BC-QA-07003 are 2 of its 4 or 5 points (docs/lessons/unit-07/README.md, section 5). The minutes go on the substitution line and the branch.

## Checks

- chk-1, completion of ex-1, both bands. Key 3 plus the integral from 1 to x of 2e^(-t^2).
- chk-2, isomorph on BC-QA-07011, both bands. Draw: accumulation, rate -1, initial 2, start 0, integrand sine. Key 2 plus the integral from 0 to x of -sin(t^2).
- chk-3, MCQ on BC-QA-07003, low band. Draw: square_root, rate 3, power 1, start 2, initial 4 (16 is not 12). Key sqrt(3x^2 + 4). Distractors: sqrt(3x^2 + C) (BC-ERR-07009), sqrt(3x^2 + 2) (BC-ERR-07029), 4e^(3x^2/2 - 6) (BC-ERR-99014).

## Delivery

- pr-1: text. Rule 6, a prediction on the first example's equation with nothing to draw.
- orientation, ki-1, ki-2: text, rule 6. BC-REP-01, 04, 06 only (docs/lessons/unit-07/README.md, section 6).
- ex-1, ex-2 and the four error blocks: step_reveal, rule 1.

Figure presence: no drawn block. No rule of 2 to 5 applies, because the skills carry only symbolic, verbal and differential-equation representations (BC-REP-01, 04, 06) and no key idea describes a process, so the record carries `no_figure_reason`.

## Band plan

- Low (full): prediction, orientation, bridge, ki-1, ki-2, st-1 with its contrast, st-2, ex-1, chk-1, the four error blocks, ex-2 faded with its four reader lines, chk-2, chk-3. 894 words, 6.0 minutes (cap 900 and 6). To fit under 900 the extended ki-2, ex-2's cues and whys, st-2, the bridge and the orientation were shortened.
- Mid (brief): prediction, orientation, bridge, ki-1, st-1 with its contrast, ex-1, chk-1, err-BC-ERR-07009, err-BC-ERR-07029, chk-2. 411 words, 2.8 minutes (cap 450 and 3).
- Refresher: ki-1, the four error blocks, ex-1.

## Sources

- BC-CON-07008; BC-SKL-07029, BC-SKL-07030, BC-SKL-07032, BC-SKL-07033; BC-EK-FUN-7E1, BC-EK-FUN-7E2; ced:143
- BC-QA-07011, BC-QA-07003, BC-QA-07007; BC-PT-99028, BC-PT-99029, BC-PT-99031, BC-PT-99032
- BC-ERR-07009, BC-ERR-07029, BC-ERR-07033, BC-ERR-99014; BC-MIS-07005
- BC-PRQ-07004
- sg-23:11, sg-23:12, sg-24:11, sg-26:13
- research/units/unit-07-differential-equations.md#7.7 Finding Particular Solutions Using Initial Conditions and Separation of Variables
- research/question-analysis/question-archetypes.md#BC-QA-07011 Particular solution with a domain restriction or an accumulation form
- research/question-analysis/question-archetypes.md#BC-QA-07003 Particular solution by separation of variables
- research/scoring/common-point-losses.md#Setup points
- research/exam/exam-structure.md#Section and part layout
- [inferred] Integrand labels read as e^(-t^2) and sin(t^2). Settled by an integrand table in the spec.
- [inferred] rate multiplies the integrand. Settled by the generator's rendering.
- [inferred] Two strategy blocks for one family, none for BC-QA-07007. Settled by a template ruling.
- [inferred] BC-PT-99030 untagged. Settled by a two-tag ruling.
- [inferred] ex-1 from BC-QA-07011, ex-2 carries the points. Settled by the band A/B.
- [inferred] Part II-B. Settled by a BC-PT mapping for BC-QA-07011.

## Machine record

```json
{
 "id": "LSN-CON-07008",
 "kind": "concept",
 "target_id": "BC-CON-07008",
 "unit": "07",
 "skills": [
  "BC-SKL-07029",
  "BC-SKL-07030",
  "BC-SKL-07032",
  "BC-SKL-07033"
 ],
 "prediction": {
  "id": "pr-1",
  "stem": {
   "text": "Every solution of \\(dy/dx=2e^{-x^2}\\) differs from another by a constant. How many pass through \\((1,3)\\)?",
   "command_verb": "predict"
  },
  "format": "mcq",
  "options": [
   {
    "id": "A",
    "label": "Exactly one.",
    "is_key": true
   },
   {
    "id": "B",
    "label": "Infinitely many.",
    "is_key": false
   },
   {
    "id": "C",
    "label": "None, because no formula for \\(y\\) exists.",
    "is_key": false
   }
  ],
  "resolution": "The solutions differ by a constant, so exactly one passes through \\((1,3)\\). The initial condition picks that one.",
  "sources": [
   "BC-CON-07008",
   "BC-EK-FUN-7E1",
   "ced:143",
   "research/units/unit-07-differential-equations.md#7.7 Finding Particular Solutions Using Initial Conditions and Separation of Variables"
  ]
 },
 "no_figure_reason": "The skills carry symbolic, verbal and differential-equation representations, none figure-bearing, and no key idea describes a process. The content is written lines that fix a constant and a sign.",
 "orientation": {
  "text": "A response substitutes the initial values into the equation that holds the constant, before its form changes, and uses them to choose the sign. The answer is one function.",
  "sources": [
   "BC-CON-07008",
   "research/units/unit-07-differential-equations.md#7.7 Finding Particular Solutions Using Initial Conditions and Separation of Variables"
  ]
 },
 "key_ideas": [
  {
   "id": "ki-1",
   "ek_id": "BC-EK-FUN-7E1",
   "depth": "core",
   "text": "A general solution describes infinitely many solutions; exactly one passes through a given point. The initial values go into the equation holding C, before exponentiating or squaring changes its form, and they settle the sign of the branch.",
   "notation": "particular solution; initial condition",
   "quote": null,
   "sources": [
    "BC-EK-FUN-7E1",
    "ced:143",
    "research/units/unit-07-differential-equations.md#7.7 Finding Particular Solutions Using Initial Conditions and Separation of Variables",
    "sg-23:12"
   ]
  },
  {
   "id": "ki-2",
   "ek_id": "BC-EK-FUN-7E2",
   "depth": "extended",
   "text": "When dy/dx depends on x alone, the solution through (a, y0) is y0 plus the integral of the right side from a to x.",
   "notation": "F(a) equal to the initial value",
   "quote": null,
   "sources": [
    "BC-EK-FUN-7E2",
    "ced:143",
    "research/units/unit-07-differential-equations.md#7.7 Finding Particular Solutions Using Initial Conditions and Separation of Variables"
   ]
  }
 ],
 "strategy": [
  {
   "id": "st-1",
   "archetype_id": "BC-QA-07011",
   "cue": "An x-only equation and an initial condition: the particular solution.",
   "method": "The initial value plus an integral from the initial input to x.",
   "rival": "Choosing the branch by the constant's sign.",
   "separating_feature": "The initial condition, not C, fixes the value and the branch.",
   "sources": [
    "BC-QA-07011"
   ],
   "evidence_tag": "verified",
   "contrast": {
    "this": {
     "text": "\\(dy/dx=5e^{-x^2}\\) with \\(y(2)=1\\). Write the particular solution.",
     "archetype_id": "BC-QA-07011"
    },
    "not_this": {
     "text": "\\(dy/dx=5e^{-x^2}\\). Write the general solution.",
     "why_not": "No initial condition, so it asks for the family."
    },
    "feature": "An initial condition asks for one function."
   }
  },
  {
   "id": "st-2",
   "archetype_id": "BC-QA-07003",
   "cue": "Separation with an initial condition.",
   "method": "After the antiderivatives, the initial values go into the equation holding C.",
   "rival": "Treating the equation as though the dependent variable were a constant.",
   "separating_feature": "C is fixed while it still stands alone.",
   "sources": [
    "BC-QA-07003"
   ],
   "evidence_tag": "verified"
  }
 ],
 "worked_examples": [
  {
   "id": "ex-1",
   "archetype_id": "BC-QA-07011",
   "bands": [
    "low",
    "mid"
   ],
   "parameter_draw": {
    "form": "accumulation",
    "rate": 2,
    "initial": "3",
    "start": 1,
    "integrand": "gauss"
   },
   "problem": {
    "text": "dy/dx = 2e^(-x^2) with y(1) = 3. Write the particular solution.",
    "command_verb": "write"
   },
   "calculator_status": "no_calculator",
   "steps": [
    {
     "cue": "The right side holds x only, with no elementary antiderivative.",
     "why": "So the solution is an accumulation function.",
     "expr": "2*exp(-x**2)",
     "relation": "new"
    },
    {
     "cue": "The initial input is 1 and the initial value 3.",
     "why": "The integral starts at 1, where it is zero, so 3 is added."
    },
    {
     "cue": "Initial value plus the integral from 1 to x.",
     "why": "Its derivative is 2e^(-x^2) and F(1) = 3.",
     "expr": "y = 3 + Integral(2*exp(-t**2), (t, 1, x))",
     "relation": "integrate",
     "variable": "x"
    }
   ],
   "answer": {
    "form": "symbolic",
    "expr": "3 + Integral(2*exp(-t**2), (t, 1, x))"
   }
  },
  {
   "id": "ex-2",
   "archetype_id": "BC-QA-07003",
   "bands": [
    "low"
   ],
   "parameter_draw": {
    "form": "square_root",
    "rate": 2,
    "power": 1,
    "start": 1,
    "initial": 3
   },
   "problem": {
    "text": "dy/dx = 2x/y with y(1) = 3. Find the particular solution y = f(x).",
    "command_verb": "find"
   },
   "calculator_status": "no_calculator",
   "steps": [
    {
     "cue": "2x/y is 2x times 1/y.",
     "why": "Multiply by y and dx.",
     "expr": "y*dy = 2*x*dx",
     "relation": "new",
     "point_type_id": "BC-PT-99028"
    },
    {
     "cue": "One variable per side.",
     "why": "Integrate each; one C.",
     "expr": "y**2/2 = x**2 + C",
     "relation": "new",
     "point_type_id": "BC-PT-99029"
    },
    {
     "cue": "y(1) = 3, and C still stands alone.",
     "why": "Substitute before squaring or rooting.",
     "expr": "9/2 = 1 + C",
     "relation": "evaluate",
     "subs": {
      "x": "1",
      "y": "3"
     },
     "point_type_id": "BC-PT-99031"
    },
    {
     "cue": "One unknown.",
     "why": "Solve for C.",
     "expr": "7/2",
     "relation": "solve",
     "variable": "C"
    },
    {
     "cue": "The stem asks for y.",
     "why": "Positive root: y(1) = 3 > 0.",
     "expr": "y = sqrt(2*x**2 + 7)",
     "relation": "new",
     "point_type_id": "BC-PT-99032"
    }
   ],
   "answer": {
    "form": "symbolic",
    "expr": "sqrt(2*x**2 + 7)"
   },
   "fade_from": 4
  }
 ],
 "what_a_reader_scores": [
  {
   "example_id": "ex-2",
   "point_type_ids": [
    "BC-PT-99028",
    "BC-PT-99029",
    "BC-PT-99031",
    "BC-PT-99032"
   ],
   "lines": [
    {
     "point_type_id": "BC-PT-99028",
     "text": "Separation of variables. Earned by: Rearranging the differential equation so each variable sits with its own differential, in the form constant times the dependent differential over the dependent expression equals constant times the independent differential (sg-26:13). Not earned by: Any attempt that leaves both variables on the same side; sg-26:13, sg-23:12, sg-21:20 and sg-19:5 all state that without separation the entire part scores zero."
    },
    {
     "point_type_id": "BC-PT-99029",
     "text": "First antiderivative in a separated equation. Earned by: One consistent antiderivative, either the logarithmic side written with parentheses or absolute value, or the independent-variable side (sg-26:13). Not earned by: An antiderivative inconsistent with the separated form (sg-26:13). Notation: sg-26:13 accepts either parentheses or absolute value on the logarithm; sg-23:12 states an antiderivative written without absolute value symbols stays eligible for all points; sg-21:20 accepts either form."
    },
    {
     "point_type_id": "BC-PT-99031",
     "text": "Constant of integration used with the initial condition. Earned by: Including the constant in an equation and substituting the given initial values to solve for it (sg-26:13, sg-21:20). Not earned by: Work with no constant of integration at all, which sg-26:13 and sg-23:12 state blocks this point and the solve point."
    },
    {
     "point_type_id": "BC-PT-99032",
     "text": "Solves for the particular solution. Earned by: Isolating the dependent variable to give the particular solution, in any equivalent exponential form (sg-26:13). Not earned by: A solution left in implicit logarithmic form; a solution with no constant of integration shown anywhere (sg-26:13)."
    }
   ]
  }
 ],
 "common_errors": [
  {
   "error_id": "BC-ERR-07009",
   "observed_behavior": "The response treats the family with its constant as a single function.",
   "scoring_consequence": "The distinction the essential knowledge draws between a family and a particular solution is lost.",
   "wrong_step": {
    "text": "y = sqrt(2x^2 + C) given as the solution.",
    "expr": "y = sqrt(2*x**2 + C)"
   },
   "right_step": {
    "text": "y(1) = 3 picks one member.",
    "expr": "y = sqrt(2*x**2 + 7)"
   },
   "relation": "distinct",
   "possible_reason": {
    "misconception_id": "BC-MIS-07005",
    "text": "the family and the constant have no role"
   },
   "sources": [
    "BC-ERR-07009",
    "BC-MIS-07005"
   ],
   "fix_prompt": true
  },
  {
   "error_id": "BC-ERR-07029",
   "observed_behavior": "The response exponentiates first and then substitutes the initial condition into an expression where the constant has changed form.",
   "scoring_consequence": "The constant point is at risk; the guideline earns it for including the constant in an equation and substituting the initial values into it.",
   "wrong_step": {
    "text": "C = 7/2 put into y = sqrt(2x^2 + C).",
    "expr": "y = sqrt(2*x**2 + 7/2)"
   },
   "right_step": {
    "text": "C = 7/2 in y^2/2 = x^2 + C.",
    "expr": "y = sqrt(2*x**2 + 7)"
   },
   "relation": "distinct",
   "possible_reason": null,
   "sources": [
    "BC-ERR-07029"
   ],
   "fix_prompt": true
  },
  {
   "error_id": "BC-ERR-07033",
   "observed_behavior": "The response reports a formula with an undetermined constant where a particular solution was asked for, or fixes the constant where the general solution was asked for.",
   "scoring_consequence": "The answer is of the wrong kind for the question posed.",
   "wrong_step": {
    "text": "General solution asked; C fixed at 7/2 anyway.",
    "expr": "y**2 = 2*x**2 + 7"
   },
   "right_step": {
    "text": "General solution: C left free.",
    "expr": "y**2 = 2*x**2 + C"
   },
   "relation": "distinct",
   "possible_reason": null,
   "sources": [
    "BC-ERR-07033"
   ],
   "fix_prompt": true
  },
  {
   "error_id": "BC-ERR-99014",
   "observed_behavior": "Responses leave a variable on the wrong side of the separation, misplace a constant factor, produce an incorrect antiderivative of a trigonometric or reciprocal term, or mishandle the sign and the absolute value in a logarithm before solving for the dependent variable.",
   "scoring_consequence": "The separation, antiderivative and constant points are assessed separately, so an early slip costs several points in the part.",
   "wrong_step": {
    "text": "y left in the denominator.",
    "expr": "dy/y = 2*x*dx"
   },
   "right_step": {
    "text": "y multiplied across.",
    "expr": "y*dy = 2*x*dx"
   },
   "relation": "distinct",
   "possible_reason": null,
   "sources": [
    "BC-ERR-99014"
   ],
   "fix_prompt": true
  }
 ],
 "representations": null,
 "prerequisite_bridges": [
  {
   "prq_id": "BC-PRQ-07004",
   "text": "The given point decides the sign inside an absolute value or a root."
  }
 ],
 "time": {
  "exam_part": "II-B",
  "budget_minutes": 15.0,
  "source": "research/exam/exam-structure.md#Section and part layout",
  "written_steps": {
   "ex-1": [
    1,
    3
   ],
   "ex-2": [
    1,
    2,
    3,
    4,
    5
   ]
  },
  "skipped_steps": {
   "ex-1": [
    2
   ],
   "ex-2": []
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
   "archetype_id": "BC-QA-07011",
   "parameter_draw": {
    "form": "accumulation",
    "rate": 2,
    "initial": "3",
    "start": 1,
    "integrand": "gauss"
   },
   "completes": "ex-1",
   "stem": {
    "text": "dy/dx = 2e^(-x^2), y(1) = 3. The integral from 1 to x of 2e^(-t^2) dt is zero at x = 1. Write y.",
    "command_verb": "write"
   },
   "key": {
    "form": "symbolic",
    "expr": "3 + Integral(2*exp(-t**2), (t, 1, x))"
   },
   "steps": [
    {
     "text": "The right side.",
     "expr": "2*exp(-x**2)",
     "relation": "new"
    },
    {
     "text": "Initial value plus the integral from 1.",
     "expr": "3 + Integral(2*exp(-t**2), (t, 1, x))",
     "relation": "integrate",
     "variable": "x"
    }
   ],
   "calculator_status": "no_calculator",
   "skills": [
    "BC-SKL-07032"
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
   "archetype_id": "BC-QA-07011",
   "parameter_draw": {
    "form": "accumulation",
    "rate": -1,
    "initial": "2",
    "start": 0,
    "integrand": "sine"
   },
   "stem": {
    "text": "dy/dx = -sin(x^2) with y(0) = 2. Write the particular solution.",
    "command_verb": "write"
   },
   "key": {
    "form": "symbolic",
    "expr": "2 + Integral(-sin(t**2), (t, 0, x))"
   },
   "steps": [
    {
     "text": "The right side.",
     "expr": "-sin(x**2)",
     "relation": "new"
    },
    {
     "text": "Initial value plus the integral from 0.",
     "expr": "2 + Integral(-sin(t**2), (t, 0, x))",
     "relation": "integrate",
     "variable": "x"
    }
   ],
   "calculator_status": "no_calculator",
   "skills": [
    "BC-SKL-07032"
   ]
  },
  {
   "id": "chk-3",
   "check_kind": "mcq",
   "format": "mcq",
   "bands": [
    "low"
   ],
   "archetype_id": "BC-QA-07003",
   "parameter_draw": {
    "form": "square_root",
    "rate": 3,
    "power": 1,
    "start": 2,
    "initial": 4
   },
   "stem": {
    "text": "dy/dx = 3x/y with y(2) = 4. Which is the particular solution?",
    "command_verb": "identify"
   },
   "key": {
    "form": "symbolic",
    "expr": "sqrt(3*x**2 + 4)"
   },
   "steps": [
    {
     "text": "Separate.",
     "expr": "y*dy = 3*x*dx",
     "relation": "new"
    },
    {
     "text": "Integrate.",
     "expr": "y**2/2 = 3*x**2/2 + C",
     "relation": "new"
    },
    {
     "text": "x = 2, y = 4.",
     "expr": "8 = 6 + C",
     "relation": "evaluate",
     "subs": {
      "x": "2",
      "y": "4"
     }
    },
    {
     "text": "C.",
     "expr": "2",
     "relation": "solve",
     "variable": "C"
    },
    {
     "text": "Positive root, since y(2) > 0.",
     "expr": "y = sqrt(3*x**2 + 4)",
     "relation": "new"
    }
   ],
   "options": [
    {
     "id": "A",
     "is_key": false,
     "expr": "sqrt(3*x**2 + C)",
     "error_path": "BC-ERR-07009",
     "derivation": "the family reported with C left in"
    },
    {
     "id": "B",
     "is_key": true,
     "expr": "sqrt(3*x**2 + 4)",
     "error_path": null
    },
    {
     "id": "C",
     "is_key": false,
     "expr": "sqrt(3*x**2 + 2)",
     "error_path": "BC-ERR-07029",
     "derivation": "C = 2 from y^2/2 = 3x^2/2 + C put into y = sqrt(3x^2 + C)"
    },
    {
     "id": "D",
     "is_key": false,
     "expr": "4*exp(3*x**2/2 - 6)",
     "error_path": "BC-ERR-99014",
     "derivation": "y left in the denominator: dy/y = 3x dx"
    }
   ],
   "calculator_status": "no_calculator",
   "skills": [
    "BC-SKL-07029",
    "BC-SKL-07030"
   ]
  }
 ],
 "delivery": [
  {
   "block": "pr-1",
   "mode": "text",
   "reason": "rule 6: a prediction on the first example's equation with nothing to draw",
   "sources": [
    "BC-SKL-07033"
   ]
  },
  {
   "block": "orientation",
   "mode": "text",
   "reason": "rule 6: a statement of what a response shows; BC-REP-01, BC-REP-04, BC-REP-06 only",
   "sources": [
    "BC-SKL-07029"
   ]
  },
  {
   "block": "ki-1",
   "mode": "text",
   "reason": "rule 6: a rule about the constant and the branch; BC-REP-01, BC-REP-04, BC-REP-06 on BC-SKL-07029, BC-SKL-07030, BC-SKL-07033",
   "sources": [
    "BC-SKL-07029",
    "BC-SKL-07030",
    "BC-SKL-07033"
   ]
  },
  {
   "block": "ki-2",
   "mode": "text",
   "reason": "rule 6: a symbolic form; BC-REP-01, BC-REP-06 on BC-SKL-07032",
   "sources": [
    "BC-SKL-07032"
   ]
  },
  {
   "block": "ex-1",
   "mode": "step_reveal",
   "reason": "rule 1: a worked example or an error block",
   "sources": []
  },
  {
   "block": "ex-2",
   "mode": "step_reveal",
   "reason": "rule 1: a worked example or an error block",
   "sources": []
  },
  {
   "block": "err-BC-ERR-07009",
   "mode": "step_reveal",
   "reason": "rule 1: a worked example or an error block",
   "sources": []
  },
  {
   "block": "err-BC-ERR-07029",
   "mode": "step_reveal",
   "reason": "rule 1: a worked example or an error block",
   "sources": []
  },
  {
   "block": "err-BC-ERR-07033",
   "mode": "step_reveal",
   "reason": "rule 1: a worked example or an error block",
   "sources": []
  },
  {
   "block": "err-BC-ERR-99014",
   "mode": "step_reveal",
   "reason": "rule 1: a worked example or an error block",
   "sources": []
  }
 ],
 "refresher": [
  "ki-1",
  "err-BC-ERR-07009",
  "err-BC-ERR-07029",
  "err-BC-ERR-07033",
  "err-BC-ERR-99014",
  "ex-1"
 ],
 "research_lines": [
  {
   "file": "research/units/unit-07-differential-equations.md",
   "line": "A general solution describes infinitely many solutions and exactly one of them passes through a given point"
  }
 ],
 "inferred": [
  {
   "claim": "The integrand label gauss is read as e^(-t^2) and sine as sin(t^2); parameter_spec names the labels but not the functions.",
   "settles": "An integrand table in BC-QA-07011's parameter_spec."
  },
  {
   "claim": "The parameter rate multiplies the integrand in the accumulation form (dy/dx = rate * f(x)); the spec notes do not say.",
   "settles": "The generator's rendering of the accumulation form in BC-QA-07011."
  },
  {
   "claim": "Two strategy blocks, one per archetype, although BC-QA-07011 and BC-QA-07003 share the separation-of-variables family, because their first lines differ; BC-QA-07007 (verification) gets no block under the 900-word full cap and is taught in LSN-CON-07002.",
   "settles": "A template ruling on whether the strategy cap counts archetypes or families."
  },
  {
   "claim": "BC-PT-99030 is not tagged on ex-2: one step carries both antiderivatives, as the 2023 four-point shape scores them together (sg-23:12).",
   "settles": "A plan 15 ruling on whether one step may carry two point tags."
  },
  {
   "claim": "ex-1 comes from BC-QA-07011 (listed first, no point_types) and ex-2 from BC-QA-07003 so the constant and branch lines carry reader lines in the low band only, which keeps the brief band under 450 words.",
   "settles": "The modality and band A/B in the build plan."
  },
  {
   "claim": "The exam part is II-B: BC-QA-07011 is one FRQ part or one MCQ, and its topic's FRQ forms score the constant handling (sg-23:12, sg-24:11).",
   "settles": "A BC-PT mapping for BC-QA-07011."
  }
 ],
 "sources": [
  "BC-CON-07008",
  "BC-SKL-07029",
  "BC-SKL-07030",
  "BC-SKL-07032",
  "BC-SKL-07033",
  "BC-EK-FUN-7E1",
  "BC-EK-FUN-7E2",
  "ced:143",
  "BC-QA-07011",
  "BC-QA-07003",
  "BC-QA-07007",
  "BC-PT-99028",
  "BC-PT-99029",
  "BC-PT-99031",
  "BC-PT-99032",
  "BC-ERR-07009",
  "BC-ERR-07029",
  "BC-ERR-07033",
  "BC-ERR-99014",
  "BC-MIS-07005",
  "BC-PRQ-07004",
  "sg-23:11",
  "sg-23:12",
  "sg-24:11",
  "sg-26:13",
  "research/units/unit-07-differential-equations.md#7.7 Finding Particular Solutions Using Initial Conditions and Separation of Variables",
  "research/question-analysis/question-archetypes.md#BC-QA-07011 Particular solution with a domain restriction or an accumulation form",
  "research/question-analysis/question-archetypes.md#BC-QA-07003 Particular solution by separation of variables",
  "research/scoring/common-point-losses.md#Setup points",
  "research/exam/exam-structure.md#Section and part layout"
 ],
 "word_count": {
  "full": 893,
  "brief": 410
 },
 "read_minutes": {
  "full": 6.0,
  "brief": 2.8
 }
}
```
