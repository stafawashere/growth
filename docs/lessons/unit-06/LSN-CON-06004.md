---
title: LSN-CON-06004 Over and under estimate reasoning for approximations
research_date: 2026-09-29
status: designed
purpose: Authoring spec for the concept lesson on BC-CON-06004, deciding whether a Riemann or trapezoidal sum over or underestimates from monotonicity or concavity, built from authoring_bundle("BC-CON-06004") and the research files it cites.
---

# LSN-CON-06004 Over and under estimate reasoning for approximations

Concept BC-CON-06004 (skills BC-SKL-06010, BC-SKL-06011), topic 6.2 of Unit 6, loaded by BC-QA-06001 and BC-QA-06002 (family integral-approximation). Its hard parent is BC-CON-06003 (docs/lessons/unit-06/README.md, section 1).

## Orientation

Served text, from BC-CON-06004 `description_plain` and the topic's Assessment behaviour paragraph (research/units/unit-06-integration-accumulation.md#6.2 Approximating Areas with Riemann Sums): conceptual variants ask only whether the estimate is high or low; justification variants require monotonicity or concavity to be named. No count, no frequency.

## Key ideas

Both skills map to BC-EK-LIM-5A4, so one core block, both bands.

- ki-1 (core), BC-EK-LIM-5A4, ced:119. Paraphrase of the Error direction paragraph of Required mathematical knowledge: monotonicity for left and right sums, concavity for trapezoidal and midpoint sums. No anchor quote: the LIM-5.A.4 sentence is 31 words. Notation line from the concept record.

## Recognition

