---
title: LSN-CON-08001 Average value of a function over an interval
research_date: 2026-09-29
status: designed
purpose: Authoring spec for the concept lesson on BC-CON-08001, the average value of a function as its definite integral over an interval divided by the interval length, built from authoring_bundle("BC-CON-08001") and the research files it cites, so an author fills plan 15's lesson record without making a teaching decision.
---

# LSN-CON-08001 Average value of a function over an interval

Concept BC-CON-08001 (skills BC-SKL-08001, BC-SKL-08002, BC-SKL-08003), topic 8.1 of Unit 8, first in the average value strand with no Unit 8 hard parent (docs/lessons/unit-08/README.md, section 1). Loaded by BC-QA-08001; the bundle also lists BC-QA-08002 and BC-QA-99007, which load BC-SKL-08003.

## Orientation

Served text, from BC-CON-08001 `description_plain` and the topic's Assessment behaviour paragraph (research/units/unit-08-applications-integration.md#8.1 Finding the Average Value of a Function on an Interval): a response writes the definite integral of the function over the stated interval, divides by the interval length, and reports three decimal places, with the setup shown before the calculator value. No count, no frequency.

## Key ideas

All three skills map to BC-EK-CHA-4B1 (ced:152), so one core block, both bands.

- ki-1 (core). Paraphrase of the Required mathematical knowledge paragraph: for f continuous on [a, b], the average value is the definite integral of f over [a, b] divided by b minus a; it carries the units of f; the integral alone is the accumulated amount; the quotient may be written in one line or two (sg-25:3). No anchor quote, to hold the brief band under its cap. Notation line from the concept record.

## Recognition

