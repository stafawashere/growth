---
title: LSN-CON-10021 Radius of convergence from the ratio test
research_date: 2026-09-29
status: designed
purpose: Authoring spec for the concept lesson on BC-CON-10021, the radius of convergence read from the limit of the ratio of consecutive terms of a power series, built from authoring_bundle("BC-CON-10021") and the research files it cites, so an author fills plan 15's lesson record without making a teaching decision.
---

# LSN-CON-10021 Radius of convergence from the ratio test

Concept BC-CON-10021 (skills BC-SKL-10054, BC-SKL-10055, BC-SKL-10056), topic 10.13 of Unit 10, BC only (ced:198), loaded by two archetypes, BC-QA-10014 and BC-QA-10013 (family radius-interval). Hard parents BC-CON-10012 (the ratio test) and BC-CON-10020 (the centre) (docs/lessons/unit-10/README.md, section 1).

## Prediction

Served first, both bands: an `mcq` on ex-1's own numbers. The ratio limit of \(\sum\frac{2n(x-3)^n}{4^n}\) is given as \(\frac{|x-3|}{4}\), and the student says for which \(x\) the ratio test shows convergence. Key B, \(-1<x<7\). The distractors are \(x<7\) (one bound only) and \(-4<x<4\) (the radius read as an interval about 0). The question is answerable from the ratio test alone (BC-CON-10012, a hard parent) with no rule of this lesson: a limit below 1 is the condition. The resolution states the distance from the centre and names it the radius, with no verdict. Source: BC-CON-10021 and research/units/unit-10-infinite-sequences-series.md#10.13 Radius and Interval of Convergence of Power Series.

## Orientation

Served text (41 words), from BC-CON-10021 `description_plain` ("the ratio test turns a power series into an inequality that bounds the distance from the centre") and the topic's Assessment behaviour paragraph: MCQ forms ask for the radius or the interval, one FRQ form asks only for the radius with points for the ratio, the limit and the explicit radius (sg-21:24, research/units/unit-10-infinite-sequences-series.md#10.13 Radius and Interval of Convergence of Power Series). No count, no frequency.

## Key ideas

