---
title: LSN-CON-06018 Linear partial fractions
research_date: 2026-09-29
status: designed
purpose: Authoring spec for the concept lesson on BC-CON-06018, antiderivatives of rational functions over distinct linear factors by partial fractions, built from authoring_bundle("BC-CON-06018") and the research files it cites.
---

# LSN-CON-06018 Linear partial fractions

Concept BC-CON-06018 (skills BC-SKL-06062 to BC-SKL-06065), topic 6.12 of Unit 6, loaded by one archetype, BC-QA-06010 (family antidifferentiation-technique). Its hard parents are BC-CON-06012 and BC-CON-06015 (docs/lessons/unit-06/README.md, section 1).

## Prediction

One multiple choice question on worked example 1's own integrand, \(\frac{7}{2x^2-5x-3}\) with the factored denominator given, asked before the rule is shown: which sum of simple fractions equals it. The key is \(-\frac{2}{2x+1}+\frac{1}{x-3}\), ex-1's third valued step. The distractors keep the numerator 7 over each factor, and swap the two constants. The resolution, shown beside the choice on the key idea screen, states that each factor takes one constant numerator, what clearing denominators gives and that each term integrates to a logarithm, with no verdict word. Sources: BC-CON-06018 and the topic 6.12 section the key idea cites [inferred].

## Orientation

Served text (14 words), from BC-CON-06018 `description_plain` and the topic's Assessment behaviour paragraph (research/units/unit-06-integration-accumulation.md#6.12 Integrating Using Linear Partial Fractions): a response factors, finds the numerators and writes logarithms. No count, no frequency.

## Key ideas

All four skills map to BC-EK-FUN-6F1, so one core block, both bands.

- ki-1 (core), BC-EK-FUN-6F1, ced:129. Paraphrase of the Decomposition and Procedure paragraphs of Required mathematical knowledge. No quote: the EK sentence on ced:129 is 21 words and the brief band has no room. Notation line from the concept record.

## Recognition

