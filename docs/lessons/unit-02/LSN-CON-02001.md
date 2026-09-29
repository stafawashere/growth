---
title: LSN-CON-02001 Average rate of change as a difference quotient
research_date: 2026-09-29
status: designed
purpose: Authoring spec for the concept lesson on BC-CON-02001, the average rate of change as a difference quotient, built from authoring_bundle("BC-CON-02001") and the research files it cites, so an author fills plan 15's lesson record without making a teaching decision.
---

# LSN-CON-02001 Average rate of change as a difference quotient

Concept BC-CON-02001 (skills BC-SKL-02001, BC-SKL-02002, BC-SKL-02003), topic 2.1 of Unit 2, loaded by BC-QA-02014 (listed first in the bundle) and BC-QA-04002. It is a root of the unit (docs/lessons/unit-02/README.md section 1), so no Unit 2 concept precedes it.

## Prediction

One multiple choice question on worked example 1's own numbers, asked before the rule is shown: the runner covered 31 meters by minute 3 and 52 meters by minute 8, and the student picks the expression that gives the average rate over \(3\le t\le 8\). The key is the quotient, whose value is ex-1's answer; the distractors are the bare difference (BC-ERR-02001) and the mean of the two readings. The resolution, shown on the key idea screen beside the student's choice, states the quotient and its value with units. No verdict word. Sources: BC-CON-02001 and the topic 2.1 section the key idea cites.

## Orientation

Served text (26 words), from BC-CON-02001 `description_plain` and the topic's Assessment behaviour paragraph (research/units/unit-02-differentiation-definition-properties.md#2.1 Defining Average and Instantaneous Rates of Change at a Point): a response shows the change in the output divided by the change in the input, uses the two values the interval names, and carries the compound units of a rate; a difference alone is not a rate (sg-25:11, sg-24:2). No count, no frequency.

## Key ideas

The three skills all map BC-EK-CHA-2A1 (ced:60), so one core block, both bands.

