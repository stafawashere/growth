---
title: LSN-CON-10023 Taylor series and the general term
research_date: 2026-09-29
status: designed
purpose: Authoring spec for the concept lesson on BC-CON-10023, the Taylor series as a polynomial pattern that continues without stopping, written with a general term in the index, with a Taylor polynomial read as its partial sum, built from authoring_bundle("BC-CON-10023") and the research files it cites, so an author fills plan 15's lesson record without making a teaching decision.
---

# LSN-CON-10023 Taylor series and the general term

Concept BC-CON-10023 (skills BC-SKL-10060, BC-SKL-10066, BC-SKL-10067), topic 10.14 of Unit 10, BC only (ced:199), loaded by four archetypes, BC-QA-10016 and BC-QA-10018 (family taylor-construction), BC-QA-10002 (series-value) and BC-QA-10008 (taylor-error). Hard parents BC-CON-10016 (Taylor coefficients) and BC-CON-10022 (docs/lessons/unit-10/README.md, section 1).

## Prediction

Served first, both bands: an `mcq` on ex-1's own numbers. The first three nonzero terms of the Maclaurin series of \(2xe^{3x}\) are given as \(2x, 6x^2, 9x^3\), and the student picks the formula for the term of index \(n\). Key A, \(\frac{2\cdot3^nx^{n+1}}{n!}\). Option B has \((n+1)!\) and returns \(2x, 3x^2, 3x^3\); option C has \(x^n\) and returns \(2, 6x, 9x^2\). Each is tested at \(n=0,1,2\) against the given terms, so only A is true, and the question is answerable with no rule of this lesson. The resolution states the index check and that the formula continues, with no verdict. Source: BC-CON-10023 and research/units/unit-10-infinite-sequences-series.md#10.14 Finding Taylor or Maclaurin Series for a Function.

## Orientation

Served text, from BC-CON-10023 `description_plain` ("the Taylor series continues the polynomial pattern without stopping") and the topic's Assessment behaviour paragraph: MCQ forms ask for the coefficient of a named power or the general term, and FRQ forms ask for the first three nonzero terms and the general term, scored as two separate points (sg-25:26, research/units/unit-10-infinite-sequences-series.md#10.14 Finding Taylor or Maclaurin Series for a Function). The orientation states what a response shows. No count, no frequency.

## Key ideas

Two essential knowledge statements meet the skills: ki-1 (core) BC-EK-LIM-8E1, a Taylor polynomial is a partial sum of the Taylor series (ced:199), with the notation line "general term; partial sum of the series" and the polynomial rule of BC-ERR-10030 (no term past the degree, no ellipsis, sg-23:20, sg-23:21); ki-2 (extended) BC-EK-LIM-8F2, the series for sin x, cos x and e to the x are the base, with substitution of an expression or a number for x. No anchor quote. Core serves both bands, extended the low band.

## Recognition

