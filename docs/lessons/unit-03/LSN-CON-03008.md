---
title: LSN-CON-03008 Classification of an expression before differentiating
research_date: 2026-09-29
status: designed
purpose: Authoring spec for the concept lesson on BC-CON-03008, classifying an expression by its outermost operation to choose and order the differentiation rules, built from authoring_bundle("BC-CON-03008") and the research files it cites, so an author fills plan 15's lesson record without making a teaching decision.
---

# LSN-CON-03008 Classification of an expression before differentiating

Concept BC-CON-03008 (skills BC-SKL-03026 to BC-SKL-03029), topic 3.5 of Unit 3, loaded by one archetype, BC-QA-03009 (family procedure-selection). Its parent concept is BC-CON-03002 through BC-SKL-03004 (docs/lessons/unit-03/README.md, section 1).

## Orientation

Served text, from BC-CON-03008 `description_plain` and the topic's Assessment behaviour paragraph (research/units/unit-03-differentiation-composite-implicit-inverse.md#3.5 Selecting Procedures for Calculating Derivatives): a response names the operation applied last, opens with the rule for it, and works inward. No count, no frequency.

## Key ideas

No skill of BC-CON-03008 lists `essential_knowledge` (BC-SKL-03026 to BC-SKL-03029 carry an empty list), and ced:79 prints no essential knowledge statement for topic 3.5, so the one core block carries `ek_id` null and is tagged [inferred], following LSN-CON-01009.

- ki-1 (core). Paraphrase of the Required mathematical knowledge paragraphs (Classification, Order of rules, Rewriting). Anchor quote from ced:79, 17 words, the topic's own statement of focus. Notation line from the concept record.

## Recognition

