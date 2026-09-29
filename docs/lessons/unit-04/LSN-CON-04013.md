---
title: LSN-CON-04013 Indeterminate form
research_date: 2026-09-29
status: designed
purpose: Authoring spec for the concept lesson on BC-CON-04013, recognising zero over zero and infinity over infinity as labels for an unsettled limit shown by two separate limits, built from authoring_bundle("BC-CON-04013") and the research files it cites.
---

# LSN-CON-04013 Indeterminate form

Concept BC-CON-04013 (skill BC-SKL-04033), topic 4.7, loaded by BC-QA-04009 (family lhospital-limit). No hard parent in the unit; BC-CON-04014 supports it (docs/lessons/unit-04/README.md, section 1).

## Prediction

One question on ex-1's own numbers, both bands, served first: Predict before the rule: f(3) = 2, so f(3x) - 2 and x - 1 both tend to 0 as x tends to 1. What does that say about the limit of their ratio? Form: `mcq` with three options (A, The limit is 0, because the numerator tends to 0; B, The limit is not settled yet, and more work is needed (the key); C, The limit does not exist, because the denominator tends to 0). Resolution shown on the key idea screen: Two parts that both tend to 0 leave the ratio's limit unsettled: the form is indeterminate. Here the ratio's limit is -12, a value neither part's limit shows on its own. Sources: the concept record and the topic section the key idea cites.

## Orientation

Served text, from BC-CON-04013 `description_plain` and the topic's Assessment behaviour paragraph (research/units/unit-04-contextual-applications-differentiation.md#4.7 Using L'Hospital's Rule for Determining Limits of Indeterminate Forms): a response computes the limit of the numerator and of the denominator as two separate statements, and names the form in words; neither 0/0 nor the numerator's limit is the answer.

## Key ideas

BC-SKL-04033 maps to BC-EK-LIM-4A1 (ced:93), one core block.

- ki-1 (core). Paraphrase of "Indeterminate form" and "The hypothesis": a ratio whose parts both tend to 0, or both to infinity, is indeterminate; the form is shown by two separate limits and is never written as the quotient's value (ced:84, sg-23:14). Anchor quote from ced:93.

## Recognition

