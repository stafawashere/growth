---
title: LSN-CON-10003 Geometric series and the constant ratio
research_date: 2026-09-29
status: designed
purpose: Authoring spec for the concept lesson on BC-CON-10003, a series whose consecutive terms have a constant quotient, found by dividing and read with its first term as written, built from authoring_bundle("BC-CON-10003") and the research files it cites, so an author fills plan 15's lesson record without making a teaching decision.
---

# LSN-CON-10003 Geometric series and the constant ratio

Concept BC-CON-10003 (skill BC-SKL-10006), topic 10.2 of Unit 10, BC only (ced:187). Hard parent BC-CON-10001 (docs/lessons/unit-10/README.md, section 1), so S_n and sigma notation are assumed. Two archetypes load BC-SKL-10006: BC-QA-10001 (family procedure-selection) and BC-QA-10003 (family series-value).

## Prediction

Served first, both bands: an `mcq` on ex-1's own numbers. The first three terms of the sum of 3 times 2^n over 5^n are 6/5, 12/25 and 24/125, and the question is the multiple from one term to the next. Key B, 2/5. The distractors are 3 (the coefficient) and 5/2 (the multiple upside down); the division of consecutive terms settles it before any rule is stated. The resolution names the quotient as the common ratio and says the coefficient does not decide it, with no verdict. Source: BC-CON-10003 and the topic 10.2 section.

## Orientation

Served text, from BC-CON-10003 `description_plain` ("A geometric series multiplies by the same number to get from one term to the next") and the topic's Assessment behaviour paragraph (research/units/unit-10-infinite-sequences-series.md#10.2 Working with Geometric Series): conceptual variants ask only for the ratio, and FRQ forms ask a response to recognise a series as geometric. The orientation states what a response shows: r by division and a as the first term as written. No count, no frequency.

## Key ideas

One essential knowledge statement maps to the skill, BC-EK-LIM-7A3 (ced:187): one core block, both bands.

- ki-1 (core). Paraphrase of the Required mathematical knowledge paragraphs Geometric series (a constant ratio between successive terms) and First term ("the first term of the series as written, whatever the starting index"), with the coefficient and the exponent's base named as the two readings BC-ERR-10004 records. Notation line: the concept's `notation`. No anchor quote, since the brief band has no words to spare.

## Recognition

BC-QA-10001 (family procedure-selection; `common_givens` "a series of numbers in sigma or expanded form"; `parameter_spec` form geometric, "a geometric term written as a quotient of powers") and BC-QA-10003 (`asked_to_produce` "the first term and common ratio"; `common_givens` "a power series stated to be geometric") load BC-SKL-10006. Shapes: an MCQ that asks for the sum or the ratio of a numerical geometric series, and a free response part that asks a response to recognise a Taylor series as geometric (topic Assessment behaviour); the official examples of BC-QA-10003 are BC-FRQ-2022-Q6-D, BC-FRQ-2025-Q6-C, BC-FRQ-2026-Q6-A and BC-MCQ-PE2012-005. What says this concept: the index n sits in exponents and each term is a fixed multiple of the last. What says not this concept: the index sits in a base (a p-series) or in a product of shifted factors (telescoping), whose consecutive quotients change with n.

The near miss of the contrast pair is a telescoping series from BC-QA-10002 (family series-value), which a student could read as decreasing and therefore geometric, the pattern behind BC-MIS-10003; the Unit 10 README, section 3, names geometric against p-series against telescoping as the neighbouring recognition.

## Method choice

- st-1, BC-QA-10001. Cue from `common_givens` and `parameter_spec` notes. Method, `expected_solution_path[0]` "read the general term", then dividing consecutive terms (BC-QA-10003 `expected_solution_path[0]`). Rival, `common_distractors` "using the geometric formula on a series without a constant ratio". Separating feature: the index in an exponent gives a constant quotient. Both cue fields exist, so the block is verified. It carries the contrast pair, a geometric stem from BC-QA-10001 beside a telescoping stem from BC-QA-10002.
- st-2, BC-QA-10003. Cue from `common_givens` and `asked_to_produce`. Method, `expected_solution_path[0]` "divide consecutive terms to find the ratio" and `expected_solution_path[1]` "identify the first term as written". Rival, `common_distractors` "taking the coefficient as the ratio". Low band only. No served field opens with the reader's own label.

## Solution path

