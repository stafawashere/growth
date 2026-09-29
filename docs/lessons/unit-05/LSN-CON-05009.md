---
title: LSN-CON-05009 Second derivative test at a critical point
research_date: 2026-09-29
status: designed
purpose: Authoring spec for the concept lesson on BC-CON-05009, the second derivative test at a critical point with its inconclusive case and the choice between derivative tests, built from authoring_bundle("BC-CON-05009") and the research files it cites, so an author fills plan 15's lesson record without making a teaching decision.
---

# LSN-CON-05009 Second derivative test at a critical point

Concept BC-CON-05009 (skills BC-SKL-05036, BC-SKL-05037, BC-SKL-05039), topic 5.7 of Unit 5. Two archetypes load its skills, both in the extremum-classification family: BC-QA-05013 (primary, through all three skills) and BC-QA-05007 (through BC-SKL-05039). Unit parents BC-CON-05003, 05005 and 05007 (docs/lessons/unit-05/README.md, section 1).

## Prediction

Both bands, first. Poses ex-1's own numbers: f(x) = 2x^3 - 3x^2 - 12x + 2 has f'(2) = 0 and f''(2) = 18, and the student predicts what f has at x = 2. Form `mcq`, three options, key A (a relative minimum). The resolution says a positive f'' at a horizontal tangent is concave up, a relative minimum. Sources: BC-CON-05009 and the topic 5.7 section.

## Orientation

Served text, from BC-CON-05009 `description_plain` and the topic's Assessment behaviour paragraph (research/units/unit-05-analytical-applications-differentiation.md#5.7 Using the Second Derivative Test to Determine Extrema): a response states that f prime is zero at the input and states the sign of f double prime there, then classifies. A zero second derivative settles nothing. No count, no frequency.

## Key ideas

All three skills map to BC-EK-FUN-4A7 (ced:105), so one core block, both bands.

- ki-1 (core). Paraphrase of the Required mathematical knowledge paragraph (Second derivative test, Local scope): hypotheses f'(c) = 0 and f'' existing near c; negative gives a relative maximum, positive a relative minimum, zero leaves the test inconclusive; the test is local, so it earns no global justification (sg-25:19). Anchor quote from ced:105, 22 words. Notation line from the concept record, f''(c).

## Recognition

