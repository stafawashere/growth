---
title: LSN-CON-07001 Differential equation as a relation between a function and its derivatives
research_date: 2026-09-29
status: designed
purpose: Authoring spec for the concept lesson on BC-CON-07001, writing a differential equation and its initial condition from a verbal rate statement, built from authoring_bundle("BC-CON-07001") and the research files it cites, so an author fills plan 15's lesson record without making a teaching decision.
---

# LSN-CON-07001 Differential equation as a relation between a function and its derivatives

Concept BC-CON-07001 (skills BC-SKL-07001 to BC-SKL-07005), topic 7.1 of Unit 7, loaded by one archetype, BC-QA-07006 (family de-modelling). It is first in the unit order and has no hard parent inside Unit 7 (docs/lessons/unit-07/README.md, section 1).

## Orientation

Served text, from BC-CON-07001 `description_plain` and the topic's Assessment behaviour paragraph (research/units/unit-07-differential-equations.md#7.1 Modeling Situations with Differential Equations): a response turns the rate sentence into an equation for the derivative with a named constant, and writes the stated starting value as a separate initial condition. No count, no frequency.

## Key ideas

All five skills map to BC-EK-FUN-7A1 (ced:137), so one core block, both bands.

- ki-1 (core). Paraphrase of the Required mathematical knowledge paragraph (Definition, Translation rules, Variables and units, Initial condition): the equation relates the function to its first derivative; "proportional to" gives a constant multiple, of the quantity or of a difference from a fixed level; the derivative carries quantity units over time units; the stated value is a separate condition. Anchor quote from ced:137, 13 words. Notation line from the concept record.

## Recognition

