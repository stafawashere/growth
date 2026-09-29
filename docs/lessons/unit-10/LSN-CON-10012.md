---
title: LSN-CON-10012 The ratio test and its three cases
research_date: 2026-09-29
status: designed
purpose: Authoring spec for the concept lesson on BC-CON-10012, the ratio test with its three cases on the limit of the absolute ratio of consecutive terms, built from authoring_bundle("BC-CON-10012") and the research files it cites, so an author fills plan 15's lesson record without making a teaching decision.
---

# LSN-CON-10012 The ratio test and its three cases

Concept BC-CON-10012 (skills BC-SKL-10031, BC-SKL-10032, BC-SKL-10033), topic 10.8 of Unit 10, BC only (ced:193), loaded by four archetypes, BC-QA-10013, BC-QA-10014, BC-QA-10001 and BC-QA-10004. Hard parent in Unit 10: BC-CON-10003 (the geometric series and its constant ratio); the outside supporting parent is BC-SKL-01058 (docs/lessons/unit-10/README.md, section 1). The CED closes the list of assessed tests, so the ratio test is one of six and no root test is taught (ced:193).

## Prediction

Served first, both bands: an `mcq` on ex-1's own series at one input. At \(x=5\) the terms of \(\sum\frac{2n(x-3)^n}{5^n}\) are \(2n(0.4)^n\), and the student says what the partial sums do. Key A, they settle at a finite value. The distractors are unbounded growth and a swing between two values, both false, so A is the only true option. It is answerable before the rule: the terms shrink by a factor near 0.4 each step, faster than the factor n grows. The resolution states the ratio, 0.4, and the three cases of the ratio test as the topic gives them, with no verdict word. Source: BC-CON-10012 and the topic section the key idea cites.

## Orientation

Served text, from BC-CON-10012 `description_plain` and the topic's Assessment behaviour paragraph (research/units/unit-10-infinite-sequences-series.md#10.8 Ratio Test for Convergence): the ratio is the first scored step of the interval of convergence question and of the radius question, a ratio and its limit each earn a point, and a response with no ratio is not eligible for the limit point. The orientation states what a response shows, with no count and no frequency.

## Key ideas

All three skills map one BC-EK, BC-EK-LIM-7A11 (ced:193): one core block, both bands.

- ki-1 (core). Paraphrase of the topic's Ratio test paragraph: the hypothesis (the limit of the absolute value of the ratio exists or is infinite), the three cases (below 1 converges absolutely, above 1 diverges, equal to 1 gives no information), the Substitution paragraph (every occurrence of the index is replaced, including inside an exponent, sg-22:21) and the Notation paragraph (limit notation, sg-25:25). Notation line: the concept's `notation`. No anchor quote: the CED sentence on ced:193 adds nothing the paraphrase lacks.

## Recognition

