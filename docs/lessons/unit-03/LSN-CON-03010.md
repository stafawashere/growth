---
title: LSN-CON-03010 Notation for higher-order derivatives
research_date: 2026-09-29
status: designed
purpose: Authoring spec for the concept lesson on BC-CON-03010, reading and writing second and higher derivatives in prime and Leibniz notation, built from authoring_bundle("BC-CON-03010") and the research files it cites, so an author fills plan 15's lesson record without making a teaching decision.
---

# LSN-CON-03010 Notation for higher-order derivatives

Concept BC-CON-03010 (one skill, BC-SKL-03032), topic 3.6 of Unit 3, loaded by one archetype, BC-QA-03008 (family higher-order-derivative), shared with BC-CON-03009. Its only hard parent is BC-SKL-02010 in Unit 2 (docs/lessons/unit-03/README.md, section 1).

## Orientation

Served text, from BC-CON-03010 `description_plain` and the topic's Assessment behaviour paragraph (research/units/unit-03-differentiation-composite-implicit-inverse.md#3.6 Calculating Higher-Order Derivatives): a response reads y'', f''(x) and d^2y/dx^2 as one object, the derivative of the first derivative, and writes the operator d/dx apart from the result. No count, no frequency.

## Key ideas

BC-SKL-03032 maps to BC-EK-FUN-3F2 (ced:80), so one core block, both bands.

- ki-1 (core). Paraphrase of the Required mathematical knowledge paragraph (Notation): the three names for the second derivative and the two for the nth. Anchor quote, 9 words, the first sentence of FUN-3.F.2 on ced:80, which the topic section notes is the part the cached page renders cleanly. Notation line from the concept record.

## Recognition