- BC-QA-08001 (family average-value, calculator; research/question-analysis/question-archetypes.md#BC-QA-08001 Average value of a function over an interval): `typical_wording` "find the average value of the function over the stated interval, showing the setup for your calculations"; `common_givens` a model function in a context and a closed interval; `asked_to_produce` an integral quotient, a decimal value, a sentence with units. The signal is the phrase "average value of" followed by the function's own name. Official parts: BC-FRQ-2015-Q3-D, 2019-Q1-B, 2019-Q2-B, 2021-Q1-D, 2022-Q1-B; MCQ BC-MCQ-PE2012-035, BC-MCQ-SAMPLE-009.
- BC-QA-99007 (family average-rate-of-change; research/question-analysis/question-archetypes.md#BC-QA-99007 Average rate of change reported on its own with units): "average rate of change of the modelling function", a difference quotient with units.
- BC-QA-08002 (family mean-value-theorem; research/question-analysis/question-archetypes.md#BC-QA-08002 Instantaneous rate set equal to an average rate of change): "the time at which the instantaneous rate of change equals its average rate of change".

What says "not this concept": the words "rate of change" after "average" (BC-CON-08002 and the two archetypes above), or "total" or "how much" with no division (topic 8.3).

## Method choice

Three strategy blocks, one per family, low band; st-1 also in mid. Every archetype carries `asked_to_produce` and `common_givens`, so none is tagged inferred.

- st-1, BC-QA-08001. Method, `expected_solution_path[0]`: write the definite integral of the function over the interval, then divide by its length. Rival, `wrong_approaches`: averaging the two endpoint values. Separating feature: "average value of f" asks about f across the whole interval, so an integral, not two samples.
- st-2, BC-QA-99007. Method: evaluate the function at both endpoints. Rival: integrating the function and dividing by the interval length. Separating feature: the words "rate of change".
- st-3, BC-QA-08002. Method: compute the average rate of change over the interval. Rival: reporting that rate itself as the time. Separating feature: the stem asks for an input value.

## Solution path

- ex-1, BC-QA-08001, both bands, calculator. Draw from `parameter_spec`: amplitude 5, shift 1, scale 2, length 3, context depth, framing bare, so \(W(t)=5\cos(t^2/2)+1\) on [0, 3]. The spec's constraints hold (5 > 1, 9 >= 8), and W changes sign inside the interval, as the spec's notes require. No published BC-QA-08001 item carries this draw (content/items_gen_unit08).
- Steps: the integral quotient (new, tagged BC-PT-99020), the calculator value to three places (evaluate, approx). A fluent solver writes both lines; the interval length is held in the head.

## Scoring

BC-QA-08001 lists BC-PT-99001, 99004, 99020 and 99003. ex-1 tags BC-PT-99020 on the setup line, and the line is `reader_checks(["BC-PT-99020"])` copied into the machine record. The answer point BC-PT-99004 is earned on step 2 but not tagged: its reader line would take the brief band past 450 words, so the tag is dropped and listed as inferred. Point losses the scoring research names: setup not shown before a calculator value (research/scoring/common-point-losses.md#Setup points, BC-ERR-99021); fewer than three decimals or an intermediate rounded before reuse (research/scoring/common-point-losses.md#Answer points, BC-ERR-99019). Unclear linkage between integral and answer kept both points in 2025 (sg-25:3) and cost one in 2023 (sg-23:4).

## Traps

Five active errors meet the skills; the first four in the bundle's order are served. Low band all four, mid band the first two. All on ex-1's draw.

- err-BC-ERR-06014: the absolute value integrated, against the signed integral. Possible reason, words from BC-MIS-08024.
- err-BC-ERR-08001: the integral reported with no division. Possible reason, words from BC-MIS-08002.
- err-BC-ERR-08002: limits [1, 3] and divisor 2, against [0, 3] and 3. No possible reason line: neither linked description names the interval choice for an average.
- err-BC-ERR-99019: the integral rounded to 5.9 before dividing. No possible reason line: the linked descriptions do not name rounding.

BC-ERR-99021 is the fifth and is not served (cap 4); st-1's first line carries its habit.

## Representations

None as a separate block. The topic's Representations paragraph names graph to signed area to average (BC-REP-02 to BC-REP-08); ki-1's figure carries it.

## Prerequisite bridge

- BC-PRQ-06005, BC-PRQ-06007, BC-PRQ-08006, each from its `description_plain` and `failure_signature`.

## Time

BC-QA-08001 is `calculator`, one part of the calculator active free response question, so Section II Part A, 15.0 minutes per question (research/exam/exam-structure.md#Section and part layout). The part is two points of nine, a 3.33 minute share (docs/lessons/unit-08/README.md, section 5) [inferred: settled by per-step timing data]. The minutes go on the written setup; the calculator value is typed, not derived.

## Checks

- chk-1, completion of ex-1, both bands: the setup is given, the student evaluates. Key 1.961.
- chk-2, isomorph, both bands. Draw: amplitude 4, shift -1, scale 1, length 2; \(W(t)=4\cos(t^2)-1\) on [0, 2]. Key -0.077.
- chk-3, MCQ, low band. Draw: amplitude 6, shift 1, scale 3, length 4; \(W(t)=6\cos(t^2/3)+1\) on [0, 4]. Key 2.153. Distractors: 4.391 (BC-ERR-06014), 8.610 (BC-ERR-08001), 2.150 (BC-ERR-99019, the integral rounded to 8.6).

## Delivery

- orientation: text. Rule 6, a statement of what a response shows; the figure is served once, on ki-1.
- ki-1: figure. Rule 4: BC-REP-02 and BC-REP-08 on BC-SKL-08002; the unit README's delivery map names the average value rectangle. Not promoted to interactive: BC-QA-08001 `difficulty_variables` vary a presentation form ("formula versus graph presentation"), not a quantity the stem reads [inferred; settled by the modality A/B].
- ex-1 and the four error blocks: step_reveal. Rule 1.

## Band plan

- Low (full): orientation, ki-1, st-1 to st-3, ex-1 with its scoring line, four error blocks, chk-1 to chk-3, three bridges. 635 words, 4.3 minutes (cap 900 and 6).
- Mid (brief): orientation, ki-1, st-1, ex-1 with its scoring line, err-BC-ERR-06014, err-BC-ERR-08001, chk-1, chk-2, three bridges. 421 words, 2.9 minutes (cap 450 and 3).
- Refresher: ki-1, the four error blocks, ex-1.

## Sources

- BC-CON-08001; BC-SKL-08001, BC-SKL-08002, BC-SKL-08003; BC-EK-CHA-4B1; ced:152
- BC-QA-08001, BC-QA-99007, BC-QA-08002; BC-PT-99020; sg-25:3, sg-23:4
- BC-ERR-06014, BC-ERR-08001, BC-ERR-08002, BC-ERR-99019, BC-ERR-99021; BC-MIS-08024, BC-MIS-08002
- BC-PRQ-06005, BC-PRQ-06007, BC-PRQ-08006
- research/units/unit-08-applications-integration.md#8.1 Finding the Average Value of a Function on an Interval
- research/question-analysis/question-archetypes.md#BC-QA-08001 Average value of a function over an interval
- research/question-analysis/question-archetypes.md#BC-QA-99007 Average rate of change reported on its own with units
- research/question-analysis/question-archetypes.md#BC-QA-08002 Instantaneous rate set equal to an average rate of change
- research/scoring/common-point-losses.md#Setup points
- research/scoring/common-point-losses.md#Answer points
- research/exam/exam-structure.md#Section and part layout
- [inferred] The 3.33 minute share and the written and held steps. Settled by per-step timing data.
- [inferred] ki-1 as a static figure. Settled by the modality A/B.
- [inferred] BC-PT-99004 untagged on ex-1 step 2 to hold the brief cap. Settled by a brief band cap that admits two reader lines.

## Machine record

```json
{
 "id": "LSN-CON-08001",
 "kind": "concept",
 "target_id": "BC-CON-08001",
 "unit": "08",
 "skills": ["BC-SKL-08001", "BC-SKL-08002", "BC-SKL-08003"],
 "orientation": {
  "text": "A response writes the integral of the function over the stated interval, divides by the interval length, and reports three decimal places, setup before the calculator value.",
  "sources": ["BC-CON-08001", "research/units/unit-08-applications-integration.md#8.1 Finding the Average Value of a Function on an Interval"]
 },
 "key_ideas": [
  {
   "id": "ki-1",
   "ek_id": "BC-EK-CHA-4B1",
   "depth": "core",
   "text": "For f continuous on [a, b], the average value is the integral of f over [a, b] divided by b minus a, in the units of f. The integral alone is the accumulated amount, not the average.",
   "notation": "average value of f on [a,b]",
   "quote": null,
   "sources": ["BC-EK-CHA-4B1", "ced:152", "sg-25:3", "research/units/unit-08-applications-integration.md#8.1 Finding the Average Value of a Function on an Interval"]
  }
 ],
 "strategy": [
  {
   "id": "st-1",
   "archetype_id": "BC-QA-08001",
   "cue": "Average value of a model function over a closed interval, setup shown.",
   "method": "First line: the integral over the interval, divided by its length.",
   "rival": "Rival: averaging the two endpoint values.",
   "separating_feature": "Average value of f means f across the whole interval: an integral, not two samples.",
   "sources": ["BC-QA-08001"],
   "evidence_tag": "verified"
  },
  {
   "id": "st-2",
   "archetype_id": "BC-QA-99007",
   "cue": "The stem asks for the average rate of change with units, from a modelling function and a closed interval.",
   "method": "First line: the function at both endpoints, their difference over the interval length.",
   "rival": "Rival: integrating the function and dividing by the interval length.",
   "separating_feature": "The words rate of change select the difference quotient.",
   "sources": ["BC-QA-99007"],
   "evidence_tag": "verified"
  },
  {
   "id": "st-3",
   "archetype_id": "BC-QA-08002",
   "cue": "The stem asks when the instantaneous rate equals the average rate of change, from a model and its derivative.",
   "method": "First line: the average rate of change over the interval.",
   "rival": "Rival: reporting that rate itself as the time.",
   "separating_feature": "The answer is an input on the interval, solved from the derivative equal to that rate.",
   "sources": ["BC-QA-08002"],
   "evidence_tag": "verified"
  }
 ],
 "worked_examples": [
  {
   "id": "ex-1",
   "archetype_id": "BC-QA-08001",
   "bands": ["low", "mid"],
   "parameter_draw": {"amplitude": 5, "shift": 1, "scale": 2, "length": 3, "context": "depth", "framing": "bare"},
   "problem": {"text": "W(t) = 5cos(t^2/2) + 1. With a calculator, find the average value of W on [0, 3], showing the setup.", "command_verb": "find"},
   "calculator_status": "calculator",
   "steps": [
    {"cue": "Average value of W on [0, 3]: integral, divided by the length 3.", "why": "The formula point needs the integral and the division shown.", "expr": "Integral(5*cos(t**2/2) + 1, (t, 0, 3))/3", "relation": "new", "point_type_id": "BC-PT-99020"},
    {"cue": "Setup written, so the calculator evaluates it.", "why": "Three places. Where W is negative, that part subtracts.", "expr": "1.961", "relation": "evaluate", "subs": {}, "approx": true}
   ],
   "answer": {"form": "numeric", "expr": "1.961"}
  }
 ],
 "what_a_reader_scores": [
  {"example_id": "ex-1", "point_type_ids": ["BC-PT-99020"], "lines": [{"point_type_id": "BC-PT-99020", "text": "Average value formula. Earned by: The definite integral over the interval together with evidence of division by the interval length; a correct answer alongside a correct integral counts as that evidence (sg-25:3, sg-26:9). Not earned by: An integral with the wrong integrand, such as the derivative in place of the function (crabbc-25:3); a formula divided by the wrong length (sg-22:3). Notation: Differential optional (sg-26:9). The formula may be presented in one step or across several (sg-25:3, sg-22:3)."}]}
 ],
 "common_errors": [
  {
   "error_id": "BC-ERR-06014",
   "observed_behavior": "Every piece of the region is added with a positive sign, so a signed integral is reported as a plain area.",
   "scoring_consequence": "The value point is lost, and any later part that imports the value inherits the error.",
   "wrong_step": {"text": "The absolute value integrated.", "expr": "Integral(Abs(5*cos(t**2/2) + 1), (t, 0, 3))/3"},
   "right_step": {"text": "The signed integral.", "expr": "Integral(5*cos(t**2/2) + 1, (t, 0, 3))/3"},
   "relation": "distinct",
   "possible_reason": {"misconception_id": "BC-MIS-08024", "text": "reads every definite integral as area under a graph"},
   "sources": ["BC-ERR-06014", "BC-MIS-08024"]
  },
  {
   "error_id": "BC-ERR-08001",
   "observed_behavior": "The response presents the correct definite integral and reports its value as the average.",
   "scoring_consequence": "The average value point is lost unless the correct answer appears elsewhere as evidence of the division (sg-25:3).",
   "wrong_step": {"text": "No division.", "expr": "Integral(5*cos(t**2/2) + 1, (t, 0, 3))"},
   "right_step": {"text": "Divided by 3.", "expr": "Integral(5*cos(t**2/2) + 1, (t, 0, 3))/3"},
   "relation": "distinct",
   "possible_reason": {"misconception_id": "BC-MIS-08002", "text": "sees the integral as the averaging operation itself"},
   "sources": ["BC-ERR-08001", "BC-MIS-08002"]
  },
  {
   "error_id": "BC-ERR-08002",
   "observed_behavior": "The limits of the average value integral, or the divisor, come from an interval other than the one the prompt states.",
   "scoring_consequence": "Both the setup point and the answer point are lost.",
   "wrong_step": {"text": "Over [1, 3].", "expr": "Integral(5*cos(t**2/2) + 1, (t, 1, 3))/2"},
   "right_step": {"text": "Over [0, 3].", "expr": "Integral(5*cos(t**2/2) + 1, (t, 0, 3))/3"},
   "relation": "distinct",
   "possible_reason": null,
   "sources": ["BC-ERR-08002"]
  },
  {
   "error_id": "BC-ERR-99019",
   "observed_behavior": "Responses report fewer than three digits after the decimal point, round an intermediate value before it is used again, or read a value off a trace rather than solving for it.",
   "scoring_consequence": "The answer point is not earned; the report notes this recurs across several parts of the same response.",
   "wrong_step": {"text": "5.9 divided by 3.", "expr": "5.9/3"},
   "right_step": {"text": "Full precision, then 1.961.", "expr": "1.961"},
   "relation": "distinct",
   "possible_reason": null,
   "sources": ["BC-ERR-99019"]
  }
 ],
 "representations": null,
 "prerequisite_bridges": [
  {"prq_id": "BC-PRQ-06005", "text": "W(t) is the value of W at input t; a value read at the wrong input changes the integral."},
  {"prq_id": "BC-PRQ-06007", "text": "From a graph: signed sums of rectangle, triangle, trapezoid and semicircle areas."},
  {"prq_id": "BC-PRQ-08006", "text": "Full precision until the last line, then three places."}
 ],
 "time": {"exam_part": "II-A", "budget_minutes": 15.0, "source": "research/exam/exam-structure.md#Section and part layout", "written_steps": {"ex-1": [1, 2]}, "skipped_steps": {"ex-1": []}},
 "checks": [
  {
   "id": "chk-1",
   "check_kind": "completion",
   "format": "short_answer",
   "bands": ["low", "mid"],
   "archetype_id": "BC-QA-08001",
   "parameter_draw": {"amplitude": 5, "shift": 1, "scale": 2, "length": 3, "context": "depth", "framing": "bare"},
   "completes": "ex-1",
   "stem": {"text": "Evaluate (1/3) times the integral of 5cos(t^2/2) + 1 from 0 to 3, to three places.", "command_verb": "evaluate"},
   "key": {"form": "numeric", "expr": "1.961"},
   "steps": [
    {"text": "The setup.", "expr": "Integral(5*cos(t**2/2) + 1, (t, 0, 3))/3", "relation": "new"},
    {"text": "Calculator.", "expr": "1.961", "relation": "evaluate", "subs": {}, "approx": true}
   ],
   "calculator_status": "calculator",
   "skills": ["BC-SKL-08003"]
  },
  {
   "id": "chk-2",
   "check_kind": "isomorph",
   "format": "short_answer",
   "bands": ["low", "mid"],
   "archetype_id": "BC-QA-08001",
   "parameter_draw": {"amplitude": 4, "shift": -1, "scale": 1, "length": 2, "context": "flow", "framing": "bare"},
   "stem": {"text": "W(t) = 4cos(t^2) - 1. Find the average value of W on [0, 2], with the setup.", "command_verb": "find"},
   "key": {"form": "numeric", "expr": "-0.077"},
   "steps": [
    {"text": "The setup.", "expr": "Integral(4*cos(t**2) - 1, (t, 0, 2))/2", "relation": "new"},
    {"text": "Calculator.", "expr": "-0.077", "relation": "evaluate", "subs": {}, "approx": true}
   ],
   "calculator_status": "calculator",
   "skills": ["BC-SKL-08001", "BC-SKL-08003"]
  },
  {
   "id": "chk-3",
   "check_kind": "mcq",
   "format": "mcq",
   "bands": ["low"],
   "archetype_id": "BC-QA-08001",
   "parameter_draw": {"amplitude": 6, "shift": 1, "scale": 3, "length": 4, "context": "temperature", "framing": "bare"},
   "stem": {"text": "Let W(t) = 6cos(t^2/3) + 1. Which is the average value of W on [0, 4]?", "command_verb": "identify"},
   "key": {"form": "numeric", "expr": "2.153"},
   "steps": [
    {"text": "The setup.", "expr": "Integral(6*cos(t**2/3) + 1, (t, 0, 4))/4", "relation": "new"},
    {"text": "Calculator.", "expr": "2.153", "relation": "evaluate", "subs": {}, "approx": true}
   ],
   "options": [
    {"id": "A", "is_key": false, "expr": "4.391", "error_path": "BC-ERR-06014", "derivation": "the integral of the absolute value of W divided by 4"},
    {"id": "B", "is_key": true, "expr": "2.153", "error_path": null},
    {"id": "C", "is_key": false, "expr": "8.610", "error_path": "BC-ERR-08001", "derivation": "the integral reported with no division by 4"},
    {"id": "D", "is_key": false, "expr": "2.150", "error_path": "BC-ERR-99019", "derivation": "the integral rounded to 8.6 before dividing by 4"}
   ],
   "calculator_status": "calculator",
   "skills": ["BC-SKL-08001", "BC-SKL-08003"]
  }
 ],
 "delivery": [
  {"block": "orientation", "mode": "text", "reason": "rule 6: a statement of what a response shows; the figure is served once, on ki-1", "sources": ["BC-SKL-08001"]},
  {"block": "ki-1", "mode": "figure", "reason": "rule 4: BC-REP-02 and BC-REP-08 on BC-SKL-08002; the unit README delivery map names the average value rectangle; not promoted, BC-QA-08001 difficulty_variables vary a presentation form", "sources": ["BC-SKL-08002", "BC-QA-08001"],
   "spec": {"kind": "graph", "representations": ["BC-REP-02", "BC-REP-08"], "window": {"x": [0, 3], "y": [-5, 7]},
    "curves": [{"expr": "5*cos(t**2/2) + 1", "domain": [0, 3]}],
    "shaded": [{"between": ["5*cos(t**2/2) + 1", "0"], "domain": [0, 3], "signed": true}],
    "rectangles": [{"from": 0, "to": 3, "height": 1.961}],
    "labels": [{"text": "W(t)", "placement": "inside"}, {"text": "rectangle height 1.961: the average value", "placement": "inside"}, {"text": "same signed area as the region", "placement": "inside"}]},
   "fallback": "the same figure, static, with the three labels inside and a one line text description beneath", "keyboard": "no control; the figure description is reached with Tab"},
  {"block": "ex-1", "mode": "step_reveal", "reason": "rule 1", "sources": []},
  {"block": "err-BC-ERR-06014", "mode": "step_reveal", "reason": "rule 1", "sources": []},
  {"block": "err-BC-ERR-08001", "mode": "step_reveal", "reason": "rule 1", "sources": []},
  {"block": "err-BC-ERR-08002", "mode": "step_reveal", "reason": "rule 1", "sources": []},
  {"block": "err-BC-ERR-99019", "mode": "step_reveal", "reason": "rule 1", "sources": []}
 ],
 "refresher": ["ki-1", "err-BC-ERR-06014", "err-BC-ERR-08001", "err-BC-ERR-08002", "err-BC-ERR-99019", "ex-1"],
 "read_minutes": {"full": 4.3, "brief": 2.9},
 "word_count": {"full": 635, "brief": 421},
 "research_lines": [
  {"file": "research/units/unit-08-applications-integration.md", "line": "the average value of f over [a,b] is the definite integral of f over [a,b] divided by b minus a"}
 ],
 "inferred": [
  {"claim": "The average value part takes a 3.33 minute share of the 15.0 minute question, and a fluent solver writes both lines of ex-1.", "settles": "Per-step timing data from the fluency telemetry."},
  {"claim": "ki-1 is served as a static figure of the average value rectangle.", "settles": "The modality A/B in the build plan: skip rate and time to first credited success by mode."},
  {"claim": "BC-PT-99004 is earned on ex-1 step 2 but not tagged, because its reader line would take the brief band past 450 words.", "settles": "A brief band cap that admits two reader lines, or a shorter BC-PT-99004 reader line."}
 ],
 "sources": ["BC-CON-08001", "BC-SKL-08001", "BC-SKL-08002", "BC-SKL-08003", "BC-EK-CHA-4B1", "ced:152", "BC-QA-08001", "BC-QA-99007", "BC-QA-08002", "BC-PT-99020", "sg-25:3", "sg-23:4", "BC-ERR-06014", "BC-ERR-08001", "BC-ERR-08002", "BC-ERR-99019", "BC-ERR-99021", "BC-MIS-08024", "BC-MIS-08002", "BC-PRQ-06005", "BC-PRQ-06007", "BC-PRQ-08006", "research/units/unit-08-applications-integration.md#8.1 Finding the Average Value of a Function on an Interval", "research/question-analysis/question-archetypes.md#BC-QA-08001 Average value of a function over an interval", "research/scoring/common-point-losses.md#Setup points", "research/scoring/common-point-losses.md#Answer points", "research/exam/exam-structure.md#Section and part layout"]
}
```
