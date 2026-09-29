---
title: LSN-CON-02008 Differentiability implies continuity
research_date: 2026-09-29
status: designed
purpose: Authoring spec for the concept lesson on BC-CON-02008, differentiability implies continuity, built from authoring_bundle("BC-CON-02008") and the research files it cites, so an author fills plan 15's lesson record without making a teaching decision.
---

# LSN-CON-02008 Differentiability implies continuity

Concept BC-CON-02008 (skills BC-SKL-02019, BC-SKL-02020, BC-SKL-02024), topic 2.4 of Unit 2, loaded by BC-QA-02004 only. The structure follows LSN-CON-02013.

## Prediction

Served first, both bands, on ex-1's numbers (source BC-CON-02008 concept record and the topic's 2.4 section). Form `mcq`, three options, key: the limit equals \(-2\), the value of \(g\) at 2. The other options are the readings that treat differentiability as silent about the limit. The resolution states the implication and what it gives on this draw, without a verdict word.

## Orientation

Served text (45 words), from BC-CON-02008 `description_plain` and the topic's Assessment behaviour paragraph (research/units/unit-02-differentiation-definition-properties.md#2.4 Connecting Differentiability and Continuity: Determining When Derivatives Do and Do Not Exist): continuity is written as derived from the stated differentiability, and the implication is used inside a larger argument to replace a limit by a value or to meet an existence theorem's hypothesis (sg-25:12, sg-23:14). No count, no frequency.

## Key ideas

One BC-EK maps to the three skills, BC-EK-FUN-2A1 (ced:63), so one core block, both bands.

- ki-1 (core). The implication, the domain remark, the one way direction and the contrapositive, paraphrased from the topic's Required mathematical knowledge paragraph (Implication, Contrapositive, Justification standard). No anchor quote, to hold the brief cap. Notation line from the concept record: differentiable implies continuous.

## Recognition

