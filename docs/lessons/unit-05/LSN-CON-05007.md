---
title: LSN-CON-05007 Concavity as the monotonicity of the first derivative
research_date: 2026-09-29
status: designed
purpose: Authoring spec for the concept lesson on BC-CON-05007, concavity as the monotonicity of the first derivative, built from authoring_bundle("BC-CON-05007") and the research files it cites, so an author fills plan 15's lesson record without making a teaching decision.
---

# LSN-CON-05007 Concavity as the monotonicity of the first derivative

Concept BC-CON-05007 (skills BC-SKL-05030, BC-SKL-05031), topic 5.6 of Unit 5, loaded by one archetype, BC-QA-05004 (family concavity-analysis). Unit parent BC-CON-05004 (docs/lessons/unit-05/README.md, section 1). The written reason, f' increasing or decreasing on the interval, is the object of the lesson; the sign of f' is the rival it displaces.

## Prediction

Both bands, first. Poses ex-1's own numbers: f' falls from 3 to 1 on (2, 3) and stays positive, and the student predicts the concavity there. Form `mcq`, two options, key A (concave down, since f' falls). The resolution says concavity follows f' falling, not its sign. Sources: BC-CON-05007 and the topic 5.6 section.

## Orientation

Served text, from BC-CON-05007 `description_plain` and the topic's Assessment behaviour paragraph (research/units/unit-05-analytical-applications-differentiation.md#5.6 Determining Concavity of Functions over Their Domains): a response reports open intervals where f' rises (concave up) or falls (concave down), and gives as reason the behaviour of f', not its sign. No count, no frequency.

## Key ideas

Two BC-EK map to the skills: BC-EK-FUN-4A4 (BC-SKL-05031) and BC-EK-FUN-4A5 (BC-SKL-05030), both on ced:104. Two core blocks, both bands.

- ki-1 (core, BC-EK-FUN-4A4). Paraphrase of the Required mathematical knowledge paragraph (Concavity; Justification standard): concave up where f' increases, down where it decreases; the reason discusses the behaviour or slopes of f' (sg-23:14). Anchor quote (22 words) from ced:104.
- ki-2 (core, BC-EK-FUN-4A5). The same test from a formula: f'' > 0 concave up, f'' < 0 concave down. No quote.

## Recognition

- BC-QA-05004 (research/question-analysis/question-archetypes.md#BC-QA-05004 Intervals of concavity from derivative information with a reason): `typical_wording` "on what open intervals, if any, is the graph of the function concave down, and give a reason for the answer"; `common_givens` a graph of the derivative, or a formula for the function; `asked_to_produce` a list of open intervals, a reason about the behaviour of the derivative. The signal: "concave" beside a graph labelled f'. FRQ appearances BC-FRQ-2013-Q4-C, BC-FRQ-2014-Q3-B, BC-FRQ-2023-Q4-B, BC-FRQ-2026-Q4-C, BC-FRQ-2018-Q3-C; MCQ BC-MCQ-PE2012-037.

What says "not this concept" (the contrast pair's near miss comes from BC-CON-05004, where the same graph asked for "increasing" calls for the sign of f', and from BC-ERR-05016, BC-MIS-05020): "increasing" asks for the sign of f' (BC-CON-05004, BC-ERR-05016); "point of inflection" asks where the concavity changes (BC-CON-05008).

## Method choice

One strategy block, both bands.

- st-1, BC-QA-05004. Method, `expected_solution_path[0]`: identify where the derivative is decreasing (or increasing, for concave up). Rival, `wrong_approaches`: computing a second derivative formula when only a graph of the derivative is supplied; the scored rival is the sign of f' (BC-ERR-05031). Separating feature: concave asks whether f' rises, not whether it is positive. The archetype carries `asked_to_produce` and `common_givens`, so the block is not tagged inferred.

## Solution path

- ex-1, BC-QA-05004, both bands, no calculator. Draw: heights -2, 1, 3, 1, -1, 0, 2 at x = 0 to 6, asked down: f' falls on [2, 4], and the segment from x = 2 to 3 falls above the axis, as the constraint requires, so the sign reading differs. No published BC-QA-05004 item carries this draw. Steps follow `expected_solution_path`: where f' decreases (no value), the interval (new), the reason (no value, tagged BC-PT-99063).

A fluent solver writes the interval and the reason sentence; the segment reading is held in the head. Endpoints may be included (sg-23:14).

## Scoring

BC-QA-05004 lists BC-PT-99062 and BC-PT-99063. ex-1 tags BC-PT-99063 on the reason step; its line is `reader_checks(["BC-PT-99063"])`. The BC-PT-99062 line is not served, to hold the brief band under its cap. For the author: the reason point needs the intervals right, and one of two intervals with a reason earns one point (sg-23:14); a reason about f'' or "f changes concavity" where a graph of f' was given does not tie to the object (sg-25:17, research/scoring/justification-requirements.md#Reasons tied to the object the prompt names; research/scoring/justification-requirements.md#Reasons about slope fields and concavity).

## Traps

Four active errors meet the skills, all served in the bundle's order (low band all four, mid band the first two).

- err-BC-ERR-05015: a feature of the drawn curve read as a feature of f. Statement-shaped. Possible reason, words from BC-MIS-05011.
- err-BC-ERR-05016: f increasing reported where f' rises and concavity was asked, on (4, 6). Statement-shaped. Possible reason, words from BC-MIS-05020.
- err-BC-ERR-05030: the slope of f' on (4, 5) read as negative, giving (2, 5). No possible reason line.
- err-BC-ERR-05031: concave down where f' < 0, giving (0, 2/3) and (7/2, 5). Possible reason, words from BC-MIS-05020.

## Representations

None as a separate block. The topic's Representations paragraph names the graph of f' to intervals of concavity (BC-REP-02 to BC-REP-04), which ki-1's interactive carries.

## Prerequisite bridge

- BC-PRQ-05001, BC-PRQ-05002, BC-PRQ-05006, each from its `description_plain` and `failure_signature`.

## Time

BC-QA-05004 has `calculator_status` either, so the lesson takes Section I Part A, 2.14 minutes per question (research/exam/exam-structure.md#Section and part layout) [inferred: as an FRQ part it is 2 points, 3.3 minutes on the README's per-point share]. The minutes go on reading which segments fall; the reason is one sentence.

## Checks

- chk-1, completion of ex-1, both bands: the falling stretch is given, the student writes the interval. Key (2, 4).
- chk-2, isomorph, both bands. Draw: heights 2, -1, -3, -2, 1, -1, 0, asked up. Key (2, 4) union (5, 6).
- chk-3, MCQ, low band. Draw: heights 0, 2, 1, -1, -2, 1, 3, asked down. Key (1, 4). Distractors: (5/2, 14/3), where f' < 0 (BC-ERR-05031); (1, 5) and (0, 4), each from one segment slope misread (BC-ERR-05030). BC-ERR-05015 and BC-ERR-05016 produce no interval distinct from these on this draw, so two distractors share an error path.

## Delivery

- orientation: figure. Rule 4 on BC-REP-02 in BC-SKL-05031 (docs/lessons/unit-05/README.md, section 6).
- ki-1: interactive, a point sliding along the graph of f' with the tangent drawn on f. Rule 4 promoted by BC-QA-05004 `common_givens` "a graph of the derivative" and `difficulty_variables` "whether the question asks for concave up or concave down"; TEMPLATE names concavity against the tangent as an interactive case [inferred; settled by the modality A/B].
- ki-2: text. Rule 6; BC-SKL-05030 carries BC-REP-01 only.
- ex-1 and the four error blocks: step_reveal. Rule 1.

## Band plan

- Low (full): served order of 2026-09-29: prediction, orientation, the three bridges, ki-1, ki-2, st-1 with its contrast pair, ex-1 with its scoring line, chk-1, the four error blocks, chk-2, chk-3. 560 words, 3.8 minutes (cap 900 and 6).
- Mid (brief): prediction, orientation, the bridges, ki-1, ki-2, st-1 with its contrast pair, ex-1 with its scoring line, chk-1, err-BC-ERR-05015 and err-BC-ERR-05016, chk-2. 447 words, 3.0 minutes (cap 450 and 3). The orientation, key idea texts, strategy fields, bridges and ex-1 cues were shortened to hold the cap; the anchor quote stays.
- Refresher: ki-1, ki-2, err-BC-ERR-05015, err-BC-ERR-05016, err-BC-ERR-05030, err-BC-ERR-05031, ex-1.

## Sources

- Prediction and contrast pair: BC-CON-05007, BC-CON-05004, BC-ERR-05016, BC-MIS-05020 (as above).

- BC-CON-05007; BC-SKL-05030, BC-SKL-05031; BC-EK-FUN-4A4, BC-EK-FUN-4A5; ced:104
- BC-QA-05004; BC-FRQ-2013-Q4-C, BC-FRQ-2014-Q3-B, BC-FRQ-2023-Q4-B, BC-FRQ-2026-Q4-C, BC-FRQ-2018-Q3-C, BC-MCQ-PE2012-037
- BC-PT-99063, BC-PT-99062; sg-23:14, sg-25:17
- BC-ERR-05015, BC-ERR-05016, BC-ERR-05030, BC-ERR-05031; BC-MIS-05011, BC-MIS-05020
- BC-PRQ-05001, BC-PRQ-05002, BC-PRQ-05006
- research/units/unit-05-analytical-applications-differentiation.md#5.6 Determining Concavity of Functions over Their Domains
- research/question-analysis/question-archetypes.md#BC-QA-05004 Intervals of concavity from derivative information with a reason
- research/scoring/justification-requirements.md#Reasons tied to the object the prompt names
- research/scoring/justification-requirements.md#Reasons about slope fields and concavity
- research/exam/exam-structure.md#Section and part layout
- [inferred] BC-QA-05004 is an either archetype placed in Section I Part A. Settled by a calculator_status of calculator or no_calculator on the archetype.
- [inferred] The orientation figure and the ki-1 interactive. Settled by the modality A/B.

## Machine record

```json
{
 "id": "LSN-CON-05007",
 "kind": "concept",
 "target_id": "BC-CON-05007",
 "unit": "05",
 "skills": [
  "BC-SKL-05030",
  "BC-SKL-05031"
 ],
 "prediction": {
  "id": "pr-1",
  "stem": {
   "text": "f' falls from 3 to 1 on (2, 3). Is f concave up or concave down there?",
   "command_verb": "predict"
  },
  "format": "mcq",
  "options": [
   {
    "id": "A",
    "label": "Down, since f' falls",
    "is_key": true
   },
   {
    "id": "B",
    "label": "Up, since f' is positive",
    "is_key": false
   }
  ],
  "resolution": "f' falls from 3 to 1 on (2, 3), so f is concave down there. Concavity follows f' falling, not its sign.",
  "sources": [
   "BC-CON-05007",
   "research/units/unit-05-analytical-applications-differentiation.md#5.6 Determining Concavity of Functions over Their Domains"
  ]
 },
 "orientation": {
  "text": "A response reports open intervals where f' rises or falls, with that as the reason.",
  "sources": [
   "BC-CON-05007",
   "research/units/unit-05-analytical-applications-differentiation.md#5.6 Determining Concavity of Functions over Their Domains"
  ]
 },
 "key_ideas": [
  {
   "id": "ki-1",
   "ek_id": "BC-EK-FUN-4A4",
   "depth": "core",
   "text": "The reason names f' rising or falling, not its sign.",
   "notation": "concavity",
   "quote": {
    "text": "The graph of a function is concave up (down) on an open interval if the function's derivative is increasing (decreasing) on that interval.",
    "source": "ced:104"
   },
   "sources": [
    "BC-EK-FUN-4A4",
    "ced:104",
    "sg-23:14",
    "research/units/unit-05-analytical-applications-differentiation.md#5.6 Determining Concavity of Functions over Their Domains"
   ]
  },
  {
   "id": "ki-2",
   "ek_id": "BC-EK-FUN-4A5",
   "depth": "core",
   "text": "From f'': positive is up, negative down.",
   "notation": "f''",
   "quote": null,
   "sources": [
    "BC-EK-FUN-4A5",
    "ced:104",
    "research/units/unit-05-analytical-applications-differentiation.md#5.6 Determining Concavity of Functions over Their Domains"
   ]
  }
 ],
 "strategy": [
  {
   "id": "st-1",
   "archetype_id": "BC-QA-05004",
   "cue": "Concave, from a graph of f'?",
   "method": "Where f' decreases.",
   "rival": "Where f' is negative.",
   "separating_feature": "Concave asks whether f' rises.",
   "sources": [
    "BC-QA-05004"
   ],
   "evidence_tag": "verified",
   "contrast": {
    "this": {
     "text": "f' joins (0, 1), (2, 3), (4, -1), (6, 2). Where is f concave up?",
     "archetype_id": "BC-QA-05004"
    },
    "not_this": {
     "text": "f' joins (0, 1), (2, 3), (4, -1), (6, 2). Where is f increasing?",
     "why_not": "Increasing asks for the sign of f'."
    },
    "feature": "Concave: f' rises. Increasing: f' is positive."
   }
  }
 ],
 "worked_examples": [
  {
   "id": "ex-1",
   "archetype_id": "BC-QA-05004",
   "bands": [
    "low",
    "mid"
   ],
   "parameter_draw": {
    "heights": [
     -2,
     1,
     3,
     1,
     -1,
     0,
     2
    ],
    "asked": "down"
   },
   "problem": {
    "text": "The graph of f' joins (0, -2), (1, 1), (2, 3), (3, 1), (4, -1), (5, 0), (6, 2) by segments. Where is f concave down? Give a reason.",
    "command_verb": "find"
   },
   "calculator_status": "no_calculator",
   "steps": [
    {
     "cue": "Concave down: f' decreases.",
     "why": "f' falls from x = 2 to 4."
    },
    {
     "cue": "Open.",
     "why": "Endpoints optional.",
     "expr": "Interval.open(2, 4)",
     "relation": "new"
    },
    {
     "cue": "Reason.",
     "why": "f is concave down on (2, 4) because f' is decreasing.",
     "point_type_id": "BC-PT-99063"
    }
   ],
   "answer": {
    "form": "symbolic",
    "expr": "Interval.open(2, 4)"
   }
  }
 ],
 "what_a_reader_scores": [
  {
   "example_id": "ex-1",
   "point_type_ids": [
    "BC-PT-99063"
   ],
   "lines": [
    {
     "point_type_id": "BC-PT-99063",
     "text": "Reason for an interval answer citing the derivative's behaviour. Earned by: A reason citing the sign of the derivative and the increasing or decreasing behaviour of the derivative, matched to the compound condition asked (sg-26:16, sg-23:14). Not earned by: A reason addressing only one half of a compound condition, which sg-26:16 lists as two special cases earning the interval point but not this one."
    }
   ]
  }
 ],
 "common_errors": [
  {
   "error_id": "BC-ERR-05015",
   "wrong_step": {
    "text": "Where the drawn curve bends down.",
    "expr": "drawn_curve_bends_down"
   },
   "right_step": {
    "text": "Where f' falls.",
    "expr": "f_prime_decreasing"
   },
   "relation": "distinct",
   "possible_reason": {
    "misconception_id": "BC-MIS-05011",
    "text": "reading features of whatever curve is drawn"
   },
   "sources": [
    "BC-ERR-05015",
    "BC-MIS-05011"
   ],
   "observed_behavior": "The response answers a question about the function by describing features of the curve shown, which is the derivative.",
   "scoring_consequence": "Every part that rests on the plotted object is answered about the wrong function.",
   "fix_prompt": true
  },
  {
   "error_id": "BC-ERR-05016",
   "wrong_step": {
    "text": "f' rises on (4, 6), so f increases on (4, 6).",
    "expr": "f_increasing_on_4_6"
   },
   "right_step": {
    "text": "f' rises on (4, 6), so f is concave up on (4, 6).",
    "expr": "f_concave_up_on_4_6"
   },
   "relation": "distinct",
   "possible_reason": {
    "misconception_id": "BC-MIS-05020",
    "text": "does not distinguish rising from bending upward"
   },
   "sources": [
    "BC-ERR-05016",
    "BC-MIS-05020"
   ],
   "observed_behavior": "The response reports concavity where monotonicity was asked for, or reports increase of the function where the derivative graph is rising.",
   "scoring_consequence": "The intervals reported belong to the other question and the reason point is unavailable.",
   "fix_prompt": true
  },
  {
   "error_id": "BC-ERR-05030",
   "wrong_step": {
    "text": "Slope on (4, 5) read negative.",
    "expr": "Interval.open(2, 5)"
   },
   "right_step": {
    "text": "Slope 1 there.",
    "expr": "Interval.open(2, 4)"
   },
   "relation": "distinct",
   "possible_reason": null,
   "sources": [
    "BC-ERR-05030"
   ],
   "observed_behavior": "The response assigns the wrong sign to the second derivative on one interval of its sign chart.",
   "scoring_consequence": "The concavity intervals are wrong and the reason point is unavailable.",
   "fix_prompt": true
  },
  {
   "error_id": "BC-ERR-05031",
   "wrong_step": {
    "text": "Where f' < 0.",
    "expr": "Union(Interval.open(0, 2/3), Interval.open(7/2, 5))"
   },
   "right_step": {
    "text": "Where f' falls.",
    "expr": "Interval.open(2, 4)"
   },
   "relation": "distinct",
   "possible_reason": {
    "misconception_id": "BC-MIS-05020",
    "text": "the sign and the direction of the derivative are used interchangeably"
   },
   "sources": [
    "BC-ERR-05031",
    "BC-MIS-05020"
   ],
   "observed_behavior": "The response reports concave up where the plotted derivative is above the axis rather than where it is rising.",
   "scoring_consequence": "The intervals reported are those of increase, so both the interval point and the reason point are lost.",
   "fix_prompt": true
  }
 ],
 "representations": null,
 "prerequisite_bridges": [
  {
   "prq_id": "BC-PRQ-05001",
   "text": "Zeros."
  },
  {
   "prq_id": "BC-PRQ-05002",
   "text": "Signs."
  },
  {
   "prq_id": "BC-PRQ-05006",
   "text": "The curve is f'."
  }
 ],
 "time": {
  "exam_part": "I-A",
  "budget_minutes": 2.14,
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
   "archetype_id": "BC-QA-05004",
   "parameter_draw": {
    "heights": [
     -2,
     1,
     3,
     1,
     -1,
     0,
     2
    ],
    "asked": "down"
   },
   "completes": "ex-1",
   "stem": {
    "text": "The example's f' falls only from x = 2 to x = 4. Where is f concave down?",
    "command_verb": "find"
   },
   "key": {
    "form": "symbolic",
    "expr": "Interval.open(2, 4)"
   },
   "steps": [
    {
     "text": "Open interval.",
     "expr": "Interval.open(2, 4)",
     "relation": "new"
    }
   ],
   "calculator_status": "no_calculator",
   "skills": [
    "BC-SKL-05031"
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
   "archetype_id": "BC-QA-05004",
   "parameter_draw": {
    "heights": [
     2,
     -1,
     -3,
     -2,
     1,
     -1,
     0
    ],
    "asked": "up"
   },
   "stem": {
    "text": "f' joins heights 2, -1, -3, -2, 1, -1, 0 at x = 0 to 6. Where is f concave up?",
    "command_verb": "find"
   },
   "key": {
    "form": "symbolic",
    "expr": "Union(Interval.open(2, 4), Interval.open(5, 6))"
   },
   "steps": [
    {
     "text": "f' rises on (2, 4) and (5, 6).",
     "expr": "Union(Interval.open(2, 4), Interval.open(5, 6))",
     "relation": "new"
    }
   ],
   "calculator_status": "no_calculator",
   "skills": [
    "BC-SKL-05031"
   ]
  },
  {
   "id": "chk-3",
   "check_kind": "mcq",
   "format": "mcq",
   "bands": [
    "low"
   ],
   "archetype_id": "BC-QA-05004",
   "parameter_draw": {
    "heights": [
     0,
     2,
     1,
     -1,
     -2,
     1,
     3
    ],
    "asked": "down"
   },
   "stem": {
    "text": "f' joins heights 0, 2, 1, -1, -2, 1, 3 at x = 0 to 6. Where is f concave down?",
    "command_verb": "identify"
   },
   "key": {
    "form": "symbolic",
    "expr": "Interval.open(1, 4)"
   },
   "steps": [
    {
     "text": "f' falls from x = 1 to x = 4.",
     "expr": "Interval.open(1, 4)",
     "relation": "new"
    }
   ],
   "options": [
    {
     "id": "A",
     "is_key": false,
     "expr": "Interval.open(5/2, 14/3)",
     "error_path": "BC-ERR-05031",
     "derivation": "where f' < 0: zeros of f' at 5/2 and 14/3"
    },
    {
     "id": "B",
     "is_key": true,
     "expr": "Interval.open(1, 4)",
     "error_path": null
    },
    {
     "id": "C",
     "is_key": false,
     "expr": "Interval.open(1, 5)",
     "error_path": "BC-ERR-05030",
     "derivation": "slope 3 on (4, 5) read as negative"
    },
    {
     "id": "D",
     "is_key": false,
     "expr": "Interval.open(0, 4)",
     "error_path": "BC-ERR-05030",
     "derivation": "slope 2 on (0, 1) read as negative"
    }
   ],
   "calculator_status": "no_calculator",
   "skills": [
    "BC-SKL-05031"
   ]
  }
 ],
 "delivery": [
  {
   "block": "orientation",
   "mode": "figure",
   "reason": "rule 4: BC-REP-02 on BC-SKL-05031; unit README delivery map",
   "sources": [
    "BC-SKL-05031"
   ],
   "spec": {
    "kind": "graph",
    "representations": [
     "BC-REP-02"
    ],
    "curve": "f' through (0, -2), (1, 1), (2, 3), (3, 1), (4, -1), (5, 0), (6, 2)",
    "window": {
     "x": [
      0,
      6
     ],
     "y": [
      -3,
      4
     ]
    },
    "labels": [
     {
      "text": "graph of f'",
      "placement": "inside"
     },
     {
      "text": "f' falling: f concave down",
      "placement": "inside"
     },
     {
      "text": "f' rising: f concave up",
      "placement": "inside"
     }
    ]
   },
   "fallback": "the same graph static with the falling stretch shaded and labelled",
   "keyboard": "no control; the figure description is reached with Tab"
  },
  {
   "block": "ki-1",
   "mode": "interactive",
   "reason": "rule 4 promoted: BC-REP-02 on BC-SKL-05031; BC-QA-05004 common_givens a graph of the derivative and difficulty_variables concave up or concave down, a reading the stem tests",
   "sources": [
    "BC-SKL-05031",
    "BC-QA-05004"
   ],
   "spec": {
    "kind": "graph_pair",
    "representations": [
     "BC-REP-02"
    ],
    "top": "f' through (0, -2), (1, 1), (2, 3), (3, 1), (4, -1), (5, 0), (6, 2)",
    "bottom": {
     "curve": "1.25*x**2 - 6*x - 0.25*(x - 1)*abs(x - 1) - (x - 2)*abs(x - 2) + 0.75*(x - 4)*abs(x - 4) + 0.25*(x - 5)*abs(x - 5) + 14",
     "interval": [
      0,
      6
     ],
     "tangent": {
      "at": "x",
      "slope": "-6 + 2.5*x - 0.5*abs(x - 1) - 2*abs(x - 2) + 1.5*abs(x - 4) + 0.5*abs(x - 5)"
     }
    },
    "controls": [
     {
      "type": "slider",
      "name": "x",
      "domain": [
       0,
       6
      ],
      "step": 0.1,
      "readout": "is f' rising or falling at x"
     }
    ],
    "question": "Is f' rising here, and does the curve f bend above or below its tangent?",
    "labels": [
     {
      "text": "f'",
      "placement": "inside"
     },
     {
      "text": "f and its tangent",
      "placement": "inside"
     }
    ]
   },
   "fallback": "three static frames at x = 1, 3 and 5.5, each with f' rising or falling and the tangent on f",
   "keyboard": "Tab focuses the slider; Left and Right arrow keys move x by 0.1; Home and End jump to 0 and 6"
  },
  {
   "block": "ki-2",
   "mode": "text",
   "reason": "rule 6: BC-SKL-05030 carries BC-REP-01 only",
   "sources": [
    "BC-SKL-05030"
   ]
  },
  {
   "block": "ex-1",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  },
  {
   "block": "err-BC-ERR-05015",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  },
  {
   "block": "err-BC-ERR-05016",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  },
  {
   "block": "err-BC-ERR-05030",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  },
  {
   "block": "err-BC-ERR-05031",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  }
 ],
 "refresher": [
  "ki-1",
  "ki-2",
  "err-BC-ERR-05015",
  "err-BC-ERR-05016",
  "err-BC-ERR-05030",
  "err-BC-ERR-05031",
  "ex-1"
 ],
 "research_lines": [
  {
   "file": "research/scoring/justification-requirements.md",
   "line": "sg-26:16 requires a response to refer to the derivative and to cite both that it is positive and that it is decreasing"
  }
 ],
 "inferred": [
  {
   "claim": "BC-QA-05004 has calculator_status either, so the lesson places it in Section I Part A.",
   "settles": "A calculator_status of calculator or no_calculator on BC-QA-05004."
  },
  {
   "claim": "The orientation is a static figure and ki-1 an interactive slider.",
   "settles": "The modality A/B in the build plan: skip rate and time to first credited success by mode."
  }
 ],
 "sources": [
  "BC-CON-05007",
  "BC-EK-FUN-4A4",
  "BC-EK-FUN-4A5",
  "ced:104",
  "BC-QA-05004",
  "BC-PT-99063",
  "BC-PT-99062",
  "sg-23:14",
  "sg-25:17",
  "BC-ERR-05015",
  "BC-ERR-05016",
  "BC-ERR-05030",
  "BC-ERR-05031",
  "BC-MIS-05011",
  "BC-MIS-05020",
  "BC-PRQ-05001",
  "BC-PRQ-05002",
  "BC-PRQ-05006",
  "research/units/unit-05-analytical-applications-differentiation.md#5.6 Determining Concavity of Functions over Their Domains",
  "research/question-analysis/question-archetypes.md#BC-QA-05004 Intervals of concavity from derivative information with a reason",
  "research/scoring/justification-requirements.md#Reasons tied to the object the prompt names",
  "research/scoring/justification-requirements.md#Reasons about slope fields and concavity",
  "research/exam/exam-structure.md#Section and part layout"
 ],
 "word_count": {
  "full": 559,
  "brief": 446
 },
 "read_minutes": {
  "full": 3.8,
  "brief": 3.0
 }
}
```
