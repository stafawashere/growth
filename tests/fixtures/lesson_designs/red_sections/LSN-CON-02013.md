---
title: LSN-CON-02013 The product rule
research_date: 2026-09-29
status: designed
purpose: Authoring spec for the concept lesson on BC-CON-02013, the product rule, built from authoring_bundle("BC-CON-02013") and the research files it cites, so an author fills plan 15's lesson record without making a teaching decision.
---

# LSN-CON-02013 The product rule

Concept BC-CON-02013 (skills BC-SKL-02036, BC-SKL-02037, BC-SKL-02038), topic 2.8 of Unit 2, loaded by BC-QA-02008 (primary) and BC-QA-02009. The reference lesson content/lessons/LSN-CON-02013.json is the hand-authored L0 exemplar; this design keeps its section structure and adds the recognition, time and delivery decisions.

## Orientation

Served text (50 words), from BC-CON-02013 `description_plain` and the topic's Assessment behaviour paragraph (research/units/unit-02-differentiation-definition-properties.md#2.8 The Product Rule): a response shows the derivative of a product as two terms added, the first factor times the derivative of the second plus the second factor times the derivative of the first, and questions ask for it symbolically or from values supplied at a point. No count, no frequency.

## Key ideas

One BC-EK maps to the three skills, BC-EK-FUN-3B1 (ced:67), so one core block, both bands.

- ki-1 (core, 47 words). The rule, its negation and the expansion alternative, paraphrased from the topic's Required mathematical knowledge paragraph: the derivative of \(fg\) is \(f'g+fg'\); it is not \(f'g'\), which expanding a simple product shows at once; a product of polynomials may be expanded first. Anchor quote (13 words) from ced:67. Notation line from the concept record: product rule.

## Recognition

Stem features that say "this concept":

