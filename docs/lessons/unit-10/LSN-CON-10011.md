---
title: LSN-CON-10011 The alternating series test and its two conditions
research_date: 2026-09-29
status: designed
purpose: Authoring spec for the concept lesson on BC-CON-10011, the alternating series test with its two conditions on the sizes of the terms, built from authoring_bundle("BC-CON-10011") and the research files it cites, so an author fills plan 15's lesson record without making a teaching decision.
---

# LSN-CON-10011 The alternating series test and its two conditions

Concept BC-CON-10011 (skills BC-SKL-10027, BC-SKL-10028, BC-SKL-10029, BC-SKL-10030), topic 10.7 of Unit 10, BC only (ced:192), loaded by three archetypes, BC-QA-10004, BC-QA-10008 and BC-QA-10015. Hard parents in Unit 10: BC-CON-10001 and BC-CON-10005, so the sequence of partial sums and the nth term test are assumed (docs/lessons/unit-10/README.md, section 1).

## Prediction

Served first, both bands: an `mcq` on ex-1's own series, \(\sum(-1)^{n+1}\frac{4}{n+3}\). Which change would stop the partial sums settling? Key A, term sizes that stay near 1 instead of falling to 0. The distractors are a change of starting index and a change of the coefficient, both of which leave the series convergent, so A is the only true option. It is answerable before the rule: terms that do not tend to 0 cannot give settling partial sums, which the nth term test (BC-EK-LIM-7A5, ced:188) states. The resolution restates that and the alternating series conclusion with no verdict word. Source: BC-CON-10011 and the topic section the key idea cites.

## Orientation

Served text, from BC-CON-10011 `description_plain` and the topic's Assessment behaviour paragraph (research/units/unit-10-infinite-sequences-series.md#10.7 Alternating Series Test for Convergence): justification variants score the statement of the two conditions rather than the conclusion alone, and the test is used at an endpoint of an interval, where naming it is accepted as the analysis. The orientation states what a response shows, with no count and no frequency.

## Key ideas

All four skills map one BC-EK, BC-EK-LIM-7A10 (ced:192): one core block, both bands.

- ki-1 (core). Paraphrase of the topic's Alternating series test paragraph: the hypotheses (alternating signs, decreasing sizes, sizes with limit zero), the conclusion, the Both conditions paragraph (both stated, sg-22:21, sg-24:21) and the No converse paragraph (convergence only). Notation line: the concept's `notation`. No anchor quote: the CED sentence on ced:192 adds nothing the paraphrase lacks.

## Recognition

