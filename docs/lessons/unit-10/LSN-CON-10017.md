---
title: LSN-CON-10017 Taylor polynomials as approximations near the centre
research_date: 2026-09-29
status: designed
purpose: Authoring spec for the concept lesson on BC-CON-10017, the value of a Taylor polynomial at an input near the centre reported as an approximation of the function value at the stated degree, built from authoring_bundle("BC-CON-10017") and the research files it cites, so an author fills plan 15's lesson record without making a teaching decision.
---

# LSN-CON-10017 Taylor polynomials as approximations near the centre

## Prediction

Served first, both bands: an `mcq` on ex-1's own numbers. g is 3x over one minus 2x and P is its degree 3 Taylor polynomial about 0, and the student picks how P at one tenth compares with g at one tenth. Key B, slightly less. The student settles it by arithmetic before any rule: P gives 93/250 = 0.372 and g gives 3/8 = 0.375. The distractors are equality and greater than. The resolution states both values and their difference of 3/1000, with no verdict word. Source: BC-CON-10017 and the topic 10.11 section the key idea cites.

## Orientation

Served text from BC-CON-10017 `description_plain` (near the centre the polynomial value stands in for the function value) and the topic's Assessment behaviour paragraph (MCQ forms give derivative values and ask for a coefficient or the polynomial; FRQ parts are no calculator, a polynomial of the right shape can earn a term point, and a coefficient with no support does not earn the final point, sg-23:20). The orientation states what a response shows: the polynomial to the stated degree, the substitution, the sum reported as an approximation. No count, no frequency.

## Key ideas

One core block. BC-SKL-10048 maps one essential knowledge statement, BC-EK-LIM-8B1 (ced:196), so the lesson has one key idea, served in both bands. It paraphrases the Approximation paragraph and the Degree discipline paragraph of the topic (a polynomial with terms above the requested degree, or a trailing ellipsis, is not the requested polynomial, sg-23:19, sg-23:20). Notation line: the concept's `notation`, approximation near the centre. No anchor quote: the CED sentence adds nothing the paraphrase lacks and costs words in the brief band.

## Recognition

Two archetypes load BC-SKL-10048, BC-QA-10012 (family taylor-construction) and BC-QA-10009 (family taylor-error), and both are `no_calculator`.

- BC-QA-10012 `asked_to_produce`: "the Taylor polynomial of the stated degree for the related function". `common_givens`: "values or a Taylor polynomial of the first function at the centre". Shapes: a related function g(x) = c x^m f(kx), the polynomial to a stated degree, then a value from it (question-archetypes.md, BC-QA-10012); official examples BC-FRQ-2019-Q6-B, 2013-Q6-C, 2015-Q6-C, 2023-Q6-C.
- BC-QA-10009 `common_givens`: "an input near the centre", "a tolerance for the error". The polynomial approximates a function value and the bound is written about that approximation.

What says this concept: a Taylor polynomial of stated degree and an input near the centre, with a request for the approximation. What says not this concept: a supplied bound on the next derivative and a request for how far the polynomial lies from f, which is the Lagrange bound (BC-CON-10018). The near miss of the contrast pair comes from BC-QA-10009.

## Method choice

- st-1, BC-QA-10012, verified (both cue fields exist). Cue from `common_givens` and `asked_to_produce`. Method from `expected_solution_path`: expand to the stated degree, then substitute the input. Rival from `common_distractors`: "presenting a polynomial with terms of higher degree", and the exact value in place of an approximation. Separating feature: the stated degree fixes the terms and the input only fixes where to evaluate. The block carries the contrast pair, a value stem of BC-QA-10012's shape beside an error-bound stem of BC-QA-10009's shape.
- st-2, BC-QA-10009, low band only. Cue from `common_givens`, method `expected_solution_path[1]`, rival the polynomial's own value as the answer, feature the request for a distance from f.

## Solution path

