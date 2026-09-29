---
title: LSN-CON-06017 Integration by parts
research_date: 2026-09-29
status: designed
purpose: Authoring spec for the concept lesson on BC-CON-06017, antiderivatives and definite integrals of products by integration by parts, built from authoring_bundle("BC-CON-06017") and the research files it cites.
---

# LSN-CON-06017 Integration by parts

Concept BC-CON-06017 (skills BC-SKL-06057 to BC-SKL-06061), topic 6.11 of Unit 6, loaded by one archetype, BC-QA-06009 (family antidifferentiation-technique). Its hard parents are BC-CON-06012 and BC-CON-06014, with BC-TOP-0208 (the product rule) outside the unit (docs/lessons/unit-06/README.md, section 1).

## Orientation

Served text, from BC-CON-06017 `description_plain` and the topic's Assessment behaviour paragraph (research/units/unit-06-integration-accumulation.md#6.11 Integrating Using Integration by Parts): a response declares u and dv, writes uv minus the integral of v du, and finishes. No count, no frequency.

## Key ideas

All five skills map to BC-EK-FUN-6E1, so one core block, both bands.

- ki-1 (core), BC-EK-FUN-6E1, ced:128. Paraphrase of the Integration by parts and Definite form paragraphs of Required mathematical knowledge. No quote, to keep the brief band under cap. Notation line from the concept record.

## Recognition

