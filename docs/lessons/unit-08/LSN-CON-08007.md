---
title: LSN-CON-08007 Net rate as rate in minus rate out
research_date: 2026-09-29
status: designed
purpose: Authoring spec for the concept lesson on BC-CON-08007, the net rate as inflow minus outflow in one integral, built from authoring_bundle("BC-CON-08007") and the research files it cites, so an author fills plan 15's lesson record without making a teaching decision.
---

# LSN-CON-08007 Net rate as rate in minus rate out

Concept BC-CON-08007 (skill BC-SKL-08013), topic 8.3 of Unit 8, with no Unit 8 hard parent (docs/lessons/unit-08/README.md, section 1). The skill names a retired archetype id; the bundle lists its successor, BC-QA-06006 (family rate-in-rate-out).

## Prediction

One multiple choice question on worked example 1's own rates, asked before the rule is shown: water enters at E(t) = 6 + 2sin(t^2/3) and leaves at L(t) = 3 + cos(t/2) gallons per hour, and the student picks the net rate of change of the water in the tank. The key is E minus L; the distractors are E plus L and L minus E. The resolution, shown on the key idea screen, says entering raises and leaving lowers the amount. No verdict word. Sources: BC-CON-08007 and the topic 8.3 section the key ideas cite. [inferred]

## Orientation

Served text, from BC-CON-08007 `description_plain` and the topic's Assessment behaviour paragraph (research/units/unit-08-applications-integration.md#8.3 Using Accumulation Functions and Definite Integrals in Applied Contexts): a response writes one integral of the inflow minus the outflow, the outflow in parentheses, adds the initial amount when an amount is asked, and reports three decimals. No count, no frequency.

## Key ideas

BC-SKL-08013 maps to BC-EK-CHA-4D2 and BC-EK-CHA-4E1 (ced:154): two blocks.

- ki-1 (core, both bands), BC-EK-CHA-4D2. Paraphrase of the Accumulation and Net rate paragraphs: the integral of a rate over an interval is the net change; with inflow and outflow at once the net rate is their difference, and the amount rises where it is positive.
- ki-2 (extended, low band), BC-EK-CHA-4E1. Paraphrase of the Amount at a time and Interpretation paragraphs: the integral of the net rate is the net change in the amount, in the rate's units times the time units; the amount adds the initial amount (sg-24:4).

No anchor quotes. Notation line on ki-1 from the concept record.

## Recognition

