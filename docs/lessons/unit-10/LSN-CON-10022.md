---
title: LSN-CON-10022 Endpoint testing and the interval of convergence
research_date: 2026-09-29
status: designed
purpose: Authoring spec for the concept lesson on BC-CON-10022, the two endpoints of a power series put in place of x, each tested on its own, and the interval of convergence written with brackets that match the verdicts, built from authoring_bundle("BC-CON-10022") and the research files it cites, so an author fills plan 15's lesson record without making a teaching decision.
---

# LSN-CON-10022 Endpoint testing and the interval of convergence

Concept BC-CON-10022 (skills BC-SKL-10057, BC-SKL-10058, BC-SKL-10059), topic 10.13 of Unit 10, BC only (ced:198), loaded by two archetypes, BC-QA-10013 (family radius-interval) and BC-QA-10015 (the endpoint drill). Hard parents BC-CON-10008 (test selection) and BC-CON-10021 (the radius from the ratio test) (docs/lessons/unit-10/README.md, section 1).

## Prediction

Served first, both bands: an `mcq` on ex-1's own numbers. The ratio test gives \(-6<x<2\) for \(\sum\frac{5(x+2)^n}{4^n n}\) and is silent at the ends, and the student says what happens at \(x=-6\) and at \(x=2\). Key B, converges at \(-6\) and diverges at \(2\). The four options are the four combinations, so only B is true: the series is \(5\sum\frac{(-1)^n}{n}\) at \(-6\) (alternating, converges) and \(5\sum\frac1n\) at \(2\) (harmonic, diverges). Both facts come from parent concepts (BC-CON-10004, 10011), so the question is answerable before this lesson's rule. The resolution names the two series and says each needs its own test, with no verdict. Source: BC-CON-10022 and research/units/unit-10-infinite-sequences-series.md#10.13 Radius and Interval of Convergence of Power Series.

## Orientation

Served text (32 words), from BC-CON-10022 `description_plain` ("the two ends of the interval have to be checked one at a time with a suitable test") and the topic's Assessment behaviour paragraph: five points over the ratio, its limit, the interior, considering both endpoints and the analysis with the final interval, or four when the endpoints share an argument (sg-25:24, sg-22:20, research/units/unit-10-infinite-sequences-series.md#10.13 Radius and Interval of Convergence of Power Series). No count, no frequency.

## Key ideas

Two essential knowledge statements meet the skills (ced:198): ki-1 (core) BC-EK-LIM-8D4, the radius gives an open interval and both endpoints must be tested, with the substitution rule of BC-ERR-10034 (the endpoint replaces the variable, and a negative displacement brings the alternating factor) and the point that the ends can differ (BC-MIS-10024); ki-2 (extended) BC-EK-LIM-8D2, a convergent power series converges at one point or on an interval, so each end takes its own bracket. No anchor quote. Core serves both bands, extended the low band.

## Recognition

