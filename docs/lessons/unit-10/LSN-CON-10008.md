---
title: LSN-CON-10008 Selection of a convergence test from the form of the terms
research_date: 2026-09-29
status: designed
purpose: Authoring spec for the concept lesson on BC-CON-10008, the selection of a convergence test from the form of the general term, built from authoring_bundle("BC-CON-10008") and the research files it cites, so an author fills plan 15's lesson record without making a teaching decision.
---

# LSN-CON-10008 Selection of a convergence test from the form of the terms

Concept BC-CON-10008 (skill BC-SKL-10021), topic 10.5 of Unit 10, BC only (ced:190, ced:193), loaded by two archetypes, BC-QA-10001 and BC-QA-10015. Hard parents BC-CON-10004 and BC-CON-10007 (docs/lessons/unit-10/README.md, section 1); no outside hard parent. It is the lesson where the series-test contrast is taught, since the 67-skill confusable component leaves no derived decision lesson (README, section 3).

## Prediction

Served first, both bands: an `mcq` on ex-1's own numbers. In \(\sum\frac{3\cdot2^n}{5^n}\) each term is \(\frac25\) of the one before, and the student says whether the series converges. Key A, it converges. The distractors are that it diverges and that it depends on the first term; both are false, and a student who knows the geometric series (the hard parent BC-CON-10004) can rule them out before the lesson states any selection cue. The resolution names the geometric form and the rule that the form of the general term picks the test, with no verdict word. Delivery: text. Source: BC-CON-10008 and the topic 10.5 section the key ideas cite.

## Orientation

Served text (26 words), from BC-CON-10008 `description_plain` ("read the shape of the general term and pick the test it fits") and the topic's Assessment behaviour paragraph: selection is scored implicitly, and a test that does not fit the series earns nothing even when the conclusion is correct (research/units/unit-10-infinite-sequences-series.md#10.5 Harmonic Series and p-Series, sg-21:23). The orientation states what a response must show. No count, no frequency.

## Key ideas

The skill maps two essential knowledge statements, BC-EK-LIM-7A11 (ced:193) and BC-EK-LIM-7A7 (ced:190).

- ki-1 (core, BC-EK-LIM-7A11). Paraphrase of the Required mathematical knowledge paragraph Decision cues: a constant quotient of consecutive terms points to the geometric test, factorials or nth powers to the ratio test, a factor of negative one to the n to the alternating series test, a rational expression in n to comparison or limit comparison. Notation line: the concept's `notation`. No anchor quote, to keep the brief band under its cap.
- ki-2 (extended, BC-EK-LIM-7A7). The reference series (geometric, harmonic, alternating harmonic, p-series), the integral test cue (a positive decreasing continuous function of n) and the exclusion statement that closes the list of assessed tests: the nth term, integral, comparison, limit comparison, alternating series and ratio tests (ced:193). Low band only. No anchor quote.

## Recognition

Two archetypes load BC-SKL-10021: BC-QA-10001 (family procedure-selection) and BC-QA-10015 (radius-interval). The examples and checks draw from BC-QA-10001, the archetype docs/lessons/unit-10/README.md, section 3, names for test selection.

