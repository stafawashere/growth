---
title: LSN-CON-03004 Solving a differentiated relation for dy/dx
research_date: 2026-09-29
status: designed
purpose: Authoring spec for the concept lesson on BC-CON-03004, collecting, factoring and isolating dy/dx after implicit differentiation, built from authoring_bundle("BC-CON-03004") and the research files it cites, so an author fills plan 15's lesson record without making a teaching decision.
---

# LSN-CON-03004 Solving a differentiated relation for dy/dx

Concept BC-CON-03004 (skills BC-SKL-03010, BC-SKL-03011, BC-SKL-03014), topic 3.2 of Unit 3. Two archetypes load its skills, BC-QA-03004 (BC-SKL-03010, 03011, 03014) and BC-QA-03005 (BC-SKL-03011), both in the family implicit-differentiation. Its hard parent concept is BC-CON-03003 (docs/lessons/unit-03/README.md, section 1).

## Orientation

Served text, from BC-CON-03004 `description_plain` and the topic's Assessment behaviour paragraph (research/units/unit-03-differentiation-composite-implicit-inverse.md#3.2 Implicit Differentiation): after both sides are differentiated, a response collects the dy/dx terms, factors dy/dx out and divides, and substitutes both coordinates for a slope. Stems ask to find dy/dx, verify a stated one, or give a slope. No count, no frequency.

## Key ideas

The skills map to one BC-EK, BC-EK-FUN-3D1 (ced:76), so one core block, both bands.

- ki-1 (core). Paraphrase of the Required mathematical knowledge paragraph (Implicit differentiation: the differentiated equation is linear in dy/dx), with the verification and evaluation demands of BC-SKL-03014 and BC-SKL-03011. Anchor quote (9 words) from ced:76, found on the cached page. Notation line from the concept record: dy/dx expressed as a quotient in x and y.

## Recognition

