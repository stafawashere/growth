---
title: LSN-CON-06005 Summation notation and the Riemann sum as a sum of products
research_date: 2026-09-29
status: designed
purpose: Authoring spec for the concept lesson on BC-CON-06005, writing and expanding a Riemann sum in sigma notation, built from authoring_bundle("BC-CON-06005") and the research files it cites.
---

# LSN-CON-06005 Summation notation and the Riemann sum as a sum of products

Concept BC-CON-06005 (skills BC-SKL-06012, BC-SKL-06013), topic 6.3 of Unit 6, loaded by one archetype, BC-QA-06014 (family riemann-limit-to-integral). Its hard parent is BC-CON-06003 (docs/lessons/unit-06/README.md, section 1).

## Prediction

One short answer question on worked example 1's own case, asked before the rule is shown: the right Riemann sum for the integral of x^2 over [2, 6] with n = 2, given the right endpoints 4 and 6, and its value. The key is 104, worked example 1's answer, which the checker verifies with SymPy. The typical wrong value adds the two values without the width (BC-ERR-06003, 52), which the error block below works. The resolution, shown on the key idea screen beside the entry, states each term as a value times the width. No verdict word. Sources: BC-CON-06005 and the topic 6.3 section the key idea cites.

## Orientation

Served text, from BC-CON-06005 `description_plain` and the topic's Assessment behaviour paragraph (research/units/unit-06-integration-accumulation.md#6.3 Riemann Sums, Summation Notation, and Definite Integral Notation): computational variants ask for an expanded sum, conceptual variants for what each factor of a term represents. No count, no frequency. The served text carries no record id.

## Key ideas

Both skills map to BC-EK-LIM-5B2, so one core block, both bands.

- ki-1 (core), BC-EK-LIM-5B2, ced:120. Paraphrase of the Riemann sum as a sum of products paragraph of Required mathematical knowledge, with the width and right endpoint for n equal pieces. Anchor quote, 21 words, found on ced:120. Notation line from the concept record.

## Recognition