BC-QA-05013 (research/question-analysis/question-archetypes.md#BC-QA-05013 Second derivative test applied at a critical point): `typical_wording` "determine whether the critical point is the location of a relative minimum, a relative maximum, or neither"; `common_givens` a function, a differential equation or an implicit relation, and a critical point; `asked_to_produce` the second derivative at the point and the classification. The signal: "relative" beside a named critical point, with a formula that can be differentiated twice. Shape: an MCQ, or one part of a free response question where the test is an alternate route to the classification point (sg-24:10); no `official_examples` in the record.

BC-QA-05007 carries BC-SKL-05039, the choice of test: a relation or accumulation function given, and "whether the classification is by sign change or by second derivative" among its `difficulty_variables`.

What says "not this concept" (the contrast pair's near miss is the first derivative test read from a graph of the derivative only, BC-ERR-05040 and BC-MIS-05024): the word "absolute" or "on the closed interval" (a global claim, sg-25:19; BC-CON-05006, 05010), or a derivative given only as a graph (first derivative test, BC-ERR-05040).

## Method choice

One strategy block, both bands, for the extremum-classification family.

- st-1, BC-QA-05013. Cue from `asked_to_produce` and `common_givens`. Method, `expected_solution_path[0]`: confirm the first derivative is zero at the point. Rival, `wrong_approaches`: classifying from the sign of the function value. Separating feature: the classification reads the sign of f double prime at a point where f prime is zero, never the value of f. The block also names the switch to the first derivative test when f double prime is zero. Not tagged inferred: both fields are present.

## Solution path

- ex-1, BC-QA-05013, both bands, no calculator. Draw from `parameter_spec`: first_root -1, second_root 2, other_input 4, tested_root second, leading_sign 1, constant 2, letter f, given function. So f'(x) = 6(x + 1)(x - 2) and f(x) = 2x^3 - 3x^2 - 12x + 2. The spec's constraints hold (2 times 4 is not 1). No published BC-QA-05013 item carries this draw.
- Steps follow `expected_solution_path`: f prime (new); f'(2) = 0 (evaluate); f double prime (new); f''(2) = 18 (evaluate); the classification with its reason (no value, the justified conclusion). A fluent solver writes all five; the two derivatives are one line each.

## Scoring

BC-QA-05013 lists no `point_types`, so no what_a_reader_scores entry and no point tag. For the author: the test earned the same point as a sign argument where a classification was asked (sg-24:10) and lost the justification point where a global claim was asked (sg-25:19), and a local argument such as a Second Derivative Test does not justify a global claim (research/scoring/justification-requirements.md#Global versus local arguments).

## Traps

Four active errors meet the skills, in the bundle's order: BC-ERR-05037, BC-ERR-05040, BC-ERR-05036, BC-ERR-05038. Low band all four; mid band the first two. All on ex-1's draw.

- err-BC-ERR-05037: relative maximum reported where f''(2) = 18. Statement-shaped. No possible reason line: neither linked description names the reversal.
- err-BC-ERR-05040: a second derivative test started from a graph of f prime with its slope never discussed. Statement-shaped. Possible reason, words from BC-MIS-05024.
- err-BC-ERR-05036: f''(4) = 42 used at x = 4, where f'(4) is 60, not 0. No possible reason line.
- err-BC-ERR-05038: "neither" read from a zero second derivative. Statement-shaped. Possible reason, words from BC-MIS-05023.

## Representations

None. The topic's Representations paragraph names BC-REP-01, 03 and 06 conversions, none figure-shaped.

## Prerequisite bridge

None.

## Time

BC-QA-05013 is `either` and an MCQ or one FRQ part, so Section I Part A, 2.14 minutes per question (research/exam/exam-structure.md#Section and part layout) [inferred: an either archetype placed in Part A]. The minutes go on the two derivatives and one evaluation; the conclusion is one sentence naming f'(2) = 0 and the sign of f''(2).

## Checks

- chk-1, completion of ex-1, both bands: f'(2) = 0 and f''(x) = 12x - 6 given; the student evaluates and classifies. Key: relative minimum at x = 2.
- chk-2, isomorph, both bands. Draw: first_root 1, second_root 4, other_input -2, tested_root second, leading_sign -1, constant 0, letter h, given derivative. h'(x) = -6(x - 1)(x - 4), h''(4) = -18. Key: relative maximum at x = 4.
- chk-3, MCQ, low band. Draw: first_root -3, second_root 1, other_input 2, tested_root first, leading_sign -1, constant 0, letter g, given derivative. g''(-3) = 24. Key: relative minimum at x = -3. Distractors: relative maximum at x = -3 (BC-ERR-05037), relative maximum at x = 2 from g''(2) = -36 (BC-ERR-05036), neither (BC-ERR-05038).

## Delivery

- orientation: text. Rule 5: BC-SKL-05036, 05037 carry BC-REP-01, 04, 06 only (docs/lessons/unit-05/README.md, section 6).
- ki-1: figure. Rule 4: BC-SKL-05039 carries BC-REP-02, so the graph of ex-1's f with the horizontal tangent at x = 2 marked and labelled replaces the earlier text choice [inferred; settled by the modality A/B].
- ex-1: step_reveal. Rule 1.
- the four error blocks: step_reveal. Rule 1.

## Band plan

- Low (full): served order of 2026-09-29: prediction, orientation, ki-1, st-1 with its contrast pair, ex-1, chk-1, the four error blocks, chk-2, chk-3. 556 words, 3.8 minutes (cap 900 and 6). There is one worked example, so nothing is faded, and no scoring lines.
- Mid (brief): prediction, orientation, ki-1, st-1 with its contrast pair, ex-1, chk-1, err-BC-ERR-05037 and err-BC-ERR-05040, chk-2. 419 words, 2.8 minutes (cap 450 and 3).
- Refresher: ki-1, the four error blocks, ex-1.

## Sources

- Prediction and contrast pair: BC-CON-05009, BC-ERR-05040, BC-MIS-05024 (as above).

- BC-CON-05009; BC-SKL-05036, BC-SKL-05037, BC-SKL-05039; BC-EK-FUN-4A7; ced:105
- BC-QA-05013, BC-QA-05007; sg-24:10, sg-25:19
- BC-ERR-05037, BC-ERR-05040, BC-ERR-05036, BC-ERR-05038; BC-MIS-05023, BC-MIS-05024, BC-MIS-05014
- research/units/unit-05-analytical-applications-differentiation.md#5.7 Using the Second Derivative Test to Determine Extrema
- research/question-analysis/question-archetypes.md#BC-QA-05013 Second derivative test applied at a critical point
- research/scoring/justification-requirements.md#Global versus local arguments
- research/exam/exam-structure.md#Section and part layout
- [inferred] BC-QA-05013 placed in Section I Part A although its calculator status is either. Settled by a calculator status on the archetype.
- [inferred] ki-1 as a figure. Settled by the modality A/B.
- [inferred] The chk-3 distractor for BC-ERR-05038 on a draw whose f double prime is nonzero at the critical point. Settled by a parameter_spec that admits a zero second derivative.

## Machine record

```json
{
 "id": "LSN-CON-05009",
 "kind": "concept",
 "target_id": "BC-CON-05009",
 "unit": "05",
 "skills": [
  "BC-SKL-05036",
  "BC-SKL-05037",
  "BC-SKL-05039"
 ],
 "prediction": {
  "id": "pr-1",
  "stem": {
   "text": "Predict. For \\(f(x)=2x^3-3x^2-12x+2\\), \\(f'(2)=0\\) and \\(f''(2)=18\\). What does \\(f\\) have at \\(x=2\\)?",
   "command_verb": "predict"
  },
  "format": "mcq",
  "options": [
   {
    "id": "A",
    "label": "A relative minimum",
    "is_key": true
   },
   {
    "id": "B",
    "label": "A relative maximum",
    "is_key": false
   },
   {
    "id": "C",
    "label": "Neither",
    "is_key": false
   }
  ],
  "resolution": "\\(f'(2)=0\\) and \\(f''(2)=18>0\\), so the curve is concave up at a horizontal tangent: a relative minimum at \\(x=2\\).",
  "sources": [
   "BC-CON-05009",
   "research/units/unit-05-analytical-applications-differentiation.md#5.7 Using the Second Derivative Test to Determine Extrema"
  ]
 },
 "orientation": {
  "text": "A response states \\(f'(c)=0\\), then the sign of \\(f''(c)\\), then classifies. A zero second derivative settles nothing, and the first derivative test takes over.",
  "sources": [
   "BC-CON-05009",
   "research/units/unit-05-analytical-applications-differentiation.md#5.7 Using the Second Derivative Test to Determine Extrema"
  ]
 },
 "key_ideas": [
  {
   "id": "ki-1",
   "ek_id": "BC-EK-FUN-4A7",
   "depth": "core",
   "text": "With \\(f'(c)=0\\): \\(f''(c)<0\\) gives a relative maximum, \\(f''(c)>0\\) a relative minimum, and \\(f''(c)=0\\) is inconclusive, so the sign of \\(f'\\) on each side decides. The test is local: it does not justify an absolute extremum.",
   "notation": "f''(c)",
   "quote": {
    "text": "The second derivative of a function may determine whether a critical point is the location of a relative (local) maximum or minimum.",
    "source": "ced:105"
   },
   "sources": [
    "BC-EK-FUN-4A7",
    "ced:105",
    "sg-25:19",
    "research/units/unit-05-analytical-applications-differentiation.md#5.7 Using the Second Derivative Test to Determine Extrema"
   ]
  }
 ],
 "strategy": [
  {
   "id": "st-1",
   "archetype_id": "BC-QA-05013",
   "cue": "Classify a critical point, with the word relative.",
   "method": "Confirm \\(f'(c)=0\\).",
   "rival": "The sign of \\(f(c)\\).",
   "separating_feature": "The verdict reads the sign of \\(f''(c)\\), not \\(f(c)\\). If \\(f''(c)=0\\), switch to the sign of \\(f'\\).",
   "sources": [
    "BC-QA-05013"
   ],
   "evidence_tag": "verified",
   "contrast": {
    "this": {
     "text": "\\(g(x)=x^3-12x\\). Classify the critical point \\(x=2\\), with a reason.",
     "archetype_id": "BC-QA-05013"
    },
    "not_this": {
     "text": "The graph of \\(g'\\) crosses zero at \\(x=2\\). Classify \\(x=2\\), with a reason.",
     "why_not": "Only a graph of \\(g'\\) is given, so the sign change of \\(g'\\) decides."
    },
    "feature": "A formula to differentiate twice, against a graph of the derivative only."
   }
  }
 ],
 "worked_examples": [
  {
   "id": "ex-1",
   "archetype_id": "BC-QA-05013",
   "bands": [
    "low",
    "mid"
   ],
   "parameter_draw": {
    "first_root": -1,
    "second_root": 2,
    "other_input": 4,
    "tested_root": "second",
    "leading_sign": 1,
    "constant": 2,
    "letter": "f",
    "given": "function"
   },
   "problem": {
    "text": "Let \\(f(x)=2x^3-3x^2-12x+2\\). Determine whether \\(x=2\\) is the location of a relative minimum, a relative maximum, or neither. Justify.",
    "command_verb": "determine"
   },
   "calculator_status": "no_calculator",
   "steps": [
    {
     "cue": "The test starts at a critical point, so differentiate first.",
     "why": "\\(f'(x)=6x^2-6x-12\\).",
     "expr": "6*x**2 - 6*x - 12",
     "relation": "new"
    },
    {
     "cue": "The hypothesis to write: \\(f'(2)=0\\).",
     "why": "Without it the second derivative says nothing about an extremum.",
     "expr": "0",
     "relation": "evaluate",
     "subs": {
      "x": "2"
     }
    },
    {
     "cue": "Hypothesis met, so differentiate again.",
     "why": "\\(f''(x)=12x-6\\).",
     "expr": "12*x - 6",
     "relation": "new"
    },
    {
     "cue": "Evaluate at the critical point only.",
     "why": "\\(f''(2)=18\\), positive.",
     "expr": "18",
     "relation": "evaluate",
     "subs": {
      "x": "2"
     }
    },
    {
     "cue": "The stem asks for a classification with a reason.",
     "why": "\\(f'(2)=0\\) and \\(f''(2)>0\\), so \\(f\\) has a relative minimum at \\(x=2\\)."
    }
   ],
   "answer": {
    "form": "statement",
    "expr": "relative_minimum_at_2"
   }
  }
 ],
 "what_a_reader_scores": [],
 "common_errors": [
  {
   "error_id": "BC-ERR-05037",
   "observed_behavior": "The response reports a relative minimum where the second derivative is negative, or the reverse.",
   "scoring_consequence": "The classification is wrong and the point is lost.",
   "wrong_step": {
    "text": "\\(f''(2)=18\\), so a relative maximum.",
    "expr": "relative_maximum_at_2"
   },
   "right_step": {
    "text": "\\(f''(2)=18>0\\), so a relative minimum: the graph is concave up there.",
    "expr": "relative_minimum_at_2"
   },
   "relation": "distinct",
   "possible_reason": null,
   "sources": [
    "BC-ERR-05037"
   ],
   "fix_prompt": true
  },
  {
   "error_id": "BC-ERR-05040",
   "observed_behavior": "The response reaches for a second derivative test when only a graph of the first derivative is given and its slope is never discussed.",
   "scoring_consequence": "The argument cannot be completed from the given information, so the justification point is lost.",
   "wrong_step": {
    "text": "Given only a graph of \\(f'\\): \"\\(f''(2)>0\\)\", with the slope of that graph never mentioned.",
    "expr": "second_derivative_claimed_without_slope_of_graph"
   },
   "right_step": {
    "text": "\\(f'\\) changes from negative to positive at \\(x=2\\), read from the graph of \\(f'\\).",
    "expr": "sign_change_of_f_prime_at_2"
   },
   "relation": "distinct",
   "possible_reason": {
    "misconception_id": "BC-MIS-05024",
    "text": "picks a test by habit rather than by what the given representation supports"
   },
   "sources": [
    "BC-ERR-05040",
    "BC-MIS-05024"
   ],
   "fix_prompt": true
  },
  {
   "error_id": "BC-ERR-05036",
   "observed_behavior": "The response evaluates the second derivative at an input that is not a critical point and classifies it.",
   "scoring_consequence": "The conclusion does not follow and the justification point is lost.",
   "wrong_step": {
    "text": "\\(f''(4)=42>0\\), so a minimum at \\(x=4\\), where \\(f'(4)=60\\).",
    "expr": "12*4 - 6"
   },
   "right_step": {
    "text": "\\(f''(2)=18\\), at the critical point \\(x=2\\).",
    "expr": "12*2 - 6"
   },
   "relation": "distinct",
   "possible_reason": null,
   "sources": [
    "BC-ERR-05036"
   ],
   "fix_prompt": true
  },
  {
   "error_id": "BC-ERR-05038",
   "observed_behavior": "The response reports neither a maximum nor a minimum because the second derivative is zero at the critical point.",
   "scoring_consequence": "The classification is unsupported, since the test settles nothing in that case.",
   "wrong_step": {
    "text": "\\(f''(c)=0\\), so neither.",
    "expr": "neither_from_zero_second_derivative"
   },
   "right_step": {
    "text": "\\(f''(c)=0\\): inconclusive, so read the sign of \\(f'\\) on each side of \\(c\\).",
    "expr": "inconclusive_then_first_derivative_test"
   },
   "relation": "distinct",
   "possible_reason": {
    "misconception_id": "BC-MIS-05023",
    "text": "reads a zero second derivative as a verdict"
   },
   "sources": [
    "BC-ERR-05038",
    "BC-MIS-05023"
   ],
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
    1,
    2,
    3,
    4,
    5
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
   "archetype_id": "BC-QA-05013",
   "parameter_draw": {
    "first_root": -1,
    "second_root": 2,
    "other_input": 4,
    "tested_root": "second",
    "leading_sign": 1,
    "constant": 2,
    "letter": "f",
    "given": "function"
   },
   "completes": "ex-1",
   "stem": {
    "text": "For \\(f(x)=2x^3-3x^2-12x+2\\), \\(f'(2)=0\\) and \\(f''(x)=12x-6\\). Classify \\(x=2\\) and give the reason.",
    "command_verb": "determine"
   },
   "key": {
    "form": "statement",
    "expr": "relative_minimum_at_2"
   },
   "steps": [
    {
     "text": "The second derivative.",
     "expr": "12*x - 6",
     "relation": "new"
    },
    {
     "text": "At the critical point, 18.",
     "expr": "18",
     "relation": "evaluate",
     "subs": {
      "x": "2"
     }
    }
   ],
   "calculator_status": "no_calculator",
   "skills": [
    "BC-SKL-05036"
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
   "archetype_id": "BC-QA-05013",
   "parameter_draw": {
    "first_root": 1,
    "second_root": 4,
    "other_input": -2,
    "tested_root": "second",
    "leading_sign": -1,
    "constant": 0,
    "letter": "h",
    "given": "derivative"
   },
   "stem": {
    "text": "\\(h'(x)=-6(x-1)(x-4)\\). Classify the critical point \\(x=4\\) with the second derivative test.",
    "command_verb": "determine"
   },
   "key": {
    "form": "statement",
    "expr": "relative_maximum_at_4"
   },
   "steps": [
    {
     "text": "\\(h'(x)\\) expanded.",
     "expr": "-6*x**2 + 30*x - 24",
     "relation": "new"
    },
    {
     "text": "\\(h'(4)=0\\).",
     "expr": "0",
     "relation": "evaluate",
     "subs": {
      "x": "4"
     }
    },
    {
     "text": "\\(h''(x)=-12x+30\\).",
     "expr": "-12*x + 30",
     "relation": "new"
    },
    {
     "text": "\\(h''(4)=-18<0\\): relative maximum.",
     "expr": "-18",
     "relation": "evaluate",
     "subs": {
      "x": "4"
     }
    }
   ],
   "calculator_status": "no_calculator",
   "skills": [
    "BC-SKL-05036"
   ]
  },
  {
   "id": "chk-3",
   "check_kind": "mcq",
   "format": "mcq",
   "bands": [
    "low"
   ],
   "archetype_id": "BC-QA-05013",
   "parameter_draw": {
    "first_root": -3,
    "second_root": 1,
    "other_input": 2,
    "tested_root": "first",
    "leading_sign": -1,
    "constant": 0,
    "letter": "g",
    "given": "derivative"
   },
   "stem": {
    "text": "\\(g'(x)=-6(x+3)(x-1)\\), so \\(g''(x)=-12x-12\\). Which statement about \\(g\\) is justified?",
    "command_verb": "identify"
   },
   "key": {
    "form": "statement",
    "expr": "relative_minimum_at_minus_3"
   },
   "steps": [
    {
     "text": "\\(g'(x)=-6(x+3)(x-1)\\).",
     "expr": "-6*(x + 3)*(x - 1)",
     "relation": "new"
    },
    {
     "text": "\\(g'(-3)=0\\): a critical point.",
     "expr": "0",
     "relation": "evaluate",
     "subs": {
      "x": "-3"
     }
    },
    {
     "text": "\\(g''(x)=-12x-12\\).",
     "expr": "-12*x - 12",
     "relation": "new"
    },
    {
     "text": "\\(g''(-3)=24>0\\): relative minimum.",
     "expr": "24",
     "relation": "evaluate",
     "subs": {
      "x": "-3"
     }
    }
   ],
   "options": [
    {
     "id": "A",
     "is_key": true,
     "label": "Relative minimum at \\(x=-3\\), since \\(g'(-3)=0\\) and \\(g''(-3)=24>0\\).",
     "error_path": null
    },
    {
     "id": "B",
     "is_key": false,
     "label": "Relative maximum at \\(x=-3\\), since \\(g''(-3)=24\\).",
     "error_path": "BC-ERR-05037",
     "derivation": "sign convention reversed"
    },
    {
     "id": "C",
     "is_key": false,
     "label": "Relative maximum at \\(x=2\\), since \\(g''(2)=-36<0\\).",
     "error_path": "BC-ERR-05036",
     "derivation": "the test applied at x = 2, where g'(2) = -30, not 0"
    },
    {
     "id": "D",
     "is_key": false,
     "label": "Neither at \\(x=-3\\): the second derivative test gives no extremum.",
     "error_path": "BC-ERR-05038",
     "derivation": "the inconclusive outcome reported as a verdict of neither"
    }
   ],
   "calculator_status": "no_calculator",
   "skills": [
    "BC-SKL-05036"
   ]
  }
 ],
 "delivery": [
  {
   "block": "orientation",
   "mode": "text",
   "reason": "rule 5: BC-SKL-05036 and 05037 carry BC-REP-01, 04, 06 only",
   "sources": [
    "BC-SKL-05036",
    "BC-SKL-05037"
   ]
  },
  {
   "block": "ki-1",
   "mode": "figure",
   "reason": "rule 4: BC-REP-02 on BC-SKL-05039; the critical point read on the graph of f",
   "sources": [
    "BC-SKL-05039"
   ],
   "spec": {
    "kind": "graph",
    "representations": [
     "BC-REP-02"
    ],
    "curve": "f(x) = 2*x**3 - 3*x**2 - 12*x + 2",
    "window": {
     "x": [
      -2,
      4
     ],
     "y": [
      -22,
      36
     ]
    },
    "marks": [
     "horizontal tangent at x = 2"
    ],
    "labels": [
     {
      "text": "graph of f",
      "placement": "inside"
     },
     {
      "text": "x = 2: f' = 0, f'' = 18, relative minimum",
      "placement": "inside"
     }
    ]
   },
   "fallback": "the same graph static with the horizontal tangent at x = 2 marked and labelled",
   "keyboard": "no control; the figure description is reached with Tab"
  },
  {
   "block": "ex-1",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  },
  {
   "block": "err-BC-ERR-05037",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  },
  {
   "block": "err-BC-ERR-05040",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  },
  {
   "block": "err-BC-ERR-05036",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  },
  {
   "block": "err-BC-ERR-05038",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  }
 ],
 "refresher": [
  "ki-1",
  "err-BC-ERR-05037",
  "err-BC-ERR-05040",
  "err-BC-ERR-05036",
  "err-BC-ERR-05038",
  "ex-1"
 ],
 "read_minutes": {
  "full": 3.8,
  "brief": 2.8
 },
 "word_count": {
  "full": 556,
  "brief": 419
 },
 "research_lines": [
  {
   "file": "research/scoring/justification-requirements.md",
   "line": "a response presenting a local argument, such as a First Derivative Test or a Second Derivative Test, or an incorrect global argument, does not earn the justification point"
  }
 ],
 "inferred": [
  {
   "claim": "BC-QA-05013 has calculator_status either; the lesson places it in Section I Part A at 2.14 minutes.",
   "settles": "A single calculator status on BC-QA-05013 or an official example fixing its part."
  },
  {
   "claim": "The chk-3 distractor for BC-ERR-05038 sits on a draw where the second derivative is nonzero at the critical point, since the parameter_spec invariants exclude a zero second derivative.",
   "settles": "A BC-QA-05013 parameter_spec admitting a critical point with a zero second derivative."
  },
  {
   "claim": "ki-1 is served as a figure rather than text.",
   "settles": "The modality A/B in the build plan: skip rate and time to first credited success by mode."
  }
 ],
 "sources": [
  "BC-CON-05009",
  "BC-SKL-05036",
  "BC-SKL-05037",
  "BC-SKL-05039",
  "BC-EK-FUN-4A7",
  "ced:105",
  "BC-QA-05013",
  "BC-QA-05007",
  "sg-24:10",
  "sg-25:19",
  "BC-ERR-05037",
  "BC-ERR-05040",
  "BC-ERR-05036",
  "BC-ERR-05038",
  "BC-MIS-05023",
  "BC-MIS-05024",
  "BC-MIS-05014",
  "research/units/unit-05-analytical-applications-differentiation.md#5.7 Using the Second Derivative Test to Determine Extrema",
  "research/question-analysis/question-archetypes.md#BC-QA-05013 Second derivative test applied at a critical point",
  "research/scoring/justification-requirements.md#Global versus local arguments",
  "research/exam/exam-structure.md#Section and part layout"
 ]
}
```