BC-QA-03004 (research/question-analysis/question-archetypes.md#BC-QA-03004 Implicit differentiation producing or verifying dy/dx): `typical_wording` "show that dy/dx is equal to the stated expression for the given curve"; `asked_to_produce` an implicit derivative, a verification, a numerical slope at a point; `common_givens` an equation in x and y, a stated expression for dy/dx, a point on the curve. The signal for this concept: the stem supplies the target expression ("show that") or a point, so the work after differentiating decides the answer. BC-QA-03005 reuses the evaluated dy/dx inside the tangent parts (research/question-analysis/question-archetypes.md#BC-QA-03005 Horizontal or vertical tangent on an implicitly defined curve).

What says "not this concept": a stem that gives dy/dx and asks where the tangent is horizontal or vertical (BC-CON-03005), or asks for the second derivative (BC-CON-03009).

## Method choice

One strategy block, both bands: both archetypes are in one family, so one block, on the primary archetype BC-QA-03004.

- st-1. Cue from `asked_to_produce` and `common_givens`. Method, `expected_solution_path[0]`: differentiate every term of both sides with respect to x. Rival, from `wrong_approaches`: differentiating one side and dropping the right side (BC-ERR-03009). Separating feature: the differentiated line is an equation, so dy/dx is solved for, and its terms are collected before any division (path entries 4 and 5).

## Solution path

- ex-1, BC-QA-03004, both bands, no calculator, the verification variant. Draw from `parameter_spec`: mixed -1, y_coefficient 1, right_slope 2, x_at 2, y_at 1, y_power 3. Curve x^2 - xy + y^3 = 2x - 1 (c = -1, nonzero); y_rate 3, denominator 1; options -1, 2, -1/3, -3, distinct, key nonzero. No published BC-QA-03004 item carries this draw.
- Steps: the differentiated equation (new); collected and factored (equivalent); divided (solve for dydx), which is the stated expression and so the verification; the slope at (2, 1) (evaluate). A fluent solver writes all four: in the FRQ form the collected line is the visible link between the differentiation and the stated result (research/question-analysis/question-archetypes.md#BC-QA-03004 Implicit differentiation producing or verifying dy/dx, scoring pattern).

## Scoring

Neither archetype lists `point_types`, so no what_a_reader_scores entry, no point tag, and the served text names no point beyond the error records' own scoring_consequence. For the author: the Chief Reader reports describe a further point for the algebraic verification or evaluation (research/question-analysis/question-archetypes.md#BC-QA-03004 Implicit differentiation producing or verifying dy/dx), and a variable expression equated to a number is a named notation loss (research/scoring/common-point-losses.md#Notation points, BC-ERR-99002; research/scoring/notation-requirements.md#The equal sign, sg-23:6), which is why ex-1 writes dy/dx at (2, 1), not dy/dx, beside the value.

## Traps

Two active errors meet the skills, in the bundle's order (BC-ERR-03010 then BC-ERR-03011; linked BC-MIS-03006 at severity medium). Both bands serve both.

- err-BC-ERR-03010: dividing by 3y^2 while -x dy/dx is still on the other side. Wrong and right as expressions on ex-1's draw, distinct. No possible reason line: the linked descriptions do not name the order of operations.
- err-BC-ERR-03011: only x = 2 substituted, (y - 2)/(3y^2 - 2), against -1. Distinct. No possible reason line.

## Representations

None. The skills carry BC-REP-01 only.

## Prerequisite bridge

- BC-PRQ-03002 and BC-PRQ-03006, each from its `description_plain` and `failure_signature`.

## Time

BC-QA-03004 is `no_calculator`, the opening part of a multipart FRQ, so Section II Part B, 15.0 minutes per question (research/exam/exam-structure.md#Section and part layout), this part a share of it [inferred, as in BC-CON-03003]. The MCQ form is Part A at 2.14. No step is skipped: the collected line is the step readers look for between the differentiation and the result.

## Checks

- chk-1, completion of ex-1, both bands: the collected line is given, the student divides and evaluates. Key -1.
- chk-2, isomorph, both bands. Draw: mixed 2, y_coefficient -1, right_slope 1, x_at 1, y_at 2, y_power 3; curve x^2 + 2xy - y^3 = x - 4. Key 1/2.
- No chk-3. The bundle holds two error records, and a 4-option MCQ needs three distractors anchored to distinct error blocks [inferred reading of the rule], so the lesson carries 2 checks.

## Delivery

- orientation: text. Rule 5; BC-REP-01 only.
- ki-1: text. Rule 5; an algebraic procedure.
- ex-1: step_reveal. Rule 1.
- err-BC-ERR-03010, err-BC-ERR-03011: step_reveal. Rule 1.

## Band plan

- Low (full) and mid (brief) serve the same blocks: orientation, ki-1, st-1, ex-1, err-BC-ERR-03010, err-BC-ERR-03011, chk-1, chk-2, the two bridges. 414 words, 2.8 minutes in each (caps 900 and 6, 450 and 3).
- Refresher: ki-1, err-BC-ERR-03010, err-BC-ERR-03011, ex-1.

## Sources

- BC-CON-03004; BC-SKL-03010, BC-SKL-03011, BC-SKL-03014; BC-EK-FUN-3D1; ced:76
- BC-QA-03004, BC-QA-03005
- BC-ERR-03010, BC-ERR-03011, BC-ERR-99002; BC-MIS-03006; sg-23:6
- BC-PRQ-03002, BC-PRQ-03006
- research/units/unit-03-differentiation-composite-implicit-inverse.md#3.2 Implicit Differentiation
- research/question-analysis/question-archetypes.md#BC-QA-03004 Implicit differentiation producing or verifying dy/dx
- research/question-analysis/question-archetypes.md#BC-QA-03005 Horizontal or vertical tangent on an implicitly defined curve
- research/scoring/common-point-losses.md#Notation points
- research/scoring/notation-requirements.md#The equal sign
- research/exam/exam-structure.md#Section and part layout
- [inferred] The share of the 15.0 minutes. Settled by a BC-PT mapping for the part.
- [inferred] Two checks only. Settled by a third active error record held by the concept's skills.
- [inferred] Text and step reveal only. Settled by the modality A/B.

## Machine record

```json
{
 "id": "LSN-CON-03004",
 "kind": "concept",
 "target_id": "BC-CON-03004",
 "unit": "03",
 "skills": ["BC-SKL-03010", "BC-SKL-03011", "BC-SKL-03014"],
 "orientation": {
  "text": "After both sides are differentiated, a response collects the dy/dx terms, factors dy/dx out and divides; a slope at a point needs both coordinates. Stems ask to find dy/dx, to show that it equals a stated expression, or for a slope.",
  "sources": ["BC-CON-03004", "research/units/unit-03-differentiation-composite-implicit-inverse.md#3.2 Implicit Differentiation"]
 },
 "key_ideas": [
  {
   "id": "ki-1",
   "ek_id": "BC-EK-FUN-3D1",
   "depth": "core",
   "text": "Implicit differentiation gives an equation linear in dy/dx. Collect every dy/dx term on one side and everything else on the other, factor dy/dx out, then divide by its bracket. The result is a quotient in x and y, so a slope at a point takes both coordinates. Verifying a stated dy/dx means deriving it.",
   "notation": "dy/dx expressed as a quotient in x and y",
   "quote": {"text": "The chain rule is the basis for implicit differentiation.", "source": "ced:76"},
   "sources": ["BC-EK-FUN-3D1", "ced:76", "research/units/unit-03-differentiation-composite-implicit-inverse.md#3.2 Implicit Differentiation"]
  }
 ],
 "strategy": [
  {
   "id": "st-1",
   "archetype_id": "BC-QA-03004",
   "cue": "The stem asks for dy/dx, a verification of a stated dy/dx, or a slope, from an equation in x and y.",
   "method": "First written line: differentiate every term of both sides with respect to x.",
   "rival": "Rival: differentiating one side and dropping the right side (BC-ERR-03009).",
   "separating_feature": "The line is an equation: collect the dy/dx terms, then divide.",
   "sources": ["BC-QA-03004"],
   "evidence_tag": "verified"
  }
 ],
 "worked_examples": [
  {
   "id": "ex-1",
   "archetype_id": "BC-QA-03004",
   "bands": ["low", "mid"],
   "parameter_draw": {"mixed": -1, "y_coefficient": 1, "right_slope": 2, "x_at": 2, "y_at": 1, "y_power": 3},
   "problem": {"text": "For x^2 - xy + y^3 = 2x - 1, show that dy/dx = (2 - 2x + y)/(3y^2 - x). Find dy/dx at (2, 1).", "command_verb": "show"},
   "calculator_status": "no_calculator",
   "steps": [
    {"cue": "Show that: dy/dx is derived, not assumed.", "why": "-xy takes the product rule; y^3 gives 3y^2 dy/dx.", "expr": "2*x - y - x*dydx + 3*y**2*dydx = 2", "relation": "new"},
    {"cue": "dy/dx sits in two terms.", "why": "Collect them before dividing, then factor.", "expr": "dydx*(3*y**2 - x) = 2 - 2*x + y", "relation": "equivalent"},
    {"cue": "One bracket multiplies dy/dx.", "why": "Dividing gives the stated expression: verified.", "expr": "dydx = (2 - 2*x + y)/(3*y**2 - x)", "relation": "solve", "variable": "dydx"},
    {"cue": "The point gives both coordinates.", "why": "(2 - 4 + 1)/(3 - 2).", "expr": "-1", "relation": "evaluate", "subs": {"x": "2", "y": "1"}}
   ],
   "answer": {"form": "numeric", "expr": "-1"}
  }
 ],
 "what_a_reader_scores": [],
 "common_errors": [
  {
   "error_id": "BC-ERR-03010",
   "observed_behavior": "The response divides by a factor while dy/dx still appears on both sides, so the isolated expression is not dy/dx.",
   "scoring_consequence": "The stated expression for dy/dx does not match the verification requested, and later parts built on it are compromised.",
   "wrong_step": {"text": "Divided by 3y^2 with x dy/dx still on the right.", "expr": "(2 - 2*x + y + x*dydx)/(3*y**2)"},
   "right_step": {"text": "Collected first.", "expr": "(2 - 2*x + y)/(3*y**2 - x)"},
   "relation": "distinct",
   "possible_reason": null,
   "sources": ["BC-ERR-03010"]
  },
  {
   "error_id": "BC-ERR-03011",
   "observed_behavior": "The response substitutes the x coordinate into an expression containing both variables and reports a slope still containing y.",
   "scoring_consequence": "No numerical slope is produced, so the evaluation point is lost.",
   "wrong_step": {"text": "Only x = 2 substituted.", "expr": "(y - 2)/(3*y**2 - 2)"},
   "right_step": {"text": "x = 2 and y = 1: -1.", "expr": "-1"},
   "relation": "distinct",
   "possible_reason": null,
   "sources": ["BC-ERR-03011"]
  }
 ],
 "representations": null,
 "prerequisite_bridges": [
  {"prq_id": "BC-PRQ-03002", "text": "Collect the terms in an unknown that appears in several places, factor it out, then divide. Otherwise dy/dx is never isolated, or is divided before collection."},
  {"prq_id": "BC-PRQ-03006", "text": "Combine fractions and cancel factors without changing the value. A wrong simplification after a correct derivative changes the value reported."}
 ],
 "time": {"exam_part": "II-B", "budget_minutes": 15.0, "source": "research/exam/exam-structure.md#Section and part layout", "written_steps": {"ex-1": [1, 2, 3, 4]}, "skipped_steps": {"ex-1": []}},
 "checks": [
  {
   "id": "chk-1",
   "check_kind": "completion",
   "format": "short_answer",
   "bands": ["low", "mid"],
   "archetype_id": "BC-QA-03004",
   "parameter_draw": {"mixed": -1, "y_coefficient": 1, "right_slope": 2, "x_at": 2, "y_at": 1, "y_power": 3},
   "completes": "ex-1",
   "stem": {"text": "Given dy/dx (3y^2 - x) = 2 - 2x + y, find dy/dx at (2, 1).", "command_verb": "find"},
   "key": {"form": "numeric", "expr": "-1"},
   "steps": [
    {"text": "The collected line.", "expr": "dydx*(3*y**2 - x) = 2 - 2*x + y", "relation": "new"},
    {"text": "Divided.", "expr": "dydx = (2 - 2*x + y)/(3*y**2 - x)", "relation": "solve", "variable": "dydx"},
    {"text": "At (2, 1).", "expr": "-1", "relation": "evaluate", "subs": {"x": "2", "y": "1"}}
   ],
   "calculator_status": "no_calculator",
   "skills": ["BC-SKL-03010", "BC-SKL-03011"]
  },
  {
   "id": "chk-2",
   "check_kind": "isomorph",
   "format": "short_answer",
   "bands": ["low", "mid"],
   "archetype_id": "BC-QA-03004",
   "parameter_draw": {"mixed": 2, "y_coefficient": -1, "right_slope": 1, "x_at": 1, "y_at": 2, "y_power": 3},
   "stem": {"text": "For x^2 + 2xy - y^3 = x - 4, find dy/dx at (1, 2).", "command_verb": "find"},
   "key": {"form": "numeric", "expr": "1/2"},
   "steps": [
    {"text": "Both sides differentiated.", "expr": "2*x + 2*y + 2*x*dydx - 3*y**2*dydx = 1", "relation": "new"},
    {"text": "Collected and divided.", "expr": "dydx = (1 - 2*x - 2*y)/(2*x - 3*y**2)", "relation": "solve", "variable": "dydx"},
    {"text": "At (1, 2).", "expr": "1/2", "relation": "evaluate", "subs": {"x": "1", "y": "2"}}
   ],
   "calculator_status": "no_calculator",
   "skills": ["BC-SKL-03010", "BC-SKL-03011"]
  }
 ],
 "delivery": [
  {"block": "orientation", "mode": "text", "reason": "rule 5: BC-REP-01 only on the skills", "sources": ["BC-SKL-03010"]},
  {"block": "ki-1", "mode": "text", "reason": "rule 5: an algebraic procedure with no figure-bearing BC-REP", "sources": ["BC-SKL-03010", "BC-SKL-03011", "BC-SKL-03014"]},
  {"block": "ex-1", "mode": "step_reveal", "reason": "rule 1", "sources": []},
  {"block": "err-BC-ERR-03010", "mode": "step_reveal", "reason": "rule 1", "sources": []},
  {"block": "err-BC-ERR-03011", "mode": "step_reveal", "reason": "rule 1", "sources": []}
 ],
 "refresher": ["ki-1", "err-BC-ERR-03010", "err-BC-ERR-03011", "ex-1"],
 "read_minutes": {"full": 2.8, "brief": 2.8},
 "word_count": {"full": 414, "brief": 414},
 "research_lines": [
  {"file": "research/units/unit-03-differentiation-composite-implicit-inverse.md", "line": "produces an equation that is linear in dy/dx"}
 ],
 "inferred": [
  {"claim": "The implicit differentiation part takes a share of the 15.0 minute Section II question that no record fixes.", "settles": "A BC-PT mapping for the implicit differentiation parts described in cr-23:22 and cr-24:17."},
  {"claim": "The lesson carries two checks because two error records cannot anchor three distinct distractors.", "settles": "A third active error record held by BC-SKL-03010, BC-SKL-03011 or BC-SKL-03014."},
  {"claim": "No non-text delivery mode serves this concept better than text and step reveal.", "settles": "The modality A/B in the build plan: skip rate and time to first credited success by mode."}
 ],
 "sources": ["BC-CON-03004", "BC-SKL-03010", "BC-SKL-03011", "BC-SKL-03014", "BC-EK-FUN-3D1", "ced:76", "BC-QA-03004", "BC-QA-03005", "BC-ERR-03010", "BC-ERR-03011", "BC-ERR-99002", "BC-MIS-03006", "sg-23:6", "BC-PRQ-03002", "BC-PRQ-03006", "research/units/unit-03-differentiation-composite-implicit-inverse.md#3.2 Implicit Differentiation", "research/question-analysis/question-archetypes.md#BC-QA-03004 Implicit differentiation producing or verifying dy/dx", "research/scoring/common-point-losses.md#Notation points", "research/scoring/notation-requirements.md#The equal sign", "research/exam/exam-structure.md#Section and part layout"]
}
```
