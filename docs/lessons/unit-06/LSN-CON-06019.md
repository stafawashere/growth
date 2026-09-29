---
title: LSN-CON-06019 Improper integrals and convergence
research_date: 2026-09-29
status: designed
purpose: Authoring spec for the concept lesson on BC-CON-06019, improper integrals written as limits of definite integrals and concluded as convergent with a value or divergent, built from authoring_bundle("BC-CON-06019") and the research files it cites.
---

# LSN-CON-06019 Improper integrals and convergence

Concept BC-CON-06019 (skills BC-SKL-06066 to BC-SKL-06070), topic 6.13 of Unit 6, loaded by one archetype, BC-QA-06011 (family improper-integral). Its hard parents are BC-CON-06011 and BC-CON-06012, with BC-SKL-01054 and BC-TOP-0102 (limits at infinity) outside the unit (docs/lessons/unit-06/README.md, section 1).

## Prediction

One multiple choice question on worked example 1's own integrand, \(\frac{6x}{(x^2+2)^2}\) from 1, asked before the rule is shown: given that the area to \(b\) is \(1-\frac{3}{b^2+2}\), what the area out to infinity is. The key is 1, the limit of ex-1's third valued step as \(b\) grows, which is ex-1's answer. The distractors are an undefined area because the interval is infinite, and the term that leaves \(b\) out. The resolution, shown beside the choice on the key idea screen, states that an improper integral is the limit of the integrals to \(b\) and that a finite limit means convergence, with no verdict word. Sources: BC-CON-06019 and the topic 6.13 section the key idea cites [inferred].

## Orientation

Served text (16 words), from BC-CON-06019 `description_plain` and the topic's Assessment behaviour paragraph (research/units/unit-06-integration-accumulation.md#6.13 Evaluating Improper Integrals): limit notation carried throughout and a conclusion stated as convergence or divergence rather than a bare number. No count, no frequency.

## Key ideas

BC-SKL-06066 maps to BC-EK-LIM-6A1; BC-SKL-06067, 06068 and 06069 map to BC-EK-LIM-6A2; BC-SKL-06070 to both. Two blocks.

- ki-1 (core), BC-EK-LIM-6A1, ced:130. Paraphrase of the Definition paragraph of Required mathematical knowledge. Notation line from the concept record.
- ki-2 (core), BC-EK-LIM-6A2, ced:130. Paraphrase of the Evaluation paragraph: limits of definite integrals, converging when the limit exists. Its notation line is the limit form written in ex-1.

No quotes: the brief band has no room.

## Recognition

