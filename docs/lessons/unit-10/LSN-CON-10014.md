---
title: LSN-CON-10014 Conditional convergence as a separate classification
research_date: 2026-09-29
status: designed
purpose: Authoring spec for the concept lesson on BC-CON-10014, conditional convergence as a signed series that converges while its series of absolute values diverges, classified apart from absolute convergence, built from authoring_bundle and the research files it cites.
---

# LSN-CON-10014 Conditional convergence as a separate classification

Concept BC-CON-10014 (skill BC-SKL-10036), topic 10.9 of Unit 10, BC only (ced:194), loaded by BC-QA-10007 and BC-QA-10015. Hard parents in the unit are BC-CON-10011 and BC-CON-10013 (docs/lessons/unit-10/README.md, section 1).

## Prediction

Served first, both bands: an mcq on ex-1's own numbers. The signed series alternates with sizes decreasing to 0 and its series of absolute values diverges, and the question is what is true of the signed series. Key B, it converges but not absolutely. Option A, that it diverges because the sizes add to infinity, is false, and C contradicts the stem, so B is the only true option. Answerable before the rule by asking whether alternating terms of shrinking size can cancel. The resolution carries no verdict word.

## Orientation

From the concept's description_plain and the topic's Assessment behaviour paragraph (research/units/unit-10-infinite-sequences-series.md#10.9 Determining Absolute or Conditional Convergence): justification variants require both halves of a conditional convergence claim, and MCQ forms ask which of three classifications applies (sg-21:23). The orientation states what a response shows: both findings and the label. No count, no frequency.

## Key ideas

One essential knowledge statement, BC-EK-LIM-7A12 (ced:194), from the Required mathematical knowledge paragraphs Three outcomes and Conditional convergence: one core block, both bands. The alternating harmonic series is the topic paragraph's standard instance. No anchor quote. Notation: the concept's notation.

## Recognition

BC-QA-10007 loads BC-SKL-10036 with the alternating factor as given and a label as the ask (wording: determine whether the series converges absolutely, converges conditionally, or diverges). BC-QA-10015 loads it with a power series and an endpoint value as givens and a verdict with a named test as the ask; the skill's diagnostic_archetypes name it as the usual setting of a conditionally convergent endpoint series. Official examples: BC-MCQ-SAMPLE-022, BC-MCQ-CED-019. What says conditional: the signed terms shrink to 0 with alternating sign, and the absolute value series is a p-series with p at most 1. The near miss of the contrast pair is a geometric series with a sign factor asked for its sum (BC-QA-10003), which shares the (-1)^n and asks for a value.

## Method choice

st-1 on BC-QA-10007: method is the first two expected_solution_path entries, then the label; rival is the wrong_approaches entry, a label from the signed series alone (BC-ERR-10023); separating feature is the pair of findings. st-2 on BC-QA-10015: substitute the endpoint, then two tests. Both archetypes carry asked_to_produce and common_givens. The first block carries the contrast pair.

## Solution path

ex-1, BC-QA-10007, both bands: draw form power, power 2/3, coefficient 3, offset 5, start 1, sign_start n. No published item on BC-QA-10007 has form power with power 2/3 (content/items_gen_unit10). The limits 0 and 3 are computed by SymPy. ex-2, BC-QA-10015, low band, faded from step 4: draw form power, power 1/2, sign positive, end left, given value, centre 4, radius 3, shift 2; the left endpoint x = 1 gives the alternating series with sizes 1/sqrt(n). Steps 1 to 3 are shown, the student writes the absolute value finding and the label, and steps 4 and 5 then reveal. The fade falls there because the substitution and the alternating test repeat ex-1, and the second series is the new work. A fluent solver writes the two limits and the label.

## Scoring

Neither BC-QA-10007 nor BC-QA-10015 lists point_types, so the lesson says nothing about points (plan 15, R14, docs/lessons/unit-10/README.md, Library gaps).

## Traps

One error meets the skill, BC-ERR-10023 (high severity BC-MIS-10015 and BC-MIS-10016). It is distinct on ex-1's draw, so fix_prompt true, with symbols for the two labels. Possible reason from BC-MIS-10016.

## Representations

None. The topic names BC-REP-11, 01 and 04; nothing figure-shaped.

## Prerequisite bridge

BC-PRQ-06005, from its description_plain and failure_signature.

## Time

Both archetypes are no calculator. The MCQ form is Section I Part A, 2.14 minutes (research/exam/exam-structure.md#Section and part layout). As a free response part the shape is 2 points, 3.33 minutes (docs/lessons/unit-10/README.md, section 5). A fluent solver writes the two limits and the label.

## Checks

chk-1 completes ex-1. chk-2 is an isomorph on BC-QA-10007: form power, power 1, coefficient 6, offset 2, start 1, sign_start n+1, key converges conditionally. chk-3, low band, is a 4 option MCQ on BC-QA-10015: form power, power 1, sign alternating, end right, given value, centre 1, radius 2, shift 3; at x = 3 the series is the alternating harmonic series. The lesson's only held error is BC-ERR-10023, so all three distractors carry it, each a different way of exchanging the labels.

## Delivery

All blocks are text or step_reveal. Rule 6 for the prediction, orientation and key idea; rule 1 for the two examples and the error block. The record carries no_figure_reason.

## Band plan

Low (full): prediction, orientation, bridge, ki-1, st-1 with the contrast pair, st-2, ex-1, chk-1, err-BC-ERR-10023, ex-2 (faded from step 4), chk-2, chk-3. 600 words, 4.0 minutes. Mid (brief): prediction, orientation, bridge, ki-1, st-1 with the contrast pair, ex-1, chk-1, err-BC-ERR-10023, chk-2. 399 words, 2.7 minutes. Refresher: ki-1, err-BC-ERR-10023, ex-1.

## Sources

- BC-CON-10014; BC-SKL-10036; BC-EK-LIM-7A12; ced:194
- BC-QA-10007, BC-QA-10015; BC-ERR-10023; BC-MIS-10016; BC-PRQ-06005
- sg-24:19
- research/units/unit-10-infinite-sequences-series.md#10.9 Determining Absolute or Conditional Convergence
- research/exam/exam-structure.md#Section and part layout
- [inferred] the missing point types, the added label request on ex-2, the held steps; each settled as the inferred array states.

## Machine record

```json
{
 "id": "LSN-CON-10014",
 "kind": "concept",
 "target_id": "BC-CON-10014",
 "unit": "10",
 "skills": [
  "BC-SKL-10036"
 ],
 "prediction": {
  "id": "pr-1",
  "stem": {
   "text": "Predict. The terms of \\(\\sum_{n=1}^{\\infty}\\frac{3(-1)^{n}}{(n+5)^{2/3}}\\) alternate and their sizes decrease to 0, while \\(\\sum_{n=1}^{\\infty}\\frac{3}{(n+5)^{2/3}}\\) diverges. What is true of the signed series?",
   "command_verb": "predict"
  },
  "format": "mcq",
  "options": [
   {
    "id": "A",
    "label": "It diverges, because the sizes add to infinity",
    "is_key": false
   },
   {
    "id": "B",
    "label": "It converges, but not absolutely",
    "is_key": true
   },
   {
    "id": "C",
    "label": "It converges absolutely",
    "is_key": false
   }
  ],
  "resolution": "Alternating signs let successive terms cancel, so the signed partial sums can settle even when the sizes add to infinity. Such a series converges without converging absolutely.",
  "sources": [
   "BC-CON-10014",
   "research/units/unit-10-infinite-sequences-series.md#10.9 Determining Absolute or Conditional Convergence"
  ]
 },
 "orientation": {
  "text": "A series that converges while its series of absolute values diverges is conditionally convergent. A response reports both findings, that the signed series converges and that the series of absolute values diverges, and gives the label with both as the reason.",
  "sources": [
   "BC-CON-10014",
   "research/units/unit-10-infinite-sequences-series.md#10.9 Determining Absolute or Conditional Convergence"
  ]
 },
 "key_ideas": [
  {
   "id": "ki-1",
   "ek_id": "BC-EK-LIM-7A12",
   "depth": "core",
   "text": "A series that converges while \\(\\sum|a_n|\\) diverges is conditionally convergent. The three outcomes are exclusive, so a series that converges absolutely is never called conditional. The alternating harmonic series is the standard instance: it converges while the harmonic series diverges.",
   "notation": "conditionally convergent; absolutely convergent",
   "quote": null,
   "sources": [
    "BC-EK-LIM-7A12",
    "ced:194",
    "research/units/unit-10-infinite-sequences-series.md#10.9 Determining Absolute or Conditional Convergence"
   ]
  }
 ],
 "strategy": [
  {
   "id": "st-1",
   "archetype_id": "BC-QA-10007",
   "cue": "A signed series whose terms shrink to 0, asked to classify.",
   "method": "Test \\(\\sum a_n\\), test \\(\\sum|a_n|\\), then write conditionally convergent with both findings as the reason.",
   "rival": "Calling the series absolutely convergent from the signed test alone.",
   "separating_feature": "Conditional needs the signed series to converge and the series of absolute values to diverge.",
   "sources": [
    "BC-QA-10007"
   ],
   "evidence_tag": "verified",
   "contrast": {
    "this": {
     "text": "Classify \\(\\sum_{n=1}^{\\infty}\\frac{(-1)^{n}}{\\sqrt{n+3}}\\) as absolutely convergent, conditionally convergent, or divergent.",
     "archetype_id": "BC-QA-10007"
    },
    "not_this": {
     "text": "Find the sum of \\(\\sum_{n=0}^{\\infty}\\frac{(-1)^{n}}{2^{n}}\\).",
     "why_not": "It asks for a value, and the series is geometric with ratio \\(-\\frac12\\)."
    },
    "feature": "Classify asks for a label from two tests, not for a sum."
   }
  },
  {
   "id": "st-2",
   "archetype_id": "BC-QA-10015",
   "cue": "An endpoint of a power series, with the kind of convergence asked.",
   "method": "Substitute the endpoint, then test the endpoint series and its series of absolute values.",
   "rival": "Applying a comparison test to the alternating endpoint series.",
   "separating_feature": "An endpoint that produces a sign factor needs two tests when the label is asked.",
   "sources": [
    "BC-QA-10015"
   ],
   "evidence_tag": "verified"
  }
 ],
 "worked_examples": [
  {
   "id": "ex-1",
   "archetype_id": "BC-QA-10007",
   "bands": [
    "low",
    "mid"
   ],
   "parameter_draw": {
    "form": "power",
    "power": "2/3",
    "coefficient": 3,
    "offset": 5,
    "start": 1,
    "sign_start": "n"
   },
   "problem": {
    "text": "Classify \\(\\sum_{n=1}^{\\infty}\\frac{3(-1)^{n}}{(n+5)^{2/3}}\\) as absolutely convergent, conditionally convergent, or divergent.",
    "command_verb": "classify"
   },
   "calculator_status": "no_calculator",
   "steps": [
    {
     "cue": "The signed series alternates: check the sizes.",
     "why": "The alternating series test needs sizes decreasing to 0.",
     "expr": "3/(n+5)**(2/3)",
     "relation": "new"
    },
    {
     "cue": "Take the limit of the sizes.",
     "why": "They decrease to 0, so \\(\\sum a_n\\) converges.",
     "expr": "0",
     "relation": "limit",
     "variable": "n",
     "point": "oo"
    },
    {
     "cue": "Series of absolute values: compare with \\(\\sum\\frac{1}{n^{2/3}}\\).",
     "why": "Limit comparison with a p-series.",
     "expr": "(3/(n+5)**(2/3))/(1/n**(2/3))",
     "relation": "new"
    },
    {
     "cue": "Take the limit.",
     "why": "Positive and finite.",
     "expr": "3",
     "relation": "limit",
     "variable": "n",
     "point": "oo"
    },
    {
     "cue": "The partner has \\(p=\\frac23\\le1\\).",
     "why": "\\(\\sum|a_n|\\) diverges.",
     "expr": "2/3",
     "relation": "new"
    },
    {
     "cue": "Combine the two findings.",
     "why": "Converges while the absolute value series diverges: conditionally convergent."
    }
   ],
   "answer": {
    "form": "statement",
    "expr": "2/3",
    "text": "The series converges conditionally: it converges by the alternating series test and its series of absolute values diverges, p = 2/3."
   }
  },
  {
   "id": "ex-2",
   "archetype_id": "BC-QA-10015",
   "bands": [
    "low"
   ],
   "fade_from": 4,
   "parameter_draw": {
    "form": "power",
    "power": "1/2",
    "sign": "positive",
    "end": "left",
    "given": "value",
    "centre": 4,
    "radius": 3,
    "shift": 2
   },
   "problem": {
    "text": "The power series \\(\\sum_{n=1}^{\\infty}\\frac{(x-4)^{n}}{3^{n}\\sqrt{n}}\\) has radius of convergence 3. Determine whether it converges or diverges at \\(x=1\\), naming the test, and state whether the convergence is absolute or conditional.",
    "command_verb": "determine"
   },
   "calculator_status": "no_calculator",
   "steps": [
    {
     "cue": "Substitute the endpoint x = 1.",
     "why": "The endpoint turns the power series into a numerical series.",
     "expr": "(-3)**n/(3**n*sqrt(n))",
     "relation": "new"
    },
    {
     "cue": "Read the sizes.",
     "why": "The series alternates, and the sizes are these.",
     "expr": "1/sqrt(n)",
     "relation": "new"
    },
    {
     "cue": "Take the limit of the sizes.",
     "why": "Decreasing to 0: the alternating series test gives convergence.",
     "expr": "0",
     "relation": "limit",
     "variable": "n",
     "point": "oo"
    },
    {
     "cue": "Series of absolute values: \\(p=\\frac12\\).",
     "why": "A p-series with p at most 1 diverges.",
     "expr": "1/2",
     "relation": "new"
    },
    {
     "cue": "Combine the two findings.",
     "why": "Converges while the absolute value series diverges: conditionally convergent."
    }
   ],
   "answer": {
    "form": "statement",
    "expr": "1/2",
    "text": "The series converges at x = 1 by the alternating series test, conditionally, since its series of absolute values is a p-series with p = 1/2."
   }
  }
 ],
 "what_a_reader_scores": [],
 "common_errors": [
  {
   "error_id": "BC-ERR-10023",
   "observed_behavior": "The response labels a series conditionally convergent when the absolute value series converges, or absolutely convergent when only the signed series converges.",
   "scoring_consequence": "The classification point is lost, since the two labels are exclusive.",
   "wrong_step": {
    "text": "Labelled absolutely convergent.",
    "expr": "absolute"
   },
   "right_step": {
    "text": "Labelled conditionally convergent.",
    "expr": "conditional"
   },
   "relation": "distinct",
   "possible_reason": {
    "misconception_id": "BC-MIS-10016",
    "text": "orders the two classifications on a single scale"
   },
   "sources": [
    "BC-ERR-10023",
    "BC-MIS-10016"
   ],
   "fix_prompt": true
  }
 ],
 "representations": null,
 "prerequisite_bridges": [
  {
   "prq_id": "BC-PRQ-06005",
   "text": "\\(a_n\\) is the term at index n, and \\(|a_n|\\) is its size."
  }
 ],
 "time": {
  "exam_part": "I-A",
  "budget_minutes": 2.14,
  "source": "research/exam/exam-structure.md#Section and part layout",
  "written_steps": {
   "ex-1": [
    2,
    4,
    6
   ]
  },
  "skipped_steps": {
   "ex-1": [
    1,
    3,
    5
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
   "archetype_id": "BC-QA-10007",
   "parameter_draw": {
    "form": "power",
    "power": "2/3",
    "coefficient": 3,
    "offset": 5,
    "start": 1,
    "sign_start": "n"
   },
   "completes": "ex-1",
   "stem": {
    "text": "\\(\\sum\\frac{3(-1)^{n}}{(n+5)^{2/3}}\\) converges by the alternating series test and \\(\\sum\\frac{3}{(n+5)^{2/3}}\\) diverges. Classify the series, naming it.",
    "command_verb": "classify"
   },
   "key": {
    "form": "statement",
    "expr": "2/3",
    "text": "It converges conditionally."
   },
   "steps": [
    {
     "text": "The absolute value series is a p-series with p = 2/3.",
     "expr": "2/3",
     "relation": "new"
    }
   ],
   "calculator_status": "no_calculator",
   "skills": [
    "BC-SKL-10036"
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
   "archetype_id": "BC-QA-10007",
   "parameter_draw": {
    "form": "power",
    "power": "1",
    "coefficient": 6,
    "offset": 2,
    "start": 1,
    "sign_start": "n+1"
   },
   "stem": {
    "text": "Classify \\(\\sum_{n=1}^{\\infty}\\frac{6(-1)^{n+1}}{n+2}\\) as absolutely convergent, conditionally convergent, or divergent.",
    "command_verb": "classify"
   },
   "key": {
    "form": "statement",
    "expr": "1",
    "text": "It converges conditionally."
   },
   "steps": [
    {
     "text": "Sizes.",
     "expr": "6/(n+2)",
     "relation": "new"
    },
    {
     "text": "Sizes tend to 0.",
     "expr": "0",
     "relation": "limit",
     "variable": "n",
     "point": "oo"
    },
    {
     "text": "Quotient with 1/n.",
     "expr": "(6/(n+2))/(1/n)",
     "relation": "new"
    },
    {
     "text": "Limit 6, positive and finite.",
     "expr": "6",
     "relation": "limit",
     "variable": "n",
     "point": "oo"
    },
    {
     "text": "p = 1, so the series of absolute values diverges.",
     "expr": "1",
     "relation": "new"
    }
   ],
   "calculator_status": "no_calculator",
   "skills": [
    "BC-SKL-10036"
   ]
  },
  {
   "id": "chk-3",
   "check_kind": "mcq",
   "format": "mcq",
   "bands": [
    "low"
   ],
   "archetype_id": "BC-QA-10015",
   "parameter_draw": {
    "form": "power",
    "power": "1",
    "sign": "alternating",
    "end": "right",
    "given": "value",
    "centre": 1,
    "radius": 2,
    "shift": 3
   },
   "stem": {
    "text": "The power series \\(\\sum_{n=1}^{\\infty}\\frac{(-1)^{n}(x-1)^{n}}{2^{n}n}\\) has radius of convergence 2. At \\(x=3\\) the series is",
    "command_verb": "identify"
   },
   "key": {
    "form": "statement",
    "expr": "1",
    "text": "Conditionally convergent: it converges by the alternating series test and \\(\\sum\\frac1n\\) diverges."
   },
   "steps": [
    {
     "text": "Endpoint series.",
     "expr": "(-1)**n*2**n/(2**n*n)",
     "relation": "new"
    },
    {
     "text": "Sizes.",
     "expr": "1/n",
     "relation": "new"
    },
    {
     "text": "Sizes tend to 0.",
     "expr": "0",
     "relation": "limit",
     "variable": "n",
     "point": "oo"
    },
    {
     "text": "p = 1 for the absolute values.",
     "expr": "1",
     "relation": "new"
    }
   ],
   "options": [
    {
     "id": "A",
     "is_key": false,
     "label": "Absolutely convergent, because the alternating series test shows it converges.",
     "error_path": "BC-ERR-10023",
     "derivation": "the label taken from the signed test alone, so conditional is read as absolute"
    },
    {
     "id": "B",
     "is_key": true,
     "label": "Conditionally convergent: it converges by the alternating series test and \\(\\sum\\frac1n\\) diverges.",
     "error_path": null
    },
    {
     "id": "C",
     "is_key": false,
     "label": "Conditionally convergent, because the series of absolute values converges.",
     "error_path": "BC-ERR-10023",
     "derivation": "the reason is the absolute case and the label is conditional"
    },
    {
     "id": "D",
     "is_key": false,
     "label": "Absolutely convergent, because the series of absolute values diverges.",
     "error_path": "BC-ERR-10023",
     "derivation": "the finding is the conditional case and the label is absolute"
    }
   ],
   "calculator_status": "no_calculator",
   "skills": [
    "BC-SKL-10036"
   ]
  }
 ],
 "no_figure_reason": "The skill carries series and verbal representations only, none figure-bearing, and no key idea describes a process, since conditional convergence is a pair of test results.",
 "delivery": [
  {
   "block": "pr-1",
   "mode": "text",
   "reason": "rule 6: a question on a series pair, no figure-bearing representation",
   "sources": [
    "BC-CON-10014"
   ]
  },
  {
   "block": "orientation",
   "mode": "text",
   "reason": "rule 6: a statement of what a response shows",
   "sources": [
    "BC-CON-10014"
   ]
  },
  {
   "block": "ki-1",
   "mode": "text",
   "reason": "rule 6: BC-REP-04, 11 on BC-SKL-10036, none figure-bearing",
   "sources": [
    "BC-SKL-10036"
   ]
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
   "block": "err-BC-ERR-10023",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  }
 ],
 "refresher": [
  "ki-1",
  "err-BC-ERR-10023",
  "ex-1"
 ],
 "research_lines": [
  {
   "file": "research/units/unit-10-infinite-sequences-series.md",
   "line": "the alternating harmonic series is the standard instance"
  }
 ],
 "inferred": [
  {
   "claim": "Neither BC-QA-10007 nor BC-QA-10015 lists point_types, so the lesson carries no scoring line; the two-finding requirement is taught from the skill's mastered_if text and the topic's justification variants.",
   "settles": "Point types on BC-QA-10007 and BC-QA-10015."
  },
  {
   "claim": "ex-2 adds a request to state absolute or conditional to BC-QA-10015's endpoint stem, since the archetype's own stem asks only converges or diverges; the skill's diagnostic_archetypes name BC-QA-10015 as the usual setting of a conditionally convergent endpoint.",
   "settles": "An endpoint task value in BC-QA-10015's parameter_spec that asks for the label."
  },
  {
   "claim": "A fluent solver writes the two limits and the label, and holds the substitution and the partner.",
   "settles": "Timing data per step once the fluency telemetry exists."
  }
 ],
 "sources": [
  "BC-CON-10014",
  "BC-SKL-10036",
  "BC-EK-LIM-7A12",
  "ced:194",
  "BC-QA-10007",
  "BC-QA-10015",
  "BC-ERR-10023",
  "BC-MIS-10016",
  "BC-PRQ-06005",
  "sg-24:19",
  "research/units/unit-10-infinite-sequences-series.md#10.9 Determining Absolute or Conditional Convergence",
  "research/exam/exam-structure.md#Section and part layout"
 ],
 "word_count": {
  "full": 600,
  "brief": 399
 },
 "read_minutes": {
  "full": 4.0,
  "brief": 2.7
 }
}
```
