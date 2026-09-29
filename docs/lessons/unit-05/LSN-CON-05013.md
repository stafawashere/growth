---
title: LSN-CON-05013 Optimisation model with an objective and a constraint
research_date: 2026-09-29
status: designed
purpose: Authoring spec for the concept lesson on BC-CON-05013, building a one variable objective from a situation and a constraint, stating its contextual domain and verifying the extremum, built from authoring_bundle("BC-CON-05013") and the research files it cites, so an author fills plan 15's lesson record without making a teaching decision.
---

# LSN-CON-05013 Optimisation model with an objective and a constraint

Concept BC-CON-05013 (skills BC-SKL-05049 to BC-SKL-05053), topic 5.10 of Unit 5. One archetype loads its skills, BC-QA-05011 (family optimisation, tagged [inferred] in research). Unit parents BC-CON-05003, 05006, 05010 (docs/lessons/unit-05/README.md, section 1).

## Prediction

pr-1, `mcq`, both bands, served first, on ex-1's draw. Stem: squares of side x are cut from a 24 by 24 inch sheet and the sides folded up; which formula gives the tray's volume. Key: V = x(24 - 2x)^2, the constraint substituted so one variable remains. Distractors: V = x(24 - x)^2 and V = x^2(24 - 2x), each a mis-built base or height. The resolution states the reduction and the domain in the record's words and says nothing about the student. Sources: BC-CON-05013 and the topic's 5.10 section (research/units/unit-05-analytical-applications-differentiation.md#5.10 Introduction to Optimization Problems). Tagged [inferred] in the record's `inferred` array.

## Orientation

Served text, from BC-CON-05013 `description_plain` and the topic's Assessment behaviour paragraph (research/units/unit-05-analytical-applications-differentiation.md#5.10 Introduction to Optimization Problems): a response names the variables, writes the objective in one variable by substituting the constraint, states the domain from the context, then finds and verifies the extremum on that domain. No count, no frequency.

## Key ideas

All five skills map to BC-EK-FUN-4B1 (ced:108): one core block, both bands.

- ki-1 (core). Paraphrase of Model, Domain and Closing the argument: substitute the constraint to reach one variable; the context sets the domain and so whether endpoints are candidates; a candidates test on a closed domain or the sole critical point rule on an open one closes the argument. No anchor quote, to keep the brief form under 450 words.

## Recognition

BC-QA-05011 (research/question-analysis/question-archetypes.md#BC-QA-05011 Applied optimisation with model setup, domain, and verification): `typical_wording` "find the dimensions that make the described quantity as large as possible, and justify that the value found is the maximum"; `common_givens` a verbal situation or a diagram, a fixed total or a geometric relation, a contextual range; `asked_to_produce` the objective in one variable, the domain, the critical point, the verification, the interpreted value. The signal: "as large as possible" or "least" with two dimensions tied by a fixed quantity. Shape: a multipart FRQ, or an MCQ that supplies the reduced objective; no `official_examples` in the record.

What says "not this concept": the objective already reduced and only the value's meaning asked (BC-CON-05014), or a function given with no constraint (BC-CON-05006).
The contrast pair on st-1 comes from the paragraph above. `this` gives a situation with a fixed sheet and asks for the input of the largest volume. `not_this` gives a bare function with no situation and asks where it attains its absolute maximum on a closed interval, a BC-QA-05006 `typical_wording` stem from outside this archetype and the sibling concept the "not this concept" line names (BC-CON-05006): \(g'(x)=6-2x\) is zero at 3, and g(0) = 0, g(3) = 9, g(5) = 5, so x = 3 (SymPy). `feature` is whether a situation is to be modelled or a function is given.

## Method choice

One strategy block, both bands.

- st-1, BC-QA-05011. Method, `expected_solution_path[0]`: define the variables and write the objective. Rival, `wrong_approaches`: substituting a numerical value before differentiating. Separating feature: the objective is reduced by the constraint to one variable with a stated domain, and numbers enter only after the derivative. Tagged inferred (the archetype record is inferred): both fields are present.
The strategy fields carry no leading label, because the reader prints Cue, First line, Rival and Separating feature itself. st-1 carries the contrast pair described under Recognition. The fields, the orientation, the key idea and the bridges are cut to fit the brief cap once the prediction and the contrast are served.

## Solution path

- ex-1, BC-QA-05011, both bands, no calculator. Draw from `parameter_spec`: scale 4, height_cap 2, sheet_shape square, material cardboard, purpose tray, length_unit inches, domain_limit none. The notes give V(x) = x(24 - 2x)^2 on a 24 by 24 sheet, critical points 4 and 12, optimum 4. No published BC-QA-05011 item carries this draw.
- Steps follow `expected_solution_path`: objective (new); domain 0 to 12 (no value); V prime (differentiate); its zeros (solve); objective again (new) and V(4) = 1024 (evaluate); verification against the endpoints (no value, the justified conclusion); the answer x = 4 (new). A fluent solver writes every line; the domain line is the one most often held in the head (BC-ERR-05052).

## Scoring

BC-QA-05011 lists no `point_types`, so no what_a_reader_scores entry and no point tag. For the author: the archetype's scoring pattern separates setup, derivative condition, verification and interpreted value, and a local verification does not meet a demand on a closed domain (sg-25:19; research/scoring/justification-requirements.md#The candidates test).

## Traps

Six active errors meet the skills; the first four in the bundle's order are served: BC-ERR-05050, BC-ERR-05051, BC-ERR-05052, BC-ERR-05053. BC-ERR-05054 and BC-ERR-99004 are left out by the cap of 4. Low band all four; mid band the first two. All on ex-1's draw, with w = 24 - 2x the base side.

- err-BC-ERR-05050: V = xy^2 with letters never defined. Statement-shaped. No possible reason line.
- err-BC-ERR-05051: x w^2 differentiated with w held fixed. Possible reason, words from BC-MIS-05027.
- err-BC-ERR-05052: no domain stated. Possible reason, words from BC-MIS-05028.
- err-BC-ERR-05053: derivative taken in w after w was eliminated. Possible reason, words from BC-MIS-05033.
All four blocks have `relation` distinct, so all four carry `fix_prompt` true: the student writes the right step before it is shown.

## Representations

None as a separate block. The topic's Representations paragraph names a diagram to a constraint equation (BC-REP-08 to BC-REP-01); ki-1's figure carries it.

## Prerequisite bridge

- BC-PRQ-05003 and BC-PRQ-05005, from their `description_plain` and `failure_signature`.

## Time

BC-QA-05011 is `either`, so Section I Part A, 2.14 minutes per question, in the MCQ form that supplies the reduced objective (research/exam/exam-structure.md#Section and part layout) [inferred]. The FRQ form is a multipart question at 15.0 minutes. The minutes go on the objective and the derivative; the verification is one sentence comparing three values.

## Checks

- chk-1, completion of ex-1, both bands: V(x) and its critical points given; the student compares and answers. Key x = 4.
- chk-2, isomorph, both bands. Draw: scale 3, height_cap 1, sheet_shape rectangle, material steel, purpose planter, length_unit centimeters, domain_limit none. V(x) = x(15 - 2x)(24 - 2x) on 0 to 7.5; critical points 3 and 10. Key x = 3.
- chk-3, MCQ, low band. Draw: scale 2, height_cap 1, sheet_shape square, material tin, purpose storage bin, length_unit inches, domain_limit none. V(x) = x(12 - 2x)^2. Key x = 2. Distractors: unbounded with no domain (BC-ERR-05052), x = 6 from w held fixed (BC-ERR-05051), every x from a derivative in the eliminated w (BC-ERR-05053).

## Delivery

- orientation: text. Rule 6, a statement of what a response shows.
- ki-1: figure, the sheet with the corner squares and the folded box, labels inside. Rule 4 on BC-REP-08 in BC-SKL-05049; not promoted, because BC-QA-05011 `difficulty_variables` are yes or no features (docs/lessons/unit-05/README.md, section 6).
- ex-1 and the four error blocks: step_reveal. Rule 1.
- pr-1: text. Rule 6; the sheet is drawn on ki-1. Figure presence: ki-1 is a drawn figure, so no `no_figure_reason`.

## Band plan
- Low (full): pr-1, orientation, the two bridges, ki-1, st-1 with its contrast pair, ex-1, chk-1, the four error blocks, chk-2, chk-3. 605 words, 4.5 minutes (cap 900 and 6).
- Mid (brief): pr-1, orientation, the two bridges, ki-1, st-1 with its contrast pair, ex-1, chk-1, err-BC-ERR-05050, err-BC-ERR-05051, chk-2. 448 words, 3.0 minutes (cap 450 and 3).
- Refresher: ki-1, the four error blocks, ex-1. No prediction and no check.

## Sources

- BC-CON-05013; BC-SKL-05049, BC-SKL-05050, BC-SKL-05051, BC-SKL-05052, BC-SKL-05053; BC-EK-FUN-4B1; ced:108
- BC-QA-05011; sg-25:19
- BC-QA-05006, BC-CON-05006 (the not-this stem of the contrast pair); research/question-analysis/question-archetypes.md#BC-QA-05006 Absolute extremum by the candidates test with a global justification
- BC-ERR-05050, BC-ERR-05051, BC-ERR-05052, BC-ERR-05053; BC-MIS-05027, BC-MIS-05028, BC-MIS-05033
- BC-PRQ-05003, BC-PRQ-05005
- research/units/unit-05-analytical-applications-differentiation.md#5.10 Introduction to Optimization Problems
- research/question-analysis/question-archetypes.md#BC-QA-05011 Applied optimisation with model setup, domain, and verification
- research/scoring/justification-requirements.md#The candidates test
- research/exam/exam-structure.md#Section and part layout
- [inferred] Section I Part A for an either archetype. Settled by a calculator status on BC-QA-05011.
- [inferred] ki-1 as a static figure. Settled by the modality A/B.
- [inferred] The prediction and the contrast stems, authored on ex-1's draw. Settled by the blind re-solve and a pretest measurement.

## Machine record

```json
{
 "id": "LSN-CON-05013",
 "kind": "concept",
 "target_id": "BC-CON-05013",
 "unit": "05",
 "skills": ["BC-SKL-05049", "BC-SKL-05050", "BC-SKL-05051", "BC-SKL-05052", "BC-SKL-05053"],
 "prediction": {"id": "pr-1", "stem": {"text": "Squares of side \\(x\\) inches are cut from the corners of a 24 by 24 inch sheet and the sides folded up. Which formula gives the tray's volume?", "command_verb": "predict"}, "format": "mcq", "options": [{"id": "A", "label": "\\(V=x(24-2x)^2\\)", "is_key": true}, {"id": "B", "label": "\\(V=x(24-x)^2\\)", "is_key": false}, {"id": "C", "label": "\\(V=x^2(24-2x)\\)", "is_key": false}], "resolution": "The base side is \\(24-2x\\), so \\(V(x)=x(24-2x)^2\\). The cut cannot exceed 12, so \\(0\\le x\\le 12\\) and the endpoints are candidates.", "sources": ["BC-CON-05013", "research/units/unit-05-analytical-applications-differentiation.md#5.10 Introduction to Optimization Problems"]},
 "orientation": {"text": "A response defines the variables, reduces the objective to one variable, states the domain, then verifies the extremum.", "sources": ["BC-CON-05013", "research/units/unit-05-analytical-applications-differentiation.md#5.10 Introduction to Optimization Problems"]},
 "key_ideas": [
  {"id": "ki-1", "ek_id": "BC-EK-FUN-4B1", "depth": "core", "text": "The constraint reduces the objective to one variable. The context sets the domain, so a closed domain makes the endpoints candidates.", "notation": "objective function; constraint; domain", "quote": null, "sources": ["BC-EK-FUN-4B1", "ced:108", "research/units/unit-05-analytical-applications-differentiation.md#5.10 Introduction to Optimization Problems"]}
 ],
 "strategy": [
  {"id": "st-1", "archetype_id": "BC-QA-05011", "cue": "A largest or least quantity with a fixed total.", "method": "Define the variables and write the objective.", "rival": "Substituting a number before differentiating.", "separating_feature": "The constraint leaves one variable on a stated domain.", "sources": ["BC-QA-05011"], "evidence_tag": "inferred", "contrast": {"this": {"text": "Squares of side \\(x\\) are cut from a 20 by 20 sheet and the sides folded up. Find \\(x\\) for the largest volume.", "archetype_id": "BC-QA-05011"}, "not_this": {"text": "\\(g(x)=6x-x^2\\) on \\([0,5]\\). Where does \\(g\\) attain its absolute maximum?", "why_not": "No situation; the function is given."}, "feature": "A situation to model, or a function given."}}
 ],
 "worked_examples": [
  {"id": "ex-1", "archetype_id": "BC-QA-05011", "bands": ["low", "mid"], "parameter_draw": {"scale": 4, "height_cap": 2, "sheet_shape": "square", "material": "cardboard", "purpose": "tray", "length_unit": "inches", "domain_limit": "none"}, "problem": {"text": "Squares of side \\(x\\) inches are cut from the corners of a 24 by 24 inch cardboard sheet and the sides folded up to make a tray. Find \\(x\\) giving the largest volume. Justify.", "command_verb": "find"}, "calculator_status": "no_calculator", "steps": [{"cue": "Largest volume: the objective is \\(V\\); the base side is \\(24-2x\\).", "why": "The constraint is folded in, so one variable remains.", "expr": "x*(24 - 2*x)**2", "relation": "new"}, {"cue": "The cut cannot be negative or exceed half the side.", "why": "Domain \\(0\\le x\\le 12\\), so the endpoints are candidates."}, {"cue": "One variable, so differentiate.", "why": "\\(V'(x)=(24-2x)(24-6x)\\).", "expr": "(24 - 2*x)*(24 - 6*x)", "relation": "differentiate", "variable": "x"}, {"cue": "Critical points: \\(V'(x)=0\\).", "why": "\\(x=4\\) or \\(x=12\\).", "expr": "FiniteSet(4, 12)", "relation": "solve", "variable": "x"}, {"cue": "Closed domain: evaluate \\(V\\) at each candidate.", "why": "Back to the objective.", "expr": "x*(24 - 2*x)**2", "relation": "new"}, {"cue": "Interior candidate \\(x=4\\).", "why": "\\(V(4)=4\\cdot16^2=1024\\).", "expr": "1024", "relation": "evaluate", "subs": {"x": "4"}}, {"cue": "The stem says justify: compare with the endpoints.", "why": "\\(V(0)=V(12)=0<1024\\), so the maximum on \\([0,12]\\) is at \\(x=4\\)."}, {"cue": "The stem asks for \\(x\\).", "why": "4 inches.", "expr": "4", "relation": "new"}], "answer": {"form": "numeric", "expr": "4"}}
 ],
 "what_a_reader_scores": [],
 "common_errors": [
  {"error_id": "BC-ERR-05050", "observed_behavior": "The response writes an objective and a constraint in letters that are never given meanings or units.", "scoring_consequence": "The setup point is at risk and the interpretation that follows has nothing to name.", "wrong_step": {"text": "\\(V=xy^2\\), with \\(x\\) and \\(y\\) never defined.", "expr": "letters_without_meaning"}, "right_step": {"text": "\\(x\\) is the cut in inches, \\(V\\) the volume in cubic inches.", "expr": "letters_defined_with_units"}, "relation": "distinct", "possible_reason": null, "sources": ["BC-ERR-05050"], "fix_prompt": true},
  {"error_id": "BC-ERR-05051", "observed_behavior": "The response differentiates an expression that still contains both unknowns.", "scoring_consequence": "The derivative is not the derivative of a one variable objective, so the critical point is wrong.", "wrong_step": {"text": "\\(V=xw^2\\) differentiated in \\(x\\) with \\(w\\) held fixed: \\(w^2\\).", "expr": "w**2"}, "right_step": {"text": "\\(w=24-2x\\) substituted first: \\((24-2x)(24-6x)\\).", "expr": "(24 - 2*x)*(24 - 6*x)"}, "relation": "distinct", "possible_reason": {"misconception_id": "BC-MIS-05027", "text": "differentiates the first expression written down"}, "sources": ["BC-ERR-05051", "BC-MIS-05027"], "fix_prompt": true},
  {"error_id": "BC-ERR-05052", "observed_behavior": "The response never states the range of inputs the situation allows and treats the objective as defined everywhere.", "scoring_consequence": "Endpoints that could hold the extremum are never considered and the verification is incomplete.", "wrong_step": {"text": "\\(V\\) treated on all real \\(x\\).", "expr": "Interval(-oo, oo)"}, "right_step": {"text": "\\(0\\le x\\le 12\\).", "expr": "Interval(0, 12)"}, "relation": "distinct", "possible_reason": {"misconception_id": "BC-MIS-05028", "text": "ignores what the situation permits"}, "sources": ["BC-ERR-05052", "BC-MIS-05028"], "fix_prompt": true},
  {"error_id": "BC-ERR-05053", "observed_behavior": "The response differentiates with respect to a variable that the constraint has already eliminated.", "scoring_consequence": "The derivative is meaningless for the reduced objective and the critical point is wrong.", "wrong_step": {"text": "\\(\\frac{dV}{dw}=0\\) once \\(w\\) is replaced by \\(24-2x\\), so every \\(x\\) is critical.", "expr": "0"}, "right_step": {"text": "\\(\\frac{dV}{dx}=(24-2x)(24-6x)\\).", "expr": "(24 - 2*x)*(24 - 6*x)"}, "relation": "distinct", "possible_reason": {"misconception_id": "BC-MIS-05033", "text": "differentiates expressions in the second variable without the chain rule"}, "sources": ["BC-ERR-05053", "BC-MIS-05033"], "fix_prompt": true}
 ],
 "representations": null,
 "prerequisite_bridges": [
  {"prq_id": "BC-PRQ-05003", "text": "State the allowed inputs."},
  {"prq_id": "BC-PRQ-05005", "text": "Write the volume in the named dimensions."}
 ],
 "time": {"exam_part": "I-A", "budget_minutes": 2.14, "source": "research/exam/exam-structure.md#Section and part layout", "written_steps": {"ex-1": [1, 2, 3, 4, 6, 7, 8]}, "skipped_steps": {"ex-1": [5]}},
 "checks": [
  {"id": "chk-1", "check_kind": "completion", "format": "short_answer", "bands": ["low", "mid"], "archetype_id": "BC-QA-05011", "parameter_draw": {"scale": 4, "height_cap": 2, "sheet_shape": "square", "material": "cardboard", "purpose": "tray", "length_unit": "inches", "domain_limit": "none"}, "completes": "ex-1", "stem": {"text": "\\(V(x)=x(24-2x)^2\\) on \\(0\\le x\\le 12\\) has critical points 4 and 12. Give the \\(x\\) of the largest volume.", "command_verb": "find"}, "key": {"form": "numeric", "expr": "4"}, "steps": [{"text": "The objective.", "expr": "x*(24 - 2*x)**2", "relation": "new"}, {"text": "\\(V(4)=1024\\); \\(V(0)=V(12)=0\\).", "expr": "1024", "relation": "evaluate", "subs": {"x": "4"}}, {"text": "Largest at \\(x=4\\).", "expr": "4", "relation": "new"}], "calculator_status": "no_calculator", "skills": ["BC-SKL-05053"]},
  {"id": "chk-2", "check_kind": "isomorph", "format": "short_answer", "bands": ["low", "mid"], "archetype_id": "BC-QA-05011", "parameter_draw": {"scale": 3, "height_cap": 1, "sheet_shape": "rectangle", "material": "steel", "purpose": "planter", "length_unit": "centimeters", "domain_limit": "none"}, "stem": {"text": "Corner squares of side \\(x\\) cm are cut from a 15 by 24 cm steel sheet to make a planter. Find \\(x\\) giving the largest volume.", "command_verb": "find"}, "key": {"form": "numeric", "expr": "3"}, "steps": [{"text": "\\(V(x)=x(15-2x)(24-2x)\\) on \\(0\\le x\\le 7.5\\).", "expr": "x*(15 - 2*x)*(24 - 2*x)", "relation": "new"}, {"text": "\\(V'(x)=12(x-3)(x-10)\\).", "expr": "12*(x - 3)*(x - 10)", "relation": "differentiate", "variable": "x"}, {"text": "Critical points 3 and 10; only 3 is in the domain.", "expr": "FiniteSet(3, 10)", "relation": "solve", "variable": "x"}, {"text": "\\(V(3)=486>0=V(0)=V(7.5)\\).", "expr": "3", "relation": "new"}], "calculator_status": "no_calculator", "skills": ["BC-SKL-05052"]},
  {"id": "chk-3", "check_kind": "mcq", "format": "mcq", "bands": ["low"], "archetype_id": "BC-QA-05011", "parameter_draw": {"scale": 2, "height_cap": 1, "sheet_shape": "square", "material": "tin", "purpose": "storage bin", "length_unit": "inches", "domain_limit": "none"}, "stem": {"text": "Corner squares of side \\(x\\) in are cut from a 12 by 12 in tin sheet, base side \\(w=12-2x\\). Which conclusion is correct?", "command_verb": "identify"}, "key": {"form": "statement", "expr": "largest_volume_at_x_equals_2"}, "steps": [{"text": "\\(V(x)=x(12-2x)^2\\) on \\(0\\le x\\le 6\\).", "expr": "x*(12 - 2*x)**2", "relation": "new"}, {"text": "\\(V'(x)=(12-2x)(12-6x)\\).", "expr": "(12 - 2*x)*(12 - 6*x)", "relation": "differentiate", "variable": "x"}, {"text": "Zeros 2 and 6; \\(V(2)=128\\), \\(V(0)=V(6)=0\\).", "expr": "FiniteSet(2, 6)", "relation": "solve", "variable": "x"}], "options": [{"id": "A", "is_key": true, "label": "\\(x=2\\) in, since \\(V(2)=128\\) exceeds \\(V(0)=V(6)=0\\).", "error_path": null}, {"id": "B", "is_key": false, "label": "No largest volume: \\(V(x)\\) grows without bound as \\(x\\) grows.", "error_path": "BC-ERR-05052", "derivation": "the domain never stated, so V is read on all real x"}, {"id": "C", "is_key": false, "label": "\\(x=6\\) in, where \\(w^2\\), the derivative with \\(w\\) held fixed, is zero.", "error_path": "BC-ERR-05051", "derivation": "x w^2 differentiated in x with w held fixed, giving w = 0"}, {"id": "D", "is_key": false, "label": "Every \\(x\\): \\(\\frac{dV}{dw}=0\\) once \\(w\\) is replaced by \\(12-2x\\).", "error_path": "BC-ERR-05053", "derivation": "derivative taken in the eliminated variable w"}], "calculator_status": "no_calculator", "skills": ["BC-SKL-05051"]}
 ],
 "delivery": [
  {"block": "pr-1", "mode": "text", "reason": "rule 6: a formula question; the sheet is drawn on ki-1", "sources": ["BC-CON-05013"]},
  {"block": "orientation", "mode": "text", "reason": "rule 6: a statement of what a response shows; the diagram is served once, on ki-1", "sources": ["BC-SKL-05049"]},
  {"block": "ki-1", "mode": "figure", "reason": "rule 4: BC-REP-08 on BC-SKL-05049; not promoted, BC-QA-05011 difficulty_variables are yes or no features", "sources": ["BC-SKL-05049", "BC-QA-05011"], "spec": {"kind": "geometric_diagram", "representations": ["BC-REP-08"], "labels": [{"text": "x", "placement": "inside", "at": [1, 1.5]}, {"text": "24 - 2x", "placement": "inside", "at": [8, 1.5]}, {"text": "V = x(24 - 2x)^2", "placement": "inside", "at": [30, 16]}, {"text": "0 <= x <= 12", "placement": "inside", "at": [30, 20]}], "window": {"x": [-2, 56], "y": [-2, 26]}, "segments": [{"from": [4, 0], "to": [20, 0]}, {"from": [20, 0], "to": [20, 4]}, {"from": [20, 4], "to": [24, 4]}, {"from": [24, 4], "to": [24, 20]}, {"from": [24, 20], "to": [20, 20]}, {"from": [20, 20], "to": [20, 24]}, {"from": [20, 24], "to": [4, 24]}, {"from": [4, 24], "to": [4, 20]}, {"from": [4, 20], "to": [0, 20]}, {"from": [0, 20], "to": [0, 4]}, {"from": [0, 4], "to": [4, 4]}, {"from": [4, 4], "to": [4, 0]}, {"from": [0, 0], "to": [4, 0], "style": "dashed"}, {"from": [0, 0], "to": [0, 4], "style": "dashed"}, {"from": [20, 0], "to": [24, 0], "style": "dashed"}, {"from": [24, 0], "to": [24, 4], "style": "dashed"}, {"from": [24, 24], "to": [20, 24], "style": "dashed"}, {"from": [24, 24], "to": [24, 20], "style": "dashed"}, {"from": [0, 24], "to": [4, 24], "style": "dashed"}, {"from": [0, 24], "to": [0, 20], "style": "dashed"}, {"from": [4, 4], "to": [20, 4], "style": "dashed"}, {"from": [20, 4], "to": [20, 20], "style": "dashed"}, {"from": [20, 20], "to": [4, 20], "style": "dashed"}, {"from": [4, 20], "to": [4, 4], "style": "dashed"}, {"from": [30, 0], "to": [46, 0]}, {"from": [46, 0], "to": [46, 4]}, {"from": [46, 4], "to": [30, 4]}, {"from": [30, 4], "to": [30, 0]}, {"from": [30, 4], "to": [36, 10]}, {"from": [36, 10], "to": [52, 10]}, {"from": [52, 10], "to": [46, 4]}, {"from": [46, 0], "to": [52, 6]}, {"from": [52, 6], "to": [52, 10]}]}, "fallback": "the same sheet and box, static, as a described diagram with the four labels inside", "keyboard": "none needed; no control"},
  {"block": "ex-1", "mode": "step_reveal", "reason": "rule 1", "sources": []},
  {"block": "err-BC-ERR-05050", "mode": "step_reveal", "reason": "rule 1", "sources": []},
  {"block": "err-BC-ERR-05051", "mode": "step_reveal", "reason": "rule 1", "sources": []},
  {"block": "err-BC-ERR-05052", "mode": "step_reveal", "reason": "rule 1", "sources": []},
  {"block": "err-BC-ERR-05053", "mode": "step_reveal", "reason": "rule 1", "sources": []}
 ],
 "refresher": ["ki-1", "err-BC-ERR-05050", "err-BC-ERR-05051", "err-BC-ERR-05052", "err-BC-ERR-05053", "ex-1"],
 "read_minutes": {"full": 4.5, "brief": 3.0},
 "word_count": {"full": 604, "brief": 447},
 "research_lines": [
  {"file": "research/scoring/justification-requirements.md", "line": "sg-25:5 requires a global argument that correctly evaluates the function at the interior critical point and at both endpoints."}
 ],
 "inferred": [
  {"claim": "BC-QA-05011 has calculator_status either; the lesson places it in Section I Part A at 2.14 minutes, the MCQ form with the reduced objective.", "settles": "A single calculator status on BC-QA-05011 or an official example fixing its part."},
  {"claim": "ki-1 is served as a static diagram rather than text.", "settles": "The modality A/B in the build plan: skip rate and time to first credited success by mode."},
  {"claim": "The prediction and the contrast stems are authored on ex-1's draw and on the archetype's typical wording; no record supplies them.", "settles": "The blind re-solve of the prediction key and a pretest measurement of the prediction's option choices."}
 ],
 "sources": ["BC-CON-05013", "BC-SKL-05049", "BC-SKL-05050", "BC-SKL-05051", "BC-SKL-05052", "BC-SKL-05053", "BC-EK-FUN-4B1", "ced:108", "BC-QA-05011", "BC-QA-05006", "BC-CON-05006", "sg-25:19", "BC-ERR-05050", "BC-ERR-05051", "BC-ERR-05052", "BC-ERR-05053", "BC-MIS-05027", "BC-MIS-05028", "BC-MIS-05033", "BC-PRQ-05003", "BC-PRQ-05005", "research/units/unit-05-analytical-applications-differentiation.md#5.10 Introduction to Optimization Problems", "research/question-analysis/question-archetypes.md#BC-QA-05011 Applied optimisation with model setup, domain, and verification", "research/scoring/justification-requirements.md#The candidates test", "research/exam/exam-structure.md#Section and part layout"]
}
```
