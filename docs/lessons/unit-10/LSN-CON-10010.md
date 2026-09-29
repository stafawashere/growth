---
title: LSN-CON-10010 Limit comparison of series with nonnegative terms
research_date: 2026-09-29
status: designed
purpose: Authoring spec for the concept lesson on BC-CON-10010, the limit comparison test for series with positive terms, built from authoring_bundle("BC-CON-10010") and the research files it cites, so an author fills plan 15's lesson record without making a teaching decision.
---

# LSN-CON-10010 Limit comparison of series with nonnegative terms

Concept BC-CON-10010 (skills BC-SKL-10025, BC-SKL-10026), topic 10.6 of Unit 10, BC only (ced:191), loaded by two archetypes, BC-QA-10006 (family convergence-test) and BC-QA-10015 (family radius-interval). Hard parent in Unit 10: BC-CON-10009, so a term-by-term comparison and the behaviour of p-series are assumed (docs/lessons/unit-10/README.md, section 1).

## Prediction

Served first, both bands: a `short_answer` on ex-1's own numbers. The terms \(\frac{3n+4}{2n^3+5}\) are close to a constant multiple of \(\frac{1}{n^2}\) for large n, and the student gives the multiple. Key \(\frac32\), the limit step of ex-1, so the blind re-solve of ex-1 covers it. It is answerable before the rule: the leading terms give \(\frac{3n}{2n^3}\), and dividing by \(\frac{1}{n^2}\) leaves \(\frac32\). The resolution states the ratio and the record's claim that two positive series with a positive finite ratio behave alike, with no verdict word. Source: BC-CON-10010 and the topic section the key idea cites.

## Orientation

Served text, from BC-CON-10010 `description_plain` and the topic's Assessment behaviour paragraph (research/units/unit-10-infinite-sequences-series.md#10.6 Comparison Tests for Convergence): the FRQ directs the response to a named comparison series and requires the limit comparison to be carried out exactly as named, with limit notation in the setup, and the conclusion names the series. The orientation states what a response shows, with no count and no frequency.

## Key ideas

Both skills map one BC-EK, BC-EK-LIM-7A9 (ced:191): one core block, both bands.

- ki-1 (core). Paraphrase of the topic's Limit comparison test paragraph: the hypotheses (positive terms, a positive finite limit of the quotient of general terms), the conclusion (the two series converge together or diverge together), the point that the value is compared with zero and infinity and never with one (the 2021 guideline, sg-21:23), and the Naming paragraph. Notation line: the concept's `notation`, "limit comparison". No anchor quote: the CED sentence on ced:191 adds nothing the paraphrase lacks and costs words in the brief band.

## Recognition

