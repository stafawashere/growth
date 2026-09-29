---
title: LSN-CON-06001 Accumulation of change as area under a rate graph
research_date: 2026-09-29
status: designed
purpose: Authoring spec for the concept lesson on BC-CON-06001, the signed area under a rate graph as accumulated change, found by geometry or stated in words, built from authoring_bundle("BC-CON-06001") and the research files it cites.
---

# LSN-CON-06001 Accumulation of change as area under a rate graph

Concept BC-CON-06001 (skills BC-SKL-06001, BC-SKL-06004), topic 6.1 of Unit 6, loaded by BC-QA-06015 (family accumulation-interpretation) and BC-QA-06004 (family definite-integral-from-graph). It is Unit 6's productive-failure target (app/engine/constants.py PRODUCTIVE_FAILURE_TARGETS) and has no Unit 6 hard parent (docs/lessons/unit-06/README.md, section 1).

## Prediction

One multiple choice question on worked example 1's own regions, asked before the rule is shown: the areas 3 above the axis and 2 and 2π below it, and what the integral over [0, 8] is. The key option is that regions below the axis subtract, which gives 3 - 2 - 2π, ex-1's fourth valued step. The distractors add every region (the BC-ERR-06014 path) and subtract only the 2, adding the semicircle's region. The resolution, shown on the key idea screen beside the choice, states that regions below subtract and gives the net change. No verdict word. Sources: BC-CON-06001 and the topic 6.1 section the key ideas cite.

## Orientation

Served text (21 words), from BC-CON-06001 `description_plain` and the topic's Assessment behaviour paragraph (research/units/unit-06-integration-accumulation.md#6.1 Exploring Accumulations of Change): the area between a rate graph and the axis is the change in the quantity, given as signed area or as a sentence with units and interval. No count, no frequency. The served text carries no record id.

## Key ideas

Two skills, two BC-EK, both core, both bands.

- ki-1 (core), BC-EK-CHA-4A1 (BC-SKL-06001), ced:118. Paraphrase of the Rate and accumulation paragraph of Required mathematical knowledge: signed area between the rate graph and the axis is the accumulated change. No anchor quote, to hold the brief band under 450 words.
- ki-2 (core), BC-EK-CHA-4A2 (BC-SKL-06004), ced:118. Geometry as the method when the graph is segments and arcs. No anchor quote, for the same reason.

The Units and Sign paragraphs map to BC-EK-CHA-4A4 and 4A3, which belong to BC-CON-06002 (LSN-CON-06002).

## Recognition

