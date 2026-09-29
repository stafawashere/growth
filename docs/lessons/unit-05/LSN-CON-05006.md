---
title: LSN-CON-05006 Candidates test for absolute extrema on a closed interval
research_date: 2026-09-29
status: designed
purpose: Authoring spec for the concept lesson on BC-CON-05006, the candidates test for absolute extrema on a closed interval, built from authoring_bundle("BC-CON-05006") and the research files it cites, so an author fills plan 15's lesson record without making a teaching decision.
---

# LSN-CON-05006 Candidates test for absolute extrema on a closed interval

Concept BC-CON-05006 (skills BC-SKL-05024 to BC-SKL-05029), topic 5.5 of Unit 5, loaded by one archetype, BC-QA-05006 (family absolute-extremum-candidates). Unit parents BC-CON-05003 and BC-CON-05004 (docs/lessons/unit-05/README.md, section 1). The written justification, every candidate evaluated and no other input, is the object of the lesson.

## Prediction

Both bands, first. Poses ex-1's own function: f(x) = x^3 - 3x has a relative maximum at x = -1, and the student predicts where the absolute maximum on [-2, 3] sits. Form `mcq`, three options, key B, the endpoint x = 3. The resolution lists the four candidates with their values and says an endpoint can hold the extremum. No rule is stated in the stem. Sources: BC-CON-05006 and the topic 5.5 section.

## Orientation

Served text, from BC-CON-05006 `description_plain` and the topic's Assessment behaviour paragraph (research/units/unit-05-analytical-applications-differentiation.md#5.5 Using the Candidates Test to Determine Absolute (Global) Extrema): a response writes f'(x) = 0, lists the critical points inside the interval and both endpoints, evaluates f at each and at nothing else, and reports the extreme value. No count, no frequency.

## Key ideas

All six skills map to BC-EK-FUN-4A3 (ced:103), so one core block, both bands.

- ki-1 (core). Paraphrase of the Required mathematical knowledge paragraph (Candidates test; Global argument requirement; Value against location): absolute extrema on [a, b] occur only at interior critical points or endpoints; the justification covers every candidate and no other input (sg-25:19), with both endpoints (sg-23:15); the answer is the value (sg-23:15). Anchor quote (18 words) from ced:103. Notation line from the concept record.

## Recognition