BC-QA-06009 (research/question-analysis/question-archetypes.md#BC-QA-06009 Antiderivative by integration by parts). `typical_wording`: "find the indefinite integral of the given product, showing the work that leads to your answer"; "let h be defined as x times the derivative of an unknown function; find the value of the definite integral of h over the stated interval". `common_givens`: a product of a linear factor and a cosine, an unknown function with a stated endpoint value and a stated integral, a table of values of a function and its derivative. `asked_to_produce`: a choice of u and dv, the uv minus the integral of v du expression, an antiderivative with a constant, the value of a definite integral. Official examples: BC-FRQ-2023-Q5-C, BC-FRQ-2024-Q5-D, BC-MCQ-CED-016, BC-MCQ-PE2012-024.

The signal: two unlike factors multiplied, one a polynomial that differentiation reduces, with no factor that is the derivative of an inner expression. What says "not this concept": a composite times its inner derivative (substitution, BC-CON-06015); a rational function (division or partial fractions, BC-CON-06016, BC-CON-06018).

## Method choice

One strategy block, both bands.

- st-1, BC-QA-06009. Cue from `common_givens` and `asked_to_produce`. Method, `expected_solution_path[0]`: declare u and dv and compute du and v. Rival from `wrong_approaches`: antidifferentiating each factor and multiplying (BC-ERR-06022). Separating feature: no inner derivative pairs the factors, and a product's antiderivative is not the product of the antiderivatives. First written line: u = 3x, dv = cos 2x dx.

## Solution path

- ex-1, BC-QA-06009, both bands, no calculator. Draw from `parameter_spec`: multiplier 3, rate 2, variable x, reach 1, partner cosine, form definite; the integral of 3x cos 2x from 0 to π/6, where the boundary term is not zero. No published BC-QA-06009 item carries this draw.
- Steps follow `expected_solution_path`: u, dv, du, v (no value); uv minus the integral of v du (new, BC-PT-99057); the remaining integral finished (equivalent); limits applied (new); √3π/8 - 3/8 (equivalent, BC-PT-99004).

A fluent solver writes the expression, the finished antiderivative and the value; u and dv can be implied by the correct expression (`scoring_pattern`, sg-23:18) [inferred as to what is held].

## Scoring

BC-QA-06009 lists BC-PT-99056, BC-PT-99057 and BC-PT-99004. ex-1 tags BC-PT-99057 on the expression and BC-PT-99004 on the value; reader lines are `reader_checks` output copied exactly. BC-PT-99056 is not tagged, to keep the brief band under 450 words [inferred]. From `scoring_pattern`: the answer point is available only if the first two were earned, and the tabular arrangement is accepted (sg-23:18, sg-24:18). Parts with the wrong sign or pieces is an answer-point loss (research/scoring/common-point-losses.md#Answer points).

## Traps

All three active errors meeting the skills, in the bundle's order: BC-ERR-06022, BC-ERR-06023, BC-ERR-99025. Mid band shows the first two. On ex-1's draw:

- err-BC-ERR-06022: (3x^2/2)(sin 2x/2) against the parts antiderivative. Possible reason, words from BC-MIS-06019.
- err-BC-ERR-06023: uv plus the integral of v du, giving - (3/4) cos 2x, against + (3/4) cos 2x. No possible reason line.
- err-BC-ERR-99025: u and dv the wrong way round. The CAS finds the result equivalent: the identity holds, but the remaining integral of 3x^2 sin 2x is harder than the start, so the work stalls.

## Representations

None. The topic's conversions are symbolic to symbolic and verbal values to a number; nothing figure-shaped.

## Prerequisite bridge

- BC-PRQ-06005, from its `description_plain` (reading f, f' and values at an input) and `failure_signature` (f' and f interchanged).

## Time

BC-QA-06009 is `no_calculator`, typically one part of a multipart free response question; Section II Part B, 15.0 minutes per question (research/exam/exam-structure.md#Section and part layout). Its three points give a 5.0 minute share (unit README section 5). As a multiple choice item it takes the Part A 2.14. The minutes go on the remaining integral and the limits.

## Checks

- chk-1, completion of ex-1, both bands: the antiderivative is given; key √3π/8 - 3/8.
- chk-2, isomorph, both bands. Draw: multiplier 2, rate 3, variable t, reach 1, sine, definite; 2t sin 3t from 0 to π/9. Key √3/9 - π/27.
- chk-3, MCQ, low band. Draw: multiplier 4, rate 2, variable x, reach 1, exponential, definite; 4x e^(2x) from 0 to 1. Key e^2 + 1. Distractors: 3e^2 - 1 (BC-ERR-06023), e^2 (BC-ERR-06022), 1 - e^2 (BC-ERR-99025, boundary term dropped).

## Delivery

- orientation, ki-1: text. Rule 6: BC-REP-01 and BC-REP-04 only, and the unit README delivery map puts parts in text and step reveal.
- ex-1 and the three error blocks: step_reveal. Rule 1.

## Band plan

- Low (full): orientation, ki-1, st-1, ex-1 with its reader lines, three error blocks, chk-1 to chk-3, the bridge. 512 words, 3.5 minutes (cap 900 and 6).
- Mid (brief): orientation, ki-1, st-1, ex-1 with its reader lines, err-BC-ERR-06022, err-BC-ERR-06023, chk-1, chk-2, the bridge. 427 words, 2.9 minutes (cap 450 and 3).
- Refresher: ki-1, the three error blocks, ex-1.

## Sources

- BC-CON-06017; BC-SKL-06057, BC-SKL-06058, BC-SKL-06059, BC-SKL-06060, BC-SKL-06061; BC-EK-FUN-6E1; ced:128
- BC-QA-06009; BC-PT-99056, BC-PT-99057, BC-PT-99004; sg-23:18, sg-24:18
- BC-ERR-06022, BC-ERR-06023, BC-ERR-99025; BC-MIS-06019
- BC-PRQ-06005
- research/units/unit-06-integration-accumulation.md#6.11 Integrating Using Integration by Parts
- research/question-analysis/question-archetypes.md#BC-QA-06009 Antiderivative by integration by parts
- research/exam/exam-structure.md#Section and part layout
- research/scoring/common-point-losses.md#Answer points
- [inferred] BC-PT-99056 untagged for the brief cap. Settled by a cap or a shorter reader text.
- [inferred] What a fluent solver holds in the head. Settled by timing data per step.
- [inferred] The trigonometric upper limit π/(3 rate) at reach 1. Settled by a parameter_spec note.

## Machine record

```json
{
 "id": "LSN-CON-06017",
 "kind": "concept",
 "target_id": "BC-CON-06017",
 "unit": "06",
 "skills": [
  "BC-SKL-06057",
  "BC-SKL-06058",
  "BC-SKL-06059",
  "BC-SKL-06060",
  "BC-SKL-06061"
 ],
 "orientation": {
  "text": "Unlike factors multiplied, one simpler once differentiated: a response declares u and dv, writes uv minus ∫v du, and finishes.",
  "sources": [
   "BC-CON-06017",
   "research/units/unit-06-integration-accumulation.md#6.11 Integrating Using Integration by Parts"
  ]
 },
 "key_ideas": [
  {
   "id": "ki-1",
   "ek_id": "BC-EK-FUN-6E1",
   "depth": "core",
   "text": "The product rule read backwards: ∫u dv = uv - ∫v du. Pick u to simplify when differentiated, dv integrable. With limits, uv takes both limits and the remaining integral is subtracted.",
   "notation": "u, dv, du, v",
   "quote": null,
   "sources": [
    "BC-EK-FUN-6E1",
    "ced:128",
    "research/units/unit-06-integration-accumulation.md#6.11 Integrating Using Integration by Parts"
   ]
  }
 ],
 "strategy": [
  {
   "id": "st-1",
   "archetype_id": "BC-QA-06009",
   "cue": "A product of a linear factor and a cosine; u and dv, the expression, or a value asked.",
   "method": "Declare u and dv and compute du and v.",
   "rival": "Rival: antidifferentiating each factor and multiplying (BC-ERR-06022).",
   "separating_feature": "No inner derivative pairs the factors; a product's antiderivative is not a product of antiderivatives.",
   "sources": [
    "BC-QA-06009"
   ],
   "evidence_tag": "verified"
  }
 ],
 "worked_examples": [
  {
   "id": "ex-1",
   "archetype_id": "BC-QA-06009",
   "bands": [
    "low",
    "mid"
   ],
   "parameter_draw": {
    "multiplier": 3,
    "rate": 2,
    "variable": "x",
    "reach": 1,
    "partner": "cosine",
    "form": "definite"
   },
   "problem": {
    "text": "Evaluate ∫_0^(π/6) 3x cos(2x) dx.",
    "command_verb": "evaluate"
   },
   "calculator_status": "no_calculator",
   "steps": [
    {
     "cue": "3x differentiates to a constant; cos 2x integrates.",
     "why": "u = 3x, dv = cos 2x dx, du = 3 dx, v = (1/2) sin 2x."
    },
    {
     "cue": "Write uv minus the integral of v du.",
     "why": "Readers check the subtracted integral (sg-23:18).",
     "expr": "3*x*sin(2*x)/2 - Integral(3*sin(2*x)/2, x)",
     "relation": "new",
     "point_type_id": "BC-PT-99057"
    },
    {
     "cue": "(3/2) sin 2x integrates to -(3/4) cos 2x.",
     "why": "The minus in front turns it to plus.",
     "expr": "3*x*sin(2*x)/2 + 3*cos(2*x)/4",
     "relation": "equivalent"
    },
    {
     "cue": "Apply 0 and π/6 to both terms.",
     "why": "At 0 only the cosine term survives.",
     "expr": "(pi/4)*(sqrt(3)/2) + (3/4)*(1/2) - 3/4",
     "relation": "new"
    },
    {
     "cue": "Simplify.",
     "why": "The value.",
     "expr": "sqrt(3)*pi/8 - 3/8",
     "relation": "equivalent",
     "point_type_id": "BC-PT-99004"
    }
   ],
   "answer": {
    "form": "symbolic",
    "expr": "sqrt(3)*pi/8 - 3/8"
   }
  }
 ],
 "what_a_reader_scores": [
  {
   "example_id": "ex-1",
   "point_type_ids": [
    "BC-PT-99057",
    "BC-PT-99004"
   ],
   "lines": [
    {
     "point_type_id": "BC-PT-99057",
     "text": "Integration by parts expression uv minus the integral of v du. Earned by: The parts expression written out with the remaining integral (sg-23:18, sg-22:18). Not earned by: An expression missing the subtracted integral term (sg-24:18). Notation: sg-23:18 and sg-22:18 state limits of integration may be present, omitted, or partially present in the parts work."
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
   "error_id": "BC-ERR-06022",
   "observed_behavior": "The response antidifferentiates each factor of a product and multiplies the results.",
   "scoring_consequence": "Neither the u and dv point nor the expression point is earned (sg-23:18, sg-24:18).",
   "wrong_step": {
    "text": "Antiderivatives of 3x and cos 2x multiplied.",
    "expr": "(3*x**2/2)*(sin(2*x)/2)"
   },
   "right_step": {
    "text": "uv minus ∫v du.",
    "expr": "3*x*sin(2*x)/2 + 3*cos(2*x)/4"
   },
   "relation": "distinct",
   "possible_reason": {
    "misconception_id": "BC-MIS-06019",
    "text": "extends the sum rule to products"
   },
   "sources": [
    "BC-ERR-06022",
    "BC-MIS-06019"
   ]
  },
  {
   "error_id": "BC-ERR-06023",
   "observed_behavior": "The response writes u times v plus the integral of v du.",
   "scoring_consequence": "The expression point is not earned, and the answer point depends on it (sg-23:18).",
   "wrong_step": {
    "text": "uv plus ∫v du.",
    "expr": "3*x*sin(2*x)/2 - 3*cos(2*x)/4"
   },
   "right_step": {
    "text": "uv minus ∫v du.",
    "expr": "3*x*sin(2*x)/2 + 3*cos(2*x)/4"
   },
   "relation": "distinct",
   "possible_reason": null,
   "sources": [
    "BC-ERR-06023"
   ]
  },
  {
   "error_id": "BC-ERR-99025",
   "observed_behavior": "Responses add instead of subtract the second integral, choose u and dv the wrong way round, multiply two antiderivatives together, antidifferentiate the second factor incorrectly, or misplace the limits of integration between the uv term and the remaining integral.",
   "scoring_consequence": "The technique point and the evaluation point are separate, so an unlabelled or mis-signed application loses at least one of them.",
   "wrong_step": {
    "text": "u = cos 2x, dv = 3x dx: a harder integral left.",
    "expr": "3*x**2*cos(2*x)/2 + Integral(3*x**2*sin(2*x), x)"
   },
   "right_step": {
    "text": "u = 3x, dv = cos 2x dx.",
    "expr": "3*x*sin(2*x)/2 + 3*cos(2*x)/4"
   },
   "relation": "equivalent",
   "possible_reason": null,
   "sources": [
    "BC-ERR-99025"
   ]
  }
 ],
 "representations": null,
 "prerequisite_bridges": [
  {
   "prq_id": "BC-PRQ-06005",
   "text": "Keep f and f' apart when importing supplied values."
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
    5
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
   "archetype_id": "BC-QA-06009",
   "parameter_draw": {
    "multiplier": 3,
    "rate": 2,
    "variable": "x",
    "reach": 1,
    "partner": "cosine",
    "form": "definite"
   },
   "completes": "ex-1",
   "stem": {
    "text": "Evaluate [(3x/2) sin 2x + (3/4) cos 2x] from 0 to π/6.",
    "command_verb": "find"
   },
   "key": {
    "form": "symbolic",
    "expr": "sqrt(3)*pi/8 - 3/8"
   },
   "steps": [
    {
     "text": "Both limits.",
     "expr": "(pi/4)*(sqrt(3)/2) + (3/4)*(1/2) - 3/4",
     "relation": "new"
    },
    {
     "text": "Value.",
     "expr": "sqrt(3)*pi/8 - 3/8",
     "relation": "equivalent"
    }
   ],
   "calculator_status": "no_calculator",
   "skills": [
    "BC-SKL-06060"
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
   "archetype_id": "BC-QA-06009",
   "parameter_draw": {
    "multiplier": 2,
    "rate": 3,
    "variable": "t",
    "reach": 1,
    "partner": "sine",
    "form": "definite"
   },
   "stem": {
    "text": "Evaluate ∫_0^(π/9) 2t sin(3t) dt.",
    "command_verb": "evaluate"
   },
   "key": {
    "form": "symbolic",
    "expr": "sqrt(3)/9 - pi/27"
   },
   "steps": [
    {
     "text": "u = 2t, v = -(1/3) cos 3t.",
     "expr": "-2*t*cos(3*t)/3 + 2*sin(3*t)/9",
     "relation": "new"
    },
    {
     "text": "At π/9; the value at 0 is 0.",
     "expr": "sqrt(3)/9 - pi/27",
     "relation": "evaluate",
     "subs": {
      "t": "pi/9"
     }
    }
   ],
   "calculator_status": "no_calculator",
   "skills": [
    "BC-SKL-06057",
    "BC-SKL-06058",
    "BC-SKL-06060"
   ]
  },
  {
   "id": "chk-3",
   "check_kind": "mcq",
   "format": "mcq",
   "bands": [
    "low"
   ],
   "archetype_id": "BC-QA-06009",
   "parameter_draw": {
    "multiplier": 4,
    "rate": 2,
    "variable": "x",
    "reach": 1,
    "partner": "exponential",
    "form": "definite"
   },
   "stem": {
    "text": "∫_0^1 4x e^(2x) dx =",
    "command_verb": "identify"
   },
   "key": {
    "form": "symbolic",
    "expr": "exp(2) + 1"
   },
   "steps": [
    {
     "text": "u = 4x, v = (1/2) e^(2x).",
     "expr": "2*x*exp(2*x) - exp(2*x)",
     "relation": "new"
    },
    {
     "text": "At 1 minus at 0.",
     "expr": "2*exp(2) - exp(2) + 1",
     "relation": "new"
    },
    {
     "text": "Value.",
     "expr": "exp(2) + 1",
     "relation": "equivalent"
    }
   ],
   "options": [
    {
     "id": "A",
     "is_key": false,
     "expr": "3*exp(2) - 1",
     "error_path": "BC-ERR-06023",
     "derivation": "uv plus the integral of v du"
    },
    {
     "id": "B",
     "is_key": false,
     "expr": "exp(2)",
     "error_path": "BC-ERR-06022",
     "derivation": "2x^2 times (1/2) e^(2x), factors antidifferentiated apart"
    },
    {
     "id": "C",
     "is_key": true,
     "expr": "exp(2) + 1",
     "error_path": null
    },
    {
     "id": "D",
     "is_key": false,
     "expr": "1 - exp(2)",
     "error_path": "BC-ERR-99025",
     "derivation": "the uv boundary term dropped, only the remaining integral kept"
    }
   ],
   "calculator_status": "no_calculator",
   "skills": [
    "BC-SKL-06058",
    "BC-SKL-06060"
   ]
  }
 ],
 "delivery": [
  {
   "block": "orientation",
   "mode": "text",
   "reason": "rule 6: BC-REP-01 only on the archetype; a statement of what a response shows (unit README delivery map)",
   "sources": [
    "BC-SKL-06057"
   ]
  },
  {
   "block": "ki-1",
   "mode": "text",
   "reason": "rule 6: a symbolic rule with BC-REP-01 and BC-REP-04, neither figure-bearing",
   "sources": [
    "BC-SKL-06058",
    "BC-SKL-06061"
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
   "block": "err-BC-ERR-06023",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  },
  {
   "block": "err-BC-ERR-99025",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  }
 ],
 "refresher": [
  "ki-1",
  "err-BC-ERR-06022",
  "err-BC-ERR-06023",
  "err-BC-ERR-99025",
  "ex-1"
 ],
 "research_lines": [
  {
   "file": "research/units/unit-06-integration-accumulation.md",
   "line": "The boundary term u times v is evaluated at both limits and the remaining definite integral is subtracted."
  }
 ],
 "inferred": [
  {
   "claim": "BC-PT-99056 (choice of u and dv) is listed by BC-QA-06009 but not tagged on ex-1: its reader line would take the brief band past 450 words. The u and dv declaration sits in step 1's why line.",
   "settles": "A brief-band cap that admits a third reader line, or a shorter BC-PT-99056 reader text."
  },
  {
   "claim": "BC-QA-06009 is served as a no-calculator free-response part, Section II Part B; its three points give a 5.0 minute share of the 15.0 (unit README section 5).",
   "settles": "Timing data per step once the fluency telemetry exists."
  },
  {
   "claim": "A fluent solver holds the u and dv choice in the head when the expression implies it, and writes the expression, the remaining integral and the value.",
   "settles": "Timing data per step once the fluency telemetry exists."
  },
  {
   "claim": "The trigonometric definite form runs from 0 to pi/(3 rate) with reach 1, read from the parameter_spec notes and ITM-GEN-06009-06.",
   "settles": "A parameter_spec note stating how reach scales the trigonometric upper limit."
  }
 ],
 "sources": [
  "BC-CON-06017",
  "BC-SKL-06057",
  "BC-SKL-06058",
  "BC-SKL-06059",
  "BC-SKL-06060",
  "BC-SKL-06061",
  "BC-EK-FUN-6E1",
  "ced:128",
  "BC-QA-06009",
  "BC-PT-99056",
  "BC-PT-99057",
  "BC-PT-99004",
  "sg-23:18",
  "sg-24:18",
  "BC-ERR-06022",
  "BC-ERR-06023",
  "BC-ERR-99025",
  "BC-MIS-06019",
  "BC-PRQ-06005",
  "research/units/unit-06-integration-accumulation.md#6.11 Integrating Using Integration by Parts",
  "research/question-analysis/question-archetypes.md#BC-QA-06009 Antiderivative by integration by parts",
  "research/exam/exam-structure.md#Section and part layout",
  "research/scoring/common-point-losses.md#Answer points"
 ],
 "read_minutes": {
  "full": 3.5,
  "brief": 2.9
 },
 "word_count": {
  "full": 512,
  "brief": 427
 }
}
```