BC-QA-10006 (family convergence-test; research/question-analysis/question-archetypes.md#BC-QA-10006 Limit comparison used to classify a series) is the archetype the examples draw on.

- `common_givens`: "a named comparison series", "a Maclaurin series evaluated at a point".
- `asked_to_produce`: "a limit of the quotient of general terms with limit notation", "a statement that the limit is positive and finite", "a conclusion naming the series".
- `typical_wording`: "use the limit comparison test with the given series to show that the series converges absolutely".
- The signal in the stem: the words "limit comparison" with a named p-series, or terms that are quotients of polynomials in n whose degrees differ, with no cheap inequality between the terms.
- Shapes: an MCQ asking which comparison settles a series, and the two point FRQ part BC-FRQ-2021-Q6-B, which names the comparison series (sg-21:23). `multipart_structure`: "Typically one part of the multipart free response question that closes Section II Part B, or a single multiple choice item."

The near miss of the contrast pair is a direct comparison stem, from outside the archetype (BC-QA-10004), on terms with a constant added inside a p-series term, where a clean inequality exists. The pair differs in the test the stem names.

What says "not this concept": the stem names direct comparison or asks for an inequality between terms (BC-CON-10009); terms that alternate (BC-CON-10011); a ratio of consecutive terms \(\frac{a_{n+1}}{a_n}\) rather than of two series' terms (BC-CON-10012).

## Method choice

- st-1, BC-QA-10006, both bands. Cue from `common_givens`. Method, `expected_solution_path[0]` and `[1]`: the quotient of general terms under limit notation, written as the first line without a label. Rival from `wrong_approaches` and `common_distractors`: the limit compared with one (BC-ERR-10019), and no limit symbol (BC-ERR-10017). Separating feature: no clean inequality, only matching growth. The block also carries the contrast pair.
- st-2, BC-QA-10015, low band. The endpoint shape with a shifted p-series term: the limit of the quotient with the plain p-series partner, then the partner's behaviour. Rival: a comparison test on an alternating endpoint series (BC-ERR-10015).

Both archetypes carry `asked_to_produce` and `common_givens`, so both blocks are verified.

## Solution path

- ex-1, BC-QA-10006, both bands, no calculator. Draw: claim converging, partner given, gap 2, top_degree 1, lead_top 3, constant_top 4, lead_bottom 2, constant_bottom 5, start 1, so \(a_n=\frac{3n+4}{2n^3+5}\), partner \(\frac{1}{n^2}\), limit \(\frac32\). No published item on BC-QA-10006 carries this draw (content/items_gen_unit10/ITM-GEN-10006-00 to 21).
- ex-2, low band, no calculator. Draw: claim diverging, partner chosen, gap 2 (the generator sets the gap to 1 for a diverging claim), top_degree 1, lead_top 5, constant_top 2, lead_bottom 3, constant_bottom 7, start 2, so \(a_n=\frac{5n+2}{3n^2+7}\), partner \(\frac1n\), limit \(\frac53\).
- ex-2 is faded from step 3: steps 1 and 2 (the term, the chosen partner and the quotient) are shown, the student writes the limit and the verdict, and steps 3 to 5 then reveal. The fade falls there because the setup repeats ex-1's pattern and the limit and the conclusion are what the student must produce.
- Steps follow `expected_solution_path`: the term (new), the quotient of terms (new), its limit (limit as n to infinity), the statement that the limit is positive and finite with the partner's behaviour, and the verdict, which carry no value. A fluent solver writes the quotient under limit notation, the limit and the verdict, and holds the restatement of the term and the partner's p (Time).
- No productive-failure comparison: BC-CON-10010 is not in `PRODUCTIVE_FAILURE_TARGETS` (docs/lessons/unit-10/README.md, section 6).

## Scoring

BC-QA-10006 lists BC-PT-99042 and BC-PT-99005. Its `scoring_pattern` names two points: one for the setup with limit notation and one for the explanation, which requires the limit to be positive, and the conclusion must name the series (sg-21:23). ex-1 tags BC-PT-99042 on the quotient step and ex-2 tags BC-PT-99005 on the verdict; the lines are `reader_checks` output. The reader line for BC-PT-99042 describes the ratio of consecutive terms in the ratio test, and the reader line for BC-PT-99005 is the generic answer line (library gap, inferred array).

Point losses from research: limit notation is required in the setup of a limit comparison, and the limit is reported as positive; comparing it with one does not earn the explanation point (research/units/unit-10-infinite-sequences-series.md#10.6 Comparison Tests for Convergence, sg-21:23); the conclusion names its series when several are present.

## Traps

Four errors meet the skills, in bundle order: BC-ERR-10003, BC-ERR-10018, BC-ERR-10017, BC-ERR-10019. Low band all four, mid band the first two. All on ex-1's draw.

- err-BC-ERR-10003: "It converges." beside \(\sum a_n\) converges. Equivalent, `fix_prompt` false. No possible reason line (brief band words).
- err-BC-ERR-10018: the quotient of signed terms, against the quotient of sizes. ex-1's terms are positive, so the signed form adds the sign factor the error describes. Distinct, `fix_prompt` true. No possible reason line (brief band words).
- err-BC-ERR-10017: the quotient set equal to \(\frac32\) with no limit symbol, against the limit written. Equivalent, `fix_prompt` false, since the difference is the notation.
- err-BC-ERR-10019: the limit \(\frac32\) compared with one, against positive and finite. Equivalent, `fix_prompt` false. Possible reason, BC-MIS-10011.

## Representations

None. The topic's Representations paragraph names BC-REP-11, 01 and 04 and the conversions general term to comparison partner and limit value to a named conclusion; nothing figure-shaped (docs/lessons/unit-10/README.md, section 6).

## Prerequisite bridge

BC-PRQ-10004 and BC-PRQ-10007, each from its `description_plain` and `failure_signature`, at most 8 words to keep the brief band under its cap.

## Time

Section I Part A, 2.14 minutes for the MCQ shape (research/exam/exam-structure.md#Section and part layout). As a free response part BC-QA-10006 is worth two points, 3.33 minutes (docs/lessons/unit-10/README.md, section 5). A fluent solver writes the quotient under limit notation, the limit value and the verdict naming the series; the restatement of the term and the reading of the partner's p are held [inferred].

## Checks

- chk-1, completion of ex-1, both bands: the limit is given, the conclusion is asked. Key: converges by limit comparison with \(\frac{1}{n^2}\), limit \(\frac32\) positive and finite.
- chk-2, isomorph, both bands, no calculator. Draw: claim converging, partner given, gap 3, top_degree 2, lead_top 2, constant_top 3, lead_bottom 5, constant_bottom 4, start 1, so \(\frac{2n^2+3}{5n^5+4}\) against \(\frac{1}{n^3}\), limit \(\frac25\).
- chk-3, MCQ, low band, no calculator. Draw: claim converging, partner given, gap 2, top_degree 1, lead_top 5, constant_top 3, lead_bottom 2, constant_bottom 6, start 1, so \(a_n=\frac{5n+3}{2n^3+6}\), limit \(\frac52\). Key C. Distractors: A, the limit greater than 1 read as divergence (BC-ERR-10019); B, the quotient set equal to its limit (BC-ERR-10017); D, the conclusion with no series named (BC-ERR-10003).

## Delivery

- pr-1, orientation, ki-1: text. Rule 6: the skills carry BC-REP-01 and 04, none figure-bearing (docs/lessons/unit-10/README.md, section 6). No block is drawn, so the record carries `no_figure_reason`.
- ex-1, ex-2, the four error blocks: step_reveal. Rule 1.

## Band plan

- Low (full): prediction, orientation, bridges, ki-1, st-1 with the contrast pair, st-2, ex-1 and its line, chk-1, the four error blocks, ex-2 (faded from step 3) and its line, chk-2, chk-3. 868 words, 5.8 minutes.
- Mid (brief): prediction, orientation, bridges, ki-1, st-1 with the contrast pair, ex-1 and its line, chk-1, err-BC-ERR-10003, err-BC-ERR-10018, chk-2. 449 words, 3.0 minutes.
- Refresher: ki-1, the four error blocks, ex-1.

## Sources

- BC-CON-10010; BC-SKL-10025, BC-SKL-10026; BC-EK-LIM-7A9; ced:191
- BC-QA-10006, BC-QA-10015, BC-QA-10004; BC-PT-99042, BC-PT-99005
- BC-ERR-10003, BC-ERR-10018, BC-ERR-10017, BC-ERR-10019; BC-MIS-10011
- BC-PRQ-10004, BC-PRQ-10007
- sg-21:23
- research/units/unit-10-infinite-sequences-series.md#10.6 Comparison Tests for Convergence
- research/question-analysis/question-archetypes.md#BC-QA-10006 Limit comparison used to classify a series
- research/exam/exam-structure.md#Section and part layout
- [inferred] the BC-PT-99042 reader line's fit; the tag placement; the held steps; the direct comparison stem of the contrast pair. Each settled as the inferred array states.

## Machine record

```json
{
 "id": "LSN-CON-10010",
 "kind": "concept",
 "target_id": "BC-CON-10010",
 "unit": "10",
 "skills": [
  "BC-SKL-10025",
  "BC-SKL-10026"
 ],
 "prediction": {
  "id": "pr-1",
  "stem": {
   "text": "For large \\(n\\), \\(\\frac{3n+4}{2n^3+5}\\) is close to a constant multiple of \\(\\frac{1}{n^2}\\). What is the multiple?",
   "command_verb": "predict"
  },
  "format": "short_answer",
  "key": {
   "form": "numeric",
   "expr": "3/2"
  },
  "resolution": "The quotient settles near \\(\\frac32\\), so the terms are about \\(\\frac32\\) of \\(\\frac{1}{n^2}\\). Two positive series whose terms have a positive finite ratio in the limit behave alike.",
  "sources": [
   "BC-CON-10010",
   "research/units/unit-10-infinite-sequences-series.md#10.6 Comparison Tests for Convergence"
  ]
 },
 "no_figure_reason": "No skill carries a figure-bearing representation (the topic names series, symbolic and verbal forms) and no key idea describes a process, since the test is a limit of a quotient and a verdict.",
 "orientation": {
  "text": "Limit comparison classifies a positive-term series against a partner whose terms it matches in the limit. A response writes the limit of the quotient with limit notation, says it is positive and finite, and names the series it concludes about.",
  "sources": [
   "BC-CON-10010",
   "research/units/unit-10-infinite-sequences-series.md#10.6 Comparison Tests for Convergence"
  ]
 },
 "key_ideas": [
  {
   "id": "ki-1",
   "ek_id": "BC-EK-LIM-7A9",
   "depth": "core",
   "text": "With positive terms, if \\(\\lim_{n\\to\\infty} \\frac{a_n}{b_n}\\) is a positive finite number, then \\(\\sum a_n\\) and \\(\\sum b_n\\) converge together or diverge together. Compare it with 0 and infinity, never 1. The conclusion names the series it is about.",
   "notation": "limit of the ratio; L positive and finite",
   "quote": null,
   "sources": [
    "BC-EK-LIM-7A9",
    "ced:191",
    "sg-21:23",
    "research/units/unit-10-infinite-sequences-series.md#10.6 Comparison Tests for Convergence"
   ]
  }
 ],
 "strategy": [
  {
   "id": "st-1",
   "archetype_id": "BC-QA-10006",
   "cue": "Rational terms; a p-series partner named or chosen.",
   "method": "\\(\\lim_{n\\to\\infty}\\frac{a_n}{b_n}\\), evaluated, then positive and finite.",
   "rival": "Comparing the limit with 1, or leaving off the limit symbol.",
   "separating_feature": "No clean inequality, only matching growth.",
   "sources": [
    "BC-QA-10006"
   ],
   "evidence_tag": "verified",
   "contrast": {
    "this": {
     "text": "Use the limit comparison test with \\(\\sum\\frac{1}{n^2}\\) to determine whether \\(\\sum_{n=1}^{\\infty}\\frac{5n+2}{4n^3+1}\\) converges or diverges.",
     "archetype_id": "BC-QA-10006"
    },
    "not_this": {
     "text": "Use the direct comparison test to determine whether \\(\\sum_{n=1}^{\\infty}\\frac{3}{n^2+4}\\) converges or diverges.",
     "why_not": "It names direct comparison: an inequality, not a limit."
    },
    "feature": "The named test: a limit of the quotient, or a term-by-term inequality."
   }
  },
  {
   "id": "st-2",
   "archetype_id": "BC-QA-10015",
   "cue": "A power series with an endpoint put in for x, terms shifted by a constant.",
   "method": "Write the endpoint series, take the limit of its quotient with \\(\\frac{1}{n^p}\\), then read the partner.",
   "rival": "A comparison test on an alternating endpoint series.",
   "separating_feature": "Positive terms with a constant added inside.",
   "sources": [
    "BC-QA-10015"
   ],
   "evidence_tag": "verified"
  }
 ],
 "worked_examples": [
  {
   "id": "ex-1",
   "archetype_id": "BC-QA-10006",
   "bands": [
    "low",
    "mid"
   ],
   "parameter_draw": {
    "claim": "converging",
    "partner": "given",
    "gap": "2",
    "top_degree": "1",
    "lead_top": "3",
    "constant_top": "4",
    "lead_bottom": "2",
    "constant_bottom": "5",
    "start": "1"
   },
   "problem": {
    "text": "Use the limit comparison test with \\(\\sum_{n=1}^{\\infty}\\frac{1}{n^2}\\) to determine whether \\(\\sum_{n=1}^{\\infty} a_n\\), where \\(a_n=\\frac{3n+4}{2n^3+5}\\), converges or diverges. State the conclusion, naming the series it concerns.",
    "command_verb": "determine"
   },
   "calculator_status": "no_calculator",
   "steps": [
    {
     "cue": "Positive terms; the partner is \\(b_n=\\frac{1}{n^2}\\).",
     "why": "The test needs positive terms in both series.",
     "expr": "(3*n+4)/(2*n**3+5)",
     "relation": "new"
    },
    {
     "cue": "Form \\(\\frac{a_n}{b_n}\\).",
     "why": "The setup carries limit notation.",
     "expr": "((3*n+4)/(2*n**3+5))/(1/n**2)",
     "relation": "new",
     "point_type_id": "BC-PT-99042"
    },
    {
     "cue": "Take \\(n\\to\\infty\\).",
     "why": "Leading powers decide.",
     "expr": "3/2",
     "relation": "limit",
     "variable": "n",
     "point": "oo"
    },
    {
     "cue": "\\(\\frac32\\) is positive and finite.",
     "why": "That transfers the partner's behaviour, \\(p=2>1\\)."
    },
    {
     "cue": "Name the series in the verdict.",
     "why": "\\(\\sum a_n\\) converges, as \\(\\sum b_n\\) does."
    }
   ],
   "answer": {
    "form": "statement",
    "expr": "converges by limit comparison with 1/n**2, limit 3/2 positive and finite"
   }
  },
  {
   "id": "ex-2",
   "archetype_id": "BC-QA-10006",
   "bands": [
    "low"
   ],
   "parameter_draw": {
    "claim": "diverging",
    "partner": "chosen",
    "gap": "2",
    "top_degree": "1",
    "lead_top": "5",
    "constant_top": "2",
    "lead_bottom": "3",
    "constant_bottom": "7",
    "start": "2"
   },
   "fade_from": 3,
   "problem": {
    "text": "Use the limit comparison test with a p-series you choose to determine whether \\(\\sum_{n=2}^{\\infty} a_n\\), where \\(a_n=\\frac{5n+2}{3n^2+7}\\), converges or diverges. State the conclusion, naming the series it concerns.",
    "command_verb": "determine"
   },
   "calculator_status": "no_calculator",
   "steps": [
    {
     "cue": "Degrees differ by 1, so choose \\(b_n=\\frac1n\\).",
     "why": "The partner must match the growth of \\(a_n\\).",
     "expr": "(5*n+2)/(3*n**2+7)",
     "relation": "new"
    },
    {
     "cue": "Form \\(\\frac{a_n}{b_n}\\).",
     "why": "The setup carries limit notation.",
     "expr": "((5*n+2)/(3*n**2+7))/(1/n)",
     "relation": "new"
    },
    {
     "cue": "Take \\(n\\to\\infty\\).",
     "why": "Equal degrees give the ratio of leading coefficients.",
     "expr": "5/3",
     "relation": "limit",
     "variable": "n",
     "point": "oo"
    },
    {
     "cue": "\\(\\frac53\\) is positive and finite.",
     "why": "The partner, the harmonic series with \\(p=1\\), diverges."
    },
    {
     "cue": "Name the series in the verdict.",
     "why": "\\(\\sum a_n\\) diverges, as \\(\\sum b_n\\) does.",
     "point_type_id": "BC-PT-99005"
    }
   ],
   "answer": {
    "form": "statement",
    "expr": "diverges by limit comparison with 1/n, limit 5/3 positive and finite"
   }
  }
 ],
 "what_a_reader_scores": [
  {
   "example_id": "ex-1",
   "point_type_ids": [
    "BC-PT-99042"
   ],
   "lines": [
    {
     "point_type_id": "BC-PT-99042",
     "text": "Ratio setup for the ratio test. Earned by: A correct ratio of consecutive terms, with or without absolute values (sg-25:25, sg-22:21). Not earned by: A response that presents no ratio at all, which sg-25:25 states leaves the limit point unavailable."
    }
   ]
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
    "expr": "3/2"
   },
   "right_step": {
    "text": "\\(\\sum a_n\\) converges.",
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
    "text": "The quotient of signed terms, \\(\\frac{(-1)^n a_n}{b_n}\\).",
    "expr": "(-1)**n*((3*n+4)/(2*n**3+5))/(1/n**2)"
   },
   "right_step": {
    "text": "The quotient of sizes, \\(\\frac{\\lvert a_n\\rvert}{b_n}\\).",
    "expr": "((3*n+4)/(2*n**3+5))/(1/n**2)"
   },
   "relation": "distinct",
   "possible_reason": null,
   "sources": [
    "BC-ERR-10018"
   ],
   "fix_prompt": true
  },
  {
   "error_id": "BC-ERR-10017",
   "observed_behavior": "The response computes the value of a ratio or a quotient as the index grows without writing the limit symbol.",
   "scoring_consequence": "Limit notation is required for the setup point in a limit comparison (sg-21:23) and for the limit point in a ratio test (sg-25:25).",
   "wrong_step": {
    "text": "\\(\\frac{a_n}{b_n}=\\frac32\\).",
    "expr": "3/2"
   },
   "right_step": {
    "text": "\\(\\lim_{n\\to\\infty}\\frac{a_n}{b_n}=\\frac32\\).",
    "expr": "3/2"
   },
   "relation": "equivalent",
   "possible_reason": null,
   "sources": [
    "BC-ERR-10017"
   ],
   "fix_prompt": false
  },
  {
   "error_id": "BC-ERR-10019",
   "observed_behavior": "The response evaluates the limit of the ratio and then compares that value with one, as in a ratio test, instead of noting that it is positive and finite.",
   "scoring_consequence": "Comparing the limit with one does not earn the explanation point (sg-21:23).",
   "wrong_step": {
    "text": "\\(\\frac32>1\\), so \\(\\sum a_n\\) diverges.",
    "expr": "3/2"
   },
   "right_step": {
    "text": "\\(\\frac32\\) is positive and finite, so \\(\\sum a_n\\) follows \\(\\sum b_n\\).",
    "expr": "3/2"
   },
   "relation": "equivalent",
   "possible_reason": {
    "misconception_id": "BC-MIS-10011",
    "text": "treats one as the deciding threshold rather than requiring a positive finite limit"
   },
   "sources": [
    "BC-ERR-10019",
    "BC-MIS-10011"
   ],
   "fix_prompt": false
  }
 ],
 "representations": null,
 "prerequisite_bridges": [
  {
   "prq_id": "BC-PRQ-10004",
   "text": "Dominant terms decide limits in \\(n\\)."
  },
  {
   "prq_id": "BC-PRQ-10007",
   "text": "Quotients of powers subtract exponents."
  }
 ],
 "time": {
  "exam_part": "I-A",
  "budget_minutes": 2.14,
  "source": "research/exam/exam-structure.md#Section and part layout",
  "written_steps": {
   "ex-1": [
    2,
    3,
    5
   ],
   "ex-2": [
    2,
    3,
    5
   ]
  },
  "skipped_steps": {
   "ex-1": [
    1,
    4
   ],
   "ex-2": [
    1,
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
   "archetype_id": "BC-QA-10006",
   "parameter_draw": {
    "claim": "converging",
    "partner": "given",
    "gap": "2",
    "top_degree": "1",
    "lead_top": "3",
    "constant_top": "4",
    "lead_bottom": "2",
    "constant_bottom": "5",
    "start": "1"
   },
   "completes": "ex-1",
   "stem": {
    "text": "\\(\\lim_{n\\to\\infty}\\frac{a_n}{b_n}=\\frac32\\), with \\(a_n=\\frac{3n+4}{2n^3+5}\\) and \\(b_n=\\frac{1}{n^2}\\). State the conclusion for \\(\\sum_{n=1}^{\\infty} a_n\\).",
    "command_verb": "state"
   },
   "key": {
    "form": "statement",
    "expr": "converges by limit comparison with 1/n**2, limit 3/2 positive and finite"
   },
   "steps": [
    {
     "text": "The limit is positive and finite, and the partner converges.",
     "expr": "3/2",
     "relation": "new"
    }
   ],
   "calculator_status": "no_calculator",
   "skills": [
    "BC-SKL-10026"
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
   "archetype_id": "BC-QA-10006",
   "parameter_draw": {
    "claim": "converging",
    "partner": "given",
    "gap": "3",
    "top_degree": "2",
    "lead_top": "2",
    "constant_top": "3",
    "lead_bottom": "5",
    "constant_bottom": "4",
    "start": "1"
   },
   "stem": {
    "text": "Use the limit comparison test with \\(\\sum_{n=1}^{\\infty}\\frac{1}{n^3}\\) to determine whether \\(\\sum_{n=1}^{\\infty} a_n\\), where \\(a_n=\\frac{2n^2+3}{5n^5+4}\\), converges or diverges. Name the series concluded about.",
    "command_verb": "determine"
   },
   "key": {
    "form": "statement",
    "expr": "converges by limit comparison with 1/n**3, limit 2/5 positive and finite"
   },
   "steps": [
    {
     "text": "Terms.",
     "expr": "(2*n**2+3)/(5*n**5+4)",
     "relation": "new"
    },
    {
     "text": "Quotient with the partner.",
     "expr": "((2*n**2+3)/(5*n**5+4))/(1/n**3)",
     "relation": "new"
    },
    {
     "text": "Limit.",
     "expr": "2/5",
     "relation": "limit",
     "variable": "n",
     "point": "oo"
    }
   ],
   "calculator_status": "no_calculator",
   "skills": [
    "BC-SKL-10025",
    "BC-SKL-10026"
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
    "claim": "converging",
    "partner": "given",
    "gap": "2",
    "top_degree": "1",
    "lead_top": "5",
    "constant_top": "3",
    "lead_bottom": "2",
    "constant_bottom": "6",
    "start": "1"
   },
   "stem": {
    "text": "Use the limit comparison test with \\(\\sum_{n=1}^{\\infty}\\frac{1}{n^2}\\) on \\(a_n=\\frac{5n+3}{2n^3+6}\\). The complete conclusion, naming the series it concerns, is",
    "command_verb": "identify"
   },
   "key": {
    "form": "statement",
    "expr": "sum a_n converges, limit 5/2 positive and finite, sum 1/n**2 converges"
   },
   "steps": [
    {
     "text": "Terms.",
     "expr": "(5*n+3)/(2*n**3+6)",
     "relation": "new"
    },
    {
     "text": "Quotient with the partner.",
     "expr": "((5*n+3)/(2*n**3+6))/(1/n**2)",
     "relation": "new"
    },
    {
     "text": "Limit.",
     "expr": "5/2",
     "relation": "limit",
     "variable": "n",
     "point": "oo"
    }
   ],
   "options": [
    {
     "id": "A",
     "is_key": false,
     "label": "\\(\\sum a_n\\) diverges, because \\(\\lim_{n\\to\\infty}\\frac{a_n}{b_n}=\\frac52\\) is greater than 1.",
     "error_path": "BC-ERR-10019",
     "derivation": "the limit compared with 1, as in the ratio test, and found greater than 1"
    },
    {
     "id": "B",
     "is_key": false,
     "label": "\\(\\sum a_n\\) converges, because \\(\\frac{a_n}{b_n}=\\frac52\\) is positive and finite and \\(\\sum\\frac{1}{n^2}\\) converges.",
     "error_path": "BC-ERR-10017",
     "derivation": "the quotient of the terms written equal to its limit, with the limit notation left off"
    },
    {
     "id": "C",
     "is_key": true,
     "label": "\\(\\sum a_n\\) converges, because \\(\\lim_{n\\to\\infty}\\frac{a_n}{b_n}=\\frac52\\) is positive and finite and \\(\\sum\\frac{1}{n^2}\\) converges."
    },
    {
     "id": "D",
     "is_key": false,
     "label": "It converges, because \\(\\lim_{n\\to\\infty}\\frac{a_n}{b_n}=\\frac52\\) is positive and finite and \\(\\sum\\frac{1}{n^2}\\) converges.",
     "error_path": "BC-ERR-10003",
     "derivation": "the conclusion left with no series named, so it could be read as a statement about the partner"
    }
   ],
   "calculator_status": "no_calculator",
   "skills": [
    "BC-SKL-10025",
    "BC-SKL-10026"
   ]
  }
 ],
 "delivery": [
  {
   "block": "pr-1",
   "mode": "text",
   "reason": "rule 6: the question is about a quotient of terms, symbolic and verbal forms, none figure-bearing",
   "sources": [
    "BC-CON-10010"
   ]
  },
  {
   "block": "orientation",
   "mode": "text",
   "reason": "rule 6: a statement of what a response shows",
   "sources": [
    "BC-CON-10010"
   ]
  },
  {
   "block": "ki-1",
   "mode": "text",
   "reason": "rule 6: BC-REP-01, 04 on BC-SKL-10025 and 10026, none figure-bearing; the idea is a limit and a verdict, not a process",
   "sources": [
    "BC-SKL-10025",
    "BC-SKL-10026"
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
   "block": "err-BC-ERR-10017",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  },
  {
   "block": "err-BC-ERR-10019",
   "mode": "step_reveal",
   "reason": "rule 1",
   "sources": []
  }
 ],
 "refresher": [
  "ki-1",
  "err-BC-ERR-10003",
  "err-BC-ERR-10018",
  "err-BC-ERR-10017",
  "err-BC-ERR-10019",
  "ex-1"
 ],
 "research_lines": [
  {
   "file": "research/units/unit-10-infinite-sequences-series.md",
   "line": "Hypotheses: both series have positive terms and the limit of the quotient of general terms is a positive finite number."
  }
 ],
 "inferred": [
  {
   "claim": "BC-PT-99042 is the record's setup point for BC-QA-10006 (scoring_pattern, sg-21:23), but its reader line describes the ratio of consecutive terms in the ratio test; the line is served as generated.",
   "settles": "A BC-PT record for the limit comparison setup with limit notation, or a reader line that covers both uses."
  },
  {
   "claim": "ex-1 tags BC-PT-99042 on the setup step, and ex-2 tags BC-PT-99005 on the verdict; ex-1 does not tag BC-PT-99005 because its 110 word line would take the brief band past its cap, and ex-2 does not repeat BC-PT-99042 to keep the full band under its cap.",
   "settles": "A brief cap that admits the reader line, or a shorter BC-PT-99005 line."
  },
  {
   "claim": "A fluent solver writes the quotient with its limit, the limit value and the verdict, and holds the restatement of the term and the reading of the partner's p.",
   "settles": "Timing data per step once the fluency telemetry exists."
  },
  {
   "claim": "The direct comparison stem in the contrast pair is a stem shaped like BC-QA-10004, chosen so a clean inequality exists; it is not a published item.",
   "settles": "A check of the stem against the published items on BC-QA-10004."
  }
 ],
 "sources": [
  "BC-CON-10010",
  "BC-SKL-10025",
  "BC-SKL-10026",
  "BC-EK-LIM-7A9",
  "ced:191",
  "BC-QA-10006",
  "BC-QA-10015",
  "BC-QA-10004",
  "BC-PT-99042",
  "BC-PT-99005",
  "BC-ERR-10003",
  "BC-ERR-10018",
  "BC-ERR-10017",
  "BC-ERR-10019",
  "BC-MIS-10011",
  "BC-PRQ-10004",
  "BC-PRQ-10007",
  "sg-21:23",
  "research/units/unit-10-infinite-sequences-series.md#10.6 Comparison Tests for Convergence",
  "research/question-analysis/question-archetypes.md#BC-QA-10006 Limit comparison used to classify a series",
  "research/exam/exam-structure.md#Section and part layout"
 ],
 "word_count": {
  "full": 867,
  "brief": 448
 },
 "read_minutes": {
  "full": 5.8,
  "brief": 3.0
 }
}
```
