---
title: LSN-CON-06013 Average value of a function
research_date: 2026-09-29
status: designed
purpose: Authoring spec for the concept lesson on BC-CON-06013, the average value of a function as the integral over an interval divided by the interval's length, built from authoring_bundle("BC-CON-06013") and the research files it cites, so an author fills plan 15's lesson record without making a teaching decision.
---

# LSN-CON-06013 Average value of a function

Concept BC-CON-06013 (one skill, BC-SKL-06038), topic 6.7 of Unit 6, loaded by BC-QA-06015 (accumulation-interpretation) and BC-QA-08001 (average-value); neither carries BC-SKL-06038 first, so the bundle names no primary archetype. The retired Unit 6 average value archetype is superseded by BC-QA-08001 (docs/lessons/unit-06/README.md, section 2). Hard parent BC-CON-06012.

## Orientation

Served text, from BC-CON-06013 `description_plain` and the topic's Assessment behaviour paragraph (research/units/unit-06-integration-accumulation.md#6.7 The Fundamental Theorem of Calculus and Definite Integrals): a response writes the integral over the interval divided by the interval's length, evaluates it, and describes the result as an average over that interval. No count, no frequency.

## Key ideas

BC-SKL-06038 maps to BC-EK-FUN-6B3 (ced:124): one core block, both bands.

- ki-1 (core). Paraphrase of "Net change and average value": the average value of f over [a, b] is one over (b - a) times the integral of f from a to b, the accumulated amount spread over the interval's length. No anchor quote: the EK text on ced:124 is extracted with broken spacing around the integral. Notation line from the concept record.

## Recognition

