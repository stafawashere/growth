---
title: LSN-CON-06002 Sign and units of accumulated change
research_date: 2026-09-29
status: designed
purpose: Authoring spec for the concept lesson on BC-CON-06002, the sign and the units of an accumulated change, built from authoring_bundle("BC-CON-06002") and the research files it cites.
---

# LSN-CON-06002 Sign and units of accumulated change

Concept BC-CON-06002 (skills BC-SKL-06002, BC-SKL-06003), topic 6.1 of Unit 6, loaded by one archetype, BC-QA-06015 (family accumulation-interpretation). It has no Unit 6 hard parent (docs/lessons/unit-06/README.md, section 1).

## Orientation

Served text, from BC-CON-06002 `description_plain` and the topic's Assessment behaviour paragraph (research/units/unit-06-integration-accumulation.md#6.1 Exploring Accumulations of Change): conceptual variants ask only for the sign or the units, justification variants ask why the accumulation is positive or negative. No count, no frequency.

## Key ideas

Two skills, two BC-EK, both core, both bands.

- ki-1 (core), BC-EK-CHA-4A4 (BC-SKL-06002), ced:118. Paraphrase of the Units paragraph of Required mathematical knowledge. No anchor quote: the CHA-4.A.4 sentence on ced:118 is 27 words, over the 25 word cap.
- ki-2 (core), BC-EK-CHA-4A3 (BC-SKL-06003), ced:118. Paraphrase of the Sign paragraph, with the outflow case added from BC-QA-06015's `difficulty_variables` ("whether the quantity accumulates or depletes"). Anchor quote, 18 words, found on ced:118.

Both carry the concept's notation line.

## Recognition

