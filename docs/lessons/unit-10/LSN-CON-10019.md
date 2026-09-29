---
title: LSN-CON-10019 Choosing between the Lagrange and alternating series bounds
research_date: 2026-09-29
status: designed
purpose: Authoring spec for the concept lesson on BC-CON-10019, the choice of error bound for a Taylor approximation by the hypotheses that hold, the alternating series bound when the terms alternate and shrink to 0 and the Lagrange bound when a derivative bound is given, built from authoring_bundle("BC-CON-10019") and the research files it cites, so an author fills plan 15's lesson record without making a teaching decision.
---

# LSN-CON-10019 Choosing between the Lagrange and alternating series bounds

## Prediction

Served first, both bands: an `mcq` on ex-1's numbers. The series for 4 arctan x at x = 1/2 alternates with shrinking terms, S_2 = 223/120 and S_3 = S_2 - 1/224, and the student picks where the sum lies: above S_2, between S_3 and S_2, or below S_3. Key B. The student can reason it from the zig-zag of the partial sums before any bound is taught, and only B holds (SymPy: S_3 = 1.85387, the sum 1.85459, S_2 = 1.85833). The resolution names the first omitted term as the size of the error and the conditions it needs, with no verdict word. Source: BC-CON-10019 and the topic 10.12 section the key ideas cite.

## Orientation

Served text from BC-CON-10019 `description_plain` (two bounds are available and the hypotheses decide which applies) and the topic's Assessment behaviour paragraph (parts are no calculator; the form and the comparison are scored separately, sg-23:20). The orientation states what a response shows: the conditions that hold, the matching bound, the error at most that bound. No count, no frequency.

## Key ideas

Two core blocks, one per essential knowledge statement the skill maps (ced:197): ki-1 BC-EK-LIM-8C1 (the Lagrange bound and its hypothesis, a bound on the next derivative) and ki-2 BC-EK-LIM-8C2 (the alternating series bound for a Taylor approximation "in some situations", with the alternating, shrinking, limit-zero conditions, sg-22:21, sg-26:22). Both core, so both serve the brief band. Notation line on ki-1 only: the concept's `notation`. No anchor quote.

## Recognition

Two archetypes load BC-SKL-10052, both family taylor-error and both `no_calculator`.

- BC-QA-10008 `common_givens`: "a power series and an input value", "a statement that the terms alternate and decrease to zero". `asked_to_produce`: "the first omitted term evaluated at the given input". Official examples BC-FRQ-2012-Q6-B, 2019-Q6-D, 2021-Q6-D, 2022-Q6-B, 2024-Q6-B, 2026-Q6-C, 2018-Q6-C.
- BC-QA-10009 `common_givens`: "a bound on the next derivative over an interval". Official examples BC-FRQ-2023-Q6-B, 2025-Q5-C.

What selects each (docs/lessons/unit-10/README.md, section 3, the Lagrange against alternating row): a supplied bound on the next derivative selects Lagrange, a series whose terms alternate and decrease to zero at the input selects the first omitted term. The contrast pair is the README's row: an alternating stem of BC-QA-10008's shape beside a Lagrange stem from BC-QA-10009.

## Method choice

- st-1, BC-QA-10008, verified. Cue from `common_givens`. Method `expected_solution_path[0]` and [1]: state the conditions, identify the first omitted term. Rival from `wrong_approaches`: reaching for the Lagrange bound where the alternating bound applies. Feature: alternating shrinking terms. The block carries the contrast pair.
- st-2, BC-QA-10009, low band only. Cue from `common_givens`, method `expected_solution_path[1]`, rival the first omitted term of a series that does not alternate, feature a supplied derivative bound. No field opens with the reader's own label.

## Solution path

