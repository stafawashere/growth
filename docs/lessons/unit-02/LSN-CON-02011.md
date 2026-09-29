---
title: LSN-CON-02011 Linearity of differentiation
research_date: 2026-09-29
status: designed
purpose: Authoring spec for the concept lesson on BC-CON-02011, linearity of differentiation, built from authoring_bundle("BC-CON-02011") and the research files it cites, so an author fills plan 15's lesson record without making a teaching decision.
---

# LSN-CON-02011 Linearity of differentiation

Concept BC-CON-02011 (skills BC-SKL-02028, BC-SKL-02029, BC-SKL-02030, BC-SKL-02031), topic 2.6 of Unit 2, loaded by BC-QA-02006 only. The structure follows LSN-CON-02013.

## Prediction

Served first, both bands. On ex-1's numbers, \(f(x)=5x^4-\frac3x+8\), the student picks what the constant term 8 contributes to \(f'(x)\): stays, contributes 0, or is multiplied by the exponent 4. Format `mcq`, key "contributes 0, so it drops out". The distractors are the constant carried (BC-ERR-02016) and a power rule applied to a term that is not a power. The resolution states that the derivative of a constant function is zero and that multipliers stay in front, in the words of BC-EK-FUN-3A2 on ced:65. Sources: BC-CON-02011, BC-EK-FUN-3A2, ced:65 [verified].

## Orientation

Served text, from BC-CON-02011 `description_plain` and the topic's Assessment behaviour paragraph (research/units/unit-02-differentiation-definition-properties.md#2.6 Derivative Rules: Constant, Sum, Difference, and Constant Multiple): term by term differentiation, multipliers kept, constants to zero. The sentence on MCQ forms and supplied models in application parts was cut to bring the brief form under 450 words. No count, no frequency.

## Key ideas

Two BC-EK map to the skills: BC-EK-FUN-3A2 (BC-SKL-02028 to 02030) and BC-EK-FUN-3A3 (BC-SKL-02031), both on ced:65.

- ki-1 (core, both bands). Linearity and the constant, paraphrased from the Linearity and Constants paragraphs. Anchor quote (13 words) from ced:65.
- ki-2 (extended, low band). The polynomial case, paraphrased from the same paragraph; no quote.

## Recognition