- BC-QA-08001 (research/question-analysis/question-archetypes.md#BC-QA-08001 Average value of a function over an interval): `typical_wording` "find the average value of the modelled quantity over the stated time interval and show the setup"; `common_givens` a model function in a context, a closed interval; `asked_to_produce` an integral quotient, a decimal value, a sentence with units. Signal: the words "average value" and an interval. Shapes: the calculator FRQ (BC-FRQ-2019-Q1-B, BC-FRQ-2021-Q1-D, BC-FRQ-2022-Q1-B) and MCQ (BC-MCQ-SAMPLE-009).
- BC-QA-06015 (research/question-analysis/question-archetypes.md#BC-QA-06015 Interpreting a definite integral in context with units): a displayed expression to interpret; a factor 1/(b - a) in front makes it an average.

What says "not this concept": "average rate of change" asks for a difference quotient; "how much accumulated" asks for the integral alone (BC-CON-06012) (docs/lessons/unit-06/README.md, section 3).

## Method choice

Two strategy blocks; st-1 serves both bands.

- st-1, BC-QA-08001. Method, `expected_solution_path[0]` and [1]: the definite integral over the interval, divided by the interval's length. Rival from `wrong_approaches`: averaging the two endpoint values. Separating feature: the average of every value on the interval needs the integral.
- st-2, BC-QA-06015. Method, `expected_solution_path[0]`: identify what the integrand measures per unit input. Rival: naming the quantity without the interval. Separating feature: the limits name the interval, and a factor 1/(b - a) makes it an average.

## Solution path

- ex-1, BC-QA-08001, both bands, calculator. Draw from `parameter_spec`: amplitude 4, shift 1, scale 2, length 3, context temperature, framing context; constraints hold (4 > 1, 9 at least 8). W(t) = 4 cos(t^2/2) + 1 on [0, 3]; average 1.769. No published BC-QA-08001 item carries this draw.
- Steps follow `expected_solution_path`: the quotient written (new, tagged BC-PT-99020), the calculator value to three places (evaluate, approx, tagged BC-PT-99004). A fluent solver writes both lines; nothing is held.

## Scoring

BC-QA-08001 lists BC-PT-99001, 99004, 99020, 99003. ex-1 tags BC-PT-99020 on the quotient and BC-PT-99004 on the value; their reader_checks lines are in the machine record. Two points: the integral with evidence of division, and the value to three decimal places (sg-25:3); a correct integral with a correct quotient value earns both even with unclear linkage (sg-25:3). The interpretation must say average over the interval (BC-QA-06015 `scoring_pattern`, sg-24:3; research/scoring/common-point-losses.md#Interpretation points).

## Traps

Four active errors meet the skill, in the bundle's order: BC-ERR-06016, BC-ERR-06030, BC-ERR-99015 (linked BC-MIS at severity high), BC-ERR-06032 (no linked BC-MIS). Mid band: the first two. All on ex-1's draw.

- err-BC-ERR-06016: the integral 5.306 with no division, against 1.769. Possible reason, words from BC-MIS-06014.
- err-BC-ERR-06030: the quotient described as the total. The wrong expression is the integral, the right one the quotient. Possible reason, words from BC-MIS-06014.
- err-BC-ERR-99015: the difference quotient (W(3) - W(0))/3. Possible reason, words from BC-MIS-99006.
- err-BC-ERR-06032: cos evaluated in degrees. No possible reason: the record links no BC-MIS.

## Representations

None.

## Prerequisite bridge

None.

## Time

BC-QA-08001 is `calculator`, one part of the calculator FRQ or a single MCQ; the lesson takes the FRQ shape, Section II Part A, 15.0 minutes per question (research/exam/exam-structure.md#Section and part layout), two points, about 3.33 minutes (docs/lessons/unit-06/README.md, section 5) [inferred]. The minutes go on the quotient line and the three-place value.

## Checks

- chk-1, completion of ex-1, both bands: the quotient is given; the student evaluates. Key 1.769.
- chk-2, isomorph, both bands. Draw: amplitude 3, shift -1, scale 2, length 3.5. Key -0.297.
- chk-3, MCQ, low band. Draw: amplitude 6, shift 2, scale 3, length 4. Key 3.153. Distractors: 12.610 (BC-ERR-06016), -0.627 (BC-ERR-99015), 7.995 (BC-ERR-06032).

## Delivery

- orientation, ki-1: text. Rule 6: BC-REP-01, 05 and 09 on BC-SKL-06038, none figure-bearing (docs/lessons/unit-06/README.md, section 6).
- ex-1 and the four error blocks: step_reveal. Rule 1.

## Band plan

- Low (full): orientation, ki-1, st-1, st-2, ex-1 with its scoring lines, the four error blocks, chk-1 to chk-3. 600 words, 4.0 minutes (cap 900 and 6).
- Mid (brief): orientation, ki-1, st-1, ex-1 with its scoring lines, err-BC-ERR-06016, err-BC-ERR-06030, chk-1, chk-2. 445 words, 3.0 minutes (cap 450 and 3).
- Refresher: ki-1, the four error blocks, ex-1.

## Sources

- BC-CON-06013; BC-SKL-06038; BC-EK-FUN-6B3; ced:124
- BC-QA-08001, BC-QA-06015; BC-PT-99020, BC-PT-99004; sg-25:3, sg-24:3
- BC-ERR-06016, BC-ERR-06030, BC-ERR-99015, BC-ERR-06032; BC-MIS-06014, BC-MIS-99006
- research/units/unit-06-integration-accumulation.md#6.7 The Fundamental Theorem of Calculus and Definite Integrals
- research/question-analysis/question-archetypes.md#BC-QA-08001 Average value of a function over an interval
- research/question-analysis/question-archetypes.md#BC-QA-06015 Interpreting a definite integral in context with units
- research/scoring/common-point-losses.md#Interpretation points
- research/exam/exam-structure.md#Section and part layout
- [inferred] BC-QA-08001 taken as the time archetype, since no archetype carries BC-SKL-06038 first. Settled by a primary archetype for BC-SKL-06038.
- [inferred] The 3.33 minute share of the two-point part. Settled by timing data per part.

## Machine record

```json
{
 "id": "LSN-CON-06013",
 "kind": "concept",
 "target_id": "BC-CON-06013",
 "unit": "06",
 "skills": ["BC-SKL-06038"],
 "orientation": {
  "text": "A response writes the integral over the interval divided by the interval's length, evaluates it, and calls the result an average over that interval.",
  "sources": ["BC-CON-06013", "research/units/unit-06-integration-accumulation.md#6.7 The Fundamental Theorem of Calculus and Definite Integrals"]
 },
 "key_ideas": [
  {
   "id": "ki-1",
   "ek_id": "BC-EK-FUN-6B3",
   "depth": "core",
   "text": "The average value of f on [a, b] is 1/(b - a) times the integral of f from a to b: the accumulated amount spread evenly over the interval's length.",
   "notation": "1/(b-a) times integral from a to b",
   "quote": null,
   "sources": ["BC-EK-FUN-6B3", "ced:124", "research/units/unit-06-integration-accumulation.md#6.7 The Fundamental Theorem of Calculus and Definite Integrals"]
  }
 ],
 "strategy": [
  {
   "id": "st-1",
   "archetype_id": "BC-QA-08001",
   "cue": "Average value of a model over a stated interval, setup shown.",
   "method": "First line: the integral over the interval, divided by its length.",
   "rival": "Rival: the two endpoint values averaged.",
   "separating_feature": "Every value on the interval counts, so an integral.",
   "sources": ["BC-QA-08001"],
   "evidence_tag": "verified"
  },
  {
   "id": "st-2",
   "archetype_id": "BC-QA-06015",
   "cue": "A displayed integral of a contextual rate; its meaning with units asked.",
   "method": "First line: what the integrand measures per unit input.",
   "rival": "Rival: the quantity named without the interval.",
   "separating_feature": "The limits name the interval; a factor 1/(b - a) makes it an average.",
   "sources": ["BC-QA-06015"],
   "evidence_tag": "verified"
  }
 ],
 "worked_examples": [
  {
   "id": "ex-1",
   "archetype_id": "BC-QA-08001",
   "bands": ["low", "mid"],
   "parameter_draw": {"amplitude": 4, "shift": 1, "scale": 2, "length": 3, "context": "temperature", "framing": "context"},
   "problem": {"text": "A temperature is W(t) = 4 cos(t^2/2) + 1 degrees for 0 <= t <= 3 hours. Find its average value, showing the setup.", "command_verb": "find"},
   "calculator_status": "calculator",
   "steps": [
    {"cue": "Average value over [0, 3].", "why": "Integral over the interval, divided by length 3.", "expr": "(1/3)*Integral(4*cos(t**2/2) + 1, (t, 0, 3))", "relation": "new", "point_type_id": "BC-PT-99020"},
    {"cue": "Calculator allowed.", "why": "Radian mode, three places.", "expr": "1.769", "relation": "evaluate", "subs": {}, "approx": true, "point_type_id": "BC-PT-99004"}
   ],
   "answer": {"form": "numeric", "expr": "1.769"}
  }
 ],
 "what_a_reader_scores": [
  {"example_id": "ex-1", "point_type_ids": ["BC-PT-99020", "BC-PT-99004"], "lines": [
   {"point_type_id": "BC-PT-99020", "text": "Average value formula. Earned by: The definite integral over the interval together with evidence of division by the interval length; a correct answer alongside a correct integral counts as that evidence (sg-25:3, sg-26:9). Not earned by: An integral with the wrong integrand, such as the derivative in place of the function (crabbc-25:3); a formula divided by the wrong length (sg-22:3). Notation: Differential optional (sg-26:9). The formula may be presented in one step or across several (sg-25:3, sg-22:3)."},
   {"point_type_id": "BC-PT-99004", "text": "Answer with or without supporting work. Earned by: The correct value on its own, with no supporting work required (sg-25:3, sg-26:4). Not earned by: A value outside the accepted precision, or a value inconsistent with a required earlier step where the rubric imposes one. Precision: A reported decimal answer must be accurate to three places after the decimal point, rounded or truncated; at most one point per question is lost to inappropriate rounding (sg-25:2, sg-26:2). sg-26:4 also accepts a stated rounding to the nearest integer and several truncations."}
  ]}
 ],
 "common_errors": [
  {
   "error_id": "BC-ERR-06016",
   "observed_behavior": "The definite integral is presented as the average value with no division by the length of the interval.",
   "scoring_consequence": "The average value formula point is lost; a correct integral together with the correct quotient value earns both points even when the linkage is unclear (sg-25:3).",
   "wrong_step": {"text": "No division.", "expr": "Integral(4*cos(t**2/2) + 1, (t, 0, 3))"},
   "right_step": {"text": "Divided by 3.", "expr": "(1/3)*Integral(4*cos(t**2/2) + 1, (t, 0, 3))"},
   "relation": "distinct",
   "possible_reason": {"misconception_id": "BC-MIS-06014", "text": "does not separate the integral from the integral divided by the interval length"},
   "sources": ["BC-ERR-06016", "BC-MIS-06014"]
  },
  {
   "error_id": "BC-ERR-06030",
   "observed_behavior": "A displayed average value expression is described as the total amount accumulated over the interval.",
   "scoring_consequence": "The interpretation point is not earned because the description must say average over the interval (sg-24:3).",
   "wrong_step": {"text": "Total over 0 to 3 hours.", "expr": "Integral(4*cos(t**2/2) + 1, (t, 0, 3))"},
   "right_step": {"text": "Average degrees over 0 to 3 hours.", "expr": "(1/3)*Integral(4*cos(t**2/2) + 1, (t, 0, 3))"},
   "relation": "distinct",
   "possible_reason": {"misconception_id": "BC-MIS-06014", "text": "the two expressions are described and computed interchangeably"},
   "sources": ["BC-ERR-06030", "BC-MIS-06014"]
  },
  {
   "error_id": "BC-ERR-99015",
   "observed_behavior": "Responses compute a difference quotient where the average value of a function was asked, or integrate the derivative instead of the function, or divide by the wrong quantity.",
   "scoring_consequence": "The setup point is not earned and the numerical answer point follows it.",
   "wrong_step": {"text": "(W(3) - W(0))/3.", "expr": "(4*cos(9/2) + 1 - 5)/3"},
   "right_step": {"text": "The integral quotient.", "expr": "(1/3)*Integral(4*cos(t**2/2) + 1, (t, 0, 3))"},
   "relation": "distinct",
   "possible_reason": {"misconception_id": "BC-MIS-99006", "text": "a difference quotient is offered for an average value"},
   "sources": ["BC-ERR-99015", "BC-MIS-99006"]
  },
  {
   "error_id": "BC-ERR-06032",
   "observed_behavior": "Numerical values of an integral or of a rate involving a trigonometric function are computed in degree mode.",
   "scoring_consequence": "The first point that the value would otherwise earn is not earned, and the response remains eligible for subsequent points (sg-23:4).",
   "wrong_step": {"text": "Degree mode.", "expr": "(1/3)*Integral(4*cos(pi*t**2/360) + 1, (t, 0, 3))"},
   "right_step": {"text": "Radian mode.", "expr": "(1/3)*Integral(4*cos(t**2/2) + 1, (t, 0, 3))"},
   "relation": "distinct",
   "possible_reason": null,
   "sources": ["BC-ERR-06032"]
  }
 ],
 "representations": null,
 "prerequisite_bridges": [],
 "time": {"exam_part": "II-A", "budget_minutes": 15.0, "source": "research/exam/exam-structure.md#Section and part layout", "written_steps": {"ex-1": [1, 2]}, "skipped_steps": {"ex-1": []}},
 "checks": [
  {
   "id": "chk-1",
   "check_kind": "completion",
   "format": "short_answer",
   "bands": ["low", "mid"],
   "archetype_id": "BC-QA-08001",
   "parameter_draw": {"amplitude": 4, "shift": 1, "scale": 2, "length": 3, "context": "temperature", "framing": "context"},
   "completes": "ex-1",
   "stem": {"text": "Evaluate (1/3) times the integral from 0 to 3 of W(t) dt.", "command_verb": "evaluate"},
   "key": {"form": "numeric", "expr": "1.769"},
   "steps": [
    {"text": "The quotient.", "expr": "(1/3)*Integral(4*cos(t**2/2) + 1, (t, 0, 3))", "relation": "new"},
    {"text": "Calculator.", "expr": "1.769", "relation": "evaluate", "subs": {}, "approx": true}
   ],
   "calculator_status": "calculator",
   "skills": ["BC-SKL-06038"]
  },
  {
   "id": "chk-2",
   "check_kind": "isomorph",
   "format": "short_answer",
   "bands": ["low", "mid"],
   "archetype_id": "BC-QA-08001",
   "parameter_draw": {"amplitude": 3, "shift": -1, "scale": 2, "length": 3.5, "context": "depth", "framing": "bare"},
   "stem": {"text": "W(t) = 3 cos(t^2/2) - 1. Find its average value on [0, 3.5].", "command_verb": "find"},
   "key": {"form": "numeric", "expr": "-0.297"},
   "steps": [
    {"text": "The quotient.", "expr": "(1/(7/2))*Integral(3*cos(t**2/2) - 1, (t, 0, 7/2))", "relation": "new"},
    {"text": "Calculator.", "expr": "-0.297", "relation": "evaluate", "subs": {}, "approx": true}
   ],
   "calculator_status": "calculator",
   "skills": ["BC-SKL-06038"]
  },
  {
   "id": "chk-3",
   "check_kind": "mcq",
   "format": "mcq",
   "bands": ["low"],
   "archetype_id": "BC-QA-08001",
   "parameter_draw": {"amplitude": 6, "shift": 2, "scale": 3, "length": 4, "context": "flow", "framing": "bare"},
   "stem": {"text": "The average value of W(t) = 6 cos(t^2/3) + 2 on [0, 4] is", "command_verb": "identify"},
   "key": {"form": "numeric", "expr": "3.153"},
   "steps": [
    {"text": "The quotient.", "expr": "(1/4)*Integral(6*cos(t**2/3) + 2, (t, 0, 4))", "relation": "new"},
    {"text": "Calculator.", "expr": "3.153", "relation": "evaluate", "subs": {}, "approx": true}
   ],
   "options": [
    {"id": "A", "is_key": false, "expr": "-0.627", "error_path": "BC-ERR-99015", "derivation": "(W(4) - W(0))/4, a difference quotient"},
    {"id": "B", "is_key": true, "expr": "3.153", "error_path": null},
    {"id": "C", "is_key": false, "expr": "7.995", "error_path": "BC-ERR-06032", "derivation": "the quotient evaluated in degree mode"},
    {"id": "D", "is_key": false, "expr": "12.610", "error_path": "BC-ERR-06016", "derivation": "the integral with no division by 4"}
   ],
   "calculator_status": "calculator",
   "skills": ["BC-SKL-06038"]
  }
 ],
 "delivery": [
  {"block": "orientation", "mode": "text", "reason": "rule 6: BC-REP-01, 05 and 09 on BC-SKL-06038, none figure-bearing", "sources": ["BC-SKL-06038"]},
  {"block": "ki-1", "mode": "text", "reason": "rule 6: a formula, BC-REP-01", "sources": ["BC-SKL-06038"]},
  {"block": "ex-1", "mode": "step_reveal", "reason": "rule 1", "sources": []},
  {"block": "err-BC-ERR-06016", "mode": "step_reveal", "reason": "rule 1", "sources": []},
  {"block": "err-BC-ERR-06030", "mode": "step_reveal", "reason": "rule 1", "sources": []},
  {"block": "err-BC-ERR-99015", "mode": "step_reveal", "reason": "rule 1", "sources": []},
  {"block": "err-BC-ERR-06032", "mode": "step_reveal", "reason": "rule 1", "sources": []}
 ],
 "refresher": ["ki-1", "err-BC-ERR-06016", "err-BC-ERR-06030", "err-BC-ERR-99015", "err-BC-ERR-06032", "ex-1"],
 "read_minutes": {"full": 4.0, "brief": 3.0},
 "word_count": {"full": 600, "brief": 445},
 "research_lines": [
  {"file": "research/units/unit-06-integration-accumulation.md", "line": "the average value of f over [a,b] is one over (b minus a) times that integral"}
 ],
 "inferred": [
  {"claim": "BC-QA-08001 is taken as the worked example and time archetype, since neither loading archetype carries BC-SKL-06038 first.", "settles": "A primary archetype for BC-SKL-06038 in the library."},
  {"claim": "The two-point average value part takes about 3.33 of the 15.0 Section II minutes.", "settles": "Timing data per part once the fluency telemetry exists."}
 ],
 "sources": ["BC-CON-06013", "BC-SKL-06038", "BC-EK-FUN-6B3", "ced:124", "BC-QA-08001", "BC-QA-06015", "BC-PT-99020", "BC-PT-99004", "sg-25:3", "sg-24:3", "BC-ERR-06016", "BC-ERR-06030", "BC-ERR-99015", "BC-ERR-06032", "BC-MIS-06014", "BC-MIS-99006", "research/units/unit-06-integration-accumulation.md#6.7 The Fundamental Theorem of Calculus and Definite Integrals", "research/question-analysis/question-archetypes.md#BC-QA-08001 Average value of a function over an interval", "research/exam/exam-structure.md#Section and part layout"]
}
```
