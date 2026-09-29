---
title: LSN-CON-10020 Power series and their centre
research_date: 2026-09-29
status: designed
purpose: Authoring spec for the concept lesson on BC-CON-10020, the form of a power series in powers of x minus a fixed number and the reading of that number as its centre, built from authoring_bundle("BC-CON-10020") and the research files it cites, so an author fills plan 15's lesson record without making a teaching decision.
---

# LSN-CON-10020 Power series and their centre

## Prediction

Served first, both bands: an `mcq` on ex-1's series. Each term has the factor (x + 2)^n, and the student picks the x at which every term is 0: 2, -2 or 0. Key B, -2. The student settles it by substitution before any rule: at x = 2 the terms are 1/n, and at x = 0 they are 2^n/(4^n n), both nonzero. The resolution ties the zero of the factor to the centre, with no verdict word. Source: BC-CON-10020 and the topic 10.13 section the key idea cites.

## Orientation

Served text from BC-CON-10020 `description_plain` (a power series is built from powers of x minus a fixed number) and the topic's Assessment behaviour paragraph (the opening FRQ part is the interval or the radius of a given power series, no calculator, and the ratio and interior points depend on the series read correctly). The orientation states what a response shows: the centre from the base, the coefficients apart from the powers. No count, no frequency.

## Key ideas

One core block. BC-SKL-10053 maps one essential knowledge statement, BC-EK-LIM-8D1 (ced:198), so one key idea serves both bands. It paraphrases the Power series paragraph (the form, the centre r). Notation line: the concept's `notation`. No anchor quote: the CED sentence is garbled in the cached page and the paraphrase carries it.

## Recognition

Two archetypes load BC-SKL-10053, both family radius-interval and both `no_calculator`.

- BC-QA-10013 `common_givens`: "a power series with its general term", "the centre of the series", "an instruction to use the ratio test". Official examples BC-FRQ-2012-Q6-A, 2022-Q6-A, 2025-Q6-A, 2018-Q6-B.
- BC-QA-10014 `common_givens`: "a Maclaurin or Taylor series in sigma notation". Official examples BC-FRQ-2021-Q6-C, 2014-Q6-A, 2015-Q6-A, 2024-Q6-D.

What says this concept: a variable x inside a base of the form x minus a number, raised to n. What says not this concept: a series of numbers with no variable, which is tested for convergence or divergence and has no centre (BC-CON-10012 and BC-QA-10004, docs/lessons/unit-10/README.md, section 3). The near miss of the contrast pair is a numerical ratio test stem from BC-QA-10004.

## Method choice

- st-1, BC-QA-10013, inferred. Cue from `common_givens`. Method: read the centre, then `expected_solution_path[0]`, the ratio. Rival: the centre read with the wrong sign [inferred, no record names it]. Feature: the centre is r in x minus r. The block carries the contrast pair.
- st-2, BC-QA-10014, low band only, inferred. Cue from `asked_to_produce`, method the path from the ratio to the radius with the centre read first, rival from `wrong_approaches` (an interval where the radius was asked, BC-ERR-10036), feature that a radius is a distance from the centre.

## Solution path

- ex-1, BC-QA-10013, both bands, no calculator. Draw: power 1, sign positive, centre -2, radius 4, coefficient 1, start 1, so the series is the sum from n = 1 of (x + 2)^n / (4^n n). Ratio, limit |x + 2|/4 (SymPy), interior (-6, 2). The stem asks for the interior only, since the endpoint work belongs to BC-CON-10022. No published item on BC-QA-10013 carries this draw (draw_exclusion).
- ex-2, low band, faded from step 3, BC-QA-10014. Draw: form divided, centre 3, base 5, power 1, coefficient 1, start 1, so n (x - 3)^n / 5^n, radius 5. Steps 1 and 2 (the centre and the ratio) are shown, the student writes the radius, and steps 3 and 4 then reveal. The fade falls there because the reading and the ratio repeat ex-1 and the limit and the radius are what the student must produce.
- Steps: the centre (new), the ratio (new), the limit (limit), the interior or radius (new). A fluent solver writes the ratio, the limit and the interior, and holds the reading of the centre (Time). No productive-failure comparison.

## Scoring

