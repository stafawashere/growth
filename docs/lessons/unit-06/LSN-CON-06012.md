---
title: LSN-CON-06012 Fundamental Theorem of Calculus part two and net change
research_date: 2026-09-29
status: designed
purpose: Authoring spec for the concept lesson on BC-CON-06012, a definite integral as F(b) minus F(a) and a later value as a known value plus the integral of the rate, built from authoring_bundle("BC-CON-06012") and the research files it cites, so an author fills plan 15's lesson record without making a teaching decision.
---

# LSN-CON-06012 Fundamental Theorem of Calculus part two and net change

Concept BC-CON-06012 (skills BC-SKL-06034, 06035, 06036, 06037, 06039), topic 6.7 of Unit 6, loaded by 11 archetypes, more than any other Unit 6 concept (docs/lessons/unit-06/README.md, section 3). The bundle lists them primary first: BC-QA-06005, BC-QA-06006 and BC-QA-99008 carry a skill of this concept first; the strategy cap of 3 takes those three. Hard parents: BC-CON-06001, 06008, 06010, 06014.

## Prediction

Short answer on ex-1's numbers, tagged [inferred] (the record carries no pretest). Stem: predict the amount at t = 3 from 40 liters at t = 1 and the inflow rate 3t^2 + 2t + 2. Key 78, ex-1's answer. The resolution says the change is the integral, 38, and the amount is 40 plus 38, with no verdict word. Source: BC-CON-06012 and the topic section 6.7 the key idea cites.

## Orientation

Served text, from BC-CON-06012 `description_plain` and the topic's Assessment behaviour paragraph (research/units/unit-06-integration-accumulation.md#6.7 The Fundamental Theorem of Calculus and Definite Integrals): a later value is the known value plus the integral. No count, no frequency. Cut to hold the brief cap.

## Key ideas

BC-SKL-06034 maps to BC-EK-FUN-6B1 and 6B3, BC-SKL-06035 to 6B2 and 6B3, the other three to 6B3 (ced:124). Three blocks: ki-1 (BC-EK-FUN-6B3) core, ki-2 (6B1) and ki-3 (6B2) extended, low band.

- ki-1 (core, BC-EK-FUN-6B3). Paraphrase of "Fundamental Theorem of Calculus part two" and "Net change and average value": with f continuous on [a, b] and F an antiderivative, the integral from a to b is F(b) - F(a); the integral of a rate is the net change, so a later value is the earlier value plus the integral. No quote, to keep the brief band under its cap.
- ki-2 (extended, BC-EK-FUN-6B1). Paraphrase of "Antiderivative". Anchor quote from ced:124.
- ki-3 (extended, BC-EK-FUN-6B2). Paraphrase of "Fundamental Theorem of Calculus part one, restated": the accumulation function is an antiderivative of f.

## Recognition

