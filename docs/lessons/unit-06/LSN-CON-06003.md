---
title: LSN-CON-06003 Riemann sum approximation of a definite integral
research_date: 2026-09-29
status: designed
purpose: Authoring spec for the concept lesson on BC-CON-06003, left, right, midpoint and trapezoidal sums over a given partition, built from authoring_bundle("BC-CON-06003") and the research files it cites.
---

# LSN-CON-06003 Riemann sum approximation of a definite integral

Concept BC-CON-06003 (skills BC-SKL-06005 to BC-SKL-06009), topic 6.2 of Unit 6, loaded by BC-QA-06001, BC-QA-06002 and BC-QA-06017 (family integral-approximation). Its hard parent is BC-CON-06001 (docs/lessons/unit-06/README.md, section 1).

## Orientation

Served text, from BC-CON-06003 `description_plain` and the topic's Assessment behaviour paragraph (research/units/unit-06-integration-accumulation.md#6.2 Approximating Areas with Riemann Sums): FRQ forms ask for a left, right or trapezoidal sum over the subintervals the data indicate. No count, no frequency.

## Key ideas

Three BC-EK across five skills; at most two may be core, and one is chosen to hold the brief band.

- ki-1 (core), BC-EK-LIM-5A2 (every skill), ced:119. Paraphrase of the Riemann sum and Trapezoidal sum paragraphs of Required mathematical knowledge. No quote: the LIM-5.A.2 sentence runs past 25 words.
- ki-2 (extended), BC-EK-LIM-5A1 (BC-SKL-06005, 06006, 06009), ced:119, with the LIM-5.A.1 sentence as anchor quote.
- ki-3 (extended), BC-EK-LIM-5A3 (BC-SKL-06009), ced:119, with the LIM-5.A.3 sentence as anchor quote.

Each carries the concept notation line. The Error direction paragraph belongs to BC-CON-06004.

## Recognition

Three archetypes in one family, integral-approximation.

