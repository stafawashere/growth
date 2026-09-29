---
title: LSN-CON-06020 Selecting an antidifferentiation technique
research_date: 2026-09-29
status: designed
purpose: Authoring spec for the concept lesson on BC-CON-06020, choosing an antidifferentiation technique from the integrand's structure and ruling out techniques whose preconditions fail, built from authoring_bundle("BC-CON-06020") and the research files it cites.
---

# LSN-CON-06020 Selecting an antidifferentiation technique

Concept BC-CON-06020 (skills BC-SKL-06071 to BC-SKL-06074), topic 6.14 of Unit 6, loaded by one archetype, BC-QA-06016 (family procedure-selection), plan 15's technique-selection drill archetype. Its hard parents are BC-CON-06015 to BC-CON-06019, so it is last in the unit (docs/lessons/unit-06/README.md, section 1). It teaches the technique contrast that no printed confusable set holds (unit README section 3).

## Orientation

Served text, from BC-CON-06020 `description_plain` and the topic's Assessment behaviour paragraph (research/units/unit-06-integration-accumulation.md#6.14 Selecting Techniques for Antidifferentiation): an unsignalled integrand, the technique named from its structure and the rival ruled out, then the setup and the antiderivative. No count, no frequency.

## Key ideas

BC-SKL-06071 maps to BC-EK-FUN-6C2 and BC-EK-FUN-6D3, BC-SKL-06072 to FUN-6C2, BC-SKL-06073 to FUN-6D3, BC-SKL-06074 to FUN-6C3. Three blocks.

- ki-1 (core), BC-EK-FUN-6C2. Paraphrase of the Structural markers paragraph of Required mathematical knowledge. Anchor quote, 16 words, verbatim on ced:131.
- ki-2 (core), BC-EK-FUN-6D3. Rearrangement first, and chaining.
- ki-3 (extended), BC-EK-FUN-6C3. No closed form: a definite integral or a numerical value. Low band only [inferred].

## Recognition

