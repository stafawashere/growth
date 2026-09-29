---
title: LSN-CON-07007 Separation of variables
research_date: 2026-09-29
status: designed
purpose: Authoring spec for the concept lesson on BC-CON-07007, separation of variables, built from authoring_bundle("BC-CON-07007") and the research files it cites, so an author fills plan 15's lesson record without making a teaching decision.
---

# LSN-CON-07007 Separation of variables

Concept BC-CON-07007 (skills BC-SKL-07024 to BC-SKL-07028), topic 7.6 of Unit 7, loaded by BC-QA-07003 and BC-QA-07012, both in family separation-of-variables. Its hard parent in Unit 7 is BC-CON-07004 (docs/lessons/unit-07/README.md, section 1).

## Prediction

Both bands, served first, before any rule. Form `mcq`, three options, on ex-1's equation \(dy/dx=2xy\) with \(y(1)=3\): which rewriting lets each side be integrated in its own variable. Key: \(dy/y=2x\,dx\). One distractor keeps \(y\) on the \(dx\) side (\(dy=2xy\,dx\)) and the other is not equivalent to the equation (\(y\,dy=2x\,dx\)). The question is ex-1's first step, not its answer. The resolution states the divide and multiply that gives one variable per side, and never grades the choice. Sources: BC-CON-07007 and the 7.6 topic section that ki-1 cites (BC-EK-FUN-7D1, ced:142). Delivery: text. [inferred] Settled by the prediction's first-try rate in the build plan.

## Orientation

Served text, from BC-CON-07007 `description_plain` and the topic's Assessment behaviour paragraph (research/units/unit-07-differential-equations.md#7.6 Finding General Solutions Using Separation of Variables): a response separates with a differential on each side, antidifferentiates both sides, carries one constant and solves for y. The scoring gate on the whole part is sg-23:12; it stays in `sources` and out of the served text.

## Key ideas

Two BC-EK statements, both core, both bands. No anchor quote: the paraphrase carries the idea in fewer words.

- ki-1 (core), BC-EK-FUN-7D1 (ced:142). Paraphrase of the Separation paragraph: the hypothesis is a right side that factors as an x part times a y part; the conclusion is the separated form. The sum case is BC-SKL-07028. Notation: separated form.
- ki-2 (core), BC-EK-FUN-7D2 (ced:142). Paraphrase of the Antidifferentiation paragraph: both sides antidifferentiated, one constant collected on one side. Notation: one constant of integration.

## Recognition

