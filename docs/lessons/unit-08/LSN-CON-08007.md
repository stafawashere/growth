---
title: LSN-CON-08007 Net rate as rate in minus rate out
research_date: 2026-09-29
status: designed
purpose: Authoring spec for the concept lesson on BC-CON-08007, the net rate as inflow minus outflow in one integral, built from authoring_bundle("BC-CON-08007") and the research files it cites, so an author fills plan 15's lesson record without making a teaching decision.
---

# LSN-CON-08007 Net rate as rate in minus rate out

Concept BC-CON-08007 (skill BC-SKL-08013), topic 8.3 of Unit 8, with no Unit 8 hard parent (docs/lessons/unit-08/README.md, section 1). The skill names a retired archetype id; the bundle lists its successor, BC-QA-06006 (family rate-in-rate-out).

## Orientation

Served text, from BC-CON-08007 `description_plain` and the topic's Assessment behaviour paragraph (research/units/unit-08-applications-integration.md#8.3 Using Accumulation Functions and Definite Integrals in Applied Contexts): a response writes one integral of the inflow minus the outflow, the outflow in parentheses, adds the initial amount when an amount is asked, and reports three decimals. No count, no frequency.

## Key ideas

BC-SKL-08013 maps to BC-EK-CHA-4D2 and BC-EK-CHA-4E1 (ced:154): two blocks.

- ki-1 (core, both bands), BC-EK-CHA-4D2. Paraphrase of the Accumulation and Net rate paragraphs: the integral of a rate over an interval is the net change; with inflow and outflow at once the net rate is their difference, and the amount rises where it is positive.
- ki-2 (extended, low band), BC-EK-CHA-4E1. Paraphrase of the Amount at a time and Interpretation paragraphs: the integral of the net rate is the net change in the amount, in the rate's units times the time units; the amount adds the initial amount (sg-24:4).

No anchor quotes. Notation line on ki-1 from the concept record.

## Recognition

