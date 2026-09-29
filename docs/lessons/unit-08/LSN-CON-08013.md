---
title: LSN-CON-08013 Region split where the boundary curves cross
research_date: 2026-09-29
status: designed
purpose: Authoring spec for the concept lesson on BC-CON-08013, the area of a region whose boundary curves cross, cut at every crossing and summed or written as one absolute value integral, built from authoring_bundle("BC-CON-08013") and the research files it cites, so an author fills plan 15's lesson record without making a teaching decision.
---

# LSN-CON-08013 Region split where the boundary curves cross

Concept BC-CON-08013 (skills BC-SKL-08027, BC-SKL-08028, BC-SKL-08029, BC-SKL-08030), topic 8.6 of Unit 8, loaded by one archetype, BC-QA-08010 (family area-between-curves). Its hard parents are BC-CON-08010 and BC-CON-08011 (docs/lessons/unit-08/README.md, section 1).

## Prediction

One multiple choice question on worked example 1's own numbers, asked before the rule is shown: f(x) = x^2 - 3x + 4 and g(x) = x + 1 give f - g = (x - 1)(x - 3), and the student picks how the total area over [0, 7/2] is found. The key is three integrals cut at 1 and 3, ex-1's structure; the distractors are one integral of f - g over the whole interval (BC-ERR-08026) and two integrals cut at 1 only (BC-ERR-08025). The option labels are worded rather than written as expressions. The resolution states that the upper curve changes at each crossing and that the area is the sum of three integrals of upper minus lower. No verdict word. Sources: BC-CON-08013 and the topic 8.6 section the key idea cites (ced:157).

## Orientation

Served text, from BC-CON-08013 `description_plain` and the topic's Assessment behaviour paragraph (research/units/unit-08-applications-integration.md#8.6 Finding the Area Between Curves That Intersect at More Than Two Points): a response finds every crossing inside the interval, integrates upper minus lower on each piece and adds the pieces, or integrates the absolute value of the difference. No count, no frequency.

## Key ideas

All four skills map to BC-EK-CHA-5A3 (ced:157): one core block, both bands.

- ki-1 (core). Paraphrase of the Required mathematical knowledge paragraphs (Split regions; Where to split; Equivalence; Notation): where the curves cross, the order of subtraction changes, so the region is cut at every interior solution of f = g; the area is a sum of integrals with the order fixed per piece, or one integral of the absolute value of the difference, which gives the same number and is the form a calculator evaluates; the bars sit inside the integral. Anchor quote from ced:157. Notation line from the concept record.

## Recognition

