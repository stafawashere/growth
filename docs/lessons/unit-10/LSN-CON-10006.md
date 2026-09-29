---
title: LSN-CON-10006 The integral test and its hypotheses
research_date: 2026-09-29
status: designed
purpose: Authoring spec for the concept lesson on BC-CON-10006, the integral test with its three conditions, the matching improper integral evaluated with limit notation and a conclusion about the series, built from authoring_bundle("BC-CON-10006") and the research files it cites, so an author fills plan 15's lesson record without making a teaching decision.
---

# LSN-CON-10006 The integral test and its hypotheses

Concept BC-CON-10006 (skills BC-SKL-10014, BC-SKL-10015, BC-SKL-10016, BC-SKL-10017), topic 10.4 of Unit 10, BC only (ced:189), loaded by one archetype, BC-QA-10005 (family convergence-test). No Unit 10 hard parent (docs/lessons/unit-10/README.md, section 1); the outside hard parents are BC-SKL-05014, 06034, 06067 and 06068, so the improper integral and the monotonicity test are assumed.

## Prediction

Served first, both bands: an `mcq` on ex-1's own numbers. The function \(f(x)=\frac{6x}{(x^2+2)^2}\) is positive and decreasing for \(x\ge1\) and the area under it from 1 onward is 1 (the value of ex-1's improper integral, a Unit 6 skill). The student says what can be said about \(f(1)+f(2)+f(3)+\cdots\). Key A, finite and larger than 1. The distractors are infinite and finite and equal to 1. A student can rule out the third before any rule: \(f(1)=\frac23\) and \(f(2)=\frac13\) already total 1 and every later term is positive. Width-1 rectangles of height \(f(n)\) fit under a decreasing curve, which shows the sum stays finite. The resolution states this and the integral test's link, with no verdict word. Delivery: text. Source: BC-CON-10006 and the topic 10.4 section that ki-1 cites.

## Orientation

Served text (28 words), from BC-CON-10006 `description_plain` and the topic's Assessment behaviour paragraph: the multiple choice form asks which series the integral test settles or which condition fails, and the free response form asks for the conditions, the improper integral and the evaluation as separate points (research/units/unit-10-infinite-sequences-series.md#10.4 Integral Test for Convergence). The orientation states what a response must show. No count, no frequency.

## Key ideas

All four skills map to one essential knowledge statement, BC-EK-LIM-7A6 (ced:189): one core block, both bands.

- ki-1 (core). Paraphrase of the Required mathematical knowledge paragraphs Integral test (hypotheses and conclusion), Value ("The convergent integral bounds the series but is not its sum") and Improper integral (limit notation, not the infinity symbol; sg-21:22). Notation line: the concept's `notation`. No anchor quote: the ced:189 sentence "The integral test is a method to determine whether a series converges or diverges." adds no content and costs 14 words in the brief band.

## Recognition

