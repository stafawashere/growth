---
title: LSN-CON-02014 The quotient rule
research_date: 2026-09-29
status: designed
purpose: Authoring spec for the concept lesson on BC-CON-02014, the quotient rule, built from authoring_bundle("BC-CON-02014") and the research files it cites, so an author fills plan 15's lesson record without making a teaching decision.
---

# LSN-CON-02014 The quotient rule

Concept BC-CON-02014 (skills BC-SKL-02039, BC-SKL-02040, BC-SKL-02041, BC-SKL-02042), topic 2.9 of Unit 2, loaded by BC-QA-02008 (primary) and BC-QA-02009. The structure follows LSN-CON-02013, the product rule beside it.

## Prediction

Served first, both bands. On ex-1's function, \(h(x)=\frac{3x^2-2}{\sin x}\), with the piece derivatives \(6x\) and \(\cos x\) stated, the student picks \(h'(x)\): the two derivatives divided, the rule with the denominator's term first, or the rule with the numerator subtracted the other way round. Format `mcq`, key the rule with \(vu'\) first. The distractors are the error BC-ERR-02026 records and BC-ERR-02021. The resolution states \(\frac{vu'-uv'}{v^2}\) and that order matters, in the words of BC-EK-FUN-3B2 on ced:68. Sources: BC-CON-02014, BC-EK-FUN-3B2, ced:68 [verified].

## Orientation

Served text, from BC-CON-02014 `description_plain` and the topic's Assessment behaviour paragraph (research/units/unit-02-differentiation-definition-properties.md#2.9 The Quotient Rule): the rule's order and square, asked symbolically or from supplied values. No count, no frequency.

## Key ideas

One BC-EK maps to the four skills, BC-EK-FUN-3B2 (ced:68), so one core block, both bands.

- ki-1 (core). The rule, order matters, the square, and the constant denominator route, paraphrased from the Quotient rule, Order matters and Constant denominator paragraphs. Notation line: quotient rule. The anchor quote was dropped to bring the brief form under 450 words.

## Recognition

