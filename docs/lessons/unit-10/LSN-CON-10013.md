---
title: LSN-CON-10013 Absolute convergence and its consequences
research_date: 2026-09-29
status: designed
purpose: Authoring spec for the concept lesson on BC-CON-10013, absolute convergence as convergence of the series of absolute values, its implication for convergence and its rearrangement property, built from authoring_bundle and the research files it cites.
---

# LSN-CON-10013 Absolute convergence and its consequences

Concept BC-CON-10013 (skills BC-SKL-10034, 10035, 10037, 10038), topic 10.9 of Unit 10, BC only (ced:194), loaded by BC-QA-10007 and BC-QA-10006. Hard parents in the unit are BC-CON-10008 and BC-CON-10011 (docs/lessons/unit-10/README.md, section 1).

## Prediction

Served first, both bands: an mcq on ex-1's own numbers. The series of absolute values of ex-1 converges, and the question is what follows for the signed series. Key B, it converges. The distractors, that it may diverge because the signs alternate and that it converges to the same value, are both false, so B is the only true option. It is answerable before the rule by asking whether sizes with a finite total can push the signed partial sums out of bounds. The resolution states the general implication with no verdict word.

## Orientation

From the concept's description_plain and the topic's Assessment behaviour paragraph (research/units/unit-10-infinite-sequences-series.md#10.9 Determining Absolute or Conditional Convergence): MCQ forms ask which of three classifications applies, and free-response forms direct a comparison at the series of absolute values and require a conclusion about a specific series, with the bars explicit or implicit (sg-21:23). No count, no frequency.

## Key ideas

Three essential knowledge statements, from the Required mathematical knowledge paragraphs. ki-1 (BC-EK-LIM-7A12) and ki-2 (BC-EK-LIM-7A13) are core and serve both bands. ki-3 (BC-EK-LIM-7A14) is extended, low band. No anchor quote: each CED sentence is a line the paraphrase already carries. Notation: the concept's notation, series of absolute values.

## Recognition

BC-QA-10007 (classification) and BC-QA-10006 (limit comparison used to classify) load the four skills. In 10007 the givens are a series with an alternating factor and the ask is one of three labels with the series named; wording: determine whether the series converges absolutely, converges conditionally, or diverges. In 10006 the givens are a named comparison series and the ask is a limit with limit notation, positive and finite, and a conclusion naming the series; wording: use the limit comparison test to show that the series converges absolutely. The word absolutely says the series of absolute values. Official examples: BC-MCQ-SAMPLE-022, BC-MCQ-CED-019, BC-FRQ-2021-Q6-B. The near miss of the contrast pair is a request to show a signed series converges (BC-QA-10004 in shape, the alternating series test), the rival named in BC-QA-10007 wrong_approaches being a test run on the signed terms.

## Method choice

st-1 on BC-QA-10007: method is expected_solution_path[0], test the series of absolute values, then the classification with the series named; rival is the wrong_approaches entry, testing signed terms while claiming absolute convergence (BC-ERR-10018); separating feature is the word absolutely. st-2 on BC-QA-10006: the quotient with absolute values. Both archetypes carry asked_to_produce and common_givens, so neither is inferred. No served field opens with the reader's own label. The first block carries the contrast pair.

## Solution path

ex-1, BC-QA-10007, both bands: draw form power, power 3/2, coefficient 5, offset 2, start 1, sign_start n. No published item on BC-QA-10007 carries this draw (content/items_gen_unit10 lists power 3/2 only with coefficient 9, offset 3). The steps are the series of absolute values, the quotient with 1/n^(3/2), its limit 5 (SymPy), and the p value. ex-2, BC-QA-10006, low band, faded from step 4: draw claim absolute, partner given, gap 2, top_degree 1, lead_top 3, constant_top 5, lead_bottom 7, constant_bottom 2, start 1; the limit is 3/7 (SymPy). Steps 1 to 3 are shown, the student writes the limit and conclusion, and steps 4 and 5 then reveal. The fade falls there because the setup repeats ex-1 and the limit and the named conclusion are what must be produced. A fluent solver writes the absolute value series, the limit and the conclusion, and holds the choice of partner.

## Scoring

BC-QA-10007 lists no point types, so ex-1 carries no scoring line. BC-QA-10006 lists BC-PT-99042 and BC-PT-99005; ex-2 tags BC-PT-99042 on the quotient, and the line is the reader_checks output. The answer point BC-PT-99005 is taught and left untagged for the word cap (inferred array). Point losses from research: the explanation point requires absolute value symbols, explicit or implicit, and a conclusion that says which series it concerns (sg-21:23; research/scoring/justification-requirements.md#Justification inside series work).

## Traps

Three errors meet the skills, in bundle order: BC-ERR-10003, BC-ERR-10018, BC-ERR-10023 (each linked to a high severity BC-MIS, then by id). Low band all three, mid band the first two. All on ex-1's draw. BC-ERR-10003 is a sentence difference, so relation equivalent and fix_prompt false; the other two are distinct and fix_prompt true. BC-ERR-10023 uses symbols for the two labels. No possible reason line, for the brief band words.

## Representations

None. The topic names BC-REP-11, 01 and 04 and the conversions signed series to absolute value series and a pair of results to a label; nothing figure-shaped (docs/lessons/unit-10/README.md, section 6).

## Prerequisite bridge

BC-PRQ-06005 and BC-PRQ-10008, each from its description_plain and failure_signature.

## Time

Both archetypes are no calculator. The MCQ form is Section I Part A, 2.14 minutes (research/exam/exam-structure.md#Section and part layout). As free response parts the shape is 2 points, 3.33 minutes (docs/lessons/unit-10/README.md, section 5). A fluent solver writes the absolute value series, the limit and the conclusion; the partner is held.

## Checks

chk-1 completes ex-1 (both bands). chk-2 is an isomorph on BC-QA-10007: form power, power 2, coefficient 4, offset 3, start 2, sign_start n+1, key converges absolutely. chk-3, low band, is a 4 option MCQ on BC-QA-10006: claim absolute, partner given, gap 2, top_degree 1, lead_top 4, constant_top 1, lead_bottom 3, constant_bottom 2, start 1, limit 4/3. Distractors: conditionally convergent (BC-ERR-10023), the alternating series test called absolute (BC-ERR-10018), no series named (BC-ERR-10003).

## Delivery

All blocks are text or step_reveal. Rule 6 for the prediction, orientation and key ideas: no skill carries a figure-bearing representation. Rule 1 for the two examples and three error blocks. The record carries no_figure_reason.

## Band plan

Low (full): prediction, orientation, bridges, ki-1 to ki-3, st-1 with the contrast pair, st-2, ex-1, chk-1, the three error blocks, ex-2 (faded from step 4) and its line, chk-2, chk-3. 729 words, 4.9 minutes. Mid (brief): prediction, orientation, bridges, ki-1, ki-2, st-1 with the contrast pair, ex-1, chk-1, err-BC-ERR-10003, err-BC-ERR-10018, chk-2. 429 words, 2.9 minutes. Refresher: ki-1, ki-2, the three error blocks, ex-1.

## Sources

- BC-CON-10013; BC-SKL-10034, 10035, 10037, 10038; BC-EK-LIM-7A12, 7A13, 7A14; ced:194
- BC-QA-10007, BC-QA-10006; BC-PT-99042
- BC-ERR-10003, 10018, 10023; BC-PRQ-06005, 10008
- sg-21:23
- research/units/unit-10-infinite-sequences-series.md#10.9 Determining Absolute or Conditional Convergence
- research/exam/exam-structure.md#Section and part layout
- [inferred] the tag on BC-PT-99042, the missing points on BC-QA-10007, the held steps, the untagged answer point; each settled as the inferred array states.

## Machine record

```json
{
 "id": "LSN-CON-10013",
 "kind": "concept",
 "target_id": "BC-CON-10013",
 "unit": "10",
 "skills": [
  "BC-SKL-10034",
  "BC-SKL-10035",
  "BC-SKL-10037",
  "BC-SKL-10038"
 ],
 "prediction": {
  "id": "pr-1",
  "stem": {
   "text": "\\(\\sum_{n=1}^{\\infty}\\frac{5}{(n+2)^{3/2}}\\) converges. What follows for \\(\\sum_{n=1}^{\\infty}\\frac{5(-1)^{n}}{(n+2)^{3/2}}\\)?",
   "command_verb": "predict"
  },
  "format": "mcq",
  "options": [
   {
    "id": "A",
    "label": "It may diverge, since the signs alternate",
    "is_key": false
   },
   {
    "id": "B",
    "label": "It converges",
    "is_key": true
   },
   {
    "id": "C",
    "label": "It converges to the same value",
    "is_key": false
   }
  ],
  "resolution": "Terms whose sizes add to a finite total cannot drive the signed partial sums to infinity, so the signed series converges, generally to a different value. Convergence of \\(\\sum|a_n|\\) gives convergence of \\(\\sum a_n\\).",
  "sources": [
   "BC-CON-10013",
   "research/units/unit-10-infinite-sequences-series.md#10.9 Determining Absolute or Conditional Convergence"
  ]
 },
 "orientation": {
  "text": "A signed series is classified by testing the series of absolute values first. A response shows that series, a named test on it, and a conclusion naming which series it concerns, with absolute value bars visible. Absolute convergence then gives convergence and leaves the value unchanged under rearrangement.",
  "sources": [
   "BC-CON-10013",
   "research/units/unit-10-infinite-sequences-series.md#10.9 Determining Absolute or Conditional Convergence"
  ]
 },
 "key_ideas": [
  {
   "id": "ki-1",
   "ek_id": "BC-EK-LIM-7A12",
   "depth": "core",
   "text": "A series is absolutely convergent, conditionally convergent, or divergent, and the three are exclusive. It is absolutely convergent when the series of absolute values \\(\\sum|a_n|\\) converges.",
   "notation": "series of absolute values",
   "quote": null,
   "sources": [
    "BC-EK-LIM-7A12",
    "ced:194",
    "research/units/unit-10-infinite-sequences-series.md#10.9 Determining Absolute or Conditional Convergence"
   ]
  },
  {
   "id": "ki-2",
   "ek_id": "BC-EK-LIM-7A13",
   "depth": "core",
   "text": "If \\(\\sum|a_n|\\) converges, then \\(\\sum a_n\\) converges. The hypothesis concerns the series of absolute values, so that series is tested, and the conclusion names the signed series it is about.",
   "notation": "",
   "quote": null,
   "sources": [
    "BC-EK-LIM-7A13",
    "ced:194",
    "sg-21:23",
    "research/units/unit-10-infinite-sequences-series.md#10.9 Determining Absolute or Conditional Convergence"
   ]
  },
  {
   "id": "ki-3",
   "ek_id": "BC-EK-LIM-7A14",
   "depth": "extended",
   "text": "If a series converges absolutely, any regrouping or rearranging of its terms has the same value. The series of absolute values must be tested first, since the statement is not made for a series shown only to converge.",
   "notation": "",
   "quote": null,
   "sources": [
    "BC-EK-LIM-7A14",
    "ced:194",
    "research/units/unit-10-infinite-sequences-series.md#10.9 Determining Absolute or Conditional Convergence"
   ]
  }
 ],
 "strategy": [
  {
   "id": "st-1",
   "archetype_id": "BC-QA-10007",
   "cue": "A signed series and a request to classify it.",
   "method": "Write \\(\\sum|a_n|\\), test it by name, then state the classification and the series it names.",
   "rival": "Testing the signed terms and calling the result absolute convergence.",
   "separating_feature": "Absolutely refers to the series of absolute values, never the signed terms.",
   "sources": [
    "BC-QA-10007"
   ],
   "evidence_tag": "verified",
   "contrast": {
    "this": {
     "text": "Classify \\(\\sum_{n=1}^{\\infty}\\frac{(-1)^{n}}{(n+4)^{2}}\\) as absolutely convergent, conditionally convergent, or divergent.",
     "archetype_id": "BC-QA-10007"
    },
    "not_this": {
     "text": "Show that \\(\\sum_{n=1}^{\\infty}\\frac{(-1)^{n}}{n+4}\\) converges.",
     "why_not": "It asks only about the signed series, which the alternating series test settles."
    },
    "feature": "Classify also asks for the series of absolute values."
   }
  },
  {
   "id": "st-2",
   "archetype_id": "BC-QA-10006",
   "cue": "A named comparison series and the word absolutely.",
   "method": "Form \\(|a_n|/b_n\\), take its limit with limit notation, state positive and finite, then name the series concluded about.",
   "rival": "Running the quotient on the signed terms.",
   "separating_feature": "A claim of absolute convergence puts the bars in the quotient.",
   "sources": [
    "BC-QA-10006"
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
    "power": "3/2",
    "coefficient": 5,
    "offset": 2,
    "start": 1,
    "sign_start": "n"
   },
   "problem": {
    "text": "Classify \\(\\sum_{n=1}^{\\infty}\\frac{5(-1)^{n}}{(n+2)^{3/2}}\\) as absolutely convergent, conditionally convergent, or divergent.",
    "command_verb": "classify"
   },
   "calculator_status": "no_calculator",
   "steps": [
    {
     "cue": "Asked to classify: test the absolute values.",
     "why": "Absolute convergence is decided on the series of absolute values.",
     "expr": "5/(n+2)**(3/2)",
     "relation": "new"
    },
    {
     "cue": "Compare with \\(\\sum\\frac{1}{n^{3/2}}\\).",
     "why": "Limit comparison needs a positive finite limit.",
     "expr": "(5/(n+2)**(3/2))/(1/n**(3/2))",
     "relation": "new"
    },
    {
     "cue": "Take the limit.",
     "why": "Positive and finite: the two series behave alike.",
     "expr": "5",
     "relation": "limit",
     "variable": "n",
     "point": "oo"
    },
    {
     "cue": "The partner has \\(p=\\frac32>1\\).",
     "why": "\\(\\sum|a_n|\\) converges, so \\(\\sum a_n\\) converges absolutely.",
     "expr": "3/2",
     "relation": "new"
    }
   ],
   "answer": {
    "form": "statement",
    "expr": "3/2",
    "text": "The series converges absolutely, since the series of absolute values converges by limit comparison with a p-series, p = 3/2."
   }
  },
  {
   "id": "ex-2",
   "archetype_id": "BC-QA-10006",
   "bands": [
    "low"
   ],
   "fade_from": 4,
   "parameter_draw": {
    "claim": "absolute",
    "partner": "given",
    "gap": 2,
    "top_degree": 1,
    "lead_top": 3,
    "constant_top": 5,
    "lead_bottom": 7,
    "constant_bottom": 2,
    "start": 1
   },
   "problem": {
    "text": "Use limit comparison with \\(\\sum_{n=1}^{\\infty}\\frac{1}{n^{2}}\\) to show that \\(\\sum_{n=1}^{\\infty}a_n\\), where \\(a_n=\\frac{(-1)^{n}(3n+5)}{7n^{3}+2}\\), converges absolutely. Name the series in the conclusion.",
    "command_verb": "show"
   },
   "calculator_status": "no_calculator",
   "steps": [
    {
     "cue": "Absolutely: work with \\(|a_n|\\).",
     "why": "The quotient is taken on the series of absolute values.",
     "expr": "(3*n+5)/(7*n**3+2)",
     "relation": "new"
    },
    {
     "cue": "Quotient with the partner, with limit notation.",
     "why": "The setup earns its own point.",
     "expr": "((3*n+5)/(7*n**3+2))/(1/n**2)",
     "relation": "new",
     "point_type_id": "BC-PT-99042"
    },
    {
     "cue": "Take the limit.",
     "why": "Positive and finite.",
     "expr": "3/7",
     "relation": "limit",
     "variable": "n",
     "point": "oo"
    },
    {
     "cue": "The partner has \\(p=2\\).",
     "why": "A p-series with p above 1 converges.",
     "expr": "2",
     "relation": "new"
    },
    {
     "cue": "Conclude, naming the series.",
     "why": "\\(\\sum|a_n|\\) converges, so \\(\\sum a_n\\) converges absolutely."
    }
   ],
   "answer": {
    "form": "statement",
    "expr": "3/7",
    "text": "The series a_n converges absolutely, since the limit of the quotient is 3/7 and the p-series with p = 2 converges."
   }
  }
 ],
 "what_a_reader_scores": [
  {
   "example_id": "ex-2",
   "point_type_ids": [
    "BC-PT-99042"
   ],
   "lines": [
    {
     "point_type_id": "BC-PT-99042",
     "text": "Ratio setup for the ratio test. Earned by: A correct ratio of consecutive terms, with or without absolute values (sg-25:25, sg-22:21). Not earned by: A response that presents no ratio at all, which sg-25:25 states leaves the limit point unavailable."
    }
   ]
  }
 ],
 "common_errors": [
  {
   "error_id": "BC-ERR-10003",
   "observed_behavior": "With several series present in one part, the response concludes that the series converges without identifying which one.",
   "scoring_consequence": "The explanation point is not earned, because the reader cannot tell which series the claim is about (sg-21:23).",
   "wrong_step": {
    "text": "It converges absolutely.",
    "expr": "3/2"
   },
   "right_step": {
    "text": "\\(\\sum\\frac{5(-1)^{n}}{(n+2)^{3/2}}\\) converges absolutely.",
    "expr": "3/2"
   },
   "relation": "equivalent",
   "possible_reason": null,
   "sources": [
    "BC-ERR-10003"
   ],
   "fix_prompt": false
  },
  {
   "error_id": "BC-ERR-10018",
   "observed_behavior": "The response runs a comparison or limit comparison on the signed terms while claiming absolute convergence.",
   "scoring_consequence": "The explanation point requires absolute value symbols, explicitly or implicitly (sg-21:23).",
   "wrong_step": {
    "text": "Quotient on the signed terms.",
    "expr": "((-1)**n*5/(n+2)**(3/2))/(1/n**(3/2))"
   },
   "right_step": {
    "text": "Quotient on \\(|a_n|\\).",
    "expr": "(5/(n+2)**(3/2))/(1/n**(3/2))"
   },
   "relation": "distinct",
   "possible_reason": null,
   "sources": [
    "BC-ERR-10018"
   ],
   "fix_prompt": true
  },
  {
   "error_id": "BC-ERR-10023",
   "observed_behavior": "The response labels a series conditionally convergent when the absolute value series converges, or absolutely convergent when only the signed series converges.",
   "scoring_consequence": "The classification point is lost, since the two labels are exclusive.",
   "wrong_step": {
    "text": "Labelled conditionally convergent.",
    "expr": "conditional"
   },
   "right_step": {
    "text": "Labelled absolutely convergent.",
    "expr": "absolute"
   },
   "relation": "distinct",
   "possible_reason": null,
   "sources": [
    "BC-ERR-10023"
   ],
   "fix_prompt": true
  }
 ],
 "representations": null,
 "prerequisite_bridges": [
  {
   "prq_id": "BC-PRQ-06005",
   "text": "\\(a_n\\) is the term at index n, and \\(|a_n|\\) is its size."
  },
  {
   "prq_id": "BC-PRQ-10008",
   "text": "Read \\(a_n\\) out of sigma form and keep \\((-1)^{n}\\) until the signs are dropped on purpose."
  }
 ],
 "time": {
  "exam_part": "I-A",
  "budget_minutes": 2.14,
  "source": "research/exam/exam-structure.md#Section and part layout",
  "written_steps": {
   "ex-1": [
    1,
    3,
    4
   ]
  },
  "skipped_steps": {
   "ex-1": [
    2
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
    "power": "3/2",
    "coefficient": 5,
    "offset": 2,
    "start": 1,
    "sign_start": "n"
   },
   "completes": "ex-1",
   "stem": {
    "text": "\\(\\sum\\frac{5}{(n+2)^{3/2}}\\) converges by limit comparison with \\(\\sum\\frac{1}{n^{3/2}}\\). Classify \\(\\sum\\frac{5(-1)^{n}}{(n+2)^{3/2}}\\), naming the series.",
    "command_verb": "classify"
   },
   "key": {
    "form": "statement",
    "expr": "3/2",
    "text": "It converges absolutely."
   },
   "steps": [
    {
     "text": "The series of absolute values converges, p = 3/2.",
     "expr": "3/2",
     "relation": "new"
    }
   ],
   "calculator_status": "no_calculator",
   "skills": [
    "BC-SKL-10035"
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
    "power": "2",
    "coefficient": 4,
    "offset": 3,
    "start": 2,
    "sign_start": "n+1"
   },
   "stem": {
    "text": "Classify \\(\\sum_{n=2}^{\\infty}\\frac{4(-1)^{n+1}}{(n+3)^{2}}\\) as absolutely convergent, conditionally convergent, or divergent.",
    "command_verb": "classify"
   },
   "key": {
    "form": "statement",
    "expr": "2",
    "text": "It converges absolutely."
   },
   "steps": [
    {
     "text": "Quotient with 1/n^2.",
     "expr": "(4/(n+3)**2)/(1/n**2)",
     "relation": "new"
    },
    {
     "text": "Limit 4, positive and finite.",
     "expr": "4",
     "relation": "limit",
     "variable": "n",
     "point": "oo"
    },
    {
     "text": "p = 2 above 1.",
     "expr": "2",
     "relation": "new"
    }
   ],
   "calculator_status": "no_calculator",
   "skills": [
    "BC-SKL-10034",
    "BC-SKL-10035"
   ]
  },
  {
   "id": "chk-3",
   "check_kind": "mcq",
   "format": "mcq",
   "bands": [
    "low"
   ],
   "archetype_id": "BC-QA-10006",
   "parameter_draw": {
    "claim": "absolute",
    "partner": "given",
    "gap": 2,
    "top_degree": 1,
    "lead_top": 4,
    "constant_top": 1,
    "lead_bottom": 3,
    "constant_bottom": 2,
    "start": 1
   },
   "stem": {
    "text": "Use limit comparison with \\(\\sum\\frac{1}{n^{2}}\\) to show that \\(\\sum a_n\\), \\(a_n=\\frac{(-1)^{n}(4n+1)}{3n^{3}+2}\\), converges absolutely. Which conclusion is complete?",
    "command_verb": "identify"
   },
   "key": {
    "form": "statement",
    "expr": "4/3",
    "text": "\\(\\sum a_n\\) converges absolutely: the limit of \\(|a_n|/(1/n^2)\\) is 4/3 and \\(\\sum\\frac1{n^2}\\) converges."
   },
   "steps": [
    {
     "text": "|a_n|.",
     "expr": "(4*n+1)/(3*n**3+2)",
     "relation": "new"
    },
    {
     "text": "Quotient.",
     "expr": "((4*n+1)/(3*n**3+2))/(1/n**2)",
     "relation": "new"
    },
    {
     "text": "Limit.",
     "expr": "4/3",
     "relation": "limit",
     "variable": "n",
     "point": "oo"
    }
   ],
   "options": [
    {
     "id": "A",
     "is_key": false,
     "label": "\\(\\sum a_n\\) converges conditionally: the limit is 4/3 and \\(\\sum\\frac1{n^2}\\) converges.",
     "error_path": "BC-ERR-10023",
     "derivation": "the labels exchanged after the series of absolute values was shown to converge"
    },
    {
     "id": "B",
     "is_key": true,
     "label": "\\(\\sum a_n\\) converges absolutely: the limit of \\(|a_n|/(1/n^2)\\) is 4/3 and \\(\\sum\\frac1{n^2}\\) converges.",
     "error_path": null
    },
    {
     "id": "C",
     "is_key": false,
     "label": "\\(\\sum a_n\\) converges absolutely by the alternating series test, since \\(|a_n|\\) decreases to 0.",
     "error_path": "BC-ERR-10018",
     "derivation": "absolute values never tested, the signed series' test called absolute convergence"
    },
    {
     "id": "D",
     "is_key": false,
     "label": "It converges absolutely: the limit is 4/3 and \\(\\sum\\frac1{n^2}\\) converges.",
     "error_path": "BC-ERR-10003",
     "derivation": "the conclusion names no series"
    }
   ],
   "calculator_status": "no_calculator",
   "skills": [
    "BC-SKL-10034",
    "BC-SKL-10035"
   ]
  }
 ],
 "no_figure_reason": "The skills carry series, symbolic and verbal representations only, none figure-bearing, and no key idea describes a process, since a classification is a pair of test results.",
 "delivery": [
  {
   "block": "pr-1",
   "mode": "text",
   "reason": "rule 6: a question on a series pair, no figure-bearing representation",
   "sources": [
    "BC-CON-10013"
   ]
  },
  {
   "block": "orientation",
   "mode": "text",
   "reason": "rule 6: a statement of what a response shows",
   "sources": [
    "BC-CON-10013"
   ]
  },
  {
   "block": "ki-1",
   "mode": "text",
   "reason": "rule 6: BC-REP-11, 01, 04 on BC-SKL-10034, none figure-bearing",
   "sources": [
    "BC-SKL-10034",
    "BC-SKL-10035"
   ]
  },
  {
   "block": "ki-2",
   "mode": "text",
   "reason": "rule 6: a hypothesis and a conclusion in words and symbols",
   "sources": [
    "BC-SKL-10037"
   ]
  },
  {
   "block": "ki-3",
   "mode": "text",
   "reason": "rule 6: a statement with its hypothesis",
   "sources": [
    "BC-SKL-10038"
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
   "block": "err-BC-ERR-10003",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  },
  {
   "block": "err-BC-ERR-10018",
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
  "ki-2",
  "err-BC-ERR-10003",
  "err-BC-ERR-10018",
  "err-BC-ERR-10023",
  "ex-1"
 ],
 "research_lines": [
  {
   "file": "research/units/unit-10-infinite-sequences-series.md",
   "line": "A series may be absolutely convergent, conditionally convergent, or divergent"
  }
 ],
 "inferred": [
  {
   "claim": "BC-PT-99042 is tagged on the limit comparison quotient of ex-2; its reader line names the ratio of consecutive terms, while BC-QA-10006 lists it for the limit comparison setup.",
   "settles": "A point type for the limit comparison setup, or a rubric mapping BC-PT-99042 to it."
  },
  {
   "claim": "BC-QA-10007 lists no point_types, so ex-1 carries no scoring line; the explanation point of sg-21:23 is taught in ki-2 and the error blocks only.",
   "settles": "Point types on BC-QA-10007."
  },
  {
   "claim": "A fluent solver writes the absolute value series, the limit and the conclusion, and holds the choice of partner.",
   "settles": "Timing data per step once the fluency telemetry exists."
  },
  {
   "claim": "ex-2 tags the setup point only, since the answer point's reader line is 110 words and would break the full band cap.",
   "settles": "A cap that admits it, or a shorter reader line."
  }
 ],
 "sources": [
  "BC-CON-10013",
  "BC-SKL-10034",
  "BC-SKL-10035",
  "BC-SKL-10037",
  "BC-SKL-10038",
  "BC-EK-LIM-7A12",
  "BC-EK-LIM-7A13",
  "BC-EK-LIM-7A14",
  "ced:194",
  "BC-QA-10007",
  "BC-QA-10006",
  "BC-PT-99042",
  "BC-ERR-10003",
  "BC-ERR-10018",
  "BC-ERR-10023",
  "BC-PRQ-06005",
  "BC-PRQ-10008",
  "sg-21:23",
  "research/units/unit-10-infinite-sequences-series.md#10.9 Determining Absolute or Conditional Convergence",
  "research/exam/exam-structure.md#Section and part layout"
 ],
 "word_count": {
  "full": 728,
  "brief": 428
 },
 "read_minutes": {
  "full": 4.9,
  "brief": 2.9
 }
}
```
