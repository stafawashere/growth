---
title: LSN-CON-08006 Amount at a time from an initial amount and a rate
research_date: 2026-09-29
status: designed
purpose: Authoring spec for the concept lesson on BC-CON-08006, the amount at a time as the initial amount plus the integral of its rate, built from authoring_bundle("BC-CON-08006") and the research files it cites, so an author fills plan 15's lesson record without making a teaching decision.
---

# LSN-CON-08006 Amount at a time from an initial amount and a rate

Concept BC-CON-08006 (skills BC-SKL-08012, BC-SKL-08016, BC-SKL-08017), topic 8.3 of Unit 8, first in the applied accumulation strand with no Unit 8 hard parent (docs/lessons/unit-08/README.md, section 1). The skills name retired archetype ids; the bundle lists their successors and neighbours: BC-QA-06005, 06006, 08006, 99008, 99009.

## Prediction

One multiple choice question on worked example 1's own numbers, asked before the rule is shown: water enters a tank at \(R(t)=4t+3\) gallons per hour, the tank holds 40 gallons at t = 2, and the student picks the expression for the gallons at t = 4. The key is 40 plus the integral of R from 2 to 4; the distractors are the integral alone and 40 times R(4). The resolution, shown on the key idea screen, gives the 30 gallons gained and the 70 gallons present. No verdict word. Sources: BC-CON-08006 and the topic 8.3 section the key ideas cite. [inferred]

## Orientation

Served text, from BC-CON-08006 `description_plain` and the topic's Assessment behaviour paragraph (research/units/unit-08-applications-integration.md#8.3 Using Accumulation Functions and Definite Integrals in Applied Contexts): a response writes the amount at the asked time as the known amount plus the definite integral of the rate, with the differential, then reports the value with units. No count, no frequency.

## Key ideas

BC-SKL-08012 maps to BC-EK-CHA-4D1 and BC-EK-CHA-4E1; BC-SKL-08016 and 08017 to BC-EK-CHA-4E1 (ced:154). Two blocks.

- ki-1 (core, both bands), BC-EK-CHA-4D1. Paraphrase of the Required mathematical knowledge paragraphs (Accumulation, Amount at a time): a function defined as an integral accumulates a rate; the amount at t is the amount at a plus the integral of the rate from a to t (sg-24:4).
- ki-2 (extended, low band), BC-EK-CHA-4E1. Paraphrase of the Interpretation and Notation paragraphs: in context the integral is the amount gained over the interval, and a complete statement names the quantity, the interval and the units (sg-23:2).

No anchor quotes. Notation line on ki-1 from the concept record.

## Recognition

