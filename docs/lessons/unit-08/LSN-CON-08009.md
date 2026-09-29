---
title: LSN-CON-08009 Meaning of a definite integral in context
research_date: 2026-09-29
status: designed
purpose: Authoring spec for the concept lesson on BC-CON-08009, the sentence that interprets a definite integral of a rate with its quantity, interval and units, built from authoring_bundle("BC-CON-08009") and the research files it cites, so an author fills plan 15's lesson record without making a teaching decision.
---

# LSN-CON-08009 Meaning of a definite integral in context

Concept BC-CON-08009 (skill BC-SKL-08015), topic 8.3 of Unit 8, loaded by one archetype, BC-QA-06015 (family accumulation-interpretation), which Unit 6 shares. It has no Unit 8 hard parent (docs/lessons/unit-08/README.md, section 1).

## Prediction

One multiple choice question on worked example 1's own quantities, asked before the rule is shown: snow piles onto a driveway at S(t) cubic feet per hour with t in hours, and the student picks the units of the integral of S from t = 4 to t = 10. The key is cubic feet; the distractors are cubic feet per hour and hours. The resolution, shown on the key idea screen, multiplies the units and names the amount added over the interval. No verdict word. Sources: BC-CON-08009 and the topic 8.3 section the key ideas cite. [inferred]

## Orientation

Served text, from BC-CON-08009 `description_plain` and the topic's Assessment behaviour paragraph (research/units/unit-08-applications-integration.md#8.3 Using Accumulation Functions and Definite Integrals in Applied Contexts): a response writes one sentence naming the quantity that accumulates, the interval from the limits, and units that multiply the rate's units by the input's units. No count, no frequency.

## Key ideas

BC-SKL-08015 maps to BC-EK-CHA-4D1 and BC-EK-CHA-4D2 (both ced:154): two core blocks, both bands.

- ki-1 (core, BC-EK-CHA-4D1). Paraphrase of the Required mathematical knowledge paragraph (Accumulation): an integral of a rate accumulates it; the integrand says what changes per unit of input, and the units of the integral are the rate's units times the input's units. Anchor quote from ced:154.
- ki-2 (core, BC-EK-CHA-4D2). Paraphrase of the paragraphs (Accumulation; Interpretation): the integral over an interval is the net change over that interval, not the amount present, and a complete interpretation names the quantity, the interval and the units (sg-23:2). Anchor quote from ced:154. Notation line on both from the concept record.

## Recognition