BC-QA-06014 (research/question-analysis/question-archetypes.md#BC-QA-06014 Converting between a limit of Riemann sums and a definite integral). `typical_wording`: "express the given limit of a Riemann sum as a definite integral", "write the given definite integral as the limit of a Riemann sum". `common_givens`: a definite integral with stated limits, a limit of a Riemann sum in sigma notation. `asked_to_produce`: an equivalent definite integral, an equivalent limit of Riemann sums. Official examples are MCQ only: BC-MCQ-CED-006, BC-MCQ-SAMPLE-008.

This concept is the sum without the limit: the stem shows Σ, or asks to write or expand one for a stated n. Contrast pair on st-1: this stem is on BC-QA-06014, a limit of a sigma sum to write as a definite integral (`typical_wording[0]`); not this stem is a plain sigma sum with n = 4 and no limit, which asks for a number, the finite sum this lesson writes and expands. The separating feature is the limit in front.

Not this concept: "lim as n approaches infinity" in front (BC-CON-06006), or a table with a named sum (BC-CON-06003).

## Method choice

- st-1, BC-QA-06014, both bands. Cue from `asked_to_produce` and `common_givens`. Method, `expected_solution_path[0]`: separate the general term into a value and a width. Rival: BC-QA-06014 records no `wrong_approaches` or `prohibited_shortcuts`, so the rival is taken from the one error the bundle holds, values summed without the width (BC-ERR-06003), and the block carries `evidence_tag: inferred`. Separating feature: a term with no width factor is not a product. The block also carries the contrast pair above. Every field is served without the reader's own label, and record ids sit in `sources`.

## Solution path

- ex-1, BC-QA-06014, both bands, no calculator. Draw from `parameter_spec`: direction to_sum, function square, coefficient 1, start 2, width 4, convention right, letter x, so ∫_2^6 x^2 dx (derived finish 6). No published BC-QA-06014 item carries this draw.
- Steps: width 4/n (new); right endpoint 2 + 4i/n (new); the term (new); the sigma sum (new); n = 2 (evaluate, subs n = 2); 104 (equivalent). n = 2 is chosen so the width is 2, not 1, and a sum of values differs from the Riemann sum.

A fluent solver writes the sigma sum and the expansion; the width and sample point are held [inferred].

## Scoring

BC-QA-06014 lists no `point_types`, so no what_a_reader_scores entry and no point tag; the lesson says nothing about points beyond the error record's scoring_consequence (plan 15, R14). Its `scoring_pattern` records no conversion part in the 2023 to 2025 free response questions (ced:120).

## Traps

One active error meets the skills: BC-ERR-06003 (linked BC-MIS-06001, severity high). Both bands.

- err-BC-ERR-06003, on ex-1's draw at n = 2: 4^2 + 6^2 against 2(4^2) + 2(6^2). Possible reason, words from BC-MIS-06001.

## Representations

None. The topic's conversion is symbolic to symbolic (BC-REP-01 to BC-REP-01), carried by ex-1's steps.

## Prerequisite bridge

- BC-PRQ-06006, from its `description_plain` (index, limits, general term) and `failure_signature` (index substituted wrongly, off by one).

## Time

BC-QA-06014 is `no_calculator` with no FRQ part recorded, so Section I Part A, 2.14 minutes per question (research/exam/exam-structure.md#Section and part layout). The minutes go on the width and the sample point; the expansion for a small n is short.

## Checks

- chk-1, completion of ex-1, both bands: the n = 2 sum given; key 104.
- chk-2, isomorph, both bands. Draw: to_sum, cube, coefficient 2, start 1, width 4, left, t, so ∫_1^5 2t^3 dt; at n = 2 the key is 112.

Two checks only: the bundle holds one error, so an MCQ with three error-path distractors cannot be built (inferred array).

## Delivery

- orientation, ki-1: text. Rule 6, BC-REP-01 only (unit README section 6).
- ex-1, err-BC-ERR-06003: step_reveal. Rule 1. The error block is a fix prompt (`distinct`).
- prediction: text, no delivery entry.

No drawn block. The skills carry BC-REP-01 only (topic 6.3 Representations paragraph: symbolic to symbolic) and the key idea states a rule about terms, so none of rules 2 to 5 applies. The machine record states `no_figure_reason`.

## Band plan

- Low (full), in served order: prediction, orientation, the bridge, ki-1, st-1 with its contrast pair, ex-1, chk-1, the error block, chk-2. 440 words, 3.0 minutes (cap 900 and 6). There is one example, so nothing is faded.
- Mid (brief): the same blocks. 440 words, 3.0 minutes (cap 450 and 3).
- Refresher: ki-1, err-BC-ERR-06003, ex-1.

## Sources

- BC-CON-06005; BC-SKL-06012, BC-SKL-06013; BC-EK-LIM-5B2; ced:120
- BC-QA-06014
- BC-ERR-06003; BC-MIS-06001
- BC-PRQ-06006
- research/units/unit-06-integration-accumulation.md#6.3 Riemann Sums, Summation Notation, and Definite Integral Notation
- research/question-analysis/question-archetypes.md#BC-QA-06014 Converting between a limit of Riemann sums and a definite integral
- research/exam/exam-structure.md#Section and part layout
- [inferred] Two checks for want of errors. Settled by more active BC-ERR on these skills.
- [inferred] The rival from BC-ERR-06003. Settled by wrong_approaches on BC-QA-06014.
- [inferred] I-A for an archetype with no FRQ part. Settled by a conversion rubric.
- [inferred] The function label read as a formula. Settled by a formula template in the parameter_spec.
- [inferred] Which steps a fluent solver holds. Settled by timing data per step.

## Machine record

```json
{
 "id": "LSN-CON-06005",
 "kind": "concept",
 "target_id": "BC-CON-06005",
 "unit": "06",
 "skills": [
  "BC-SKL-06012",
  "BC-SKL-06013"
 ],
 "prediction": {
  "id": "pr-1",
  "stem": {
   "text": "The right Riemann sum for ∫_2^6 x^2 dx with n = 2 equal pieces has right endpoints 4 and 6. What is its value?",
   "command_verb": "predict"
  },
  "format": "short_answer",
  "key": {
   "form": "numeric",
   "expr": "104"
  },
  "resolution": "Each term is a value times the width 2: 2(4^2) + 2(6^2) = 104.",
  "sources": [
   "BC-CON-06005",
   "research/units/unit-06-integration-accumulation.md#6.3 Riemann Sums, Summation Notation, and Definite Integral Notation"
  ]
 },
 "no_figure_reason": "The skills carry only symbolic representations and the key idea states a rule about terms, each a value times a width. No figure-bearing representation is in play and no process is described.",
 "orientation": {
  "text": "Sigma notation writes a Riemann sum as a sum of products. A response writes each term as the function at a sample point times the width, and can expand the sum term by term.",
  "sources": [
   "BC-CON-06005",
   "research/units/unit-06-integration-accumulation.md#6.3 Riemann Sums, Summation Notation, and Definite Integral Notation"
  ]
 },
 "key_ideas": [
  {
   "id": "ki-1",
   "ek_id": "BC-EK-LIM-5B2",
   "depth": "core",
   "text": "A Riemann sum needs a partition. Each term is a height times a width: f at the ith sample point times the ith width. For n equal pieces of [a, b] the width is (b - a)/n and the right endpoint is a + i(b - a)/n.",
   "notation": "sigma from i = 1 to n",
   "quote": {
    "text": "each of which is the value of the function at a point in a subinterval multiplied by the length of that subinterval",
    "source": "ced:120"
   },
   "sources": [
    "BC-EK-LIM-5B2",
    "ced:120",
    "research/units/unit-06-integration-accumulation.md#6.3 Riemann Sums, Summation Notation, and Definite Integral Notation"
   ]
  }
 ],
 "strategy": [
  {
   "id": "st-1",
   "archetype_id": "BC-QA-06014",
   "cue": "A definite integral with limits, or a sigma sum; the other form asked.",
   "method": "Separate the general term into a value and a width.",
   "rival": "The values summed with the width left out.",
   "separating_feature": "A term with no width factor is not a product, so not a Riemann sum.",
   "sources": [
    "BC-QA-06014"
   ],
   "evidence_tag": "inferred",
   "contrast": {
    "this": {
     "text": "Write lim as n → ∞ of Σ (1 + 4i/n)^2 (4/n) as a definite integral.",
     "archetype_id": "BC-QA-06014"
    },
    "not_this": {
     "text": "Evaluate Σ_{i=1}^{4} (1 + i)^2, the right sum for ∫_1^5 x^2 dx with n = 4.",
     "why_not": "No limit: add four terms to get a number."
    },
    "feature": "lim as n → ∞ in front."
   }
  }
 ],
 "worked_examples": [
  {
   "id": "ex-1",
   "archetype_id": "BC-QA-06014",
   "bands": [
    "low",
    "mid"
   ],
   "parameter_draw": {
    "direction": "to_sum",
    "function": "square",
    "coefficient": 1,
    "start": 2,
    "width": 4,
    "convention": "right",
    "letter": "x"
   },
   "problem": {
    "text": "Write the right Riemann sum for ∫_2^6 x^2 dx with n equal subintervals in sigma notation. Expand and evaluate it for n = 2.",
    "command_verb": "write"
   },
   "calculator_status": "no_calculator",
   "steps": [
    {
     "cue": "Interval length 4, n pieces.",
     "why": "Equal widths.",
     "expr": "4/n",
     "relation": "new"
    },
    {
     "cue": "Right endpoint of the ith piece.",
     "why": "Start 2, i widths along.",
     "expr": "2 + 4*i/n",
     "relation": "new"
    },
    {
     "cue": "Term: value times width.",
     "why": "A product, not a value alone.",
     "expr": "(2 + 4*i/n)**2*(4/n)",
     "relation": "new"
    },
    {
     "cue": "Sum i = 1 to n.",
     "why": "One term per piece.",
     "expr": "Sum((2 + 4*i/n)**2*(4/n), (i, 1, n))",
     "relation": "new"
    },
    {
     "cue": "n = 2: width 2, endpoints 4 and 6.",
     "why": "Two terms.",
     "expr": "2*4**2 + 2*6**2",
     "relation": "evaluate",
     "subs": {
      "n": "2"
     }
    },
    {
     "cue": "Add.",
     "why": "32 + 72.",
     "expr": "104",
     "relation": "equivalent"
    }
   ],
   "answer": {
    "form": "numeric",
    "expr": "104"
   }
  }
 ],
 "what_a_reader_scores": [],
 "common_errors": [
  {
   "error_id": "BC-ERR-06003",
   "observed_behavior": "The response adds the tabulated rate values without multiplying each by a subinterval width.",
   "scoring_consequence": "Neither the form point nor the answer point is earned because no products appear.",
   "wrong_step": {
    "text": "Values added: 4^2 + 6^2.",
    "expr": "4**2 + 6**2"
   },
   "right_step": {
    "text": "Each times width 2.",
    "expr": "2*4**2 + 2*6**2"
   },
   "relation": "distinct",
   "fix_prompt": true,
   "possible_reason": {
    "misconception_id": "BC-MIS-06001",
    "text": "treats a Riemann sum as an operation on the list of function values alone, so the partition widths play no role"
   },
   "sources": [
    "BC-ERR-06003",
    "BC-MIS-06001"
   ]
  }
 ],
 "representations": null,
 "prerequisite_bridges": [
  {
   "prq_id": "BC-PRQ-06006",
   "text": "Sigma notation: the index runs from the lower to the upper limit, one term each. Substitute the index correctly; n terms, not n + 1."
  }
 ],
 "time": {
  "exam_part": "I-A",
  "budget_minutes": 2.14,
  "source": "research/exam/exam-structure.md#Section and part layout",
  "written_steps": {
   "ex-1": [
    4,
    5,
    6
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
   "archetype_id": "BC-QA-06014",
   "parameter_draw": {
    "direction": "to_sum",
    "function": "square",
    "coefficient": 1,
    "start": 2,
    "width": 4,
    "convention": "right",
    "letter": "x"
   },
   "completes": "ex-1",
   "stem": {
    "text": "For n = 2 the sum is Σ_(i=1)^2 (2 + 2i)^2 (2). Expand and evaluate.",
    "command_verb": "evaluate"
   },
   "key": {
    "form": "numeric",
    "expr": "104"
   },
   "steps": [
    {
     "text": "The sum at n = 2.",
     "expr": "Sum((2 + 2*i)**2*2, (i, 1, 2))",
     "relation": "new"
    },
    {
     "text": "Expand.",
     "expr": "2*4**2 + 2*6**2",
     "relation": "equivalent"
    },
    {
     "text": "Add.",
     "expr": "104",
     "relation": "equivalent"
    }
   ],
   "calculator_status": "no_calculator",
   "skills": [
    "BC-SKL-06012"
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
   "archetype_id": "BC-QA-06014",
   "parameter_draw": {
    "direction": "to_sum",
    "function": "cube",
    "coefficient": 2,
    "start": 1,
    "width": 4,
    "convention": "left",
    "letter": "t"
   },
   "stem": {
    "text": "Write the left Riemann sum for ∫_1^5 2t^3 dt with n equal pieces in sigma notation; evaluate it for n = 2.",
    "command_verb": "write"
   },
   "key": {
    "form": "numeric",
    "expr": "112"
   },
   "steps": [
    {
     "text": "Width 4/n, left endpoint 1 + 4(i - 1)/n.",
     "expr": "Sum(2*(1 + 4*(i - 1)/n)**3*(4/n), (i, 1, n))",
     "relation": "new"
    },
    {
     "text": "n = 2: endpoints 1 and 3, width 2.",
     "expr": "2*1**3*2 + 2*3**3*2",
     "relation": "evaluate",
     "subs": {
      "n": "2"
     }
    },
    {
     "text": "Add.",
     "expr": "112",
     "relation": "equivalent"
    }
   ],
   "calculator_status": "no_calculator",
   "skills": [
    "BC-SKL-06013"
   ]
  }
 ],
 "delivery": [
  {
   "block": "orientation",
   "mode": "text",
   "reason": "rule 6: BC-REP-01 only on BC-SKL-06012 and BC-SKL-06013 (unit README delivery map)",
   "sources": [
    "BC-SKL-06012",
    "BC-SKL-06013"
   ]
  },
  {
   "block": "ki-1",
   "mode": "text",
   "reason": "rule 6: a symbolic rule with BC-REP-01 givens",
   "sources": [
    "BC-SKL-06012",
    "BC-SKL-06013"
   ]
  },
  {
   "block": "ex-1",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  },
  {
   "block": "err-BC-ERR-06003",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  }
 ],
 "refresher": [
  "ki-1",
  "err-BC-ERR-06003",
  "ex-1"
 ],
 "research_lines": [
  {
   "file": "research/units/unit-06-integration-accumulation.md",
   "line": "A Riemann sum requires a partition of an interval and is the sum of products, each the value of the function at a point in a subinterval multiplied by the length of that subinterval (BC-EK-LIM-5B2)."
  }
 ],
 "inferred": [
  {
   "claim": "The bundle holds one error for this concept, BC-ERR-06003, so the lesson carries two checks and no MCQ.",
   "settles": "A second and third active BC-ERR on BC-SKL-06012 or BC-SKL-06013, such as an off-by-one index or a sample point for the wrong convention (BC-PRQ-06006 failure_signature)."
  },
  {
   "claim": "The rival, values summed without the width, is taken from BC-ERR-06003; BC-QA-06014 has no wrong_approaches or prohibited_shortcuts.",
   "settles": "wrong_approaches on BC-QA-06014."
  },
  {
   "claim": "BC-QA-06014 has no FRQ part recorded, so the time part is I-A.",
   "settles": "A free response rubric with a conversion part."
  },
  {
   "claim": "Reading the function label: square with coefficient 1 is taken as x^2 and cube with coefficient 2 as 2t^3.",
   "settles": "An explicit formula template in BC-QA-06014's parameter_spec."
  },
  {
   "claim": "A fluent solver writes the sigma sum and its expansion and holds the width and sample point.",
   "settles": "Timing data per step once the fluency telemetry exists."
  }
 ],
 "sources": [
  "BC-CON-06005",
  "BC-SKL-06012",
  "BC-SKL-06013",
  "BC-EK-LIM-5B2",
  "ced:120",
  "BC-QA-06014",
  "BC-ERR-06003",
  "BC-MIS-06001",
  "BC-PRQ-06006",
  "research/units/unit-06-integration-accumulation.md#6.3 Riemann Sums, Summation Notation, and Definite Integral Notation",
  "research/question-analysis/question-archetypes.md#BC-QA-06014 Converting between a limit of Riemann sums and a definite integral",
  "research/exam/exam-structure.md#Section and part layout",
  "research/scoring/common-point-losses.md#Setup points"
 ],
 "read_minutes": {
  "full": 3.0,
  "brief": 3.0
 },
 "word_count": {
  "full": 439,
  "brief": 439
 }
}
```