BC-QA-04009 (research/question-analysis/question-archetypes.md#BC-QA-04009 Limit of an indeterminate form with L'Hospital's rule): `typical_wording` "find the value of the stated limit, or show that it does not exist, and justify the answer"; `common_givens` a quotient with a function known through values and derivatives; `asked_to_produce` "separate limits of the numerator and denominator". The signal: substituting the limit point sends both parts to zero. Shapes: MCQ (BC-MCQ-SAMPLE-001) and one part of a graphical analysis FRQ (BC-FRQ-2023-Q4-C, BC-FRQ-2021-Q4-C).

Not this concept: a quotient whose denominator tends to a nonzero number; direct substitution settles it.

The near miss comes from a quotient whose denominator tends to a nonzero number, where direct substitution settles the limit and no form is named. That stem is the `not_this` of the contrast pair on st-1.

## Method choice

- st-1, BC-QA-04009. Method, `expected_solution_path[0]` to [2]: the numerator's limit, the denominator's limit, the form stated. Rival from `wrong_approaches`: reporting zero because the numerator tends to zero (BC-ERR-01008). Separating feature: the denominator's own limit.

## Solution path

- ex-1, BC-QA-04009, both bands, no calculator. Draw: anchor 1, stretch 3, far_value 2, far_slope -4, near_value 5, near_slope 1, denominator linear; the limit of (f(3x) - 2)/(x - 1) as x tends to 1, with f(3) = 2 and f'(3) = -4. Not a published draw.
- Steps: numerator limit by continuity (new, equivalent); denominator limit (new, limit); the form in words (no value); the ratio of derivatives (new). A fluent solver writes every line: each carries a point (sg-23:14).
- Model inside the reveal: numerator, denominator and ratio at x = 1.1, 1.01, 1.001, with the numerator taken from f's tangent line at 3 [inferred].

## Scoring

BC-QA-04009 lists BC-PT-99055; ex-1 tags it on the separate limits. The 2023 rubric withholds the first point from a limit written explicitly equal to 0/0 (sg-23:14, research/scoring/notation-requirements.md#Limit notation). Unverified hypotheses of the rule lose the condition point (research/scoring/common-point-losses.md#Justification points).

## Traps

Three active errors in the bundle's order: BC-ERR-01008, BC-ERR-04028, BC-ERR-04029. On ex-1's draw; mid band the first two.

- err-BC-ERR-01008: 0 reported, against -12. Reason words from BC-MIS-01006.
- err-BC-ERR-04028: the quotient written equal to 0/0, against two limits each 0. Reason words from BC-MIS-04014.
- err-BC-ERR-04029: -12 reached with no form stated; same value, marked equivalent. Reason words from BC-MIS-04015.

## Representations

None as a separate block; ki-1's motion carries the limit being taken.

## Prerequisite bridge

- BC-PRQ-04008, from `description_plain` and `failure_signature`.

## Time

BC-QA-04009 is `no_calculator` and one part of a graphical analysis FRQ, so Section II Part B, 15.0 minutes per question (research/exam/exam-structure.md#Section and part layout); the part is scored as three points (sg-23:14). Written: two limits, the form, the derivative ratio, the value. Nothing is skipped.

## Checks

- chk-1, completion of ex-1, both bands. Key -12.
- chk-2, isomorph, both bands: anchor 2, stretch 2, far_value -3, far_slope 5, near_value 1, near_slope 2, square. Key 5/2.
- chk-3, MCQ, low band, statement key: anchor 2, stretch 2, far_value 1, far_slope 3, near_value -2, near_slope -1, cube. Which line earns the form point? Distractors carry BC-ERR-01008, BC-ERR-04028, BC-ERR-04029.

## Delivery

- orientation: text. Rule 6: BC-SKL-04033 carries BC-REP-01 only.
- ki-1: motion. Rule 2: BC-EK-LIM-4A1 describes a ratio that tends to 0/0 in the limit, a limit being taken (docs/lessons/unit-04/README.md, section 6) [inferred].
- ex-1: step_reveal, rule 1, with a model table (rule 2: the ratio's behaviour is a computed sequence) [inferred].
- the three error blocks: step_reveal. Rule 1.

## Band plan

- Low (full): prediction, orientation, the bridge, key ideas, st-1 with the contrast pair, ex-1 with its scoring line, chk-1, err-BC-ERR-01008, err-BC-ERR-04028, err-BC-ERR-04029, chk-2, chk-3. 567 words, 3.78 minutes (cap 900 and 6).
- Mid (brief): prediction, orientation, the bridge, core key ideas, st-1 with the contrast pair, ex-1 with its scoring line, chk-1, err-BC-ERR-01008, err-BC-ERR-04028, chk-2. 448 words, 2.99 minutes (cap 450 and 3).
- Refresher: ki-1, err-BC-ERR-01008, err-BC-ERR-04028, err-BC-ERR-04029, ex-1.

## Sources

- BC-CON-04013; BC-SKL-04033; BC-EK-LIM-4A1; ced:84, ced:93
- BC-QA-04009; BC-PT-99055; sg-23:14
- BC-ERR-01008, BC-ERR-04028, BC-ERR-04029; BC-MIS-01006, BC-MIS-04014, BC-MIS-04015
- BC-PRQ-04008
- research/units/unit-04-contextual-applications-differentiation.md#4.7 Using L'Hospital's Rule for Determining Limits of Indeterminate Forms
- research/question-analysis/question-archetypes.md#BC-QA-04009 Limit of an indeterminate form with L'Hospital's rule
- research/scoring/notation-requirements.md#Limit notation
- research/scoring/common-point-losses.md#Justification points
- research/exam/exam-structure.md#Section and part layout
- [inferred] The model table's numerator values come from f's tangent line at 3, since f is known only at two points. Settled by an archetype draw with a closed-form numerator.
- [inferred] The motion and model modes. Settled by the modality A/B.

## Machine record

```json
{
 "id": "LSN-CON-04013",
 "kind": "concept",
 "target_id": "BC-CON-04013",
 "unit": "04",
 "skills": [
  "BC-SKL-04033"
 ],
 "prediction": {
  "id": "pr-1",
  "stem": {
   "text": "Predict: as x tends to 1, f(3x) - 2 and x - 1 both tend to 0. What follows for their ratio's limit?",
   "command_verb": "predict"
  },
  "format": "mcq",
  "options": [
   {
    "id": "A",
    "label": "It is 0",
    "is_key": false
   },
   {
    "id": "B",
    "label": "It is not settled yet",
    "is_key": true
   },
   {
    "id": "C",
    "label": "It does not exist",
    "is_key": false
   }
  ],
  "resolution": "Both tending to 0 leaves the ratio's limit unsettled: an indeterminate form. Here the limit is -12.",
  "sources": [
   "BC-CON-04013",
   "BC-EK-LIM-4A1",
   "research/units/unit-04-contextual-applications-differentiation.md#4.7 Using L'Hospital's Rule for Determining Limits of Indeterminate Forms"
  ]
 },
 "orientation": {
  "text": "Take the numerator's and denominator's limits separately, then name the form in words.",
  "sources": [
   "BC-CON-04013",
   "research/units/unit-04-contextual-applications-differentiation.md#4.7 Using L'Hospital's Rule for Determining Limits of Indeterminate Forms"
  ]
 },
 "key_ideas": [
  {
   "id": "ki-1",
   "ek_id": "BC-EK-LIM-4A1",
   "depth": "core",
   "text": "When both parts tend to 0, or both to infinity, the ratio's limit is unsettled: indeterminate. Show it with two separate limits.",
   "notation": "0/0 and infinity/infinity",
   "quote": {
    "text": "such forms are said to be indeterminate",
    "source": "ced:93"
   },
   "sources": [
    "BC-EK-LIM-4A1",
    "ced:93",
    "ced:84",
    "sg-23:14",
    "research/units/unit-04-contextual-applications-differentiation.md#4.7 Using L'Hospital's Rule for Determining Limits of Indeterminate Forms"
   ]
  }
 ],
 "strategy": [
  {
   "id": "st-1",
   "archetype_id": "BC-QA-04009",
   "cue": "Both parts of a quotient vanish at the limit point.",
   "method": "The numerator's limit, then the denominator's.",
   "rival": "0 reported from the numerator alone.",
   "separating_feature": "The denominator's own limit.",
   "sources": [
    "BC-QA-04009",
    "BC-ERR-01008"
   ],
   "evidence_tag": "verified",
   "contrast": {
    "this": {
     "text": "g(4) = 1 and g'(4) = 3. Find the limit of (g(2x) - 1)/(x - 2) as x tends to 2.",
     "archetype_id": "BC-QA-04009"
    },
    "not_this": {
     "text": "Find the limit of (x^2 + 1)/(x + 3) as x tends to 2.",
     "why_not": "The denominator tends to 5; substitution settles it."
    },
    "feature": "Does the denominator tend to 0?"
   }
  }
 ],
 "worked_examples": [
  {
   "id": "ex-1",
   "archetype_id": "BC-QA-04009",
   "bands": [
    "low",
    "mid"
   ],
   "parameter_draw": {
    "anchor": 1,
    "stretch": 3,
    "far_value": 2,
    "far_slope": -4,
    "near_value": 5,
    "near_slope": 1,
    "denominator": "linear"
   },
   "problem": {
    "text": "f is differentiable, f(3) = 2, f'(3) = -4, f(1) = 5, f'(1) = 1. Find the limit of (f(3x) - 2)/(x - 1) as x tends to 1.",
    "command_verb": "find"
   },
   "calculator_status": "no_calculator",
   "steps": [
    {
     "cue": "Numerator first.",
     "why": "Differentiable, so continuous: f(3x) tends to 2.",
     "expr": "2 - 2",
     "relation": "new"
    },
    {
     "cue": "Its limit.",
     "why": "Its own statement.",
     "expr": "0",
     "relation": "equivalent",
     "point_type_id": "BC-PT-99055"
    },
    {
     "cue": "Denominator next.",
     "why": "Its own limit.",
     "expr": "x - 1",
     "relation": "new"
    },
    {
     "cue": "x tends to 1.",
     "why": "Also 0.",
     "expr": "0",
     "relation": "limit",
     "variable": "x",
     "point": "1"
    },
    {
     "cue": "Both zero.",
     "why": "Form 0/0, in words."
    },
    {
     "cue": "Ratio of derivatives.",
     "why": "3f'(3x) over 1 at x = 1.",
     "expr": "3*(-4)/1",
     "relation": "new"
    }
   ],
   "answer": {
    "form": "symbolic",
    "expr": "-12"
   }
  }
 ],
 "what_a_reader_scores": [
  {
   "example_id": "ex-1",
   "point_type_ids": [
    "BC-PT-99055"
   ],
   "lines": [
    {
     "point_type_id": "BC-PT-99055",
     "text": "L'Hospital's Rule application. Earned by: Separate limits for numerator and denominator establishing the indeterminate form, then a ratio of derivatives with at least one derivative correct (sg-23:14). Not earned by: A limit written explicitly as zero over zero, which sg-23:14 states does not earn the form point."
    }
   ]
  }
 ],
 "common_errors": [
  {
   "error_id": "BC-ERR-01008",
   "observed_behavior": "The response reports zero because the numerator tends to zero, without attending to the denominator.",
   "scoring_consequence": "The value point is lost and the rewriting step is absent.",
   "wrong_step": {
    "text": "0.",
    "expr": "0"
   },
   "right_step": {
    "text": "-12.",
    "expr": "-12"
   },
   "relation": "distinct",
   "fix_prompt": true,
   "possible_reason": {
    "misconception_id": "BC-MIS-01006",
    "text": "treats the symbol zero over zero as an answer"
   },
   "sources": [
    "BC-ERR-01008",
    "BC-MIS-01006"
   ]
  },
  {
   "error_id": "BC-ERR-04028",
   "observed_behavior": "The response writes the limit of the quotient equal to zero over zero rather than presenting the two limits separately.",
   "scoring_consequence": "The 2023 rubric states that a response presenting a limit explicitly equal to zero over zero does not earn the first point, and the Chief Reader report names this arithmetic with infinity (sg-23:14, cr-23:15).",
   "wrong_step": {
    "text": "Limit = 0/0.",
    "expr": "0/0"
   },
   "right_step": {
    "text": "Two limits, each 0.",
    "expr": "0"
   },
   "relation": "distinct",
   "fix_prompt": true,
   "possible_reason": {
    "misconception_id": "BC-MIS-04014",
    "text": "as values that may be written on the right of an equals sign"
   },
   "sources": [
    "BC-ERR-04028",
    "BC-MIS-04014"
   ]
  },
  {
   "error_id": "BC-ERR-04029",
   "observed_behavior": "The derivatives of numerator and denominator are taken with no statement that the limit was indeterminate.",
   "scoring_consequence": "The hypothesis point is lost; the CED unit overview states that students must show that the rule applies, and BC-ERR-99008 records unverified hypotheses across years (ced:84).",
   "wrong_step": {
    "text": "-12, form unstated.",
    "expr": "-12"
   },
   "right_step": {
    "text": "Form stated, then -12.",
    "expr": "-12"
   },
   "relation": "equivalent",
   "fix_prompt": false,
   "possible_reason": {
    "misconception_id": "BC-MIS-04015",
    "text": "no form is checked before it is used"
   },
   "sources": [
    "BC-ERR-04029",
    "BC-MIS-04015"
   ]
  }
 ],
 "representations": null,
 "prerequisite_bridges": [
  {
   "prq_id": "BC-PRQ-04008",
   "text": "Name each quantity in the stem and whether it varies."
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
    5,
    6
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
   "archetype_id": "BC-QA-04009",
   "parameter_draw": {
    "anchor": 1,
    "stretch": 3,
    "far_value": 2,
    "far_slope": -4,
    "near_value": 5,
    "near_slope": 1,
    "denominator": "linear"
   },
   "completes": "ex-1",
   "stem": {
    "text": "In the example above, both limits are 0. Finish with the ratio of derivatives.",
    "command_verb": "find"
   },
   "key": {
    "form": "symbolic",
    "expr": "-12"
   },
   "steps": [
    {
     "text": "3f'(3)/1.",
     "expr": "3*(-4)/1",
     "relation": "new"
    }
   ],
   "calculator_status": "no_calculator",
   "skills": [
    "BC-SKL-04033"
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
   "archetype_id": "BC-QA-04009",
   "parameter_draw": {
    "anchor": 2,
    "stretch": 2,
    "far_value": -3,
    "far_slope": 5,
    "near_value": 1,
    "near_slope": 2,
    "denominator": "square"
   },
   "stem": {
    "text": "f(4) = -3, f'(4) = 5. Show the form, then find the limit of (f(2x) + 3)/(x^2 - 4) as x tends to 2.",
    "command_verb": "find"
   },
   "key": {
    "form": "symbolic",
    "expr": "5/2"
   },
   "steps": [
    {
     "text": "Numerator.",
     "expr": "-3 + 3",
     "relation": "new"
    },
    {
     "text": "0.",
     "expr": "0",
     "relation": "equivalent"
    },
    {
     "text": "Denominator.",
     "expr": "x**2 - 4",
     "relation": "new"
    },
    {
     "text": "0.",
     "expr": "0",
     "relation": "limit",
     "variable": "x",
     "point": "2"
    },
    {
     "text": "2f'(4)/(2x) at 2.",
     "expr": "2*5/(2*2)",
     "relation": "new"
    }
   ],
   "calculator_status": "no_calculator",
   "skills": [
    "BC-SKL-04033"
   ]
  },
  {
   "id": "chk-3",
   "check_kind": "mcq",
   "format": "mcq",
   "bands": [
    "low"
   ],
   "archetype_id": "BC-QA-04009",
   "parameter_draw": {
    "anchor": 2,
    "stretch": 2,
    "far_value": 1,
    "far_slope": 3,
    "near_value": -2,
    "near_slope": -1,
    "denominator": "cube"
   },
   "stem": {
    "text": "f(4) = 1, f'(4) = 3. Which opening line for the limit of (f(2x) - 1)/(x^3 - 8) as x tends to 2 earns the form point?",
    "command_verb": "identify"
   },
   "key": {
    "form": "statement",
    "expr": "separate_limits",
    "label": "The numerator's limit is f(4) - 1 = 0 and the denominator's is 0."
   },
   "steps": [
    {
     "text": "Numerator.",
     "expr": "1 - 1",
     "relation": "new"
    },
    {
     "text": "Denominator.",
     "expr": "x**3 - 8",
     "relation": "new"
    },
    {
     "text": "0.",
     "expr": "0",
     "relation": "limit",
     "variable": "x",
     "point": "2"
    }
   ],
   "options": [
    {
     "id": "A",
     "is_key": false,
     "label": "The numerator tends to 0, so the limit is 0.",
     "error_path": "BC-ERR-01008",
     "derivation": "denominator ignored"
    },
    {
     "id": "B",
     "is_key": false,
     "label": "The limit equals 0/0.",
     "error_path": "BC-ERR-04028",
     "derivation": "quotient written equal to the form"
    },
    {
     "id": "C",
     "is_key": true,
     "label": "The numerator's limit is f(4) - 1 = 0 and the denominator's is 0.",
     "error_path": null
    },
    {
     "id": "D",
     "is_key": false,
     "label": "By L'Hospital's rule the limit is 2f'(4)/12.",
     "error_path": "BC-ERR-04029",
     "derivation": "rule applied with no form stated"
    }
   ],
   "calculator_status": "no_calculator",
   "skills": [
    "BC-SKL-04033"
   ]
  }
 ],
 "delivery": [
  {
   "block": "orientation",
   "mode": "text",
   "reason": "rule 6: BC-SKL-04033 carries BC-REP-01 only",
   "sources": [
    "BC-SKL-04033"
   ]
  },
  {
   "block": "ki-1",
   "mode": "motion",
   "reason": "rule 2: BC-EK-LIM-4A1 describes a ratio tending to 0/0 in the limit, a limit being taken",
   "sources": [
    "BC-SKL-04033"
   ],
   "spec": {
    "kind": "number_line_pair",
    "representations": [
     "BC-REP-01"
    ],
    "frames": [
     {
      "x": 1.1,
      "numerator": -1.2,
      "denominator": 0.1
     },
     {
      "x": 1.01,
      "numerator": -0.12,
      "denominator": 0.01
     },
     {
      "x": 1.001,
      "numerator": -0.012,
      "denominator": 0.001
     }
    ],
    "labels": [
     {
      "text": "numerator tends to 0",
      "placement": "inside"
     },
     {
      "text": "denominator tends to 0",
      "placement": "inside"
     },
     {
      "text": "ratio stays near -12",
      "placement": "inside"
     }
    ]
   },
   "fallback": "the three frames as one static table",
   "keyboard": "Right arrow steps to the next frame, Left arrow to the previous; Space pauses auto-advance",
   "reduced_motion": "no auto-advance; each key press cross-fades to the next frame"
  },
  {
   "block": "ex-1",
   "mode": "step_reveal",
   "reason": "rule 1; rule 2 names a computed sequence as the idea, so the reveal carries a model table of numerator, denominator and ratio at shrinking distance",
   "sources": [
    "BC-SKL-04033"
   ],
   "spec": {
    "kind": "table",
    "columns": [
     "x",
     "numerator",
     "denominator",
     "ratio"
    ],
    "rows": [
     [
      "1.1",
      "-1.2",
      "0.1",
      "-12"
     ],
     [
      "1.01",
      "-0.12",
      "0.01",
      "-12"
     ],
     [
      "1.001",
      "-0.012",
      "0.001",
      "-12"
     ]
    ],
    "labels": [
     {
      "text": "both parts shrink; the ratio does not",
      "placement": "inside"
     }
    ]
   },
   "fallback": "the same three rows as static text",
   "keyboard": "Tab moves between rows; no control"
  },
  {
   "block": "err-BC-ERR-01008",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  },
  {
   "block": "err-BC-ERR-04028",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  },
  {
   "block": "err-BC-ERR-04029",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  }
 ],
 "refresher": [
  "ki-1",
  "err-BC-ERR-01008",
  "err-BC-ERR-04028",
  "err-BC-ERR-04029",
  "ex-1"
 ],
 "research_lines": [
  {
   "file": "research/units/unit-04-contextual-applications-differentiation.md",
   "line": "it is incorrect to write the limit of the quotient equal to zero over zero"
  }
 ],
 "inferred": [
  {
   "claim": "The model and motion values take the numerator from f's tangent line at 3, since f is known only through two values and two slopes.",
   "settles": "An archetype draw with a closed-form numerator, or a model rule for functions known through values."
  },
  {
   "claim": "The ki-1 motion and the ex-1 model table serve better than text.",
   "settles": "The modality A/B in the build plan: skip rate and time to first credited success by mode."
  }
 ],
 "sources": [
  "BC-CON-04013",
  "BC-SKL-04033",
  "BC-EK-LIM-4A1",
  "ced:84",
  "ced:93",
  "BC-QA-04009",
  "BC-PT-99055",
  "sg-23:14",
  "BC-ERR-01008",
  "BC-ERR-04028",
  "BC-ERR-04029",
  "BC-MIS-01006",
  "BC-MIS-04014",
  "BC-MIS-04015",
  "BC-PRQ-04008",
  "research/units/unit-04-contextual-applications-differentiation.md#4.7 Using L'Hospital's Rule for Determining Limits of Indeterminate Forms",
  "research/question-analysis/question-archetypes.md#BC-QA-04009 Limit of an indeterminate form with L'Hospital's rule",
  "research/scoring/notation-requirements.md#Limit notation",
  "research/scoring/common-point-losses.md#Justification points",
  "research/exam/exam-structure.md#Section and part layout"
 ],
 "word_count": {
  "full": 567,
  "brief": 448
 },
 "read_minutes": {
  "full": 3.78,
  "brief": 2.99
 }
}
```