BC-QA-10004 (family convergence-test; research/question-analysis/question-archetypes.md#BC-QA-10004 Convergence or divergence established with a named test), in its alternating form, is the archetype the examples draw on. BC-QA-10008 (alternating series error bound) and BC-QA-10015 (endpoint series) also load skills of the concept.

- `common_givens`: "a Maclaurin series with its radius of convergence", "a value of x at an end of the interval", "candidate series in sigma notation".
- `asked_to_produce`: "a convergence or divergence verdict with a reason", "the conditions of the named test".
- `typical_wording`: "determine whether the series converges or diverges, and give a reason for your answer".
- The signal in the stem: a sign factor \((-1)^n\) or \((-1)^{n+1}\) in the general term and a request to show convergence, or an endpoint that leaves such a factor after substitution.
- Shapes: an MCQ asking which alternating series converge, with distractors whose terms do not decrease (topic Assessment behaviour; BC-MCQ-CED-019, BC-MCQ-PE2012-027, BC-MCQ-PE2012-043), and an FRQ part at an endpoint, where naming the test is accepted as the analysis (sg-25:25, sg-22:20). `multipart_structure`: "Typically one part of the multipart free response question that closes Section II Part B, or a single multiple choice item."

The near miss of the contrast pair is the same series asked as a classification, from outside the archetype (BC-QA-10007): a stem asking for absolutely convergent, conditionally convergent or divergent tests the series of sizes first.

What says "not this concept": terms of one sign with a p-series partner (BC-CON-10009); a request to classify as absolute or conditional (BC-CON-10013, 10014); an error bound with a tolerance (BC-CON-10015).

## Method choice

- st-1, BC-QA-10004, both bands. Cue from `common_givens` and `asked_to_produce`. Method, `expected_solution_path[1]`: state the conditions and verify them for this series, written as the sizes with the two checks. Rival from `wrong_approaches`: terms tending to 0 taken as enough (BC-ERR-10008), and a comparison test on the alternating series (BC-ERR-10015). Separating feature: the sign factor puts the test on the sizes. The block also carries the contrast pair.
- st-2, BC-QA-10015, low band. The endpoint shape: substitute the endpoint, find the factor \((-1)^n\) left, then apply the two conditions to the sizes. Rival: a comparison test on the alternating endpoint series (BC-ERR-10015).

Both archetypes carry `asked_to_produce` and `common_givens`, so both blocks are verified.

## Solution path

- ex-1, BC-QA-10004, both bands, no calculator. Draw: form alternating, naming unnamed, coefficient 4, large_power 3, shift 3, small_power 1, start 1, so \(a_n=(-1)^{n+1}\frac{4}{n+3}\). No published item on BC-QA-10004 carries this draw (content/items_gen_unit10/ITM-GEN-10004-00 to 21). Sizes \(\frac{4}{n+3}\), limit 0, and \(s_n-s_{n+1}=\frac{4}{(n+3)(n+4)}>0\).
- ex-2, low band, no calculator. Draw: form alternating, naming named, coefficient 7, large_power 3, shift 2, small_power 1/2, start 2, so \(a_n=(-1)^{n+1}\frac{7}{\sqrt{n}+2}\). Sizes \(\frac{7}{\sqrt n+2}\), limit 0, difference \(\frac{7(\sqrt{n+1}-\sqrt n)}{(\sqrt n+2)(\sqrt{n+1}+2)}>0\).
- ex-2 is faded from step 3: steps 1 and 2 (the sizes and their limit) are shown, the student writes the decrease check and the verdict, and steps 3 to 5 then reveal. The fade falls there because the sizes and the limit repeat ex-1's pattern, and the decrease check is what a response omits when it names the test without both conditions.
- Steps follow `expected_solution_path`: the sizes (new), their limit (limit as n to infinity), the difference of consecutive sizes (new), its simplification (equivalent), and the verdict, which carries no value. A fluent solver writes the limit, the positive difference and the verdict, and holds the restatement of the sizes and the unsimplified difference (Time).
- No productive-failure comparison: BC-CON-10011 is not in `PRODUCTIVE_FAILURE_TARGETS` (docs/lessons/unit-10/README.md, section 6).

## Scoring

BC-QA-10004 lists BC-PT-99005 (answer with supporting work or setup shown). ex-2 tags it on the verdict step and quotes the `reader_checks` line. ex-1 carries an empty entry: the BC-PT-99005 line is 110 words and would take the brief band past its cap (inferred array). The archetype's `scoring_pattern` names two points, one for considering the right object and one for the answer with a reason (sg-24:19).

Point losses from research: the justification point requires both conditions to be stated (research/units/unit-10-infinite-sequences-series.md#10.7 Alternating Series Test for Convergence, sg-22:21, sg-24:21); at an endpoint, a comparison applied to an alternating series loses the analysis point (research/scoring/common-point-losses.md#Justification points, sg-25:25).

## Traps

Four errors meet the skills, in bundle order: BC-ERR-10008, BC-ERR-10009, BC-ERR-10015, BC-ERR-10020. Low band all four, mid band the first two. All on ex-1's draw.

- err-BC-ERR-10008: sizes tending to 0 taken as enough, against the added check that the sizes decrease. Distinct, `fix_prompt` true. Possible reason, BC-MIS-10005.
- err-BC-ERR-10009: "By the test, it converges." beside the sizes checked first. The two share the sizes, so the relation is equivalent and `fix_prompt` is false. Possible reason, BC-MIS-10007.
- err-BC-ERR-10015: the signed terms compared with \(\frac4n\), against the sizes tested for both conditions. Distinct, `fix_prompt` true. Possible reason, BC-MIS-10007.
- err-BC-ERR-10020: "Decreasing, so it converges." against decreasing with the limit of the sizes 0. Distinct, `fix_prompt` true. Possible reason, BC-MIS-10013.

## Representations

None. The topic's Representations paragraph names BC-REP-11, 01 and 04 and the conversions sigma form to the sequence of absolute values and verified conditions to a named conclusion; nothing figure-shaped. BC-REP-10 on BC-SKL-10028 and 10029 is a sequence of sizes (docs/lessons/unit-10/README.md, section 6).

## Prerequisite bridge

BC-PRQ-06005, BC-PRQ-10004, BC-PRQ-10008, each from its `description_plain` and `failure_signature`, at most 8 words to keep the brief band under its cap.

## Time

Section I Part A, 2.14 minutes for the MCQ shape (research/exam/exam-structure.md#Section and part layout). As a free response part BC-QA-10004 is worth two points, 3.33 minutes (docs/lessons/unit-10/README.md, section 5). A fluent solver writes the limit of the sizes, the positive difference of consecutive sizes and the verdict naming the series; the restatement of the sizes and the unsimplified difference are held [inferred].

## Checks

- chk-1, completion of ex-1, both bands: the two conditions are given as holding, the verdict is asked. Key: converges by the alternating series test.
- chk-2, isomorph, both bands, no calculator. Draw: form alternating, naming named, coefficient 3, large_power 2, shift 4, small_power 1/2, start 1, so \(\frac{3}{\sqrt n+4}\). Key: converges by the alternating series test, sizes decrease, limit 0.
- chk-3, MCQ, low band, no calculator. Draw: form alternating, naming named, coefficient 5, large_power 3, shift 2, small_power 1, start 1, so \(a_n=(-1)^{n+1}\frac{5}{n+2}\). Key C. Distractors: A, the nth term test used to conclude convergence (BC-ERR-10008); B, the alternating series test with only the limit condition (BC-ERR-10020); D, direct comparison with a divergent partner on a signed series (BC-ERR-10015).

## Delivery

- pr-1, orientation, ki-1: text. Rule 6: the skills carry BC-REP-11, 01, 04 and 10, none figure-bearing (docs/lessons/unit-10/README.md, section 6). No block is drawn, so the record carries `no_figure_reason`.
- ex-1, ex-2, the four error blocks: step_reveal. Rule 1.

## Band plan

- Low (full): prediction, orientation, bridges, ki-1, st-1 with the contrast pair, st-2, ex-1, chk-1, the four error blocks, ex-2 (faded from step 3) and its line, chk-2, chk-3. 838 words, 5.6 minutes.
- Mid (brief): prediction, orientation, bridges, ki-1, st-1 with the contrast pair, ex-1, chk-1, err-BC-ERR-10008, err-BC-ERR-10009, chk-2. 438 words, 3.0 minutes.
- Refresher: ki-1, the four error blocks, ex-1.

## Sources

- BC-CON-10011; BC-SKL-10027, BC-SKL-10028, BC-SKL-10029, BC-SKL-10030; BC-EK-LIM-7A10, BC-EK-LIM-7A5; ced:192, ced:188
- BC-QA-10004, BC-QA-10015, BC-QA-10007; BC-PT-99005
- BC-ERR-10008, BC-ERR-10009, BC-ERR-10015, BC-ERR-10020; BC-MIS-10005, BC-MIS-10007, BC-MIS-10013
- BC-PRQ-06005, BC-PRQ-10004, BC-PRQ-10008
- sg-22:21, sg-24:21, sg-25:25
- research/units/unit-10-infinite-sequences-series.md#10.7 Alternating Series Test for Convergence
- research/question-analysis/question-archetypes.md#BC-QA-10004 Convergence or divergence established with a named test
- research/scoring/common-point-losses.md#Justification points
- research/exam/exam-structure.md#Section and part layout
- [inferred] ex-1's empty scoring entry; the held steps; the classification stem of the contrast pair. Each settled as the inferred array states.

## Machine record

```json
{
 "id": "LSN-CON-10011",
 "kind": "concept",
 "target_id": "BC-CON-10011",
 "unit": "10",
 "skills": [
  "BC-SKL-10027",
  "BC-SKL-10028",
  "BC-SKL-10029",
  "BC-SKL-10030"
 ],
 "prediction": {
  "id": "pr-1",
  "stem": {
   "text": "Which change to \\(\\sum_{n=1}^{\\infty}(-1)^{n+1}\\frac{4}{n+3}\\) would stop its partial sums settling?",
   "command_verb": "predict"
  },
  "format": "mcq",
  "options": [
   {
    "id": "A",
    "label": "Sizes staying near 1 instead of falling to 0",
    "is_key": true
   },
   {
    "id": "B",
    "label": "Starting the sum at \\(n=2\\)",
    "is_key": false
   },
   {
    "id": "C",
    "label": "Replacing 4 by 5",
    "is_key": false
   }
  ],
  "resolution": "Terms that do not tend to 0 make a series diverge, so sizes near 1 stop the partial sums settling. Terms that alternate, decrease in size and tend to 0 give a convergent series.",
  "sources": [
   "BC-CON-10011",
   "research/units/unit-10-infinite-sequences-series.md#10.7 Alternating Series Test for Convergence"
  ]
 },
 "no_figure_reason": "No skill carries a figure-bearing representation (BC-REP-10 on two skills is a sequence of sizes, not a figure) and no key idea describes a process, since the test is two conditions and a verdict.",
 "orientation": {
  "text": "The alternating series test settles a series whose terms alternate in sign. A response states that the terms alternate, that their sizes decrease, and that the sizes tend to 0, then names the series it concludes about.",
  "sources": [
   "BC-CON-10011",
   "research/units/unit-10-infinite-sequences-series.md#10.7 Alternating Series Test for Convergence"
  ]
 },
 "key_ideas": [
  {
   "id": "ki-1",
   "ek_id": "BC-EK-LIM-7A10",
   "depth": "core",
   "text": "A series alternates when its terms alternate in sign. If the sizes \\(\\lvert a_n\\rvert\\) decrease and \\(\\lim_{n\\to\\infty}\\lvert a_n\\rvert=0\\), the series converges. Neither condition alone is enough, and both are stated. The test gives convergence only.",
   "notation": "negative one to the n; decreasing in absolute value",
   "quote": null,
   "sources": [
    "BC-EK-LIM-7A10",
    "ced:192",
    "sg-22:21",
    "sg-24:21",
    "research/units/unit-10-infinite-sequences-series.md#10.7 Alternating Series Test for Convergence"
   ]
  }
 ],
 "strategy": [
  {
   "id": "st-1",
   "archetype_id": "BC-QA-10004",
   "cue": "A sign factor \\((-1)^n\\); convergence is asked.",
   "method": "Sizes \\(\\lvert a_n\\rvert\\): decreasing, and limit 0.",
   "rival": "Terms tending to 0 alone, or a comparison test.",
   "separating_feature": "The sign factor puts the test on the sizes.",
   "sources": [
    "BC-QA-10004"
   ],
   "evidence_tag": "verified",
   "contrast": {
    "this": {
     "text": "Use the alternating series test to determine whether \\(\\sum_{n=1}^{\\infty}(-1)^{n+1}\\frac{6}{n+5}\\) converges.",
     "archetype_id": "BC-QA-10004"
    },
    "not_this": {
     "text": "Classify \\(\\sum_{n=1}^{\\infty}(-1)^{n+1}\\frac{6}{n+5}\\) as absolutely convergent, conditionally convergent or divergent.",
     "why_not": "It asks for a classification, so the series of sizes is tested first."
    },
    "feature": "Show convergence, or classify absolute against conditional."
   }
  },
  {
   "id": "st-2",
   "archetype_id": "BC-QA-10015",
   "cue": "A power series with an endpoint put in for x, leaving a sign factor.",
   "method": "Write the endpoint series, then the sizes, then decrease and limit 0, and conclude about the endpoint series.",
   "rival": "A comparison test on an alternating endpoint series.",
   "separating_feature": "A factor \\((-1)^n\\) survives the substitution.",
   "sources": [
    "BC-QA-10015"
   ],
   "evidence_tag": "verified"
  }
 ],
 "worked_examples": [
  {
   "id": "ex-1",
   "archetype_id": "BC-QA-10004",
   "bands": [
    "low",
    "mid"
   ],
   "parameter_draw": {
    "form": "alternating",
    "naming": "unnamed",
    "coefficient": "4",
    "large_power": "3",
    "shift": "3",
    "small_power": "1",
    "start": "1"
   },
   "problem": {
    "text": "Determine whether \\(\\sum_{n=1}^{\\infty}(-1)^{n+1}\\frac{4}{n+3}\\) converges or diverges. Name the test and verify its conditions.",
    "command_verb": "determine"
   },
   "calculator_status": "no_calculator",
   "steps": [
    {
     "cue": "Sign factor \\((-1)^{n+1}\\); sizes \\(s_n=\\frac{4}{n+3}\\).",
     "why": "The conditions are on the sizes.",
     "expr": "4/(n+3)",
     "relation": "new"
    },
    {
     "cue": "\\(\\lim_{n\\to\\infty}s_n\\).",
     "why": "Sizes must tend to 0.",
     "expr": "0",
     "relation": "limit",
     "variable": "n",
     "point": "oo"
    },
    {
     "cue": "\\(s_n-s_{n+1}\\).",
     "why": "Positive means decreasing.",
     "expr": "4/(n+3) - 4/(n+4)",
     "relation": "new"
    },
    {
     "cue": "Combine.",
     "why": "Positive for every \\(n\\).",
     "expr": "4/((n+3)*(n+4))",
     "relation": "equivalent"
    },
    {
     "cue": "Verdict, naming the series.",
     "why": "\\(\\sum a_n\\) converges by the alternating series test."
    }
   ],
   "answer": {
    "form": "statement",
    "expr": "converges by the alternating series test: alternates, sizes 4/(n+3) decrease, limit 0"
   }
  },
  {
   "id": "ex-2",
   "archetype_id": "BC-QA-10004",
   "bands": [
    "low"
   ],
   "parameter_draw": {
    "form": "alternating",
    "naming": "named",
    "coefficient": "7",
    "large_power": "3",
    "shift": "2",
    "small_power": "1/2",
    "start": "2"
   },
   "fade_from": 3,
   "problem": {
    "text": "Use the alternating series test to determine whether \\(\\sum_{n=2}^{\\infty}(-1)^{n+1}\\frac{7}{\\sqrt{n}+2}\\) converges or diverges. Verify the conditions of the test.",
    "command_verb": "determine"
   },
   "calculator_status": "no_calculator",
   "steps": [
    {
     "cue": "Sign factor \\((-1)^{n+1}\\); sizes \\(s_n=\\frac{7}{\\sqrt{n}+2}\\).",
     "why": "The conditions are on the sizes.",
     "expr": "7/(sqrt(n)+2)",
     "relation": "new"
    },
    {
     "cue": "\\(\\lim_{n\\to\\infty}s_n\\).",
     "why": "The denominator grows without bound.",
     "expr": "0",
     "relation": "limit",
     "variable": "n",
     "point": "oo"
    },
    {
     "cue": "\\(s_n-s_{n+1}\\).",
     "why": "Positive means decreasing.",
     "expr": "7/(sqrt(n)+2) - 7/(sqrt(n+1)+2)",
     "relation": "new"
    },
    {
     "cue": "Combine over one denominator.",
     "why": "\\(\\sqrt{n+1}>\\sqrt{n}\\), so positive.",
     "expr": "7*(sqrt(n+1)-sqrt(n))/((sqrt(n)+2)*(sqrt(n+1)+2))",
     "relation": "equivalent"
    },
    {
     "cue": "Verdict, naming the series.",
     "why": "\\(\\sum a_n\\) converges by the alternating series test, both conditions holding.",
     "point_type_id": "BC-PT-99005"
    }
   ],
   "answer": {
    "form": "statement",
    "expr": "converges by the alternating series test: alternates, sizes 7/(sqrt(n)+2) decrease, limit 0"
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
    "BC-PT-99005"
   ],
   "lines": [
    {
     "point_type_id": "BC-PT-99005",
     "text": "Answer with supporting work or setup shown. Earned by: The correct value together with the setup the prompt demanded, such as a difference and a quotient from a table or an equation that produces the value (sg-26:2, sg-25:4). Not earned by: An unsupported value (sg-23:10, sg-22:9), or a setup with no value (sg-26:2). Notation: sg-22:6 withholds this point for an equation of the form function equals constant, such as a derivative expression set equal to a number without evaluation. Precision: A reported decimal answer must be accurate to three places after the decimal point, rounded or truncated; at most one point per question is lost to inappropriate rounding (sg-25:2, sg-26:2)."
    }
   ]
  }
 ],
 "common_errors": [
  {
   "error_id": "BC-ERR-10008",
   "observed_behavior": "The response states that the series converges on the grounds that the limit of the general term is zero, with no other test applied.",
   "scoring_consequence": "No convergence point is earned, because the nth term test supports divergence only (ced:188).",
   "wrong_step": {
    "text": "Sizes tend to 0, so it converges.",
    "expr": "0"
   },
   "right_step": {
    "text": "Sizes also decrease: \\(\\frac{4}{(n+3)(n+4)}>0\\).",
    "expr": "4/((n+3)*(n+4))"
   },
   "relation": "distinct",
   "possible_reason": {
    "misconception_id": "BC-MIS-10005",
    "text": "reads the nth term test as a two way criterion, so a limit of zero is taken as proof of convergence"
   },
   "sources": [
    "BC-ERR-10008",
    "BC-MIS-10005"
   ],
   "fix_prompt": true
  },
  {
   "error_id": "BC-ERR-10009",
   "observed_behavior": "The response names a convergence test and states a conclusion without establishing the conditions the test requires.",
   "scoring_consequence": "Points tied to the conditions or to the justification are lost even when the verdict is right (sg-21:22).",
   "wrong_step": {
    "text": "By the test, it converges.",
    "expr": "4/(n+3)"
   },
   "right_step": {
    "text": "Sizes \\(\\frac{4}{n+3}\\) checked first.",
    "expr": "4/(n+3)"
   },
   "relation": "equivalent",
   "possible_reason": {
    "misconception_id": "BC-MIS-10007",
    "text": "treats the name of a test as the argument"
   },
   "sources": [
    "BC-ERR-10009",
    "BC-MIS-10007"
   ],
   "fix_prompt": false
  },
  {
   "error_id": "BC-ERR-10015",
   "observed_behavior": "The response applies a comparison test to an alternating series, or applies the alternating series test to a series of positive terms.",
   "scoring_consequence": "The analysis point at that endpoint is lost, and the interval point with it (sg-25:25).",
   "wrong_step": {
    "text": "Compare the signed terms with \\(\\frac4n\\).",
    "expr": "(-1)**(n+1)*4/(n+3)"
   },
   "right_step": {
    "text": "Test the sizes \\(\\frac{4}{n+3}\\) for both conditions.",
    "expr": "4/(n+3)"
   },
   "relation": "distinct",
   "possible_reason": {
    "misconception_id": "BC-MIS-10007",
    "text": "a test may be used on a series it does not cover"
   },
   "sources": [
    "BC-ERR-10015",
    "BC-MIS-10007"
   ],
   "fix_prompt": true
  },
  {
   "error_id": "BC-ERR-10020",
   "observed_behavior": "The response invokes the alternating series test or its error bound without stating that the terms alternate and decrease in absolute value to zero.",
   "scoring_consequence": "The justification point requires both conditions to be stated (sg-22:21, sg-24:21).",
   "wrong_step": {
    "text": "Decreasing, so it converges.",
    "expr": "4/((n+3)*(n+4))"
   },
   "right_step": {
    "text": "Decreasing, and the limit of the sizes is 0.",
    "expr": "0"
   },
   "relation": "distinct",
   "possible_reason": {
    "misconception_id": "BC-MIS-10013",
    "text": "collapses the two requirements of the alternating series test into one statement"
   },
   "sources": [
    "BC-ERR-10020",
    "BC-MIS-10013"
   ],
   "fix_prompt": true
  }
 ],
 "representations": null,
 "prerequisite_bridges": [
  {
   "prq_id": "BC-PRQ-06005",
   "text": "\\(a_n\\) is a value at a stated \\(n\\)."
  },
  {
   "prq_id": "BC-PRQ-10004",
   "text": "Dominant terms decide limits in \\(n\\)."
  },
  {
   "prq_id": "BC-PRQ-10008",
   "text": "The sign factor belongs to \\(a_n\\)."
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
   ],
   "ex-2": [
    2,
    4,
    5
   ]
  },
  "skipped_steps": {
   "ex-1": [
    1,
    3
   ],
   "ex-2": [
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
   "archetype_id": "BC-QA-10004",
   "parameter_draw": {
    "form": "alternating",
    "naming": "unnamed",
    "coefficient": "4",
    "large_power": "3",
    "shift": "3",
    "small_power": "1",
    "start": "1"
   },
   "completes": "ex-1",
   "stem": {
    "text": "The terms of \\(\\sum_{n=1}^{\\infty}(-1)^{n+1}\\frac{4}{n+3}\\) alternate, and their sizes decrease to 0. State the verdict.",
    "command_verb": "state"
   },
   "key": {
    "form": "statement",
    "expr": "converges by the alternating series test: alternates, sizes 4/(n+3) decrease, limit 0"
   },
   "steps": [
    {
     "text": "Both conditions hold.",
     "expr": "0",
     "relation": "new"
    }
   ],
   "calculator_status": "no_calculator",
   "skills": [
    "BC-SKL-10030"
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
   "archetype_id": "BC-QA-10004",
   "parameter_draw": {
    "form": "alternating",
    "naming": "named",
    "coefficient": "3",
    "large_power": "2",
    "shift": "4",
    "small_power": "1/2",
    "start": "1"
   },
   "stem": {
    "text": "Use the alternating series test to determine whether \\(\\sum_{n=1}^{\\infty}(-1)^{n+1}\\frac{3}{\\sqrt{n}+4}\\) converges or diverges. Verify the conditions.",
    "command_verb": "determine"
   },
   "key": {
    "form": "statement",
    "expr": "converges by the alternating series test: alternates, sizes 3/(sqrt(n)+4) decrease, limit 0"
   },
   "steps": [
    {
     "text": "Sizes.",
     "expr": "3/(sqrt(n)+4)",
     "relation": "new"
    },
    {
     "text": "Limit of the sizes.",
     "expr": "0",
     "relation": "limit",
     "variable": "n",
     "point": "oo"
    }
   ],
   "calculator_status": "no_calculator",
   "skills": [
    "BC-SKL-10027",
    "BC-SKL-10028",
    "BC-SKL-10029"
   ]
  },
  {
   "id": "chk-3",
   "check_kind": "mcq",
   "format": "mcq",
   "bands": [
    "low"
   ],
   "archetype_id": "BC-QA-10004",
   "parameter_draw": {
    "form": "alternating",
    "naming": "named",
    "coefficient": "5",
    "large_power": "3",
    "shift": "2",
    "small_power": "1",
    "start": "1"
   },
   "stem": {
    "text": "Use the alternating series test on \\(\\sum_{n=1}^{\\infty}(-1)^{n+1}\\frac{5}{n+2}\\) and verify its conditions. The complete conclusion is",
    "command_verb": "identify"
   },
   "key": {
    "form": "statement",
    "expr": "converges by the alternating series test, sizes 5/(n+2) decrease and have limit 0"
   },
   "steps": [
    {
     "text": "Sizes.",
     "expr": "5/(n+2)",
     "relation": "new"
    },
    {
     "text": "Limit of the sizes.",
     "expr": "0",
     "relation": "limit",
     "variable": "n",
     "point": "oo"
    },
    {
     "text": "Decrease.",
     "expr": "5/(n+2) - 5/(n+3)",
     "relation": "new"
    },
    {
     "text": "Positive.",
     "expr": "5/((n+2)*(n+3))",
     "relation": "equivalent"
    }
   ],
   "options": [
    {
     "id": "A",
     "is_key": false,
     "label": "The series converges by the nth term test, because \\(\\lim_{n\\to\\infty}a_n=0\\).",
     "error_path": "BC-ERR-10008",
     "derivation": "convergence concluded because the terms tend to 0, a reading the nth term test does not support"
    },
    {
     "id": "B",
     "is_key": false,
     "label": "The series converges by the alternating series test, because \\(\\lim_{n\\to\\infty}\\frac{5}{n+2}=0\\).",
     "error_path": "BC-ERR-10020",
     "derivation": "the alternating series test named with only the limit condition, the decrease never stated"
    },
    {
     "id": "C",
     "is_key": true,
     "label": "The series converges by the alternating series test, because it alternates, \\(\\frac{5}{n+2}\\) decreases, and \\(\\lim_{n\\to\\infty}\\frac{5}{n+2}=0\\)."
    },
    {
     "id": "D",
     "is_key": false,
     "label": "The series converges by direct comparison with \\(\\sum\\frac{5}{n}\\), because \\(\\lvert a_n\\rvert\\le\\frac{5}{n}\\).",
     "error_path": "BC-ERR-10015",
     "derivation": "a comparison test applied to a series whose terms are not all positive, against a divergent partner"
    }
   ],
   "calculator_status": "no_calculator",
   "skills": [
    "BC-SKL-10028",
    "BC-SKL-10029",
    "BC-SKL-10030"
   ]
  }
 ],
 "delivery": [
  {
   "block": "pr-1",
   "mode": "text",
   "reason": "rule 6: the question is about a signed series, symbolic and verbal forms, none figure-bearing",
   "sources": [
    "BC-CON-10011"
   ]
  },
  {
   "block": "orientation",
   "mode": "text",
   "reason": "rule 6: a statement of what a response shows",
   "sources": [
    "BC-CON-10011"
   ]
  },
  {
   "block": "ki-1",
   "mode": "text",
   "reason": "rule 6: BC-REP-11, 01, 04 on BC-SKL-10027 to 10030; BC-REP-10 on BC-SKL-10028 and 10029 is a sequence, not a figure-bearing representation; the idea is two conditions and a verdict, not a process",
   "sources": [
    "BC-SKL-10027",
    "BC-SKL-10028",
    "BC-SKL-10029",
    "BC-SKL-10030"
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
   "block": "err-BC-ERR-10008",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  },
  {
   "block": "err-BC-ERR-10009",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  },
  {
   "block": "err-BC-ERR-10015",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  },
  {
   "block": "err-BC-ERR-10020",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  }
 ],
 "refresher": [
  "ki-1",
  "err-BC-ERR-10008",
  "err-BC-ERR-10009",
  "err-BC-ERR-10015",
  "err-BC-ERR-10020",
  "ex-1"
 ],
 "research_lines": [
  {
   "file": "research/units/unit-10-infinite-sequences-series.md",
   "line": "Hypotheses: the terms alternate in sign, the absolute values of the terms decrease, and the limit of the absolute values is zero."
  }
 ],
 "inferred": [
  {
   "claim": "ex-1 carries no point tag and its what_a_reader_scores entry is empty, because the only point type on BC-QA-10004, BC-PT-99005, has a 110 word reader line that would take the brief band over its cap; ex-2 carries the tag.",
   "settles": "A brief cap that admits the reader line, or a shorter BC-PT-99005 line."
  },
  {
   "claim": "A fluent solver writes the limit of the sizes, the positive difference of consecutive sizes and the verdict, and holds the restatement of the sizes and the difference before it is simplified.",
   "settles": "Timing data per step once the fluency telemetry exists."
  },
  {
   "claim": "The classification stem in the contrast pair is a stem shaped like BC-QA-10007, written on the same series as the alternating series test stem; it is not a published item.",
   "settles": "A check of the stem against the published items on BC-QA-10007."
  }
 ],
 "sources": [
  "BC-CON-10011",
  "BC-SKL-10027",
  "BC-SKL-10028",
  "BC-SKL-10029",
  "BC-SKL-10030",
  "BC-EK-LIM-7A10",
  "ced:192",
  "BC-QA-10004",
  "BC-QA-10015",
  "BC-QA-10007",
  "BC-PT-99005",
  "BC-ERR-10008",
  "BC-ERR-10009",
  "BC-ERR-10015",
  "BC-ERR-10020",
  "BC-MIS-10007",
  "BC-MIS-10013",
  "BC-PRQ-06005",
  "BC-PRQ-10004",
  "BC-PRQ-10008",
  "sg-22:21",
  "sg-24:21",
  "sg-25:25",
  "ced:188",
  "research/units/unit-10-infinite-sequences-series.md#10.7 Alternating Series Test for Convergence",
  "research/question-analysis/question-archetypes.md#BC-QA-10004 Convergence or divergence established with a named test",
  "research/exam/exam-structure.md#Section and part layout"
 ],
 "word_count": {
  "full": 837,
  "brief": 437
 },
 "read_minutes": {
  "full": 5.6,
  "brief": 3.0
 }
}
```