- ex-1, BC-QA-10012, both bands, no calculator. Draw: base geometric, power 1, terms 3, scale 2, coefficient 3, so g(x) = 3x/(1 - 2x) and the degree is power plus terms minus 1 = 3, P(x) = 3x + 6x^2 + 12x^3. Input 1/10, value 93/250 (SymPy). No published item on BC-QA-10012 carries this draw (checker rule draw_exclusion).
- ex-2, low band, faded from step 3. Draw: base exp, power 1, terms 3, scale -2, coefficient 3, g(x) = 3x e^(-2x), P(x) = 3x - 6x^2 + 6x^3, value at 1/10 = 123/500. Steps 1 and 2 (the series substitution and the truncated polynomial) are shown, the student writes the approximation, and steps 3 and 4 then reveal. The fade falls there because the construction repeats ex-1's pattern and the substitution is what the student must produce.
- Steps follow `expected_solution_path`: expand (new), truncate (equivalent), evaluate at the input (evaluate), then a sentence with no value. A fluent solver writes the truncated polynomial and the substituted value and holds the series substitution and the closing sentence (Time). No productive-failure comparison: BC-CON-10017 is not in `PRODUCTIVE_FAILURE_TARGETS`.

## Scoring

BC-QA-10012 lists BC-PT-99037, 99035, 99036 and 99027. Each example tags BC-PT-99036 on the truncated polynomial, the point a term past the stated degree or a trailing ellipsis loses (sg-25:22, sg-23:19, sg-23:21). BC-PT-99037 is earned in step 1 but untagged in the brief-band cap (inferred array), and BC-PT-99035 and 99027 are earned on constructions this lesson does not stress. No listed point type scores the substitution itself, so the lesson says nothing about points for the approximation step. The lines are `reader_checks` output.