- ex-1, BC-QA-10001, both bands, no calculator. Draw: form geometric, power 1/2, coefficient 3, start 1, lead_top 3, constant_top 2, lead_bottom 2, constant_bottom 5, ratio 2/5, base 3, degree 2. Series the sum from n = 1 of 3 times 2^n over 5^n, ratio 2/5. No published item on BC-QA-10001 carries this draw (content/items_gen_unit10, ITM-GEN-10001-00 to 21).
- ex-2, low band, BC-QA-10001. Draw: form geometric, power 1/2, coefficient 6, start 2, lead_top 3, constant_top 2, lead_bottom 2, constant_bottom 5, ratio 3/4, base 3, degree 2. Series the sum from n = 2 of 6 times 3^n over 4^n, first term 27/8, ratio 3/4. No published item carries this draw.
- ex-2 is faded from step 3: steps 1 and 2 (the general term and the first term at n = 2) are shown, the student writes the ratio, and steps 3 and 4 then reveal. The fade falls there because the division repeats ex-1's pattern and the new demand is the ratio, with the first term already read at the start index.
- Steps: the general term (new), on ex-2 the first term (evaluate at the start index), the quotient of consecutive terms (new) and its cancelled value (equivalent). A fluent solver writes the quotient and its value; the reading of the general term is held (Time). ex-2's answer is a statement (a and r), and its last valued step is r.
- No productive-failure comparison: BC-CON-10003 is not in `PRODUCTIVE_FAILURE_TARGETS`.

## Scoring

None. BC-QA-10001 lists no `point_types`, and neither example is on BC-QA-10003, which lists BC-PT-99067, 99068 and 99004. BC-PT-99067 scores the first term over one minus the ratio, taught in LSN-CON-10004; the rubrics reviewed award no point for stating a and r alone. The lesson says nothing about points and carries no scoring lines (plan 15, R14).

## Traps

One error meets the skill: BC-ERR-10004 (linked to BC-MIS-10003, medium). On ex-1's draw, distinct, so `fix_prompt` true. Low band and mid band both show it. Possible reason, BC-MIS-10003.

- err-BC-ERR-10004: r = 3, the coefficient, against r = 2/5. The record's observed behaviour also names the exponent as a misread ratio; chk-3 uses the upside-down ratio and the numerator's base for the other two distractors (Checks).

## Representations

None. The topic's Representations paragraph names BC-REP-11, 01 and 04 and the conversions sigma form to the pair a and r and a power series in x to a closed form; nothing figure-shaped, and the Unit 10 README delivery map gives text for this concept.

## Prerequisite bridge

- BC-PRQ-10005, BC-PRQ-10008, each from its `description_plain` and `failure_signature`.

## Time

