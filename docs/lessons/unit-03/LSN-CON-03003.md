---
title: LSN-CON-03003 A dependent variable inside an equation
research_date: 2026-09-29
status: designed
purpose: Authoring spec for the concept lesson on BC-CON-03003, differentiating an equation in which y depends on x, built from authoring_bundle("BC-CON-03003") and the research files it cites, so an author fills plan 15's lesson record without making a teaching decision.
---

# LSN-CON-03003 A dependent variable inside an equation

Concept BC-CON-03003 (skills BC-SKL-03007, BC-SKL-03008, BC-SKL-03009), topic 3.2 of Unit 3, loaded by one archetype, BC-QA-03004 (family implicit-differentiation), which it shares with BC-CON-03004. Its hard parent concept is BC-CON-03002 (docs/lessons/unit-03/README.md, section 1).

## Orientation

Served text, from BC-CON-03003 `description_plain` and the topic's Assessment behaviour paragraph (research/units/unit-03-differentiation-composite-implicit-inverse.md#3.2 Implicit Differentiation): a response differentiates both sides of an equation in x and y, gives every y term a dy/dx factor and every mixed term the product rule, and keeps the right side. The opening part of a multipart question asks for it. No count, no frequency.

## Key ideas

The three skills map to one BC-EK, BC-EK-FUN-3D1 (ced:76), so one core block, both bands.

- ki-1 (core). Paraphrase of the Required mathematical knowledge paragraph (Implicit differentiation, The dy/dx factor, Mixed terms): under the hypothesis that the equation determines y as a differentiable function of x, differentiate both sides with respect to x; each y term gives its y derivative times dy/dx; a mixed term is a product. Anchor quote (9 words) from ced:76, found on the cached page, served in the low and mid bands. Notation line from the concept record.

## Recognition

