---
title: LSN-CON-10005 The nth term test as a one directional test
research_date: 2026-09-29
status: designed
purpose: Authoring spec for the concept lesson on BC-CON-10005, the nth term test as a test for divergence only, built from authoring_bundle("BC-CON-10005") and the research files it cites, so an author fills plan 15's lesson record without making a teaching decision.
---

# LSN-CON-10005 The nth term test as a one directional test

Concept BC-CON-10005 (skills BC-SKL-10011, BC-SKL-10012, BC-SKL-10013), topic 10.3 of Unit 10, BC only (ced:188), loaded by two archetypes, BC-QA-10001 and BC-QA-10004. Hard parent BC-CON-10001 (docs/lessons/unit-10/README.md, section 1); no outside hard parent, so the limit of a rational expression in n is assumed.

## Prediction

Served first, both bands: an `mcq` on ex-1's own numbers. The terms \(a_n=\frac{3n+1}{2n+5}\) are close to 1.5 for large n, and the student says what the partial sums do as terms are added. Key C, they grow without bound. The distractors are that they level off near 1.5 and that they level off at a value set by the first terms; both are false, and a student can rule them out before any rule, because a running total that gains about 1.5 each step cannot level off. The resolution states the same reasoning and names the test, with no verdict word. Delivery: text. Source: BC-CON-10005 and the topic 10.3 section that ki-1 cites.

## Orientation

Served text (29 words), from BC-CON-10005 `description_plain` ("shrinking terms prove nothing") and the topic's Assessment behaviour paragraph: the multiple choice form asks which of four series diverges by the nth term test with distractors whose terms go to zero, and the free response form uses the test as a screening step before a named test (research/units/unit-10-infinite-sequences-series.md#10.3 The nth Term Test for Divergence). The orientation states what a response must show: the limit of the general term and what it settles. No count, no frequency.

## Key ideas

All three skills map to one essential knowledge statement, BC-EK-LIM-7A5 (ced:188): one core block, both bands.

- ki-1 (core). Paraphrase of the Required mathematical knowledge paragraphs nth term test (hypothesis: the limit of a sub n is not zero or does not exist; conclusion: the series diverges) and One directional (a limit of zero is consistent with both outcomes, as the harmonic series shows). The harmonic series sentence is served because the topic states it; the series itself is taught in LSN-CON-10007. Notation line: the concept's `notation`. No anchor quote: the ced:188 sentence "The nth term test is a test for divergence of a series." adds nothing the first sentence lacks and costs 12 words in the brief band.

## Recognition

Two archetypes load the three skills: BC-QA-10001 (family procedure-selection) and BC-QA-10004 (family convergence-test). The examples and checks draw from BC-QA-10001, because BC-QA-10004's `parameter_spec` has no rational or nonzero limit form (its forms are comparison and alternating).