Point losses from research: a polynomial with terms of higher degree or a trailing ellipsis loses the final polynomial point (research/scoring/notation-requirements.md#Terms, ellipses and extraneous terms, sg-23:19, sg-23:20).

## Traps

One active error meets the skills, BC-ERR-10030 (BC-SKL-10048 lists only it), linked to BC-MIS-10020 and 10021. One block, `fix_prompt` true: the pair is distinct, P with a degree 4 term against P stopping at degree 3, on ex-1's draw. `possible_reason` from BC-MIS-10020. Check 3's three distractors all carry BC-ERR-10030, with one, two and three extra terms; the record holds no second honest error for this skill (see gaps in the report).

## Representations

None. The topic's Representations paragraph names BC-REP-01, 03, 09 and 11 and the conversions table to polynomial, relation to derivative values, and known series to polynomial; nothing figure-shaped for approximation at an input.

## Prerequisite bridge

- BC-PRQ-06005, from its `description_plain` and `failure_signature`: evaluation at a stated input, and f kept apart from what stands in for it.

## Time

The MCQ shape is Section I Part A, 2.14 minutes (research/exam/exam-structure.md#Section and part layout). As a free response part on BC-QA-10012, 3 points, 5.0 minutes (docs/lessons/unit-10/README.md, section 5). A fluent solver writes the truncated polynomial and the substituted value; the series substitution and the closing sentence are held [inferred]. The minutes go on the series and the arithmetic.

## Checks

- chk-1, completion of ex-1, both bands: P given, the approximation asked. Key 93/250.
- chk-2, isomorph, both bands. Draw: base geometric, power 2, terms 3, scale -3, coefficient 4, g(x) = 4x^2/(1 + 3x), degree 4, key 79/2500.
- chk-3, MCQ, low band. Draw: base geometric, power 1, terms 3, scale 2, coefficient 1, g(x) = x/(1 - 2x), key 31/250. Distractors 78/625 (degree 4 term kept), 781/6250 (degree 4 and 5 terms kept), 1953/15625 (degree 4, 5 and 6 terms kept), each BC-ERR-10030.

## Delivery

- pr-1, orientation, ki-1: text. Rule 6. BC-SKL-10048 carries BC-REP-01 and 09, neither figure-bearing, and BC-EK-LIM-8B1 states an approximation, not a process. The README delivery map (docs/lessons/unit-10/README.md, section 6) names a `motion` block for BC-EK-LIM-8A2, but no skill carries that statement, so no key idea can cite it. The record carries `no_figure_reason`.
- ex-1, ex-2, err-BC-ERR-10030: step_reveal. Rule 1.

## Band plan

- Low (full): prediction, orientation, bridge, ki-1, st-1 with the contrast pair, st-2, ex-1 and its line, chk-1, the error block, ex-2 (faded from step 3) and its line, chk-2, chk-3. 614 words, 4.1 minutes.
- Mid (brief): prediction, orientation, bridge, ki-1, st-1 with the contrast pair, ex-1 and its line, chk-1, the error block, chk-2. 447 words, 3.0 minutes.
- Refresher: ki-1, err-BC-ERR-10030, ex-1.

## Sources

- BC-CON-10017; BC-SKL-10048; BC-EK-LIM-8B1; ced:196
- BC-QA-10012; BC-QA-10009; BC-PT-99036; BC-PT-99037
- BC-ERR-10030; BC-MIS-10020
- BC-PRQ-06005
- sg-23:19, sg-23:20, sg-25:22
- research/units/unit-10-infinite-sequences-series.md#10.11 Finding Taylor Polynomial Approximations of Functions
- research/question-analysis/question-archetypes.md#BC-QA-10012 Taylor polynomial for a related function built from a known series
- research/question-analysis/question-archetypes.md#BC-QA-10009 Lagrange error bound with a supplied derivative bound
- research/exam/exam-structure.md#Section and part layout
- [inferred] the task value for an input, the missing motion link, the held steps, the untagged BC-PT-99037. Each settled as the inferred array states.

## Machine record

```json
{
 "id": "LSN-CON-10017",
 "kind": "concept",
 "target_id": "BC-CON-10017",
 "unit": "10",
 "skills": [
  "BC-SKL-10048"
 ],
 "prediction": {
  "id": "pr-1",
  "stem": {
   "text": "Let \\(g(x)=\\frac{3x}{1-2x}\\) and \\(P(x)=3x+6x^2+12x^3\\), its degree 3 Taylor polynomial about \\(x=0\\). Predict how \\(P(\\tfrac{1}{10})\\) compares with \\(g(\\tfrac{1}{10})\\).",
   "command_verb": "predict"
  },
  "format": "mcq",
  "options": [
   {
    "id": "A",
    "label": "\\(P(\\tfrac{1}{10})=g(\\tfrac{1}{10})\\)",
    "is_key": false
   },
   {
    "id": "B",
    "label": "\\(P(\\tfrac{1}{10})\\) is slightly less than \\(g(\\tfrac{1}{10})\\)",
    "is_key": true
   },
   {
    "id": "C",
    "label": "\\(P(\\tfrac{1}{10})\\) is greater than \\(g(\\tfrac{1}{10})\\)",
    "is_key": false
   }
  ],
  "resolution": "\\(P(\\tfrac{1}{10})=\\frac{93}{250}\\) and \\(g(\\tfrac{1}{10})=\\frac{3}{8}\\). Near the centre, the polynomial's value stands in for the function's value as an approximation.",
  "sources": [
   "BC-CON-10017",
   "research/units/unit-10-infinite-sequences-series.md#10.11 Finding Taylor Polynomial Approximations of Functions"
  ]
 },
 "no_figure_reason": "No skill of this concept carries a figure-bearing representation. The one process idea, polynomials of rising degree approaching f, sits on an essential knowledge statement that no skill of this concept carries.",
 "orientation": {
  "text": "Near the centre, a Taylor polynomial's value stands in for the function's value. A response gives the polynomial to exactly the stated degree, substitutes the input, and reports the sum as an approximation.",
  "sources": [
   "BC-CON-10017",
   "research/units/unit-10-infinite-sequences-series.md#10.11 Finding Taylor Polynomial Approximations of Functions"
  ]
 },
 "key_ideas": [
  {
   "id": "ki-1",
   "ek_id": "BC-EK-LIM-8B1",
   "depth": "core",
   "text": "The Taylor polynomial \\(P_n\\) for \\(f\\) about \\(x=a\\) approximates \\(f(x)\\) near \\(a\\). Substitute the input, evaluate each term and report the sum as an approximation. The polynomial stops at the stated degree, with no extra term or ellipsis.",
   "notation": "approximation near the centre",
   "quote": null,
   "sources": [
    "BC-EK-LIM-8B1",
    "ced:196",
    "sg-23:19",
    "sg-23:20",
    "research/units/unit-10-infinite-sequences-series.md#10.11 Finding Taylor Polynomial Approximations of Functions"
   ]
  }
 ],
 "strategy": [
  {
   "id": "st-1",
   "archetype_id": "BC-QA-10012",
   "cue": "A Taylor polynomial of stated degree and an input near the centre.",
   "method": "Build the polynomial to the stated degree, then substitute the input.",
   "rival": "Terms past the stated degree, or the exact function value.",
   "separating_feature": "The stated degree fixes the terms, and the input only fixes where to evaluate.",
   "sources": [
    "BC-QA-10012"
   ],
   "evidence_tag": "verified",
   "contrast": {
    "this": {
     "text": "Let \\(g(x)=\\frac{2x}{1-3x}\\). Use the Taylor polynomial of degree 3 for \\(g\\) about \\(x=0\\) to approximate \\(g(\\tfrac{1}{20})\\).",
     "archetype_id": "BC-QA-10012"
    },
    "not_this": {
     "text": "Let \\(P_3\\) be the degree 3 Taylor polynomial of \\(f\\) about \\(x=2\\), with \\(|f^{(4)}(x)|\\le 12\\) on \\([2,\\frac52]\\). Find a bound on \\(|f(\\tfrac52)-P_3(\\tfrac52)|\\).",
     "why_not": "It asks how far \\(P_3\\) lies from \\(f\\), so the answer is an error bound."
    },
    "feature": "One asks for the polynomial's value, the other for its distance from the function."
   }
  },
  {
   "id": "st-2",
   "archetype_id": "BC-QA-10009",
   "cue": "A bound on the next derivative and a tolerance for the error.",
   "method": "Write the Lagrange bound and compare it with the tolerance.",
   "rival": "The polynomial's own value given as the answer.",
   "separating_feature": "The stem asks how far the polynomial lies from \\(f\\).",
   "sources": [
    "BC-QA-10009"
   ],
   "evidence_tag": "verified"
  }
 ],
 "worked_examples": [
  {
   "id": "ex-1",
   "archetype_id": "BC-QA-10012",
   "bands": [
    "low",
    "mid"
   ],
   "parameter_draw": {
    "base": "geometric",
    "power": 1,
    "terms": 3,
    "scale": "2",
    "coefficient": 3
   },
   "problem": {
    "text": "Let \\(g(x)=\\frac{3x}{1-2x}\\). Write the Taylor polynomial of degree 3 for \\(g\\) about \\(x=0\\), then approximate \\(g(\\tfrac{1}{10})\\).",
    "command_verb": "find"
   },
   "calculator_status": "no_calculator",
   "steps": [
    {
     "cue": "Put \\(u=2x\\), then multiply by \\(3x\\).",
     "why": "The series for \\(\\frac{1}{1-u}\\) is known.",
     "expr": "3*x*(1 + 2*x + 4*x**2)",
     "relation": "new"
    },
    {
     "cue": "Stop at degree 3.",
     "why": "The degree fixes the terms.",
     "expr": "3*x + 6*x**2 + 12*x**3",
     "relation": "equivalent",
     "point_type_id": "BC-PT-99036"
    },
    {
     "cue": "\\(\\frac{1}{10}\\) is near the centre 0.",
     "why": "\\(P\\) stands in for \\(g\\) there.",
     "expr": "93/250",
     "relation": "evaluate",
     "subs": {
      "x": "1/10"
     }
    },
    {
     "cue": "\\(g\\) is not a polynomial.",
     "why": "So \\(\\frac{93}{250}\\) approximates \\(g(\\tfrac{1}{10})\\)."
    }
   ],
   "answer": {
    "form": "numeric",
    "expr": "93/250"
   }
  },
  {
   "id": "ex-2",
   "archetype_id": "BC-QA-10012",
   "bands": [
    "low"
   ],
   "fade_from": 3,
   "parameter_draw": {
    "base": "exp",
    "power": 1,
    "terms": 3,
    "scale": "-2",
    "coefficient": 3
   },
   "problem": {
    "text": "Let \\(g(x)=3xe^{-2x}\\). Use the series for \\(e^u\\) to write the Taylor polynomial of degree 3 for \\(g\\) about \\(x=0\\), then approximate \\(g(\\tfrac{1}{10})\\).",
    "command_verb": "find"
   },
   "calculator_status": "no_calculator",
   "steps": [
    {
     "cue": "Put \\(u=-2x\\), then multiply by \\(3x\\).",
     "why": "The series for \\(e^u\\) is known.",
     "expr": "3*x*(1 - 2*x + 2*x**2)",
     "relation": "new"
    },
    {
     "cue": "Stop at degree 3.",
     "why": "The next nonzero term has degree 4.",
     "expr": "3*x - 6*x**2 + 6*x**3",
     "relation": "equivalent",
     "point_type_id": "BC-PT-99036"
    },
    {
     "cue": "\\(\\frac{1}{10}\\) is near the centre 0.",
     "why": "Substitute and sum.",
     "expr": "123/500",
     "relation": "evaluate",
     "subs": {
      "x": "1/10"
     }
    },
    {
     "cue": "State what the number is.",
     "why": "It approximates \\(g(\\tfrac{1}{10})\\) and is not its value."
    }
   ],
   "answer": {
    "form": "numeric",
    "expr": "123/500"
   }
  }
 ],
 "what_a_reader_scores": [
  {
   "example_id": "ex-1",
   "point_type_ids": [
    "BC-PT-99036"
   ],
   "lines": [
    {
     "point_type_id": "BC-PT-99036",
     "text": "Remaining terms of a Taylor or Maclaurin polynomial. Earned by: The remaining required terms, completing the polynomial to the requested degree (sg-26:22, sg-25:22). Not earned by: A polynomial carrying terms of higher degree than asked, or an ellipsis suggesting the series continues (sg-25:22, sg-23:19, sg-23:21)."
    }
   ]
  },
  {
   "example_id": "ex-2",
   "point_type_ids": [
    "BC-PT-99036"
   ],
   "lines": [
    {
     "point_type_id": "BC-PT-99036",
     "text": "Remaining terms of a Taylor or Maclaurin polynomial. Earned by: The remaining required terms, completing the polynomial to the requested degree (sg-26:22, sg-25:22). Not earned by: A polynomial carrying terms of higher degree than asked, or an ellipsis suggesting the series continues (sg-25:22, sg-23:19, sg-23:21)."
    }
   ]
  }
 ],
 "common_errors": [
  {
   "error_id": "BC-ERR-10030",
   "observed_behavior": "The response writes a polynomial that includes terms beyond the requested degree, or appends an ellipsis, turning the answer into a series.",
   "scoring_consequence": "A polynomial with terms of higher degree, or with an ellipsis, does not earn the final polynomial point (sg-23:20, sg-23:21).",
   "wrong_step": {
    "text": "\\(P\\) carries a degree 4 term.",
    "expr": "3*x + 6*x**2 + 12*x**3 + 24*x**4"
   },
   "right_step": {
    "text": "\\(P\\) stops at degree 3.",
    "expr": "3*x + 6*x**2 + 12*x**3"
   },
   "relation": "distinct",
   "fix_prompt": true,
   "possible_reason": {
    "misconception_id": "BC-MIS-10020",
    "text": "does not treat the requested degree as binding"
   },
   "sources": [
    "BC-ERR-10030",
    "BC-MIS-10020"
   ]
  }
 ],
 "representations": null,
 "prerequisite_bridges": [
  {
   "prq_id": "BC-PRQ-06005",
   "text": "Substitute the stated input for \\(x\\), and keep \\(f\\) and its polynomial as separate functions."
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
    1,
    4
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
   "archetype_id": "BC-QA-10012",
   "parameter_draw": {
    "base": "geometric",
    "power": 1,
    "terms": 3,
    "scale": "2",
    "coefficient": 3
   },
   "completes": "ex-1",
   "stem": {
    "text": "\\(P(x)=3x+6x^2+12x^3\\) is the degree 3 Taylor polynomial for \\(g\\) about \\(x=0\\). Write the approximation of \\(g(\\tfrac{1}{10})\\).",
    "command_verb": "write"
   },
   "key": {
    "form": "numeric",
    "expr": "93/250"
   },
   "steps": [
    {
     "text": "Substitute.",
     "expr": "3*(1/10) + 6*(1/10)**2 + 12*(1/10)**3",
     "relation": "new"
    },
    {
     "text": "Sum.",
     "expr": "93/250",
     "relation": "equivalent"
    }
   ],
   "calculator_status": "no_calculator",
   "skills": [
    "BC-SKL-10048"
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
   "archetype_id": "BC-QA-10012",
   "parameter_draw": {
    "base": "geometric",
    "power": 2,
    "terms": 3,
    "scale": "-3",
    "coefficient": 4
   },
   "stem": {
    "text": "Let \\(g(x)=\\frac{4x^2}{1+3x}\\). Write the Taylor polynomial of degree 4 for \\(g\\) about \\(x=0\\), then approximate \\(g(\\tfrac{1}{10})\\).",
    "command_verb": "write"
   },
   "key": {
    "form": "numeric",
    "expr": "79/2500"
   },
   "steps": [
    {
     "text": "Series.",
     "expr": "4*x**2*(1 - 3*x + 9*x**2)",
     "relation": "new"
    },
    {
     "text": "Degree 4.",
     "expr": "4*x**2 - 12*x**3 + 36*x**4",
     "relation": "equivalent"
    },
    {
     "text": "Substitute.",
     "expr": "79/2500",
     "relation": "evaluate",
     "subs": {
      "x": "1/10"
     }
    }
   ],
   "calculator_status": "no_calculator",
   "skills": [
    "BC-SKL-10048"
   ]
  },
  {
   "id": "chk-3",
   "check_kind": "mcq",
   "format": "mcq",
   "bands": [
    "low"
   ],
   "archetype_id": "BC-QA-10012",
   "parameter_draw": {
    "base": "geometric",
    "power": 1,
    "terms": 3,
    "scale": "2",
    "coefficient": 1
   },
   "stem": {
    "text": "Let \\(g(x)=\\frac{x}{1-2x}\\). The approximation of \\(g(\\tfrac{1}{10})\\) from the degree 3 Taylor polynomial about \\(x=0\\) is",
    "command_verb": "identify"
   },
   "key": {
    "form": "numeric",
    "expr": "31/250"
   },
   "steps": [
    {
     "text": "Series.",
     "expr": "x*(1 + 2*x + 4*x**2)",
     "relation": "new"
    },
    {
     "text": "Degree 3.",
     "expr": "x + 2*x**2 + 4*x**3",
     "relation": "equivalent"
    },
    {
     "text": "Substitute.",
     "expr": "31/250",
     "relation": "evaluate",
     "subs": {
      "x": "1/10"
     }
    }
   ],
   "options": [
    {
     "id": "A",
     "is_key": false,
     "expr": "78/625",
     "error_path": "BC-ERR-10030",
     "derivation": "the degree 4 term 8x^4 kept beyond the requested degree 3"
    },
    {
     "id": "B",
     "is_key": true,
     "expr": "31/250",
     "error_path": null
    },
    {
     "id": "C",
     "is_key": false,
     "expr": "781/6250",
     "error_path": "BC-ERR-10030",
     "derivation": "the terms of degree 4 and 5 kept beyond the requested degree 3"
    },
    {
     "id": "D",
     "is_key": false,
     "expr": "1953/15625",
     "error_path": "BC-ERR-10030",
     "derivation": "the terms of degree 4, 5 and 6 kept beyond the requested degree 3"
    }
   ],
   "calculator_status": "no_calculator",
   "skills": [
    "BC-SKL-10048"
   ]
  }
 ],
 "delivery": [
  {
   "block": "pr-1",
   "mode": "text",
   "reason": "rule 6: a question on ex-1's own numbers, no figure-bearing representation",
   "sources": [
    "BC-CON-10017"
   ]
  },
  {
   "block": "orientation",
   "mode": "text",
   "reason": "rule 6: a statement of what a response shows",
   "sources": [
    "BC-CON-10017"
   ]
  },
  {
   "block": "ki-1",
   "mode": "text",
   "reason": "rule 6: BC-REP-01 and BC-REP-09 on BC-SKL-10048, neither figure-bearing; BC-EK-LIM-8B1 states an approximation, not a process, and BC-EK-LIM-8A2 (the process) is carried by no skill of this concept",
   "sources": [
    "BC-SKL-10048",
    "BC-EK-LIM-8B1"
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
   "block": "err-BC-ERR-10030",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  }
 ],
 "refresher": [
  "ki-1",
  "err-BC-ERR-10030",
  "ex-1"
 ],
 "research_lines": [
  {
   "file": "research/units/unit-10-infinite-sequences-series.md",
   "line": "A polynomial presented with terms of degree higher than requested, or with a trailing ellipsis, is not the requested polynomial"
  }
 ],
 "inferred": [
  {
   "claim": "Both worked examples end by evaluating the polynomial at an input, a step the parameter_spec of BC-QA-10012 has no task value for; the archetype draw fixes the function and the degree.",
   "settles": "A parameter_spec task value on BC-QA-10012 that names an input near the centre."
  },
  {
   "claim": "No motion block of polynomials of rising degree is delivered, because BC-EK-LIM-8A2 is on no skill of this concept.",
   "settles": "Linking BC-EK-LIM-8A2 to BC-SKL-10048 or BC-SKL-10067 in the library."
  },
  {
   "claim": "A fluent solver writes the truncated polynomial and the substituted value, and holds the series substitution and the closing sentence.",
   "settles": "Timing data per step once the fluency telemetry exists."
  },
  {
   "claim": "BC-PT-99037 (the first terms of the related series) is earned in step 1 of each example but untagged, because its reader line does not fit the brief band.",
   "settles": "A brief cap that admits a second reader line."
  }
 ],
 "sources": [
  "BC-CON-10017",
  "BC-SKL-10048",
  "BC-EK-LIM-8B1",
  "ced:196",
  "BC-QA-10012",
  "BC-QA-10009",
  "BC-PT-99036",
  "BC-PT-99037",
  "BC-ERR-10030",
  "BC-MIS-10020",
  "BC-PRQ-06005",
  "sg-23:19",
  "sg-23:20",
  "sg-25:22",
  "research/units/unit-10-infinite-sequences-series.md#10.11 Finding Taylor Polynomial Approximations of Functions",
  "research/question-analysis/question-archetypes.md#BC-QA-10012 Taylor polynomial for a related function built from a known series",
  "research/question-analysis/question-archetypes.md#BC-QA-10009 Lagrange error bound with a supplied derivative bound",
  "research/exam/exam-structure.md#Section and part layout"
 ],
 "word_count": {
  "full": 614,
  "brief": 447
 },
 "read_minutes": {
  "full": 4.1,
  "brief": 3.0
 }
}
```