- BC-QA-06005 (research/question-analysis/question-archetypes.md#BC-QA-06005 Net change from a rate with an initial condition): `common_givens` a rate function and a known value at one time; `asked_to_produce` an integral expression with the initial value and a value with units. The signal: "how much ... at time t" with a stated amount.
- BC-QA-99008 (research/question-analysis/question-archetypes.md#BC-QA-99008 Total amount from a rate over an interval with no initial condition and no rate out): "how many units flow in during the stated time interval"; the integral alone.
- BC-QA-08006 (research/question-analysis/question-archetypes.md#BC-QA-08006 Time at which an accumulated amount is maximal): "at what time ... does the modelled amount attain its maximum".

The contrast pair on st-1 sets a BC-QA-06005 stem (a modelled rate and one known value, the later value asked) against a BC-QA-99008 stem (how many gallons flow in over the interval, the integral alone). The near miss comes from BC-QA-99008, the archetype whose `wrong_approaches` name the initial-condition reading and whose `prohibited_shortcuts` name adding the initial amount; the feature is the known amount with the amount at another time asked.

These are the Q1 chain (BC-FRQ-2013-Q1-B to D, BC-FRQ-2015-Q1-A to D; docs/lessons/unit-08/README.md, section 3). BC-QA-06006 (two rates) belongs to BC-CON-08007 and BC-QA-99009 (density) to topic 8.3's later concepts; neither gets a block (cap 3).

## Method choice

- st-1, BC-QA-06005 (both bands), carrying the contrast pair. Method, `expected_solution_path[0]`: the later value as the earlier value plus the definite integral of the rate. Rival, `wrong_approaches`: reporting the net change as the amount. Separating feature: a stated amount plus "how much at time t". The served fields carry no leading label.
- st-2, BC-QA-99008 (low band). Method: read the interval out of the wording. Rival, `wrong_approaches`: treating the part as a net change question because the stem gives an initial condition. Separating feature: "how much entered" asks for the change.
- st-3, BC-QA-08006 (low band). Method: differentiate the amount function. Rival: presenting a local argument for a global claim. Separating feature: "greatest" asks for a time.

All three carry `asked_to_produce` and `common_givens`; none is tagged inferred.

## Solution path

- ex-1, BC-QA-06005, both bands, no calculator. Draw: cubic 0, square 2, linear 3, start 2, span 2, known 40, base_rate 6, swing 2, stretch 4, horizon 3, context tank, tool exact, direction forward; rate \(R(t)=4t+3\) gallons per hour, 40 gallons at t = 2. Exact options 70, 30, 48, 84 are distinct. No published item carries this draw.
- Steps: the setup (new, tagged BC-PT-99033); the integral's value in place (equivalent); the sum (equivalent). A fluent solver writes all three. One example only, so no `fade_from`.

## Scoring

ex-1 tags BC-PT-99033; the line is `reader_checks(["BC-PT-99033"])`. BC-PT-99001 (the integral with limits) and BC-PT-99004 (the answer) are earned on steps 1 and 3 but not tagged, to hold the brief cap (listed inferred). Pattern: the integral without the initial amount does not earn BC-PT-99033 (sg-24:3, sg-24:4). Point losses: the differential omitted (research/scoring/common-point-losses.md#Setup points, BC-ERR-99006); units missing (research/scoring/common-point-losses.md#Units points, BC-ERR-99005).

## Traps

Six active errors meet the skills; the first four in the bundle's order are served: BC-ERR-08011, 08012, 99006, 99005. Mid band the first two. BC-ERR-99019 and BC-ERR-99032 are not served (cap 4).

- err-BC-ERR-08011: the integral alone. Possible reason, words from BC-MIS-08006.
- err-BC-ERR-08012: the net change 30 reported as the amount. Possible reason, words from BC-MIS-08006.
- err-BC-ERR-99006: dx written for a rate in t. Possible reason, words from BC-MIS-08013.
- err-BC-ERR-99005: gallons per hour on an amount. Values equal, relation equivalent. No possible reason line.

## Representations

None as a separate block. The topic's Representations paragraph names a tabulated rate (BC-REP-03), which no ex-1 given uses; ki-1's motion carries the accumulation picture.

## Prerequisite bridge

- BC-PRQ-06005, BC-PRQ-08006.

## Time

BC-QA-06005 is `either`: Section I Part A, 2.14 minutes per question (research/exam/exam-structure.md#Section and part layout) [inferred]. In the calculator free response form the part is 3 points, a 5.0 minute share (docs/lessons/unit-08/README.md, section 5).

## Checks

- chk-1, completion of ex-1, both bands. Key 70.
- chk-2, isomorph, both bands. Draw: cubic -1, square 3, linear 4, start 1, span 1, known 30. Key 36.
- chk-3, MCQ, low band, statement key. Draw: cubic 0, square 1, linear 4, start 1, span 3, known 20. Distractors carry BC-ERR-08011, 99006, 99005. BC-ERR-08012 gives the same number as BC-ERR-08011 on every draw, so it has no distinct distractor.

## Delivery

- orientation: text. Rule 6.
- ki-1: motion. Rule 2: "an accumulation of a rate of change" (ced:154) is a quantity accumulating; the unit README's delivery map names the amount traced from its initial value as the upper time moves [inferred; settled by the modality A/B].
- ki-2: text. Rule 6.
- ex-1 and the four error blocks: step_reveal. Rule 1.

## Band plan

- Low (full), in served order: prediction, orientation, two bridges, ki-1, ki-2, st-1 with its contrast, st-2, st-3, ex-1 with its scoring line, chk-1, four error blocks, chk-2, chk-3. 758 words, 5.1 minutes.
- Mid (brief): prediction, orientation, two bridges, ki-1, st-1 with its contrast, ex-1 with its scoring line, chk-1, err-BC-ERR-08011, err-BC-ERR-08012, chk-2. 449 words, 3.0 minutes. To fit the cap the orientation, ki-1, the st-1 fields, the ex-1 cues and whys and the bridges were shortened; no anchor quote or scoring tag was dropped.
- Refresher: ki-1, the four error blocks, ex-1.

## Sources

- BC-CON-08006; the prediction (pr-1) cites it and the topic 8.3 heading below; BC-SKL-08012, BC-SKL-08016, BC-SKL-08017; BC-EK-CHA-4D1, BC-EK-CHA-4E1; ced:154
- BC-QA-06005, BC-QA-99008, BC-QA-08006, BC-QA-06006, BC-QA-99009; BC-PT-99033; sg-24:3, sg-24:4, sg-23:2
- BC-ERR-08011, BC-ERR-08012, BC-ERR-99006, BC-ERR-99005, BC-ERR-99019, BC-ERR-99032; BC-MIS-08006, BC-MIS-08013
- BC-PRQ-06005, BC-PRQ-08006
- research/units/unit-08-applications-integration.md#8.3 Using Accumulation Functions and Definite Integrals in Applied Contexts
- research/question-analysis/question-archetypes.md#BC-QA-06005 Net change from a rate with an initial condition
- research/question-analysis/question-archetypes.md#BC-QA-99008 Total amount from a rate over an interval with no initial condition and no rate out
- research/question-analysis/question-archetypes.md#BC-QA-08006 Time at which an accumulated amount is maximal
- research/scoring/common-point-losses.md#Setup points
- research/scoring/common-point-losses.md#Units points
- research/exam/exam-structure.md#Section and part layout
- [inferred] Exam part I-A for an "either" archetype. Settled by the item mix.
- [inferred] The prediction and the contrast pair as teaching moves. Settled by the modality and prompt A/B in the build plan.
- [inferred] ki-1 as motion. Settled by the modality A/B.
- [inferred] BC-PT-99001 and BC-PT-99004 untagged. Settled by a brief cap that admits three reader lines.

## Machine record

```json
{
 "id": "LSN-CON-08006",
 "kind": "concept",
 "target_id": "BC-CON-08006",
 "unit": "08",
 "skills": [
  "BC-SKL-08012",
  "BC-SKL-08016",
  "BC-SKL-08017"
 ],
 "prediction": {
  "id": "pr-1",
  "stem": {
   "text": "Water enters a tank at \\(R(t)=4t+3\\) gallons per hour; it holds 40 gallons at \\(t=2\\). Which gives the gallons at \\(t=4\\)?",
   "command_verb": "predict"
  },
  "format": "mcq",
  "options": [
   {
    "id": "A",
    "label": "The integral of \\(R\\) from 2 to 4",
    "is_key": false
   },
   {
    "id": "B",
    "label": "40 plus the integral of \\(R\\) from 2 to 4",
    "is_key": true
   },
   {
    "id": "C",
    "label": "40 times \\(R(4)\\)",
    "is_key": false
   }
  ],
  "resolution": "The integral of \\(R\\) from 2 to 4 is 30 gallons gained; adding the 40 already there gives 70 gallons.",
  "sources": [
   "BC-CON-08006",
   "research/units/unit-08-applications-integration.md#8.3 Using Accumulation Functions and Definite Integrals in Applied Contexts"
  ]
 },
 "orientation": {
  "text": "A response adds the known amount to the rate's integral, with units.",
  "sources": [
   "BC-CON-08006",
   "research/units/unit-08-applications-integration.md#8.3 Using Accumulation Functions and Definite Integrals in Applied Contexts"
  ]
 },
 "key_ideas": [
  {
   "id": "ki-1",
   "ek_id": "BC-EK-CHA-4D1",
   "depth": "core",
   "text": "The amount at t is the amount at a plus the integral of the rate from a to t.",
   "notation": "Q(t) = Q(a) + integral of q",
   "quote": null,
   "sources": [
    "BC-EK-CHA-4D1",
    "ced:154",
    "sg-24:4",
    "research/units/unit-08-applications-integration.md#8.3 Using Accumulation Functions and Definite Integrals in Applied Contexts"
   ]
  },
  {
   "id": "ki-2",
   "ek_id": "BC-EK-CHA-4E1",
   "depth": "extended",
   "text": "In context, the integral of a rate over an interval is the amount gained over that interval, in the rate's units times the input's units. A complete statement names the quantity, the interval and the units.",
   "notation": "",
   "quote": null,
   "sources": [
    "BC-EK-CHA-4E1",
    "ced:154",
    "sg-23:2",
    "research/units/unit-08-applications-integration.md#8.3 Using Accumulation Functions and Definite Integrals in Applied Contexts"
   ]
  }
 ],
 "strategy": [
  {
   "id": "st-1",
   "archetype_id": "BC-QA-06005",
   "cue": "A rate and a known amount; the later amount is asked.",
   "method": "The known amount plus the definite integral of the rate.",
   "rival": "Reporting the net change as the amount.",
   "separating_feature": "A stated amount plus how much at t.",
   "sources": [
    "BC-QA-06005"
   ],
   "evidence_tag": "verified",
   "contrast": {
    "this": {
     "text": "A quantity's rate is modelled by \\(R(t)\\), and its value is known at one time. Find its value later, showing the setup.",
     "archetype_id": "BC-QA-06005"
    },
    "not_this": {
     "text": "How many gallons flow in from \\(t=2\\) to \\(t=4\\), given \\(R(t)\\)?",
     "why_not": "It asks for the amount entered only."
    },
    "feature": "A known amount, and the later amount asked."
   }
  },
  {
   "id": "st-2",
   "archetype_id": "BC-QA-99008",
   "cue": "A rate function and a closed interval; the total that arrives is asked.",
   "method": "Read the interval out of the wording, then the integral of the rate over it.",
   "rival": "Treating the part as a net change question because the stem gives an initial condition.",
   "separating_feature": "How much entered asks for the change, not the amount.",
   "sources": [
    "BC-QA-99008"
   ],
   "evidence_tag": "verified"
  },
  {
   "id": "st-3",
   "archetype_id": "BC-QA-08006",
   "cue": "An amount defined with a definite integral and a closed interval; the time of the maximum is asked.",
   "method": "Differentiate the amount function.",
   "rival": "Presenting a local argument for a global claim.",
   "separating_feature": "Greatest asks for a time, with both endpoints as candidates.",
   "sources": [
    "BC-QA-08006"
   ],
   "evidence_tag": "verified"
  }
 ],
 "worked_examples": [
  {
   "id": "ex-1",
   "archetype_id": "BC-QA-06005",
   "bands": [
    "low",
    "mid"
   ],
   "parameter_draw": {
    "cubic": 0,
    "square": 2,
    "linear": 3,
    "start": 2,
    "span": 2,
    "known": 40,
    "base_rate": 6,
    "swing": 2,
    "stretch": 4,
    "horizon": 3,
    "context": "tank",
    "tool": "exact",
    "direction": "forward"
   },
   "problem": {
    "text": "Water enters a tank at R(t) = 4t + 3 gallons per hour. At t = 2 the tank holds 40 gallons. Find A(4), showing the setup.",
    "command_verb": "find"
   },
   "calculator_status": "no_calculator",
   "steps": [
    {
     "cue": "Amount at t = 4, known at t = 2.",
     "why": "The integral is gallons gained; add the start.",
     "expr": "40 + Integral(4*t + 3, (t, 2, 4))",
     "relation": "new",
     "point_type_id": "BC-PT-99033"
    },
    {
     "cue": "2t^2 + 3t from 2 to 4.",
     "why": "44 - 14 = 30.",
     "expr": "40 + 30",
     "relation": "equivalent"
    },
    {
     "cue": "Add the known amount.",
     "why": "Gallons.",
     "expr": "70",
     "relation": "equivalent"
    }
   ],
   "answer": {
    "form": "symbolic",
    "expr": "70"
   }
  }
 ],
 "what_a_reader_scores": [
  {
   "example_id": "ex-1",
   "point_type_ids": [
    "BC-PT-99033"
   ],
   "lines": [
    {
     "point_type_id": "BC-PT-99033",
     "text": "Uses the initial condition in an accumulation expression. Earned by: Adding the known function value at one endpoint to a definite integral of the rate (sg-24:3, sg-22:8). Not earned by: A definite integral alone with the known value never added (sg-22:8). Notation: sg-22:8 lists cases where a missing differential shifts which of the three points are available."
    }
   ]
  }
 ],
 "common_errors": [
  {
   "error_id": "BC-ERR-08011",
   "observed_behavior": "The response evaluates the integral of the rate and reports it as the value of the quantity.",
   "scoring_consequence": "The initial condition point is lost and the answer point falls with it (sg-24:7).",
   "wrong_step": {
    "text": "The integral alone.",
    "expr": "Integral(4*t + 3, (t, 2, 4))"
   },
   "right_step": {
    "text": "40 plus the integral.",
    "expr": "40 + Integral(4*t + 3, (t, 2, 4))"
   },
   "relation": "distinct",
   "possible_reason": {
    "misconception_id": "BC-MIS-08006",
    "text": "reads an accumulation integral as the quantity itself rather than as the change in it"
   },
   "sources": [
    "BC-ERR-08011",
    "BC-MIS-08006"
   ],
   "fix_prompt": true
  },
  {
   "error_id": "BC-ERR-08012",
   "observed_behavior": "A question asking how much is present at a time is answered with the net change over the interval.",
   "scoring_consequence": "The answer point is lost even when the integral is correct.",
   "wrong_step": {
    "text": "30 gallons reported as present.",
    "expr": "30"
   },
   "right_step": {
    "text": "70 gallons present.",
    "expr": "70"
   },
   "relation": "distinct",
   "possible_reason": {
    "misconception_id": "BC-MIS-08006",
    "text": "so the initial value has no role"
   },
   "sources": [
    "BC-ERR-08012",
    "BC-MIS-08006"
   ],
   "fix_prompt": true
  },
  {
   "error_id": "BC-ERR-99006",
   "observed_behavior": "Responses present a definite integral with no differential, or with a differential in the wrong variable, producing a setup the reader cannot interpret.",
   "scoring_consequence": "The setup point is not earned when the resulting expression is ambiguous; in some parts later points in that part are also lost.",
   "wrong_step": {
    "text": "dx for a rate in t.",
    "expr": "40 + Integral(4*t + 3, (x, 2, 4))"
   },
   "right_step": {
    "text": "dt.",
    "expr": "40 + Integral(4*t + 3, (t, 2, 4))"
   },
   "relation": "distinct",
   "possible_reason": {
    "misconception_id": "BC-MIS-08013",
    "text": "treats dx and dy as labels"
   },
   "sources": [
    "BC-ERR-99006",
    "BC-MIS-08013"
   ],
   "fix_prompt": true
  },
  {
   "error_id": "BC-ERR-99005",
   "observed_behavior": "Responses give no units where units are requested, or report units of the original quantity instead of the derived one, for example words per minute for a second difference quotient.",
   "scoring_consequence": "The units point is not earned; it is scored separately from the value.",
   "wrong_step": {
    "text": "70 gallons per hour.",
    "expr": "70"
   },
   "right_step": {
    "text": "70 gallons.",
    "expr": "70"
   },
   "relation": "equivalent",
   "possible_reason": null,
   "sources": [
    "BC-ERR-99005"
   ],
   "fix_prompt": false
  }
 ],
 "representations": null,
 "prerequisite_bridges": [
  {
   "prq_id": "BC-PRQ-06005",
   "text": "40 is an amount; R is a rate."
  },
  {
   "prq_id": "BC-PRQ-08006",
   "text": "Full precision, then three places."
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
    3
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
   "archetype_id": "BC-QA-06005",
   "parameter_draw": {
    "cubic": 0,
    "square": 2,
    "linear": 3,
    "start": 2,
    "span": 2,
    "known": 40,
    "base_rate": 6,
    "swing": 2,
    "stretch": 4,
    "horizon": 3,
    "context": "tank",
    "tool": "exact",
    "direction": "forward"
   },
   "completes": "ex-1",
   "stem": {
    "text": "A(2) = 40 gallons and the integral of R from 2 to 4 is 30. Find A(4).",
    "command_verb": "find"
   },
   "key": {
    "form": "symbolic",
    "expr": "70"
   },
   "steps": [
    {
     "text": "Known amount plus change.",
     "expr": "40 + 30",
     "relation": "new"
    },
    {
     "text": "Add.",
     "expr": "70",
     "relation": "equivalent"
    }
   ],
   "calculator_status": "no_calculator",
   "skills": [
    "BC-SKL-08012"
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
   "archetype_id": "BC-QA-06005",
   "parameter_draw": {
    "cubic": -1,
    "square": 3,
    "linear": 4,
    "start": 1,
    "span": 1,
    "known": 30,
    "base_rate": 6,
    "swing": 2,
    "stretch": 4,
    "horizon": 3,
    "context": "tank",
    "tool": "exact",
    "direction": "forward"
   },
   "stem": {
    "text": "R(t) = -3t^2 + 6t + 4 gallons per hour and A(1) = 30 gallons. Find A(2).",
    "command_verb": "find"
   },
   "key": {
    "form": "symbolic",
    "expr": "36"
   },
   "steps": [
    {
     "text": "Setup.",
     "expr": "30 + Integral(-3*t**2 + 6*t + 4, (t, 1, 2))",
     "relation": "new"
    },
    {
     "text": "30 + 6.",
     "expr": "36",
     "relation": "equivalent"
    }
   ],
   "calculator_status": "no_calculator",
   "skills": [
    "BC-SKL-08012"
   ]
  },
  {
   "id": "chk-3",
   "check_kind": "mcq",
   "format": "mcq",
   "bands": [
    "low"
   ],
   "archetype_id": "BC-QA-06005",
   "parameter_draw": {
    "cubic": 0,
    "square": 1,
    "linear": 4,
    "start": 1,
    "span": 3,
    "known": 20,
    "base_rate": 6,
    "swing": 2,
    "stretch": 4,
    "horizon": 3,
    "context": "tank",
    "tool": "exact",
    "direction": "forward"
   },
   "stem": {
    "text": "R(t) = 2t + 4 gallons per hour and A(1) = 20 gallons. Which response earns every point for A(4)?",
    "command_verb": "identify"
   },
   "key": {
    "form": "statement",
    "expr": "20 + Integral(2*t + 4, (t, 1, 4))"
   },
   "options": [
    {
     "id": "A",
     "is_key": true,
     "label": "20 + integral from 1 to 4 of R(t) dt = 47 gallons",
     "error_path": null
    },
    {
     "id": "B",
     "is_key": false,
     "label": "integral from 1 to 4 of R(t) dt = 27 gallons",
     "error_path": "BC-ERR-08011",
     "derivation": "the integral reported with the 20 gallons left out"
    },
    {
     "id": "C",
     "is_key": false,
     "label": "20 + integral from 1 to 4 of R(t) dx = 47 gallons",
     "error_path": "BC-ERR-99006",
     "derivation": "the differential in the wrong variable"
    },
    {
     "id": "D",
     "is_key": false,
     "label": "20 + integral from 1 to 4 of R(t) dt = 47 gallons per hour",
     "error_path": "BC-ERR-99005",
     "derivation": "the rate's units on an amount"
    }
   ],
   "calculator_status": "no_calculator",
   "skills": [
    "BC-SKL-08012",
    "BC-SKL-08016",
    "BC-SKL-08017"
   ]
  }
 ],
 "delivery": [
  {
   "block": "orientation",
   "mode": "text",
   "reason": "rule 6: a statement of what a response shows",
   "sources": [
    "BC-SKL-08012"
   ]
  },
  {
   "block": "ki-1",
   "mode": "motion",
   "reason": "rule 2: an accumulation of a rate of change (ced:154) is a quantity accumulating; unit README delivery map, the amount traced from its initial value",
   "sources": [
    "BC-SKL-08012"
   ],
   "spec": {
    "kind": "graph",
    "representations": [
     "BC-REP-05",
     "BC-REP-01"
    ],
    "window": {
     "x": [
      2,
      4
     ],
     "y": [
      0,
      80
     ]
    },
    "curves": [
     {
      "expr": "2*x**2 + 3*x + 26",
      "domain": [
       2,
       4
      ],
      "name": "A(x) = 40 + integral from 2 to x of R(t) dt"
     }
    ],
    "frames": [
     {
      "x": 2,
      "y": 40
     },
     {
      "x": 3,
      "y": 53
     },
     {
      "x": 4,
      "y": 70
     }
    ],
    "labels": [
     {
      "text": "A(2) = 40: the start",
      "placement": "inside"
     },
     {
      "text": "A(x) = 40 + integral from 2 to x of R",
      "placement": "inside"
     },
     {
      "text": "A(4) = 70",
      "placement": "inside"
     }
    ]
   },
   "reduced_motion": "a cross-fade between the three frames on the student's own key press; no auto-advance",
   "fallback": "the three frames side by side, static, each with its label inside",
   "keyboard": "Right arrow steps to the next frame, Left arrow to the previous; Space pauses auto-advance"
  },
  {
   "block": "ki-2",
   "mode": "text",
   "reason": "rule 6: an interpretation habit, BC-REP-05 and 01",
   "sources": [
    "BC-SKL-08016",
    "BC-SKL-08017"
   ]
  },
  {
   "block": "ex-1",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  },
  {
   "block": "err-BC-ERR-08011",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  },
  {
   "block": "err-BC-ERR-08012",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  },
  {
   "block": "err-BC-ERR-99006",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  },
  {
   "block": "err-BC-ERR-99005",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  }
 ],
 "refresher": [
  "ki-1",
  "err-BC-ERR-08011",
  "err-BC-ERR-08012",
  "err-BC-ERR-99006",
  "err-BC-ERR-99005",
  "ex-1"
 ],
 "read_minutes": {
  "full": 5.1,
  "brief": 3.0
 },
 "word_count": {
  "full": 757,
  "brief": 448
 },
 "research_lines": [
  {
   "file": "research/units/unit-08-applications-integration.md",
   "line": "the amount at t equals the amount at a plus the definite integral of the rate from a to t"
  }
 ],
 "inferred": [
  {
   "claim": "BC-QA-06005 is an either archetype, so the lesson takes Section I Part A and a no calculator example.",
   "settles": "The exam part mix the archetype is served in."
  },
  {
   "claim": "ki-1 is served as motion, the amount traced as the upper time moves.",
   "settles": "The modality A/B in the build plan: skip rate and time to first credited success by mode."
  },
  {
   "claim": "BC-PT-99001 and BC-PT-99004 are earned on ex-1 steps 1 and 3 but not tagged, to hold the brief band under 450 words.",
   "settles": "A brief band cap that admits three reader lines."
  }
 ],
 "sources": [
  "BC-CON-08006",
  "BC-SKL-08012",
  "BC-SKL-08016",
  "BC-SKL-08017",
  "BC-EK-CHA-4D1",
  "BC-EK-CHA-4E1",
  "ced:154",
  "BC-QA-06005",
  "BC-QA-99008",
  "BC-QA-08006",
  "BC-PT-99033",
  "sg-24:3",
  "sg-24:4",
  "sg-23:2",
  "BC-ERR-08011",
  "BC-ERR-08012",
  "BC-ERR-99006",
  "BC-ERR-99005",
  "BC-MIS-08006",
  "BC-MIS-08013",
  "BC-PRQ-06005",
  "BC-PRQ-08006",
  "research/units/unit-08-applications-integration.md#8.3 Using Accumulation Functions and Definite Integrals in Applied Contexts",
  "research/question-analysis/question-archetypes.md#BC-QA-06005 Net change from a rate with an initial condition",
  "research/scoring/common-point-losses.md#Setup points",
  "research/scoring/common-point-losses.md#Units points",
  "research/exam/exam-structure.md#Section and part layout"
 ]
}
```
