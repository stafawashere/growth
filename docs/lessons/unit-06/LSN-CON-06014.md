---
title: LSN-CON-06014 Antiderivative and indefinite integral
research_date: 2026-09-29
status: designed
purpose: Authoring spec for the concept lesson on BC-CON-06014, the indefinite integral as the family F(x) + C built from differentiation rules read backwards and confirmed by differentiating, built from authoring_bundle("BC-CON-06014") and the research files it cites, so an author fills plan 15's lesson record without making a teaching decision.
---

# LSN-CON-06014 Antiderivative and indefinite integral

Concept BC-CON-06014 (skills BC-SKL-06040 to BC-SKL-06045), topic 6.8 of Unit 6. Plan 15's content model records it as loaded by no active archetype; the current snapshot has six archetypes loading its skills, BC-QA-06018 and BC-QA-06019 with a BC-CON-06014 skill first, then BC-QA-06008, 06009, 06011 and 06016 (docs/lessons/unit-06/README.md, section 1). The retired skill for integrands with no closed-form antiderivative still names this concept but no concept list holds it; its content is taught in LSN-CON-06020. No Unit 6 hard parent.

## Prediction

Multiple choice on ex-1's integrand, tagged [inferred] (the record carries no pretest). Stem: which describes all functions whose derivative is 3x^(1/2) - 2x^(-1/2). Options: the single function, the family with + C (the key), and the family with the exponents raised and not divided, which is the BC-ERR-06033 move. The resolution says the derivative of the function and of any shifted copy is the integrand, so the antiderivatives form F(x) + C, with no verdict word. Source: BC-CON-06014 and the topic section 6.8 the key idea cites.

## Orientation

Served text, from BC-CON-06014 `description_plain` and the topic's Assessment behaviour paragraph (research/units/unit-06-integration-accumulation.md#6.8 Finding Antiderivatives and Indefinite Integrals: Basic Rules and Notation): a response rewrites the integrand as powers, reverses the power rule, writes + C and confirms by differentiating. No count, no frequency.

## Key ideas

BC-SKL-06040, 06044 and 06045 map to BC-EK-FUN-6C1; BC-SKL-06040 to 06043 and 06045 to BC-EK-FUN-6C2 (ced:125). Two blocks, both core.

- ki-1 (core, BC-EK-FUN-6C1). Paraphrase of "Indefinite integral": the integral of f(x) dx is F(x) + C with F' = f and C any constant; differentiating a candidate confirms it. No quote: the EK text on ced:125 is extracted with broken spacing. Notation line from the concept record.
- ki-2 (core, BC-EK-FUN-6C2). Paraphrase of "Source of the rules": each derivative rule read backwards, the power rule for every exponent but -1, the exponential and logarithm forms, the trigonometric and inverse trigonometric forms. Anchor quote from ced:125.

## Recognition

