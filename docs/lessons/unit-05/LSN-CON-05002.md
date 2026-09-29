---
title: LSN-CON-05002 Extreme Value Theorem as an existence result
research_date: 2026-09-29
status: designed
purpose: Authoring spec for the concept lesson on BC-CON-05002, the Extreme Value Theorem as an existence result, built from authoring_bundle("BC-CON-05002") and the research files it cites, so an author fills plan 15's lesson record without making a teaching decision.
---

# LSN-CON-05002 Extreme Value Theorem as an existence result

Concept BC-CON-05002 (skills BC-SKL-05007, BC-SKL-05008, BC-SKL-05009), topic 5.2 of Unit 5, loaded by one archetype, BC-QA-05010 (family evt-existence, tagged [inferred] in the research). It has no unit parent (docs/lessons/unit-05/README.md, section 1). The written reason is the single hypothesis, continuity on a closed interval, checked before the conclusion.

## Orientation

Served text, from BC-CON-05002 `description_plain` and the topic's Assessment behaviour paragraph (research/units/unit-05-analytical-applications-differentiation.md#5.2 Extreme Value Theorem, Global Versus Local Extrema, and Critical Points): a response checks that the interval is closed and that f is continuous on it, then answers that a maximum and a minimum value are attained. No count, no frequency.

## Key ideas

All three skills map to BC-EK-FUN-1C1 (ced:100), so one core block, both bands.

- ki-1 (core). Paraphrase of the Required mathematical knowledge paragraph (Extreme Value Theorem): one hypothesis, continuity on the closed interval; the conclusion is existence of a minimum and a maximum value, not their location. Anchor quote (14 words) from ced:100. The research notes the EK wording was clarified for Fall 2026 (ced-clarifications-2026:1); the quote is from the cached ced:100 page. Notation line from the concept record.

## Recognition