- BC-QA-06005 (research/question-analysis/question-archetypes.md#BC-QA-06005 Net change from a rate with an initial condition): `typical_wording` "find the value of the quantity at the later time, showing the setup"; `common_givens` a rate function and a known value at one time; `asked_to_produce` an integral expression with the initial value, a value with units. Signal: a rate, a value at one time, and "at the later time". Shapes: FRQ parts (BC-FRQ-2019-Q1-A, BC-FRQ-2024-Q1-C, BC-FRQ-2025-Q3-D) and MCQ.
- BC-QA-06006 (research/question-analysis/question-archetypes.md#BC-QA-06006 Rate in minus rate out accumulation): two rates acting in opposite directions and an initial amount.
- BC-QA-99008 (research/question-analysis/question-archetypes.md#BC-QA-99008 Total amount from a rate over an interval with no initial condition and no rate out): "the total amount that arrives", with an initial amount in the stem that belongs to a later part.

What says "not this concept": a variable upper limit and a derivative request select part one (BC-CON-06008); "average value" or a factor 1/(b - a) selects BC-CON-06013 (docs/lessons/unit-06/README.md, section 3).

The near miss in the contrast pair comes from the sibling archetype BC-QA-99008 in this concept: a total that arrives, with no known value to add, asks for the integral alone, where st-1's stem gives a known value at one time and asks for the amount later.

## Method choice

Three strategy blocks; st-1 serves both bands.

- st-1, BC-QA-06005. Method, `expected_solution_path[0]`: the value at the later input as the value at the earlier input plus the integral of the rate. Rival from `wrong_approaches`: reporting the net change as the amount (BC-ERR-06015). Separating feature: a known value of the quantity at one time.
- st-2, BC-QA-06006. Method: identify which rate increases and which decreases the quantity. Rival: dropping the parentheses around the outflow rate. Separating feature: two rates acting in opposite directions.
- st-3, BC-QA-99008. Method: read the interval out of the wording of the part. Rival: treating the part as a net change question because the stem gives an initial condition. Separating feature: "arrives" or "total" with no request for the amount present.

Contrast pair on st-1 (new on 2026-09-29): this is a known-value stem on BC-QA-06005; not this is a total-arriving stem on BC-QA-99008; the feature is the known value. The strategy fields, orientation, ki-1 and the bridges are shortened to hold the brief cap, and no scoring tag or anchor quote was dropped.

## Solution path

- ex-1, BC-QA-06005, both bands, no calculator. Draw from `parameter_spec`, tool exact, direction forward: cubic 1, square 1, linear 2, start 1, span 2, known 40, context tank (base_rate 5, swing 2, stretch 3, horizon 3 unused by the exact tool). Rate 3t^2 + 2t + 2 on [1, 3]; change 38; exact_options [78, 38, 68, 82] distinct, known - change > 0. No published BC-QA-06005 item carries this draw.
- Steps follow `expected_solution_path`: A(3) as 40 plus the integral (new, tagged BC-PT-99033); the antiderivative (new, tagged BC-PT-99003); F(3) - F(1) added (new); the value (equivalent). A fluent solver writes all four; the calculator evaluation is held on the calculator form (docs/lessons/unit-06/README.md, section 5).

## Scoring

BC-QA-06005 lists BC-PT-99001, 99004, 99069, 99002, 99033, 99003. ex-1 tags BC-PT-99033 on the setup line and BC-PT-99003 on the antiderivative; their reader_checks lines are in the machine record. The answer point BC-PT-99004 is earned by the final line but its reader line is left untagged, since adding it takes the brief band over 450 words (listed in the inferred array). A response that presents only the integral value does not earn the initial condition point (sg-24:3, sg-24:4); with no initial condition the answer point requires the antiderivative point (sg-25:14). Simplification that was never required can lose a secured point (research/scoring/common-point-losses.md#Answer points).

## Traps

Four active errors meet the skills, in the bundle's order: BC-ERR-06015 and BC-ERR-99012 (linked BC-MIS at severity high), BC-ERR-06032 and BC-ERR-99022 (no linked BC-MIS). Mid band: the first two.

- err-BC-ERR-06015: 38 reported, against 78. Possible reason, words from BC-MIS-08006.
- err-BC-ERR-99012: only the upper limit substituted, 40 + 42 = 82, against 78. Possible reason, words from BC-MIS-99004.
- err-BC-ERR-06032: shown on the archetype's calculator form (tool calculator, base_rate 5, swing 2, stretch 3, horizon 3), since the exact draw has no trigonometric integrand [inferred]. No possible reason: the record links no BC-MIS.
- err-BC-ERR-99022: parentheses dropped around F(1), 84, against 78. No possible reason: the record links no BC-MIS.

## Representations

None as a separate block; ki-1's table carries the known value plus the accumulated change.

## Prerequisite bridge

- BC-PRQ-06002 and BC-PRQ-06005, each from its `description_plain` and `failure_signature`.

## Time

BC-QA-06005 is `either`; the lesson takes Section I Part A, 2.14 minutes (research/exam/exam-structure.md#Section and part layout), and says so in the inferred array. The FRQ form of the part is 3 points, a 5.0 minute share (docs/lessons/unit-06/README.md, section 5). The minutes go on the setup line and the antiderivative.

## Checks

- chk-1, completion of ex-1, both bands: the setup and the antiderivative are given. Key 78.
- chk-2, isomorph, both bands. Draw: cubic -1, square 3, linear 4, start 1, span 2, known 30. Key 36.
- chk-3, MCQ, low band. Draw: cubic 2, square 0, linear 1, start 2, span 1, known 50. Key 89. Distractors: 39 (BC-ERR-06015), 107 (BC-ERR-99012, upper limit only), 93 (BC-ERR-99022, parentheses dropped around F(2)).

## Delivery

- orientation: text. Rule 6.
- ki-1: table. Rule 5: BC-REP-03 on BC-SKL-06037, the known value plus the accumulated change (docs/lessons/unit-06/README.md, section 6).
- ki-2, ki-3: text. Rule 6: BC-REP-01 and BC-REP-04 only.
- ex-1 and the four error blocks: step_reveal. Rule 1.

## Band plan

- Low (full): prediction, orientation, both bridges, ki-1 to ki-3, st-1 with its contrast, st-2, st-3, ex-1 with its scoring lines, chk-1, the four error blocks, chk-2, chk-3. 709 words, 4.9 minutes (cap 900 and 6).
- Mid (brief): prediction, orientation, both bridges, ki-1, st-1 with its contrast, ex-1 with its scoring lines, chk-1, err-BC-ERR-06015, err-BC-ERR-99012, chk-2. 450 words, 3.0 minutes (cap 450 and 3).
- Refresher: ki-1, the four error blocks, ex-1.

## Sources

- BC-CON-06012; BC-SKL-06034, BC-SKL-06035, BC-SKL-06036, BC-SKL-06037, BC-SKL-06039; BC-EK-FUN-6B1, BC-EK-FUN-6B2, BC-EK-FUN-6B3; ced:124
- BC-QA-06005, BC-QA-06006, BC-QA-99008; BC-PT-99033, BC-PT-99003, BC-PT-99004; sg-24:3, sg-24:4, sg-25:14
- BC-ERR-06015, BC-ERR-99012, BC-ERR-06032, BC-ERR-99022; BC-MIS-08006, BC-MIS-99004
- BC-PRQ-06002, BC-PRQ-06005
- research/units/unit-06-integration-accumulation.md#6.7 The Fundamental Theorem of Calculus and Definite Integrals
- research/question-analysis/question-archetypes.md#BC-QA-06005 Net change from a rate with an initial condition
- research/question-analysis/question-archetypes.md#BC-QA-06006 Rate in minus rate out accumulation
- research/question-analysis/question-archetypes.md#BC-QA-99008 Total amount from a rate over an interval with no initial condition and no rate out
- research/scoring/common-point-losses.md#Answer points
- research/exam/exam-structure.md#Section and part layout
- [inferred] Section I Part A for an `either` archetype. Settled by a calculator status per draw.
- [inferred] The answer point left untagged. Settled by a shorter BC-PT-99004 reader line or a larger brief cap.
- [inferred] The degree-mode block on the calculator form. Settled by a trigonometric exact form in the parameter_spec.

## Machine record

```json
{
 "id": "LSN-CON-06012",
 "kind": "concept",
 "target_id": "BC-CON-06012",
 "unit": "06",
 "skills": ["BC-SKL-06034", "BC-SKL-06035", "BC-SKL-06036", "BC-SKL-06037", "BC-SKL-06039"],
 "prediction": {
  "id": "pr-1",
  "stem": {
   "text": "Predict the amount at t = 3: 40 liters at t = 1, inflow 3t^2 + 2t + 2 per hour.",
   "command_verb": "predict"
  },
  "format": "short_answer",
  "key": {
   "form": "numeric",
   "expr": "78"
  },
  "resolution": "The change is the integral, 38; the amount is 40 plus 38.",
  "sources": ["BC-CON-06012", "research/units/unit-06-integration-accumulation.md#6.7 The Fundamental Theorem of Calculus and Definite Integrals"]
 },
 "orientation": {
  "text": "A later value is the known value plus the integral.",
  "sources": ["BC-CON-06012", "research/units/unit-06-integration-accumulation.md#6.7 The Fundamental Theorem of Calculus and Definite Integrals"]
 },
 "key_ideas": [
  {
   "id": "ki-1",
   "ek_id": "BC-EK-FUN-6B3",
   "depth": "core",
   "text": "The integral from a to b is F(b) - F(a). So A(b) = A(a) + the integral of the rate.",
   "notation": "F(b) - F(a)",
   "quote": null,
   "sources": ["BC-EK-FUN-6B3", "ced:124", "research/units/unit-06-integration-accumulation.md#6.7 The Fundamental Theorem of Calculus and Definite Integrals"]
  },
  {
   "id": "ki-2",
   "ek_id": "BC-EK-FUN-6B1",
   "depth": "extended",
   "text": "An antiderivative of f is any function whose derivative is f.",
   "notation": "F' = f",
   "quote": {
    "text": "An antiderivative of a function f is a function g whose derivative is f.",
    "source": "ced:124"
   },
   "sources": ["BC-EK-FUN-6B1", "ced:124"]
  },
  {
   "id": "ki-3",
   "ek_id": "BC-EK-FUN-6B2",
   "depth": "extended",
   "text": "With f continuous on an interval containing a, the integral of f from a to x is an antiderivative of f there.",
   "notation": "F(x) = integral from a to x of f(t) dt",
   "quote": null,
   "sources": ["BC-EK-FUN-6B2", "ced:124"]
  }
 ],
 "strategy": [
  {
   "id": "st-1",
   "archetype_id": "BC-QA-06005",
   "cue": "Rate and known value.",
   "method": "Known value plus the integral.",
   "rival": "Net change alone.",
   "separating_feature": "A known value.",
   "sources": ["BC-QA-06005", "BC-ERR-06015"],
   "evidence_tag": "verified",
   "contrast": {
    "this": {
     "text": "Rate 4t + 1; 10 liters at t = 2. Find the amount at t = 5.",
     "archetype_id": "BC-QA-06005"
    },
    "not_this": {
     "text": "Find the total liters entering from t = 2 to t = 5.",
     "why_not": "Only the integral."
    },
    "feature": "A known value."
   }
  },
  {
   "id": "st-2",
   "archetype_id": "BC-QA-06006",
   "cue": "An inflow rate, an outflow rate and an initial amount.",
   "method": "Which rate increases the quantity and which decreases it, then one integral of inflow minus outflow.",
   "rival": "The parentheses around the outflow dropped.",
   "separating_feature": "Two rates acting in opposite directions.",
   "sources": ["BC-QA-06006"],
   "evidence_tag": "verified"
  },
  {
   "id": "st-3",
   "archetype_id": "BC-QA-99008",
   "cue": "A rate over a closed interval; the total that arrives asked.",
   "method": "The interval read from the wording, then the integral of the rate.",
   "rival": "The stem's initial amount added, as for net change.",
   "separating_feature": "Arrives or total, with no amount present asked.",
   "sources": ["BC-QA-99008"],
   "evidence_tag": "verified"
  }
 ],
 "worked_examples": [
  {
   "id": "ex-1",
   "archetype_id": "BC-QA-06005",
   "bands": ["low", "mid"],
   "parameter_draw": {
    "cubic": 1,
    "square": 1,
    "linear": 2,
    "start": 1,
    "span": 2,
    "known": 40,
    "base_rate": 5,
    "swing": 2,
    "stretch": 3,
    "horizon": 3,
    "context": "tank",
    "tool": "exact",
    "direction": "forward"
   },
   "problem": {
    "text": "Water enters a tank at 3t^2 + 2t + 2 liters per hour. At t = 1 the tank holds 40 liters. Find the amount at t = 3.",
    "command_verb": "find"
   },
   "calculator_status": "no_calculator",
   "steps": [
    {
     "cue": "Known amount at t = 1.",
     "why": "Known value plus the change.",
     "expr": "40 + Integral(3*t**2 + 2*t + 2, (t, 1, 3))",
     "relation": "new",
     "point_type_id": "BC-PT-99033"
    },
    {
     "cue": "Antiderivative first.",
     "why": "Power rule, term by term.",
     "expr": "t**3 + t**2 + 2*t",
     "relation": "new",
     "point_type_id": "BC-PT-99003"
    },
    {
     "cue": "Both limits.",
     "why": "F(3) - F(1).",
     "expr": "40 + (27 + 9 + 6) - (1 + 1 + 2)",
     "relation": "new"
    },
    {
     "cue": "An amount.",
     "why": "78 liters.",
     "expr": "78",
     "relation": "equivalent"
    }
   ],
   "answer": {
    "form": "numeric",
    "expr": "78"
   }
  }
 ],
 "what_a_reader_scores": [
  {
   "example_id": "ex-1",
   "point_type_ids": ["BC-PT-99033", "BC-PT-99003"],
   "lines": [
    {
     "point_type_id": "BC-PT-99033",
     "text": "Uses the initial condition in an accumulation expression. Earned by: Adding the known function value at one endpoint to a definite integral of the rate (sg-24:3, sg-22:8). Not earned by: A definite integral alone with the known value never added (sg-22:8). Notation: sg-22:8 lists cases where a missing differential shifts which of the three points are available."
    },
    {
     "point_type_id": "BC-PT-99003",
     "text": "Antiderivative. Earned by: A correct antiderivative of the presented integrand, with or without the constant of integration (sg-25:14). Not earned by: An antiderivative of the wrong form, or a jump from integral to value with no antiderivative shown (sg-26:18)."
    }
   ]
  }
 ],
 "common_errors": [
  {
   "error_id": "BC-ERR-06015",
   "observed_behavior": "The definite integral of the rate is reported as the value of the quantity at the later input.",
   "scoring_consequence": "The initial condition point is not earned; the response that presents only the integral value does not earn it (sg-24:4).",
   "wrong_step": {
    "text": "38.",
    "expr": "38"
   },
   "right_step": {
    "text": "40 + 38.",
    "expr": "78"
   },
   "relation": "distinct",
   "possible_reason": {
    "misconception_id": "BC-MIS-08006",
    "text": "reads an accumulation integral as the quantity itself rather than as the change in it"
   },
   "sources": ["BC-ERR-06015", "BC-MIS-08006"],
   "fix_prompt": true
  },
  {
   "error_id": "BC-ERR-99012",
   "observed_behavior": "Responses write the integral of f prime from a to x as f of x, ignoring the value at the lower limit, or mishandle a reversed pair of limits and report the wrong sign for an accumulated area.",
   "scoring_consequence": "The value or setup point in that part is not earned, and the error usually propagates to later parts that build on the value.",
   "wrong_step": {
    "text": "40 + F(3).",
    "expr": "40 + 42"
   },
   "right_step": {
    "text": "40 + F(3) - F(1).",
    "expr": "40 + 42 - 4"
   },
   "relation": "distinct",
   "possible_reason": {
    "misconception_id": "BC-MIS-99004",
    "text": "the value at the lower limit and the direction of the limits play no role"
   },
   "sources": ["BC-ERR-99012", "BC-MIS-99004"],
   "fix_prompt": true
  },
  {
   "error_id": "BC-ERR-06032",
   "observed_behavior": "Numerical values of an integral or of a rate involving a trigonometric function are computed in degree mode.",
   "scoring_consequence": "The first point that the value would otherwise earn is not earned, and the response remains eligible for subsequent points (sg-23:4).",
   "wrong_step": {
    "text": "Degree mode.",
    "expr": "40 + Integral(5 + 2*sin(pi*t**2/540), (t, 0, 3))"
   },
   "right_step": {
    "text": "Radian mode.",
    "expr": "40 + Integral(5 + 2*sin(t**2/3), (t, 0, 3))"
   },
   "relation": "distinct",
   "possible_reason": null,
   "sources": ["BC-ERR-06032"],
   "fix_prompt": true
  },
  {
   "error_id": "BC-ERR-99022",
   "observed_behavior": "Responses simplify a numerical or algebraic expression that the exam does not require to be simplified, and introduce sign, order of operations or fraction errors that spoil an otherwise correct result.",
   "scoring_consequence": "A point already secured by the correct setup can be lost when the simplified final form is wrong.",
   "wrong_step": {
    "text": "Parentheses dropped.",
    "expr": "40 + 42 - 1 + 1 + 2"
   },
   "right_step": {
    "text": "F(1) subtracted whole.",
    "expr": "40 + 42 - (1 + 1 + 2)"
   },
   "relation": "distinct",
   "possible_reason": null,
   "sources": ["BC-ERR-99022"],
   "fix_prompt": true
  }
 ],
 "representations": null,
 "prerequisite_bridges": [
  {
   "prq_id": "BC-PRQ-06002",
   "text": "Radicals are powers."
  },
  {
   "prq_id": "BC-PRQ-06005",
   "text": "An amount is not a rate."
  }
 ],
 "time": {
  "exam_part": "I-A",
  "budget_minutes": 2.14,
  "source": "research/exam/exam-structure.md#Section and part layout",
  "written_steps": {
   "ex-1": [1, 2, 3, 4]
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
   "bands": ["low", "mid"],
   "archetype_id": "BC-QA-06005",
   "parameter_draw": {
    "cubic": 1,
    "square": 1,
    "linear": 2,
    "start": 1,
    "span": 2,
    "known": 40,
    "base_rate": 5,
    "swing": 2,
    "stretch": 3,
    "horizon": 3,
    "context": "tank",
    "tool": "exact",
    "direction": "forward"
   },
   "completes": "ex-1",
   "stem": {
    "text": "Given F(t) = t^3 + t^2 + 2t, find A(3).",
    "command_verb": "find"
   },
   "key": {
    "form": "numeric",
    "expr": "78"
   },
   "steps": [
    {
     "text": "Both limits.",
     "expr": "40 + (27 + 9 + 6) - (1 + 1 + 2)",
     "relation": "new"
    },
    {
     "text": "Value.",
     "expr": "78",
     "relation": "equivalent"
    }
   ],
   "calculator_status": "no_calculator",
   "skills": ["BC-SKL-06037"]
  },
  {
   "id": "chk-2",
   "check_kind": "isomorph",
   "format": "short_answer",
   "bands": ["low", "mid"],
   "archetype_id": "BC-QA-06005",
   "parameter_draw": {
    "cubic": -1,
    "square": 3,
    "linear": 4,
    "start": 1,
    "span": 2,
    "known": 30,
    "base_rate": 5,
    "swing": 2,
    "stretch": 3,
    "horizon": 3,
    "context": "pile",
    "tool": "exact",
    "direction": "forward"
   },
   "stem": {
    "text": "Rate -3t^2 + 6t + 4 tons per hour; 30 tons at t = 1. Amount at t = 3?",
    "command_verb": "find"
   },
   "key": {
    "form": "numeric",
    "expr": "36"
   },
   "steps": [
    {
     "text": "Setup.",
     "expr": "30 + Integral(-3*t**2 + 6*t + 4, (t, 1, 3))",
     "relation": "new"
    },
    {
     "text": "F(3) - F(1).",
     "expr": "30 + 12 - 6",
     "relation": "equivalent"
    },
    {
     "text": "Value.",
     "expr": "36",
     "relation": "equivalent"
    }
   ],
   "calculator_status": "no_calculator",
   "skills": ["BC-SKL-06037"]
  },
  {
   "id": "chk-3",
   "check_kind": "mcq",
   "format": "mcq",
   "bands": ["low"],
   "archetype_id": "BC-QA-06005",
   "parameter_draw": {
    "cubic": 2,
    "square": 0,
    "linear": 1,
    "start": 2,
    "span": 1,
    "known": 50,
    "base_rate": 5,
    "swing": 2,
    "stretch": 3,
    "horizon": 3,
    "context": "balloon",
    "tool": "exact",
    "direction": "forward"
   },
   "stem": {
    "text": "Air enters a balloon at 6t^2 + 1 liters per second; 50 liters at t = 2. The amount at t = 3 is",
    "command_verb": "identify"
   },
   "key": {
    "form": "numeric",
    "expr": "89"
   },
   "steps": [
    {
     "text": "Setup.",
     "expr": "50 + Integral(6*t**2 + 1, (t, 2, 3))",
     "relation": "new"
    },
    {
     "text": "F(t) = 2t^3 + t.",
     "expr": "50 + 57 - 18",
     "relation": "equivalent"
    },
    {
     "text": "Value.",
     "expr": "89",
     "relation": "equivalent"
    }
   ],
   "options": [
    {
     "id": "A",
     "is_key": false,
     "expr": "39",
     "error_path": "BC-ERR-06015",
     "derivation": "the integral alone, 57 - 18"
    },
    {
     "id": "B",
     "is_key": true,
     "expr": "89",
     "error_path": null
    },
    {
     "id": "C",
     "is_key": false,
     "expr": "93",
     "error_path": "BC-ERR-99022",
     "derivation": "50 + 57 - 16 + 2, parentheses dropped around F(2)"
    },
    {
     "id": "D",
     "is_key": false,
     "expr": "107",
     "error_path": "BC-ERR-99012",
     "derivation": "50 + F(3), the lower limit ignored"
    }
   ],
   "calculator_status": "no_calculator",
   "skills": ["BC-SKL-06037"]
  }
 ],
 "delivery": [
  {
   "block": "orientation",
   "mode": "text",
   "reason": "rule 6: a statement of what a response writes",
   "sources": ["BC-SKL-06036"]
  },
  {
   "block": "ki-1",
   "mode": "table",
   "reason": "rule 5: BC-REP-03 on BC-SKL-06037, the known value plus the accumulated change",
   "sources": ["BC-SKL-06037"],
   "spec": {
    "kind": "table",
    "representations": ["BC-REP-03"],
    "columns": ["t", "1", "3"],
    "rows": [
     ["A(t), liters", "40", "40 + 38 = 78"],
     ["change since t = 1", "0", "38"]
    ],
    "labels": [
     {
      "text": "change = integral of the rate from 1 to 3",
      "placement": "inside"
     }
    ]
   },
   "fallback": "the table as plain text rows",
   "keyboard": "Tab moves between cells; no control"
  },
  {
   "block": "ki-2",
   "mode": "text",
   "reason": "rule 6: a definition, BC-REP-01 only",
   "sources": ["BC-SKL-06034"]
  },
  {
   "block": "ki-3",
   "mode": "text",
   "reason": "rule 6: a theorem statement, BC-REP-04",
   "sources": ["BC-SKL-06035"]
  },
  {
   "block": "ex-1",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  },
  {
   "block": "err-BC-ERR-06015",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  },
  {
   "block": "err-BC-ERR-99012",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  },
  {
   "block": "err-BC-ERR-06032",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  },
  {
   "block": "err-BC-ERR-99022",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  }
 ],
 "refresher": ["ki-1", "err-BC-ERR-06015", "err-BC-ERR-99012", "err-BC-ERR-06032", "err-BC-ERR-99022", "ex-1"],
 "read_minutes": {
  "full": 4.9,
  "brief": 3.0
 },
 "word_count": {
  "full": 709,
  "brief": 450
 },
 "research_lines": [
  {
   "file": "research/scoring/common-point-losses.md",
   "line": "Simplification that was never required introduces an arithmetic or algebra error"
  }
 ],
 "inferred": [
  {
   "claim": "BC-QA-06005 is calculator status either; the lesson takes Section I Part A at 2.14 minutes.",
   "settles": "A calculator status per draw on the archetype, or a rule for either archetypes in plan 15."
  },
  {
   "claim": "The answer point BC-PT-99004 is earned by ex-1's last line but not tagged, because its 88 word reader line takes the brief band over 450 words.",
   "settles": "A shorter BC-PT-99004 reader line, or a brief cap that admits three reader lines."
  },
  {
   "claim": "The BC-ERR-06032 block uses the archetype's calculator form, since the exact draw has no trigonometric integrand.",
   "settles": "A trigonometric exact form in BC-QA-06005's parameter_spec."
  }
 ],
 "sources": ["BC-CON-06012", "BC-SKL-06034", "BC-SKL-06035", "BC-SKL-06036", "BC-SKL-06037", "BC-SKL-06039", "BC-EK-FUN-6B1", "BC-EK-FUN-6B2", "BC-EK-FUN-6B3", "ced:124", "BC-QA-06005", "BC-QA-06006", "BC-QA-99008", "BC-PT-99033", "BC-PT-99003", "BC-PT-99004", "sg-24:3", "sg-24:4", "sg-25:14", "BC-ERR-06015", "BC-ERR-99012", "BC-ERR-06032", "BC-ERR-99022", "BC-MIS-08006", "BC-MIS-99004", "BC-PRQ-06002", "BC-PRQ-06005", "research/units/unit-06-integration-accumulation.md#6.7 The Fundamental Theorem of Calculus and Definite Integrals", "research/question-analysis/question-archetypes.md#BC-QA-06005 Net change from a rate with an initial condition", "research/exam/exam-structure.md#Section and part layout"]
}
```
