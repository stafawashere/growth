---
title: LSN-CON-02010 The power rule
research_date: 2026-09-29
status: designed
purpose: Authoring spec for the concept lesson on BC-CON-02010, the power rule, built from authoring_bundle("BC-CON-02010") and the research files it cites, so an author fills plan 15's lesson record without making a teaching decision.
---

# LSN-CON-02010 The power rule

Concept BC-CON-02010 (skills BC-SKL-02025, BC-SKL-02026, BC-SKL-02027), topic 2.5 of Unit 2, loaded by BC-QA-02006 (primary) and BC-QA-02002. The structure follows LSN-CON-02013.

## Prediction

Served first, both bands, on ex-1's function (source BC-CON-02010 and the topic's 2.5 section, research/units/unit-02-differentiation-definition-properties.md#2.5 Applying the Power Rule). Form `mcq`, three options, key: \(12x^2\) for the term \(4x^3\). The distractors are the two readings the traps record, the exponent lowered with no factor and the factor taken with no lowering. The resolution states the rule and applies it to the term, without a verdict word.

## Orientation

Served text, from BC-CON-02010 `description_plain` and the topic's Assessment behaviour paragraph (research/units/unit-02-differentiation-definition-properties.md#2.5 Applying the Power Rule): the two moves of the rule, the rewriting that comes first, and the definition-derived case. No count, no frequency.

## Key ideas

One BC-EK maps to the three skills, BC-EK-FUN-3A1 (ced:64), so one core block, both bands.

- ki-1 (core). The rule \(rx^{r-1}\), the scope of the exponent (radicals and reciprocals rewritten), and the relation to the definition, paraphrased from the topic's Required mathematical knowledge paragraph. No anchor quote, to hold the brief cap. Notation line from the concept record and topic: power rule; the exponent as a fraction or a negative number.

## Recognition

