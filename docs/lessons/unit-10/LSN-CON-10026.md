---
title: LSN-CON-10026 Radius preserved and endpoints rechecked
research_date: 2026-09-29
status: designed
purpose: Authoring spec for the concept lesson on BC-CON-10026, the radius of a differentiated or integrated power series carried over unchanged, its endpoints tested again, and convergence to the function decided at a stated input, built from authoring_bundle("BC-CON-10026") and the research files it cites, so an author fills plan 15's lesson record without making a teaching decision.
---

# LSN-CON-10026 Radius preserved and endpoints rechecked

Concept BC-CON-10026 (skills BC-SKL-10070, BC-SKL-10071, BC-SKL-10073), topic 10.15 of Unit 10, BC only (ced:198 and ced:200), loaded by three archetypes, BC-QA-10018 (family taylor-construction), BC-QA-10015 (family radius-interval) and BC-QA-10020 (family taylor-error). Hard parents inside the unit are BC-CON-10021, BC-CON-10022 and BC-CON-10025 (docs/lessons/unit-10/README.md, section 1): the ratio test radius, the interval with its endpoint tests and term-by-term operations are assumed.

## Prediction

Served first, both bands: an `mcq` on ex-1's numbers. The stem gives the general term of \(f'\) and asks what the series does at \(x=3\). Key B, diverges. The distractor is converges, the verdict \(f\) itself has at 3. The p-series and harmonic series facts from the prerequisite concepts answer it before any rule about derived series is stated: the terms at 3 are \(\frac{3}{2n}\). The resolution states the harmonic multiple and that an endpoint can change, with no verdict on the student's choice. Source: BC-CON-10026 and the topic section.

## Orientation

Served text, from BC-CON-10026 `description_plain` ("The derived series reaches just as far, but the ends may behave differently") and the topic's Assessment behaviour paragraph (research/units/unit-10-infinite-sequences-series.md#10.15 Representing Functions as Power Series): the FRQ asks for the radius of the differentiated series resting on the preservation statement, and for a reasoned decision about convergence at a specific input, where naming the position relative to the interval earns the point. The orientation states what a response shows. No count, no frequency.

## Key ideas

Four essential knowledge statements map from the three skills. ki-1 (core) is BC-EK-LIM-8D6 (ced:198), the preserved radius. ki-2 (core) is BC-EK-LIM-8D4 (ced:198), the open interval and both endpoints tested. ki-3 (extended, low band only) is BC-EK-LIM-8D5 (ced:198), the series as the Taylor series of the function on the open interval. ki-4 (extended) is BC-EK-LIM-8D2 (ced:198), convergence at a point or on an interval, with the position-as-reason sentence taken from the `scoring_pattern` of BC-QA-10020 (inferred array). No anchor quote: each CED sentence adds nothing the paraphrase lacks and costs words in the brief band.

## Recognition