BC-QA-03009 (research/question-analysis/question-archetypes.md#BC-QA-03009 Selecting the differentiation procedure for a given expression): `typical_wording` "find the derivative of the given expression", "identify the rule needed to differentiate the given expression"; `common_givens` an expression built from products, quotients, compositions or exponentials; `asked_to_produce` the derivative or the rule. The signal: an expression whose surface suggests one family and whose last operation is another, such as a polynomial times an exponential with a polynomial exponent. Shape: one no-calculator MCQ, or the opening decision inside a differentiation part (cr-22:21); no `official_examples`.

What says "not this concept": a single named function of x with nothing nested, where the rule is the only one available.

## Method choice

One strategy block, both bands.

- st-1, BC-QA-03009. Method, `expected_solution_path[0]`: classify the outermost operation. Rival, `wrong_approaches`: the power rule applied to an exponential term (BC-ERR-99036), and a composite factor differentiated without the enclosing product rule (BC-ERR-03006). Separating feature: where the variable sits; in the exponent means the exponential rule with the chain rule. The archetype carries both fields, so verified.

## Solution path

- ex-1, BC-QA-03009, both bands, no calculator. Draw from `parameter_spec`: scale 2, power 2, rate 3, offset -1, inner_degree 1, at -1; derived exponent_at = -4, inner_rate = 3, key_factor = 1. The constraint list holds: 1, 3 and -1 are distinct. h(x) = 2x^2 e^(3x - 1). No published BC-QA-03009 item carries this draw (the published draws use a different parameter set).
- Steps follow `expected_solution_path`: the expression classified (new); product rule outside, chain rule inside (differentiate); the safe rewrite by factoring (equivalent); the value (evaluate). A fluent solver writes steps 2 and 4; the classification is held in the head and the rewrite is optional.

## Scoring

BC-QA-03009 lists no `point_types`, so no what_a_reader_scores entry and no point tag. For the author: the Chief Reader reports record rule choice driven by the shape of an expression as a recurring loss (cr-22:21), and unnecessary simplification that changes the value as another (cr-24:19; research/scoring/notation-requirements.md#Simplification).

## Traps

Four active errors meet the skills, in the bundle's order: BC-ERR-03002, BC-ERR-03006, BC-ERR-03020, BC-ERR-99036. Low band all four; mid band the first two. All on ex-1's draw except the first, which needs three layers.

- err-BC-ERR-03002: on e^((3x - 1)^2), three layers, the innermost derivative 3 omitted. Possible reason, words from BC-MIS-03001.
- err-BC-ERR-03006: the composite factor alone differentiated. Possible reason, words from BC-MIS-03012.
- err-BC-ERR-03020: a factoring slip changes the value. No possible reason line: neither linked description names simplification.
- err-BC-ERR-99036: the power rule applied to e^(3x - 1). Possible reason, words from BC-MIS-02010.

## Representations

None. The topic's Representations paragraph names BC-REP-01 and BC-REP-04 only.

## Prerequisite bridge

- BC-PRQ-03001, from its `description_plain` and `failure_signature`.
- BC-PRQ-03006, from its `description_plain` and `failure_signature`.

## Time

BC-QA-03009 is `no_calculator`, a single MCQ: Section I Part A, 2.14 minutes per question (research/exam/exam-structure.md#Section and part layout). The minutes go on the derivative line; the classification is not written [inferred, docs/lessons/unit-03/README.md, section 5].

## Checks

- chk-1, completion of ex-1, both bands: h'(x) = 2x(2 + 3x)e^(3x - 1) is given, the student evaluates at x = -1. Key 2e^(-4).
- chk-2, isomorph, both bands. Draw: scale 3, power 1, rate -2, offset 2, inner_degree 1, at 2; h(x) = 3x e^(-2x + 2). Key h'(2) = -9e^(-2).
- chk-3, MCQ, low band. Draw: scale 1, power 1, rate 2, offset 1, inner_degree 2, at 1; h(x) = x e^(2x^2 + 1). Key 5e^3. Distractors: 4e^3 (BC-ERR-03006), 3e^3 (BC-ERR-03020), e^3 + 3e^2 (BC-ERR-99036).

## Delivery

- orientation, ki-1: text. Rule 5: BC-REP-01 and BC-REP-04 only (docs/lessons/unit-03/README.md, section 6).
- ex-1: step_reveal. Rule 1.
- err-BC-ERR-03002, err-BC-ERR-03006, err-BC-ERR-03020, err-BC-ERR-99036: step_reveal. Rule 1.

## Band plan

- Low (full): orientation, ki-1, st-1, ex-1, the four error blocks, chk-1 to chk-3, the two bridges. 547 words, 3.65 minutes (cap 900 and 6).
- Mid (brief): orientation, ki-1, st-1, ex-1, err-BC-ERR-03002, err-BC-ERR-03006, chk-1, chk-2, the two bridges. 423 words, 2.82 minutes (cap 450 and 3).
- Refresher: ki-1, err-BC-ERR-03002, err-BC-ERR-03006, err-BC-ERR-03020, err-BC-ERR-99036, ex-1.

## Sources

- BC-CON-03008; BC-SKL-03026, BC-SKL-03027, BC-SKL-03028, BC-SKL-03029; ced:79, ced:72
- BC-QA-03009; cr-22:21, cr-24:19
- BC-ERR-03002, BC-ERR-03006, BC-ERR-03020, BC-ERR-99036; BC-MIS-03001, BC-MIS-03012, BC-MIS-02010
- BC-PRQ-03001, BC-PRQ-03006
- research/units/unit-03-differentiation-composite-implicit-inverse.md#3.5 Selecting Procedures for Calculating Derivatives
- research/question-analysis/question-archetypes.md#BC-QA-03009 Selecting the differentiation procedure for a given expression
- research/scoring/notation-requirements.md#Simplification
- research/exam/exam-structure.md#Section and part layout
- [inferred] ki-1 has no BC-EK. Settled by a library pass mapping BC-SKL-03026 to 03029 to a BC-EK.
- [inferred] The classification is held in the head on the MCQ. Settled by timing data on BC-QA-03009 items.

## Machine record

```json
{
 "id": "LSN-CON-03008",
 "kind": "concept",
 "target_id": "BC-CON-03008",
 "unit": "03",
 "skills": ["BC-SKL-03026", "BC-SKL-03027", "BC-SKL-03028", "BC-SKL-03029"],
 "orientation": {
  "text": "A response names the operation applied last, opens with the rule for that operation, and works inward, so each rule acts on the piece it belongs to.",
  "sources": ["BC-CON-03008", "research/units/unit-03-differentiation-composite-implicit-inverse.md#3.5 Selecting Procedures for Calculating Derivatives"]
 },
 "key_ideas": [
  {
   "id": "ki-1",
   "ek_id": null,
   "depth": "core",
   "text": "An expression is classified by the operation applied last: a sum, a constant multiple, a product, a quotient, a composition or a basic function. That class picks the opening rule, and nested pieces are handled from the outside in. A rewrite that leaves the function unchanged may replace a harder rule, once checked [inferred: no BC-EK is mapped].",
   "notation": "outermost operation; order of rule application",
   "quote": {"text": "This topic is intended to focus on the skill of selecting an appropriate procedure for calculating derivatives.", "source": "ced:79"},
   "sources": ["ced:79", "ced:72", "research/units/unit-03-differentiation-composite-implicit-inverse.md#3.5 Selecting Procedures for Calculating Derivatives"]
  }
 ],
 "strategy": [
  {
   "id": "st-1",
   "archetype_id": "BC-QA-03009",
   "cue": "An expression mixing products, compositions or exponentials, with its derivative or rule asked.",
   "method": "First move: name the last operation, then apply rules from the outside in.",
   "rival": "Rival: the power rule on an exponential (BC-ERR-99036), or the product rule dropped (BC-ERR-03006).",
   "separating_feature": "Where x sits: in an exponent means the exponential rule; multiplied factors mean the product rule first.",
   "sources": ["BC-QA-03009"],
   "evidence_tag": "verified"
  }
 ],
 "worked_examples": [
  {
   "id": "ex-1",
   "archetype_id": "BC-QA-03009",
   "bands": ["low", "mid"],
   "parameter_draw": {"scale": 2, "power": 2, "rate": 3, "offset": -1, "inner_degree": 1, "at": -1},
   "problem": {"text": "h(x) = 2x^2 e^(3x - 1). Find h'(-1).", "command_verb": "find"},
   "calculator_status": "no_calculator",
   "steps": [
    {"cue": "Last operation: 2x^2 times e^(3x - 1).", "why": "A product; one factor is a composite with x in the exponent.", "expr": "2*x**2*exp(3*x - 1)", "relation": "new"},
    {"cue": "Product rule outside, chain rule on the exponential.", "why": "e^u has derivative e^u times u', with u' = 3.", "expr": "4*x*exp(3*x - 1) + 6*x**2*exp(3*x - 1)", "relation": "differentiate", "variable": "x"},
    {"cue": "Both terms share 2x e^(3x - 1).", "why": "A safe rewrite; it shortens the evaluation.", "expr": "2*x*(2 + 3*x)*exp(3*x - 1)", "relation": "equivalent"},
    {"cue": "The stem asks for x = -1.", "why": "2(-1)(-1) = 2 and e^(-4).", "expr": "2*exp(-4)", "relation": "evaluate", "subs": {"x": "-1"}}
   ],
   "answer": {"form": "symbolic", "expr": "2*exp(-4)"}
  }
 ],
 "what_a_reader_scores": [],
 "common_errors": [
  {
   "error_id": "BC-ERR-03002",
   "observed_behavior": "A composition of three functions is differentiated through the first two layers and the innermost derivative is omitted.",
   "scoring_consequence": "The derivative is wrong; no credit is available for a partially applied rule in a single answer item.",
   "wrong_step": {"text": "e^((3x - 1)^2) has three layers; the outer two give 2(3x - 1)e^((3x - 1)^2) and the innermost factor 3 is omitted.", "expr": "2*(3*x - 1)*exp((3*x - 1)**2)"},
   "right_step": {"text": "Times the innermost derivative 3.", "expr": "6*(3*x - 1)*exp((3*x - 1)**2)"},
   "relation": "distinct",
   "possible_reason": {"misconception_id": "BC-MIS-03001", "text": "whatever sits inside is copied across unchanged"},
   "sources": ["BC-ERR-03002", "BC-MIS-03001"]
  },
  {
   "error_id": "BC-ERR-03006",
   "observed_behavior": "The composite factor is differentiated correctly but the enclosing product or quotient rule is not applied.",
   "scoring_consequence": "The derivative is wrong; in the 2025 implicit differentiation task the product rule carries its own scoring point (sg-25:20).",
   "wrong_step": {"text": "2x^2 times the exponential's derivative only.", "expr": "6*x**2*exp(3*x - 1)"},
   "right_step": {"text": "Both product rule terms.", "expr": "4*x*exp(3*x - 1) + 6*x**2*exp(3*x - 1)"},
   "relation": "distinct",
   "possible_reason": {"misconception_id": "BC-MIS-03012", "text": "selects a rule by the visual pattern of the expression rather than by the operation applied last"},
   "sources": ["BC-ERR-03006", "BC-MIS-03012"]
  },
  {
   "error_id": "BC-ERR-03020",
   "observed_behavior": "A correct derivative is simplified further and the simplification changes the value.",
   "scoring_consequence": "The Chief Reader reports record unnecessary simplification as a recurring source of lost points (cr-24:19, crabbc-25:26).",
   "wrong_step": {"text": "2x factored out, 6x left.", "expr": "2*x*(2 + 6*x)*exp(3*x - 1)"},
   "right_step": {"text": "2x factored out, 3x left.", "expr": "2*x*(2 + 3*x)*exp(3*x - 1)"},
   "relation": "distinct",
   "possible_reason": null,
   "sources": ["BC-ERR-03020"]
  },
  {
   "error_id": "BC-ERR-99036",
   "observed_behavior": "Responses apply the power rule to an exponential term, decrementing the exponent as though the variable were the base, rather than selecting the rule that matches the type of function.",
   "scoring_consequence": "The derivative point is not earned, and every later part that uses the derivative inherits the error.",
   "wrong_step": {"text": "e^(3x - 1) treated as a power.", "expr": "4*x*exp(3*x - 1) + 2*x**2*(3*x - 1)*exp(3*x - 2)"},
   "right_step": {"text": "The exponential rule with the chain rule.", "expr": "4*x*exp(3*x - 1) + 6*x**2*exp(3*x - 1)"},
   "relation": "distinct",
   "possible_reason": {"misconception_id": "BC-MIS-02010", "text": "applies the exponent move to transcendental functions, so the natural exponential is treated as a power"},
   "sources": ["BC-ERR-99036", "BC-MIS-02010"]
  }
 ],
 "representations": null,
 "prerequisite_bridges": [
  {"prq_id": "BC-PRQ-03001", "text": "Name the operation applied last and the one applied first; otherwise the outer shell is differentiated and the work stops, or the inner piece alone is reported."},
  {"prq_id": "BC-PRQ-03006", "text": "A wrong simplification after a correct derivative changes the value reported."}
 ],
 "time": {"exam_part": "I-A", "budget_minutes": 2.14, "source": "research/exam/exam-structure.md#Section and part layout", "written_steps": {"ex-1": [2, 4]}, "skipped_steps": {"ex-1": [1, 3]}},
 "checks": [
  {
   "id": "chk-1",
   "check_kind": "completion",
   "format": "short_answer",
   "bands": ["low", "mid"],
   "archetype_id": "BC-QA-03009",
   "parameter_draw": {"scale": 2, "power": 2, "rate": 3, "offset": -1, "inner_degree": 1, "at": -1},
   "completes": "ex-1",
   "stem": {"text": "h'(x) = 2x(2 + 3x)e^(3x - 1). Find h'(-1).", "command_verb": "find"},
   "key": {"form": "symbolic", "expr": "2*exp(-4)"},
   "steps": [
    {"text": "The derivative.", "expr": "2*x*(2 + 3*x)*exp(3*x - 1)", "relation": "new"},
    {"text": "x = -1.", "expr": "2*exp(-4)", "relation": "evaluate", "subs": {"x": "-1"}}
   ],
   "calculator_status": "no_calculator",
   "skills": ["BC-SKL-03028"]
  },
  {
   "id": "chk-2",
   "check_kind": "isomorph",
   "format": "short_answer",
   "bands": ["low", "mid"],
   "archetype_id": "BC-QA-03009",
   "parameter_draw": {"scale": 3, "power": 1, "rate": -2, "offset": 2, "inner_degree": 1, "at": 2},
   "stem": {"text": "h(x) = 3x e^(-2x + 2). Find h'(2).", "command_verb": "find"},
   "key": {"form": "symbolic", "expr": "-9*exp(-2)"},
   "steps": [
    {"text": "A product.", "expr": "3*x*exp(-2*x + 2)", "relation": "new"},
    {"text": "Product rule, chain rule inside.", "expr": "3*exp(-2*x + 2) - 6*x*exp(-2*x + 2)", "relation": "differentiate", "variable": "x"},
    {"text": "x = 2.", "expr": "-9*exp(-2)", "relation": "evaluate", "subs": {"x": "2"}}
   ],
   "calculator_status": "no_calculator",
   "skills": ["BC-SKL-03026", "BC-SKL-03028"]
  },
  {
   "id": "chk-3",
   "check_kind": "mcq",
   "format": "mcq",
   "bands": ["low"],
   "archetype_id": "BC-QA-03009",
   "parameter_draw": {"scale": 1, "power": 1, "rate": 2, "offset": 1, "inner_degree": 2, "at": 1},
   "stem": {"text": "h(x) = x e^(2x^2 + 1). What is h'(1)?", "command_verb": "identify"},
   "key": {"form": "symbolic", "expr": "5*exp(3)"},
   "steps": [
    {"text": "A product.", "expr": "x*exp(2*x**2 + 1)", "relation": "new"},
    {"text": "Product rule, chain rule inside.", "expr": "exp(2*x**2 + 1) + 4*x**2*exp(2*x**2 + 1)", "relation": "differentiate", "variable": "x"},
    {"text": "x = 1.", "expr": "5*exp(3)", "relation": "evaluate", "subs": {"x": "1"}}
   ],
   "options": [
    {"id": "A", "is_key": false, "expr": "4*exp(3)", "error_path": "BC-ERR-03006", "derivation": "x times the exponential's derivative only"},
    {"id": "B", "is_key": false, "expr": "3*exp(3)", "error_path": "BC-ERR-03020", "derivation": "e^u + 4x^2 e^u factored with a sign slip as (4x^2 - 1)e^u"},
    {"id": "C", "is_key": true, "expr": "5*exp(3)", "error_path": null},
    {"id": "D", "is_key": false, "expr": "exp(3) + 3*exp(2)", "error_path": "BC-ERR-99036", "derivation": "power rule on the exponential: (2x^2 + 1)e^(2x^2)"}
   ],
   "calculator_status": "no_calculator",
   "skills": ["BC-SKL-03026", "BC-SKL-03027", "BC-SKL-03029"]
  }
 ],
 "delivery": [
  {"block": "orientation", "mode": "text", "reason": "rule 5: BC-REP-01 and BC-REP-04 only", "sources": ["BC-SKL-03026"]},
  {"block": "ki-1", "mode": "text", "reason": "rule 5: a classification rule stated in words", "sources": ["BC-SKL-03026", "BC-SKL-03027"]},
  {"block": "ex-1", "mode": "step_reveal", "reason": "rule 1", "sources": []},
  {"block": "err-BC-ERR-03002", "mode": "step_reveal", "reason": "rule 1", "sources": []},
  {"block": "err-BC-ERR-03006", "mode": "step_reveal", "reason": "rule 1", "sources": []},
  {"block": "err-BC-ERR-03020", "mode": "step_reveal", "reason": "rule 1", "sources": []},
  {"block": "err-BC-ERR-99036", "mode": "step_reveal", "reason": "rule 1", "sources": []}
 ],
 "refresher": ["ki-1", "err-BC-ERR-03002", "err-BC-ERR-03006", "err-BC-ERR-03020", "err-BC-ERR-99036", "ex-1"],
 "read_minutes": {"full": 3.65, "brief": 2.82},
 "word_count": {"full": 547, "brief": 423},
 "research_lines": [
  {"file": "research/units/unit-03-differentiation-composite-implicit-inverse.md", "line": "An expression is classified by the operation applied last"}
 ],
 "inferred": [
  {"claim": "No skill of BC-CON-03008 lists essential_knowledge, so ki-1 carries ek_id null and paraphrases the topic's Required mathematical knowledge paragraph.", "settles": "A library pass mapping BC-SKL-03026 to 03029 to a BC-EK (ced:79 prints no essential knowledge statement for topic 3.5)."},
  {"claim": "On the MCQ the classification is held in the head and only the derivative line is written.", "settles": "Timing data on BC-QA-03009 items."}
 ],
 "sources": ["BC-CON-03008", "BC-SKL-03026", "BC-SKL-03027", "BC-SKL-03028", "BC-SKL-03029", "ced:79", "ced:72", "BC-QA-03009", "cr-22:21", "cr-24:19", "BC-ERR-03002", "BC-ERR-03006", "BC-ERR-03020", "BC-ERR-99036", "BC-MIS-03001", "BC-MIS-03012", "BC-MIS-02010", "BC-PRQ-03001", "BC-PRQ-03006", "research/units/unit-03-differentiation-composite-implicit-inverse.md#3.5 Selecting Procedures for Calculating Derivatives", "research/question-analysis/question-archetypes.md#BC-QA-03009 Selecting the differentiation procedure for a given expression", "research/scoring/notation-requirements.md#Simplification", "research/exam/exam-structure.md#Section and part layout"]
}
```