- BC-QA-10001 (research/question-analysis/question-archetypes.md#BC-QA-10001 Selecting a convergence test for a given series): `common_givens` "a series of numbers in sigma or expanded form", "several series to classify together"; `asked_to_produce` "a convergence or divergence verdict naming the series", "the name of an applicable test", "a check of that test's conditions"; `typical_wording` "determine whether the series converges or diverges, and justify your answer". Its six general-term forms are a p-series multiple, a rational term with a nonzero limit, a geometric term, a polynomial over an exponential, an exponential over a factorial and an alternating p-series. `difficulty_variables` include "whether more than one test applies" and "whether the nth term test screens the series first".
- Shape: the multiple choice item BC-MCQ-PE2012-009; the free response record names 2024 Q6(a) and 2025 Q6(A) (research/units/unit-10-infinite-sequences-series.md#Archetype summary, a library gap in the archetype's `official_examples`).

The signal in the stem: a series in sigma form, a verdict requested and no test named. The near miss of the contrast pair is a sum request on a term with a constant quotient, from the geometric archetypes (BC-QA-10003, closed form): \(\frac{n^2}{3^n}\) and \(\frac{2}{3^n}\) both carry \(3^n\), and only the second has a constant quotient.

What says "not this concept": a named test in the stem (the test is then given and only its conditions are checked, sg-21:23); a request for a sum (BC-CON-10004); a series already classified as a reference series.

## Method choice

One strategy block, both bands.

- st-1, BC-QA-10001. Cue from `common_givens` and `asked_to_produce`: a sigma series, a verdict requested, no test named. Method, `expected_solution_path[0]` "read the general term" and `[1]` "match its form to a test whose conditions it meets": the test the form selects. Rival, `common_distractors` "using the geometric formula on a series without a constant ratio": a test chosen by a familiar symbol. Separating feature: a constant quotient of consecutive terms, checked before the test is named. Both cue fields exist, so the block is verified. The block carries the contrast pair. No served field opens with the reader's own label.
- BC-QA-10015's block is not served, to keep both bands under their caps; it presents a power series with its radius, which the unit teaches later [inferred: settled by a brief cap that admits a second block].

## Solution path

- ex-1, BC-QA-10001, both bands, no calculator. Draw: form geometric, coefficient 3, ratio 2/5, start 1 (the other spec keys are carried unused). \(a_n=\frac{3\cdot2^n}{5^n}\), quotient \(\frac25\), converges. No published item on BC-QA-10001 carries this draw (content/items_gen_unit10/ITM-GEN-10001-00 to 21 list none with all keys equal).
- ex-2, low band. Draw: form ratio_power, base 4, degree 2, coefficient 3, start 1. \(a_n=\frac{n^2}{4^n}\), quotient \(\frac{(n+1)^2}{4n^2}\), not constant, so the ratio test. Not equal to any published draw. The answer is a statement, the name of the test, so the example has no numeric key.
- ex-2 is faded from step 3: steps 1 and 2 (the term and the quotient) are shown, the student names the test, and steps 3 and 4 then reveal. The fade falls there because reading the term and forming the quotient repeat ex-1 and the choice is what the student must produce.
- Steps follow `expected_solution_path`: the general term (new), the quotient of consecutive terms (new), its simplification (equivalent), and the condition and verdict (no value). ex-2 stops at naming the ratio test, because docs/lessons/unit-10/README.md, section 1 allows this design to assume geometric, harmonic and p-series behaviour and nothing more [inferred]. A fluent solver writes the quotient and the condition; the reading of the term is held. No productive-failure comparison: BC-CON-10008 is not in `PRODUCTIVE_FAILURE_TARGETS`.

## Scoring

None. BC-QA-10001 lists no `point_types`, so the lesson carries no what_a_reader_scores entry, no step carries a point tag and the lesson says nothing about points (plan 15, R14; README section 3). The `scoring_pattern` says that where a test is named by the prompt only that test earns credit (sg-21:23) and that where the choice is free the verdict earns nothing unless the chosen test's conditions are established (sg-25:25); it names no BC-PT and is not served.

## Traps

Two active errors meet the skill, in the bundle's order: BC-ERR-10009 (BC-MIS-10007 high, BC-MIS-99009 high) and BC-ERR-10015 (BC-MIS-10007 high, BC-MIS-10024 medium). Both are served in both bands, on ex-1's draw. Both carry fix prompt true, since each pair is distinct.

- err-BC-ERR-10009: the geometric test named with no quotient shown, the empty set, against the quotient \(\frac25\) written. No possible reason line (brief band words); the record links BC-MIS-10007 and BC-MIS-99009.
- err-BC-ERR-10015: the alternating series test applied to a series of positive terms, the sign of the terms as -1 against 1. No possible reason line.

## Representations

None. The topic's Representations paragraph names BC-REP-11, 01 and 04 and the conversions general term to the name of a test whose hypotheses it satisfies and a standard series to its known behaviour; nothing figure-shaped (docs/lessons/unit-10/README.md, section 6).

## Prerequisite bridge

BC-PRQ-10005 and BC-PRQ-10008, each from its `description_plain` and `failure_signature`, gated by state, in both bands.

## Time

Section I Part A, 2.14 minutes (research/exam/exam-structure.md#Section and part layout), the multiple choice form; BC-QA-10001 records no FRQ example with points [inferred]. A fluent solver writes the quotient, its simplification and the condition; the reading of the term is held, and on an exam item the choice among tests is made in the head (docs/lessons/unit-10/README.md, section 5, "the choice among tests"). The minutes go on the quotient.

## Checks

- chk-1, completion of ex-1, both bands. The general term given, the quotient asked. Key \(\frac25\).
- chk-2, isomorph, both bands, no calculator. Draw: form geometric, coefficient 2, ratio 4/5, start 1. \(\sum\frac{2\cdot4^n}{5^n}\), key \(\frac45\). Not equal to a published draw.
- chk-3, MCQ, low band. Draw: form ratio_power, base 5, degree 3, coefficient 3, start 1. \(\sum\frac{n^3}{5^n}\). Key: the ratio test, since the term has an nth power and \(n^3\). Distractors: the geometric test with \(r=\frac15\) (BC-ERR-10009, the quotient never checked); the alternating series test on positive terms (BC-ERR-10015); the p-series test named for a term that is not \(\frac1{n^p}\) (BC-ERR-10009). Two distractors share BC-ERR-10009 because the record links only two errors.

## Delivery

- orientation, ki-1, ki-2: text. Rule 6: BC-REP-11 and 04 on BC-SKL-10021, none figure-bearing (docs/lessons/unit-10/README.md, section 6). No block is drawn, so the record carries `no_figure_reason`.
- ex-1, ex-2, the two error blocks: step_reveal. Rule 1.

## Band plan

- Low (full): prediction, orientation, bridges, ki-1 and ki-2, st-1 with the contrast pair, ex-1, chk-1, the two error blocks, ex-2 (faded from step 3), chk-2, chk-3. 555 words, 3.7 minutes.
- Mid (brief): prediction, orientation, bridges, ki-1, st-1 with the contrast pair, ex-1, chk-1, err-BC-ERR-10009, err-BC-ERR-10015, chk-2. 394 words, 2.7 minutes.
- Refresher: ki-1, the two error blocks, ex-1.

## Sources

- BC-CON-10008; BC-SKL-10021; BC-EK-LIM-7A11, BC-EK-LIM-7A7; ced:190, ced:193
- BC-QA-10001, BC-QA-10015
- BC-ERR-10009, BC-ERR-10015; BC-MIS-10007, BC-MIS-99009, BC-MIS-10024
- BC-PRQ-10005, BC-PRQ-10008
- sg-21:23, sg-25:25
- research/units/unit-10-infinite-sequences-series.md#10.5 Harmonic Series and p-Series
- research/question-analysis/question-archetypes.md#BC-QA-10001 Selecting a convergence test for a given series
- research/exam/exam-structure.md#Section and part layout
- [inferred] the held step, Part A for a no-point archetype, ex-2 stopping at the name of the test, the unserved BC-QA-10015 block and the delivery choice, each settled as the inferred array states.

## Machine record

```json
{
 "id": "LSN-CON-10008",
 "kind": "concept",
 "target_id": "BC-CON-10008",
 "unit": "10",
 "skills": [
  "BC-SKL-10021"
 ],
 "prediction": {
  "id": "pr-1",
  "stem": {
   "text": "In \\(\\sum_{n=1}^{\\infty}\\frac{3\\cdot2^n}{5^n}\\) each term is \\(\\frac25\\) of the one before. Does the series converge?",
   "command_verb": "predict"
  },
  "format": "mcq",
  "options": [
   {
    "id": "A",
    "label": "It converges.",
    "is_key": true
   },
   {
    "id": "B",
    "label": "It diverges.",
    "is_key": false
   },
   {
    "id": "C",
    "label": "It depends on the first term.",
    "is_key": false
   }
  ],
  "resolution": "A fixed quotient of \\(\\frac25\\) makes it geometric, and a quotient below 1 in size gives convergence. The form of the general term picks the test before any computing.",
  "sources": [
   "BC-CON-10008",
   "research/units/unit-10-infinite-sequences-series.md#10.5 Harmonic Series and p-Series"
  ]
 },
 "no_figure_reason": "Test selection is a match between the written form of one general term and a named test. No skill carries a figure-bearing representation and no key idea describes a process.",
 "orientation": {
  "text": "A response reads the form of the general term, names a test whose conditions the series meets, checks them, and states the verdict naming the series.",
  "sources": [
   "BC-CON-10008",
   "research/units/unit-10-infinite-sequences-series.md#10.5 Harmonic Series and p-Series"
  ]
 },
 "key_ideas": [
  {
   "id": "ki-1",
   "ek_id": "BC-EK-LIM-7A11",
   "depth": "core",
   "text": "Read the general term before computing. A constant quotient of consecutive terms selects the geometric test. A factorial or an nth power selects the ratio test, \\((-1)^n\\) the alternating series test, and a rational term in n comparison.",
   "notation": "test selection; decision cues",
   "quote": null,
   "sources": [
    "BC-EK-LIM-7A11",
    "ced:193",
    "research/units/unit-10-infinite-sequences-series.md#10.5 Harmonic Series and p-Series"
   ]
  },
  {
   "id": "ki-2",
   "ek_id": "BC-EK-LIM-7A7",
   "depth": "extended",
   "text": "Geometric, harmonic, alternating harmonic and p-series are the reference series, so a term of that shape is decided by known behaviour. A positive decreasing function of n selects the integral test. The assessed tests are the nth term, integral, comparison, limit comparison, alternating series and ratio tests.",
   "notation": "reference series",
   "quote": null,
   "sources": [
    "BC-EK-LIM-7A7",
    "BC-EK-LIM-7A11",
    "ced:190",
    "ced:193",
    "research/units/unit-10-infinite-sequences-series.md#10.5 Harmonic Series and p-Series"
   ]
  }
 ],
 "strategy": [
  {
   "id": "st-1",
   "archetype_id": "BC-QA-10001",
   "cue": "A series in sigma form and a request for a verdict, with no test named.",
   "method": "The test that the form of \\(a_n\\) selects.",
   "rival": "A test chosen by a familiar symbol, such as any \\(b^n\\) taken as geometric.",
   "separating_feature": "A constant quotient of consecutive terms, checked before the test is named.",
   "sources": [
    "BC-QA-10001",
    "research/question-analysis/question-archetypes.md#BC-QA-10001 Selecting a convergence test for a given series"
   ],
   "evidence_tag": "verified",
   "contrast": {
    "this": {
     "text": "Determine whether \\(\\sum_{n=1}^{\\infty}\\frac{n^2}{3^n}\\) converges or diverges. Name a test whose conditions the series meets.",
     "archetype_id": "BC-QA-10001"
    },
    "not_this": {
     "text": "Find the sum of \\(\\sum_{n=1}^{\\infty}\\frac{2}{3^n}\\).",
     "why_not": "The quotient of consecutive terms is constant, so it is geometric and has a sum formula."
    },
    "feature": "\\(3^n\\) in both. Only \\(\\frac{2}{3^n}\\) has a constant quotient."
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
    "form": "geometric",
    "power": "3/2",
    "coefficient": "3",
    "start": "1",
    "lead_top": "3",
    "constant_top": "1",
    "lead_bottom": "2",
    "constant_bottom": "5",
    "ratio": "2/5",
    "base": "4",
    "degree": "2"
   },
   "problem": {
    "text": "Name the test that \\(\\sum_{n=1}^{\\infty}\\frac{3\\cdot2^n}{5^n}\\) fits, give its ratio, and state the verdict.",
    "command_verb": "determine"
   },
   "calculator_status": "no_calculator",
   "steps": [
    {
     "cue": "Read the general term.",
     "why": "The form picks the test before any computing.",
     "expr": "3*2**n/5**n",
     "relation": "new"
    },
    {
     "cue": "Quotient of consecutive terms.",
     "why": "A constant quotient selects the geometric test.",
     "expr": "(3*2**(n+1)/5**(n+1))/(3*2**n/5**n)",
     "relation": "new"
    },
    {
     "cue": "Simplify it.",
     "why": "The n cancels, so the quotient is constant.",
     "expr": "2/5",
     "relation": "equivalent"
    },
    {
     "cue": "Check the condition.",
     "why": "\\(|r|=\\frac25<1\\), so the series converges."
    }
   ],
   "answer": {
    "form": "numeric",
    "expr": "2/5"
   }
  },
  {
   "id": "ex-2",
   "archetype_id": "BC-QA-10001",
   "bands": [
    "low"
   ],
   "fade_from": 3,
   "parameter_draw": {
    "form": "ratio_power",
    "power": "3/2",
    "coefficient": "3",
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
    "text": "Name the test that \\(\\sum_{n=1}^{\\infty}\\frac{n^2}{4^n}\\) fits and say why the geometric test does not.",
    "command_verb": "determine"
   },
   "calculator_status": "no_calculator",
   "steps": [
    {
     "cue": "Read the general term.",
     "why": "The form picks the test before any computing.",
     "expr": "n**2/4**n",
     "relation": "new"
    },
    {
     "cue": "Quotient of consecutive terms.",
     "why": "A constant quotient would select the geometric test.",
     "expr": "((n+1)**2/4**(n+1))/(n**2/4**n)",
     "relation": "new"
    },
    {
     "cue": "Simplify it.",
     "why": "The quotient still depends on n, so it is not geometric.",
     "expr": "(n+1)**2/(4*n**2)",
     "relation": "equivalent"
    },
    {
     "cue": "Match the form to a test.",
     "why": "An nth power with \\(n^2\\) selects the ratio test, which is taught in its own lesson."
    }
   ],
   "answer": {
    "form": "statement",
    "expr": "the ratio test, since the quotient is not constant"
   }
  }
 ],
 "what_a_reader_scores": [],
 "common_errors": [
  {
   "error_id": "BC-ERR-10009",
   "observed_behavior": "The response names a convergence test and states a conclusion without establishing the conditions the test requires.",
   "scoring_consequence": "Points tied to the conditions or to the justification are lost even when the verdict is right (sg-21:22).",
   "wrong_step": {
    "text": "Geometric, so it converges.",
    "expr": "EmptySet"
   },
   "right_step": {
    "text": "The quotient is \\(\\frac25\\), constant.",
    "expr": "2/5"
   },
   "relation": "distinct",
   "possible_reason": null,
   "sources": [
    "BC-ERR-10009"
   ],
   "fix_prompt": true
  },
  {
   "error_id": "BC-ERR-10015",
   "observed_behavior": "The response applies a comparison test to an alternating series, or applies the alternating series test to a series of positive terms.",
   "scoring_consequence": "The analysis point at that endpoint is lost, and the interval point with it (sg-25:25).",
   "wrong_step": {
    "text": "Alternating series test: terms decrease to 0.",
    "expr": "-1"
   },
   "right_step": {
    "text": "All terms are positive, so it does not apply.",
    "expr": "1"
   },
   "relation": "distinct",
   "possible_reason": null,
   "sources": [
    "BC-ERR-10015"
   ],
   "fix_prompt": true
  }
 ],
 "representations": null,
 "prerequisite_bridges": [
  {
   "prq_id": "BC-PRQ-10005",
   "text": "Divide consecutive terms and confirm the quotient is constant."
  },
  {
   "prq_id": "BC-PRQ-10008",
   "text": "Read \\(a_n\\) from sigma form."
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
    4
   ]
  },
  "skipped_steps": {
   "ex-1": [
    1
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
   "archetype_id": "BC-QA-10001",
   "parameter_draw": {
    "form": "geometric",
    "power": "3/2",
    "coefficient": "3",
    "start": "1",
    "lead_top": "3",
    "constant_top": "1",
    "lead_bottom": "2",
    "constant_bottom": "5",
    "ratio": "2/5",
    "base": "4",
    "degree": "2"
   },
   "completes": "ex-1",
   "stem": {
    "text": "For \\(a_n=\\frac{3\\cdot2^n}{5^n}\\), simplify \\(\\frac{a_{n+1}}{a_n}\\).",
    "command_verb": "find"
   },
   "key": {
    "form": "numeric",
    "expr": "2/5"
   },
   "steps": [
    {
     "text": "The quotient.",
     "expr": "(3*2**(n+1)/5**(n+1))/(3*2**n/5**n)",
     "relation": "new"
    },
    {
     "text": "Simplified.",
     "expr": "2/5",
     "relation": "equivalent"
    }
   ],
   "calculator_status": "no_calculator",
   "skills": [
    "BC-SKL-10021"
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
    "form": "geometric",
    "power": "3/2",
    "coefficient": "2",
    "start": "1",
    "lead_top": "3",
    "constant_top": "1",
    "lead_bottom": "2",
    "constant_bottom": "5",
    "ratio": "4/5",
    "base": "4",
    "degree": "2"
   },
   "stem": {
    "text": "Name the ratio r for the geometric test on \\(\\sum_{n=1}^{\\infty}\\frac{2\\cdot4^n}{5^n}\\).",
    "command_verb": "find"
   },
   "key": {
    "form": "numeric",
    "expr": "4/5"
   },
   "steps": [
    {
     "text": "The quotient.",
     "expr": "(2*4**(n+1)/5**(n+1))/(2*4**n/5**n)",
     "relation": "new"
    },
    {
     "text": "Simplified.",
     "expr": "4/5",
     "relation": "equivalent"
    }
   ],
   "calculator_status": "no_calculator",
   "skills": [
    "BC-SKL-10021"
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
    "form": "ratio_power",
    "power": "3/2",
    "coefficient": "3",
    "start": "1",
    "lead_top": "3",
    "constant_top": "1",
    "lead_bottom": "2",
    "constant_bottom": "5",
    "ratio": "1/3",
    "base": "5",
    "degree": "3"
   },
   "stem": {
    "text": "Which test's conditions does \\(\\sum_{n=1}^{\\infty}\\frac{n^3}{5^n}\\) meet?",
    "command_verb": "identify"
   },
   "key": {
    "form": "statement",
    "expr": "the ratio test, since the term has an nth power and n^3"
   },
   "steps": [
    {
     "text": "The quotient of consecutive terms.",
     "expr": "((n+1)**3/5**(n+1))/(n**3/5**n)",
     "relation": "new"
    },
    {
     "text": "Simplified, still depending on n.",
     "expr": "(n+1)**3/(5*n**3)",
     "relation": "equivalent"
    }
   ],
   "options": [
    {
     "id": "A",
     "is_key": true,
     "label": "The ratio test: the term has an nth power and \\(n^3\\).",
     "error_path": null
    },
    {
     "id": "B",
     "is_key": false,
     "label": "The geometric test: \\(r=\\frac15<1\\).",
     "error_path": "BC-ERR-10009",
     "derivation": "the geometric test named because 5^n is in the denominator, the quotient never checked, and r read as 1/5"
    },
    {
     "id": "C",
     "is_key": false,
     "label": "The alternating series test: the terms decrease to 0.",
     "error_path": "BC-ERR-10015",
     "derivation": "the alternating series test applied to a series of positive terms"
    },
    {
     "id": "D",
     "is_key": false,
     "label": "The p-series test: \\(n^3\\) is a power of n.",
     "error_path": "BC-ERR-10009",
     "derivation": "the p-series test named for a term that is not \\(\\frac1{n^p}\\)"
    }
   ],
   "calculator_status": "no_calculator",
   "skills": [
    "BC-SKL-10021"
   ]
  }
 ],
 "delivery": [
  {
   "block": "orientation",
   "mode": "text",
   "reason": "rule 6: a statement of what a response shows",
   "sources": [
    "BC-CON-10008"
   ]
  },
  {
   "block": "ki-1",
   "mode": "text",
   "reason": "rule 6: BC-REP-11, 04 on BC-SKL-10021, none figure-bearing; the idea is a match between a written form and a named test, not a process (docs/lessons/unit-10/README.md, section 6)",
   "sources": [
    "BC-SKL-10021"
   ]
  },
  {
   "block": "ki-2",
   "mode": "text",
   "reason": "rule 6: BC-REP-11, 04 on BC-SKL-10021, none figure-bearing",
   "sources": [
    "BC-SKL-10021"
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
  }
 ],
 "refresher": [
  "ki-1",
  "err-BC-ERR-10009",
  "err-BC-ERR-10015",
  "ex-1"
 ],
 "read_minutes": {
  "full": 3.7,
  "brief": 2.7
 },
 "word_count": {
  "full": 554,
  "brief": 393
 },
 "research_lines": [
  {
   "file": "research/units/unit-10-infinite-sequences-series.md",
   "line": "A constant quotient of consecutive terms points to the geometric test"
  }
 ],
 "inferred": [
  {
   "claim": "A fluent solver writes the quotient, its simplification and the condition, and holds the reading of the general term.",
   "settles": "Timing data per step once the fluency telemetry exists."
  },
  {
   "claim": "BC-QA-10001 records no FRQ example with points, so its multiple choice form is timed against Section I Part A at 2.14 minutes.",
   "settles": "Timing data on series items split by exam part."
  },
  {
   "claim": "ex-2 stops at naming the ratio test, because the README allows this design to assume only geometric, harmonic and p-series behaviour; the test itself is taught in its own lesson.",
   "settles": "A design decision on whether selection examples may run tests taught later."
  },
  {
   "claim": "The BC-QA-10015 block is not served, to keep both bands under their caps; the endpoint archetype presents a power series that the unit teaches later.",
   "settles": "A brief cap that admits a second block."
  },
  {
   "claim": "The delivery choice serves better than the alternatives.",
   "settles": "The modality A/B in the build plan: skip rate and time to first credited success by mode."
  }
 ],
 "sources": [
  "BC-CON-10008",
  "BC-SKL-10021",
  "BC-EK-LIM-7A11",
  "BC-EK-LIM-7A7",
  "ced:190",
  "ced:193",
  "BC-QA-10001",
  "BC-QA-10015",
  "BC-ERR-10009",
  "BC-ERR-10015",
  "BC-PRQ-10005",
  "BC-PRQ-10008",
  "BC-REP-11",
  "research/exam/exam-structure.md#Section and part layout",
  "research/question-analysis/question-archetypes.md#BC-QA-10001 Selecting a convergence test for a given series",
  "research/units/unit-10-infinite-sequences-series.md#10.5 Harmonic Series and p-Series",
  "sg-21:22",
  "sg-25:25"
 ]
}
```
