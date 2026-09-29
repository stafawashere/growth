---
title: LSN-CON-06015 Substitution of variables
research_date: 2026-09-29
status: designed
purpose: Authoring spec for the concept lesson on BC-CON-06015, antiderivatives and definite integrals by substitution with the differential and the limits converted, built from authoring_bundle("BC-CON-06015") and the research files it cites.
---

# LSN-CON-06015 Substitution of variables

Concept BC-CON-06015 (skills BC-SKL-06047 to BC-SKL-06052), topic 6.9 of Unit 6, loaded by BC-QA-06008 (primary) and BC-QA-06018, both family antidifferentiation-technique. It has no Unit 6 hard parent; its outside parent is BC-SKL-03002 (docs/lessons/unit-06/README.md, section 1).

## Prediction

Multiple choice on ex-1's substitution, tagged [inferred] (the record carries no pretest). Stem: with u = x^2 + 1, 6x dx equals which multiple of du. Options 2 du, 3 du (the key), 6 du, the last being the BC-ERR-06019 move. The resolution says du = 2x dx, so 6x dx = 3 du, with no verdict word. Source: BC-CON-06015 and the topic section 6.9 the key idea cites.

## Orientation

Served text, from BC-CON-06015 `description_plain` and the topic's Assessment behaviour paragraph (research/units/unit-06-integration-accumulation.md#6.9 Integrating Using Substitution): a response names u and du, rewrites the integral in u and converts the limits. No count, no frequency. Cut to hold the brief cap.

## Key ideas

Skills BC-SKL-06047, 06048, 06049 and 06052 map to BC-EK-FUN-6D1; BC-SKL-06050 and 06051 map to BC-EK-FUN-6D2. Two blocks.

- ki-1 (core), BC-EK-FUN-6D1, ced:126. Paraphrase of the Substitution paragraph of Required mathematical knowledge: u = g(x), du = g'(x) dx, and the integral of f(g(x)) g'(x) dx equals the integral of f(u) du. No quote, to keep the brief band under its cap. Notation line from the concept record.
- ki-2 (extended), BC-EK-FUN-6D2, ced:126. Paraphrase of the Definite integrals paragraph: limits change with the variable, or back-substitute first. Anchor quote, 15 words, verbatim on ced:126. Served low band only [inferred]; the mid band meets the conversion in ex-1 step 2 and err-BC-ERR-06018.

## Recognition

