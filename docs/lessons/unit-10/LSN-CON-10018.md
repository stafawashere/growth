---
title: LSN-CON-10018 The Lagrange error bound
research_date: 2026-09-29
status: designed
purpose: Authoring spec for the concept lesson on BC-CON-10018, the Lagrange bound on the error of a Taylor polynomial written from a supplied bound on the next derivative, evaluated and stated as an inequality, built from authoring_bundle("BC-CON-10018") and the research files it cites, so an author fills plan 15's lesson record without making a teaching decision.
---

# LSN-CON-10018 The Lagrange error bound

## Prediction

Served first, both bands: an `mcq` on ex-1's numbers. f is one half of (x - 2)^4, so its fourth derivative is 12 and its degree 3 Taylor polynomial about 2 is 0. The student picks the error at x = 5/2. Key B, 1/32, which the student gets by evaluating f at 5/2, before any rule. The distractors are 1/16 (the leading one half dropped) and 1/64. The resolution shows that the Lagrange form with M = 12 gives the same number, so the bound is attained when the fourth derivative sits at its maximum. No verdict word. Source: BC-CON-10018 and the topic 10.12 section the key idea cites.

## Orientation

Served text from BC-CON-10018 `description_plain` and the topic's Assessment behaviour paragraph (an FRQ part supplies a bound on a higher derivative on an interval and asks for the bound and the comparison with a tolerance, two points, sg-23:20). The orientation states what a response shows: the bound in its form with matching order, power and factorial, and an inequality. No count, no frequency.

## Key ideas

One core block. The three skills map one essential knowledge statement, BC-EK-LIM-8C1 (ced:197), so one key idea serves both bands. It paraphrases the Lagrange error bound paragraph (hypothesis, conclusion) and the Presentation paragraph (an error written equal to the bound does not earn the comparison point, sg-23:20). Notation line: the concept's `notation`. No anchor quote. BC-EK-LIM-8C2 belongs to BC-CON-10019.

## Recognition

BC-QA-10009 (question-archetypes.md, BC-QA-10009) is the only archetype loading the three skills.

- `common_givens`: "a bound on the next derivative over an interval", "a Taylor polynomial of stated degree about a centre", "an input near the centre", "a tolerance for the error".
- `asked_to_produce`: "the form of the Lagrange error bound", "an inequality showing the error is at most the tolerance".
- `typical_wording`: use the Lagrange error bound to show the approximation is within the stated amount of the exact value.
- Shapes: an MCQ for the form of the bound or the degree that brings the bound under a tolerance, and an FRQ part with a bound on the fifth derivative and a fourth degree approximation (topic Assessment behaviour); official examples BC-FRQ-2023-Q6-B, BC-FRQ-2025-Q5-C, BC-MCQ-CED-022.

What says this concept: a supplied bound on a derivative one order past the polynomial. What says not this concept: a series whose terms alternate and shrink, which selects the first omitted term (BC-CON-10015). The near miss of the contrast pair is that series stem, the first `wrong_approaches` entry of BC-QA-10009.

## Method choice

- st-1, BC-QA-10009, verified. Cue from `common_givens`. Method from `expected_solution_path`: identify the order, write the bound, evaluate it, present the inequality. Rival from `wrong_approaches`: the alternating series bound where Lagrange is the tool, and the wrong order or factorial. Separating feature: a supplied derivative bound. The block carries the contrast pair: a Lagrange stem of BC-QA-10009's shape beside an alternating series stem from BC-QA-10008's shape. No field opens with the reader's own label.

## Solution path

- ex-1, BC-QA-10009, both bands, no calculator. Draw: given bound, degree 3, centre 2, step 1/2, maximum 12, minimum 1 (unused in the bound form), target 5/2. M = 12, bound 12/4! times (1/2)^4 = 1/32 (SymPy). The stem matches the prediction's numbers. No published item on BC-QA-10009 carries this draw (draw_exclusion).
- ex-2, low band, faded from step 3. Draw: given endpoints, degree 2, centre 1, step 1/2, maximum 8, minimum 3, target 3/2. The derivative is positive and increasing, so M = 8 at the right end, and the bound is 8/3! times (1/2)^3 = 1/6. Steps 1 and 2 (M and the assembled form) are shown, the student writes the value, and steps 3 and 4 then reveal. The fade falls there because the order and the form repeat ex-1 and the evaluation is what the student must produce.
- Steps follow `expected_solution_path`: the order (a value only when M is read from endpoints), the form (new), the value (equivalent), the inequality sentence. A fluent solver writes the form, the value and the inequality, and holds the derivative order (Time).

