---
title: LSN-CON-04001 The derivative as a rate in context
research_date: 2026-09-29
status: designed
purpose: Authoring spec for the concept lesson on BC-CON-04001, interpreting a derivative value as an instantaneous rate in context, built from authoring_bundle("BC-CON-04001") and the research files it cites, so an author fills plan 15's lesson record without making a teaching decision.
---

# LSN-CON-04001 The derivative as a rate in context

Concept BC-CON-04001 (skills BC-SKL-04002, BC-SKL-04003, BC-SKL-04005), topic 4.1 of Unit 4, loaded by one archetype, BC-QA-04001 (family derivative-in-context). Its hard parent is BC-CON-04002, the units (docs/lessons/unit-04/README.md, section 1).

## Prediction

Both bands, served first, before any rule. Form `mcq`, three options, on ex-1's own numbers: \(W'(9)=-3.5\) for water in a tank, in liters, at \(t\) minutes. The student picks among an amount, a decrease at a rate and an increase at a rate. Key: the water decreases 3.5 liters per minute. The resolution states what the derivative gives (a rate at the instant, in liters per minute, negative so decreasing) and never grades the choice. Sources: BC-CON-04001 and the 4.1 topic section that ki-1 cites (BC-EK-CHA-3A1, ced:87). Delivery: text. [inferred] Settled by the prediction's first-try rate in the build plan.

## Orientation