Every Unit 10 archetype is `no_calculator`; its MCQ shape is Section I Part A, 2.14 minutes (research/exam/exam-structure.md#Section and part layout). BC-QA-10001 has no recorded points. A fluent solver writes the quotient of consecutive terms and its value, and holds the reading of the general term [inferred]. The minutes go on the cancellation of the powers.

## Checks

- chk-1, completion of ex-1, both bands: the quotient written, r asked. Key 2/5.
- chk-2, isomorph, both bands. Draw BC-QA-10001: form geometric, power 1/2, coefficient 2, start 1, lead_top 3, constant_top 2, lead_bottom 2, constant_bottom 5, ratio 5/6, base 3, degree 2. Ratio of 2 times 5^n over 6^n, key 5/6.
- chk-3, MCQ, low band. Draw BC-QA-10001: form geometric, power 1/2, coefficient 5, start 1, ratio 3/7, other values as ex-1. Ratio of 5 times 3^n over 7^n, key 3/7. Distractors, each on BC-ERR-10004: 5, the coefficient; 7/3, the ratio upside down (the template's own distractor for this form); 3, the numerator's base with the 7 to the n left out (BC-QA-10003's template distractor). The skill holds one error, so the three distractors are three misidentifications of the ratio, all inside that record's observed behaviour.

## Delivery

- pr-1, orientation, ki-1: text. Rule 6: BC-SKL-10006 carries BC-REP-11 and 01, none figure-bearing, and the Unit 10 README delivery map gives text for this concept. No block is drawn, so the record carries `no_figure_reason`.
- ex-1, ex-2, err-BC-ERR-10004: step_reveal. Rule 1.

## Band plan

- Low (full): prediction, orientation, bridges, ki-1, st-1 with the contrast pair, st-2, ex-1, chk-1, err-BC-ERR-10004, ex-2 (faded from step 3), chk-2, chk-3. 437 words, 3.0 minutes.
- Mid (brief): prediction, orientation, bridges, ki-1, st-1 with the contrast pair, ex-1, chk-1, err-BC-ERR-10004, chk-2. 336 words, 2.3 minutes.
- Refresher: ki-1, err-BC-ERR-10004, ex-1.

## Sources

- BC-CON-10003; BC-SKL-10006; BC-EK-LIM-7A3; ced:187
- BC-QA-10001, BC-QA-10002, BC-QA-10003
- BC-ERR-10004; BC-MIS-10003
- BC-PRQ-10005, BC-PRQ-10008
- research/units/unit-10-infinite-sequences-series.md#10.2 Working with Geometric Series
- research/question-analysis/question-archetypes.md#BC-QA-10001 Selecting a convergence test for a given series
- research/question-analysis/question-archetypes.md#BC-QA-10002 Value of a convergent series requested
- research/question-analysis/question-archetypes.md#BC-QA-10003 Geometric series summed in closed form
- research/exam/exam-structure.md#Section and part layout
- [inferred] The held steps, the prediction form, the untagged examples, and the shared error path on chk-3. Each settled as the inferred array states.

## Machine record

```json
{
 "id": "LSN-CON-10003",
 "kind": "concept",
 "target_id": "BC-CON-10003",
 "unit": "10",
 "skills": [
  "BC-SKL-10006"
 ],
 "prediction": {
  "id": "pr-1",
  "stem": {
   "text": "Predict. The terms of \\(\\sum_{n=1}^{\\infty}\\frac{3\\cdot2^n}{5^n}\\) are \\(\\frac65,\\frac{12}{25},\\frac{24}{125}\\). Each is the same multiple of the term before it. What is the multiple?",
   "command_verb": "predict"
  },
  "format": "mcq",
  "options": [
   {
    "id": "A",
    "label": "\\(3\\)",
    "is_key": false
   },
   {
    "id": "B",
    "label": "\\(\\frac25\\)",
    "is_key": true
   },
   {
    "id": "C",
    "label": "\\(\\frac52\\)",
    "is_key": false
   }
  ],
  "resolution": "Each quotient \\(\\frac{a_{n+1}}{a_n}\\) equals \\(\\frac25\\), the common ratio, whatever the coefficient 3.",
  "sources": [
   "BC-CON-10003",
   "research/units/unit-10-infinite-sequences-series.md#10.2 Working with Geometric Series"
  ]
 },
 "no_figure_reason": "No skill carries a figure-bearing representation (series, symbolic and verbal only) and the key idea is a definition about a quotient of terms, not a process.",
 "orientation": {
  "text": "A geometric series has the same quotient \\(r\\) from each term to the next, so its terms are \\(a, ar, ar^2,\\dots\\). A response names \\(r\\) by dividing consecutive terms, and names \\(a\\) as the first term of the series as written.",
  "sources": [
   "BC-CON-10003",
   "research/units/unit-10-infinite-sequences-series.md#10.2 Working with Geometric Series"
  ]
 },
 "key_ideas": [
  {
   "id": "ki-1",
   "ek_id": "BC-EK-LIM-7A3",
   "depth": "core",
   "text": "A series is geometric when \\(\\frac{a_{n+1}}{a_n}\\) is the same constant \\(r\\) for every \\(n\\). The first term \\(a\\) is the term the series starts with, whatever the starting index. In \\(c\\,p^n/q^n\\), neither the coefficient \\(c\\) nor the exponent's base \\(p\\) is \\(r\\) by itself.",
   "notation": "\\(a\\) for the first term, \\(r\\) for the common ratio",
   "quote": null,
   "sources": [
    "BC-EK-LIM-7A3",
    "ced:187",
    "research/units/unit-10-infinite-sequences-series.md#10.2 Working with Geometric Series"
   ]
  }
 ],
 "strategy": [
  {
   "id": "st-1",
   "archetype_id": "BC-QA-10001",
   "cue": "A series in sigma form, with the index in an exponent.",
   "method": "Read the general term, then divide \\(a_{n+1}\\) by \\(a_n\\).",
   "rival": "Using the geometric formula on a series without a constant ratio.",
   "separating_feature": "The index in an exponent gives a constant quotient; the index in a base does not.",
   "sources": [
    "BC-QA-10001"
   ],
   "evidence_tag": "verified",
   "contrast": {
    "this": {
     "text": "Name a test that fits \\(\\sum_{n=1}^{\\infty}\\frac{4\\cdot5^n}{9^n}\\) and state its ratio.",
     "archetype_id": "BC-QA-10001"
    },
    "not_this": {
     "text": "Find the sum of \\(\\sum_{n=1}^{\\infty}\\frac{3}{(n+1)(n+2)}\\).",
     "why_not": "The quotient \\(\\frac{n+1}{n+3}\\) changes with \\(n\\), so the series telescopes."
    },
    "feature": "A constant quotient of consecutive terms."
   }
  },
  {
   "id": "st-2",
   "archetype_id": "BC-QA-10003",
   "cue": "A power series in \\(x\\) stated to be geometric, with a first term and ratio asked.",
   "method": "Divide consecutive terms to find the ratio, then read the first term as written.",
   "rival": "Taking the coefficient as the ratio.",
   "separating_feature": "The ratio is the quotient of consecutive terms, whatever the coefficient.",
   "sources": [
    "BC-QA-10003"
   ],
   "evidence_tag": "verified"
  }
 ],
 "worked_examples": [
  {
   "id": "ex-1",
   "archetype_id": "BC-QA-10001",
   "bands": [
    "low",
    "mid"
   ],
   "parameter_draw": {
    "form": "geometric",
    "power": "1/2",
    "coefficient": 3,
    "start": 1,
    "lead_top": 3,
    "constant_top": 2,
    "lead_bottom": 2,
    "constant_bottom": 5,
    "ratio": "2/5",
    "base": 3,
    "degree": 2
   },
   "problem": {
    "text": "Find the common ratio of \\(\\sum_{n=1}^{\\infty}\\frac{3\\cdot2^n}{5^n}\\).",
    "command_verb": "find"
   },
   "calculator_status": "no_calculator",
   "steps": [
    {
     "cue": "Read the general term.",
     "why": "The ratio comes from the term itself.",
     "expr": "3*2**n/5**n",
     "relation": "new"
    },
    {
     "cue": "Divide \\(a_{n+1}\\) by \\(a_n\\).",
     "why": "A constant quotient makes it geometric.",
     "expr": "(3*2**(n+1)/5**(n+1))/(3*2**n/5**n)",
     "relation": "new"
    },
    {
     "cue": "Cancel.",
     "why": "The \\(n\\) drops out, so \\(r=\\frac25\\).",
     "expr": "2/5",
     "relation": "equivalent"
    }
   ],
   "answer": {
    "form": "numeric",
    "expr": "2/5"
   }
  },
  {
   "id": "ex-2",
   "archetype_id": "BC-QA-10001",
   "bands": [
    "low"
   ],
   "fade_from": 3,
   "parameter_draw": {
    "form": "geometric",
    "power": "1/2",
    "coefficient": 6,
    "start": 2,
    "lead_top": 3,
    "constant_top": 2,
    "lead_bottom": 2,
    "constant_bottom": 5,
    "ratio": "3/4",
    "base": 3,
    "degree": 2
   },
   "problem": {
    "text": "Find the first term and the common ratio of \\(\\sum_{n=2}^{\\infty}\\frac{6\\cdot3^n}{4^n}\\).",
    "command_verb": "find"
   },
   "calculator_status": "no_calculator",
   "steps": [
    {
     "cue": "Read the general term.",
     "why": "Both answers come from it.",
     "expr": "6*3**n/4**n",
     "relation": "new"
    },
    {
     "cue": "The series starts at \\(n=2\\).",
     "why": "The first term is \\(a_2\\), not \\(a_0\\).",
     "expr": "27/8",
     "relation": "evaluate",
     "subs": {
      "n": 2
     }
    },
    {
     "cue": "Divide \\(a_{n+1}\\) by \\(a_n\\).",
     "why": "A constant quotient makes it geometric.",
     "expr": "(6*3**(n+1)/4**(n+1))/(6*3**n/4**n)",
     "relation": "new"
    },
    {
     "cue": "Cancel.",
     "why": "The \\(n\\) drops out, so \\(r=\\frac34\\).",
     "expr": "3/4",
     "relation": "equivalent"
    }
   ],
   "answer": {
    "form": "statement",
    "expr": "a = 27/8, r = 3/4"
   }
  }
 ],
 "what_a_reader_scores": [],
 "common_errors": [
  {
   "error_id": "BC-ERR-10004",
   "observed_behavior": "The response names a ratio that does not equal the quotient of consecutive terms, often taking the coefficient or the exponent as the ratio.",
   "scoring_consequence": "The sum and the convergence condition both follow from the ratio, so the part is lost from that step onward.",
   "wrong_step": {
    "text": "\\(r=3\\), the coefficient.",
    "expr": "3"
   },
   "right_step": {
    "text": "\\(r=\\frac25\\), the quotient.",
    "expr": "2/5"
   },
   "relation": "distinct",
   "fix_prompt": true,
   "possible_reason": {
    "misconception_id": "BC-MIS-10003",
    "text": "without identifying a constant ratio or checking its size"
   },
   "sources": [
    "BC-ERR-10004",
    "BC-MIS-10003"
   ]
  }
 ],
 "representations": null,
 "prerequisite_bridges": [
  {
   "prq_id": "BC-PRQ-10005",
   "text": "Divide consecutive terms and check the quotient is constant."
  },
  {
   "prq_id": "BC-PRQ-10008",
   "text": "The general term is read at each index, and a sign factor is kept."
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
   "archetype_id": "BC-QA-10001",
   "parameter_draw": {
    "form": "geometric",
    "power": "1/2",
    "coefficient": 3,
    "start": 1,
    "lead_top": 3,
    "constant_top": 2,
    "lead_bottom": 2,
    "constant_bottom": 5,
    "ratio": "2/5",
    "base": 3,
    "degree": 2
   },
   "completes": "ex-1",
   "stem": {
    "text": "For \\(\\sum_{n=1}^{\\infty}\\frac{3\\cdot2^n}{5^n}\\), \\(\\frac{a_{n+1}}{a_n}=\\frac{3\\cdot2^{n+1}\\cdot5^n}{5^{n+1}\\cdot3\\cdot2^n}\\). Find \\(r\\).",
    "command_verb": "find"
   },
   "key": {
    "form": "numeric",
    "expr": "2/5"
   },
   "steps": [
    {
     "text": "Quotient of consecutive terms.",
     "expr": "(3*2**(n+1)/5**(n+1))/(3*2**n/5**n)",
     "relation": "new"
    },
    {
     "text": "Cancel.",
     "expr": "2/5",
     "relation": "equivalent"
    }
   ],
   "calculator_status": "no_calculator",
   "skills": [
    "BC-SKL-10006"
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
   "archetype_id": "BC-QA-10001",
   "parameter_draw": {
    "form": "geometric",
    "power": "1/2",
    "coefficient": 2,
    "start": 1,
    "lead_top": 3,
    "constant_top": 2,
    "lead_bottom": 2,
    "constant_bottom": 5,
    "ratio": "5/6",
    "base": 3,
    "degree": 2
   },
   "stem": {
    "text": "Find the common ratio of \\(\\sum_{n=1}^{\\infty}\\frac{2\\cdot5^n}{6^n}\\).",
    "command_verb": "find"
   },
   "key": {
    "form": "numeric",
    "expr": "5/6"
   },
   "steps": [
    {
     "text": "General term.",
     "expr": "2*5**n/6**n",
     "relation": "new"
    },
    {
     "text": "Quotient of consecutive terms.",
     "expr": "(2*5**(n+1)/6**(n+1))/(2*5**n/6**n)",
     "relation": "new"
    },
    {
     "text": "Cancel.",
     "expr": "5/6",
     "relation": "equivalent"
    }
   ],
   "calculator_status": "no_calculator",
   "skills": [
    "BC-SKL-10006"
   ]
  },
  {
   "id": "chk-3",
   "check_kind": "mcq",
   "format": "mcq",
   "bands": [
    "low"
   ],
   "archetype_id": "BC-QA-10001",
   "parameter_draw": {
    "form": "geometric",
    "power": "1/2",
    "coefficient": 5,
    "start": 1,
    "lead_top": 3,
    "constant_top": 2,
    "lead_bottom": 2,
    "constant_bottom": 5,
    "ratio": "3/7",
    "base": 3,
    "degree": 2
   },
   "stem": {
    "text": "Find the common ratio of \\(\\sum_{n=1}^{\\infty}\\frac{5\\cdot3^n}{7^n}\\).",
    "command_verb": "find"
   },
   "key": {
    "form": "numeric",
    "expr": "3/7"
   },
   "steps": [
    {
     "text": "General term.",
     "expr": "5*3**n/7**n",
     "relation": "new"
    },
    {
     "text": "Quotient of consecutive terms.",
     "expr": "(5*3**(n+1)/7**(n+1))/(5*3**n/7**n)",
     "relation": "new"
    },
    {
     "text": "Cancel.",
     "expr": "3/7",
     "relation": "equivalent"
    }
   ],
   "options": [
    {
     "id": "A",
     "is_key": false,
     "expr": "5",
     "error_path": "BC-ERR-10004",
     "derivation": "the coefficient taken as the ratio"
    },
    {
     "id": "B",
     "is_key": false,
     "expr": "7/3",
     "error_path": "BC-ERR-10004",
     "derivation": "the ratio read upside down, the denominator's base over the numerator's"
    },
    {
     "id": "C",
     "is_key": true,
     "expr": "3/7",
     "error_path": null
    },
    {
     "id": "D",
     "is_key": false,
     "expr": "3",
     "error_path": "BC-ERR-10004",
     "derivation": "the numerator's base taken as the ratio, with the 7 to the n left out"
    }
   ],
   "calculator_status": "no_calculator",
   "skills": [
    "BC-SKL-10006"
   ]
  }
 ],
 "delivery": [
  {
   "block": "pr-1",
   "mode": "text",
   "reason": "rule 6: a question on numbers, no figure-bearing representation",
   "sources": [
    "BC-CON-10003"
   ]
  },
  {
   "block": "orientation",
   "mode": "text",
   "reason": "rule 6: a statement of what a response shows",
   "sources": [
    "BC-CON-10003"
   ]
  },
  {
   "block": "ki-1",
   "mode": "text",
   "reason": "rule 6: BC-REP-11 and 01 on BC-SKL-10006, neither figure-bearing; a definition, not a process",
   "sources": [
    "BC-SKL-10006"
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
   "block": "err-BC-ERR-10004",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  }
 ],
 "refresher": [
  "ki-1",
  "err-BC-ERR-10004",
  "ex-1"
 ],
 "read_minutes": {
  "full": 3.0,
  "brief": 2.3
 },
 "word_count": {
  "full": 437,
  "brief": 336
 },
 "research_lines": [
  {
   "file": "research/units/unit-10-infinite-sequences-series.md",
   "line": "Conceptual variants ask only for the ratio"
  }
 ],
 "inferred": [
  {
   "claim": "A fluent solver writes the quotient of consecutive terms and its cancelled value, and holds the reading of the general term.",
   "settles": "Timing data per step once the fluency telemetry exists."
  },
  {
   "claim": "The prediction asks for the multiple between consecutive terms, which the three terms settle by division, before the ratio is named.",
   "settles": "Response data on the prediction, split by whether the key was chosen."
  },
  {
   "claim": "Neither example carries a point type: BC-PT-99067 scores the first term over one minus the ratio, which LSN-CON-10004 teaches, and no point in the rubrics reviewed is earned by naming a and r alone.",
   "settles": "A rubric part that scores a stated first term and ratio."
  },
  {
   "claim": "The two distractors of chk-3 beyond the coefficient, the ratio upside down and the numerator's base alone, share BC-ERR-10004, because the skill holds one error and its observed behaviour lists more than one misidentification.",
   "settles": "A second error record for the ratio read upside down."
  }
 ],
 "sources": [
  "BC-CON-10003",
  "BC-SKL-10006",
  "BC-EK-LIM-7A3",
  "ced:187",
  "BC-QA-10001",
  "BC-QA-10002",
  "BC-QA-10003",
  "BC-ERR-10004",
  "BC-MIS-10003",
  "BC-PRQ-10005",
  "BC-PRQ-10008",
  "research/units/unit-10-infinite-sequences-series.md#10.2 Working with Geometric Series",
  "research/question-analysis/question-archetypes.md#BC-QA-10001 Selecting a convergence test for a given series",
  "research/question-analysis/question-archetypes.md#BC-QA-10002 Value of a convergent series requested",
  "research/question-analysis/question-archetypes.md#BC-QA-10003 Geometric series summed in closed form",
  "research/exam/exam-structure.md#Section and part layout"
 ]
}
```