- BC-QA-06001 (research/question-analysis/question-archetypes.md#BC-QA-06001 Riemann sum from a table with over or under estimate reasoning): `common_givens` include a statement that the rate is differentiable, increasing, or decreasing; `asked_to_produce` includes an over or under estimate decision with a reason. Official examples include BC-FRQ-2021-Q1-C and BC-FRQ-2022-Q4-C.
- BC-QA-06002 (research/question-analysis/question-archetypes.md#BC-QA-06002 Trapezoidal approximation of an accumulated amount from a table): `difficulty_variables` include whether a concavity based over or under estimate justification is required.

The signal: "overestimate or underestimate" with "explain" or "give a reason", and a property of f stated in the stem or readable from f prime. Not this concept: a request for the sum's value alone (BC-CON-06003), or a tangent line estimate, where the same concavity reason applies to a different approximation (Unit 4).

## Method choice

One strategy block: both archetypes share the family integral-approximation.

- st-1, BC-QA-06001, both bands. Method, the last entry of `expected_solution_path` ("compare with the exact integral using monotonicity"), with BC-QA-06002's concavity case beside it; the first entry, the subintervals, belongs to BC-CON-06003. Rival: a trapezoidal direction decided from monotonicity (BC-ERR-06007, in BC-QA-06002's lineage; `wrong_approaches` on both archetypes name only sum-building errors) [inferred]. Separating feature: the named sum type.

## Solution path

- ex-1, BC-QA-06001, both bands, calculator. Draw: gaps 2, 2, 1, 3, even_gap 2, rates 3, 5, 8, 12, 17 (increasing), endpoint left, context rain, spacing nonuniform, framing context; derived left_sum 60, right_sum 89, left_values 28, third_option 56. No published item carries this draw.
- Steps: the products (new, BC-PT-99018); 60 (equivalent, BC-PT-99019); the property that decides (no value); direction with reason (no value). The answer is a statement: 60, an underestimate, because r is increasing.

A fluent solver writes the products, the value and one sentence naming the property; the choice of property is held in the head [inferred].

## Scoring

BC-QA-06001 lists BC-PT-99018, 99019, 99022, 99026, 99007. ex-1 tags 99018 and 99019 and the checklist is `reader_checks(["BC-PT-99018", "BC-PT-99019"])` copied exactly. BC-PT-99026 covers a concavity reason only, so the monotonicity step carries no tag (library gap, inferred array). For the author: an over or underestimate claimed without concavity loses the point (cr-23:11, cr-23:12; research/scoring/common-point-losses.md#Justification points); for concavity the reason runs to the position of the curve and never rests on a single point (research/scoring/justification-requirements.md#Reasons about slope fields and concavity).

## Traps

Three active errors meet the skills, in the bundle's order: BC-ERR-06005, BC-ERR-06006, BC-ERR-06007 (each linked to BC-MIS-07010, severity high). Low band all three, mid band the first two. On ex-1's draw:

- err-BC-ERR-06005: "Underestimate." against the same direction with its reason; the CAS finds the two inequalities equivalent, so the loss is the reason alone.
- err-BC-ERR-06006: 60 > the integral against 60 < the integral.
- err-BC-ERR-06007: the same table as a trapezoidal sum, 74.5, called an overestimate because r increases, against no direction without concavity. Possible reason, words from BC-MIS-05020.

No possible-reason line on the first two, to hold the brief band.

## Representations

None as a separate block. The topic's graph-to-approximation conversion is carried by the orientation and ki-1 figures.

## Prerequisite bridge

- BC-PRQ-06008, from its `description_plain` (comparing an approximation with the exact quantity) and `failure_signature` (a claim with no monotonicity or concavity).

## Time

BC-QA-06001 is `calculator` and scored as a free response part: Section II Part A, 15.0 minutes per question (research/exam/exam-structure.md#Section and part layout); the sum is a 3.33 minute two-point share, the reason a short addition [inferred]. As an MCQ it takes Part B, 2.92. The minutes go on the reason sentence, not the arithmetic.

## Checks

- chk-1, completion of ex-1, both bands: 60 and "increasing" given; key: underestimate, because r is increasing.
- chk-2, isomorph, both bands. Draw: gaps 1, 3, 2, 2, even_gap 2, rates 18, 14, 9, 6, 2 (decreasing), right, tank, nonuniform, context. Key: 57, an underestimate, because R is decreasing.
- chk-3, MCQ, low band, on BC-QA-06002. Draw: gaps 2, 4, 6, rates 2, 3, 6, 15, initial 30, download, integral; trapezoid 86. Key: overestimate, because r is concave up. Distractors: "because r is increasing" (BC-ERR-06007), a bare "Overestimate" (BC-ERR-06005), "Underestimate, since a sum only approximates" (BC-ERR-06005). BC-ERR-06006 concerns left and right sums, so no trapezoid distractor carries it.

## Delivery

- orientation: figure. Rule 4, BC-REP-02 on BC-SKL-06010 and 06011 (unit README section 6).
- ki-1: figure, two panels. Rule 4; not promoted, since BC-QA-06001's `difficulty_variables` name a property, not a varying quantity.
- ex-1 and the three error blocks: step_reveal. Rule 1.

Every non-text choice is [inferred]; settled by the modality A/B.

## Band plan

- Low (full): orientation, ki-1, st-1, ex-1 with its reader lines, three error blocks, chk-1 to chk-3, the bridge. 527 words, 3.6 minutes (cap 900 and 6).
- Mid (brief): orientation, ki-1, st-1, ex-1 with its reader lines, err-BC-ERR-06005, err-BC-ERR-06006, chk-1, chk-2, the bridge. 426 words, 2.9 minutes (cap 450 and 3).
- Refresher: ki-1, the three error blocks, ex-1.

## Sources

- BC-CON-06004; BC-SKL-06010, BC-SKL-06011; BC-EK-LIM-5A4; ced:119
- BC-QA-06001, BC-QA-06002; BC-PT-99018, BC-PT-99019, BC-PT-99026; sg-23:2, sg-25:13; cr-23:11, cr-23:12
- BC-ERR-06005, BC-ERR-06006, BC-ERR-06007; BC-MIS-05020
- BC-PRQ-06008
- research/units/unit-06-integration-accumulation.md#6.2 Approximating Areas with Riemann Sums
- research/question-analysis/question-archetypes.md#BC-QA-06001 Riemann sum from a table with over or under estimate reasoning
- research/question-analysis/question-archetypes.md#BC-QA-06002 Trapezoidal approximation of an accumulated amount from a table
- research/exam/exam-structure.md#Section and part layout
- research/scoring/common-point-losses.md#Justification points
- research/scoring/justification-requirements.md#Reasons about slope fields and concavity
- [inferred] No point type for a monotonicity reason. Settled by a BC-PT record for it.
- [inferred] The time share. Settled by timing data per step.
- [inferred] Units for the context label. Settled by a units field.
- [inferred] The concavity statement added to chk-3's stem. Settled by a concavity parameter.
- [inferred] The rival as BC-ERR-06007. Settled by a wrong_approaches entry naming it.
- [inferred] Static figures. Settled by the modality A/B.

## Machine record

```json
{
 "id": "LSN-CON-06004",
 "kind": "concept",
 "target_id": "BC-CON-06004",
 "unit": "06",
 "skills": [
  "BC-SKL-06010",
  "BC-SKL-06011"
 ],
 "orientation": {
  "text": "Whether a sum is too big or too small follows from how the function rises, falls or bends. A response names that property of the given function, then the direction.",
  "sources": [
   "BC-CON-06004",
   "research/units/unit-06-integration-accumulation.md#6.2 Approximating Areas with Riemann Sums"
  ]
 },
 "key_ideas": [
  {
   "id": "ki-1",
   "ek_id": "BC-EK-LIM-5A4",
   "depth": "core",
   "text": "Left and right sums: monotonicity decides. Increasing f: left under, right over; decreasing reverses. Trapezoid and midpoint: concavity decides. Concave up: trapezoid over, midpoint under; concave down reverses.",
   "notation": "underestimate, overestimate",
   "quote": null,
   "sources": [
    "BC-EK-LIM-5A4",
    "ced:119",
    "research/units/unit-06-integration-accumulation.md#6.2 Approximating Areas with Riemann Sums"
   ]
  }
 ],
 "strategy": [
  {
   "id": "st-1",
   "archetype_id": "BC-QA-06001",
   "cue": "A sum from a table, a stated increasing, decreasing or concavity property, and over or under asked.",
   "method": "Name the sum type: left or right uses monotonicity, trapezoid or midpoint uses concavity.",
   "rival": "Rival: a trapezoid judged by increasing.",
   "separating_feature": "The named sum type.",
   "sources": [
    "BC-QA-06001",
    "BC-QA-06002"
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
     2,
     1,
     3
    ],
    "even_gap": 2,
    "rates": [
     3,
     5,
     8,
     12,
     17
    ],
    "endpoint": "left",
    "context": "rain",
    "spacing": "nonuniform",
    "framing": "context"
   },
   "problem": {
    "text": "Rain falls at r(t) mm per hour, r increasing. t: 0, 2, 4, 5, 8; r(t): 3, 5, 8, 12, 17. Find the left sum for ∫_0^8 r(t) dt. Under or over?",
    "command_verb": "find"
   },
   "calculator_status": "calculator",
   "steps": [
    {
     "cue": "Left ends times widths 2, 2, 1, 3.",
     "why": "Products shown.",
     "expr": "2*3 + 2*5 + 1*8 + 3*12",
     "relation": "new",
     "point_type_id": "BC-PT-99018"
    },
    {
     "cue": "Add.",
     "why": "The value with its products.",
     "expr": "60",
     "relation": "equivalent",
     "point_type_id": "BC-PT-99019"
    },
    {
     "cue": "Left sum and r increasing: monotonicity decides.",
     "why": "Each left height is the least on its subinterval."
    },
    {
     "cue": "Write direction and reason.",
     "why": "A bare direction earns nothing."
    }
   ],
   "answer": {
    "form": "statement",
    "expr": "underestimate",
    "text": "60, an underestimate, because r is increasing on [0, 8]."
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
  }
 ],
 "common_errors": [
  {
   "error_id": "BC-ERR-06005",
   "observed_behavior": "The response asserts that an approximation is an underestimate or an overestimate but cites no monotonicity or concavity evidence.",
   "scoring_consequence": "The justification point is not earned even when the direction stated is correct.",
   "wrong_step": {
    "text": "Underestimate.",
    "expr": "60 < Integral(r(t), (t, 0, 8))"
   },
   "right_step": {
    "text": "Underestimate, r increasing.",
    "expr": "60 < Integral(r(t), (t, 0, 8))"
   },
   "relation": "equivalent",
   "possible_reason": null,
   "sources": [
    "BC-ERR-06005"
   ]
  },
  {
   "error_id": "BC-ERR-06006",
   "observed_behavior": "A left sum is called an overestimate for an increasing function, or a right sum an underestimate.",
   "scoring_consequence": "The justification point is lost and the answer point with it when the direction is part of the answer.",
   "wrong_step": {
    "text": "Overestimate.",
    "expr": "60 > Integral(r(t), (t, 0, 8))"
   },
   "right_step": {
    "text": "Underestimate.",
    "expr": "60 < Integral(r(t), (t, 0, 8))"
   },
   "relation": "distinct",
   "possible_reason": null,
   "sources": [
    "BC-ERR-06006"
   ]
  },
  {
   "error_id": "BC-ERR-06007",
   "observed_behavior": "The response argues that a trapezoidal sum overestimates because the function is increasing.",
   "scoring_consequence": "The justification point is not earned because the stated reason does not support the conclusion.",
   "wrong_step": {
    "text": "Same table, trapezoidal sum 74.5, called an overestimate because r increases.",
    "expr": "149/2 > Integral(r(t), (t, 0, 8))"
   },
   "right_step": {
    "text": "74.5, with no concavity given, so no direction follows.",
    "expr": "149/2"
   },
   "relation": "distinct",
   "possible_reason": {
    "misconception_id": "BC-MIS-05020",
    "text": "does not distinguish rising from bending upward"
   },
   "sources": [
    "BC-ERR-06007",
    "BC-MIS-05020"
   ]
  }
 ],
 "representations": null,
 "prerequisite_bridges": [
  {
   "prq_id": "BC-PRQ-06008",
   "text": "Say which is larger, estimate or exact, from how f rises, falls or bends; a claim with no such reason fails."
  }
 ],
 "time": {
  "exam_part": "II-A",
  "budget_minutes": 15.0,
  "source": "research/exam/exam-structure.md#Section and part layout",
  "written_steps": {
   "ex-1": [
    1,
    2,
    4
   ]
  },
  "skipped_steps": {
   "ex-1": [
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
   "archetype_id": "BC-QA-06001",
   "parameter_draw": {
    "gaps": [
     2,
     2,
     1,
     3
    ],
    "even_gap": 2,
    "rates": [
     3,
     5,
     8,
     12,
     17
    ],
    "endpoint": "left",
    "context": "rain",
    "spacing": "nonuniform",
    "framing": "context"
   },
   "completes": "ex-1",
   "stem": {
    "text": "The left sum is 60 and r is increasing. Under or over, with the reason?",
    "command_verb": "determine"
   },
   "key": {
    "form": "statement",
    "expr": "underestimate",
    "text": "An underestimate, because r is increasing on [0, 8]."
   },
   "calculator_status": "calculator",
   "skills": [
    "BC-SKL-06010"
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
    "even_gap": 2,
    "rates": [
     18,
     14,
     9,
     6,
     2
    ],
    "endpoint": "right",
    "context": "tank",
    "spacing": "nonuniform",
    "framing": "context"
   },
   "stem": {
    "text": "R decreasing; t: 0, 1, 4, 6, 8; R(t): 18, 14, 9, 6, 2. Right sum for ∫_0^8 R(t) dt, under or over?",
    "command_verb": "find"
   },
   "key": {
    "form": "statement",
    "expr": "underestimate",
    "text": "57, an underestimate, because R is decreasing on [0, 8]."
   },
   "steps": [
    {
     "text": "Right ends times widths 1, 3, 2, 2.",
     "expr": "1*14 + 3*9 + 2*6 + 2*2",
     "relation": "new"
    },
    {
     "text": "Add.",
     "expr": "57",
     "relation": "equivalent"
    }
   ],
   "calculator_status": "calculator",
   "skills": [
    "BC-SKL-06010"
   ]
  },
  {
   "id": "chk-3",
   "check_kind": "mcq",
   "format": "mcq",
   "bands": [
    "low"
   ],
   "archetype_id": "BC-QA-06002",
   "parameter_draw": {
    "gaps": [
     2,
     4,
     6
    ],
    "rates": [
     2,
     3,
     6,
     15
    ],
    "initial": 30,
    "context": "download",
    "ask": "integral"
   },
   "stem": {
    "text": "r is increasing and concave up; t: 0, 2, 6, 12; r(t): 2, 3, 6, 15. The trapezoidal sum for ∫_0^12 r(t) dt is 86. Which is right?",
    "command_verb": "identify"
   },
   "key": {
    "form": "statement",
    "expr": "overestimate_concave_up"
   },
   "options": [
    {
     "id": "A",
     "is_key": true,
     "label": "Overestimate, because r is concave up.",
     "error_path": null
    },
    {
     "id": "B",
     "is_key": false,
     "label": "Overestimate, because r is increasing.",
     "error_path": "BC-ERR-06007",
     "derivation": "the trapezoid judged by monotonicity"
    },
    {
     "id": "C",
     "is_key": false,
     "label": "Overestimate.",
     "error_path": "BC-ERR-06005",
     "derivation": "a direction with no property cited"
    },
    {
     "id": "D",
     "is_key": false,
     "label": "Underestimate, since a sum only approximates.",
     "error_path": "BC-ERR-06005",
     "derivation": "a direction with no monotonicity or concavity evidence"
    }
   ],
   "calculator_status": "no_calculator",
   "skills": [
    "BC-SKL-06011"
   ]
  }
 ],
 "delivery": [
  {
   "block": "orientation",
   "mode": "figure",
   "reason": "rule 4: BC-REP-02 on BC-SKL-06010 and BC-SKL-06011 (unit README delivery map)",
   "sources": [
    "BC-SKL-06010",
    "BC-SKL-06011"
   ],
   "spec": {
    "kind": "graph",
    "representations": [
     "BC-REP-02"
    ],
    "curve": "an increasing curve on [0, 8]",
    "rectangles": {
     "sum": "left",
     "n": 4
    },
    "labels": [
     {
      "text": "gap above each rectangle: left sum too small",
      "placement": "inside",
      "at": "top left"
     }
    ]
   },
   "fallback": "the same graph as a static image with its label",
   "keyboard": "none needed: the figure has no control"
  },
  {
   "block": "ki-1",
   "mode": "figure",
   "reason": "rule 4: BC-REP-02 on BC-SKL-06010 and BC-SKL-06011; not promoted, since BC-QA-06001's difficulty_variables name a property (whether the table is monotone), not a varying quantity",
   "sources": [
    "BC-SKL-06010",
    "BC-SKL-06011",
    "BC-QA-06001"
   ],
   "spec": {
    "kind": "graph_panels",
    "representations": [
     "BC-REP-02"
    ],
    "panels": [
     {
      "curve": "increasing",
      "sums": [
       "left",
       "right"
      ]
     },
     {
      "curve": "concave up",
      "sums": [
       "trapezoid",
       "midpoint"
      ]
     }
    ],
    "labels": [
     {
      "text": "increasing: left under, right over",
      "placement": "inside",
      "at": "panel 1 top"
     },
     {
      "text": "concave up: trapezoid over, midpoint under",
      "placement": "inside",
      "at": "panel 2 top"
     }
    ]
   },
   "fallback": "the two panels as one static image with their labels",
   "keyboard": "none needed: the figure has no control"
  },
  {
   "block": "ex-1",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  },
  {
   "block": "err-BC-ERR-06005",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  },
  {
   "block": "err-BC-ERR-06006",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  },
  {
   "block": "err-BC-ERR-06007",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  }
 ],
 "refresher": [
  "ki-1",
  "err-BC-ERR-06005",
  "err-BC-ERR-06006",
  "err-BC-ERR-06007",
  "ex-1"
 ],
 "research_lines": [
  {
   "file": "research/units/unit-06-integration-accumulation.md",
   "line": "Hypotheses: f monotone on the interval. Conclusion: a left sum underestimates when f is increasing and overestimates when f is decreasing, with the reverse for a right sum."
  },
  {
   "file": "research/scoring/justification-requirements.md",
   "line": "For over and underestimate questions the reason must run from the second derivative to concavity to the position of the tangent line."
  }
 ],
 "inferred": [
  {
   "claim": "BC-QA-06001 lists BC-PT-99026 (concavity) but no point type for a monotonicity justification, so ex-1's direction step carries no tag and no reader line.",
   "settles": "A BC-PT record for an over or under estimate decided from monotonicity, from a rubric such as the one BC-FRQ-2021-Q1-C scores."
  },
  {
   "claim": "The two-point sum share of the 15.0 Section II minutes is 3.33, plus the reason.",
   "settles": "Timing data per step once the fluency telemetry exists (unit README section 5)."
  },
  {
   "claim": "Units (mm per hour) are chosen for the context label rain; parameter_spec names none.",
   "settles": "A units field in BC-QA-06001's parameter_spec."
  },
  {
   "claim": "The concavity statement in chk-3 is added to the stem; BC-QA-06002's parameter_spec has no concavity parameter.",
   "settles": "A concavity parameter in BC-QA-06002's parameter_spec."
  },
  {
   "claim": "The orientation and ki-1 are served as static figures.",
   "settles": "The modality A/B in the build plan: skip rate and time to first credited success by mode."
  }
 ],
 "sources": [
  "BC-CON-06004",
  "BC-SKL-06010",
  "BC-SKL-06011",
  "BC-EK-LIM-5A4",
  "ced:119",
  "BC-QA-06001",
  "BC-QA-06002",
  "BC-PT-99018",
  "BC-PT-99019",
  "BC-PT-99026",
  "sg-23:2",
  "sg-25:13",
  "BC-ERR-06005",
  "BC-ERR-06006",
  "BC-ERR-06007",
  "BC-MIS-05020",
  "BC-PRQ-06008",
  "cr-23:11",
  "cr-23:12",
  "research/units/unit-06-integration-accumulation.md#6.2 Approximating Areas with Riemann Sums",
  "research/question-analysis/question-archetypes.md#BC-QA-06001 Riemann sum from a table with over or under estimate reasoning",
  "research/question-analysis/question-archetypes.md#BC-QA-06002 Trapezoidal approximation of an accumulated amount from a table",
  "research/exam/exam-structure.md#Section and part layout",
  "research/scoring/common-point-losses.md#Justification points",
  "research/scoring/justification-requirements.md#Reasons about slope fields and concavity"
 ],
 "read_minutes": {
  "full": 3.6,
  "brief": 2.9
 },
 "word_count": {
  "full": 527,
  "brief": 426
 }
}
```