- BC-QA-02006 (family rule-manipulation, single MCQ, no calculator; research/question-analysis/question-archetypes.md#BC-QA-02006 Derivative of a polynomial or power expression by rule): `typical_wording` "Find the derivative of the given function."; `common_givens` an expression built from powers, radicals and reciprocals; `asked_to_produce` the derivative, and its value at a named input. The signal is terms joined by plus and minus, each a number times a power, with a lone constant.

What says "not this concept": two variable factors multiplied or divided (BC-CON-02013, 02014); a constant denominator, which this concept's constant multiple rule handles instead of the quotient rule (BC-ERR-02023, taught in BC-CON-02014).

The contrast pair on st-1 takes its near miss from the sibling concept BC-CON-02013. `this` is a sum of constant multiples of powers with a lone constant (BC-QA-02006 wording, a different draw from every published item). `not_this` multiplies two binomials, which reads as a polynomial but calls for the product rule; the feature is terms joined by plus or minus against factors multiplied.

## Method choice

One strategy block, both bands.

- st-1, BC-QA-02006. Method, `expected_solution_path[0]`: rewrite radicals and reciprocals as powers, so every term is a constant times a power. The served method text carries no leading label. Rival: the constant term carried (BC-ERR-02016); the archetype records no `wrong_approaches`, so the rival is [inferred] and the block is tagged inferred. Separating feature: a multiplier touches a power; a constant stands alone.

## Solution path

- ex-1, BC-QA-02006, both bands, no calculator. Draw: leading 5, degree 4, second reciprocal, second coefficient \(-3\), reciprocal power 1, constant 8: \(f(x)=5x^4-\frac3x+8\). Steps: the given, rewrite, differentiate term by term, fraction form. A fluent solver writes the rewritten line, the derivative and the final form.

No productive-failure opener targets this concept, so no comparison callout.

## Scoring

None. BC-QA-02006 lists no `point_types`, so no step is tagged and the lesson says nothing about points beyond the error records' consequence text.

## Traps

Two active errors meet the concept's skills, in the bundle's order; both bands show both.

- err-BC-ERR-02015 (BC-MIS-02009): \(5x^3-3x^{-2}\) against \(20x^3+3x^{-2}\). Distinct, `fix_prompt` true.
- err-BC-ERR-02016 (BC-MIS-02009): the 8 carried. Distinct, `fix_prompt` true.

## Representations

None. The topic's Representations paragraph names BC-REP-01 only.

## Prerequisite bridge

- BC-PRQ-02004 (Prime notation and Leibniz notation conventions), from its `description_plain` and `failure_signature`, served when that state is unmet.

## Time

BC-QA-02006 is `no_calculator` and a single MCQ, so the part is Section I Part A, 2.14 minutes per question (research/exam/exam-structure.md#Section and part layout; plan 15, Fluency). A fluent solver writes the rewritten line and the derivative; the sum structure is read, not written.

## Checks

- chk-1, completion of ex-1, both bands: the rule line given, fraction form written. Key \(20x^3+\frac{3}{x^2}\).
- chk-2, isomorph on BC-QA-02006, both bands: \(f(x)=-3x^2+8\sqrt[3]{x}-4\). Key \(-6x+\frac{8}{3x^{2/3}}\).
- chk-3, MCQ on BC-QA-02006, low band: \(f(x)=2x^6+\frac{7}{x^3}+9\). Key \(12x^5-\frac{21}{x^4}\). Distractors: the 9 carried (BC-ERR-02016); factors omitted on both terms (BC-ERR-02015); factor omitted on the reciprocal term (BC-ERR-02015). The bundle holds two errors, so one path carries two distractors.

No draw equals a published BC-QA-02006 `parameter_draw`.

## Delivery

- orientation, ki-1, ki-2: text. Rule 5, BC-REP-01 only; unit README delivery map.
- ex-1: step_reveal. Rule 1.
- err-BC-ERR-02015, err-BC-ERR-02016: step_reveal. Rule 1.

No drawn block applies: no skill carries a figure-bearing BC-REP (rules 2 to 5 do not select), so the machine record states `no_figure_reason` [inferred; settled by the modality A/B].

## Band plan

- Low (full): prediction, orientation, ki-1, ki-2, st-1 with its contrast pair, ex-1, chk-1, err-BC-ERR-02015, err-BC-ERR-02016, chk-2, chk-3, the bridge. 472 words, 3.2 minutes (cap 900 and 6). No second example, so no fade.
- Mid (brief): prediction, orientation, bridge, ki-1, st-1 with its contrast pair, ex-1, chk-1, err-BC-ERR-02015, err-BC-ERR-02016, chk-2. 446 words, 3.0 minutes (cap 450 and 3).
- Refresher: ki-1, err-BC-ERR-02015, err-BC-ERR-02016, ex-1.

## Sources

- BC-CON-02011; BC-SKL-02028, BC-SKL-02029, BC-SKL-02030, BC-SKL-02031; BC-EK-FUN-3A2, BC-EK-FUN-3A3; ced:65
- BC-QA-02006
- BC-ERR-02015, BC-ERR-02016; BC-MIS-02009
- BC-PRQ-02004
- research/units/unit-02-differentiation-definition-properties.md#2.6 Derivative Rules: Constant, Sum, Difference, and Constant Multiple
- research/question-analysis/question-archetypes.md#BC-QA-02006 Derivative of a polynomial or power expression by rule
- research/exam/exam-structure.md#Section and part layout
- [inferred] st-1's rival. Settled by a staging pass adding `wrong_approaches` to BC-QA-02006.
- [inferred] The example carries a reciprocal term because BC-QA-02006's spec always includes one. Settled by a polynomial-only archetype.
- [inferred] No drawn block, `no_figure_reason` stated. Settled by the modality A/B.

## Machine record

```json
{
 "id": "LSN-CON-02011",
 "kind": "concept",
 "target_id": "BC-CON-02011",
 "unit": "02",
 "skills": [
  "BC-SKL-02028",
  "BC-SKL-02029",
  "BC-SKL-02030",
  "BC-SKL-02031"
 ],
 "prediction": {
  "id": "pr-1",
  "stem": {
   "text": "Predict before the rule. For \\(f(x)=5x^4-\\frac{3}{x}+8\\), the derivative is found term by term. What does the constant term 8 contribute to \\(f'(x)\\)?",
   "command_verb": "predict"
  },
  "format": "mcq",
  "options": [
   {
    "id": "A",
    "label": "The term 8 stays in \\(f'(x)\\) unchanged",
    "is_key": false
   },
   {
    "id": "B",
    "label": "The term 8 contributes 0, so it drops out",
    "is_key": true
   },
   {
    "id": "C",
    "label": "The term 8 is multiplied by the exponent 4",
    "is_key": false
   }
  ],
  "resolution": "The derivative of a constant function is zero, so the 8 contributes 0. The multipliers 5 and \\(-3\\) stay in front of their terms, and each multiplies the derivative of its own power.",
  "sources": [
   "BC-CON-02011",
   "BC-EK-FUN-3A2",
   "ced:65"
  ]
 },
 "no_figure_reason": "The skills carry BC-REP-01 only, and the key ideas state symbolic rules with no process, so no figure, table or motion fits.",
 "orientation": {
  "text": "A response differentiates a sum or difference term by term, keeps each constant multiplier in front, and sends each constant term to zero.",
  "sources": [
   "BC-CON-02011",
   "research/units/unit-02-differentiation-definition-properties.md#2.6 Derivative Rules: Constant, Sum, Difference, and Constant Multiple"
  ]
 },
 "key_ideas": [
  {
   "id": "ki-1",
   "ek_id": "BC-EK-FUN-3A2",
   "depth": "core",
   "text": "Sums, differences and constant multiples are differentiated by rule: \\((f\\pm g)'=f'\\pm g'\\) and \\((cf)'=cf'\\). The derivative of a constant function is zero, the constant multiple rule applied to the zeroth power. So a constant multiplier stays; a constant term disappears.",
   "notation": "constant multiple rule; sum rule; difference rule",
   "quote": {
    "text": "Sums, differences, and constant multiples of functions can be differentiated using derivative rules.",
    "source": "ced:65"
   },
   "sources": [
    "BC-EK-FUN-3A2",
    "ced:65",
    "research/units/unit-02-differentiation-definition-properties.md#2.6 Derivative Rules: Constant, Sum, Difference, and Constant Multiple"
   ]
  },
  {
   "id": "ki-2",
   "ek_id": "BC-EK-FUN-3A3",
   "depth": "extended",
   "text": "The power rule with the sum, difference and constant multiple properties differentiates any polynomial term by term.",
   "notation": "constant multiple rule; sum rule",
   "quote": null,
   "sources": [
    "BC-EK-FUN-3A3",
    "ced:65",
    "research/units/unit-02-differentiation-definition-properties.md#2.6 Derivative Rules: Constant, Sum, Difference, and Constant Multiple"
   ]
  }
 ],
 "strategy": [
  {
   "id": "st-1",
   "archetype_id": "BC-QA-02006",
   "cue": "The stem asks for the derivative of a sum of constant multiples of powers, with or without a constant term.",
   "method": "Every term written as a constant times a power of \\(x\\).",
   "rival": "The rival is carrying the constant term into the derivative.",
   "separating_feature": "A multiplier touches a power and stays; a constant stands alone and goes to zero.",
   "sources": [
    "BC-QA-02006",
    "BC-ERR-02016"
   ],
   "evidence_tag": "inferred",
   "contrast": {
    "this": {
     "text": "Let \\(g(x)=4x^3-\\frac{6}{x^2}+5\\). Find \\(g'(x)\\).",
     "archetype_id": "BC-QA-02006"
    },
    "not_this": {
     "text": "Let \\(h(x)=(4x^3-6)(x^2+5)\\). Find \\(h'(x)\\).",
     "why_not": "Two variable factors are multiplied, so the product rule applies, not term by term differentiation."
    },
    "feature": "Terms joined by plus or minus, each a number times a power, against factors multiplied."
   }
  }
 ],
 "worked_examples": [
  {
   "id": "ex-1",
   "archetype_id": "BC-QA-02006",
   "bands": [
    "low",
    "mid"
   ],
   "parameter_draw": {
    "leading": "5",
    "degree": "4",
    "second": "reciprocal",
    "second_coefficient": "-3",
    "root_index": "2",
    "reciprocal_power": "1",
    "constant": "8"
   },
   "problem": {
    "text": "Let \\(f(x)=5x^4-\\frac{3}{x}+8\\). Find \\(f'(x)\\).",
    "command_verb": "find"
   },
   "calculator_status": "no_calculator",
   "steps": [
    {
     "cue": "Three terms joined by \\(+\\) and \\(-\\): a sum.",
     "why": "The sum rule lets each term be differentiated alone.",
     "expr": "5*x**4-3/x+8",
     "relation": "new"
    },
    {
     "cue": "One term is a reciprocal: write it as a power.",
     "why": "\\(-\\frac3x=-3x^{-1}\\), a constant times a power.",
     "expr": "5*x**4-3*x**(-1)+8",
     "relation": "equivalent"
    },
    {
     "cue": "Differentiate term by term, multipliers kept.",
     "why": "\\(5\\cdot4x^3\\), \\(-3\\cdot(-1)x^{-2}\\), and the constant 8 gives 0.",
     "expr": "20*x**3+3*x**(-2)",
     "relation": "differentiate",
     "variable": "x"
    },
    {
     "cue": "The stem gave a fraction, so return to that form.",
     "why": "\\(x^{-2}=\\frac{1}{x^2}\\).",
     "expr": "20*x**3+3/x**2",
     "relation": "equivalent"
    }
   ],
   "answer": {
    "form": "symbolic",
    "expr": "20*x**3+3/x**2"
   }
  }
 ],
 "what_a_reader_scores": [],
 "common_errors": [
  {
   "error_id": "BC-ERR-02015",
   "observed_behavior": "The response lowers the exponent by one but omits the factor of the original exponent.",
   "scoring_consequence": "The derivative point is lost.",
   "wrong_step": {
    "text": "\\(5x^3-3x^{-2}\\): exponents lowered, factors 4 and \\(-1\\) missing.",
    "expr": "5*x**3-3*x**(-2)"
   },
   "right_step": {
    "text": "\\(20x^3+3x^{-2}\\).",
    "expr": "20*x**3+3*x**(-2)"
   },
   "relation": "distinct",
   "possible_reason": {
    "misconception_id": "BC-MIS-02009",
    "text": "the exponent decreasing but not the multiplication by the original exponent"
   },
   "sources": [
    "BC-ERR-02015",
    "BC-MIS-02009"
   ],
   "fix_prompt": true
  },
  {
   "error_id": "BC-ERR-02016",
   "observed_behavior": "The response carries a constant term unchanged into the derivative.",
   "scoring_consequence": "The derivative point is lost.",
   "wrong_step": {
    "text": "\\(20x^3+\\frac{3}{x^2}+8\\): the 8 carried.",
    "expr": "20*x**3+3/x**2+8"
   },
   "right_step": {
    "text": "\\(20x^3+\\frac{3}{x^2}\\): the constant term gives 0.",
    "expr": "20*x**3+3/x**2"
   },
   "relation": "distinct",
   "possible_reason": {
    "misconception_id": "BC-MIS-02009",
    "text": "does not see constants and radicals as powers"
   },
   "sources": [
    "BC-ERR-02016",
    "BC-MIS-02009"
   ],
   "fix_prompt": true
  }
 ],
 "representations": null,
 "prerequisite_bridges": [
  {
   "prq_id": "BC-PRQ-02004",
   "text": "A derivative is written in one notation that names the variable, \\(f'(x)\\) or \\(\\frac{dy}{dx}\\), never a mix inside one expression. A result that does not name the independent variable, or mixes notations, is the gap to close first."
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
   "archetype_id": "BC-QA-02006",
   "parameter_draw": {
    "leading": "5",
    "degree": "4",
    "second": "reciprocal",
    "second_coefficient": "-3",
    "root_index": "2",
    "reciprocal_power": "1",
    "constant": "8"
   },
   "completes": "ex-1",
   "stem": {
    "text": "For \\(f(x)=5x^4-\\frac3x+8\\), the rule gives \\(20x^3+3x^{-2}\\). Write \\(f'(x)\\) in fraction form.",
    "command_verb": "write"
   },
   "key": {
    "form": "symbolic",
    "expr": "20*x**3+3/x**2"
   },
   "steps": [
    {
     "text": "The rule line.",
     "expr": "20*x**3+3*x**(-2)",
     "relation": "new"
    },
    {
     "text": "Fraction form.",
     "expr": "20*x**3+3/x**2",
     "relation": "equivalent"
    }
   ],
   "calculator_status": "no_calculator",
   "skills": [
    "BC-SKL-02030"
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
   "archetype_id": "BC-QA-02006",
   "parameter_draw": {
    "leading": "-3",
    "degree": "2",
    "second": "radical",
    "second_coefficient": "8",
    "root_index": "3",
    "reciprocal_power": "1",
    "constant": "-4"
   },
   "stem": {
    "text": "Let \\(f(x)=-3x^2+8\\sqrt[3]{x}-4\\). Find \\(f'(x)\\).",
    "command_verb": "find"
   },
   "key": {
    "form": "symbolic",
    "expr": "-6*x+8/(3*x**(2/3))"
   },
   "steps": [
    {
     "text": "Rewrite: \\(-3x^2+8x^{1/3}-4\\).",
     "expr": "-3*x**2+8*x**(1/3)-4",
     "relation": "new"
    },
    {
     "text": "Differentiate term by term.",
     "expr": "-6*x+(8/3)*x**(-2/3)",
     "relation": "differentiate",
     "variable": "x"
    },
    {
     "text": "Fraction form.",
     "expr": "-6*x+8/(3*x**(2/3))",
     "relation": "equivalent"
    }
   ],
   "calculator_status": "no_calculator",
   "skills": [
    "BC-SKL-02030"
   ]
  },
  {
   "id": "chk-3",
   "check_kind": "mcq",
   "format": "mcq",
   "bands": [
    "low"
   ],
   "archetype_id": "BC-QA-02006",
   "parameter_draw": {
    "leading": "2",
    "degree": "6",
    "second": "reciprocal",
    "second_coefficient": "7",
    "root_index": "2",
    "reciprocal_power": "3",
    "constant": "9"
   },
   "stem": {
    "text": "If \\(f(x)=2x^6+\\frac{7}{x^3}+9\\), then \\(f'(x)=\\)",
    "command_verb": "find"
   },
   "key": {
    "form": "symbolic",
    "expr": "12*x**5-21/x**4"
   },
   "steps": [
    {
     "text": "Rewrite: \\(2x^6+7x^{-3}+9\\).",
     "expr": "2*x**6+7*x**(-3)+9",
     "relation": "new"
    },
    {
     "text": "Differentiate.",
     "expr": "12*x**5-21*x**(-4)",
     "relation": "differentiate",
     "variable": "x"
    },
    {
     "text": "Fraction form.",
     "expr": "12*x**5-21/x**4",
     "relation": "equivalent"
    }
   ],
   "options": [
    {
     "id": "A",
     "is_key": true,
     "expr": "12*x**5-21/x**4",
     "error_path": null
    },
    {
     "id": "B",
     "is_key": false,
     "expr": "12*x**5-21/x**4+9",
     "error_path": "BC-ERR-02016",
     "derivation": "the constant 9 carried"
    },
    {
     "id": "C",
     "is_key": false,
     "expr": "2*x**5+7/x**4",
     "error_path": "BC-ERR-02015",
     "derivation": "exponents lowered, factors 6 and -3 omitted"
    },
    {
     "id": "D",
     "is_key": false,
     "expr": "12*x**5+7/x**4",
     "error_path": "BC-ERR-02015",
     "derivation": "the factor -3 omitted on the reciprocal term"
    }
   ],
   "calculator_status": "no_calculator",
   "skills": [
    "BC-SKL-02031"
   ]
  }
 ],
 "delivery": [
  {
   "block": "orientation",
   "mode": "text",
   "reason": "rule 5: BC-REP-01 only on BC-SKL-02028 to 02031; unit README delivery map",
   "sources": [
    "BC-SKL-02028"
   ]
  },
  {
   "block": "ki-1",
   "mode": "text",
   "reason": "rule 5: a symbolic rule, BC-REP-01 only",
   "sources": [
    "BC-SKL-02029",
    "BC-SKL-02030"
   ]
  },
  {
   "block": "ki-2",
   "mode": "text",
   "reason": "rule 5: a symbolic rule, BC-REP-01 only",
   "sources": [
    "BC-SKL-02031"
   ]
  },
  {
   "block": "ex-1",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  },
  {
   "block": "err-BC-ERR-02015",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  },
  {
   "block": "err-BC-ERR-02016",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  }
 ],
 "refresher": [
  "ki-1",
  "err-BC-ERR-02015",
  "err-BC-ERR-02016",
  "ex-1"
 ],
 "read_minutes": {
  "full": 3.2,
  "brief": 3.0
 },
 "word_count": {
  "full": 472,
  "brief": 446
 },
 "research_lines": [
  {
   "file": "research/units/unit-02-differentiation-definition-properties.md",
   "line": "MCQ forms ask for the derivative of a polynomial or of a linear combination."
  }
 ],
 "inferred": [
  {
   "claim": "BC-QA-02006 records no wrong_approaches and no prohibited_shortcuts, so st-1's rival is taken from BC-ERR-02016, whose skills the archetype loads.",
   "settles": "A library staging pass adding wrong_approaches to BC-QA-02006."
  },
  {
   "claim": "BC-QA-02006 is the only archetype loading this concept's skills and it is shared with BC-CON-02010, so the example carries a reciprocal term from its spec rather than a pure polynomial.",
   "settles": "An archetype record whose parameter_spec draws polynomials with constant terms only."
  },
  {
   "claim": "No non-text delivery mode serves this concept better than text and step reveal.",
   "settles": "The modality A/B in the build plan: skip rate and time to first credited success by mode."
  }
 ],
 "sources": [
  "BC-CON-02011",
  "BC-SKL-02028",
  "BC-SKL-02029",
  "BC-SKL-02030",
  "BC-SKL-02031",
  "BC-EK-FUN-3A2",
  "BC-EK-FUN-3A3",
  "ced:65",
  "BC-QA-02006",
  "BC-ERR-02015",
  "BC-ERR-02016",
  "BC-MIS-02009",
  "BC-PRQ-02004",
  "research/units/unit-02-differentiation-definition-properties.md#2.6 Derivative Rules: Constant, Sum, Difference, and Constant Multiple",
  "research/question-analysis/question-archetypes.md#BC-QA-02006 Derivative of a polynomial or power expression by rule",
  "research/exam/exam-structure.md#Section and part layout"
 ]
}
```
