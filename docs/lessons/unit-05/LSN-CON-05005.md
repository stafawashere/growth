---
title: LSN-CON-05005 First derivative test for relative extrema
research_date: 2026-09-29
status: designed
purpose: Authoring spec for the concept lesson on BC-CON-05005, the first derivative test for relative extrema, built from authoring_bundle("BC-CON-05005") and the research files it cites, so an author fills plan 15's lesson record without making a teaching decision.
---

# LSN-CON-05005 First derivative test for relative extrema

Concept BC-CON-05005 (skills BC-SKL-05019 to BC-SKL-05023), topic 5.4 of Unit 5, loaded by BC-QA-05003 (primary) and BC-QA-05007, both in family extremum-classification. Unit parents BC-CON-05003 and BC-CON-05004 (docs/lessons/unit-05/README.md, section 1). The written reason, the sign change of f' at the input or its absence, is the object of the lesson.

## Prediction

One multiple choice question on worked example 1's own numbers, asked before the rule is shown: \(f'(x)=3(x-1)^2(x+2)\) with \(f'(1)=0\), and the student picks what f has at x = 1. The key is neither, ex-1's answer; the distractors are a relative minimum and a relative maximum, the two verdicts a zero of f' invites (BC-ERR-05013). The resolution, shown on the key idea screen beside the student's choice, states the sign of f' on both sides and its consequence. No verdict word. Sources: BC-CON-05005 and the topic 5.4 section the key idea cites (ced:102).

## Orientation

Served text, from BC-CON-05005 `description_plain` and the topic's Assessment behaviour paragraph (research/units/unit-05-analytical-applications-differentiation.md#5.4 Using the First Derivative Test to Determine Relative (Local) Extrema): a response classifies the critical point and gives the sign behaviour of f' there as the reason, in one sentence naming f'. An unsupported classification earns nothing (sg-23:13). No count, no frequency.

## Key ideas

All five skills map to BC-EK-FUN-4A2 (ced:102), so one core block, both bands.

- ki-1 (core). Paraphrase of the Required mathematical knowledge paragraph (First derivative test; Sign change is the whole content; Location against value): positive to negative is a maximum, negative to positive a minimum, no change neither; "does not change sign" is accepted, "positive before and after" is not (sg-23:13); the extreme value is f(c), a separate evaluation. The anchor quote is dropped: with the prediction and the contrast pair added the brief form passed its cap, and the orientation and the strategy fields were shortened first, then the quote as the last resort. Notation line from the concept record.

## Recognition

- BC-QA-05003 (research/question-analysis/question-archetypes.md#BC-QA-05003 Relative extremum classified from the behaviour of the first derivative): `typical_wording` "does the function have a relative minimum, a relative maximum, or neither at the named input, and give a reason for the answer"; `common_givens` a graph of the derivative made of segments and arcs, or a derivative formula, a named input; `asked_to_produce` the classification, a reason naming the sign behaviour of the derivative. The signal: "relative" and "neither" with a named input. FRQ appearances BC-FRQ-2013-Q4-A, BC-FRQ-2015-Q4-C, BC-FRQ-2015-Q5-B, BC-FRQ-2023-Q4-A.
- BC-QA-05007 (research/question-analysis/question-archetypes.md#BC-QA-05007 Critical point located and classified for a function given indirectly): "the input at which the modelled quantity has a critical point, and determine whether it is ... a relative minimum, a relative maximum, or neither", given a differential equation with a sign fact or an accumulation function. FRQ appearances BC-FRQ-2021-Q3-B, BC-FRQ-2015-Q5-C, BC-FRQ-2024-Q3-B, BC-FRQ-2026-Q2-C.

The near miss served in the contrast pair of st-1 comes from the sibling concept BC-CON-05006 and sg-25:5: the same derivative formula with the stem asking for the absolute maximum value on a closed interval, which the candidates test answers and a local sign argument does not. The pair differs in the one thing the feature names, relative at an input against absolute on an interval.

What says "not this concept": "absolute" on a closed interval asks for the candidates test (BC-CON-05006), and a local test does not earn that justification (sg-25:5).

## Method choice

Two strategy blocks; st-1 serves both bands, st-2 the low band.

- st-1, BC-QA-05003. Method, `expected_solution_path[0]`: locate the named input on the derivative information. Rival, `wrong_approaches`: the second derivative test where only the derivative graph is available and its slope is not discussed. Separating feature: f' is given, so its sign on each side is read directly.
- st-2, BC-QA-05007. Method: write the derivative from the given relation. Rival, `wrong_approaches`: solving the differential equation before locating the critical point. Separating feature: the relation already is the derivative.

Both archetypes carry `asked_to_produce` and `common_givens`; neither block is tagged inferred.

## Solution path

- ex-1, BC-QA-05003, both bands, no calculator. Draw: named 1, other -2, scale 3, sign positive, multiplicity 2, factor none, so f'(x) = 3(x - 1)^2(x + 2) by the spec's notes; side_sign = 3 > 0, as the constraint for multiplicity 2 requires, so the answer is neither. No published BC-QA-05003 item carries this draw. Steps follow `expected_solution_path`: f' (new), f'(1) = 0 (evaluate), the sign on each side (no value), the classification with its reason (no value, tagged BC-PT-99012).

A fluent solver writes one sentence, the classification and "f' does not change sign at x = 1"; the evaluation and the side signs are read, not written (sg-23:13 does not require intervals, and any given must be correct).

## Scoring

BC-QA-05003 lists BC-PT-99012 and BC-PT-99013. ex-1 tags BC-PT-99012 on the classification step; its line is `reader_checks(["BC-PT-99012"])`. For BC-QA-05003 classification and reason are one point, and "positive before and after" does not earn it (sg-23:13). For the author: a reason point is satisfied by one correctly targeted sentence (research/scoring/justification-requirements.md#Justify, give a reason, and give reasons); an unnamed referent forfeits it (sg-25:17, research/scoring/justification-requirements.md#Reasons tied to the object the prompt names; research/scoring/common-point-losses.md#Notation points).

## Traps

Eight active errors meet the skills; the first four in the bundle's order are served (low band all four, mid band the first two). BC-ERR-05022, 05023, 99001 and 05024 are left out by the cap of 4.

- err-BC-ERR-05013 on ex-1: an extremum declared at x = 1. Statement-shaped. Possible reason, words from BC-MIS-05008.
- err-BC-ERR-05018 on ex-1: "it does not change sign" against "f' does not change sign". Statement-shaped. No possible reason line: neither linked description names the missing referent.
- err-BC-ERR-05020 on ex-1: inputs 0 and 2 tested as candidates, against the critical points -2 and 1. No possible reason line.
- err-BC-ERR-05021 on ex-1 at x = -2: a maximum where f' goes from negative to positive. Possible reason, words from BC-MIS-05014.

## Representations

None as a separate block. The topic's Representations paragraph names the graph of f' to a classified critical point (BC-REP-02 to BC-REP-04), which ki-1's interactive carries.

## Prerequisite bridge

None. The bundle lists no BC-PRQ parent of BC-SKL-05019 to BC-SKL-05023.

## Time

BC-QA-05003 has `calculator_status` either, so the lesson takes Section I Part A, 2.14 minutes per question (research/exam/exam-structure.md#Section and part layout) [inferred: as an FRQ part it is 1 point, 1.7 minutes on the README's per-point share]. The minutes go on reading the sign of f' on each side; the sentence is short.

## Checks

- chk-1, completion of ex-1, both bands: f'(1) = 0 and the side signs are given, the student writes the classification with its reason. Key: neither.
- chk-2, isomorph, both bands. Draw: named -1, other 3, scale 2, sign positive, multiplicity 1, factor none; f'(x) = 2(x + 1)(x - 3). Key: relative maximum at x = -1.
- chk-3, MCQ, low band. Draw: named 0, other -3, scale 1, sign positive, multiplicity 2, factor none; f'(x) = x^2(x + 3). Key: a minimum at -3 only. Distractors: a minimum also at 0 (BC-ERR-05013), a maximum at -3 (BC-ERR-05021), the right list with "it" as referent (BC-ERR-05018). Verdicts, so statement keys with option labels.

## Delivery

- orientation: text. Rule 5, per the unit delivery map.
- ki-1: interactive, a point sliding through the named input on a graph of f', reading the sign each side; window x [-3, 2] and y [-50, 15], which holds f' from -48 at x = -3 to 12 at x = 2. Rule 3 promoted: BC-REP-02 on BC-SKL-05019 to 05021, with BC-QA-05003 `common_givens` "a named input" and `difficulty_variables` "whether the answer is neither" (docs/lessons/unit-05/README.md, section 6) [inferred; settled by the modality A/B].
- ex-1 and the four error blocks: step_reveal. Rule 1.

## Band plan

- Low (full), in served order: prediction, orientation, ki-1, st-1 with its contrast pair, st-2, ex-1 with its scoring line, chk-1, the four error blocks, chk-2, chk-3. 629 words, 4.2 minutes (cap 900 and 6). There is one worked example, so nothing is faded.
- Mid (brief): prediction, orientation, ki-1, st-1 with its contrast pair, ex-1 with its scoring line, chk-1, err-BC-ERR-05013, err-BC-ERR-05018, chk-2. 450 words, 3.0 minutes (cap 450 and 3).
- Refresher: ki-1, err-BC-ERR-05013, err-BC-ERR-05018, err-BC-ERR-05020, err-BC-ERR-05021, ex-1.

## Sources

- BC-CON-05005; BC-SKL-05019 to BC-SKL-05023; BC-EK-FUN-4A2; ced:102
- BC-CON-05006 (the sibling concept of the not-this stem in the contrast pair)
- BC-QA-05003, BC-QA-05007; BC-FRQ-2013-Q4-A, BC-FRQ-2015-Q4-C, BC-FRQ-2015-Q5-B, BC-FRQ-2023-Q4-A, BC-FRQ-2021-Q3-B, BC-FRQ-2015-Q5-C, BC-FRQ-2024-Q3-B, BC-FRQ-2026-Q2-C
- BC-PT-99012, BC-PT-99013; sg-23:13, sg-25:5, sg-25:17
- BC-ERR-05013, BC-ERR-05018, BC-ERR-05020, BC-ERR-05021, BC-ERR-05022, BC-ERR-05023, BC-ERR-99001, BC-ERR-05024; BC-MIS-05008, BC-MIS-05014
- research/units/unit-05-analytical-applications-differentiation.md#5.4 Using the First Derivative Test to Determine Relative (Local) Extrema
- research/question-analysis/question-archetypes.md#BC-QA-05003 Relative extremum classified from the behaviour of the first derivative
- research/question-analysis/question-archetypes.md#BC-QA-05007 Critical point located and classified for a function given indirectly
- research/scoring/justification-requirements.md#Justify, give a reason, and give reasons
- research/scoring/justification-requirements.md#Reasons tied to the object the prompt names
- research/scoring/common-point-losses.md#Notation points
- research/exam/exam-structure.md#Section and part layout
- [inferred] BC-QA-05003 is an either archetype placed in Section I Part A. Settled by a calculator_status of calculator or no_calculator on the archetype.
- [inferred] ki-1 as an interactive. Settled by the modality A/B.

## Machine record

```json
{
 "id": "LSN-CON-05005",
 "kind": "concept",
 "target_id": "BC-CON-05005",
 "unit": "05",
 "skills": [
  "BC-SKL-05019",
  "BC-SKL-05020",
  "BC-SKL-05021",
  "BC-SKL-05022",
  "BC-SKL-05023"
 ],
 "prediction": {
  "id": "pr-1",
  "stem": {
   "text": "Predict: f'(x) = 3(x - 1)^2(x + 2) and f'(1) = 0. What does f have at x = 1?",
   "command_verb": "predict"
  },
  "format": "mcq",
  "options": [
   {
    "id": "A",
    "label": "A relative minimum",
    "is_key": false
   },
   {
    "id": "B",
    "label": "A relative maximum",
    "is_key": false
   },
   {
    "id": "C",
    "label": "Neither",
    "is_key": true
   }
  ],
  "resolution": "Near 1, (x - 1)^2 and x + 2 are positive, so f' > 0 on both sides. f' does not change sign, so neither.",
  "sources": [
   "BC-CON-05005",
   "ced:102"
  ]
 },
 "orientation": {
  "text": "A response classifies the critical point and gives, as its reason, how the sign of f' behaves there.",
  "sources": [
   "BC-CON-05005",
   "research/units/unit-05-analytical-applications-differentiation.md#5.4 Using the First Derivative Test to Determine Relative (Local) Extrema",
   "sg-23:13"
  ]
 },
 "key_ideas": [
  {
   "id": "ki-1",
   "ek_id": "BC-EK-FUN-4A2",
   "depth": "core",
   "text": "At a critical point c: f' from positive to negative is a relative maximum, negative to positive a relative minimum, no sign change neither. Write \"f' does not change sign\".",
   "notation": "sign change of f'",
   "quote": null,
   "sources": [
    "BC-EK-FUN-4A2",
    "ced:102",
    "sg-23:13",
    "research/units/unit-05-analytical-applications-differentiation.md#5.4 Using the First Derivative Test to Determine Relative (Local) Extrema"
   ]
  }
 ],
 "strategy": [
  {
   "id": "st-1",
   "archetype_id": "BC-QA-05003",
   "cue": "Maximum, minimum or neither at a named input?",
   "method": "Locate the input on f'.",
   "rival": "The second derivative test.",
   "separating_feature": "f' is given; read its sign each side.",
   "sources": [
    "BC-QA-05003"
   ],
   "evidence_tag": "verified",
   "contrast": {
    "this": {
     "text": "f'(x) = 2(x + 3)^2(x - 4). Relative minimum, maximum or neither at x = 4?",
     "archetype_id": "BC-QA-05003"
    },
    "not_this": {
     "text": "f'(x) = 2(x + 3)^2(x - 4). Find the absolute maximum value of f on [-5, 6].",
     "why_not": "It asks for candidate values."
    },
    "feature": "Relative at an input, or absolute."
   }
  },
  {
   "id": "st-2",
   "archetype_id": "BC-QA-05007",
   "cue": "Critical point of a quantity given by a differential equation or an accumulation function.",
   "method": "The derivative from the relation.",
   "rival": "Solving the differential equation first.",
   "separating_feature": "The relation already is the derivative.",
   "sources": [
    "BC-QA-05007"
   ],
   "evidence_tag": "verified"
  }
 ],
 "worked_examples": [
  {
   "id": "ex-1",
   "archetype_id": "BC-QA-05003",
   "bands": [
    "low",
    "mid"
   ],
   "parameter_draw": {
    "named": 1,
    "other": -2,
    "scale": 3,
    "sign": "positive",
    "multiplicity": 2,
    "factor": "none"
   },
   "problem": {
    "text": "f'(x) = 3(x - 1)^2(x + 2). Does f have a relative minimum, relative maximum, or neither at x = 1? Give a reason.",
    "command_verb": "determine"
   },
   "calculator_status": "no_calculator",
   "steps": [
    {
     "cue": "Named input: locate it on f'.",
     "why": "The test reads f' only.",
     "expr": "3*(x - 1)**2*(x + 2)",
     "relation": "new"
    },
    {
     "cue": "At x = 1.",
     "why": "A critical point.",
     "expr": "0",
     "relation": "evaluate",
     "subs": {
      "x": "1"
     }
    },
    {
     "cue": "Sign each side of 1.",
     "why": "(x - 1)^2 > 0 and x + 2 > 0 near 1: f' > 0 on both sides."
    },
    {
     "cue": "No change.",
     "why": "Neither, because f' does not change sign at x = 1.",
     "point_type_id": "BC-PT-99012"
    }
   ],
   "answer": {
    "form": "statement",
    "expr": "neither_at_1",
    "label": "Neither: f' does not change sign at x = 1."
   }
  }
 ],
 "what_a_reader_scores": [
  {
   "example_id": "ex-1",
   "point_type_ids": [
    "BC-PT-99012"
   ],
   "lines": [
    {
     "point_type_id": "BC-PT-99012",
     "text": "Classification of a critical point by a derivative test. Earned by: Correct classification of the critical point as a relative maximum, relative minimum, or neither, with analysis using a first or second derivative test; the test need not be named (sg-26:8). Not earned by: A candidates test, which sg-26:8 states is not sufficient justification here; an assertion with no supporting sign or second-derivative analysis."
    }
   ]
  }
 ],
 "common_errors": [
  {
   "error_id": "BC-ERR-05013",
   "wrong_step": {
    "text": "Extremum at 1, since f'(1) = 0.",
    "expr": "extremum_at_1"
   },
   "right_step": {
    "text": "Neither: no sign change.",
    "expr": "neither_at_1"
   },
   "relation": "distinct",
   "possible_reason": {
    "misconception_id": "BC-MIS-05008",
    "text": "reads the derivative being zero as the definition of a turning point, so no sign change is checked"
   },
   "sources": [
    "BC-ERR-05013",
    "BC-MIS-05008"
   ],
   "observed_behavior": "The response reports a relative maximum or minimum at an input where the derivative is zero but keeps its sign on both sides.",
   "scoring_consequence": "The single answer with reason point is lost.",
   "fix_prompt": true
  },
  {
   "error_id": "BC-ERR-05018",
   "wrong_step": {
    "text": "It does not change sign.",
    "expr": "it_does_not_change_sign"
   },
   "right_step": {
    "text": "f' does not change sign.",
    "expr": "f_prime_does_not_change_sign"
   },
   "relation": "distinct",
   "possible_reason": null,
   "sources": [
    "BC-ERR-05018"
   ],
   "observed_behavior": "The reason says that the function or the graph changes sign, without naming which object is meant.",
   "scoring_consequence": "The reason point is lost; the 2025 guideline names an ambiguous referent as disqualifying.",
   "fix_prompt": true
  },
  {
   "error_id": "BC-ERR-05020",
   "wrong_step": {
    "text": "Tests x = 0 and 2.",
    "expr": "FiniteSet(0, 2)"
   },
   "right_step": {
    "text": "Critical points -2 and 1.",
    "expr": "FiniteSet(-2, 1)"
   },
   "relation": "distinct",
   "possible_reason": null,
   "sources": [
    "BC-ERR-05020"
   ],
   "observed_behavior": "The response tests inputs that are neither critical points nor endpoints when hunting for a relative extremum.",
   "scoring_consequence": "Time is spent on inputs that cannot be extrema, and in a candidates argument extra inputs cost the justification point.",
   "fix_prompt": true
  },
  {
   "error_id": "BC-ERR-05021",
   "wrong_step": {
    "text": "Maximum at -2.",
    "expr": "relative_maximum_at_minus_2"
   },
   "right_step": {
    "text": "f' negative to positive: minimum.",
    "expr": "relative_minimum_at_minus_2"
   },
   "relation": "distinct",
   "possible_reason": {
    "misconception_id": "BC-MIS-05014",
    "text": "reads the size or the sign of the derivative at one nearby input as the classification"
   },
   "sources": [
    "BC-ERR-05021",
    "BC-MIS-05014"
   ],
   "observed_behavior": "The response reports a relative maximum where the derivative changes from negative to positive, or the reverse.",
   "scoring_consequence": "The answer with reason point is lost.",
   "fix_prompt": true
  }
 ],
 "representations": null,
 "prerequisite_bridges": [],
 "time": {
  "exam_part": "I-A",
  "budget_minutes": 2.14,
  "source": "research/exam/exam-structure.md#Section and part layout",
  "written_steps": {
   "ex-1": [
    4
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
   "archetype_id": "BC-QA-05003",
   "parameter_draw": {
    "named": 1,
    "other": -2,
    "scale": 3,
    "sign": "positive",
    "multiplicity": 2,
    "factor": "none"
   },
   "completes": "ex-1",
   "stem": {
    "text": "f'(1) = 0 and f' > 0 on both sides of 1. Classify x = 1, with a reason.",
    "command_verb": "determine"
   },
   "key": {
    "form": "statement",
    "expr": "neither_at_1",
    "label": "Neither: f' does not change sign at x = 1."
   },
   "steps": [],
   "calculator_status": "no_calculator",
   "skills": [
    "BC-SKL-05021",
    "BC-SKL-05022"
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
   "archetype_id": "BC-QA-05003",
   "parameter_draw": {
    "named": -1,
    "other": 3,
    "scale": 2,
    "sign": "positive",
    "multiplicity": 1,
    "factor": "none"
   },
   "stem": {
    "text": "f'(x) = 2(x + 1)(x - 3). Classify x = -1, with a reason.",
    "command_verb": "determine"
   },
   "key": {
    "form": "statement",
    "expr": "relative_maximum_at_minus_1",
    "label": "Relative maximum: f' changes from positive to negative at x = -1."
   },
   "steps": [],
   "calculator_status": "no_calculator",
   "skills": [
    "BC-SKL-05020",
    "BC-SKL-05022"
   ]
  },
  {
   "id": "chk-3",
   "check_kind": "mcq",
   "format": "mcq",
   "bands": [
    "low"
   ],
   "archetype_id": "BC-QA-05003",
   "parameter_draw": {
    "named": 0,
    "other": -3,
    "scale": 1,
    "sign": "positive",
    "multiplicity": 2,
    "factor": "none"
   },
   "stem": {
    "text": "f'(x) = x^2(x + 3). Which response gives the relative extrema of f with a reason?",
    "command_verb": "identify"
   },
   "key": {
    "form": "statement",
    "expr": "relative_minimum_at_minus_3_only",
    "label": "Minimum at -3 only: f' goes negative to positive there, no change at 0."
   },
   "steps": [],
   "options": [
    {
     "id": "A",
     "is_key": false,
     "label": "Minima at -3 and 0, since f'(0) = 0.",
     "error_path": "BC-ERR-05013",
     "derivation": "x = 0 declared an extremum with no sign change"
    },
    {
     "id": "B",
     "is_key": false,
     "label": "Maximum at -3 only.",
     "error_path": "BC-ERR-05021",
     "derivation": "negative to positive read as a maximum"
    },
    {
     "id": "C",
     "is_key": true,
     "label": "Minimum at -3 only: f' goes negative to positive there, no change at 0.",
     "error_path": null
    },
    {
     "id": "D",
     "is_key": false,
     "label": "Minimum at -3 only: it goes negative to positive there.",
     "error_path": "BC-ERR-05018",
     "derivation": "the referent it names no object"
    }
   ],
   "calculator_status": "no_calculator",
   "skills": [
    "BC-SKL-05020",
    "BC-SKL-05021"
   ]
  }
 ],
 "delivery": [
  {
   "block": "orientation",
   "mode": "text",
   "reason": "rule 5: a statement of what a response shows; the figure-bearing BC-REP-02 is served once, on ki-1",
   "sources": [
    "BC-SKL-05022"
   ]
  },
  {
   "block": "ki-1",
   "mode": "interactive",
   "reason": "rule 3 promoted: BC-REP-02 on BC-SKL-05019 to 05021; BC-QA-05003 common_givens a named input and difficulty_variables whether the answer is neither",
   "sources": [
    "BC-SKL-05020",
    "BC-SKL-05021",
    "BC-QA-05003"
   ],
   "spec": {
    "kind": "graph",
    "representations": [
     "BC-REP-02"
    ],
    "curve": "f'(x) = 3(x - 1)^2(x + 2)",
    "window": {
     "x": [
      -3,
      2
     ],
     "y": [
      -50,
      15
     ]
    },
    "controls": [
     {
      "type": "slider",
      "name": "x",
      "domain": [
       -3,
       2
      ],
      "step": 0.1,
      "readout": "sign of f'(x)"
     }
    ],
    "question": "Does the sign of f' change as x passes -2? As x passes 1?",
    "labels": [
     {
      "text": "graph of f'",
      "placement": "inside"
     },
     {
      "text": "x = -2: minus to plus",
      "placement": "inside"
     },
     {
      "text": "x = 1: plus to plus",
      "placement": "inside"
     }
    ]
   },
   "fallback": "three static frames at x = -2.5, 0 and 1.5 with the sign of f' beside each, and the two labels",
   "keyboard": "Tab focuses the slider; Left and Right arrow keys move x by 0.1; Home and End jump to the window edges"
  },
  {
   "block": "ex-1",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  },
  {
   "block": "err-BC-ERR-05013",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  },
  {
   "block": "err-BC-ERR-05018",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  },
  {
   "block": "err-BC-ERR-05020",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  },
  {
   "block": "err-BC-ERR-05021",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  }
 ],
 "refresher": [
  "ki-1",
  "err-BC-ERR-05013",
  "err-BC-ERR-05018",
  "err-BC-ERR-05020",
  "err-BC-ERR-05021",
  "ex-1"
 ],
 "research_lines": [
  {
   "file": "research/scoring/justification-requirements.md",
   "line": "A part saying to give a reason carries a reason point that can be satisfied by one correctly targeted sentence"
  }
 ],
 "inferred": [
  {
   "claim": "BC-QA-05003 has calculator_status either, so the lesson places it in Section I Part A.",
   "settles": "A calculator_status of calculator or no_calculator on BC-QA-05003."
  },
  {
   "claim": "ki-1 is served as an interactive slider rather than a static figure.",
   "settles": "The modality A/B in the build plan: skip rate and time to first credited success by mode."
  }
 ],
 "sources": [
  "BC-CON-05005",
  "BC-EK-FUN-4A2",
  "ced:102",
  "BC-QA-05003",
  "BC-QA-05007",
  "BC-PT-99012",
  "BC-PT-99013",
  "sg-23:13",
  "sg-25:5",
  "sg-25:17",
  "BC-ERR-05013",
  "BC-ERR-05018",
  "BC-ERR-05020",
  "BC-ERR-05021",
  "BC-MIS-05008",
  "BC-MIS-05014",
  "research/units/unit-05-analytical-applications-differentiation.md#5.4 Using the First Derivative Test to Determine Relative (Local) Extrema",
  "research/question-analysis/question-archetypes.md#BC-QA-05003 Relative extremum classified from the behaviour of the first derivative",
  "research/question-analysis/question-archetypes.md#BC-QA-05007 Critical point located and classified for a function given indirectly",
  "research/scoring/justification-requirements.md#Justify, give a reason, and give reasons",
  "research/scoring/justification-requirements.md#Reasons tied to the object the prompt names",
  "research/scoring/common-point-losses.md#Notation points",
  "research/exam/exam-structure.md#Section and part layout"
 ],
 "word_count": {
  "full": 629,
  "brief": 450
 },
 "read_minutes": {
  "full": 4.2,
  "brief": 3.0
 }
}
```