BC-QA-10018 (research/question-analysis/question-archetypes.md#BC-QA-10018 Series differentiated term by term with its radius carried over) loads BC-SKL-10070 and 10071. `common_givens`: "the radius of convergence of the original series", "a power series with its general term". `asked_to_produce`: "the radius of convergence of the derivative series". `difficulty_variables`: "whether the endpoints must be rechecked". Shapes: BC-FRQ-2024-Q6-C, BC-FRQ-2025-Q6-B, BC-FRQ-2026-Q6-B, BC-MCQ-CED-020.

BC-QA-10015 (research/question-analysis/question-archetypes.md#BC-QA-10015 Endpoint series identified and tested) loads BC-SKL-10071. `common_givens`: "a power series with its radius of convergence", "an endpoint value of x". `asked_to_produce`: "the numerical series at the endpoint", "a convergence or divergence verdict with a named test". It lists no point types.

BC-QA-10020 (research/question-analysis/question-archetypes.md#BC-QA-10020 Convergence to the function at a specified input decided with a reason) loads BC-SKL-10073. `common_givens`: "an interval of convergence from an earlier part", "a specific input". `asked_to_produce`: "a yes or no verdict on convergence to the function at the input", "a reason placing the input relative to the interval". Shape: BC-FRQ-2025-Q6-D.

The near miss of the contrast pair is a fresh series whose interval is asked with no earlier series given. It belongs to the interval of convergence archetype (BC-QA-10013, BC-CON-10022) and calls for the ratio test, the rival named in `common_distractors` of BC-QA-10018, so it comes from outside BC-QA-10018 (docs/lessons/unit-10/README.md, section 3, radius against interval).

## Method choice

- st-1, BC-QA-10018. Cue from `common_givens` and `asked_to_produce`. Method from `expected_solution_path`: state the radius unchanged, recheck the endpoints. Rival: `common_distractors` "recomputing and misreporting the radius", "carrying the original interval including its endpoints". Separating feature: a derived series inherits the radius, never the endpoints. Carries the contrast pair.
- st-2, BC-QA-10015. Method: substitute the endpoint, simplify, name a test whose conditions it meets. Rival: `wrong_approaches` "applying a comparison test to an alternating endpoint series (BC-ERR-10015)".
- st-3, BC-QA-10020. Method: state the interval, locate the input, give the position as the reason. Rival: `common_distractors` "answering with no reason", "treating the series as valid for all inputs".
All three archetypes carry both cue fields, so none is inferred. No served field opens with the reader's own label.

## Solution path

- ex-1, BC-QA-10018, both bands, no calculator. Draw: sign positive, given interval, centre 1, base 2, coefficient 3. \(f=\sum\frac{3(x-1)^n}{n^22^n}\) on \([-1,3]\); \(f'\) has terms \(\frac{3(x-1)^{n-1}}{n2^n}\), which are \(\frac{3}{2n}\) at 3 and \(\frac{3(-1)^{n-1}}{2n}\) at \(-1\), checked with SymPy. Key \([-1,3)\). No published item on BC-QA-10018 carries this draw.
- ex-2, BC-QA-10020, low band, no calculator. Draw: case geometric_left, framing radius_given, centre 1, radius 3, coefficient 2. \(f(x)=\frac{6}{4-x}\), series \(2\sum\left(\frac{x-1}{3}\right)^n\), interval \((-2,4)\), input \(-2\), where \(f(-2)=1\) and the series diverges. The answer is a statement.
- ex-2 is faded from step 3: steps 1 and 2 (the interval and the input's position) are shown, the student writes the verdict and reason, and steps 3 and 4 then reveal. The fade falls there because the interval and the location repeat ex-1's endpoint habit and the verdict with its position is what the student must produce.
- Relations: the interval steps are new, since no expression relation links an endpoint verdict to an interval. A fluent solver writes the open interval, the endpoint verdicts and the interval, and holds the simplification of each endpoint series (Time). No productive-failure comparison: BC-CON-10026 is not in `PRODUCTIVE_FAILURE_TARGETS`.

## Scoring

BC-QA-10018 lists BC-PT-99037, 99038, 99067, 99047, 99035 and 99036, BC-QA-10020 lists BC-PT-99005 and BC-QA-10015 lists none. Neither example tags a point type and both scoring entries are empty. ex-1 leaves out BC-PT-99047, whose 45 word line does not fit the 450 word brief band once the prediction and contrast pair are served. ex-2 leaves out BC-PT-99005, whose record describes a value with its setup and not the answer with a reason that BC-QA-10020's `scoring_pattern` names (inferred array).

Point losses from research: the radius point rests on the preservation statement, so an inconsistent value loses it (sg-24:22); the answer with reason needs the position relative to the interval, and a short response naming the input as outside the interval earns it (sg-25:27); endpoints left untested lose the endpoint and interval points (sg-25:24).

## Traps

Six errors meet the skills, in bundle order: BC-ERR-10015, BC-ERR-10037, BC-ERR-10042, BC-ERR-10043, BC-ERR-10038, BC-ERR-99017. The last two fall past the cap of 4. Low band all four, mid band the first two. BC-ERR-10015, 10037 and 10042 are on ex-1's draw, BC-ERR-10043 on ex-2's. All carry `fix_prompt` true, since each pair is distinct. No possible reason lines (brief band words).

- err-BC-ERR-10015: the alternating series test applied to the positive endpoint series at 3. The SymPy pair is the interval the verdict produces, \([-1,3]\) against \([-1,3)\).
- err-BC-ERR-10037: the open interval reported. \((-1,3)\) against \([-1,3)\).
- err-BC-ERR-10042: a radius of 1 against 2.
- err-BC-ERR-10043: a verdict with no interval; the SymPy pair is the empty set against \((-2,4)\).

## Representations

None. The topic's Representations paragraph names BC-REP-11, 01 and 04 and the conversion of an interval of convergence to a verdict about an input; nothing figure-shaped. The unit map notes that a draggable input over the interval would be an interactive reading outside the rules (docs/lessons/unit-10/README.md, section 6).

## Prerequisite bridge

Three bridges, one per BC-PRQ, each from its `description_plain` and `failure_signature`: BC-PRQ-06005 (function notation, f' and f interchanged), BC-PRQ-10006 (interval notation with open and closed endpoints), BC-PRQ-10008 (general term from sigma form). Gated by state, not band.

## Time

ex-1 is the MCQ-shaped draw, Section I Part A, 2.14 minutes (research/exam/exam-structure.md#Section and part layout). As free response parts, the differentiated series shape is 2 points, 3.33 minutes, and the input decision shape 1 point, 1.67 minutes (docs/lessons/unit-10/README.md, section 5). A fluent solver writes the open interval, the endpoint verdicts and the final interval; the simplification of each endpoint series is held [inferred]. The minutes go on naming a test that fits each endpoint series.

## Checks

- chk-1, completion of ex-1, both bands: the radius and both endpoint verdicts given, the interval asked. Key \([-1,3)\).
- chk-2, isomorph, both bands. Draw: sign alternating, given interval, centre 3, base 5, coefficient 2. Terms of \(f'\) at 8 are \(\frac{2(-1)^n}{5n}\), at \(-2\) they are \(-\frac{2}{5n}\). Key \((-2,8]\).
- chk-3, MCQ, low band. Draw: sign positive, given interval, centre -2, base 4, coefficient 5. Key \([-6,2)\). Distractors: \((-6,2)\), endpoints untested (BC-ERR-10037); \([-6,2]\), the alternating series test applied to the positive series at 2 (BC-ERR-10015); \((-5,1)\), the radius recomputed as 3 (BC-ERR-10042).

## Delivery

- orientation, ki-1 to ki-4: text. Rule 5: the skills carry BC-REP-11 and 04, none figure-bearing (docs/lessons/unit-10/README.md, section 6). No block is drawn, so the record carries `no_figure_reason`.
- ex-1, ex-2, the four error blocks: step_reveal. Rule 1.

## Band plan

- Low (full): prediction, orientation, bridges, ki-1 to ki-4, st-1 with the contrast pair, st-2, st-3, ex-1, chk-1, the four error blocks, ex-2 (faded from step 3), chk-2, chk-3. 795 words, 5.3 minutes.
- Mid (brief): prediction, orientation, bridges, ki-1, ki-2, st-1 with the contrast pair, ex-1, chk-1, err-BC-ERR-10015, err-BC-ERR-10037, chk-2. 443 words, 3.0 minutes.
- Refresher: ki-1, ki-2, the four error blocks, ex-1.

## Sources

- BC-CON-10026; BC-SKL-10070, BC-SKL-10071, BC-SKL-10073; BC-EK-LIM-8D6, BC-EK-LIM-8D4, BC-EK-LIM-8D5, BC-EK-LIM-8D2; ced:198, ced:200
- BC-QA-10018, BC-QA-10015, BC-QA-10020; BC-PT-99005, BC-PT-99047
- BC-ERR-10015, BC-ERR-10037, BC-ERR-10042, BC-ERR-10043
- BC-PRQ-06005, BC-PRQ-10006, BC-PRQ-10008
- sg-24:22, sg-25:24, sg-25:27
- research/units/unit-10-infinite-sequences-series.md#10.15 Representing Functions as Power Series
- research/question-analysis/question-archetypes.md#BC-QA-10018 Series differentiated term by term with its radius carried over
- research/question-analysis/question-archetypes.md#BC-QA-10015 Endpoint series identified and tested
- research/question-analysis/question-archetypes.md#BC-QA-10020 Convergence to the function at a specified input decided with a reason
- research/exam/exam-structure.md#Section and part layout
- [inferred] the untagged points; the radius and no-interval encodings of two error pairs; the position-as-reason sentence; the held steps. Each settled as the inferred array states.

## Machine record

```json
{
 "id": "LSN-CON-10026",
 "kind": "concept",
 "target_id": "BC-CON-10026",
 "unit": "10",
 "skills": [
  "BC-SKL-10070",
  "BC-SKL-10071",
  "BC-SKL-10073"
 ],
 "prediction": {
  "id": "pr-1",
  "stem": {
   "text": "\\(f'(x)=\\sum_{n=1}^{\\infty}\\frac{3(x-1)^{n-1}}{n2^n}\\). Predict what this series does at \\(x=3\\).",
   "command_verb": "predict"
  },
  "format": "mcq",
  "options": [
   {
    "id": "A",
    "label": "Converges",
    "is_key": false
   },
   {
    "id": "B",
    "label": "Diverges",
    "is_key": true
   }
  ],
  "resolution": "At \\(x=3\\) the terms are \\(\\frac{3}{2n}\\), a multiple of the harmonic series. The series for \\(f\\) itself converges at 3, so an endpoint can change when the series is differentiated.",
  "sources": [
   "BC-CON-10026",
   "research/units/unit-10-infinite-sequences-series.md#10.15 Representing Functions as Power Series"
  ]
 },
 "no_figure_reason": "No skill carries a figure-bearing representation (the topic names series, symbolic and verbal forms) and no key idea describes a process, since the radius and the endpoint verdicts are stated and tested.",
 "orientation": {
  "text": "A derived series keeps the radius, but its endpoints are tested again. A response states the radius, tests each endpoint series, and places a given input relative to the interval.",
  "sources": [
   "BC-CON-10026",
   "research/units/unit-10-infinite-sequences-series.md#10.15 Representing Functions as Power Series"
  ]
 },
 "key_ideas": [
  {
   "id": "ki-1",
   "ek_id": "BC-EK-LIM-8D6",
   "depth": "core",
   "text": "Term-by-term differentiation or integration leaves the radius of convergence unchanged. It is stated, not recomputed.",
   "notation": "same radius",
   "quote": null,
   "sources": [
    "BC-EK-LIM-8D6",
    "ced:198",
    "research/units/unit-10-infinite-sequences-series.md#10.15 Representing Functions as Power Series"
   ]
  },
  {
   "id": "ki-2",
   "ek_id": "BC-EK-LIM-8D4",
   "depth": "core",
   "text": "The radius gives the open interval. Each endpoint is tested for the new series with a test whose conditions it meets, since the old verdicts need not carry over.",
   "notation": "endpoints retested",
   "quote": null,
   "sources": [
    "BC-EK-LIM-8D4",
    "ced:198",
    "research/units/unit-10-infinite-sequences-series.md#10.15 Representing Functions as Power Series"
   ]
  },
  {
   "id": "ki-3",
   "ek_id": "BC-EK-LIM-8D5",
   "depth": "extended",
   "text": "A power series with positive radius is the Taylor series of the function it converges to, on the open interval.",
   "notation": "series and function",
   "quote": null,
   "sources": [
    "BC-EK-LIM-8D5",
    "ced:198",
    "research/units/unit-10-infinite-sequences-series.md#10.15 Representing Functions as Power Series"
   ]
  },
  {
   "id": "ki-4",
   "ek_id": "BC-EK-LIM-8D2",
   "depth": "extended",
   "text": "A power series that converges does so at a single point or on an interval. To decide convergence at an input, place the input relative to the interval.",
   "notation": "position in the interval",
   "quote": null,
   "sources": [
    "BC-EK-LIM-8D2",
    "ced:198",
    "research/units/unit-10-infinite-sequences-series.md#10.15 Representing Functions as Power Series"
   ]
  }
 ],
 "strategy": [
  {
   "id": "st-1",
   "archetype_id": "BC-QA-10018",
   "cue": "A series with its radius or interval, and the derivative series wanted.",
   "method": "State the same radius, then test each endpoint of the derived series.",
   "rival": "Recomputing the radius, or carrying the original interval over.",
   "separating_feature": "A derived series inherits the radius, never the endpoints.",
   "sources": [
    "BC-QA-10018",
    "research/question-analysis/question-archetypes.md#BC-QA-10018 Series differentiated term by term with its radius carried over"
   ],
   "evidence_tag": "verified",
   "contrast": {
    "this": {
     "text": "The series for \\(f\\) has radius 2 and converges on \\([-1,3]\\). Find the interval of convergence of the series for \\(f'\\).",
     "archetype_id": "BC-QA-10018"
    },
    "not_this": {
     "text": "Find the interval of convergence of \\(\\sum_{n=1}^{\\infty}\\frac{(x-1)^{n-1}}{n2^n}\\).",
     "why_not": "No earlier series is given, so the radius comes from the ratio test."
    },
    "feature": "A derivative of a series with a known radius inherits it; a fresh series needs the ratio test."
   }
  },
  {
   "id": "st-2",
   "archetype_id": "BC-QA-10015",
   "cue": "A power series with its radius, and an endpoint value of \\(x\\).",
   "method": "Put the endpoint in for \\(x\\), simplify to a numerical series, then name a test whose conditions it meets.",
   "rival": "A comparison test on an alternating series, or the other endpoint's verdict.",
   "separating_feature": "The endpoint series is alternating or positive, and that decides the test.",
   "sources": [
    "BC-QA-10015",
    "research/question-analysis/question-archetypes.md#BC-QA-10015 Endpoint series identified and tested"
   ],
   "evidence_tag": "verified"
  },
  {
   "id": "st-3",
   "archetype_id": "BC-QA-10020",
   "cue": "An interval from an earlier part, and a specific input.",
   "method": "State the interval, locate the input, then give that position as the reason.",
   "rival": "A verdict with no reason, or the series taken as valid at every input.",
   "separating_feature": "The input's position relative to the interval decides the verdict.",
   "sources": [
    "BC-QA-10020",
    "research/question-analysis/question-archetypes.md#BC-QA-10020 Convergence to the function at a specified input decided with a reason"
   ],
   "evidence_tag": "verified"
  }
 ],
 "worked_examples": [
  {
   "id": "ex-1",
   "archetype_id": "BC-QA-10018",
   "bands": [
    "low",
    "mid"
   ],
   "parameter_draw": {
    "sign": "positive",
    "given": "interval",
    "centre": 1,
    "base": 2,
    "coefficient": 3
   },
   "problem": {
    "text": "The series for \\(f\\) is \\(\\sum_{n=1}^{\\infty}\\frac{3(x-1)^n}{n^22^n}\\), with interval of convergence \\([-1,3]\\). Find the interval of convergence of the series for \\(f'\\).",
    "command_verb": "find"
   },
   "calculator_status": "no_calculator",
   "steps": [
    {
     "cue": "Differentiating term by term.",
     "why": "The radius stays 2."
    },
    {
     "cue": "Centre 1, radius 2.",
     "why": "Only the interior is inherited.",
     "expr": "Interval.open(-1, 3)",
     "relation": "new"
    },
    {
     "cue": "At \\(x=3\\) the terms are \\(\\frac{3}{2n}\\).",
     "why": "Harmonic multiple, so it diverges."
    },
    {
     "cue": "At \\(x=-1\\) the terms are \\(\\frac{3(-1)^{n-1}}{2n}\\).",
     "why": "Alternating with terms falling to 0, so it converges."
    },
    {
     "cue": "Keep \\(-1\\), drop 3.",
     "why": "Brackets follow the tests.",
     "expr": "Interval.Ropen(-1, 3)",
     "relation": "new"
    }
   ],
   "answer": {
    "form": "symbolic",
    "expr": "Interval.Ropen(-1, 3)"
   }
  },
  {
   "id": "ex-2",
   "archetype_id": "BC-QA-10020",
   "bands": [
    "low"
   ],
   "fade_from": 3,
   "parameter_draw": {
    "case": "geometric_left",
    "framing": "radius_given",
    "centre": 1,
    "radius": 3,
    "coefficient": 2
   },
   "problem": {
    "text": "The series \\(2\\sum_{n=0}^{\\infty}\\left(\\frac{x-1}{3}\\right)^n\\), with radius 3, represents \\(f(x)=\\frac{6}{4-x}\\) inside its interval. Does it converge to \\(f(-2)\\)? Give a reason.",
    "command_verb": "state"
   },
   "calculator_status": "no_calculator",
   "steps": [
    {
     "cue": "Centre 1, radius 3.",
     "why": "This is the interval in play.",
     "expr": "Interval.open(-2, 4)",
     "relation": "new"
    },
    {
     "cue": "The input \\(-2\\) is the left end.",
     "why": "It is not inside the open interval."
    },
    {
     "cue": "At \\(x=-2\\) the series is \\(2\\sum(-1)^n\\).",
     "why": "Its terms do not tend to 0, so it diverges."
    },
    {
     "cue": "State the verdict with its position.",
     "why": "The position is the reason."
    }
   ],
   "answer": {
    "form": "statement",
    "text": "No. The input -2 is an endpoint, not inside (-2, 4), and the series diverges there although f(-2)=1."
   }
  }
 ],
 "what_a_reader_scores": [
  {
   "example_id": "ex-1",
   "point_type_ids": [],
   "lines": []
  },
  {
   "example_id": "ex-2",
   "point_type_ids": [],
   "lines": []
  }
 ],
 "common_errors": [
  {
   "error_id": "BC-ERR-10015",
   "observed_behavior": "The response applies a comparison test to an alternating series, or applies the alternating series test to a series of positive terms.",
   "scoring_consequence": "The analysis point at that endpoint is lost, and the interval point with it (sg-25:25).",
   "wrong_step": {
    "text": "Alternating series test on \\(\\sum\\frac{3}{2n}\\): converges, so 3 is in.",
    "expr": "Interval(-1, 3)"
   },
   "right_step": {
    "text": "Harmonic multiple: diverges, so 3 is out.",
    "expr": "Interval.Ropen(-1, 3)"
   },
   "relation": "distinct",
   "fix_prompt": true,
   "possible_reason": null,
   "sources": [
    "BC-ERR-10015"
   ]
  },
  {
   "error_id": "BC-ERR-10037",
   "observed_behavior": "The response reports the open interval found from the ratio test as the interval of convergence without examining either endpoint.",
   "scoring_consequence": "Both the endpoint consideration point and the interval point are lost (sg-25:24).",
   "wrong_step": {
    "text": "The radius alone gives \\((-1,3)\\).",
    "expr": "Interval.open(-1, 3)"
   },
   "right_step": {
    "text": "Both ends tested, so \\([-1,3)\\).",
    "expr": "Interval.Ropen(-1, 3)"
   },
   "relation": "distinct",
   "fix_prompt": true,
   "possible_reason": null,
   "sources": [
    "BC-ERR-10037"
   ]
  },
  {
   "error_id": "BC-ERR-10042",
   "observed_behavior": "The response asserts a different radius for the derived series, or redoes the ratio test and reports a value inconsistent with the original radius.",
   "scoring_consequence": "The radius point rests on the preservation statement, so an inconsistent value loses it (sg-24:22).",
   "wrong_step": {
    "text": "The derived series has radius 1.",
    "expr": "1"
   },
   "right_step": {
    "text": "The radius is unchanged, 2.",
    "expr": "2"
   },
   "relation": "distinct",
   "fix_prompt": true,
   "possible_reason": null,
   "sources": [
    "BC-ERR-10042"
   ]
  },
  {
   "error_id": "BC-ERR-10043",
   "observed_behavior": "The response states that the series does or does not converge at the given input without placing the input relative to the interval of convergence.",
   "scoring_consequence": "The answer with reason point requires the position relative to the interval to be given (sg-25:27).",
   "wrong_step": {
    "text": "Says only that it diverges at \\(-2\\).",
    "expr": "EmptySet"
   },
   "right_step": {
    "text": "\\(-2\\) is not in \\((-2,4)\\), so it diverges.",
    "expr": "Interval.open(-2, 4)"
   },
   "relation": "distinct",
   "fix_prompt": true,
   "possible_reason": null,
   "sources": [
    "BC-ERR-10043"
   ]
  }
 ],
 "representations": null,
 "prerequisite_bridges": [
  {
   "prq_id": "BC-PRQ-06005",
   "text": "\\(f'\\) and \\(f\\) are different functions."
  },
  {
   "prq_id": "BC-PRQ-10006",
   "text": "Square bracket includes an endpoint."
  },
  {
   "prq_id": "BC-PRQ-10008",
   "text": "Read the nth term, sign included."
  }
 ],
 "time": {
  "exam_part": "I-A",
  "budget_minutes": 2.14,
  "source": "research/exam/exam-structure.md#Section and part layout",
  "written_steps": {
   "ex-1": [
    2,
    5
   ]
  },
  "skipped_steps": {
   "ex-1": [
    1,
    3,
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
   "archetype_id": "BC-QA-10018",
   "parameter_draw": {
    "sign": "positive",
    "given": "interval",
    "centre": 1,
    "base": 2,
    "coefficient": 3
   },
   "completes": "ex-1",
   "stem": {
    "text": "The derived series has radius 2 about 1, diverges at 3 and converges at \\(-1\\). Write its interval of convergence.",
    "command_verb": "write"
   },
   "key": {
    "form": "symbolic",
    "expr": "Interval.Ropen(-1, 3)"
   },
   "steps": [
    {
     "text": "Interior.",
     "expr": "Interval.open(-1, 3)",
     "relation": "new"
    },
    {
     "text": "Keep -1.",
     "expr": "Interval.Ropen(-1, 3)",
     "relation": "new"
    }
   ],
   "calculator_status": "no_calculator",
   "skills": [
    "BC-SKL-10071"
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
   "archetype_id": "BC-QA-10018",
   "parameter_draw": {
    "sign": "alternating",
    "given": "interval",
    "centre": 3,
    "base": 5,
    "coefficient": 2
   },
   "stem": {
    "text": "The series for \\(f\\) is \\(\\sum_{n=1}^{\\infty}\\frac{2(-1)^n(x-3)^n}{n^25^n}\\), with interval \\([-2,8]\\). Find the interval of convergence of the series for \\(f'\\).",
    "command_verb": "find"
   },
   "key": {
    "form": "symbolic",
    "expr": "Interval.Lopen(-2, 8)"
   },
   "steps": [
    {
     "text": "Radius 5 about 3.",
     "expr": "Interval.open(-2, 8)",
     "relation": "new"
    },
    {
     "text": "At 8 alternating, converges; at -2 harmonic, diverges.",
     "expr": "Interval.Lopen(-2, 8)",
     "relation": "new"
    }
   ],
   "calculator_status": "no_calculator",
   "skills": [
    "BC-SKL-10070",
    "BC-SKL-10071"
   ]
  },
  {
   "id": "chk-3",
   "check_kind": "mcq",
   "format": "mcq",
   "bands": [
    "low"
   ],
   "archetype_id": "BC-QA-10018",
   "parameter_draw": {
    "sign": "positive",
    "given": "interval",
    "centre": -2,
    "base": 4,
    "coefficient": 5
   },
   "stem": {
    "text": "The series for \\(f\\) is \\(\\sum_{n=1}^{\\infty}\\frac{5(x+2)^n}{n^24^n}\\), with interval \\([-6,2]\\). The interval of convergence of the series for \\(f'\\) is",
    "command_verb": "identify"
   },
   "key": {
    "form": "symbolic",
    "expr": "Interval.Ropen(-6, 2)"
   },
   "steps": [
    {
     "text": "Radius 4 about -2.",
     "expr": "Interval.open(-6, 2)",
     "relation": "new"
    },
    {
     "text": "At 2 harmonic, diverges; at -6 alternating, converges.",
     "expr": "Interval.Ropen(-6, 2)",
     "relation": "new"
    }
   ],
   "options": [
    {
     "id": "A",
     "is_key": false,
     "expr": "Interval.open(-6, 2)",
     "error_path": "BC-ERR-10037",
     "derivation": "the open interval from the radius, endpoints untested"
    },
    {
     "id": "B",
     "is_key": false,
     "expr": "Interval(-6, 2)",
     "error_path": "BC-ERR-10015",
     "derivation": "the alternating series test applied to the positive series at 2, so both ends are kept"
    },
    {
     "id": "C",
     "is_key": true,
     "expr": "Interval.Ropen(-6, 2)",
     "error_path": null
    },
    {
     "id": "D",
     "is_key": false,
     "expr": "Interval.open(-5, 1)",
     "error_path": "BC-ERR-10042",
     "derivation": "the radius recomputed as 3 instead of carried over as 4"
    }
   ],
   "calculator_status": "no_calculator",
   "skills": [
    "BC-SKL-10070",
    "BC-SKL-10071"
   ]
  }
 ],
 "delivery": [
  {
   "block": "orientation",
   "mode": "text",
   "reason": "rule 5: a statement of what a response shows",
   "sources": [
    "BC-CON-10026"
   ]
  },
  {
   "block": "ki-1",
   "mode": "text",
   "reason": "rule 5: BC-REP-11, 04 on BC-SKL-10070, a stated radius and not a process",
   "sources": [
    "BC-SKL-10070"
   ]
  },
  {
   "block": "ki-2",
   "mode": "text",
   "reason": "rule 5: BC-REP-11, 04 on BC-SKL-10071",
   "sources": [
    "BC-SKL-10071"
   ]
  },
  {
   "block": "ki-3",
   "mode": "text",
   "reason": "rule 5: BC-REP-11, 04 on BC-SKL-10073",
   "sources": [
    "BC-SKL-10073"
   ]
  },
  {
   "block": "ki-4",
   "mode": "text",
   "reason": "rule 5: BC-REP-11, 04 on BC-SKL-10073; the interactive reading the unit map names is outside the rules",
   "sources": [
    "BC-SKL-10073"
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
   "block": "err-BC-ERR-10037",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  },
  {
   "block": "err-BC-ERR-10042",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  },
  {
   "block": "err-BC-ERR-10043",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  }
 ],
 "refresher": [
  "ki-1",
  "ki-2",
  "err-BC-ERR-10015",
  "err-BC-ERR-10037",
  "err-BC-ERR-10042",
  "err-BC-ERR-10043",
  "ex-1"
 ],
 "research_lines": [
  {
   "file": "research/units/unit-10-infinite-sequences-series.md",
   "line": "The endpoints are not covered by this statement and must be tested for the new series (BC-EK-LIM-8D4)."
  }
 ],
 "inferred": [
  {
   "claim": "BC-QA-10015 lists no point_types and BC-QA-10020 lists only BC-PT-99005, whose record (a value with its setup) does not describe the answer with a reason that BC-QA-10020's scoring_pattern names, so ex-2 tags nothing. ex-1 tags nothing, because a BC-PT-99047 line (45 words) does not fit the brief cap beside the prediction and contrast pair.",
   "settles": "A point type for the answer with a reason on BC-QA-10020, and a brief cap that admits a reader line."
  },
  {
   "claim": "BC-ERR-10042 is shown as a radius value of 1 against 2, and BC-ERR-10043 as no interval against the interval, because the error records name a different radius and a verdict with no position, not a specific wrong value.",
   "settles": "A scored response sample carrying the radius the error produces."
  },
  {
   "claim": "ki-4's sentence that the position relative to the interval is the reason rests on the scoring_pattern of BC-QA-10020, not on a BC-EK statement.",
   "settles": "Linking a BC-EK statement to BC-SKL-10073 that carries the position-as-reason claim."
  },
  {
   "claim": "A fluent solver writes the open interval, the two endpoint verdicts and the final interval, and holds the simplification of each endpoint series.",
   "settles": "Timing data per step once the fluency telemetry exists."
  }
 ],
 "sources": [
  "BC-CON-10026",
  "BC-SKL-10070",
  "BC-SKL-10071",
  "BC-SKL-10073",
  "BC-EK-LIM-8D6",
  "BC-EK-LIM-8D4",
  "BC-EK-LIM-8D5",
  "BC-EK-LIM-8D2",
  "ced:198",
  "ced:200",
  "BC-QA-10018",
  "BC-QA-10015",
  "BC-QA-10020",
  "BC-PT-99005",
  "BC-PT-99047",
  "BC-ERR-10015",
  "BC-ERR-10037",
  "BC-ERR-10042",
  "BC-ERR-10043",
  "BC-PRQ-06005",
  "BC-PRQ-10006",
  "BC-PRQ-10008",
  "research/units/unit-10-infinite-sequences-series.md#10.15 Representing Functions as Power Series",
  "research/question-analysis/question-archetypes.md#BC-QA-10018 Series differentiated term by term with its radius carried over",
  "research/question-analysis/question-archetypes.md#BC-QA-10015 Endpoint series identified and tested",
  "research/question-analysis/question-archetypes.md#BC-QA-10020 Convergence to the function at a specified input decided with a reason",
  "research/exam/exam-structure.md#Section and part layout"
 ],
 "word_count": {
  "full": 795,
  "brief": 443
 },
 "read_minutes": {
  "full": 5.3,
  "brief": 3.0
 }
}
```