- ex-1, BC-QA-10008, both bands, no calculator. Draw: function atan, last 2, point 1/2, multiple 4, so f(x) = 4 arctan x, S_2 = 223/120, first omitted term 4x^7/7 = 1/224 at 1/2 (SymPy). The stem matches the prediction's numbers. No published item on BC-QA-10008 carries this draw.
- ex-2, low band, faded from step 3. Draw (BC-QA-10009): given bound, degree 2, centre -1, step 1/3, maximum 6, minimum 1, target -2/3, bound 6/3! times (1/3)^3 = 1/27 (SymPy). The stem states that no series is given, which is what turns the choice. Steps 1 and 2 (the choice and the assembled form) are shown, the student writes the value, and steps 3 and 4 then reveal. The fade falls there because the choice and the form are the lesson and the evaluation is the part to produce.
- ex-1 steps: the conditions (a sentence), the first omitted term (new), its value (evaluate), the inequality sentence. A fluent solver writes the conditions, the value and the inequality, and holds the identification of the term (Time). No productive-failure comparison.

## Scoring

BC-QA-10008 lists BC-PT-99040, 99041 and 99036; ex-1 earns BC-PT-99040 on the evaluated first omitted term and BC-PT-99041 on its inequality, but tags neither, because the reader lines do not fit the brief cap (inferred array), so its scoring entry is empty. BC-QA-10009 lists BC-PT-99039 and 99041; ex-2 tags both. The lines are `reader_checks` output.

