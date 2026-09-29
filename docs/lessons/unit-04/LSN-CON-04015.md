---
title: LSN-CON-04015 The conclusion of L'Hospital's rule
research_date: 2026-09-29
status: designed
purpose: Authoring spec for the concept lesson on BC-CON-04015, replacing the limit of a ratio by the limit of the ratio of the two derivatives and evaluating it, built from authoring_bundle("BC-CON-04015") and the research files it cites.
---

# LSN-CON-04015 The conclusion of L'Hospital's rule

Concept BC-CON-04015 (skills BC-SKL-04035, BC-SKL-04036, BC-SKL-04037), topic 4.7, loaded by BC-QA-04009. Its hard parents are BC-CON-04013 and BC-CON-04014 (docs/lessons/unit-04/README.md, section 1).

## Orientation

Served text, from BC-CON-04015 `description_plain` and the topic's The conclusion paragraph (research/units/unit-04-contextual-applications-differentiation.md#4.7 Using L'Hospital's Rule for Determining Limits of Indeterminate Forms): once the form is shown indeterminate, a response differentiates numerator and denominator separately, keeps limit notation, evaluates the new limit, and applies the rule again only if the form persists.

## Key ideas

All three skills map to BC-EK-LIM-4A2 (ced:93), one core block.

- ki-1 (core). Paraphrase of "The conclusion": under the hypothesis, the limit of the quotient equals the limit of the derivative of the numerator over the derivative of the denominator, the ratio of the derivatives and not the derivative of the ratio (ced:84). A chain rule factor on an inner function stays. Anchor quote from ced:93.

## Recognition

