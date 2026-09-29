---
title: LSN-CON-10001 Partial sums of an infinite series
research_date: 2026-09-29
status: designed
purpose: Authoring spec for the concept lesson on BC-CON-10001, the nth partial sum as the total of the first n terms and its difference from the general term, built from authoring_bundle("BC-CON-10001") and the research files it cites, so an author fills plan 15's lesson record without making a teaching decision.
---

# LSN-CON-10001 Partial sums of an infinite series

Concept BC-CON-10001 (skills BC-SKL-10001, BC-SKL-10002), topic 10.1 of Unit 10, BC only (ced:186). It is the root of the convergence strand and has no Unit 10 hard parent (docs/lessons/unit-10/README.md, section 1). Two archetypes load its skills as a series-value shape, BC-QA-10021 and BC-QA-10002, and BC-QA-10001 loads both skills as a selection shape.

## Prediction

Served first, both bands: an `mcq` on ex-1's own numbers. The first four totals of the series (1/3, 1/2, 3/5, 2/3) follow n/(n+2), and the question is the total of the first ten terms. Key B, 5/6. The distractors are 1/66 (the tenth term alone) and 2/3 (the total does not change with n). The question uses no rule the lesson has not stated: the pattern of the four totals settles it. The resolution states the total of the first n terms and names it the partial sum, with no verdict. Source: BC-CON-10001 and the topic 10.1 section.

## Orientation

Served text, from BC-CON-10001 `description_plain` ("The first n terms of a series add to a number that depends on n") and the topic's Assessment behaviour paragraph (research/units/unit-10-infinite-sequences-series.md#10.1 Defining Convergent and Divergent Infinite Series): MCQ forms give a closed form for S_n or a general term and ask which of a sequence and a series converges, and a free response conclusion must name which series it is about. The orientation states what a response shows: S_n as a sum or an expression, and which object a claim is about. No count, no frequency.

## Key ideas

- ki-1 (core), BC-EK-LIM-7A1 (ced:186), loaded by BC-SKL-10002. Paraphrase of the Required mathematical knowledge paragraph Partial sum, with the sequence against series distinction the paragraph Convergence draws. Notation line: the concept's `notation`. No anchor quote, because the words are the definition and the brief band has no words to spare.
- ki-2 (core budget permitting, here extended), BC-EK-LIM-7A2 (ced:186), loaded by BC-SKL-10001 (the CED statement it maps is the convergence statement for a series). It says the partial sums form a sequence and that convergence is the limit of that sequence, and defers the limit to LSN-CON-10002. Extended, so the low band only.

## Recognition

BC-QA-10021 (family series-value; `common_givens` "a formula for the nth partial sum", "or an unsplit telescoping term"; `asked_to_produce` "the sum of the series") and BC-QA-10002 (`common_givens` "a geometric or telescoping series"; `asked_to_produce` "the value of the series") load BC-SKL-10002; BC-QA-10001 loads BC-SKL-10001 and BC-SKL-10005 (family procedure-selection; `typical_wording` "determine whether the series converges or diverges, and justify your answer"). Shapes: an MCQ that gives a closed form for S_n and asks for the sum; an MCQ that gives a general term and asks which of a sequence and a series converges; a free response part where the conclusion must name the series (topic Assessment behaviour). What says this concept: a sigma with n written above it, S_n named, or a total of a stated number of terms. What says not this concept: a list a_1, a_2, ... with the word sequence, which asks for the limit of the terms (BC-SKL-10001, the sibling skill).

The near miss of the contrast pair comes from BC-QA-10001's wrong approach "reporting the limit of the general term as the behaviour of the series": the same general term asked as a sequence.

## Method choice

- st-1, BC-QA-10021. Cue from `common_givens`. Method, `expected_solution_path[0]` "obtain the nth partial sum, directly or by cancelling a telescoping sum". Rival, `wrong_approaches` "taking the limit of the general term as the value of the series". Separating feature: the stem asks for a total of terms, not the size of one term. Both cue fields exist, so the block is verified. It carries the contrast pair, a total of three terms beside the same terms asked as a sequence.
- st-2, BC-QA-10001. Cue from `common_givens` ("a series of numbers in sigma or expanded form"). Method, `expected_solution_path[0]` "read the general term", followed by naming the object. Rival, `wrong_approaches` "reporting the limit of the general term as the behaviour of the series". Separating feature: a list of terms is about a_n, a sigma with the word series is about S_n. Low band only. No served field opens with the reader's own label.