BC-QA-07006 (research/question-analysis/question-archetypes.md#BC-QA-07006 Differential equation written from a verbal rate statement): `typical_wording` "write a differential equation that models the described rate of change, and state the initial condition"; `common_givens` a verbal description of a rate and a value of the quantity at a stated input; `asked_to_produce` the differential equation, the initial condition, the meaning of each variable. The signal: the words "rate" and "proportional to" in a sentence, with no equation printed. Shapes: an MCQ that offers four equations for one sentence (BC-MCQ-PE2012-023), or the unscored opening of a free-response question, where the equation is usually supplied and the scored work starts at the field or the separation (research/units/unit-07-differential-equations.md#7.1 Modeling Situations with Differential Equations).

What says "not this concept": an equation already printed with a request to solve it (BC-CON-07007), or "jointly proportional to the quantity and the difference", which is the logistic form (BC-CON-07011; docs/lessons/unit-07/README.md, section 3).

## Method choice

One strategy block, both bands.

- st-1, BC-QA-07006. Cue from `asked_to_produce` and `common_givens`. Method, `expected_solution_path[0]`: name the dependent and independent variables, then write the derivative equal to a constant times the named expression. Rival, `wrong_approaches`: writing an exponential formula instead of the equation (BC-ERR-07005). Separating feature: the stem asks for the rate, so the left side is the derivative. The archetype carries both fields, so the block is not tagged inferred.

## Solution path

- ex-1, BC-QA-07006, both bands. Draw from `parameter_spec`: context temperature, level 70, gap 25, approach from_above, time_unit minutes, so the derived initial value is 95. No published BC-QA-07006 item carries this draw (content/items_gen_unit07 and content/items_unit07_agent searched).
- Steps follow `expected_solution_path`: variables named (no value); the proportional expression (new); the equation (new); the initial condition (new). A fluent solver writes the equation and the condition; naming the variables is one clause.
- The answer is a statement (an equation and a condition), so the lesson records it with form statement.

## Scoring

BC-QA-07006 lists no `point_types`, so no what_a_reader_scores entry and no point tag; the served text names no point beyond the error records' scoring_consequence. For the author: the archetype's `scoring_pattern` treats this as the setup stage of the separable family (sg-23:12).

## Traps

Six active errors meet the skills; the first four in the bundle's order are served: BC-ERR-07001, BC-ERR-07002, BC-ERR-07003, BC-ERR-07004. Low band all four; mid band the first two. All on ex-1's draw.

- err-BC-ERR-07001: the rate set equal to 70 - H with no k. Possible reason, words from BC-MIS-07001.
- err-BC-ERR-07002: k(H - 70), so the model moves away from 70. No possible reason: neither linked description names the orientation of the difference.
- err-BC-ERR-07003: letters y and x never given meanings. No possible reason: the linked descriptions describe other slips.
- err-BC-ERR-07004: 95 put inside the equation. Possible reason, words from BC-MIS-07003.

BC-ERR-07005 and BC-ERR-99035 exceed the cap of four.

## Representations

None. The topic's Representations paragraph names BC-REP-04, BC-REP-05 and BC-REP-06, none figure-shaped.

## Prerequisite bridge

- BC-PRQ-06005, BC-PRQ-07002, BC-PRQ-07003, each from its `description_plain` and `failure_signature`.

## Time

BC-QA-07006 is `either` and its `multipart_structure` names a single MCQ first, so Section I Part A, 2.14 minutes (research/exam/exam-structure.md#Section and part layout) [inferred: an either archetype placed in I-A]. The minutes go on the orientation of the difference; the constant and the separate condition are written without deliberation.

## Checks

- chk-1, completion of ex-1, both bands: the variables are named; the student writes the equation and the condition. Key the same statement as ex-1.
- chk-2, isomorph, both bands. Draw: concentration, level 40, gap 15, from_below, minutes. Key dC/dt = k(40 - C).
- chk-3, MCQ, low band. Draw: price, level 50, gap 10, from_above, hours. Key dP/dt = k(50 - P). Distractors: dP/dt = 50 - P (BC-ERR-07001), dP/dt = k(P - 50) (BC-ERR-07002), dP/dt = k(50 - 60) (BC-ERR-07004).

## Delivery

- orientation, ki-1: text. Rule 6: BC-REP-04, 05, 06 on BC-SKL-07001 to 07005, none figure-bearing (docs/lessons/unit-07/README.md, section 6).
- ex-1 and the four error blocks: step_reveal. Rule 1.

## Band plan

- Low (full): orientation, ki-1, st-1, ex-1, the four error blocks, chk-1 to chk-3, the three bridges. 575 words, 4.0 minutes (cap 900 and 6).
- Mid (brief): orientation, ki-1, st-1, ex-1, err-BC-ERR-07001, err-BC-ERR-07002, chk-1, chk-2, the bridges. 446 words, 3.0 minutes (cap 450 and 3).
- Refresher: ki-1, the four error blocks, ex-1.

## Sources

- BC-CON-07001; BC-SKL-07001 to BC-SKL-07005; BC-EK-FUN-7A1; ced:137
- BC-QA-07006; BC-MCQ-PE2012-023; sg-23:12
- BC-ERR-07001, BC-ERR-07002, BC-ERR-07003, BC-ERR-07004; BC-MIS-07001, BC-MIS-07003
- BC-PRQ-06005, BC-PRQ-07002, BC-PRQ-07003
- research/units/unit-07-differential-equations.md#7.1 Modeling Situations with Differential Equations
- research/question-analysis/question-archetypes.md#BC-QA-07006 Differential equation written from a verbal rate statement
- research/exam/exam-structure.md#Section and part layout
- [inferred] I-A for an either archetype. Settled by a calculator_status fixed on BC-QA-07006.

## Machine record

```json
{
 "id": "LSN-CON-07001",
 "kind": "concept",
 "target_id": "BC-CON-07001",
 "unit": "07",
 "skills": ["BC-SKL-07001", "BC-SKL-07002", "BC-SKL-07003", "BC-SKL-07004", "BC-SKL-07005"],
 "orientation": {
  "text": "A rate sentence becomes an equation for the derivative: the derivative equals a named constant times the quantity or the stated difference. The value given at a stated time is written apart, as the initial condition.",
  "sources": ["BC-CON-07001", "research/units/unit-07-differential-equations.md#7.1 Modeling Situations with Differential Equations"]
 },
 "key_ideas": [
  {
   "id": "ki-1",
   "ek_id": "BC-EK-FUN-7A1",
   "depth": "core",
   "text": "The equation ties a function to its first derivative. Proportional to the quantity gives k times the quantity; proportional to the difference from a fixed level gives k times that difference, oriented so the quantity moves toward the level. The derivative carries units of the quantity per unit of time. A value at a stated time is the initial condition, kept outside the equation.",
   "notation": "dy/dt; k for the constant of proportionality",
   "quote": {"text": "Differential equations relate a function of an independent variable and the function's derivatives.", "source": "ced:137"},
   "sources": ["BC-EK-FUN-7A1", "ced:137", "research/units/unit-07-differential-equations.md#7.1 Modeling Situations with Differential Equations"]
  }
 ],
 "strategy": [
  {
   "id": "st-1",
   "archetype_id": "BC-QA-07006",
   "cue": "A sentence says a rate is proportional to something and gives a value at one time; no equation is printed.",
   "method": "First line: name the variables, then write the derivative equal to k times the named expression.",
   "rival": "Rival: an exponential formula for the quantity (BC-ERR-07005).",
   "separating_feature": "The stem asks for the rate, so the left side is a derivative.",
   "sources": ["BC-QA-07006"],
   "evidence_tag": "verified"
  }
 ],
 "worked_examples": [
  {
   "id": "ex-1",
   "archetype_id": "BC-QA-07006",
   "bands": ["low", "mid"],
   "parameter_draw": {"context": "temperature", "level": 70, "gap": 25, "approach": "from_above", "time_unit": "minutes"},
   "problem": {"text": "Tea is 95 degrees at time t = 0 minutes. Its temperature changes at a rate proportional to the difference between 70 degrees and its temperature, with positive constant k. Write the differential equation and the initial condition.", "command_verb": "write"},
   "calculator_status": "no_calculator",
   "steps": [
    {"cue": "The stem names a temperature and a time.", "why": "H in degrees, t in minutes; dH/dt in degrees per minute."},
    {"cue": "Proportional to the difference selects k times that difference.", "why": "70 - H is negative above 70, so H falls toward 70.", "expr": "k*(70 - H)", "relation": "new"},
    {"cue": "The rate is the derivative of H.", "why": "An equation about the rate, not a formula for H.", "expr": "dH/dt = k*(70 - H)", "relation": "new"},
    {"cue": "At time t = 0 marks a stated value.", "why": "It selects one solution, so it stands apart.", "expr": "H(0) = 95", "relation": "new"}
   ],
   "answer": {"form": "statement", "expr": "dH/dt = k*(70 - H) with H(0) = 95"}
  }
 ],
 "what_a_reader_scores": [],
 "common_errors": [
  {
   "error_id": "BC-ERR-07001",
   "observed_behavior": "The response writes the derivative equal to the quantity itself, with no constant of proportionality.",
   "scoring_consequence": "The model is wrong by a factor and every later value built on it is wrong.",
   "wrong_step": {"text": "No constant.", "expr": "dH/dt = 70 - H"},
   "right_step": {"text": "k written.", "expr": "dH/dt = k*(70 - H)"},
   "relation": "distinct",
   "possible_reason": {"misconception_id": "BC-MIS-07001", "text": "drops the constant of proportionality"},
   "sources": ["BC-ERR-07001", "BC-MIS-07001"]
  },
  {
   "error_id": "BC-ERR-07002",
   "observed_behavior": "The response writes the difference the other way round, so the modelled quantity moves away from the fixed level instead of toward it.",
   "scoring_consequence": "The sign of the solution's approach is wrong, and the slope field and the particular solution both follow it.",
   "wrong_step": {"text": "H - 70.", "expr": "dH/dt = k*(H - 70)"},
   "right_step": {"text": "70 - H.", "expr": "dH/dt = k*(70 - H)"},
   "relation": "distinct",
   "possible_reason": null,
   "sources": ["BC-ERR-07002"]
  },
  {
   "error_id": "BC-ERR-07003",
   "observed_behavior": "The equation is written in letters that are never given meanings or units.",
   "scoring_consequence": "An interpretation point that requires the quantity and its units is lost.",
   "wrong_step": {"text": "Unnamed y and x.", "expr": "dy/dx = k*(70 - y)"},
   "right_step": {"text": "H degrees, t minutes.", "expr": "dH/dt = k*(70 - H)"},
   "relation": "distinct",
   "possible_reason": null,
   "sources": ["BC-ERR-07003"]
  },
  {
   "error_id": "BC-ERR-07004",
   "observed_behavior": "The response writes the stated value as part of the equation rather than as a separate condition.",
   "scoring_consequence": "The equation is not the model asked for and the constant of integration has nothing to be fixed by.",
   "wrong_step": {"text": "95 inside the equation.", "expr": "dH/dt = k*(70 - 95)"},
   "right_step": {"text": "95 as the condition.", "expr": "H(0) = 95"},
   "relation": "distinct",
   "possible_reason": {"misconception_id": "BC-MIS-07003", "text": "treats the stated value as a term of the equation rather than as the condition that selects one solution"},
   "sources": ["BC-ERR-07004", "BC-MIS-07003"]
  }
 ],
 "representations": null,
 "prerequisite_bridges": [
  {"prq_id": "BC-PRQ-06005", "text": "H(0) means the value of H at input 0, not H times 0; misreading it pulls a value for the wrong input."},
  {"prq_id": "BC-PRQ-07002", "text": "dH/dt is the derivative of H with respect to t; its letters name which quantity changes and against what."},
  {"prq_id": "BC-PRQ-07003", "text": "Proportional to means a constant multiple; an equality in place of the multiple, or no constant, changes the model."}
 ],
 "time": {"exam_part": "I-A", "budget_minutes": 2.14, "source": "research/exam/exam-structure.md#Section and part layout", "written_steps": {"ex-1": [3, 4]}, "skipped_steps": {"ex-1": [1, 2]}},
 "checks": [
  {
   "id": "chk-1",
   "check_kind": "completion",
   "format": "short_answer",
   "bands": ["low", "mid"],
   "archetype_id": "BC-QA-07006",
   "parameter_draw": {"context": "temperature", "level": 70, "gap": 25, "approach": "from_above", "time_unit": "minutes"},
   "completes": "ex-1",
   "stem": {"text": "Tea: H degrees at t minutes, 95 at t = 0, rate proportional to 70 - H with constant k. Write the equation and the condition.", "command_verb": "write"},
   "key": {"form": "statement", "expr": "dH/dt = k*(70 - H) with H(0) = 95"},
   "steps": [
    {"text": "The equation.", "expr": "dH/dt = k*(70 - H)", "relation": "new"},
    {"text": "The condition.", "expr": "H(0) = 95", "relation": "new"}
   ],
   "calculator_status": "no_calculator",
   "skills": ["BC-SKL-07002", "BC-SKL-07004"]
  },
  {
   "id": "chk-2",
   "check_kind": "isomorph",
   "format": "short_answer",
   "bands": ["low", "mid"],
   "archetype_id": "BC-QA-07006",
   "parameter_draw": {"context": "concentration", "level": 40, "gap": 15, "approach": "from_below", "time_unit": "minutes"},
   "stem": {"text": "A concentration C, 25 at t = 0 minutes, changes at a rate proportional to 40 minus C, constant k. Write the differential equation.", "command_verb": "write"},
   "key": {"form": "symbolic", "expr": "dC/dt = k*(40 - C)"},
   "steps": [
    {"text": "k times the difference.", "expr": "k*(40 - C)", "relation": "new"},
    {"text": "The derivative equals it.", "expr": "dC/dt = k*(40 - C)", "relation": "new"}
   ],
   "calculator_status": "no_calculator",
   "skills": ["BC-SKL-07002"]
  },
  {
   "id": "chk-3",
   "check_kind": "mcq",
   "format": "mcq",
   "bands": ["low"],
   "archetype_id": "BC-QA-07006",
   "parameter_draw": {"context": "price", "level": 50, "gap": 10, "approach": "from_above", "time_unit": "hours"},
   "stem": {"text": "A price P is 60 at t = 0 hours and changes at a rate proportional to 50 minus P. Which models it, k > 0?", "command_verb": "identify"},
   "key": {"form": "symbolic", "expr": "dP/dt = k*(50 - P)"},
   "steps": [
    {"text": "k times the difference.", "expr": "k*(50 - P)", "relation": "new"},
    {"text": "The derivative equals it.", "expr": "dP/dt = k*(50 - P)", "relation": "new"}
   ],
   "options": [
    {"id": "A", "is_key": false, "expr": "dP/dt = 50 - P", "error_path": "BC-ERR-07001", "derivation": "the constant of proportionality dropped"},
    {"id": "B", "is_key": false, "expr": "dP/dt = k*(P - 50)", "error_path": "BC-ERR-07002", "derivation": "the difference reversed"},
    {"id": "C", "is_key": true, "expr": "dP/dt = k*(50 - P)", "error_path": null},
    {"id": "D", "is_key": false, "expr": "dP/dt = k*(50 - 60)", "error_path": "BC-ERR-07004", "derivation": "the starting value 60 put into the equation"}
   ],
   "calculator_status": "no_calculator",
   "skills": ["BC-SKL-07002"]
  }
 ],
 "delivery": [
  {"block": "orientation", "mode": "text", "reason": "rule 6: BC-REP-04, 05, 06 on BC-SKL-07001 to 07005, none figure-bearing", "sources": ["BC-SKL-07001"]},
  {"block": "ki-1", "mode": "text", "reason": "rule 6: a translation rule with no figure-bearing representation", "sources": ["BC-SKL-07001", "BC-SKL-07002"]},
  {"block": "ex-1", "mode": "step_reveal", "reason": "rule 1", "sources": []},
  {"block": "err-BC-ERR-07001", "mode": "step_reveal", "reason": "rule 1", "sources": []},
  {"block": "err-BC-ERR-07002", "mode": "step_reveal", "reason": "rule 1", "sources": []},
  {"block": "err-BC-ERR-07003", "mode": "step_reveal", "reason": "rule 1", "sources": []},
  {"block": "err-BC-ERR-07004", "mode": "step_reveal", "reason": "rule 1", "sources": []}
 ],
 "refresher": ["ki-1", "err-BC-ERR-07001", "err-BC-ERR-07002", "err-BC-ERR-07003", "err-BC-ERR-07004", "ex-1"],
 "read_minutes": {"full": 4.0, "brief": 3.0},
 "word_count": {"full": 0, "brief": 0},
 "research_lines": [
  {"file": "research/units/unit-07-differential-equations.md", "line": "A statement of the value of the quantity at a stated input is the initial condition and is separate from the differential equation itself."}
 ],
 "inferred": [
  {"claim": "BC-QA-07006 is either calculator status; the lesson places it in Section I Part A.", "settles": "A calculator_status fixed on BC-QA-07006, or an official item of this shape in a calculator part."}
 ],
 "sources": ["BC-CON-07001", "BC-SKL-07001", "BC-SKL-07002", "BC-SKL-07003", "BC-SKL-07004", "BC-SKL-07005", "BC-EK-FUN-7A1", "ced:137", "BC-QA-07006", "BC-MCQ-PE2012-023", "sg-23:12", "BC-ERR-07001", "BC-ERR-07002", "BC-ERR-07003", "BC-ERR-07004", "BC-MIS-07001", "BC-MIS-07003", "BC-PRQ-06005", "BC-PRQ-07002", "BC-PRQ-07003", "research/units/unit-07-differential-equations.md#7.1 Modeling Situations with Differential Equations", "research/question-analysis/question-archetypes.md#BC-QA-07006 Differential equation written from a verbal rate statement", "research/exam/exam-structure.md#Section and part layout"]
}
```