BC-QA-06010 (research/question-analysis/question-archetypes.md#BC-QA-06010 Antiderivative by linear partial fractions). `typical_wording`: "find the indefinite integral of the given rational expression by decomposing it into partial fractions". `common_givens`: a rational function whose quadratic denominator factors into distinct linear factors, a family of functions with the parameter fixed at a stated value, the limits of integration. `asked_to_produce`: a partial fraction decomposition, logarithmic antiderivatives, the value of a definite integral. Official examples: BC-FRQ-2019-Q5-B, BC-FRQ-2015-Q5-D, BC-MCQ-PE2012-020.

The signal: a constant or linear numerator over a quadratic that factors into two distinct linears. Contrast pair on st-1: the this stem is on BC-QA-06010, a constant over a quadratic that factors into distinct linears; the not this stem has the same denominator with the numerator 4x + 7, its derivative, the near miss from BC-QA-06008 (substitution, the archetype BC-ERR-06019 in the bundle carries), where u is the denominator and the antiderivative is ln|2x^2 + 7x + 3| + C. The separating feature is a numerator that is not the denominator's derivative. The rival, decomposing without dividing (BC-ERR-06026), stays on st-1 and on its error block.

What says "not this concept": the numerator is a multiple of the denominator's derivative (substitution to one logarithm, BC-CON-06015); numerator degree at least the denominator's (divide first, BC-CON-06016); a quadratic that does not factor (complete the square, BC-CON-06016).

## Method choice

One strategy block, both bands.

- st-1, BC-QA-06010. Cue from `common_givens` and `asked_to_produce`. Method, `expected_solution_path[0]`: factor the denominator. Rival from `wrong_approaches`: decomposing an improper rational integrand without dividing first, cited in the block's `sources` (BC-ERR-06026), not in its text. Separating feature: the degree comparison. First written line: the factored denominator.

## Solution path

- There is no example 2, so nothing is faded and there is no `fade_from`.
- ex-1, BC-QA-06010, both bands, no calculator. Draw from `parameter_spec`: degree proper, leading 2, first_shift 1, second_shift -3, weight -1; derived numerator_constant 7, integrand 7/((2x + 1)(x - 3)), decomposition -2/(2x + 1) + 1/(x - 3). No published BC-QA-06010 item carries this draw.
- Steps follow `expected_solution_path`: factor (no value); the integrand (new); the decomposition (equivalent); the logarithms (integrate, BC-PT-99003); the reported form (equivalent, BC-PT-99004). SymPy strings drop the absolute value bars that the served text keeps [inferred].

A fluent solver writes the factored denominator, the constants and the logarithms; clearing denominators is held in the head (unit README section 5) [inferred].

## Scoring

BC-QA-06010 lists BC-PT-99005, BC-PT-99003, BC-PT-99004 and BC-PT-99081. ex-1 tags BC-PT-99003 on the antiderivative and BC-PT-99004 on the reported answer; reader lines are `reader_checks` output copied exactly. BC-PT-99081 (the decomposition) is not tagged, to keep the brief band under 450 words [inferred]; BC-PT-99005 is the answer-with-setup variant, not needed on an indefinite answer. `scoring_pattern` records the point structure as inferred from the technique parts of 2023 to 2025, where setup and antiderivative carry separate points and the value depends on the antiderivative (research/scoring/common-point-losses.md#Answer points).

## Traps

All four active errors meeting the skills, in the bundle's order: BC-ERR-06019, BC-ERR-06022, BC-ERR-06026, BC-ERR-07030. Mid band shows the first two. All four wrong steps differ from the right step as expressions, so each block is a fix prompt (`fix_prompt` true).

- err-BC-ERR-06019: -2 ln|2x + 1|, the 1/2 from the factor's leading coefficient dropped. Possible reason, words from BC-MIS-06016.
- err-BC-ERR-06022: 7 times the logarithms of the two factors multiplied. Possible reason, words from BC-MIS-06019.
- err-BC-ERR-06026: on the improper form of the draw, the fraction split directly, missing the 1 from division [inferred]. Possible reason, words from BC-MIS-06022.
- err-BC-ERR-07030: the bars dropped with no stated bound. Possible reason, words from BC-MIS-07018.

## Representations

None. The topic's conversions are symbolic to symbolic.

## Prerequisite bridge

- BC-PRQ-06003 (absolute value inside the ln of a linear factor, as `description_plain` restricts it) and BC-PRQ-06011 (clearing denominators and solving for the numerators), each from its `description_plain` and `failure_signature`.

## Time

BC-QA-06010 is `no_calculator`, typically one part of a multipart free response question; Section II Part B, 15.0 minutes per question (research/exam/exam-structure.md#Section and part layout), with a 5.0 minute share for three points that the record itself infers (unit README section 5). As a multiple choice item it takes the Part A 2.14.

## Checks

- chk-1, completion of ex-1, both bands: the decomposition is given; key ln|x - 3| - ln|2x + 1| + C.
- chk-2, isomorph, both bands. Draw: proper, leading 3, first_shift 2, second_shift -2, weight -1; 8/((3x + 2)(x - 2)). Key ln|x - 2| - ln|3x + 2| + C.
- chk-3, MCQ, low band. Draw: improper, leading 2, first_shift 3, second_shift -2, weight -1; (2x^2 - x + 1)/(2x^2 - x - 6). Key x + ln|x - 2| - ln|2x + 3| + C. Distractors: no x term (BC-ERR-06026), -2 ln|2x + 3| (BC-ERR-06019), a product of logarithms (BC-ERR-06022).

## Delivery

- orientation, ki-1: text. Rule 6: BC-REP-01 alone, and the unit README delivery map puts partial fractions in text and step reveal.
- ex-1 and the four error blocks: step_reveal. Rule 1.
- The prediction: text, on the key idea screen's resolution.
- No drawn block: none of rules 2 to 5 applies. The skills carry BC-REP-01 alone, which is not figure-bearing, and the key idea states a procedure, not a process to draw. The machine record states `no_figure_reason`.

## Band plan

- Low (full), in served order: prediction, orientation, the two bridges, ki-1, st-1 with its contrast pair, ex-1 with its reader lines, chk-1, four error blocks, chk-2, chk-3. 566 words, 3.8 minutes (cap 900 and 6). There is no example 2, so nothing is faded.
- Mid (brief): prediction, orientation, the two bridges, ki-1, st-1 with its contrast pair, ex-1 with its reader lines, chk-1, err-BC-ERR-06019, err-BC-ERR-06022, chk-2. 446 words, 3.0 minutes (cap 450 and 3). The orientation, the strategy cue and separating feature, three cues of ex-1 and both bridges were shortened to fit; no anchor quote (there was none) and no scoring tag (BC-PT-99081 was already untagged) was dropped.
- Refresher: ki-1, the four error blocks, ex-1.

## Sources

- BC-CON-06018; BC-SKL-06062, BC-SKL-06063, BC-SKL-06064, BC-SKL-06065; BC-EK-FUN-6F1; ced:129
- BC-QA-06010; BC-PT-99003, BC-PT-99004, BC-PT-99005, BC-PT-99081
- BC-ERR-06019, BC-ERR-06022, BC-ERR-06026, BC-ERR-07030; BC-MIS-06016, BC-MIS-06019, BC-MIS-06022, BC-MIS-07018
- BC-PRQ-06003, BC-PRQ-06011
- research/units/unit-06-integration-accumulation.md#6.12 Integrating Using Linear Partial Fractions
- research/question-analysis/question-archetypes.md#BC-QA-06010 Antiderivative by linear partial fractions
- research/question-analysis/question-archetypes.md#BC-QA-06008 Antiderivative or definite integral by substitution
- research/exam/exam-structure.md#Section and part layout
- research/scoring/common-point-losses.md#Answer points
- [inferred] BC-PT-99081 untagged for the brief cap. Settled by a cap or a shorter reader text.
- [inferred] The point structure and minute share. Settled by a partial fraction scoring guideline.
- [inferred] ln without bars in SymPy strings. Settled by checker support for Abs.
- [inferred] err-BC-ERR-06026 on the improper form. Settled by serving that draw as an example.
- [inferred] What a fluent solver holds in the head. Settled by timing data per step.

## Machine record

```json
{
 "id": "LSN-CON-06018",
 "kind": "concept",
 "target_id": "BC-CON-06018",
 "unit": "06",
 "skills": [
  "BC-SKL-06062",
  "BC-SKL-06063",
  "BC-SKL-06064",
  "BC-SKL-06065"
 ],
 "prediction": {
  "id": "pr-1",
  "stem": {
   "text": "\\(2x^2-5x-3=(2x+1)(x-3)\\). Which sum of simple fractions equals \\(\\frac{7}{2x^2-5x-3}\\)?",
   "command_verb": "predict"
  },
  "format": "mcq",
  "options": [
   {
    "id": "A",
    "label": "\\(\\frac{7}{2x+1}+\\frac{7}{x-3}\\)",
    "is_key": false
   },
   {
    "id": "B",
    "label": "\\(-\\frac{2}{2x+1}+\\frac{1}{x-3}\\)",
    "is_key": true
   },
   {
    "id": "C",
    "label": "\\(\\frac{1}{2x+1}-\\frac{2}{x-3}\\)",
    "is_key": false
   }
  ],
  "resolution": "Each factor takes one constant numerator. Clearing denominators gives \\(A=-2\\) and \\(B=1\\), and each term integrates to a constant times a logarithm.",
  "sources": [
   "BC-CON-06018",
   "research/units/unit-06-integration-accumulation.md#6.12 Integrating Using Linear Partial Fractions"
  ]
 },
 "no_figure_reason": "The skills carry the symbolic representation only, and the key idea is a decomposition procedure, not a process to draw, so no figure fits.",
 "orientation": {
  "text": "A response factors, solves for the numerators, and writes each term as a logarithm.",
  "sources": [
   "BC-CON-06018",
   "research/units/unit-06-integration-accumulation.md#6.12 Integrating Using Linear Partial Fractions"
  ]
 },
 "key_ideas": [
  {
   "id": "ki-1",
   "ek_id": "BC-EK-FUN-6F1",
   "depth": "core",
   "text": "Factor the denominator into distinct linear factors, write one unknown numerator over each, clear denominators and solve. Each term integrates to a constant times ln|factor|, divided by the factor's leading coefficient.",
   "notation": "A/(x - r) + B/(x - s)",
   "quote": null,
   "sources": [
    "BC-EK-FUN-6F1",
    "ced:129",
    "research/units/unit-06-integration-accumulation.md#6.12 Integrating Using Linear Partial Fractions"
   ]
  }
 ],
 "strategy": [
  {
   "id": "st-1",
   "archetype_id": "BC-QA-06010",
   "cue": "A rational function over a quadratic with distinct linear factors.",
   "method": "Factor the denominator.",
   "rival": "Decomposing an improper integrand without dividing.",
   "separating_feature": "Decompose only when the numerator's degree is lower.",
   "sources": [
    "BC-QA-06010",
    "BC-ERR-06026",
    "research/question-analysis/question-archetypes.md#BC-QA-06008 Antiderivative or definite integral by substitution"
   ],
   "evidence_tag": "verified",
   "contrast": {
    "this": {
     "text": "Find \\(\\int \\frac{9}{2x^2+7x+3}\\,dx\\).",
     "archetype_id": "BC-QA-06010"
    },
    "not_this": {
     "text": "Find \\(\\int \\frac{4x+7}{2x^2+7x+3}\\,dx\\).",
     "why_not": "The numerator is the denominator's derivative: substitute."
    },
    "feature": "Numerator not the denominator's derivative."
   }
  }
 ],
 "worked_examples": [
  {
   "id": "ex-1",
   "archetype_id": "BC-QA-06010",
   "bands": [
    "low",
    "mid"
   ],
   "parameter_draw": {
    "degree": "proper",
    "leading": 2,
    "first_shift": 1,
    "second_shift": -3,
    "weight": -1
   },
   "problem": {
    "text": "Find ∫ 7/(2x^2 - 5x - 3) dx.",
    "command_verb": "find"
   },
   "calculator_status": "no_calculator",
   "steps": [
    {
     "cue": "Degree 0 over degree 2: proper.",
     "why": "2x^2 - 5x - 3 = (2x + 1)(x - 3), distinct factors."
    },
    {
     "cue": "One numerator per factor.",
     "why": "Decomposition applies.",
     "expr": "7/(2*x**2 - 5*x - 3)",
     "relation": "new"
    },
    {
     "cue": "7 = A(x - 3) + B(2x + 1).",
     "why": "Each root clears one term: B = 1, A = -2.",
     "expr": "-2/(2*x + 1) + 1/(x - 3)",
     "relation": "equivalent"
    },
    {
     "cue": "-2/(2x + 1) is derivative over function.",
     "why": "Its 2 cancels: -ln|2x + 1|.",
     "expr": "log(x - 3) - log(2*x + 1) + C",
     "relation": "integrate",
     "variable": "x",
     "point_type_id": "BC-PT-99003"
    },
    {
     "cue": "Report with bars.",
     "why": "ln|x - 3| - ln|2x + 1| + C.",
     "expr": "log(x - 3) + C - log(2*x + 1)",
     "relation": "equivalent",
     "point_type_id": "BC-PT-99004"
    }
   ],
   "answer": {
    "form": "symbolic",
    "expr": "log(x - 3) + C - log(2*x + 1)"
   }
  }
 ],
 "what_a_reader_scores": [
  {
   "example_id": "ex-1",
   "point_type_ids": [
    "BC-PT-99003",
    "BC-PT-99004"
   ],
   "lines": [
    {
     "point_type_id": "BC-PT-99003",
     "text": "Antiderivative. Earned by: A correct antiderivative of the presented integrand, with or without the constant of integration (sg-25:14). Not earned by: An antiderivative of the wrong form, or a jump from integral to value with no antiderivative shown (sg-26:18)."
    },
    {
     "point_type_id": "BC-PT-99004",
     "text": "Answer with or without supporting work. Earned by: The correct value on its own, with no supporting work required (sg-25:3, sg-26:4). Not earned by: A value outside the accepted precision, or a value inconsistent with a required earlier step where the rubric imposes one. Precision: A reported decimal answer must be accurate to three places after the decimal point, rounded or truncated; at most one point per question is lost to inappropriate rounding (sg-25:2, sg-26:2). sg-26:4 also accepts a stated rounding to the nearest integer and several truncations."
    }
   ]
  }
 ],
 "common_errors": [
  {
   "error_id": "BC-ERR-06019",
   "observed_behavior": "The substitution is carried out without the reciprocal constant that du introduces.",
   "scoring_consequence": "The antiderivative point is lost and the value point with it.",
   "wrong_step": {
    "text": "-2 ln|2x + 1|.",
    "expr": "log(x - 3) - 2*log(2*x + 1) + C"
   },
   "right_step": {
    "text": "-ln|2x + 1|.",
    "expr": "log(x - 3) - log(2*x + 1) + C"
   },
   "relation": "distinct",
   "possible_reason": {
    "misconception_id": "BC-MIS-06016",
    "text": "differentials carry over unchanged"
   },
   "sources": [
    "BC-ERR-06019",
    "BC-MIS-06016"
   ],
   "fix_prompt": true
  },
  {
   "error_id": "BC-ERR-06022",
   "observed_behavior": "The response antidifferentiates each factor of a product and multiplies the results.",
   "scoring_consequence": "Neither the u and dv point nor the expression point is earned (sg-23:18, sg-24:18).",
   "wrong_step": {
    "text": "7 times ln-factors multiplied.",
    "expr": "7*log(2*x + 1)*log(x - 3)/2"
   },
   "right_step": {
    "text": "Decomposed first.",
    "expr": "log(x - 3) - log(2*x + 1) + C"
   },
   "relation": "distinct",
   "possible_reason": {
    "misconception_id": "BC-MIS-06019",
    "text": "each factor is antidifferentiated on its own"
   },
   "sources": [
    "BC-ERR-06022",
    "BC-MIS-06019"
   ],
   "fix_prompt": true
  },
  {
   "error_id": "BC-ERR-06026",
   "observed_behavior": "A rational integrand whose numerator degree is at least the denominator degree is split into partial fractions directly.",
   "scoring_consequence": "The decomposition cannot be solved consistently and the antiderivative point is not earned.",
   "wrong_step": {
    "text": "(2x^2 - 5x + 4)/(2x^2 - 5x - 3) split directly.",
    "expr": "-2/(2*x + 1) + 1/(x - 3)"
   },
   "right_step": {
    "text": "Divided first: 1 plus the fractions.",
    "expr": "1 - 2/(2*x + 1) + 1/(x - 3)"
   },
   "relation": "distinct",
   "possible_reason": {
    "misconception_id": "BC-MIS-06022",
    "text": "selects a technique from a visual resemblance to a worked example"
   },
   "sources": [
    "BC-ERR-06026",
    "BC-MIS-06022"
   ],
   "fix_prompt": true
  },
  {
   "error_id": "BC-ERR-07030",
   "observed_behavior": "The response removes an absolute value from a logarithm without using the initial condition or a stated bound to decide the sign.",
   "scoring_consequence": "The branch may contradict the initial condition, which costs the final solving point.",
   "wrong_step": {
    "text": "Bars dropped with no stated bound.",
    "expr": "log(x - 3) - log(2*x + 1) + C"
   },
   "right_step": {
    "text": "Bars kept.",
    "expr": "log(Abs(x - 3)) - log(Abs(2*x + 1)) + C"
   },
   "relation": "distinct",
   "possible_reason": {
    "misconception_id": "BC-MIS-07018",
    "text": "removes an absolute value by habit"
   },
   "sources": [
    "BC-ERR-07030",
    "BC-MIS-07018"
   ],
   "fix_prompt": true
  }
 ],
 "representations": null,
 "prerequisite_bridges": [
  {
   "prq_id": "BC-PRQ-06003",
   "text": "ln of a linear factor carries absolute value bars."
  },
  {
   "prq_id": "BC-PRQ-06011",
   "text": "Clear denominators, then substitute each root."
  }
 ],
 "time": {
  "exam_part": "II-B",
  "budget_minutes": 15.0,
  "source": "research/exam/exam-structure.md#Section and part layout",
  "written_steps": {
   "ex-1": [
    3,
    4,
    5
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
   "archetype_id": "BC-QA-06010",
   "parameter_draw": {
    "degree": "proper",
    "leading": 2,
    "first_shift": 1,
    "second_shift": -3,
    "weight": -1
   },
   "completes": "ex-1",
   "stem": {
    "text": "7/(2x^2 - 5x - 3) = -2/(2x + 1) + 1/(x - 3). Antidifferentiate.",
    "command_verb": "find"
   },
   "key": {
    "form": "symbolic",
    "expr": "log(x - 3) + C - log(2*x + 1)"
   },
   "steps": [
    {
     "text": "Decomposition.",
     "expr": "-2/(2*x + 1) + 1/(x - 3)",
     "relation": "new"
    },
    {
     "text": "Logarithms.",
     "expr": "log(x - 3) - log(2*x + 1) + C",
     "relation": "integrate",
     "variable": "x"
    }
   ],
   "calculator_status": "no_calculator",
   "skills": [
    "BC-SKL-06064"
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
   "archetype_id": "BC-QA-06010",
   "parameter_draw": {
    "degree": "proper",
    "leading": 3,
    "first_shift": 2,
    "second_shift": -2,
    "weight": -1
   },
   "stem": {
    "text": "Find ∫ 8/(3x^2 - 4x - 4) dx.",
    "command_verb": "find"
   },
   "key": {
    "form": "symbolic",
    "expr": "log(x - 2) - log(3*x + 2) + C"
   },
   "steps": [
    {
     "text": "(3x + 2)(x - 2); A = -3, B = 1.",
     "expr": "-3/(3*x + 2) + 1/(x - 2)",
     "relation": "new"
    },
    {
     "text": "Logarithms.",
     "expr": "log(x - 2) - log(3*x + 2) + C",
     "relation": "integrate",
     "variable": "x"
    }
   ],
   "calculator_status": "no_calculator",
   "skills": [
    "BC-SKL-06062",
    "BC-SKL-06063",
    "BC-SKL-06064"
   ]
  },
  {
   "id": "chk-3",
   "check_kind": "mcq",
   "format": "mcq",
   "bands": [
    "low"
   ],
   "archetype_id": "BC-QA-06010",
   "parameter_draw": {
    "degree": "improper",
    "leading": 2,
    "first_shift": 3,
    "second_shift": -2,
    "weight": -1
   },
   "stem": {
    "text": "∫ (2x^2 - x + 1)/(2x^2 - x - 6) dx =",
    "command_verb": "identify"
   },
   "key": {
    "form": "symbolic",
    "expr": "x + log(x - 2) - log(2*x + 3) + C"
   },
   "steps": [
    {
     "text": "Divide: 1 + 7/((2x + 3)(x - 2)).",
     "expr": "1 - 2/(2*x + 3) + 1/(x - 2)",
     "relation": "new"
    },
    {
     "text": "Antidifferentiate.",
     "expr": "x + log(x - 2) - log(2*x + 3) + C",
     "relation": "integrate",
     "variable": "x"
    }
   ],
   "options": [
    {
     "id": "A",
     "is_key": false,
     "expr": "log(x - 2) - log(2*x + 3) + C",
     "error_path": "BC-ERR-06026",
     "derivation": "decomposed without dividing, the 1 lost"
    },
    {
     "id": "B",
     "is_key": false,
     "expr": "x + log(x - 2) - 2*log(2*x + 3) + C",
     "error_path": "BC-ERR-06019",
     "derivation": "the 1/2 from the factor 2x + 3 dropped"
    },
    {
     "id": "C",
     "is_key": false,
     "expr": "x + 7*log(2*x + 3)*log(x - 2)/2 + C",
     "error_path": "BC-ERR-06022",
     "derivation": "the 7 and the two factors antidifferentiated apart and multiplied"
    },
    {
     "id": "D",
     "is_key": true,
     "expr": "x + log(x - 2) - log(2*x + 3) + C",
     "error_path": null
    }
   ],
   "calculator_status": "no_calculator",
   "skills": [
    "BC-SKL-06062",
    "BC-SKL-06064"
   ]
  }
 ],
 "delivery": [
  {
   "block": "orientation",
   "mode": "text",
   "reason": "rule 6: BC-REP-01 only on the concept's skills (unit README delivery map)",
   "sources": [
    "BC-SKL-06062"
   ]
  },
  {
   "block": "ki-1",
   "mode": "text",
   "reason": "rule 6: a symbolic procedure with BC-REP-01 alone; no process, no figure-bearing representation",
   "sources": [
    "BC-SKL-06063",
    "BC-SKL-06064"
   ]
  },
  {
   "block": "ex-1",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  },
  {
   "block": "err-BC-ERR-06019",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  },
  {
   "block": "err-BC-ERR-06022",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  },
  {
   "block": "err-BC-ERR-06026",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  },
  {
   "block": "err-BC-ERR-07030",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  }
 ],
 "refresher": [
  "ki-1",
  "err-BC-ERR-06019",
  "err-BC-ERR-06022",
  "err-BC-ERR-06026",
  "err-BC-ERR-07030",
  "ex-1"
 ],
 "research_lines": [
  {
   "file": "research/units/unit-06-integration-accumulation.md",
   "line": "Factor the denominator into distinct linear factors, write the decomposition with unknown constant numerators, clear denominators, solve for the constants, and antidifferentiate each term into a constant times the natural logarithm of an absolute value."
  }
 ],
 "inferred": [
  {
   "claim": "BC-PT-99081 (the decomposition point) is listed by BC-QA-06010 but not tagged on ex-1: its reader line would take the brief band past 450 words. Step 3 carries the decomposition.",
   "settles": "A brief-band cap that admits a third reader line, or a shorter BC-PT-99081 reader text."
  },
  {
   "claim": "BC-QA-06010's point structure is itself inferred in the record (no Unit 6 partial fraction part in the 2023 to 2025 guidelines); the lesson takes Section II Part B with a 5.0 minute share (unit README section 5).",
   "settles": "A scoring guideline for a partial fraction part."
  },
  {
   "claim": "SymPy strings in ex-1 and the checks write ln without absolute value; the served text carries the bars. The checker's integrate relation cannot differentiate Abs.",
   "settles": "Checker support for Abs under the integrate relation."
  },
  {
   "claim": "err-BC-ERR-06026 is shown on the improper form of ex-1's draw (degree improper, numerator 2x^2 - 5x + 4), since the proper draw needs no division.",
   "settles": "Serving the improper draw as a second example."
  },
  {
   "claim": "A fluent solver clears denominators in the head and writes the factored denominator, the constants and the logarithms.",
   "settles": "Timing data per step once the fluency telemetry exists."
  }
 ],
 "sources": [
  "BC-CON-06018",
  "BC-SKL-06062",
  "BC-SKL-06063",
  "BC-SKL-06064",
  "BC-SKL-06065",
  "BC-EK-FUN-6F1",
  "ced:129",
  "BC-QA-06010",
  "BC-PT-99003",
  "BC-PT-99004",
  "BC-PT-99005",
  "BC-PT-99081",
  "BC-ERR-06019",
  "BC-ERR-06022",
  "BC-ERR-06026",
  "BC-ERR-07030",
  "BC-MIS-06016",
  "BC-MIS-06019",
  "BC-MIS-06022",
  "BC-MIS-07018",
  "BC-PRQ-06003",
  "BC-PRQ-06011",
  "research/units/unit-06-integration-accumulation.md#6.12 Integrating Using Linear Partial Fractions",
  "research/question-analysis/question-archetypes.md#BC-QA-06010 Antiderivative by linear partial fractions",
  "research/exam/exam-structure.md#Section and part layout",
  "research/scoring/common-point-losses.md#Answer points"
 ],
 "read_minutes": {
  "full": 3.8,
  "brief": 3.0
 },
 "word_count": {
  "full": 565,
  "brief": 445
 }
}
```