BC-QA-04009 (research/question-analysis/question-archetypes.md#BC-QA-04009 Limit of an indeterminate form with L'Hospital's rule): `asked_to_produce` "a limit of the ratio of derivatives" and the value with justification; `difficulty_variables` "whether the rule must be applied more than once". The signal: the form has been established and a value is asked. Shapes: MCQ (BC-MCQ-PE2012-028) and a graphical analysis FRQ part (BC-FRQ-2023-Q4-C), scored as form, application, answer (sg-23:14).

Not this concept: a limit settled by substitution or by algebra, with no indeterminate form.

## Method choice

- st-1, BC-QA-04009. Method, `expected_solution_path[3]`: differentiate numerator and denominator separately. Rival from `wrong_approaches`: the quotient rule on the whole quotient (BC-ERR-04030). Separating feature: the conclusion is a ratio of two derivatives.

## Solution path

- ex-1, BC-QA-04009, both bands, no calculator. Draw: anchor 1, stretch 2, far_value 3, far_slope 5, near_value -2, near_slope -1, denominator sine; the limit of (f(2x) - 3)/sin(x - 1) as x tends to 1, with f(2) = 3, f'(2) = 5, f(1) = -2, f'(1) = -1. Not a published draw.
- Steps: the form, carried from BC-CON-04014 (no value); numerator derivative at the point (new); denominator derivative (new, evaluate); the value (new). A fluent solver writes the ratio in limit notation and the value.

## Scoring

BC-QA-04009 lists BC-PT-99055; ex-1 tags it on the ratio of derivatives. Limit notation is kept on every line (research/scoring/notation-requirements.md#Limit notation). An incorrect derivative after a correct application costs the answer point (cr-23:15).

## Traps

Five active errors meet the skills; the first four in the bundle's order are served: BC-ERR-03003, BC-ERR-04029, BC-ERR-04030, BC-ERR-04031. BC-ERR-99008 is left out by the cap; BC-ERR-04029 carries the same unverified hypothesis. On ex-1's draw; mid band the first two.

- err-BC-ERR-03003: 2f'(1) used for 2f'(2). Reason words from BC-MIS-03002.
- err-BC-ERR-04029: 10 reached with no form stated; same value, marked equivalent. Reason words from BC-MIS-04015.
- err-BC-ERR-04030: the quotient rule on the whole ratio. Reason words from BC-MIS-04016.
- err-BC-ERR-04031: the chain factor 2 dropped. No reason line.

## Representations

None. The topic's Representations paragraph names a quotient of functions to a quotient of derivatives (BC-REP-01 to BC-REP-01), carried by ex-1.

## Prerequisite bridge

- BC-PRQ-04008, from `description_plain` and `failure_signature`.

## Time

BC-QA-04009 is `no_calculator`, one part of a graphical analysis FRQ: Section II Part B, 15.0 minutes per question (research/exam/exam-structure.md#Section and part layout). Written: the ratio of derivatives in limit notation and the value. Held: the chain rule factor's arithmetic.

## Checks

- chk-1, completion of ex-1, both bands. Key 10.
- chk-2, isomorph, both bands: anchor 1, stretch 3, far_value 0, far_slope -2, near_value 2, near_slope 4, denominator cube. Key -2.
- chk-3, MCQ, low band: anchor 2, stretch 3, far_value -1, far_slope 2, near_value 4, near_slope -3, denominator linear. Key 6. Distractors: -9 (BC-ERR-03003), 0 (BC-ERR-04030, the quotient rule numerator at x = 2) [inferred], 2 (BC-ERR-04031).

## Delivery

- orientation and ki-1: text. Rule 5: BC-SKL-04035, 04036 and 04037 carry BC-REP-01 only (docs/lessons/unit-04/README.md, section 6).
- ex-1 and the four error blocks: step_reveal. Rule 1.

## Band plan

- Low (full): orientation, ki-1, st-1, ex-1 with its scoring line, four error blocks, chk-1 to chk-3, the bridge. 532 words, 3.6 minutes (cap 900 and 6).
- Mid (brief): orientation, ki-1, st-1, ex-1 with its scoring line, err-BC-ERR-03003, err-BC-ERR-04029, chk-1, chk-2, the bridge. 390 words, 2.6 minutes (cap 450 and 3).
- Refresher: ki-1, err-BC-ERR-03003, err-BC-ERR-04029, err-BC-ERR-04030, err-BC-ERR-04031, ex-1.

## Sources

- BC-CON-04015; BC-SKL-04035, BC-SKL-04036, BC-SKL-04037; BC-EK-LIM-4A2; ced:84, ced:93
- BC-QA-04009; BC-PT-99055; sg-23:14, cr-23:15
- BC-ERR-03003, BC-ERR-04029, BC-ERR-04030, BC-ERR-04031; BC-MIS-03002, BC-MIS-04015, BC-MIS-04016
- BC-PRQ-04008
- research/units/unit-04-contextual-applications-differentiation.md#4.7 Using L'Hospital's Rule for Determining Limits of Indeterminate Forms
- research/question-analysis/question-archetypes.md#BC-QA-04009 Limit of an indeterminate form with L'Hospital's rule
- research/scoring/notation-requirements.md#Limit notation
- research/exam/exam-structure.md#Section and part layout
- [inferred] The BC-ERR-04030 distractor value 0. Settled by response data on chk-3.

## Machine record

```json
{
 "id": "LSN-CON-04015",
 "kind": "concept",
 "target_id": "BC-CON-04015",
 "unit": "04",
 "skills": [
  "BC-SKL-04035",
  "BC-SKL-04036",
  "BC-SKL-04037"
 ],
 "orientation": {
  "text": "Once the form is shown indeterminate, differentiate numerator and denominator separately, keep limit notation, and evaluate. If the new limit is still indeterminate, apply the rule again.",
  "sources": [
   "BC-CON-04015",
   "research/units/unit-04-contextual-applications-differentiation.md#4.7 Using L'Hospital's Rule for Determining Limits of Indeterminate Forms"
  ]
 },
 "key_ideas": [
  {
   "id": "ki-1",
   "ek_id": "BC-EK-LIM-4A2",
   "depth": "core",
   "text": "Under the hypothesis, the limit of the quotient equals the limit of the numerator's derivative over the denominator's derivative: the ratio of the derivatives, not the derivative of the ratio. An inner function keeps its chain rule factor.",
   "notation": "limit of f'/g'",
   "quote": {
    "text": "Limits of the indeterminate forms 0 over 0",
    "source": "ced:93"
   },
   "sources": [
    "BC-EK-LIM-4A2",
    "ced:93",
    "ced:84",
    "research/units/unit-04-contextual-applications-differentiation.md#4.7 Using L'Hospital's Rule for Determining Limits of Indeterminate Forms"
   ]
  }
 ],
 "strategy": [
  {
   "id": "st-1",
   "archetype_id": "BC-QA-04009",
   "cue": "Form shown 0/0; the value is asked.",
   "method": "Next line: the limit of the numerator's derivative over the denominator's derivative.",
   "rival": "Rival: the quotient rule on the whole ratio (BC-ERR-04030).",
   "separating_feature": "Two separate derivatives, one ratio.",
   "sources": [
    "BC-QA-04009"
   ],
   "evidence_tag": "verified"
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
    "stretch": 2,
    "far_value": 3,
    "far_slope": 5,
    "near_value": -2,
    "near_slope": -1,
    "denominator": "sine"
   },
   "problem": {
    "text": "f is differentiable, f(2) = 3, f'(2) = 5, f(1) = -2, f'(1) = -1. Find the limit of (f(2x) - 3)/sin(x - 1) as x tends to 1.",
    "command_verb": "find"
   },
   "calculator_status": "no_calculator",
   "steps": [
    {
     "cue": "Both limits are 0.",
     "why": "Form 0/0 stated, so the rule applies."
    },
    {
     "cue": "Numerator f(2x): inner 2x.",
     "why": "2f'(2x); at x = 1 read f' at 2.",
     "expr": "2*5",
     "relation": "new",
     "point_type_id": "BC-PT-99055"
    },
    {
     "cue": "Denominator separately.",
     "why": "Its own derivative.",
     "expr": "cos(x - 1)",
     "relation": "new"
    },
    {
     "cue": "At x = 1.",
     "why": "Nonzero: no second application.",
     "expr": "1",
     "relation": "evaluate",
     "subs": {
      "x": "1"
     }
    },
    {
     "cue": "Ratio of the two.",
     "why": "Limit notation kept.",
     "expr": "10/1",
     "relation": "new"
    }
   ],
   "answer": {
    "form": "symbolic",
    "expr": "10"
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
   "error_id": "BC-ERR-03003",
   "observed_behavior": "In a table or graph based composite, the derivative of the outer function is read at the stated input instead of at the value the inner function produces.",
   "scoring_consequence": "The numerical answer is wrong even though the chain rule structure was written correctly.",
   "wrong_step": {
    "text": "2f'(1).",
    "expr": "2*(-1)"
   },
   "right_step": {
    "text": "2f'(2).",
    "expr": "2*5"
   },
   "relation": "distinct",
   "possible_reason": {
    "misconception_id": "BC-MIS-03002",
    "text": "the inner output plays no part in where the outer derivative is read"
   },
   "sources": [
    "BC-ERR-03003",
    "BC-MIS-03002"
   ]
  },
  {
   "error_id": "BC-ERR-04029",
   "observed_behavior": "The derivatives of numerator and denominator are taken with no statement that the limit was indeterminate.",
   "scoring_consequence": "The hypothesis point is lost; the CED unit overview states that students must show that the rule applies, and BC-ERR-99008 records unverified hypotheses across years (ced:84).",
   "wrong_step": {
    "text": "10, form unstated.",
    "expr": "10"
   },
   "right_step": {
    "text": "Form stated, then 10.",
    "expr": "10"
   },
   "relation": "equivalent",
   "possible_reason": {
    "misconception_id": "BC-MIS-04015",
    "text": "no form is checked before it is used"
   },
   "sources": [
    "BC-ERR-04029",
    "BC-MIS-04015"
   ]
  },
  {
   "error_id": "BC-ERR-04030",
   "observed_behavior": "The derivative of the whole quotient is taken rather than the quotient of the two derivatives.",
   "scoring_consequence": "The application point is lost; the CED unit overview emphasises that the conclusion features the ratio of the derivatives rather than the derivative of the ratio (ced:84).",
   "wrong_step": {
    "text": "Quotient rule.",
    "expr": "(2*fp*sin(x - 1) - (f2 - 3)*cos(x - 1))/sin(x - 1)**2"
   },
   "right_step": {
    "text": "Separate derivatives.",
    "expr": "2*fp/cos(x - 1)"
   },
   "relation": "distinct",
   "possible_reason": {
    "misconception_id": "BC-MIS-04016",
    "text": "reads the conclusion as the limit of the derivative of the quotient"
   },
   "sources": [
    "BC-ERR-04030",
    "BC-MIS-04016"
   ]
  },
  {
   "error_id": "BC-ERR-04031",
   "observed_behavior": "The numerator contains a function known only through supplied properties and its derivative is mishandled, so the resulting limit is wrong.",
   "scoring_consequence": "The answer point is lost although the hypothesis and application points may be earned; the 2023 report records incorrect derivatives of the numerator or denominator as the common failure after a correct application (cr-23:15).",
   "wrong_step": {
    "text": "f'(2).",
    "expr": "5"
   },
   "right_step": {
    "text": "2f'(2).",
    "expr": "10"
   },
   "relation": "distinct",
   "possible_reason": null,
   "sources": [
    "BC-ERR-04031"
   ]
  }
 ],
 "representations": null,
 "prerequisite_bridges": [
  {
   "prq_id": "BC-PRQ-04008",
   "text": "Name each quantity given in the stem and whether it varies."
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
    5
   ]
  },
  "skipped_steps": {
   "ex-1": [
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
   "archetype_id": "BC-QA-04009",
   "parameter_draw": {
    "anchor": 1,
    "stretch": 2,
    "far_value": 3,
    "far_slope": 5,
    "near_value": -2,
    "near_slope": -1,
    "denominator": "sine"
   },
   "completes": "ex-1",
   "stem": {
    "text": "For ex-1 the derivatives are 2f'(2x) and cos(x - 1). Evaluate the limit.",
    "command_verb": "find"
   },
   "key": {
    "form": "symbolic",
    "expr": "10"
   },
   "steps": [
    {
     "text": "2f'(2)/cos(0).",
     "expr": "2*5/cos(0)",
     "relation": "new"
    }
   ],
   "calculator_status": "no_calculator",
   "skills": [
    "BC-SKL-04036"
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
    "far_value": 0,
    "far_slope": -2,
    "near_value": 2,
    "near_slope": 4,
    "denominator": "cube"
   },
   "stem": {
    "text": "f(3) = 0, f'(3) = -2, and the form is 0/0. Find the limit of f(3x)/(x^3 - 1) as x tends to 1.",
    "command_verb": "find"
   },
   "key": {
    "form": "symbolic",
    "expr": "-2"
   },
   "steps": [
    {
     "text": "Numerator derivative.",
     "expr": "3*(-2)",
     "relation": "new"
    },
    {
     "text": "Denominator derivative.",
     "expr": "3*x**2",
     "relation": "new"
    },
    {
     "text": "At 1.",
     "expr": "3",
     "relation": "evaluate",
     "subs": {
      "x": "1"
     }
    },
    {
     "text": "Ratio.",
     "expr": "-6/3",
     "relation": "new"
    }
   ],
   "calculator_status": "no_calculator",
   "skills": [
    "BC-SKL-04035"
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
    "stretch": 3,
    "far_value": -1,
    "far_slope": 2,
    "near_value": 4,
    "near_slope": -3,
    "denominator": "linear"
   },
   "stem": {
    "text": "f(6) = -1, f'(6) = 2, f(2) = 4, f'(2) = -3. The limit of (f(3x) + 1)/(x - 2) as x tends to 2 is",
    "command_verb": "identify"
   },
   "key": {
    "form": "symbolic",
    "expr": "6"
   },
   "steps": [
    {
     "text": "3f'(6).",
     "expr": "3*2",
     "relation": "new"
    },
    {
     "text": "Over 1.",
     "expr": "6/1",
     "relation": "equivalent"
    }
   ],
   "options": [
    {
     "id": "A",
     "is_key": false,
     "expr": "-9",
     "error_path": "BC-ERR-03003",
     "derivation": "3f'(2) read in place of 3f'(6)"
    },
    {
     "id": "B",
     "is_key": false,
     "expr": "0",
     "error_path": "BC-ERR-04030",
     "derivation": "quotient rule numerator N'D - ND' evaluated at x = 2"
    },
    {
     "id": "C",
     "is_key": false,
     "expr": "2",
     "error_path": "BC-ERR-04031",
     "derivation": "chain factor 3 dropped"
    },
    {
     "id": "D",
     "is_key": true,
     "expr": "6",
     "error_path": null
    }
   ],
   "calculator_status": "no_calculator",
   "skills": [
    "BC-SKL-04035"
   ]
  }
 ],
 "delivery": [
  {
   "block": "orientation",
   "mode": "text",
   "reason": "rule 5: BC-SKL-04035, BC-SKL-04036 and BC-SKL-04037 carry BC-REP-01 only",
   "sources": [
    "BC-SKL-04035"
   ]
  },
  {
   "block": "ki-1",
   "mode": "text",
   "reason": "rule 5: a symbolic rule",
   "sources": [
    "BC-SKL-04035"
   ]
  },
  {
   "block": "ex-1",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  },
  {
   "block": "err-BC-ERR-03003",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  },
  {
   "block": "err-BC-ERR-04029",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  },
  {
   "block": "err-BC-ERR-04030",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  },
  {
   "block": "err-BC-ERR-04031",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  }
 ],
 "refresher": [
  "ki-1",
  "err-BC-ERR-03003",
  "err-BC-ERR-04029",
  "err-BC-ERR-04030",
  "err-BC-ERR-04031",
  "ex-1"
 ],
 "research_lines": [
  {
   "file": "research/units/unit-04-contextual-applications-differentiation.md",
   "line": "this is the ratio of the derivatives and not the derivative of the ratio"
  }
 ],
 "inferred": [
  {
   "claim": "The BC-ERR-04030 distractor takes the quotient rule numerator at x = 2, which is 0.",
   "settles": "Response data on chk-3 showing the value the quotient rule produces."
  },
  {
   "claim": "BC-ERR-99008 is not served because the cap of four error blocks is reached.",
   "settles": "A review of error order for BC-CON-04015."
  }
 ],
 "sources": [
  "BC-CON-04015",
  "BC-SKL-04035",
  "BC-SKL-04036",
  "BC-SKL-04037",
  "BC-EK-LIM-4A2",
  "ced:84",
  "ced:93",
  "BC-QA-04009",
  "BC-PT-99055",
  "sg-23:14",
  "cr-23:15",
  "BC-ERR-03003",
  "BC-ERR-04029",
  "BC-ERR-04030",
  "BC-ERR-04031",
  "BC-MIS-03002",
  "BC-MIS-04015",
  "BC-MIS-04016",
  "BC-PRQ-04008",
  "research/units/unit-04-contextual-applications-differentiation.md#4.7 Using L'Hospital's Rule for Determining Limits of Indeterminate Forms",
  "research/question-analysis/question-archetypes.md#BC-QA-04009 Limit of an indeterminate form with L'Hospital's rule",
  "research/scoring/notation-requirements.md#Limit notation",
  "research/exam/exam-structure.md#Section and part layout"
 ],
 "word_count": {
  "full": 532,
  "brief": 390
 },
 "read_minutes": {
  "full": 3.6,
  "brief": 2.6
 }
}
```