BC-QA-03008 (research/question-analysis/question-archetypes.md#BC-QA-03008 Higher-order derivative of a function or of a derivative expression): `typical_wording` "find the value of the second derivative at the given point, showing the work that leads to the answer"; `common_givens` a differential equation for dy/dx and a point; `difficulty_variables` "whether the answer must be expressed in the notation of the prompt". The signal for this concept: the stem names the derivative in one notation (y'', or d^2y/dx^2) and supplies the first derivative in the other, or asks what a notation names (the Assessment behaviour's interpretation variant). Shape: an MCQ on the meaning of a notation, or the opening FRQ part (BC-FRQ-2025-Q5-A).

What says "not this concept": dy/dx alone, with no second order named.

## Method choice

One strategy block, both bands.

- st-1, BC-QA-03008. Cue: the stem names the second derivative in one notation and gives the first in the other (`difficulty_variables`, "whether the answer must be expressed in the notation of the prompt"). Method, `expected_solution_path[0]`: differentiate the supplied expression with respect to the independent variable, read as d^2y/dx^2 = y'' = d/dx(y') and written as that first line. Rival: the archetype's `common_distractors` entry "the second derivative reported in the wrong notation", which is BC-ERR-03022 (the error record lists BC-QA-03008); `wrong_approaches` holds no notation entry, so the block carries `evidence_tag: inferred`. Separating feature: d/dx is an operator that acts on y', while dy/dx is a result.

## Solution path

- ex-1, BC-QA-03008, both bands, no calculator. Draw from `parameter_spec`: mixed -2, y_part 3, x_part 1, x_at 2, y_at 1, notation prime; y' = -2xy + 3y + x; derived slope 1; options [-2, 0, -1, 1], distinct, first nonzero. No published BC-QA-03008 item carries this draw.
- Problem in mixed notation: y' is given in prime form and d^2y/dx^2 is asked, with the answer written again as y''(2).
- Steps: the naming line d^2y/dx^2 = d/dx(y'), carrying y' (new); y'(2) (evaluate); y'' by the product and chain rules (new, BC-PT-99022); the value, named in both notations (evaluate, BC-PT-99027). A fluent solver writes all four; the Leibniz naming is the first written line.

## Scoring

BC-QA-03008 lists BC-PT-99022, BC-PT-99023 and BC-PT-99027. ex-1 tags BC-PT-99022 and BC-PT-99027 and the what_a_reader_scores lines are reader_checks output for those two; the BC-PT-99023 line would take the brief band over 450 [inferred]. Loose derivative notation is accepted when intent is clear, and Leibniz form in place of prime is accepted (research/scoring/notation-requirements.md#Derivative notation; sg-24:8), while differentials and derivatives mixed cost the reader's ability to credit the work (research/scoring/common-point-losses.md#Notation points). Whether a higher-order notation slip costs a point on its own is not stated [inferred].

## Traps

One active error meets the skill: BC-ERR-03022, both bands, on ex-1's draw: dy/dx written where d/dx is meant, so y'' reads as dy/dx times y'. Possible reason, words from BC-MIS-03014.

## Representations

None. The topic's Representations paragraph names BC-REP-01, BC-REP-04 and BC-REP-06; a prime against Leibniz table is text layout, not rule 4 (docs/lessons/unit-03/README.md, section 6).

## Prerequisite bridge

- BC-PRQ-03005, from its `description_plain` and `failure_signature`.

## Time

BC-QA-03008 is `no_calculator`, the opening part of an FRQ: Section II Part B, 15.0 minutes per question (research/exam/exam-structure.md#Section and part layout), this part about 5.0 of them (docs/lessons/unit-03/README.md, section 5) [inferred]. Reading the notation is the first written line, d^2y/dx^2 = d/dx(y').

## Checks

Two checks: the bundle holds one error, and check 3 needs three error blocks for its distractors.

- chk-1, completion of ex-1, both bands, notation reading: the second derivative is given in Leibniz form (d^2y/dx^2 in x, y and dy/dx) with dy/dx = 1 at x = 2, and y''(2) is asked in prime form. Key -2.
- chk-2, isomorph, both bands, notation reading: dy/dx = xy + 2y - x is given in Leibniz form and y'' is asked in prime form, first as an expression in x, y and y', then at x = 1. Draw: mixed 1, y_part 2, x_part -1, x_at 1, y_at 1, notation leibniz; slope 2. Key 6.

## Delivery

- orientation, ki-1: text. Rule 5: BC-SKL-03032 carries BC-REP-01 and BC-REP-04, no BC-REP-03 given (docs/lessons/unit-03/README.md, section 6).
- ex-1: step_reveal. Rule 1.
- err-BC-ERR-03022: step_reveal. Rule 1.

## Band plan

- Low (full): orientation, ki-1, st-1, ex-1 with its scoring lines, err-BC-ERR-03022, chk-1, chk-2, the bridge. 448 words, 3.0 minutes (cap 900 and 6).
- Mid (brief): the same blocks, since the lesson has one strategy block, one example, one error block and two checks. 448 words, 3.0 minutes (cap 450 and 3).
- Refresher: ki-1, err-BC-ERR-03022, ex-1.

## Sources

- BC-CON-03010; BC-SKL-03032; BC-EK-FUN-3F2; ced:80
- BC-QA-03008; BC-FRQ-2025-Q5-A; sg-24:8; BC-PT-99022, BC-PT-99027
- BC-ERR-03022; BC-MIS-03014
- BC-PRQ-03005
- research/units/unit-03-differentiation-composite-implicit-inverse.md#3.6 Calculating Higher-Order Derivatives
- research/question-analysis/question-archetypes.md#BC-QA-03008 Higher-order derivative of a function or of a derivative expression
- research/scoring/notation-requirements.md#Derivative notation
- research/scoring/common-point-losses.md#Notation points
- research/exam/exam-structure.md#Section and part layout
- [inferred] Two checks only. Settled by a second and third BC-ERR record held by BC-SKL-03032.
- [inferred] Step 4 carries no BC-PT-99023 tag, for the brief band cap. Settled by a shorter reader_checks text for BC-PT-99023.
- [inferred] Whether a higher-order notation slip costs a point on its own. Settled by a scoring guideline note on a higher-derivative part.
- [inferred] The part's share of the 15.0 minute question. Settled by timing data on BC-FRQ-2025-Q5-A.

## Machine record

```json
{
 "id": "LSN-CON-03010",
 "kind": "concept",
 "target_id": "BC-CON-03010",
 "unit": "03",
 "skills": ["BC-SKL-03032"],
 "orientation": {
  "text": "A response reads y'', f''(x) and d^2y/dx^2 as one object, the derivative of the first derivative, and writes the operator d/dx apart from its result.",
  "sources": ["BC-CON-03010", "research/units/unit-03-differentiation-composite-implicit-inverse.md#3.6 Calculating Higher-Order Derivatives"]
 },
 "key_ideas": [
  {
   "id": "ki-1",
   "ek_id": "BC-EK-FUN-3F2",
   "depth": "core",
   "text": "For y = f(x), the second derivative is written d^2y/dx^2, f''(x) or y''; the nth is d^ny/dx^n or f^(n)(x). Each names d/dx applied again to the previous derivative. d/dx is the operator; dy/dx is its result.",
   "notation": "d squared y over d x squared; f superscript n of x",
   "quote": {"text": "Higher-order derivatives are represented with a variety of notations.", "source": "ced:80"},
   "sources": ["BC-EK-FUN-3F2", "ced:80", "research/units/unit-03-differentiation-composite-implicit-inverse.md#3.6 Calculating Higher-Order Derivatives"]
  }
 ],
 "strategy": [
  {
   "id": "st-1",
   "archetype_id": "BC-QA-03008",
   "cue": "Second derivative named in one notation, first derivative given in the other.",
   "method": "Read d^2y/dx^2 and y'' as one object. First line: d^2y/dx^2 = d/dx(y').",
   "rival": "Rival: dy/dx for d/dx, a product (BC-ERR-03022).",
   "separating_feature": "d/dx acts on y'; dy/dx is a result, never a factor.",
   "sources": ["BC-QA-03008", "BC-ERR-03022"],
   "evidence_tag": "inferred"
  }
 ],
 "worked_examples": [
  {
   "id": "ex-1",
   "archetype_id": "BC-QA-03008",
   "bands": ["low", "mid"],
   "parameter_draw": {"mixed": -2, "y_part": 3, "x_part": 1, "x_at": 2, "y_at": 1, "notation": "prime"},
   "problem": {"text": "y' = -2xy + 3y + x and y(2) = 1. Find d^2y/dx^2 at x = 2, written as y''(2).", "command_verb": "find"},
   "calculator_status": "no_calculator",
   "steps": [
    {"cue": "d^2y/dx^2 and y'' name one object: d/dx applied to y'.", "why": "Write d^2y/dx^2 = d/dx(-2xy + 3y + x).", "expr": "-2*x*y + 3*y + x", "relation": "new"},
    {"cue": "y' reappears, so find y'(2) first.", "why": "-4 + 3 + 2.", "expr": "1", "relation": "evaluate", "subs": {"x": "2", "y": "1"}},
    {"cue": "d/dx of -2xy: product rule; y terms gain y'.", "why": "-2y - 2xy' + 3y' + 1.", "expr": "-2*y - 2*x*yp + 3*yp + 1", "relation": "new", "point_type_id": "BC-PT-99022"},
    {"cue": "Point and y' known.", "why": "-2 - 4 + 3 + 1, so y''(2) = -2.", "expr": "-2", "relation": "evaluate", "subs": {"x": "2", "y": "1", "yp": "1"}, "point_type_id": "BC-PT-99027"}
   ],
   "answer": {"form": "numeric", "expr": "-2"}
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
   "error_id": "BC-ERR-03022",
   "observed_behavior": "The response writes dy in place of dy/dx, or uses dy/dx where the operator d/dx is meant, or mixes the two notations inside one line.",
   "scoring_consequence": "The 2025 Chief Reader report lists this notation as a misconception seen in implicit differentiation responses, and poor notation cost points there (crabbc-25:25).",
   "wrong_step": {"text": "y'' written as dy/dx times y', a product.", "expr": "yp*(-2*x*y + 3*y + x)"},
   "right_step": {"text": "y'' as d/dx applied to y'.", "expr": "-2*y - 2*x*yp + 3*yp + 1"},
   "relation": "distinct",
   "possible_reason": {"misconception_id": "BC-MIS-03014", "text": "treats the symbols for derivatives as labels attached to an answer rather than as operators with a meaning"},
   "sources": ["BC-ERR-03022", "BC-MIS-03014"]
  }
 ],
 "representations": null,
 "prerequisite_bridges": [
  {"prq_id": "BC-PRQ-03005", "text": "f'(x), dy/dx, d^2y/dx^2 and y'' name derivatives; d/dx is the operator. dy for dy/dx, or dy/dx for d/dx, loses the meaning."}
 ],
 "time": {"exam_part": "II-B", "budget_minutes": 15.0, "source": "research/exam/exam-structure.md#Section and part layout", "written_steps": {"ex-1": [1, 2, 3, 4]}, "skipped_steps": {"ex-1": []}},
 "checks": [
  {
   "id": "chk-1",
   "check_kind": "completion",
   "format": "short_answer",
   "bands": ["low", "mid"],
   "archetype_id": "BC-QA-03008",
   "parameter_draw": {"mixed": -2, "y_part": 3, "x_part": 1, "x_at": 2, "y_at": 1, "notation": "prime"},
   "completes": "ex-1",
   "stem": {"text": "d^2y/dx^2 = -2y - 2x dy/dx + 3 dy/dx + 1; at x = 2, y = 1 and dy/dx = 1. Find y''(2).", "command_verb": "find"},
   "key": {"form": "numeric", "expr": "-2"},
   "steps": [
    {"text": "y'' is d^2y/dx^2.", "expr": "-2*y - 2*x*yp + 3*yp + 1", "relation": "new"},
    {"text": "x = 2, y = 1, y' = 1.", "expr": "-2", "relation": "evaluate", "subs": {"x": "2", "y": "1", "yp": "1"}}
   ],
   "calculator_status": "no_calculator",
   "skills": ["BC-SKL-03032"]
  },
  {
   "id": "chk-2",
   "check_kind": "isomorph",
   "format": "short_answer",
   "bands": ["low", "mid"],
   "archetype_id": "BC-QA-03008",
   "parameter_draw": {"mixed": 1, "y_part": 2, "x_part": -1, "x_at": 1, "y_at": 1, "notation": "leibniz"},
   "stem": {"text": "dy/dx = xy + 2y - x, y(1) = 1. Write y'' in x, y and y', then find y''(1).", "command_verb": "find"},
   "key": {"form": "numeric", "expr": "6"},
   "steps": [
    {"text": "y' is the given dy/dx.", "expr": "x*y + 2*y - x", "relation": "new"},
    {"text": "y'(1) = 2.", "expr": "2", "relation": "evaluate", "subs": {"x": "1", "y": "1"}},
    {"text": "y'' = d/dx(y').", "expr": "y + x*yp + 2*yp - 1", "relation": "new"},
    {"text": "Point and slope.", "expr": "6", "relation": "evaluate", "subs": {"x": "1", "y": "1", "yp": "2"}}
   ],
   "calculator_status": "no_calculator",
   "skills": ["BC-SKL-03032"]
  }
 ],
 "delivery": [
  {"block": "orientation", "mode": "text", "reason": "rule 5: BC-REP-01 and BC-REP-04 only", "sources": ["BC-SKL-03032"]},
  {"block": "ki-1", "mode": "text", "reason": "rule 5: a notation list, no BC-REP-03 given", "sources": ["BC-SKL-03032"]},
  {"block": "ex-1", "mode": "step_reveal", "reason": "rule 1", "sources": []},
  {"block": "err-BC-ERR-03022", "mode": "step_reveal", "reason": "rule 1", "sources": []}
 ],
 "refresher": ["ki-1", "err-BC-ERR-03022", "ex-1"],
 "read_minutes": {"full": 3.0, "brief": 3.0},
 "word_count": {"full": 448, "brief": 448},
 "research_lines": [
  {"file": "research/scoring/notation-requirements.md", "line": "sg-24:8 accepts a derivative written in Leibniz form in place of prime notation."}
 ],
 "inferred": [
  {"claim": "The lesson carries two checks: the bundle holds one error, BC-ERR-03022, and check 3 needs three error blocks for its distractors.", "settles": "Further BC-ERR records held by BC-SKL-03032."},
  {"claim": "ex-1 tags BC-PT-99022 and BC-PT-99027 only; the BC-PT-99023 reader line takes the brief band over 450 words.", "settles": "A shorter reader_checks text for BC-PT-99023, or a band rule serving scoring lines to the low band only."},
  {"claim": "Whether a higher-order notation slip costs a point on its own is not stated in the scoring files read.", "settles": "A scoring guideline note on a higher-derivative part."},
  {"claim": "The second derivative part takes about 5.0 of the 15.0 minutes of its Section II question.", "settles": "Timing data on BC-FRQ-2025-Q5-A or a record fixing the part's share."}
 ],
 "sources": ["BC-CON-03010", "BC-SKL-03032", "BC-EK-FUN-3F2", "ced:80", "BC-QA-03008", "BC-FRQ-2025-Q5-A", "sg-24:8", "BC-PT-99022", "BC-PT-99027", "BC-ERR-03022", "BC-MIS-03014", "BC-PRQ-03005", "research/units/unit-03-differentiation-composite-implicit-inverse.md#3.6 Calculating Higher-Order Derivatives", "research/question-analysis/question-archetypes.md#BC-QA-03008 Higher-order derivative of a function or of a derivative expression", "research/scoring/notation-requirements.md#Derivative notation", "research/scoring/common-point-losses.md#Notation points", "research/exam/exam-structure.md#Section and part layout"]
}
```
