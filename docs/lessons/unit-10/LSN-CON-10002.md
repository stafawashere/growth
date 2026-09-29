---
title: LSN-CON-10002 Convergence of a series as a limit of its partial sums
research_date: 2026-09-29
status: designed
purpose: Authoring spec for the concept lesson on BC-CON-10002, a series converging exactly when the limit of its partial sums exists, with that limit as its sum, built from authoring_bundle("BC-CON-10002") and the research files it cites, so an author fills plan 15's lesson record without making a teaching decision.
---

# LSN-CON-10002 Convergence of a series as a limit of its partial sums

Concept BC-CON-10002 (skills BC-SKL-10003, BC-SKL-10004, BC-SKL-10005), topic 10.1 of Unit 10, BC only (ced:186). Hard parent BC-CON-10001, so S_n as a sum of terms is assumed (docs/lessons/unit-10/README.md, section 1). BC-CON-10002 is a productive-failure target through BC-QA-10021, which the README says is served as an opener before convergence tests are taught.

## Prediction

Served first, both bands: a `short_answer` on ex-1's own numbers. The partial sums 2, 2.5, 2.75, 2.875 and the formula 3 - 2(1/2)^n are given; the question is the number they settle on. Key 3, which equals ex-1's answer, so the blind re-solve covers it. The four values settle it before any rule is stated: each step halves the gap to 3. The resolution states that the power tends to 0 and that a series has sum S when its partial sums approach S, with no verdict. This also serves as the productive-failure opener the README asks for on this concept. Source: BC-CON-10002 and the topic 10.1 section.

## Orientation

Served text, from BC-CON-10002 `description_plain` ("A series converges when its running totals settle on a single number") and the topic's Assessment behaviour paragraph (research/units/unit-10-infinite-sequences-series.md#10.1 Defining Convergent and Divergent Infinite Series): MCQ forms give a closed form for S_n and ask for the sum, and a free response conclusion must name which series it is about. The orientation states what a response shows: S_n, its limit, and the limit reported as the sum or the divergence. No count, no frequency.

## Key ideas

- ki-1 (core), BC-EK-LIM-7A2 (ced:186), loaded by BC-SKL-10003, 10004 and 10005. Paraphrase of the Required mathematical knowledge paragraph Convergence (hypothesis: S_n has a limit S; conclusion: the series converges with sum S; otherwise it diverges), with the limit of the terms set apart as a different limit (BC-ERR-10001). No anchor quote, since the brief band has no words to spare. Notation line: the concept's `notation`. Delivery is motion (Delivery).
- ki-2 (extended), BC-EK-LIM-7A1 (ced:186), loaded by BC-SKL-10004 and 10005. The partial sum definition restated and the telescoping cancellation of BC-SKL-10004 ("Cancel the interior terms of the running total and take the limit of what is left"). Low band only.

## Recognition

BC-QA-10021 (family series-value; `common_givens` "a formula for the nth partial sum", "or an unsplit telescoping term"; `typical_wording` "the series converges; find its sum") loads all three skills; BC-QA-10001 loads BC-SKL-10005. Shapes: an MCQ that gives a closed form for S_n and asks for the sum; an MCQ that gives a general term and asks which of a sequence and a series converges; a free response part where the conclusion names the series (topic Assessment behaviour). What says this concept: S_n given or writable, and a request for the sum or for convergence. What says not this concept: the request is about a list, the word sequence, or the limit of a_n (BC-SKL-10001, LSN-CON-10001).

The near miss of the contrast pair is the same fraction 7n+1 over 2n+5 read as the general term of a sequence, from BC-QA-10001 and its wrong approach "reporting the limit of the general term as the behaviour of the series": it has limit 7/2 as a sequence, and 7/2 is not a sum.

## Method choice

