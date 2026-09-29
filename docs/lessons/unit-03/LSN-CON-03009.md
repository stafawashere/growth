---
title: LSN-CON-03009 Repeated differentiation
research_date: 2026-09-29
status: designed
purpose: Authoring spec for the concept lesson on BC-CON-03009, the second and higher derivatives, including the second derivative of an implicit relation evaluated at a point, built from authoring_bundle("BC-CON-03009") and the research files it cites, so an author fills plan 15's lesson record without making a teaching decision.
---

# LSN-CON-03009 Repeated differentiation

Concept BC-CON-03009 (skills BC-SKL-03030, BC-SKL-03031, BC-SKL-03033, BC-SKL-03034), topic 3.6 of Unit 3, loaded by one archetype, BC-QA-03008 (family higher-order-derivative), whose official example is BC-FRQ-2025-Q5-A. Its hard parent concepts are BC-CON-03003, BC-CON-03004 and BC-CON-03008 (docs/lessons/unit-03/README.md, section 1).

## Orientation

Served text, from BC-CON-03009 `description_plain` and the topic's Assessment behaviour paragraph (research/units/unit-03-differentiation-composite-implicit-inverse.md#3.6 Calculating Higher-Order Derivatives): a response differentiates the given dy/dx again, product rule on mixed terms and chain rule on y, then substitutes the point and the value of dy/dx there. No count, no frequency.

## Key ideas

All four skills map to BC-EK-FUN-3F1 (ced:80), so one core block, both bands.

- ki-1 (core). Paraphrase of the Required mathematical knowledge paragraphs (Repeated differentiation, Second derivatives of implicit relations, Evaluation order): f'' is the derivative of f', and when dy/dx contains y the second differentiation brings dy/dx back, so its value at the point is found first. No anchor quote, to keep the brief band under 450 words. Notation line from the concept record.

## Recognition