BC-QA-06006 (research/question-analysis/question-archetypes.md#BC-QA-06006 Rate in minus rate out accumulation): `typical_wording` "water enters at one rate and leaves at another; find the amount present at the end of the interval, showing the setup for your calculations"; `common_givens` an inflow rate, an outflow rate, an initial amount; `asked_to_produce` a net rate expression, an integral, a value with units. The signal is two rates with opposite verbs (enters, leaves). Official parts BC-FRQ-2015-Q1-D, 2018-Q1-B.

What says "not this concept": one rate only (BC-CON-08006); "at what time is the amount greatest" (BC-CON-08008, the net rate set to zero).

## Method choice

One strategy block, both bands. st-1, BC-QA-06006. Method, `expected_solution_path[0]`: identify which rate increases and which decreases the quantity. Rival, `wrong_approaches`: dropping the parentheses around the outflow rate, and integrating each rate and subtracting the wrong way round. Separating feature: the verb attached to each rate. Not tagged inferred.

## Solution path

- ex-1, BC-QA-06006, both bands, calculator. Draw: inflow_base 6, inflow_swing 2, stretch 3, outflow_base 3, outflow_swing 1, horizon 3, initial 50, context tank, ask amount; \(E(t)=6+2\sin(t^2/3)\), \(L(t)=3+\cos(t/2)\) on [0, 3]. The amount constraint holds (50 + (6 - 2 - 3 - 1)(3) > 0). No published item carries this draw.
- Steps: which rate is which (no value); the setup (new, tagged BC-PT-99001); the calculator value (evaluate, approx). A fluent solver writes the setup and the value and holds the identification.

## Scoring

BC-QA-06006 lists BC-PT-99001 and BC-PT-99068. ex-1 tags BC-PT-99001 on the setup; the line is `reader_checks(["BC-PT-99001"])`. BC-PT-99068 is a show-that verification and does not apply. Pattern: the integral without the initial value forfeits the initial condition point (sg-24:4). Point loss: parentheses omitted when a given expression replaces a named function (research/scoring/common-point-losses.md#Notation points, BC-ERR-99009).

## Traps

Two active errors, both bands, on ex-1's draw.

- err-BC-ERR-08013: the rates added. Possible reason, words from BC-MIS-08007.
- err-BC-ERR-99009: L substituted without parentheses, so its cosine term is added. Possible reason, words from BC-MIS-08007.

## Representations

None. The topic's Representations paragraph names contextual, symbolic, tabular and calculator conversions; nothing figure-shaped for two rates combined.

## Prerequisite bridge

- BC-PRQ-06005, from its `description_plain` and `failure_signature`.

## Time

BC-QA-06006 is `calculator`, one part of a free response question: Section II Part A, 15.0 minutes per question (research/exam/exam-structure.md#Section and part layout). Two points on the records, a 3.33 minute share (docs/lessons/unit-08/README.md, section 5) [inferred].

## Checks

- chk-1, completion of ex-1, both bands. Key 60.095.
- chk-2, isomorph, both bands. Draw: inflow_base 8, inflow_swing 1, stretch 4, outflow_base 2, outflow_swing 2, horizon 2, initial 30, context silo, ask amount. Key 39.255.
- No chk-3: two errors in the bundle (listed inferred).

## Delivery

- orientation, ki-1, ki-2: text. Rule 6: BC-REP-05 and 01 on BC-SKL-08013; the unit README's delivery map names text.
- ex-1, err-BC-ERR-08013, err-BC-ERR-99009: step_reveal. Rule 1.

## Band plan

- Low (full): orientation, ki-1, ki-2, st-1, ex-1 with its scoring line, two error blocks, chk-1, chk-2, the bridge. 464 words, 3.1 minutes.
- Mid (brief): the same without ki-2. 430 words, 2.9 minutes.
- Refresher: ki-1, err-BC-ERR-08013, err-BC-ERR-99009, ex-1.

## Sources

- BC-CON-08007; BC-SKL-08013; BC-EK-CHA-4D2, BC-EK-CHA-4E1; ced:154
- BC-QA-06006; BC-PT-99001; sg-24:4
- BC-ERR-08013, BC-ERR-99009; BC-MIS-08007
- BC-PRQ-06005
- research/units/unit-08-applications-integration.md#8.3 Using Accumulation Functions and Definite Integrals in Applied Contexts
- research/question-analysis/question-archetypes.md#BC-QA-06006 Rate in minus rate out accumulation
- research/scoring/common-point-losses.md#Notation points
- research/exam/exam-structure.md#Section and part layout
- [inferred] The 3.33 minute share and the held identification. Settled by per-step timing data.
- [inferred] Two checks only. Settled by a third active error on BC-SKL-08013.

## Machine record

```json
{
 "id": "LSN-CON-08007",
 "kind": "concept",
 "target_id": "BC-CON-08007",
 "unit": "08",
 "skills": ["BC-SKL-08013"],
 "orientation": {
  "text": "A response writes one integral of inflow minus (outflow), adds the initial amount when an amount is asked, and reports three decimals.",
  "sources": ["BC-CON-08007", "research/units/unit-08-applications-integration.md#8.3 Using Accumulation Functions and Definite Integrals in Applied Contexts"]
 },
 "key_ideas": [
  {
   "id": "ki-1",
   "ek_id": "BC-EK-CHA-4D2",
   "depth": "core",
   "text": "The integral of a rate over an interval is the net change. With inflow E and outflow L at once, the net rate is E minus L; the amount rises where it is positive.",
   "notation": "rate in minus rate out",
   "quote": null,
   "sources": ["BC-EK-CHA-4D2", "ced:154", "research/units/unit-08-applications-integration.md#8.3 Using Accumulation Functions and Definite Integrals in Applied Contexts"]
  },
  {
   "id": "ki-2",
   "ek_id": "BC-EK-CHA-4E1",
   "depth": "extended",
   "text": "In context, the integral of E minus L over [a, b] is the net change in the amount, in the rate's units times the time units. The amount at b adds the initial amount.",
   "notation": "",
   "quote": null,
   "sources": ["BC-EK-CHA-4E1", "ced:154", "sg-24:4", "research/units/unit-08-applications-integration.md#8.3 Using Accumulation Functions and Definite Integrals in Applied Contexts"]
  }
 ],
 "strategy": [
  {
   "id": "st-1",
   "archetype_id": "BC-QA-06006",
   "cue": "An inflow rate, an outflow rate and an initial amount; the amount or the change is asked.",
   "method": "First: which rate increases the quantity and which decreases it.",
   "rival": "Rival: dropping the parentheses around the outflow rate, or subtracting the wrong way round.",
   "separating_feature": "The verb on each rate: enters adds, leaves subtracts.",
   "sources": ["BC-QA-06006"],
   "evidence_tag": "verified"
  }
 ],
 "worked_examples": [
  {
   "id": "ex-1",
   "archetype_id": "BC-QA-06006",
   "bands": ["low", "mid"],
   "parameter_draw": {"inflow_base": 6, "inflow_swing": 2, "stretch": 3, "outflow_base": 3, "outflow_swing": 1, "horizon": 3, "initial": 50, "context": "tank", "ask": "amount"},
   "problem": {"text": "Water enters a tank at E(t) = 6 + 2sin(t^2/3) and leaves at L(t) = 3 + cos(t/2) gallons per hour. At t = 0 it holds 50 gallons. Find the amount at t = 3.", "command_verb": "find"},
   "calculator_status": "calculator",
   "steps": [
    {"cue": "Two rates: enters and leaves.", "why": "E raises the amount, L lowers it: net rate E - L."},
    {"cue": "Amount at t = 3, with 50 gallons at t = 0.", "why": "L in parentheses, so all of it subtracts.", "expr": "50 + Integral(6 + 2*sin(t**2/3) - (3 + cos(t/2)), (t, 0, 3))", "relation": "new", "point_type_id": "BC-PT-99001"},
    {"cue": "Setup written; calculator in radian mode.", "why": "Gallons, three places.", "expr": "60.095", "relation": "evaluate", "subs": {}, "approx": true}
   ],
   "answer": {"form": "numeric", "expr": "60.095"}
  }
 ],
 "what_a_reader_scores": [
  {"example_id": "ex-1", "point_type_ids": ["BC-PT-99001"], "lines": [{"point_type_id": "BC-PT-99001", "text": "Definite integral expression with correct limits. Earned by: A definite integral whose limits match the requested interval and whose integrand matches the requested quantity, with or without the differential (sg-26:4, sg-22:2). Not earned by: An unsupported numerical value, or a definite integral whose bounds are wrong (sg-22:18). Notation: Differential may be omitted; sg-22:2 accepts dx written for dt. sg-23:8 treats a missing differential as recoverable for this point but restricts later eligibility."}]}
 ],
 "common_errors": [
  {
   "error_id": "BC-ERR-08013",
   "observed_behavior": "The net rate is written as the sum of the two rates, or the difference is taken in the wrong order.",
   "scoring_consequence": "The setup point is lost.",
   "wrong_step": {"text": "E + L.", "expr": "50 + Integral(6 + 2*sin(t**2/3) + (3 + cos(t/2)), (t, 0, 3))"},
   "right_step": {"text": "E - L.", "expr": "50 + Integral(6 + 2*sin(t**2/3) - (3 + cos(t/2)), (t, 0, 3))"},
   "relation": "distinct",
   "possible_reason": {"misconception_id": "BC-MIS-08007", "text": "attaches accumulation to every rate in the problem"},
   "sources": ["BC-ERR-08013", "BC-MIS-08007"]
  },
  {
   "error_id": "BC-ERR-99009",
   "observed_behavior": "Responses that replace named functions by their given analytic expressions fail to distribute a subtraction or omit the grouping parentheses, changing the integrand.",
   "scoring_consequence": "The integrand point is lost; the answer point may survive if a correct calculator value is also reported.",
   "wrong_step": {"text": "No parentheses: cos(t/2) added.", "expr": "50 + Integral(6 + 2*sin(t**2/3) - 3 + cos(t/2), (t, 0, 3))"},
   "right_step": {"text": "Parentheses kept.", "expr": "50 + Integral(6 + 2*sin(t**2/3) - (3 + cos(t/2)), (t, 0, 3))"},
   "relation": "distinct",
   "possible_reason": {"misconception_id": "BC-MIS-08007", "text": "without attending to the direction in which each one moves the quantity"},
   "sources": ["BC-ERR-99009", "BC-MIS-08007"]
  }
 ],
 "representations": null,
 "prerequisite_bridges": [
  {"prq_id": "BC-PRQ-06005", "text": "E(t) and L(t) are rates; 50 is an amount at t = 0."}
 ],
 "time": {"exam_part": "II-A", "budget_minutes": 15.0, "source": "research/exam/exam-structure.md#Section and part layout", "written_steps": {"ex-1": [2, 3]}, "skipped_steps": {"ex-1": [1]}},
 "checks": [
  {
   "id": "chk-1",
   "check_kind": "completion",
   "format": "short_answer",
   "bands": ["low", "mid"],
   "archetype_id": "BC-QA-06006",
   "parameter_draw": {"inflow_base": 6, "inflow_swing": 2, "stretch": 3, "outflow_base": 3, "outflow_swing": 1, "horizon": 3, "initial": 50, "context": "tank", "ask": "amount"},
   "completes": "ex-1",
   "stem": {"text": "Evaluate 50 + the integral from 0 to 3 of (6 + 2sin(t^2/3) - (3 + cos(t/2))) dt, to three places.", "command_verb": "evaluate"},
   "key": {"form": "numeric", "expr": "60.095"},
   "steps": [
    {"text": "Setup.", "expr": "50 + Integral(6 + 2*sin(t**2/3) - (3 + cos(t/2)), (t, 0, 3))", "relation": "new"},
    {"text": "Calculator.", "expr": "60.095", "relation": "evaluate", "subs": {}, "approx": true}
   ],
   "calculator_status": "calculator",
   "skills": ["BC-SKL-08013"]
  },
  {
   "id": "chk-2",
   "check_kind": "isomorph",
   "format": "short_answer",
   "bands": ["low", "mid"],
   "archetype_id": "BC-QA-06006",
   "parameter_draw": {"inflow_base": 8, "inflow_swing": 1, "stretch": 4, "outflow_base": 2, "outflow_swing": 2, "horizon": 2, "initial": 30, "context": "silo", "ask": "amount"},
   "stem": {"text": "Grain is loaded at 8 + sin(t^2/4) and unloaded at 2 + 2cos(t/2) tons per hour. The silo holds 30 tons at t = 0. Find the amount at t = 2.", "command_verb": "find"},
   "key": {"form": "numeric", "expr": "39.255"},
   "steps": [
    {"text": "Setup.", "expr": "30 + Integral(8 + sin(t**2/4) - (2 + 2*cos(t/2)), (t, 0, 2))", "relation": "new"},
    {"text": "Calculator.", "expr": "39.255", "relation": "evaluate", "subs": {}, "approx": true}
   ],
   "calculator_status": "calculator",
   "skills": ["BC-SKL-08013"]
  }
 ],
 "delivery": [
  {"block": "orientation", "mode": "text", "reason": "rule 6: BC-REP-05 and 01 on BC-SKL-08013, none figure-bearing", "sources": ["BC-SKL-08013"]},
  {"block": "ki-1", "mode": "text", "reason": "rule 6: a rule for combining two rates; unit README delivery map names text", "sources": ["BC-SKL-08013"]},
  {"block": "ki-2", "mode": "text", "reason": "rule 6: an interpretation habit", "sources": ["BC-SKL-08013"]},
  {"block": "ex-1", "mode": "step_reveal", "reason": "rule 1", "sources": []},
  {"block": "err-BC-ERR-08013", "mode": "step_reveal", "reason": "rule 1", "sources": []},
  {"block": "err-BC-ERR-99009", "mode": "step_reveal", "reason": "rule 1", "sources": []}
 ],
 "refresher": ["ki-1", "err-BC-ERR-08013", "err-BC-ERR-99009", "ex-1"],
 "read_minutes": {"full": 3.1, "brief": 2.9},
 "word_count": {"full": 464, "brief": 430},
 "research_lines": [
  {"file": "research/units/unit-08-applications-integration.md", "line": "the net rate is the difference, and the amount increases where that difference is positive"}
 ],
 "inferred": [
  {"claim": "The part takes a 3.33 minute share of the 15.0 minute question, and a fluent solver holds the identification of the rates.", "settles": "Per-step timing data from the fluency telemetry."},
  {"claim": "The lesson carries two checks: the bundle holds two errors, fewer than the three distractors a 4-option MCQ needs.", "settles": "A third active BC-ERR on BC-SKL-08013."}
 ],
 "sources": ["BC-CON-08007", "BC-SKL-08013", "BC-EK-CHA-4D2", "BC-EK-CHA-4E1", "ced:154", "BC-QA-06006", "BC-PT-99001", "sg-24:4", "BC-ERR-08013", "BC-ERR-99009", "BC-MIS-08007", "BC-PRQ-06005", "research/units/unit-08-applications-integration.md#8.3 Using Accumulation Functions and Definite Integrals in Applied Contexts", "research/question-analysis/question-archetypes.md#BC-QA-06006 Rate in minus rate out accumulation", "research/scoring/common-point-losses.md#Notation points", "research/exam/exam-structure.md#Section and part layout"]
}
```
