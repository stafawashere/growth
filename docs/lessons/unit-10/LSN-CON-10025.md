---
title: LSN-CON-10025 Term-by-term differentiation and integration of a power series
research_date: 2026-09-29
status: designed
purpose: Authoring spec for the concept lesson on BC-CON-10025, differentiating and integrating a power series term by term with its constant fixed from a given value and a geometric series recognised in closed form, built from authoring_bundle("BC-CON-10025") and the research files it cites, so an author fills plan 15's lesson record without making a teaching decision.
---

# LSN-CON-10025 Term-by-term differentiation and integration of a power series

Concept BC-CON-10025 (skills BC-SKL-10068, BC-SKL-10069, BC-SKL-10072), topic 10.15 of Unit 10, BC only (ced:200), loaded by three archetypes, BC-QA-10019 and BC-QA-10018 (family taylor-construction) and BC-QA-10003 (family series-value). Hard parents inside the unit are BC-CON-10004, BC-CON-10023 and BC-CON-10024, with BC-SKL-06047 outside it (docs/lessons/unit-10/README.md, section 1): the geometric series, the Taylor series general term, the standard series and the antiderivative are assumed.

## Prediction

Served first, both bands: an `mcq` on ex-1's numbers. The stem gives \(f'(x)=2+6x^2+18x^4+\cdots\) and \(f(0)=5\) and asks for the first three terms of \(f\). Key A, \(5+2x+2x^3\). The distractors are \(5+2x+6x^3\) (the power raised and the coefficient left undivided) and \(2x+2x^3+\frac{18}{5}x^5\) (no constant). A polynomial antiderivative with a value at 0 answers it before any rule about infinite series is stated. The resolution shows the term rule and the constant, with no verdict. Source: BC-CON-10025 and the topic section.

## Orientation

Served text, from BC-CON-10025 `description_plain` ("A power series can be differentiated or integrated one term at a time") and the topic's Assessment behaviour paragraph (research/units/unit-10-infinite-sequences-series.md#10.15 Representing Functions as Power Series): the MCQ asks for a series representation built by an operation, the FRQ for the terms and the general term of a differentiated series with its radius. The orientation states what a response shows. No count, no frequency.

## Key ideas

Three essential knowledge statements map from the three skills. ki-1 (core) is BC-EK-LIM-8G1 (ced:200), the operation on a known series, with the Notation line of the topic (both the displayed terms and the general term, and the constant from a given value). ki-2 (core) is BC-EK-LIM-8D6 (ced:198), the preserved radius. ki-3 (extended, low band only) is BC-EK-LIM-8F1 (ced:199), the geometric series, with the condition on the ratio from BC-EK-LIM-7A4 (ced:187). No anchor quote: each CED sentence adds nothing the paraphrase lacks and costs words in the brief band.

## Recognition