BC-QA-10013 lists BC-PT-99042 to 99046 and BC-QA-10014 lists 99042, 99043 and 99047. ex-1 tags BC-PT-99044, the interior, the point that rests on reading the centre and radius; its ratio and limit lines are dropped to fit the brief cap (inferred array). ex-2 tags BC-PT-99042, 99043 and 99047. No listed point type scores the reading of the centre itself. The lines are `reader_checks` output.

Point losses from research: the bare absolute value form is not sufficient for the interior (BC-PT-99044, sg-25:25); an interval presented where the radius was asked does not earn the radius point (BC-PT-99047, sg-21:24).

## Traps

One active error meets BC-SKL-10053, BC-ERR-10034 (also held by BC-SKL-10057 and 10066). One block on ex-1's draw, `fix_prompt` true: the left endpoint x = -6 gives (-4)^n / (4^n n) = (-1)^n / n, and the wrong step drops the alternating factor the negative endpoint produces. No possible reason line (brief band words). Check 3's three distractors all carry BC-ERR-10034 (see the inferred array).

## Representations

None. The topic's Representations paragraph names BC-REP-11, 01 and 04 and the conversions power series to ratio, inequality to interval, endpoint value to numerical series; nothing figure-shaped.

## Prerequisite bridge

- BC-PRQ-10008, from its `description_plain` and `failure_signature`.

## Time