BC-QA-10016 (research/question-analysis/question-archetypes.md#BC-QA-10016 First nonzero terms and the general term of a series): `common_givens` "the centre of the series"; `asked_to_produce` "the first nonzero terms of the series" and "the general term of the series"; `typical_wording` "find the first three nonzero terms and the general term of the Taylor series for the function about the given centre". BC-QA-10002 (research/question-analysis/question-archetypes.md#BC-QA-10002 Value of a convergent series requested) loads BC-SKL-10066 through `common_givens` "a series obtained by evaluating a power series at a point". BC-QA-10018 and BC-QA-10008 also load skills of the concept and are served through BC-CON-10025 and BC-CON-10015. BC-QA-10016 lists no official example.

What in the stem says this concept: the words series or general term, or the first nonzero terms. What says not this concept: a polynomial of a stated degree (BC-CON-10016, BC-QA-10012). The near miss of the contrast pair is the degree 4 polynomial for the same function, from BC-QA-10012, the README's Taylor polynomial against Taylor series row (docs/lessons/unit-10/README.md, section 3).

## Method choice

- st-1, BC-QA-10016. Cue from `asked_to_produce` and `common_givens`. Method, `expected_solution_path`: produce the terms from a known series, detect the pattern, write a general term, check it against the displayed terms. Rival from `wrong_approaches`: "differentiating the general term with respect to the index" and "writing terms from a misremembered standard series". Separating feature: a general term that continues, against a polynomial that ends. Carries the contrast pair: a series stem beside a polynomial stem on one function.
- st-2, BC-QA-10002, low band only. Method, `expected_solution_path` [0] "identify the structure of the series", after the input is put in the general term. Rival from `wrong_approaches`: "adding the first few terms instead of summing in closed form" and "reporting the limit of the general term as the value". Separating feature: series of numbers against a series in x.
No served field opens with the reader's own label.

## Solution path

- ex-1, BC-QA-10016, both bands. Draw: base exp, sign positive, count 3, scale 3, coefficient 2, power 1, giving \(f(x)=2xe^{3x}\), terms \(2x, 6x^2, 9x^3\), general term \(\frac{2\cdot3^nx^{n+1}}{n!}\). No published item on BC-QA-10016 carries this draw (content/items_gen_*/ITM-GEN-10016-00 to 04). Steps: the base series (new), \(3x\) for \(x\) (evaluate), the factor \(2x\) (new), the collected general term (equivalent), then a check at \(n=0,1,2\) with no value.
- ex-2, low band, BC-QA-10016. Draw: base sin, sign positive, count 3, scale 2, coefficient 3, power 1, giving \(3x\sin2x\), terms \(6x^2, -4x^4, \frac45x^6\). No published item carries this draw.
- ex-2 is faded from step 4: the base series, the substitution and the factor are shown, and the student writes the collected general term before step 4 and the check reveal. The fade falls there because steps 1 to 3 repeat ex-1's pattern, and collecting the powers with the alternating factor and the odd factorial is what the student must produce.
- A fluent solver writes the substituted series, the general term and the check, and holds the base series and the factor multiplication (Time). No productive-failure comparison: BC-CON-10023 is not in `PRODUCTIVE_FAILURE_TARGETS`.

## Scoring

BC-QA-10016 lists no point type, so ex-1 and ex-2 carry no scoring line and no tag, and this lesson says nothing about points beyond the two points the topic's Assessment behaviour names for the first terms and the general term (sg-25:26, docs/lessons/unit-10/README.md, section 5).

## Traps

Five errors meet the skills; the cap keeps four, in bundle order: BC-ERR-10030, BC-ERR-10034, BC-ERR-10040, BC-ERR-10041. BC-ERR-99018 falls past the cap. Low band all four, mid band the first two. All on ex-1's draw. All four carry `fix_prompt` true, since each pair is distinct. None carries a possible reason line.

- err-BC-ERR-10030: the degree 3 polynomial written with the next term \(9x^4\) (inferred array, since ex-1 asks for the series).
- err-BC-ERR-10034: the series at \(x=-1\) with the alternating factor dropped (inferred array).
- err-BC-ERR-10040: the \(e^x\) series without its factorials.
- err-BC-ERR-10041: \(3x\) substituted with 3 not raised to \(n\).

## Representations

None. The topic's Representations paragraph names BC-REP-11, 01 and 04 and the conversions first terms to a general term, a function to a series, a series at a point to a numerical series; nothing figure-shaped (docs/lessons/unit-10/README.md, section 6).

## Prerequisite bridge

- BC-PRQ-06002, 06005, 10003, 10008, each from its `description_plain` and `failure_signature`, one short paragraph each.

## Time

ex-1 is the MCQ shape "the general term of the series": Section I Part A, 2.14 minutes (research/exam/exam-structure.md#Section and part layout). As a free response part: 2 points, 3.33 minutes (docs/lessons/unit-10/README.md, section 5). A fluent solver writes the substituted series, the general term and the check at three indices; the base series and the factor multiplication are held. The minutes go on the check at \(n=0,1,2\).

## Checks

- chk-1, completion of ex-1, both bands: the series for \(e^{3x}\) given, the general term for \(2xe^{3x}\) asked.
- chk-2, isomorph, both bands. Draw: base cos, sign positive, count 3, scale 2, coefficient 3, power 0, giving \(3\cos2x\). Key \(\frac{3(-1)^n2^{2n}x^{2n}}{(2n)!}\).
- chk-3, MCQ, low band. Draw: base exp, sign negative, count 3, scale 2, coefficient 3, power 1, giving \(3xe^{-2x}\). Key \(\frac{3(-2)^nx^{n+1}}{n!}\). Distractors: no factorial (BC-ERR-10040), the alternating factor dropped (BC-ERR-10034), \(-2\) not raised to \(n\) (BC-ERR-10041).

## Delivery

- prediction, orientation, ki-1, ki-2: text. Rule 6: the skills carry BC-REP-11, 01 and 04, none figure-bearing. No block is drawn, so the record carries `no_figure_reason`: no figure-bearing representation and no process idea, since the general term is a formula in the index.
- ex-1, ex-2, the four error blocks: step_reveal. Rule 1.

## Band plan

- Low (full): prediction, orientation, four bridges, ki-1, ki-2, st-1 with the contrast pair, st-2, ex-1, chk-1, four error blocks, ex-2 (faded from step 4), chk-2, chk-3. 777 words, 5.2 minutes.
- Mid (brief): prediction, orientation, bridges, ki-1, st-1 with the contrast pair, ex-1, chk-1, err-BC-ERR-10030, err-BC-ERR-10034, chk-2. 449 words, 3.0 minutes.
- Refresher: ki-1, the four error blocks, ex-1.

## Sources

- BC-CON-10023; BC-SKL-10060, BC-SKL-10066, BC-SKL-10067; BC-EK-LIM-8E1, BC-EK-LIM-8F2; ced:199
- BC-QA-10016, BC-QA-10002
- BC-ERR-10030, BC-ERR-10034, BC-ERR-10040, BC-ERR-10041
- BC-PRQ-06002, BC-PRQ-06005, BC-PRQ-10003, BC-PRQ-10008
- sg-23:20, sg-23:21, sg-25:25, sg-25:26
- research/units/unit-10-infinite-sequences-series.md#10.14 Finding Taylor or Maclaurin Series for a Function
- research/exam/exam-structure.md#Section and part layout
- [inferred] the prediction, the contrast pair, the delivery modes, the missing worked example for BC-SKL-10066, the two uses of BC-ERR-10034 and BC-ERR-10030 beyond the record's wording, and the held steps. Each settled as the inferred array states.

## Machine record

```json
{
 "id": "LSN-CON-10023",
 "kind": "concept",
 "target_id": "BC-CON-10023",
 "unit": "10",
 "skills": [
  "BC-SKL-10060",
  "BC-SKL-10066",
  "BC-SKL-10067"
 ],
 "prediction": {
  "id": "pr-1",
  "stem": {
   "text": "The first three nonzero terms of the Maclaurin series of \\(f(x)=2xe^{3x}\\) are \\(2x,\\ 6x^2,\\ 9x^3\\). Which formula gives the term of index \\(n\\) and continues without stopping?",
   "command_verb": "predict"
  },
  "format": "mcq",
  "options": [
   {
    "id": "A",
    "label": "\\(\\frac{2\\cdot3^n x^{n+1}}{n!}\\)",
    "is_key": true
   },
   {
    "id": "B",
    "label": "\\(\\frac{2\\cdot3^n x^{n+1}}{(n+1)!}\\)",
    "is_key": false
   },
   {
    "id": "C",
    "label": "\\(\\frac{2\\cdot3^n x^{n}}{n!}\\)",
    "is_key": false
   }
  ],
  "resolution": "Setting \\(n=0,1,2\\) must return \\(2x,\\ 6x^2,\\ 9x^3\\) in turn. The same formula supplies every later term, so the series has no last term.",
  "sources": [
   "BC-CON-10023",
   "research/units/unit-10-infinite-sequences-series.md#10.14 Finding Taylor or Maclaurin Series for a Function"
  ]
 },
 "no_figure_reason": "No skill carries a figure-bearing representation (the topic names series, symbolic and verbal forms) and no key idea describes a process, since the general term is a formula in the index.",
 "orientation": {
  "text": "A Taylor series continues the polynomial pattern without stopping. A response writes the first nonzero terms and a general term in \\(n\\) that reproduces them, and a polynomial as a partial sum ending at its degree with no ellipsis.",
  "sources": [
   "BC-CON-10023",
   "research/units/unit-10-infinite-sequences-series.md#10.14 Finding Taylor or Maclaurin Series for a Function"
  ]
 },
 "key_ideas": [
  {
   "id": "ki-1",
   "ek_id": "BC-EK-LIM-8E1",
   "depth": "core",
   "text": "A Taylor polynomial for \\(f\\) is a partial sum of the Taylor series for \\(f\\). The series has a general term in \\(n\\) and no last term; a polynomial stops at its degree with no ellipsis.",
   "notation": "general term; partial sum of the series",
   "quote": null,
   "sources": [
    "BC-EK-LIM-8E1",
    "ced:199",
    "sg-23:20",
    "research/units/unit-10-infinite-sequences-series.md#10.14 Finding Taylor or Maclaurin Series for a Function"
   ]
  },
  {
   "id": "ki-2",
   "ek_id": "BC-EK-LIM-8F2",
   "depth": "extended",
   "text": "The Maclaurin series for \\(\\sin x\\), \\(\\cos x\\) and \\(e^x\\) are the base for other series. Replacing \\(x\\) by an expression puts the whole expression in each power. Putting a number for \\(x\\) gives a series of numbers, and a negative number brings a factor \\((-1)^n\\).",
   "notation": "general term; series at a point",
   "quote": null,
   "sources": [
    "BC-EK-LIM-8F2",
    "ced:199"
   ]
  }
 ],
 "strategy": [
  {
   "id": "st-1",
   "archetype_id": "BC-QA-10016",
   "cue": "A standard series inside a function; terms and a general term requested.",
   "method": "The known series with the whole argument in each power, then a general term checked at \\(n=0,1,2\\).",
   "rival": "The general term differentiated in \\(n\\), or a misremembered series.",
   "separating_feature": "A series continues; a polynomial ends.",
   "sources": [
    "BC-QA-10016"
   ],
   "evidence_tag": "verified",
   "contrast": {
    "this": {
     "text": "Let \\(g(x)=5x^2e^{-x}\\). Find the first three nonzero terms and the general term of the Maclaurin series.",
     "archetype_id": "BC-QA-10016"
    },
    "not_this": {
     "text": "Let \\(g(x)=5x^2e^{-x}\\). Write the Taylor polynomial of degree 4 for \\(g\\) about \\(x=0\\).",
     "why_not": "It ends at degree 4: no general term."
    },
    "feature": "A series continues; a polynomial stops."
   }
  },
  {
   "id": "st-2",
   "archetype_id": "BC-QA-10002",
   "cue": "A power series and an input value, with the value of the resulting series requested.",
   "method": "The input put in every power of the general term, simplified to a series of numbers, then its structure identified.",
   "rival": "The first few terms added, or the limit of the general term reported.",
   "separating_feature": "A series of numbers asks for a value; a series in \\(x\\) asks for terms.",
   "sources": [
    "BC-QA-10002"
   ],
   "evidence_tag": "verified"
  }
 ],
 "worked_examples": [
  {
   "id": "ex-1",
   "archetype_id": "BC-QA-10016",
   "bands": [
    "low",
    "mid"
   ],
   "parameter_draw": {
    "base": "exp",
    "sign": "positive",
    "count": 3,
    "scale": 3,
    "coefficient": 2,
    "power": 1
   },
   "problem": {
    "text": "Let \\(f(x)=2xe^{3x}\\). Find the first three nonzero terms and the general term of the Maclaurin series for \\(f\\).",
    "command_verb": "find"
   },
   "calculator_status": "no_calculator",
   "steps": [
    {
     "cue": "Base: \\(e^x\\), with \\(3x\\) for \\(x\\).",
     "why": "General term of the series for \\(e^x\\).",
     "expr": "x**n/factorial(n)",
     "relation": "new"
    },
    {
     "cue": "\\(3x\\) in place of \\(x\\).",
     "why": "The whole \\(3x\\) is raised to \\(n\\).",
     "expr": "(3*x)**n/factorial(n)",
     "relation": "evaluate",
     "subs": {
      "x": "3*x"
     }
    },
    {
     "cue": "Multiply by \\(2x\\).",
     "why": "Every power shifts up by one.",
     "expr": "2*x*(3*x)**n/factorial(n)",
     "relation": "new"
    },
    {
     "cue": "Collect powers of 3 and of \\(x\\).",
     "why": "One general term.",
     "expr": "2*3**n*x**(n+1)/factorial(n)",
     "relation": "equivalent"
    },
    {
     "cue": "Check at \\(n=0,1,2\\).",
     "why": "It returns \\(2x,\\ 6x^2,\\ 9x^3\\)."
    }
   ],
   "answer": {
    "form": "symbolic",
    "expr": "2*3**n*x**(n+1)/factorial(n)"
   }
  },
  {
   "id": "ex-2",
   "archetype_id": "BC-QA-10016",
   "bands": [
    "low"
   ],
   "fade_from": 4,
   "parameter_draw": {
    "base": "sin",
    "sign": "positive",
    "count": 3,
    "scale": 2,
    "coefficient": 3,
    "power": 1
   },
   "problem": {
    "text": "Let \\(f(x)=3x\\sin 2x\\). Find the first three nonzero terms and the general term of the Maclaurin series for \\(f\\).",
    "command_verb": "find"
   },
   "calculator_status": "no_calculator",
   "steps": [
    {
     "cue": "\\(\\sin 2x\\) is \\(\\sin x\\) with \\(2x\\) for \\(x\\).",
     "why": "Start from the general term for \\(\\sin x\\).",
     "expr": "(-1)**n*x**(2*n+1)/factorial(2*n+1)",
     "relation": "new"
    },
    {
     "cue": "Put \\(2x\\) in place of \\(x\\) everywhere.",
     "why": "The whole \\(2x\\) is raised to \\(2n+1\\).",
     "expr": "(-1)**n*(2*x)**(2*n+1)/factorial(2*n+1)",
     "relation": "evaluate",
     "subs": {
      "x": "2*x"
     }
    },
    {
     "cue": "Multiply by the factor \\(3x\\).",
     "why": "It shifts every power up by one.",
     "expr": "3*x*(-1)**n*(2*x)**(2*n+1)/factorial(2*n+1)",
     "relation": "new"
    },
    {
     "cue": "Collect the powers of 2 and of \\(x\\).",
     "why": "The alternating factor and the odd factorial stay.",
     "expr": "3*(-1)**n*2**(2*n+1)*x**(2*n+2)/factorial(2*n+1)",
     "relation": "equivalent"
    },
    {
     "cue": "Check at \\(n=0,1,2\\).",
     "why": "It returns \\(6x^2,\\ -4x^4,\\ \\frac45x^6\\)."
    }
   ],
   "answer": {
    "form": "symbolic",
    "expr": "3*(-1)**n*2**(2*n+1)*x**(2*n+2)/factorial(2*n+1)"
   }
  }
 ],
 "what_a_reader_scores": [],
 "common_errors": [
  {
   "error_id": "BC-ERR-10030",
   "observed_behavior": "The response writes a polynomial that includes terms beyond the requested degree, or appends an ellipsis, turning the answer into a series.",
   "scoring_consequence": "A polynomial with terms of higher degree, or with an ellipsis, does not earn the final polynomial point (sg-23:20, sg-23:21).",
   "wrong_step": {
    "text": "For the degree 3 polynomial: \\(2x+6x^2+9x^3+9x^4\\).",
    "expr": "2*x+6*x**2+9*x**3+9*x**4"
   },
   "right_step": {
    "text": "For the degree 3 polynomial: \\(2x+6x^2+9x^3\\).",
    "expr": "2*x+6*x**2+9*x**3"
   },
   "relation": "distinct",
   "fix_prompt": true,
   "possible_reason": null,
   "sources": [
    "BC-ERR-10030",
    "sg-23:20",
    "sg-23:21"
   ]
  },
  {
   "error_id": "BC-ERR-10034",
   "observed_behavior": "The response substitutes the endpoint for the index rather than for the variable, or drops the alternating factor produced by a negative endpoint.",
   "scoring_consequence": "The endpoint series is wrong, so the analysis and interval points are lost (sg-25:25).",
   "wrong_step": {
    "text": "At \\(x=-1\\) the alternating factor dropped: \\(\\frac{2\\cdot3^n}{n!}\\).",
    "expr": "2*3**n/factorial(n)"
   },
   "right_step": {
    "text": "At \\(x=-1\\): \\(\\frac{-2(-3)^n}{n!}\\).",
    "expr": "-2*(-3)**n/factorial(n)"
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
   "error_id": "BC-ERR-10040",
   "observed_behavior": "The response writes the series for the exponential, the sine, the cosine, or one over one minus x with wrong signs, wrong parities of the powers, or missing factorials.",
   "scoring_consequence": "Every term built on the misremembered series is wrong, so the dependent points are lost (sg-23:21).",
   "wrong_step": {
    "text": "The series for \\(e^x\\) recalled without its factorials.",
    "expr": "2*3**n*x**(n+1)"
   },
   "right_step": {
    "text": "The factorial \\(n!\\) under each term.",
    "expr": "2*3**n*x**(n+1)/factorial(n)"
   },
   "relation": "distinct",
   "fix_prompt": true,
   "possible_reason": null,
   "sources": [
    "BC-ERR-10040",
    "sg-23:21"
   ]
  },
  {
   "error_id": "BC-ERR-10041",
   "observed_behavior": "The response substitutes an expression for the variable in a known series but does not raise the whole expression to the required power, or loses a constant factor.",
   "scoring_consequence": "The resulting series is wrong from the first affected term onward.",
   "wrong_step": {
    "text": "\\(3x\\) put in, but 3 not raised to \\(n\\).",
    "expr": "2*3*x**(n+1)/factorial(n)"
   },
   "right_step": {
    "text": "The whole \\(3x\\) raised to \\(n\\).",
    "expr": "2*3**n*x**(n+1)/factorial(n)"
   },
   "relation": "distinct",
   "fix_prompt": true,
   "possible_reason": null,
   "sources": [
    "BC-ERR-10041"
   ]
  }
 ],
 "representations": null,
 "prerequisite_bridges": [
  {
   "prq_id": "BC-PRQ-06002",
   "text": "\\((3x)^n=3^nx^n\\)."
  },
  {
   "prq_id": "BC-PRQ-06005",
   "text": "\\(f(-1)\\) replaces \\(x\\) everywhere by \\(-1\\)."
  },
  {
   "prq_id": "BC-PRQ-10003",
   "text": "Shifting the index changes the start and the general term."
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
    4,
    5
   ]
  },
  "skipped_steps": {
   "ex-1": [
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
   "archetype_id": "BC-QA-10016",
   "parameter_draw": {
    "base": "exp",
    "sign": "positive",
    "count": 3,
    "scale": 3,
    "coefficient": 2,
    "power": 1
   },
   "completes": "ex-1",
   "stem": {
    "text": "The series for \\(e^{3x}\\) has general term \\(\\frac{(3x)^n}{n!}\\). Write the general term for \\(2xe^{3x}\\).",
    "command_verb": "write"
   },
   "key": {
    "form": "symbolic",
    "expr": "2*3**n*x**(n+1)/factorial(n)"
   },
   "steps": [
    {
     "text": "Multiply by 2x.",
     "expr": "2*x*(3*x)**n/factorial(n)",
     "relation": "new"
    },
    {
     "text": "Collect the powers.",
     "expr": "2*3**n*x**(n+1)/factorial(n)",
     "relation": "equivalent"
    }
   ],
   "calculator_status": "no_calculator",
   "skills": [
    "BC-SKL-10060"
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
   "archetype_id": "BC-QA-10016",
   "parameter_draw": {
    "base": "cos",
    "sign": "positive",
    "count": 3,
    "scale": 2,
    "coefficient": 3,
    "power": 0
   },
   "stem": {
    "text": "Let \\(f(x)=3\\cos 2x\\). Write the general term of the Maclaurin series for \\(f\\).",
    "command_verb": "write"
   },
   "key": {
    "form": "symbolic",
    "expr": "3*(-1)**n*2**(2*n)*x**(2*n)/factorial(2*n)"
   },
   "steps": [
    {
     "text": "General term for cos x.",
     "expr": "(-1)**n*x**(2*n)/factorial(2*n)",
     "relation": "new"
    },
    {
     "text": "Put 2x in place of x.",
     "expr": "(-1)**n*(2*x)**(2*n)/factorial(2*n)",
     "relation": "evaluate",
     "subs": {
      "x": "2*x"
     }
    },
    {
     "text": "Multiply by 3.",
     "expr": "3*(-1)**n*(2*x)**(2*n)/factorial(2*n)",
     "relation": "new"
    },
    {
     "text": "Collect the powers.",
     "expr": "3*(-1)**n*2**(2*n)*x**(2*n)/factorial(2*n)",
     "relation": "equivalent"
    }
   ],
   "calculator_status": "no_calculator",
   "skills": [
    "BC-SKL-10060"
   ]
  },
  {
   "id": "chk-3",
   "check_kind": "mcq",
   "format": "mcq",
   "bands": [
    "low"
   ],
   "archetype_id": "BC-QA-10016",
   "parameter_draw": {
    "base": "exp",
    "sign": "negative",
    "count": 3,
    "scale": 2,
    "coefficient": 3,
    "power": 1
   },
   "stem": {
    "text": "The general term of the Maclaurin series for \\(f(x)=3xe^{-2x}\\) is",
    "command_verb": "identify"
   },
   "key": {
    "form": "symbolic",
    "expr": "3*(-2)**n*x**(n+1)/factorial(n)"
   },
   "steps": [
    {
     "text": "General term for e^x.",
     "expr": "x**n/factorial(n)",
     "relation": "new"
    },
    {
     "text": "Put -2x in place of x.",
     "expr": "(-2*x)**n/factorial(n)",
     "relation": "evaluate",
     "subs": {
      "x": "-2*x"
     }
    },
    {
     "text": "Multiply by 3x and collect the powers.",
     "expr": "3*(-2)**n*x**(n+1)/factorial(n)",
     "relation": "new"
    }
   ],
   "options": [
    {
     "id": "A",
     "is_key": false,
     "expr": "3*(-2)**n*x**(n+1)",
     "label": "\\(3(-2)^nx^{n+1}\\)",
     "error_path": "BC-ERR-10040",
     "derivation": "the series for e^x recalled without its factorials"
    },
    {
     "id": "B",
     "is_key": false,
     "expr": "3*2**n*x**(n+1)/factorial(n)",
     "label": "\\(\\frac{3\\cdot2^nx^{n+1}}{n!}\\)",
     "error_path": "BC-ERR-10034",
     "derivation": "the alternating factor from the negative argument dropped"
    },
    {
     "id": "C",
     "is_key": true,
     "expr": "3*(-2)**n*x**(n+1)/factorial(n)",
     "label": "\\(\\frac{3(-2)^nx^{n+1}}{n!}\\)",
     "error_path": null
    },
    {
     "id": "D",
     "is_key": false,
     "expr": "3*(-2)*x**(n+1)/factorial(n)",
     "label": "\\(\\frac{-6x^{n+1}}{n!}\\)",
     "error_path": "BC-ERR-10041",
     "derivation": "-2 not raised to the power n"
    }
   ],
   "calculator_status": "no_calculator",
   "skills": [
    "BC-SKL-10060",
    "BC-SKL-10066"
   ]
  }
 ],
 "delivery": [
  {
   "block": "pr-1",
   "mode": "text",
   "reason": "rule 6: a choice among general terms, no figure-bearing representation",
   "sources": [
    "BC-SKL-10060"
   ]
  },
  {
   "block": "orientation",
   "mode": "text",
   "reason": "rule 6: a statement of what a response shows",
   "sources": [
    "BC-CON-10023"
   ]
  },
  {
   "block": "ki-1",
   "mode": "text",
   "reason": "rule 6: BC-REP-11, 01 and 04 on BC-SKL-10060 and 10067, none figure-bearing",
   "sources": [
    "BC-SKL-10060",
    "BC-SKL-10067"
   ]
  },
  {
   "block": "ki-2",
   "mode": "text",
   "reason": "rule 6: BC-REP-11 and 01 on BC-SKL-10066",
   "sources": [
    "BC-SKL-10066"
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
  },
  {
   "block": "err-BC-ERR-10034",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  },
  {
   "block": "err-BC-ERR-10040",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  },
  {
   "block": "err-BC-ERR-10041",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  }
 ],
 "refresher": [
  "ki-1",
  "err-BC-ERR-10030",
  "err-BC-ERR-10034",
  "err-BC-ERR-10040",
  "err-BC-ERR-10041",
  "ex-1"
 ],
 "research_lines": [
  {
   "file": "research/units/unit-10-infinite-sequences-series.md",
   "line": "A Taylor polynomial for f is a partial sum of the Taylor series for f"
  }
 ],
 "inferred": [
  {
   "claim": "The prediction, the contrast pair and the delivery modes are teaching decisions, not record facts.",
   "settles": "The modality A/B and first-attempt data on the prediction."
  },
  {
   "claim": "BC-SKL-10066 (a Taylor series evaluated at a point) has no worked example, because BC-QA-10002 and BC-QA-10008, the archetypes that load it, draw no Taylor series evaluated at a point in their parameter_spec; it is taught in ki-2, err-BC-ERR-10034 and chk-3.",
   "settles": "A BC-QA-10002 parameter_spec form that evaluates a Maclaurin series at a point."
  },
  {
   "claim": "BC-ERR-10034 is shown on the evaluation of ex-1's series at x = -1 and as the negative argument distractor of chk-3, a use of its alternating factor wording beyond the endpoint case the record names.",
   "settles": "A BC-ERR record for the alternating factor lost when a negative input or argument is substituted into a Taylor series."
  },
  {
   "claim": "BC-ERR-10030 is shown as a degree 3 polynomial for ex-1's function, which ex-1 does not ask for, because BC-QA-10016 draws no polynomial task.",
   "settles": "A BC-QA-10016 or BC-QA-10012 task value that asks for the polynomial and the series together."
  },
  {
   "claim": "A fluent solver writes the substituted series, the general term and the check at three indices, and holds the base series and the factor multiplication.",
   "settles": "Timing data per step once the fluency telemetry exists."
  }
 ],
 "sources": [
  "BC-CON-10023",
  "BC-SKL-10060",
  "BC-SKL-10066",
  "BC-SKL-10067",
  "BC-EK-LIM-8E1",
  "BC-EK-LIM-8F2",
  "ced:199",
  "BC-QA-10016",
  "BC-QA-10002",
  "BC-ERR-10030",
  "BC-ERR-10034",
  "BC-ERR-10040",
  "BC-ERR-10041",
  "BC-PRQ-06002",
  "BC-PRQ-06005",
  "BC-PRQ-10003",
  "BC-PRQ-10008",
  "sg-23:20",
  "sg-23:21",
  "sg-25:25",
  "sg-25:26",
  "research/units/unit-10-infinite-sequences-series.md#10.14 Finding Taylor or Maclaurin Series for a Function",
  "research/exam/exam-structure.md#Section and part layout"
 ],
 "word_count": {
  "full": 776,
  "brief": 448
 },
 "read_minutes": {
  "full": 5.2,
  "brief": 3.0
 }
}
```