BC-QA-10019 (research/question-analysis/question-archetypes.md#BC-QA-10019 Function represented by term-by-term integration of a known series) loads BC-SKL-10069. `common_givens`: "a known series or Taylor polynomial for the integrand", "a value of the antiderivative at one input". `asked_to_produce`: "a series or polynomial for the antiderivative", "the constant fixed by the supplied value". Shapes: the FRQ parts BC-FRQ-2019-Q6-C and BC-FRQ-2014-Q6-C.

BC-QA-10018 (research/question-analysis/question-archetypes.md#BC-QA-10018 Series differentiated term by term with its radius carried over) loads BC-SKL-10068, 10070 and 10071. `common_givens`: "a power series with its general term", "the radius of convergence of the original series". `asked_to_produce`: "the first nonzero terms of the derivative series", "the general term of the derivative series", "the radius of convergence of the derivative series". Shapes: BC-FRQ-2024-Q6-C, BC-FRQ-2025-Q6-B, BC-MCQ-CED-020.

BC-QA-10003 (research/question-analysis/question-archetypes.md#BC-QA-10003 Geometric series summed in closed form) loads BC-SKL-10072: a series stated to be geometric, or a closed form to verify.

The near miss of the contrast pair is the substitution form, a stem that gives the function itself and asks for four terms. It belongs to BC-CON-10024 (archetype BC-QA-10017), so it comes from outside BC-QA-10019. The unit map names the pair: a derivative or an integral of a known function selects the operation on the terms, a composite argument selects substitution (docs/lessons/unit-10/README.md, section 3).

## Method choice

- st-1, BC-QA-10019. Cue from `common_givens`. Method from `expected_solution_path`: series for the integrand, antidifferentiate term by term, constant from the value. Rival: `common_distractors` "omitting the constant of integration" and "integrating with respect to the index". Separating feature: an antiderivative relation with a given value needs the constant. Carries the contrast pair.
- st-2, BC-QA-10018. Cue from `common_givens` and `asked_to_produce`. Method: differentiate the displayed terms and the general term, then state the radius unchanged. Rival: `wrong_approaches` "differentiating the general term with respect to the index (BC-ERR-99018)" and "claiming the derived series has a different radius (BC-ERR-10042)". Separating feature: the variable is \(x\).
- st-3, BC-QA-10003. Cue from `common_givens`. Method: ratio, condition, quotient. Rival: `wrong_approaches`, BC-ERR-10005. Separating feature: a constant quotient.
No served field opens with the reader's own label, and all three blocks have both cue fields, so none is inferred.

## Solution path

- ex-1, BC-QA-10019, both bands, no calculator. Draw: inner_power 2, sign minus, count 4, scale 3, coefficient 2, start_value 5. \(f'(x)=\frac{2}{1-3x^2}\), \(f(0)=5\), key \(5+2x+2x^3+\frac{18}{5}x^5\), computed with SymPy. The sign label minus is read as a denominator \(1-kx^p\) (inferred array). No published item on BC-QA-10019 carries this draw.
- ex-2, BC-QA-10018, low band, no calculator. Draw: sign alternating, given none, centre 2, base 3, coefficient 4. \(f=\sum\frac{4(-1)^n(x-2)^n}{n^23^n}\), radius 3, derivative terms \(-\frac43+\frac29(x-2)-\frac{4}{81}(x-2)^2\), general term \(\frac{4(-1)^n(x-2)^{n-1}}{n3^n}\), all computed with SymPy.
- ex-2 is faded from step 3: steps 1 and 2 (the displayed terms of \(f\) and their derivative) are shown, the student writes the radius and the general term, and steps 3 and 4 then reveal. The fade falls there because the term-wise differentiation repeats ex-1's operation and the radius statement and the general term are what the student must produce.
- Relations: the integrand series (new), the antiderivative terms (integrate, with the constant C), the constant fixed (evaluate at C). A fluent solver writes the antiderivative terms and the constant, and holds the recognition of the geometric form (Time). No productive-failure comparison: BC-CON-10025 is not in `PRODUCTIVE_FAILURE_TARGETS`.

## Scoring

BC-QA-10019 lists BC-PT-99003, 99004 and 99067. BC-QA-10018 lists BC-PT-99037, 99038, 99067, 99047, 99035 and 99036. ex-1 tags nothing and its scoring entry is empty: the 39 word line for BC-PT-99003 does not fit the 450 word brief band once the prediction and contrast pair are served (inferred array). ex-2 tags BC-PT-99038 on the general term and BC-PT-99047 on the radius, and its lines are `reader_checks` output. BC-PT-99037 is not tagged, to keep the full form under 900 words.

Point losses from research: the radius point rests on the preservation statement (sg-24:22, research/units/unit-10-infinite-sequences-series.md#10.15 Representing Functions as Power Series); an ellipsis with no closed form does not earn the general term (BC-PT-99038, sg-22:22).

## Traps

Five errors meet the skills, in bundle order: BC-ERR-07026, BC-ERR-10005, BC-ERR-10041, BC-ERR-99018, BC-ERR-10006. BC-ERR-10006 falls past the cap of 4. Low band all four, mid band the first two. BC-ERR-07026, 10005 and 10041 are on ex-1's draw, BC-ERR-99018 on ex-2's. All carry `fix_prompt` true, since each pair is distinct.

- err-BC-ERR-07026: the constant left out. No possible reason line (brief band words); the record links BC-MIS-07016 and 06018.
- err-BC-ERR-10005: the closed form used at \(x=1\), where \(|3x^2|=3\). The SymPy pair is the set of inputs for which the series is claimed to equal the function, all reals against \(\left(-\frac{1}{\sqrt3},\frac{1}{\sqrt3}\right)\). No possible reason line.
- err-BC-ERR-10041: the 3 left unraised in the integrand series. Possible reason, BC-MIS-10026.
- err-BC-ERR-99018: the coefficient left as \(n^2\) after the power rule. No possible reason line.

## Representations

None. The topic's Representations paragraph names BC-REP-11, 01 and 04 and the conversions series to derived series, geometric series to closed form, interval to verdict; nothing figure-shaped.

## Prerequisite bridge

Five bridges, one per BC-PRQ, each from its `description_plain` and `failure_signature`: BC-PRQ-06002 (exponent rules, the power rule in reverse), BC-PRQ-06013 (the variable of integration), BC-PRQ-10001 (the absolute value inequality), BC-PRQ-10005 (geometric pattern), BC-PRQ-10008 (general term from sigma form). Gated by state, not band.

## Time

ex-1 is the MCQ-shaped draw, Section I Part A, 2.14 minutes (research/exam/exam-structure.md#Section and part layout). As a free response part the integrated-series shape is 2 points, 3.33 minutes, and the differentiated-series shape 2 points, 3.33 minutes (docs/lessons/unit-10/README.md, section 5; the integrated shape is inferred there). A fluent solver writes the antiderivative terms and the constant; the recognition of the geometric form is held [inferred]. The minutes go on the division by each new exponent.

## Checks

- chk-1, completion of ex-1, both bands: the antiderivative terms given with C, the four terms of \(f\) asked. Key \(5+2x+2x^3+\frac{18}{5}x^5\).
- chk-2, isomorph, both bands. Draw: inner_power 1, sign plus, count 4, scale 2, coefficient 3, start_value -4. \(f'=\frac{3}{1+2x}\). Key \(-4+3x-3x^2+4x^3\).
- chk-3, MCQ, low band. Draw: inner_power 2, sign minus, count 4, scale 4, coefficient 3, start_value -2. Key \(-2+3x+4x^3+\frac{48}{5}x^5\). Distractors: \(3x+4x^3+\frac{48}{5}x^5+\frac{192}{7}x^7\), no constant (BC-ERR-07026); \(-2+3x+12x^3+48x^5\), coefficients left undivided (BC-ERR-99018); \(-2+3x+4x^3+\frac{12}{5}x^5\), the 4 not raised in the integrand series (BC-ERR-10041).

## Delivery

- orientation, ki-1, ki-2, ki-3: text. Rule 5: the skills carry BC-REP-11 and 01, none figure-bearing (docs/lessons/unit-10/README.md, section 6). No block is drawn, so the record carries `no_figure_reason`.
- ex-1, ex-2, the four error blocks: step_reveal. Rule 1.

## Band plan

- Low (full): prediction, orientation, bridges, ki-1 to ki-3, st-1 with the contrast pair, st-2, st-3, ex-1, chk-1, the four error blocks, ex-2 (faded from step 3) and its lines, chk-2, chk-3. 893 words, 6.0 minutes.
- Mid (brief): prediction, orientation, bridges, ki-1, ki-2, st-1 with the contrast pair, ex-1, chk-1, err-BC-ERR-07026, err-BC-ERR-10005, chk-2. 449 words, 3.0 minutes.
- Refresher: ki-1, ki-2, the four error blocks, ex-1.

## Sources

- BC-CON-10025; BC-SKL-10068, BC-SKL-10069, BC-SKL-10072; BC-EK-LIM-8G1, BC-EK-LIM-8D6, BC-EK-LIM-8F1; ced:187, ced:198, ced:199, ced:200
- BC-QA-10019, BC-QA-10018, BC-QA-10003; BC-PT-99003, BC-PT-99037, BC-PT-99038, BC-PT-99047
- BC-ERR-07026, BC-ERR-10005, BC-ERR-10041, BC-ERR-99018; BC-MIS-10026
- BC-PRQ-06002, BC-PRQ-06013, BC-PRQ-10001, BC-PRQ-10005, BC-PRQ-10008
- research/units/unit-10-infinite-sequences-series.md#10.15 Representing Functions as Power Series
- research/question-analysis/question-archetypes.md#BC-QA-10019 Function represented by term-by-term integration of a known series
- research/question-analysis/question-archetypes.md#BC-QA-10018 Series differentiated term by term with its radius carried over
- research/question-analysis/question-archetypes.md#BC-QA-10003 Geometric series summed in closed form
- research/exam/exam-structure.md#Section and part layout
- [inferred] the sign label reading; the errors shown on the integrand and the coefficient; the untagged points; the held steps. Each settled as the inferred array states.

## Machine record

```json
{
 "id": "LSN-CON-10025",
 "kind": "concept",
 "target_id": "BC-CON-10025",
 "unit": "10",
 "skills": [
  "BC-SKL-10068",
  "BC-SKL-10069",
  "BC-SKL-10072"
 ],
 "prediction": {
  "id": "pr-1",
  "stem": {
   "text": "\\(f'(x)=2+6x^2+18x^4+\\cdots\\) and \\(f(0)=5\\). Predict the first three terms of the series for \\(f(x)\\).",
   "command_verb": "predict"
  },
  "format": "mcq",
  "options": [
   {
    "id": "A",
    "label": "\\(5+2x+2x^3\\)",
    "is_key": true
   },
   {
    "id": "B",
    "label": "\\(5+2x+6x^3\\)",
    "is_key": false
   },
   {
    "id": "C",
    "label": "\\(2x+2x^3+\\frac{18}{5}x^5\\)",
    "is_key": false
   }
  ],
  "resolution": "Each term is antidifferentiated as it stands, \\(\\int 6x^2\\,dx=2x^3\\), and \\(f(0)=5\\) supplies the constant. The same holds for the whole series, term by term.",
  "sources": [
   "BC-CON-10025",
   "research/units/unit-10-infinite-sequences-series.md#10.15 Representing Functions as Power Series"
  ]
 },
 "no_figure_reason": "No skill carries a figure-bearing representation (the topic names series, symbolic and verbal forms) and no key idea describes a process, since the operation is applied to displayed terms and a general term.",
 "orientation": {
  "text": "A power series is differentiated or integrated one term at a time, on the displayed terms and the general term. Integration needs a constant from a given value. A response shows the new terms.",
  "sources": [
   "BC-CON-10025",
   "research/units/unit-10-infinite-sequences-series.md#10.15 Representing Functions as Power Series"
  ]
 },
 "key_ideas": [
  {
   "id": "ki-1",
   "ek_id": "BC-EK-LIM-8G1",
   "depth": "core",
   "text": "A known series gives a series for a related function by term-by-term differentiation or integration, with respect to \\(x\\). Integration also needs the constant, fixed by a given value of the function.",
   "notation": "term-by-term differentiation; term-by-term integration",
   "quote": null,
   "sources": [
    "BC-EK-LIM-8G1",
    "ced:200",
    "research/units/unit-10-infinite-sequences-series.md#10.15 Representing Functions as Power Series"
   ]
  },
  {
   "id": "ki-2",
   "ek_id": "BC-EK-LIM-8D6",
   "depth": "core",
   "text": "Differentiating or integrating term by term leaves the radius of convergence unchanged.",
   "notation": "same radius",
   "quote": null,
   "sources": [
    "BC-EK-LIM-8D6",
    "ced:198",
    "research/units/unit-10-infinite-sequences-series.md#10.15 Representing Functions as Power Series"
   ]
  },
  {
   "id": "ki-3",
   "ek_id": "BC-EK-LIM-8F1",
   "depth": "extended",
   "text": "A geometric power series with first term \\(a\\) and ratio \\(r\\) sums to \\(\\frac{a}{1-r}\\) where \\(|r|<1\\). It is the series of \\(\\frac{1}{1-x}\\) with an expression put in for \\(x\\).",
   "notation": "geometric series",
   "quote": null,
   "sources": [
    "BC-EK-LIM-8F1",
    "ced:199",
    "ced:187",
    "research/units/unit-10-infinite-sequences-series.md#10.15 Representing Functions as Power Series"
   ]
  }
 ],
 "strategy": [
  {
   "id": "st-1",
   "archetype_id": "BC-QA-10019",
   "cue": "A known series for the integrand, and a value of the antiderivative.",
   "method": "Write the series for the integrand, antidifferentiate each term, then fix the constant from the value.",
   "rival": "Omitting the constant, or integrating with respect to the index.",
   "separating_feature": "An antiderivative relation with a given value needs the constant.",
   "sources": [
    "BC-QA-10019",
    "research/question-analysis/question-archetypes.md#BC-QA-10019 Function represented by term-by-term integration of a known series"
   ],
   "evidence_tag": "verified",
   "contrast": {
    "this": {
     "text": "Let \\(f'(x)=\\frac{2}{1-3x^2}\\) and \\(f(0)=5\\). Use a geometric series to write four nonzero terms of \\(f\\).",
     "archetype_id": "BC-QA-10019"
    },
    "not_this": {
     "text": "Use a geometric series to write four nonzero terms of \\(f(x)=\\frac{2}{1-3x^2}\\).",
     "why_not": "The function itself is given, so an expression goes in for \\(x\\) and nothing is integrated."
    },
    "feature": "A derivative or antiderivative relation means term-by-term integration; an expression in place of \\(x\\) means substitution."
   }
  },
  {
   "id": "st-2",
   "archetype_id": "BC-QA-10018",
   "cue": "A power series with its general term, and its derivative series wanted.",
   "method": "Differentiate the displayed terms and the general term with respect to \\(x\\), then state the radius as unchanged.",
   "rival": "Differentiating with respect to the index, or recomputing the radius.",
   "separating_feature": "The variable of differentiation is \\(x\\), and the index is a label.",
   "sources": [
    "BC-QA-10018",
    "research/question-analysis/question-archetypes.md#BC-QA-10018 Series differentiated term by term with its radius carried over"
   ],
   "evidence_tag": "verified"
  },
  {
   "id": "st-3",
   "archetype_id": "BC-QA-10003",
   "cue": "A series stated to be geometric, or a closed form to verify.",
   "method": "Divide consecutive terms for \\(r\\), state \\(|r|<1\\), then write first term over \\(1-r\\).",
   "rival": "The closed form with \\(|r|\\ge 1\\), or the index zero term when the series starts later.",
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
   "archetype_id": "BC-QA-10019",
   "bands": [
    "low",
    "mid"
   ],
   "parameter_draw": {
    "inner_power": 2,
    "sign": "minus",
    "count": 4,
    "scale": 3,
    "coefficient": 2,
    "start_value": 5
   },
   "problem": {
    "text": "Let \\(f'(x)=\\frac{2}{1-3x^2}\\) and \\(f(0)=5\\). Use a geometric series to write the first four nonzero terms of the series for \\(f(x)\\).",
    "command_verb": "write"
   },
   "calculator_status": "no_calculator",
   "steps": [
    {
     "cue": "\\(f'\\) is 2 times \\(\\frac{1}{1-u}\\), \\(u=3x^2\\).",
     "why": "Geometric series with ratio \\(3x^2\\)."
    },
    {
     "cue": "Series for \\(f'\\), three terms.",
     "why": "The constant term of \\(f\\) is the fourth.",
     "expr": "2 + 6*x**2 + 18*x**4",
     "relation": "new"
    },
    {
     "cue": "Antidifferentiate each term.",
     "why": "Raise each power, divide by it.",
     "expr": "C + 2*x + 2*x**3 + 18*x**5/5",
     "relation": "integrate",
     "variable": "x"
    },
    {
     "cue": "\\(f(0)=5\\).",
     "why": "The value at 0 fixes the constant.",
     "expr": "5 + 2*x + 2*x**3 + 18*x**5/5",
     "relation": "evaluate",
     "subs": {
      "C": "5"
     }
    }
   ],
   "answer": {
    "form": "symbolic",
    "expr": "5 + 2*x + 2*x**3 + 18*x**5/5"
   }
  },
  {
   "id": "ex-2",
   "archetype_id": "BC-QA-10018",
   "bands": [
    "low"
   ],
   "fade_from": 3,
   "parameter_draw": {
    "sign": "alternating",
    "given": "none",
    "centre": 2,
    "base": 3,
    "coefficient": 4
   },
   "problem": {
    "text": "The series for \\(f\\) is \\(\\sum_{n=1}^{\\infty}\\frac{4(-1)^n(x-2)^n}{n^23^n}\\), with radius 3. Write the first three nonzero terms of the series for \\(f'\\), its radius, and its general term.",
    "command_verb": "write"
   },
   "calculator_status": "no_calculator",
   "steps": [
    {
     "cue": "Displayed terms of \\(f\\), \\(n=1,2,3\\).",
     "why": "The operation acts on them first.",
     "expr": "-4*(x - 2)/3 + (x - 2)**2/9 - 4*(x - 2)**3/243",
     "relation": "new"
    },
    {
     "cue": "Differentiate each term with respect to \\(x\\).",
     "why": "Each power drops by one.",
     "expr": "-4/3 + 2*(x - 2)/9 - 4*(x - 2)**2/81",
     "relation": "differentiate",
     "variable": "x"
    },
    {
     "cue": "Differentiation preserves the radius.",
     "why": "The radius carries over, not recomputed.",
     "expr": "3",
     "relation": "new",
     "point_type_id": "BC-PT-99047"
    },
    {
     "cue": "General term: differentiate in \\(x\\), and \\(n\\) cancels one \\(n\\).",
     "why": "The index is a label, not the variable.",
     "expr": "4*(-1)**n*(x - 2)**(n - 1)/(n*3**n)",
     "relation": "new",
     "point_type_id": "BC-PT-99038"
    }
   ],
   "answer": {
    "form": "symbolic",
    "expr": "4*(-1)**n*(x - 2)**(n - 1)/(n*3**n)"
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
    "BC-PT-99047",
    "BC-PT-99038"
   ],
   "lines": [
    {
     "point_type_id": "BC-PT-99047",
     "text": "Radius of convergence stated explicitly. Earned by: An explicit statement of the radius, obtained either from the ratio test inequality or by citing the radius of a related series (sg-21:24, sg-24:22). Not earned by: An interval presented with no identification of the radius, which sg-21:24 states does not earn the point."
    },
    {
     "point_type_id": "BC-PT-99038",
     "text": "General term of a series. Earned by: The correct general term, presented on its own or as the closing term of a polynomial or series (sg-25:26, sg-22:22). Not earned by: An ellipsis with no closed form for the nth term (sg-22:22)."
    }
   ]
  }
 ],
 "common_errors": [
  {
   "error_id": "BC-ERR-07026",
   "observed_behavior": "The antiderivative equation is written with no constant.",
   "scoring_consequence": "At most the first two points are available; the guideline caps the response there.",
   "wrong_step": {
    "text": "No constant: \\(2x+2x^3+\\frac{18}{5}x^5\\).",
    "expr": "2*x + 2*x**3 + 18*x**5/5"
   },
   "right_step": {
    "text": "Constant 5: \\(5+2x+2x^3+\\frac{18}{5}x^5\\).",
    "expr": "5 + 2*x + 2*x**3 + 18*x**5/5"
   },
   "relation": "distinct",
   "fix_prompt": true,
   "possible_reason": null,
   "sources": [
    "BC-ERR-07026"
   ]
  },
  {
   "error_id": "BC-ERR-10005",
   "observed_behavior": "The response applies the closed form for the sum without checking that the absolute value of the ratio is less than one, and reports a finite value for a divergent series.",
   "scoring_consequence": "A finite value reported for a divergent series loses the answer point and any reasoning point attached to it.",
   "wrong_step": {
    "text": "The series equals \\(\\frac{2}{1-3x^2}\\) for every \\(x\\), so at \\(x=1\\) it sums to \\(-1\\).",
    "expr": "Interval(-oo, oo)"
   },
   "right_step": {
    "text": "It equals \\(\\frac{2}{1-3x^2}\\) only where \\(|3x^2|<1\\), so at \\(x=1\\) it diverges.",
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
   "error_id": "BC-ERR-10041",
   "observed_behavior": "The response substitutes an expression for the variable in a known series but does not raise the whole expression to the required power, or loses a constant factor.",
   "scoring_consequence": "The resulting series is wrong from the first affected term onward.",
   "wrong_step": {
    "text": "The 3 is not raised: \\(2+6x^2+6x^4\\).",
    "expr": "2 + 6*x**2 + 6*x**4"
   },
   "right_step": {
    "text": "The 3 is raised too: \\(2+6x^2+18x^4\\).",
    "expr": "2 + 6*x**2 + 18*x**4"
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
  },
  {
   "error_id": "BC-ERR-99018",
   "observed_behavior": "Responses can write the first several terms of a series but cannot differentiate the general term, apply the quotient rule to it, differentiate with respect to the index, or simplify the resulting coefficient correctly.",
   "scoring_consequence": "The general term point is not earned; the first terms point may be earned separately.",
   "wrong_step": {
    "text": "The \\(n\\) is left in the square: general term \\(\\frac{4(-1)^n(x-2)^{n-1}}{n^23^n}\\).",
    "expr": "4*(-1)**n*(x - 2)**(n - 1)/(n**2*3**n)"
   },
   "right_step": {
    "text": "The power rule brings down \\(n\\): \\(\\frac{4(-1)^n(x-2)^{n-1}}{n\\,3^n}\\).",
    "expr": "4*(-1)**n*(x - 2)**(n - 1)/(n*3**n)"
   },
   "relation": "distinct",
   "fix_prompt": true,
   "possible_reason": null,
   "sources": [
    "BC-ERR-99018"
   ]
  }
 ],
 "representations": null,
 "prerequisite_bridges": [
  {
   "prq_id": "BC-PRQ-06002",
   "text": "Exponents: \\(\\int x^{2n}dx=\\frac{x^{2n+1}}{2n+1}\\)."
  },
  {
   "prq_id": "BC-PRQ-06013",
   "text": "Integrate in \\(x\\), not \\(n\\)."
  },
  {
   "prq_id": "BC-PRQ-10001",
   "text": "\\(|r|<1\\) means \\(-1<r<1\\)."
  },
  {
   "prq_id": "BC-PRQ-10005",
   "text": "Geometric means a constant quotient."
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
   "archetype_id": "BC-QA-10019",
   "parameter_draw": {
    "inner_power": 2,
    "sign": "minus",
    "count": 4,
    "scale": 3,
    "coefficient": 2,
    "start_value": 5
   },
   "completes": "ex-1",
   "stem": {
    "text": "The antiderivative terms are \\(C+2x+2x^3+\\frac{18}{5}x^5\\), and \\(f(0)=5\\). Write the four terms of \\(f\\).",
    "command_verb": "write"
   },
   "key": {
    "form": "symbolic",
    "expr": "5 + 2*x + 2*x**3 + 18*x**5/5"
   },
   "steps": [
    {
     "text": "Antiderivative terms.",
     "expr": "C + 2*x + 2*x**3 + 18*x**5/5",
     "relation": "new"
    },
    {
     "text": "C is 5.",
     "expr": "5 + 2*x + 2*x**3 + 18*x**5/5",
     "relation": "evaluate",
     "subs": {
      "C": "5"
     }
    }
   ],
   "calculator_status": "no_calculator",
   "skills": [
    "BC-SKL-10069"
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
   "archetype_id": "BC-QA-10019",
   "parameter_draw": {
    "inner_power": 1,
    "sign": "plus",
    "count": 4,
    "scale": 2,
    "coefficient": 3,
    "start_value": -4
   },
   "stem": {
    "text": "Let \\(f'(x)=\\frac{3}{1+2x}\\) and \\(f(0)=-4\\). Use a geometric series to write the first four nonzero terms of the series for \\(f(x)\\).",
    "command_verb": "write"
   },
   "key": {
    "form": "symbolic",
    "expr": "-4 + 3*x - 3*x**2 + 4*x**3"
   },
   "steps": [
    {
     "text": "Series for \\(f'\\).",
     "expr": "3*(1 - 2*x + 4*x**2)",
     "relation": "new"
    },
    {
     "text": "Antidifferentiate.",
     "expr": "C + 3*x - 3*x**2 + 4*x**3",
     "relation": "integrate",
     "variable": "x"
    },
    {
     "text": "C is -4.",
     "expr": "-4 + 3*x - 3*x**2 + 4*x**3",
     "relation": "evaluate",
     "subs": {
      "C": "-4"
     }
    }
   ],
   "calculator_status": "no_calculator",
   "skills": [
    "BC-SKL-10069",
    "BC-SKL-10072"
   ]
  },
  {
   "id": "chk-3",
   "check_kind": "mcq",
   "format": "mcq",
   "bands": [
    "low"
   ],
   "archetype_id": "BC-QA-10019",
   "parameter_draw": {
    "inner_power": 2,
    "sign": "minus",
    "count": 4,
    "scale": 4,
    "coefficient": 3,
    "start_value": -2
   },
   "stem": {
    "text": "Let \\(f'(x)=\\frac{3}{1-4x^2}\\) and \\(f(0)=-2\\). The first four nonzero terms of the series for \\(f\\) are",
    "command_verb": "identify"
   },
   "key": {
    "form": "symbolic",
    "expr": "-2 + 3*x + 4*x**3 + 48*x**5/5"
   },
   "steps": [
    {
     "text": "Series for \\(f'\\).",
     "expr": "3 + 12*x**2 + 48*x**4",
     "relation": "new"
    },
    {
     "text": "Antidifferentiate.",
     "expr": "C + 3*x + 4*x**3 + 48*x**5/5",
     "relation": "integrate",
     "variable": "x"
    },
    {
     "text": "C is -2.",
     "expr": "-2 + 3*x + 4*x**3 + 48*x**5/5",
     "relation": "evaluate",
     "subs": {
      "C": "-2"
     }
    }
   ],
   "options": [
    {
     "id": "A",
     "is_key": false,
     "expr": "3*x + 4*x**3 + 48*x**5/5 + 192*x**7/7",
     "error_path": "BC-ERR-07026",
     "derivation": "no constant, so four antiderivative terms"
    },
    {
     "id": "B",
     "is_key": false,
     "expr": "-2 + 3*x + 12*x**3 + 48*x**5",
     "error_path": "BC-ERR-99018",
     "derivation": "each power raised and the coefficient left undivided"
    },
    {
     "id": "C",
     "is_key": true,
     "expr": "-2 + 3*x + 4*x**3 + 48*x**5/5",
     "error_path": null
    },
    {
     "id": "D",
     "is_key": false,
     "expr": "-2 + 3*x + 4*x**3 + 12*x**5/5",
     "error_path": "BC-ERR-10041",
     "derivation": "the 4 in the ratio not raised: 3 + 12x^2 + 12x^4"
    }
   ],
   "calculator_status": "no_calculator",
   "skills": [
    "BC-SKL-10069",
    "BC-SKL-10072"
   ]
  }
 ],
 "delivery": [
  {
   "block": "orientation",
   "mode": "text",
   "reason": "rule 5: a statement of what a response shows",
   "sources": [
    "BC-CON-10025"
   ]
  },
  {
   "block": "ki-1",
   "mode": "text",
   "reason": "rule 5: BC-REP-11, 01 on BC-SKL-10068, 10069, an operation on terms and not a process",
   "sources": [
    "BC-SKL-10068",
    "BC-SKL-10069"
   ]
  },
  {
   "block": "ki-2",
   "mode": "text",
   "reason": "rule 5: BC-REP-11, 01 on BC-SKL-10068, a stated radius",
   "sources": [
    "BC-SKL-10068"
   ]
  },
  {
   "block": "ki-3",
   "mode": "text",
   "reason": "rule 5: BC-REP-11, 01 on BC-SKL-10072",
   "sources": [
    "BC-SKL-10072"
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
   "block": "err-BC-ERR-07026",
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
   "block": "err-BC-ERR-10041",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  },
  {
   "block": "err-BC-ERR-99018",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  }
 ],
 "refresher": [
  "ki-1",
  "ki-2",
  "err-BC-ERR-07026",
  "err-BC-ERR-10005",
  "err-BC-ERR-10041",
  "err-BC-ERR-99018",
  "ex-1"
 ],
 "research_lines": [
  {
   "file": "research/units/unit-10-infinite-sequences-series.md",
   "line": "Term-by-term operations written on both the displayed terms and the general term, plus a constant of integration determined from a given value."
  }
 ],
 "inferred": [
  {
   "claim": "In BC-QA-10019's parameter_spec the sign label minus is read as a denominator 1 - k x^p and plus as 1 + k x^p; the spec's note does not say which.",
   "settles": "The generator template for BC-QA-10019 or a note in its parameter_spec."
  },
  {
   "claim": "BC-ERR-10005 and BC-ERR-10041 are shown on the integrand of ex-1's draw, which arrives from a geometric series and a substitution; BC-ERR-99018 is shown on ex-2's draw, as a coefficient not simplified after the power rule.",
   "settles": "A parameter_spec task on BC-QA-10019 that asks for the value of the integrand series at an input."
  },
  {
   "claim": "ex-1 tags nothing, because the BC-PT-99003 line (39 words) does not fit the brief cap beside the prediction and contrast pair; ex-2 tags the general term and the radius, and its first terms point (BC-PT-99037) is untagged to keep the full form under 900 words.",
   "settles": "A brief cap that admits more reader lines."
  },
  {
   "claim": "A fluent solver writes the integrand series, the antiderivative terms and the constant, and holds the recognition of the geometric form.",
   "settles": "Timing data per step once the fluency telemetry exists."
  }
 ],
 "sources": [
  "BC-CON-10025",
  "BC-SKL-10068",
  "BC-SKL-10069",
  "BC-SKL-10072",
  "BC-EK-LIM-8G1",
  "BC-EK-LIM-8D6",
  "BC-EK-LIM-8F1",
  "ced:187",
  "ced:198",
  "ced:199",
  "ced:200",
  "BC-QA-10019",
  "BC-QA-10018",
  "BC-QA-10003",
  "BC-PT-99003",
  "BC-PT-99037",
  "BC-PT-99038",
  "BC-PT-99047",
  "BC-ERR-07026",
  "BC-ERR-10005",
  "BC-ERR-10041",
  "BC-ERR-99018",
  "BC-MIS-10026",
  "BC-PRQ-06002",
  "BC-PRQ-06013",
  "BC-PRQ-10001",
  "BC-PRQ-10005",
  "BC-PRQ-10008",
  "research/units/unit-10-infinite-sequences-series.md#10.15 Representing Functions as Power Series",
  "research/question-analysis/question-archetypes.md#BC-QA-10019 Function represented by term-by-term integration of a known series",
  "research/question-analysis/question-archetypes.md#BC-QA-10018 Series differentiated term by term with its radius carried over",
  "research/question-analysis/question-archetypes.md#BC-QA-10003 Geometric series summed in closed form",
  "research/exam/exam-structure.md#Section and part layout"
 ],
 "word_count": {
  "full": 893,
  "brief": 449
 },
 "read_minutes": {
  "full": 6.0,
  "brief": 3.0
 }
}
```