- BC-QA-05010 (research/question-analysis/question-archetypes.md#BC-QA-05010 Extreme Value Theorem existence claim on a closed interval): `typical_wording` "must the function attain a maximum value on the closed interval, and justify the answer"; `common_givens` a continuity or differentiability statement, or a graph with a break, a closed interval; `asked_to_produce` a yes or no answer, the continuity statement, the named theorem. The signal: "must ... attain a maximum (or minimum) value" with an interval in brackets. Shape: a single MCQ, or a short FRQ part; no `official_examples` (library gap).

What says "not this concept": a stem asking where the maximum occurs, or for its value (the candidates test, BC-CON-05006); a stem asking for c with a named derivative value (the Mean Value Theorem, BC-CON-05001).

## Method choice

One strategy block, both bands.

- st-1, BC-QA-05010. Method, `expected_solution_path[0]`: check the interval is closed. Rival, `wrong_approaches`: differentiating to find the extremum when only existence was asked. Separating feature: "must ... attain" asks existence, so no derivative is taken. The archetype carries `asked_to_produce` and `common_givens`, so the block is not tagged inferred.

## Solution path

- ex-1, BC-QA-05010, both bands, no calculator. Draw: left_end -1, length 5, jump_offset 3, critical_offset 2, letter f, extreme maximum, situation differentiable, so the interval is [-1, 4] and the relative maximum the spec's notes plant sits at x = 1. Steps follow `expected_solution_path`: closed interval, continuity from differentiability, the conclusion; the last step says why x = 1 is not the answer. No step has a value.
- ex-2, BC-QA-05010, low band. Draw: left_end 0, length 6, jump_offset 2, critical_offset 4, letter g, extreme minimum, situation jump: a jump at x = 2 inside [0, 6], so the verdict is no (the spec's invariant ties the verdict to the situation).

No published BC-QA-05010 item carries either draw. A fluent solver writes the three sentences; none is held in the head.

## Scoring

BC-QA-05010 lists no `point_types`, so no what_a_reader_scores entry and no point tag; the served text names no point beyond the error records' scoring_consequence. For the author: the research scores this archetype by analogy with the Mean Value Theorem part, a hypothesis point that a bare assertion does not earn and a conclusion point (sg-23:3, sg-25:12; research/scoring/justification-requirements.md#Theorem hypotheses). The analogy is the research's, tagged [inferred] on the family.

## Traps

Three active errors meet the skills, in the bundle's order; low band all three, mid band the first two.

- err-BC-ERR-05007 on ex-2: yes by the theorem across the jump, against the theorem not applying. Possible reason, words from BC-MIS-05006.
- err-BC-ERR-05008 on ex-1: x = 1 reported, against existence with the location left open. No possible reason line: neither linked description fits the location claim.
- err-BC-ERR-99008 on ex-1: continuity asserted against continuity derived. Possible reason, words from BC-MIS-99009.

## Representations

None as a separate block. The topic's Representations paragraph names graphs of f' for critical points, which belong to BC-CON-05003; the graph with a break inside the interval is served on ki-1.

## Prerequisite bridge

- BC-PRQ-05004, from its `description_plain` and `failure_signature`.

## Time

BC-QA-05010 is `no_calculator` and a single MCQ or short FRQ part, so Section I Part A, 2.14 minutes per question (research/exam/exam-structure.md#Section and part layout). The minutes go on reading the brackets and the continuity source; differentiating is the wrong approach and costs time with no credit (docs/lessons/unit-05/README.md, section 5).

## Checks

- chk-1, completion of ex-1, both bands: the interval and continuity lines are given, the student writes the conclusion. Key: the ex-1 statement.
- chk-2, isomorph, both bands. Draw: left_end 1, length 3, jump_offset 2, critical_offset 1, letter h, extreme minimum, situation continuous. Key: yes, a minimum value on [1, 4].
- chk-3, MCQ, low band. Draw: left_end -2, length 5, jump_offset 4, critical_offset 2, letter g, extreme minimum, situation open. Key: no conclusion, the interval is open. Distractors: yes by the theorem (BC-ERR-05007), yes at x = 0 (BC-ERR-05008), yes because g is continuous (BC-ERR-99008).

Every key is a verdict, so each is a statement key with option labels.

## Delivery

- orientation: text. Rule 5.
- ki-1: figure. Rule 3 on BC-REP-02 in BC-SKL-05008; not promoted, because BC-QA-05010 `difficulty_variables` are yes or no features, not a varying quantity (docs/lessons/unit-05/README.md, section 6) [inferred; settled by the modality A/B].
- ex-1, ex-2 and the three error blocks: step_reveal. Rule 1.

## Band plan

- Low (full): orientation, ki-1, st-1, ex-1, the three error blocks, chk-1 to chk-3, ex-2, the bridge. 523 words, 3.5 minutes (cap 900 and 6).
- Mid (brief): orientation, ki-1, st-1, ex-1, err-BC-ERR-05007, err-BC-ERR-05008, chk-1, chk-2, the bridge. 352 words, 2.4 minutes (cap 450 and 3).
- Refresher: ki-1, err-BC-ERR-05007, err-BC-ERR-05008, err-BC-ERR-99008, ex-1.

## Sources

- BC-CON-05002; BC-SKL-05007, BC-SKL-05008, BC-SKL-05009; BC-EK-FUN-1C1; ced:100; ced-clarifications-2026:1
- BC-QA-05010; sg-23:3, sg-25:12
- BC-ERR-05007, BC-ERR-05008, BC-ERR-99008; BC-MIS-05006, BC-MIS-99009
- BC-PRQ-05004
- research/units/unit-05-analytical-applications-differentiation.md#5.2 Extreme Value Theorem, Global Versus Local Extrema, and Critical Points
- research/question-analysis/question-archetypes.md#BC-QA-05010 Extreme Value Theorem existence claim on a closed interval
- research/scoring/justification-requirements.md#Theorem hypotheses
- research/scoring/common-point-losses.md#Justification points
- research/exam/exam-structure.md#Section and part layout
- [inferred] The scoring shape of BC-QA-05010 by analogy with the Mean Value Theorem part. Settled by a released FRQ scoring an EVT existence part, and point_types on BC-QA-05010.
- [inferred] ki-1 as a static figure. Settled by the modality A/B.

## Machine record

```json
{
 "id": "LSN-CON-05002",
 "kind": "concept",
 "target_id": "BC-CON-05002",
 "unit": "05",
 "skills": [
  "BC-SKL-05007",
  "BC-SKL-05008",
  "BC-SKL-05009"
 ],
 "orientation": {
  "text": "A response checks that the interval is closed and that f is continuous on it, saying where continuity comes from, then answers that a maximum and a minimum value are attained.",
  "sources": [
   "BC-CON-05002",
   "research/units/unit-05-analytical-applications-differentiation.md#5.2 Extreme Value Theorem, Global Versus Local Extrema, and Critical Points"
  ]
 },
 "key_ideas": [
  {
   "id": "ki-1",
   "ek_id": "BC-EK-FUN-1C1",
   "depth": "core",
   "text": "The Extreme Value Theorem has one hypothesis: f continuous on a closed interval [a, b]. A break inside, or an open interval, and the theorem gives nothing. Its conclusion is existence: it says a largest and a smallest value occur, not where.",
   "notation": "absolute maximum; absolute minimum",
   "quote": {
    "text": "f has at least one minimum value and at least one maximum value on [a, b]",
    "source": "ced:100"
   },
   "sources": [
    "BC-EK-FUN-1C1",
    "ced:100",
    "research/units/unit-05-analytical-applications-differentiation.md#5.2 Extreme Value Theorem, Global Versus Local Extrema, and Critical Points"
   ]
  }
 ],
 "strategy": [
  {
   "id": "st-1",
   "archetype_id": "BC-QA-05010",
   "cue": "Must f attain a maximum or minimum value, from a continuity statement and an interval?",
   "method": "First line: the interval is closed.",
   "rival": "Rival: differentiating to locate the extremum.",
   "separating_feature": "Must attain asks existence; nothing is located.",
   "sources": [
    "BC-QA-05010"
   ],
   "evidence_tag": "verified"
  }
 ],
 "worked_examples": [
  {
   "id": "ex-1",
   "archetype_id": "BC-QA-05010",
   "bands": [
    "low",
    "mid"
   ],
   "parameter_draw": {
    "left_end": -1,
    "length": 5,
    "jump_offset": 3,
    "critical_offset": 2,
    "letter": "f",
    "extreme": "maximum",
    "situation": "differentiable"
   },
   "problem": {
    "text": "f is differentiable on [-1, 4], with a relative maximum at x = 1. Must f attain a maximum value on [-1, 4]? Justify.",
    "command_verb": "justify"
   },
   "calculator_status": "no_calculator",
   "steps": [
    {
     "cue": "Brackets in [-1, 4].",
     "why": "The theorem needs a closed interval."
    },
    {
     "cue": "Stem says differentiable.",
     "why": "Differentiable on [-1, 4], so continuous there."
    },
    {
     "cue": "Both checks written.",
     "why": "Yes: by the Extreme Value Theorem f attains a maximum value on [-1, 4]."
    },
    {
     "cue": "The relative maximum at x = 1.",
     "why": "Not asked; the theorem does not place the maximum."
    }
   ],
   "answer": {
    "form": "statement",
    "expr": "maximum_value_attained_on_closed_interval",
    "label": "Yes, by the Extreme Value Theorem."
   }
  },
  {
   "id": "ex-2",
   "archetype_id": "BC-QA-05010",
   "bands": [
    "low"
   ],
   "parameter_draw": {
    "left_end": 0,
    "length": 6,
    "jump_offset": 2,
    "critical_offset": 4,
    "letter": "g",
    "extreme": "minimum",
    "situation": "jump"
   },
   "problem": {
    "text": "g has a jump at x = 2 and a relative minimum at x = 4. Must g attain a minimum value on [0, 6]?",
    "command_verb": "justify"
   },
   "calculator_status": "no_calculator",
   "steps": [
    {
     "cue": "Closed interval [0, 6].",
     "why": "First check passes."
    },
    {
     "cue": "Jump at x = 2, inside.",
     "why": "g is not continuous on [0, 6]."
    },
    {
     "cue": "A hypothesis fails.",
     "why": "The theorem does not apply, so no minimum is assured."
    }
   ],
   "answer": {
    "form": "statement",
    "expr": "theorem_does_not_apply",
    "label": "No: the Extreme Value Theorem does not apply."
   }
  }
 ],
 "what_a_reader_scores": [],
 "common_errors": [
  {
   "error_id": "BC-ERR-05007",
   "wrong_step": {
    "text": "Yes, by the theorem.",
    "expr": "yes_by_extreme_value_theorem"
   },
   "right_step": {
    "text": "Jump at 2: no conclusion.",
    "expr": "theorem_does_not_apply"
   },
   "relation": "distinct",
   "possible_reason": {
    "misconception_id": "BC-MIS-05006",
    "text": "applies the Extreme Value Theorem to open intervals or across discontinuities"
   },
   "sources": [
    "BC-ERR-05007",
    "BC-MIS-05006"
   ],
   "observed_behavior": "The response claims that a maximum and a minimum are attained for a function with a break inside the interval, or on an open interval.",
   "scoring_consequence": "The hypothesis point is lost and the conclusion is unsupported."
  },
  {
   "error_id": "BC-ERR-05008",
   "wrong_step": {
    "text": "Maximum at x = 1.",
    "expr": "Eq(x, 1)"
   },
   "right_step": {
    "text": "A maximum value exists.",
    "expr": "maximum_value_attained_on_closed_interval"
   },
   "relation": "distinct",
   "possible_reason": null,
   "sources": [
    "BC-ERR-05008"
   ],
   "observed_behavior": "The response treats the Extreme Value Theorem as though it named the input at which the extremum occurs.",
   "scoring_consequence": "The response answers a different question and the location it reports is unsupported."
  },
  {
   "error_id": "BC-ERR-99008",
   "wrong_step": {
    "text": "f is continuous.",
    "expr": "continuous_asserted"
   },
   "right_step": {
    "text": "Continuous because differentiable.",
    "expr": "continuous_because_differentiable"
   },
   "relation": "distinct",
   "possible_reason": {
    "misconception_id": "BC-MIS-99009",
    "text": "continuity is asserted rather than derived from differentiability"
   },
   "sources": [
    "BC-ERR-99008",
    "BC-MIS-99009"
   ],
   "observed_behavior": "Responses apply the Mean Value Theorem, the Intermediate Value Theorem or L'Hospital's Rule without establishing continuity from differentiability, without bounding the target value between two function values, or without confirming the indeterminate form.",
   "scoring_consequence": "The condition point is not earned; in several years this was the point earned by the smallest proportion of responses on the question."
  }
 ],
 "representations": null,
 "prerequisite_bridges": [
  {
   "prq_id": "BC-PRQ-05004",
   "text": "[a, b] includes its endpoints; (a, b) does not. Read the brackets first."
  }
 ],
 "time": {
  "exam_part": "I-A",
  "budget_minutes": 2.14,
  "source": "research/exam/exam-structure.md#Section and part layout",
  "written_steps": {
   "ex-1": [
    1,
    2,
    3
   ],
   "ex-2": [
    1,
    2,
    3
   ]
  },
  "skipped_steps": {
   "ex-1": [
    4
   ],
   "ex-2": []
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
   "archetype_id": "BC-QA-05010",
   "parameter_draw": {
    "left_end": -1,
    "length": 5,
    "jump_offset": 3,
    "critical_offset": 2,
    "letter": "f",
    "extreme": "maximum",
    "situation": "differentiable"
   },
   "completes": "ex-1",
   "stem": {
    "text": "[-1, 4] is closed; f is continuous there because differentiable. Finish: must f attain a maximum value?",
    "command_verb": "justify"
   },
   "key": {
    "form": "statement",
    "expr": "maximum_value_attained_on_closed_interval",
    "label": "Yes, by the Extreme Value Theorem."
   },
   "steps": [],
   "calculator_status": "no_calculator",
   "skills": [
    "BC-SKL-05009"
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
   "archetype_id": "BC-QA-05010",
   "parameter_draw": {
    "left_end": 1,
    "length": 3,
    "jump_offset": 2,
    "critical_offset": 1,
    "letter": "h",
    "extreme": "minimum",
    "situation": "continuous"
   },
   "stem": {
    "text": "h is continuous on [1, 4] with a relative minimum at x = 2. Must h attain a minimum value on [1, 4]?",
    "command_verb": "justify"
   },
   "key": {
    "form": "statement",
    "expr": "minimum_value_attained_on_closed_interval",
    "label": "Yes: continuous on the closed interval, Extreme Value Theorem."
   },
   "steps": [],
   "calculator_status": "no_calculator",
   "skills": [
    "BC-SKL-05008",
    "BC-SKL-05009"
   ]
  },
  {
   "id": "chk-3",
   "check_kind": "mcq",
   "format": "mcq",
   "bands": [
    "low"
   ],
   "archetype_id": "BC-QA-05010",
   "parameter_draw": {
    "left_end": -2,
    "length": 5,
    "jump_offset": 4,
    "critical_offset": 2,
    "letter": "g",
    "extreme": "minimum",
    "situation": "open"
   },
   "stem": {
    "text": "g is differentiable on (-2, 3), relative minimum at x = 0. Must g attain a minimum value on (-2, 3)?",
    "command_verb": "identify"
   },
   "key": {
    "form": "statement",
    "expr": "theorem_does_not_apply",
    "label": "No conclusion: the interval is open."
   },
   "steps": [],
   "options": [
    {
     "id": "A",
     "is_key": false,
     "label": "Yes, by the Extreme Value Theorem.",
     "error_path": "BC-ERR-05007",
     "derivation": "the theorem applied on an open interval"
    },
    {
     "id": "B",
     "is_key": false,
     "label": "Yes, at x = 0.",
     "error_path": "BC-ERR-05008",
     "derivation": "the theorem used to place the extremum at the relative minimum"
    },
    {
     "id": "C",
     "is_key": true,
     "label": "No conclusion: the interval is open.",
     "error_path": null
    },
    {
     "id": "D",
     "is_key": false,
     "label": "Yes, because g is continuous.",
     "error_path": "BC-ERR-99008",
     "derivation": "continuity asserted and the closed interval never checked"
    }
   ],
   "calculator_status": "no_calculator",
   "skills": [
    "BC-SKL-05007",
    "BC-SKL-05008"
   ]
  }
 ],
 "delivery": [
  {
   "block": "orientation",
   "mode": "text",
   "reason": "rule 5: a statement of what a response shows; the figure-bearing BC-REP-02 is served once, on ki-1",
   "sources": [
    "BC-SKL-05007"
   ]
  },
  {
   "block": "ki-1",
   "mode": "figure",
   "reason": "rule 3: BC-REP-02 on BC-SKL-05008; not promoted, BC-QA-05010 difficulty_variables are yes or no features",
   "sources": [
    "BC-SKL-05008",
    "BC-QA-05010"
   ],
   "spec": {
    "kind": "graph",
    "representations": [
     "BC-REP-02"
    ],
    "window": {
     "x": [
      -1,
      7
     ],
     "y": [
      -1,
      6
     ]
    },
    "panels": [
     {
      "curve": "continuous curve on [0, 6]",
      "marks": [
       "filled endpoints at x = 0 and x = 6",
       "highest and lowest points marked"
      ]
     },
     {
      "curve": "same curve with a jump at x = 2",
      "marks": [
       "open and filled dots at x = 2"
      ]
     }
    ],
    "labels": [
     {
      "text": "continuous on [0, 6]: max and min attained",
      "placement": "inside"
     },
     {
      "text": "jump at x = 2: theorem gives nothing",
      "placement": "inside"
     }
    ]
   },
   "fallback": "the two panels as static images with the same inside labels, and a sentence naming the jump",
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
   "block": "err-BC-ERR-05007",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  },
  {
   "block": "err-BC-ERR-05008",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  },
  {
   "block": "err-BC-ERR-99008",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  }
 ],
 "refresher": [
  "ki-1",
  "err-BC-ERR-05007",
  "err-BC-ERR-05008",
  "err-BC-ERR-99008",
  "ex-1"
 ],
 "research_lines": [
  {
   "file": "research/scoring/justification-requirements.md",
   "line": "Existence questions are scored as a hypothesis point plus a conclusion point."
  }
 ],
 "inferred": [
  {
   "claim": "BC-QA-05010 is scored like the Mean Value Theorem existence part, a hypothesis point and a conclusion point.",
   "settles": "A released free-response scoring guideline with an Extreme Value Theorem part, and point_types filled on BC-QA-05010."
  },
  {
   "claim": "ki-1 is served as a static two-panel figure rather than text.",
   "settles": "The modality A/B in the build plan: skip rate and time to first credited success by mode."
  }
 ],
 "sources": [
  "BC-CON-05002",
  "BC-EK-FUN-1C1",
  "ced:100",
  "BC-QA-05010",
  "sg-23:3",
  "sg-25:12",
  "BC-ERR-05007",
  "BC-ERR-05008",
  "BC-ERR-99008",
  "BC-MIS-05006",
  "BC-MIS-99009",
  "BC-PRQ-05004",
  "research/units/unit-05-analytical-applications-differentiation.md#5.2 Extreme Value Theorem, Global Versus Local Extrema, and Critical Points",
  "research/question-analysis/question-archetypes.md#BC-QA-05010 Extreme Value Theorem existence claim on a closed interval",
  "research/scoring/justification-requirements.md#Theorem hypotheses",
  "research/scoring/common-point-losses.md#Justification points",
  "research/exam/exam-structure.md#Section and part layout"
 ],
 "word_count": {
  "full": 523,
  "brief": 352
 },
 "read_minutes": {
  "full": 3.5,
  "brief": 2.4
 }
}
```