Point losses from research: a bound whose conditions are not met earns no justification point (BC-ERR-10033, sg-24:21); the conditions for an error bound not stated, or the error written as equal to the bound (research/scoring/common-point-losses.md#Justification points, BC-ERR-99016); the alternating bound needs the statement that the series is alternating with terms decreasing in absolute value to zero (research/scoring/justification-requirements.md#Justification inside series work, sg-26:22, sg-22:21).

## Traps

Two active errors meet BC-SKL-10052, in bundle order: BC-ERR-10033 and BC-ERR-99016. Both are shown, on ex-1's draw. BC-ERR-10033 is distinct (`fix_prompt` true): the Lagrange form with an unstated M against the first omitted term 1/224; no `possible_reason` line (brief band words). BC-ERR-99016 is equivalent (`fix_prompt` false): the value 1/224 is right and the sign is equals against at most.

## Representations

None. The topic's Representations paragraph names BC-REP-01 and 04, and the conversions supplied bound to assembled bound, and evaluated bound to inequality chain; nothing figure-shaped.

## Prerequisite bridge

- BC-PRQ-06005, from its `description_plain` and `failure_signature`: what the bound is about.

## Time

The MCQ shape is Section I Part A, 2.14 minutes (research/exam/exam-structure.md#Section and part layout). As a free response part, 2 points, 3.33 minutes (docs/lessons/unit-10/README.md, section 5). A fluent solver writes the conditions, the value and the inequality, and holds the identification of the first omitted term [inferred]. The minutes go on the choice and its justification.

## Checks

- chk-1, completion of ex-1, both bands: the term given, its size asked. Key 1/224.
- chk-2, isomorph, both bands (BC-QA-10008). Draw: function cos, last 1, point 2/3, multiple 6, first omitted term 6x^4/4! at 2/3 = 4/81.
- chk-3, MCQ, low band, statement key (BC-QA-10009). Draw: given endpoints, degree 3, centre 2, step 1/2, maximum 9, minimum 4. Key: Lagrange with M = 9, at most 3/128. Distractors: the alternating first omitted term 1/96 (BC-ERR-10033), the alternating bound with the number 3/128 (BC-ERR-10033), Lagrange with an equals sign (BC-ERR-99016).

## Delivery

- pr-1, orientation, ki-1, ki-2: text. Rule 6, BC-REP-04 and 11 on BC-SKL-10052, neither figure-bearing, and the unit README delivery map names text for both statements. The record carries `no_figure_reason`.
- ex-1, ex-2, the two error blocks: step_reveal. Rule 1.

## Band plan

- Low (full): prediction, orientation, bridge, ki-1, ki-2, st-1 with the contrast pair, st-2, ex-1 and its line, chk-1, the two error blocks, ex-2 (faded from step 3) and its lines, chk-2, chk-3. 738 words, 5.0 minutes.
- Mid (brief): prediction, orientation, bridge, ki-1, ki-2, st-1 with the contrast pair, ex-1 and its line, chk-1, the two error blocks, chk-2. 445 words, 3.0 minutes.
- Refresher: ki-1, ki-2, the two error blocks, ex-1.

## Sources

- BC-CON-10019; BC-SKL-10052; BC-EK-LIM-8C1, BC-EK-LIM-8C2; ced:197
- BC-QA-10008; BC-QA-10009; BC-PT-99039, BC-PT-99040, BC-PT-99041
- BC-ERR-10033, BC-ERR-99016
- BC-PRQ-06005
- sg-22:21, sg-24:21, sg-26:22
- research/units/unit-10-infinite-sequences-series.md#10.12 Lagrange Error Bound
- research/question-analysis/question-archetypes.md#BC-QA-10008 Alternating series error bound compared with a tolerance
- research/question-analysis/question-archetypes.md#BC-QA-10009 Lagrange error bound with a supplied derivative bound
- research/scoring/common-point-losses.md#Justification points
- research/scoring/justification-requirements.md#Justification inside series work
- research/exam/exam-structure.md#Section and part layout
- [inferred] the statement-key check 3, the held steps, the untagged reader lines on ex-1, the BC-ERR-10033 wrong step. Each settled as the inferred array states.

## Machine record

```json
{
 "id": "LSN-CON-10019",
 "kind": "concept",
 "target_id": "BC-CON-10019",
 "unit": "10",
 "skills": [
  "BC-SKL-10052"
 ],
 "prediction": {
  "id": "pr-1",
  "stem": {
   "text": "The terms of \\(\\sum_{n=0}^{\\infty}(-1)^n\\frac{4x^{2n+1}}{2n+1}\\) alternate and shrink at \\(x=\\tfrac12\\), with \\(S_2=\\frac{223}{120}\\) and \\(S_3=S_2-\\frac{1}{224}\\). Predict where the sum \\(S\\) lies.",
   "command_verb": "predict"
  },
  "format": "mcq",
  "options": [
   {
    "id": "A",
    "label": "above \\(S_2\\)",
    "is_key": false
   },
   {
    "id": "B",
    "label": "between \\(S_3\\) and \\(S_2\\)",
    "is_key": true
   },
   {
    "id": "C",
    "label": "below \\(S_3\\)",
    "is_key": false
   }
  ],
  "resolution": "Partial sums swing across the sum, so \\(S\\) lies between \\(S_3\\) and \\(S_2\\), and \\(|S-S_2|\\le\\frac{1}{224}\\), the first omitted term.",
  "sources": [
   "BC-CON-10019",
   "research/units/unit-10-infinite-sequences-series.md#10.12 Lagrange Error Bound"
  ]
 },
 "no_figure_reason": "No skill of this concept carries a figure-bearing representation, and the concept is a choice between two written bounds by their hypotheses, not a process.",
 "orientation": {
  "text": "Two bounds are available for a Taylor approximation, and the hypotheses decide which applies. A response states the conditions that hold, writes the matching bound, and gives the error as at most that bound.",
  "sources": [
   "BC-CON-10019",
   "research/units/unit-10-infinite-sequences-series.md#10.12 Lagrange Error Bound"
  ]
 },
 "key_ideas": [
  {
   "id": "ki-1",
   "ek_id": "BC-EK-LIM-8C1",
   "depth": "core",
   "text": "With \\(|f^{(n+1)}|\\le M\\) between \\(a\\) and \\(x\\), the error of \\(P_n\\) is at most \\(\\frac{M}{(n+1)!}|x-a|^{n+1}\\).",
   "notation": "error bound selection",
   "quote": null,
   "sources": [
    "BC-EK-LIM-8C1",
    "ced:197",
    "research/units/unit-10-infinite-sequences-series.md#10.12 Lagrange Error Bound"
   ]
  },
  {
   "id": "ki-2",
   "ek_id": "BC-EK-LIM-8C2",
   "depth": "core",
   "text": "In some situations the alternating series bound applies to a Taylor approximation. Terms that alternate and shrink to 0 at the input make the error at most the first omitted term.",
   "notation": "",
   "quote": null,
   "sources": [
    "BC-EK-LIM-8C2",
    "ced:197",
    "sg-22:21",
    "sg-26:22",
    "research/units/unit-10-infinite-sequences-series.md#10.12 Lagrange Error Bound"
   ]
  }
 ],
 "strategy": [
  {
   "id": "st-1",
   "archetype_id": "BC-QA-10008",
   "cue": "A series whose terms alternate and shrink at the input.",
   "method": "State that the terms alternate and shrink to 0, then take the first omitted term.",
   "rival": "The Lagrange bound, with no derivative bound given.",
   "separating_feature": "Alternating shrinking terms select the first omitted term.",
   "sources": [
    "BC-QA-10008"
   ],
   "evidence_tag": "verified",
   "contrast": {
    "this": {
     "text": "Let \\(S_2\\) be the partial sum through \\(n=2\\) of \\(\\sum_{n=0}^{\\infty}(-1)^n\\frac{x^{2n+1}}{(2n+1)!}\\). Find an upper bound for \\(|\\sin\\tfrac12-S_2|\\).",
     "archetype_id": "BC-QA-10008"
    },
    "not_this": {
     "text": "Let \\(P_2\\) be the degree 2 Taylor polynomial of \\(f\\) about \\(x=1\\), with \\(|f'''|\\le6\\) on \\([1,\\frac32]\\). Find an upper bound for \\(|f(\\tfrac32)-P_2(\\tfrac32)|\\).",
     "why_not": "No alternating series is given, so the Lagrange bound applies."
    },
    "feature": "Alternating shrinking terms, against a supplied derivative bound."
   }
  },
  {
   "id": "st-2",
   "archetype_id": "BC-QA-10009",
   "cue": "A bound on the next derivative on an interval.",
   "method": "Write the Lagrange bound from that bound and the distance.",
   "rival": "The first omitted term of a series that does not alternate.",
   "separating_feature": "A supplied derivative bound with no alternating series.",
   "sources": [
    "BC-QA-10009"
   ],
   "evidence_tag": "verified"
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
    "function": "atan",
    "last": 2,
    "point": "1/2",
    "multiple": 4
   },
   "problem": {
    "text": "The series for \\(f(x)=4\\arctan x\\) is \\(\\sum_{n=0}^{\\infty}(-1)^n\\frac{4x^{2n+1}}{2n+1}\\). Let \\(S_2\\) be its partial sum through \\(n=2\\). Find an upper bound for \\(|f(\\tfrac12)-S_2|\\).",
    "command_verb": "find"
   },
   "calculator_status": "no_calculator",
   "steps": [
    {
     "cue": "Terms alternate and shrink to 0 at \\(x=\\tfrac12\\).",
     "why": "The alternating bound applies."
    },
    {
     "cue": "First omitted term is \\(n=3\\).",
     "why": "\\(S_2\\) stops at \\(n=2\\).",
     "expr": "4*x**7/7",
     "relation": "new"
    },
    {
     "cue": "Evaluate at \\(x=\\tfrac12\\).",
     "why": "Its size is the bound.",
     "expr": "1/224",
     "relation": "evaluate",
     "subs": {
      "x": "1/2"
     }
    },
    {
     "cue": "State the inequality.",
     "why": "The error is at most that term."
    }
   ],
   "answer": {
    "form": "numeric",
    "expr": "1/224"
   }
  },
  {
   "id": "ex-2",
   "archetype_id": "BC-QA-10009",
   "bands": [
    "low"
   ],
   "fade_from": 3,
   "parameter_draw": {
    "given": "bound",
    "degree": 2,
    "centre": -1,
    "step": "1/3",
    "maximum": 6,
    "minimum": 1
   },
   "problem": {
    "text": "Let \\(P_2\\) be the Taylor polynomial of degree 2 for \\(f\\) about \\(x=-1\\). On \\([-1,-\\frac23]\\), \\(|f'''(x)|\\le6\\), and no series for \\(f\\) is given. Find an upper bound for \\(|f(-\\tfrac23)-P_2(-\\tfrac23)|\\).",
    "command_verb": "find"
   },
   "calculator_status": "no_calculator",
   "steps": [
    {
     "cue": "No alternating series, a derivative bound.",
     "why": "So the Lagrange bound is the tool."
    },
    {
     "cue": "Degree 2 needs \\(f'''\\), so \\(M=6\\).",
     "why": "Power and factorial are both 3.",
     "expr": "6*Abs(-2/3 - (-1))**3/factorial(3)",
     "relation": "new",
     "point_type_id": "BC-PT-99039"
    },
    {
     "cue": "The distance is \\(\\frac13\\).",
     "why": "Evaluate.",
     "expr": "1/27",
     "relation": "equivalent"
    },
    {
     "cue": "State the inequality.",
     "why": "The error is at most the bound.",
     "point_type_id": "BC-PT-99041"
    }
   ],
   "answer": {
    "form": "numeric",
    "expr": "1/27"
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
    "BC-PT-99039",
    "BC-PT-99041"
   ],
   "lines": [
    {
     "point_type_id": "BC-PT-99039",
     "text": "Lagrange error bound form. Earned by: The bound written as the maximum of the next derivative over the interval, divided by the factorial, times the distance raised to the matching power, or its evaluated form (sg-25:22, sg-23:20). Not earned by: A bound with the wrong factorial or the wrong power of the distance (sg-23:20)."
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
   "error_id": "BC-ERR-10033",
   "observed_behavior": "The response reaches for the Lagrange bound where the alternating series bound is the available tool, or the reverse, without checking the conditions.",
   "scoring_consequence": "A bound whose conditions are not met earns no justification point (sg-24:21).",
   "wrong_step": {
    "text": "\\(\\frac{M}{6!}\\left(\\tfrac12\\right)^6\\), with no \\(M\\) given.",
    "expr": "M*(1/2)**6/factorial(6)"
   },
   "right_step": {
    "text": "First omitted term, \\(\\frac{1}{224}\\).",
    "expr": "4*(1/2)**7/7"
   },
   "relation": "distinct",
   "fix_prompt": true,
   "possible_reason": null,
   "sources": [
    "BC-ERR-10033"
   ]
  },
  {
   "error_id": "BC-ERR-99016",
   "observed_behavior": "Responses invoke an error bound without confirming that the series alternates with terms decreasing to zero, reach for the Lagrange bound where the alternating series bound applies, or write the error as equal to or strictly less than the bound instead of at most the bound.",
   "scoring_consequence": "The condition or analysis point is lost even when the numerical bound is computed correctly.",
   "wrong_step": {
    "text": "Error \\(=\\frac{1}{224}\\).",
    "expr": "1/224"
   },
   "right_step": {
    "text": "Error \\(\\le\\frac{1}{224}\\).",
    "expr": "1/224"
   },
   "relation": "equivalent",
   "fix_prompt": false,
   "possible_reason": null,
   "sources": [
    "BC-ERR-99016"
   ]
  }
 ],
 "representations": null,
 "prerequisite_bridges": [
  {
   "prq_id": "BC-PRQ-06005",
   "text": "The bound is on \\(f^{(n+1)}\\) or on the series terms, not on \\(f\\)."
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
    4
   ]
  },
  "skipped_steps": {
   "ex-1": [
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
   "archetype_id": "BC-QA-10008",
   "parameter_draw": {
    "function": "atan",
    "last": 2,
    "point": "1/2",
    "multiple": 4
   },
   "completes": "ex-1",
   "stem": {
    "text": "The first omitted term of \\(S_2\\) is \\(\\frac{4x^7}{7}\\). Write its size at \\(x=\\tfrac12\\), the upper bound.",
    "command_verb": "write"
   },
   "key": {
    "form": "numeric",
    "expr": "1/224"
   },
   "steps": [
    {
     "text": "Term.",
     "expr": "4*(1/2)**7/7",
     "relation": "new"
    },
    {
     "text": "Evaluate.",
     "expr": "1/224",
     "relation": "equivalent"
    }
   ],
   "calculator_status": "no_calculator",
   "skills": [
    "BC-SKL-10052"
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
    "function": "cos",
    "last": 1,
    "point": "2/3",
    "multiple": 6
   },
   "stem": {
    "text": "The series for \\(f(x)=6\\cos x\\) is \\(\\sum_{n=0}^{\\infty}(-1)^n\\frac{6x^{2n}}{(2n)!}\\). Let \\(S_1\\) be its partial sum through \\(n=1\\). Find an upper bound for \\(|f(\\tfrac23)-S_1|\\).",
    "command_verb": "find"
   },
   "key": {
    "form": "numeric",
    "expr": "4/81"
   },
   "steps": [
    {
     "text": "First omitted term, n = 2.",
     "expr": "6*x**4/factorial(4)",
     "relation": "new"
    },
    {
     "text": "Evaluate.",
     "expr": "4/81",
     "relation": "evaluate",
     "subs": {
      "x": "2/3"
     }
    }
   ],
   "calculator_status": "no_calculator",
   "skills": [
    "BC-SKL-10052"
   ]
  },
  {
   "id": "chk-3",
   "check_kind": "mcq",
   "format": "mcq",
   "bands": [
    "low"
   ],
   "archetype_id": "BC-QA-10009",
   "parameter_draw": {
    "given": "endpoints",
    "degree": 3,
    "centre": 2,
    "step": "1/2",
    "maximum": 9,
    "minimum": 4
   },
   "stem": {
    "text": "Let \\(P_3\\) be the degree 3 Taylor polynomial of \\(f\\) about \\(x=2\\). On \\([2,\\frac52]\\), \\(f^{(4)}\\) is positive and increasing, with \\(f^{(4)}(2)=4\\) and \\(f^{(4)}(\\tfrac52)=9\\). No series for \\(f\\) is given. Which statement bounds \\(|f(\\tfrac52)-P_3(\\tfrac52)|\\)?",
    "command_verb": "identify"
   },
   "key": {
    "form": "statement",
    "label": "Lagrange bound with \\(M=9\\): the error is at most \\(\\frac{3}{128}\\)."
   },
   "options": [
    {
     "id": "A",
     "is_key": true,
     "label": "Lagrange bound with \\(M=9\\): the error is at most \\(\\frac{3}{128}\\).",
     "error_path": null
    },
    {
     "id": "B",
     "is_key": false,
     "label": "Alternating bound, first omitted term: the error is at most \\(\\frac{1}{96}\\).",
     "error_path": "BC-ERR-10033",
     "derivation": "the next Taylor term 4/4! times (1/2)^4 = 1/96 taken as the bound, with no alternating series given"
    },
    {
     "id": "C",
     "is_key": false,
     "label": "Alternating bound: the error is at most \\(\\frac{3}{128}\\).",
     "error_path": "BC-ERR-10033",
     "derivation": "the right number under the alternating bound, whose conditions the situation does not meet"
    },
    {
     "id": "D",
     "is_key": false,
     "label": "Lagrange bound with \\(M=9\\): the error equals \\(\\frac{3}{128}\\).",
     "error_path": "BC-ERR-99016",
     "derivation": "the error written as equal to the bound"
    }
   ],
   "calculator_status": "no_calculator",
   "skills": [
    "BC-SKL-10052"
   ]
  }
 ],
 "delivery": [
  {
   "block": "pr-1",
   "mode": "text",
   "reason": "rule 6: a question on ex-1's own numbers",
   "sources": [
    "BC-CON-10019"
   ]
  },
  {
   "block": "orientation",
   "mode": "text",
   "reason": "rule 6: a statement of what a response shows",
   "sources": [
    "BC-CON-10019"
   ]
  },
  {
   "block": "ki-1",
   "mode": "text",
   "reason": "rule 6: BC-REP-04 and 11 on BC-SKL-10052, neither figure-bearing; a written bound with its hypotheses",
   "sources": [
    "BC-SKL-10052",
    "BC-EK-LIM-8C1"
   ]
  },
  {
   "block": "ki-2",
   "mode": "text",
   "reason": "rule 6: BC-REP-04 and 11 on BC-SKL-10052, neither figure-bearing; the conditions of a written bound",
   "sources": [
    "BC-SKL-10052",
    "BC-EK-LIM-8C2"
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
   "block": "err-BC-ERR-10033",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  },
  {
   "block": "err-BC-ERR-99016",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  }
 ],
 "refresher": [
  "ki-1",
  "ki-2",
  "err-BC-ERR-10033",
  "err-BC-ERR-99016",
  "ex-1"
 ],
 "research_lines": [
  {
   "file": "research/units/unit-10-infinite-sequences-series.md",
   "line": "In some situations the alternating series error bound can bound the error of a Taylor polynomial approximation"
  }
 ],
 "inferred": [
  {
   "claim": "Check 3 is a statement-key multiple choice whose options name a bound and its value, because BC-SKL-10052 holds two errors, BC-ERR-10033 and BC-ERR-99016, and only BC-ERR-10033 yields a wrong number.",
   "settles": "A third error linked to BC-SKL-10052 with a numeric consequence."
  },
  {
   "claim": "A fluent solver writes the conditions, the evaluated term or bound and the inequality, and holds the identification of the first omitted term.",
   "settles": "Timing data per step once the fluency telemetry exists."
  },
  {
   "claim": "ex-1 tags no point type, because BC-PT-99040 and BC-PT-99041 reader lines do not fit the brief cap once the prediction and contrast pair are served; ex-2 carries BC-PT-99039 and BC-PT-99041.",
   "settles": "A brief cap that admits a reader line on ex-1."
  },
  {
   "claim": "The BC-ERR-10033 wrong step is the Lagrange form with an unstated M, the reverse choice, because the record gives no numeric consequence.",
   "settles": "A numeric consequence on the BC-ERR-10033 record."
  }
 ],
 "sources": [
  "BC-CON-10019",
  "BC-SKL-10052",
  "BC-EK-LIM-8C1",
  "BC-EK-LIM-8C2",
  "ced:197",
  "BC-QA-10008",
  "BC-QA-10009",
  "BC-PT-99039",
  "BC-PT-99040",
  "BC-PT-99041",
  "BC-ERR-10033",
  "BC-ERR-99016",
  "BC-PRQ-06005",
  "sg-22:21",
  "sg-24:21",
  "sg-26:22",
  "research/units/unit-10-infinite-sequences-series.md#10.12 Lagrange Error Bound",
  "research/question-analysis/question-archetypes.md#BC-QA-10008 Alternating series error bound compared with a tolerance",
  "research/question-analysis/question-archetypes.md#BC-QA-10009 Lagrange error bound with a supplied derivative bound",
  "research/exam/exam-structure.md#Section and part layout"
 ],
 "word_count": {
  "full": 738,
  "brief": 445
 },
 "read_minutes": {
  "full": 5.0,
  "brief": 3.0
 }
}
```
