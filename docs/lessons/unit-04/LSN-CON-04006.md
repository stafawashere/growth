---
title: LSN-CON-04006 The structure of contextual rate problems
research_date: 2026-09-29
status: designed
purpose: Authoring spec for the concept lesson on BC-CON-04006, the shared structure of rate problems outside motion, built from authoring_bundle("BC-CON-04006") and the research files it cites, so an author fills plan 15's lesson record without making a teaching decision.
---

# LSN-CON-04006 The structure of contextual rate problems

Concept BC-CON-04006 (skills BC-SKL-04013, BC-SKL-04015, BC-SKL-04016), topic 4.3 of Unit 4, loaded by one archetype, BC-QA-04005 (family derivative-in-context). Its hard parent is BC-CON-04002 (docs/lessons/unit-04/README.md, section 1).

## Prediction

Served first in both bands. Multiple choice on ex-1's own model, \(M(t)=20+60(1-e^{-t/8})\): what \(M'(4)\) measures. Three options, key the medicine's rate of change in milligrams per hour, the others a velocity and the amount itself. The resolution states the rate of change of the named quantity in the record's words. Sources: BC-CON-04006 and the topic 4.3 section that ki-1 cites. Delivery: text.

## Orientation

Served text, from BC-CON-04006 `description_plain` and the Assessment behaviour paragraph (research/units/unit-04-contextual-applications-differentiation.md#4.3 Rates of Change in Applied Contexts Other Than Motion), which describes the calculator question on one context asking a rate, its meaning and an end behaviour limit (sg-25:2, sg-25:4). No count, no frequency.

## Key ideas

All three skills map BC-EK-CHA-3C1 (ced:89): one core block, both bands.

- ki-1 (core, BC-EK-CHA-3C1). The Common structure, Units and End behaviour paragraphs of Required mathematical knowledge (ced:84, sg-25:4). Anchor quote from ced:89.

## Recognition

BC-QA-04005 (research/question-analysis/question-archetypes.md#BC-QA-04005 Contextual rate in a setting other than motion): `typical_wording` "write a limit expression that describes the end behaviour of the rate of change and evaluate it", "find the time at which the instantaneous rate of change equals the average rate of change"; `common_givens` a contextual model, the derivative supplied in the stem, rate functions for a quantity other than position, a time interval; `asked_to_produce` the time the rates agree, a limit expression and its value, whether a rate increases with a reason. The signal: a quantity that is not a position, with a formula in t and a calculator part. Shape: a multipart calculator FRQ on one model (BC-FRQ-2019-Q1-D, BC-FRQ-2022-Q1-C).

Not this concept: a particle's position, velocity or acceleration (BC-CON-04003), whose vocabulary is motion.

The contrast pair on st-1 takes its near miss from that sibling: a tank whose long run rate is asked, beside a particle's velocity at an instant. The separating feature is a non-position quantity with a long run rate asked.

## Method choice

One strategy block: BC-QA-04005 is the only archetype loading these skills.

- st-1, BC-QA-04005. Method, `expected_solution_path[0]`: identify the quantity and its independent variable, served without a label. Rival, `wrong_approaches`: substituting infinity in place of a limit expression (BC-ERR-99007). Separating feature: an end behaviour request, answered with the limit written before any value. The archetype carries `asked_to_produce` and `common_givens`, so the block is verified.

## Solution path

- ex-1, BC-QA-04005, both bands, calculator. Draw: context medicine, base 20, amount 60, scale 8, instant 4, trend rising, supplied model. Model 20 + 60(1 - e^(-t/8)) [inferred: the model form], rate 7.5e^(-t/8), rate at 4 about 4.549, inside the spec's invariant 0.5 < |rate| < 20. No published BC-QA-04005 item carries this draw.
- Steps follow `expected_solution_path`: name quantity and input (new), differentiate, the sign of the rate (BC-PT-99014), the limit (limit at oo), the rate restated (new), evaluate at 4 (approx). A fluent solver writes the rate, the limit line and the three decimal value, and holds the naming in the answer sentence.

## Scoring

BC-QA-04005 lists BC-PT-99027, BC-PT-99010 and BC-PT-99014. ex-1 tags BC-PT-99014 on the statement that the rate is positive [inferred: which part earns it]; the line is reader_checks(["BC-PT-99014"]) copied exactly.

For the author: sg-25:4 awards a point for the limit expression and one for its value, and treats arithmetic with infinity as scratch work that cannot earn the value point (research/scoring/notation-requirements.md#Limit notation; research/scoring/common-point-losses.md#Notation points). sg-25:3 scored a response calling an average value an average velocity as unclear communication (BC-ERR-04013).

## Traps

Three active errors meet the skills, in the bundle's order: BC-ERR-04012, BC-ERR-04013, BC-ERR-99007. Low band all three; mid band the first two. All on ex-1's draw. Only BC-ERR-04012 is a fix prompt (relation distinct); the other two share ex-1's value and keep the reveal form.

- err-BC-ERR-04012: 4.549 with nothing named, against the quantity, the input and the units. No possible reason: the linked descriptions do not name the naming step.
- err-BC-ERR-04013: velocity against the amount of medicine; the values agree, so the relation is equivalent. Possible reason from BC-MIS-04007.
- err-BC-ERR-99007: 7.5e^(-oo) computed against the limit written; the values agree, the notation does not. Possible reason from BC-MIS-99008.

## Representations

None. The topic's Representations paragraph names BC-REP-05 to BC-REP-01 and BC-REP-01 to BC-REP-09 (a three decimal value); nothing is figure-shaped.

## Prerequisite bridge

- BC-PRQ-04008, from its `description_plain` and `failure_signature`.

## Time

BC-QA-04005 is `calculator` with a multipart free response structure, so Section II Part A, 15.0 minutes per question (research/exam/exam-structure.md#Section and part layout). The README gives 3.33 minutes for a two point part of this shape (docs/lessons/unit-04/README.md, section 5). The minutes go on the written limit expression and the equation beside the calculator value; the keystrokes are not written.

## Checks

- chk-1, completion of ex-1, both bands: the rate given, the student evaluates. Key 4.549.
- chk-2, isomorph, both bands. Draw: battery, base 20, amount 50, scale 5, instant 3, rising, rate supplied: 10e^(-t/5). Key 5.488.
- chk-3, MCQ, low band. Draw: pollutant, base 30, amount 40, scale 10, instant 5, falling, rate supplied: -4e^(-t/10), about -2.426 at 5. Key A; B carries BC-ERR-04012, C BC-ERR-04013, D BC-ERR-99007. The options share the number and differ in the response, as the spec's notes describe, so the key is a statement with labels.

## Delivery

- orientation, ki-1: text. Rule 5: BC-REP-01, 04, 05 only; the limit is scored as notation retained (sg-25:4), not a process to watch (docs/lessons/unit-04/README.md, section 6).
- ex-1 and the three error blocks: step_reveal. Rule 1.
- No drawn block. No skill carries a figure-bearing BC-REP and the key idea states a notation habit, so the record carries `no_figure_reason`.

## Band plan

- Low (full), served order: prediction, orientation, bridge BC-PRQ-04008 when gated, ki-1, st-1 with its contrast pair, ex-1 with its scoring line, chk-1, err-BC-ERR-04012, err-BC-ERR-04013, err-BC-ERR-99007, chk-2, chk-3. 565 words, 3.8 minutes (cap 900 and 6). This design has one worked example, so nothing is faded.
- Mid (brief): prediction, orientation, bridge when gated, ki-1, st-1 with its contrast pair, ex-1 with its scoring line, chk-1, err-BC-ERR-04012, err-BC-ERR-04013, chk-2. 445 words, 3.0 minutes (cap 450 and 3).
- Refresher: ki-1, the three error blocks, ex-1.

## Sources

- BC-CON-04006; BC-SKL-04013, BC-SKL-04015, BC-SKL-04016; BC-EK-CHA-3C1; ced:89, ced:84
- BC-QA-04005; BC-PT-99014; sg-25:2, sg-25:3, sg-25:4
- Prediction pr-1 and the contrast pair: BC-CON-04006, BC-CON-04003, BC-ERR-99007
- BC-ERR-04012, BC-ERR-04013, BC-ERR-99007; BC-MIS-04007, BC-MIS-99008; BC-PRQ-04008
- research/units/unit-04-contextual-applications-differentiation.md#4.3 Rates of Change in Applied Contexts Other Than Motion
- research/question-analysis/question-archetypes.md#BC-QA-04005 Contextual rate in a setting other than motion
- research/scoring/notation-requirements.md#Limit notation
- research/scoring/common-point-losses.md#Notation points
- research/exam/exam-structure.md#Section and part layout
- [inferred] The model's written form. Settled by an explicit model in the parameter_spec.
- [inferred] BC-PT-99014 on the sign statement. Settled by a rubric instance for a contextual rate part.

## Machine record

```json
{
 "id": "LSN-CON-04006",
 "kind": "concept",
 "target_id": "BC-CON-04006",
 "unit": "04",
 "skills": [
  "BC-SKL-04013",
  "BC-SKL-04015",
  "BC-SKL-04016"
 ],
 "prediction": {
  "id": "pr-1",
  "stem": {
   "text": "Predict. M(t) = 20 + 60(1 - e^(-t/8)) milligrams at t hours. What does M'(4) measure?",
   "command_verb": "predict"
  },
  "format": "mcq",
  "options": [
   {
    "id": "A",
    "label": "The velocity of the medicine.",
    "is_key": false
   },
   {
    "id": "B",
    "label": "The medicine's rate of change, in milligrams per hour.",
    "is_key": true
   },
   {
    "id": "C",
    "label": "The amount of medicine, in milligrams.",
    "is_key": false
   }
  ],
  "resolution": "M'(4) is the medicine's rate of change, in milligrams per hour.",
  "sources": [
   "BC-CON-04006",
   "research/units/unit-04-contextual-applications-differentiation.md#4.3 Rates of Change in Applied Contexts Other Than Motion"
  ]
 },
 "no_figure_reason": "No skill carries a figure-bearing representation (only BC-REP-01, 04, 05 and 09), and the key idea states a notation habit for a limit, not a process the student watches.",
 "orientation": {
  "text": "A contextual rate names its quantity and input, and words its derivative in context units.",
  "sources": [
   "BC-CON-04006",
   "research/units/unit-04-contextual-applications-differentiation.md#4.3 Rates of Change in Applied Contexts Other Than Motion"
  ]
 },
 "key_ideas": [
  {
   "id": "ki-1",
   "ek_id": "BC-EK-CHA-3C1",
   "depth": "core",
   "text": "A non-motion rate keeps the context's words, not a velocity. Units are quantity per input unit. Long run behaviour is a limit, never infinity substituted.",
   "notation": "rate of change of the named quantity",
   "quote": {
    "text": "The derivative can be used to solve problems involving rates of change in applied contexts.",
    "source": "ced:89"
   },
   "sources": [
    "BC-EK-CHA-3C1",
    "ced:89",
    "ced:84",
    "sg-25:4",
    "research/units/unit-04-contextual-applications-differentiation.md#4.3 Rates of Change in Applied Contexts Other Than Motion"
   ]
  }
 ],
 "strategy": [
  {
   "id": "st-1",
   "archetype_id": "BC-QA-04005",
   "cue": "A model or rate over time; rate, meaning or long run value asked.",
   "method": "Name the quantity and input, then the rate.",
   "rival": "Infinity substituted for a limit.",
   "separating_feature": "End behaviour asked: write the limit first.",
   "sources": [
    "BC-QA-04005",
    "BC-ERR-99007",
    "BC-CON-04003"
   ],
   "evidence_tag": "verified",
   "contrast": {
    "this": {
     "text": "V(t) = 50 + 30(1 - e^(-t/5)) liters. Write and evaluate the limit of V'(t) as t grows.",
     "archetype_id": "BC-QA-04005"
    },
    "not_this": {
     "text": "x(t) = t^3 - 6t. Find the velocity at t = 2.",
     "why_not": "Motion vocabulary."
    },
    "feature": "A long run rate of a non-position quantity."
   }
  }
 ],
 "worked_examples": [
  {
   "id": "ex-1",
   "archetype_id": "BC-QA-04005",
   "bands": [
    "low",
    "mid"
   ],
   "parameter_draw": {
    "context": "medicine",
    "base": 20,
    "amount": 60,
    "scale": 8,
    "instant": 4,
    "trend": "rising",
    "supplied": "model"
   },
   "problem": {
    "text": "The medicine in a patient, in milligrams, is \\(M(t)=20+60(1-e^{-t/8})\\) at \\(t\\) hours. Write and evaluate \\(\\lim_{t\\to\\infty}M'(t)\\), and find \\(M'(4)\\).",
    "command_verb": "find"
   },
   "calculator_status": "calculator",
   "steps": [
    {
     "cue": "Medicine in mg; input hours.",
     "why": "Milligrams per hour.",
     "expr": "20 + 60*(1 - exp(-t/8))",
     "relation": "new"
    },
    {
     "cue": "Rate of the model.",
     "why": "\\(M'(t)=7.5e^{-t/8}\\).",
     "expr": "15/2*exp(-t/8)",
     "relation": "differentiate",
     "variable": "t"
    },
    {
     "cue": "\\(M'(t)>0\\).",
     "why": "Increasing.",
     "point_type_id": "BC-PT-99014"
    },
    {
     "cue": "Limit written first.",
     "why": "\\(\\lim_{t\\to\\infty}7.5e^{-t/8}=0\\).",
     "expr": "0",
     "relation": "limit",
     "variable": "t",
     "point": "oo"
    },
    {
     "cue": "Rate at \\(t=4\\).",
     "why": "The rate again.",
     "expr": "15/2*exp(-t/8)",
     "relation": "new"
    },
    {
     "cue": "Calculator.",
     "why": "4.549 milligrams per hour.",
     "expr": "4.549",
     "relation": "evaluate",
     "subs": {
      "t": "4"
     },
     "approx": true
    }
   ],
   "answer": {
    "form": "numeric",
    "expr": "4.549"
   }
  }
 ],
 "what_a_reader_scores": [
  {
   "example_id": "ex-1",
   "point_type_ids": [
    "BC-PT-99014"
   ],
   "lines": [
    {
     "point_type_id": "BC-PT-99014",
     "text": "Considers the sign of a derivative. Earned by: An explicit statement about whether a first or second derivative is positive, negative, or zero on the relevant interval, symbolically or in words (sg-26:12, sg-24:8). Not earned by: A statement about the sign of the function rather than the derivative, or a reference to the concavity of the derivative itself (sg-26:12)."
    }
   ]
  }
 ],
 "common_errors": [
  {
   "error_id": "BC-ERR-04012",
   "wrong_step": {
    "text": "4.549, nothing named.",
    "expr": "4.549"
   },
   "right_step": {
    "text": "Medicine rises at 4.549 milligrams per hour.",
    "expr": "4.549*milligram/hour"
   },
   "relation": "distinct",
   "possible_reason": null,
   "sources": [
    "BC-ERR-04012"
   ],
   "observed_behavior": "The response computes without saying which quantity is modelled or what the input variable measures.",
   "scoring_consequence": "Later interpretation points become unavailable because the answer cannot be tied to the situation; BC-ERR-99033 records variables introduced without being defined.",
   "fix_prompt": true
  },
  {
   "error_id": "BC-ERR-04013",
   "wrong_step": {
    "text": "The velocity is 4.549.",
    "expr": "4.549"
   },
   "right_step": {
    "text": "The amount rises at 4.549 milligrams per hour.",
    "expr": "4.549"
   },
   "relation": "equivalent",
   "possible_reason": {
    "misconception_id": "BC-MIS-04007",
    "text": "maps every rate context onto the vocabulary of a moving particle"
   },
   "sources": [
    "BC-ERR-04013",
    "BC-MIS-04007"
   ],
   "observed_behavior": "The response calls the rate of change of a temperature, a population, or an area a velocity.",
   "scoring_consequence": "The 2025 scoring notes show a response calling an average value an average velocity treated as unclear communication and scored as scratch work, so the points survived in that instance (sg-25:3); the CED nonetheless directs that context vocabulary be used (ced:84).",
   "fix_prompt": false
  },
  {
   "error_id": "BC-ERR-99007",
   "wrong_step": {
    "text": "\\(M'(\\infty)=7.5e^{-\\infty}=0\\).",
    "expr": "15/2*exp(-oo)"
   },
   "right_step": {
    "text": "\\(\\lim_{t\\to\\infty}7.5e^{-t/8}=0\\).",
    "expr": "0"
   },
   "relation": "equivalent",
   "possible_reason": {
    "misconception_id": "BC-MIS-99008",
    "text": "substitutes the infinity symbol for the variable and computes with the result"
   },
   "sources": [
    "BC-ERR-99007",
    "BC-MIS-99008"
   ],
   "observed_behavior": "Responses substitute the infinity symbol for the variable and compute with it, or open an improper integral with limit notation and then abandon it before the evaluation is complete.",
   "scoring_consequence": "The response becomes ineligible for the final point of the part; in improper integral parts the evaluation points are lost.",
   "fix_prompt": false
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
  "exam_part": "II-A",
  "budget_minutes": 15.0,
  "source": "research/exam/exam-structure.md#Section and part layout",
  "written_steps": {
   "ex-1": [
    2,
    3,
    4,
    6
   ]
  },
  "skipped_steps": {
   "ex-1": [
    1,
    5
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
   "archetype_id": "BC-QA-04005",
   "parameter_draw": {
    "context": "medicine",
    "base": 20,
    "amount": 60,
    "scale": 8,
    "instant": 4,
    "trend": "rising",
    "supplied": "model"
   },
   "completes": "ex-1",
   "stem": {
    "text": "\\(M'(t)=7.5e^{-t/8}\\) milligrams per hour. Give \\(M'(4)\\) to three decimals.",
    "command_verb": "give"
   },
   "key": {
    "form": "numeric",
    "expr": "4.549"
   },
   "steps": [
    {
     "text": "Rate.",
     "expr": "15/2*exp(-t/8)",
     "relation": "new"
    },
    {
     "text": "At t = 4.",
     "expr": "4.549",
     "relation": "evaluate",
     "subs": {
      "t": "4"
     },
     "approx": true
    }
   ],
   "calculator_status": "calculator",
   "skills": [
    "BC-SKL-04013"
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
   "archetype_id": "BC-QA-04005",
   "parameter_draw": {
    "context": "battery",
    "base": 20,
    "amount": 50,
    "scale": 5,
    "instant": 3,
    "trend": "rising",
    "supplied": "rate"
   },
   "stem": {
    "text": "A battery's charge rises at \\(B'(t)=10e^{-t/5}\\) percent per minute. Find \\(B'(3)\\).",
    "command_verb": "find"
   },
   "key": {
    "form": "numeric",
    "expr": "5.488"
   },
   "steps": [
    {
     "text": "Rate supplied.",
     "expr": "10*exp(-t/5)",
     "relation": "new"
    },
    {
     "text": "At t = 3.",
     "expr": "5.488",
     "relation": "evaluate",
     "subs": {
      "t": "3"
     },
     "approx": true
    }
   ],
   "calculator_status": "calculator",
   "skills": [
    "BC-SKL-04013"
   ]
  },
  {
   "id": "chk-3",
   "check_kind": "mcq",
   "format": "mcq",
   "bands": [
    "low"
   ],
   "archetype_id": "BC-QA-04005",
   "parameter_draw": {
    "context": "pollutant",
    "base": 30,
    "amount": 40,
    "scale": 10,
    "instant": 5,
    "trend": "falling",
    "supplied": "rate"
   },
   "stem": {
    "text": "A pollutant, \\(P(t)\\) grams at \\(t\\) hours, changes at \\(P'(t)=-4e^{-t/10}\\). Which response is correct?",
    "command_verb": "identify"
   },
   "key": {
    "form": "statement",
    "expr": "-2.426",
    "text": "A"
   },
   "steps": [
    {
     "text": "Rate.",
     "expr": "-4*exp(-t/10)",
     "relation": "new"
    },
    {
     "text": "At t = 5.",
     "expr": "-2.426",
     "relation": "evaluate",
     "subs": {
      "t": "5"
     },
     "approx": true
    }
   ],
   "options": [
    {
     "id": "A",
     "is_key": true,
     "label": "At t = 5 hours the pollutant decreases at 2.426 grams per hour; its limit as t grows is 0.",
     "error_path": null
    },
    {
     "id": "B",
     "is_key": false,
     "label": "P'(5) = -2.426, with no quantity or input named.",
     "error_path": "BC-ERR-04012",
     "derivation": "the value computed without naming the quantity or its input"
    },
    {
     "id": "C",
     "is_key": false,
     "label": "At t = 5 the pollutant's velocity is -2.426.",
     "error_path": "BC-ERR-04013",
     "derivation": "motion vocabulary used for a mass"
    },
    {
     "id": "D",
     "is_key": false,
     "label": "P'(infinity) = -4e^(-infinity) = 0.",
     "error_path": "BC-ERR-99007",
     "derivation": "infinity substituted and limit notation dropped"
    }
   ],
   "calculator_status": "calculator",
   "skills": [
    "BC-SKL-04013",
    "BC-SKL-04015",
    "BC-SKL-04016"
   ]
  }
 ],
 "delivery": [
  {
   "block": "orientation",
   "mode": "text",
   "reason": "rule 5: BC-SKL-04013 and BC-SKL-04015 carry BC-REP-04 and BC-REP-05",
   "sources": [
    "BC-SKL-04013"
   ]
  },
  {
   "block": "ki-1",
   "mode": "text",
   "reason": "rule 5: BC-REP-01, 04, 05; the end behaviour limit is scored as notation retained (sg-25:4), not as a process to watch",
   "sources": [
    "BC-SKL-04016"
   ]
  },
  {
   "block": "ex-1",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  },
  {
   "block": "err-BC-ERR-04012",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  },
  {
   "block": "err-BC-ERR-04013",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  },
  {
   "block": "err-BC-ERR-99007",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  }
 ],
 "refresher": [
  "ki-1",
  "err-BC-ERR-04012",
  "err-BC-ERR-04013",
  "err-BC-ERR-99007",
  "ex-1"
 ],
 "research_lines": [
  {
   "file": "research/scoring/notation-requirements.md",
   "line": "arithmetic with infinity will be considered as scratch work and will not be considered in scoring"
  }
 ],
 "inferred": [
  {
   "claim": "The model is written as base plus amount times (1 minus e to the minus t over scale), rising, and base plus amount times e to the minus t over scale, falling; the parameter_spec notes say only base plus or minus an exponential approach.",
   "settles": "An explicit model expression in the BC-QA-04005 parameter_spec, or a published item on this archetype showing it."
  },
  {
   "claim": "BC-PT-99014 is tagged on the statement that the rate is positive; the archetype lists it without naming which part earns it.",
   "settles": "A rubric instance on BC-PT-99014 for a contextual rate part (sg-25:4 or a later guideline)."
  }
 ],
 "sources": [
  "BC-CON-04006",
  "BC-SKL-04013",
  "BC-SKL-04015",
  "BC-SKL-04016",
  "BC-EK-CHA-3C1",
  "ced:89",
  "ced:84",
  "sg-25:4",
  "sg-25:3",
  "BC-QA-04005",
  "BC-PT-99014",
  "BC-ERR-04012",
  "BC-ERR-04013",
  "BC-ERR-99007",
  "BC-MIS-04007",
  "BC-MIS-99008",
  "BC-PRQ-04008",
  "research/units/unit-04-contextual-applications-differentiation.md#4.3 Rates of Change in Applied Contexts Other Than Motion",
  "research/question-analysis/question-archetypes.md#BC-QA-04005 Contextual rate in a setting other than motion",
  "research/scoring/notation-requirements.md#Limit notation",
  "research/scoring/common-point-losses.md#Notation points",
  "research/exam/exam-structure.md#Section and part layout"
 ],
 "word_count": {
  "full": 565,
  "brief": 445
 },
 "read_minutes": {
  "full": 3.8,
  "brief": 3.0
 }
}
```
