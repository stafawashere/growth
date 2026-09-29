---
title: LSN-CON-04014 The hypothesis of L'Hospital's rule
research_date: 2026-09-29
status: designed
purpose: Authoring spec for the concept lesson on BC-CON-04014, establishing the indeterminate form, with continuity drawn from differentiability, before L'Hospital's rule is used, built from authoring_bundle("BC-CON-04014") and the research files it cites.
---

# LSN-CON-04014 The hypothesis of L'Hospital's rule

Concept BC-CON-04014 (skills BC-SKL-04034, BC-SKL-04038), topic 4.7, loaded by BC-QA-04009. No hard parent in the unit; BC-CON-04013 supports it (docs/lessons/unit-04/README.md, section 1).

## Prediction

One question on ex-1's own numbers, both bands, served first: Predict before the rule: f is differentiable with f(4) = 4. What is the limit of f(2x) - 4 as x tends to 2? Form: `short_answer` with numeric key 0, which is a valued step of ex-1. Resolution shown on the key idea screen: A differentiable function is continuous, so f(2x) tends to f(4) = 4 as x tends to 2 and the numerator tends to 0. That is the first half of the rule's hypothesis. Sources: the concept record and the topic section the key idea cites.

## Orientation

Served text, from BC-CON-04014 `description_plain` and the topic's Assessment behaviour paragraph (research/units/unit-04-contextual-applications-differentiation.md#4.7 Using L'Hospital's Rule for Determining Limits of Indeterminate Forms): a response shows the form is indeterminate before using the rule, taking the limit of a function known through values as its value because differentiability gives continuity.

## Key ideas

BC-SKL-04034 maps to BC-EK-LIM-4A2 and BC-SKL-04038 to BC-EK-LIM-4A1 (ced:93): two core blocks.

- ki-1 (core), BC-EK-LIM-4A2. Paraphrase of "The hypothesis": both limits zero, or both infinite, is the necessary first step, checked before the rule (ced:84, sg-23:14). Anchor quote from ced:93.
- ki-2 (core), BC-EK-LIM-4A1. Paraphrase of "Continuity from differentiability": a function known only through values is differentiable, hence continuous, so its limit is its value (sg-23:14). Anchor quote from ced:93.

## Recognition