The MCQ shape is Section I Part A, 2.14 minutes (research/exam/exam-structure.md#Section and part layout). As a free response part, 5 points, 8.33 minutes for BC-QA-10013 and 3 points, 5.0 minutes for BC-QA-10014 (docs/lessons/unit-10/README.md, section 5). A fluent solver writes the ratio, the limit and the interior, and holds the reading of the centre and the algebra of the ratio [inferred]. The minutes go on the ratio and its limit.

## Checks

- chk-1, completion of ex-1, both bands: the limit given, the interior asked. Key (-6, 2).
- chk-2, isomorph, both bands (BC-QA-10013). Draw: power 1, sign positive, centre 3, radius 2, coefficient 1, start 1, so (x - 3)^n / (2^n n), key (1, 5).
- chk-3, MCQ, low band. Draw: power 1, sign positive, centre 1, radius 3, coefficient 1, start 1. The third term of the left endpoint series at x = -2, key -1/3. Distractors: 1/3 (the alternating factor dropped), -9/8 (endpoint substituted for the index), 9/8 (both slips), each BC-ERR-10034.

## Delivery

- pr-1, orientation, ki-1: text. Rule 6, BC-REP-11 and 01 on BC-SKL-10053, neither figure-bearing, and the unit README delivery map names text. The record carries `no_figure_reason`.
- ex-1, ex-2, err-BC-ERR-10034: step_reveal. Rule 1.

## Band plan

- Low (full): prediction, orientation, bridge, ki-1, st-1 with the contrast pair, st-2, ex-1 and its line, chk-1, the error block, ex-2 (faded from step 3) and its lines, chk-2, chk-3. 693 words, 4.7 minutes.
- Mid (brief): prediction, orientation, bridge, ki-1, st-1 with the contrast pair, ex-1 and its line, chk-1, the error block, chk-2. 416 words, 2.8 minutes.
- Refresher: ki-1, err-BC-ERR-10034, ex-1.

## Sources

- BC-CON-10020; BC-SKL-10053; BC-EK-LIM-8D1; ced:198
- BC-QA-10013; BC-QA-10014; BC-QA-10004; BC-PT-99042, BC-PT-99043, BC-PT-99044, BC-PT-99047
- BC-ERR-10034
- BC-PRQ-10008
- sg-25:25, sg-21:24
- research/units/unit-10-infinite-sequences-series.md#10.13 Radius and Interval of Convergence of Power Series
- research/question-analysis/question-archetypes.md#BC-QA-10013 Interval of convergence by the ratio test with endpoint analysis
- research/question-analysis/question-archetypes.md#BC-QA-10014 Radius of convergence from a given series
- research/exam/exam-structure.md#Section and part layout
- [inferred] the centre-first method and its rival, the three distractors on one error, the held steps, the untagged ratio and limit lines on ex-1. Each settled as the inferred array states.

## Machine record

```json
{
 "id": "LSN-CON-10020",
 "kind": "concept",
 "target_id": "BC-CON-10020",
 "unit": "10",
 "skills": [
  "BC-SKL-10053"
 ],
 "prediction": {
  "id": "pr-1",
  "stem": {
   "text": "Each term of \\(\\sum_{n=1}^{\\infty}\\frac{(x+2)^n}{4^n n}\\) has the factor \\((x+2)^n\\). Predict the \\(x\\) at which every term equals 0.",
   "command_verb": "predict"
  },
  "format": "mcq",
  "options": [
   {
    "id": "A",
    "label": "\\(x\\) equals 2",
    "is_key": false
   },
   {
    "id": "B",
    "label": "\\(x\\) equals negative 2",
    "is_key": true
   },
   {
    "id": "C",
    "label": "\\(x\\) equals 0",
    "is_key": false
   }
  ],
  "resolution": "\\((x+2)^n\\) is 0 at \\(x=-2\\). The series is written in powers of \\(x-(-2)\\), so its centre is \\(-2\\).",
  "sources": [
   "BC-CON-10020",
   "research/units/unit-10-infinite-sequences-series.md#10.13 Radius and Interval of Convergence of Power Series"
  ]
 },
 "no_figure_reason": "The skill carries series and symbolic representations, neither figure-bearing, and the key idea is a form and a reading of its centre, not a process.",
 "orientation": {
  "text": "A power series is built from powers of \\(x-r\\) for a fixed number \\(r\\), its centre. A response names the centre from the base, reading \\(x+2\\) as centre \\(-2\\), and keeps the coefficients apart from the powers.",
  "sources": [
   "BC-CON-10020",
   "research/units/unit-10-infinite-sequences-series.md#10.13 Radius and Interval of Convergence of Power Series"
  ]
 },
 "key_ideas": [
  {
   "id": "ki-1",
   "ek_id": "BC-EK-LIM-8D1",
   "depth": "core",
   "text": "A power series has the form \\(\\sum a_n(x-r)^n\\), with \\(a_n\\) real and \\(r\\) the centre. The centre is the number subtracted from \\(x\\), so \\((x+2)^n\\) has centre \\(-2\\). The coefficients \\(a_n\\) are read apart from the powers.",
   "notation": "centre \\(r\\); coefficients \\(a_n\\)",
   "quote": null,
   "sources": [
    "BC-EK-LIM-8D1",
    "ced:198",
    "research/units/unit-10-infinite-sequences-series.md#10.13 Radius and Interval of Convergence of Power Series"
   ]
  }
 ],
 "strategy": [
  {
   "id": "st-1",
   "archetype_id": "BC-QA-10013",
   "cue": "A series in powers of \\(x-r\\), with the ratio test asked.",
   "method": "Read the centre from the base, then form the ratio of consecutive terms.",
   "rival": "The centre read with the wrong sign.",
   "separating_feature": "The centre is \\(r\\) in \\(x-r\\), so \\(x+2\\) has centre \\(-2\\).",
   "sources": [
    "BC-QA-10013"
   ],
   "evidence_tag": "inferred",
   "contrast": {
    "this": {
     "text": "Find the interval of convergence of \\(\\sum_{n=1}^{\\infty}\\frac{(x-1)^n}{5^n n}\\) using the ratio test.",
     "archetype_id": "BC-QA-10013"
    },
    "not_this": {
     "text": "Use the ratio test to decide whether \\(\\sum_{n=1}^{\\infty}\\frac{2^n}{5^n n}\\) converges.",
     "why_not": "It has no variable and no centre, and the answer is converges or diverges."
    },
    "feature": "A power series has \\(x\\) inside \\((x-r)^n\\), and a numerical series has none."
   }
  },
  {
   "id": "st-2",
   "archetype_id": "BC-QA-10014",
   "cue": "A power series in sigma notation with the radius asked.",
   "method": "Read the centre, form the ratio, take its limit, then state the radius.",
   "rival": "An interval given where the radius was asked.",
   "separating_feature": "The radius is a distance from the centre, not an endpoint.",
   "sources": [
    "BC-QA-10014"
   ],
   "evidence_tag": "inferred"
  }
 ],
 "worked_examples": [
  {
   "id": "ex-1",
   "archetype_id": "BC-QA-10013",
   "bands": [
    "low",
    "mid"
   ],
   "parameter_draw": {
    "power": "1",
    "sign": "positive",
    "centre": -2,
    "radius": 4,
    "coefficient": 1,
    "start": 1
   },
   "problem": {
    "text": "Use the ratio test to find the interior of the interval of convergence of \\(\\sum_{n=1}^{\\infty}\\frac{(x+2)^n}{4^n n}\\).",
    "command_verb": "find"
   },
   "calculator_status": "no_calculator",
   "steps": [
    {
     "cue": "The base is \\(x+2=x-(-2)\\).",
     "why": "So the centre is \\(-2\\).",
     "expr": "-2",
     "relation": "new"
    },
    {
     "cue": "Ratio of consecutive terms, \\(n+1\\) throughout.",
     "why": "The ratio test compares neighbours.",
     "expr": "Abs(x + 2)*n/(4*(n + 1))",
     "relation": "new"
    },
    {
     "cue": "Limit as \\(n\\to\\infty\\).",
     "why": "\\(\\frac{n}{n+1}\\to1\\).",
     "expr": "Abs(x + 2)/4",
     "relation": "limit",
     "variable": "n",
     "point": "oo",
     "dir": "-"
    },
    {
     "cue": "Solve \\(\\frac{|x+2|}{4}<1\\).",
     "why": "The interior is the centre plus and minus 4.",
     "expr": "Interval(-6, 2, True, True)",
     "relation": "new",
     "point_type_id": "BC-PT-99044"
    }
   ],
   "answer": {
    "form": "symbolic",
    "expr": "Interval(-6, 2, True, True)"
   }
  },
  {
   "id": "ex-2",
   "archetype_id": "BC-QA-10014",
   "bands": [
    "low"
   ],
   "fade_from": 3,
   "parameter_draw": {
    "form": "divided",
    "centre": 3,
    "base": 5,
    "power": 1,
    "coefficient": 1,
    "start": 1
   },
   "problem": {
    "text": "Read the centre of \\(\\sum_{n=1}^{\\infty}\\frac{n(x-3)^n}{5^n}\\), then find its radius of convergence.",
    "command_verb": "find"
   },
   "calculator_status": "no_calculator",
   "steps": [
    {
     "cue": "The base is \\(x-3\\).",
     "why": "So the centre is 3.",
     "expr": "3",
     "relation": "new"
    },
    {
     "cue": "Ratio of consecutive terms.",
     "why": "Put \\(n+1\\) in every place \\(n\\) appears.",
     "expr": "(n + 1)*Abs(x - 3)/(5*n)",
     "relation": "new",
     "point_type_id": "BC-PT-99042"
    },
    {
     "cue": "Limit as \\(n\\to\\infty\\).",
     "why": "\\(\\frac{n+1}{n}\\to1\\).",
     "expr": "Abs(x - 3)/5",
     "relation": "limit",
     "variable": "n",
     "point": "oo",
     "dir": "-",
     "point_type_id": "BC-PT-99043"
    },
    {
     "cue": "Solve \\(\\frac{|x-3|}{5}<1\\).",
     "why": "The radius is the distance from the centre.",
     "expr": "5",
     "relation": "new",
     "point_type_id": "BC-PT-99047"
    }
   ],
   "answer": {
    "form": "numeric",
    "expr": "5"
   }
  }
 ],
 "what_a_reader_scores": [
  {
   "example_id": "ex-1",
   "point_type_ids": [
    "BC-PT-99044"
   ],
   "lines": [
    {
     "point_type_id": "BC-PT-99044",
     "text": "Interior of the interval of convergence. Earned by: Resolving the inequality to a two-sided inequality or an interval for the variable (sg-25:25, sg-22:21). Not earned by: An absolute value inequality left unresolved; sg-25:25 states the bare form with the centre and radius is not sufficient unless it is resolved to a two-sided inequality, and sg-22:21 states a one-sided bound is insufficient."
    }
   ]
  },
  {
   "example_id": "ex-2",
   "point_type_ids": [
    "BC-PT-99042",
    "BC-PT-99043",
    "BC-PT-99047"
   ],
   "lines": [
    {
     "point_type_id": "BC-PT-99042",
     "text": "Ratio setup for the ratio test. Earned by: A correct ratio of consecutive terms, with or without absolute values (sg-25:25, sg-22:21). Not earned by: A response that presents no ratio at all, which sg-25:25 states leaves the limit point unavailable."
    },
    {
     "point_type_id": "BC-PT-99043",
     "text": "Limit of the ratio. Earned by: Correct evaluation of the limit of the ratio, including correct limit notation (sg-22:21, sg-21:24). Not earned by: Any error in simplification or evaluation of the limit, which sg-25:25 states forfeits this point even when the ratio point stands. Notation: sg-22:21 requires correct limit notation and either the absolute value of the ratio or a resolution to a squared inequality; sg-25:25 states a response not using absolute value can still earn both the ratio and the limit points."
    },
    {
     "point_type_id": "BC-PT-99047",
     "text": "Radius of convergence stated explicitly. Earned by: An explicit statement of the radius, obtained either from the ratio test inequality or by citing the radius of a related series (sg-21:24, sg-24:22). Not earned by: An interval presented with no identification of the radius, which sg-21:24 states does not earn the point."
    }
   ]
  }
 ],
 "common_errors": [
  {
   "error_id": "BC-ERR-10034",
   "observed_behavior": "The response substitutes the endpoint for the index rather than for the variable, or drops the alternating factor produced by a negative endpoint.",
   "scoring_consequence": "The endpoint series is wrong, so the analysis and interval points are lost (sg-25:25).",
   "wrong_step": {
    "text": "Left endpoint series \\(\\sum\\frac{1}{n}\\).",
    "expr": "1/n"
   },
   "right_step": {
    "text": "Left endpoint series \\(\\sum\\frac{(-1)^n}{n}\\).",
    "expr": "(-1)**n/n"
   },
   "relation": "distinct",
   "fix_prompt": true,
   "possible_reason": null,
   "sources": [
    "BC-ERR-10034"
   ]
  }
 ],
 "representations": null,
 "prerequisite_bridges": [
  {
   "prq_id": "BC-PRQ-10008",
   "text": "Substitute into the variable, not the index, and keep the alternating factor."
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
   "archetype_id": "BC-QA-10013",
   "parameter_draw": {
    "power": "1",
    "sign": "positive",
    "centre": -2,
    "radius": 4,
    "coefficient": 1,
    "start": 1
   },
   "completes": "ex-1",
   "stem": {
    "text": "The limit of the ratio is \\(\\frac{|x+2|}{4}\\). Solve \\(\\frac{|x+2|}{4}<1\\) and write the interior as an interval.",
    "command_verb": "write"
   },
   "key": {
    "form": "symbolic",
    "expr": "Interval(-6, 2, True, True)"
   },
   "steps": [
    {
     "text": "Limit.",
     "expr": "Abs(x + 2)/4",
     "relation": "new"
    },
    {
     "text": "Interior.",
     "expr": "Interval(-6, 2, True, True)",
     "relation": "new"
    }
   ],
   "calculator_status": "no_calculator",
   "skills": [
    "BC-SKL-10053"
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
   "archetype_id": "BC-QA-10013",
   "parameter_draw": {
    "power": "1",
    "sign": "positive",
    "centre": 3,
    "radius": 2,
    "coefficient": 1,
    "start": 1
   },
   "stem": {
    "text": "Use the ratio test to find the interior of the interval of convergence of \\(\\sum_{n=1}^{\\infty}\\frac{(x-3)^n}{2^n n}\\).",
    "command_verb": "find"
   },
   "key": {
    "form": "symbolic",
    "expr": "Interval(1, 5, True, True)"
   },
   "steps": [
    {
     "text": "Centre.",
     "expr": "3",
     "relation": "new"
    },
    {
     "text": "Ratio.",
     "expr": "Abs(x - 3)*n/(2*(n + 1))",
     "relation": "new"
    },
    {
     "text": "Limit.",
     "expr": "Abs(x - 3)/2",
     "relation": "limit",
     "variable": "n",
     "point": "oo",
     "dir": "-"
    },
    {
     "text": "Interior.",
     "expr": "Interval(1, 5, True, True)",
     "relation": "new"
    }
   ],
   "calculator_status": "no_calculator",
   "skills": [
    "BC-SKL-10053"
   ]
  },
  {
   "id": "chk-3",
   "check_kind": "mcq",
   "format": "mcq",
   "bands": [
    "low"
   ],
   "archetype_id": "BC-QA-10013",
   "parameter_draw": {
    "power": "1",
    "sign": "positive",
    "centre": 1,
    "radius": 3,
    "coefficient": 1,
    "start": 1
   },
   "stem": {
    "text": "For \\(\\sum_{n=1}^{\\infty}\\frac{(x-1)^n}{3^n n}\\), find the third term of the series obtained at the left endpoint \\(x=-2\\).",
    "command_verb": "find"
   },
   "key": {
    "form": "numeric",
    "expr": "-1/3"
   },
   "steps": [
    {
     "text": "General term.",
     "expr": "(x - 1)**3/(3**3*3)",
     "relation": "new"
    },
    {
     "text": "At x = -2.",
     "expr": "-1/3",
     "relation": "evaluate",
     "subs": {
      "x": "-2"
     }
    }
   ],
   "options": [
    {
     "id": "A",
     "is_key": false,
     "expr": "1/3",
     "error_path": "BC-ERR-10034",
     "derivation": "the alternating factor produced by the negative endpoint dropped, (-3)^3 read as 3^3"
    },
    {
     "id": "B",
     "is_key": true,
     "expr": "-1/3",
     "error_path": null
    },
    {
     "id": "C",
     "is_key": false,
     "expr": "-9/8",
     "error_path": "BC-ERR-10034",
     "derivation": "the endpoint -2 substituted for the index n and the index 3 for x"
    },
    {
     "id": "D",
     "is_key": false,
     "expr": "9/8",
     "error_path": "BC-ERR-10034",
     "derivation": "the endpoint substituted for the index n, and the alternating factor dropped"
    }
   ],
   "calculator_status": "no_calculator",
   "skills": [
    "BC-SKL-10053"
   ]
  }
 ],
 "delivery": [
  {
   "block": "pr-1",
   "mode": "text",
   "reason": "rule 6: a question on ex-1's own numbers",
   "sources": [
    "BC-CON-10020"
   ]
  },
  {
   "block": "orientation",
   "mode": "text",
   "reason": "rule 6: a statement of what a response shows",
   "sources": [
    "BC-CON-10020"
   ]
  },
  {
   "block": "ki-1",
   "mode": "text",
   "reason": "rule 6: BC-REP-11 and 01 on BC-SKL-10053, neither figure-bearing; the idea is a form and a reading, not a process",
   "sources": [
    "BC-SKL-10053",
    "BC-EK-LIM-8D1"
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
   "block": "err-BC-ERR-10034",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  }
 ],
 "refresher": [
  "ki-1",
  "err-BC-ERR-10034",
  "ex-1"
 ],
 "research_lines": [
  {
   "file": "research/units/unit-10-infinite-sequences-series.md",
   "line": "A power series has the form the sum of a sub n times x minus r to the n, with r the centre"
  }
 ],
 "inferred": [
  {
   "claim": "The method of st-1 and st-2 begins with reading the centre, a step neither BC-QA-10013 nor BC-QA-10014 lists in expected_solution_path, and the rival of st-1 is a misreading no record names.",
   "settles": "A centre-reading step in the archetype paths, or a BC-SIG or BC-ERR record for the sign of the centre."
  },
  {
   "claim": "BC-ERR-10034 is the only error held by BC-SKL-10053, so check 3's three distractors all carry it, as the dropped factor, the swapped index and both together.",
   "settles": "A second error linked to BC-SKL-10053, such as the centre read with the wrong sign."
  },
  {
   "claim": "A fluent solver writes the ratio, the limit and the interior, and holds the reading of the centre.",
   "settles": "Timing data per step once the fluency telemetry exists."
  },
  {
   "claim": "ex-1 tags BC-PT-99044 only, because the ratio and limit reader lines do not fit the brief cap; ex-2 carries BC-PT-99042, 99043 and 99047.",
   "settles": "A brief cap that admits a second reader line."
  }
 ],
 "sources": [
  "BC-CON-10020",
  "BC-SKL-10053",
  "BC-EK-LIM-8D1",
  "ced:198",
  "BC-QA-10013",
  "BC-QA-10014",
  "BC-QA-10004",
  "BC-PT-99042",
  "BC-PT-99043",
  "BC-PT-99044",
  "BC-PT-99047",
  "BC-ERR-10034",
  "BC-PRQ-10008",
  "sg-25:25",
  "sg-21:24",
  "research/units/unit-10-infinite-sequences-series.md#10.13 Radius and Interval of Convergence of Power Series",
  "research/question-analysis/question-archetypes.md#BC-QA-10013 Interval of convergence by the ratio test with endpoint analysis",
  "research/question-analysis/question-archetypes.md#BC-QA-10014 Radius of convergence from a given series",
  "research/exam/exam-structure.md#Section and part layout"
 ],
 "word_count": {
  "full": 693,
  "brief": 416
 },
 "read_minutes": {
  "full": 4.7,
  "brief": 2.8
 }
}
```