- BC-QA-10001 (research/question-analysis/question-archetypes.md#BC-QA-10001 Selecting a convergence test for a given series): `common_givens` "a series of numbers in sigma or expanded form"; `asked_to_produce` "a convergence or divergence verdict naming the series", "the name of an applicable test", "a check of that test's conditions"; `typical_wording` "determine whether the series converges or diverges, and justify your answer". The generator's nth_term form is a quotient of two linear expressions whose limit is the ratio of the leading coefficients.
- BC-QA-10004 `official_examples` BC-MCQ-CED-019, BC-MCQ-PE2012-027 and BC-MCQ-PE2012-043, and BC-FRQ-2024-Q6-A, where the nth term test screens an endpoint series before a named test (topic Assessment behaviour, sg-24:19). BC-QA-10001 `official_examples` BC-MCQ-PE2012-009.

The signal in the stem: a series in sigma form whose general term is a quotient of expressions in n, with a request to determine convergence. The near miss of the contrast pair is the same general term asked as a sequence, which belongs to BC-CON-10001 and BC-CON-10002: BC-SKL-10011's `adaptive.common_confusions` names "the same limit computed as a statement about a sequence". The two stems share a general term and differ in the word sigma against the word sequence.

What says "not this concept": the word sequence with no sigma (a limit of terms only); a request for the sum of the series (geometric or telescoping, BC-CON-10004, BC-CON-10002); a series whose terms are already known to tend to 0 and a named test asked for (BC-CON-10009 onward).

## Method choice

One strategy block, both bands.

- st-1, BC-QA-10001. Cue from `common_givens` and `asked_to_produce`: a sigma series with a rational general term and a verdict requested. Method, `expected_solution_path[0]` "read the general term", written as the limit of it with its value. Rival, `wrong_approaches` "concluding convergence because the terms approach zero" (BC-ERR-10008). Separating feature: a limit not equal to 0 settles divergence, and a limit of 0 settles nothing. Both cue fields exist, so the block is verified. The block carries the contrast pair. No served field opens with the reader's own label.
- BC-QA-10004 loads the same skills, but its strategy is the named-test shape (name the test, state its conditions, verify them); its block is not served, to keep both bands under their caps [inferred: settled by a brief cap that admits a second block].

## Solution path

- ex-1, BC-QA-10001, both bands, no calculator. Draw: form nth_term, lead_top 3, constant_top 1, lead_bottom 2, constant_bottom 5, start 1 (the other spec keys are carried unused). \(a_n=\frac{3n+1}{2n+5}\), limit \(\frac32\), diverges. The constraint `constant_top * lead_bottom != lead_top * constant_bottom` holds (2 against 15). No published item on BC-QA-10001 carries this draw (content/items_gen_unit10/ITM-GEN-10001-00 to 21, and the agent items list none on BC-QA-10001).
- ex-2, low band. Draw: form pseries, power 3/2, coefficient 5, start 2. \(a_n=\frac{5}{n^{3/2}}\), limit 0, the test gives no conclusion. Not equal to any published pseries draw.
- ex-2 is faded from step 2: step 1 (the general term) is shown, the student writes the limit, and steps 2 and 3 then reveal. The fade falls there because reading the general term repeats ex-1 and the new work is what a limit of 0 permits.
- Steps follow `expected_solution_path`: the general term (new), its limit as n grows (limit), and the sentence that names the test's verdict (no value). A fluent solver writes all three lines; the division by n is held. No productive-failure comparison: BC-CON-10005 is not in `PRODUCTIVE_FAILURE_TARGETS`.

## Scoring

None. BC-QA-10001 lists no `point_types`, so the lesson carries no what_a_reader_scores entry, no step carries a point tag and the lesson says nothing about points (plan 15, R14). BC-QA-10004 lists BC-PT-99005 but is not the archetype of any example here. The archetype's `scoring_pattern` says a named test earns credit alone and that a verdict without the chosen test's conditions earns nothing (sg-21:23, sg-25:25); it is not served, since it names no BC-PT.

## Traps

Three active errors meet the skills, in the bundle's order (each linked to a high severity BC-MIS, then by id): BC-ERR-10007, BC-ERR-10008, BC-ERR-10009. Low band all three, mid band the first two. Blocks 10007 and 10009 are on ex-1's draw; block 10008 is on ex-2's draw, because a zero limit is the only case where that error can occur.

- err-BC-ERR-10007: limit read as 0 against \(\frac32\). Distinct, fix prompt true. No possible reason line (brief band words); the record links BC-MIS-10005.
- err-BC-ERR-10008: for \(\frac{5}{n^{3/2}}\), the limit 0 read as convergence, against the same limit read as no conclusion. Both steps hold the value 0, so the relation is equivalent and the fix prompt false. No possible reason line.
- err-BC-ERR-10009: the divergence stated with no limit shown, against the limit \(\frac32\ne0\) written first. The wrong step carries the empty set as its expression, the precedent of the missing element in LSN-CON-08021 err-BC-ERR-08043. Distinct, fix prompt true. Possible reason, BC-MIS-10007.

## Representations

None. The topic's Representations paragraph names BC-REP-11, 01 and 04 and the conversions sigma form to the general term and its limit, and a limit value to a verbal conclusion naming the test; nothing figure-shaped (docs/lessons/unit-10/README.md, section 6).

## Prerequisite bridge

BC-PRQ-06005, BC-PRQ-10004 and BC-PRQ-10008, each from its `description_plain` and `failure_signature`, gated by state, in both bands.

## Time

Section I Part A, 2.14 minutes (research/exam/exam-structure.md#Section and part layout), the multiple choice form the topic names; BC-QA-10001 records no FRQ example with points, and its `scoring_pattern` names none [inferred]. A fluent solver writes the general term, the limit and the verdict; the division by n is held. The minutes go on the limit.

## Checks

- chk-1, completion of ex-1, both bands. \(a_n\) given, the limit asked. Key \(\frac32\).
- chk-2, isomorph, both bands, no calculator. Draw: form nth_term, lead_top 5, constant_top -2, lead_bottom 4, constant_bottom 3, start 2. \(\frac{5n-2}{4n+3}\), key \(\frac54\). Constraint holds (-8 against 15).
- chk-3, MCQ, low band. Draw: form pseries, power 1/3, coefficient 6, start 1. \(a_n=\frac{6}{\sqrt[3]{n}}\). Key: the limit is 0, so the test gives no conclusion. Distractors: the limit reported as 6, so diverges (BC-ERR-10007); the limit 0 read as convergence (BC-ERR-10008); the test shown to give divergence because every term is positive, with the limit never checked (BC-ERR-10009). The stem asks about the test's own output, so only the key is true of the test.

## Delivery

- orientation, ki-1: text. Rule 6: BC-REP-11, 01, 04, none figure-bearing (docs/lessons/unit-10/README.md, section 6). The key idea states a condition on one limit, so no rule for a process fires. No block is drawn, so the record carries `no_figure_reason`.
- ex-1, ex-2, the three error blocks: step_reveal. Rule 1.

## Band plan

- Low (full): prediction, orientation, bridges, ki-1, st-1 with the contrast pair, ex-1, chk-1, the three error blocks, ex-2 (faded from step 2), chk-2, chk-3. 611 words, 4.1 minutes.
- Mid (brief): prediction, orientation, bridges, ki-1, st-1 with the contrast pair, ex-1, chk-1, err-BC-ERR-10007, err-BC-ERR-10008, chk-2. 447 words, 3.0 minutes.
- Refresher: ki-1, the three error blocks, ex-1.

## Sources

- BC-CON-10005; BC-SKL-10011, BC-SKL-10012, BC-SKL-10013; BC-EK-LIM-7A5; ced:188
- BC-QA-10001, BC-QA-10004
- BC-ERR-10007, BC-ERR-10008, BC-ERR-10009; BC-MIS-10007
- BC-PRQ-06005, BC-PRQ-10004, BC-PRQ-10008
- research/units/unit-10-infinite-sequences-series.md#10.3 The nth Term Test for Divergence
- research/question-analysis/question-archetypes.md#BC-QA-10001 Selecting a convergence test for a given series
- research/exam/exam-structure.md#Section and part layout
- [inferred] the held step, Part A for a no-point archetype, the unserved BC-QA-10004 block and the delivery choice, each settled as the inferred array states.

## Machine record

```json
{
 "id": "LSN-CON-10005",
 "kind": "concept",
 "target_id": "BC-CON-10005",
 "unit": "10",
 "skills": [
  "BC-SKL-10011",
  "BC-SKL-10012",
  "BC-SKL-10013"
 ],
 "prediction": {
  "id": "pr-1",
  "stem": {
   "text": "Predict. A series has terms \\(a_n=\\frac{3n+1}{2n+5}\\), each close to 1.5 once n is large. As more terms are added, what do the partial sums do?",
   "command_verb": "predict"
  },
  "format": "mcq",
  "options": [
   {
    "id": "A",
    "label": "They level off near 1.5.",
    "is_key": false
   },
   {
    "id": "B",
    "label": "They level off at a value set by the first terms.",
    "is_key": false
   },
   {
    "id": "C",
    "label": "They grow without bound.",
    "is_key": true
   }
  ],
  "resolution": "Each added term is near \\(\\frac32\\), so the sums rise by about \\(\\frac32\\) each time and never level off. The nth term test states this for any terms that do not approach 0.",
  "sources": [
   "BC-CON-10005",
   "research/units/unit-10-infinite-sequences-series.md#10.3 The nth Term Test for Divergence"
  ]
 },
 "no_figure_reason": "The test is a statement about the limit of one general term. No skill carries a figure-bearing representation and no key idea describes a process.",
 "orientation": {
  "text": "A response finds the limit of the general term and states what it settles: a limit other than 0 means divergence, and a limit of 0 settles nothing.",
  "sources": [
   "BC-CON-10005",
   "research/units/unit-10-infinite-sequences-series.md#10.3 The nth Term Test for Divergence"
  ]
 },
 "key_ideas": [
  {
   "id": "ki-1",
   "ek_id": "BC-EK-LIM-7A5",
   "depth": "core",
   "text": "If \\(\\lim_{n\\to\\infty}a_n\\) is not 0, or does not exist, then \\(\\sum a_n\\) diverges. A limit of 0 allows convergence or divergence, so the test never shows convergence. The harmonic series has terms tending to 0 and diverges.",
   "notation": "limit of a sub n; test for divergence",
   "quote": null,
   "sources": [
    "BC-EK-LIM-7A5",
    "ced:188",
    "research/units/unit-10-infinite-sequences-series.md#10.3 The nth Term Test for Divergence"
   ]
  }
 ],
 "strategy": [
  {
   "id": "st-1",
   "archetype_id": "BC-QA-10001",
   "cue": "A series in sigma form with a rational general term, and a request for a verdict.",
   "method": "\\(\\lim_{n\\to\\infty}a_n\\), with its value.",
   "rival": "Concluding convergence because the terms approach zero.",
   "separating_feature": "A limit not equal to 0 settles divergence. A limit of 0 settles nothing.",
   "sources": [
    "BC-QA-10001",
    "research/question-analysis/question-archetypes.md#BC-QA-10001 Selecting a convergence test for a given series"
   ],
   "evidence_tag": "verified",
   "contrast": {
    "this": {
     "text": "Determine whether \\(\\sum_{n=1}^{\\infty}\\frac{4n-3}{3n+7}\\) converges or diverges, and justify.",
     "archetype_id": "BC-QA-10001"
    },
    "not_this": {
     "text": "Determine whether the sequence \\(a_n=\\frac{4n-3}{3n+7}\\) converges.",
     "why_not": "It asks about the list of terms, so the limit of \\(a_n\\) is the whole answer."
    },
    "feature": "A sigma asks about partial sums. The word sequence asks about the terms."
   }
  }
 ],
 "worked_examples": [
  {
   "id": "ex-1",
   "archetype_id": "BC-QA-10001",
   "bands": [
    "low",
    "mid"
   ],
   "parameter_draw": {
    "form": "nth_term",
    "power": "3/2",
    "coefficient": "5",
    "start": "1",
    "lead_top": "3",
    "constant_top": "1",
    "lead_bottom": "2",
    "constant_bottom": "5",
    "ratio": "1/3",
    "base": "4",
    "degree": "2"
   },
   "problem": {
    "text": "Use the nth term test on \\(\\sum_{n=1}^{\\infty}\\frac{3n+1}{2n+5}\\). Find \\(\\lim_{n\\to\\infty}a_n\\) and state what the test shows.",
    "command_verb": "find"
   },
   "calculator_status": "no_calculator",
   "steps": [
    {
     "cue": "The sigma gives the general term.",
     "why": "The test looks at \\(a_n\\) alone.",
     "expr": "(3*n+1)/(2*n+5)",
     "relation": "new"
    },
    {
     "cue": "Let n grow: divide top and bottom by n.",
     "why": "Terms settle near a fixed value.",
     "expr": "3/2",
     "relation": "limit",
     "variable": "n",
     "point": "oo"
    },
    {
     "cue": "The limit is not 0.",
     "why": "Terms that do not shrink to 0 cannot let the sum settle, so the series diverges."
    }
   ],
   "answer": {
    "form": "numeric",
    "expr": "3/2"
   }
  },
  {
   "id": "ex-2",
   "archetype_id": "BC-QA-10001",
   "bands": [
    "low"
   ],
   "fade_from": 2,
   "parameter_draw": {
    "form": "pseries",
    "power": "3/2",
    "coefficient": "5",
    "start": "2",
    "lead_top": "3",
    "constant_top": "1",
    "lead_bottom": "2",
    "constant_bottom": "5",
    "ratio": "1/3",
    "base": "4",
    "degree": "2"
   },
   "problem": {
    "text": "Use the nth term test on \\(\\sum_{n=2}^{\\infty}\\frac{5}{n^{3/2}}\\). Find \\(\\lim_{n\\to\\infty}a_n\\) and state what the test shows.",
    "command_verb": "find"
   },
   "calculator_status": "no_calculator",
   "steps": [
    {
     "cue": "The sigma gives the general term.",
     "why": "The test looks at \\(a_n\\) alone.",
     "expr": "5/n**(3/2)",
     "relation": "new"
    },
    {
     "cue": "The power of n in the denominator grows.",
     "why": "Dividing 5 by ever larger numbers approaches 0.",
     "expr": "0",
     "relation": "limit",
     "variable": "n",
     "point": "oo"
    },
    {
     "cue": "The limit is 0.",
     "why": "A limit of 0 fits convergence and divergence, so the test gives no conclusion and another test is needed."
    }
   ],
   "answer": {
    "form": "numeric",
    "expr": "0"
   }
  }
 ],
 "what_a_reader_scores": [],
 "common_errors": [
  {
   "error_id": "BC-ERR-10007",
   "observed_behavior": "The response reports the limit of a sub n as zero or as a nonzero number that the expression does not support, often mishandling a ratio of like degree polynomials.",
   "scoring_consequence": "A conclusion built on the wrong limit earns no reasoning point even when the verdict happens to be correct.",
   "wrong_step": {
    "text": "Limit read as 0.",
    "expr": "0"
   },
   "right_step": {
    "text": "Limit \\(\\frac32\\).",
    "expr": "3/2"
   },
   "relation": "distinct",
   "possible_reason": null,
   "sources": [
    "BC-ERR-10007"
   ],
   "fix_prompt": true
  },
  {
   "error_id": "BC-ERR-10008",
   "observed_behavior": "The response states that the series converges on the grounds that the limit of the general term is zero, with no other test applied.",
   "scoring_consequence": "No convergence point is earned, because the nth term test supports divergence only (ced:188).",
   "wrong_step": {
    "text": "\\(\\lim a_n=0\\), so \\(\\sum\\frac{5}{n^{3/2}}\\) converges.",
    "expr": "0"
   },
   "right_step": {
    "text": "\\(\\lim a_n=0\\), so the test is silent.",
    "expr": "0"
   },
   "relation": "equivalent",
   "possible_reason": null,
   "sources": [
    "BC-ERR-10008"
   ],
   "fix_prompt": false
  },
  {
   "error_id": "BC-ERR-10009",
   "observed_behavior": "The response names a convergence test and states a conclusion without establishing the conditions the test requires.",
   "scoring_consequence": "Points tied to the conditions or to the justification are lost even when the verdict is right (sg-21:22).",
   "wrong_step": {
    "text": "Diverges by the nth term test.",
    "expr": "EmptySet"
   },
   "right_step": {
    "text": "\\(\\lim a_n=\\frac32\\ne0\\), so it diverges.",
    "expr": "3/2"
   },
   "relation": "distinct",
   "possible_reason": {
    "misconception_id": "BC-MIS-10007",
    "text": "treats the name of a test as the argument"
   },
   "sources": [
    "BC-ERR-10009",
    "BC-MIS-10007"
   ],
   "fix_prompt": true
  }
 ],
 "representations": null,
 "prerequisite_bridges": [
  {
   "prq_id": "BC-PRQ-06005",
   "text": "Evaluate \\(a_n\\) at a stated index. Failure: \\(f\\) read at the wrong input."
  },
  {
   "prq_id": "BC-PRQ-10004",
   "text": "Compare dominant terms. Failure: like degrees read as 0."
  },
  {
   "prq_id": "BC-PRQ-10008",
   "text": "Read \\(a_n\\) from sigma form. Failure: the alternating factor lost."
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
   "archetype_id": "BC-QA-10001",
   "parameter_draw": {
    "form": "nth_term",
    "power": "3/2",
    "coefficient": "5",
    "start": "1",
    "lead_top": "3",
    "constant_top": "1",
    "lead_bottom": "2",
    "constant_bottom": "5",
    "ratio": "1/3",
    "base": "4",
    "degree": "2"
   },
   "completes": "ex-1",
   "stem": {
    "text": "\\(a_n=\\frac{3n+1}{2n+5}\\). Find \\(\\lim_{n\\to\\infty}a_n\\).",
    "command_verb": "find"
   },
   "key": {
    "form": "numeric",
    "expr": "3/2"
   },
   "steps": [
    {
     "text": "The general term.",
     "expr": "(3*n+1)/(2*n+5)",
     "relation": "new"
    },
    {
     "text": "Its limit.",
     "expr": "3/2",
     "relation": "limit",
     "variable": "n",
     "point": "oo"
    }
   ],
   "calculator_status": "no_calculator",
   "skills": [
    "BC-SKL-10011"
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
   "archetype_id": "BC-QA-10001",
   "parameter_draw": {
    "form": "nth_term",
    "power": "3/2",
    "coefficient": "5",
    "start": "2",
    "lead_top": "5",
    "constant_top": "-2",
    "lead_bottom": "4",
    "constant_bottom": "3",
    "ratio": "1/3",
    "base": "4",
    "degree": "2"
   },
   "stem": {
    "text": "Use the nth term test on \\(\\sum_{n=2}^{\\infty}\\frac{5n-2}{4n+3}\\). Find \\(\\lim_{n\\to\\infty}a_n\\).",
    "command_verb": "find"
   },
   "key": {
    "form": "numeric",
    "expr": "5/4"
   },
   "steps": [
    {
     "text": "The general term.",
     "expr": "(5*n-2)/(4*n+3)",
     "relation": "new"
    },
    {
     "text": "Leading coefficients.",
     "expr": "5/4",
     "relation": "limit",
     "variable": "n",
     "point": "oo"
    }
   ],
   "calculator_status": "no_calculator",
   "skills": [
    "BC-SKL-10011"
   ]
  },
  {
   "id": "chk-3",
   "check_kind": "mcq",
   "format": "mcq",
   "bands": [
    "low"
   ],
   "archetype_id": "BC-QA-10001",
   "parameter_draw": {
    "form": "pseries",
    "power": "1/3",
    "coefficient": "6",
    "start": "1",
    "lead_top": "3",
    "constant_top": "1",
    "lead_bottom": "2",
    "constant_bottom": "5",
    "ratio": "1/3",
    "base": "4",
    "degree": "2"
   },
   "stem": {
    "text": "Let \\(a_n=\\frac{6}{\\sqrt[3]{n}}\\). Which statement about the nth term test applied to \\(\\sum_{n=1}^{\\infty}a_n\\) is correct?",
    "command_verb": "identify"
   },
   "key": {
    "form": "statement",
    "expr": "the limit is 0, so the test gives no conclusion"
   },
   "steps": [
    {
     "text": "The general term.",
     "expr": "6/n**(1/3)",
     "relation": "new"
    },
    {
     "text": "Its limit.",
     "expr": "0",
     "relation": "limit",
     "variable": "n",
     "point": "oo"
    }
   ],
   "options": [
    {
     "id": "A",
     "is_key": false,
     "label": "\\(\\lim a_n=6\\), so the series diverges.",
     "error_path": "BC-ERR-10007",
     "derivation": "the limit reported as the coefficient 6, the factor \\(n^{-1/3}\\) ignored"
    },
    {
     "id": "B",
     "is_key": false,
     "label": "\\(\\lim a_n=0\\), so the series converges.",
     "error_path": "BC-ERR-10008",
     "derivation": "the zero limit read as convergence"
    },
    {
     "id": "C",
     "is_key": true,
     "label": "\\(\\lim a_n=0\\), so the test gives no conclusion.",
     "error_path": null
    },
    {
     "id": "D",
     "is_key": false,
     "label": "The test shows divergence, because every term is positive.",
     "error_path": "BC-ERR-10009",
     "derivation": "the test named with its condition on the limit never checked"
    }
   ],
   "calculator_status": "no_calculator",
   "skills": [
    "BC-SKL-10013"
   ]
  }
 ],
 "delivery": [
  {
   "block": "orientation",
   "mode": "text",
   "reason": "rule 6: a statement of what a response shows",
   "sources": [
    "BC-CON-10005"
   ]
  },
  {
   "block": "ki-1",
   "mode": "text",
   "reason": "rule 6: BC-REP-11, 01, 04 on BC-SKL-10011 to 10013, none figure-bearing; the idea is a condition on one limit, not a process",
   "sources": [
    "BC-SKL-10011",
    "BC-SKL-10012",
    "BC-SKL-10013"
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
   "block": "err-BC-ERR-10007",
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
  }
 ],
 "refresher": [
  "ki-1",
  "err-BC-ERR-10007",
  "err-BC-ERR-10008",
  "err-BC-ERR-10009",
  "ex-1"
 ],
 "read_minutes": {
  "full": 4.1,
  "brief": 3.0
 },
 "word_count": {
  "full": 611,
  "brief": 447
 },
 "research_lines": [
  {
   "file": "research/units/unit-10-infinite-sequences-series.md",
   "line": "No converse is available: a limit of zero is consistent with convergence and with divergence, as the harmonic series shows"
  }
 ],
 "inferred": [
  {
   "claim": "A fluent solver writes the limit and the verdict and holds the division by n.",
   "settles": "Timing data per step once the fluency telemetry exists."
  },
  {
   "claim": "BC-QA-10001 records no calculator_status split and no FRQ example, so its multiple choice form is timed against Section I Part A at 2.14 minutes.",
   "settles": "Timing data on series items split by exam part."
  },
  {
   "claim": "The prediction and every non-text or text delivery choice serve better than the alternatives.",
   "settles": "The modality A/B in the build plan: skip rate and time to first credited success by mode."
  }
 ],
 "sources": [
  "BC-CON-10005",
  "BC-SKL-10011",
  "BC-SKL-10012",
  "BC-SKL-10013",
  "BC-EK-LIM-7A5",
  "ced:188",
  "BC-QA-10001",
  "BC-ERR-10007",
  "BC-ERR-10008",
  "BC-ERR-10009",
  "BC-MIS-10007",
  "BC-PRQ-06005",
  "BC-PRQ-10004",
  "BC-PRQ-10008",
  "BC-REP-11",
  "research/exam/exam-structure.md#Section and part layout",
  "research/question-analysis/question-archetypes.md#BC-QA-10001 Selecting a convergence test for a given series",
  "research/units/unit-10-infinite-sequences-series.md#10.3 The nth Term Test for Divergence",
  "sg-21:22"
 ]
}
```
