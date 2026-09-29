---
title: LSN-CON-10024 The standard Maclaurin series
research_date: 2026-09-29
status: designed
purpose: Authoring spec for the concept lesson on BC-CON-10024, the recalled Maclaurin series for e to the x, sin x, cos x and one over one minus x and their use by substitution and multiplication, built from authoring_bundle("BC-CON-10024") and the research files it cites, so an author fills plan 15's lesson record without making a teaching decision.
---

# LSN-CON-10024 The standard Maclaurin series

Concept BC-CON-10024 (skills BC-SKL-10061 to BC-SKL-10065), topic 10.14 of Unit 10, BC only (ced:199), loaded by three archetypes, BC-QA-10017 and BC-QA-10012 (family taylor-construction) and BC-QA-10003 (family series-value). Hard parents inside the unit are BC-CON-10004, BC-CON-10016 and BC-CON-10023 (docs/lessons/unit-10/README.md, section 1), so the geometric series, the Taylor polynomial and the Taylor series general term are assumed.

## Prediction

Served first, both bands: an `mcq` on the base of ex-1, the geometric series for \(g(u)=\frac{1}{1-u}\). The stem gives \(g'''(0)=6\) and asks for the coefficient of \(u^3\). Key B, 1. The distractors are \(\frac16\) (the exponential's coefficient) and 6 (the derivative left unfactored). The Taylor coefficient formula from the prerequisite concepts answers it before any standard series is stated. The resolution gives \(g^{(n)}(0)=n!\), the coefficient 1 and the pattern, with no verdict. Source: BC-CON-10024 and the topic section.

## Orientation

Served text, from BC-CON-10024 `description_plain` ("Four series are recalled rather than rederived") and the topic's Assessment behaviour paragraph (research/units/unit-10-infinite-sequences-series.md#10.14 Finding Taylor or Maclaurin Series for a Function): MCQ forms ask for a coefficient or the general term of a series built by substitution, FRQ forms for the first nonzero terms and the general term. The orientation states what a response shows. No count, no frequency.

## Key ideas

Three essential knowledge statements map from the five skills, so three blocks. ki-1 (core) is BC-EK-LIM-8F1 (ced:199), the series for \(\frac{1}{1-x}\) as a geometric series, with the interval statement from BC-EK-LIM-7A4 (ced:187) and the Caution paragraph of the topic. ki-2 (core) is BC-EK-LIM-8F2 (ced:199), the three foundation series, with the parities and the general terms computed with SymPy and never stated from memory. ki-3 (extended, low band only) is BC-EK-LIM-8G1 (ced:200), construction by substitution and multiplication, with the centre statement from the `invariant_structure` of BC-QA-10017. No anchor quote: each CED sentence adds nothing the paraphrase lacks and costs words in the brief band.

## Recognition

BC-QA-10017 (research/question-analysis/question-archetypes.md#BC-QA-10017 Maclaurin series built from a known series by substitution or multiplication) loads BC-SKL-10061 to 10065. `common_givens`: "a function formed by substitution into or multiplication of that series". `asked_to_produce`: "the first nonzero terms of the new series", "the general term of the new series". `typical_wording`: "use a known Maclaurin series to find the series for the given function". The signal in the stem is a standard function of an expression, or a multiple of one, with the words first nonzero terms. Shapes: the MCQ BC-MCQ-PE2012-017 and the FRQ parts BC-FRQ-2026-Q6-D and BC-FRQ-2018-Q6-A.

BC-QA-10003 (research/question-analysis/question-archetypes.md#BC-QA-10003 Geometric series summed in closed form) supplies the geometric form: a series stated to be geometric, or a closed form to verify.

The near miss of the contrast pair is the derivative form, a stem that names the known series and asks for the series of its derivative, which belongs to term-by-term differentiation (BC-CON-10025). The unit map names the pair: an expression in place of \(x\) selects substitution, a derivative or integral of a known function selects the operation on the terms (docs/lessons/unit-10/README.md, section 3). The not_this stem comes from outside BC-QA-10017.

## Method choice

- st-1, BC-QA-10017. Cue from `common_givens` and `asked_to_produce`. Method from `expected_solution_path`: recall the standard series, substitute raising every power, multiply by any factor. Rival: `wrong_approaches` "substituting without raising the whole expression to the power", and the derivative route the CED does not require for these four functions. Separating feature: a standard function of an expression is recalled, not rederived. The block carries the contrast pair. Both cue fields exist, so the block is not inferred.
- st-2, BC-QA-10003. Cue from `common_givens`. Method from `expected_solution_path`: ratio, condition on its size, quotient. Rival: `wrong_approaches` "applying the closed form with a ratio of size at least one". Separating feature: a constant quotient of consecutive terms. No served field opens with the reader's own label.

## Solution path

- ex-1, BC-QA-10017, both bands, no calculator. Draw: base geometric, inner_power 2, scale 3, coefficient 5, count 4. \(f(x)=\frac{5}{1-3x^2}\), key \(5+15x^2+45x^4+135x^6\), computed with SymPy. No published item on BC-QA-10017 carries this draw (content/items_gen_unit10/ITM-GEN-10017-00 to 04 and the agent items use other bases and keys).
- ex-2, low band, no calculator. Draw: base cos, inner_power 3, scale 2, coefficient 6, count 3. \(f(x)=6\cos(2x^3)\), key \(6-12x^6+4x^{12}\).
- ex-2 is faded from step 3: steps 1 and 2 (the cosine series times 6, then the substitution) are shown, the student writes the expansion, and step 3 then reveals. The fade falls there because the recall and the substitution repeat ex-1's pattern and the expansion, where the squared and fourth powers of 2 are combined with the factorials, is what the student must produce.
- Steps follow `expected_solution_path`. Relations: the series times the factor (new), the substitution (evaluate with u), the expansion (equivalent). A fluent solver writes the substituted series and the expanded terms, and holds the recall (Time). No productive-failure comparison: BC-CON-10024 is not in `PRODUCTIVE_FAILURE_TARGETS`.

## Scoring

BC-QA-10017 lists BC-PT-99037, 99035 and 99036. ex-2 tags BC-PT-99037 on the expanded terms, and its line is `reader_checks` output. ex-1 tags nothing and its scoring entry is empty: the 48 word line for BC-PT-99037 does not fit the 450 word brief band once the prediction and contrast pair are served (inferred array). BC-PT-99035 and 99036 score a polynomial for the function itself and are not tagged.

Point losses from research: a response that misremembers a standard series loses the terms that depend on it (sg-23:21, research/units/unit-10-infinite-sequences-series.md#10.14 Finding Taylor or Maclaurin Series for a Function); terms whose construction does not follow from the given series earn nothing for that point (BC-PT-99037, sg-26:23).

## Traps

Three errors meet the skills, in bundle order: BC-ERR-10005, BC-ERR-10040, BC-ERR-10041. Low band all three, mid band the first two. All on ex-1's draw, all with `fix_prompt` true, since each pair is distinct.

- err-BC-ERR-10005: the closed form used as the sum at \(x=1\), where \(|3x^2|=3\). The SymPy pair is the set of inputs for which the series is claimed to equal the function, all reals against \(\left(-\frac{1}{\sqrt3},\frac{1}{\sqrt3}\right)\). No possible reason line (brief band words).
- err-BC-ERR-10040: the geometric series recalled with alternating signs. No possible reason line.
- err-BC-ERR-10041: the 3 left unraised. Possible reason, BC-MIS-10026 (words from its description).

## Representations

None. The topic's Representations paragraph names BC-REP-11, 01 and 04 and the conversions first terms to a general term, function to series, series to numerical series; nothing figure-shaped.

## Prerequisite bridge

Five bridges, one per BC-PRQ, each from its `description_plain` and `failure_signature`: BC-PRQ-06002 (exponent rules), BC-PRQ-10002 (factorial simplification), BC-PRQ-10005 (geometric pattern), BC-PRQ-10007 (ratios of powers), BC-PRQ-10008 (general term from sigma form). Gated by state, not band.

## Time

ex-1 is the MCQ-shaped draw, Section I Part A, 2.14 minutes (research/exam/exam-structure.md#Section and part layout). As a free response part the shape scores 2 points, 3.33 minutes (docs/lessons/unit-10/README.md, section 5). A fluent solver writes the substituted series and the expanded terms; the recall of the standard series and the recognition are held [inferred]. The minutes go on expanding the powers of the inner expression.

## Checks

- chk-1, completion of ex-1, both bands: the substituted series given, the four terms asked. Key \(5+15x^2+45x^4+135x^6\).
- chk-2, isomorph, both bands. Draw: base exp, inner_power 2, scale -2, coefficient 3, count 3. Key \(3-6x^2+6x^4\).
- chk-3, MCQ, low band. Draw: base sin, inner_power 2, scale 3, coefficient 2, count 3. Key \(6x^2-9x^6+\frac{81}{20}x^{10}\). Distractors: \(6x^2-x^6+\frac{x^{10}}{20}\), the 3 not raised (BC-ERR-10041); \(6x^2-54x^6+486x^{10}\), factorials dropped (BC-ERR-10040); \(6x^2-\frac92x^6+\frac{81}{40}x^{10}\), the factor 2 on the first term only (BC-ERR-10041).

## Delivery

- orientation, ki-1, ki-2, ki-3: text. Rule 5: the skills carry BC-REP-11 and 01, none figure-bearing (docs/lessons/unit-10/README.md, section 6). No block is drawn, so the record carries `no_figure_reason`.
- ex-1, ex-2, the three error blocks: step_reveal. Rule 1.

## Band plan

- Low (full): prediction, orientation, bridges, ki-1 to ki-3, st-1 with the contrast pair, st-2, ex-1, chk-1, the three error blocks, ex-2 (faded from step 3) and its line, chk-2, chk-3. 708 words, 4.8 minutes.
- Mid (brief): prediction, orientation, bridges, ki-1, ki-2, st-1 with the contrast pair, ex-1, chk-1, err-BC-ERR-10005, err-BC-ERR-10040, chk-2. 441 words, 3.0 minutes.
- Refresher: ki-1, ki-2, the three error blocks, ex-1.

## Sources

- BC-CON-10024; BC-SKL-10061, BC-SKL-10062, BC-SKL-10063, BC-SKL-10064, BC-SKL-10065; BC-EK-LIM-8F1, BC-EK-LIM-8F2, BC-EK-LIM-8G1; ced:187, ced:199, ced:200
- BC-QA-10017, BC-QA-10003, BC-QA-10012; BC-PT-99037
- BC-ERR-10005, BC-ERR-10040, BC-ERR-10041; BC-MIS-10026
- BC-PRQ-06002, BC-PRQ-10002, BC-PRQ-10005, BC-PRQ-10007, BC-PRQ-10008
- sg-23:21
- research/units/unit-10-infinite-sequences-series.md#10.14 Finding Taylor or Maclaurin Series for a Function
- research/question-analysis/question-archetypes.md#BC-QA-10017 Maclaurin series built from a known series by substitution or multiplication
- research/question-analysis/question-archetypes.md#BC-QA-10003 Geometric series summed in closed form
- research/exam/exam-structure.md#Section and part layout
- [inferred] ex-1 untagged, BC-PT-99035 and 99036 untagged; the held steps; the geometric draw carrying BC-ERR-10005. Each settled as the inferred array states.

## Machine record

```json
{
 "id": "LSN-CON-10024",
 "kind": "concept",
 "target_id": "BC-CON-10024",
 "unit": "10",
 "skills": [
  "BC-SKL-10061",
  "BC-SKL-10062",
  "BC-SKL-10063",
  "BC-SKL-10064",
  "BC-SKL-10065"
 ],
 "prediction": {
  "id": "pr-1",
  "stem": {
   "text": "Let \\(g(u)=\\frac{1}{1-u}\\), so \\(g'''(0)=6\\). Predict the coefficient of \\(u^3\\) in its Maclaurin series.",
   "command_verb": "predict"
  },
  "format": "mcq",
  "options": [
   {
    "id": "A",
    "label": "\\(\\frac{1}{6}\\)",
    "is_key": false
   },
   {
    "id": "B",
    "label": "1",
    "is_key": true
   },
   {
    "id": "C",
    "label": "6",
    "is_key": false
   }
  ],
  "resolution": "Each derivative \\(g^{(n)}(0)\\) equals \\(n!\\), so every coefficient is \\(\\frac{n!}{n!}=1\\), and \\(\\frac{1}{1-u}=1+u+u^2+\\cdots\\). Any expression can stand in for \\(u\\).",
  "sources": [
   "BC-CON-10024",
   "research/units/unit-10-infinite-sequences-series.md#10.14 Finding Taylor or Maclaurin Series for a Function"
  ]
 },
 "no_figure_reason": "No skill carries a figure-bearing representation (the topic names series, symbolic and verbal forms) and no key idea describes a process, since each series is a recalled pattern of terms.",
 "orientation": {
  "text": "Four series are recalled, not rederived: \\(e^x\\), \\(\\sin x\\), \\(\\cos x\\) and \\(\\frac{1}{1-x}\\). A response writes the standard series, puts the whole expression in for \\(x\\), and gives the first nonzero terms.",
  "sources": [
   "BC-CON-10024",
   "research/units/unit-10-infinite-sequences-series.md#10.14 Finding Taylor or Maclaurin Series for a Function"
  ]
 },
 "key_ideas": [
  {
   "id": "ki-1",
   "ek_id": "BC-EK-LIM-8F1",
   "depth": "core",
   "text": "The Maclaurin series for \\(\\frac{1}{1-x}\\) is geometric: \\(1+x+x^2+\\cdots\\). It equals the function only where \\(|x|<1\\).",
   "notation": "geometric series",
   "quote": null,
   "sources": [
    "BC-EK-LIM-8F1",
    "ced:199",
    "ced:187",
    "research/units/unit-10-infinite-sequences-series.md#10.14 Finding Taylor or Maclaurin Series for a Function"
   ]
  },
  {
   "id": "ki-2",
   "ek_id": "BC-EK-LIM-8F2",
   "depth": "core",
   "text": "The series for \\(e^x\\), \\(\\sin x\\) and \\(\\cos x\\) build other series: \\(e^x=\\sum\\frac{x^n}{n!}\\), \\(\\sin x=\\sum\\frac{(-1)^nx^{2n+1}}{(2n+1)!}\\), \\(\\cos x=\\sum\\frac{(-1)^nx^{2n}}{(2n)!}\\).",
   "notation": "e to the x, sin x, cos x, one over one minus x",
   "quote": null,
   "sources": [
    "BC-EK-LIM-8F2",
    "ced:199",
    "research/units/unit-10-infinite-sequences-series.md#10.14 Finding Taylor or Maclaurin Series for a Function"
   ]
  },
  {
   "id": "ki-3",
   "ek_id": "BC-EK-LIM-8G1",
   "depth": "extended",
   "text": "A known series gives the series of a related function by putting an expression in for \\(x\\), raising the whole expression to each power, or multiplying every term by a factor. The centre stays at 0.",
   "notation": "substitution into a series",
   "quote": null,
   "sources": [
    "BC-EK-LIM-8G1",
    "ced:200",
    "research/question-analysis/question-archetypes.md#BC-QA-10017 Maclaurin series built from a known series by substitution or multiplication"
   ]
  }
 ],
 "strategy": [
  {
   "id": "st-1",
   "archetype_id": "BC-QA-10017",
   "cue": "A function built from a standard one, first nonzero terms wanted.",
   "method": "Write the standard series in \\(u\\), put the whole expression in for \\(u\\), then expand.",
   "rival": "Derivatives at 0, or substituting without raising the whole expression.",
   "separating_feature": "A standard function of an expression is recalled, not rederived.",
   "sources": [
    "BC-QA-10017",
    "research/question-analysis/question-archetypes.md#BC-QA-10017 Maclaurin series built from a known series by substitution or multiplication"
   ],
   "evidence_tag": "verified",
   "contrast": {
    "this": {
     "text": "Use the series for \\(\\frac{1}{1-x}\\) to write three nonzero terms of \\(\\frac{2}{1-5x^3}\\).",
     "archetype_id": "BC-QA-10017"
    },
    "not_this": {
     "text": "Use the series for \\(\\frac{1}{1-x}\\) to write three nonzero terms of \\(\\frac{1}{(1-x)^2}\\).",
     "why_not": "It is the derivative of \\(\\frac{1}{1-x}\\), so the series is differentiated."
    },
    "feature": "An expression in place of \\(x\\) means substitution; a derivative means term-by-term differentiation."
   }
  },
  {
   "id": "st-2",
   "archetype_id": "BC-QA-10003",
   "cue": "A series stated to be geometric, or a closed form to verify.",
   "method": "Divide consecutive terms for \\(r\\), state \\(|r|<1\\), then write first term over \\(1-r\\).",
   "rival": "The closed form with \\(|r|\\ge 1\\), or adding a few terms.",
   "separating_feature": "A constant quotient of consecutive terms makes it geometric.",
   "sources": [
    "BC-QA-10003",
    "research/question-analysis/question-archetypes.md#BC-QA-10003 Geometric series summed in closed form"
   ],
   "evidence_tag": "verified"
  }
 ],
 "worked_examples": [
  {
   "id": "ex-1",
   "archetype_id": "BC-QA-10017",
   "bands": [
    "low",
    "mid"
   ],
   "parameter_draw": {
    "base": "geometric",
    "inner_power": 2,
    "scale": 3,
    "coefficient": 5,
    "count": 4
   },
   "problem": {
    "text": "Use the Maclaurin series for \\(\\frac{1}{1-x}\\) to write the first four nonzero terms of the series for \\(f(x)=\\frac{5}{1-3x^2}\\).",
    "command_verb": "write"
   },
   "calculator_status": "no_calculator",
   "steps": [
    {
     "cue": "\\(f\\) is 5 times \\(\\frac{1}{1-u}\\), \\(u=3x^2\\).",
     "why": "The stem names the series."
    },
    {
     "cue": "Standard series, times 5.",
     "why": "The factor multiplies every term.",
     "expr": "5*(1 + u + u**2 + u**3)",
     "relation": "new"
    },
    {
     "cue": "Put \\(3x^2\\) in for every \\(u\\).",
     "why": "Each power of \\(u\\) becomes a power of \\(3x^2\\).",
     "expr": "5*(1 + 3*x**2 + (3*x**2)**2 + (3*x**2)**3)",
     "relation": "evaluate",
     "subs": {
      "u": "3*x**2"
     }
    },
    {
     "cue": "Expand each power.",
     "why": "Both 3 and \\(x^2\\) are raised.",
     "expr": "5 + 15*x**2 + 45*x**4 + 135*x**6",
     "relation": "equivalent"
    }
   ],
   "answer": {
    "form": "symbolic",
    "expr": "5 + 15*x**2 + 45*x**4 + 135*x**6"
   }
  },
  {
   "id": "ex-2",
   "archetype_id": "BC-QA-10017",
   "bands": [
    "low"
   ],
   "fade_from": 3,
   "parameter_draw": {
    "base": "cos",
    "inner_power": 3,
    "scale": 2,
    "coefficient": 6,
    "count": 3
   },
   "problem": {
    "text": "Use the Maclaurin series for \\(\\cos x\\) to write the first three nonzero terms of the series for \\(f(x)=6\\cos(2x^3)\\).",
    "command_verb": "write"
   },
   "calculator_status": "no_calculator",
   "steps": [
    {
     "cue": "Cosine has even powers and alternating signs.",
     "why": "Recalled, then multiplied by 6.",
     "expr": "6*(1 - u**2/2 + u**4/24)",
     "relation": "new"
    },
    {
     "cue": "Put \\(2x^3\\) in for every \\(u\\).",
     "why": "The whole expression is raised, so 2 is squared and to the fourth.",
     "expr": "6*(1 - (2*x**3)**2/2 + (2*x**3)**4/24)",
     "relation": "evaluate",
     "subs": {
      "u": "2*x**3"
     }
    },
    {
     "cue": "Expand and multiply by 6.",
     "why": "Three nonzero terms are asked for.",
     "expr": "6 - 12*x**6 + 4*x**12",
     "relation": "equivalent",
     "point_type_id": "BC-PT-99037"
    }
   ],
   "answer": {
    "form": "symbolic",
    "expr": "6 - 12*x**6 + 4*x**12"
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
   "point_type_ids": [
    "BC-PT-99037"
   ],
   "lines": [
    {
     "point_type_id": "BC-PT-99037",
     "text": "First nonzero terms of a series for a related function. Earned by: The requested count of nonzero terms for the derivative, antiderivative, or product function, listed or as part of a series (sg-25:26, sg-22:22). Not earned by: Terms whose construction does not follow from the given series (sg-26:23)."
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
    "text": "The series equals \\(\\frac{5}{1-3x^2}\\) for every \\(x\\), so at \\(x=1\\) it sums to \\(-\\frac{5}{2}\\).",
    "expr": "Interval(-oo, oo)"
   },
   "right_step": {
    "text": "It equals \\(\\frac{5}{1-3x^2}\\) only where \\(|3x^2|<1\\), so at \\(x=1\\) it diverges.",
    "expr": "Interval.open(-sqrt(3)/3, sqrt(3)/3)"
   },
   "relation": "distinct",
   "fix_prompt": true,
   "possible_reason": null,
   "sources": [
    "BC-ERR-10005"
   ]
  },
  {
   "error_id": "BC-ERR-10040",
   "observed_behavior": "The response writes the series for the exponential, the sine, the cosine, or one over one minus x with wrong signs, wrong parities of the powers, or missing factorials.",
   "scoring_consequence": "Every term built on the misremembered series is wrong, so the dependent points are lost (sg-23:21).",
   "wrong_step": {
    "text": "Alternating signs: \\(5-15x^2+45x^4-135x^6\\).",
    "expr": "5 - 15*x**2 + 45*x**4 - 135*x**6"
   },
   "right_step": {
    "text": "All signs positive: \\(5+15x^2+45x^4+135x^6\\).",
    "expr": "5 + 15*x**2 + 45*x**4 + 135*x**6"
   },
   "relation": "distinct",
   "fix_prompt": true,
   "possible_reason": null,
   "sources": [
    "BC-ERR-10040"
   ]
  },
  {
   "error_id": "BC-ERR-10041",
   "observed_behavior": "The response substitutes an expression for the variable in a known series but does not raise the whole expression to the required power, or loses a constant factor.",
   "scoring_consequence": "The resulting series is wrong from the first affected term onward.",
   "wrong_step": {
    "text": "The 3 is not raised: \\(5+15x^2+15x^4+15x^6\\).",
    "expr": "5 + 15*x**2 + 15*x**4 + 15*x**6"
   },
   "right_step": {
    "text": "The 3 is raised too: \\(5+15x^2+45x^4+135x^6\\).",
    "expr": "5 + 15*x**2 + 45*x**4 + 135*x**6"
   },
   "relation": "distinct",
   "fix_prompt": true,
   "possible_reason": {
    "misconception_id": "BC-MIS-10026",
    "text": "treats a substitution as relocating the centre of the series"
   },
   "sources": [
    "BC-ERR-10041",
    "BC-MIS-10026"
   ]
  }
 ],
 "representations": null,
 "prerequisite_bridges": [
  {
   "prq_id": "BC-PRQ-06002",
   "text": "Exponents: \\((3x^2)^3=27x^6\\)."
  },
  {
   "prq_id": "BC-PRQ-10002",
   "text": "Factorials: \\(\\frac{(n+1)!}{n!}=n+1\\)."
  },
  {
   "prq_id": "BC-PRQ-10005",
   "text": "Geometric means a constant quotient."
  },
  {
   "prq_id": "BC-PRQ-10007",
   "text": "Like bases: subtract exponents."
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
    3,
    4
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
   "archetype_id": "BC-QA-10017",
   "parameter_draw": {
    "base": "geometric",
    "inner_power": 2,
    "scale": 3,
    "coefficient": 5,
    "count": 4
   },
   "completes": "ex-1",
   "stem": {
    "text": "The series is \\(5\\left(1+3x^2+(3x^2)^2+(3x^2)^3\\right)\\). Write its four terms.",
    "command_verb": "write"
   },
   "key": {
    "form": "symbolic",
    "expr": "5 + 15*x**2 + 45*x**4 + 135*x**6"
   },
   "steps": [
    {
     "text": "Expand.",
     "expr": "5*(1 + 3*x**2 + (3*x**2)**2 + (3*x**2)**3)",
     "relation": "new"
    },
    {
     "text": "Terms.",
     "expr": "5 + 15*x**2 + 45*x**4 + 135*x**6",
     "relation": "equivalent"
    }
   ],
   "calculator_status": "no_calculator",
   "skills": [
    "BC-SKL-10063"
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
   "archetype_id": "BC-QA-10017",
   "parameter_draw": {
    "base": "exp",
    "inner_power": 2,
    "scale": -2,
    "coefficient": 3,
    "count": 3
   },
   "stem": {
    "text": "Use the series for \\(e^x\\) to write the first three nonzero terms of the series for \\(3e^{-2x^2}\\).",
    "command_verb": "write"
   },
   "key": {
    "form": "symbolic",
    "expr": "3 - 6*x**2 + 6*x**4"
   },
   "steps": [
    {
     "text": "Standard series, times 3.",
     "expr": "3*(1 + u + u**2/2)",
     "relation": "new"
    },
    {
     "text": "Put \\(-2x^2\\) in for u.",
     "expr": "3*(1 + (-2*x**2) + (-2*x**2)**2/2)",
     "relation": "evaluate",
     "subs": {
      "u": "-2*x**2"
     }
    },
    {
     "text": "Expand.",
     "expr": "3 - 6*x**2 + 6*x**4",
     "relation": "equivalent"
    }
   ],
   "calculator_status": "no_calculator",
   "skills": [
    "BC-SKL-10061",
    "BC-SKL-10064"
   ]
  },
  {
   "id": "chk-3",
   "check_kind": "mcq",
   "format": "mcq",
   "bands": [
    "low"
   ],
   "archetype_id": "BC-QA-10017",
   "parameter_draw": {
    "base": "sin",
    "inner_power": 2,
    "scale": 3,
    "coefficient": 2,
    "count": 3
   },
   "stem": {
    "text": "The first three nonzero terms of the Maclaurin series for \\(2\\sin(3x^2)\\) are",
    "command_verb": "identify"
   },
   "key": {
    "form": "symbolic",
    "expr": "6*x**2 - 9*x**6 + 81*x**10/20"
   },
   "steps": [
    {
     "text": "Sine series, times 2.",
     "expr": "2*(u - u**3/6 + u**5/120)",
     "relation": "new"
    },
    {
     "text": "Put \\(3x^2\\) in for u.",
     "expr": "2*(3*x**2 - (3*x**2)**3/6 + (3*x**2)**5/120)",
     "relation": "evaluate",
     "subs": {
      "u": "3*x**2"
     }
    },
    {
     "text": "Expand.",
     "expr": "6*x**2 - 9*x**6 + 81*x**10/20",
     "relation": "equivalent"
    }
   ],
   "options": [
    {
     "id": "A",
     "is_key": false,
     "expr": "6*x**2 - x**6 + x**10/20",
     "error_path": "BC-ERR-10041",
     "derivation": "the 3 is not raised: u**n replaced by 3*x**(2n)"
    },
    {
     "id": "B",
     "is_key": true,
     "expr": "6*x**2 - 9*x**6 + 81*x**10/20",
     "error_path": null
    },
    {
     "id": "C",
     "is_key": false,
     "expr": "6*x**2 - 54*x**6 + 486*x**10",
     "error_path": "BC-ERR-10040",
     "derivation": "sine recalled with the factorials dropped"
    },
    {
     "id": "D",
     "is_key": false,
     "expr": "6*x**2 - 9*x**6/2 + 81*x**10/40",
     "error_path": "BC-ERR-10041",
     "derivation": "the factor 2 applied to the first term only"
    }
   ],
   "calculator_status": "no_calculator",
   "skills": [
    "BC-SKL-10062",
    "BC-SKL-10064",
    "BC-SKL-10065"
   ]
  }
 ],
 "delivery": [
  {
   "block": "orientation",
   "mode": "text",
   "reason": "rule 5: a statement of what a response shows",
   "sources": [
    "BC-CON-10024"
   ]
  },
  {
   "block": "ki-1",
   "mode": "text",
   "reason": "rule 5: BC-REP-11, 01 on BC-SKL-10063, a recalled series and not a process",
   "sources": [
    "BC-SKL-10063"
   ]
  },
  {
   "block": "ki-2",
   "mode": "text",
   "reason": "rule 5: BC-REP-11, 01 on BC-SKL-10061, 10062, recalled series",
   "sources": [
    "BC-SKL-10061",
    "BC-SKL-10062"
   ]
  },
  {
   "block": "ki-3",
   "mode": "text",
   "reason": "rule 5: BC-REP-11, 01 on BC-SKL-10064, 10065",
   "sources": [
    "BC-SKL-10064",
    "BC-SKL-10065"
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
  "ki-2",
  "err-BC-ERR-10005",
  "err-BC-ERR-10040",
  "err-BC-ERR-10041",
  "ex-1"
 ],
 "research_lines": [
  {
   "file": "research/units/unit-10-infinite-sequences-series.md",
   "line": "Recall of the standard series is scored indirectly, since a response that misremembers one loses the terms that depend on it."
  }
 ],
 "inferred": [
  {
   "claim": "ex-1 tags no point type, because its BC-PT-99037 reader line (48 words) does not fit the brief cap beside the prediction and contrast pair; ex-2 carries the tag. BC-PT-99035 and 99036 score a polynomial rather than a series for a related function and are untagged.",
   "settles": "A brief cap that admits the reader line, and a rubric for this shape that separates the first terms from the remaining terms."
  },
  {
   "claim": "BC-ERR-10005 is shown on the geometric draw of ex-1, where the closed form fails outside the interval, and its right step is the set of inputs where the series equals the function.",
   "settles": "A parameter_spec task on BC-QA-10017 that asks for the value at an input."
  },
  {
   "claim": "A fluent solver writes the substituted series and the expanded terms and holds the recall of the standard series.",
   "settles": "Timing data per step once the fluency telemetry exists."
  }
 ],
 "sources": [
  "BC-CON-10024",
  "BC-SKL-10061",
  "BC-SKL-10062",
  "BC-SKL-10063",
  "BC-SKL-10064",
  "BC-SKL-10065",
  "BC-EK-LIM-8F1",
  "BC-EK-LIM-8F2",
  "BC-EK-LIM-8G1",
  "ced:199",
  "ced:200",
  "ced:187",
  "BC-QA-10017",
  "BC-QA-10003",
  "BC-QA-10012",
  "BC-PT-99037",
  "BC-ERR-10005",
  "BC-ERR-10040",
  "BC-ERR-10041",
  "BC-MIS-10026",
  "BC-PRQ-06002",
  "BC-PRQ-10002",
  "BC-PRQ-10005",
  "BC-PRQ-10007",
  "BC-PRQ-10008",
  "sg-23:21",
  "research/units/unit-10-infinite-sequences-series.md#10.14 Finding Taylor or Maclaurin Series for a Function",
  "research/question-analysis/question-archetypes.md#BC-QA-10017 Maclaurin series built from a known series by substitution or multiplication",
  "research/question-analysis/question-archetypes.md#BC-QA-10003 Geometric series summed in closed form",
  "research/exam/exam-structure.md#Section and part layout"
 ],
 "word_count": {
  "full": 708,
  "brief": 441
 },
 "read_minutes": {
  "full": 4.8,
  "brief": 3.0
 }
}
```