BC-QA-03004 (research/question-analysis/question-archetypes.md#BC-QA-03004 Implicit differentiation producing or verifying dy/dx): `typical_wording` "find dy/dx for the curve defined by the given equation", "show that dy/dx is equal to the stated expression for the given curve"; `common_givens` an equation in x and y defining a curve, a stated expression for dy/dx to verify, a point on the curve; `asked_to_produce` an implicit derivative dy/dx, a verification, a numerical slope at a point. The signal: the stem names a curve by an equation not solved for y, and asks for dy/dx. Shapes: an MCQ (BC-MCQ-CED-004) or the opening part of a no-calculator FRQ built on one curve (cr-23:22, cr-24:17).

What says "not this concept": the stem gives y = an expression in x, which is differentiated directly (docs/lessons/unit-03/README.md, section 3, BC-EK-FUN-3D1). A term such as 3xy is the feature that adds the product rule; a y term inside a power adds the chain rule factor.

## Method choice

One strategy block, both bands.

- st-1, BC-QA-03004. Cue from `asked_to_produce` and `common_givens`. Method, `expected_solution_path[0]`: differentiate every term of both sides with respect to x. First written line: d/dx applied to both sides, the right side kept. Rival, `wrong_approaches`: differentiating y terms as though y were the independent variable (BC-ERR-03007). Separating feature: y depends on x, so every y term carries dy/dx.

The archetype carries both fields in the snapshot, so the block is not tagged inferred.

## Solution path

- ex-1, BC-QA-03004, both bands, no calculator. Draw from `parameter_spec`: mixed 3, y_coefficient 1, right_slope 2, x_at 1, y_at 1, y_power 2. The curve is x^2 + 3xy + y^2 = 2x + 3 (c = 3, nonzero). Derived: y_rate 2, denominator 5, options -3/5, -5/3, -3/2, -1, distinct and the key nonzero, so every constraint holds. No published BC-QA-03004 item carries this draw.
- Steps follow `expected_solution_path`: differentiate both sides (no value); the differentiated equation with dy/dx on each y term and the product rule on 3xy (valued, new); collect (equivalent); divide (solve for dy/dx); substitute the point (evaluate). dy/dx is written as the symbol dydx in the SymPy strings.
- A fluent solver writes steps 2 to 5; step 1 is the decision, held in the head. Steps 3 and 4 belong to BC-CON-03004 and are shown so the example ends where the stem ends.

## Scoring

BC-QA-03004 lists no `point_types`, so the lesson carries no what_a_reader_scores entry, no step carries a point tag, and no served text in the machine record names a point beyond the error records' own scoring_consequence text. For the author: the Chief Reader reports describe an eligible-attempt point and a completely-correct-differentiation point on this shape (cr-23:22, cr-24:17; research/question-analysis/question-archetypes.md#BC-QA-03004 Implicit differentiation producing or verifying dy/dx), and the snapshot holds no BC-PT for them (docs/lessons/unit-03/README.md, section 7).

## Traps

Three active errors meet the skills, in the bundle's order (linked BC-MIS at severity high): all served in the low band, the first two in the mid band. Wrong and right steps are the differentiated equation on ex-1's draw.

- err-BC-ERR-03007: 2y in place of 2y dy/dx. Possible reason, words from BC-MIS-03004.
- err-BC-ERR-03008: 3xy differentiated as 3y, the x dy/dx term missing. Possible reason, words from BC-MIS-03005.
- err-BC-ERR-03009: right side derivative dropped, so the equation ends in 0 instead of 2. No possible reason line: the linked descriptions (BC-MIS-03004, BC-MIS-99011) do not describe dropping a side.

## Representations

None. The topic's Representations paragraph names a slope-field conversion and a geometric tangent statement; the first belongs to Unit 7 and the second to BC-CON-03005.

## Prerequisite bridge

- BC-PRQ-03005, from its `description_plain` and `failure_signature`.

## Time

BC-QA-03004 is `no_calculator` and "ordinarily the opening part of a multipart free response question", so the part is Section II Part B, 15.0 minutes per question (research/exam/exam-structure.md#Section and part layout), of which this part is a share [inferred: no BC-PT record fixes its points; docs/lessons/unit-03/README.md, section 5]. The MCQ form sits in Part A at 2.14. A fluent solver writes the differentiated equation in one line with every dy/dx visible, because later parts reuse the curve and an error propagates (cr-23:22).

## Checks

- chk-1, completion of ex-1, both bands: the differentiated equation is given, the student solves and evaluates. Key -3/5.
- chk-2, isomorph, both bands. Draw: mixed -2, y_coefficient 1, right_slope 1, x_at 1, y_at -1, y_power 2; curve x^2 - 2xy + y^2 = x + 3. Key 3/4.
- chk-3, MCQ, low band. Draw: mixed 1, y_coefficient 2, right_slope 4, x_at 2, y_at -1, y_power 2; curve x^2 + xy + 2y^2 = 4x - 4. Key -1/2. Distractors: 5/2 (BC-ERR-03007), -1/4 (BC-ERR-03008), 3/2 (BC-ERR-03009).

## Delivery

- orientation: text. Rule 5; the skills carry BC-REP-01 only.
- ki-1: text. Rule 5; the dy/dx factor is an algebraic statement.
- ex-1: step_reveal. Rule 1.
- err-BC-ERR-03007, err-BC-ERR-03008, err-BC-ERR-03009: step_reveal. Rule 1.

## Band plan

- Low (full): orientation, ki-1, st-1, ex-1, the three error blocks, chk-1 to chk-3, the bridge. 534 words, 3.6 minutes (cap 900 and 6).
- Mid (brief): orientation, ki-1, st-1, ex-1, err-BC-ERR-03007, err-BC-ERR-03008, chk-1, chk-2, the bridge. 449 words, 3.0 minutes (cap 450 and 3).
- Refresher: ki-1, err-BC-ERR-03007, err-BC-ERR-03008, err-BC-ERR-03009, ex-1.

## Sources

- BC-CON-03003; BC-SKL-03007, BC-SKL-03008, BC-SKL-03009; BC-EK-FUN-3D1; ced:76
- BC-QA-03004; BC-MCQ-CED-004; cr-23:22, cr-24:17
- BC-ERR-03007, BC-ERR-03008, BC-ERR-03009; BC-MIS-03004, BC-MIS-03005, BC-MIS-99011
- BC-PRQ-03005
- research/units/unit-03-differentiation-composite-implicit-inverse.md#3.2 Implicit Differentiation
- research/question-analysis/question-archetypes.md#BC-QA-03004 Implicit differentiation producing or verifying dy/dx
- research/exam/exam-structure.md#Section and part layout
- [inferred] The share of the 15.0 minutes this part takes. Settled by a BC-PT mapping for the implicit differentiation part.
- [inferred] Text and step reveal only. Settled by the modality A/B.

## Machine record

```json
{
 "id": "LSN-CON-03003",
 "kind": "concept",
 "target_id": "BC-CON-03003",
 "unit": "03",
 "skills": ["BC-SKL-03007", "BC-SKL-03008", "BC-SKL-03009"],
 "orientation": {
  "text": "A response differentiates both sides of an equation in x and y with respect to x: every y term carries dy/dx, every mixed term takes the product rule, and the right side is kept. It opens a multipart question.",
  "sources": ["BC-CON-03003", "research/units/unit-03-differentiation-composite-implicit-inverse.md#3.2 Implicit Differentiation"]
 },
 "key_ideas": [
  {
   "id": "ki-1",
   "ek_id": "BC-EK-FUN-3D1",
   "depth": "core",
   "text": "When an equation determines y as a differentiable function of x, differentiate both sides with respect to x. A y term gives its derivative in y times dy/dx. A term holding both variables is a product, and its y factor still carries dy/dx. The result is linear in dy/dx.",
   "notation": "d/dx of y to the n equals n times y to the n minus one times dy/dx",
   "quote": {"text": "The chain rule is the basis for implicit differentiation.", "source": "ced:76"},
   "sources": ["BC-EK-FUN-3D1", "ced:76", "research/units/unit-03-differentiation-composite-implicit-inverse.md#3.2 Implicit Differentiation"]
  }
 ],
 "strategy": [
  {
   "id": "st-1",
   "archetype_id": "BC-QA-03004",
   "cue": "The stem asks for dy/dx or a slope at a point, from an equation in x and y defining a curve.",
   "method": "First written line: differentiate every term of both sides with respect to x.",
   "rival": "Rival: differentiating y terms as though y were the independent variable (BC-ERR-03007).",
   "separating_feature": "y depends on x, so every y term carries dy/dx.",
   "sources": ["BC-QA-03004"],
   "evidence_tag": "verified"
  }
 ],
 "worked_examples": [
  {
   "id": "ex-1",
   "archetype_id": "BC-QA-03004",
   "bands": ["low", "mid"],
   "parameter_draw": {"mixed": 3, "y_coefficient": 1, "right_slope": 2, "x_at": 1, "y_at": 1, "y_power": 2},
   "problem": {"text": "The curve x^2 + 3xy + y^2 = 2x + 3 passes through (1, 1). Find dy/dx at (1, 1).", "command_verb": "find"},
   "calculator_status": "no_calculator",
   "steps": [
    {"cue": "An equation in x and y, not solved for y.", "why": "y depends on x: differentiate both sides with respect to x."},
    {"cue": "y^2 is a y term; 3xy holds both variables.", "why": "2y dy/dx; 3y + 3x dy/dx; the right side gives 2.", "expr": "2*x + 3*y + 3*x*dydx + 2*y*dydx = 2", "relation": "new"},
    {"cue": "The line is linear in dy/dx.", "why": "Collect the two dy/dx terms and factor.", "expr": "dydx*(3*x + 2*y) = 2 - 2*x - 3*y", "relation": "equivalent"},
    {"cue": "One bracket multiplies dy/dx.", "why": "Divide by it; it is 5 at (1, 1).", "expr": "dydx = (2 - 2*x - 3*y)/(3*x + 2*y)", "relation": "solve", "variable": "dydx"},
    {"cue": "The stem gives the point (1, 1).", "why": "Both coordinates go in.", "expr": "-3/5", "relation": "evaluate", "subs": {"x": "1", "y": "1"}}
   ],
   "answer": {"form": "numeric", "expr": "-3/5"}
  }
 ],
 "what_a_reader_scores": [],
 "common_errors": [
  {
   "error_id": "BC-ERR-03007",
   "observed_behavior": "In an implicit differentiation the y terms are differentiated as though y were the independent variable, so no dy/dx factor appears.",
   "scoring_consequence": "The differentiation is not eligible for the completely correct differentiation point described in the Chief Reader reports (crabbc-25:24).",
   "wrong_step": {"text": "y^2 gives 2y.", "expr": "2*x + 3*y + 3*x*dydx + 2*y = 2"},
   "right_step": {"text": "y^2 gives 2y dy/dx.", "expr": "2*x + 3*y + 3*x*dydx + 2*y*dydx = 2"},
   "relation": "distinct",
   "possible_reason": {"misconception_id": "BC-MIS-03004", "text": "y as a second free variable rather than as a function of x"},
   "sources": ["BC-ERR-03007", "BC-MIS-03004"]
  },
  {
   "error_id": "BC-ERR-03008",
   "observed_behavior": "A term that is a product of an expression in x and an expression in y is differentiated as though one of the two were constant.",
   "scoring_consequence": "The differentiation loses the point for a completely correct implicit derivative, and the 2025 scoring guidelines award the product rule its own point (sg-25:20, crabbc-25:24).",
   "wrong_step": {"text": "3xy gives 3y.", "expr": "2*x + 3*y + 2*y*dydx = 2"},
   "right_step": {"text": "3xy gives 3y + 3x dy/dx.", "expr": "2*x + 3*y + 3*x*dydx + 2*y*dydx = 2"},
   "relation": "distinct",
   "possible_reason": {"misconception_id": "BC-MIS-03005", "text": "a term containing both variables as one object rather than as a product"},
   "sources": ["BC-ERR-03008", "BC-MIS-03005"]
  },
  {
   "error_id": "BC-ERR-03009",
   "observed_behavior": "The response differentiates the left hand side and omits the equals zero or the derivative of the right hand side, leaving an expression rather than an equation.",
   "scoring_consequence": "The Chief Reader report for 2025 records that responses dropping the equals zero were generally unable to recover and earned neither of the first two points (crabbc-25:25).",
   "wrong_step": {"text": "Right side dropped: = 0.", "expr": "2*x + 3*y + 3*x*dydx + 2*y*dydx = 0"},
   "right_step": {"text": "Right side 2x + 3 gives 2.", "expr": "2*x + 3*y + 3*x*dydx + 2*y*dydx = 2"},
   "relation": "distinct",
   "possible_reason": null,
   "sources": ["BC-ERR-03009"]
  }
 ],
 "representations": null,
 "prerequisite_bridges": [
  {"prq_id": "BC-PRQ-03005", "text": "dy/dx is a derivative, d/dx the operator. Writing dy for dy/dx loses the meaning of the line."}
 ],
 "time": {"exam_part": "II-B", "budget_minutes": 15.0, "source": "research/exam/exam-structure.md#Section and part layout", "written_steps": {"ex-1": [2, 3, 4, 5]}, "skipped_steps": {"ex-1": [1]}},
 "checks": [
  {
   "id": "chk-1",
   "check_kind": "completion",
   "format": "short_answer",
   "bands": ["low", "mid"],
   "archetype_id": "BC-QA-03004",
   "parameter_draw": {"mixed": 3, "y_coefficient": 1, "right_slope": 2, "x_at": 1, "y_at": 1, "y_power": 2},
   "completes": "ex-1",
   "stem": {"text": "Given 2x + 3y + 3x dy/dx + 2y dy/dx = 2, find dy/dx at (1, 1).", "command_verb": "find"},
   "key": {"form": "numeric", "expr": "-3/5"},
   "steps": [
    {"text": "The differentiated equation.", "expr": "2*x + 3*y + 3*x*dydx + 2*y*dydx = 2", "relation": "new"},
    {"text": "Solved for dy/dx.", "expr": "dydx = (2 - 2*x - 3*y)/(3*x + 2*y)", "relation": "solve", "variable": "dydx"},
    {"text": "At (1, 1).", "expr": "-3/5", "relation": "evaluate", "subs": {"x": "1", "y": "1"}}
   ],
   "calculator_status": "no_calculator",
   "skills": ["BC-SKL-03009"]
  },
  {
   "id": "chk-2",
   "check_kind": "isomorph",
   "format": "short_answer",
   "bands": ["low", "mid"],
   "archetype_id": "BC-QA-03004",
   "parameter_draw": {"mixed": -2, "y_coefficient": 1, "right_slope": 1, "x_at": 1, "y_at": -1, "y_power": 2},
   "stem": {"text": "For x^2 - 2xy + y^2 = x + 3, find dy/dx at (1, -1).", "command_verb": "find"},
   "key": {"form": "numeric", "expr": "3/4"},
   "steps": [
    {"text": "Both sides differentiated.", "expr": "2*x - 2*y - 2*x*dydx + 2*y*dydx = 1", "relation": "new"},
    {"text": "Solved for dy/dx.", "expr": "dydx = (1 - 2*x + 2*y)/(2*y - 2*x)", "relation": "solve", "variable": "dydx"},
    {"text": "At (1, -1).", "expr": "3/4", "relation": "evaluate", "subs": {"x": "1", "y": "-1"}}
   ],
   "calculator_status": "no_calculator",
   "skills": ["BC-SKL-03009"]
  },
  {
   "id": "chk-3",
   "check_kind": "mcq",
   "format": "mcq",
   "bands": ["low"],
   "archetype_id": "BC-QA-03004",
   "parameter_draw": {"mixed": 1, "y_coefficient": 2, "right_slope": 4, "x_at": 2, "y_at": -1, "y_power": 2},
   "stem": {"text": "The curve x^2 + xy + 2y^2 = 4x - 4 passes through (2, -1). What is dy/dx there?", "command_verb": "find"},
   "key": {"form": "numeric", "expr": "-1/2"},
   "steps": [
    {"text": "Both sides differentiated.", "expr": "2*x + y + x*dydx + 4*y*dydx = 4", "relation": "new"},
    {"text": "Solved for dy/dx.", "expr": "dydx = (4 - 2*x - y)/(x + 4*y)", "relation": "solve", "variable": "dydx"},
    {"text": "At (2, -1).", "expr": "-1/2", "relation": "evaluate", "subs": {"x": "2", "y": "-1"}}
   ],
   "options": [
    {"id": "A", "is_key": false, "expr": "5/2", "error_path": "BC-ERR-03007", "derivation": "2y^2 differentiated to 4y with no dy/dx: (4 - 4 + 1 + 4)/2"},
    {"id": "B", "is_key": false, "expr": "-1/4", "error_path": "BC-ERR-03008", "derivation": "xy differentiated to y alone: (4 - 4 + 1)/(-4)"},
    {"id": "C", "is_key": true, "expr": "-1/2", "error_path": null},
    {"id": "D", "is_key": false, "expr": "3/2", "error_path": "BC-ERR-03009", "derivation": "right side derivative dropped: (-4 + 1)/(-2)"}
   ],
   "calculator_status": "no_calculator",
   "skills": ["BC-SKL-03007", "BC-SKL-03008"]
  }
 ],
 "delivery": [
  {"block": "orientation", "mode": "text", "reason": "rule 5: BC-REP-01 only on the skills", "sources": ["BC-SKL-03007"]},
  {"block": "ki-1", "mode": "text", "reason": "rule 5: an algebraic statement about the dy/dx factor, no figure-bearing BC-REP", "sources": ["BC-SKL-03007", "BC-SKL-03008", "BC-SKL-03009"]},
  {"block": "ex-1", "mode": "step_reveal", "reason": "rule 1", "sources": []},
  {"block": "err-BC-ERR-03007", "mode": "step_reveal", "reason": "rule 1", "sources": []},
  {"block": "err-BC-ERR-03008", "mode": "step_reveal", "reason": "rule 1", "sources": []},
  {"block": "err-BC-ERR-03009", "mode": "step_reveal", "reason": "rule 1", "sources": []}
 ],
 "refresher": ["ki-1", "err-BC-ERR-03007", "err-BC-ERR-03008", "err-BC-ERR-03009", "ex-1"],
 "read_minutes": {"full": 3.6, "brief": 3.0},
 "word_count": {"full": 534, "brief": 449},
 "research_lines": [
  {"file": "research/units/unit-03-differentiation-composite-implicit-inverse.md", "line": "A term containing both variables is a product, so the product rule applies and the factor in y still carries dy/dx"}
 ],
 "inferred": [
  {"claim": "The implicit differentiation part takes a share of the 15.0 minute Section II question that no record fixes.", "settles": "A BC-PT mapping for the implicit differentiation parts described in cr-23:22 and cr-24:17."},
  {"claim": "No non-text delivery mode serves this concept better than text and step reveal.", "settles": "The modality A/B in the build plan: skip rate and time to first credited success by mode."}
 ],
 "sources": ["BC-CON-03003", "BC-SKL-03007", "BC-SKL-03008", "BC-SKL-03009", "BC-EK-FUN-3D1", "ced:76", "BC-QA-03004", "BC-MCQ-CED-004", "cr-23:22", "cr-24:17", "BC-ERR-03007", "BC-ERR-03008", "BC-ERR-03009", "BC-MIS-03004", "BC-MIS-03005", "BC-MIS-99011", "BC-PRQ-03005", "research/units/unit-03-differentiation-composite-implicit-inverse.md#3.2 Implicit Differentiation", "research/question-analysis/question-archetypes.md#BC-QA-03004 Implicit differentiation producing or verifying dy/dx", "research/exam/exam-structure.md#Section and part layout"]
}
```