- BC-QA-02004 (family differentiability-and-continuity, one part of a free response question, no calculator; research/question-analysis/question-archetypes.md#BC-QA-02004 Continuity deduced from differentiability inside a larger argument): `typical_wording` "Justify the conclusion, stating any property of the function that your argument relies on"; `common_givens` a statement that the function is differentiable, function values at the ends of an interval, a limit of a quotient built from the function; `asked_to_produce` a statement that the function is continuous because it is differentiable, an answer justified from the theorem, a limit value after the continuity step. The signal is the word differentiable in the stem, before the parts, with a part that needs continuity. The archetype lists no `official_examples`; the topic names the 2025 and 2023 parts (sg-25:12, sg-23:14).

The contrast pair on st-1 takes its near miss from the sibling concept BC-CON-02009 and the `wrong_approaches` entry behind BC-ERR-02012: a stem that gives continuity and asks about the derivative (BC-QA-02005). The `this` stem is a fresh draw on BC-QA-02004.

What says "not this concept": the stem gives continuity and asks whether the derivative exists (BC-CON-02009, BC-QA-02005); the stem gives a piecewise rule and asks about a corner or cusp (BC-CON-02009).

## Method choice

One strategy block, both bands.

- st-1, BC-QA-02004. Cue from `asked_to_produce` and `common_givens`. Method, `expected_solution_path[0]`, written without a leading label: read the differentiability statement from the stem and write that \(g\) is differentiable, so \(g\) is continuous. The contrast pair rides on this block. Rival, `wrong_approaches`: inferring differentiability from continuity (BC-ERR-02012) or applying the theorem without establishing continuity from differentiability (BC-ERR-99008). Separating feature: which property the stem supplies.

## Solution path

- ex-1, BC-QA-02004, both bands, no calculator. Draw: inputs 0, 2, 5, 8; values \(-3, -2, 3, 7\); slopes 1, \(-3\), 2, 4; scale 3, offset 5, target 1, argument limit. Steps follow `expected_solution_path`: the continuity sentence (no value), the limit replaced by \(3g(2)+5\) (valued), the value \(-1\). A fluent solver writes all three; the continuity sentence is never skipped because it is the reason the limit step rests on.
- ex-2, BC-QA-02004, low band, the same table with argument existence and target 1: continuity from differentiability, the target bracketed by \(g(0)\) and \(g(8)\) through a negative product, and the conclusion. The product line is held in the head; the bracketing inequality is written. Faded from step 3: steps 1 and 2 are shown (the continuity sentence and the product setup, the one valued step), the student writes the answer, and steps 3 and 4 (the product's value and the conclusion) then reveal. The fade falls there because the setup is the only step that needs the theorem's condition named.

No productive-failure opener targets this concept, so no comparison callout.

## Scoring

None. BC-QA-02004 lists no `point_types`, so no example tags a point type, no reader checklist is served and the lesson says nothing about points beyond the error records' own consequence text.

## Traps

Three active errors meet the concept's skills, in the bundle's order. Low band all three, mid band the first two.

- err-BC-ERR-02011 (BC-MIS-02005). Wrong: continuity stated bare, then the limit \(-1\). Right: continuity because differentiable, then \(-1\). Equivalent values: the reason, not the number, is what the record's consequence names. Possible reason from BC-MIS-02005.
- err-BC-ERR-02012 (BC-MIS-02006). Wrong: continuity at 2 used to claim differentiability. Right: the implication run from differentiability. Equivalent values. Possible reason from BC-MIS-02006.
- err-BC-ERR-99008 (BC-MIS-99009). On ex-2: the theorem named with the bracketing but no continuity. Right: continuity derived first. Equivalent values. Possible reason from BC-MIS-99009.

## Representations

One low band figure from the topic's Representations paragraph (a graph to a verdict on differentiability, BC-REP-02 to BC-REP-04): a line with a jump at \(x=1\), labelled inside, carrying the contrapositive of BC-SKL-02024.

## Prerequisite bridge

None. The bundle lists no BC-PRQ parent of BC-SKL-02019, 02020 or 02024.

## Time

BC-QA-02004 is `no_calculator` and one part of a multipart free response question, so the part is Section II Part B, 15.0 minutes per question (research/exam/exam-structure.md#Section and part layout; plan 15, Fluency). The continuity sentence is one line inside that budget. On ex-1 a fluent solver writes the sentence, the substituted limit and the value; on ex-2 the sentence, the bracketing inequality and the conclusion, holding the product in the head.

## Checks

- chk-1, completion of ex-1, both bands: the continuity step is given, the student writes the value. Key \(-1\), equal to ex-1's answer.
- chk-2, isomorph on BC-QA-02004, both bands: \(\lim_{x\to3}(2g(x)-1)\) with \(g(3)=-4\). Key \(-9\).
- chk-3, MCQ on BC-QA-02004, low band, statement key: which response justifies a zero of \(g\) on \((1,6)\). Key D. Distractors: A (BC-ERR-02011, continuity without reason), B (BC-ERR-02012, implication reversed), C (BC-ERR-99008, theorem without continuity).

No draw equals a published BC-QA-02004 `parameter_draw` (content/items_gen_unit02).

## Delivery

- orientation: text. Rule 5, verbal statements (BC-REP-04 on BC-SKL-02019).
- ki-1: text. Rule 5, the implication is a verbal rule; unit README delivery map.
- ex-1: step_reveal, the table of supplied values inside the problem (BC-REP-03 on BC-SKL-02020). Rule 1.
- ex-2: step_reveal. Rule 1.
- err-BC-ERR-02011, err-BC-ERR-02012, err-BC-ERR-99008: step_reveal. Rule 1.
- representations: figure. It is the drawn block, so no `no_figure_reason`. Rule 3, BC-REP-02 on BC-SKL-02024; nothing varies, so no promotion. Static figure with both labels inside, fallback alt text, no control [inferred; settled by the modality A/B].

## Band plan

- Low (full): prediction, orientation, ki-1, st-1 with the contrast pair, ex-1, chk-1, err-BC-ERR-02011, err-BC-ERR-02012, err-BC-ERR-99008, ex-2 faded from step 3, chk-2, representations, chk-3. 694 words, 4.7 minutes (cap 900 and 6).
- Mid (brief): prediction, orientation, ki-1, st-1 with the contrast pair, ex-1, chk-1, err-BC-ERR-02011, err-BC-ERR-02012, chk-2. 449 words, 3.0 minutes (cap 450 and 3).
- Refresher: ki-1, err-BC-ERR-02011, err-BC-ERR-02012, err-BC-ERR-99008, ex-1.

## Sources

- BC-CON-02008; BC-SKL-02019, BC-SKL-02020, BC-SKL-02024; BC-EK-FUN-2A1; ced:63
- BC-QA-02004; BC-QA-02005 (the contrast near miss)
- BC-ERR-02011, BC-ERR-02012, BC-ERR-99008; BC-MIS-02005, BC-MIS-02006, BC-MIS-99009
- sg-25:12, sg-23:14
- research/units/unit-02-differentiation-definition-properties.md#2.4 Connecting Differentiability and Continuity: Determining When Derivatives Do and Do Not Exist
- research/question-analysis/question-archetypes.md#BC-QA-02004 Continuity deduced from differentiability inside a larger argument
- research/exam/exam-structure.md#Section and part layout
- [inferred] The static figure for the contrapositive. Settled by the modality A/B.
- [inferred] BC-QA-02004's research page shows no common givens or outputs while the snapshot record carries them. Settled by a library reconciliation pass.

## Machine record

```json
{
 "id": "LSN-CON-02008",
 "kind": "concept",
 "target_id": "BC-CON-02008",
 "unit": "02",
 "skills": [
  "BC-SKL-02019",
  "BC-SKL-02020",
  "BC-SKL-02024"
 ],
 "prediction": {
  "id": "pr-1",
  "stem": {
   "text": "Predict before the rule: \\(g\\) is differentiable for all \\(x\\) and \\(g(2)=-2\\). What is true of \\(\\lim_{x\\to2}g(x)\\)?",
   "command_verb": "predict"
  },
  "format": "mcq",
  "options": [
   {
    "id": "A",
    "label": "The limit equals \\(-2\\).",
    "is_key": true
   },
   {
    "id": "B",
    "label": "The limit may differ from \\(-2\\).",
    "is_key": false
   },
   {
    "id": "C",
    "label": "The limit need not exist.",
    "is_key": false
   }
  ],
  "resolution": "Differentiable at 2 means continuous at 2, so \\(\\lim_{x\\to2}g(x)=g(2)=-2\\).",
  "sources": [
   "BC-CON-02008",
   "research/units/unit-02-differentiation-definition-properties.md#2.4 Connecting Differentiability and Continuity: Determining When Derivatives Do and Do Not Exist"
  ]
 },
 "orientation": {
  "text": "A response writes continuity as derived from a stated differentiability, then uses it to replace a limit by a value or meet a theorem's hypothesis.",
  "sources": [
   "BC-CON-02008",
   "research/units/unit-02-differentiation-definition-properties.md#2.4 Connecting Differentiability and Continuity: Determining When Derivatives Do and Do Not Exist"
  ]
 },
 "key_ideas": [
  {
   "id": "ki-1",
   "ek_id": "BC-EK-FUN-2A1",
   "depth": "core",
   "text": "A function differentiable at a point is continuous there, and an input outside the domain of \\(f\\) is outside the domain of \\(f'\\). The implication runs one way. Contrapositive: not continuous at a point means not differentiable there. Continuity alone supplies nothing about the derivative.",
   "notation": "differentiable implies continuous",
   "quote": null,
   "sources": [
    "BC-EK-FUN-2A1",
    "ced:63",
    "research/units/unit-02-differentiation-definition-properties.md#2.4 Connecting Differentiability and Continuity: Determining When Derivatives Do and Do Not Exist"
   ]
  }
 ],
 "strategy": [
  {
   "id": "st-1",
   "archetype_id": "BC-QA-02004",
   "cue": "The stem states differentiability and asks for a justified conclusion or a value.",
   "method": "\\(g\\) is differentiable, so \\(g\\) is continuous.",
   "rival": "Reversing the implication, or citing the theorem with no continuity established.",
   "separating_feature": "The stem supplies differentiability, so continuity is the conclusion, never the premise.",
   "sources": [
    "BC-QA-02004"
   ],
   "evidence_tag": "verified",
   "contrast": {
    "this": {
     "text": "Given \\(h\\) differentiable with \\(h(4)=7\\), find \\(\\lim_{x\\to4}(2h(x)-3)\\), justifying the step.",
     "archetype_id": "BC-QA-02004"
    },
    "not_this": {
     "text": "\\(f\\) is continuous at \\(x=2\\). Must \\(f\\) be differentiable there?",
     "why_not": "The premise is continuity, and continuity supplies nothing about the derivative."
    },
    "feature": "Which property the stem supplies: differentiability gives continuity, not the reverse."
   }
  }
 ],
 "worked_examples": [
  {
   "id": "ex-1",
   "archetype_id": "BC-QA-02004",
   "bands": [
    "low",
    "mid"
   ],
   "parameter_draw": {
    "inputs": [
     "0",
     "2",
     "5",
     "8"
    ],
    "values": [
     "-3",
     "-2",
     "3",
     "7"
    ],
    "slopes": [
     "1",
     "-3",
     "2",
     "4"
    ],
    "scale": "3",
    "offset": "5",
    "target": "1",
    "argument": "limit"
   },
   "problem": {
    "text": "The function \\(g\\) is differentiable for all \\(x\\). A table gives \\(g(0)=-3\\), \\(g(2)=-2\\), \\(g(5)=3\\), \\(g(8)=7\\) and \\(g'(0)=1\\), \\(g'(2)=-3\\), \\(g'(5)=2\\), \\(g'(8)=4\\). Find \\(\\lim_{x\\to2}(3g(x)+5)\\), justifying the step.",
    "command_verb": "find"
   },
   "calculator_status": "no_calculator",
   "steps": [
    {
     "cue": "The stem states that \\(g\\) is differentiable.",
     "why": "Differentiability at 2 forces continuity at 2, the hypothesis the limit step needs: \\(g\\) is continuous because it is differentiable."
    },
    {
     "cue": "Continuity at 2 lets the limit be replaced by the value.",
     "why": "\\(\\lim_{x\\to2}g(x)=g(2)\\), so the limit is \\(3g(2)+5\\).",
     "expr": "3*(-2)+5",
     "relation": "new"
    },
    {
     "cue": "The stem asks for a value.",
     "why": "Arithmetic on the substituted line.",
     "expr": "-1",
     "relation": "equivalent"
    }
   ],
   "answer": {
    "form": "numeric",
    "expr": "-1"
   }
  },
  {
   "id": "ex-2",
   "archetype_id": "BC-QA-02004",
   "bands": [
    "low"
   ],
   "fade_from": 3,
   "parameter_draw": {
    "inputs": [
     "0",
     "2",
     "5",
     "8"
    ],
    "values": [
     "-3",
     "-2",
     "3",
     "7"
    ],
    "slopes": [
     "1",
     "-3",
     "2",
     "4"
    ],
    "scale": "3",
    "offset": "5",
    "target": "1",
    "argument": "existence"
   },
   "problem": {
    "text": "For the same \\(g\\), must there be a value \\(c\\) with \\(0<c<8\\) and \\(g(c)=1\\)? Justify the answer.",
    "command_verb": "justify"
   },
   "calculator_status": "no_calculator",
   "steps": [
    {
     "cue": "The theorem needs continuity on \\([0,8]\\); the stem gives differentiability.",
     "why": "\\(g\\) is differentiable, so \\(g\\) is continuous on \\([0,8]\\)."
    },
    {
     "cue": "The target 1 must lie between the endpoint values.",
     "why": "A negative product of the two differences puts 1 between \\(g(0)\\) and \\(g(8)\\).",
     "expr": "(-3-1)*(7-1)",
     "relation": "new"
    },
    {
     "cue": "Evaluate the product.",
     "why": "It is negative, so \\(g(0)<1<g(8)\\).",
     "expr": "-24",
     "relation": "equivalent"
    },
    {
     "cue": "The stem asks whether there must be such a value.",
     "why": "Yes: by the Intermediate Value Theorem some \\(c\\) in \\((0,8)\\) has \\(g(c)=1\\)."
    }
   ],
   "answer": {
    "form": "statement",
    "expr": "yes",
    "text": "Yes. g is continuous because it is differentiable, and g(0) < 1 < g(8)."
   }
  }
 ],
 "what_a_reader_scores": [],
 "common_errors": [
  {
   "error_id": "BC-ERR-02011",
   "observed_behavior": "The response states that the function is continuous without saying that it is continuous because it is differentiable.",
   "scoring_consequence": "The continuity point requires the reason; a bare statement that the function is continuous does not earn it (sg-25:12).",
   "wrong_step": {
    "text": "\\(g\\) is continuous, so the limit is \\(3g(2)+5=-1\\).",
    "expr": "3*(-2)+5"
   },
   "right_step": {
    "text": "\\(g\\) is differentiable, so continuous at 2, and the limit is \\(3g(2)+5=-1\\).",
    "expr": "-1"
   },
   "relation": "equivalent",
   "fix_prompt": false,
   "possible_reason": {
    "misconception_id": "BC-MIS-02005",
    "text": "continuity is asserted rather than derived from the differentiability stated in the stem"
   },
   "sources": [
    "BC-ERR-02011",
    "BC-MIS-02005"
   ]
  },
  {
   "error_id": "BC-ERR-02012",
   "observed_behavior": "The response concludes that a function is differentiable at a point because it is continuous there.",
   "scoring_consequence": "A justification point is lost because the claim is not supported by the theorem.",
   "wrong_step": {
    "text": "\\(g\\) is continuous at 2, so \\(g\\) is differentiable at 2, and the limit is \\(-1\\).",
    "expr": "-1"
   },
   "right_step": {
    "text": "\\(g\\) is differentiable at 2, so \\(g\\) is continuous at 2, and the limit is \\(3g(2)+5\\).",
    "expr": "3*(-2)+5"
   },
   "relation": "equivalent",
   "fix_prompt": false,
   "possible_reason": {
    "misconception_id": "BC-MIS-02006",
    "text": "the implication as running in both directions"
   },
   "sources": [
    "BC-ERR-02012",
    "BC-MIS-02006"
   ]
  },
  {
   "error_id": "BC-ERR-99008",
   "observed_behavior": "Responses apply the Mean Value Theorem, the Intermediate Value Theorem or L'Hospital's Rule without establishing continuity from differentiability, without bounding the target value between two function values, or without confirming the indeterminate form.",
   "scoring_consequence": "The condition point is not earned; in several years this was the point earned by the smallest proportion of responses on the question.",
   "wrong_step": {
    "text": "On ex-2: yes, by the Intermediate Value Theorem, since \\(g(0)<1<g(8)\\).",
    "expr": "(-3-1)*(7-1)"
   },
   "right_step": {
    "text": "\\(g\\) is differentiable, so continuous on \\([0,8]\\); \\(g(0)<1<g(8)\\), so yes.",
    "expr": "-24"
   },
   "relation": "equivalent",
   "fix_prompt": false,
   "possible_reason": {
    "misconception_id": "BC-MIS-99009",
    "text": "continuity is asserted rather than derived from differentiability"
   },
   "sources": [
    "BC-ERR-99008",
    "BC-MIS-99009"
   ]
  }
 ],
 "representations": {
  "text": "By the contrapositive: where the graph breaks, the function is not continuous, so it has no derivative there.",
  "figure": {
   "kind": "graph",
   "curves": [
    {
     "expr": "x + 1",
     "domain": [
      -1,
      1
     ]
    },
    {
     "expr": "x + 3",
     "domain": [
      1,
      3
     ]
    }
   ],
   "points": [
    {
     "at": [
      1,
      2
     ],
     "style": "open"
    },
    {
     "at": [
      1,
      4
     ],
     "style": "filled"
    }
   ],
   "labels": [
    {
     "text": "jump at x = 1",
     "placement": "inside"
    },
    {
     "text": "not continuous, so no derivative at x = 1",
     "placement": "inside"
    }
   ]
  }
 },
 "prerequisite_bridges": [],
 "time": {
  "exam_part": "II-B",
  "budget_minutes": 15.0,
  "source": "research/exam/exam-structure.md#Section and part layout",
  "written_steps": {
   "ex-1": [
    1,
    2,
    3
   ],
   "ex-2": [
    1,
    2,
    4
   ]
  },
  "skipped_steps": {
   "ex-1": [],
   "ex-2": [
    3
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
   "archetype_id": "BC-QA-02004",
   "parameter_draw": {
    "inputs": [
     "0",
     "2",
     "5",
     "8"
    ],
    "values": [
     "-3",
     "-2",
     "3",
     "7"
    ],
    "slopes": [
     "1",
     "-3",
     "2",
     "4"
    ],
    "scale": "3",
    "offset": "5",
    "target": "1",
    "argument": "limit"
   },
   "completes": "ex-1",
   "stem": {
    "text": "\\(g\\) is differentiable, so \\(g\\) is continuous at 2 and \\(\\lim_{x\\to2}(3g(x)+5)=3g(2)+5\\), with \\(g(2)=-2\\). Write the value of the limit.",
    "command_verb": "write"
   },
   "key": {
    "form": "numeric",
    "expr": "-1"
   },
   "steps": [
    {
     "text": "By continuity the limit is \\(3g(2)+5\\).",
     "expr": "3*(-2)+5",
     "relation": "new"
    },
    {
     "text": "That is \\(-1\\).",
     "expr": "-1",
     "relation": "equivalent"
    }
   ],
   "calculator_status": "no_calculator",
   "skills": [
    "BC-SKL-02020"
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
   "archetype_id": "BC-QA-02004",
   "parameter_draw": {
    "inputs": [
     "1",
     "3",
     "4",
     "6"
    ],
    "values": [
     "-5",
     "-4",
     "2",
     "4"
    ],
    "slopes": [
     "2",
     "-1",
     "3",
     "0"
    ],
    "scale": "2",
    "offset": "-1",
    "target": "0",
    "argument": "limit"
   },
   "stem": {
    "text": "\\(g\\) is differentiable for all \\(x\\), with \\(g(3)=-4\\) and \\(g'(3)=-1\\). Find \\(\\lim_{x\\to3}(2g(x)-1)\\).",
    "command_verb": "find"
   },
   "key": {
    "form": "numeric",
    "expr": "-9"
   },
   "steps": [
    {
     "text": "\\(g\\) is differentiable, so continuous at 3, and the limit is \\(2g(3)-1\\).",
     "expr": "2*(-4)-1",
     "relation": "new"
    },
    {
     "text": "That is \\(-9\\).",
     "expr": "-9",
     "relation": "equivalent"
    }
   ],
   "calculator_status": "no_calculator",
   "skills": [
    "BC-SKL-02020"
   ]
  },
  {
   "id": "chk-3",
   "check_kind": "mcq",
   "format": "mcq",
   "bands": [
    "low"
   ],
   "archetype_id": "BC-QA-02004",
   "parameter_draw": {
    "inputs": [
     "1",
     "3",
     "4",
     "6"
    ],
    "values": [
     "-5",
     "-4",
     "2",
     "4"
    ],
    "slopes": [
     "2",
     "-1",
     "3",
     "0"
    ],
    "scale": "2",
    "offset": "-1",
    "target": "0",
    "argument": "existence"
   },
   "stem": {
    "text": "\\(g\\) is differentiable for all \\(x\\), \\(g(1)=-5\\) and \\(g(6)=4\\). Which response justifies that \\(g(c)=0\\) for some \\(c\\) in \\((1,6)\\)?",
    "command_verb": "choose"
   },
   "key": {
    "form": "statement",
    "expr": "D",
    "text": "g is differentiable, so continuous on [1,6], and g(1) < 0 < g(6)."
   },
   "steps": [
    {
     "text": "The differences from the target have product \\((-5-0)(4-0)\\).",
     "expr": "(-5-0)*(4-0)",
     "relation": "new"
    },
    {
     "text": "It is negative, so 0 lies between \\(g(1)\\) and \\(g(6)\\).",
     "expr": "-20",
     "relation": "equivalent"
    }
   ],
   "options": [
    {
     "id": "A",
     "is_key": false,
     "label": "Yes: \\(g\\) is continuous and \\(g(1)<0<g(6)\\).",
     "error_path": "BC-ERR-02011",
     "derivation": "continuity stated with no reason"
    },
    {
     "id": "B",
     "is_key": false,
     "label": "Yes: \\(g\\) is continuous, so \\(g\\) is differentiable, and \\(g(1)<0<g(6)\\).",
     "error_path": "BC-ERR-02012",
     "derivation": "the implication run from continuity to differentiability"
    },
    {
     "id": "C",
     "is_key": false,
     "label": "Yes, by the Intermediate Value Theorem, since \\(g(1)<0<g(6)\\).",
     "error_path": "BC-ERR-99008",
     "derivation": "the theorem applied without establishing continuity"
    },
    {
     "id": "D",
     "is_key": true,
     "label": "Yes: \\(g\\) is differentiable, so \\(g\\) is continuous on \\([1,6]\\), and \\(g(1)<0<g(6)\\).",
     "error_path": null
    }
   ],
   "calculator_status": "no_calculator",
   "skills": [
    "BC-SKL-02020"
   ]
  }
 ],
 "delivery": [
  {
   "block": "orientation",
   "mode": "text",
   "reason": "rule 5: BC-REP-04 verbal statements on BC-SKL-02019; unit README delivery map",
   "sources": [
    "BC-SKL-02019"
   ]
  },
  {
   "block": "ki-1",
   "mode": "text",
   "reason": "rule 5: the implication is a verbal rule (BC-REP-04 on BC-SKL-02019 and 02020); unit README delivery map",
   "sources": [
    "BC-SKL-02019",
    "BC-SKL-02020"
   ]
  },
  {
   "block": "ex-1",
   "mode": "step_reveal",
   "reason": "rule 1; the supplied values render as a table inside the problem (BC-REP-03 on BC-SKL-02020)",
   "sources": [
    "BC-SKL-02020"
   ]
  },
  {
   "block": "ex-2",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  },
  {
   "block": "err-BC-ERR-02011",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  },
  {
   "block": "err-BC-ERR-02012",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  },
  {
   "block": "err-BC-ERR-99008",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  },
  {
   "block": "representations",
   "mode": "figure",
   "reason": "rule 3: BC-REP-02 on BC-SKL-02024, a discontinuity concluding non-differentiability; unit README delivery map; nothing varies, so no promotion",
   "sources": [
    "BC-SKL-02024"
   ],
   "spec": {
    "kind": "graph",
    "window": {
     "x": [
      -1,
      3
     ],
     "y": [
      0,
      6
     ]
    },
    "curves": [
     {
      "expr": "x + 1",
      "domain": [
       -1,
       1
      ]
     },
     {
      "expr": "x + 3",
      "domain": [
       1,
       3
      ]
     }
    ],
    "points": [
     {
      "at": [
       1,
       2
      ],
      "style": "open"
     },
     {
      "at": [
       1,
       4
      ],
      "style": "filled"
     }
    ],
    "labels": [
     {
      "text": "jump at x = 1",
      "placement": "inside"
     },
     {
      "text": "not continuous, so no derivative at x = 1",
      "placement": "inside"
     }
    ]
   },
   "fallback": "Alt text: a line with a jump from height 2 to height 4 at x = 1, and the sentence that a function not continuous at 1 has no derivative there.",
   "keyboard": "none needed: a static figure; its description is reached with Tab"
  }
 ],
 "refresher": [
  "ki-1",
  "err-BC-ERR-02011",
  "err-BC-ERR-02012",
  "err-BC-ERR-99008",
  "ex-1"
 ],
 "read_minutes": {"full": 4.7, "brief": 3.0},
 "word_count": {"full": 694, "brief": 449},
 "research_lines": [
  {
   "file": "research/units/unit-02-differentiation-definition-properties.md",
   "line": "FRQ forms use the implication as a step"
  }
 ],
 "inferred": [
  {
   "claim": "The static figure for the contrapositive serves the reading better than text.",
   "settles": "The modality A/B in the build plan: skip rate and time to first credited success by mode."
  },
  {
   "claim": "BC-QA-02004 records asked_to_produce and common_givens in the snapshot, while research/question-analysis/question-archetypes.md shows none recorded for it.",
   "settles": "A library pass reconciling the research page with data/staging archetype records."
  }
 ],
 "sources": [
  "BC-CON-02008",
  "BC-SKL-02019",
  "BC-SKL-02020",
  "BC-SKL-02024",
  "BC-EK-FUN-2A1",
  "ced:63",
  "BC-QA-02004",
  "BC-ERR-02011",
  "BC-ERR-02012",
  "BC-ERR-99008",
  "BC-MIS-02005",
  "BC-MIS-02006",
  "BC-MIS-99009",
  "sg-25:12",
  "sg-23:14",
  "research/units/unit-02-differentiation-definition-properties.md#2.4 Connecting Differentiability and Continuity: Determining When Derivatives Do and Do Not Exist",
  "research/question-analysis/question-archetypes.md#BC-QA-02004 Continuity deduced from differentiability inside a larger argument",
  "research/exam/exam-structure.md#Section and part layout"
 ]
}
```
