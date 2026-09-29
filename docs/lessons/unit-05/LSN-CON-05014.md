---
title: LSN-CON-05014 Interpretation of an optimal value in context
research_date: 2026-09-29
status: designed
purpose: Authoring spec for the concept lesson on BC-CON-05014, reporting an optimal value as a statement about the situation with its units and the input where it occurs, after comparing it with the endpoints, built from authoring_bundle("BC-CON-05014") and the research files it cites, so an author fills plan 15's lesson record without making a teaching decision.
---

# LSN-CON-05014 Interpretation of an optimal value in context

Concept BC-CON-05014 (skills BC-SKL-05054 to BC-SKL-05057), topic 5.11 of Unit 5. One archetype loads its skills, BC-QA-05011 (family optimisation, tagged [inferred] in research). Unit parents BC-CON-05006 and 05013 (docs/lessons/unit-05/README.md, section 1).

## Prediction

pr-1, `mcq`, both bands, served first, on ex-1's draw. Stem: the planter's volume is largest, 1600, at x = 4 on 0 <= x <= 9; which sentence states the largest volume with correct units. Key: the volume is largest, 1600 cubic centimeters, at a 4 cm cut. Distractors: the input alone (BC-ERR-05024) and the bare number with no units and no quantity (BC-ERR-05055, BC-ERR-05056). The resolution states what an interpretation names, in the record's words, and says nothing about the student. Sources: BC-CON-05014 and the topic's 5.11 section (research/units/unit-05-analytical-applications-differentiation.md#5.11 Solving Optimization Problems). Tagged [inferred] in the record's `inferred` array.

## Orientation

Served text, from BC-CON-05014 `description_plain` and the topic's Assessment behaviour paragraph (research/units/unit-05-analytical-applications-differentiation.md#5.11 Solving Optimization Problems): a response compares the interior candidate with the endpoints, returns the quantity asked for (value or input), and states it with units and the input where it occurs. No count, no frequency.

## Key ideas

All four skills map to BC-EK-FUN-4C1 (ced:109): one core block, both bands.

- ki-1 (core). Paraphrase of Interpretation, Completeness of an interpretation and Value against location: the optimal value and its input both carry units and meaning; the quantity, units and input are named together (sg-23:2 per the topic paragraph); "largest volume" asks for the volume, "dimensions" for the input. Anchor quote from ced:109, 14 words.

## Recognition

BC-QA-05011 (research/question-analysis/question-archetypes.md#BC-QA-05011 Applied optimisation with model setup, domain, and verification): `typical_wording` "using correct units, state the largest value the modelled quantity attains on the stated interval"; `asked_to_produce` the verification and the interpreted value; `common_givens` a contextual range. The signal: "using correct units", "largest value", "what does it mean". Shape: an MCQ asking what the value means, or the interpretation sentence inside an FRQ, scored apart from the computation; no `official_examples` in the record.

What says "not this concept": "find the dimensions" (the input, BC-CON-05013), or no context.
The contrast pair on st-1 comes from the paragraph above. `this` asks for the largest volume with correct units. `not_this` is a bare function with no context asking for its absolute maximum value, a BC-QA-05006 `typical_wording` stem from outside this archetype (BC-CON-05006), the "no context" case the line above names: \(h'(x)=6-2x\) is zero at 3, and h(0) = 0, h(3) = 9, h(5) = 5, so the value is 9 with no units (SymPy). `feature` is whether the value sits in a context that gives it units.

## Method choice

One strategy block, both bands.

- st-1, BC-QA-05011. Method, `expected_solution_path[0]`: define the variables and write the objective, so every letter carries its units into the last line. Rival, `wrong_approaches`: substituting a numerical value before differentiating. Separating feature: the last line answers the asked quantity, value or input, with units. Tagged inferred (the archetype record is inferred).
The strategy fields carry no leading label, because the reader prints Cue, First line, Rival and Separating feature itself. st-1 carries the contrast pair described under Recognition. The fields, the orientation and the key idea are cut to fit the brief cap once the prediction and the contrast are served; the key idea keeps its anchor quote.

## Solution path

- ex-1, BC-QA-05011, both bands, no calculator. Draw: scale 2, height_cap 1, sheet_shape strip, material cardboard, purpose planter, length_unit centimeters, domain_limit none. The notes give an 18 by 48 sheet, V(x) = x(18 - 2x)(48 - 2x), critical points 4 and 18, optimum 4; the domain is 0 to 9. No published BC-QA-05011 item carries this draw.
- Steps: objective (new); V(4) = 1600 (evaluate); endpoints compared (no value); the interpretation sentence (no value). A fluent solver writes all four.

## Scoring

BC-QA-05011 lists no `point_types`, so no what_a_reader_scores entry and no point tag. For the author: an interpretation names the quantity and the interval (research/scoring/common-point-losses.md#Interpretation points), and units are scored apart from the value (research/scoring/common-point-losses.md#Units points).

## Traps

Four active errors, in the bundle's order: BC-ERR-05026, BC-ERR-05055, BC-ERR-05024, BC-ERR-05056. Low band all four; mid band the first two. All on ex-1's draw.

- err-BC-ERR-05026: only x = 4 considered. Statement-shaped. Possible reason, words from BC-MIS-05016.
- err-BC-ERR-05055: 1600 with no units. Possible reason, words from BC-MIS-07023.
- err-BC-ERR-05024: 4 reported where the volume was asked. Possible reason, words from BC-MIS-05015.
- err-BC-ERR-05056: "the maximum is 1600". Statement-shaped. Possible reason, words from BC-MIS-07023.
All four blocks have `relation` distinct, so all four carry `fix_prompt` true: the student writes the right step before it is shown.

## Representations

None. The topic's Representations paragraph names verbal and contextual conversions only.

## Prerequisite bridge

None.

## Time

BC-QA-05011 is `either`, so Section I Part A, 2.14 minutes per question (research/exam/exam-structure.md#Section and part layout) [inferred]. The minutes go on the three evaluations; the sentence is one line.

## Checks

- chk-1, completion of ex-1, both bands. Key 1600.
- chk-2, isomorph, both bands. Draw: scale 5, height_cap 3, sheet_shape square, material plastic, purpose storage bin, length_unit inches, domain_limit none. V(x) = x(30 - 2x)^2 on 0 to 15. Key 2000.
- chk-3, MCQ, low band. Draw: scale 3, height_cap 2, sheet_shape rectangle, material tin, purpose tray, length_unit centimeters, domain_limit binding; height at most 2 cm, so the domain is 0 to 2 and V rises on it. Key 440 cubic centimeters. Distractors: 486 cubic centimeters at the excluded interior point (BC-ERR-05026), 440 with no units (BC-ERR-05055), 2 centimeters (BC-ERR-05024).

## Delivery

- orientation, ki-1: text. Rule 6: BC-SKL-05054 to 05057 carry BC-REP-01, 04, 05 only (docs/lessons/unit-05/README.md, section 6).
- ex-1 and the four error blocks: step_reveal. Rule 1.
- pr-1: text. Rule 6. Figure presence: no drawn block fits, and the record carries `no_figure_reason`: no skill carries a figure-bearing representation, the key ideas describe no process, and no BC-REP-03 givens appear, so rules 2 to 5 select nothing.

## Band plan
- Low (full): pr-1, orientation, ki-1, st-1 with its contrast pair, ex-1, chk-1, the four error blocks, chk-2, chk-3. 571 words, 4.0 minutes (cap 900 and 6).
- Mid (brief): pr-1, orientation, ki-1, st-1 with its contrast pair, ex-1, chk-1, err-BC-ERR-05026, err-BC-ERR-05055, chk-2. 430 words, 3.0 minutes (cap 450 and 3).
- Refresher: ki-1, the four error blocks, ex-1. No prediction and no check.

## Sources

- BC-CON-05014; BC-SKL-05054, BC-SKL-05055, BC-SKL-05056, BC-SKL-05057; BC-EK-FUN-4C1; ced:109
- BC-QA-05011; sg-23:2
- BC-QA-05006, BC-CON-05006 (the not-this stem of the contrast pair); research/question-analysis/question-archetypes.md#BC-QA-05006 Absolute extremum by the candidates test with a global justification
- BC-ERR-05026, BC-ERR-05055, BC-ERR-05024, BC-ERR-05056; BC-MIS-05016, BC-MIS-07023, BC-MIS-05015
- research/units/unit-05-analytical-applications-differentiation.md#5.11 Solving Optimization Problems
- research/question-analysis/question-archetypes.md#BC-QA-05011 Applied optimisation with model setup, domain, and verification
- research/scoring/common-point-losses.md#Interpretation points
- research/scoring/common-point-losses.md#Units points
- research/exam/exam-structure.md#Section and part layout
- [inferred] Section I Part A for an either archetype. Settled by a calculator status on BC-QA-05011.
- [inferred] Units written as the symbols cm and inch in the SymPy strings. Settled by a units convention for keys in plan 15.
- [inferred] The prediction and the contrast stems, authored on ex-1's draw. Settled by the blind re-solve and a pretest measurement.

## Machine record

```json
{
 "id": "LSN-CON-05014",
 "kind": "concept",
 "target_id": "BC-CON-05014",
 "unit": "05",
 "skills": ["BC-SKL-05054", "BC-SKL-05055", "BC-SKL-05056", "BC-SKL-05057"],
 "prediction": {"id": "pr-1", "stem": {"text": "A planter's volume is largest, 1600, at \\(x=4\\) on \\(0\\le x\\le 9\\). Which sentence states the largest volume with correct units?", "command_verb": "predict"}, "format": "mcq", "options": [{"id": "A", "label": "The largest volume occurs at a cut of 4 cm.", "is_key": false}, {"id": "B", "label": "The maximum is 1600.", "is_key": false}, {"id": "C", "label": "The volume is largest, 1600 cubic centimeters, at a 4 cm cut.", "is_key": true}], "resolution": "An interpretation names the quantity asked for, its units and where it occurs: the volume is 1600 cubic centimeters when the cut is 4 cm. A bare number, or the input alone, leaves part unstated.", "sources": ["BC-CON-05014", "research/units/unit-05-analytical-applications-differentiation.md#5.11 Solving Optimization Problems"]},
 "orientation": {"text": "A response compares the candidate with the ends and states the asked quantity with its units and input.", "sources": ["BC-CON-05014", "research/units/unit-05-analytical-applications-differentiation.md#5.11 Solving Optimization Problems"]},
 "key_ideas": [
  {"id": "ki-1", "ek_id": "BC-EK-FUN-4C1", "depth": "core", "text": "The optimal value and its input both carry units. An interpretation names the quantity, units and input together. Largest volume asks for the volume; dimensions ask for the input.", "notation": "units; optimal value", "quote": {"text": "Minimum and maximum values of a function take on specific meanings in applied contexts.", "source": "ced:109"}, "sources": ["BC-EK-FUN-4C1", "ced:109", "sg-23:2", "research/units/unit-05-analytical-applications-differentiation.md#5.11 Solving Optimization Problems"]}
 ],
 "strategy": [
  {"id": "st-1", "archetype_id": "BC-QA-05011", "cue": "Correct units, on a contextual range.", "method": "Define the variables and write the objective, each letter with its units.", "rival": "Substituting a number before differentiating.", "separating_feature": "The last line answers the asked quantity, with units.", "sources": ["BC-QA-05011"], "evidence_tag": "inferred", "contrast": {"this": {"text": "A 30 by 30 cm sheet with corner cuts of side \\(x\\) cm makes a tray. State the largest volume, with units.", "archetype_id": "BC-QA-05011"}, "not_this": {"text": "\\(h(x)=6x-x^2\\) on \\([0,5]\\). Find the absolute maximum value of \\(h\\).", "why_not": "No context, so the value carries no units."}, "feature": "A value in context with units, or a bare value."}}
 ],
 "worked_examples": [
  {"id": "ex-1", "archetype_id": "BC-QA-05011", "bands": ["low", "mid"], "parameter_draw": {"scale": 2, "height_cap": 1, "sheet_shape": "strip", "material": "cardboard", "purpose": "planter", "length_unit": "centimeters", "domain_limit": "none"}, "problem": {"text": "A planter is folded from an 18 by 48 cm sheet after cutting corner squares of side \\(x\\) cm, \\(0\\le x\\le 9\\). The only critical point inside is \\(x=4\\). Using correct units, state the largest volume.", "command_verb": "state"}, "calculator_status": "no_calculator", "steps": [{"cue": "Volume in cubic centimeters, from the cut \\(x\\).", "why": "\\(V(x)=x(18-2x)(48-2x)\\).", "expr": "x*(18 - 2*x)*(48 - 2*x)", "relation": "new"}, {"cue": "Interior candidate \\(x=4\\).", "why": "\\(4\\cdot10\\cdot40\\).", "expr": "1600", "relation": "evaluate", "subs": {"x": "4"}}, {"cue": "Closed range: the ends compete.", "why": "\\(V(0)=V(9)=0<1600\\)."}, {"cue": "The stem asks for the volume, with units.", "why": "The largest volume is 1600 cubic centimeters, when the cut is 4 cm."}], "answer": {"form": "numeric", "expr": "1600"}}
 ],
 "what_a_reader_scores": [],
 "common_errors": [
  {"error_id": "BC-ERR-05026", "observed_behavior": "The response compares values only at the interior critical points and never evaluates at the ends of the interval.", "scoring_consequence": "The justification point is lost; the 2023 guideline states that a response not considering both endpoints does not earn it.", "wrong_step": {"text": "\\(V'(4)=0\\), so 1600 is the largest.", "expr": "interior_only"}, "right_step": {"text": "\\(V(0)=0\\), \\(V(4)=1600\\), \\(V(9)=0\\).", "expr": "interior_and_both_ends"}, "relation": "distinct", "possible_reason": {"misconception_id": "BC-MIS-05016", "text": "does not regard the endpoints as competitors"}, "sources": ["BC-ERR-05026", "BC-MIS-05016"], "fix_prompt": true},
  {"error_id": "BC-ERR-05055", "observed_behavior": "The response gives a number for the optimal value and never names its units.", "scoring_consequence": "An interpretation point that requires units is lost.", "wrong_step": {"text": "1600.", "expr": "1600"}, "right_step": {"text": "1600 cubic centimeters.", "expr": "1600*cm**3"}, "relation": "distinct", "possible_reason": {"misconception_id": "BC-MIS-07023", "text": "leaves the quantity, the units, and the direction implicit"}, "sources": ["BC-ERR-05055", "BC-MIS-07023"], "fix_prompt": true},
  {"error_id": "BC-ERR-05024", "observed_behavior": "The response names the input at which the extremum occurs when the question asked for the extreme value, or the reverse.", "scoring_consequence": "The answer point is lost; the 2023 guideline awarded it only for the minimum value, not for the input.", "wrong_step": {"text": "The largest volume is at 4 cm.", "expr": "4*cm"}, "right_step": {"text": "The largest volume is 1600 cubic centimeters.", "expr": "1600*cm**3"}, "relation": "distinct", "possible_reason": {"misconception_id": "BC-MIS-05015", "text": "does not separate the input at which the extremum occurs from the extreme value itself"}, "sources": ["BC-ERR-05024", "BC-MIS-05015"], "fix_prompt": true},
  {"error_id": "BC-ERR-05056", "observed_behavior": "The interpretation sentence names a number without saying what it measures or when it is attained.", "scoring_consequence": "The interpretation point is lost because the sentence is incomplete.", "wrong_step": {"text": "The maximum is 1600.", "expr": "number_only_sentence"}, "right_step": {"text": "The planter's volume is largest, 1600 cubic centimeters, when the cut is 4 cm.", "expr": "quantity_units_and_input_named"}, "relation": "distinct", "possible_reason": {"misconception_id": "BC-MIS-07023", "text": "reports the number and leaves the quantity, the units, and the direction implicit"}, "sources": ["BC-ERR-05056", "BC-MIS-07023"], "fix_prompt": true}
 ],
 "representations": null,
 "prerequisite_bridges": [],
 "time": {"exam_part": "I-A", "budget_minutes": 2.14, "source": "research/exam/exam-structure.md#Section and part layout", "written_steps": {"ex-1": [1, 2, 3, 4]}, "skipped_steps": {"ex-1": []}},
 "checks": [
  {"id": "chk-1", "check_kind": "completion", "format": "short_answer", "bands": ["low", "mid"], "archetype_id": "BC-QA-05011", "parameter_draw": {"scale": 2, "height_cap": 1, "sheet_shape": "strip", "material": "cardboard", "purpose": "planter", "length_unit": "centimeters", "domain_limit": "none"}, "completes": "ex-1", "stem": {"text": "\\(V(x)=x(18-2x)(48-2x)\\) on \\(0\\le x\\le 9\\), critical point 4. Give the largest volume in cubic centimeters.", "command_verb": "state"}, "key": {"form": "numeric", "expr": "1600"}, "steps": [{"text": "The objective.", "expr": "x*(18 - 2*x)*(48 - 2*x)", "relation": "new"}, {"text": "\\(V(4)=1600\\); the ends give 0.", "expr": "1600", "relation": "evaluate", "subs": {"x": "4"}}], "calculator_status": "no_calculator", "skills": ["BC-SKL-05054"]},
  {"id": "chk-2", "check_kind": "isomorph", "format": "short_answer", "bands": ["low", "mid"], "archetype_id": "BC-QA-05011", "parameter_draw": {"scale": 5, "height_cap": 3, "sheet_shape": "square", "material": "plastic", "purpose": "storage bin", "length_unit": "inches", "domain_limit": "none"}, "stem": {"text": "A bin has \\(V(x)=x(30-2x)^2\\) cubic inches, \\(0\\le x\\le 15\\); the only interior critical point is 5. Give the largest volume.", "command_verb": "state"}, "key": {"form": "numeric", "expr": "2000"}, "steps": [{"text": "The objective.", "expr": "x*(30 - 2*x)**2", "relation": "new"}, {"text": "\\(V(5)=2000\\); \\(V(0)=V(15)=0\\): 2000 cubic inches.", "expr": "2000", "relation": "evaluate", "subs": {"x": "5"}}], "calculator_status": "no_calculator", "skills": ["BC-SKL-05054"]},
  {"id": "chk-3", "check_kind": "mcq", "format": "mcq", "bands": ["low"], "archetype_id": "BC-QA-05011", "parameter_draw": {"scale": 3, "height_cap": 2, "sheet_shape": "rectangle", "material": "tin", "purpose": "tray", "length_unit": "centimeters", "domain_limit": "binding"}, "stem": {"text": "A tray: \\(V(x)=x(15-2x)(24-2x)\\), height \\(x\\) at most 2 cm; \\(V'(x)=12(x-3)(x-10)\\). What is the largest volume?", "command_verb": "identify"}, "key": {"form": "numeric", "expr": "440*cm**3"}, "steps": [{"text": "The objective.", "expr": "x*(15 - 2*x)*(24 - 2*x)", "relation": "new"}, {"text": "\\(V'>0\\) on \\([0,2]\\), so the right end: \\(V(2)=440\\).", "expr": "440", "relation": "evaluate", "subs": {"x": "2"}}, {"text": "With units.", "expr": "440*cm**3", "relation": "new"}], "options": [{"id": "A", "is_key": false, "expr": "486*cm**3", "error_path": "BC-ERR-05026", "derivation": "V(3) at the critical point, with the ends never evaluated and x = 3 outside the range"}, {"id": "B", "is_key": false, "expr": "440", "error_path": "BC-ERR-05055", "derivation": "the value with no units"}, {"id": "C", "is_key": true, "expr": "440*cm**3", "error_path": null}, {"id": "D", "is_key": false, "expr": "2*cm", "error_path": "BC-ERR-05024", "derivation": "the input reported for the value"}], "calculator_status": "no_calculator", "skills": ["BC-SKL-05056"]}
 ],
 "delivery": [
  {"block": "pr-1", "mode": "text", "reason": "rule 6: a question about the wording of an answer", "sources": ["BC-CON-05014"]},
  {"block": "orientation", "mode": "text", "reason": "rule 6: BC-SKL-05054 to 05057 carry BC-REP-01, 04, 05 only", "sources": ["BC-SKL-05054"]},
  {"block": "ki-1", "mode": "text", "reason": "rule 6: a statement about meaning and units", "sources": ["BC-SKL-05055"]},
  {"block": "ex-1", "mode": "step_reveal", "reason": "rule 1", "sources": []},
  {"block": "err-BC-ERR-05026", "mode": "step_reveal", "reason": "rule 1", "sources": []},
  {"block": "err-BC-ERR-05055", "mode": "step_reveal", "reason": "rule 1", "sources": []},
  {"block": "err-BC-ERR-05024", "mode": "step_reveal", "reason": "rule 1", "sources": []},
  {"block": "err-BC-ERR-05056", "mode": "step_reveal", "reason": "rule 1", "sources": []}
 ],
 "refresher": ["ki-1", "err-BC-ERR-05026", "err-BC-ERR-05055", "err-BC-ERR-05024", "err-BC-ERR-05056", "ex-1"],
 "read_minutes": {"full": 4.0, "brief": 3.0},
 "word_count": {"full": 570, "brief": 429},
 "research_lines": [
  {"file": "research/scoring/common-point-losses.md", "line": "An interpretation point asks what a computed value means in the setting of the problem, in words, with the quantity and the interval named."}
 ],
 "inferred": [
  {"claim": "BC-QA-05011 has calculator_status either; the lesson places it in Section I Part A at 2.14 minutes.", "settles": "A single calculator status on BC-QA-05011 or an official example fixing its part."},
  {"claim": "Units are carried in the SymPy strings as the symbol cm, so a key with units and a bare number compare as distinct.", "settles": "A units convention for keys and options in plan 15's content model."},
  {"claim": "The prediction and the contrast stems are authored on ex-1's draw and on the archetype's typical wording; no record supplies them.", "settles": "The blind re-solve of the prediction key and a pretest measurement of the prediction's option choices."}
 ],
 "sources": ["BC-CON-05014", "BC-SKL-05054", "BC-SKL-05055", "BC-SKL-05056", "BC-SKL-05057", "BC-EK-FUN-4C1", "ced:109", "BC-QA-05011", "BC-QA-05006", "BC-CON-05006", "sg-23:2", "BC-ERR-05026", "BC-ERR-05055", "BC-ERR-05024", "BC-ERR-05056", "BC-MIS-05016", "BC-MIS-07023", "BC-MIS-05015", "research/units/unit-05-analytical-applications-differentiation.md#5.11 Solving Optimization Problems", "research/question-analysis/question-archetypes.md#BC-QA-05011 Applied optimisation with model setup, domain, and verification", "research/scoring/common-point-losses.md#Interpretation points", "research/scoring/common-point-losses.md#Units points", "research/exam/exam-structure.md#Section and part layout"],
 "no_figure_reason": "The skills carry symbolic, verbal and contextual representations only, and the key ideas describe no process, so no figure, table or motion would show more than the sentence about value, units and input."
}
```
