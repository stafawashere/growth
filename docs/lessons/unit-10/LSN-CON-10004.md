---
title: LSN-CON-10004 Convergence condition and sum of a geometric series
research_date: 2026-09-29
status: designed
purpose: Authoring spec for the concept lesson on BC-CON-10004, a geometric series converging exactly when the ratio is smaller than one in size, with sum the first term as written over one minus the ratio, built from authoring_bundle("BC-CON-10004") and the research files it cites, so an author fills plan 15's lesson record without making a teaching decision.
---

# LSN-CON-10004 Convergence condition and sum of a geometric series

Concept BC-CON-10004 (skills BC-SKL-10007, BC-SKL-10008, BC-SKL-10009, BC-SKL-10010), topics 10.2 of Unit 10, BC only (ced:187), with BC-SKL-10010 also mapped to BC-EK-LIM-8F1 (ced:199). Hard parent BC-CON-10003 (docs/lessons/unit-10/README.md, section 1), so the ratio and the first term are assumed. Three archetypes load its skills: BC-QA-10003, BC-QA-10002 and BC-QA-10020.

## Prediction

Served first, both bands: an `mcq` on ex-1's own numbers. The first three terms of the sum from n = 2 of 3(2/5)^n are given with the ratio 2/5, and the question is the total of all the terms. Key B, 4/5. The distractors are 12/25 (the first term alone), 6/5 and "No finite total". The running totals 0.48, 0.672, 0.7488 settle it near 0.8 before any rule is stated, and 6/5 is out of reach of them. The resolution names the first term over one minus the ratio, with no verdict. Source: BC-CON-10004 and the topic 10.2 section.

## Orientation

Served text, from BC-CON-10004 `description_plain` ("A geometric series adds to a finite total exactly when the ratio is smaller than one in size") and the topic's Assessment behaviour paragraph (research/units/unit-10-infinite-sequences-series.md#10.2 Working with Geometric Series): computational variants ask for the value, and justification variants require the convergence condition alongside the sum. The orientation states what a response shows: the condition on |r|, the first term as written, and the sum or the divergence. No count, no frequency.

## Key ideas

Two essential knowledge statements map to the skills; ki-1 is the only core block.

- ki-1 (core), BC-EK-LIM-7A4 (ced:187), loaded by BC-SKL-10007 to 10010. Paraphrase of the Required mathematical knowledge paragraphs Sum (hypotheses a real and |r| < 1; conclusion a over 1 minus r; at least one in size, the series diverges) and First term ("the first term of the series as written, whatever the starting index"). Notation line: the concept's `notation`. No anchor quote, since the CED statement on ced:187 is broken across lines and the brief band has no words to spare.
- ki-2 (extended), BC-EK-LIM-8F1 (ced:199), loaded by BC-SKL-10010. The topic 10.14 Standard series paragraph ("The Maclaurin series for one over one minus x is a geometric series") with the skill's own description, "Treat the expression in x as the ratio, sum it, and record where the sum is valid". Low band only.

## Recognition

BC-QA-10003 (family series-value; `asked_to_produce` "the value of the series at a point", "the closed form of the series on its interval of convergence"; `common_givens` "a power series stated to be geometric") loads all four skills; BC-QA-10002 (`common_givens` "a geometric or telescoping series", `typical_wording` "find the value of the series, or state that it diverges") loads BC-SKL-10008; BC-QA-10020 (`asked_to_produce` "a reason placing the input relative to the interval of convergence") loads BC-SKL-10007 and BC-SKL-10010. Shapes: an MCQ that asks for the sum of a numerical geometric series or the values of x for which a geometric power series converges, and free response parts that recognise a Taylor series as geometric and show it sums to a closed form (topic Assessment behaviour); official examples of BC-QA-10003 include BC-FRQ-2022-Q6-D, BC-FRQ-2025-Q6-C, BC-FRQ-2026-Q6-A and BC-MCQ-PE2012-005. What says this concept: a geometric series and a request for its value, its closed form, or where it converges. What says not this concept: a ratio of size at least one at the input, which calls for divergence, or a series whose quotient is not constant (LSN-CON-10003).