- BC-QA-02006 (family rule-manipulation, single MCQ, no calculator; research/question-analysis/question-archetypes.md#BC-QA-02006 Derivative of a polynomial or power expression by rule): `typical_wording` "Find the derivative of the given function."; `common_givens` an expression built from powers, radicals and reciprocals; `asked_to_produce` the derivative, and its value at a named input. The signal is a root sign or a variable in a denominator, with no product or quotient of two variable factors.
- BC-QA-02002 (family derivative-definition-limit; research/question-analysis/question-archetypes.md#BC-QA-02002 Derivative computed from the limit definition): `typical_wording` "Use the definition of the derivative to find ..."; `common_givens` a function rule. The signal is the phrase use the definition. `official_examples`: BC-MCQ-SAMPLE-006.

The contrast pair on st-1 takes its near miss from the sibling concepts named below: a product of two variable factors with sine, which calls for the product rule (BC-CON-02013) and BC-CON-02012. The `this` stem is a fresh draw on BC-QA-02006.

What says "not this concept": a product or quotient of two variable factors (BC-CON-02013, 02014); sine, cosine, \(e^x\) or \(\ln x\) (BC-CON-02012), where the exponent move does not apply.

## Method choice

Two strategy blocks, low and mid bands, the first only in mid.

- st-1, BC-QA-02006. Method, `expected_solution_path[0]`, written without a leading label: every radical and reciprocal rewritten as a power. The contrast pair rides on this block. Rival: exponent lowered without the factor (BC-ERR-02015); the archetype records no `wrong_approaches` or `prohibited_shortcuts`, so the rival is [inferred] from the errors its skills carry and the block is tagged inferred. Separating feature: coefficient and exponent change together.
- st-2, BC-QA-02002. Method, `expected_solution_path[0]`, written without a leading label: the difference quotient for the given rule inside the limit. Rival, `wrong_approaches`: the rule dressed as the definition (BC-ERR-02008). Separating feature: the word definition.

## Solution path

- ex-1, BC-QA-02006, both bands, no calculator. Draw: leading 4, degree 3, second radical, second coefficient 6, root index 2, constant \(-5\): \(f(x)=4x^3+6\sqrt{x}-5\). Steps: the given (valued), rewrite (equivalent), differentiate, return to radical form. A fluent solver writes the rewritten line, the derivative and the final form, and reads the given.
- ex-2, BC-QA-02002, low band. Draw: leading 2, linear \(-3\), constant 1, point 1, degree 2: \(f(x)=2x^2-3x+1\), \(f'(1)=1\). Every line is written, because the definition's lines are the work asked for. Faded from step 3: steps 1 and 2 (the quotient and the simplified numerator) are shown, the student writes the limit, and steps 3 and 4 (dividing out the increment, then the limit) then reveal. The fade falls there because the two withheld lines are the ones the trap records (BC-ERR-02005) put at risk.

No productive-failure opener targets this concept, so no comparison callout.

## Scoring

None. Neither BC-QA-02006 nor BC-QA-02002 lists `point_types`, so no step is tagged, no reader checklist is served and the lesson says nothing about points beyond the error records' consequence text.

## Traps

Four active errors meet the concept's skills, in the bundle's order. Low band all four, mid band the first two.

- err-BC-ERR-02005 (BC-MIS-02002), on ex-2: \(h=0\) substituted before dividing out, read as 0, against the limit 1. Distinct.
- err-BC-ERR-02008 (BC-MIS-02002), on ex-2: the rule's \(4(1)-3\) presented as the definition. Equivalent value; the record's consequence is the lost quotient and simplification work.
- err-BC-ERR-02015 (BC-MIS-02009), on ex-1: \(4x^2+6x^{-1/2}\) against \(12x^2+3x^{-1/2}\). Distinct.
- err-BC-ERR-02017 (BC-MIS-02009), on ex-1: the radical copied, \(12x^2+6\sqrt{x}\). Distinct.

## Representations

None. The topic's Representations paragraph names BC-REP-01 only, and the one conversion (a radical or reciprocal to a power) is symbolic.

## Prerequisite bridge

- BC-PRQ-06002 (Exponent rules including negative and fractional exponents), from its `description_plain` and `failure_signature`, served when that state is unmet.

## Time

BC-QA-02006 is `no_calculator` and a single MCQ, so the part is Section I Part A, 2.14 minutes per question (research/exam/exam-structure.md#Section and part layout; plan 15, Fluency). On ex-1 the rewritten line and the derivative carry the time; on ex-2 the four definition lines are all written.

## Checks

- chk-1, completion of ex-1, both bands: the rule line given, the radical restored. Key \(12x^2+\frac{3}{\sqrt{x}}\).
- chk-2, isomorph on BC-QA-02006, both bands: \(f(x)=-2x^4+\frac{5}{x^2}+7\). Key \(-8x^3-\frac{10}{x^3}\).
- chk-3, MCQ on BC-QA-02006, low band: \(f(x)=3x^5+\frac4x-6\). Key \(15x^4-\frac{4}{x^2}\). Distractors: \(3x^4+\frac{4}{x^2}\) (BC-ERR-02015), \(15x^4+\frac4x\) (BC-ERR-02017), \(15x^4+\frac{4}{x^2}\) (BC-ERR-02015 on one term).

No draw equals a published BC-QA-02006 or BC-QA-02002 `parameter_draw`.

## Delivery

- orientation: text. Rule 5, BC-REP-01 only.
- ki-1: text. Rule 5; unit README delivery map.
- ex-1, ex-2: step_reveal. Rule 1.
- err-BC-ERR-02005, err-BC-ERR-02008, err-BC-ERR-02015, err-BC-ERR-02017: step_reveal. Rule 1.

No figure, motion, interactive or model mode applies [inferred; settled by the modality A/B]. `no_figure_reason` states it: the skills carry BC-REP-01 only and no key idea describes a process.

## Band plan

- Low (full): prediction, orientation, the bridge, ki-1, st-1 with the contrast pair, st-2, ex-1, chk-1, err-BC-ERR-02005, err-BC-ERR-02008, err-BC-ERR-02015, err-BC-ERR-02017, ex-2 faded from step 3, chk-2, chk-3. 621 words, 4.2 minutes (cap 900 and 6).
- Mid (brief): prediction, orientation, the bridge, ki-1, st-1 with the contrast pair, ex-1, chk-1, err-BC-ERR-02005, err-BC-ERR-02008, chk-2. 427 words, 2.9 minutes (cap 450 and 3).
- Refresher: ki-1, err-BC-ERR-02005, err-BC-ERR-02008, err-BC-ERR-02015, err-BC-ERR-02017, ex-1.

## Sources

- BC-CON-02010; BC-SKL-02025, BC-SKL-02026, BC-SKL-02027; BC-EK-FUN-3A1; ced:64
- BC-QA-02006, BC-QA-02002; BC-MCQ-SAMPLE-006; BC-CON-02012, BC-CON-02013 (the contrast near miss)
- BC-ERR-02005, BC-ERR-02008, BC-ERR-02015, BC-ERR-02017; BC-MIS-02002, BC-MIS-02009
- BC-PRQ-06002
- research/units/unit-02-differentiation-definition-properties.md#2.5 Applying the Power Rule
- research/question-analysis/question-archetypes.md#BC-QA-02006 Derivative of a polynomial or power expression by rule
- research/question-analysis/question-archetypes.md#BC-QA-02002 Derivative computed from the limit definition
- research/exam/exam-structure.md#Section and part layout
- [inferred] st-1's rival, BC-QA-02006 having no `wrong_approaches`. Settled by a staging pass adding them.
- [inferred] No non-text mode. Settled by the modality A/B.

## Machine record

```json
{
 "id": "LSN-CON-02010",
 "kind": "concept",
 "target_id": "BC-CON-02010",
 "unit": "02",
 "skills": [
  "BC-SKL-02025",
  "BC-SKL-02026",
  "BC-SKL-02027"
 ],
 "prediction": {
  "id": "pr-1",
  "stem": {
   "text": "Predict before the rule: the term \\(4x^3\\) of \\(f(x)=4x^3+6\\sqrt{x}-5\\) has which derivative?",
   "command_verb": "predict"
  },
  "format": "mcq",
  "options": [
   {
    "id": "A",
    "label": "\\(4x^2\\)",
    "is_key": false
   },
   {
    "id": "B",
    "label": "\\(12x^2\\)",
    "is_key": true
   },
   {
    "id": "C",
    "label": "\\(12x^3\\)",
    "is_key": false
   }
  ],
  "resolution": "The derivative of \\(x^r\\) is \\(rx^{r-1}\\): multiply by the exponent, then lower it by one. So \\(4x^3\\) gives \\(3\\cdot4x^2=12x^2\\).",
  "sources": [
   "BC-CON-02010",
   "research/units/unit-02-differentiation-definition-properties.md#2.5 Applying the Power Rule"
  ]
 },
 "no_figure_reason": "The power rule is symbolic and its skills carry BC-REP-01 only. No key idea describes a process or a graph, so no figure, table or motion fits.",
 "orientation": {
  "text": "A response differentiates a power by multiplying by the exponent and lowering it by one, after rewriting any radical or reciprocal as a power. Some questions ask for a case derived from the definition.",
  "sources": [
   "BC-CON-02010",
   "research/units/unit-02-differentiation-definition-properties.md#2.5 Applying the Power Rule"
  ]
 },
 "key_ideas": [
  {
   "id": "ki-1",
   "ek_id": "BC-EK-FUN-3A1",
   "depth": "core",
   "text": "For \\(f(x)=x^r\\) the derivative is \\(rx^{r-1}\\): multiply by the old exponent, then lower it by one. A radical or a reciprocal is first rewritten as a power: \\(\\sqrt{x}=x^{1/2}\\), \\(\\frac{1}{x^2}=x^{-2}\\). For one specific exponent the rule also comes out of the difference quotient, by expanding and dividing out the increment.",
   "notation": "power rule; the exponent written as a fraction or a negative number",
   "quote": null,
   "sources": [
    "BC-EK-FUN-3A1",
    "ced:64",
    "research/units/unit-02-differentiation-definition-properties.md#2.5 Applying the Power Rule"
   ]
  }
 ],
 "strategy": [
  {
   "id": "st-1",
   "archetype_id": "BC-QA-02006",
   "cue": "The stem asks for the derivative of an expression built from powers, radicals and reciprocals.",
   "method": "The expression with every radical and reciprocal rewritten as a power.",
   "rival": "Lowering the exponent without multiplying by it.",
   "separating_feature": "Each term changes coefficient and exponent together.",
   "sources": [
    "BC-QA-02006",
    "BC-ERR-02015"
   ],
   "evidence_tag": "inferred",
   "contrast": {
    "this": {
     "text": "Find \\(g'(x)\\) for \\(g(x)=5x^4-\\frac{2}{\\sqrt{x}}+9\\).",
     "archetype_id": "BC-QA-02006"
    },
    "not_this": {
     "text": "Find \\(g'(x)\\) for \\(g(x)=x^2\\sin x\\).",
     "why_not": "A product of two variable factors, one of them sine, calls for the product rule."
    },
    "feature": "Each term is one power of \\(x\\), not a product of variable factors."
   }
  },
  {
   "id": "st-2",
   "archetype_id": "BC-QA-02002",
   "cue": "The stem says use the definition of the derivative, from a function rule.",
   "method": "The difference quotient for the given rule inside the limit.",
   "rival": "Differentiating by the power rule and presenting it as the definition.",
   "separating_feature": "The word definition in the stem forbids the rule as the route.",
   "sources": [
    "BC-QA-02002"
   ],
   "evidence_tag": "verified"
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
    "leading": "4",
    "degree": "3",
    "second": "radical",
    "second_coefficient": "6",
    "root_index": "2",
    "reciprocal_power": "1",
    "constant": "-5"
   },
   "problem": {
    "text": "Let \\(f(x)=4x^3+6\\sqrt{x}-5\\). Find \\(f'(x)\\).",
    "command_verb": "find"
   },
   "calculator_status": "no_calculator",
   "steps": [
    {
     "cue": "The stem gives a radical term.",
     "why": "The rule needs every term as a power.",
     "expr": "4*x**3+6*sqrt(x)-5",
     "relation": "new"
    },
    {
     "cue": "Rewrite \\(\\sqrt{x}\\) as \\(x^{1/2}\\).",
     "why": "Now each term is a power of \\(x\\).",
     "expr": "4*x**3+6*x**(1/2)-5",
     "relation": "equivalent"
    },
    {
     "cue": "Differentiate term by term: multiply by each exponent, lower it by one.",
     "why": "\\(3\\cdot4=12\\), \\(\\frac12\\cdot6=3\\); the constant goes to 0.",
     "expr": "12*x**2+3*x**(-1/2)",
     "relation": "differentiate",
     "variable": "x"
    },
    {
     "cue": "The stem gave a radical, so return to that form.",
     "why": "\\(x^{-1/2}=\\frac{1}{\\sqrt{x}}\\).",
     "expr": "12*x**2+3/sqrt(x)",
     "relation": "equivalent"
    }
   ],
   "answer": {
    "form": "symbolic",
    "expr": "12*x**2+3/sqrt(x)"
   }
  },
  {
   "id": "ex-2",
   "archetype_id": "BC-QA-02002",
   "bands": [
    "low"
   ],
   "fade_from": 3,
   "parameter_draw": {
    "leading": "2",
    "linear": "-3",
    "constant": "1",
    "point": "1",
    "degree": "2"
   },
   "problem": {
    "text": "Let \\(f(x)=2x^2-3x+1\\). Use the definition of the derivative to find \\(f'(1)\\).",
    "command_verb": "find"
   },
   "calculator_status": "no_calculator",
   "steps": [
    {
     "cue": "The stem says use the definition: write the quotient, \\(f(1)=0\\).",
     "why": "The quotient is the demanded work, not a ritual line.",
     "expr": "(2*(1+h)**2-3*(1+h)+1-0)/h",
     "relation": "new"
    },
    {
     "cue": "Expand and simplify the numerator.",
     "why": "The constant and linear parts cancel down to \\(2h^2+h\\).",
     "expr": "(2*h**2+h)/h",
     "relation": "equivalent"
    },
    {
     "cue": "Divide out the increment before any substitution.",
     "why": "\\(h\\) is not zero inside the limit.",
     "expr": "2*h+1",
     "relation": "equivalent"
    },
    {
     "cue": "Now let \\(h\\to0\\).",
     "why": "Substitution is safe once \\(h\\) is gone from the denominator.",
     "expr": "1",
     "relation": "limit",
     "variable": "h",
     "point": "0"
    }
   ],
   "answer": {
    "form": "numeric",
    "expr": "1"
   }
  }
 ],
 "what_a_reader_scores": [],
 "common_errors": [
  {
   "error_id": "BC-ERR-02005",
   "observed_behavior": "The response substitutes zero for the increment while it is still in the denominator.",
   "scoring_consequence": "The simplification point and the value point are both lost.",
   "wrong_step": {
    "text": "On ex-2: \\(h=0\\) put into \\(\\frac{2h^2+h}{h}\\) at once; the numerator is read as 0.",
    "expr": "0"
   },
   "right_step": {
    "text": "Divide out \\(h\\) first: \\(2h+1\\to1\\).",
    "expr": "1"
   },
   "relation": "distinct",
   "fix_prompt": true,
   "possible_reason": {
    "misconception_id": "BC-MIS-02002",
    "text": "the increment is set to zero immediately"
   },
   "sources": [
    "BC-ERR-02005",
    "BC-MIS-02002"
   ]
  },
  {
   "error_id": "BC-ERR-02008",
   "observed_behavior": "The response differentiates with the power rule and presents the result as an application of the definition.",
   "scoring_consequence": "The points attached to the difference quotient and its simplification are lost although the final value may be right.",
   "wrong_step": {
    "text": "On ex-2: \\(f'(x)=4x-3\\) by rule, so \\(f'(1)=1\\), labelled the definition.",
    "expr": "4*1-3"
   },
   "right_step": {
    "text": "The quotient simplified to \\(2h+1\\), limit 1.",
    "expr": "1"
   },
   "relation": "equivalent",
   "fix_prompt": false,
   "possible_reason": {
    "misconception_id": "BC-MIS-02002",
    "text": "the answer is produced by a rule and the definition is copied around it"
   },
   "sources": [
    "BC-ERR-02008",
    "BC-MIS-02002"
   ]
  },
  {
   "error_id": "BC-ERR-02015",
   "observed_behavior": "The response lowers the exponent by one but omits the factor of the original exponent.",
   "scoring_consequence": "The derivative point is lost.",
   "wrong_step": {
    "text": "\\(4x^2+6x^{-1/2}\\): exponents lowered, factors 3 and \\(\\frac12\\) missing.",
    "expr": "4*x**2+6*x**(-1/2)"
   },
   "right_step": {
    "text": "\\(12x^2+3x^{-1/2}\\).",
    "expr": "12*x**2+3*x**(-1/2)"
   },
   "relation": "distinct",
   "fix_prompt": true,
   "possible_reason": {
    "misconception_id": "BC-MIS-02009",
    "text": "the exponent decreasing but not the multiplication by the original exponent"
   },
   "sources": [
    "BC-ERR-02015",
    "BC-MIS-02009"
   ]
  },
  {
   "error_id": "BC-ERR-02017",
   "observed_behavior": "The response differentiates the polynomial terms and copies a radical or reciprocal term unchanged.",
   "scoring_consequence": "The derivative point is lost.",
   "wrong_step": {
    "text": "\\(12x^2+6\\sqrt{x}\\): the radical copied.",
    "expr": "12*x**2+6*sqrt(x)"
   },
   "right_step": {
    "text": "\\(12x^2+\\frac{3}{\\sqrt{x}}\\).",
    "expr": "12*x**2+3/sqrt(x)"
   },
   "relation": "distinct",
   "fix_prompt": true,
   "possible_reason": {
    "misconception_id": "BC-MIS-02009",
    "text": "does not see constants and radicals as powers"
   },
   "sources": [
    "BC-ERR-02017",
    "BC-MIS-02009"
   ]
  }
 ],
 "representations": null,
 "prerequisite_bridges": [
  {
   "prq_id": "BC-PRQ-06002",
   "text": "The rule runs on exponents, so radicals and reciprocals are converted to powers first: \\(\\sqrt[3]{x}=x^{1/3}\\), \\(\\frac{1}{x}=x^{-1}\\). A radical or reciprocal left unrewritten is the gap to close first."
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
   ],
   "ex-2": [
    1,
    2,
    3,
    4
   ]
  },
  "skipped_steps": {
   "ex-1": [
    1
   ],
   "ex-2": []
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
    "leading": "4",
    "degree": "3",
    "second": "radical",
    "second_coefficient": "6",
    "root_index": "2",
    "reciprocal_power": "1",
    "constant": "-5"
   },
   "completes": "ex-1",
   "stem": {
    "text": "For \\(f(x)=4x^3+6\\sqrt{x}-5\\), the rule gives \\(12x^2+3x^{-1/2}\\). Write \\(f'(x)\\) with the radical restored.",
    "command_verb": "write"
   },
   "key": {
    "form": "symbolic",
    "expr": "12*x**2+3/sqrt(x)"
   },
   "steps": [
    {
     "text": "The rule line.",
     "expr": "12*x**2+3*x**(-1/2)",
     "relation": "new"
    },
    {
     "text": "\\(x^{-1/2}=\\frac{1}{\\sqrt{x}}\\).",
     "expr": "12*x**2+3/sqrt(x)",
     "relation": "equivalent"
    }
   ],
   "calculator_status": "no_calculator",
   "skills": [
    "BC-SKL-02026"
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
    "leading": "-2",
    "degree": "4",
    "second": "reciprocal",
    "second_coefficient": "5",
    "root_index": "2",
    "reciprocal_power": "2",
    "constant": "7"
   },
   "stem": {
    "text": "Let \\(f(x)=-2x^4+\\frac{5}{x^2}+7\\). Find \\(f'(x)\\).",
    "command_verb": "find"
   },
   "key": {
    "form": "symbolic",
    "expr": "-8*x**3-10/x**3"
   },
   "steps": [
    {
     "text": "Rewrite: \\(-2x^4+5x^{-2}+7\\).",
     "expr": "-2*x**4+5*x**(-2)+7",
     "relation": "new"
    },
    {
     "text": "Differentiate.",
     "expr": "-8*x**3-10*x**(-3)",
     "relation": "differentiate",
     "variable": "x"
    },
    {
     "text": "Return to fraction form.",
     "expr": "-8*x**3-10/x**3",
     "relation": "equivalent"
    }
   ],
   "calculator_status": "no_calculator",
   "skills": [
    "BC-SKL-02026"
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
    "leading": "3",
    "degree": "5",
    "second": "reciprocal",
    "second_coefficient": "4",
    "root_index": "2",
    "reciprocal_power": "1",
    "constant": "-6"
   },
   "stem": {
    "text": "If \\(f(x)=3x^5+\\frac{4}{x}-6\\), then \\(f'(x)=\\)",
    "command_verb": "find"
   },
   "key": {
    "form": "symbolic",
    "expr": "15*x**4-4/x**2"
   },
   "steps": [
    {
     "text": "Rewrite: \\(3x^5+4x^{-1}-6\\).",
     "expr": "3*x**5+4*x**(-1)-6",
     "relation": "new"
    },
    {
     "text": "Differentiate.",
     "expr": "15*x**4-4*x**(-2)",
     "relation": "differentiate",
     "variable": "x"
    },
    {
     "text": "Fraction form.",
     "expr": "15*x**4-4/x**2",
     "relation": "equivalent"
    }
   ],
   "options": [
    {
     "id": "A",
     "is_key": false,
     "expr": "3*x**4+4/x**2",
     "error_path": "BC-ERR-02015",
     "derivation": "exponents lowered on both terms, factors 5 and -1 omitted"
    },
    {
     "id": "B",
     "is_key": true,
     "expr": "15*x**4-4/x**2",
     "error_path": null
    },
    {
     "id": "C",
     "is_key": false,
     "expr": "15*x**4+4/x",
     "error_path": "BC-ERR-02017",
     "derivation": "the reciprocal term copied unchanged"
    },
    {
     "id": "D",
     "is_key": false,
     "expr": "15*x**4+4/x**2",
     "error_path": "BC-ERR-02015",
     "derivation": "the factor -1 omitted on the reciprocal term"
    }
   ],
   "calculator_status": "no_calculator",
   "skills": [
    "BC-SKL-02026"
   ]
  }
 ],
 "delivery": [
  {
   "block": "orientation",
   "mode": "text",
   "reason": "rule 5: BC-REP-01 only on BC-SKL-02025 to 02027; unit README delivery map",
   "sources": [
    "BC-SKL-02025"
   ]
  },
  {
   "block": "ki-1",
   "mode": "text",
   "reason": "rule 5: a symbolic rule with no figure-bearing BC-REP; unit README delivery map",
   "sources": [
    "BC-SKL-02025",
    "BC-SKL-02026"
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
   "block": "err-BC-ERR-02005",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  },
  {
   "block": "err-BC-ERR-02008",
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
   "block": "err-BC-ERR-02017",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  }
 ],
 "refresher": [
  "ki-1",
  "err-BC-ERR-02005",
  "err-BC-ERR-02008",
  "err-BC-ERR-02015",
  "err-BC-ERR-02017",
  "ex-1"
 ],
 "read_minutes": {"full": 4.2, "brief": 2.9},
 "word_count": {"full": 621, "brief": 427},
 "research_lines": [
  {
   "file": "research/units/unit-02-differentiation-definition-properties.md",
   "line": "MCQ forms ask for the derivative of a power or of an expression that becomes one after rewriting."
  }
 ],
 "inferred": [
  {
   "claim": "BC-QA-02006 records no wrong_approaches and no prohibited_shortcuts, so st-1's rival is taken from BC-ERR-02015, whose skills the archetype loads.",
   "settles": "A library staging pass adding wrong_approaches to BC-QA-02006."
  },
  {
   "claim": "No non-text delivery mode serves this concept better than text and step reveal.",
   "settles": "The modality A/B in the build plan: skip rate and time to first credited success by mode."
  }
 ],
 "sources": [
  "BC-CON-02010",
  "BC-SKL-02025",
  "BC-SKL-02026",
  "BC-SKL-02027",
  "BC-EK-FUN-3A1",
  "ced:64",
  "BC-QA-02006",
  "BC-QA-02002",
  "BC-MCQ-SAMPLE-006",
  "BC-ERR-02005",
  "BC-ERR-02008",
  "BC-ERR-02015",
  "BC-ERR-02017",
  "BC-MIS-02002",
  "BC-MIS-02009",
  "BC-PRQ-06002",
  "research/units/unit-02-differentiation-definition-properties.md#2.5 Applying the Power Rule",
  "research/question-analysis/question-archetypes.md#BC-QA-02006 Derivative of a polynomial or power expression by rule",
  "research/question-analysis/question-archetypes.md#BC-QA-02002 Derivative computed from the limit definition",
  "research/exam/exam-structure.md#Section and part layout"
 ]
}
```
