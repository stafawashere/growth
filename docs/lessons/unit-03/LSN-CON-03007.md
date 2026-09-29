---
title: LSN-CON-03007 Derivatives of inverse trigonometric functions
research_date: 2026-09-29
status: designed
purpose: Authoring spec for the concept lesson on BC-CON-03007, derivatives of the inverse sine, cosine and tangent with an inner function, built from authoring_bundle("BC-CON-03007") and the research files it cites, so an author fills plan 15's lesson record without making a teaching decision.
---

# LSN-CON-03007 Derivatives of inverse trigonometric functions

Concept BC-CON-03007 (skills BC-SKL-03021 to BC-SKL-03025), topic 3.4 of Unit 3, loaded by three archetypes in three families: BC-QA-03007 (primary, rule-manipulation), BC-QA-03010 (inverse-function-derivative, the derivation) and BC-QA-06018 (antidifferentiation-technique, through BC-SKL-03021). Its hard parent concepts are BC-CON-03002, BC-CON-03003 and BC-CON-03006 (docs/lessons/unit-03/README.md, section 1).

## Orientation

Served text, from BC-CON-03007 `description_plain` and the topic's Assessment behaviour paragraph (research/units/unit-03-differentiation-composite-implicit-inverse.md#3.4 Differentiating Inverse Trigonometric Functions): a response writes the standard formula with the inner expression in place of x, multiplies by the inner derivative, and keeps any enclosing product rule. No count, no frequency.

## Key ideas

All five skills map to BC-EK-FUN-3E2 (ced:78), so one core block, both bands.

- ki-1 (core). Paraphrase of the Required mathematical knowledge paragraphs (Standard derivatives, Composite form, Derivation): the three formulas, the extra factor u' for an inner function u, and the route back through the trigonometric equation and a Pythagorean identity. No anchor quote, to keep the brief band under 450 words. Notation line from the concept record.

## Recognition