BC-QA-08010 (research/question-analysis/question-archetypes.md#BC-QA-08010 Area of a region whose boundary curves cross): `typical_wording` "find the total area of the region bounded by the two graphs over the stated interval"; `common_givens` two curve equations, an interval or a figure; `asked_to_produce` a sum of definite integrals or one absolute value integral, the total area. The signal: the word "total" with a stated interval, and f = g having a solution strictly inside it (`difficulty_variables`: the number of interior crossings). Shapes: an MCQ whose distractor is one integral of one difference (the topic's Assessment behaviour paragraph); no 2023 to 2025 BC free response part required a split region.

The near miss served in the contrast pair of st-1 comes from the sibling archetype BC-QA-08008 (BC-CON-08011): the same two curves asked as the area of the region enclosed by them, where the meeting points bound the region and one integral suffices. The pair differs in the one thing the feature names, a stated interval with a crossing inside it.

What says "not this concept": a region enclosed between two meeting points with one curve on top throughout (BC-CON-08010).

## Method choice

One strategy block, both bands.

- st-1, BC-QA-08010, carrying the contrast pair. Cue from `asked_to_produce` and `common_givens`. Method, `expected_solution_path[0]`: solve for every intersection in the interval. Rival, `wrong_approaches`: integrating a fixed difference across a crossing (BC-ERR-08026). Separating feature: a solution of f = g strictly inside the interval. Both fields are present, so the block is not tagged inferred.

## Solution path

- ex-1, BC-QA-08010, both bands, no calculator. Draw from `parameter_spec`: start 0, lead 1, gap 2, overrun 1/2, bulge 1, slope 1, intercept 1, presentation formula; so g(x) = x + 1, f(x) = x^2 - 3x + 4, f - g = (x - 1)(x - 3), interval [0, 7/2], crossings 1 and 3. Pieces 4/3, 4/3, 7/24; total 71/24. No published BC-QA-08010 item carries this draw.
- Steps follow `expected_solution_path`: f = g (new); the crossings (solve); the sign on each piece (no value); one integral per piece (new); the piece values (equivalent); the total (equivalent). A fluent solver writes all but the sign test, which is one line of three signs [inferred].

## Scoring

BC-QA-08010 lists no `point_types`, so the lesson carries no what_a_reader_scores entry, no point tag, and says nothing about points beyond the error records' `scoring_consequence`. For the author: the archetype's scoring pattern (the setup needs every piece) is inferred from the 2023 area part (sg-23:16; research/units/unit-08-applications-integration.md#Unresolved).

## Traps

Four active errors meet the skills, in the bundle's order: BC-ERR-08020, BC-ERR-08025, BC-ERR-08026, BC-ERR-08027. Low band all four; mid band the first two. All on ex-1's draw. All four are fix prompts (`fix_prompt` true, relation distinct).

- err-BC-ERR-08020: lower minus upper on every piece, -71/24. Possible reason, words from BC-MIS-08011.
- err-BC-ERR-08025: the crossing at 3 missed, two pieces, 19/8. Possible reason, words from BC-MIS-08014.
- err-BC-ERR-08026: one integral of f - g over [0, 7/2], 7/24. Possible reason, words from BC-MIS-08014.
- err-BC-ERR-08027: the single integral form without its bars, 7/24 against 71/24. Possible reason, words from BC-MIS-08011.

## Representations

None as a separate block. The topic's Representations paragraph names a figure with several crossings converted to a sum of integrals (BC-REP-02 to BC-REP-01); ki-1's interactive carries it.

## Prerequisite bridge

- BC-PRQ-06005, from its `description_plain` and `failure_signature`.
- BC-PRQ-08001, from its `description_plain` and `failure_signature`.
- BC-PRQ-08003, from its `description_plain` and `failure_signature`.

## Time

BC-QA-08010 is `either`; the design takes Section I Part A, 2.14 minutes per question (research/exam/exam-structure.md#Section and part layout) [inferred: an either archetype placed in I-A]. As a free response part it is two points [inferred from sg-23:16], 3.33 minutes (docs/lessons/unit-08/README.md, section 5). The minutes go on three antiderivative evaluations; on a calculator part the absolute value integral replaces them.

## Checks

- chk-1, completion of ex-1, both bands: the three piece values given, the total. Key 71/24.
- chk-2, isomorph, both bands. Draw: start -1, lead 1, gap 3, overrun 1, bulge 1, slope 0, intercept 2, formula; f(x) = x^2 - 3x + 2, g(x) = 2 on [-1, 4], crossings 0 and 3. Key 49/6.
- chk-3, MCQ, low band. Draw: start 0, lead 3/2, gap 2, overrun 1/2, bulge 1, slope -1, intercept 0, formula; f(x) = x^2 - 6x + 21/4, g(x) = -x on [0, 4], crossings 3/2 and 7/2. Key 5. Distractors: -5 (BC-ERR-08020), 53/12 with 7/2 missed (BC-ERR-08025), 7/3 as one integral (BC-ERR-08026).

## Delivery

- orientation: figure. Rule 4: BC-REP-02 on BC-SKL-08027 and BC-SKL-08028; unit README delivery map.
- ki-1: interactive. Rule 4 promoted: BC-REP-02 on BC-SKL-08027 and BC-SKL-08028, and BC-QA-08010 `difficulty_variables` name "the number of interior crossings", with the stem asking which curve is greater on each piece. One draggable vertical rectangle; the reading is which curve is on top at the dragged input and where the difference changes sign (docs/lessons/unit-08/README.md, section 6) [inferred; settled by the modality A/B].
- ex-1: step_reveal. Rule 1.
- err-BC-ERR-08020, err-BC-ERR-08025, err-BC-ERR-08026, err-BC-ERR-08027: step_reveal. Rule 1.

## Band plan

- Low (full), in served order: prediction, orientation, the three bridges, ki-1, st-1 with the contrast pair, ex-1, chk-1, the four error blocks, chk-2, chk-3. 542 words, 3.7 minutes (cap 900 and 6). There is no second example, so nothing is faded.
- Mid (brief): prediction, orientation, the three bridges, ki-1, st-1 with the contrast pair, ex-1, chk-1, err-BC-ERR-08020, err-BC-ERR-08025, chk-2. 447 words, 3.0 minutes (cap 450 and 3). To fit the cap the orientation, ki-1 (its sentence on the sum of integrals with the order fixed per piece is dropped), the strategy fields, the step cues and whys and the bridges were shortened; the anchor quote was kept, and the archetype has no scoring tag to drop.
- Refresher: ki-1, err-BC-ERR-08020, err-BC-ERR-08025, err-BC-ERR-08026, err-BC-ERR-08027, ex-1.

## Sources

- BC-CON-08013; BC-SKL-08027, BC-SKL-08028, BC-SKL-08029, BC-SKL-08030; BC-EK-CHA-5A3; ced:157
- BC-QA-08010; BC-QA-08008 (the contrast pair's near miss); sg-23:16
- BC-ERR-08020, BC-ERR-08025, BC-ERR-08026, BC-ERR-08027; BC-MIS-08011, BC-MIS-08014
- BC-PRQ-06005, BC-PRQ-08001, BC-PRQ-08003
- research/units/unit-08-applications-integration.md#8.6 Finding the Area Between Curves That Intersect at More Than Two Points
- research/units/unit-08-applications-integration.md#Unresolved
- research/question-analysis/question-archetypes.md#BC-QA-08010 Area of a region whose boundary curves cross
- research/exam/exam-structure.md#Section and part layout
- [inferred] BC-QA-08010 is either; the lesson takes I-A. Settled by a ruling on which part an either archetype's budget comes from.
- [inferred] The free response point count. Settled by a scoring guideline for a split region part.
- [inferred] ki-1 as an interactive and the orientation as a figure; the held sign test. Settled by the modality A/B and timing data per step.

## Machine record

```json
{
 "id": "LSN-CON-08013",
 "kind": "concept",
 "target_id": "BC-CON-08013",
 "unit": "08",
 "skills": [
  "BC-SKL-08027",
  "BC-SKL-08028",
  "BC-SKL-08029",
  "BC-SKL-08030"
 ],
 "prediction": {
  "id": "pr-1",
  "stem": {
   "text": "Predict: \\(f-g=(x-1)(x-3)\\) for \\(f(x)=x^2-3x+4\\) and \\(g(x)=x+1\\). How is the area over \\(0\\le x\\le 7/2\\) found?",
   "command_verb": "predict"
  },
  "format": "mcq",
  "options": [
   {
    "id": "A",
    "label": "One integral of f - g, whole interval",
    "is_key": false
   },
   {
    "id": "B",
    "label": "Three integrals, cut at 1 and 3",
    "is_key": true
   },
   {
    "id": "C",
    "label": "Two integrals, cut at 1 only",
    "is_key": false
   }
  ],
  "resolution": "The curves cross at x = 1 and x = 3, so the upper curve changes. The area is the sum of three integrals of upper minus lower.",
  "sources": [
   "BC-CON-08013",
   "ced:157"
  ]
 },
 "orientation": {
  "text": "A response finds every crossing inside the interval and integrates upper minus lower on each piece.",
  "sources": [
   "BC-CON-08013",
   "research/units/unit-08-applications-integration.md#8.6 Finding the Area Between Curves That Intersect at More Than Two Points"
  ]
 },
 "key_ideas": [
  {
   "id": "ki-1",
   "ek_id": "BC-EK-CHA-5A3",
   "depth": "core",
   "text": "The region is cut at every crossing inside the interval, because the upper curve changes there. The absolute value form gives the same number, with the bars inside the integral.",
   "notation": "sum of definite integrals; absolute value",
   "quote": {
    "text": "a sum of two or more definite integrals or by evaluating a definite integral of the absolute value of the difference of two functions",
    "source": "ced:157"
   },
   "sources": [
    "BC-EK-CHA-5A3",
    "ced:157",
    "research/units/unit-08-applications-integration.md#8.6 Finding the Area Between Curves That Intersect at More Than Two Points"
   ]
  }
 ],
 "strategy": [
  {
   "id": "st-1",
   "archetype_id": "BC-QA-08010",
   "cue": "Total area between two graphs over a stated interval.",
   "method": "\\(f(x)=g(x)\\), solved for every input in the interval.",
   "rival": "One fixed difference integrated across a crossing.",
   "separating_feature": "A crossing strictly inside the interval.",
   "sources": [
    "BC-QA-08010",
    "BC-QA-08008",
    "BC-ERR-08026"
   ],
   "evidence_tag": "verified",
   "contrast": {
    "this": {
     "text": "Find the total area between \\(f(x)=x^2-4x\\) and \\(g(x)=-3\\) for \\(0\\le x\\le 5\\).",
     "archetype_id": "BC-QA-08010"
    },
    "not_this": {
     "text": "Find the area enclosed by \\(f(x)=x^2-4x\\) and \\(g(x)=-3\\).",
     "why_not": "No interval is stated; the region ends at the meeting points."
    },
    "feature": "A crossing inside the stated interval."
   }
  }
 ],
 "worked_examples": [
  {
   "id": "ex-1",
   "archetype_id": "BC-QA-08010",
   "bands": [
    "low",
    "mid"
   ],
   "parameter_draw": {
    "start": 0,
    "lead": "1",
    "gap": 2,
    "overrun": "1/2",
    "bulge": 1,
    "slope": 1,
    "intercept": 1,
    "presentation": "formula"
   },
   "problem": {
    "text": "Find the total area between \\(f(x)=x^2-3x+4\\) and \\(g(x)=x+1\\) for \\(0\\le x\\le 7/2\\).",
    "command_verb": "find"
   },
   "calculator_status": "no_calculator",
   "steps": [
    {
     "cue": "Stated interval: do the curves cross inside it?",
     "why": "Every crossing is a cut.",
     "expr": "x**2 - 3*x + 4 = x + 1",
     "relation": "new"
    },
    {
     "cue": "Factor.",
     "why": "\\((x-1)(x-3)=0\\): three pieces.",
     "expr": "FiniteSet(1, 3)",
     "relation": "solve",
     "variable": "x"
    },
    {
     "cue": "Sign of \\(f-g\\): test 0, 2, 13/4.",
     "why": "\\(f\\), then \\(g\\), then \\(f\\) on top."
    },
    {
     "cue": "Upper minus lower on each piece.",
     "why": "Each piece nonnegative.",
     "expr": "Integral(x**2 - 4*x + 3, (x, 0, 1)) + Integral(4*x - x**2 - 3, (x, 1, 3)) + Integral(x**2 - 4*x + 3, (x, 3, 7/2))",
     "relation": "new"
    },
    {
     "cue": "Evaluate each piece.",
     "why": "\\(F(x)=x^3/3-2x^2+3x\\).",
     "expr": "4/3 + 4/3 + 7/24",
     "relation": "equivalent"
    },
    {
     "cue": "The stem asks for the total.",
     "why": "Sum of the pieces.",
     "expr": "71/24",
     "relation": "equivalent"
    }
   ],
   "answer": {
    "form": "numeric",
    "expr": "71/24"
   }
  }
 ],
 "what_a_reader_scores": [],
 "common_errors": [
  {
   "error_id": "BC-ERR-08020",
   "observed_behavior": "The integrand is the lower curve minus the upper curve, or the left curve minus the right curve.",
   "scoring_consequence": "The integrand point may survive, since either order earned it in 2023, but a negative value reported as an area loses the answer point (sg-23:16, sg-23:17).",
   "wrong_step": {
    "text": "Lower minus upper on each piece: \\(-71/24\\).",
    "expr": "Integral(4*x - x**2 - 3, (x, 0, 1)) + Integral(x**2 - 4*x + 3, (x, 1, 3)) + Integral(4*x - x**2 - 3, (x, 3, 7/2))"
   },
   "right_step": {
    "text": "Upper minus lower: \\(71/24\\).",
    "expr": "Integral(x**2 - 4*x + 3, (x, 0, 1)) + Integral(4*x - x**2 - 3, (x, 1, 3)) + Integral(x**2 - 4*x + 3, (x, 3, 7/2))"
   },
   "relation": "distinct",
   "possible_reason": {
    "misconception_id": "BC-MIS-08011",
    "text": "any sign problem can be repaired at the end"
   },
   "sources": [
    "BC-ERR-08020",
    "BC-MIS-08011"
   ],
   "fix_prompt": true
  },
  {
   "error_id": "BC-ERR-08025",
   "observed_behavior": "Only the outer two crossings are used, so an interior crossing is integrated across.",
   "scoring_consequence": "The setup point is lost because part of the region is subtracted rather than added.",
   "wrong_step": {
    "text": "Crossing 3 missed: \\(19/8\\).",
    "expr": "Integral(x**2 - 4*x + 3, (x, 0, 1)) + Integral(4*x - x**2 - 3, (x, 1, 7/2))"
   },
   "right_step": {
    "text": "Cut at 1 and 3: \\(71/24\\).",
    "expr": "Integral(x**2 - 4*x + 3, (x, 0, 1)) + Integral(4*x - x**2 - 3, (x, 1, 3)) + Integral(x**2 - 4*x + 3, (x, 3, 7/2))"
   },
   "relation": "distinct",
   "possible_reason": {
    "misconception_id": "BC-MIS-08014",
    "text": "a crossing inside the interval does not signal that the region has pieces"
   },
   "sources": [
    "BC-ERR-08025",
    "BC-MIS-08014"
   ],
   "fix_prompt": true
  },
  {
   "error_id": "BC-ERR-08026",
   "observed_behavior": "A fixed order of subtraction is integrated over an interval in which the curves exchange places.",
   "scoring_consequence": "The reported area is smaller than the true area and the setup point is lost.",
   "wrong_step": {
    "text": "One integral: \\(7/24\\).",
    "expr": "Integral(x**2 - 4*x + 3, (x, 0, 7/2))"
   },
   "right_step": {
    "text": "Three pieces: \\(71/24\\).",
    "expr": "71/24"
   },
   "relation": "distinct",
   "possible_reason": {
    "misconception_id": "BC-MIS-08014",
    "text": "treats the area formula as a template applied once"
   },
   "sources": [
    "BC-ERR-08026",
    "BC-MIS-08014"
   ],
   "fix_prompt": true
  },
  {
   "error_id": "BC-ERR-08027",
   "observed_behavior": "The single integral form is written without the absolute value bars around the difference.",
   "scoring_consequence": "The value returned is the signed difference of the lobes, so the answer point is lost.",
   "wrong_step": {
    "text": "No bars: \\(7/24\\).",
    "expr": "Integral(x**2 - 4*x + 3, (x, 0, 7/2))"
   },
   "right_step": {
    "text": "Bars inside: \\(71/24\\).",
    "expr": "Integral(Abs(x**2 - 4*x + 3), (x, 0, 7/2))"
   },
   "relation": "distinct",
   "possible_reason": null,
   "sources": [
    "BC-ERR-08027"
   ],
   "fix_prompt": true
  }
 ],
 "representations": null,
 "prerequisite_bridges": [
  {
   "prq_id": "BC-PRQ-06005",
   "text": "\\(f(2)\\) is one value at one input; else the wrong curve is on top."
  },
  {
   "prq_id": "BC-PRQ-08001",
   "text": "Every solution of \\(f=g\\) in the interval; else cuts are missing."
  },
  {
   "prq_id": "BC-PRQ-08003",
   "text": "\\(\\lvert h\\rvert\\) is \\(h\\) where \\(h\\ge0\\) and \\(-h\\) elsewhere."
  }
 ],
 "time": {
  "exam_part": "I-A",
  "budget_minutes": 2.14,
  "source": "research/exam/exam-structure.md#Section and part layout",
  "written_steps": {
   "ex-1": [
    1,
    2,
    4,
    5,
    6
   ]
  },
  "skipped_steps": {
   "ex-1": [
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
   "archetype_id": "BC-QA-08010",
   "parameter_draw": {
    "start": 0,
    "lead": "1",
    "gap": 2,
    "overrun": "1/2",
    "bulge": 1,
    "slope": 1,
    "intercept": 1,
    "presentation": "formula"
   },
   "completes": "ex-1",
   "stem": {
    "text": "The three pieces are \\(4/3\\), \\(4/3\\) and \\(7/24\\). Find the total area.",
    "command_verb": "find"
   },
   "key": {
    "form": "numeric",
    "expr": "71/24"
   },
   "steps": [
    {
     "text": "Sum.",
     "expr": "4/3 + 4/3 + 7/24",
     "relation": "new"
    },
    {
     "text": "Total.",
     "expr": "71/24",
     "relation": "equivalent"
    }
   ],
   "calculator_status": "no_calculator",
   "skills": [
    "BC-SKL-08029"
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
   "archetype_id": "BC-QA-08010",
   "parameter_draw": {
    "start": -1,
    "lead": "1",
    "gap": 3,
    "overrun": "1",
    "bulge": 1,
    "slope": 0,
    "intercept": 2,
    "presentation": "formula"
   },
   "stem": {
    "text": "Find the total area between \\(f(x)=x^2-3x+2\\) and \\(g(x)=2\\) for \\(-1\\le x\\le 4\\).",
    "command_verb": "find"
   },
   "key": {
    "form": "numeric",
    "expr": "49/6"
   },
   "steps": [
    {
     "text": "\\(f=g\\).",
     "expr": "x**2 - 3*x + 2 = 2",
     "relation": "new"
    },
    {
     "text": "Crossings 0 and 3.",
     "expr": "FiniteSet(0, 3)",
     "relation": "solve",
     "variable": "x"
    },
    {
     "text": "Three pieces.",
     "expr": "Integral(x**2 - 3*x, (x, -1, 0)) + Integral(3*x - x**2, (x, 0, 3)) + Integral(x**2 - 3*x, (x, 3, 4))",
     "relation": "new"
    },
    {
     "text": "\\(11/6+9/2+11/6\\).",
     "expr": "49/6",
     "relation": "equivalent"
    }
   ],
   "calculator_status": "no_calculator",
   "skills": [
    "BC-SKL-08029"
   ]
  },
  {
   "id": "chk-3",
   "check_kind": "mcq",
   "format": "mcq",
   "bands": [
    "low"
   ],
   "archetype_id": "BC-QA-08010",
   "parameter_draw": {
    "start": 0,
    "lead": "3/2",
    "gap": 2,
    "overrun": "1/2",
    "bulge": 1,
    "slope": -1,
    "intercept": 0,
    "presentation": "formula"
   },
   "stem": {
    "text": "What is the total area between \\(f(x)=x^2-6x+21/4\\) and \\(g(x)=-x\\) for \\(0\\le x\\le 4\\)?",
    "command_verb": "find"
   },
   "key": {
    "form": "numeric",
    "expr": "5"
   },
   "steps": [
    {
     "text": "\\(f-g=(x-3/2)(x-7/2)\\).",
     "expr": "x**2 - 5*x + 21/4 = 0",
     "relation": "new"
    },
    {
     "text": "Crossings.",
     "expr": "FiniteSet(3/2, 7/2)",
     "relation": "solve",
     "variable": "x"
    },
    {
     "text": "Three pieces.",
     "expr": "Integral(x**2 - 5*x + 21/4, (x, 0, 3/2)) + Integral(-x**2 + 5*x - 21/4, (x, 3/2, 7/2)) + Integral(x**2 - 5*x + 21/4, (x, 7/2, 4))",
     "relation": "new"
    },
    {
     "text": "\\(27/8+4/3+7/24\\).",
     "expr": "5",
     "relation": "equivalent"
    }
   ],
   "options": [
    {
     "id": "A",
     "is_key": false,
     "expr": "-5",
     "error_path": "BC-ERR-08020",
     "derivation": "lower minus upper on every piece"
    },
    {
     "id": "B",
     "is_key": false,
     "expr": "53/12",
     "error_path": "BC-ERR-08025",
     "derivation": "the crossing at 7/2 missed, two pieces"
    },
    {
     "id": "C",
     "is_key": false,
     "expr": "7/3",
     "error_path": "BC-ERR-08026",
     "derivation": "one integral of f minus g over [0, 4]"
    },
    {
     "id": "D",
     "is_key": true,
     "expr": "5",
     "error_path": null
    }
   ],
   "calculator_status": "no_calculator",
   "skills": [
    "BC-SKL-08029"
   ]
  }
 ],
 "delivery": [
  {
   "block": "orientation",
   "mode": "figure",
   "reason": "rule 4: BC-REP-02 on BC-SKL-08027 and BC-SKL-08028; unit README delivery map",
   "sources": [
    "BC-SKL-08027",
    "BC-SKL-08028"
   ],
   "spec": {
    "kind": "graph",
    "representations": [
     "BC-REP-02"
    ],
    "window": {
     "x": [
      -0.5,
      4
     ],
     "y": [
      0,
      6
     ]
    },
    "curves": [
     {
      "expr": "x**2 - 3*x + 4",
      "domain": [
       0,
       3.5
      ]
     },
     {
      "expr": "x + 1",
      "domain": [
       0,
       3.5
      ]
     }
    ],
    "shade": {
     "between": [
      "x**2 - 3*x + 4",
      "x + 1"
     ],
     "x": [
      0,
      3.5
     ]
    },
    "labels": [
     {
      "text": "f",
      "placement": "inside"
     },
     {
      "text": "g",
      "placement": "inside"
     },
     {
      "text": "three pieces",
      "placement": "inside"
     }
    ]
   },
   "fallback": "the same shaded region static with the curve labels",
   "keyboard": "no control; the figure description is reached with Tab"
  },
  {
   "block": "ki-1",
   "mode": "interactive",
   "reason": "rule 4 promoted: BC-REP-02 on BC-SKL-08027 and BC-SKL-08028; BC-QA-08010 difficulty_variables name the number of interior crossings, and the stem asks which curve is greater on each piece",
   "sources": [
    "BC-SKL-08027",
    "BC-SKL-08028",
    "BC-QA-08010"
   ],
   "spec": {
    "kind": "graph",
    "representations": [
     "BC-REP-02",
     "BC-REP-01"
    ],
    "window": {
     "x": [
      -0.5,
      4
     ],
     "y": [
      0,
      6
     ]
    },
    "curves": [
     {
      "expr": "x**2 - 3*x + 4",
      "domain": [
       0,
       3.5
      ]
     },
     {
      "expr": "x + 1",
      "domain": [
       0,
       3.5
      ]
     }
    ],
    "controls": [
     {
      "type": "draggable_rectangle",
      "name": "x",
      "domain": [
       0,
       3.5
      ],
      "step": 0.25,
      "start": 0.5,
      "readout": "f(x) - g(x) and which curve is on top"
     }
    ],
    "drawn": [
     "a vertical rectangle from the lower curve to the upper curve at the dragged input",
     "the crossings at x = 1 and x = 3 marked"
    ],
    "labels": [
     {
      "text": "x = 1: curves cross",
      "placement": "inside"
     },
     {
      "text": "x = 3: curves cross",
      "placement": "inside"
     },
     {
      "text": "top curve at this x",
      "placement": "inside"
     }
    ],
    "question": "On which pieces is f on top, and where does f(x) - g(x) change sign?"
   },
   "fallback": "three static frames side by side, the rectangle at x = 0.5, 2 and 3.25, each labelled with the top curve and the sign of f(x) - g(x)",
   "keyboard": "Tab focuses the rectangle; left and right arrow keys move it by 0.25; Home and End jump to 0 and 3.5; Enter reads out the top curve and f(x) - g(x)"
  },
  {
   "block": "ex-1",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  },
  {
   "block": "err-BC-ERR-08020",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  },
  {
   "block": "err-BC-ERR-08025",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  },
  {
   "block": "err-BC-ERR-08026",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  },
  {
   "block": "err-BC-ERR-08027",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  }
 ],
 "refresher": [
  "ki-1",
  "err-BC-ERR-08020",
  "err-BC-ERR-08025",
  "err-BC-ERR-08026",
  "err-BC-ERR-08027",
  "ex-1"
 ],
 "read_minutes": {
  "full": 3.7,
  "brief": 3.0
 },
 "word_count": {
  "full": 542,
  "brief": 447
 },
 "research_lines": [
  {
   "file": "research/units/unit-08-applications-integration.md",
   "line": "The interior intersection points are the split inputs"
  }
 ],
 "inferred": [
  {
   "claim": "BC-QA-08010 is an either archetype; the lesson takes Section I Part A and its 2.14 minute budget.",
   "settles": "A ruling on which exam part an either archetype's budget comes from."
  },
  {
   "claim": "The free response part is worth two points, taken from the 2023 area pattern.",
   "settles": "A scoring guideline for a split region part."
  },
  {
   "claim": "ki-1 is an interactive draggable rectangle and the orientation a static figure; the sign test is held in the head.",
   "settles": "The modality A/B in the build plan, and timing data per step from 10's fluency telemetry."
  }
 ],
 "sources": [
  "BC-CON-08013",
  "BC-SKL-08027",
  "BC-SKL-08028",
  "BC-SKL-08029",
  "BC-SKL-08030",
  "BC-EK-CHA-5A3",
  "ced:157",
  "BC-QA-08010",
  "sg-23:16",
  "BC-ERR-08020",
  "BC-ERR-08025",
  "BC-ERR-08026",
  "BC-ERR-08027",
  "BC-MIS-08011",
  "BC-MIS-08014",
  "BC-PRQ-06005",
  "BC-PRQ-08001",
  "BC-PRQ-08003",
  "research/units/unit-08-applications-integration.md#8.6 Finding the Area Between Curves That Intersect at More Than Two Points",
  "research/units/unit-08-applications-integration.md#Unresolved",
  "research/question-analysis/question-archetypes.md#BC-QA-08010 Area of a region whose boundary curves cross",
  "research/exam/exam-structure.md#Section and part layout"
 ]
}
```
