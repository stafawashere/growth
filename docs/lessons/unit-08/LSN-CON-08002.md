---
title: LSN-CON-08002 Average value contrasted with average rate of change
research_date: 2026-09-29
status: designed
purpose: Authoring spec for the concept lesson on BC-CON-08002, telling the average value of a function from its average rate of change by the stem's wording and by units, built from authoring_bundle("BC-CON-08002") and the research files it cites, so an author fills plan 15's lesson record without making a teaching decision.
---

# LSN-CON-08002 Average value contrasted with average rate of change

Concept BC-CON-08002 (skills BC-SKL-08004, BC-SKL-08005), topic 8.1 of Unit 8, hard parent BC-CON-08001 (docs/lessons/unit-08/README.md, section 1). The bundle lists five archetypes loading its skills, BC-QA-08002 first; the lesson carries three strategy blocks (cap 3) for the three families the unit README's contrast row names (docs/lessons/unit-08/README.md, section 3).

## Prediction

Predict which expression gives the average rate of change of W(t) = 3e^(t/2) + t gallons on [1, 3], before any rule is stated. Form: mcq, three options, key: the endpoint difference over the interval length. The rivals are the integral quotient (BC-QA-99007 `wrong_approaches`) and the mean of the endpoint derivatives. The resolution names the quotient and its units and says nothing about the reader's choice. Sources: BC-CON-08002 and the topic 8.1 section its key idea cites.

## Orientation

Served text, from BC-CON-08002 `description_plain` and the topic's Assessment behaviour paragraph (research/units/unit-08-applications-integration.md#8.1 Finding the Average Value of a Function on an Interval): the wording decides the formula. "Average value of f" is an integral quotient in the units of f; "average rate of change" is a difference quotient in units per unit of input. No count, no frequency.

## Key ideas

Both skills map to BC-EK-CHA-4B1 (ced:152): one core block, both bands.

- ki-1 (core). Paraphrase of the Required mathematical knowledge paragraphs (Average value, Average rate of change, Units): the two formulas side by side with their units, and the fact that they coincide numerically when F is an antiderivative of f (sg-25:4). No anchor quote. Notation line from the concept record.

## Recognition