- BC-QA-06004 (research/question-analysis/question-archetypes.md#BC-QA-06004 Definite integral evaluated from a graph by geometry). `typical_wording`: "the graph of f consists of line segments and semicircles; evaluate the definite integral of f over the stated interval". `common_givens`: a graph of f made of line segments and semicircles, an accumulation function with a fixed lower limit. `asked_to_produce`: the value of a definite integral, labelled values of an accumulation function. Official examples BC-FRQ-2024-Q4-A, BC-FRQ-2025-Q4-C, BC-FRQ-2018-Q3-B.
- BC-QA-06015 (research/question-analysis/question-archetypes.md#BC-QA-06015 Interpreting a definite integral in context with units). `typical_wording`: "using correct units, interpret the meaning of the displayed definite integral in the context of the problem". `common_givens`: a contextual rate function, a definite integral expression. `asked_to_produce`: a sentence with quantity, interval, and units. No `official_examples`; the notes name 2023 Q1(a) and 2024 Q1(b).

Contrast pair on st-1: this stem is on BC-QA-06004, a graph of segments and a semicircle with a definite integral asked; not this stem is the same graph with the average value of f asked, the near miss from the sibling concept BC-CON-06013 (a leading factor 1/(b - a)). The separating feature is that leading factor.

The signal: a rate (a graph with a named rate, or units "per" something) and a request for a change or its meaning. Not this concept: a leading factor 1/(b - a) (average value, BC-CON-06013), or an initial amount with "how much is present" (BC-CON-06012).

## Method choice

- st-1, BC-QA-06004 (both bands). Method, `expected_solution_path[0]`: partition the region at the points where the graph changes character. Rival from `wrong_approaches`: regions below the axis added as positive area (BC-ERR-06014). Separating feature: pieces below the axis are negative. The first block also carries the contrast pair above. Every field is served without the reader's own label, and record ids sit in `sources`.
- st-2, BC-QA-06015 (low band). Method, `expected_solution_path[0]`: identify what the integrand measures per unit input. Rival from `wrong_approaches`: naming the quantity without the interval; giving the units of the rate. Separating feature: an amount over an interval carries the product of units and both limits.

Both archetypes carry `asked_to_produce` and `common_givens`, so neither block is tagged inferred.

## Solution path

- ex-1, BC-QA-06004, both bands, no calculator. Draw: heights 2, 2, 0, -2, lower 0, circle below, forward; derived `linear_area` = 1. Steps follow `expected_solution_path`: partition (no value); gain on [0, 2], 3 (new); loss on [2, 4], -2 (new); semicircle, -2π (new); signed total (new, BC-PT-99069); 1 - 2π (equivalent). No published BC-QA-06004 item carries this draw.
- ex-2, BC-QA-06015, low band, statement answer, faded (`fade_from` 3): steps 1 and 2 are shown (the rate, the units product gallons/hour times hour), and the student cancels the hours to gallons and writes the sentence before steps 3 to 5 (the cancelled hours, the limits naming the interval, the sentence itself) reveal. The fade falls there so the withheld part holds a valued step, the units result, as well as the scored sentence. Draw: context water, start 2, length 4, display total, direction accumulates. Units chain gallons/hour times hour to gallons (new, equivalent); the sentence names quantity, units, interval. No point tag: BC-QA-06015 lists no `point_types`.

A fluent solver writes the signed total and the labelled value of ex-1 and the one sentence of ex-2; the partition, formulas and units product are held (unit README section 5) [inferred].

Comparison gap, productive-failure target (BC-CON-06001, app/engine/constants.py; BC-QA-06004 carries BC-DF-13). When the opener preceded the lesson, ex-1 opens with a comparison callout: the opener attempt adds every shaded piece as area, 5 + 2π on this draw, against the canonical signed sum, 1 - 2π. The gap is the sign of the pieces below the axis (BC-QA-06004 `wrong_approaches`, BC-ERR-06014; docs/plan/15-lessons.md, Within a concept, step 2) [inferred: the attempt shape is the recorded wrong approach, not an observed opener log].

## Scoring

ex-1 on BC-QA-06004 tags BC-PT-99069 on the signed total; the reader line is `reader_checks(["BC-PT-99069"])` copied exactly. ex-2 is on BC-QA-06015, which lists no `point_types`, so it carries no checklist and no tag. For the author: the interpretation point requires both the accumulated quantity with its units and the interval (sg-23:2), and an average value must be called an average over the interval (sg-24:3); key phrases absent from an average value interpretation cost that point (research/scoring/common-point-losses.md#Interpretation points).

## Traps

Four active errors meet the skills, in the bundle's order: BC-ERR-06014 (BC-MIS-08024, high), BC-ERR-06030 (BC-MIS-06014, high), BC-ERR-06013 (BC-MIS-08019, medium), BC-ERR-06029 (BC-MIS-08009, medium). Low band all four, mid band the first two.

- err-BC-ERR-06014, on ex-1: 3 + 2 + 2π against 3 - 2 - 2π. Possible reason, words from BC-MIS-08024.
- err-BC-ERR-06030, on ex-1: (1/8) of the integral called the total, 1 - 2π, against the average (1 - 2π)/8. No possible reason line, to hold the brief band.
- err-BC-ERR-06013, on ex-1: the semicircle as 4π against 2π. Possible reason, words from BC-MIS-08019.
- err-BC-ERR-06029, on ex-2: gallons per hour against gallons with the interval. Possible reason, words from BC-MIS-08009.

## Representations

One block, low band, from the topic's Representations paragraph (contextual model to signed area, BC-REP-05 to BC-REP-02): the running total of ex-1's rate at x = 1, 2, 3, 4, 6, 8, computed and shown as a table beside the graph, served as the model the unit README's delivery map fixes for this productive-failure target.

## Prerequisite bridge

- BC-PRQ-06005 (reading function notation and evaluation), from `description_plain` and `failure_signature`.
- BC-PRQ-06007 (area formulas), from `description_plain` and `failure_signature`.

## Time

ex-1's archetype BC-QA-06004 is `no_calculator`, one part of a free response question or one MCQ; the design takes Section II Part B, 15.0 minutes per question (research/exam/exam-structure.md#Section and part layout), of which this one point part is a 1.67 minute share (unit README section 5) [inferred]. BC-QA-06015 is `either` and would take I-A [inferred]. The minutes go on the signs of the pieces and on the interval in the sentence.

## Checks

- chk-1, completion of ex-1, both bands: the signed pieces are given; key 1 - 2π.
- chk-2, isomorph, both bands. Draw: heights 3, 3, 0, -3, lower 1, circle above, forward. Key 2π - 3/2.
- chk-3, MCQ, low band, on BC-QA-06015. Draw: water, start 2, length 4, display average, accumulates. Key: the average rate in gallons per hour over 2 ≤ t ≤ 6. Distractors: the total (BC-ERR-06030), the average with no interval (BC-ERR-06029), the change in gallons (BC-ERR-06030).

## Delivery

- orientation, ki-1, ki-2: figure. Rule 4: BC-REP-02 on BC-SKL-06001 and 06004 (unit README section 6).
- ex-1, ex-2 and the four error blocks: step_reveal. Rule 1. The four error blocks are fix prompts (all `distinct`).
- prediction: text, no delivery entry.
- representations: model. The template's model row puts every productive-failure target on a model; the running total is a computed sequence.

Every non-text choice is [inferred]; settled by the modality A/B.

## Band plan

- Low (full), in served order: prediction, orientation, both bridges, ki-1, ki-2, st-1 with its contrast pair, st-2, ex-1 with its reader line, chk-1, the four error blocks, ex-2 faded, chk-2, the model, chk-3. 797 words, 5.4 minutes (cap 900 and 6).
- Mid (brief), in served order: prediction, orientation, both bridges, ki-1, ki-2, st-1 with its contrast pair, ex-1 with its reader line, chk-1, err-BC-ERR-06014, err-BC-ERR-06030, chk-2. 448 words, 3.0 minutes (cap 450 and 3). The orientation, key ideas, strategy, cues and bridges were shortened to hold this; no anchor quote or scoring tag was dropped.
- Refresher: ki-1, ki-2, the four error blocks, ex-1.

## Sources

- BC-CON-06001; BC-SKL-06001, BC-SKL-06004; BC-EK-CHA-4A1, BC-EK-CHA-4A2; ced:118
- BC-QA-06004, BC-QA-06015; BC-PT-99069; sg-25:18, sg-24:12, sg-23:2, sg-24:3
- BC-ERR-06014, BC-ERR-06030, BC-ERR-06013, BC-ERR-06029; BC-MIS-08024, BC-MIS-08019, BC-MIS-08009
- BC-PRQ-06005, BC-PRQ-06007
- research/units/unit-06-integration-accumulation.md#6.1 Exploring Accumulations of Change
- research/question-analysis/question-archetypes.md#BC-QA-06004 Definite integral evaluated from a graph by geometry
- research/question-analysis/question-archetypes.md#BC-QA-06015 Interpreting a definite integral in context with units
- research/exam/exam-structure.md#Section and part layout
- research/scoring/common-point-losses.md#Interpretation points
- [inferred] Example 1 from BC-QA-06004 ahead of the first-listed BC-QA-06015. Settled by a ruling on productive-failure archetypes.
- [inferred] The II-B share of 1.67 minutes. Settled by timing data per step.
- [inferred] Gallons per hour as the unit for the water context. Settled by a units field in the parameter_spec.
- [inferred] The opener attempt shape in the comparison gap. Settled by opener attempt logs.
- [inferred] Every non-text delivery mode. Settled by the modality A/B.

## Machine record

```json
{
 "id": "LSN-CON-06001",
 "kind": "concept",
 "target_id": "BC-CON-06001",
 "unit": "06",
 "skills": [
  "BC-SKL-06001",
  "BC-SKL-06004"
 ],
 "prediction": {
  "id": "pr-1",
  "stem": {
   "text": "Before the rule: f has regions of area 3 above the axis, and 2 and 2π below it. What is ∫_0^8 f(x) dx?",
   "command_verb": "predict"
  },
  "format": "mcq",
  "options": [
   {
    "id": "A",
    "label": "All three regions add",
    "is_key": false
   },
   {
    "id": "B",
    "label": "Regions below the axis subtract",
    "is_key": true
   },
   {
    "id": "C",
    "label": "Only the 2 subtracts",
    "is_key": false
   }
  ],
  "resolution": "Regions below subtract: 3 - 2 - 2π = 1 - 2π, the net change.",
  "sources": [
   "BC-CON-06001",
   "research/units/unit-06-integration-accumulation.md#6.1 Exploring Accumulations of Change"
  ]
 },
 "orientation": {
  "text": "Area between a rate graph and the axis is the quantity's change: signed area, or a sentence with units and interval.",
  "sources": [
   "BC-CON-06001",
   "research/units/unit-06-integration-accumulation.md#6.1 Exploring Accumulations of Change"
  ]
 },
 "key_ideas": [
  {
   "id": "ki-1",
   "ek_id": "BC-EK-CHA-4A1",
   "depth": "core",
   "text": "The region between a rate graph and the axis is the quantity's change: gain above, loss below.",
   "notation": "signed area; accumulated change",
   "quote": null,
   "sources": [
    "BC-EK-CHA-4A1",
    "ced:118",
    "research/units/unit-06-integration-accumulation.md#6.1 Exploring Accumulations of Change"
   ]
  },
  {
   "id": "ki-2",
   "ek_id": "BC-EK-CHA-4A2",
   "depth": "core",
   "text": "One area formula per piece; pieces below the axis are negative.",
   "notation": "signed area",
   "quote": null,
   "sources": [
    "BC-EK-CHA-4A2",
    "ced:118",
    "research/units/unit-06-integration-accumulation.md#6.1 Exploring Accumulations of Change"
   ]
  }
 ],
 "strategy": [
  {
   "id": "st-1",
   "archetype_id": "BC-QA-06004",
   "cue": "Segments and semicircles; a value asked.",
   "method": "Partition where the graph changes character.",
   "rival": "Every piece added as area.",
   "separating_feature": "Pieces below the axis are negative.",
   "sources": [
    "BC-QA-06004"
   ],
   "evidence_tag": "verified",
   "contrast": {
    "this": {
     "text": "f is segments and a semicircle. Find ∫_0^8 f(x) dx.",
     "archetype_id": "BC-QA-06004"
    },
    "not_this": {
     "text": "f is segments and a semicircle. Find the average value of f on [0, 8].",
     "why_not": "It asks for the integral divided by the length."
    },
    "feature": "A leading factor 1/(b - a)."
   }
  },
  {
   "id": "st-2",
   "archetype_id": "BC-QA-06015",
   "cue": "A contextual rate and a displayed integral; a sentence with quantity, interval and units asked.",
   "method": "Identify what the integrand measures per unit input.",
   "rival": "Naming the quantity without the interval, or with the rate's units.",
   "separating_feature": "The integral is an amount over an interval, so it carries the product of the units and both limits.",
   "sources": [
    "BC-QA-06015"
   ],
   "evidence_tag": "verified"
  }
 ],
 "worked_examples": [
  {
   "id": "ex-1",
   "archetype_id": "BC-QA-06004",
   "bands": [
    "low",
    "mid"
   ],
   "parameter_draw": {
    "heights": [
     2,
     2,
     0,
     -2
    ],
    "lower": 0,
    "circle": "below",
    "direction": "forward"
   },
   "problem": {
    "text": "Rate f: segments through (0, 2), (1, 2), (2, 0), (3, -2), (4, 0), then a radius 2 semicircle below [4, 8]. Find ∫_0^8 f(x) dx.",
    "command_verb": "find"
   },
   "calculator_status": "no_calculator",
   "steps": [
    {
     "cue": "Split at x = 2 and 4.",
     "why": "One shape each."
    },
    {
     "cue": "[0, 2]: above.",
     "why": "Gain.",
     "expr": "2*1 + (1/2)*1*2",
     "relation": "new"
    },
    {
     "cue": "[2, 4]: below.",
     "why": "Loss is negative.",
     "expr": "-(1/2)*2*2",
     "relation": "new"
    },
    {
     "cue": "[4, 8]: semicircle below.",
     "why": "Half of πr².",
     "expr": "-(1/2)*pi*2**2",
     "relation": "new"
    },
    {
     "cue": "The signed total.",
     "why": "Intervals add.",
     "expr": "3 - 2 - 2*pi",
     "relation": "new",
     "point_type_id": "BC-PT-99069"
    },
    {
     "cue": "Label it.",
     "why": "Net loss.",
     "expr": "1 - 2*pi",
     "relation": "equivalent"
    }
   ],
   "answer": {
    "form": "symbolic",
    "expr": "1 - 2*pi"
   }
  },
  {
   "id": "ex-2",
   "archetype_id": "BC-QA-06015",
   "bands": [
    "low"
   ],
   "parameter_draw": {
    "context": "water",
    "start": 2,
    "length": 4,
    "display": "total",
    "direction": "accumulates"
   },
   "problem": {
    "text": "Water flows into a tank at R(t) gallons per hour, t in hours. Interpret ∫_2^6 R(t) dt with units.",
    "command_verb": "interpret"
   },
   "calculator_status": "no_calculator",
   "steps": [
    {
     "cue": "The integrand is a rate: gallons per hour.",
     "why": "The integral accumulates what the rate measures."
    },
    {
     "cue": "Multiply the units.",
     "why": "Rate units times input units.",
     "expr": "gallons/hour*hour",
     "relation": "new"
    },
    {
     "cue": "Hours cancel.",
     "why": "An amount, not a rate.",
     "expr": "gallons",
     "relation": "equivalent"
    },
    {
     "cue": "The limits name the interval.",
     "why": "The interval is required."
    },
    {
     "cue": "Write the sentence.",
     "why": "Quantity, units and interval together."
    }
   ],
   "answer": {
    "form": "statement",
    "expr": "gallons",
    "text": "The number of gallons of water that flow into the tank from t = 2 to t = 6 hours."
   },
   "fade_from": 3
  }
 ],
 "what_a_reader_scores": [
  {
   "example_id": "ex-1",
   "point_type_ids": [
    "BC-PT-99069"
   ],
   "lines": [
    {
     "point_type_id": "BC-PT-99069",
     "text": "Value of an accumulation function found from geometry of a graph. Earned by: The value of the accumulation function at the requested input, computed from areas of the regions under the graph, with the correct sign for reversed limits (sg-25:18, sg-24:12). Not earned by: A value from the wrong starting limit; sg-24:13 has a special case where an explicitly wrong lower limit forfeits the first point it would otherwise have earned."
    }
   ]
  }
 ],
 "common_errors": [
  {
   "error_id": "BC-ERR-06014",
   "observed_behavior": "Every piece of the region is added with a positive sign, so a signed integral is reported as a plain area.",
   "scoring_consequence": "The value point is lost, and any later part that imports the value inherits the error.",
   "wrong_step": {
    "text": "Losses added.",
    "expr": "3 + 2 + 2*pi"
   },
   "right_step": {
    "text": "Losses subtracted.",
    "expr": "3 - 2 - 2*pi"
   },
   "relation": "distinct",
   "fix_prompt": true,
   "possible_reason": {
    "misconception_id": "BC-MIS-08024",
    "text": "reads every definite integral as area"
   },
   "sources": [
    "BC-ERR-06014",
    "BC-MIS-08024"
   ]
  },
  {
   "error_id": "BC-ERR-06030",
   "observed_behavior": "A displayed average value expression is described as the total amount accumulated over the interval.",
   "scoring_consequence": "The interpretation point is not earned because the description must say average over the interval (sg-24:3).",
   "wrong_step": {
    "text": "(1/8)∫_0^8 f called the total change.",
    "expr": "1 - 2*pi"
   },
   "right_step": {
    "text": "It is the average of f on [0, 8].",
    "expr": "(1 - 2*pi)/8"
   },
   "relation": "distinct",
   "fix_prompt": true,
   "possible_reason": null,
   "sources": [
    "BC-ERR-06030"
   ]
  },
  {
   "error_id": "BC-ERR-06013",
   "observed_behavior": "The area of a semicircular piece of the region is computed as pi times the radius squared.",
   "scoring_consequence": "The value point for that integral is lost.",
   "wrong_step": {
    "text": "Semicircle as 4π.",
    "expr": "3 - 2 - 4*pi"
   },
   "right_step": {
    "text": "Semicircle as 2π.",
    "expr": "3 - 2 - 2*pi"
   },
   "relation": "distinct",
   "fix_prompt": true,
   "possible_reason": {
    "misconception_id": "BC-MIS-08019",
    "text": "remembers the squared dimension but not the fraction in front of it"
   },
   "sources": [
    "BC-ERR-06013",
    "BC-MIS-08019"
   ]
  },
  {
   "error_id": "BC-ERR-06029",
   "observed_behavior": "The response names the accumulated quantity but not the interval over which it accumulates, or gives the units of the rate.",
   "scoring_consequence": "The interpretation point requires both the accumulated quantity with units and the interval, so it is not earned (sg-23:2).",
   "wrong_step": {
    "text": "Water in, in gallons per hour.",
    "expr": "gallons/hour"
   },
   "right_step": {
    "text": "Gallons in, from t = 2 to t = 6.",
    "expr": "gallons"
   },
   "relation": "distinct",
   "fix_prompt": true,
   "possible_reason": {
    "misconception_id": "BC-MIS-08009",
    "text": "treats the sentence as a label for the integral rather than as a statement that must fix the quantity, the interval, and the units"
   },
   "sources": [
    "BC-ERR-06029",
    "BC-MIS-08009"
   ]
  }
 ],
 "representations": {
  "text": "Run the running total of the first example's rate from x = 0: 2, 3, 2, 1, then 1 - π at 6 and 1 - 2π at 8. It rises while f is positive and falls while f is negative.",
  "figure": {
   "kind": "numeric_experiment",
   "function": "F(x) = ∫_0^x f(t) dt, the running total of the first example's rate f",
   "computed": "F(x), evaluated at each x",
   "x_values": [
    1,
    2,
    3,
    4,
    6,
    8
   ],
   "values": [
    "2",
    "3",
    "2",
    "1",
    "1 - pi",
    "1 - 2*pi"
   ],
   "labels": [
    {
     "text": "total rises while f > 0",
     "placement": "inside",
     "at": "rows x = 1 to 2"
    },
    {
     "text": "total falls while f < 0",
     "placement": "inside",
     "at": "rows x = 3 to 8"
    }
   ]
  },
  "sources": [
   "research/units/unit-06-integration-accumulation.md#6.1 Exploring Accumulations of Change",
   "BC-QA-06004"
  ]
 },
 "prerequisite_bridges": [
  {
   "prq_id": "BC-PRQ-06005",
   "text": "f(t) is the rate at input t."
  },
  {
   "prq_id": "BC-PRQ-06007",
   "text": "A semicircle is half a circle."
  }
 ],
 "time": {
  "exam_part": "II-B",
  "budget_minutes": 15.0,
  "source": "research/exam/exam-structure.md#Section and part layout",
  "written_steps": {
   "ex-1": [
    5,
    6
   ],
   "ex-2": [
    5
   ]
  },
  "skipped_steps": {
   "ex-1": [
    1,
    2,
    3,
    4
   ],
   "ex-2": [
    1,
    2,
    3,
    4
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
   "archetype_id": "BC-QA-06004",
   "parameter_draw": {
    "heights": [
     2,
     2,
     0,
     -2
    ],
    "lower": 0,
    "circle": "below",
    "direction": "forward"
   },
   "completes": "ex-1",
   "stem": {
    "text": "The signed pieces of ∫_0^8 f(x) dx are 3, -2 and -2π. Find the integral.",
    "command_verb": "find"
   },
   "key": {
    "form": "symbolic",
    "expr": "1 - 2*pi"
   },
   "steps": [
    {
     "text": "Add the signed pieces.",
     "expr": "3 - 2 - 2*pi",
     "relation": "new"
    },
    {
     "text": "Simplify.",
     "expr": "1 - 2*pi",
     "relation": "equivalent"
    }
   ],
   "calculator_status": "no_calculator",
   "skills": [
    "BC-SKL-06004"
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
   "archetype_id": "BC-QA-06004",
   "parameter_draw": {
    "heights": [
     3,
     3,
     0,
     -3
    ],
    "lower": 1,
    "circle": "above",
    "direction": "forward"
   },
   "stem": {
    "text": "f: segments through (0, 3), (1, 3), (2, 0), (3, -3), (4, 0), then a radius 2 semicircle above [4, 8]. Find ∫_1^8 f(x) dx.",
    "command_verb": "find"
   },
   "key": {
    "form": "symbolic",
    "expr": "2*pi - 3/2"
   },
   "steps": [
    {
     "text": "Triangle above on [1, 2].",
     "expr": "(1/2)*1*3",
     "relation": "new"
    },
    {
     "text": "Triangle below on [2, 4].",
     "expr": "-(1/2)*2*3",
     "relation": "new"
    },
    {
     "text": "Semicircle above.",
     "expr": "(1/2)*pi*2**2",
     "relation": "new"
    },
    {
     "text": "Sum.",
     "expr": "3/2 - 3 + 2*pi",
     "relation": "new"
    },
    {
     "text": "Simplify.",
     "expr": "2*pi - 3/2",
     "relation": "equivalent"
    }
   ],
   "calculator_status": "no_calculator",
   "skills": [
    "BC-SKL-06004"
   ]
  },
  {
   "id": "chk-3",
   "check_kind": "mcq",
   "format": "mcq",
   "bands": [
    "low"
   ],
   "archetype_id": "BC-QA-06015",
   "parameter_draw": {
    "context": "water",
    "start": 2,
    "length": 4,
    "display": "average",
    "direction": "accumulates"
   },
   "stem": {
    "text": "Water flows into a tank at R(t) gallons per hour. Which interprets (1/4)∫_2^6 R(t) dt?",
    "command_verb": "interpret"
   },
   "key": {
    "form": "statement",
    "expr": "average_rate_gallons_per_hour_on_2_to_6"
   },
   "options": [
    {
     "id": "A",
     "is_key": true,
     "label": "The average rate of flow, in gallons per hour, over 2 ≤ t ≤ 6.",
     "error_path": null
    },
    {
     "id": "B",
     "is_key": false,
     "label": "The total gallons that flow in over 2 ≤ t ≤ 6.",
     "error_path": "BC-ERR-06030",
     "derivation": "the average value expression read as a total"
    },
    {
     "id": "C",
     "is_key": false,
     "label": "The average rate of flow, in gallons per hour.",
     "error_path": "BC-ERR-06029",
     "derivation": "the interval omitted"
    },
    {
     "id": "D",
     "is_key": false,
     "label": "The change in gallons in the tank from t = 2 to t = 6.",
     "error_path": "BC-ERR-06030",
     "derivation": "the leading one quarter ignored, the expression read as the change"
    }
   ],
   "calculator_status": "no_calculator",
   "skills": [
    "BC-SKL-06001"
   ]
  }
 ],
 "delivery": [
  {
   "block": "orientation",
   "mode": "figure",
   "reason": "rule 4: BC-REP-02 on BC-SKL-06001 and BC-SKL-06004 (unit README delivery map)",
   "sources": [
    "BC-SKL-06001",
    "BC-SKL-06004"
   ],
   "spec": {
    "kind": "graph",
    "representations": [
     "BC-REP-02"
    ],
    "window": {
     "x": [
      0,
      8
     ],
     "y": [
      -3,
      3
     ]
    },
    "curves": [
     {
      "type": "polyline",
      "points": [
       [
        0,
        2
       ],
       [
        1,
        2
       ],
       [
        2,
        0
       ],
       [
        3,
        -2
       ],
       [
        4,
        0
       ]
      ]
     },
     {
      "type": "semicircle",
      "center": [
       6,
       0
      ],
      "radius": 2,
      "side": "below"
     }
    ],
    "shading": [
     {
      "between": "graph and x axis",
      "interval": [
       0,
       8
      ]
     }
    ],
    "labels": [
     {
      "text": "rate f",
      "placement": "inside",
      "at": "near (0.5, 2)"
     },
     {
      "text": "shaded: change in the quantity",
      "placement": "inside",
      "at": "top right"
     }
    ]
   },
   "fallback": "the same shaded graph as a static image with its two labels",
   "keyboard": "none needed: the figure has no control"
  },
  {
   "block": "ki-1",
   "mode": "figure",
   "reason": "rule 4: BC-REP-02 on BC-SKL-06001; not promoted, since the stems ask for a sentence or a value, not a reading of a varying quantity",
   "sources": [
    "BC-SKL-06001"
   ],
   "spec": {
    "kind": "graph",
    "representations": [
     "BC-REP-02"
    ],
    "window": {
     "x": [
      0,
      8
     ],
     "y": [
      -3,
      3
     ]
    },
    "curves": [
     {
      "type": "polyline",
      "points": [
       [
        0,
        2
       ],
       [
        1,
        2
       ],
       [
        2,
        0
       ],
       [
        3,
        -2
       ],
       [
        4,
        0
       ]
      ]
     },
     {
      "type": "semicircle",
      "center": [
       6,
       0
      ],
      "radius": 2,
      "side": "below"
     }
    ],
    "shading": [
     {
      "interval": [
       0,
       2
      ],
      "sign": "plus"
     },
     {
      "interval": [
       2,
       8
      ],
      "sign": "minus"
     }
    ],
    "labels": [
     {
      "text": "gain",
      "placement": "inside",
      "at": "region on [0, 2]"
     },
     {
      "text": "loss",
      "placement": "inside",
      "at": "region on [2, 8]"
     }
    ]
   },
   "fallback": "the same graph, static, with the gain and loss regions labelled",
   "keyboard": "none needed: the figure has no control"
  },
  {
   "block": "ki-2",
   "mode": "figure",
   "reason": "rule 4: BC-REP-02 on BC-SKL-06004; the pieces and their formulas sit on one static graph",
   "sources": [
    "BC-SKL-06004"
   ],
   "spec": {
    "kind": "graph",
    "representations": [
     "BC-REP-02"
    ],
    "window": {
     "x": [
      0,
      8
     ],
     "y": [
      -3,
      3
     ]
    },
    "curves": [
     {
      "type": "polyline",
      "points": [
       [
        0,
        2
       ],
       [
        1,
        2
       ],
       [
        2,
        0
       ],
       [
        3,
        -2
       ],
       [
        4,
        0
       ]
      ]
     },
     {
      "type": "semicircle",
      "center": [
       6,
       0
      ],
      "radius": 2,
      "side": "below"
     }
    ],
    "partition": [
     0,
     2,
     4,
     8
    ],
    "labels": [
     {
      "text": "3",
      "placement": "inside",
      "at": "region on [0, 2]"
     },
     {
      "text": "-(1/2)(2)(2)",
      "placement": "inside",
      "at": "region on [2, 4]"
     },
     {
      "text": "-(1/2)π(2)^2",
      "placement": "inside",
      "at": "semicircle"
     }
    ]
   },
   "fallback": "the same graph, static, with the three signed areas written in their regions",
   "keyboard": "none needed: the figure has no control"
  },
  {
   "block": "ex-1",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  },
  {
   "block": "ex-2",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  },
  {
   "block": "err-BC-ERR-06014",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  },
  {
   "block": "err-BC-ERR-06030",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  },
  {
   "block": "err-BC-ERR-06013",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  },
  {
   "block": "err-BC-ERR-06029",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  },
  {
   "block": "representations",
   "mode": "model",
   "reason": "template model row: BC-CON-06001 is the unit's productive-failure target (app/engine/constants.py PRODUCTIVE_FAILURE_TARGETS) through BC-QA-06004, which carries BC-DF-13; the running total is a computed sequence of values",
   "sources": [
    "BC-QA-06004",
    "BC-CON-06001"
   ],
   "spec": {
    "kind": "numeric_experiment",
    "representations": [
     "BC-REP-02",
     "BC-REP-03"
    ],
    "function": "2*(abs(x) - abs(x - 1) + 1)/2 + 4*((abs(x - 1) - abs(x - 3) + 4)/2 - 1) - (((abs(x - 1) - abs(x - 3) + 4)/2)**2 - 1) + (((abs(x - 3) - abs(x - 4) + 7)/2)**2 - 9) - 8*((abs(x - 3) - abs(x - 4) + 7)/2 - 3) - (((abs(x - 4) - abs(x - 8))/2)*sqrt(4 - ((abs(x - 4) - abs(x - 8))/2)**2)/2 + 2*asin((abs(x - 4) - abs(x - 8))/4) + pi)",
    "computed": "F(x) = ∫_0^x f(t) dt, the running total; the field function holds F, not the rate f",
    "x_values": [
     1,
     2,
     3,
     4,
     6,
     8
    ],
    "columns": [
     "x",
     "F(x), running total"
    ],
    "labels": [
     {
      "text": "x",
      "placement": "inside",
      "at": "first column header"
     },
     {
      "text": "rises while f > 0, falls while f < 0",
      "placement": "inside",
      "at": "row below the last value"
     }
    ]
   },
   "fallback": "the six computed rows printed as a static table beside the static graph, with the closing label",
   "keyboard": "a Run control reached by Tab and pressed with Enter or Space adds one row per press; the table is read in row order"
  }
 ],
 "refresher": [
  "ki-1",
  "ki-2",
  "err-BC-ERR-06014",
  "err-BC-ERR-06030",
  "err-BC-ERR-06013",
  "err-BC-ERR-06029",
  "ex-1"
 ],
 "research_lines": [
  {
   "file": "research/units/unit-06-integration-accumulation.md",
   "line": "For a rate of change function f on [a,b], the signed area of the region between the graph of f and the x axis over [a,b] is the accumulated change in the quantity whose rate is f."
  },
  {
   "file": "research/scoring/common-point-losses.md",
   "line": "An interpretation point asks what a computed value means in the setting of the problem, in words, with the quantity and the interval named."
  }
 ],
 "inferred": [
  {
   "claim": "Worked example 1 is drawn from BC-QA-06004 although the bundle lists BC-QA-06015 first, because BC-QA-06004 carries the BC-DF-13 productive-failure opener and a CAS-checkable value.",
   "settles": "A ruling on whether the productive-failure archetype outranks the primary archetype for example 1."
  },
  {
   "claim": "The time part is II-B from ex-1's archetype, a one point share of about 1.67 minutes; BC-QA-06015 is calculator status either and would take I-A.",
   "settles": "Timing data per step once the fluency telemetry exists, and a BC-PT record for the interpretation part."
  },
  {
   "claim": "The rate unit, gallons per hour, is chosen for the context label water; parameter_spec names no units.",
   "settles": "A units field in BC-QA-06015's parameter_spec."
  },
  {
   "claim": "The comparison gap names the opener attempt as a plain area sum.",
   "settles": "Opener attempt logs once the productive-failure opener is wired (plan 15, Within a concept)."
  },
  {
   "claim": "Every non-text delivery mode, including the model on the representations block.",
   "settles": "The modality A/B in the build plan: skip rate and time to first credited success by mode."
  }
 ],
 "sources": [
  "BC-CON-06001",
  "BC-SKL-06001",
  "BC-SKL-06004",
  "BC-EK-CHA-4A1",
  "BC-EK-CHA-4A2",
  "ced:118",
  "BC-QA-06004",
  "BC-QA-06015",
  "BC-PT-99069",
  "sg-25:18",
  "sg-24:12",
  "sg-23:2",
  "sg-24:3",
  "BC-ERR-06014",
  "BC-ERR-06030",
  "BC-ERR-06013",
  "BC-ERR-06029",
  "BC-MIS-08024",
  "BC-MIS-08019",
  "BC-MIS-08009",
  "BC-PRQ-06005",
  "BC-PRQ-06007",
  "research/units/unit-06-integration-accumulation.md#6.1 Exploring Accumulations of Change",
  "research/question-analysis/question-archetypes.md#BC-QA-06004 Definite integral evaluated from a graph by geometry",
  "research/question-analysis/question-archetypes.md#BC-QA-06015 Interpreting a definite integral in context with units",
  "research/exam/exam-structure.md#Section and part layout",
  "research/scoring/common-point-losses.md#Interpretation points"
 ],
 "read_minutes": {
  "full": 5.4,
  "brief": 3.0
 },
 "word_count": {
  "full": 797,
  "brief": 448
 }
}
```