BC-QA-03007 (research/question-analysis/question-archetypes.md#BC-QA-03007 Inverse trigonometric derivative with an inner function): `typical_wording` "find the derivative of the given inverse trigonometric expression", "find the rate of change of the modelled quantity at the stated time"; `common_givens` an inverse trigonometric function of an inner expression, a contextual inverse tangent model; `asked_to_produce` the derivative, or a rate at a stated time. Signal: arcsin, arccos or arctan with anything other than a bare x inside. Shape: one MCQ (official example BC-MCQ-PE2012-007), or a step inside a contextual FRQ where the derivative is often supplied (sg-25:2, sg-25:4).

BC-QA-03010: the identity tan(g(x)) = u is given with the instruction to differentiate both sides. BC-QA-06018 (research/question-analysis/question-archetypes.md#BC-QA-06018 Antiderivative matched to an inverse trigonometric form, directly or after completing the square): a constant over a sum of squares, or over the root of a difference of squares, to be integrated.

What says "not this concept": sin, cos or tan with no inverse (a Unit 2 derivative), or a named inverse g of a general f (BC-CON-03006).

## Method choice

Three strategy blocks, one per archetype family; st-1 serves both bands.

- st-1, BC-QA-03007. Method, `expected_solution_path[0]`: the standard derivative with the inner expression substituted. Rival, `wrong_approaches`: the inverse sine formula used for the inverse tangent (BC-ERR-03017). Separating feature: arctan carries no radical.
- st-2, BC-QA-03010. Method: differentiate both sides of the identity with the chain rule on the left. Rival, `wrong_approaches`: a remembered formula without the inner factor.
- st-3, BC-QA-06018. Method: complete the square where the quadratic is expanded. Rival, `wrong_approaches`: a logarithm forced with the quadratic as u and its derivative absent. Separating feature: the numerator is a constant.

All three archetypes carry `asked_to_produce` and `common_givens`, so none is tagged inferred.

## Solution path

- ex-1, BC-QA-03007, both bands, no calculator. Draw from `parameter_spec`: family arctan, inner linear, slope 2, at 2, coefficient 3, power 1, sign 1; the inner expression is 2x - 3 so that it equals sign = 1 at x = 2. h(x) = 3x arctan(2x - 3). Constraint holds: arctan with |at| = 2. No published BC-QA-03007 item carries this draw.
- Steps: the arctan factor (new); its derivative, formula with u and u' (differentiate); the product rule assembled (new); the value at x = 2 (evaluate). A fluent solver writes steps 2 to 4 as one line and the value; step 1 is the classification, held in the head.

## Scoring

BC-QA-03007, BC-QA-03010 and BC-QA-06018 list no `point_types`, so no what_a_reader_scores entry and no point tag. For the author: in the 2025 contextual question the derivative is supplied and later parts score its use (sg-25:2, sg-25:4, per the archetype's scoring pattern).

## Traps

Three active errors meet the skills, in the bundle's order: BC-ERR-03006, BC-ERR-03018, BC-ERR-03017. Low band all three; mid band the first two. All on ex-1's draw, as expressions for h'(x).

- err-BC-ERR-03006: the product rule dropped, only 3x times the arctan derivative. Possible reason, words from BC-MIS-03012.
- err-BC-ERR-03018: the inner factor 2 dropped. Possible reason, words from BC-MIS-03001.
- err-BC-ERR-03017: the radical of the inverse sine form carried into the arctan formula, which still gives a value at x = 2 (3π/4 + 6√2 against 3π/4 + 6). Possible reason, words from BC-MIS-03010.

## Representations

None. The topic's Representations paragraph names BC-REP-01, BC-REP-05 and BC-REP-09, none figure-shaped.

## Prerequisite bridge

- BC-PRQ-03004, from its `description_plain` and `failure_signature`.
- BC-PRQ-03006, from its `description_plain` and `failure_signature`.

## Time

BC-QA-03007 is `calculator_status` either, a single MCQ or a step inside a contextual FRQ. The design takes Section I Part A, 2.14 minutes per question (research/exam/exam-structure.md#Section and part layout) [inferred: an either archetype placed in I-A]. The minutes go on the derivative line; the value at the point is arithmetic on arctan(1).

## Checks

- chk-1, completion of ex-1, both bands: h'(x) is given, the student evaluates at x = 2. Key 3π/4 + 6.
- chk-2, isomorph, both bands. Draw: arcsin, linear, slope 3, at 1, coefficient 2, power 1, sign 1; inner 3x - 5/2, equal to 1/2 at x = 1. h(x) = 2x arcsin(3x - 5/2). Key h'(1) = π/3 + 4√3.
- chk-3, MCQ, low band. Draw: arctan, linear, slope 3, at -2, coefficient 1, power 2, sign -1; inner 3x + 5, equal to -1 at x = -2. h(x) = x^2 arctan(3x + 5). Key h'(-2) = π + 6. Distractors: 6 (BC-ERR-03006), π + 2 (BC-ERR-03018), π - 6 (BC-ERR-03017, the sign misplaced).

## Delivery

- orientation, ki-1: text. Rule 5: the skills carry BC-REP-01 and BC-REP-09, neither figure-bearing (docs/lessons/unit-03/README.md, section 6).
- ex-1: step_reveal. Rule 1.
- err-BC-ERR-03006, err-BC-ERR-03018, err-BC-ERR-03017: step_reveal. Rule 1.

## Band plan

- Low (full): orientation, ki-1, st-1 to st-3, ex-1, the three error blocks, chk-1 to chk-3, the two bridges. 586 words, 3.91 minutes (cap 900 and 6).
- Mid (brief): orientation, ki-1, st-1, ex-1, err-BC-ERR-03006, err-BC-ERR-03018, chk-1, chk-2, the two bridges. 407 words, 2.8 minutes (cap 450 and 3).
- Refresher: ki-1, err-BC-ERR-03006, err-BC-ERR-03018, err-BC-ERR-03017, ex-1.

## Sources

- BC-CON-03007; BC-SKL-03021, BC-SKL-03022, BC-SKL-03023, BC-SKL-03024, BC-SKL-03025; BC-EK-FUN-3E2; ced:78
- BC-QA-03007, BC-QA-03010, BC-QA-06018; BC-MCQ-PE2012-007; sg-25:2, sg-25:4
- BC-ERR-03006, BC-ERR-03018, BC-ERR-03017; BC-MIS-03012, BC-MIS-03001, BC-MIS-03010
- BC-PRQ-03004, BC-PRQ-03006
- research/units/unit-03-differentiation-composite-implicit-inverse.md#3.4 Differentiating Inverse Trigonometric Functions
- research/question-analysis/question-archetypes.md#BC-QA-03007 Inverse trigonometric derivative with an inner function
- research/question-analysis/question-archetypes.md#BC-QA-06018 Antiderivative matched to an inverse trigonometric form, directly or after completing the square
- research/exam/exam-structure.md#Section and part layout
- [inferred] BC-QA-03007 is placed in Section I Part A although its calculator status is either. Settled by the section of BC-MCQ-PE2012-007 recorded on the archetype.

## Machine record

```json
{
 "id": "LSN-CON-03007",
 "kind": "concept",
 "target_id": "BC-CON-03007",
 "unit": "03",
 "skills": ["BC-SKL-03021", "BC-SKL-03022", "BC-SKL-03023", "BC-SKL-03024", "BC-SKL-03025"],
 "orientation": {
  "text": "A response writes the standard inverse trigonometric formula with the inner expression in place of x, multiplies by the inner derivative, and keeps any product rule around it.",
  "sources": ["BC-CON-03007", "research/units/unit-03-differentiation-composite-implicit-inverse.md#3.4 Differentiating Inverse Trigonometric Functions"]
 },
 "key_ideas": [
  {
   "id": "ki-1",
   "ek_id": "BC-EK-FUN-3E2",
   "depth": "core",
   "text": "arcsin x has derivative 1/sqrt(1 - x^2), arccos x its negative, arctan x has 1/(1 + x^2). With an inner function u, the formula takes u in place of x and gains the factor u'. Each formula comes back from the trigonometric equation, such as tan y = x, differentiated implicitly with a Pythagorean identity.",
   "notation": "derivative of arctan u equals u prime over one plus u squared",
   "quote": null,
   "sources": ["BC-EK-FUN-3E2", "ced:78", "research/units/unit-03-differentiation-composite-implicit-inverse.md#3.4 Differentiating Inverse Trigonometric Functions"]
  }
 ],
 "strategy": [
  {
   "id": "st-1",
   "archetype_id": "BC-QA-03007",
   "cue": "arcsin or arctan of an inner expression, often one factor of a product, and a derivative or rate asked.",
   "method": "First line: the standard formula with the inner expression for x, times its derivative.",
   "rival": "Rival: the arcsin formula used for arctan (BC-ERR-03017).",
   "separating_feature": "arctan: u' over 1 + u^2, no radical. arcsin: a root of 1 - u^2.",
   "sources": ["BC-QA-03007"],
   "evidence_tag": "verified"
  },
  {
   "id": "st-2",
   "archetype_id": "BC-QA-03010",
   "cue": "An identity such as tan(g(x)) = u is supplied and g' is asked for in x.",
   "method": "First line: differentiate both sides, chain rule on the left.",
   "rival": "Rival: a remembered formula without the inner factor.",
   "separating_feature": "The stem supplies the identity, so the derivation is the answer.",
   "sources": ["BC-QA-03010"],
   "evidence_tag": "verified"
  },
  {
   "id": "st-3",
   "archetype_id": "BC-QA-06018",
   "cue": "A constant over a quadratic, or over its square root, to be integrated.",
   "method": "First line: complete the square when the quadratic is expanded.",
   "rival": "Rival: a logarithm, with the quadratic as u and its derivative absent.",
   "separating_feature": "The numerator is a constant, so u'/u is not there.",
   "sources": ["BC-QA-06018"],
   "evidence_tag": "verified"
  }
 ],
 "worked_examples": [
  {
   "id": "ex-1",
   "archetype_id": "BC-QA-03007",
   "bands": ["low", "mid"],
   "parameter_draw": {"family": "arctan", "inner": "linear", "slope": 2, "at": 2, "coefficient": 3, "power": 1, "sign": 1},
   "problem": {"text": "h(x) = 3x arctan(2x - 3). Find h'(2).", "command_verb": "find"},
   "calculator_status": "no_calculator",
   "steps": [
    {"cue": "Last operation: 3x times arctan(2x - 3), a product.", "why": "Product rule outside; the arctan factor needs its own derivative.", "expr": "atan(2*x - 3)", "relation": "new"},
    {"cue": "arctan of u, with u = 2x - 3.", "why": "u' over 1 + u^2; u' = 2.", "expr": "2/(1 + (2*x - 3)**2)", "relation": "differentiate", "variable": "x"},
    {"cue": "Product rule on 3x and the arctan factor.", "why": "Both terms: 3 times arctan, plus 3x times its derivative.", "expr": "3*atan(2*x - 3) + 3*x*2/(1 + (2*x - 3)**2)", "relation": "new"},
    {"cue": "The stem asks for x = 2, where u = 1.", "why": "arctan(1) = π/4, and 1 + u^2 = 2.", "expr": "3*pi/4 + 6", "relation": "evaluate", "subs": {"x": "2"}}
   ],
   "answer": {"form": "symbolic", "expr": "3*pi/4 + 6"}
  }
 ],
 "what_a_reader_scores": [],
 "common_errors": [
  {
   "error_id": "BC-ERR-03006",
   "observed_behavior": "The composite factor is differentiated correctly but the enclosing product or quotient rule is not applied.",
   "scoring_consequence": "The derivative is wrong; in the 2025 implicit differentiation task the product rule carries its own scoring point (sg-25:20).",
   "wrong_step": {"text": "3x times the arctan derivative only.", "expr": "3*x*2/(1 + (2*x - 3)**2)"},
   "right_step": {"text": "Both product rule terms.", "expr": "3*atan(2*x - 3) + 3*x*2/(1 + (2*x - 3)**2)"},
   "relation": "distinct",
   "possible_reason": {"misconception_id": "BC-MIS-03012", "text": "selects a rule by the visual pattern of the expression rather than by the operation applied last"},
   "sources": ["BC-ERR-03006", "BC-MIS-03012"]
  },
  {
   "error_id": "BC-ERR-03018",
   "observed_behavior": "The standard formula is written with the variable rather than the inner expression in the denominator, or the inner derivative factor is omitted.",
   "scoring_consequence": "The derivative is wrong; the missing factor is the chain rule element the formula requires.",
   "wrong_step": {"text": "The factor 2 dropped.", "expr": "3*atan(2*x - 3) + 3*x/(1 + (2*x - 3)**2)"},
   "right_step": {"text": "Times u' = 2.", "expr": "3*atan(2*x - 3) + 6*x/(1 + (2*x - 3)**2)"},
   "relation": "distinct",
   "possible_reason": {"misconception_id": "BC-MIS-03001", "text": "whatever sits inside is copied across unchanged"},
   "sources": ["BC-ERR-03018", "BC-MIS-03001"]
  },
  {
   "error_id": "BC-ERR-03017",
   "observed_behavior": "The derivative of the inverse sine is used for the inverse tangent, or a sign or a radical is misplaced in the recalled formula.",
   "scoring_consequence": "The derivative is wrong from the first line.",
   "wrong_step": {"text": "A radical misplaced: the arctan form written with a root, 6x over the root of 1 + (2x - 3)^2; at x = 2 it gives 3π/4 + 6√2.", "expr": "3*atan(2*x - 3) + 6*x/sqrt(1 + (2*x - 3)**2)"},
   "right_step": {"text": "The arctan form, no radical; at x = 2 it gives 3π/4 + 6.", "expr": "3*atan(2*x - 3) + 6*x/(1 + (2*x - 3)**2)"},
   "relation": "distinct",
   "possible_reason": {"misconception_id": "BC-MIS-03010", "text": "selects among them by resemblance"},
   "sources": ["BC-ERR-03017", "BC-MIS-03010"]
  }
 ],
 "representations": null,
 "prerequisite_bridges": [
  {"prq_id": "BC-PRQ-03004", "text": "Exact values such as arctan(1) = π/4 and the Pythagorean identities carry the evaluation and the derivation; without them the derivative cannot be derived or evaluated."},
  {"prq_id": "BC-PRQ-03006", "text": "A wrong simplification after a correct derivative changes the value reported."}
 ],
 "time": {"exam_part": "I-A", "budget_minutes": 2.14, "source": "research/exam/exam-structure.md#Section and part layout", "written_steps": {"ex-1": [2, 3, 4]}, "skipped_steps": {"ex-1": [1]}},
 "checks": [
  {
   "id": "chk-1",
   "check_kind": "completion",
   "format": "short_answer",
   "bands": ["low", "mid"],
   "archetype_id": "BC-QA-03007",
   "parameter_draw": {"family": "arctan", "inner": "linear", "slope": 2, "at": 2, "coefficient": 3, "power": 1, "sign": 1},
   "completes": "ex-1",
   "stem": {"text": "h'(x) = 3 arctan(2x - 3) + 6x/(1 + (2x - 3)^2). Find h'(2).", "command_verb": "find"},
   "key": {"form": "symbolic", "expr": "3*pi/4 + 6"},
   "steps": [
    {"text": "The derivative.", "expr": "3*atan(2*x - 3) + 6*x/(1 + (2*x - 3)**2)", "relation": "new"},
    {"text": "x = 2.", "expr": "3*pi/4 + 6", "relation": "evaluate", "subs": {"x": "2"}}
   ],
   "calculator_status": "no_calculator",
   "skills": ["BC-SKL-03024"]
  },
  {
   "id": "chk-2",
   "check_kind": "isomorph",
   "format": "short_answer",
   "bands": ["low", "mid"],
   "archetype_id": "BC-QA-03007",
   "parameter_draw": {"family": "arcsin", "inner": "linear", "slope": 3, "at": 1, "coefficient": 2, "power": 1, "sign": 1},
   "stem": {"text": "h(x) = 2x arcsin(3x - 5/2). Find h'(1).", "command_verb": "find"},
   "key": {"form": "symbolic", "expr": "pi/3 + 4*sqrt(3)"},
   "steps": [
    {"text": "h(x).", "expr": "2*x*asin(3*x - 5/2)", "relation": "new"},
    {"text": "Product rule, arcsin of u times u' = 3.", "expr": "2*asin(3*x - 5/2) + 6*x/sqrt(1 - (3*x - 5/2)**2)", "relation": "differentiate", "variable": "x"},
    {"text": "x = 1, u = 1/2.", "expr": "pi/3 + 4*sqrt(3)", "relation": "evaluate", "subs": {"x": "1"}}
   ],
   "calculator_status": "no_calculator",
   "skills": ["BC-SKL-03022", "BC-SKL-03025"]
  },
  {
   "id": "chk-3",
   "check_kind": "mcq",
   "format": "mcq",
   "bands": ["low"],
   "archetype_id": "BC-QA-03007",
   "parameter_draw": {"family": "arctan", "inner": "linear", "slope": 3, "at": -2, "coefficient": 1, "power": 2, "sign": -1},
   "stem": {"text": "h(x) = x^2 arctan(3x + 5). What is h'(-2)?", "command_verb": "identify"},
   "key": {"form": "symbolic", "expr": "pi + 6"},
   "steps": [
    {"text": "h(x).", "expr": "x**2*atan(3*x + 5)", "relation": "new"},
    {"text": "Product rule, arctan of u times u' = 3.", "expr": "2*x*atan(3*x + 5) + 3*x**2/(1 + (3*x + 5)**2)", "relation": "differentiate", "variable": "x"},
    {"text": "x = -2, u = -1.", "expr": "pi + 6", "relation": "evaluate", "subs": {"x": "-2"}}
   ],
   "options": [
    {"id": "A", "is_key": true, "expr": "pi + 6", "error_path": null},
    {"id": "B", "is_key": false, "expr": "6", "error_path": "BC-ERR-03006", "derivation": "product rule dropped: x^2 times 3/(1 + u^2) only"},
    {"id": "C", "is_key": false, "expr": "pi + 2", "error_path": "BC-ERR-03018", "derivation": "inner factor 3 dropped"},
    {"id": "D", "is_key": false, "expr": "pi - 6", "error_path": "BC-ERR-03017", "derivation": "sign misplaced in the recalled arctan formula"}
   ],
   "calculator_status": "no_calculator",
   "skills": ["BC-SKL-03025"]
  }
 ],
 "delivery": [
  {"block": "orientation", "mode": "text", "reason": "rule 5: the skills carry BC-REP-01 and BC-REP-09, neither figure-bearing", "sources": ["BC-SKL-03021"]},
  {"block": "ki-1", "mode": "text", "reason": "rule 5: three formulas and a chain rule factor, symbolic only", "sources": ["BC-SKL-03021", "BC-SKL-03022"]},
  {"block": "ex-1", "mode": "step_reveal", "reason": "rule 1", "sources": []},
  {"block": "err-BC-ERR-03006", "mode": "step_reveal", "reason": "rule 1", "sources": []},
  {"block": "err-BC-ERR-03018", "mode": "step_reveal", "reason": "rule 1", "sources": []},
  {"block": "err-BC-ERR-03017", "mode": "step_reveal", "reason": "rule 1", "sources": []}
 ],
 "refresher": ["ki-1", "err-BC-ERR-03006", "err-BC-ERR-03018", "err-BC-ERR-03017", "ex-1"],
 "read_minutes": {"full": 3.91, "brief": 2.8},
 "word_count": {"full": 586, "brief": 407},
 "research_lines": [
  {"file": "research/units/unit-03-differentiation-composite-implicit-inverse.md", "line": "the derivative of the inverse tangent of u is u prime divided by one plus u squared"}
 ],
 "inferred": [
  {"claim": "BC-QA-03007 has calculator_status either and the lesson places it in Section I Part A at 2.14 minutes.", "settles": "The exam section of BC-MCQ-PE2012-007 recorded on the archetype."}
 ],
 "sources": ["BC-CON-03007", "BC-SKL-03021", "BC-SKL-03022", "BC-SKL-03023", "BC-SKL-03024", "BC-SKL-03025", "BC-EK-FUN-3E2", "ced:78", "BC-QA-03007", "BC-QA-03010", "BC-QA-06018", "BC-MCQ-PE2012-007", "sg-25:2", "sg-25:4", "BC-ERR-03006", "BC-ERR-03018", "BC-ERR-03017", "BC-MIS-03012", "BC-MIS-03001", "BC-MIS-03010", "BC-PRQ-03004", "BC-PRQ-03006", "research/units/unit-03-differentiation-composite-implicit-inverse.md#3.4 Differentiating Inverse Trigonometric Functions", "research/question-analysis/question-archetypes.md#BC-QA-03007 Inverse trigonometric derivative with an inner function", "research/question-analysis/question-archetypes.md#BC-QA-06018 Antiderivative matched to an inverse trigonometric form, directly or after completing the square", "research/exam/exam-structure.md#Section and part layout"]
}
```