BC-QA-06008 (research/question-analysis/question-archetypes.md#BC-QA-06008 Antiderivative or definite integral by substitution). `typical_wording`: "find the indefinite integral of the given composite expression, showing the work that leads to your answer"; "evaluate the definite integral of the given expression over the stated interval". `common_givens`: an explicit composite integrand, the limits of integration, a stated substitution. `asked_to_produce`: an antiderivative with supporting work, the value of a definite integral, a definite integral rewritten in the substituted variable, the area of a region. Official examples: BC-FRQ-2021-Q3-A, BC-FRQ-2026-Q5-A, BC-MCQ-CED-008, BC-MCQ-PE2012-006, BC-MCQ-PE2012-010.

BC-QA-06018 (research/question-analysis/question-archetypes.md#BC-QA-06018 Antiderivative matched to an inverse trigonometric form, directly or after completing the square) loads BC-SKL-06047 and 06048: a constant over a quadratic, where the substitution is u = x + h after completing the square and the scaling constant is carried.

The signal: a function inside another function, and outside it a factor that is a constant multiple of the inner derivative. What says "not this concept": a product of unlike factors with no inner derivative present (parts, BC-CON-06017), a rational integrand with factorable denominator and constant numerator (partial fractions, BC-CON-06018), a numerator degree at least the denominator's (long division, BC-CON-06016).

The near miss in the contrast pair comes from the sibling concept BC-CON-06017 and the `wrong_approaches` entry of BC-QA-06008: x cos x is a product of unlike factors with no inner derivative present, where 2x cos(x^2) has the derivative of the inner expression as a factor.

## Method choice

One strategy block, both bands, since both archetypes share the family antidifferentiation-technique.

- st-1, BC-QA-06008. Cue from `common_givens` and `asked_to_produce`. Method, `expected_solution_path[0]`: choose u as the inner expression. Rival from `wrong_approaches`: substituting for an inner expression whose derivative does not appear (BC-ERR-06020). Separating feature: a constant multiple of g'(x) multiplies f(g(x)). The first written line is u = g(x), du = g'(x) dx.

Contrast pair on st-1 (new on 2026-09-29): this is a composite with its inner derivative present on BC-QA-06008; not this is a product of unlike factors, integration by parts (topic 6.11 section, cited in st-1's sources); the feature is a multiple of the inner derivative as a factor. Strategy fields, ki-1, the orientation and the bridges are shortened to hold the brief cap. No scoring tag or anchor quote was dropped.

## Solution path

- ex-1, BC-QA-06008, both bands, no calculator. Draw from `parameter_spec`: inner_power 2, inner_scale 1, inner_shift 1, multiplier 6, outer_power 3, upper 1, outer power, form definite; integrand 6x(x^2 + 1)^3 on [0, 1], constant adjustment 6/2 = 3. No published BC-QA-06008 item carries this draw.
- Steps follow `expected_solution_path`: choose u (no value); du and the constant with converted limits, 3u^3 (new); antiderivative 3u^4/4 (integrate in u, BC-PT-99003); u limits applied (new); 45/4 (equivalent, BC-PT-99004).

A fluent solver writes du with the constant, the integral in u with its limits, the antiderivative and the value; the choice of u is held in the head [inferred].

## Scoring

BC-QA-06008 lists BC-PT-99002, BC-PT-99003 and BC-PT-99004; ex-1 tags BC-PT-99003 on the antiderivative and BC-PT-99004 on the value, and the reader lines are `reader_checks` output copied exactly. BC-PT-99002 (integrand only) belongs to area parts and is not tagged. From `scoring_pattern`: original limits applied to an expression still in u make the response ineligible for the answer point even when the value is right (sg-23:17, sg-23:16). The loss sits with answer points (research/scoring/common-point-losses.md#Answer points).

## Traps

All four active errors meeting the skills, in the bundle's order: BC-ERR-06018, BC-ERR-06019, BC-ERR-06020, BC-ERR-07026. Mid band shows the first two. On ex-1's draw:

- err-BC-ERR-06018: the u antiderivative at x = 0, 1 (3/4) against u = 1, 2 (45/4). Possible reason, words from BC-MIS-06016.
- err-BC-ERR-06019: 6x dx read as 6 du, 6u^4/4, against 3u^4/4. No possible reason line, to keep the brief band under cap.
- err-BC-ERR-06020: dx replaced by du with the 6x left, against 3u^3 [inferred: the draw has its inner derivative present]. Possible reason, words from BC-MIS-06017.
- err-BC-ERR-07026: the indefinite antiderivative 3(x^2 + 1)^4/4 with no constant, against + C [inferred]. Possible reason, words from BC-MIS-06018.

## Representations

None. The topic's Representations paragraph names only BC-REP-01 to BC-REP-01 conversions.

## Prerequisite bridge

- BC-PRQ-06001, from its `description_plain` (factor constants out to expose the inner derivative) and `failure_signature` (term-by-term antidifferentiation of a composite).
- BC-PRQ-06003, from its `description_plain` (absolute value inside ln) and `failure_signature` (ln of a negative quantity).

## Time

BC-QA-06008 is `no_calculator`, typically one part of a multipart free response question or a single multiple choice item; served as the free-response part, Section II Part B, 15.0 minutes per question (research/exam/exam-structure.md#Section and part layout). The part's share is set by points that `scoring_pattern` does not count [inferred; unit README section 5]; as a multiple choice item it takes the Part A 2.14. The minutes go on du with its constant and the converted limits.

## Checks

- chk-1, completion of ex-1, both bands: the integral in u is given; key 45/4.
- chk-2, isomorph, both bands. Draw: inner_power 3, inner_scale 1, inner_shift 2, multiplier 6, outer_power 2, upper 1, power, definite; 6x^2(x^3 + 2)^2 on [0, 1]. Key 38/3.
- chk-3, MCQ, low band. Draw: inner_power 2, inner_scale 1, inner_shift 3, multiplier 4, outer_power 2, upper 1, power, definite; 4x(x^2 + 3)^2 on [0, 1]. Key 74/3. Distractors: 2/3 (BC-ERR-06018, x limits), 148/3 (BC-ERR-06019, 1/2 dropped), 128/3 (BC-ERR-06018, lower x limit kept).

## Delivery

- orientation, ki-1, ki-2: text. Rule 6: the skills carry BC-REP-01 alone, and the unit README delivery map puts the antidifferentiation techniques in text and step reveal.
- ex-1 and the four error blocks: step_reveal. Rule 1.
- No drawn block: `no_figure_reason` states that the skills carry symbolic representations only and no key idea describes a process, so none of rules 2 to 5 applies.

## Band plan

- Low (full): prediction, orientation, both bridges, ki-1, ki-2, st-1 with its contrast, ex-1 with its reader lines, chk-1, four error blocks, chk-2, chk-3. 611 words, 4.2 minutes (cap 900 and 6).
- Mid (brief): prediction, orientation, both bridges, ki-1, st-1 with its contrast, ex-1 with its reader lines, chk-1, err-BC-ERR-06018, err-BC-ERR-06019, chk-2. 447 words, 3.0 minutes (cap 450 and 3).
- Refresher: ki-1, the four error blocks, ex-1.

## Sources

- BC-CON-06015; BC-SKL-06047, BC-SKL-06048, BC-SKL-06049, BC-SKL-06050, BC-SKL-06051, BC-SKL-06052; BC-EK-FUN-6D1, BC-EK-FUN-6D2; ced:126
- BC-QA-06008, BC-QA-06018; BC-PT-99002, BC-PT-99003, BC-PT-99004; sg-23:16, sg-23:17
- BC-ERR-06018, BC-ERR-06019, BC-ERR-06020, BC-ERR-07026; BC-MIS-06016, BC-MIS-06017, BC-MIS-06018
- BC-PRQ-06001, BC-PRQ-06003
- research/units/unit-06-integration-accumulation.md#6.9 Integrating Using Substitution
- research/units/unit-06-integration-accumulation.md#6.11 Integrating Using Integration by Parts
- research/question-analysis/question-archetypes.md#BC-QA-06008 Antiderivative or definite integral by substitution
- research/question-analysis/question-archetypes.md#BC-QA-06018 Antiderivative matched to an inverse trigonometric form
- research/exam/exam-structure.md#Section and part layout
- research/scoring/common-point-losses.md#Answer points
- [inferred] ki-2 as extended. Settled by mid-band error rates on BC-ERR-06018 with and without it.
- [inferred] The Section II share of a substitution part. Settled by a rubric fixing its point count.
- [inferred] Which steps a fluent solver holds in the head. Settled by timing data per step.
- [inferred] err-BC-ERR-06020 and err-BC-ERR-07026 shown on adapted forms of ex-1's draw. Settled by draws that carry those features.

## Machine record

```json
{
 "id": "LSN-CON-06015",
 "kind": "concept",
 "target_id": "BC-CON-06015",
 "unit": "06",
 "skills": ["BC-SKL-06047", "BC-SKL-06048", "BC-SKL-06049", "BC-SKL-06050", "BC-SKL-06051", "BC-SKL-06052"],
 "prediction": {
  "id": "pr-1",
  "stem": {
   "text": "With u = x^2 + 1, 6x dx equals which multiple of du?",
   "command_verb": "predict"
  },
  "format": "mcq",
  "options": [
   {
    "id": "A",
    "label": "2 du",
    "is_key": false
   },
   {
    "id": "B",
    "label": "3 du",
    "is_key": true
   },
   {
    "id": "C",
    "label": "6 du",
    "is_key": false
   }
  ],
  "resolution": "du = 2x dx, so 6x dx = 3 du.",
  "sources": ["BC-CON-06015", "research/units/unit-06-integration-accumulation.md#6.9 Integrating Using Substitution"]
 },
 "orientation": {
  "text": "A response names u and du, rewrites the integral in u, converts the limits.",
  "sources": ["BC-CON-06015", "research/units/unit-06-integration-accumulation.md#6.9 Integrating Using Substitution"]
 },
 "key_ideas": [
  {
   "id": "ki-1",
   "ek_id": "BC-EK-FUN-6D1",
   "depth": "core",
   "text": "Name u = g(x). With g'(x) dx present up to a constant, f(g(x)) g'(x) dx becomes f(u) du.",
   "notation": "u = g(x), du = g'(x) dx",
   "quote": null,
   "sources": ["BC-EK-FUN-6D1", "ced:126", "research/units/unit-06-integration-accumulation.md#6.9 Integrating Using Substitution"]
  },
  {
   "id": "ki-2",
   "ek_id": "BC-EK-FUN-6D2",
   "depth": "extended",
   "text": "In a definite integral the limits change with the variable: x = a and x = b become u = g(a) and u = g(b). The alternative is to back-substitute first and then use the x limits.",
   "notation": "converted limits g(a), g(b)",
   "quote": {
    "text": "For a definite integral, substitution of variables requires corresponding changes to the limits of integration.",
    "source": "ced:126"
   },
   "sources": ["BC-EK-FUN-6D2", "ced:126", "research/units/unit-06-integration-accumulation.md#6.9 Integrating Using Substitution"]
  }
 ],
 "strategy": [
  {
   "id": "st-1",
   "archetype_id": "BC-QA-06008",
   "cue": "A composite, its inner derivative a factor.",
   "method": "Choose u as the inner expression.",
   "rival": "Substituting where the inner derivative is absent.",
   "separating_feature": "A constant multiple of g'(x) as a factor.",
   "sources": ["BC-QA-06008", "BC-ERR-06020", "research/units/unit-06-integration-accumulation.md#6.11 Integrating Using Integration by Parts"],
   "evidence_tag": "verified",
   "contrast": {
    "this": {
     "text": "Find the integral of 2x cos(x^2) dx.",
     "archetype_id": "BC-QA-06008"
    },
    "not_this": {
     "text": "Find the integral of x cos x dx.",
     "why_not": "No composite with its inner derivative; it calls for integration by parts."
    },
    "feature": "A multiple of the inner derivative."
   }
  }
 ],
 "worked_examples": [
  {
   "id": "ex-1",
   "archetype_id": "BC-QA-06008",
   "bands": ["low", "mid"],
   "parameter_draw": {
    "inner_power": 2,
    "inner_scale": 1,
    "inner_shift": 1,
    "multiplier": 6,
    "outer_power": 3,
    "upper": 1,
    "outer": "power",
    "form": "definite"
   },
   "problem": {
    "text": "Evaluate ∫_0^1 6x(x^2 + 1)^3 dx.",
    "command_verb": "evaluate"
   },
   "calculator_status": "no_calculator",
   "steps": [
    {
     "cue": "Inner x^2 + 1; 6x is a multiple of 2x.",
     "why": "Inner derivative present: substitution applies."
    },
    {
     "cue": "u = x^2 + 1: 6x dx = 3 du; limits become u = 1, 2.",
     "why": "Constant and limits change with the variable.",
     "expr": "3*u**3",
     "relation": "new"
    },
    {
     "cue": "3u^3 is a basic power.",
     "why": "Power rule in u.",
     "expr": "3*u**4/4",
     "relation": "integrate",
     "variable": "u",
     "point_type_id": "BC-PT-99003"
    },
    {
     "cue": "Use the u limits 1 and 2.",
     "why": "A u expression takes u limits only.",
     "expr": "3*2**4/4 - 3*1**4/4",
     "relation": "new"
    },
    {
     "cue": "Simplify.",
     "why": "The value.",
     "expr": "45/4",
     "relation": "equivalent",
     "point_type_id": "BC-PT-99004"
    }
   ],
   "answer": {
    "form": "symbolic",
    "expr": "45/4"
   }
  }
 ],
 "what_a_reader_scores": [
  {
   "example_id": "ex-1",
   "point_type_ids": ["BC-PT-99003", "BC-PT-99004"],
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
    "text": "u antiderivative at x = 0, 1.",
    "expr": "3*1**4/4 - 3*0**4/4"
   },
   "right_step": {
    "text": "At u = 1, 2.",
    "expr": "3*2**4/4 - 3*1**4/4"
   },
   "relation": "distinct",
   "possible_reason": {
    "misconception_id": "BC-MIS-06016",
    "text": "limits of integration and differentials carry over unchanged"
   },
   "sources": ["BC-ERR-06018", "BC-MIS-06016"],
   "fix_prompt": true
  },
  {
   "error_id": "BC-ERR-06019",
   "observed_behavior": "The substitution is carried out without the reciprocal constant that du introduces.",
   "scoring_consequence": "The antiderivative point is lost and the value point with it.",
   "wrong_step": {
    "text": "6x dx read as 6 du.",
    "expr": "6*u**4/4"
   },
   "right_step": {
    "text": "6x dx = 3 du.",
    "expr": "3*u**4/4"
   },
   "relation": "distinct",
   "possible_reason": null,
   "sources": ["BC-ERR-06019"],
   "fix_prompt": true
  },
  {
   "error_id": "BC-ERR-06020",
   "observed_behavior": "A composite is substituted although no constant multiple of the derivative of the inner expression appears in the integrand.",
   "scoring_consequence": "The setup point for the technique is not earned and the work does not lead to the antiderivative.",
   "wrong_step": {
    "text": "dx swapped for du, 6x left behind.",
    "expr": "6*x*u**3"
   },
   "right_step": {
    "text": "6x dx absorbed as 3 du.",
    "expr": "3*u**3"
   },
   "relation": "distinct",
   "possible_reason": {
    "misconception_id": "BC-MIS-06017",
    "text": "selects substitution from the presence of an inner function alone, without checking that its derivative is present"
   },
   "sources": ["BC-ERR-06020", "BC-MIS-06017"],
   "fix_prompt": true
  },
  {
   "error_id": "BC-ERR-07026",
   "observed_behavior": "The antiderivative equation is written with no constant.",
   "scoring_consequence": "At most the first two points are available; the guideline caps the response there.",
   "wrong_step": {
    "text": "Indefinite form with no constant.",
    "expr": "3*(x**2 + 1)**4/4"
   },
   "right_step": {
    "text": "With + C.",
    "expr": "3*(x**2 + 1)**4/4 + C"
   },
   "relation": "distinct",
   "possible_reason": {
    "misconception_id": "BC-MIS-06018",
    "text": "treats the antiderivative as unique"
   },
   "sources": ["BC-ERR-07026", "BC-MIS-06018"],
   "fix_prompt": true
  }
 ],
 "representations": null,
 "prerequisite_bridges": [
  {
   "prq_id": "BC-PRQ-06001",
   "text": "Factor out constants to expose the inner derivative."
  },
  {
   "prq_id": "BC-PRQ-06003",
   "text": "Keep the bars in ln|u|."
  }
 ],
 "time": {
  "exam_part": "II-B",
  "budget_minutes": 15.0,
  "source": "research/exam/exam-structure.md#Section and part layout",
  "written_steps": {
   "ex-1": [2, 3, 4, 5]
  },
  "skipped_steps": {
   "ex-1": [1]
  }
 },
 "checks": [
  {
   "id": "chk-1",
   "check_kind": "completion",
   "format": "short_answer",
   "bands": ["low", "mid"],
   "archetype_id": "BC-QA-06008",
   "parameter_draw": {
    "inner_power": 2,
    "inner_scale": 1,
    "inner_shift": 1,
    "multiplier": 6,
    "outer_power": 3,
    "upper": 1,
    "outer": "power",
    "form": "definite"
   },
   "completes": "ex-1",
   "stem": {
    "text": "∫_0^1 6x(x^2 + 1)^3 dx = ∫_1^2 3u^3 du. Find the value.",
    "command_verb": "find"
   },
   "key": {
    "form": "symbolic",
    "expr": "45/4"
   },
   "steps": [
    {
     "text": "Antiderivative in u.",
     "expr": "3*u**4/4",
     "relation": "new"
    },
    {
     "text": "u limits.",
     "expr": "3*2**4/4 - 3*1**4/4",
     "relation": "new"
    },
    {
     "text": "Value.",
     "expr": "45/4",
     "relation": "equivalent"
    }
   ],
   "calculator_status": "no_calculator",
   "skills": ["BC-SKL-06050", "BC-SKL-06051"]
  },
  {
   "id": "chk-2",
   "check_kind": "isomorph",
   "format": "short_answer",
   "bands": ["low", "mid"],
   "archetype_id": "BC-QA-06008",
   "parameter_draw": {
    "inner_power": 3,
    "inner_scale": 1,
    "inner_shift": 2,
    "multiplier": 6,
    "outer_power": 2,
    "upper": 1,
    "outer": "power",
    "form": "definite"
   },
   "stem": {
    "text": "Evaluate ∫_0^1 6x^2(x^3 + 2)^2 dx.",
    "command_verb": "evaluate"
   },
   "key": {
    "form": "symbolic",
    "expr": "38/3"
   },
   "steps": [
    {
     "text": "u = x^3 + 2, 6x^2 dx = 2 du, u from 2 to 3.",
     "expr": "Integral(2*u**2, (u, 2, 3))",
     "relation": "new"
    },
    {
     "text": "Value.",
     "expr": "38/3",
     "relation": "equivalent"
    }
   ],
   "calculator_status": "no_calculator",
   "skills": ["BC-SKL-06047", "BC-SKL-06048", "BC-SKL-06050"]
  },
  {
   "id": "chk-3",
   "check_kind": "mcq",
   "format": "mcq",
   "bands": ["low"],
   "archetype_id": "BC-QA-06008",
   "parameter_draw": {
    "inner_power": 2,
    "inner_scale": 1,
    "inner_shift": 3,
    "multiplier": 4,
    "outer_power": 2,
    "upper": 1,
    "outer": "power",
    "form": "definite"
   },
   "stem": {
    "text": "∫_0^1 4x(x^2 + 3)^2 dx =",
    "command_verb": "identify"
   },
   "key": {
    "form": "symbolic",
    "expr": "74/3"
   },
   "steps": [
    {
     "text": "u = x^2 + 3, 4x dx = 2 du, u from 3 to 4.",
     "expr": "Integral(2*u**2, (u, 3, 4))",
     "relation": "new"
    },
    {
     "text": "Value.",
     "expr": "74/3",
     "relation": "equivalent"
    }
   ],
   "options": [
    {
     "id": "A",
     "is_key": false,
     "expr": "2/3",
     "error_path": "BC-ERR-06018",
     "derivation": "(2/3)u^3 evaluated at the x limits 0 and 1"
    },
    {
     "id": "B",
     "is_key": false,
     "expr": "148/3",
     "error_path": "BC-ERR-06019",
     "derivation": "4x dx read as 4 du, the 1/2 dropped"
    },
    {
     "id": "C",
     "is_key": true,
     "expr": "74/3",
     "error_path": null
    },
    {
     "id": "D",
     "is_key": false,
     "expr": "128/3",
     "error_path": "BC-ERR-06018",
     "derivation": "upper limit converted to 4, lower x limit 0 kept"
    }
   ],
   "calculator_status": "no_calculator",
   "skills": ["BC-SKL-06048", "BC-SKL-06050"]
  }
 ],
 "delivery": [
  {
   "block": "orientation",
   "mode": "text",
   "reason": "rule 6: BC-REP-01 only on the concept's skills; a statement of what a response shows (unit README delivery map)",
   "sources": ["BC-SKL-06047"]
  },
  {
   "block": "ki-1",
   "mode": "text",
   "reason": "rule 6: a symbolic rule with BC-REP-01 alone; no process, no figure-bearing representation",
   "sources": ["BC-SKL-06047", "BC-SKL-06048"]
  },
  {
   "block": "ki-2",
   "mode": "text",
   "reason": "rule 6: a symbolic rule about limits with BC-REP-01 alone",
   "sources": ["BC-SKL-06050"]
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
   "block": "err-BC-ERR-06020",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  },
  {
   "block": "err-BC-ERR-07026",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  }
 ],
 "refresher": ["ki-1", "err-BC-ERR-06018", "err-BC-ERR-06019", "err-BC-ERR-06020", "err-BC-ERR-07026", "ex-1"],
 "research_lines": [
  {
   "file": "research/units/unit-06-integration-accumulation.md",
   "line": "For a definite integral, substitution of variables requires corresponding changes to the limits of integration (BC-EK-FUN-6D2); the alternative is to back-substitute before applying the original limits."
  }
 ],
 "inferred": [
  {
   "claim": "ki-2 (BC-EK-FUN-6D2) is served as extended, low band only, so the brief band stays under 450 words; ex-1 step 2 and err-BC-ERR-06018 carry the limit conversion in the mid band.",
   "settles": "Mid-band error rates on BC-ERR-06018 with and without ki-2 served."
  },
  {
   "claim": "BC-QA-06008 is served here as a no-calculator free-response part, Section II Part B, its share of the 15.0 minutes set by points not recorded in scoring_pattern.",
   "settles": "A rubric fixing the point count of a substitution part (unit README section 5)."
  },
  {
   "claim": "A fluent solver holds the choice of u in the head and writes du with the constant, the integral in u, the antiderivative and the value.",
   "settles": "Timing data per step once the fluency telemetry exists."
  },
  {
   "claim": "err-BC-ERR-06020 is shown on ex-1's draw, where the inner derivative is present, as dx replaced by du with the x factor left; the draw has no absent derivative to show.",
   "settles": "A BC-QA-06008 draw whose integrand lacks the inner derivative, which parameter_spec does not generate."
  },
  {
   "claim": "err-BC-ERR-07026 is shown on the indefinite form of ex-1's integrand, since the definite draw carries no constant.",
   "settles": "An indefinite draw (form indefinite) served as a second example."
  }
 ],
 "sources": ["BC-CON-06015", "BC-SKL-06047", "BC-SKL-06048", "BC-SKL-06049", "BC-SKL-06050", "BC-SKL-06051", "BC-SKL-06052", "BC-EK-FUN-6D1", "BC-EK-FUN-6D2", "ced:126", "BC-QA-06008", "BC-QA-06018", "BC-PT-99003", "BC-PT-99004", "BC-PT-99002", "sg-23:16", "sg-23:17", "BC-ERR-06018", "BC-ERR-06019", "BC-ERR-06020", "BC-ERR-07026", "BC-MIS-06016", "BC-MIS-06017", "BC-MIS-06018", "BC-PRQ-06001", "BC-PRQ-06003", "research/units/unit-06-integration-accumulation.md#6.9 Integrating Using Substitution", "research/question-analysis/question-archetypes.md#BC-QA-06008 Antiderivative or definite integral by substitution", "research/question-analysis/question-archetypes.md#BC-QA-06018 Antiderivative matched to an inverse trigonometric form", "research/exam/exam-structure.md#Section and part layout", "research/scoring/common-point-losses.md#Answer points"],
 "read_minutes": {
  "full": 4.2,
  "brief": 3.0
 },
 "word_count": {
  "full": 610,
  "brief": 446
 },
 "no_figure_reason": "The skills carry symbolic representations only, and no key idea describes a process. The lesson is a chain of written substitutions."
}
```