- st-1, BC-QA-10021. Cue from `common_givens`. Method, `expected_solution_path[1]` "take its limit as n increases", the sum being that limit (`expected_solution_path[2]`). Rival, `wrong_approaches` "taking the limit of the general term as the value of the series". Separating feature: the sum is the limit of the totals, not of the terms. Both cue fields exist, so the block is verified. It carries the contrast pair, given S_n beside given a_n on the same fraction.
- st-2, BC-QA-10001. Cue from `common_givens`. Method, `expected_solution_path[0]` "read the general term", then naming the object, which is BC-SKL-10005. Rival, `wrong_approaches` "reporting the limit of the general term as the behaviour of the series". Low band only. No served field opens with the reader's own label.

## Solution path

- ex-1, BC-QA-10021, both bands, no calculator. Draw: family exponential, lead 3, shift 1, rate 1, offset 2, ratio 1/2, numerator 3, start 0. S_n = 3 - 2(1/2)^n, sum 3. No published item on BC-QA-10021 carries this draw (content/items_gen_unit10, ITM-GEN-10021-22 to 43).
- ex-2, low band, BC-QA-10021. Draw: family telescoping, lead 2, shift 1, rate 1, offset 3, ratio 1/3, numerator 4, start 2. Series the sum from n = 1 of 4/((n+2)(n+3)), S_n = 4/3 - 4/(n+3), sum 4/3. No published item on BC-QA-10021 carries this draw.
- ex-2 is faded from step 4: steps 1 to 3 (the plan, the general term, the split) are shown, the student writes S_n and the sum, and steps 4 and 5 then reveal. The fade falls there because the split repeats a pattern of LSN-CON-10001 and the new demand is S_n and its limit.
- Steps: ex-1 the given S_n (new) and its limit (limit); ex-2 the general term (new), the split (equivalent), S_n (new, because the checker does not evaluate a sum with a symbolic upper limit) and its limit (limit). A fluent solver writes S_n and the limit; the statement that the sum is the limit of the partial sums is held (Time).
- Productive-failure comparison: the prediction is the opener, attempted before the rule; the model table on the representations block is the comparison the student reads afterwards (BC-CON-10002 is in `PRODUCTIVE_FAILURE_TARGETS`, docs/lessons/unit-10/README.md, section 6).

## Scoring

None. BC-QA-10021 lists no `point_types` and its `scoring_pattern` reads "No scoring guideline scores an opener; the answer is checked as a value", so the lesson says nothing about points and carries no scoring lines (plan 15, R14).

## Traps

Three errors meet the skills, in bundle order: BC-ERR-10001, BC-ERR-10003, BC-ERR-99038. All on ex-1's draw and all distinct, so all three carry `fix_prompt` true. Low band all three, mid band the first two. No block carries a possible reason line, to keep the brief band under its cap; the record links BC-MIS-10001 and BC-MIS-10005 to BC-ERR-10001, BC-MIS-10001 to BC-ERR-10003, and BC-MIS-10002 to BC-ERR-99038 (the last is used in the low band).

- err-BC-ERR-10001: 0, the limit of a_n, against 3, the limit of S_n.
- err-BC-ERR-10003: the sentence names no series; the SymPy pair is the empty set against the set holding the sum, 3.
- err-BC-ERR-99038: S_4 = 2.875 as the sum against 3. Possible reason, BC-MIS-10002.

## Representations

One block, low band, mode model (the README delivery map for this concept). A table of partial sums at n = 1, 2, 3, 5, 10, 50 for three series, an exponential, a rational and a telescoping S_n, each closing on one number: 3 - 2(1/2)^n, (2n+1)/(n+3) and 1 - 1/(n+1). Their limits are 3, 2 and 1, so no column equals the answer of ex-2 (4/3), chk-2 (5/3) or chk-3 (3). ex-1's column repeats the prediction's series by design. The topic's Representations paragraph names BC-REP-10, 11, 01 and 04; the table is the numeric experiment of the mode table, not a representation the stem carries.

## Prerequisite bridge

- BC-PRQ-06005, BC-PRQ-10003, BC-PRQ-10004, BC-PRQ-10008, each from its `description_plain` and `failure_signature`.

## Time