- BC-QA-08002 (family mean-value-theorem, calculator; research/question-analysis/question-archetypes.md#BC-QA-08002 Instantaneous rate set equal to an average rate of change): `typical_wording` "find the time at which the instantaneous rate of change of the modelled quantity equals its average rate of change over the stated interval"; `common_givens` a model function, its derivative, a closed interval; `asked_to_produce` an equation, a solved input value. Official parts BC-FRQ-2014-Q1-A, 2014-Q1-C, 2025-Q1-B.
- BC-QA-99007 (research/question-analysis/question-archetypes.md#BC-QA-99007 Average rate of change reported on its own with units): "find the average rate of change of the modelling function over the stated interval, indicating units of measure".
- BC-QA-08001 (research/question-analysis/question-archetypes.md#BC-QA-08001 Average value of a function over an interval): "find the average value of the function over the stated interval".

The signal is the word after "average": "value of f" against "rate of change of f". BC-QA-06015 and BC-QA-99009 also load BC-SKL-08005 and are not given blocks (cap 3); their shapes are the interpretation sentence and a density count, which belong to topic 8.3.

The near miss for the contrast pair is BC-QA-08001, the average value of a function on the same interval (a stem from outside BC-QA-08002): it uses the same function and interval and asks for the integral quotient, not a time. The pair separates on the phrase after "average".

## Method choice

- st-1, BC-QA-08002 (both bands). Method, `expected_solution_path[0]`: compute the average rate of change over the interval. Rival, `wrong_approaches`: reporting the average rate of change itself as the time. Separating feature: the stem asks for a time, so the rate is only the right side of an equation.
- st-2, BC-QA-99007 (low band). Method: evaluate the function at both endpoints. Rival: integrating the function and dividing by the interval length. Separating feature: "rate of change".
- st-3, BC-QA-08001 (low band). Method: write the definite integral of the function over the interval. Rival: averaging the two endpoint values. Separating feature: "average value of".

All three archetypes carry `asked_to_produce` and `common_givens`; none is tagged inferred.

Contrast pair on st-1. This: a BC-QA-08002 stem, the time at which the instantaneous rate equals the average rate of change. Not this: the BC-QA-08001 stem, the average value of the function, an integral quotient. The feature is which quotient the wording names.

## Solution path

- ex-1, BC-QA-08002, both bands, calculator. Draw: model exponential, coefficient 3, linear_rate 1, scale 2, start 1, length 2, context water, framing context, presentation formula, so \(W(t)=3e^{t/2}+t\) gallons on [1, 3]. The constraint start + length <= 7 holds. No published BC-QA-08002 item carries this draw.
- Steps follow `expected_solution_path`: the average rate of change (new, tagged BC-PT-99021); \(W'(t)\) set equal to it (new); the solve (solve); the value to three places (evaluate, approx). The draw admits an exact root, \(t=2\ln(e^{3/2}-e^{1/2})\), which the calculator solve returns as 2.083. A fluent solver writes the quotient, the equation and the value, and holds the derivative.

## Scoring

BC-QA-08002 lists BC-PT-99021, 99020, 99004, 99005. ex-1 tags BC-PT-99021 on step 1; the line is `reader_checks(["BC-PT-99021"])`. BC-PT-99005 is earned on the final value with its equation but not tagged, to hold the brief cap (listed inferred). The scoring pattern: the average rate value alone presented as the answer earns neither point (sg-25:4). Point losses: an average value setup replaced by a difference quotient, or the reverse (research/scoring/common-point-losses.md#Setup points, BC-ERR-99015); units missing or built wrongly (research/scoring/common-point-losses.md#Units points, BC-ERR-99005).

## Traps

Two active errors meet the skills, both served in both bands.

- err-BC-ERR-99015: the average value of W taken in place of the average rate of change. Possible reason, words from BC-MIS-99006.
- err-BC-ERR-99005: the rate reported in gallons, against gallons per hour. The two values are equal, so the relation is equivalent: the error is in the units line. Possible reason, words from BC-MIS-02008.

## Representations

None. The topic's Representations paragraph names contextual, symbolic and calculator conversions for this contrast; nothing figure-shaped.

## Prerequisite bridge

- BC-PRQ-06005, from its `description_plain` and `failure_signature`.

## Time

BC-QA-08002 is `calculator`, one part of the calculator active free response question: Section II Part A, 15.0 minutes per question (research/exam/exam-structure.md#Section and part layout). Two points, a 3.33 minute share (docs/lessons/unit-08/README.md, section 5) [inferred]. The minutes go on the quotient and the equation; the solve is typed.

## Checks

- chk-1, completion of ex-1, both bands: the average rate is given as the exact quotient; the student solves. Key 2.083.
- chk-2, isomorph, both bands. Draw: exponential, coefficient 4, linear_rate 2, scale 2, start 2, length 2; \(W(t)=4e^{t/2}+2t\) on [2, 4]. Key 3.083.
- No chk-3: the bundle holds two errors, and a 4-option MCQ needs three distractors anchored to error blocks (listed inferred).

## Delivery

- orientation: text. Rule 6: BC-REP-04, 01 and 05 on the skills, none figure-bearing.
- ki-1: text. Rule 6; the unit README's delivery map names the two quotients side by side as text.
- ex-1, err-BC-ERR-99015, err-BC-ERR-99005: step_reveal. Rule 1.

Figure presence: no delivery entry is drawn, so the record carries `no_figure_reason`. No skill of BC-CON-08002 carries a figure-bearing representation (BC-REP-04, 01 and 05 only), and ki-1 holds two formulas with units, no process. Rules 2 to 5 do not apply.

## Band plan

The served order of 2026-09-29: prediction, orientation, bridges, key ideas, strategy with the contrast pair, example 1 and its scoring lines, check 1, error blocks, example 2 faded when present, check 2, representations, check 3.

- Low (full): orientation, ki-1, st-1 to st-3, ex-1 with its scoring line, two error blocks, chk-1, chk-2, the bridge, with the prediction and the st-1 contrast pair first. 512 words, 3.5 minutes (cap 900 and 6).
- Mid (brief): orientation, ki-1, st-1 with the contrast pair, ex-1 with its scoring line, two error blocks, chk-1, chk-2, the bridge, with the prediction first. 450 words, 3.0 minutes (cap 450 and 3).
- Refresher: ki-1, err-BC-ERR-99015, err-BC-ERR-99005, ex-1.

## Sources

- BC-CON-08002; BC-SKL-08004, BC-SKL-08005; BC-EK-CHA-4B1; ced:152
- BC-QA-08002, BC-QA-99007, BC-QA-08001, BC-QA-06015, BC-QA-99009; BC-PT-99021; sg-25:4
- BC-ERR-99015, BC-ERR-99005; BC-MIS-99006, BC-MIS-02008
- BC-PRQ-06005
- research/units/unit-08-applications-integration.md#8.1 Finding the Average Value of a Function on an Interval
- research/question-analysis/question-archetypes.md#BC-QA-08002 Instantaneous rate set equal to an average rate of change
- research/question-analysis/question-archetypes.md#BC-QA-99007 Average rate of change reported on its own with units
- research/question-analysis/question-archetypes.md#BC-QA-08001 Average value of a function over an interval
- research/scoring/common-point-losses.md#Setup points
- research/scoring/common-point-losses.md#Units points
- research/exam/exam-structure.md#Section and part layout
- [inferred] The 3.33 minute share and the held derivative. Settled by per-step timing data.
- [inferred] BC-PT-99005 untagged. Settled by a brief cap that admits two reader lines.
- [inferred] Two checks only. Settled by a third active error on BC-SKL-08004 or BC-SKL-08005.
- [inferred] pr-1 and the st-1 contrast pair are authored for the redesign. Settled by the pretest and contrast measurements in the build plan.
- [inferred] No drawn block. Settled by a figure-bearing representation on BC-SKL-08004 or BC-SKL-08005.

## Machine record

```json
{
 "id": "LSN-CON-08002",
 "kind": "concept",
 "target_id": "BC-CON-08002",
 "unit": "08",
 "skills": ["BC-SKL-08004", "BC-SKL-08005"],
 "prediction": {"id": "pr-1", "stem": {"text": "Predict: W(t) = 3e^(t/2) + t on [1, 3]. Which is the average rate of change of W?", "command_verb": "predict"}, "format": "mcq", "options": [{"id": "A", "label": "Integral of W over [1, 3], divided by 2", "is_key": false}, {"id": "B", "label": "W(3) minus W(1), divided by 2", "is_key": true}, {"id": "C", "label": "W'(1) plus W'(3), halved", "is_key": false}], "resolution": "The change in W over the change in t, in gallons per hour.", "sources": ["BC-CON-08002", "research/units/unit-08-applications-integration.md#8.1 Finding the Average Value of a Function on an Interval"]},
 "no_figure_reason": "The topic gives contextual, symbolic and calculator conversions, and no skill carries a figure-bearing representation. The key idea is a pair of formulas with units, with no process to draw.",
 "orientation": {"text": "The wording picks the formula: integral quotient or difference quotient.", "sources": ["BC-CON-08002", "research/units/unit-08-applications-integration.md#8.1 Finding the Average Value of a Function on an Interval"]},
 "key_ideas": [
  {"id": "ki-1", "ek_id": "BC-EK-CHA-4B1", "depth": "core", "text": "Average value: the integral of f over [a, b], over b minus a. Average rate: F(b) minus F(a), over b minus a.", "notation": "average value; average rate", "quote": null, "sources": ["BC-EK-CHA-4B1", "ced:152", "sg-25:4", "research/units/unit-08-applications-integration.md#8.1 Finding the Average Value of a Function on an Interval"]}
 ],
 "strategy": [
  {"id": "st-1", "archetype_id": "BC-QA-08002", "cue": "When the rate equals the average rate.", "method": "The average rate of change.", "rival": "Reporting it as the time.", "separating_feature": "A time is asked.", "sources": ["BC-QA-08002"], "evidence_tag": "verified", "contrast": {"this": {"text": "Find t where P'(t) equals the average rate of change of P on [0, 4].", "archetype_id": "BC-QA-08002"}, "not_this": {"text": "Find the average value of P on [0, 4].", "why_not": "It asks for an integral quotient."}, "feature": "Rate of change: endpoint quotient. Average value: integral quotient."}},
  {"id": "st-2", "archetype_id": "BC-QA-99007", "cue": "The average rate of change with units, from a function and a closed interval.", "method": "The function at both endpoints.", "rival": "Integrating the function and dividing by the interval length.", "separating_feature": "The words rate of change.", "sources": ["BC-QA-99007"], "evidence_tag": "verified"},
  {"id": "st-3", "archetype_id": "BC-QA-08001", "cue": "The average value of a model function over a closed interval.", "method": "The integral of the function over the interval.", "rival": "Averaging the two endpoint values.", "separating_feature": "The words average value of.", "sources": ["BC-QA-08001"], "evidence_tag": "verified"}
 ],
 "worked_examples": [
  {"id": "ex-1", "archetype_id": "BC-QA-08002", "bands": ["low", "mid"], "parameter_draw": {"model": "exponential", "coefficient": 3, "linear_rate": 1, "scale": 2, "start": 1, "length": "2", "context": "water", "framing": "context", "presentation": "formula"}, "problem": {"text": "A tank holds W(t) = 3e^(t/2) + t gallons at t hours. Find t in (1, 3) where W'(t) equals W's average rate of change over [1, 3].", "command_verb": "find"}, "calculator_status": "calculator", "steps": [{"cue": "Rate of change over [1, 3]: the difference quotient.", "why": "Endpoint values, not an integral. Gallons per hour.", "expr": "(3*exp(3/2) + 3 - (3*exp(1/2) + 1))/2", "relation": "new", "point_type_id": "BC-PT-99021"}, {"cue": "Instantaneous rate equals that average: W'(t) set equal to it.", "why": "The equation is the setup the answer needs.", "expr": "3*exp(t/2)/2 + 1 = (3*exp(3/2) + 3 - (3*exp(1/2) + 1))/2", "relation": "new"}, {"cue": "The stem asks for t.", "why": "The calculator solve on (1, 3).", "expr": "2*log(exp(3/2) - exp(1/2))", "relation": "solve", "variable": "t"}, {"cue": "Three decimals.", "why": "Hours, inside (1, 3).", "expr": "2.083", "relation": "evaluate", "subs": {}, "approx": true}], "answer": {"form": "numeric", "expr": "2.083"}}
 ],
 "what_a_reader_scores": [
  {"example_id": "ex-1", "point_type_ids": ["BC-PT-99021"], "lines": [{"point_type_id": "BC-PT-99021", "text": "Average rate of change expression. Earned by: An expression showing both a difference of function values and a quotient by the difference of inputs, or its correct value (sg-26:2, sg-25:11). Not earned by: A bare quotient template with no values substituted (sg-25:11, sg-26:2); the solved value alone where the prompt demanded the setup (sg-25:4). Precision: sg-22:13 and sg-21:17 do not require simplification, but any simplification presented must be correct."}]}
 ],
 "common_errors": [
  {"error_id": "BC-ERR-99015", "observed_behavior": "Responses compute a difference quotient where the average value of a function was asked, or integrate the derivative instead of the function, or divide by the wrong quantity.", "scoring_consequence": "The setup point is not earned and the numerical answer point follows it.", "wrong_step": {"text": "Average value of W.", "expr": "Integral(3*exp(t/2) + t, (t, 1, 3))/2"}, "right_step": {"text": "Average rate of change.", "expr": "(3*exp(3/2) + 3 - (3*exp(1/2) + 1))/2"}, "relation": "distinct", "possible_reason": {"misconception_id": "BC-MIS-99006", "text": "treats the two phrases as synonyms"}, "sources": ["BC-ERR-99015", "BC-MIS-99006"], "fix_prompt": true},
  {"error_id": "BC-ERR-99005", "observed_behavior": "Responses give no units where units are requested, or report units of the original quantity instead of the derived one, for example words per minute for a second difference quotient.", "scoring_consequence": "The units point is not earned; it is scored separately from the value.", "wrong_step": {"text": "5.249 gallons.", "expr": "5.249"}, "right_step": {"text": "5.249 gallons per hour.", "expr": "5.249"}, "relation": "equivalent", "possible_reason": {"misconception_id": "BC-MIS-02008", "text": "treats units as optional"}, "sources": ["BC-ERR-99005", "BC-MIS-02008"], "fix_prompt": false}
 ],
 "representations": null,
 "prerequisite_bridges": [
  {"prq_id": "BC-PRQ-06005", "text": "W is the amount, W' its rate."}
 ],
 "time": {"exam_part": "II-A", "budget_minutes": 15.0, "source": "research/exam/exam-structure.md#Section and part layout", "written_steps": {"ex-1": [1, 2, 4]}, "skipped_steps": {"ex-1": [3]}},
 "checks": [
  {"id": "chk-1", "check_kind": "completion", "format": "short_answer", "bands": ["low", "mid"], "archetype_id": "BC-QA-08002", "parameter_draw": {"model": "exponential", "coefficient": 3, "linear_rate": 1, "scale": 2, "start": 1, "length": "2", "context": "water", "framing": "context", "presentation": "formula"}, "completes": "ex-1", "stem": {"text": "W(t) = 3e^(t/2) + t. Solve W'(t) = (W(3) - W(1))/2 on (1, 3), to three places.", "command_verb": "solve"}, "key": {"form": "numeric", "expr": "2.083"}, "steps": [{"text": "The equation.", "expr": "3*exp(t/2)/2 + 1 = (3*exp(3/2) + 3 - (3*exp(1/2) + 1))/2", "relation": "new"}, {"text": "Solve.", "expr": "2*log(exp(3/2) - exp(1/2))", "relation": "solve", "variable": "t"}, {"text": "Three places.", "expr": "2.083", "relation": "evaluate", "subs": {}, "approx": true}], "calculator_status": "calculator", "skills": ["BC-SKL-08004"]},
  {"id": "chk-2", "check_kind": "isomorph", "format": "short_answer", "bands": ["low", "mid"], "archetype_id": "BC-QA-08002", "parameter_draw": {"model": "exponential", "coefficient": 4, "linear_rate": 2, "scale": 2, "start": 2, "length": "2", "context": "water", "framing": "bare", "presentation": "formula"}, "stem": {"text": "W(t) = 4e^(t/2) + 2t. Find t in (2, 4) where W'(t) equals the average rate of change of W over [2, 4].", "command_verb": "find"}, "key": {"form": "numeric", "expr": "3.083"}, "steps": [{"text": "Average rate.", "expr": "(4*exp(2) + 8 - (4*exp(1) + 4))/2", "relation": "new"}, {"text": "The equation.", "expr": "2*exp(t/2) + 2 = (4*exp(2) + 8 - (4*exp(1) + 4))/2", "relation": "new"}, {"text": "Solve.", "expr": "2*log(exp(2) - exp(1))", "relation": "solve", "variable": "t"}, {"text": "Three places.", "expr": "3.083", "relation": "evaluate", "subs": {}, "approx": true}], "calculator_status": "calculator", "skills": ["BC-SKL-08004"]}
 ],
 "delivery": [
  {"block": "orientation", "mode": "text", "reason": "rule 6: BC-REP-04, 01 and 05 on the skills, none figure-bearing", "sources": ["BC-SKL-08004", "BC-SKL-08005"]},
  {"block": "ki-1", "mode": "text", "reason": "rule 6: two quotients side by side with units; the unit README delivery map names text", "sources": ["BC-SKL-08004"]},
  {"block": "ex-1", "mode": "step_reveal", "reason": "rule 1", "sources": []},
  {"block": "err-BC-ERR-99015", "mode": "step_reveal", "reason": "rule 1", "sources": []},
  {"block": "err-BC-ERR-99005", "mode": "step_reveal", "reason": "rule 1", "sources": []}
 ],
 "refresher": ["ki-1", "err-BC-ERR-99015", "err-BC-ERR-99005", "ex-1"],
 "read_minutes": {"full": 3.5, "brief": 3.0},
 "word_count": {"full": 512, "brief": 450},
 "research_lines": [
  {"file": "research/units/unit-08-applications-integration.md", "line": "An average rate of change carries the units of the function divided by the units of the input"}
 ],
 "inferred": [
  {"claim": "The part takes a 3.33 minute share of the 15.0 minute question, and a fluent solver holds the derivative in the head.", "settles": "Per-step timing data from the fluency telemetry."},
  {"claim": "BC-PT-99005 is earned on ex-1's final value with its equation but not tagged, to hold the brief band under 450 words.", "settles": "A brief band cap that admits two reader lines."},
  {"claim": "The lesson carries two checks: the bundle holds two errors, fewer than the three distractors a 4-option MCQ needs.", "settles": "A third active BC-ERR on BC-SKL-08004 or BC-SKL-08005."}
 ],
 "sources": ["BC-CON-08002", "BC-SKL-08004", "BC-SKL-08005", "BC-EK-CHA-4B1", "ced:152", "BC-QA-08002", "BC-QA-99007", "BC-QA-08001", "BC-QA-06015", "BC-QA-99009", "BC-PT-99021", "sg-25:4", "BC-ERR-99015", "BC-ERR-99005", "BC-MIS-99006", "BC-MIS-02008", "BC-PRQ-06005", "research/units/unit-08-applications-integration.md#8.1 Finding the Average Value of a Function on an Interval", "research/question-analysis/question-archetypes.md#BC-QA-08002 Instantaneous rate set equal to an average rate of change", "research/scoring/common-point-losses.md#Setup points", "research/scoring/common-point-losses.md#Units points", "research/exam/exam-structure.md#Section and part layout"]
}
```