BC-QA-03008 (research/question-analysis/question-archetypes.md#BC-QA-03008 Higher-order derivative of a function or of a derivative expression): `typical_wording` "find the value of the second derivative at the given point, showing the work that leads to the answer"; `common_givens` a differential equation for dy/dx, a point on the solution curve, a function or derivative expression; `asked_to_produce` an expression for the second derivative or its value at a point. The signal: d^2y/dx^2 or y'' requested, with dy/dx already supplied in x and y. Shape: the opening part of a Taylor polynomial or differential equation FRQ, no calculator (BC-FRQ-2025-Q5-A; sg-25:20).

What says "not this concept": dy/dx itself asked from a curve equation (BC-CON-03004), or dy/dx supplied and a slope asked (one substitution, no second differentiation).

## Method choice

One strategy block, both bands.

- st-1, BC-QA-03008. Method, `expected_solution_path[0]`: differentiate the supplied expression with respect to the independent variable. Rival, `wrong_approaches`: the derivative expression differentiated as though y were constant (BC-ERR-05060). Separating feature: y in the dy/dx expression. The archetype carries both fields, so verified.

## Solution path

- ex-1, BC-QA-03008, both bands, no calculator. Draw from `parameter_spec`: mixed 2, y_part 1, x_part -3, x_at 1, y_at 2, notation leibniz; dy/dx = 2xy + y - 3x; derived slope 3; options [10, 6, 1, 3], distinct, first nonzero. No published BC-QA-03008 item carries this draw.
- Steps, in the order BC-SKL-03034's `description_plain` sets (dy/dx at the point first): dy/dx (new); its value at (1, 2) (evaluate); the product rule on 2xy (new, BC-PT-99022); the full second derivative with the chain rule on y (new, untagged; see Scoring); the value (evaluate, BC-PT-99027). A fluent solver writes all five; steps 3 and 4 are one written line in the response.

## Scoring

BC-QA-03008 lists BC-PT-99022, BC-PT-99023 and BC-PT-99027. ex-1 tags BC-PT-99022 on step 3 and BC-PT-99027 on step 5, and the what_a_reader_scores lines are reader_checks output for those two; the BC-PT-99023 line (60 words) would take the brief band over 450, so step 4 carries no tag [inferred]. The 2025 guidelines award the product rule, the chain rule and the value separately, so the two rule points survive an arithmetic slip (sg-25:20). A general expression equated to a number costs credit (research/scoring/notation-requirements.md#The equal sign), so the response writes the value after an evaluation, not after d^2y/dx^2 in general.

## Traps

Five active errors meet the skills; the cap is four, so the first four in the bundle's order: BC-ERR-03008, BC-ERR-03011, BC-ERR-03023, BC-ERR-05060. BC-ERR-03021 (first derivative reported for the second) is left out by the cap. Low band all four; mid band the first two. All on ex-1's draw.

- err-BC-ERR-03008: 2xy differentiated as 2x dy/dx. Possible reason, words from BC-MIS-03005.
- err-BC-ERR-03011: only x = 1 put into dy/dx. No possible reason line: the linked descriptions do not name the substitution.
- err-BC-ERR-03023: 3 dy/dx + 1 left unevaluated. No possible reason line, for the same cause.
- err-BC-ERR-05060: y held constant. Possible reason, words from BC-MIS-05033.

## Representations

None. The topic's Representations paragraph names BC-REP-01, BC-REP-04 and BC-REP-06, none figure-shaped.

## Prerequisite bridge

- BC-PRQ-03002, BC-PRQ-03005, BC-PRQ-03006, each from its `description_plain` and `failure_signature`.

## Time

BC-QA-03008 is `no_calculator`, the opening part of an FRQ: Section II Part B, 15.0 minutes per question (research/exam/exam-structure.md#Section and part layout), this part about 5.0 of them (docs/lessons/unit-03/README.md, section 5) [inferred: the share is not fixed by a record]. The minutes go on the differentiated line; the evaluation is arithmetic.

## Checks

- chk-1, completion of ex-1, both bands: the second derivative and dy/dx = 3 at (1, 2) are given. Key 10.
- chk-2, isomorph, both bands. Draw: mixed -1, y_part 2, x_part 3, x_at 1, y_at 1, notation prime; y' = -xy + 2y + 3x, slope 4. Key y''(1) = 6.
- chk-3, MCQ, low band. Draw: mixed 1, y_part 2, x_part 1, x_at 2, y_at -1, notation leibniz; dy/dx = xy + 2y + x, slope -2. Key -8. Distractors: -7 (BC-ERR-03008), 0 (BC-ERR-05060), y + 4 dy/dx + 1 (BC-ERR-03011, only x = 2 substituted).

## Delivery

- orientation, ki-1: text. Rule 5: the skills carry BC-REP-01 only, and repeated differentiation is not one of rule 2's processes (docs/lessons/unit-03/README.md, section 6).
- ex-1: step_reveal. Rule 1.
- err-BC-ERR-03008, err-BC-ERR-03011, err-BC-ERR-03023, err-BC-ERR-05060: step_reveal. Rule 1.

## Band plan

- Low (full): orientation, ki-1, st-1, ex-1 with its scoring lines, the four error blocks, chk-1 to chk-3, the three bridges. 560 words, 3.8 minutes (cap 900 and 6).
- Mid (brief): orientation, ki-1, st-1, ex-1 with its scoring lines, err-BC-ERR-03008, err-BC-ERR-03011, chk-1, chk-2, the three bridges. 442 words, 3.0 minutes (cap 450 and 3).
- Refresher: ki-1, err-BC-ERR-03008, err-BC-ERR-03011, err-BC-ERR-03023, err-BC-ERR-05060, ex-1.

## Sources

- BC-CON-03009; BC-SKL-03030, BC-SKL-03031, BC-SKL-03033, BC-SKL-03034; BC-EK-FUN-3F1; ced:80
- BC-QA-03008; BC-FRQ-2025-Q5-A; sg-25:20; BC-PT-99022, BC-PT-99023, BC-PT-99027
- BC-ERR-03008, BC-ERR-03011, BC-ERR-03023, BC-ERR-05060, BC-ERR-03021; BC-MIS-03005, BC-MIS-05033
- BC-PRQ-03002, BC-PRQ-03005, BC-PRQ-03006
- research/units/unit-03-differentiation-composite-implicit-inverse.md#3.6 Calculating Higher-Order Derivatives
- research/question-analysis/question-archetypes.md#BC-QA-03008 Higher-order derivative of a function or of a derivative expression
- research/scoring/notation-requirements.md#The equal sign
- research/exam/exam-structure.md#Section and part layout
- [inferred] Step 4 carries no BC-PT-99023 tag, for the brief band cap. Settled by a shorter reader_checks text for BC-PT-99023.
- [inferred] The part's share of the 15.0 minute question. Settled by timing data on BC-FRQ-2025-Q5-A.

## Machine record

```json
{
 "id": "LSN-CON-03009",
 "kind": "concept",
 "target_id": "BC-CON-03009",
 "unit": "03",
 "skills": ["BC-SKL-03030", "BC-SKL-03031", "BC-SKL-03033", "BC-SKL-03034"],
 "orientation": {
  "text": "A response differentiates dy/dx again, product rule on mixed terms and chain rule on y, then substitutes the point and the value of dy/dx there.",
  "sources": ["BC-CON-03009", "research/units/unit-03-differentiation-composite-implicit-inverse.md#3.6 Calculating Higher-Order Derivatives"]
 },
 "key_ideas": [
  {
   "id": "ki-1",
   "ek_id": "BC-EK-FUN-3F1",
   "depth": "core",
   "text": "Differentiating f' gives f''; repeating gives higher derivatives. When dy/dx contains y, the second differentiation needs the product rule on mixed terms and the chain rule on y, so dy/dx reappears and its value at the point is needed.",
   "notation": "f double prime; f superscript n",
   "quote": null,
   "sources": ["BC-EK-FUN-3F1", "ced:80", "sg-25:20", "research/units/unit-03-differentiation-composite-implicit-inverse.md#3.6 Calculating Higher-Order Derivatives"]
  }
 ],
 "strategy": [
  {
   "id": "st-1",
   "archetype_id": "BC-QA-03008",
   "cue": "d^2y/dx^2 asked at a point, dy/dx given in x and y.",
   "method": "First line: d/dx of the dy/dx expression.",
   "rival": "Rival: y held constant (BC-ERR-05060).",
   "separating_feature": "y in dy/dx means each y term gains a dy/dx factor.",
   "sources": ["BC-QA-03008"],
   "evidence_tag": "verified"
  }
 ],
 "worked_examples": [
  {
   "id": "ex-1",
   "archetype_id": "BC-QA-03008",
   "bands": ["low", "mid"],
   "parameter_draw": {"mixed": 2, "y_part": 1, "x_part": -3, "x_at": 1, "y_at": 2, "notation": "leibniz"},
   "problem": {"text": "dy/dx = 2xy + y - 3x. Find d^2y/dx^2 at the point (1, 2).", "command_verb": "find"},
   "calculator_status": "no_calculator",
   "steps": [
    {"cue": "dy/dx will reappear: find its value first.", "why": "The given expression.", "expr": "2*x*y + y - 3*x", "relation": "new"},
    {"cue": "Substitute (1, 2).", "why": "4 + 2 - 3.", "expr": "3", "relation": "evaluate", "subs": {"x": "1", "y": "2"}},
    {"cue": "2xy is x times y.", "why": "Product rule: 2y + 2x dy/dx.", "expr": "2*y + 2*x*yp", "relation": "new", "point_type_id": "BC-PT-99022"},
    {"cue": "y is a function of x.", "why": "Chain rule: y gives dy/dx.", "expr": "2*y + 2*x*yp + yp - 3", "relation": "new"},
    {"cue": "Point and slope known.", "why": "x = 1, y = 2, dy/dx = 3.", "expr": "10", "relation": "evaluate", "subs": {"x": "1", "y": "2", "yp": "3"}, "point_type_id": "BC-PT-99027"}
   ],
   "answer": {"form": "numeric", "expr": "10"}
  }
 ],
 "what_a_reader_scores": [
  {"example_id": "ex-1", "point_type_ids": ["BC-PT-99022", "BC-PT-99027"], "lines": [
   {"point_type_id": "BC-PT-99022", "text": "Product rule. Earned by: A differentiation that correctly applies the product rule to the given expression (sg-25:20, sg-22:16). Not earned by: A response that treats one factor as constant, which sg-22:16 states is eligible for the chain rule point but not this one."},
   {"point_type_id": "BC-PT-99027", "text": "Higher derivative expression evaluated at a point. Earned by: A correct expression for the second or higher derivative, evaluated at the requested point, consistent with the earlier derivative work (sg-25:20, sg-23:10). Not earned by: An expression left in terms of the first derivative where the prompt asked for it in terms of the dependent variable (sg-23:11)."}
  ]}
 ],
 "common_errors": [
  {
   "error_id": "BC-ERR-03008",
   "observed_behavior": "A term that is a product of an expression in x and an expression in y is differentiated as though one of the two were constant.",
   "scoring_consequence": "The differentiation loses the point for a completely correct implicit derivative, and the 2025 scoring guidelines award the product rule its own point (sg-25:20, crabbc-25:24).",
   "wrong_step": {"text": "2x dy/dx.", "expr": "2*x*yp + yp - 3"},
   "right_step": {"text": "2y + 2x dy/dx.", "expr": "2*y + 2*x*yp + yp - 3"},
   "relation": "distinct",
   "possible_reason": {"misconception_id": "BC-MIS-03005", "text": "reads a term containing both variables as one object rather than as a product"},
   "sources": ["BC-ERR-03008", "BC-MIS-03005"]
  },
  {
   "error_id": "BC-ERR-03011",
   "observed_behavior": "The response substitutes the x coordinate into an expression containing both variables and reports a slope still containing y.",
   "scoring_consequence": "No numerical slope is produced, so the evaluation point is lost.",
   "wrong_step": {"text": "x = 1 only.", "expr": "3*y - 3"},
   "right_step": {"text": "Both coordinates.", "expr": "3"},
   "relation": "distinct",
   "possible_reason": null,
   "sources": ["BC-ERR-03011"]
  },
  {
   "error_id": "BC-ERR-03023",
   "observed_behavior": "An expression for the second derivative containing dy/dx is evaluated without first computing the value of dy/dx at the point.",
   "scoring_consequence": "The numerical second derivative is wrong, although the product and chain rule points described in the 2025 scoring guidelines may still be earned (sg-25:20).",
   "wrong_step": {"text": "3 dy/dx + 1 reported.", "expr": "3*yp + 1"},
   "right_step": {"text": "dy/dx = 3 substituted.", "expr": "10"},
   "relation": "distinct",
   "possible_reason": null,
   "sources": ["BC-ERR-03023"]
  },
  {
   "error_id": "BC-ERR-05060",
   "observed_behavior": "The response differentiates the derivative expression without applying the chain rule to the dependent variable.",
   "scoring_consequence": "The differentiation point is lost, and the value point remains available only through a correct substitution.",
   "wrong_step": {"text": "y held constant.", "expr": "2*y - 3"},
   "right_step": {"text": "Each y term gains dy/dx.", "expr": "2*y + 2*x*yp + yp - 3"},
   "relation": "distinct",
   "possible_reason": {"misconception_id": "BC-MIS-05033", "text": "differentiates expressions in the second variable without the chain rule"},
   "sources": ["BC-ERR-05060", "BC-MIS-05033"]
  }
 ],
 "representations": null,
 "prerequisite_bridges": [
  {"prq_id": "BC-PRQ-03002", "text": "Collect the dy/dx terms, then divide; otherwise dy/dx is never isolated."},
  {"prq_id": "BC-PRQ-03005", "text": "d/dx is the operator, dy/dx the result; swapping them loses the meaning."},
  {"prq_id": "BC-PRQ-03006", "text": "A wrong simplification after a correct derivative changes the value reported."}
 ],
 "time": {"exam_part": "II-B", "budget_minutes": 15.0, "source": "research/exam/exam-structure.md#Section and part layout", "written_steps": {"ex-1": [1, 2, 3, 4, 5]}, "skipped_steps": {"ex-1": []}},
 "checks": [
  {
   "id": "chk-1",
   "check_kind": "completion",
   "format": "short_answer",
   "bands": ["low", "mid"],
   "archetype_id": "BC-QA-03008",
   "parameter_draw": {"mixed": 2, "y_part": 1, "x_part": -3, "x_at": 1, "y_at": 2, "notation": "leibniz"},
   "completes": "ex-1",
   "stem": {"text": "d^2y/dx^2 = 2y + 2x dy/dx + dy/dx - 3; dy/dx = 3 at (1, 2). Evaluate there.", "command_verb": "find"},
   "key": {"form": "numeric", "expr": "10"},
   "steps": [
    {"text": "The second derivative.", "expr": "2*y + 2*x*yp + yp - 3", "relation": "new"},
    {"text": "x = 1, y = 2, dy/dx = 3.", "expr": "10", "relation": "evaluate", "subs": {"x": "1", "y": "2", "yp": "3"}}
   ],
   "calculator_status": "no_calculator",
   "skills": ["BC-SKL-03034"]
  },
  {
   "id": "chk-2",
   "check_kind": "isomorph",
   "format": "short_answer",
   "bands": ["low", "mid"],
   "archetype_id": "BC-QA-03008",
   "parameter_draw": {"mixed": -1, "y_part": 2, "x_part": 3, "x_at": 1, "y_at": 1, "notation": "prime"},
   "stem": {"text": "y' = -xy + 2y + 3x and y(1) = 1. Find y''(1).", "command_verb": "find"},
   "key": {"form": "numeric", "expr": "6"},
   "steps": [
    {"text": "y'.", "expr": "-x*y + 2*y + 3*x", "relation": "new"},
    {"text": "y'(1) = 4.", "expr": "4", "relation": "evaluate", "subs": {"x": "1", "y": "1"}},
    {"text": "y'' by the product and chain rules.", "expr": "-y - x*yp + 2*yp + 3", "relation": "new"},
    {"text": "x = 1, y = 1, y' = 4.", "expr": "6", "relation": "evaluate", "subs": {"x": "1", "y": "1", "yp": "4"}}
   ],
   "calculator_status": "no_calculator",
   "skills": ["BC-SKL-03033", "BC-SKL-03034"]
  },
  {
   "id": "chk-3",
   "check_kind": "mcq",
   "format": "mcq",
   "bands": ["low"],
   "archetype_id": "BC-QA-03008",
   "parameter_draw": {"mixed": 1, "y_part": 2, "x_part": 1, "x_at": 2, "y_at": -1, "notation": "leibniz"},
   "stem": {"text": "dy/dx = xy + 2y + x through (2, -1). What is d^2y/dx^2 at (2, -1)?", "command_verb": "identify"},
   "key": {"form": "numeric", "expr": "-8"},
   "steps": [
    {"text": "dy/dx.", "expr": "x*y + 2*y + x", "relation": "new"},
    {"text": "dy/dx = -2 at the point.", "expr": "-2", "relation": "evaluate", "subs": {"x": "2", "y": "-1"}},
    {"text": "The second derivative.", "expr": "y + x*yp + 2*yp + 1", "relation": "new"},
    {"text": "Point and slope.", "expr": "-8", "relation": "evaluate", "subs": {"x": "2", "y": "-1", "yp": "-2"}}
   ],
   "options": [
    {"id": "A", "is_key": false, "expr": "-7", "error_path": "BC-ERR-03008", "derivation": "product rule omitted on xy: x dy/dx + 2 dy/dx + 1"},
    {"id": "B", "is_key": true, "expr": "-8", "error_path": null},
    {"id": "C", "is_key": false, "expr": "0", "error_path": "BC-ERR-05060", "derivation": "y held constant: y + 1"},
    {"id": "D", "is_key": false, "expr": "y + 4*yp + 1", "error_path": "BC-ERR-03011", "derivation": "only x = 2 substituted"}
   ],
   "calculator_status": "no_calculator",
   "skills": ["BC-SKL-03033", "BC-SKL-03034"]
  }
 ],
 "delivery": [
  {"block": "orientation", "mode": "text", "reason": "rule 5: BC-REP-01 only on the skills", "sources": ["BC-SKL-03030"]},
  {"block": "ki-1", "mode": "text", "reason": "rule 5: repeated differentiation is not a rule 2 process", "sources": ["BC-SKL-03030", "BC-SKL-03033"]},
  {"block": "ex-1", "mode": "step_reveal", "reason": "rule 1", "sources": []},
  {"block": "err-BC-ERR-03008", "mode": "step_reveal", "reason": "rule 1", "sources": []},
  {"block": "err-BC-ERR-03011", "mode": "step_reveal", "reason": "rule 1", "sources": []},
  {"block": "err-BC-ERR-03023", "mode": "step_reveal", "reason": "rule 1", "sources": []},
  {"block": "err-BC-ERR-05060", "mode": "step_reveal", "reason": "rule 1", "sources": []}
 ],
 "refresher": ["ki-1", "err-BC-ERR-03008", "err-BC-ERR-03011", "err-BC-ERR-03023", "err-BC-ERR-05060", "ex-1"],
 "read_minutes": {"full": 3.8, "brief": 3.0},
 "word_count": {"full": 560, "brief": 442},
 "research_lines": [
  {"file": "research/units/unit-03-differentiation-composite-implicit-inverse.md", "line": "so dy/dx reappears and must be replaced by its value before a number is reported"}
 ],
 "inferred": [
  {"claim": "ex-1 tags BC-PT-99022 and BC-PT-99027 only; the chain rule step carries no BC-PT-99023 tag because its reader line takes the brief band over the 450 word cap.", "settles": "A shorter reader_checks text for BC-PT-99023, or a band rule that serves scoring lines to the low band only."},
  {"claim": "The second derivative part takes about 5.0 of the 15.0 minutes of its Section II question.", "settles": "Timing data on BC-FRQ-2025-Q5-A or a record fixing the part's share."}
 ],
 "sources": ["BC-CON-03009", "BC-SKL-03030", "BC-SKL-03031", "BC-SKL-03033", "BC-SKL-03034", "BC-EK-FUN-3F1", "ced:80", "BC-QA-03008", "BC-FRQ-2025-Q5-A", "sg-25:20", "BC-PT-99022", "BC-PT-99023", "BC-PT-99027", "BC-ERR-03008", "BC-ERR-03011", "BC-ERR-03023", "BC-ERR-05060", "BC-ERR-03021", "BC-MIS-03005", "BC-MIS-05033", "BC-PRQ-03002", "BC-PRQ-03005", "BC-PRQ-03006", "research/units/unit-03-differentiation-composite-implicit-inverse.md#3.6 Calculating Higher-Order Derivatives", "research/question-analysis/question-archetypes.md#BC-QA-03008 Higher-order derivative of a function or of a derivative expression", "research/scoring/notation-requirements.md#The equal sign", "research/exam/exam-structure.md#Section and part layout"]
}
```
