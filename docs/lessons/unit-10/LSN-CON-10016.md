---
title: LSN-CON-10016 Taylor polynomial coefficients from derivative values
research_date: 2026-09-29
status: designed
purpose: Authoring spec for the concept lesson on BC-CON-10016, each Taylor coefficient as a derivative value at the centre divided by a factorial, built from a relation or a table and stopped at the stated degree, from authoring_bundle and the research files it cites.
---

# LSN-CON-10016 Taylor polynomial coefficients from derivative values

Concept BC-CON-10016 (skills BC-SKL-10043 to 10047), topic 10.11 of Unit 10, BC only (ced:196), loaded by BC-QA-10010, BC-QA-10011 and BC-QA-10012. No Unit 10 hard parent; the outside hard parents are BC-SKL-02036, 03002 and 03030 (docs/lessons/unit-10/README.md, section 1).

## Prediction

Served first, both bands: an mcq on ex-1's own numbers. Given f(1) = 3, f'(1) = 7, f''(1) = 20, the question is the coefficient of (x-1)^2 in the degree 2 polynomial. Key B, 10. The distractors 20 and 40 are false. It is answerable before the rule: a term c(x-1)^2 has second derivative 2c, which must match 20. The resolution states the general coefficient with no verdict word.

## Orientation

From the concept's description_plain and the topic's Assessment behaviour paragraph (research/units/unit-10-infinite-sequences-series.md#10.11 Finding Taylor Polynomial Approximations of Functions): MCQ forms give derivative values and ask for a coefficient or the polynomial; free-response forms give a relation or a table and score the derivative, the first two terms and the remaining terms, with a polynomial of the wrong degree or a trailing ellipsis losing the last point (sg-23:19). No count, no frequency.

## Key ideas

Two essential knowledge statements from the skills. BC-EK-LIM-8A1 (ced:196) is core, both bands, from the paragraphs Taylor coefficient and Degree discipline. BC-EK-LIM-8E1 (ced:199) is extended, low band. No anchor quote. Notation: the concept's notation.

## Recognition

BC-QA-10010 (a relation defines the derivatives; wording: find the next derivative and write the Taylor polynomial of the stated degree about the centre), BC-QA-10011 (a table of the function and its derivatives at the centre; wording: use the values in the table to write the Taylor polynomial) and BC-QA-10012 (a related function from a known series) load the skills. Official examples include BC-FRQ-2023-Q6-A, BC-FRQ-2019-Q6-A and BC-MCQ-SAMPLE-021. What says this concept: a stated degree and a centre, with derivative values supplied or derivable. What says not this: no degree and a request for the general term, which is the Taylor series (BC-CON-10023). The near miss of the contrast pair is the same relation asked as a series with its general term, the polynomial against series pair of the unit README, section 3.

## Method choice

st-1 on BC-QA-10010: method is the four entries of expected_solution_path; rival is the wrong_approaches entry, values placed directly as coefficients (BC-ERR-10029). st-2 on BC-QA-10011, whose own evidence_tag is inferred (its scoring pattern is inferred from related constructions), so the block carries evidence_tag inferred. The first block carries the contrast pair.

## Solution path

ex-1, BC-QA-10010, both bands: draw degree 2, centre 1, alpha 2, beta 1, start_value 3, so f' = 2xf + 1, f(1) = 3, f'(1) = 7, f''(1) = 20, f'''(1) = 68 (from the spec's derived values). No published item on BC-QA-10010 carries this draw (content/items_gen_unit10). ex-2, BC-QA-10011, low band, faded from step 3: draw degree 3, centre 2, gap 2, centre_row 2, -3, 4, 6, -1, other_row 5, -2, 7, 1, 3, centre_first yes. Steps 1 and 2 are shown, the student writes the remaining terms, and steps 3 and 4 then reveal. The fade falls there because reading the centre row and forming the first two terms repeats ex-1, and the factorial division is what must be produced. A fluent solver writes the two evaluations and the polynomial; recognising the relation is held.

## Scoring

BC-QA-10010 lists BC-PT-99035, 99068, 99036, 99004, 99022 and 99027; BC-QA-10011 lists BC-PT-99035 and 99036. ex-1 tags no point, for the brief band cap (inferred array); ex-2 tags BC-PT-99035 and BC-PT-99036, lines from reader_checks. Point losses from research: a polynomial with a nonzero term of the wrong degree or a trailing ellipsis loses the final point, and the form of the product rule is scored apart from the derivative (sg-23:19).

## Traps

Four errors meet the skills, in bundle order: BC-ERR-10028, 10029, 10030 and 10031 (each linked to a high severity BC-MIS). Low band all four, mid band the first two. The first three are on ex-1's draw, the fourth on ex-2's table. All are distinct, so fix_prompt true. No possible reason lines, for the brief band words.

## Representations

The topic names BC-REP-01, 03, 11 and 09, and the conversion table to polynomial. The lesson shows ex-2's table, low band, with the centre column marked. Rule 4 chose it: BC-REP-03 on BC-SKL-10045 and the common_givens of BC-QA-10011.

## Prerequisite bridge

BC-PRQ-06005 and BC-PRQ-10002, each from its description_plain and failure_signature.

## Time

BC-QA-10010 is no calculator. The MCQ form is Section I Part A, 2.14 minutes (research/exam/exam-structure.md#Section and part layout). As a free response part: 4 points, 6.67 minutes (docs/lessons/unit-10/README.md, section 5). A fluent solver writes the two evaluations and the polynomial.

## Checks

chk-1 completes ex-1. chk-2 is an isomorph: degree 2, centre 0, alpha -2, beta 1, start_value 2, key 2 + x - 2x^2. chk-3, low band, is a 4 option MCQ: degree 2, centre -1, alpha 1, beta 2, start_value 3, key 3 - (x+1) + 2(x+1)^2. Distractors: the value 4 with no factorial (BC-ERR-10029), the product rule term dropped (BC-ERR-10028), a degree 3 term added (BC-ERR-10030).

## Delivery

Prediction, orientation and key ideas: text (rule 6). Examples and error blocks: step_reveal (rule 1). representations: table (rule 4), with a fallback and a keyboard line.

## Band plan

Low (full): prediction, orientation, bridges, ki-1, ki-2, st-1 with the contrast pair, st-2, ex-1, chk-1, the four error blocks, ex-2 (faded from step 3) and its lines, chk-2, the table, chk-3. 800 words, 5.4 minutes. Mid (brief): prediction, orientation, bridges, ki-1, st-1 with the contrast pair, ex-1, chk-1, err-BC-ERR-10028, err-BC-ERR-10029, chk-2. 428 words, 2.9 minutes. Refresher: ki-1, the four error blocks, ex-1.

## Sources

- BC-CON-10016; BC-SKL-10043, 10044, 10045, 10046, 10047; BC-EK-LIM-8A1, 8E1; ced:196, ced:199
- BC-QA-10010, BC-QA-10011; BC-PT-99035, BC-PT-99036
- BC-ERR-10028, 10029, 10030, 10031; BC-PRQ-06005, 10002
- sg-23:19
- research/units/unit-10-infinite-sequences-series.md#10.11 Finding Taylor Polynomial Approximations of Functions
- research/exam/exam-structure.md#Section and part layout
- [inferred] st-2's basis, the y symbol chain, the untagged ex-1, the held steps; each settled as the inferred array states.

## Machine record

```json
{
 "id": "LSN-CON-10016",
 "kind": "concept",
 "target_id": "BC-CON-10016",
 "unit": "10",
 "skills": [
  "BC-SKL-10043",
  "BC-SKL-10044",
  "BC-SKL-10045",
  "BC-SKL-10046",
  "BC-SKL-10047"
 ],
 "prediction": {
  "id": "pr-1",
  "stem": {
   "text": "Predict. A function has \\(f(1)=3\\), \\(f'(1)=7\\), \\(f''(1)=20\\). In its degree 2 Taylor polynomial about \\(x=1\\), the coefficient of \\((x-1)^2\\) is",
   "command_verb": "predict"
  },
  "format": "mcq",
  "options": [
   {
    "id": "A",
    "label": "20",
    "is_key": false
   },
   {
    "id": "B",
    "label": "10",
    "is_key": true
   },
   {
    "id": "C",
    "label": "40",
    "is_key": false
   }
  ],
  "resolution": "A polynomial \\(c(x-1)^2\\) has second derivative \\(2c\\), so \\(2c=20\\) and \\(c=10=\\frac{f''(1)}{2!}\\). In general the coefficient is \\(\\frac{f^{(n)}(a)}{n!}\\).",
  "sources": [
   "BC-CON-10016",
   "research/units/unit-10-infinite-sequences-series.md#10.11 Finding Taylor Polynomial Approximations of Functions"
  ]
 },
 "orientation": {
  "text": "A Taylor polynomial about x = a takes each coefficient from a derivative at a divided by a factorial. A response shows the derivative values, the first two terms, the remaining terms to the stated degree, and no term beyond it.",
  "sources": [
   "BC-CON-10016",
   "research/units/unit-10-infinite-sequences-series.md#10.11 Finding Taylor Polynomial Approximations of Functions"
  ]
 },
 "key_ideas": [
  {
   "id": "ki-1",
   "ek_id": "BC-EK-LIM-8A1",
   "depth": "core",
   "text": "The coefficient of \\((x-a)^n\\) in the Taylor polynomial for f about \\(x=a\\) is \\(\\frac{f^{(n)}(a)}{n!}\\). The polynomial stops at the stated degree, with no extra term and no ellipsis.",
   "notation": "T sub n of x; f superscript n of a over n factorial",
   "quote": null,
   "sources": [
    "BC-EK-LIM-8A1",
    "ced:196",
    "sg-23:19",
    "research/units/unit-10-infinite-sequences-series.md#10.11 Finding Taylor Polynomial Approximations of Functions"
   ]
  },
  {
   "id": "ki-2",
   "ek_id": "BC-EK-LIM-8E1",
   "depth": "extended",
   "text": "A Taylor polynomial is a partial sum of the Taylor series, so it ends at its degree and is not the series.",
   "notation": "",
   "quote": null,
   "sources": [
    "BC-EK-LIM-8E1",
    "ced:199",
    "research/units/unit-10-infinite-sequences-series.md#10.11 Finding Taylor Polynomial Approximations of Functions"
   ]
  }
 ],
 "strategy": [
  {
   "id": "st-1",
   "archetype_id": "BC-QA-10010",
   "cue": "A relation for derivatives, a value at the centre, a polynomial asked.",
   "method": "Differentiate the relation, evaluate at the centre, divide each value by its factorial, stop at the degree.",
   "rival": "Attaching derivative values as coefficients, with no factorial.",
   "separating_feature": "The coefficient of the nth power is the nth derivative over n factorial.",
   "sources": [
    "BC-QA-10010"
   ],
   "evidence_tag": "verified",
   "contrast": {
    "this": {
     "text": "Given \\(f'(x)=3xf(x)-2\\) and \\(f(1)=2\\), write the degree 2 Taylor polynomial for f about \\(x=1\\).",
     "archetype_id": "BC-QA-10010"
    },
    "not_this": {
     "text": "Given \\(f'(x)=3xf(x)-2\\) and \\(f(1)=2\\), write the Taylor series for f about \\(x=1\\) with its general term.",
     "why_not": "No degree is stated: it asks for the infinite series and its nth term."
    },
    "feature": "A stated degree asks for a finite polynomial."
   }
  },
  {
   "id": "st-2",
   "archetype_id": "BC-QA-10011",
   "cue": "A table of f and its derivatives at the centre.",
   "method": "Take the row at the centre, divide each derivative value by its factorial, attach the power of the displacement.",
   "rival": "Pairing a derivative value with the power of another order.",
   "separating_feature": "The values at the centre, not at the other x, build the coefficients.",
   "sources": [
    "BC-QA-10011"
   ],
   "evidence_tag": "inferred"
  }
 ],
 "worked_examples": [
  {
   "id": "ex-1",
   "archetype_id": "BC-QA-10010",
   "bands": [
    "low",
    "mid"
   ],
   "parameter_draw": {
    "degree": 2,
    "centre": 1,
    "alpha": 2,
    "beta": 1,
    "start_value": 3
   },
   "problem": {
    "text": "Let f satisfy \\(f'(x)=2xf(x)+1\\) and \\(f(1)=3\\). Write the degree 2 Taylor polynomial for f about \\(x=1\\).",
    "command_verb": "write"
   },
   "calculator_status": "no_calculator",
   "steps": [
    {
     "cue": "The relation gives f'.",
     "why": "Evaluate it at the centre.",
     "expr": "2*x*y+1",
     "relation": "new"
    },
    {
     "cue": "At \\(x=1\\), \\(f=3\\).",
     "why": "\\(f'(1)\\) is the first derivative value.",
     "expr": "7",
     "relation": "evaluate",
     "subs": {
      "x": "1",
      "y": "3"
     }
    },
    {
     "cue": "Differentiate f': a product.",
     "why": "Product rule on 2xf, then substitute f'.",
     "expr": "2*y+2*x*(2*x*y+1)",
     "relation": "new"
    },
    {
     "cue": "Evaluate at the centre.",
     "why": "\\(f''(1)\\) is the second value.",
     "expr": "20",
     "relation": "evaluate",
     "subs": {
      "x": "1",
      "y": "3"
     }
    },
    {
     "cue": "Divide by the factorials.",
     "why": "The coefficient is \\(f''(1)/2!\\); stop at degree 2.",
     "expr": "3+7*(x-1)+20*(x-1)**2/factorial(2)",
     "relation": "new"
    }
   ],
   "answer": {
    "form": "symbolic",
    "expr": "3+7*(x-1)+10*(x-1)**2"
   }
  },
  {
   "id": "ex-2",
   "archetype_id": "BC-QA-10011",
   "bands": [
    "low"
   ],
   "fade_from": 3,
   "parameter_draw": {
    "degree": 3,
    "centre": 2,
    "gap": 2,
    "centre_row": [
     2,
     -3,
     4,
     6,
     -1
    ],
    "other_row": [
     5,
     -2,
     7,
     1,
     3
    ],
    "centre_first": "yes"
   },
   "problem": {
    "text": "A table gives f and its derivatives at \\(x=2\\): \\(f=2\\), \\(f'=-3\\), \\(f''=4\\), \\(f'''=6\\), and at \\(x=4\\): \\(5\\), \\(-2\\), \\(7\\), \\(1\\). Write the degree 3 Taylor polynomial for f about \\(x=2\\).",
    "command_verb": "write"
   },
   "calculator_status": "no_calculator",
   "steps": [
    {
     "cue": "The centre is 2: use the x = 2 values.",
     "why": "The x = 4 values are not the centre's."
    },
    {
     "cue": "First two terms.",
     "why": "\\(f(2)\\) and \\(f'(2)\\) over \\(1!\\).",
     "expr": "2-3*(x-2)",
     "relation": "new",
     "point_type_id": "BC-PT-99035"
    },
    {
     "cue": "Remaining terms over \\(2!\\) and \\(3!\\).",
     "why": "Each value with its own order.",
     "expr": "2-3*(x-2)+4*(x-2)**2/factorial(2)+6*(x-2)**3/factorial(3)",
     "relation": "new"
    },
    {
     "cue": "Simplify; stop at degree 3.",
     "why": "No extra term, no ellipsis.",
     "expr": "2-3*(x-2)+2*(x-2)**2+(x-2)**3",
     "relation": "equivalent",
     "point_type_id": "BC-PT-99036"
    }
   ],
   "answer": {
    "form": "symbolic",
    "expr": "2-3*(x-2)+2*(x-2)**2+(x-2)**3"
   }
  }
 ],
 "what_a_reader_scores": [
  {
   "example_id": "ex-1",
   "point_type_ids": [],
   "lines": []
  },
  {
   "example_id": "ex-2",
   "point_type_ids": [
    "BC-PT-99035",
    "BC-PT-99036"
   ],
   "lines": [
    {
     "point_type_id": "BC-PT-99035",
     "text": "First terms of a Taylor or Maclaurin polynomial. Earned by: The first two nonzero terms, in a list or as part of a polynomial or series (sg-26:22, sg-25:22). Not earned by: A correct expanded form that is not written in powers of the centre, which sg-25:22 states earns this point but not the remaining-term point."
    },
    {
     "point_type_id": "BC-PT-99036",
     "text": "Remaining terms of a Taylor or Maclaurin polynomial. Earned by: The remaining required terms, completing the polynomial to the requested degree (sg-26:22, sg-25:22). Not earned by: A polynomial carrying terms of higher degree than asked, or an ellipsis suggesting the series continues (sg-25:22, sg-23:19, sg-23:21)."
    }
   ]
  }
 ],
 "common_errors": [
  {
   "error_id": "BC-ERR-10028",
   "observed_behavior": "The response differentiates a relation defining a derivative and omits a product rule factor or a chain rule factor.",
   "scoring_consequence": "The form of the rule is scored separately from the resulting derivative, so an omitted factor loses the second point while the first may survive (sg-23:19).",
   "wrong_step": {
    "text": "Product rule missing the \\(2f\\) term.",
    "expr": "2*x*(2*x*y+1)"
   },
   "right_step": {
    "text": "\\(2f\\) plus \\(2xf'\\).",
    "expr": "2*y+2*x*(2*x*y+1)"
   },
   "relation": "distinct",
   "possible_reason": null,
   "sources": [
    "BC-ERR-10028"
   ],
   "fix_prompt": true
  },
  {
   "error_id": "BC-ERR-10029",
   "observed_behavior": "The response places the derivative value directly as the coefficient of the power, with no factorial denominator.",
   "scoring_consequence": "The polynomial is not the requested one and its term points are lost (sg-23:19).",
   "wrong_step": {
    "text": "Coefficient 20, no factorial.",
    "expr": "3+7*(x-1)+20*(x-1)**2"
   },
   "right_step": {
    "text": "Coefficient \\(20/2!\\).",
    "expr": "3+7*(x-1)+10*(x-1)**2"
   },
   "relation": "distinct",
   "possible_reason": null,
   "sources": [
    "BC-ERR-10029"
   ],
   "fix_prompt": true
  },
  {
   "error_id": "BC-ERR-10030",
   "observed_behavior": "The response writes a polynomial that includes terms beyond the requested degree, or appends an ellipsis, turning the answer into a series.",
   "scoring_consequence": "A polynomial with terms of higher degree, or with an ellipsis, does not earn the final polynomial point (sg-23:20, sg-23:21).",
   "wrong_step": {
    "text": "A degree 3 term added.",
    "expr": "3+7*(x-1)+10*(x-1)**2+34*(x-1)**3/3"
   },
   "right_step": {
    "text": "Stops at degree 2.",
    "expr": "3+7*(x-1)+10*(x-1)**2"
   },
   "relation": "distinct",
   "possible_reason": null,
   "sources": [
    "BC-ERR-10030"
   ],
   "fix_prompt": true
  },
  {
   "error_id": "BC-ERR-10031",
   "observed_behavior": "The response reads a table of derivative values and pairs a derivative of one order with the power of another.",
   "scoring_consequence": "Each misplaced value spoils the term that depends on it.",
   "wrong_step": {
    "text": "The \\(f''\\) and \\(f'''\\) values swapped.",
    "expr": "2-3*(x-2)+6*(x-2)**2/factorial(2)+4*(x-2)**3/factorial(3)"
   },
   "right_step": {
    "text": "Each value with its own order.",
    "expr": "2-3*(x-2)+2*(x-2)**2+(x-2)**3"
   },
   "relation": "distinct",
   "possible_reason": null,
   "sources": [
    "BC-ERR-10031"
   ],
   "fix_prompt": true
  }
 ],
 "representations": {
  "text": "Ex-2's table: the x = 2 column is the centre.",
  "figure": {
   "kind": "table",
   "columns": [
    "order",
    "x = 2",
    "x = 4"
   ],
   "rows": [
    [
     "f",
     "2",
     "5"
    ],
    [
     "f'",
     "-3",
     "-2"
    ],
    [
     "f''",
     "4",
     "7"
    ],
    [
     "f'''",
     "6",
     "1"
    ]
   ],
   "labels": [
    {
     "text": "centre column: x = 2",
     "placement": "inside",
     "at": "first value column header"
    }
   ]
  },
  "sources": [
   "research/units/unit-10-infinite-sequences-series.md#10.11 Finding Taylor Polynomial Approximations of Functions",
   "BC-QA-10011"
  ]
 },
 "prerequisite_bridges": [
  {
   "prq_id": "BC-PRQ-06005",
   "text": "\\(f'(1)\\) is a value at the centre, not a formula in x."
  },
  {
   "prq_id": "BC-PRQ-10002",
   "text": "\\(2!=2\\) and \\(3!=6\\); divide, never subtract."
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
    5
   ]
  },
  "skipped_steps": {
   "ex-1": [
    1,
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
   "archetype_id": "BC-QA-10010",
   "parameter_draw": {
    "degree": 2,
    "centre": 1,
    "alpha": 2,
    "beta": 1,
    "start_value": 3
   },
   "completes": "ex-1",
   "stem": {
    "text": "\\(f(1)=3\\), \\(f'(1)=7\\), \\(f''(1)=20\\). Write the degree 2 Taylor polynomial for f about \\(x=1\\).",
    "command_verb": "write"
   },
   "key": {
    "form": "symbolic",
    "expr": "3+7*(x-1)+10*(x-1)**2"
   },
   "steps": [
    {
     "text": "Divide by the factorials.",
     "expr": "3+7*(x-1)+20*(x-1)**2/factorial(2)",
     "relation": "new"
    },
    {
     "text": "Simplify.",
     "expr": "3+7*(x-1)+10*(x-1)**2",
     "relation": "equivalent"
    }
   ],
   "calculator_status": "no_calculator",
   "skills": [
    "BC-SKL-10044"
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
   "archetype_id": "BC-QA-10010",
   "parameter_draw": {
    "degree": 2,
    "centre": 0,
    "alpha": -2,
    "beta": 1,
    "start_value": 2
   },
   "stem": {
    "text": "Let f satisfy \\(f'(x)=-2xf(x)+1\\) and \\(f(0)=2\\). Write the degree 2 Taylor polynomial for f about \\(x=0\\).",
    "command_verb": "write"
   },
   "key": {
    "form": "symbolic",
    "expr": "2+x-2*x**2"
   },
   "steps": [
    {
     "text": "f'.",
     "expr": "-2*x*y+1",
     "relation": "new"
    },
    {
     "text": "At the centre.",
     "expr": "1",
     "relation": "evaluate",
     "subs": {
      "x": "0",
      "y": "2"
     }
    },
    {
     "text": "f'' by the product rule.",
     "expr": "-2*y-2*x*(-2*x*y+1)",
     "relation": "new"
    },
    {
     "text": "At the centre.",
     "expr": "-4",
     "relation": "evaluate",
     "subs": {
      "x": "0",
      "y": "2"
     }
    },
    {
     "text": "Over the factorials.",
     "expr": "2+x-4*x**2/factorial(2)",
     "relation": "new"
    }
   ],
   "calculator_status": "no_calculator",
   "skills": [
    "BC-SKL-10043",
    "BC-SKL-10044",
    "BC-SKL-10046"
   ]
  },
  {
   "id": "chk-3",
   "check_kind": "mcq",
   "format": "mcq",
   "bands": [
    "low"
   ],
   "archetype_id": "BC-QA-10010",
   "parameter_draw": {
    "degree": 2,
    "centre": -1,
    "alpha": 1,
    "beta": 2,
    "start_value": 3
   },
   "stem": {
    "text": "Let f satisfy \\(f'(x)=xf(x)+2\\) and \\(f(-1)=3\\). The degree 2 Taylor polynomial for f about \\(x=-1\\) is",
    "command_verb": "identify"
   },
   "key": {
    "form": "symbolic",
    "expr": "3-(x+1)+2*(x+1)**2"
   },
   "steps": [
    {
     "text": "f'.",
     "expr": "x*y+2",
     "relation": "new"
    },
    {
     "text": "At the centre.",
     "expr": "-1",
     "relation": "evaluate",
     "subs": {
      "x": "-1",
      "y": "3"
     }
    },
    {
     "text": "f'' by the product rule.",
     "expr": "y+x*(x*y+2)",
     "relation": "new"
    },
    {
     "text": "At the centre.",
     "expr": "4",
     "relation": "evaluate",
     "subs": {
      "x": "-1",
      "y": "3"
     }
    },
    {
     "text": "Over the factorials.",
     "expr": "3-(x+1)+4*(x+1)**2/factorial(2)",
     "relation": "new"
    }
   ],
   "options": [
    {
     "id": "A",
     "is_key": false,
     "expr": "3-(x+1)+4*(x+1)**2",
     "error_path": "BC-ERR-10029",
     "derivation": "the second derivative value 4 as the coefficient, with no factorial"
    },
    {
     "id": "B",
     "is_key": false,
     "expr": "3-(x+1)+(x+1)**2/2",
     "error_path": "BC-ERR-10028",
     "derivation": "the derivative of xf taken as x f' alone, so the second value is 1"
    },
    {
     "id": "C",
     "is_key": true,
     "expr": "3-(x+1)+2*(x+1)**2",
     "error_path": null
    },
    {
     "id": "D",
     "is_key": false,
     "expr": "3-(x+1)+2*(x+1)**2-(x+1)**3",
     "error_path": "BC-ERR-10030",
     "derivation": "the degree 3 term, with third derivative value -6 over 3!, added"
    }
   ],
   "calculator_status": "no_calculator",
   "skills": [
    "BC-SKL-10043",
    "BC-SKL-10044"
   ]
  }
 ],
 "delivery": [
  {
   "block": "pr-1",
   "mode": "text",
   "reason": "rule 6: a question on one coefficient, no figure-bearing representation",
   "sources": [
    "BC-CON-10016"
   ]
  },
  {
   "block": "orientation",
   "mode": "text",
   "reason": "rule 6: a statement of what a response shows",
   "sources": [
    "BC-CON-10016"
   ]
  },
  {
   "block": "ki-1",
   "mode": "text",
   "reason": "rule 6: BC-REP-01, 11 on BC-SKL-10043, 10044, 10046, 10047; a formula, not a process",
   "sources": [
    "BC-SKL-10044"
   ]
  },
  {
   "block": "ki-2",
   "mode": "text",
   "reason": "rule 6: a statement relating polynomial and series",
   "sources": [
    "BC-SKL-10047"
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
   "block": "err-BC-ERR-10028",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  },
  {
   "block": "err-BC-ERR-10029",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  },
  {
   "block": "err-BC-ERR-10030",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  },
  {
   "block": "err-BC-ERR-10031",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  },
  {
   "block": "representations",
   "mode": "table",
   "reason": "rule 4: BC-REP-03 on BC-SKL-10045 and BC-QA-10011 common_givens, a table of the function and its derivatives at the centre",
   "sources": [
    "BC-SKL-10045",
    "BC-QA-10011"
   ],
   "spec": {
    "kind": "table",
    "representations": [
     "BC-REP-03"
    ],
    "columns": [
     "order",
     "x = 2",
     "x = 4"
    ],
    "rows": [
     [
      "f",
      "2",
      "5"
     ],
     [
      "f'",
      "-3",
      "-2"
     ],
     [
      "f''",
      "4",
      "7"
     ],
     [
      "f'''",
      "6",
      "1"
     ]
    ],
    "labels": [
     {
      "text": "centre column: x = 2",
      "placement": "inside",
      "at": "first value column header"
     }
    ]
   },
   "fallback": "the four rows as static text",
   "keyboard": "no control; cells reached in reading order with Tab"
  }
 ],
 "refresher": [
  "ki-1",
  "err-BC-ERR-10028",
  "err-BC-ERR-10029",
  "err-BC-ERR-10030",
  "err-BC-ERR-10031",
  "ex-1"
 ],
 "research_lines": [
  {
   "file": "research/units/unit-10-infinite-sequences-series.md",
   "line": "The coefficient of the nth degree term of the Taylor polynomial for f about x equals a is the nth derivative of f at a divided by n factorial"
  }
 ],
 "inferred": [
  {
   "claim": "st-2 is tagged inferred because BC-QA-10011 carries evidence_tag inferred and its scoring pattern is inferred from related constructions (sg-23:19).",
   "settles": "A 2021 to 2025 rubric for the table shape."
  },
  {
   "claim": "ex-1's derivative chain is written with a symbol y for f(x), so the product rule and substitution steps are new relations and the evaluations are recomputed.",
   "settles": "A step relation for a derivative of an unknown function."
  },
  {
   "claim": "ex-1 tags no point, because its reader line would take 43 to 100 words of the 450 word brief band; ex-2 tags BC-PT-99035 and BC-PT-99036.",
   "settles": "A brief cap that admits the reader line."
  },
  {
   "claim": "A fluent solver writes the two evaluations and the polynomial, and holds the recognition of the relation.",
   "settles": "Timing data per step once the fluency telemetry exists."
  }
 ],
 "sources": [
  "BC-CON-10016",
  "BC-SKL-10043",
  "BC-SKL-10044",
  "BC-SKL-10045",
  "BC-SKL-10046",
  "BC-SKL-10047",
  "BC-EK-LIM-8A1",
  "BC-EK-LIM-8E1",
  "ced:196",
  "ced:199",
  "BC-QA-10010",
  "BC-QA-10011",
  "BC-PT-99035",
  "BC-PT-99036",
  "BC-ERR-10028",
  "BC-ERR-10029",
  "BC-ERR-10030",
  "BC-ERR-10031",
  "BC-PRQ-06005",
  "BC-PRQ-10002",
  "sg-23:19",
  "research/units/unit-10-infinite-sequences-series.md#10.11 Finding Taylor Polynomial Approximations of Functions",
  "research/exam/exam-structure.md#Section and part layout"
 ],
 "word_count": {
  "full": 800,
  "brief": 428
 },
 "read_minutes": {
  "full": 5.4,
  "brief": 2.9
 }
}
```