The near miss of the contrast pair is BC-QA-10020's input outside the interval, where the closed form still returns a number: at x = 6 the ratio is 5/4 and 4/(5 - 6) = -4 is not a sum. It is the wrong approach of BC-QA-10020, "substituting into the geometric closed form at an input whose ratio has size at least one".

## Method choice

- st-1, BC-QA-10002. Cue from `common_givens`. Method, `expected_solution_path` "identify the structure of the series", "write ... the pair of first term and ratio", "apply the closed form", joined with the condition on |r| that BC-EK-LIM-7A4 requires. Rival, `wrong_approaches` "adding the first few terms instead of summing in closed form". Separating feature: a constant ratio of size below 1. Both cue fields exist, so the block is verified. It carries the contrast pair, a convergent numerical series from BC-QA-10002 beside an input at which the closed form does not apply from BC-QA-10020.
- st-2, BC-QA-10003. Cue from `common_givens` and `typical_wording`. Method, `expected_solution_path` "divide consecutive terms to find the ratio", "identify the first term as written", "state the condition on the size of the ratio", "form the quotient and simplify". Rival, `wrong_approaches` "applying the closed form with a ratio of size at least one". Low band only. No served field opens with the reader's own label.

## Solution path

- ex-1, BC-QA-10002, both bands, no calculator. Draw: form geometric, start 2, coefficient 3, ratio 2/5, offset 1. Sum from n = 2 of 3(2/5)^n = (12/25)/(3/5) = 4/5. No published item on BC-QA-10002 carries this draw (content/items_gen_unit10, ITM-GEN-10002-00 to 04, whose geometric draws are 3, 1, -2/5 and 2, 6, 2/5 on start, coefficient, ratio).
- ex-2, low band, BC-QA-10003. Draw: power 1, start 2, sign positive, coefficient 5, base 3, centre 0. Sum from n = 2 of 5x^n/3^n, ratio x/3, first term 5x^2/9, sum 5x^2/(3(3 - x)) for |x| < 3. The constraint coefficient != base^start holds (5 != 9). No published item on BC-QA-10003 carries this draw.
- ex-2 is faded from step 5: steps 1 to 4 (the ratio in x, the general term, the first term at n = 2, the condition) are shown, the student writes the closed form, and steps 5 and 6 then reveal. The fade falls there because reading a and r repeats ex-1 and the new demand is the sum with x in the ratio.
- Steps: ex-1 the general term (new), the first term at the start index (evaluate), the closed form (new) and its value (equivalent); ex-2 the same with x. A fluent solver writes the first term, the closed form and its value; the ratio and the check of |r| are held (Time).
- No productive-failure comparison: BC-CON-10004 is not in `PRODUCTIVE_FAILURE_TARGETS`.

## Scoring

BC-QA-10003 lists BC-PT-99067, 99068 and 99004. ex-2 tags BC-PT-99067 on the first term over one minus the ratio, quoted from `reader_checks`. BC-PT-99068 (verification for a show-that prompt) applies only where a closed form is supplied, and BC-PT-99004 (a value answer) scores a value, not a closed form in x, so neither is tagged. ex-1 is on BC-QA-10002, which lists no `point_types`, so it carries no scoring lines.

Point losses from the archetype: a single verification point is available where the closed form is supplied, and presenting the unsimplified quotient of first term by one minus ratio is sufficient (BC-QA-10003 `scoring_pattern`, sg-25:26); a ratio of magnitude at least one earns no point (BC-PT-99067 `does_not_earn`, sg-26:21).

## Traps

Three errors meet the skills, in bundle order: BC-ERR-10005, BC-ERR-10006, BC-ERR-99038. All distinct, so all carry `fix_prompt` true. Low band all three, mid band the first two. BC-ERR-10006 and BC-ERR-99038 are on ex-1's draw. BC-ERR-10005 is shown on ex-1's terms with the ratio inverted to 5/2, since no draw of these archetypes has a ratio of size at least one (inferred array). Possible reasons: BC-MIS-10003, BC-MIS-10004, BC-MIS-10002.