BC-QA-06015 (research/question-analysis/question-archetypes.md#BC-QA-06015 Interpreting a definite integral in context with units). `typical_wording`: "using correct units, interpret the meaning of the displayed definite integral in the context of the problem". `common_givens`: a contextual rate function, a definite integral expression. `asked_to_produce`: a sentence with quantity, interval, and units. No `official_examples`; the notes name 2023 Q1(a) and 2024 Q1(b). MCQ forms ask for the units of an accumulation or the meaning of an area (topic Assessment behaviour).

The signal: "using correct units" or "per" in the rate's description, and a request to interpret or to say whether the quantity rose or fell. Not this concept: a request for the value of the change (BC-CON-06001 or BC-CON-06012), or a factor 1/(b - a) in front (average value, BC-CON-06013).

## Method choice

- st-1, BC-QA-06015, both bands. Cue from `asked_to_produce` and `common_givens`. Method, `expected_solution_path[0]`: identify what the integrand measures per unit input. Rival from `wrong_approaches`: naming the quantity without the interval; giving the units of the rate rather than of the accumulation. Separating feature: the integral is an amount over an interval. The archetype carries both fields, so the block is not tagged inferred.

## Solution path

- ex-1, BC-QA-06015, both bands, statement answer. Draw from `parameter_spec`: context sand, start 1, length 5, display total, direction depletes (derived finish 6). No published BC-QA-06015 item carries this draw.
- Steps follow `expected_solution_path`: the integrand as a rate (no value); the units product tons/hour times hour (new); tons (equivalent); the sign from the outflow (no value); the interval from the limits (no value). The answer is a sentence.

A fluent solver writes the sentence only and holds the units product and the sign [inferred].

## Scoring

BC-QA-06015 lists no `point_types`, so no what_a_reader_scores entry and no point tag; the served text names no point beyond the error records' scoring_consequence. For the author: the archetype's `scoring_pattern` names one interpretation point needing quantity, units and interval (sg-23:2), and units are scored separately from the value (research/scoring/common-point-losses.md#Units points).

## Traps

Two active errors meet the skills, in the bundle's order: BC-ERR-99034 (linked BC-MIS-08024, severity high), BC-ERR-06029 (BC-MIS-08009, medium). Both bands show both. On ex-1's draw:

- err-BC-ERR-99034: the work shows sand removed, and the pile is reported to grow; the right step reports the change as the negative of the integral. No possible reason line: BC-MIS-08024's description is about area readings, not a sign contradiction.
- err-BC-ERR-06029: tons per hour against tons with the interval. Possible reason, words from BC-MIS-08009.

## Representations

None. The topic's conversions (BC-REP-02 to BC-REP-04, BC-REP-05 to BC-REP-02) are carried by ki-2's figure and ex-1's sentence.

## Prerequisite bridge

- BC-PRQ-06005, from its `description_plain` (a function against its value at a point) and `failure_signature` (f and f prime interchanged).

## Time

BC-QA-06015 is `either`; the design takes Section I Part A, 2.14 minutes per question (research/exam/exam-structure.md#Section and part layout) [inferred]. As a free response part it is one point, a 1.67 minute share of 15.0 (unit README section 5). The minutes go on the sentence: quantity, units, interval, and the sign word.

## Checks

- chk-1, completion of ex-1, both bands: units and outflow given; the student writes the sentence. Key: the ex-1 sentence.
- chk-2, isomorph, both bands. Draw: people, start 8, length 4, total, accumulates. Key: people.
- chk-3, MCQ, low band. Draw: oil, start 0, length 6, total, depletes. Key: gallons drained over 0 ≤ t ≤ 6, the tank's oil fell. Distractors: no interval (BC-ERR-06029), rate units (BC-ERR-06029), the tank's oil rose (BC-ERR-99034).

## Delivery

- orientation: text. Rule 6 (unit README section 6).
- ki-1: text. Rule 6: BC-SKL-06002 carries BC-REP-04 and BC-REP-05 only.
- ki-2: figure. Rule 4: BC-REP-02 on BC-SKL-06003 [inferred; settled by the modality A/B].
- ex-1, err-BC-ERR-99034, err-BC-ERR-06029: step_reveal. Rule 1.

## Band plan

- Low (full): orientation, ki-1, ki-2, st-1, ex-1, both error blocks, chk-1 to chk-3, the bridge. 503 words, 3.4 minutes (cap 900 and 6).
- Mid (brief): orientation, ki-1, ki-2, st-1, ex-1, both error blocks, chk-1, chk-2, the bridge. 437 words, 3.0 minutes (cap 450 and 3).
- Refresher: ki-1, ki-2, err-BC-ERR-99034, err-BC-ERR-06029, ex-1.

## Sources

- BC-CON-06002; BC-SKL-06002, BC-SKL-06003; BC-EK-CHA-4A4, BC-EK-CHA-4A3; ced:118
- BC-QA-06015; sg-23:2, sg-24:3
- BC-ERR-99034, BC-ERR-06029; BC-MIS-08009
- BC-PRQ-06005
- research/units/unit-06-integration-accumulation.md#6.1 Exploring Accumulations of Change
- research/question-analysis/question-archetypes.md#BC-QA-06015 Interpreting a definite integral in context with units
- research/exam/exam-structure.md#Section and part layout
- research/scoring/common-point-losses.md#Interpretation points
- research/scoring/common-point-losses.md#Units points
- [inferred] I-A for an either archetype. Settled by a fixed calculator_status or timing data.
- [inferred] Rate units for the context labels. Settled by a units field in the parameter_spec.
- [inferred] ki-2 as a static figure. Settled by the modality A/B.
- [inferred] Which steps a fluent solver holds. Settled by timing data per step.

## Machine record

```json
{
 "id": "LSN-CON-06002",
 "kind": "concept",
 "target_id": "BC-CON-06002",
 "unit": "06",
 "skills": [
  "BC-SKL-06002",
  "BC-SKL-06003"
 ],
 "orientation": {
  "text": "The rate's sign fixes the sign of the change, and units multiply. A response gives the amount's units and says whether the quantity rose or fell.",
  "sources": [
   "BC-CON-06002",
   "research/units/unit-06-integration-accumulation.md#6.1 Exploring Accumulations of Change"
  ]
 },
 "key_ideas": [
  {
   "id": "ki-1",
   "ek_id": "BC-EK-CHA-4A4",
   "depth": "core",
   "text": "Units of an accumulated change: rate units times input units, so gallons per second times seconds is gallons. An amount, never a rate.",
   "notation": "units of f times units of t",
   "quote": null,
   "sources": [
    "BC-EK-CHA-4A4",
    "ced:118",
    "research/units/unit-06-integration-accumulation.md#6.1 Exploring Accumulations of Change"
   ]
  },
  {
   "id": "ki-2",
   "ek_id": "BC-EK-CHA-4A3",
   "depth": "core",
   "text": "A rate positive on an interval gives a positive change there; a negative rate gives a negative change. A positive outflow rate means the quantity falls.",
   "notation": "units of f times units of t",
   "quote": {
    "text": "If a rate of change is positive (negative) over an interval, then the accumulated change is positive (negative).",
    "source": "ced:118"
   },
   "sources": [
    "BC-EK-CHA-4A3",
    "ced:118",
    "research/units/unit-06-integration-accumulation.md#6.1 Exploring Accumulations of Change"
   ]
  }
 ],
 "strategy": [
  {
   "id": "st-1",
   "archetype_id": "BC-QA-06015",
   "cue": "A contextual rate and a displayed integral; a sentence with quantity, interval and units asked.",
   "method": "Identify what the integrand measures per unit input.",
   "rival": "Rival: the quantity named without the interval, or with the rate's units.",
   "separating_feature": "An amount over an interval: units multiply, and both limits appear.",
   "sources": [
    "BC-QA-06015"
   ],
   "evidence_tag": "verified"
  }
 ],
 "worked_examples": [
  {
   "id": "ex-1",
   "archetype_id": "BC-QA-06015",
   "bands": [
    "low",
    "mid"
   ],
   "parameter_draw": {
    "context": "sand",
    "start": 1,
    "length": 5,
    "display": "total",
    "direction": "depletes"
   },
   "problem": {
    "text": "Sand leaves a pile at R(t) tons per hour, R(t) > 0, t in hours. Interpret ∫_1^6 R(t) dt with units, and give the sign of the pile's change.",
    "command_verb": "interpret"
   },
   "calculator_status": "no_calculator",
   "steps": [
    {
     "cue": "The integrand R is a rate: tons per hour.",
     "why": "The integral accumulates what R measures."
    },
    {
     "cue": "Multiply the units.",
     "why": "Rate units times input units.",
     "expr": "tons/hour*hour",
     "relation": "new"
    },
    {
     "cue": "Hours cancel.",
     "why": "An amount, not a rate.",
     "expr": "tons",
     "relation": "equivalent"
    },
    {
     "cue": "R > 0 and R is an outflow.",
     "why": "The integral is sand removed; the pile's change is its negative."
    },
    {
     "cue": "Limits 1 and 6 name the interval.",
     "why": "Quantity, units and interval together (sg-23:2)."
    }
   ],
   "answer": {
    "form": "statement",
    "expr": "tons",
    "text": "The tons of sand removed from the pile from t = 1 to t = 6 hours; the pile's change is negative."
   }
  }
 ],
 "what_a_reader_scores": [],
 "common_errors": [
  {
   "error_id": "BC-ERR-99034",
   "observed_behavior": "Responses compute a correct intermediate result and then report a final value inconsistent with it, such as changing the sign of a negative sum or carrying forward an earlier incorrect value that contradicts a later correct conclusion, without noticing the conflict.",
   "scoring_consequence": "The answer point is lost although the supporting work would have earned it, and in the extremum case the justification point is lost as well.",
   "wrong_step": {
    "text": "Pile grew by the integral.",
    "expr": "Integral(R(t), (t, 1, 6))"
   },
   "right_step": {
    "text": "Pile changed by its negative.",
    "expr": "-Integral(R(t), (t, 1, 6))"
   },
   "relation": "distinct",
   "possible_reason": null,
   "sources": [
    "BC-ERR-99034"
   ]
  },
  {
   "error_id": "BC-ERR-06029",
   "observed_behavior": "The response names the accumulated quantity but not the interval over which it accumulates, or gives the units of the rate.",
   "scoring_consequence": "The interpretation point requires both the accumulated quantity with units and the interval, so it is not earned (sg-23:2).",
   "wrong_step": {
    "text": "Sand removed, tons per hour.",
    "expr": "tons/hour"
   },
   "right_step": {
    "text": "Tons removed, t = 1 to 6.",
    "expr": "tons"
   },
   "relation": "distinct",
   "possible_reason": {
    "misconception_id": "BC-MIS-08009",
    "text": "treats the sentence as a label for the integral"
   },
   "sources": [
    "BC-ERR-06029",
    "BC-MIS-08009"
   ]
  }
 ],
 "representations": null,
 "prerequisite_bridges": [
  {
   "prq_id": "BC-PRQ-06005",
   "text": "R(t) is a rate at input t, not an amount; swapping f and f prime changes what is measured."
  }
 ],
 "time": {
  "exam_part": "I-A",
  "budget_minutes": 2.14,
  "source": "research/exam/exam-structure.md#Section and part layout",
  "written_steps": {
   "ex-1": [
    5
   ]
  },
  "skipped_steps": {
   "ex-1": [
    1,
    2,
    3,
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
   "archetype_id": "BC-QA-06015",
   "parameter_draw": {
    "context": "sand",
    "start": 1,
    "length": 5,
    "display": "total",
    "direction": "depletes"
   },
   "completes": "ex-1",
   "stem": {
    "text": "∫_1^6 R(t) dt is in tons and R is the outflow rate. Write the interpretation with its sign.",
    "command_verb": "interpret"
   },
   "key": {
    "form": "statement",
    "expr": "tons",
    "text": "The tons of sand removed from the pile from t = 1 to t = 6 hours; the pile's change is negative."
   },
   "calculator_status": "no_calculator",
   "skills": [
    "BC-SKL-06003"
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
   "archetype_id": "BC-QA-06015",
   "parameter_draw": {
    "context": "people",
    "start": 8,
    "length": 4,
    "display": "total",
    "direction": "accumulates"
   },
   "stem": {
    "text": "People enter a museum at E(t) people per hour, t in hours. Give the units of ∫_8^12 E(t) dt.",
    "command_verb": "find"
   },
   "key": {
    "form": "symbolic",
    "expr": "people"
   },
   "steps": [
    {
     "text": "Rate units times input units.",
     "expr": "people/hour*hour",
     "relation": "new"
    },
    {
     "text": "Hours cancel.",
     "expr": "people",
     "relation": "equivalent"
    }
   ],
   "calculator_status": "no_calculator",
   "skills": [
    "BC-SKL-06002"
   ]
  },
  {
   "id": "chk-3",
   "check_kind": "mcq",
   "format": "mcq",
   "bands": [
    "low"
   ],
   "archetype_id": "BC-QA-06015",
   "parameter_draw": {
    "context": "oil",
    "start": 0,
    "length": 6,
    "display": "total",
    "direction": "depletes"
   },
   "stem": {
    "text": "Oil drains from a tank at D(t) gallons per minute, D(t) > 0. Which describes ∫_0^6 D(t) dt?",
    "command_verb": "interpret"
   },
   "key": {
    "form": "statement",
    "expr": "gallons_drained_0_to_6_tank_decreased"
   },
   "options": [
    {
     "id": "A",
     "is_key": true,
     "label": "Gallons drained from t = 0 to t = 6 minutes; the tank's oil fell.",
     "error_path": null
    },
    {
     "id": "B",
     "is_key": false,
     "label": "Gallons of oil drained.",
     "error_path": "BC-ERR-06029",
     "derivation": "the interval omitted"
    },
    {
     "id": "C",
     "is_key": false,
     "label": "Oil drained from t = 0 to t = 6, in gallons per minute.",
     "error_path": "BC-ERR-06029",
     "derivation": "the units of the rate given"
    },
    {
     "id": "D",
     "is_key": false,
     "label": "Gallons drained from t = 0 to t = 6 minutes; the tank's oil rose.",
     "error_path": "BC-ERR-99034",
     "derivation": "a positive integral of an outflow reported as a gain, contradicting the work"
    }
   ],
   "calculator_status": "no_calculator",
   "skills": [
    "BC-SKL-06002",
    "BC-SKL-06003"
   ]
  }
 ],
 "delivery": [
  {
   "block": "orientation",
   "mode": "text",
   "reason": "rule 6: a statement of what a response shows (unit README delivery map)",
   "sources": [
    "BC-CON-06002"
   ]
  },
  {
   "block": "ki-1",
   "mode": "text",
   "reason": "rule 6: BC-SKL-06002 carries BC-REP-04 and BC-REP-05 only; a units product is a rule",
   "sources": [
    "BC-SKL-06002"
   ]
  },
  {
   "block": "ki-2",
   "mode": "figure",
   "reason": "rule 4: BC-REP-02 on BC-SKL-06003; not promoted, since BC-QA-06015's stem asks for a sentence, not a reading of a varying quantity",
   "sources": [
    "BC-SKL-06003"
   ],
   "spec": {
    "kind": "graph",
    "representations": [
     "BC-REP-02"
    ],
    "window": {
     "t": [
      0,
      6
     ],
     "y": [
      -3,
      3
     ]
    },
    "curves": [
     {
      "type": "polyline",
      "points": [
       [
        0,
        2
       ],
       [
        3,
        0
       ],
       [
        6,
        -2
       ]
      ]
     }
    ],
    "shading": [
     {
      "interval": [
       0,
       3
      ],
      "sign": "plus"
     },
     {
      "interval": [
       3,
       6
      ],
      "sign": "minus"
     }
    ],
    "labels": [
     {
      "text": "rate > 0: change > 0",
      "placement": "inside",
      "at": "region on [0, 3]"
     },
     {
      "text": "rate < 0: change < 0",
      "placement": "inside",
      "at": "region on [3, 6]"
     }
    ]
   },
   "fallback": "the same graph, static, with the two signed regions labelled",
   "keyboard": "none needed: the figure has no control"
  },
  {
   "block": "ex-1",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  },
  {
   "block": "err-BC-ERR-99034",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  },
  {
   "block": "err-BC-ERR-06029",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  }
 ],
 "refresher": [
  "ki-1",
  "ki-2",
  "err-BC-ERR-99034",
  "err-BC-ERR-06029",
  "ex-1"
 ],
 "research_lines": [
  {
   "file": "research/units/unit-06-integration-accumulation.md",
   "line": "A rate positive on an interval gives positive accumulated change; a rate negative on an interval gives negative accumulated change (BC-EK-CHA-4A3)."
  },
  {
   "file": "research/scoring/common-point-losses.md",
   "line": "Units are scored separately from the value, and in several years the value was more often correct than the units accompanying it."
  }
 ],
 "inferred": [
  {
   "claim": "BC-QA-06015 is calculator status either, so the time part is I-A at 2.14 minutes.",
   "settles": "A calculator_status of calculator or no_calculator on BC-QA-06015, or timing data by part."
  },
  {
   "claim": "The rate units (tons per hour, people per hour, gallons per minute) are chosen for the context labels; parameter_spec names no units.",
   "settles": "A units field in BC-QA-06015's parameter_spec."
  },
  {
   "claim": "ki-2 is served as a static figure.",
   "settles": "The modality A/B in the build plan: skip rate and time to first credited success by mode."
  },
  {
   "claim": "A fluent solver writes only the sentence and holds the units product and the sign.",
   "settles": "Timing data per step once the fluency telemetry exists."
  }
 ],
 "sources": [
  "BC-CON-06002",
  "BC-SKL-06002",
  "BC-SKL-06003",
  "BC-EK-CHA-4A4",
  "BC-EK-CHA-4A3",
  "ced:118",
  "BC-QA-06015",
  "sg-23:2",
  "sg-24:3",
  "BC-ERR-99034",
  "BC-ERR-06029",
  "BC-MIS-08009",
  "BC-PRQ-06005",
  "research/units/unit-06-integration-accumulation.md#6.1 Exploring Accumulations of Change",
  "research/question-analysis/question-archetypes.md#BC-QA-06015 Interpreting a definite integral in context with units",
  "research/exam/exam-structure.md#Section and part layout",
  "research/scoring/common-point-losses.md#Interpretation points",
  "research/scoring/common-point-losses.md#Units points"
 ],
 "read_minutes": {
  "full": 3.4,
  "brief": 3.0
 },
 "word_count": {
  "full": 503,
  "brief": 437
 }
}
```