- BC-QA-05006 (research/question-analysis/question-archetypes.md#BC-QA-05006 Absolute extremum by the candidates test with a global justification): `typical_wording` "find the absolute minimum value of the function on the closed interval and justify the answer"; `common_givens` a function or its derivative, one known function value, a closed interval; `asked_to_produce` the derivative condition considered, a candidate table, the extremum. The signal: "absolute" with "on the closed interval". FRQ appearances BC-FRQ-2013-Q4-B, BC-FRQ-2022-Q3-D, BC-FRQ-2023-Q4-D, BC-FRQ-2025-Q1-D, BC-FRQ-2025-Q4-D, BC-FRQ-2026-Q4-D; the Unit 5 with Unit 6 pairing builds the candidate values from an accumulation function (research/question-analysis/frq-analysis.md#How concepts combine inside one question).

What says "not this concept": the contrast pair's near miss comes from the local-test rival (BC-ERR-99004) and from the first derivative test of BC-CON-05005, so `not_this` asks to justify a relative extremum at one input. "Relative" at a named input is a first derivative test (BC-CON-05005), where a candidates test does not earn the classification point (sg-26:8); "must f attain" is existence only (BC-CON-05002).

## Method choice

One strategy block, both bands.

- st-1, BC-QA-05006. Method, `expected_solution_path[0]`: consider the derivative equal to zero and solve. Rival, `wrong_approaches`: appealing to the Extreme Value Theorem as though it located the extremum; the local-test rival is the one scored against (sg-25:5, research/scoring/justification-requirements.md#Global versus local arguments). Separating feature: "absolute" on a closed interval makes every candidate a competitor. The archetype carries `asked_to_produce` and `common_givens`, so the block is not tagged inferred. The local-test rival is sourced by BC-ERR-99004, which the block cites.

## Solution path

- ex-1, BC-QA-05006, both bands, no calculator. Draw (cubic family): first_critical -1, gap 2, left 1, right 2, orientation 1, shift 0, extreme maximum, root 2, coefficient 1. By the spec's derived values f(x) = x^3 - 3x on [-2, 3], value_low -2, value_high 18, value_first 2, value_second -2; best 18 at the endpoint, local_best 2, as the notes intend. Steps: f' = 0 (new), roots (solve), the candidate list (new), f (new), the values (new), the comparison (new, tagged BC-PT-99011).
- ex-2, BC-QA-05006, low band, faded from step 4 (`fade_from` 4). Steps 1 to 3 (the equation, the roots, the candidate list with -2 discarded) are shown, so the student meets the interval check first and then writes the values and the comparison. The fade falls there because the two withheld steps are the ones ex-1 has already modelled.
- ex-2 detail:  Draw (reciprocal family): first_critical 0, gap 2, left 1, right 2, orientation 1, shift 0, extreme minimum, root 2, coefficient 1; f(x) = x + 4/x on [1, 4]. The critical point -2 lies outside and is discarded; minimum value 4.

No published BC-QA-05006 item carries either draw. A fluent solver writes the equation, the candidate table and the sentence naming the value; the solving is held in the head.

## Scoring

BC-QA-05006 lists BC-PT-99013, 99004, 99011 and 99005. ex-1 tags BC-PT-99011 on the comparison, the justification point; its line is `reader_checks(["BC-PT-99011"])`. The BC-PT-99013 line is not served, to hold the brief band under its cap; the equation step is written in full instead. ex-2 tags no point, so its entry is empty. For the author: an evaluation error or a missing endpoint loses the justification (sg-23:15, research/scoring/justification-requirements.md#The candidates test); candidate values are held to the first decimal (sg-25:5); a local argument where a global one was required is a named loss (research/scoring/common-point-losses.md#Justification points).

## Traps

Eight active errors meet the skills; the first four in the bundle's order are served (low band all four, mid band the first two). BC-ERR-99004, 99034, 05024 and 05028 are left out by the cap of 4.

- err-BC-ERR-05011: zeros of f' only, against zeros and undefined points. Statement-shaped (the ex-1 f' is defined everywhere). Possible reason, words from BC-MIS-05009.
- err-BC-ERR-05025 on ex-2: x = -2 kept, giving -4, against 4. No possible reason line.
- err-BC-ERR-05026 on ex-1: the endpoints dropped, giving 2, against 18. Possible reason, words from BC-MIS-05016.
- err-BC-ERR-05027 on ex-1: f(3) taken as 24, against 18. No possible reason line.

## Representations

One block, low band: the topic's Representations paragraph names the conversion of a candidate table to a single extreme value (BC-REP-03 to BC-REP-04), served as ex-1's candidate table.

## Prerequisite bridge

- BC-PRQ-05004 and BC-PRQ-06005, each from its `description_plain` and `failure_signature`.

## Time

BC-QA-05006 has `calculator_status` either, so the lesson takes Section I Part A, 2.14 minutes per question (research/exam/exam-structure.md#Section and part layout) [inferred: as an FRQ part it is 3 points, 5.0 minutes on the README's per-point share]. The minutes go on the evaluations, since one wrong entry costs the justification.

## Checks

- chk-1, completion of ex-1, both bands: the candidate values are given, the student compares. Key 18.
- chk-2, isomorph, both bands. Draw: first_critical 0, gap 2, left 2, right 3, orientation -1, shift 4, extreme minimum, root 2, coefficient 1, cubic; f(x) = -x^3 + 3x^2 + 4 on [-2, 5]. Key -46.
- chk-3, MCQ, low band. Draw: first_critical 0, gap 2, left 2, right 3, orientation 1, shift 0, extreme minimum, root 3, coefficient 1, reciprocal; f(x) = x + 9/x on [1, 6]. Key: the complete response, minimum value 6. Distractors: -3 kept (BC-ERR-05025), only x = 3 argued (BC-ERR-05026), f(3) misevaluated as 10/3 (BC-ERR-05027). The key is a response, so a statement key with labels.

## Delivery

- orientation: text. Rule 5, per the unit delivery map.
- ki-1: figure, a graph of f' with the candidate list marked. Rule 3 on BC-REP-02 in BC-SKL-05024, 05025 [inferred; settled by the modality A/B].
- representations: table. Rule 4 on BC-REP-03 in BC-SKL-05026, 05028.
- ex-1, ex-2 and the four error blocks: step_reveal. Rule 1.

## Band plan

- Low (full): served order of 2026-09-29: prediction, orientation, the two bridges, ki-1, st-1 with its contrast pair, ex-1 with its scoring line, chk-1, the four error blocks, ex-2 faded from step 4, chk-2, representations, chk-3. 687 words, 4.6 minutes (cap 900 and 6).
- Mid (brief): prediction, orientation, the two bridges, ki-1, st-1 with its contrast pair, ex-1 with its scoring line, chk-1, err-BC-ERR-05011 and err-BC-ERR-05025, chk-2. 448 words, 3.0 minutes (cap 450 and 3). The orientation, ki-1 text, strategy fields, bridges and ex-1 cues were shortened to hold the cap; the anchor quote stays.
- Refresher: ki-1, err-BC-ERR-05011, err-BC-ERR-05025, err-BC-ERR-05026, err-BC-ERR-05027, ex-1.

## Sources

- Prediction and contrast pair: BC-CON-05006, BC-ERR-99004, sg-26:8 (as above).

- BC-CON-05006; BC-SKL-05024 to BC-SKL-05029; BC-EK-FUN-4A3; ced:103
- BC-QA-05006; BC-FRQ-2013-Q4-B, BC-FRQ-2022-Q3-D, BC-FRQ-2023-Q4-D, BC-FRQ-2025-Q1-D, BC-FRQ-2025-Q4-D, BC-FRQ-2026-Q4-D
- BC-PT-99011, BC-PT-99013, BC-PT-99004, BC-PT-99005; sg-23:15, sg-25:19, sg-25:5, sg-26:8
- BC-ERR-05011, BC-ERR-05025, BC-ERR-05026, BC-ERR-05027, BC-ERR-99004, BC-ERR-99034, BC-ERR-05024, BC-ERR-05028; BC-MIS-05009, BC-MIS-05016
- BC-PRQ-05004, BC-PRQ-06005
- research/units/unit-05-analytical-applications-differentiation.md#5.5 Using the Candidates Test to Determine Absolute (Global) Extrema
- research/question-analysis/question-archetypes.md#BC-QA-05006 Absolute extremum by the candidates test with a global justification
- research/scoring/justification-requirements.md#The candidates test
- research/scoring/justification-requirements.md#Global versus local arguments
- research/scoring/common-point-losses.md#Justification points
- research/question-analysis/frq-analysis.md#How concepts combine inside one question
- research/exam/exam-structure.md#Section and part layout
- [inferred] BC-QA-05006 is an either archetype placed in Section I Part A. Settled by a calculator_status of calculator or no_calculator on the archetype.
- [inferred] ki-1 as a figure and the representations block as a table. Settled by the modality A/B.

## Machine record

```json
{
 "id": "LSN-CON-05006",
 "kind": "concept",
 "target_id": "BC-CON-05006",
 "unit": "05",
 "skills": [
  "BC-SKL-05024",
  "BC-SKL-05025",
  "BC-SKL-05026",
  "BC-SKL-05027",
  "BC-SKL-05028",
  "BC-SKL-05029"
 ],
 "prediction": {
  "id": "pr-1",
  "stem": {
   "text": "Predict. f(x) = x^3 - 3x has a relative maximum at x = -1. Where is its absolute maximum on [-2, 3]?",
   "command_verb": "predict"
  },
  "format": "mcq",
  "options": [
   {
    "id": "A",
    "label": "At the relative maximum",
    "is_key": false
   },
   {
    "id": "B",
    "label": "At the endpoint x = 3",
    "is_key": true
   },
   {
    "id": "C",
    "label": "At the other critical point",
    "is_key": false
   }
  ],
  "resolution": "The values at -2, -1, 1 and 3 are -2, 2, -2 and 18. The largest, 18, is at the endpoint x = 3.",
  "sources": [
   "BC-CON-05006",
   "research/units/unit-05-analytical-applications-differentiation.md#5.5 Using the Candidates Test to Determine Absolute (Global) Extrema"
  ]
 },
 "orientation": {
  "text": "A response writes f'(x) = 0, evaluates f at every candidate, and reports the extreme value.",
  "sources": [
   "BC-CON-05006",
   "research/units/unit-05-analytical-applications-differentiation.md#5.5 Using the Candidates Test to Determine Absolute (Global) Extrema"
  ]
 },
 "key_ideas": [
  {
   "id": "ki-1",
   "ek_id": "BC-EK-FUN-4A3",
   "depth": "core",
   "text": "Evaluate f at every candidate and nowhere else. Report the value.",
   "notation": "candidate list; absolute extreme value",
   "quote": {
    "text": "Absolute (global) extrema of a function on a closed interval can only occur at critical points or at endpoints.",
    "source": "ced:103"
   },
   "sources": [
    "BC-EK-FUN-4A3",
    "ced:103",
    "sg-25:19",
    "sg-23:15",
    "research/units/unit-05-analytical-applications-differentiation.md#5.5 Using the Candidates Test to Determine Absolute (Global) Extrema"
   ]
  }
 ],
 "strategy": [
  {
   "id": "st-1",
   "archetype_id": "BC-QA-05006",
   "cue": "Absolute extreme value on a closed interval?",
   "method": "f'(x) = 0, as an equation.",
   "rival": "A local test at one point.",
   "separating_feature": "Absolute makes every candidate compete.",
   "sources": [
    "BC-QA-05006",
    "BC-ERR-99004"
   ],
   "evidence_tag": "verified",
   "contrast": {
    "this": {
     "text": "f(x) = x^3 - 12x. Find the absolute maximum value on [-4, 5]. Justify.",
     "archetype_id": "BC-QA-05006"
    },
    "not_this": {
     "text": "f(x) = x^3 - 12x. Justify a relative minimum at x = 2.",
     "why_not": "Relative at one input asks for a derivative test."
    },
    "feature": "Absolute on a closed interval."
   }
  }
 ],
 "worked_examples": [
  {
   "id": "ex-1",
   "archetype_id": "BC-QA-05006",
   "bands": [
    "low",
    "mid"
   ],
   "parameter_draw": {
    "first_critical": -1,
    "gap": 2,
    "left": 1,
    "right": 2,
    "orientation": 1,
    "shift": 0,
    "extreme": "maximum",
    "root": 2,
    "coefficient": 1,
    "family": "cubic"
   },
   "problem": {
    "text": "f(x) = x^3 - 3x. Find the absolute maximum value of f on [-2, 3]. Justify.",
    "command_verb": "find"
   },
   "calculator_status": "no_calculator",
   "steps": [
    {
     "cue": "Absolute on [-2, 3].",
     "why": "Write f'(x) = 0 as an equation.",
     "expr": "3*x**2 - 3 = 0",
     "relation": "new"
    },
    {
     "cue": "Solve.",
     "why": "Both inside.",
     "expr": "FiniteSet(-1, 1)",
     "relation": "solve",
     "variable": "x"
    },
    {
     "cue": "Add the endpoints.",
     "why": "Endpoints compete.",
     "expr": "FiniteSet(-2, -1, 1, 3)",
     "relation": "new"
    },
    {
     "cue": "Evaluate f.",
     "why": "f at -2, -1, 1, 3.",
     "expr": "Tuple(-2, 2, -2, 18)",
     "relation": "new"
    },
    {
     "cue": "Compare.",
     "why": "18 is largest, so the absolute maximum value is 18.",
     "expr": "18",
     "relation": "new",
     "point_type_id": "BC-PT-99011"
    }
   ],
   "answer": {
    "form": "numeric",
    "expr": "18"
   }
  },
  {
   "id": "ex-2",
   "archetype_id": "BC-QA-05006",
   "bands": [
    "low"
   ],
   "parameter_draw": {
    "first_critical": 0,
    "gap": 2,
    "left": 1,
    "right": 2,
    "orientation": 1,
    "shift": 0,
    "extreme": "minimum",
    "root": 2,
    "coefficient": 1,
    "family": "reciprocal"
   },
   "problem": {
    "text": "f(x) = x + 4/x. Find the absolute minimum value on [1, 4]. Justify.",
    "command_verb": "find"
   },
   "calculator_status": "no_calculator",
   "steps": [
    {
     "cue": "Absolute: f'(x) = 0.",
     "why": "f'(x) = 1 - 4/x^2.",
     "expr": "1 - 4/x**2 = 0",
     "relation": "new"
    },
    {
     "cue": "Solve.",
     "why": "Two roots.",
     "expr": "FiniteSet(-2, 2)",
     "relation": "solve",
     "variable": "x"
    },
    {
     "cue": "Inside [1, 4]?",
     "why": "-2 is not a candidate.",
     "expr": "FiniteSet(1, 2, 4)",
     "relation": "new"
    },
    {
     "cue": "Evaluate.",
     "why": "f(1) = 5, f(2) = 4, f(4) = 5.",
     "expr": "Tuple(5, 4, 5)",
     "relation": "new"
    },
    {
     "cue": "Compare.",
     "why": "Smallest is 4.",
     "expr": "4",
     "relation": "new"
    }
   ],
   "answer": {
    "form": "numeric",
    "expr": "4"
   },
   "fade_from": 4
  }
 ],
 "what_a_reader_scores": [
  {
   "example_id": "ex-1",
   "point_type_ids": [
    "BC-PT-99011"
   ],
   "lines": [
    {
     "point_type_id": "BC-PT-99011",
     "text": "Justification by candidates test. Earned by: A global argument that evaluates the function at every interior critical point and at both endpoints, with the evaluations correct to the stated precision (sg-25:5, sg-25:19). Not earned by: A candidates table missing an endpoint (sg-23:15), containing an evaluation error (sg-23:15), or listing extra x-values (sg-25:19). Precision: sg-25:5 and sg-25:9 require candidate evaluations correct to the first digit after the decimal, rounded or truncated; sg-22:5 allows up to three decimals or correctly rounded integers."
    }
   ]
  },
  {
   "example_id": "ex-2",
   "point_type_ids": [],
   "lines": []
  }
 ],
 "common_errors": [
  {
   "error_id": "BC-ERR-05011",
   "wrong_step": {
    "text": "Only where f' = 0.",
    "expr": "zeros_of_f_prime_only"
   },
   "right_step": {
    "text": "Also where f' fails to exist.",
    "expr": "zeros_and_undefined_points_of_f_prime"
   },
   "relation": "distinct",
   "possible_reason": {
    "misconception_id": "BC-MIS-05009",
    "text": "does not look for corners, cusps, or vertical tangents"
   },
   "sources": [
    "BC-ERR-05011",
    "BC-MIS-05009"
   ],
   "observed_behavior": "The response finds only the zeros of the derivative and skips corners, cusps, and vertical tangents.",
   "scoring_consequence": "A candidate is missing, so the comparison may select the wrong extremum and the justification is incomplete.",
   "fix_prompt": true
  },
  {
   "error_id": "BC-ERR-05025",
   "wrong_step": {
    "text": "x = -2 kept: -4.",
    "expr": "-4"
   },
   "right_step": {
    "text": "Inside [1, 4] only: 4.",
    "expr": "4"
   },
   "relation": "distinct",
   "possible_reason": null,
   "sources": [
    "BC-ERR-05025"
   ],
   "observed_behavior": "The response carries a critical point that lies outside the closed interval into the candidate comparison.",
   "scoring_consequence": "The justification point is lost because inputs other than the candidates appear in the argument.",
   "fix_prompt": true
  },
  {
   "error_id": "BC-ERR-05026",
   "wrong_step": {
    "text": "Endpoints dropped: 2.",
    "expr": "2"
   },
   "right_step": {
    "text": "f(3) = 18 wins.",
    "expr": "18"
   },
   "relation": "distinct",
   "possible_reason": {
    "misconception_id": "BC-MIS-05016",
    "text": "builds the candidate list from the interior critical points and does not regard the endpoints as competitors"
   },
   "sources": [
    "BC-ERR-05026",
    "BC-MIS-05016"
   ],
   "observed_behavior": "The response compares values only at the interior critical points and never evaluates at the ends of the interval.",
   "scoring_consequence": "The justification point is lost; the 2023 guideline states that a response not considering both endpoints does not earn it.",
   "fix_prompt": true
  },
  {
   "error_id": "BC-ERR-05027",
   "wrong_step": {
    "text": "f(3) = 27 - 3 = 24.",
    "expr": "3**3 - 3"
   },
   "right_step": {
    "text": "f(3) = 27 - 9 = 18.",
    "expr": "3**3 - 3*3"
   },
   "relation": "distinct",
   "possible_reason": null,
   "sources": [
    "BC-ERR-05027"
   ],
   "observed_behavior": "One entry of the candidate table is wrong, whether by substitution or by an area computation.",
   "scoring_consequence": "The justification point is lost outright; the 2023 guideline withholds it for any evaluation error at a candidate.",
   "fix_prompt": true
  }
 ],
 "representations": {
  "text": "Every candidate, one row each; the answer is the value column's extreme.",
  "figure": {
   "kind": "table",
   "columns": [
    "x",
    "-2",
    "-1",
    "1",
    "3"
   ],
   "rows": [
    [
     "f(x)",
     "-2",
     "2",
     "-2",
     "18"
    ]
   ],
   "labels": [
    {
     "text": "largest: 18",
     "placement": "inside"
    }
   ]
  }
 },
 "prerequisite_bridges": [
  {
   "prq_id": "BC-PRQ-05004",
   "text": "[a, b] includes both endpoints."
  },
  {
   "prq_id": "BC-PRQ-06005",
   "text": "f(3) is a value of f."
  }
 ],
 "time": {
  "exam_part": "I-A",
  "budget_minutes": 2.14,
  "source": "research/exam/exam-structure.md#Section and part layout",
  "written_steps": {
   "ex-1": [
    1,
    3,
    4,
    5
   ],
   "ex-2": [
    1,
    3,
    4,
    5
   ]
  },
  "skipped_steps": {
   "ex-1": [
    2
   ],
   "ex-2": [
    2
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
   "archetype_id": "BC-QA-05006",
   "parameter_draw": {
    "first_critical": -1,
    "gap": 2,
    "left": 1,
    "right": 2,
    "orientation": 1,
    "shift": 0,
    "extreme": "maximum",
    "root": 2,
    "coefficient": 1,
    "family": "cubic"
   },
   "completes": "ex-1",
   "stem": {
    "text": "f(-2) = -2, f(-1) = 2, f(1) = -2, f(3) = 18. Absolute maximum value on [-2, 3]?",
    "command_verb": "find"
   },
   "key": {
    "form": "numeric",
    "expr": "18"
   },
   "steps": [
    {
     "text": "The values.",
     "expr": "Tuple(-2, 2, -2, 18)",
     "relation": "new"
    },
    {
     "text": "Largest.",
     "expr": "18",
     "relation": "new"
    }
   ],
   "calculator_status": "no_calculator",
   "skills": [
    "BC-SKL-05026",
    "BC-SKL-05027"
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
   "archetype_id": "BC-QA-05006",
   "parameter_draw": {
    "first_critical": 0,
    "gap": 2,
    "left": 2,
    "right": 3,
    "orientation": -1,
    "shift": 4,
    "extreme": "minimum",
    "root": 2,
    "coefficient": 1,
    "family": "cubic"
   },
   "stem": {
    "text": "f(x) = -x^3 + 3x^2 + 4. Absolute minimum value on [-2, 5]? Justify.",
    "command_verb": "find"
   },
   "key": {
    "form": "numeric",
    "expr": "-46"
   },
   "steps": [
    {
     "text": "f' = 0.",
     "expr": "-3*x**2 + 6*x = 0",
     "relation": "new"
    },
    {
     "text": "x = 0, 2.",
     "expr": "FiniteSet(0, 2)",
     "relation": "solve",
     "variable": "x"
    },
    {
     "text": "f at -2, 0, 2, 5.",
     "expr": "Tuple(24, 4, 8, -46)",
     "relation": "new"
    },
    {
     "text": "Smallest.",
     "expr": "-46",
     "relation": "new"
    }
   ],
   "calculator_status": "no_calculator",
   "skills": [
    "BC-SKL-05024",
    "BC-SKL-05026"
   ]
  },
  {
   "id": "chk-3",
   "check_kind": "mcq",
   "format": "mcq",
   "bands": [
    "low"
   ],
   "archetype_id": "BC-QA-05006",
   "parameter_draw": {
    "first_critical": 0,
    "gap": 2,
    "left": 2,
    "right": 3,
    "orientation": 1,
    "shift": 0,
    "extreme": "minimum",
    "root": 3,
    "coefficient": 1,
    "family": "reciprocal"
   },
   "stem": {
    "text": "f(x) = x + 9/x, f'(x) = 1 - 9/x^2. Which response justifies the absolute minimum value on [1, 6]?",
    "command_verb": "identify"
   },
   "key": {
    "form": "statement",
    "expr": "6",
    "label": "f(1) = 10, f(3) = 6, f(6) = 7.5: minimum value 6."
   },
   "steps": [],
   "options": [
    {
     "id": "A",
     "is_key": false,
     "label": "f(-3) = -6, f(1) = 10, f(3) = 6, f(6) = 7.5: minimum value -6.",
     "error_path": "BC-ERR-05025",
     "derivation": "the critical point -3, outside [1, 6], kept"
    },
    {
     "id": "B",
     "is_key": false,
     "label": "f(3) = 6, a relative minimum: minimum value 6.",
     "error_path": "BC-ERR-05026",
     "derivation": "both endpoints left out of the comparison"
    },
    {
     "id": "C",
     "is_key": true,
     "label": "f(1) = 10, f(3) = 6, f(6) = 7.5: minimum value 6.",
     "error_path": null
    },
    {
     "id": "D",
     "is_key": false,
     "label": "f(1) = 10, f(3) = 10/3, f(6) = 7.5: minimum value 10/3.",
     "error_path": "BC-ERR-05027",
     "derivation": "9/3 taken as 1/3 at the candidate x = 3"
    }
   ],
   "calculator_status": "no_calculator",
   "skills": [
    "BC-SKL-05024",
    "BC-SKL-05028"
   ]
  }
 ],
 "delivery": [
  {
   "block": "orientation",
   "mode": "text",
   "reason": "rule 5: a statement of what a response shows; unit README delivery map",
   "sources": [
    "BC-SKL-05028"
   ]
  },
  {
   "block": "ki-1",
   "mode": "figure",
   "reason": "rule 3: BC-REP-02 on BC-SKL-05024, 05025; the candidate list read from a graph of f'",
   "sources": [
    "BC-SKL-05024",
    "BC-SKL-05025"
   ],
   "spec": {
    "kind": "graph",
    "representations": [
     "BC-REP-02"
    ],
    "curve": "f'(x) = 3x^2 - 3",
    "window": {
     "x": [
      -2,
      3
     ],
     "y": [
      -4,
      24
     ]
    },
    "marks": [
     "zeros at x = -1 and x = 1",
     "endpoints x = -2 and x = 3 as vertical lines"
    ],
    "labels": [
     {
      "text": "graph of f'",
      "placement": "inside"
     },
     {
      "text": "candidates: -2, -1, 1, 3",
      "placement": "inside"
     }
    ]
   },
   "fallback": "the same graph static with the four candidates marked and labelled",
   "keyboard": "no control; the figure description is reached with Tab"
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
   "block": "err-BC-ERR-05011",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  },
  {
   "block": "err-BC-ERR-05025",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  },
  {
   "block": "err-BC-ERR-05026",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  },
  {
   "block": "err-BC-ERR-05027",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  },
  {
   "block": "representations",
   "mode": "table",
   "reason": "rule 4: BC-REP-03 on BC-SKL-05026, 05028",
   "sources": [
    "BC-SKL-05026",
    "BC-SKL-05028"
   ],
   "spec": {
    "kind": "table",
    "representations": [
     "BC-REP-03"
    ],
    "columns": [
     "x",
     "-2",
     "-1",
     "1",
     "3"
    ],
    "rows": [
     [
      "f(x)",
      "-2",
      "2",
      "-2",
      "18"
     ],
     [
      "role",
      "endpoint",
      "critical",
      "critical",
      "endpoint"
     ]
    ],
    "labels": [
     {
      "text": "largest value: 18, at x = 3",
      "placement": "inside"
     }
    ]
   },
   "fallback": "the table as plain text rows with the largest value named",
   "keyboard": "Tab moves between cells; no control"
  }
 ],
 "refresher": [
  "ki-1",
  "err-BC-ERR-05011",
  "err-BC-ERR-05025",
  "err-BC-ERR-05026",
  "err-BC-ERR-05027",
  "ex-1"
 ],
 "research_lines": [
  {
   "file": "research/scoring/justification-requirements.md",
   "line": "sg-23:15 states that a response presenting any error in evaluating at any critical point or endpoint will not earn the justification point"
  }
 ],
 "inferred": [
  {
   "claim": "BC-QA-05006 has calculator_status either, so the lesson places it in Section I Part A.",
   "settles": "A calculator_status of calculator or no_calculator on BC-QA-05006."
  },
  {
   "claim": "ki-1 is served as a figure and the representations block as a table rather than text.",
   "settles": "The modality A/B in the build plan: skip rate and time to first credited success by mode."
  }
 ],
 "sources": [
  "BC-CON-05006",
  "BC-EK-FUN-4A3",
  "ced:103",
  "BC-QA-05006",
  "BC-PT-99011",
  "BC-PT-99013",
  "BC-PT-99004",
  "BC-PT-99005",
  "sg-23:15",
  "sg-25:19",
  "sg-25:5",
  "sg-26:8",
  "BC-ERR-05011",
  "BC-ERR-05025",
  "BC-ERR-05026",
  "BC-ERR-05027",
  "BC-MIS-05009",
  "BC-MIS-05016",
  "BC-PRQ-05004",
  "BC-PRQ-06005",
  "research/units/unit-05-analytical-applications-differentiation.md#5.5 Using the Candidates Test to Determine Absolute (Global) Extrema",
  "research/question-analysis/question-archetypes.md#BC-QA-05006 Absolute extremum by the candidates test with a global justification",
  "research/scoring/justification-requirements.md#The candidates test",
  "research/scoring/justification-requirements.md#Global versus local arguments",
  "research/scoring/common-point-losses.md#Justification points",
  "research/question-analysis/frq-analysis.md#How concepts combine inside one question",
  "research/exam/exam-structure.md#Section and part layout"
 ],
 "word_count": {
  "full": 687,
  "brief": 448
 },
 "read_minutes": {
  "full": 4.6,
  "brief": 3.0
 }
}
```