## Solution path

- ex-1, BC-QA-10021, both bands, no calculator. Draw: family telescoping, lead 6, shift 0, rate 5, offset 2, ratio 3/4, numerator 2, start 1. Series the sum from n = 1 of 2/((n+1)(n+2)); S_4 = 2/3, S_n = 1 - 2/(n+2). No published item on BC-QA-10021 carries this draw (content/items_gen_unit10, ITM-GEN-10021-22 to 43).
- ex-2, low band, BC-QA-10002. Draw: form telescoping, start 2, coefficient 4, ratio 1/2, offset 2. Series the sum from n = 2 of 4/((n+2)(n+3)); S_n = 1 - 4/(n+3), and S_2 = 1/5 equals a_2. No published item on BC-QA-10002 carries this draw.
- ex-2 is faded from step 4: steps 1 to 3 (the start index, the general term, the split) are shown, the student writes S_n, and step 4 then reveals. The fade falls there because the split repeats ex-1's pattern and the new demand is the start index in the total.
- Steps: the general term (new), the split (equivalent), S_n (new, since the checker does not evaluate a sum with a symbolic upper limit), and on ex-1 the value at n = 4 (evaluate). A fluent solver writes S_n and the value; the reading of the sigma and the split are held (Time).
- The examples end at S_n, the first entry of BC-QA-10021's `expected_solution_path`; the limit that follows belongs to LSN-CON-10002. No productive-failure comparison: BC-CON-10001 is not in `PRODUCTIVE_FAILURE_TARGETS`.

## Scoring

None. BC-QA-10021 and BC-QA-10002 list no `point_types`, so the lesson says nothing about points and carries no scoring lines (plan 15, R14).

## Traps

Two errors meet the skills, in bundle order: BC-ERR-10001, BC-ERR-99038 (the earlier duplicate of BC-ERR-99038 is retired). Both blocks show the wrong and right step on ex-1's draw, both distinct, so both carry `fix_prompt` true. Low band both, mid band both.

- err-BC-ERR-10001: 0, the limit of a_n, against 1, the limit of S_n. Possible reason, BC-MIS-10001.
- err-BC-ERR-99038: S_4 = 2/3 offered as the value against 1. No possible reason line (the description names a belief the record marks inferred).

## Representations

None. The topic's Representations paragraph names BC-REP-10, 11, 01 and 04 and the conversions expanded terms to sigma, general term to the sequence of partial sums, and verbal to limit statement; nothing figure-shaped, and the Unit 10 README delivery map gives text for this concept.

## Prerequisite bridge

- BC-PRQ-06006, BC-PRQ-10004, BC-PRQ-10008, each from its `description_plain` and `failure_signature`.

## Time

