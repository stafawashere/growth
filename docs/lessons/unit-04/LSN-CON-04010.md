---
title: LSN-CON-04010 Interpreting a related rate in context
research_date: 2026-09-29
status: designed
purpose: Authoring spec for the concept lesson on BC-CON-04010, isolating the requested rate and reporting it with units and a sign read in the situation, built from authoring_bundle("BC-CON-04010") and the research files it cites.
---

# LSN-CON-04010 Interpreting a related rate in context

Concept BC-CON-04010 (skills BC-SKL-04024, BC-SKL-04025), topic 4.5, loaded by BC-QA-04006 (primary) and BC-QA-04007. Its hard parent is BC-CON-04009 (docs/lessons/unit-04/README.md, section 1).

## Orientation

Served text, from BC-CON-04010 `description_plain` and the topic's Interpretation paragraph (research/units/unit-04-contextual-applications-differentiation.md#4.5 Solving Related Rates Problems): a response solves the differentiated equation for the requested rate and reports it with the quantity's units over time units, reading a negative sign as a decrease.

## Key ideas

Both skills map to BC-EK-CHA-3E1 (ced:91), one core block.

- ki-1 (core). Paraphrase of "Solving" and "Interpretation": with the instant's values in, one unknown rate remains and is isolated by algebra; the answer carries the quantity's units divided by time units, and its sign says increase or decrease. Anchor quote from ced:91.

## Recognition