BC-QA-10014 (family radius-interval; research/question-analysis/question-archetypes.md#BC-QA-10014 Radius of convergence from a given series) is the archetype of ex-1; BC-QA-10001 (family procedure-selection) is the archetype of ex-2. BC-QA-10013 (interval of convergence) and BC-QA-10004 also load skills of the concept.

- BC-QA-10014 `common_givens`: "a Maclaurin or Taylor series in sigma notation", "an instruction to use the ratio test". `asked_to_produce`: "the ratio of consecutive terms", "the limit of the ratio", "the radius of convergence stated as a value". `typical_wording`: "determine the radius of convergence of the series".
- BC-QA-10001 `common_givens`: "a series of numbers in sigma or expanded form"; `asked_to_produce`: "a convergence or divergence verdict naming the series", "the name of an applicable test". Its `difficulty_variables` name "whether a factorial or an nth power is present".
- The signal in the stem: an exponential in n, such as \(5^n\) or \(4^n\), or a factorial, in the general term, with a request for a radius or a verdict.
- Shapes: an MCQ giving a series with factorials or nth powers and asking what the ratio test shows (topic Assessment behaviour; BC-MCQ-PE2012-013), and the radius part of an FRQ (BC-FRQ-2021-Q6-C, BC-FRQ-2014-Q6-A, BC-FRQ-2015-Q6-A, BC-FRQ-2024-Q6-D). BC-QA-10014 `multipart_structure`: "Typically one part of the multipart free response question that closes Section II Part B, or a single multiple choice item."

The near miss of the contrast pair is a p-series stem, from outside the archetype (BC-QA-10001, the p-series form): the ratio tends to 1 and the ratio test gives no information, so another test decides. The pair differs in the general term.

What says "not this concept": a fixed power of n alone (BC-CON-10007); terms that bound cleanly against a known series (BC-CON-10009); a sign factor with a request to show convergence (BC-CON-10011). The root test is not assessed (ced:193).

## Method choice

- st-1, BC-QA-10014, both bands. Cue from `common_givens` and `asked_to_produce`. Method, `expected_solution_path[0]` and `[1]`: the ratio of consecutive terms with n+1 in every place, then its limit, written as the first line without a label. Rival from `wrong_approaches`: no absolute values (BC-ERR-10022), and n replaced in some places only (BC-ERR-10021). Separating feature: exponentials or factorials in n. The block also carries the contrast pair.
- st-2, BC-QA-10001, low band. The verdict shape: the ratio, its limit L, then the three cases, naming the series in the verdict. Rival from the `wrong_approaches` of the concept's errors: reading L equal to 1 as convergence (BC-MIS-10014).

Both archetypes carry `asked_to_produce` and `common_givens`, so both blocks are verified.

## Solution path

- ex-1, BC-QA-10014, both bands, no calculator. Draw: form divided, centre 3, base 5, power 1, coefficient 2, start 1, so the series \(\sum\frac{2n(x-3)^n}{5^n}\), the cancelled ratio \(\frac{(n+1)\lvert x-3\rvert}{5n}\), the limit \(\frac{\lvert x-3\rvert}{5}\) and \(R=5\). No published item on BC-QA-10014 carries this draw (content/items_gen_unit10/ITM-GEN-10014-00 to 04; the ITM-AGT items use another draw shape).
- ex-2, low band, no calculator. Draw: form ratio_factorial, base 5, power 2, coefficient 3, start 1, lead_top 2, constant_top 3, lead_bottom 2, constant_bottom 3, ratio 1/2, degree 2, so \(a_n=\frac{5^n}{n!}\), ratio \(\frac{5}{n+1}\), limit 0. The only published ratio_factorial draw on BC-QA-10001 is ITM-GEN-10001-06 (base 2).
- ex-2 is faded from step 3: steps 1 and 2 (the term and the unsimplified ratio) are shown, the student writes the cancelled ratio, its limit and the verdict, and steps 3 to 5 then reveal. The fade falls there because writing \(n+1\) in every place is what ex-1 has just modelled, and the cancellation of the factorial is the step the student must produce.
- Steps follow `expected_solution_path`: the term (new), the ratio (new), its cancelled form (equivalent, checked on ex-2 for the factorial), the limit (limit as n to infinity), and the value the limit gives, which on ex-1 is the radius (new) and on ex-2 the comparison with 1. The ratio on ex-1 is written in its cancelled form, because a symbolic power \((x-3)^{n+1}\) has no equivalence the checker recomputes. A fluent solver writes the cancelled ratio, its limit and the radius (Time).
- No productive-failure comparison: BC-CON-10012 is not in `PRODUCTIVE_FAILURE_TARGETS` (docs/lessons/unit-10/README.md, section 6).

## Scoring

BC-QA-10014 lists BC-PT-99042, BC-PT-99043 and BC-PT-99047. ex-1 tags BC-PT-99042 on the ratio step and quotes the `reader_checks` line. The limit point BC-PT-99043 and the radius point BC-PT-99047 are taught in ex-1's steps but untagged, since their reader lines (83 and 51 words) would take the brief band past its cap (inferred array). ex-2 is on BC-QA-10001, which lists no `point_types`, so it carries no scoring line and the lesson says nothing about points there (plan 15, R14).

Point losses from research: a correct ratio earns its point with or without absolute values, and a response with no ratio is not eligible for the limit point (research/units/unit-10-infinite-sequences-series.md#10.8 Ratio Test for Convergence, sg-25:25); any error in simplification or evaluation forfeits the limit point while the ratio point stands; an interval presented with no radius does not earn the radius point (sg-21:24).

## Traps

Four errors meet the skills, in bundle order: BC-ERR-10009, BC-ERR-10022, BC-ERR-10017, BC-ERR-10021. Low band all four, mid band the first two. All on ex-1's draw.

- err-BC-ERR-10009: "The ratio test converges." beside \(L=\frac{\lvert x-3\rvert}{5}\) then \(L<1\). The two share a value, so the relation is equivalent and `fix_prompt` is false. Possible reason, BC-MIS-10007.
- err-BC-ERR-10022: the cancelled ratio without bars, against with bars. Distinct, `fix_prompt` true. No possible reason line (the linked BC-MIS-10014 and BC-MIS-10015 do not describe the omission).
- err-BC-ERR-10017: the ratio written equal to \(\frac{\lvert x-3\rvert}{5}\) with no limit symbol, against the limit written. Equivalent, `fix_prompt` false, since the difference is the notation.
- err-BC-ERR-10021: n+1 in the power of \(x-3\) only, against n+1 in every place. Distinct, `fix_prompt` true. Possible reason, BC-MIS-10014.

## Representations

None. The topic's Representations paragraph names BC-REP-11 and 01 and the conversions general term to the ratio of consecutive terms and ratio limit to an inequality in the variable; nothing figure-shaped (docs/lessons/unit-10/README.md, section 6).

## Prerequisite bridge

BC-PRQ-10001, BC-PRQ-10002, BC-PRQ-10004, BC-PRQ-10007, BC-PRQ-10008, each from its `description_plain` and `failure_signature`, at most 7 words to keep the brief band under its cap.

## Time

Section I Part A, 2.14 minutes for the MCQ shape (research/exam/exam-structure.md#Section and part layout). As a free response part BC-QA-10014 is worth three points, 5.0 minutes, and BC-QA-10013 five points, 8.33 minutes (docs/lessons/unit-10/README.md, section 5). A fluent solver writes the cancelled ratio, its limit and the radius; the restatement of the term and the algebra of the ratio before it is cancelled are held [inferred].

## Checks

- chk-1, completion of ex-1, both bands: the limit is given, the radius is asked. Key 5.
- chk-2, isomorph, both bands, no calculator. Draw: form multiplied, centre 1, base 4, power 2, coefficient 1, start 1, so \(\sum\frac{4^n(x-1)^n}{n^2}\), cancelled ratio \(\frac{4n^2\lvert x-1\rvert}{(n+1)^2}\), limit \(4\lvert x-1\rvert\), key \(\frac14\).
- chk-3, MCQ, low band, no calculator. Draw: form divided, centre 2, base 6, power 2, coefficient 3, start 1, so \(\sum\frac{3n^2(x-2)^n}{6^n}\), key C, \(R=6\). Distractors: A, \(R=1\) from n+1 in the power of \(x-2\) only (BC-ERR-10021); B, \(R=8\) from the ratio without bars, the bound of \(x<8\) reported (BC-ERR-10022); D, the ratio written equal to its limit with the limit symbol left off, which is false since the ratio still carries \(\frac{(n+1)^2}{n^2}\) (BC-ERR-10017).

## Delivery

- pr-1, orientation, ki-1: text. Rule 6: the skills carry BC-REP-11 and 01, none figure-bearing (docs/lessons/unit-10/README.md, section 6). No block is drawn, so the record carries `no_figure_reason`.
- ex-1, ex-2, the four error blocks: step_reveal. Rule 1.

## Band plan

- Low (full): prediction, orientation, bridges, ki-1, st-1 with the contrast pair, st-2, ex-1 and its line, chk-1, the four error blocks, ex-2 (faded from step 3), chk-2, chk-3. 698 words, 4.7 minutes.
- Mid (brief): prediction, orientation, bridges, ki-1, st-1 with the contrast pair, ex-1 and its line, chk-1, err-BC-ERR-10009, err-BC-ERR-10022, chk-2. 436 words, 3.0 minutes.
- Refresher: ki-1, the four error blocks, ex-1.

## Sources

- BC-CON-10012; BC-SKL-10031, BC-SKL-10032, BC-SKL-10033; BC-EK-LIM-7A11; ced:193
- BC-QA-10014, BC-QA-10001, BC-QA-10013; BC-PT-99042, BC-PT-99043, BC-PT-99047
- BC-ERR-10009, BC-ERR-10022, BC-ERR-10017, BC-ERR-10021; BC-MIS-10007, BC-MIS-10014
- BC-PRQ-10001, BC-PRQ-10002, BC-PRQ-10004, BC-PRQ-10007, BC-PRQ-10008
- sg-25:25, sg-22:21, sg-21:24
- research/units/unit-10-infinite-sequences-series.md#10.8 Ratio Test for Convergence
- research/question-analysis/question-archetypes.md#BC-QA-10014 Radius of convergence from a given series
- research/exam/exam-structure.md#Section and part layout
- [inferred] the untagged points on ex-1; the held steps; the p-series stem of the contrast pair; the L equal to 1 case without a worked example. Each settled as the inferred array states.

## Machine record

```json
{
 "id": "LSN-CON-10012",
 "kind": "concept",
 "target_id": "BC-CON-10012",
 "unit": "10",
 "skills": [
  "BC-SKL-10031",
  "BC-SKL-10032",
  "BC-SKL-10033"
 ],
 "prediction": {
  "id": "pr-1",
  "stem": {
   "text": "Predict. At \\(x=5\\), the terms of \\(\\sum_{n=1}^{\\infty}\\frac{2n(x-3)^n}{5^n}\\) are \\(2n(0.4)^n\\). What do the partial sums do?",
   "command_verb": "predict"
  },
  "format": "mcq",
  "options": [
   {
    "id": "A",
    "label": "Settle at a finite value",
    "is_key": true
   },
   {
    "id": "B",
    "label": "Grow without bound",
    "is_key": false
   },
   {
    "id": "C",
    "label": "Swing between two values",
    "is_key": false
   }
  ],
  "resolution": "The ratio of consecutive terms tends to 0.4, below 1. The ratio test reads that limit: below 1 converges, above 1 diverges, exactly 1 gives no conclusion.",
  "sources": [
   "BC-CON-10012",
   "research/units/unit-10-infinite-sequences-series.md#10.8 Ratio Test for Convergence"
  ]
 },
 "no_figure_reason": "No skill carries a figure-bearing representation (the topic names series and symbolic forms) and no key idea describes a process, since the test is a ratio, a limit and a comparison with 1.",
 "orientation": {
  "text": "The ratio test compares consecutive terms in the limit. A response writes the ratio with \\(n+1\\) put in everywhere, its limit with limit notation, and what that limit gives against 1.",
  "sources": [
   "BC-CON-10012",
   "research/units/unit-10-infinite-sequences-series.md#10.8 Ratio Test for Convergence"
  ]
 },
 "key_ideas": [
  {
   "id": "ki-1",
   "ek_id": "BC-EK-LIM-7A11",
   "depth": "core",
   "text": "Let \\(L=\\lim_{n\\to\\infty}\\left\\lvert\\frac{a_{n+1}}{a_n}\\right\\rvert\\). If \\(L<1\\) the series converges absolutely, if \\(L>1\\) it diverges, and if \\(L=1\\) the test gives no information. Every \\(n\\) becomes \\(n+1\\), including inside exponents. The limit is written with limit notation.",
   "notation": "limit of the ratio; L less than one",
   "quote": null,
   "sources": [
    "BC-EK-LIM-7A11",
    "ced:193",
    "sg-25:25",
    "sg-22:21",
    "research/units/unit-10-infinite-sequences-series.md#10.8 Ratio Test for Convergence"
   ]
  }
 ],
 "strategy": [
  {
   "id": "st-1",
   "archetype_id": "BC-QA-10014",
   "cue": "A power series in sigma notation; the radius is asked.",
   "method": "\\(\\left\\lvert\\frac{a_{n+1}}{a_n}\\right\\rvert\\) with \\(n+1\\) put in everywhere, then its limit.",
   "rival": "No absolute values, or \\(n\\) replaced in some places only.",
   "separating_feature": "Exponentials or factorials in \\(n\\), not a fixed power alone.",
   "sources": [
    "BC-QA-10014"
   ],
   "evidence_tag": "verified",
   "contrast": {
    "this": {
     "text": "Use the ratio test to find the radius of convergence of \\(\\sum_{n=1}^{\\infty}\\frac{3n(x-2)^n}{4^n}\\).",
     "archetype_id": "BC-QA-10014"
    },
    "not_this": {
     "text": "Use the ratio test to determine whether \\(\\sum_{n=1}^{\\infty}\\frac{1}{n^2}\\) converges.",
     "why_not": "The ratio tends to 1, where the test says nothing; the p-series test decides."
    },
    "feature": "A fixed power of \\(n\\) gives a ratio near 1; an exponential or factorial does not."
   }
  },
  {
   "id": "st-2",
   "archetype_id": "BC-QA-10001",
   "cue": "A series of numbers with a factorial or an nth power.",
   "method": "The ratio, its limit \\(L\\), then \\(L<1\\), \\(L>1\\) or \\(L=1\\), naming the series in the verdict.",
   "rival": "Reading \\(L=1\\) as convergence.",
   "separating_feature": "Only \\(L=1\\) settles nothing.",
   "sources": [
    "BC-QA-10001"
   ],
   "evidence_tag": "verified"
  }
 ],
 "worked_examples": [
  {
   "id": "ex-1",
   "archetype_id": "BC-QA-10014",
   "bands": [
    "low",
    "mid"
   ],
   "parameter_draw": {
    "form": "divided",
    "centre": "3",
    "base": "5",
    "power": "1",
    "coefficient": "2",
    "start": "1"
   },
   "problem": {
    "text": "Find the radius of convergence of the power series \\(\\sum_{n=1}^{\\infty}\\frac{2n(x-3)^n}{5^n}\\).",
    "command_verb": "find"
   },
   "calculator_status": "no_calculator",
   "steps": [
    {
     "cue": "General term \\(a_n=\\frac{2n(x-3)^n}{5^n}\\).",
     "why": "The ratio test needs \\(a_n\\).",
     "expr": "2*n*(x-3)**n/5**n",
     "relation": "new"
    },
    {
     "cue": "Form \\(\\left\\lvert\\frac{a_{n+1}}{a_n}\\right\\rvert\\) and cancel.",
     "why": "Put \\(n+1\\) in every \\(n\\).",
     "expr": "(n+1)*Abs(x-3)/(5*n)",
     "relation": "new",
     "point_type_id": "BC-PT-99042"
    },
    {
     "cue": "Take \\(n\\to\\infty\\).",
     "why": "\\(\\frac{n+1}{n}\\to1\\).",
     "expr": "Abs(x-3)/5",
     "relation": "limit",
     "variable": "n",
     "point": "oo"
    },
    {
     "cue": "Set \\(L<1\\): \\(\\lvert x-3\\rvert<5\\).",
     "why": "The bound is the radius.",
     "expr": "5",
     "relation": "new"
    }
   ],
   "answer": {
    "form": "numeric",
    "expr": "5"
   }
  },
  {
   "id": "ex-2",
   "archetype_id": "BC-QA-10001",
   "bands": [
    "low"
   ],
   "parameter_draw": {
    "form": "ratio_factorial",
    "power": "2",
    "coefficient": "3",
    "start": "1",
    "lead_top": "2",
    "constant_top": "3",
    "lead_bottom": "2",
    "constant_bottom": "3",
    "ratio": "1/2",
    "base": "5",
    "degree": "2"
   },
   "fade_from": 3,
   "problem": {
    "text": "Determine whether the series \\(\\sum_{n=1}^{\\infty} a_n\\), where \\(a_n=\\frac{5^n}{n!}\\), converges or diverges. Name a test whose conditions the series meets and state the verdict it gives.",
    "command_verb": "determine"
   },
   "calculator_status": "no_calculator",
   "steps": [
    {
     "cue": "A factorial in the term: the ratio test fits.",
     "why": "Factorials cancel in a ratio.",
     "expr": "5**n/factorial(n)",
     "relation": "new"
    },
    {
     "cue": "Form \\(\\left\\lvert\\frac{a_{n+1}}{a_n}\\right\\rvert\\).",
     "why": "Put \\(n+1\\) in every \\(n\\).",
     "expr": "(5**(n+1)/factorial(n+1))/(5**n/factorial(n))",
     "relation": "new"
    },
    {
     "cue": "Cancel.",
     "why": "\\(\\frac{(n+1)!}{n!}=n+1\\) and \\(\\frac{5^{n+1}}{5^n}=5\\).",
     "expr": "5/(n+1)",
     "relation": "equivalent"
    },
    {
     "cue": "Take \\(n\\to\\infty\\).",
     "why": "The denominator grows without bound.",
     "expr": "0",
     "relation": "limit",
     "variable": "n",
     "point": "oo"
    },
    {
     "cue": "Compare \\(L\\) with 1, naming the series.",
     "why": "\\(L=0<1\\), so \\(\\sum a_n\\) converges by the ratio test."
    }
   ],
   "answer": {
    "form": "statement",
    "expr": "converges by the ratio test, L = 0 < 1"
   }
  }
 ],
 "what_a_reader_scores": [
  {
   "example_id": "ex-1",
   "point_type_ids": [
    "BC-PT-99042"
   ],
   "lines": [
    {
     "point_type_id": "BC-PT-99042",
     "text": "Ratio setup for the ratio test. Earned by: A correct ratio of consecutive terms, with or without absolute values (sg-25:25, sg-22:21). Not earned by: A response that presents no ratio at all, which sg-25:25 states leaves the limit point unavailable."
    }
   ]
  }
 ],
 "common_errors": [
  {
   "error_id": "BC-ERR-10009",
   "observed_behavior": "The response names a convergence test and states a conclusion without establishing the conditions the test requires.",
   "scoring_consequence": "Points tied to the conditions or to the justification are lost even when the verdict is right (sg-21:22).",
   "wrong_step": {
    "text": "The ratio test converges.",
    "expr": "Abs(x-3)/5"
   },
   "right_step": {
    "text": "\\(L=\\frac{\\lvert x-3\\rvert}{5}\\), then \\(L<1\\).",
    "expr": "Abs(x-3)/5"
   },
   "relation": "equivalent",
   "possible_reason": {
    "misconception_id": "BC-MIS-10007",
    "text": "treats the name of a test as the argument"
   },
   "sources": [
    "BC-ERR-10009",
    "BC-MIS-10007"
   ],
   "fix_prompt": false
  },
  {
   "error_id": "BC-ERR-10022",
   "observed_behavior": "The response forms and evaluates the ratio of consecutive terms without absolute value bars.",
   "scoring_consequence": "A ratio without absolute values still earns the setup and limit points, but the interior point then requires the inequality to be resolved without error (sg-25:25).",
   "wrong_step": {
    "text": "No bars: \\(\\frac{(n+1)(x-3)}{5n}\\).",
    "expr": "(n+1)*(x-3)/(5*n)"
   },
   "right_step": {
    "text": "With bars: \\(\\frac{(n+1)\\lvert x-3\\rvert}{5n}\\).",
    "expr": "(n+1)*Abs(x-3)/(5*n)"
   },
   "relation": "distinct",
   "possible_reason": null,
   "sources": [
    "BC-ERR-10022"
   ],
   "fix_prompt": true
  },
  {
   "error_id": "BC-ERR-10017",
   "observed_behavior": "The response computes the value of a ratio or a quotient as the index grows without writing the limit symbol.",
   "scoring_consequence": "Limit notation is required for the setup point in a limit comparison (sg-21:23) and for the limit point in a ratio test (sg-25:25).",
   "wrong_step": {
    "text": "\\(\\left\\lvert\\frac{a_{n+1}}{a_n}\\right\\rvert=\\frac{\\lvert x-3\\rvert}{5}\\).",
    "expr": "Abs(x-3)/5"
   },
   "right_step": {
    "text": "\\(\\lim_{n\\to\\infty}\\left\\lvert\\frac{a_{n+1}}{a_n}\\right\\rvert=\\frac{\\lvert x-3\\rvert}{5}\\).",
    "expr": "Abs(x-3)/5"
   },
   "relation": "equivalent",
   "possible_reason": null,
   "sources": [
    "BC-ERR-10017"
   ],
   "fix_prompt": false
  },
  {
   "error_id": "BC-ERR-10021",
   "observed_behavior": "The response replaces n by n plus one in some places and not others, for example writing an exponent of two n plus two where two n plus three is required.",
   "scoring_consequence": "A substitution error of this kind keeps the early points but blocks the final interval point (sg-22:21).",
   "wrong_step": {
    "text": "\\(n+1\\) in the power of \\(x-3\\) only: \\(\\frac{(n+1)\\lvert x-3\\rvert}{n}\\).",
    "expr": "(n+1)*Abs(x-3)/n"
   },
   "right_step": {
    "text": "\\(n+1\\) in every place: \\(\\frac{(n+1)\\lvert x-3\\rvert}{5n}\\).",
    "expr": "(n+1)*Abs(x-3)/(5*n)"
   },
   "relation": "distinct",
   "possible_reason": {
    "misconception_id": "BC-MIS-10014",
    "text": "applies the ratio test where its limit gives nothing"
   },
   "sources": [
    "BC-ERR-10021",
    "BC-MIS-10014"
   ],
   "fix_prompt": true
  }
 ],
 "representations": null,
 "prerequisite_bridges": [
  {
   "prq_id": "BC-PRQ-10001",
   "text": "\\(\\lvert x-3\\rvert<5\\) is a two-sided inequality."
  },
  {
   "prq_id": "BC-PRQ-10002",
   "text": "\\(\\frac{(n+1)!}{n!}\\) is \\(n+1\\)."
  },
  {
   "prq_id": "BC-PRQ-10004",
   "text": "Dominant terms decide limits in \\(n\\)."
  },
  {
   "prq_id": "BC-PRQ-10007",
   "text": "Quotients of powers subtract exponents."
  },
  {
   "prq_id": "BC-PRQ-10008",
   "text": "Read \\(a_n\\) out of the sigma form."
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
   ],
   "ex-2": [
    2,
    4,
    5
   ]
  },
  "skipped_steps": {
   "ex-1": [
    1
   ],
   "ex-2": [
    1,
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
   "archetype_id": "BC-QA-10014",
   "parameter_draw": {
    "form": "divided",
    "centre": "3",
    "base": "5",
    "power": "1",
    "coefficient": "2",
    "start": "1"
   },
   "completes": "ex-1",
   "stem": {
    "text": "\\(\\lim_{n\\to\\infty}\\left\\lvert\\frac{a_{n+1}}{a_n}\\right\\rvert=\\frac{\\lvert x-3\\rvert}{5}\\). State the radius of convergence.",
    "command_verb": "state"
   },
   "key": {
    "form": "numeric",
    "expr": "5"
   },
   "steps": [
    {
     "text": "Set the limit below 1.",
     "expr": "5",
     "relation": "new"
    }
   ],
   "calculator_status": "no_calculator",
   "skills": [
    "BC-SKL-10032"
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
   "archetype_id": "BC-QA-10014",
   "parameter_draw": {
    "form": "multiplied",
    "centre": "1",
    "base": "4",
    "power": "2",
    "coefficient": "1",
    "start": "1"
   },
   "stem": {
    "text": "Find the radius of convergence of \\(\\sum_{n=1}^{\\infty}\\frac{4^n(x-1)^n}{n^2}\\).",
    "command_verb": "find"
   },
   "key": {
    "form": "numeric",
    "expr": "1/4"
   },
   "steps": [
    {
     "text": "The ratio of consecutive terms, cancelled.",
     "expr": "4*n**2*Abs(x-1)/(n+1)**2",
     "relation": "new"
    },
    {
     "text": "Its limit.",
     "expr": "4*Abs(x-1)",
     "relation": "limit",
     "variable": "n",
     "point": "oo"
    },
    {
     "text": "Set the limit below 1.",
     "expr": "1/4",
     "relation": "new"
    }
   ],
   "calculator_status": "no_calculator",
   "skills": [
    "BC-SKL-10031",
    "BC-SKL-10032"
   ]
  },
  {
   "id": "chk-3",
   "check_kind": "mcq",
   "format": "mcq",
   "bands": [
    "low"
   ],
   "archetype_id": "BC-QA-10014",
   "parameter_draw": {
    "form": "divided",
    "centre": "2",
    "base": "6",
    "power": "2",
    "coefficient": "3",
    "start": "1"
   },
   "stem": {
    "text": "Use the ratio test to find the radius of convergence of \\(\\sum_{n=1}^{\\infty}\\frac{3n^2(x-2)^n}{6^n}\\). The complete result is",
    "command_verb": "identify"
   },
   "key": {
    "form": "statement",
    "expr": "R = 6, from the limit of the absolute ratio |x-2|/6"
   },
   "steps": [
    {
     "text": "The ratio of consecutive terms, cancelled.",
     "expr": "(n+1)**2*Abs(x-2)/(6*n**2)",
     "relation": "new"
    },
    {
     "text": "Its limit.",
     "expr": "Abs(x-2)/6",
     "relation": "limit",
     "variable": "n",
     "point": "oo"
    },
    {
     "text": "Set the limit below 1.",
     "expr": "6",
     "relation": "new"
    }
   ],
   "options": [
    {
     "id": "A",
     "is_key": false,
     "label": "\\(R=1\\), from \\(\\lim_{n\\to\\infty}\\frac{(n+1)^2\\lvert x-2\\rvert}{n^2}=\\lvert x-2\\rvert\\).",
     "error_path": "BC-ERR-10021",
     "derivation": "n replaced by n + 1 in the power of the displacement but not in 6^n, so the radius comes out as 1"
    },
    {
     "id": "B",
     "is_key": false,
     "label": "\\(R=8\\), from \\(\\lim_{n\\to\\infty}\\frac{(n+1)^2(x-2)}{6n^2}<1\\), that is \\(x<8\\).",
     "error_path": "BC-ERR-10022",
     "derivation": "the ratio test done without absolute values, so the inequality became x < 8 and that bound was reported as the radius"
    },
    {
     "id": "C",
     "is_key": true,
     "label": "\\(R=6\\), from \\(\\lim_{n\\to\\infty}\\left\\lvert\\frac{a_{n+1}}{a_n}\\right\\rvert=\\frac{\\lvert x-2\\rvert}{6}<1\\)."
    },
    {
     "id": "D",
     "is_key": false,
     "label": "\\(R=6\\), from \\(\\left\\lvert\\frac{a_{n+1}}{a_n}\\right\\rvert=\\frac{\\lvert x-2\\rvert}{6}<1\\).",
     "error_path": "BC-ERR-10017",
     "derivation": "the ratio written equal to its limit, with the limit symbol left off, though the ratio still carries the factor (n+1)^2 over n^2"
    }
   ],
   "calculator_status": "no_calculator",
   "skills": [
    "BC-SKL-10031",
    "BC-SKL-10032"
   ]
  }
 ],
 "delivery": [
  {
   "block": "pr-1",
   "mode": "text",
   "reason": "rule 6: the question is about terms of a power series at one input, symbolic and verbal forms, none figure-bearing",
   "sources": [
    "BC-CON-10012"
   ]
  },
  {
   "block": "orientation",
   "mode": "text",
   "reason": "rule 6: a statement of what a response shows",
   "sources": [
    "BC-CON-10012"
   ]
  },
  {
   "block": "ki-1",
   "mode": "text",
   "reason": "rule 6: BC-REP-11, 01 on BC-SKL-10031 to 10033, none figure-bearing; the idea is a ratio, a limit and three cases, not a process",
   "sources": [
    "BC-SKL-10031",
    "BC-SKL-10032",
    "BC-SKL-10033"
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
   "block": "err-BC-ERR-10009",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  },
  {
   "block": "err-BC-ERR-10022",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  },
  {
   "block": "err-BC-ERR-10017",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  },
  {
   "block": "err-BC-ERR-10021",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  }
 ],
 "refresher": [
  "ki-1",
  "err-BC-ERR-10009",
  "err-BC-ERR-10022",
  "err-BC-ERR-10017",
  "err-BC-ERR-10021",
  "ex-1"
 ],
 "research_lines": [
  {
   "file": "research/units/unit-10-infinite-sequences-series.md",
   "line": "Every occurrence of the index must be replaced, including inside an exponent such as two n plus one (sg-22:21)."
  }
 ],
 "inferred": [
  {
   "claim": "ex-1 tags BC-PT-99042 only. The limit point BC-PT-99043 and the radius point BC-PT-99047 of BC-QA-10014 are taught in ex-1's steps but untagged, because their reader lines (83 and 51 words) would take the brief band past its cap; ex-2 is on BC-QA-10001, which lists no point types.",
   "settles": "A brief cap that admits the reader lines, or shorter BC-PT-99043 and BC-PT-99047 lines."
  },
  {
   "claim": "A fluent solver writes the cancelled ratio, its limit and the radius, and on the factorial series the ratio, the limit and the verdict; the restatement of the term and the cancellation are held.",
   "settles": "Timing data per step once the fluency telemetry exists."
  },
  {
   "claim": "The p-series stem in the contrast pair is a stem shaped like a BC-QA-10001 p-series form, chosen so the ratio tends to 1; it is not a published item.",
   "settles": "A check of the stem against the published items on BC-QA-10001."
  },
  {
   "claim": "The L equals 1 case of skill BC-SKL-10033 is carried by ki-1, the prediction resolution and the contrast pair and by no worked example, since BC-QA-10001 has no ratio draw that gives L equal to 1.",
   "settles": "A BC-QA-10001 form or a BC-QA-10013 draw whose ratio limit is 1."
  }
 ],
 "sources": [
  "BC-CON-10012",
  "BC-SKL-10031",
  "BC-SKL-10032",
  "BC-SKL-10033",
  "BC-EK-LIM-7A11",
  "ced:193",
  "BC-QA-10014",
  "BC-QA-10001",
  "BC-QA-10013",
  "BC-PT-99042",
  "BC-PT-99043",
  "BC-PT-99047",
  "BC-ERR-10009",
  "BC-ERR-10022",
  "BC-ERR-10017",
  "BC-ERR-10021",
  "BC-MIS-10014",
  "BC-PRQ-10001",
  "BC-PRQ-10002",
  "BC-PRQ-10004",
  "BC-PRQ-10007",
  "BC-PRQ-10008",
  "sg-25:25",
  "sg-22:21",
  "sg-21:24",
  "research/units/unit-10-infinite-sequences-series.md#10.8 Ratio Test for Convergence",
  "research/question-analysis/question-archetypes.md#BC-QA-10014 Radius of convergence from a given series",
  "research/exam/exam-structure.md#Section and part layout"
 ],
 "word_count": {
  "full": 698,
  "brief": 436
 },
 "read_minutes": {
  "full": 4.7,
  "brief": 3.0
 }
}
```