BC-QA-10005 (family convergence-test; research/question-analysis/question-archetypes.md#BC-QA-10005 Integral test with its conditions stated) is the only archetype loading the four skills.

- `common_givens`: "a series of numbers with an exponential general term" and "a positive decreasing continuous function whose values give the terms". `asked_to_produce`: the three conditions, the matching improper integral, an evaluation with limit notation, a convergence conclusion for the series. `typical_wording`: "state the conditions necessary to use the integral test, then use the test to show that the series converges".
- Shapes: a free response part of three points, BC-FRQ-2021-Q6-A (sg-21:21, sg-21:22), and the multiple choice item BC-MCQ-SAMPLE-024. The topic's multiple choice forms ask which series the test settles or which hypothesis fails.

The signal in the stem: terms given as the values of a function, the phrase integral test or a request for its conditions, and a function whose antiderivative is available. The near miss of the contrast pair is the improper integral asked alone, an integral-evaluation stem from Unit 6 (BC-CON-06019 teaches its limit process): same function, same lower limit, but no series and no conditions. The feature that separates them is that a series of terms is named.

What says "not this concept": an integral evaluation with no series (Unit 6); a series with a constant ratio or a p-series form, which has its own test (BC-CON-10003, BC-CON-10007); terms that are not positive or not decreasing, where the hypotheses fail.

## Method choice

One strategy block, both bands.

- st-1, BC-QA-10005. Cue from `common_givens` and `asked_to_produce`: terms that are values of a positive function and a request for its conditions. Method, `expected_solution_path[0]`: state that f is positive, decreasing and continuous on the interval. Rival, `wrong_approaches`: infinity written into the antiderivative (BC-ERR-10011) and the integral's value taken as the sum (BC-ERR-10013). Separating feature: the integral decides the series but is not its sum. Both cue fields exist, so the block is verified. The block carries the contrast pair. No served field opens with the reader's own label.

## Solution path

- ex-1, BC-QA-10005, both bands, no calculator. Draw: form squared, start 1, shift 2, coefficient 6. \(f(x)=\frac{6x}{(x^2+2)^2}\), \(f'(x)=\frac{6(2-3x^2)}{(x^2+2)^3}\), integral from 1 to b \(1-\frac{3}{b^2+2}\), limit 1. The constraint `shift < 3 * start ** 2` holds (2 against 3). No published item on BC-QA-10005 carries this draw (content/items_gen_unit10/ITM-GEN-10005-00 to 04 draw forms squared, gaussian and cubic at other values; ITM-AGT-10005-00 to 19 use another draw shape).
- ex-2, low band. Draw: form gaussian, start 2, shift 3, coefficient 4. \(f(x)=4xe^{-3x^2}\), integral value \(\frac23e^{-12}\), so the series converges. Not equal to any published draw.
- ex-2 is faded from step 4: steps 1 to 3 (the function, the conditions, the setup) are shown, the student writes the evaluation, and steps 4 to 6 then reveal. The fade falls there because the conditions and the setup repeat ex-1's pattern and the evaluation with limit notation is what the student must produce.
- Steps follow `expected_solution_path`: the function (new), its derivative for the decreasing condition (differentiate), the improper integral to b (new), the antiderivative evaluated (equivalent, checked against the integral), the limit (limit), and the sentence about the series (no value). A fluent solver writes the conditions, the setup, the evaluation and the verdict; the recognition of \(f(n)\) is held. No productive-failure comparison: BC-CON-10006 is not in `PRODUCTIVE_FAILURE_TARGETS`.

## Scoring

BC-QA-10005 lists BC-PT-99005, 99053 and 99003. ex-1 tags BC-PT-99003 on the antiderivative step only; ex-2 tags BC-PT-99003 and BC-PT-99053. The lines are `reader_checks` output. BC-PT-99005 is untagged: its reader line is generic, 110 words, and does not describe the conditions the archetype's pattern assigns to the first point (inferred array). The conditions point is taught in ki-1 and the error blocks.

Point losses from research: an evaluation written with the infinity symbol does not earn the limit notation point (research/scoring/common-point-losses.md#Notation points, sg-21:22); all three conditions are required for the first point, and an incorrect lower limit costs the setup point while the evaluation stays reachable (README section 4, sg-21:21, sg-21:22).

## Traps

Four errors meet the skills, in the bundle's order (each linked to a high severity BC-MIS, then by id): BC-ERR-10003, BC-ERR-10009, BC-ERR-10010, BC-ERR-10011. BC-ERR-10012 (wrong lower limit), BC-ERR-10013 (integral value as the sum) and BC-ERR-10044 fall past the cap of 4; ki-1 and the resolution of the prediction cover the value claim. Low band all four, mid band the first two. All on ex-1's draw.

- err-BC-ERR-10003: "It converges" against the series named. Both steps hold the general term, so the relation is equivalent and the fix prompt false. No possible reason line (brief band words).
- err-BC-ERR-10009: the test named with no conditions, the empty set, against the conditions on \([1,\infty)\). Distinct, fix prompt true. No possible reason line (brief band words); the record links BC-MIS-10007 and BC-MIS-99009.
- err-BC-ERR-10010: one condition stated, against all three, counted as 1 and 3. Distinct, fix prompt true. No possible reason line.
- err-BC-ERR-10011: the infinity symbol substituted, against the limit written. Both give 1, so the relation is equivalent and the fix prompt false. Possible reason, BC-MIS-99008.

## Representations

None. The topic's Representations paragraph names BC-REP-01, 11 and 04 and the conversions series general term to a function of x and integral value to a statement about the series; nothing figure-shaped (docs/lessons/unit-10/README.md, section 6).

## Prerequisite bridge

BC-PRQ-06002, BC-PRQ-06003, BC-PRQ-06005 and BC-PRQ-06013, each from its `description_plain` and `failure_signature`, gated by state, in both bands.

## Time

Section II Part B, 15.0 minutes per question (research/exam/exam-structure.md#Section and part layout), the FRQ shape BC-FRQ-2021-Q6-A; the three points take 5.0 minutes of it (docs/lessons/unit-10/README.md, section 5). The multiple choice form would take 2.14 minutes [inferred]. A fluent solver writes the conditions, the improper integral, the evaluation with limit notation and the verdict; the recognition of \(f(n)\) is held. The minutes go on the antiderivative.

## Checks

- chk-1, completion of ex-1, both bands. The integral to b given, the improper integral asked. Key 1.
- chk-2, isomorph, both bands, no calculator. Draw: form squared, start 2, shift 5, coefficient 8 (constraint 5 against 12 holds). \(f(x)=\frac{8x}{(x^2+5)^2}\), integral from 2 to infinity \(\frac49\). Not equal to a published draw.
- chk-3, MCQ, low band. Draw: form plain, start 3, shift 4, coefficient 2 (constraint 4 against 10 holds). \(f(x)=\frac{2x}{x^2+4}\), the integral to b is \(\ln(b^2+4)-\ln13\), which grows without bound. Key: the complete argument. Distractors: only positivity stated (BC-ERR-10010); the infinity symbol substituted, giving \(\infty\) (BC-ERR-10011); the conclusion with no series named (BC-ERR-10003).

## Delivery

- orientation, ki-1: text. Rule 6: BC-REP-01, 04, 11, none figure-bearing (docs/lessons/unit-10/README.md, section 6). No block is drawn, so the record carries `no_figure_reason`.
- ex-1, ex-2, the four error blocks: step_reveal. Rule 1.

## Band plan

- Low (full): prediction, orientation, bridges, ki-1, st-1 with the contrast pair, ex-1 and its line, chk-1, the four error blocks, ex-2 (faded from step 4) and its lines, chk-2, chk-3. 807 words, 5.4 minutes.
- Mid (brief): prediction, orientation, bridges, ki-1, st-1 with the contrast pair, ex-1 and its line, chk-1, err-BC-ERR-10003, err-BC-ERR-10009, chk-2. 450 words, 3.0 minutes.
- Refresher: ki-1, the four error blocks, ex-1.

## Sources

- BC-CON-10006; BC-SKL-10014, BC-SKL-10015, BC-SKL-10016, BC-SKL-10017; BC-EK-LIM-7A6; ced:189
- BC-QA-10005; BC-PT-99003, BC-PT-99053, BC-PT-99005
- BC-ERR-10003, BC-ERR-10009, BC-ERR-10010, BC-ERR-10011; BC-MIS-99008
- BC-PRQ-06002, BC-PRQ-06003, BC-PRQ-06005, BC-PRQ-06013
- sg-21:22
- research/units/unit-10-infinite-sequences-series.md#10.4 Integral Test for Convergence
- research/question-analysis/question-archetypes.md#BC-QA-10005 Integral test with its conditions stated
- research/scoring/common-point-losses.md#Notation points
- research/exam/exam-structure.md#Section and part layout
- [inferred] the held step, the point tags, Part B for the FRQ shape and the delivery choice, each settled as the inferred array states.

## Machine record

```json
{
 "id": "LSN-CON-10006",
 "kind": "concept",
 "target_id": "BC-CON-10006",
 "unit": "10",
 "skills": [
  "BC-SKL-10014",
  "BC-SKL-10015",
  "BC-SKL-10016",
  "BC-SKL-10017"
 ],
 "prediction": {
  "id": "pr-1",
  "stem": {
   "text": "\\(f(x)=\\frac{6x}{(x^2+2)^2}\\) is positive and decreasing for \\(x\\ge1\\), and its area from \\(x=1\\) onward is 1. What can be said about \\(f(1)+f(2)+f(3)+\\cdots\\)?",
   "command_verb": "predict"
  },
  "format": "mcq",
  "options": [
   {
    "id": "A",
    "label": "It is finite, and larger than 1.",
    "is_key": true
   },
   {
    "id": "B",
    "label": "It is infinite.",
    "is_key": false
   },
   {
    "id": "C",
    "label": "It is finite, and equal to 1.",
    "is_key": false
   }
  ],
  "resolution": "The first two terms already total 1, so the sum exceeds the area, yet unit rectangles under the curve keep it finite. The integral test links them: series and integral both converge or both diverge.",
  "sources": [
   "BC-CON-10006",
   "research/units/unit-10-infinite-sequences-series.md#10.4 Integral Test for Convergence"
  ]
 },
 "no_figure_reason": "The test pairs a series with an improper integral through written conditions and limit notation. No skill carries a figure-bearing representation, and the limit process itself is taught in the Unit 6 lesson.",
 "orientation": {
  "text": "A response states the three conditions on the function, evaluates the matching improper integral with limit notation, and concludes about the series, not the integral's value.",
  "sources": [
   "BC-CON-10006",
   "research/units/unit-10-infinite-sequences-series.md#10.4 Integral Test for Convergence"
  ]
 },
 "key_ideas": [
  {
   "id": "ki-1",
   "ek_id": "BC-EK-LIM-7A6",
   "depth": "core",
   "text": "Let \\(a_n=f(n)\\) with f positive, decreasing and continuous on \\([s,\\infty)\\). Then \\(\\sum a_n\\) and \\(\\int_s^{\\infty}f(x)\\,dx\\) both converge or both diverge. The integral's value is not the series' sum. Evaluate with \\(\\lim_{b\\to\\infty}\\), never with the infinity symbol.",
   "notation": "improper integral; positive, decreasing, continuous",
   "quote": null,
   "sources": [
    "BC-EK-LIM-7A6",
    "ced:189",
    "sg-21:22",
    "research/units/unit-10-infinite-sequences-series.md#10.4 Integral Test for Convergence"
   ]
  }
 ],
 "strategy": [
  {
   "id": "st-1",
   "archetype_id": "BC-QA-10005",
   "cue": "Terms that are values of a positive function, and a request for its conditions.",
   "method": "\\(f\\) positive, decreasing and continuous on \\([s,\\infty)\\).",
   "rival": "Infinity written into the antiderivative, or the integral's value reported as the sum.",
   "separating_feature": "The integral decides the series but is not its sum.",
   "sources": [
    "BC-QA-10005",
    "research/question-analysis/question-archetypes.md#BC-QA-10005 Integral test with its conditions stated"
   ],
   "evidence_tag": "verified",
   "contrast": {
    "this": {
     "text": "Let \\(f(x)=\\frac{3x}{(x^2+1)^2}\\), \\(a_n=f(n)\\). State the integral test conditions for \\(\\sum_{n=1}^{\\infty}a_n\\) and decide convergence.",
     "archetype_id": "BC-QA-10005"
    },
    "not_this": {
     "text": "Evaluate \\(\\int_1^{\\infty}\\frac{3x}{(x^2+1)^2}\\,dx\\).",
     "why_not": "It asks for an improper integral's value, with no series or conditions."
    },
    "feature": "A series of terms is named, so the answer is about the series."
   }
  }
 ],
 "worked_examples": [
  {
   "id": "ex-1",
   "archetype_id": "BC-QA-10005",
   "bands": [
    "low",
    "mid"
   ],
   "parameter_draw": {
    "form": "squared",
    "start": "1",
    "shift": "2",
    "coefficient": "6"
   },
   "problem": {
    "text": "Let \\(f(x)=\\frac{6x}{(x^2+2)^2}\\), \\(a_n=f(n)\\). State the conditions for \\(\\sum_{n=1}^{\\infty}a_n\\), evaluate the improper integral with limit notation, and conclude.",
    "command_verb": "determine"
   },
   "calculator_status": "no_calculator",
   "steps": [
    {
     "cue": "Terms are \\(f(n)\\).",
     "why": "The test needs f on \\([1,\\infty)\\).",
     "expr": "6*x/(x**2+2)**2",
     "relation": "new"
    },
    {
     "cue": "Check the three conditions.",
     "why": "Positive, continuous, and \\(f'<0\\) there.",
     "expr": "6*(2-3*x**2)/(x**2+2)**3",
     "relation": "differentiate",
     "variable": "x"
    },
    {
     "cue": "Improper integral from 1.",
     "why": "Lower limit is the start index.",
     "expr": "Integral(6*x/(x**2+2)**2,(x,1,b))",
     "relation": "new"
    },
    {
     "cue": "Antiderivative \\(-\\frac{3}{x^2+2}\\).",
     "why": "Substitute \\(u=x^2+2\\).",
     "expr": "1 - 3/(b**2+2)",
     "relation": "equivalent",
     "point_type_id": "BC-PT-99003"
    },
    {
     "cue": "Let \\(b\\to\\infty\\).",
     "why": "Use limit notation.",
     "expr": "1",
     "relation": "limit",
     "variable": "b",
     "point": "oo"
    },
    {
     "cue": "The integral converges.",
     "why": "So the series converges. Its sum is not 1."
    }
   ],
   "answer": {
    "form": "numeric",
    "expr": "1"
   }
  },
  {
   "id": "ex-2",
   "archetype_id": "BC-QA-10005",
   "bands": [
    "low"
   ],
   "fade_from": 4,
   "parameter_draw": {
    "form": "gaussian",
    "start": "2",
    "shift": "3",
    "coefficient": "4"
   },
   "problem": {
    "text": "Let \\(f(x)=4xe^{-3x^2}\\), \\(a_n=f(n)\\). State the conditions for \\(\\sum_{n=2}^{\\infty}a_n\\), evaluate the improper integral with limit notation, and conclude.",
    "command_verb": "determine"
   },
   "calculator_status": "no_calculator",
   "steps": [
    {
     "cue": "Terms are \\(f(n)\\).",
     "why": "The test needs f on \\([2,\\infty)\\).",
     "expr": "4*x*exp(-3*x**2)",
     "relation": "new"
    },
    {
     "cue": "Check the three conditions.",
     "why": "Positive, continuous, and \\(f'=4e^{-3x^2}(1-6x^2)<0\\) there.",
     "expr": "4*exp(-3*x**2)*(1-6*x**2)",
     "relation": "differentiate",
     "variable": "x"
    },
    {
     "cue": "Improper integral from 2.",
     "why": "Lower limit is the start index.",
     "expr": "Integral(4*x*exp(-3*x**2),(x,2,b))",
     "relation": "new"
    },
    {
     "cue": "Antiderivative \\(-\\frac23e^{-3x^2}\\).",
     "why": "Substitute \\(u=-3x^2\\); evaluate from 2 to b.",
     "expr": "2*exp(-12)/3 - 2*exp(-3*b**2)/3",
     "relation": "equivalent",
     "point_type_id": "BC-PT-99003"
    },
    {
     "cue": "Let \\(b\\to\\infty\\).",
     "why": "The exponential term tends to 0, in limit notation.",
     "expr": "2*exp(-12)/3",
     "relation": "limit",
     "variable": "b",
     "point": "oo",
     "point_type_id": "BC-PT-99053"
    },
    {
     "cue": "The integral converges.",
     "why": "So the series converges. Its sum is not the integral's value."
    }
   ],
   "answer": {
    "form": "numeric",
    "expr": "2*exp(-12)/3"
   }
  }
 ],
 "what_a_reader_scores": [
  {
   "example_id": "ex-1",
   "point_type_ids": [
    "BC-PT-99003"
   ],
   "lines": [
    {
     "point_type_id": "BC-PT-99003",
     "text": "Antiderivative. Earned by: A correct antiderivative of the presented integrand, with or without the constant of integration (sg-25:14). Not earned by: An antiderivative of the wrong form, or a jump from integral to value with no antiderivative shown (sg-26:18)."
    }
   ]
  },
  {
   "example_id": "ex-2",
   "point_type_ids": [
    "BC-PT-99003",
    "BC-PT-99053"
   ],
   "lines": [
    {
     "point_type_id": "BC-PT-99003",
     "text": "Antiderivative. Earned by: A correct antiderivative of the presented integrand, with or without the constant of integration (sg-25:14). Not earned by: An antiderivative of the wrong form, or a jump from integral to value with no antiderivative shown (sg-26:18)."
    },
    {
     "point_type_id": "BC-PT-99053",
     "text": "Limit notation on an improper integral. Earned by: Replacing the infinite limit with a variable and writing the limit of the resulting expression, applied to the integral or to an antiderivative of the correct form (sg-26:20). Not earned by: Arithmetic with infinity written in place of a limit, which sg-23:17, sg-22:19 and sg-26:20 all treat as a failure of this point. Notation: sg-23:17 requires correct limit notation throughout; sg-26:20 banks the point once correct notation appears, so later arithmetic with infinity does not remove it, which is a change from the earlier treatment."
    }
   ]
  }
 ],
 "common_errors": [
  {
   "error_id": "BC-ERR-10003",
   "observed_behavior": "With several series present in one part, the response concludes that the series converges without identifying which one.",
   "scoring_consequence": "The explanation point is not earned, because the reader cannot tell which series the claim is about (sg-21:23).",
   "wrong_step": {
    "text": "It converges.",
    "expr": "6*n/(n**2+2)**2"
   },
   "right_step": {
    "text": "\\(\\sum a_n\\) converges.",
    "expr": "6*n/(n**2+2)**2"
   },
   "relation": "equivalent",
   "possible_reason": null,
   "sources": [
    "BC-ERR-10003"
   ],
   "fix_prompt": false
  },
  {
   "error_id": "BC-ERR-10009",
   "observed_behavior": "The response names a convergence test and states a conclusion without establishing the conditions the test requires.",
   "scoring_consequence": "Points tied to the conditions or to the justification are lost even when the verdict is right (sg-21:22).",
   "wrong_step": {
    "text": "Integral test, so it converges.",
    "expr": "EmptySet"
   },
   "right_step": {
    "text": "\\(f>0\\), continuous, decreasing on \\([1,\\infty)\\).",
    "expr": "Interval(1, oo)"
   },
   "relation": "distinct",
   "possible_reason": null,
   "sources": [
    "BC-ERR-10009"
   ],
   "fix_prompt": true
  },
  {
   "error_id": "BC-ERR-10010",
   "observed_behavior": "The response applies the integral test without stating that the function is positive, decreasing, and continuous, or states only one or two of the three.",
   "scoring_consequence": "The conditions point requires all three properties to be listed (sg-21:22).",
   "wrong_step": {
    "text": "One condition stated.",
    "expr": "1"
   },
   "right_step": {
    "text": "All three conditions.",
    "expr": "3"
   },
   "relation": "distinct",
   "possible_reason": null,
   "sources": [
    "BC-ERR-10010"
   ],
   "fix_prompt": true
  },
  {
   "error_id": "BC-ERR-10011",
   "observed_behavior": "The response substitutes the infinity symbol into the antiderivative, or opens with limit notation and abandons it before the evaluation is finished.",
   "scoring_consequence": "The evaluation point requires correct limit notation; an evaluation written with the infinity symbol does not earn it (sg-21:22).",
   "wrong_step": {
    "text": "\\(1-\\frac{3}{\\infty^2+2}=1\\).",
    "expr": "1 - 3/(oo**2 + 2)"
   },
   "right_step": {
    "text": "\\(\\lim_{b\\to\\infty}\\left(1-\\frac{3}{b^2+2}\\right)=1\\).",
    "expr": "1"
   },
   "relation": "equivalent",
   "possible_reason": {
    "misconception_id": "BC-MIS-99008",
    "text": "substitutes the infinity symbol for the variable"
   },
   "sources": [
    "BC-ERR-10011",
    "BC-MIS-99008"
   ],
   "fix_prompt": false
  }
 ],
 "representations": null,
 "prerequisite_bridges": [
  {
   "prq_id": "BC-PRQ-06002",
   "text": "Rewrite reciprocals as powers."
  },
  {
   "prq_id": "BC-PRQ-06003",
   "text": "Keep absolute value inside logarithms."
  },
  {
   "prq_id": "BC-PRQ-06005",
   "text": "Tell \\(f'\\) from \\(f\\)."
  },
  {
   "prq_id": "BC-PRQ-06013",
   "text": "The integration variable is internal."
  }
 ],
 "time": {
  "exam_part": "II-B",
  "budget_minutes": 15.0,
  "source": "research/exam/exam-structure.md#Section and part layout",
  "written_steps": {
   "ex-1": [
    2,
    3,
    4,
    5,
    6
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
   "archetype_id": "BC-QA-10005",
   "parameter_draw": {
    "form": "squared",
    "start": "1",
    "shift": "2",
    "coefficient": "6"
   },
   "completes": "ex-1",
   "stem": {
    "text": "For \\(f(x)=\\frac{6x}{(x^2+2)^2}\\), \\(\\int_1^b f\\,dx=1-\\frac{3}{b^2+2}\\). Evaluate \\(\\int_1^{\\infty}f\\,dx\\) with limit notation.",
    "command_verb": "evaluate"
   },
   "key": {
    "form": "numeric",
    "expr": "1"
   },
   "steps": [
    {
     "text": "The integral to b.",
     "expr": "1 - 3/(b**2+2)",
     "relation": "new"
    },
    {
     "text": "Its limit as b grows.",
     "expr": "1",
     "relation": "limit",
     "variable": "b",
     "point": "oo"
    }
   ],
   "calculator_status": "no_calculator",
   "skills": [
    "BC-SKL-10016"
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
   "archetype_id": "BC-QA-10005",
   "parameter_draw": {
    "form": "squared",
    "start": "2",
    "shift": "5",
    "coefficient": "8"
   },
   "stem": {
    "text": "Let \\(f(x)=\\frac{8x}{(x^2+5)^2}\\). Evaluate \\(\\int_2^{\\infty}f\\,dx\\) with limit notation.",
    "command_verb": "evaluate"
   },
   "key": {
    "form": "numeric",
    "expr": "4/9"
   },
   "steps": [
    {
     "text": "The integral from 2 to b.",
     "expr": "Integral(8*x/(x**2+5)**2,(x,2,b))",
     "relation": "new"
    },
    {
     "text": "Antiderivative \\(-\\frac{4}{x^2+5}\\), evaluated.",
     "expr": "4/9 - 4/(b**2+5)",
     "relation": "equivalent"
    },
    {
     "text": "The limit as b grows.",
     "expr": "4/9",
     "relation": "limit",
     "variable": "b",
     "point": "oo"
    }
   ],
   "calculator_status": "no_calculator",
   "skills": [
    "BC-SKL-10016"
   ]
  },
  {
   "id": "chk-3",
   "check_kind": "mcq",
   "format": "mcq",
   "bands": [
    "low"
   ],
   "archetype_id": "BC-QA-10005",
   "parameter_draw": {
    "form": "plain",
    "start": "3",
    "shift": "4",
    "coefficient": "2"
   },
   "stem": {
    "text": "Let \\(f(x)=\\frac{2x}{x^2+4}\\), \\(a_n=f(n)\\). Which response is a complete integral test argument for \\(\\sum_{n=3}^{\\infty}a_n\\)?",
    "command_verb": "identify"
   },
   "key": {
    "form": "statement",
    "expr": "all three conditions, limit notation, the series named as diverging"
   },
   "steps": [
    {
     "text": "The integral to b.",
     "expr": "Integral(2*x/(x**2+4),(x,3,b))",
     "relation": "new"
    },
    {
     "text": "Antiderivative \\(\\ln(x^2+4)\\), evaluated.",
     "expr": "log(b**2+4) - log(13)",
     "relation": "equivalent"
    }
   ],
   "options": [
    {
     "id": "A",
     "is_key": true,
     "label": "\\(\\sum a_n\\) diverges: \\(f\\) is positive, decreasing, continuous on \\([3,\\infty)\\), and \\(\\lim_{b\\to\\infty}\\int_3^b f\\,dx=\\infty\\).",
     "error_path": null
    },
    {
     "id": "B",
     "is_key": false,
     "label": "\\(\\sum a_n\\) diverges: \\(f\\) is positive on \\([3,\\infty)\\), and \\(\\lim_{b\\to\\infty}\\int_3^b f\\,dx=\\infty\\).",
     "error_path": "BC-ERR-10010",
     "derivation": "only one of the three conditions stated"
    },
    {
     "id": "C",
     "is_key": false,
     "label": "\\(\\sum a_n\\) diverges: the conditions hold, and \\(\\ln(\\infty^2+4)-\\ln 13=\\infty\\).",
     "error_path": "BC-ERR-10011",
     "derivation": "the infinity symbol substituted, giving \\(\\infty\\), in place of a limit"
    },
    {
     "id": "D",
     "is_key": false,
     "label": "It diverges: the conditions hold, and \\(\\lim_{b\\to\\infty}\\int_3^b f\\,dx=\\infty\\).",
     "error_path": "BC-ERR-10003",
     "derivation": "the conclusion stated with no series named"
    }
   ],
   "calculator_status": "no_calculator",
   "skills": [
    "BC-SKL-10014",
    "BC-SKL-10017"
   ]
  }
 ],
 "delivery": [
  {
   "block": "orientation",
   "mode": "text",
   "reason": "rule 6: a statement of what a response shows",
   "sources": [
    "BC-CON-10006"
   ]
  },
  {
   "block": "ki-1",
   "mode": "text",
   "reason": "rule 6: BC-REP-01, 04, 11 on BC-SKL-10014 to 10017, none figure-bearing; the improper integral's limit process is taught in the Unit 6 lesson (docs/lessons/unit-10/README.md, section 6)",
   "sources": [
    "BC-SKL-10014",
    "BC-SKL-10015",
    "BC-SKL-10016",
    "BC-SKL-10017"
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
   "block": "err-BC-ERR-10003",
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
   "block": "err-BC-ERR-10010",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  },
  {
   "block": "err-BC-ERR-10011",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  }
 ],
 "refresher": [
  "ki-1",
  "err-BC-ERR-10003",
  "err-BC-ERR-10009",
  "err-BC-ERR-10010",
  "err-BC-ERR-10011",
  "ex-1"
 ],
 "read_minutes": {
  "full": 5.4,
  "brief": 3.0
 },
 "word_count": {
  "full": 806,
  "brief": 449
 },
 "research_lines": [
  {
   "file": "research/units/unit-10-infinite-sequences-series.md",
   "line": "The convergent integral bounds the series but is not its sum."
  }
 ],
 "inferred": [
  {
   "claim": "A fluent solver holds the recognition of f(n) and writes the conditions, the setup, the evaluation and the verdict.",
   "settles": "Timing data per step once the fluency telemetry exists."
  },
  {
   "claim": "The point tags: BC-PT-99005 is generic and 110 words as a reader line, so ex-1 tags only BC-PT-99003 to fit the brief cap and ex-2 adds BC-PT-99053; the conditions point is taught in ki-1 and the error blocks.",
   "settles": "A brief cap that admits the reader lines, or a BC-PT for the conditions."
  },
  {
   "claim": "The time budget is Section II Part B for the FRQ shape; a multiple choice form would take 2.14 minutes.",
   "settles": "Timing data on integral test items split by exam part."
  },
  {
   "claim": "The delivery choice serves better than the alternatives.",
   "settles": "The modality A/B in the build plan: skip rate and time to first credited success by mode."
  }
 ],
 "sources": [
  "BC-CON-10006",
  "BC-SKL-10014",
  "BC-SKL-10015",
  "BC-SKL-10016",
  "BC-SKL-10017",
  "BC-EK-LIM-7A6",
  "ced:189",
  "BC-QA-10005",
  "BC-PT-99003",
  "BC-PT-99005",
  "BC-PT-99053",
  "BC-ERR-10003",
  "BC-ERR-10009",
  "BC-ERR-10010",
  "BC-ERR-10011",
  "BC-MIS-99008",
  "BC-PRQ-06002",
  "BC-PRQ-06003",
  "BC-PRQ-06005",
  "BC-PRQ-06013",
  "BC-REP-01",
  "research/exam/exam-structure.md#Section and part layout",
  "research/question-analysis/question-archetypes.md#BC-QA-10005 Integral test with its conditions stated",
  "research/units/unit-10-infinite-sequences-series.md#10.4 Integral Test for Convergence",
  "sg-21:22",
  "sg-21:23",
  "sg-22:19",
  "sg-23:17",
  "sg-25:14",
  "sg-26:18",
  "sg-26:20"
 ]
}
```