BC-QA-04006 (research/question-analysis/question-archetypes.md#BC-QA-04006 Related rates in a geometric setting): `asked_to_produce` "the rate of change of the requested quantity at the stated instant" and "units of the rate"; `difficulty_variables` "whether the answer must be interpreted in words". BC-QA-04007 (research/question-analysis/question-archetypes.md#BC-QA-04007 Related rates on an implicitly defined curve): the rate of the other coordinate. The signal: "find the rate", "give units", "is it increasing or decreasing". Shapes: MCQ for the value; FRQ parts score the value and the units separately (research/scoring/common-point-losses.md#Units points).

Not this concept: a stem asking what the derivative of a named function means at a time, with no relating equation (BC-CON-04001).

## Method choice

- st-1, BC-QA-04006. Method, `expected_solution_path[5]`: solve for the requested rate and report it with units. Rival: the equation left unsolved (BC-ERR-04021). Separating feature: the stem names one rate as the target.
- st-2, BC-QA-04007. Method, `expected_solution_path[3]`: solve for the requested rate. Rival: dy/dx reported in place of dy/dt (BC-ERR-99013, `wrong_approaches`). Separating feature: the stem supplies a rate in time.

## Solution path

- ex-1, BC-QA-04006, both bands, no calculator. Draw: ladder, size 7, rate 4, ratio 1, leg short, centimeter, minute; the template reads the ladder units as meters: a 5 meter ladder, foot 3 meters out, sliding away at 4 meters per minute. Not a published draw.
- Steps: relating equation (new), differentiation (new), instant (evaluate), rate (solve), then the sentence with units and direction (no value). A fluent solver writes all; y = 4 from the 3, 4, 5 triangle is held in the head.

## Scoring

BC-QA-04006 lists BC-PT-99006 (units); ex-1 tags it on the reported rate. Units points are lost for absent units, units of the original quantity on a derived one, or an inverted ratio (research/scoring/common-point-losses.md#Units points). An interpretation that omits the direction loses its point (research/scoring/common-point-losses.md#Interpretation points).

## Traps

Three active errors, in the bundle's order: BC-ERR-04001, BC-ERR-04005, BC-ERR-04021. On ex-1's draw; the mid band shows the first two.

- err-BC-ERR-04001: -3 reported in meters; the same value, so the pair is marked equivalent. Reason words from BC-MIS-04003.
- err-BC-ERR-04005: 3 reported as an increase, against -3. Reason words from BC-MIS-04002.
- err-BC-ERR-04021: the response stops at 24 + 8 dy/dt = 0. No reason line: the linked descriptions do not describe stopping.

## Representations

None. The topic's Representations paragraph names a rate to a sentence (BC-REP-01 to BC-REP-04), which ex-1's last step carries.

## Prerequisite bridge

- BC-PRQ-04004 and BC-PRQ-04007, from `description_plain` and `failure_signature`.

## Time

BC-QA-04006 has `calculator_status` either, so Section I Part A, 2.14 minutes (research/exam/exam-structure.md#Section and part layout) [inferred]. Written: the relation, the differentiated equation, the substitution, the rate with units in one sentence. Held: y from the triangle.

## Checks

- chk-1, completion of ex-1, both bands. Key -3.
- chk-2, isomorph, both bands: sphere, size 5, rate 3, ratio 1, leg short, meter, second; radius 5 meters growing at 3 meters per second. Key 300 pi (cubic meters per second).
- chk-3, MCQ, low band, statement key: ladder, size 9, rate 3, ratio 2, leg long, foot, minute; a 10 foot ladder, foot 8 feet out at 3 feet per minute; dy/dt = -4. Distractors: "increases at 4 feet per minute" (BC-ERR-04005), "-4 feet" (BC-ERR-04001), the unsolved equation (BC-ERR-04021).

## Delivery

- orientation and ki-1: text. Rule 5: BC-SKL-04024 carries BC-REP-01 and BC-REP-09, BC-SKL-04025 BC-REP-04 and BC-REP-05 (docs/lessons/unit-04/README.md, section 6).
- ex-1 and the three error blocks: step_reveal. Rule 1.

## Band plan

- Low (full): orientation, ki-1, st-1, st-2, ex-1 with its scoring line, three error blocks, chk-1 to chk-3, two bridges. 514 words, 3.5 minutes (cap 900 and 6).
- Mid (brief): orientation, ki-1, st-1, ex-1 with its scoring line, err-BC-ERR-04001, err-BC-ERR-04005, chk-1, chk-2, two bridges. 399 words, 2.7 minutes (cap 450 and 3).
- Refresher: ki-1, err-BC-ERR-04001, err-BC-ERR-04005, err-BC-ERR-04021, ex-1.

## Sources

- BC-CON-04010; BC-SKL-04024, BC-SKL-04025; BC-EK-CHA-3E1; ced:91
- BC-QA-04006, BC-QA-04007; BC-PT-99006
- BC-ERR-04001, BC-ERR-04005, BC-ERR-04021; BC-MIS-04002, BC-MIS-04003
- BC-PRQ-04004, BC-PRQ-04007
- research/units/unit-04-contextual-applications-differentiation.md#4.5 Solving Related Rates Problems
- research/question-analysis/question-archetypes.md#BC-QA-04006 Related rates in a geometric setting
- research/question-analysis/question-archetypes.md#BC-QA-04007 Related rates on an implicitly defined curve
- research/scoring/common-point-losses.md#Units points
- research/scoring/common-point-losses.md#Interpretation points
- research/exam/exam-structure.md#Section and part layout
- [inferred] I-A for an either archetype. Settled by a plan 15 budget rule for calculator_status either.

## Machine record

```json
{
 "id": "LSN-CON-04010",
 "kind": "concept",
 "target_id": "BC-CON-04010",
 "unit": "04",
 "skills": [
  "BC-SKL-04024",
  "BC-SKL-04025"
 ],
 "orientation": {
  "text": "Solve the differentiated equation for the requested rate, then report it with the quantity's units over time units, and read a negative sign as the quantity decreasing.",
  "sources": [
   "BC-CON-04010",
   "research/units/unit-04-contextual-applications-differentiation.md#4.5 Solving Related Rates Problems"
  ]
 },
 "key_ideas": [
  {
   "id": "ki-1",
   "ek_id": "BC-EK-CHA-3E1",
   "depth": "core",
   "text": "Once the instant's values are in, one unknown rate is left, isolated by algebra. The answer has units of the quantity divided by units of time, and its sign says whether the quantity grows or shrinks.",
   "notation": "units and sign of the rate",
   "quote": {
    "text": "finding a rate at which one quantity is changing",
    "source": "ced:91"
   },
   "sources": [
    "BC-EK-CHA-3E1",
    "ced:91",
    "research/units/unit-04-contextual-applications-differentiation.md#4.5 Solving Related Rates Problems"
   ]
  }
 ],
 "strategy": [
  {
   "id": "st-1",
   "archetype_id": "BC-QA-04006",
   "cue": "\"Find the rate\" with units asked.",
   "method": "Solve for that rate; state value, units and direction.",
   "rival": "Rival: stopping at the equation (BC-ERR-04021).",
   "separating_feature": "The stem names one target rate.",
   "sources": [
    "BC-QA-04006"
   ],
   "evidence_tag": "verified"
  },
  {
   "id": "st-2",
   "archetype_id": "BC-QA-04007",
   "cue": "One coordinate's rate given on a curve.",
   "method": "Solve the differentiated curve equation for the other rate.",
   "rival": "Rival: dy/dx reported (BC-ERR-99013).",
   "separating_feature": "The given rate is in time.",
   "sources": [
    "BC-QA-04007"
   ],
   "evidence_tag": "verified"
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
    "size": 7,
    "rate": 4,
    "ratio": 1,
    "leg": "short",
    "length_unit": "centimeter",
    "time_unit": "minute"
   },
   "problem": {
    "text": "A 5 meter ladder's foot slides from a wall at 4 meters per minute. When the foot is 3 meters out, how is the top's height changing?",
    "command_verb": "find"
   },
   "calculator_status": "no_calculator",
   "steps": [
    {
     "cue": "Wall, ground, ladder.",
     "why": "Right triangle.",
     "expr": "x**2 + y**2 = 25",
     "relation": "new"
    },
    {
     "cue": "Rates in time asked.",
     "why": "Differentiate in t.",
     "expr": "2*x*dxdt + 2*y*dydt = 0",
     "relation": "new"
    },
    {
     "cue": "The instant: y = 4.",
     "why": "x = 3, dx/dt = 4.",
     "expr": "24 + 8*dydt = 0",
     "relation": "evaluate",
     "subs": {
      "x": "3",
      "y": "4",
      "dxdt": "4"
     }
    },
    {
     "cue": "One unknown rate.",
     "why": "Meters over minutes.",
     "expr": "-3",
     "relation": "solve",
     "variable": "dydt",
     "point_type_id": "BC-PT-99006"
    },
    {
     "cue": "\"How is it changing\" asks direction.",
     "why": "Negative: the height decreases at 3 meters per minute."
    }
   ],
   "answer": {
    "form": "symbolic",
    "expr": "-3"
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
   "observed_behavior": "A correct numerical rate is reported with no units, or with the units of the quantity alone, or with the numerator and denominator units exchanged.",
   "scoring_consequence": "The units point is a separate point in the 2024 and 2025 table based questions and is lost outright (sg-24:2, sg-25:11); BC-ERR-99005 records the same behaviour across years.",
   "wrong_step": {
    "text": "-3 meters.",
    "expr": "-3"
   },
   "right_step": {
    "text": "-3 meters per minute.",
    "expr": "-3"
   },
   "relation": "equivalent",
   "possible_reason": {
    "misconception_id": "BC-MIS-04003",
    "text": "treats the unit as something added at the end"
   },
   "sources": [
    "BC-ERR-04001",
    "BC-MIS-04003"
   ]
  },
  {
   "error_id": "BC-ERR-04005",
   "observed_behavior": "A negative rate is reported as a magnitude or is described as an increase.",
   "scoring_consequence": "The interpretation point is lost; BC-ERR-99030 records the same confusion of direction with quantity.",
   "wrong_step": {
    "text": "Increases at 3.",
    "expr": "3"
   },
   "right_step": {
    "text": "Decreases at 3.",
    "expr": "-3"
   },
   "relation": "distinct",
   "possible_reason": {
    "misconception_id": "BC-MIS-04002",
    "text": "treats its sign as a formatting detail"
   },
   "sources": [
    "BC-ERR-04005",
    "BC-MIS-04002"
   ]
  },
  {
   "error_id": "BC-ERR-04021",
   "observed_behavior": "The differentiated equation is correct and the response stops without solving for the unknown rate.",
   "scoring_consequence": "The final scoring point is lost although the differentiation points may be earned (cr-24:18).",
   "wrong_step": {
    "text": "Stops here.",
    "expr": "24 + 8*dydt = 0"
   },
   "right_step": {
    "text": "Solved.",
    "expr": "-3"
   },
   "relation": "distinct",
   "possible_reason": null,
   "sources": [
    "BC-ERR-04021"
   ]
  }
 ],
 "representations": null,
 "prerequisite_bridges": [
  {
   "prq_id": "BC-PRQ-04004",
   "text": "Compound units such as meters per minute; without them the unit is absent or inverted."
  },
  {
   "prq_id": "BC-PRQ-04007",
   "text": "Isolate one unknown in a linear equation; otherwise the rate is never extracted."
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
   "archetype_id": "BC-QA-04006",
   "parameter_draw": {
    "shape": "ladder",
    "size": 7,
    "rate": 4,
    "ratio": 1,
    "leg": "short",
    "length_unit": "centimeter",
    "time_unit": "minute"
   },
   "completes": "ex-1",
   "stem": {
    "text": "For ex-1, 24 + 8 dy/dt = 0. Find dy/dt with units.",
    "command_verb": "find"
   },
   "key": {
    "form": "symbolic",
    "expr": "-3"
   },
   "steps": [
    {
     "text": "Substituted.",
     "expr": "24 + 8*dydt = 0",
     "relation": "new"
    },
    {
     "text": "Solve; meters per minute.",
     "expr": "-3",
     "relation": "solve",
     "variable": "dydt"
    }
   ],
   "calculator_status": "no_calculator",
   "skills": [
    "BC-SKL-04024"
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
    "shape": "sphere",
    "size": 5,
    "rate": 3,
    "ratio": 1,
    "leg": "short",
    "length_unit": "meter",
    "time_unit": "second"
   },
   "stem": {
    "text": "A sphere's radius grows at 3 meters per second. Find dV/dt, with units, when the radius is 5 meters.",
    "command_verb": "find"
   },
   "key": {
    "form": "symbolic",
    "expr": "300*pi"
   },
   "steps": [
    {
     "text": "dV/dt = 4 pi r^2 dr/dt.",
     "expr": "4*pi*r**2*drdt",
     "relation": "new"
    },
    {
     "text": "r = 5, dr/dt = 3; cubic meters per second.",
     "expr": "300*pi",
     "relation": "evaluate",
     "subs": {
      "r": "5",
      "drdt": "3"
     }
    }
   ],
   "calculator_status": "no_calculator",
   "skills": [
    "BC-SKL-04025"
   ]
  },
  {
   "id": "chk-3",
   "check_kind": "mcq",
   "format": "mcq",
   "bands": [
    "low"
   ],
   "archetype_id": "BC-QA-04006",
   "parameter_draw": {
    "shape": "ladder",
    "size": 9,
    "rate": 3,
    "ratio": 2,
    "leg": "long",
    "length_unit": "foot",
    "time_unit": "minute"
   },
   "stem": {
    "text": "A 10 foot ladder's foot slides out at 3 feet per minute. When it is 8 feet out, which statement answers how the top's height changes?",
    "command_verb": "identify"
   },
   "key": {
    "form": "statement",
    "expr": "dydt = -4",
    "label": "The height decreases at 4 feet per minute."
   },
   "steps": [
    {
     "text": "Differentiated, instant.",
     "expr": "48 + 12*dydt = 0",
     "relation": "new"
    },
    {
     "text": "Solve.",
     "expr": "-4",
     "relation": "solve",
     "variable": "dydt"
    }
   ],
   "options": [
    {
     "id": "A",
     "is_key": true,
     "label": "The height decreases at 4 feet per minute.",
     "error_path": null
    },
    {
     "id": "B",
     "is_key": false,
     "label": "The height increases at 4 feet per minute.",
     "error_path": "BC-ERR-04005",
     "derivation": "the sign dropped"
    },
    {
     "id": "C",
     "is_key": false,
     "label": "The height changes by -4 feet.",
     "error_path": "BC-ERR-04001",
     "derivation": "units of the quantity alone"
    },
    {
     "id": "D",
     "is_key": false,
     "label": "The rate satisfies 48 + 12 dy/dt = 0.",
     "error_path": "BC-ERR-04021",
     "derivation": "stops before isolating dy/dt"
    }
   ],
   "calculator_status": "no_calculator",
   "skills": [
    "BC-SKL-04025"
   ]
  }
 ],
 "delivery": [
  {
   "block": "orientation",
   "mode": "text",
   "reason": "rule 5: BC-SKL-04024 and BC-SKL-04025 carry no figure-bearing representation",
   "sources": [
    "BC-SKL-04024",
    "BC-SKL-04025"
   ]
  },
  {
   "block": "ki-1",
   "mode": "text",
   "reason": "rule 5: a rule for units and sign",
   "sources": [
    "BC-SKL-04025"
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
   "block": "err-BC-ERR-04005",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  },
  {
   "block": "err-BC-ERR-04021",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  }
 ],
 "refresher": [
  "ki-1",
  "err-BC-ERR-04001",
  "err-BC-ERR-04005",
  "err-BC-ERR-04021",
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
   "claim": "BC-QA-04006 has calculator_status either, so the exam part is taken as I-A.",
   "settles": "A plan 15 budget rule for calculator_status either."
  }
 ],
 "sources": [
  "BC-CON-04010",
  "BC-SKL-04024",
  "BC-SKL-04025",
  "BC-EK-CHA-3E1",
  "ced:91",
  "BC-QA-04006",
  "BC-QA-04007",
  "BC-PT-99006",
  "BC-ERR-04001",
  "BC-ERR-04005",
  "BC-ERR-04021",
  "BC-MIS-04002",
  "BC-MIS-04003",
  "BC-PRQ-04004",
  "BC-PRQ-04007",
  "research/units/unit-04-contextual-applications-differentiation.md#4.5 Solving Related Rates Problems",
  "research/question-analysis/question-archetypes.md#BC-QA-04006 Related rates in a geometric setting",
  "research/question-analysis/question-archetypes.md#BC-QA-04007 Related rates on an implicitly defined curve",
  "research/scoring/common-point-losses.md#Units points",
  "research/scoring/common-point-losses.md#Interpretation points",
  "research/exam/exam-structure.md#Section and part layout"
 ],
 "word_count": {
  "full": 514,
  "brief": 399
 },
 "read_minutes": {
  "full": 3.5,
  "brief": 2.7
 }
}
```