Every Unit 10 archetype is `no_calculator`; its MCQ shape is Section I Part A, 2.14 minutes (research/exam/exam-structure.md#Section and part layout). BC-QA-10021 is an opener with no exam part, so the Part A figure is the only budget. A fluent solver writes S_n and the limit, and holds the definition [inferred]. The minutes go on the cancellation in a telescoping S_n.

## Checks

- chk-1, completion of ex-1, both bands: S_n and the vanishing power given, the sum asked. Key 3.
- chk-2, isomorph, both bands. Draw BC-QA-10021: family rational, lead 5, shift 2, rate 3, offset 4, ratio 1/2, numerator 1, start 0. S_n = (5n+2)/(3n+4), key 5/3. The constraints hold: gcd(5, 3) = 1 and 0, 5/3, S_1 = 1, S_2 = 6/5 are distinct.
- chk-3, MCQ, low band. Draw BC-QA-10021: family telescoping, lead 9, shift 0, rate 4, offset 6, ratio 3/4, numerator 6, start 1. Sum of 6/((n+1)(n+2)), S_n = 3 - 6/(n+2). Key 3. Distractors: 0, the limit of the terms (BC-ERR-10001); 1, S_1 (BC-ERR-99038); 3/2, S_2 (BC-ERR-99038). BC-ERR-10003 has no natural distractor, since it concerns a sentence and not a value; two distractors share BC-ERR-99038, the archetype's own first and second partial sum distractors.

## Delivery

- pr-1, orientation, ki-2: text. Rule 6.
- ki-1: motion. Rule 2: the key idea describes a limit being taken and terms accumulating. The spec is the partial sums of ex-1 as points on a number line, S_1 = 2, S_2 = 2.5, S_4 = 2.875, and the level 3, stepped by n. It is the process's own picture and not a representation the stem carries, and the README delivery map names it. Fallback three static frames, keyboard arrow keys, reduced motion by cross-fade.
- representations: model. The mode table names productive-failure targets and a concept whose meaning is the behaviour of a computed sequence of values.
- ex-1, ex-2, the three error blocks: step_reveal. Rule 1.
- All non-text choices are [inferred], settled by the modality A/B.

## Band plan

- Low (full): prediction, orientation, bridges, ki-1, ki-2, st-1 with the contrast pair, st-2, ex-1, chk-1, the three error blocks, ex-2 (faded from step 4), chk-2, representations, chk-3. 642 words, 4.3 minutes.
- Mid (brief): prediction, orientation, bridges, ki-1, st-1 with the contrast pair, ex-1, chk-1, err-BC-ERR-10001, err-BC-ERR-10003, chk-2. 411 words, 2.8 minutes.
- Refresher: ki-1, the three error blocks, ex-1.

## Sources

- BC-CON-10002; BC-SKL-10003, BC-SKL-10004, BC-SKL-10005; BC-EK-LIM-7A1, BC-EK-LIM-7A2; ced:186
- BC-QA-10001, BC-QA-10021
- BC-ERR-10001, BC-ERR-10003, BC-ERR-99038; BC-MIS-10002
- BC-PRQ-06005, BC-PRQ-10003, BC-PRQ-10004, BC-PRQ-10008
- research/units/unit-10-infinite-sequences-series.md#10.1 Defining Convergent and Divergent Infinite Series
- research/question-analysis/question-archetypes.md#BC-QA-10021 Sum of a series found from its partial sums before any test is taught
- research/question-analysis/question-archetypes.md#BC-QA-10001 Selecting a convergence test for a given series
- research/exam/exam-structure.md#Section and part layout
- [inferred] The held steps, the prediction form, every non-text delivery choice, and the model table's series. Each settled as the inferred array states.

## Machine record

```json
{
 "id": "LSN-CON-10002",
 "kind": "concept",
 "target_id": "BC-CON-10002",
 "unit": "10",
 "skills": [
  "BC-SKL-10003",
  "BC-SKL-10004",
  "BC-SKL-10005"
 ],
 "prediction": {
  "id": "pr-1",
  "stem": {
   "text": "Predict. A series has partial sums \\(S_1=2,\\ S_2=2.5,\\ S_3=2.75,\\ S_4=2.875\\), and so on, given by \\(S_n=3-2\\left(\\frac12\\right)^n\\). What number do the partial sums settle on as \\(n\\) grows?",
   "command_verb": "predict"
  },
  "format": "short_answer",
  "key": {
   "form": "numeric",
   "expr": "3"
  },
  "resolution": "\\(\\left(\\frac12\\right)^n\\to0\\), so \\(S_n\\to3\\). A series has sum \\(S\\) when its partial sums approach \\(S\\).",
  "sources": [
   "BC-CON-10002",
   "research/units/unit-10-infinite-sequences-series.md#10.1 Defining Convergent and Divergent Infinite Series"
  ]
 },
 "orientation": {
  "text": "A series converges when its partial sums \\(S_n\\) settle on one number. A response writes \\(S_n\\), takes its limit as \\(n\\to\\infty\\), and reports that limit as the sum, or says the limit does not exist and the series diverges.",
  "sources": [
   "BC-CON-10002",
   "research/units/unit-10-infinite-sequences-series.md#10.1 Defining Convergent and Divergent Infinite Series"
  ]
 },
 "key_ideas": [
  {
   "id": "ki-1",
   "ek_id": "BC-EK-LIM-7A2",
   "depth": "core",
   "text": "The series converges to \\(S\\) exactly when \\(\\lim_{n\\to\\infty}S_n=S\\), and \\(S\\) is its sum. If that limit does not exist, the series diverges. The limit of the terms \\(a_n\\) is a different limit and does not give the sum.",
   "notation": "limit of \\(S_n\\); sum equals \\(S\\)",
   "quote": null,
   "sources": [
    "BC-EK-LIM-7A2",
    "ced:186",
    "research/units/unit-10-infinite-sequences-series.md#10.1 Defining Convergent and Divergent Infinite Series"
   ]
  },
  {
   "id": "ki-2",
   "ek_id": "BC-EK-LIM-7A1",
   "depth": "extended",
   "text": "Partial sums come first: \\(S_n=a_1+\\cdots+a_n\\). For a telescoping series, split each term into two fractions and cancel the middle terms of \\(S_n\\) before taking the limit.",
   "notation": "\\(S_n=a_1+a_2+\\cdots+a_n\\)",
   "quote": null,
   "sources": [
    "BC-EK-LIM-7A1",
    "ced:186",
    "research/units/unit-10-infinite-sequences-series.md#10.1 Defining Convergent and Divergent Infinite Series"
   ]
  }
 ],
 "strategy": [
  {
   "id": "st-1",
   "archetype_id": "BC-QA-10021",
   "cue": "A formula for \\(S_n\\), or a term that splits into two fractions.",
   "method": "Take \\(\\lim_{n\\to\\infty}S_n\\) and report it as the sum.",
   "rival": "Taking the limit of the general term as the value of the series.",
   "separating_feature": "The sum is the limit of the totals, not of the terms.",
   "sources": [
    "BC-QA-10021"
   ],
   "evidence_tag": "verified",
   "contrast": {
    "this": {
     "text": "\\(S_n=\\frac{7n+1}{2n+5}\\) for \\(\\sum a_n\\), which converges. Find its sum.",
     "archetype_id": "BC-QA-10021"
    },
    "not_this": {
     "text": "For \\(a_n=\\frac{7n+1}{2n+5}\\), find \\(\\lim_{n\\to\\infty}a_n\\).",
     "why_not": "It asks for the limit of the terms, which is not the sum."
    },
    "feature": "Given \\(S_n\\), its limit is the sum. Given \\(a_n\\), its limit is not."
   }
  },
  {
   "id": "st-2",
   "archetype_id": "BC-QA-10001",
   "cue": "A general term, with the words sequence or series.",
   "method": "Name the object first, the list \\(a_n\\) or the totals \\(S_n\\), then take its limit.",
   "rival": "Reporting the limit of the general term as the behaviour of the series.",
   "separating_feature": "The word sequence points to \\(a_n\\); a sigma with the word series points to \\(S_n\\).",
   "sources": [
    "BC-QA-10001"
   ],
   "evidence_tag": "verified"
  }
 ],
 "worked_examples": [
  {
   "id": "ex-1",
   "archetype_id": "BC-QA-10021",
   "bands": [
    "low",
    "mid"
   ],
   "parameter_draw": {
    "family": "exponential",
    "lead": 3,
    "shift": 1,
    "rate": 1,
    "offset": 2,
    "ratio": "1/2",
    "numerator": 3,
    "start": 0
   },
   "problem": {
    "text": "The nth partial sum of \\(\\sum a_n\\) is \\(S_n=3-2\\left(\\frac12\\right)^n\\). The series converges. Find its sum.",
    "command_verb": "find"
   },
   "calculator_status": "no_calculator",
   "steps": [
    {
     "cue": "The stem gives \\(S_n\\), not the terms.",
     "why": "The sum is the limit of the partial sums."
    },
    {
     "cue": "Write \\(S_n\\).",
     "why": "This is the sequence whose limit matters.",
     "expr": "3 - 2*(1/2)**n",
     "relation": "new"
    },
    {
     "cue": "Let \\(n\\to\\infty\\).",
     "why": "\\(\\left(\\frac12\\right)^n\\to0\\), so only 3 remains.",
     "expr": "3",
     "relation": "limit",
     "variable": "n",
     "point": "oo"
    }
   ],
   "answer": {
    "form": "numeric",
    "expr": "3"
   }
  },
  {
   "id": "ex-2",
   "archetype_id": "BC-QA-10021",
   "bands": [
    "low"
   ],
   "fade_from": 4,
   "parameter_draw": {
    "family": "telescoping",
    "lead": 2,
    "shift": 1,
    "rate": 1,
    "offset": 3,
    "ratio": "1/3",
    "numerator": 4,
    "start": 2
   },
   "problem": {
    "text": "The series \\(\\sum_{n=1}^{\\infty}\\frac{4}{(n+2)(n+3)}\\) converges. Find its sum.",
    "command_verb": "find"
   },
   "calculator_status": "no_calculator",
   "steps": [
    {
     "cue": "Only the terms are given.",
     "why": "So \\(S_n\\) must be written first."
    },
    {
     "cue": "Read the general term.",
     "why": "It is the piece each total adds.",
     "expr": "4/((n+2)*(n+3))",
     "relation": "new"
    },
    {
     "cue": "Split into two fractions.",
     "why": "Neighbouring terms will cancel.",
     "expr": "4/(n+2) - 4/(n+3)",
     "relation": "equivalent"
    },
    {
     "cue": "Add the first \\(n\\) terms.",
     "why": "Only \\(\\frac43\\) and \\(-\\frac{4}{n+3}\\) remain.",
     "expr": "4/3 - 4/(n+3)",
     "relation": "new"
    },
    {
     "cue": "Let \\(n\\to\\infty\\).",
     "why": "\\(\\frac{4}{n+3}\\to0\\), so the sum is \\(\\frac43\\).",
     "expr": "4/3",
     "relation": "limit",
     "variable": "n",
     "point": "oo"
    }
   ],
   "answer": {
    "form": "numeric",
    "expr": "4/3"
   }
  }
 ],
 "what_a_reader_scores": [],
 "common_errors": [
  {
   "error_id": "BC-ERR-10001",
   "observed_behavior": "The response evaluates the limit of the general term, finds a number, and reports that number as the value or the behaviour of the series.",
   "scoring_consequence": "The conclusion is about the wrong object, so no point tied to the series is earned.",
   "wrong_step": {
    "text": "\\(a_n\\to0\\), so the sum is 0.",
    "expr": "0"
   },
   "right_step": {
    "text": "\\(S_n\\to3\\), so the sum is 3.",
    "expr": "3"
   },
   "relation": "distinct",
   "fix_prompt": true,
   "possible_reason": null,
   "sources": [
    "BC-ERR-10001"
   ]
  },
  {
   "error_id": "BC-ERR-10003",
   "observed_behavior": "With several series present in one part, the response concludes that the series converges without identifying which one.",
   "scoring_consequence": "The explanation point is not earned, because the reader cannot tell which series the claim is about (sg-21:23).",
   "wrong_step": {
    "text": "The series converges.",
    "expr": "EmptySet"
   },
   "right_step": {
    "text": "The series with \\(S_n=3-2\\left(\\frac12\\right)^n\\) converges to 3.",
    "expr": "FiniteSet(3)"
   },
   "relation": "distinct",
   "fix_prompt": true,
   "possible_reason": null,
   "sources": [
    "BC-ERR-10003"
   ]
  },
  {
   "error_id": "BC-ERR-99038",
   "observed_behavior": "Responses asked for the value of a convergent series add the first few terms and present that total, or recognise the series as geometric but cannot identify the common ratio, instead of summing it in closed form.",
   "scoring_consequence": "The value point is not earned, since a decimal approximation is not the requested exact value.",
   "wrong_step": {
    "text": "\\(S_4=2.875\\) is the sum.",
    "expr": "2.875"
   },
   "right_step": {
    "text": "The sum is \\(\\lim_{n\\to\\infty}S_n=3\\).",
    "expr": "3"
   },
   "relation": "distinct",
   "fix_prompt": true,
   "possible_reason": {
    "misconception_id": "BC-MIS-10002",
    "text": "treats the total of the first few terms as the value of the infinite series"
   },
   "sources": [
    "BC-ERR-99038",
    "BC-MIS-10002"
   ]
  }
 ],
 "representations": {
  "text": "Partial sums at growing \\(n\\) for three series. Each column closes on one number.",
  "figure": {
   "kind": "numeric_experiment",
   "representations": [
    "BC-REP-03"
   ],
   "columns": [
    "n",
    "3 - 2(1/2)^n",
    "(2n+1)/(n+3)",
    "1 - 1/(n+1)"
   ],
   "n_values": [
    1,
    2,
    3,
    5,
    10,
    50
   ],
   "labels": [
    {
     "text": "partial sums S_n",
     "placement": "inside",
     "at": "column headers"
    }
   ]
  }
 },
 "prerequisite_bridges": [
  {
   "prq_id": "BC-PRQ-06005",
   "text": "Read \\(S_n\\) as a function of \\(n\\)."
  },
  {
   "prq_id": "BC-PRQ-10003",
   "text": "A sum keeps its value when its index is shifted."
  },
  {
   "prq_id": "BC-PRQ-10004",
   "text": "Limits of quotients in \\(n\\) compare leading terms."
  },
  {
   "prq_id": "BC-PRQ-10008",
   "text": "The general term is read at each index."
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
   "archetype_id": "BC-QA-10021",
   "parameter_draw": {
    "family": "exponential",
    "lead": 3,
    "shift": 1,
    "rate": 1,
    "offset": 2,
    "ratio": "1/2",
    "numerator": 3,
    "start": 0
   },
   "completes": "ex-1",
   "stem": {
    "text": "\\(S_n=3-2\\left(\\frac12\\right)^n\\) and \\(\\left(\\frac12\\right)^n\\to0\\). Find the sum of the series.",
    "command_verb": "find"
   },
   "key": {
    "form": "numeric",
    "expr": "3"
   },
   "steps": [
    {
     "text": "S_n.",
     "expr": "3 - 2*(1/2)**n",
     "relation": "new"
    },
    {
     "text": "Let n grow.",
     "expr": "3",
     "relation": "limit",
     "variable": "n",
     "point": "oo"
    }
   ],
   "calculator_status": "no_calculator",
   "skills": [
    "BC-SKL-10003"
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
   "archetype_id": "BC-QA-10021",
   "parameter_draw": {
    "family": "rational",
    "lead": 5,
    "shift": 2,
    "rate": 3,
    "offset": 4,
    "ratio": "1/2",
    "numerator": 1,
    "start": 0
   },
   "stem": {
    "text": "The nth partial sum of \\(\\sum a_n\\) is \\(S_n=\\frac{5n+2}{3n+4}\\). The series converges. Find its sum.",
    "command_verb": "find"
   },
   "key": {
    "form": "numeric",
    "expr": "5/3"
   },
   "steps": [
    {
     "text": "S_n.",
     "expr": "(5*n+2)/(3*n+4)",
     "relation": "new"
    },
    {
     "text": "Divide by n and let n grow.",
     "expr": "5/3",
     "relation": "limit",
     "variable": "n",
     "point": "oo"
    }
   ],
   "calculator_status": "no_calculator",
   "skills": [
    "BC-SKL-10003"
   ]
  },
  {
   "id": "chk-3",
   "check_kind": "mcq",
   "format": "mcq",
   "bands": [
    "low"
   ],
   "archetype_id": "BC-QA-10021",
   "parameter_draw": {
    "family": "telescoping",
    "lead": 9,
    "shift": 0,
    "rate": 4,
    "offset": 6,
    "ratio": "3/4",
    "numerator": 6,
    "start": 1
   },
   "stem": {
    "text": "The series \\(\\sum_{n=1}^{\\infty}\\frac{6}{(n+1)(n+2)}\\) converges. Find its sum.",
    "command_verb": "find"
   },
   "key": {
    "form": "numeric",
    "expr": "3"
   },
   "steps": [
    {
     "text": "General term.",
     "expr": "6/((n+1)*(n+2))",
     "relation": "new"
    },
    {
     "text": "Split.",
     "expr": "6/(n+1) - 6/(n+2)",
     "relation": "equivalent"
    },
    {
     "text": "Add the first n terms.",
     "expr": "3 - 6/(n+2)",
     "relation": "new"
    },
    {
     "text": "Let n grow.",
     "expr": "3",
     "relation": "limit",
     "variable": "n",
     "point": "oo"
    }
   ],
   "options": [
    {
     "id": "A",
     "is_key": false,
     "expr": "0",
     "error_path": "BC-ERR-10001",
     "derivation": "the limit of the terms, 0, reported as the sum"
    },
    {
     "id": "B",
     "is_key": false,
     "expr": "1",
     "error_path": "BC-ERR-99038",
     "derivation": "the first partial sum S_1 reported as the sum"
    },
    {
     "id": "C",
     "is_key": false,
     "expr": "3/2",
     "error_path": "BC-ERR-99038",
     "derivation": "the second partial sum S_2 reported as the sum"
    },
    {
     "id": "D",
     "is_key": true,
     "expr": "3",
     "error_path": null
    }
   ],
   "calculator_status": "no_calculator",
   "skills": [
    "BC-SKL-10004"
   ]
  }
 ],
 "delivery": [
  {
   "block": "pr-1",
   "mode": "text",
   "reason": "rule 6: a question on numbers; the process itself is drawn in ki-1",
   "sources": [
    "BC-CON-10002"
   ]
  },
  {
   "block": "orientation",
   "mode": "text",
   "reason": "rule 6: a statement of what a response shows",
   "sources": [
    "BC-CON-10002"
   ]
  },
  {
   "block": "ki-1",
   "mode": "motion",
   "reason": "rule 2: the limit of the partial sums is a limit being taken and terms accumulating (BC-SKL-10003, BC-EK-LIM-7A2); the number line is the process's own picture, not a representation the stem carries",
   "sources": [
    "BC-SKL-10003"
   ],
   "spec": {
    "kind": "graph_sweep",
    "axis": "number line from 0 to 3.2",
    "parameter": {
     "name": "n",
     "frames": [
      1,
      2,
      3,
      4,
      8
     ]
    },
    "series": "S_n = 3 - 2*(1/2)**n",
    "markers": [
     {
      "at": "S_n",
      "shown": "each frame, with the earlier S_n left as small ticks"
     },
     {
      "at": "3",
      "shown": "every frame"
     }
    ],
    "labels": [
     {
      "text": "S_1 = 2",
      "placement": "inside"
     },
     {
      "text": "S_2 = 2.5",
      "placement": "inside"
     },
     {
      "text": "S_4 = 2.875",
      "placement": "inside"
     },
     {
      "text": "S = 3",
      "placement": "inside"
     }
    ]
   },
   "fallback": "three static frames side by side, n = 1, 4 and 8, each with its S_n labelled inside and the level 3 marked",
   "keyboard": "Right and Left arrow keys step the frames; Space pauses auto-advance",
   "reduced_motion": "no auto-advance; each key press cross-fades to the next frame"
  },
  {
   "block": "ki-2",
   "mode": "text",
   "reason": "rule 6: a definition and a procedure; BC-REP-11 and 01 on BC-SKL-10004",
   "sources": [
    "BC-SKL-10004"
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
   "block": "err-BC-ERR-10001",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  },
  {
   "block": "err-BC-ERR-10003",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  },
  {
   "block": "err-BC-ERR-99038",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  },
  {
   "block": "representations",
   "mode": "model",
   "reason": "the mode table: BC-CON-10002 is a productive-failure target through BC-QA-10021 (BC-DF-13, 15), and the computed sequence of partial sums is the idea; a numeric experiment shown as a table",
   "sources": [
    "BC-QA-10021"
   ],
   "spec": {
    "kind": "numeric_experiment",
    "representations": [
     "BC-REP-03"
    ],
    "computed": [
     "3 - 2*(1/2)**n",
     "(2*n+1)/(n+3)",
     "1 - 1/(n+1)"
    ],
    "n_values": [
     1,
     2,
     3,
     5,
     10,
     50
    ],
    "columns": [
     "n",
     "exponential S_n",
     "rational S_n",
     "telescoping S_n"
    ],
    "labels": [
     {
      "text": "each column of S_n closes on one number",
      "placement": "inside",
      "at": "row below the last value"
     }
    ]
   },
   "fallback": "the same six rows as static text under the representations text",
   "keyboard": "no control; table cells are reached in reading order with Tab"
  }
 ],
 "refresher": [
  "ki-1",
  "err-BC-ERR-10001",
  "err-BC-ERR-10003",
  "err-BC-ERR-99038",
  "ex-1"
 ],
 "read_minutes": {
  "full": 4.3,
  "brief": 2.8
 },
 "word_count": {
  "full": 642,
  "brief": 411
 },
 "research_lines": [
  {
   "file": "research/units/unit-10-infinite-sequences-series.md",
   "line": "Conceptual variants ask what the limit of the partial sums means; computational variants ask for a numerical partial sum or a telescoping total"
  }
 ],
 "inferred": [
  {
   "claim": "A fluent solver writes S_n and its limit and holds the statement that the sum is the limit of the partial sums.",
   "settles": "Timing data per step once the fluency telemetry exists."
  },
  {
   "claim": "The prediction poses S_n from ex-1 as four values and the formula and asks for the number the partial sums settle on, answerable from the values alone.",
   "settles": "Response data on the prediction, split by whether the key was entered."
  },
  {
   "claim": "Every non-text delivery choice (the motion on ki-1, the model on the representations block) follows the mode table and the Unit 10 README delivery map.",
   "settles": "The modality A/B in the build plan: skip rate and time to first credited success by mode."
  },
  {
   "claim": "The model table uses three series whose numbers appear in no example or check, so the table shows the idea without giving an answer.",
   "settles": "A review that the columns stay clear of every worked answer."
  }
 ],
 "sources": [
  "BC-CON-10002",
  "BC-SKL-10003",
  "BC-SKL-10004",
  "BC-SKL-10005",
  "BC-EK-LIM-7A1",
  "BC-EK-LIM-7A2",
  "ced:186",
  "BC-QA-10001",
  "BC-QA-10021",
  "BC-ERR-10001",
  "BC-ERR-10003",
  "BC-ERR-99038",
  "BC-MIS-10002",
  "BC-PRQ-06005",
  "BC-PRQ-10003",
  "BC-PRQ-10004",
  "BC-PRQ-10008",
  "research/units/unit-10-infinite-sequences-series.md#10.1 Defining Convergent and Divergent Infinite Series",
  "research/question-analysis/question-archetypes.md#BC-QA-10021 Sum of a series found from its partial sums before any test is taught",
  "research/question-analysis/question-archetypes.md#BC-QA-10001 Selecting a convergence test for a given series",
  "research/exam/exam-structure.md#Section and part layout"
 ]
}
```