- err-BC-ERR-10005: the closed form at r = 5/2 gives -25/2, against divergence, written as infinity in the SymPy pair.
- err-BC-ERR-10006: 3/(1 - 2/5) = 5 from the n = 0 term, against (12/25)/(1 - 2/5) = 4/5.
- err-BC-ERR-99038: three terms added, against the closed form 4/5.

## Representations

None. The topic's Representations paragraph names BC-REP-11, 01 and 04 and the conversions sigma form to the pair a and r and a power series in x to a closed form with the inequality that bounds x; nothing figure-shaped, and the Unit 10 README delivery map gives text for this concept.

## Prerequisite bridge

- BC-PRQ-10001, BC-PRQ-10003, BC-PRQ-10005, BC-PRQ-10008, each from its `description_plain` and `failure_signature`.

## Time

Every Unit 10 archetype is `no_calculator`; its MCQ shape is Section I Part A, 2.14 minutes (research/exam/exam-structure.md#Section and part layout). As a free response part, BC-QA-10003 with a closed form to verify scores one point, 1.67 minutes, and a value part with a first term and ratio scores more (docs/lessons/unit-10/README.md, section 5). A fluent solver writes the first term, the closed form and its value, and holds the reading of the ratio and the check of |r| [inferred]. The minutes go on the first term at the start index.

## Checks

- chk-1, completion of ex-1, both bands: the first term and ratio given, the sum asked. Key 4/5.
- chk-2, isomorph, both bands. Draw BC-QA-10002: form geometric, start 3, coefficient 4, ratio 1/3, offset 1. Sum from n = 3 of 4(1/3)^n = (4/27)/(2/3) = 2/9.
- chk-3, MCQ, low band. Draw BC-QA-10002: form geometric, start 2, coefficient 5, ratio -1/2, offset 3. Key 5/6. Distractors: 10/3, the n = 0 term as the first term (BC-ERR-10006); 5/8, the first two terms (BC-ERR-99038); 15/16, the first three terms (BC-ERR-99038). BC-ERR-10005 has no distractor, since a convergent draw cannot produce it, and two distractors share BC-ERR-99038, the archetype's own partial sum distractors.

## Delivery

- pr-1, orientation, ki-1, ki-2: text. Rule 6: the skills carry BC-REP-11, 01 and 04, none figure-bearing, and the Unit 10 README delivery map gives text for this concept. No block is drawn, so the record carries `no_figure_reason`.
- ex-1, ex-2, the three error blocks: step_reveal. Rule 1.

## Band plan

- Low (full): prediction, orientation, bridges, ki-1, ki-2, st-1 with the contrast pair, st-2, ex-1, chk-1, the three error blocks, ex-2 (faded from step 5) and its line, chk-2, chk-3. 754 words, 5.1 minutes.
- Mid (brief): prediction, orientation, bridges, ki-1, st-1 with the contrast pair, ex-1, chk-1, err-BC-ERR-10005, err-BC-ERR-10006, chk-2. 450 words, 3.0 minutes.
- Refresher: ki-1, the three error blocks, ex-1.

## Sources

- BC-CON-10004; BC-SKL-10007, BC-SKL-10008, BC-SKL-10009, BC-SKL-10010; BC-EK-LIM-7A4, BC-EK-LIM-8F1; ced:187, ced:199
- BC-QA-10002, BC-QA-10003, BC-QA-10020; BC-PT-99067
- BC-ERR-10005, BC-ERR-10006, BC-ERR-99038; BC-MIS-10002, BC-MIS-10003, BC-MIS-10004
- BC-PRQ-10001, BC-PRQ-10003, BC-PRQ-10005, BC-PRQ-10008
- sg-25:26
- research/units/unit-10-infinite-sequences-series.md#10.2 Working with Geometric Series
- research/units/unit-10-infinite-sequences-series.md#10.14 Finding Taylor or Maclaurin Series for a Function
- research/question-analysis/question-archetypes.md#BC-QA-10002 Value of a convergent series requested
- research/question-analysis/question-archetypes.md#BC-QA-10003 Geometric series summed in closed form
- research/exam/exam-structure.md#Section and part layout
- [inferred] The held steps, the prediction form, the inverted ratio on BC-ERR-10005, and the missing distractor on chk-3. Each settled as the inferred array states.

## Machine record

```json
{
 "id": "LSN-CON-10004",
 "kind": "concept",
 "target_id": "BC-CON-10004",
 "unit": "10",
 "skills": [
  "BC-SKL-10007",
  "BC-SKL-10008",
  "BC-SKL-10009",
  "BC-SKL-10010"
 ],
 "prediction": {
  "id": "pr-1",
  "stem": {
   "text": "Predict. The first terms of \\(\\sum_{n=2}^{\\infty}3\\left(\\frac25\\right)^n\\) are \\(\\frac{12}{25},\\frac{24}{125},\\frac{48}{625}\\), each \\(\\frac25\\) of the one before. About what total do all the terms add to?",
   "command_verb": "predict"
  },
  "format": "mcq",
  "options": [
   {
    "id": "A",
    "label": "\\(\\frac{12}{25}\\)",
    "is_key": false
   },
   {
    "id": "B",
    "label": "\\(\\frac{4}{5}\\)",
    "is_key": true
   },
   {
    "id": "C",
    "label": "\\(\\frac{6}{5}\\)",
    "is_key": false
   },
   {
    "id": "D",
    "label": "No finite total",
    "is_key": false
   }
  ],
  "resolution": "The terms shrink by \\(\\frac25\\) each time, so the total is finite: the first term over one minus the ratio, \\(\\frac{12/25}{1-2/5}=\\frac45\\).",
  "sources": [
   "BC-CON-10004",
   "research/units/unit-10-infinite-sequences-series.md#10.2 Working with Geometric Series"
  ]
 },
 "orientation": {
  "text": "A geometric series with first term \\(a\\) and ratio \\(r\\) converges exactly when \\(|r|<1\\), and then its sum is \\(\\frac{a}{1-r}\\). A response states the condition on \\(|r|\\), takes \\(a\\) as the first term as written, and reports the sum, or says the series diverges.",
  "sources": [
   "BC-CON-10004",
   "research/units/unit-10-infinite-sequences-series.md#10.2 Working with Geometric Series"
  ]
 },
 "key_ideas": [
  {
   "id": "ki-1",
   "ek_id": "BC-EK-LIM-7A4",
   "depth": "core",
   "text": "If \\(|r|<1\\), then \\(\\sum_{n=0}^{\\infty}ar^n=\\frac{a}{1-r}\\). If \\(|r|\\ge1\\), the series diverges. The formula takes \\(a\\) as the first term of the series as written, at any starting index.",
   "notation": "\\(\\frac{a}{1-r}\\); \\(|r|<1\\)",
   "quote": null,
   "sources": [
    "BC-EK-LIM-7A4",
    "ced:187",
    "research/units/unit-10-infinite-sequences-series.md#10.2 Working with Geometric Series"
   ]
  },
  {
   "id": "ki-2",
   "ek_id": "BC-EK-LIM-8F1",
   "depth": "extended",
   "text": "When the ratio contains \\(x\\), the sum holds where \\(|r|<1\\), which bounds \\(x\\). The Maclaurin series for \\(\\frac{1}{1-x}\\) is the geometric series with \\(a=1\\) and \\(r=x\\), valid for \\(|x|<1\\).",
   "notation": "\\(\\frac{1}{1-x}=\\sum_{n=0}^{\\infty}x^n\\)",
   "quote": null,
   "sources": [
    "BC-EK-LIM-8F1",
    "ced:199",
    "research/units/unit-10-infinite-sequences-series.md#10.14 Finding Taylor or Maclaurin Series for a Function"
   ]
  }
 ],
 "strategy": [
  {
   "id": "st-1",
   "archetype_id": "BC-QA-10002",
   "cue": "A geometric series, or a series that comes from a power series at a point.",
   "method": "Name \\(a\\) and \\(r\\), check \\(|r|<1\\), then take \\(\\frac{a}{1-r}\\).",
   "rival": "Adding the first few terms instead of the closed form.",
   "separating_feature": "A constant ratio of size below 1 allows the closed form.",
   "sources": [
    "BC-QA-10002"
   ],
   "evidence_tag": "verified",
   "contrast": {
    "this": {
     "text": "Find the value of \\(\\sum_{n=1}^{\\infty}5\\left(\\frac14\\right)^n\\), or state that it diverges.",
     "archetype_id": "BC-QA-10002"
    },
    "not_this": {
     "text": "At \\(x=6\\), does \\(\\sum_{n=0}^{\\infty}\\left(\\frac{x-1}{4}\\right)^n\\) converge to \\(\\frac{4}{5-x}\\)?",
     "why_not": "The ratio there is \\(\\frac54\\), so the series diverges and has no sum."
    },
    "feature": "\\(|r|<1\\) lets the closed form apply."
   }
  },
  {
   "id": "st-2",
   "archetype_id": "BC-QA-10003",
   "cue": "A power series in x, with a closed form to reach or verify.",
   "method": "Divide consecutive terms for \\(r\\), read \\(a\\) as written, state \\(|r|<1\\), then form \\(\\frac{a}{1-r}\\).",
   "rival": "Applying the closed form with a ratio of size at least one.",
   "separating_feature": "A ratio containing \\(x\\) turns \\(|r|<1\\) into a condition on \\(x\\).",
   "sources": [
    "BC-QA-10003"
   ],
   "evidence_tag": "verified"
  }
 ],
 "worked_examples": [
  {
   "id": "ex-1",
   "archetype_id": "BC-QA-10002",
   "bands": [
    "low",
    "mid"
   ],
   "parameter_draw": {
    "form": "geometric",
    "start": 2,
    "coefficient": 3,
    "ratio": "2/5",
    "offset": 1
   },
   "problem": {
    "text": "Find the value of \\(\\sum_{n=2}^{\\infty}3\\left(\\frac25\\right)^n\\), or state that it diverges.",
    "command_verb": "find"
   },
   "calculator_status": "no_calculator",
   "steps": [
    {
     "cue": "Each term is \\(\\frac25\\) of the last.",
     "why": "\\(\\left|\\frac25\\right|<1\\), so it converges and the formula applies."
    },
    {
     "cue": "Read the general term.",
     "why": "The first term comes from it.",
     "expr": "3*(2/5)**n",
     "relation": "new"
    },
    {
     "cue": "The series starts at \\(n=2\\).",
     "why": "The first term is \\(a_2\\), not \\(a_0=3\\).",
     "expr": "12/25",
     "relation": "evaluate",
     "subs": {
      "n": 2
     }
    },
    {
     "cue": "First term over one minus the ratio.",
     "why": "The closed form of the sum.",
     "expr": "(12/25)/(1 - 2/5)",
     "relation": "new"
    },
    {
     "cue": "Simplify.",
     "why": "\\(\\frac{12}{25}\\div\\frac35=\\frac45\\).",
     "expr": "4/5",
     "relation": "equivalent"
    }
   ],
   "answer": {
    "form": "numeric",
    "expr": "4/5"
   }
  },
  {
   "id": "ex-2",
   "archetype_id": "BC-QA-10003",
   "bands": [
    "low"
   ],
   "fade_from": 5,
   "parameter_draw": {
    "power": 1,
    "start": 2,
    "sign": "positive",
    "coefficient": 5,
    "base": 3,
    "centre": 0
   },
   "problem": {
    "text": "Find the sum of \\(\\sum_{n=2}^{\\infty}\\frac{5x^n}{3^n}\\) as an expression in \\(x\\), where the series converges.",
    "command_verb": "find"
   },
   "calculator_status": "no_calculator",
   "steps": [
    {
     "cue": "The ratio has \\(x\\) in it.",
     "why": "So convergence is a condition on \\(x\\)."
    },
    {
     "cue": "Read the general term.",
     "why": "The ratio is \\(\\frac{x}{3}\\).",
     "expr": "5*x**n/3**n",
     "relation": "new"
    },
    {
     "cue": "The series starts at \\(n=2\\).",
     "why": "The first term is \\(a_2\\).",
     "expr": "5*x**2/9",
     "relation": "evaluate",
     "subs": {
      "n": 2
     }
    },
    {
     "cue": "Convergence needs \\(\\left|\\frac{x}{3}\\right|<1\\).",
     "why": "That is \\(|x|<3\\)."
    },
    {
     "cue": "First term over one minus the ratio.",
     "why": "Inside \\(|x|<3\\), the closed form applies.",
     "expr": "(5*x**2/9)/(1 - x/3)",
     "relation": "new",
     "point_type_id": "BC-PT-99067"
    },
    {
     "cue": "Simplify.",
     "why": "Multiply top and bottom by 3.",
     "expr": "5*x**2/(3*(3 - x))",
     "relation": "equivalent"
    }
   ],
   "answer": {
    "form": "symbolic",
    "expr": "5*x**2/(3*(3 - x))"
   }
  }
 ],
 "what_a_reader_scores": [
  {
   "example_id": "ex-2",
   "point_type_ids": [
    "BC-PT-99067"
   ],
   "lines": [
    {
     "point_type_id": "BC-PT-99067",
     "text": "Geometric series sum from first term and common ratio. Earned by: Use of the first term over one minus the common ratio, with a nonzero first term and a ratio of the correct magnitude (sg-26:21). Not earned by: A sum formula built on a ratio of magnitude at least one; a series imported from an earlier part that is not geometric, which sg-22:22 states makes the point unavailable."
    }
   ]
  }
 ],
 "common_errors": [
  {
   "error_id": "BC-ERR-10005",
   "observed_behavior": "The response applies the closed form for the sum without checking that the absolute value of the ratio is less than one, and reports a finite value for a divergent series.",
   "scoring_consequence": "A finite value reported for a divergent series loses the answer point and any reasoning point attached to it.",
   "wrong_step": {
    "text": "With \\(r=\\frac52\\): \\(\\frac{75/4}{1-5/2}\\).",
    "expr": "(75/4)/(1 - 5/2)"
   },
   "right_step": {
    "text": "With \\(r=\\frac52\\), \\(|r|>1\\): the series diverges.",
    "expr": "oo"
   },
   "relation": "distinct",
   "fix_prompt": true,
   "possible_reason": {
    "misconception_id": "BC-MIS-10003",
    "text": "without identifying a constant ratio or checking its size"
   },
   "sources": [
    "BC-ERR-10005",
    "BC-MIS-10003"
   ]
  },
  {
   "error_id": "BC-ERR-10006",
   "observed_behavior": "The response applies the geometric sum formula with a first term read from the index zero position although the series as written starts at a different index.",
   "scoring_consequence": "The reported sum is wrong by a factor, so the value point is lost.",
   "wrong_step": {
    "text": "\\(\\frac{3}{1-2/5}=5\\), the \\(n=0\\) term.",
    "expr": "3/(1 - 2/5)"
   },
   "right_step": {
    "text": "\\(\\frac{12/25}{1-2/5}=\\frac45\\), the \\(n=2\\) term.",
    "expr": "(12/25)/(1 - 2/5)"
   },
   "relation": "distinct",
   "fix_prompt": true,
   "possible_reason": {
    "misconception_id": "BC-MIS-10004",
    "text": "reads the sum formula as requiring the term at index zero"
   },
   "sources": [
    "BC-ERR-10006",
    "BC-MIS-10004"
   ]
  },
  {
   "error_id": "BC-ERR-99038",
   "observed_behavior": "Responses asked for the value of a convergent series add the first few terms and present that total, or recognise the series as geometric but cannot identify the common ratio, instead of summing it in closed form.",
   "scoring_consequence": "The value point is not earned, since a decimal approximation is not the requested exact value.",
   "wrong_step": {
    "text": "\\(\\frac{12}{25}+\\frac{24}{125}+\\frac{48}{625}\\), three terms.",
    "expr": "12/25 + 24/125 + 48/625"
   },
   "right_step": {
    "text": "\\(\\frac{12/25}{1-2/5}=\\frac45\\), the closed form.",
    "expr": "(12/25)/(1 - 2/5)"
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
 "representations": null,
 "prerequisite_bridges": [
  {
   "prq_id": "BC-PRQ-10001",
   "text": "\\(|r|<1\\) means \\(-1<r<1\\); with \\(x\\), solve for \\(x\\)."
  },
  {
   "prq_id": "BC-PRQ-10003",
   "text": "A sum keeps its value when its index is shifted."
  },
  {
   "prq_id": "BC-PRQ-10005",
   "text": "Divide consecutive terms and check the quotient is constant."
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
    4,
    5
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
   "archetype_id": "BC-QA-10002",
   "parameter_draw": {
    "form": "geometric",
    "start": 2,
    "coefficient": 3,
    "ratio": "2/5",
    "offset": 1
   },
   "completes": "ex-1",
   "stem": {
    "text": "For \\(\\sum_{n=2}^{\\infty}3\\left(\\frac25\\right)^n\\), the first term is \\(\\frac{12}{25}\\) and \\(r=\\frac25\\). Find the sum.",
    "command_verb": "find"
   },
   "key": {
    "form": "numeric",
    "expr": "4/5"
   },
   "steps": [
    {
     "text": "First term over one minus the ratio.",
     "expr": "(12/25)/(1 - 2/5)",
     "relation": "new"
    },
    {
     "text": "Simplify.",
     "expr": "4/5",
     "relation": "equivalent"
    }
   ],
   "calculator_status": "no_calculator",
   "skills": [
    "BC-SKL-10008"
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
   "archetype_id": "BC-QA-10002",
   "parameter_draw": {
    "form": "geometric",
    "start": 3,
    "coefficient": 4,
    "ratio": "1/3",
    "offset": 1
   },
   "stem": {
    "text": "Find the value of \\(\\sum_{n=3}^{\\infty}4\\left(\\frac13\\right)^n\\), or state that it diverges.",
    "command_verb": "find"
   },
   "key": {
    "form": "numeric",
    "expr": "2/9"
   },
   "steps": [
    {
     "text": "General term.",
     "expr": "4*(1/3)**n",
     "relation": "new"
    },
    {
     "text": "First term, at n = 3.",
     "expr": "4/27",
     "relation": "evaluate",
     "subs": {
      "n": 3
     }
    },
    {
     "text": "First term over one minus the ratio.",
     "expr": "(4/27)/(1 - 1/3)",
     "relation": "new"
    },
    {
     "text": "Simplify.",
     "expr": "2/9",
     "relation": "equivalent"
    }
   ],
   "calculator_status": "no_calculator",
   "skills": [
    "BC-SKL-10009"
   ]
  },
  {
   "id": "chk-3",
   "check_kind": "mcq",
   "format": "mcq",
   "bands": [
    "low"
   ],
   "archetype_id": "BC-QA-10002",
   "parameter_draw": {
    "form": "geometric",
    "start": 2,
    "coefficient": 5,
    "ratio": "-1/2",
    "offset": 3
   },
   "stem": {
    "text": "Find the value of \\(\\sum_{n=2}^{\\infty}5\\left(-\\frac12\\right)^n\\), or state that it diverges.",
    "command_verb": "find"
   },
   "key": {
    "form": "numeric",
    "expr": "5/6"
   },
   "steps": [
    {
     "text": "General term.",
     "expr": "5*(-1/2)**n",
     "relation": "new"
    },
    {
     "text": "First term, at n = 2.",
     "expr": "5/4",
     "relation": "evaluate",
     "subs": {
      "n": 2
     }
    },
    {
     "text": "First term over one minus the ratio.",
     "expr": "(5/4)/(1 - (-1/2))",
     "relation": "new"
    },
    {
     "text": "Simplify.",
     "expr": "5/6",
     "relation": "equivalent"
    }
   ],
   "options": [
    {
     "id": "A",
     "is_key": false,
     "expr": "10/3",
     "error_path": "BC-ERR-10006",
     "derivation": "the n = 0 term, 5, used as the first term"
    },
    {
     "id": "B",
     "is_key": false,
     "expr": "5/8",
     "error_path": "BC-ERR-99038",
     "derivation": "the first two terms added and reported as the value"
    },
    {
     "id": "C",
     "is_key": false,
     "expr": "15/16",
     "error_path": "BC-ERR-99038",
     "derivation": "the first three terms added and reported as the value"
    },
    {
     "id": "D",
     "is_key": true,
     "expr": "5/6",
     "error_path": null
    }
   ],
   "calculator_status": "no_calculator",
   "skills": [
    "BC-SKL-10009"
   ]
  }
 ],
 "delivery": [
  {
   "block": "pr-1",
   "mode": "text",
   "reason": "rule 6: a question on numbers, no figure-bearing representation",
   "sources": [
    "BC-CON-10004"
   ]
  },
  {
   "block": "orientation",
   "mode": "text",
   "reason": "rule 6: a statement of what a response shows",
   "sources": [
    "BC-CON-10004"
   ]
  },
  {
   "block": "ki-1",
   "mode": "text",
   "reason": "rule 6: BC-REP-11, 01 and 04 on BC-SKL-10007 to 10010, none figure-bearing; a formula and its condition, not a process",
   "sources": [
    "BC-SKL-10007",
    "BC-SKL-10008",
    "BC-SKL-10009"
   ]
  },
  {
   "block": "ki-2",
   "mode": "text",
   "reason": "rule 6: a statement about a ratio containing x and a recall fact, BC-REP-11 and 01",
   "sources": [
    "BC-SKL-10010"
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
   "block": "err-BC-ERR-10005",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  },
  {
   "block": "err-BC-ERR-10006",
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
  "err-BC-ERR-10005",
  "err-BC-ERR-10006",
  "err-BC-ERR-99038",
  "ex-1"
 ],
 "read_minutes": {
  "full": 5.1,
  "brief": 3.0
 },
 "word_count": {
  "full": 754,
  "brief": 450
 },
 "no_figure_reason": "No skill carries a figure-bearing representation (series, symbolic and verbal only) and the key ideas state a condition and a formula, not a process.",
 "research_lines": [
  {
   "file": "research/units/unit-10-infinite-sequences-series.md",
   "line": "justification variants require the convergence condition to be stated alongside the sum"
  }
 ],
 "inferred": [
  {
   "claim": "A fluent solver writes the first term at the start index, the closed form and its value, and holds the reading of the ratio and the condition check.",
   "settles": "Timing data per step once the fluency telemetry exists."
  },
  {
   "claim": "The prediction asks for the total of ex-1's series, which the first terms and the ratio place near 0.8 before the closed form is stated.",
   "settles": "Response data on the prediction, split by whether the key was chosen."
  },
  {
   "claim": "The BC-ERR-10005 block shows the wrong and right step on ex-1's terms with the ratio inverted to 5/2, because the draws of BC-QA-10002 and BC-QA-10003 never carry a ratio of size at least one.",
   "settles": "A parameter_spec case with a ratio of size at least one, or an archetype task value that asks for divergence."
  },
  {
   "claim": "chk-3 carries no distractor on BC-ERR-10005, because a convergent draw of BC-QA-10002 cannot produce a finite value that the error would misreport; two distractors share BC-ERR-99038.",
   "settles": "A divergent case in the archetype's parameter_spec."
  }
 ],
 "sources": [
  "BC-CON-10004",
  "BC-SKL-10007",
  "BC-SKL-10008",
  "BC-SKL-10009",
  "BC-SKL-10010",
  "BC-EK-LIM-7A4",
  "BC-EK-LIM-8F1",
  "ced:187",
  "ced:199",
  "BC-QA-10002",
  "BC-QA-10003",
  "BC-QA-10020",
  "BC-PT-99067",
  "sg-25:26",
  "BC-ERR-10005",
  "BC-ERR-10006",
  "BC-ERR-99038",
  "BC-MIS-10002",
  "BC-MIS-10003",
  "BC-MIS-10004",
  "BC-PRQ-10001",
  "BC-PRQ-10003",
  "BC-PRQ-10005",
  "BC-PRQ-10008",
  "research/units/unit-10-infinite-sequences-series.md#10.2 Working with Geometric Series",
  "research/units/unit-10-infinite-sequences-series.md#10.14 Finding Taylor or Maclaurin Series for a Function",
  "research/question-analysis/question-archetypes.md#BC-QA-10002 Value of a convergent series requested",
  "research/question-analysis/question-archetypes.md#BC-QA-10003 Geometric series summed in closed form",
  "research/exam/exam-structure.md#Section and part layout"
 ]
}
```
