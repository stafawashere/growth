---
title: LSN-CON-10009 Direct comparison of series with nonnegative terms
research_date: 2026-09-29
status: designed
purpose: Authoring spec for the concept lesson on BC-CON-10009, the direct comparison test for series with nonnegative terms, built from authoring_bundle("BC-CON-10009") and the research files it cites, so an author fills plan 15's lesson record without making a teaching decision.
---

# LSN-CON-10009 Direct comparison of series with nonnegative terms

Concept BC-CON-10009 (skills BC-SKL-10022, BC-SKL-10023, BC-SKL-10024), topic 10.6 of Unit 10, BC only (ced:191), loaded by two archetypes, BC-QA-10004 (family convergence-test) and BC-QA-10015 (family radius-interval). Hard parent in Unit 10: BC-CON-10007 (harmonic and p-series behaviour), so the partner series are assumed known (docs/lessons/unit-10/README.md, section 1).

## Prediction

Served first, both bands: an `mcq` on ex-1's own numbers. The series of \(\frac{3}{n^3}\) has a finite total T, and the student says what the partial sums of \(\frac{3}{n^3+7}\) do. Key A, they stay below T and level off. The distractors are the reversed direction (they pass T) and the claim that different terms leave the question open. It is answerable before the rule: each term is smaller and positive, so each partial sum is smaller than the matching partial sum of the partner series. The resolution restates the topic's conclusion for a series dominated by a convergent one and carries no verdict word. Source: BC-CON-10009 and the topic section the key idea cites.

## Orientation

Served text, from BC-CON-10009 `description_plain` and the topic's Assessment behaviour paragraph (research/units/unit-10-infinite-sequences-series.md#10.6 Comparison Tests for Convergence): the MCQ asks which comparison settles a series, and the FRQ asks for the analysis of a series by comparison, with the partner named and the inequality direction stated. The orientation states what a response shows, with no count and no frequency.

## Key ideas

The three skills map two BC-EK: BC-EK-LIM-7A8 (all three skills) and BC-EK-LIM-7A9 (BC-SKL-10022), both on ced:191.

- ki-1 (core, BC-EK-LIM-7A8). Paraphrase of the topic's Direct comparison test paragraph: the hypotheses (nonnegative terms, a term-by-term inequality from some index onward), the two conclusions, the direction that supports each, and the Naming paragraph (the conclusion names its series, sg-21:23). Notation line: the concept's `notation`, "term-by-term inequality". No anchor quote: the CED sentence on ced:191 adds nothing the paraphrase lacks.
- ki-2 (extended, BC-EK-LIM-7A9). One statement of the sibling test's hypotheses and conclusion, so the concept's third-way boundary is visible; the full treatment belongs to BC-CON-10010. Low band only.

## Recognition