## Scoring

BC-QA-10009 lists BC-PT-99039 and 99041. ex-1 tags BC-PT-99039 on the assembled form; its BC-PT-99041 tag is dropped to fit the brief cap (inferred array). ex-2 tags both, 99041 on the inequality sentence. The lines are `reader_checks` output.

Point losses from research: the error written as equal to the bound, or the conditions not stated (research/scoring/common-point-losses.md#Justification points, sg-23:20, sg-22:21); later simplification errors cost the comparison point and leave the form point (BC-QA-10009 `scoring_pattern`, sg-23:20).

## Traps

Five active errors meet the skills, in bundle order: BC-ERR-10025, BC-ERR-10032, BC-ERR-99016, BC-ERR-10026, BC-ERR-10027. The cap of 4 drops BC-ERR-10027 (the comparison with the tolerance left out; ex-1 has no tolerance). Low band all four, mid band the first two. All on ex-1's draw. BC-ERR-10025 and BC-ERR-10032 are distinct pairs (`fix_prompt` true): distance 5/2 for 1/2, factorial 3! for 4!. BC-ERR-99016 and BC-ERR-10026 are equivalent pairs (`fix_prompt` false): the value 1/32 is right and the symbol is wrong, less than and equals against at most. No possible reason lines (brief band words).

## Representations

None. The topic's Representations paragraph names BC-REP-01 and 04 and the conversions supplied bound to assembled bound, and evaluated bound to inequality chain; nothing figure-shaped.

## Prerequisite bridge

- BC-PRQ-06002, BC-PRQ-06005, BC-PRQ-10001, BC-PRQ-10002, each from its `description_plain` and `failure_signature`, in a line each.

## Time

The MCQ shape is Section I Part A, 2.14 minutes. As a free response part, 2 points, 3.33 minutes (docs/lessons/unit-10/README.md, section 5; research/exam/exam-structure.md#Section and part layout). A fluent solver writes the form, the value and the inequality, and holds the derivative order and the evaluation arithmetic [inferred]. The minutes go on the form.

## Checks

- chk-1, completion of ex-1, both bands: the form given, the value asked. Key 1/32.
- chk-2, isomorph, both bands. Draw: given bound, degree 4, centre -1, step 1/3, maximum 10, minimum 1. Key 10/(3^5 * 5!) = 1/2916.
- chk-3, MCQ, low band. Draw: given bound, degree 2, centre 3, step -1/2, maximum 6, minimum 1, target 5/2. Key 1/8. Distractors: 3/8 (factorial 2!, BC-ERR-10032), 1/4 (power 2, BC-ERR-10032), 125/8 (evaluated at the input 5/2, BC-ERR-10025).

## Delivery

- pr-1, orientation: text. Rule 6.
- ki-1: `model`, a table of the Lagrange bound against the actual error of e^x at x = 1/2 for degrees 1 to 4, the row the unit README's delivery map gives this concept (section 6). The mode table admits `model` for a concept whose meaning is the behaviour of a computed sequence of values, and rule 2 does not fire because BC-EK-LIM-8C1 states a bound, not a process. It sits on ki-1 because worked examples must be step_reveal. Each row is a SymPy computation (inferred array). The record carries no `no_figure_reason`.
- ex-1, ex-2, the four error blocks: step_reveal. Rule 1.

## Band plan

- Low (full): prediction, orientation, bridges, ki-1, st-1 with the contrast pair, ex-1 and its line, chk-1, the four error blocks, ex-2 (faded from step 3) and its lines, chk-2, chk-3. 742 words, 5.0 minutes.
- Mid (brief): prediction, orientation, bridges, ki-1, st-1 with the contrast pair, ex-1 and its line, chk-1, err-BC-ERR-10025, err-BC-ERR-10032, chk-2. 436 words, 3.0 minutes.
- Refresher: ki-1, the four error blocks, ex-1.

## Sources

- BC-CON-10018; BC-SKL-10049, BC-SKL-10050, BC-SKL-10051; BC-EK-LIM-8C1; ced:197
- BC-QA-10009; BC-PT-99039, BC-PT-99041
- BC-ERR-10025, BC-ERR-10032, BC-ERR-99016, BC-ERR-10026
- BC-PRQ-06002, BC-PRQ-06005, BC-PRQ-10001, BC-PRQ-10002
- sg-23:20, sg-22:21, sg-24:21
- research/units/unit-10-infinite-sequences-series.md#10.12 Lagrange Error Bound
- research/question-analysis/question-archetypes.md#BC-QA-10009 Lagrange error bound with a supplied derivative bound
- research/exam/exam-structure.md#Section and part layout
- [inferred] the model table, the held steps, the untagged BC-PT-99041 on ex-1, BC-ERR-10025's archetype link. Each settled as the inferred array states.

## Machine record

```json
{
 "id": "LSN-CON-10018",
 "kind": "concept",
 "target_id": "BC-CON-10018",
 "unit": "10",
 "skills": [
  "BC-SKL-10049",
  "BC-SKL-10050",
  "BC-SKL-10051"
 ],
 "prediction": {
  "id": "pr-1",
  "stem": {
   "text": "Let \\(f(x)=\\frac12(x-2)^4\\), so \\(f^{(4)}(x)=12\\), and let \\(P_3\\) be its degree 3 Taylor polynomial about \\(x=2\\). Predict \\(|f(\\tfrac52)-P_3(\\tfrac52)|\\).",
   "command_verb": "predict"
  },
  "format": "mcq",
  "options": [
   {
    "id": "A",
    "label": "\\(\\frac{1}{16}\\)",
    "is_key": false
   },
   {
    "id": "B",
    "label": "\\(\\frac{1}{32}\\)",
    "is_key": true
   },
   {
    "id": "C",
    "label": "\\(\\frac{1}{64}\\)",
    "is_key": false
   }
  ],
  "resolution": "\\(P_3=0\\), so the error is \\(f(\\tfrac52)=\\frac{1}{32}\\). The Lagrange form with \\(M=12\\) gives \\(\\frac{12}{4!}\\left(\\frac12\\right)^4=\\frac{1}{32}\\), the same number.",
  "sources": [
   "BC-CON-10018",
   "research/units/unit-10-infinite-sequences-series.md#10.12 Lagrange Error Bound"
  ]
 },
 "orientation": {
  "text": "A Taylor polynomial's error is at most a term built from a bound on the next derivative. A response writes that bound in form and states the error is at most that number.",
  "sources": [
   "BC-CON-10018",
   "research/units/unit-10-infinite-sequences-series.md#10.12 Lagrange Error Bound"
  ]
 },
 "key_ideas": [
  {
   "id": "ki-1",
   "ek_id": "BC-EK-LIM-8C1",
   "depth": "core",
   "text": "If \\(|f^{(n+1)}|\\le M\\) between \\(a\\) and \\(x\\), then \\(|f(x)-P_n(x)|\\le\\frac{M}{(n+1)!}|x-a|^{n+1}\\). Order, power and factorial all equal \\(n+1\\). The error is at most the bound, never equal to it.",
   "notation": "max of the next derivative; (n+1) factorial",
   "quote": null,
   "sources": [
    "BC-EK-LIM-8C1",
    "ced:197",
    "sg-23:20",
    "research/units/unit-10-infinite-sequences-series.md#10.12 Lagrange Error Bound"
   ]
  }
 ],
 "strategy": [
  {
   "id": "st-1",
   "archetype_id": "BC-QA-10009",
   "cue": "A bound on the next derivative and a polynomial of stated degree.",
   "method": "Name order \\(n+1\\), write the bound, evaluate, compare.",
   "rival": "The alternating series bound, or the wrong order or factorial.",
   "separating_feature": "A supplied derivative bound.",
   "sources": [
    "BC-QA-10009"
   ],
   "evidence_tag": "verified",
   "contrast": {
    "this": {
     "text": "Let \\(P_4\\) be the degree 4 Taylor polynomial of \\(f\\) about \\(x=1\\), with \\(|f^{(5)}|\\le9\\) on \\([1,\\frac43]\\). Bound \\(|f(\\tfrac43)-P_4(\\tfrac43)|\\).",
     "archetype_id": "BC-QA-10009"
    },
    "not_this": {
     "text": "Let \\(S_2\\) be a partial sum of \\(\\sum_{n=0}^{\\infty}\\frac{(-1)^n}{n!\\,2^n}\\). Bound \\(|S-S_2|\\).",
     "why_not": "Its terms alternate and shrink, so the first omitted term bounds the error."
    },
    "feature": "A supplied derivative bound, against alternating shrinking terms."
   }
  }
 ],
 "worked_examples": [
  {
   "id": "ex-1",
   "archetype_id": "BC-QA-10009",
   "bands": [
    "low",
    "mid"
   ],
   "parameter_draw": {
    "given": "bound",
    "degree": 3,
    "centre": 2,
    "step": "1/2",
    "maximum": 12,
    "minimum": 1
   },
   "problem": {
    "text": "Let \\(P_3\\) be the Taylor polynomial of degree 3 for \\(f\\) about \\(x=2\\). For all \\(x\\) in \\([2,\\frac52]\\), \\(|f^{(4)}(x)|\\le12\\). Find an upper bound for \\(|f(\\tfrac52)-P_3(\\tfrac52)|\\).",
    "command_verb": "find"
   },
   "calculator_status": "no_calculator",
   "steps": [
    {
     "cue": "Degree 3 needs the fourth derivative.",
     "why": "One order past the polynomial, so \\(M=12\\)."
    },
    {
     "cue": "Assemble \\(M\\), distance, factorial.",
     "why": "Power and factorial are both 4.",
     "expr": "12*Abs(5/2 - 2)**4/factorial(4)",
     "relation": "new",
     "point_type_id": "BC-PT-99039"
    },
    {
     "cue": "The distance is \\(\\frac12\\).",
     "why": "Evaluate.",
     "expr": "1/32",
     "relation": "equivalent"
    },
    {
     "cue": "State the inequality.",
     "why": "The error is at most the bound."
    }
   ],
   "answer": {
    "form": "numeric",
    "expr": "1/32"
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
    "given": "endpoints",
    "degree": 2,
    "centre": 1,
    "step": "1/2",
    "maximum": 8,
    "minimum": 3
   },
   "problem": {
    "text": "Let \\(P_2\\) be the Taylor polynomial of degree 2 for \\(f\\) about \\(x=1\\). On \\([1,\\frac32]\\), \\(f'''\\) is positive and increasing, with \\(f'''(1)=3\\) and \\(f'''(\\tfrac32)=8\\). Find an upper bound for \\(|f(\\tfrac32)-P_2(\\tfrac32)|\\).",
    "command_verb": "find"
   },
   "calculator_status": "no_calculator",
   "steps": [
    {
     "cue": "Increasing \\(f'''\\) peaks at the right end.",
     "why": "So \\(M=8\\).",
     "expr": "8",
     "relation": "new"
    },
    {
     "cue": "Degree 2 needs the third derivative.",
     "why": "Power and factorial are both 3.",
     "expr": "8*Abs(3/2 - 1)**3/factorial(3)",
     "relation": "new",
     "point_type_id": "BC-PT-99039"
    },
    {
     "cue": "The distance is \\(\\frac12\\).",
     "why": "Evaluate.",
     "expr": "1/6",
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
    "expr": "1/6"
   }
  }
 ],
 "what_a_reader_scores": [
  {
   "example_id": "ex-1",
   "point_type_ids": [
    "BC-PT-99039"
   ],
   "lines": [
    {
     "point_type_id": "BC-PT-99039",
     "text": "Lagrange error bound form. Earned by: The bound written as the maximum of the next derivative over the interval, divided by the factorial, times the distance raised to the matching power, or its evaluated form (sg-25:22, sg-23:20). Not earned by: A bound with the wrong factorial or the wrong power of the distance (sg-23:20)."
    }
   ]
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
   "error_id": "BC-ERR-10025",
   "observed_behavior": "The response identifies the correct omitted term but substitutes the index, the centre, or another value in place of the stated input.",
   "scoring_consequence": "The point attached to using the term correctly is lost (sg-22:21).",
   "wrong_step": {
    "text": "Distance \\(\\frac52\\).",
    "expr": "12*(5/2)**4/factorial(4)"
   },
   "right_step": {
    "text": "Distance \\(\\frac12\\).",
    "expr": "12*Abs(5/2 - 2)**4/factorial(4)"
   },
   "relation": "distinct",
   "fix_prompt": true,
   "possible_reason": null,
   "sources": [
    "BC-ERR-10025"
   ]
  },
  {
   "error_id": "BC-ERR-10032",
   "observed_behavior": "The response writes the bound without the maximum of the next derivative, with the wrong power of the difference, or with the wrong factorial.",
   "scoring_consequence": "The form point is lost, and with it the comparison point that depends on it (sg-23:20).",
   "wrong_step": {
    "text": "Factorial \\(3!\\).",
    "expr": "12*Abs(5/2 - 2)**4/factorial(3)"
   },
   "right_step": {
    "text": "Factorial \\(4!\\).",
    "expr": "12*Abs(5/2 - 2)**4/factorial(4)"
   },
   "relation": "distinct",
   "fix_prompt": true,
   "possible_reason": null,
   "sources": [
    "BC-ERR-10032"
   ]
  },
  {
   "error_id": "BC-ERR-99016",
   "observed_behavior": "Responses invoke an error bound without confirming that the series alternates with terms decreasing to zero, reach for the Lagrange bound where the alternating series bound applies, or write the error as equal to or strictly less than the bound instead of at most the bound.",
   "scoring_consequence": "The condition or analysis point is lost even when the numerical bound is computed correctly.",
   "wrong_step": {
    "text": "Error \\(<\\frac{1}{32}\\).",
    "expr": "1/32"
   },
   "right_step": {
    "text": "Error \\(\\le\\frac{1}{32}\\).",
    "expr": "1/32"
   },
   "relation": "equivalent",
   "fix_prompt": false,
   "possible_reason": null,
   "sources": [
    "BC-ERR-99016"
   ]
  },
  {
   "error_id": "BC-ERR-10026",
   "observed_behavior": "The response presents the error as equal to the bounding expression rather than at most that expression.",
   "scoring_consequence": "A statement of equality does not earn the justification point in either bound (sg-22:21, sg-23:20, sg-24:21).",
   "wrong_step": {
    "text": "Error \\(=\\frac{1}{32}\\).",
    "expr": "1/32"
   },
   "right_step": {
    "text": "Error \\(\\le\\frac{1}{32}\\).",
    "expr": "1/32"
   },
   "relation": "equivalent",
   "fix_prompt": false,
   "possible_reason": null,
   "sources": [
    "BC-ERR-10026"
   ]
  }
 ],
 "representations": null,
 "prerequisite_bridges": [
  {
   "prq_id": "BC-PRQ-06002",
   "text": "Powers of a fraction, written out."
  },
  {
   "prq_id": "BC-PRQ-06005",
   "text": "The bound is on \\(f^{(n+1)}\\), not \\(f\\)."
  },
  {
   "prq_id": "BC-PRQ-10001",
   "text": "Distance is \\(|x-a|\\)."
  },
  {
   "prq_id": "BC-PRQ-10002",
   "text": "Keep the factorial: \\(4!=24\\)."
  }
 ],
 "time": {
  "exam_part": "I-A",
  "budget_minutes": 2.14,
  "source": "research/exam/exam-structure.md#Section and part layout",
  "written_steps": {
   "ex-1": [
    2,
    3,
    4
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
   "archetype_id": "BC-QA-10009",
   "parameter_draw": {
    "given": "bound",
    "degree": 3,
    "centre": 2,
    "step": "1/2",
    "maximum": 12,
    "minimum": 1
   },
   "completes": "ex-1",
   "stem": {
    "text": "The bound is \\(\\frac{12}{4!}\\left|\\frac52-2\\right|^4\\). Evaluate it to give the upper bound.",
    "command_verb": "write"
   },
   "key": {
    "form": "numeric",
    "expr": "1/32"
   },
   "steps": [
    {
     "text": "Form.",
     "expr": "12*Abs(5/2 - 2)**4/factorial(4)",
     "relation": "new"
    },
    {
     "text": "Evaluate.",
     "expr": "1/32",
     "relation": "equivalent"
    }
   ],
   "calculator_status": "no_calculator",
   "skills": [
    "BC-SKL-10051"
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
   "archetype_id": "BC-QA-10009",
   "parameter_draw": {
    "given": "bound",
    "degree": 4,
    "centre": -1,
    "step": "1/3",
    "maximum": 10,
    "minimum": 1
   },
   "stem": {
    "text": "Let \\(P_4\\) be the degree 4 Taylor polynomial of \\(f\\) about \\(x=-1\\). On \\([-1,-\\frac23]\\), \\(|f^{(5)}(x)|\\le10\\). Find an upper bound for \\(|f(-\\tfrac23)-P_4(-\\tfrac23)|\\).",
    "command_verb": "find"
   },
   "key": {
    "form": "numeric",
    "expr": "1/2916"
   },
   "steps": [
    {
     "text": "Form.",
     "expr": "10*Abs(-2/3 - (-1))**5/factorial(5)",
     "relation": "new"
    },
    {
     "text": "Evaluate.",
     "expr": "1/2916",
     "relation": "equivalent"
    }
   ],
   "calculator_status": "no_calculator",
   "skills": [
    "BC-SKL-10050"
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
    "given": "bound",
    "degree": 2,
    "centre": 3,
    "step": "-1/2",
    "maximum": 6,
    "minimum": 1
   },
   "stem": {
    "text": "Let \\(P_2\\) be the Taylor polynomial of degree 2 for \\(f\\) about \\(x=3\\). On \\([\\frac52,3]\\), \\(|f'''(x)|\\le6\\). An upper bound for \\(|f(\\tfrac52)-P_2(\\tfrac52)|\\) is",
    "command_verb": "identify"
   },
   "key": {
    "form": "numeric",
    "expr": "1/8"
   },
   "steps": [
    {
     "text": "Form.",
     "expr": "6*Abs(5/2 - 3)**3/factorial(3)",
     "relation": "new"
    },
    {
     "text": "Evaluate.",
     "expr": "1/8",
     "relation": "equivalent"
    }
   ],
   "options": [
    {
     "id": "A",
     "is_key": false,
     "expr": "3/8",
     "error_path": "BC-ERR-10032",
     "derivation": "the factorial taken as 2! instead of 3!"
    },
    {
     "id": "B",
     "is_key": true,
     "expr": "1/8",
     "error_path": null
    },
    {
     "id": "C",
     "is_key": false,
     "expr": "1/4",
     "error_path": "BC-ERR-10032",
     "derivation": "the power of the distance taken as 2 instead of 3"
    },
    {
     "id": "D",
     "is_key": false,
     "expr": "125/8",
     "error_path": "BC-ERR-10025",
     "derivation": "the bound evaluated at the input 5/2 instead of at its distance 1/2 from the centre"
    }
   ],
   "calculator_status": "no_calculator",
   "skills": [
    "BC-SKL-10050"
   ]
  }
 ],
 "delivery": [
  {
   "block": "pr-1",
   "mode": "text",
   "reason": "rule 6: a question on ex-1's own numbers",
   "sources": [
    "BC-CON-10018"
   ]
  },
  {
   "block": "orientation",
   "mode": "text",
   "reason": "rule 6: a statement of what a response shows",
   "sources": [
    "BC-CON-10018"
   ]
  },
  {
   "block": "ki-1",
   "mode": "model",
   "reason": "mode table: the bound above the actual error at growing degree is the behaviour of a computed sequence of values (unit README, section 6, the LSN-CON-10018 row); rule 2 does not fire because BC-EK-LIM-8C1 states a bound, not a process [inferred]",
   "sources": [
    "BC-SKL-10049",
    "BC-SKL-10050",
    "BC-SKL-10051"
   ],
   "spec": {
    "kind": "table",
    "representations": [
     "BC-REP-01"
    ],
    "experiment": "f(x)=e^x about x=0 at x=1/2 with |f^(n+1)| <= 2 on [0,1/2], degrees n=1 to 4",
    "columns": [
     {
      "text": "degree n",
      "placement": "inside"
     },
     {
      "text": "Lagrange bound",
      "placement": "inside"
     },
     {
      "text": "actual error",
      "placement": "inside"
     }
    ],
    "rows": [
     {
      "degree": 1,
      "bound": "1/4",
      "actual_error": "0.148721",
      "bound_decimal": "0.25"
     },
     {
      "degree": 2,
      "bound": "1/24",
      "actual_error": "0.023721",
      "bound_decimal": "0.041667"
     },
     {
      "degree": 3,
      "bound": "1/192",
      "actual_error": "0.002888",
      "bound_decimal": "0.005208"
     },
     {
      "degree": 4,
      "bound": "1/1920",
      "actual_error": "0.000284",
      "bound_decimal": "0.000521"
     }
    ]
   },
   "fallback": "the same four rows as a static table",
   "keyboard": "none needed: the table has no control"
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
   "block": "err-BC-ERR-10025",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  },
  {
   "block": "err-BC-ERR-10032",
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
   "block": "err-BC-ERR-10026",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  }
 ],
 "refresher": [
  "ki-1",
  "err-BC-ERR-10025",
  "err-BC-ERR-10032",
  "err-BC-ERR-99016",
  "err-BC-ERR-10026",
  "ex-1"
 ],
 "research_lines": [
  {
   "file": "research/units/unit-10-infinite-sequences-series.md",
   "line": "The form of the bound and the final comparison are scored separately"
  }
 ],
 "inferred": [
  {
   "claim": "The model table on ki-1 is delivered as a model, and its rows are a SymPy computation of the Lagrange bound and the actual error of e^x at x=1/2, an experiment no skill or archetype supplies.",
   "settles": "The modality A/B in the build plan."
  },
  {
   "claim": "A fluent solver writes the assembled form, its value and the inequality, and holds the derivative order.",
   "settles": "Timing data per step once the fluency telemetry exists."
  },
  {
   "claim": "ex-1 tags BC-PT-99039 only; its BC-PT-99041 tag is dropped from ex-1 to fit the brief cap, and ex-2 carries both.",
   "settles": "A brief cap that admits a second reader line."
  },
  {
   "claim": "BC-ERR-10025 is held by BC-SKL-10050 but recorded against BC-QA-10008, and is shown here as the bound evaluated at the input.",
   "settles": "Linking BC-ERR-10025 to BC-QA-10009 in the library."
  }
 ],
 "sources": [
  "BC-CON-10018",
  "BC-SKL-10049",
  "BC-SKL-10050",
  "BC-SKL-10051",
  "BC-EK-LIM-8C1",
  "ced:197",
  "BC-QA-10009",
  "BC-PT-99039",
  "BC-PT-99041",
  "BC-ERR-10025",
  "BC-ERR-10032",
  "BC-ERR-99016",
  "BC-ERR-10026",
  "BC-PRQ-06002",
  "BC-PRQ-06005",
  "BC-PRQ-10001",
  "BC-PRQ-10002",
  "sg-23:20",
  "sg-22:21",
  "sg-24:21",
  "research/units/unit-10-infinite-sequences-series.md#10.12 Lagrange Error Bound",
  "research/question-analysis/question-archetypes.md#BC-QA-10009 Lagrange error bound with a supplied derivative bound",
  "research/exam/exam-structure.md#Section and part layout"
 ],
 "word_count": {
  "full": 742,
  "brief": 436
 },
 "read_minutes": {
  "full": 5.0,
  "brief": 3.0
 }
}
```