- BC-QA-02008 (family rule-manipulation, MCQ or one part, no calculator; research/question-analysis/question-archetypes.md#BC-QA-02008 Derivative of a product or a quotient by rule): `typical_wording` "Find the derivative of the given function."; `common_givens` a product or quotient of two differentiable expressions, a family of rational functions with a constant parameter, a stated tangent slope; `asked_to_produce` the derivative, or a parameter from a stated slope. The signal is a fraction bar with the variable below it. `official_examples`: BC-FRQ-2019-Q5-A, BC-FRQ-2014-Q3-C.
- BC-QA-02009 (family derivative-from-table; research/question-analysis/question-archetypes.md#BC-QA-02009 Derivative of a product or quotient evaluated from supplied values): four values at one input, two of them derivatives, and a quotient \(\frac{f}{g}\). `official_examples`: BC-FRQ-2021-Q4-B, BC-MCQ-CED-003.

The contrast pair on st-1 takes its near miss from outside this concept, from the product rule (BC-CON-02013). `this` is a polynomial over a cosine on BC-QA-02008 (a different draw from every published item). `not_this` multiplies the same two factors, \((x^3+4)\cos x\), which calls for the product rule (SymPy: \(3x^2\cos x-(x^3+4)\sin x\)); the feature is a variable in the denominator. A constant denominator was not used, since that is a BC-QA-02008 stem inside this concept (BC-SKL-02042), where the quotient rule still gives the right derivative.

What says "not this concept": a constant denominator (constant multiple rule, BC-SKL-02042, BC-ERR-02023); two factors multiplied (BC-CON-02013); tan, cot, sec or csc, which BC-CON-02015 rewrites first.

## Method choice

Two strategy blocks, low and mid bands, the first only in mid.

- st-1, BC-QA-02008. Method, `expected_solution_path[0]`: identify the two pieces and their derivatives, written as \(u\), \(v\), \(u'\), \(v'\), then the rule; the served text carries no leading label. Rival, `wrong_approaches`: numerator and denominator differentiated separately (BC-ERR-02026). Separating feature: a variable denominator.
- st-2, BC-QA-02009. Method, `expected_solution_path[0]`: record the four values. Rival, `wrong_approaches`: a function value in a derivative position (BC-ERR-02024). Separating feature: each number labelled first.

## Solution path

- ex-1, BC-QA-02008, both bands, no calculator. Draw: numerator quadratic, leading 3, constant \(-2\), trig sin, angle 1/4: \(h(x)=\frac{3x^2-2}{\sin x}\) at \(\frac{\pi}{4}\). Steps: identify pieces (no value), rule line (tagged BC-PT-99080), value \(\sqrt2(\frac{3\pi}{2}-\frac{3\pi^2}{16}+2)\). A fluent solver writes the rule line and the value.
- ex-2, BC-QA-02009, low band. Draw row 1 of the table: \(f(1)=-3\), \(f'(1)=5\), \(g(1)=2\), \(g'(1)=-2\), form quotient. Steps: label the values (no value), the substituted rule, the value 1 (tagged BC-PT-99004). Key 1. ex-2 is faded from step 3: steps 1 and 2 are shown, the student writes the value, and then the arithmetic step is revealed. The fade falls there because step 2 is the valued rule line and step 3 is the arithmetic the student can produce from it.

No productive-failure opener targets this concept, so no comparison callout.

## Scoring

BC-QA-02008 lists BC-PT-99080 and ex-1 tags it on the rule line; BC-QA-02009 lists BC-PT-99004 (not 99080) and ex-2 tags it on the value. One line each, generated by `reader_checks` and copied into the machine record:

Quotient rule applied to a ratio of two functions. Earned by: A derivative of a ratio presented with the denominator's derivative subtracted in the numerator and the denominator squared, whether the ratio is built from named functions or from an explicit expression. samples-14-q3:1 awards two of the three points in the part to this derivative expression before any value is substituted. sg-25:21 states that a response correctly applying the quotient rule, together with the chain rule, to a separated solution earns the corresponding structure points. Not earned by: A numerator difference written in the wrong order, an unsquared denominator, or a derivative formed as the ratio of the two derivatives. sg-25:21 states that a response applying the quotient rule but not the chain rule does not earn the second structure point.

Answer with or without supporting work. Earned by: The correct value on its own, with no supporting work required (sg-25:3, sg-26:4). Not earned by: A value outside the accepted precision, or a value inconsistent with a required earlier step where the rubric imposes one. Precision: A reported decimal answer must be accurate to three places after the decimal point, rounded or truncated; at most one point per question is lost to inappropriate rounding (sg-25:2, sg-26:2). sg-26:4 also accepts a stated rounding to the nearest integer and several truncations.

Point losses the scoring research names for rule shapes: simplification is optional but an attempted simplification must be correct (research/scoring/notation-requirements.md#Simplification, sg-23:16), and an unrequired simplification that introduces an error loses the answer point (research/scoring/common-point-losses.md#Answer points, BC-ERR-99022). BC-PT-99005, 99022 and 99069 are not tagged.

## Traps

Five active errors meet the concept's skills; the cap is 4, so the first four in the bundle's order are served (BC-ERR-02026 is served in LSN-CON-02015, where the rewritten trigonometric quotient carries it). Low band all four, mid band the first two.

- err-BC-ERR-02021 (BC-MIS-02012): numerator reversed on ex-1. Distinct, `fix_prompt` true.
- err-BC-ERR-02022 (BC-MIS-02012): \(\sin x\) below the line, not \(\sin^2x\). Distinct, `fix_prompt` true.
- err-BC-ERR-02023: the full rule on \(\frac{3x^2-2}{5}\) against \(\frac{6x}{5}\). Equivalent, which is the record's own consequence; `fix_prompt` false.
- err-BC-ERR-02024 (BC-MIS-02011): on ex-2, \(f(1)\) for \(f'(1)\) gives \(-3\) against 1. Distinct, `fix_prompt` true.

## Representations

None. The topic names BC-REP-03 and BC-REP-02 through supplied values, which ex-2 carries as values written in its problem. BC-REP-02 is carried by the ki-1 graph (Delivery).

## Prerequisite bridge

None. The bundle lists no BC-PRQ parent of BC-SKL-02039 to 02042.

## Time

Both archetypes are `no_calculator` and MCQ-shaped, so the part is Section I Part A, 2.14 minutes per question (research/exam/exam-structure.md#Section and part layout; plan 15, Fluency). A fluent solver writes the rule line and the value on each example and holds the piece identification and value labelling in the head. The rule line is written even under time pressure because it carries BC-PT-99080.

## Checks

- chk-1, completion of ex-1, both bands: rule line given, value found. Key equals ex-1's answer.
- chk-2, isomorph on BC-QA-02008, both bands: \(\frac{2x+5}{\cos x}\) at \(\frac{\pi}{3}\). Key \(4+2\sqrt3(\frac{2\pi}{3}+5)\).
- chk-3, MCQ on BC-QA-02009, low band: \(f(3)=-2\), \(f'(3)=5\), \(g(3)=3\), \(g'(3)=-4\). Key \(\frac79\). Distractors \(-\frac79\) (BC-ERR-02021), \(\frac73\) (BC-ERR-02022), \(-\frac{14}{9}\) (BC-ERR-02024), the three positions of the spec's `options`.

No draw equals a published BC-QA-02008 or BC-QA-02009 `parameter_draw`.

## Delivery

- orientation: text. Rule 5, BC-REP-01; unit README delivery map.
- ki-1: figure. Rule 4, BC-REP-02 on BC-SKL-02041, which the selection order puts ahead of rule 5: the graph of \(h(x)=\frac{x^2}{x+1}\), with \(f(x)=x^2\) and \(g(x)=x+1\), and its tangent at \(x=1\), slope \(\frac{f'g-fg'}{g^2}=\frac{4-1}{4}=\frac34\), beside the dashed line of slope \(\frac{f'}{g'}=2\) through \((1,\frac12)\), which is not tangent (SymPy: \(h'(1)=\frac34\), tangent \(y=\frac34x-\frac14\), dashed line \(y=2x-\frac32\)). The figure puts the prediction's claim on a graph; every label sits inside it. Fallback alt text naming both slopes, keyboard none needed [inferred; settled by the modality A/B].
- ex-1: step_reveal. Rule 1.
- ex-2: step_reveal with the supplied values written in the problem text. Rule 1.
- err-BC-ERR-02021, err-BC-ERR-02022, err-BC-ERR-02023, err-BC-ERR-02024: step_reveal. Rule 1.

No motion, interactive or model mode applies: the concept has no parameter that varies and no process to watch [inferred; settled by the modality A/B].

## Band plan

- Low (full): prediction, orientation, ki-1, st-1 with its contrast pair, st-2, ex-1 with its scoring line, chk-1, the four error blocks, ex-2 faded from step 3 with its scoring line, chk-2, chk-3. 720 words, 4.8 minutes (cap 900 and 6).
- Mid (brief): prediction, orientation, ki-1, st-1 with its contrast pair, ex-1 with its scoring line, chk-1, err-BC-ERR-02021, err-BC-ERR-02022, chk-2. 442 words, 3.0 minutes (cap 450 and 3).
- Refresher: ki-1, err-BC-ERR-02021, err-BC-ERR-02022, err-BC-ERR-02023, err-BC-ERR-02024, ex-1.

## Sources

- BC-CON-02014; BC-SKL-02039, BC-SKL-02040, BC-SKL-02041, BC-SKL-02042; BC-EK-FUN-3B2; ced:68
- BC-QA-02008, BC-QA-02009; BC-FRQ-2019-Q5-A, BC-FRQ-2014-Q3-C, BC-FRQ-2021-Q4-B, BC-MCQ-CED-003
- BC-PT-99080, BC-PT-99004; sg-25:21, sg-23:16, sg-25:3, sg-26:4, sg-25:2, sg-26:2
- BC-ERR-02021, BC-ERR-02022, BC-ERR-02023, BC-ERR-02024, BC-ERR-02026; BC-MIS-02011, BC-MIS-02012; BC-ERR-99022
- research/units/unit-02-differentiation-definition-properties.md#2.9 The Quotient Rule
- research/question-analysis/question-archetypes.md#BC-QA-02008 Derivative of a product or a quotient by rule
- research/question-analysis/question-archetypes.md#BC-QA-02009 Derivative of a product or quotient evaluated from supplied values
- research/scoring/notation-requirements.md#Simplification
- research/scoring/common-point-losses.md#Answer points
- research/exam/exam-structure.md#Section and part layout
- [inferred] The ki-1 graph as the drawn block, and no motion, interactive or model mode. Settled by the modality A/B.

## Machine record

```json
{
 "id": "LSN-CON-02014",
 "kind": "concept",
 "target_id": "BC-CON-02014",
 "unit": "02",
 "skills": [
  "BC-SKL-02039",
  "BC-SKL-02040",
  "BC-SKL-02041",
  "BC-SKL-02042"
 ],
 "prediction": {
  "id": "pr-1",
  "stem": {
   "text": "Predict before the rule. For \\(h(x)=\\frac{3x^2-2}{\\sin x}\\), the pieces have derivatives \\(6x\\) and \\(\\cos x\\). Which expression is \\(h'(x)\\)?",
   "command_verb": "predict"
  },
  "format": "mcq",
  "options": [
   {
    "id": "A",
    "label": "\\(\\frac{6x}{\\cos x}\\), the two derivatives divided",
    "is_key": false
   },
   {
    "id": "B",
    "label": "\\(\\frac{6x\\sin x-(3x^2-2)\\cos x}{\\sin^2x}\\)",
    "is_key": true
   },
   {
    "id": "C",
    "label": "\\(\\frac{(3x^2-2)\\cos x-6x\\sin x}{\\sin^2x}\\)",
    "is_key": false
   }
  ],
  "resolution": "The quotient rule is \\(\\frac{vu'-uv'}{v^2}\\): the denominator times the numerator's derivative, minus the numerator times the denominator's derivative, over the denominator squared. The order of the subtraction matters.",
  "sources": [
   "BC-CON-02014",
   "BC-EK-FUN-3B2",
   "ced:68"
  ]
 },
 "orientation": {
  "text": "A response differentiates a quotient as the denominator times the numerator's derivative, minus the numerator times the denominator's derivative, over the denominator squared. Questions ask for it symbolically or from supplied values.",
  "sources": [
   "BC-CON-02014",
   "research/units/unit-02-differentiation-definition-properties.md#2.9 The Quotient Rule"
  ]
 },
 "key_ideas": [
  {
   "id": "ki-1",
   "ek_id": "BC-EK-FUN-3B2",
   "depth": "core",
   "text": "For \\(\\frac{u}{v}\\) the derivative is \\(\\frac{vu'-uv'}{v^2}\\). Order matters: reversing the numerator terms flips the sign of the whole derivative. The denominator is squared. When the denominator carries no variable, the constant multiple rule is shorter.",
   "notation": "quotient rule",
   "quote": null,
   "sources": [
    "BC-EK-FUN-3B2",
    "ced:68",
    "research/units/unit-02-differentiation-definition-properties.md#2.9 The Quotient Rule"
   ]
  }
 ],
 "strategy": [
  {
   "id": "st-1",
   "archetype_id": "BC-QA-02008",
   "cue": "The stem asks for the derivative of a quotient of two differentiable expressions.",
   "method": "\\(u\\), \\(v\\), \\(u'\\), \\(v'\\), then \\(\\frac{vu'-uv'}{v^2}\\).",
   "rival": "The rival is differentiating numerator and denominator separately.",
   "separating_feature": "A variable denominator: its derivative enters the numerator, subtracted second.",
   "sources": [
    "BC-QA-02008"
   ],
   "evidence_tag": "verified",
   "contrast": {
    "this": {
     "text": "Let \\(k(x)=\\frac{x^3+4}{\\cos x}\\). Find \\(k'(x)\\).",
     "archetype_id": "BC-QA-02008"
    },
    "not_this": {
     "text": "Let \\(m(x)=(x^3+4)\\cos x\\). Find \\(m'(x)\\).",
     "why_not": "The cosine multiplies the polynomial, so the product rule applies, not the quotient rule."
    },
    "feature": "A variable in the denominator."
   }
  },
  {
   "id": "st-2",
   "archetype_id": "BC-QA-02009",
   "cue": "The stem asks for the derivative value at a named input, from a table of two functions and their derivatives.",
   "method": "The four values at the input, each labelled a value or a derivative.",
   "rival": "The rival is placing a function value where the rule calls for a derivative value.",
   "separating_feature": "Each number is labelled before it is placed.",
   "sources": [
    "BC-QA-02009"
   ],
   "evidence_tag": "verified"
  }
 ],
 "worked_examples": [
  {
   "id": "ex-1",
   "archetype_id": "BC-QA-02008",
   "bands": [
    "low",
    "mid"
   ],
   "parameter_draw": {
    "numerator": "quadratic",
    "leading": "3",
    "constant": "-2",
    "trig": "sin",
    "angle": "1/4"
   },
   "problem": {
    "text": "Let \\(h(x)=\\frac{3x^2-2}{\\sin x}\\). Find \\(h'(\\frac{\\pi}{4})\\).",
    "command_verb": "find"
   },
   "calculator_status": "no_calculator",
   "steps": [
    {
     "cue": "A variable denominator: \\(u=3x^2-2\\), \\(v=\\sin x\\).",
     "why": "\\(u'=6x\\), \\(v'=\\cos x\\)."
    },
    {
     "cue": "Quotient: \\(\\frac{vu'-uv'}{v^2}\\), \\(v\\) first.",
     "why": "Denominator times \\(u'\\), minus numerator times \\(v'\\), over \\(v^2\\).",
     "expr": "(6*x*sin(x)-(3*x**2-2)*cos(x))/sin(x)**2",
     "relation": "new",
     "point_type_id": "BC-PT-99080"
    },
    {
     "cue": "The stem names \\(\\frac{\\pi}{4}\\).",
     "why": "\\(\\sin=\\cos=\\frac{\\sqrt2}{2}\\), \\(v^2=\\frac12\\).",
     "expr": "sqrt(2)*(3*pi/2-3*pi**2/16+2)",
     "relation": "evaluate",
     "subs": {
      "x": "pi/4"
     }
    }
   ],
   "answer": {
    "form": "symbolic",
    "expr": "sqrt(2)*(3*pi/2-3*pi**2/16+2)"
   }
  },
  {
   "id": "ex-2",
   "archetype_id": "BC-QA-02009",
   "bands": [
    "low"
   ],
   "parameter_draw": {
    "f_values": [
     "2",
     "-3",
     "4"
    ],
    "f_slopes": [
     "-1",
     "5",
     "2"
    ],
    "g_values": [
     "3",
     "2",
     "-1"
    ],
    "g_slopes": [
     "4",
     "-2",
     "1"
    ],
    "row": "1",
    "start": "0",
    "form": "quotient"
   },
   "problem": {
    "text": "Suppose \\(f(1)=-3\\), \\(f'(1)=5\\), \\(g(1)=2\\), \\(g'(1)=-2\\). Let \\(h(x)=\\frac{f(x)}{g(x)}\\). Find \\(h'(1)\\).",
    "command_verb": "find"
   },
   "calculator_status": "no_calculator",
   "steps": [
    {
     "cue": "Four values at 1, two of them derivatives.",
     "why": "Label each before use."
    },
    {
     "cue": "\\(h\\) is a quotient: \\(\\frac{g(1)f'(1)-f(1)g'(1)}{g(1)^2}\\).",
     "why": "Each numerator term holds one derivative value.",
     "expr": "(2*5-(-3)*(-2))/2**2",
     "relation": "new"
    },
    {
     "cue": "The stem asks for a value.",
     "why": "Arithmetic on the substituted line.",
     "expr": "1",
     "relation": "equivalent",
     "point_type_id": "BC-PT-99004"
    }
   ],
   "answer": {
    "form": "numeric",
    "expr": "1"
   },
   "fade_from": 3
  }
 ],
 "what_a_reader_scores": [
  {
   "example_id": "ex-1",
   "point_type_ids": [
    "BC-PT-99080"
   ],
   "lines": [
    {
     "point_type_id": "BC-PT-99080",
     "text": "Quotient rule applied to a ratio of two functions. Earned by: A derivative of a ratio presented with the denominator's derivative subtracted in the numerator and the denominator squared, whether the ratio is built from named functions or from an explicit expression. samples-14-q3:1 awards two of the three points in the part to this derivative expression before any value is substituted. sg-25:21 states that a response correctly applying the quotient rule, together with the chain rule, to a separated solution earns the corresponding structure points. Not earned by: A numerator difference written in the wrong order, an unsquared denominator, or a derivative formed as the ratio of the two derivatives. sg-25:21 states that a response applying the quotient rule but not the chain rule does not earn the second structure point."
    }
   ]
  },
  {
   "example_id": "ex-2",
   "point_type_ids": [
    "BC-PT-99004"
   ],
   "lines": [
    {
     "point_type_id": "BC-PT-99004",
     "text": "Answer with or without supporting work. Earned by: The correct value on its own, with no supporting work required (sg-25:3, sg-26:4). Not earned by: A value outside the accepted precision, or a value inconsistent with a required earlier step where the rubric imposes one. Precision: A reported decimal answer must be accurate to three places after the decimal point, rounded or truncated; at most one point per question is lost to inappropriate rounding (sg-25:2, sg-26:2). sg-26:4 also accepts a stated rounding to the nearest integer and several truncations."
    }
   ]
  }
 ],
 "common_errors": [
  {
   "error_id": "BC-ERR-02021",
   "observed_behavior": "The response subtracts in the opposite order in the numerator of the quotient rule.",
   "scoring_consequence": "The result point is lost because the derivative carries the wrong sign.",
   "wrong_step": {
    "text": "\\(\\frac{(3x^2-2)\\cos x-6x\\sin x}{\\sin^2x}\\).",
    "expr": "((3*x**2-2)*cos(x)-6*x*sin(x))/sin(x)**2"
   },
   "right_step": {
    "text": "\\(\\frac{6x\\sin x-(3x^2-2)\\cos x}{\\sin^2x}\\).",
    "expr": "(6*x*sin(x)-(3*x**2-2)*cos(x))/sin(x)**2"
   },
   "relation": "distinct",
   "possible_reason": {
    "misconception_id": "BC-MIS-02012",
    "text": "the two numerator terms as interchangeable"
   },
   "sources": [
    "BC-ERR-02021",
    "BC-MIS-02012"
   ],
   "fix_prompt": true
  },
  {
   "error_id": "BC-ERR-02022",
   "observed_behavior": "The response writes the quotient rule with the denominator rather than its square below the line.",
   "scoring_consequence": "The result point is lost.",
   "wrong_step": {
    "text": "Below the line: \\(\\sin x\\).",
    "expr": "(6*x*sin(x)-(3*x**2-2)*cos(x))/sin(x)"
   },
   "right_step": {
    "text": "Below the line: \\(\\sin^2x\\).",
    "expr": "(6*x*sin(x)-(3*x**2-2)*cos(x))/sin(x)**2"
   },
   "relation": "distinct",
   "possible_reason": {
    "misconception_id": "BC-MIS-02012",
    "text": "the denominator as carrying no square"
   },
   "sources": [
    "BC-ERR-02022",
    "BC-MIS-02012"
   ],
   "fix_prompt": true
  },
  {
   "error_id": "BC-ERR-02023",
   "observed_behavior": "The response applies the full quotient rule to an expression whose denominator carries no variable.",
   "scoring_consequence": "No point is necessarily lost but the additional algebra invites a further error.",
   "wrong_step": {
    "text": "The full rule on \\(\\frac{3x^2-2}{5}\\).",
    "expr": "(6*x*5-(3*x**2-2)*0)/5**2"
   },
   "right_step": {
    "text": "Constant denominator: \\(\\frac{6x}{5}\\).",
    "expr": "6*x/5"
   },
   "relation": "equivalent",
   "possible_reason": null,
   "sources": [
    "BC-ERR-02023"
   ],
   "fix_prompt": false
  },
  {
   "error_id": "BC-ERR-02024",
   "observed_behavior": "The response substitutes the value of a function into a position in the product or quotient rule that calls for the value of its derivative.",
   "scoring_consequence": "The value point is lost.",
   "wrong_step": {
    "text": "On ex-2, \\(f(1)\\) for \\(f'(1)\\): \\(\\frac{2(-3)-(-3)(-2)}{4}=-3\\).",
    "expr": "(2*(-3)-(-3)*(-2))/2**2"
   },
   "right_step": {
    "text": "\\(\\frac{2(5)-(-3)(-2)}{4}=1\\).",
    "expr": "(2*5-(-3)*(-2))/2**2"
   },
   "relation": "distinct",
   "possible_reason": {
    "misconception_id": "BC-MIS-02011",
    "text": "supplied values are placed in the wrong positions"
   },
   "sources": [
    "BC-ERR-02024",
    "BC-MIS-02011"
   ],
   "fix_prompt": true
  }
 ],
 "representations": null,
 "prerequisite_bridges": [],
 "time": {
  "exam_part": "I-A",
  "budget_minutes": 2.14,
  "source": "research/exam/exam-structure.md#Section and part layout",
  "written_steps": {
   "ex-1": [
    2,
    3
   ],
   "ex-2": [
    2,
    3
   ]
  },
  "skipped_steps": {
   "ex-1": [
    1
   ],
   "ex-2": [
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
   "archetype_id": "BC-QA-02008",
   "parameter_draw": {
    "numerator": "quadratic",
    "leading": "3",
    "constant": "-2",
    "trig": "sin",
    "angle": "1/4"
   },
   "completes": "ex-1",
   "stem": {
    "text": "\\(h'(x)=\\frac{6x\\sin x-(3x^2-2)\\cos x}{\\sin^2x}\\). Find \\(h'(\\frac{\\pi}{4})\\).",
    "command_verb": "find"
   },
   "key": {
    "form": "symbolic",
    "expr": "sqrt(2)*(3*pi/2-3*pi**2/16+2)"
   },
   "steps": [
    {
     "text": "The rule line.",
     "expr": "(6*x*sin(x)-(3*x**2-2)*cos(x))/sin(x)**2",
     "relation": "new",
     "point_type_id": "BC-PT-99080"
    },
    {
     "text": "At \\(\\frac{\\pi}{4}\\).",
     "expr": "sqrt(2)*(3*pi/2-3*pi**2/16+2)",
     "relation": "evaluate",
     "subs": {
      "x": "pi/4"
     }
    }
   ],
   "calculator_status": "no_calculator",
   "skills": [
    "BC-SKL-02039"
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
   "archetype_id": "BC-QA-02008",
   "parameter_draw": {
    "numerator": "linear",
    "leading": "2",
    "constant": "5",
    "trig": "cos",
    "angle": "1/3"
   },
   "stem": {
    "text": "Let \\(h(x)=\\frac{2x+5}{\\cos x}\\). Find \\(h'(\\frac{\\pi}{3})\\).",
    "command_verb": "find"
   },
   "key": {
    "form": "symbolic",
    "expr": "4+2*sqrt(3)*(2*pi/3+5)"
   },
   "steps": [
    {
     "text": "The rule line.",
     "expr": "(2*cos(x)+(2*x+5)*sin(x))/cos(x)**2",
     "relation": "new",
     "point_type_id": "BC-PT-99080"
    },
    {
     "text": "At \\(\\frac{\\pi}{3}\\).",
     "expr": "4+2*sqrt(3)*(2*pi/3+5)",
     "relation": "evaluate",
     "subs": {
      "x": "pi/3"
     }
    }
   ],
   "calculator_status": "no_calculator",
   "skills": [
    "BC-SKL-02039"
   ]
  },
  {
   "id": "chk-3",
   "check_kind": "mcq",
   "format": "mcq",
   "bands": [
    "low"
   ],
   "archetype_id": "BC-QA-02009",
   "parameter_draw": {
    "f_values": [
     "1",
     "4",
     "-2"
    ],
    "f_slopes": [
     "3",
     "-2",
     "5"
    ],
    "g_values": [
     "-1",
     "2",
     "3"
    ],
    "g_slopes": [
     "2",
     "3",
     "-4"
    ],
    "row": "2",
    "start": "1",
    "form": "quotient"
   },
   "stem": {
    "text": "Suppose \\(f(3)=-2\\), \\(f'(3)=5\\), \\(g(3)=3\\), \\(g'(3)=-4\\) and \\(h(x)=\\frac{f(x)}{g(x)}\\). Find \\(h'(3)\\).",
    "command_verb": "find"
   },
   "key": {
    "form": "numeric",
    "expr": "7/9"
   },
   "steps": [
    {
     "text": "The rule with values.",
     "expr": "(3*5-(-2)*(-4))/3**2",
     "relation": "new"
    },
    {
     "text": "That is \\(\\frac79\\).",
     "expr": "7/9",
     "relation": "equivalent"
    }
   ],
   "options": [
    {
     "id": "A",
     "is_key": false,
     "expr": "-7/9",
     "error_path": "BC-ERR-02021",
     "derivation": "numerator terms reversed"
    },
    {
     "id": "B",
     "is_key": true,
     "expr": "7/9",
     "error_path": null
    },
    {
     "id": "C",
     "is_key": false,
     "expr": "7/3",
     "error_path": "BC-ERR-02022",
     "derivation": "denominator g(3) not squared"
    },
    {
     "id": "D",
     "is_key": false,
     "expr": "-14/9",
     "error_path": "BC-ERR-02024",
     "derivation": "f(3) used in place of f'(3): (3(-2) - (-2)(-4))/9"
    }
   ],
   "calculator_status": "no_calculator",
   "skills": [
    "BC-SKL-02041"
   ]
  }
 ],
 "delivery": [
  {
   "block": "orientation",
   "mode": "text",
   "reason": "rule 5: BC-REP-01 on BC-SKL-02039; unit README delivery map",
   "sources": [
    "BC-SKL-02039"
   ]
  },
  {
   "block": "ki-1",
   "mode": "figure",
   "reason": "rule 4: BC-REP-02 on BC-SKL-02041, ahead of rule 5; the quotient of x^2 by x + 1 graphed with its tangent at x = 1 beside the line whose slope is the quotient of the derivatives",
   "sources": [
    "BC-SKL-02041"
   ],
   "spec": {
    "kind": "graph",
    "window": {
     "x": [
      0,
      2
     ],
     "y": [
      -1.5,
      2.5
     ]
    },
    "curves": [
     {
      "expr": "x**2/(x + 1)",
      "style": "solid",
      "label": {
       "text": "h(x) = x^2 over (x + 1)",
       "placement": "inside"
      }
     },
     {
      "expr": "3*x/4 - 1/4",
      "style": "solid",
      "label": {
       "text": "tangent, slope (f'g - fg')/g^2 = 3/4",
       "placement": "inside"
      }
     },
     {
      "expr": "2*x - 3/2",
      "style": "dashed",
      "label": {
       "text": "slope f'/g' = 2, not the tangent",
       "placement": "inside"
      }
     }
    ],
    "points": [
     {
      "x": 1,
      "y": 0.5,
      "style": "closed",
      "label": {
       "text": "(1, 1/2)",
       "placement": "inside"
      }
     }
    ],
    "labels": [],
    "representations": [
     "BC-REP-02"
    ]
   },
   "fallback": "Alt text: the graph of \\(h(x)=\\frac{x^2}{x+1}\\), with \\(f(x)=x^2\\) and \\(g(x)=x+1\\), through \\((1,\\frac12)\\). The tangent there has slope \\(\\frac{f'(1)g(1)-f(1)g'(1)}{g(1)^2}=\\frac34\\); the dashed line of slope \\(\\frac{f'(1)}{g'(1)}=2\\) through the same point is not tangent.",
   "keyboard": "none needed: a static figure"
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
   "reason": "rule 1; the four supplied values are written in the problem text",
   "sources": [
    "BC-SKL-02041"
   ]
  },
  {
   "block": "err-BC-ERR-02021",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  },
  {
   "block": "err-BC-ERR-02022",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  },
  {
   "block": "err-BC-ERR-02023",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  },
  {
   "block": "err-BC-ERR-02024",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  }
 ],
 "refresher": [
  "ki-1",
  "err-BC-ERR-02021",
  "err-BC-ERR-02022",
  "err-BC-ERR-02023",
  "err-BC-ERR-02024",
  "ex-1"
 ],
 "read_minutes": {
  "full": 4.8,
  "brief": 3.0
 },
 "word_count": {
  "full": 720,
  "brief": 442
 },
 "research_lines": [
  {
   "file": "research/scoring/notation-requirements.md",
   "line": "simplification is optional, but attempted simplification must be correct"
  }
 ],
 "inferred": [
  {
   "claim": "The graph on ki-1 serves the concept better than text alone, and no motion, interactive or model mode serves it better than that.",
   "settles": "The modality A/B in the build plan: skip rate and time to first credited success by mode."
  }
 ],
 "sources": [
  "BC-CON-02014",
  "BC-SKL-02039",
  "BC-SKL-02040",
  "BC-SKL-02041",
  "BC-SKL-02042",
  "BC-EK-FUN-3B2",
  "ced:68",
  "BC-QA-02008",
  "BC-QA-02009",
  "BC-PT-99080",
  "BC-PT-99004",
  "sg-25:21",
  "sg-25:3",
  "sg-26:4",
  "sg-25:2",
  "sg-26:2",
  "BC-FRQ-2019-Q5-A",
  "BC-FRQ-2014-Q3-C",
  "BC-FRQ-2021-Q4-B",
  "BC-MCQ-CED-003",
  "BC-ERR-02021",
  "BC-ERR-02022",
  "BC-ERR-02023",
  "BC-ERR-02024",
  "BC-ERR-02026",
  "BC-MIS-02011",
  "BC-MIS-02012",
  "BC-ERR-99022",
  "sg-23:16",
  "research/units/unit-02-differentiation-definition-properties.md#2.9 The Quotient Rule",
  "research/question-analysis/question-archetypes.md#BC-QA-02008 Derivative of a product or a quotient by rule",
  "research/question-analysis/question-archetypes.md#BC-QA-02009 Derivative of a product or quotient evaluated from supplied values",
  "research/scoring/notation-requirements.md#Simplification",
  "research/scoring/common-point-losses.md#Answer points",
  "research/exam/exam-structure.md#Section and part layout"
 ]
}
```