Served text, from BC-CON-04001 `description_plain` and the Assessment behaviour paragraph (research/units/unit-04-contextual-applications-differentiation.md#4.1 Interpreting the Meaning of the Derivative in Context), stated as what the sentence must hold and cut to fit the brief cap. No count, no frequency.

## Key ideas

BC-SKL-04002 maps BC-EK-CHA-3A1 and BC-EK-CHA-3A2, BC-SKL-04003 maps BC-EK-CHA-3A1, BC-SKL-04005 maps BC-EK-CHA-3A2: two blocks, one core, one extended, to hold the brief band under its cap.

- ki-1 (core, BC-EK-CHA-3A1, ced:87). The Derivative as an instantaneous rate paragraph of Required mathematical knowledge, with the rate against amount contrast of BC-SKL-04003. No anchor quote, to hold the brief band under its cap.
- ki-2 (extended, BC-EK-CHA-3A2, ced:87). The Interpretation paragraph: quantity, instant, direction, units (sg-24:2, sg-25:11). Anchor quote from ced:87.

## Recognition

BC-QA-04001 (research/question-analysis/question-archetypes.md#BC-QA-04001 Interpreting the value of a derivative in context with units): `typical_wording` "using correct units, interpret the meaning of the stated value in the context of the problem"; `common_givens` a contextual model, the units of the quantity and of the input, a numerical value of the derivative; `asked_to_produce` the value, its interpretation, the units of the rate. The signal: the word interpret beside a primed symbol and a number. Shapes: one part of a multipart contextual FRQ, often sharing the part with a computation (BC-FRQ-2013-Q1-A, BC-FRQ-2014-Q1-B, BC-FRQ-2023-Q1-D, BC-FRQ-2018-Q2-A), and an MCQ choosing among sentences (BC-MCQ-SAMPLE-013).

Not this concept: a stem asking for the units alone (BC-CON-04002), for an estimate from a table (BC-QA-04002), or for the amount at an instant, which is a function value.
The contrast pair on st-1 sets an interpretation stem beside its near miss. Where the near miss comes from: the `wrong_approaches` entry that reads the value as an amount (BC-ERR-04003), so the near-miss stem gives an unprimed function value, which asks for an amount and not a rate. The separating feature is the prime.

## Method choice

One strategy block: BC-QA-04001 is the only archetype loading these skills.

- st-1, BC-QA-04001. Method, `expected_solution_path[0]`: name the quantity and the instant. Rival from `wrong_approaches`: the value read as an amount (BC-ERR-04003), carried in `sources` and not in the served text. Separating feature: the prime on the given symbol. The reader prints its own labels, so no field starts with one. The archetype carries `asked_to_produce` and `common_givens`, so the block is verified. The block carries the contrast pair: a primed coffee temperature to interpret, beside an unprimed one.

## Solution path

- ex-1, BC-QA-04001, both bands. Draw from `parameter_spec`: context tank, instant 9, magnitude 7/2, sign negative, order first, so the stated value is -7/2. No published BC-QA-04001 item carries this draw.
- Steps follow `expected_solution_path`: name the rate and the instant (new, -7/2), the direction from the sign, the units as liters per minute, the sentence about the rate (tagged BC-PT-99008). The answer is a statement. A fluent solver writes only the sentence; the three reads before it are held in the head.
One example, so it is not faded and carries no `fade_from`.

## Scoring

BC-QA-04001 lists BC-PT-99004 and BC-PT-99008. ex-1 tags BC-PT-99008 on the sentence; the line is reader_checks(["BC-PT-99008"]) copied exactly. There is no computed value, so BC-PT-99004 is not tagged.

Point losses for the author: a rate of a rate described as a rate, a true statement that does not answer the question (BC-ERR-99027, cr-23:4; research/scoring/common-point-losses.md#Interpretation points), and malformed units (research/scoring/common-point-losses.md#Units points). sg-23:4 withholds the point for decreasing at a rate of a negative number.

## Traps

Four active errors meet the skills, in the bundle's order: BC-ERR-04001, BC-ERR-04003, BC-ERR-04005, BC-ERR-99027. Low band all four; mid band the first two. All on ex-1's draw.

- err-BC-ERR-04001: minutes per liter against liters per minute. Possible reason from BC-MIS-04003. Distinct, so `fix_prompt` true.
- err-BC-ERR-04003: 3.5 liters held against a rate of -3.5 liters per minute. Possible reason from BC-MIS-04001. Distinct, `fix_prompt` true.
- err-BC-ERR-04005: increasing against decreasing. Possible reason from BC-MIS-04002. Distinct, `fix_prompt` true.
- err-BC-ERR-99027: the same value with no instant and no direction; the values are equal, so the relation is equivalent, `fix_prompt` false, and the loss is the missing phrases.

The text writes 3.5, so every expression is the decimal 3.5 or -3.5, not 7/2.

## Representations

None. The topic's Representations paragraph names BC-REP-05 to BC-REP-04, a model to a sentence; nothing is figure-shaped.

## Prerequisite bridge

- BC-PRQ-04004 and BC-PRQ-04008, each from its `description_plain` and `failure_signature`.

## Time

BC-QA-04001 has calculator status either, so the lesson takes Section I Part A, 2.14 minutes per question (research/exam/exam-structure.md#Section and part layout) [inferred: the either status]. As an FRQ part it shares 15.0 minutes, 3.33 for a two point part (docs/lessons/unit-04/README.md, section 5). The minutes go on the one written sentence; the sign read and the unit quotient are held in the head.

## Checks

- chk-1, completion of ex-1, both bands: the sentence finished from the value. Key: decreasing at 3.5 liters per minute.
- chk-2, isomorph, both bands. Draw: snow, instant 10, magnitude 5/2, positive, first. Key: increasing at 2.5 centimeters per hour at t = 10 hours.
- chk-3, MCQ, low band. Draw: balloon, instant 3, magnitude 4, negative, first. Key A; B carries BC-ERR-04003 (an amount), C BC-ERR-04005 (increasing), D BC-ERR-04001 (inverted units). The key is a statement, so options carry labels.

## Delivery

- pr-1: text. Rule 6, a prediction on the worked example's numbers with nothing to draw.
- orientation, ki-1, ki-2: text. Rule 5: the three skills carry BC-REP-04 and BC-REP-05 only (docs/lessons/unit-04/README.md, section 6).
- ex-1 and the four error blocks: step_reveal. Rule 1.

Figure presence: no drawn block. No rule of 2 to 5 applies, because BC-REP-04 and BC-REP-05 are a model read into a sentence and no key idea describes a process, so the record carries `no_figure_reason`.

## Band plan

- Low (full): prediction, orientation, both bridges, ki-1, ki-2, st-1 with its contrast, ex-1 with its scoring line, chk-1, four error blocks, chk-2, chk-3. 702 words, 4.7 minutes (cap 900 and 6).
- Mid (brief): prediction, orientation, both bridges, ki-1, st-1 with its contrast, ex-1 with its scoring line, chk-1, err-BC-ERR-04001, err-BC-ERR-04003, chk-2. 449 words, 3.0 minutes (cap 450 and 3). The orientation, ki-1, the strategy cue, the prediction and the bridges were shortened to fit.
- Refresher: ki-1, the four error blocks, ex-1.

## Sources

- BC-CON-04001; BC-SKL-04002, BC-SKL-04003, BC-SKL-04005; BC-EK-CHA-3A1, BC-EK-CHA-3A2; ced:87
- BC-QA-04001; BC-PT-99008; sg-24:2, sg-25:11, sg-23:4, sg-21:3, cr-23:4
- BC-ERR-04001, BC-ERR-04003, BC-ERR-04005, BC-ERR-99027; BC-MIS-04001, BC-MIS-04002, BC-MIS-04003
- BC-PRQ-04004, BC-PRQ-04008
- research/units/unit-04-contextual-applications-differentiation.md#4.1 Interpreting the Meaning of the Derivative in Context
- research/question-analysis/question-archetypes.md#BC-QA-04001 Interpreting the value of a derivative in context with units
- research/scoring/common-point-losses.md#Interpretation points
- research/scoring/common-point-losses.md#Units points
- research/exam/exam-structure.md#Section and part layout
- [inferred] The exam part for an either archetype. Settled by a calculator status on BC-QA-04001.

## Machine record

```json
{
 "id": "LSN-CON-04001",
 "kind": "concept",
 "target_id": "BC-CON-04001",
 "unit": "04",
 "skills": [
  "BC-SKL-04002",
  "BC-SKL-04003",
  "BC-SKL-04005"
 ],
 "prediction": {
  "id": "pr-1",
  "stem": {
   "text": "Predict what \\(W'(9)=-3.5\\) says, for \\(W(t)\\) liters of water at \\(t\\) minutes.",
   "command_verb": "predict"
  },
  "format": "mcq",
  "options": [
   {
    "id": "A",
    "label": "The tank holds 3.5 liters.",
    "is_key": false
   },
   {
    "id": "B",
    "label": "The water decreases 3.5 liters per minute.",
    "is_key": true
   },
   {
    "id": "C",
    "label": "The water increases 3.5 liters per minute.",
    "is_key": false
   }
  ],
  "resolution": "\\(W'(9)\\) is a rate at \\(t=9\\), in liters per minute. It is negative, so the water is decreasing.",
  "sources": [
   "BC-CON-04001",
   "BC-EK-CHA-3A1",
   "ced:87",
   "research/units/unit-04-contextual-applications-differentiation.md#4.1 Interpreting the Meaning of the Derivative in Context"
  ]
 },
 "no_figure_reason": "The three skills carry only BC-REP-04 and BC-REP-05, a model read into a sentence, and the key ideas describe no process. No figure-bearing representation applies.",
 "orientation": {
  "text": "A derivative value is a rate at one instant. A response names quantity, instant, direction, size and units.",
  "sources": [
   "BC-CON-04001",
   "research/units/unit-04-contextual-applications-differentiation.md#4.1 Interpreting the Meaning of the Derivative in Context"
  ]
 },
 "key_ideas": [
  {
   "id": "ki-1",
   "ek_id": "BC-EK-CHA-3A1",
   "depth": "core",
   "text": "The derivative is the instantaneous rate of change: how fast, not how much. \\(W'(9)\\) is a rate at \\(t=9\\).",
   "notation": "f prime of a, a rate",
   "quote": null,
   "sources": [
    "BC-EK-CHA-3A1",
    "ced:87",
    "research/units/unit-04-contextual-applications-differentiation.md#4.1 Interpreting the Meaning of the Derivative in Context"
   ]
  },
  {
   "id": "ki-2",
   "ek_id": "BC-EK-CHA-3A2",
   "depth": "extended",
   "text": "A complete interpretation names the quantity, the instant, the direction of change, and the units. A negative rate means the quantity is decreasing; the size is the rate's magnitude.",
   "notation": "units of f per unit of t",
   "quote": {
    "text": "The derivative can be used to express information about rates of change in applied contexts.",
    "source": "ced:87"
   },
   "sources": [
    "BC-EK-CHA-3A2",
    "ced:87",
    "sg-24:2",
    "sg-25:11",
    "research/units/unit-04-contextual-applications-differentiation.md#4.1 Interpreting the Meaning of the Derivative in Context"
   ]
  }
 ],
 "strategy": [
  {
   "id": "st-1",
   "archetype_id": "BC-QA-04001",
   "cue": "A derivative value to interpret.",
   "method": "Name the quantity and the instant.",
   "rival": "The value read as an amount.",
   "separating_feature": "The prime makes it a rate.",
   "sources": [
    "BC-QA-04001",
    "BC-ERR-04003"
   ],
   "evidence_tag": "verified",
   "contrast": {
    "this": {
     "text": "\\(C'(5)=-2\\) for a coffee's temperature in degrees Celsius. Interpret it.",
     "archetype_id": "BC-QA-04001"
    },
    "not_this": {
     "text": "\\(C(5)=62\\), the coffee's temperature. Interpret it.",
     "why_not": "No prime: an amount, not a rate."
    },
    "feature": "A prime marks a rate."
   }
  }
 ],
 "worked_examples": [
  {
   "id": "ex-1",
   "archetype_id": "BC-QA-04001",
   "bands": [
    "low",
    "mid"
   ],
   "parameter_draw": {
    "context": "tank",
    "instant": 9,
    "magnitude": "7/2",
    "sign": "negative",
    "order": "first"
   },
   "problem": {
    "text": "\\(W(t)\\) is the water in a tank, in liters, at \\(t\\) minutes. \\(W'(9)=-3.5\\). Using correct units, interpret \\(W'(9)=-3.5\\).",
    "command_verb": "interpret"
   },
   "calculator_status": "no_calculator",
   "steps": [
    {
     "cue": "The given value carries a prime.",
     "why": "A rate at \\(t=9\\), not an amount.",
     "expr": "-7/2",
     "relation": "new"
    },
    {
     "cue": "The value is negative.",
     "why": "The water is decreasing."
    },
    {
     "cue": "\\(W\\) in liters, \\(t\\) in minutes.",
     "why": "Liters per minute."
    },
    {
     "cue": "Interpret: one sentence.",
     "why": "At \\(t=9\\) minutes the water decreases at 3.5 liters per minute.",
     "point_type_id": "BC-PT-99008"
    }
   ],
   "answer": {
    "form": "statement",
    "expr": "-7/2",
    "text": "At t = 9 minutes the amount of water in the tank is decreasing at 3.5 liters per minute."
   }
  }
 ],
 "what_a_reader_scores": [
  {
   "example_id": "ex-1",
   "point_type_ids": [
    "BC-PT-99008"
   ],
   "lines": [
    {
     "point_type_id": "BC-PT-99008",
     "text": "Interpretation of a derivative value in context with units. Earned by: A sentence giving the rate of change of the named quantity, its value, its units, and the instant it applies to (sg-21:3, sg-23:4). Not earned by: An interpretation whose sign language contradicts the presented value, such as decreasing at a rate of a negative number (sg-23:4). Units are required on the answer."
    }
   ]
  }
 ],
 "common_errors": [
  {
   "error_id": "BC-ERR-04001",
   "wrong_step": {
    "text": "Decreasing at 3.5 minutes per liter.",
    "expr": "3.5*minute/liter"
   },
   "right_step": {
    "text": "Decreasing at 3.5 liters per minute.",
    "expr": "3.5*liter/minute"
   },
   "relation": "distinct",
   "possible_reason": {
    "misconception_id": "BC-MIS-04003",
    "text": "the unit as something added at the end"
   },
   "sources": [
    "BC-ERR-04001",
    "BC-MIS-04003"
   ],
   "observed_behavior": "A correct numerical rate is reported with no units, or with the units of the quantity alone, or with the numerator and denominator units exchanged.",
   "scoring_consequence": "The units point is a separate point in the 2024 and 2025 table based questions and is lost outright (sg-24:2, sg-25:11); BC-ERR-99005 records the same behaviour across years.",
   "fix_prompt": true
  },
  {
   "error_id": "BC-ERR-04003",
   "wrong_step": {
    "text": "3.5 liters in the tank.",
    "expr": "3.5*liter"
   },
   "right_step": {
    "text": "A rate, liters per minute.",
    "expr": "-3.5*liter/minute"
   },
   "relation": "distinct",
   "possible_reason": {
    "misconception_id": "BC-MIS-04001",
    "text": "its amount or its rate of change"
   },
   "sources": [
    "BC-ERR-04003",
    "BC-MIS-04001"
   ],
   "observed_behavior": "The response supplies a value of the modelled function where the question asked for a value of its derivative, or the reverse.",
   "scoring_consequence": "The answer point is lost; BC-ERR-99030 records confusion of the direction of change with the quantity itself.",
   "fix_prompt": true
  },
  {
   "error_id": "BC-ERR-04005",
   "wrong_step": {
    "text": "Increasing at 3.5 liters per minute.",
    "expr": "3.5"
   },
   "right_step": {
    "text": "Decreasing at 3.5 liters per minute.",
    "expr": "-3.5"
   },
   "relation": "distinct",
   "possible_reason": {
    "misconception_id": "BC-MIS-04002",
    "text": "treats its sign as a formatting detail rather than as the statement that the quantity is falling"
   },
   "sources": [
    "BC-ERR-04005",
    "BC-MIS-04002"
   ],
   "observed_behavior": "A negative rate is reported as a magnitude or is described as an increase.",
   "scoring_consequence": "The interpretation point is lost; BC-ERR-99030 records the same confusion of direction with quantity.",
   "fix_prompt": true
  },
  {
   "error_id": "BC-ERR-99027",
   "wrong_step": {
    "text": "It changes at 3.5 liters per minute.",
    "expr": "-3.5"
   },
   "right_step": {
    "text": "At \\(t=9\\) the water decreases at 3.5 liters per minute.",
    "expr": "-3.5"
   },
   "relation": "equivalent",
   "possible_reason": null,
   "sources": [
    "BC-ERR-99027"
   ],
   "observed_behavior": "Responses interpret a derivative or an integral without naming the quantity, the interval, or the fact that a rate is itself changing, or they answer a different question than the one asked.",
   "scoring_consequence": "The interpretation point requires the key phrases, so an answer missing the interval or the rate of a rate is not earned.",
   "fix_prompt": false
  }
 ],
 "representations": null,
 "prerequisite_bridges": [
  {
   "prq_id": "BC-PRQ-04004",
   "text": "A compound unit is a quotient, such as liters per minute, attached to the value."
  },
  {
   "prq_id": "BC-PRQ-04008",
   "text": "Name each quantity, its unit, and whether it varies."
  }
 ],
 "time": {
  "exam_part": "I-A",
  "budget_minutes": 2.14,
  "source": "research/exam/exam-structure.md#Section and part layout",
  "written_steps": {
   "ex-1": [
    4
   ]
  },
  "skipped_steps": {
   "ex-1": [
    1,
    2,
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
   "archetype_id": "BC-QA-04001",
   "parameter_draw": {
    "context": "tank",
    "instant": 9,
    "magnitude": "7/2",
    "sign": "negative",
    "order": "first"
   },
   "completes": "ex-1",
   "stem": {
    "text": "\\(W'(9)=-3.5\\), liters and minutes. Complete: at \\(t=9\\) minutes, the water in the tank is ...",
    "command_verb": "complete"
   },
   "key": {
    "form": "statement",
    "expr": "-7/2",
    "text": "decreasing at 3.5 liters per minute"
   },
   "steps": [
    {
     "text": "A negative rate: decreasing, size 3.5, liters per minute.",
     "expr": "-7/2",
     "relation": "new"
    }
   ],
   "calculator_status": "no_calculator",
   "skills": [
    "BC-SKL-04002"
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
   "archetype_id": "BC-QA-04001",
   "parameter_draw": {
    "context": "snow",
    "instant": 10,
    "magnitude": "5/2",
    "sign": "positive",
    "order": "first"
   },
   "stem": {
    "text": "\\(S(t)\\) is snow depth in centimeters at \\(t\\) hours. Interpret \\(S'(10)=2.5\\) with units.",
    "command_verb": "interpret"
   },
   "key": {
    "form": "statement",
    "expr": "5/2",
    "text": "At t = 10 hours the snow depth is increasing at 2.5 centimeters per hour."
   },
   "steps": [
    {
     "text": "Positive rate: increasing, centimeters per hour.",
     "expr": "5/2",
     "relation": "new"
    }
   ],
   "calculator_status": "no_calculator",
   "skills": [
    "BC-SKL-04002",
    "BC-SKL-04005"
   ]
  },
  {
   "id": "chk-3",
   "check_kind": "mcq",
   "format": "mcq",
   "bands": [
    "low"
   ],
   "archetype_id": "BC-QA-04001",
   "parameter_draw": {
    "context": "balloon",
    "instant": 3,
    "magnitude": 4,
    "sign": "negative",
    "order": "first"
   },
   "stem": {
    "text": "\\(V(t)\\) is a balloon's volume in cubic centimeters at \\(t\\) seconds, and \\(V'(3)=-4\\). Which interprets \\(V'(3)\\)?",
    "command_verb": "identify"
   },
   "key": {
    "form": "statement",
    "expr": "-4",
    "text": "A"
   },
   "steps": [
    {
     "text": "Negative rate at t = 3: decreasing, cubic centimeters per second.",
     "expr": "-4",
     "relation": "new"
    }
   ],
   "options": [
    {
     "id": "A",
     "is_key": true,
     "label": "At t = 3 seconds the volume is decreasing at 4 cubic centimeters per second.",
     "error_path": null
    },
    {
     "id": "B",
     "is_key": false,
     "label": "At t = 3 seconds the balloon holds 4 cubic centimeters of air.",
     "error_path": "BC-ERR-04003",
     "derivation": "the rate read as an amount"
    },
    {
     "id": "C",
     "is_key": false,
     "label": "At t = 3 seconds the volume is increasing at 4 cubic centimeters per second.",
     "error_path": "BC-ERR-04005",
     "derivation": "the negative sign dropped and read as an increase"
    },
    {
     "id": "D",
     "is_key": false,
     "label": "At t = 3 seconds the volume is decreasing at 4 seconds per cubic centimeter.",
     "error_path": "BC-ERR-04001",
     "derivation": "the units assembled the wrong way round"
    }
   ],
   "calculator_status": "no_calculator",
   "skills": [
    "BC-SKL-04002",
    "BC-SKL-04003",
    "BC-SKL-04005"
   ]
  }
 ],
 "delivery": [
  {
   "block": "pr-1",
   "mode": "text",
   "reason": "rule 6: a prediction on the worked example's numbers with no picture in the question",
   "sources": [
    "BC-SKL-04003"
   ]
  },
  {
   "block": "orientation",
   "mode": "text",
   "reason": "rule 5: BC-SKL-04002, 04003, 04005 carry BC-REP-04 and BC-REP-05 only",
   "sources": [
    "BC-SKL-04002"
   ]
  },
  {
   "block": "ki-1",
   "mode": "text",
   "reason": "rule 5: a definition with BC-REP-04 and BC-REP-05 givens",
   "sources": [
    "BC-SKL-04003"
   ]
  },
  {
   "block": "ki-2",
   "mode": "text",
   "reason": "rule 5: a rule for the sentence, BC-REP-04 and BC-REP-05",
   "sources": [
    "BC-SKL-04005"
   ]
  },
  {
   "block": "ex-1",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  },
  {
   "block": "err-BC-ERR-04001",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  },
  {
   "block": "err-BC-ERR-04003",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  },
  {
   "block": "err-BC-ERR-04005",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  },
  {
   "block": "err-BC-ERR-99027",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  }
 ],
 "refresher": [
  "ki-1",
  "err-BC-ERR-04001",
  "err-BC-ERR-04003",
  "err-BC-ERR-04005",
  "err-BC-ERR-99027",
  "ex-1"
 ],
 "research_lines": [
  {
   "file": "research/scoring/common-point-losses.md",
   "line": "An interpretation point asks what a computed value means in the setting of the problem"
  }
 ],
 "inferred": [
  {
   "claim": "BC-QA-04001 is calculator status either, so the lesson times it as Section I Part A at 2.14 minutes.",
   "settles": "A calculator status of calculator or no_calculator on BC-QA-04001."
  }
 ],
 "sources": [
  "BC-CON-04001",
  "BC-SKL-04002",
  "BC-SKL-04003",
  "BC-SKL-04005",
  "BC-EK-CHA-3A1",
  "BC-EK-CHA-3A2",
  "ced:87",
  "sg-24:2",
  "sg-25:11",
  "sg-23:4",
  "sg-21:3",
  "cr-23:4",
  "BC-QA-04001",
  "BC-PT-99008",
  "BC-ERR-04001",
  "BC-ERR-04003",
  "BC-ERR-04005",
  "BC-ERR-99027",
  "BC-MIS-04001",
  "BC-MIS-04002",
  "BC-MIS-04003",
  "BC-PRQ-04004",
  "BC-PRQ-04008",
  "research/units/unit-04-contextual-applications-differentiation.md#4.1 Interpreting the Meaning of the Derivative in Context",
  "research/question-analysis/question-archetypes.md#BC-QA-04001 Interpreting the value of a derivative in context with units",
  "research/scoring/common-point-losses.md#Interpretation points",
  "research/scoring/common-point-losses.md#Units points",
  "research/exam/exam-structure.md#Section and part layout"
 ],
 "word_count": {
  "full": 702,
  "brief": 449
 },
 "read_minutes": {
  "full": 4.7,
  "brief": 3.0
 }
}
```
