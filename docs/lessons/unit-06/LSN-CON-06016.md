---
title: LSN-CON-06016 Rearrangement into an integrable form
research_date: 2026-09-29
status: designed
purpose: Authoring spec for the concept lesson on BC-CON-06016, long division and completing the square before antidifferentiating, built from authoring_bundle("BC-CON-06016") and the research files it cites.
---

# LSN-CON-06016 Rearrangement into an integrable form

Concept BC-CON-06016 (skills BC-SKL-06053 to BC-SKL-06056), topic 6.10 of Unit 6, loaded by BC-QA-06016 (family procedure-selection), BC-QA-06018 and BC-QA-06019 (family antidifferentiation-technique). Its hard parents are BC-CON-06014 and BC-CON-06015 (docs/lessons/unit-06/README.md, section 1).

## Prediction

One multiple choice question on worked example 1's own integrand, \(\frac{2(x^2+3)}{x+2}\), asked before the rule is shown: which first step makes it antidifferentiable term by term. The key is division, whose result is ex-1's second valued step, \(2x-4+\frac{14}{x+2}\). The distractors are the two errors of the concept's traps, splitting into \(\frac{A}{x+2}\) without dividing (BC-ERR-06026) and antidifferentiating top and bottom apart (BC-ERR-06022). The resolution, shown beside the choice on the key idea screen, states what the degrees give and that decomposition needs a proper fraction, with no verdict word. Sources: BC-CON-06016 and the topic 6.10 section the key idea cites [inferred].

## Orientation

Served text (16 words), from BC-CON-06016 `description_plain` and the topic's Assessment behaviour paragraph (research/units/unit-06-integration-accumulation.md#6.10 Integrating Functions Using Long Division and Completing the Square): the integrand is rewritten, by division or completing the square, before any antiderivative is written. No count, no frequency.

## Key ideas

All four skills map to BC-EK-FUN-6D3, so one core block, both bands.

- ki-1 (core), BC-EK-FUN-6D3, ced:127. Paraphrase of the Long division and Completing the square paragraphs of Required mathematical knowledge. Anchor quote, 17 words, verbatim on ced:127. Notation line from the concept record.

## Recognition