BC-QA-06006 (research/question-analysis/question-archetypes.md#BC-QA-06006 Rate in minus rate out accumulation): `typical_wording` "water enters at one rate and leaves at another; find the amount present at the end of the interval, showing the setup for your calculations"; `common_givens` an inflow rate, an outflow rate, an initial amount; `asked_to_produce` a net rate expression, an integral, a value with units. The signal is two rates with opposite verbs (enters, leaves). Official parts BC-FRQ-2015-Q1-D, 2018-Q1-B.

The contrast pair on st-1 sets a BC-QA-06006 stem (two flows, the final amount asked) against a stem that names the same two flows and asks only how much enters. The near miss comes from BC-QA-99008, whose `prohibited_shortcuts` name subtracting the second rate where the part asks for the inflow alone. The feature is the amount or net change asked, not one flow.

What says "not this concept": one rate only (BC-CON-08006); "at what time is the amount greatest" (BC-CON-08008, the net rate set to zero).

## Method choice

One strategy block, both bands, carrying the contrast pair. st-1, BC-QA-06006. Method, `expected_solution_path[0]`: identify which rate increases and which decreases the quantity. Rival, `wrong_approaches`: dropping the parentheses around the outflow rate, and integrating each rate and subtracting the wrong way round. Separating feature: the verb attached to each rate. Not tagged inferred. The served fields carry no leading label.

## Solution path

- ex-1, BC-QA-06006, both bands, calculator. Draw: inflow_base 6, inflow_swing 2, stretch 3, outflow_base 3, outflow_swing 1, horizon 3, initial 50, context tank, ask amount; \(E(t)=6+2\sin(t^2/3)\), \(L(t)=3+\cos(t/2)\) on [0, 3]. The amount constraint holds (50 + (6 - 2 - 3 - 1)(3) > 0). No published item carries this draw.
- Steps: which rate is which (no value); the setup (new, tagged BC-PT-99001); the calculator value (evaluate, approx). A fluent solver writes the setup and the value and holds the identification. One example only, so no `fade_from`.

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
- Figure presence: no drawn block. No rule of 2 to 5 applies, since no skill representation is figure-bearing and no key idea describes a process, so the record carries `no_figure_reason`.
- ex-1, err-BC-ERR-08013, err-BC-ERR-99009: step_reveal. Rule 1.

## Band plan

- Low (full), in served order: prediction, orientation, the bridge, ki-1, ki-2, st-1 with its contrast, ex-1 with its scoring line, chk-1, two error blocks, chk-2. 482 words, 3.3 minutes.
- Mid (brief): the same without ki-2. 448 words, 3.0 minutes. To fit the cap the orientation, ki-1, the st-1 fields, the ex-1 cues and whys and the bridge were shortened; no anchor quote or scoring tag was dropped.
- Refresher: ki-1, err-BC-ERR-08013, err-BC-ERR-99009, ex-1.

## Sources

- BC-CON-08007; BC-SKL-08013; BC-EK-CHA-4D2, BC-EK-CHA-4E1; ced:154
- BC-QA-06006, BC-QA-99008; BC-PT-99001; sg-24:4
- BC-ERR-08013, BC-ERR-99009; BC-MIS-08007
- BC-PRQ-06005
- research/units/unit-08-applications-integration.md#8.3 Using Accumulation Functions and Definite Integrals in Applied Contexts
- research/question-analysis/question-archetypes.md#BC-QA-06006 Rate in minus rate out accumulation
- research/scoring/common-point-losses.md#Notation points
- research/exam/exam-structure.md#Section and part layout
- [inferred] The 3.33 minute share and the held identification. Settled by per-step timing data.
- [inferred] The prediction and the contrast pair as teaching moves. Settled by the modality and prompt A/B in the build plan.
- [inferred] Two checks only. Settled by a third active error on BC-SKL-08013.

## Machine record

```json
{
 "id": "LSN-CON-08007",
 "kind": "concept",
 "target_id": "BC-CON-08007",
 "unit": "08",
 "skills": [
  "BC-SKL-08013"
 ],
 "prediction": {
  "id": "pr-1",
  "stem": {
   "text": "Predict: water enters a tank at \\(E(t)=6+2\\sin(t^2/3)\\) and leaves at \\(L(t)=3+\\cos(t/2)\\) gallons per hour. Which gives the tank's net rate of change?",
   "command_verb": "predict"
  },
  "format": "mcq",
  "options": [
   {
    "id": "A",
    "label": "\\(E(t)\\) plus \\(L(t)\\)",
    "is_key": false
   },
   {
    "id": "B",
    "label": "\\(E(t)\\) minus \\(L(t)\\)",
    "is_key": true
   },
   {
    "id": "C",
    "label": "\\(L(t)\\) minus \\(E(t)\\)",
    "is_key": false
   }
  ],
  "resolution": "Entering raises the amount, leaving lowers it: the net rate is \\(E(t)-L(t)\\).",
  "sources": [
   "BC-CON-08007",
   "research/units/unit-08-applications-integration.md#8.3 Using Accumulation Functions and Definite Integrals in Applied Contexts"
  ]
 },
 "no_figure_reason": "The skill's representations are contextual and symbolic, none figure-bearing, and the key ideas describe no process; the net rate is a difference of two written rates.",
 "orientation": {
  "text": "One integral of inflow minus (outflow), plus the initial amount, to three decimals.",
  "sources": [
   "BC-CON-08007",
   "research/units/unit-08-applications-integration.md#8.3 Using Accumulation Functions and Definite Integrals in Applied Contexts"
  ]
 },
 "key_ideas": [
  {
   "id": "ki-1",
   "ek_id": "BC-EK-CHA-4D2",
   "depth": "core",
   "text": "The integral of a rate is the net change; with two flows the net rate is their difference.",
   "notation": "rate in minus rate out",
   "quote": null,
   "sources": [
    "BC-EK-CHA-4D2",
    "ced:154",
    "research/units/unit-08-applications-integration.md#8.3 Using Accumulation Functions and Definite Integrals in Applied Contexts"
   ]
  },
  {
   "id": "ki-2",
   "ek_id": "BC-EK-CHA-4E1",
   "depth": "extended",
   "text": "In context, the integral of E minus L over [a, b] is the net change in the amount, in the rate's units times the time units. The amount at b adds the initial amount.",
   "notation": "",
   "quote": null,
   "sources": [
    "BC-EK-CHA-4E1",
    "ced:154",
    "sg-24:4",
    "research/units/unit-08-applications-integration.md#8.3 Using Accumulation Functions and Definite Integrals in Applied Contexts"
   ]
  }
 ],
 "strategy": [
  {
   "id": "st-1",
   "archetype_id": "BC-QA-06006",
   "cue": "Inflow, outflow, initial amount; the amount is asked.",
   "method": "Which rate increases the quantity, which decreases it.",
   "rival": "Dropping the outflow's parentheses, or subtracting the wrong way round.",
   "separating_feature": "Enters adds, leaves subtracts.",
   "sources": [
    "BC-QA-06006",
    "BC-QA-99008"
   ],
   "evidence_tag": "verified",
   "contrast": {
    "this": {
     "text": "Grain enters a bin at \\(G(t)\\) and leaves at \\(H(t)\\). Find the final amount, showing the setup.",
     "archetype_id": "BC-QA-06006"
    },
    "not_this": {
     "text": "Water enters a tank at \\(E(t)\\) and leaves at \\(L(t)\\). How much enters from \\(t=0\\) to \\(t=3\\)?",
     "why_not": "Only the inflow integral is asked."
    },
    "feature": "The amount, not one flow."
   }
  }
 ],
 "worked_examples": [
  {
   "id": "ex-1",
   "archetype_id": "BC-QA-06006",
   "bands": [
    "low",
    "mid"
   ],
   "parameter_draw": {
    "inflow_base": 6,
    "inflow_swing": 2,
    "stretch": 3,
    "outflow_base": 3,
    "outflow_swing": 1,
    "horizon": 3,
    "initial": 50,
    "context": "tank",
    "ask": "amount"
   },
   "problem": {
    "text": "Water enters a tank at E(t) = 6 + 2sin(t^2/3) and leaves at L(t) = 3 + cos(t/2) gallons per hour. At t = 0 it holds 50 gallons. Find the amount at t = 3.",
    "command_verb": "find"
   },
   "calculator_status": "calculator",
   "steps": [
    {
     "cue": "Enters and leaves.",
     "why": "Net rate E - L."
    },
    {
     "cue": "Amount at t = 3, 50 at t = 0.",
     "why": "L in parentheses.",
     "expr": "50 + Integral(6 + 2*sin(t**2/3) - (3 + cos(t/2)), (t, 0, 3))",
     "relation": "new",
     "point_type_id": "BC-PT-99001"
    },
    {
     "cue": "Radian mode.",
     "why": "Gallons, three places.",
     "expr": "60.095",
     "relation": "evaluate",
     "subs": {},
     "approx": true
    }
   ],
   "answer": {
    "form": "numeric",
    "expr": "60.095"
   }
  }
 ],
 "what_a_reader_scores": [
  {
   "example_id": "ex-1",
   "point_type_ids": [
    "BC-PT-99001"
   ],
   "lines": [
    {
     "point_type_id": "BC-PT-99001",
     "text": "Definite integral expression with correct limits. Earned by: A definite integral whose limits match the requested interval and whose integrand matches the requested quantity, with or without the differential (sg-26:4, sg-22:2). Not earned by: An unsupported numerical value, or a definite integral whose bounds are wrong (sg-22:18). Notation: Differential may be omitted; sg-22:2 accepts dx written for dt. sg-23:8 treats a missing differential as recoverable for this point but restricts later eligibility."
    }
   ]
  }
 ],
 "common_errors": [
  {
   "error_id": "BC-ERR-08013",
   "observed_behavior": "The net rate is written as the sum of the two rates, or the difference is taken in the wrong order.",
   "scoring_consequence": "The setup point is lost.",
   "wrong_step": {
    "text": "E + L.",
    "expr": "50 + Integral(6 + 2*sin(t**2/3) + (3 + cos(t/2)), (t, 0, 3))"
   },
   "right_step": {
    "text": "E - L.",
    "expr": "50 + Integral(6 + 2*sin(t**2/3) - (3 + cos(t/2)), (t, 0, 3))"
   },
   "relation": "distinct",
   "possible_reason": {
    "misconception_id": "BC-MIS-08007",
    "text": "attaches accumulation to every rate in the problem"
   },
   "sources": [
    "BC-ERR-08013",
    "BC-MIS-08007"
   ],
   "fix_prompt": true
  },
  {
   "error_id": "BC-ERR-99009",
   "observed_behavior": "Responses that replace named functions by their given analytic expressions fail to distribute a subtraction or omit the grouping parentheses, changing the integrand.",
   "scoring_consequence": "The integrand point is lost; the answer point may survive if a correct calculator value is also reported.",
   "wrong_step": {
    "text": "No parentheses: cos(t/2) added.",
    "expr": "50 + Integral(6 + 2*sin(t**2/3) - 3 + cos(t/2), (t, 0, 3))"
   },
   "right_step": {
    "text": "Parentheses kept.",
    "expr": "50 + Integral(6 + 2*sin(t**2/3) - (3 + cos(t/2)), (t, 0, 3))"
   },
   "relation": "distinct",
   "possible_reason": {
    "misconception_id": "BC-MIS-08007",
    "text": "without attending to the direction in which each one moves the quantity"
   },
   "sources": [
    "BC-ERR-99009",
    "BC-MIS-08007"
   ],
   "fix_prompt": true
  }
 ],
 "representations": null,
 "prerequisite_bridges": [
  {
   "prq_id": "BC-PRQ-06005",
   "text": "50 is an amount; E, L are rates."
  }
 ],
 "time": {
  "exam_part": "II-A",
  "budget_minutes": 15.0,
  "source": "research/exam/exam-structure.md#Section and part layout",
  "written_steps": {
   "ex-1": [
    2,
    3
   ]
  },
  "skipped_steps": {
   "ex-1": [
    1
   ]
  }
 },
 "checks": [
  {
   "id": "chk-1",
   "check_kind": "completion",
   "format": "short_answer",
   "bands": [
    "low",
    "mid"
   ],
   "archetype_id": "BC-QA-06006",
   "parameter_draw": {
    "inflow_base": 6,
    "inflow_swing": 2,
    "stretch": 3,
    "outflow_base": 3,
    "outflow_swing": 1,
    "horizon": 3,
    "initial": 50,
    "context": "tank",
    "ask": "amount"
   },
   "completes": "ex-1",
   "stem": {
    "text": "Evaluate 50 + the integral from 0 to 3 of (6 + 2sin(t^2/3) - (3 + cos(t/2))) dt, to three places.",
    "command_verb": "evaluate"
   },
   "key": {
    "form": "numeric",
    "expr": "60.095"
   },
   "steps": [
    {
     "text": "Setup.",
     "expr": "50 + Integral(6 + 2*sin(t**2/3) - (3 + cos(t/2)), (t, 0, 3))",
     "relation": "new"
    },
    {
     "text": "Calculator.",
     "expr": "60.095",
     "relation": "evaluate",
     "subs": {},
     "approx": true
    }
   ],
   "calculator_status": "calculator",
   "skills": [
    "BC-SKL-08013"
   ]
  },
  {
   "id": "chk-2",
   "check_kind": "isomorph",
   "format": "short_answer",
   "bands": [
    "low",
    "mid"
   ],
   "archetype_id": "BC-QA-06006",
   "parameter_draw": {
    "inflow_base": 8,
    "inflow_swing": 1,
    "stretch": 4,
    "outflow_base": 2,
    "outflow_swing": 2,
    "horizon": 2,
    "initial": 30,
    "context": "silo",
    "ask": "amount"
   },
   "stem": {
    "text": "Grain is loaded at 8 + sin(t^2/4) and unloaded at 2 + 2cos(t/2) tons per hour. The silo holds 30 tons at t = 0. Find the amount at t = 2.",
    "command_verb": "find"
   },
   "key": {
    "form": "numeric",
    "expr": "39.255"
   },
   "steps": [
    {
     "text": "Setup.",
     "expr": "30 + Integral(8 + sin(t**2/4) - (2 + 2*cos(t/2)), (t, 0, 2))",
     "relation": "new"
    },
    {
     "text": "Calculator.",
     "expr": "39.255",
     "relation": "evaluate",
     "subs": {},
     "approx": true
    }
   ],
   "calculator_status": "calculator",
   "skills": [
    "BC-SKL-08013"
   ]
  }
 ],
 "delivery": [
  {
   "block": "orientation",
   "mode": "text",
   "reason": "rule 6: BC-REP-05 and 01 on BC-SKL-08013, none figure-bearing",
   "sources": [
    "BC-SKL-08013"
   ]
  },
  {
   "block": "ki-1",
   "mode": "text",
   "reason": "rule 6: a rule for combining two rates; unit README delivery map names text",
   "sources": [
    "BC-SKL-08013"
   ]
  },
  {
   "block": "ki-2",
   "mode": "text",
   "reason": "rule 6: an interpretation habit",
   "sources": [
    "BC-SKL-08013"
   ]
  },
  {
   "block": "ex-1",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  },
  {
   "block": "err-BC-ERR-08013",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  },
  {
   "block": "err-BC-ERR-99009",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  }
 ],
 "refresher": [
  "ki-1",
  "err-BC-ERR-08013",
  "err-BC-ERR-99009",
  "ex-1"
 ],
 "read_minutes": {
  "full": 3.3,
  "brief": 3.0
 },
 "word_count": {
  "full": 482,
  "brief": 448
 },
 "research_lines": [
  {
   "file": "research/units/unit-08-applications-integration.md",
   "line": "the net rate is the difference, and the amount increases where that difference is positive"
  }
 ],
 "inferred": [
  {
   "claim": "The part takes a 3.33 minute share of the 15.0 minute question, and a fluent solver holds the identification of the rates.",
   "settles": "Per-step timing data from the fluency telemetry."
  },
  {
   "claim": "The lesson carries two checks: the bundle holds two errors, fewer than the three distractors a 4-option MCQ needs.",
   "settles": "A third active BC-ERR on BC-SKL-08013."
  }
 ],
 "sources": [
  "BC-CON-08007",
  "BC-SKL-08013",
  "BC-EK-CHA-4D2",
  "BC-EK-CHA-4E1",
  "ced:154",
  "BC-QA-06006",
  "BC-PT-99001",
  "sg-24:4",
  "BC-ERR-08013",
  "BC-ERR-99009",
  "BC-MIS-08007",
  "BC-PRQ-06005",
  "research/units/unit-08-applications-integration.md#8.3 Using Accumulation Functions and Definite Integrals in Applied Contexts",
  "research/question-analysis/question-archetypes.md#BC-QA-06006 Rate in minus rate out accumulation",
  "research/scoring/common-point-losses.md#Notation points",
  "research/exam/exam-structure.md#Section and part layout"
 ]
}
```