BC-QA-07003 (research/question-analysis/question-archetypes.md#BC-QA-07003 Particular solution by separation of variables): `typical_wording` "use separation of variables to find an expression for the particular solution to the differential equation with the given initial condition"; `common_givens` a separable differential equation, an initial condition, sometimes a stated bound; `asked_to_produce` the separated form, the antiderivatives, the evaluated constant, the explicit solution. Shape: the closing part of the no-calculator differential equation FRQ, 4 or 5 points (BC-FRQ-2023-Q3-D, BC-FRQ-2024-Q3-C, BC-FRQ-2026-Q3-D, BC-FRQ-2021-Q5-C, BC-FRQ-2013-Q5-C, BC-FRQ-2019-Q4-C).

BC-QA-07012 (research/question-analysis/question-archetypes.md#BC-QA-07012 Differential equation judged separable or not, and a separable one separated): `typical_wording` "decide whether the differential equation can be solved by separation of variables"; `common_givens` an expanded right side. Shape: one MCQ or short answer, and the first step of every separation part.

Not this concept: "show that the given function is a solution" supplies a candidate (verification, BC-CON-07002); "use Euler's method" asks for an approximation (BC-CON-07006); a right side in x alone is an accumulation (BC-CON-07008).

The contrast pair on st-1 sets a separation stem beside its near miss. Where the near miss comes from: the sibling concept BC-CON-07002, verification, so the near-miss stem gives the same equation and a candidate function to show is a solution, which supplies the answer instead of asking for it. The separating feature is that the stem asks to find \(y\).

## Method choice

- st-1, BC-QA-07003, both bands. Method, `expected_solution_path[0]`: separate the variables with a differential on each side. Rival, `wrong_approaches`: treating the equation as though the dependent variable were a constant. Separating feature: y varies, so it must move to the dy side first.
- st-2, BC-QA-07012, low band. Method, `expected_solution_path[0]`: look for a common factor that makes the right side a function of x times a function of y. Rival, `wrong_approaches`: dividing each term by y separately. Separating feature: a common factor, or a leftover term that blocks one.

Both archetypes carry `asked_to_produce` and `common_givens`, so neither block is tagged inferred. The reader prints its own labels, so no field starts with one, and no method begins with a label. st-1 carries the contrast pair: a separation stem beside a verification stem.

## Solution path

- ex-1, BC-QA-07003, both bands, no calculator. Draw from `parameter_spec`: form exponential, rate 2, power 1, start 1, initial 3, so dy/dx = 2xy with y(1) = 3. It meets every constraint (|2 * 1^2| <= 12) and matches no published BC-QA-07003 draw (content/items_gen_unit07, items_unit07_agent).
- Steps follow `expected_solution_path`: separated equation (new, BC-PT-99028); integrated equation with one C (new, the antiderivative points untagged); initial values substituted (evaluate, BC-PT-99031); C solved (solve); explicit y (new, BC-PT-99032). The sign of y is settled in the last line from y(1) = 3.
- A fluent solver writes all five lines; the choice of branch is held in the head [inferred].
- One example, so it is not faded and carries no `fade_from`.

## Scoring

BC-QA-07003 lists BC-PT-99028, 99029, 99031, 99032, 99033, 99030. ex-1 tags 99028 (separation), 99031 (constant) and 99032 (answer), and the what_a_reader_scores lines are reader_checks output for those three. The antiderivative points 99029 and 99030 are not tagged: either reader line pushes the brief band past 450 words (see Sources, inferred) and BC-PT-99033 fits the accumulation form, not this part (docs/lessons/unit-07/README.md, section 2).

Point losses: a separable equation separated with a constant on the wrong side, or antidifferentiated incorrectly, BC-ERR-99014 (research/scoring/common-point-losses.md#Setup points). Absolute value on the logarithm is optional (sg-23:12, sg-26:13; research/scoring/notation-requirements.md#Parentheses). With no constant, at most the first two points (sg-23:12); the 2024 shape scores the two antiderivatives separately (sg-24:11).

## Traps

Six errors meet the skills; every served block is distinct, so each carries `fix_prompt` true; the first four in the bundle's order are served, low band all four, mid band the first two. All on ex-1's draw except BC-ERR-07028, which needs a non-separable equation (dy/dx = 2xy + 3, the BC-QA-07012 not-separable shape).

- err-BC-ERR-07024: y held fixed and 2xy integrated in x. No possible reason line: neither linked description names this move.
- err-BC-ERR-07025: ln y beside an untouched 2x. No possible reason line, cut for the brief-band cap.
- err-BC-ERR-07026: no constant. Possible reason from BC-MIS-07016.
- err-BC-ERR-07028: a sum split as if it factored. Possible reason from BC-MIS-07014.

## Representations

None. The topic's Representations paragraph names BC-REP-01 and BC-REP-06 only, with symbolic conversions; nothing figure-shaped.

## Prerequisite bridge

- BC-PRQ-06003, BC-PRQ-07001, BC-PRQ-07002, each from its `description_plain` and `failure_signature`.

## Time

BC-QA-07003 is `no_calculator` and the closing part of a multipart FRQ, so Section II Part B, 15.0 minutes per question (research/exam/exam-structure.md#Section and part layout). At 4 or 5 of 9 points the part's share is 6.67 or 8.33 minutes (docs/lessons/unit-07/README.md, section 5). The minutes go on the separation and the constant line; the exponentiation is one line.

## Checks

- chk-1, completion of ex-1, both bands: C is given; the student writes y. Key 3e^(x^2 - 1).
- chk-2, isomorph, both bands. Draw: exponential, rate -2, power 2, start 0, initial 5. Key 5e^(-2x^3/3).
- chk-3, MCQ, low band. Draw: exponential, rate 4, power 1, start 1, initial 2. Key 2e^(2x^2 - 2). Distractors: 4x^2 - 2 (BC-ERR-07024), 2e^(4x - 4) (BC-ERR-07025), e^(2x^2) (BC-ERR-07026).

## Delivery

- pr-1: text. Rule 6, a prediction on ex-1's equation with nothing to draw.
- orientation, ki-1, ki-2: text. Rule 6: the representations are BC-REP-01 and BC-REP-06, none figure-bearing, and the content is a sequence of written lines (docs/lessons/unit-07/README.md, section 6).
- ex-1 and the four error blocks: step_reveal, rule 1.

Figure presence: no drawn block. No rule of 2 to 5 applies, because the topic's representations are a differential equation and symbolic forms converted by rewriting, and no key idea describes a process, so the record carries `no_figure_reason`.

## Band plan

- Low (full): prediction, orientation, bridges, ki-1, ki-2, st-1 with its contrast, st-2, ex-1 with its three reader lines, chk-1, the four error blocks, chk-2, chk-3. 618 words, 4.12 minutes (cap 900 and 6).
- Mid (brief): prediction, orientation, bridges, ki-1, ki-2, st-1 with its contrast, ex-1 with its reader lines, chk-1, err-BC-ERR-07024, err-BC-ERR-07025, chk-2. 449 words, 3.0 minutes (cap 450 and 3). The orientation, both key ideas, the bridges, the st-1 fields and contrast, the prediction and ex-1's cues and whys were shortened to fit; no scoring tag was dropped.
- Refresher: ki-1, ki-2, the four error blocks, ex-1.

## Sources

- BC-CON-07007; BC-SKL-07024 to BC-SKL-07028; BC-EK-FUN-7D1, BC-EK-FUN-7D2; ced:142
- BC-QA-07003, BC-QA-07012; BC-PT-99028, BC-PT-99029, BC-PT-99030, BC-PT-99031, BC-PT-99032
- BC-ERR-07024, BC-ERR-07025, BC-ERR-07026, BC-ERR-07028; BC-MIS-07014, BC-MIS-07016
- BC-PRQ-06003, BC-PRQ-07001, BC-PRQ-07002
- sg-23:12, sg-24:11, sg-26:13
- research/units/unit-07-differential-equations.md#7.6 Finding General Solutions Using Separation of Variables
- research/question-analysis/question-archetypes.md#BC-QA-07003 Particular solution by separation of variables
- research/question-analysis/question-archetypes.md#BC-QA-07012 Differential equation judged separable or not, and a separable one separated
- research/scoring/common-point-losses.md#Setup points
- research/scoring/notation-requirements.md#Parentheses
- research/exam/exam-structure.md#Section and part layout
- [inferred] BC-PT-99029 and BC-PT-99030 untagged under the brief cap. Settled by a plan 15 ruling on reader lines and the cap.
- [inferred] Two strategy blocks for one family. Settled by a template ruling on the cap.
- [inferred] Every line written. Settled by per-step timing data.
- [inferred] BC-ERR-99014 and BC-ERR-07027 outside the cap. Settled by a cap or severity ruling.

## Machine record

```json
{
 "id": "LSN-CON-07007",
 "kind": "concept",
 "target_id": "BC-CON-07007",
 "unit": "07",
 "skills": [
  "BC-SKL-07024",
  "BC-SKL-07025",
  "BC-SKL-07026",
  "BC-SKL-07027",
  "BC-SKL-07028"
 ],
 "prediction": {
  "id": "pr-1",
  "stem": {
   "text": "Predict. \\(dy/dx=2xy\\) with \\(y(1)=3\\). Which rewriting lets each side integrate in its own variable?",
   "command_verb": "predict"
  },
  "format": "mcq",
  "options": [
   {
    "id": "A",
    "label": "\\(dy/y=2x\\,dx\\)",
    "is_key": true
   },
   {
    "id": "B",
    "label": "\\(dy=2xy\\,dx\\)",
    "is_key": false
   },
   {
    "id": "C",
    "label": "\\(y\\,dy=2x\\,dx\\)",
    "is_key": false
   }
  ],
  "resolution": "Divide by \\(y\\), multiply by \\(dx\\): \\(dy/y=2x\\,dx\\). Each side integrates in its own variable.",
  "sources": [
   "BC-CON-07007",
   "BC-EK-FUN-7D1",
   "ced:142",
   "research/units/unit-07-differential-equations.md#7.6 Finding General Solutions Using Separation of Variables"
  ]
 },
 "no_figure_reason": "The topic's representations are a differential equation and symbolic forms, converted by rewriting. No key idea describes a process and no representation is figure-bearing.",
 "orientation": {
  "text": "Separate, integrate with one constant, solve for y.",
  "sources": [
   "BC-CON-07007",
   "research/units/unit-07-differential-equations.md#7.6 Finding General Solutions Using Separation of Variables",
   "sg-23:12"
  ]
 },
 "key_ideas": [
  {
   "id": "ki-1",
   "ek_id": "BC-EK-FUN-7D1",
   "depth": "core",
   "text": "If the right side is an x part times a y part, y goes with dy and x with dx. A sum with no common factor does not separate.",
   "notation": "separated form",
   "quote": null,
   "sources": [
    "BC-EK-FUN-7D1",
    "ced:142",
    "research/units/unit-07-differential-equations.md#7.6 Finding General Solutions Using Separation of Variables"
   ]
  },
  {
   "id": "ki-2",
   "ek_id": "BC-EK-FUN-7D2",
   "depth": "core",
   "text": "Integrate each side in its own variable with one constant. The initial condition fixes it.",
   "notation": "one constant of integration",
   "quote": null,
   "sources": [
    "BC-EK-FUN-7D2",
    "ced:142",
    "research/units/unit-07-differential-equations.md#7.6 Finding General Solutions Using Separation of Variables"
   ]
  }
 ],
 "strategy": [
  {
   "id": "st-1",
   "archetype_id": "BC-QA-07003",
   "cue": "Separation with an initial condition.",
   "method": "y with dy, x with dx.",
   "rival": "Integrating with y held constant.",
   "separating_feature": "y varies, so it moves first.",
   "sources": [
    "BC-QA-07003"
   ],
   "evidence_tag": "verified",
   "contrast": {
    "this": {
     "text": "\\(dy/dx=3x^2y\\), \\(y(0)=4\\). Find \\(y\\) by separation.",
     "archetype_id": "BC-QA-07003"
    },
    "not_this": {
     "text": "\\(dy/dx=3x^2y\\). Show that \\(y=4e^{x^3}\\) is a solution with \\(y(0)=4\\).",
     "why_not": "It supplies a candidate."
    },
    "feature": "The stem asks to find \\(y\\)."
   }
  },
  {
   "id": "st-2",
   "archetype_id": "BC-QA-07012",
   "cue": "The stem asks whether the equation separates, with the right side printed expanded.",
   "method": "The right side factored as an x part times a y part.",
   "rival": "Dividing each term by y separately.",
   "separating_feature": "A common factor exists, or a leftover constant term blocks it.",
   "sources": [
    "BC-QA-07012"
   ],
   "evidence_tag": "verified"
  }
 ],
 "worked_examples": [
  {
   "id": "ex-1",
   "archetype_id": "BC-QA-07003",
   "bands": [
    "low",
    "mid"
   ],
   "parameter_draw": {
    "form": "exponential",
    "rate": 2,
    "power": 1,
    "start": 1,
    "initial": 3
   },
   "problem": {
    "text": "dy/dx = 2xy, y(1) = 3. Find y by separation.",
    "command_verb": "find"
   },
   "calculator_status": "no_calculator",
   "steps": [
    {
     "cue": "2xy is 2x times y.",
     "why": "Divide by y, multiply by dx.",
     "expr": "dy/y = 2*x*dx",
     "relation": "new",
     "point_type_id": "BC-PT-99028"
    },
    {
     "cue": "One variable per side.",
     "why": "One C.",
     "expr": "log(Abs(y)) = x**2 + C",
     "relation": "new"
    },
    {
     "cue": "y(1) = 3.",
     "why": "Substitute before exponentiating.",
     "expr": "log(3) = 1 + C",
     "relation": "evaluate",
     "subs": {
      "x": "1",
      "y": "3"
     },
     "point_type_id": "BC-PT-99031"
    },
    {
     "cue": "C alone.",
     "why": "Solve.",
     "expr": "log(3) - 1",
     "relation": "solve",
     "variable": "C"
    },
    {
     "cue": "The stem asks for y.",
     "why": "y(1) > 0, so |y| = y.",
     "expr": "y = 3*exp(x**2 - 1)",
     "relation": "new",
     "point_type_id": "BC-PT-99032"
    }
   ],
   "answer": {
    "form": "symbolic",
    "expr": "3*exp(x**2 - 1)"
   }
  }
 ],
 "what_a_reader_scores": [
  {
   "example_id": "ex-1",
   "point_type_ids": [
    "BC-PT-99028",
    "BC-PT-99031",
    "BC-PT-99032"
   ],
   "lines": [
    {
     "point_type_id": "BC-PT-99028",
     "text": "Separation of variables. Earned by: Rearranging the differential equation so each variable sits with its own differential, in the form constant times the dependent differential over the dependent expression equals constant times the independent differential (sg-26:13). Not earned by: Any attempt that leaves both variables on the same side; sg-26:13, sg-23:12, sg-21:20 and sg-19:5 all state that without separation the entire part scores zero."
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
   "error_id": "BC-ERR-07024",
   "observed_behavior": "The response antidifferentiates the equation as written, with both variables on the same side.",
   "scoring_consequence": "All four points of the separation part are lost; the guideline states that a response with no separation earns none of them.",
   "wrong_step": {
    "text": "y held fixed.",
    "expr": "y = x**2*y + C"
   },
   "right_step": {
    "text": "Separated first.",
    "expr": "log(y) = x**2 + C"
   },
   "relation": "distinct",
   "possible_reason": null,
   "sources": [
    "BC-ERR-07024"
   ],
   "fix_prompt": true
  },
  {
   "error_id": "BC-ERR-07025",
   "observed_behavior": "The response integrates the dependent side and leaves the independent side untouched, or the reverse.",
   "scoring_consequence": "The antiderivative point is lost and every later point with it.",
   "wrong_step": {
    "text": "2x left untouched.",
    "expr": "log(y) = 2*x"
   },
   "right_step": {
    "text": "Both sides integrated.",
    "expr": "log(y) = x**2 + C"
   },
   "relation": "distinct",
   "possible_reason": null,
   "sources": [
    "BC-ERR-07025"
   ],
   "fix_prompt": true
  },
  {
   "error_id": "BC-ERR-07026",
   "observed_behavior": "The antiderivative equation is written with no constant.",
   "scoring_consequence": "At most the first two points are available; the guideline caps the response there.",
   "wrong_step": {
    "text": "No C, so y(1) = 3 cannot act.",
    "expr": "log(y) = x**2"
   },
   "right_step": {
    "text": "One C, fixed by y(1) = 3.",
    "expr": "log(y) = x**2 + C"
   },
   "relation": "distinct",
   "possible_reason": {
    "misconception_id": "BC-MIS-07016",
    "text": "the family collapses and the initial condition has nothing to act on"
   },
   "sources": [
    "BC-ERR-07026",
    "BC-MIS-07016"
   ],
   "fix_prompt": true
  },
  {
   "error_id": "BC-ERR-07028",
   "observed_behavior": "The response moves terms across as though the right side factored when it is a sum in both variables.",
   "scoring_consequence": "The separated form is not equivalent to the equation, so nothing that follows is valid.",
   "wrong_step": {
    "text": "dy/dx = 2xy + 3 split as if it factored.",
    "expr": "dy/y = (2*x + 3)*dx"
   },
   "right_step": {
    "text": "No common factor: not separable, left as given.",
    "expr": "dy/dx = 2*x*y + 3"
   },
   "relation": "distinct",
   "possible_reason": {
    "misconception_id": "BC-MIS-07014",
    "text": "applies the separation move to every equation, whether or not the right side factors"
   },
   "sources": [
    "BC-ERR-07028",
    "BC-MIS-07014"
   ],
   "fix_prompt": true
  }
 ],
 "representations": null,
 "prerequisite_bridges": [
  {
   "prq_id": "BC-PRQ-06003",
   "text": "1/y integrates to ln|y|."
  },
  {
   "prq_id": "BC-PRQ-07001",
   "text": "Exponentiating isolates y."
  },
  {
   "prq_id": "BC-PRQ-07002",
   "text": "dy/dx splits into dy and dx."
  }
 ],
 "time": {
  "exam_part": "II-B",
  "budget_minutes": 15.0,
  "source": "research/exam/exam-structure.md#Section and part layout",
  "written_steps": {
   "ex-1": [
    1,
    2,
    3,
    4,
    5
   ]
  },
  "skipped_steps": {
   "ex-1": []
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
   "archetype_id": "BC-QA-07003",
   "parameter_draw": {
    "form": "exponential",
    "rate": 2,
    "power": 1,
    "start": 1,
    "initial": 3
   },
   "completes": "ex-1",
   "stem": {
    "text": "ln|y| = x^2 + C, C = ln 3 - 1. Write y.",
    "command_verb": "write"
   },
   "key": {
    "form": "symbolic",
    "expr": "3*exp(x**2 - 1)"
   },
   "steps": [
    {
     "text": "C substituted.",
     "expr": "log(y) = x**2 + log(3) - 1",
     "relation": "new"
    },
    {
     "text": "Exponentiated.",
     "expr": "y = 3*exp(x**2 - 1)",
     "relation": "new"
    }
   ],
   "calculator_status": "no_calculator",
   "skills": [
    "BC-SKL-07027"
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
   "archetype_id": "BC-QA-07003",
   "parameter_draw": {
    "form": "exponential",
    "rate": -2,
    "power": 2,
    "start": 0,
    "initial": 5
   },
   "stem": {
    "text": "dy/dx = -2x^2 y, y(0) = 5. Find y.",
    "command_verb": "find"
   },
   "key": {
    "form": "symbolic",
    "expr": "5*exp(-2*x**3/3)"
   },
   "steps": [
    {
     "text": "Separate.",
     "expr": "dy/y = -2*x**2*dx",
     "relation": "new",
     "point_type_id": "BC-PT-99028"
    },
    {
     "text": "Integrate.",
     "expr": "log(Abs(y)) = -2*x**3/3 + C",
     "relation": "new"
    },
    {
     "text": "x = 0, y = 5.",
     "expr": "log(5) = C",
     "relation": "evaluate",
     "subs": {
      "x": "0",
      "y": "5"
     }
    },
    {
     "text": "C.",
     "expr": "log(5)",
     "relation": "solve",
     "variable": "C"
    },
    {
     "text": "Solve for y.",
     "expr": "y = 5*exp(-2*x**3/3)",
     "relation": "new"
    }
   ],
   "calculator_status": "no_calculator",
   "skills": [
    "BC-SKL-07024",
    "BC-SKL-07027"
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
    "form": "exponential",
    "rate": 4,
    "power": 1,
    "start": 1,
    "initial": 2
   },
   "stem": {
    "text": "dy/dx = 4xy with y(1) = 2. Which is the particular solution?",
    "command_verb": "identify"
   },
   "key": {
    "form": "symbolic",
    "expr": "2*exp(2*x**2 - 2)"
   },
   "steps": [
    {
     "text": "Separate.",
     "expr": "dy/y = 4*x*dx",
     "relation": "new"
    },
    {
     "text": "Integrate.",
     "expr": "log(Abs(y)) = 2*x**2 + C",
     "relation": "new"
    },
    {
     "text": "x = 1, y = 2.",
     "expr": "log(2) = 2 + C",
     "relation": "evaluate",
     "subs": {
      "x": "1",
      "y": "2"
     }
    },
    {
     "text": "C.",
     "expr": "log(2) - 2",
     "relation": "solve",
     "variable": "C"
    },
    {
     "text": "Solve for y.",
     "expr": "y = 2*exp(2*x**2 - 2)",
     "relation": "new"
    }
   ],
   "options": [
    {
     "id": "A",
     "is_key": false,
     "expr": "4*x**2 - 2",
     "error_path": "BC-ERR-07024",
     "derivation": "4xy integrated in x with y held at 2, then y(1) = 2 used"
    },
    {
     "id": "B",
     "is_key": true,
     "expr": "2*exp(2*x**2 - 2)",
     "error_path": null
    },
    {
     "id": "C",
     "is_key": false,
     "expr": "2*exp(4*x - 4)",
     "error_path": "BC-ERR-07025",
     "derivation": "the x side left as 4x, not antidifferentiated"
    },
    {
     "id": "D",
     "is_key": false,
     "expr": "exp(2*x**2)",
     "error_path": "BC-ERR-07026",
     "derivation": "no constant, so y(1) = 2 never enters"
    }
   ],
   "calculator_status": "no_calculator",
   "skills": [
    "BC-SKL-07024",
    "BC-SKL-07025",
    "BC-SKL-07026"
   ]
  }
 ],
 "delivery": [
  {
   "block": "pr-1",
   "mode": "text",
   "reason": "rule 6: a prediction on ex-1's equation with nothing to draw",
   "sources": [
    "BC-SKL-07024"
   ]
  },
  {
   "block": "orientation",
   "mode": "text",
   "reason": "rule 6: a statement of what a response shows; BC-REP-01 and BC-REP-06 only, no figure-bearing representation",
   "sources": [
    "BC-SKL-07024"
   ]
  },
  {
   "block": "ki-1",
   "mode": "text",
   "reason": "rule 6: a rule about the form of the right side; BC-REP-01, BC-REP-06 on BC-SKL-07024 and BC-SKL-07028",
   "sources": [
    "BC-SKL-07024",
    "BC-SKL-07028"
   ]
  },
  {
   "block": "ki-2",
   "mode": "text",
   "reason": "rule 6: a sequence of written lines that the worked example carries in step reveal; BC-REP-01 on BC-SKL-07025 to BC-SKL-07027",
   "sources": [
    "BC-SKL-07025",
    "BC-SKL-07026",
    "BC-SKL-07027"
   ]
  },
  {
   "block": "ex-1",
   "mode": "step_reveal",
   "reason": "rule 1: a worked example or an error block",
   "sources": []
  },
  {
   "block": "err-BC-ERR-07024",
   "mode": "step_reveal",
   "reason": "rule 1: a worked example or an error block",
   "sources": []
  },
  {
   "block": "err-BC-ERR-07025",
   "mode": "step_reveal",
   "reason": "rule 1: a worked example or an error block",
   "sources": []
  },
  {
   "block": "err-BC-ERR-07026",
   "mode": "step_reveal",
   "reason": "rule 1: a worked example or an error block",
   "sources": []
  },
  {
   "block": "err-BC-ERR-07028",
   "mode": "step_reveal",
   "reason": "rule 1: a worked example or an error block",
   "sources": []
  }
 ],
 "refresher": [
  "ki-1",
  "ki-2",
  "err-BC-ERR-07024",
  "err-BC-ERR-07025",
  "err-BC-ERR-07026",
  "err-BC-ERR-07028",
  "ex-1"
 ],
 "research_lines": [
  {
   "file": "research/units/unit-07-differential-equations.md",
   "line": "A response with no separation earns none of the four; a response with no constant of integration earns at most the first two"
  }
 ],
 "inferred": [
  {
   "claim": "The antiderivative points BC-PT-99029 and BC-PT-99030 are not tagged on ex-1: with the separation, constant and answer lines (BC-PT-99028, 99031, 99032) the brief band is 441 words, and either antiderivative line (66 or 36 words) pushes it past 450 after the prose was cut to its floor. The 2023 four-point shape scores the antiderivatives as one point (sg-23:12).",
   "settles": "A plan 15 ruling that reader lines sit outside the brief-band word cap, or a shorter reader_checks text for BC-PT-99029."
  },
  {
   "claim": "Two strategy blocks are kept for one archetype family (separation-of-variables), one per archetype, because BC-QA-07012's separability judgment has its own first line.",
   "settles": "A template ruling on whether the strategy cap counts archetypes or families."
  },
  {
   "claim": "The fluent solver writes every step of ex-1 because each carries a point or feeds one.",
   "settles": "Per-step timing data from the fluency telemetry."
  },
  {
   "claim": "BC-ERR-99014 and BC-ERR-07027 are left out of the traps under the four-block cap; BC-ERR-07027 (answer left implicit) is carried by ex-1's final step and the BC-PT-99032 reader line.",
   "settles": "A cap ruling or a severity order that ranks BC-ERR-07027 above BC-ERR-07028."
  }
 ],
 "sources": [
  "BC-CON-07007",
  "BC-SKL-07024",
  "BC-SKL-07025",
  "BC-SKL-07026",
  "BC-SKL-07027",
  "BC-SKL-07028",
  "BC-EK-FUN-7D1",
  "BC-EK-FUN-7D2",
  "ced:142",
  "BC-QA-07003",
  "BC-QA-07012",
  "BC-PT-99028",
  "BC-PT-99029",
  "BC-PT-99031",
  "BC-PT-99032",
  "BC-ERR-07024",
  "BC-ERR-07025",
  "BC-ERR-07026",
  "BC-ERR-07028",
  "BC-MIS-07014",
  "BC-MIS-07016",
  "BC-PRQ-06003",
  "BC-PRQ-07001",
  "BC-PRQ-07002",
  "sg-23:12",
  "sg-24:11",
  "sg-26:13",
  "research/units/unit-07-differential-equations.md#7.6 Finding General Solutions Using Separation of Variables",
  "research/question-analysis/question-archetypes.md#BC-QA-07003 Particular solution by separation of variables",
  "research/question-analysis/question-archetypes.md#BC-QA-07012 Differential equation judged separable or not, and a separable one separated",
  "research/scoring/common-point-losses.md#Setup points",
  "research/scoring/notation-requirements.md#Parentheses",
  "research/exam/exam-structure.md#Section and part layout"
 ],
 "word_count": {
  "full": 618,
  "brief": 449
 },
 "read_minutes": {
  "full": 4.12,
  "brief": 3.0
 }
}
```