Every Unit 10 archetype is `no_calculator`; its MCQ shape is Section I Part A, 2.14 minutes (research/exam/exam-structure.md#Section and part layout). BC-QA-10021 is an opener with no exam part and BC-QA-10002 has no recorded points, so the Part A budget is the only figure. A fluent solver writes S_n and the value, and holds the reading of the sigma and the split [inferred]. The minutes go on the split.

## Checks

- chk-1, completion of ex-1, both bands: S_n given, S_4 asked. Key 2/3.
- chk-2, isomorph, both bands. Draw BC-QA-10021: family telescoping, lead 2, shift 3, rate 4, offset 5, ratio 1/3, numerator 3, start 2. Write S_n for the sum of 3/((n+2)(n+3)). Key 1 - 3/(n+3).
- chk-3, MCQ, low band. Draw BC-QA-10021: family telescoping, lead 7, shift 1, rate 2, offset 3, ratio 2/3, numerator 5, start 1. Sum of 5/((n+1)(n+2)), S_n = 5/2 - 5/(n+2). Key 5/2. Distractors: 0, the limit of the terms (BC-ERR-10001); 5/6, S_1 (BC-ERR-99038); 5/4, S_2 (BC-ERR-99038). The skills hold two errors, so two distractors share BC-ERR-99038, the archetype's own first and second partial sum distractors.

## Delivery

- pr-1, orientation, ki-1, ki-2: text. Rule 6: the skills carry BC-REP-10, 11, 01 and 04, none figure-bearing, and the Unit 10 README delivery map gives text for this concept. No block is drawn, so the record carries `no_figure_reason`.
- ex-1, ex-2, the two error blocks: step_reveal. Rule 1.

## Band plan

- Low (full): prediction, orientation, bridges, ki-1, ki-2, st-1 with the contrast pair, st-2, ex-1, chk-1, the two error blocks, ex-2 (faded from step 4), chk-2, chk-3. 597 words, 4.0 minutes.
- Mid (brief): prediction, orientation, bridges, ki-1, st-1 with the contrast pair, ex-1, chk-1, the two error blocks, chk-2. 449 words, 3.0 minutes.
- Refresher: ki-1, the two error blocks, ex-1.

## Sources

- BC-CON-10001; BC-SKL-10001, BC-SKL-10002; BC-EK-LIM-7A1, BC-EK-LIM-7A2; ced:186
- BC-QA-10001, BC-QA-10002, BC-QA-10021
- BC-ERR-10001, BC-ERR-99038; BC-MIS-10001
- BC-PRQ-06006, BC-PRQ-10004, BC-PRQ-10008
- research/units/unit-10-infinite-sequences-series.md#10.1 Defining Convergent and Divergent Infinite Series
- research/question-analysis/question-archetypes.md#BC-QA-10021 Sum of a series found from its partial sums before any test is taught
- research/question-analysis/question-archetypes.md#BC-QA-10001 Selecting a convergence test for a given series
- research/question-analysis/question-archetypes.md#BC-QA-10002 Value of a convergent series requested
- research/exam/exam-structure.md#Section and part layout
- [inferred] The held steps, the prediction form, and ending the examples at S_n. Each settled as the inferred array states.

## Machine record

```json
{
 "id": "LSN-CON-10001",
 "kind": "concept",
 "target_id": "BC-CON-10001",
 "unit": "10",
 "skills": [
  "BC-SKL-10001",
  "BC-SKL-10002"
 ],
 "prediction": {
  "id": "pr-1",
  "stem": {
   "text": "The series \\(\\sum_{n=1}^{\\infty}\\frac{2}{(n+1)(n+2)}\\) has terms \\(\\frac13,\\frac16,\\frac1{10},\\frac1{15}\\). Adding the first 1, 2, 3, 4 terms gives \\(\\frac13,\\frac12,\\frac35,\\frac23\\). What do the first 10 terms add to?",
   "command_verb": "predict"
  },
  "format": "mcq",
  "options": [
   {
    "id": "A",
    "label": "\\(\\frac{1}{66}\\)",
    "is_key": false
   },
   {
    "id": "B",
    "label": "\\(\\frac{5}{6}\\)",
    "is_key": true
   },
   {
    "id": "C",
    "label": "\\(\\frac{2}{3}\\)",
    "is_key": false
   }
  ],
  "resolution": "The first \\(n\\) terms add to \\(\\frac{n}{n+2}\\), so ten terms give \\(\\frac56\\). That total is the partial sum \\(S_n\\), and it changes with \\(n\\).",
  "sources": [
   "BC-CON-10001",
   "research/units/unit-10-infinite-sequences-series.md#10.1 Defining Convergent and Divergent Infinite Series"
  ]
 },
 "no_figure_reason": "No skill carries a figure-bearing representation (sequence, series, symbolic and verbal only) and the key ideas define a total of terms, not a process.",
 "orientation": {
  "text": "The nth partial sum \\(S_n\\) is the total of the first \\(n\\) terms of a series, a number that depends on \\(n\\). A response writes \\(S_n\\) as a sum or as an expression in \\(n\\), and says whether a claim is about the terms \\(a_n\\) or the totals \\(S_n\\).",
  "sources": [
   "BC-CON-10001",
   "research/units/unit-10-infinite-sequences-series.md#10.1 Defining Convergent and Divergent Infinite Series"
  ]
 },
 "key_ideas": [
  {
   "id": "ki-1",
   "ek_id": "BC-EK-LIM-7A1",
   "depth": "core",
   "text": "For a series with terms \\(a_n\\), the nth partial sum is \\(S_n=a_1+a_2+\\cdots+a_n\\), the sum of the first \\(n\\) terms. The terms \\(a_n\\) and the partial sums \\(S_n\\) are two different sequences, and a claim about one is not a claim about the other.",
   "notation": "\\(a_n\\), \\(S_n\\), sigma notation",
   "quote": null,
   "sources": [
    "BC-EK-LIM-7A1",
    "ced:186",
    "research/units/unit-10-infinite-sequences-series.md#10.1 Defining Convergent and Divergent Infinite Series"
   ]
  },
  {
   "id": "ki-2",
   "ek_id": "BC-EK-LIM-7A2",
   "depth": "extended",
   "text": "The partial sums \\(S_1,S_2,S_3,\\dots\\) form a sequence. The series converges to \\(S\\) exactly when that sequence has limit \\(S\\), and diverges when the limit does not exist. Taking that limit is the next lesson.",
   "notation": "\\(\\lim_{n\\to\\infty}S_n\\)",
   "quote": null,
   "sources": [
    "BC-EK-LIM-7A2",
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
   "method": "Add the first \\(n\\) terms, cancel what telescopes, and write \\(S_n\\).",
   "rival": "Taking the limit of the general term as the value of the series.",
   "separating_feature": "The total of the first \\(n\\) terms is asked for, not the size of one term.",
   "sources": [
    "BC-QA-10021"
   ],
   "evidence_tag": "verified",
   "contrast": {
    "this": {
     "text": "For \\(\\sum_{n=1}^{\\infty}\\frac{3}{(n+3)(n+4)}\\), find the sum of the first three terms.",
     "archetype_id": "BC-QA-10021"
    },
    "not_this": {
     "text": "Does the sequence \\(a_n=\\frac{3}{(n+3)(n+4)}\\) converge, and to what?",
     "why_not": "It asks where the terms settle, not what a total reaches."
    },
    "feature": "A total of terms against a list of terms."
   }
  },
  {
   "id": "st-2",
   "archetype_id": "BC-QA-10001",
   "cue": "A series in sigma form, with the words converges or diverges.",
   "method": "Read the general term, then say whether the claim is about \\(a_n\\) or about the series.",
   "rival": "Reporting the limit of the general term as the behaviour of the series.",
   "separating_feature": "A list of terms is a question about \\(a_n\\); a sigma with the word series is about \\(S_n\\).",
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
    "family": "telescoping",
    "lead": 6,
    "shift": 0,
    "rate": 5,
    "offset": 2,
    "ratio": "3/4",
    "numerator": 2,
    "start": 1
   },
   "problem": {
    "text": "For \\(\\sum_{n=1}^{\\infty}\\frac{2}{(n+1)(n+2)}\\), write \\(S_n\\) and find \\(S_4\\).",
    "command_verb": "write"
   },
   "calculator_status": "no_calculator",
   "steps": [
    {
     "cue": "The sigma gives the general term.",
     "why": "Each \\(S_n\\) adds these terms.",
     "expr": "2/((n+1)*(n+2))",
     "relation": "new"
    },
    {
     "cue": "Split into two fractions.",
     "why": "Neighbouring terms will cancel.",
     "expr": "2/(n+1) - 2/(n+2)",
     "relation": "equivalent"
    },
    {
     "cue": "Add the first \\(n\\) terms.",
     "why": "Middle terms cancel; only \\(\\frac22\\) and \\(-\\frac{2}{n+2}\\) remain.",
     "expr": "1 - 2/(n+2)",
     "relation": "new"
    },
    {
     "cue": "Put \\(n=4\\).",
     "why": "\\(S_4\\) is one number, the total of four terms.",
     "expr": "2/3",
     "relation": "evaluate",
     "subs": {
      "n": 4
     }
    }
   ],
   "answer": {
    "form": "numeric",
    "expr": "2/3"
   }
  },
  {
   "id": "ex-2",
   "archetype_id": "BC-QA-10002",
   "bands": [
    "low"
   ],
   "fade_from": 4,
   "parameter_draw": {
    "form": "telescoping",
    "start": 2,
    "coefficient": 4,
    "ratio": "1/2",
    "offset": 2
   },
   "problem": {
    "text": "For \\(\\sum_{n=2}^{\\infty}\\frac{4}{(n+2)(n+3)}\\), write \\(S_n\\).",
    "command_verb": "write"
   },
   "calculator_status": "no_calculator",
   "steps": [
    {
     "cue": "The series starts at \\(n=2\\).",
     "why": "The first term is \\(a_2\\), so \\(S_n\\) adds \\(a_2\\) through \\(a_n\\)."
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
     "cue": "Add \\(a_2\\) through \\(a_n\\).",
     "why": "Only \\(\\frac44\\) and \\(-\\frac{4}{n+3}\\) remain.",
     "expr": "1 - 4/(n+3)",
     "relation": "new"
    }
   ],
   "answer": {
    "form": "symbolic",
    "expr": "1 - 4/(n+3)"
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
    "text": "\\(a_n\\to0\\), so the series adds to 0.",
    "expr": "0"
   },
   "right_step": {
    "text": "\\(S_n=1-\\frac{2}{n+2}\\to1\\), so the series adds to 1.",
    "expr": "1"
   },
   "relation": "distinct",
   "fix_prompt": true,
   "possible_reason": {
    "misconception_id": "BC-MIS-10001",
    "text": "does not separate the list of terms from their accumulated total"
   },
   "sources": [
    "BC-ERR-10001",
    "BC-MIS-10001"
   ]
  },
  {
   "error_id": "BC-ERR-99038",
   "observed_behavior": "Responses asked for the value of a convergent series add the first few terms and present that total, or recognise the series as geometric but cannot identify the common ratio, instead of summing it in closed form.",
   "scoring_consequence": "The value point is not earned, since a decimal approximation is not the requested exact value.",
   "wrong_step": {
    "text": "\\(S_4=\\frac23\\) is the value of the series.",
    "expr": "2/3"
   },
   "right_step": {
    "text": "The value is \\(\\lim_{n\\to\\infty}S_n=1\\).",
    "expr": "1"
   },
   "relation": "distinct",
   "fix_prompt": true,
   "possible_reason": null,
   "sources": [
    "BC-ERR-99038"
   ]
  }
 ],
 "representations": null,
 "prerequisite_bridges": [
  {
   "prq_id": "BC-PRQ-06006",
   "text": "Sigma notation lists terms by index."
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
    3,
    4
   ]
  },
  "skipped_steps": {
   "ex-1": [
    1,
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
   "archetype_id": "BC-QA-10021",
   "parameter_draw": {
    "family": "telescoping",
    "lead": 6,
    "shift": 0,
    "rate": 5,
    "offset": 2,
    "ratio": "3/4",
    "numerator": 2,
    "start": 1
   },
   "completes": "ex-1",
   "stem": {
    "text": "For \\(\\sum_{n=1}^{\\infty}\\frac{2}{(n+1)(n+2)}\\), \\(S_n=1-\\frac{2}{n+2}\\). Find \\(S_4\\).",
    "command_verb": "find"
   },
   "key": {
    "form": "numeric",
    "expr": "2/3"
   },
   "steps": [
    {
     "text": "S_n.",
     "expr": "1 - 2/(n+2)",
     "relation": "new"
    },
    {
     "text": "Put n = 4.",
     "expr": "2/3",
     "relation": "evaluate",
     "subs": {
      "n": 4
     }
    }
   ],
   "calculator_status": "no_calculator",
   "skills": [
    "BC-SKL-10002"
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
    "family": "telescoping",
    "lead": 2,
    "shift": 3,
    "rate": 4,
    "offset": 5,
    "ratio": "1/3",
    "numerator": 3,
    "start": 2
   },
   "stem": {
    "text": "Write \\(S_n\\) for \\(\\sum_{n=1}^{\\infty}\\frac{3}{(n+2)(n+3)}\\).",
    "command_verb": "write"
   },
   "key": {
    "form": "symbolic",
    "expr": "1 - 3/(n+3)"
   },
   "steps": [
    {
     "text": "General term.",
     "expr": "3/((n+2)*(n+3))",
     "relation": "new"
    },
    {
     "text": "Split.",
     "expr": "3/(n+2) - 3/(n+3)",
     "relation": "equivalent"
    },
    {
     "text": "Middle terms cancel.",
     "expr": "1 - 3/(n+3)",
     "relation": "new"
    }
   ],
   "calculator_status": "no_calculator",
   "skills": [
    "BC-SKL-10002"
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
    "lead": 7,
    "shift": 1,
    "rate": 2,
    "offset": 3,
    "ratio": "2/3",
    "numerator": 5,
    "start": 1
   },
   "stem": {
    "text": "The series \\(\\sum_{n=1}^{\\infty}\\frac{5}{(n+1)(n+2)}\\) converges. Find its sum.",
    "command_verb": "find"
   },
   "key": {
    "form": "numeric",
    "expr": "5/2"
   },
   "steps": [
    {
     "text": "General term.",
     "expr": "5/((n+1)*(n+2))",
     "relation": "new"
    },
    {
     "text": "Split.",
     "expr": "5/(n+1) - 5/(n+2)",
     "relation": "equivalent"
    },
    {
     "text": "Add the first n terms.",
     "expr": "5/2 - 5/(n+2)",
     "relation": "new"
    },
    {
     "text": "Let n grow.",
     "expr": "5/2",
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
     "expr": "5/6",
     "error_path": "BC-ERR-99038",
     "derivation": "the first partial sum S_1 reported as the sum"
    },
    {
     "id": "C",
     "is_key": true,
     "expr": "5/2",
     "error_path": null
    },
    {
     "id": "D",
     "is_key": false,
     "expr": "5/4",
     "error_path": "BC-ERR-99038",
     "derivation": "the second partial sum S_2 reported as the sum"
    }
   ],
   "calculator_status": "no_calculator",
   "skills": [
    "BC-SKL-10002"
   ]
  }
 ],
 "delivery": [
  {
   "block": "pr-1",
   "mode": "text",
   "reason": "rule 6: a question on numbers, no figure-bearing representation",
   "sources": [
    "BC-CON-10001"
   ]
  },
  {
   "block": "orientation",
   "mode": "text",
   "reason": "rule 6: BC-REP-10, 11, 01, 04 on BC-SKL-10001 and BC-SKL-10002, none figure-bearing",
   "sources": [
    "BC-SKL-10001",
    "BC-SKL-10002"
   ]
  },
  {
   "block": "ki-1",
   "mode": "text",
   "reason": "rule 6: a definition of a sum of terms; BC-REP-11 and 01 only",
   "sources": [
    "BC-SKL-10002"
   ]
  },
  {
   "block": "ki-2",
   "mode": "text",
   "reason": "rule 6: a statement about a sequence of totals, not a process the student steps through here",
   "sources": [
    "BC-SKL-10001"
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
   "block": "err-BC-ERR-99038",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  }
 ],
 "refresher": [
  "ki-1",
  "err-BC-ERR-10001",
  "err-BC-ERR-99038",
  "ex-1"
 ],
 "read_minutes": {
  "full": 4.0,
  "brief": 3.0
 },
 "word_count": {
  "full": 596,
  "brief": 448
 },
 "research_lines": [
  {
   "file": "research/units/unit-10-infinite-sequences-series.md",
   "line": "FRQ forms embed the definition inside a later part, where a conclusion must name which series is under discussion before it can be scored"
  }
 ],
 "inferred": [
  {
   "claim": "A fluent solver writes the general term split and S_n and holds the reading of the sigma and the split.",
   "settles": "Timing data per step once the fluency telemetry exists."
  },
  {
   "claim": "The prediction asks for the total of ten terms from the pattern of the first four totals, which the topic's Assessment behaviour does not state as a form.",
   "settles": "Response data on the prediction, split by whether the key was chosen."
  },
  {
   "claim": "Ex-1 and ex-2 end at S_n, the first step of BC-QA-10021's expected solution path, because the limit is taught in the next concept.",
   "settles": "An archetype task value that asks for S_n alone."
  }
 ],
 "sources": [
  "BC-CON-10001",
  "BC-SKL-10001",
  "BC-SKL-10002",
  "BC-EK-LIM-7A1",
  "BC-EK-LIM-7A2",
  "ced:186",
  "BC-QA-10001",
  "BC-QA-10002",
  "BC-QA-10021",
  "BC-ERR-10001",
  "BC-ERR-99038",
  "BC-MIS-10001",
  "BC-PRQ-06006",
  "BC-PRQ-10004",
  "BC-PRQ-10008",
  "research/units/unit-10-infinite-sequences-series.md#10.1 Defining Convergent and Divergent Infinite Series",
  "research/question-analysis/question-archetypes.md#BC-QA-10021 Sum of a series found from its partial sums before any test is taught",
  "research/question-analysis/question-archetypes.md#BC-QA-10001 Selecting a convergence test for a given series",
  "research/question-analysis/question-archetypes.md#BC-QA-10002 Value of a convergent series requested",
  "research/exam/exam-structure.md#Section and part layout"
 ]
}
```