- ki-1 (core). The two difference quotients, paraphrased from the topic's Required mathematical knowledge paragraph, and the units rule from topic 2.3's Units paragraph (research/units/unit-02-differentiation-definition-properties.md#2.3 Estimating Derivatives of a Function at a Point): both quotients divide a change in output by the matching change in input; from a table the interval names the two rows. No anchor quote (the ced:60 wording is the citation in `sources`). Notation line from the concept record: difference quotient.

## Recognition

- BC-QA-04002 (family derivative-from-table; research/question-analysis/question-archetypes.md#BC-QA-04002 Approximating a derivative from a table with units): `typical_wording` "approximate the derivative at the stated input using the average rate of change over the named interval; show the work and indicate units of measure"; `common_givens` a table of values of a contextual quantity and the interval; `asked_to_produce` a difference and a quotient, and units of measure. The signal is a named interval with two endpoints in a table. It is the opening part of table based FRQs: BC-FRQ-2021-Q1-A, BC-FRQ-2022-Q4-A, BC-FRQ-2024-Q1-A, BC-FRQ-2025-Q3-A, BC-FRQ-2026-Q1-A (`official_examples`).
- BC-QA-02014 (family derivative-definition-limit; research/question-analysis/question-archetypes.md#BC-QA-02014 Rate at an instant found before the derivative is defined, as a limit of average rates): `typical_wording` "at what rate is the quantity changing at the instant t equal to a named time". Its first written line is an average rate over a short interval starting at the instant, which is this concept's quotient; the question itself belongs to BC-CON-02002.

Contrast pair on st-1: this stem gives two tabulated values and a named interval and asks for an approximation with units; not this stem is the BC-QA-02014 shape, a polynomial model and one named instant, which is the rate at an instant and belongs to BC-CON-02002 (the rival archetype, and the `wrong_approaches` entry of averaging over the whole interval from the start). The separating feature is two named endpoints against one named instant.

What says "not this concept": a single instant with no interval asks for the rate at a point (BC-CON-02002); an interval that must be chosen to bracket a point asks for a derivative estimate (BC-CON-02007, the LSN-DEC-02-01 selector in the unit README section 3).

## Method choice

- st-1, BC-QA-04002. Cue from `asked_to_produce` and `common_givens`: a table, a named interval, and an approximation with work and units. Method, `expected_solution_path[0]`: select the two tabulated values the named interval determines. First written line: those two values over the difference of their inputs. Rival, `wrong_approaches`: the difference without the division (BC-ERR-02001). Separating feature: a rate carries a per in its units, so a quotient is on the page. The `method` text carries no leading label.
- st-2, BC-QA-02014. Cue: the rate at one named instant, from a polynomial model. Method, `expected_solution_path[0]`: write the average rate over a short interval starting at the instant. Rival, `wrong_approaches`: averaging over the whole interval from the start. Separating feature: one instant is named, not two endpoints.

Both archetypes carry `asked_to_produce` and `common_givens`, so neither block is tagged inferred.

## Solution path

- ex-1, BC-QA-04002, both bands, no calculator. Draw: times 1, 3, 6, 8, 11; readings 20, 31, 43, 52, 70; context runner; trend increasing, giving \(D(3)=31\), \(D(8)=52\) on the named interval \(3\le t\le 8\) and the point \(t=6\) inside it. Steps follow `expected_solution_path`: select the two values (no value), form the difference over the difference (valued), divide (valued), attach the units (no value). No step carries a point tag (Scoring). A fluent solver writes the quotient line, the value and the units, and holds the row selection in the head. The context's units (meters, minutes) come from the generation template for this archetype, not from `parameter_spec` [inferred].

BC-QA-02014 is listed first in the bundle, but its answer is a rate at an instant, which is BC-CON-02002's idea; ex-1 is drawn from BC-QA-04002, whose answer is this concept's average rate [inferred]. One example only, so nothing is faded. No productive-failure opener targets this concept (BC-CON-02002 is the unit's target), so no comparison callout.

## Scoring

BC-QA-04002 lists BC-PT-99005, BC-PT-99008 and BC-PT-99006, so ex-1 carries a scoring entry, and no step is tagged, so the entry holds no lines. Two reasons, both recorded as library gaps. The generated BC-PT-99005 line is 117 words, and with it the brief form exceeds its 450-word cap. The generated BC-PT-99006 line quotes an accepted compound unit whose wording the style check rejects. The two point conditions reach the student anyway, verbatim, as the scoring consequences of the two error blocks: the answer point needs a difference and a quotient from the table (BC-ERR-02001, sg-25:11), and the units point is earned for compound units attached or not (BC-ERR-02003, sg-25:11).

Point losses the scoring research names for this shape: no units, the units of the quantity, or a wrong ratio of units (research/scoring/common-point-losses.md#Units points, BC-ERR-99005; cr-22:14, cr-24:4); a setup with no value does not earn the answer point (research/scoring/common-point-losses.md#Answer points; sg-26:2).

## Traps

Two active errors meet the concept's skills, in the bundle's order (BC-MIS-02001 high, then BC-MIS-02008 medium). Both bands show both.

- err-BC-ERR-02001 (BC-MIS-02001, BC-MIS-02008). Wrong step on ex-1's draw: \(52-31=21\). Right step: \(\frac{52-31}{8-3}=\frac{21}{5}\). Distinct. Possible reason, words from BC-MIS-02001: the division by the change in the input is omitted.
- err-BC-ERR-02003 (BC-MIS-02008, BC-MIS-02001). Wrong step: \(\frac{21}{5}\) meters. Right step: \(\frac{21}{5}\) meters per minute. The two values are equivalent; the units point is what differs, which is the record's own scoring consequence. Possible reason, words from BC-MIS-02008: copies them from the table header.

## Representations

None as a separate block. The topic's Representations paragraph names one figure-shaped conversion, a table of values to an average rate with units (BC-REP-03 to BC-REP-04), and ki-1 carries it as a table (Delivery).

## Prerequisite bridge

Two BC-PRQ parents, both `supporting` on BC-SKL-02001, from `description_plain` and `failure_signature`:

- BC-PRQ-02005: \(f(a+h)\) is one value of \(f\), at the shifted input.
- BC-PRQ-02001: expand the shifted value and divide out \(h\) before setting \(h\) to zero.

## Time

BC-QA-04002 has `calculator_status` either and is the opening part of a table based FRQ. Under the template's rule an "either" archetype takes Section I Part A, 2.14 minutes (research/exam/exam-structure.md#Section and part layout) [inferred]; as an FRQ part it is 2 points of 9, 3.33 minutes of a 15.0 minute question (unit README section 5). Inside either budget a fluent solver writes three lines (the quotient, the value, the units) and skips the row selection, which is read, not written.

## Checks

- chk-1, completion of ex-1, both bands, short answer: the quotient line is given, the student evaluates it. Key \(\frac{21}{5}\), equal to ex-1's answer.
- chk-2, isomorph on BC-QA-04002, both bands: context crowd, times 0, 2, 5, 7, 10, readings 12, 18, 30, 41, 47, interval \(2\le t\le 7\). Key \(\frac{23}{5}\).
- chk-3, MCQ on BC-QA-04002, low band: context oven, trend decreasing, times 2, 4, 5, 9, 12, readings 75, 58, 40, 22, 15 (served pairing), interval \(4\le t\le 9\). Key \(-\frac{36}{5}\) degrees Fahrenheit per minute. The two error blocks differ in value (BC-ERR-02001) and in units (BC-ERR-02003), so the options are statements of value with units: \(-36\) degrees Fahrenheit (BC-ERR-02001), \(-\frac{36}{5}\) degrees Fahrenheit (BC-ERR-02003), \(-36\) degrees Fahrenheit per minute (BC-ERR-02001).

No example or check draw equals a published BC-QA-04002 `parameter_draw` (content/items_gen_unit04).

## Delivery

- orientation: text. Rule 5; a statement of what a response shows.
- ki-1: table. Rule 4; BC-SKL-02002 lists BC-REP-03, and the unit README's delivery map names a table for the average rate over a tabulated interval. Spec: ex-1's table with the two named rows marked and the quotient written inside the table frame.
- ex-1: step_reveal. Rule 1.
- err-BC-ERR-02001, err-BC-ERR-02003: step_reveal. Rule 1.

The table choice is [inferred], settled by the modality A/B in the build plan. The lesson already carries a drawn block (the table on ki-1), so it states no `no_figure_reason`. The prediction is delivered as text.

## Band plan

- Low (full), in served order: prediction, orientation, the two bridges (counted in both bands, served when state gates them in), ki-1, st-1 with its contrast pair, st-2, ex-1, chk-1, err-02001, err-02003, chk-2, chk-3. 535 words, 3.6 minutes (cap 900 and 6). Example 2 does not exist, so nothing is faded.
- Mid (brief): prediction, orientation, the bridges, ki-1, st-1 with its contrast pair, ex-1, chk-1, err-02001, err-02003, chk-2. 448 words, 3.0 minutes (cap 450 and 3).
- Refresher: ki-1, err-BC-ERR-02001, err-BC-ERR-02003, ex-1.

## Sources

- BC-CON-02001; BC-SKL-02001, BC-SKL-02002, BC-SKL-02003; BC-EK-CHA-2A1; ced:60
- BC-QA-04002, BC-QA-02014; BC-FRQ-2021-Q1-A, BC-FRQ-2022-Q4-A, BC-FRQ-2024-Q1-A, BC-FRQ-2025-Q3-A, BC-FRQ-2026-Q1-A
- BC-PT-99005, BC-PT-99006, BC-PT-99008; sg-25:11, sg-24:2, sg-25:4, sg-26:2; cr-22:14, cr-24:4; BC-ERR-99005
- BC-ERR-02001, BC-ERR-02003; BC-MIS-02001, BC-MIS-02008
- BC-PRQ-02001, BC-PRQ-02005
- research/units/unit-02-differentiation-definition-properties.md#2.1 Defining Average and Instantaneous Rates of Change at a Point
- research/units/unit-02-differentiation-definition-properties.md#2.3 Estimating Derivatives of a Function at a Point
- research/question-analysis/question-archetypes.md#BC-QA-04002 Approximating a derivative from a table with units
- research/question-analysis/question-archetypes.md#BC-QA-02014 Rate at an instant found before the derivative is defined, as a limit of average rates
- research/scoring/common-point-losses.md#Units points
- research/scoring/common-point-losses.md#Answer points
- research/exam/exam-structure.md#Section and part layout
- [inferred] BC-QA-04002 is "either" on calculator status, so the part is I-A by the template's rule. Settled by a calculator status on the archetype, or by the FRQ records' part assignments.
- [inferred] ex-1 is drawn from BC-QA-04002 rather than the bundle's first archetype, BC-QA-02014. Settled by a primary-archetype field on the concept.
- [inferred] The context units come from the generation template, not the parameter_spec. Settled by unit labels in the spec.
- [inferred] ex-1 tags no point type (Scoring). Settled by a shorter reader_checks form for BC-PT-99005 and BC-PT-99006 wording the style check accepts.
- [inferred] The table delivery for ki-1. Settled by the modality A/B.

## Machine record

```json
{
 "id": "LSN-CON-02001",
 "kind": "concept",
 "target_id": "BC-CON-02001",
 "unit": "02",
 "skills": ["BC-SKL-02001", "BC-SKL-02002", "BC-SKL-02003"],
 "prediction": {
  "id": "pr-1",
  "stem": {"text": "\\(D(3)=31\\) and \\(D(8)=52\\) meters. Which gives the average rate over \\(3\\le t\\le 8\\)?", "command_verb": "predict"},
  "format": "mcq",
  "options": [
   {"id": "A", "label": "\\(52-31\\)", "is_key": false},
   {"id": "B", "label": "\\(\\frac{52-31}{8-3}\\)", "is_key": true},
   {"id": "C", "label": "\\(\\frac{52+31}{2}\\)", "is_key": false}
  ],
  "resolution": "The average rate is the change in output divided by the change in input: \\(\\frac{21}{5}\\) meters per minute.",
  "sources": ["BC-CON-02001", "research/units/unit-02-differentiation-definition-properties.md#2.1 Defining Average and Instantaneous Rates of Change at a Point"]
 },
 "orientation": {
  "text": "A response shows an average rate as a quotient with compound units: the change in output divided by the change in input over the named interval.",
  "sources": ["BC-CON-02001", "research/units/unit-02-differentiation-definition-properties.md#2.1 Defining Average and Instantaneous Rates of Change at a Point", "sg-25:11"]
 },
 "key_ideas": [
  {
   "id": "ki-1",
   "ek_id": "BC-EK-CHA-2A1",
   "depth": "core",
   "text": "The average rate of \\(f\\) over an interval is \\(\\frac{f(a+h)-f(a)}{h}\\) or \\(\\frac{f(x)-f(a)}{x-a}\\), each a change in output over the matching change in input. From a table, the interval names two rows. Units: output per input.",
   "notation": "difference quotient",
   "quote": null,
   "sources": ["BC-EK-CHA-2A1", "ced:60", "research/units/unit-02-differentiation-definition-properties.md#2.1 Defining Average and Instantaneous Rates of Change at a Point", "research/units/unit-02-differentiation-definition-properties.md#2.3 Estimating Derivatives of a Function at a Point"]
  }
 ],
 "strategy": [
  {
   "id": "st-1",
   "archetype_id": "BC-QA-04002",
   "cue": "A table, a named interval, an approximation with units.",
   "method": "The two named values, differenced, over the difference of their inputs.",
   "rival": "The difference without the division.",
   "separating_feature": "A rate has a per in its units, so a quotient appears.",
   "contrast": {
    "this": {"text": "A table gives \\(V(4)=20\\) and \\(V(10)=31\\) gallons. Using the average rate over \\(4\\le t\\le 10\\), approximate \\(V'(6)\\) with units.", "archetype_id": "BC-QA-04002"},
    "not_this": {"text": "\\(V(t)=t^2+2t\\) gallons. At what rate is the volume changing at \\(t=6\\)?", "why_not": "One instant and no interval asks for the limit of average rates."},
    "feature": "Two named endpoints against one named instant."
   },
   "sources": ["BC-QA-04002", "BC-ERR-02001"],
   "evidence_tag": "verified"
  },
  {
   "id": "st-2",
   "archetype_id": "BC-QA-02014",
   "cue": "A polynomial model and one named instant; the stem asks for the rate at that instant.",
   "method": "The average rate over a short interval starting at the instant, \\(\\frac{f(t_0+h)-f(t_0)}{h}\\).",
   "rival": "The rival averages over the whole interval from the start.",
   "separating_feature": "One instant is named, not two endpoints.",
   "sources": ["BC-QA-02014"],
   "evidence_tag": "verified"
  }
 ],
 "worked_examples": [
  {
   "id": "ex-1",
   "archetype_id": "BC-QA-04002",
   "bands": ["low", "mid"],
   "parameter_draw": {"times": [1, 3, 6, 8, 11], "readings": [20, 31, 43, 52, 70], "context": "runner", "trend": "increasing"},
   "problem": {"text": "A runner has covered \\(D(t)\\) meters at \\(t\\) minutes: \\(D(1)=20\\), \\(D(3)=31\\), \\(D(6)=43\\), \\(D(8)=52\\), \\(D(11)=70\\). Using the average rate over \\(3\\le t\\le 8\\), approximate \\(D'(6)\\) with units.", "command_verb": "approximate"},
   "calculator_status": "no_calculator",
   "steps": [
    {"cue": "The stem names \\(3\\le t\\le 8\\): read rows 3 and 8.", "why": "\\(D(3)=31\\), \\(D(8)=52\\); the row at 6 is the point, not an endpoint."},
    {"cue": "A rate is asked: difference of values over difference of inputs.", "why": "The answer point needs both on the page.", "expr": "(52 - 31)/(8 - 3)", "relation": "new"},
    {"cue": "A value is asked; no calculator.", "why": "The exact fraction stands.", "expr": "21/5", "relation": "equivalent"},
    {"cue": "Units are asked.", "why": "Meters over minutes: meters per minute, scored separately."}
   ],
   "answer": {"form": "numeric", "expr": "21/5"}
  }
 ],
 "what_a_reader_scores": [
  {"example_id": "ex-1", "point_type_ids": [], "lines": []}
 ],
 "common_errors": [
  {
   "error_id": "BC-ERR-02001",
   "observed_behavior": "The response reports the change in the function values over the interval without dividing by the change in the inputs.",
   "scoring_consequence": "The answer point requires both a difference and a quotient using values from the table, so a difference alone does not earn it (sg-25:11).",
   "wrong_step": {"text": "\\(52-31=21\\).", "expr": "52 - 31"},
   "right_step": {"text": "\\(\\frac{52-31}{8-3}=\\frac{21}{5}\\).", "expr": "(52 - 31)/(8 - 3)"},
   "relation": "distinct",
   "fix_prompt": true,
   "possible_reason": {"misconception_id": "BC-MIS-02001", "text": "the division by the change in the input is omitted"},
   "sources": ["BC-ERR-02001", "BC-MIS-02001"]
  },
  {
   "error_id": "BC-ERR-02003",
   "observed_behavior": "The response reports an estimated derivative with no units, or with the units of the modelled quantity rather than of its rate.",
   "scoring_consequence": "The units point is lost; it is earned for the correct compound units whether or not they are attached to a value, and an equivalent compound form is accepted (sg-25:11).",
   "wrong_step": {"text": "\\(\\frac{21}{5}\\) meters.", "expr": "21/5"},
   "right_step": {"text": "\\(\\frac{21}{5}\\) meters per minute.", "expr": "(52 - 31)/(8 - 3)"},
   "relation": "equivalent",
   "fix_prompt": false,
   "possible_reason": {"misconception_id": "BC-MIS-02008", "text": "copies them from the table header"},
   "sources": ["BC-ERR-02003", "BC-MIS-02008"]
  }
 ],
 "representations": null,
 "prerequisite_bridges": [
  {"prq_id": "BC-PRQ-02005", "text": "\\(f(a+h)\\) is one value of \\(f\\), at the shifted input."},
  {"prq_id": "BC-PRQ-02001", "text": "Expand the shifted value and divide out \\(h\\) before setting \\(h\\) to zero."}
 ],
 "time": {"exam_part": "I-A", "budget_minutes": 2.14, "source": "research/exam/exam-structure.md#Section and part layout", "written_steps": {"ex-1": [2, 3, 4]}, "skipped_steps": {"ex-1": [1]}},
 "checks": [
  {
   "id": "chk-1",
   "check_kind": "completion",
   "format": "short_answer",
   "bands": ["low", "mid"],
   "archetype_id": "BC-QA-04002",
   "parameter_draw": {"times": [1, 3, 6, 8, 11], "readings": [20, 31, 43, 52, 70], "context": "runner", "trend": "increasing"},
   "completes": "ex-1",
   "stem": {"text": "The work reads \\(D'(6)\\approx\\frac{52-31}{8-3}\\). Give the value.", "command_verb": "give"},
   "key": {"form": "numeric", "expr": "21/5"},
   "steps": [
    {"text": "The quotient \\(\\frac{52-31}{8-3}\\).", "expr": "(52 - 31)/(8 - 3)", "relation": "new", "point_type_id": "BC-PT-99005"},
    {"text": "That is \\(\\frac{21}{5}\\).", "expr": "21/5", "relation": "equivalent"}
   ],
   "calculator_status": "no_calculator",
   "skills": ["BC-SKL-02002"]
  },
  {
   "id": "chk-2",
   "check_kind": "isomorph",
   "format": "short_answer",
   "bands": ["low", "mid"],
   "archetype_id": "BC-QA-04002",
   "parameter_draw": {"times": [0, 2, 5, 7, 10], "readings": [12, 18, 30, 41, 47], "context": "crowd", "trend": "increasing"},
   "stem": {"text": "\\(P(t)\\) hundred people are in a stadium at \\(t\\) minutes: \\(P(0)=12\\), \\(P(2)=18\\), \\(P(5)=30\\), \\(P(7)=41\\), \\(P(10)=47\\). Using the average rate over \\(2\\le t\\le 7\\), approximate \\(P'(5)\\).", "command_verb": "approximate"},
   "key": {"form": "numeric", "expr": "23/5"},
   "steps": [
    {"text": "\\(\\frac{41-18}{7-2}\\).", "expr": "(41 - 18)/(7 - 2)", "relation": "new", "point_type_id": "BC-PT-99005"},
    {"text": "That is \\(\\frac{23}{5}\\) hundred people per minute.", "expr": "23/5", "relation": "equivalent"}
   ],
   "calculator_status": "no_calculator",
   "skills": ["BC-SKL-02002"]
  },
  {
   "id": "chk-3",
   "check_kind": "mcq",
   "format": "mcq",
   "bands": ["low"],
   "archetype_id": "BC-QA-04002",
   "parameter_draw": {"times": [2, 4, 5, 9, 12], "readings": [75, 58, 40, 22, 15], "context": "oven", "trend": "decreasing"},
   "stem": {"text": "\\(H(t)\\) degrees Fahrenheit is an oven's temperature at \\(t\\) minutes: \\(H(2)=75\\), \\(H(4)=58\\), \\(H(5)=40\\), \\(H(9)=22\\), \\(H(12)=15\\). Using the average rate over \\(4\\le t\\le 9\\), which approximates \\(H'(5)\\)?", "command_verb": "approximate"},
   "key": {"form": "statement", "expr": "-36/5", "label": "\\(-\\frac{36}{5}\\) degrees Fahrenheit per minute"},
   "steps": [
    {"text": "\\(\\frac{22-58}{9-4}\\).", "expr": "(22 - 58)/(9 - 4)", "relation": "new", "point_type_id": "BC-PT-99005"},
    {"text": "That is \\(-\\frac{36}{5}\\) degrees Fahrenheit per minute.", "expr": "-36/5", "relation": "equivalent"}
   ],
   "options": [
    {"id": "A", "is_key": false, "label": "\\(-36\\) degrees Fahrenheit", "expr": "-36", "error_path": "BC-ERR-02001", "derivation": "the difference 22 - 58 reported without dividing by 9 - 4"},
    {"id": "B", "is_key": true, "label": "\\(-\\frac{36}{5}\\) degrees Fahrenheit per minute", "expr": "-36/5", "error_path": null},
    {"id": "C", "is_key": false, "label": "\\(-\\frac{36}{5}\\) degrees Fahrenheit", "expr": "-36/5", "error_path": "BC-ERR-02003", "derivation": "the right value with the units of the quantity"},
    {"id": "D", "is_key": false, "label": "\\(-36\\) degrees Fahrenheit per minute", "expr": "-36", "error_path": "BC-ERR-02001", "derivation": "the difference reported as the rate, with rate units attached"}
   ],
   "calculator_status": "no_calculator",
   "skills": ["BC-SKL-02002", "BC-SKL-02003"]
  }
 ],
 "delivery": [
  {"block": "orientation", "mode": "text", "reason": "rule 5: a statement of what a response shows", "sources": ["BC-CON-02001"]},
  {"block": "ki-1", "mode": "table", "reason": "rule 4: BC-SKL-02002 lists BC-REP-03; the unit README delivery map names a table for the average rate over a tabulated interval", "sources": ["BC-SKL-02002"],
   "spec": {"kind": "table", "representations": ["BC-REP-03"], "columns": ["t (minutes)", "D(t) (meters)"], "rows": [[1, 20], [3, 31], [6, 43], [8, 52], [11, 70]], "marked_rows": [2, 4],
    "labels": [{"text": "named interval: t = 3 to t = 8", "placement": "inside", "at": "bracket joining rows 2 and 4"}, {"text": "(52 - 31)/(8 - 3) = 21/5 meters per minute", "placement": "inside", "at": "last line of the table frame"}]},
   "fallback": "the same five rows as a text list with the two named rows in bold and the quotient written after them", "keyboard": "none needed; the table is read row by row in order by a screen reader, with the marked rows announced"},
  {"block": "ex-1", "mode": "step_reveal", "reason": "rule 1", "sources": []},
  {"block": "err-BC-ERR-02001", "mode": "step_reveal", "reason": "rule 1", "sources": []},
  {"block": "err-BC-ERR-02003", "mode": "step_reveal", "reason": "rule 1", "sources": []}
 ],
 "refresher": ["ki-1", "err-BC-ERR-02001", "err-BC-ERR-02003", "ex-1"],
 "read_minutes": {"full": 3.6, "brief": 3.0},
 "word_count": {"full": 534, "brief": 447},
 "research_lines": [
  {"file": "research/units/unit-02-differentiation-definition-properties.md", "line": "FRQ forms compute an average rate with supporting work and units"},
  {"file": "research/scoring/common-point-losses.md", "line": "Units are scored separately from the value"}
 ],
 "inferred": [
  {"claim": "BC-QA-04002 carries calculator status either, so the lesson takes Section I Part A by the template's rule.", "settles": "A single calculator status on the archetype, or the FRQ records' part assignments."},
  {"claim": "ex-1 is drawn from BC-QA-04002 rather than the bundle's first archetype, BC-QA-02014, whose answer is a rate at an instant.", "settles": "A primary-archetype field on the concept record."},
  {"claim": "The context units (meters, minutes; hundred people; degrees Fahrenheit) come from the generation template, not the parameter_spec.", "settles": "Unit labels in the BC-QA-04002 parameter_spec."},
  {"claim": "ex-1 tags no point type: the BC-PT-99005 reader line would break the brief cap and the BC-PT-99006 line fails the style check, so the point conditions are served through the error blocks' scoring consequences.", "settles": "A shorter reader_checks form for BC-PT-99005, and BC-PT-99006 wording without the rejected unit phrase."},
  {"claim": "A table serves ki-1 better than text.", "settles": "The modality A/B in the build plan: skip rate and time to first credited success by mode."}
 ],
 "sources": ["BC-CON-02001", "BC-SKL-02001", "BC-SKL-02002", "BC-SKL-02003", "BC-EK-CHA-2A1", "ced:60", "BC-QA-04002", "BC-QA-02014", "BC-PT-99005", "BC-PT-99006", "BC-PT-99008", "sg-25:11", "sg-24:2", "sg-25:4", "sg-26:2", "cr-22:14", "cr-24:4", "BC-ERR-99005", "BC-ERR-02001", "BC-ERR-02003", "BC-MIS-02001", "BC-MIS-02008", "BC-PRQ-02001", "BC-PRQ-02005", "BC-FRQ-2021-Q1-A", "BC-FRQ-2022-Q4-A", "BC-FRQ-2024-Q1-A", "BC-FRQ-2025-Q3-A", "BC-FRQ-2026-Q1-A", "research/units/unit-02-differentiation-definition-properties.md#2.1 Defining Average and Instantaneous Rates of Change at a Point", "research/units/unit-02-differentiation-definition-properties.md#2.3 Estimating Derivatives of a Function at a Point", "research/scoring/common-point-losses.md#Units points", "research/scoring/common-point-losses.md#Answer points", "research/exam/exam-structure.md#Section and part layout"]
}
```