BC-QA-10013 (research/question-analysis/question-archetypes.md#BC-QA-10013 Interval of convergence by the ratio test with endpoint analysis): `asked_to_produce` "an analysis of each endpoint" and "the interval of convergence"; `typical_wording` "using the ratio test, find the interval of convergence of the series and justify the answer". BC-QA-10015 (research/question-analysis/question-archetypes.md#BC-QA-10015 Endpoint series identified and tested): `common_givens` "a power series with its radius of convergence" and "an endpoint value of x"; `asked_to_produce` "the numerical series at the endpoint" and "a convergence or divergence verdict with a named test". Official parts: BC-FRQ-2012-Q6-A, 2022-Q6-A, 2025-Q6-A, 2018-Q6-B and MCQ BC-MCQ-PE2012-022 for the interval; BC-QA-10015 lists no official example.

What in the stem says this concept: the words interval of convergence, or a stated endpoint value with a request for a verdict and a named test. What says not this concept: the word radius with no endpoint (BC-CON-10021). The near miss of the contrast pair is the radius stem on the same series (docs/lessons/unit-10/README.md, section 3, the radius against interval row).

## Method choice

- st-1, BC-QA-10013. Cue from `asked_to_produce` and the typical wording. Method, `expected_solution_path`: interior from the ratio test, substitute each endpoint, test each, state the interval with matching brackets. Rival from `wrong_approaches`: "reporting the open interval without testing the endpoints". Separating feature: interval asks for both verdicts. Carries the contrast pair: an interval stem beside a radius stem on one series.
- st-2, BC-QA-10015, low band only. Method: substitute the endpoint, simplify to a numerical series, name a test whose conditions it meets. Rival from `wrong_approaches`: "applying a comparison test to an alternating endpoint series". Separating feature: the signs of the endpoint series, the series test contrast the README assigns to this lesson (docs/lessons/unit-10/README.md, section 3).
No served field opens with the reader's own label.

## Solution path

- ex-1, BC-QA-10013, both bands. Draw: power 1, sign positive, centre -2, radius 4, coefficient 5, start 1, giving \(\sum\frac{5(x+2)^n}{4^n n}\), interval \([-6,2)\). No published item on BC-QA-10013 carries this draw (content/items_gen_*/ITM-GEN-10013-00 to 21). The problem states the ratio test result, and one unvalued step carries it, because the ratio and limit steps belong to BC-CON-10021 (inferred array). Valued steps: the series at 2, the series at -6, the interval.
- ex-2, low band, BC-QA-10015. Draw: form power, power 3/2, sign positive, end right, given value, centre 1, radius 3, shift 2, giving \(\sum\frac{(x-1)^n}{3^n n^{3/2}}\) at \(x=4\). No published item on BC-QA-10015 carries this draw (ITM-GEN-10015-00 to 21). The endpoint series is \(\sum\frac1{n^{3/2}}\), a convergent p-series. Its answer is a statement, so no check completes it.
- ex-2 is faded from step 3: the general term and the endpoint series are shown, and the student writes the test and verdict before steps 3 and 4 reveal. The fade falls there because the substitution repeats ex-1's step and the test choice is what the student must produce.
- A fluent solver writes the two endpoint series, the tests and the interval, and holds the ratio result (Time). No productive-failure comparison: BC-CON-10022 is not in `PRODUCTIVE_FAILURE_TARGETS`.

## Scoring

BC-QA-10013 lists BC-PT-99042 to 99046; BC-QA-10015 lists no point type, so ex-2 carries no scoring line and no tag. ex-1 tags BC-PT-99045 on the endpoint series step; BC-PT-99046 is earned by the interval step and left untagged, since its reader line does not fit the brief band beside the prediction and contrast pair (inferred array). BC-PT-99042 to 99044 are not exercised because the interior is given. The lines are `reader_checks` output.

Point losses from research: considering one endpoint only does not earn the endpoint point (BC-PT-99045, sg-22:21); naming an appropriate test at each endpoint suffices for the analysis (research/units/unit-10-infinite-sequences-series.md#10.13 Radius and Interval of Convergence of Power Series, sg-25:25); the final interval point requires the interval to match the analysis (BC-ERR-10038 `scoring_consequence`, sg-25:25).

## Traps

Five errors meet the skills; the cap keeps four, in bundle order: BC-ERR-10015, BC-ERR-10034, BC-ERR-10037, BC-ERR-10038. BC-ERR-99017 falls past the cap. Low band all four, mid band the first two. All on ex-1's draw. All four carry `fix_prompt` true, since each pair is distinct.

- err-BC-ERR-10015: the term \(\frac5n\) tested by the p-series test in place of \(\frac{5(-1)^n}{n}\) by the alternating series test. No possible reason line.
- err-BC-ERR-10034: \(x=-6\) put in place of the index, an expression in \(x\) with the index gone, in place of the endpoint series.
- err-BC-ERR-10037: the open interval in place of \([-6,2)\).
- err-BC-ERR-10038: \((-6,2]\) in place of \([-6,2)\).

## Representations

None. The topic's Representations paragraph names BC-REP-11, 01 and 04 and the conversion of an endpoint value to a numerical series; nothing figure-shaped (docs/lessons/unit-10/README.md, section 6). The README's proposed interactive, \(x\) dragged across the interval, is outside the rules and not adopted here.

## Prerequisite bridge

- BC-PRQ-06002, 06005, 10006, 10008, each from its `description_plain` and `failure_signature`, one short paragraph each.

## Time

ex-1 is the MCQ shape "the interval of convergence": Section I Part A, 2.14 minutes (research/exam/exam-structure.md#Section and part layout). As a free response part: 5 points, 8.33 minutes, or 2 points and 3.33 minutes for a named test at an endpoint (docs/lessons/unit-10/README.md, section 5). A fluent solver writes both endpoint series, a named test with its conditions at each, and the interval; the ratio result is held. The minutes go on matching the sign of each endpoint series to its test.

## Checks

- chk-1, completion of ex-1, both bands: both verdicts given, the interval asked. Key \([-6,2)\).
- chk-2, isomorph, both bands. Draw: power 1, sign alternating, centre 2, radius 5, coefficient 4, start 1. Key \((-3,7]\): the alternating series converges at 7 and the signs cancel to the harmonic series at -3.
- chk-3, MCQ, low band. Draw: power 1/2, sign positive, centre 3, radius 2, coefficient 2, start 1. Key \([1,5)\). Distractors: \((1,5)\) (BC-ERR-10037), \((1,5]\) (BC-ERR-10038), \([1,5]\) (BC-ERR-10015, the alternating series test applied to the positive endpoint series).

## Delivery

- prediction, orientation, ki-1, ki-2: text. Rule 6: the skills carry BC-REP-11, 01 and 04, none figure-bearing. No block is drawn, so the record carries `no_figure_reason`: no figure-bearing representation and no process idea, since each endpoint is a numerical series tested on its own.
- ex-1, ex-2, the four error blocks: step_reveal. Rule 1.

## Band plan

- Low (full): prediction, orientation, four bridges, ki-1, ki-2, st-1 with the contrast pair, st-2, ex-1 and its lines, chk-1, four error blocks, ex-2 (faded from step 3), chk-2, chk-3. 716 words, 4.8 minutes.
- Mid (brief): prediction, orientation, bridges, ki-1, st-1 with the contrast pair, ex-1 and its lines, chk-1, err-BC-ERR-10015, err-BC-ERR-10034, chk-2. 447 words, 3.0 minutes.
- Refresher: ki-1, the four error blocks, ex-1.

## Sources

- BC-CON-10022; BC-SKL-10057, BC-SKL-10058, BC-SKL-10059; BC-EK-LIM-8D2, BC-EK-LIM-8D4; ced:198
- BC-QA-10013, BC-QA-10015; BC-PT-99045, BC-PT-99046
- BC-ERR-10015, BC-ERR-10034, BC-ERR-10037, BC-ERR-10038
- BC-PRQ-06002, BC-PRQ-06005, BC-PRQ-10006, BC-PRQ-10008
- sg-25:24, sg-25:25
- research/units/unit-10-infinite-sequences-series.md#10.13 Radius and Interval of Convergence of Power Series
- research/exam/exam-structure.md#Section and part layout
- [inferred] the prediction, the contrast pair, the delivery modes, the given interior in ex-1, the held step and the tag choice. Each settled as the inferred array states.

## Machine record

```json
{
 "id": "LSN-CON-10022",
 "kind": "concept",
 "target_id": "BC-CON-10022",
 "unit": "10",
 "skills": [
  "BC-SKL-10057",
  "BC-SKL-10058",
  "BC-SKL-10059"
 ],
 "prediction": {
  "id": "pr-1",
  "stem": {
   "text": "The ratio test shows \\(\\sum_{n=1}^{\\infty}\\frac{5(x+2)^n}{4^n\\,n}\\) converges for \\(-6<x<2\\) and is silent at the ends. What happens at \\(x=-6\\) and \\(x=2\\)?",
   "command_verb": "predict"
  },
  "format": "mcq",
  "options": [
   {
    "id": "A",
    "label": "Converges at both",
    "is_key": false
   },
   {
    "id": "B",
    "label": "Converges at \\(-6\\) only",
    "is_key": true
   },
   {
    "id": "C",
    "label": "Diverges at both",
    "is_key": false
   },
   {
    "id": "D",
    "label": "Converges at \\(2\\) only",
    "is_key": false
   }
  ],
  "resolution": "At \\(x=-6\\) the series is \\(5\\sum\\frac{(-1)^n}{n}\\), at \\(x=2\\) it is \\(5\\sum\\frac1n\\). Different series, each needing its own test.",
  "sources": [
   "BC-CON-10022",
   "research/units/unit-10-infinite-sequences-series.md#10.13 Radius and Interval of Convergence of Power Series"
  ]
 },
 "no_figure_reason": "No skill carries a figure-bearing representation (the topic names series, symbolic and verbal forms) and no key idea describes a process, since each endpoint is a numerical series tested on its own.",
 "orientation": {
  "text": "After the ratio test gives the interior, each endpoint is tested on its own. A response shows both endpoint series, a named test at each with its conditions met, and matching brackets.",
  "sources": [
   "BC-CON-10022",
   "research/units/unit-10-infinite-sequences-series.md#10.13 Radius and Interval of Convergence of Power Series"
  ]
 },
 "key_ideas": [
  {
   "id": "ki-1",
   "ek_id": "BC-EK-LIM-8D4",
   "depth": "core",
   "text": "The radius gives an open interval, but both endpoints must be tested. Put each endpoint in place of \\(x\\), not the index; a negative displacement brings \\((-1)^n\\). The ends can differ, so each gets its own test.",
   "notation": "interval of convergence; endpoint series",
   "quote": null,
   "sources": [
    "BC-EK-LIM-8D4",
    "ced:198",
    "sg-25:25",
    "research/units/unit-10-infinite-sequences-series.md#10.13 Radius and Interval of Convergence of Power Series"
   ]
  },
  {
   "id": "ki-2",
   "ek_id": "BC-EK-LIM-8D2",
   "depth": "extended",
   "text": "A convergent power series converges at one point or on an interval. An end is included where its test shows convergence and left out where it shows divergence, so each end takes its own bracket.",
   "notation": "interval of convergence",
   "quote": null,
   "sources": [
    "BC-EK-LIM-8D2",
    "ced:198"
   ]
  }
 ],
 "strategy": [
  {
   "id": "st-1",
   "archetype_id": "BC-QA-10013",
   "cue": "A series in \\((x-r)^n\\) and the interval of convergence requested.",
   "method": "The interior from the ratio test, then each endpoint tested, then brackets.",
   "rival": "The open interval alone.",
   "separating_feature": "Interval asks for both verdicts.",
   "sources": [
    "BC-QA-10013"
   ],
   "evidence_tag": "verified",
   "contrast": {
    "this": {
     "text": "Find the interval of convergence of \\(\\sum_{n=1}^{\\infty}\\frac{7(x-1)^n}{3^n\\sqrt n}\\), justifying each endpoint.",
     "archetype_id": "BC-QA-10013"
    },
    "not_this": {
     "text": "Find the radius of convergence of \\(\\sum_{n=1}^{\\infty}\\frac{7(x-1)^n}{3^n\\sqrt n}\\).",
     "why_not": "It asks for \\(R\\) alone."
    },
    "feature": "Interval needs endpoint verdicts."
   }
  },
  {
   "id": "st-2",
   "archetype_id": "BC-QA-10015",
   "cue": "A power series with its radius and one endpoint value.",
   "method": "The endpoint put in place of \\(x\\), simplified to a series of numbers, then the test its signs allow.",
   "rival": "A comparison test on an alternating endpoint series.",
   "separating_feature": "Alternating terms take the alternating series test; positive terms take p-series or comparison.",
   "sources": [
    "BC-QA-10015"
   ],
   "evidence_tag": "verified"
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
    "coefficient": 5,
    "start": 1
   },
   "problem": {
    "text": "Find the interval of convergence of \\(\\sum_{n=1}^{\\infty}\\frac{5(x+2)^n}{4^n\\,n}\\), justifying each endpoint. The ratio test gives \\(|x+2|<4\\).",
    "command_verb": "find"
   },
   "calculator_status": "no_calculator",
   "steps": [
    {
     "cue": "\\(|x+2|<4\\) gives \\(-6<x<2\\).",
     "why": "The ratio limit is 1 at each end."
    },
    {
     "cue": "Put \\(x=2\\) in place of \\(x\\).",
     "why": "\\(\\frac{4^n}{4^n}=1\\), leaving a positive series.",
     "expr": "Sum(5/n, (n, 1, oo))",
     "relation": "new"
    },
    {
     "cue": "Put \\(x=-6\\) in place of \\(x\\).",
     "why": "\\((-4)^n\\) over \\(4^n\\) leaves \\((-1)^n\\).",
     "expr": "Sum(5*(-1)**n/n, (n, 1, oo))",
     "relation": "new",
     "point_type_id": "BC-PT-99045"
    },
    {
     "cue": "Test each series.",
     "why": "Positive, \\(p=1\\): diverges. Alternating, sizes fall to 0: converges."
    },
    {
     "cue": "Match brackets to verdicts.",
     "why": "Closed where it converges, open where it diverges.",
     "expr": "Interval.Ropen(-6, 2)",
     "relation": "new"
    }
   ],
   "answer": {
    "form": "symbolic",
    "expr": "Interval.Ropen(-6, 2)"
   }
  },
  {
   "id": "ex-2",
   "archetype_id": "BC-QA-10015",
   "bands": [
    "low"
   ],
   "fade_from": 3,
   "parameter_draw": {
    "form": "power",
    "power": "3/2",
    "sign": "positive",
    "end": "right",
    "given": "value",
    "centre": 1,
    "radius": 3,
    "shift": 2
   },
   "problem": {
    "text": "The series \\(\\sum_{n=1}^{\\infty}\\frac{(x-1)^n}{3^n\\,n^{3/2}}\\) has radius of convergence 3. Determine whether it converges or diverges at \\(x=4\\), naming the test.",
    "command_verb": "determine"
   },
   "calculator_status": "no_calculator",
   "steps": [
    {
     "cue": "\\(x=4\\) is the right end, \\(1+3\\).",
     "why": "The ratio test is silent there, so substitute.",
     "expr": "(x-1)**n/(3**n*n**(3/2))",
     "relation": "new"
    },
    {
     "cue": "Put \\(x=4\\) in place of \\(x\\).",
     "why": "\\(\\frac{3^n}{3^n}=1\\) leaves positive terms.",
     "expr": "1/n**(3/2)",
     "relation": "evaluate",
     "subs": {
      "x": "4"
     }
    },
    {
     "cue": "Terms of the form \\(\\frac1{n^p}\\).",
     "why": "A p-series with \\(p=\\frac32>1\\) converges."
    },
    {
     "cue": "State the verdict at the endpoint.",
     "why": "It converges by the p-series test, so \\(x=4\\) is in the interval."
    }
   ],
   "answer": {
    "form": "statement",
    "expr": "Converges by the p-series test, since p = 3/2 > 1, so x = 4 is in the interval."
   }
  }
 ],
 "what_a_reader_scores": [
  {
   "example_id": "ex-1",
   "point_type_ids": [
    "BC-PT-99045"
   ],
   "lines": [
    {
     "point_type_id": "BC-PT-99045",
     "text": "Considers both endpoints. Earned by: Substituting both endpoints of the interval and writing the two resulting series (sg-25:25, sg-22:20). Not earned by: Considering one endpoint only (sg-22:21)."
    }
   ]
  }
 ],
 "common_errors": [
  {
   "error_id": "BC-ERR-10015",
   "observed_behavior": "The response applies a comparison test to an alternating series, or applies the alternating series test to a series of positive terms.",
   "scoring_consequence": "The analysis point at that endpoint is lost, and the interval point with it (sg-25:25).",
   "wrong_step": {
    "text": "At \\(x=-6\\), tested as \\(\\sum\\frac5n\\) by the p-series test.",
    "expr": "5/n"
   },
   "right_step": {
    "text": "At \\(x=-6\\), tested as \\(\\sum\\frac{5(-1)^n}{n}\\) by the alternating series test.",
    "expr": "5*(-1)**n/n"
   },
   "relation": "distinct",
   "fix_prompt": true,
   "possible_reason": null,
   "sources": [
    "BC-ERR-10015",
    "sg-25:25"
   ]
  },
  {
   "error_id": "BC-ERR-10034",
   "observed_behavior": "The response substitutes the endpoint for the index rather than for the variable, or drops the alternating factor produced by a negative endpoint.",
   "scoring_consequence": "The endpoint series is wrong, so the analysis and interval points are lost (sg-25:25).",
   "wrong_step": {
    "text": "\\(x=-6\\) put in place of the index \\(n\\).",
    "expr": "5*(x+2)**(-6)/(4**(-6)*(-6))"
   },
   "right_step": {
    "text": "\\(x=-6\\) put in place of \\(x\\).",
    "expr": "5*(-1)**n/n"
   },
   "relation": "distinct",
   "fix_prompt": true,
   "possible_reason": null,
   "sources": [
    "BC-ERR-10034",
    "sg-25:25"
   ]
  },
  {
   "error_id": "BC-ERR-10037",
   "observed_behavior": "The response reports the open interval found from the ratio test as the interval of convergence without examining either endpoint.",
   "scoring_consequence": "Both the endpoint consideration point and the interval point are lost (sg-25:24).",
   "wrong_step": {
    "text": "The open interval \\(-6<x<2\\).",
    "expr": "Interval.open(-6, 2)"
   },
   "right_step": {
    "text": "\\(-6\\le x<2\\).",
    "expr": "Interval.Ropen(-6, 2)"
   },
   "relation": "distinct",
   "fix_prompt": true,
   "possible_reason": null,
   "sources": [
    "BC-ERR-10037",
    "sg-25:24"
   ]
  },
  {
   "error_id": "BC-ERR-10038",
   "observed_behavior": "The response tests the endpoints correctly and then writes an interval whose brackets do not match the findings, or attaches a closed bracket to an unbounded end.",
   "scoring_consequence": "The final interval point requires the interval to match the analysis (sg-25:25).",
   "wrong_step": {
    "text": "Closed at the diverging end: \\(-6<x\\le2\\).",
    "expr": "Interval.Lopen(-6, 2)"
   },
   "right_step": {
    "text": "Closed at the converging end: \\(-6\\le x<2\\).",
    "expr": "Interval.Ropen(-6, 2)"
   },
   "relation": "distinct",
   "fix_prompt": true,
   "possible_reason": null,
   "sources": [
    "BC-ERR-10038",
    "sg-25:25"
   ]
  }
 ],
 "representations": null,
 "prerequisite_bridges": [
  {
   "prq_id": "BC-PRQ-06002",
   "text": "\\(\\frac{1}{\\sqrt n}=n^{-1/2}\\)."
  },
  {
   "prq_id": "BC-PRQ-06005",
   "text": "Replace \\(x\\) everywhere by \\(-6\\)."
  },
  {
   "prq_id": "BC-PRQ-10006",
   "text": "Round brackets open an end, square close it."
  },
  {
   "prq_id": "BC-PRQ-10008",
   "text": "Keep any \\((-1)^n\\) in the nth term."
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
    4,
    5
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
    "coefficient": 5,
    "start": 1
   },
   "completes": "ex-1",
   "stem": {
    "text": "At \\(x=-6\\) the series \\(5\\sum\\frac{(-1)^n}{n}\\) converges, and at \\(x=2\\) the series \\(5\\sum\\frac1n\\) diverges. Write the interval of convergence.",
    "command_verb": "write"
   },
   "key": {
    "form": "symbolic",
    "expr": "Interval.Ropen(-6, 2)"
   },
   "steps": [
    {
     "text": "Closed at -6, open at 2.",
     "expr": "Interval.Ropen(-6, 2)",
     "relation": "new"
    }
   ],
   "calculator_status": "no_calculator",
   "skills": [
    "BC-SKL-10059"
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
    "sign": "alternating",
    "centre": 2,
    "radius": 5,
    "coefficient": 4,
    "start": 1
   },
   "stem": {
    "text": "Find the interval of convergence of \\(\\sum_{n=1}^{\\infty}\\frac{4(-1)^n(x-2)^n}{5^n\\,n}\\), justifying each endpoint. The ratio test gives \\(|x-2|<5\\).",
    "command_verb": "find"
   },
   "key": {
    "form": "symbolic",
    "expr": "Interval.Lopen(-3, 7)"
   },
   "steps": [
    {
     "text": "At x = 7 the series alternates and converges.",
     "expr": "Sum(4*(-1)**n/n, (n, 1, oo))",
     "relation": "new"
    },
    {
     "text": "At x = -3 the signs cancel and the series diverges.",
     "expr": "Sum(4/n, (n, 1, oo))",
     "relation": "new"
    },
    {
     "text": "Open at -3, closed at 7.",
     "expr": "Interval.Lopen(-3, 7)",
     "relation": "new"
    }
   ],
   "calculator_status": "no_calculator",
   "skills": [
    "BC-SKL-10057",
    "BC-SKL-10058",
    "BC-SKL-10059"
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
    "power": "1/2",
    "sign": "positive",
    "centre": 3,
    "radius": 2,
    "coefficient": 2,
    "start": 1
   },
   "stem": {
    "text": "The interval of convergence of \\(\\sum_{n=1}^{\\infty}\\frac{2(x-3)^n}{2^n\\sqrt n}\\), where the ratio test gives \\(|x-3|<2\\), is",
    "command_verb": "identify"
   },
   "key": {
    "form": "symbolic",
    "expr": "Interval.Ropen(1, 5)"
   },
   "steps": [
    {
     "text": "At x = 5 the series is a p-series with p = 1/2, which diverges.",
     "expr": "Sum(2/sqrt(n), (n, 1, oo))",
     "relation": "new"
    },
    {
     "text": "At x = 1 the series alternates with sizes decreasing to 0, which converges.",
     "expr": "Sum(2*(-1)**n/sqrt(n), (n, 1, oo))",
     "relation": "new"
    },
    {
     "text": "Closed at 1, open at 5.",
     "expr": "Interval.Ropen(1, 5)",
     "relation": "new"
    }
   ],
   "options": [
    {
     "id": "A",
     "is_key": false,
     "expr": "Interval.open(1, 5)",
     "label": "\\(1<x<5\\)",
     "error_path": "BC-ERR-10037",
     "derivation": "the open interval from the ratio test reported with both ends untested"
    },
    {
     "id": "B",
     "is_key": false,
     "expr": "Interval.Lopen(1, 5)",
     "label": "\\(1<x\\le5\\)",
     "error_path": "BC-ERR-10038",
     "derivation": "the brackets placed the other way round from the verdicts"
    },
    {
     "id": "C",
     "is_key": true,
     "expr": "Interval.Ropen(1, 5)",
     "label": "\\(1\\le x<5\\)",
     "error_path": null
    },
    {
     "id": "D",
     "is_key": false,
     "expr": "Interval(1, 5)",
     "label": "\\(1\\le x\\le5\\)",
     "error_path": "BC-ERR-10015",
     "derivation": "the alternating series test applied to the positive series at x = 5, which is called convergent"
    }
   ],
   "calculator_status": "no_calculator",
   "skills": [
    "BC-SKL-10058",
    "BC-SKL-10059"
   ]
  }
 ],
 "delivery": [
  {
   "block": "pr-1",
   "mode": "text",
   "reason": "rule 6: a question on two numerical series, no figure-bearing representation",
   "sources": [
    "BC-SKL-10057"
   ]
  },
  {
   "block": "orientation",
   "mode": "text",
   "reason": "rule 6: a statement of what a response shows",
   "sources": [
    "BC-CON-10022"
   ]
  },
  {
   "block": "ki-1",
   "mode": "text",
   "reason": "rule 6: BC-REP-11, 01 and 04 on BC-SKL-10057 to 10059, none figure-bearing",
   "sources": [
    "BC-SKL-10057",
    "BC-SKL-10058"
   ]
  },
  {
   "block": "ki-2",
   "mode": "text",
   "reason": "rule 6: BC-REP-01 and 04 on BC-SKL-10059",
   "sources": [
    "BC-SKL-10059"
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
   "block": "err-BC-ERR-10015",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  },
  {
   "block": "err-BC-ERR-10034",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  },
  {
   "block": "err-BC-ERR-10037",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  },
  {
   "block": "err-BC-ERR-10038",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  }
 ],
 "refresher": [
  "ki-1",
  "err-BC-ERR-10015",
  "err-BC-ERR-10034",
  "err-BC-ERR-10037",
  "err-BC-ERR-10038",
  "ex-1"
 ],
 "research_lines": [
  {
   "file": "research/units/unit-10-infinite-sequences-series.md",
   "line": "Naming an appropriate test at each endpoint suffices for the analysis"
  }
 ],
 "inferred": [
  {
   "claim": "The prediction, the contrast pair and the delivery modes are teaching decisions, not record facts.",
   "settles": "The modality A/B and first-attempt data on the prediction."
  },
  {
   "claim": "ex-1 states the ratio test result in the problem and folds it into one unvalued step, because the ratio steps belong to BC-CON-10021.",
   "settles": "A rubric part that supplies the interior and asks for the endpoints alone."
  },
  {
   "claim": "A fluent solver writes the two endpoint series, the tests and the interval, and holds the ratio result.",
   "settles": "Timing data per step once the fluency telemetry exists."
  },
  {
   "claim": "ex-1 tags the endpoint point only; BC-PT-99046 is earned by the last step but untagged, and BC-PT-99042 to 99044 are not exercised because the interior is given. The reader lines do not fit the brief band beside the prediction and contrast pair.",
   "settles": "An archetype draw that gives the interior and asks for the endpoints."
  }
 ],
 "sources": [
  "BC-CON-10022",
  "BC-SKL-10057",
  "BC-SKL-10058",
  "BC-SKL-10059",
  "BC-EK-LIM-8D2",
  "BC-EK-LIM-8D4",
  "ced:198",
  "BC-QA-10013",
  "BC-QA-10015",
  "BC-PT-99045",
  "BC-PT-99046",
  "BC-ERR-10015",
  "BC-ERR-10034",
  "BC-ERR-10037",
  "BC-ERR-10038",
  "BC-PRQ-06002",
  "BC-PRQ-06005",
  "BC-PRQ-10006",
  "BC-PRQ-10008",
  "sg-25:24",
  "sg-25:25",
  "research/units/unit-10-infinite-sequences-series.md#10.13 Radius and Interval of Convergence of Power Series",
  "research/exam/exam-structure.md#Section and part layout"
 ],
 "word_count": {
  "full": 715,
  "brief": 446
 },
 "read_minutes": {
  "full": 4.8,
  "brief": 3.0
 }
}
```