- BC-QA-06001 (research/question-analysis/question-archetypes.md#BC-QA-06001 Riemann sum from a table with over or under estimate reasoning): `common_givens` a table of rate values at selected times, the subintervals indicated by the table; `asked_to_produce` a left, right, or midpoint Riemann sum with every product shown, a numerical approximation. Official examples include BC-FRQ-2021-Q1-B, BC-FRQ-2023-Q1-A, BC-FRQ-2024-Q1-B.
- BC-QA-06002 (research/question-analysis/question-archetypes.md#BC-QA-06002 Trapezoidal approximation of an accumulated amount from a table): `common_givens` a table at unevenly spaced inputs; `asked_to_produce` a trapezoidal sum with each term shown. Official examples BC-FRQ-2014-Q4-C, BC-FRQ-2025-Q3-C, BC-FRQ-2018-Q4-C.
- BC-QA-06017 (research/question-analysis/question-archetypes.md#BC-QA-06017 Riemann or trapezoidal sum with equal subintervals for a function given by a formula or a graph): `common_givens` a formula or a graph of segments, the interval, the number of subintervals; `typical_wording` "use a midpoint Riemann sum with four subintervals of equal width".

The signal: "approximate" beside a named sum and a table or a stated n. Not this concept: "is it an over or under estimate" (BC-CON-06004), a sigma expression (BC-CON-06005), "lim" in front of the sum (BC-CON-06006).

## Method choice

One strategy block, since all three archetypes share the family integral-approximation [inferred].

- st-1. Method, BC-QA-06001 `expected_solution_path[0]`: identify the subintervals indicated by the table. Rival from `wrong_approaches`: one common width on unevenly spaced data (BC-ERR-06001). Separating feature: unequal gaps between inputs. For BC-QA-06002 the first line is each trapezoid as the average of two end values times the width; for BC-QA-06017 the common width first. The cue rests on `common_givens` and `asked_to_produce`, so the block is not tagged inferred.

## Solution path

- ex-1, BC-QA-06001, both bands, calculator. Draw: gaps 2, 1, 3, 2, even_gap 2, rates 6, 10, 13, 9, 4, endpoint left, context tank, spacing nonuniform, framing context; derived left_sum 79, right_sum 68, left_values 38, third_option 76, all distinct. Steps: subintervals (no value); the products (new, BC-PT-99018); 79 (equivalent, BC-PT-99019).
- ex-2, BC-QA-06002, low band, no calculator. Draw: gaps 4, 2, 6, rates 5, 9, 11, 7, initial 40, context rain, ask integral; derived trapezoid 102. Steps: the three halved terms (new, BC-PT-99018); 102 (equivalent, BC-PT-99019).

No published item carries either draw. A fluent solver writes every product and the value; reading the widths off the table is held in the head (unit README section 5) [inferred].

## Scoring

Both archetypes list BC-PT-99018 and BC-PT-99019; each example tags the product line with 99018 and the value with 99019, and each checklist is `reader_checks(["BC-PT-99018", "BC-PT-99019"])` copied exactly. For the author: a bare value earns neither point (sg-23:3); bare values or a uniform width on unequal data lose the setup point (research/scoring/common-point-losses.md#Setup points); an equals sign is read as approximately equal for the form point (research/scoring/notation-requirements.md#The equal sign).

## Traps

Six active errors meet the skills; the first four in the bundle's order are shown (cap 4): BC-ERR-06001, BC-ERR-06002, BC-ERR-06003, BC-ERR-06004. BC-ERR-99028 and BC-ERR-99034 are left out by the cap. Low band all four, mid band the first two. All on ex-1's table.

- err-BC-ERR-06001: 2(6 + 10 + 13 + 9) against the products with widths 2, 1, 3, 2. No reason line, to hold the brief band.
- err-BC-ERR-06002: right-end values against left. No reason line, same reason.
- err-BC-ERR-06003: 6 + 10 + 13 + 9 against the products. Possible reason, words from BC-MIS-06001.
- err-BC-ERR-06004: the same table as trapezoids with only the first halved. Possible reason, words from BC-MIS-06004.

## Representations

None as a separate block. The topic's conversions (table to value, graph to value) are carried by the orientation table, ki-1's panels and ki-2's table.

## Prerequisite bridge

- BC-PRQ-06005 (evaluation at a stated input), BC-PRQ-06007 (area formulas), BC-PRQ-06012 (widths as differences of consecutive inputs), each from its `description_plain` and `failure_signature`.

## Time

BC-QA-06001 is `calculator` and its scored form is a free response part, so Section II Part A, 15.0 minutes per question (research/exam/exam-structure.md#Section and part layout); the two-point part is a 3.33 minute share [inferred]. As an MCQ it takes the Part B 2.92. The minutes go on writing each product; the arithmetic is short.

## Checks

- chk-1, completion of ex-1, both bands: the products given; key 79.
- chk-2, isomorph, both bands. Draw: gaps 1, 3, 2, 2, even_gap 1, rates 2, 7, 5, 11, 8, right, download, nonuniform, context. Key 60.
- chk-3, MCQ, low band. Draw: gaps 3, 1, 2, 2, even_gap 2, rates 5, 8, 14, 9, 3, left, traffic, nonuniform, bare. Key 69 (chosen_sum). Distractors from the spec's own derived values: 36 (BC-ERR-06003), 62 (BC-ERR-06002), 72 (BC-ERR-06001).

## Delivery

- orientation: table. Rule 5, BC-REP-03 (unit README section 6).
- ki-1: figure, four panels at one n. Rule 4, BC-REP-02 on BC-SKL-06007 and 06009.
- ki-2: table. Rule 5.
- ki-3: text. Rule 6.
- ex-1, ex-2 and the four error blocks: step_reveal. Rule 1.

Every non-text choice is [inferred]; settled by the modality A/B.

## Band plan

- Low (full): orientation, ki-1 to ki-3, st-1, ex-1 and ex-2 with their reader lines, four error blocks, chk-1 to chk-3, three bridges. 851 words, 5.7 minutes (cap 900 and 6).
- Mid (brief): orientation, ki-1, st-1, ex-1 with its reader lines, err-BC-ERR-06001, err-BC-ERR-06002, chk-1, chk-2, three bridges. 447 words, 3.0 minutes (cap 450 and 3).
- Refresher: ki-1, the four error blocks, ex-1.

## Sources

- BC-CON-06003; BC-SKL-06005 to BC-SKL-06009; BC-EK-LIM-5A1, 5A2, 5A3; ced:119
- BC-QA-06001, BC-QA-06002, BC-QA-06017; BC-PT-99018, BC-PT-99019; sg-23:2, sg-23:3, sg-25:13
- BC-ERR-06001, BC-ERR-06002, BC-ERR-06003, BC-ERR-06004; BC-MIS-06001, BC-MIS-06004
- BC-PRQ-06005, BC-PRQ-06007, BC-PRQ-06012
- research/units/unit-06-integration-accumulation.md#6.2 Approximating Areas with Riemann Sums
- research/question-analysis/question-archetypes.md#BC-QA-06001 Riemann sum from a table with over or under estimate reasoning
- research/question-analysis/question-archetypes.md#BC-QA-06002 Trapezoidal approximation of an accumulated amount from a table
- research/question-analysis/question-archetypes.md#BC-QA-06017 Riemann or trapezoidal sum with equal subintervals for a function given by a formula or a graph
- research/exam/exam-structure.md#Section and part layout
- research/scoring/common-point-losses.md#Setup points
- research/scoring/notation-requirements.md#The equal sign
- [inferred] One strategy block for the family. Settled by a ruling on per-family blocks.
- [inferred] The 3.33 minute share. Settled by timing data per step.
- [inferred] Units for the context labels. Settled by a units field in the parameter_spec.
- [inferred] Every non-text delivery mode. Settled by the modality A/B.

## Machine record

```json
{
 "id": "LSN-CON-06003",
 "kind": "concept",
 "target_id": "BC-CON-06003",
 "unit": "06",
 "skills": [
  "BC-SKL-06005",
  "BC-SKL-06006",
  "BC-SKL-06007",
  "BC-SKL-06008",
  "BC-SKL-06009"
 ],
 "orientation": {
  "text": "A response estimates the integral as a sum of value times width over the given subintervals, writes every product, then the value.",
  "sources": [
   "BC-CON-06003",
   "research/units/unit-06-integration-accumulation.md#6.2 Approximating Areas with Riemann Sums"
  ]
 },
 "key_ideas": [
  {
   "id": "ki-1",
   "ek_id": "BC-EK-LIM-5A2",
   "depth": "core",
   "text": "Each subinterval gives width times one height. Left, right and midpoint differ only in the sample point; a trapezoid averages the two end values. Widths may be unequal.",
   "notation": "L sub n, R sub n, M sub n, T sub n",
   "quote": null,
   "sources": [
    "BC-EK-LIM-5A2",
    "ced:119",
    "research/units/unit-06-integration-accumulation.md#6.2 Approximating Areas with Riemann Sums"
   ]
  },
  {
   "id": "ki-2",
   "ek_id": "BC-EK-LIM-5A1",
   "depth": "extended",
   "text": "A table, a graph, a formula or a description can each supply the heights; the partition supplies the widths.",
   "notation": "L sub n, R sub n, M sub n, T sub n",
   "quote": {
    "text": "Definite integrals can be approximated for functions that are represented graphically, numerically, analytically, and verbally.",
    "source": "ced:119"
   },
   "sources": [
    "BC-EK-LIM-5A1",
    "ced:119",
    "research/units/unit-06-integration-accumulation.md#6.2 Approximating Areas with Riemann Sums"
   ]
  },
  {
   "id": "ki-3",
   "ek_id": "BC-EK-LIM-5A3",
   "depth": "extended",
   "text": "The sum is computed by hand or on a calculator; either way the products are written before the value (sg-23:3).",
   "notation": "L sub n, R sub n, M sub n, T sub n",
   "quote": {
    "text": "Definite integrals can be approximated using numerical methods, with or without technology.",
    "source": "ced:119"
   },
   "sources": [
    "BC-EK-LIM-5A3",
    "ced:119",
    "sg-23:3",
    "research/units/unit-06-integration-accumulation.md#6.2 Approximating Areas with Riemann Sums"
   ]
  }
 ],
 "strategy": [
  {
   "id": "st-1",
   "archetype_id": "BC-QA-06001",
   "cue": "A table of rate values and a named sum over the subintervals the table indicates.",
   "method": "Identify the subintervals and their widths from the table.",
   "rival": "Rival: one common width on unevenly spaced data.",
   "separating_feature": "Unequal gaps between inputs mean unequal widths.",
   "sources": [
    "BC-QA-06001",
    "BC-QA-06002",
    "BC-QA-06017"
   ],
   "evidence_tag": "verified"
  }
 ],
 "worked_examples": [
  {
   "id": "ex-1",
   "archetype_id": "BC-QA-06001",
   "bands": [
    "low",
    "mid"
   ],
   "parameter_draw": {
    "gaps": [
     2,
     1,
     3,
     2
    ],
    "even_gap": 2,
    "rates": [
     6,
     10,
     13,
     9,
     4
    ],
    "endpoint": "left",
    "context": "tank",
    "spacing": "nonuniform",
    "framing": "context"
   },
   "problem": {
    "text": "Water enters a tank at R(t) gallons per hour. t: 0, 2, 3, 6, 8; R(t): 6, 10, 13, 9, 4. Approximate ∫_0^8 R(t) dt by a left Riemann sum on these subintervals.",
    "command_verb": "approximate"
   },
   "calculator_status": "calculator",
   "steps": [
    {
     "cue": "Table inputs fix the subintervals.",
     "why": "Widths 2, 1, 3, 2."
    },
    {
     "cue": "Left sum: left-end values 6, 10, 13, 9.",
     "why": "Each times its own width.",
     "expr": "2*6 + 1*10 + 3*13 + 2*9",
     "relation": "new",
     "point_type_id": "BC-PT-99018"
    },
    {
     "cue": "Add.",
     "why": "The value with products shown.",
     "expr": "79",
     "relation": "equivalent",
     "point_type_id": "BC-PT-99019"
    }
   ],
   "answer": {
    "form": "numeric",
    "expr": "79"
   }
  },
  {
   "id": "ex-2",
   "archetype_id": "BC-QA-06002",
   "bands": [
    "low"
   ],
   "parameter_draw": {
    "gaps": [
     4,
     2,
     6
    ],
    "rates": [
     5,
     9,
     11,
     7
    ],
    "initial": 40,
    "context": "rain",
    "ask": "integral"
   },
   "problem": {
    "text": "Rain falls at r(t) millimetres per hour. t: 0, 4, 6, 12; r(t): 5, 9, 11, 7. Approximate ∫_0^12 r(t) dt with a trapezoidal sum on these subintervals.",
    "command_verb": "approximate"
   },
   "calculator_status": "no_calculator",
   "steps": [
    {
     "cue": "Trapezoidal: average of the two end values times the width.",
     "why": "Widths 4, 2, 6, the half in every term.",
     "expr": "4*(5 + 9)/2 + 2*(9 + 11)/2 + 6*(11 + 7)/2",
     "relation": "new",
     "point_type_id": "BC-PT-99018"
    },
    {
     "cue": "Add.",
     "why": "28 + 20 + 54.",
     "expr": "102",
     "relation": "equivalent",
     "point_type_id": "BC-PT-99019"
    }
   ],
   "answer": {
    "form": "numeric",
    "expr": "102"
   }
  }
 ],
 "what_a_reader_scores": [
  {
   "example_id": "ex-1",
   "point_type_ids": [
    "BC-PT-99018",
    "BC-PT-99019"
   ],
   "lines": [
    {
     "point_type_id": "BC-PT-99018",
     "text": "Form of a Riemann or trapezoidal sum. Earned by: A sum whose terms each show a value factor and a width factor, with at least five of the six factors correct for three subintervals (sg-25:13, sg-26:3, sg-23:2) or seven of eight for four subintervals (sg-22:15). Not earned by: A left or right sum where a midpoint or trapezoidal sum was asked for (sg-26:3, sg-25:13); an unsupported total (sg-26:3, sg-22:15). Notation: sg-25:13 and sg-26:3 instruct readers to read an equals sign as approximately equal for this point."
    },
    {
     "point_type_id": "BC-PT-99019",
     "text": "Approximation value supported by the sum. Earned by: The numerical value of the sum with the supporting products present (sg-25:13, sg-23:2). Not earned by: The value alone with no work (sg-26:3, sg-22:15, sg-23:2)."
    }
   ]
  },
  {
   "example_id": "ex-2",
   "point_type_ids": [
    "BC-PT-99018",
    "BC-PT-99019"
   ],
   "lines": [
    {
     "point_type_id": "BC-PT-99018",
     "text": "Form of a Riemann or trapezoidal sum. Earned by: A sum whose terms each show a value factor and a width factor, with at least five of the six factors correct for three subintervals (sg-25:13, sg-26:3, sg-23:2) or seven of eight for four subintervals (sg-22:15). Not earned by: A left or right sum where a midpoint or trapezoidal sum was asked for (sg-26:3, sg-25:13); an unsupported total (sg-26:3, sg-22:15). Notation: sg-25:13 and sg-26:3 instruct readers to read an equals sign as approximately equal for this point."
    },
    {
     "point_type_id": "BC-PT-99019",
     "text": "Approximation value supported by the sum. Earned by: The numerical value of the sum with the supporting products present (sg-25:13, sg-23:2). Not earned by: The value alone with no work (sg-26:3, sg-22:15, sg-23:2)."
    }
   ]
  }
 ],
 "common_errors": [
  {
   "error_id": "BC-ERR-06001",
   "observed_behavior": "The response multiplies every tabulated value by one common width although the table inputs are unevenly spaced.",
   "scoring_consequence": "The form point is lost because more than one of the six factors is incorrect, and the answer point is lost with it.",
   "wrong_step": {
    "text": "Width 2 for all.",
    "expr": "2*(6 + 10 + 13 + 9)"
   },
   "right_step": {
    "text": "Widths 2, 1, 3, 2.",
    "expr": "2*6 + 1*10 + 3*13 + 2*9"
   },
   "relation": "distinct",
   "possible_reason": null,
   "sources": [
    "BC-ERR-06001"
   ]
  },
  {
   "error_id": "BC-ERR-06002",
   "observed_behavior": "A completely correct Riemann sum is built with left endpoints when right endpoints were requested, or the reverse.",
   "scoring_consequence": "A completely correct sum of the wrong type earns one of the two remaining points in 2023 and the form point only in 2025 (sg-23:3, sg-25:13).",
   "wrong_step": {
    "text": "Right ends used.",
    "expr": "2*10 + 1*13 + 3*9 + 2*4"
   },
   "right_step": {
    "text": "Left ends.",
    "expr": "2*6 + 1*10 + 3*13 + 2*9"
   },
   "relation": "distinct",
   "possible_reason": null,
   "sources": [
    "BC-ERR-06002"
   ]
  },
  {
   "error_id": "BC-ERR-06003",
   "observed_behavior": "The response adds the tabulated rate values without multiplying each by a subinterval width.",
   "scoring_consequence": "Neither the form point nor the answer point is earned because no products appear.",
   "wrong_step": {
    "text": "Values added, no widths.",
    "expr": "6 + 10 + 13 + 9"
   },
   "right_step": {
    "text": "Each value times its width.",
    "expr": "2*6 + 1*10 + 3*13 + 2*9"
   },
   "relation": "distinct",
   "possible_reason": {
    "misconception_id": "BC-MIS-06001",
    "text": "treats a Riemann sum as an operation on the list of function values alone, so the partition widths play no role"
   },
   "sources": [
    "BC-ERR-06003",
    "BC-MIS-06001"
   ]
  },
  {
   "error_id": "BC-ERR-06004",
   "observed_behavior": "One or two trapezoid terms are halved and the remaining term is not.",
   "scoring_consequence": "At least one of the six factors is incorrect, so the form point may survive but the answer point is lost (sg-25:13).",
   "wrong_step": {
    "text": "Same table, trapezoids: only the first halved.",
    "expr": "2*(6 + 10)/2 + 1*(10 + 13) + 3*(13 + 9) + 2*(9 + 4)"
   },
   "right_step": {
    "text": "Every term halved.",
    "expr": "2*(6 + 10)/2 + 1*(10 + 13)/2 + 3*(13 + 9)/2 + 2*(9 + 4)/2"
   },
   "relation": "distinct",
   "possible_reason": {
    "misconception_id": "BC-MIS-06004",
    "text": "averages across the entire interval rather than forming a separate trapezoid on each subinterval"
   },
   "sources": [
    "BC-ERR-06004",
    "BC-MIS-06004"
   ]
  }
 ],
 "representations": null,
 "prerequisite_bridges": [
  {
   "prq_id": "BC-PRQ-06005",
   "text": "A value read from the wrong row changes a factor."
  },
  {
   "prq_id": "BC-PRQ-06007",
   "text": "A trapezoid's area averages its parallel sides; it is not a rectangle."
  },
  {
   "prq_id": "BC-PRQ-06012",
   "text": "Each width is a difference of consecutive inputs, not one common width."
  }
 ],
 "time": {
  "exam_part": "II-A",
  "budget_minutes": 15.0,
  "source": "research/exam/exam-structure.md#Section and part layout",
  "written_steps": {
   "ex-1": [
    2,
    3
   ],
   "ex-2": [
    1,
    2
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
   "archetype_id": "BC-QA-06001",
   "parameter_draw": {
    "gaps": [
     2,
     1,
     3,
     2
    ],
    "even_gap": 2,
    "rates": [
     6,
     10,
     13,
     9,
     4
    ],
    "endpoint": "left",
    "context": "tank",
    "spacing": "nonuniform",
    "framing": "context"
   },
   "completes": "ex-1",
   "stem": {
    "text": "The left sum is 2(6) + 1(10) + 3(13) + 2(9). Give its value.",
    "command_verb": "find"
   },
   "key": {
    "form": "numeric",
    "expr": "79"
   },
   "steps": [
    {
     "text": "The products.",
     "expr": "2*6 + 1*10 + 3*13 + 2*9",
     "relation": "new"
    },
    {
     "text": "Add.",
     "expr": "79",
     "relation": "equivalent"
    }
   ],
   "calculator_status": "calculator",
   "skills": [
    "BC-SKL-06005"
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
   "archetype_id": "BC-QA-06001",
   "parameter_draw": {
    "gaps": [
     1,
     3,
     2,
     2
    ],
    "even_gap": 1,
    "rates": [
     2,
     7,
     5,
     11,
     8
    ],
    "endpoint": "right",
    "context": "download",
    "spacing": "nonuniform",
    "framing": "context"
   },
   "stem": {
    "text": "t: 0, 1, 4, 6, 8; D(t): 2, 7, 5, 11, 8. Right Riemann sum for ∫_0^8 D(t) dt?",
    "command_verb": "approximate"
   },
   "key": {
    "form": "numeric",
    "expr": "60"
   },
   "steps": [
    {
     "text": "Right ends times widths 1, 3, 2, 2.",
     "expr": "1*7 + 3*5 + 2*11 + 2*8",
     "relation": "new"
    },
    {
     "text": "Add.",
     "expr": "60",
     "relation": "equivalent"
    }
   ],
   "calculator_status": "calculator",
   "skills": [
    "BC-SKL-06006"
   ]
  },
  {
   "id": "chk-3",
   "check_kind": "mcq",
   "format": "mcq",
   "bands": [
    "low"
   ],
   "archetype_id": "BC-QA-06001",
   "parameter_draw": {
    "gaps": [
     3,
     1,
     2,
     2
    ],
    "even_gap": 2,
    "rates": [
     5,
     8,
     14,
     9,
     3
    ],
    "endpoint": "left",
    "context": "traffic",
    "spacing": "nonuniform",
    "framing": "bare"
   },
   "stem": {
    "text": "t: 0, 3, 4, 6, 8; f(t): 5, 8, 14, 9, 3. Which is the left Riemann sum for ∫_0^8 f(t) dt on these subintervals?",
    "command_verb": "identify"
   },
   "key": {
    "form": "numeric",
    "expr": "69"
   },
   "steps": [
    {
     "text": "Left ends times widths 3, 1, 2, 2.",
     "expr": "3*5 + 1*8 + 2*14 + 2*9",
     "relation": "new"
    },
    {
     "text": "Add.",
     "expr": "69",
     "relation": "equivalent"
    }
   ],
   "options": [
    {
     "id": "A",
     "is_key": false,
     "expr": "36",
     "error_path": "BC-ERR-06003",
     "derivation": "the four left values added with no widths"
    },
    {
     "id": "B",
     "is_key": false,
     "expr": "62",
     "error_path": "BC-ERR-06002",
     "derivation": "right endpoints used: 3(8) + 1(14) + 2(9) + 2(3)"
    },
    {
     "id": "C",
     "is_key": true,
     "expr": "69",
     "error_path": null
    },
    {
     "id": "D",
     "is_key": false,
     "expr": "72",
     "error_path": "BC-ERR-06001",
     "derivation": "one common width 2 times the four left values"
    }
   ],
   "calculator_status": "calculator",
   "skills": [
    "BC-SKL-06005"
   ]
  }
 ],
 "delivery": [
  {
   "block": "orientation",
   "mode": "table",
   "reason": "rule 5: BC-REP-03 on BC-SKL-06005, 06006, 06008 (unit README delivery map)",
   "sources": [
    "BC-SKL-06005",
    "BC-SKL-06006",
    "BC-SKL-06008"
   ],
   "spec": {
    "kind": "table",
    "representations": [
     "BC-REP-03"
    ],
    "columns": [
     "t",
     "0",
     "2",
     "3",
     "6",
     "8"
    ],
    "rows": [
     [
      "R(t)",
      "6",
      "10",
      "13",
      "9",
      "4"
     ],
     [
      "width",
      "",
      "2",
      "1",
      "3",
      "2"
     ]
    ],
    "labels": [
     {
      "text": "widths from the inputs",
      "placement": "inside",
      "at": "width row"
     }
    ]
   },
   "fallback": "the table as plain text rows",
   "keyboard": "Tab moves between cells; no control"
  },
  {
   "block": "ki-1",
   "mode": "figure",
   "reason": "rule 4: BC-REP-02 on BC-SKL-06007 and BC-SKL-06009; one static figure of the four sample-point choices at a fixed n (unit README delivery map)",
   "sources": [
    "BC-SKL-06007",
    "BC-SKL-06009"
   ],
   "spec": {
    "kind": "graph_panels",
    "representations": [
     "BC-REP-02"
    ],
    "curve": "an increasing concave-down curve on [0, 4]",
    "n": 4,
    "panels": [
     {
      "sum": "left"
     },
     {
      "sum": "right"
     },
     {
      "sum": "midpoint"
     },
     {
      "sum": "trapezoid"
     }
    ],
    "labels": [
     {
      "text": "left",
      "placement": "inside",
      "at": "panel 1 top"
     },
     {
      "text": "right",
      "placement": "inside",
      "at": "panel 2 top"
     },
     {
      "text": "midpoint",
      "placement": "inside",
      "at": "panel 3 top"
     },
     {
      "text": "trapezoid",
      "placement": "inside",
      "at": "panel 4 top"
     }
    ]
   },
   "fallback": "the four panels as one static image with their labels",
   "keyboard": "none needed: the figure has no control"
  },
  {
   "block": "ki-2",
   "mode": "table",
   "reason": "rule 5: BC-REP-03 on BC-SKL-06005 and BC-SKL-06006; the tabulated case of the heights",
   "sources": [
    "BC-SKL-06005",
    "BC-SKL-06006"
   ],
   "spec": {
    "kind": "table",
    "representations": [
     "BC-REP-03"
    ],
    "columns": [
     "subinterval",
     "[0, 2]",
     "[2, 3]",
     "[3, 6]",
     "[6, 8]"
    ],
    "rows": [
     [
      "width",
      "2",
      "1",
      "3",
      "2"
     ],
     [
      "left height",
      "6",
      "10",
      "13",
      "9"
     ],
     [
      "product",
      "12",
      "10",
      "39",
      "18"
     ]
    ],
    "labels": [
     {
      "text": "sum of products 79",
      "placement": "inside",
      "at": "row below the products"
     }
    ]
   },
   "fallback": "the table as plain text rows",
   "keyboard": "Tab moves between cells; no control"
  },
  {
   "block": "ki-3",
   "mode": "text",
   "reason": "rule 6: a statement about computation, no figure-bearing representation needed",
   "sources": [
    "BC-SKL-06009"
   ]
  },
  {
   "block": "ex-1",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  },
  {
   "block": "ex-2",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  },
  {
   "block": "err-BC-ERR-06001",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  },
  {
   "block": "err-BC-ERR-06002",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  },
  {
   "block": "err-BC-ERR-06003",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  },
  {
   "block": "err-BC-ERR-06004",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  }
 ],
 "refresher": [
  "ki-1",
  "err-BC-ERR-06001",
  "err-BC-ERR-06002",
  "err-BC-ERR-06003",
  "err-BC-ERR-06004",
  "ex-1"
 ],
 "research_lines": [
  {
   "file": "research/units/unit-06-integration-accumulation.md",
   "line": "Left, right, and midpoint sums differ only in the sample point."
  },
  {
   "file": "research/scoring/notation-requirements.md",
   "line": "sg-25:13 and sg-26:3 both instruct readers to read an equals sign as an approximation sign for the sum form point"
  }
 ],
 "inferred": [
  {
   "claim": "The three integral-approximation archetypes share one family, so one strategy block covers them; its first line is BC-QA-06001's.",
   "settles": "A ruling on whether one strategy block per family or per archetype applies when the methods differ in sample point only."
  },
  {
   "claim": "The FRQ share of the sum part is 3.33 of the 15.0 minutes, two points of nine.",
   "settles": "Timing data per step once the fluency telemetry exists (unit README section 5)."
  },
  {
   "claim": "Units (gallons per hour, millimetres per hour) are chosen for the context labels; parameter_spec names none.",
   "settles": "A units field in BC-QA-06001 and BC-QA-06002 parameter_spec."
  },
  {
   "claim": "The calculator example has an exact integer answer, so no three-decimal rounding applies.",
   "settles": "Nothing further: BC-QA-06001's parameter_spec notes state that the Riemann sum itself is exact."
  },
  {
   "claim": "Every non-text delivery mode.",
   "settles": "The modality A/B in the build plan: skip rate and time to first credited success by mode."
  }
 ],
 "sources": [
  "BC-CON-06003",
  "BC-SKL-06005",
  "BC-SKL-06006",
  "BC-SKL-06007",
  "BC-SKL-06008",
  "BC-SKL-06009",
  "BC-EK-LIM-5A1",
  "BC-EK-LIM-5A2",
  "BC-EK-LIM-5A3",
  "ced:119",
  "BC-QA-06001",
  "BC-QA-06002",
  "BC-QA-06017",
  "BC-PT-99018",
  "BC-PT-99019",
  "sg-23:2",
  "sg-23:3",
  "sg-25:13",
  "BC-ERR-06001",
  "BC-ERR-06002",
  "BC-ERR-06003",
  "BC-ERR-06004",
  "BC-MIS-06001",
  "BC-MIS-06004",
  "BC-PRQ-06005",
  "BC-PRQ-06007",
  "BC-PRQ-06012",
  "research/units/unit-06-integration-accumulation.md#6.2 Approximating Areas with Riemann Sums",
  "research/question-analysis/question-archetypes.md#BC-QA-06001 Riemann sum from a table with over or under estimate reasoning",
  "research/question-analysis/question-archetypes.md#BC-QA-06002 Trapezoidal approximation of an accumulated amount from a table",
  "research/question-analysis/question-archetypes.md#BC-QA-06017 Riemann or trapezoidal sum with equal subintervals for a function given by a formula or a graph",
  "research/exam/exam-structure.md#Section and part layout",
  "research/scoring/common-point-losses.md#Setup points",
  "research/scoring/notation-requirements.md#The equal sign"
 ],
 "read_minutes": {
  "full": 5.7,
  "brief": 3.0
 },
 "word_count": {
  "full": 851,
  "brief": 447
 }
}
```