BC-QA-06015 (research/question-analysis/question-archetypes.md#BC-QA-06015 Interpreting a definite integral in context with units): `typical_wording` "using correct units, interpret the meaning of the displayed definite integral in the context of the problem"; `common_givens` a contextual rate function, a definite integral expression; `asked_to_produce` a sentence with quantity, interval, and units. The signal: the verb "interpret" beside a displayed integral and the words "using correct units". Shapes: one part of a free response question or an MCQ; the archetype notes name 2023 Q1(a) and 2024 Q1(b); no `official_examples` in the record.

The contrast pair on st-1 sets a BC-QA-06015 stem (interpret a bare displayed integral with correct units) against the same stem with a leading factor of one over the interval length. The near miss comes from the average-value reading, BC-CON-08002 (a sibling concept), which the design's not-this list names; its units stay the rate's units. The feature is a bare integral, an accumulated amount, not an average.

What says "not this concept": "find the value" of the same integral (computation, BC-CON-08006); a leading factor of one over the interval length, which makes it an average (BC-CON-08002).

## Method choice

One strategy block, both bands.

- st-1, BC-QA-06015, carrying the contrast pair. Cue from `asked_to_produce` and `common_givens`. Method, `expected_solution_path[0]`: identify what the integrand measures per unit input, then multiply the units. Rival, `wrong_approaches`: naming the quantity without the interval; giving the units of the rate (BC-ERR-08017, BC-ERR-99005). Separating feature: an accumulated amount carries the product of units and both limits. Both fields are present, so the block is not tagged inferred. The served fields carry no leading label.

## Solution path

- ex-1, BC-QA-06015, both bands, statement answer. Draw from `parameter_spec`: context snow, start 4, length 6, display total, direction accumulates; so the integral runs from 4 to 10. No published BC-QA-06015 item carries this draw.
- Steps follow `expected_solution_path`: the integrand as a rate (no value); the units multiplied (new); the units cancelled (equivalent); the interval from the limits (no value); the sentence (no value). A fluent solver writes only the sentence; the units product is held [inferred]. One example only, so no `fade_from`.

## Scoring

BC-QA-06015 lists no `point_types`, so the lesson carries no what_a_reader_scores entry, no point tag, and says nothing about points beyond the error records' `scoring_consequence`. For the author: the archetype's scoring pattern is one interpretation point that needs the quantity with its units and the interval (sg-23:2; research/scoring/common-point-losses.md#Interpretation points), and units are scored separately from a value where asked (research/scoring/common-point-losses.md#Units points).

## Traps

Two active errors meet the skill, in the bundle's order: BC-ERR-08017, BC-ERR-99005. Both bands serve both. On ex-1's draw.

- err-BC-ERR-08017: the sentence without "from t = 4 to t = 10". The units agree, so the wrong and right unit expressions are equivalent; the loss is the interval in the text. Possible reason, words from BC-MIS-08009.
- err-BC-ERR-99005: cubic feet per hour, the rate's units, against cubic feet. Possible reason, words from BC-MIS-02008.

## Representations

None. The topic's Representations paragraph names verbal and symbolic conversions, none figure-shaped for this concept.

## Prerequisite bridge

- BC-PRQ-06005, from its `description_plain` and `failure_signature`.

## Time

BC-QA-06015 is `either`; the design takes Section I Part A, 2.14 minutes per question (research/exam/exam-structure.md#Section and part layout) [inferred: an either archetype placed in I-A]. As a free response part it is one point, 1.67 minutes (docs/lessons/unit-08/README.md, section 5). The minute goes on the sentence; the units product is held.

## Checks

- chk-1, completion of ex-1, both bands: the units and limits given, the sentence. Key statement, the ex-1 sentence.
- chk-2, isomorph, both bands. Draw: context people, start 9, length 3, display total, direction depletes; people leave a stadium at L(t) people per minute. Key statement: the number of people who leave from t = 9 to t = 12 minutes.
- chk-3, MCQ, low band. Draw: context oil, start 1, length 5, display total, direction accumulates. Key statement with gallons and the interval. Distractors: no interval (BC-ERR-08017); gallons per hour (BC-ERR-99005); no units (BC-ERR-99005).

## Delivery

- orientation: text. Rule 6: BC-REP-04 and BC-REP-05 on BC-SKL-08015 draw nothing; unit README delivery map.
- ki-1, ki-2: text. Rule 6, same field.
- ex-1: step_reveal. Rule 1.
- Figure presence: no drawn block. No rule of 2 to 5 applies, since BC-REP-04 and 05 are not figure-bearing and the key ideas describe no process, so the record carries `no_figure_reason`.
- err-BC-ERR-08017, err-BC-ERR-99005: step_reveal. Rule 1.

## Band plan

- Low (full), in served order: prediction, orientation, the bridge, ki-1, ki-2, st-1 with its contrast, ex-1, chk-1, both error blocks, chk-2, chk-3. 518 words, 3.5 minutes (cap 900 and 6).
- Mid (brief): the same without chk-3. 442 words, 3.0 minutes (cap 450 and 3). To fit the cap the orientation, both key idea texts, the st-1 fields, the ex-1 cues and whys and the bridge were shortened; both anchor quotes stay.
- Refresher: ki-1, ki-2, err-BC-ERR-08017, err-BC-ERR-99005, ex-1.

## Sources

- BC-CON-08009; BC-SKL-08015; BC-EK-CHA-4D1, BC-EK-CHA-4D2; ced:154
- BC-QA-06015; sg-23:2
- BC-ERR-08017, BC-ERR-99005; BC-MIS-08009, BC-MIS-02008
- BC-PRQ-06005
- research/units/unit-08-applications-integration.md#8.3 Using Accumulation Functions and Definite Integrals in Applied Contexts
- research/question-analysis/question-archetypes.md#BC-QA-06015 Interpreting a definite integral in context with units
- research/scoring/common-point-losses.md#Interpretation points
- research/scoring/common-point-losses.md#Units points
- research/exam/exam-structure.md#Section and part layout
- [inferred] The prediction and the contrast pair as teaching moves. Settled by the modality and prompt A/B in the build plan.
- [inferred] BC-QA-06015 is either; the lesson takes I-A. Settled by a ruling on which part an either archetype's budget comes from.
- [inferred] The units attached to each context (cubic feet for snow, people for people, gallons for oil). Settled by a unit field in BC-QA-06015's parameter_spec.
- [inferred] The units product is held in the head. Settled by timing data per step from 10's fluency telemetry.

## Machine record

```json
{
 "id": "LSN-CON-08009",
 "kind": "concept",
 "target_id": "BC-CON-08009",
 "unit": "08",
 "skills": [
  "BC-SKL-08015"
 ],
 "prediction": {
  "id": "pr-1",
  "stem": {
   "text": "Predict: snow piles onto a driveway at \\(S(t)\\) cubic feet per hour, with \\(t\\) in hours. What are the units of the integral of \\(S\\) from \\(t=4\\) to \\(t=10\\)?",
   "command_verb": "predict"
  },
  "format": "mcq",
  "options": [
   {
    "id": "A",
    "label": "Cubic feet per hour",
    "is_key": false
   },
   {
    "id": "B",
    "label": "Cubic feet",
    "is_key": true
   },
   {
    "id": "C",
    "label": "Hours",
    "is_key": false
   }
  ],
  "resolution": "Cubic feet per hour times hours gives cubic feet, so the integral is an amount of snow, the amount added from \\(t=4\\) to \\(t=10\\).",
  "sources": [
   "BC-CON-08009",
   "research/units/unit-08-applications-integration.md#8.3 Using Accumulation Functions and Definite Integrals in Applied Contexts"
  ]
 },
 "no_figure_reason": "The skill's representations are verbal and contextual, none figure-bearing, and the key ideas describe no process; the deliverable is one sentence with units.",
 "orientation": {
  "text": "A response names the quantity, the interval and the units in one sentence.",
  "sources": [
   "BC-CON-08009",
   "research/units/unit-08-applications-integration.md#8.3 Using Accumulation Functions and Definite Integrals in Applied Contexts"
  ]
 },
 "key_ideas": [
  {
   "id": "ki-1",
   "ek_id": "BC-EK-CHA-4D1",
   "depth": "core",
   "text": "An integral of a rate accumulates it: the integrand is change per unit of input, and the integral's units are the rate's units times the input's.",
   "notation": "interpretation with units",
   "quote": {
    "text": "A function defined as an integral represents an accumulation of a rate of change.",
    "source": "ced:154"
   },
   "sources": [
    "BC-EK-CHA-4D1",
    "ced:154",
    "research/units/unit-08-applications-integration.md#8.3 Using Accumulation Functions and Definite Integrals in Applied Contexts"
   ]
  },
  {
   "id": "ki-2",
   "ek_id": "BC-EK-CHA-4D2",
   "depth": "core",
   "text": "Over an interval the integral is the change in the quantity, not the amount present; an interpretation names the quantity, interval and units.",
   "notation": "interpretation with units",
   "quote": {
    "text": "The definite integral of the rate of change of a quantity over an interval gives the net change of that quantity over that interval.",
    "source": "ced:154"
   },
   "sources": [
    "BC-EK-CHA-4D2",
    "ced:154",
    "sg-23:2",
    "research/units/unit-08-applications-integration.md#8.3 Using Accumulation Functions and Definite Integrals in Applied Contexts"
   ]
  }
 ],
 "strategy": [
  {
   "id": "st-1",
   "archetype_id": "BC-QA-06015",
   "cue": "A contextual rate and a displayed integral; a sentence with quantity, interval and units.",
   "method": "What the integrand measures, units multiplied.",
   "rival": "No interval, or the rate's units.",
   "separating_feature": "Units multiplied, both limits named.",
   "sources": [
    "BC-QA-06015"
   ],
   "evidence_tag": "verified",
   "contrast": {
    "this": {
     "text": "Sand falls at \\(F(t)\\) tons per minute. Using correct units, interpret the meaning of \\(\\int_2^5 F(t)\\,dt\\).",
     "archetype_id": "BC-QA-06015"
    },
    "not_this": {
     "text": "Sand falls at \\(F(t)\\) tons per minute. Interpret \\(\\frac{1}{3}\\int_2^5 F(t)\\,dt\\).",
     "why_not": "The factor of one over the interval length makes it an average rate."
    },
    "feature": "A bare integral is an accumulated amount, not an average."
   }
  }
 ],
 "worked_examples": [
  {
   "id": "ex-1",
   "archetype_id": "BC-QA-06015",
   "bands": [
    "low",
    "mid"
   ],
   "parameter_draw": {
    "context": "snow",
    "start": 4,
    "length": 6,
    "display": "total",
    "direction": "accumulates"
   },
   "problem": {
    "text": "Snow piles onto a driveway at \\(S(t)\\) cubic feet per hour, \\(t\\) in hours. Using correct units, interpret \\(\\int_4^{10} S(t)\\,dt\\).",
    "command_verb": "interpret"
   },
   "calculator_status": "no_calculator",
   "steps": [
    {
     "cue": "A rate.",
     "why": "Cubic feet per hour."
    },
    {
     "cue": "Multiply units.",
     "why": "Times hours.",
     "expr": "feet**3/hour*hour",
     "relation": "new"
    },
    {
     "cue": "Hours cancel.",
     "why": "An amount.",
     "expr": "feet**3",
     "relation": "equivalent"
    },
    {
     "cue": "Limits name the interval.",
     "why": "\\(t=4\\) to \\(t=10\\)."
    },
    {
     "cue": "Write the sentence.",
     "why": "Quantity, units, interval."
    }
   ],
   "answer": {
    "form": "statement",
    "expr": "feet**3",
    "text": "The cubic feet of snow that pile onto the driveway from t = 4 to t = 10 hours."
   }
  }
 ],
 "what_a_reader_scores": [],
 "common_errors": [
  {
   "error_id": "BC-ERR-08017",
   "observed_behavior": "The sentence says what is accumulating without saying between which inputs.",
   "scoring_consequence": "The interpretation point is lost because the guideline requires the interval as well as the quantity (sg-23:2).",
   "wrong_step": {
    "text": "The cubic feet of snow on the driveway.",
    "expr": "feet**3"
   },
   "right_step": {
    "text": "The cubic feet that pile on from \\(t=4\\) to \\(t=10\\).",
    "expr": "feet**3"
   },
   "relation": "equivalent",
   "possible_reason": {
    "misconception_id": "BC-MIS-08009",
    "text": "the sentence as a label for the integral"
   },
   "sources": [
    "BC-ERR-08017",
    "BC-MIS-08009"
   ],
   "fix_prompt": false
  },
  {
   "error_id": "BC-ERR-99005",
   "observed_behavior": "Responses give no units where units are requested, or report units of the original quantity instead of the derived one, for example words per minute for a second difference quotient.",
   "scoring_consequence": "The units point is not earned; it is scored separately from the value.",
   "wrong_step": {
    "text": "Cubic feet per hour.",
    "expr": "feet**3/hour"
   },
   "right_step": {
    "text": "Cubic feet.",
    "expr": "feet**3"
   },
   "relation": "distinct",
   "possible_reason": {
    "misconception_id": "BC-MIS-02008",
    "text": "units as optional"
   },
   "sources": [
    "BC-ERR-99005",
    "BC-MIS-02008"
   ],
   "fix_prompt": true
  }
 ],
 "representations": null,
 "prerequisite_bridges": [
  {
   "prq_id": "BC-PRQ-06005",
   "text": "\\(S(t)\\) is a rate; the limits are times."
  }
 ],
 "time": {
  "exam_part": "I-A",
  "budget_minutes": 2.14,
  "source": "research/exam/exam-structure.md#Section and part layout",
  "written_steps": {
   "ex-1": [
    5
   ]
  },
  "skipped_steps": {
   "ex-1": [
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
   "archetype_id": "BC-QA-06015",
   "parameter_draw": {
    "context": "snow",
    "start": 4,
    "length": 6,
    "display": "total",
    "direction": "accumulates"
   },
   "completes": "ex-1",
   "stem": {
    "text": "The units are cubic feet and the limits 4 and 10 hours. Write the interpretation of \\(\\int_4^{10} S(t)\\,dt\\).",
    "command_verb": "interpret"
   },
   "key": {
    "form": "statement",
    "expr": "feet**3",
    "text": "The cubic feet of snow that pile onto the driveway from t = 4 to t = 10 hours."
   },
   "steps": [
    {
     "text": "Units.",
     "expr": "feet**3/hour*hour",
     "relation": "new"
    },
    {
     "text": "Cubic feet.",
     "expr": "feet**3",
     "relation": "equivalent"
    }
   ],
   "calculator_status": "no_calculator",
   "skills": [
    "BC-SKL-08015"
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
   "archetype_id": "BC-QA-06015",
   "parameter_draw": {
    "context": "people",
    "start": 9,
    "length": 3,
    "display": "total",
    "direction": "depletes"
   },
   "stem": {
    "text": "People leave a stadium at \\(L(t)\\) people per minute, \\(t\\) in minutes. Interpret \\(\\int_9^{12} L(t)\\,dt\\) with units.",
    "command_verb": "interpret"
   },
   "key": {
    "form": "statement",
    "expr": "people",
    "text": "The number of people who leave the stadium from t = 9 to t = 12 minutes."
   },
   "steps": [
    {
     "text": "Units.",
     "expr": "people/minute*minute",
     "relation": "new"
    },
    {
     "text": "People.",
     "expr": "people",
     "relation": "equivalent"
    }
   ],
   "calculator_status": "no_calculator",
   "skills": [
    "BC-SKL-08015"
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
    "context": "oil",
    "start": 1,
    "length": 5,
    "display": "total",
    "direction": "accumulates"
   },
   "stem": {
    "text": "Oil flows into a tank at \\(R(t)\\) gallons per hour. Which interprets \\(\\int_1^6 R(t)\\,dt\\)?",
    "command_verb": "interpret"
   },
   "key": {
    "form": "statement",
    "expr": "gallons_into_tank_on_1_to_6"
   },
   "options": [
    {
     "id": "A",
     "is_key": false,
     "label": "The gallons of oil that flow into the tank.",
     "error_path": "BC-ERR-08017",
     "derivation": "the interval omitted"
    },
    {
     "id": "B",
     "is_key": true,
     "label": "The gallons of oil that flow into the tank from t = 1 to t = 6 hours.",
     "error_path": null
    },
    {
     "id": "C",
     "is_key": false,
     "label": "The gallons per hour of oil that flow into the tank from t = 1 to t = 6 hours.",
     "error_path": "BC-ERR-99005",
     "derivation": "the rate's units kept"
    },
    {
     "id": "D",
     "is_key": false,
     "label": "The oil that flows into the tank from t = 1 to t = 6.",
     "error_path": "BC-ERR-99005",
     "derivation": "no units"
    }
   ],
   "calculator_status": "no_calculator",
   "skills": [
    "BC-SKL-08015"
   ]
  }
 ],
 "delivery": [
  {
   "block": "orientation",
   "mode": "text",
   "reason": "rule 6: BC-REP-04 and BC-REP-05 on BC-SKL-08015 draw nothing; unit README delivery map",
   "sources": [
    "BC-SKL-08015"
   ]
  },
  {
   "block": "ki-1",
   "mode": "text",
   "reason": "rule 6: a units rule in words",
   "sources": [
    "BC-SKL-08015"
   ]
  },
  {
   "block": "ki-2",
   "mode": "text",
   "reason": "rule 6: what a sentence must name",
   "sources": [
    "BC-SKL-08015"
   ]
  },
  {
   "block": "ex-1",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  },
  {
   "block": "err-BC-ERR-08017",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  },
  {
   "block": "err-BC-ERR-99005",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  }
 ],
 "refresher": [
  "ki-1",
  "ki-2",
  "err-BC-ERR-08017",
  "err-BC-ERR-99005",
  "ex-1"
 ],
 "read_minutes": {
  "full": 3.5,
  "brief": 3.0
 },
 "word_count": {
  "full": 518,
  "brief": 442
 },
 "research_lines": [
  {
   "file": "research/units/unit-08-applications-integration.md",
   "line": "A complete interpretation names the quantity, the interval, and the units (sg-23:2)."
  }
 ],
 "inferred": [
  {
   "claim": "BC-QA-06015 is an either archetype; the lesson takes Section I Part A and its 2.14 minute budget.",
   "settles": "A ruling on which exam part an either archetype's budget comes from."
  },
  {
   "claim": "The units attached to each context: cubic feet for snow, people for people, gallons for oil.",
   "settles": "A unit field in BC-QA-06015's parameter_spec."
  },
  {
   "claim": "A fluent solver writes only the sentence and holds the units product.",
   "settles": "Timing data per step from 10's fluency telemetry."
  }
 ],
 "sources": [
  "BC-CON-08009",
  "BC-SKL-08015",
  "BC-EK-CHA-4D1",
  "BC-EK-CHA-4D2",
  "ced:154",
  "BC-QA-06015",
  "sg-23:2",
  "BC-ERR-08017",
  "BC-ERR-99005",
  "BC-MIS-08009",
  "BC-MIS-02008",
  "BC-PRQ-06005",
  "research/units/unit-08-applications-integration.md#8.3 Using Accumulation Functions and Definite Integrals in Applied Contexts",
  "research/question-analysis/question-archetypes.md#BC-QA-06015 Interpreting a definite integral in context with units",
  "research/scoring/common-point-losses.md#Interpretation points",
  "research/scoring/common-point-losses.md#Units points",
  "research/exam/exam-structure.md#Section and part layout"
 ]
}
```