BC-QA-04009 (research/question-analysis/question-archetypes.md#BC-QA-04009 Limit of an indeterminate form with L'Hospital's rule): `common_givens` "a quotient containing a function known only through a graph of its derivative and one value" and "values of a function and its derivative at one input"; `difficulty_variables` "whether differentiability must be used to evaluate a limit in the numerator". The signal: an unknown f inside the numerator with f and f' given at the inner point. FRQ shape: BC-FRQ-2023-Q4-C, BC-FRQ-2013-Q5-A.

Not this concept: a quotient of named elementary functions, where the limits are read directly.

The near miss comes from a quotient of named elementary functions, where each limit is read directly and no differentiability reason is asked for. That stem is the `not_this` of the contrast pair on st-1.

## Method choice

- st-1, BC-QA-04009. Method, `expected_solution_path[0]`: "evaluate the limit of the numerator, using continuity where the function is known to be differentiable". Rival from `wrong_approaches`: applying the rule with no check of the form (BC-ERR-04029). Separating feature: an unknown f, whose limit needs the continuity reason.

## Solution path

- ex-1, BC-QA-04009, both bands, no calculator. Draw: anchor 2, stretch 2, far_value 4, far_slope -3, near_value 1, near_slope 5, denominator exponential; the limit of (f(2x) - 4)/(e^(x - 2) - 1) as x tends to 2. Not a published draw.
- Steps: numerator via continuity (new, equivalent); denominator (new, limit); the form (no value); the ratio of derivatives (new). A fluent solver writes all; the continuity clause is one phrase.

## Scoring

BC-QA-04009 lists BC-PT-99055; ex-1 tags it on the numerator limit. Continuity is derived from differentiability, not asserted (research/scoring/justification-requirements.md#Theorem hypotheses, sg-25:12); unverified hypotheses of the rule lose the condition point (research/scoring/common-point-losses.md#Justification points).

## Traps

Two active errors in the bundle's order: BC-ERR-04028, BC-ERR-04029. Both on ex-1's draw, both bands.

- err-BC-ERR-04028: the quotient written equal to 0/0. Reason words from BC-MIS-04014.
- err-BC-ERR-04029: the rule applied with no form stated; same value, marked equivalent. Reason words from BC-MIS-04015.

## Representations

None as a separate block; ki-2's figure carries the graph-to-limit conversion (BC-REP-02 to BC-REP-01).

## Prerequisite bridge

- BC-PRQ-04008, from `description_plain` and `failure_signature`.

## Time

BC-QA-04009 is `no_calculator`, one part of a graphical analysis FRQ: Section II Part B, 15.0 minutes per question (research/exam/exam-structure.md#Section and part layout). Written: each limit with its reason, the form, the ratio, the value. Nothing is skipped (sg-23:14).

## Checks

Two checks: the bundle holds two errors, fewer than chk-3's three distractors need [inferred].

- chk-1, completion of ex-1, both bands. Key -6.
- chk-2, isomorph, both bands: anchor 1, stretch 3, far_value -1, far_slope 2, near_value 3, near_slope 4, denominator sine. Key 6.

## Delivery

- orientation: text. Rule 5 for a statement of what a response shows.
- ki-1: text. Rule 5: BC-SKL-04034 carries BC-REP-01 and BC-REP-04.
- ki-2: figure. Rule 3: BC-REP-02 in BC-SKL-04038; no varying quantity is read, so no promotion (docs/lessons/unit-04/README.md, section 6) [inferred].
- ex-1 and the two error blocks: step_reveal. Rule 1.

## Band plan

- Low (full): prediction, orientation, the bridge, key ideas, st-1 with the contrast pair, ex-1 with its scoring line, chk-1, err-BC-ERR-04028, err-BC-ERR-04029, chk-2. 450 words, 3.0 minutes (cap 900 and 6).
- Mid (brief): prediction, orientation, the bridge, core key ideas, st-1 with the contrast pair, ex-1 with its scoring line, chk-1, err-BC-ERR-04028, err-BC-ERR-04029, chk-2. 450 words, 3.0 minutes (cap 450 and 3).
- Refresher: ki-1, ki-2, err-BC-ERR-04028, err-BC-ERR-04029, ex-1.

## Sources

- BC-CON-04014; BC-SKL-04034, BC-SKL-04038; BC-EK-LIM-4A1, BC-EK-LIM-4A2; ced:84, ced:93
- BC-QA-04009; BC-PT-99055; sg-23:14, sg-25:12
- BC-ERR-04028, BC-ERR-04029; BC-MIS-04014, BC-MIS-04015
- BC-PRQ-04008
- research/units/unit-04-contextual-applications-differentiation.md#4.7 Using L'Hospital's Rule for Determining Limits of Indeterminate Forms
- research/question-analysis/question-archetypes.md#BC-QA-04009 Limit of an indeterminate form with L'Hospital's rule
- research/scoring/justification-requirements.md#Theorem hypotheses
- research/scoring/common-point-losses.md#Justification points
- research/exam/exam-structure.md#Section and part layout
- [inferred] Two checks, for want of a third error. Settled by a third active error on BC-SKL-04034 or BC-SKL-04038.
- [inferred] The ki-2 figure. Settled by the modality A/B.

## Machine record

```json
{
 "id": "LSN-CON-04014",
 "kind": "concept",
 "target_id": "BC-CON-04014",
 "unit": "04",
 "skills": [
  "BC-SKL-04034",
  "BC-SKL-04038"
 ],
 "prediction": {
  "id": "pr-1",
  "stem": {
   "text": "Predict: f is differentiable and f(4) = 4. What is the limit of f(2x) - 4 as x tends to 2?",
   "command_verb": "predict"
  },
  "format": "short_answer",
  "key": {
   "form": "numeric",
   "expr": "0"
  },
  "resolution": "Differentiable means continuous, so f(2x) tends to 4 and the numerator tends to 0.",
  "sources": [
   "BC-CON-04014",
   "BC-EK-LIM-4A1",
   "research/units/unit-04-contextual-applications-differentiation.md#4.7 Using L'Hospital's Rule for Determining Limits of Indeterminate Forms"
  ]
 },
 "orientation": {
  "text": "Show the form is indeterminate with two separate limits, each with its reason.",
  "sources": [
   "BC-CON-04014",
   "research/units/unit-04-contextual-applications-differentiation.md#4.7 Using L'Hospital's Rule for Determining Limits of Indeterminate Forms"
  ]
 },
 "key_ideas": [
  {
   "id": "ki-1",
   "ek_id": "BC-EK-LIM-4A2",
   "depth": "core",
   "text": "Both limits tend to 0, or both to infinity; check this first, before any derivative.",
   "notation": "two separate limits",
   "quote": {
    "text": "Limits of the indeterminate forms 0 over 0",
    "source": "ced:93"
   },
   "sources": [
    "BC-EK-LIM-4A2",
    "ced:93",
    "ced:84",
    "sg-23:14",
    "research/units/unit-04-contextual-applications-differentiation.md#4.7 Using L'Hospital's Rule for Determining Limits of Indeterminate Forms"
   ]
  },
  {
   "id": "ki-2",
   "ek_id": "BC-EK-LIM-4A1",
   "depth": "core",
   "text": "A function known only through values is differentiable, so continuous.",
   "notation": "differentiable implies continuous",
   "quote": {
    "text": "such forms are said to be indeterminate",
    "source": "ced:93"
   },
   "sources": [
    "BC-EK-LIM-4A1",
    "ced:93",
    "sg-23:14",
    "research/units/unit-04-contextual-applications-differentiation.md#4.7 Using L'Hospital's Rule for Determining Limits of Indeterminate Forms"
   ]
  }
 ],
 "strategy": [
  {
   "id": "st-1",
   "archetype_id": "BC-QA-04009",
   "cue": "An unknown f in the numerator.",
   "method": "The numerator's limit, citing differentiability.",
   "rival": "The rule with no form checked.",
   "separating_feature": "f known only through values.",
   "sources": [
    "BC-QA-04009",
    "BC-ERR-04029"
   ],
   "evidence_tag": "verified",
   "contrast": {
    "this": {
     "text": "g is differentiable, g(3) = 2. Find the limit of (g(3x) - 2)/(x - 1) as x tends to 1.",
     "archetype_id": "BC-QA-04009"
    },
    "not_this": {
     "text": "Find the limit of sin(x)/(e^x - 1) as x tends to 0.",
     "why_not": "Each limit is read directly."
    },
    "feature": "An unknown f in the numerator."
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
    "anchor": 2,
    "stretch": 2,
    "far_value": 4,
    "far_slope": -3,
    "near_value": 1,
    "near_slope": 5,
    "denominator": "exponential"
   },
   "problem": {
    "text": "f is differentiable, f(4) = 4, f'(4) = -3. Find the limit of (f(2x) - 4)/(e^(x - 2) - 1) as x tends to 2.",
    "command_verb": "find"
   },
   "calculator_status": "no_calculator",
   "steps": [
    {
     "cue": "Unknown f in the numerator.",
     "why": "Continuous: f(2x) tends to 4.",
     "expr": "4 - 4",
     "relation": "new"
    },
    {
     "cue": "Numerator limit.",
     "why": "Alone.",
     "expr": "0",
     "relation": "equivalent",
     "point_type_id": "BC-PT-99055"
    },
    {
     "cue": "Denominator.",
     "why": "Its own limit.",
     "expr": "exp(x - 2) - 1",
     "relation": "new"
    },
    {
     "cue": "x tends to 2.",
     "why": "Also 0.",
     "expr": "0",
     "relation": "limit",
     "variable": "x",
     "point": "2"
    },
    {
     "cue": "Hypothesis met.",
     "why": "0/0, in words."
    },
    {
     "cue": "Rule applies.",
     "why": "2f'(2x) over e^(x - 2).",
     "expr": "2*(-3)/exp(0)",
     "relation": "new"
    }
   ],
   "answer": {
    "form": "symbolic",
    "expr": "-6"
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
    "text": "-6, form unstated.",
    "expr": "-6"
   },
   "right_step": {
    "text": "Form stated, then -6.",
    "expr": "-6"
   },
   "relation": "equivalent",
   "fix_prompt": false,
   "possible_reason": {
    "misconception_id": "BC-MIS-04015",
    "text": "treats the rule as a general device for limits that resist substitution"
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
    "anchor": 2,
    "stretch": 2,
    "far_value": 4,
    "far_slope": -3,
    "near_value": 1,
    "near_slope": 5,
    "denominator": "exponential"
   },
   "completes": "ex-1",
   "stem": {
    "text": "For ex-1 the form is 0/0. Finish with the ratio of derivatives.",
    "command_verb": "find"
   },
   "key": {
    "form": "symbolic",
    "expr": "-6"
   },
   "steps": [
    {
     "text": "2f'(4)/e^0.",
     "expr": "2*(-3)/exp(0)",
     "relation": "new"
    }
   ],
   "calculator_status": "no_calculator",
   "skills": [
    "BC-SKL-04034"
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
    "anchor": 1,
    "stretch": 3,
    "far_value": -1,
    "far_slope": 2,
    "near_value": 3,
    "near_slope": 4,
    "denominator": "sine"
   },
   "stem": {
    "text": "f is differentiable, f(3) = -1, f'(3) = 2. Verify the form, then find the limit of (f(3x) + 1)/sin(x - 1) as x tends to 1.",
    "command_verb": "find"
   },
   "key": {
    "form": "symbolic",
    "expr": "6"
   },
   "steps": [
    {
     "text": "Numerator, by continuity.",
     "expr": "-1 + 1",
     "relation": "new"
    },
    {
     "text": "0.",
     "expr": "0",
     "relation": "equivalent"
    },
    {
     "text": "Denominator.",
     "expr": "sin(x - 1)",
     "relation": "new"
    },
    {
     "text": "0.",
     "expr": "0",
     "relation": "limit",
     "variable": "x",
     "point": "1"
    },
    {
     "text": "3f'(3)/cos(0).",
     "expr": "3*2/cos(0)",
     "relation": "new"
    }
   ],
   "calculator_status": "no_calculator",
   "skills": [
    "BC-SKL-04038"
   ]
  }
 ],
 "delivery": [
  {
   "block": "orientation",
   "mode": "text",
   "reason": "rule 5: a statement of what a response shows",
   "sources": [
    "BC-SKL-04034"
   ]
  },
  {
   "block": "ki-1",
   "mode": "text",
   "reason": "rule 5: BC-SKL-04034 carries BC-REP-01 and BC-REP-04",
   "sources": [
    "BC-SKL-04034"
   ]
  },
  {
   "block": "ki-2",
   "mode": "figure",
   "reason": "rule 3: BC-REP-02 in BC-SKL-04038 and BC-QA-04009 common_givens; no varying quantity is read, so no promotion",
   "sources": [
    "BC-SKL-04038",
    "BC-QA-04009"
   ],
   "spec": {
    "kind": "graph",
    "representations": [
     "BC-REP-02"
    ],
    "window": {
     "x": [
      3,
      5
     ],
     "y": [
      1,
      7
     ]
    },
    "curves": [
     {
      "expr": "4 - 3*(x - 4) + (x - 4)**3/2"
     }
    ],
    "points": [
     {
      "x": 4,
      "y": 4,
      "style": "closed"
     }
    ],
    "labels": [
     {
      "text": "(4, 4): no hole, no jump",
      "placement": "inside"
     },
     {
      "text": "differentiable here, so continuous",
      "placement": "inside"
     }
    ]
   },
   "fallback": "the same graph as a static image with its two labels",
   "keyboard": "none needed: the figure has no control"
  },
  {
   "block": "ex-1",
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
  "ki-2",
  "err-BC-ERR-04028",
  "err-BC-ERR-04029",
  "ex-1"
 ],
 "research_lines": [
  {
   "file": "research/units/unit-04-contextual-applications-differentiation.md",
   "line": "differentiability at the point gives continuity there, so the limit of that function is its value"
  }
 ],
 "inferred": [
  {
   "claim": "The lesson carries two checks, because the bundle holds two errors and chk-3 needs three distractors from error blocks.",
   "settles": "A third active error on BC-SKL-04034 or BC-SKL-04038."
  },
  {
   "claim": "The ki-2 figure serves better than text.",
   "settles": "The modality A/B in the build plan: skip rate and time to first credited success by mode."
  }
 ],
 "sources": [
  "BC-CON-04014",
  "BC-SKL-04034",
  "BC-SKL-04038",
  "BC-EK-LIM-4A1",
  "BC-EK-LIM-4A2",
  "ced:84",
  "ced:93",
  "BC-QA-04009",
  "BC-PT-99055",
  "sg-23:14",
  "sg-25:12",
  "BC-ERR-04028",
  "BC-ERR-04029",
  "BC-MIS-04014",
  "BC-MIS-04015",
  "BC-PRQ-04008",
  "research/units/unit-04-contextual-applications-differentiation.md#4.7 Using L'Hospital's Rule for Determining Limits of Indeterminate Forms",
  "research/question-analysis/question-archetypes.md#BC-QA-04009 Limit of an indeterminate form with L'Hospital's rule",
  "research/scoring/justification-requirements.md#Theorem hypotheses",
  "research/scoring/common-point-losses.md#Justification points",
  "research/exam/exam-structure.md#Section and part layout"
 ],
 "word_count": {
  "full": 450,
  "brief": 450
 },
 "read_minutes": {
  "full": 3.0,
  "brief": 3.0
 }
}
```