- BC-QA-06019 (research/question-analysis/question-archetypes.md#BC-QA-06019 Antiderivative found after splitting a fraction or expanding a product, and confirmed by differentiating): `typical_wording` "find the indefinite integral"; `common_givens` a product of two binomials, or a fraction whose numerator is a sum; `asked_to_produce` an antiderivative with the constant of integration. Signal: an integral sign with no limits over a product or a fraction of powers. Shape: a single MCQ or short answer.
- BC-QA-06018 (research/question-analysis/question-archetypes.md#BC-QA-06018 Antiderivative matched to an inverse trigonometric form, directly or after completing the square): a constant over a quadratic or its square root.
- BC-QA-06016 (research/question-analysis/question-archetypes.md#BC-QA-06016 Selecting an antidifferentiation technique from the form of the integrand) and BC-QA-06011 (research/question-analysis/question-archetypes.md#BC-QA-06011 Improper integral convergence or divergence) reach this concept through a basic antiderivative inside a technique.

What says "not this concept": a composite with its inner derivative present selects substitution; a product of unlike factors selects parts (docs/lessons/unit-06/README.md, section 3).

The near miss in the contrast pair comes from the `wrong_approaches` entry of BC-QA-06019 and the sibling concept BC-CON-06017: a product of unlike factors such as x cos x has no expansion into powers and calls for integration by parts, where a product of binomials expands.

## Method choice

One block per archetype family, three families; st-1 serves both bands.

- st-1, BC-QA-06019 (family antidifferentiation-technique, which also holds BC-QA-06018, 06008 and 06009). Method, `expected_solution_path[0]`: expand the product or split the fraction into a sum of powers. Rival from `wrong_approaches`: antidifferentiating the factors of a product separately. Separating feature: a product or quotient has no rule of its own.
- st-2, BC-QA-06016 (procedure-selection). Method: inspect the integrand for structural markers. Rival: substituting for an inner expression whose derivative is absent (BC-ERR-06020). Separating feature: whether the inner derivative is present.
- st-3, BC-QA-06011 (improper-integral). Method: name the impropriety and replace the offending limit by a variable. Rival: substituting infinity and computing with it (BC-ERR-99007). Separating feature: an infinite limit or an unbounded integrand.

Contrast pair on st-1 (new on 2026-09-29): this is a product of binomials on BC-QA-06019; not this is a product of unlike factors, integration by parts; the feature is that binomials expand into powers and unlike factors do not. The orientation and bridges are shortened to fit the brief cap.

## Solution path

- ex-1, BC-QA-06019, both bands, no calculator. Draw from `parameter_spec`: structure root, coefficient 3, first -2, second 1, power 2; middle = 1 + 3(-2) = -5, nonzero. Integrand (3x - 2)/sqrt(x) = 3x^(1/2) - 2x^(-1/2); antiderivative 2x^(3/2) - 4x^(1/2) + C. No published BC-QA-06019 item carries this draw.
- Steps follow `expected_solution_path`: the integrand (new), split into powers (equivalent), the power rule term by term with + C (integrate, x), the check by differentiating (no value). A fluent solver writes the split and the antiderivative; the check is held.

## Scoring

BC-QA-06019 lists no `point_types`, so no what_a_reader_scores entry and no point tag; the served text names no point beyond the error records' scoring_consequence (plan 15, R14).

## Traps

Two active errors meet the skills, in the bundle's order (both linked BC-MIS at severity high): BC-ERR-06033, BC-ERR-07026. Both bands serve both. On ex-1's draw.

- err-BC-ERR-06033: 3x^(3/2) - 2x^(1/2) + C, exponents raised with no division, against 2x^(3/2) - 4x^(1/2) + C. Possible reason, words from BC-MIS-02009.
- err-BC-ERR-07026: the answer without + C. Possible reason, words from BC-MIS-06018.

## Representations

None.

## Prerequisite bridge

- BC-PRQ-06002, BC-PRQ-06003, BC-PRQ-06004, each from its `description_plain` and `failure_signature`.

## Time

BC-QA-06019 is `no_calculator`, a single MCQ or short answer, so Section I Part A, 2.14 minutes (research/exam/exam-structure.md#Section and part layout). The minutes go on the rewrite into powers; the check by differentiating is held (docs/lessons/unit-06/README.md, section 5).

## Checks

- chk-1, completion of ex-1, both bands: the split 3x^(1/2) - 2x^(-1/2) is given. Key 2x^(3/2) - 4x^(1/2) + C.
- chk-2, isomorph, both bands. Draw: structure product, coefficient 2, first 3, second -1, power 2; (x + 3)(2x - 1). Key 2x^3/3 + 5x^2/2 - 3x + C.
- No chk-3: the bundle holds two errors and a 4-option MCQ needs three distractors anchored to distinct error blocks (listed in the inferred array).

## Delivery

- orientation, ki-1, ki-2: text. Rule 6: BC-REP-01 only on every skill (docs/lessons/unit-06/README.md, section 6).
- ex-1, err-BC-ERR-06033, err-BC-ERR-07026: step_reveal. Rule 1.
- No drawn block: `no_figure_reason` states that every skill carries symbolic representations only and no key idea describes a process, so none of rules 2 to 5 applies.

## Band plan

- Low (full): prediction, orientation, the three bridges, ki-1, ki-2, st-1 with its contrast, st-2, st-3, ex-1, chk-1, both error blocks, chk-2. 498 words, 3.5 minutes (cap 900 and 6).
- Mid (brief): prediction, orientation, the three bridges, ki-1, ki-2, st-1 with its contrast, ex-1, chk-1, both error blocks, chk-2. 433 words, 3.0 minutes (cap 450 and 3).
- Refresher: ki-1, ki-2, err-BC-ERR-06033, err-BC-ERR-07026, ex-1.

## Sources

- BC-CON-06014; BC-SKL-06040, BC-SKL-06041, BC-SKL-06042, BC-SKL-06043, BC-SKL-06044, BC-SKL-06045; BC-EK-FUN-6C1, BC-EK-FUN-6C2; ced:125
- BC-QA-06019, BC-QA-06018, BC-QA-06016, BC-QA-06011, BC-QA-06008, BC-QA-06009
- BC-ERR-06033, BC-ERR-07026, BC-ERR-06020, BC-ERR-99007; BC-MIS-02009, BC-MIS-06018
- BC-PRQ-06002, BC-PRQ-06003, BC-PRQ-06004
- research/units/unit-06-integration-accumulation.md#6.8 Finding Antiderivatives and Indefinite Integrals: Basic Rules and Notation
- research/question-analysis/question-archetypes.md#BC-QA-06019 Antiderivative found after splitting a fraction or expanding a product, and confirmed by differentiating
- research/exam/exam-structure.md#Section and part layout
- [inferred] Two checks, not three. Settled by a third active BC-ERR on a BC-CON-06014 skill.

## Machine record

```json
{
 "id": "LSN-CON-06014",
 "kind": "concept",
 "target_id": "BC-CON-06014",
 "unit": "06",
 "skills": ["BC-SKL-06040", "BC-SKL-06041", "BC-SKL-06042", "BC-SKL-06043", "BC-SKL-06044", "BC-SKL-06045"],
 "prediction": {
  "id": "pr-1",
  "stem": {
   "text": "Which describes all functions whose derivative is 3x^(1/2) - 2x^(-1/2)?",
   "command_verb": "predict"
  },
  "format": "mcq",
  "options": [
   {
    "id": "A",
    "label": "Only 2x^(3/2) - 4x^(1/2).",
    "is_key": false
   },
   {
    "id": "B",
    "label": "2x^(3/2) - 4x^(1/2) + C, for any constant C.",
    "is_key": true
   },
   {
    "id": "C",
    "label": "3x^(3/2) - 2x^(1/2) + C, for any constant C.",
    "is_key": false
   }
  ],
  "resolution": "Differentiating 2x^(3/2) - 4x^(1/2) gives the integrand, and so does adding any constant. The antiderivatives form the family F(x) + C.",
  "sources": ["BC-CON-06014", "research/units/unit-06-integration-accumulation.md#6.8 Finding Antiderivatives and Indefinite Integrals: Basic Rules and Notation"]
 },
 "orientation": {
  "text": "A response rewrites the integrand as powers, reverses the power rule, writes + C, and confirms by differentiating.",
  "sources": ["BC-CON-06014", "research/units/unit-06-integration-accumulation.md#6.8 Finding Antiderivatives and Indefinite Integrals: Basic Rules and Notation"]
 },
 "key_ideas": [
  {
   "id": "ki-1",
   "ek_id": "BC-EK-FUN-6C1",
   "depth": "core",
   "text": "The indefinite integral of f is the whole family F(x) + C, where F' = f and C is any constant. Differentiating a candidate and getting f back confirms it.",
   "notation": "integral of f(x) dx = F(x) + C",
   "quote": null,
   "sources": ["BC-EK-FUN-6C1", "ced:125", "research/units/unit-06-integration-accumulation.md#6.8 Finding Antiderivatives and Indefinite Integrals: Basic Rules and Notation"]
  },
  {
   "id": "ki-2",
   "ek_id": "BC-EK-FUN-6C2",
   "depth": "core",
   "text": "Each derivative rule read backwards is an antiderivative rule. Powers: raise the exponent by one and divide by the new exponent, for every exponent except -1. Also the exponential, logarithm, trigonometric and inverse trigonometric forms.",
   "notation": "integral of x^n dx = x^(n+1)/(n+1) + C, n not -1",
   "quote": {
    "text": "Differentiation rules provide the foundation for finding antiderivatives.",
    "source": "ced:125"
   },
   "sources": ["BC-EK-FUN-6C2", "ced:125", "research/units/unit-06-integration-accumulation.md#6.8 Finding Antiderivatives and Indefinite Integrals: Basic Rules and Notation"]
  }
 ],
 "strategy": [
  {
   "id": "st-1",
   "archetype_id": "BC-QA-06019",
   "cue": "A product of binomials, or a fraction with a sum on top.",
   "method": "Expand the product or split the fraction into powers.",
   "rival": "Each factor antidifferentiated separately.",
   "separating_feature": "A product or quotient has no rule of its own.",
   "sources": ["BC-QA-06019"],
   "evidence_tag": "verified",
   "contrast": {
    "this": {
     "text": "Find the indefinite integral of (x + 2)(3x - 1) dx.",
     "archetype_id": "BC-QA-06019"
    },
    "not_this": {
     "text": "Find the indefinite integral of x cos x dx.",
     "why_not": "A product of unlike factors calls for integration by parts."
    },
    "feature": "Binomials expand into powers; unlike factors do not."
   }
  },
  {
   "id": "st-2",
   "archetype_id": "BC-QA-06016",
   "cue": "An indefinite integral with supporting work, the technique left to the reader.",
   "method": "The structural markers of the integrand named.",
   "rival": "Substitution with the inner derivative absent.",
   "separating_feature": "Whether the inner derivative is present.",
   "sources": ["BC-QA-06016", "BC-ERR-06020"],
   "evidence_tag": "verified"
  },
  {
   "id": "st-3",
   "archetype_id": "BC-QA-06011",
   "cue": "An integral on an infinite interval, or unbounded at a point; value or divergence asked.",
   "method": "The offending limit replaced by a variable.",
   "rival": "Infinity substituted and computed with.",
   "separating_feature": "An infinite limit or an unbounded integrand.",
   "sources": ["BC-QA-06011", "BC-ERR-99007"],
   "evidence_tag": "verified"
  }
 ],
 "worked_examples": [
  {
   "id": "ex-1",
   "archetype_id": "BC-QA-06019",
   "bands": ["low", "mid"],
   "parameter_draw": {
    "structure": "root",
    "coefficient": 3,
    "first": -2,
    "second": 1,
    "power": 2
   },
   "problem": {
    "text": "Find the indefinite integral of (3x - 2)/sqrt(x) dx.",
    "command_verb": "find"
   },
   "calculator_status": "no_calculator",
   "steps": [
    {
     "cue": "A fraction over sqrt(x): no quotient rule backwards.",
     "why": "Split it.",
     "expr": "(3*x - 2)/sqrt(x)",
     "relation": "new"
    },
    {
     "cue": "sqrt(x) is x^(1/2).",
     "why": "Each term becomes a power.",
     "expr": "3*x**(1/2) - 2*x**(-1/2)",
     "relation": "equivalent"
    },
    {
     "cue": "Powers, neither -1.",
     "why": "Raise by one, divide by the new exponent; + C.",
     "expr": "2*x**(3/2) - 4*x**(1/2) + C",
     "relation": "integrate",
     "variable": "x"
    },
    {
     "cue": "Check: differentiate back.",
     "why": "3x^(1/2) - 2x^(-1/2), the integrand."
    }
   ],
   "answer": {
    "form": "symbolic",
    "expr": "2*x**(3/2) - 4*x**(1/2) + C"
   }
  }
 ],
 "what_a_reader_scores": [],
 "common_errors": [
  {
   "error_id": "BC-ERR-06033",
   "observed_behavior": "The response raises each exponent by one but does not divide by the new exponent, or divides by the old exponent instead.",
   "scoring_consequence": "The proposed function does not differentiate to the integrand, so an antiderivative point is not earned.",
   "wrong_step": {
    "text": "No division.",
    "expr": "3*x**(3/2) - 2*x**(1/2) + C"
   },
   "right_step": {
    "text": "Divided by 3/2 and 1/2.",
    "expr": "2*x**(3/2) - 4*x**(1/2) + C"
   },
   "relation": "distinct",
   "possible_reason": {
    "misconception_id": "BC-MIS-02009",
    "text": "does not see constants and radicals as powers"
   },
   "sources": ["BC-ERR-06033", "BC-MIS-02009"],
   "fix_prompt": true
  },
  {
   "error_id": "BC-ERR-07026",
   "observed_behavior": "The antiderivative equation is written with no constant.",
   "scoring_consequence": "At most the first two points are available; the guideline caps the response there.",
   "wrong_step": {
    "text": "No + C.",
    "expr": "2*x**(3/2) - 4*x**(1/2)"
   },
   "right_step": {
    "text": "With + C.",
    "expr": "2*x**(3/2) - 4*x**(1/2) + C"
   },
   "relation": "distinct",
   "possible_reason": {
    "misconception_id": "BC-MIS-06018",
    "text": "treats the antiderivative as unique, so the arbitrary constant is decoration rather than part of the answer"
   },
   "sources": ["BC-ERR-07026", "BC-MIS-06018"],
   "fix_prompt": true
  }
 ],
 "representations": null,
 "prerequisite_bridges": [
  {
   "prq_id": "BC-PRQ-06002",
   "text": "Radicals and reciprocals become powers first; exponent -1 is excluded."
  },
  {
   "prq_id": "BC-PRQ-06003",
   "text": "ln takes an absolute value around a linear expression."
  },
  {
   "prq_id": "BC-PRQ-06004",
   "text": "A squared trigonometric integrand is rewritten by an identity."
  }
 ],
 "time": {
  "exam_part": "I-A",
  "budget_minutes": 2.14,
  "source": "research/exam/exam-structure.md#Section and part layout",
  "written_steps": {
   "ex-1": [2, 3]
  },
  "skipped_steps": {
   "ex-1": [1, 4]
  }
 },
 "checks": [
  {
   "id": "chk-1",
   "check_kind": "completion",
   "format": "short_answer",
   "bands": ["low", "mid"],
   "archetype_id": "BC-QA-06019",
   "parameter_draw": {
    "structure": "root",
    "coefficient": 3,
    "first": -2,
    "second": 1,
    "power": 2
   },
   "completes": "ex-1",
   "stem": {
    "text": "(3x - 2)/sqrt(x) = 3x^(1/2) - 2x^(-1/2). Find its indefinite integral.",
    "command_verb": "find"
   },
   "key": {
    "form": "symbolic",
    "expr": "2*x**(3/2) - 4*x**(1/2) + C"
   },
   "steps": [
    {
     "text": "The split.",
     "expr": "3*x**(1/2) - 2*x**(-1/2)",
     "relation": "new"
    },
    {
     "text": "Power rule, + C.",
     "expr": "2*x**(3/2) - 4*x**(1/2) + C",
     "relation": "integrate",
     "variable": "x"
    }
   ],
   "calculator_status": "no_calculator",
   "skills": ["BC-SKL-06040"]
  },
  {
   "id": "chk-2",
   "check_kind": "isomorph",
   "format": "short_answer",
   "bands": ["low", "mid"],
   "archetype_id": "BC-QA-06019",
   "parameter_draw": {
    "structure": "product",
    "coefficient": 2,
    "first": 3,
    "second": -1,
    "power": 2
   },
   "stem": {
    "text": "Find the indefinite integral of (x + 3)(2x - 1) dx.",
    "command_verb": "find"
   },
   "key": {
    "form": "symbolic",
    "expr": "2*x**3/3 + 5*x**2/2 - 3*x + C"
   },
   "steps": [
    {
     "text": "Product.",
     "expr": "(x + 3)*(2*x - 1)",
     "relation": "new"
    },
    {
     "text": "Expanded.",
     "expr": "2*x**2 + 5*x - 3",
     "relation": "equivalent"
    },
    {
     "text": "Power rule, + C.",
     "expr": "2*x**3/3 + 5*x**2/2 - 3*x + C",
     "relation": "integrate",
     "variable": "x"
    }
   ],
   "calculator_status": "no_calculator",
   "skills": ["BC-SKL-06040"]
  }
 ],
 "delivery": [
  {
   "block": "orientation",
   "mode": "text",
   "reason": "rule 6: BC-REP-01 only",
   "sources": ["BC-SKL-06040"]
  },
  {
   "block": "ki-1",
   "mode": "text",
   "reason": "rule 6: a definition, BC-REP-01 only",
   "sources": ["BC-SKL-06044", "BC-SKL-06045"]
  },
  {
   "block": "ki-2",
   "mode": "text",
   "reason": "rule 6: rules, BC-REP-01 only",
   "sources": ["BC-SKL-06040", "BC-SKL-06041", "BC-SKL-06042", "BC-SKL-06043"]
  },
  {
   "block": "ex-1",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  },
  {
   "block": "err-BC-ERR-06033",
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
 "refresher": ["ki-1", "ki-2", "err-BC-ERR-06033", "err-BC-ERR-07026", "ex-1"],
 "read_minutes": {
  "full": 3.5,
  "brief": 3.0
 },
 "word_count": {
  "full": 497,
  "brief": 432
 },
 "research_lines": [
  {
   "file": "research/units/unit-06-integration-accumulation.md",
   "line": "The integral of f(x) dx equals F(x) plus C, where F'(x) = f(x) and C is any constant"
  }
 ],
 "inferred": [
  {
   "claim": "The lesson carries two checks: the bundle holds two errors, BC-ERR-06033 and BC-ERR-07026, and check 3 needs three distractors anchored to error blocks.",
   "settles": "A third active BC-ERR on a BC-CON-06014 skill."
  }
 ],
 "sources": ["BC-CON-06014", "BC-SKL-06040", "BC-SKL-06041", "BC-SKL-06042", "BC-SKL-06043", "BC-SKL-06044", "BC-SKL-06045", "BC-EK-FUN-6C1", "BC-EK-FUN-6C2", "ced:125", "BC-QA-06019", "BC-QA-06018", "BC-QA-06016", "BC-QA-06011", "BC-ERR-06033", "BC-ERR-07026", "BC-MIS-02009", "BC-MIS-06018", "BC-PRQ-06002", "BC-PRQ-06003", "BC-PRQ-06004", "research/units/unit-06-integration-accumulation.md#6.8 Finding Antiderivatives and Indefinite Integrals: Basic Rules and Notation", "research/question-analysis/question-archetypes.md#BC-QA-06019 Antiderivative found after splitting a fraction or expanding a product, and confirmed by differentiating", "research/exam/exam-structure.md#Section and part layout"],
 "no_figure_reason": "Every skill carries symbolic representations only, and no key idea describes a process. The lesson is a chain of written lines."
}
```
