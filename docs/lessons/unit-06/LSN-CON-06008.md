---
title: LSN-CON-06008 Fundamental Theorem of Calculus part one
research_date: 2026-09-29
status: designed
purpose: Authoring spec for the concept lesson on BC-CON-06008, the derivative of an accumulation function as the integrand at the upper limit times the limit's derivative, built from authoring_bundle("BC-CON-06008") and the research files it cites, so an author fills plan 15's lesson record without making a teaching decision.
---

# LSN-CON-06008 Fundamental Theorem of Calculus part one

Concept BC-CON-06008 (skills BC-SKL-06018, BC-SKL-06019, BC-SKL-06021), topic 6.4 of Unit 6, loaded by BC-QA-06012 (primary, family ftc-differentiation) and BC-QA-06003 (accumulation-function-analysis, through BC-SKL-06018). BC-SKL-06021 names BC-CON-06008 as its own concept, so it sits here and not in LSN-CON-06007 (plan 15 Q19; docs/lessons/unit-06/README.md, front notes). Hard parents: BC-CON-06007 through BC-SKL-06017, and the chain rule BC-SKL-03002 for BC-SKL-06019.

## Prediction

One multiple choice question on worked example 1's own function, h(x) the integral from 1 to 2x^2 of (t^2 - 3) dt, asked before the rule is shown: what h'(1) is. The key is 4, ex-1's answer. The distractors are the integrand at the upper limit with no chain factor, 1 (the BC-ERR-06027 path), and the integrand at x = 1, negative 2. The resolution, shown on the key idea screen beside the choice, states the integrand at the upper limit times the limit's derivative. No verdict word. Sources: BC-CON-06008 and the topic 6.4 section the key idea cites.

## Orientation

Served text, from BC-CON-06008 `description_plain` and the topic's Assessment behaviour paragraph (research/units/unit-06-integration-accumulation.md#6.4 The Fundamental Theorem of Calculus and Accumulation Functions): a response writes the derivative as the integrand at the upper limit, times the upper limit's derivative when that limit is a function of x, then evaluates. No count, no frequency.

## Key ideas

All three skills map to BC-EK-FUN-5A2 (ced:121), so one core block, both bands.

- ki-1 (core). Paraphrase of the Required mathematical knowledge paragraphs "Fundamental Theorem of Calculus part one" and "Composite upper limit": with f continuous on an interval containing a, the derivative of the integral from a to x of f(t) dt is f(x); with upper limit u(x) it is f(u(x)) u'(x); the lower limit contributes nothing. The continuity hypothesis (BC-SKL-06021) is named in the text. No anchor quote, to keep the brief band under its cap. Notation line from the concept record.

## Recognition