- BC-QA-02008 (family rule-manipulation, MCQ shape, no calculator; research/question-analysis/question-archetypes.md#BC-QA-02008 Derivative of a product or a quotient by rule): `typical_wording` "Find the derivative of the given function"; `common_givens` a product or quotient of two differentiable expressions; `asked_to_produce` the derivative of the product or quotient. The signal is two variable factors multiplied, each differentiable on its own. FRQ appearances inside larger computations: BC-FRQ-2019-Q5-A and BC-FRQ-2014-Q3-C (`official_examples`).
- BC-QA-02009 (family derivative-from-table, MCQ or one FRQ part; research/question-analysis/question-archetypes.md#BC-QA-02009 Derivative of a product or quotient evaluated from supplied values): `typical_wording` a table of values of \(f\), \(g\) and their derivatives at selected inputs, the derivative of the indicated product at a named input; `common_givens` a table of values of two functions and their derivatives. The signal is four numbers at one input, two of them derivative values. FRQ appearance BC-FRQ-2021-Q4-B.

What says "not this concept": one factor is a constant (the constant multiple rule, BC-ERR-02023 names the over-application); the expression is a composite \(f(g(x))\) rather than a product (the chain rule, topic 3.1); a quotient with a variable denominator (the quotient rule, BC-CON-02014, taught beside this one).

## Method choice

Two strategy blocks, low and mid bands, the first only in mid.

- st-1, BC-QA-02008. Cue: the stem asks for the derivative of the product or quotient, from a product or quotient of two differentiable expressions (`asked_to_produce`, `common_givens`). Method, `expected_solution_path[0]`: identify the two factors and their derivatives. First written line: \(f=\), \(g=\), \(f'=\), \(g'=\) on one line. Rival, `wrong_approaches`: multiplying the derivatives of the two factors (BC-ERR-02020). Separating feature: a product gives two terms, each holding exactly one derivative.
- st-2, BC-QA-02009. Cue: the stem asks for the derivative value at the named input, from a table of values of two functions and their derivatives. Method, `expected_solution_path[0]`: record the four supplied values at the named input. First written line: the four values, each labelled a value or a derivative. Rival, `wrong_approaches`: placing a function value where the rule calls for a derivative value (BC-ERR-02024). Separating feature: each of the four numbers is labelled before it is used.

Both archetypes carry `asked_to_produce` and `common_givens`, so neither block is tagged inferred.

## Solution path

- ex-1, BC-QA-02008, both bands, no calculator. Draw: structure product, numerator quadratic, leading 1, constant 3, trig cos, giving \(h(x)=(x^2+3)\cos x\). The spec of BC-QA-02008 has no parameter that selects a product against a quotient [inferred]; the draw carries `structure` beside the spec's keys, and the gap is listed under Sources. Steps follow `expected_solution_path`: identify factors and derivatives (no value), substitute into the rule (valued, tagged BC-PT-99022), simplify as requested (valued). A fluent solver writes the rule line and the simplified line and holds the factor identification in the head.
- ex-2, BC-QA-02009, low band only, no calculator. Draw: \(f(1)=3\), \(f'(1)=-2\), \(g(1)=4\), \(g'(1)=5\), product form, row 1. Steps: record the four values (no value), write the rule with the names in place and substitute (valued, tagged BC-PT-99022), evaluate (valued). A fluent solver writes the substituted line and the value.

No productive-failure opener targets this concept (BC-CON-02002 is Unit 2's target), so no comparison callout.

## Scoring

Both archetypes list BC-PT-99022; the examples tag that point only, so one line per example, generated by `reader_checks(["BC-PT-99022"])` and copied into the machine record:

Product rule. Earned by: A differentiation that correctly applies the product rule to the given expression (sg-25:20, sg-22:16). Not earned by: A response that treats one factor as constant, which sg-22:16 states is eligible for the chain rule point but not this one.

Point losses the scoring research names for this shape: simplification is optional but an attempted simplification must be correct, so the rule line is the banked point and the collected line is where the answer point is lost (research/scoring/notation-requirements.md#Simplification, sg-23:16); an unrequired simplification that introduces an algebra error loses the answer point (research/scoring/common-point-losses.md#Answer points, BC-ERR-99022). The other point types the archetypes list (BC-PT-99004, BC-PT-99005, BC-PT-99069, BC-PT-99080) belong to quotient and accumulation draws and are not tagged here.

## Traps

Three active errors meet the concept's skills, in the bundle's order (all linked BC-MIS at severity high, so by id). Low band all three, mid band the first two.

- err-BC-ERR-02020 (BC-MIS-02011, BC-MIS-02012). Wrong step on ex-1's draw: \(f'g'=2x(-\sin x)\). Right step: \(2x\cos x-(x^2+3)\sin x\). Distinct. Possible reason, words from BC-MIS-02011: the derivative of a product is taken as the product of the derivatives.
- err-BC-ERR-02023 (BC-MIS-02012, BC-MIS-02011). Wrong step: the full quotient rule applied to \(\frac{x^2+3}{4}\). Right step: term by term, \(\frac{x}{2}\). Equivalent (the rule is not wrong, the algebra is unnecessary), which is the record's own scoring consequence.
- err-BC-ERR-02024 (BC-MIS-02011, BC-MIS-02014). Wrong step on ex-2's draw: \(f(1)\) in place of \(f'(1)\) gives \(3\cdot4+3\cdot5=27\). Right step: \(-2\cdot4+3\cdot5=7\). Distinct. Possible reason, words from BC-MIS-02011: supplied values are placed in the wrong positions.

## Representations

None. The topic's Representations paragraph names BC-REP-01, BC-REP-03 and BC-REP-02 and one conversion (supplied values to a derivative of their product), which ex-2 carries as a table; no figure-shaped content exists for a symbolic rule.

## Prerequisite bridge

None. The bundle lists no BC-PRQ parent of BC-SKL-02036, 02037 or 02038.

## Timing

Both archetypes are `no_calculator` and MCQ-shaped, so the part is Section I Part A, 29 questions in 62 minutes, 2.14 minutes per question (research/exam/exam-structure.md#Section and part layout; plan 15, Fluency). Inside that budget a fluent solver writes two lines on ex-1 (the rule line, the collected line) and two on ex-2 (the substituted line, the value), and skips the factor identification and the value labelling, which are read, not written. The rule line is written even under time pressure because it is the point that banks (Scoring above).

## Checks

- chk-1, completion of ex-1, both bands, short answer: the rule line is given, the student collects terms. Key \(2x\cos x-(x^2+3)\sin x\), which equals ex-1's answer.
- chk-2, isomorph on BC-QA-02008, both bands, short answer: \(h(x)=(x^2-2)\sin x\), find \(h'(x)\). Key \(2x\sin x+(x^2-2)\cos x\).
- chk-3, MCQ on BC-QA-02009, low band: \(f(2)=-1\), \(f'(2)=4\), \(g(2)=2\), \(g'(2)=-3\), \(h=fg\), find \(h'(2)\). Key 11. Distractors: 1 (BC-ERR-02024, \(f(2)\) for \(f'(2)\)), \(-12\) (BC-ERR-02020, the derivatives multiplied), 6 (BC-ERR-02024, \(g(2)\) for \(g'(2)\)).

No check draw equals a published BC-QA-02008 or BC-QA-02009 `parameter_draw` (content/items_gen_unit02, content/items_p1_agent).

## Delivery

- orientation: text. Rule 5, a symbolic rule whose skills' representations are BC-REP-01 (with BC-REP-03 on BC-SKL-02037 carried by ex-2, not here).
- ki-1: text. Rule 5; no figure-bearing BC-REP on the skills, and the idea is an algebraic identity, so a figure would add a representation with nothing to read from it.
- ex-1: step_reveal. Rule 1.
- ex-2: step_reveal with the four supplied values rendered as a table inside the problem (BC-REP-03 given). Rule 1; the table is the given, not a second representation.
- err-BC-ERR-02020, err-BC-ERR-02023, err-BC-ERR-02024: step_reveal, the wrong step beside the right step. Rule 1.

No motion, interactive or model mode applies: the concept has no parameter that varies and no process to watch, so every non-text mode would be decoration [inferred; settled by the modality A/B in the build plan].

## Band plan

- Low (full): orientation, ki-1, st-1, st-2, ex-1 with its scoring line, err-02020, err-02023, err-02024, chk-1, ex-2 with its scoring line, chk-2, chk-3, closing line. 626 words, 4.5 minutes (cap 900 and 6).
- Mid (brief): orientation, ki-1, st-1, ex-1 with its scoring line, err-02020, err-02023, chk-1, chk-2, closing line. 394 words, 2.7 minutes (cap 450 and 3).
- Refresher: ki-1, err-BC-ERR-02020, err-BC-ERR-02023, err-BC-ERR-02024, ex-1.

## Sources

- BC-CON-02013; BC-SKL-02036, BC-SKL-02037, BC-SKL-02038; BC-EK-FUN-3B1; ced:67, ced:68
- BC-QA-02008, BC-QA-02009; BC-FRQ-2019-Q5-A, BC-FRQ-2014-Q3-C, BC-FRQ-2021-Q4-B
- BC-PT-99022; sg-25:20, sg-22:16, sg-23:16
- BC-ERR-02020, BC-ERR-02023, BC-ERR-02024; BC-MIS-02011, BC-MIS-02012, BC-MIS-02014; BC-ERR-99022
- research/units/unit-02-differentiation-definition-properties.md#2.8 The Product Rule
- research/question-analysis/question-archetypes.md#BC-QA-02008 Derivative of a product or a quotient by rule
- research/question-analysis/question-archetypes.md#BC-QA-02009 Derivative of a product or quotient evaluated from supplied values
- research/scoring/notation-requirements.md#Simplification
- research/scoring/common-point-losses.md#Answer points
- research/exam/exam-structure.md#Section and part layout
- [inferred] The `parameter_spec` of BC-QA-02008 carries no product-versus-quotient parameter, so a product draw adds a `structure` key. Settled by a library staging pass adding the parameter, or by the template under app/generation/templates confirming that it only produces quotients.
- [inferred] No non-text delivery mode. Settled by the modality A/B.

## Machine record

```json
{
 "id": "LSN-CON-02013",
 "kind": "concept",
 "target_id": "BC-CON-02013",
 "unit": "02",
 "skills": ["BC-SKL-02036", "BC-SKL-02037", "BC-SKL-02038"],
 "orientation": {
  "text": "A response shows the derivative of a product as two terms added: the first factor times the derivative of the second, plus the second factor times the derivative of the first. Questions ask for it symbolically, or from values of the two functions and their derivatives supplied at one input.",
  "sources": ["BC-CON-02013", "research/units/unit-02-differentiation-definition-properties.md#2.8 The Product Rule"]
 },
 "key_ideas": [
  {
   "id": "ki-1",
   "ek_id": "BC-EK-FUN-3B1",
   "depth": "core",
   "text": "For a product \\(fg\\) the derivative is \\(f'g+fg'\\) (BC-EK-FUN-3B1, ced:67). It is not \\(f'g'\\), which expanding a simple product and differentiating term by term shows at once. A product of polynomials can also be expanded first and differentiated term by term, which is sometimes the shorter route.",
   "notation": "product rule",
   "quote": {"text": "Derivatives of products of differentiable functions can be found using the product rule.", "source": "ced:67"},
   "sources": ["BC-EK-FUN-3B1", "ced:67", "research/units/unit-02-differentiation-definition-properties.md#2.8 The Product Rule"]
  }
 ],
 "strategy": [
  {
   "id": "st-1",
   "archetype_id": "BC-QA-02008",
   "cue": "The stem asks for the derivative of the product or quotient, from a product or quotient of two differentiable expressions.",
   "method": "First written line: name the two factors and their derivatives, \\(f\\), \\(g\\), \\(f'\\), \\(g'\\).",
   "rival": "The rival is multiplying the derivatives of the two factors (BC-ERR-02020).",
   "separating_feature": "A product gives two terms, each holding exactly one derivative.",
   "sources": ["BC-QA-02008"],
   "evidence_tag": "verified"
  },
  {
   "id": "st-2",
   "archetype_id": "BC-QA-02009",
   "cue": "The stem asks for the derivative value at the named input, from a table of values of two functions and their derivatives.",
   "method": "First written line: record the four supplied values at the named input, each labelled a value or a derivative.",
   "rival": "The rival is placing a function value where the rule calls for a derivative value (BC-ERR-02024).",
   "separating_feature": "Each of the four numbers is labelled before it is used.",
   "sources": ["BC-QA-02009"],
   "evidence_tag": "verified"
  }
 ],
 "worked_examples": [
  {
   "id": "ex-1",
   "archetype_id": "BC-QA-02008",
   "bands": ["low", "mid"],
   "parameter_draw": {"structure": "product", "numerator": "quadratic", "leading": 1, "constant": 3, "trig": "cos"},
   "problem": {"text": "Let \\(h(x)=(x^2+3)\\cos x\\). Find \\(h'(x)\\).", "command_verb": "find"},
   "calculator_status": "no_calculator",
   "steps": [
    {"cue": "The stem is a product of \\(f=x^2+3\\) and \\(g=\\cos x\\).", "why": "Each factor needs its own derivative: \\(f'=2x\\) and \\(g'=-\\sin x\\)."},
    {"cue": "Two factors are multiplied, so the rule is \\(f'g+fg'\\).", "why": "Both terms are needed. Each keeps one factor and differentiates the other.", "expr": "2*x*cos(x) + (x**2+3)*(-sin(x))", "relation": "new", "point_type_id": "BC-PT-99022"},
    {"cue": "The stem asks for \\(h'(x)\\), so clear the double sign.", "why": "The answer is the rule line tidied; no further simplification is required.", "expr": "2*x*cos(x) - (x**2+3)*sin(x)", "relation": "equivalent"}
   ],
   "answer": {"form": "symbolic", "expr": "2*x*cos(x) - (x**2+3)*sin(x)"}
  },
  {
   "id": "ex-2",
   "archetype_id": "BC-QA-02009",
   "bands": ["low"],
   "parameter_draw": {"f_values": 3, "f_slopes": -2, "g_values": 4, "g_slopes": 5, "row": 1, "start": 0, "form": "product"},
   "problem": {"text": "The table gives \\(f(1)=3\\), \\(f'(1)=-2\\), \\(g(1)=4\\), \\(g'(1)=5\\). Let \\(h(x)=f(x)g(x)\\). Find \\(h'(1)\\).", "command_verb": "find"},
   "calculator_status": "no_calculator",
   "steps": [
    {"cue": "Four values at the input 1, two of them derivative values.", "why": "Label each before use: \\(f(1)=3\\), \\(f'(1)=-2\\), \\(g(1)=4\\), \\(g'(1)=5\\)."},
    {"cue": "\\(h\\) is a product, so \\(h'(1)=f'(1)g(1)+f(1)g'(1)\\).", "why": "Each term holds one derivative value and one function value.", "expr": "(-2)*4 + 3*5", "relation": "new", "point_type_id": "BC-PT-99022"},
    {"cue": "The stem asks for a value.", "why": "Arithmetic on the substituted line.", "expr": "7", "relation": "equivalent"}
   ],
   "answer": {"form": "numeric", "expr": "7"}
  }
 ],
 "what_a_reader_scores": [
  {"example_id": "ex-1", "point_type_ids": ["BC-PT-99022"], "lines": [{"point_type_id": "BC-PT-99022", "text": "Product rule. Earned by: A differentiation that correctly applies the product rule to the given expression (sg-25:20, sg-22:16). Not earned by: A response that treats one factor as constant, which sg-22:16 states is eligible for the chain rule point but not this one."}]},
  {"example_id": "ex-2", "point_type_ids": ["BC-PT-99022"], "lines": [{"point_type_id": "BC-PT-99022", "text": "Product rule. Earned by: A differentiation that correctly applies the product rule to the given expression (sg-25:20, sg-22:16). Not earned by: A response that treats one factor as constant, which sg-22:16 states is eligible for the chain rule point but not this one."}]}
 ],
 "common_errors": [
  {
   "error_id": "BC-ERR-02020",
   "observed_behavior": "The response multiplies the derivatives of the two factors together.",
   "scoring_consequence": "The rule point and the result point are both lost.",
   "wrong_step": {"text": "The derivatives of the two factors are multiplied: \\(f'g'=2x(-\\sin x)\\).", "expr": "2*x*(-sin(x))"},
   "right_step": {"text": "The rule adds two terms: \\(f'g+fg'=2x\\cos x-(x^2+3)\\sin x\\).", "expr": "2*x*cos(x) - (x**2+3)*sin(x)"},
   "relation": "distinct",
   "possible_reason": {"misconception_id": "BC-MIS-02011", "text": "the derivative of a product is taken as the product of the derivatives"},
   "sources": ["BC-ERR-02020", "BC-MIS-02011"]
  },
  {
   "error_id": "BC-ERR-02023",
   "observed_behavior": "The response applies the full quotient rule to an expression whose denominator carries no variable.",
   "scoring_consequence": "No point is necessarily lost but the additional algebra invites a further error.",
   "wrong_step": {"text": "The full quotient rule is applied to \\(\\frac{x^2+3}{4}\\).", "expr": "((2*x)*4 - (x**2+3)*0)/4**2"},
   "right_step": {"text": "The denominator is constant, so differentiate term by term: \\(\\frac{x}{2}\\).", "expr": "x/2"},
   "relation": "equivalent",
   "possible_reason": null,
   "sources": ["BC-ERR-02023"]
  },
  {
   "error_id": "BC-ERR-02024",
   "observed_behavior": "The response substitutes the value of a function into a position in the product or quotient rule that calls for the value of its derivative.",
   "scoring_consequence": "The value point is lost.",
   "wrong_step": {"text": "With \\(f(1)=3\\), \\(f'(1)=-2\\), \\(g(1)=4\\), \\(g'(1)=5\\), using \\(f(1)\\) in place of \\(f'(1)\\) gives \\(3\\cdot4+3\\cdot5=27\\).", "expr": "3*4 + 3*5"},
   "right_step": {"text": "The rule gives \\(f'(1)g(1)+f(1)g'(1)=-8+15=7\\).", "expr": "(-2)*4 + 3*5"},
   "relation": "distinct",
   "possible_reason": {"misconception_id": "BC-MIS-02011", "text": "supplied values are placed in the wrong positions"},
   "sources": ["BC-ERR-02024", "BC-MIS-02011"]
  }
 ],
 "representations": null,
 "prerequisite_bridges": [],
 "time": {"exam_part": "I-A", "budget_minutes": 2.14, "source": "research/exam/exam-structure.md#Section and part layout", "written_steps": {"ex-1": [2, 3], "ex-2": [2, 3]}, "skipped_steps": {"ex-1": [1], "ex-2": [1]}},
 "checks": [
  {
   "id": "chk-1",
   "check_kind": "completion",
   "format": "short_answer",
   "bands": ["low", "mid"],
   "archetype_id": "BC-QA-02008",
   "parameter_draw": {"structure": "product", "numerator": "quadratic", "leading": 1, "constant": 3, "trig": "cos"},
   "completes": "ex-1",
   "stem": {"text": "The product rule gives \\(h'(x)=(2x)(\\cos x)+(x^2+3)(-\\sin x)\\). Write \\(h'(x)\\) with the double sign cleared.", "command_verb": "write"},
   "key": {"form": "symbolic", "expr": "2*x*cos(x) - (x**2+3)*sin(x)"},
   "steps": [
    {"text": "The rule gives the two terms \\((2x)(\\cos x)\\) and \\((x^2+3)(-\\sin x)\\).", "expr": "2*x*cos(x) + (x**2+3)*(-sin(x))", "relation": "new", "point_type_id": "BC-PT-99022"},
    {"text": "Clearing the double sign gives \\(2x\\cos x-(x^2+3)\\sin x\\).", "expr": "2*x*cos(x) - (x**2+3)*sin(x)", "relation": "equivalent"}
   ],
   "calculator_status": "no_calculator",
   "skills": ["BC-SKL-02036"]
  },
  {
   "id": "chk-2",
   "check_kind": "isomorph",
   "format": "short_answer",
   "bands": ["low", "mid"],
   "archetype_id": "BC-QA-02008",
   "parameter_draw": {"structure": "product", "numerator": "quadratic", "leading": 1, "constant": -2, "trig": "sin"},
   "stem": {"text": "Let \\(h(x)=(x^2-2)\\sin x\\). Find \\(h'(x)\\).", "command_verb": "find"},
   "key": {"form": "symbolic", "expr": "2*x*sin(x) + (x**2-2)*cos(x)"},
   "steps": [
    {"text": "The rule gives \\((2x)(\\sin x)+(x^2-2)(\\cos x)\\).", "expr": "2*x*sin(x) + (x**2-2)*cos(x)", "relation": "new", "point_type_id": "BC-PT-99022"}
   ],
   "calculator_status": "no_calculator",
   "skills": ["BC-SKL-02036"]
  },
  {
   "id": "chk-3",
   "check_kind": "mcq",
   "format": "mcq",
   "bands": ["low"],
   "archetype_id": "BC-QA-02009",
   "parameter_draw": {"f_values": -1, "f_slopes": 4, "g_values": 2, "g_slopes": -3, "row": 2, "start": 0, "form": "product"},
   "stem": {"text": "Suppose \\(f(2)=-1\\), \\(f'(2)=4\\), \\(g(2)=2\\), \\(g'(2)=-3\\) and \\(h(x)=f(x)g(x)\\). Find \\(h'(2)\\).", "command_verb": "find"},
   "key": {"form": "numeric", "expr": "11"},
   "steps": [
    {"text": "The rule gives \\(h'(2)=f'(2)g(2)+f(2)g'(2)=4(2)+(-1)(-3)\\).", "expr": "4*2 + (-1)*(-3)", "relation": "new", "point_type_id": "BC-PT-99022"},
    {"text": "That is 11.", "expr": "11", "relation": "equivalent"}
   ],
   "options": [
    {"id": "A", "is_key": false, "expr": "1", "error_path": "BC-ERR-02024", "derivation": "f(2) used in place of f'(2): (-1)(2) + (-1)(-3)"},
    {"id": "B", "is_key": false, "expr": "-12", "error_path": "BC-ERR-02020", "derivation": "the two derivatives multiplied: 4(-3)"},
    {"id": "C", "is_key": true, "expr": "11", "error_path": null},
    {"id": "D", "is_key": false, "expr": "6", "error_path": "BC-ERR-02024", "derivation": "g(2) used in place of g'(2): 4(2) + (-1)(2)"}
   ],
   "calculator_status": "no_calculator",
   "skills": ["BC-SKL-02037"]
  }
 ],
 "delivery": [
  {"block": "orientation", "mode": "text", "reason": "rule 5: a symbolic rule, BC-REP-01 givens on BC-SKL-02036", "sources": ["BC-SKL-02036"]},
  {"block": "ki-1", "mode": "text", "reason": "rule 5: an algebraic identity with no figure-bearing BC-REP on the skills", "sources": ["BC-SKL-02036"]},
  {"block": "ex-1", "mode": "step_reveal", "reason": "rule 1", "sources": []},
  {"block": "ex-2", "mode": "step_reveal", "reason": "rule 1; the four supplied values render as a table inside the problem (BC-REP-03 given)", "sources": ["BC-SKL-02037"]},
  {"block": "err-BC-ERR-02020", "mode": "step_reveal", "reason": "rule 1", "sources": []},
  {"block": "err-BC-ERR-02023", "mode": "step_reveal", "reason": "rule 1", "sources": []},
  {"block": "err-BC-ERR-02024", "mode": "step_reveal", "reason": "rule 1", "sources": []}
 ],
 "refresher": ["ki-1", "err-BC-ERR-02020", "err-BC-ERR-02023", "err-BC-ERR-02024", "ex-1"],
 "read_minutes": {"full": 4.5, "brief": 2.7},
 "word_count": {"full": 626, "brief": 394},
 "research_lines": [
  {"file": "research/scoring/notation-requirements.md", "line": "simplification is optional, but attempted simplification must be correct"},
  {"file": "research/units/unit-02-differentiation-definition-properties.md", "line": "MCQ forms ask for the derivative of a product, either symbolically or from supplied values at a point."}
 ],
 "inferred": [
  {"claim": "The parameter_spec of BC-QA-02008 carries no product-versus-quotient parameter, so the product draw adds a structure key.", "settles": "A library staging pass adding the parameter, or the template confirming it only produces quotients."},
  {"claim": "No non-text delivery mode serves this concept better than text and step reveal.", "settles": "The modality A/B in the build plan: skip rate and time to first credited success by mode."}
 ],
 "sources": ["BC-CON-02013", "BC-SKL-02036", "BC-SKL-02037", "BC-SKL-02038", "BC-EK-FUN-3B1", "ced:67", "ced:68", "BC-QA-02008", "BC-QA-02009", "BC-PT-99022", "sg-25:20", "sg-22:16", "sg-23:16", "BC-ERR-02020", "BC-ERR-02023", "BC-ERR-02024", "BC-MIS-02011", "BC-MIS-02012", "BC-MIS-02014", "BC-ERR-99022", "BC-FRQ-2019-Q5-A", "BC-FRQ-2014-Q3-C", "BC-FRQ-2021-Q4-B", "research/units/unit-02-differentiation-definition-properties.md#2.8 The Product Rule", "research/scoring/notation-requirements.md#Simplification", "research/scoring/common-point-losses.md#Answer points", "research/exam/exam-structure.md#Section and part layout"]
}
```
