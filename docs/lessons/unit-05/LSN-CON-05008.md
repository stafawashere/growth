---
title: LSN-CON-05008 Point of inflection as a change of concavity
research_date: 2026-09-29
status: designed
purpose: Authoring spec for the concept lesson on BC-CON-05008, the point of inflection as a change of concavity, built from authoring_bundle("BC-CON-05008") and the research files it cites, so an author fills plan 15's lesson record without making a teaching decision.
---

# LSN-CON-05008 Point of inflection as a change of concavity

Concept BC-CON-05008 (skills BC-SKL-05032 to BC-SKL-05035), topic 5.6 of Unit 5, loaded by BC-QA-05005 (primary) and BC-QA-05004, both in family concavity-analysis. Unit parent BC-CON-05007 (docs/lessons/unit-05/README.md, section 1). The written reason, phrased through the plotted object the stem supplies, is the object of the lesson.

## Prediction

Both bands, first. Poses ex-1's own graph: f' peaks at x = 3 and crosses zero at 4/3 and 5, and the student predicts where f has its inflection point. Form `mcq`, two options, key A (at the peak of f'). The resolution says f' turns from rising to falling there, so f'' changes sign. Sources: BC-CON-05008 and the topic 5.6 section.

## Orientation

Served text, from BC-CON-05008 `description_plain` and the topic's Assessment behaviour paragraph (research/units/unit-05-analytical-applications-differentiation.md#5.6 Determining Concavity of Functions over Their Domains): a response lists exactly the inputs where the concavity changes, and gives the reason through the graph the stem supplied, such as f' changing from increasing to decreasing. No count, no frequency.

## Key ideas

All four skills map to BC-EK-FUN-4A6 (ced:104), so one core block, both bands.

- ki-1 (core). Paraphrase of the Required mathematical knowledge paragraph (Point of inflection; Justification standard): an inflection at c in the domain needs f'' to change sign, and a zero of f'' without a change is not one; from a graph of f', that is where f' switches between increasing and decreasing, and the reason names f' (sg-25:17). Anchor quote (17 words) from ced:104. Notation line from the concept record.

## Recognition

- BC-QA-05005 (research/question-analysis/question-archetypes.md#BC-QA-05005 Points of inflection identified with a reason tied to the given graph): `typical_wording` "find all values in the open interval at which the graph has a point of inflection, and give a reason for the answer"; `common_givens` a graph of the derivative or of an integrand, an open interval; `asked_to_produce` the complete list of inputs, a reason phrased through the given function. The signal: "point of inflection" beside a graph labelled f' or an integrand. FRQ appearances BC-FRQ-2022-Q3-B, BC-FRQ-2025-Q4-B, BC-FRQ-2026-Q4-B, BC-FRQ-2018-Q3-D; MCQ BC-MCQ-CED-014, BC-MCQ-PE2012-034.
- BC-QA-05004 (research/question-analysis/question-archetypes.md#BC-QA-05004 Intervals of concavity from derivative information with a reason) shares the family and the graph; it asks for intervals, not inputs (BC-CON-05007).

What says "not this concept" (the contrast pair's near miss is the sibling concept BC-CON-05005, where a relative maximum needs f' to change sign, and the zero-of-f' rival of BC-ERR-05033): "relative maximum" asks where f' changes sign, not where it turns (BC-CON-05005).

## Method choice

One strategy block, both bands: BC-QA-05005 and BC-QA-05004 share one family, so one block.

- st-1, BC-QA-05005. Method, `expected_solution_path[0]`: find where the given plot changes from increasing to decreasing or the reverse. Rival, `wrong_approaches`: testing candidates with a second derivative test; the scored rivals are the zeros of the plot and every corner (BC-ERR-05033, BC-ERR-05034). Separating feature: the plotted f' must turn, not merely cross zero or change steepness. The archetype carries `asked_to_produce` and `common_givens`, so the block is not tagged inferred.

## Solution path

- ex-1, BC-QA-05005, both bands, no calculator. Draw: heights -3, -1, 2, 3, 1, 0, -2 at x = 0 to 6, so slopes 2, 3, 1, -2, -1, -2: one turning corner at x = 3 (the answer), corners where only the steepness changes, and an axis crossing inside the segment from x = 1 to 2, as the spec's notes require. No published BC-QA-05005 item carries this draw. Steps follow `expected_solution_path`: where f' turns (no value), the list (new), the reason (no value, tagged BC-PT-99061).

A fluent solver writes the list and the reason sentence; the slope reading is held in the head.

## Scoring

BC-QA-05005 lists BC-PT-99060 and BC-PT-99061. ex-1 tags BC-PT-99061 on the reason step, the justification point; its line is `reader_checks(["BC-PT-99061"])`. The BC-PT-99060 line is not served, to hold the brief band under its cap; its content (any extra input inside the interval forfeits both points, sg-25:17, sg-26:15) is carried by the error records' scoring_consequence. For the author: "f changes concavity" or "f'' changes sign" earns the list, not the reason, and "the function" or "the graph" as subject forfeits it (sg-22:11, research/scoring/justification-requirements.md#Reasons tied to the object the prompt names; research/scoring/common-point-losses.md#Justification points).

## Traps

Seven active errors meet the skills; the first four in the bundle's order are served (low band all four, mid band the first two). BC-ERR-99001, 99023 and 99030 are left out by the cap of 4.

- err-BC-ERR-05032: an input outside the domain listed. Statement-shaped (ex-1's f is defined on the whole interval). No possible reason line.
- err-BC-ERR-05033 on ex-1: the zeros of the plot, 4/3 and 5, against 3. Possible reason, words from BC-MIS-05021.
- err-BC-ERR-05034 on ex-1: every corner, where f'' keeps its sign across four of them, against 3. No possible reason line.
- err-BC-ERR-05035: "f'' changes sign" against "f' changes from increasing to decreasing". Statement-shaped. Possible reason, words from BC-MIS-05022.

## Representations

One block, low band: the topic's Representations paragraph names the graph of f' to the concavity of f (BC-REP-02 to BC-REP-04), served as a static figure of ex-1's f' with the turning corner and a steepness-only corner labelled, the touching-zero case of the unit delivery map.

## Prerequisite bridge

- BC-PRQ-05001 and BC-PRQ-05003, each from its `description_plain` and `failure_signature`.

## Time

BC-QA-05005 is `no_calculator` and one 2-point part of a free-response question, so Section II Part B, 15.0 minutes per question (research/exam/exam-structure.md#Section and part layout), this part a share of it (3.3 minutes on the README's per-point share) [inferred]. The minutes go on reading the slopes; the answer is a list and one sentence.

## Checks

- chk-1, completion of ex-1, both bands: the slopes are given, the student writes the list. Key {3}.
- chk-2, isomorph, both bands. Draw: heights 2, 0, -1, 1, 2, 1, -2; slopes -2, -1, 2, 1, -1, -3. Key {2, 4}.
- chk-3, MCQ, low band. Draw: heights 1, 3, 2, -1, -2, 0, 1; slopes 2, -1, -3, -1, 2, 1. Key {1, 4}. Distractors: the zeros of f', {8/3, 5} (BC-ERR-05033); every corner, {1, 2, 3, 4, 5} (BC-ERR-05034); the zeros added to the turns, {1, 8/3, 4, 5} (BC-ERR-05033). BC-ERR-05032 produces no list on this draw, so two distractors share an error path.

## Delivery

- orientation: text. Rule 6, per the unit delivery map.
- ki-1: interactive, a point dragged along the graph of f' building the sign chart of f'' as it passes each corner. Rule 4 promoted: BC-REP-02 on BC-SKL-05032 to 05035, with BC-QA-05005 `difficulty_variables` "how many points of inflection there are" and "whether a candidate is a touching zero with no sign change" [inferred; settled by the modality A/B].
- representations: figure. Rule 4 on BC-REP-02.
- ex-1 and the four error blocks: step_reveal. Rule 1.

## Band plan

- Low (full): served order of 2026-09-29: prediction, orientation, the two bridges, ki-1, st-1 with its contrast pair, ex-1 with its scoring line, chk-1, the four error blocks, chk-2, representations, chk-3. 580 words, 3.9 minutes (cap 900 and 6).
- Mid (brief): prediction, orientation, the two bridges, ki-1, st-1 with its contrast pair, ex-1 with its scoring line, chk-1, err-BC-ERR-05032 and err-BC-ERR-05033, chk-2. 443 words, 3.0 minutes (cap 450 and 3). The orientation, key idea text, strategy fields, bridges and ex-1 cues were shortened to hold the cap; the anchor quote stays.
- Refresher: ki-1, err-BC-ERR-05032, err-BC-ERR-05033, err-BC-ERR-05034, err-BC-ERR-05035, ex-1.

## Sources

- Prediction and contrast pair: BC-CON-05008, BC-CON-05005, BC-ERR-05033 (as above).

- BC-CON-05008; BC-SKL-05032 to BC-SKL-05035; BC-EK-FUN-4A6; ced:104
- BC-QA-05005, BC-QA-05004; BC-FRQ-2022-Q3-B, BC-FRQ-2025-Q4-B, BC-FRQ-2026-Q4-B, BC-FRQ-2018-Q3-D, BC-MCQ-CED-014, BC-MCQ-PE2012-034
- BC-PT-99061, BC-PT-99060; sg-25:17, sg-26:15, sg-22:11
- BC-ERR-05032, BC-ERR-05033, BC-ERR-05034, BC-ERR-05035, BC-ERR-99001, BC-ERR-99023, BC-ERR-99030; BC-MIS-05021, BC-MIS-05022
- BC-PRQ-05001, BC-PRQ-05003
- research/units/unit-05-analytical-applications-differentiation.md#5.6 Determining Concavity of Functions over Their Domains
- research/question-analysis/question-archetypes.md#BC-QA-05005 Points of inflection identified with a reason tied to the given graph
- research/question-analysis/question-archetypes.md#BC-QA-05004 Intervals of concavity from derivative information with a reason
- research/scoring/justification-requirements.md#Reasons tied to the object the prompt names
- research/scoring/common-point-losses.md#Justification points
- research/exam/exam-structure.md#Section and part layout
- [inferred] The share of the 15.0 minutes the inflection part takes. Settled by a timing measurement of Section II parts, or a per-part budget in research/exam.
- [inferred] The ki-1 interactive and the representations figure. Settled by the modality A/B.

## Machine record

```json
{
 "id": "LSN-CON-05008",
 "kind": "concept",
 "target_id": "BC-CON-05008",
 "unit": "05",
 "skills": [
  "BC-SKL-05032",
  "BC-SKL-05033",
  "BC-SKL-05034",
  "BC-SKL-05035"
 ],
 "prediction": {
  "id": "pr-1",
  "stem": {
   "text": "f' peaks at x = 3 and crosses zero at 4/3 and 5. Where is f's inflection point?",
   "command_verb": "predict"
  },
  "format": "mcq",
  "options": [
   {
    "id": "A",
    "label": "At the peak of f'",
    "is_key": true
   },
   {
    "id": "B",
    "label": "At a zero of f'",
    "is_key": false
   }
  ],
  "resolution": "f' turns from rising to falling at its peak, so f'' changes sign there.",
  "sources": [
   "BC-CON-05008",
   "research/units/unit-05-analytical-applications-differentiation.md#5.6 Determining Concavity of Functions over Their Domains"
  ]
 },
 "orientation": {
  "text": "A response lists where concavity changes, with a reason through the graph given.",
  "sources": [
   "BC-CON-05008",
   "research/units/unit-05-analytical-applications-differentiation.md#5.6 Determining Concavity of Functions over Their Domains"
  ]
 },
 "key_ideas": [
  {
   "id": "ki-1",
   "ek_id": "BC-EK-FUN-4A6",
   "depth": "core",
   "text": "A point of inflection needs f'' to change sign.",
   "notation": "inflection point",
   "quote": {
    "text": "The second derivative of a function may be used to locate points of inflection for the graph of the original function.",
    "source": "ced:104"
   },
   "sources": [
    "BC-EK-FUN-4A6",
    "ced:104",
    "sg-25:17",
    "research/units/unit-05-analytical-applications-differentiation.md#5.6 Determining Concavity of Functions over Their Domains"
   ]
  }
 ],
 "strategy": [
  {
   "id": "st-1",
   "archetype_id": "BC-QA-05005",
   "cue": "Inflection points from a graph of f'?",
   "method": "Where the plotted f' turns.",
   "rival": "Its zeros, or every corner.",
   "separating_feature": "f' must switch rising and falling.",
   "sources": [
    "BC-QA-05005"
   ],
   "evidence_tag": "verified",
   "contrast": {
    "this": {
     "text": "f' peaks at x = 2. Where is the inflection point of f?",
     "archetype_id": "BC-QA-05005"
    },
    "not_this": {
     "text": "f' crosses zero at x = 4. Where is the relative maximum of f?",
     "why_not": "A relative maximum needs f' to change sign."
    },
    "feature": "Inflection: f' turns. Extremum: f' crosses zero."
   }
  }
 ],
 "worked_examples": [
  {
   "id": "ex-1",
   "archetype_id": "BC-QA-05005",
   "bands": [
    "low",
    "mid"
   ],
   "parameter_draw": {
    "heights": [
     -3,
     -1,
     2,
     3,
     1,
     0,
     -2
    ]
   },
   "problem": {
    "text": "The graph of f' joins (0, -3), (1, -1), (2, 2), (3, 3), (4, 1), (5, 0), (6, -2) by segments. Find every inflection point of f, with a reason.",
    "command_verb": "find"
   },
   "calculator_status": "no_calculator",
   "steps": [
    {
     "cue": "Where f' turns.",
     "why": "One slope switch, at x = 3."
    },
    {
     "cue": "List those.",
     "why": "Other corners keep the slope's sign.",
     "expr": "FiniteSet(3)",
     "relation": "new"
    },
    {
     "cue": "Reason through f'.",
     "why": "At x = 3, f' changes from increasing to decreasing.",
     "point_type_id": "BC-PT-99061"
    }
   ],
   "answer": {
    "form": "symbolic",
    "expr": "FiniteSet(3)"
   }
  }
 ],
 "what_a_reader_scores": [
  {
   "example_id": "ex-1",
   "point_type_ids": [
    "BC-PT-99061"
   ],
   "lines": [
    {
     "point_type_id": "BC-PT-99061",
     "text": "Reason for a point of inflection tied to the given graph. Earned by: A reason stated in terms of the graphed derivative changing from increasing to decreasing or the reverse, the slope of that graph changing sign, or that graph attaining a relative extremum (sg-25:17, sg-26:15). Not earned by: A reason in terms of the function changing concavity, or in terms of the second derivative changing sign, both of which sg-25:17 and sg-26:15 state earn the answer point but not this one; a reason using an ambiguous term such as the function or the graph."
    }
   ]
  }
 ],
 "common_errors": [
  {
   "error_id": "BC-ERR-05032",
   "wrong_step": {
    "text": "Input outside the domain listed.",
    "expr": "input_outside_domain_listed"
   },
   "right_step": {
    "text": "Only inputs where f is defined.",
    "expr": "inputs_in_domain_only"
   },
   "relation": "distinct",
   "possible_reason": null,
   "sources": [
    "BC-ERR-05032"
   ],
   "observed_behavior": "The response lists a candidate point of inflection at an input where the function is not defined.",
   "scoring_consequence": "The declared list contains an extra input, which costs the answer point.",
   "fix_prompt": true
  },
  {
   "error_id": "BC-ERR-05033",
   "wrong_step": {
    "text": "Zeros of f'.",
    "expr": "FiniteSet(4/3, 5)"
   },
   "right_step": {
    "text": "Where f' turns.",
    "expr": "FiniteSet(3)"
   },
   "relation": "distinct",
   "possible_reason": {
    "misconception_id": "BC-MIS-05021",
    "text": "equates the candidate condition with the conclusion and never checks the sign change"
   },
   "sources": [
    "BC-ERR-05033",
    "BC-MIS-05021"
   ],
   "observed_behavior": "The response reports every zero of the second derivative, or every zero of the plotted curve, as a point of inflection.",
   "scoring_consequence": "An extra input in the list costs the answer point outright.",
   "fix_prompt": true
  },
  {
   "error_id": "BC-ERR-05034",
   "wrong_step": {
    "text": "Every corner.",
    "expr": "FiniteSet(1, 2, 3, 4, 5)"
   },
   "right_step": {
    "text": "Only the turning corner.",
    "expr": "FiniteSet(3)"
   },
   "relation": "distinct",
   "possible_reason": null,
   "sources": [
    "BC-ERR-05034"
   ],
   "observed_behavior": "The response keeps an input where the second derivative reaches zero and returns to the same sign.",
   "scoring_consequence": "The list has an extra entry, so the answer point is lost.",
   "fix_prompt": true
  },
  {
   "error_id": "BC-ERR-05035",
   "wrong_step": {
    "text": "f'' changes sign at 3.",
    "expr": "f_double_prime_changes_sign"
   },
   "right_step": {
    "text": "f' changes from increasing to decreasing at 3.",
    "expr": "f_prime_increasing_to_decreasing"
   },
   "relation": "distinct",
   "possible_reason": {
    "misconception_id": "BC-MIS-05022",
    "text": "supplies derivative notation in place of a statement about the object the question gave"
   },
   "sources": [
    "BC-ERR-05035",
    "BC-MIS-05022"
   ],
   "observed_behavior": "The reason says that the second derivative changes sign there, without tying the claim to the plotted object the question supplied.",
   "scoring_consequence": "The reason point is lost while the answer point stands; the 2025 guideline names this split directly.",
   "fix_prompt": true
  }
 ],
 "representations": {
  "text": "Only a turn of f' is an inflection; a change of steepness is not.",
  "figure": {
   "kind": "graph",
   "labels": [
    {
     "text": "x = 3: f' turns",
     "placement": "inside"
    },
    {
     "text": "x = 1: steeper, same sign",
     "placement": "inside"
    }
   ]
  }
 },
 "prerequisite_bridges": [
  {
   "prq_id": "BC-PRQ-05001",
   "text": "Zeros."
  },
  {
   "prq_id": "BC-PRQ-05003",
   "text": "Domain."
  }
 ],
 "time": {
  "exam_part": "II-B",
  "budget_minutes": 15.0,
  "source": "research/exam/exam-structure.md#Section and part layout",
  "written_steps": {
   "ex-1": [
    2,
    3
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
   "archetype_id": "BC-QA-05005",
   "parameter_draw": {
    "heights": [
     -3,
     -1,
     2,
     3,
     1,
     0,
     -2
    ]
   },
   "completes": "ex-1",
   "stem": {
    "text": "The example's f' has slopes 2, 3, 1, -2, -1, -2 on its six segments. List the inflection points.",
    "command_verb": "find"
   },
   "key": {
    "form": "symbolic",
    "expr": "FiniteSet(3)"
   },
   "steps": [
    {
     "text": "One switch, at 3.",
     "expr": "FiniteSet(3)",
     "relation": "new"
    }
   ],
   "calculator_status": "no_calculator",
   "skills": [
    "BC-SKL-05033"
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
   "archetype_id": "BC-QA-05005",
   "parameter_draw": {
    "heights": [
     2,
     0,
     -1,
     1,
     2,
     1,
     -2
    ]
   },
   "stem": {
    "text": "f' joins heights 2, 0, -1, 1, 2, 1, -2 at x = 0 to 6. List the inflection points of f.",
    "command_verb": "find"
   },
   "key": {
    "form": "symbolic",
    "expr": "FiniteSet(2, 4)"
   },
   "steps": [
    {
     "text": "Slopes -2, -1, 2, 1, -1, -3: switches at 2 and 4.",
     "expr": "FiniteSet(2, 4)",
     "relation": "new"
    }
   ],
   "calculator_status": "no_calculator",
   "skills": [
    "BC-SKL-05033",
    "BC-SKL-05034"
   ]
  },
  {
   "id": "chk-3",
   "check_kind": "mcq",
   "format": "mcq",
   "bands": [
    "low"
   ],
   "archetype_id": "BC-QA-05005",
   "parameter_draw": {
    "heights": [
     1,
     3,
     2,
     -1,
     -2,
     0,
     1
    ]
   },
   "stem": {
    "text": "f' joins heights 1, 3, 2, -1, -2, 0, 1 at x = 0 to 6. Which lists every inflection point of f?",
    "command_verb": "identify"
   },
   "key": {
    "form": "symbolic",
    "expr": "FiniteSet(1, 4)"
   },
   "steps": [
    {
     "text": "Slopes 2, -1, -3, -1, 2, 1: switches at 1 and 4.",
     "expr": "FiniteSet(1, 4)",
     "relation": "new"
    }
   ],
   "options": [
    {
     "id": "A",
     "is_key": false,
     "expr": "FiniteSet(8/3, 5)",
     "error_path": "BC-ERR-05033",
     "derivation": "the zeros of f' listed"
    },
    {
     "id": "B",
     "is_key": false,
     "expr": "FiniteSet(1, 2, 3, 4, 5)",
     "error_path": "BC-ERR-05034",
     "derivation": "every corner kept, including those where the slope keeps its sign"
    },
    {
     "id": "C",
     "is_key": true,
     "expr": "FiniteSet(1, 4)",
     "error_path": null
    },
    {
     "id": "D",
     "is_key": false,
     "expr": "FiniteSet(1, 8/3, 4, 5)",
     "error_path": "BC-ERR-05033",
     "derivation": "the zeros of f' added to the turns"
    }
   ],
   "calculator_status": "no_calculator",
   "skills": [
    "BC-SKL-05033",
    "BC-SKL-05034"
   ]
  }
 ],
 "delivery": [
  {
   "block": "orientation",
   "mode": "text",
   "reason": "rule 6: a statement of what a response shows; unit README delivery map",
   "sources": [
    "BC-SKL-05035"
   ]
  },
  {
   "block": "ki-1",
   "mode": "interactive",
   "reason": "rule 4 promoted: BC-REP-02 on BC-SKL-05032 to 05035; BC-QA-05005 difficulty_variables how many points of inflection there are and whether a candidate is a touching zero",
   "sources": [
    "BC-SKL-05033",
    "BC-SKL-05034",
    "BC-QA-05005"
   ],
   "spec": {
    "kind": "graph",
    "representations": [
     "BC-REP-02"
    ],
    "curve": "f' through (0, -3), (1, -1), (2, 2), (3, 3), (4, 1), (5, 0), (6, -2)",
    "window": {
     "x": [
      0,
      6
     ],
     "y": [
      -4,
      4
     ]
    },
    "controls": [
     {
      "type": "draggable_point",
      "constrained_to": "curve",
      "start": [
       0.5,
       -2
      ]
     }
    ],
    "drawn": [
     "a sign row for f'' under the graph, filled in as the point passes each segment"
    ],
    "question": "At which corners does the sign of f'' change?",
    "labels": [
     {
      "text": "graph of f'",
      "placement": "inside"
     },
     {
      "text": "sign of f'' (slope of f')",
      "placement": "inside"
     }
    ]
   },
   "fallback": "the graph static with the completed sign row: +, +, +, -, -, - and x = 3 marked",
   "keyboard": "Tab focuses the point; Left and Right arrow keys move it by 0.25; Enter records the sign of f'' at the point"
  },
  {
   "block": "ex-1",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  },
  {
   "block": "err-BC-ERR-05032",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  },
  {
   "block": "err-BC-ERR-05033",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  },
  {
   "block": "err-BC-ERR-05034",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  },
  {
   "block": "err-BC-ERR-05035",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  },
  {
   "block": "representations",
   "mode": "figure",
   "reason": "rule 4: BC-REP-02 on BC-SKL-05034; unit README delivery map, the touching-zero case",
   "sources": [
    "BC-SKL-05034"
   ],
   "spec": {
    "kind": "graph",
    "representations": [
     "BC-REP-02"
    ],
    "curve": "f' through (0, -3), (1, -1), (2, 2), (3, 3), (4, 1), (5, 0), (6, -2)",
    "window": {
     "x": [
      0,
      6
     ],
     "y": [
      -4,
      4
     ]
    },
    "labels": [
     {
      "text": "x = 3: f' turns, inflection",
      "placement": "inside"
     },
     {
      "text": "x = 1: steeper, same sign, not one",
      "placement": "inside"
     },
     {
      "text": "x = 4/3: f' = 0, not one",
      "placement": "inside"
     }
    ]
   },
   "fallback": "the same static figure with its labels read as a list",
   "keyboard": "no control; the figure description is reached with Tab"
  }
 ],
 "refresher": [
  "ki-1",
  "err-BC-ERR-05032",
  "err-BC-ERR-05033",
  "err-BC-ERR-05034",
  "err-BC-ERR-05035",
  "ex-1"
 ],
 "research_lines": [
  {
   "file": "research/scoring/justification-requirements.md",
   "line": "Where a question gives the graph of a derivative and asks about the original function, the reason point is earned only by reasoning about the graphed object."
  }
 ],
 "inferred": [
  {
   "claim": "The inflection part takes a 3.3 minute share of the 15.0 minute Section II question.",
   "settles": "A per-part time budget in research/exam, or a timing measurement of Section II parts."
  },
  {
   "claim": "ki-1 is an interactive draggable point and the representations block a static figure.",
   "settles": "The modality A/B in the build plan: skip rate and time to first credited success by mode."
  }
 ],
 "sources": [
  "BC-CON-05008",
  "BC-EK-FUN-4A6",
  "ced:104",
  "BC-QA-05005",
  "BC-QA-05004",
  "BC-PT-99061",
  "BC-PT-99060",
  "sg-25:17",
  "sg-26:15",
  "sg-22:11",
  "BC-ERR-05032",
  "BC-ERR-05033",
  "BC-ERR-05034",
  "BC-ERR-05035",
  "BC-MIS-05021",
  "BC-MIS-05022",
  "BC-PRQ-05001",
  "BC-PRQ-05003",
  "research/units/unit-05-analytical-applications-differentiation.md#5.6 Determining Concavity of Functions over Their Domains",
  "research/question-analysis/question-archetypes.md#BC-QA-05005 Points of inflection identified with a reason tied to the given graph",
  "research/question-analysis/question-archetypes.md#BC-QA-05004 Intervals of concavity from derivative information with a reason",
  "research/scoring/justification-requirements.md#Reasons tied to the object the prompt names",
  "research/scoring/common-point-losses.md#Justification points",
  "research/exam/exam-structure.md#Section and part layout"
 ],
 "word_count": {
  "full": 579,
  "brief": 442
 },
 "read_minutes": {
  "full": 3.9,
  "brief": 3.0
 }
}
```