BC-QA-06016 (research/question-analysis/question-archetypes.md#BC-QA-06016 Selecting an antidifferentiation technique from the form of the integrand), the technique-selection drill archetype of plan 15. `typical_wording`: "find the indefinite integral, showing the work that leads to your answer". `asked_to_produce`: an indefinite integral with supporting work, the technique the integrand's structure calls for. `common_givens`: a product of a linear factor and a cosine. The `parameter_spec` notes give the rational form m(x^2 + c)/(x + a), numerator degree above the denominator's, which selects long division first. No official examples are listed.

BC-QA-06018 (research/question-analysis/question-archetypes.md#BC-QA-06018 Antiderivative matched to an inverse trigonometric form, directly or after completing the square): a constant over a quadratic or its square root, completed to a square for arctan or arcsin. BC-QA-06019 (research/question-analysis/question-archetypes.md#BC-QA-06019 Antiderivative found after splitting a fraction or expanding a product, and confirmed by differentiating): a product of two binomials or a fraction whose numerator is a sum, expanded or split into powers.

The signal is the shape of the integrand, read before any technique: compare the degrees of numerator and denominator; look for an expanded quadratic under a constant. Contrast pair on st-1: the this stem is on BC-QA-06016, an improper rational integrand; the not this stem is a proper fraction over distinct linear factors, the near miss from partial fractions (BC-CON-06018) that the rival method of the archetype, decomposing without dividing (BC-ERR-06026), invites. The separating feature is the degree comparison.

What says "not this concept": a constant multiple of an inner derivative multiplying a composite (substitution, BC-CON-06015), a proper fraction over distinct linear factors (partial fractions, BC-CON-06018), a product of unlike factors (parts, BC-CON-06017).

## Method choice

Two families load the skills, so two strategy blocks; st-1 both bands, st-2 low band.

- st-1, BC-QA-06016. Method, `expected_solution_path[0]`: inspect the integrand for structural markers, here the two degrees. Rival from `wrong_approaches`: decomposing an improper rational integrand without dividing first, cited in the block's `sources` (BC-ERR-06026), not in its text. Separating feature: numerator degree at least the denominator's. `evidence_tag` inferred: the cue comes from `asked_to_produce` and the spec notes, since `common_givens` names only the product form [inferred].
- st-2, BC-QA-06018. Method, `expected_solution_path[0]`: complete the square in the quadratic when it is expanded. Rival from `wrong_approaches`: forcing a logarithm by treating the quadratic as u without its derivative present. Separating feature: the numerator is a constant, not the quadratic's derivative.

## Solution path

- ex-1, BC-QA-06016, both bands, no calculator. Draw from `parameter_spec`: structure improper_rational, multiplier 2, rate 2, rate_sign 1, shift 2, constant 3; integrand 2(x^2 + 3)/(x + 2), derived remainder 7. No published BC-QA-06016 item carries this draw.
- There is no example 2, so nothing is faded and there is no `fade_from`.
- Steps follow `expected_solution_path`: inspect the degrees (no value); the integrand (new); the divided form 2x - 4 + 14/(x + 2) (equivalent); the antiderivative with C (integrate). The domain x > -2 lets ln(x + 2) stand for ln|x + 2| in the SymPy strings [inferred].

A fluent solver writes the divided form and the antiderivative; the degree comparison is held in the head [inferred].

## Scoring

None. BC-QA-06016, BC-QA-06018 and BC-QA-06019 carry no `point_types`, so no reader checklist and no point tag (plan 15, R14).

## Traps

All three active errors meeting the skills, in the bundle's order: BC-ERR-06022, BC-ERR-06026, BC-ERR-06033. Mid band shows the first two. All three wrong steps differ from the right step as expressions, so each block is a fix prompt (`fix_prompt` true). On ex-1's draw:

- err-BC-ERR-06022: numerator and 2/(x + 2) antidifferentiated apart and multiplied, against the divided form's antiderivative. Possible reason, words from BC-MIS-06019.
- err-BC-ERR-06026: the fraction split as A/(x + 2) with A = 14, losing the quotient 2x - 4. Possible reason, words from BC-MIS-06022.
- err-BC-ERR-06033: 2x - 4 raised to 2x^2 - 4x with no divisor. The linked BC-MIS-02009 describes derivatives, so no possible reason line.

## Representations

None. The topic's Representations paragraph names only BC-REP-01 to BC-REP-01 conversions.

## Prerequisite bridge

- BC-PRQ-06001 (splitting and factoring out constants), BC-PRQ-06002 (powers, never the exponent -1), BC-PRQ-06009 (long division), BC-PRQ-06010 (completing the square), each from its `description_plain` and `failure_signature`.

## Time

BC-QA-06016 is `no_calculator`, typically one part of a multipart free response question or a single multiple choice item, with no `point_types`; served as Section I Part A, 2.14 minutes per question (research/exam/exam-structure.md#Section and part layout) [inferred]. The minutes go on the division; the antiderivative is short.

## Checks

- chk-1, completion of ex-1, both bands: the divided form is given; key x^2 - 4x + 14 ln(x + 2) + C.
- chk-2, isomorph, both bands. Draw: improper_rational, multiplier 3, rate 1, rate_sign -1, shift -1, constant 2; 3(x^2 + 2)/(x - 1). Key 3x^2/2 + 3x + 9 ln(x - 1) + C.
- chk-3, MCQ, low band. Draw: improper_rational, multiplier 1, rate 3, rate_sign 1, shift 3, constant 1; (x^2 + 1)/(x + 3). Key x^2/2 - 3x + 10 ln(x + 3) + C. Distractors: 10 ln(x + 3) + C (BC-ERR-06026), x^2 - 3x + 10 ln(x + 3) + C (BC-ERR-06033), (x^3/3 + x) ln(x + 3) + C (BC-ERR-06022).

## Delivery

- orientation, ki-1: text. Rule 6: the skills carry BC-REP-01 alone, and the unit README delivery map puts the rearrangements in text and step reveal.
- ex-1 and the three error blocks: step_reveal. Rule 1.
- The prediction: text, on the key idea screen's resolution.
- No drawn block: none of rules 2 to 5 applies. The skills carry BC-REP-01 alone, which is not figure-bearing, and the key idea states a rewriting rule, not a process to draw. The machine record states `no_figure_reason`.

## Band plan

- Low (full), in served order: prediction, orientation, the four bridges, ki-1, st-1 with its contrast pair, st-2, ex-1, chk-1, err-BC-ERR-06022, err-BC-ERR-06026, err-BC-ERR-06033, chk-2, chk-3. 555 words, 3.7 minutes (cap 900 and 6). There is no example 2, so nothing is faded, and no scoring lines (no `point_types`).
- Mid (brief): prediction, orientation, the four bridges, ki-1, st-1 with its contrast pair, ex-1, chk-1, err-BC-ERR-06022, err-BC-ERR-06026, chk-2. 441 words, 3.0 minutes (cap 450 and 3). The orientation, cue, bridges and separating feature were shortened to fit; no quote or scoring tag was dropped (there was none).
- Refresher: ki-1, the three error blocks, ex-1.

## Sources

- BC-CON-06016; BC-SKL-06053, BC-SKL-06054, BC-SKL-06055, BC-SKL-06056; BC-EK-FUN-6D3; ced:127
- BC-QA-06016, BC-QA-06018, BC-QA-06019
- BC-ERR-06022, BC-ERR-06026, BC-ERR-06033; BC-MIS-06019, BC-MIS-06022
- BC-PRQ-06001, BC-PRQ-06002, BC-PRQ-06009, BC-PRQ-06010
- research/units/unit-06-integration-accumulation.md#6.10 Integrating Functions Using Long Division and Completing the Square
- research/question-analysis/question-archetypes.md#BC-QA-06016 Selecting an antidifferentiation technique from the form of the integrand
- research/question-analysis/question-archetypes.md#BC-QA-06018 Antiderivative matched to an inverse trigonometric form
- research/question-analysis/question-archetypes.md#BC-QA-06019 Antiderivative found after splitting a fraction or expanding a product
- research/exam/exam-structure.md#Section and part layout
- [inferred] st-1's cue from asked_to_produce and the spec notes. Settled by adding the rational form to BC-QA-06016 common_givens.
- [inferred] Section I Part A for BC-QA-06016. Settled by a rubric or item record fixing its shape.
- [inferred] ln(x + 2) for ln|x + 2| on x > -2. Settled by checker support for Abs.
- [inferred] Which steps a fluent solver holds in the head. Settled by timing data per step.

## Machine record

```json
{
 "id": "LSN-CON-06016",
 "kind": "concept",
 "target_id": "BC-CON-06016",
 "unit": "06",
 "skills": [
  "BC-SKL-06053",
  "BC-SKL-06054",
  "BC-SKL-06055",
  "BC-SKL-06056"
 ],
 "prediction": {
  "id": "pr-1",
  "stem": {
   "text": "\\(\\frac{2(x^2+3)}{x+2}\\) has numerator degree 2 over denominator degree 1. Which first step turns it into terms that can be antidifferentiated one at a time?",
   "command_verb": "predict"
  },
  "format": "mcq",
  "options": [
   {
    "id": "A",
    "label": "Split it as \\(\\frac{A}{x+2}\\) and solve for \\(A\\)",
    "is_key": false
   },
   {
    "id": "B",
    "label": "Divide, giving a polynomial plus a remainder over \\(x+2\\)",
    "is_key": true
   },
   {
    "id": "C",
    "label": "Antidifferentiate the numerator and denominator separately",
    "is_key": false
   }
  ],
  "resolution": "Degree 2 is at least degree 1, so division gives \\(2x-4+\\frac{14}{x+2}\\), and each term is basic. Decomposition needs a proper fraction.",
  "sources": [
   "BC-CON-06016",
   "research/units/unit-06-integration-accumulation.md#6.10 Integrating Functions Using Long Division and Completing the Square"
  ]
 },
 "no_figure_reason": "The skills carry only symbolic expressions and the key idea is a rewriting rule, not a process to draw, so no figure fits.",
 "orientation": {
  "text": "A response rewrites the integrand first, by division or completing the square, then antidifferentiates each piece.",
  "sources": [
   "BC-CON-06016",
   "research/units/unit-06-integration-accumulation.md#6.10 Integrating Functions Using Long Division and Completing the Square"
  ]
 },
 "key_ideas": [
  {
   "id": "ki-1",
   "ek_id": "BC-EK-FUN-6D3",
   "depth": "core",
   "text": "Rearrange before antidifferentiating. Numerator degree at least the denominator's: divide, giving a polynomial plus a proper remainder over the divisor, each piece basic. A quadratic denominator: complete the square to expose a logarithm or inverse tangent form.",
   "notation": "quotient plus remainder over divisor",
   "quote": {
    "text": "Techniques for finding antiderivatives include rearrangements into equivalent forms, such as long division and completing the square.",
    "source": "ced:127"
   },
   "sources": [
    "BC-EK-FUN-6D3",
    "ced:127",
    "research/units/unit-06-integration-accumulation.md#6.10 Integrating Functions Using Long Division and Completing the Square"
   ]
  }
 ],
 "strategy": [
  {
   "id": "st-1",
   "archetype_id": "BC-QA-06016",
   "cue": "A rational integrand with numerator degree at least the denominator's.",
   "method": "Inspect the integrand for structural markers: compare the degrees.",
   "rival": "Partial fractions straight away.",
   "separating_feature": "A degree at least the denominator's means divide first.",
   "sources": [
    "BC-QA-06016",
    "BC-ERR-06026"
   ],
   "evidence_tag": "inferred",
   "contrast": {
    "this": {
     "text": "Find \\(\\int \\frac{3(x^2+1)}{x+4}\\,dx\\) for \\(x>-4\\).",
     "archetype_id": "BC-QA-06016"
    },
    "not_this": {
     "text": "Find \\(\\int \\frac{5}{(x+1)(x+3)}\\,dx\\) for \\(x>-1\\).",
     "why_not": "A proper fraction over distinct linear factors calls for partial fractions, with no division."
    },
    "feature": "Numerator degree at least the denominator's: divide first."
   }
  },
  {
   "id": "st-2",
   "archetype_id": "BC-QA-06018",
   "cue": "A constant over an expanded quadratic or its square root; an antiderivative with C asked.",
   "method": "Complete the square in the quadratic when it is expanded.",
   "rival": "A logarithm with the quadratic as u.",
   "separating_feature": "The numerator is a constant, not the quadratic's derivative, so the square gives arctan or arcsin.",
   "sources": [
    "BC-QA-06018"
   ],
   "evidence_tag": "verified"
  }
 ],
 "worked_examples": [
  {
   "id": "ex-1",
   "archetype_id": "BC-QA-06016",
   "bands": [
    "low",
    "mid"
   ],
   "parameter_draw": {
    "structure": "improper_rational",
    "multiplier": 2,
    "rate": 2,
    "rate_sign": 1,
    "shift": 2,
    "constant": 3
   },
   "problem": {
    "text": "Find ∫ 2(x^2 + 3)/(x + 2) dx for x > -2.",
    "command_verb": "find"
   },
   "calculator_status": "no_calculator",
   "steps": [
    {
     "cue": "Numerator degree 2, denominator degree 1.",
     "why": "Improper rational: division comes before any other technique."
    },
    {
     "cue": "The integrand as given.",
     "why": "Divide it before antidifferentiating.",
     "expr": "2*(x**2 + 3)/(x + 2)",
     "relation": "new"
    },
    {
     "cue": "x^2 + 3 = (x + 2)(x - 2) + 7.",
     "why": "Quotient plus proper remainder over divisor.",
     "expr": "2*x - 4 + 14/(x + 2)",
     "relation": "equivalent"
    },
    {
     "cue": "2x - 4 by the power rule; 14/(x + 2) is derivative over function.",
     "why": "Each piece is basic; add C.",
     "expr": "x**2 - 4*x + 14*log(x + 2) + C",
     "relation": "integrate",
     "variable": "x"
    }
   ],
   "answer": {
    "form": "symbolic",
    "expr": "x**2 - 4*x + 14*log(x + 2) + C"
   }
  }
 ],
 "what_a_reader_scores": [],
 "common_errors": [
  {
   "error_id": "BC-ERR-06022",
   "observed_behavior": "The response antidifferentiates each factor of a product and multiplies the results.",
   "scoring_consequence": "Neither the u and dv point nor the expression point is earned (sg-23:18, sg-24:18).",
   "wrong_step": {
    "text": "Top and bottom antidifferentiated apart, multiplied.",
    "expr": "(x**3/3 + 3*x)*2*log(x + 2)"
   },
   "right_step": {
    "text": "Divided first.",
    "expr": "x**2 - 4*x + 14*log(x + 2) + C"
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
    "text": "Split as A/(x + 2): A = 14.",
    "expr": "14/(x + 2)"
   },
   "right_step": {
    "text": "Divided: 2x - 4 + 14/(x + 2).",
    "expr": "2*x - 4 + 14/(x + 2)"
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
   "error_id": "BC-ERR-06033",
   "observed_behavior": "The response raises each exponent by one but does not divide by the new exponent, or divides by the old exponent instead.",
   "scoring_consequence": "The proposed function does not differentiate to the integrand, so an antiderivative point is not earned.",
   "wrong_step": {
    "text": "2x - 4 to 2x^2 - 4x, no divisor.",
    "expr": "2*x**2 - 4*x + 14*log(x + 2) + C"
   },
   "right_step": {
    "text": "2x - 4 to x^2 - 4x.",
    "expr": "x**2 - 4*x + 14*log(x + 2) + C"
   },
   "relation": "distinct",
   "possible_reason": null,
   "sources": [
    "BC-ERR-06033"
   ],
   "fix_prompt": true
  }
 ],
 "representations": null,
 "prerequisite_bridges": [
  {
   "prq_id": "BC-PRQ-06001",
   "text": "Split fractions and factor out constants first."
  },
  {
   "prq_id": "BC-PRQ-06002",
   "text": "Rewrite radicals and reciprocals as powers."
  },
  {
   "prq_id": "BC-PRQ-06009",
   "text": "Long division gives a polynomial plus a proper remainder."
  },
  {
   "prq_id": "BC-PRQ-06010",
   "text": "Completing the square gives a square plus a constant."
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
   "archetype_id": "BC-QA-06016",
   "parameter_draw": {
    "structure": "improper_rational",
    "multiplier": 2,
    "rate": 2,
    "rate_sign": 1,
    "shift": 2,
    "constant": 3
   },
   "completes": "ex-1",
   "stem": {
    "text": "2(x^2 + 3)/(x + 2) = 2x - 4 + 14/(x + 2) for x > -2. Find the antiderivative.",
    "command_verb": "find"
   },
   "key": {
    "form": "symbolic",
    "expr": "x**2 - 4*x + 14*log(x + 2) + C"
   },
   "steps": [
    {
     "text": "Divided form.",
     "expr": "2*x - 4 + 14/(x + 2)",
     "relation": "new"
    },
    {
     "text": "Antidifferentiate each piece.",
     "expr": "x**2 - 4*x + 14*log(x + 2) + C",
     "relation": "integrate",
     "variable": "x"
    }
   ],
   "calculator_status": "no_calculator",
   "skills": [
    "BC-SKL-06053"
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
   "archetype_id": "BC-QA-06016",
   "parameter_draw": {
    "structure": "improper_rational",
    "multiplier": 3,
    "rate": 1,
    "rate_sign": -1,
    "shift": -1,
    "constant": 2
   },
   "stem": {
    "text": "Find ∫ 3(x^2 + 2)/(x - 1) dx for x > 1.",
    "command_verb": "find"
   },
   "key": {
    "form": "symbolic",
    "expr": "3*x**2/2 + 3*x + 9*log(x - 1) + C"
   },
   "steps": [
    {
     "text": "x^2 + 2 = (x - 1)(x + 1) + 3.",
     "expr": "3*x + 3 + 9/(x - 1)",
     "relation": "new"
    },
    {
     "text": "Antidifferentiate.",
     "expr": "3*x**2/2 + 3*x + 9*log(x - 1) + C",
     "relation": "integrate",
     "variable": "x"
    }
   ],
   "calculator_status": "no_calculator",
   "skills": [
    "BC-SKL-06053",
    "BC-SKL-06056"
   ]
  },
  {
   "id": "chk-3",
   "check_kind": "mcq",
   "format": "mcq",
   "bands": [
    "low"
   ],
   "archetype_id": "BC-QA-06016",
   "parameter_draw": {
    "structure": "improper_rational",
    "multiplier": 1,
    "rate": 3,
    "rate_sign": 1,
    "shift": 3,
    "constant": 1
   },
   "stem": {
    "text": "For x > -3, ∫ (x^2 + 1)/(x + 3) dx =",
    "command_verb": "identify"
   },
   "key": {
    "form": "symbolic",
    "expr": "x**2/2 - 3*x + 10*log(x + 3) + C"
   },
   "steps": [
    {
     "text": "x^2 + 1 = (x + 3)(x - 3) + 10.",
     "expr": "x - 3 + 10/(x + 3)",
     "relation": "new"
    },
    {
     "text": "Antidifferentiate.",
     "expr": "x**2/2 - 3*x + 10*log(x + 3) + C",
     "relation": "integrate",
     "variable": "x"
    }
   ],
   "options": [
    {
     "id": "A",
     "is_key": false,
     "expr": "10*log(x + 3) + C",
     "error_path": "BC-ERR-06026",
     "derivation": "split as A/(x + 3) with A = 10, the quotient lost"
    },
    {
     "id": "B",
     "is_key": true,
     "expr": "x**2/2 - 3*x + 10*log(x + 3) + C",
     "error_path": null
    },
    {
     "id": "C",
     "is_key": false,
     "expr": "x**2 - 3*x + 10*log(x + 3) + C",
     "error_path": "BC-ERR-06033",
     "derivation": "x raised to x^2 without dividing by 2"
    },
    {
     "id": "D",
     "is_key": false,
     "expr": "(x**3/3 + x)*log(x + 3) + C",
     "error_path": "BC-ERR-06022",
     "derivation": "numerator and 1/(x + 3) antidifferentiated apart and multiplied"
    }
   ],
   "calculator_status": "no_calculator",
   "skills": [
    "BC-SKL-06053",
    "BC-SKL-06056"
   ]
  }
 ],
 "delivery": [
  {
   "block": "orientation",
   "mode": "text",
   "reason": "rule 6: BC-REP-01 only on the concept's skills (unit README delivery map)",
   "sources": [
    "BC-SKL-06053"
   ]
  },
  {
   "block": "ki-1",
   "mode": "text",
   "reason": "rule 6: a rewriting rule with BC-REP-01 alone; no process, no figure-bearing representation",
   "sources": [
    "BC-SKL-06053",
    "BC-SKL-06054"
   ]
  },
  {
   "block": "ex-1",
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
   "block": "err-BC-ERR-06033",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  }
 ],
 "refresher": [
  "ki-1",
  "err-BC-ERR-06022",
  "err-BC-ERR-06026",
  "err-BC-ERR-06033",
  "ex-1"
 ],
 "research_lines": [
  {
   "file": "research/units/unit-06-integration-accumulation.md",
   "line": "Applied when the numerator degree is at least the denominator degree, producing a polynomial plus a proper remainder term."
  }
 ],
 "inferred": [
  {
   "claim": "st-1's cue rests on asked_to_produce and the parameter_spec notes (improper rational form), since BC-QA-06016's common_givens names only a product of a linear factor and a cosine.",
   "settles": "A library pass adding the improper rational integrand to BC-QA-06016 common_givens."
  },
  {
   "claim": "BC-QA-06016 is 'typically one part of a multipart free response question, or a single multiple choice item' with no point_types; the lesson takes Section I Part A, 2.14 minutes.",
   "settles": "A rubric or item record fixing the shape this archetype is served in."
  },
  {
   "claim": "SymPy strings write ln(x + 2) without absolute value; the problem restricts to x > -2 so the two agree, because the checker's integrate relation cannot differentiate Abs.",
   "settles": "Checker support for Abs under the integrate relation."
  },
  {
   "claim": "A fluent solver holds the degree comparison in the head and writes the divided form and the antiderivative.",
   "settles": "Timing data per step once the fluency telemetry exists."
  }
 ],
 "sources": [
  "BC-CON-06016",
  "BC-SKL-06053",
  "BC-SKL-06054",
  "BC-SKL-06055",
  "BC-SKL-06056",
  "BC-EK-FUN-6D3",
  "ced:127",
  "BC-QA-06016",
  "BC-QA-06018",
  "BC-QA-06019",
  "BC-ERR-06022",
  "BC-ERR-06026",
  "BC-ERR-06033",
  "BC-MIS-06019",
  "BC-MIS-06022",
  "BC-PRQ-06001",
  "BC-PRQ-06002",
  "BC-PRQ-06009",
  "BC-PRQ-06010",
  "research/units/unit-06-integration-accumulation.md#6.10 Integrating Functions Using Long Division and Completing the Square",
  "research/question-analysis/question-archetypes.md#BC-QA-06016 Selecting an antidifferentiation technique from the form of the integrand",
  "research/question-analysis/question-archetypes.md#BC-QA-06018 Antiderivative matched to an inverse trigonometric form",
  "research/question-analysis/question-archetypes.md#BC-QA-06019 Antiderivative found after splitting a fraction or expanding a product",
  "research/exam/exam-structure.md#Section and part layout"
 ],
 "read_minutes": {
  "full": 3.7,
  "brief": 3.0
 },
 "word_count": {
  "full": 554,
  "brief": 440
 }
}
```