BC-QA-10004 (family convergence-test; research/question-analysis/question-archetypes.md#BC-QA-10004 Convergence or divergence established with a named test) is the archetype the examples draw on.

- `common_givens`: "candidate series in sigma notation", "a positive-term series known to converge", "a p-series and a geometric series sharing a parameter".
- `asked_to_produce`: "a convergence or divergence verdict with a reason" and "the conditions of the named test".
- `typical_wording`: "determine whether the series converges or diverges, and give a reason for your answer".
- The signal in the stem: positive terms whose general term is a p-series term with a constant added to the denominator (converging case) or a constant added to the numerator (diverging case), so a p-series partner bounds the term by inspection.
- Shapes: an MCQ asking which comparison settles a series (BC-MCQ-CED-019, BC-MCQ-PE2012-027, BC-MCQ-PE2012-043) and a two point FRQ part, BC-FRQ-2024-Q6-A, where an endpoint series is compared with the harmonic series (BC-QA-10015, sg-24:19, sg-24:20). BC-QA-10004 `multipart_structure`: "Typically one part of the multipart free response question that closes Section II Part B, or a single multiple choice item."

The near miss of the contrast pair is a limit comparison stem, from outside the archetype (BC-QA-10006), on terms asymptotic to a p-series where no clean inequality is offered. The pair differs in the test the stem names and in what the terms allow.

What says "not this concept": the stem names the limit comparison test or asks for a limit of the quotient of terms (BC-CON-10010); terms that alternate in sign (BC-CON-10011); a request to classify as absolute or conditional (BC-CON-10013).

## Method choice

- st-1, BC-QA-10004, both bands. Cue from `common_givens` and `asked_to_produce`. Method, `expected_solution_path[1]` and `[2]`: state the term-by-term inequality against a partner and read the partner, written as the first line without a label. Rival from `wrong_approaches`: the inequality in the direction that supports no conclusion (BC-ERR-10016), and terms tending to zero (BC-ERR-10008). Separating feature: a clean term-by-term bound exists. The block also carries the contrast pair.
- st-2, BC-QA-10015, low band. The endpoint shape from the 2024 part: substitute the endpoint, bound the positive terms by the harmonic or a p-series partner, name the endpoint series in the verdict. Rival from `wrong_approaches`: a comparison test on an alternating endpoint series (BC-ERR-10015).

Both archetypes carry `asked_to_produce` and `common_givens`, so both blocks are verified. No served field opens with the reader's own label.

## Solution path

- ex-1, BC-QA-10004, both bands, no calculator. Draw: form comparison_converges, naming unnamed, coefficient 3, large_power 3, shift 7, small_power 2/3, start 1, so \(a_n=\frac{3}{n^3+7}\) and the partner \(\frac{3}{n^3}\). No published item on BC-QA-10004 carries this draw (content/items_gen_unit10/ITM-GEN-10004-00 to 21). The difference \(b_n-a_n\) is \(\frac{21}{n^3(n^3+7)}\), positive for every \(n\).
- ex-2, low band, no calculator. Draw: form comparison_diverges, naming named, coefficient 6, large_power 3/2, shift 5, small_power 1/2, start 1, so \(a_n=\frac{\sqrt n+5}{n}\) and the partner \(\frac{1}{\sqrt n}\). The difference \(a_n-b_n\) is \(\frac5n\).
- ex-2 is faded from step 3: steps 1 and 2 (the term and the difference with the partner) are shown, the student writes the sign of the difference and the verdict, and steps 3 to 5 then reveal. The fade falls there because choosing the partner is the recognition step ex-1 has just modelled, and the sign of the difference is what fixes the direction.
- Steps follow `expected_solution_path`: the term (new), the difference of partner and term (new), its simplification (equivalent), the partner's p (new), and the verdict, which carries no value. Each valued step relation is one the checker recomputes; the inequality itself is carried by the sign of the simplified difference.
- No productive-failure comparison: BC-CON-10009 is not in `PRODUCTIVE_FAILURE_TARGETS` (docs/lessons/unit-10/README.md, section 6).

## Scoring

BC-QA-10004 lists BC-PT-99005 (answer with supporting work or setup shown). ex-2 tags it on the verdict step and quotes the `reader_checks` line. ex-1 carries an empty entry: the BC-PT-99005 line is 110 words and would take the brief band past its cap (inferred array). The archetype's `scoring_pattern` names two points, one for considering the right object and one for the answer with a reason, and a conclusion with no supporting condition earns the first point only (sg-24:19).

Point losses from research: the conclusion must name which series it is about when several are present (research/units/unit-10-infinite-sequences-series.md#10.6 Comparison Tests for Convergence, sg-21:23); the reason point is lost when the test named does not fit the series (sg-24:20).

## Traps

Three errors meet the skills, in bundle order: BC-ERR-10003, BC-ERR-10015, BC-ERR-10016. Low band all three, mid band the first two. All on ex-1's draw.

- err-BC-ERR-10003: the sentence "It converges." beside \(\sum a_n\) converges. The two share a value, so the relation is equivalent and `fix_prompt` is false. No possible reason line (brief band words).
- err-BC-ERR-10015: the signed terms compared with the partner, against the nonnegative terms. Distinct, `fix_prompt` true. No possible reason line (brief band words).
- err-BC-ERR-10016: bounded above by \(\frac3n\), a divergent series, against \(\frac{3}{n^3}\), a convergent one. Distinct, `fix_prompt` true. Possible reason, BC-MIS-10010.

## Representations

None. The topic's Representations paragraph names BC-REP-11, 01 and 04 and the conversions general term to comparison partner and limit value to a named conclusion; nothing figure-shaped (docs/lessons/unit-10/README.md, section 6).

## Prerequisite bridge

BC-PRQ-06002, BC-PRQ-06005, BC-PRQ-10004, each from its `description_plain` and `failure_signature`, at most 12 words to keep the brief band under its cap.

## Time

The exam part the archetype's shape lives in: Section I Part A, 2.14 minutes (research/exam/exam-structure.md#Section and part layout) for the MCQ shape. As a free response part BC-QA-10004 is worth two points, 3.33 minutes (docs/lessons/unit-10/README.md, section 5). A fluent solver writes the inequality, the partner's p and the verdict; the restatement of the term and the difference that fixes the direction are held [inferred].

## Checks

- chk-1, completion of ex-1, both bands: the inequality and the partner's behaviour are given, the verdict is asked. Key: converges by direct comparison with \(\frac3{n^3}\), p = 3.
- chk-2, isomorph, both bands, no calculator. Draw: form comparison_converges, naming named, coefficient 4, large_power 2, shift 9, small_power 1/3, start 1, so \(\frac{4}{n^2+9}\). Key: converges by direct comparison with \(\frac4{n^2}\), p = 2.
- chk-3, MCQ, low band, no calculator. Draw: form comparison_diverges, naming named, coefficient 5, large_power 2, shift 4, small_power 1, start 1, so \(a_n=\frac{n+4}{n^2}\), partner \(\frac1n\), difference \(\frac4{n^2}\). Key C. Distractors: A, bounded above by \(\frac5n\) (BC-ERR-10016); B, the conclusion given about \(\sum\frac1n\) (BC-ERR-10003); D, the alternating series test on positive terms (BC-ERR-10015).

## Delivery

- pr-1, orientation, ki-1, ki-2: text. Rule 6: the skills carry BC-REP-11, 01 and 04, none figure-bearing (docs/lessons/unit-10/README.md, section 6). No block is drawn, so the record carries `no_figure_reason`.
- ex-1, ex-2, the three error blocks: step_reveal. Rule 1.

## Band plan

- Low (full): prediction, orientation, bridges, ki-1, ki-2, st-1 with the contrast pair, st-2, ex-1, chk-1, the three error blocks, ex-2 (faded from step 3) and its line, chk-2, chk-3. 840 words, 5.6 minutes.
- Mid (brief): prediction, orientation, bridges, ki-1, st-1 with the contrast pair, ex-1, chk-1, err-BC-ERR-10003, err-BC-ERR-10015, chk-2. 449 words, 3.0 minutes.
- Refresher: ki-1, the three error blocks, ex-1.

## Sources

- BC-CON-10009; BC-SKL-10022, BC-SKL-10023, BC-SKL-10024; BC-EK-LIM-7A8, BC-EK-LIM-7A9; ced:191
- BC-QA-10004, BC-QA-10015, BC-QA-10006; BC-PT-99005
- BC-ERR-10003, BC-ERR-10015, BC-ERR-10016; BC-MIS-10010
- BC-PRQ-06002, BC-PRQ-06005, BC-PRQ-10004
- sg-21:23, sg-24:19, sg-24:20
- research/units/unit-10-infinite-sequences-series.md#10.6 Comparison Tests for Convergence
- research/question-analysis/question-archetypes.md#BC-QA-10004 Convergence or divergence established with a named test
- research/exam/exam-structure.md#Section and part layout
- [inferred] ex-1's empty scoring entry; the held steps; the limit comparison stem of the contrast pair. Each settled as the inferred array states.

## Machine record

```json
{
 "id": "LSN-CON-10009",
 "kind": "concept",
 "target_id": "BC-CON-10009",
 "unit": "10",
 "skills": [
  "BC-SKL-10022",
  "BC-SKL-10023",
  "BC-SKL-10024"
 ],
 "prediction": {
  "id": "pr-1",
  "stem": {
   "text": "\\(\\sum_{n=1}^{\\infty}\\frac{3}{n^3}\\) has a finite total \\(T\\). What do the partial sums of \\(\\sum_{n=1}^{\\infty}\\frac{3}{n^3+7}\\) do?",
   "command_verb": "predict"
  },
  "format": "mcq",
  "options": [
   {
    "id": "A",
    "label": "They stay below \\(T\\) and level off.",
    "is_key": true
   },
   {
    "id": "B",
    "label": "They pass \\(T\\) and keep growing.",
    "is_key": false
   },
   {
    "id": "C",
    "label": "Nothing can be said.",
    "is_key": false
   }
  ],
  "resolution": "Every term is smaller than its partner, and the partner series converges. A series below a convergent series converges, so the partial sums level off at a finite value.",
  "sources": [
   "BC-CON-10009",
   "research/units/unit-10-infinite-sequences-series.md#10.6 Comparison Tests for Convergence"
  ]
 },
 "no_figure_reason": "No skill carries a figure-bearing representation (the topic names series, symbolic and verbal forms) and no key idea describes a process, since the test is an inequality between terms and a verdict.",
 "orientation": {
  "text": "Comparison places a positive-term series beside one whose behaviour is known. Below a convergent series it converges, and above a divergent one it diverges. A response names the partner, states the inequality, and names the series it concludes about.",
  "sources": [
   "BC-CON-10009",
   "research/units/unit-10-infinite-sequences-series.md#10.6 Comparison Tests for Convergence"
  ]
 },
 "key_ideas": [
  {
   "id": "ki-1",
   "ek_id": "BC-EK-LIM-7A8",
   "depth": "core",
   "text": "With nonnegative terms, if \\(a_n \\le b_n\\) from some index on and \\(\\sum b_n\\) converges, then \\(\\sum a_n\\) converges. If \\(a_n \\ge b_n\\) and \\(\\sum b_n\\) diverges, then \\(\\sum a_n\\) diverges. The inequality must point the way that supports the claim. The conclusion names the series it is about.",
   "notation": "term-by-term inequality",
   "quote": null,
   "sources": [
    "BC-EK-LIM-7A8",
    "ced:191",
    "sg-21:23",
    "research/units/unit-10-infinite-sequences-series.md#10.6 Comparison Tests for Convergence"
   ]
  },
  {
   "id": "ki-2",
   "ek_id": "BC-EK-LIM-7A9",
   "depth": "extended",
   "text": "The limit comparison test is the other comparison method. With positive terms, if \\(\\lim_{n\\to\\infty} a_n/b_n\\) is positive and finite, the two series converge together or diverge together.",
   "notation": "limit comparison",
   "quote": null,
   "sources": [
    "BC-EK-LIM-7A9",
    "ced:191",
    "research/units/unit-10-infinite-sequences-series.md#10.6 Comparison Tests for Convergence"
   ]
  }
 ],
 "strategy": [
  {
   "id": "st-1",
   "archetype_id": "BC-QA-10004",
   "cue": "Positive terms with a p-series or geometric series close by.",
   "method": "Compare term by term with a partner \\(b_n\\), then read the partner.",
   "rival": "A reversed inequality, or terms tending to zero.",
   "separating_feature": "A clean bound, so no limit of a quotient.",
   "sources": [
    "BC-QA-10004"
   ],
   "evidence_tag": "verified",
   "contrast": {
    "this": {
     "text": "Use the direct comparison test to determine whether \\(\\sum_{n=1}^{\\infty}\\frac{5}{n^2+2}\\) converges or diverges.",
     "archetype_id": "BC-QA-10004"
    },
    "not_this": {
     "text": "Use the limit comparison test with \\(\\sum\\frac{1}{n^2}\\) to determine whether \\(\\sum_{n=1}^{\\infty}\\frac{2n+1}{n^3+3}\\) converges.",
     "why_not": "It names the limit comparison test, which uses a quotient, not an inequality."
    },
    "feature": "The named test: an inequality of terms, or a limit of their quotient."
   }
  },
  {
   "id": "st-2",
   "archetype_id": "BC-QA-10015",
   "cue": "A power series with an endpoint value put in for x.",
   "method": "Write the endpoint series, bound its positive terms by a harmonic or p-series partner, and conclude about the endpoint series.",
   "rival": "A comparison test on an alternating endpoint series.",
   "separating_feature": "Positive terms after substitution, with no sign factor.",
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
    "form": "comparison_converges",
    "naming": "unnamed",
    "coefficient": "3",
    "large_power": "3",
    "shift": "7",
    "small_power": "2/3",
    "start": "1"
   },
   "problem": {
    "text": "Determine whether the series \\(\\sum_{n=1}^{\\infty} a_n\\), where \\(a_n = \\frac{3}{n^3+7}\\), converges or diverges. Name the test used and verify its conditions.",
    "command_verb": "determine"
   },
   "calculator_status": "no_calculator",
   "steps": [
    {
     "cue": "Positive terms; \\(n^3\\) dominates.",
     "why": "A p-series partner is in view.",
     "expr": "3/(n**3+7)",
     "relation": "new"
    },
    {
     "cue": "Try \\(b_n=\\frac{3}{n^3}\\); form \\(b_n-a_n\\).",
     "why": "Its sign gives the direction.",
     "expr": "3/n**3 - 3/(n**3+7)",
     "relation": "new"
    },
    {
     "cue": "Combine the fractions.",
     "why": "Positive, so \\(a_n<b_n\\) for every \\(n\\).",
     "expr": "21/(n**3*(n**3+7))",
     "relation": "equivalent"
    },
    {
     "cue": "Read \\(p\\) for \\(\\sum b_n\\).",
     "why": "\\(p=3>1\\), so \\(\\sum b_n\\) converges.",
     "expr": "3",
     "relation": "new"
    },
    {
     "cue": "Name the series in the verdict.",
     "why": "\\(\\sum a_n\\) converges by direct comparison."
    }
   ],
   "answer": {
    "form": "statement",
    "expr": "converges by direct comparison with 3/n**3, p = 3 > 1"
   }
  },
  {
   "id": "ex-2",
   "archetype_id": "BC-QA-10004",
   "bands": [
    "low"
   ],
   "parameter_draw": {
    "form": "comparison_diverges",
    "naming": "named",
    "coefficient": "6",
    "large_power": "3/2",
    "shift": "5",
    "small_power": "1/2",
    "start": "1"
   },
   "fade_from": 3,
   "problem": {
    "text": "Use the direct comparison test to determine whether the series \\(\\sum_{n=1}^{\\infty} a_n\\), where \\(a_n = \\frac{\\sqrt{n}+5}{n}\\), converges or diverges. Verify the conditions of the test.",
    "command_verb": "determine"
   },
   "calculator_status": "no_calculator",
   "steps": [
    {
     "cue": "Positive terms; \\(\\sqrt{n}\\) over \\(n\\) reads like \\(p=\\frac12\\).",
     "why": "A divergent partner needs terms above it.",
     "expr": "(sqrt(n)+5)/n",
     "relation": "new"
    },
    {
     "cue": "Try \\(b_n=\\frac{1}{\\sqrt{n}}\\); form \\(a_n-b_n\\).",
     "why": "Divergence needs \\(a_n\\) above the partner.",
     "expr": "(sqrt(n)+5)/n - 1/sqrt(n)",
     "relation": "new"
    },
    {
     "cue": "Combine the fractions.",
     "why": "Positive, so \\(a_n>b_n>0\\) for every \\(n\\).",
     "expr": "5/n",
     "relation": "equivalent"
    },
    {
     "cue": "Read \\(p\\) for \\(\\sum b_n\\).",
     "why": "\\(p=\\frac12\\le 1\\), so \\(\\sum b_n\\) diverges.",
     "expr": "1/2",
     "relation": "new"
    },
    {
     "cue": "Name the series in the verdict.",
     "why": "\\(\\sum a_n\\) diverges by direct comparison, since \\(a_n>b_n>0\\).",
     "point_type_id": "BC-PT-99005"
    }
   ],
   "answer": {
    "form": "statement",
    "expr": "diverges by direct comparison with 1/sqrt(n), p = 1/2 <= 1"
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
   "error_id": "BC-ERR-10003",
   "observed_behavior": "With several series present in one part, the response concludes that the series converges without identifying which one.",
   "scoring_consequence": "The explanation point is not earned, because the reader cannot tell which series the claim is about (sg-21:23).",
   "wrong_step": {
    "text": "It converges.",
    "expr": "3/(n**3+7)"
   },
   "right_step": {
    "text": "\\(\\sum a_n\\) converges.",
    "expr": "3/(n**3+7)"
   },
   "relation": "equivalent",
   "possible_reason": null,
   "sources": [
    "BC-ERR-10003"
   ],
   "fix_prompt": false
  },
  {
   "error_id": "BC-ERR-10015",
   "observed_behavior": "The response applies a comparison test to an alternating series, or applies the alternating series test to a series of positive terms.",
   "scoring_consequence": "The analysis point at that endpoint is lost, and the interval point with it (sg-25:25).",
   "wrong_step": {
    "text": "Compare the signed terms \\((-1)^n a_n\\) with \\(b_n\\).",
    "expr": "(-1)**n*3/(n**3+7)"
   },
   "right_step": {
    "text": "Compare nonnegative terms, \\(a_n\\).",
    "expr": "3/(n**3+7)"
   },
   "relation": "distinct",
   "possible_reason": null,
   "sources": [
    "BC-ERR-10015"
   ],
   "fix_prompt": true
  },
  {
   "error_id": "BC-ERR-10016",
   "observed_behavior": "The response bounds the terms above by a divergent series, or below by a convergent series, and draws a conclusion anyway.",
   "scoring_consequence": "The answer with reason point is lost because the inequality does not support the claim (sg-24:20).",
   "wrong_step": {
    "text": "Bound above by \\(\\frac{3}{n}\\), a divergent series.",
    "expr": "3/n - 3/(n**3+7)"
   },
   "right_step": {
    "text": "Bound above by \\(\\frac{3}{n^3}\\), a convergent series.",
    "expr": "3/n**3 - 3/(n**3+7)"
   },
   "relation": "distinct",
   "possible_reason": {
    "misconception_id": "BC-MIS-10010",
    "text": "the direction of the term inequality is not tied to the conclusion drawn"
   },
   "sources": [
    "BC-ERR-10016",
    "BC-MIS-10010"
   ],
   "fix_prompt": true
  }
 ],
 "representations": null,
 "prerequisite_bridges": [
  {
   "prq_id": "BC-PRQ-06002",
   "text": "Radicals become powers before \\(p\\) is read."
  },
  {
   "prq_id": "BC-PRQ-06005",
   "text": "\\(a_n\\) and \\(b_n\\) are values at the same \\(n\\)."
  },
  {
   "prq_id": "BC-PRQ-10004",
   "text": "The dominant term in \\(n\\) sets the partner."
  }
 ],
 "time": {
  "exam_part": "I-A",
  "budget_minutes": 2.14,
  "source": "research/exam/exam-structure.md#Section and part layout",
  "written_steps": {
   "ex-1": [
    3,
    4,
    5
   ],
   "ex-2": [
    3,
    4,
    5
   ]
  },
  "skipped_steps": {
   "ex-1": [
    1,
    2
   ],
   "ex-2": [
    1,
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
   "archetype_id": "BC-QA-10004",
   "parameter_draw": {
    "form": "comparison_converges",
    "naming": "unnamed",
    "coefficient": "3",
    "large_power": "3",
    "shift": "7",
    "small_power": "2/3",
    "start": "1"
   },
   "completes": "ex-1",
   "stem": {
    "text": "\\(0<a_n<\\frac{3}{n^3}\\) and \\(\\sum\\frac{3}{n^3}\\) converges. State the verdict for \\(\\sum_{n=1}^{\\infty}\\frac{3}{n^3+7}\\).",
    "command_verb": "state"
   },
   "key": {
    "form": "statement",
    "expr": "converges by direct comparison with 3/n**3, p = 3 > 1"
   },
   "steps": [
    {
     "text": "The bound and the partner's behaviour give the verdict.",
     "expr": "3",
     "relation": "new"
    }
   ],
   "calculator_status": "no_calculator",
   "skills": [
    "BC-SKL-10024"
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
    "form": "comparison_converges",
    "naming": "named",
    "coefficient": "4",
    "large_power": "2",
    "shift": "9",
    "small_power": "1/3",
    "start": "1"
   },
   "stem": {
    "text": "Use the direct comparison test to determine whether \\(\\sum_{n=1}^{\\infty}\\frac{4}{n^2+9}\\) converges or diverges. Verify the conditions.",
    "command_verb": "determine"
   },
   "key": {
    "form": "statement",
    "expr": "converges by direct comparison with 4/n**2, p = 2 > 1"
   },
   "steps": [
    {
     "text": "Terms.",
     "expr": "4/(n**2+9)",
     "relation": "new"
    },
    {
     "text": "Partner minus term.",
     "expr": "4/n**2 - 4/(n**2+9)",
     "relation": "new"
    },
    {
     "text": "Positive.",
     "expr": "36/(n**2*(n**2+9))",
     "relation": "equivalent"
    },
    {
     "text": "p of the partner.",
     "expr": "2",
     "relation": "new"
    }
   ],
   "calculator_status": "no_calculator",
   "skills": [
    "BC-SKL-10022",
    "BC-SKL-10023"
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
    "form": "comparison_diverges",
    "naming": "named",
    "coefficient": "5",
    "large_power": "2",
    "shift": "4",
    "small_power": "1",
    "start": "1"
   },
   "stem": {
    "text": "Use the direct comparison test on \\(\\sum_{n=1}^{\\infty} a_n\\), where \\(a_n=\\frac{n+4}{n^2}\\). The conclusion about \\(\\sum a_n\\) is",
    "command_verb": "identify"
   },
   "key": {
    "form": "statement",
    "expr": "diverges by direct comparison with 1/n"
   },
   "steps": [
    {
     "text": "Terms.",
     "expr": "(n+4)/n**2",
     "relation": "new"
    },
    {
     "text": "Term minus partner.",
     "expr": "(n+4)/n**2 - 1/n",
     "relation": "new"
    },
    {
     "text": "Positive.",
     "expr": "4/n**2",
     "relation": "equivalent"
    },
    {
     "text": "p of the partner.",
     "expr": "1",
     "relation": "new"
    }
   ],
   "options": [
    {
     "id": "A",
     "is_key": false,
     "label": "\\(\\sum a_n\\) diverges by direct comparison, since \\(a_n\\le\\frac{5}{n}\\) and \\(\\sum\\frac5n\\) diverges.",
     "error_path": "BC-ERR-10016",
     "derivation": "the bound written above by a divergent series, which supports no conclusion"
    },
    {
     "id": "B",
     "is_key": false,
     "label": "\\(\\sum\\frac1n\\) diverges by the p-series test.",
     "error_path": "BC-ERR-10003",
     "derivation": "the conclusion attached to the partner, the series asked about never named"
    },
    {
     "id": "C",
     "is_key": true,
     "label": "\\(\\sum a_n\\) diverges by direct comparison, since \\(a_n\\ge\\frac1n\\) and \\(\\sum\\frac1n\\) diverges."
    },
    {
     "id": "D",
     "is_key": false,
     "label": "\\(\\sum a_n\\) converges by the alternating series test, since \\(a_n\\) decreases to 0.",
     "error_path": "BC-ERR-10015",
     "derivation": "the alternating series test applied to a series of positive terms"
    }
   ],
   "calculator_status": "no_calculator",
   "skills": [
    "BC-SKL-10023",
    "BC-SKL-10024"
   ]
  }
 ],
 "delivery": [
  {
   "block": "pr-1",
   "mode": "text",
   "reason": "rule 6: the question is about series, symbolic and verbal forms, none figure-bearing",
   "sources": [
    "BC-CON-10009"
   ]
  },
  {
   "block": "orientation",
   "mode": "text",
   "reason": "rule 6: a statement of what a response shows",
   "sources": [
    "BC-CON-10009"
   ]
  },
  {
   "block": "ki-1",
   "mode": "text",
   "reason": "rule 6: BC-REP-11, 01 on BC-SKL-10022 to 10024, none figure-bearing; the idea is an inequality and a verdict, not a process",
   "sources": [
    "BC-SKL-10022",
    "BC-SKL-10023",
    "BC-SKL-10024"
   ]
  },
  {
   "block": "ki-2",
   "mode": "text",
   "reason": "rule 6: a hypothesis and a conclusion stated in symbols",
   "sources": [
    "BC-SKL-10022"
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
   "block": "err-BC-ERR-10015",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  },
  {
   "block": "err-BC-ERR-10016",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  }
 ],
 "refresher": [
  "ki-1",
  "err-BC-ERR-10003",
  "err-BC-ERR-10015",
  "err-BC-ERR-10016",
  "ex-1"
 ],
 "research_lines": [
  {
   "file": "research/units/unit-10-infinite-sequences-series.md",
   "line": "Hypotheses: both series have nonnegative terms and a term-by-term inequality holds from some index onward."
  }
 ],
 "inferred": [
  {
   "claim": "ex-1 carries no point tag and its what_a_reader_scores entry is empty, because the only point type on BC-QA-10004, BC-PT-99005, has a 110 word reader line that would take the brief band over its cap; ex-2 carries the tag.",
   "settles": "A brief cap that admits the reader line, or a shorter BC-PT-99005 line."
  },
  {
   "claim": "A fluent solver writes the inequality, the partner's p and the verdict, and holds the restatement of the term and the difference that gives the inequality's direction.",
   "settles": "Timing data per step once the fluency telemetry exists."
  },
  {
   "claim": "The limit comparison stem in the contrast pair is a stem shaped like BC-QA-10006, chosen so the terms are asymptotic to a p-series with no clean term-by-term inequality; it is not a published item.",
   "settles": "A check of the stem against the published items on BC-QA-10006."
  }
 ],
 "sources": [
  "BC-CON-10009",
  "BC-SKL-10022",
  "BC-SKL-10023",
  "BC-SKL-10024",
  "BC-EK-LIM-7A8",
  "BC-EK-LIM-7A9",
  "ced:191",
  "BC-QA-10004",
  "BC-QA-10015",
  "BC-QA-10006",
  "BC-PT-99005",
  "BC-ERR-10003",
  "BC-ERR-10015",
  "BC-ERR-10016",
  "BC-MIS-10010",
  "BC-PRQ-06002",
  "BC-PRQ-06005",
  "BC-PRQ-10004",
  "sg-21:23",
  "sg-24:19",
  "sg-24:20",
  "research/units/unit-10-infinite-sequences-series.md#10.6 Comparison Tests for Convergence",
  "research/question-analysis/question-archetypes.md#BC-QA-10004 Convergence or divergence established with a named test",
  "research/exam/exam-structure.md#Section and part layout"
 ],
 "word_count": {
  "full": 839,
  "brief": 448
 },
 "read_minutes": {
  "full": 5.6,
  "brief": 3.0
 }
}
```