BC-QA-06012 (research/question-analysis/question-archetypes.md#BC-QA-06012 Differentiating an accumulation function with a variable upper limit): `typical_wording` "the function h is defined by the integral from a fixed input to x of the given expression; find the value of h prime at a stated input"; `asked_to_produce` "the value of the derivative of the accumulation function at a stated input"; `common_givens` a graph of the integrand, a table of values inside the integrand. The signal: a function defined by an integral with a variable in the upper limit, and the word prime or derivative. Shapes: MCQ (BC-MCQ-SAMPLE-007) and a no-calculator FRQ part (BC-FRQ-2024-Q4-C, BC-FRQ-2025-Q4-A).

BC-QA-06003 (research/question-analysis/question-archetypes.md#BC-QA-06003 Accumulation function analysed from the graph of the integrand): "find the value of g prime at a stated input and give a reason" on a graph of f.

Contrast pair on st-1: this stem is on BC-QA-06012, a variable upper limit x^3 with h prime asked; not this stem is a definite integral with numerical limits, the near miss from BC-CON-06012, where an antiderivative gives a value and no chain factor arises. The separating feature is a variable upper limit with the derivative asked.

What says "not this concept": numerical limits and a request for a value select part two (BC-CON-06012); a request for g itself selects BC-CON-06007 (docs/lessons/unit-06/README.md, section 3).

## Method choice

Two strategy blocks; st-1 serves both bands.

- st-1, BC-QA-06012. Method, `expected_solution_path[0]`: state that the derivative equals the integrand at the upper limit. Rival from `wrong_approaches`: the integrand at the upper limit without the chain factor (BC-ERR-06027). Separating feature: an upper limit that is a function of x.
- st-2, BC-QA-06003. Method: `expected_solution_path[0]` evaluates g as signed areas; for g prime the path's second step writes g' = f and reads f at the input. Rival: features read off the plotted f (BC-ERR-06008). Separating feature: g prime is a height of f, g is an area under it.

The reader prints its own labels, so no strategy field begins with one, and each rival's record id sits in the block's `sources`, not in its text. Both archetypes carry `asked_to_produce` and `common_givens`; no block is tagged inferred.

## Solution path

- ex-1, BC-QA-06012, both bands, no calculator. Draw from `parameter_spec`: power 2, scale 2, quadratic 1, constant -3, lower 1, point 1. Derived: top 2, chain_factor 4, value_at_top 1, value_at_point -2, value_at_lower -2, key_value 4; every constraint holds. h(x) is the integral from 1 to 2x^2 of (t^2 - 3) dt; h'(1) = 4. No published BC-QA-06012 item carries this draw.
- Steps follow `expected_solution_path`: the derivative written as the integrand at 2x^2 times 4x (new, tagged BC-PT-99024), x = 1 substituted (evaluate), the value (equivalent, tagged BC-PT-99004). A fluent solver writes all three. There is no example 2, so nothing is faded.

## Scoring

BC-QA-06012 lists BC-PT-99024 and BC-PT-99004. The theorem point is earned by presenting the derivative in terms of the integrand; a correct value without the theorem exhibited can still earn the answer point (BC-QA-06012 `scoring_pattern`, sg-24:15, sg-25:16; research/scoring/point-taxonomy.md#BC-PT-99024 Derivative of an accumulation function by the Fundamental Theorem). The chain factor omitted loses the answer point while the theorem point may stand (BC-ERR-06027, sg-24:15).

## Traps

Two active errors meet the skills, in the bundle's order (both linked BC-MIS at severity medium): BC-ERR-06027, BC-ERR-06028. Both bands serve both. Both relations are distinct, so both are fix prompts (`fix_prompt` true). On ex-1's draw.

- err-BC-ERR-06027: h'(1) = f(2) = 1 against 4. Possible reason, words from BC-MIS-06023.
- err-BC-ERR-06028: the derivative left as t^2 - 3 against ((2x^2)^2 - 3)(4x). Possible reason, words from BC-MIS-06024.

## Representations

None as a separate block. ki-1's figure carries the height of f at the upper limit.

## Prerequisite bridge

- BC-PRQ-06005 and BC-PRQ-06013, each from its `description_plain` and `failure_signature`.

## Time

BC-QA-06012 is `no_calculator`, one part of a multipart FRQ or a single MCQ, so the FRQ shape is Section II Part B, 15.0 minutes per question (research/exam/exam-structure.md#Section and part layout); its two points are a share of about 3.33 minutes (docs/lessons/unit-06/README.md, section 5) [inferred]. The minutes go on the chain factor and the substitution; nothing is held.

## Checks

- chk-1, completion of ex-1, both bands: the derivative line is given; the student evaluates at 1. Key 4.
- chk-2, isomorph, both bands. Draw: power 1, scale 3, quadratic 1, constant -2, lower 0, point 1; h(x) = integral from 0 to 3x of (t^2 - 2) dt. Key 21.
- No chk-3: the bundle holds two errors and a 4-option MCQ needs three distractors, each anchored to a distinct error block (listed in the inferred array).

## Delivery

- prediction: text [inferred; settled by the modality A/B].
- orientation: text. Rule 6.
- ki-1: figure. Rule 4: BC-REP-02 on BC-SKL-06018; not promoted, since BC-QA-06012's `difficulty_variables` vary a form (upper limit x or a function of x), not a quantity (docs/lessons/unit-06/README.md, section 6) [inferred; settled by the modality A/B].
- ex-1, err-BC-ERR-06027, err-BC-ERR-06028: step_reveal. Rule 1.

The drawn block ki-1 (figure) is already present, so no figure is added and no `no_figure_reason` is stated.

## Band plan

- Low (full), in served order: prediction, orientation, ki-1, st-1 with its contrast pair, st-2, ex-1 with its scoring lines, chk-1, both error blocks, chk-2, both bridges. 489 words, 3.3 minutes (cap 900 and 6). There is no example 2, so nothing is faded.
- Mid (brief): the same blocks less st-2. 442 words, 3.0 minutes (cap 450 and 3). The orientation, ki-1, the st-1 fields, the contrast, the prediction and the bridges were shortened to fit; both scoring tags stay.
- Refresher: ki-1, err-BC-ERR-06027, err-BC-ERR-06028, ex-1.

## Sources

- BC-CON-06008; BC-SKL-06018, BC-SKL-06019, BC-SKL-06021; BC-EK-FUN-5A2; ced:121
- BC-QA-06012, BC-QA-06003; BC-PT-99024, BC-PT-99004; sg-24:15, sg-25:16
- BC-ERR-06027, BC-ERR-06028; BC-MIS-06023, BC-MIS-06024
- BC-PRQ-06005, BC-PRQ-06013
- research/units/unit-06-integration-accumulation.md#6.4 The Fundamental Theorem of Calculus and Accumulation Functions
- research/question-analysis/question-archetypes.md#BC-QA-06012 Differentiating an accumulation function with a variable upper limit
- research/question-analysis/question-archetypes.md#BC-QA-06003 Accumulation function analysed from the graph of the integrand
- BC-ERR-06027 and BC-ERR-06008, each cited in a strategy block's `sources`
- research/scoring/point-taxonomy.md#BC-PT-99024 Derivative of an accumulation function by the Fundamental Theorem
- research/exam/exam-structure.md#Section and part layout
- [inferred] The 3.33 minute share of a two-point part. Settled by timing data per part.
- [inferred] The contrast near miss, numerical limits with a value asked, is a stem written for this pair. Settled by a published near-miss item.
- [inferred] ki-1 as a static figure. Settled by the modality A/B.
- [inferred] Two checks, not three. Settled by a third BC-ERR on BC-SKL-06018 or BC-SKL-06019.

## Machine record

```json
{
 "id": "LSN-CON-06008",
 "kind": "concept",
 "target_id": "BC-CON-06008",
 "unit": "06",
 "skills": [
  "BC-SKL-06018",
  "BC-SKL-06019",
  "BC-SKL-06021"
 ],
 "prediction": {
  "id": "pr-1",
  "stem": {
   "text": "Predict. \\(h(x)=\\int_1^{2x^2}(t^2-3)\\,dt\\). Find \\(h'(1)\\).",
   "command_verb": "predict"
  },
  "format": "mcq",
  "options": [
   {
    "id": "A",
    "label": "1",
    "is_key": false
   },
   {
    "id": "B",
    "label": "4",
    "is_key": true
   },
   {
    "id": "C",
    "label": "Negative 2",
    "is_key": false
   }
  ],
  "resolution": "The derivative is the integrand at the upper limit times the limit's derivative: \\(1\\cdot 4=4\\).",
  "sources": [
   "BC-CON-06008",
   "research/units/unit-06-integration-accumulation.md#6.4 The Fundamental Theorem of Calculus and Accumulation Functions"
  ]
 },
 "orientation": {
  "text": "A response writes h' as the integrand at the upper limit, times the limit's derivative.",
  "sources": [
   "BC-CON-06008",
   "research/units/unit-06-integration-accumulation.md#6.4 The Fundamental Theorem of Calculus and Accumulation Functions"
  ]
 },
 "key_ideas": [
  {
   "id": "ki-1",
   "ek_id": "BC-EK-FUN-5A2",
   "depth": "core",
   "text": "For continuous f, the derivative with upper limit u(x) is f(u(x)) times u'(x); u(x) = x gives f(x). The lower limit adds nothing.",
   "notation": "\\(\\frac{d}{dx}\\int_a^x f(t)\\,dt=f(x)\\)",
   "quote": null,
   "sources": [
    "BC-EK-FUN-5A2",
    "ced:121",
    "research/units/unit-06-integration-accumulation.md#6.4 The Fundamental Theorem of Calculus and Accumulation Functions"
   ]
  }
 ],
 "strategy": [
  {
   "id": "st-1",
   "archetype_id": "BC-QA-06012",
   "cue": "Variable upper limit; h prime asked.",
   "method": "h' equals the integrand at the upper limit.",
   "rival": "No chain factor.",
   "separating_feature": "An upper limit that is a function of x.",
   "sources": [
    "BC-QA-06012",
    "BC-ERR-06027"
   ],
   "evidence_tag": "verified",
   "contrast": {
    "this": {
     "text": "\\(h(x)=\\int_2^{x^3}(t+1)\\,dt\\). Find \\(h'(1)\\).",
     "archetype_id": "BC-QA-06012"
    },
    "not_this": {
     "text": "Find \\(\\int_1^2 (t^2-3)\\,dt\\).",
     "why_not": "Its limits are numbers, so an antiderivative applies."
    },
    "feature": "A variable upper limit, with the derivative asked."
   }
  },
  {
   "id": "st-2",
   "archetype_id": "BC-QA-06003",
   "cue": "g from a graph of f; g prime at an input, with a reason.",
   "method": "g as signed areas; for g prime, g' = f read at the input.",
   "rival": "Features read off the plotted f.",
   "separating_feature": "g prime is a height of f; g is an area under it.",
   "sources": [
    "BC-QA-06003",
    "BC-ERR-06008"
   ],
   "evidence_tag": "verified"
  }
 ],
 "worked_examples": [
  {
   "id": "ex-1",
   "archetype_id": "BC-QA-06012",
   "bands": [
    "low",
    "mid"
   ],
   "parameter_draw": {
    "power": 2,
    "scale": 2,
    "quadratic": 1,
    "constant": -3,
    "lower": 1,
    "point": 1
   },
   "problem": {
    "text": "h(x) = integral from 1 to 2x^2 of (t^2 - 3) dt. Find h'(1).",
    "command_verb": "find"
   },
   "calculator_status": "no_calculator",
   "steps": [
    {
     "cue": "Upper limit 2x^2, a function of x.",
     "why": "Integrand at the limit, times 4x.",
     "expr": "((2*x**2)**2 - 3)*4*x",
     "relation": "new",
     "point_type_id": "BC-PT-99024"
    },
    {
     "cue": "The stem asks at x = 1.",
     "why": "Limit 2, factor 4.",
     "expr": "(2**2 - 3)*4",
     "relation": "evaluate",
     "subs": {
      "x": "1"
     }
    },
    {
     "cue": "Simplify.",
     "why": "The value is read.",
     "expr": "4",
     "relation": "equivalent",
     "point_type_id": "BC-PT-99004"
    }
   ],
   "answer": {
    "form": "symbolic",
    "expr": "4"
   }
  }
 ],
 "what_a_reader_scores": [
  {
   "example_id": "ex-1",
   "point_type_ids": [
    "BC-PT-99024",
    "BC-PT-99004"
   ],
   "lines": [
    {
     "point_type_id": "BC-PT-99024",
     "text": "Derivative of an accumulation function by the Fundamental Theorem. Earned by: Writing the derivative of the accumulation function as the integrand evaluated at the variable, in general or at the requested value (sg-25:16, sg-24:13). Not earned by: Differencing the integrand at the two limits, which sg-25:16 states earns the answer point but not this one."
    },
    {
     "point_type_id": "BC-PT-99004",
     "text": "Answer with or without supporting work. Earned by: The correct value on its own, with no supporting work required (sg-25:3, sg-26:4). Not earned by: A value outside the accepted precision, or a value inconsistent with a required earlier step where the rubric imposes one. Precision: A reported decimal answer must be accurate to three places after the decimal point, rounded or truncated; at most one point per question is lost to inappropriate rounding (sg-25:2, sg-26:2). sg-26:4 also accepts a stated rounding to the nearest integer and several truncations."
    }
   ]
  }
 ],
 "common_errors": [
  {
   "error_id": "BC-ERR-06027",
   "observed_behavior": "The derivative of an accumulation function with a composite upper limit is reported as the integrand at that limit with no extra factor.",
   "scoring_consequence": "The answer point is not earned even though the theorem point may be (sg-24:15).",
   "wrong_step": {
    "text": "f(2) = 1.",
    "expr": "1"
   },
   "right_step": {
    "text": "f(2) times 4.",
    "expr": "4"
   },
   "relation": "distinct",
   "possible_reason": {
    "misconception_id": "BC-MIS-06023",
    "text": "applies the theorem as a fixed template regardless of what the upper limit is"
   },
   "sources": [
    "BC-ERR-06027",
    "BC-MIS-06023"
   ],
   "fix_prompt": true
  },
  {
   "error_id": "BC-ERR-06028",
   "observed_behavior": "The response evaluates the integrand at the dummy variable or leaves the answer in terms of t.",
   "scoring_consequence": "The answer point is not earned because the derivative is not expressed in the independent variable.",
   "wrong_step": {
    "text": "t^2 - 3.",
    "expr": "t**2 - 3"
   },
   "right_step": {
    "text": "((2x^2)^2 - 3)(4x).",
    "expr": "((2*x**2)**2 - 3)*4*x"
   },
   "relation": "distinct",
   "possible_reason": {
    "misconception_id": "BC-MIS-06024",
    "text": "does not distinguish the bound variable inside the integral from the variable in the upper limit"
   },
   "sources": [
    "BC-ERR-06028",
    "BC-MIS-06024"
   ],
   "fix_prompt": true
  }
 ],
 "representations": null,
 "prerequisite_bridges": [
  {
   "prq_id": "BC-PRQ-06005",
   "text": "f(u(x)) is f read at u(x)."
  },
  {
   "prq_id": "BC-PRQ-06013",
   "text": "t stays inside; limits carry x."
  }
 ],
 "time": {
  "exam_part": "II-B",
  "budget_minutes": 15.0,
  "source": "research/exam/exam-structure.md#Section and part layout",
  "written_steps": {
   "ex-1": [
    1,
    2,
    3
   ]
  },
  "skipped_steps": {
   "ex-1": []
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
   "archetype_id": "BC-QA-06012",
   "parameter_draw": {
    "power": 2,
    "scale": 2,
    "quadratic": 1,
    "constant": -3,
    "lower": 1,
    "point": 1
   },
   "completes": "ex-1",
   "stem": {
    "text": "h'(x) = ((2x^2)^2 - 3)(4x). Find h'(1).",
    "command_verb": "find"
   },
   "key": {
    "form": "symbolic",
    "expr": "4"
   },
   "steps": [
    {
     "text": "The derivative.",
     "expr": "((2*x**2)**2 - 3)*4*x",
     "relation": "new"
    },
    {
     "text": "x = 1.",
     "expr": "4",
     "relation": "evaluate",
     "subs": {
      "x": "1"
     }
    }
   ],
   "calculator_status": "no_calculator",
   "skills": [
    "BC-SKL-06019"
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
   "archetype_id": "BC-QA-06012",
   "parameter_draw": {
    "power": 1,
    "scale": 3,
    "quadratic": 1,
    "constant": -2,
    "lower": 0,
    "point": 1
   },
   "stem": {
    "text": "h(x) = integral from 0 to 3x of (t^2 - 2) dt. Find h'(1).",
    "command_verb": "find"
   },
   "key": {
    "form": "symbolic",
    "expr": "21"
   },
   "steps": [
    {
     "text": "Integrand at 3x, times 3.",
     "expr": "((3*x)**2 - 2)*3",
     "relation": "new"
    },
    {
     "text": "x = 1.",
     "expr": "21",
     "relation": "evaluate",
     "subs": {
      "x": "1"
     }
    }
   ],
   "calculator_status": "no_calculator",
   "skills": [
    "BC-SKL-06019"
   ]
  }
 ],
 "delivery": [
  {
   "block": "orientation",
   "mode": "text",
   "reason": "rule 6: a statement of what a response writes",
   "sources": [
    "BC-SKL-06018"
   ]
  },
  {
   "block": "ki-1",
   "mode": "figure",
   "reason": "rule 4: BC-REP-02 on BC-SKL-06018; not promoted, since BC-QA-06012 difficulty_variables vary a form, not a quantity",
   "sources": [
    "BC-SKL-06018",
    "BC-QA-06012"
   ],
   "spec": {
    "kind": "graph",
    "representations": [
     "BC-REP-02"
    ],
    "window": {
     "x": [
      0,
      5
     ],
     "y": [
      -4,
      14
     ]
    },
    "curves": [
     {
      "expr": "t**2 - 3",
      "domain": [
       0,
       4
      ]
     }
    ],
    "drawn": [
     "the region from t = 1 to t = 2 shaded",
     "a vertical segment from the axis to the curve at t = 2"
    ],
    "labels": [
     {
      "text": "lower limit 1",
      "placement": "inside"
     },
     {
      "text": "upper limit 2x^2 = 2 at x = 1",
      "placement": "inside"
     },
     {
      "text": "height f(2) = 1, times u'(1) = 4",
      "placement": "inside"
     }
    ]
   },
   "fallback": "the same figure described in text: the height of f at the upper limit, times the derivative of the limit",
   "keyboard": "none needed; the figure has no control"
  },
  {
   "block": "ex-1",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  },
  {
   "block": "err-BC-ERR-06027",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  },
  {
   "block": "err-BC-ERR-06028",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  }
 ],
 "refresher": [
  "ki-1",
  "err-BC-ERR-06027",
  "err-BC-ERR-06028",
  "ex-1"
 ],
 "read_minutes": {
  "full": 3.3,
  "brief": 3.0
 },
 "word_count": {
  "full": 489,
  "brief": 442
 },
 "research_lines": [
  {
   "file": "research/units/unit-06-integration-accumulation.md",
   "line": "With the chain rule, the derivative of the integral from a to u(x) of f(t) dt equals f(u(x)) times u'(x)."
  }
 ],
 "inferred": [
  {
   "claim": "A two-point FTC part takes about 3.33 of the 15.0 Section II minutes.",
   "settles": "Timing data per part once the fluency telemetry exists."
  },
  {
   "claim": "ki-1 is served as a static figure rather than text.",
   "settles": "The modality A/B in the build plan: skip rate and time to first credited success by mode."
  },
  {
   "claim": "The lesson carries two checks: the bundle holds two errors, BC-ERR-06027 and BC-ERR-06028, and check 3 needs three distractors anchored to error blocks.",
   "settles": "A third active BC-ERR on BC-SKL-06018, BC-SKL-06019 or BC-SKL-06021."
  }
 ],
 "sources": [
  "BC-CON-06008",
  "BC-SKL-06018",
  "BC-SKL-06019",
  "BC-SKL-06021",
  "BC-EK-FUN-5A2",
  "ced:121",
  "BC-QA-06012",
  "BC-QA-06003",
  "BC-PT-99024",
  "BC-PT-99004",
  "sg-24:15",
  "sg-25:16",
  "BC-ERR-06027",
  "BC-ERR-06028",
  "BC-MIS-06023",
  "BC-MIS-06024",
  "BC-PRQ-06005",
  "BC-PRQ-06013",
  "research/units/unit-06-integration-accumulation.md#6.4 The Fundamental Theorem of Calculus and Accumulation Functions",
  "research/question-analysis/question-archetypes.md#BC-QA-06012 Differentiating an accumulation function with a variable upper limit",
  "research/exam/exam-structure.md#Section and part layout"
 ]
}
```
