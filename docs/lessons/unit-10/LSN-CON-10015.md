---
title: LSN-CON-10015 The alternating series error bound
research_date: 2026-09-29
status: designed
purpose: Authoring spec for the concept lesson on BC-CON-10015, the error of a partial sum of an alternating series being at most the first omitted term, stated with its conditions and compared with a tolerance, built from authoring_bundle and the research files it cites.
---

# LSN-CON-10015 The alternating series error bound

Concept BC-CON-10015 (skills BC-SKL-10039 to 10042), topic 10.10 of Unit 10, BC only (ced:195), loaded by one archetype, BC-QA-10008 (family taylor-error). Hard parents in the unit are BC-CON-10001 and BC-CON-10011 (docs/lessons/unit-10/README.md, section 1).

## Prediction

Served first, both bands: an mcq on ex-1's own numbers. The stem gives the partial sum, states that the first omitted term has size 1/12, and asks what the error is. Key B, at most 1/12. Option A, that it can exceed 1/12, is false, and C, that it is exactly 1/12, is false (the error is 0.0739). Every distractor is false, so B is the only true option. It is answerable before the rule by seeing that partial sums of a decreasing alternating series straddle the value. The resolution carries no verdict word.

## Orientation

From the concept's description_plain and the topic's Assessment behaviour paragraph (research/units/unit-10-infinite-sequences-series.md#10.10 Alternating Series Error Bound): forms ask a response to show that a partial sum differs from the value by less than a given number, with one point for the correct omitted term and one for the justification, which needs the conditions and the inequality (sg-22:21, sg-24:21). No count, no frequency.

## Key ideas

One essential knowledge statement, BC-EK-LIM-7B1 (ced:195), on all four skills: one core block, both bands. Source: the Required mathematical knowledge paragraphs Alternating series error bound, Strictness of the write up and Which term. No anchor quote. Notation: the concept's notation.

## Recognition

BC-QA-10008 (research/question-analysis/question-archetypes.md#BC-QA-10008 Alternating series error bound compared with a tolerance) is the only archetype loading the four skills. common_givens: a power series and an input value; a partial sum or Taylor polynomial approximation; a tolerance; a statement that the terms alternate and decrease to zero. asked_to_produce: the first omitted term evaluated at the input; the conditions; an inequality against the tolerance; an upper bound. typical_wording: show that the partial sum differs from the value of the series by less than the given amount. The near miss of the contrast pair is the Lagrange bound with a supplied derivative bound (BC-QA-10009, and the wrong_approaches entry of BC-QA-10008). Official examples include BC-FRQ-2022-Q6-B, BC-FRQ-2024-Q6-B and BC-MCQ-SAMPLE-020.

## Method choice

st-1 on BC-QA-10008: method is the four entries of expected_solution_path in order; rival is the wrong_approaches entries, the Lagrange bound and a term inside the partial sum; separating feature is that alternating decreasing terms make the next term the bound. Both cue fields exist, so the block is not inferred. The first block carries the contrast pair.

## Solution path

ex-1, BC-QA-10008, both bands: draw function exp, last 2, point 1/2, multiple 4, bound 1/12 (SymPy). ex-2, low band, faded from step 3: draw function atan, last 2, point 1/2, multiple 5, bound 5/896. No published item on BC-QA-10008 carries either draw (content/items_gen_unit10). Steps 1 and 2 are shown, the student evaluates the omitted term, and steps 3 and 4 then reveal. The fade falls there because the conditions and the omitted term repeat ex-1's pattern, and the evaluation and the inequality are what the student must produce. A fluent solver writes the conditions, the omitted term and the inequality; the index of the omitted term is held.

## Scoring

BC-QA-10008 lists BC-PT-99040, 99041 and 99036. ex-1 tags no point, for the brief band cap (inferred array); ex-2 tags BC-PT-99040 and BC-PT-99041. The lines are reader_checks output. BC-PT-99036 belongs to the Taylor polynomial variant and is untagged (inferred array). Point losses from research: conditions not stated, or the error written as equal to the bound (research/scoring/common-point-losses.md#Justification points, sg-22:21, sg-24:21); a term of the wrong degree does not earn the first point (sg-22:21).

## Traps

Six errors meet the skills; the four in bundle order are BC-ERR-10020, BC-ERR-10024, BC-ERR-10025 and BC-ERR-99016. BC-ERR-10026 and BC-ERR-10027 fall past the cap of 4. Low band all four, mid band the first two. All on ex-1's draw. BC-ERR-10020 is a sentence difference, so relation equivalent and fix_prompt false. The other three are distinct. BC-ERR-99016 is shown as the error written equal to the bound. No possible reason lines, for the brief band words.

## Representations

The topic's Representations paragraph names BC-REP-11, 01 and 04 and no graphical conversion. The lesson adds a computed table, low band: ex-1's series at x = 1/2 for n = 1 to 4, with the partial sum, the actual error and the first omitted term. The values are SymPy output rounded to three places. Rule chosen: the mode table row for a computed sequence of values, `model`, on the representations block, since the example blocks are fixed to step_reveal [inferred].

## Prerequisite bridge

BC-PRQ-06002, 06005, 10001, 10003 and 10008, each from its description_plain and failure_signature.

## Time

BC-QA-10008 is no calculator. The MCQ form is Section I Part A, 2.14 minutes (research/exam/exam-structure.md#Section and part layout). As a free response part: 2 points, 3.33 minutes (docs/lessons/unit-10/README.md, section 5). A fluent solver writes the conditions, the omitted term and the inequality.

## Checks

chk-1 completes ex-1. chk-2 is an isomorph: function sin, last 1, point 1/2, multiple 8, bound 1/480. chk-3, low band, is a 4 option MCQ: function cos, last 2, point 1/2, multiple 6, key 1/7680. Distractors: 1/64, the n = 2 term (BC-ERR-10024); 1/1720320, the n = 4 term (BC-ERR-10024); 1/120, evaluated at x = 1 (BC-ERR-10025).

## Delivery

orientation, ki-1 and the prediction: text (rule 6). Examples and error blocks: step_reveal (rule 1). representations: model, a numeric experiment table with a fallback and a keyboard line [inferred].

## Band plan

Low (full): prediction, orientation, bridges, ki-1, st-1 with the contrast pair, ex-1, chk-1, the four error blocks, ex-2 (faded from step 3) and its lines, chk-2, the model table, chk-3. 782 words, 5.3 minutes. Mid (brief): prediction, orientation, bridges, ki-1, st-1 with the contrast pair, ex-1, chk-1, err-BC-ERR-10020, err-BC-ERR-10024, chk-2. 448 words, 3.0 minutes. Refresher: ki-1, the four error blocks, ex-1.

## Sources

- BC-CON-10015; BC-SKL-10039, 10040, 10041, 10042; BC-EK-LIM-7B1; ced:195
- BC-QA-10008; BC-PT-99040, BC-PT-99041
- BC-ERR-10020, 10024, 10025, 99016; BC-PRQ-06002, 06005, 10001, 10003, 10008
- sg-22:21, sg-24:21
- research/units/unit-10-infinite-sequences-series.md#10.10 Alternating Series Error Bound
- research/exam/exam-structure.md#Section and part layout
- [inferred] the model delivery, the untagged BC-PT-99036, the held steps; each settled as the inferred array states.

## Machine record

```json
{
 "id": "LSN-CON-10015",
 "kind": "concept",
 "target_id": "BC-CON-10015",
 "unit": "10",
 "skills": [
  "BC-SKL-10039",
  "BC-SKL-10040",
  "BC-SKL-10041",
  "BC-SKL-10042"
 ],
 "prediction": {
  "id": "pr-1",
  "stem": {
   "text": "Predict. \\(S_2\\) is a partial sum of the alternating series for \\(4e^{-x}\\), and at \\(x=\\frac12\\) its first omitted term has size \\(\\frac1{12}\\). The error \\(|4e^{-1/2}-S_2|\\) is",
   "command_verb": "predict"
  },
  "format": "mcq",
  "options": [
   {
    "id": "A",
    "label": "It can exceed \\(\\frac1{12}\\)",
    "is_key": false
   },
   {
    "id": "B",
    "label": "It is at most \\(\\frac1{12}\\)",
    "is_key": true
   },
   {
    "id": "C",
    "label": "It is exactly \\(\\frac1{12}\\)",
    "is_key": false
   }
  ],
  "resolution": "Partial sums of a decreasing alternating series fall on alternate sides of the value, so the error is under the next term, here at most \\(\\frac1{12}\\).",
  "sources": [
   "BC-CON-10015",
   "research/units/unit-10-infinite-sequences-series.md#10.10 Alternating Series Error Bound"
  ]
 },
 "orientation": {
  "text": "A partial sum of a series that converges by the alternating series test misses the value by at most the first term left out. A response states the conditions, names that term, evaluates it, and writes the inequality.",
  "sources": [
   "BC-CON-10015",
   "research/units/unit-10-infinite-sequences-series.md#10.10 Alternating Series Error Bound"
  ]
 },
 "key_ideas": [
  {
   "id": "ki-1",
   "ek_id": "BC-EK-LIM-7B1",
   "depth": "core",
   "text": "If an alternating series converges by the alternating series test, then \\(|S-S_n|\\le|a_{n+1}|\\), the first omitted term. The terms must alternate and decrease in absolute value to 0. The bound is an inequality.",
   "notation": "error at most the first omitted term",
   "quote": null,
   "sources": [
    "BC-EK-LIM-7B1",
    "ced:195",
    "sg-22:21",
    "research/units/unit-10-infinite-sequences-series.md#10.10 Alternating Series Error Bound"
   ]
  }
 ],
 "strategy": [
  {
   "id": "st-1",
   "archetype_id": "BC-QA-10008",
   "cue": "A partial sum of an alternating series, error bound asked.",
   "method": "State the conditions, name the first omitted term, evaluate it, write error at most that value.",
   "rival": "The Lagrange bound, or a term inside the partial sum.",
   "separating_feature": "Alternating, decreasing terms make the next term the bound.",
   "sources": [
    "BC-QA-10008"
   ],
   "evidence_tag": "verified",
   "contrast": {
    "this": {
     "text": "Bound the error of the partial sum \\(S_3\\) of \\(\\sum_{n=0}^{\\infty}\\frac{(-1)^{n}x^{n}}{n!}\\) at \\(x=\\frac13\\).",
     "archetype_id": "BC-QA-10008"
    },
    "not_this": {
     "text": "With \\(|f^{(4)}|\\le1\\), bound \\(|\\sin\\frac13-P_3(\\frac13)|\\) for the degree 3 Taylor polynomial about 0.",
     "why_not": "A derivative bound is supplied, which calls for the Lagrange bound."
    },
    "feature": "A supplied derivative bound selects Lagrange."
   }
  }
 ],
 "worked_examples": [
  {
   "id": "ex-1",
   "archetype_id": "BC-QA-10008",
   "bands": [
    "low",
    "mid"
   ],
   "parameter_draw": {
    "function": "exp",
    "last": 2,
    "point": "1/2",
    "multiple": 4
   },
   "problem": {
    "text": "\\(4e^{-x}=\\sum_{n=0}^{\\infty}\\frac{4(-1)^{n}x^{n}}{n!}\\). Let \\(S_2\\) be the partial sum through \\(n=2\\). Use the alternating series error bound for an upper bound on \\(|4e^{-1/2}-S_2|\\).",
    "command_verb": "find"
   },
   "calculator_status": "no_calculator",
   "steps": [
    {
     "cue": "Signs alternate; sizes fall to 0.",
     "why": "Both conditions, stated."
    },
    {
     "cue": "Sum stops at n = 2.",
     "why": "The first omitted term is n = 3.",
     "expr": "4*x**3/factorial(3)",
     "relation": "new"
    },
    {
     "cue": "Evaluate at \\(x=\\frac12\\).",
     "why": "The size of that term at the given input.",
     "expr": "1/12",
     "relation": "evaluate",
     "subs": {
      "x": "1/2"
     }
    },
    {
     "cue": "Write the inequality.",
     "why": "Error at most \\(\\frac1{12}\\)."
    }
   ],
   "answer": {
    "form": "numeric",
    "expr": "1/12"
   }
  },
  {
   "id": "ex-2",
   "archetype_id": "BC-QA-10008",
   "bands": [
    "low"
   ],
   "fade_from": 3,
   "parameter_draw": {
    "function": "atan",
    "last": 2,
    "point": "1/2",
    "multiple": 5
   },
   "problem": {
    "text": "\\(5\\arctan x=\\sum_{n=0}^{\\infty}\\frac{5(-1)^{n}x^{2n+1}}{2n+1}\\). Let \\(S_2\\) be the partial sum through \\(n=2\\). Use the alternating series error bound for an upper bound on \\(|5\\arctan\\tfrac12-S_2|\\).",
    "command_verb": "find"
   },
   "calculator_status": "no_calculator",
   "steps": [
    {
     "cue": "Signs alternate; sizes fall to 0.",
     "why": "Both conditions are stated first."
    },
    {
     "cue": "Sum stops at n = 2.",
     "why": "The first omitted term is n = 3.",
     "expr": "5*x**7/7",
     "relation": "new",
     "point_type_id": "BC-PT-99040"
    },
    {
     "cue": "Evaluate at \\(x=\\frac12\\).",
     "why": "The size of that term at the given input.",
     "expr": "5/896",
     "relation": "evaluate",
     "subs": {
      "x": "1/2"
     }
    },
    {
     "cue": "Write the inequality.",
     "why": "Error at most \\(\\frac5{896}\\).",
     "point_type_id": "BC-PT-99041"
    }
   ],
   "answer": {
    "form": "numeric",
    "expr": "5/896"
   }
  }
 ],
 "what_a_reader_scores": [
  {
   "example_id": "ex-1",
   "point_type_ids": [],
   "lines": []
  },
  {
   "example_id": "ex-2",
   "point_type_ids": [
    "BC-PT-99040",
    "BC-PT-99041"
   ],
   "lines": [
    {
     "point_type_id": "BC-PT-99040",
     "text": "Alternating series error bound, first omitted term. Earned by: Evaluating the first omitted term of the alternating series at the requested value (sg-26:22, sg-22:21). Not earned by: Using a term of the wrong degree; sg-22:21 states any term of degree five or higher does not earn the point, and sg-22:21 states listing the term inside a polynomial is insufficient."
    },
    {
     "point_type_id": "BC-PT-99041",
     "text": "Error bound analysis with an explicit inequality. Earned by: Connecting the computed bound to the target value with an inequality, for example writing that the error is at most the stated number (sg-25:22, sg-22:21). Not earned by: Declaring the error equal to the bound rather than bounded by it; sg-25:22, sg-26:22, sg-23:20 and sg-22:21 all withhold the point for an equality claim."
    }
   ]
  }
 ],
 "common_errors": [
  {
   "error_id": "BC-ERR-10020",
   "observed_behavior": "The response invokes the alternating series test or its error bound without stating that the terms alternate and decrease in absolute value to zero.",
   "scoring_consequence": "The justification point requires both conditions to be stated (sg-22:21, sg-24:21).",
   "wrong_step": {
    "text": "No conditions stated.",
    "expr": "1/12"
   },
   "right_step": {
    "text": "Conditions stated first.",
    "expr": "1/12"
   },
   "relation": "equivalent",
   "possible_reason": null,
   "sources": [
    "BC-ERR-10020"
   ],
   "fix_prompt": false
  },
  {
   "error_id": "BC-ERR-10024",
   "observed_behavior": "The response bounds the error with a term already included in the partial sum, or with a term further along than the first omitted one.",
   "scoring_consequence": "The first point is earned only for the correct omitted term, and a term of higher degree does not earn it (sg-22:21).",
   "wrong_step": {
    "text": "The n = 2 term.",
    "expr": "4*(1/2)**2/factorial(2)"
   },
   "right_step": {
    "text": "The n = 3 term.",
    "expr": "4*(1/2)**3/factorial(3)"
   },
   "relation": "distinct",
   "possible_reason": null,
   "sources": [
    "BC-ERR-10024"
   ],
   "fix_prompt": true
  },
  {
   "error_id": "BC-ERR-10025",
   "observed_behavior": "The response identifies the correct omitted term but substitutes the index, the centre, or another value in place of the stated input.",
   "scoring_consequence": "The point attached to using the term correctly is lost (sg-22:21).",
   "wrong_step": {
    "text": "The term at x = 1.",
    "expr": "4*1**3/factorial(3)"
   },
   "right_step": {
    "text": "The term at \\(x=\\frac12\\).",
    "expr": "4*(1/2)**3/factorial(3)"
   },
   "relation": "distinct",
   "possible_reason": null,
   "sources": [
    "BC-ERR-10025"
   ],
   "fix_prompt": true
  },
  {
   "error_id": "BC-ERR-99016",
   "observed_behavior": "Responses invoke an error bound without confirming that the series alternates with terms decreasing to zero, reach for the Lagrange bound where the alternating series bound applies, or write the error as equal to or strictly less than the bound instead of at most the bound.",
   "scoring_consequence": "The condition or analysis point is lost even when the numerical bound is computed correctly.",
   "wrong_step": {
    "text": "The error written as equal to the bound.",
    "expr": "1/12"
   },
   "right_step": {
    "text": "The error written as at most the bound.",
    "expr": "1/12"
   },
   "relation": "equivalent",
   "possible_reason": null,
   "sources": [
    "BC-ERR-99016"
   ],
   "fix_prompt": false
  }
 ],
 "representations": {
  "text": "Ex-1 at x = 1/2: the error stays below the first omitted term.",
  "figure": {
   "kind": "numeric_experiment",
   "series": "4*(-1)**n*x**n/factorial(n)",
   "x": "1/2",
   "n_values": [
    1,
    2,
    3,
    4
   ],
   "columns": [
    "n",
    "S_n",
    "actual error",
    "first omitted term"
   ],
   "rows": [
    [
     "1",
     "2.000",
     "0.426",
     "0.500"
    ],
    [
     "2",
     "2.500",
     "0.074",
     "0.083"
    ],
    [
     "3",
     "2.417",
     "0.009",
     "0.010"
    ],
    [
     "4",
     "2.427",
     "0.00096",
     "0.00104"
    ]
   ],
   "labels": [
    {
     "text": "error below the omitted term in every row",
     "placement": "inside",
     "at": "row below the last value"
    }
   ]
  },
  "sources": [
   "research/units/unit-10-infinite-sequences-series.md#10.10 Alternating Series Error Bound",
   "BC-QA-10008"
  ]
 },
 "prerequisite_bridges": [
  {
   "prq_id": "BC-PRQ-06002",
   "text": "Powers evaluate at the input."
  },
  {
   "prq_id": "BC-PRQ-06005",
   "text": "The error is a value at the input."
  },
  {
   "prq_id": "BC-PRQ-10001",
   "text": "Absolute values read as two sided."
  },
  {
   "prq_id": "BC-PRQ-10003",
   "text": "The omitted index is one past the last."
  },
  {
   "prq_id": "BC-PRQ-10008",
   "text": "Read the term, keeping the sign factor."
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
   "archetype_id": "BC-QA-10008",
   "parameter_draw": {
    "function": "exp",
    "last": 2,
    "point": "1/2",
    "multiple": 4
   },
   "completes": "ex-1",
   "stem": {
    "text": "The first omitted term of \\(S_2\\) is \\(\\frac{4x^{3}}{3!}\\). Give the error bound for \\(|4e^{-1/2}-S_2|\\).",
    "command_verb": "give"
   },
   "key": {
    "form": "numeric",
    "expr": "1/12"
   },
   "steps": [
    {
     "text": "First omitted term.",
     "expr": "4*x**3/factorial(3)",
     "relation": "new"
    },
    {
     "text": "At x = 1/2.",
     "expr": "1/12",
     "relation": "evaluate",
     "subs": {
      "x": "1/2"
     }
    }
   ],
   "calculator_status": "no_calculator",
   "skills": [
    "BC-SKL-10041"
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
   "archetype_id": "BC-QA-10008",
   "parameter_draw": {
    "function": "sin",
    "last": 1,
    "point": "1/2",
    "multiple": 8
   },
   "stem": {
    "text": "\\(8\\sin x=\\sum_{n=0}^{\\infty}\\frac{8(-1)^{n}x^{2n+1}}{(2n+1)!}\\). With \\(S_1\\) the partial sum through \\(n=1\\), bound \\(|8\\sin\\tfrac12-S_1|\\).",
    "command_verb": "find"
   },
   "key": {
    "form": "numeric",
    "expr": "1/480"
   },
   "steps": [
    {
     "text": "First omitted term, n = 2.",
     "expr": "8*x**5/factorial(5)",
     "relation": "new"
    },
    {
     "text": "At x = 1/2.",
     "expr": "1/480",
     "relation": "evaluate",
     "subs": {
      "x": "1/2"
     }
    }
   ],
   "calculator_status": "no_calculator",
   "skills": [
    "BC-SKL-10040",
    "BC-SKL-10041"
   ]
  },
  {
   "id": "chk-3",
   "check_kind": "mcq",
   "format": "mcq",
   "bands": [
    "low"
   ],
   "archetype_id": "BC-QA-10008",
   "parameter_draw": {
    "function": "cos",
    "last": 2,
    "point": "1/2",
    "multiple": 6
   },
   "stem": {
    "text": "\\(6\\cos x=\\sum_{n=0}^{\\infty}\\frac{6(-1)^{n}x^{2n}}{(2n)!}\\). With \\(S_2\\) the partial sum through \\(n=2\\), a bound for \\(|6\\cos\\tfrac12-S_2|\\) is",
    "command_verb": "identify"
   },
   "key": {
    "form": "numeric",
    "expr": "1/7680"
   },
   "steps": [
    {
     "text": "First omitted term, n = 3.",
     "expr": "6*x**6/factorial(6)",
     "relation": "new"
    },
    {
     "text": "At x = 1/2.",
     "expr": "1/7680",
     "relation": "evaluate",
     "subs": {
      "x": "1/2"
     }
    }
   ],
   "options": [
    {
     "id": "A",
     "is_key": false,
     "expr": "1/64",
     "error_path": "BC-ERR-10024",
     "derivation": "the n = 2 term, already inside the partial sum"
    },
    {
     "id": "B",
     "is_key": false,
     "expr": "1/1720320",
     "error_path": "BC-ERR-10024",
     "derivation": "the n = 4 term, one past the first omitted term"
    },
    {
     "id": "C",
     "is_key": true,
     "expr": "1/7680",
     "error_path": null
    },
    {
     "id": "D",
     "is_key": false,
     "expr": "1/120",
     "error_path": "BC-ERR-10025",
     "derivation": "the first omitted term evaluated at x = 1 instead of 1/2"
    }
   ],
   "calculator_status": "no_calculator",
   "skills": [
    "BC-SKL-10040",
    "BC-SKL-10041"
   ]
  }
 ],
 "delivery": [
  {
   "block": "pr-1",
   "mode": "text",
   "reason": "rule 6: a question on an inequality, no figure-bearing representation",
   "sources": [
    "BC-CON-10015"
   ]
  },
  {
   "block": "orientation",
   "mode": "text",
   "reason": "rule 6: a statement of what a response shows",
   "sources": [
    "BC-CON-10015"
   ]
  },
  {
   "block": "ki-1",
   "mode": "text",
   "reason": "rule 6: BC-REP-11, 01, 04 on BC-SKL-10039 to 10042, none figure-bearing; the key idea states a bound, not a process",
   "sources": [
    "BC-SKL-10039",
    "BC-SKL-10040",
    "BC-SKL-10041",
    "BC-SKL-10042"
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
   "block": "err-BC-ERR-10020",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  },
  {
   "block": "err-BC-ERR-10024",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  },
  {
   "block": "err-BC-ERR-10025",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  },
  {
   "block": "err-BC-ERR-99016",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  },
  {
   "block": "representations",
   "mode": "model",
   "reason": "template model row [inferred]: the idea is the behaviour of a computed sequence, the error beside the first omitted term at growing n (unit README delivery map)",
   "sources": [
    "BC-QA-10008",
    "BC-EK-LIM-7B1"
   ],
   "spec": {
    "kind": "numeric_experiment",
    "representations": [
     "BC-REP-11"
    ],
    "series": "4*(-1)**n*x**n/factorial(n)",
    "x": "1/2",
    "n_values": [
     1,
     2,
     3,
     4
    ],
    "columns": [
     "n",
     "S_n",
     "actual error",
     "first omitted term"
    ],
    "labels": [
     {
      "text": "n",
      "placement": "inside",
      "at": "first column header"
     },
     {
      "text": "error below the omitted term in every row",
      "placement": "inside",
      "at": "row below the last value"
     }
    ]
   },
   "fallback": "the four computed rows printed as a static table with the closing label",
   "keyboard": "a Run control reached by Tab and pressed with Enter or Space adds one row per press; the table is read in row order"
  }
 ],
 "refresher": [
  "ki-1",
  "err-BC-ERR-10020",
  "err-BC-ERR-10024",
  "err-BC-ERR-10025",
  "err-BC-ERR-99016",
  "ex-1"
 ],
 "research_lines": [
  {
   "file": "research/units/unit-10-infinite-sequences-series.md",
   "line": "the absolute difference between the series value and a partial sum is at most the absolute value of the first omitted term"
  }
 ],
 "inferred": [
  {
   "claim": "The model on the representations block is chosen under the mode table row for a computed sequence of values; rule 2 does not fire because BC-EK-LIM-7B1 states a bound, not a process.",
   "settles": "The modality A/B in the build plan (skip rate and time to first credited success by mode)."
  },
  {
   "claim": "ex-1 tags no point, because its two reader lines would take 121 words of the 450 word brief band; ex-2 tags BC-PT-99040 and BC-PT-99041. BC-PT-99036 is untagged because it scores the polynomial form of a Taylor variant.",
   "settles": "A brief cap that admits both reader lines on ex-1."
  },
  {
   "claim": "A fluent solver writes the conditions, the omitted term and the inequality, and holds the index of the first omitted term.",
   "settles": "Timing data per step once the fluency telemetry exists."
  }
 ],
 "sources": [
  "BC-CON-10015",
  "BC-SKL-10039",
  "BC-SKL-10040",
  "BC-SKL-10041",
  "BC-SKL-10042",
  "BC-EK-LIM-7B1",
  "ced:195",
  "BC-QA-10008",
  "BC-PT-99040",
  "BC-PT-99041",
  "BC-ERR-10020",
  "BC-ERR-10024",
  "BC-ERR-10025",
  "BC-ERR-99016",
  "BC-PRQ-06002",
  "BC-PRQ-06005",
  "BC-PRQ-10001",
  "BC-PRQ-10003",
  "BC-PRQ-10008",
  "sg-22:21",
  "sg-24:21",
  "research/units/unit-10-infinite-sequences-series.md#10.10 Alternating Series Error Bound",
  "research/exam/exam-structure.md#Section and part layout"
 ],
 "word_count": {
  "full": 782,
  "brief": 448
 },
 "read_minutes": {
  "full": 5.3,
  "brief": 3.0
 }
}
```