BC-QA-06011 (research/question-analysis/question-archetypes.md#BC-QA-06011 Improper integral convergence or divergence). `typical_wording`: "evaluate the improper integral of the given expression, or show that the integral diverges". `common_givens`: an explicit integrand on an infinite interval, an integrand unbounded at a point of the interval, a family of functions with the parameter fixed at a stated value. `asked_to_produce`: the improper integral written as a limit of definite integrals, an antiderivative, a value or a statement of divergence with a reason, a parameter value that gives the integral a stated value. Official examples: BC-FRQ-2019-Q5-C, BC-FRQ-2023-Q5-B, BC-FRQ-2026-Q5-D, BC-MCQ-SAMPLE-019, BC-MCQ-PE2012-025.

The signal: ∞ as a limit of integration, or a denominator vanishing at an endpoint. The words "or show that the integral diverges" confirm it. Contrast pair on st-1: the this stem is on BC-QA-06011, a rational integrand on an infinite interval; the not this stem is the same integrand on a finite interval, the ordinary definite integral (BC-CON-06012) that the near miss of computing with infinity would treat alike. The separating feature is an infinite limit or an unbounded integrand.

What says "not this concept": finite limits with an integrand bounded on the interval (an ordinary definite integral, BC-CON-06012).

## Method choice

One strategy block, both bands.

- st-1, BC-QA-06011. Cue from `common_givens` and `asked_to_produce`. Method, `expected_solution_path[0]`: name the impropriety and replace the offending limit by a variable. Rival from `wrong_approaches`: substituting ∞ and computing with it, cited in the block's `sources` (BC-ERR-99007), not in its text. Separating feature: ∞ is not a value, so only the limit of ordinary integrals is written. First written line: lim as b → ∞ of the integral from 1 to b.

## Solution path

- There is no example 2, so nothing is faded and there is no `fade_from`.
- ex-1, BC-QA-06011, both bands, no calculator. Draw from `parameter_spec`: impropriety infinite, outcome converges, coefficient 6, degree 2, lower 1, shift 2, root 1, gap 1; integrand 6x/(x^2 + 2)^2 on [1, ∞). No published BC-QA-06011 item carries this draw.
- Steps follow `expected_solution_path`: name the impropriety (no value); the integral to b (new); the antiderivative evaluated from 1 to b, 1 - 3/(b^2 + 2) (equivalent, BC-PT-99003); the limit, 1 (limit in b at ∞, BC-PT-99004).

A fluent solver writes every line with its limit notation, since the notation is scored throughout (unit README section 5); the naming of the impropriety is held in the head [inferred].

## Scoring

BC-QA-06011 lists BC-PT-99053, BC-PT-99003, BC-PT-99005 and BC-PT-99004. ex-1 tags BC-PT-99003 on the antiderivative and BC-PT-99004 on the value; reader lines are `reader_checks` output copied exactly. BC-PT-99053 is not tagged, to keep the brief band under 450 words [inferred]. From `scoring_pattern`: one point for limit notation carried throughout with no arithmetic involving ∞, one for the antiderivative, one for the value; substituting while still in u forfeits the value point (sg-23:17). The notation point is the one place notation is scored on its own (research/scoring/notation-requirements.md#Limit notation); arithmetic with ∞ is a notation loss (research/scoring/common-point-losses.md#Notation points).

## Traps

All four active errors meeting the skills, in the bundle's order: BC-ERR-06018, BC-ERR-06019, BC-ERR-99007, BC-ERR-06025. Mid band shows the first two. BC-ERR-06018, BC-ERR-06019 and BC-ERR-06025 differ from the right step as expressions, so they are fix prompts (`fix_prompt` true); BC-ERR-99007 is equivalent, so it keeps the reveal form (`fix_prompt` false).

- err-BC-ERR-06018: -3/u evaluated at x = 1 and b, giving 3 - 3/b, against the u limits. No possible reason line.
- err-BC-ERR-06019: 6x dx read as du, 2 - 6/(b^2 + 2). No possible reason line.
- err-BC-ERR-99007: 1 - 3/(∞^2 + 2) written. The CAS finds it equivalent to the limit: the number is the same, the notation point is not. Possible reason, words from BC-MIS-99008.
- err-BC-ERR-06025: on the divergent form of the draw (power 1/2), -6√3 reported where 6√(b^2 + 2) grows without bound [inferred]. No possible reason: the integrand tends to 6, not 0, so BC-MIS-06021 does not fit this draw.

## Representations

None as a separate block. The topic's conversion, unbounded graph to a finite value statement (BC-REP-02 to BC-REP-01), is carried by the ki-1 figure and the ki-2 motion.

## Prerequisite bridge

None.

## Time

BC-QA-06011 is `no_calculator`, typically one part of a multipart free response question; Section II Part B, 15.0 minutes per question (research/exam/exam-structure.md#Section and part layout), a 5.0 minute share for its three points (unit README section 5). As a multiple choice item it takes the Part A 2.14. Nothing is skipped on paper: the limit notation is scored on every line.

## Checks

- chk-1, completion of ex-1, both bands: the integral to b is given; key 1.
- chk-2, isomorph, both bands. Draw: infinite, converges, coefficient 4, degree 3, lower 1, shift 1, root 1, gap 1; 4x^2/(x^3 + 1)^2 on [1, ∞). Key 2/3.
- chk-3, MCQ, low band. Draw: infinite, converges, coefficient 3, degree 2, lower 2, shift 5, root 1, gap 1; 3x/(x^2 + 5)^2 on [2, ∞). Key 1/6. Distractors: 3/4 (BC-ERR-06018), 1/3 and 2/3 (BC-ERR-06019, constant dropped or not inverted).

## Delivery

- orientation: text. Rule 6.
- ki-1: figure. Rule 4: BC-REP-02 on BC-QA-06011 and the topic's graph-to-value conversion; two panels, an infinite interval and a vertical asymptote, labels inside [inferred].
- ki-2: motion. Rule 2: the upper limit b moving outward with the area approaching 1; reduced motion steps by key press; the fallback is three frames side by side [inferred].
- ex-1 and the four error blocks: step_reveal. Rule 1.
- The prediction: text, on the key idea screen's resolution.

## Band plan

- Low (full), in served order: prediction, orientation, ki-1 (figure), ki-2 (motion), st-1 with its contrast pair, ex-1 with its reader lines, chk-1, four error blocks, chk-2, chk-3. 569 words, 3.8 minutes (cap 900 and 6). There is no example 2, so nothing is faded, and no bridges (no BC-PRQ parent).
- Mid (brief): prediction, orientation, ki-1, ki-2, st-1 with its contrast pair, ex-1 with its reader lines, chk-1, err-BC-ERR-06018, err-BC-ERR-06019, chk-2. 450 words, 3.0 minutes (cap 450 and 3). The orientation, both key ideas, the strategy cue and separating feature, the prediction options and two cues of ex-1 were shortened to fit; no anchor quote (there was none) and no scoring tag was dropped (BC-PT-99053 was already untagged).
- Refresher: ki-1, ki-2, the four error blocks, ex-1.

## Sources

- BC-CON-06019; BC-SKL-06066, BC-SKL-06067, BC-SKL-06068, BC-SKL-06069, BC-SKL-06070; BC-EK-LIM-6A1, BC-EK-LIM-6A2; ced:130
- BC-QA-06011; BC-PT-99053, BC-PT-99003, BC-PT-99005, BC-PT-99004; sg-23:17
- BC-ERR-06018, BC-ERR-06019, BC-ERR-99007, BC-ERR-06025; BC-MIS-99008, BC-MIS-06021
- research/units/unit-06-integration-accumulation.md#6.13 Evaluating Improper Integrals
- research/question-analysis/question-archetypes.md#BC-QA-06011 Improper integral convergence or divergence
- research/exam/exam-structure.md#Section and part layout
- research/scoring/notation-requirements.md#Limit notation
- research/scoring/common-point-losses.md#Notation points
- [inferred] BC-PT-99053 untagged for the brief cap. Settled by a cap or a shorter reader text.
- [inferred] err-BC-ERR-06025 on the divergent form. Settled by serving that draw as an example.
- [inferred] Figure and motion modes. Settled by the modality A/B.
- [inferred] What a fluent solver holds in the head. Settled by timing data per step.

## Machine record

```json
{
 "id": "LSN-CON-06019",
 "kind": "concept",
 "target_id": "BC-CON-06019",
 "unit": "06",
 "skills": [
  "BC-SKL-06066",
  "BC-SKL-06067",
  "BC-SKL-06068",
  "BC-SKL-06069",
  "BC-SKL-06070"
 ],
 "prediction": {
  "id": "pr-1",
  "stem": {
   "text": "Predict. The area under \\(y=\\frac{6x}{(x^2+2)^2}\\) from 1 to \\(b\\) is \\(1-\\frac{3}{b^2+2}\\). What is the area out to infinity?",
   "command_verb": "predict"
  },
  "format": "mcq",
  "options": [
   {
    "id": "A",
    "label": "Undefined, the interval is infinite",
    "is_key": false
   },
   {
    "id": "B",
    "label": "1, the limit as \\(b\\) grows",
    "is_key": true
   },
   {
    "id": "C",
    "label": "3, the term without \\(b\\)",
    "is_key": false
   }
  ],
  "resolution": "An improper integral is the limit of the integrals to \\(b\\): \\(1-\\frac{3}{b^2+2}\\to 1\\), so it converges to 1.",
  "sources": [
   "BC-CON-06019",
   "research/units/unit-06-integration-accumulation.md#6.13 Evaluating Improper Integrals"
  ]
 },
 "orientation": {
  "text": "A response carries the limit on every line and concludes convergence with a value, or divergence.",
  "sources": [
   "BC-CON-06019",
   "research/units/unit-06-integration-accumulation.md#6.13 Evaluating Improper Integrals"
  ]
 },
 "key_ideas": [
  {
   "id": "ki-1",
   "ek_id": "BC-EK-LIM-6A1",
   "depth": "core",
   "text": "An integral is improper when a limit is infinite or the integrand is unbounded.",
   "notation": "limit as b approaches infinity",
   "quote": null,
   "sources": [
    "BC-EK-LIM-6A1",
    "ced:130",
    "research/units/unit-06-integration-accumulation.md#6.13 Evaluating Improper Integrals"
   ]
  },
  {
   "id": "ki-2",
   "ek_id": "BC-EK-LIM-6A2",
   "depth": "core",
   "text": "Replace the offending limit by b; a finite limit as b moves out means convergence.",
   "notation": "lim_(b→∞) ∫_a^b f(x) dx",
   "quote": null,
   "sources": [
    "BC-EK-LIM-6A2",
    "ced:130",
    "research/units/unit-06-integration-accumulation.md#6.13 Evaluating Improper Integrals"
   ]
  }
 ],
 "strategy": [
  {
   "id": "st-1",
   "archetype_id": "BC-QA-06011",
   "cue": "An integrand on an infinite interval, or unbounded inside it.",
   "method": "Name the impropriety and replace the offending limit by a variable.",
   "rival": "Computing with ∞ as a number.",
   "separating_feature": "∞ is not a value.",
   "sources": [
    "BC-QA-06011",
    "BC-ERR-99007"
   ],
   "evidence_tag": "verified",
   "contrast": {
    "this": {
     "text": "Evaluate \\(\\int_2^{\\infty} \\frac{4x}{(x^2+1)^2}\\,dx\\).",
     "archetype_id": "BC-QA-06011"
    },
    "not_this": {
     "text": "Evaluate \\(\\int_2^{5} \\frac{4x}{(x^2+1)^2}\\,dx\\).",
     "why_not": "Finite limits, bounded integrand: an ordinary definite integral."
    },
    "feature": "An infinite limit or an unbounded integrand."
   }
  }
 ],
 "worked_examples": [
  {
   "id": "ex-1",
   "archetype_id": "BC-QA-06011",
   "bands": [
    "low",
    "mid"
   ],
   "parameter_draw": {
    "impropriety": "infinite",
    "outcome": "converges",
    "coefficient": 6,
    "degree": 2,
    "lower": 1,
    "shift": 2,
    "root": 1,
    "gap": 1
   },
   "problem": {
    "text": "Evaluate ∫_1^∞ 6x/(x^2 + 2)^2 dx or show it diverges.",
    "command_verb": "evaluate"
   },
   "calculator_status": "no_calculator",
   "steps": [
    {
     "cue": "Upper limit ∞.",
     "why": "Replace it by b."
    },
    {
     "cue": "Write lim_(b→∞) of the integral to b.",
     "why": "Limit notation on every line.",
     "expr": "Integral(6*x/(x**2 + 2)**2, (x, 1, b))",
     "relation": "new"
    },
    {
     "cue": "u = x^2 + 2: antiderivative -3/(x^2 + 2).",
     "why": "Evaluated from 1 to b.",
     "expr": "3/3 - 3/(b**2 + 2)",
     "relation": "equivalent",
     "point_type_id": "BC-PT-99003"
    },
    {
     "cue": "b → ∞: 3/(b^2 + 2) → 0.",
     "why": "Finite limit: converges to 1.",
     "expr": "1",
     "relation": "limit",
     "variable": "b",
     "point": "oo",
     "point_type_id": "BC-PT-99004"
    }
   ],
   "answer": {
    "form": "symbolic",
    "expr": "1"
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
   "error_id": "BC-ERR-06018",
   "observed_behavior": "The antiderivative is written in the substituted variable and the original x limits are substituted into it.",
   "scoring_consequence": "The response is not eligible for the answer point even when the numerical value is correct (sg-23:17, sg-23:16).",
   "wrong_step": {
    "text": "-3/u at x = 1, b.",
    "expr": "3 - 3/b"
   },
   "right_step": {
    "text": "-3/u at u = 3, b^2 + 2.",
    "expr": "1 - 3/(b**2 + 2)"
   },
   "relation": "distinct",
   "possible_reason": null,
   "sources": [
    "BC-ERR-06018"
   ],
   "fix_prompt": true
  },
  {
   "error_id": "BC-ERR-06019",
   "observed_behavior": "The substitution is carried out without the reciprocal constant that du introduces.",
   "scoring_consequence": "The antiderivative point is lost and the value point with it.",
   "wrong_step": {
    "text": "6x dx = du.",
    "expr": "2 - 6/(b**2 + 2)"
   },
   "right_step": {
    "text": "6x dx = 3 du.",
    "expr": "1 - 3/(b**2 + 2)"
   },
   "relation": "distinct",
   "possible_reason": null,
   "sources": [
    "BC-ERR-06019"
   ],
   "fix_prompt": true
  },
  {
   "error_id": "BC-ERR-99007",
   "observed_behavior": "Responses substitute the infinity symbol for the variable and compute with it, or open an improper integral with limit notation and then abandon it before the evaluation is complete.",
   "scoring_consequence": "The response becomes ineligible for the final point of the part; in improper integral parts the evaluation points are lost.",
   "wrong_step": {
    "text": "1 - 3/(∞^2 + 2) written.",
    "expr": "1 - 3/(oo**2 + 2)"
   },
   "right_step": {
    "text": "The limit as b → ∞.",
    "expr": "Limit(1 - 3/(b**2 + 2), b, oo)"
   },
   "relation": "equivalent",
   "possible_reason": {
    "misconception_id": "BC-MIS-99008",
    "text": "substitutes the infinity symbol for the variable and computes with the result"
   },
   "sources": [
    "BC-ERR-99007",
    "BC-MIS-99008"
   ],
   "fix_prompt": false
  },
  {
   "error_id": "BC-ERR-06025",
   "observed_behavior": "The response produces a finite number although the limit is infinite or fails to exist.",
   "scoring_consequence": "The answer point is not earned because the required conclusion is a statement of divergence.",
   "wrong_step": {
    "text": "Power 1/2 form: -6√3 reported.",
    "expr": "-6*sqrt(3)"
   },
   "right_step": {
    "text": "6√(b^2 + 2) grows: diverges.",
    "expr": "oo"
   },
   "relation": "distinct",
   "possible_reason": null,
   "sources": [
    "BC-ERR-06025",
    "BC-MIS-06021"
   ],
   "fix_prompt": true
  }
 ],
 "representations": null,
 "prerequisite_bridges": [],
 "time": {
  "exam_part": "II-B",
  "budget_minutes": 15.0,
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
   "archetype_id": "BC-QA-06011",
   "parameter_draw": {
    "impropriety": "infinite",
    "outcome": "converges",
    "coefficient": 6,
    "degree": 2,
    "lower": 1,
    "shift": 2,
    "root": 1,
    "gap": 1
   },
   "completes": "ex-1",
   "stem": {
    "text": "∫_1^b 6x/(x^2 + 2)^2 dx = 1 - 3/(b^2 + 2). Find the improper integral to ∞.",
    "command_verb": "find"
   },
   "key": {
    "form": "symbolic",
    "expr": "1"
   },
   "steps": [
    {
     "text": "Integral to b.",
     "expr": "1 - 3/(b**2 + 2)",
     "relation": "new"
    },
    {
     "text": "Limit.",
     "expr": "1",
     "relation": "limit",
     "variable": "b",
     "point": "oo"
    }
   ],
   "calculator_status": "no_calculator",
   "skills": [
    "BC-SKL-06068"
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
   "archetype_id": "BC-QA-06011",
   "parameter_draw": {
    "impropriety": "infinite",
    "outcome": "converges",
    "coefficient": 4,
    "degree": 3,
    "lower": 1,
    "shift": 1,
    "root": 1,
    "gap": 1
   },
   "stem": {
    "text": "Evaluate ∫_1^∞ 4x^2/(x^3 + 1)^2 dx or show it diverges.",
    "command_verb": "evaluate"
   },
   "key": {
    "form": "symbolic",
    "expr": "2/3"
   },
   "steps": [
    {
     "text": "Limit of the integral to b.",
     "expr": "Integral(4*x**2/(x**3 + 1)**2, (x, 1, b))",
     "relation": "new"
    },
    {
     "text": "u = x^3 + 1: antiderivative -4/(3u).",
     "expr": "2/3 - 4/(3*(b**3 + 1))",
     "relation": "equivalent"
    },
    {
     "text": "b → ∞.",
     "expr": "2/3",
     "relation": "limit",
     "variable": "b",
     "point": "oo"
    }
   ],
   "calculator_status": "no_calculator",
   "skills": [
    "BC-SKL-06067",
    "BC-SKL-06068"
   ]
  },
  {
   "id": "chk-3",
   "check_kind": "mcq",
   "format": "mcq",
   "bands": [
    "low"
   ],
   "archetype_id": "BC-QA-06011",
   "parameter_draw": {
    "impropriety": "infinite",
    "outcome": "converges",
    "coefficient": 3,
    "degree": 2,
    "lower": 2,
    "shift": 5,
    "root": 1,
    "gap": 1
   },
   "stem": {
    "text": "∫_2^∞ 3x/(x^2 + 5)^2 dx =",
    "command_verb": "identify"
   },
   "key": {
    "form": "symbolic",
    "expr": "1/6"
   },
   "steps": [
    {
     "text": "Limit of the integral to b.",
     "expr": "Integral(3*x/(x**2 + 5)**2, (x, 2, b))",
     "relation": "new"
    },
    {
     "text": "Antiderivative -3/(2(x^2 + 5)) from 2 to b.",
     "expr": "1/6 - 3/(2*(b**2 + 5))",
     "relation": "equivalent"
    },
    {
     "text": "b → ∞.",
     "expr": "1/6",
     "relation": "limit",
     "variable": "b",
     "point": "oo"
    }
   ],
   "options": [
    {
     "id": "A",
     "is_key": false,
     "expr": "3/4",
     "error_path": "BC-ERR-06018",
     "derivation": "-3/(2u) evaluated at the x limits 2 and b"
    },
    {
     "id": "B",
     "is_key": false,
     "expr": "1/3",
     "error_path": "BC-ERR-06019",
     "derivation": "3x dx read as 3 du, the 1/2 dropped"
    },
    {
     "id": "C",
     "is_key": true,
     "expr": "1/6",
     "error_path": null
    },
    {
     "id": "D",
     "is_key": false,
     "expr": "2/3",
     "error_path": "BC-ERR-06019",
     "derivation": "the constant multiplied by 2 instead of its reciprocal"
    }
   ],
   "calculator_status": "no_calculator",
   "skills": [
    "BC-SKL-06067",
    "BC-SKL-06068"
   ]
  }
 ],
 "delivery": [
  {
   "block": "orientation",
   "mode": "text",
   "reason": "rule 6: a statement of what a response shows; the figure-bearing representation is served once, on the first key idea",
   "sources": [
    "BC-SKL-06066"
   ]
  },
  {
   "block": "ki-1",
   "mode": "figure",
   "reason": "rule 4: BC-REP-02 in BC-QA-06011 representations and the topic's conversion 'unbounded graph to a finite value statement' (unit README delivery map); not promoted, since no stem asks for a reading of a varying relationship here",
   "sources": [
    "BC-QA-06011",
    "BC-SKL-06066"
   ],
   "spec": {
    "kind": "stacked_graphs",
    "representations": [
     "BC-REP-02"
    ],
    "panels": [
     {
      "curve": "6*x/(x**2 + 2)**2",
      "window": {
       "x": [
        0,
        8
       ],
       "y": [
        0,
        0.8
       ]
      },
      "shade": {
       "from": 1,
       "to": 8,
       "open_right": true
      },
      "labels": [
       {
        "text": "upper limit infinite",
        "placement": "inside",
        "at": "right end of the shaded region"
       }
      ]
     },
     {
      "curve": "3*x**2/sqrt(x**3 - 1)",
      "window": {
       "x": [
        1,
        2
       ],
       "y": [
        0,
        20
       ]
      },
      "asymptotes": [
       {
        "type": "vertical",
        "x": 1,
        "style": "dashed"
       }
      ],
      "labels": [
       {
        "text": "integrand unbounded at x = 1",
        "placement": "inside",
        "at": "beside the asymptote"
       }
      ]
     }
    ]
   },
   "fallback": "the two panels as one static image with their labels",
   "keyboard": "none needed: the figure has no control"
  },
  {
   "block": "ki-2",
   "mode": "motion",
   "reason": "rule 2: 'determined using limits of definite integrals' is a limit being taken, the upper limit b moving outward (unit README delivery map)",
   "sources": [
    "BC-SKL-06067",
    "BC-SKL-06068"
   ],
   "spec": {
    "kind": "graph",
    "representations": [
     "BC-REP-02"
    ],
    "window": {
     "x": [
      0,
      12
     ],
     "y": [
      0,
      0.8
     ]
    },
    "curves": [
     {
      "expr": "6*x/(x**2 + 2)**2",
      "domain": [
       0,
       12
      ]
     }
    ],
    "frames": [
     {
      "b": 2,
      "area": 0.5
     },
     {
      "b": 5,
      "area": 0.889
     },
     {
      "b": 10,
      "area": 0.971
     },
     {
      "b": 50,
      "area": 0.999
     }
    ],
    "shade": {
     "from": 1,
     "to": "b"
    },
    "labels": [
     {
      "text": "area from 1 to b = 1 - 3/(b^2 + 2)",
      "placement": "inside"
     },
     {
      "text": "b",
      "placement": "inside",
      "at": "the moving right edge"
     },
     {
      "text": "approaches 1",
      "placement": "inside"
     }
    ]
   },
   "fallback": "the frames at b = 2, 5 and 50 side by side with their areas",
   "keyboard": "Right arrow steps to the next frame, Left arrow to the previous; Space pauses auto-advance",
   "reduced_motion": "no auto-advance; each key press cross-fades to the next frame"
  },
  {
   "block": "ex-1",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  },
  {
   "block": "err-BC-ERR-06018",
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
   "block": "err-BC-ERR-99007",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  },
  {
   "block": "err-BC-ERR-06025",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  }
 ],
 "refresher": [
  "ki-1",
  "ki-2",
  "err-BC-ERR-06018",
  "err-BC-ERR-06019",
  "err-BC-ERR-99007",
  "err-BC-ERR-06025",
  "ex-1"
 ],
 "research_lines": [
  {
   "file": "research/scoring/notation-requirements.md",
   "line": "Improper integrals are the one place the guidelines treat notation as a point in its own right."
  }
 ],
 "inferred": [
  {
   "claim": "BC-PT-99053 (limit notation) is listed by BC-QA-06011 but not tagged on ex-1: its reader line would take the brief band past 450 words. Step 2's why line and err-BC-ERR-99007 carry the requirement.",
   "settles": "A brief-band cap that admits a third reader line, or a shorter BC-PT-99053 reader text."
  },
  {
   "claim": "err-BC-ERR-06025 is shown on the divergent form of ex-1's draw (power 1/2, outcome diverges), since the drawn integral converges.",
   "settles": "Serving the divergent draw as a second example."
  },
  {
   "claim": "The figure for ki-1 and the motion for ki-2 serve better than text.",
   "settles": "The modality A/B in the build plan: skip rate and time to first credited success by mode."
  },
  {
   "claim": "A fluent solver holds the naming of the impropriety in the head and writes the limit of the integral, the antiderivative in b and the limit.",
   "settles": "Timing data per step once the fluency telemetry exists."
  }
 ],
 "sources": [
  "BC-CON-06019",
  "BC-SKL-06066",
  "BC-SKL-06067",
  "BC-SKL-06068",
  "BC-SKL-06069",
  "BC-SKL-06070",
  "BC-EK-LIM-6A1",
  "BC-EK-LIM-6A2",
  "ced:130",
  "BC-QA-06011",
  "BC-PT-99053",
  "BC-PT-99003",
  "BC-PT-99005",
  "BC-PT-99004",
  "sg-23:17",
  "BC-ERR-06018",
  "BC-ERR-06019",
  "BC-ERR-99007",
  "BC-ERR-06025",
  "BC-MIS-99008",
  "BC-MIS-06021",
  "research/units/unit-06-integration-accumulation.md#6.13 Evaluating Improper Integrals",
  "research/question-analysis/question-archetypes.md#BC-QA-06011 Improper integral convergence or divergence",
  "research/exam/exam-structure.md#Section and part layout",
  "research/scoring/notation-requirements.md#Limit notation",
  "research/scoring/common-point-losses.md#Notation points"
 ],
 "read_minutes": {
  "full": 3.8,
  "brief": 3.0
 },
 "word_count": {
  "full": 569,
  "brief": 450
 }
}
```