Three essential knowledge statements meet the skills (ced:198): ki-1 (core) BC-EK-LIM-8D3, the ratio test gives the radius, with the notation line "R; open interval of radius R" and the index rule of BC-ERR-10021 (BC-SKL-10031's habit carried in); ki-2 (extended) BC-EK-LIM-8D2, a convergent power series converges at one point or on an interval; ki-3 (extended) BC-EK-LIM-8D4, the radius gives an open interval and the interior is a two sided inequality (sg-22:21, sg-25:25). No anchor quote: each CED sentence adds nothing the paraphrase lacks. Core serves both bands, extended the low band.

## Recognition

BC-QA-10014 (research/question-analysis/question-archetypes.md#BC-QA-10014 Radius of convergence from a given series): `common_givens` "a Maclaurin or Taylor series in sigma notation" and "an instruction to use the ratio test"; `asked_to_produce` "the radius of convergence stated as a value"; `typical_wording` "determine the radius of convergence of the series". BC-QA-10013 (research/question-analysis/question-archetypes.md#BC-QA-10013 Interval of convergence by the ratio test with endpoint analysis) loads BC-SKL-10054 and 10055 and asks for "the interior of the interval" as part of the interval. Official parts: BC-FRQ-2021-Q6-C, 2014-Q6-A, 2015-Q6-A, 2024-Q6-D (radius), BC-FRQ-2012-Q6-A, 2022-Q6-A, 2025-Q6-A (interval), MCQ BC-MCQ-PE2012-013 and PE2012-022.

What in the stem says this concept: a power series in \((x-r)^n\) and the word radius, or the words ratio test with an interval whose interior is wanted. What says not this concept: the endpoints are to be tested and the answer is an interval with brackets (BC-CON-10022), or the terms are numbers with no \(x\) (BC-CON-10012). The near miss of the contrast pair is the interval stem on the same series, the README's radius against interval row (docs/lessons/unit-10/README.md, section 3).

## Method choice

- st-1, BC-QA-10014. Cue from `common_givens` and `asked_to_produce`. Method, `expected_solution_path`: ratio, limit, limit below one solved for the displacement, radius stated. Rival from `wrong_approaches`: "solving the ratio inequality into an interval without naming the radius" and "running the ratio test without absolute values". Separating feature: the word radius. Carries the contrast pair: a radius stem beside an interval stem on one series.
- st-2, BC-QA-10013. The same ratio and limit, the interior as a compound inequality; rival "stopping at the open interval" narrowed to the interior here, since the endpoints belong to BC-CON-10022. Served in the low band only.
No served field opens with the reader's own label.

## Solution path

- ex-1, BC-QA-10014, both bands. Draw: form divided, centre 3, base 4, power 1, coefficient 2, start 1, giving \(\sum\frac{2n(x-3)^n}{4^n}\), radius 4. No published item on BC-QA-10014 carries this draw (content/items_gen_*/ITM-GEN-10014-00 to 04). Steps: the ratio simplified, the limit (limit relation), and \(R=4\), whose cue carries the inequality.
- ex-2, low band, BC-QA-10013. Draw: power 2, sign positive, centre -1, radius 3, coefficient 4, start 1, giving \(\sum\frac{4(x+1)^n}{3^n n^2}\), interior \(-4<x<2\). No published item on BC-QA-10013 carries this draw. It stops at the interior, since the endpoints are BC-CON-10022.
- ex-2 is faded from step 3: the ratio and the limit are shown, and the student writes the interior before steps 3 and 4 reveal. The fade falls there because the two shown steps repeat ex-1's pattern, and the inequality and its two sided form are what the student must produce.
- A fluent solver writes all three steps and holds the cancellation and the inequality inside step 3 (Time). No productive-failure comparison: BC-CON-10021 is not in `PRODUCTIVE_FAILURE_TARGETS`.

## Scoring

BC-QA-10014 lists BC-PT-99042, 99043 and 99047; BC-QA-10013 lists BC-PT-99042 to 99046. ex-1 tags BC-PT-99047 only, since the reader lines of BC-PT-99042 and 99043 do not fit the brief band beside the prediction and contrast pair (inferred array). ex-2 tags BC-PT-99043 and 99044; BC-PT-99042 is earned but untagged for the same reason in the low band, and BC-PT-99045 and 99046 are left to BC-CON-10022 because ex-2 stops at the interior. The lines are `reader_checks` output.

Point losses from research: an interval alone does not earn the radius point (sg-21:24, research/units/unit-10-infinite-sequences-series.md#10.13 Radius and Interval of Convergence of Power Series); a bare absolute value inequality is not sufficient for the interior and a one sided bound is insufficient (sg-22:21, sg-25:25); a reciprocal ratio keeps every point except the final interval point (sg-25:25); limit notation is required for the limit point (BC-PT-99043 `notation_requirements`, sg-25:25).

## Traps

Four errors meet the skills, in bundle order: BC-ERR-10036, BC-ERR-99037, BC-ERR-10017, BC-ERR-10021. Low band all four, mid band the first two. Blocks 10036, 10017 and 10021 sit on ex-1's draw; 99037 sits on ex-2's draw because it concerns the interior.

- err-BC-ERR-10036: the interval \(-1<x<7\) in place of \(R=4\). Distinct, fix prompt. No possible reason line (brief band words).
- err-BC-ERR-99037: \(x<2\) in place of \(-4<x<2\). Distinct, fix prompt.
- err-BC-ERR-10017: the same value, \(\frac{|x-3|}{4}\), with and without the limit symbol. Equivalent, no fix prompt, since the difference lives in the sentence.
- err-BC-ERR-10021: \(n+1\) in the power of \(x-3\) but not in \(4^n\), the limit \(|x-3|\) in place of \(\frac{|x-3|}{4}\). Distinct, fix prompt.

## Representations

None. The topic's Representations paragraph names BC-REP-11, 01 and 04 and the conversions series to ratio and limit, inequality to interval; nothing figure-shaped (docs/lessons/unit-10/README.md, section 6).

## Prerequisite bridge

- BC-PRQ-10001, 10002, 10004, 10006, 10007, each from its `description_plain` and `failure_signature`, one short paragraph each.

## Time

ex-1 is the MCQ shape "the radius of the series": Section I Part A, 2.14 minutes (research/exam/exam-structure.md#Section and part layout). As a free response part: 3 points, 5.0 minutes (docs/lessons/unit-10/README.md, section 5). A fluent solver writes the simplified ratio, the limit with its notation and the radius; the cancellation and the inequality are held. The minutes go on the ratio with \(n+1\) in every place.

## Checks

- chk-1, completion of ex-1, both bands: the limit is given, the radius asked. Key 4.
- chk-2, isomorph, both bands. Draw: form multiplied, centre 2, base 5, power 2, coefficient 3, start 1. Key \(\frac15\), radius the reciprocal of the base.
- chk-3, MCQ, low band. Draw: form divided, centre 1, base 7, power 3, coefficient 3, start 2. Key \(R=7\). Distractors: \(-6<x<8\) (BC-ERR-10036), \(R=1\) (BC-ERR-10021), \(R=8\) (BC-ERR-99037, the one sided bound read as the radius, [inferred]).

## Delivery

- prediction, orientation, ki-1, ki-2, ki-3: text. Rule 6: the skills carry BC-REP-11, 01 and 04, none figure-bearing. No block is drawn, so the record carries `no_figure_reason`: no figure-bearing representation and no process idea, since the radius is read from an inequality.
- ex-1, ex-2, the four error blocks: step_reveal. Rule 1.

## Band plan

- Low (full): prediction, orientation, five bridges, ki-1 to ki-3, st-1 with the contrast pair, st-2, ex-1 and its lines, chk-1, four error blocks, ex-2 (faded from step 3) and its lines, chk-2, chk-3. 876 words, 5.9 minutes.
- Mid (brief): prediction, orientation, bridges, ki-1, st-1 with the contrast pair, ex-1 and its lines, chk-1, err-BC-ERR-10036, err-BC-ERR-99037, chk-2. 425 words, 2.9 minutes.
- Refresher: ki-1, the four error blocks, ex-1.

## Sources

- BC-CON-10021; BC-SKL-10054, BC-SKL-10055, BC-SKL-10056; BC-EK-LIM-8D2, BC-EK-LIM-8D3, BC-EK-LIM-8D4; ced:198
- BC-QA-10014, BC-QA-10013; BC-PT-99042, BC-PT-99043, BC-PT-99044, BC-PT-99047
- BC-ERR-10036, BC-ERR-99037, BC-ERR-10017, BC-ERR-10021
- BC-PRQ-10001, BC-PRQ-10002, BC-PRQ-10004, BC-PRQ-10006, BC-PRQ-10007
- sg-21:24, sg-22:21, sg-25:24, sg-25:25, cr-22:30
- research/units/unit-10-infinite-sequences-series.md#10.13 Radius and Interval of Convergence of Power Series
- research/exam/exam-structure.md#Section and part layout
- [inferred] the prediction, the contrast pair, the delivery modes, the held steps, the one sided bound distractor and the tag choice. Each settled as the inferred array states.

## Machine record

```json
{
 "id": "LSN-CON-10021",
 "kind": "concept",
 "target_id": "BC-CON-10021",
 "unit": "10",
 "skills": [
  "BC-SKL-10054",
  "BC-SKL-10055",
  "BC-SKL-10056"
 ],
 "prediction": {
  "id": "pr-1",
  "stem": {
   "text": "For \\(\\sum_{n=1}^{\\infty}\\frac{2n(x-3)^n}{4^n}\\) the ratio of consecutive terms tends to \\(\\frac{|x-3|}{4}\\). For which \\(x\\) does the ratio test show convergence?",
   "command_verb": "predict"
  },
  "format": "mcq",
  "options": [
   {
    "id": "A",
    "label": "\\(x<7\\)",
    "is_key": false
   },
   {
    "id": "B",
    "label": "\\(-1<x<7\\)",
    "is_key": true
   },
   {
    "id": "C",
    "label": "\\(-4<x<4\\)",
    "is_key": false
   }
  ],
  "resolution": "The limit is below 1 exactly when \\(|x-3|<4\\): \\(x\\) lies within 4 of the centre. That distance is the radius.",
  "sources": [
   "BC-CON-10021",
   "research/units/unit-10-infinite-sequences-series.md#10.13 Radius and Interval of Convergence of Power Series"
  ]
 },
 "no_figure_reason": "No skill carries a figure-bearing representation (the topic names series, symbolic and verbal forms) and no key idea describes a process, since the radius is read from an inequality.",
 "orientation": {
  "text": "The ratio test turns a power series into an inequality bounding the distance from the centre. A response shows the ratio, its limit with limit notation, and the radius named as \\(R=\\) a number. An interval alone does not name it.",
  "sources": [
   "BC-CON-10021",
   "research/units/unit-10-infinite-sequences-series.md#10.13 Radius and Interval of Convergence of Power Series"
  ]
 },
 "key_ideas": [
  {
   "id": "ki-1",
   "ek_id": "BC-EK-LIM-8D3",
   "depth": "core",
   "text": "The ratio test gives the radius of convergence. Form \\(\\left|\\frac{a_{n+1}}{a_n}\\right|\\) with \\(n+1\\) in every place \\(n\\) appears, take its limit, and require it below 1. That bounds \\(|x-r|\\) by a number, the radius \\(R\\).",
   "notation": "R; open interval of radius R",
   "quote": null,
   "sources": [
    "BC-EK-LIM-8D3",
    "ced:198",
    "sg-25:25",
    "research/units/unit-10-infinite-sequences-series.md#10.13 Radius and Interval of Convergence of Power Series"
   ]
  },
  {
   "id": "ki-2",
   "ek_id": "BC-EK-LIM-8D2",
   "depth": "extended",
   "text": "A convergent power series converges at one point only or on an interval around its centre. The ratio inequality \\(|x-r|<R\\) describes the interior of that interval.",
   "notation": "interval around the centre",
   "quote": null,
   "sources": [
    "BC-EK-LIM-8D2",
    "ced:198"
   ]
  },
  {
   "id": "ki-3",
   "ek_id": "BC-EK-LIM-8D4",
   "depth": "extended",
   "text": "The radius gives the open interval \\(r-R<x<r+R\\). Solve \\(|x-r|<R\\) as a two-sided inequality, since one bound alone drops half the interval. The endpoints are a separate question that needs its own tests.",
   "notation": "open interval of radius R",
   "quote": null,
   "sources": [
    "BC-EK-LIM-8D4",
    "ced:198",
    "sg-22:21"
   ]
  }
 ],
 "strategy": [
  {
   "id": "st-1",
   "archetype_id": "BC-QA-10014",
   "cue": "A series with an \\((x-r)^n\\) factor and the radius requested.",
   "method": "The ratio, its limit, the limit below 1 solved for \\(|x-r|\\), ending at \\(R=\\).",
   "rival": "An interval, or no absolute values.",
   "separating_feature": "The word radius asks for one number.",
   "sources": [
    "BC-QA-10014"
   ],
   "evidence_tag": "verified",
   "contrast": {
    "this": {
     "text": "Find the radius of convergence of \\(\\sum_{n=1}^{\\infty}\\frac{3^n(x-5)^n}{n^2}\\).",
     "archetype_id": "BC-QA-10014"
    },
    "not_this": {
     "text": "Find the interval of convergence of \\(\\sum_{n=1}^{\\infty}\\frac{3^n(x-5)^n}{n^2}\\).",
     "why_not": "It asks for the interior and both endpoint verdicts."
    },
    "feature": "Radius is one number; interval adds the endpoints."
   }
  },
  {
   "id": "st-2",
   "archetype_id": "BC-QA-10013",
   "cue": "The same kind of series, with the interval of convergence requested.",
   "method": "The same ratio and limit, then \\(|x-r|<R\\) written as \\(r-R<x<r+R\\).",
   "rival": "Stopping at \\(R\\), or leaving the bound one sided.",
   "separating_feature": "Interval asks for the interior, then both endpoint verdicts.",
   "sources": [
    "BC-QA-10013"
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
    "centre": 3,
    "base": 4,
    "power": 1,
    "coefficient": 2,
    "start": 1
   },
   "problem": {
    "text": "Find the radius of convergence of the power series \\(\\sum_{n=1}^{\\infty}\\frac{2n(x-3)^n}{4^n}\\).",
    "command_verb": "find"
   },
   "calculator_status": "no_calculator",
   "steps": [
    {
     "cue": "Radius asked for: ratio test, \\(n+1\\) in every place.",
     "why": "Powers of \\(x-3\\) and of 4 cancel to one factor each.",
     "expr": "Abs(x-3)*(n+1)/(4*n)",
     "relation": "new"
    },
    {
     "cue": "Limit as \\(n\\to\\infty\\), with limit notation.",
     "why": "\\(\\frac{n+1}{n}\\to1\\) leaves \\(\\frac{|x-3|}{4}\\).",
     "expr": "Abs(x-3)/4",
     "relation": "limit",
     "variable": "n",
     "point": "oo"
    },
    {
     "cue": "Limit below 1 gives \\(|x-3|<4\\).",
     "why": "The prompt says radius, so name the number.",
     "expr": "4",
     "relation": "new",
     "point_type_id": "BC-PT-99047"
    }
   ],
   "answer": {
    "form": "numeric",
    "expr": "4"
   }
  },
  {
   "id": "ex-2",
   "archetype_id": "BC-QA-10013",
   "bands": [
    "low"
   ],
   "fade_from": 3,
   "parameter_draw": {
    "power": "2",
    "sign": "positive",
    "centre": -1,
    "radius": 3,
    "coefficient": 4,
    "start": 1
   },
   "problem": {
    "text": "Use the ratio test to find the open interval on which \\(\\sum_{n=1}^{\\infty}\\frac{4(x+1)^n}{3^n\\,n^2}\\) converges.",
    "command_verb": "find"
   },
   "calculator_status": "no_calculator",
   "steps": [
    {
     "cue": "Interval asked for, so the same ratio first.",
     "why": "Consecutive terms, with \\(n+1\\) in every place.",
     "expr": "Abs(x+1)*n**2/(3*(n+1)**2)",
     "relation": "new"
    },
    {
     "cue": "Take the limit as \\(n\\to\\infty\\).",
     "why": "\\(\\frac{n^2}{(n+1)^2}\\to1\\) leaves \\(\\frac{|x+1|}{3}\\).",
     "expr": "Abs(x+1)/3",
     "relation": "limit",
     "variable": "n",
     "point": "oo",
     "point_type_id": "BC-PT-99043"
    },
    {
     "cue": "Require the limit below 1.",
     "why": "\\(|x+1|<3\\): within 3 of the centre \\(-1\\)."
    },
    {
     "cue": "Split the absolute value into two sides.",
     "why": "A two-sided inequality is the interior.",
     "expr": "Interval.open(-4, 2)",
     "relation": "new",
     "point_type_id": "BC-PT-99044"
    }
   ],
   "answer": {
    "form": "symbolic",
    "expr": "Interval.open(-4, 2)"
   }
  }
 ],
 "what_a_reader_scores": [
  {
   "example_id": "ex-1",
   "point_type_ids": [
    "BC-PT-99047"
   ],
   "lines": [
    {
     "point_type_id": "BC-PT-99047",
     "text": "Radius of convergence stated explicitly. Earned by: An explicit statement of the radius, obtained either from the ratio test inequality or by citing the radius of a related series (sg-21:24, sg-24:22). Not earned by: An interval presented with no identification of the radius, which sg-21:24 states does not earn the point."
    }
   ]
  },
  {
   "example_id": "ex-2",
   "point_type_ids": [
    "BC-PT-99043",
    "BC-PT-99044"
   ],
   "lines": [
    {
     "point_type_id": "BC-PT-99043",
     "text": "Limit of the ratio. Earned by: Correct evaluation of the limit of the ratio, including correct limit notation (sg-22:21, sg-21:24). Not earned by: Any error in simplification or evaluation of the limit, which sg-25:25 states forfeits this point even when the ratio point stands. Notation: sg-22:21 requires correct limit notation and either the absolute value of the ratio or a resolution to a squared inequality; sg-25:25 states a response not using absolute value can still earn both the ratio and the limit points."
    },
    {
     "point_type_id": "BC-PT-99044",
     "text": "Interior of the interval of convergence. Earned by: Resolving the inequality to a two-sided inequality or an interval for the variable (sg-25:25, sg-22:21). Not earned by: An absolute value inequality left unresolved; sg-25:25 states the bare form with the centre and radius is not sufficient unless it is resolved to a two-sided inequality, and sg-22:21 states a one-sided bound is insufficient."
    }
   ]
  }
 ],
 "common_errors": [
  {
   "error_id": "BC-ERR-10036",
   "observed_behavior": "The response solves the inequality and presents an interval without naming the radius as a value.",
   "scoring_consequence": "The radius point cannot be earned by presenting an interval alone (sg-21:24).",
   "wrong_step": {
    "text": "The interval \\(-1<x<7\\).",
    "expr": "Interval.open(-1, 7)"
   },
   "right_step": {
    "text": "\\(R=4\\).",
    "expr": "4"
   },
   "relation": "distinct",
   "fix_prompt": true,
   "possible_reason": null,
   "sources": [
    "BC-ERR-10036",
    "sg-21:24"
   ]
  },
  {
   "error_id": "BC-ERR-99037",
   "observed_behavior": "Responses convert the ratio test inequality into an interval without the absolute value, producing a one sided interval, and related presentations attach the infinity symbol to a square bracket or otherwise misuse interval notation.",
   "scoring_consequence": "The interval point is not earned even where the limit of the ratio was found correctly.",
   "wrong_step": {
    "text": "On the ex-2 series: \\(x<2\\), with the absolute value dropped.",
    "expr": "Interval.open(-oo, 2)"
   },
   "right_step": {
    "text": "\\(-4<x<2\\).",
    "expr": "Interval.open(-4, 2)"
   },
   "relation": "distinct",
   "fix_prompt": true,
   "possible_reason": null,
   "sources": [
    "BC-ERR-99037",
    "cr-22:30"
   ]
  },
  {
   "error_id": "BC-ERR-10017",
   "observed_behavior": "The response computes the value of a ratio or a quotient as the index grows without writing the limit symbol.",
   "scoring_consequence": "Limit notation is required for the setup point in a limit comparison (sg-21:23) and for the limit point in a ratio test (sg-25:25).",
   "wrong_step": {
    "text": "\\(\\frac{|x-3|}{4}\\) written beside the ratio with no limit symbol.",
    "expr": "Abs(x-3)/4"
   },
   "right_step": {
    "text": "\\(\\lim_{n\\to\\infty}\\) written in front, then \\(\\frac{|x-3|}{4}\\).",
    "expr": "Abs(x-3)/4"
   },
   "relation": "equivalent",
   "fix_prompt": false,
   "possible_reason": null,
   "sources": [
    "BC-ERR-10017",
    "sg-25:25"
   ]
  },
  {
   "error_id": "BC-ERR-10021",
   "observed_behavior": "The response replaces n by n plus one in some places and not others, for example writing an exponent of two n plus two where two n plus three is required.",
   "scoring_consequence": "A substitution error of this kind keeps the early points but blocks the final interval point (sg-22:21).",
   "wrong_step": {
    "text": "\\(n+1\\) in the power of \\(x-3\\) but not in \\(4^n\\), so the limit is \\(|x-3|\\).",
    "expr": "Abs(x-3)"
   },
   "right_step": {
    "text": "\\(n+1\\) in both, so the limit is \\(\\frac{|x-3|}{4}\\).",
    "expr": "Abs(x-3)/4"
   },
   "relation": "distinct",
   "fix_prompt": true,
   "possible_reason": null,
   "sources": [
    "BC-ERR-10021",
    "sg-22:21"
   ]
  }
 ],
 "representations": null,
 "prerequisite_bridges": [
  {
   "prq_id": "BC-PRQ-10001",
   "text": "\\(|x-3|<4\\) means \\(-1<x<7\\)."
  },
  {
   "prq_id": "BC-PRQ-10002",
   "text": "\\(\\frac{(n+1)!}{n!}=n+1\\)."
  },
  {
   "prq_id": "BC-PRQ-10004",
   "text": "Dominant terms give \\(\\frac{n+1}{n}\\to1\\)."
  },
  {
   "prq_id": "BC-PRQ-10006",
   "text": "Round brackets open an end, square close it."
  },
  {
   "prq_id": "BC-PRQ-10007",
   "text": "Subtract exponents when dividing powers."
  }
 ],
 "time": {
  "exam_part": "I-A",
  "budget_minutes": 2.14,
  "source": "research/exam/exam-structure.md#Section and part layout",
  "written_steps": {
   "ex-1": [
    1,
    2,
    3
   ]
  },
  "skipped_steps": {
   "ex-1": []
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
    "centre": 3,
    "base": 4,
    "power": 1,
    "coefficient": 2,
    "start": 1
   },
   "completes": "ex-1",
   "stem": {
    "text": "The ratio limit is \\(\\frac{|x-3|}{4}\\). State the radius \\(R\\).",
    "command_verb": "state"
   },
   "key": {
    "form": "numeric",
    "expr": "4"
   },
   "steps": [
    {
     "text": "Limit of the ratio.",
     "expr": "Abs(x-3)/4",
     "relation": "new"
    },
    {
     "text": "Below 1 gives \\(|x-3|<4\\), so \\(R=4\\).",
     "expr": "4",
     "relation": "new"
    }
   ],
   "calculator_status": "no_calculator",
   "skills": [
    "BC-SKL-10056"
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
    "centre": 2,
    "base": 5,
    "power": 2,
    "coefficient": 3,
    "start": 1
   },
   "stem": {
    "text": "Find the radius of convergence of \\(\\sum_{n=1}^{\\infty}\\frac{3\\cdot5^n(x-2)^n}{n^2}\\).",
    "command_verb": "find"
   },
   "key": {
    "form": "numeric",
    "expr": "1/5"
   },
   "steps": [
    {
     "text": "Ratio of consecutive terms.",
     "expr": "5*Abs(x-2)*n**2/(n+1)**2",
     "relation": "new"
    },
    {
     "text": "Limit as n grows.",
     "expr": "5*Abs(x-2)",
     "relation": "limit",
     "variable": "n",
     "point": "oo"
    },
    {
     "text": "Below 1 gives \\(|x-2|<\\frac15\\).",
     "expr": "1/5",
     "relation": "new"
    }
   ],
   "calculator_status": "no_calculator",
   "skills": [
    "BC-SKL-10054",
    "BC-SKL-10056"
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
    "centre": 1,
    "base": 7,
    "power": 3,
    "coefficient": 3,
    "start": 2
   },
   "stem": {
    "text": "The radius of convergence of \\(\\sum_{n=2}^{\\infty}\\frac{3n^3(x-1)^n}{7^n}\\) is",
    "command_verb": "identify"
   },
   "key": {
    "form": "numeric",
    "expr": "7"
   },
   "steps": [
    {
     "text": "Ratio of consecutive terms.",
     "expr": "Abs(x-1)*(n+1)**3/(7*n**3)",
     "relation": "new"
    },
    {
     "text": "Limit as n grows.",
     "expr": "Abs(x-1)/7",
     "relation": "limit",
     "variable": "n",
     "point": "oo"
    },
    {
     "text": "Below 1 gives \\(|x-1|<7\\).",
     "expr": "7",
     "relation": "new"
    }
   ],
   "options": [
    {
     "id": "A",
     "is_key": false,
     "expr": "Interval.open(-6, 8)",
     "label": "\\(-6<x<8\\)",
     "error_path": "BC-ERR-10036",
     "derivation": "the interval solved from the inequality and given where the radius was asked for"
    },
    {
     "id": "B",
     "is_key": false,
     "expr": "1",
     "label": "\\(R=1\\)",
     "error_path": "BC-ERR-10021",
     "derivation": "n + 1 put in the power of x - 1 but not in 7^n, so the limit is |x - 1|"
    },
    {
     "id": "C",
     "is_key": true,
     "expr": "7",
     "label": "\\(R=7\\)",
     "error_path": null
    },
    {
     "id": "D",
     "is_key": false,
     "expr": "8",
     "label": "\\(R=8\\)",
     "error_path": "BC-ERR-99037",
     "derivation": "the absolute value dropped, leaving x < 8, and the bound 8 read as the radius"
    }
   ],
   "calculator_status": "no_calculator",
   "skills": [
    "BC-SKL-10054",
    "BC-SKL-10056"
   ]
  }
 ],
 "delivery": [
  {
   "block": "pr-1",
   "mode": "text",
   "reason": "rule 6: a question on a series and an inequality, no figure-bearing representation",
   "sources": [
    "BC-SKL-10054"
   ]
  },
  {
   "block": "orientation",
   "mode": "text",
   "reason": "rule 6: a statement of what a response shows",
   "sources": [
    "BC-CON-10021"
   ]
  },
  {
   "block": "ki-1",
   "mode": "text",
   "reason": "rule 6: BC-REP-11 and 01 on BC-SKL-10054, neither figure-bearing",
   "sources": [
    "BC-SKL-10054"
   ]
  },
  {
   "block": "ki-2",
   "mode": "text",
   "reason": "rule 6",
   "sources": [
    "BC-SKL-10055"
   ]
  },
  {
   "block": "ki-3",
   "mode": "text",
   "reason": "rule 6: BC-REP-01 on BC-SKL-10055",
   "sources": [
    "BC-SKL-10055",
    "BC-SKL-10056"
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
   "block": "err-BC-ERR-10036",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  },
  {
   "block": "err-BC-ERR-99037",
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
  "err-BC-ERR-10036",
  "err-BC-ERR-99037",
  "err-BC-ERR-10017",
  "err-BC-ERR-10021",
  "ex-1"
 ],
 "research_lines": [
  {
   "file": "research/units/unit-10-infinite-sequences-series.md",
   "line": "A radius must be named as a radius; an interval alone does not earn the radius point"
  }
 ],
 "inferred": [
  {
   "claim": "The prediction, the contrast pair and the delivery modes are teaching decisions, not record facts.",
   "settles": "The modality A/B and first-attempt data on the prediction."
  },
  {
   "claim": "A fluent solver writes the ratio, the limit and the radius, and holds the inequality step.",
   "settles": "Timing data per step once the fluency telemetry exists."
  },
  {
   "claim": "BC-ERR-99037 is shown on ex-2's draw, the interval draw, and its option in chk-3 reads the one sided bound as a radius, a chain the record does not state.",
   "settles": "A BC-ERR record for the one sided bound reported as the radius on BC-QA-10014."
  },
  {
   "claim": "Tag choice: ex-1 tags the radius point only and ex-2 the limit and interior points, because the reader lines of the ratio and limit points do not fit the brief band with the prediction and contrast pair.",
   "settles": "A brief cap that admits every reader line."
  }
 ],
 "sources": [
  "BC-CON-10021",
  "BC-SKL-10054",
  "BC-SKL-10055",
  "BC-SKL-10056",
  "BC-EK-LIM-8D2",
  "BC-EK-LIM-8D3",
  "BC-EK-LIM-8D4",
  "ced:198",
  "BC-QA-10014",
  "BC-QA-10013",
  "BC-PT-99042",
  "BC-PT-99043",
  "BC-PT-99044",
  "BC-PT-99047",
  "BC-ERR-10036",
  "BC-ERR-99037",
  "BC-ERR-10017",
  "BC-ERR-10021",
  "BC-PRQ-10001",
  "BC-PRQ-10002",
  "BC-PRQ-10004",
  "BC-PRQ-10006",
  "BC-PRQ-10007",
  "sg-21:24",
  "sg-22:21",
  "sg-25:24",
  "sg-25:25",
  "cr-22:30",
  "research/units/unit-10-infinite-sequences-series.md#10.13 Radius and Interval of Convergence of Power Series",
  "research/exam/exam-structure.md#Section and part layout"
 ],
 "word_count": {
  "full": 875,
  "brief": 424
 },
 "read_minutes": {
  "full": 5.9,
  "brief": 2.9
 }
}
```