BC-QA-06016 (research/question-analysis/question-archetypes.md#BC-QA-06016 Selecting an antidifferentiation technique from the form of the integrand). `typical_wording`: "find the indefinite integral, showing the work that leads to your answer". `asked_to_produce`: an indefinite integral with supporting work, the technique the integrand's structure calls for. `common_givens`: a product of a linear factor and a cosine. No official examples are listed. The topic's Assessment behaviour: MCQ forms ask which technique applies; FRQ forms present an unsignalled integrand and score the setup and the antiderivative separately (sg-24:18).

The signal is the absence of a named technique: "find the indefinite integral" with nothing else. The student reads the integrand's shape: a composite with its inner derivative (substitution), unlike factors multiplied (parts), numerator degree at least the denominator's (division), a proper fraction over distinct linears (partial fractions), an infinite limit or unbounded integrand (improper). A stem that names the technique or supplies u belongs to that technique's own lesson.

## Method choice

One strategy block, both bands.

- st-1, BC-QA-06016. Cue from `common_givens` and `asked_to_produce`. Method, `expected_solution_path[0]`: inspect the integrand for structural markers. Rival from `wrong_approaches`: substituting for an inner expression whose derivative is absent (BC-ERR-06020). Separating feature: the linear factor is not the derivative of the exponent, so parts, not substitution. The block teaches selection from the integrand's shape, as the unit README asks of BC-QA-06016.

## Solution path

- ex-1, BC-QA-06016, both bands, no calculator. Draw from `parameter_spec`: structure product, multiplier 3, rate 2, rate_sign -1, shift 1, constant 1; integrand 3x e^(-2x). Steps follow `expected_solution_path`: inspect (no value); rule out substitution (no value); parts expression (new); finished antiderivative (equivalent), with C named in the cue.
- ex-2, BC-QA-06016, low band only. Draw: structure improper_rational, multiplier 4, rate 1, rate_sign 1, shift -2, constant 5; integrand 4(x^2 + 5)/(x - 2), remainder 9. Steps: inspect (no value); integrand (new); divided form (equivalent); antiderivative with C (integrate). The two examples show the same inspection selecting two different techniques.

No published BC-QA-06016 item carries either draw. A fluent solver holds the inspection in the head and writes the first line of the chosen technique (unit README section 5) [inferred].

## Scoring

None. BC-QA-06016 carries no `point_types`, so no reader checklist and no point tag (plan 15, R14).

## Traps

Both active errors meeting the skills, in the bundle's order: BC-ERR-06020, BC-ERR-06022. Both bands show both. On ex-1's draw:

- err-BC-ERR-06020: u = -2x with 3x treated as a constant, against the parts result. Possible reason, words from BC-MIS-06017.
- err-BC-ERR-06022: (3x^2/2)(-(1/2)e^(-2x)), against the parts result. Possible reason, words from BC-MIS-06019.

## Representations

None. The topic's conversions go from a symbolic integrand to a named technique or a number; nothing figure-shaped.

## Prerequisite bridge

- BC-PRQ-06001, from its `description_plain` (rewriting to expose an inner function and its derivative) and `failure_signature` (term-by-term antidifferentiation).

## Time

BC-QA-06016 is `no_calculator`, typically one part of a multipart free response question or a single multiple choice item, with no `point_types`; Section I Part A, 2.14 minutes per question (research/exam/exam-structure.md#Section and part layout) [inferred]. The inspection costs seconds; the minutes go on the chosen technique.

## Checks

- chk-1, completion of ex-1, both bands: the parts expression is given; key -(3x/2)e^(-2x) - (3/4)e^(-2x).
- chk-2, isomorph, both bands. Draw: product, multiplier 2, rate 3, rate_sign 1, shift -2, constant 4; 2x e^(3x). Key (2x/3)e^(3x) - (2/9)e^(3x).
- chk-3, MCQ, low band, statement key naming the technique's first line. Draw: product, multiplier 5, rate 1, rate_sign -1, shift 3, constant 2; 5x e^(-x). Key u = 5x, dv = e^(-x) dx. Distractors: u = -x with 5x left (BC-ERR-06020), the factors antidifferentiated and multiplied (BC-ERR-06022), u = 5x as a substitution (BC-ERR-06020).

## Delivery

- orientation, ki-1, ki-2, ki-3: text. Rule 6: BC-REP-01 on BC-SKL-06071 to 06073, and BC-REP-09 on BC-SKL-06074 is not figure-bearing (unit README delivery map).
- ex-1, ex-2 and the two error blocks: step_reveal. Rule 1.

## Band plan

- Low (full): orientation, ki-1, ki-2, ki-3, st-1, ex-1, ex-2, two error blocks, chk-1 to chk-3, the bridge. 471 words, 3.2 minutes (cap 900 and 6).
- Mid (brief): orientation, ki-1, ki-2, st-1, ex-1, both error blocks, chk-1, chk-2, the bridge. 353 words, 2.4 minutes (cap 450 and 3).
- Refresher: ki-1, ki-2, both error blocks, ex-1.

## Sources

- BC-CON-06020; BC-SKL-06071, BC-SKL-06072, BC-SKL-06073, BC-SKL-06074; BC-EK-FUN-6C2, BC-EK-FUN-6D3, BC-EK-FUN-6C3; ced:131
- BC-QA-06016; sg-24:18
- BC-ERR-06020, BC-ERR-06022; BC-MIS-06017, BC-MIS-06019, BC-MIS-06022
- BC-PRQ-06001
- research/units/unit-06-integration-accumulation.md#6.14 Selecting Techniques for Antidifferentiation
- research/question-analysis/question-archetypes.md#BC-QA-06016 Selecting an antidifferentiation technique from the form of the integrand
- research/exam/exam-structure.md#Section and part layout
- [inferred] Section I Part A for BC-QA-06016. Settled by a rubric or item record fixing its shape.
- [inferred] No quote from ced:125. Settled by adding ced:125 to the concept's ced sources.
- [inferred] ki-3 extended with no example. Settled by a nonelementary structure value in parameter_spec.
- [inferred] ln(x - 2) without bars on x > 2. Settled by checker support for Abs.
- [inferred] What a fluent solver holds in the head. Settled by timing data per step.

## Machine record

```json
{
 "id": "LSN-CON-06020",
 "kind": "concept",
 "target_id": "BC-CON-06020",
 "unit": "06",
 "skills": [
  "BC-SKL-06071",
  "BC-SKL-06072",
  "BC-SKL-06073",
  "BC-SKL-06074"
 ],
 "orientation": {
  "text": "When no technique is named, the integrand's structure picks one. A response names the marker, rules out the techniques whose preconditions fail, then writes the chosen technique's first line.",
  "sources": [
   "BC-CON-06020",
   "research/units/unit-06-integration-accumulation.md#6.14 Selecting Techniques for Antidifferentiation"
  ]
 },
 "key_ideas": [
  {
   "id": "ki-1",
   "ek_id": "BC-EK-FUN-6C2",
   "depth": "core",
   "text": "Each technique reverses a derivative rule and has a precondition. A composite with its inner derivative present selects substitution; a product of unlike factors, parts; a proper fraction over distinct linear factors, partial fractions.",
   "notation": "technique classification",
   "quote": {
    "text": "This topic is intended to focus on the skill of selecting an appropriate procedure for antidifferentiation.",
    "source": "ced:131"
   },
   "sources": [
    "BC-EK-FUN-6C2",
    "ced:131",
    "research/units/unit-06-integration-accumulation.md#6.14 Selecting Techniques for Antidifferentiation"
   ]
  },
  {
   "id": "ki-2",
   "ek_id": "BC-EK-FUN-6D3",
   "depth": "core",
   "text": "Some integrands need a rearrangement first: numerator degree at least the denominator's selects long division, and a technique may leave a second integral that needs another.",
   "notation": "chained techniques",
   "quote": null,
   "sources": [
    "BC-EK-FUN-6D3",
    "ced:131",
    "research/units/unit-06-integration-accumulation.md#6.14 Selecting Techniques for Antidifferentiation"
   ]
  },
  {
   "id": "ki-3",
   "ek_id": "BC-EK-FUN-6C3",
   "depth": "extended",
   "text": "Some integrands have no closed-form antiderivative; the answer then stays a definite integral or a numerical value.",
   "notation": "integral or numerical representation",
   "quote": null,
   "sources": [
    "BC-EK-FUN-6C3",
    "research/units/unit-06-integration-accumulation.md#6.14 Selecting Techniques for Antidifferentiation"
   ]
  }
 ],
 "strategy": [
  {
   "id": "st-1",
   "archetype_id": "BC-QA-06016",
   "cue": "An unsignalled integrand, a product of a linear factor and a transcendental factor; an indefinite integral asked.",
   "method": "Inspect the integrand for structural markers.",
   "rival": "Rival: substituting for the exponent although its derivative is not the other factor (BC-ERR-06020).",
   "separating_feature": "The linear factor is not the inner derivative, so parts, not substitution.",
   "sources": [
    "BC-QA-06016"
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
    "structure": "product",
    "multiplier": 3,
    "rate": 2,
    "rate_sign": -1,
    "shift": 1,
    "constant": 1
   },
   "problem": {
    "text": "Find ∫ 3x e^(-2x) dx.",
    "command_verb": "find"
   },
   "calculator_status": "no_calculator",
   "steps": [
    {
     "cue": "A linear factor times an exponential.",
     "why": "Marker: a product of unlike factors."
    },
    {
     "cue": "Substitution u = -2x needs the other factor constant; 3x is not.",
     "why": "Precondition fails: substitution is ruled out."
    },
    {
     "cue": "Parts: u = 3x, dv = e^(-2x) dx, v = -(1/2) e^(-2x).",
     "why": "3x differentiates to a constant.",
     "expr": "-3*x*exp(-2*x)/2 + Integral(3*exp(-2*x)/2, x)",
     "relation": "new"
    },
    {
     "cue": "The remaining integral is basic.",
     "why": "Finish, then add C.",
     "expr": "-3*x*exp(-2*x)/2 - 3*exp(-2*x)/4",
     "relation": "equivalent"
    }
   ],
   "answer": {
    "form": "symbolic",
    "expr": "-3*x*exp(-2*x)/2 - 3*exp(-2*x)/4"
   }
  },
  {
   "id": "ex-2",
   "archetype_id": "BC-QA-06016",
   "bands": [
    "low"
   ],
   "parameter_draw": {
    "structure": "improper_rational",
    "multiplier": 4,
    "rate": 1,
    "rate_sign": 1,
    "shift": -2,
    "constant": 5
   },
   "problem": {
    "text": "Find ∫ 4(x^2 + 5)/(x - 2) dx for x > 2.",
    "command_verb": "find"
   },
   "calculator_status": "no_calculator",
   "steps": [
    {
     "cue": "Numerator degree 2 over degree 1.",
     "why": "Marker: improper rational, so long division first."
    },
    {
     "cue": "The integrand as given.",
     "why": "Divide before any other technique.",
     "expr": "4*(x**2 + 5)/(x - 2)",
     "relation": "new"
    },
    {
     "cue": "x^2 + 5 = (x - 2)(x + 2) + 9.",
     "why": "Quotient plus remainder over divisor.",
     "expr": "4*x + 8 + 36/(x - 2)",
     "relation": "equivalent"
    },
    {
     "cue": "Each piece is basic.",
     "why": "Power rule and ln; add C.",
     "expr": "2*x**2 + 8*x + 36*log(x - 2) + C",
     "relation": "integrate",
     "variable": "x"
    }
   ],
   "answer": {
    "form": "symbolic",
    "expr": "2*x**2 + 8*x + 36*log(x - 2) + C"
   }
  }
 ],
 "what_a_reader_scores": [],
 "common_errors": [
  {
   "error_id": "BC-ERR-06020",
   "observed_behavior": "A composite is substituted although no constant multiple of the derivative of the inner expression appears in the integrand.",
   "scoring_consequence": "The setup point for the technique is not earned and the work does not lead to the antiderivative.",
   "wrong_step": {
    "text": "u = -2x, the 3x treated as constant.",
    "expr": "-3*x*exp(-2*x)/2"
   },
   "right_step": {
    "text": "Parts.",
    "expr": "-3*x*exp(-2*x)/2 - 3*exp(-2*x)/4"
   },
   "relation": "distinct",
   "possible_reason": {
    "misconception_id": "BC-MIS-06017",
    "text": "selects substitution from the presence of an inner function alone"
   },
   "sources": [
    "BC-ERR-06020",
    "BC-MIS-06017"
   ]
  },
  {
   "error_id": "BC-ERR-06022",
   "observed_behavior": "The response antidifferentiates each factor of a product and multiplies the results.",
   "scoring_consequence": "Neither the u and dv point nor the expression point is earned (sg-23:18, sg-24:18).",
   "wrong_step": {
    "text": "Antiderivatives of 3x and e^(-2x) multiplied.",
    "expr": "-3*x**2*exp(-2*x)/4"
   },
   "right_step": {
    "text": "Parts.",
    "expr": "-3*x*exp(-2*x)/2 - 3*exp(-2*x)/4"
   },
   "relation": "distinct",
   "possible_reason": {
    "misconception_id": "BC-MIS-06019",
    "text": "each factor is antidifferentiated on its own"
   },
   "sources": [
    "BC-ERR-06022",
    "BC-MIS-06019"
   ]
  }
 ],
 "representations": null,
 "prerequisite_bridges": [
  {
   "prq_id": "BC-PRQ-06001",
   "text": "Rewrite first: factor out constants and split fractions, so a composite's inner derivative shows or is seen to be absent."
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
   ],
   "ex-2": [
    3,
    4
   ]
  },
  "skipped_steps": {
   "ex-1": [
    1,
    2
   ],
   "ex-2": [
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
    "structure": "product",
    "multiplier": 3,
    "rate": 2,
    "rate_sign": -1,
    "shift": 1,
    "constant": 1
   },
   "completes": "ex-1",
   "stem": {
    "text": "∫ 3x e^(-2x) dx = -(3x/2) e^(-2x) + ∫ (3/2) e^(-2x) dx. Finish.",
    "command_verb": "find"
   },
   "key": {
    "form": "symbolic",
    "expr": "-3*x*exp(-2*x)/2 - 3*exp(-2*x)/4"
   },
   "steps": [
    {
     "text": "Parts expression.",
     "expr": "-3*x*exp(-2*x)/2 + Integral(3*exp(-2*x)/2, x)",
     "relation": "new"
    },
    {
     "text": "Remaining integral.",
     "expr": "-3*x*exp(-2*x)/2 - 3*exp(-2*x)/4",
     "relation": "equivalent"
    }
   ],
   "calculator_status": "no_calculator",
   "skills": [
    "BC-SKL-06071",
    "BC-SKL-06073"
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
    "structure": "product",
    "multiplier": 2,
    "rate": 3,
    "rate_sign": 1,
    "shift": -2,
    "constant": 4
   },
   "stem": {
    "text": "Find ∫ 2x e^(3x) dx.",
    "command_verb": "find"
   },
   "key": {
    "form": "symbolic",
    "expr": "2*x*exp(3*x)/3 - 2*exp(3*x)/9"
   },
   "steps": [
    {
     "text": "Parts, u = 2x, v = (1/3) e^(3x).",
     "expr": "2*x*exp(3*x)/3 - Integral(2*exp(3*x)/3, x)",
     "relation": "new"
    },
    {
     "text": "Remaining integral.",
     "expr": "2*x*exp(3*x)/3 - 2*exp(3*x)/9",
     "relation": "equivalent"
    }
   ],
   "calculator_status": "no_calculator",
   "skills": [
    "BC-SKL-06071",
    "BC-SKL-06072"
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
    "structure": "product",
    "multiplier": 5,
    "rate": 1,
    "rate_sign": -1,
    "shift": 3,
    "constant": 2
   },
   "stem": {
    "text": "The first line for ∫ 5x e^(-x) dx is",
    "command_verb": "identify"
   },
   "key": {
    "form": "statement",
    "expr": "integration by parts, u = 5x, dv = e^(-x) dx"
   },
   "options": [
    {
     "id": "A",
     "is_key": false,
     "label": "u = -x, du = -dx, then 5x e^u (-du)",
     "error_path": "BC-ERR-06020",
     "derivation": "substitution for the exponent with the 5x left behind"
    },
    {
     "id": "B",
     "is_key": false,
     "label": "(5x^2/2)(-e^(-x))",
     "error_path": "BC-ERR-06022",
     "derivation": "each factor antidifferentiated and multiplied"
    },
    {
     "id": "C",
     "is_key": true,
     "label": "u = 5x, dv = e^(-x) dx"
    },
    {
     "id": "D",
     "is_key": false,
     "label": "u = 5x, du = 5 dx, then e^(-x) du/5",
     "error_path": "BC-ERR-06020",
     "derivation": "substitution for the linear factor, whose derivative is not the other factor"
    }
   ],
   "calculator_status": "no_calculator",
   "skills": [
    "BC-SKL-06071",
    "BC-SKL-06072"
   ]
  }
 ],
 "delivery": [
  {
   "block": "orientation",
   "mode": "text",
   "reason": "rule 6: BC-REP-01 only on BC-SKL-06071 to 06073 (unit README delivery map)",
   "sources": [
    "BC-SKL-06071"
   ]
  },
  {
   "block": "ki-1",
   "mode": "text",
   "reason": "rule 6: a classification by structure with BC-REP-01 alone",
   "sources": [
    "BC-SKL-06071",
    "BC-SKL-06072"
   ]
  },
  {
   "block": "ki-2",
   "mode": "text",
   "reason": "rule 6: a rewriting rule with BC-REP-01 alone",
   "sources": [
    "BC-SKL-06073"
   ]
  },
  {
   "block": "ki-3",
   "mode": "text",
   "reason": "rule 6: BC-REP-09 on BC-SKL-06074 is not figure-bearing",
   "sources": [
    "BC-SKL-06074"
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
   "block": "err-BC-ERR-06020",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  },
  {
   "block": "err-BC-ERR-06022",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  }
 ],
 "refresher": [
  "ki-1",
  "ki-2",
  "err-BC-ERR-06020",
  "err-BC-ERR-06022",
  "ex-1"
 ],
 "research_lines": [
  {
   "file": "research/units/unit-06-integration-accumulation.md",
   "line": "A composite with its inner derivative present selects substitution; a product of unlike factors selects integration by parts; a numerator degree at least the denominator degree selects long division; a factorable nonrepeating linear denominator selects partial fractions"
  }
 ],
 "inferred": [
  {
   "claim": "BC-QA-06016 is 'typically one part of a multipart free response question, or a single multiple choice item' with no point_types; the lesson takes Section I Part A, 2.14 minutes (unit README section 5).",
   "settles": "A rubric or item record fixing the shape this archetype is served in."
  },
  {
   "claim": "ki-1 (BC-EK-FUN-6C2) and ki-2 (BC-EK-FUN-6D3) carry the ced:131 framing; the EK sentences for FUN-6C2 and FUN-6C3 sit on ced:125, which the bundle's ced_pages for BC-CON-06020 do not hold, so no quote is taken from them.",
   "settles": "Adding ced:125 to the concept's ced sources."
  },
  {
   "claim": "ki-3 (BC-EK-FUN-6C3) is extended, low band only, and no example draws a nonelementary integrand, since BC-QA-06016's parameter_spec generates only the product and improper rational forms.",
   "settles": "A BC-QA-06016 structure value for an integrand with no closed-form antiderivative."
  },
  {
   "claim": "SymPy strings in ex-2 write ln(x - 2) without bars; the problem restricts to x > 2.",
   "settles": "Checker support for Abs under the integrate relation."
  },
  {
   "claim": "A fluent solver holds the marker inspection and ruling out in the head and writes the chosen technique's first line and the result.",
   "settles": "Timing data per step once the fluency telemetry exists."
  }
 ],
 "sources": [
  "BC-CON-06020",
  "BC-SKL-06071",
  "BC-SKL-06072",
  "BC-SKL-06073",
  "BC-SKL-06074",
  "BC-EK-FUN-6C2",
  "BC-EK-FUN-6D3",
  "BC-EK-FUN-6C3",
  "ced:131",
  "BC-QA-06016",
  "sg-24:18",
  "BC-ERR-06020",
  "BC-ERR-06022",
  "BC-MIS-06017",
  "BC-MIS-06019",
  "BC-MIS-06022",
  "BC-PRQ-06001",
  "research/units/unit-06-integration-accumulation.md#6.14 Selecting Techniques for Antidifferentiation",
  "research/question-analysis/question-archetypes.md#BC-QA-06016 Selecting an antidifferentiation technique from the form of the integrand",
  "research/exam/exam-structure.md#Section and part layout"
 ],
 "read_minutes": {
  "full": 3.2,
  "brief": 2.4
 },
 "word_count": {
  "full": 471,
  "brief": 353
 }
}
```
