---
title: LSN-CON-04002 Units of a derivative
research_date: 2026-09-29
status: designed
purpose: Authoring spec for the concept lesson on BC-CON-04002, the units of a derivative and the table approximation that carries them, built from authoring_bundle("BC-CON-04002") and the research files it cites, so an author fills plan 15's lesson record without making a teaching decision.
---

# LSN-CON-04002 Units of a derivative

Concept BC-CON-04002 (skills BC-SKL-04001, BC-SKL-04004, BC-SKL-04014), topics 4.1 and 4.3 of Unit 4, loaded by BC-QA-04001, BC-QA-04002 and BC-QA-04005. It is first in the unit's skill order because BC-SKL-04001 is the root of the 4.1 to 4.3 chain (docs/lessons/unit-04/README.md, section 1).

## Orientation

Served text, from BC-CON-04002 `description_plain` and the Assessment behaviour paragraph (research/units/unit-04-contextual-applications-differentiation.md#4.1 Interpreting the Meaning of the Derivative in Context). It states the units rule as what a response writes, and the table form of the approximation, whose estimate and units are scored as two points (sg-24:2, sg-25:11). No count, no frequency.

## Key ideas

The three skills map three BC-EK: BC-SKL-04001 to BC-EK-CHA-3A3, BC-SKL-04004 to BC-EK-CHA-3A1, BC-SKL-04014 to BC-EK-CHA-3C1. Two core blocks (ki-1, ki-3), one extended.

- ki-1 (core, BC-EK-CHA-3A3, ced:87). Paraphrase of the Units paragraph of Required mathematical knowledge: function unit over input unit, the second derivative over the input unit squared (sg-25:11). No anchor quote, to hold the brief band under its cap.
- ki-2 (extended, BC-EK-CHA-3A1, ced:87). The Approximation paragraph: the average rate over an interval containing the input approximates the derivative, written as a difference over a difference (sg-25:11). Anchor quote from ced:87.
- ki-3 (core, BC-EK-CHA-3C1, ced:89). Core so that the mid band teaches BC-SKL-04014 (differentiate the model, evaluate it, and attach the right units), which no other mid block holds (plan 15, Sourcing, Pipeline step 2). From the 4.3 Units paragraph and its model to rate expression conversion (research/units/unit-04-contextual-applications-differentiation.md#4.3 Rates of Change in Applied Contexts Other Than Motion): the rate is the model's derivative at the named instant, in the quantity's unit over the input's unit, in the context's words. No anchor quote and no notation line, to hold the brief band under its cap.

## Recognition

- BC-QA-04002 (research/question-analysis/question-archetypes.md#BC-QA-04002 Approximating a derivative from a table with units): `typical_wording` "approximate the derivative at the stated input using the average rate of change over the named interval; show the work and indicate units of measure"; `common_givens` a table of values of a contextual quantity, the interval; `asked_to_produce` the approximation, supporting work of a difference and a quotient, units. The signal: a table plus the words indicate units. FRQ shape: the opening part of a table based question (BC-FRQ-2021-Q1-A, BC-FRQ-2024-Q1-A, BC-FRQ-2025-Q3-A, BC-FRQ-2026-Q1-A, BC-FRQ-2022-Q4-A).
- BC-QA-04001 (research/question-analysis/question-archetypes.md#BC-QA-04001 Interpreting the value of a derivative in context with units): "using correct units, interpret the meaning of the stated value in the context of the problem"; givens name the units of the quantity and of the input. MCQ shape: which unit, or which sentence (BC-MCQ-SAMPLE-013).
- BC-QA-04005 (research/question-analysis/question-archetypes.md#BC-QA-04005 Contextual rate in a setting other than motion), same family as BC-QA-04001: a calculator model whose rate is reported with units (BC-SKL-04014).

Not this concept: a stem asking for the amount of the quantity at an instant (a function value, BC-SKL-04003), or for a rate of a different named quantity.

## Method choice

Two strategy blocks, one per archetype family (derivative-from-table, derivative-in-context); st-1 serves both bands, st-2 the low band.

- st-1, BC-QA-04002. Method, `expected_solution_path[0]`: select the two tabulated values the named interval determines. Rival from `wrong_approaches`: the difference never divided (BC-ERR-02001) or a wrong pair of rows (BC-ERR-02004). Separating feature: the named interval.
- st-2, BC-QA-04001. Method: name the quantity and the instant. Rival: the value read as an amount (BC-ERR-04003). Separating feature: a derivative value is a rate, so its unit is a quotient.

Both archetypes carry `asked_to_produce` and `common_givens` in the snapshot, so neither block is tagged inferred.

## Solution path

- ex-1, BC-QA-04002, both bands, no calculator. Draw from `parameter_spec`: times [0, 2, 4, 6, 10], readings [20, 31, 40, 55, 70], context oven, trend increasing. The named interval runs from the second to the fourth row: key (55 - 31)/(6 - 2) = 6; the one-sided rates 9/2 and 15/2 and the bare change 24 are distinct, as the spec's constraint requires. No published BC-QA-04002 item carries this draw.
- Steps follow `expected_solution_path`: choose the rows (no value), difference over difference (new), divide (equivalent), attach the units (no value, tagged BC-PT-99006). A fluent solver writes steps 2 to 4 and holds the row choice in the head.

## Scoring

BC-QA-04002 lists BC-PT-99005, BC-PT-99008 and BC-PT-99006. ex-1 tags BC-PT-99006 on the units step, the point this concept owns; its what_a_reader_scores line is reader_checks(["BC-PT-99006"]) copied exactly. The estimate with its setup (BC-PT-99005) belongs to the approximation, served in chk-1.

Point losses for the author: absent units, the original quantity's units on a derived quantity, and an inverted ratio (BC-ERR-99005, cr-24:4; research/scoring/common-point-losses.md#Units points). The units point is earned whether or not the units are attached to a number (sg-25:11, sg-24:2).

## Traps

Two active errors meet the skills, in the bundle's order: BC-ERR-04001, BC-ERR-04004 (both linked to BC-MIS-04003, severity high). Both bands show both, on ex-1's draw.

- err-BC-ERR-04001: 6 minutes per degree Celsius against 6 degrees Celsius per minute. Possible reason in words from BC-MIS-04003.
- err-BC-ERR-04004: the bare value 6 against the quotient that shows the difference; the two are equal as values, so the relation is equivalent and the loss is the missing setup (sg-25:11).

## Representations

None as a separate block. The topic's Representations paragraph names BC-REP-03 to BC-REP-04, a tabulated quantity to a rate with units; ki-2's table carries it.

## Prerequisite bridge

- BC-PRQ-04004, from its `description_plain` and `failure_signature`.

## Time

BC-QA-04002 has calculator status either, so the lesson takes Section I Part A, 2.14 minutes per question (research/exam/exam-structure.md#Section and part layout) [inferred: the either status]. As an FRQ part it is the opening part of a Section II question, 15.0 minutes in all, with 3.33 minutes for its two points (docs/lessons/unit-04/README.md, section 5). The minutes go on the written quotient and the units; the row choice is read off the stem.

## Checks

- chk-1, completion of ex-1, both bands: the setup is given, the student gives 6 with degrees Celsius per minute.
- chk-2, isomorph, both bands. Draw: times [1, 3, 5, 7, 9], readings [12, 20, 33, 50, 60], context download, increasing. Key 15/2, megabytes per second.
- No chk-3: the bundle lists two errors, and an MCQ check 3 needs three error paths (inferred array).

## Delivery

- orientation: text. Rule 5.
- ki-1: text. Rule 5, the units rule (docs/lessons/unit-04/README.md, section 6).
- ki-2: table. Rule 4: BC-REP-03 in BC-SKL-04004 and in BC-QA-04002 `common_givens` [inferred; settled by the modality A/B]. Fallback: the table as text rows. Keyboard: Tab between cells.
- ki-3: text. Rule 5.
- ex-1, err-BC-ERR-04001, err-BC-ERR-04004: step_reveal. Rule 1.

## Band plan

- Low (full): orientation, ki-1, ki-2, ki-3, st-1, st-2, ex-1 with its scoring line, both error blocks, chk-1, chk-2, the bridge. 569 words, 4.2 minutes (cap 900 and 6).
- Mid (brief): orientation, ki-1, ki-3, st-1, ex-1 with its scoring line, both error blocks, chk-1, chk-2, the bridge. 449 words, 3.0 minutes (cap 450 and 3).
- Refresher: ki-1, ki-3, err-BC-ERR-04001, err-BC-ERR-04004, ex-1.

## Sources

- BC-CON-04002; BC-SKL-04001, BC-SKL-04004, BC-SKL-04014; BC-EK-CHA-3A3, BC-EK-CHA-3A1, BC-EK-CHA-3C1; ced:87, ced:89
- BC-QA-04002, BC-QA-04001, BC-QA-04005; BC-PT-99006; sg-25:11, sg-24:2, cr-24:4
- BC-ERR-04001, BC-ERR-04004; BC-MIS-04003; BC-PRQ-04004
- research/units/unit-04-contextual-applications-differentiation.md#4.1 Interpreting the Meaning of the Derivative in Context
- research/units/unit-04-contextual-applications-differentiation.md#4.3 Rates of Change in Applied Contexts Other Than Motion
- research/question-analysis/question-archetypes.md#BC-QA-04002 Approximating a derivative from a table with units
- research/question-analysis/question-archetypes.md#BC-QA-04001 Interpreting the value of a derivative in context with units
- research/question-analysis/question-archetypes.md#BC-QA-04005 Contextual rate in a setting other than motion
- research/scoring/common-point-losses.md#Units points
- research/exam/exam-structure.md#Section and part layout
- [inferred] The exam part for an either archetype. Settled by a calculator status on BC-QA-04002.
- [inferred] Two checks only. Settled by a third error linked to the concept's skills.
- [inferred] ki-2 as a table. Settled by the modality A/B.

## Machine record

```json
{
 "id": "LSN-CON-04002",
 "kind": "concept",
 "target_id": "BC-CON-04002",
 "unit": "04",
 "skills": [
  "BC-SKL-04001",
  "BC-SKL-04004",
  "BC-SKL-04014"
 ],
 "orientation": {
  "text": "A response shows a difference of values over a difference of inputs, the value, then its units, the function's unit over the input's unit.",
  "sources": [
   "BC-CON-04002",
   "research/units/unit-04-contextual-applications-differentiation.md#4.1 Interpreting the Meaning of the Derivative in Context"
  ]
 },
 "key_ideas": [
  {
   "id": "ki-1",
   "ek_id": "BC-EK-CHA-3A3",
   "depth": "core",
   "text": "A derivative's unit is the function's unit over the input's unit, as in degrees Celsius per minute. A second derivative divides by the input's unit twice (sg-25:11). Units carry their own point.",
   "notation": "units of f per unit of x",
   "quote": null,
   "sources": [
    "BC-EK-CHA-3A3",
    "ced:87",
    "sg-25:11",
    "research/units/unit-04-contextual-applications-differentiation.md#4.1 Interpreting the Meaning of the Derivative in Context"
   ]
  },
  {
   "id": "ki-2",
   "ek_id": "BC-EK-CHA-3A1",
   "depth": "extended",
   "text": "The derivative at an input is the instantaneous rate of change there. From a table, the average rate of change over an interval containing the input approximates it, written as a difference of values divided by a difference of inputs (sg-25:11).",
   "notation": "f prime of a",
   "quote": {
    "text": "The derivative of a function can be interpreted as the instantaneous rate of change with respect to its independent variable.",
    "source": "ced:87"
   },
   "sources": [
    "BC-EK-CHA-3A1",
    "ced:87",
    "sg-25:11",
    "research/units/unit-04-contextual-applications-differentiation.md#4.1 Interpreting the Meaning of the Derivative in Context"
   ]
  },
  {
   "id": "ki-3",
   "ek_id": "BC-EK-CHA-3C1",
   "depth": "core",
   "text": "A model's rate is its derivative at the named instant. For \\(V(t)\\) liters at \\(t\\) hours, \\(V'(2)\\) is in liters per hour, in the context's words.",
   "notation": "",
   "quote": null,
   "sources": [
    "BC-EK-CHA-3C1",
    "ced:89",
    "research/units/unit-04-contextual-applications-differentiation.md#4.3 Rates of Change in Applied Contexts Other Than Motion"
   ]
  }
 ],
 "strategy": [
  {
   "id": "st-1",
   "archetype_id": "BC-QA-04002",
   "cue": "A table, a named interval, and the words approximate the derivative, show the work, indicate units.",
   "method": "First line: the difference of the two named rows over the difference of their inputs.",
   "rival": "The difference never divided (BC-ERR-02001), or a one-sided pair of rows (BC-ERR-02004).",
   "separating_feature": "The named interval fixes both rows, which bracket the input.",
   "sources": [
    "BC-QA-04002"
   ],
   "evidence_tag": "verified"
  },
  {
   "id": "st-2",
   "archetype_id": "BC-QA-04001",
   "cue": "A value of a derivative is given, and the stem says using correct units, interpret it in context.",
   "method": "First line: name the quantity and the instant, then the direction and the units.",
   "rival": "Rival: reading the value as an amount of the quantity (BC-ERR-04003).",
   "separating_feature": "A derivative value is a rate, so its unit has a per.",
   "sources": [
    "BC-QA-04001"
   ],
   "evidence_tag": "verified"
  }
 ],
 "worked_examples": [
  {
   "id": "ex-1",
   "archetype_id": "BC-QA-04002",
   "bands": [
    "low",
    "mid"
   ],
   "parameter_draw": {
    "times": [
     0,
     2,
     4,
     6,
     10
    ],
    "readings": [
     20,
     31,
     40,
     55,
     70
    ],
    "context": "oven",
    "trend": "increasing"
   },
   "problem": {
    "text": "An oven's temperature \\(T(t)\\), degrees Celsius, is tabulated at \\(t=0,2,4,6,10\\) minutes: 20, 31, 40, 55, 70. Approximate \\(T'(4)\\) using the average rate of change over \\([2,6]\\). Indicate units.",
    "command_verb": "approximate"
   },
   "calculator_status": "no_calculator",
   "steps": [
    {
     "cue": "The interval \\([2,6]\\) names the rows \\(t=2\\) and \\(t=6\\).",
     "why": "They bracket \\(t=4\\)."
    },
    {
     "cue": "Average rate: difference over difference.",
     "why": "The setup shows table values.",
     "expr": "(55 - 31)/(6 - 2)",
     "relation": "new"
    },
    {
     "cue": "Divide.",
     "why": "The value beside its setup.",
     "expr": "6",
     "relation": "equivalent"
    },
    {
     "cue": "\\(T\\) in degrees Celsius, \\(t\\) in minutes.",
     "why": "Units: degrees Celsius per minute.",
     "point_type_id": "BC-PT-99006"
    }
   ],
   "answer": {
    "form": "numeric",
    "expr": "6"
   }
  }
 ],
 "what_a_reader_scores": [
  {
   "example_id": "ex-1",
   "point_type_ids": [
    "BC-PT-99006"
   ],
   "lines": [
    {
     "point_type_id": "BC-PT-99006",
     "text": "Units. Earned by: Correct units, whether or not they are attached to a numerical value (sg-25:11, sg-26:2); equivalent compact forms such as birds per day squared are accepted (sg-26:2). Not earned by: Units with no value present at all where the rubric ties them to a presented value (sg-22:13). Units are required on the answer."
    }
   ]
  }
 ],
 "common_errors": [
  {
   "error_id": "BC-ERR-04001",
   "wrong_step": {
    "text": "6 minutes per degree Celsius.",
    "expr": "6*minute/celsius"
   },
   "right_step": {
    "text": "6 degrees Celsius per minute.",
    "expr": "6*celsius/minute"
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
   "scoring_consequence": "The units point is a separate point in the 2024 and 2025 table based questions and is lost outright (sg-24:2, sg-25:11); BC-ERR-99005 records the same behaviour across years."
  },
  {
   "error_id": "BC-ERR-04004",
   "wrong_step": {
    "text": "6, with no difference shown.",
    "expr": "6"
   },
   "right_step": {
    "text": "\\((55-31)/(6-2)=6\\).",
    "expr": "(55 - 31)/(6 - 2)"
   },
   "relation": "equivalent",
   "possible_reason": null,
   "sources": [
    "BC-ERR-04004"
   ],
   "observed_behavior": "The approximation is written as a single quotient or as a bare number with no visible difference of tabulated values.",
   "scoring_consequence": "The 2025 rubric states that the setup expression by itself is not sufficient for the point, which requires the answer together with a difference and a quotient using values from the table (sg-25:11)."
  }
 ],
 "representations": null,
 "prerequisite_bridges": [
  {
   "prq_id": "BC-PRQ-04004",
   "text": "A compound unit is a quotient, such as degrees Celsius per minute, attached to the value. The failure: a correct number with the unit missing or upside down."
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
   "archetype_id": "BC-QA-04002",
   "parameter_draw": {
    "times": [
     0,
     2,
     4,
     6,
     10
    ],
    "readings": [
     20,
     31,
     40,
     55,
     70
    ],
    "context": "oven",
    "trend": "increasing"
   },
   "completes": "ex-1",
   "stem": {
    "text": "The setup is \\((55-31)/(6-2)\\). Give \\(T'(4)\\) with its units.",
    "command_verb": "give"
   },
   "key": {
    "form": "numeric",
    "expr": "6"
   },
   "steps": [
    {
     "text": "Setup.",
     "expr": "(55 - 31)/(6 - 2)",
     "relation": "new"
    },
    {
     "text": "Value, in degrees Celsius per minute.",
     "expr": "6",
     "relation": "equivalent"
    }
   ],
   "calculator_status": "no_calculator",
   "skills": [
    "BC-SKL-04004",
    "BC-SKL-04001"
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
   "archetype_id": "BC-QA-04002",
   "parameter_draw": {
    "times": [
     1,
     3,
     5,
     7,
     9
    ],
    "readings": [
     12,
     20,
     33,
     50,
     60
    ],
    "context": "download",
    "trend": "increasing"
   },
   "stem": {
    "text": "Megabytes downloaded \\(D(t)\\) at \\(t=1,3,5,7,9\\) seconds: 12, 20, 33, 50, 60. Approximate \\(D'(5)\\) over \\([3,7]\\), with units.",
    "command_verb": "approximate"
   },
   "key": {
    "form": "numeric",
    "expr": "15/2"
   },
   "steps": [
    {
     "text": "Rows \\(t=3\\) and \\(t=7\\).",
     "expr": "(50 - 20)/(7 - 3)",
     "relation": "new"
    },
    {
     "text": "7.5 megabytes per second.",
     "expr": "15/2",
     "relation": "equivalent"
    }
   ],
   "calculator_status": "no_calculator",
   "skills": [
    "BC-SKL-04004",
    "BC-SKL-04001"
   ]
  }
 ],
 "delivery": [
  {
   "block": "orientation",
   "mode": "text",
   "reason": "rule 5: a statement of what a response shows, BC-REP-04 and BC-REP-05 on BC-SKL-04001",
   "sources": [
    "BC-SKL-04001"
   ]
  },
  {
   "block": "ki-1",
   "mode": "text",
   "reason": "rule 5: CHA-3A3 is a rule about units with BC-REP-04 and BC-REP-05 givens",
   "sources": [
    "BC-SKL-04001"
   ]
  },
  {
   "block": "ki-2",
   "mode": "table",
   "reason": "rule 4: BC-REP-03 in BC-SKL-04004 representations and BC-QA-04002 common_givens, a table of values of a contextual quantity",
   "sources": [
    "BC-SKL-04004",
    "BC-QA-04002"
   ],
   "spec": {
    "kind": "table",
    "columns": [
     "t (minutes)",
     "0",
     "2",
     "4",
     "6",
     "10"
    ],
    "rows": [
     [
      "T(t) (degrees Celsius)",
      "20",
      "31",
      "40",
      "55",
      "70"
     ]
    ],
    "labels": [
     {
      "text": "interval [2, 6] brackets t = 4",
      "placement": "inside"
     },
     {
      "text": "(55 - 31)/(6 - 2) degrees Celsius per minute",
      "placement": "inside"
     }
    ],
    "representations": [
     "BC-REP-03"
    ]
   },
   "fallback": "the table as plain text rows with the bracketing pair and the quotient named",
   "keyboard": "Tab moves between cells; no control"
  },
  {
   "block": "ki-3",
   "mode": "text",
   "reason": "rule 5: CHA-3C1 on BC-SKL-04014 carries BC-REP-01, BC-REP-05 and BC-REP-09, none figure-bearing",
   "sources": [
    "BC-SKL-04014"
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
   "block": "err-BC-ERR-04004",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  }
 ],
 "refresher": [
  "ki-1",
  "ki-3",
  "err-BC-ERR-04001",
  "err-BC-ERR-04004",
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
   "claim": "BC-QA-04002 is calculator status either, so the lesson times it as Section I Part A at 2.14 minutes.",
   "settles": "A calculator status of calculator or no_calculator on BC-QA-04002, or a scored MCQ record for it."
  },
  {
   "claim": "The lesson carries 2 checks: the bundle lists two errors, fewer than the three distractors an MCQ check 3 needs.",
   "settles": "A third active BC-ERR linked to BC-SKL-04001, BC-SKL-04004 or BC-SKL-04014."
  },
  {
   "claim": "ki-2 is served as a rendered table rather than text.",
   "settles": "The modality A/B in the build plan: skip rate and time to first credited success by mode."
  }
 ],
 "sources": [
  "BC-CON-04002",
  "BC-SKL-04001",
  "BC-SKL-04004",
  "BC-SKL-04014",
  "BC-EK-CHA-3A3",
  "BC-EK-CHA-3A1",
  "BC-EK-CHA-3C1",
  "ced:87",
  "ced:89",
  "sg-25:11",
  "sg-24:2",
  "BC-QA-04002",
  "BC-QA-04001",
  "BC-QA-04005",
  "BC-PT-99006",
  "BC-ERR-04001",
  "BC-ERR-04004",
  "BC-MIS-04003",
  "BC-PRQ-04004",
  "research/units/unit-04-contextual-applications-differentiation.md#4.1 Interpreting the Meaning of the Derivative in Context",
  "research/units/unit-04-contextual-applications-differentiation.md#4.3 Rates of Change in Applied Contexts Other Than Motion",
  "research/question-analysis/question-archetypes.md#BC-QA-04002 Approximating a derivative from a table with units",
  "research/question-analysis/question-archetypes.md#BC-QA-04001 Interpreting the value of a derivative in context with units",
  "research/scoring/common-point-losses.md#Units points",
  "research/exam/exam-structure.md#Section and part layout"
 ],
 "word_count": {
  "full": 569,
  "brief": 449
 },
 "read_minutes": {
  "full": 4.2,
  "brief": 3.0
 }
}
```
